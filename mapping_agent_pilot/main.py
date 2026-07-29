"""
main.py
-------
Orchestrates the full pilot pipeline end to end using the chassis/cartridge
component design (architecture doc v1.1, Section 3.1):

  One AgentChassis (shared, identical code) processes artifacts for three
  DomainCartridges (finance, engineering, legal -- each isolated: its own
  ontology, its own agent identity, its own tuning pack). Adding the legal
  domain to this pilot required a new cartridge and two sample artifacts --
  zero changes to chassis.py, router.py, validation.py, kgcl.py, or
  monitor.py. That is the reuse-and-isolation guarantee, demonstrated.

Run it with:  python3 main.py
No external packages or network access are required (see llm_backend.py
for the real-Claude seam, used automatically if ANTHROPIC_API_KEY is set
and the `anthropic` package is installed).
"""

from artifacts_sample import SAMPLE_ARTIFACTS
from cartridge import make_cartridge
from chassis import AgentChassis
from kgcl import KGCLCommitLog
from llm_backend import get_default_backend
from monitor import DriftMonitor
from ontology import build_federated_graph
from reconciliation import reconcile
from registry import AgentRegistry
from router import ContentContextRouter
from validation import ValidationGate

DOMAIN_SIGNAL_KEYWORDS = {
    # The seven-agent roster (design doc §3.2):
    "finance": ["budget", "forecast", "variance", "fiscal", "sox", "cfo", "quarter", "financial outcome",
                 "quarterly outcome", "kpi", "accuracy"],
    "requirements": ["requirement spec", "requirements specification", "requirement document", "req-", "traceability"],
    "mbse": ["system model", "mbse", "model-based systems engineering", "sysml", "integration test", "hw-sw"],
    "systems_safety": ["unsafe control action", "stpa", "hazard", "uca", "stamp", "safety review"],
    "knowledge_systems": ["vocabulary", "taxonomy", "ontology engineer", "knowledge system", "steward"],
    "enterprise_architecture": ["architecture decision", "adr", "architecture review", "enterprise architecture",
                                  "architecture alignment", "target state"],
    "decision_analysis": ["scenario outcome", "decision analysis", "scenario planning", "tradeoff review",
                            "decision maker", "executive stakeholder"],
    # Extra domains kept from the original reuse proof (not part of the §3.2 roster).
    # Kept deliberately specific (e.g. "user account schema" not bare "schema") so
    # they don't false-positive against unrelated roster domains that happen to
    # share a generic word like "schema" or "severity".
    # Note: router.py strips punctuation (including hyphens) before matching, so
    # signals must use the post-strip form -- "on call" (space), not "on-call".
    "engineering": ["deployment approval", "deployment gate", "release gate", "incident event", "outage",
                     "user account schema", "on call", "oncall", "pagerduty", "data retention", "release cadence"],
    "legal": ["contract", "nda", "counterparty", "legal review", "agreement", "legal document"],
}

# Stand-ins for what a real Domain Governance Team would curate. HeuristicBackend
# ignores these (it has no LLM to prompt); AnthropicBackend would use them to
# build each cartridge's system prompt. Kept here, not in chassis.py, because
# tuning packs are cartridge state, never chassis state.
TUNING_PACKS = {
    "finance": {"system_prompt": "You are the Finance/FP&A domain's mapping specialist...", "few_shot_examples": []},
    "requirements": {"system_prompt": "You are the Requirements Engineering domain's mapping specialist...", "few_shot_examples": []},
    "mbse": {"system_prompt": "You are the Systems Engineering (MBSE) domain's mapping specialist...", "few_shot_examples": []},
    "systems_safety": {"system_prompt": "You are the Systems Safety (STPA/STAMP) domain's mapping specialist...", "few_shot_examples": []},
    "knowledge_systems": {"system_prompt": "You are the Knowledge Systems domain's mapping specialist...", "few_shot_examples": []},
    "enterprise_architecture": {"system_prompt": "You are the Enterprise Architecture domain's mapping specialist...", "few_shot_examples": []},
    "decision_analysis": {"system_prompt": "You are the Decision Analysis domain's mapping specialist...", "few_shot_examples": []},
    "engineering": {"system_prompt": "You are the Engineering domain's mapping specialist...", "few_shot_examples": []},
    "legal": {"system_prompt": "You are the Legal domain's mapping specialist...", "few_shot_examples": []},
}

