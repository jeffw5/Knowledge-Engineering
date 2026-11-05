#!/usr/bin/env python3
"""Structural checks and measures of Semantic Governance v2.3 (amendments A1-A6, A9, A11).

    python3 ingest/structural_checks.py            # from the "KE Workbench" folder: check every current model file, emit telemetry

Each check runs per graph (an asset IRI) and emits its result as a telemetry event (ingest/telemetry.py); the
Operations Dashboard reads those events and does not recompute them (A12). The same rules run in the browser
in assets/ke-rules.js for GraphDB and Turtle-file mode.

Checks (rule ids as reported):
  derivation-bfo      A1, A6.1  every concept, class and primitive has a derivation path to the BFO root
  primitive-site      A2        primitives are minted only in the core or a top-level domain
  polyhierarchy       A3        more than two parents is reported to the data steward
  edge-matrix         A4        a cross-tier edge must be an allowed edge type (default deny)
  tenant-derivation   A5        every customer-tier concept derives from a core or domain class; no ontology, no primitive
  label-resolution    A6.3      a label resolves to exactly one concept in its scope, or the term is pending (A8)
  tenant-isolation    A9        no edge, import or query path joins two tenant graphs; core, domain and enterprise never refer to a tenant
  core-immutable      A1        a deprecated core term names its replacement (core:supersededBy)
Not yet measured (no emitter): schema binding coverage (A6.2: no source-schema bindings are modelled yet).
"""
import collections, datetime, json, pathlib, re, statistics, sys

WB = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WB / 'ingest'))
import telemetry

RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
OWL = 'http://www.w3.org/2002/07/owl#'
SKOS = 'http://www.w3.org/2004/02/skos/core#'
SKOSXL = 'http://www.w3.org/2008/05/skos-xl#'
DCT = 'http://purl.org/dc/terms/'
CORE = 'https://www.insperity.com/ontology/core/'
BASE = 'https://www.insperity.com/'
BFO = ('http://purl.obolibrary.org/obo/BFO_', 'https://purl.obolibrary.org/obo/BFO_')

# A4: the three edge types and the predicates that carry them
DERIVATION = {RDFS + 'subClassOf', SKOS + 'broader', DCT + 'subject', CORE + 'hasPrimaryTerm', CORE + 'formalizedBy'}
CORRESPONDENCE = {SKOS + 'exactMatch', SKOS + 'closeMatch', SKOS + 'broadMatch', SKOS + 'narrowMatch', SKOS + 'relatedMatch'}
LEXICALIZATION = {SKOSXL + 'altLabel', SKOSXL + 'prefLabel', CORE + 'labels'}
EDGE_TYPE = {}
for _p in DERIVATION: EDGE_TYPE[_p] = 'derivation'
for _p in CORRESPONDENCE: EDGE_TYPE[_p] = 'correspondence'
for _p in LEXICALIZATION: EDGE_TYPE[_p] = 'lexicalization'
PARENT_PREDS = (RDFS + 'subClassOf', SKOS + 'broader', SKOS + 'broadMatch')   # parents counted for A3
PENDING = CORE + 'pending'                    # provisional: core:hasResolutionState core:pending (A8)
PENDING_PRED = CORE + 'hasResolutionState'

# Allowed-edge matrix (A4), default deny. {from tier: {to tier: edge types}}. Provisional: the amendment set states
# the principle (derivation upward to the core, correspondence lateral, lexicalization label to concept) and leaves the
# table to the build; edit "allowedEdges" in ingest/ke-ingest.config.json to change it.
MATRIX = {
    'core':       {'core': {'derivation', 'correspondence'}, 'reference': {'derivation', 'correspondence'}},
    'domain':     {'core': {'derivation', 'correspondence'}, 'domain': {'derivation', 'correspondence'}, 'reference': {'derivation', 'correspondence'}},
    'enterprise': {'core': {'derivation', 'correspondence'}, 'domain': {'derivation', 'correspondence'}, 'enterprise': {'derivation', 'correspondence'},
                   'reference': {'derivation', 'correspondence'}},
    'customer':   {'core': {'derivation', 'correspondence'}, 'domain': {'derivation', 'correspondence'}, 'enterprise': {'derivation', 'correspondence'},
                   'customer': {'derivation', 'correspondence'}, 'reference': {'correspondence'}},
}
TENANT = re.compile(r'(?:^|-)customer-(t[0-9a-f]{8})(?:-|$)')


