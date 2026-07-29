"""
domain_agent.py  [SUPERSEDED -- kept for reference only, not imported by main.py]
----------------
This was the pilot's original, single-class agent. Architecture doc v1.1
splits this into two pieces to make reuse and domain isolation structural
properties of the code rather than just a convention:

  * chassis.py   -- the reusable, identical-for-every-domain runtime
  * cartridge.py -- the isolated, one-per-domain configuration and state

See those two files, and Section 3.1 of the design doc, for the current
design. This file is left in place only so the diff between "one class per
agent" and "shared chassis + isolated cartridge" is easy to see.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

from llm_backend import LLMBackend
from ontology import Concept, DomainOntology


@dataclass
class MappingProposal:
    concept: Concept
    confidence: float
    evidence: str
    agent_id: str


class DomainMappingAgent:
    def __init__(self, ontology: DomainOntology, backend: LLMBackend, agent_id: Optional[str] = None):
        self.ontology = ontology
        self.backend = backend
        self.agent_id = agent_id or f"agent::{ontology.domain}"

    def propose(self, artifact_text: str, top_k: int = 1) -> List[MappingProposal]:
        ranked = self.backend.propose(artifact_text, self.ontology.candidates())
        proposals = [
            MappingProposal(concept=c, confidence=conf, evidence=ev, agent_id=self.agent_id)
            for c, conf, ev in ranked[:top_k]
        ]
        return proposals
