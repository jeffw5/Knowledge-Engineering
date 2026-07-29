"""
router.py
---------
Stage 0 / Stage 1 of the pipeline: Content & Context Router.

Tags an incoming artifact with the five relevancy dimensions
(WHO/WHAT/WHEN/WHERE/WHY) and decides which domain(s) -- the WHERE
dimension -- should receive it. An artifact can legitimately route to more
than one domain; the router does not force a single-domain assignment
(Section 1.1, Section 3.4 of the design doc).
"""

import datetime
import re
from dataclasses import dataclass, field
from typing import Dict, List

from ontology import FederatedGraphDB


@dataclass
class RelevancyContext:
    who: str
    what: str
    when: str
    where: List[str]     # one or more candidate domains
    why: str


@dataclass
class Artifact:
    artifact_id: str
    category: str          # one of the 9 content-type categories
    text: str
    metadata: Dict = field(default_factory=dict)


class ContentContextRouter:
    def __init__(self, graph: FederatedGraphDB, domain_signal_keywords: Dict[str, List[str]]):
        self.graph = graph
        self.domain_signal_keywords = domain_signal_keywords

    def tag(self, artifact: Artifact) -> RelevancyContext:
        text_norm = re.sub(r"[^a-z0-9\s]", " ", artifact.text.lower())

        where = []
        for domain, signals in self.domain_signal_keywords.items():
            if any(sig in text_norm for sig in signals):
                where.append(domain)
        if not where:
            where = list(self.graph.domain_names())  # unknown domain: fan out to all, let agents self-select

        who = artifact.metadata.get("author", "unspecified-submitter")
        when = artifact.metadata.get("timestamp", datetime.datetime.utcnow().isoformat())
        why = f"onboard '{artifact.category}' artifact '{artifact.artifact_id}' into the holarchy"

        return RelevancyContext(who=who, what=artifact.category, when=when, where=where, why=why)
