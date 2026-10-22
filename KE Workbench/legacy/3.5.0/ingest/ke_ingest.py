#!/usr/bin/env python3
"""
KE Ingest — bring legacy knowledge artifacts (vocabularies, taxonomies, ontologies)
into line with the Part III standards of "Semantic Governance: Services,
Architecture & Integration" v1.9 (Draft), including the §3.11 metadata field set.

What it does, per run:
  1. Reads every Turtle, N-Triples or RDF/XML file given and works out what each one is (SKOS vocabulary,
     OWL taxonomy, OWL ontology) from its header.
  2. Mints new IRIs under the base URL with the §3.2 URI patterns
       /vocabulary/{domain}/{term}   /taxonomy/{domain}/{Concept}
       /ontology/{domain}/{Class}    /shapes/{domain}/{ClassShape}
     and rewrites every reference, across all files, through one crosswalk.
  3. Rebuilds the metadata: sentence-case labels tagged @en, preferred labels,
     definitions (from the linked vocabulary term where the class has none, or from
     the config), rdfs:isDefinedBy, lifecycle status, semantic version, a single
     author, created dates kept from the source and modified dates set to now.
  4. Writes generated titles and descriptions on each asset header.
  5. Drops properties that don't belong (tool bookkeeping, legacy status flags,
     misused annotations, stub subjects) — everything not on the allow-list.
  6. Moves SHACL shapes into their own shapes graph.
  7. Checks the output against the Part III rules and writes a report, an
     old→new IRI crosswalk and a PROV-O change record.

v1.9 changes:
  - Taxonomies are always SKOS (§3.11): a taxonomy authored as OWL classes is converted
    (owl:Class → skos:Concept, rdfs:subClassOf → skos:broader). Config "taxonomiesAsSkos": false
    turns this off.
  - Class, taxonomy concept and vocabulary term IRIs join their words with hyphens, lower case (§3.2 as amended
    for Baseline Core v1.0: polymorphic terms are phrases, never new words).
  - Links from a taxonomy concept to its vocabulary term are written as core:hasPrimaryTerm and
    dcterms:subject (dc:subject is still read on input).
  - Asset headers carry the §3.11 fields: vaem:namespace, vann:preferredNamespacePrefix,
    owl:versionIRI, dcterms:publisher, dcterms:conformsTo, dcterms:subject and, on taxonomies,
    dcterms:source (the vocabularies its concepts draw on). Values come from the config.
  - Dates keep their datatype: a date-only value is written as xsd:date, never as an invalid
    xsd:dateTime.
  - Numbered labels ("01. Data governance") lose the number, which moves to skos:notation;
    "&" in a preferred label is spelled out as "and".

No third-party packages: runs with the Python 3.8+ standard library.
Inputs: .ttl .nt (Turtle/N-Triples) and .rdf .rdfs .owl .xml (RDF/XML; .owl is sniffed).

Usage:
  python3 ke_ingest.py input/ -o output                 # ttl/ and trig/ subfolders
  python3 ke_ingest.py input/*.owl -o output --ttl-dir turtle --trig-dir graphs
  python3 ke_ingest.py input/ -r -o output --timestamp 2026-10-15T20:00:00-05:00

The KE Workbench Ingestion page runs the same code through proxy.py.
"""
import argparse, collections, csv, datetime, json, pathlib, re, sys

# ─────────────────────────────────────────────────────────────────────────────
# Namespaces
# ─────────────────────────────────────────────────────────────────────────────
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
OWL = 'http://www.w3.org/2002/07/owl#'
XSD = 'http://www.w3.org/2001/XMLSchema#'
SKOS = 'http://www.w3.org/2004/02/skos/core#'
DCT = 'http://purl.org/dc/terms/'
DC = 'http://purl.org/dc/elements/1.1/'
SH = 'http://www.w3.org/ns/shacl#'
VANN = 'http://purl.org/vocab/vann/'
VAEM = 'http://www.linkedmodel.org/schema/vaem#'
SUBJECT_IN = (DC + 'subject', DCT + 'subject')     # predicates read as a link to a vocabulary term (plus core:hasPrimaryTerm)
PROV = 'http://www.w3.org/ns/prov#'

# Terms: ('I', iri) | ('B', id) | ('L', lexical, lang, datatype)
def I(v): return ('I', v)
def L(v, lang=None, dt=None): return ('L', v, lang, dt)
TYPE = I(RDF + 'type')

# ─────────────────────────────────────────────────────────────────────────────
# Turtle reader (RDF 1.1 Turtle, no RDF-star)
# ─────────────────────────────────────────────────────────────────────────────
_PNB = 'A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD'
_PN = _PNB + '0-9_\\-\u00B7'
RX_PREFIX = re.compile('([' + _PNB + '](?:[' + _PN + ']|\\.(?=[' + _PN + ']))*)?:')
RX_LOCAL = re.compile('(?:[' + _PN + ':%]|\\\\[_~.\\-!$&\'()*+,;=/?#@%]|\\.(?=[' + _PN + ':%\\\\]))*')
RX_NUM = re.compile(r'[+-]?(?:[0-9]+\.[0-9]*[eE][+-]?[0-9]+|\.[0-9]+[eE][+-]?[0-9]+|[0-9]+[eE][+-]?[0-9]+|[0-9]*\.[0-9]+|[0-9]+)')
_ESC = {'t': '\t', 'b': '\b', 'n': '\n', 'r': '\r', 'f': '\f', '"': '"', "'": "'", '\\': '\\'}

def _unescape(s):
    def rep(m):
        e = m.group(1)
        return _ESC[e] if e in _ESC else chr(int(e[1:], 16))
    return re.sub(r'\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|[tbnrf"\'\\])', rep, s)

class TurtleError(ValueError):
    pass

def _tokenize(src):
    toks, i, n, line = [], 0, len(src), 1
    def push(t, v=None): toks.append((t, v, line))
    while i < n:
        c = src[i]
        if c == '\n': line += 1; i += 1; continue
        if c in ' \t\r': i += 1; continue
        if c == '#':
            while i < n and src[i] != '\n': i += 1
            continue
        if c == '<':
            m = re.compile(r'<([^<>"{}|^`\\\s]*)>').match(src, i)
            if not m: raise TurtleError(f'line {line}: bad IRI')
            push('IRI', _unescape(m.group(1))); i = m.end(); continue
        if c in '"\'':
            q = c * 3 if src.startswith(c * 3, i) else c
            j, buf = i + len(q), []
            while True:
                if j >= n: raise TurtleError(f'line {line}: unterminated string')
                if src[j] == '\\': buf.append(src[j:j + 2]); j += 2; continue
                if src.startswith(q, j): break
                if len(q) == 1 and src[j] in '\r\n': raise TurtleError(f'line {line}: newline in string')
                if src[j] == '\n': line += 1
                buf.append(src[j]); j += 1
            push('STR', _unescape(''.join(buf))); i = j + len(q); continue
        if c == '@':
            m = re.compile(r'@([a-zA-Z]+(?:-[a-zA-Z0-9]+)*)').match(src, i)
            if not m: raise TurtleError(f'line {line}: bad @ token')
            w = m.group(1)
            if w in ('prefix', 'base'): push(w.upper(), '@')
            else: push('LANG', w.lower())
            i = m.end(); continue
        if src.startswith('^^', i): push('^^'); i += 2; continue
        if c in '.;,[]()' and not (c == '.' and i + 1 < n and src[i + 1].isdigit()):
            push(c); i += 1; continue
        if src.startswith('_:', i):
            m = re.compile('_:([' + _PN + '](?:[' + _PN + ']|\\.(?=[' + _PN + ']))*)').match(src, i)
            if not m: raise TurtleError(f'line {line}: bad blank node')
            push('BNODE', m.group(1)); i = m.end(); continue
        m = RX_NUM.match(src, i)
        if m and (c != '.' or (i + 1 < n and src[i + 1].isdigit())):
            num = m.group(0)
            dt = 'double' if re.search('[eE]', num) else ('decimal' if '.' in num else 'integer')
            push('NUM', (num, XSD + dt)); i = m.end(); continue
        m = re.compile(r'(PREFIX|BASE)\b', re.I).match(src, i)
        if m and not re.compile(r'[A-Za-z]+:').match(src, i):
            push(m.group(1).upper(), 'sparql'); i = m.end(); continue
        m = re.compile(r'(true|false)\b').match(src, i)
        if m and not src.startswith(':', m.end()):
            push('BOOL', m.group(1)); i = m.end(); continue
        if c == 'a' and i + 1 < n and src[i + 1] in ' \t\r\n<["\'(_#':
            push('A'); i += 1; continue
        m = RX_PREFIX.match(src, i)
        if m:
            lm = RX_LOCAL.match(src, m.end())
            local = lm.group(0) if lm else ''
            push('PNAME', (m.group(1) or '', re.sub(r'\\(.)', r'\1', local)))
            i = m.end() + len(local); continue
        raise TurtleError(f'line {line}: unexpected {src[i:i + 20].splitlines()[0]!r}')
    toks.append(('EOF', None, line))
    return toks

def parse_turtle(text, base=''):
    """Return (triples, prefixes). Blank nodes get ids unique to this parse."""
    toks, k = _tokenize(text), [0]
    prefixes, triples, bn = {}, [], [0]
    uid = 'p%x_' % (id(text) & 0xffff)

    def peek(): return toks[k[0]]
    def nxt():
        t = toks[k[0]]; k[0] += 1; return t
    def expect(tt):
        t = nxt()
        if t[0] != tt: raise TurtleError(f'line {t[2]}: expected {tt}, found {t[0]}')
        return t
    def fresh():
        bn[0] += 1; return ('B', uid + 'g%d' % bn[0])
    def iri_of(t):
        if t[0] == 'IRI':
            v = t[1]
            if not re.match(r'[a-zA-Z][\w+.-]*:', v): v = base + v
            return I(v)
        if t[0] == 'PNAME':
            p, l = t[1]
            if p not in prefixes: raise TurtleError(f'line {t[2]}: undefined prefix "{p}:"')
            return I(prefixes[p] + l)
        return None
    def emit(s, p, o): triples.append((s, p, o))

    def collection():
        items = []
        while peek()[0] != ')':
            if peek()[0] == 'EOF': raise TurtleError('unterminated collection')
            items.append(obj())
        nxt()
        if not items: return I(RDF + 'nil')
        head = cur = fresh()
        for idx, it in enumerate(items):
            emit(cur, I(RDF + 'first'), it)
            nx = I(RDF + 'nil') if idx == len(items) - 1 else fresh()
            emit(cur, I(RDF + 'rest'), nx); cur = nx
        return head
    def bnode_list():
        b = fresh()
        if peek()[0] != ']': pred_obj_list(b)
        expect(']'); return b
    def obj():
        t = nxt()
        r = iri_of(t)
        if r: return r
        if t[0] == 'BNODE': return ('B', uid + 'u_' + t[1])
        if t[0] == '[': return bnode_list()
        if t[0] == '(': return collection()
        if t[0] == 'NUM': return L(t[1][0], None, t[1][1])
        if t[0] == 'BOOL': return L(t[1], None, XSD + 'boolean')
        if t[0] == 'STR':
            if peek()[0] == 'LANG': return L(t[1], nxt()[1], None)
            if peek()[0] == '^^':
                nxt(); d = iri_of(nxt())
                if not d: raise TurtleError(f'line {t[2]}: bad datatype')
                return L(t[1], None, d[1])
            return L(t[1])
        raise TurtleError(f'line {t[2]}: unexpected {t[0]} in object position')
    def verb():
        t = nxt()
        if t[0] == 'A': return TYPE
        r = iri_of(t)
        if r: return r
        raise TurtleError(f'line {t[2]}: expected a predicate, found {t[0]}')
    def pred_obj_list(s):
        while True:
            p = verb(); emit(s, p, obj())
            while peek()[0] == ',': nxt(); emit(s, p, obj())
            if peek()[0] != ';': return
            while peek()[0] == ';': nxt()
            if peek()[0] in ('.', ']', 'EOF'): return

    while peek()[0] != 'EOF':
        t = peek()
        if t[0] == 'PREFIX':
            nxt(); pn = nxt()
            if pn[0] != 'PNAME' or pn[1][1]: raise TurtleError(f'line {pn[2]}: bad prefix declaration')
            prefixes[pn[1][0]] = expect('IRI')[1]
            if t[1] == '@': expect('.')
            continue
        if t[0] == 'BASE':
            nxt(); base = expect('IRI')[1]
            if t[1] == '@': expect('.')
            continue
        nxt()
        if t[0] == '[':
            s = bnode_list()
            if peek()[0] == '.': nxt(); continue
        elif t[0] == '(':
            s = collection()
        elif t[0] == 'BNODE':
            s = ('B', uid + 'u_' + t[1])
        else:
            s = iri_of(t)
            if not s: raise TurtleError(f'line {t[2]}: expected a subject, found {t[0]}')
        pred_obj_list(s)
        expect('.')
    return triples, prefixes

# ─────────────────────────────────────────────────────────────────────────────
# RDF/XML reader (.rdf, .rdfs, .owl, .xml) — the core of the W3C RDF/XML syntax:
# node elements, rdf:about/ID/nodeID, property attributes, rdf:resource,
# rdf:datatype, xml:lang, xml:base, rdf:li, parseType Resource/Collection/Literal.
# ─────────────────────────────────────────────────────────────────────────────
_XMLNS = '{http://www.w3.org/XML/1998/namespace}'
_R = '{' + RDF + '}'
_RDF_SYNTAX_ATTRS = {_R + a for a in ('about', 'ID', 'nodeID', 'resource', 'datatype', 'parseType', 'type')}

def parse_rdfxml(data, base=''):
    import xml.etree.ElementTree as ET, urllib.parse
    if isinstance(data, str): data = data.encode('utf-8')
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        raise TurtleError(f'RDF/XML: {e}')
    triples, bn = [], [0]
    uid = 'x%x_' % (id(data) & 0xffff)
    def fresh():
        bn[0] += 1; return ('B', uid + 'g%d' % bn[0])
    def tag_iri(tag):
        if tag.startswith('{'):
            ns, local = tag[1:].split('}', 1); return ns + local
        raise TurtleError(f'RDF/XML: element <{tag}> has no namespace')
    def resolve(ref, b):
        if re.match(r'[a-zA-Z][\w+.-]*:', ref): return ref
        if not b: return ref
        if ref == '': return b.split('#')[0]
        return urllib.parse.urljoin(b, ref)
    def emit(s_, p_, o_): triples.append((s_, p_, o_))
    def ctx(el, b, lang):
        if el.get(_XMLNS + 'base'): b = resolve(el.get(_XMLNS + 'base'), b)
        return b, el.get(_XMLNS + 'lang', lang)
    def subject_of(el, b):
        if el.get(_R + 'about') is not None: return I(resolve(el.get(_R + 'about'), b))
        if el.get(_R + 'ID') is not None: return I(resolve('#' + el.get(_R + 'ID'), b))
        if el.get(_R + 'nodeID') is not None: return ('B', uid + 'n_' + el.get(_R + 'nodeID'))
        return fresh()
    def prop_attrs(s_, el, b, lang):
        for k, v in el.attrib.items():
            if k in _RDF_SYNTAX_ATTRS or k.startswith(_XMLNS):
                if k == _R + 'type': emit(s_, TYPE, I(resolve(v, b)))
                continue
            emit(s_, I(tag_iri(k)), L(v, lang))
    def node(el, b, lang):
        b, lang = ctx(el, b, lang)
        s_ = subject_of(el, b)
        if el.tag != _R + 'Description': emit(s_, TYPE, I(tag_iri(el.tag)))
        prop_attrs(s_, el, b, lang)
        li = [0]
        for c in el: prop(s_, c, b, lang, li)
        return s_
    def prop(s_, el, b, lang, li):
        b, lang = ctx(el, b, lang)
        p_ = tag_iri(el.tag)
        if p_ == RDF + 'li':
            li[0] += 1; p_ = RDF + '_%d' % li[0]
        p_ = I(p_)
        pt = el.get(_R + 'parseType')
        if pt == 'Resource':
            o_ = fresh(); emit(s_, p_, o_)
            inner = [0]
            for c in el: prop(o_, c, b, lang, inner)
            return
        if pt == 'Collection':
            items = [node(c, b, lang) for c in el]
            if not items: emit(s_, p_, I(RDF + 'nil')); return
            head = cur = fresh(); emit(s_, p_, head)
            for i, it in enumerate(items):
                emit(cur, I(RDF + 'first'), it)
                nx = I(RDF + 'nil') if i == len(items) - 1 else fresh()
                emit(cur, I(RDF + 'rest'), nx); cur = nx
            return
        if pt == 'Literal':
            inner = (el.text or '') + ''.join(ET.tostring(c, encoding='unicode') for c in el)
            emit(s_, p_, L(inner, None, RDF + 'XMLLiteral')); return
        extra = [k for k in el.attrib if k not in _RDF_SYNTAX_ATTRS and not k.startswith(_XMLNS)]
        if el.get(_R + 'resource') is not None or el.get(_R + 'nodeID') is not None:
            o_ = I(resolve(el.get(_R + 'resource'), b)) if el.get(_R + 'resource') is not None else ('B', uid + 'n_' + el.get(_R + 'nodeID'))
            emit(s_, p_, o_); prop_attrs(o_, el, b, lang); return
        children = list(el)
        if children:
            emit(s_, p_, node(children[0], b, lang)); return
        if extra or el.get(_R + 'type') is not None:
            o_ = fresh(); emit(s_, p_, o_); prop_attrs(o_, el, b, lang); return
        dt = el.get(_R + 'datatype')
        emit(s_, p_, L(el.text or '', None if dt else lang, resolve(dt, b) if dt else None))
    b0, lang0 = ctx(root, base, None)
    if root.tag == _R + 'RDF':
        for c in root: node(c, b0, lang0)
    else:
        node(root, b0, lang0)
    return triples, {}

