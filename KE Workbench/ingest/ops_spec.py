'''Operations Dashboard: authored policy and standards content (read by build_ops_snapshot.py).

GUIDE     where Semantic Governance v1.9 (Draft) no longer matched how the core and domains are built, with the
          decision or release that changed it and the change made in the next edition;
RESOLUTION, per edition, where each GUIDE item is resolved (Appendix E.4 of that edition) and its status;
POLICIES  the process policies the change log is checked against (Part III §3.3, §3.4);
CATEGORIES and PRIORITIES for the action list.
'''

# The current edition is read from assets/ke-guide.js (written by ingest/guide_sync.py); these are fallbacks.
GUIDE_EDITION = '2.0'
GUIDE_NEXT = '2.1'


def G(id, section, topic, v19, practice, sources, change, priority='high', kind='update'):
    return dict(id=id, section=section, topic=topic, v19=v19, practice=practice, sources=sources, change=change,
                priority=priority, kind=kind)


GUIDE = [
    G('G01', '3.2', 'Identifiers of classes and taxonomy concepts',
      'Classes and taxonomy concepts use UpperCamelCase identifiers (PayrollRun, WagesAndHours); the same rule is repeated in §3.6, §3.11 and Appendix E.',
      'Classes, taxonomy concepts and vocabulary terms join their primitives with hyphens in lower case (…/ontology/core/process-step, …/taxonomy/core-process/approval-step). Labels are spaced phrases; concatenating primitives creates new words.',
      ['Baseline Core decision 5', 'Workbench 3.0.0 (Baseline Core v1.0)', 'Customer 360 schema 0.3.0'],
      'Rewrite the naming table: one identifier rule for classes, concepts and terms (hyphen-joined primitives, lower case); keep lowerCamelCase for properties; state the instance rule (G02). Update every example in §3.2, §3.6, §3.11, Appendix A and Appendix E.'),
    G('G02', '3.2', 'Identifiers of individuals and instance graphs',
      'Individuals use UpperCamelCase names or a class name plus a stable identifier (TexasMinimumWageAct, Worksite-000123); instance data lives at resource/{domain}/{Class}/{id}.',
      'Instance IRIs are mixed: assemblies use …/resource/domain-<L1>/… with hyphenated local names; Customer 360 uses ob:Job-J01, ob:Outcome-O001 and ob:BusinessOwner; change records use resource/change-log/ChangeRecord/{stamp}-{tool}.',
      ['D17', 'D18', 'Customer 360 0.3.0', 'change records'],
      'Decide one instance rule (recommended: …/resource/{scope}/{class}/{stable-id}, class in the same hyphenated form as G01) and record the exceptions that stay for stability (identifier-coded instances such as O001).', 'medium', 'decide'),
    G('G03', '3.2', 'URI patterns for core, areas and nested domains',
      'One pattern per element with the domain name in lower case (…/ontology/payroll/, …/taxonomy/compliance/), and an operational module at …/ontology/operational/.',
      'Core assets are split by facet (…/vocabulary/core-process/, …/taxonomy/core-process/, …/ontology/core/); operational areas use …/<kind>/<area>/; domains use …/<kind>/domain-<L1>[.<L2>[.<L3>]]/ with levels joined by dots and & written "and"; the APQC registry is …/taxonomy/apqc-pcf/.',
      ['D26', 'Workbench 3.6.0', 'Workbench 3.9.0'],
      'Replace the URI table with the core-facet, area and dotted-domain patterns and their prefixes (salesvoc:, commercialopsvoc:), and drop the payroll and compliance examples that no longer exist.'),
    G('G04', '3.2, 3.11', 'Named graph pattern',
      'Each artifact’s current release is held in …/graph/{artifact-type}/{domain}[/{SchemeName}].',
      'The named graph is the asset IRI itself (…/ontology/domain-sales/); other graphs are …/graph/change-log, …/graph/customer-360/…, record and party graphs (…/record-graph/commercial-records/, …/party-graph/commercial-parties/) and one graph per assembly component.',
      ['D4', 'D17', 'Workbench 1.4.0', 'Workbench 4.1.0'],
      'Adopt "named graph = asset IRI" for models (it is what every loader and editor relies on), and list the reserved graph families for logs, records, parties, components and Customer 360.'),
    G('G05', '3.2', 'Asset titles (naming standard)',
      'No rule for asset titles.',
      'Asset names take a first qualifier (Core, Domain L1.L2.L3, or the area name) and a second qualifier (Vocabulary, Taxonomy, Ontology): "Domain Sales Vocabulary", "Commercial Operations Ontology"; HR is spelled out with the short form as alternative label.',
      ['D26'],
      'Add the title standard next to the identifier rules.', 'medium'),
    G('G06', '3.1', 'Operational modules versus operational areas',
      'Inter-domain properties live in an operational module (…/ontology/operational/) that imports the domains it connects, with joint ownership.',
      'Four operational areas (Business, Commercial, HR Service, Technical Operations) aggregate domains; each area has a container (D2). Classes, relations, concepts and imports refer only to the core, the area, parent domains and the domain itself; cross-area composition happens only in the enterprise service catalog (D25, D27). "Operational" now names the areas, not a module.',
      ['D2', 'D25', 'D26', 'D27'],
      'Rewrite "Operational Domains" in §3.1: areas and containers, the insulation rule, and the enterprise service catalog as the only cross-area composition point. Rename or retire "operational module" to avoid the clash, and update §1.3, §2.1 and the Human in the Loop table.'),
    G('G07', '3.1, 3.7', 'Primitives and polymorphic terms',
      'Vocabularies hold preferred terms and synonyms; §3.11 introduces core:hasPrimaryTerm.',
      'Vocabularies hold primitives only (unique across core and domains; multiword lexical units allowed; adjectives become their noun primitive). Concepts link to every primitive with dcterms:subject and to the head with core:hasPrimaryTerm; domains specialize core concepts with skos:broadMatch and never copy them; promotion candidates are flagged for the core.',
      ['Baseline Core decisions 1–8, 30', 'D6', 'D7', 'D8'],
      'Add a "Primitives" subsection to §3.7 with the rules, the promotion process and the build checks that enforce them.'),
    G('G08', '3.10', 'Reference ontologies and the formalization stack',
      'Company relations are subproperties of BFO or RO relations; taxonomies stay SKOS and reach meaning through core:formalizedBy.',
      'Stack: BFO 2020 ← RO Core + RO extract ← core domain ontology ← area container ← domain. BFO and RO keep their own IRIs and named graphs; domain ontologies pin imports of the core and container (D3); every domain class reaches BFO through a core class (D5).',
      ['Workbench 2.1.0', 'Workbench 2.2.0', 'D3', 'D5'],
      'Add the load order and the stack diagram; state the pinned-import rule.', 'medium'),
    G('G09', '3.3', 'Change record model',
      'core:ChangeRecord with core:implementsFeature, core:changeType (KGCL), core:changeCommand, core:affectsArtifact, core:versionBump, added/removed triple graphs, core:approvedBy, core:releasedIn and a pull request link.',
      'Every tool writes a PROV-O record: prov:Activity + dcterms:ProvenanceStatement at …/resource/change-log/ChangeRecord/{stamp}-{tool}, with dcterms:description, creator and contributor, prov:startedAtTime/endedAtTime, prov:used, prov:generated, prov:invalidated, and dcterms:hasPart entries (label, comment, dcterms:subject, dcterms:type). Approver, requirement, version bump and KGCL type are not recorded.',
      ['Workbench 1.4.0', '1.5.0', '3.1.0', 'build scripts'],
      'Make §3.3 describe the PROV-O profile that is implemented, and keep the governance fields as required extensions: core:approvedBy, core:implementsFeature (requirement), core:versionBump and core:changeType. Close the tool side with action P03/P04.'),
    G('G10', '3.3', 'Deployment records and the release pipeline',
      'A five-stage pipeline with release packages, a deployment log graph (core:DeploymentRecord) and nightly drift checks.',
      'Loading is done by graphdb-load.command and graphdb-rebuild.command (backup, replace graphs, lineage check) and by the workbench’s Load into GraphDB; no deployment record is written and there is one environment.',
      ['D4', 'Workbench 2.2.0'],
      'State the current single-environment practice as stage 1 of the target pipeline, and have the load scripts write a deployment record (action P05).', 'medium'),
    G('G11', '3.3', 'Versioning before 1.0.0',
      'MAJOR / MINOR / PATCH by schema diff.',
      'Assets start at 0.1.0 as Draft; Conformance Review bumps PATCH for edits and MINOR before 1.0.0 (MAJOR after) for removals and new identifiers; a metadata save bumps PATCH.',
      ['Workbench 1.5.0', '§3.3 (current)'],
      'Add the pre-1.0 rule and the bump each tool applies.', 'low'),
    G('G12', '3.3, 3.4', 'Lifecycle promotion criteria',
      'Draft → Candidate → Released → Deprecated → Retired, mapped to environments.',
      'Every asset is Draft; no criteria say when a Draft becomes a Candidate.',
      ['Asset inventory'],
      'Define Candidate entry criteria (0 conformance errors, open questions on the asset closed, SME review recorded, shapes executed) so the dashboard can report readiness.', 'high', 'decide'),
    G('G13', '3.4', 'Human review and learning loop',
      'Human in the Loop table by artifact; quality gates by SHACL.',
      'Conformance Review records dispositions (fix, accept, not an issue, defer, escalate) that later ingestions replay; loading is blocked by named rules (loadBlockingRules); business and compliance SMEs review Customer 360 items in GraphDB.',
      ['Workbench 2.0.0', '3.3.0', '4.1.0'],
      'Add dispositions, load gates and SME review to §3.4 as the implemented quality gates.', 'medium'),
    G('G14', '3.8', 'Personas and jobs to be done',
      'Persona labels via core:intendedForPersona with persona IRIs such as …/vocabulary/persona/SoftwareDeveloper.',
      'One persona model, no role typing (Baseline 22–23); personas are assembled with jobs, job steps and desired outcomes (Baseline 16–21) in the Customer 360 ontology (jtbd:client-persona, jtbd:desired-outcome) aligned to core:persona, core:job, core:job-step; persona vocabulary is …/vocabulary/core-persona/.',
      ['Baseline Core decisions 16–23', 'Workbench 4.0.0'],
      'Split §3.8 into labels-for-personas (unchanged rule, new IRIs) and a new subsection on the persona and jobs model.'),
    G('G15', '3.1, 3.9', 'Service assembly model and process registry',
      'No service assembly model; process steps anchor the unifying ontology.',
      'Service › Process › Process step with SIPOCM per step (D17–D24); domain process levels are APQC PCF 7.4 (process group › process › activity › task; D28) from one reference registry with one owner per element (D29); external services follow the business model (D25).',
      ['D17–D24', 'D28', 'D29'],
      'Add a §3.12 "Services, processes and the reference registry".'),
    G('G16', '1.3, 2.1', 'Operating model: areas, domains and the service catalog',
      'Domains and the core; domain stewards; no operational areas.',
      'Enterprise › operational area › domain (L1–L3) › services and processes; two portfolios (internal on APQC, external on the business model) in one enterprise service catalog.',
      ['D25', 'D26'],
      'Update the operating model and architecture views; add area stewardship to the RACI.', 'medium'),
    G('G17', 'Appendix E', 'Tooling: RDF Studio steps',
      'Appendix E is a stepwise guide in RDF Studio.',
      'The KE Workbench does ingestion, conformance review, editing (vocabulary, taxonomy, ontology), service assembly, Customer 360 and operations.',
      ['Workbench releases 1.4.0–4.4.0'],
      'Replace or supplement Appendix E with the workbench procedure (one step per tool) and keep RDF Studio as an alternative.', 'medium'),
    G('G18', 'Appendix A', 'Worked example',
      'FP&A example with UpperCamelCase classes and …/ontology/finance/ IRIs.',
      'Finance is a Business Operations domain (…/ontology/domain-finance/) not yet built.',
      ['D26'],
      'Re-key the example to the new identifiers and URI patterns, or replace it with Domain Sales, which is built and assembled.', 'low'),
    G('G19', 'Appendix F', 'Glossary',
      'Terms through v1.9.',
      'New terms in use: primitive, polymorphic term, multiword lexical unit, operational area, container domain, bounded context, domain service, enterprise service catalog, service assembly, SIPOCM, job map stage, desired outcome, disposition, load gate, circuit breaker.',
      ['Baseline Core decisions', 'D-series'],
      'Add the entries in alphabetical order.', 'low'),
    G('G20', '1.2, 2.6', 'Measured agent assurance',
      'Circuit breakers and human review in the agent pattern.',
      'Proposed: reference question sets from Customer 360, measured accuracy and groundedness with uncertainty, release-level measurement records, thresholds that trip circuit breakers (PEO Service Map proposals A02–A04).',
      ['PEO Service Map expansion (Draft)'],
      'Add a metrology subsection once the proposals are decided.', 'low', 'consider'),
    G('G21', 'Front matter', 'Edition and conformance claims',
      'v1.9 Draft, 2026-10-15.',
      'Every asset and generated file declares dcterms:conformsTo the v1.9 edition and "Standards: … v1.9" in its header.',
      ['ke-ingest.config.json conformsTo'],
      'Publish v2.0 (MAJOR: identifier and URI rules change), then update conformsTo in the configuration and rebuild the core and domains so assets claim the edition they meet.', 'high'),
]


