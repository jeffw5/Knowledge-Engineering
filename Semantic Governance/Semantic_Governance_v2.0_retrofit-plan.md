# Semantic Governance v2.0: retrofit plan from v1.9

Generated from `KE Workbench/ingest/ops_spec.py` (also shown on Operations Dashboard › Standards guide). 21 items where v1.9 no longer matches practice. The identifier and URI rules change, so the next edition is MAJOR (v2.0).

| Item | Section | Topic | Priority |
|---|---|---|---|
| G01 | §3.2 | Identifiers of classes and taxonomy concepts | high |
| G02 | §3.2 | Identifiers of individuals and instance graphs | medium, decide |
| G03 | §3.2 | URI patterns for core, areas and nested domains | high |
| G04 | §3.2, 3.11 | Named graph pattern | high |
| G05 | §3.2 | Asset titles (naming standard) | medium |
| G06 | §3.1 | Operational modules versus operational areas | high |
| G07 | §3.1, 3.7 | Primitives and polymorphic terms | high |
| G08 | §3.10 | Reference ontologies and the formalization stack | medium |
| G09 | §3.3 | Change record model | high |
| G10 | §3.3 | Deployment records and the release pipeline | medium |
| G11 | §3.3 | Versioning before 1.0.0 | low |
| G12 | §3.3, 3.4 | Lifecycle promotion criteria | high, decide |
| G13 | §3.4 | Human review and learning loop | medium |
| G14 | §3.8 | Personas and jobs to be done | high |
| G15 | §3.1, 3.9 | Service assembly model and process registry | high |
| G16 | §1.3, 2.1 | Operating model: areas, domains and the service catalog | medium |
| G17 | §Appendix E | Tooling: RDF Studio steps | medium |
| G18 | §Appendix A | Worked example | low |
| G19 | §Appendix F | Glossary | low |
| G20 | §1.2, 2.6 | Measured agent assurance | low, consider |
| G21 | §Front matter | Edition and conformance claims | high |

## G01 · §3.2 Identifiers of classes and taxonomy concepts (high)

- **v1.9 says:** Classes and taxonomy concepts use UpperCamelCase identifiers (PayrollRun, WagesAndHours); the same rule is repeated in §3.6, §3.11 and Appendix E.
- **Practice now:** Classes, taxonomy concepts and vocabulary terms join their primitives with hyphens in lower case (…/ontology/core/process-step, …/taxonomy/core-process/approval-step). Labels are spaced phrases; concatenating primitives creates new words.
- **Decided by:** Baseline Core decision 5; Workbench 3.0.0 (Baseline Core v1.0); Customer 360 schema 0.3.0
- **Change:** Rewrite the naming table: one identifier rule for classes, concepts and terms (hyphen-joined primitives, lower case); keep lowerCamelCase for properties; state the instance rule (G02). Update every example in §3.2, §3.6, §3.11, Appendix A and Appendix E.

## G02 · §3.2 Identifiers of individuals and instance graphs (medium)

- **v1.9 says:** Individuals use UpperCamelCase names or a class name plus a stable identifier (TexasMinimumWageAct, Worksite-000123); instance data lives at resource/{domain}/{Class}/{id}.
- **Practice now:** Instance IRIs are mixed: assemblies use …/resource/domain-<L1>/… with hyphenated local names; Customer 360 uses ob:Job-J01, ob:Outcome-O001 and ob:BusinessOwner; change records use resource/change-log/ChangeRecord/{stamp}-{tool}.
- **Decided by:** D17; D18; Customer 360 0.3.0; change records
- **Change:** Decide one instance rule (recommended: …/resource/{scope}/{class}/{stable-id}, class in the same hyphenated form as G01) and record the exceptions that stay for stability (identifier-coded instances such as O001).

## G03 · §3.2 URI patterns for core, areas and nested domains (high)

- **v1.9 says:** One pattern per element with the domain name in lower case (…/ontology/payroll/, …/taxonomy/compliance/), and an operational module at …/ontology/operational/.
- **Practice now:** Core assets are split by facet (…/vocabulary/core-process/, …/taxonomy/core-process/, …/ontology/core/); operational areas use …/<kind>/<area>/; domains use …/<kind>/domain-<L1>[.<L2>[.<L3>]]/ with levels joined by dots and & written "and"; the APQC registry is …/taxonomy/apqc-pcf/.
- **Decided by:** D26; Workbench 3.6.0; Workbench 3.9.0
- **Change:** Replace the URI table with the core-facet, area and dotted-domain patterns and their prefixes (salesvoc:, commercialopsvoc:), and drop the payroll and compliance examples that no longer exist.

## G04 · §3.2, 3.11 Named graph pattern (high)

- **v1.9 says:** Each artifact’s current release is held in …/graph/{artifact-type}/{domain}[/{SchemeName}].
- **Practice now:** The named graph is the asset IRI itself (…/ontology/domain-sales/); other graphs are …/graph/change-log, …/graph/customer-360/…, record and party graphs (…/record-graph/commercial-records/, …/party-graph/commercial-parties/) and one graph per assembly component.
- **Decided by:** D4; D17; Workbench 1.4.0; Workbench 4.1.0
- **Change:** Adopt "named graph = asset IRI" for models (it is what every loader and editor relies on), and list the reserved graph families for logs, records, parties, components and Customer 360.