RDF_EXTENSIONS = {'.ttl': 'Turtle', '.turtle': 'Turtle', '.nt': 'N-Triples',
                  '.rdf': 'RDF/XML', '.rdfs': 'RDF/XML', '.owl': 'RDF/XML', '.xml': 'RDF/XML'}

def read_rdf(path):
    """Parse a Turtle, N-Triples or RDF/XML file. .owl/.xml files are sniffed, since
    both syntaxes are common under those extensions. Returns (triples, format name)."""
    path = pathlib.Path(path)
    data = path.read_bytes()
    head = data[:2048].lstrip().decode('utf-8', 'replace')
    is_xml = bool(re.match(r'(<\?xml|<rdf:RDF|<!DOCTYPE|<!--)', head)) or (
        path.suffix.lower() in ('.rdf', '.rdfs') and head.startswith('<') and not head.startswith('<http'))
    if is_xml:
        return parse_rdfxml(data)[0], 'RDF/XML'
    text = data.decode('utf-8-sig')
    return parse_turtle(text)[0], ('N-Triples' if path.suffix.lower() == '.nt' else 'Turtle')

class IngestError(ValueError):
    pass

# ─────────────────────────────────────────────────────────────────────────────
# Turtle writer
# ─────────────────────────────────────────────────────────────────────────────
PRED_ORDER = [RDF + 'type', RDFS + 'label', SKOS + 'prefLabel', DCT + 'title', SKOS + 'altLabel',
              SKOS + 'definition', DCT + 'description', SKOS + 'scopeNote', SKOS + 'example', SKOS + 'notation',
              RDFS + 'subClassOf', OWL + 'equivalentClass', RDFS + 'subPropertyOf', RDFS + 'domain', RDFS + 'range',
              SKOS + 'inScheme', SKOS + 'topConceptOf', SKOS + 'broader', SKOS + 'narrower', SKOS + 'hasTopConcept',
              RDFS + 'isDefinedBy', 'https://www.insperity.com/ontology/core/hasPrimaryTerm', DCT + 'subject', DC + 'subject',
              'https://www.insperity.com/ontology/core/formalizedBy', SH + 'targetClass', SH + 'path', SH + 'class', SH + 'property',
              OWL + 'imports', VAEM + 'namespace', VANN + 'preferredNamespacePrefix', DCT + 'language', DCT + 'source',
              DCT + 'publisher', DCT + 'conformsTo',
              None,  # everything not listed goes here
              SKOS + 'editorialNote', SKOS + 'changeNote',
              OWL + 'versionInfo', OWL + 'versionIRI']
GOV_TAIL = ['https://www.insperity.com/ontology/core/hasLifecycleStatus', DCT + 'creator', DCT + 'contributor',
            DCT + 'created', DCT + 'modified']
RX_SAFE_LOCAL = re.compile(r'^[A-Za-z_][A-Za-z0-9_\-]*$')

def _esc_lit(s):
    return (s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
             .replace('\r', '\\r').replace('\t', '\\t'))

class Writer:
    def __init__(self, prefixes, gov_tail=GOV_TAIL):
        self.prefixes = sorted(prefixes.items(), key=lambda kv: -len(kv[1]))
        self.used = set()
        self.gov_tail = gov_tail

    def iri(self, v):
        if v == RDF + 'type': return 'a'
        for p, ns in self.prefixes:
            if v.startswith(ns) and RX_SAFE_LOCAL.match(v[len(ns):] or '_') and v != ns:
                self.used.add(p); return f'{p}:{v[len(ns):]}'
        return f'<{v}>'

    def term(self, t, graph, depth):
        if t[0] == 'I': return self.iri(t[1])
        if t[0] == 'L':
            s = f'"{_esc_lit(t[1])}"'
            if t[2]: return s + '@' + t[2]
            if t[3] and t[3] != XSD + 'string':
                if t[3] == XSD + 'boolean' and t[1] in ('true', 'false'): return t[1]
                return s + '^^' + self.iri(t[3])
            return s
        if t not in graph:
            return '[]'
        items = self.as_list(t, graph)
        if items is not None:
            return '( ' + ' '.join(self.term(x, graph, depth) for x in items) + ' )'
        # blank node: inline as [ … ]
        body = self.po_block(t, graph, depth + 1)
        pad = '    ' * depth + '  '
        return '[\n' + body + '\n' + pad + ']'

    @staticmethod
    def as_list(t, graph):
        """Members of a well-formed RDF collection starting at blank node t, else None."""
        out, cur, seen = [], t, set()
        while cur != ('I', RDF + 'nil'):
            if cur[0] != 'B' or cur in seen or cur not in graph: return None
            seen.add(cur)
            ps = graph[cur]
            if set(ps) != {RDF + 'first', RDF + 'rest'} or len(ps[RDF + 'first']) != 1 or len(ps[RDF + 'rest']) != 1: return None
            out.append(ps[RDF + 'first'][0]); cur = ps[RDF + 'rest'][0]
        return out

    def order(self, preds):
        def key(p):
            if p in self.gov_tail: return (2, self.gov_tail.index(p), p)
            if p in PRED_ORDER: return (0, PRED_ORDER.index(p), p)
            return (1, 0, p)
        return sorted(preds, key=key)

    def po_block(self, s, graph, depth):
        pad = '    ' * depth + '  '
        props = graph[s]
        lines = []
        for p in self.order(props.keys()):
            objs = props[p]
            objs = sorted(objs, key=lambda o: (o[0], str(o[1:])))
            rendered = [self.term(o, graph, depth) for o in objs]
            pr = self.iri(p)
            if sum(len(r) for r in rendered) > 70 and len(rendered) > 1:
                lines.append(f'{pad}{pr} ' + (' ,\n' + pad + '    ').join(rendered))
            else:
                lines.append(f'{pad}{pr} ' + ' , '.join(rendered))
        return ' ;\n'.join(lines)

    def write(self, graph, subjects, header_comment):
        out = []
        for s in subjects:
            if s[0] == 'B':      # top-level axiom such as owl:AllDisjointClasses
                out.append('[\n' + self.po_block(s, graph, 0) + '\n] .\n')
            else:
                out.append(self.iri(s[1]) + '\n' + self.po_block(s, graph, 0) + ' .\n')
        body = '\n'.join(out)
        pre = ''.join(f'@prefix {p}: <{ns}> .\n' for p, ns in sorted(self.prefixes) if p in self.used)
        return header_comment + '\n' + pre + '\n' + body

    def write_trig(self, graph, subjects, header_comment, graph_iri):
        """Same content as write(), wrapped in a named graph so an import lands it in that graph."""
        text = self.write(graph, subjects, header_comment)
        head, _, body = text.partition('\n\n' + self.iri(subjects[0][1]))
        body = self.iri(subjects[0][1]) + body
        inner = '\n'.join(('  ' + ln) if ln else ln for ln in body.rstrip('\n').split('\n'))
        return head + '\n\n<' + graph_iri + '> {\n\n' + inner + '\n}\n'

# ─────────────────────────────────────────────────────────────────────────────
# Text helpers
# ─────────────────────────────────────────────────────────────────────────────
def sentence_case(label, keep=()):
    words = label.strip().split()
    out = []
    for i, w in enumerate(words):
        core = re.sub(r'[^A-Za-z]', '', w)
        if i == 0:
            out.append(w[:1].upper() + w[1:] if not (len(core) > 1 and core.isupper()) else w)
        elif (len(core) > 1 and core.isupper()) or core in keep:
            out.append(w)            # acronym or proper noun: keep as written
        else:
            out.append(w.lower())
    return ' '.join(out)

def slug(label):
    s = re.sub(r'[^\w\s-]', '', label.lower().replace('&', ' and '))
    return re.sub(r'[\s_]+', '-', s.strip()).strip('-')

def upper_camel(label):
    return ''.join(w[:1].upper() + w[1:] for w in re.split(r'[^A-Za-z0-9]+', label) if w)

