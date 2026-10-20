# Build report: Commercial Operations domains

Built 2026-10-20T17:03:21Z against Baseline Core v1.0 (core 0.1.0) by `_build/build_domains.py`.

| Domain | Version | Vocabulary terms | Taxonomy concepts | Classes | Relations | Shapes | Triples |
|---|---|---:|---:|---:|---:|---:|---:|
| Commercial operations | 0.3.0 | 38 | 55 | 10 | 3 | 5 | 1765 |
| Sales | 0.3.0 | 13 | 59 | 4 | 0 | 3 | 1341 |
| Marketing | 0.1.1 | 34 | 66 | 3 | 0 | 3 | 1671 |
| Legal | 0.1.1 | 39 | 68 | 9 | 2 | 4 | 1907 |
| Customer success | 0.1.1 | 13 | 50 | 4 | 0 | 3 | 1179 |
| Pricing and contracts | 0.2.0 | 12 | 48 | 3 | 0 | 2 | 1124 |
| Partner and channel | 0.1.1 | 9 | 36 | 2 | 0 | 2 | 840 |
| **Total** | | 158 | 382 | 35 | 5 | 22 | 9827 |

## Checks

- Part III conformance (ke_ingest.check) and the domain rules D1–D6: **0 errors, 0 warnings**, 60 notes.
- Lineage: 40 of 40 domain classes and relations reach BFO/RO/IAO through the core.
- Insulation: every file refers only to the core, the Commercial Operations container and its own domain.
- Primitives: 158 domain primitives, none duplicating a core or sibling primitive; 1 declared homonyms (`homonyms.csv`); 20 general primitives proposed for promotion to the core (`promotion-candidates.csv`).
- Concepts: 382 taxonomy concepts, every one linked to its primitives (`concept-links.csv`); 68 have a label word not covered by a primitive (listed in `unmatched_words` for review).

## Errors

None.

## Warnings

None.

## Notes

