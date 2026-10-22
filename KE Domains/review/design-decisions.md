# Commercial Operations design decisions (0.1.0)

These decisions govern the Commercial Operations domains. They extend the Baseline Core v1.0 decisions (`KE Baseline/Baseline Core v1.0/review/design-decisions.md`, cited here as "Baseline n") and never override them. D1 records Jeffrey Wallk's instructions of 2026-10-19. The other decisions are proposed in this release and await his review.

## Structure and insulation

- **D1 · Folders.** Each operational area has its own folder under `KE Domains/`, and each domain within an area has its own subfolder. This separates domains and insulates them from changes in top-down modeling. The baseline stays pristine. *(Stated, 2026-10-19.)*
- **D2 · Container domain.** Every operational area has a container domain named after the area: here `commercial-operations`. Primitives, concepts and classes used by two or more domains of the area live in the container. A domain refers only to the core, its area's container and itself, never to a sibling. This is what lets one domain change without touching the others. *(Proposed.)*
- **D3 · Pinned imports.** A domain ontology imports the core ontology and its container by their ontology IRIs (`owl:imports …/ontology/core/`), so that tools such as the KE Workbench resolve them, and pins the versions it was built against with `dcterms:requires …/ontology/core/0.1.0/`. A core release reaches a domain only when the domain is rebuilt against it and re-released. *(Proposed; amended in 0.1.1/0.2.0. In 0.1.0, imports named the version IRIs, which the workbench could not resolve.)*
- **D4 · Named graphs per domain asset.** Each vocabulary, taxonomy, ontology and shapes file loads into its own named graph. The load script replaces only those graphs, backs them up first, and checks that the baseline statement count is unchanged. *(Proposed.)*
- **D5 · Formalizing core concepts from a domain.** When a domain class formalizes an existing core taxonomy concept (core "Statute" → `legal:statute`, core "Client service agreement" → `commercialops:client-service-agreement`, core "Worksite employee" → `commercialops:worksite-employee`), the `core:formalizedBy` triple is stored in the domain's ontology graph rather than in the core. Unloading the domain removes it. *(Proposed; see open question 6.)*

## Terms

- **D6 · Domain primitives.** A domain vocabulary holds only primitives that are missing from the core (Baseline 1–3, 7). A primitive is unique across the core and every domain. The build rejects a duplicate label unless it is declared a homonym with its sense difference stated (`homonyms.csv`).
- **D7 · Promotion candidates.** A general primitive the core lacks (analysis, stage, program, certification…) is added to the domain that first needs it, or to the container if several do. It is flagged for promotion to the core (`promotion-candidates.csv`) rather than added to the baseline, so the baseline is only changed by a deliberate core release.
- **D8 · Specialize, don't redefine.** A domain concept that narrows a core or container concept links to it with `skos:broadMatch`. The core concept is not copied. For example, legal "Regulatory obligation" broad-matches core "Obligation", and marketing "Competitive alternative" broad-matches the container's "Competitor".
- **D9 · Acronyms.** Preferred labels spell out acronyms; the acronym is kept as an alternative label (PEO, ASO, HCM, ICP, CPEO, ERISA, ACA, MQL, NPS…). Named statutes are multiword lexical units (Baseline 3), labeled in sentence case as the core does for its named regulations.

## Model

