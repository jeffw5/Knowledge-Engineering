# Domain Customer Care

A domain of the Commercial Operations operational area. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the Commercial Operations ontology, never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).

The customer care ontology. It extends the core domain ontology and the Commercial Operations ontology with the client success process and its steps, client health scores that measure accounts, and playbooks that govern client success steps.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-customer-care-0.2.0.ttl` · `trig/vocabulary-domain-customer-care-0.2.0.trig` | `https://www.insperity.com/vocabulary/domain-customer-care/` | 184 |
| `ttl/taxonomy-domain-customer-care-0.2.0.ttl` · `trig/taxonomy-domain-customer-care-0.2.0.trig` | `https://www.insperity.com/taxonomy/domain-customer-care/` | 825 |
| `ttl/ontology-domain-customer-care-0.2.0.ttl` · `trig/ontology-domain-customer-care-0.2.0.trig` | `https://www.insperity.com/ontology/domain-customer-care/` | 101 |
| `ttl/shapes-domain-customer-care-0.2.0.ttl` · `trig/shapes-domain-customer-care-0.2.0.trig` | `https://www.insperity.com/shapes/domain-customer-care/` | 77 |

Built from `KE Domains/_build/spec_customer_care.py` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (13 primitives)

health, churn, adoption, expansion, upsell, cross-sell, satisfaction, advocacy, save, win-back, net promoter score, playbook, milestone ⁺

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (50 concepts, 9 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Client success stage | `customercare:client-success-step` | 5 |  |
| Client success activity | `core:process-step` | 8 | `core-process/process-step` |
| Client health | `customercare:health-score` | 4 |  |
| Client status | `core:lifecycle-status` | 4 |  |
| Churn | `core:event` | 7 | `core-event/business-event` |
| Expansion type | `commercialops:opportunity` | 3 | `commercial-operations/client-opportunity` |
| Client success measure | `core:measure` | 6 | `core-measure/key-performance-indicator` |
| Client success role | `core:role` | 1 | `core-role/employment-role` |
| Client success playbook | `customercare:playbook` | 3 |  |

## Ontology (4 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `customercare:client-success-process` | `core:process` | core:hasStep some customercare:client-success-step |
| `customercare:client-success-step` | `core:process-step` | core:isStepOf some customercare:client-success-process; core:addresses only core:job-step |
| `customercare:health-score` | `core:measure` | core:measures some commercialops:account |
| `customercare:playbook` | `core:directive` | core:governs some customercare:client-success-step |

## Shapes (3)

- `client-success-step-shape` on `customercare:client-success-step`: A shape that checks a client success step belongs to a client success process.
- `health-score-shape` on `customercare:health-score`: A shape that checks a health score measures an account.
- `playbook-shape` on `customercare:playbook`: A shape that checks a playbook governs at least one client success step.
