#!/usr/bin/env python3
"""Build the PEO Service Map: the external services of HR Service Operations joined to the questions customers ask.

    python3 _build/build_service_map.py            # from the "KE Domains" folder

Structure (D25, D26): HR Service Operations > L1 domain > L2 bounded context > L3 domain service, each L3 service
also filed under the service line a client buys it in.
Demand side (Customer 360): persona > job to be done > job map stage > desired outcome. Every desired outcome is
turned into the question a persona asks while getting the job done, and answered by the L3 services that address it
(jtbd:isAddressedByService).

Reads   HR Service Operations/hr-service-operations/ttl/taxonomy-hr-service-operations-*.ttl   (the L1 domains)
        Reference/hr-services-business-model/business-model-structure.json                    (L2 and L3, service lines)
        ../KE Workbench/data/c360/*.ttl                                                        (personas, jobs, outcomes)
Writes  HR Service Operations/peo-service-map/peo-service-map.json, coverage-report.md, README.md
        ../KE Workbench/data/peo-service-map/peo-service-map.js   (read by tools/peo-service-map.html)

L2 and L3 IRIs follow the D26 pattern (.../taxonomy/domain-<L1>.<L2>.<L3>/) and are marked planned: they are minted
when the business model is ingested (open question 27).
"""
import collections, datetime, glob, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WB = ROOT.parent / 'KE Workbench'
sys.path.insert(0, str(WB / 'ingest'))
import ke_ingest as k

BASE = 'https://www.insperity.com/'
J = BASE + 'ontology/jobs-to-be-done/'
SK = 'http://www.w3.org/2004/02/skos/core#'
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
VERSION = '0.1.0'

# business-model L1 id -> HR Service Operations taxonomy concept (the same eight domains, D26)
L1 = {
    'WorkforceAdminDomain': 'workforce-administration-and-payroll-domain',
    'BenefitsRetirementDomain': 'employee-benefits-and-retirement-sponsorship-domain',
    'ComplianceRiskDomain': 'government-compliance-and-employer-risk-management-domain',
    'TalentManagementDomain': 'talent-management-and-organizational-development-domain',
    'ClientRelationshipDomain': 'client-relationship-and-business-development-domain',
    'HRTechnologyPlatformDomain': 'hr-technology-platform-and-employee-experience-domain',
    'WorkforceDevelopmentDomain': 'workforce-development-coaching-and-performance-measurement-domain',
    'ValuesCultureStewardshipDomain': 'organizational-values-culture-and-ethics-stewardship-domain',
}


def slug(s):
    s = s.replace('&', ' and ')
    s = re.sub(r"['’]", '', s)
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def load_ttl(paths):
    S = collections.defaultdict(lambda: collections.defaultdict(list))
    for p in paths:
        ts, _ = k.parse_turtle(open(p, encoding='utf-8').read())
        for s, pr, o in ts:
            if s[0] == 'I':
                S[s[1]][pr[1]].append(o)
    return S


def one(S, s, p):
    v = S[s].get(p) or [] if s in S else []
    en = [x for x in v if x[0] == 'L' and len(x) > 2 and x[2] == 'en']
    x = (en or v or [None])[0]
    return x[1] if x else ''


def many(S, s, p):
    return [x[1] for x in S[s].get(p, [])] if s in S else []


RULES = [
    (r'^Minimize the time required to (.+)$', 'How quickly can you help me {0}?'),
    (r'^Minimize the time required for (.+)$', 'How do you shorten the time it takes for {0}?'),
    (r'^Minimize the total elapsed time (.+)$', 'How do you shorten the total time {0}?'),
    (r'^Minimize the time (.+)$', 'How do you shorten the time {0}?'),
    (r'^Minimize the likelihood (that|of) (.+)$', 'How do you reduce the chance {0} {1}?'),
    (r'^Minimize the number of (.+)$', 'How do you reduce the number of {0}?'),
    (r'^Minimize the (.+)$', 'How do you keep down the {0}?'),
    (r'^(?:Maximize|Increase) the (.+)$', 'How do you increase the {0}?'),
]


def question(stmt):
    s = stmt.strip().rstrip('.')
    for rx, tpl in RULES:
        m = re.match(rx, s)
        if m:
            return tpl.format(*m.groups())
    return 'How do you help me ' + s[0].lower() + s[1:] + '?'