def split_camel(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', name)

def label_number(label):
    """'01. Data strategy' → ('01', 'Data strategy'); a label without a leading number → (None, label)."""
    m = re.fullmatch(r'\s*(\d+(?:\.\d+)*)[.)]?\s+(.+)', label or '')
    return (m.group(1), m.group(2)) if m and not re.match(r'\d', m.group(2)) else (None, label)

def date_lit(value):
    """A dct:created/dct:modified value with the right datatype: xsd:date for a date alone, else xsd:dateTime."""
    v = value.strip()
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', v): return L(v, None, XSD + 'date')
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?', v):
        return L(v.replace(' ', 'T'), None, XSD + 'dateTime')
    return None

# ─────────────────────────────────────────────────────────────────────────────
# Ingestion
# ─────────────────────────────────────────────────────────────────────────────
ACRONYM = re.compile(r'\b(?![IVX]+\b)[A-Z]{2,}s?\b')
CAMEL_ACR = re.compile(r'[A-Z]{2,}(?=[A-Z][a-z]|$|[0-9_-])|[A-Z]{3,}')
_STOP = {'and', 'of', 'the', 'for', 'to', 'in', 'on', '&', 'a', 'an'}

def _initials(phrase):
    words = [w for w in re.split(r'[\s/&,-]+', phrase) if w and w.lower() not in _STOP]
    return ''.join(w[0] for w in words).upper(), len(words)


class Policy:
    """Acronym and organization rules from the config (Part III §3.2 and the
    'acronyms' / 'organizations' sections). Shared by ingestion and the checks."""
    def __init__(self, cfg):
        a = cfg.get('acronyms', {}) or {}
        self.approved = {x.upper() for x in a.get('approved', [])}
        self.expansions = {k.upper(): v for k, v in (a.get('expansions', {}) or {}).items()}
        self.orgs = []
        for o in cfg.get('organizations', []) or []:
            self.orgs.append(dict(name=o['name'], rx=re.compile('|'.join(f'(?:{x})' for x in o['patterns']), re.I),
                                  remove=o.get('removeTerms', True), replacement=o.get('replacement', 'the organization')))

    def acronyms(self, label):
        out = []
        for m in ACRONYM.finditer(label or ''):
            t = m.group(0)
            if t.upper() in self.approved or (t.endswith('s') and t[:-1].upper() in self.approved): continue
            out.append(t)
        return out

    def org_hit(self, text):
        for o in self.orgs:
            m = o['rx'].search(text or '')
            if m: return o, m.group(0)
        return None, None

    def expansion(self, tok, alts=(), defs=()):
        """Spelled-out form of an acronym: config, then an alternative label whose
        initials match, then 'An acronym/abbreviation for X' in the definition."""
        key = tok.upper()
        if key in self.expansions: return self.expansions[key], 'config'
        for a in alts:
            ini, n = _initials(a)
            if n > 1 and ini == key and not ACRONYM.fullmatch(a.strip()): return a.strip(), 'alternative label'
        for d in defs:
            m = re.search(r'\b(acronym|abbreviation)\s+for\s+(.+?)(?:,\s+(?:this|that|a|an|the|is|which)\b|\s+is\b|[.;(])', d, re.I)
            if m:
                phrase = m.group(2).strip()
                ini, n = _initials(phrase)
                if n > 1 and (ini == key or (m.group(1).lower() == 'abbreviation' and ini[:1] == key[:1] and n <= 5)):
                    return phrase, 'definition'
        return None, None

    def expand_label(self, label, alts=(), defs=()):
        out, done = label, []
        for tok in self.acronyms(label):
            plural = tok.endswith('s') and len(tok) > 2
            exp, how = self.expansion(tok[:-1], alts, defs) if plural else (None, None)
            if exp: exp += 's'
            else: exp, how = self.expansion(tok, alts, defs)
            if not exp: continue
            rx = re.compile(r'(?:-|(?<!\w))' + re.escape(tok) + r'(?!\w)')
            m = rx.search(out)
            if not m: continue
            sep = ' ' if m.group(0).startswith('-') else ''
            out = out[:m.start()] + sep + exp + out[m.end():]
            done.append((tok, exp, how))
        # "short message service service" → "short message service"
        out = re.sub(r'\b(\w+)(\s+\1\b)+', r'\1', out, flags=re.I)
        return out, done

    def generic(self, text):
        """Suggested organization-neutral wording (for review, never applied silently)."""
        for o in self.orgs:
            r = o['replacement']
            text = re.sub(r"(?:" + o['rx'].pattern + r")(?:['’]s)", r + "'s", text, flags=re.I)
            text = re.sub(r"(?:" + o['rx'].pattern + r")(?=\s+[A-Z][a-z])", r + "'s", text)
            text = o['rx'].sub(r, text)
        text = re.sub(r'\b(an|a|the) (the organization)', r'\2', text, flags=re.I)
        return re.sub(r'(^|[.!?]\s+)the organization', lambda m: m.group(1) + 'The organization', text)


class Ingest:
    def __init__(self, cfg, now):
        self.cfg = cfg
        self.base = cfg['baseUrl'].rstrip('/') + '/'
        self.CORE = self.base + 'ontology/core/'
        self.HAS_STATUS = self.CORE + 'hasLifecycleStatus'
        self.HAS_PRIMARY = self.CORE + 'hasPrimaryTerm'
        self.notations = {}        # new IRI → number taken out of a numbered label
        self.author = cfg['author']
        self.author_term = I(cfg['authorIri']) if cfg.get('authorIri') else L(cfg['author'])
        self.version = cfg['initialVersion']
        self.now = now
        self.day = now.date()
        self.now_lit = L(now.strftime('%Y-%m-%dT%H:%M:%SZ'), None, XSD + 'dateTime')
        self.src_rx = [(re.compile(r['pattern']), r) for r in cfg['sourceNamespaces']]
        self.keep = set(cfg.get('keepCase', []))
        self.policy = Policy(cfg)
        self.dropped = {}          # old IRI → why the term was removed (organization-specific)
        self.fixes = collections.defaultdict(list)   # new IRI → automatic fixes applied
        self.cross = {}            # old IRI → new IRI
        self.cross_kind = {}       # old IRI → kind of thing (for the crosswalk file)
        self.labels = {}           # new IRI → sentence-case label
        self.findings = collections.defaultdict(list)   # asset key → [(level, text)]
        self.removed = collections.defaultdict(collections.Counter)
        self.removed_refs = collections.Counter()
        self.orphans = collections.Counter()
        self.bare = collections.Counter()
        self.foreign = collections.Counter()
        self.missing_defs = []          # (asset key, term) with no definition anywhere, for generation
        self.sources = []          # loaded files
        self.outputs = {}          # asset key → {graph, subjects, header}

    # ── namespace mapping ────────────────────────────────────────────────────
    def classify(self, iri):
        """Legacy IRI → (kind, domain, local) using the configured patterns."""
        for rx, rule in self.src_rx:
            m = rx.match(iri)
            if m:
                g = m.groupdict()
                return (g.get('kind') or rule['kind'], g.get('domain') or rule['domain'], g.get('local') or '')
        return None

    def asset_iri(self, kind, domain): return f'{self.base}{kind}/{domain}/'
    def key(self, kind, domain): return f'{kind}/{domain}'

    def renamed(self, kind, domain, local):
        r = self.cfg.get('renames', {}).get(f'{kind}/{domain}/{local}')
        return (r['local'], r.get('label')) if r else (local, None)

    def map_iri(self, iri):
        """Every reference goes through here: crosswalk first, then the generic pattern."""
        if iri in self.cross: return self.cross[iri]
        c = self.classify(iri)
        if not c: return iri
        kind, domain, local = c
        if not local: return self.asset_iri(kind, domain)
        if kind == 'vocabulary': return iri     # unresolved vocabulary term: handled by the caller
        local, _ = self.renamed(kind, domain, local)
        return self.asset_iri(kind, domain) + local

    def map_term(self, t):
        return I(self.map_iri(t[1])) if t[0] == 'I' else t

    # ── loading ──────────────────────────────────────────────────────────────
    def inspect(self, path):
        """Parse one file and say what it is, without changing anything."""
        try:
            triples, fmt = read_rdf(path)
        except (TurtleError, UnicodeDecodeError) as e:
            raise IngestError(f'cannot be parsed: {e}')
        g = collections.OrderedDict()
        for s, p, o in triples:
            g.setdefault(s, collections.OrderedDict()).setdefault(p[1], []).append(o)
        headers = [s for s, ps in g.items() if s[0] == 'I' and
                   any(o in (I(OWL + 'Ontology'), I(SKOS + 'ConceptScheme')) for o in ps.get(RDF + 'type', []))]
        if not headers:
            raise IngestError('has no owl:Ontology or skos:ConceptScheme header, so it is not a vocabulary, taxonomy or ontology')
        if len(headers) > 1:
            raise IngestError(f'declares {len(headers)} assets ({", ".join(h[1] for h in headers[:3])}); split it into one file per asset')
        h = headers[0]
        c = self.classify(h[1])
        if not c and h[1].startswith(REFERENCE_NS):
            raise IngestError(f'is a reference ontology ({h[1]}): it keeps its own IRIs and is never ingested. Load it under '
                              'Reference ontologies further down this page (BFO source or RO Core source: this file\'s path), or with GraphDB › Import')
        if not c:
            raise IngestError(f'header {h[1]} matches no sourceNamespaces pattern in the config; add one for its namespace')
        kind, domain, hlocal = c
        ns_domain = None
        m = re.fullmatch(r'([A-Z][A-Za-z0-9]*?)(Taxonomy|Vocabulary|Ontology|Scheme)?', hlocal or '')
        if hlocal and m:
            # the header is a named resource inside a namespace that several files share (e.g.
            # …/taxonomy/core/IssueTaxonomy and …/taxonomy/core/PartyTaxonomy): one asset per file,
            # named after the header — core + Issue → core-issue
            ns_domain, domain = domain, f'{domain}-{slug(split_camel(m.group(1)))}'
        scheme = I(SKOS + 'ConceptScheme') in g[h].get(RDF + 'type', [])
        if kind == 'taxonomy' and not scheme and self.cfg.get('taxonomiesAsSkos', True) not in (False, 'false', '0', 0):
            n, lost = self.owl_taxonomy_to_skos(g, h)
            scheme = True
            self.note(self.key(kind, domain), 'fixed', f'Taxonomy authored as OWL converted to SKOS (§3.11): {n} classes became concepts, '
                      f'rdfs:subClassOf became skos:broader' + (f'; {lost} OWL restrictions dropped (they belong in the ontology)' if lost else ''))
        terms = sum(1 for s, ps in g.items() if s[0] == 'I' and s != h and
                    any(t in ps.get(RDF + 'type', []) for t in (I(SKOS + 'Concept'), I(OWL + 'Class'), I(RDFS + 'Class'))))
        return dict(path=str(path), name=pathlib.Path(path).name, format=fmt, graph=g, header=h, kind=kind, domain=domain, ns_domain=ns_domain,
                    triples=len(triples), terms=terms, key=self.key(kind, domain), scheme=scheme,
                    label=self.pref(g[h]), new_iri=self.asset_iri(kind, domain))

    @staticmethod
    def owl_taxonomy_to_skos(g, h):
        """Rewrite, in place, a taxonomy authored as OWL classes as a SKOS concept scheme.
        Returns (classes converted, restrictions dropped)."""
        hp = g[h]
        hp[RDF + 'type'] = [t for t in hp.get(RDF + 'type', []) if t != I(OWL + 'Ontology')] + [I(SKOS + 'ConceptScheme')]
        for p in (OWL + 'imports', OWL + 'versionIRI', OWL + 'priorVersion'):
            hp.pop(p, None)                  # a scheme imports nothing; its concepts point to classes with core:formalizedBy
        n = lost = 0
        for s, ps in g.items():
            if s[0] != 'I' or s == h: continue
            types = ps.get(RDF + 'type', [])
            if I(OWL + 'Class') not in types or s[1].startswith((OWL, RDFS, RDF, XSD)): continue
            n += 1
            ps[RDF + 'type'] = [t for t in types if t not in (I(OWL + 'Class'), I(RDFS + 'Class'))] + [I(SKOS + 'Concept')]
            parents = ps.pop(RDFS + 'subClassOf', [])
            named = [x for x in parents if x[0] == 'I' and x[1] != OWL + 'Thing']
            lost += sum(1 for x in parents if x[0] == 'B')
            if named: ps.setdefault(SKOS + 'broader', []).extend(x for x in named if x not in ps.get(SKOS + 'broader', []))
            for p in (RDFS + 'isDefinedBy', OWL + 'equivalentClass', OWL + 'disjointWith'):
                ps.pop(p, None)
        return n, lost

    def load(self, path):
        src = self.inspect(path)
        if any(x['key'] == src['key'] for x in self.sources):
            other = next(x for x in self.sources if x['key'] == src['key'])
            raise IngestError(f'maps to the same asset ({src["new_iri"]}) as {other["name"]}; ingest one of them at a time')
        self.sources.append(src)
        return src

    @staticmethod
    def lits(ps, p):
        return [o[1] for o in ps.get(p, []) if o[0] == 'L' and o[2] in (None, 'en')]

    def std_label(self, ps, fallback=''):
        """Preferred label after the automatic fixes: grouping parentheses removed and
        acronyms spelled out where the config, an alternative label or the definition
        says what they stand for. Returns (label, [fix descriptions])."""
        lab = self.pref(ps) or fallback
        fixes = []
        m = re.fullmatch(r'\s*\((.+)\)\s*', lab)
        if m:
            fixes.append(f'parentheses removed from "{lab}"'); lab = m.group(1)
        num, rest = label_number(lab)
        if num:
            fixes.append(f'number "{num}" moved from the label to skos:notation'); lab = rest
        if '&' in lab:
            fixes.append(f'"&" spelled out as "and" in "{lab}"')
            lab = re.sub(r'\s*&\s*', ' and ', lab).strip()
        alts = self.lits(ps, SKOS + 'altLabel')
        defs = self.lits(ps, SKOS + 'definition') + self.lits(ps, RDFS + 'comment')
        new, done = self.policy.expand_label(lab, alts, defs)
        for tok, exp, how in done:
            fixes.append(f'{tok} spelled out as "{exp}" (from the {how})')
        return new, fixes

    def org_term(self, label, iri):
        o, hit = self.policy.org_hit(label)
        if not o: o, hit = self.policy.org_hit(iri.rstrip('/').split('/')[-1].split('#')[-1].replace('-', ' '))
        return (o, hit) if o and o['remove'] else (None, None)

    # ── pass 1: crosswalk for every term the files define ────────────────────
    def build_crosswalk(self):
        for src in self.sources:
            g, kind, domain = src['graph'], src['kind'], src['domain']
            new_asset = self.asset_iri(kind, domain)
            self.cross[src['header'][1]] = new_asset; self.cross_kind[src['header'][1]] = 'asset header'
            # trailing-slash variants of the header resolve to the same asset
            h = src['header'][1]
            self.cross.setdefault(h.rstrip('/') if h.endswith('/') else h + '/', new_asset)
            seen = {}
            for s, ps in g.items():
                if s[0] != 'I' or s == src['header']: continue
                types = ps.get(RDF + 'type', [])
                if I(SKOS + 'Concept') in types:
                    lab, fixes = self.std_label(ps)
                    o, hit = self.org_term(lab, s[1])
                    if o:
                        self.dropped[s[1]] = f'names {o["name"]} ("{hit}")'; continue
                    newlab = None
                    if kind == 'taxonomy':        # taxonomy concepts and vocabulary terms: hyphen-joined (§3.2 as amended)
                        local, newlab = self.renamed(kind, domain, slug(lab))
                        new = new_asset + local
                        kindname = 'taxonomy concept'
                    else:
                        new = new_asset + slug(lab)
                        kindname = 'vocabulary term'
                    self.labels[new] = newlab or sentence_case(lab, self.keep)
                    num, _ = label_number(self.pref(ps))
                    if fixes: self.fixes[new] += fixes
                elif I(OWL + 'Class') in types or I(RDFS + 'Class') in types:
                    c = self.classify(s[1])
                    local = c[2] if c else s[1].rstrip('/').split('/')[-1].split('#')[-1]
                    local, newlab = self.renamed(kind, domain, local)
                    lab, fixes = self.std_label(ps, split_camel(local))
                    o, hit = self.org_term(newlab or lab, s[1])
                    if o:
                        self.dropped[s[1]] = f'names {o["name"]} ("{hit}")'; continue
                    local = slug(newlab or lab)           # identifier: the label's words joined with hyphens (§3.2 as amended)
                    owner = c[:2] if c else (kind, domain)
                    if src.get('ns_domain') and c and c[:2] == (kind, src['ns_domain']):
                        owner = (kind, domain)            # shared namespace: the term belongs to this file's asset
                    new = self.asset_iri(*owner) + local
                    self.labels[new] = newlab or sentence_case(lab, self.keep)
                    if fixes: self.fixes[new] += fixes
                    kindname = 'class'
                    num = None
                elif any(t in types for t in (I(OWL + 'ObjectProperty'), I(OWL + 'DatatypeProperty'), I(OWL + 'AnnotationProperty'), I(RDF + 'Property'))):
                    c = self.classify(s[1])
                    if not c or not c[2]:
                        continue                      # property from another vocabulary: left as is
                    local = re.split(r'[#/]', c[2])[-1]
                    local = (lambda w: w[:1].lower() + w[1:])(upper_camel(local)) if not re.fullmatch(r'[a-z][A-Za-z0-9]*', local) else local
                    new = self.asset_iri(*c[:2]) + local
                    self.labels[new] = sentence_case(self.pref(ps) or split_camel(local), self.keep)
                    kindname = 'property'
                    num = None
                else:
                    continue
                sep = '-' if kindname == 'vocabulary term' else ''
                if new in seen and (num or new in self.notations):
                    # a numbered label that, without its number, repeats another term's label: keep the two apart
                    if num:                        # this term is the numbered one
                        alt = new + sep + num.replace('.', '-')
                        self.labels[alt] = self.labels[new]; other = seen[new]
                        self.labels[new] = self.labels.get(new)
                        new = alt
                    else:                          # the term seen earlier was the numbered one: move it
                        n0 = self.notations.pop(new); old0 = seen.pop(new)
                        alt = new + sep + n0.replace('.', '-')
                        self.cross[old0] = alt; self.labels[alt] = self.labels[new]; self.notations[alt] = n0; seen[alt] = old0
                        self.fixes[alt] += self.fixes.pop(new, [])
                        other = old0
                    self.note(src['key'], 'warn', f'{short_iri(s[1])} and {short_iri(other)} have the same label once the number is removed; '
                              f'the numbered one is kept apart as {short_iri(alt)}; merge or rename one in Conformance Review')
                if num: self.notations[new] = num
                if new in seen:
                    self.note(src['key'], 'error', f'Two terms would share {new}: {seen[new]} and {s[1]}')
                seen[new] = s[1]
                self.cross[s[1]] = new; self.cross_kind[s[1]] = kindname
        # shapes: named after the target class, in the shapes graph of the target's domain
        for src in self.sources:
            for s, ps in src['graph'].items():
                if s[0] == 'I' and I(SH + 'NodeShape') in ps.get(RDF + 'type', []):
                    tgt = ps.get(SH + 'targetClass', [None])[0]
                    new_tgt = self.map_iri(tgt[1]) if tgt else None
                    if new_tgt and new_tgt.startswith(self.base):
                        # shapes live in the shapes graph of the model that authored them
                        new = f'{self.base}shapes/{src["domain"]}/{new_tgt.rstrip("/").split("/")[-1]}-shape'
                    else:
                        c = self.classify(s[1])
                        new = f'{self.base}shapes/{c[1] if c else src["domain"]}/{s[1].rstrip("/").split("/")[-1]}'
                    self.cross[s[1]] = new; self.cross_kind[s[1]] = 'shape'

    @staticmethod
    def pref(ps):
        for p in (SKOS + 'prefLabel', RDFS + 'label'):
            for o in ps.get(p, []):
                if o[0] == 'L' and (o[2] in (None, 'en')): return o[1]
        return ''

    def note(self, key, level, text):
        self.findings[key].append((level, text))

    # ── pass 2: transform ────────────────────────────────────────────────────
    # Structural predicates kept (and re-pointed). Labels, definitions and
    # governance fields are rebuilt; anything else is removed and reported.
    KEEP_TERM = {RDF + 'type', RDFS + 'subClassOf', OWL + 'equivalentClass', OWL + 'disjointWith',
                 RDFS + 'subPropertyOf', RDFS + 'domain', RDFS + 'range', OWL + 'inverseOf',
                 SKOS + 'broader', SKOS + 'related', SKOS + 'exactMatch', SKOS + 'closeMatch',
                 SKOS + 'broadMatch', SKOS + 'narrowMatch', SKOS + 'notation', SKOS + 'scopeNote',
                 SKOS + 'example', SKOS + 'altLabel', SKOS + 'hiddenLabel', SKOS + 'editorialNote', RDFS + 'seeAlso', DC + 'subject',
                 SH + 'targetClass', SH + 'property', SH + 'path', SH + 'class', SH + 'datatype',
                 SH + 'minCount', SH + 'maxCount', SH + 'nodeKind', SH + 'in', SH + 'node'}
    REBUILT = {RDFS + 'label', SKOS + 'prefLabel', SKOS + 'definition', RDFS + 'comment', RDFS + 'isDefinedBy',
               SKOS + 'inScheme', SKOS + 'topConceptOf', SKOS + 'narrower', DCT + 'created', DCT + 'modified',
               DCT + 'creator', DCT + 'contributor', OWL + 'versionInfo', SKOS + 'hasTopConcept'}

    def out(self, key, header_iri, kind):
        if key not in self.outputs:
            self.outputs[key] = dict(graph=collections.OrderedDict(), header=I(header_iri), kind=kind,
                                     sources=[], subjects=[])
        return self.outputs[key]

    def add(self, g, s, p, o):
        lst = g.setdefault(s, collections.OrderedDict()).setdefault(p, [])
        if o not in lst: lst.append(o)

    def governance(self, g, s, created):
        self.add(g, s, I(self.HAS_STATUS), I(self.CORE + self.cfg['lifecycleStatus']))
        self.add(g, s, I(OWL + 'versionInfo'), L(self.version))
        self.add(g, s, I(DCT + 'creator'), self.author_term)
        self.add(g, s, I(DCT + 'created'), created or self.now_lit)
        self.add(g, s, I(DCT + 'modified'), self.now_lit)

    @staticmethod
    def earliest(ps):
        ds = [d for d in (date_lit(o[1]) for o in ps.get(DCT + 'created', []) if o[0] == 'L') if d]
        if not ds: return None
        return min(ds, key=lambda x: x[1])

    def copy_bnode(self, srcg, dstg, b, key):
        """Copy a blank-node structure (restrictions, property shapes), re-pointing IRIs."""
        for p, objs in srcg.get(b, {}).items():
            for o in objs:
                if o[0] == 'B': self.copy_bnode(srcg, dstg, o, key)
                self.add(dstg, b, I(self.map_iri(p)), self.map_term(o))

    def transform(self):
        vocab_terms = {}          # new vocabulary IRI → source predicates (for filling class metadata)
        vocab_by_label = {}       # (vocab asset, normalized label) → new IRI
        for src in self.sources:
            if src['kind'] != 'vocabulary': continue      # a SKOS taxonomy is not a vocabulary to link to
            for s, ps in src['graph'].items():
                if s[0] == 'I' and I(SKOS + 'Concept') in ps.get(RDF + 'type', []) and s[1] in self.cross:
                    new = self.cross[s[1]]
                    vocab_terms[new] = ps
                    vocab_by_label[(self.asset_iri(src['kind'], src['domain']), self.labels.get(new, self.pref(ps)).lower())] = new

        for src in self.sources:
            g, key = src['graph'], src['key']
            asset = self.asset_iri(src['kind'], src['domain'])
            o = self.out(key, asset, src['kind'])
            o['sources'].append(src)
            dst = o['graph']
            shapes_key = f'shapes/{src["domain"]}'
            referenced_bnodes = {ob for ps in g.values() for objs in ps.values() for ob in objs if ob[0] == 'B'}

            for s, ps in g.items():
                if s == src['header'] or s in referenced_bnodes: continue
                if s[0] == 'B':
                    types = {t[1] for t in ps.get(RDF + 'type', [])}
                    if types & {OWL + 'AllDisjointClasses', OWL + 'AllDifferent', OWL + 'AllDisjointProperties'}:
                        members = [m for lst in ps.get(OWL + 'members', []) + ps.get(OWL + 'distinctMembers', [])
                                   for m in (Writer.as_list(lst, g) or [])]
                        live = [m for m in members if not (m[0] == 'I' and m[1] in self.dropped)]
                        if len(live) >= 2:
                            for p, objs in ps.items():
                                for ob in objs:
                                    if ob[0] == 'B': self.copy_bnode(g, dst, ob, key)
                                    self.add(dst, s, I(p), self.map_term(ob))
                            o['subjects'].append(s)
                            continue
                    self.orphans[key] += 1          # restriction, datatype or list cell attached to nothing
                    continue
                if self.is_bare(s, ps):
                    self.bare[key] += 1            # bare declaration of a term from another namespace, nothing else said about it
                    continue
                if s[1] in self.dropped:
                    self.note(key, 'dropped', f'{s[1].rstrip("/").split("/")[-1]} ("{self.pref(ps)}") removed: {self.dropped[s[1]]}')
                    continue
                types = ps.get(RDF + 'type', [])
                if not types:
                    self.note(key, 'removed', f'Stub subject {s[1]} (no type; only {", ".join(sorted(short(p) for p in ps))})')
                    for p in ps: self.removed[key][p] += len(ps[p])
                    continue
                if I(SH + 'NodeShape') in types:
                    self.shape(src, s, ps, shapes_key)
                    continue
                new = I(self.cross.get(s[1], s[1]))
                if not new[1].startswith(self.base):
                    # a term from another namespace with real content: kept as written for review
                    # in Conformance Review (base URL finding), never stamped as one of ours
                    for p, objs in ps.items():
                        if p in (DCT + 'created', DCT + 'modified', DCT + 'creator', DCT + 'contributor', OWL + 'versionInfo'): continue
                        for ob in objs:
                            if ob[0] == 'I' and ob[1] in self.dropped: continue
                            if ob[0] == 'B': self.copy_bnode(g, dst, ob, key)
                            self.add(dst, new, I(p), self.map_term(ob))
                    self.foreign[key] += 1
                    o['subjects'].append(new)
                    continue
                is_concept = I(SKOS + 'Concept') in types
                label = self.labels.get(new[1]) or sentence_case(self.pref(ps), self.keep)
                orig_label = self.pref(ps)

                for p, objs in ps.items():
                    if p in self.REBUILT: continue
                    is_subj = p in SUBJECT_IN or p == self.HAS_PRIMARY
                    if p not in self.KEEP_TERM and not is_subj and p != self.CORE + 'formalizedBy':
                        self.removed[key][p] += len(objs); continue
                    for ob in objs:
                        if ob[0] == 'I' and ob[1] in self.dropped:
                            if p in (SKOS + 'broader', RDFS + 'subClassOf'):
                                for par in self.surviving_parents(ob[1], p):   # children move up a level
                                    self.add(dst, new, I(p), I(self.map_iri(par)))
                            self.removed_refs[key] += 1
                            continue
                        if p == SKOS + 'altLabel' and ob[0] == 'L':
                            o_, hit = self.policy.org_hit(ob[1])
                            if o_:
                                self.note(key, 'fixed', f'{short_iri(new[1])}: alternative label "{ob[1]}" removed (names {o_["name"]})'); continue
                            if not ps.get(SKOS + 'definition') and self.looks_like_definition(ob[1]):
                                continue                          # moved to skos:definition below
                        if ob[0] == 'B': self.copy_bnode(g, dst, ob, key)
                        if is_subj:
                            if ob[0] != 'I': continue
                            ob = I(self.subject_link(key, new[1], ob[1], label, vocab_terms, vocab_by_label))
                            self.add(dst, new, I(DCT + 'subject'), ob)
                            continue
                        elif p == SKOS + 'altLabel' and ob[0] == 'L':
                            ob = L(ob[1], ob[2] or 'en')
                        else:
                            ob = self.map_term(ob)
                        self.add(dst, new, I(p), ob)

                # labels (§3.11: skos:prefLabel and rdfs:label on every term)
                self.add(dst, new, I(SKOS + 'prefLabel'), L(label, 'en'))
                self.add(dst, new, I(RDFS + 'label'), L(label, 'en'))
                if new[1] in self.notations:
                    self.add(dst, new, I(SKOS + 'notation'), L(self.notations[new[1]]))
                old_alt = sentence_case(label_number(orig_label)[1], self.keep) if orig_label else ''
                if old_alt and old_alt.lower() != label.lower():
                    self.add(dst, new, I(SKOS + 'altLabel'), L(old_alt, 'en'))
                    self.note(key, 'renamed', f'{short_iri(s[1])} → {short_iri(new[1])} ("{orig_label}" → "{label}")')
                elif orig_label and orig_label != label:
                    self.note(key, 'label', f'"{orig_label}" → "{label}"')

                # definition: own → linked vocabulary term → config
                defs = [x for x in ps.get(SKOS + 'definition', []) + ps.get(RDFS + 'comment', []) if x[0] == 'L']
                if not defs:
                    moved = [x for x in ps.get(SKOS + 'altLabel', []) if x[0] == 'L' and self.looks_like_definition(x[1])]
                    if moved:
                        defs = moved[:1]
                        self.note(key, 'fixed', f'{short_iri(new[1])}: definition was stored as an alternative label; moved to skos:definition')
                for fx in self.fixes.get(new[1], []):
                    self.note(key, 'fixed', f'{short_iri(new[1])}: {fx}')
                linked = [x for x in dst[new].get(I(DCT + 'subject'), [])] if new in dst else []
                if defs:
                    d = defs[0]; self.add(dst, new, I(SKOS + 'definition'), L(clean(d[1]), d[2] or 'en'))
                else:
                    filled = False
                    for lk in linked:
                        vps = vocab_terms.get(lk[1])
                        ev = getattr(self, 'extra_vocab', {}).get(lk[1])
                        if not vps and ev and ev[3]:      # a vocabulary already in the destination folder
                            self.add(dst, new, I(SKOS + 'definition'), L(clean(ev[3]), 'en')); filled = True
                            self.note(key, 'filled', f'{short_iri(new[1])}: definition taken from its vocabulary term')
                            break
                        if vps:
                            for d in vps.get(SKOS + 'definition', []):
                                self.add(dst, new, I(SKOS + 'definition'), L(clean(d[1]), d[2] or 'en')); filled = True
                            for a in vps.get(SKOS + 'altLabel', []):
                                self.add(dst, new, I(SKOS + 'altLabel'), L(a[1], a[2] or 'en'))
                            if filled:
                                self.note(key, 'filled', f'{short_iri(new[1])}: definition taken from its vocabulary term')
                                break
                    if not filled:
                        ck = new[1][len(self.base):]
                        gen = self.cfg.get('definitions', {}).get(ck)
                        if gen:
                            self.add(dst, new, I(SKOS + 'definition'), L(gen, 'en'))
                            self.add(dst, new, I(SKOS + 'editorialNote'),
                                     L(f'Definition written during ingestion on {self.day:%Y-%m-%d}; review before the term moves to Candidate.', 'en'))
                            self.note(key, 'generated', f'{short_iri(new[1])}: definition written ("{gen}")')
                        else:
                            self.note(key, 'warn', f'{short_iri(new[1])}: no definition found or configured')
                            self.missing_defs.append((key, new))

                # ownership and scheme membership
                if is_concept:
                    self.add(dst, new, I(SKOS + 'inScheme'), I(asset))
                    broader = dst[new].get(I(SKOS + 'broader'), [])
                    tops = [self.map_iri(t[1]) for t in g[src['header']].get(SKOS + 'hasTopConcept', [])]
                    if not broader or new[1] in tops:
                        self.add(dst, new, I(SKOS + 'topConceptOf'), I(asset))
                        self.add(dst, I(asset), I(SKOS + 'hasTopConcept'), new)
                    for b in broader:
                        self.add(dst, b, I(SKOS + 'narrower'), new)
                else:
                    self.add(dst, new, I(RDFS + 'isDefinedBy'), I(asset))
                if src['kind'] == 'taxonomy' and not dst[new].get(I(DCT + 'subject')):
                    alts = [a[1] for a in ps.get(SKOS + 'altLabel', []) if a[0] == 'L']
                    hit = self.vocab_match(label, alts, src['domain'], vocab_by_label)
                    if hit:
                        self.add(dst, new, I(DCT + 'subject'), I(hit))
                        self.note(key, 'fixed', f'{short_iri(new[1])}: linked to vocabulary term {short_iri(hit)} (same label)')
                if src['kind'] == 'taxonomy':
                    self.primary_term(key, dst, new, label, vocab_terms)
                self.governance(dst, new, self.earliest(ps))
                o['subjects'].append(new)

            self.header(src, o)

        # move narrower triples written before their subject existed to the end of each subject
        for o in self.outputs.values():
            for s in list(o['graph']):
                if s not in o['subjects'] and s != o['header'] and s[0] == 'I':
                    # a broader target defined in this graph is always in subjects; anything else is a stray
                    self.note(self.key_of(o), 'warn', f'Reference to undefined term {s[1]}')
                    del o['graph'][s]

    def primary_term(self, key, dst, new, label, vocab_terms):
        """core:hasPrimaryTerm: the one vocabulary term that names the concept (§3.11). Of the concept's
        dcterms:subject terms, the one whose label matches; else the only one; else left for review."""
        if dst[new].get(I(self.HAS_PRIMARY)): return
        subs = [x for x in dst[new].get(I(DCT + 'subject'), []) if x[0] == 'I' and '/vocabulary/' in x[1]]
        if not subs: return
        def vlabel(t):
            ps = vocab_terms.get(t[1])
            if ps: return self.labels.get(t[1], self.pref(ps)).lower()
            ev = getattr(self, 'extra_vocab', {}).get(t[1])
            return ev[0].lower() if ev else ''
        same = [x for x in subs if vlabel(x) == label.lower()]
        pick = same[0] if same else (subs[0] if len(subs) == 1 else None)
        if pick: self.add(dst, new, I(self.HAS_PRIMARY), pick)
        else: self.note(key, 'warn', f'{short_iri(new[1])}: {len(subs)} vocabulary terms and none named like the concept; choose its primary term')

    def surviving_parents(self, old, p, seen=None):
        """Parents of a removed term that are not removed themselves (walking up)."""
        seen = seen or set()
        if old in seen: return []
        seen.add(old)
        out = []
        for src in self.sources:
            ps = src['graph'].get(I(old))
            if not ps: continue
            for par in ps.get(p, []):
                if par[0] != 'I': continue
                out += self.surviving_parents(par[1], p, seen) if par[1] in self.dropped else [par[1]]
        return out

    def is_bare(self, s, ps):
        """A term from another namespace that the file only declares: its type, and at most a
        super-property, domain or range that also lies outside the base URL. Leftovers of
        earlier editing sessions; nothing in the model can use them."""
        if s[1] in self.cross or s[1].startswith(self.base): return False
        if not set(ps) <= {RDF + 'type', RDFS + 'subPropertyOf', RDFS + 'domain', RDFS + 'range'}: return False
        for p in (RDFS + 'subPropertyOf', RDFS + 'domain', RDFS + 'range'):
            for o in ps.get(p, []):
                if o[0] != 'I' or self.map_iri(o[1]).startswith(self.base): return False
        return True

    @staticmethod
    def looks_like_definition(text):
        t = text.strip()
        return len(t.split()) >= 4 and t.endswith('.') and t[:1].isupper()

    def key_of(self, o):
        for k, v in self.outputs.items():
            if v is o: return k

    def vocab_match(self, label, alts, domain, vocab_by_label):
        """The vocabulary term a taxonomy term names, matched on preferred or alternative label:
        this run's vocabularies first, then the vocabularies already in the destination folder.
        A match in the vocabulary of the same domain wins; an ambiguous match is left for review."""
        names = {x.strip().lower() for x in [label] + alts if x and x.strip()}
        same = self.asset_iri('vocabulary', domain)
        hits = [iri for (va, l), iri in vocab_by_label.items() if l in names]
        for t, (pref, a2, scheme, _d) in getattr(self, 'extra_vocab', {}).items():
            if pref.lower() in names or any(x.lower() in names for x in a2):
                hits.append(t)
        hits = list(dict.fromkeys(hits))
        if len(hits) == 1:
            return hits[0]
        local = [h for h in hits if h.startswith(same)]
        return local[0] if len(local) == 1 else None

    def subject_link(self, key, cls, old, label, vocab_terms, vocab_by_label):
        """Re-point dc:subject to the new vocabulary IRI and check it names the same thing."""
        new = self.cross.get(old)
        c = self.classify(old)
        vasset = self.asset_iri(c[0], c[1]) if c else None
        if new:
            vlabel = self.pref(vocab_terms.get(new, {})).lower()
            if vlabel and vlabel != label.lower():
                better = vocab_by_label.get((vasset, label.lower()))
                if better:
                    self.note(key, 'fixed', f'{short_iri(cls)}: dc:subject pointed at "{vlabel}"; re-pointed to {short_iri(better)}')
                    return better
                self.note(key, 'warn', f'{short_iri(cls)}: linked vocabulary term is labelled "{vlabel}"')
            return new
        if c and c[0] == 'vocabulary':
            hit = self.vocab_match(label, [], c[1], vocab_by_label)      # the vocabulary is already in the destination
            if hit:
                return hit
            predicted = vasset + slug(label)
            self.note(key, 'unresolved', f'{short_iri(cls)}: vocabulary {c[1]} was not in this run; dc:subject set to the expected IRI {short_iri(predicted)}')
            return predicted
        return self.map_iri(old)

    def shape(self, src, s, ps, shapes_key):
        tgt0 = ps.get(SH + 'targetClass', [None])[0]
        if tgt0 and tgt0[0] == 'I' and tgt0[1] in self.dropped:
            self.note(shapes_key, 'dropped', f'{s[1].rstrip("/").split("/")[-1]} removed with the class it targets ({self.dropped[tgt0[1]]})')
            return
        new = I(self.cross[s[1]])
        asset = self.asset_iri('shapes', src['domain'])
        o = self.out(shapes_key, asset, 'shapes')
        if src not in o['sources']: o['sources'].append(src)
        dst = o['graph']
        for p, objs in ps.items():
            if p not in self.KEEP_TERM:
                if p not in self.REBUILT: self.removed[shapes_key][p] += len(objs)
                continue
            for ob in objs:
                if ob[0] == 'B': self.copy_bnode(src['graph'], dst, ob, shapes_key)
                self.add(dst, new, I(p), self.map_term(ob))
        tgt = dst[new].get(I(SH + 'targetClass'), [None])[0]
        tl = self.labels.get(tgt[1]) if tgt else None
        if not tl and tgt: tl = sentence_case(split_camel(tgt[1].rstrip('/').split('/')[-1]), self.keep)
        lab = f'{tl} shape' if tl else sentence_case(split_camel(new[1].split('/')[-1]))
        self.add(dst, new, I(RDFS + 'label'), L(lab, 'en'))
        self.add(dst, new, I(RDFS + 'isDefinedBy'), I(asset))
        self.governance(dst, new, self.earliest(ps))
        o['subjects'].append(new)
        if tgt and not tgt[1].startswith(self.asset_iri('ontology', src['domain'])):
            self.note(shapes_key, 'warn', f'{short_iri(new[1])} constrains {short_iri(tgt[1])}, a class from another model; it stays with the {src["domain"]} shapes because it was authored here')
        self.note(shapes_key, 'moved', f'{short_iri(s[1])} → {short_iri(new[1])}')

    def header(self, src, o):
        g, h, key = src['graph'], src['header'], src['key']
        dst, asset = o['graph'], o['header']
        hp = g[h]
        meta = self.cfg.get('assets', {}).get(key, {})
        legacy = self.pref(hp)
        title = meta.get('title') or f'{sentence_case(src["domain"].replace("-", " "))} {src["kind"]}'
        self.add(dst, asset, TYPE, I(SKOS + 'ConceptScheme') if src['scheme'] else I(OWL + 'Ontology'))
        self.add(dst, asset, I(RDFS + 'label'), L(title, 'en'))
        if src['scheme']: self.add(dst, asset, I(SKOS + 'prefLabel'), L(title, 'en'))
        self.add(dst, asset, I(DCT + 'title'), L(title, 'en'))
        if legacy and legacy != title: self.add(dst, asset, I(SKOS + 'altLabel'), L(legacy, 'en'))
        for a in hp.get(SKOS + 'altLabel', []):
            if a[0] == 'L': self.add(dst, asset, I(SKOS + 'altLabel'), L(a[1], a[2] or 'en'))
        desc = meta.get('description')
        if desc:
            self.add(dst, asset, I(DCT + 'description'), L(desc, 'en'))
        else:
            d = [x for x in hp.get(DCT + 'description', []) + hp.get(RDFS + 'comment', []) if x[0] == 'L']
            if d:
                self.add(dst, asset, I(DCT + 'description'), L(clean(d[0][1]), 'en'))
            else:
                gen = self.describe(src, o)
                self.add(dst, asset, I(DCT + 'description'), L(gen, 'en'))
                self.add(dst, asset, I(SKOS + 'editorialNote'),
                         L(f'Description generated during ingestion on {self.day:%Y-%m-%d} from the asset\'s content; review it.', 'en'))
                self.note(key, 'generated', f'Description written: "{gen}"')
        if not meta.get('title'):
            self.note(key, 'generated', f'Title written: "{title}" (add an entry under "assets" in the config to change it)')
        self.add(dst, asset, I(DCT + 'language'), L('en'))
        if not src['scheme']:
            for imp in hp.get(OWL + 'imports', []):
                self.add(dst, asset, I(OWL + 'imports'), I(self.map_iri(imp[1])))
        self.header_311(dst, asset, key)
        if meta.get('editorialNote'): self.add(dst, asset, I(SKOS + 'editorialNote'), L(meta['editorialNote'], 'en'))
        self.add(dst, asset, I(SKOS + 'changeNote'), L(
            f'{self.version} ({self.day:%Y-%m-%d}): ingested into the {self.base} namespace; IRIs, labels and metadata '
            f'brought into line with {self.cfg["standardsRef"]}.', 'en'))
        self.governance(dst, asset, self.earliest(hp))
        self.add(dst, asset, I(DCT + 'contributor'), self.author_term)
        for p, objs in hp.items():
            if p not in self.REBUILT and p not in (RDF + 'type', OWL + 'imports', DCT + 'title', DCT + 'description', SKOS + 'altLabel'):
                self.removed[key][p] += len(objs)

    def prefix_name(self, kind, domain):
        """Namespace prefix by the naming convention: core-process taxonomy → processtax, domain-finance vocabulary → domainfinancevoc."""
        name = domain.replace('core-', '').replace('-', '') or domain
        return {'ontology': name, 'taxonomy': name + 'tax', 'vocabulary': name + 'voc', 'shapes': name + 'shp'}[kind]

    def header_311(self, g, asset, key):
        """The §3.11 header fields every vocabulary, taxonomy, ontology and shapes graph carries."""
        kind, domain = key.split('/', 1)
        meta = self.cfg.get('assets', {}).get(key, {})
        self.add(g, asset, I(VAEM + 'namespace'), L(asset[1], None, XSD + 'anyURI'))
        self.add(g, asset, I(VANN + 'preferredNamespacePrefix'), L(meta.get('prefix') or self.prefix_name(kind, domain)))
        self.add(g, asset, I(OWL + 'versionIRI'), I(asset[1] + self.version + '/'))
        if self.cfg.get('publisher'):
            self.add(g, asset, I(DCT + 'publisher'), I(self.cfg['publisher']))
        else:
            self.note(key, 'warn', 'No dcterms:publisher: set "publisher" (an organization IRI) in the config')
        conf = list(self.cfg.get('conformsTo', []) or [])
        if kind == 'ontology': conf += list(self.cfg.get('ontologyConformsTo', []) or [])
        for c in conf: self.add(g, asset, I(DCT + 'conformsTo'), I(c))
        if not conf: self.note(key, 'warn', 'No dcterms:conformsTo: set "conformsTo" (the IRI of the guide edition) in the config')
        subj = meta.get('subject') or self.cfg.get('defaultSubject')
        for x in ([subj] if isinstance(subj, str) else subj or []):
            self.add(g, asset, I(DCT + 'subject'), I(x))
        if not subj: self.note(key, 'warn', f'No dcterms:subject: add "subject" (a domain taxonomy concept) under assets/{key} in the config')

    def describe(self, src, o):
        """One-sentence description built from what the asset contains."""
        g = o['graph']
        subs = [x for x in o['subjects']]
        n = len(subs)
        lab = lambda x: (self.pref_out(g[x]) or split_camel(x[1].rstrip('/').split('/')[-1])).lower()
        parent_p = I(SKOS + 'broader') if src['scheme'] else I(RDFS + 'subClassOf')
        inset = set(subs)
        roots = [x for x in subs if not any(p in inset for p in g[x].get(parent_p, []))]
        second = [x for x in subs if any(p in roots for p in g[x].get(parent_p, []))]
        show = sorted({lab(x) for x in (second if 1 <= len(roots) <= 2 and second else roots)})
        def listing(items):
            items = items[:6]
            return items[0] if len(items) == 1 else ', '.join(items[:-1]) + ' and ' + items[-1]
        topic = src['domain'].replace('core-', '').replace('domain-', '').replace('-', ' ')
        if src['scheme'] and src['kind'] == 'taxonomy':
            text = f'A taxonomy of {n} concept{"s" if n != 1 else ""} for classifying {topic}'
        elif src['scheme']:
            text = f'A controlled vocabulary of {n} {topic} term{"s" if n != 1 else ""} with preferred labels, synonyms and definitions'
        elif src['kind'] == 'taxonomy':
            text = f'A taxonomy of {n} class{"es" if n != 1 else ""} for classifying {topic}'
        else:
            text = f'An ontology of {n} class{"es" if n != 1 else ""} that describes {topic}'
        if show: text += f', covering {listing(show)}'
        return text + '.'

    def finish_headers(self):
        """owl:imports for every other ontology/taxonomy a model's axioms refer to; shapes header."""
        for key, o in self.outputs.items():
            g, asset = o['graph'], o['header']
            if key.startswith('shapes/'):
                domain = key.split('/', 1)[1]
                meta = self.cfg.get('assets', {}).get(key, {})
                title = meta.get('title') or f'{sentence_case(domain.replace("-", " "))} shapes'
                self.add(g, asset, TYPE, I(OWL + 'Ontology'))
                self.add(g, asset, I(RDFS + 'label'), L(title, 'en'))
                self.add(g, asset, I(DCT + 'title'), L(title, 'en'))
                if meta.get('description'): self.add(g, asset, I(DCT + 'description'), L(meta['description'], 'en'))
                self.add(g, asset, I(DCT + 'language'), L('en'))
                self.add(g, asset, I(SKOS + 'changeNote'), L(
                    f'{self.version} ({self.day:%Y-%m-%d}): shapes moved out of the {domain} ontology into their own shapes graph '
                    f'under {self.base}shapes/, as {self.cfg["standardsRef"]} requires.', 'en'))
                self.governance(g, asset, min((self.earliest(src['graph'][src['header']]) for src in o['sources']),
                                              key=lambda x: x[1] if x else '9', default=None))
                self.add(g, asset, I(DCT + 'contributor'), self.author_term)
                self.header_311(g, asset, key)
            if o['kind'] == 'taxonomy':
                # dcterms:source: the vocabularies whose terms the concepts draw on (§3.11)
                for v in sorted({x[1] for sub in o['subjects'] for x in g.get(sub, {}).get(I(DCT + 'subject'), [])
                                 if x[0] == 'I' and '/vocabulary/' in x[1] and x[1].startswith(self.base)}):
                    parts = v[len(self.base):].split('/')
                    if len(parts) >= 3: self.add(g, asset, I(DCT + 'source'), I(self.asset_iri('vocabulary', parts[1])))
                if not g[asset].get(I(DCT + 'source')):
                    self.note(key, 'warn', 'No dcterms:source: none of the concepts is linked to a vocabulary term')
            if o['kind'] == 'vocabulary': continue
            refs = set()
            for s in o['subjects']:
                for p in (RDFS + 'subClassOf', SH + 'targetClass', SH + 'class', SH + 'path'):
                    for ob in g[s].get(I(p), []): refs.add(ob)
            for b in [x for x in g if x[0] == 'B']:
                for p in (SH + 'class', SH + 'path'):
                    for ob in g[b].get(I(p), []): refs.add(ob)
            for r in refs:
                if r[0] != 'I' or not r[1].startswith(self.base): continue
                parts = r[1][len(self.base):].split('/')
                if parts[0] in ('ontology', 'taxonomy') and len(parts) >= 3:
                    tgt = self.asset_iri(parts[0], parts[1])
                    if tgt != asset[1]:
                        if I(tgt) not in g[asset].get(I(OWL + 'imports'), []):
                            self.note(key, 'filled', f'owl:imports {short_iri(tgt)} added (referenced by the model)')
                        self.add(g, asset, I(OWL + 'imports'), I(tgt))

    # ── writing ──────────────────────────────────────────────────────────────
    def prefixes_for(self, key, o):
        px = {'rdf': RDF, 'rdfs': RDFS, 'owl': OWL, 'xsd': XSD, 'skos': SKOS, 'dct': DCT, 'dc': DC,
              'vann': VANN, 'vaem': VAEM, 'core': self.CORE, 'sh': SH}
        kind, domain = key.split('/', 1)
        own = self.cfg.get('assets', {}).get(key, {}).get('prefix') or self.prefix_name(kind, domain)
        px[own if own not in px else {'vocabulary': 'voc', 'taxonomy': 'tax', 'ontology': 'ont', 'shapes': 'shp'}[kind]] = self.asset_iri(kind, domain)
        seen = {}
        for s, ps in o['graph'].items():
            for objs in list(ps.values()) + [[s]]:
                for t in objs:
                    if t[0] == 'I' and t[1].startswith(self.base):
                        parts = t[1][len(self.base):].split('/')
                        if len(parts) >= 3 and parts[0] in ('ontology', 'taxonomy', 'vocabulary', 'shapes'):
                            ns = self.asset_iri(parts[0], parts[1])
                            if ns not in px.values():
                                name = parts[1].replace('core-', '').replace('-', '') or parts[1]
                                name = {'ontology': name, 'taxonomy': name + 'tax', 'vocabulary': name + 'voc', 'shapes': name + 'shp'}[parts[0]]
                                if parts[0] == 'ontology' and parts[1] == 'core': continue
                                seen[name] = ns
        px.update({k: v for k, v in seen.items() if k not in px})
        return px

    def order_subjects(self, o):
        """Header first, then terms top-down by hierarchy, alphabetically within a level."""
        g, subs = o['graph'], o['subjects']
        is_scheme = I(SKOS + 'ConceptScheme') in g.get(o['header'], {}).get(TYPE, [])
        parent_p = I(SKOS + 'broader') if is_scheme else I(RDFS + 'subClassOf')
        inset = set(subs)
        kids = collections.defaultdict(list); roots = []
        for s in subs:
            ps = [p for p in g[s].get(parent_p, []) if p in inset]
            if ps: kids[ps[0]].append(s)
            else: roots.append(s)
        lab = lambda s: (self.pref_out(g[s]) or s[1]).lower()
        order, seen = [o['header']], set()
        def walk(s):
            if s in seen: return
            seen.add(s); order.append(s)
            for c in sorted(kids[s], key=lab): walk(c)
        for r in sorted(roots, key=lab): walk(r)
        for s in subs:
            if s not in seen: order.append(s)
        return order

    @staticmethod
    def pref_out(ps):
        for o in ps.get(I(SKOS + 'prefLabel'), []) + ps.get(I(RDFS + 'label'), []):
            return o[1]

    def write(self, outdir, ttl_dir='ttl', trig_dir='trig'):
        outdir = pathlib.Path(outdir)
        tdir, gdir = outdir / ttl_dir, outdir / trig_dir
        tdir.mkdir(parents=True, exist_ok=True); gdir.mkdir(parents=True, exist_ok=True)
        self.trig_files = {}
        files = {}
        for key, o in self.outputs.items():
            kind, domain = key.split('/', 1)
            # convert graph keys (terms) to writer form: predicates as strings
            g2 = collections.OrderedDict()
            for s, ps in o['graph'].items():
                g2[s] = collections.OrderedDict((p[1], objs) for p, objs in ps.items())
            w = Writer(self.prefixes_for(key, o), [self.HAS_STATUS] + GOV_TAIL[1:])
            title = self.pref_out(o['graph'][o['header']]) or key
            srcs = ', '.join(pathlib.Path(s['path']).name for s in o['sources'])
            head = (f'# {title}\n# {o["header"][1]}  ·  version {self.version}  ·  {self.cfg["lifecycleStatus"]}\n'
                    f'# Generated by ke_ingest.py on {self.now_lit[1]} from {srcs}\n'
                    f'# Standards: {self.cfg["standardsRef"]}\n')
            text = w.write(g2, self.order_subjects(o), head)
            name = f'{kind}-{domain}-{self.version}.ttl'
            (tdir / name).write_text(text, encoding='utf-8')
            files[key] = tdir / name
            # TriG copy: the named graph is the asset IRI, which is how the KE Workbench finds an asset
            trig = w.write_trig(g2, self.order_subjects(o), head.replace('\n# Standards', f'\n# Named graph: {o["header"][1]}\n# Standards'), o['header'][1])
            (gdir / name.replace('.ttl', '.trig')).write_text(trig, encoding='utf-8')
            self.trig_files[key] = gdir / name.replace('.ttl', '.trig')
        return files

def clean(s): return re.sub(r'\s+', ' ', s).strip()
def short(p):
    for pre, ns in (('rdfs', RDFS), ('rdf', RDF), ('owl', OWL), ('skos', SKOS), ('dct', DCT), ('dc', DC),
                    ('sh', SH), ('oslc', 'http://open-services.net/ns/core#'), ('vaem', 'http://www.linkedmodel.org/1.2/schema/vaem#'),
                    ('bibo', 'http://purl.org/ontology/bibo/')):
        if p.startswith(ns): return pre + ':' + p[len(ns):]
    return '<' + p + '>'
def short_iri(v):
    v = v.replace('https://www.insperity.com/', '…/')
    return v

# ─────────────────────────────────────────────────────────────────────────────
# Part III conformance checks (same rules as the workbench's Standards Conformance tool)
# ─────────────────────────────────────────────────────────────────────────────
REFERENCE_NS = ('http://purl.obolibrary.org/obo/', 'https://purl.obolibrary.org/obo/', 'http://www.w3.org/', 'http://purl.org/')   # BFO, RO, IAO, W3C and DCMI vocabularies

STANDARD_NS = ('http://www.w3.org/', 'https://www.w3.org/', 'http://purl.org/', 'http://purl.obolibrary.org/', 'http://www.linkedmodel.org/',
               'http://xmlns.com/', 'https://schema.org/', 'http://schema.org/', 'http://qudt.org/')

def check(triples, base, policy=None, vocab=None):
    ents = collections.OrderedDict()
    for s, p, o in triples:
        if s[0] != 'I': continue
        e = ents.setdefault(s[1], collections.defaultdict(list)); e[p[1]].append(o)
    res = collections.OrderedDict()
    def r(rule, sev, iri, msg): res.setdefault(rule, []).append((sev, iri, msg))
    counted = collections.Counter()
    for iri, e in ents.items():
        types = {t[1] for t in e.get(RDF + 'type', [])}
        kind = ('ontology' if OWL + 'Ontology' in types else 'scheme' if SKOS + 'ConceptScheme' in types else
                'concept' if SKOS + 'Concept' in types else 'class' if OWL + 'Class' in types else
                'shape' if SH + 'NodeShape' in types else None)
        if not kind:
            # any other typed term from outside the base URL (an individual or a datatype left over from
            # another organization's ontology) is still foreign content
            if types and not iri.startswith(base) and not iri.startswith(STANDARD_NS):
                r('Base URL (§3.2)', 'error', iri, 'term from another ontology (' + ', '.join(sorted(t.rsplit('#', 1)[-1].rsplit('/', 1)[-1] for t in types)) + ')')
            continue
        counted[kind] += 1
        lits = lambda p: [o for o in e.get(p, []) if o[0] == 'L']
        prefs = lits(SKOS + 'prefLabel') or lits(RDFS + 'label')
        segs = iri[len(base):].split('/') if iri.startswith(base) else []
        local = iri.rstrip('/').split('/')[-1]
        if not iri.startswith(base): r('Base URL (§3.2)', 'error', iri, 'outside the base URL')
        elif '#' in iri: r('URI pattern (§3.2)', 'warn', iri, 'hash namespace')
        else:
            want = {'concept': ('vocabulary', 'taxonomy'), 'scheme': ('vocabulary', 'taxonomy'), 'shape': ('shapes',),
                    'class': ('ontology', 'taxonomy'), 'ontology': ('ontology', 'taxonomy', 'shapes')}[kind]
            if segs[0] not in want: r('URI pattern (§3.2)', 'warn', iri, f'{kind} under /{segs[0]}/')
            if len(segs) > 1 and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', segs[1]): r('URI pattern (§3.2)', 'warn', iri, 'domain segment not lower-case hyphenated')
            if kind in ('class', 'concept', 'shape') and len(segs) != 3: r('URI pattern (§3.2)', 'warn', iri, 'expected {kind}/{domain}/{Term}')
        if kind == 'class' and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', local): r('Identifier case (§3.2)', 'warn', iri, 'class not lower-case hyphenated')
        if kind == 'concept' and segs and segs[0] == 'vocabulary' and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', local): r('Identifier case (§3.2)', 'warn', iri, 'vocabulary term not lower-case hyphenated')
        if kind == 'concept' and segs and segs[0] == 'taxonomy' and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', local): r('Identifier case (§3.2)', 'warn', iri, 'taxonomy concept not lower-case hyphenated')
        if kind == 'class' and segs and segs[0] == 'taxonomy': r('Taxonomies stay in SKOS (§3.11)', 'warn', iri, 'OWL class in a taxonomy')
        for p_ in (DCT + 'created', DCT + 'modified', DCT + 'issued'):
            for d_ in e.get(p_, []):
                if d_[0] == 'L' and d_[3] in (XSD + 'date', XSD + 'dateTime') and (date_lit(d_[1]) or ('', '', '', ''))[3] != d_[3]:
                    r('Valid dates (ISO 8601)', 'error', iri, f'{short(p_)} "{d_[1]}" is not a valid {d_[3].split("#")[1]}')
        if kind == 'shape' and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*-shape', local): r('Identifier case (§3.2)', 'warn', iri, 'shape not {class}-shape')
        if kind in ('class', 'shape') and CAMEL_ACR.search(local): r('No acronyms in identifiers (§3.2)', 'error', iri, local)
        for l in prefs:
            bad = policy.acronyms(l[1]) if policy else [m.group(0) for m in ACRONYM.finditer(l[1])]
            if bad: r('No acronyms in preferred labels (§3.2)', 'error', iri, f'{l[1]} ({", ".join(bad)})')
        if policy and policy.orgs:
            for p_, field in ((SKOS + 'prefLabel', 'label'), (RDFS + 'label', 'label'), (SKOS + 'altLabel', 'alternative label'),
                              (SKOS + 'definition', 'definition'), (DCT + 'description', 'description'), (RDFS + 'comment', 'comment'),
                              (DCT + 'title', 'title')):
                for l in lits(p_):
                    o_, hit = policy.org_hit(l[1])
                    if o_:
                        r('No other organization\'s content', 'error', iri, f'{field} names {o_["name"]} ("{hit}")'); break
        alllab = lits(RDFS + 'label') + lits(SKOS + 'prefLabel')
        if kind != 'shape' and not alllab: r('Label present, tagged @en (§3.7)', 'error', iri, 'no label')
        for l in alllab:
            if not l[2]: r('Label present, tagged @en (§3.7)', 'error', iri, f'"{l[1]}" untagged')
        if kind in ('class', 'concept'):
            for l in prefs:
                w = l[1].split()
                if len(w) > 1 and sum(1 for x in w[1:] if re.match(r'[A-Z][a-z]', x) and len(x) > 2) >= max(1, (len(w) - 1 + 1) // 2):
                    r('Sentence-case labels (§3.2)', 'warn', iri, l[1])
            d = lits(SKOS + 'definition')
            if not d: r('Definition present (§3.7)', 'error', iri, 'no skos:definition')
            else:
                t = d[0][1]
                if not re.match(r'(A|An)\s', t): r('Genus plus differentia (§3.7)', 'info', iri, 'does not open "A …/An …": ' + t[:60])
            if re.search(r'/v?\d+\.\d+(\.\d+)?/', iri): r('No version in term IRIs (§3.3)', 'error', iri, 'version in IRI')
            if not e.get(DCT + 'creator') or not e.get(DCT + 'modified') or not e.get(owl_v := OWL + 'versionInfo'):
                r('Governance fields (§3.7)', 'error', iri, 'missing creator / modified / versionInfo')
        if kind == 'class':
            named = [o for o in e.get(RDFS + 'subClassOf', []) if o[0] == 'I' and o[1] != OWL + 'Thing']
            if not named: r('Named parent class (§3.7)', 'warn', iri, 'root class: no named rdfs:subClassOf parent')
            if not e.get(RDFS + 'isDefinedBy'): r('rdfs:isDefinedBy (§3.7)', 'warn', iri, 'missing')
            if e.get(OWL + 'equivalentClass'): r('Restricted OWL constructs (§3.7)', 'info', iri, 'owl:equivalentClass')
        if kind == 'concept':
            if not e.get(SKOS + 'inScheme'): r('Concept in scheme, one preferred label (§3.9)', 'error', iri, 'no skos:inScheme')
            langs = collections.Counter(l[2] for l in lits(SKOS + 'prefLabel'))
            if any(v > 1 for v in langs.values()): r('Concept in scheme, one preferred label (§3.9)', 'error', iri, 'several prefLabels per language')
        if kind in ('ontology', 'scheme'):
            v = lits(OWL + 'versionInfo')
            if not v or not re.fullmatch(r'\d+\.\d+\.\d+', v[0][1]): r('Semantic version on releases (§3.3)', 'warn', iri, 'versionInfo not MAJOR.MINOR.PATCH')
            if not e.get(OWL + 'versionIRI'): r('Semantic version on releases (§3.3)', 'warn', iri, 'no owl:versionIRI')
            want = [(VAEM + 'namespace', 'vaem:namespace'), (VANN + 'preferredNamespacePrefix', 'vann:preferredNamespacePrefix'),
                    (DCT + 'title', 'dcterms:title'), (DCT + 'description', 'dcterms:description'), (DCT + 'language', 'dcterms:language'),
                    (DCT + 'creator', 'dcterms:creator'), (DCT + 'publisher', 'dcterms:publisher'), (DCT + 'subject', 'dcterms:subject'),
                    (DCT + 'conformsTo', 'dcterms:conformsTo'), (DCT + 'created', 'dcterms:created'), (DCT + 'modified', 'dcterms:modified')]
            if segs[:1] == ['taxonomy']: want.append((DCT + 'source', 'dcterms:source'))
            miss = [n for p_, n in want if not e.get(p_)]
            if miss: r('Asset header fields (§3.11)', 'warn', iri, 'missing ' + ', '.join(miss))
            if kind == 'scheme' and not e.get(SKOS + 'hasTopConcept'): r('One scheme, top concepts flagged (E.3)', 'error', iri, 'no top concepts')
        if vocab is not None and kind in ('class', 'concept') and segs[:1] == ['taxonomy']:
            primary = base + 'ontology/core/hasPrimaryTerm'
            subj = [o[1] for p_ in SUBJECT_IN + (primary,) for o in e.get(p_, []) if o[0] == 'I']
            if not subj:
                r('Taxonomy term in a vocabulary (§3.11)', 'error', iri, 'not linked to a vocabulary term (no core:hasPrimaryTerm or dcterms:subject)')
            elif not any(x in vocab for x in subj):
                r('Taxonomy term in a vocabulary (§3.11)', 'error', iri, 'linked to ' + ', '.join(short_iri(x) for x in subj) + ', which is in no vocabulary')
            elif not e.get(primary):
                r('Taxonomy term in a vocabulary (§3.11)', 'warn', iri, 'no core:hasPrimaryTerm')
            if e.get(DC + 'subject'):
                r('Dublin Core terms (§3.11)', 'info', iri, 'dc:subject (Dublin Core 1.1): use dcterms:subject')
    return counted, res

# ─────────────────────────────────────────────────────────────────────────────
# Report, crosswalk, change record
# ─────────────────────────────────────────────────────────────────────────────
def change_record(ing, outputs, skipped):
    """PROV-O change record for the append-only change-log graph (§3.3). Returns (ttl, trig, id)."""
    stamp = f'{ing.now:%Y-%m-%dT%H%M%SZ}'
    rid = f'{ing.base}resource/change-log/ChangeRecord/{stamp}-ingestion'
    log = f'{ing.base}graph/change-log'
    def q(v): return '"' + _esc_lit(v) + '"'
    n_assets = len(outputs)
    desc = (f'Ingested {len(ing.sources)} source file{"s" if len(ing.sources) != 1 else ""} into {n_assets} asset{"s" if n_assets != 1 else ""} '
            f'under {ing.base}, with IRIs, labels and metadata brought into line with {ing.cfg["standardsRef"]}. '
            f'Every asset is at version {ing.version}, {ing.cfg["lifecycleStatus"]}.')
    plural = lambda n, w: f'{n} {w}' + ('' if n == 1 else 's')
    desc += ' Results: ' + '; '.join(f'{o["title"]} ({plural(o["terms"], "term")}, {plural(o["errors"], "conformance error")}, '
                                     f'{plural(o["warnings"], "warning")})' for o in outputs) + '.'
    if skipped: desc += f' {len(skipped)} file{"s were" if len(skipped) != 1 else " was"} skipped: ' + ', '.join(x['name'] for x in skipped) + '.'
    body = [f'<{rid}> a prov:Activity , dct:ProvenanceStatement ;',
            f'  rdfs:label {q("Ingestion of knowledge artifacts, " + ing.now_lit[1])}@en ;',
            f'  dct:description {q(desc)}@en ;',
            f'  dct:creator {q(ing.author)} ;',
            f'  prov:startedAtTime "{ing.now_lit[1]}"^^xsd:dateTime ;',
            f'  prov:endedAtTime "{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ}"^^xsd:dateTime ;',
            '  dct:source ' + ' ,\n    '.join(q(s['name']) for s in ing.sources) + ' ;',
            '  prov:used ' + ' ,\n    '.join(f'<{u}>' for u in sorted({s["header"][1] for s in ing.sources})) + ' ;',
            '  prov:generated ' + ' ,\n    '.join(f'<{o["iri"]}>' for o in outputs) + ' .']
    # Only PROV links go on the asset IRIs: anything else here (a version, a label) would be
    # read back as the asset's own metadata by tools that query across graphs.
    for o in outputs:
        derived = sorted({s['header'][1] for s in ing.outputs[o['key']]['sources']})
        body += ['', f'<{o["iri"]}>', f'  prov:wasGeneratedBy <{rid}> ;',
                 '  prov:wasDerivedFrom ' + ' , '.join(f'<{d}>' for d in derived) + ' .']
    pre = (f'# Change record {stamp} for the {log} graph (append-only, §3.3)\n'
           f'@prefix prov: <{PROV}> .\n@prefix dct: <{DCT}> .\n@prefix rdfs: <{RDFS}> .\n@prefix owl: <{OWL}> .\n@prefix xsd: <{XSD}> .\n\n')
    ttl = pre + '\n'.join(body) + '\n'
    trig = pre + f'<{log}> {{\n\n' + '\n'.join(('  ' + l) if l else l for l in body) + '\n}\n'
    return ttl, trig, rid, stamp


def report_md(ing, outputs, skipped, files, checks, cr_names):
    R = [f'# Ingestion report\n\nRun {ing.now_lit[1]} · base URL `{ing.base}` · author {ing.author} · '
         f'version {ing.version} ({ing.cfg["lifecycleStatus"]})\n\nStandards: {ing.cfg["standardsRef"]}\n']
    R.append('## Outputs\n\n| Asset | IRI | Terms | Triples | Turtle | TriG | From |\n|---|---|---|---|---|---|---|')
    for o in outputs:
        R.append(f'| {o["title"]} | `{o["iri"]}` | {o["terms"]} | {o["triples"]} | `{o["ttl_name"]}` | `{o["trig_name"]}` | {", ".join(o["sources"])} |')
    R.append(f'\nChange record: `{cr_names[0]}` and `{cr_names[1]}`. Crosswalk of every legacy IRI: `crosswalk.csv`.\n')
    if skipped:
        R.append('## Skipped files\n')
        R += [f'- `{x["name"]}` {x["error"]}' for x in skipped]
        R.append('')
    R.append('## Conformance after ingestion\n')
    for key, (counted, res) in checks.items():
        o = next(x for x in outputs if x['key'] == key)
        R.append(f'**{o["ttl_name"]}** — {o["errors"]} errors, {o["warnings"]} warnings, {o["info"]} info')
        for rule, items in res.items():
            R.append(f'- {rule}: ' + '; '.join(f'`{short_iri(i)}` {m}' for _, i, m in items[:6]) + (f' (+{len(items) - 6} more)' if len(items) > 6 else ''))
        R.append('')
    R.append('## What changed, by asset\n')
    R.append(f'On every asset and term the governance fields were rebuilt, not copied: `dct:creator` and (on asset headers) '
             f'`dct:contributor` are {ing.author} only; `dct:created` keeps the source date (or the run time when the source had none); '
             f'`dct:modified` is {ing.now_lit[1]}; `owl:versionInfo` is {ing.version}; lifecycle status is {ing.cfg["lifecycleStatus"]}. '
             'Labels and definitions were re-tagged `@en`. The source values of those fields are not counted below.\n')
    order = ['dropped', 'fixed', 'learned', 'renamed', 'generated', 'filled', 'unresolved', 'moved', 'removed', 'label', 'warn', 'error']
    titles = {'dropped': 'Removed as organization-specific', 'fixed': 'Corrected', 'learned': 'Applied from review decisions', 'renamed': 'Renamed to meet naming rules', 'generated': 'Written during ingestion',
              'filled': 'Filled from existing metadata', 'unresolved': 'Unresolved links', 'moved': 'Moved',
              'removed': 'Removed subjects', 'label': 'Labels put in sentence case', 'warn': 'Review', 'error': 'Errors'}
    for key in list(ing.outputs):
        R.append(f'### {key}\n')
        if ing.foreign.get(key):
            R.append(f'Kept for review: {ing.foreign[key]} terms from other namespaces that carry content (labels, types or links); resolve them in Conformance Review\n')
        if ing.bare.get(key):
            R.append(f'Broken references removed: {ing.bare[key]} bare declarations of terms from other namespaces (only "a owl:NamedIndividual" or similar, nothing else said about them)\n')
        if ing.orphans.get(key):
            R.append(f'Broken structures removed: {ing.orphans[key]} blank-node restrictions, datatypes or list cells that nothing referred to\n')
        if ing.removed_refs.get(key):
            R.append(f'References to removed terms dropped: {ing.removed_refs[key]} (children were moved up to the removed term\'s parent)\n')
        if ing.removed.get(key):
            R.append('Removed properties: ' + ', '.join(f'`{short(p)}` ×{n}' for p, n in ing.removed[key].most_common()) + '\n')
        by = collections.defaultdict(list)
        for lvl, t in ing.findings.get(key, []): by[lvl].append(t)
        for lvl in order:
            if by[lvl]:
                items = by[lvl]
                if lvl in ('label', 'filled') and len(items) > 8:
                    R.append(f'**{titles[lvl]}** ({len(items)}): ' + '; '.join(items[:5]) + f' … and {len(items) - 5} more\n')
                else:
                    R.append(f'**{titles[lvl]}**\n' + '\n'.join(f'- {t}' for t in items) + '\n')
    return '\n'.join(R)


def load_config(path=None):
    path = pathlib.Path(path) if path else pathlib.Path(__file__).with_name('ke-ingest.config.json')
    return json.loads(path.read_text(encoding='utf-8')), path


def collect(paths, recursive=False):
    """Expand folders into the RDF files they hold (sorted), keep files as given."""
    out = []
    for p in paths:
        p = pathlib.Path(p).expanduser()
        if p.is_dir():
            it = p.rglob('*') if recursive else p.iterdir()
            out += sorted(x for x in it if x.is_file() and x.suffix.lower() in RDF_EXTENSIONS and not x.name.startswith('.'))
        elif p.is_file():
            out.append(p)
    return out


def align_domains(srcs, known=(), log=None):
    """A file named after the singular (core-rule) joins the plural domain already in use (core-rules),
    so the same subject never ends up as two assets. known: domains already in the destination."""
    have = {x['domain'] for x in srcs} | set(known)
    for x in srcs:
        d = x['domain']
        alt = d + 's' if not d.endswith('s') else None
        if alt and d not in known and alt in have and alt != d:
            x['domain'] = alt; x['key'] = f"{x['kind']}/{alt}"
            x['new_iri'] = x['new_iri'].replace(f'/{d}/', f'/{alt}/')
            if log: log(f'note  {x["name"]}: domain {d} → {alt} (same subject as the existing {alt})')
    return srcs


def known_domains(dest, ttl_dir='ttl'):
    d = pathlib.Path(dest) / ttl_dir
    return {h['iri'].rstrip('/').split('/')[-1] for h in folder_plan(d)['current']} if d.is_dir() else set()


def pick_largest(srcs, cfg):
    """Several files for the same asset: keep the largest — most terms (config duplicates: "most-terms",
    the default) or most bytes ("largest-file"). Returns (kept, [(dropped, winner)])."""
    rule = cfg.get('duplicates', 'most-terms')
    size = (lambda x: (pathlib.Path(x['path']).stat().st_size, x['terms'])) if rule == 'largest-file' else \
           (lambda x: (x['terms'], pathlib.Path(x['path']).stat().st_size))
    by = collections.OrderedDict()
    for x in srcs:
        by.setdefault(x['key'], []).append(x)
    kept, dropped = [], []
    for key, xs in by.items():
        xs = sorted(xs, key=size, reverse=True)
        kept.append(xs[0]); dropped += [(x, xs[0]) for x in xs[1:]]
    return kept, dropped


def dup_reason(x, w, cfg):
    unit = 'bytes' if cfg.get('duplicates') == 'largest-file' else 'terms'
    a = pathlib.Path(w['path']).stat().st_size if unit == 'bytes' else w['terms']
    b = pathlib.Path(x['path']).stat().st_size if unit == 'bytes' else x['terms']
    return f'same asset as {w["name"]} ({w["new_iri"]}); the larger file is used: {a:,} {unit} there, {b:,} here'


def scan(paths, cfg, recursive=False, known=()):
    """What each file is and where it would go — nothing is written."""
    ing = Ingest(cfg, datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0))
    rows = []
    for f in collect(paths, recursive):
        row = dict(path=str(f), name=f.name, size=f.stat().st_size, ext=f.suffix.lower())
        try:
            src = ing.inspect(f)
            row.update(ok=True, format=src['format'], kind=src['kind'], domain=src['domain'], header=src['header'][1],
                       label=src['label'], new_iri=src['new_iri'], triples=src['triples'], terms=src['terms'],
                       scheme=src['scheme'], title=(cfg.get('assets', {}).get(src['key'], {}).get('title')
                                                    or f'{sentence_case(src["domain"].replace("-", " "))} {src["kind"]}'))
        except IngestError as e:
            row.update(ok=False, error=str(e))
        rows.append(row)
    srcs = [dict(path=r['path'], name=r['name'], key=f"{r['kind']}/{r['domain']}", kind=r['kind'], domain=r['domain'], new_iri=r['new_iri'], terms=r['terms'], row=r)
            for r in rows if r.get('ok')]
    align_domains(srcs, known)
    for x in srcs:
        x['row'].update(domain=x['domain'], new_iri=x['new_iri'])
    _, dropped = pick_largest(srcs, cfg)
    lost = {x['path']: dup_reason(x, w, cfg) for x, w in dropped}
    for r in rows:
        if r['path'] in lost:
            r.update(ok=False, duplicate=True, error=lost[r['path']])
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Which files in an output folder are current
# ─────────────────────────────────────────────────────────────────────────────
RX_GEN = re.compile(r'^#\s*(\S+)\s+·\s+version\s+(\S+).*\n#\s*Generated by (?:ke_ingest|build_core|migrate_v1)\.py on (\S+) from (.+)$', re.M)
ASSET_PREFIXES = ('vocabulary-', 'taxonomy-', 'ontology-', 'shapes-')


def output_header(path):
    """(asset IRI, version, generated-at, [source file names], title) from an ingested file's header, or None."""
    try:
        head = pathlib.Path(path).read_text(encoding='utf-8', errors='replace')[:1500]
    except OSError:
        return None
    m = RX_GEN.search(head)
    if not m:
        return None
    title = head.split('\n', 1)[0].lstrip('# ').strip()
    return dict(iri=m.group(1), version=m.group(2), generated=m.group(3),
                sources=[x.strip() for x in m.group(4).split(',') if x.strip()], title=title)


def folder_plan(ttl_dir):
    """Split the ingested Turtle files in ttl_dir into current and superseded ones. A file is superseded
    when a later run produced the same asset IRI or was made from any of the same source files, so a
    renamed or re-versioned asset never leaves its old copy behind to be loaded or reviewed."""
    ttl_dir = pathlib.Path(ttl_dir)
    files = []
    for f in sorted(ttl_dir.glob('*.ttl')):
        if not f.name.startswith(ASSET_PREFIXES):
            continue
        h = output_header(f)
        if h:
            h['path'] = f; h['kind'] = f.name.split('-', 1)[0]
            files.append(h)
    files.sort(key=lambda h: (h['generated'], h['path'].stat().st_mtime), reverse=True)   # newest first
    current, superseded, seen = [], [], {}      # key → generated-at of the newest file that claimed it
    for h in files:
        keys = {('iri', h['iri'])} | {(h['kind'], src) for src in h['sources']}
        # only a strictly later run supersedes: one run can make several assets from a single source
        if any(k in seen and seen[k] > h['generated'] for k in keys):
            superseded.append(h)
        else:
            current.append(h)
        for k in keys:
            seen.setdefault(k, h['generated'])
    crs = sorted(ttl_dir.glob('change-record-*.ttl'))
    return dict(current=sorted(current, key=lambda h: h['path'].name), superseded=superseded, change_records=crs)


def vocab_index(ttl_dir, exclude=()):
    """Every vocabulary term in the current vocabulary files of an output folder:
    {term IRI: (preferred label, [alternative labels], vocabulary IRI, definition)}."""
    out = {}
    d = pathlib.Path(ttl_dir)
    if not d.is_dir():
        return out
    for h in folder_plan(d)['current']:
        if h['kind'] != 'vocabulary' or h['path'].name in exclude:
            continue
        try:
            triples, _ = parse_turtle(h['path'].read_text(encoding='utf-8'))
        except Exception:
            continue
        ps = collections.defaultdict(lambda: collections.defaultdict(list))
        for s_, p_, o_ in triples:
            if s_[0] == 'I': ps[s_[1]][p_[1]].append(o_)
        for t, e in ps.items():
            if ('I', SKOS + 'Concept') in e.get(RDF + 'type', []):
                pref = next((o[1] for o in e.get(SKOS + 'prefLabel', []) if o[0] == 'L'), '')
                alts = [o[1] for o in e.get(SKOS + 'altLabel', []) if o[0] == 'L']
                scheme = next((o[1] for o in e.get(SKOS + 'inScheme', []) if o[0] == 'I'), h['iri'])
                dfn = next((o[1] for o in e.get(SKOS + 'definition', []) if o[0] == 'L'), '')
                out[t] = (pref, alts, scheme, dfn)
    return out


def is_corrected(path):
    try:
        return 'Corrected in Conformance Review' in pathlib.Path(path).read_text(encoding='utf-8', errors='replace')[:2500]
    except OSError:
        return False


def keep_corrected(dest, ttl_dir, trig_dir, stems, stamp, log=print):
    """Before a run overwrites files that were corrected in Conformance Review, copy them to
    dest/superseded/<stamp>/ so the corrections are never lost."""
    import shutil
    dest = pathlib.Path(dest); kept = []
    for st in stems:
        t = dest / ttl_dir / (st + '.ttl')
        if t.is_file() and is_corrected(t):
            for f in (t, dest / trig_dir / (st + '.trig')):
                if f.is_file():
                    to = dest / 'superseded' / stamp / f.parent.name
                    to.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, to / f.name); kept.append(f.name)
    if kept:
        log(f'kept {len(kept)} file(s) corrected in Conformance Review in superseded/{stamp}/ before replacing them')
    return kept


