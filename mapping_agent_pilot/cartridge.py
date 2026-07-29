"""
cartridge.py
------------
The isolated cartridge (design doc Section 3.1). Everything here is unique
to one domain and is never merged with, or influenced by, another domain's
cartridge:

  * the ontology binding (which SHACL/SWRL/PEP scope this agent may see)
  * the agent's own identity (its registry id)
  * its tuning pack -- the system prompt, few-shot examples, and evaluation
    set a Domain Governance Team curates to make this agent an expert in
    exactly one domain

The pilot's HeuristicBackend doesn't consume `tuning_pack` (it has no LLM
to prompt), but the field is real: it is exactly what `AnthropicBackend`
(see llm_backend.py) would read to build its system prompt once you wire in
real Claude. Retraining a domain means editing this object's tuning_pack --
nothing in chassis.py ever needs to change.
"""

from dataclasses import dataclass, field
from typing import Any, Dict

from ontology import DomainOntology


@dataclass
class DomainCartridge:
    domain: str
    ontology: DomainOntology
    agent_id: str
    tuning_pack: Dict[str, Any] = field(default_factory=dict)


def make_cartridge(ontology: DomainOntology, tuning_pack: Dict[str, Any] = None) -> DomainCartridge:
    return DomainCartridge(
        domain=ontology.domain,
        ontology=ontology,
        agent_id=f"agent::{ontology.domain}",
        tuning_pack=tuning_pack or {},
    )
