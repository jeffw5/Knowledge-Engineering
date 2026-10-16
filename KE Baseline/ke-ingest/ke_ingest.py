#!/usr/bin/env python3
"""
KE Ingest — bring legacy knowledge artifacts (vocabularies, taxonomies, ontologies)
into line with the Part III standards of "Semantic Governance: Services,
Architecture & Integration" v1.8 (Draft).

What it does, per run:
  1. Reads every Turtle file given and works out what each one is (SKOS vocabulary,
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

No third-party packages: runs with the Python 3.8+ standard library.

Usage:
  python3 ke_ingest.py input/*.ttl -o output
  python3 ke_ingest.py input/*.ttl -o output --config ke-ingest.config.json --timestamp 2026-10-15T20:00:00-05:00
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
# Turtle writer
# ─────────────────────────────────────────────────────────────────────────────
PRED_ORDER = [RDF + 'type', RDFS + 'label', SKOS + 'prefLabel', DCT + 'title', SKOS + 'altLabel',
              SKOS + 'definition', DCT + 'description', SKOS + 'scopeNote', SKOS + 'example', SKOS + 'notation',
              RDFS + 'subClassOf', OWL + 'equivalentClass', RDFS + 'subPropertyOf', RDFS + 'domain', RDFS + 'range',
              SKOS + 'inScheme', SKOS + 'topConceptOf', SKOS + 'broader', SKOS + 'narrower', SKOS + 'hasTopConcept',
              RDFS + 'isDefinedBy', DC + 'subject', SH + 'targetClass', SH + 'path', SH + 'class', SH + 'property',
              OWL + 'imports', VANN + 'preferredNamespaceUri', DCT + 'language',
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
        # blank node: inline as [ … ]
        body = self.po_block(t, graph, depth + 1)
        pad = '    ' * depth + '  '
        return '[\n' + body + '\n' + pad + ']'

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

# ─────────────────────────────────────────────────────────────────────────────
# Ingestion
# ─────────────────────────────────────────────────────────────────────────────
class Ingest:
    def __init__(self, cfg, now):
        self.cfg = cfg
        self.base = cfg['baseUrl'].rstrip('/') + '/'
        self.CORE = self.base + 'ontology/core/'
        self.HAS_STATUS = self.CORE + 'hasLifecycleStatus'
        self.author = cfg['author']
        self.version = cfg['initialVersion']
        self.now = now
        self.day = now.date()
        self.now_lit = L(now.strftime('%Y-%m-%dT%H:%M:%SZ'), None, XSD + 'dateTime')
        self.src_rx = [(re.compile(r['pattern']), r) for r in cfg['sourceNamespaces']]
        self.keep = set(cfg.get('keepCase', []))
        self.cross = {}            # old IRI → new IRI
        self.cross_kind = {}       # old IRI → kind of thing (for the crosswalk file)
        self.labels = {}           # new IRI → sentence-case label
        self.findings = collections.defaultdict(list)   # asset key → [(level, text)]
        self.removed = collections.defaultdict(collections.Counter)
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
    def load(self, path):
        text = pathlib.Path(path).read_text(encoding='utf-8')
        triples, _ = parse_turtle(text)
        g = collections.OrderedDict()
        for s, p, o in triples:
            g.setdefault(s, collections.OrderedDict()).setdefault(p[1], []).append(o)
        headers = [s for s, ps in g.items() if s[0] == 'I' and
                   any(o in (I(OWL + 'Ontology'), I(SKOS + 'ConceptScheme')) for o in ps.get(RDF + 'type', []))]
        if len(headers) != 1:
            raise SystemExit(f'{path}: expected one owl:Ontology or skos:ConceptScheme header, found {len(headers)}')
        h = headers[0]
        c = self.classify(h[1])
        if not c: raise SystemExit(f'{path}: header {h[1]} does not match any sourceNamespaces pattern in the config')
        kind, domain, _ = c
        src = dict(path=str(path), graph=g, header=h, kind=kind, domain=domain, triples=len(triples),
                   key=self.key(kind, domain), scheme=I(SKOS + 'ConceptScheme') in g[h].get(RDF + 'type', []))
        self.sources.append(src)
        return src

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
                    lab = self.pref(ps)
                    new = new_asset + slug(lab)
                    self.labels[new] = sentence_case(lab, self.keep)
                    kindname = 'vocabulary term'
                elif I(OWL + 'Class') in types or I(RDFS + 'Class') in types:
                    c = self.classify(s[1])
                    local = c[2] if c else s[1].rstrip('/').split('/')[-1].split('#')[-1]
                    local, newlab = self.renamed(kind, domain, local)
                    local = upper_camel(local) if not re.fullmatch(r'[A-Z][A-Za-z0-9]*', local) else local
                    owner = c[:2] if c else (kind, domain)
                    new = self.asset_iri(*owner) + local
                    self.labels[new] = newlab or sentence_case(self.pref(ps) or split_camel(local), self.keep)
                    kindname = 'class'
                else:
                    continue
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
                        new = f'{self.base}shapes/{src["domain"]}/{new_tgt.rstrip("/").split("/")[-1]}Shape'
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
        self.add(g, s, I(DCT + 'creator'), L(self.author))
        self.add(g, s, I(DCT + 'created'), created or self.now_lit)
        self.add(g, s, I(DCT + 'modified'), self.now_lit)

    @staticmethod
    def earliest(ps):
        ds = [o for o in ps.get(DCT + 'created', []) if o[0] == 'L']
        if not ds: return None
        o = min(ds, key=lambda x: x[1])
        return L(o[1], None, XSD + 'dateTime')

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
            if not src['scheme']: continue
            for s, ps in src['graph'].items():
                if s[0] == 'I' and I(SKOS + 'Concept') in ps.get(RDF + 'type', []):
                    new = self.cross[s[1]]
                    vocab_terms[new] = ps
                    vocab_by_label[(self.asset_iri(src['kind'], src['domain']), self.pref(ps).lower())] = new

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
                types = ps.get(RDF + 'type', [])
                if not types:
                    self.note(key, 'removed', f'Stub subject {s[1]} (no type; only {", ".join(sorted(short(p) for p in ps))})')
                    for p in ps: self.removed[key][p] += len(ps[p])
                    continue
                if I(SH + 'NodeShape') in types:
                    self.shape(src, s, ps, shapes_key)
                    continue
                new = I(self.cross.get(s[1], s[1]))
                is_concept = I(SKOS + 'Concept') in types
                label = self.labels.get(new[1]) or sentence_case(self.pref(ps), self.keep)
                orig_label = self.pref(ps)

                for p, objs in ps.items():
                    if p in self.REBUILT: continue
                    if p not in self.KEEP_TERM:
                        self.removed[key][p] += len(objs); continue
                    for ob in objs:
                        if ob[0] == 'B': self.copy_bnode(g, dst, ob, key)
                        if p == DC + 'subject':
                            ob = I(self.subject_link(key, new[1], ob[1], label, vocab_terms, vocab_by_label))
                        elif p == SKOS + 'altLabel' and ob[0] == 'L':
                            ob = L(ob[1], ob[2] or 'en')
                        else:
                            ob = self.map_term(ob)
                        self.add(dst, new, I(p), ob)

                # labels
                self.add(dst, new, I(SKOS + 'prefLabel'), L(label, 'en'))
                if not is_concept: self.add(dst, new, I(RDFS + 'label'), L(label, 'en'))
                if orig_label and orig_label.lower() != label.lower():
                    self.add(dst, new, I(SKOS + 'altLabel'), L(sentence_case(orig_label, self.keep), 'en'))
                    self.note(key, 'renamed', f'{short_iri(s[1])} → {short_iri(new[1])} ("{orig_label}" → "{label}")')
                elif orig_label and orig_label != label:
                    self.note(key, 'label', f'"{orig_label}" → "{label}"')

                # definition: own → linked vocabulary term → config
                defs = [x for x in ps.get(SKOS + 'definition', []) + ps.get(RDFS + 'comment', []) if x[0] == 'L']
                linked = [x for x in dst[new].get(I(DC + 'subject'), [])] if new in dst else []
                if defs:
                    d = defs[0]; self.add(dst, new, I(SKOS + 'definition'), L(clean(d[1]), d[2] or 'en'))
                else:
                    filled = False
                    for lk in linked:
                        vps = vocab_terms.get(lk[1])
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

    def key_of(self, o):
        for k, v in self.outputs.items():
            if v is o: return k

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
            predicted = vasset + slug(label)
            self.note(key, 'unresolved', f'{short_iri(cls)}: vocabulary {c[1]} was not in this run; dc:subject set to the expected IRI {short_iri(predicted)}')
            return predicted
        return self.map_iri(old)

    def shape(self, src, s, ps, shapes_key):
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
            d = [x for x in hp.get(DCT + 'description', []) if x[0] == 'L']
            if d: self.add(dst, asset, I(DCT + 'description'), L(clean(d[0][1]), 'en'))
            else: self.note(key, 'warn', 'No description configured or found')
        self.add(dst, asset, I(DCT + 'language'), L('en'))
        self.add(dst, asset, I(VANN + 'preferredNamespaceUri'), L(asset[1], None, XSD + 'anyURI'))
        if not src['scheme']:
            for imp in hp.get(OWL + 'imports', []):
                self.add(dst, asset, I(OWL + 'imports'), I(self.map_iri(imp[1])))
            self.add(dst, asset, I(OWL + 'versionIRI'), I(asset[1] + self.version + '/'))
        if meta.get('editorialNote'): self.add(dst, asset, I(SKOS + 'editorialNote'), L(meta['editorialNote'], 'en'))
        self.add(dst, asset, I(SKOS + 'changeNote'), L(
            f'{self.version} ({self.day:%Y-%m-%d}): ingested into the {self.base} namespace; IRIs, labels and metadata '
            f'brought into line with {self.cfg["standardsRef"]}.', 'en'))
        self.governance(dst, asset, self.earliest(hp))
        self.add(dst, asset, I(DCT + 'contributor'), L(self.author))
        for p, objs in hp.items():
            if p not in self.REBUILT and p not in (RDF + 'type', OWL + 'imports', DCT + 'title', DCT + 'description', SKOS + 'altLabel'):
                self.removed[key][p] += len(objs)

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
                self.add(g, asset, I(VANN + 'preferredNamespaceUri'), L(asset[1], None, XSD + 'anyURI'))
                self.add(g, asset, I(OWL + 'versionIRI'), I(asset[1] + self.version + '/'))
                self.add(g, asset, I(SKOS + 'changeNote'), L(
                    f'{self.version} ({self.day:%Y-%m-%d}): shapes moved out of the {domain} ontology into their own shapes graph '
                    f'under {self.base}shapes/, as {self.cfg["standardsRef"]} requires.', 'en'))
                self.governance(g, asset, min((self.earliest(src['graph'][src['header']]) for src in o['sources']),
                                              key=lambda x: x[1] if x else '9', default=None))
                self.add(g, asset, I(DCT + 'contributor'), L(self.author))
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
              'vann': VANN, 'core': self.CORE, 'sh': SH}
        kind, domain = key.split('/', 1)
        px[{'vocabulary': 'voc', 'taxonomy': 'tax', 'ontology': 'ont', 'shapes': 'shp'}[kind]] = self.asset_iri(kind, domain)
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
        parent_p = I(SKOS + 'broader') if o['kind'] == 'vocabulary' else I(RDFS + 'subClassOf')
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

    def write(self, outdir):
        outdir = pathlib.Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
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
            (outdir / name).write_text(text, encoding='utf-8')
            files[key] = outdir / name
            # TriG copy: the named graph is the asset IRI, which is how the KE Workbench finds an asset
            trig = w.write_trig(g2, self.order_subjects(o), head.replace('\n# Standards', f'\n# Named graph: {o["header"][1]}\n# Standards'), o['header'][1])
            (outdir / name.replace('.ttl', '.trig')).write_text(trig, encoding='utf-8')
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
ACRONYM = re.compile(r'\b(?![IVX]+\b)[A-Z]{2,}s?\b')
CAMEL_ACR = re.compile(r'[A-Z]{2,}(?=[A-Z][a-z]|$|[0-9_-])|[A-Z]{3,}')

def check(triples, base):
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
        if not kind: continue
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
        if kind == 'class' and not re.fullmatch(r'[A-Z][A-Za-z0-9]*', local): r('Identifier case (§3.2)', 'warn', iri, 'class not UpperCamelCase')
        if kind == 'concept' and segs and segs[0] == 'vocabulary' and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', local): r('Identifier case (§3.2)', 'warn', iri, 'vocabulary term not lower-case hyphenated')
        if kind == 'shape' and not re.fullmatch(r'[A-Z][A-Za-z0-9]*Shape', local): r('Identifier case (§3.2)', 'warn', iri, 'shape not {Class}Shape')
        if kind in ('class', 'shape') and CAMEL_ACR.search(local): r('No acronyms in identifiers (§3.2)', 'error', iri, local)
        for l in prefs:
            if ACRONYM.search(l[1]): r('No acronyms in preferred labels (§3.2)', 'error', iri, l[1])
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
            if kind == 'ontology' and not e.get(OWL + 'versionIRI'): r('Semantic version on releases (§3.3)', 'warn', iri, 'no owl:versionIRI')
            if kind == 'scheme' and not e.get(SKOS + 'hasTopConcept'): r('One scheme, top concepts flagged (E.3)', 'error', iri, 'no top concepts')
    return counted, res

# ─────────────────────────────────────────────────────────────────────────────
# Report, crosswalk, change record
# ─────────────────────────────────────────────────────────────────────────────
def write_extras(ing, files, outdir, checks, src_triples):
    outdir = pathlib.Path(outdir)
    # crosswalk
    with open(outdir / 'crosswalk.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['kind', 'legacy_iri', 'new_iri', 'new_label'])
        for old, new in sorted(ing.cross.items(), key=lambda kv: (ing.cross_kind.get(kv[0], 'z'), kv[1])):
            if old not in ing.cross_kind: continue
            w.writerow([ing.cross_kind[old], old, new, ing.labels.get(new, '')])
    # change record (PROV-O), for the append-only change-log graph
    rid = f'{ing.base}resource/change-log/ChangeRecord/{ing.now:%Y-%m-%dT%H%M%SZ}-ingestion'
    lines = [f'# Change record for {ing.base}graph/change-log (append-only, §3.3)',
             f'@prefix prov: <{PROV}> .', f'@prefix dct: <{DCT}> .', f'@prefix rdfs: <{RDFS}> .', f'@prefix xsd: <{XSD}> .', '',
             f'<{rid}> a prov:Activity ;',
             f'  rdfs:label "Ingestion of legacy knowledge artifacts"@en ;',
             f'  dct:description "Migrated {len(ing.sources)} legacy files to {ing.base} and the Part III naming and metadata standards; '
             f'every asset starts at version {ing.version}, {ing.cfg["lifecycleStatus"]}."@en ;',
             f'  dct:creator "{ing.author}" ;',
             f'  prov:startedAtTime "{ing.now_lit[1]}"^^xsd:dateTime ;']
    used = sorted({s['header'][1] for s in ing.sources})
    lines.append('  prov:used ' + ' ,\n    '.join(f'<{u}>' for u in used) + ' ;')
    gen = sorted(o['header'][1] for o in ing.outputs.values())
    lines.append('  prov:generated ' + ' ,\n    '.join(f'<{u}>' for u in gen) + ' .')
    (outdir / f'change-record-{ing.day:%Y-%m-%d}.ttl').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    pre = [l for l in lines if l.startswith('@prefix') or l.startswith('#')]
    rest = [l for l in lines if not (l.startswith('@prefix') or l.startswith('#'))]
    (outdir / f'change-record-{ing.day:%Y-%m-%d}.trig').write_text(
        '\n'.join(pre) + f'\n\n<{ing.base}graph/change-log> {{\n' + '\n'.join(('  ' + l) if l else l for l in rest).rstrip() + '\n}\n', encoding='utf-8')

    # report
    R = []
    R.append(f'# Ingestion report\n\nRun {ing.now_lit[1]} · base URL `{ing.base}` · author {ing.author} · '
             f'version {ing.version} ({ing.cfg["lifecycleStatus"]})\n\nStandards: {ing.cfg["standardsRef"]}\n')
    R.append('## Outputs\n\n| Output | Asset IRI | Terms | Triples | From |\n|---|---|---|---|---|')
    for key, f in files.items():
        o = ing.outputs[key]
        R.append(f'| `{f.name}` | `{o["header"][1]}` | {len(o["subjects"])} | {src_triples[key]} | '
                 + ', '.join(pathlib.Path(s["path"]).name for s in o['sources']) + ' |')
    R.append('\nAlso written: `crosswalk.csv` (every legacy IRI and its new IRI) and the PROV-O change record.\n')
    R.append('## Conformance after ingestion\n')
    for key, (counted, res) in checks.items():
        errs = sum(1 for v in res.values() for x in v if x[0] == 'error')
        warns = sum(1 for v in res.values() for x in v if x[0] == 'warn')
        infos = sum(1 for v in res.values() for x in v if x[0] == 'info')
        R.append(f'**{files[key].name}** — {errs} errors, {warns} warnings, {infos} info')
        for rule, items in res.items():
            R.append(f'- {rule}: ' + '; '.join(f'`{short_iri(i)}` {m}' for _, i, m in items[:6]) + (f' (+{len(items) - 6} more)' if len(items) > 6 else ''))
        R.append('')
    R.append('## What changed, by asset\n')
    R.append(f'On every asset and term the governance fields were rebuilt, not copied: `dct:creator` and (on asset headers) '
             f'`dct:contributor` are {ing.author} only; `dct:created` keeps the source date (or the run time when the source had none); '
             f'`dct:modified` is {ing.now_lit[1]}; `owl:versionInfo` is {ing.version}; lifecycle status is {ing.cfg["lifecycleStatus"]}. '
             'Labels and definitions were re-tagged `@en`. The source values of those fields are not counted below.\n')
    order = ['fixed', 'renamed', 'generated', 'filled', 'unresolved', 'moved', 'removed', 'label', 'warn', 'error']
    titles = {'fixed': 'Corrected', 'renamed': 'Renamed to meet naming rules', 'generated': 'Definitions written',
              'filled': 'Filled from existing metadata', 'unresolved': 'Unresolved links', 'moved': 'Moved',
              'removed': 'Removed subjects', 'label': 'Labels put in sentence case', 'warn': 'Review', 'error': 'Errors'}
    for key in list(ing.outputs):
        R.append(f'### {key}\n')
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
    (outdir / 'ingestion-report.md').write_text('\n'.join(R), encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+', help='legacy Turtle files')
    ap.add_argument('-o', '--out', default='output', help='output folder (default: output)')
    ap.add_argument('-c', '--config', default=str(pathlib.Path(__file__).with_name('ke-ingest.config.json')))
    ap.add_argument('--timestamp', help='ISO 8601 time to stamp as dct:modified (default: now)')
    a = ap.parse_args(argv)
    cfg = json.loads(pathlib.Path(a.config).read_text(encoding='utf-8'))
    now = (datetime.datetime.fromisoformat(a.timestamp) if a.timestamp else datetime.datetime.now(datetime.timezone.utc))
    if now.tzinfo is None: now = now.astimezone()
    local_day = (now if a.timestamp else now.astimezone()).date()
    now = now.astimezone(datetime.timezone.utc).replace(microsecond=0)

    ing = Ingest(cfg, now)
    ing.day = local_day
    for p in a.inputs:
        src = ing.load(p)
        print(f'read  {pathlib.Path(p).name}: {src["kind"]}/{src["domain"]}, {src["triples"]} triples')
    for key, notes in cfg.get('reviewNotes', {}).items():
        for n in notes: ing.note(key, 'warn', n)
    ing.build_crosswalk()
    ing.transform()
    ing.finish_headers()
    files = ing.write(a.out)

    checks, counts = {}, {}
    for key, f in files.items():
        triples, _ = parse_turtle(f.read_text(encoding='utf-8'))   # re-read: proves the output is valid Turtle
        counts[key] = len(triples)
        checks[key] = check(triples, ing.base)
        errs = sum(1 for v in checks[key][1].values() for x in v if x[0] == 'error')
        print(f'wrote {f.name}: {len(ing.outputs[key]["subjects"])} terms, {len(triples)} triples, {errs} conformance errors')
    write_extras(ing, files, a.out, checks, counts)
    print(f'wrote crosswalk.csv, change-record-{ing.day:%Y-%m-%d}.ttl, ingestion-report.md')

if __name__ == '__main__':
    main()
