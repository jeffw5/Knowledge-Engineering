#!/usr/bin/env python3
"""Pending terms and their disposition (Semantic Governance v2.3, A8).

A label or concept proposal that cannot be resolved to an existing concept in its scope does not create a concept. It is
stored here in the pending state and routed to the human trustee, whose decision passes the AI circuit breaker gateway
(ingest_api.evaluate_decision) like every other decision. The steward chooses exactly one disposition:

  alternate-label   another name for an existing concept; record it in the right lexicon (A7)
  domain-concept    new for the domain; mint a concept with a derivation edge (A2, A5)
  core-change       a gap in the core; open a core change under the core release process (A1)
  reject            record the reason in the change log

A pending term may exist in DEV and STG only; a release containing one fails the label resolution check (A6).
File: ingest/feedback/pending.jsonl (append-only; a later line for the same id wins).
"""
import datetime, json, pathlib, uuid

WB = pathlib.Path(__file__).resolve().parent.parent
FILE = WB / 'ingest/feedback/pending.jsonl'
DISPOSITIONS = ('alternate-label', 'domain-concept', 'core-change', 'reject')
ENVIRONMENTS = ('DEV', 'STG')


def _now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).strftime('%Y-%m-%dT%H:%M:%SZ')


def _read():
    if not FILE.exists(): return []
    out = []
    for ln in FILE.read_text(encoding='utf-8').splitlines():
        try: out.append(json.loads(ln))
        except Exception: pass
    return out


def records():
    """Pending terms, newest state of each (a disposition line merges into its term)."""
    cur = {}
    for r in _read():
        cur[r['id']] = dict(cur.get(r['id'], {}), **r)
    return list(cur.values())


def add(items, env='DEV'):
    if env not in ENVIRONMENTS:
        return {'ok': False, 'error': f'A pending term may exist in {" and ".join(ENVIRONMENTS)} only, not in {env}'}
    FILE.parent.mkdir(parents=True, exist_ok=True)
    ids = []
    with open(FILE, 'a', encoding='utf-8') as fh:
        for it in items:
            if not (it.get('label') or '').strip():
                return {'ok': False, 'error': 'each pending term needs a label'}
            r = {'id': 'pend-' + uuid.uuid4().hex[:10], 'at': _now(), 'state': 'pending', 'env': env, 'kind': it.get('kind') or 'label',
                 'label': it['label'].strip(), 'scope': it.get('scope') or '', 'context': it.get('context') or '', 'proposedBy': it.get('proposedBy') or ''}
            fh.write(json.dumps(r, ensure_ascii=False) + '\n'); ids.append(r['id'])
    return {'ok': True, 'ids': ids}


def check_disposition(d):
    """The fields each disposition needs. Returns an error string or None."""
    k = d.get('disposition')
    if k not in DISPOSITIONS: return f'disposition must be one of {", ".join(DISPOSITIONS)}'
    if k == 'alternate-label' and not d.get('concept'): return 'an alternate label names the existing concept it labels (concept) and the lexicon (lexicon)'
    if k == 'alternate-label' and not d.get('lexicon'): return 'name the lexicon that holds the label (A7: the narrowest scope that fits)'
    if k == 'domain-concept' and not d.get('parent'): return 'a domain concept needs a derivation edge to a core or domain class (parent)'
    if k == 'core-change' and not d.get('changeRequest'): return 'name the core change request (changeRequest)'
    if k == 'reject' and not (d.get('rationale') or '').strip(): return 'record the reason for rejecting in the change log (rationale)'
    return None


def dispose(d, decision):
    """Record a disposition (already evaluated by the gateway: `decision` is its envelope). Only PASS takes effect."""
    r = {k: d.get(k) for k in ('id', 'disposition', 'concept', 'lexicon', 'parent', 'changeRequest', 'rationale', 'by', 'signOff') if d.get(k) is not None}
    r['at'] = _now(); r['decision'] = decision
    r['state'] = 'resolved' if decision.get('verdict') == 'PASS' else 'pending'
    FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE, 'a', encoding='utf-8') as fh:
        fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    return r


def get(pid):
    return next((r for r in records() if r['id'] == pid), None)