def P(id, title, check, standard, priority):
    return dict(id=id, title=title, check=check, standard=standard, priority=priority)


# status: resolved | decide (written as a proposal, decision pending) | tools (resolved in the guide; tool work open)
RESOLUTION = {
    '2.0': {
        'G01': ('resolved', '§3.2 Naming Conventions; examples throughout'),
        'G02': ('decide', '§3.2 Instance Identifiers (proposed)'),
        'G03': ('resolved', '§3.2 URI Conventions'),
        'G04': ('resolved', '§3.2 Named Graphs; §3.11'),
        'G05': ('resolved', '§3.2 Asset Titles'),
        'G06': ('resolved', '§3.1 Operational Areas, Containers, and Insulation; §1.3; §3.3 Human in the Loop'),
        'G07': ('resolved', '§3.7 Primitives and Polymorphic Terms'),
        'G08': ('resolved', '§3.10 Reference Ontology Stack and Load Order'),
        'G09': ('tools', '§3.3 Change Record Profile (approver and requirement: policies P03, P04)'),
        'G10': ('tools', '§3.3 Current Practice (deployment records: policy P05)'),
        'G11': ('resolved', '§3.3 Versioning'),
        'G12': ('decide', '§3.3 Candidate Entry Criteria (proposed)'),
        'G13': ('resolved', '§3.4 Implemented Quality Gates; §3.6 Recursive Learning'),
        'G14': ('resolved', '§3.8 The Persona Model; §3.13'),
        'G15': ('resolved', '§3.12 Services, Processes, and the Reference Registry'),
        'G16': ('resolved', '§1.3; §3.1'),
        'G17': ('resolved', 'Appendix E (KE Workbench)'),
        'G18': ('resolved', 'Appendix A (identifiers and URIs re-keyed)'),
        'G19': ('resolved', 'Appendix F'),
        'G20': ('decide', '§3.6 Measured Agent Assurance (proposed)'),
        'G21': ('tools', 'Front matter; §3.11 Edition Conformance (rebuild assets: policy P07)'),
    },
}

