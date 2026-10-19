#!/usr/bin/env python3
"""Build the core domain ontology and its shapes from their authored sources.

    python3 ingest/build_core.py [--out "../KE Baseline"] [--version 0.1.0]

Reads   ingest/core/ontology-core.source.ttl   and   ingest/core/shapes-core.source.ttl
Writes  <out>/ttl/ontology-core-<version>.ttl, <out>/trig/ontology-core-<version>.trig,
        <out>/ttl/shapes-core-<version>.ttl,   <out>/trig/shapes-core-<version>.trig

The sources are authored, not legacy, so nothing is renamed or removed (that is what ke_ingest.py is for).
The build only adds what every published asset carries (Part III §3.7, §3.11):
  * rdfs:label next to each skos:prefLabel, rdfs:isDefinedBy on each term;
  * core:hasLifecycleStatus, owl:versionInfo, dcterms:creator, dcterms:created, dcterms:modified on each term;
  * dcterms:subject next to each core:hasPrimaryTerm (hasPrimaryTerm is a subproperty of dcterms:subject);
  * the §3.11 header fields from ke-ingest.config.json (namespace, prefix, version IRI, publisher, conformsTo,
    subject, language), then runs the ke_ingest Part III checks and a lineage check:
    every core class reaches a BFO class, every core relation reaches a BFO/RO/IAO relation.
"""
import argparse, collections, datetime, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ke_ingest as k
from ke_ingest import I, L, RDF, RDFS, OWL, SKOS, DCT, XSD, SH, VAEM, VANN

CORE = 'https://www.insperity.com/ontology/core/'
OBO = 'http://purl.obolibrary.org/obo/'
TYPE = RDF + 'type'


def load(path):
    g = collections.OrderedDict()
    text = path.read_text(encoding='utf-8')
    triples = k.parse_turtle(text)[0]
    for s, p, o in triples:
        g.setdefault(s, collections.OrderedDict()).setdefault(p[1], [])
        if o not in g[s][p[1]]: g[s][p[1]].append(o)
    return g, triples


def add(g, s, p, o):
    lst = g.setdefault(s, collections.OrderedDict()).setdefault(p, [])
    if o not in lst: lst.append(o)


def build(src, kind, cfg, version, now, today, log):
    g, _ = load(src)
    base = cfg['baseUrl']
    header = next(s for s, ps in g.items() if s[0] == 'I' and I(OWL + 'Ontology') in ps.get(TYPE, []))
    asset = header[1]
    author = L(cfg['author'])
    status = I(CORE + cfg['lifecycleStatus'])
    created_default = L(today, None, XSD + 'date')
    subjects = [header]
    for s, ps in g.items():
        if s == header or s[0] != 'I' or not s[1].startswith(base): continue
        subjects.append(s)
        for lab in ps.get(SKOS + 'prefLabel', []):
            add(g, s, RDFS + 'label', lab)
        for t in ps.get(CORE + 'hasPrimaryTerm', []):
            add(g, s, DCT + 'subject', t)
        add(g, s, RDFS + 'isDefinedBy', I(asset))
        add(g, s, CORE + 'hasLifecycleStatus', status)
        add(g, s, OWL + 'versionInfo', L(version))
        add(g, s, DCT + 'creator', author)
        if not ps.get(DCT + 'created'): add(g, s, DCT + 'created', created_default)
        add(g, s, DCT + 'modified', now)

    # header (§3.11)
    hp = g[header]
    title = hp[DCT + 'title'][0]
    add(g, header, RDFS + 'label', title)
    add(g, header, DCT + 'language', L('en'))
    add(g, header, VAEM + 'namespace', L(asset, None, XSD + 'anyURI'))
    add(g, header, VANN + 'preferredNamespacePrefix', L('core' if kind == 'ontology' else 'coreshp'))
    add(g, header, OWL + 'versionInfo', L(version))
    add(g, header, OWL + 'versionIRI', I(asset + version + '/'))
    if cfg.get('publisher'): add(g, header, DCT + 'publisher', I(cfg['publisher']))
    for c in cfg.get('conformsTo', []) + (cfg.get('ontologyConformsTo', []) if kind == 'ontology' else []):
        add(g, header, DCT + 'conformsTo', I(c))
    meta = cfg.get('assets', {}).get(f'{kind}/core', {})
    subj = meta.get('subject') or cfg.get('defaultSubject')
    for x in ([subj] if isinstance(subj, str) else subj or []):
        add(g, header, DCT + 'subject', I(x))
    add(g, header, SKOS + 'changeNote', L(
        f'{version} ({today}): rebuilt under {asset} from the authored source {src.name}. Every class specializes a BFO 2020 class '
        f'and every relation a BFO, RO or IAO relation; anchored on the process step. Replaces {base}ontology/core-domain/ and the '
        f'core-* shapes graphs.' if kind == 'ontology' else
        f'{version} ({today}): process-step anchoring shapes for {CORE}, built from {src.name}. Replace the core-compliance, '
        f'core-domain, core-party, core-process and core-product shapes graphs.', 'en'))
    add(g, header, CORE + 'hasLifecycleStatus', status)
    add(g, header, DCT + 'creator', author)
    add(g, header, DCT + 'contributor', author)
    add(g, header, DCT + 'modified', now)

    # order: header, annotation properties, classes (source order), object properties, individuals, shapes
    rank = {OWL + 'Ontology': 0, OWL + 'AnnotationProperty': 1, OWL + 'Class': 2, OWL + 'ObjectProperty': 4, SH + 'NodeShape': 5}
    def r(s):
        ts = [t[1] for t in g[s].get(TYPE, [])]
        return min([rank.get(t, 3) for t in ts] or [3])
    order = {s: i for i, s in enumerate(subjects)}
    subjects = sorted(subjects, key=lambda s: (r(s), order[s]))
    return g, subjects, asset, title[1]


