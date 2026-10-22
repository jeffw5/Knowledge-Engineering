#!/usr/bin/env python3
"""Build the enterprise service catalog (D25): the services every operational area publishes, in two portfolios.

    python3 _build/build_catalog.py            # from the "KE Domains" folder

  internal portfolio   internal domain services (department services, built on the APQC PCF reference registry)
  external portfolio   external services, which follow the HR Services & PEO Enterprise Business Model
                       (service line › L1 domain › L2 bounded context › L3 domain service); filled when the model is ingested
  manifest             the catalog release

A portfolio lists its services with dcterms:hasPart. A domain consumes another area's service only through its entry here,
never by referring to that area's processes or resources (D25, D27). Each published service must be defined by its
domain's assembly and loaded in GraphDB; the catalog only points to it.
"""
import argparse, collections, datetime, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
VERSION = '0.1.0'
# (portfolio, service IRI path under …/resource/, provider, note)
PUBLISHED = [
    ('internal', 'domain-sales/service/total-cost-of-employment-analysis', 'Domain Sales (Commercial Operations)', 'Sales assembly 0.4.0'),
    ('internal', 'domain-sales/service/benefits-comparison', 'Domain Sales (Commercial Operations)', 'Sales assembly 0.4.0'),
]
PORTFOLIOS = {
    'internal': ('Enterprise services internal portfolio', 'The internal domain services the operational areas publish: what each department provides to the others and to the buyers it serves, built on the processes of the APQC Process Classification Framework reference registry.'),
    'external': ('Enterprise services external portfolio', 'The external services the organization delivers to clients and their worksite employees, following the HR Services & PEO Enterprise Business Model: service line, L1 domain, L2 bounded context and L3 domain service. Empty until the business model is ingested into HR Service Operations.'),
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ingest', default=str(ROOT.parent / 'KE Workbench' / 'ingest'))
    ap.add_argument('--out', default=str(ROOT))
    a = ap.parse_args(argv)
    sys.path.insert(0, a.ingest)
    import ke_ingest as k
    cfg, _ = k.load_config(str(pathlib.Path(a.ingest) / 'ke-ingest.config.json'))
    base = cfg['baseUrl']; CORE = base + 'ontology/core/'; R = base + 'resource/enterprise-services/'
    t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    now = k.L(t.strftime('%Y-%m-%dT%H:%M:%SZ'), None, k.XSD + 'dateTime'); today = k.L(t.strftime('%Y-%m-%d'), None, k.XSD + 'date')
    out = pathlib.Path(a.out) / 'Enterprise Services' / 'catalog'
    pfx = {'core': CORE, 'rdf': k.RDF, 'rdfs': k.RDFS, 'owl': k.OWL, 'skos': k.SKOS, 'dct': k.DCT, 'xsd': k.XSD,
           'assettax': base + 'taxonomy/core-asset/', 'governancetax': base + 'taxonomy/core-governance/', 'salesres': base + 'resource/domain-sales/'}
    w = k.Writer(pfx, [CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
    def asset(g, x, label, d, kind):
        def add(s, p, o):
            g.setdefault(s, collections.OrderedDict()).setdefault(p, [])
            if o not in g[s][p]: g[s][p].append(o)
        add(x, k.RDF + 'type', k.I(CORE + 'information-asset')); add(x, k.DCT + 'type', k.I(base + f'taxonomy/core-{kind}'))
        for p in (k.RDFS + 'label', k.SKOS + 'prefLabel', k.DCT + 'title'): add(x, p, k.L(label, 'en'))
        add(x, k.SKOS + 'definition', k.L(d, 'en'))
        add(x, k.DCT + 'publisher', k.I(cfg['publisher'])); add(x, k.DCT + 'conformsTo', k.I(cfg['conformsTo'][0]))
        add(x, k.OWL + 'versionInfo', k.L(VERSION)); add(x, CORE + 'hasLifecycleStatus', k.I(CORE + cfg['lifecycleStatus']))
        add(x, k.DCT + 'creator', k.L(cfg['author'])); add(x, k.DCT + 'created', today); add(x, k.DCT + 'modified', now)
        return add
    graphs = []
    for key, (label, d) in PORTFOLIOS.items():
        gid = R + f'{key}-portfolio/'
        g = collections.OrderedDict(); x = k.I(gid)
        add = asset(g, x, label, d, 'asset/knowledge-artifact')
        add(x, k.SKOS + 'note', k.L('A portfolio of the enterprise service catalog (D25). It lists published services with dcterms:hasPart; each service is defined by its domain\'s assembly.', 'en'))
        for pf, path, provider, src in PUBLISHED:
            if pf == key: add(x, k.DCT + 'hasPart', k.I(base + 'resource/' + path))
        notes = [f'{base}resource/{path}: provided by {provider}; defined by {src}.' for pf, path, provider, src in PUBLISHED if pf == key]
        for n in notes: add(x, k.SKOS + 'editorialNote', k.L(n, 'en'))
        graphs.append((gid, g, f'{key}-portfolio-enterprise-services-{VERSION}', label))
    gid = R + f'manifest/{VERSION}/'
    g = collections.OrderedDict(); x = k.I(gid)
    add = asset(g, x, f'Enterprise services catalog {VERSION}', f'The release manifest of the enterprise service catalog {VERSION}: its internal and external portfolios.', 'governance/release-manifest')
    for gi, _, _, _ in graphs: add(x, k.DCT + 'hasPart', k.I(gi))
    graphs.append((gid, g, f'manifest-enterprise-services-{VERSION}', f'Enterprise services catalog {VERSION} (manifest)'))
    errors = 0
    for gid, g, name, title in graphs:
        subjects = [k.I(gid)] + [s for s in g if s != k.I(gid)]
        head = (f'# {title}\n# {gid}  ·  version {VERSION}  ·  {cfg["lifecycleStatus"]}\n# Generated by build_catalog.py on {now[1]}\n# Standards: {cfg["standardsRef"]}\n')
        text = w.write(g, subjects, head)
        trig = w.write_trig(g, subjects, head.replace('\n# Standards', f'\n# Named graph: {gid}\n# Standards'), gid)
        triples, _ = k.parse_turtle(text)
        _, res = k.check(triples, base, k.Policy(cfg), None)
        for rule, items in res.items():
            for sev, iri, msg in items:
                if sev == 'error': errors += 1; print('ERROR', name, rule, iri, msg)
        for sub, body in (('ttl', text), ('trig', trig)):
            (out / sub).mkdir(parents=True, exist_ok=True)
            (out / sub / f'{name}.{sub}').write_text(body, encoding='utf-8')
    print(f'{len(PUBLISHED)} services published in {len(PORTFOLIOS)} portfolios → {out}; {errors} errors')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
