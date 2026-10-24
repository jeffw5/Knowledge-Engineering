#!/usr/bin/env python3
"""Build the Operations Dashboard snapshot: change log, asset inventory, conformance, decisions, releases and actions.

    python3 ingest/build_ops_snapshot.py          # from the "KE Workbench" folder (also run by the dashboard's Rebuild)

Reads   ../**/change-record-*.ttl              PROV-O change records written by every tool and build script
        ../KE Baseline/Baseline Core v1.0/ttl   the core assets
        ../KE Domains/**/ttl                    area, domain, reference and catalog assets (assemblies counted, not checked)
        data/c360/*.ttl                         Customer 360 schema and instances
        ../KE Domains/review/*.md, ../KE Baseline/Baseline Core v1.0/review/design-decisions.md
        assets/ke-releases.js, ingest/feedback/dispositions.jsonl, git history of the repository
        ingest/ops_spec.py                      guide retrofit items and process policies
Writes  data/ops/ops-snapshot.js                read by tools/operations-dashboard.html
        data/ops/history.jsonl                  one summary line per build, for trends
The dashboard merges change records it finds in GraphDB (…/graph/change-log) with the ones in the snapshot.
"""
import collections, datetime, glob, json, pathlib, re, subprocess, sys

WB = pathlib.Path(__file__).resolve().parent.parent
KE = WB.parent
sys.path.insert(0, str(WB / 'ingest'))
import ke_ingest as k
import ops_spec as SPEC

PROV = 'http://www.w3.org/ns/prov#'
DCT = 'http://purl.org/dc/terms/'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
OWL = 'http://www.w3.org/2002/07/owl#'
SKOS = 'http://www.w3.org/2004/02/skos/core#'
SH = 'http://www.w3.org/ns/shacl#'
AREAS = {'commercial-operations': 'Commercial Operations', 'business-operations': 'Business Operations',
         'hr-service-operations': 'HR Service Operations', 'technical-operations': 'Technical Operations'}
FOLDER_AREAS = {'Commercial Operations': 'Commercial Operations', 'Business Operations': 'Business Operations',
                'HR Service Operations': 'HR Service Operations', 'Technical Operations': 'Technical Operations'}
# domains that were renamed or moved; their old IRIs still appear in the change log
RETIRED = {'domain-commercial-operations': ('Commercial Operations', None), 'domain-customer-success': ('Commercial Operations', 'Customer Care'),
           'domain-pricing-and-contracts': ('Commercial Operations', 'Pricing'), 'domain-partner-and-channel': ('Commercial Operations', 'Sales.Partner & Channel')}
TOOLS = {'ingestion': 'Ingestion', 'review': 'Conformance review', 'editor': 'Model editor (vocabulary)',
         'ontology-editor': 'Model editor (ontology)', 'taxonomy-editor': 'Model editor (taxonomy)'}


def rel(p):
    try:
        return str(pathlib.Path(p).resolve().relative_to(KE))
    except ValueError:
        return str(p)


def lit(o):
    return o[1] if o and o[0] == 'L' else ''


# ---- scope of an IRI --------------------------------------------------------------------------------------
class Scopes:
    def __init__(self):
        self.domain_area = {}      # 'domain-sales' -> area name
        self.domain_label = {}     # 'domain-sales' -> 'Sales'
        self.c360 = set()

    def learn(self, iri, area, label):
        seg = self.segment(iri)
        if seg and seg.startswith('domain-'):
            self.domain_area[seg] = area
            if label: self.domain_label[seg] = label

    @staticmethod
    def segment(iri):
        m = re.match(r'https://www\.insperity\.com/(?:vocabulary|taxonomy|ontology|shapes|resource|record-graph|party-graph)/([^/#]+)', iri or '')
        return m.group(1) if m else None

    def of(self, iri):
        """(scope kind, area, domain) for an asset or term IRI."""
        if not iri: return ('other', None, None)
        if iri.startswith('http://purl.obolibrary.org/obo/'): return ('reference', 'Reference', 'BFO and RO')
        if iri in self.c360 or re.match(r'https://www\.insperity\.com/(ontology|vocabulary|resource|graph)/(jobs-to-be-done|outcome-|benchmark-|customer-360|appreciative|demand-|requirements-gateway|review-|survey-|inquiry-|evidence-|gateway-|outcome-review)', iri):
            return ('c360', 'Customer 360', 'Customer 360')
        seg = self.segment(iri)
        if seg is None:
            if '/graph/change-log' in iri or '/resource/change-log/' in iri: return ('log', 'Change log', None)
            return ('other', None, None)
        if seg == 'core' or seg.startswith('core-'): return ('core', 'Core', 'Core')
        if seg == 'apqc-pcf': return ('reference', 'Reference', 'APQC PCF')
        if seg == 'enterprise-services': return ('catalog', 'Enterprise Services', 'Service catalog')
        if seg in AREAS: return ('area', AREAS[seg], AREAS[seg] + ' (container)')
        if seg in RETIRED:
            a, d = RETIRED[seg]
            return ('domain', a, d or a + ' (container)')
        if seg.startswith('domain-'):
            area = self.domain_area.get(seg)
            label = self.domain_label.get(seg) or seg[7:].replace('.', '.').replace('-', ' ').title()
            return ('domain', area or 'Unassigned', label)
        return ('other', None, None)


