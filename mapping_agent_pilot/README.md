# Domain-Sovereign Mapping Agent — Pilot

A runnable implementation of *Domain-Sovereign Semantic-to-Metadata Mapping
Agent Architecture v1.1*: a single reusable **chassis** processes artifacts
for nine isolated **cartridges** -- the seven-agent roster from design doc
§3.2 (Finance/FP&A, Requirements Engineering, Systems Engineering/MBSE,
Systems Safety, Knowledge Systems, Enterprise Architecture, Decision
Analysis) plus two extra domains (Engineering, Legal) kept from the
original reuse proof. A deterministic gate decides what actually gets
committed, and a drift monitor can circuit-break any one cartridge's agent
without affecting the other eight.

Pure standard-library Python — no `pip install` and no API key required to
run it. That was a constraint of this sandbox (no PyPI/network access), not
a recommendation for production; see "Moving to production" below for
exactly what to swap in first.

## Run it

```bash
python3 main.py
```

Takes a few seconds. Prints, in order: every artifact's routing and agent
decision, a cross-domain reconciliation, the drift monitor's final state per
agent, the agent registry, and the resulting KGCL commit log
(`kgcl_log.jsonl`, regenerated fresh on every run).

## Component design: chassis and cartridge

This is the direct answer to "reuse and isolation." Every agent is built
from two component classes that never blend into one codebase (design doc
§3.1):

- **`chassis.py` — the reusable chassis.** One `AgentChassis` instance is
  constructed once in `main.py` and shared by every domain. Its `process()`
  method — retrieval, reasoning, validation, commit, telemetry — runs
  identically no matter which cartridge is passed in. A bug fix or a
  capability upgrade here applies to every domain simultaneously.
- **`cartridge.py` — the isolated cartridge.** A `DomainCartridge` bundles
  exactly one domain's ontology binding, agent identity, and tuning pack
  (system prompt / few-shot examples — the seam a real Domain Governance
  Team would retrain). Cartridges are never merged; retraining one never
  touches another.
- **`ontology.py`** now defines **nine** domains. Each one is a new
  cartridge (a new ontology + a couple of sample artifacts) added with
  **zero** changes to `chassis.py`, `router.py`, `validation.py`, `kgcl.py`,
  or `monitor.py` -- that is the reuse-and-isolation guarantee, demonstrated
  at roster scale rather than just as a two-domain toy.

`domain_agent.py` is the pilot's original single-class design, kept only so
the before/after is easy to diff against `chassis.py` + `cartridge.py`. It
is not imported by `main.py`.

## What the pilot actually demonstrates

Twenty-eight sample artifacts (`artifacts_sample.py`) are run through the
full pipeline. On a stock run you should see:

- **All nine content-type categories** (data structure, document, business
  rule, constraint, process map, event, measure, persona, outcome) proposed,
  validated, and committed at least once.
