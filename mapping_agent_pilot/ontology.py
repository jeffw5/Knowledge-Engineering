"""
ontology.py
-----------
Stands in for the federated GraphDB: a set of per-domain component ontologies.

In production this is a real triple store (e.g. GraphDB/Stardog/Neo4j) holding
OWL classes, SHACL shapes, and SWRL rules per domain. Here each concept is a
plain Python dict so the pilot has no external dependencies. The *shape* of
the data (concept identity, required properties, invariants, PEP tags) is
what matters -- swap this module out for a real SPARQL/Cypher client without
touching any other file.

Each concept covers one of the nine artifact categories from the design doc:
data structure, document, business rule, constraint, process map, event,
measure, persona, outcome.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class Concept:
    uri: str                      # persistent identity (URI/IRI stand-in)
    domain: str                   # owning domain holon
    category: str                 # one of the 9 artifact categories
    label: str
    keywords: List[str]           # terms used by the heuristic vector search
    required_properties: List[str]  # SHACL-like invariant: must be present on a mapped artifact
    swrl_rule: Optional[Callable[[dict], Optional[str]]] = None  # returns an error string, or None if consistent
    pep_tags: List[str] = field(default_factory=list)  # governance domains this concept is subject to


class DomainOntology:
    """One domain holon's component ontology: its concepts + governance metadata."""

    def __init__(self, domain: str, concepts: List[Concept], pep_policies: Dict[str, Callable[[dict], Optional[str]]]):
        self.domain = domain
        self.concepts = {c.uri: c for c in concepts}
        self.pep_policies = pep_policies  # tag -> policy function(artifact) -> error string or None

    def candidates(self) -> List[Concept]:
        return list(self.concepts.values())


class FederatedGraphDB:
    """The federated store: a registry of domain ontologies, keyed by domain name."""

    def __init__(self):
        self.domains: Dict[str, DomainOntology] = {}
        self.committed_mappings: List[dict] = []  # what's actually "in the graph" after KGCL commits

    def register_domain(self, ontology: DomainOntology):
        self.domains[ontology.domain] = ontology

    def domain_names(self) -> List[str]:
        return list(self.domains.keys())


# ---------------------------------------------------------------------------
# SWRL-like consistency rules (deterministic, hand-written -- stand in for
# real SWRL inference). Each returns an error string on violation, else None.
# ---------------------------------------------------------------------------

def rule_variance_bounded(artifact: dict) -> Optional[str]:
    variance = artifact.get("metadata", {}).get("variance_pct")
    if variance is not None and variance > 5:
        return f"SWRL violation: forecast variance {variance}% exceeds the 5% obligation bound"
    return None


def rule_severity_enum(artifact: dict) -> Optional[str]:
    sev = artifact.get("metadata", {}).get("severity")
    allowed = {"low", "medium", "high", "critical"}
    if sev is not None and sev not in allowed:
        return f"SWRL violation: severity '{sev}' is not a member of the defined severity enumeration"
    return None


# ---------------------------------------------------------------------------
# PEP policies (deterministic governance checks per tag)
# ---------------------------------------------------------------------------

def pep_sox(artifact: dict) -> Optional[str]:
    if not artifact.get("metadata", {}).get("sox_reviewed"):
        return "PEP violation: financial process artifacts require sox_reviewed=true (Compliance PEP)"
    return None


def pep_access_scope(artifact: dict) -> Optional[str]:
    scope = artifact.get("metadata", {}).get("access_scope")
    if not scope:
        return "PEP violation: persona artifacts require an explicit access_scope (Security PEP)"
    if scope in ("public", "public-unrestricted"):
        return f"PEP violation: access_scope '{scope}' is too broad for a governed persona (Security PEP)"
    return None


def pep_change_approval(artifact: dict) -> Optional[str]:
    if not artifact.get("metadata", {}).get("approver_role"):
        return "PEP violation: deployment rules require an approver_role (Risk PEP)"
    return None


def pep_legal_review(artifact: dict) -> Optional[str]:
    if not artifact.get("metadata", {}).get("legal_reviewed"):
        return "PEP violation: contract artifacts require legal_reviewed=true (Legal PEP)"
    return None