def tier_of(iri):
    """core | domain | enterprise | customer | reference | other, from the asset segment of an IRI (§3.2 Graph Naming)."""
    if not iri: return 'other'
    if iri.startswith(BFO) or iri.startswith('http://purl.obolibrary.org/') or iri.startswith('http://www.w3.org/') or iri.startswith('http://purl.org/'): return 'reference'
    if not iri.startswith(BASE): return 'other'
    parts = [x for x in iri[len(BASE):].split('/') if x]
    if not parts: return 'other'
    if parts[0] in ('graph', 'standard', 'catalog'): return 'other'
    seg = parts[1] if len(parts) > 1 else ''
    if parts[0] in ('resource', 'record-graph', 'party-graph'): return 'other'
    if TENANT.search(seg): return 'customer'
    if re.match(r'^(core)(-|$)', seg): return 'core'
    if re.match(r'^enterprise(-|$)', seg) or seg.startswith('lexicon-enterprise'): return 'enterprise'
    return 'domain' if seg else 'other'


def tenant_of(iri):
    if not iri or not iri.startswith(BASE): return None
    parts = [x for x in iri[len(BASE):].split('/') if x]
    m = TENANT.search(parts[1]) if len(parts) > 1 else None
    return m.group(1) if m else None


def asset_of(iri):
    """The asset IRI a term belongs to: …/{kind}/{scope}/ ."""
    if not iri or not iri.startswith(BASE): return None
    parts = [x for x in iri[len(BASE):].split('/') if x]
    if len(parts) < 2 or parts[0] not in ('vocabulary', 'taxonomy', 'ontology', 'shapes', 'lexicon', 'mapping'): return None
    return BASE + '/'.join(parts[:2]) + '/'


def top_level(scope):
    """Core or a top-level domain: no dotted nesting in the scope segment (domain-sales, not domain-sales.partner-and-channel)."""
    return '.' not in scope


class Model:
    """All the triples of the current model files, indexed by subject."""
    def __init__(self, parsed, matrix=None):
        self.matrix = matrix or MATRIX
        self.E = collections.defaultdict(lambda: collections.defaultdict(list))   # iri -> pred -> [objects]
        self.graph_of = {}                      # iri -> asset IRI (file head)
        self.heads = {}                         # asset IRI -> {file, kind}
        for path, role, ts in parsed:
            heads = [s[1] for s, p, o in ts if s[0] == 'I' and p[1] == RDF + 'type' and o[1] in (OWL + 'Ontology', SKOS + 'ConceptScheme')]
            head = heads[0] if heads else None
            if head: self.heads[head] = {'file': str(path), 'role': role}
            for s, p, o in ts:
                if s[0] != 'I': continue
                self.E[s[1]][p[1]].append(o)
                if head and s[1] not in self.graph_of: self.graph_of[s[1]] = head
        self.types = {i: {o[1] for o in e.get(RDF + 'type', [])} for i, e in self.E.items()}
        self.concepts = {i for i, t in self.types.items() if SKOS + 'Concept' in t and i.startswith(BASE)}
        self.classes = {i for i, t in self.types.items() if (OWL + 'Class' in t) and i.startswith(BASE)}
        self._bfo = {}

    def iris(self, i, pred):
        return [o[1] for o in self.E.get(i, {}).get(pred, []) if o[0] == 'I']

    def graph(self, i):
        return self.graph_of.get(i) or asset_of(i) or ''

    def reaches_bfo(self, i, seen=None):
        """Derivation path to the BFO root, forward edges only."""
        if i in self._bfo: return self._bfo[i]
        if i.startswith(BFO): return True
        seen = seen if seen is not None else set()
        if i in seen: return False
        seen.add(i)
        ok = False
        for p in DERIVATION - {DCT + 'subject', CORE + 'hasPrimaryTerm'}:   # subject / primary term name vocabulary terms, not parents
            for t in self.iris(i, p):
                if self.reaches_bfo(t, seen): ok = True; break
            if ok: break
        if len(seen) <= 1 or ok: self._bfo[i] = ok
        return ok

    def kind_of_asset(self, asset):
        m = re.match(re.escape(BASE) + r'([a-z]+)/', asset or '')
        return m.group(1) if m else ''

    def is_primitive(self, i):
        return i in self.concepts and self.kind_of_asset(self.graph(i)) == 'vocabulary'