# ---- change log -------------------------------------------------------------------------------------------
def change_records():
    files = [p for p in KE.glob('**/change-record-*.ttl') if '_to_delete' not in p.parts]
    S = collections.defaultdict(lambda: collections.defaultdict(list))
    origin = collections.defaultdict(set)
    for p in sorted(files):
        try:
            ts, _ = k.parse_turtle(p.read_text(encoding='utf-8'))
        except Exception as e:  # a broken file must not stop the dashboard
            print('  skipped', rel(p), e)
            continue
        for s, pr, o in ts:
            if s[0] != 'I': continue
            S[s[1]][pr[1]].append(o)
            if pr[1] == RDF + 'type' and o[1] == PROV + 'Activity':
                origin[s[1]].add(rel(p))
    recs, ents = [], {}
    for iri, e in S.items():
        types = {o[1] for o in e.get(RDF + 'type', [])}
        if PROV + 'Activity' in types:
            local = iri.rstrip('/').rsplit('/', 1)[-1]
            m = re.match(r'(\d{4}-?\d{2}-?\d{2}T?\d{0,6}Z?)-?(.*)', local)
            suffix = (m.group(2) if m else local) or 'ingestion'
            parts = []
            for po in e.get(DCT + 'hasPart', []):
                pe = S.get(po[1], {})
                parts.append({'label': lit((pe.get(RDFS + 'label') or [None])[0]), 'comment': lit((pe.get(RDFS + 'comment') or [None])[0]),
                              'subject': ((pe.get(DCT + 'subject') or [('', '')])[0])[1], 'type': lit((pe.get(DCT + 'type') or [None])[0])})
            sources = [lit(o) for o in e.get(DCT + 'source', [])]
            tool = TOOLS.get(suffix) or ('Migration' if any('m1_' in s or 'm2_' in s or 'migrat' in s for s in sources) else
                                         'Build' if any(s.startswith('build_') for s in sources) or suffix not in TOOLS else suffix)
            recs.append({
                'iri': iri, 'id': local, 'tool': tool, 'kind': suffix,
                'label': lit((e.get(RDFS + 'label') or [None])[0]), 'description': lit((e.get(DCT + 'description') or [None])[0]),
                'creator': [lit(o) or o[1] for o in e.get(DCT + 'creator', [])], 'contributor': [lit(o) for o in e.get(DCT + 'contributor', [])],
                'approvedBy': [o[1] for o in e.get('https://www.insperity.com/ontology/core/approvedBy', [])],
                'feature': [o[1] for o in e.get('https://www.insperity.com/ontology/core/implementsFeature', [])],
                'started': lit((e.get(PROV + 'startedAtTime') or e.get(DCT + 'date') or [None])[0]),
                'ended': lit((e.get(PROV + 'endedAtTime') or [None])[0]),
                'sources': sources, 'used': [o[1] for o in e.get(PROV + 'used', [])],
                'generated': [o[1] for o in e.get(PROV + 'generated', [])], 'invalidated': [o[1] for o in e.get(PROV + 'invalidated', [])],
                'parts': parts, 'files': sorted(origin[iri]), 'from': 'file'})
        elif PROV + 'Entity' in types and (e.get(PROV + 'wasDerivedFrom') or not e.get(DCT + 'subject')):
            ents[iri] = {'generatedBy': [o[1] for o in e.get(PROV + 'wasGeneratedBy', [])], 'derivedFrom': [o[1] for o in e.get(PROV + 'wasDerivedFrom', [])]}
    recs.sort(key=lambda r: r['started'] or r['id'])
    # an ingestion record lists its outputs as entities; fold the derivations into the record so the page needs one shape
    for r in recs:
        r['derivations'] = {g: ents[g]['derivedFrom'] for g in r['generated'] if g in ents and ents[g]['derivedFrom']}
    return recs, len(files)


