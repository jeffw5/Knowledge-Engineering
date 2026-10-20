# Core design decisions (Baseline Core v1.0)

Decisions Jeffrey Wallk made while reviewing the core vocabularies, taxonomies and ontology. They govern the primitives backfill, the relinking of taxonomy concepts and the core domain ontology rebuild.

## Primitives and polymorphic terms (2026-10-18/19)

1. A core vocabulary holds **primitives**: unique, irreducible terms. Core taxonomy concepts are built from primitives; a concept built from more than one primitive is **polymorphic**.
2. Only missing **primitives** are backfilled, never polymorphic terms.
3. A primitive may be a multiword lexical unit when its meaning is not the sum of its words (circuit breaker, segregation of duties, life event, waiting period, application programming interface).
4. Every concept carries `dcterms:subject` to each primitive it is built from; `core:hasPrimaryTerm` points to the head primitive. A concept that is itself a primitive has just that one.
5. **Polymorphic terms are phrases, never new words.** Concatenating primitives into one word (ServiceDelivery, ProcessStep) creates new words and ambiguity in search and display. Labels are spaced phrases; IRIs join primitives with hyphens (`…/taxonomy/core-process/approval-step`, `…/ontology/core/process-step`), for single-primitive concepts too. Amends Part III §3.2 (UpperCamelCase for classes and taxonomy concepts).
6. Modifier adjectives are not primitives; where useful they are kept as alternative labels of the primitive they qualify (missing → completeness, invalid → validity, inconsistent → consistency, stale → timeliness, duplicate → uniqueness, incorrect → accuracy).
7. Domain-specific terms stay out of the core (revenue belongs to domain finance).
8. The core ontology keeps a polymorphic class only where it differs in BFO (a different BFO parent or its own axioms); other polymorphic terms live in the taxonomies, formalized by the class of their head primitive.

## Assets, products and services (2026-10-19)

9. **Asset** is the genus. Physical asset (material entity) and information asset (digital, information content) are its BFO-grounded kinds.
10. **Product and service are both types of asset**, assembled from other assets. They are not a genus over physical or digital: physical and digital describe the assets they are assembled from. A product can be physical or digital; a product delivers one or more services.
11. All assets have lifecycles; every asset goes through the same five stages: Discover, Define, Design, Develop, Deliver. Introduction, growth, maturity and decline are not lifecycle stages; growth is a general primitive (an increase in a quantity over time), and sales of a product may have growth.
12. **Delivery is a type of activity under process.** "Service delivery" is a polymorphic phrase: a specific service (instance) plus the process by which it is delivered, which the asker maps to the outcomes they want for the jobs they are trying to get done. A service is delivered manually or through automation.
13. Products and services are bundled or packaged by marketing and sold to customers. Sales channels: business-to-consumer, business-to-business, business-to-business-to-consumer, business-to-government (acronyms as alternative labels).
14. Platforms are created to create and deliver products and services for a wider range of customers, giving scale across markets by industrializing smaller components for reuse.
15. Circuit breaker: a technical component that monitors the trustworthiness of an artificial intelligence agent.

## Persona and Jobs models (2026-10-19)

16. The **Persona model is supported by the Jobs model** (Clayton Christensen's Jobs To Be Done framing). Jobs are broken down by kind (functional, emotional); **desired outcomes are mapped to the job steps** within a job.
17. **Job steps are akin to process steps but intentionally not 1:1**: job steps describe what the customer is trying to get done; process steps describe how the organization does its work.
18. **Persona instances are built by assembling both models** (example: PEO Buyer Personas with JTBD: Client Admin and HR Specialist, each with a job study → jobs → job steps (with a buyer stage: Discover, Qualify, Evaluate, Propose, Decide, Onboard) → desired outcomes written as Minimize/Maximize statements with a metric, target, baseline and metric card).
19. **Jobs are a type of activity**, kept in their own taxonomy because they are not process models. A job is unique to the job executor performing it; jobs generalize on their own and gain contextual relevance when combined with the persona executing them. Uses: verifying the relevancy of requirements (lifecycle planning, and prompts where the AI circuit breaker evaluates the five dimensions of relevancy); validating relevancy of the user experience of a product or service (delivered outcomes mapped to desired outcomes at each job step); measuring value (gaps between desired and delivered outcomes).
20. **Job kinds are functional and emotional**, both evaluated in the context of the job being performed. A job that involves money (checking a bank account, withdrawing funds, paying for a service or product) is associated with finance; that is a subject association, not a job kind. Core and related jobs as a second facet: agreed.
21. **Buying stages are the provider's point of view**: steps of the selling process for the product or service being sold. A buyer stage may correspond to one or more of the persona's jobs or to steps within a job; it is a question of granularity from the persona's (customer's or consumer's) point of view. Job steps are unique to the job the persona is trying to do and must not be confused with the selling steps built into the user experience; the mismatch between them is where value gaps are created. Lifecycle stages (fully contextualized) belong to asset lifecycles.
22. **There is one Persona model.** Persona instances are many, and are not mapped to job title, role or position in an organization chart (those are specific to employees). Overlaps between a persona and a title, role or position are instance mappings to be curated when scenarios involve employees and the jobs they are trying to get done. Modeled carefully, this can augment identity management, provisioning, protection and personalization.
23. **No role typing of personas.** Typing personas by role bleeds into the job being performed and increases ambiguity and complexity (which are intimately tied as modeling grows). The role-named persona types (analytic, data, knowledge, platform, quality, systems and user experience engineering persona) and the "Persona role" concept leave the persona taxonomy; persona-to-role mappings are curated at instance level.
24. **Lifecycle and market terms** (2026-10-19): development is a lifecycle stage; introduction is an activity; maturity is primarily a commercial/strategic marketing term but is also used in engineering as an operational quality and reliability measure; decline is a commercial/macroeconomic phase but also functions as an engineering, reliability and architectural measure.
25. **Portfolio applies to assets**; portfolio management is the polymorphic term for managing asset portfolios. **Projects and initiatives are containers** associated with the lifecycle management of activities.
26. **Support is an activity associated with Run (operations).** When an activity (process, task) supports another process, service or capability, that is an **explicit dependency**: a causal factor that affects the behaviors and delivered outcomes of what it supports.
27. Maturity keeps both senses in the core: commercial/strategic (marketing) and engineering (operational quality and reliability).
28. **Scope is a container; place is an abstraction for location; national and international are relative** (to a reference jurisdiction).
29. **Capital has three senses**: a claim on assets (accounting), a type of asset (economics), and a property of an asset. Kept in core with a scope note for each sense.
30. Adjectives become their noun primitive, kept as its alternative label (strategic → strategy, deductive → deduction, regulatory → regulation). Exceptions: the RACI terms (responsible, accountable, consulted, informed) and hybrid stay as primitives.
