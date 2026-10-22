"""Derive the activities and steps of each Commercial Operations domain from APQC PCF 7.4 and apqc_commercial.py (D28)."""
import pathlib, re
import apqc_commercial as X

HERE = pathlib.Path(__file__).resolve().parent


def load_pcf():
    rows = []
    for f in sorted(HERE.glob(f'apqc-pcf-{X.PCF_VERSION}-category-*.txt')):
        for line in f.read_text(encoding='utf-8').splitlines():
            m = re.match(r'^(\d+(?:\.\d+)*) (.+) \((\d+)\)$', line.strip())
            if m: rows.append(m.groups())
    return rows


def depth(n): return 1 if re.fullmatch(r'\d+\.0', n) else len(n.split('.'))


def parent(n):
    d = depth(n)
    if d == 1: return None
    if d == 2: return n.split('.')[0] + '.0'
    return n.rsplit('.', 1)[0]


def clean(name):
    s = X.LABELS.get(name)
    return s


def label_of(n, name):
    if n in X.LABELS: return X.LABELS[n]
    s = re.sub(r'\s*\([A-Z]{2,}\)', '', name)
    s = re.sub(r'(\w)/(\w)', r'\1 or \2', s)
    return s[0].upper() + s[1:]


class Model:
    def __init__(self):
        self.rows = load_pcf()
        self.el = {n: dict(num=n, name=name, id=pid, depth=depth(n)) for n, name, pid in self.rows}
        self.kids = {}
        for n in self.el:
            p = parent(n)
            if p: self.kids.setdefault(p, []).append(n)
        self.activities = {}   # id -> dict(owner, num (APQC element it is, or extends), ext, label, steps [ids], l3)
        self.steps = {}        # id -> dict(owner, activity, num, ext, label, definition)
        for n, e in self.el.items():
            o = X.owner(n)
            if o not in X.DOMAINS or X.not_applicable(n): continue
            d = e['depth']; kids = [k for k in self.kids.get(n, [])]
            is_act = (d == 4) or (d == 3 and not kids)
            if not is_act: continue
            l5 = [k for k in kids if X.owner(k) == o and not X.not_applicable(k)]
            steps = l5 if l5 else [n]
            self.activities[n] = dict(id=n, owner=o, num=n, ext=False, label=label_of(n, e['name']), l3=n if d == 3 else parent(n), steps=[])
            for s in steps:
                self.steps[s] = dict(id=s, owner=o, activity=n, num=s, ext=False, label=label_of(s, self.el[s]['name']))
                self.activities[n]['steps'].append(s)
        for xid, (o, kind, lab, d, ext) in X.EXTENSIONS.items():
            if kind == 'activity':
                l3 = ext if depth(ext) == 3 else (parent(ext) if depth(ext) == 4 else ext)
                self.activities[xid] = dict(id=xid, owner=o, num=ext, ext=True, label=lab, definition=d, l3=l3, steps=[])
        for xid, (o, kind, lab, d, ext) in X.EXTENSIONS.items():
            if kind == 'step':
                self.steps[xid] = dict(id=xid, owner=o, activity=ext, num=self.activities[ext]['num'], ext=True, label=lab, definition=d)
                if xid not in self.activities[ext]['steps']: self.activities[ext]['steps'].append(xid)
        for xid, a in self.activities.items():
            if a['ext'] and not a['steps']:           # an extension activity with no listed steps is one step
                self.steps[xid] = dict(id=xid, owner=a['owner'], activity=xid, num=a['num'], ext=True, label=a['label'], definition=a.get('definition'))
                a['steps'] = [xid]
        for a, order in X.STEP_ORDER.items():
            assert sorted(order) == sorted(self.activities[a]['steps']), a
            self.activities[a]['steps'] = order

    def expand(self, owner, refs):
        """Activities a service names: an activity id, or an L2/L3 number for every activity the owner has under it."""
        out = []
        for r in refs:
            if r in self.activities: hits = [r]
            else: hits = [a for a, v in self.activities.items() if v['owner'] == owner and (v['num'] == r or v['num'].startswith(r + '.')) and not v['ext']]
            out += [h for h in hits if h not in out]
        return out