def archive_superseded(dest, ttl_dir, trig_dir, stamp, log=print):
    """Move superseded outputs (and their .trig twins) to dest/superseded/<stamp>/ — kept, not deleted."""
    dest = pathlib.Path(dest)
    plan = folder_plan(dest / ttl_dir)
    moved = []
    for h in plan['superseded']:
        for f in (h['path'], dest / trig_dir / (h['path'].stem + '.trig')):
            if f.is_file():
                to = dest / 'superseded' / stamp / f.parent.name
                to.mkdir(parents=True, exist_ok=True)
                f.replace(to / f.name)
                moved.append(f.name)
    if moved:
        log(f'set aside {len(moved)} superseded file(s) from earlier runs in superseded/{stamp}/')
    return moved


# ─────────────────────────────────────────────────────────────────────────────
# Definitions written by Claude (Anthropic API), for terms that have none
# ─────────────────────────────────────────────────────────────────────────────
KEY_FILE = pathlib.Path.home() / '.ke-workbench.env'


def anthropic_key():
    """ANTHROPIC_API_KEY from the environment, or from ~/.ke-workbench.env (KEY=value lines)."""
    import os
    k = os.environ.get('ANTHROPIC_API_KEY', '').strip()
    if k:
        return k
    try:
        for line in KEY_FILE.read_text(encoding='utf-8').splitlines():
            m = re.match(r'\s*(?:export\s+)?ANTHROPIC_API_KEY\s*=\s*["\']?([^"\'\s]+)', line)
            if m:
                return m.group(1)
    except OSError:
        pass
    return ''


