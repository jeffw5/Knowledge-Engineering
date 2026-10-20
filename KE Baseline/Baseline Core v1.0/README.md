# Baseline Core v1.0

The clean, ingestable set of Insperity core semantic assets (Semantic Governance v1.9, Part III).
Older ingestion runs, reports, review backups, superseded files and GraphDB backups are in `../Archive Baseline Core v0.1/`.

## Load into GraphDB

Double-click `graphdb-rebuild.command` (or run it with the repository ID: `./graphdb-rebuild.command value-kb`).
It backs up the repository into the archive folder, asks you to type the repository name, clears it, then loads:

1. `reference/bfo-core.ttl`: BFO 2020 core, ISO/IEC 21838-2 (graph `http://purl.obolibrary.org/obo/bfo.owl`)
2. `reference/ro-core.owl`: RO Core, release 2024-04-24 (graph `http://purl.obolibrary.org/obo/ro/core.owl`)
3. `reference/ro-extract.ttl`: the BFO, RO and IAO relations the core ontology uses that BFO and RO Core lack (graph `https://www.insperity.com/reference/ro-extract/`)
4. `trig/vocabulary-core-*`: core vocabularies (the primitives)
5. `trig/taxonomy-core-*`: core taxonomies, built on the vocabularies; top concepts carry `core:formalizedBy`
6. `trig/ontology-core-*`: core domain ontology (`https://www.insperity.com/ontology/core/`), every class under BFO and every relation under BFO/RO/IAO
7. `trig/shapes-core-*`: SHACL shapes that keep data anchored on the process step

It then runs the lineage checks. `ttl/` holds the same assets as plain Turtle, for review and for the KE Workbench.

## Contents

**vocabulary** (25)

- `vocabulary-core-asset-0.1.0`: Core asset vocabulary
- `vocabulary-core-capability-0.1.0`: Core capability vocabulary
- `vocabulary-core-compliance-0.1.0`: Core compliance vocabulary
- `vocabulary-core-decision-0.1.0`: Core decision vocabulary
- `vocabulary-core-domain-0.1.0`: Core domain vocabulary
- `vocabulary-core-event-0.1.0`: Core event vocabulary
- `vocabulary-core-governance-0.1.0`: Core governance vocabulary
- `vocabulary-core-issue-0.1.0`: Core issue vocabulary
- `vocabulary-core-job-0.1.0`: Core job vocabulary
- `vocabulary-core-lifecycle-0.1.0`: Core lifecycle vocabulary
- `vocabulary-core-location-0.1.0`: Core location vocabulary
- `vocabulary-core-logic-0.1.0`: Core logic vocabulary
- `vocabulary-core-measure-0.1.0`: Core measure vocabulary
- `vocabulary-core-party-0.1.0`: Core party vocabulary
- `vocabulary-core-persona-0.1.0`: Core persona vocabulary
- `vocabulary-core-policy-0.1.0`: Core policy vocabulary
- `vocabulary-core-process-0.1.0`: Core process vocabulary
- `vocabulary-core-product-0.1.0`: Core product vocabulary
- `vocabulary-core-requirements-0.1.0`: Core requirements vocabulary
- `vocabulary-core-role-0.1.0`: Core role vocabulary
- `vocabulary-core-rules-0.1.0`: Core rules vocabulary
- `vocabulary-core-services-0.1.0`: Core services vocabulary
- `vocabulary-core-time-0.1.0`: Core time vocabulary
- `vocabulary-core-value-0.1.0`: Core value vocabulary
- `vocabulary-core-valuestream-0.1.0`: Core valuestream vocabulary

**taxonomy** (23)

