#!/usr/bin/env python3
"""Build the APQC Process Classification Framework reference registry (D25): one read-only SKOS taxonomy of the PCF
elements, each with its hierarchy number, APQC element ID and the domain that owns it. Domain taxonomies link their
process kinds to it with skos:exactMatch or skos:broadMatch; no domain re-creates an APQC element.

    python3 _build/build_reference.py           # from the "KE Domains" folder

Reads   _build/apqc-pcf-7.4-category-*.txt     (element lines: "<hierarchy number> <name> (<element ID>)")
        _build/apqc-pcf-7.2.1-category-3.txt   (the previous release, for the crosswalk)
        _build/apqc_commercial.py              (owner domain and PEO applicability of each element, D28)
Writes  Reference/apqc-pcf/{ttl,trig}/taxonomy-apqc-pcf-<version>.{ttl,trig}
        Reference/apqc-pcf/crosswalk-7.2.1-to-7.4.csv

Source: APQC Cross-Industry Process Classification Framework (PCF) version 7.4 (August 2024), categories 3.0 Market and
Sell Products and Services and 6.0 Manage Customer Service. The PCF is APQC's open standard, licensed for use and
derivative works with attribution (www.apqc.org/pcf). Element names are kept as APQC publishes them, so the Part III
label rules are not applied here; the domain assemblies carry clean labels and point to the element (dcterms:type).
"""
import argparse, collections, csv, datetime, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
VERSION = '0.2.0'
PCF = '7.4'
PREVIOUS = '7.2.1'
sys.path.insert(0, str(HERE))
import apqc_commercial as X
OWNER = {k: X.OWNERS[v] for k, v in X.OWNER.items()}   # owner of each element (longest prefix wins, D25)
LEVEL = {1: 'Category', 2: 'Process group', 3: 'Process', 4: 'Activity', 5: 'Task'}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--ingest', default=str(ROOT.parent / 'KE Workbench' / 'ingest'))
    ap.add_argument('--out', default=str(ROOT))
    a = ap.parse_args(argv)
    sys.path.insert(0, a.ingest)
    import ke_ingest as k
    cfg, _ = k.load_config(str(pathlib.Path(a.ingest) / 'ke-ingest.config.json'))
    base = cfg['baseUrl']; CORE = base + 'ontology/core/'
    ns = base + 'taxonomy/apqc-pcf/'
    t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    now = k.L(t.strftime('%Y-%m-%dT%H:%M:%SZ'), None, k.XSD + 'dateTime'); today = k.L(t.strftime('%Y-%m-%d'), None, k.XSD + 'date')
    rows = []
    for f in sorted(HERE.glob(f'apqc-pcf-{PCF}-category-*.txt')):
        for line in f.read_text(encoding='utf-8').splitlines():
            m = re.match(r'^(\d+(?:\.\d+)*) (.+) \((\d+)\)$', line.strip())
            if m: rows.append(m.groups())
    num2id = {n: i for n, _, i in rows}
    g = collections.OrderedDict()
    def add(s, p, o):
        g.setdefault(s, collections.OrderedDict()).setdefault(p, [])
        if o not in g[s][p]: g[s][p].append(o)
    def gov(s):
        add(s, k.OWL + 'versionInfo', k.L(VERSION)); add(s, CORE + 'hasLifecycleStatus', k.I(CORE + cfg['lifecycleStatus']))
        add(s, k.DCT + 'creator', k.L(cfg['author'])); add(s, k.DCT + 'created', today); add(s, k.DCT + 'modified', now)
    h = k.I(ns)
    title = 'APQC Process Classification Framework Taxonomy'
    add(h, k.RDF + 'type', k.I(k.SKOS + 'ConceptScheme'))
    for p in (k.RDFS + 'label', k.SKOS + 'prefLabel', k.DCT + 'title'): add(h, p, k.L(title, 'en'))
    add(h, k.SKOS + 'altLabel', k.L('APQC PCF Taxonomy', 'en'))
    add(h, k.DCT + 'description', k.L(f'The read-only reference registry of the APQC Cross-Industry Process Classification Framework (PCF) {PCF} (D25, D28). Each element keeps its APQC name, hierarchy number (skos:notation) and element ID (dct:identifier), names the one domain that owns it, and records whether a professional employer organization performs it. The domain assemblies classify their activities and steps by it (dcterms:type); the topology shows its process groups and processes as the levels above them. Internal domain services are built on it; external services follow the HR Services & PEO Enterprise Business Model instead.', 'en'))
    add(h, k.DCT + 'source', k.L(f'APQC Cross-Industry Process Classification Framework (PCF) version {PCF}, {X.PCF_DATE}: {X.PCF_URL} (Excel: {X.PCF_EXCEL_URL})'))
    add(h, k.DCT + 'rights', k.L(f'The Process Classification Framework is an open standard developed by APQC and is used here with attribution, under the license APQC grants for use, copies and derivative works. See {X.PCF_HOME}.', 'en'))
    add(h, k.DCT + 'replaces', k.I(ns + '0.1.0/'))
    add(h, k.DCT + 'publisher', k.I(cfg['publisher']))
    add(h, k.SKOS + 'editorialNote', k.L(f'Loaded: categories 3.0 Market and Sell Products and Services and 6.0 Manage Customer Service, PCF {PCF}. Element IDs are stable across releases; crosswalk-7.2.1-to-7.4.csv lists what changed from PCF {PREVIOUS}. APQC released PCF 8.0 on 2026-02-27: move to it when a copy is saved in Reference/apqc-pcf/source (open question 29). Load the other categories as their domains are modeled.', 'en'))
    add(h, k.SKOS + 'changeNote', k.L(f'0.2.0: PCF {PCF} ({X.PCF_DATE}) replaces PCF {PREVIOUS}; category 6.0 added for Domain Customer Care; each element records its PEO applicability (D28).', 'en'))
    add(h, k.OWL + 'versionIRI', k.I(ns + VERSION + '/'))
    add(h, k.DCT + 'identifier', k.L('taxonomy-apqc-pcf'))
    gov(h)
    def owner(n):
        best = max((x for x in OWNER if n == x or n.startswith(x + '.')), key=len)
        return OWNER[best]
    for n, name, pid in rows:
        x = k.I(ns + 'element-' + pid)
        depth = 1 if n.endswith('.0') and n.count('.') == 1 else len(n.split('.'))
        add(x, k.RDF + 'type', k.I(k.SKOS + 'Concept'))
        add(x, k.RDFS + 'label', k.L(name, 'en')); add(x, k.SKOS + 'prefLabel', k.L(name, 'en'))
        add(x, k.SKOS + 'notation', k.L(n)); add(x, k.DCT + 'identifier', k.L(pid))
        add(x, k.SKOS + 'scopeNote', k.L(f'APQC PCF {PCF} {LEVEL[depth].lower()}.', 'en'))
        add(x, k.SKOS + 'inScheme', h)
        if depth == 1:
            add(x, k.SKOS + 'topConceptOf', h); add(h, k.SKOS + 'hasTopConcept', x)
        else:
            parent = n.split('.')[0] + '.0' if depth == 2 else n.rsplit('.', 1)[0]
            px = k.I(ns + 'element-' + num2id[parent])
            add(x, k.SKOS + 'broader', px); add(px, k.SKOS + 'narrower', x)
        label, concept = owner(n)
        add(x, k.SKOS + 'related', k.I(base + 'taxonomy/' + concept))
        add(x, k.SKOS + 'editorialNote', k.L(f'Owner: {label}.', 'en'))
        na, ad = X.not_applicable(n), X.ADAPT.get(n)
        add(x, k.SKOS + 'note', k.L('PEO applicability: ' + ('Not applicable. ' + na if na else ('Adapted. ' + ad if ad else 'Applicable.')), 'en'))
        gov(x)
    pfx = {'core': CORE, 'rdf': k.RDF, 'rdfs': k.RDFS, 'owl': k.OWL, 'skos': k.SKOS, 'dct': k.DCT, 'xsd': k.XSD, 'apqc': ns,
           'commercialopstax': base + 'taxonomy/commercial-operations/', 'businessopstax': base + 'taxonomy/business-operations/'}
    w = k.Writer(pfx, [CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
    subjects = [h] + [s for s in g if s != h]
    head = (f'# {title}\n# {ns}  ·  version {VERSION}  ·  {cfg["lifecycleStatus"]}  ·  source APQC PCF {PCF} (read-only reference, D25)\n'
            f'# Generated by build_reference.py on {now[1]}\n# Standards: {cfg["standardsRef"]}\n')
    text = w.write(g, subjects, head)
    trig = w.write_trig(g, subjects, head.replace('\n# Standards', f'\n# Named graph: {ns}\n# Standards'), ns)
    k.parse_turtle(text)
    out = pathlib.Path(a.out) / 'Reference' / 'apqc-pcf'
    for sub, body in (('ttl', text), ('trig', trig)):
        (out / sub).mkdir(parents=True, exist_ok=True)
        (out / sub / f'taxonomy-apqc-pcf-{VERSION}.{sub}').write_text(body, encoding='utf-8')
    # crosswalk from the previous release, by element ID
    old = {}
    for line in (HERE / f'apqc-pcf-{PREVIOUS}-category-3.txt').read_text(encoding='utf-8').splitlines():
        m = re.match(r'^(\d+(?:\.\d+)*) (.+) \((\d+)\)$', line.strip())
        if m: old[m.group(3)] = (m.group(1), m.group(2))
    new = {pid: (n, name) for n, name, pid in rows}
    with (out / f'crosswalk-{PREVIOUS}-to-{PCF}.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['element_id', f'number_{PREVIOUS}', f'name_{PREVIOUS}', f'number_{PCF}', f'name_{PCF}', 'change'])
        for pid in sorted(set(old) | set(new), key=lambda i: (new.get(i) or old.get(i))[0].split('.') and [int(x) for x in (new.get(i) or old.get(i))[0].split('.')]):
            o, nw = old.get(pid), new.get(pid)
            if nw and not nw[0].startswith('3.'): continue
            ch = 'added' if not o else 'removed' if not nw else 'renumbered' if o[0] != nw[0] else 'renamed' if o[1] != nw[1] else 'unchanged'
            w.writerow([pid, o[0] if o else '', o[1] if o else '', nw[0] if nw else '', nw[1] if nw else '', ch])
    print(f'{len(rows)} APQC PCF {PCF} elements → {out}')


if __name__ == '__main__':
    sys.exit(main())
