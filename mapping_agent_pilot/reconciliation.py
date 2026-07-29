"""
reconciliation.py
------------------
Cross-Domain Reconciliation (design doc Section 3.4).

When an artifact was routed to more than one domain and more than one
agent produced an *accepted* proposal, this doesn't merge them into one
record -- it creates a Mapping Ontology entry that links the two
domain-local mappings, preserving each domain's sovereignty over its own
half of the mapping.
"""

from dataclasses import dataclass
from typing import List

from kgcl import KGCLRecord


@dataclass
class MappingOntologyLink:
    artifact_id: str
    linked_concepts: List[str]  # concept URIs from different domains
    note: str


def reconcile(artifact_id: str, accepted_records: List[KGCLRecord]) -> MappingOntologyLink:
    domains = {r.where for r in accepted_records}
    concepts = [r.what for r in accepted_records]
    return MappingOntologyLink(
        artifact_id=artifact_id,
        linked_concepts=concepts,
        note=f"cross-domain artifact linked across {len(domains)} domains: {', '.join(sorted(domains))}",
    )
