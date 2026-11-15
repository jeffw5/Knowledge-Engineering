# Holonic Semantic Governance Architecture (HSGA): Version 6.1

Nov 9, 2026 · @jeffrey

## 1. Document control

This is version 6.1, issued 2026-11-15, of the HSGA architecture. Version 5.0 was the first to fold the lexicon layer, the graph naming standard, tenancy and the logic single source of truth into the v4.2 reference architecture. Version 6.0 adds conversational AI support (section 16) and aligns the document with the Semantic Governance Guide v2.4 and the SKL as SSOT proposal; it was drafted as 5.1 on 2026-11-13 and renumbered because it changes the asset types. Version 6.1 corrects the Wymore lineage of the system model and adds Addendum F on Model M and the AI Circuit Breaker.

| Field | Value |
| --- | --- |
| Document | Holonic Semantic Governance Architecture (HSGA) |
| Current version | 6.1, issued 2026-11-15. A minor change on 6.0: Model M lineage corrected and Addendum F added. The number 6.0 is proposed by the owner because aligning the asset types to six is a major-class change under section 14.1; the council confirms it (D20). |
| Supersedes | v6.0 (the 13 Nov 2026 draft, first numbered 5.1), which superseded v5.0, issued 2026-11-09 |
| Owner | Jeffrey Wallk |
| Status | Draft. Issued for review, not yet reviewed by the governance council |
| Companion | [HSGA Explorer](https://claude.ai/artifact/CyyiC8nVMg3oKxdLGduZwK), an interactive walkthrough of this document (to be updated to mirror section 16) |
| Related documents | Semantic Governance Standards Guide v2.4 (6 Nov 2026), including its HR 360 statement of work; SKL as Single Source of Truth, Publishing into Vizier (29 Oct 2026) |
| Review cadence | Proposed: at each delivery gate (G0 21 Dec 2026, G1 8 Mar 2027, G2 3 May 2027, G3 24 May 2027), at each HR 360 MVP1 gate (M1 to M4, section 16.13) and on any change class below |

### Versioning rules

- **Number.** MAJOR.MINOR. A major change alters an invariant, the asset types or tiers, a MUST rule in the naming standard, or the service contract model. A minor change adds or extends a capability without breaking an invariant. Wording and correction fixes do not take a new number; record them in the version history as a revision note.
- **Status.** Draft, In review, Approved, Superseded. Only the council moves a version to Approved.
- **History.** Never edit a past row of the version history. Add a new row at the top.
- **Decisions.** Every open or proposed decision lives in the decision register (section 13). A version is not Approved while a decision it depends on is open.

## 2. Version history

Version 6.1 is the newest row; add each later version above it.

| Version | Date | Class | What changed | Sources |
| --- | --- | --- | --- | --- |
| 6.1 | 2026-11-15 | Minor | Corrects the lineage of the system model: section 5 no longer attributes the tuple to Wymore and names it Model M, a Wymore-derived model (Wallk and Wach, 2026); λ becomes Λ. Adds section 5.4 and Addendum F (lineage, tuple ancestry, mapping to the AI Circuit Breaker, attribution statement, open items), with references at the circuit breaker in 5.2 and at MTBH in 12.1. Adds decision D31. | TB-07b rev 2, Wymore / Control Theory (draft, Nov 2026) |
| 6.0 | 2026-11-15 | Major (proposed; council to confirm) | Renumbers the 13 November draft, first issued as 5.1. Aligning the asset types to six alters invariant 7 and naming rule 2, a major-class change under section 14.1; the owner proposes 6.0 and the council confirms it (D20). No content change from the 5.1 draft. Labels that read "new in 5.1" or "added in version 5.1" in that draft read 6.0 here. | HSGA v5.1 draft PDF (13 Nov 2026); owner decision of 15 Nov 2026 |
| 5.1 | 2026-11-13 | Minor (asset-type alignment: class to be confirmed by the council) | Adds section 16, conversational AI support: the Context Engine as outbound services, the conversation lifecycle, term resolution and disambiguation, consumer personas and entitlements, policy and guardrail enforcement from the SSOT, content and analytics routing, measurement, failure behavior and rollout, with ten diagrams. Adds addenda A to E: service contract, policy model, question corpora and worked examples, crosswalks, glossary. Aligns asset types to six (glossary), the SSOT statement (10.5), Vizier publishing (9.3) and the persona model (8.3A) with the Semantic Governance Guide v2.4 and the SKL as SSOT proposal. Expands RDSG and states the role of the circuit breaker (11.1). Adds three design principles (4.2). Adds decisions D17 to D30 and nine risks, updates D5 and D13, and reconciles the HR 360 MVP1 calendar (13.2, 13.3, 13.4). Uses the spelling Vizier throughout, including in cited titles. | Semantic Governance Guide v2.4 (6 Nov 2026); SKL as SSOT proposal (29 Oct 2026); HR 360 statement of work (1 Nov 2026); owner statements of 13 Nov 2026 |
| 5.0 | 2026-11-09 | Major | Adds the lexicon layer (labels and customer terms in scoped graphs beside the core); five asset types and four tiers; the graph naming standard; tenancy, personas and access decisions; twelve semantic services; operations extensions (screens, monitoring, triage, simulation); the logic single source of truth; a complete one-page architecture diagram and five detailed breakdown diagrams (services, gateway, label resolution, logic pipeline). Core and domain terms keep preferred labels and a vetted universal set only. | Alternate Labels proposal (31 Oct 2026); Graph Naming Standard insert (1 Nov 2026); SSOT Logic Architecture |
| 4.2 | not recorded | Minor | Reference topology and governance diagram edition: all seven holarchy layers, four governance domains, human-in-the-loop diagram set (Section 13 of v4.2). | HSGA v4.2 |
| 4.0 | not recorded | Minor | Reference topology and diagram set introduced. | HSGA v4.2 |
| 3.0 | not recorded | Major | Semantic Abstraction and Mediation Layer: mapping graph as a persistent lateral holon; compiled semantic governance; cross-silo entity and URI resolution; RAG grounding. | HSGA v4.2 |

Versions before 3.0 and the dates of 3.0 to 4.2 are not in the source documents. Fill them in if you hold them.

### Changes in 6.1 that alter earlier statements

- The system model is no longer attributed to Wymore. It is Model M, a Wymore-derived model (Wallk and Wach, 2026), and λ is written Λ (section 5, 5.4 and Addendum F).
- The circuit breaker is stated as the runtime enforcement of R in Model M, and MTBH as a member of R (5.2, 12.1).

### Changes in 6.0 that alter earlier statements

These were drafted as version 5.1 on 13 November 2026.

- The asset types become six: glossary joins vocabulary, taxonomy, ontology, lexicon and mapping, as in the Semantic Governance Guide (invariant 7 in 6.1, 6.2 and naming rule 2 in 6.5).
- Section 10.5 now states, and no longer proposes, that the SSOT and compiled governance are one pipeline.
- Section 9.3: tenant-specific names and terms are customer-tier vocabulary extensions; whether Vizier can display a tenant-specific name is a capability check (W6-01), not a design dependency.
- Section 8.3A adds consumer personas. The operational personas in 8.3 are unchanged.
- Section 4.2 now lists ten design principles, adding three for conversational AI.
- RDSG is expanded as the Requirements Driven Semantic Gateway, and the circuit breaker is positioned as the validator of agent inferences and drafted answers (5.1, 11.1).
- The twelve baseline semantic services are unchanged. The conversation services are specified in section 16 and are not counted among them.
- The spelling Vizier replaces Visier throughout, including in the figures and in cited document titles. This is a revision note, not a design change.

### Changes in 5.0 that alter earlier statements

- Alternate, acronym, persona and hidden labels on core and domain terms are replaced by the vetted universal set; everything else moves to lexicons.
- Persona label graphs become scoped lexicons at the domain, enterprise or customer tier.
- The single-letter asset codes gain L (lexicon) and M (mapping).
- Tenant extensions are customer-tier vocabularies or taxonomies and are never ontologies.

## 3. Purpose and scope

HSGA is a governed layer of shared meaning that sits on top of existing systems, binds what exists to agreed concepts, enforces rules once, and lets AI act within limits that people can audit. It is a semantic scaffold, not a replacement platform.

**In scope**

- The holonic structure and seven-layer holarchy, and the four governance domains.
- The semantic design: core, domain, enterprise and customer assets, with their naming.
- The lexicon layer for alternate labels and customer terminology.
- Tenant isolation, personas, access decisions and provisioning.
- The semantic services and the operations extensions built on them.
- The single source of truth for business logic.
- Runtime governance (gateway, compiled rules, agents) and measurement.
- Conversational AI support: understanding a question, resolving its terms, applying policy, retrieving content and analytics, and checking and tracing the answer (section 16).

**Out of scope**

- Choice of graph store, identity provider, policy engine, telemetry platform and review-application host. The design is stack-independent; GraphDB is assumed only for sizing.
- The persona and job catalog, which Personas & Jobs owns.
- Customer data models in systems of record, which are bound, not changed.
- Transactions: the conversational agent explains and points to where to act; it does not enroll, change elections or move money.
- Individual financial, tax or legal advice. Plan documents, not the SKL, remain the legal source.

**Readers.** Council members and domain stewards read sections 3 to 7 and 13. Engineers read sections 5 to 12. Operations leads read sections 8, 9 and 12. Conversational AI teams read section 16 and its addenda.

## 4. Architecture at a glance

HSGA is additive: new layers of mapping, shared meaning, scoped terminology, governance and delivery sit above the legacy estate, which is bound to concepts rather than replaced.

&#91;embedded content: scaffold over legacy · 4 new layers, 1 existing estate\]

Requests and AI actions pass the gateway, then the services, which are the only route to any graph. The mapping graph ties system fields to concepts without moving data.

### 4.1 Flow

1. **Bind and map.** A mediation holon ties each system field to one agreed concept, with confidence scores and steward confirmation.
2. **Govern core and lexicons.** A small immutable core carries meaning; scoped lexicons and customer extensions carry the many names.
3. **Check at the gateway.** Every request and AI action passes seven stages. A conversational prompt is first anchored to a persona, a job and the concepts it names, and only then retrieved for.
4. **Compile and deliver.** Rules are written once and compiled to data checks, access policy, search filters, agent guardrails and rules-engine artifacts; released vocabularies publish to targets such as Vizier.
5. **Human and measurement spine.** People decide what machines cannot; trust and structure are measured.

### 4.2 Design principles

- Add a layer; do not replace systems of record.
- Keep the core small: onboarding a customer adds no triples to it.
- Scope terminology by where it is stored, one named graph per tenant.
- Author each rule once and generate its runtime forms.
- Machines propose, people decide.
- Measure trust instead of assuming it.
- Reach every graph through a service, never directly.
- Persona selects relevance, never access: entitlements are applied first.
- Degrade, don’t guess: when no governed source supports an answer, ask or return search results.
- Every claim is grounded in a cited, governed source, or it is withheld.

### 4.3 Complete architecture on one page

&#91;embedded content: complete architecture · 6 layers in the request path, 3 cross-cutting spines\]

Read the diagram top to bottom. Sources feed the semantic services, which write scoped graphs into the knowledge graph. Rules live once at L5 and compile to enforcement. The gateway is the single path every request and AI action takes, and only certified output reaches consumers. The human, measurement and tenancy spines apply at every layer. Sections 5 to 12 break each band down; section 16 follows a conversational request through them.

## 5. Holonic structure

A holon is simultaneously a self-contained whole and a composable part; HSGA applies that to seven nested layers that are autonomous in their own scope and accountable to the layer above, following Model M = (X, Y, W, S, Δ, Λ, R), a Wymore-derived system model (Wallk and Wach, 2026; see Addendum F).

&#91;embedded content: seven-layer holarchy · 7 layers, 1 lateral holon\]

Layers 1 to 7 run from operations up to the enterprise ecosystem; the mediation holon is lateral, not an eighth layer.

### 5.1 Layers

| Layer | What it holds | Model M element |
| --- | --- | --- |
| L7 Enterprise ecosystem | Consumers; every output traces to L4 and passes domain certification | Y output space |
| L6 Orchestration and UI | HITL workflows, intervention pane, SHACL viewer, ontology explorer, ontological RBAC | Λ output function |
| L5 Semantic governance | SHACL library, SWRL temporal rules, deontic norms, ORSD-style contracts, KGCL change log | R performance specs |
| L4 Knowledge graph and data fabric | Triplestore with one named graph per asset (domain, lexicon, customer extension, governance), federated query, vector search, lakehouse, metric layer, catalog and lineage | W state space |
| L3 Gateway holon | RDSG (Requirements Driven Semantic Gateway) traversal, AI circuit breaker, policy decision engine, safety specification, rule projection runtime | Δ transition function |
| L2 Digital twin and connectivity | Protocol adapters, twin registry, event streaming, ETL, API gateway, CDC; signals typed as RDF conformant with L5 | S admissible stimuli |
| L1 Physical and operational holons | Equipment, sensors, operational systems; each holon has a digital-twin identity with SHACL-governed state boundaries | X input space |

### 5.2 Four governance domains

They run through every layer: **data** (catalog, lineage, quality gates, master data, access policy), **semantic** (ontology registry, SHACL, term lifecycle, external alignment), **analytics** (model registry, one governed definition per metric, certified dashboards), and **AI and trust** (trust scoring, circuit breaker, model cards, mandatory human gates).

The circuit breaker in the AI and trust domain is the runtime enforcement of R in Model M: it trips when a tolerance in R is breached, so a transition that fails R does not complete. [Addendum F](#msg3g8qr59c.50403) sets out the model, its Wymore lineage and the measure attached to each element.

### 5.3 Mediation holon

The mapping graph is a persistent lateral holon that insulates the top-down ontology from bottom-up implementations: RAG and vector stores, property graphs, dbt and LookML models, third-party ontologies and catalogs. It holds six correspondence types, scores each with confidence, and routes low-confidence mappings to a steward before promotion. It also separates the definition of governance rules from their runtime execution (section 11). Mapping records also bind concepts to Digital Asset descriptions, for content, and to report, field and metric implementation records, for analytics (section 16.9).

### 5.4 Lineage of the system model

Model M is a Wymore-derived system model developed by Wallk and Wach (2026); it is not a tuple Wymore published. Its line of descent runs from Wymore's mathematical theory of systems engineering (1967, 1993), through Zeigler's DEVS, to the SysML modernization by Wach, Salado and Zeigler (2019, 2021).

The new element is R. Wymore keeps performance requirements outside the system model and judges a design against them once, at design time. Model M places R inside the tuple, so a transition completes only if R is satisfied. [Addendum F](#msg3g8qr59c.50403) gives the full lineage, the ancestry of each symbol and the mapping to the AI Circuit Breaker.

## 6. Semantic design and naming standard

Every governed asset is one of six types at one of four tiers, and its name never carries a customer name, an environment, a version or a repository, so graphs can move without being renamed.

### 6.1 Design invariants

1. **Immutable core.** Published core terms are never edited; deprecate with `supersededBy` and replace. Evolution is additive: add a parent, never reparent.
2. **Primitives are rare and rooted.** Minted only at core or a top-level domain, with BFO lineage, kept minimal.
3. **Rooted acyclic derivation DAG.** Multi-parent inheritance is allowed and limited; report any concept with more than two parents.
4. **Three edge types, default deny.** Derivation, correspondence and lexicalization; an allowed-edge matrix by graph pair avoids a fully meshed graph.
5. **Core holds meaning; lexicons hold names.** Core and domain terms keep preferred labels, definitions, relations and a small vetted set of universal alternate labels.
6. **Three orphan checks.** Derivation path to BFO, schema binding coverage, label resolution; run per graph and per release, including each tenant graph.
7. **Six asset types, no modules.** Vocabulary, taxonomy, ontology, lexicon, mapping, glossary. A lexicon holds labels only; a mapping holds match relations between assets; the glossary follows rules GN-15 to GN-19 of the Semantic Governance Guide.
8. **Four tiers with fixed content.** Customer-tier assets are never ontologies; onboarding a customer adds no triples to a core or domain graph.
9. **Scope lives in the graph.** One named graph per tenant; references point one way, from lexicon or extension up to core, by IRI.

### 6.2 Types by tier

| Tier | Allowed types | Holds |
| --- | --- | --- |
| Core | vocabulary, taxonomy, ontology, mapping | Preferred labels, definitions, relations, a small vetted set of universal alternate labels |
| Domain | vocabulary, taxonomy, ontology, lexicon, mapping | The same for one domain, plus labels common to that domain but not universal; operational domains follow this tier |
| Enterprise | vocabulary, taxonomy, lexicon, mapping | House terms valid for every tenant |
| Customer | vocabulary, taxonomy, lexicon, mapping | One tenant's labels and local concepts; never an ontology |

The glossary is allowed at the tiers set by Guide section 3.2 (rules GN-15 to GN-19). The table above is updated when the council confirms them (D20).

### 6.3 Asset names

An asset name is lowercase ASCII words joined by hyphens: `<type>-<tier>-<name>`, or `<type>-customer-<tenant-id>-<name>`. A tenant ID is `t` plus 8 lowercase hex characters, opaque, issued at provisioning and never reused. The name part is proposed at 40 characters or fewer. A customer lexicon may omit the name part, as in `lexicon-customer-t7f3a9c21`.

| Example (illustrative) | What it is |
| --- | --- |
| `vocabulary-core-party` | A core vocabulary |
| `taxonomy-domain-workforce-advisory` | A domain taxonomy |
| `ontology-domain-payroll-operations` | An operational-domain ontology |
| `lexicon-enterprise-insperity` | Insperity house terms |
| `lexicon-customer-t7f3a9c21` | One tenant's labels |
| `mapping-customer-t7f3a9c21-plan-names-to-benefit-classes` | One tenant's match relations to domain concepts |

### 6.4 Graph classes and IRIs

Every graph IRI derives from the asset URI, which is version-free and ends in the asset name. The path segments `draft`, `sim`, `changes` and `catalog` are reserved; a version segment always starts with a digit, so they cannot collide.

| Graph class | IRI | Lifetime |
| --- | --- | --- |
| Current release | Asset URI | Replaced by each release |
| Version | Asset URI + `/` + SemVer | Permanent |
| Draft | Asset URI + `/draft/` + change ID | Deleted after release or rejection |
| Simulation | Asset URI + `/sim/` + run ID | Deleted when the run record is closed; never writes to a current or version graph |
| Change records | Asset URI + `/changes` | Permanent, append-only |
| Catalog | Base URL + `/catalog` | Permanent |

Repository IDs are environment-neutral: `skl-core-domain`, `skl-lexicons`, `skl-extensions`, and `skl-tenant-` plus the tenant ID for a dedicated repository. The environment belongs to the server address. Moving an asset between repositories changes only its catalog record.

### 6.5 Naming rules

| # | Rule | Strength |
| --- | --- | --- |
| 1 | Lowercase ASCII letters, digits and hyphens; standard or customer form | MUST |
| 2 | Type is one of the six; the word "module" is not used | MUST |
| 3 | Core assets hold no customer-specific or enterprise-specific content | MUST NOT |
| 4 | No customer name, environment, version, date, status or repository name in a name | MUST NOT |
| 5 | A published name never changes; a rename is a new asset with the old one retired and its replacement recorded | MUST NOT |
| 6 | Current-release IRI equals the asset URI; archived releases use version IRIs | MUST |
| 7 | Tenant ID is opaque, issued once, never reused | MUST |
| 8 | Services derive reachable graphs from caller tenant and persona; no graph IRI is accepted from a caller or screen | MUST |
| 9 | A lexicon declares the assets it labels; labels point to concepts by IRI and never copy them | MUST |
| 10 | A domain asset declares its parent core assets in metadata; parentage is not in the name | SHOULD |
| 11 | Operational domains follow the domain tier; the first word of the name is the domain | MUST |
| 12 | A draft graph is deleted when its change is released or rejected | MUST |
| 13 | Prefixes are lowercase and unique across repositories; a customer-tier prefix begins with the tenant ID | MUST / SHOULD |

The Metadata Standard changes in five places: term labels, asset types, new fields (tier, tenant ID, labelled assets, mapping source and target), the catalog record, and the glossary (add lexicon, mapping, tier, tenant ID, draft graph; codes L and M).

## 7. Lexicon layer and customer terminology

Alternate labels and customer terms are held in scoped lexicons and customer extension vocabularies beside the core, so onboarding a customer adds no triples to the core, a label change never forces a core release, and one customer's terms never reach another.

### 7.1 Why labels do not live on the core

Putting every synonym on the core concept fails five ways: the core grows with every customer (growth); every label change needs a core release (churn); one customer's terms become visible to all (leakage); a flat list cannot say that the same word means different things to different customers (ambiguity); and a bare label records no source, approver or dates (lost evidence). Some terms are not synonyms at all and need a home that does not widen the core.

| Option | Core size and speed | Tenant confidentiality | New customer meaning | Verdict |
| --- | --- | --- | --- | --- |
| A. Labels on core concepts | Weak: grows with every customer | Weak: all tenants see all labels | Weak | Reject for customer labels; keep for a small vetted promoted set |
| B. Scoped lexicons | Strong: core unchanged | Strong: scope is the graph | Weak: names existing concepts only | Adopt for label-only terms |
| C. Customer extension vocabularies | Strong: core unchanged | Strong | Strong | Adopt for new local concepts |
| D. A copy of the core per customer | Weak: copies multiply | Strong | Partial | Reject: copies drift |

B and C together, chosen by the triage rule, are the decision. B costs a resolution service and a derived index; C costs steward review of each match. Both are paid once per platform or once per concept.

### 7.2 Principles

1. The core holds meaning, not vocabulary variety.
2. A label is a record, not a property.
3. Scope is enforced by where a label lives.
4. References point one way, by ID; nothing is copied into the core.
5. Machines propose, people decide.
6. Derived is not source: the resolution index is rebuilt, never edited.
7. Every change is traceable to source, evidence, reviewer, release and publish record.
8. One contract per function, an adapter per source or target.
9. No direct access to a graph; every read and write goes through a service or a provisioned screen.

### 7.3 The label record

A label is a resource modeled in the style of SKOS-XL, with PROV-O provenance and SHACL shapes validating each record.

| Field | Holds |
| --- | --- |
| Label text and language | The literal form |
| Concept | ID of the core, domain or extension concept it names |
| Type | Alternate, hidden (match only, never shown), abbreviation, misspelling or deprecated |
| Scope and tenant | Customer, Insperity or domain; tenant ID for customer labels |
| Evidence | Source, document or page, span, frequency |
| Confidence and triage class | Machine score and proposed class |
| Status | Proposed, in review, approved, published, rejected or deprecated |
| Reviewer and time | Who decided, when and why |
| Effective dates and release | When it applies and the SKL release that carried it |

### 7.4 Matching and match relations

Matching runs lexical first against preferred and approved labels after normalization, then embedding-assisted similarity with a confidence score. A customer concept links to the nearest core or domain concept by exactly one of four relations: **exact**, **close**, **broad** (core concept is wider) or **narrow** (core concept is more specific). A synonym, abbreviation or misspelling is never a match relation; it is a label. Match relations are re-checked on every core release.

Four cases are flagged and never resolved automatically: the same label points to different concepts in one scope; a label equals another concept's preferred label; the same label means different things in two tenants (both stay scoped, and reviewers see the pair as evidence); a candidate has no close match.

An acronym carries a resolution scope and has no global value. An unscoped acronym returns every candidate. Conversation behavior for the four flagged cases is in section 16.6.

### 7.5 Triage

| If the term is | It goes to | Approved by |
| --- | --- | --- |
| The same meaning as an existing concept (synonym, abbreviation, plural, locale variant, misspelling) | A label record in the narrowest lexicon in which it is true | Ops reviewer |
| A homonym in this scope | Stays scoped, conflict flagged, disambiguation note | Domain steward |
| A new concept used by this customer only | The customer extension vocabulary, with a match relation | Domain steward |
| A new concept of general value, or a label seen across several customers or in regulation | A core or domain change request through the normal lifecycle | Governance council |
| Noise, out of scope, or personal data | Rejected with a reason; evidence kept | Ops reviewer |

### 7.6 Label lifecycle, promotion and releases

A label starts Proposed, moves to In review, then Approved or Rejected. An approved label becomes Published only through a release; a published label can later be Deprecated. Every transition records who, when and why. A label that recurs across customers or appears in regulation can be promoted to a domain or core vocabulary as a universal alternate label by council decision and ships in a core release; a promoted label that later conflicts is demoted the same way. Lexicon changes release on their own cadence per scope; a lexicon release never changes the core version.

### 7.7 Resolution

Callers pass text and a tenant context. The label resolution service looks first in that customer's lexicon, then the Insperity lexicon, then the domain lexicon, then core preferred labels. It never searches another tenant's graphs, matches hidden labels without displaying them, and returns candidates with definitions when several concepts match at the same level. It answers from a derived index rebuilt on each release, not from the ontology graphs. In a conversation, the Context Engine calls this service (section 16.6).

&#91;embedded content: label resolution · 4 levels, 1 derived index\]

The service stops at the first level that hits. The dashed box is outside its reach by design.

## 8. Tenancy, personas and access

Each customer has its own named graphs, no repository is ever exposed, and what a person may do is decided from persona, job step, resource and context rather than a permission list.

### 8.1 Repositories and topology

Assuming GraphDB, one server per environment (dev, test, stage, prod) hosts a few repositories, split by reasoning and release cadence, not by tenant.

| Repository | Holds | Reasoning | Why separate |
| --- | --- | --- | --- |
| `skl-core-domain` | Core, domain and operational-domain vocabularies, taxonomies, ontologies and mapping graphs, one named graph per asset | On | Released and reasoned together |
| `skl-lexicons` | Insperity lexicon and one named graph per tenant lexicon | Off or minimal | Labels stay out of reasoning and core releases |
| `skl-extensions` | Local concepts and match relations, one named graph per tenant | Light | Own release and deletion per tenant |

The raw landing zone, candidate store and resolution index need not live in GraphDB. The core and domain repository is the same in every stage of growth; growth happens in the lexicon and extension repositories. Only where a customer contract or blast radius requires does a tenant move to a dedicated repository or server (`skl-tenant-` plus the tenant ID), and the move changes only its catalog record.

### 8.2 Isolation and privacy

1. **No direct access.** No repository is exposed to people, other systems or third parties. The store workbench and admin accounts are closed to normal use; break-glass access is time-bound and logged.
2. **Tenant tag from the first byte.** Every item carries a tenant ID from landing, and every query a tenant context.
3. **Isolation enforced by services.** Each tenant lexicon and extension vocabulary is its own named graph; services build the graph restriction into every query, accept no raw queries, and use separate read and write accounts. Store-level graph controls are a second layer.
4. **No cross-tenant path.** The one exception is promotion counting: reviewers see a count, never another tenant's evidence.
5. **Fail-closed screening.** Personal and sensitive content is detected, redacted or quarantined before extraction; a red-team set tests it before the pilot gate.
6. **Audit and exit.** Every read and write is logged. Offboarding removes the landing zone, graphs and index entries with no change to the core.

Written permission to use each customer's documents and feeds, a retention rule and data-use terms are conditions of onboarding.

### 8.3 Operational personas (proposed)

The persona and job catalog is owned by Personas & Jobs, which will supply fine-grained identity and access controls beyond traditional ACLs.

| Persona | Jobs | Works on |
| --- | --- | --- |
| Tenant provisioner | Create, suspend, remove a tenant; rotate service credentials | Tenant records and graphs, never content |
| Onboarding lead | Register sources, confirm data permission, run onboarding | One tenant's sources and ingest reports |
| Ops reviewer | Decide candidates, edit labels, raise escalations | Candidates and labels for assigned tenants |
| Domain steward | Approve match relations and local concepts; maintain vocabularies, taxonomies, mappings | Assets in the domains they steward |
| Ontologist | Propose changes to ontologies, triage rules, naming | Ontology assets, through the lifecycle |
| Platform operator | Run pipelines, releases, rollback, drift response | Services and releases, never content |
| Council member | Approve releases, label promotion, cross-domain conflicts | Release and promotion decisions |
| Auditor | Read the audit trail and decision records | Records only |

### 8.3A Consumer personas

People who put questions to conversational AI are modeled as individuals of `core:persona`. A persona is set from the authenticated role and never from the prompt. It selects relevance, labels, tone and prompt template, and it never grants access. A persona label never encodes a protected attribute. Twelve consumer personas are defined for the HR 360 agent (section 16.7). The Compass seller personas (BPA, BPC, BSA) and the customer personas of the PEO service map are cross-walked to this registry (D19).

### 8.4 How access is decided

Each request carries the person's persona assignments; the job and job step being performed; the resource (graph class, tenant, domain, item state); and the context (assignment, time). The service decides from rules authored in the SKL as governed rules, and logs the decision with the persona, job and step that authorized it. Rules a permission list cannot express:

- A reviewer decides only items assigned to them, in tenants they are provisioned for, while the item is In review.
- Nobody approves their own change; the proposing persona cannot be the approving one.
- The approval power of a steward ends at the domains they steward.
- A person with two personas has each persona's rights only while doing that persona's jobs.
- Elevated access is time-bound, logged and reviewed.

Entitlement filtering precedes search and ranking, and a persona tailors relevance and never widens access. An example scope rule: an employee sees only their own elections, and a client administrator only their worksite (rule R-13).

### 8.5 Provisioning

Provisioning is a persona job through the same screens and audit. **Tenant:** register; create lexicon and extension graphs, indexes and review queue; bind policies and persona assignments; confirm written data permission; activate. Deprovisioning reverses each step. **Person:** assign personas with tenant and domain scope and an end date; complete training and calibration; activate. Assignments are reassessed periodically and revoked at once for movers and leavers.

## 9. Semantic services and operations extensions

Five functions (capture, warehouse, map, manage, serve) are delivered by twelve semantic services; every graph is reached only through them, and screens, dashboards and later projects are built on their contracts.

### 9.1 The services

| Group | Service | Responsibility |
| --- | --- | --- |
| Inbound | Ingestion | Lands each item with tenant tag, provenance and change capture, one connector per source type |
| Inbound | Extraction | Recovers text, structure and language; OCR for scans |
| Inbound | Screening | Detects personal and sensitive content before any other step; fails closed |
| Processing | Candidates | Extracts terms, defined terms and drafted definitions with evidence; normalizes and merges variants |
| Processing | Matching and triage | Matches candidates to concepts, proposes match relations, classifies each as label, local concept, core request or rejection |
| Processing | Lexicon | Writes label records and extension vocabularies to scoped graphs; validates shapes; detects conflicts |
| Processing | Review | Lifecycle state machine, assignments, decisions, audit trail |
| Processing | Release | Validation, versioned releases, promotion and rollback across environments; records changes as triples |
| Outbound | Label resolution | Tenant-scoped lookups from the derived index |
| Outbound | Publishing | Projects, validates, delivers and reconciles releases to targets through adapters |
| Common | Policy decision | Decides each request from persona, job step, resource and context |
| Common | Telemetry | Receives events from every service for monitoring, triage and simulation |

Every service shares five rules: each request carries caller identity and tenant context; a policy decision is logged before any read or write; graph access is parameterized and no service accepts a raw query; each service emits events for request, decision, outcome and duration; the contract is versioned and changing it is a governed change.

**Conversation services.** Conversational AI is delivered by a family of outbound services specified in section 16.5: eight context services (resolve-persona, classify-intent, reverse-engineer-prompt, map-to-holons, map-to-jobs, score-relevancy, assemble-context, rank-context) and the answer services that draft, ground, check and record an answer. They reach graphs only through the services in this section, follow the same five rules, and are not counted among the twelve baseline services.

&#91;embedded content: semantic services · 12 services in 4 groups\]

Items move left to right: inbound services land and screen, processing services turn candidates into released vocabulary, and outbound services serve and publish it. The two common services sit under every group.

### 9.2 Capture and warehouse

Four source types are in scope: customer documentation (upload or file share), the content management system (API or export, incremental), customer data feeds (file, SFTP or API with declarative R2RML-style mappings) and employee handbooks (section-aware parsing, OCR). Each passes five steps: **land** (tenant tag, source, version, hash), **screen** (fails closed; unclear items quarantined), **extract**, **propose** (a definition is drafted only when a source span supports it), **normalize**. Only the candidate record, with text, evidence span, source, tenant, frequency and confidence, leaves capture.

The warehouse keeps each store separate: raw landing (per tenant, never loaded into a graph), candidate store (working data, never released), core and domain graphs (versioned releases), Insperity lexicon, customer lexicons and customer extensions (own version per tenant), resolution index (disposable, rebuilt on release), and change records (append-only triples).

### 9.3 Publishing to targets

Publishing follows the SKL contract: publish, validate, reconcile, status and rollback, one adapter per target. For Vizier, released vocabularies and taxonomies publish as dimension members and property values, each stamped with its SKL ID and version; synonyms and definitions stay in the SKL. Vizier consumes and never edits; any difference on read-back is drift, corrected in the SKL. Rules, constraints and deontic norms are not published; they run in deterministic services and their results can be loaded as data. A metric is held in the SKL as a symbolic, tool-neutral definition with test cases and in Vizier as an executable implementation; parity tests run on every release and block a publish on failure, and where the definition and an implementation disagree the definition is correct. What Vizier cannot express is reported as untranslatable and is not approximated. Tenant-specific names and terms are authored as customer-tier vocabulary extensions (section 7).

The display-label rule (each member shows the tenant’s approved label where one exists, otherwise the preferred label) is proposed for confirmation. Whether Vizier can display a tenant-specific name for a published member is a capability to confirm; task W6-01 asks Vizier, and if the answer is no the preferred label is published and customer terms resolve in the Context Engine, Compass and search. Vizier limits come from public documentation and should be checked against the tenant.

### 9.4 Operations extensions

These are built on the service contracts, add no route to a graph, and can change without changing the baseline.

| Extension | What it adds | Calls | Used by |
| --- | --- | --- | --- |
| Review and maintenance screens | Governed data entry for labels, local concepts, vocabularies, taxonomies, ontologies, mappings | Review, Lexicon, Release, Policy decision | Ops reviewers, stewards, ontologists |
| Provisioning | Tenant and person lifecycles, persona assignment, recertification | Policy decision, Lexicon, Telemetry | Tenant provisioner, onboarding lead |
| Monitoring dashboards | Pipeline, processing quality, review work, service health, access and security, releases, capacity | Telemetry | Platform operators, ops review lead, auditors, council |
| Triage | One queue of alerts and exceptions with severity, owner and runbook | Telemetry, Review | Platform operators, ops review lead |
| Simulation | What-if runs showing the impact of a change before it is made | Release, Matching, Publishing, Telemetry | Stewards, ontologists, council, program manager |

The review screens are the candidate queue, evidence viewer, concept picker, alternate-label editor, conflict panel, local-concept creator, lexicon browser, escalation and promotion inbox, and reviewer dashboard. Dashboards read telemetry, never the graphs. Operational triage (failed ingests, quarantines, drift, parity failures, repeated denials, expiring assignments, service-level breaches) is separate from candidate triage in Manage.

Simulation loads a proposed change into a draft graph and compares it with the current release without publishing. Workspaces use the reserved `sim` segment. The impact view shows concepts, labels, mappings and tenants affected, the objects that would change in each target, new conflicts, reviewer workload, and for capacity runs the predicted load, reasoning and lookup time. Candidate simulations: a core or domain release, label promotion or demotion, a changed match relation, an access rule, a new tenant or volume growth, and a Vizier projection as a dry run.

## 10. Logic single source of truth

Business logic is defined once in a declarative spec under version control, compiled into what each runtime needs, and reached through one Decision API, so rules cannot drift between code, rules engines and ontologies.

The problem has three compounding forms: duplication (the same eligibility rule in a stored procedure, a Drools ruleset and a service-layer condition), silent drift (an incident fix applied in one place only) and no audit trail (rules edited directly in production with no review). Forcing everything into one tool fails, because procedural algorithms do not belong in a rules engine and stateful workflows do not belong in an ontology.

### 10.1 Right home by layer

| Category | Question it answers | Home | Example |
| --- | --- | --- | --- |
| Constraints | What must always be true about the domain data? | Ontologies (OWL/RDF), schemas (JSON Schema, OpenAPI, Pydantic, Protobuf) | An order has at least one line item and the customer exists |
| Business rules | What actions or decisions follow from state? | Rules engines (Drools, Camunda, DMN) or a DSL | Gold tier and order over $100 gets 15% off |
| Computation | How is state computed or processed in sequence? | Code: microservices, DDD domain services | Route optimization, a multi-step feature pipeline |

The HR 360 statement of work uses four item types in the SSOT: constraints (C), rules (R), calculations (K) and logic (L). Values that change by year or by plan, such as limits, match formulas, waiting periods and vesting schedules, are versioned parameters with an effective period and a source citation; none is typed into a prompt or into code.

### 10.2 Governance pipeline

Specs live in a central repository in human-readable form (YAML, DMN, Turtle/OWL). Nobody edits a rule in a rules-engine screen or a production database; everything is committed first and reaches production only through CI. CI runs semantic reasoners (for example HermiT) for contradictory axioms and static analysis for malformed or conflicting DMN tables, then scenario tests against synthetic datasets. Rule sets and schemas carry semantic versions, and each consuming service declares the version it depends on, so a change cannot silently break a consumer. Rejected changes return to the author.

### 10.3 Generated executables and the Decision API

On every merge, code generators produce TypeScript and Python interfaces for microservices, SHACL/OWL files for the graph store, and DMN/Drools XML for the rules engine, all from the same spec. Drift becomes a build failure, not a production incident.

At run time callers do not reach the rules engine, ontology store or a legacy procedure directly. They call the Decision API, which resolves the caller's declared policy version, validates the request against the current schema, and routes to whichever backend owns the decision, including a wrapped legacy engine not yet migrated.

&#91;embedded content: logic single source of truth · spec to Decision API\]

Only the spec repository is edited by people. Everything below it is generated or routed, and the dashed box is the legacy engine that the strangler-fig migration retires.

### 10.4 Migration

1. **Discover and classify.** Inventory and audit with tracing and static analysis; log every point where a business decision is made; sort each into constraint, rule or computation.
2. **Decouple behind the API (strangler fig).** Wrap legacy engines and stored procedures behind the Decision API before touching internals; extract hardcoded logic into configuration or DMN piece by piece, re-pointing the facade as each piece lands.
3. **Schemas first, rules second.** Unify data definitions through a common ontology or schema registry, then consolidate rules; many apparent rule conflicts are data-shape conflicts.

Start with the repository and CI pipeline before extracting any rule; pilot on one bounded decision such as discount eligibility; run Phase 1 broadly before committing to Phase 2; make version declaration mandatory from day one.

### 10.5 Relation to compiled governance

Governance rules, constraints, logic and calculations are defined once in the SSOT and published for downstream execution. Each is tied to the policies, standards, disciplines, regulations and contractual obligations that require it, and to the legal concerns for privacy, disclosure, confidentiality and sensitivity that bound it. Compiled governance (section 11.2) is the mechanism that executes them: the same definition is compiled to data checks, access policy, search filters, agent guardrails and rules-engine artifacts.

## 11. Runtime governance

Every request and AI action takes the same seven-stage path through the gateway, rules are compiled once to where they are enforced, and agents do the continuous watching while people hold the decisions that carry judgment or risk.

### 11.1 Gateway stages (RDSG)

| Stage | Name | What it does | Human part |
| --- | --- | --- | --- |
| 0 | RCB | Assembles the Requirement Context Bundle: who, what, when, where, why; activates domain holons |  |
| 1 | SHACL | Checks structure; 212+ shapes; critical violations halt and route to the Domain Governance Team |  |
| 2 | SWRL | Checks validity in time with 96+ temporal rules, so expired constraints are never applied |  |
| 3 | PEP | Checks the four governance domains permit it for this person and purpose; cross-jurisdiction conflicts go to the Enterprise Governance Council | Yes |
| 4 | UCA | Holds unsafe or irreversible actions at the Simplex Action Gateway for human authorization | Yes |
| 5 | Directive | Issues a compiled AI Directive carrying guardrails |  |
| 6 | Facade | Checks acceptance criteria, applies the five-dimension trust score, commits the audit record to the Governance Named Graph, quarantines tripped outputs | Yes |

&#91;embedded content: gateway traversal · 7 stages, 3 with a human part\]

Stages run in order. A critical failure at stage 1 stops the request, and the three highlighted stages need a person.

RDSG is the Requirements Driven Semantic Gateway. It applies personas, jobs and outcomes to an issue or opportunity with a product, service or process, so that domain-specific features and sub-features can be generated to address value gaps between desired outcomes and delivered outcomes.

Conversational requests take the same traversal. The Context Engine supplies the persona, job, outcome and holon context that stage 0 needs (proposed, D17). The AI circuit breaker validates inferences made by agents that support the gateway, including the answers conversational agents draft, and returns PASS, COMPLY, FREEZE or HALT. Section 16.8 specifies the interface.

### 11.2 Compiled governance

Rules are authored once as SHACL shapes, SWRL rules and LKIF-style deontic norms (obligation, permission, prohibition), harmonized by the Rule Harmonization Engine into one conflict-checked contract. The Rule Projection Agent compiles them to runtime targets (SQL CHECK constraints and dbt tests, OPA policies, vector-store filters, agent guardrails), versions each artifact with a KGCL record, and keeps a compiled policy registry and cache so the graph reasoner stays off the request path. Roles come from ontological definitions, not hand-edited permission lists.

### 11.3 Agents and loop

Eight agents operate: lineage ingestion, mapping confidence, rule projection, ontology alignment (HITL-gated), drift detection, RAG grounding, compliance monitoring (HITL-gated) and recursive learning (HITL-gated). The loop is Observe, Reason, Propose, HITL review, Adapt. Agents never write governed graphs directly. The RAG grounding agent corresponds to the guide’s grounding-agent (confirm, D24). The outbound agents for conversations are listed in section 16.5.

### 11.4 Human checkpoints

| Checkpoint | Decided by |
| --- | --- |
| Ontology change | Domain Architect with the Council |
| Weak mapping below threshold | Knowledge or Data Steward |
| Rule conflict across jurisdictions | Enterprise Governance Council |
| Irreversible action | Safety Reviewer |
| Low-trust output (quarantined) | Domain Governance Team |
| Candidate term (label or reject) | Ops reviewer |
| Match relation or local concept | Domain steward |
| Label promotion, core request, cross-domain conflict | Governance council |
| Advice-seeking question | Rule R-11, no person: information plus a referral |
| Legal interpretation, dispute or personal financial hardship | Rule R-12 routes the question to a person |
| Answer held at FREEZE | Trustee |
| User flags an answer or corrects it | Review queue, then the domain steward; nothing is learned without approval |
| Low-confidence queue | Ops reviewer |

In the lexicon layer, extraction and matching propose and reviewers decide: the same rule that governs the eight agents. Persona names are illustrative; role definitions, not individuals, carry authority.

## 12. Measurement and assurance

Trust is measured, not assumed: MTBH gates AI actions, structural measures show whether the semantic design stays disciplined, and lexicon-layer targets prove the core stays small and tenants stay isolated.

### 12.1 MTBH

Mean Time Between Hallucinations is total operational time divided by verified hallucinations or breaker trips: MTBH = T\_ops / N\_h, as defined in the metrics registry of the AI Circuit Breaker v3.0 design. Track it under statistical process control; a falling MTBH is an early warning that the system is outside its validated envelope. The baseline uses 32 measures, a 150-question gold set baselined at Gate 1, and SPC monitoring on MTBH. The 32 measures are the 14 design-time and 18 run-time measures of the HR 360 metrology; whether the gold set is the HR 360 set or a broader one is open (D23).

MTBH is one member of R, the performance specification set of Model M, alongside the breaker's other tolerances. [Addendum F](#msg3g8qr59c.50403) lists each tolerance against the element of the model it measures, which is what ties a breaker trip to a stated requirement instead of a judgment call.

### 12.2 Structural measures

Dashboards read telemetry only, so each measure is emitted as a telemetry event by the check that computes it.

| Measure | What it shows |
| --- | --- |
| Correspondence density | Lateral links per concept; too dense drifts toward a meshed graph, too sparse means fragmentation |
| Stem-reuse ratio | Share of new terms built from existing stems |
| Impact radius | Terms affected by a core change, before approval |
| Polyhierarchy rate | Concepts with more than one parent; reported above two |
| Domain-minted primitive share | Primitives minted outside core; should stay minimal |
| Promotion-backlog age | How long pending terms wait; long waits mean HITL capacity is the bottleneck |
| HITL disposition mix | Label, domain concept, core change, reject; a shifting mix suggests gaps |
| Orphan rate per graph | Local concepts with no derivation path; target 0, checked in every tenant graph |

### 12.3 Lexicon-layer targets

The claims are unproven until measured. Spike W2-02 builds a synthetic core and holds the same labels two ways, in the core and in scoped lexicons, measuring load, reasoning and query time, index size and release size at rising label and tenant volumes. Pass thresholds are agreed first (W1-04) so the result cannot move them; scale test W7-03 repeats it on the built system. Customer counts and labels per customer are not yet known, so the decision record states the synthetic parameters.

| Measure | Target | Tested in |
| --- | --- | --- |
| Customer-driven triples added to the core per onboarding | 0 | Lexicon builder; second-customer onboarding |
| Core load and reasoning time at top test volume | Within a tolerance set before the spike | W2-02, W7-03 |
| P95 label lookup time | Threshold set from the spike | W2-02; Label Resolution Service |
| Cross-tenant label results | 0 | Isolation tests |
| Core releases triggered by a label change | None | Release pipeline |
| Label records with source, reviewer and release | 100% | Review service |

Also reported per customer and per release: lead time from first source to approved lexicon; candidates decided per reviewer-hour and age of the oldest open item; precision and recall of extraction, matching and triage on the gold set with reviewer agreement; drift incidents per release and parity failures caught before publish. Review service levels are set from the pilot, not guessed.

### 12.4 Lifecycle fit

HSGA governs the information baseline across the systems-engineering V-model, from stakeholder needs through operations, so requirements, architecture and design items are machine-checked early and monitored after fielding. Mapped from ISO/IEC 15288, the INCOSE SE Handbook and DoD AAF; artifact IDs are in v4.2.

### 12.5 Conversation measures

Conversational AI adds run-time measures for answer traceability, grounded claims, hallucination rate, MTBH, circuit breaker trips, accuracy on the gold set, rule-version correctness, policy compliance, entitlement violations and latency, and design-time measures such as persona label coverage. They are listed with their targets in section 16.10. Each is an individual of the measure model computed from triples or event topics, and a changed formula is a new version, not a silent edit.

## 13. Roadmap, decisions and risks

Delivery is phased and gated by measured evidence; three lexicon-layer decisions await council approval and the register below holds everything else open.

### 13.1 Programme phases

| Phase | Focus | Exit evidence |
| --- | --- | --- |
| 1. Seed and baseline | Seed core from standards, 50+ shapes, charter the council, set trust baselines, stand up model registry | Gate 1 baseline: 150-question gold set; structural measures emitting telemetry |
| 2. Extend and certify | Cross-domain extensions, 200+ shapes, external alignments, certification, ontology-driven access | Per-tenant graphs onboarded; 100% HITL compliance |
| 3. Scale and self-serve | SHACL compliance above 99%, self-service extension toolkit, full deontic library, continuous trust monitoring | Anti-collapse protocol validated |

### 13.2 Semantic services pilot and gates

The pilot uses one customer, one instance of each of the four source types, the downturn workforce advisory vocabularies from the SKL proposal, and Vizier as first target. Planning dates assume a 9 November 2026 start and a pause from 21 December to 3 January.

| Gate | Planning date | What is true when it passes |
| --- | --- | --- |
| G0 | 21 Dec 2026 | Label architecture decided on benchmark evidence; council seated; naming, ID and multi-parent rules agreed; inbound, processing and publishing contracts published; pilot customer, stewards and data permission confirmed |
| G1 | 8 Mar 2027 | All four source types ingested with provenance on every record; no personal-data leaks in the red team; candidates triaged into scoped lexicons; zero customer-driven triples in the core; zero cross-tenant results |
| G2 | 3 May 2027 | Pilot vocabularies live in Vizier in one version with parity and reconcile checks clean; pilot customer lexicon reviewed by operations and published for its tenant |
| G3 | 24 May 2027 | Scale test passed; second customer onboarded from the playbook with no change to the core; second target live; runbooks drilled |

**HR 360 MVP1 track.** A second track runs in parallel: the 12-week HR 360 statement of work, from Monday 2 November 2026 to Friday 22 January 2027, which puts a governed SKL under the HR 360 agent starting with Employee Benefits and Retirement Sponsorship. Its gates are renamed M1 to M4 here so that they do not collide with G0 to G3. Week 9 ends on 1 January 2027, inside the pause above, so either the pause excludes MVP1 or M3 moves (D21). The relationship between the two pilots is D22.

| Gate | Week | Date | Passes when |
| --- | --- | --- | --- |
| M1 Baseline (SOW G1) | 2 | 13 Nov 2026 | Deliverables 1 to 3 approved; targets confirmed against the baseline |
| M2 Keel released (SOW G2) | 6 | 11 Dec 2026 | Keel released through the pipeline; DT-02 at 80% or higher, DT-03, DT-05 and DT-08 at 100% |
| M3 Services live in test (SOW G3) | 9 | 1 Jan 2027 | HR 360 answers gold-set questions end to end through the SKL; RT-01 at 100% in test; measures reporting |
| M4 Proof of capability (SOW G4) | 12 | 22 Jan 2027 | Five scripted scenarios pass live; the after report shows the targets met or explains each gap; MVP2 recommendation delivered |

### 13.3 Decision register

Change the status with the dropdown and record the version in which it changed.

| ID | Decision | Status | Note |
| --- | --- | --- | --- |
| D1 | Primitives need BFO lineage, minimal, top-level domains only | Decided | Reflected in invariants |
| D2 | Labels and tenant concepts live in separate graphs, never in core or domain ontologies | Decided | Refined by the lexicon layer |
| D3 | MTBH is defined by the AI Circuit Breaker v3.0 metrics registry | Decided |  |
| D4 | Nested-domain primitive minting: do area containers count as top level? | Open |  |
| D5 | Persona search ranking wording must match graph-scoped resolution | Open | Sections 16.6 and 16.7 specify both; propose closing on adoption |
| D6 | Simulation sequencing against the roadmap, and which simulation is built first | Open | Label promotion, core release, Vizier projection or capacity planning |
| D7 | Council approver role, and who approves a customer term that maps to nothing in the core | Open | Listed open in one section, defined in the roles table |
| D8 | Monitoring pattern: dashboards read telemetry only, but the guide reads model files | Open |  |
| D9 | Adopt the lexicon-layer pattern (scoped lexicons, extension vocabularies, derived index) | Proposed | Decision requested |
| D10 | Adopt the five-function service model as baseline for every customer | Proposed | Decision requested |
| D11 | Run benchmark spike W2-02 before build, thresholds set first in W1-04 | Proposed | Decision requested |
| D12 | Tenant ID format (t plus 8 hex) and name length limit (40 proposed) | Open |  |
| D13 | Persona-specific labels: stay on terms when true for every tenant, move to a lexicon otherwise? | Open | The HR 360 vocabularies hold persona labels (401k match, QLE) and measure their coverage (DT-11); keep open until the council decides where they live |
| D14 | May an ontology exist at the enterprise tier? | Open |  |
| D15 | One catalog graph, or one per repository? | Open |  |
| D16 | URI path pattern for lexicon and mapping assets | Open |  |

**Added in versions 6.0 and 6.1.** D17 to D30 were added in version 6.0 (drafted as 5.1); D31 in 6.1.

| ID | Decision | Status | Note |
| --- | --- | --- | --- |
| D17 | Confirm the gateway interface: the AI circuit breaker validates agent inferences and conversational answers; the Context Engine supplies stage 0 context for conversational requests | Open | Owner’s RDSG description; Section 16.8 |
| D18 | Adopt the Contextual Relevancy family as the Context Engine, not a new baseline service | Proposed | Decision requested |
| D19 | One consumer persona registry in core:persona with a crosswalk from Compass BPA, BPC, BSA and the PEO service-map personas | Open | Owner: Personas and Jobs |
| D20 | Asset types: six, adding glossary; council classifies the change (alignment or Major) | Proposed | Guide GN-2. The owner proposes Major, hence 6.0 |
| D21 | Calendar alignment: rename SOW gates M1 to M4; cover for SOW Week 9 inside the 21 Dec to 3 Jan pause | Open | Section 16.13 |
| D22 | Relationship between the HR 360 MVP1 track and the v5.0 services pilot | Open | Two tracks, shared services |
| D23 | Gold set: one set or two; add content and analytics strata | Open | Addendum C |
| D24 | One name and function for the answer check: audit-answer, grounding-agent, RAG grounding | Open | Addendum A |
| D25 | Author and publish rule PC-1 for protected characteristics in analytics in the SSOT | Open | Compliance steward; Section 16.8 |
| D26 | Author and publish rule SG-1 for small-group suppression: threshold and scope | Open | Evidence: CQ-154 |
| D27 | Vee pattern: B now, C as target, A only if Vee supports it | Open | Needs Vizier input |
| D28 | Analytics binding: report, field and metric implementation records in the mapping graph; allowed edge pair under invariant 4 | Proposed | Section 16.9 |
| D29 | Clarification policy: tolerance values, maximum clarifications and options offered; calibrate in shadow mode | Open | Section 16.5 |
| D30 | Consumer-facing text and the responsible actor for COMPLY, FREEZE and HALT | Open | Section 16.8 |
| D31 | Adopt the Model M lineage and attribution of Addendum F in place of "Wymore defines", in this document and every submission | Proposed | Added in 6.1; awaits confirmation of the F.7 open items with Paul Wach |

**Update to W6-01.** Whether Vizier can hold a tenant-specific name becomes a capability check. Tenant terms are authored as customer-tier extensions (section 9.3).

### 13.4 Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Lexicon layer adds a run-time lookup the core did not need | Derived index; P95 threshold set before the spike; spike and scale test |
| Extraction floods reviewers with low-value candidates | Confidence floors, de-duplication, gold set, triage precision target, bulk actions |
| Reviewers approve a label at the wrong scope | Narrowest scope default; conflict panel; steward escalation; promotion only through the council |
| Extension concepts drift from the core | Re-check match relations on every core release; drift report |
| Customer documents hold personal or confidential content | Written permission; fail-closed screening; retention rule; red-team test |
| Vizier cannot hold tenant-specific names, or its Dimensions API (Alpha) is not ready | Ask early (W6-01); publish preferred label; file-based or Direct Data Intake fallback; labels stay in the SKL |
| Volumes unknown, so the spike is unrepresentative | Record synthetic parameters; repeat at scale test and final gate with real counts |
| Labels go stale | Effective dates, deprecation, periodic review of unused labels |
| Service-layer authorization flaw exposes one tenant to another | Parameterized queries only, separate read and write accounts, isolation tests in the pipeline, store graph controls as backstop |
| Store admin or workbench access bypasses the services | Private network, workbench closed, time-bound logged break-glass, encrypted backups |
| Persona and job rules too coarse or tangled to maintain | Author as governed rules with test cases; review with Personas & Jobs; pilot on reviewer and steward personas |

**Added in version 6.0 (drafted as 5.1)**

| Risk | Mitigation |
| --- | --- |
| Two gateway models are read as competing | Interface in Section 16.8; confirm in D17 |
| Chained services push latency past the 8-second answer target | Derived index, compiled policy cache, parallel retrieval, budgeted context; measure in shadow mode |
| Clarifying questions frustrate users | Persona-weighted tolerance; limit clarifications; calibrate in shadow mode (D29) |
| SOW Week 9 falls inside the pause | Agree cover or move M3 (D21) |
| Protected-characteristic questions are answered without a rule | Fail closed until PC-1 is published (D25) |
| Vee cannot accept external context or expose its reply | Pattern B first; validate what can be validated; confirm with Vizier (D27) |
| Metric drift between the SKL definition and Vizier implementation | Parity tests on every release; the definition wins; report untranslatable parts |
| Persona models diverge across Compass, the PEO map and HR 360 | One registry and a crosswalk (D19) |
| Nexus, Premier and Sales Coach content is not yet described as Digital Assets | Profile-asset and steward review before the content lane goes live (D28) |

### 13.5 Open questions

- Which customer is the pilot, and which CMS and feed formats does it use?
- Which graph store, review-application host and CI platform will the baseline use?
- How many customers and labels per customer should the spike and scale test assume?
- Who staffs operations review, and how many hours a week?
- Which languages beyond English appear in the pilot sources?
- What are the pass thresholds for core load, reasoning time and lookup time?
- Which identity provider and policy engine make access decisions, and where are persona and job assignments held?
- Who owns the persona and job catalog, and how are changes released?
- What is the break-glass procedure for store admin access, and who approves it?
- Which telemetry platform holds service events and audit records, and for how long?
- Can Vee accept external context or call SKL tools through MCP, and can its replies be passed to the circuit breaker?
- Can the HR 360 agent pass the authenticated role and call search-gateway and assemble-answer (SOW assumption, confirm in Week 1)?
- What are the five dimensions of Dr, and what are the tolerance values by persona and consequence?
- How many clarifying turns and options should the engine allow?
- What do COMPLY, FREEZE and HALT look like to a user, and who acts on each?
- Which Nexus, Premier and Sales Coach assets come first, and who profiles and classifies them?
- Is the HSGA gold set the HR 360 set, and who owns the analytics and content strata?
- Who owns the persona and job catalog (v5.0 open question) and where do persona assignments live?
- Who authors PC-1 and SG-1, and which regime roles, if any, qualify for protected-characteristic analytics?
- How does the SOW pause cover work with the 21 December to 3 January pause?

## 14. Maintenance guide

Every change follows the same five steps, and its size decides the version number. This process is proposed; adjust it when the council sets its own.

### 14.1 Change classes

| Class | Examples | Version effect |
| --- | --- | --- |
| Major | Change an invariant; add or remove an asset type or tier; change a MUST rule; change the service contract model | New MAJOR, status resets to Draft |
| Minor | Add a service, persona, measure or section; settle an open decision without breaking an invariant | New MINOR |
| Revision | Wording, corrections, new examples | Note in the version history, no new number |

### 14.2 Amendment steps

1. Describe the change and its class in a comment on the section it touches.
2. Edit the section. Keep numbering stable; add new subsections at the end of a section.
3. Add a row at the top of the version history: version, date, class, what changed, sources. Do not alter older rows.
4. Update the decision register: new decisions as Proposed or Open, settled ones as Decided with the version in the Note column.
5. Move the status in Document control to In review. Only the council sets Approved.

### 14.3 Keep in step

- The HSGA Explorer walkthrough, which mirrors sections 4 to 13 and, from version 6.0, section 16.
- The graph naming standard and the Semantic Asset Metadata Standard, when a naming rule or asset type changes.
- The Semantic Services Baseline plan, when a gate date or service contract changes.
- The crosswalks in addendum D, when the Semantic Governance Guide, the SKL as SSOT proposal or the HR 360 statement of work changes.

### 14.4 Conventions

- Example names, tenant IDs and customer terms are illustrative; label them so.
- A published asset name never changes; document a rename as a new asset and a retirement.
- Record facts from source documents with the source in the version history. Mark anything inferred as proposed.
- Use the document history to compare or restore earlier text instead of retyping it.

## 15. Sources and related documents

Version 6.1 draws on these eight documents: the four used by version 5.0, the three added in 6.0 and TB-07b rev 2, added in 6.1. None is a web source.

| Document | Date | Used for |
| --- | --- | --- |
| Holonic Semantic Governance Architecture, v4.2, Reference Topology and Governance Diagram Edition | not recorded | Holonic theory, seven-layer holarchy, gateway, compiled governance, agents, measurement, lifecycle fit, standards foundation |
| Architecture Proposal: Alternate Labels and Customer Terminology | 31 Oct 2026 | Lexicon layer, services, tenancy, personas, access, operations extensions, pilot gates, risks |
| Graph Naming Standard: Insert for Semantic Governance Standards | 1 Nov 2026 | Asset types and tiers, names, graph classes, repository and tenant IDs, rules, amendments |
| Untangling Scattered Business Logic: an SSOT Architecture | not recorded | Logic classification, governance pipeline, generated executables, Decision API, migration |
| Semantic Governance Standards Guide, v2.4 Draft | 6 Nov 2026 | Contextual relevancy, AI circuit breaker, consumer personas, guardrails, naming, HR 360 statement of work |
| Statement of Work: 12-Week Build of Semantic Services to Support the HR 360 Agent Rollout (Guide Appendix D) | 1 Nov 2026 | Consumer personas, SSOT items, services, measures, scenarios, gates |
| DRAFT Proposal: SKL as Single Source of Truth, Publishing into Vizier | 29 Oct 2026 | SSOT scope, publishing into Vizier, metric definitions, tenant terms |
| TB-07b, Wymore / Control Theory, rev 2: corrected lineage, Model M | Nov 2026 (draft) | Model M lineage and attribution, section 5.4, Addendum F |

The lexicon proposal in turn cites the SKL proposal "SKL as Single Source of Truth, Publishing into Vizier" (29 October 2026) and the PLM Lifecycle Dashboard for the SKL Semantic Services Baseline. Standards named: SKOS-XL, PROV-O, SHACL, R2RML (W3C), BFO (ISO/IEC 21838).

The "Key Pitfalls" table in the SSOT document is empty in the file provided; section 10 uses its problem statement instead.

## 16. Conversational AI support

Conversational AI answers a person’s question about content or analytics using only governed meaning, within the asker’s entitlements, with every claim cited and every answer measured. This section specifies how the SKL, the gateway and the services deliver that.

Tables carry an origin tag: v5.0 (from version 5.0), Guide (Semantic Governance Guide v2.4), SOW (HR 360 statement of work), SSOT (SKL as SSOT proposal), Owner (statement from the document owner), Corpus (the question corpora) and Proposed (an inference or design suggestion, per section 14.4).

### 16.1 Purpose, scope and boundaries

Consumers are Compass (find and explain), Copilot (answer and act), the HR 360 agent, Vee (Vizier’s agent) and partner applications through MCP or REST. Questions are about content (Nexus, Premier, Sales Coach, plan documents, knowledge articles) or analytics (legacy reporting, metrics and insights, Vizier), and some touch both.

**In scope**

- Understanding the prompt: persona, intent, terms, job, outcome
- Disambiguation and clarifying questions
- Entitlement and policy enforcement
- Content, rule and analytics retrieval
- Grounding, trust checks and tracing
- Measurement and rollout

**Out of scope**

- Transactions: the agent explains and points to where to act (SOW)
- Individual financial, tax or legal advice; plan documents remain the legal source (SOW)
- Vee’s internal agent design and model choice
- Full ontologies for every supporting domain; the SOW models Benefits and Retirement in full and other domains only as far as a question needs (SOW)

This section reuses label resolution (Section 7), tenancy and access (Section 8), the services (Section 9), the SSOT (Section 10), the gateway (Section 11) and measurement (Section 12). It adopts the Contextual Relevancy services, the AI circuit breaker and the HR 360 design from Semantic Governance Guide v2.4 (Sections 2.7 and 3.8, and Appendix D).

### 16.2 Design principles

| # | Principle | What it means | Origin |
| --- | --- | --- | --- |
| P1 | Persona from identity | Persona is set from the authenticated role, never from the prompt. It selects relevance, labels, tone and prompt template. | Guide; SOW |
| P2 | Filter first, tailor second | Entitlement filtering happens before any search or ranking. Persona never grants access. | Guide |
| P3 | Anchor before answering | Answer only when the relevancy distance (Dr) is within its persona-weighted tolerance and one holon and job fit. Otherwise ask. | Guide |
| P4 | Every claim grounded or withheld | Each answer cites at least one governed IRI and a source asset for every fact it states (constraint C-11). Answer traceability target is 100%. | SOW |
| P5 | Rules are executed, not recalled | Eligibility, limits and calculations come from the decision-api with the rule and parameter version effective on the question date. The model never computes them. | SOW; v5.0 |
| P6 | Degrade, don’t guess | When retrieval, the graph or a source is unavailable, or no governed source exists, return search results or a clarifying question and record why. | Guide |
| P7 | Information, not advice | An advice-seeking question gets information plus a referral. Legal interpretation, disputes and personal financial hardship route to a person (R-11, R-12). | SOW |
| P8 | Nothing learned without approval | User feedback and harvested terms enter a review queue and a change record before they change meaning. | Guide; SOW |
| P9 | One front door | Applications and agents call search-gateway, assemble-answer, generate-answer, serve-tools or serve-graph, never an index, vector store or graph directly. | Guide; v5.0 |
| P10 | One definition per metric | A metric is symbolic in the SKL and executable in the target; the definition wins any disagreement. | SSOT |

### 16.3 Architecture

Figure 8 shows the conversational path. Questions go down through the front doors, the Context Engine and the governance spine to the SKL and the bound sources; cited answers come back up through the circuit breaker. Tenancy, measurement and human review apply at every layer.

*Figure 8. Conversational AI architecture. The Context Engine is an outbound service; the gateway remains L3; sources are bound, not moved.*

| Component | Role | Origin |
| --- | --- | --- |
| Conversation front doors | The only entry points: search-gateway (entitlement filter first, then search by meaning, then resolve to source), assemble-answer, generate-answer, serve-tools (MCP) and serve-graph. | Guide; SOW |
| Context engine | Turns a prompt into governed context: persona, intent, concepts, job, step, outcome, Dr and entitled context. Eight services (Section 16.5). | Guide |
| Policy and rules | SSOT constraints, rules, calculations and logic, compiled to SHACL, decision tables, access policy, filters and directives (Sections 10 and 11.2). | v5.0; SOW |
| RDSG stages 0 to 5 | Context, structure, time, policy, human hold and directive checks on the request. | v5.0 |
| AI circuit breaker | Validates agent inferences and drafted answers: guardrails first, grounding, then Ds, Db and Dr against tolerances; returns PASS, COMPLY, FREEZE or HALT. trip-circuit-breaker stops or degrades a domain on breach. | Guide; Owner |
| SKL graphs | Core and domain meaning, scoped lexicons, the mapping graph and the governance graph (Sections 6 to 8). | v5.0 |
| Existing estate | Content, analytics and systems of record stay where they are. The mapping graph and Digital Asset descriptions bind them to concepts. | v5.0; Guide |
| Measurement and human spine | Event topics feed 32 measures; stewards, reviewers, the trustee and the council hold the decisions that carry judgment or risk. | v5.0; SOW |

### 16.4 Conversation lifecycle

Every conversational request follows the same twelve steps. Figure 9 shows them across the participants, and the table says where each is enforced.

*Figure 9. Conversation lifecycle. Dashed arrows are returns; the blue arrow is the verdict that decides what the consumer receives.*

| Step | What happens | Enforced by | Origin |
| --- | --- | --- | --- |
| 1 | The front door receives the prompt, the authenticated identity and the tenant context. Without an identity or a tenant it refuses (fail closed). | Front door; policy decision service | v5.0 |
| 2 | resolve-persona sets the persona from the authenticated role. The policy decision derives the entitlement scope from persona, job step, resource and context and logs it. | resolve-persona; policy decision | Guide; v5.0 |
| 3 | reverse-engineer-prompt splits the prompt. map-to-holons resolves terms through label resolution (customer, Insperity, domain, core) and the mapping graph. Flagged cases are noted. | Label resolution; mapping graph | Guide; v5.0 |
| 4 | map-to-jobs matches the job, step and outcome. score-relevancy computes Dr. If Dr is above tolerance, or more than one holon or job fits, the engine asks a clarifying question that names the candidates. classify-intent flags advice-seeking (R-11) and escalation (R-12). | Context engine; EP2 | Guide; SOW |
| 5 | assemble-context retrieves through the front door: entitlement filter, then search by meaning, then resolve to source. Content, rules and analytics are reached through the mapping graph. | search-gateway; EP3 | Guide; SOW |
| 6 | decision-api resolves rule and parameter versions effective on the question date and returns result, version and citation. | decision-api; EP4 | SOW |
| 7 | rank-context scores, filters and de-duplicates. The context package and a directive carrying guardrails go to the answer agent (stage 5). | Context engine; RDSG stage 5 | Guide; v5.0 |
| 8 | The answer agent drafts the answer from retrieved facts and decision results, with citations (generate-answer, assemble-answer). | Answer agent | Guide; SOW |
| 9 | SHACL guardrails and deontic norms are checked first. Then grounding checks every claim against cited IRIs and sources. Then the breaker measures Ds, Db and Dr against consequence-weighted tolerances. | Circuit breaker; grounding; EP5 | Guide; SOW |
| 10 | PASS releases the answer. COMPLY holds it for review or correction. FREEZE holds it for the trustee. HALT blocks it and the consumer gets a fallback message. | Circuit breaker | Guide |
| 11 | record-answer writes the trace (persona, intent, template, retrieved IRIs, rule versions, sources, model) as PROV-O triples and publishes events. | record-answer; telemetry | SOW |
| 12 | If the user disagrees, the flag enters the run-time issue queue and the feedback validation controls. Nothing is learned without approval. | Review service; change control | Guide; SOW |

### 16.5 Context Engine service design

The Context Engine is the Contextual Relevancy service family of the guide, coordinated by the outbound-orchestration-agent, which serves requests from released knowledge only. It is one of the outbound semantic services. It is not a thirteenth baseline service: Section 9.1 points here.

*Figure 10. Context engine internals. The loop returns to the start when the user answers a clarifying question.*

| Service | Does | Output | Origin |
| --- | --- | --- | --- |
| `resolve-persona` | Sets the persona from the authenticated role, never from the prompt. | Persona IRI | Guide; SOW |
| `classify-intent` | Classifies the question against the question intent taxonomy (informational, eligibility, how-to and so on) and applies R-11 and R-12. | Intent class; advice and escalation flags | SOW |
| `reverse-engineer-prompt` | Splits the prompt into intent, entities, terms and constraints. | Term spans, constraints | Guide |
| `map-to-holons` | Resolves terms and entities to concepts and so to the domain holons that own them. | Concepts with scope and match relation | Guide |
| `map-to-jobs` | Matches intent to the persona’s job, job map, step and desired outcome. | Job, step, outcome | Guide |
| `score-relevancy` | Computes Dr, the relevancy distance, and the ambiguity left. | Dr; candidate set | Guide |
| `assemble-context` | Builds the context from the narrowed holons and job within the token budget. | Context items | Guide |
| `rank-context` | Scores and filters candidate context by similarity and policy; removes noise. | Ordered context | Guide |

**The context package**

The Context Engine returns one context package per request, or a clarifying question. The guide lists the services and their roles; the package schema is proposed (Proposed) and given in addendum A. It carries the persona, intent and advice flags, resolved concepts with scope level and match relation, job, step and outcome, Dr and the candidate set, entitlement scope, context items with source asset and version, and the rule and parameter versions that apply.

**Open: does the package equal the RCB?** Stage 0 of RDSG assembles the Requirement Context Bundle (who, what, when, where, why). The package carries the same kinds of information, so this section proposes that for conversational requests the Context Engine supplies what stage 0 needs. The document owner’s description of RDSG (personas, jobs and outcomes applied to an issue or opportunity) suggests the two may be one mechanism. Confirm in D17.

**Relevancy distance and clarification**

- Dr is computed by score-relevancy across five dimensions, weighted by the persona and outcome models. The sections of the guide used for this section do not list the five dimensions; they are expected in the AI Circuit Breaker design (v3.0), which this document does not include.
- Tolerance is persona-weighted. At the gateway, tolerances are also consequence-weighted and tighten as the consequence of a decision rises.
- Above tolerance, or when more than one holon or job still fits, the engine asks a question that names the candidates with their definitions.
- (Proposed) Limit consecutive clarifications and the number of options offered, then degrade to search results or route to a person. The limits are parameters to calibrate in shadow mode (D29).

**Performance**

Targets from the guide: 95% of searches under 2 seconds and 95% of assembled answers under 8 seconds (RT-14). Label resolution answers from a derived index rebuilt on each release, and the compiled policy registry keeps the graph reasoner off the request path (v5.0 Sections 7.7 and 11.2). Parallel retrieval of content and analytics is proposed to protect the 8-second target.

### 16.6 Term resolution and disambiguation

Customers and Insperity use many names for one concept, and one word can mean different things in different places. Resolution therefore walks scopes in a fixed order and stops at the first hit (v5.0 Section 7.7). Figure 11 adds the conversation behavior.

*Figure 11. Term resolution. A term takes the first hit, becomes a clarifying question, or becomes a triage candidate.*

**Rules**

- Order: the caller’s customer lexicon, the Insperity lexicon, the domain lexicon, then core preferred labels. Another tenant’s graphs are never searched.
- An acronym carries a resolution scope and has no global value. An unscoped acronym returns every candidate (Guide Section 3.8).
- Hidden labels match but are never displayed. A synonym, abbreviation or misspelling is a label; a customer concept links to the nearest core or domain concept by exactly one of exact, close, broad or narrow (v5.0 Section 7.4).
- A term with no hit is never silently guessed. The engine answers with the terms it could anchor, asks about the rest, and queues the candidate for triage (v5.0 Section 7.5).

**The four flagged cases in a conversation**

| Flagged case (v5.0 7.4) | Behavior in the conversation | Follow-up |
| --- | --- | --- |
| The same label points to different concepts in one scope | Ask which is meant, naming the candidates with definitions. | Steward adds a disambiguation note. |
| A label equals another concept’s preferred label | Treat the preferred label as authoritative for that scope; ask if the context does not decide. | Domain steward reviews the label. |
| The same label means different things in two tenants | Resolve within the caller’s tenant only. Never mention the other tenant. | Reviewers see the pair as evidence; no cross-tenant path. |
| A candidate has no close match | Decline the term, say what could not be anchored, answer the rest if possible. | Triage as a new local concept or core request. |

**Worked cases from the question corpora**

| Term in the question | Source | Resolution | Conversation behavior |
| --- | --- | --- | --- |
| Original Hire Date | Vee question (Corpus) | No such field. The Field List has Insperity Hire Date and Client Hire Date. | Ask which date is meant. |
| Apella Hire Date | Vee question (Corpus) | A customer label, held in that tenant’s lexicon and mapped to an Insperity concept by a steward. | Answer with the mapped concept; show the tenant’s own label back. |
| turnover, voluntary turnover rate, resignation rate | Vee questions (Corpus) | Distinct metrics, each with one governed definition. | Bind to the right metric; cite its definition and release. |
| HR | Vee question (Corpus) | A department, or the HR domain. | Ask: the HR department, or HR across departments. |
| 401k match, company match, vesting, QLE, COBRA | HR 360 persona labels (SOW) | Label records in lexicons mapped to benefits concepts; DT-11 targets 90% coverage of the top 200 user terms. | Bind directly. |
| attrition (illustrative) | A customer’s own word (Proposed) | Customer lexicon label linked by an exact or close match to the turnover concept after steward approval. | Bind, then answer as turnover. |

### 16.7 Persona, job and entitlement model

*Figure 12. Identity comes first, then entitlements filter, then the persona tailors. A persona never grants access.*

**Rules**

- Persona is an individual of core:persona with the attributes in Guide Section 3.8. It selects relevance, labels, tone and prompt template.
- Persona is set from the authenticated role and never from the prompt. It never grants access; entitlements do.
- A persona label never encodes a protected attribute (constraint C-10).
- A person with two personas has each persona’s rights only while doing that persona’s jobs (v5.0 Section 8.4).

**Twelve consumer personas for the HR 360 agent**

| Persona | Group | Expertise |
| --- | --- | --- |
| worksite-employee | Co-employed worksite employee | Novice |
| new-hire-employee | Employee in the waiting period or first enrollment window | Novice |
| life-event-employee | Employee with a qualifying life event | Novice |
| departing-employee | Employee leaving or reducing hours | Novice |
| client-human-resources-administrator | HR contact at the worksite client | Practitioner |
| client-owner-executive | Business owner or executive at the worksite client | Practitioner |
| human-resources-specialist | Internal HR specialist or advisor | Expert |
| benefits-specialist | Internal benefits operations | Expert |
| retirement-plan-specialist | Internal 401(k) services | Expert |
| payroll-specialist | Internal payroll operations | Practitioner |
| compliance-analyst | Internal compliance and audit | Expert |
| insights-analyst | Enterprise Analytics consumer of HR 360 measures | Practitioner |

Source: HR 360 statement of work, Section 4.3 (SOW). Design-time roles such as knowledge engineer and steward are operating-model roles, not personas.

**Three persona registries to reconcile**

| Registry | Personas | Used by |
| --- | --- | --- |
| Compass sellers | BPA (Business Performance Advisor), BPC (Business Performance Consultant), BSA (Business Solutions Advisor) | The 200 Compass content questions |
| PEO service map | CA Client Admin; HR HR Specialist; P1 Business Owner / CEO; P2 Finance Leader; P3 HR Leader; P4 Operations and Safety Leader; P5 People Manager; P6 Worksite Employee; P7 IT and Systems Administrator | The 179 customer questions and their job classification |
| HR 360 consumers | The twelve above | The HR 360 agent and its gold set |

Candidate matches, to be confirmed by Personas and Jobs (Proposed): P6 Worksite Employee and worksite-employee; P1 Business Owner and client-owner-executive; CA Client Admin or P3 HR Leader and client-human-resources-administrator. A single registry with a crosswalk is proposed as D19.

**Jobs, steps and outcomes**

map-to-jobs anchors a question to the persona’s job, job step and desired outcome. The PEO job catalog supplies the jobs, for example J20 Use workforce data to make business decisions, J22 Get HR answers and complete HR tasks myself, and J15 Manage and improve team performance. A desired outcome is written as a direction, a metric, an object and a clarifier, with a metric card holding target and baseline (Guide Section 3.13).

**One question, three personas**

Question: “What is our turnover this year?” Outcomes follow the disclosure matrix for aggregate workforce data, classified C2 Confidential in the customer corpus.

| Persona | Anchored job | Receives | Access |
| --- | --- | --- | --- |
| Business owner or CEO | J20 | Turnover by department, compared with last year | Allowed (client owner) |
| People manager | J15 | Turnover for their own team only | Own team only (client manager) |
| Worksite employee | J22 | No company-wide figures; own records stay available | Denied for C2; own records allowed |

### 16.8 Policy, guardrails and enforcement

Guardrails are not stored beside questions. They are rules, authored once in the SSOT, tied to the obligations that require them, compiled, and enforced at five points on every conversation. This replaces guardrails wired to a fixed list of questions and answers.

*Figure 13. From sources of obligation to enforcement. Drift, verdicts and user flags return to review.*

**What the SSOT holds**

Constraints (SHACL, what must always be true), rules (decision tables, what follows from state), calculations (declarative formulas with test vectors) and logic (code that references SSOT terms and versions). Values that change by year or plan are versioned parameters with an effective period and a source citation; none is typed into a prompt or code (SOW). Each item is tied to the policies, standards, disciplines, regulations, contractual obligations and legal concerns (privacy, disclosure, confidentiality, sensitivity) that require it (Owner). SMEs maintain constraints through forms and rules as decision grids.

**Five enforcement points**

| Point | Where | Artifact and example rules | On failure |
| --- | --- | --- | --- |
| EP1 Front door | search-gateway, resolve-persona | Identity, tenant, entitlement scope; R-13: an employee sees only their own elections, a client administrator only their worksite | Refuse; fail closed |
| EP2 Intent policy | classify-intent | R-11 answer policy; R-12 escalation | Advice-seeking: information plus referral. Legal interpretation, disputes, personal hardship: route to a person |
| EP3 Retrieval | search-gateway | Entitlement filters, sensitivity class, small-group suppression (SG-1, proposed) | Filter before ranking; suppress the result |
| EP4 Generation | assemble-answer, decision-api | Directive guardrails; rule and calculation results with versions; R-14 source precedence | Two sources disagree: use the winning source and log the conflict as a defect (L-05) |
| EP5 Release | grounding-agent, circuit breaker | C-11 citation constraint; Ds, Db, Dr tolerances | Verdict: PASS, COMPLY, FREEZE or HALT |

**Verdicts**

| Verdict | Trigger | What happens | Who acts |
| --- | --- | --- | --- |
| PASS | All distances within tolerance | The cited answer is released. | No one |
| COMPLY | A distance above tolerance | Held for review or corrected before release. | Ops reviewer or the agent, then re-check |
| FREEZE | A distance at 1.5 times its tolerance or more | Held for the human trustee, with a manual fallback. | Trustee |
| HALT | A guardrail is breached (SHACL or deontic norm) | Blocked. Deterministic; it cannot be approved. The consumer receives a fallback message. | Domain Governance Team, where v5.0 routes critical violations |

Source: Guide Section 2.7 (Guide). Who acts on COMPLY and HALT, and the consumer-facing text for each verdict, are proposed (Proposed) and recorded as D30.

**The circuit breaker and RDSG**

RDSG is the requirements path: it applies personas, jobs and outcomes to an issue or opportunity. The circuit breaker measures the trustworthiness of AI and validates inferences made by agents that support the requirements gateway (Owner). A conversational answer is such an inference. The proposed interface, to confirm as D17 (Proposed):

| RDSG stage | For a conversational request | Circuit breaker role |
| --- | --- | --- |
| 0 RCB | Context engine output supplies who, what and why; holons are activated. | None |
| 1 SHACL | Structure of the context package and of the answer record. | Contributes to Ds |
| 2 SWRL | Rule and parameter versions effective on the question date (RT-08, L-06). | None |
| 3 PEP | Entitlements, purpose, advice and escalation policy. | None |
| 4 UCA | Irreversible or unsafe actions. MVP1 is information-only; this applies when tools act. | Hold for authorization |
| 5 Directive | Directive with guardrails for the answer agent. | None |
| 6 Facade | Acceptance criteria, trust score, audit record, quarantine. | The breaker is the validation behind this stage and also runs on any agent inference |

At domain level, trip-circuit-breaker stops or degrades answers in a domain when hallucination or grounding thresholds are breached. RT-02, RT-03 and RT-04 feed it; a trip publishes knowledge.breaker.tripped.v1 and stays until the root cause is fixed and a reset event is published. Every trip needs a root cause within two business days (RT-05).

**Rules not yet authored**

Two rules the conversation needs do not exist yet. Until they are published, the proposed behavior is to fail closed: route the question to a person or decline with a reason, and record “no published rule” in the answer log.

| Rule | Evidence | Parameters the rule author decides |
| --- | --- | --- |
| PC-1 Protected characteristics in analytics (proposed ID) | The customer corpus proposes a term, protected characteristic (gender, race, age), classified C4 Highly restricted for Compliance and Analytics purposes only. Vee questions ask for ethnicity, birthdays, birth year and generation, which derives from date of birth. | Aggregate or individual; purpose and role, including any named regime role; small groups; derived attributes; operational uses such as birthday lists; legal basis from compliance and legal |
| SG-1 Small-group suppression (proposed ID) | The customer corpus records that reports hide numbers for small teams (CQ-154). The Brea office, HR and generation cuts can be small. | Threshold, scope, and whether suppression is silent or explained |

### 16.9 Content and analytics routing

A governed concept reaches the answer through three lanes. Content questions go through Digital Asset descriptions. Questions about eligibility, limits and amounts go through the decision-api. Analytics questions go through metric definitions and the target that executes them. A question can use more than one lane.

*Figure 14. Content, rules and analytics lanes merge into one entitled, cited answer.*

**Binding model**

| Binding | From | To | Status |
| --- | --- | --- | --- |
| Content | Concept | Digital Asset description: owner, classification, source system, access URL, and the concepts and steps the asset is about; passages in the domain vector partition (C-08) | Guide; SOW |
| Rules and calculations | Concept | decision-api items R, K and L with versions and citations | SOW |
| Analytics | Concept | Report, field or metric implementation record: for example one of the 23 reports and its fields, or a Vizier metric | Proposed |

Invariant 4 denies edges by default and allows them by graph pair. The content and rules bindings exist in the guide. The analytics binding needs a new allowed pair, mapping graph to a metric or report implementation record (D28). Nexus, Premier and Sales Coach content must first be described as Digital Assets by profile-asset and steward review; the guide does not yet do this for them.

**Metric answers**

- The SKL holds each metric as a symbolic, tool-neutral expression over concept IDs, with period handling, aggregation, filters, units, edge cases, test cases and a version. Vizier holds an executable implementation, tested against it.
- Parity tests run on every release and block the publish on failure. If the definition and an implementation disagree, the definition is correct.
- What a target cannot express is reported as untranslatable and not approximated. If a metric cannot be expressed in Vizier, it is computed in the outbound services and loaded as data.
- The answer cites the definition and its release. Illustration from the SSOT proposal (SSOT): VoluntaryTurnoverRate for period p is the count of separations in p with a voluntary reason, divided by average headcount in p. Separation, Voluntary and Headcount are SKL concepts.

**Question types and their lanes**

The 53 Vee pre-beta questions fall into five types against the 23-report list. This is an analyst classification (Corpus; Proposed) and the counts are approximate.

| Type | Count | Lane | Controls it needs |
| --- | --- | --- | --- |
| Direct report pull (filter, list or count) | 19 | Analytics, report | Entitlements, sensitivity class, small-group rule |
| Computed on reports (rates, trends, drivers) | 15 | Analytics, metric | One governed definition per metric; small-group rule; drivers need agent validation |
| Report plus extra logic or matching | 6 | Analytics plus rules | Mappings plus rules, for example work state against work location |
| About the analysis itself (explain, define) | 9 | Analytics, metric glossary | Relevancy: the context of what the user is viewing; cited definitions |
| No supporting report or field | 4 | None | Decline honestly and log a coverage gap (degrade, don’t guess) |

**Vee and Vizier**

Vizier has its own semantic layer and its own agent, Vee. The SSOT proposal covers publishing into Vizier. It does not cover Vee as a consumer of SKL guardrails, and the guide does not mention Vee. Three patterns are possible (Figure 15).

*Figure 15. Three patterns for Vee. B is specified in the SSOT proposal; A and C depend on what Vee can accept.*

| Pattern | Needs | Strength | Limit |
| --- | --- | --- | --- |
| A Vee consumes SKL context | Vee can accept external context or call SKL tools (MCP) | Full guardrails before and after Vee | Unknown whether Vee supports it |
| B SKL publishes into Vizier | The SSOT proposal: project, validate, publish, reconcile; Dimensions API status (Alpha) | Specified; one meaning everywhere; drift is detected | Rules are not enforced in Vizier; only projections and results |
| C Hybrid (proposed target) | B in place, plus a pre-check on the prompt and the breaker on Vee’s reply | Guardrails around an agent the SKL does not control | Needs Vee to expose its reply to the breaker |

(Proposed) Start with B, which is already proposed. Move to C when the interface to Vee is known. Use A only if Vee supports it. This is recorded as D27.

### 16.10 Measurement

Trust is measured, not assumed. The measures below follow the guide’s metrology: 32 measures, 14 at design time and 18 at run time, each tagged to Trust, Quality, Accuracy or Completeness, computed from triples or event topics and shown in the Operations Workbench. Targets are starting values to calibrate. A changed formula is a new version, not a silent edit.

*Figure 16. Measures along the conversation path, and the event topics that carry them.*

| ID | Measure | Target | Dimension |
| --- | --- | --- | --- |
| RT-01 | Answer traceability: answers citing a governed IRI and a source per fact | 100% | Trust |
| RT-02 | Grounded claim rate | 98% or higher | Trust |
| RT-03 | Hallucination rate on the gold set | Below 2% | Accuracy |
| RT-04 | MTBH = T\_ops divided by N\_h (AI Circuit Breaker v3.0 metrics registry) | Rising trend; breaker threshold set at the second gate | Trust |
| RT-05 | Circuit breaker trips, with root cause | Root cause within 2 business days | Trust |
| RT-06 | Answer accuracy on the 150-question gold set | 90% or higher at the proof gate | Accuracy |
| RT-08 | Rule-version correctness | 100% | Accuracy |
| RT-09 | Policy compliance (R-11, R-12) | 100% | Trust |
| RT-10 | Entitlement violations | 0 | Trust |
| RT-14 | Answer latency, 95th percentile | 2 s search; 8 s assembled answer | Quality |

Sources: Guide Appendix D, Section 6 (SOW); v5.0 Section 12 for cross-tenant results (0) and labels with source and reviewer (100%) (v5.0).

**MTBH and statistical process control**

MTBH is tracked under statistical process control. A falling MTBH is an early warning that the system is outside its validated envelope. RT-02, RT-03 and RT-04 also feed the circuit breaker: a breach trips it for that domain until the cause is fixed.

**Shadow mode**

(Proposed) Before any cutover, run the Context Engine beside the existing hard-wired answers on the gold set. Measure agreement between the two, adjudicate each disagreement with an SME, check traceability and entitlements on every answer, and compare the clarification rate with the cases that needed one. Cut over a lane at a gate only when agreement, RT-01, RT-02 and RT-10 meet their targets.

**End-to-end traceability**

Any answer traces back to the requirement that asked for it and forward to the measure that judged it, with one SPARQL query against the answer record (SOW): requirement, competency question, change record, release (ontology and SSOT versions), question (persona, intent), retrieved IRIs and decision-api results, source assets and legal norms, answer, grounding check, measure observation, feedback or defect, new requirement.

### 16.11 Human checkpoints and the learning loop

Machines propose and people decide, as in Section 11.4. These rows extend that table for conversations.

| Event | Decided by | Result |
| --- | --- | --- |
| Advice-seeking question | Rule R-11; no person | Information plus a referral; logged for RT-09 |
| Legal interpretation, dispute or personal hardship | Rule R-12 routes to a person | A person takes the question |
| Answer held at FREEZE | Trustee | Release, correct or withhold; manual fallback meanwhile |
| Answer held at COMPLY | Ops reviewer (Proposed) | Corrected and re-checked, or withheld |
| Domain tripped | SG Operations with the domain steward (proposed) | Root cause in 2 business days; reset event |
| User flags an answer | Review queue, then steward | Change record; nothing learned without approval |
| Candidate term from question logs | Ops reviewer | Label, local concept, core request or rejection (Section 7.5) |
| Low-confidence queue | Ops reviewer | Median age of open items 3 days or less (RT-16) |

### 16.12 Failure modes and degraded behavior

| Failure | Behavior | Origin |
| --- | --- | --- |
| No authenticated identity or tenant | Refuse. Fail closed. | v5.0 |
| Dr above tolerance, or several holons or jobs fit | Ask a clarifying question naming the candidates. | Guide |
| No governed source supports the answer | Return search results or a clarifying question; do not state an ungrounded answer. | Guide |
| Retrieval or graph unavailable | Degrade; do not guess. Record the cause. | Guide |
| Two sources disagree | Use the winning source by R-14 precedence and log the conflict as a defect. | SOW |
| A new rule parameter takes effect | New answers use the new version; earlier answers keep the version they used (L-06). | SOW |
| Guardrail breached | HALT. Blocked. Fallback message. | Guide |
| Domain breaker tripped | Stop or degrade answers in that domain until reset. | SOW |
| A term cannot be mapped | Decline the term, answer what is anchored, queue the candidate. | v5.0 |
| No published rule for the question type (PC-1, SG-1) | Route to a person or decline with a reason; log “no published rule”. | Proposed |
| Vizier drifts from the SKL release | Reconcile; mismatch triggers rollback and a drift flag; answers cite the release they used. | SSOT |

### 16.13 Rollout and calendars

Two calendars apply. The HR 360 statement of work runs 12 weeks from Monday 2 November 2026 to Friday 22 January 2027. The v5.0 services pilot assumes a 9 November 2026 start and a pause from 21 December to 3 January. Figure 17 overlays them with proposed conversational AI phases.

*Figure 17. Calendars and proposed phases. SOW Week 9 ends on 1 January, inside the v5.0 pause.*

| SOW gate | Week | Date | Passes when | Proposed name |
| --- | --- | --- | --- | --- |
| G1 Baseline | 2 | 13 Nov 2026 | Deliverables 1 to 3 approved; targets confirmed against the baseline | M1 |
| G2 Keel released | 6 | 11 Dec 2026 | Keel released; DT-02 at 80% or higher, DT-03, DT-05 and DT-08 at 100% | M2 |
| G3 Services live in test | 9 | 1 Jan 2027 | HR 360 answers gold-set questions end to end; RT-01 at 100% in test | M3 |
| G4 Proof of capability | 12 | 22 Jan 2027 | Five scripted scenarios pass live; after report shows targets met or gaps explained | M4 |

Sources: Guide Appendix D, Section 10.2 (SOW). Dates are computed from the week numbers. The gate names collide with v5.0’s G0 to G3, so renaming the SOW gates M1 to M4 is proposed (D21). Week 9 ends inside the pause, so either the pause excludes MVP1 or M3 moves.

| Phase | Scope | Exit evidence | Origin |
| --- | --- | --- | --- |
| 0 Shadow mode | Context Engine beside the hard-wired Compass and HR 360 answers on the gold set | Agreement, RT-01, RT-02, RT-10 reported at M3 and M4 | Proposed |
| 1 Benefits and retirement (MVP1) | Twelve personas; 40 SSOT items; services unchanged from the guide plus six HR 360 services; five scripted scenarios and a breaker trip | Proof of capability at M4: the Section 8 targets met or gaps explained | SOW |
| 2 Pilot lane | Benefits lane under the v5.0 pilot: customer lexicon, tenant terms, isolation tests | G1 8 Mar 2027: zero customer-driven triples in the core, zero cross-tenant results | Proposed; v5.0 |
| 3 Analytics lane | Vizier projections live; Vee pattern B, then C; metric parity tests | G2 3 May 2027: pilot vocabularies live in Vizier with parity and reconcile checks clean | Proposed; v5.0 |
| 4 Content assets and Compass | Nexus, Premier and Sales Coach described as Digital Assets; Compass on the same front doors | G3 24 May 2027: second customer onboarded with no core change | Proposed; v5.0 |

### 16.14 Decisions, assumptions and open items

Decisions D17 to D30 are in section 13.3 and the open questions are in section 13.5. Assumptions this section relies on:

- The HR 360 agent can call external tools (MCP or REST) and pass the authenticated user role (SOW). Confirm in Week 1.
- Plan documents, not the SKL, remain the legal source; answers cite the norm or plan document and never interpret beyond it (SOW).
- No personal data is loaded in MVP1; instance data is synthetic or de-identified (SOW).
- The disclosure classes used in examples come from the customer-question classification (Corpus) and must be confirmed against the published matrix.

## Addendum A. Context Engine service contract

This addendum specifies the contract of the conversation services. It follows the five shared rules of v5.0 Section 9.1: each request carries caller identity and tenant context; a policy decision is logged before any read or write; graph access is parameterized and no service accepts a raw query; each service emits events for request, decision, outcome and duration; the contract is versioned and changing it is a governed change.

### A.1 Services and agents

| Name | Kind | Does | Origin |
| --- | --- | --- | --- |
| `outbound-orchestration-agent` | Agent | Chooses the route for each request; asks a clarifying question when Dr is above tolerance or more than one holon or job fits; serves released knowledge only. | Guide |
| `resolve-persona` | Service | Persona from the authenticated role. | Guide; SOW |
| `classify-intent` | Service | Intent class; applies R-11 and R-12. | SOW |
| `reverse-engineer-prompt` | Service | Intent, entities, terms, constraints. | Guide |
| `map-to-holons` | Service | Terms to concepts and holons; calls label resolution. | Guide |
| `map-to-jobs` | Service | Job, step and outcome for the persona. | Guide |
| `score-relevancy` | Service | Dr and ambiguity left. | Guide |
| `assemble-context`, `rank-context` | Services | Build and rank context within the token budget. | Guide |
| `decision-api` | Service | Resolves SSOT rule and parameter versions (R-01 to R-14, K-01 to K-08); returns result, version and citation. | SOW |
| `generate-answer` | Service | Calls the model with the assembled context; returns search results or a clarifying question when degraded. | Guide |
| `assemble-answer` | Service | Builds the HR 360 answer from retrieved facts and decision results; attaches citations; enforces C-11. | SOW |
| `audit-answer` | Service | Rejects or flags answers that cite no governed terms. | Guide |
| `grounding-agent` | Agent | Checks every claim in a draft against cited IRIs and sources; blocks or escalates ungrounded claims. | SOW |
| `trip-circuit-breaker` | Service | Stops or degrades answers in a domain when hallucination or grounding thresholds are breached. | SOW |
| `record-answer` | Service | Writes each answer’s trace as PROV-O triples. | SOW |
| `query-planning-agent`, `federation-agent`, `result-explanation-agent` | Agents | Compass search: turn a question into a graph query using persona vocabulary, plan federation, explain each match. | SOW |

Two overlaps need one name (D24): `audit-answer` and `grounding-agent` both check an answer against governed sources, and `generate-answer` and `assemble-answer` both draft it. The v5.0 agent called RAG grounding is probably `grounding-agent` (Proposed).

### A.2 Request and context package

The schema below is proposed (Proposed). IRIs, identifiers and values are illustrative. The example is scenario D1 of the HR 360 statement of work, whose trace must show R-04, R-07, K-02 and K-05 with versions and the answer limited to the employee’s own plan.

```
// ConversationRequest (from the front door)
{
  "request_id": "req-0001",
  "tenant_id": "t7f3a9c21",
  "identity": { "subject": "user-123", "role": "worksite-employee" },
  "channel": "hr360-agent",
  "prompt": "Am I eligible for the company 401(k) match, and when am I fully vested?"
}

// ContextPackage (from the context engine)
{
  "request_id": "req-0001",
  "persona": "persona:worksite-employee",
  "intent": { "class": "eligibility", "advice_seeking": false, "escalation": false },
  "concepts": [
    { "span": "401(k) match", "concept": "benefits:employer-match",
      "scope": "domain-lexicon", "relation": "exact" },
    { "span": "fully vested", "concept": "benefits:vesting",
      "scope": "domain-lexicon", "relation": "close" }
  ],
  "job": { "job": "J22", "step": "check eligibility", "outcome": "know when I am vested" },
  "relevancy": { "dr": "within tolerance", "candidates_left": 0 },
  "entitlement": { "scope": "own-plan-only", "rule": "R-13" },
  "rules": [ "R-04", "R-07", "K-02", "K-05" ],          // each with its effective version
  "context_items": [
    { "kind": "content", "asset": "plan-document", "version": "plan-year-2026", "rank": 1 },
    { "kind": "rule-result", "source": "decision-api", "version": "ssot-release-n", "rank": 2 }
  ],
  "token_budget": { "limit": "model-dependent", "used": "within limit" }
}

// Clarifying response (instead of a package)
{
  "request_id": "req-0002",
  "clarification": {
    "reason": "ambiguous-reading",
    "question": "Two readings fit. Which do you mean?",
    "options": [
      { "label": "Turnover rate for the HR department", "concept": "metric:turnover-rate" },
      { "label": "Number of HR employees who left", "concept": "metric:separation-count" }
    ]
  }
}
```

### A.3 Degraded and error responses

| Code | When | Consumer receives | Logged |
| --- | --- | --- | --- |
| IDENTITY\_MISSING, TENANT\_MISSING | No authenticated identity or tenant | Refusal | Decision record |
| AMBIGUOUS | Dr above tolerance or several holons or jobs fit | Clarifying question with candidates | Dr, candidates |
| NO\_GOVERNED\_SOURCE | No source supports the answer | Search results or a clarifying question | Cause |
| POLICY\_ROUTE | R-12 escalation, or no published rule (PC-1, SG-1) | Routed to a person, or a reasoned decline | Rule ID or “no published rule” |
| VERDICT\_HOLD | COMPLY or FREEZE | Fallback message (text per D30) | Verdict, distances |
| POLICY\_HALT | Guardrail breached | Fallback message | Rule ID |
| BREAKER\_TRIPPED | Domain tripped | Fallback message for the domain | Trip event |
| SOURCE\_UNAVAILABLE | Retrieval or graph unavailable | Degraded response | Cause |

### A.4 Event topics

| Topic | Published by | Consumed by | Origin |
| --- | --- | --- | --- |
| `knowledge.release.ontology.published.v1` | Release pipeline | search-index, search-vector, query-planning-agent caches | SOW |
| `knowledge.release.ssot.published.v1` | SSOT pipeline | decision-api, assemble-answer | SOW |
| `knowledge.answer.recorded.v1` | record-answer | Measurement services, Operations Workbench | SOW |
| `knowledge.answer.flagged.v1` | HR 360 feedback, grounding-agent | Run-time issue queue, feedback validation controls | SOW |
| `knowledge.breaker.tripped.v1`, `.reset.v1` | trip-circuit-breaker | HR 360, SG Operations, Operations Workbench | SOW |
| `knowledge.context.resolved.v1` | Context engine | Measurement services (Dr, clarification rate) | Proposed |
| `knowledge.context.clarified.v1` | Context engine | Measurement services, review queue | Proposed |

## Addendum B. Policy and guardrail model

### B.1 SSOT rule record

Each rule, constraint, calculation and logic item is one record. The field set is proposed (Proposed), built from the SOW and the SSOT proposal.

| Field | Holds |
| --- | --- |
| ID and type | C (constraint), R (rule), K (calculation), L (logic), or a parameter; one stable ID |
| Statement | The rule in controlled language, and its formal form (SHACL, decision table, formula) |
| Obligation sources | The policy, standard, discipline, regulation, contract term or legal concern behind it; for legal concerns, which of privacy, disclosure, confidentiality or sensitivity |
| Classes and purposes | Sensitivity classes it governs; purposes it allows (for example Compliance, Analytics) |
| Applies to | Personas, jobs, domains, tenants |
| Effective period | Effective from and to; parameters keep the version used by each answer |
| Owner | Accountable steward; approver; reviewer |
| Test cases | Given these inputs the result must be this; parity tests for metrics |
| Compiled targets | SHACL, decision table, OPA policy, search filter, directive text, data check |
| Status and version | Proposed, in review, approved, published, deprecated; semantic version; release that carried it |

### B.2 Disclosure matrix summary

Summary of the dispositions in the 179-question customer classification (Corpus). Confirm against the published matrix before use. The protected-characteristic term is proposed.

| Class | Worker (own data) | Client manager | Client owner or HR admin | Third party |
| --- | --- | --- | --- | --- |
| C2 Confidential (for example turnover for the company) | Deny | Allow, own team | Allow | Deny |
| C3 Restricted (for example pay data) | Own records | Own reports, by purpose | Allow, by purpose | Deny (CQ-118: a lender asks for a salary) |
| C4 Highly restricted (for example protected characteristics) | See matrix | Deny | Deny, except a named regime role | Deny |

Outcomes are Allow, Allow with conditions, Route to a person, and Deny. C1 is not summarized here.

### B.3 Example rule records

| ID | Statement | Obligation sources | Status |
| --- | --- | --- | --- |
| R-11 | A question classified as advice-seeking gets information plus a referral, never a recommendation. | No-advice policy; fiduciary duty; answer ethics (Organizational Values domain slice) | SOW |
| R-12 | Questions touching legal interpretation, disputes or personal financial hardship route to a person. | Escalation policy; legal norms | SOW |
| R-13 | An employee sees only their own elections; a client administrator only their worksite. | Entitlement scope; privacy and confidentiality (to be cited by the steward) | SOW |
| R-14 | Source precedence: plan document over SPD over FAQ over knowledge article when sources conflict. | Plan documents are the legal source | SOW |
| C-10 | A persona label never encodes a protected attribute. | Privacy; non-discrimination (to be cited by the steward) | SOW |
| C-11 | Every answer record cites at least one governed IRI and a source asset for every fact it states. | Answer traceability; ISO/IEC 42001 and NIST AI RMF alignment (SOW Section 7.3) | SOW |
| PC-1 | Protected-characteristic questions in analytics: to be authored. Parameters in Section 16.8. | To be cited by compliance and legal | Proposed |
| SG-1 | Small-group suppression: to be authored. Threshold and scope per Section 16.8. | Privacy; confidentiality | Proposed |

## Addendum C. Question corpora and worked examples

### C.1 The corpora

| Corpus | Size | What it holds | Use |
| --- | --- | --- | --- |
| Compass content questions | 200 | Seller questions tagged by persona (BPA, BPC, BSA), topic, product and tool | Content lane gold-set stratum; terminology for lexicons |
| Customer questions | 179 | Each classified by sensitivity class, asker, purpose, disclosure outcome and PEO job | Draft source for the disclosure rules; persona and job anchors |
| Vee pre-beta questions | 53 | Analytics and roster questions beside a list of 23 reports and a Field List | Analytics lane gold-set stratum; coverage gaps |
| HR 360 gold set | 150 | SME-approved question and answer pairs for benefits and retirement, with a rubric; plus a sample of real de-identified HR 360 questions | Baseline in SOW Week 2; before and after measures |
| HR 360 scenarios | 5 + 1 | D1 to D5 scripted scenarios and an unscripted breaker trip | Proof of capability at M4 |

Whether the HSGA 150-question gold set is the HR 360 set or a broader one is open (D23). The proposal is to keep the HR 360 set as the benefits stratum and add content and analytics strata drawn from the other corpora.

### C.2 Report and field coverage for analytics

- The Report List has 23 reports. Six have no Vee test question: Client Pay and Deduction Codes, Default ITA Org Level, Default Job Cost Splits, Job Cost ITA Org Level Compare, Handbook Acknowledgment, and Employee Pay Status Report.
- Some Vee questions have no supporting field in the Field List: Original Hire Date, HPI, a 401(k) balance, a debit amount, planned headcount and a PO Box. The engine should decline these honestly and log a coverage gap.
- Turnover and resignation rates have no report behind them. They are computed metrics, so they need governed definitions and an implementation in Vizier or in the outbound services.

### C.3 Worked examples

Expected behavior is proposed (Proposed) from the design in Section 16. Dispositions for corpus questions follow the customer classification.

| Question | Persona | Terms and routing | Policy | Expected outcome |
| --- | --- | --- | --- | --- |
| “Am I eligible for the company 401(k) match, and when am I fully vested?” (HR 360 D1) | Worksite employee | 401(k) match and vesting resolve in the domain lexicon; content plus rules lane | R-13: own plan only | Answer from R-04, R-07, K-02, K-05 with versions; plan provision cited |
| “Should I move my 401(k) into the Roth option?” (D4) | Worksite employee | Intent: advice-seeking | R-11 | Information on both options with sources, no recommendation, referral offered; RT-09 logs it |
| “An employee is terminating Friday. What do we owe him on benefits?” (D3) | Client HR administrator | Termination event; COBRA; final deductions | R-12 not triggered unless legal interpretation is asked | L-02 flow: R-08 notice, legal norm, final deduction, distribution options; employer and administrator duties separated |
| “What is required before making post-termination payments to staff?” (Compass Q130) | Seller (BPA, BPC or BSA) | Payroll and compliance concepts; content lane | Approved content only; legal judgment routes to a person | Cited answer from bound Insperity content |
| “I am a lender verifying employment and income. Can you confirm his salary?” (CQ-118) | Third party | Pay data, C3 | Third parties need authorization | Deny |
| “We want to terminate an employee who filed a complaint last month. Is that safe to do?” (CQ-049) | HR leader | Termination; complaint | C4 and a legal-judgment boundary | Route to a person |
| “What is our turnover this year by department, and how does it compare with last year?” (CQ-119) | Business owner | Turnover metric; J20 | Own-workforce aggregate, C2 | Allow; definition and release cited |
| “Show me turnover at the Brea office for Q3 2026 and Q3 2025.” (Vee) | Client user | Turnover metric; Brea as a location; Q3 as a period | Small groups suppressed (SG-1) | Allow with conditions; definition cited |
| “What is the headcount by ethnicity?” (Vee) | Client user | Protected characteristic | PC-1 not yet published | Route to a person or decline; log “no published rule” |
| “How many employees have an Original Hire Date in 2025?” (Vee) | Client user | No such field; Insperity Hire Date and Client Hire Date are candidates | None | Clarifying question |
| “What is turnover for HR?” (Vee) | Client user | HR as a department or as a domain; rate or count | None | Clarifying question with two options |
| “What is the home phone number for Robin Alexander?” (Vee) | Client user | Named worker; personal contact data | Classification not confirmed | Needs a rule; until then, fail closed |

## Addendum D. Crosswalks

All crosswalks are proposed (Proposed) unless a source states the correspondence.

### D.1 Guide vessel vocabulary to HSGA layers

The guide’s Keel and North Star architecture uses a vessel vocabulary. HSGA uses seven layers and cross-cutting spines.

| Guide term | Guide meaning | HSGA v5.0 counterpart |
| --- | --- | --- |
| Keel | Governed, deterministic foundation: ontologies, vocabularies, SSOT for rules and calculations, shapes, metric definitions | L4 graphs and L5 semantic governance |
| North Star | The bearing: every decision, insight and AI answer rests on governed, traceable meaning | Section 12 measurement and trust; the human spine |
| Hull | Mapping layer and federated agents; links assets to concepts and answers in place | Mediation holon (Section 5.3) and L2 connectivity |
| Bridge | Compass (find and explain) and Copilot (answer and act) | L6 and L7 consumers, with the outbound services |
| Ballast | Governance: change control, release pipeline, monitoring | L5, the L3 gateway and Section 12 |
| Waterline | Feedback validation controls: nothing is learned without traceability, validation and approval | Human checkpoints (Section 11.4) |
| The sea | Sources that stay where they are, described in the keel | L1 and L2 sources; Digital Asset descriptions |

### D.2 Names that differ between documents

| HSGA v5.0 | Guide v2.4 or SOW | Note |
| --- | --- | --- |
| Label resolution service | Called by `map-to-holons` | Resolution order is the same |
| Policy decision service; stage 3 PEP | Entitlement filtering in `search-gateway`; R-13 | Filter first, tailor second |
| Decision API (Section 10.3) | `decision-api` | The same service by name |
| RAG grounding agent | `grounding-agent`; `audit-answer` | Confirm which one (D24) |
| Trust circuit breaker (L3) | `trip-circuit-breaker`; AI circuit breaker with Intercept, Measure, Actuate | Domain-level trip and per-answer check |
| Telemetry service; governance graph audit | `record-answer`; PROV-O answer trace | Same intent |
| Candidates service | `vocabulary-agent` harvests labels from question logs | Same triage destinations |
| Mapping confidence agent | `mapping-agent` proposes mappings; steward approves | Same human gate |
| 32 measures (Section 12.1) | 14 design-time and 18 run-time measures | The same set |

### D.3 Where each topic is defined

| Topic | v5.0 | Guide v2.4 | Other |
| --- | --- | --- | --- |
| Label resolution, lexicons | Sections 7, 9 | Section 3.8 | SSOT proposal (skills terms) |
| Context engine | Section 16 (new in 6.0) | Section 2.7, Section 1.8 | HR 360 SOW (classify-intent, resolve-persona) |
| Circuit breaker, verdicts | Sections 11, 12 (MTBH) | Section 2.7 | HR 360 SOW (trip-circuit-breaker); AI Circuit Breaker v3.0 |
| Personas, jobs, outcomes | Section 8.3 (operators) | Sections 3.8, 3.13 | HR 360 SOW Section 4.3 |
| SSOT rules, calculations | Section 10 | Section 3.5 | HR 360 SOW Section 4.4 |
| Vizier publishing | Section 9.3 | None | SSOT proposal |
| Measurement | Section 12 | Section 3.6 | HR 360 SOW Section 6 |

## Addendum E. Glossary

| Term | Meaning | Origin |
| --- | --- | --- |
| AI circuit breaker | The trust gate: guardrails first, then Ds, Db and Dr against tolerances, returning PASS, COMPLY, FREEZE or HALT; also a domain-level stop (trip-circuit-breaker). | Guide; SOW |
| Context engine | The Contextual Relevancy services that turn a prompt into governed context. | Guide |
| Ds, Db, Dr | Structural, behavioral and relevancy distances measured at the gateway. | Guide |
| RDSG | Requirements Driven Semantic Gateway: applies personas, jobs and outcomes to an issue or opportunity to generate features that close value gaps. | Owner |
| Decision API | The service that resolves SSOT rule and parameter versions and returns result, version and citation. | v5.0; SOW |
| Digital Asset | A described source (document, report, system) with owner, classification, source system and access URL. | SOW |
| Entitlement | What an authenticated person may see. Distinct from persona. | Guide |
| Persona (consumer) | An individual of core:persona that selects relevance, labels, tone and template; never grants access. | Guide; SOW |
| Gold set | SME-approved question and answer pairs used to measure accuracy before and after. | SOW |
| Grounding | Checking that each claim is supported by a cited IRI or source. | SOW |
| Parity test | A test that a target’s metric implementation returns what the SKL definition requires. | SSOT |
| SSOT | Single source of truth for vocabularies, taxonomies, ontologies, rules, constraints, logic and calculations. | SSOT |
| MTBH | Mean Time Between Hallucinations, T\_ops divided by N\_h. | v5.0; SOW |
| Competency question | A test the knowledge must pass. | SOW |
| Keel, Hull, Bridge, Ballast, Waterline, North Star | The guide’s vessel vocabulary (Addendum D.1). | Guide |
| Compass, Copilot | The Bridge capabilities: find and explain meaning; answer and act. | Guide |
| HR 360 agent | The AI agent that answers client HR questions in natural language. | Guide |
| Vee, Vizier | Vizier is the analytics platform with its own semantic layer; Vee is its AI agent. | Owner |
| Model M | The system model M = (X, Y, W, S, Δ, Λ, R), a Wymore-derived model by Wallk and Wach (2026), with the performance specification set R inside the tuple (Addendum F). Added in 6.1. | Owner |

## Addendum F. Model M lineage and the AI Circuit Breaker

Model M = (X, Y, W, S, Δ, Λ, R) is a Wymore-derived system model developed by Jeffrey Wallk and Paul Wach in 2026, not a tuple Wymore published. This addendum records its lineage and shows how the AI Circuit Breaker enforces R on every transition, which is what turns AI trustworthiness into a measured engineering quantity.

**Status.** Added in version 6.1 from TB-07b rev 2 (Wymore / Control Theory, corrected lineage). Draft until Jeffrey Wallk and Paul Wach confirm the open items in F.7.

### F.1 What this corrects

Earlier text attributed the system model to Wymore directly. Section 5 of versions 5.0 and 6.0 called it "the Wymore system model M", and the October TB-07b block said "Wymore defines a system as a 7-tuple Σ = (T, X, Ω, S, Y, Λ, δ)". That seven-element form is Zeigler's general I/O system, not a statement Wymore made. The correction separates four things that were merged: what Wymore wrote, what Zeigler built on it, what Wach and co-authors did to modernize it, and what Wallk and Wach added.

### F.2 Lineage

| Step | Source | Contribution |
| --- | --- | --- |
| 1 | Wymore, *A Mathematical Theory of Systems Engineering: The Elements* (1967) | Defines a system as a mathematical object with states, inputs, admissible input functions, a time scale and a state transition function; defines coupling and homomorphism between systems |
| 2 | Wymore, *Model-Based Systems Engineering* (1993) | Restates the discrete case as a Moore-type machine Z = (S\_Z, I\_Z, O\_Z, N\_Z, R\_Z) with next-state function N\_Z: S\_Z × I\_Z → S\_Z and readout R\_Z: S\_Z → O\_Z. Builds the Tricotyledon Theory of System Design (T3SD): six requirement types and three design spaces (functional, buildable, implementable) |
| 3 | Zeigler, DEVS and *Theory of Modeling and Simulation* | Defines the Discrete Event System Specification as a specification for a subclass of Wymore systems. Its general I/O system form is (T, X, Ω, Y, Q, Δ, Λ) |
| 4 | Wach and Salado (2019) | Tests whether Wymore's framework can underpin SysML, comparing his Moore-based state machines and system coupling with SysML state machine diagrams |
| 5 | Wach, Zeigler and Salado (2021) | Re-introduces T3SD, gives it a SysML metamodel so it can be implemented in software, and argues for conjoining it with DEVS as a scientific foundation for MBSE |
| 6 | Wallk and Wach, Model M (2026) | Extends the line from design-time theory to runtime assurance of learning-enabled and agentic systems |

In Wymore's theory the requirements sit outside the system model, and a design is judged against them at design time. That is the point Model M departs from.

### F.3 The Model M tuple

| Symbol | Meaning | Ancestry |
| --- | --- | --- |
| X | Input space | Wymore I\_Z |
| Y | Output space | Wymore O\_Z |
| W | State space | Wymore S\_Z, renamed |
| S | Admissible stimulus segments | Wymore 1967 admissible input functions; Zeigler Ω |
| Δ | State transition function | Wymore N\_Z; Zeigler Δ |
| Λ | Output function | Wymore readout R\_Z; Zeigler Λ |
| R | Performance specification set | New in the tuple: Wymore's performance requirement, moved from the external design requirement into the system definition |

Submissions and this document do not say "Wymore defines". The accurate phrasing is "Model M, a Wymore-derived system model (Wallk and Wach, 2026)".

### F.4 What Model M adds

Model M departs from the inherited theory in three ways, each traceable to the AI Circuit Breaker design specification.

1. **R is inside the system and enforced at runtime.** A transition W → W′ under Δ completes only if R is satisfied. The Circuit Breaker (Subsystem 3) is the enforcement mechanism: it trips when the intent-versus-ground-truth delta exceeds tolerance or a trust metric falls below threshold, then activates the safe state and flags the data for exclusion. Wymore checks a design against requirements once; Model M checks every transition.
2. **R is non-stationary.** Tolerances move. Predator-Prey Validation (Subsystem 7) sets Tolerance\_active(t) = Tolerance\_baseline + ε(t), with ε hidden from the agent. Cross-layer feedback tightens machine constraints when operator skill degrades (Sa 0.15 → 0.10, Cr 0.85 → 0.92). Wymore's requirements are fixed for a given design problem.
3. **The human is in the state space.** W includes the operator population's condition (the Skilled, Coupled, Dependent and Recovered compartments of Subsystem 6) and the Human Trustee's calibration (K\_trust), not only machine state. R therefore constrains the human-machine system as a whole, summarized by the System Robustness Index R\_obs.

### F.5 Model M in the AI Circuit Breaker

Every element of the tuple has a concrete instantiation in the Circuit Breaker and a measure or tolerance attached to it.

| Element | Circuit Breaker instantiation | Measure or tolerance |
| --- | --- | --- |
| X | Sensor ground truth and AI intent vectors | Rule of Ten on sensory precision (SOP-01) |
| S | Stimulus sequences admitted after the semantic handshake and Context Engine relevancy filtering (Subsystem 2) | Contextual Relevancy Index Cr > 0.85 |
| W | Knowledge layer state (Subsystem 1), breaker state, operator compartments (Subsystem 6) | Sd < 0.02/month, Dop > 0.15 |
| Δ | Transitions gated by the Veto Gate (Subsystem 3); model updates gated by the exclusion filter (Subsystem 4) | Semantic Anomaly Score Sa < 0.15; Ce < 0.25 |
| Λ | Human Trustee underwriting console and trust score (Subsystem 5) | K\_trust |
| Y | Executed actions, safe-state activations, audit records | Value-Drift Coefficient |
| R | The full tolerance set above plus MTBH, held within R\_obs ∈ \[0.70, 0.85\] | MTBH; R\_obs |

Section 5.1 assigns the same seven elements to the HSGA layers. Read together, the breaker sits at L3 with Δ and enforces the R that L5 authors. That reading is proposed here; TB-07b states the Circuit Breaker mapping only.

### F.6 Why this makes trust an engineering measurement

Placing R inside the system model closes three gaps in Wymore-grounded MBSE.

| Gap in the inherited theory | What Model M and the Circuit Breaker supply |
| --- | --- |
| Models are static and checked at design time | Runtime-certified transitions: each one completes only if R holds |
| Performance requirements have no measurement procedure | Each tolerance in R has a named measure with GUM uncertainty budgets |
| Coupling has no assurance bound | The Composition Theorem (TB-01) bounds R-satisfaction of a coupled system from its components |

The formal setting is the category **WSys**, whose objects are Model M systems and whose morphisms are pairs (f\_S, f\_W) that preserve stimulus admissibility, commute with Δ, and preserve satisfaction of R. Wymore's homomorphisms and couplings are the precedent for the first two conditions; the third is new. A certified functor F\_i at a layer boundary is then an R-preserving morphism, and the fidelity score φ(F\_i) measures how far a deployed transition is from being one.

The correspondence is a proposition, not yet a proved isomorphism. No proof is on file, and TB-07b proposes the proof as a Phase I deliverable.

### F.7 Open items to confirm

Four points from TB-07b rev 2 are unconfirmed, and this addendum stays draft until they are settled with Paul Wach.

1. **Type signatures.** Proposed: Δ: W × S → W; Λ: W → Y (Moore form, matching Wymore 1993); R a set of predicates over (W, S, W′, Y). The source documents name the elements but give no signatures.
2. **The three departures in F.4.** They are read from the design specification and the Baxter Solution Architecture v2, which do not state them as a list. Confirm they match how the authors characterize the extension.
3. **Affiliation, title and date.** How Paul Wach's affiliation and title should appear, and the date of Model M. The Baxter document carrying Model M is dated May 2026.
4. **Claims to soften or source before submission.** That the correspondence is "a formal isomorphism"; that Wymore is "the implicit mathematical substrate" of MIL-STD-881 and DoDAF; and the SEBoK v2.13 recognition.

### F.8 Attribution statement

Every submission that uses the system model carries this statement.

> The system model used here, Model M, and its runtime enforcement by the AI Circuit Breaker were developed by Jeffrey Wallk (The Value Enablement Group) and Paul Wach (University of Arizona) in 2026. Model M is derived from A. Wayne Wymore's mathematical theory of systems engineering (1967, 1993) and builds on Wach and Salado (2019) and Wach, Zeigler, and Salado (2021).

### F.9 References

- Wymore, A. W. (1967). *A Mathematical Theory of Systems Engineering: The Elements*. Wiley.
- Wymore, A. W. (1993). *Model-Based Systems Engineering*. CRC Press.
- Zeigler, B. P., Muzy, A., and Kofman, E. (2018). *Theory of Modeling and Simulation*, 3rd ed. Academic Press.
- Wach, P., and Salado, A. (2019). Can Wymore's Mathematical Framework Underpin SysML? An Initial Investigation of State Machines. *Procedia Computer Science* 153, 242–249.
- Wach, P., Zeigler, B. P., and Salado, A. (2021). Conjoining Wymore's Systems Theoretic Framework and the DEVS Modeling Formalism: Toward Scientific Foundations for MBSE. *Applied Sciences* 11(11), 4936. [doi.org/10.3390/app11114936](https://doi.org/10.3390/app11114936)
- AI Circuit Breaker: Design Specification, Comprehensive Framework with Viral Engineering Integration (Subsystems 1–7).
- Operational Framework: AI Circuit Breaker and Trustworthiness Engineering.
- TB-07b, Wymore / Control Theory, rev 2: corrected lineage, Model M (draft, November 2026).