## G05 · §3.2 Asset titles (naming standard) (medium)

- **v1.9 says:** No rule for asset titles.
- **Practice now:** Asset names take a first qualifier (Core, Domain L1.L2.L3, or the area name) and a second qualifier (Vocabulary, Taxonomy, Ontology): "Domain Sales Vocabulary", "Commercial Operations Ontology"; HR is spelled out with the short form as alternative label.
- **Decided by:** D26
- **Change:** Add the title standard next to the identifier rules.

## G06 · §3.1 Operational modules versus operational areas (high)

- **v1.9 says:** Inter-domain properties live in an operational module (…/ontology/operational/) that imports the domains it connects, with joint ownership.
- **Practice now:** Four operational areas (Business, Commercial, HR Service, Technical Operations) aggregate domains; each area has a container (D2). Classes, relations, concepts and imports refer only to the core, the area, parent domains and the domain itself; cross-area composition happens only in the enterprise service catalog (D25, D27). "Operational" now names the areas, not a module.
- **Decided by:** D2; D25; D26; D27
- **Change:** Rewrite "Operational Domains" in §3.1: areas and containers, the insulation rule, and the enterprise service catalog as the only cross-area composition point. Rename or retire "operational module" to avoid the clash, and update §1.3, §2.1 and the Human in the Loop table.

## G07 · §3.1, 3.7 Primitives and polymorphic terms (high)

- **v1.9 says:** Vocabularies hold preferred terms and synonyms; §3.11 introduces core:hasPrimaryTerm.
- **Practice now:** Vocabularies hold primitives only (unique across core and domains; multiword lexical units allowed; adjectives become their noun primitive). Concepts link to every primitive with dcterms:subject and to the head with core:hasPrimaryTerm; domains specialize core concepts with skos:broadMatch and never copy them; promotion candidates are flagged for the core.
- **Decided by:** Baseline Core decisions 1–8, 30; D6; D7; D8
- **Change:** Add a "Primitives" subsection to §3.7 with the rules, the promotion process and the build checks that enforce them.

## G08 · §3.10 Reference ontologies and the formalization stack (medium)

- **v1.9 says:** Company relations are subproperties of BFO or RO relations; taxonomies stay SKOS and reach meaning through core:formalizedBy.
- **Practice now:** Stack: BFO 2020 ← RO Core + RO extract ← core domain ontology ← area container ← domain. BFO and RO keep their own IRIs and named graphs; domain ontologies pin imports of the core and container (D3); every domain class reaches BFO through a core class (D5).
- **Decided by:** Workbench 2.1.0; Workbench 2.2.0; D3; D5
- **Change:** Add the load order and the stack diagram; state the pinned-import rule.

## G09 · §3.3 Change record model (high)

- **v1.9 says:** core:ChangeRecord with core:implementsFeature, core:changeType (KGCL), core:changeCommand, core:affectsArtifact, core:versionBump, added/removed triple graphs, core:approvedBy, core:releasedIn and a pull request link.
- **Practice now:** Every tool writes a PROV-O record: prov:Activity + dcterms:ProvenanceStatement at …/resource/change-log/ChangeRecord/{stamp}-{tool}, with dcterms:description, creator and contributor, prov:startedAtTime/endedAtTime, prov:used, prov:generated, prov:invalidated, and dcterms:hasPart entries (label, comment, dcterms:subject, dcterms:type). Approver, requirement, version bump and KGCL type are not recorded.
- **Decided by:** Workbench 1.4.0; 1.5.0; 3.1.0; build scripts
- **Change:** Make §3.3 describe the PROV-O profile that is implemented, and keep the governance fields as required extensions: core:approvedBy, core:implementsFeature (requirement), core:versionBump and core:changeType. Close the tool side with action P03/P04.

## G10 · §3.3 Deployment records and the release pipeline (medium)

- **v1.9 says:** A five-stage pipeline with release packages, a deployment log graph (core:DeploymentRecord) and nightly drift checks.
- **Practice now:** Loading is done by graphdb-load.command and graphdb-rebuild.command (backup, replace graphs, lineage check) and by the workbench’s Load into GraphDB; no deployment record is written and there is one environment.
- **Decided by:** D4; Workbench 2.2.0
- **Change:** State the current single-environment practice as stage 1 of the target pipeline, and have the load scripts write a deployment record (action P05).

## G11 · §3.3 Versioning before 1.0.0 (low)

- **v1.9 says:** MAJOR / MINOR / PATCH by schema diff.
- **Practice now:** Assets start at 0.1.0 as Draft; Conformance Review bumps PATCH for edits and MINOR before 1.0.0 (MAJOR after) for removals and new identifiers; a metadata save bumps PATCH.
- **Decided by:** Workbench 1.5.0; §3.3 (current)
- **Change:** Add the pre-1.0 rule and the bump each tool applies.

