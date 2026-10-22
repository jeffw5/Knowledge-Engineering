# Domain Legal

A domain of the Business Operations operational area. Its classes, relations and concepts refer only to the core (Baseline Core v1.0), the Business Operations ontology, never to a sibling domain, so it can change without affecting them. It may cite vocabulary primitives of any domain (D27).

The legal ontology. It extends the core domain ontology and the Business Operations ontology with the client service agreement and its clauses, and with deontic norms (obligation, permission, prohibition, right) that bind roles and are traced to the provisions that state them, statutes and regulations scoped to a jurisdiction, and legal matters, so that rules, constraints and logic have a single source of truth in law.

## Files

| Asset | Named graph | Triples |
|---|---|---:|
| `ttl/vocabulary-domain-legal-0.2.0.ttl` · `trig/vocabulary-domain-legal-0.2.0.trig` | `https://www.insperity.com/vocabulary/domain-legal/` | 554 |
| `ttl/taxonomy-domain-legal-0.2.0.ttl` · `trig/taxonomy-domain-legal-0.2.0.trig` | `https://www.insperity.com/taxonomy/domain-legal/` | 1438 |
| `ttl/ontology-domain-legal-0.2.0.ttl` · `trig/ontology-domain-legal-0.2.0.trig` | `https://www.insperity.com/ontology/domain-legal/` | 251 |
| `ttl/shapes-domain-legal-0.2.0.ttl` · `trig/shapes-domain-legal-0.2.0.trig` | `https://www.insperity.com/shapes/domain-legal/` | 116 |

Built from `KE Domains/_build/spec_legal.py` by `KE Domains/_build/build_domains.py`. Edit the spec and rebuild, or edit the Turtle in the KE Workbench; a rebuild overwrites hand edits to these files.

## Vocabulary (42 primitives)

law, provision, indemnification, liability, limitation, warranty, confidentiality, governing law, arbitration, dispute, lawsuit, remedy, disclosure, consent, matter, counsel, filing, certification ⁺, accreditation, bond, producer, fiduciary, employer of record, certified professional employer organization, multiple employer welfare arrangement, multiple employer plan, Employee retirement income security act, Patient protection and affordable care act, Consolidated omnibus budget reconciliation act, Health insurance portability and accountability act, Fair labor standards act, Family and medical leave act, Americans with disabilities act, Federal unemployment tax act, Federal insurance contributions act, Internal revenue code, Small business efficiency act, Telephone consumer protection act, Controlling the assault of non-solicited pornography and marketing act, clause, term ⁼, signature

⁺ general primitive proposed for promotion to the core · ⁼ declared homonym of a core term

## Taxonomy (90 concepts, 11 top concepts)

| Top concept | Formalized by | Narrower | Specializes |
|---|---|---:|---|
| Law | `core:policy` | 21 | `core-policy/legal-norm-source` |
| Commercial legal norm | `legal:norm` | 4 | `core-policy/norm` |
| Regulatory requirement | `core:requirement` | 5 |  |
| Commercial agreement | `core:directive` | 15 | `core-policy/contractual-instrument` |
| Contract management step | `core:process-step` | 8 | `core-services/contract-management` |
| Agreement status | `core:lifecycle-status` | 4 |  |
| Regulatory credential | `legal:permission` | 4 | `core-policy/permission` |
| Legal matter | `legal:legal-matter` | 6 |  |
| Legal activity | `core:process-step` | 6 |  |
| Legal role | `core:role` | 4 | `core-role/agreement-party-role` |
| Benefit plan arrangement | `core:offering` | 2 |  |

## Ontology (11 classes, 2 relations)

| Class | Parent | Axioms |
|---|---|---|
| `legal:norm` | `core:policy` | legal:binds only core:role; core:componentOf some core:directive |
| `legal:obligation` | `legal:norm` |  |
| `legal:permission` | `legal:norm` |  |
| `legal:prohibition` | `legal:norm` |  |
| `legal:right` | `legal:norm` |  |
| `legal:statute` | `core:policy` | legal:hasJurisdiction some core:location; core:hasComponent only legal:provision |
| `legal:regulation` | `core:policy` | legal:hasJurisdiction some core:location; core:hasComponent only legal:provision |
| `legal:provision` | `core:directive` | core:componentOf some core:policy |
| `legal:legal-matter` | `core:process` | core:hasStep some core:process-step; core:governedBy only core:directive |
| `legal:client-service-agreement` | `core:directive` | core:concerns some core:party; core:hasComponent only legal:clause |
| `legal:clause` | `core:directive` | core:componentOf some core:directive |
| `legal:hasJurisdiction` (relation) | `core:concerns` | A relation between a directive and the jurisdiction in which it applies. |
| `legal:binds` (relation) | `core:concerns` | A relation between a norm and the role whose bearer it obliges, permits, forbids or entitles. |

Core taxonomy concepts formalized by classes of this ontology (the `core:formalizedBy` triples live in this domain's ontology graph; the baseline files and graphs are not changed): `core-policy/obligation` → `legal:obligation`, `core-policy/permission` → `legal:permission`, `core-policy/prohibition` → `legal:prohibition`, `core-policy/right` → `legal:right`, `core-policy/statute` → `legal:statute`, `core-policy/regulation` → `legal:regulation`, `core-policy/client-service-agreement` → `legal:client-service-agreement`.

## Shapes (5)

- `norm-shape` on `legal:norm`: A shape that checks a norm binds a role and is traced to the provision, clause or policy that states it.
- `statute-shape` on `legal:statute`: A shape that checks a statute names its jurisdiction.
- `regulation-shape` on `legal:regulation`: A shape that checks a regulation names its jurisdiction.
- `legal-matter-shape` on `legal:legal-matter`: A shape that checks a legal matter is governed by directives.
- `client-service-agreement-shape` on `legal:client-service-agreement`: A shape that checks a client service agreement names its parties and is built from clauses.