def write(g, subjects, asset, title, src, dest, kind, version, cfg, now):
    prefixes = {'core': CORE, 'obo': OBO, 'owl': OWL, 'rdf': RDF, 'rdfs': RDFS, 'skos': SKOS, 'dct': DCT, 'xsd': XSD,
                'sh': SH, 'vaem': VAEM, 'vann': VANN, 'coreshp': cfg['baseUrl'] + 'shapes/core/'}
    for d in ('process', 'party', 'role', 'asset', 'location', 'time', 'event', 'issue', 'product', 'services', 'capability',
              'persona', 'domain', 'rules', 'requirements', 'lifecycle', 'valuestream', 'compliance'):
        prefixes[d + 'voc'] = f'{cfg["baseUrl"]}vocabulary/core-{d}/'
    prefixes['domaintax'] = cfg['baseUrl'] + 'taxonomy/core-domain/'
    w = k.Writer(prefixes, [CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
    head = (f'# {title}\n# {asset}  ·  version {version}  ·  {cfg["lifecycleStatus"]}\n'
            f'# Generated by build_core.py on {now[1]} from {src.name}\n# Standards: {cfg["standardsRef"]}\n')
    name = f'{kind}-core-{version}'
    (dest / 'ttl').mkdir(parents=True, exist_ok=True); (dest / 'trig').mkdir(parents=True, exist_ok=True)
    ttl = dest / 'ttl' / f'{name}.ttl'
    ttl.write_text(w.write(g, subjects, head), encoding='utf-8')
    trig = dest / 'trig' / f'{name}.trig'
    trig.write_text(w.write_trig(g, subjects, head.replace('\n# Standards', f'\n# Named graph: {asset}\n# Standards'), asset), encoding='utf-8')
    return ttl, trig


def lineage(ont):
    """Every core class reaches a BFO class; every core object property reaches an OBO relation."""
    probs = []
    for kind, typ, up in (('class', OWL + 'Class', RDFS + 'subClassOf'), ('relation', OWL + 'ObjectProperty', RDFS + 'subPropertyOf')):
        terms = [s for s, ps in ont.items() if s[0] == 'I' and s[1].startswith(CORE) and I(typ) in ps.get(TYPE, [])]
        inv = {}
        for s in terms:
            for o in ont[s].get(OWL + 'inverseOf', []): inv[o] = s; inv[s] = o
        for s in terms:
            seen, todo, ok = set(), [s], False
            while todo:
                x = todo.pop()
                if x in seen: continue
                seen.add(x)
                for o in ont.get(x, {}).get(up, []):
                    if o[0] != 'I': continue
                    if o[1].startswith(OBO): ok = True
                    else: todo.append(o)
            if not ok and kind == 'relation' and s in inv:
                ok = 'inverse'
            if not ok: probs.append(f'{kind} {s[1][len(CORE):]} does not reach BFO/RO')
            elif ok == 'inverse': pass
    return probs, len([s for s, ps in ont.items() if s[0] == 'I' and s[1].startswith(CORE) and I(OWL + 'Class') in ps.get(TYPE, [])])


def apply_formalized(dest, csv_path, classes, cfg, now, version):
    """core:formalizedBy on taxonomy concepts (formalized-by.csv): the path from each core taxonomy to BFO.
    Rewrites ttl/taxonomy-core-*.ttl and the matching .trig in place, keeping their header comment and term order.
    Rows without a core_class are reported for review. Running it again replaces the earlier links."""
    import csv
    rows = list(csv.DictReader(csv_path.open(encoding='utf-8')))
    by_tax = collections.defaultdict(list)
    for r_ in rows: by_tax[r_['taxonomy']].append(r_)
    plan = k.folder_plan(dest / 'ttl')
    files = {h['iri']: h['path'] for h in plan['current'] if h['kind'] == 'taxonomy'}
    report = []
    FB = CORE + 'formalizedBy'
    for tax, items in sorted(by_tax.items()):
        scheme = f'{cfg["baseUrl"]}taxonomy/{tax}/'
        path = files.get(scheme)
        if not path:
            report.append(f'  warn  no current file for {scheme}'); continue
        text = path.read_text(encoding='utf-8')
        head = ''
        for ln in text.split('\n'):
            if not ln.startswith('#'): break
            if not ln.startswith('# Named graph:'): head += ln + '\n'
        triples, prefixes = k.parse_turtle(text)
        g, order = collections.OrderedDict(), []
        for s, p, o in triples:
            if s not in g: g[s] = collections.OrderedDict(); order.append(s)
            lst = g[s].setdefault(p[1], [])
            if o not in lst: lst.append(o)
        changed = 0
        for s in order:
            if s[0] == 'I' and FB in g[s]: del g[s][FB]; changed += 1
        for r_ in items:
            s = I(scheme + r_['concept'])
            if s not in g:
                report.append(f'  warn  {tax}: concept {r_["concept"]} not found'); continue
            if not r_['core_class']:
                report.append(f'  review {tax}/{r_["concept"]}: {r_["note"]}'); continue
            if r_['core_class'] not in classes:
                report.append(f'  error {tax}/{r_["concept"]}: core:{r_["core_class"]} is not a core class'); continue
            g[s][FB] = [I(CORE + r_['core_class'])]
            g[s][DCT + 'modified'] = [now]
            changed += 1
        subjects = [s for s in order if s[0] == 'I']
        w = k.Writer(dict(prefixes, core=CORE), [CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
        path.write_text(w.write(g, subjects, head), encoding='utf-8')
        trig = dest / 'trig' / (path.stem + '.trig')
        if trig.exists():
            th = head.replace('\n# Standards', f'\n# Named graph: {scheme}\n# Standards')
            trig.write_text(w.write_trig(g, subjects, th, scheme), encoding='utf-8')
        linked = sum(1 for r_ in items if r_['core_class'] and I(scheme + r_['concept']) in g)
        report.insert(0, f'  {path.name}: {linked} of {len(items)} top concepts formalized')
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--src', default=str(HERE / 'core'))
    ap.add_argument('--out', default=str(HERE.parent.parent / 'KE Baseline'))
    ap.add_argument('--version', default=None)
    ap.add_argument('-c', '--config', default=None)
    ap.add_argument('--no-taxonomies', action='store_true', help='do not write core:formalizedBy into the taxonomy files')
    a = ap.parse_args(argv)
    cfg, _ = k.load_config(a.config)
    version = a.version or cfg.get('initialVersion', '0.1.0')
    t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    now = L(t.strftime('%Y-%m-%dT%H:%M:%SZ'), None, XSD + 'dateTime')
    today = t.strftime('%Y-%m-%d')
    dest = pathlib.Path(a.out)
    policy = k.Policy(cfg) if hasattr(k, 'Policy') else None
    vocab = set(k.vocab_index(dest / 'ttl')) if hasattr(k, 'vocab_index') else None
    built = {}
    for kind in ('ontology', 'shapes'):
        src = pathlib.Path(a.src) / f'{kind}-core.source.ttl'
        g, subjects, asset, title = build(src, kind, cfg, version, now, today, print)
        ttl, trig = write(g, subjects, asset, title, src, dest, kind, version, cfg, now)
        built[kind] = g
        triples, _ = k.read_rdf(ttl)
        counted, res = k.check(triples, cfg['baseUrl'], policy, vocab)
        print(f'{ttl.name}: {len(triples)} triples, ' + ', '.join(f'{n} {kk}' for kk, n in counted.items()))
        print(f'  also {trig.relative_to(dest)}')
        for rule, items in res.items():
            for sev, iri, msg in items:
                print(f'  {sev:5} {rule}: {iri[len(cfg["baseUrl"]):] if iri.startswith(cfg["baseUrl"]) else iri}: {msg}')
    probs, n = lineage(built['ontology'])
    print(f'Lineage: {n} classes and the core relations checked against BFO/RO: ' + ('all reach BFO/RO' if not probs else ''))
    for p in probs: print('  ' + p)
    # vocabulary terms named by hasPrimaryTerm must exist
    if vocab is not None:
        for s, ps in built['ontology'].items():
            for t in ps.get(CORE + 'hasPrimaryTerm', []):
                if t[1] not in vocab: print(f'  warn  primary term {t[1]} of {s[1][len(CORE):]} is in no vocabulary')
    fb = pathlib.Path(a.src) / 'formalized-by.csv'
    if fb.exists() and not a.no_taxonomies:
        classes = {s[1][len(CORE):] for s, ps in built['ontology'].items()
                   if s[0] == 'I' and s[1].startswith(CORE) and I(OWL + 'Class') in ps.get(TYPE, [])}
        print('core:formalizedBy (taxonomy concepts → core classes):')
        for line in apply_formalized(dest, fb, classes, cfg, now, version):
            print(line)
    return 0


if __name__ == '__main__':
    sys.exit(main())
