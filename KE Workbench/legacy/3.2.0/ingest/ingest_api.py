"""
KE Workbench — ingestion endpoints served by proxy.py under /api/ingest/.

The Ingestion page (tools/ingestion.html) calls these to browse folders on this
machine, scan source files, run ke_ingest.py, edit its config, show results in
Finder, and load the output into GraphDB. Everything runs locally: proxy.py
listens on localhost only, unless HOST is set to share it.

  GET  /api/ingest/defaults           config summary, home folder, last-used folders
  GET  /api/ingest/browse?path=…      sub-folders and RDF files in a folder
  POST /api/ingest/scan               {source, recursive, dest, ttlDir, trigDir}
  POST /api/ingest/run                {source, files?, dest, ttlDir, trigDir, recursive, overrides, timestamp}
  GET  /api/ingest/config             the config file's text
  POST /api/ingest/config             {text} — validated, previous version kept as .bak
  POST /api/ingest/reveal             {path} — open the folder in Finder
  POST /api/ingest/load               {repo, outputs:[{iri, ttl}], changeRecord:{graph, ttl}, force?} — refused while a
                                      file has a blocking conformance error (config "loadBlockingRules"), unless force
  GET  /api/ingest/policy             approved acronyms, expansions, organizations (for the checks)
  POST /api/ingest/policy             {approve: "ACR"} or {expansion: {acronym, text}} — added to the config
  GET  /api/ingest/review-files?dir=… the ingested Turtle files in a folder (default: the last run's ttl folder)
  POST /api/ingest/review-read        {paths:[…]} — the statements of those files, for Conformance Review
  POST /api/ingest/review-save        {files:[{path, graph, triples}], record} — rewrite .ttl and .trig, extend the change record
  GET  /api/ingest/load-plan?dir=…    what Load into GraphDB would send from an output folder (current files only)
  POST /api/ingest/load-folder        {dir, repo, force?} — replace each current asset's named graph, add the change records
  GET  /api/ingest/vocab-index?dir=…  the folder's vocabularies and all their terms (for taxonomy-term linking)
  POST /api/ingest/load-url           {url | path, graph, repo} — fetch an RDF file (a URL, or a file on this machine) and
                                      replace that named graph with it; the format is read from the file, not guessed by GraphDB
  GET  /api/ingest/define-status      whether an Anthropic API key is set (~/.ke-workbench.env or ANTHROPIC_API_KEY)
  POST /api/ingest/define             {items:[{id, label, broader, …}]} — definitions written by Claude
"""
import json, os, pathlib, platform, re, subprocess, sys, traceback, urllib.error, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
WORKBENCH = HERE.parent
sys.path.insert(0, str(HERE))
import ke_ingest  # noqa: E402

CONFIG = HERE / 'ke-ingest.config.json'
STATE = HERE / '.ingest-state.json'          # last-used folders, so the page can offer them again


def _path(p):
    p = pathlib.Path(os.path.expanduser(str(p or '').strip()))
    return p if p.is_absolute() else (WORKBENCH / p)


def _state(update=None):
    try:
        s = json.loads(STATE.read_text(encoding='utf-8'))
    except Exception:
        s = {}
    if update:
        s.update(update)
        try:
            STATE.write_text(json.dumps(s, indent=2), encoding='utf-8')
        except OSError:
            pass
    return s


def _send(h, code, obj):
    body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
    h.send_response(code)
    h.send_header('Content-Type', 'application/json; charset=utf-8')
    h.send_header('Content-Length', str(len(body)))
    h.end_headers()
    h.wfile.write(body)


def _body(h):
    n = int(h.headers.get('Content-Length') or 0)
    if not n:
        return {}
    return json.loads(h.rfile.read(n).decode('utf-8'))


def handle(h, method, graphdb_url):
    """Entry point from proxy.py. h is the BaseHTTPRequestHandler."""
    url = urllib.parse.urlparse(h.path)
    name = url.path[len('/api/ingest/'):].strip('/')
    q = {k: v[0] for k, v in urllib.parse.parse_qs(url.query).items()}
    try:
        fn = ROUTES.get((method, name))
        if not fn:
            return _send(h, 404, {'ok': False, 'error': f'No {method} /api/ingest/{name}'})
        data = _body(h) if method == 'POST' else q
        return _send(h, 200, fn(data, graphdb_url))
    except Exception as e:  # report, don't kill the server
        traceback.print_exc()
        return _send(h, 500, {'ok': False, 'error': f'{type(e).__name__}: {e}'})