CIRCUIT_BREAKER_THRESHOLD = 0.4


def main():
    graph = build_federated_graph()
    backend = get_default_backend()
    backend_name = type(backend).__name__
    print(f"LLM backend in use: {backend_name}")
    if backend_name == "HeuristicBackend":
        print("  (no ANTHROPIC_API_KEY / anthropic package found -- running with the deterministic "
              "keyword-overlap stand-in. See llm_backend.py to wire in real Claude.)\n")
    else:
        print("  (calling Claude for real via the Anthropic API.)\n")

    # One shared chassis instance -- constructed once, used by every cartridge below.
    registry = AgentRegistry()
    monitor = DriftMonitor(circuit_breaker_threshold=CIRCUIT_BREAKER_THRESHOLD)
    kgcl_log = KGCLCommitLog("kgcl_log.jsonl")
    gate = ValidationGate(graph.domains)
    chassis = AgentChassis(backend=backend, gate=gate, kgcl_log=kgcl_log, monitor=monitor, registry=registry)

    # One isolated cartridge per domain. This is the only per-domain object in
    # the whole pipeline; everything else above is shared.
    cartridges = {}
    for domain_name, ontology in graph.domains.items():
        cartridge = make_cartridge(ontology, tuning_pack=TUNING_PACKS.get(domain_name, {}))
        chassis.load(cartridge)
        cartridges[domain_name] = cartridge

    print(f"Cartridges loaded into the shared chassis: {', '.join(cartridges.keys())}\n")

    router = ContentContextRouter(graph, DOMAIN_SIGNAL_KEYWORDS)

    print("=" * 100)
    print(f"{'ARTIFACT':<30} {'DOMAIN':<12} {'AGENT DECISION':<70}")
    print("=" * 100)

    for artifact in SAMPLE_ARTIFACTS:
        context = router.tag(artifact)
        accepted_records = []

        for domain in context.where:
            cartridge = cartridges[domain]
            outcome = chassis.process(
                cartridge=cartridge,
                artifact_id=artifact.artifact_id,
                artifact_text=artifact.text,
                artifact_metadata=artifact.metadata,
                when=context.when,
            )

            if outcome.status == "committed":
                accepted_records.append(outcome.record)
                print(f"{artifact.artifact_id:<30} {domain:<12} COMMITTED -> {outcome.concept_uri} ({outcome.detail})")
            elif outcome.status == "rejected":
                print(f"{artifact.artifact_id:<30} {domain:<12} REJECTED {outcome.detail}")
            elif outcome.status == "quarantined":
                print(f"{artifact.artifact_id:<30} {domain:<12} QUARANTINED -- {outcome.detail}")
            else:  # no_match
                print(f"{artifact.artifact_id:<30} {domain:<12} NO MATCH -- {outcome.detail}")

        if len(accepted_records) > 1:
            link = reconcile(artifact.artifact_id, accepted_records)
            print(f"{'':<30} {'':<12} RECONCILED -- {link.note}")

    print("\n" + "=" * 100)
    print("DRIFT & GOVERNANCE MONITOR")
    print("=" * 100)
    print(monitor.report())

    print("\n" + "=" * 100)
    print("AGENT REGISTRY")
    print("=" * 100)
    print(registry.report())

    committed = kgcl_log.read_all()
    print("\n" + "=" * 100)
    print(f"KGCL COMMIT LOG -- {len(committed)} mapping(s) written to kgcl_log.jsonl")
    print("=" * 100)
    for rec in committed:
        print(f"  {rec['artifact_id']:<28} -> {rec['what']:<30} (agent={rec['who']}, domain={rec['where']})")


if __name__ == "__main__":
    main()
