/* KE Workbench — release history (newest first). Shown on the Release Notes page.
   Add a new entry at the top for every release and bump `version` in ke-registry.js to match. */
window.KE_RELEASES = [
  {
    version: '3.1.0', date: '2026-10-19', title: 'Model Editor (Ontology): imported relations, domain ontologies, Force and List views',
    groups: [
      { kind: 'new', items: [
        'Relations of every loaded model, in three tiers: primary (the ontology being edited — editable), secondary (its imports and any model you tick or drag in) and tertiary (the imports of those). Secondary and tertiary relations are read-only and drawn lighter (solid grey, then dotted); the toolbar toggles each tier. Hover a line, or select it, to see which model states it; the Inspector lists a term\u2019s own relations and those stated elsewhere, and offers to open the model that states one.',
        'New ontology…: creates a domain ontology (version 0.1.0, Draft, with the core domain ontology\u2019s header fields) that imports the core domain ontology and any taxonomies and vocabularies you pick, writes a change record to the audit log and opens it.',
        'New class…: adds a class to the ontology being edited, with a hyphen-joined IRI in its namespace, a definition, its parent class (is a), its primary term (core:hasPrimaryTerm and dcterms:subject) and other primitives. On a vocabulary term or taxonomy concept, New class from this term… builds the class from that primitive, or records that the concept is formalized by the new class.',
        '+ import / − import on each model in the Models list: owl:imports changes are pending until Save, and the imported model\u2019s relations appear as secondary straight away.',
        'Force view: a force-directed layout of the terms on the diagram, with springs along the shown relations. Dragged terms stay pinned; Re-run unpins them. Tree restores the tree layout.',
        'List view: every shown relation as a sortable table (subject, relation, object, stated in, tier), grouped by model, or every loaded class and term with its parents and number of relations. Click a row to inspect it; double-click to put it on the diagram.',
        'The relation picker offers each loaded ontology\u2019s own relations (core domain ontology first), the links to primitives and concepts (formalized by, has primary term, subject, related, exact and close match) and the BFO and RO relations, grouped.',
        'Every save writes a PROV-O change record to the audit log (…/graph/change-log) listing the classes, relations and imports added or removed, and updates dct:modified on the ontology.'
      ]},
      { kind: 'improved', items: [
        'Show ontology also places the classes outside the ontology that its classes specialize (for the core domain ontology, the BFO classes), so the lineage to the imported models is visible.',
        'Deleting a relation removes it only from the edited ontology\u2019s own graph; the same triple stated in a taxonomy or another ontology is left alone.'
      ]},
      { kind: 'fixed', items: [
        'Dragging an ontology onto the canvas of another (for example the core domain ontology onto core.owl) placed its classes but none of its relations.'
      ]}
    ]
  },
  {
    version: '3.0.0', date: '2026-10-19', title: 'Baseline Core v1.0: primitives, hyphen-joined identifiers and the Jobs model',
    groups: [
      { kind: 'breaking', items: [
        'Identifiers join words with hyphens: classes, taxonomy concepts and vocabulary terms are lower-case words joined by hyphens (…/taxonomy/core-process/approval-step, …/ontology/core/process-step), so a polymorphic term stays a phrase and never becomes a new word (§3.2 as amended). Ingestion mints identifiers this way, the Part III checks and the browser rules expect it, Conformance Review proposes it and Model Editor (Taxonomy) creates it. KE Baseline/Baseline Core v1.0/review/crosswalk-v1.csv maps every old IRI to its new one.',
        'KE Baseline is now Baseline Core v1.0 (the ingestable set) and Archive Baseline Core v0.1 (everything earlier). Ingestion, Reference ontologies and build_core.py point at Baseline Core v1.0.'
      ]},
      { kind: 'new', items: [
        'Primitives: 367 primitives added to the core vocabularies after a term-by-term review, and seven new core vocabularies (decision, governance, job, logic, measure, policy, value). Every one of the 922 taxonomy concepts is linked to the primitives it is built from (dcterms:subject) and to its head primitive (core:hasPrimaryTerm).',
        'Core job taxonomy and the Jobs model in the core domain ontology: job, job step, desired outcome and delivered outcome; personas perform jobs; process steps address job steps (intentionally not one-to-one), so value gaps can be measured.',
        'Core domain ontology rebuilt to the asset model: asset is the genus; product, service, offering and platform are assets assembled from other assets (has component); every asset has a lifecycle; delivery of, delivers, supports and addresses added. 36 classes, all under BFO 2020; every relation under BFO, RO or IAO, an inverse, or a property chain.',
        'Shapes for jobs, job steps, desired and delivered outcomes and assets (lifecycle); performed by accepts a party (manual) or a digital agent (automated).',
        'RO extract 0.2.0 adds causally upstream of, the parent of addresses and supports.',
        'graphdb-rebuild.command in Baseline Core v1.0: backs up, clears and reloads a repository in dependency order, then checks lineage. The audit log (…/graph/change-log) is append-only: it is saved before the clear, put back after it, and the change records in trig/ are added to it.',
        'Audit log: five PROV-O change records for the changes made outside the workbench on 2026-10-19, in Baseline Core v1.0/ttl and trig (change-record-*): core domain ontology rebuilt on BFO (2.2.0); other organization\'s content removed; KE Baseline split into Baseline Core v1.0 and Archive Baseline Core v0.1; primitives backfill, hyphen-joined identifiers and relinking; core domain ontology rebuilt to the asset and Jobs model. Each names the assets it used, generated or superseded and says it was recorded retrospectively. ingest/migrate_v1/change_records.py writes them.'
      ]},
      { kind: 'improved', items: [
        'Personas are no longer typed by role (the engineering persona types and persona role are removed); product terms no longer carry the marketing lifecycle stages; Verizon content removed from the core set.'
      ]},
      { kind: 'fixed', items: [
        'Model Editor (Vocabulary), Conformance Review and Ingestion failed with "…/KE Baseline/ttl is not a folder": the browser still remembered the folder from before the move to Baseline Core v1.0. A remembered folder that no longer exists now falls back to the current destination (Baseline Core v1.0).',
        'Model Editor (Ontology) showed no relations for the rebuilt core domain ontology: it restored the layout saved for the same ontology IRI before the identifiers changed, so it placed boxes for terms that no longer exist (ProcessStep) and none of the current ones (process-step). A saved layout is now dropped when most of its terms are gone, and the class hierarchy is laid out afresh.',
        'Model Editor (Ontology) labels relations from any ontology by their rdfs:label (has role, is step of), not only BFO and RO relations; core relations showed as camelCase local names.'
      ]}
    ]
  },
  {
    version: '2.2.0', date: '2026-10-19', title: 'Core domain ontology on BFO, anchored on the process step',
    groups: [
      { kind: 'breaking', items: [
        'The core domain ontology moves to https://www.insperity.com/ontology/core/ (prefix core:, file ontology-core-<version>), the namespace its governance properties (core:hasLifecycleStatus, core:hasPrimaryTerm, core:formalizedBy) already used. It replaces …/ontology/core-domain/ and the five core-* shapes graphs (compliance, domain, party, process, product), which targeted legacy IRIs; their files are in KE Baseline/superseded/2026-10-19-core-rebuild. Drop the old graphs in GraphDB with KE Baseline/graphdb-drop-superseded-core.rq.'
      ]},
      { kind: 'new', items: [
        'Core domain ontology 0.1.0: 35 classes, each a subclass of a BFO 2020 class (process, process boundary, material entity, object, object aggregate, site, temporal region, role, disposition, generically dependent continuant), and 28 relations, each a subproperty of a BFO, RO or IAO relation (or the inverse of one). Event is a process boundary; an asset is anything that bears an asset role.',
        'The process step is the anchor (§3.1): it carries class restrictions to party, role, capability, directive, measure, issue, event, location and time, so Model Editor (Ontology) › Show relations draws the unifying design.',
        'Core domain shapes (…/shapes/core/): a step must belong to a process (violation); events, directives, measures and issues not tied to a step, and steps with no performer, are warnings.',
        'core:formalizedBy on the top concepts of all 22 core taxonomies (96 links): the path from each taxonomy to BFO. Eight concepts are left for a modeling decision (financial and intangible assets, six value concepts).',
        'RO extract (reference/ro-extract.ttl): the BFO 2020 relations the OBO bfo.owl lacks, has input and has output from RO, and is about from IAO. Ingestion › Reference ontologies has a third row for it, and Load all three.',
        'KE Baseline is split in two: Baseline Core v1.0 holds only the ingestable set (vocabularies, taxonomies, core domain ontology, shapes, and BFO 2020, RO Core and the RO extract under reference/), with graphdb-rebuild.command to back up, clear and reload a repository in dependency order and check lineage; everything else is in Archive Baseline Core v0.1. Ingestion, its Reference ontologies defaults and build_core.py point at the new folder.',
        'Verizon content removed from the core set (foreign individuals in the compliance taxonomy, Verizon organization units, Hum); 0 blocking conformance errors.',
        'ingest/build_core.py builds the ontology and shapes from their authored sources in ingest/core/, adds labels and governance fields, runs the Part III checks and a lineage check (every class reaches BFO, every relation reaches BFO/RO), and writes core:formalizedBy into the taxonomies from ingest/core/formalized-by.csv.'
      ]}
    ]
  },
  {
    version: '2.1.0', date: '2026-10-17', title: 'BFO as the top-level ontology',
    groups: [
      { kind: 'new', items: [
        'Ingestion: Reference ontologies. Load BFO 2020 (ISO/IEC 21838-2) and the RO Core relations into GraphDB from a URL or from a downloaded file, each into its own named graph (…/obo/bfo.owl and …/obo/ro/core.owl, replaced on every load). The workbench downloads the file itself and reads its format, so GraphDB needs no internet access and never mistakes RDF/XML for Turtle.',
        'Reference ontologies keep their own IRIs and are never ingested: a BFO, RO or other OBO file given to Ingestion is skipped with a message that points to Reference ontologies on the same page, instead of "matches no sourceNamespaces pattern".',
        'New server endpoint POST /api/ingest/load-url {url | path, graph, repo} that the page uses.'
      ]},
      { kind: 'removed', items: [
        'Model Editor (Ontology): the Load BFO button and the BFO source setting. When no BFO or RO relations are found, the editor points to Ingestion › Reference ontologies.'
      ]},
      { kind: 'fixed', items: [
        'Load BFO failed: it pointed at an add-on file in the BFO repository (the temporalized relations profile), and GraphDB read the RDF/XML it received as Turtle ("Not a valid (absolute) IRI: ?xml"). The default source is now the OBO address of the current BFO release.'
      ]}
    ]
  },
  {
    version: '2.0.0', date: '2026-10-17', title: 'Semantic Governance v1.9: SKOS taxonomies and §3.11 metadata',
    groups: [
      { kind: 'breaking', items: [
        'Taxonomies are SKOS only (§3.11). Ingestion converts a taxonomy authored as OWL classes into a concept scheme: owl:Class becomes skos:Concept, rdfs:subClassOf becomes skos:broader, OWL restrictions on taxonomy terms are dropped (they belong in the ontology). Set "taxonomiesAsSkos": false in the configuration to keep the old behavior.',
        'Taxonomy concept IRIs are UpperCamelCase (…/taxonomy/core-process/ApprovalStep, was …/approval-step). Vocabulary term IRIs stay lower-case hyphenated. crosswalk.csv maps every old IRI to the new one; links into the old IRIs from outside the ingested files break.',
        'A taxonomy concept names its vocabulary term with core:hasPrimaryTerm and dcterms:subject instead of dc:subject (Dublin Core 1.1). dc:subject is still read everywhere, but no longer written.',
        'Asset headers use vaem:namespace instead of vann:preferredNamespaceUri.',
        'Loading into GraphDB stops while a file has a blocking conformance error: terms outside the base URL, another organization’s content, or an invalid date ("loadBlockingRules" in the configuration). Load into GraphDB… lists them and offers Load anyway.'
      ]},
      { kind: 'new', items: [
        'Every vocabulary, taxonomy, ontology and shapes header gets the §3.11 fields: vaem:namespace, vann:preferredNamespacePrefix (processtax, domainfinancevoc …), owl:versionIRI on every asset, dcterms:publisher, dcterms:conformsTo (the guide edition; BFO 2020 for ontologies) and dcterms:subject, from the new configuration settings publisher, conformsTo, ontologyConformsTo and defaultSubject (or "subject" per asset).',
        'Taxonomies get dcterms:source: the vocabularies their concepts draw on, worked out from the links.',
        'core:hasPrimaryTerm is the one vocabulary term whose label matches the concept; when no term matches and there are several, the report asks you to choose.',
        'Numbered labels ("01. Data governance") lose the number, which moves to skos:notation. If the label then repeats another term’s, the numbered one is kept apart (DataGovernance06) and flagged to merge or rename.',
        'Model Editor (Taxonomy): a vocabulary term dropped on a SKOS taxonomy becomes a taxonomy concept of its own (UpperCamelCase, label and definition copied, linked with core:hasPrimaryTerm and dcterms:subject), as it already did for OWL taxonomies. The vocabulary term is no longer put into the taxonomy’s scheme.',
        'New conformance rules, in Ingestion, Standards Conformance and Conformance Review: Primary vocabulary term, Taxonomies stay in SKOS, Asset header fields (§3.11), Valid dates (ISO 8601). Typed terms from another organization’s ontology (individuals, datatypes) now count under Company base URL.',
        'Optional "authorIri" in the configuration writes dcterms:creator as a person IRI instead of the author’s name.'
      ]},
      { kind: 'improved', items: [
        'Standards: Semantic Governance v1.9 (Draft); the guide in docs/ and every page reference it.',
        'Every term gets rdfs:label as well as skos:prefLabel (§3.11), from ingestion and from Conformance Review and the Vocabulary editor when they add terms.',
        '"&" in a preferred label is spelled out as "and"; the old label stays as an alternative label.',
        'Conformance Review suggests UpperCamelCase identifiers for taxonomy concepts, and warns when a staged definition starts in lower case, so a first word cut off when pasting is caught before saving.'
      ]},
      { kind: 'fixed', items: [
        'A date with no time ("2026-10-14") is written as xsd:date; it was written as an invalid xsd:dateTime.',
        'The check that every concept scheme flags its top concepts never ran; it does now.',
        'Ingestion wrote "A controlled vocabulary of …" as the generated description of a SKOS taxonomy.'
      ]}
    ]
  },
  {
    version: '1.9.0', date: '2026-10-16', title: 'Duplicates and generated definitions',
    groups: [
      { kind: 'new', items: [
        'Ingestion: when several files describe the same taxonomy, vocabulary or ontology, the largest is used — most terms (or most bytes, with "duplicates": "largest-file" in the configuration). The others are listed as skipped with the reason, in the scan and in the report.',
        'Ingestion: files whose header is a named resource in a shared namespace (…/taxonomy/core/IssueTaxonomy) each become their own asset (…/taxonomy/core-issue/); a singular name joins the plural domain already in use (core-rule → core-rules).',
        'Definitions written by Claude: tick Write missing definitions with Claude on the Ingestion page (or --define on the command line), use ✦ Write with Claude on a term in Conformance Review or the Model Editor (Vocabulary), or tick terms under Missing definitions and write them in one go. Each gets an editorial note to review it before Candidate.',
        'Claude is told the term, its broader term and that term\u2019s definition, its alternative labels, narrower and sibling terms, and the §3.7 rules: genus + differentia, not circular, no acronyms, no organization names.',
        'Needs an Anthropic API key: put ANTHROPIC_API_KEY=… in ~/.ke-workbench.env (read on every request, no restart). The model is set by "definitionModel" in the configuration (default claude-sonnet-5-5).'
      ]},
      { kind: 'fixed', items: [
        'A SKOS taxonomy is no longer treated as a vocabulary when linking taxonomy terms to vocabulary terms.',
        'Taxonomy terms take their definition from their vocabulary term even when that vocabulary was ingested in an earlier run.'
      ]}
    ]
  },
  {
    version: '1.8.0', date: '2026-10-16', title: 'Every taxonomy term in a vocabulary',
    groups: [
      { kind: 'new', items: [
        'New rule (§3.8), an error: every taxonomy term names its vocabulary term with dc:subject, and that term exists in one of the vocabularies. Ingestion, Standards Conformance and Conformance Review all check it.',
        'Ingestion links a taxonomy term to its vocabulary term automatically when the labels match (preferred or alternative label; the vocabulary of the same domain wins), using this run\u2019s vocabularies and those already in the destination folder. Only the rest are flagged.',
        'Conformance Review: Not in a vocabulary category. Each term shows vocabulary terms with a matching label (Link), a search across all vocabularies, and Add to vocabulary: pick the vocabulary (same domain by default) and the broader term (by default the vocabulary term of the taxonomy term\u2019s parent). The new vocabulary term takes the definition and alternative labels, and the taxonomy term is linked to it.',
        'Bulk: tick terms (or a whole taxonomy) and Add N to a vocabulary — parents go first, so the taxonomy\u2019s hierarchy is kept as broader terms in the vocabulary.',
        'Saving writes both the taxonomy and the vocabulary file (or both graphs in GraphDB); the vocabulary gets a MINOR version step for added terms.'
      ]}
    ]
  },
  {
    version: '1.7.0', date: '2026-10-16', title: 'Vocabulary editor; save closes the batch',
    groups: [
      { kind: 'new', items: [
        'Model Editor (Vocabulary): open any ingested vocabulary file and edit the vocabulary\u2019s metadata (title, alternative labels, description, version, lifecycle status, creator, contributor, language, editorial note) and every term (preferred, alternative and hidden labels, identifier, definition, scope note, example, editorial note, broader, top concept, related, status, version).',
        'Add a term under any broader term, or remove one (its narrower terms move up). Broader/narrower and related links are kept in step both ways.',
        'Conformance is re-checked as you type: the term tree marks errors, and Only terms with errors lists them.',
        'Save & load into GraphDB writes the .ttl and .trig (originals backed up), adds a change note and a change record, and loads the folder into GraphDB; Save files only is there too. Cmd/Ctrl+S saves and loads.'
      ]},
      { kind: 'improved', items: [
        'Conformance Review: Save & load into GraphDB saves the corrections and loads the folder in one step, closing out the batch.',
        'Conformance Review: Save is available as soon as you type in a field; Edit in Model Editor (Vocabulary) opens the selected term in the editor.'
      ]}
    ]
  },
  {
    version: '1.6.1', date: '2026-10-16', title: 'No edit left behind',
    groups: [
      { kind: 'fixed', items: [
        'Conformance Review: text typed into the label, definition or identifier field is staged when you move to another term, category or action, even if Stage was not clicked.',
        'Conformance Review: Find issues on other files keeps the files that have staged changes loaded, so those changes are saved with the rest instead of being dropped.'
      ]}
    ]
  },
  {
    version: '1.6.0', date: '2026-10-16', title: 'Review, then load',
    groups: [
      { kind: 'new', items: [
        'Conformance Review: Load into GraphDB… loads the folder you are reviewing — every current model replaces its named graph and the change records (with your corrections) go to the change log. It works at any time, without going back to the Ingestion page.',
        'The workbench decides which files are current: when a later run produced the same asset, or the same asset from the same source file, the older copy is set aside in superseded/ automatically and is never loaded or offered for review.'
      ]},
      { kind: 'improved', items: [
        'Ingestion: Load into GraphDB… uses the same folder load, so it also takes Conformance Review corrections and leaves older copies out.',
        'Ingestion warns before a run would replace files that were corrected in Conformance Review, and keeps a copy of them in superseded/ if you go ahead.',
        'Loading a change record twice adds nothing to the change log.'
      ]}
    ]
  },
  {
    version: '1.5.2', date: '2026-10-16', title: 'Review opens the file',
    groups: [
      { kind: 'fixed', items: [
        'Review › on the Ingestion page opens the file with its first finding selected, so the label, definition and identifier fields are there to edit straight away.',
        'The workbench server picks up updated ingestion code (ingest/ke_ingest.py, ingest/ingest_api.py) without a restart.',
        'Conformance Review says so plainly when the workbench server is too old for file review, instead of showing an empty page.'
      ]}
    ]
  },
  {
    version: '1.5.1', date: '2026-10-16', title: 'Review before loading',
    groups: [
      { kind: 'new', items: [
        'Ingestion results: each file with conformance errors has a Review › button, and Review files with errors… opens all of them in Conformance Review, before anything is loaded into GraphDB.',
        'Conformance Review has a Source switch: Ingested files (the .ttl files of an ingestion run, from any folder) or GraphDB. In file mode, Save to files rewrites each corrected .ttl and its .trig twin, copies the originals to a review-backup folder, and adds the corrections to the run\u2019s change record, so Load into GraphDB on the Ingestion page carries them.'
      ]}
    ]
  },
  {
    version: '1.5.0', date: '2026-10-16', title: 'Conformance Review',
    groups: [
      { kind: 'new', items: [
        'Conformance Review page (Model & standards › Conformance Review): the findings the ingester cannot decide, grouped as other organizations\u2019 content, acronyms, broken and foreign references, missing definitions and other, for vocabularies, SKOS and OWL taxonomies, and ontologies.',
        'Each term opens in context (parents, children, what references it) with its findings and a suggested fix: an organization-neutral definition or description, a label with the acronym spelled out, or removal.',
        'Fixes: edit the preferred label (the old one kept as an alternative label), edit the definition or the model description, remove alternative labels, remove broken links, change the identifier everywhere it is used, or remove the term.',
        'Removing a term moves its children up to its parent (or makes them top concepts), takes it out of lists and disjointness axioms, and removes the restrictions, shapes and links that use it; the plan is shown before you stage it.',
        'Bulk actions on a selection or a whole model or namespace: stage the suggestions, stage removals, or skip.',
        'Approve an acronym (Appendix F) or remember an expansion from the page; both go into the ingestion configuration, so the next ingestion, Standards Conformance and this page all use them.',
        'Changes are staged and applied as one change set: each model gets a new version (§3.3: patch for edits, minor or major for removals and new identifiers), a change note, and a PROV-O change record in the change-log graph.'
      ]},
      { kind: 'improved', items: [
        'Ingestion removes other organizations\u2019 terms (named in the configuration; Verizon to start), re-parents their children, and spells out acronyms in labels from the configuration, the term\u2019s alternative labels or its definition.',
        'Ingestion removes broken references: bare declarations of terms from other namespaces (left behind by ontology editors), orphaned blank nodes, links to removed terms, and shapes of removed classes. Terms from other namespaces that have content are kept and reported for review.',
        'Ingestion moves definitions that were stored as alternative labels to skos:definition, removes parentheses around labels, and maps properties from legacy namespaces to the standard.',
        'The configuration has an approved-acronym list, known expansions and an organizations list (patterns, replacement wording).',
        'Standards Conformance uses the same approved acronyms and adds two rules: no other organization\u2019s content, no broken references.'
      ]},
      { kind: 'fixed', items: [
        'The command-line ingester accepts a --timestamp ending in Z on older Python versions.'
      ]}
    ]
  },
  {
    version: '1.4.0', date: '2026-10-15', title: 'Ingestion',
    groups: [
      { kind: 'new', items: [
        'Ingestion page (Model & standards › Ingestion): choose a source folder and a destination folder, scan, and ingest vocabularies, taxonomies and ontologies into the Part III standard.',
        'Reads Turtle (.ttl), N-Triples (.nt) and RDF/XML (.rdf, .rdfs, .owl, .xml); files that are not a single vocabulary, taxonomy or ontology are listed with the reason and skipped.',
        'Turtle and TriG are written to separate sub-folders (ttl/ and trig/ by default); each TriG file holds its asset in a named graph, so a GraphDB import puts it where the workbench looks.',
        'Every run writes a PROV-O change record (Turtle and TriG, for the …/graph/change-log graph), a crosswalk of old to new IRIs, and an ingestion report with conformance results.',
        'Titles and descriptions are generated from the content when the configuration has none, and flagged for review.',
        'Load into GraphDB from the results: each asset replaces its named graph, the change record is appended to the change log.',
        'Edit the ingestion configuration (namespace rules, titles, descriptions, renames, definitions) on the page; the previous version is kept as a backup.',
        'ingest/ke_ingest.py runs the same code from the command line: python3 ingest/ke_ingest.py SOURCE -o DEST.'
      ]},
      { kind: 'improved', items: [
        'Model Editors read only stored statements (no inferred rdfs:subClassOf closure), so a class appears once, under its own parent.',
        'Model Editors leave shapes graphs out of their asset lists, and recognise /vocabulary/, /taxonomy/, /ontology/ and /shapes/ IRIs as well as legacy hyphenated names.'
      ]}
    ]
  },
  {
    version: '1.3.0', date: '2026-10-15', title: 'Ontology canvas and release notes',
    groups: [
      { kind: 'new', items: [
        'Release Notes page (Reference › Release Notes); the release number on the Overview links to it.',
        'Model Editor (Ontology): choosing an ontology draws its whole class hierarchy on the canvas as a left-to-right tree, each class under its most specific parent.',
        'Model Editor (Ontology): drag a whole model — ontology, taxonomy or vocabulary — from the Models list onto the canvas; its terms are placed as their own hierarchy where you drop it.',
        'Model Editor (Ontology): “Show ontology” button redraws the edited ontology’s hierarchy (Undo restores the previous canvas).'
      ]},
      { kind: 'improved', items: [
        '“is a” lines implied by another “is a” (A is a B, B is a C ⇒ A is a C) are no longer drawn, so broad ontologies stay readable; the triples are untouched and the Inspector still lists every relation.',
        'Large hierarchies open centred on the root at a readable zoom instead of shrinking to fit.',
        'Both Model Editors find the terms of models that only use a namespace (IRI#… or IRI/…) — e.g. Ontology | Domain | Governance — unless a term is defined by another model.'
      ]},
      { kind: 'fixed', items: [
        'An empty saved canvas no longer hides an ontology when it is opened again.'
      ]}
    ]
  },
  {
    version: '1.2.0', date: '2026-10-15', title: 'Model editors on real data',
    groups: [
      { kind: 'new', items: [
        'start-workbench.command: double-click launcher for the Mac that stops an older server on port 3000, starts this folder’s proxy and opens the workbench.',
        'Model Editor (Taxonomy) supports OWL taxonomies (owl:Class + rdfs:subClassOf, as in taxonomy-core-*) as well as SKOS concept schemes.',
        'Dropping a vocabulary term on an OWL taxonomy reuses the class already linked by dc:subject (or a class with the same label), otherwise creates a class named from the label with rdfs:label, rdfs:isDefinedBy and dc:subject.'
      ]},
      { kind: 'improved', items: [
        'Model Manager restyled to match the workbench, with counts per Voc / Tax / Ont / Other tab and a filter.',
        'Model Editor (Ontology) lists BFO and RO core relations (obo:BFO_ and obo:RO_), hides deprecated ones, and finds relations of ontologies stored in the default graph.',
        'Edits go to the model’s named graph, or to the default graph when it has none.',
        'proxy.py tells the browser not to cache pages, so an updated tool appears on the next reload; it listens on IPv4 and IPv6 localhost, handles requests in parallel, prints the folder it serves and explains when port 3000 is already in use.'
      ]},
      { kind: 'fixed', items: [
        'Drag and drop in both Model Editors now uses the pointer directly — browser drag-and-drop did not work inside workbench tabs and embedded browser panes.',
        'Model Manager listed some assets twice (several labels, or a match both inside and outside a named graph).',
        'Model Editor (Taxonomy) showed “No taxonomies found” because the taxonomies are OWL ontologies, not SKOS schemes.'
      ]}
    ]
  },
  {
    version: '1.1.0', date: '2026-10-14', title: 'Model Editors',
    groups: [
      { kind: 'new', items: [
        'Model Editor (Taxonomy): pick a taxonomy, drag vocabulary terms onto it — drop on a term to make them narrower, on its top edge to make one broader; Alt/⌥ adds a second broader term.',
        'Model Editor (Ontology): load ontologies and taxonomies on the left, drag terms onto a canvas and relate them with a relation chosen from BFO.',
        'assets/ke-sparql.js: shared SPARQL helpers; every query goes through the proxy.'
      ]},
      { kind: 'improved', items: [
        'The classic Model Editor is hidden from the navigation (still in tools/).',
        'Model Manager’s Taxonomy and Edit buttons open the new editors through the proxy instead of calling GraphDB on port 7200 directly.'
      ]}
    ]
  },
  {
    version: '1.0.0', date: '2026-10-14', title: 'KE Workbench',
    groups: [
      { kind: 'new', items: [
        'One workbench shell for the modeling tools, the SSOT for rules and logic, and the agent operations dashboards, with tabs that keep their state, a GraphDB status pill and a light/dark theme.',
        'Overview page with live asset counts, tool map, §1.3 function mapping, Part III quick reference and the E.3 checklist.',
        'Standards Conformance: checks GraphDB graphs or a Turtle file against the Part III / Appendix E standards.',
        'proxy.py serves the workbench and forwards /graphdb/* to GraphDB, so there are no CORS problems.'
      ]},
      { kind: 'improved', items: [
        'All tools follow the workbench theme and open their links as workbench tabs.',
        'Model Manager: compliant base URLs are a setting (default https://www.insperity.com/ plus the legacy https://www.enablingvalue.com/).',
        'OWL / SKOS / Taxonomy metadata editors use semantic versioning for owl:versionInfo.'
      ]}
    ]
  }
];