## G12 · §3.3, 3.4 Lifecycle promotion criteria (high)

- **v1.9 says:** Draft → Candidate → Released → Deprecated → Retired, mapped to environments.
- **Practice now:** Every asset is Draft; no criteria say when a Draft becomes a Candidate.
- **Decided by:** Asset inventory
- **Change:** Define Candidate entry criteria (0 conformance errors, open questions on the asset closed, SME review recorded, shapes executed) so the dashboard can report readiness.

## G13 · §3.4 Human review and learning loop (medium)

- **v1.9 says:** Human in the Loop table by artifact; quality gates by SHACL.
- **Practice now:** Conformance Review records dispositions (fix, accept, not an issue, defer, escalate) that later ingestions replay; loading is blocked by named rules (loadBlockingRules); business and compliance SMEs review Customer 360 items in GraphDB.
- **Decided by:** Workbench 2.0.0; 3.3.0; 4.1.0
- **Change:** Add dispositions, load gates and SME review to §3.4 as the implemented quality gates.

## G14 · §3.8 Personas and jobs to be done (high)

- **v1.9 says:** Persona labels via core:intendedForPersona with persona IRIs such as …/vocabulary/persona/SoftwareDeveloper.
- **Practice now:** One persona model, no role typing (Baseline 22–23); personas are assembled with jobs, job steps and desired outcomes (Baseline 16–21) in the Customer 360 ontology (jtbd:client-persona, jtbd:desired-outcome) aligned to core:persona, core:job, core:job-step; persona vocabulary is …/vocabulary/core-persona/.
- **Decided by:** Baseline Core decisions 16–23; Workbench 4.0.0
- **Change:** Split §3.8 into labels-for-personas (unchanged rule, new IRIs) and a new subsection on the persona and jobs model.

## G15 · §3.1, 3.9 Service assembly model and process registry (high)

- **v1.9 says:** No service assembly model; process steps anchor the unifying ontology.
- **Practice now:** Service › Process › Process step with SIPOCM per step (D17–D24); domain process levels are APQC PCF 7.4 (process group › process › activity › task; D28) from one reference registry with one owner per element (D29); external services follow the business model (D25).
- **Decided by:** D17–D24; D28; D29
- **Change:** Add a §3.12 "Services, processes and the reference registry".

## G16 · §1.3, 2.1 Operating model: areas, domains and the service catalog (medium)

- **v1.9 says:** Domains and the core; domain stewards; no operational areas.
- **Practice now:** Enterprise › operational area › domain (L1–L3) › services and processes; two portfolios (internal on APQC, external on the business model) in one enterprise service catalog.
- **Decided by:** D25; D26
- **Change:** Update the operating model and architecture views; add area stewardship to the RACI.

## G17 · §Appendix E Tooling: RDF Studio steps (medium)

- **v1.9 says:** Appendix E is a stepwise guide in RDF Studio.
- **Practice now:** The KE Workbench does ingestion, conformance review, editing (vocabulary, taxonomy, ontology), service assembly, Customer 360 and operations.
- **Decided by:** Workbench releases 1.4.0–4.4.0
- **Change:** Replace or supplement Appendix E with the workbench procedure (one step per tool) and keep RDF Studio as an alternative.

## G18 · §Appendix A Worked example (low)

- **v1.9 says:** FP&A example with UpperCamelCase classes and …/ontology/finance/ IRIs.
- **Practice now:** Finance is a Business Operations domain (…/ontology/domain-finance/) not yet built.
- **Decided by:** D26
- **Change:** Re-key the example to the new identifiers and URI patterns, or replace it with Domain Sales, which is built and assembled.

## G19 · §Appendix F Glossary (low)

- **v1.9 says:** Terms through v1.9.
- **Practice now:** New terms in use: primitive, polymorphic term, multiword lexical unit, operational area, container domain, bounded context, domain service, enterprise service catalog, service assembly, SIPOCM, job map stage, desired outcome, disposition, load gate, circuit breaker.
- **Decided by:** Baseline Core decisions; D-series
- **Change:** Add the entries in alphabetical order.

## G20 · §1.2, 2.6 Measured agent assurance (low)

- **v1.9 says:** Circuit breakers and human review in the agent pattern.
- **Practice now:** Proposed: reference question sets from Customer 360, measured accuracy and groundedness with uncertainty, release-level measurement records, thresholds that trip circuit breakers (PEO Service Map proposals A02–A04).
- **Decided by:** PEO Service Map expansion (Draft)
- **Change:** Add a metrology subsection once the proposals are decided.

## G21 · §Front matter Edition and conformance claims (high)

- **v1.9 says:** v1.9 Draft, 2026-10-15.
- **Practice now:** Every asset and generated file declares dcterms:conformsTo the v1.9 edition and "Standards: … v1.9" in its header.
- **Decided by:** ke-ingest.config.json conformsTo
- **Change:** Publish v2.0 (MAJOR: identifier and URI rules change), then update conformsTo in the configuration and rebuild the core and domains so assets claim the edition they meet.
