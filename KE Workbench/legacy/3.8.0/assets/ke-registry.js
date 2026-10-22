/* KE Workbench — tool registry (shared by the shell and the overview page). */
window.KE_REGISTRY = {
  version: '3.8.0',
  groups: [
    {
      id: 'model', label: 'Model & standards', eyebrow: 'Knowledge fabric · GraphDB',
      blurb: 'Author, inspect and check vocabularies, taxonomies and ontologies in the graph store.',
      tools: [
        { id: 'model-manager', code: 'MM', file: 'tools/model-manager.html', title: 'Model Manager', live: true,
          desc: 'Browse every vocabulary, taxonomy and ontology graph by kind; edit asset metadata, rename URIs, move triples into named graphs, and open the editors and visualizer.',
          functions: ['Artifact versioning', 'Change monitoring'], std: ['3.2', '3.3'] },
        { id: 'ingestion', code: 'IN', file: 'tools/ingestion.html', title: 'Ingestion', live: true, isNew: true,
          desc: 'Bring vocabularies, taxonomies and ontologies (Turtle, N-Triples, RDF/XML) from a folder into the standard: new IRIs, rebuilt metadata, Turtle and TriG in separate folders, a change record, and an optional load into GraphDB.',
          functions: ['Artifact versioning', 'Governance workflow', 'Integration with graph databases'], std: ['3.2', '3.3', '3.7'] },
        { id: 'conformance-review', code: 'CR', file: 'tools/conformance-review.html', title: 'Conformance Review', live: true, isNew: true,
          desc: 'Human in the loop for conformance errors: other organizations\u2019 content, acronyms, broken and foreign references, missing definitions. Works on ingested files before loading (opened from Ingestion) or on GraphDB; stage fixes or removals across vocabularies, taxonomies and ontologies and save them with a change record.',
          functions: ['Governance workflow', 'Artifact versioning', 'Change monitoring'], std: ['3.2', '3.3', '3.7'] },
        { id: 'model-editor-vocabulary', code: 'EV', file: 'tools/model-editor-vocabulary.html', title: 'Model Editor (Vocabulary)', live: true, isNew: true,
          desc: 'Edit an ingested vocabulary file: the vocabulary\u2019s own metadata and every term (labels, definition, notes, broader and related terms, status), add or remove terms, with conformance checked as you type. Save writes the .ttl and .trig and loads them into GraphDB.',
          functions: ['Unified modeling', 'Artifact versioning'], std: ['3.2', '3.3', '3.7'] },
        { id: 'model-editor-taxonomy', code: 'ET', file: 'tools/model-editor-taxonomy.html', title: 'Model Editor (Taxonomy)', live: true, isNew: true,
          desc: 'Pick a taxonomy, then drag one or more vocabulary terms onto it: drop on a term to make them narrower, on its top edge to make one broader.',
          functions: ['Unified modeling'], std: ['3.7', '3.8'] },
        { id: 'model-editor-ontology', code: 'EO', file: 'tools/model-editor-ontology.html', title: 'Model Editor (Ontology)', live: true, isNew: true,
          desc: 'Load imported ontologies and taxonomies on the left, drag terms onto a canvas and connect them with relations from BFO.',
          functions: ['Unified modeling'], std: ['3.1', '3.7', '3.9'] },
        { id: 'service-assembly', code: 'SA', file: 'tools/service-assembly.html', title: 'Service Assembly', live: true, isNew: true,
          desc: 'Service topology (Operational area › Domain › Service › Process, with the SIPOCM of a process one row per step) and Service › Process › Process step: the services of a domain assembly, the processes that enable each one and their steps in order, with the SIPOCM (supplier, input, process step, output, customer, measure) of every step, where each process and step is reused, the SHACL shapes and assembly checks for each service, and coverage of processes and steps by service. Read only.',
          functions: ['Impact visualization', 'Governance workflow'], std: ['3.1', '3.7', '3.9'] },
        { id: 'model-editor', code: 'ME', file: 'tools/model-editor.html', title: 'Model Editor (classic)', live: true, hidden: true,
          desc: 'The original node-level ontology editor, kept for reference.',
          functions: ['Unified modeling'], std: ['3.1', '3.7', '3.9'] },
        { id: 'relation-taxonomy', code: 'RT', file: 'tools/relation-taxonomy.html', title: 'Relation Taxonomy', live: false,
          desc: 'Families of relations — SKOS for vocabularies and taxonomies, OWL/RDFS for ontologies — that the Model Editor offers and checks against.',
          functions: ['Unified modeling'], std: ['3.9'] },
        { id: 'standards-conformance', code: 'SC', file: 'tools/standards-conformance.html', title: 'Standards Conformance', live: true, isNew: true,
          desc: 'Runs the Part III standards checklist — base URL, naming, acronyms, term definition fields, taxonomy rules, versioning — against GraphDB or a Turtle file.',
          functions: ['Governance workflow', 'Change monitoring'], std: ['3.2', '3.3', '3.7', '3.8', 'E.3'] },
        { id: 'model-visualize', code: 'MV', file: 'tools/model-visualize.html', title: 'Model Visualizer', live: true, hidden: true,
          desc: 'Hierarchy, network and cloud views of one asset. Opened from Model Manager with an asset selected.',
          functions: ['Impact visualization'], std: ['1.3'] },
        { id: 'model-metadata-owl', code: 'MO', file: 'tools/model-metadata-owl.html', title: 'OWL Metadata', live: true, hidden: true },
        { id: 'model-metadata-skos', code: 'MS', file: 'tools/model-metadata-skos.html', title: 'SKOS Metadata', live: true, hidden: true },
        { id: 'model-metadata-tax', code: 'MT', file: 'tools/model-metadata-tax.html', title: 'Taxonomy Metadata', live: true, hidden: true }
      ]
    },
    {
      id: 'rules', label: 'Rules & logic', eyebrow: 'Single source of truth · §3.5',
      blurb: 'The governed rules, constraints, calculations and decision questions that processes and policies depend on.',
      tools: [
        { id: 'ssot-rules-map', code: 'RS', file: 'tools/ssot-rules-map.html', title: 'SSOT Rules & Standards Map',
          desc: 'How rules, standards and logic connect across the SSOT — families, keel and north-star alignment, and what is new.',
          functions: ['Impact visualization'], std: ['3.5'] },
        { id: 'ssot-editor', code: 'SE', file: 'tools/ssot-editor.html', title: 'SSOT Editor',
          desc: 'Edit rules, constraints and logic with change records, impact analysis and generated policy stubs.',
          functions: ['Governance workflow', 'Artifact versioning'], std: ['3.3', '3.5'] },
        { id: 'ssot-dashboard', code: 'SD', file: 'tools/ssot-dashboard.html', title: 'Rules, Constraints & Logic',
          desc: 'Dashboard prototype of rules, constraints and logic for processes and policies.',
          functions: ['Governance workflow'], std: ['3.5'] },
        { id: 'decision-question-baseline', code: 'DQ', file: 'tools/decision-question-baseline.html', title: 'Decision Question Baseline',
          desc: 'Baseline of the decision and competency questions the knowledge must answer, with obligations, permissions and prohibitions.',
          functions: ['Governance workflow'], std: ['A.4'] }
      ]
    },
    {
      id: 'ops', label: 'Agents & operations', eyebrow: 'Operations Workbench · §1.3',
      blurb: 'Run, monitor and review the agentic fabric and the lifecycle of governed artifacts.',
      tools: [
        { id: 'mapping-agent-dashboard', code: 'MA', file: 'tools/mapping-agent-dashboard.html', title: 'Mapping Agent Dashboard',
          desc: 'Simulates the domain-sovereign mapping agents: routing, SHACL → SWRL → PEP validation gate, circuit breakers, human-in-the-loop review and KGCL commits.',
          functions: ['Change monitoring', 'Governance workflow'], std: ['1.5', '2.6'] },
        { id: 'agent-service-map', code: 'AS', file: 'tools/agent-service-map.html', title: 'Agent & Service Map',
          desc: 'Catalog of agents and microservices, their contracts, guardrails and the SSOT rules each depends on.',
          functions: ['Impact visualization'], std: ['2.6'] },
        { id: 'plm-lifecycle-dashboard', code: 'PL', file: 'tools/plm-lifecycle-dashboard.html', title: 'PLM Lifecycle Dashboard',
          desc: 'Lifecycle view of knowledge artifacts from draft to retired, with phase, buffer and critical-path tracking.',
          functions: ['Governance workflow', 'Artifact versioning'], std: ['3.3', '3.4'] }
      ]
    },
    {
      id: 'context', label: 'Domain context', eyebrow: 'Labels & personas · §3.8',
      blurb: 'Who uses which words, and what each group needs.',
      tools: [
        { id: 'peo-buyer-personas', code: 'BP', file: 'tools/peo-buyer-personas.html', title: 'Buyer Personas & Jobs',
          desc: 'Professional employer organization buyer personas with jobs to be done — the persona layer behind persona labels.',
          functions: [], std: ['3.8'] }
      ]
    },
    {
      id: 'reference', label: 'Reference', eyebrow: 'Architecture & standards',
      blurb: 'The architecture and the standards the workbench applies.',
      tools: [
        { id: 'hsga-overview', code: 'HS', file: 'tools/hsga-overview.html', title: 'HSGA Governance Overview',
          desc: 'Holonic Semantic Governance Architecture — seven layers, four domains, the RDSG gateway and compiled governance.',
          functions: [], std: ['2.1'] },
        { id: 'release-notes', code: 'RN', file: 'tools/release-notes.html', title: 'Release Notes', isNew: true,
          desc: 'What changed in each workbench release: new tools and features, improvements and fixes.',
          functions: ['Artifact versioning'], std: [] },
        { id: 'guide', code: 'SG', file: 'docs/Semantic_Governance_v1.9_DRAFT.pdf', title: 'Semantic Governance v1.9',
          desc: 'The standards guide: services, architecture and integration, and Part III knowledge engineering standards.',
          functions: [], std: [] }
      ]
    }
  ]
};
window.KE_TOOLS = {};
window.KE_REGISTRY.groups.forEach(function (g) { g.tools.forEach(function (t) { t.group = g.id; window.KE_TOOLS[t.id] = t; }); });