- **D10 · Records are information assets.** Account, lead, opportunity, proposal, quote, census, intelligence and battlecard are information assets (BFO generically dependent continuants) *about* the parties and offerings they concern (`core:concerns`). The selling, marketing and success steps that create and advance them consume and produce them, so their history stays anchored on the process step.
- **D11 · Stages are the provider's view.** Selling stages (Discover, Qualify, Evaluate, Propose, Decide, Onboard), funnel stages and client success stages are process steps or statuses from the organization's point of view (Baseline 21). Selling and client success steps reach the persona's job steps only through `core:addresses`, intentionally not one-to-one. That gap is where value gaps, and leading churn indicators, are measured.
- **D12 · Roles, not personas.** Buying roles (champion, gatekeeper, decision maker, economic buyer, influencer), competitor, channel partner and worksite employee are roles (BFO realizable entities) borne by persons or organizations. Buyer personas are persona instances and are not typed by role (Baseline 22–23).
- **D13 · Deontic norms in the legal domain.** Obligation, permission, prohibition and right are classes under `legal:norm`, after the Legal Knowledge Interchange Format. A norm binds a role (`legal:binds`) and is part of the provision, clause or policy that states it (`core:componentOf`): that provision is the norm's single source of truth for rules, constraints and logic. Statutes and regulations name their jurisdiction (`legal:hasJurisdiction`).
- **D14 · Contract steps are process steps.** Drafting, pricing review, negotiation, approval, signature, amendment, renewal and termination are contract management steps. They are not lifecycle stages; every asset keeps the five Baseline lifecycle stages (Baseline 11). Agreement events stay in the core event taxonomy, and the domain steps broad-match them.
- **D15 · No finance terms.** Revenue, margin, gross profit, billing and invoices belong to Domain Finance (Baseline 7) and are not modeled here. Commercial measures count worksite employees, opportunities, rates and shares.
- **D16 · Generic professional employer organization language.** Terms are industry-generic. The organization's own names for its offerings, teams and measures can be added as alternative labels once confirmed.

## Assembly (Sales 0.2.0)

These decisions put Jeffrey Wallk's component-design and assembly approach into practice: services and the processes that enable them are built as separate components, then assembled into the domain. *(Approach stated 2026-10-19; the tiers and rules below are proposed.)*

- **D17 · Assembly tiers.** The vocabulary, taxonomy, ontology and shapes stay one each per domain: the parts catalog and the joining rules. The components are instance graphs, each in its own named graph under `…/resource/domain-<name>/<tier>/<id>/`:
  - **persona graph** (in the container, shared by every domain): personas, jobs, job steps, desired outcomes, metric cards and targets;
  - **process graph**: the standard selling process and who performs its steps;
  - **step graphs**: one per reusable selling step, with its kinds (stage and activity), inputs, outputs, performers and the job steps it addresses;
  - **service graphs**: one per service, which assemble it by joining step graphs and record what it delivers today;
  - **manifest**: the release, listing the component graphs and the asset versions they require (core "Release manifest").

  A component never copies another; it refers to it. Kinds are defined once, in the taxonomy. *(The tier names are provisional; see open questions.)*
- **D18 · Standard instances.** A step, record or service in a component graph stands for the organization's standard step, record or service, not for one occurrence of it. In strict BFO a standard step is a plan specification, and each occurrence (this census collection, for this prospect, on this date) realizes it. Occurrences are not modeled yet; when execution data is captured, they will link to the standard steps. The census shape warning (a census with no persons) is a symptom of this.
- **D19 · Joins.** A service is assembled from:
  - the step that is its delivery (`core:deliveryOf`);
  - the steps it depends on (`core:supports`, Baseline 26);
  - their order (`core:precedes`).

  A step is assembled from its inputs and outputs (`core:consumes`, `core:produces`), the job steps it addresses (`core:addresses`), its performers (`core:performedBy`: the sales organization for manual work, the sales advisor agent for automated work) and the role it fulfills. Every resource is typed by a core or domain class and classified by a taxonomy concept with `dcterms:type`.
- **D20 · Assembly measures.**
  - A node's **joins** are its parts less one. Primitives are atoms; a concept is joined from its primitives; an instance from its concepts and the resources it is assembled with; a service from its concept and its steps.
  - The **assembly index (modeled pathway)** of a service is the number of joins in its closure, with shared parts counted once. It is an upper bound on the true assembly index.
  - **Copy number** is how many services contain a part. Shared steps and records with high copy number are platform and automation candidates (Baseline 14).
- **D21 · Value gaps.** A desired outcome (persona graph: job step, metric card, target) is compared with the delivered outcome (service graph: the same job step and metric card, with the measured baseline). Values are carried by `rdf:value` on target and actual-value measures. A job step a service addresses without a measured baseline is "not yet measured", not "met".
- **D22 · Shared terms move up.** Census moved from pricing and contracts to the container in 0.2.0 (D2), because Sales collects it and pricing and contracts underwrites from it. The PEO buyer persona graph lives in the container for the same reason.