def main():
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    tax = sorted(glob.glob(str(ROOT / 'HR Service Operations/hr-service-operations/ttl/taxonomy-hr-service-operations-*.ttl')))[-1]
    T = load_ttl([tax])
    TX = BASE + 'taxonomy/hr-service-operations/'
    bm = json.load(open(ROOT / 'Reference/hr-services-business-model/business-model-structure.json', encoding='utf-8'))
    area = {'iri': TX, 'label': one(T, TX, SK + 'prefLabel') or 'Human Resources Service Operations Taxonomy',
            'name': 'Human Resources Service Operations', 'alt': 'HR Service Operations', 'taxonomy': pathlib.Path(tax).name}

    # supply side
    domains, d_by = [], {}
    for d in sorted(bm['domains'], key=lambda x: x['number']):
        iri = TX + L1[d['id']]
        assert iri in T, iri + ' is not in ' + tax
        l1slug = L1[d['id']][:-len('-domain')]
        x = {'id': d['id'], 'n': d['number'], 'iri': iri, 'label': d['label'], 'prefLabel': one(T, iri, SK + 'prefLabel'),
             'definition': one(T, iri, SK + 'definition'), 'plannedTaxonomy': BASE + 'taxonomy/domain-' + l1slug + '/', 'contexts': []}
        domains.append(x)
        d_by[d['id']] = x
    lines = collections.OrderedDict((l['label'], dict(l, services=[])) for l in bm['serviceLines'])
    ctx_by, services = collections.OrderedDict(), collections.OrderedDict()
    for s in bm['services']:
        d = d_by[s['domain']]
        c = ctx_by.get(s['boundedContext'])
        if not c:
            c = {'id': s['boundedContext'], 'label': s['boundedContextLabel'], 'domain': d['id'],
                 'plannedTaxonomy': d['plannedTaxonomy'][:-1] + '.' + slug(s['boundedContextLabel']) + '/', 'services': []}
            ctx_by[c['id']] = c
            d['contexts'].append(c['id'])
        sv = {'id': s['id'], 'label': s['label'], 'context': c['id'], 'domain': d['id'], 'line': s['serviceLine'],
              'bm': bm['namespace'] + s['id'],
              'plannedTaxonomy': c['plannedTaxonomy'][:-1] + '.' + slug(re.sub(r'\s+Service$', '', s['label'])) + '/',
              'questions': [], 'jobs': [], 'personas': []}
        services[s['id']] = sv
        c['services'].append(s['id'])
        lines[s['serviceLine']]['services'].append(s['id'])

    # demand side (Customer 360)
    C = load_ttl(sorted(glob.glob(str(WB / 'data/c360/*.ttl'))))

    def typed(t):
        return [s for s in list(C) if any(o[0] == 'I' and o[1] == t for o in C[s].get(RDF + 'type', []))]

    stages = {}
    for s in typed(J + 'job-map-stage'):
        stages[s] = {'id': one(C, s, J + 'hasIdentifier'), 'label': one(C, s, SK + 'prefLabel'),
                     'order': int(one(C, s, J + 'hasStepOrder') or 99), 'definition': one(C, s, SK + 'definition')}
    personas = []
    for s in typed(J + 'client-persona'):
        personas.append({'iri': s, 'id': one(C, s, J + 'hasIdentifier'), 'label': one(C, s, SK + 'prefLabel'),
                         'short': one(C, s, J + 'hasShortName'), 'definition': one(C, s, SK + 'definition'),
                         'context': one(C, s, J + 'hasPersonaContext'), 'buying': one(C, s, J + 'hasBuyingRole'),
                         'goal': one(C, s, J + 'hasPersonaGoal'), 'emotional': many(C, s, J + 'hasEmotionalJob'),
                         'titles': one(C, s, J + 'hasTypicalTitles'), 'executes': [], 'participates': []})
    personas.sort(key=lambda p: p['id'])
    p_by = {p['iri']: p for p in personas}
    p_id = {p['id']: p for p in personas}
    jobs, j_by = [], {}
    for kind, t in (('core', 'core-functional-job'), ('chain', 'consumption-chain-job')):
        for s in typed(J + t):
            x = {'iri': s, 'id': one(C, s, J + 'hasIdentifier'), 'kind': kind,
                 'statement': one(C, s, J + 'hasJobStatement') or one(C, s, SK + 'prefLabel'),
                 'executors': [p_by[i]['id'] for i in many(C, s, J + 'hasJobExecutor') if i in p_by],
                 'participants': [p_by[i]['id'] for i in many(C, s, J + 'hasJobParticipant') if i in p_by],
                 'domains': [i.split('#')[-1] for i in many(C, s, J + 'appliesToBusinessDomain')],
                 'outcomes': [], 'services': []}
            x['question'] = 'Can you help me ' + x['statement'][0].lower() + x['statement'][1:] + '?'
            jobs.append(x)
            j_by[s] = x
    for p in personas:
        for s in many(C, p['iri'], J + 'executesJob'):
            if s in j_by and p['id'] not in j_by[s]['executors']:
                j_by[s]['executors'].append(p['id'])
        for s in many(C, p['iri'], J + 'participatesInJob'):
            if s in j_by and p['id'] not in j_by[s]['participants'] and p['id'] not in j_by[s]['executors']:
                j_by[s]['participants'].append(p['id'])
    jobs.sort(key=lambda j: (0 if j['kind'] == 'core' else 1, j['id']))
    for j in jobs:
        for pid in j['executors']:
            p_id[pid]['executes'].append(j['id'])
        for pid in j['participants']:
            if j['id'] not in p_id[pid]['executes']:
                p_id[pid]['participates'].append(j['id'])

    questions = []
    for s in typed(J + 'desired-outcome'):
        oid = one(C, s, J + 'hasIdentifier')
        stmt = one(C, s, J + 'hasOutcomeStatement') or one(C, s, SK + 'prefLabel')
        job = next((j_by[i] for i in many(C, s, J + 'isOutcomeOfJob') if i in j_by), None)
        if not job:
            job = next((j for j in jobs if s in many(C, j['iri'], J + 'hasDesiredOutcome')), None)
        st = stages.get((many(C, s, J + 'occursAtJobStep') or [''])[0], {})
        svc = [i.split('#')[-1] for i in many(C, s, J + 'isAddressedByService')]
        q = {'id': oid, 'outcome': stmt, 'question': question(stmt), 'job': job['id'] if job else '', 'stage': st.get('id', ''),
             'metric': ((many(C, s, J + 'hasOutcomeMetricType') or [''])[0]).rstrip('/').split('/')[-1],
             'services': [i for i in svc if i in services], 'unknownServices': [i for i in svc if i not in services]}
        questions.append(q)
        if job:
            job['outcomes'].append(oid)
            for i in q['services']:
                if i not in job['services']:
                    job['services'].append(i)
        for i in q['services']:
            sv = services[i]
            sv['questions'].append(oid)
            if job and job['id'] not in sv['jobs']:
                sv['jobs'].append(job['id'])
            for pid in (job['executors'] + job['participants']) if job else []:
                if pid not in sv['personas']:
                    sv['personas'].append(pid)
    questions.sort(key=lambda q: q['id'])
    for j in jobs:
        j['outcomes'].sort()
    for sv in services.values():
        sv['personas'].sort()
        sv['questions'].sort()

    data = {'title': 'PEO Service Map', 'version': VERSION, 'status': 'Draft', 'generated': now,
            'sources': {'area': 'KE Domains/HR Service Operations/hr-service-operations/ttl/' + area['taxonomy'],
                        'structure': 'KE Domains/Reference/hr-services-business-model/business-model-structure.json',
                        'demand': 'KE Workbench/data/c360/ (Customer 360 personas, jobs and desired outcomes)'},
            'area': area, 'stages': sorted(stages.values(), key=lambda s: s['order']),
            'serviceLines': list(lines.values()), 'domains': domains, 'contexts': list(ctx_by.values()),
            'services': list(services.values()), 'personas': personas, 'jobs': jobs, 'questions': questions}
    out = ROOT / 'HR Service Operations/peo-service-map'
    out.mkdir(parents=True, exist_ok=True)
    market_report = market(data, services, ctx_by, d_by, lines, questions, out, now)
    js = json.dumps(data, ensure_ascii=False, indent=1)
    (out / 'peo-service-map.json').write_text(js + '\n', encoding='utf-8')
    w = WB / 'data/peo-service-map'
    w.mkdir(parents=True, exist_ok=True)
    (w / 'peo-service-map.js').write_text('/* Generated by KE Domains/_build/build_service_map.py; do not edit by hand. */\n'
                                          'window.PEO_SERVICE_MAP = ' + js + ';\n', encoding='utf-8')

    # coverage report
    noans = [q for q in questions if not q['services']]
    idle = [s for s in services.values() if not s['questions']]
    unk = sorted({u for q in questions for u in q['unknownServices']})
    L = ['# PEO Service Map %s: coverage report' % VERSION, '', 'Generated %s.' % now, '',
         '- %d L1 domains, %d L2 bounded contexts, %d L3 domain services, %d service lines' % (len(domains), len(ctx_by), len(services), len(lines)),
         '- %d personas, %d jobs, %d customer questions (one per desired outcome) plus %d headline job questions' % (len(personas), len(jobs), len(questions), len(jobs)),
         '- %d questions answered by at least one service; %d with no service' % (len(questions) - len(noans), len(noans)),
         '- %d services answer at least one question; %d answer none yet' % (len(services) - len(idle), len(idle)), '']
    if unk:
        L += ['## Services named by outcomes but missing from the business model', ''] + ['- ' + u for u in unk] + ['']
    L += ['## Questions with no service', ''] + (['- %s (%s): %s' % (q['id'], q['job'], q['question']) for q in noans] or ['None.']) + ['']
    L += ['## Services that no customer question reaches yet', ''] + (['- %s (%s)' % (s['label'], ctx_by[s['context']]['label']) for s in idle] or ['None.']) + ['']
    L += ['## Questions per persona', '', '| Persona | Jobs (executes / takes part) | Questions | Answered |', '|---|---|---:|---:|']
    for p in personas:
        js_ = set(p['executes'] + p['participates'])
        qs = [q for q in questions if q['job'] in js_]
        L.append('| %s | %d / %d | %d | %d |' % (p['label'], len(p['executes']), len(p['participates']), len(qs), sum(1 for q in qs if q['services'])))
    (out / 'coverage-report.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    (out / 'README.md').write_text(README.replace('{VERSION}', VERSION), encoding='utf-8')
    print('\n'.join(L[4:8]))
    print('unknown services:', unk)
    print(market_report)


# ---- market crosswalk and expansion (service_map_expansion.py + tools/peo-service-landscape.html) ------------

def js_literal_to_json(src):
    """Turn a JavaScript array/object literal with bare keys into JSON (strings, numbers, true/false/null)."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in '"\'':
            j, buf = i + 1, []
            while src[j] != c:
                if src[j] == '\\':
                    buf.append(src[j:j + 2]); j += 2; continue
                buf.append('\\"' if src[j] == '"' else src[j]); j += 1
            out.append('"' + ''.join(buf) + '"'); i = j + 1
        elif c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalnum() or src[j] == '_'):
                j += 1
            w = src[i:j]
            out.append(w if w in ('true', 'false', 'null') else '"' + w + '"'); i = j
        else:
            out.append(c); i += 1
    s = ''.join(out)
    s = re.sub(r',(\s*[\]}])', r'\1', s)
    return json.loads(s)


def load_landscape():
    p = WB / 'tools/peo-service-landscape.html'
    t = p.read_text(encoding='utf-8')
    grab = lambda name, end: js_literal_to_json(re.search(r'const ' + name + r'=(.*?)' + end, t, re.S).group(1))
    co = grab('CO', r';\s*\nconst DOM=')
    dom = grab('DOM', r';\s*\n')
    rows = grab('R', r';\s*\nconst LBL=')
    lbl = grab('LBL', r';\s*\n')
    return co, dom, rows, lbl


def market(data, services, ctx_by, d_by, lines, questions, out, now):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import service_map_expansion as X
    co, dom, rows, lbl = load_landscape()
    comp = [{'key': c['k'], 'name': c['n'], 'tag': c['s'], 'base': bool(c.get('base'))} for c in co]
    keys = [c['key'] for c in comp]
    qby = {q['id']: q for q in questions}
    errs = []

    def rating(r, k):
        v = (r[3].get(k) or 'V|').split('|', 1)
        return {'l': v[0], 'n': v[1] if len(v) > 1 else ''}

    # proposals first, so crosswalk rows can point at the proposals that fill their gaps
    newctx = {c[0]: {'id': c[0], 'label': c[1], 'domain': c[2], 'proposed': True, 'proposals': []} for c in X.NEW_CONTEXTS}
    newdom = {d[0]: {'id': d[0], 'n': d[1], 'label': d[2], 'definition': d[3], 'proposed': True, 'contexts': []} for d in X.NEW_DOMAINS}
    for c in newctx.values():
        if c['domain'] in newdom:
            newdom[c['domain']]['contexts'].append(c['id'])
        elif c['domain'] not in d_by:
            errs.append('new context %s: unknown domain %s' % (c['id'], c['domain']))
    linenames = set(lines) | {l[1] for l in X.NEW_LINES}
    rowids = {r[0] for r in rows}
    thin = {q['id'] for q in questions if len(q['services']) <= 1}
    props = []
    for p in X.PROPOSALS:
        p = dict(p)
        ctx = p['context']
        if ctx in ctx_by:
            p['domain'] = ctx_by[ctx]['domain']; p['contextIsNew'] = False
        elif ctx in newctx:
            p['domain'] = newctx[ctx]['domain']; p['contextIsNew'] = True; newctx[ctx]['proposals'].append(p['id'])
        else:
            errs.append('%s: unknown context %s' % (p['id'], ctx))
        if p['line'] not in linenames: errs.append('%s: unknown service line %s' % (p['id'], p['line']))
        for r in p['rows']:
            if r not in rowids: errs.append('%s: unknown landscape row %s' % (p['id'], r))
        for o in p['addresses']:
            if o not in qby: errs.append('%s: unknown outcome %s' % (p['id'], o))
        for e in p['enablers']:
            if e not in X.ENABLERS: errs.append('%s: unknown enabler %s' % (p['id'], e))
        for e in p['evidence']:
            if e not in X.EVIDENCE: errs.append('%s: unknown evidence %s' % (p['id'], e))
        if p['extends'] and p['extends'] not in services: errs.append('%s: extends unknown %s' % (p['id'], p['extends']))
        offered = set(p['competitors'])
        for r in rows:  # a row counts only when the proposal fills all of it (the crosswalk found no service)
            if r[0] in p['rows'] and X.CROSSWALK.get(r[0], ([], ''))[1] == 'none' and p['origin'] != 'semantic':
                offered |= {k for k in keys if k != 'nsp' and rating(r, k)['l'] in 'CAP'}
        p['offeredBy'] = sorted(offered, key=keys.index)
        p['insperity'] = [rating(r, 'nsp') for r in rows if r[0] in p['rows']]
        p['thinAddressed'] = sorted(o for o in p['addresses'] if o in thin)
        p['personas'] = sorted({pid for o in p['addresses'] if o in qby for j in data['jobs'] if j['id'] == qby[o]['job'] for pid in j['executors'] + j['participants']})
        props.append(p)
    pby_row = collections.defaultdict(list)
    for p in props:
        for r in p['rows']:
            pby_row[r].append(p['id'])

    # crosswalk
    xw = []
    for r in rows:
        svc, fit, gap = X.CROSSWALK.get(r[0], ([], 'unmapped', ''))
        if r[0] not in X.CROSSWALK: errs.append('landscape row %s is not in the crosswalk' % r[0])
        for s in svc:
            if s not in services: errs.append('crosswalk %s: unknown service %s' % (r[0], s))
        ratings = {k: rating(r, k) for k in keys}
        others = [k for k in keys if k != 'nsp' and ratings[k]['l'] in 'CAP']
        xw.append({'id': r[0], 'group': r[1], 'groupLabel': dom.get(r[1], r[1]), 'label': r[2], 'ratings': ratings, 'services': svc,
                   'fit': fit, 'gap': gap, 'proposals': pby_row.get(r[0], []), 'competitorsOffering': others})
        for s in svc:
            if s in services:
                services[s].setdefault('market', []).append(r[0])
    for s in services.values():
        s.setdefault('market', [])

    data['market'] = {
        'companies': comp, 'levels': lbl, 'groups': dom, 'crosswalk': xw,
        'delivery': [{'id': d[0], 'label': d[1], 'rows': d[2], 'insperityOffer': d[3], 'note': d[4],
                      'ratings': {k: rating(next(r for r in rows if r[0] == d[2][0]), k) for k in keys}} for d in X.DELIVERY],
        'source': 'KE Workbench/tools/peo-service-landscape.html (public sources as of 2026-10-23)'}
    data['expansion'] = {
        'lines': [{'id': l[0], 'label': l[1], 'description': l[2], 'proposed': True} for l in X.NEW_LINES],
        'domains': list(newdom.values()), 'contexts': list(newctx.values()), 'proposals': props,
        'enablers': {k: {'label': v[0], 'description': v[1]} for k, v in X.ENABLERS.items()},
        'evidence': {k: {'title': v[0], 'url': v[1]} for k, v in X.EVIDENCE.items()},
        'source': 'KE Domains/_build/service_map_expansion.py'}
    if errs:
        raise SystemExit('expansion spec errors:\n  ' + '\n  '.join(errs))

    # report
    cnt = collections.Counter(x['fit'] for x in xw)
    byo = collections.Counter(p['origin'] for p in props)
    byr = collections.Counter(p['rec'] for p in props)
    name = {c['key']: c['name'] for c in comp}
    L = ['# PEO Service Map %s: market crosswalk and expansion' % VERSION, '', 'Generated %s from the PEO Service Landscape and `_build/service_map_expansion.py`. Draft: every proposal needs a business and compliance decision.' % now, '',
         '## Crosswalk', '', '- %d landscape rows: %d direct, %d partial, %d with no L3 service.' % (len(xw), cnt['direct'], cnt['partial'], cnt['none']),
         '- Rows Insperity sells (core or add-on) but the business model has no service for: ' + (', '.join('%s %s' % (x['id'], x['label']) for x in xw if x['fit'] == 'none' and x['ratings']['nsp']['l'] in 'CA' and x['group'] != 'MOD') or 'none') + '.', '',
         '| Row | Capability | Insperity | Competitors offering | L3 services | Fit | Proposals |', '|---|---|---|---:|---|---|---|']
    for x in xw:
        L.append('| %s | %s | %s | %d | %s | %s | %s |' % (x['id'], x['label'], lbl[x['ratings']['nsp']['l']], len(x['competitorsOffering']),
                 ', '.join(services[s]['label'] for s in x['services']) or '-', x['fit'], ', '.join(x['proposals']) or '-'))
    L += ['', '## Proposals', '', '- %d proposals: %d from Insperity’s own catalog, %d from competitors, %d from the semantic knowledge layer.' % (len(props), byo['catalog'], byo['competitor'], byo['semantic']),
          '- Recommendations: ' + ', '.join('%d %s' % (v, k) for k, v in byr.items()) + '.',
          '- New L1 domains: ' + '; '.join(d['label'] for d in newdom.values()) + '.',
          '- New L2 bounded contexts: ' + '; '.join(c['label'] for c in newctx.values()) + '.',
          '- New service lines: ' + '; '.join(l[1] for l in X.NEW_LINES) + '.', '',
          '| ID | Proposed service | Where | Line | Origin | Recommendation | Offered by | Questions addressed |', '|---|---|---|---|---|---|---|---|']
    for p in props:
        where = (d_by[p['domain']]['label'] if p['domain'] in d_by else newdom[p['domain']]['label'] + ' (new)') + ' › ' + \
                (ctx_by[p['context']]['label'] if p['context'] in ctx_by else newctx[p['context']]['label'] + ' (new)')
        L.append('| %s | %s%s | %s | %s | %s | %s | %s | %d |' % (p['id'], p['label'], (' (extends %s)' % services[p['extends']]['label']) if p['extends'] else '', where, p['line'],
                 p['origin'], p['rec'], ', '.join(name[k] for k in p['offeredBy']) or '-', len(p['addresses'])))
    L += ['', '## Evidence beyond the landscape', ''] + ['- [%s](%s)' % v for v in X.EVIDENCE.values()]
    (out / 'market-and-expansion-report.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    return '- crosswalk: %d rows (%d direct, %d partial, %d none); proposals: %d (%s)' % (len(xw), cnt['direct'], cnt['partial'], cnt['none'], len(props), dict(byo))


README = """# PEO Service Map

The external services of HR Service Operations, organized so every question a client persona asks can be traced to the service that answers it. Built by `../../_build/build_service_map.py`; shown in KE Workbench > Products & Services > PEO Service Map.

**Supply side: the service breakdown.** Human Resources Service Operations > L1 domain (the eight concepts of the area taxonomy) > L2 bounded context > L3 domain service. Each L3 service is also filed under the service line a client buys it in. L2 and L3 come from the business model extract in `Reference/hr-services-business-model/`; their IRIs follow D26 (`.../taxonomy/domain-<L1>.<L2>.<L3>/`) and are marked *planned* until the model is ingested (open question 27).

**Demand side: the questions.** Customer 360 persona > job to be done > job map stage > desired outcome. Each desired outcome becomes the question the persona asks ("Minimize the time required to X" becomes "How quickly can you help me X?") and is answered by the services that address it (`jtbd:isAddressedByService`). Each job also gives a headline question ("Can you help me ...?").

| File | What |
|---|---|
| `peo-service-map.json` | The map (also written to `KE Workbench/data/peo-service-map/peo-service-map.js`) |
| `coverage-report.md` | Questions with no service, services no question reaches, questions per persona |

Rebuild after changing the business model extract, the area taxonomy or the Customer 360 data: `python3 _build/build_service_map.py` from `KE Domains`. Status: Draft {VERSION}; nothing is loaded into GraphDB.
"""

if __name__ == '__main__':
    main()