def run(parsed, cfg=None):
    cfg = cfg or {}
    M = Model(parsed, _matrix(cfg))
    per = collections.defaultdict(lambda: collections.defaultdict(list))   # asset -> rule -> [(iri, msg)]
    tot = collections.defaultdict(lambda: collections.Counter())          # asset -> counters

    def fail(rule, i, msg):
        per[M.graph(i)][rule].append((i, msg))

    terms = sorted(M.concepts | M.classes)
    # A1 / A6.1: derivation path to BFO
    for i in terms:
        g = M.graph(i); tot[g]['terms'] += 1
        prim = M.is_primitive(i)
        if prim: tot[g]['primitives'] += 1
        if i in M.concepts and not prim and tier_of(g) != 'core':
            # a taxonomy concept reaches BFO through core:formalizedBy; checked as a path, not as a declaration
            pass
        if not M.reaches_bfo(i):
            fail('derivation-bfo', i, ('Primitive declares no BFO parent (core:formalizedBy or rdfs:subClassOf to a class that reaches BFO)' if prim
                                       else 'No derivation path to the BFO root'))
        # A3: parents
        parents = {t for p in PARENT_PREDS for t in M.iris(i, p) if t != OWL + 'Thing'}
        tot[g]['parentSum'] += len(parents)
        if len(parents) > 1: tot[g]['poly'] += 1
        if len(parents) > 2: fail('polyhierarchy', i, f'{len(parents)} parents: report to the data steward')
        # A2: where primitives are minted
        if prim:
            scope = g[len(BASE):].split('/')[1] if g else ''
            t = tier_of(g)
            if t == 'core': tot[g]['primCore'] += 1
            elif t == 'domain' and not top_level(scope): fail('primitive-site', i, f'Primitive minted in the nested domain {scope}: request it from the top-level parent')
            elif t in ('enterprise', 'customer'): fail('primitive-site', i, f'Primitive minted at the {t} tier: only the core or a top-level domain mints primitives')
            if t != 'core': tot[g]['primOutside'] += 1
        # A1: deprecation keeps a pointer
        if tier_of(g) == 'core' and any(o[1] == 'true' for o in M.E[i].get(OWL + 'deprecated', [])) and not M.iris(i, CORE + 'supersededBy'):
            fail('core-immutable', i, 'Deprecated core term has no core:supersededBy')
        # A5: customer tier
        if tier_of(g) == 'customer' and i in M.concepts:
            ups = [t for p in DERIVATION - {DCT + 'subject', CORE + 'hasPrimaryTerm'} for t in M.iris(i, p)]
            if not any(tier_of(t) in ('core', 'domain') or t.startswith(BFO) for t in ups):
                fail('tenant-derivation', i, 'Customer concept has no derivation edge to a core or domain class')
    # A5: a customer asset is never an ontology
    for a in M.heads:
        if tier_of(a) == 'customer' and OWL + 'Ontology' in M.types.get(a, set()) and M.kind_of_asset(a) == 'ontology':
            per[a]['tenant-derivation'].append((a, 'A customer-tier asset holds labels and local concepts, never an ontology'))
    # A4 / A9: edges
    for i, e in M.E.items():
        if not i.startswith(BASE): continue
        ft = tier_of(M.graph(i)) if M.graph(i) else tier_of(i)
        fa = M.graph(i) or asset_of(i) or i
        for p, objs in e.items():
            etype = EDGE_TYPE.get(p)
            imports = p == OWL + 'imports'
            if not etype and not imports: continue
            for o in objs:
                if o[0] != 'I': continue
                t = o[1]
                tt = tier_of(t)
                if tt == 'other': continue
                ta = asset_of(t) or t
                if ta == fa: continue
                # A9: tenant isolation
                ften, tten = tenant_of(fa), tenant_of(ta)
                if tten and ften and tten != ften:
                    fail('tenant-isolation', i, f'Edge to another tenant ({tten}): no path joins two tenant graphs'); continue
                if tten and ft in ('core', 'domain', 'enterprise'):
                    fail('tenant-isolation', i, f'{ft.capitalize()} asset refers to tenant {tten}: tenant graphs may refer to core, domain and enterprise, never the reverse'); continue
                if imports: continue
                tot[fa]['crossEdges'] += 1
                allowed = M.matrix.get(ft, {}).get(tt)
                if not allowed or etype not in allowed:
                    fail('edge-matrix', i, f'{etype.capitalize()} edge {p.rsplit("/", 1)[-1].rsplit("#", 1)[-1]} from the {ft} tier to the {tt} tier is not in the allowed-edge matrix')
    for i in terms:
        for p in CORRESPONDENCE:
            tot[M.graph(i)]['correspondence'] += len(M.E[i].get(p, []))
    # A6.3 / A8: label resolution within a scope (graph)
    by_label = collections.defaultdict(lambda: collections.defaultdict(set))
    for i in M.concepts:
        g = M.graph(i)
        pending = PENDING in M.iris(i, PENDING_PRED)
        if pending:
            tot[g]['pending'] += 1
        for p in (SKOS + 'prefLabel', SKOS + 'altLabel'):
            for o in M.E[i].get(p, []):
                if o[0] == 'L': by_label[g][(o[1].strip().lower(), (o[2] if len(o) > 2 else '') or '')].add((i, pending))
    for g, labels in by_label.items():
        for (txt, lang), who in labels.items():
            tot[g]['labels'] += 1
            ids = {i for i, _ in who}
            if len(ids) > 1 and not all(pn for _, pn in who):
                for i in sorted(ids): fail('label-resolution', i, f'Label "{txt}" resolves to {len(ids)} concepts in this scope')
    return M, per, tot


