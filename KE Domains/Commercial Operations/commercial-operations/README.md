# Commercial operations

The container domain of the Commercial Operations operational area. It holds what two or more domains share, so that the domains never refer to one another. It imports only the core domain ontology 0.1.0.

The container ontology of the Commercial Operations operational area. It extends the core domain ontology with the classes every commercial domain shares (account, lead, opportunity, proposal, client service agreement, clause, competitor, worksite employee, sale), so that the sales, marketing, legal, customer success, pricing and contracts, and partner and channel ontologies import only the core and this ontology, never each other.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-commercial-operations-0.3.0.ttl` · `trig/vocabulary-domain-commercial-operations-0.3.0.trig` | `https://www.insperity.com/vocabulary/domain-commercial-operations/` | 503 |
| `ttl/taxonomy-domain-commercial-operations-0.3.0.ttl` · `trig/taxonomy-domain-commercial-operations-0.3.0.trig` | `https://www.insperity.com/taxonomy/domain-commercial-operations/` | 879 |
| `ttl/ontology-domain-commercial-operations-0.3.0.ttl` · `trig/ontology-domain-commercial-operations-0.3.0.trig` | `https://www.insperity.com/ontology/domain-commercial-operations/` | 253 |
| `ttl/shapes-domain-commercial-operations-0.3.0.ttl` · `trig/shapes-domain-commercial-operations-0.3.0.trig` | `https://www.insperity.com/shapes/domain-commercial-operations/` | 130 |

Built from `../_build/spec_commercial_operations.py` by `../_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (38 primitives)

account, lead, opportunity, pipeline, segment, territory, referral, commission, competitor, qualification, proposal, conversion ⁼, attribution, win, sale, engagement, influence, incentive, negotiation, enablement, registration, signal, analysis ⁺, industry ⁺, stage ⁺, buyer, census, clause, claim, benefit, payroll, insurance, unemployment, workers' compensation, professional employer organization, administrative services organization, human capital management, ideal customer profile

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (55 concepts, 10 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Commercial party role | `core:role` | 3 | `core-role/commercial-role` |
| Commercial record | `core:information-asset` | 15 |  |
| Commercial agreement | `core:directive` | 2 | `core-policy/contractual-instrument` |
| Service model | `core:offering` | 3 |  |
| Employment service | `core:service` | 4 | `core-services/business-services` |
| Market structure | `core:information-asset` | 5 |  |
| Commercial measure | `core:measure` | 4 | `core-measure/key-performance-indicator` |
| Commercial event | `core:event` | 3 | `core-event/business-event` |
| Commercial activity | `core:process-step` | 4 |  |
| Claim | `core:information-asset` | 2 |  |

## Ontology (10 classes, 3 relations)

| Class | Parent | Axioms |
|---|---|---|
| `commercialops:account` | `core:information-asset` | core:concerns some core:party |
| `commercialops:lead` | `core:information-asset` | core:concerns some core:party |
| `commercialops:opportunity` | `core:information-asset` | core:concerns some core:party; core:concerns some core:offering; commercialops:attributedTo only core:party |
| `commercialops:proposal` | `core:information-asset` | core:concerns some commercialops:opportunity |
| `commercialops:census` | `core:information-asset` | core:concerns some core:person |
| `commercialops:client-service-agreement` | `core:directive` | core:concerns some core:party; core:hasComponent only commercialops:clause |
| `commercialops:clause` | `core:directive` | core:componentOf some core:directive |
| `commercialops:competitor` | `core:role` | core:roleOf some core:organization |
| `commercialops:worksite-employee` | `core:role` | core:roleOf some core:person |
| `commercialops:sale` | `core:event` | core:triggers only core:process-step |
| `commercialops:attributedTo` (relation) | `core:concerns` | A relation between a lead, opportunity or sale and the party credited with sourcing or influencing it. |
| `commercialops:hasSupplier` (relation) | `obo:RO_0000057` | A relation between a process step and a party, or a role, outside the process that provides one of the inputs the step consumes. |
| `commercialops:hasCustomer` (relation) | `obo:RO_0000057` | A relation between a process step and a party, or a role, outside the process that receives one of the outputs the step produces. |

Core taxonomy concepts formalized by classes of this ontology (the `core:formalizedBy` triples live in this domain's ontology graph; the baseline files and graphs are not changed): `core-policy/client-service-agreement` → `commercialops:client-service-agreement`, `core-role/worksite-employee` → `commercialops:worksite-employee`.

## Shapes (5)

- `process-step-boundary-shape` on `core:process-step`: A shape that checks the supplier and customer of a process step are parties or roles.
- `account-shape` on `commercialops:account`: A shape that checks an account names the party it is about.
- `opportunity-shape` on `commercialops:opportunity`: A shape that checks an opportunity names its party and offerings and credits a party for its source.
- `census-shape` on `commercialops:census`: A shape that checks a census is about the persons it lists.
- `client-service-agreement-shape` on `commercialops:client-service-agreement`: A shape that checks a client service agreement names its parties and is built from clauses.
