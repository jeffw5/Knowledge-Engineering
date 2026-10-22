#!/usr/bin/env python3
"""Build the operational areas' and domains' vocabularies, taxonomies, ontologies and shapes from their specs.

    python3 _build/build_domains.py                     # from the "KE Domains" folder
    python3 _build/build_domains.py --only sales        # rebuild one domain or area (and check it against the others)

Areas and domains (D26): each spec's DOMAIN names its level (area or domain), its operational area, its parent domain
(for an L2 or L3 domain) and its folder under KE Domains. Area assets live at …/<kind>/<area>/ and are titled
"<Area> Vocabulary"; domain assets at …/<kind>/domain-<L1>[.<L2>[.<L3>]]/, titled "Domain <L1>[.<L2>[.<L3>]] Vocabulary".

Reads   _build/spec_<domain>.py                       (the authored source of each domain)
        ../../KE Baseline/Baseline Core v1.0/ttl/      (the core: read only, never written)
        ../../KE Workbench/ingest/ke_ingest.py         (the Turtle parser, writer and Part III checks)
Writes  <domain>/ttl/{vocabulary,taxonomy,ontology,shapes}-domain-<domain>-<version>.ttl and the same as .trig
        review/  concept links, promotion candidates, homonyms and the build report

Rules enforced (review/design-decisions.md):
  D1  one folder per domain; classes, relations, concepts and imports refer only to the core, the domain's operational
      area, its parent domains, itself and the APQC reference registry (insulation, D27); vocabulary primitives may be
      cited from any domain or area (dcterms:subject, core:hasPrimaryTerm), never copied;
  D2  shared terms live in the container;
  D3  domain vocabularies hold primitives only, unique across the core and every domain (homonyms are declared);
  D4  every taxonomy concept is built from primitives (dcterms:subject, core:hasPrimaryTerm); top concepts are
      formalized by a core or domain class; skos:broadMatch links a concept to the core or container concept it
      specializes;
  D5  every domain class reaches BFO through a core class; every domain relation specializes a core relation;
  D6  domain ontologies import the versioned core ontology (and the versioned container), so a core change reaches a
      domain only when the domain is rebuilt against it.
"""
import argparse, collections, csv, datetime, importlib, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
AREA = HERE.parent          # the KE Domains folder
sys.path.insert(0, str(HERE))

ORDER = ['commercial_operations', 'sales', 'sales_partner_and_channel', 'marketing', 'pricing', 'customer_care',
         'business_operations', 'legal', 'hr_service_operations', 'technical_operations']
KIND_TITLE = {'vocabulary': 'Vocabulary', 'taxonomy': 'Taxonomy', 'ontology': 'Ontology', 'shapes': 'Shapes'}
VERSION = '0.1.0'
CORE_VERSION = '0.1.0'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--core', default=str(AREA.parent / 'KE Baseline' / 'Baseline Core v1.0' / 'ttl'))
    ap.add_argument('--ingest', default=str(AREA.parent / 'KE Workbench' / 'ingest'))
    ap.add_argument('--out', default=str(AREA))
    ap.add_argument('--only', default=None, help='domain key to write (all are still loaded and checked)')
    ap.add_argument('--timestamp', default=None)
    a = ap.parse_args(argv)
    sys.path.insert(0, a.ingest)
    global k
    import ke_ingest as k
    cfg, _ = k.load_config(str(pathlib.Path(a.ingest) / 'ke-ingest.config.json'))
    t = (datetime.datetime.fromisoformat(a.timestamp.replace('Z', '+00:00')) if a.timestamp
         else datetime.datetime.now(datetime.timezone.utc)).replace(microsecond=0)
    b = Build(cfg, pathlib.Path(a.core), pathlib.Path(a.out), t)
    b.run(only=a.only)
    return 1 if b.errors else 0


