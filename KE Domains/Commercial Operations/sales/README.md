# Domain Sales

A domain of the Commercial Operations operational area. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the Commercial Operations ontology, never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).

The sales ontology. It extends the core domain ontology and the Commercial Operations ontology with the selling process and its steps, anchored on the process step, the sales processes that enable sales services, and sales quotas. Selling steps are bridged to the buyer persona's job steps through core:addresses in the value map, a separate assembly.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-sales-0.4.0.ttl` · `trig/vocabulary-domain-sales-0.4.0.trig` | `https://www.insperity.com/vocabulary/domain-sales/` | 185 |
| `ttl/taxonomy-domain-sales-0.4.0.ttl` · `trig/taxonomy-domain-sales-0.4.0.trig` | `https://www.insperity.com/taxonomy/domain-sales/` | 971 |
| `ttl/ontology-domain-sales-0.4.0.ttl` · `trig/ontology-domain-sales-0.4.0.trig` | `https://www.insperity.com/ontology/domain-sales/` | 102 |
| `ttl/shapes-domain-sales-0.4.0.ttl` · `trig/shapes-domain-sales-0.4.0.trig` | `https://www.insperity.com/shapes/domain-sales/` | 93 |

Built from `KE Domains/_build/spec_sales.py` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (13 primitives)

quota, booking, prospecting, outreach, cadence, demonstration, objection, champion, gatekeeper, decision maker, collection ⁺, comparison ⁺, cycle ⁺

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (59 concepts, 10 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Selling stage | `sales:selling-step` | 6 | `core-process/process-step` |
| Selling activity | `core:process-step` | 12 |  |
| Sales process | `core:process` | 3 | `core-process/operational-process` |
| Sales service | `sales:sales-service` | 2 | `core-services/sales-services` |
| Buying role | `core:role` | 5 | `core-role/commercial-role` |
| Buying committee | `core:organization` | 0 |  |
| Sales role | `core:role` | 3 | `core-role/employment-role` |
| Sales plan | `core:directive` | 4 |  |
| Sales record | `core:information-asset` | 8 |  |
| Sales measure | `core:measure` | 6 | `core-measure/key-performance-indicator` |

## Ontology (4 classes, 0 relations)

| Class | Parent | Axioms |
|---|---|---|
| `sales:selling-process` | `core:process` | core:hasStep some sales:selling-step |
| `sales:selling-step` | `core:process-step` | core:isStepOf some core:process; core:addresses only core:job-step |
| `sales:sales-service` | `core:service` | core:hasComponent only core:asset |
| `sales:quota` | `core:measure` | core:measures some sales:selling-process |

## Shapes (3)

- `selling-step-shape` on `sales:selling-step`: A shape that checks a selling step belongs to a process and that what it addresses is a job step.
- `sales-service-shape` on `sales:sales-service`: A shape that checks a sales service is enabled by a process, delivered by a selling step and classified in the Sales taxonomy.
- `quota-shape` on `sales:quota`: A shape that checks a quota names what it measures.
