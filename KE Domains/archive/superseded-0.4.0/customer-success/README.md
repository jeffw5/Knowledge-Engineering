# Customer success

A domain of the Commercial Operations operational area. It refers only to the core (Baseline Core v1.0) and to the Commercial Operations container, never to a sibling domain, so it can change without affecting them.

The customer success ontology. It extends the core domain ontology and the Commercial Operations ontology with the client success process and its steps, client health scores that measure accounts, and playbooks that govern client success steps.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-customer-success-0.1.1.ttl` · `trig/vocabulary-domain-customer-success-0.1.1.trig` | `https://www.insperity.com/vocabulary/domain-customer-success/` | 182 |
| `ttl/taxonomy-domain-customer-success-0.1.1.ttl` · `trig/taxonomy-domain-customer-success-0.1.1.trig` | `https://www.insperity.com/taxonomy/domain-customer-success/` | 823 |
| `ttl/ontology-domain-customer-success-0.1.1.ttl` · `trig/ontology-domain-customer-success-0.1.1.trig` | `https://www.insperity.com/ontology/domain-customer-success/` | 99 |
| `ttl/shapes-domain-customer-success-0.1.1.ttl` · `trig/shapes-domain-customer-success-0.1.1.trig` | `https://www.insperity.com/shapes/domain-customer-success/` | 75 |

Built from `../_build/spec_customer_success.py` by `../_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (13 primitives)

health, churn, adoption, expansion, upsell, cross-sell, satisfaction, advocacy, save, win-back, net promoter score, playbook, milestone ⁺

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (50 concepts, 9 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Client success stage | `customersuccess:client-success-step` | 5 |  |
| Client success activity | `core:process-step` | 8 | `core-process/process-step` |
| Client health | `customersuccess:health-score` | 4 |  |
| Client status | `core:lifecycle-status` | 4 |  |
| Churn | `core:event` | 7 | `core-event/business-event` |
| Expansion type | `commercialops:opportunity` | 3 | `domain-commercial-operations/client-opportunity` |
| Client success measure | `core:measure` | 6 | `core-measure/key-performance-indicator` |
| Client success role | `core:role` | 1 | `core-role/employment-role` |
| Client success playbook | `customersuccess:playbook` | 3 |  |

## Ontology (4 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `customersuccess:client-success-process` | `core:process` | core:hasStep some customersuccess:client-success-step |
| `customersuccess:client-success-step` | `core:process-step` | core:isStepOf some customersuccess:client-success-process; core:addresses only core:job-step |
| `customersuccess:health-score` | `core:measure` | core:measures some commercialops:account |
| `customersuccess:playbook` | `core:directive` | core:governs some customersuccess:client-success-step |

## Shapes (3)

- `client-success-step-shape` on `customersuccess:client-success-step`: A shape that checks a client success step belongs to a client success process.
- `health-score-shape` on `customersuccess:health-score`: A shape that checks a health score measures an account.
- `playbook-shape` on `customersuccess:playbook`: A shape that checks a playbook governs at least one client success step.