def _matrix(cfg):
    m = cfg.get('allowedEdges')
    if not m: return MATRIX
    return {a: {b: set(v) for b, v in tos.items()} for a, tos in m.items() if not a.startswith('_')}


ORPHAN_RULES = ('derivation-bfo', 'label-resolution')      # A6: concept derivation, label resolution (schema binding coverage: not yet measured)


def measures(M, per, tot, edition, now):
    """The eight A11 structural measures plus the three A6 orphan checks, as telemetry events (one per graph)."""
    ev = []
    def add(measure, graph, value, unit, count=None, total=None, target=None, note=''):
        ev.append({'at': now, 'measure': measure, 'graph': graph, 'value': value, 'unit': unit, 'count': count, 'total': total,
                   'target': target, 'note': note, 'edition': edition, 'emitter': 'ingest/structural_checks.py'})
    graphs = sorted(g for g in tot if g in M.heads)
    for g in graphs:
        t = tot[g]; n = t['terms'] or 0
        f = {r: len(v) for r, v in per[g].items()}
        add('orphan-concept-derivation', g, f.get('derivation-bfo', 0), 'failures', f.get('derivation-bfo', 0), n, 0, 'A6.1')
        add('orphan-label-resolution', g, f.get('label-resolution', 0), 'failures', f.get('label-resolution', 0), t['labels'], 0, 'A6.3')
        add('orphan-rate', g, round((f.get('derivation-bfo', 0) + f.get('label-resolution', 0)) / n, 4) if n else 0.0, 'failures per term',
            f.get('derivation-bfo', 0) + f.get('label-resolution', 0), n, 0, 'A6: schema binding coverage not yet measured')
        add('correspondence-density', g, round(t['correspondence'] / n, 4) if n else 0.0, 'links per term', t['correspondence'], n, None, 'A4')
        add('polyhierarchy-rate', g, round(t['poly'] / n, 4) if n else 0.0, 'share of terms', t['poly'], n, None, 'A3; over two parents: ' + str(f.get('polyhierarchy', 0)))
        if t['primitives']:
            add('domain-minted-primitive-share', g, round(t['primOutside'] / t['primitives'], 4), 'share of primitives', t['primOutside'], t['primitives'], None, 'A2')
    # stem reuse: share of taxonomy concepts and ontology classes built from existing primitives (dcterms:subject resolving to a vocabulary term)
    for g in graphs:
        kind = M.kind_of_asset(g)
        if kind not in ('taxonomy', 'ontology'): continue
        mine = [i for i in (M.concepts | M.classes) if M.graph(i) == g]
        built = [i for i in mine if any(M.is_primitive(p) for p in M.iris(i, DCT + 'subject') + M.iris(i, CORE + 'hasPrimaryTerm'))]
        add('stem-reuse-ratio', g, round(len(built) / len(mine), 4) if mine else 0.0, 'share of terms', len(built), len(mine), None, 'A1, A2')
    # impact radius: terms that derive (transitively) from each core term; reported for the core as a whole (max, median)
    kids = collections.defaultdict(set)
    for i in M.concepts | M.classes:
        for p in DERIVATION:
            for t in M.iris(i, p): kids[t].add(i)
    def radius(x, seen=None):
        seen = seen if seen is not None else set()
        for c in kids.get(x, ()):
            if c not in seen: seen.add(c); radius(c, seen)
        return seen
    core_terms = [i for i in M.concepts | M.classes if tier_of(M.graph(i)) == 'core']
    rad = [len(radius(i)) for i in core_terms]
    if rad:
        add('impact-radius', 'https://www.insperity.com/ontology/core/', max(rad), 'terms affected (largest core term)', max(rad), len(core_terms), None,
            'median ' + str(int(statistics.median(rad))) + ' across ' + str(len(core_terms)) + ' core terms; per change: run the change-impact query')
    return ev


