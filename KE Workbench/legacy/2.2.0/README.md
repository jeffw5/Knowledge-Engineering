# KE Workbench

One workbench for knowledge engineering. It brings the modeling tools, the SSOT for rules and logic, and the agent operations dashboards together under one overview, with a light/dark toggle. It applies the Part III standards of *Semantic Governance: Services, Architecture & Integration* v1.9 (Draft), including the §3.11 metadata field set.

## Run it

**Easiest (Mac):** double-click `start-workbench.command` in Finder. It stops any older workbench server on port 3000, starts this folder's `proxy.py` and opens http://localhost:3000/. (The first time, macOS may ask you to confirm: right-click → Open.)

**From a terminal:**

```bash
cd ~/Documents/GitHub/Knowledge-Engineering/"KE Workbench"
python3 proxy.py            # GraphDB on http://localhost:7200
# open http://localhost:3000/
```

Always open the workbench through `http://localhost:3000/`, never by double-clicking `index.html` (a `file://` page can't reach GraphDB). `proxy.py` serves the folder it sits in and prints that folder when it starts; it tells the browser not to cache the pages, so an updated tool shows up on the next reload. If it reports that port 3000 is in use, an older proxy is still running: `lsof -ti tcp:3000 | xargs kill`. It listens on this computer only; start it with `HOST=0.0.0.0` to share it on your network. To point it at another GraphDB, set `GRAPHDB_URL=http://host:7200` and/or `PORT=3000`.

The Overview shows the workbench release (currently **2.2.0**); click it, or open *Reference › Release Notes*, for the change log. To record a release, add an entry at the top of `assets/ke-releases.js` and bump `version` in `assets/ke-registry.js`.

Without GraphDB, the static tools still work: SSOT, dashboards, personas, HSGA, and Standards Conformance in Turtle-file mode. The pill in the top bar shows the connection.

## Layout

| Path | What |
|---|---|
| `start-workbench.command` | Double-click launcher (Mac) |
| `tools/release-notes.html`, `assets/ke-releases.js` | Release Notes page and the release history it shows |
| `index.html` | Workbench shell: grouped navigation, tabs that keep their state, GraphDB status, settings, light/dark |
| `tools/workbench-overview.html` | Overview: live asset counts, tool map, §1.3 function mapping, Part III quick reference, E.3 checklist |
| `tools/standards-conformance.html` | **New.** Checks GraphDB graphs or a Turtle file against the Part III / Appendix E standards |
| `tools/*.html` | Your existing tools, renamed (see below) |
| `assets/ke-theme.css` | Design tokens taken from the guide (Liberation Sans, ink `#1F2933`, accent `#2F6DB5`, band `#EEF3F9`, rule `#D5DBE1`, draft red `#B03A2E`), plus a dark theme |
| `assets/ke-bridge.js` | Loaded by every tool: theme sync, `window.open`/`window.close`/`_blank` links become workbench tabs, shared repository ID |
| `assets/ke-registry.js` | The tool list used by the shell and the overview — add new tools here |
| `tools/model-editor-taxonomy.html`, `tools/model-editor-ontology.html` | **New.** The two simplified Model Editors (see below) |
| `assets/ke-sparql.js` | SPARQL helpers shared by the Model Editors (all calls go through the proxy) |
| `assets/ke-turtle.js`, `ke-rules.js`, `ke-sample.js` | Turtle parser, conformance rules, sample file |
| `docs/` | The standards guide (PDF) |
| `legacy/` | Superseded versions kept for reference (`operational_dashboard.html`, `model-metadata.html`) |

## What changed in your tools

- **All tools:** the bridge script and a small theme adapter were added. The adapters map each page's colors onto the shared tokens, so every tool follows the workbench light/dark toggle. Each page still works on its own, outside the workbench.
- **Model Manager:** restyled to match the workbench; each asset is listed once (it used to repeat when an asset had several labels or matched in more than one graph), with counts per tab and a filter. The compliant base URLs are now a setting (gear: GraphDB pill → *Compliant base URLs*). The default is `https://www.insperity.com/` (§3.2) plus the legacy `https://www.enablingvalue.com/`. The Create-new template follows the URI pattern. Slash-terminated IRIs now show their last segment.
- **OWL / SKOS / Taxonomy metadata editors:** `owl:versionInfo` uses semantic versioning (§3.3). A metadata save bumps PATCH, a new asset starts at `0.1.0`, and legacy `1.3` becomes `1.3.1`.
- **Visualizer:** labels follow the theme; `insperity.com` has its own color.
- **SSOT Rules Map / Agent & Service Map:** links to the hosted SSOT Editor open the local copy as a tab. URLs written into downloadable packages are unchanged.
- **Tailwind CDN** is pinned to 3.4.17.

## Model Editors

The classic `model-editor.html` is replaced in the navigation by two focused editors. It is still in `tools/` (hidden from the nav).

**Model Editor (Taxonomy)** — choose a taxonomy (any asset whose IRI contains "taxonomy"; tick *all* to see every scheme and ontology). It works with both kinds of taxonomy in the repository:
- **SKOS taxonomies** (`skos:ConceptScheme`, the only kind from 2.0.0 on): `skos:inScheme`, `skos:broader`/`skos:narrower`, `skos:topConceptOf`/`skos:hasTopConcept`. A vocabulary term dropped in reuses the concept already linked to it (`core:hasPrimaryTerm`, `dcterms:subject` or legacy `dc:subject`) or a concept with the same label; otherwise a new concept is created in the taxonomy's namespace, named from the label in UpperCamelCase, with the label, the vocabulary term's definition, `core:hasPrimaryTerm` and `dcterms:subject` pointing back to the vocabulary term. The vocabulary term itself never joins the taxonomy's scheme.
- **OWL taxonomies** (`owl:Ontology` with `owl:Class` terms, from before 2.0.0; re-ingest to convert them): members are classes with `rdfs:isDefinedBy` the taxonomy, in its named graph, or in its namespace; broader/narrower is `rdfs:subClassOf`. New classes are linked the same way, with `core:hasPrimaryTerm` and `dcterms:subject`.

Pick a vocabulary on the left and select terms (Ctrl/⌘-click, Shift-click, *All*). Dragging uses the mouse directly (press, move, release); a label follows the pointer and the drop target is highlighted.
- Drop **on** a term: the dragged terms become its narrower terms (moving them from their old place).
- Drop on the **top edge** of a term: the dragged term becomes its broader term and takes its place.
- Drop on the dashed zone: top level. Hold **Alt/⌥** to add a second broader term instead of moving. Delete removes a term from the taxonomy (its children move up; for an OWL taxonomy the class's statements are deleted after a confirmation).
- Changes are pending until **Save**. They are written to the taxonomy's named graph, or to the default graph when it has none. Undo with Ctrl/⌘-Z; moves that would create a cycle are refused.

**Model Editor (Ontology)** — choose the ontology to edit: its class hierarchy is drawn on the canvas as a left-to-right tree (each class under its most specific parent; *is a* lines implied by another *is a* are not drawn, but the triples are untouched and the Inspector lists them all). It and its `owl:imports` load on the left automatically, and you can tick any other ontology, taxonomy or vocabulary.
- Drag single terms from the Terms list, or drag a **whole model** from the Models list, onto the canvas — a model is placed as its own hierarchy where you drop it. *Show ontology* redraws the edited ontology (Undo restores the previous canvas).
- Drag from a node's **+** handle to another node and pick a relation.
- The relation list is every `owl:ObjectProperty` with an `obo:BFO_` or `obo:RO_` IRI in the repository (BFO plus the RO core relations; deprecated ones are hidden), or the properties of another ontology chosen in ⚙. It is ordered by `rdfs:subPropertyOf`, with definitions from `IAO:0000115`. *is a* (`rdfs:subClassOf`) is always available. If BFO isn't in the repository, *Load BFO 2020* asks GraphDB to load it.
- Classes are related with `rdfs:subClassOf [ owl:onProperty R ; owl:someValuesFrom B ]` by default; *only (∀)* and *direct triple* (for concepts) are also offered.
- Relations whose subject belongs to the ontology (`rdfs:isDefinedBy` or its named graph) are drawn when both ends are on the canvas (*Show relations* places them). On Save, terms from other models get an `owl:imports` for their model (switch off in ⚙). The canvas layout is remembered per ontology in the browser.

## Not included

Model Manager links to `voc-editor.html`, which wasn't among the source files (its Taxonomy button now opens the Taxonomy Model Editor). The workbench shows a placeholder tab for them. Drop the files into `tools/` and they'll open normally.

## Standards Conformance rules

Base URL · URI pattern · identifier case · no acronyms in identifiers · no acronyms in preferred labels · label present with `@en` · sentence-case labels · definition present · genus + differentia · named parent class · `rdfs:isDefinedBy` · property domain and range · restricted OWL constructs · concept in scheme with one prefLabel · no version in term IRIs · semantic version (and version IRI) on releases · one scheme per taxonomy with top concepts flagged · no other organization's content · no broken references · taxonomy term in a vocabulary · primary vocabulary term · taxonomies stay in SKOS · asset header fields (§3.11) · valid dates. Approved acronyms come from the ingestion configuration.

## Ingestion (1.4.0)

**Model & standards › Ingestion** brings vocabularies, taxonomies and ontologies into the Part III standard.

1. **Source folder**: Browse or type a folder, then Scan. Turtle (`.ttl`), N-Triples (`.nt`) and RDF/XML (`.rdf`, `.rdfs`, `.owl`, `.xml`) files are read; each must hold one `owl:Ontology` or `skos:ConceptScheme`. Files that can't be ingested are listed with the reason. Tick *Include subfolders* to go deeper.
2. **Destination folder**: Turtle goes to `ttl/` and TriG to `trig/` (rename either). The preview shows which files a run would replace.
3. **Metadata**: author and editor, starting version, lifecycle status and modified date-time for this run. *Edit configuration…* opens `ingest/ke-ingest.config.json` (namespace rules, titles, descriptions, renames, definitions); saving keeps the previous version as `.bak`.
4. **Ingest**: writes one `.ttl` and one `.trig` per asset (shapes get their own), a change record in both formats for `https://www.insperity.com/graph/change-log`, `crosswalk.csv` and `ingestion-report-{date-time}.md`. **Load into GraphDB…** replaces each asset's named graph and appends the change record.

The page talks to `proxy.py` at `/api/ingest/` (code in `ingest/ingest_api.py`), so restart the workbench server after updating. The same ingester runs from a terminal:

```bash
python3 ingest/ke_ingest.py ~/path/to/legacy -o ~/path/to/ingested            # ttl/ and trig/
python3 ingest/ke_ingest.py ~/path/to/legacy -r -o out --ttl-dir turtle --trig-dir graphs
```

## Conformance Review (1.5.0)

**Model & standards › Conformance Review** is the human-in-the-loop page for what the ingester leaves behind.

1. Choose the **Source**. *Ingested files* reads the `.ttl` files an ingestion run wrote, before they are loaded (on the Ingestion page, **Review ›** next to a file with errors, or **Review files with errors…**, opens them here). *GraphDB* reads models that are already loaded. Tick the files or models and click **Find issues**; the page runs the Standards Conformance rules.
2. Work through the categories: *Other organization's content*, *Acronyms*, *Broken and foreign references*, *Missing definitions*, *Other*. Terms are grouped by model, or by namespace for terms from other namespaces.
3. Select a term to see it in context and fix it: preferred label, definition (or the model's description), alternative labels, broken links, identifier, or removal (the removal plan shows what happens to children, links, restrictions and lists). Tick several terms, or a whole group, to stage suggestions or removals in bulk.
4. **Approve** an acronym or tick **Remember the expansion** to add it to `ingest/ke-ingest.config.json`, so later ingestions use it.
5. **Review changes**, then **Save to files** or **Apply to GraphDB**. With files, finish with **Load into GraphDB…**: every current model in the folder replaces its named graph and the change records go to the change log. Older copies from earlier runs are set aside in `superseded/` automatically, so there is nothing to move by hand. Saving to files rewrites each `.ttl` and its `.trig` twin (originals copied to `review-backup-<date-time>/`), and adds the corrections to the run's change record, so **Load into GraphDB** on the Ingestion page takes them along. Applying to GraphDB gives each model gets a new version (patch for edits; minor before 1.0.0, major after, for removals and new identifiers), `dct:modified`, a `skos:changeNote`, and records the change set in `https://www.insperity.com/graph/change-log`.

The ingester's automatic rules (1.5.0) come from the configuration: `acronyms.approved`, `acronyms.expansions` and `organizations` (name, regex patterns, `removeTerms`, `replacement`). Restart `proxy.py` after updating, since the page reads `/api/ingest/policy`.

## Model Editor (Vocabulary) (1.7.0)

**Model & standards › Model Editor (Vocabulary)** edits the ingested vocabulary files directly.

1. The folder defaults to the last ingestion destination (`…/ttl`); pick a vocabulary on the left.
2. **Vocabulary metadata**: click the vocabulary at the top of the term list — title (kept in `skos:prefLabel`, `rdfs:label` and `dct:title`), alternative labels, description, version, lifecycle status, creator, contributor, language, editorial note.
3. **Terms**: select one in the tree (or find it, or tick *Only terms with errors*) — labels, identifier, definition, scope note, example, editorial note, broader terms, top concept, related terms, status, version. **+ New term** adds one under the selected term; **Remove** moves its narrower terms up.
4. **Save & load into GraphDB** (or Cmd/Ctrl+S) rewrites the `.ttl` and `.trig`, backs up the originals, adds a change note and a change record, and loads the folder into GraphDB. **Save files only** skips the load.

Conformance Review's **Save & load into GraphDB** does the same for its corrections, and its **Edit in Model Editor (Vocabulary)** button opens the selected term here.

## Taxonomy terms in vocabularies (1.8.0)

Every taxonomy term must name its vocabulary term, and that term must exist in a vocabulary — reported as an error. From 2.0.0 the link is `core:hasPrimaryTerm` plus `dcterms:subject` (§3.11); `dc:subject` is still read.

- **Ingestion** links a term automatically when its preferred or alternative label matches a vocabulary term (this run's vocabularies, then the ones already in the destination; the same-domain vocabulary wins). Unmatched terms are reported.
- **Conformance Review › Not in a vocabulary**: *Link* a matching term, search for another, or *Add to vocabulary* (choose the vocabulary and the broader term). Tick several terms to add them in one go; parents are added first, so the hierarchy carries over. **Save & load into GraphDB** writes both files and loads them.

## Duplicates and generated definitions (1.9.0)

- **Duplicates**: when several source files describe the same asset, Ingestion uses the largest (most terms; set `"duplicates": "largest-file"` in the configuration to compare bytes instead) and lists the others as skipped.
- **Shared namespaces**: a header such as `…/taxonomy/core/IssueTaxonomy` becomes its own asset, `…/taxonomy/core-issue/`.
- **Definitions written by Claude**: create `~/.ke-workbench.env` with one line, `ANTHROPIC_API_KEY=sk-ant-…`. Then tick *Write missing definitions with Claude* on the Ingestion page, or use **✦ Write with Claude** in Conformance Review (one term, or several under *Missing definitions*) and in the Model Editor (Vocabulary). Every generated definition carries an editorial note asking for review before the term moves to Candidate. `"definitionModel"` in the configuration picks the model.

## Semantic Governance v1.9 (2.0.0)

A MAJOR release: what ingestion writes changes in ways that break consumers of 1.x output, so re-ingest your sources and load the new files.

- **Taxonomies are SKOS.** A taxonomy authored as OWL classes is converted (`owl:Class` → `skos:Concept`, `rdfs:subClassOf` → `skos:broader`). `"taxonomiesAsSkos": false` keeps the old behavior.
- **Taxonomy concept IRIs are UpperCamelCase** (`…/taxonomy/core-process/ApprovalStep`); vocabulary terms stay hyphenated. `crosswalk.csv` maps old IRIs to new ones.
- **Links to vocabulary terms** are `core:hasPrimaryTerm` and `dcterms:subject`. `dcterms:source` on each taxonomy lists the vocabularies it draws on.
- **§3.11 header fields** on every asset: `vaem:namespace` (replaces `vann:preferredNamespaceUri`), `vann:preferredNamespacePrefix`, `owl:versionIRI`, `dcterms:publisher`, `dcterms:conformsTo`, `dcterms:subject`. Set them in the configuration: `publisher`, `conformsTo`, `ontologyConformsTo`, `defaultSubject` (or `"subject"` per asset under `assets`), and optionally `authorIri`.
- **Dates** keep their type: a date alone is `xsd:date`.
- **Numbered labels** move the number to `skos:notation`; `&` in a preferred label becomes "and".
- **Loading into GraphDB is blocked** while a file has terms outside the base URL, another organization's content or an invalid date (`"loadBlockingRules"` lists the rule names; `[]` turns the gate off). *Load into GraphDB…* lists the errors and offers *Load anyway*.
- The 1.9.0 copies of every file this release changed are in `legacy/1.9.0/`.

## BFO as the top-level ontology (2.1.0)

BFO 2020 (ISO/IEC 21838-2) is the top-level ontology the core domain ontology is aligned to; the RO Core relations are anchored to it (§3.10). Neither is ingested: both keep their own IRIs.

- **Ingestion › Reference ontologies** loads them into GraphDB, each into its own named graph (`http://purl.obolibrary.org/obo/bfo.owl`, `http://purl.obolibrary.org/obo/ro/core.owl`). Give a URL (defaults: the OBO addresses) or the path of a downloaded file. The workbench fetches the file and reads its format, so GraphDB needs no internet access.
- Only the core domain ontology ties into BFO: its classes have BFO parents and its relations are subproperties of BFO or RO relations. Vocabularies and taxonomies reach BFO through `core:formalizedBy` to a core class; they carry no BFO links of their own.
- **Model Editor (Ontology)** no longer has a Load BFO button; with BFO loaded, tick it in the Models list and draw *is a* from a core class to a BFO class.

## Core domain ontology (2.2.0)

The core domain ontology is authored in `ingest/core/ontology-core.source.ttl` and its shapes in `ingest/core/shapes-core.source.ttl`. Build them into `KE Baseline/Baseline Core v1.0` with

    python3 ingest/build_core.py            # --out "../KE Baseline/Baseline Core v1.0" by default; --no-taxonomies to leave the taxonomies alone

The build adds labels, rdfs:isDefinedBy, governance and §3.11 header fields, runs the Part III checks and a lineage check, and writes `core:formalizedBy` into the core taxonomies from `ingest/core/formalized-by.csv` (rows without a core class are listed for review).

Stack: BFO 2020 ← RO Core + RO extract ← core domain ontology (`/ontology/core/`) ← domain ontologies. Taxonomy concepts point up with `core:formalizedBy`; ontology classes name their vocabulary term with `core:hasPrimaryTerm`.

Load order in GraphDB: Ingestion › Reference ontologies › Load all three (BFO, RO Core, `reference/ro-extract.ttl`), then the Baseline Core v1.0 files; or run `KE Baseline/Baseline Core v1.0/graphdb-rebuild.command`, which backs up, clears and reloads the repository in that order and checks lineage. Older runs and files are in `KE Baseline/Archive Baseline Core v0.1/`.

