# Ingestion report

Run 2026-10-16T01:55:00Z · base URL `https://www.insperity.com/` · author Jeffrey Wallk · version 0.1.0 (Draft)

Standards: Semantic Governance: Services, Architecture & Integration v1.8 (Draft), Part III

## Outputs

| Output | Asset IRI | Terms | Triples | From |
|---|---|---|---|---|
| `ontology-core-asset-0.1.0.ttl` | `https://www.insperity.com/ontology/core-asset/` | 33 | 421 | Ontology_Core_Asset_1_0.ttl |
| `shapes-core-asset-0.1.0.ttl` | `https://www.insperity.com/shapes/core-asset/` | 7 | 107 | Ontology_Core_Asset_1_0.ttl |
| `taxonomy-core-issue-0.1.0.ttl` | `https://www.insperity.com/taxonomy/core-issue/` | 9 | 134 | Taxonomy_Core_Issue_1_0.ttl |
| `vocabulary-core-asset-0.1.0.ttl` | `https://www.insperity.com/vocabulary/core-asset/` | 33 | 385 | core-asset.ttl |

Also written: `crosswalk.csv` (every legacy IRI and its new IRI) and the PROV-O change record.

## Conformance after ingestion

**ontology-core-asset-0.1.0.ttl** — 0 errors, 1 warnings, 12 info
- Named parent class (§3.7): `…/ontology/core-asset/Asset` root class: no named rdfs:subClassOf parent
- Genus plus differentia (§3.7): `…/ontology/core-asset/HumanAsset` does not open "A …/An …": The skills, knowledge, and experience of an organization’s w; `…/ontology/core-asset/DigitalAsset` does not open "A …/An …": Any content or data in digital form that has value and is ow; `…/ontology/core-asset/Analytics` does not open "A …/An …": Tools, algorithms, models, and data that enable an organizat; `…/ontology/core-asset/DataEngineering` does not open "A …/An …": The practice of designing, building, and maintaining systems; `…/ontology/core-asset/FeatureDecomposition` does not open "A …/An …": The process of breaking down a complex feature or product in; `…/ontology/core-asset/KnowledgeEngineering` does not open "A …/An …": The process of capturing, structuring, and representing know (+6 more)

**shapes-core-asset-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

**taxonomy-core-issue-0.1.0.ttl** — 0 errors, 1 warnings, 0 info
- Named parent class (§3.7): `…/taxonomy/core-issue/Issue` root class: no named rdfs:subClassOf parent

**vocabulary-core-asset-0.1.0.ttl** — 0 errors, 0 warnings, 12 info
- Genus plus differentia (§3.7): `…/vocabulary/core-asset/human-asset` does not open "A …/An …": The skills, knowledge, and experience of an organization’s w; `…/vocabulary/core-asset/digital-asset` does not open "A …/An …": Any content or data in digital form that has value and is ow; `…/vocabulary/core-asset/analytics` does not open "A …/An …": Tools, algorithms, models, and data that enable an organizat; `…/vocabulary/core-asset/data-engineering` does not open "A …/An …": The practice of designing, building, and maintaining systems; `…/vocabulary/core-asset/feature-decomposition` does not open "A …/An …": The process of breaking down a complex feature or product in; `…/vocabulary/core-asset/knowledge-engineering` does not open "A …/An …": The process of capturing, structuring, and representing know (+6 more)

## What changed, by asset

On every asset and term the governance fields were rebuilt, not copied: `dct:creator` and (on asset headers) `dct:contributor` are Jeffrey Wallk only; `dct:created` keeps the source date (or the run time when the source had none); `dct:modified` is 2026-10-16T01:55:00Z; `owl:versionInfo` is 0.1.0; lifecycle status is Draft. Labels and definitions were re-tagged `@en`. The source values of those fields are not counted below.

### ontology/core-asset

Removed properties: `oslc:modifiedBy` ×37, `dct:contributor` ×3, `dct:modified` ×3, `vaem:namespace` ×1, `bibo:status` ×1, `skos:changeNote` ×1, `dct:subject` ×1, `<http://verizon.ontologies.com/terms/certified>` ×1

**Corrected**
- …/ontology/core-asset/SystemEngineering: dc:subject pointed at "solution architecture"; re-pointed to …/vocabulary/core-asset/system-engineering

**Filled from existing metadata** (34): …/ontology/core-asset/BusinessSpecification: definition taken from its vocabulary term; …/ontology/core-asset/DataEngineering: definition taken from its vocabulary term; …/ontology/core-asset/DesignSpecification: definition taken from its vocabulary term; …/ontology/core-asset/DesignThinking: definition taken from its vocabulary term; …/ontology/core-asset/DetectiveControls: definition taken from its vocabulary term … and 29 more

**Removed subjects**
- Stub subject https://ontologies.verizon.com/taxonomy-core-valuestream/DataAnalyticsInsights (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-persona/Persona (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-party/Party (no type; only dct:contributor, dct:modified, oslc:modifiedBy)

**Labels put in sentence case** (26): "Business Specification" → "Business specification"; "Data Engineering" → "Data engineering"; "Design Specification" → "Design specification"; "Design Thinking" → "Design thinking"; "Detective Controls" → "Detective controls" … and 21 more

**Review**
- HumanAsset is a subclass of both Biological asset and taxonomy core-party Person, but its definition describes workforce skills, knowledge and experience (an intangible). Decide whether it is a person, or a capability that a person bears.
- PhysicalAsset is a subclass of taxonomy core-product Individual product, which makes every physical asset a product. Check this is intended.
- Data engineering, Design thinking, Feature decomposition, Knowledge engineering, Operational readiness, Quality engineering, Solution architecture and System engineering sit under Artifact, but their definitions describe practices or states, not artifacts. Consider classes for the artifacts they produce (for example Solution architecture description).
- Asset is a root class. Align it to the core ontology (for example a BFO-aligned parent) before the ontology moves to Candidate.

