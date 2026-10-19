# Ingestion report

Run 2026-10-17T17:35:37Z · base URL `https://www.insperity.com/` · author Jeffrey Wallk · version 0.1.0 (Draft)

Standards: Semantic Governance: Services, Architecture & Integration v1.8 (Draft), Part III

## Outputs

| Asset | IRI | Terms | Triples | Turtle | TriG | From |
|---|---|---|---|---|---|---|
| Core domain ontology | `https://www.insperity.com/ontology/core-domain/` | 3 | 48 | `ontology-core-domain-0.1.0.ttl` | `ontology-core-domain-0.1.0.trig` | Ontology_Core_Domain_1.0.ttl |
| Core domain shapes | `https://www.insperity.com/shapes/core-domain/` | 24 | 354 | `shapes-core-domain-0.1.0.ttl` | `shapes-core-domain-0.1.0.trig` | Ontology_Core_Domain_1.0.ttl |

Change record: `ttl/change-record-2026-10-17T173537Z.ttl` and `trig/change-record-2026-10-17T173537Z.trig`. Crosswalk of every legacy IRI: `crosswalk.csv`.

## Skipped files

- `BFO Relations.owl` header http://purl.obolibrary.org/obo/ro/core.owl matches no sourceNamespaces pattern in the config; add one for its namespace

## Conformance after ingestion

**ontology-core-domain-0.1.0.ttl** — 1 errors, 1 warnings, 0 info
- No other organization's content: `…/ontology/core-domain/` description names Verizon ("Verizon")
- Named parent class (§3.7): `…/ontology/core-domain/Domain` root class: no named rdfs:subClassOf parent

**shapes-core-domain-0.1.0.ttl** — 0 errors, 1 warnings, 0 info
- Identifier case (§3.2): `…/shapes/core-domain/core-serviceShape` shape not {Class}Shape

## What changed, by asset

On every asset and term the governance fields were rebuilt, not copied: `dct:creator` and (on asset headers) `dct:contributor` are Jeffrey Wallk only; `dct:created` keeps the source date (or the run time when the source had none); `dct:modified` is 2026-10-17T17:35:37Z; `owl:versionInfo` is 0.1.0; lifecycle status is Draft. Labels and definitions were re-tagged `@en`. The source values of those fields are not counted below.

### ontology/core-domain

Kept for review: 2 terms from other namespaces that carry content (labels, types or links); resolve them in Conformance Review

Removed properties: `dct:contributor` ×27, `oslc:modifiedBy` ×26, `dct:modified` ×24, `rdfs:subClassOf` ×5, `vaem:namespace` ×1, `bibo:status` ×1, `skos:changeNote` ×1, `dct:subject` ×1, `<http://verizon.ontologies.com/terms/certified>` ×1

**Written during ingestion**
- Title written: "Core domain ontology" (add an entry under "assets" in the config to change it)

**Filled from existing metadata**
- …/ontology/core-domain/Domain: definition taken from its vocabulary term

**Removed subjects**
- Stub subject https://ontologies.metaphacts.com/core-taxonomy-(service)/OperationsManagement (no type; only rdfs:subClassOf)
- Stub subject https://ontologies.metaphacts.com/core-taxonomy-(service)/Communications (no type; only rdfs:subClassOf)
- Stub subject https://ontologies.metaphacts.com/core-taxonomy-(service)/ServiceLevelManagement (no type; only rdfs:subClassOf)
- Stub subject https://ontologies.metaphacts.com/taxonomy/core/service/Reporting (no type; only rdfs:subClassOf)
- Stub subject https://ontologies.metaphacts.com/taxonomy/core/service/Training (no type; only rdfs:subClassOf)
- Stub subject http://www.semanticweb.org/wallkje/ontologies/2024/event/Events (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-process/Process (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-rules/Rules (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/ontology-core-event/Event (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/ontology-core-asset/DigitalAsset (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/ontology-core-asset/PhysicalAsset (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-issue/Issue (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-role/Role (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-compliance/Compliance (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-valuestream/ValueStream (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-persona/Persona (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.verizon.com/taxonomy-core-services/Services (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy-core-process/Process (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/common-core-ontology/Party (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy-core-asset/PhysicalAsset (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy-core-asset/DigitalAsset (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/core-taxonomy-(persona)/Persona (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/core-taxonomy-(value-stream)/ValueStream (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/ontology-core-services/Service (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy-core-service (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/core-taxonomy-(role)/Role (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy-core-rules/Rules (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy/core/compliance/copy/Compliance (no type; only dct:contributor, dct:modified, oslc:modifiedBy)
- Stub subject https://ontologies.metaphacts.com/taxonomy-core-issue/Issue (no type; only dct:contributor, dct:modified, oslc:modifiedBy)

### shapes/core-domain

**Filled from existing metadata** (18): owl:imports …/taxonomy/core-issue/ added (referenced by the model); owl:imports …/ontology/core/ added (referenced by the model); owl:imports …/taxonomy/core-rules/ added (referenced by the model); owl:imports …/taxonomy/core-asset/ added (referenced by the model); owl:imports …/taxonomy/core-location/ added (referenced by the model) … and 13 more

