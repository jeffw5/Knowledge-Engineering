# Build report: operational areas and domains

Built 2026-10-22T02:04:02Z against Baseline Core v1.0 (core 0.1.0) by `_build/build_domains.py`.

| Operational area | Area or domain | Version | Vocabulary terms | Taxonomy concepts | Classes | Relations | Shapes | Triples |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Commercial Operations | Commercial Operations | 0.4.0 | 38 | 58 | 8 | 3 | 4 | 1748 |
| Commercial Operations | Domain Sales | 0.4.0 | 13 | 59 | 4 | 0 | 3 | 1351 |
| Commercial Operations | Domain Sales.Partner & Channel | 0.2.0 | 9 | 36 | 2 | 0 | 2 | 850 |
| Commercial Operations | Domain Marketing | 0.2.0 | 34 | 66 | 3 | 0 | 3 | 1675 |
| Commercial Operations | Domain Pricing | 0.3.0 | 10 | 29 | 3 | 0 | 2 | 808 |
| Commercial Operations | Domain Customer Care | 0.2.0 | 13 | 50 | 4 | 0 | 3 | 1187 |
| Business Operations | Business Operations | 0.1.0 | 3 | 8 | 0 | 0 | 0 | 244 |
| Business Operations | Domain Legal | 0.2.0 | 42 | 90 | 11 | 2 | 5 | 2359 |
| Human Resources Service Operations | Human Resources Service Operations | 0.1.0 | 10 | 9 | 0 | 0 | 0 | 383 |
| Technical Operations | Technical Operations | 0.1.0 | 2 | 7 | 0 | 0 | 0 | 231 |
| **Total** | | | 174 | 412 | 35 | 5 | 22 | 10836 |

## Checks

- Part III conformance (ke_ingest.check) and the domain rules D1–D6, D27: **0 errors, 0 warnings**, 76 notes.
- Lineage: 40 of 40 domain classes and relations reach BFO/RO/IAO.
- Insulation (D27): classes, relations, concepts and imports refer only to the core, the operational area, parent domains, the domain itself and the APQC reference registry; primitives are cited across areas, never copied.
- Primitives: 174 domain primitives, none duplicating a core or sibling primitive; 1 declared homonyms (`homonyms.csv`); 20 general primitives proposed for promotion to the core (`promotion-candidates.csv`).
- Concepts: 412 taxonomy concepts, every one linked to its primitives (`concept-links.csv`); 75 have a label word not covered by a primitive (listed in `unmatched_words` for review).

## Errors

None.

## Warnings

None.

## Notes