# ---- asset inventory and conformance ------------------------------------------------------------------------
def asset_files():
    out = []
    for p in sorted((KE / 'KE Baseline/Baseline Core v1.0/ttl').glob('*.ttl')):
        if not p.name.startswith('change-record'): out.append((p, 'model'))
    for p in sorted((KE / 'KE Domains').glob('**/ttl/*.ttl')):
        if 'archive' in p.parts or 'change-log' in p.parts or p.name.startswith('change-record'): continue
        out.append((p, 'assembly' if 'assembly' in p.parts else 'model'))
    for p in sorted((WB / 'data/c360').glob('*.ttl')):
        out.append((p, 'c360'))
    return out


def area_of_path(p):
    parts = pathlib.Path(rel(p)).parts
    if parts[0] == 'KE Baseline': return 'Core'
    if parts[0] == 'KE Workbench': return 'Customer 360'
    if len(parts) > 1 and parts[1] in FOLDER_AREAS: return FOLDER_AREAS[parts[1]]
    if len(parts) > 1 and parts[1] == 'Reference': return 'Reference'
    if len(parts) > 1 and parts[1] == 'Enterprise Services': return 'Enterprise Services'
    return 'Other'


def inventory(scopes, cfg):
    files = asset_files()
    parsed = []
    vocab = set()
    for p, role in files:
        try:
            ts, _ = k.parse_turtle(p.read_text(encoding='utf-8'))
        except Exception as e:
            print('  skipped', rel(p), e); continue
        parsed.append((p, role, ts))
        if p.name.startswith('vocabulary-') or role == 'c360':
            for s, pr, o in ts:
                if pr[1] == RDF + 'type' and o[1] == SKOS + 'Concept': vocab.add(s[1])
    assets = []
    for p, role, ts in parsed:
        E = collections.defaultdict(lambda: collections.defaultdict(list))
        for s, pr, o in ts:
            if s[0] == 'I': E[s[1]][pr[1]].append(o)
        heads = [s for s, e in E.items() if any(o[1] in (OWL + 'Ontology', SKOS + 'ConceptScheme') for o in e.get(RDF + 'type', []))
                 and (e.get(OWL + 'versionInfo') or e.get(DCT + 'title') or e.get(RDFS + 'label'))]
        head = heads[0] if heads else None
        h = E.get(head, {})
        name = p.stem
        kind = next((x for x in ('vocabulary', 'taxonomy', 'ontology', 'shapes') if name.startswith(x + '-')), None)
        if role == 'assembly': kind = 'assembly'
        if role == 'c360': kind = kind or ('ontology' if OWL + 'Ontology' in {o[1] for o in h.get(RDF + 'type', [])} else 'vocabulary' if head else 'instances')
        if not kind: kind = 'other'
        title = lit((h.get(DCT + 'title') or h.get(SKOS + 'prefLabel') or h.get(RDFS + 'label') or [None])[0]) or name
        area = area_of_path(p)
        if role == 'c360' and head: scopes.c360.add(head)
        if head: scopes.learn(head, area, re.sub(r'^Domain (.+?) (Vocabulary|Taxonomy|Ontology|Shapes)$', r'\1', title) if title.startswith('Domain ') else None)
        cnt = collections.Counter()
        for s, e in E.items():
            ty = {o[1] for o in e.get(RDF + 'type', [])}
            if SKOS + 'Concept' in ty: cnt['concepts'] += 1
            if OWL + 'Class' in ty and s.startswith('https://www.insperity.com/'): cnt['classes'] += 1
            if ty & {OWL + 'ObjectProperty', OWL + 'DatatypeProperty'}: cnt['properties'] += 1
            if SH + 'NodeShape' in ty: cnt['shapes'] += 1
            if OWL + 'NamedIndividual' in ty: cnt['individuals'] += 1
        rules = {}
        sample = []
        if role != 'assembly' and kind in ('vocabulary', 'taxonomy', 'ontology', 'shapes'):
            try:
                _, res = k.check(ts, cfg.get('baseUrl', 'https://www.insperity.com/'), k.Policy(cfg), vocab)
            except Exception as e:
                res = {'Check failed': [('error', head or '', str(e))]}
            for rule, items in res.items():
                c = collections.Counter(sev for sev, _, _ in items)
                rules[rule] = {'error': c['error'], 'warn': c['warn'], 'info': c['info']}
                for sev, iri, msg in items[:3]:
                    if sev != 'info': sample.append({'rule': rule, 'sev': sev, 'iri': iri, 'msg': msg})
        status = (h.get('https://www.insperity.com/ontology/core/hasLifecycleStatus') or [('', '')])[0][1].rsplit('/', 1)[-1]
        assets.append({
            'iri': head or '', 'file': rel(p), 'name': name, 'kind': kind, 'role': role, 'title': title, 'area': area,
            'version': lit((h.get(OWL + 'versionInfo') or [None])[0]), 'status': status,
            'created': lit((h.get(DCT + 'created') or [None])[0]), 'modified': lit((h.get(DCT + 'modified') or [None])[0]),
            'conformsTo': [o[1] for o in h.get(DCT + 'conformsTo', [])], 'triples': len(ts), 'counts': dict(cnt),
            'rules': rules, 'errors': sum(v['error'] for v in rules.values()), 'warnings': sum(v['warn'] for v in rules.values()),
            'sample': sample[:12]})
    for a in assets:
        kind_, area_, dom_ = scopes.of(a['iri'])
        if a['role'] == 'c360': kind_, area_, dom_ = 'c360', 'Customer 360', 'Customer 360'
        a['scope'], a['scopeArea'], a['domain'] = kind_, area_ or a['area'], dom_ or a['area']
    return assets


