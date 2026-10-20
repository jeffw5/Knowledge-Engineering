"""Change records (PROV-O, §3.3) for the changes made to the core set outside the KE Workbench on 2026-10-19.
They are written in the same form as ke_ingest.py's records, for the append-only graph …/graph/change-log,
and recorded after the fact: each says so in its description.

    python3 change_records.py <Baseline Core v1.0 folder>
"""
import pathlib, sys, datetime

BASE = 'https://www.insperity.com/'
LOG = BASE + 'graph/change-log'
OUT = pathlib.Path(sys.argv[1])
RECORDED = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
AUTHOR = 'Jeffrey Wallk'
ASSIST = 'Claude (AI assistant), at the direction of Jeffrey Wallk'

V18 = 'asset capability compliance domain event issue lifecycle location party persona process product requirements role rules services time valuestream'.split()
V_NEW = 'decision governance job logic measure policy value'.split()
T22 = 'asset capability compliance decision event governance issue lifecycle location logic measure party persona policy process product requirements role rules services time value'.split()
voc = lambda ds: [f'{BASE}vocabulary/core-{d}/' for d in ds]
tax = lambda ds: [f'{BASE}taxonomy/core-{d}/' for d in ds]
ONT, SHP, RX = BASE + 'ontology/core/', BASE + 'shapes/core/', BASE + 'reference/ro-extract/'
OLD_SHAPES = [f'{BASE}shapes/core-{d}/' for d in ('compliance', 'domain', 'party', 'process', 'product')]

RECORDS = [
 dict(stamp='2026-10-19T02:19:17Z', kind='core-ontology', label='Core domain ontology rebuilt on BFO 2020',
      desc='Workbench 2.2.0. The core domain ontology was rebuilt under ' + ONT + ' from the authored source ontology-core.source.ttl with build_core.py: '
           'every class specializes a BFO 2020 class and every relation a BFO, RO or IAO relation; it is anchored on the process step. '
           'Its SHACL shapes were rebuilt under ' + SHP + '. The core-domain ontology and the five core-* shapes graphs were superseded. '
           'core:formalizedBy was added to the top concepts of the 22 core taxonomies. The RO extract (0.1.0) was created as a reference module.',
      source=['ontology-core.source.ttl', 'shapes-core.source.ttl', 'formalized-by.csv', 'build_core.py'],
      used=[BASE + 'ontology/core-domain/'] + OLD_SHAPES + tax(T22),
      generated=[ONT, SHP, RX] + tax(T22),
      invalidated=[BASE + 'ontology/core-domain/'] + OLD_SHAPES,
      derived={ONT: [BASE + 'ontology/core-domain/'], SHP: OLD_SHAPES}),
 dict(stamp='2026-10-19T04:22:12Z', kind='cleanup', label='Other organization\'s content removed from the core set',
      desc='Verizon content was removed: 24 foreign individuals and datatypes from the compliance taxonomy; Verizon organization units '
           '(enterprise data and artificial intelligence, data and artificial intelligence governance, data and artificial intelligence and its '
           'hub-and-spoke unit, end to end governance, global network and technology) from the party vocabulary and taxonomy; Hum from the product '
           'vocabulary and taxonomy. The compliance and services taxonomy descriptions and the business unit definition were reworded without the '
           'company name; definitions were written for international standards organization, subsecond and relative. 0 blocking conformance errors remained.',
      source=['rewrite.py (one-off clean-up)'],
      used=tax(['compliance', 'services', 'product', 'party']) + voc(['party', 'product', 'time']),
      generated=tax(['compliance', 'services', 'product', 'party']) + voc(['party', 'product', 'time'])),
 dict(stamp='2026-10-19T04:33:03Z', kind='reorganization', label='KE Baseline split into Baseline Core v1.0 and Archive Baseline Core v0.1',
      desc='No asset content changed. KE Baseline was split into Baseline Core v1.0 (the ingestable vocabularies, taxonomies, core domain ontology and '
           'shapes, with BFO 2020 core, RO Core 2024-04-24 and the RO extract under reference/, and graphdb-rebuild.command) and Archive Baseline Core v0.1 '
           '(earlier ingestion reports, change records, review backups, superseded files and GraphDB backups).',
      source=['KE Baseline'], used=[], generated=[]),
 dict(stamp='2026-10-19T18:43:37Z', kind='primitives', label='Primitives backfill, hyphen-joined identifiers and relinking (Baseline Core v1.0)',
      desc='After a term-by-term review with Jeffrey Wallk (design decisions 1-30, review/design-decisions.md): 367 primitives were added to the core '
           'vocabularies (review/primitives-added.txt, registry review/primitives-v1.tsv), with seven new vocabularies (decision, governance, job, logic, '
           'measure, policy, value); job, journey and outcome moved from the requirements vocabulary to the job vocabulary, and the polymorphic job terms '
           'became concepts of the new core job taxonomy. Personas are no longer typed by role (seven engineering persona types and persona role removed); '
           'the product marketing lifecycle stages were removed. 912 taxonomy concept IRIs were changed to hyphen-joined words (§3.2 as amended); every one '
           'of the 922 concepts now carries dcterms:subject to each primitive it is built from and core:hasPrimaryTerm to its head primitive '
           '(review/concept-links.csv). review/crosswalk-v1.csv maps every old IRI to its new one or records its removal. Versions stay 0.1.0 (Draft).',
      source=['primitives-v1.tsv', 'm1_vocab.py', 'm2_taxonomy.py', 'design-decisions.md'],
      used=voc(V18) + tax(T22),
      generated=voc(V18 + V_NEW) + tax(T22 + ['job']),
      derived={f'{BASE}vocabulary/core-job/': [f'{BASE}vocabulary/core-requirements/'], f'{BASE}taxonomy/core-job/': [f'{BASE}vocabulary/core-requirements/']}),
 dict(stamp='2026-10-19T18:45:40Z', kind='core-ontology', label='Core domain ontology rebuilt to the asset and Jobs model (Baseline Core v1.0)',
      desc='The core domain ontology was rebuilt from ontology-core.source.ttl with build_core.py: 36 classes with hyphen-joined IRIs, all under BFO 2020; '
           'asset as the genus with product, service, offering and platform as assets assembled from other assets; lifecycles for every asset; the Jobs '
           'model (job, job step, desired outcome, delivered outcome); relations has component, lifecycle of, delivery of, delivers (property chain), '
           'addresses and supports; polymorphic classes kept only where they differ in BFO. Shapes rebuilt (13). core:formalizedBy re-pointed to the new '
           'class IRIs on the taxonomy top concepts (8 left for a modeling decision). RO extract 0.2.0 adds causally upstream of.',
      source=['ontology-core.source.ttl', 'shapes-core.source.ttl', 'formalized-by.csv', 'build_core.py', 'ro-extract.ttl'],
      used=[ONT, SHP, RX] + tax(T22),
      generated=[ONT, SHP, RX] + tax(T22)),
]


