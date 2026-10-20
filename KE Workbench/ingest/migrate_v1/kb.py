"""Small helpers for editing the Baseline Core TTL/TriG files in place (house formatting via ke_ingest.Writer)."""
import collections, pathlib, re
import ke_ingest as k

BASE = 'https://www.insperity.com/'
CORE = BASE + 'ontology/core/'
SK, RDF, RDFS, OWL, DCT, XSD = k.SKOS, k.RDF, k.RDFS, k.OWL, k.DCT, k.XSD
TYPE = RDF + 'type'
I, L = k.I, k.L


class Asset:
    """One asset file: graph {subject: {pred: [objs]}} (pred as str), subject order, prefixes, header comment."""
    def __init__(self, path):
        self.path = pathlib.Path(path)
        text = self.path.read_text(encoding='utf-8')
        self.head = ''
        for ln in text.split('\n'):
            if not ln.startswith('#'): break
            if not ln.startswith('# Named graph:'): self.head += ln + '\n'
        triples, self.prefixes = k.parse_turtle(text)
        self.g, self.order = collections.OrderedDict(), []
        for s, p, o in triples:
            if s not in self.g: self.g[s] = collections.OrderedDict(); self.order.append(s)
            lst = self.g[s].setdefault(p[1], [])
            if o not in lst: lst.append(o)
        self.header = next(s for s in self.order if s[0] == 'I' and (
            I(SK + 'ConceptScheme') in self.g[s].get(TYPE, []) or I(OWL + 'Ontology') in self.g[s].get(TYPE, [])))
        self.iri = self.header[1]

    # ── access ──
    def subjects(self, typ=None):
        return [s for s in self.order if s[0] == 'I' and s in self.g and (typ is None or I(typ) in self.g[s].get(TYPE, []))]

    def concepts(self):
        return self.subjects(SK + 'Concept')

    def lit(self, s, p):
        v = [o[1] for o in self.g.get(s, {}).get(p, []) if o[0] == 'L']
        return v[0] if v else None

    def pref(self, s):
        return self.lit(s, SK + 'prefLabel') or self.lit(s, RDFS + 'label')

    def objs(self, s, p):
        return self.g.get(s, {}).get(p, [])

    # ── edit ──
    def add(self, s, p, o):
        if s not in self.g: self.g[s] = collections.OrderedDict(); self.order.append(s)
        lst = self.g[s].setdefault(p, [])
        if o not in lst: lst.append(o)

    def set(self, s, p, objs):
        if s not in self.g: self.g[s] = collections.OrderedDict(); self.order.append(s)
        if objs: self.g[s][p] = list(objs)
        else: self.g[s].pop(p, None)

    def remove(self, iris):
        """Remove subjects and every triple that points at them."""
        iris = set(iris)
        for s in list(self.g):
            if s[0] == 'I' and s[1] in iris:
                del self.g[s]
        for s, ps in self.g.items():
            for p in list(ps):
                ps[p] = [o for o in ps[p] if not (o[0] == 'I' and o[1] in iris)]
                if not ps[p]: del ps[p]
        self.order = [s for s in self.order if s in self.g]

    def rename(self, m):
        """Re-point IRIs (subjects and objects) through mapping m {old: new}."""
        if not m: return
        f = lambda t: I(m[t[1]]) if t[0] == 'I' and t[1] in m else t
        g2 = collections.OrderedDict()
        for s, ps in self.g.items():
            ns = f(s)
            d = g2.setdefault(ns, collections.OrderedDict())
            for p, objs in ps.items():
                lst = d.setdefault(m.get(p, p), [])
                for o in objs:
                    o2 = f(o)
                    if o2 not in lst: lst.append(o2)
        self.g = g2
        seen, order = set(), []
        for s in self.order:
            ns = f(s)
            if ns not in seen: seen.add(ns); order.append(ns)
        for s in self.g:
            if s not in seen: order.append(s)
        self.order = order
        if self.header[1] in m: self.header = I(m[self.header[1]]); self.iri = self.header[1]

    # ── write ──
    def write(self, ttl_dir, trig_dir, name=None, extra_prefixes=None):
        name = name or self.path.stem
        px = dict(self.prefixes); px.update(extra_prefixes or {})
        px.setdefault('core', CORE)
        w = k.Writer(px, [CORE + 'hasLifecycleStatus'] + k.GOV_TAIL[1:])
        subjects = [s for s in self.order if s[0] == 'I' and s in self.g]
        subjects.remove(self.header); subjects.insert(0, self.header)
        ttl = pathlib.Path(ttl_dir) / (name + '.ttl')
        ttl.write_text(w.write(self.g, subjects, self.head), encoding='utf-8')
        th = self.head.replace('\n# Standards', f'\n# Named graph: {self.iri}\n# Standards')
        (pathlib.Path(trig_dir) / (name + '.trig')).write_text(w.write_trig(self.g, subjects, th, self.iri), encoding='utf-8')
        return ttl


def norm(label):
    """Normalized label for matching: lower case, words singularized."""
    def sing(w):
        if len(w) > 4 and w.endswith('ies'): return w[:-3] + 'y'
        if len(w) > 4 and w.endswith(('sses', 'ches', 'shes', 'xes')): return w[:-2]
        if len(w) > 3 and w.endswith('s') and not w.endswith(('ss', 'us', 'is')): return w[:-1]
        return w
    return ' '.join(sing(w) for w in re.findall(r'[a-z0-9]+', label.lower().replace('&', ' and ')))


def slug(label):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', label.lower().replace('&', ' and '))).strip('-')