# ── endpoints ────────────────────────────────────────────────────────────────
def defaults(_, __):
    cfg, path = ke_ingest.load_config(CONFIG)
    st = _state()
    return {'ok': True, 'home': str(pathlib.Path.home()), 'workbench': str(WORKBENCH), 'platform': platform.system(),
            'python': platform.python_version(), 'config': str(path),
            'settings': {k: cfg.get(k) for k in ('baseUrl', 'author', 'initialVersion', 'lifecycleStatus', 'standardsRef')},
            'assetsConfigured': sorted(cfg.get('assets', {})),
            'extensions': sorted(ke_ingest.RDF_EXTENSIONS),
            'last': {k: st.get(k) for k in ('source', 'dest', 'ttlDir', 'trigDir', 'recursive')}}


def browse(q, _):
    p = _path(q.get('path') or pathlib.Path.home())
    if not p.exists():
        # walk up to the nearest folder that exists, so a typo still lands somewhere useful
        probe = p
        while not probe.exists() and probe != probe.parent:
            probe = probe.parent
        return {'ok': False, 'error': f'{p} does not exist', 'nearest': str(probe)}
    if p.is_file():
        p = p.parent
    dirs, files = [], []
    try:
        for c in sorted(p.iterdir(), key=lambda x: x.name.lower()):
            if c.name.startswith('.'):
                continue
            if c.is_dir():
                dirs.append(c.name)
            elif c.suffix.lower() in ke_ingest.RDF_EXTENSIONS:
                files.append({'name': c.name, 'size': c.stat().st_size})
    except PermissionError:
        return {'ok': False, 'error': f'No permission to read {p}', 'nearest': str(p.parent)}
    return {'ok': True, 'path': str(p), 'parent': str(p.parent) if p.parent != p else None, 'dirs': dirs, 'files': files}


def _planned(rows, dest, ttl_dir, trig_dir, version):
    """Files this run would write, and which of them already exist."""
    if not dest:
        return [], []
    d = _path(dest)
    names = []
    for r in rows:
        if r.get('ok'):
            kind, domain = r['new_iri'].rstrip('/').split('/')[-2:]
            names.append(f'{kind}-{domain}-{version}')
    # shapes graphs appear only when an ontology holds SHACL shapes; predicted by name only
    out = [str(d / ttl_dir / f'{n}.ttl') for n in names] + [str(d / trig_dir / f'{n}.trig') for n in names]
    return out, [x for x in out if pathlib.Path(x).exists()]


def scan(b, _):
    src = _path(b.get('source'))
    if not src.exists():
        return {'ok': False, 'error': f'Source folder {src} does not exist'}
    cfg, _ = ke_ingest.load_config(CONFIG)
    known = ke_ingest.known_domains(_path(b['dest']), b.get('ttlDir') or 'ttl') if b.get('dest') else set()
    rows = ke_ingest.scan([src], cfg, bool(b.get('recursive')), known)
    for r in rows:
        r['rel'] = os.path.relpath(r['path'], src) if src.is_dir() else r['name']
    planned, existing = _planned(rows, b.get('dest'), b.get('ttlDir') or 'ttl', b.get('trigDir') or 'trig',
                                 (b.get('overrides') or {}).get('initialVersion') or cfg['initialVersion'])
    corrected = [x for x in existing if x.endswith('.ttl') and ke_ingest.is_corrected(x)]
    return {'ok': True, 'source': str(src), 'files': rows, 'planned': planned, 'existing': existing, 'corrected': corrected}


