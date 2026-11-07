#!/usr/bin/env python3
"""Pick up the latest edition of the Semantic Governance guide and point the workbench at it.

    python3 ingest/guide_sync.py            # from the "KE Workbench" folder; also POST /api/ingest/guide-sync

Looks for Semantic_Governance_v<MAJOR>.<MINOR>[_DRAFT].pdf in docs/ and in ../Semantic Governance/ (the newest PDF
there is copied into docs/). An amendment set for a later edition ("Semantic Governance Guide v2.3 — Amendment Set
(Draft).pdf", stored in docs/ as Semantic_Governance_v2.3_Amendment_Set_DRAFT.pdf) makes that edition the one in
force, with the full guide it amends recorded as baseEdition / baseFile, but only while no full guide for that edition
exists: once the amendments are merged and saved as Semantic_Governance_v<M>.<N>[_DRAFT].pdf (as v2.3 and v2.4 were), the
full guide takes over (kind: guide, previous: the edition before). Then:
  - writes assets/ke-guide.js (window.KE_GUIDE), which the shell, the Overview, the guide link, the Model Editor
    (Ontology) and the Operations Dashboard read;
  - sets conformsTo and standardsRef in ingest/ke-ingest.config.json to that edition, so every asset ingested or
    built from now on declares it (dcterms:conformsTo …/standard/semantic-governance/<edition>/);
  - when the edition changed, rebuilds the Operations Dashboard snapshot so its reports use the new edition.
"""
import datetime, json, pathlib, re, shutil, sys

WB = pathlib.Path(__file__).resolve().parent.parent
KE = WB.parent
DOCS = WB / 'docs'
GUIDE_JS = WB / 'assets/ke-guide.js'
CONFIG = WB / 'ingest/ke-ingest.config.json'
TITLE = 'Semantic Governance: Services, Architecture & Integration'
PAT = re.compile(r'^Semantic_Governance_v(\d+)\.(\d+)(_DRAFT)?\.pdf$', re.I)
# An amendment set proposes the next edition as changes to the full guide before it (v2.3 amends v2.2).
# It is stored in docs/ as Semantic_Governance_v<MAJOR>.<MINOR>_Amendment_Set[_DRAFT].pdf; the original title
# "Semantic Governance Guide v2.3 — Amendment Set (Draft).pdf" in ../Semantic Governance/ is copied under that name.
APAT = re.compile(r'^Semantic_Governance_v(\d+)\.(\d+)_Amendment_Set(_DRAFT)?\.pdf$', re.I)
ORIG_APAT = re.compile(r'^Semantic Governance Guide v(\d+)\.(\d+)\s*\W+\s*Amendment Set(?:\s*\(Draft\))?\.pdf$', re.I)


def _key(p):
    m = PAT.match(p.name)
    return (int(m.group(1)), int(m.group(2)))


def editions():
    found = {}
    for d in (DOCS, KE / 'Semantic Governance'):
        if d.is_dir():
            for p in d.iterdir():
                if PAT.match(p.name):
                    k = _key(p)
                    # prefer the copy in docs/ (served by the workbench)
                    if k not in found or p.parent == DOCS:
                        found[k] = p
    return dict(sorted(found.items()))


def amendments():
    """{(major, minor): path} of amendment sets, docs/ copy preferred."""
    found = {}
    for d in (DOCS, KE / 'Semantic Governance'):
        if d.is_dir():
            for p in d.iterdir():
                m = APAT.match(p.name) or ORIG_APAT.match(p.name)
                if m:
                    k = (int(m.group(1)), int(m.group(2)))
                    if k not in found or p.parent == DOCS:
                        found[k] = p
    return dict(sorted(found.items()))


def current():
    if not GUIDE_JS.exists():
        return None
    m = re.search(r'window\.KE_GUIDE\s*=\s*(\{.*\});', GUIDE_JS.read_text(encoding='utf-8'), re.S)
    try:
        return json.loads(m.group(1)) if m else None
    except Exception:
        return None