- commercial-operations: vocabulary-domain-commercial-operations-0.3.0: Genus plus differentia (§3.7): …/vocabulary/domain-commercial-operations/engagement: does not open "A …/An …": The depth and frequency of a party's interaction with the or
- commercial-operations: vocabulary-domain-commercial-operations-0.3.0: Genus plus differentia (§3.7): …/vocabulary/domain-commercial-operations/payroll: does not open "A …/An …": The calculation, payment and recording of workers' wages, wi
- commercial-operations: vocabulary-domain-commercial-operations-0.3.0: Genus plus differentia (§3.7): …/vocabulary/domain-commercial-operations/unemployment: does not open "A …/An …": The condition of a person who is able and available to work 
- commercial-operations: vocabulary-domain-commercial-operations-0.3.0: Genus plus differentia (§3.7): …/vocabulary/domain-commercial-operations/human-capital-management: does not open "A …/An …": The practices and technology an organization uses to recruit
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/awareness: does not open "A …/An …": The degree to which the parties in a market know of a brand 
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/positioning: does not open "A …/An …": The place an offering is meant to hold in the minds of a tar
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/generation: does not open "A …/An …": The creation of something, such as leads or demand, through 
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/firmographics: does not open "A …/An …": The characteristics of an organization used to segment a mar
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/public-relations: does not open "A …/An …": The management of the information the organization shares wi
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/social-media: does not open "A …/An …": Websites and applications through which parties create and s
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/search-engine-optimization: does not open "A …/An …": The practice of improving content so that search engines sho
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/intelligence: does not open "A …/An …": Information gathered and analyzed to inform decisions about 
- marketing: vocabulary-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/status-quo: does not open "A …/An …": The buyer's current way of getting a job done, kept when it 
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/case-study: does not open "A …/An …": Marketing content that tells how a client used an offering t
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/value-proposition: does not open "A …/An …": Marketing content that states the value an offering delivers
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/positioning: does not open "A …/An …": Marketing content that states the place an offering is meant
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitive-intelligence: does not open "A …/An …": Intelligence about competitors, their offerings and the mark
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitor-profile: does not open "A …/An …": Competitive intelligence that describes a competitor, its of
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/battlecard: does not open "A …/An …": Competitive intelligence that equips sellers to position an 
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitive-landscape: does not open "A …/An …": Competitive intelligence that gives an overview of the compe
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/pricing-intelligence: does not open "A …/An …": Competitive intelligence about the prices and pricing models
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/market-intelligence: does not open "A …/An …": Intelligence about the buyers, segments, demand and regulati
- marketing: taxonomy-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitive-insight: does not open "A …/An …": Competitive intelligence that states a finding about a compe
- marketing: ontology-domain-marketing-0.1.1: Genus plus differentia (§3.7): …/ontology/domain-marketing/battlecard: does not open "A …/An …": Intelligence that equips sellers to position an offering aga
- legal: vocabulary-domain-legal-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-legal/governing-law: does not open "A …/An …": The law of the jurisdiction that the parties agree will gove
- legal: vocabulary-domain-legal-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-legal/internal-revenue-code: does not open "A …/An …": The body of federal statutory tax law, including the provisi
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employee-benefits-law: does not open "A …/An …": Law that governs benefit plans offered to employees and the 
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employee-retirement-income-security-act: does not open "A …/An …": Employee benefits law that sets standards for private-sector
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/patient-protection-and-affordable-care-act: does not open "A …/An …": Employee benefits law that sets health coverage requirements
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/consolidated-omnibus-budget-reconciliation-act: does not open "A …/An …": Employee benefits law that requires continuation coverage un
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/health-insurance-portability-and-accountability-act: does not open "A …/An …": Employee benefits law that protects health information and t
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employment-law: does not open "A …/An …": Law that governs the relationship between employers and the 
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/fair-labor-standards-act: does not open "A …/An …": Employment law that sets wage, overtime and recordkeeping st
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/family-and-medical-leave-act: does not open "A …/An …": Employment law that entitles eligible employees to job-prote
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/americans-with-disabilities-act: does not open "A …/An …": Employment law that prohibits discrimination against people 
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employment-tax-law: does not open "A …/An …": Law that imposes, and sets who must pay and report, taxes on
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/federal-unemployment-tax-act: does not open "A …/An …": Employment tax law that funds unemployment insurance through
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/federal-insurance-contributions-act: does not open "A …/An …": Employment tax law that funds social security and medicare t
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/internal-revenue-code: does not open "A …/An …": Employment tax law that is the body of federal statutory tax
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/small-business-efficiency-act: does not open "A …/An …": Employment tax law that created the certification program fo
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/workers-compensation-law: does not open "A …/An …": Law, set by each state, that requires employers to provide w
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/unemployment-insurance-law: does not open "A …/An …": Law, set by each state within federal rules, that governs un
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/insurance-law: does not open "A …/An …": Law that governs the sale of insurance and the parties licen
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/professional-employer-organization-law: does not open "A …/An …": Law, set by most states, that requires professional employer
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/marketing-communication-law: does not open "A …/An …": Law that governs how the organization may contact parties to
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/telephone-consumer-protection-act: does not open "A …/An …": Marketing communication law that restricts calls and texts w
- legal: taxonomy-domain-legal-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-legal/controlling-the-assault-of-non-solicited-pornography-and-marketing-act: does not open "A …/An …": Marketing communication law that sets rules for commercial e
- customer-success: vocabulary-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-customer-success/health: does not open "A …/An …": The overall condition of a client relationship, judged from 
- customer-success: vocabulary-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-customer-success/adoption: does not open "A …/An …": The extent to which a client and its employees use the servi
- customer-success: vocabulary-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/vocabulary/domain-customer-success/satisfaction: does not open "A …/An …": The degree to which a client's experience meets or exceeds i
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/client-churn: does not open "A …/An …": Churn in which a client ends its agreement.
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/worksite-employee-churn: does not open "A …/An …": Churn in which a client keeps its agreement but covers fewer
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/price-driven-churn: does not open "A …/An …": Client churn caused by the client's judgment that the price 
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/benefits-renewal-churn: does not open "A …/An …": Client churn caused by an increase in benefit rates at renew
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/service-failure-churn: does not open "A …/An …": Client churn caused by failures in the services delivered to
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/competitive-churn: does not open "A …/An …": Client churn in which the client moves to a competitor.
- customer-success: taxonomy-domain-customer-success-0.1.1: Genus plus differentia (§3.7): …/taxonomy/domain-customer-success/acquisition-churn: does not open "A …/An …": Client churn caused by the client being acquired by, or merg
- pricing-and-contracts: vocabulary-domain-pricing-and-contracts-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-pricing-and-contracts/underwriting: does not open "A …/An …": The assessment of the risk of covering a client, used to dec
- pricing-and-contracts: vocabulary-domain-pricing-and-contracts-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-pricing-and-contracts/burden: does not open "A …/An …": The total cost an employer bears for a worker beyond wages, 
- pricing-and-contracts: vocabulary-domain-pricing-and-contracts-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-pricing-and-contracts/term: does not open "A …/An …": The period for which an agreement is in force.