## Editing (D23)

- **D23 · One graph for every edit.** *(Agreed by Jeffrey Wallk, 2026-10-20.)* All edits to models and instances, assembly components included, are made in GraphDB, whatever view or editor is used to make them. The workbench pages are views of the graph: Service Assembly (read only in 3.4.0, editing controls to follow), the model editors and the Model Manager. The Turtle and TriG files are exported releases of the graph, not a second place to edit. `_build/build_assembly.py` stays as the release check (typing, classification, insulation, closure, shapes) and computes the assembly measures (assembly index, copy number, value gaps). Until editing controls exist, the specification files in `_build/` remain the way to add services and steps; once they do, the specifications are retired and the graph is exported instead.

## Service › Process › Process step (D24)

- **D24 · Services are enabled by processes; personas are a separate assembly.** *(Stated by Jeffrey Wallk, 2026-10-20; the relations below were agreed the same day.)*
  - A service is enabled by one or more processes (`core:supports`). A process is built from process steps (`core:hasStep`), in order (`core:precedes`). The step that hands the service over is its `core:deliveryOf`. Processes, not only steps, are reusable components: census collection is one process that enables two services.
  - Every process step carries its **SIPOCM**, in terms of the core ontology: **S**upplier, **I**nput (`core:consumes`), the **P**rocess step and who performs it (`core:performedBy`, `core:fulfillsRole`), **O**utput (`core:produces`), **C**ustomer and **M**easure (`core:measuredBy`).
  - Inside an assembly, suppliers and customers are derived from the data flow: the supplier of an input is whoever performs the step that produces it, and the customer of an output is whoever performs the step that consumes it. Parties outside the assembly (the prospect, a broker) are stated with two relations added to the Commercial Operations container 0.3.0, `commercialops:hasSupplier` and `commercialops:hasCustomer`. They specialize RO *has participant* (the supplier or customer takes part in the step at its boundary) and point to a party or a role. Both are candidates for promotion to the core, since SIPOC applies to every process.
  - The persona model, the jobs model and the desired outcomes mapped to each job step are a separate assembly. The Sales assembly 0.3.0 does not refer to them, and the build fails if it does. The bridge from selling steps to job steps (`core:addresses`) and the delivered outcomes live in the **Sales value map** (value-map graph and its own manifest, with the PEO buyer persona graph). The value map is shown on a separate Value Mapping page.
  - Measures of a step (for example the census validation failure rate) are the provider's measures and belong to the service assembly. Metric cards of desired outcomes are the buyer's measures and belong to the value map. The value map relates the two.

## Enterprise service catalog (D25)