- **One failure of each kind** — a SHACL violation (missing required
  property), a SWRL violation (an inferred rule breach — invalid severity
  enum), and a PEP violation (a governance policy breach — an access scope
  that's structurally present but too broad) — all in the engineering
  domain.
- **A circuit-breaker trip** — after three rejections push the engineering
  agent's rolling rejection rate over 40%, its breaker trips. The very next
  engineering-routed artifact is quarantined without even being evaluated,
  even though it would otherwise have passed.
- **Isolation** — the finance and legal agents keep committing normally
  throughout, including after the engineering agent trips. One domain's
  degradation never touches another's.
- **Cross-domain reconciliation** — one artifact (a deployment gate that
  also triggers a budget review) is routed to both finance and engineering
  in parallel; both propose and validate independently, and the two
  accepted mappings are linked via a Mapping Ontology record rather than
  merged into one.
- **Reuse across the full roster** — all seven §3.2 agents (plus the two
  extra proof domains) run through the exact same chassis code; each was
  added as a new cartridge only.

## File map

| File | Role (design doc section) |
|---|---|
| `ontology.py` | Federated GraphDB + nine domain ontologies (SHACL-like shapes, SWRL-like rules, PEP policies) |
| `router.py` | Content & Context Router — 5D (WHO/WHAT/WHEN/WHERE/WHY) tagging and domain routing (§2) |
| `llm_backend.py` | The agent's reasoning step — **the seam where real Claude plugs in** (§3.1, §5.2) |
| `cartridge.py` | **Isolated cartridge** — one domain's ontology binding, identity, and tuning pack (§3.1) |
| `chassis.py` | **Reusable chassis** — the shared runtime every cartridge is loaded into (§3.1) |
| `domain_agent.py` | Superseded single-class design, kept for reference only — not imported by `main.py` |
| `validation.py` | Deterministic Validation Gate — SHACL / SWRL / PEP, in order (§3.4) |
| `reconciliation.py` | Cross-Domain Reconciliation (§3.5) |
| `kgcl.py` | KGCL Commit — the append-only, provenance-carrying change log (§3.6) |
| `monitor.py` | Drift & Governance Monitor — MTBH/Value-Drift proxies, per-agent circuit breaker (§3.7) |
| `registry.py` | Agent Registry — persistent identity, DEV/STG/PRD lifecycle (§3.8) |
| `artifacts_sample.py` | The 28 sample artifacts driving the demo run |
| `main.py` | Builds the shared chassis and all nine cartridges, then runs everything end to end |

## Recommended agent roster (design doc §3.2) -- now generated

These are the seven cartridges the design doc recommends building first,
grounded in the disciplines your own architecture already names. All seven
are implemented in `ontology.py` and running in the pilot:

| Agent | Owns (primary categories) | Sample artifacts |
|---|---|---|
| Finance / FP&A | Business rules, constraints, process maps, measures, outcomes | A01-A06, A09, A14 |
| Requirements Engineering | Data structures, constraints, documents | A17-A18 |
| Systems Engineering (MBSE) | Data structures, process maps, events | A19-A20 |
| Systems Safety (STPA/STAMP) | Constraints, events, business rules | A21-A22 |
| Knowledge Systems | Documents, data structures, personas | A23-A24 |
| Enterprise Architecture | Process maps, outcomes, measures | A25-A26 |
| Decision Analysis | Outcomes, measures, personas | A27-A28 |

Two extra cartridges (Engineering, Legal — A07-A16) are kept from the
original two/three-domain reuse proof; they are not part of the §3.2
roster but demonstrate the circuit breaker and cross-domain reconciliation
without being torn out.

Each roster agent is a `DomainCartridge` — a new ontology binding, agent id,
and tuning pack — loaded into the same `AgentChassis` in `main.py`. Adding
each one required no changes to chassis code, proving the reuse-and-
isolation guarantee at the scale the design doc actually recommends, not
just a two-domain toy example.

## Moving to production

This pilot intentionally keeps every stage's *shape* faithful to the design
while keeping every implementation swappable. In priority order:

1. **`llm_backend.py` → real Claude.** `AnthropicBackend` is already
   sketched out and activates automatically once `pip install anthropic`
   and `ANTHROPIC_API_KEY` are both present — no other file changes. This is
   also where you'd move to the Claude Agent SDK with MCP tool access to
   each cartridge's real vector DB, per the design doc's §3.1. Each
   cartridge's `tuning_pack` (system prompt, few-shot examples) is exactly
   what `AnthropicBackend` should read to build its per-domain prompt.

2. **`ontology.py` → real GraphDB.** Replace `DomainOntology`/`Concept`
   with a client against your actual triple store (real OWL classes, real
   SHACL shapes, real SWRL rules). `validation.py` should then call a real
   SHACL engine (e.g. `pyshacl`) and a real rule engine instead of the
   hand-written `shacl_check`/`swrl_check` functions — those functions are
   deliberately isolated so this swap doesn't touch `chassis.py`.

3. **Vector retrieval.** `HeuristicBackend`'s keyword overlap stands in for
   the two-level hybrid search (vector DB ANN search narrows candidates,
   ontology confirms validity) described in the design doc. A real domain
   vector DB (Pinecone/Weaviate-class) slots in as the first half of a real
   `LLMBackend.propose()` implementation, scoped per cartridge.

4. **MTBH dimensional stratification.** `monitor.py` tracks one aggregate
   rejection rate per agent to keep this demo readable. Production should
   stratify by WHO/WHAT/WHEN/WHERE/WHY per the design doc's §3.7, so a
   domain-routing failure doesn't trigger review of unrelated concept-
   resolution failures within the same agent.

5. **Circuit-breaker thresholds and reset.** The pilot's 40% threshold and
   its lack of any un-trip mechanism are placeholders. Production
   thresholds should be set per cartridge by that domain's Governance Team
   (see the design doc's open questions), and a tripped agent needs an
   explicit review-and-reset workflow rather than running forever quarantined.

6. **Build out the roster.** Add the remaining six cartridges from the
   recommended roster above, one at a time, each moving through its own
   DEV → STG → PRD lifecycle independently.
