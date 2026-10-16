# KE Ingest

Brings legacy vocabularies, taxonomies and ontologies (Turtle) into line with the Part III standards of *Semantic Governance: Services, Architecture & Integration* v1.8 (Draft). Plain Python 3.8+, no packages to install.

```bash
python3 ke_ingest.py input/*.ttl -o output
```

Give it every file that belongs together in one run, so references between them (for example an ontology class's `dc:subject` link to its vocabulary term) are re-pointed through one crosswalk. Re-running it on its own output changes nothing, so it is safe to run again after editing the config.

## What it does

| Step | Rule |
|---|---|
| New IRIs under `https://www.insperity.com/` | §3.2 patterns: `/vocabulary/{domain}/{term}` (lower-case hyphenated), `/taxonomy/{domain}/{Concept}` and `/ontology/{domain}/{Class}` (UpperCamelCase), `/shapes/{domain}/{ClassShape}`. The domain keeps the core-/domain- tier: `vocabulary-core-asset` → `/vocabulary/core-asset/`. Every reference in every file is rewritten. |
| Labels | Sentence case, tagged `@en`, as `rdfs:label` and `skos:prefLabel`; acronyms stay only in `skos:altLabel`. |
| Definitions | Kept where present. A class without one takes the definition (and synonyms) of the vocabulary term it is linked to; otherwise the config supplies one, flagged with an editorial note for review. |
| Governance fields | Rebuilt on every asset and term: `dct:creator` (and `dct:contributor` on asset headers) is the configured author only; `dct:created` keeps the source date; `dct:modified` is the run time (UTC); `owl:versionInfo` starts at 0.1.0; lifecycle status `core:Draft`. |
| Asset headers | Generated title and description, `dct:language`, `vann:preferredNamespaceUri`, `owl:versionIRI`, a change note, and `owl:imports` for every other model the axioms refer to. The legacy title is kept as `skos:altLabel` so search still finds it. |
| Clean-up | Anything not on the allow-list is removed and counted in the report: tool bookkeeping (`oslc:modifiedBy`, `vaem:namespace`), legacy status flags (`bibo:status`, `certified`), misused annotations (`dct:subject` holding a sentence), and stub subjects that carry only bookkeeping. |
| Shapes | SHACL shapes move out of the ontology into their own shapes graph. |
| Checks | Each output is re-read (proving it is valid Turtle) and checked against the Part III rules used by the workbench's Standards Conformance tool. |

## Outputs

- `{kind}-{domain}-{version}.trig` — **load these into GraphDB.** Each holds one asset in a named graph whose IRI is the asset IRI, which is how the KE Workbench finds assets. Anything loaded into the default graph doesn't appear in Model Manager, the Model Editors or Standards Conformance.
- `{kind}-{domain}-{version}.ttl` — the same content as plain Turtle, for review and diffs (if you import a `.ttl`, set the target to *Named graph* with the asset IRI)
- `crosswalk.csv` — every legacy IRI and its new IRI and label
- `change-record-{date}.trig` / `.ttl` — a PROV-O record for the `https://www.insperity.com/graph/change-log` graph
- `ingestion-report.md` — what changed, what was removed, what was written, conformance results and modeling questions to review

## Configuration (`ke-ingest.config.json`)

Base URL, author, starting version and lifecycle status; how legacy namespaces map to kinds and domains; titles and descriptions per asset; identifier renames; definitions for terms that have none; words that keep their capitals; and modeling notes to carry into the report. Change the config rather than the script.

To stamp a specific time: `--timestamp 2026-10-15T20:55:00-05:00`.