**Moved**
- https://ontologies.metaphacts.com/taxonomy-core-serviceShape → …/shapes/core-domain/core-serviceShape
- https://ontologies.metaphacts.com/taxonomy-core-process/ProcessShape → …/shapes/core-domain/ProcessShape
- http://www.semanticweb.org/wallkje/ontologies/2024/event/EventsShape → …/shapes/core-domain/EventsShape
- https://ontologies.metaphacts.com/core-taxonomy-(value-stream)/ValueStreamShape → …/shapes/core-domain/ValueStreamShape
- https://ontologies.metaphacts.com/common-core-ontology/PartyShape → …/shapes/core-domain/PartyShape
- https://ontologies.metaphacts.com/core-taxonomy-(persona)/PersonaShape → …/shapes/core-domain/PersonaShape
- https://ontologies.metaphacts.com/taxonomy-core-rules/RulesShape → …/shapes/core-domain/RulesShape
- https://ontologies.metaphacts.com/taxonomy/core/compliance/copy/ComplianceShape → …/shapes/core-domain/ComplianceShape
- https://ontologies.metaphacts.com/taxonomy-core-issue/IssueShape → …/shapes/core-domain/IssueShape
- https://ontologies.metaphacts.com/core-taxonomy-(role)/RoleShape → …/shapes/core-domain/RoleShape
- https://ontologies.metaphacts.com/taxonomy-core-asset/DigitalAssetShape → …/shapes/core-domain/DigitalAssetShape
- https://ontologies.metaphacts.com/taxonomy-core-asset/PhysicalAssetShape → …/shapes/core-domain/PhysicalAssetShape
- https://ontologies.metaphacts.com/ontology-core-services/ServiceShape → …/shapes/core-domain/ServiceShape
- https://ontologies.verizon.com/taxonomy-core-compliance/ComplianceShape → …/shapes/core-domain/ComplianceShape
- https://ontologies.verizon.com/taxonomy-core-persona/PersonaShape → …/shapes/core-domain/PersonaShape
- https://ontologies.verizon.com/ontology-core-asset/DigitalAssetShape → …/shapes/core-domain/DigitalAssetShape
- https://ontologies.verizon.com/ontology-core-asset/PhysicalAssetShape → …/shapes/core-domain/PhysicalAssetShape
- https://ontologies.verizon.com/ontology-core-event/EventShape → …/shapes/core-domain/EventShape
- https://ontologies.verizon.com/taxonomy-core-issue/IssueShape → …/shapes/core-domain/IssueShape
- https://ontologies.verizon.com/taxonomy-core-process/ProcessShape → …/shapes/core-domain/ProcessShape
- https://ontologies.verizon.com/taxonomy-core-role/RoleShape → …/shapes/core-domain/RoleShape
- https://ontologies.verizon.com/taxonomy-core-rules/RulesShape → …/shapes/core-domain/RulesShape
- https://ontologies.verizon.com/taxonomy-core-services/ServicesShape → …/shapes/core-domain/ServicesShape
- https://ontologies.verizon.com/taxonomy-core-valuestream/ValueStreamShape → …/shapes/core-domain/ValueStreamShape

**Review**
- …/shapes/core-domain/core-serviceShape constrains …/taxonomy/core-service/, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ProcessShape constrains …/taxonomy/core-process/Process, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/EventsShape constrains http://www.semanticweb.org/wallkje/ontologies/2024/event/Events, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ValueStreamShape constrains https://ontologies.metaphacts.com/core-taxonomy-(value-stream)/ValueStream, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/PartyShape constrains https://ontologies.metaphacts.com/common-core-ontology/Party, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/PersonaShape constrains https://ontologies.metaphacts.com/core-taxonomy-(persona)/Persona, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/RulesShape constrains …/taxonomy/core-rules/Rules, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ComplianceShape constrains https://ontologies.metaphacts.com/taxonomy/core/compliance/copy/Compliance, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/IssueShape constrains …/taxonomy/core-issue/Issue, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/RoleShape constrains https://ontologies.metaphacts.com/core-taxonomy-(role)/Role, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/DigitalAssetShape constrains …/taxonomy/core-asset/DigitalAsset, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/PhysicalAssetShape constrains …/taxonomy/core-asset/PhysicalAsset, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ServiceShape constrains …/ontology/core-services/Service, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ComplianceShape constrains https://ontologies.metaphacts.com/taxonomy/core/compliance/copy/Compliance, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/PersonaShape constrains https://ontologies.metaphacts.com/core-taxonomy-(persona)/Persona, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/DigitalAssetShape constrains …/taxonomy/core-asset/DigitalAsset, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/PhysicalAssetShape constrains …/taxonomy/core-asset/PhysicalAsset, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/EventShape constrains …/ontology/core-event/Event, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/IssueShape constrains …/taxonomy/core-issue/Issue, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ProcessShape constrains …/taxonomy/core-process/Process, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/RoleShape constrains https://ontologies.metaphacts.com/core-taxonomy-(role)/Role, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/RulesShape constrains …/taxonomy/core-rules/Rules, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ServicesShape constrains …/taxonomy/core-services/Services, a class from another model; it stays with the core-domain shapes because it was authored here
- …/shapes/core-domain/ValueStreamShape constrains https://ontologies.metaphacts.com/core-taxonomy-(value-stream)/ValueStream, a class from another model; it stays with the core-domain shapes because it was authored here