def pending_measures(now, edition):
    """Promotion-backlog age and HITL disposition mix, from the pending-term store (ingest/feedback/pending.jsonl) and its dispositions."""
    import pending as P
    recs = P.records()
    open_ = [r for r in recs if r.get('state') != 'resolved']
    age = 0.0
    if open_:
        t0 = min(datetime.datetime.fromisoformat(r['at'].replace('Z', '+00:00')) for r in open_)
        age = round((datetime.datetime.now(datetime.timezone.utc) - t0).total_seconds() / 86400, 1)
    ev = [{'at': now, 'measure': 'promotion-backlog-age', 'graph': BASE + 'graph/pending-terms', 'value': age, 'unit': 'days (oldest open)', 'count': len(open_),
           'total': len(recs), 'target': None, 'note': 'A8', 'edition': edition, 'emitter': 'ingest/pending.py'}]
    done = [r for r in recs if r.get('state') == 'resolved']
    mix = collections.Counter(r['disposition'] for r in done)
    for k in P.DISPOSITIONS:
        ev.append({'at': now, 'measure': 'hitl-disposition-mix', 'graph': BASE + 'graph/pending-terms/' + k, 'value': round(mix[k] / len(done), 4) if done else 0.0,
                   'unit': 'share of dispositions', 'count': mix[k], 'total': len(done), 'target': None, 'note': 'A8: ' + k, 'edition': edition, 'emitter': 'ingest/pending.py'})
    return ev


def main(parsed=None, cfg=None, edition=''):
    import ke_ingest as k
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')
    if cfg is None:
        cfg, _ = k.load_config(str(WB / 'ingest/ke-ingest.config.json'))
    if parsed is None:
        parsed = load_parsed(k)
    M, per, tot = run(parsed, cfg)
    ev = measures(M, per, tot, edition, now) + pending_measures(now, edition)
    # one event per rule outcome, so policies read results from telemetry too
    for g in sorted(tot):
        if g not in M.heads: continue
        for rule in ('derivation-bfo', 'primitive-site', 'polyhierarchy', 'edge-matrix', 'tenant-derivation', 'label-resolution', 'tenant-isolation', 'core-immutable'):
            ev.append({'at': now, 'measure': 'check:' + rule, 'graph': g, 'value': len(per[g].get(rule, [])), 'unit': 'failures', 'count': len(per[g].get(rule, [])),
                       'total': tot[g]['terms'], 'target': 0 if rule != 'polyhierarchy' else None,
                       'note': (per[g][rule][0][1] if per[g].get(rule) else ''), 'edition': edition, 'emitter': 'ingest/structural_checks.py'})
    telemetry.emit(ev)
    summ = {'graphs': len([g for g in tot if g in M.heads]), 'events': len(ev)}
    for rule in ('derivation-bfo', 'primitive-site', 'polyhierarchy', 'edge-matrix', 'tenant-derivation', 'label-resolution', 'tenant-isolation', 'core-immutable'):
        summ[rule] = sum(len(v.get(rule, [])) for v in per.values())
    return summ


def load_parsed(k):
    KE = WB.parent
    files = []
    for p in sorted((KE / 'KE Baseline/Baseline Core v1.0/ttl').glob('*.ttl')):
        if not p.name.startswith('change-record'): files.append((p, 'model'))
    for p in sorted((KE / 'KE Domains').glob('**/ttl/*.ttl')):
        if 'archive' in p.parts or 'change-log' in p.parts or 'assembly' in p.parts or p.name.startswith('change-record'): continue
        files.append((p, 'model'))
    for p in sorted((WB / 'data/c360').glob('*.ttl')): files.append((p, 'c360'))
    out = []
    for p, role in files:
        try:
            ts, _ = k.parse_turtle(p.read_text(encoding='utf-8'))
            out.append((p, role, ts))
        except Exception as e:
            print('  skipped', p.name, e)
    return out


if __name__ == '__main__':
    guide = {}
    try:
        m = re.search(r'window\.KE_GUIDE\s*=\s*(\{.*\});', (WB / 'assets/ke-guide.js').read_text(encoding='utf-8'), re.S)
        guide = json.loads(m.group(1)) if m else {}
    except Exception:
        pass
    print(json.dumps(main(edition=guide.get('edition', '')), indent=2))
