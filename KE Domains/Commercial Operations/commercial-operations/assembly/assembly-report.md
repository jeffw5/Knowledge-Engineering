# Commercial Operations assembly report

Built 2026-10-22T04:04:49Z by `_build/build_assembly.py` from `apqc_commercial.py`, on APQC PCF 7.4 (August 2024, https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-12).

Levels (D28): APQC process group (L2) › process (L3) › activity (L4) are the process levels; the activity's tasks (L5) are its steps. An activity with no L5 tasks is performed as one step; an L3 process with no activities is itself the activity. PEO extensions are classified by the APQC element they extend.

| Domain | Manifest | Activities | of which extensions | Steps | Performed as one step | Services | Not applicable elements |
|---|---|---:|---:|---:|---:|---:|---:|
| Domain Sales | 0.5.0 | 41 | 3 | 56 | 38 | 16 | 4 |
| Domain Sales.Partner & Channel | 0.1.0 | 26 | 1 | 30 | 24 | 5 | 4 |
| Domain Marketing | 0.1.0 | 54 | 2 | 56 | 50 | 11 | 6 |
| Domain Pricing | 0.1.0 | 15 | 2 | 17 | 14 | 4 | 2 |
| Domain Customer Care | 0.1.0 | 39 | 1 | 49 | 33 | 9 | 45 |

Shared: 13 parties and roles outside the processes, 228 records.

## Hand-offs between domains

Records one domain produces and another consumes (derived suppliers and customers, D24).

| From | To | Records |
|---|---|---|
| Domain Customer Care | Domain Marketing | Client feedback insights, Client health signals, Client roster, Client satisfaction results |
| Domain Customer Care | Domain Sales | Client master record, Client relationship review, Expansion referral, Service level targets |
| Domain Marketing | Domain Customer Care | Buyer needs research, Campaign responses, Client lifetime value, Service adoption patterns |
| Domain Marketing | Domain Sales.Partner & Channel | Brand guidelines, Market trends brief, Marketing goals, Sales content kit, Target segment list |
| Domain Marketing | Domain Pricing | Competitive intelligence, Marketing goals |
| Domain Marketing | Domain Sales | Client growth trend, Client lifetime value, Client metrics dashboard, Competitive intelligence, Market share report, Marketing goals, Marketing-qualified leads, Prioritized market opportunities, Propensity scores, Sales content kit, Target segment list |
| Domain Sales.Partner & Channel | Domain Customer Care | Cross-channel strategy |
| Domain Sales.Partner & Channel | Domain Marketing | Channel strategy |
| Domain Sales.Partner & Channel | Domain Sales | Partner opportunity registrations |
| Domain Pricing | Domain Marketing | Pricing guidelines |
| Domain Pricing | Domain Sales | Binding quote, Deal profitability analysis, Pricing exception decision, Published rates |
| Domain Sales | Domain Customer Care | Client account record, Client handoff package |
| Domain Sales | Domain Marketing | Win-loss record |
| Domain Sales | Domain Pricing | Pricing exception request, Quote outcomes, Quote request package |

## Checks

- Errors: **0** · warnings: **625** (all manifests).

**Domain Sales.Partner & Channel:** 48 SHACL findings.

| Severity | Shape | Finding | Focus nodes |
|---|---|---|---|
| warn | `process-shape` | A process should have at least one process step. | 30: determine-channels-to-be-supported, establish-channel-objectives, determine-channel-role-and-fit-with-target-segments, select-channels-for-target-segments, identify-required-channel-capabilities … |
| warn | `asset-shape` | An asset should have a lifecycle. | 18: , partner-portal, , ,  … |

**Domain Marketing:** 94 SHACL findings.

| Severity | Shape | Finding | Focus nodes |
|---|---|---|---|
| warn | `process-shape` | A process should have at least one process step. | 56: understand-consumer-needs-and-historical-behaviors, predict-customer-purchasing-behavior, determine-market-share-gain-or-loss, analyze-market-and-industry-trends, analyze-competing-organizations-and-their-products-and-services … |
| warn | `asset-shape` | An asset should have a lifecycle. | 38: , marketing-automation, , ,  … |

**Domain Pricing:** 32 SHACL findings.

| Severity | Shape | Finding | Focus nodes |
|---|---|---|---|
| warn | `process-shape` | A process should have at least one process step. | 17: conduct-pricing-analysis, establish-guidelines-for-applying-pricing-and-discounting, establish-pricing-targets, approve-pricing-strategies-policies-and-targets, review-pricing-exceptions … |
| warn | `asset-shape` | An asset should have a lifecycle. | 15: , pricing-engine, , ,  … |

**Domain Customer Care:** 85 SHACL findings.

| Severity | Shape | Finding | Focus nodes |
|---|---|---|---|
| warn | `process-shape` | A process should have at least one process step. | 49: manage-customer-relationships, collect-and-merge-internal-and-third-party-customer-information, de-duplicate-customer-data, define-customer-service-requirements-across-the-enterprise, define-customer-service-experience … |
| warn | `asset-shape` | An asset should have a lifecycle. | 36: , service-desk, , ,  … |