### shapes/core-asset

**Filled from existing metadata**
- owl:imports …/taxonomy/core-lifecycle/ added (referenced by the model)
- owl:imports …/ontology/core-asset/ added (referenced by the model)
- owl:imports …/ontology/core/ added (referenced by the model)
- owl:imports …/taxonomy/core-valuestream/ added (referenced by the model)
- owl:imports …/taxonomy/core-persona/ added (referenced by the model)
- owl:imports …/taxonomy/core-party/ added (referenced by the model)

**Moved**
- https://ontologies.verizon.com/taxonomy-core-persona/PersonaShape → …/shapes/core-asset/PersonaShape
- https://ontologies.verizon.com/ontology-core-asset/AnalyticProductShape → …/shapes/core-asset/AnalyticProductShape
- https://ontologies.verizon.com/ontology-core-asset/AssetShape → …/shapes/core-asset/AssetShape
- https://ontologies.verizon.com/ontology-core-asset/DataProductShape → …/shapes/core-asset/DataProductShape
- https://ontologies.verizon.com/taxonomy-core-party/PartyShape → …/shapes/core-asset/PartyShape
- https://ontologies.verizon.com/taxonomy-core-valuestream/DataAnalyticsInsightsShape → …/shapes/core-asset/DataAnalyticsInsightsShape
- https://ontologies.verizon.com/ontology-core-asset/BiologicalAssetShape → …/shapes/core-asset/BiologicalAssetShape

**Review**
- …/shapes/core-asset/PersonaShape constrains …/taxonomy/core-persona/Persona, a class from another model; it stays with the core-asset shapes because it was authored here
- …/shapes/core-asset/PartyShape constrains …/taxonomy/core-party/Party, a class from another model; it stays with the core-asset shapes because it was authored here
- …/shapes/core-asset/DataAnalyticsInsightsShape constrains …/taxonomy/core-valuestream/DataAnalyticsInsights, a class from another model; it stays with the core-asset shapes because it was authored here

### taxonomy/core-issue

Removed properties: `oslc:modifiedBy` ×10, `vaem:namespace` ×1, `bibo:status` ×1, `skos:changeNote` ×1, `<http://verizon.ontologies.com/terms/certified>` ×1

**Renamed to meet naming rules**
- https://ontologies.verizon.com/taxonomy-core-issue/Major → …/taxonomy/core-issue/MajorDefect ("Major" → "Major defect")
- https://ontologies.verizon.com/taxonomy-core-issue/Minor → …/taxonomy/core-issue/MinorDefect ("Minor" → "Minor defect")
- https://ontologies.verizon.com/taxonomy-core-issue/Needs → …/taxonomy/core-issue/Need ("Needs" → "Need")

**Definitions written**
- …/taxonomy/core-issue/Defect: definition written ("An issue in which a product, service or system does not conform to its specified requirements.")
- …/taxonomy/core-issue/Issue: definition written ("A matter raised by a person or system that a responsible team must track, prioritize and resolve.")
- …/taxonomy/core-issue/Incident: definition written ("A problem that causes an unplanned interruption to a service or a reduction in its quality.")
- …/taxonomy/core-issue/Problem: definition written ("An issue that disrupts or threatens normal operation and whose cause must be investigated and removed.")
- …/taxonomy/core-issue/MajorDefect: definition written ("A defect that prevents or severely impairs an essential function and has no acceptable workaround.")
- …/taxonomy/core-issue/MinorDefect: definition written ("A defect that impairs a non-essential function or that has an acceptable workaround.")
- …/taxonomy/core-issue/Need: definition written ("A request for a capability, resource or change that the requester requires to reach an objective.")
- …/taxonomy/core-issue/Request: definition written ("An issue raised to ask for information, a service or a change rather than to report a fault.")
- …/taxonomy/core-issue/Question: definition written ("A request that asks for information or clarification.")

**Unresolved links**
- …/taxonomy/core-issue/Defect: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/defect
- …/taxonomy/core-issue/Issue: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/issue
- …/taxonomy/core-issue/Incident: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/incident
- …/taxonomy/core-issue/Problem: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/problem
- …/taxonomy/core-issue/MajorDefect: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/major-defect
- …/taxonomy/core-issue/MinorDefect: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/minor-defect
- …/taxonomy/core-issue/Need: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/need
- …/taxonomy/core-issue/Request: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/request
- …/taxonomy/core-issue/Question: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/question

**Review**
- Incident is a subclass of Problem. In ITIL practice an incident is an interruption and a problem is its underlying cause, so they are usually siblings under Issue. The written definitions follow the current hierarchy.
- The core issue vocabulary was not part of this run. dc:subject links point to the IRIs it will have once it is ingested with the same rules.
- Issue is a root class. Align it to the core ontology before the taxonomy moves to Candidate.

### vocabulary/core-asset

Removed properties: `oslc:modifiedBy` ×34, `skos:editorialNote` ×1, `vaem:namespace` ×1, `skos:changeNote` ×1

**Labels put in sentence case** (26): "Analytic Product" → "Analytic product"; "Artificial Intelligence Agent" → "Artificial intelligence agent"; "Autonomous Agent" → "Autonomous agent"; "Biological Asset" → "Biological asset"; "Business Intelligence Agent" → "Business intelligence agent" … and 21 more