def build_finance_ontology() -> DomainOntology:
    concepts = [
        Concept(
            uri="fin:ForecastingProcess",
            domain="finance",
            category="process map",
            label="Forecasting Process",
            keywords=["forecast", "forecasting", "projection", "variance", "quarterly", "budget"],
            required_properties=["owner", "cadence"],
            swrl_rule=rule_variance_bounded,
            pep_tags=["sox"],
        ),
        Concept(
            uri="fin:BudgetVarianceRule",
            domain="finance",
            category="business rule",
            label="Budget Variance Rule",
            keywords=["variance", "threshold", "budget", "deviation", "tolerance"],
            required_properties=["threshold", "applies_to"],
            pep_tags=["sox"],
        ),
        Concept(
            uri="fin:ForecastAccuracyMeasure",
            domain="finance",
            category="measure",
            label="Forecast Accuracy Measure",
            keywords=["accuracy", "measure", "kpi", "metric", "forecast"],
            required_properties=["unit", "target"],
        ),
        Concept(
            uri="fin:CFOPersona",
            domain="finance",
            category="persona",
            label="CFO Persona",
            keywords=["cfo", "finance leader", "persona", "stakeholder"],
            required_properties=["access_scope"],
            pep_tags=["security"],
        ),
        Concept(
            uri="fin:QuarterCloseEvent",
            domain="finance",
            category="event",
            label="Quarter Close Event",
            keywords=["quarter close", "close", "reporting period", "fiscal"],
            required_properties=["timestamp_type"],
        ),
        Concept(
            uri="fin:BudgetDocument",
            domain="finance",
            category="document",
            label="Budget Planning Document",
            keywords=["budget document", "planning document", "annual budget", "budget narrative"],
            required_properties=["version", "owner"],
        ),
        Concept(
            uri="fin:QuarterlyOutcome",
            domain="finance",
            category="outcome",
            label="Quarterly Financial Outcome",
            keywords=["outcome", "result", "quarterly performance", "decision"],
            required_properties=["decision_tier"],
        ),
    ]
    pep_policies = {"sox": pep_sox, "security": pep_access_scope}
    return DomainOntology("finance", concepts, pep_policies)


def build_engineering_ontology() -> DomainOntology:
    concepts = [
        Concept(
            uri="eng:UserAccountSchema",
            domain="engineering",
            category="data structure",
            label="User Account Schema",
            keywords=["schema", "user", "account", "fields", "data structure", "record"],
            required_properties=["fields"],
        ),
        Concept(
            uri="eng:DeploymentApprovalRule",
            domain="engineering",
            category="business rule",
            label="Deployment Approval Rule",
            keywords=["deploy", "deployment", "release", "approval", "gate"],
            required_properties=["approver_role"],
            pep_tags=["risk"],
        ),
        Concept(
            uri="eng:IncidentEvent",
            domain="engineering",
            category="event",
            label="Incident Event",
            keywords=["incident", "outage", "severity", "alert", "pagerduty"],
            required_properties=["severity"],
            swrl_rule=rule_severity_enum,
        ),
        Concept(
            uri="eng:ReleaseCadenceMeasure",
            domain="engineering",
            category="measure",
            label="Release Cadence Measure",
            keywords=["cadence", "release frequency", "deploys per week", "measure", "metric"],
            required_properties=["unit"],
        ),
        Concept(
            uri="eng:OnCallPersona",
            domain="engineering",
            category="persona",
            label="On-Call Engineer Persona",
            keywords=["on-call", "oncall", "engineer", "persona", "rotation"],
            required_properties=["access_scope"],
            pep_tags=["security"],
        ),
        Concept(
            uri="eng:DataRetentionConstraint",
            domain="engineering",
            category="constraint",
            label="Data Retention Constraint",
            keywords=["retention", "data retention", "constraint", "expire", "ttl"],
            required_properties=["retention_days"],
        ),
    ]
    pep_policies = {"risk": pep_change_approval, "security": pep_access_scope}
    return DomainOntology("engineering", concepts, pep_policies)


def build_requirements_ontology() -> DomainOntology:
    """Requirements Engineering -- roster agent #2 (design doc §3.2). Owns:
    data structures, constraints, documents."""
    concepts = [
        Concept(
            uri="req:RequirementSpecDocument",
            domain="requirements",
            category="document",
            label="Requirement Specification Document",
            keywords=["requirement spec", "requirements specification", "requirement document", "req-"],
            required_properties=["version", "requirement_id"],
        ),
        Concept(
            uri="req:TraceabilityConstraint",
            domain="requirements",
            category="constraint",
            label="Traceability Constraint",
            keywords=["traceability", "requirements traceability", "linked requirement", "parent requirement"],
            required_properties=["linked_requirement_id"],
        ),
    ]
    return DomainOntology("requirements", concepts, pep_policies={})


def build_mbse_ontology() -> DomainOntology:
    """Systems Engineering (MBSE) -- roster agent #3. Owns: data structures,
    process maps, events."""
    concepts = [
        Concept(
            uri="mbse:SystemModelSchema",
            domain="mbse",
            category="data structure",
            label="System Model Schema",
            keywords=["system model", "mbse", "model-based systems engineering", "sysml"],
            required_properties=["model_type"],
        ),
        Concept(
            uri="mbse:IntegrationTestEvent",
            domain="mbse",
            category="event",
            label="Integration Test Event",
            keywords=["integration test", "hw-sw integration", "test phase"],
            required_properties=["test_phase"],
        ),
    ]
    return DomainOntology("mbse", concepts, pep_policies={})


