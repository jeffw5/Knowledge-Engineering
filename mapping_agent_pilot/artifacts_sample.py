"""
artifacts_sample.py
--------------------
Fourteen sample artifacts run through the pilot, in order. They are chosen to:

  1. Exercise all nine content-type categories at least once with a clean pass.
  2. Show one failure of each kind (SHACL, SWRL, PEP) in the engineering domain,
     driving that agent's rejection rate over the circuit-breaker threshold.
  3. Show one failure in the finance domain that does NOT trip its breaker,
     proving isolation: one domain's agent can degrade without affecting another.
  4. Include one artifact that legitimately spans both domains, to exercise
     cross-domain reconciliation.
  5. Include one artifact submitted *after* the engineering breaker trips, to
     show it gets quarantined even though it would otherwise have passed.
"""

from router import Artifact

SAMPLE_ARTIFACTS = [
    Artifact(
        artifact_id="A01-fin-process",
        category="process map",
        text="Quarterly forecasting process: finance runs a rolling budget forecast each quarter, tracking variance against plan.",
        metadata={"owner": "fin-analytics-team", "cadence": "quarterly", "variance_pct": 3, "sox_reviewed": True, "author": "m.reyes"},
    ),
    Artifact(
        artifact_id="A02-fin-document",
        category="document",
        text="Annual budget planning document and budget narrative for FY26, covering the planning document workflow.",
        metadata={"version": "v3.2", "owner": "fpna-team", "author": "m.reyes"},
    ),
    Artifact(
        artifact_id="A03-fin-measure",
        category="measure",
        text="Forecast accuracy measure: a KPI/metric tracking how close quarterly forecasts land to actuals.",
        metadata={"unit": "%", "target": 95, "author": "m.reyes"},
    ),
    Artifact(
        artifact_id="A04-fin-outcome",
        category="outcome",
        text="Quarterly financial outcome and result summary feeding the strategic decision review.",
        metadata={"decision_tier": "Tier 3 - Strategic", "author": "m.reyes"},
    ),
    Artifact(
        artifact_id="A05-fin-event",
        category="event",
        text="Quarter close event marking the end of the fiscal reporting period.",
        metadata={"timestamp_type": "fiscal_quarter_end", "author": "m.reyes"},
    ),
    Artifact(
        artifact_id="A06-fin-rule-FAIL-shacl",
        category="business rule",
        text="Budget variance rule defining the deviation tolerance threshold for department budgets.",
        metadata={"threshold": 5, "sox_reviewed": True, "author": "m.reyes"},  # missing required "applies_to"
    ),
    Artifact(
        artifact_id="A07-eng-schema",
        category="data structure",
        text="User account schema: the data structure record with fields for a user account.",
        metadata={"fields": ["id", "email", "created_at"], "author": "d.chen"},
    ),
    Artifact(
        artifact_id="A08-eng-persona",
        category="persona",
        text="On-call engineer persona describing the rotation and responsibilities during an on-call shift.",
        metadata={"access_scope": "prod-readonly", "author": "d.chen"},
    ),
    Artifact(
        artifact_id="A09-cross-domain",
        category="business rule",
        text="The deployment approval gate for a production release also triggers a budget variance review before the release ships.",
        metadata={
            "approver_role": "release-manager",       # satisfies eng:DeploymentApprovalRule
            "threshold": 5, "applies_to": "engineering-releases", "sox_reviewed": True,  # satisfies fin:BudgetVarianceRule
            "author": "d.chen",
        },
    ),
    Artifact(
        artifact_id="A10-eng-rule-FAIL-shacl",
        category="business rule",
        text="Deployment approval rule: release gate requiring sign-off before a deployment can proceed.",
        metadata={"author": "d.chen"},  # missing required "approver_role"
    ),
    Artifact(
        artifact_id="A11-eng-event-FAIL-swrl",
        category="event",
        text="Incident event: an outage alert routed through PagerDuty with an assigned severity.",
        metadata={"severity": "extreme", "author": "d.chen"},  # not in the allowed severity enum
    ),
    Artifact(
        artifact_id="A12-eng-persona-FAIL-pep",
        category="persona",
        text="On-call engineer persona for the new rotation, describing engineer responsibilities.",
        metadata={"access_scope": "public", "author": "d.chen"},  # present, but violates the Security PEP
    ),
    Artifact(
        artifact_id="A13-eng-constraint-post-trip",
        category="constraint",
        text="Data retention constraint: log data retention and expiry (TTL) policy for the engineering domain.",
        metadata={"retention_days": 90, "author": "d.chen"},  # would pass -- submitted after the breaker trips
    ),
    Artifact(
        artifact_id="A14-fin-measure-2",
        category="measure",
        text="Q3 forecast accuracy KPI/metric tracking dashboard, a second forecast accuracy measure.",
        metadata={"unit": "%", "target": 97, "author": "m.reyes"},
    ),
    # A15/A16 exercise the third domain (legal) added purely to prove the chassis
    # reuses unchanged across a new cartridge -- see chassis.py and ontology.py.
    Artifact(
        artifact_id="A15-legal-document",
        category="document",
        text="Vendor contract agreement and NDA counterparty legal document under review before signature.",
        metadata={"version": "v1.0", "counterparty": "Acme Vendor Corp", "author": "l.nguyen"},
    ),
    Artifact(
        artifact_id="A16-legal-constraint",
        category="constraint",
        text="Non-disclosure confidentiality constraint applying to the counterparty NDA.",
        metadata={"counterparty_type": "external-vendor", "legal_reviewed": True, "author": "l.nguyen"},
    ),

    # ---- The seven-agent roster (design doc §3.2), two artifacts each ----

    Artifact(
        artifact_id="A17-req-document",
        category="document",
        text="Requirements specification document capturing the requirement spec for the onboarding feature, tracked as REQ-118.",
        metadata={"version": "v2", "requirement_id": "REQ-118", "author": "r.oyelaran"},
    ),
    Artifact(
        artifact_id="A18-req-constraint",
        category="constraint",
        text="Traceability constraint linking this requirement back to its parent requirement for full requirements traceability.",
        metadata={"linked_requirement_id": "REQ-100", "author": "r.oyelaran"},
    ),
    Artifact(
        artifact_id="A19-mbse-schema",
        category="data structure",
        text="System model schema describing the model-based systems engineering (MBSE) representation of the braking subsystem.",
        metadata={"model_type": "SysML-block-definition", "author": "t.kowalski"},
    ),
    Artifact(
        artifact_id="A20-mbse-event",
        category="event",
        text="Integration test event marking completion of the hardware/software (hw-sw) integration test phase.",
        metadata={"test_phase": "HW-SW integration", "author": "t.kowalski"},
    ),
    Artifact(
        artifact_id="A21-safety-constraint",
        category="constraint",
        text="Unsafe control action constraint identified during the STPA hazard analysis for the braking system.",
        metadata={"hazard_id": "HAZ-04", "author": "s.abara"},
    ),
    Artifact(
        artifact_id="A22-safety-event",
        category="event",
        text="Hazard event logged during the STAMP safety review with an assigned severity.",
        metadata={"severity": "high", "author": "s.abara"},
    ),
    Artifact(
        artifact_id="A23-ks-document",
        category="document",
        text="Vocabulary document defining core taxonomy terms, maintained by the knowledge systems steward.",
        metadata={"version": "v5", "steward": "k.patel", "author": "k.patel"},
    ),
    Artifact(
        artifact_id="A24-ks-persona",
        category="persona",
        text="Ontology engineer persona granted access within the knowledge system governance program.",
        metadata={"access_scope": "ontology-authoring", "author": "k.patel"},
    ),
    Artifact(
        artifact_id="A25-ea-process",
        category="process map",
        text="Architecture decision process documenting the enterprise architecture review for a new platform ADR-027.",
        metadata={"owner": "architecture-review-board", "decision_id": "ADR-027", "author": "a.mercer"},
    ),
    Artifact(
        artifact_id="A26-ea-measure",
        category="measure",
        text="Architecture alignment measure tracking conformance to the enterprise architecture target state.",
        metadata={"unit": "%", "target": 90, "author": "a.mercer"},
    ),
    Artifact(
        artifact_id="A27-da-outcome",
        category="outcome",
        text="Scenario outcome from the decision analysis scenario planning exercise for the strategic tradeoff review.",
        metadata={"decision_tier": "Tier 3 - Strategic", "author": "j.finch"},
    ),
    Artifact(
        artifact_id="A28-da-persona",
        category="persona",
        text="Decision maker persona representing the executive stakeholder in this decision analysis review.",
        metadata={"access_scope": "executive-readonly", "author": "j.finch"},
    ),
]