def run(b, _):
    src = _path(b.get('source'))
    dest = b.get('dest')
    if not dest:
        return {'ok': False, 'error': 'Choose a destination folder'}
    dest = _path(dest)
    ttl_dir = _safe_sub(b.get('ttlDir') or 'ttl')
    trig_dir = _safe_sub(b.get('trigDir') or 'trig')
    if ttl_dir == trig_dir:
        return {'ok': False, 'error': 'The Turtle and TriG folders must be different'}
    try:
        if src.is_dir() and dest.resolve().is_relative_to(src.resolve()) and b.get('recursive'):
            return {'ok': False, 'error': 'The destination is inside the source folder and subfolders are included; the next run would read its own output. Choose another destination.'}
    except AttributeError:  # Python < 3.9
        pass
    paths = [_path(p) for p in (b.get('files') or [])] or [src]
    cfg, _ = ke_ingest.load_config(CONFIG)
    log = []
    res = ke_ingest.run(paths, dest, cfg, ttl_dir, trig_dir, bool(b.get('recursive')) and not b.get('files'),
                        b.get('timestamp') or None, b.get('overrides') or {}, log=log.append)
    res['log'] = log
    if res.get('ok'):
        _state({'source': str(src), 'dest': str(dest), 'ttlDir': ttl_dir, 'trigDir': trig_dir, 'recursive': bool(b.get('recursive'))})
        print('  ingest: ' + '\n  ingest: '.join(log))
    return res


def _safe_sub(name):
    name = str(name).strip().strip('/')
    if not name or name.startswith('..') or os.path.isabs(name) or '/../' in f'/{name}/':
        raise ValueError(f'"{name}" is not a sub-folder name')
    return name


def config_get(_, __):
    return {'ok': True, 'path': str(CONFIG), 'text': CONFIG.read_text(encoding='utf-8')}


def config_save(b, _):
    text = b.get('text') or ''
    try:
        cfg = json.loads(text)
    except json.JSONDecodeError as e:
        return {'ok': False, 'error': f'Not valid JSON: line {e.lineno}, column {e.colno}: {e.msg}'}
    missing = [k for k in ('baseUrl', 'author', 'initialVersion', 'lifecycleStatus', 'standardsRef', 'sourceNamespaces') if k not in cfg]
    if missing:
        return {'ok': False, 'error': 'Missing setting' + ('s' if len(missing) > 1 else '') + ': ' + ', '.join(missing)}
    if not re.fullmatch(r'\d+\.\d+\.\d+', str(cfg['initialVersion'])):
        return {'ok': False, 'error': 'initialVersion must be MAJOR.MINOR.PATCH, for example 0.1.0'}
    for i, r in enumerate(cfg['sourceNamespaces']):
        try:
            rx = re.compile(r['pattern'])
        except (re.error, KeyError, TypeError) as e:
            return {'ok': False, 'error': f'sourceNamespaces[{i}]: {e}'}
        if 'domain' not in rx.groupindex and 'domain' not in r:
            return {'ok': False, 'error': f'sourceNamespaces[{i}] needs a (?P<domain>…) group or a "domain" value'}
    bak = CONFIG.with_suffix('.json.bak')
    bak.write_text(CONFIG.read_text(encoding='utf-8'), encoding='utf-8')
    CONFIG.write_text(text if text.endswith('\n') else text + '\n', encoding='utf-8')
    return {'ok': True, 'path': str(CONFIG), 'backup': str(bak)}


def reveal(b, _):
    p = _path(b.get('path'))
    if not p.exists():
        return {'ok': False, 'error': f'{p} does not exist'}
    cmd = {'Darwin': ['open'], 'Windows': ['explorer'], 'Linux': ['xdg-open']}.get(platform.system())
    if not cmd:
        return {'ok': False, 'error': 'Cannot open folders on this system'}
    if platform.system() == 'Darwin' and p.is_file():
        cmd = ['open', '-R']
    subprocess.Popen(cmd + [str(p)])
    return {'ok': True}


DEFAULT_BLOCKING = ['Base URL (§3.2)', "No other organization's content", 'Valid dates (ISO 8601)']


