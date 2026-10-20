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

