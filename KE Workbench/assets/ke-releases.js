/* KE Workbench — release history (newest first). Shown on the Release Notes page.
   Add a new entry at the top for every release and bump `version` in ke-registry.js to match. */
window.KE_RELEASES = [
  {
    version: '4.5.0', date: '2026-10-24', title: 'Semantic Governance v2.0 in force',
    groups: [
      { kind: 'new', items: [
        'The workbench applies the latest edition of the standards guide it finds: ingest/guide_sync.py (run when the shell opens, through POST /api/ingest/guide-sync) picks the newest Semantic_Governance_v*.pdf in docs/ or ../Semantic Governance/, copies it into docs/ if needed, and writes assets/ke-guide.js. Semantic Governance v2.0 (Draft) is now in force.',
        'When the edition changes, the ingestion configuration moves to it (conformsTo …/standard/semantic-governance/2.0/ and standardsRef), so everything ingested or built from now on declares v2.0, and the Operations Dashboard reports are rebuilt.',
        'Operations Dashboard: if the guide in force differs from the edition its reports were built against, the page rebuilds them and reloads. The Standards guide tab shows the edition in force and where it resolves each of the 21 retrofit items (resolved, decision pending, or resolved in the guide with tool work open).'
      ] },
      { kind: 'improved', items: [
        'The sidebar, the Overview, the guide link (Reference) and Model Editor (Ontology) take the edition from assets/ke-guide.js instead of naming v1.9.',
        'Actions: the 15 retrofit items v2.0 resolves leave the list; the three it writes as proposals (G02 instance identifiers, G12 Candidate criteria, G20 measured agent assurance) become decisions; tool work is tracked by policies P03–P05 and P07. Open actions went from 74 to 56.',
        'Policy P07 now checks assets against the edition in force: all 107 model assets still declare v1.9 (or none) until they are rebuilt.'
      ] }
    ]
  },
  {
    version: '4.4.0', date: '2026-10-23', title: 'Operations Dashboard: the change log as evidence',
    groups: [
      { kind: 'new', items: [
        'Operations Dashboard (Agents & operations): every change record (PROV-O activities in the change-log graph and the change-record files) joined to the current inventory of core and domain models and their conformance.',
        'Causality & root cause: for a change set, its upstream causes and downstream effects through prov:used, prov:generated and prov:wasDerivedFrom; for an asset or term, its history, current findings and the change set that introduced them; and which tools the defects enter through.',
        'Domains: expansion over time by area, and continuous improvement by domain (change sets, edits, review cycles, findings and error density, with a trend across snapshots).',
        'Compliance: conformance by rule and domain, nine process policies on the change log (creator, approver, requirement, deployment records, one current copy, lifecycle), and the guide edition each asset declares.',
        'Standards guide: 21 places where Semantic Governance v1.9 no longer matches practice (identifiers, URIs, named graphs, change records, operational areas, primitives, service assembly), with the proposed v2.0 text; copy as Markdown.',
        'Actions: one list of what closes each gap (conformance, policy, guide, decisions, lifecycle, portfolio), with status kept in the browser and CSV export.'
      ] },
      { kind: 'improved', items: [
        'Rebuild snapshot: POST /api/ingest/ops-snapshot (or python3 ingest/build_ops_snapshot.py) rebuilds data/ops/ and adds a line to the history used for trends. With GraphDB on, change records in the graph are merged with those on disk and the gaps between them are listed.'
      ] }
    ]
  },
  {
    version: '4.3.0', date: '2026-10-23', title: 'PEO Service Map: market crosswalk and expansion',
    groups: [
      { kind: 'new', items: [
        'Market crosswalk tab: each of the 44 PEO Service Landscape rows is mapped to the L3 services that deliver it (21 direct, 10 partial, 13 with no service), with Insperity and the six competitors side by side and the proposals that fill each gap. Rows Insperity sells but the business model lacks: expense management, business insurance and outplacement. Offer and delivery models (co-employment, HRCore, HRScale, ASO, EOR, published pricing) are shown as a dimension of the offer, not as services. Copy as CSV.',
        'Expansion tab: 41 proposed L3 services, each with origin (4 from Insperity\u2019s catalog, 17 from competitors, 20 from the semantic knowledge layer), recommendation (pursue, partner, monitor, decline), the competitors that offer it, the knowledge-layer capabilities it builds on, evidence links and the customer questions it would strengthen. Two proposed L1 domains (Workforce Intelligence, Risk & Agentic Assurance; Global Employment & Contingent Workforce), eleven L2 bounded contexts and six service lines (Global Workforce, Business Insurance, Compliance Intelligence, Risk Intelligence, Decision Intelligence, Agentic Assurance). Copy as CSV.',
        'Service breakdown: Show proposed services adds the proposals to the tree as dashed entries; each L3 service shows how the market delivers it.',
        'Authored in KE Domains/_build/service_map_expansion.py; the builder reads the landscape matrix straight from tools/peo-service-landscape.html and writes KE Domains/HR Service Operations/peo-service-map/market-and-expansion-report.md.'
      ]}
    ]
  },
  {
    version: '4.2.0', date: '2026-10-23', title: 'Products & Services: the PEO Service Map and the PEO Service Landscape',
    groups: [
      { kind: 'new', items: [
        'Section 05 is Products & Services, after Customer 360. It holds two pages.',
        'PEO Service Map (tools/peo-service-map.html): the external services of HR Service Operations broken down as L1 domain \u203a L2 bounded context \u203a L3 domain service (8, 17, 74), also organized by the 11 service lines clients buy, and joined to the Customer 360 personas, jobs and desired outcomes. Every desired outcome becomes the question a persona asks (224, plus a headline question per job, 250 in all) and is traced to the services that answer it. Four views: Service breakdown, By persona (each job\u2019s questions by job map stage), Questions (search and filter by persona, domain, service line, stage; copy CSV) and Coverage (persona by domain and by service line, gaps, thinly covered services).',
        'The map is built by KE Domains/_build/build_service_map.py from the HR Service Operations taxonomy (L1), the business model extract in KE Domains/Reference/hr-services-business-model/ (L2, L3, service lines) and data/c360/. It writes KE Domains/HR Service Operations/peo-service-map/ (the map, a coverage report and a README) and data/peo-service-map/peo-service-map.js. L2 and L3 IRIs follow D26 and are marked planned until the business model is ingested (open question 27).',
        'PEO Service Landscape (tools/peo-service-landscape.html): the competitive capability matrix of Insperity and six U.S. PEOs (core, add-on, partner, none, verify), with evidence notes and sources. Formerly titled PEO Service Map.'
      ]}
    ]
  },
  {
    version: '4.1.0', date: '2026-10-23', title: 'Customer 360 runs entirely inside the workbench',
    groups: [
      { kind: 'new', items: [
        'PEO Outcome Review is a workbench page (tools/peo-outcome-review.html). Reviewers enter their name once (and whether they record final decisions); reviews are shared through GraphDB, one named graph per reviewer (\u2026/graph/customer-360/review/reviewer/{id}) and one per final decision (\u2026/review/decision/{item}), and the page re-reads them every 15 seconds. With GraphDB off, reviews are kept in the browser and published the next time GraphDB is reachable. Export CSV still works.',
        'Outcome review ontology and vocabulary (data/c360/15-, 16-): reviewer, item review and review decision, aligned to Baseline Core (core:person, core:information-asset, core:decision), with roles, verdicts, risk flags, approved uses, study dispositions and decision statuses as concepts. Load benchmark into GraphDB adds them.',
        'PEO Outcome Playbook is a workbench page (tools/peo-outcome-playbook.html). It uses the survey results loaded in the Job Study when there are any, instead of always showing the example scores.'
      ]},
      { kind: 'improved', items: [
        'The Demand Gateway and Buyer Personas & Jobs read review decisions and compliance flags straight from the graph; the review CSV import is now only for reviews recorded elsewhere, and decisions in the graph take precedence.',
        'The sales advisor in the Playbook has no live Claude connection in the workbench, so \u201cCopy prompt for Claude\u201d copies the rules, the prospect and the retrieved outcomes as one prompt to paste into Claude.'
      ]},
      { kind: 'removed', items: [
        'No Customer 360 tool links to claude.ai any more: the registry, the Gateway, the Playbook and the release history point at the pages in tools/.'
      ]}
    ]
  },
  {
    version: '4.0.0', date: '2026-10-22', title: 'Customer 360: from persona interviews to demand planning and back',
    links: [
      { label: 'PEO Outcome Review', href: 'peo-outcome-review.html', note: 'business and compliance sign-off (in the workbench since 4.1.0)' },
      { label: 'PEO Outcome Playbook', href: 'peo-outcome-playbook.html', note: 'battle cards, the Fix / Innovate / Protect / Simplify rule and the sales advisor agent (in the workbench since 4.1.0)' }
    ],
    groups: [
      { kind: 'new', items: [
        'Section 04 is now Customer 360 (it was Domain context): Appreciative Inquiry, Buyer Personas & Jobs, PEO Job Study, PEO Outcome Review \u2197, PEO Outcome Playbook \u2197 and Demand Gateway. In 4.0.0 the two tools marked \u2197 opened outside the workbench; 4.1.0 brings them in.',
        'Buyer Personas & Jobs reads persona instances from GraphDB in the same layout as before (Explore, Graph, Job Study). The Job Study tab has a pull-down of every job: pick one to see its desired outcomes on the eight job map stages, the steps people described in interviews, study scores and the Playbook action, review status, interview evidence and demand. Copy a job as CSV.',
        'Appreciative Inquiry: capture persona interviews through Discover, Dream, Design and Destiny with prompts tailored to a focus job; select a passage and code it as a functional, emotional or social job, a job step or a desired outcome (built from direction, metric, object and clarifier), either as a new candidate or as evidence for an existing item. Interviews save as drafts in the browser and publish to their own named graph.',
        'PEO Job Study is in the workbench (tools/peo-benchmark/): opportunity landscape, job map and PEO vs non-PEO comparison. Load survey results there; every Customer 360 tool uses the same scores.',
        'Demand Gateway, the requirements engineering semantic gateway: bundle under-served outcomes into demand requests, check them against six rules (traced, reviewed, evidenced, measurable, owned, unflagged), and admit them to demand planning. Requests are written back to the graph, so personas and jobs show what is in demand, and the portfolio exports to demand planning as CSV or Turtle.',
        'Bundled Customer 360 data (data/c360/, 15 Turtle files with a manifest): the jobs-to-be-done, appreciative inquiry and demand planning ontologies, their vocabularies and the PEO benchmark instances. With GraphDB connected but empty, Buyer Personas & Jobs offers to load them into their named graphs; with GraphDB off, every tool reads them directly.'
      ]},
      { kind: 'breaking', items: [
        'Customer 360 schema 0.3.0: classes and taxonomy concepts use lower-case hyphenated identifiers (jtbd:client-persona, theme:payroll) under Semantic Governance v1.9 \u00a73.2 as amended for Baseline Core v1.0. If you loaded the 0.1.0 or 0.2.0 Turtle into GraphDB, reload with Load benchmark into GraphDB (the same named graphs are replaced).',
        'The eight universal stages are jtbd:job-map-stage (they were jtbd:JobStep), so they no longer collide with core:job-step, a step that belongs to one job. Steps captured in interviews are jtbd:job-map-step, a core:job-step.'
      ]},
      { kind: 'improved', items: [
        'Aligned to Baseline Core v1.0: client persona \u2286 core:persona, job to be done \u2286 core:job, job map step \u2286 core:job-step, desired outcome \u2286 core:desired-outcome, demand request \u2286 core:requirement, outcome target \u2286 core:measure, interview notes and excerpts \u2286 core:information-asset; executesJob, hasJobMapStep and isStepOfJob specialize core:performsJob, core:hasStep and core:isStepOf. Sales selling steps reach these job steps through core:addresses.',
        'Every Customer 360 ontology and scheme carries the \u00a73.11 header fields; the bundled files and the graphs the tools write pass Standards Conformance with no findings.',
        'Triples loaded into the default graph instead of their named graphs are still read, with a note to move them.'
      ]},
      { kind: 'fixed', items: [
        'The shell and the Overview open external tools in a browser tab instead of an empty workbench tab.'
      ]}
    ]
  },
  {
    version: '3.9.0', date: '2026-10-21', title: 'Commercial Operations on APQC PCF 7.4: every domain, down to the activity',
    links: [
      { label: 'APQC PCF reference (in the workbench)', href: '../reference/apqc-pcf/index.html', note: 'version 7.4 in use, categories 3.0 and 6.0 browsable to L5, the 7.2.1 \u2192 7.4 crosswalk and the attribution' },
      { label: 'APQC Process Classification Framework, Cross-Industry, version 7.4 (PDF)', href: 'https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-pdf-12', note: 'published 21 August 2024 by APQC' },
      { label: 'APQC Process Classification Framework, Cross-Industry, version 7.4 (Excel)', href: 'https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-excel-11' },
      { label: 'About the APQC PCF', href: 'https://www.apqc.org/pcf', note: 'version 8.0 was released 27 February 2026 and is not adopted yet (open question 29)' }
    ],
    groups: [
      { kind: 'new', items: [
        'All five Commercial Operations domains have a service assembly, built on APQC PCF 7.4 (design decisions D28, D29): Sales 0.5.0 (16 services, 44 activities, 63 steps), Sales.Partner & Channel 0.1.0 (5, 26, 30), Marketing 0.1.0 (11, 54, 56), Pricing 0.1.0 (4, 15, 17) and Customer Care 0.1.0 (9, 39, 49), all on category 3.0 except Customer Care, which is on 6.0 Manage Customer Service. Load them with KE Domains/graphdb-load.command; \u201cAll service assemblies (5)\u201d is the default.',
        'The topology shows each domain\u2019s processes on APQC\u2019s levels: process group (L2) \u203a process (L3) \u203a activity (L4), with the activity\u2019s tasks (L5) as its steps. L2 and L3 come from the APQC reference registry, so a process whose activities are owned by several domains is shown under each, with \u201cowned by\u201d for the domain that owns it. L2 / L3 / L4 buttons set how deep the tree opens. PEO extensions (activities APQC does not list, such as underwriting and quoting) sit under the element they extend.',
        'Click an activity for its SIPOCM, one row per step, with the domain of each supplier and customer; click a process group or process for the SIPOCM of all its activities in the domain. Each domain also lists its services, and a service opens the SIPOCM of the activities that enable it.',
        '\u201cShow not applicable\u201d adds the APQC elements a PEO does not perform (warranty, recall, packaging and the like), as recorded in the registry. \u201cSet aside known core warnings\u201d (on by default) keeps the two warnings the core shapes raise on every assembly (open question 16) out of the counts; the Validation tab still lists them.',
        'APQC PCF reference page (Reference \u203a apqc-pcf in the workbench folder): the version in use and the official links, categories 3.0 and 6.0 as a searchable outline to L5, and the crosswalk from 7.2.1.',
        'Release Notes can list references with each release, as below.'
      ]}
    ]
  },
  {
    version: '3.8.0', date: '2026-10-21', title: 'Service topology across every domain, filtered by L1, L2 and L3',
    groups: [
      { kind: 'new', items: [
        'The topology shows every operational area and all of its domains, read from the area taxonomies (the domain concepts under each area\u2019s top concept, nested L1 \u203a L2 \u203a L3). A domain with no service assembly is drawn as a dashed box marked \u201cno service model yet\u201d, with \u201contology x.y.z\u201d when its ontology is loaded or \u201cnot started\u201d when it is only listed in the area taxonomy. Domain names follow the naming standard (Domain Sales, Domain Sales.Partner & Channel).',
        'Filter by operational area and by L1, L2 and L3 domain (each list offers the children of the level above), and tick \u201cOnly domains with services\u201d to hide the gaps. The filter also narrows the Services view, is remembered in the browser, and can be set in the address with ?domain=domain-sales.partner-and-channel.',
        'When more than one service assembly is loaded, \u201cAll service assemblies\u201d at the top of the assembly list reads them all into one topology.'
      ]}
    ]
  },
  {
    version: '3.7.0', date: '2026-10-21', title: 'Service Assembly: service topology with SIPOCM by process',
    groups: [
      { kind: 'new', items: [
        'Topology view on Service Assembly (now the default): the assembly drawn as a tree, Operational area \u203a Domain (and nested domains) \u203a Service \u203a Process. The area is read from the domain ontology\u2019s dcterms:isPartOf and the names from the asset titles (naming standard, D26). Each box shows its counts and validation status; a process also shows its steps, whether it delivers the service, the APQC element its kind is anchored to (exact or broad match) and, with a dashed edge, that several services share it.',
        'Click a process to see its SIPOCM below the tree, one row per step in order: supplier, input, process step (and who performs it), output, customer, measure, and a Check column with each step\u2019s validation status. Click a service for the SIPOCM of every process that enables it. Clicking a step opens its detail in the inspector; Validation and Used by work as on the Services view.',
        'Expand all, Collapse all and Print (prints the tree and the SIPOCM table for sign-off). Open the other views directly with ?view=catalog or ?view=coverage.'
      ]}
    ]
  },
  {
    version: '3.6.0', date: '2026-10-21', title: 'Operational areas and the naming standard',
    groups: [
      { kind: 'improved', items: [
        'Standards checks (ke_ingest.py, used by Ingestion, Conformance Review and the KE Domains builds) accept the naming standard for nested domains: an IRI segment of lower-case hyphenated words with levels joined by dots, such as …/taxonomy/domain-sales.partner-and-channel/ (§3.2 as amended, D26).',
        'Service Assembly reads the Commercial Operations ontology at its new IRI (…/ontology/commercial-operations/), and checks insulation by operational area: a domain may refer to the core, its own area (read from its ontology\u2019s dcterms:isPartOf), its parent domains and itself; vocabulary primitives may be cited from any domain (D27).'
      ]}
    ]
  },
  {
    version: '3.5.0', date: '2026-10-20', title: 'Service Assembly: Service › Process › Process step, with SIPOCM',
    groups: [
      { kind: 'new', items: [
        'Service Assembly shows each service as the processes that enable it (core:supports), each process as its steps in order (core:hasStep, core:precedes), and the step that hands the service over (core:deliveryOf). Click a process or a step to drill down; the breadcrumb goes Assembly › Service › Process › Step.',
        'SIPOCM table for every service, one row per step, grouped by process: supplier, input, process step (and who performs it), output, customer and measure. Suppliers and customers inside the assembly are derived from the data flow (the step that produces an input, or consumes an output); parties outside it are read from has supplier and has customer (Commercial Operations container 0.3.0). The step detail lists the same, with each measure\u2019s definition, unit and direction.',
        'Used by and copy number for processes as well as steps; a Process filter in the service list; Coverage shows processes by service and steps by service.'
      ]},
      { kind: 'improved', items: [
        'Buyer personas, job steps and desired outcomes are no longer shown on Service Assembly: they are a separate assembly, the value map (design decision D24), which gets its own Value Mapping page. The page lists only manifests that contain service graphs, and flags any reference from the service assembly to the persona graph or value map as an error.'
      ]}
    ]
  },
  {
    version: '3.4.0', date: '2026-10-20', title: 'Service Assembly: the services of a domain and the steps that deliver them',
    groups: [
      { kind: 'new', items: [
        'Service Assembly (Model & standards): pick a domain assembly by its release manifest (core concept “Release manifest”) and see its services, each with its delivery step (core:deliveryOf), the steps that support it (core:supports) and their order (core:precedes). The page reads only the graphs the manifest lists and the taxonomies, ontologies and shapes it requires, from GraphDB, and writes nothing.',
        'Drill down from a service to a step: what it uses and produces, its stage, kind and mode (manual, automated or hybrid, from core:performedBy), the role it fulfills, the job steps it addresses, and Used by: every service that contains the step (its copy number), so the reach of a change is visible before it is made.',
        'Job steps addressed: each desired outcome of the persona graph with its metric card and target, beside the baseline the service delivers today, marked value gap, met or not measured.',
        'Validation for each service and step: the core, container and domain SHACL shapes (targetClass, path and inverse path, class, or, min and max count) and the assembly checks (typed by a loaded class, classified by a loaded concept, no reference to a sibling domain), after the owl:inverseOf pairs are applied. Filter the catalog by stage, mode, or errors, warnings and value gaps.',
        'Coverage: steps by service (shared steps first, the platform candidates) and job steps by service, with the job steps no service addresses marked, filterable by buyer stage.'
      ]}
    ]
  },
  {
    version: '3.3.0', date: '2026-10-20', title: 'Conformance Review: dispositions that train the ingestion agents',
    groups: [
      { kind: 'new', items: [
        'Disposition for every finding in Conformance Review: Fixed by the staged changes, Accept as is (an exception), Not an issue (the rule fired wrongly), Defer, or Needs a modeling decision — with a rationale. Several selected findings can be dispositioned at once. The last decision on a term is shown with it.',
        'Each decision is recorded in ingest/feedback/dispositions.jsonl (append-only, schema in ingest/feedback/README.md): the term and the context the agent saw, the findings, what the tool suggested, what the reviewer decided and changed, the Claude draft a reviewer corrected, and why. Fixes are recorded when the change set is saved; the other dispositions when you click Record. Download the training set from the left panel.',
        'Ingestion learns from the decisions: fixes are replayed when the same term is ingested again with the value the reviewer replaced (label, definition, description, vocabulary link, formalized by); findings accepted or marked not an issue are reported as information with the rationale; and Claude is shown the definitions reviewers approved, corrected drafts first, when it writes new ones. The ingestion report lists what was applied under “Applied from review decisions”. Set "learnFromReview": false in the configuration to switch it off.',
        'New category “Not formalized by a class”: taxonomy concepts that neither carry core:formalizedBy nor sit under a concept that does, reported on the broadest such concept with the number of concepts that depend on it. Formalize by a likely class (same label, same primary term, head word, an earlier decision, or what the other top concepts use) or any class, one at a time or in bulk.'
      ]},
      { kind: 'improved', items: [
        'Findings accepted or marked not an issue leave the queue (Show staged, skipped and dispositioned brings them back); deferred and escalated ones stay, tagged.'
      ]}
    ]
  },
  {
    version: '3.2.0', date: '2026-10-20', title: 'Core domain ontology includes the core taxonomies; expandable tree with levels',
    groups: [
      { kind: 'new', items: [
        'The core domain ontology imports the 23 core taxonomies (owl:imports), so it includes every core taxonomy and its concepts. Concepts stay linked to their classes by core:formalizedBy, stated in the taxonomies; no class, relation or concept changed and the version stays 0.1.0 (Draft). Updated in ingest/core/ontology-core.source.ttl, in Baseline Core v1.0 (ttl and trig) and in GraphDB, with a change record (change-record-2026-10-20T121500Z) in the audit log.',
        'Model Editor (Ontology) Tree view is an expandable hierarchy: the edited ontology\u2019s classes, the subclasses other loaded ontologies add, the taxonomy concepts each class formalizes and their narrower concepts. Double-click a term, or click the chip at its lower right (+N = N hidden below it, − = open), to expand or collapse it.',
        'Levels control (− Levels n + All) on the canvas: how many levels of the hierarchy are open. Show ontology goes back to the default: every class open with the first level of concepts under it.',
        'Taxonomy concepts that no class formalizes yet hang under their taxonomy (shown as a root marked “concepts not yet formalized by a class”), so every concept of every shown taxonomy is in the tree.'
      ]},
      { kind: 'improved', items: [
        'A term goes under its most specific parent within the tree, so a class that also specializes a BFO class sits under its core parent (information asset under asset), and the BFO parents sit in a column on the right.',
        'The tree is rebuilt from the data each time; the editor remembers per ontology how far it was opened and the terms you placed by hand. Layouts saved before 3.2.0 are ignored.',
        'Turning a tier off removes what it contributes to the tree (for example the taxonomy concepts, which are secondary).',
        'Imports that name a version IRI (…/ontology/core/0.1.0/, as the Commercial Operations domain ontologies do) resolve to the ontology, so its relations show as secondary.'
      ]}
    ]
  },
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