def build_systems_safety_ontology() -> DomainOntology:
    """Systems Safety (STPA/STAMP) -- roster agent #4. Owns: constraints,
    events, business rules."""
    concepts = [
        Concept(
            uri="safety:UnsafeControlActionConstraint",
            domain="systems_safety",
            category="constraint",
            label="Unsafe Control Action Constraint",
            keywords=["unsafe control action", "stpa", "hazard analysis", "uca"],
            required_properties=["hazard_id"],
        ),
        Concept(
            uri="safety:HazardEvent",
            domain="systems_safety",
            category="event",
            label="Hazard Event",
            keywords=["hazard event", "hazard", "safety review", "stamp"],
            required_properties=["severity"],
            swrl_rule=rule_severity_enum,
        ),
    ]
    return DomainOntology("systems_safety", concepts, pep_policies={})


def build_knowledge_systems_ontology() -> DomainOntology:
    """Knowledge Systems -- roster agent #5. Owns: documents, data structures,
    personas."""
    concepts = [
        Concept(
            uri="ks:VocabularyDocument",
            domain="knowledge_systems",
            category="document",
            label="Vocabulary Document",
            keywords=["vocabulary", "taxonomy", "vocabulary document", "steward"],
            required_properties=["version", "steward"],
        ),
        Concept(
            uri="ks:OntologyEngineerPersona",
            domain="knowledge_systems",
            category="persona",
            label="Ontology Engineer Persona",
            keywords=["ontology engineer", "knowledge system", "vocabulary steward", "persona"],
            required_properties=["access_scope"],
            pep_tags=["security"],
        ),
    ]
    return DomainOntology("knowledge_systems", concepts, pep_policies={"security": pep_access_scope})


def build_enterprise_architecture_ontology() -> DomainOntology:
    """Enterprise Architecture -- roster agent #6. Owns: process maps,
    outcomes, measures."""
    concepts = [
        Concept(
            uri="ea:ArchitectureDecisionProcess",
            domain="enterprise_architecture",
            category="process map",
            label="Architecture Decision Process",
            keywords=["architecture decision", "adr", "architecture review", "enterprise architecture"],
            required_properties=["owner", "decision_id"],
        ),
        Concept(
            uri="ea:ArchitectureAlignmentMeasure",
            domain="enterprise_architecture",
            category="measure",
            label="Architecture Alignment Measure",
            keywords=["architecture alignment", "target state", "conformance", "measure"],
            required_properties=["unit", "target"],
        ),
    ]
    return DomainOntology("enterprise_architecture", concepts, pep_policies={})


def build_decision_analysis_ontology() -> DomainOntology:
    """Decision Analysis -- roster agent #7. Owns: outcomes, measures,
    personas."""
    concepts = [
        Concept(
            uri="da:ScenarioOutcome",
            domain="decision_analysis",
            category="outcome",
            label="Scenario Outcome",
            keywords=["scenario outcome", "decision analysis", "scenario planning", "tradeoff review"],
            required_properties=["decision_tier"],
        ),
        Concept(
            uri="da:DecisionMakerPersona",
            domain="decision_analysis",
            category="persona",
            label="Decision Maker Persona",
            keywords=["decision maker", "executive stakeholder", "decision analysis", "persona"],
            required_properties=["access_scope"],
            pep_tags=["security"],
        ),
    ]
    return DomainOntology("decision_analysis", concepts, pep_policies={"security": pep_access_scope})


def build_legal_ontology() -> DomainOntology:
    """
    A third domain, added purely to demonstrate that the chassis/cartridge
    split scales: this domain reuses every chassis component in chassis.py
    unchanged -- only this file (a new cartridge's ontology binding) and
    artifacts_sample.py (two new sample artifacts) had to change.
    """
    concepts = [
        Concept(
            uri="legal:ContractDocument",
            domain="legal",
            category="document",
            label="Contract Document",
            keywords=["contract", "agreement", "nda", "counterparty", "legal document"],
            required_properties=["version", "counterparty"],
        ),
        Concept(
            uri="legal:NDAConstraint",
            domain="legal",
            category="constraint",
            label="NDA Confidentiality Constraint",
            keywords=["nda", "confidentiality", "non-disclosure", "constraint"],
            required_properties=["counterparty_type"],
            pep_tags=["legal"],
        ),
    ]
    pep_policies = {"legal": pep_legal_review}
    return DomainOntology("legal", concepts, pep_policies)


def build_federated_graph() -> FederatedGraphDB:
    graph = FederatedGraphDB()
    # The seven-agent roster recommended in design doc §3.2:
    graph.register_domain(build_finance_ontology())
    graph.register_domain(build_requirements_ontology())
    graph.register_domain(build_mbse_ontology())
    graph.register_domain(build_systems_safety_ontology())
    graph.register_domain(build_knowledge_systems_ontology())
    graph.register_domain(build_enterprise_architecture_ontology())
    graph.register_domain(build_decision_analysis_ontology())
    # Two extra domains kept from the original chassis/cartridge reuse proof
    # (not part of the §3.2 roster, but left in to keep the circuit-breaker
    # and cross-domain-reconciliation demonstrations intact):
    graph.register_domain(build_engineering_ontology())
    graph.register_domain(build_legal_ontology())
    return graph