# ---- decisions, questions, releases, dispositions, git -----------------------------------------------------
def decisions():
    out, qs = [], []
    p = KE / 'KE Domains/review/design-decisions.md'
    if p.exists():
        for m in re.finditer(r'^- \*\*(D\d+) · (.+?)\*\*(.*)$', p.read_text(encoding='utf-8'), re.M):
            when = re.search(r'(\d{4}-\d{2}-\d{2})', m.group(3))
            out.append({'id': m.group(1), 'title': m.group(2).rstrip('.'), 'date': when.group(1) if when else '', 'source': 'KE Domains/review/design-decisions.md'})
    p = KE / 'KE Baseline/Baseline Core v1.0/review/design-decisions.md'
    if p.exists():
        for m in re.finditer(r'^(\d+)\. (.+)$', p.read_text(encoding='utf-8'), re.M):
            t = re.sub(r'\*\*', '', m.group(2))
            out.append({'id': 'B' + m.group(1), 'title': (t[:157] + '…') if len(t) > 160 else t, 'date': '2026-10-19', 'source': 'KE Baseline/Baseline Core v1.0/review/design-decisions.md'})
    p = KE / 'KE Domains/review/open-questions.md'
    if p.exists():
        sec = ''
        for line in p.read_text(encoding='utf-8').splitlines():
            if line.startswith('## '): sec = line[3:].strip()
            m = re.match(r'^(\d+)\. \*\*(.+?)\*\*\s*(.*)$', line)
            if m:
                body = m.group(3)
                qs.append({'id': 'Q' + m.group(1), 'title': m.group(2).rstrip('.?') + ('?' if m.group(2).endswith('?') else ''), 'section': sec,
                           'detail': (body[:297] + '…') if len(body) > 300 else body})
    return out, qs


