/* KE Workbench — release history (newest first). Shown on the Release Notes page.
   Add a new entry at the top for every release and bump `version` in ke-registry.js to match. */
window.KE_RELEASES = [
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