- **D25 · Two service portfolios in one enterprise service catalog.** *(Agreed by Jeffrey Wallk, 2026-10-21. It applies to the whole enterprise; this file moved from `Commercial Operations/review/` to `KE Domains/review/` for that reason.)*
  - **Hierarchy.** Enterprise › Operational area › Domain › domain services and processes. The four operational areas are Business Operations, Commercial Operations, HR Service Operations and Technical Operations. Each aggregates domains (departments); Commercial Operations aggregates Sales, Marketing, Legal, Customer success, Pricing and contracts, and Partner and channel.
  - **External services** (what clients and their worksite employees receive) follow Jeffrey Wallk's HR Services & PEO Enterprise Business Model: Service line › Domain (L1) › Bounded context (L2) › Domain service (L3) › Business process. There are 9 service lines, 8 L1 domains, 17 bounded contexts, 74 domain services and 148 business processes.
  - **Internal domain services** (what each department provides, its department setup) are built on the APQC Process Classification Framework. APQC is used **only** for internal domain services.
  - **One process registry.** The APQC PCF is loaded once as a read-only reference taxonomy. Each APQC element has exactly one owner domain. Domain process kinds and PEO extensions link to it with skos:exactMatch or skos:broadMatch; other domains refer to the owner's process and never re-create it.
  - **Enterprise service catalog, above the operational areas.** Every area publishes its services, external and internal, to the catalog as interfaces. A domain may consume another area's service only through its published entry, never by referring to that area's processes or resources. This extends the insulation rule (D1): a domain refers to the core, its area's container, itself and the enterprise service catalog.
  - **How the portfolios meet.** The business processes behind an external domain service are performed by internal domains (the model's supportedByOperation). In this way an external service is delivered through the internal services and processes of the departments that support it.

## Operational areas, domains and naming (D26)

- **D26 · The four operational areas and their domains, and the naming standard.** *(Stated by Jeffrey Wallk, 2026-10-21; enterprise-wide.)*
  - **Commercial Operations:** Sales, Marketing, Pricing, Customer Care.
  - **HR Service Operations** (the external service domains of the HR Services & PEO Enterprise Business Model): Workforce Administration & Payroll; Employee Benefits & Retirement Sponsorship; Government Compliance & Employer Risk Management; Talent Management & Organizational Development; Client Relationship & Business Development; HR Technology Platform & Employee Experience; Workforce Development, Coaching & Performance Measurement; Organizational Values, Culture & Ethics Stewardship.
  - **Business Operations:** Finance, Accounting, HR, Billing & AR, Compliance, Legal, Security.
  - **Technical Operations:** Business Systems Services, AI Strategy & Enterprise Analytic Services, Platform Services, Data Engineering Services, Knowledge Engineering Services, Cybersecurity Services.
  - **Naming standard.** An asset's name is a first qualifier followed by a second qualifier.
    - The first qualifier is one of three forms: Core; Domain L1.L2.L3; or the operation name.
    - The second qualifier is Vocabulary, Taxonomy or Ontology.
    - Domains nest up to three levels, for example:
      - L1 "Domain Finance";
      - L2 "Domain Finance.Capital Budgeting & Investment Analysis";
      - L3 "Domain Finance.Capital Budgeting & Investment Analysis.Valuation & Deal Screening".
    - For HR Service Operations, the levels are the business model's L1 domain, L2 bounded context and L3 domain service.
  - **Applied 2026-10-21 (Commercial Operations 0.4.0):**
    - Legal moved to Business Operations and took the agreements and contract management with it.
    - Customer success became Domain Customer Care; Pricing and contracts became Domain Pricing.
    - Partner and channel became Domain Sales.Partner & Channel, an L2 of Sales (Jeffrey Wallk's choice).
    - Every asset is titled by the standard.
  - **IRIs** (Jeffrey Wallk's choice):
    - Area assets drop "domain-": `…/ontology/commercial-operations/`, titled "Commercial Operations Ontology".
    - Nested domains join their levels with dots in one segment: `…/taxonomy/domain-sales.partner-and-channel/`; "&" is written "and".
    - The workbench URI pattern check (§3.2) accepts the dots.
  - **"HR" in titles.** Part III spells out "HR" in preferred labels (the configured expansion), so the HR Service Operations assets are titled "Human Resources Service Operations …", with "HR Service Operations …" as the alternative label. The folder keeps the name "HR Service Operations".

## Primitives and cross-area references (D27)

- **D27 · Core terms are the DNA, domain terms are the molecules, and enterprise services are composed from both.** *(Stated and agreed by Jeffrey Wallk, 2026-10-21.)*
  - The core vocabulary, taxonomy and ontology support the core domain ontology, and the domain ontologies are built from it. Enterprise services are composed from core terms and domain-specific terms. There is no enterprise-level vocabulary.
  - **Each primitive has one owner**, the domain (or area) whose subject it is. Any domain in any area may build its concepts from it (`dcterms:subject`, `core:hasPrimaryTerm`), citing it and never copying it. For example, Domain Sales builds "Benefits plan comparison" from benefit.
  - **Classes, relations, concepts (`skos:broader`, `broadMatch`, `exactMatch`, `core:formalizedBy`), imports and instances stay insulated.** They refer only to:
    - the core;
    - the domain's own operational area;
    - its parent domains (an L2 may refer to its L1);
    - itself;
    - the APQC reference registry.
  - Classes and instances from different areas are combined only in enterprise services. This extends D1. The builder, the load script and the Service Assembly page enforce it.
  - **Shared primitives that cross areas stay where they are until their owning domain exists.** Benefit, payroll, insurance, workers' compensation and claim are in the Commercial Operations vocabulary today, cited by Legal and the HR Service Operations taxonomy. They move to their owning HR Service Operations domains when those are built.
  - **Agreements moved to Legal.** The client service agreement, commercial agreement and clause (classes, concepts and the clause primitive) went from Commercial Operations to Domain Legal. So did the contract management steps, agreement terms and statuses, with the term and signature primitives, from Pricing and contracts. Contracts are now a single domain's concern, and Legal no longer imports any Commercial Operations class.

## Commercial Operations on APQC PCF 7.4 (D28, D29)

- **D28 · The process levels of a domain are APQC's: process group (L2) › process (L3) › activity (L4), and an activity's tasks (L5) are its steps.** *(Levels chosen by Jeffrey Wallk, 2026-10-21.)*
  - **What is instantiated.** Each domain instantiates only the activities it owns (`core:process`) and their steps (`core:process-step`, or `sales:selling-step` in Sales). L2 and L3 are not instantiated: the topology reads them from the APQC reference registry (`skos:broader`), so one APQC process can hold activities owned by different domains without a cross-domain part-of link. For example, 3.5.3 is Sales', but 3.5.3.10 Conduct profitability analysis is Pricing's.
  - **Classification.** An activity or step is classified (`dcterms:type`) by the APQC element it is, and carries its hierarchy number as `skos:notation`. A PEO extension is classified by the element it extends, with its own identifier as notation (PX-…). The older Sales processes (census collection and the rest) reach APQC through their kind concept's `skos:broadMatch`, as before.
  - **Leaves.** An activity with no L5 tasks is performed as one step, a step that is the activity itself. An L3 process with no L4 activities, such as 3.3.8 Develop go-to-market strategy, is itself the activity.
  - **Not applicable.** Elements a PEO does not perform, such as warranty, recall, packaging and point of sale, are not instantiated. The registry records their applicability (`skos:note "PEO applicability: Not applicable. …"`), and the topology can show them.
  - **Shared records and parties.** The records steps consume and produce, and the parties and roles outside the processes, are in two Commercial Operations graphs (`…/resource/commercial-operations/record-graph/commercial-records/` and `…/party-graph/commercial-parties/`). A record one domain produces and another consumes is the hand-off between them; the supplier and customer of a step are derived from it (D24). Each domain's own organization, digital agent and role are in its party graph.
  - **Components.** There is one process graph per APQC process (L3) per domain, holding its activities, their steps, the SIPOCM of each step and the step measures. There is one service graph per service, and one manifest per domain assembly: Sales 0.5.0, and Marketing, Pricing, Customer Care and Sales.Partner & Channel 0.1.0. The content is authored in `_build/apqc_commercial.py`.
  - **Drafts.** Every SIPOCM, measure and service of this release is a draft for review (lifecycle status Draft).
- **D29 · APQC PCF 7.4 replaces 7.2.1 in the reference registry, with category 6.0 added for Customer Care.**
  - The registry (APQC PCF Taxonomy 0.2.0) holds categories 3.0 and 6.0 of PCF 7.4 (August 2024), 309 elements. Element IDs are stable across releases. `Reference/apqc-pcf/crosswalk-7.2.1-to-7.4.csv` lists what changed: 9 elements added, 3 removed, 2 renumbered, 5 renamed.
  - APQC released **PCF 8.0 on 2026-02-27**. Its text could not be retrieved here (APQC's download needs a sign-in). When a copy is saved in `Reference/apqc-pcf/source/`, the registry moves to 8.0 (0.3.0) with a 7.4 → 8.0 crosswalk, and the assemblies are rebuilt. Since they point to element IDs, only renumbered or removed elements need attention.
  - The PCF is APQC's open standard, licensed for use and derivative works with attribution (www.apqc.org/pcf). APQC's names are kept as published on the registry; the domain resources carry labels that follow Part III.
