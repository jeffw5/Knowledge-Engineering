"""
validation.py
-------------
Stage: Deterministic Validation Gate (design doc Section 3.3 / RDSG Steps 1-3).

Three checks, in order. Any failure rejects the proposal with a reason --
nothing is silently dropped. This module is deliberately dumb and rule-based:
it must never consult the LLM. The whole point of the architecture is that
this layer overrules the agent, not the other way around.

In production, replace `shacl_check` with a real SHACL engine (e.g. pySHACL
against real shapes graphs) and `swrl_check` with a real rule engine. The
function signatures here are written so that swap doesn't touch any other
file.
"""

from dataclasses import dataclass
from typing import Optional

from ontology import Concept


@dataclass
class ValidationResult:
    passed: bool
    stage_failed: Optional[str]  # "shacl" | "swrl" | "pep" | None
    reason: Optional[str]


def shacl_check(artifact_metadata: dict, concept: Concept) -> Optional[str]:
    """Required-property invariant check. Returns an error string, or None if valid."""
    missing = [p for p in concept.required_properties if p not in artifact_metadata]
    if missing:
        return f"SHACL violation: missing required propert{'y' if len(missing)==1 else 'ies'}: {', '.join(missing)}"
    return None


def swrl_check(artifact: dict, concept: Concept) -> Optional[str]:
    if concept.swrl_rule is None:
        return None
    return concept.swrl_rule(artifact)


def pep_check(artifact: dict, concept: Concept, pep_policies: dict) -> Optional[str]:
    for tag in concept.pep_tags:
        policy = pep_policies.get(tag)
        if policy is None:
            continue
        error = policy(artifact)
        if error:
            return error
    return None


class ValidationGate:
    def __init__(self, ontology_by_domain: dict):
        self.ontology_by_domain = ontology_by_domain  # domain -> DomainOntology

    def validate(self, artifact_dict: dict, concept: Concept) -> ValidationResult:
        metadata = artifact_dict.get("metadata", {})

        error = shacl_check(metadata, concept)
        if error:
            return ValidationResult(False, "shacl", error)

        error = swrl_check(artifact_dict, concept)
        if error:
            return ValidationResult(False, "swrl", error)

        ontology = self.ontology_by_domain[concept.domain]
        error = pep_check(artifact_dict, concept, ontology.pep_policies)
        if error:
            return ValidationResult(False, "pep", error)

        return ValidationResult(True, None, None)
