#!/usr/bin/env python3
"""Build the Sales assembly (Service › Process › Process step, with the SIPOCM of every step) and the Sales value map,
then validate them and measure the assembly.

    python3 _build/build_assembly.py                 # from the "KE Domains/Commercial Operations" folder

Reads   _build/assembly_sales.py, _build/persona-peo-buyers.json
        <domain>/ttl/*-domain-*.ttl (latest version of each asset), ../../KE Baseline/Baseline Core v1.0/ttl (read only)
        ../../KE Workbench/ingest/ke_ingest.py (Turtle parser and writer)
Writes  commercial-operations/assembly/{ttl,trig}/persona-graph-…
        sales/assembly/{ttl,trig}/{party-graph,step-graph,process-graph,service-graph,value-map,manifest}-…
        sales/assembly/assembly-report.md, assembly-measures.csv, value-gaps.csv
        Superseded component files are moved to archive/superseded-assembly-<release>/.

Checks (exit 1 on an error), for each manifest: every instance is typed by a core or domain class and classified
(dcterms:type) by a concept that exists; every graph refers only to the core, the container and its own domain (D1);
every resource a graph refers to is defined by a component in that manifest (closure); the service assembly never
refers to the persona graph (D24); and the core, container and Sales SHACL shapes hold over the assembled data (run here by a small SHACL Core subset: targetClass, path and inversePath, class, or, minCount, maxCount),
after the owl:inverseOf pairs of the ontologies are applied, as a repository with inference would.
"""
import argparse, collections, csv, datetime, importlib, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
AREA = HERE.parent
sys.path.insert(0, str(HERE))
import assembly_sales as A

CORE_NAMES = ('process party role asset location time event issue product services capability persona domain rules requirements '
              'lifecycle valuestream compliance job decision governance logic measure policy value').split()
DOMAINS = ['commercial_operations', 'sales', 'marketing', 'legal', 'customer_success', 'pricing_and_contracts', 'partner_and_channel']


def slug(x): return re.sub(r'[^a-z0-9]+', '-', x.lower()).strip('-')


def vkey(path):
    m = re.search(r'-(\d+)\.(\d+)\.(\d+)\.ttl$', path.name)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