DEF_RULES = (
    'Write one definition per term, following Semantic Governance Part III §3.7:\n'
    '- one sentence in genus + differentia form: "A [genus] that [what sets it apart]." (or "An …")\n'
    '- the genus is the broader term when one is given, otherwise the nearest general category\n'
    '- do not use the term itself or its words to define it (no circular definitions)\n'
    '- no acronyms or abbreviations; spell everything out\n'
    '- no company, product or brand names, and no references to any particular organization\n'
    '- plain, precise business English, at most 35 words, ending with a full stop\n'
    '- keep it consistent with the broader term\'s definition and distinct from the sibling terms\n'
    'Answer with JSON only: {"definitions": [{"id": "<id>", "definition": "<text>"}]}')


def generate_definitions(items, cfg, log=print):
    """items: [{id, label, kind, scheme, broader, broader_definition, alternative_labels, narrower, siblings,
    scope_note}]. Returns ({id: definition}, model, error). Calls the Anthropic Messages API in batches."""
    import urllib.request, urllib.error
    key = anthropic_key()
    if not key:
        return {}, None, ('No Anthropic API key. Put ANTHROPIC_API_KEY=… in ' + str(KEY_FILE) +
                          ' (or the environment) and try again; the workbench reads it on each request.')
    model = cfg.get('definitionModel') or 'claude-sonnet-5-5'
    out, err = {}, None
    examples = definition_examples(int(cfg.get('definitionExamples', 12) or 0)) if cfg.get('learnFromReview', True) else []
    for i in range(0, len(items), 25):
        batch = items[i:i + 25]
        system = 'You write definitions for controlled vocabularies and taxonomies. ' + DEF_RULES
        if examples:
            system += ('\n\nReviewers approved or corrected these earlier definitions; follow their style and choices. Where a draft was '
                       'rejected, the approved text shows what the reviewer wanted instead:\n' + json.dumps(examples, ensure_ascii=False, indent=1))
        body = {'model': model, 'max_tokens': 4000, 'system': system,
                'messages': [{'role': 'user', 'content': 'Terms:\n' + json.dumps(batch, ensure_ascii=False, indent=1)}]}
        import os
        req = urllib.request.Request(os.environ.get('KE_ANTHROPIC_URL', 'https://api.anthropic.com/v1/messages'), data=json.dumps(body).encode('utf-8'), method='POST',
                                     headers={'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                resp = json.loads(r.read().decode('utf-8'))
            text = ''.join(c.get('text', '') for c in resp.get('content', []) if c.get('type') == 'text')
            m = re.search(r'\{.*\}', text, re.S)
            for d in (json.loads(m.group(0)).get('definitions', []) if m else []):
                if d.get('id') and d.get('definition'):
                    out[d['id']] = clean(d['definition'])
            log(f'definitions: {len(out)} of {min(i + 25, len(items))} written by {model}')
        except urllib.error.HTTPError as e:
            err = f'Anthropic API answered {e.code}: {e.read().decode("utf-8", "replace")[:300]}'; break
        except Exception as e:                 # network, timeout, malformed answer
            err = f'{type(e).__name__}: {e}'; break
    return out, model, err


def define_missing(ing, log=print):
    """Ingestion: write definitions for the terms that still have none."""
    items, where = [], {}
    for key, t in ing.missing_defs:
        o = ing.outputs.get(key)
        if not o or t not in o['graph']: continue
        g = o['graph']; ps = g[t]
        lab = lambda x: next((l[1] for l in g.get(x, {}).get(I(SKOS + 'prefLabel'), []) + g.get(x, {}).get(I(RDFS + 'label'), []) if l[0] == 'L'), x[1].rstrip('/').split('/')[-1])
        par = (ps.get(I(SKOS + 'broader'), []) + [p for p in ps.get(I(RDFS + 'subClassOf'), []) if p[0] == 'I'])[:1]
        pdef = next((l[1] for l in g.get(par[0], {}).get(I(SKOS + 'definition'), []) if l[0] == 'L'), '') if par else ''
        kids = [x for x, xp in g.items() if any(b == t for b in xp.get(I(SKOS + 'broader'), []) + xp.get(I(RDFS + 'subClassOf'), []))]
        sibs = [x for x, xp in g.items() if par and x != t and any(b == par[0] for b in xp.get(I(SKOS + 'broader'), []) + xp.get(I(RDFS + 'subClassOf'), []))]
        it = {'id': t[1], 'label': lab(t), 'kind': key.split('/')[0] + ' term', 'scheme': ing.pref_out(g[o['header']]) or key}
        if par: it.update(broader=lab(par[0]), broader_definition=pdef)
        alts = [a[1] for a in ps.get(I(SKOS + 'altLabel'), []) if a[0] == 'L']
        if alts: it['alternative_labels'] = alts
        if kids: it['narrower'] = [lab(k) for k in kids[:12]]
        if sibs: it['siblings'] = [lab(k) for k in sibs[:12]]
        items.append(it); where[t[1]] = (key, t)
    if not items:
        return 0
    defs, model, err = generate_definitions(items, ing.cfg, log)
    if err:
        log('definitions: ' + err)
        for key in {k for k, _ in where.values()}:
            ing.note(key, 'warn', 'definitions were not generated: ' + err)
    for iri, text in defs.items():
        key, t = where.get(iri, (None, None))
        if not key: continue
        g = ing.outputs[key]['graph']
        ing.add(g, t, I(SKOS + 'definition'), L(text, 'en'))
        ing.add(g, t, I(SKOS + 'editorialNote'), L(f'Definition written by {model} during ingestion on {ing.day:%Y-%m-%d}; review before the term moves to Candidate.', 'en'))
        ing.note(key, 'generated', f'{short_iri(iri)}: definition written ("{text}")')
    return len(defs)


# ─────────────────────────────────────────────────────────────────────────────
# Review decisions (feedback). Conformance Review records how a person disposed of each finding in
# feedback/dispositions.jsonl (one JSON object per line, append-only). Ingestion learns from them:
#   * fixes are replayed: a correction made in review (label, definition, description, vocabulary link,
#     formalized by) is applied again when the same term is ingested again with the value the reviewer replaced,
#     so re-ingesting a source never brings an error back;
#   * findings accepted as exceptions, or marked not an issue, are reported as information, not errors;
#   * the definitions reviewers wrote or corrected are given to Claude as examples when it writes new ones.
FEEDBACK_FILE = pathlib.Path(__file__).with_name('feedback') / 'dispositions.jsonl'
# Conformance Review rule ids → the start of the rule names check() reports
RULE_NAMES = {'base-url': 'Base URL', 'uri-pattern': 'URI pattern', 'name-case': 'Identifier case', 'acronym-id': 'No acronyms in identifiers',
              'acronym-label': 'No acronyms in preferred labels', 'org-content': 'No other organization', 'vocab-term': 'Taxonomy term in a vocabulary',
              'primary-term': 'Taxonomy term in a vocabulary', 'skos-taxonomy': 'Taxonomies stay in SKOS', 'header-fields': 'Asset header fields',
              'valid-date': 'Valid dates', 'label': 'Label present', 'sentence-case': 'Sentence-case labels', 'definition': 'Definition present',
              'genus': 'Genus plus differentia', 'parent': 'Named parent class', 'defined-by': 'rdfs:isDefinedBy', 'in-scheme': 'Concept in scheme',
              'versioned-term': 'No version in term IRIs', 'version-format': 'Semantic version', 'one-scheme': 'One scheme'}


def load_feedback(path=None):
    p = pathlib.Path(path) if path else FEEDBACK_FILE
    out = []
    try:
        for line in p.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line:
                try: out.append(json.loads(line))
                except ValueError: pass
    except OSError:
        pass
    return out


def _norm_label(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]+', ' ', str(s or '').lower())).strip()


def exemptions(records=None):
    """(rule id, term IRI) → the latest record that accepted the finding or marked it not an issue."""
    latest = {}
    for r in records if records is not None else load_feedback():
        for f in (r.get('findings') or []):
            k = (f.get('rule'), (r.get('term') or {}).get('iri'))
            if k[0] and k[1]: latest[k] = r
    return {k: r for k, r in latest.items() if r.get('disposition') in ('accept', 'not-an-issue')}


def apply_exemptions(res, ex):
    """Downgrade findings a reviewer accepted to information, saying why. res: {rule name: [(sev, iri, msg)]}."""
    n = 0
    if not ex: return 0
    by = collections.defaultdict(dict)
    for (rid, iri), r in ex.items():
        name = RULE_NAMES.get(rid)
        if name: by[iri][name] = r
    for rule, items in res.items():
        for i, (sev, iri, msg) in enumerate(items):
            hit = next((r for name, r in by.get(iri, {}).items() if rule.startswith(name)), None)
            if hit and sev in ('error', 'warn'):
                why = (hit.get('rationale') or '').strip()
                items[i] = ('info', iri, f'{msg} — {"accepted" if hit["disposition"] == "accept" else "not an issue"} in Conformance Review'
                                       f'{" by " + hit["by"] if hit.get("by") else ""} on {str(hit.get("at", ""))[:10]}{": " + why if why else ""}')
                n += 1
    return n


def apply_feedback(ing, log=print):
    """Replay the fixes reviewers made, on this run's outputs (before the headers are finished and files written)."""
    recs = [r for r in load_feedback() if r.get('disposition') == 'fix' and r.get('actions')]
    if not recs:
        return 0
    FB = ing.CORE + 'formalizedBy'
    subj_ps = [ing.HAS_PRIMARY, DCT + 'subject']
    where = {}                                   # term IRI → output key
    by_label = collections.defaultdict(list)     # (kind, normalized label) → (key, term)
    for key, o in ing.outputs.items():
        for s, ps in o['graph'].items():
            if s[0] != 'I': continue
            where[s[1]] = key
            lab = next((l[1] for l in ps.get(I(SKOS + 'prefLabel'), []) + ps.get(I(RDFS + 'label'), []) if l[0] == 'L'), None)
            if lab: by_label[(key.split('/')[0], _norm_label(lab))].append((key, s))
    lits = lambda ps, p: [x for x in ps.get(I(p), []) if x[0] == 'L']
    n = 0
    for r in recs:                               # oldest first: later decisions win
        t = (r.get('term') or {})
        targets = [(where[t['iri']], I(t['iri']))] if t.get('iri') in where else []
        for a in r['actions']:
            ty = a.get('type')
            if not targets and ty in ('formalize', 'link') and t.get('label'):
                # the same concept under another identifier (e.g. a source re-ingested into another domain)
                targets = by_label.get(('taxonomy', _norm_label(t['label'])), [])[:1]
            for key, s in targets:
                g = ing.outputs[key]['graph']; ps = g.get(s)
                if ps is None: continue
                did = None
                if ty == 'label':
                    cur = [x[1] for x in lits(ps, SKOS + 'prefLabel') + lits(ps, RDFS + 'label')]
                    if a.get('old') and a.get('new') and a['old'] in cur:
                        for p in (SKOS + 'prefLabel', RDFS + 'label'):
                            if ps.get(I(p)): ps[I(p)] = [x for x in ps[I(p)] if not (x[0] == 'L' and x[1] == a['old'])] + [L(a['new'], 'en')]
                        if a.get('keepOld'): ing.add(g, s, I(SKOS + 'altLabel'), L(a['old'], 'en'))
                        did = f'label "{a["old"]}" → "{a["new"]}"'
                elif ty in ('definition', 'description'):
                    p = SKOS + 'definition' if ty == 'definition' else DCT + 'description'
                    cur = [x[1] for x in lits(ps, p)]
                    if a.get('new') and a['new'] not in cur and (not cur or (a.get('old') or '') in cur):
                        ps[I(p)] = [x for x in ps.get(I(p), []) if x[0] != 'L'] + [L(a['new'], 'en')]
                        if ps.get(I(SKOS + 'editorialNote')):
                            ps[I(SKOS + 'editorialNote')] = [x for x in ps[I(SKOS + 'editorialNote')] if not (x[0] == 'L' and 'Definition written' in x[1])]
                        did = f'{ty} as approved in review'
                elif ty == 'formalize' and a.get('target'):
                    if I(a['target']) not in ps.get(I(FB), []):
                        ps[I(FB)] = [I(a['target'])]; did = f'formalized by {short_iri(a["target"])}'
                elif ty == 'link' and a.get('target'):
                    if not ps.get(I(ing.HAS_PRIMARY)):
                        for p in subj_ps: ps[I(p)] = [I(a['target'])]
                        did = f'linked to vocabulary term {short_iri(a["target"])}'
                if did:
                    n += 1
                    ing.note(key, 'learned', f'{short_iri(s[1])}: {did} (review decision {str(r.get("at", ""))[:10]}{", " + r["by"] if r.get("by") else ""})')
    if n: log(f'feedback: {n} review decisions applied again')
    return n


def definition_examples(limit=12):
    """Definitions reviewers wrote, approved or corrected — newest first — as examples for the definition writer."""
    out, seen = [], set()
    for r in reversed(load_feedback()):
        if r.get('disposition') != 'fix': continue
        for a in r.get('actions') or []:
            if a.get('type') != 'definition' or not a.get('new'): continue
            t = r.get('term') or {}
            if t.get('iri') in seen: continue
            seen.add(t.get('iri'))
            ex = {'term': t.get('label'), 'approved_definition': a['new']}
            ctx = t.get('context') or {}
            if ctx.get('broader'): ex['broader'] = ctx['broader']
            if a.get('generatedDraft') and a['generatedDraft'] != a['new']: ex['rejected_draft'] = a['generatedDraft']
            if r.get('rationale'): ex['reviewer_note'] = r['rationale']
            out.append(ex)
        if len(out) >= limit: break
    # corrections first: they teach the most
    return sorted(out, key=lambda e: 'rejected_draft' not in e)


def run(paths, dest, cfg, ttl_dir='ttl', trig_dir='trig', recursive=False, timestamp=None, overrides=None, log=print):
    """Ingest the given files/folders into dest/ttl_dir and dest/trig_dir. Returns a summary dict."""
    cfg = json.loads(json.dumps(cfg))
    for k, v in (overrides or {}).items():
        if v not in (None, ''): cfg[k] = v
    if timestamp:
        now = datetime.datetime.fromisoformat(re.sub(r'Z$', '+00:00', timestamp.strip()))  # 'Z' needs Python 3.11+
        if now.tzinfo is None: now = now.astimezone()
        local_day = now.date()
    else:
        now = datetime.datetime.now(datetime.timezone.utc); local_day = now.astimezone().date()
    now = now.astimezone(datetime.timezone.utc).replace(microsecond=0)
    dest = pathlib.Path(dest).expanduser()
    ing = Ingest(cfg, now); ing.day = local_day
    skipped = []
    read = []
    for f in collect(paths, recursive):
        try:
            src = ing.inspect(f)
            read.append(src)
            log(f'read  {f.name}: {src["format"]}, {src["kind"]}/{src["domain"]}, {src["terms"]} terms, {src["triples"]} triples')
        except IngestError as e:
            skipped.append(dict(name=f.name, path=str(f), error=str(e)))
            log(f'skip  {f.name}: {e}')
    align_domains(read, known_domains(dest, ttl_dir), log)
    kept, dropped = pick_largest(read, cfg)
    for x, w in dropped:
        skipped.append(dict(name=x['name'], path=x['path'], error=dup_reason(x, w, cfg), duplicate=True))
        log(f'skip  {x["name"]}: {dup_reason(x, w, cfg)}')
    ing.sources = kept
    if not ing.sources:
        return dict(ok=False, error='No file could be ingested.', skipped=skipped)
    for key, notes in cfg.get('reviewNotes', {}).items():
        if any(s['key'] == key for s in ing.sources):
            for n in notes: ing.note(key, 'warn', n)
    ing.extra_vocab = vocab_index(dest / ttl_dir)        # vocabularies already in the destination
    ing.build_crosswalk(); ing.transform()
    learn = cfg.get('learnFromReview', True) not in (False, 'false', '0', 0)
    if learn: apply_feedback(ing, log)                   # replay the fixes made in Conformance Review
    if cfg.get('generateDefinitions') in (True, 'true', '1', 1):
        define_missing(ing, log)
    ing.finish_headers()
    keep_corrected(dest, ttl_dir, trig_dir, [f'{k.replace("/", "-")}-{ing.version}' for k in ing.outputs], f'{ing.now:%Y-%m-%dT%H%M%SZ}', log)
    files = ing.write(dest, ttl_dir, trig_dir)

    checks, outputs = {}, []
    vocab_all = set(vocab_index(dest / ttl_dir))          # this run's vocabularies (just written) and earlier ones
    exempt = exemptions() if learn else {}                # findings reviewers accepted, or marked not an issue
    for key, f in files.items():
        triples, _ = parse_turtle(f.read_text(encoding='utf-8'))   # re-read: proves the output is valid Turtle
        checks[key] = check(triples, ing.base, ing.policy, vocab_all)
        res = checks[key][1]
        if apply_exemptions(res, exempt): ing.note(key, 'learned', 'findings accepted in Conformance Review are reported as information')
        cnt = lambda sev: sum(1 for v in res.values() for x in v if x[0] == sev)
        o = ing.outputs[key]
        outputs.append(dict(key=key, kind=key.split('/')[0], iri=o['header'][1], title=ing.pref_out(o['graph'][o['header']]) or key,
                            terms=len(o['subjects']), triples=len(triples), ttl=str(f), trig=str(ing.trig_files[key]),
                            ttl_name=f.name, trig_name=ing.trig_files[key].name,
                            sources=[s['name'] for s in o['sources']],
                            errors=cnt('error'), warnings=cnt('warn'), info=cnt('info'),
                            rules=[dict(rule=r, items=[dict(sev=a, iri=b, msg=c) for a, b, c in v]) for r, v in res.items()],
                            notes=[dict(level=l, text=t) for l, t in ing.findings.get(key, [])],
                            removed={short(p): n for p, n in ing.removed.get(key, {}).items()}))
        log(f'wrote {f.name} + {ing.trig_files[key].name}: {len(o["subjects"])} terms, {len(triples)} triples, {cnt("error")} conformance errors')

    ttl, trig, rid, stamp = change_record(ing, outputs, skipped)
    cr_ttl = dest / ttl_dir / f'change-record-{stamp}.ttl'
    cr_trig = dest / trig_dir / f'change-record-{stamp}.trig'
    cr_ttl.write_text(ttl, encoding='utf-8'); cr_trig.write_text(trig, encoding='utf-8')
    parse_turtle(ttl)

    with open(dest / 'crosswalk.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['kind', 'legacy_iri', 'new_iri', 'new_label'])
        for old, new in sorted(ing.cross.items(), key=lambda kv: (ing.cross_kind.get(kv[0], 'z'), kv[1])):
            if old in ing.cross_kind: w.writerow([ing.cross_kind[old], old, new, ing.labels.get(new, '')])
    md = report_md(ing, outputs, skipped, files, checks, (cr_ttl.relative_to(dest).as_posix(), cr_trig.relative_to(dest).as_posix()))
    rep = dest / f'ingestion-report-{stamp}.md'
    rep.write_text(md, encoding='utf-8')
    log(f'wrote {cr_ttl.name}, {cr_trig.name}, crosswalk.csv, {rep.name}')
    archive_superseded(dest, ttl_dir, trig_dir, stamp, log)
    return dict(ok=True, run_at=ing.now_lit[1], dest=str(dest), ttl_dir=str(dest / ttl_dir), trig_dir=str(dest / trig_dir),
                author=ing.author, version=ing.version, status=cfg['lifecycleStatus'], base=ing.base,
                outputs=outputs, skipped=skipped,
                sources=[dict(name=s['name'], format=s['format'], header=s['header'][1], new_iri=s['new_iri']) for s in ing.sources],
                change_record=dict(id=rid, graph=f'{ing.base}graph/change-log', ttl=str(cr_ttl), trig=str(cr_trig), text=ttl),
                report=dict(path=str(rep), markdown=md), crosswalk=str(dest / 'crosswalk.csv'))

# ─────────────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+', help='RDF files (.ttl .nt .rdf .rdfs .owl .xml) or folders that hold them')
    ap.add_argument('-o', '--out', default='output', help='destination folder (default: output)')
    ap.add_argument('--ttl-dir', default='ttl', help='subfolder for Turtle files (default: ttl)')
    ap.add_argument('--trig-dir', default='trig', help='subfolder for TriG files (default: trig)')
    ap.add_argument('-r', '--recursive', action='store_true', help='also read subfolders of input folders')
    ap.add_argument('-c', '--config', default=None, help='config file (default: ke-ingest.config.json next to this script)')
    ap.add_argument('--define', action='store_true', help='write missing definitions with Claude (needs ANTHROPIC_API_KEY or ~/.ke-workbench.env)')
    ap.add_argument('--timestamp', help='ISO 8601 time to stamp as dct:modified (default: now)')
    a = ap.parse_args(argv)
    cfg, _ = load_config(a.config)
    res = run(a.inputs, a.out, cfg, a.ttl_dir, a.trig_dir, a.recursive, a.timestamp,
              {'generateDefinitions': True} if a.define else None)
    if not res['ok']:
        raise SystemExit(res['error'])

if __name__ == '__main__':
    main()