def js_literal(src):
    """A JavaScript array/object literal (bare keys, single or double quotes, comments) as Python data."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '/' and src[i:i + 2] == '/*':
            i = src.index('*/', i) + 2; continue
        if c == '/' and src[i:i + 2] == '//':
            i = src.index('\n', i); continue
        if c in '"\'':
            j, buf = i + 1, []
            while src[j] != c:
                if src[j] == '\\':
                    nxt = src[j + 1]
                    buf.append("'" if nxt == "'" else src[j:j + 2]); j += 2; continue
                buf.append('\\"' if src[j] == '"' else src[j]); j += 1
            out.append('"' + ''.join(buf) + '"'); i = j + 1
        elif c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalnum() or src[j] == '_'): j += 1
            w = src[i:j]
            out.append(w if w in ('true', 'false', 'null') else '"' + w + '"'); i = j
        else:
            out.append(c); i += 1
    return json.loads(re.sub(r',(\s*[\]}])', r'\1', ''.join(out)))


def releases():
    p = WB / 'assets/ke-releases.js'
    try:
        t = p.read_text(encoding='utf-8')
        data = js_literal(t[t.index('['):t.rindex(']') + 1])
    except Exception as e:
        print('  releases not read:', e); return []
    out = []
    for r in data:
        g = {x.get('kind'): len(x.get('items', [])) for x in r.get('groups', [])}
        out.append({'version': r.get('version'), 'date': r.get('date'), 'title': r.get('title'), 'counts': g})
    return out


def git_history(limit=400):
    def run(args):
        try:
            r = subprocess.run(['git', '-C', str(KE), 'log', f'-{limit}', '--date=iso-strict', '--pretty=format:@@%H|%ad|%s'] + args,
                               capture_output=True, text=True, timeout=60)
            return r.stdout if r.returncode == 0 else None
        except Exception:
            return None
    out = run(['--name-only']) or run([]) or ''
    commits = []
    for block in out.split('@@')[1:]:
        lines = [x for x in block.splitlines() if x.strip()]
        h, date, msg = lines[0].split('|', 2)
        areas = collections.Counter()
        for f in lines[1:]:
            parts = f.split('/')
            if parts[0] == 'KE Workbench': areas['Workbench' if not f.startswith('KE Workbench/data') else 'Workbench data'] += 1
            elif parts[0] == 'KE Baseline': areas['Core'] += 1
            elif parts[0] == 'KE Domains': areas[FOLDER_AREAS.get(parts[1], parts[1]) if len(parts) > 1 else 'KE Domains'] += 1
            else: areas['Other'] += 1
        models = sum(1 for f in lines[1:] if f.endswith(('.ttl', '.trig')) and not f.rsplit('/', 1)[-1].startswith('change-record'))
        commits.append({'hash': h[:8], 'date': date, 'message': msg, 'files': len(lines) - 1, 'areas': dict(areas), 'modelFiles': models})
    return commits


def guide_editions():
    eds = set()
    for d in (KE / 'Semantic Governance', WB / 'docs'):
        for p in d.glob('Semantic_Governance_v*'):
            m = re.search(r'v(\d+\.\d+)', p.name)
            if m: eds.add(m.group(1))
    return sorted(eds, key=lambda v: tuple(int(x) for x in v.split('.')))


# ---- actions ----------------------------------------------------------------------------------------------
def actions(recs, assets, qs, policy, expansion):
    A = []
    def add(id, cat, title, detail, prio, scope='', source='', count=1, link=''):
        A.append({'id': id, 'category': cat, 'title': title, 'detail': detail, 'priority': prio, 'scope': scope, 'source': source, 'count': count, 'link': link})
    # conformance: one action per rule and domain
    grp = collections.defaultdict(lambda: {'error': 0, 'warn': 0, 'assets': set()})
    for a in assets:
        for rule, c in a['rules'].items():
            if c['error'] or c['warn']:
                g = grp[(a['domain'], rule)]; g['error'] += c['error']; g['warn'] += c['warn']; g['assets'].add(a['name'])
    for (dom, rule), g in sorted(grp.items(), key=lambda x: (-x[1]['error'], -x[1]['warn'])):
        sev = 'high' if g['error'] else 'medium'
        add('C-' + re.sub(r'\W+', '-', (dom + '-' + rule).lower()).strip('-')[:60], 'Conformance',
            f'{rule}: {g["error"]} errors, {g["warn"]} warnings in {dom}',
            'Fix in Conformance Review or rebuild from the spec: ' + ', '.join(sorted(g['assets'])[:6]) + ('…' if len(g['assets']) > 6 else ''),
            sev, dom, 'Standards Conformance (ke_ingest.check)', g['error'] + g['warn'], 'tools/conformance-review.html')
    for p in policy:
        if p['status'] != 'pass':
            add('P-' + p['id'], 'Process policy', p['title'], p['finding'], p['priority'], 'All', p['standard'], p.get('failing', 1))
    for g in SPEC.GUIDE:
        add('G-' + g['id'], 'Standards guide', f'§{g["section"]} {g["topic"]}', g['change'], g['priority'], 'Guide', ', '.join(g['sources']), 1)
    for q in qs:
        add(q['id'], 'Decision', q['title'], q['detail'], 'medium', q['section'], 'KE Domains/review/open-questions.md')
    drafts = [a for a in assets if a['status'] in ('Draft', '') and a['kind'] in ('vocabulary', 'taxonomy', 'ontology', 'shapes')]
    if drafts:
        add('L-candidate', 'Lifecycle', f'{len(drafts)} assets are Draft; define Candidate criteria and promote the core',
            'No asset has reached Candidate. Agree the entry criteria (guide item G12), then promote Baseline Core v1.0 first, since every domain pins it.', 'high', 'All', '§3.3 Lifecycle Management', len(drafts))
    if expansion:
        add('X-service-map', 'Portfolio', f'Decide the {expansion} PEO Service Map expansion proposals', 'Business and compliance decision on each proposed L3 service, domain and service line (Products & Services › PEO Service Map › Expansion).',
            'medium', 'HR Service Operations', 'KE Domains/_build/service_map_expansion.py', expansion, 'tools/peo-service-map.html')
    return A


def policies(recs, assets, editions):
    touched = set()
    for r in recs:
        touched.update(r['generated']); touched.update(r['used']); touched.update(r['invalidated'])
        touched.update(p['subject'] for p in r['parts'])
    models = [a for a in assets if a['kind'] in ('vocabulary', 'taxonomy', 'ontology', 'shapes') and a['iri']]
    untracked = [a['name'] for a in models if a['iri'] not in touched]
    latest = editions[-1] if editions else SPEC.GUIDE_EDITION
    stale = [a['name'] for a in models if a['conformsTo'] and not any(latest in c for c in a['conformsTo'])]
    nocl = [a['name'] for a in models if not a['conformsTo']]
    by_iri = collections.defaultdict(set)
    for a in models: by_iri[a['iri']].add((a['version'], a['file']))
    dups = {i: v for i, v in by_iri.items() if len({x[0] for x in v}) > 1}
    beyond = [a for a in models if a['status'] not in ('Draft', '')]
    n = len(recs)
    def res(id, failing, total, finding):
        s = SPEC.POLICIES[[p['id'] for p in SPEC.POLICIES].index(id)]
        return dict(s, total=total, failing=failing, passing=total - failing, status='pass' if failing == 0 else 'fail', finding=finding)
    return [
        res('P01', len(untracked), len(models), f'{len(untracked)} of {len(models)} current model assets appear in no change record' + (': ' + ', '.join(untracked[:8]) + ('…' if len(untracked) > 8 else '') if untracked else '.')),
        res('P02', sum(1 for r in recs if not r['creator']), n, f'{sum(1 for r in recs if not r["creator"])} of {n} records have no dcterms:creator.'),
        res('P03', sum(1 for r in recs if not r['approvedBy']), n, f'{sum(1 for r in recs if not r["approvedBy"])} of {n} records name no approver. The tools do not write core:approvedBy yet (guide item G09).'),
        res('P04', sum(1 for r in recs if not r['feature']), n, f'{sum(1 for r in recs if not r["feature"])} of {n} records trace to no requirement or demand request.'),
        res('P05', 1, 1, 'No deployment record is written when graphs are loaded (graphdb-load.command, graphdb-rebuild.command, Load into GraphDB).'),
        res('P06', sum(1 for r in recs if not r['ended']), n, f'{sum(1 for r in recs if not r["ended"])} of {n} records have no prov:endedAtTime.'),
        res('P07', len(stale) + len(nocl), len(models), f'Latest guide edition on disk is v{latest}. {len(stale)} assets claim an older edition and {len(nocl)} claim none. After v{SPEC.GUIDE_NEXT} is published every asset will need rebuilding.'),
        res('P08', len(dups), len(by_iri), f'{len(dups)} asset IRIs have current copies at different versions: ' + '; '.join(f'{i.rsplit("/", 2)[-2]} ({", ".join(sorted(v for v, _ in vs))})' for i, vs in list(dups.items())[:6])),
        res('P09', len(models) - len(beyond), len(models), f'{len(models) - len(beyond)} of {len(models)} model assets are Draft.'),
    ], untracked, dups


def main():
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')
    cfg, _ = k.load_config(str(WB / 'ingest/ke-ingest.config.json'))
    scopes = Scopes()
    assets = inventory(scopes, cfg)            # first, so domain IRIs map to their areas
    recs, nfiles = change_records()
    for r in recs:
        r['scopes'] = sorted({' › '.join(x for x in scopes.of(i)[1:3] if x) for i in r['generated'] + r['invalidated'] + [p['subject'] for p in r['parts']] if scopes.of(i)[1]})
    dec, qs = decisions()
    eds = guide_editions()
    pol, untracked, dups = policies(recs, assets, eds)
    exp = 0
    sm = KE / 'KE Domains/HR Service Operations/peo-service-map/peo-service-map.json'
    if sm.exists():
        try: exp = len(json.loads(sm.read_text(encoding='utf-8')).get('expansion', {}).get('proposals', []))
        except Exception: pass
    acts = actions(recs, assets, qs, pol, exp)
    disp = k.load_feedback()
    scope_iri = {}
    for r in recs:
        for i in set(r['generated'] + r['used'] + r['invalidated'] + [p['subject'] for p in r['parts']]):
            if i and i not in scope_iri: scope_iri[i] = scopes.of(i)
    data = {
        'generated': now, 'workbench': WB.name, 'guide': {'edition': SPEC.GUIDE_EDITION, 'next': SPEC.GUIDE_NEXT, 'editionsOnDisk': eds, 'items': SPEC.GUIDE},
        'changeLog': {'records': recs, 'files': nfiles, 'graph': cfg.get('baseUrl', 'https://www.insperity.com/') + 'graph/change-log'},
        'scopeOf': {i: list(v) for i, v in scope_iri.items()},
        'domainMap': dict({s: [scopes.domain_area.get(s), scopes.domain_label.get(s)] for s in scopes.domain_area},
                          **{s: [a_, d_] for s, (a_, d_) in RETIRED.items()}),
        'areas': AREAS,
        'assets': assets, 'policies': pol, 'decisions': dec, 'questions': qs, 'releases': releases(), 'git': git_history(),
        'dispositions': [{'at': d.get('at') or d.get('recorded'), 'disposition': d.get('disposition'), 'rules': [f.get('rule') for f in d.get('findings') or []],
                          'term': (d.get('term') or {}).get('iri'), 'source': d.get('source')} for d in disp],
        'actions': acts, 'categories': SPEC.CATEGORIES,
        'sources': {'changeRecords': 'change-record-*.ttl under ' + KE.name, 'core': 'KE Baseline/Baseline Core v1.0/ttl', 'domains': 'KE Domains/**/ttl', 'c360': 'KE Workbench/data/c360'}}
    out = WB / 'data/ops'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'ops-snapshot.js').write_text('/* Generated by ingest/build_ops_snapshot.py; do not edit by hand. */\nwindow.KE_OPS = ' +
                                         json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    models = [a for a in assets if a['kind'] in ('vocabulary', 'taxonomy', 'ontology', 'shapes')]
    by = collections.defaultdict(lambda: {'assets': 0, 'terms': 0, 'errors': 0, 'warnings': 0})
    for a in models:
        b = by[a['domain']]; b['assets'] += 1; b['terms'] += a['counts'].get('concepts', 0) + a['counts'].get('classes', 0)
        b['errors'] += a['errors']; b['warnings'] += a['warnings']
    line = {'at': now, 'records': len(recs), 'assets': len(models), 'errors': sum(a['errors'] for a in models),
            'warnings': sum(a['warnings'] for a in models), 'actions': len(acts), 'byDomain': by}
    with open(out / 'history.jsonl', 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + '\n')
    hist = [json.loads(x) for x in (out / 'history.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    (out / 'history.js').write_text('window.KE_OPS_HISTORY = ' + json.dumps(hist[-200:], ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf-8')
    summary = {'records': len(recs), 'recordFiles': nfiles, 'assets': len(assets), 'models': len(models),
               'errors': line['errors'], 'warnings': line['warnings'], 'actions': len(acts), 'policiesFailing': sum(1 for p in pol if p['status'] != 'pass')}
    print(json.dumps(summary))
    return summary


if __name__ == '__main__':
    main()
