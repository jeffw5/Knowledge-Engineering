#!/usr/bin/env python3
"""Telemetry events for the Operations Dashboard (Semantic Governance v2.3, A12: dashboards read telemetry events only).

Every check that computes a measure calls emit(); the dashboard (through ingest/build_ops_snapshot.py) reads the latest
event per (measure, graph) and never recomputes a measure from model files. A measure with no emitter is listed as
"not yet measured" (NOT_YET_MEASURED below).

Event: {at, measure, graph, value, unit, count, total, target, note, edition, emitter}
File:  data/ops/telemetry.jsonl (append-only; trimmed to the newest MAX_LINES lines).
"""
import json, pathlib

WB = pathlib.Path(__file__).resolve().parent.parent
FILE = WB / 'data/ops/telemetry.jsonl'
MAX_LINES = 40000

# The A11 structural measures and the check that emits each; None = no emitter yet.
STRUCTURAL = [
    ('correspondence-density', 'Correspondence density', 'ingest/structural_checks.py (A4 matrix)'),
    ('stem-reuse-ratio', 'Stem-reuse ratio', 'ingest/structural_checks.py (A1, A2)'),
    ('impact-radius', 'Impact radius', 'ingest/structural_checks.py (baseline); per change: change-impact query'),
    ('polyhierarchy-rate', 'Polyhierarchy rate', 'ingest/structural_checks.py (A3)'),
    ('domain-minted-primitive-share', 'Domain-minted primitive share', 'ingest/structural_checks.py (A2)'),
    ('promotion-backlog-age', 'Promotion-backlog age', 'ingest/pending.py (A8)'),
    ('hitl-disposition-mix', 'HITL disposition mix', 'ingest/pending.py (A8)'),
    ('orphan-rate', 'Orphan rate per graph', 'ingest/structural_checks.py (A6)'),
]
NOT_YET_MEASURED = [
    ('orphan-schema-binding', 'Schema binding coverage (A6.2)', 'No bound source-schema elements are modelled in the workbench yet.'),
]


def emit(events):
    FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FILE, 'a', encoding='utf-8') as fh:
        for e in events:
            fh.write(json.dumps(e, ensure_ascii=False, separators=(',', ':')) + '\n')
    lines = FILE.read_text(encoding='utf-8').splitlines()
    if len(lines) > MAX_LINES:
        FILE.write_text('\n'.join(lines[-MAX_LINES:]) + '\n', encoding='utf-8')


def events():
    if not FILE.exists(): return []
    out = []
    for ln in FILE.read_text(encoding='utf-8').splitlines():
        try: out.append(json.loads(ln))
        except Exception: pass
    return out


def latest():
    """The newest event per (measure, graph)."""
    cur = {}
    for e in events():
        cur[(e['measure'], e['graph'])] = e
    return list(cur.values())