class Build:
    def __init__(self, cfg, core_dir, out, t):
        self.cfg, self.core_dir, self.out = cfg, core_dir, out
        self.base = cfg['baseUrl']
        self.CORE = self.base + 'ontology/core/'
        self.now = k.L(t.strftime('%Y-%m-%dT%H:%M:%SZ'), None, k.XSD + 'dateTime')
        self.today = k.L(t.strftime('%Y-%m-%d'), None, k.XSD + 'date')
        self.stamp = t.strftime('%Y-%m-%dT%H%M%SZ')
        self.author = k.L(cfg['author'])
        self.status = k.I(self.CORE + cfg['lifecycleStatus'])
        self.policy = k.Policy(cfg)
        self.errors, self.warnings, self.notes = [], [], []
        self.load_core()
        self.specs = [importlib.import_module('spec_' + n) for n in ORDER]
        self.ont_prefix = {'core': self.CORE, 'obo': 'http://purl.obolibrary.org/obo/'}
        self.by_key = {s.DOMAIN['key']: s for s in self.specs}
        for s in self.specs:
            self.ont_prefix[s.DOMAIN['prefix']] = self.base + f'ontology/{slug_of(s.DOMAIN)}/'
        self.slugs = {slug_of(s.DOMAIN) for s in self.specs} | {'apqc-pcf'}
        self.load_reference()

    def load_reference(self):
        """The APQC PCF reference registry (read only), if it has been built."""
        self.ref_tax = set()
        for f in sorted((self.out / 'Reference' / 'apqc-pcf' / 'ttl').glob('taxonomy-apqc-pcf-*.ttl')):
            for s_, p_, o in k.parse_turtle(f.read_text(encoding='utf-8'))[0]:
                if p_[1] == k.RDF + 'type' and o[1] == k.SKOS + 'Concept': self.ref_tax.add(s_[1])

    def lineage_of(self, d):
        """The slugs a domain may refer to for classes, relations, concepts and imports (D1, D27)."""
        out = {'core', 'apqc-pcf', slug_of(d), d['area']}
        p = d.get('parent')
        while p:
            out.add(slug_of(self.by_key[p].DOMAIN)); p = self.by_key[p].DOMAIN.get('parent')
        return out

    # ── the core (read only) ────────────────────────────────────────────────
    def load_core(self):
        self.core_vocab, self.core_labels, self.core_tax, self.core_classes, self.core_props = {}, collections.defaultdict(list), set(), set(), set()
        self.core_graph = collections.OrderedDict()
        for f in sorted(self.core_dir.glob('*.ttl')):
            # only the core assets from the baseline folder: anything else that lands there is not core (D1)
            if not re.match(r'(vocabulary|taxonomy|ontology|shapes)-core(-[a-z]+)?-\d', f.name): continue
            for s, p, o in k.parse_turtle(f.read_text(encoding='utf-8'))[0]:
                self.core_graph.setdefault(s, collections.OrderedDict()).setdefault(p[1], []).append(o)
        T = k.RDF + 'type'
        for s, ps in self.core_graph.items():
            if s[0] != 'I': continue
            types = {x[1] for x in ps.get(T, [])}
            if k.SKOS + 'Concept' in types:
                if '/vocabulary/' in s[1]:
                    lab = [x[1] for x in ps.get(k.SKOS + 'prefLabel', [])]
                    alts = [x[1] for x in ps.get(k.SKOS + 'altLabel', [])]
                    self.core_vocab[s[1]] = lab[0] if lab else ''
                    self.core_alts = getattr(self, 'core_alts', {}); self.core_alts[s[1]] = alts
                    for l in lab + alts: self.core_labels[norm(l)].append(s[1])
                elif '/taxonomy/' in s[1]:
                    self.core_tax.add(s[1])
            if s[1].startswith(self.CORE):
                if k.OWL + 'Class' in types: self.core_classes.add(s[1])
                if k.OWL + 'ObjectProperty' in types: self.core_props.add(s[1])

    # ── reference resolution ───────────────────────────────────────────────
    def voc(self, ref):
        return self.base + 'vocabulary/' + ref

    def cls(self, ref):
        if ref.startswith('dct:'): return k.DCT + ref[4:]
        pre, local = ref.split(':', 1)
        if pre not in self.ont_prefix: raise KeyError(f'unknown prefix in {ref}')
        return self.ont_prefix[pre] + local

    def ref_domain(self, iri):
        """'core', the slug of an area or domain, or None for IRIs outside the base."""
        m = re.match(re.escape(self.base) + r'(?:vocabulary|taxonomy|ontology|shapes|resource)/([a-z0-9.-]+)/', iri)
        if not m: return None
        seg = m.group(1)
        if re.match(r'core(-[a-z]+)?$', seg): return 'core'
        return seg if (seg in self.slugs or seg.startswith('domain-')) else None

    # ── build ──────────────────────────────────────────────────────────────
    def run(self, only=None):
        # index every domain vocabulary first, so references can be checked across domains
        self.dom_vocab, self.dom_labels, self.dom_tax, self.dom_classes, self.dom_props = {}, collections.defaultdict(list), set(), set(), set()
        for s in self.specs:
            key, sl = s.DOMAIN['key'], slug_of(s.DOMAIN)
            for v in s.VOCAB:
                iri = self.voc(f'{sl}/{v.id}')
                if iri in self.dom_vocab: self.err(key, f'duplicate vocabulary id {v.id}')
                self.dom_vocab[iri] = (key, v)
            for c in s.TAXONOMY: self.dom_tax.add(self.base + f'taxonomy/{sl}/{c.id}')
            for c in s.CLASSES: self.dom_classes.add(self.ont_prefix[s.DOMAIN['prefix']] + c.id)
            for p in s.PROPERTIES: self.dom_props.add(self.ont_prefix[s.DOMAIN['prefix']] + p.id)
        self.check_primitives()
        self.outputs = []
        self.links = []
        for s in self.specs:
            key = s.DOMAIN['key']
            files = self.build_domain(s, write=(only in (None, key)))
            self.outputs.append((s, files))
        self.check_lineage()
        self.reports(only)

    def err(self, dom, msg): self.errors.append(f'{dom}: {msg}')
    def warn(self, dom, msg): self.warnings.append(f'{dom}: {msg}')

    def check_primitives(self):
        """D3: a primitive's label is unique across the core and all domain vocabularies (declared homonyms excepted)."""
        seen = collections.defaultdict(list)
        for iri, (key, v) in self.dom_vocab.items():
            for l in [v.label] + v.alt:
                seen[norm(l)].append((iri, key, v))
        self.homonyms = []
        for iri, (key, v) in self.dom_vocab.items():
            for l in [v.label] + v.alt:
                n = norm(l)
                hits = [x for x in self.core_labels.get(n, [])]
                if hits:
                    declared = v.homonym and any(h.endswith('/' + v.homonym) for h in hits)
                    if declared:
                        self.homonyms.append((iri, l, hits[0], v.scope or ''))
                    elif l in v.alt:
                        self.warn(key, f'alternative label "{l}" of {v.id} is also a core label ({short(self, hits[0])})')
                    else:
                        self.err(key, f'primitive "{l}" ({v.id}) duplicates core term {short(self, hits[0])}; reuse it or declare a homonym')
                others = [x for x in seen[n] if x[0] != iri]
                if others:
                    self.err(key, f'primitive "{l}" ({v.id}) also in {", ".join(short(self, x[0]) for x in others)}')

    def gov(self, g, s):
        add(g, s, k.OWL + 'versionInfo', k.L(self.ver))
        add(g, s, self.CORE + 'hasLifecycleStatus', self.status)
        add(g, s, k.DCT + 'creator', self.author)
        add(g, s, k.DCT + 'created', self.today)
        add(g, s, k.DCT + 'modified', self.now)

    def header(self, g, iri, kind, s, title, description, sources=None, imports=None, requires=None):
        d = s.DOMAIN
        h = k.I(iri)
        add(g, h, k.RDF + 'type', k.I(k.OWL + 'Ontology' if kind in ('ontology', 'shapes') else k.SKOS + 'ConceptScheme'))
        add(g, h, k.RDFS + 'label', k.L(title, 'en'))
        if kind in ('vocabulary', 'taxonomy'): add(g, h, k.SKOS + 'prefLabel', k.L(title, 'en'))
        add(g, h, k.DCT + 'title', k.L(title, 'en'))
        if d.get('alt_title'): add(g, h, k.SKOS + 'altLabel', k.L(title.replace(d['title'], d['alt_title']), 'en'))
        add(g, h, k.DCT + 'description', k.L(description, 'en'))
        add(g, h, k.DCT + 'subject', k.I(self.voc(d['subject'])))
        for x in imports or []: add(g, h, k.OWL + 'imports', k.I(x))
        for x in requires or []: add(g, h, k.DCT + 'requires', k.I(x))
        add(g, h, k.VAEM + 'namespace', k.L(iri, None, k.XSD + 'anyURI'))
        add(g, h, k.VANN + 'preferredNamespacePrefix', k.L(d['prefix'] + {'vocabulary': 'voc', 'taxonomy': 'tax', 'ontology': '', 'shapes': 'shp'}[kind]))
        add(g, h, k.DCT + 'language', k.L('en'))
        for x in sorted(sources or []): add(g, h, k.DCT + 'source', k.I(x))
        add(g, h, k.DCT + 'publisher', k.I(self.cfg['publisher']))
        for c in self.cfg.get('conformsTo', []) + (self.cfg.get('ontologyConformsTo', []) if kind == 'ontology' else []):
            add(g, h, k.DCT + 'conformsTo', k.I(c))
        if d['level'] == 'domain': add(g, h, k.DCT + 'isPartOf', k.I(self.base + f'{kind}/{d["area"]}/'))
        if d.get('replaces'): add(g, h, k.DCT + 'replaces', k.I(self.base + f'{kind}/{d["replaces"]}/'))
        add(g, h, k.SKOS + 'editorialNote', k.L('Definitions were first drafted with the assistance of generative artificial intelligence tools, at the direction of the author, and are under review.', 'en'))
        for v_, when, note in d.get('changes', [('0.1.0', '2026-10-20', 'first release.')]):
            add(g, h, k.SKOS + 'changeNote', k.L(f'{v_} ({when}): {note} Built by build_domains.py from {spec_file(d)} against Baseline Core v1.0 (core {CORE_VERSION}).', 'en'))
        add(g, h, k.OWL + 'versionInfo', k.L(self.ver))
        add(g, h, k.OWL + 'versionIRI', k.I(iri + self.ver + '/'))
        add(g, h, k.DCT + 'identifier', k.L(f'{kind}-{slug_of(d)}'))
        add(g, h, self.CORE + 'hasLifecycleStatus', self.status)
        add(g, h, k.DCT + 'creator', self.author)
        add(g, h, k.DCT + 'created', self.today)
        add(g, h, k.DCT + 'modified', self.now)
        return h

    def build_domain(self, s, write=True):
        d = s.DOMAIN
        key, pre = d['key'], d['prefix']
        self.ver = d.get('version', '0.1.0')
        self.cur = d
        allowed = self.lineage_of(d)
        sl = slug_of(d)
        vns = self.base + f'vocabulary/{sl}/'
        tns = self.base + f'taxonomy/{sl}/'
        ons = self.ont_prefix[pre]
        sns = self.base + f'shapes/{sl}/'
        title = d['title']
        files = {}

        def known_voc(ref):
            iri = self.voc(ref)
            if iri in self.core_vocab or iri in self.dom_vocab: return iri
            self.err(key, f'unknown primitive {ref}'); return iri

        def known_cls(ref):
            iri = self.cls(ref)
            if iri not in self.core_classes and iri not in self.dom_classes: self.err(key, f'unknown class {ref}')
            return iri

        def known_prop(ref):
            iri = self.cls(ref)
            if iri.startswith(k.DCT) or iri.startswith('http://purl.obolibrary.org/obo/RO_'): return iri
            if iri not in self.core_props and iri not in self.dom_props: self.err(key, f'unknown relation {ref}')
            return iri

        # vocabulary
        g = collections.OrderedDict()
        h = self.header(g, vns, 'vocabulary', s, f'{title} {KIND_TITLE["vocabulary"]}', d['vocabulary_description'])
        tops = [v for v in s.VOCAB if not v.broader]
        for v in tops: add(g, h, k.SKOS + 'hasTopConcept', k.I(vns + v.id))
        kids = collections.defaultdict(list)
        for v in s.VOCAB:
            if v.broader: kids[v.broader].append(v.id)
        for v in s.VOCAB:
            x = k.I(vns + v.id)
            add(g, x, k.RDF + 'type', k.I(k.SKOS + 'Concept'))
            add(g, x, k.RDFS + 'label', k.L(v.label, 'en'))
            add(g, x, k.SKOS + 'prefLabel', k.L(v.label, 'en'))
            for al in v.alt: add(g, x, k.SKOS + 'altLabel', k.L(al, 'en'))
            add(g, x, k.SKOS + 'definition', k.L(v.definition, 'en'))
            if v.scope: add(g, x, k.SKOS + 'scopeNote', k.L(v.scope, 'en'))
            if v.promote: add(g, x, k.SKOS + 'editorialNote', k.L('Candidate for promotion to the core: ' + v.promote, 'en'))
            if v.homonym: add(g, x, k.SKOS + 'editorialNote', k.L(f'Homonym of {self.voc(v.homonym)}, kept apart because the senses differ.', 'en'))
            add(g, x, k.SKOS + 'inScheme', k.I(vns))
            if v.broader: add(g, x, k.SKOS + 'broader', k.I(vns + v.broader))
            else: add(g, x, k.SKOS + 'topConceptOf', k.I(vns))
            for c in kids[v.id]: add(g, x, k.SKOS + 'narrower', k.I(vns + c))
            self.gov(g, x)
        files['vocabulary'] = (g, vns, f'{title} {KIND_TITLE["vocabulary"]}')

        # taxonomy
        g = collections.OrderedDict()
        by_id = {c.id: c for c in s.TAXONOMY}
        if len(by_id) != len(s.TAXONOMY): self.err(key, 'duplicate taxonomy ids')
        sources = set()
        for c in s.TAXONOMY:
            for r_ in c.subjects + ([c.primary] if c.primary else []):
                sources.add(self.base + 'vocabulary/' + r_.split('/')[0] + '/')
        h = self.header(g, tns, 'taxonomy', s, f'{title} {KIND_TITLE["taxonomy"]}', d['taxonomy_description'], sources=sources)
        kids = collections.defaultdict(list)
        for c in s.TAXONOMY:
            if c.broader:
                if c.broader not in by_id: self.err(key, f'{c.id}: broader {c.broader} not in the taxonomy')
                kids[c.broader].append(c.id)
            else:
                add(g, h, k.SKOS + 'hasTopConcept', k.I(tns + c.id))
        for c in s.TAXONOMY:
            x = k.I(tns + c.id)
            add(g, x, k.RDF + 'type', k.I(k.SKOS + 'Concept'))
            add(g, x, k.RDFS + 'label', k.L(c.label, 'en'))
            add(g, x, k.SKOS + 'prefLabel', k.L(c.label, 'en'))
            for al in c.alt: add(g, x, k.SKOS + 'altLabel', k.L(al, 'en'))
            add(g, x, k.SKOS + 'definition', k.L(c.definition, 'en'))
            if c.scope: add(g, x, k.SKOS + 'scopeNote', k.L(c.scope, 'en'))
            add(g, x, k.SKOS + 'inScheme', k.I(tns))
            if c.broader: add(g, x, k.SKOS + 'broader', k.I(tns + c.broader))
            else: add(g, x, k.SKOS + 'topConceptOf', k.I(tns))
            for kid in kids[c.id]: add(g, x, k.SKOS + 'narrower', k.I(tns + kid))
            primary = c.primary or c.subjects[-1]
            if primary not in c.subjects: self.err(key, f'{c.id}: primary {primary} is not one of its subjects')
            add(g, x, self.CORE + 'hasPrimaryTerm', k.I(known_voc(primary)))
            for r_ in c.subjects: add(g, x, k.DCT + 'subject', k.I(known_voc(r_)))
            if c.formalized: add(g, x, self.CORE + 'formalizedBy', k.I(known_cls(c.formalized)))
            elif not c.broader: self.err(key, f'top concept {c.id} has no formalizedBy')
            bm = s.BROADMATCH.get(c.id)
            if bm:
                biri = self.base + bm
                if biri not in self.core_tax and biri not in self.dom_tax and biri not in self.ref_tax: self.err(key, f'{c.id}: broadMatch target {bm} does not exist')
                add(g, x, k.SKOS + 'broadMatch', k.I(biri))
            for em in getattr(s, 'EXACTMATCH', {}).get(c.id, []):
                eiri = self.base + em
                if eiri not in self.core_tax and eiri not in self.dom_tax and eiri not in self.ref_tax: self.err(key, f'{c.id}: exactMatch target {em} does not exist')
                add(g, x, k.SKOS + 'exactMatch', k.I(eiri))
            self.gov(g, x)
            # concept links report: words of the label not covered by its primitives
            words = set(self.label_words(c.label))
            covered = set()
            for r_ in c.subjects:
                iri = self.voc(r_)
                lab = self.core_vocab.get(iri) or (self.dom_vocab[iri][1].label if iri in self.dom_vocab else '')
                alts = self.dom_vocab[iri][1].alt if iri in self.dom_vocab else self.core_alts.get(iri, [])
                for l in [lab] + alts: covered |= set(self.label_words(l))
            unmatched = sorted(w for w in words if not any(stem(w) == stem(cw) for cw in covered))
            self.links.append(dict(domain=key, concept=c.id, label=c.label, kind='primitive' if len(c.subjects) == 1 else 'polymorphic',
                                   primary_term=primary, subjects=' '.join(c.subjects), formalized_by=c.formalized or '',
                                   broad_match=bm or '', unmatched_words=' '.join(unmatched)))
        for bad in [x for x in s.BROADMATCH if x not in by_id]: self.err(key, f'broadMatch for unknown concept {bad}')
        files['taxonomy'] = (g, tns, f'{title} {KIND_TITLE["taxonomy"]}')

        # ontology
        g = collections.OrderedDict()
        # D3 (0.1.1): owl:imports names the ontology IRI, so tools resolve it; dct:requires pins the version built against
        imports, requires = [self.CORE], [self.CORE + CORE_VERSION + '/']
        ups = []
        if d['level'] == 'domain':
            ups.append(self.by_key[d['area']].DOMAIN)          # the area ontology
            p_ = d.get('parent')
            while p_:
                ups.append(self.by_key[p_].DOMAIN); p_ = self.by_key[p_].DOMAIN.get('parent')
        for u in ups:
            imports.append(self.ont_prefix[u['prefix']]); requires.append(self.ont_prefix[u['prefix']] + u.get('version', '0.1.0') + '/')
        h = self.header(g, ons, 'ontology', s, f'{title} {KIND_TITLE["ontology"]}', d['ontology_description'], imports=imports, requires=requires)
        bn = Blank(key.replace('.', '_'))
        for c in s.CLASSES:
            x = k.I(ons + c.id)
            add(g, x, k.RDF + 'type', k.I(k.OWL + 'Class'))
            add(g, x, k.RDFS + 'label', k.L(c.label, 'en'))
            add(g, x, k.SKOS + 'prefLabel', k.L(c.label, 'en'))
            for al in c.alt: add(g, x, k.SKOS + 'altLabel', k.L(al, 'en'))
            add(g, x, k.SKOS + 'definition', k.L(c.definition, 'en'))
            if c.scope: add(g, x, k.SKOS + 'scopeNote', k.L(c.scope, 'en'))
            for p_ in c.parents: add(g, x, k.RDFS + 'subClassOf', k.I(known_cls(p_)))
            for q, prop, target in c.restrictions:
                b = bn()
                add(g, b, k.RDF + 'type', k.I(k.OWL + 'Restriction'))
                add(g, b, k.OWL + 'onProperty', k.I(known_prop(prop)))
                add(g, b, k.OWL + ('someValuesFrom' if q == 'some' else 'allValuesFrom'), k.I(known_cls(target)))
                add(g, x, k.RDFS + 'subClassOf', b)
            add(g, x, k.RDFS + 'isDefinedBy', k.I(ons))
            add(g, x, self.CORE + 'hasPrimaryTerm', k.I(known_voc(c.primary)))
            add(g, x, k.DCT + 'subject', k.I(self.voc(c.primary)))
            self.gov(g, x)
        for p_ in s.PROPERTIES:
            x = k.I(ons + p_.id)
            add(g, x, k.RDF + 'type', k.I(k.OWL + 'ObjectProperty'))
            add(g, x, k.RDFS + 'label', k.L(p_.label, 'en'))
            add(g, x, k.SKOS + 'prefLabel', k.L(p_.label, 'en'))
            add(g, x, k.SKOS + 'definition', k.L(p_.definition, 'en'))
            if p_.scope: add(g, x, k.SKOS + 'scopeNote', k.L(p_.scope, 'en'))
            add(g, x, k.RDFS + 'subPropertyOf', k.I(known_prop(p_.parent)))
            if p_.inverse: add(g, x, k.OWL + 'inverseOf', k.I(known_prop(p_.inverse)))
            if p_.promote: add(g, x, k.SKOS + 'editorialNote', k.L('Candidate for promotion to the core: ' + p_.promote, 'en'))
            add(g, x, k.RDFS + 'isDefinedBy', k.I(ons))
            self.gov(g, x)
        for cid, concept in getattr(s, 'FORMALIZES', {}).items():
            ciri = self.base + concept
            if ciri not in self.core_tax: self.err(key, f'FORMALIZES target {concept} is not a core taxonomy concept')
            add(g, k.I(ciri), self.CORE + 'formalizedBy', k.I(ons + cid))
        files['ontology'] = (g, ons, f'{title} {KIND_TITLE["ontology"]}')

        # shapes
        g = collections.OrderedDict()
        h = self.header(g, sns, 'shapes', s, f'{title} {KIND_TITLE["shapes"]}', d['shapes_description'], imports=[ons], requires=[ons + self.ver + '/'])
        bn = Blank(key.replace('.', '_') + 's')
        for sh in s.SHAPES:
            x = k.I(sns + sh.id + '-shape')
            add(g, x, k.RDF + 'type', k.I(k.SH + 'NodeShape'))
            add(g, x, k.RDFS + 'label', k.L(sh.label, 'en'))
            add(g, x, k.SKOS + 'prefLabel', k.L(sh.label, 'en'))
            add(g, x, k.SKOS + 'definition', k.L(sh.definition, 'en'))
            add(g, x, k.RDFS + 'isDefinedBy', k.I(sns))
            add(g, x, k.SH + 'targetClass', k.I(known_cls(sh.target)))
            for pr in sh.props:
                b = bn()
                if pr['path'].startswith('^'):
                    pb = bn(); add(g, pb, k.SH + 'inversePath', k.I(known_prop(pr['path'][1:]))); add(g, b, k.SH + 'path', pb)
                else:
                    add(g, b, k.SH + 'path', k.I(known_prop(pr['path'])))
                if pr.get('cls'): add(g, b, k.SH + 'class', k.I(known_cls(pr['cls'])))
                if pr.get('or_cls'):      # sh:or ( [ sh:class A ] [ sh:class B ] … )
                    head = cur = bn()
                    for i, c_ in enumerate(pr['or_cls']):
                        alt = bn(); add(g, alt, k.SH + 'class', k.I(known_cls(c_)))
                        add(g, cur, k.RDF + 'first', alt)
                        nxt = bn() if i < len(pr['or_cls']) - 1 else k.I(k.RDF + 'nil')
                        add(g, cur, k.RDF + 'rest', nxt); cur = nxt
                    add(g, b, k.SH + 'or', head)
                if pr.get('min'): add(g, b, k.SH + 'minCount', k.L(str(pr['min']), None, k.XSD + 'integer'))
                if pr.get('max'): add(g, b, k.SH + 'maxCount', k.L(str(pr['max']), None, k.XSD + 'integer'))
                add(g, b, k.SH + 'message', k.L(pr['msg'], 'en'))
                if pr.get('warn'): add(g, b, k.SH + 'severity', k.I(k.SH + 'Warning'))
                add(g, x, k.SH + 'property', b)
            self.gov(g, x)
        files['shapes'] = (g, sns, f'{title} {KIND_TITLE["shapes"]}')

        # D1: insulation
        CITE = {k.DCT + 'subject', self.CORE + 'hasPrimaryTerm', k.DCT + 'source'}
        for kind, (gg, _, _) in files.items():
            for subj, ps in gg.items():
                for p_, objs in ps.items():
                    for o in objs + [subj]:
                        if o[0] != 'I': continue
                        if p_ in CITE and '/vocabulary/' in o[1]: continue      # primitives may be cited from any domain (D27)
                        if p_ == k.DCT + 'replaces': continue                   # provenance: the asset this one replaces
                        dom = self.ref_domain(o[1])
                        if dom and dom not in allowed:
                            self.err(key, f'{kind} refers to {dom}, outside its area and lineage: {short(self, o[1])}')
        # write and check
        written = {}
        for kind, (gg, iri, ttitle) in files.items():
            name = f'{kind}-{sl}-{self.ver}'
            text, trig = self.serialize(gg, iri, ttitle, name, kind)
            triples, _ = k.parse_turtle(text)          # round trip through the workbench parser
            vocab = set(self.core_vocab) | set(self.dom_vocab)
            counted, res = k.check(triples, self.base, self.policy, vocab)
            for rule, items in res.items():
                for sev, iri_, msg in items:
                    line = f'{name}: {rule}: {short(self, iri_)}: {msg}'
                    if sev == 'error': self.err(key, line)
                    elif sev == 'warn': self.warn(key, line)
                    else: self.notes.append(f'{key}: {line}')
            written[kind] = dict(name=name, triples=len(triples), counted=dict(counted), graph=iri, text=text, trig=trig)
            if write:
                folder = self.out / d['folder']
                (folder / 'ttl').mkdir(parents=True, exist_ok=True); (folder / 'trig').mkdir(parents=True, exist_ok=True)
                (folder / 'ttl' / f'{name}.ttl').write_text(text, encoding='utf-8')
                (folder / 'trig' / f'{name}.trig').write_text(trig, encoding='utf-8')
        files['_written'] = written
        files['_graphs'] = {kk: v[0] for kk, v in files.items() if not kk.startswith('_')}
        return files

    def label_words(self, label):
        return [w for w in re.split(r"[\s,/]+|-", label.lower().replace("'", '')) if w and w not in {'and', 'of', 'the', 'for', 'to', 'in', 'on', 'a', 'an', 'per', 'with'}]

    def serialize(self, g, iri, title, name, kind):
        prefixes = {'core': self.CORE, 'obo': 'http://purl.obolibrary.org/obo/', 'owl': k.OWL, 'rdf': k.RDF, 'rdfs': k.RDFS,
                    'skos': k.SKOS, 'dct': k.DCT, 'xsd': k.XSD, 'sh': k.SH, 'vaem': k.VAEM, 'vann': k.VANN}
        for p_ in ('process', 'party', 'role', 'asset', 'location', 'time', 'event', 'issue', 'product', 'services', 'capability',
                   'persona', 'domain', 'rules', 'requirements', 'lifecycle', 'valuestream', 'compliance', 'job', 'decision',
                   'governance', 'logic', 'measure', 'policy', 'value'):
            prefixes[p_ + 'voc'] = f'{self.base}vocabulary/core-{p_}/'
            prefixes[p_ + 'tax'] = f'{self.base}taxonomy/core-{p_}/'
        prefixes['apqc'] = f'{self.base}taxonomy/apqc-pcf/'
        for s in self.specs:
            dk, dp = slug_of(s.DOMAIN), s.DOMAIN['prefix']
            prefixes[dp] = self.ont_prefix[dp]
            prefixes[dp + 'voc'] = f'{self.base}vocabulary/{dk}/'
            prefixes[dp + 'tax'] = f'{self.base}taxonomy/{dk}/'
            prefixes[dp + 'shp'] = f'{self.base}shapes/{dk}/'
        w = k.Writer(prefixes, [self.CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
        header = next(x for x in g if x[0] == 'I' and x[1] == iri)
        rank = {k.OWL + 'Ontology': 0, k.SKOS + 'ConceptScheme': 0, k.OWL + 'Class': 2, k.OWL + 'ObjectProperty': 4, k.SH + 'NodeShape': 5}
        order = {x: i for i, x in enumerate(g)}
        subjects = [x for x in g if x[0] == 'I']
        def r(x):
            ts = [t[1] for t in g[x].get(k.RDF + 'type', [])]
            return min([rank.get(t, 3) for t in ts] or [6])
        subjects = sorted(subjects, key=lambda x: (0 if x == header else 1, r(x), order[x]))
        d = self.cur
        area = self.by_key[d['area']].DOMAIN['title']
        ups = 'the core' if d['level'] == 'area' else f'the core and the {area} ontology' + (' and its parent domains' if d.get('parent') else '')
        head = (f'# {title}\n# {iri}  ·  version {self.ver}  ·  {self.cfg["lifecycleStatus"]}\n'
                f'# Generated by build_domains.py on {self.now[1]} from {spec_file(d)}\n'
                f'# Operational area: {area}  ·  imports only {ups}\n'
                f'# Standards: {self.cfg["standardsRef"]}\n')
        text = w.write(g, subjects, head)
        trig = w.write_trig(g, subjects, head.replace('\n# Standards', f'\n# Named graph: {iri}\n# Standards'), iri)
        return text, trig

    # ── D5: lineage ────────────────────────────────────────────────────────
    def check_lineage(self):
        OBO = 'http://purl.obolibrary.org/obo/'
        g = collections.OrderedDict((s_, collections.OrderedDict((p, list(o)) for p, o in ps.items())) for s_, ps in self.core_graph.items())
        for s, files in self.outputs:
            for s_, ps in files['_graphs']['ontology'].items():
                for p, objs in ps.items():
                    for o in objs: g.setdefault(s_, collections.OrderedDict()).setdefault(p, []).append(o)
        self.lineage = []
        for s, files in self.outputs:
            key = s.DOMAIN['key']
            ons = self.ont_prefix[s.DOMAIN['prefix']]
            for kind, typ, up in (('class', k.OWL + 'Class', k.RDFS + 'subClassOf'), ('relation', k.OWL + 'ObjectProperty', k.RDFS + 'subPropertyOf')):
                for x, ps in files['_graphs']['ontology'].items():
                    if x[0] != 'I' or not x[1].startswith(ons) or k.I(typ) not in ps.get(k.RDF + 'type', []): continue
                    seen, todo, path_ok = set(), [x], False
                    while todo:
                        y = todo.pop()
                        if y in seen: continue
                        seen.add(y)
                        for o in g.get(y, {}).get(up, []):
                            if o[0] != 'I': continue
                            if o[1].startswith(OBO): path_ok = True
                            else: todo.append(o)
                    if not path_ok: self.err(key, f'{kind} {short(self, x[1])} does not reach BFO/RO/IAO')
                    self.lineage.append((key, kind, x[1], path_ok))

    # ── reports ────────────────────────────────────────────────────────────
    def reports(self, only):
        rv = self.out / 'review'   # KE Domains/review
        rv.mkdir(parents=True, exist_ok=True)
        with (rv / 'concept-links.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(self.links[0].keys())); w.writeheader(); w.writerows(self.links)
        with (rv / 'promotion-candidates.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['domain', 'primitive', 'label', 'definition', 'reason'])
            for iri, (key, v) in self.dom_vocab.items():
                if v.promote: w.writerow([key, short(self, iri), v.label, v.definition, v.promote])
            for s in self.specs:
                for p_ in s.PROPERTIES:
                    if p_.promote: w.writerow([s.DOMAIN['key'], short(self, self.ont_prefix[s.DOMAIN['prefix']] + p_.id) + ' (relation)', p_.label, p_.definition, p_.promote])
        with (rv / 'homonyms.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['domain_term', 'label', 'core_term', 'how_the_senses_differ'])
            for iri, l, core, note in self.homonyms: w.writerow([short(self, iri), l, short(self, core), note])
        lines = [f'# Build report: operational areas and domains', '',
                 f'Built {self.now[1]} against Baseline Core v1.0 (core {CORE_VERSION}) by `_build/build_domains.py`.', '',
                 '| Operational area | Area or domain | Version | Vocabulary terms | Taxonomy concepts | Classes | Relations | Shapes | Triples |', '|---|---|---|---:|---:|---:|---:|---:|---:|']
        tot = collections.Counter()
        for s, files in self.outputs:
            wr = files['_written']
            n = dict(v=len(s.VOCAB), t=len(s.TAXONOMY), c=len(s.CLASSES), r=len(s.PROPERTIES), s=len(s.SHAPES),
                     x=sum(v['triples'] for v in wr.values()))
            tot.update(n)
            lines.append(f'| {self.by_key[s.DOMAIN["area"]].DOMAIN["title"]} | {s.DOMAIN["title"]} | {s.DOMAIN.get("version", "0.1.0")} | {n["v"]} | {n["t"]} | {n["c"]} | {n["r"]} | {n["s"]} | {n["x"]} |')
        lines.append(f'| **Total** | | | {tot["v"]} | {tot["t"]} | {tot["c"]} | {tot["r"]} | {tot["s"]} | {tot["x"]} |')
        lines += ['', '## Checks', '',
                  f'- Part III conformance (ke_ingest.check) and the domain rules D1–D6, D27: **{len(self.errors)} errors, {len(self.warnings)} warnings**, {len(self.notes)} notes.',
                  f'- Lineage: {sum(1 for x in self.lineage if x[3])} of {len(self.lineage)} domain classes and relations reach BFO/RO/IAO.',
                  f'- Insulation (D27): classes, relations, concepts and imports refer only to the core, the operational area, parent domains, the domain itself and the APQC reference registry; primitives are cited across areas, never copied.',
                  f'- Primitives: {len(self.dom_vocab)} domain primitives, none duplicating a core or sibling primitive; {len(self.homonyms)} declared homonyms (`homonyms.csv`); '
                  f'{sum(1 for v in self.dom_vocab.values() if v[1].promote)} general primitives proposed for promotion to the core (`promotion-candidates.csv`).',
                  f'- Concepts: {len(self.links)} taxonomy concepts, every one linked to its primitives (`concept-links.csv`); '
                  f'{sum(1 for x in self.links if x["unmatched_words"])} have a label word not covered by a primitive (listed in `unmatched_words` for review).', '']
        for title, items in (('Errors', self.errors), ('Warnings', self.warnings), ('Notes', self.notes)):
            lines += [f'## {title}', ''] + ([f'- {x}' for x in items] or ['None.']) + ['']
        (rv / 'build-report.md').write_text('\n'.join(lines), encoding='utf-8')
        for s, files in self.outputs:
            if only in (None, s.DOMAIN['key']): self.domain_readme(s, files)
        print('\n'.join(lines[:12 + len(self.outputs)]))
        print(f'errors {len(self.errors)}  warnings {len(self.warnings)}  notes {len(self.notes)}')
        for x in self.errors[:60]: print('  ERROR', x)
        for x in self.warnings[:60]: print('  warn ', x)


    def domain_readme(self, s, files):
        d = s.DOMAIN
        key, title = d['key'], d['title']
        is_container = d['level'] == 'area'
        area = self.by_key[d['area']].DOMAIN['title']
        tops = [c for c in s.TAXONOMY if not c.broader]
        kids = collections.Counter(c.broader for c in s.TAXONOMY if c.broader)
        def cref(ref):
            pre, local = ref.split(':', 1)
            return f'`{pre}:{local}`'
        L = [f'# {title}', '',
             (f'The shared assets of the {area} operational area. They hold what two or more of its domains share, so that the '
              f'domains never refer to one another. They import only the core domain ontology {CORE_VERSION}.' if is_container else
              f'A domain of the {area} operational area' + (f', an L{key.count(".") + 1} domain of {self.by_key[d["parent"]].DOMAIN["title"]}' if d.get('parent') else '') +
              f'. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the {area} ontology' + (' and its parent domains' if d.get('parent') else '') +
              f', never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).'), '',
             d['ontology_description'], '',
             '## Files', '', '| Asset | Named graph | Triples |', '|---|---|---:|']
        for kind in ('vocabulary', 'taxonomy', 'ontology', 'shapes'):
            w = files['_written'][kind]
            L.append(f'| `ttl/{w["name"]}.ttl` · `trig/{w["name"]}.trig` | `{w["graph"]}` | {w["triples"]} |')
        L += ['', f'Built from `KE Domains/_build/{spec_file(d)}` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; '
              'a rebuild overwrites hand edits to these files.', '',
              f'## Vocabulary ({len(s.VOCAB)} primitives)', '',
              ', '.join(f'{v.label}' + (' ⁺' if v.promote else '') + (' ⁼' if v.homonym else '') for v in s.VOCAB), '',
              '⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term', '',
              f'## Taxonomy ({len(s.TAXONOMY)} concepts, {len(tops)} top concepts)', '', '| Top concept | Formalized by | Narrower | Specializes |', '|---|---|---:|---|']
        def count_all(cid):
            n = 0
            for c in s.TAXONOMY:
                if c.broader == cid: n += 1 + count_all(c.id)
            return n
        for c in tops:
            bm = s.BROADMATCH.get(c.id, '')
            L.append(f'| {c.label} | {cref(c.formalized)} | {count_all(c.id)} | {("`" + bm.replace("taxonomy/", "") + "`") if bm else ""} |')
        L += ['', f'## Ontology ({len(s.CLASSES)} classes, {len(s.PROPERTIES)} relations)', '', '| Class | Parent | Axioms |', '|---|---|---|']
        for c in s.CLASSES:
            ax = '; '.join(f'{p_} {q} {t}' for q, p_, t in c.restrictions)
            L.append(f'| `{d["prefix"]}:{c.id}` | {", ".join(cref(p_) for p_ in c.parents)} | {ax} |')
        for p_ in s.PROPERTIES:
            L.append(f'| `{d["prefix"]}:{p_.id}` (relation) | {cref(p_.parent)} | {p_.definition} |')
        if getattr(s, 'FORMALIZES', None):
            L += ['', 'Core taxonomy concepts formalized by classes of this ontology (the `core:formalizedBy` triples live in this domain\'s ontology graph; the baseline files and graphs are not changed): '
                  + ', '.join(f'`{v.replace("taxonomy/", "")}` → `{d["prefix"]}:{kk}`' for kk, v in s.FORMALIZES.items()) + '.']
        L += ['', f'## Shapes ({len(s.SHAPES)})', ''] + [f'- `{sh.id}-shape` on `{sh.target}`: {sh.definition}' for sh in s.SHAPES] + ['']
        folder = self.out / d['folder']
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'README.md').write_text('\n'.join(L), encoding='utf-8')


def slug_of(d):
    return d['key'] if d['level'] == 'area' else 'domain-' + d['key']


def spec_file(d):
    return 'spec_' + re.sub(r'[-.]', '_', d['key']) + '.py'


class Blank:
    def __init__(self, tag): self.tag, self.n = tag, 0
    def __call__(self):
        self.n += 1
        return ('B', f'{self.tag}{self.n}')


def add(g, s, p, o):
    lst = g.setdefault(s, collections.OrderedDict()).setdefault(p, [])
    if o not in lst: lst.append(o)


def norm(label):
    return re.sub(r'[^a-z0-9]+', ' ', label.lower().replace("'", '')).strip()


def stem(w):
    for suf in ('ies', 'ing', 'es', 's', 'ed', 'ion', 'ment', 'al', 'ive', 'er', 'or', 'ity', 'ure'):
        if w.endswith(suf) and len(w) - len(suf) >= 4: return w[:-len(suf)]
    return w


def short(b, iri):
    return iri.replace(b.base, '…/')


if __name__ == '__main__':
    sys.exit(main())