def q(v): return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'


def record(r):
    stamp = r['stamp'].replace(':', '')
    rid = f'{BASE}resource/change-log/ChangeRecord/{stamp}-{r["kind"]}'
    desc = r['desc'] + f' Changed outside the KE Workbench; recorded retrospectively on {RECORDED}.'
    body = [f'<{rid}> a prov:Activity , dct:ProvenanceStatement ;',
            f'  rdfs:label {q(r["label"] + ", " + r["stamp"])}@en ;',
            f'  dct:description {q(desc)}@en ;',
            f'  dct:creator {q(AUTHOR)} ;',
            f'  dct:contributor {q(ASSIST)} ;',
            f'  prov:startedAtTime "{r["stamp"]}"^^xsd:dateTime ;',
            f'  prov:endedAtTime "{r["stamp"]}"^^xsd:dateTime ;',
            f'  dct:date "{RECORDED}"^^xsd:dateTime ;',
            '  dct:source ' + ' ,\n    '.join(q(s) for s in r['source'])]
    if r['used']: body[-1] += ' ;'; body.append('  prov:used ' + ' ,\n    '.join(f'<{u}>' for u in sorted(set(r['used']))))
    if r['generated']: body[-1] += ' ;'; body.append('  prov:generated ' + ' ,\n    '.join(f'<{g}>' for g in sorted(set(r['generated']))))
    if r.get('invalidated'): body[-1] += ' ;'; body.append('  prov:invalidated ' + ' ,\n    '.join(f'<{g}>' for g in sorted(set(r['invalidated']))))
    body[-1] += ' .'
    for g in sorted(set(r['generated'])):
        der = r.get('derived', {}).get(g) or ([g] if g in r['used'] else [])
        body += ['', f'<{g}>', f'  prov:wasGeneratedBy <{rid}>' + (' ;' if der else ' .')]
        if der: body.append('  prov:wasDerivedFrom ' + ' , '.join(f'<{d}>' for d in der) + ' .')
    pre = (f'# Change record {stamp} for the {LOG} graph (append-only, §3.3)\n'
           f'# Recorded retrospectively on {RECORDED} for a change made outside the KE Workbench\n'
           '@prefix prov: <http://www.w3.org/ns/prov#> .\n@prefix dct: <http://purl.org/dc/terms/> .\n'
           '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n')
    ttl = pre + '\n'.join(body) + '\n'
    trig = pre + f'<{LOG}> {{\n\n' + '\n'.join(('  ' + l) if l else l for l in body) + '\n}\n'
    (OUT / 'ttl' / f'change-record-{stamp}.ttl').write_text(ttl, encoding='utf-8')
    (OUT / 'trig' / f'change-record-{stamp}.trig').write_text(trig, encoding='utf-8')
    return rid


for r in RECORDS:
    print(record(r))