class Asm:
    def __init__(self, a):
        sys.path.insert(0, a.ingest)
        global k
        import ke_ingest as k
        self.k = k
        self.cfg, _ = k.load_config(str(pathlib.Path(a.ingest) / 'ke-ingest.config.json'))
        self.base = self.cfg['baseUrl']
        self.CORE = self.base + 'ontology/core/'
        self.out = pathlib.Path(a.out)
        t = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        self.now = k.L(t.strftime('%Y-%m-%dT%H:%M:%SZ'), None, k.XSD + 'dateTime')
        self.today = k.L(t.strftime('%Y-%m-%d'), None, k.XSD + 'date')
        self.errors, self.warnings = [], []
        self.specs = {n: importlib.import_module('spec_' + n).DOMAIN for n in DOMAINS}
        self.ver = {d['key']: d.get('version', '0.1.0') for d in self.specs.values()}
        # prefixes
        p = {'core': self.CORE, 'rdf': k.RDF, 'rdfs': k.RDFS, 'owl': k.OWL, 'skos': k.SKOS, 'dct': k.DCT, 'xsd': k.XSD,
             'sh': k.SH, 'obo': 'http://purl.obolibrary.org/obo/'}
        for c in CORE_NAMES:
            p[c + 'tax'] = f'{self.base}taxonomy/core-{c}/'; p[c + 'voc'] = f'{self.base}vocabulary/core-{c}/'
        for d in self.specs.values():
            p[d['prefix']] = f'{self.base}ontology/domain-{d["key"]}/'
            p[d['prefix'] + 'tax'] = f'{self.base}taxonomy/domain-{d["key"]}/'
            p[d['prefix'] + 'voc'] = f'{self.base}vocabulary/domain-{d["key"]}/'
            p[d['prefix'] + 'shp'] = f'{self.base}shapes/domain-{d["key"]}/'
        self.RS = self.base + 'resource/domain-sales/'
        self.RC = self.base + 'resource/domain-commercial-operations/'
        p.update({'salesres': self.RS, 'commercialopsres': self.RC})
        self.pfx = p
        self.load_model(pathlib.Path(a.core))

    # ── the model the assembly is built on (read only) ───────────────────────
    def load_model(self, core_dir):
        k = self.k
        # only the core assets from the baseline folder: anything else that lands there is not core (D1)
        files = [f for f in sorted(core_dir.glob('*.ttl')) if re.match(r'(vocabulary|taxonomy|ontology|shapes)-core(-[a-z]+)?-\d', f.name)]
        latest = {}
        for f in self.out.glob('*/ttl/*-domain-*.ttl'):
            stem = re.sub(r'-\d+\.\d+\.\d+\.ttl$', '', f.name)
            if stem not in latest or vkey(f) > vkey(latest[stem]): latest[stem] = f
        files += sorted(latest.values())
        self.model_files = files
        G = collections.OrderedDict()
        for i, f in enumerate(files):
            for s, p_, o in k.parse_turtle(f.read_text(encoding='utf-8'))[0]:
                s, o = bnode(s, i), bnode(o, i)
                G.setdefault(s, collections.OrderedDict()).setdefault(p_[1], []).append(o)
        self.G = G
        T = k.RDF + 'type'
        self.classes = {s[1] for s, ps in G.items() if s[0] == 'I' and k.I(k.OWL + 'Class') in ps.get(T, [])}
        self.concepts = {s[1] for s, ps in G.items() if s[0] == 'I' and '/taxonomy/' in s[1] and k.I(k.SKOS + 'Concept') in ps.get(T, [])}
        self.primitives = {s[1] for s, ps in G.items() if s[0] == 'I' and '/vocabulary/' in s[1] and k.I(k.SKOS + 'Concept') in ps.get(T, [])}
        self.sup = collections.defaultdict(set)
        for s, ps in G.items():
            for o in ps.get(k.RDFS + 'subClassOf', []):
                if s[0] == 'I' and o[0] == 'I': self.sup[s[1]].add(o[1])
        self.inverse = {}
        for s, ps in G.items():
            for o in ps.get(k.OWL + 'inverseOf', []):
                if s[0] == 'I' and o[0] == 'I': self.inverse[s[1]] = o[1]; self.inverse[o[1]] = s[1]
        self.label = {s[1]: ps[k.SKOS + 'prefLabel'][0][1] for s, ps in G.items() if s[0] == 'I' and ps.get(k.SKOS + 'prefLabel')}

    def supers(self, c, seen=None):
        seen = seen if seen is not None else set()
        for x in self.sup.get(c, ()):
            if x not in seen: seen.add(x); self.supers(x, seen)
        return seen

    # ── references ──────────────────────────────────────────────────────────
    def iri(self, ref):
        pre, local = ref.split(':', 1)
        if pre == 'js': return self.RC + 'job-step/' + slug(local)
        if pre in ('step', 'record', 'service', 'process', 'party', 'role', 'agent', 'measure'): return self.RS + pre + '/' + local
        return self.pfx[pre] + local

    def I(self, ref): return self.k.I(self.iri(ref))
    def L(self, v, lang='en'): return self.k.L(v, lang)

    # ── graph writing ───────────────────────────────────────────────────────
    def new_graph(self, gid, label, definition, kind, requires, version):
        self.cur_ver = version
        g = collections.OrderedDict()
        h = self.k.I(gid)
        k = self.k
        add(g, h, k.RDF + 'type', self.I('core:information-asset'))
        add(g, h, k.DCT + 'type', self.I('assettax:knowledge-artifact'))
        add(g, h, k.RDFS + 'label', self.L(label)); add(g, h, k.SKOS + 'prefLabel', self.L(label))
        add(g, h, k.DCT + 'title', self.L(label))
        add(g, h, k.SKOS + 'definition', self.L(definition))
        add(g, h, k.SKOS + 'note', self.L(f'A {kind} of the Commercial Operations assembly (design decisions D17–D24). Its resources are typed by core and domain classes and classified by taxonomy concepts.'))
        for r in requires: add(g, h, k.DCT + 'requires', k.I(r))
        add(g, h, k.DCT + 'conformsTo', k.I(self.cfg['conformsTo'][0]))
        add(g, h, k.DCT + 'publisher', k.I(self.cfg['publisher']))
        add(g, h, k.OWL + 'versionInfo', k.L(version))
        self.gov(g, h, header=True)
        return g, h

    def gov(self, g, s, header=False):
        k = self.k
        if not header: add(g, s, k.OWL + 'versionInfo', k.L(self.cur_ver))
        add(g, s, self.CORE + 'hasLifecycleStatus', k.I(self.CORE + self.cfg['lifecycleStatus']))
        add(g, s, k.DCT + 'creator', k.L(self.cfg['author']))
        add(g, s, k.DCT + 'created', self.today)
        add(g, s, k.DCT + 'modified', self.now)

    def resource(self, g, ref, cls, types, label, definition, alt=(), scope=None):
        k = self.k
        x = self.I(ref)
        add(g, x, k.RDF + 'type', self.I(cls))
        for t in types: add(g, x, k.DCT + 'type', self.I(t))
        add(g, x, k.RDFS + 'label', self.L(label)); add(g, x, k.SKOS + 'prefLabel', self.L(label))
        for a_ in alt: add(g, x, k.SKOS + 'altLabel', self.L(a_))
        if definition: add(g, x, k.SKOS + 'definition', self.L(definition))
        if scope: add(g, x, k.SKOS + 'scopeNote', self.L(scope))
        self.gov(g, x)
        return x

    def write(self, g, gid, folder, name, title, manifest):
        k = self.k
        w = k.Writer(self.pfx, [self.CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
        subjects = [x for x in g if x[0] == 'I']
        hdr = k.I(gid); subjects = [hdr] + [x for x in subjects if x != hdr]
        head = (f'# {title}\n# {gid}  ·  version {self.cur_ver}  ·  {self.cfg["lifecycleStatus"]}\n'
                f'# Generated by build_assembly.py on {self.now[1]} from assembly_sales.py and persona-peo-buyers.json\n'
                f'# Standards: {self.cfg["standardsRef"]}\n')
        text = w.write(g, subjects, head)
        trig = w.write_trig(g, subjects, head.replace('\n# Standards', f'\n# Named graph: {gid}\n# Standards'), gid)
        for sub, body in (('ttl', text), ('trig', trig)):
            d = folder / sub; d.mkdir(parents=True, exist_ok=True)
            (d / f'{name}.{sub}').write_text(body, encoding='utf-8')
        self.graphs[gid] = dict(g=g, name=name, folder=folder, title=title, manifest=manifest, version=self.cur_ver,
                                domain=('commercial-operations' if '/domain-commercial-operations/' in gid else 'sales'))
        return text

    # ── build ───────────────────────────────────────────────────────────────
    def build(self):
        self.graphs = collections.OrderedDict()
        sales_req = [f'{self.base}{kind}/domain-sales/{self.ver["sales"]}/' for kind in ('taxonomy', 'ontology', 'shapes')]
        co_req = [f'{self.base}{kind}/domain-commercial-operations/{self.ver["commercial-operations"]}/' for kind in ('taxonomy', 'ontology', 'shapes')]
        core_req = [self.CORE + '0.1.0/']
        self.req = core_req + co_req + sales_req
        self.steps = {'step:' + s['id']: s for s in A.STEPS}
        self.persona_graph(core_req + co_req)            # value map
        self.party_graph(self.req)                       # service assembly
        for st in A.STEPS: self.step_graph(st, self.req)
        for pr in A.PROCESSES: self.process_graph(pr, self.req)
        for sv in A.SERVICES: self.service_graph(sv, self.req)
        self.manifest(self.req)
        self.value_map(self.req)
        self.value_map_manifest(self.req)

    def sales_write(self, g, gid, name, title, manifest='assembly'):
        self.write(g, gid, self.out / 'sales' / 'assembly', name, title, manifest)

    def persona_graph(self, req):
        k = self.k
        data = json.load(open(HERE / 'persona-peo-buyers.json', encoding='utf-8'))
        self.persona = data
        gid = self.RC + 'persona-graph/peo-buyer-personas/'
        g, h = self.new_graph(gid, 'PEO buyer personas', 'The buyer personas of a professional employer organization, assembled from the Persona and Jobs models: each persona, the jobs its typical executor is trying to get done, their job steps, and the desired outcomes mapped to each job step, with their metric cards and targets. Shared by every Commercial Operations domain.', 'persona graph', req, '0.1.0')
        add(g, h, k.DCT + 'source', k.L(data['_source']))
        KIND = {'Core functional job': ['jobtax:core-job', 'jobtax:functional-job'],
                'Related financial job': ['jobtax:related-job', 'jobtax:functional-job'],
                'Related emotional/risk job': ['jobtax:related-job', 'jobtax:emotional-job'],
                'Related social job': ['jobtax:related-job', 'jobtax:emotional-job'],
                'Related functional job': ['jobtax:related-job', 'jobtax:functional-job']}
        self.js = {}           # job step id -> dict(label, stage, outcomes)
        for key, st in data['studies'].items():
            pname = 'Client Admin' if key == 'admin' else 'HR Specialist'
            p_ = self.RC + 'persona/' + slug(pname)
            study = self.RC + 'job-study/' + slug(st['id'])
            x = k.I(study)
            add(g, x, k.RDF + 'type', self.I('core:information-asset')); add(g, x, k.DCT + 'type', self.I('jobtax:job-study'))
            add(g, x, k.RDFS + 'label', self.L(st['title'])); add(g, x, k.SKOS + 'prefLabel', self.L(st['title']))
            add(g, x, k.SKOS + 'scopeNote', self.L(st['scope'])); add(g, x, k.SKOS + 'notation', k.L(st['id']))
            add(g, x, self.CORE + 'concerns', k.I(p_)); self.gov(g, x)
            x = k.I(p_)
            add(g, x, k.RDF + 'type', self.I('core:persona')); add(g, x, k.DCT + 'type', self.I('personatax:persona'))
            add(g, x, k.RDFS + 'label', self.L(pname)); add(g, x, k.SKOS + 'prefLabel', self.L(pname))
            add(g, x, k.SKOS + 'definition', self.L(f'The {pname} buyer persona of a prospect evaluating a professional employer organization.'))
            add(g, x, k.SKOS + 'scopeNote', self.L('A persona instance assembled from the Persona and Jobs models; not typed by role (Baseline decisions 22 and 23).'))
            self.gov(g, x)
            for job in st['jobs']:
                j = k.I(self.RC + 'job/' + slug(job['id']))
                add(g, k.I(p_), self.CORE + 'performsJob', j)
                add(g, j, k.RDF + 'type', self.I('core:job'))
                for t in KIND[job['kind']]: add(g, j, k.DCT + 'type', self.I(t))
                if 'financial' in job['kind']: add(g, j, k.DCT + 'subject', self.I('domainvoc:finance'))
                add(g, j, k.RDFS + 'label', self.L(job['name'])); add(g, j, k.SKOS + 'prefLabel', self.L(job['name']))
                add(g, j, k.SKOS + 'definition', self.L(job['statement'])); add(g, j, k.SKOS + 'notation', k.L(job['id']))
                if job['kind'] in ('Related financial job', 'Related social job', 'Related emotional/risk job'):
                    add(g, j, k.SKOS + 'scopeNote', self.L(f'Recorded in the job study as "{job["kind"]}". Job kinds are functional and emotional only (Baseline decision 20): a financial job is functional with a finance subject, a social or risk job is emotional.'))
                self.gov(g, j)
                for s_ in job['steps']:
                    sid = self.RC + 'job-step/' + slug(s_['id'])
                    x = k.I(sid)
                    add(g, j, self.CORE + 'hasStep', x)
                    add(g, x, k.RDF + 'type', self.I('core:job-step')); add(g, x, k.DCT + 'type', self.I('jobtax:job-step'))
                    add(g, x, k.RDFS + 'label', self.L(s_['name'])); add(g, x, k.SKOS + 'prefLabel', self.L(s_['name']))
                    add(g, x, k.SKOS + 'notation', k.L(s_['id'])); add(g, x, self.CORE + 'isStepOf', j)
                    add(g, x, k.SKOS + 'note', self.L(f'Buyer stage: {s_["stage"]}. The stage is the provider\'s view of where this job step falls in the selling process (Baseline decision 21); it is not part of the job.'))
                    add(g, x, k.SKOS + 'editorialNote', self.L(f'Addressed in the buyer persona tool by: {s_["service"]}.'))
                    self.gov(g, x)
                    outs = []
                    for n, o in enumerate(s_['outcomes'], 1):
                        stmt, unit, direction, target, baseline, card, source = o
                        oid = self.RC + 'desired-outcome/' + slug(s_['id']) + f'-{n}'
                        mc = self.RC + 'measure/' + slug(card)
                        ox = k.I(oid)
                        add(g, x, self.CORE + 'hasOutcome', ox)
                        add(g, ox, k.RDF + 'type', self.I('core:desired-outcome')); add(g, ox, k.DCT + 'type', self.I('jobtax:desired-outcome'))
                        add(g, ox, k.RDFS + 'label', self.L(stmt)); add(g, ox, k.SKOS + 'prefLabel', self.L(stmt))
                        add(g, ox, self.CORE + 'outcomeOf', x); add(g, ox, self.CORE + 'measuredBy', k.I(mc))
                        add(g, ox, k.SKOS + 'note', self.L('Direction: ' + ('minimize' if direction == 'min' else 'maximize') + '.'))
                        self.gov(g, ox)
                        mx = k.I(mc)
                        if mx not in g:
                            add(g, mx, k.RDF + 'type', self.I('core:measure')); add(g, mx, k.DCT + 'type', self.I('measuretax:derived-measure'))
                            add(g, mx, k.RDFS + 'label', self.L(card)); add(g, mx, k.SKOS + 'prefLabel', self.L(card))
                            add(g, mx, k.SKOS + 'definition', self.L(f'The metric card {card}, measured in {unit}.'))
                            add(g, mx, k.DCT + 'source', k.L(source)); self.gov(g, mx)
                        tx = k.I(self.RC + 'measure/' + slug(s_['id']) + f'-{n}-target')
                        add(g, tx, k.RDF + 'type', self.I('core:measure')); add(g, tx, k.DCT + 'type', self.I('measuretax:target'))
                        add(g, tx, k.RDFS + 'label', self.L(f'Target for {s_["id"]}.{n}')); add(g, tx, k.SKOS + 'prefLabel', self.L(f'Target for {s_["id"]}.{n}'))
                        add(g, tx, self.CORE + 'measures', ox); add(g, tx, k.RDF + 'value', k.L(str(target), None, k.XSD + 'decimal'))
                        add(g, tx, k.SKOS + 'note', self.L(f'Unit: {unit}.')); self.gov(g, tx)
                        outs.append(dict(n=n, iri=oid, stmt=stmt, unit=unit, direction=direction, target=target, baseline=baseline, card=card, source=source, card_iri=mc))
                    self.js[s_['id']] = dict(iri=sid, label=s_['name'], stage=s_['stage'], persona=pname, outcomes=outs)
        self.write(g, gid, self.out / 'commercial-operations' / 'assembly', 'persona-graph-domain-commercial-operations-peo-buyer-personas-0.1.0', 'PEO buyer personas (persona graph)', 'value-map')

    def party_graph(self, req):
        P = A.PARTY_GRAPH
        gid = self.RS + 'party-graph/' + P['id'] + '/'
        g, h = self.new_graph(gid, P['label'], P['definition'], 'party graph', req, P['version'])
        for ref, cls, types, label, d, extra in P['resources']:
            self.resource(g, ref, cls, types, label, d, alt=extra.get('alt', ()))
        self.sales_write(g, gid, f'party-graph-domain-sales-{P["id"]}-{P["version"]}', f'{P["label"]} (party graph)')

    def step_graph(self, st, req):
        k = self.k
        sid, label, mode = st['id'], st['label'], st['mode']
        gid = self.RS + 'step-graph/' + sid + '/'
        g, h = self.new_graph(gid, label, f'The step graph of the {label.lower()} selling step: a reusable component that process graphs are built from, with its suppliers, inputs, outputs, customers and measures (SIPOCM).', 'step graph', req, st['version'])
        x = self.resource(g, 'step:' + sid, 'sales:selling-step', [st['stage'], st['kind']], label, st['definition'],
                          scope=f'Delivery mode: {mode.lower()}. Performed by ' + {'Manual': 'the sales organization', 'Automated': 'the sales advisor agent', 'Hybrid': 'the sales organization and the sales advisor agent'}[mode] + '.')
        add(g, x, self.CORE + 'fulfillsRole', self.I('role:sales-representative'))
        if mode in ('Manual', 'Hybrid'): add(g, x, self.CORE + 'performedBy', self.I('party:sales-organization'))
        if mode in ('Automated', 'Hybrid'): add(g, x, self.CORE + 'performedBy', self.I('agent:sales-advisor'))
        for s_ in st['suppliers']: add(g, x, self.pfx['commercialops'] + 'hasSupplier', self.I(s_))
        for r in st['consumes']:
            if isinstance(r, tuple):
                ref, cls, typ, rl, rd = r
                self.resource(g, ref, cls, [typ], rl, rd, scope='An input from outside the assembled processes, supplied by the parties this step names with has supplier.')
                r = ref
            add(g, x, self.CORE + 'consumes', self.I(r))
        for ref, cls, typ, rl, rd in st['produces']:
            add(g, x, self.CORE + 'produces', self.I(ref))
            self.resource(g, ref, cls, [typ], rl, rd)
        for c_ in st['customers']: add(g, x, self.pfx['commercialops'] + 'hasCustomer', self.I(c_))
        for mid, ml, md, unit, direction, dim in st['measures']:
            m = self.resource(g, 'measure:' + mid, 'core:measure', ['measuretax:derived-measure', dim], ml, md)
            add(g, m, k.SKOS + 'note', self.L(f'Unit: {unit}. Direction: {direction}.'))
            add(g, x, self.CORE + 'measuredBy', m)
        self.sales_write(g, gid, f'step-graph-domain-sales-{sid}-{st["version"]}', f'{label} (step graph)')

    def process_graph(self, pr, req):
        k = self.k
        pid, label, d, kind, steps, ver = pr
        gid = self.RS + 'process-graph/' + pid + '/'
        g, h = self.new_graph(gid, label, f'The process graph of the {label.lower()} sales process: it builds the process from its step graphs, in order.', 'process graph', req, ver)
        x = self.resource(g, 'process:' + pid, 'core:process', [kind, 'processtax:operational-process'], label, d,
                          scope='Built from ' + ', '.join(self.steps[s]['label'].lower() for s in steps) + ', in that order.')
        for s in steps: add(g, x, self.CORE + 'hasStep', self.I(s))
        for a_, b_ in zip(steps, steps[1:]): add(g, self.I(a_), self.CORE + 'precedes', self.I(b_))
        self.sales_write(g, gid, f'process-graph-domain-sales-{pid}-{ver}', f'{label} (process graph)')

    def service_graph(self, sv, req):
        vid, label, d, kind, delivery, processes, ver = sv
        gid = self.RS + 'service-graph/' + vid + '/'
        g, h = self.new_graph(gid, label, f'The service graph of the {label.lower()} sales service: it assembles the service from the process graphs that enable it.', 'service graph', req, ver)
        plabel = {('process:' + p[0]): p[1].lower() for p in A.PROCESSES}
        x = self.resource(g, 'service:' + vid, 'sales:sales-service', [kind], label, d,
                          scope='Enabled by ' + ' and '.join(plabel[p] for p in processes) + '; delivered by ' + self.steps[delivery]['label'].lower() + '.')
        for p in processes: add(g, self.I(p), self.CORE + 'supports', x)
        add(g, self.I(delivery), self.CORE + 'deliveryOf', x)
        self.sales_write(g, gid, f'service-graph-domain-sales-{vid}-{ver}', f'{label} (service graph)')

    def service_steps(self, sv):
        """The steps of a service: the steps of the processes that enable it, in process order."""
        out = []
        for p in sv[5]:
            for s in next(pr[4] for pr in A.PROCESSES if 'process:' + pr[0] == p):
                if s not in out: out.append(s)
        return out

    def value_map(self, req):
        k = self.k
        gid = self.RS + 'value-map/sales-buyer-value/'
        g, h = self.new_graph(gid, 'Sales buyer value map', 'The value map between the Sales assembly and the PEO buyer personas: the job steps each selling step addresses, and what each sales service delivers today at those job steps, measured on the same metric cards as the desired outcomes.', 'value map', req, '0.1.0')
        for s, jss in A.ADDRESSES.items():
            for j in jss: add(g, self.I(s), self.CORE + 'addresses', self.I(j))
        for sv in A.SERVICES:
            vid, x = sv[0], self.I('service:' + sv[0])
            addressed = []
            for s in self.service_steps(sv):
                addressed += [j for j in A.ADDRESSES.get(s, []) if j not in addressed]
            for j in addressed:
                info = self.js[j.split(':', 1)[1]]
                for o in info['outcomes']:
                    if o['baseline'] is None: continue
                    did = self.RS + 'delivered-outcome/' + vid + '-' + slug(j.split(':', 1)[1]) + f'-{o["n"]}'
                    dx = k.I(did)
                    add(g, dx, k.RDF + 'type', self.I('core:delivered-outcome')); add(g, dx, k.DCT + 'type', self.I('jobtax:delivered-outcome'))
                    lab = f'Delivered: {o["stmt"]}'
                    add(g, dx, k.RDFS + 'label', self.L(lab)); add(g, dx, k.SKOS + 'prefLabel', self.L(lab))
                    add(g, dx, self.CORE + 'outcomeOf', k.I(info['iri'])); add(g, dx, self.CORE + 'achievedBy', x)
                    add(g, dx, self.CORE + 'measuredBy', k.I(o['card_iri']))
                    add(g, dx, k.SKOS + 'note', self.L(f'Compare with desired outcome {j.split(":", 1)[1]}.{o["n"]}: same job step, same metric card.'))
                    self.gov(g, dx)
                    ax = k.I(self.RS + 'measure/' + vid + '-' + slug(j.split(':', 1)[1]) + f'-{o["n"]}-actual')
                    add(g, ax, k.RDF + 'type', self.I('core:measure')); add(g, ax, k.DCT + 'type', self.I('measuretax:actual-value'))
                    al = f'Baseline for {j.split(":", 1)[1]}.{o["n"]}'
                    add(g, ax, k.RDFS + 'label', self.L(al)); add(g, ax, k.SKOS + 'prefLabel', self.L(al))
                    add(g, ax, self.CORE + 'measures', dx); add(g, ax, k.RDF + 'value', k.L(str(o['baseline']), None, k.XSD + 'decimal'))
                    add(g, ax, k.SKOS + 'note', self.L(f'Unit: {o["unit"]}. Measured by: {o["source"]}.')); self.gov(g, ax)
        self.sales_write(g, gid, 'value-map-domain-sales-sales-buyer-value-0.1.0', 'Sales buyer value map (value map)', 'value-map')

    def manifest_graph(self, ident, version, label, definition, parts, req):
        k = self.k
        gid = self.RS + f'manifest/{ident}/'
        g, h = self.new_graph(gid, f'{label} manifest', f'The release manifest of the {label}: the component graphs, and their versions, that make it up.', 'manifest', req, version)
        x = k.I(self.RS + 'manifest/' + ident)
        add(g, x, k.RDF + 'type', self.I('core:information-asset')); add(g, x, k.DCT + 'type', self.I('governancetax:release-manifest'))
        add(g, x, k.RDFS + 'label', self.L(label)); add(g, x, k.SKOS + 'prefLabel', self.L(label))
        add(g, x, k.SKOS + 'definition', self.L(definition))
        for gi in parts: add(g, x, k.DCT + 'hasPart', k.I(gi))
        add(g, x, k.OWL + 'versionInfo', k.L(version))
        for r in req: add(g, x, k.DCT + 'requires', k.I(r))
        self.gov(g, x, header=True)
        return g, gid, x

    def manifest(self, req):
        parts = [gi for gi, info in self.graphs.items() if info['manifest'] == 'assembly']
        label = f'Sales assembly {A.VERSION}'
        g, gid, x = self.manifest_graph(A.VERSION, A.VERSION, label,
            f'The Sales domain assembly, release {A.VERSION}: the Sales and Commercial Operations taxonomies, ontologies and shapes it requires, and the party, step, process and service graphs assembled from them (Service › Process › Process step, D24).', parts, req)
        self.manifest_iri = x[1]
        self.sales_write(g, gid, f'manifest-domain-sales-{A.VERSION}', f'{label} (manifest)', 'assembly')

    def value_map_manifest(self, req):
        parts = [gi for gi, info in self.graphs.items() if info['manifest'] == 'value-map']
        label = f'Sales value map {A.VALUE_MAP_VERSION}'
        g, gid, x = self.manifest_graph('value-map-' + A.VALUE_MAP_VERSION, A.VALUE_MAP_VERSION, label,
            f'The Sales value map, release {A.VALUE_MAP_VERSION}: the PEO buyer persona graph and the value-map graph that bridges the Sales assembly {A.VERSION} to it. A separate assembly from the Sales assembly, which it requires (D24).',
            parts, req + [self.manifest_iri])
        self.vm_manifest_iri = x[1]
        self.sales_write(g, gid, f'manifest-domain-sales-value-map-{A.VALUE_MAP_VERSION}', f'{label} (manifest)', 'value-map')

    def archive_superseded(self):
        """Move component files that are no longer current (older versions, removed graphs) out of the assembly folders."""
        current = {info['name'] for info in self.graphs.values()}
        dest = self.out / 'archive' / f'superseded-assembly-{A.VERSION}'
        moved = []
        for folder in (self.out / 'sales' / 'assembly', self.out / 'commercial-operations' / 'assembly'):
            for sub in ('ttl', 'trig'):
                for f in sorted((folder / sub).glob('*.' + sub)):
                    if f.stem not in current:
                        d = dest / folder.parent.name / sub; d.mkdir(parents=True, exist_ok=True)
                        f.rename(d / f.name); moved.append(f.name)
        self.moved = moved

    # ── validate ────────────────────────────────────────────────────────────
    PERSONA_TIERS = ('persona-graph', 'persona', 'job-study', 'job', 'job-step', 'desired-outcome', 'delivered-outcome')

    def merged(self, manifests):
        k = self.k
        data = collections.OrderedDict()
        for gi, info in self.graphs.items():
            if info['manifest'] not in manifests: continue
            for s, ps in info['g'].items():
                for p_, objs in ps.items():
                    for o in objs: add(data, s, p_, o)
        for s, ps in list(data.items()):       # owl:inverseOf, as a repository with inference would apply it
            for p_, objs in list(ps.items()):
                inv = self.inverse.get(p_)
                if inv:
                    for o in objs:
                        if o[0] == 'I': add(data, o, inv, s)
        return data

    def validate(self):
        k = self.k
        T = k.RDF + 'type'
        allowed = {'commercial-operations': {'core', 'commercial-operations'}, 'sales': {'core', 'commercial-operations', 'sales'}}
        sets = {'assembly': ('assembly',), 'value-map': ('assembly', 'value-map')}
        self.datasets = {name: self.merged(ms) for name, ms in sets.items()}
        for gi, info in self.graphs.items():
            scope = 'value-map' if info['manifest'] == 'value-map' else 'assembly'
            data = self.datasets[scope]
            typed = {s[1] for s, ps in data.items() if s[0] == 'I' and ps.get(T)}
            g = info['g']
            for s, ps in g.items():
                for p_, objs in ps.items():
                    for o in objs + [s]:
                        if o[0] != 'I': continue
                        m = re.match(re.escape(self.base) + r'(?:vocabulary|taxonomy|ontology|shapes|resource)/(core(?:-[a-z]+)?|domain-([a-z0-9-]+))/', o[1])
                        if m:
                            dom = m.group(2) or 'core'
                            if dom not in allowed[info['domain']]: self.errors.append(f'{info["name"]}: refers to sibling domain {dom}: {o[1]}')
                        if o[1].startswith(self.base + 'resource/domain-') and o[1] not in typed and o[1] not in (self.manifest_iri, self.vm_manifest_iri) and o[1] not in self.graphs:
                            self.errors.append(f'{info["name"]}: {short(self, o[1])} is not defined by any component in its manifest')
                        if scope == 'assembly' and re.match(re.escape(self.base) + r'resource/domain-[a-z0-9-]+/(' + '|'.join(self.PERSONA_TIERS) + ')/', o[1]):
                            self.errors.append(f'{info["name"]}: the service assembly refers to the value map or persona graph: {short(self, o[1])} (D24)')
                    if scope == 'assembly' and p_ == self.CORE + 'addresses':
                        self.errors.append(f'{info["name"]}: {short(self, s[1])} has core:addresses, which belongs in the value map, not the service assembly (D24)')
                    if p_ == T:
                        for o in objs:
                            if o[1] not in self.classes: self.errors.append(f'{info["name"]}: {short(self, s[1])} is typed by {short(self, o[1])}, which is not a core or domain class')
                    if p_ == k.DCT + 'type':
                        for o in objs:
                            if o[1] not in self.concepts: self.errors.append(f'{info["name"]}: {short(self, s[1])} is classified by {short(self, o[1])}, which is not a taxonomy concept')
            text = (info['folder'] / 'ttl' / f'{info["name"]}.ttl').read_text(encoding='utf-8')
            triples, _ = k.parse_turtle(text)
            _, res = k.check(triples, self.base, k.Policy(self.cfg), None)
            for rule, items in res.items():
                for sev, iri_, msg in items:
                    if sev == 'error': self.errors.append(f'{info["name"]}: {rule}: {short(self, iri_)}: {msg}')
        self.data = self.datasets['assembly']
        self.shape_results = self.run_shapes(self.datasets['assembly'])
        vm = self.run_shapes(self.datasets['value-map'])
        seen = set(self.shape_results)
        self.vm_shape_results = [r for r in vm if r not in seen]
        for sev, sh, n, msg, why in self.shape_results + self.vm_shape_results:
            (self.errors if sev == 'error' else self.warnings).append(f'SHACL {sh} on {n}: {msg} ({why})')

    def run_shapes(self, data):
        k = self.k
        T = k.RDF + 'type'
        S = collections.OrderedDict()
        for i, f in enumerate(self.model_files):
            if f.name.startswith('shapes-'):
                for s, p_, o in k.parse_turtle(f.read_text(encoding='utf-8'))[0]:
                    s, o = bnode(s, i), bnode(o, i)
                    S.setdefault(s, collections.OrderedDict()).setdefault(p_[1], []).append(o)
        def lst(t):
            out = []
            while t != ('I', k.RDF + 'nil') and t in S:
                out.append(S[t][k.RDF + 'first'][0]); t = S[t][k.RDF + 'rest'][0]
            return out
        def types(n):
            ts = {t[1] for t in data.get(n, {}).get(T, [])}
            return ts | {x for t in ts for x in self.supers(t)}
        results = []
        nshapes = 0
        for sh, ps in S.items():
            if k.I(k.SH + 'NodeShape') not in ps.get(T, []): continue
            nshapes += 1
            for tc in ps.get(k.SH + 'targetClass', []):
                focus = [n for n in data if n[0] == 'I' and tc[1] in types(n)]
                for pb in ps.get(k.SH + 'property', []):
                    P = S.get(pb, {})
                    path = P[k.SH + 'path'][0]
                    inverse = None
                    if path[0] == 'B': inverse = S[path][k.SH + 'inversePath'][0][1]
                    sev = 'warn' if P.get(k.SH + 'severity') == [k.I(k.SH + 'Warning')] else 'error'
                    msg = P[k.SH + 'message'][0][1]
                    mn = int(P[k.SH + 'minCount'][0][1]) if P.get(k.SH + 'minCount') else None
                    mx = int(P[k.SH + 'maxCount'][0][1]) if P.get(k.SH + 'maxCount') else None
                    cls = P.get(k.SH + 'class', [None])[0]
                    ors = [S[b][k.SH + 'class'][0][1] for b in lst(P[k.SH + 'or'][0])] if P.get(k.SH + 'or') else None
                    for n in focus:
                        if inverse: vals = [s for s, pp in data.items() if n in pp.get(inverse, [])]
                        else: vals = data.get(n, {}).get(path[1], [])
                        bad = None
                        if mn is not None and len(vals) < mn: bad = f'{len(vals)} value(s), at least {mn} required'
                        elif mx is not None and len(vals) > mx: bad = f'{len(vals)} values, at most {mx} allowed'
                        else:
                            for v in vals:
                                vt = types(v) if v[0] == 'I' else set()
                                if cls and cls[1] not in vt: bad = f'{short(self, v[1])} is not a {short(self, cls[1])}'; break
                                if ors and not any(c in vt for c in ors): bad = f'{short(self, v[1])} matches none of the allowed classes'; break
                        if bad:
                            results.append((sev, short(self, sh[1]), short(self, n[1]), msg, bad))
        self.nshapes = nshapes
        return results

    # ── measure ─────────────────────────────────────────────────────────────
    def parts(self, n):
        """The parts a node is joined from (D20). Primitives are atoms; concepts are joined from their primitives; a
        step from its classifying concepts and its SIPOCM (suppliers, inputs, performers and role, outputs, customers,
        measures); a process from its concepts and its steps; a service from its concept, the processes that enable it
        and its delivery step. Other instances from their concepts. The value map is not part of the service assembly."""
        k = self.k
        if n in self._parts: return self._parts[n]
        out = []
        if n[1] in self.primitives: out = []
        elif n[1] in self.concepts:
            out = [o for o in self.G.get(n, {}).get(k.DCT + 'subject', []) if o[0] == 'I' and o[1] in self.primitives]
        else:
            ps = self.data.get(n, {})
            CO = self.pfx['commercialops']
            for p_ in (k.DCT + 'type', CO + 'hasSupplier', self.CORE + 'consumes', self.CORE + 'performedBy', self.CORE + 'fulfillsRole',
                       self.CORE + 'produces', CO + 'hasCustomer', self.CORE + 'measuredBy', self.CORE + 'hasStep'):
                out += [o for o in ps.get(p_, []) if o[0] == 'I']
            if self.pfx['sales'] + 'sales-service' in {t[1] for t in ps.get(k.RDF + 'type', [])}:
                out += [s for s, pp in self.data.items() if n in pp.get(self.CORE + 'supports', []) or n in pp.get(self.CORE + 'deliveryOf', [])]
        seen, uniq = set(), []
        for o in out:
            if o not in seen and o != n: seen.add(o); uniq.append(o)
        self._parts[n] = uniq
        return uniq

    def closure(self, n, acc=None):
        acc = acc if acc is not None else set()
        if n in acc: return acc
        acc.add(n)
        for p_ in self.parts(n): self.closure(p_, acc)
        return acc

    def joins(self, n): return max(0, len(self.parts(n)) - 1)

    def tree(self, n, memo, stack=()):
        if n in memo: return memo[n]
        if n in stack: return 0
        v = self.joins(n) + sum(self.tree(p_, memo, stack + (n,)) for p_ in self.parts(n))
        memo[n] = v
        return v

    def kind(self, n):
        if n[1] in self.primitives: return 'primitive'
        if n[1] in self.concepts: return 'concept'
        m = re.match(re.escape(self.base) + r'resource/domain-[a-z0-9-]+/([a-z-]+)/', n[1])
        return m.group(1) if m else 'other'

    def measure(self):
        k = self.k
        self._parts = {}
        services = [k.I(self.iri('service:' + s[0])) for s in A.SERVICES]
        self.svc = []
        memo = {}
        closures = {}
        for s in services:
            c = self.closure(s)
            closures[s] = c
            ai = sum(self.joins(n) for n in c)
            tr = self.tree(s, memo)
            self.svc.append(dict(iri=s, label=self.label.get(s[1]) or self.data[s][k.SKOS + 'prefLabel'][0][1], ai=ai, tree=tr, nodes=len(c),
                                 prim=sum(1 for n in c if self.kind(n) == 'primitive')))
        union = set().union(*closures.values())
        self.union_ai = sum(self.joins(n) for n in union)
        self.sum_ai = sum(x['ai'] for x in self.svc)
        self.copy = []
        for n in union:
            cn = sum(1 for c in closures.values() if n in c)
            lab = (self.data.get(n, {}).get(k.SKOS + 'prefLabel') or self.G.get(n, {}).get(k.SKOS + 'prefLabel') or [('L', n[1].rsplit('/', 1)[-1])])[0][1]
            self.copy.append(dict(iri=n[1], label=lab, kind=self.kind(n), copy=cn, joins=self.joins(n),
                                  closure_joins=sum(self.joins(m) for m in self.closure(n))))
        self.copy.sort(key=lambda r: (-r['copy'], -r['closure_joins'], r['kind'], r['label']))
        # value map: desired outcomes of the job steps each service's steps address, against the delivered baseline
        self.gaps = []
        for sv in A.SERVICES:
            addressed = []
            for s in self.service_steps(sv):
                addressed += [j for j in A.ADDRESSES.get(s, []) if j not in addressed]
            for j in addressed:
                info = self.js[j.split(':', 1)[1]]
                for o in info['outcomes']:
                    b, t = o['baseline'], o['target']
                    if b is None: status = 'Not yet measured'
                    elif (o['direction'] == 'min' and b > t) or (o['direction'] == 'max' and b < t): status = 'Value gap'
                    else: status = 'Met'
                    self.gaps.append(dict(service=sv[1], job_step=j.split(':', 1)[1], job_step_label=info['label'], persona=info['persona'],
                                          outcome=f'{j.split(":", 1)[1]}.{o["n"]}', statement=o['stmt'], metric_card=o['card'], unit=o['unit'],
                                          direction='minimize' if o['direction'] == 'min' else 'maximize', target=t, baseline=b, status=status,
                                          gap=(round(b - t, 3) if b is not None else None)))

    # ── report ──────────────────────────────────────────────────────────────
    def sipocm(self, sref):
        """Suppliers, inputs, step, outputs, customers and measures of a step, with derived suppliers and customers."""
        k = self.k
        x = self.I(sref); ps = self.data.get(x, {})
        CO = self.pfx['commercialops']
        lab = lambda n: (self.data.get(n, {}).get(k.SKOS + 'prefLabel') or [('L', n[1].rsplit('/', 1)[-1])])[0][1]
        ins = [o for o in ps.get(self.CORE + 'consumes', [])]
        outs = [o for o in ps.get(self.CORE + 'produces', [])]
        sup = [lab(o) + ' (outside)' for o in ps.get(CO + 'hasSupplier', [])]
        cus = [lab(o) + ' (outside)' for o in ps.get(CO + 'hasCustomer', [])]
        for i in ins:
            for s, pp in self.data.items():
                if s != x and i in pp.get(self.CORE + 'produces', []) and pp.get(self.CORE + 'performedBy'): sup.append(lab(s))
        for o in outs:
            for s, pp in self.data.items():
                if s != x and o in pp.get(self.CORE + 'consumes', []) and pp.get(self.CORE + 'performedBy'): cus.append(lab(s))
        uniq = lambda xs: list(dict.fromkeys(xs))
        return dict(S=uniq(sup), I=[lab(o) for o in ins], P=lab(x) + ' — ' + ', '.join(lab(o) for o in ps.get(self.CORE + 'performedBy', [])),
                    O=[lab(o) for o in outs], C=uniq(cus), M=[lab(o) for o in ps.get(self.CORE + 'measuredBy', [])])

    def report(self):
        folder = self.out / 'sales' / 'assembly'
        with (folder / 'assembly-measures.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['label', 'kind', 'copy', 'joins', 'closure_joins', 'iri']); w.writeheader()
            for r in self.copy: w.writerow({kk: r[kk] for kk in ['label', 'kind', 'copy', 'joins', 'closure_joins', 'iri']})
        with (folder / 'value-gaps.csv').open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(self.gaps[0].keys())); w.writeheader(); w.writerows(self.gaps)
        shared = [r for r in self.copy if r['copy'] > 1]
        by_kind = collections.Counter(r['kind'] for r in shared)
        L = ['# Sales assembly report', '',
             f'Built {self.now[1]} by `_build/build_assembly.py`.', '',
             f'- **Sales assembly {A.VERSION}** (`{self.manifest_iri}`): Service › Process › Process step (D24).',
             f'- **Sales value map {A.VALUE_MAP_VERSION}** (`{self.vm_manifest_iri}`): a separate assembly that bridges the Sales assembly to the PEO buyer personas.', '',
             '## Components', '', '| Graph | Kind | Release | Version | Resources | Triples |', '|---|---|---|---|---:|---:|']
        for gi, info in self.graphs.items():
            nres = sum(1 for s in info['g'] if s[0] == 'I' and s[1] != gi)
            ntr = sum(len(v) for ps in info['g'].values() for v in ps.values())
            rel = {'assembly': 'Sales assembly', 'value-map': 'Sales value map'}[info['manifest']]
            L.append(f'| `{info["name"]}` | {info["name"].split("-domain-")[0].replace("-", " ")} | {rel} | {info["version"]} | {nres} | {ntr} |')
        if getattr(self, 'moved', None):
            L += ['', f'Superseded and moved to `archive/superseded-assembly-{A.VERSION}/`: ' + ', '.join(f'`{m}`' for m in self.moved) + '.']
        L += ['', '## How each service is assembled', '']
        for sv in A.SERVICES:
            L += [f'### {sv[1]}', '', f'Enabled by ' + ' and '.join(next(p[1] for p in A.PROCESSES if 'process:' + p[0] == pr).lower() for pr in sv[5]) + f'; delivered by {self.steps[sv[4]]["label"].lower()}.', '',
                  '| Process | Step | Suppliers | Inputs | Performed by | Outputs | Customers | Measures |', '|---|---|---|---|---|---|---|---|']
            for pr in sv[5]:
                p = next(p for p in A.PROCESSES if 'process:' + p[0] == pr)
                for s in p[4]:
                    x = self.sipocm(s)
                    who = x['P'].split(' — ', 1)[1]
                    L.append(f'| {p[1]} | {self.steps[s]["label"]}{" (delivery)" if s == sv[4] else ""} | {"; ".join(x["S"]) or "—"} | {"; ".join(x["I"]) or "—"} | {who} | {"; ".join(x["O"])} | {"; ".join(x["C"]) or "—"} | {"; ".join(x["M"])} |')
            L.append('')
        L += ['Suppliers and customers marked *(outside)* are stated with has supplier and has customer; the others are derived from the data flow: the step that produces an input, or that consumes an output (D24).', '',
              '## Checks', '',
              f'- Errors: **{len(self.errors)}** · warnings: **{len(self.warnings)}**.',
              '- For each manifest: every instance is typed by a core or domain class and classified by an existing taxonomy concept; every graph refers only to the core, the Commercial Operations container and its own domain; every resource referred to is defined by a component in that manifest. The Sales assembly does not refer to the persona graph or the value map.',
              f'- SHACL: {self.nshapes} node shapes (core, Commercial Operations, Sales and the other domains) run over the Sales assembly, and again over the assembly with the value map, after the ontologies\' owl:inverseOf pairs are applied.', '']
        other = [e for e in self.errors if not e.startswith('SHACL')]
        if other: L += ['| Error |', '|---|'] + [f'| {e} |' for e in other] + ['']
        for title, rows in (('Sales assembly', self.shape_results), ('Added by the value map', self.vm_shape_results)):
            grp = collections.OrderedDict()
            for sev, sh, n, msg, why in rows:
                grp.setdefault((sev, sh, msg), []).append(n.rsplit('/', 2)[-2] + '/' + n.rsplit('/', 1)[-1])
            L += [f'**{title}:** ' + ('no findings.' if not grp else f'{len(rows)} findings.'), '']
            if grp:
                L += ['| Severity | Shape | Finding | Focus nodes |', '|---|---|---|---|']
                for (sev, sh, msg), ns in grp.items():
                    L.append(f'| {sev} | `{sh.rsplit("/", 1)[-1]}` ({sh.split("/")[2]}) | {msg} | {len(ns)}: {", ".join(ns[:6])}{" …" if len(ns) > 6 else ""} |')
                L.append('')
        L += ['## Assembly measures', '',
              'A node\'s **joins** are the parts it is joined from, less one (n parts take n − 1 joins). Primitives are atoms (0 joins); a taxonomy concept is joined from its primitives; a step from its concepts and its SIPOCM (suppliers, inputs, performers and role, outputs, customers, measures); a process from its concepts and its steps; a service from its concept, the processes that enable it and its delivery step. The value map is not counted.', '',
              '**Assembly index (modeled pathway)** is the number of joins in the service\'s closure, each shared part counted once. It is the length of the pathway the model records, so it is an upper bound on the true assembly index (the shortest possible pathway). **Without reuse** counts every part again wherever it is used. **Copy number** is how many services contain a part.', '',
              '| Service | Nodes in closure | Primitives | Assembly index (modeled) | Without reuse | Saved by reuse |', '|---|---:|---:|---:|---:|---:|']
        for x in self.svc:
            L.append(f'| {x["label"]} | {x["nodes"]} | {x["prim"]} | {x["ai"]} | {x["tree"]} | {x["tree"] - x["ai"]} |')
        L += ['', f'Assembled together, the two services take **{self.union_ai}** joins, against **{self.sum_ai}** built separately: **{self.sum_ai - self.union_ai}** joins ({round(100 * (self.sum_ai - self.union_ai) / self.sum_ai)}%) are saved because the services share parts.', '',
              f'**Shared parts** (copy number > 1): {len(shared)} — ' + ', '.join(f'{v} {kk}{"s" if v != 1 else ""}' for kk, v in by_kind.most_common()) + '. The shared processes, steps and records are the platform candidates (Baseline decision 14):', '',
              '| Part | Kind | Copy number | Joins in its closure |', '|---|---|---:|---:|']
        for r in [r for r in shared if r['kind'] not in ('primitive', 'concept')][:20]:
            L.append(f'| {r["label"]} | {r["kind"].replace("-", " ")} | {r["copy"]} | {r["closure_joins"]} |')
        L += ['', 'All parts, with copy number and joins: `assembly-measures.csv`.', '',
              f'## Value map (Sales value map {A.VALUE_MAP_VERSION})', '',
              'A separate assembly (D24). For each job step a service\'s steps address (core:addresses, in the value-map graph), each desired outcome (persona graph) is compared with what the service delivers today (delivered outcome, value-map graph). Same job step, same metric card. These results will be shown on the Value Mapping page.', '',
              '| Service | Job step | Desired outcome | Target | Baseline | Status |', '|---|---|---|---:|---:|---|']
        for g_ in self.gaps:
            L.append(f'| {g_["service"]} | {g_["job_step"]} {g_["job_step_label"]} | {g_["statement"]} ({g_["unit"]}) | {fmt(g_["target"])} | {fmt(g_["baseline"])} | {g_["status"]} |')
        cnt = collections.Counter(g_['status'] for g_ in self.gaps)
        L += ['', f'{cnt["Value gap"]} value gaps, {cnt["Met"]} met, {cnt["Not yet measured"]} not yet measured. All rows: `value-gaps.csv`.', '']
        (folder / 'assembly-report.md').write_text('\n'.join(L), encoding='utf-8')
        print('\n'.join(L))


def fmt(v): return '' if v is None else (str(int(v)) if float(v).is_integer() else str(v))


def bnode(t, i):
    return ('B', f'f{i}_{t[1]}') if t[0] == 'B' else t


def add(g, s, p, o):
    lst = g.setdefault(s, collections.OrderedDict()).setdefault(p, [])
    if o not in lst: lst.append(o)


def short(b, iri): return iri.replace(b.base, '…/')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--core', default=str(AREA.parent.parent / 'KE Baseline' / 'Baseline Core v1.0' / 'ttl'))
    ap.add_argument('--ingest', default=str(AREA.parent.parent / 'KE Workbench' / 'ingest'))
    ap.add_argument('--out', default=str(AREA))
    a = ap.parse_args(argv)
    x = Asm(a)
    x.build(); x.archive_superseded(); x.validate(); x.measure(); x.report()
    return 1 if x.errors else 0


if __name__ == '__main__':
    sys.exit(main())