- commercial-operations: vocabulary-commercial-operations-0.4.0: Genus plus differentia (§3.7): …/vocabulary/commercial-operations/engagement: does not open "A …/An …": The depth and frequency of a party's interaction with the or
- commercial-operations: vocabulary-commercial-operations-0.4.0: Genus plus differentia (§3.7): …/vocabulary/commercial-operations/payroll: does not open "A …/An …": The calculation, payment and recording of workers' wages, wi
- commercial-operations: vocabulary-commercial-operations-0.4.0: Genus plus differentia (§3.7): …/vocabulary/commercial-operations/unemployment: does not open "A …/An …": The condition of a person who is able and available to work 
- commercial-operations: vocabulary-commercial-operations-0.4.0: Genus plus differentia (§3.7): …/vocabulary/commercial-operations/human-capital-management: does not open "A …/An …": The practices and technology an organization uses to recruit
- commercial-operations: vocabulary-commercial-operations-0.4.0: Genus plus differentia (§3.7): …/vocabulary/commercial-operations/care: does not open "A …/An …": The attention given to meeting the needs of a client after t
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/awareness: does not open "A …/An …": The degree to which the parties in a market know of a brand 
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/positioning: does not open "A …/An …": The place an offering is meant to hold in the minds of a tar
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/generation: does not open "A …/An …": The creation of something, such as leads or demand, through 
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/firmographics: does not open "A …/An …": The characteristics of an organization used to segment a mar
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/public-relations: does not open "A …/An …": The management of the information the organization shares wi
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/social-media: does not open "A …/An …": Websites and applications through which parties create and s
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/search-engine-optimization: does not open "A …/An …": The practice of improving content so that search engines sho
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/intelligence: does not open "A …/An …": Information gathered and analyzed to inform decisions about 
- marketing: vocabulary-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-marketing/status-quo: does not open "A …/An …": The buyer's current way of getting a job done, kept when it 
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/case-study: does not open "A …/An …": Marketing content that tells how a client used an offering t
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/value-proposition: does not open "A …/An …": Marketing content that states the value an offering delivers
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/positioning: does not open "A …/An …": Marketing content that states the place an offering is meant
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitive-intelligence: does not open "A …/An …": Intelligence about competitors, their offerings and the mark
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitor-profile: does not open "A …/An …": Competitive intelligence that describes a competitor, its of
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/battlecard: does not open "A …/An …": Competitive intelligence that equips sellers to position an 
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitive-landscape: does not open "A …/An …": Competitive intelligence that gives an overview of the compe
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/pricing-intelligence: does not open "A …/An …": Competitive intelligence about the prices and pricing models
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/market-intelligence: does not open "A …/An …": Intelligence about the buyers, segments, demand and regulati
- marketing: taxonomy-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-marketing/competitive-insight: does not open "A …/An …": Competitive intelligence that states a finding about a compe
- marketing: ontology-domain-marketing-0.2.0: Genus plus differentia (§3.7): …/ontology/domain-marketing/battlecard: does not open "A …/An …": Intelligence that equips sellers to position an offering aga
- pricing: vocabulary-domain-pricing-0.3.0: Genus plus differentia (§3.7): …/vocabulary/domain-pricing/underwriting: does not open "A …/An …": The assessment of the risk of covering a client, used to dec
- pricing: vocabulary-domain-pricing-0.3.0: Genus plus differentia (§3.7): …/vocabulary/domain-pricing/burden: does not open "A …/An …": The total cost an employer bears for a worker beyond wages, 
- customer-care: vocabulary-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-customer-care/health: does not open "A …/An …": The overall condition of a client relationship, judged from 
- customer-care: vocabulary-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-customer-care/adoption: does not open "A …/An …": The extent to which a client and its employees use the servi
- customer-care: vocabulary-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-customer-care/satisfaction: does not open "A …/An …": The degree to which a client's experience meets or exceeds i
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/client-churn: does not open "A …/An …": Churn in which a client ends its agreement.
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/worksite-employee-churn: does not open "A …/An …": Churn in which a client keeps its agreement but covers fewer
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/price-driven-churn: does not open "A …/An …": Client churn caused by the client's judgment that the price 
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/benefits-renewal-churn: does not open "A …/An …": Client churn caused by an increase in benefit rates at renew
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/service-failure-churn: does not open "A …/An …": Client churn caused by failures in the services delivered to
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/competitive-churn: does not open "A …/An …": Client churn in which the client moves to a competitor.
- customer-care: taxonomy-domain-customer-care-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-customer-care/acquisition-churn: does not open "A …/An …": Client churn caused by the client being acquired by, or merg
- business-operations: vocabulary-business-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/business-operations/accounting: does not open "A …/An …": The recording, classification and reporting of an organizati
- business-operations: vocabulary-business-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/business-operations/billing: does not open "A …/An …": The preparation and issue of invoices for the services an or
- business-operations: vocabulary-business-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/business-operations/accounts-receivable: does not open "A …/An …": The amounts owed to an organization by its clients for servi
- legal: vocabulary-domain-legal-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-legal/governing-law: does not open "A …/An …": The law of the jurisdiction that the parties agree will gove
- legal: vocabulary-domain-legal-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-legal/internal-revenue-code: does not open "A …/An …": The body of federal statutory tax law, including the provisi
- legal: vocabulary-domain-legal-0.2.0: Genus plus differentia (§3.7): …/vocabulary/domain-legal/term: does not open "A …/An …": The period for which an agreement is in force.
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employee-benefits-law: does not open "A …/An …": Law that governs benefit plans offered to employees and the 
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employee-retirement-income-security-act: does not open "A …/An …": Employee benefits law that sets standards for private-sector
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/patient-protection-and-affordable-care-act: does not open "A …/An …": Employee benefits law that sets health coverage requirements
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/consolidated-omnibus-budget-reconciliation-act: does not open "A …/An …": Employee benefits law that requires continuation coverage un
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/health-insurance-portability-and-accountability-act: does not open "A …/An …": Employee benefits law that protects health information and t
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employment-law: does not open "A …/An …": Law that governs the relationship between employers and the 
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/fair-labor-standards-act: does not open "A …/An …": Employment law that sets wage, overtime and recordkeeping st
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/family-and-medical-leave-act: does not open "A …/An …": Employment law that entitles eligible employees to job-prote
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/americans-with-disabilities-act: does not open "A …/An …": Employment law that prohibits discrimination against people 
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/employment-tax-law: does not open "A …/An …": Law that imposes, and sets who must pay and report, taxes on
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/federal-unemployment-tax-act: does not open "A …/An …": Employment tax law that funds unemployment insurance through
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/federal-insurance-contributions-act: does not open "A …/An …": Employment tax law that funds social security and medicare t
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/internal-revenue-code: does not open "A …/An …": Employment tax law that is the body of federal statutory tax
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/small-business-efficiency-act: does not open "A …/An …": Employment tax law that created the certification program fo
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/workers-compensation-law: does not open "A …/An …": Law, set by each state, that requires employers to provide w
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/unemployment-insurance-law: does not open "A …/An …": Law, set by each state within federal rules, that governs un
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/insurance-law: does not open "A …/An …": Law that governs the sale of insurance and the parties licen
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/professional-employer-organization-law: does not open "A …/An …": Law, set by most states, that requires professional employer
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/marketing-communication-law: does not open "A …/An …": Law that governs how the organization may contact parties to
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/telephone-consumer-protection-act: does not open "A …/An …": Marketing communication law that restricts calls and texts w
- legal: taxonomy-domain-legal-0.2.0: Genus plus differentia (§3.7): …/taxonomy/domain-legal/controlling-the-assault-of-non-solicited-pornography-and-marketing-act: does not open "A …/An …": Marketing communication law that sets rules for commercial e
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/administration: does not open "A …/An …": The organized performance of the routine work of running an 
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/retirement: does not open "A …/An …": The period after a worker leaves the workforce, and the savi
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/sponsorship: does not open "A …/An …": The act of establishing and maintaining a benefit plan and b
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/government: does not open "A …/An …": The bodies that make, administer and enforce law and regulat
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/talent: does not open "A …/An …": The skills and abilities of the people an employer attracts,
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/coaching: does not open "A …/An …": Guidance given to a person over time to improve their perfor
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/culture: does not open "A …/An …": The shared values, beliefs and behaviors that characterize a
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/ethics: does not open "A …/An …": The principles of right conduct that govern a person or an o
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/stewardship: does not open "A …/An …": The responsible care and management of something entrusted t
- hr-service-operations: vocabulary-hr-service-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/hr-service-operations/experience: does not open "A …/An …": What a person perceives and feels in their interactions with
- technical-operations: vocabulary-technical-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/technical-operations/engineering: does not open "A …/An …": The disciplined design, construction and operation of system
- technical-operations: vocabulary-technical-operations-0.1.0: Genus plus differentia (§3.7): …/vocabulary/technical-operations/cybersecurity: does not open "A …/An …": The protection of information systems, networks and data fro