- `taxonomy-core-asset-0.1.0`: Core asset taxonomy
- `taxonomy-core-capability-0.1.0`: Core capability taxonomy
- `taxonomy-core-compliance-0.1.0`: Core compliance taxonomy
- `taxonomy-core-decision-0.1.0`: Core decision taxonomy
- `taxonomy-core-event-0.1.0`: Core event taxonomy
- `taxonomy-core-governance-0.1.0`: Core governance taxonomy
- `taxonomy-core-issue-0.1.0`: Core issue taxonomy
- `taxonomy-core-job-0.1.0`: Core job taxonomy
- `taxonomy-core-lifecycle-0.1.0`: Core lifecycle taxonomy
- `taxonomy-core-location-0.1.0`: Core location taxonomy
- `taxonomy-core-logic-0.1.0`: Core logic taxonomy
- `taxonomy-core-measure-0.1.0`: Core measure taxonomy
- `taxonomy-core-party-0.1.0`: Core party taxonomy
- `taxonomy-core-persona-0.1.0`: Core persona taxonomy
- `taxonomy-core-policy-0.1.0`: Core policy taxonomy
- `taxonomy-core-process-0.1.0`: Core process taxonomy
- `taxonomy-core-product-0.1.0`: Core product taxonomy
- `taxonomy-core-requirements-0.1.0`: Core requirements taxonomy
- `taxonomy-core-role-0.1.0`: Core role taxonomy
- `taxonomy-core-rules-0.1.0`: Core rules taxonomy
- `taxonomy-core-services-0.1.0`: Core services taxonomy
- `taxonomy-core-time-0.1.0`: Core time taxonomy
- `taxonomy-core-value-0.1.0`: Core value taxonomy

**ontology** (1)

- `ontology-core-0.1.0`: Core domain ontology

**shapes** (1)

- `shapes-core-0.1.0`: Core domain shapes

## How the set is built

- **Vocabularies** hold primitives: unique, irreducible terms (decisions 1-3, 6). 367 primitives were added on 2026-10-19 (`review/primitives-added.txt`, source `review/primitives-v1.tsv`), with seven new vocabularies: decision, governance, job, logic, measure, policy and value.
- **Taxonomies** are built on the vocabularies: every concept carries `dcterms:subject` to each primitive it is built from and `core:hasPrimaryTerm` to the head primitive (decision 4). `review/concept-links.csv` lists every concept with its primitives. Top concepts point to the core domain ontology with `core:formalizedBy`.
- **Identifiers** join words with hyphens (decision 5): `…/taxonomy/core-process/approval-step`, `…/ontology/core/process-step`. `review/crosswalk-v1.csv` maps every old IRI to its new one (or notes its removal).
- **Core domain ontology**: every class reaches BFO 2020, every relation reaches BFO/RO/IAO. Asset is the genus; product, service, offering and platform are assets assembled from other assets; the Jobs model (job, job step, desired and delivered outcome) meets the process model through *addresses*.
- **Design decisions** are recorded in `review/design-decisions.md`.
- **Audit log**: `ttl/` and `trig/` also hold the PROV-O change records (`change-record-*`) for the changes made on 2026-10-19 outside the workbench. They load into the append-only graph `…/graph/change-log`; the rebuild script keeps that graph across a clear and adds them.

## Open items

- Eight taxonomy top concepts wait on a modeling decision (financial asset, intangible asset, six value concepts); the rebuild's lineage check reports them.
- Ten links point to `vocabulary/domain-finance/` terms (revenue, budget, prepayment, cash, cash equivalent, receivable, investment), which belong to the finance domain and are not part of the core set; three of them are flagged by the conformance check until a domain-finance vocabulary is loaded.
- The selling process (discover, qualify, evaluate, propose, decide, onboard) is not yet in the process taxonomy.
- Some existing vocabulary terms are still polymorphic or duplicated (for example data quality management, event / events, requirement / requirements, product development and the lifecycle stage develop); they are listed for a later clean-up.

## 2026-10-20: core taxonomies imported

The core domain ontology now imports the 23 core taxonomies (`owl:imports`), so it includes every core taxonomy and its concepts. Nothing else changed; the version stays 0.1.0 (Draft). Change record: `ttl/change-record-2026-10-20T121500Z.ttl` (and `.trig`); `graphdb-rebuild.command` loads it with the others. The previous ontology files are in `Archive Baseline Core v0.1/pre-taxonomy-imports-2026-10-20/`.
