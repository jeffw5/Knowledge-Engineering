"""
chassis.py
----------
The reusable chassis (design doc Section 3.1). One AgentChassis instance is
constructed once and shared by every domain in the pilot -- Finance,
Engineering, and Legal all call the exact same `process()` method. What
changes from call to call is only the DomainCartridge argument.

If you ever find yourself writing `if cartridge.domain == "finance": ...`
inside this file, that is a signal the logic belongs in a cartridge (or in
a cartridge-supplied tuning pack) instead -- the chassis must stay domain-
blind for the reuse guarantee to mean anything.

Owned centrally (in the design doc's terms: by the Semantic Governance
Center of Excellence), not by any one Domain Governance Team.
"""

from dataclasses import dataclass
from typing import Optional

from cartridge import DomainCartridge
from kgcl import KGCLCommitLog, KGCLRecord
from llm_backend import LLMBackend
from monitor import DriftMonitor
from registry import AgentRegistry
from validation import ValidationGate


@dataclass
class ProcessingOutcome:
    status: str  # "committed" | "rejected" | "quarantined" | "no_match"
    detail: str
    concept_uri: Optional[str] = None
    record: Optional[KGCLRecord] = None


class AgentChassis:
    def __init__(self, backend: LLMBackend, gate: ValidationGate, kgcl_log: KGCLCommitLog,
                 monitor: DriftMonitor, registry: AgentRegistry):
        self.backend = backend      # LLM reasoning client (shared)
        self.gate = gate            # deterministic validation gate (shared)
        self.kgcl_log = kgcl_log    # KGCL commit sink (shared)
        self.monitor = monitor      # drift & governance monitor (shared)
        self.registry = registry    # agent registry (shared)

    def load(self, cartridge: DomainCartridge):
        """Register a cartridge's agent identity. Call once per cartridge at startup --
        this is the only place a cartridge and the chassis's shared registry meet."""
        self.registry.register(cartridge.agent_id, cartridge.domain)
        self.registry.promote(cartridge.agent_id, "STG")
        self.registry.promote(cartridge.agent_id, "PRD")

    def process(self, cartridge: DomainCartridge, artifact_id: str, artifact_text: str,
                artifact_metadata: dict, when: str) -> ProcessingOutcome:
        """
        Retrieval -> reasoning -> validation -> commit -> telemetry, in that
        order. This method's code path is identical no matter which
        cartridge is passed in.
        """
        if self.monitor.is_tripped(cartridge.agent_id):
            return ProcessingOutcome("quarantined", f"circuit breaker tripped for {cartridge.agent_id}")

        # Retrieval + reasoning: shared backend, scoped only by this cartridge's
        # ontology candidates (and, with a real LLMBackend, this cartridge's tuning_pack).
        proposals = self.backend.propose(artifact_text, cartridge.ontology.candidates())
        if not proposals:
            self.monitor.record_outcome(cartridge.agent_id, accepted=False)
            return ProcessingOutcome("no_match", "no candidate concept above threshold")

        concept, confidence, evidence = proposals[0]
        artifact_dict = {"metadata": artifact_metadata, "artifact_id": artifact_id}

        # Deterministic validation gate: shared code, cartridge-scoped ontology/PEPs.
        result = self.gate.validate(artifact_dict, concept)
        if not result.passed:
            self.monitor.record_outcome(cartridge.agent_id, accepted=False)
            return ProcessingOutcome("rejected", f"[{result.stage_failed}] {result.reason}", concept.uri)

        # Commit + telemetry: shared code.
        record = KGCLRecord(
            what=concept.uri,
            who=cartridge.agent_id,
            when=when,
            where=cartridge.domain,
            why=f"confidence={confidence} ({evidence})",
            artifact_id=artifact_id,
            confidence=confidence,
            validation="passed: shacl, swrl, pep",
        )
        self.kgcl_log.commit(record)
        self.monitor.record_outcome(cartridge.agent_id, accepted=True)
        return ProcessingOutcome("committed", f"confidence={confidence}", concept.uri, record)