def sync(rebuild=True):
    eds = editions()
    ams = amendments()
    if not eds and not ams:
        return {'ok': False, 'error': 'No Semantic_Governance_v*.pdf in docs/ or ../Semantic Governance/'}
    top_full = list(eds.items())[-1] if eds else None
    top_am = list(ams.items())[-1] if ams else None
    # an amendment set for a later edition than the newest full guide makes that edition the one in force
    amend = bool(top_am and (not top_full or top_am[0] > top_full[0]))
    (maj, mnr), src = top_am if amend else top_full
    edition = f'{maj}.{mnr}'
    base_file = base_ed = None
    if amend:
        if top_full:
            base_ed = f'{top_full[0][0]}.{top_full[0][1]}'
            bsrc = top_full[1]
            if bsrc.parent != DOCS:
                shutil.copyfile(bsrc, DOCS / bsrc.name); bsrc = DOCS / bsrc.name
            base_file = f'docs/{bsrc.name}'
        if not APAT.match(src.name):
            dst = DOCS / f'Semantic_Governance_v{maj}.{mnr}_Amendment_Set_DRAFT.pdf'
            shutil.copyfile(src, dst); src = dst
        draft = bool(APAT.match(src.name).group(3)) if APAT.match(src.name) else True
    else:
        if src.parent != DOCS:
            DOCS.mkdir(exist_ok=True)
            dst = DOCS / src.name
            shutil.copyfile(src, dst)
            src = dst
        draft = bool(PAT.match(src.name).group(3))
    date = datetime.date.fromtimestamp(src.stat().st_mtime).isoformat()
    cfg_txt = CONFIG.read_text(encoding='utf-8')
    cfg = json.loads(cfg_txt)
    base = cfg.get('baseUrl', 'https://www.insperity.com/')
    conforms = f'{base}standard/semantic-governance/{edition}/'
    ref = f'{TITLE} v{edition}' + (' (Draft)' if draft else '') + ', Part III'
    prev = current()
    guide = {
        'edition': edition, 'status': 'Draft' if draft else 'Released', 'date': date, 'title': TITLE,
        'file': f'docs/{src.name}', 'conformsTo': conforms, 'standardsRef': ref,
        'previous': (prev or {}).get('edition') if (prev or {}).get('edition') != edition else (prev or {}).get('previous'),
        'editions': sorted({f'{a}.{b}' for a, b in list(eds) + list(ams)}, key=lambda v: tuple(int(x) for x in v.split('.'))),
        'kind': 'amendment-set' if amend else 'guide', 'baseEdition': base_ed, 'baseFile': base_file,
        'syncedAt': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    if amend and base_ed:
        guide['previous'] = base_ed
    elif not guide['previous'] and len(eds) > 1:
        a, b = list(eds)[-2]
        guide['previous'] = f'{a}.{b}'
    changed = not prev or prev.get('edition') != edition or prev.get('file') != guide['file']
    if changed or not prev:
        GUIDE_JS.write_text('/* Generated by ingest/guide_sync.py: the edition of the Semantic Governance guide the workbench applies. */\n'
                            'window.KE_GUIDE = ' + json.dumps(guide, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
    # configuration: edit the text in place so key order and comments stay as they are
    new_txt = re.sub(r'(https?://[^"]*/standard/semantic-governance/)\d+\.\d+/', r'\g<1>' + edition + '/', cfg_txt)
    new_txt = re.sub(r'("standardsRef":\s*")[^"]*(")', lambda m: m.group(1) + ref + m.group(2), new_txt)
    new_txt = re.sub(r'(Architecture & Integration )v\d+\.\d+( \((?:Draft)\))?', r'\g<1>v' + edition + (' (Draft)' if draft else ''), new_txt)
    cfg_changed = new_txt != cfg_txt
    if cfg_changed:
        json.loads(new_txt)                      # still valid JSON
        CONFIG.write_text(new_txt, encoding='utf-8')
    summary = None
    if rebuild and (changed or cfg_changed):
        sys.path.insert(0, str(WB / 'ingest'))
        import importlib
        mod = importlib.import_module('build_ops_snapshot')
        mod = importlib.reload(mod)
        summary = mod.main()
    return {'ok': True, 'edition': edition, 'previous': guide['previous'], 'file': guide['file'], 'changed': changed,
            'configChanged': cfg_changed, 'snapshotRebuilt': summary is not None, 'summary': summary}


if __name__ == '__main__':
    r = sync(rebuild='--no-rebuild' not in sys.argv)
    print(json.dumps({k: v for k, v in r.items() if k != 'summary'}, indent=2))
    sys.exit(0 if r.get('ok') else 1)