POLICIES = [
    P('P01', 'Every change set has a change record', 'Assets in the inventory that no change record generated, revised or used.', '§3.3 Change Log Structure', 'high'),
    P('P02', 'Change records name who made the change', 'Records with dcterms:creator.', '§3.3, W3C PROV', 'medium'),
    P('P03', 'Change records name who approved the change', 'Records with core:approvedBy (or prov:wasAssociatedWith in an approver role).', '§3.3 Human in the Loop', 'high'),
    P('P04', 'Change records trace to a requirement', 'Records with core:implementsFeature or a link to a demand request.', '§3.3, ORSD (Appendix A.4)', 'high'),
    P('P05', 'Deployments are recorded', 'Deployment records in …/graph/deployment-log.', '§3.3 Deployment Records', 'medium'),
    P('P06', 'Records are closed', 'Records with prov:endedAtTime.', '§3.3', 'low'),
    P('P07', 'Assets declare the current guide edition', 'Assets whose dcterms:conformsTo is the latest edition of the guide.', '§3.11', 'medium'),
    P('P08', 'Assets have one current copy', 'An asset IRI found in more than one current file, at different versions.', '§3.3 Release Pipeline, D4', 'medium'),
    P('P09', 'Assets move through the lifecycle', 'Assets beyond Draft (Candidate or Released).', '§3.3 Lifecycle Management', 'medium'),
]

CATEGORIES = ['Conformance', 'Process policy', 'Standards guide', 'Decision', 'Lifecycle', 'Portfolio']
PRIORITIES = ['high', 'medium', 'low']