def blocking_errors(ttl_paths):
    """Conformance errors that stop a load into GraphDB (config "loadBlockingRules"; by default: terms outside the
    base URL, another organization's content, invalid dates). Returns [{file, rule, iri, msg}]."""
    cfg, _ = ke_ingest.load_config(CONFIG)
    rules = set(cfg.get('loadBlockingRules', DEFAULT_BLOCKING))
    if not rules:
        return []
    policy = ke_ingest.Policy(cfg)
    base = cfg['baseUrl'].rstrip('/') + '/'
    out = []
    for t in ttl_paths:
        p = pathlib.Path(t)
        try:
            triples, _ = ke_ingest.parse_turtle(p.read_text(encoding='utf-8'))
        except Exception as e:
            out.append({'file': p.name, 'rule': 'Valid Turtle', 'iri': '', 'msg': f'{type(e).__name__}: {e}'}); continue
        _, res = ke_ingest.check(triples, base, policy)
        for rule, items in res.items():
            if rule in rules:
                out += [{'file': p.name, 'rule': rule, 'iri': iri, 'msg': msg} for sev, iri, msg in items if sev == 'error']
    return out


def load(b, graphdb_url):
    """Replace each asset's named graph with its new content; append the change record.
    Refused while any file has a blocking conformance error, unless b['force'] is set."""
    repo = (b.get('repo') or 'value-kb').strip()
    if not re.fullmatch(r'[\w.-]+', repo):
        return {'ok': False, 'error': f'"{repo}" is not a repository ID'}
    if not b.get('force'):
        blocked = blocking_errors([o['ttl'] for o in b.get('outputs') or []])
        if blocked:
            files = sorted({x['file'] for x in blocked})
            return {'ok': False, 'blocked': blocked[:200], 'blockedCount': len(blocked), 'results': [], 'repo': repo,
                    'error': f'Not loaded: {len(blocked)} blocking conformance error{"s" if len(blocked) != 1 else ""} in '
                             f'{", ".join(files[:4])}{" …" if len(files) > 4 else ""} ({blocked[0]["rule"]}: {blocked[0]["msg"]}). '
                             'Resolve them in Conformance Review, or load anyway.'}
    endpoint = f'{graphdb_url.rstrip("/")}/repositories/{repo}/statements'
    results = []

    def send(method, graph, ttl_path):
        p = pathlib.Path(ttl_path)
        if p.suffix != '.ttl' or not p.is_file():
            return {'graph': graph, 'ok': False, 'error': f'{p.name} is not a Turtle file from this run'}
        url = endpoint + '?' + urllib.parse.urlencode({'context': f'<{graph}>'})
        req = urllib.request.Request(url, data=p.read_bytes(), method=method,
                                     headers={'Content-Type': 'text/turtle; charset=utf-8'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return {'graph': graph, 'ok': True, 'status': r.status, 'mode': 'replaced' if method == 'PUT' else 'appended', 'file': p.name}
        except urllib.error.HTTPError as e:
            return {'graph': graph, 'ok': False, 'error': f'GraphDB answered {e.code}: {e.read().decode("utf-8", "replace")[:300]}'}
        except urllib.error.URLError as e:
            return {'graph': graph, 'ok': False, 'error': f'GraphDB not reachable at {graphdb_url}: {e.reason}'}

    for o in b.get('outputs') or []:
        results.append(send('PUT', o['iri'], o['ttl']))         # PUT with context = replace that graph
    cr = b.get('changeRecord')
    if cr:
        results.append(send('POST', cr['graph'], cr['ttl']))   # POST = append to the change log
    return {'ok': all(r['ok'] for r in results), 'repo': repo, 'results': results}


def policy_get(_, __):
    cfg, _ = ke_ingest.load_config(CONFIG)
    a = cfg.get('acronyms', {}) or {}
    return {'ok': True, 'baseUrl': cfg.get('baseUrl'), 'author': cfg.get('author'),
            'approved': sorted(a.get('approved', [])), 'expansions': a.get('expansions', {}),
            'organizations': cfg.get('organizations', [])}


def policy_save(b, _):
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    a = cfg.setdefault('acronyms', {})
    a.setdefault('approved', []); a.setdefault('expansions', {})
    if b.get('approve'):
        tok = str(b['approve']).strip()
        if not re.fullmatch(r'[A-Za-z0-9-]{2,12}', tok):
            return {'ok': False, 'error': f'"{tok}" does not look like an acronym'}
        if tok.upper() not in {x.upper() for x in a['approved']}:
            a['approved'] = sorted(a['approved'] + [tok])
    elif b.get('expansion'):
        acr = str(b['expansion'].get('acronym', '')).strip().upper()
        text = str(b['expansion'].get('text', '')).strip()
        if not acr or not text:
            return {'ok': False, 'error': 'Give both the acronym and what it stands for'}
        a['expansions'][acr] = text
        a['expansions'] = dict(sorted(a['expansions'].items()))
    else:
        return {'ok': False, 'error': 'Nothing to change'}
    bak = CONFIG.with_suffix('.json.bak')
    bak.write_text(CONFIG.read_text(encoding='utf-8'), encoding='utf-8')
    CONFIG.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return policy_get(None, None)


# ── Conformance Review on ingested files (before they are loaded into GraphDB) ──
RX_HEAD2 = re.compile(r'^#\s*(\S+)\s+·\s+version\s+(\S+)', re.M)


def _twin(ttl):
    """The .trig written next to a .ttl by the same run: ../<trigDir>/<same name>.trig"""
    ttl = pathlib.Path(ttl)
    st = _state()
    cands = [ttl.parent.parent / (st.get('trigDir') or 'trig'), ttl.parent.parent / 'trig', ttl.parent]
    for d in cands:
        t = d / (ttl.stem + '.trig')
        if t.is_file():
            return t
    return None


def review_files(q, _):
    st = _state()
    d = q.get('dir') or (str(pathlib.Path(st['dest']) / (st.get('ttlDir') or 'ttl')) if st.get('dest') else '')
    if not d:
        return {'ok': True, 'dir': '', 'files': []}
    d = _path(d)
    if not d.exists() and st.get('dest'):
        d = _path(st['dest'])      # a folder remembered by the browser that has since moved
    if d.is_dir() and not any(d.glob('*.ttl')) and (d / (st.get('ttlDir') or 'ttl')).is_dir():
        d = d / (st.get('ttlDir') or 'ttl')           # a destination folder was given: use its ttl/ folder
    if not d.is_dir():
        return {'ok': False, 'error': f'{d} is not a folder'}
    plan = ke_ingest.folder_plan(d)            # current files only: superseded copies are never offered
    files = [{'path': str(h['path']), 'name': h['path'].name, 'title': h['title'], 'iri': h['iri'], 'version': h['version'],
              'kind': h['kind'], 'trig': str(_twin(h['path']) or '')} for h in plan['current'] if h['kind'] != 'shapes']
    return {'ok': True, 'dir': str(d), 'files': files}


def _enc(t):
    return [t[0], t[1]] if t[0] != 'L' else ['L', t[1], t[2] or '', t[3] or '']


def review_read(b, _):
    out = []
    for p in b.get('paths') or []:
        f = _path(p)
        if f.suffix != '.ttl' or not f.is_file():
            out.append({'path': str(f), 'ok': False, 'error': 'not a Turtle file'}); continue
        try:
            triples, _prefixes = ke_ingest.parse_turtle(f.read_text(encoding='utf-8'))
        except Exception as e:
            out.append({'path': str(f), 'ok': False, 'error': f'{type(e).__name__}: {e}'}); continue
        heads = [s[1] for s, p_, o in triples if p_[1] == ke_ingest.RDF + 'type' and o[1] in (ke_ingest.OWL + 'Ontology', ke_ingest.SKOS + 'ConceptScheme')]
        out.append({'path': str(f), 'ok': True, 'graph': heads[0] if heads else 'file:' + f.name,
                    'trig': str(_twin(f) or ''), 'triples': [[_enc(s), _enc(p_), _enc(o)] for s, p_, o in triples]})
    return {'ok': True, 'files': out}


def _dec(t):
    if t[0] == 'L':
        return ('L', t[1], (t[2] or None), (t[3] or None))
    return (t[0], t[1])


def _comment_head(text):
    lines = []
    for ln in text.split('\n'):
        if ln.startswith('#'):
            lines.append(ln)
        else:
            break
    return '\n'.join(lines) + ('\n' if lines else '')


def review_save(b, _):
    import collections, datetime, shutil
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
    written, backup_root = [], None
    for fobj in b.get('files') or []:
        f = _path(fobj['path'])
        if f.suffix != '.ttl' or not f.is_file():
            return {'ok': False, 'error': f'{f} is not an ingested Turtle file'}
        old = f.read_text(encoding='utf-8')
        _, prefixes = ke_ingest.parse_turtle(old)
        trig = _twin(f)
        # keep the originals once per save, next to the folders: review-backup-<stamp>/
        if backup_root is None:
            backup_root = f.parent.parent / f'review-backup-{stamp}'
        (backup_root / f.parent.name).mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, backup_root / f.parent.name / f.name)
        if trig:
            (backup_root / trig.parent.name).mkdir(parents=True, exist_ok=True)
            shutil.copy2(trig, backup_root / trig.parent.name / trig.name)
        # rebuild the graph: subjects in the order sent, header first, top-level blank nodes as [ … ] .
        g = collections.OrderedDict()
        objs = set()
        for s, p_, o in fobj['triples']:
            s, p_, o = _dec(s), _dec(p_), _dec(o)
            g.setdefault(s, collections.OrderedDict()).setdefault(p_[1], [])
            if o not in g[s][p_[1]]:
                g[s][p_[1]].append(o)
            if o[0] == 'B':
                objs.add(o)
        header = ('I', fobj['graph'])
        subjects = ([header] if header in g else []) + [s for s in g if s != header and (s[0] == 'I' or s not in objs)]
        w = ke_ingest.Writer(prefixes)
        note = f'# Corrected in Conformance Review on {stamp}\n'
        head = _comment_head(old)
        text = w.write(g, subjects, head + note)
        f.write_text(text, encoding='utf-8')
        item = {'ttl': str(f), 'triples': sum(len(v) for ps in g.values() for v in ps.values())}
        if trig and header in g:
            w2 = ke_ingest.Writer(prefixes)
            thead = _comment_head(trig.read_text(encoding='utf-8'))
            trig.write_text(w2.write_trig(g, subjects, thead + note, fobj['graph']), encoding='utf-8')
            item['trig'] = str(trig)
        written.append(item)
    # change record: append this review to the newest change record in the same folders (it is what Load sends)
    rec = b.get('record') or ''
    cr = None
    if rec and written:
        tdir = pathlib.Path(written[0]['ttl']).parent
        crs = sorted(tdir.glob('change-record-*.ttl'), key=lambda x: x.stat().st_mtime)
        pre = ''.join(f'@prefix {k}: <{v}> .\n' for k, v in (('rdfs', ke_ingest.RDFS), ('dct', ke_ingest.DCT),
                                                              ('prov', 'http://www.w3.org/ns/prov#'), ('xsd', ke_ingest.XSD)))
        graph = b.get('changeLog') or ''
        if crs:
            cr = crs[-1]
            with cr.open('a', encoding='utf-8') as fh:
                fh.write(f'\n# Conformance Review, {stamp}\n' + pre + rec + '\n')
        else:
            cr = tdir / f'change-record-{stamp}-review.ttl'
            cr.write_text(f'# Change record: Conformance Review, {stamp}\n' + pre + '\n' + rec + '\n', encoding='utf-8')
        ctrig = _twin(cr)
        if ctrig is None:
            st = _state()
            ctrig = cr.parent.parent / (st.get('trigDir') or 'trig') / (cr.stem + '.trig')
            if not ctrig.parent.is_dir():
                ctrig = None
            elif graph:
                ctrig.write_text(f'# Change record: Conformance Review, {stamp}\n', encoding='utf-8')
        if ctrig is not None and graph:
            with ctrig.open('a', encoding='utf-8') as fh:
                fh.write(f'\n# Conformance Review, {stamp}\n' + pre + f'<{graph}> {{\n' + rec + '\n}\n')
    return {'ok': True, 'written': written, 'backup': str(backup_root) if backup_root else '',
            'changeRecord': str(cr) if cr else ''}


def _out_dirs(d):
    """(dest, ttl folder, trig folder name) for a destination folder or its ttl folder."""
    st = _state()
    d = _path(d or st.get('dest') or '')
    if not d.exists() and st.get('dest'):
        d = _path(st['dest'])      # a folder remembered by the browser that has since moved (e.g. KE Baseline → Baseline Core v1.0)
    tname = st.get('ttlDir') or 'ttl'
    if (d / tname).is_dir():
        return d, d / tname, st.get('trigDir') or 'trig'
    return d.parent, d, st.get('trigDir') or 'trig'


def load_plan(q, _):
    dest, tdir, _ = _out_dirs(q.get('dir'))
    if not tdir.is_dir():
        return {'ok': False, 'error': f'{tdir} is not a folder'}
    plan = ke_ingest.folder_plan(tdir)
    corrected = lambda p: 'Corrected in Conformance Review' in p.read_text(encoding='utf-8', errors='replace')[:2000]
    blocked = blocking_errors([str(h['path']) for h in plan['current']])
    return {'ok': True, 'dest': str(dest), 'dir': str(tdir), 'blocked': blocked[:200], 'blockedCount': len(blocked),
            'assets': [{'name': h['path'].name, 'title': h['title'], 'iri': h['iri'], 'kind': h['kind'], 'version': h['version'],
                        'corrected': corrected(h['path'])} for h in plan['current']],
            'superseded': [h['path'].name for h in plan['superseded']],
            'changeRecords': [p.name for p in plan['change_records']]}


def vocab_index(q, _):
    """The vocabularies of an output folder and all their terms, for linking taxonomy terms."""
    dest, tdir, _ = _out_dirs(q.get('dir'))
    if not tdir.is_dir():
        return {'ok': False, 'error': f'{tdir} is not a folder'}
    plan = ke_ingest.folder_plan(tdir)
    vocabs = [{'iri': h['iri'], 'title': h['title'], 'path': str(h['path']), 'version': h['version']}
              for h in plan['current'] if h['kind'] == 'vocabulary']
    idx = ke_ingest.vocab_index(tdir)
    return {'ok': True, 'dir': str(tdir), 'vocabularies': sorted(vocabs, key=lambda v: v['title']),
            'terms': [{'iri': t, 'label': v[0], 'alts': v[1], 'scheme': v[2], 'definition': v[3]} for t, v in idx.items()]}


def _rdf_type(data, name=''):
    """Media type of an RDF file from its first bytes (then its name): RDF/XML, Turtle, N-Triples, JSON-LD."""
    head = data[:4000].lstrip(b'\xef\xbb\xbf').lstrip()
    low = head[:400].lower()
    if head.startswith(b'<?xml') or b'<rdf:rdf' in low or head.startswith(b'<rdf') or b'<owl:ontology' in low:
        return 'application/rdf+xml'
    if head.startswith((b'{', b'[')):
        return 'application/ld+json'
    n = name.lower()
    if n.endswith(('.nt',)):
        return 'application/n-triples'
    if n.endswith(('.owl', '.rdf', '.xml')):
        return 'application/rdf+xml'
    return 'text/turtle'


def load_url(b, graphdb_url):
    """Load a reference ontology (BFO, RO …) into its own named graph: the workbench fetches it, so GraphDB needs no
    internet access and never has to guess the format."""
    repo = (b.get('repo') or 'value-kb').strip()
    graph = (b.get('graph') or '').strip()
    if not re.fullmatch(r'[\w.-]+', repo):
        return {'ok': False, 'error': f'"{repo}" is not a repository ID'}
    if not re.match(r'^https?://\S+$', graph):
        return {'ok': False, 'error': 'Give the named graph as an http(s) IRI'}
    src = (b.get('url') or b.get('path') or '').strip()
    if not src:
        return {'ok': False, 'error': 'Give a URL or a file path'}
    try:
        if re.match(r'^https?://', src):
            req = urllib.request.Request(src, headers={'Accept': 'application/rdf+xml, text/turtle;q=0.9, application/n-triples;q=0.8, */*;q=0.1',
                                                       'User-Agent': 'KE-Workbench'})
            with urllib.request.urlopen(req, timeout=120) as r:      # follows the PURL's redirects
                data, name = r.read(), r.geturl()
        else:
            f = _path(src)
            if not f.is_file():
                return {'ok': False, 'error': f'{f} is not a file'}
            data, name = f.read_bytes(), f.name
    except urllib.error.HTTPError as e:
        return {'ok': False, 'error': f'{src} answered {e.code}'}
    except urllib.error.URLError as e:
        return {'ok': False, 'error': f'Could not download {src}: {e.reason} (this computer needs internet access; or give the path of a downloaded copy)'}
    ctype = _rdf_type(data, name)
    url = f'{graphdb_url.rstrip("/")}/repositories/{repo}/statements?' + urllib.parse.urlencode({'context': f'<{graph}>'})
    req = urllib.request.Request(url, data=data, method='PUT', headers={'Content-Type': ctype + '; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return {'ok': True, 'repo': repo, 'graph': graph, 'format': ctype, 'bytes': len(data), 'source': name}
    except urllib.error.HTTPError as e:
        return {'ok': False, 'error': f'GraphDB answered {e.code} for {ctype}: {e.read().decode("utf-8", "replace")[:300]}'}
    except urllib.error.URLError as e:
        return {'ok': False, 'error': f'GraphDB not reachable at {graphdb_url}: {e.reason}'}


def define_status(_, __):
    cfg, _ = ke_ingest.load_config(CONFIG)
    return {'ok': True, 'key': bool(ke_ingest.anthropic_key()), 'model': cfg.get('definitionModel') or 'claude-sonnet-5-5',
            'keyFile': str(ke_ingest.KEY_FILE)}


def define(b, _):
    """Definitions written by Claude for the given terms (label, broader term, siblings … as context)."""
    items = [i for i in (b.get('items') or []) if i.get('id') and i.get('label')][:200]
    if not items:
        return {'ok': False, 'error': 'No terms to define'}
    cfg, _ = ke_ingest.load_config(CONFIG)
    defs, model, err = ke_ingest.generate_definitions(items, cfg, log=lambda m: print('  define: ' + m))
    return {'ok': not err or bool(defs), 'definitions': defs, 'model': model, 'error': err}


def load_folder(b, graphdb_url):
    """Load an output folder: each current asset replaces its named graph; change records are added to the
    change log (re-adding one already loaded changes nothing — they hold no blank nodes). Superseded copies
    from earlier runs are set aside first, so they can never be loaded."""
    import datetime
    dest, tdir, trig_dir = _out_dirs(b.get('dir'))
    if not tdir.is_dir():
        return {'ok': False, 'error': f'{tdir} is not a folder'}
    cfg, _ = ke_ingest.load_config(CONFIG)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
    moved = ke_ingest.archive_superseded(dest, tdir.name, trig_dir, stamp, log=lambda m: print('  ingest: ' + m))
    plan = ke_ingest.folder_plan(tdir)
    log_graph = cfg['baseUrl'].rstrip('/') + '/graph/change-log'
    res = load({'repo': b.get('repo'), 'force': b.get('force'), 'outputs': [{'iri': h['iri'], 'ttl': str(h['path'])} for h in plan['current']]}, graphdb_url)
    if res.get('error'):
        return res
    for cr in plan['change_records']:
        r = load({'repo': b.get('repo'), 'force': True, 'changeRecord': {'graph': log_graph, 'ttl': str(cr)}}, graphdb_url)
        res['results'] += r.get('results', [])
        res['ok'] = res['ok'] and r.get('ok', False)
    res['setAside'] = moved
    return res


ROUTES = {
    ('GET', 'defaults'): defaults,
    ('GET', 'browse'): browse,
    ('POST', 'scan'): scan,
    ('POST', 'run'): run,
    ('GET', 'config'): config_get,
    ('POST', 'config'): config_save,
    ('POST', 'reveal'): reveal,
    ('POST', 'load'): load,
    ('GET', 'policy'): policy_get,
    ('POST', 'policy'): policy_save,
    ('GET', 'review-files'): review_files,
    ('POST', 'review-read'): review_read,
    ('POST', 'review-save'): review_save,
    ('GET', 'load-plan'): load_plan,
    ('POST', 'load-folder'): load_folder,
    ('GET', 'vocab-index'): vocab_index,
    ('POST', 'load-url'): load_url,
    ('GET', 'define-status'): define_status,
    ('POST', 'define'): define,
}
