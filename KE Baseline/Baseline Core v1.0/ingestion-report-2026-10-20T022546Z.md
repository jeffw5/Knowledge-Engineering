# Ingestion report

Run 2026-10-20T02:25:46Z · base URL `https://www.insperity.com/` · author Jeffrey Wallk · version 0.1.0 (Draft)

Standards: Semantic Governance: Services, Architecture & Integration v1.9 (Draft), Part III

## Outputs

| Asset | IRI | Terms | Triples | Turtle | TriG | From |
|---|---|---|---|---|---|---|
| Domain sales ontology | `https://www.insperity.com/ontology/domain-sales/` | 3 | 76 | `ontology-domain-sales-0.1.0.ttl` | `ontology-domain-sales-0.1.0.trig` | ontology-domain-sales-0.1.0.ttl |
| Domain sales shapes | `https://www.insperity.com/shapes/domain-sales/` | 2 | 54 | `shapes-domain-sales-0.1.0.ttl` | `shapes-domain-sales-0.1.0.trig` | shapes-domain-sales-0.1.0.ttl |
| Domain sales taxonomy | `https://www.insperity.com/taxonomy/domain-sales/` | 38 | 596 | `taxonomy-domain-sales-0.1.0.ttl` | `taxonomy-domain-sales-0.1.0.trig` | taxonomy-domain-sales-0.1.0.ttl |
| Domain sales vocabulary | `https://www.insperity.com/vocabulary/domain-sales/` | 11 | 155 | `vocabulary-domain-sales-0.1.0.ttl` | `vocabulary-domain-sales-0.1.0.trig` | vocabulary-domain-sales-0.1.0.ttl |

Change record: `ttl/change-record-2026-10-20T022546Z.ttl` and `trig/change-record-2026-10-20T022546Z.trig`. Crosswalk of every legacy IRI: `crosswalk.csv`.

## Conformance after ingestion

**ontology-domain-sales-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

**shapes-domain-sales-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

**taxonomy-domain-sales-0.1.0.ttl** — 25 errors, 3 warnings, 0 info
- Taxonomy term in a vocabulary (§3.11): `…/taxonomy/domain-sales/buying-committee` linked to …/vocabulary/core-governance/buying-committee, …/vocabulary/domain-commercial-operations/buying-committee, which is in no vocabulary; `…/taxonomy/domain-sales/buying-role` linked to …/vocabulary/core-role/buying-role, …/vocabulary/domain-commercial-operations/buying-role, which is in no vocabulary; `…/taxonomy/domain-sales/economic-buyer` linked to …/vocabulary/core-value/economic-buyer, …/vocabulary/domain-commercial-operations/economic-buyer, which is in no vocabulary; `…/taxonomy/domain-sales/influencer` linked to …/vocabulary/domain-commercial-operations/influencer, …/vocabulary/domain-commercial-operations/influencer, which is in no vocabulary; `…/taxonomy/domain-sales/sales-measure` linked to …/vocabulary/core-domain/sales-measure, …/vocabulary/core-measure/sales-measure, which is in no vocabulary; `…/taxonomy/domain-sales/average-opportunity-size` linked to …/vocabulary/core-measure/average-opportunity-size, …/vocabulary/domain-commercial-operations/average-opportunity-size, which is in no vocabulary (+22 more)

**vocabulary-domain-sales-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

## What changed, by asset

On every asset and term the governance fields were rebuilt, not copied: `dct:creator` and (on asset headers) `dct:contributor` are Jeffrey Wallk only; `dct:created` keeps the source date (or the run time when the source had none); `dct:modified` is 2026-10-20T02:25:46Z; `owl:versionInfo` is 0.1.0; lifecycle status is Draft. Labels and definitions were re-tagged `@en`. The source values of those fields are not counted below.

### ontology/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×4, `dct:conformsTo` ×2, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `skos:editorialNote` ×1, `skos:changeNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales ontology" (add an entry under "assets" in the config to change it)

**Filled from existing metadata**
- owl:imports …/ontology/core/ added (referenced by the model)

**Unresolved links**
- …/ontology/domain-sales/selling-process: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-process
- …/ontology/domain-sales/selling-process: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-process
- …/ontology/domain-sales/selling-step: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-step
- …/ontology/domain-sales/selling-step: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-step

### shapes/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×3, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `dct:conformsTo` ×1, `skos:editorialNote` ×1, `skos:changeNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales shapes" (add an entry under "assets" in the config to change it)

**Filled from existing metadata**
- owl:imports …/ontology/domain-sales/ added (referenced by the model)
- owl:imports …/ontology/core/ added (referenced by the model)

**Moved**
- …/shapes/domain-sales/selling-step-shape → …/shapes/domain-sales/selling-step-shape
- …/shapes/domain-sales/quota-shape → …/shapes/domain-sales/quota-shape

### taxonomy/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×39, `dct:source` ×14, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `dct:conformsTo` ×1, `skos:editorialNote` ×1, `skos:changeNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales taxonomy" (add an entry under "assets" in the config to change it)

**Unresolved links**
- …/taxonomy/domain-sales/selling-stage: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/selling-stage
- …/taxonomy/domain-sales/selling-stage: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/selling-stage
- …/taxonomy/domain-sales/selling-stage: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/selling-stage
- …/taxonomy/domain-sales/qualify: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/qualify
- …/taxonomy/domain-sales/qualify: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/qualify
- …/taxonomy/domain-sales/evaluate: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/evaluate
- …/taxonomy/domain-sales/evaluate: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/evaluate
- …/taxonomy/domain-sales/propose: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/propose
- …/taxonomy/domain-sales/propose: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/propose
- …/taxonomy/domain-sales/decide: vocabulary core-decision was not in this run; dc:subject set to the expected IRI …/vocabulary/core-decision/decide
- …/taxonomy/domain-sales/decide: vocabulary core-decision was not in this run; dc:subject set to the expected IRI …/vocabulary/core-decision/decide
- …/taxonomy/domain-sales/onboard: vocabulary core-event was not in this run; dc:subject set to the expected IRI …/vocabulary/core-event/onboard
- …/taxonomy/domain-sales/onboard: vocabulary core-event was not in this run; dc:subject set to the expected IRI …/vocabulary/core-event/onboard
- …/taxonomy/domain-sales/selling-activity: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-activity
- …/taxonomy/domain-sales/selling-activity: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/selling-activity
- …/taxonomy/domain-sales/selling-activity: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-activity
- …/taxonomy/domain-sales/objection-handling: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/objection-handling
- …/taxonomy/domain-sales/client-handoff: vocabulary core-event was not in this run; dc:subject set to the expected IRI …/vocabulary/core-event/client-handoff
- …/taxonomy/domain-sales/client-handoff: vocabulary core-event was not in this run; dc:subject set to the expected IRI …/vocabulary/core-event/client-handoff
- …/taxonomy/domain-sales/client-handoff: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/client-handoff
- …/taxonomy/domain-sales/buying-role: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/buying-role
- …/taxonomy/domain-sales/buying-role: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/buying-role
- …/taxonomy/domain-sales/buying-role: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/buying-role
- …/taxonomy/domain-sales/economic-buyer: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/economic-buyer
- …/taxonomy/domain-sales/economic-buyer: vocabulary core-value was not in this run; dc:subject set to the expected IRI …/vocabulary/core-value/economic-buyer
- …/taxonomy/domain-sales/economic-buyer: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/economic-buyer
- …/taxonomy/domain-sales/influencer: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/influencer
- …/taxonomy/domain-sales/influencer: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/influencer
- …/taxonomy/domain-sales/buying-committee: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/buying-committee
- …/taxonomy/domain-sales/buying-committee: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/buying-committee
- …/taxonomy/domain-sales/buying-committee: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/buying-committee
- …/taxonomy/domain-sales/sales-role: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-role
- …/taxonomy/domain-sales/sales-role: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-role
- …/taxonomy/domain-sales/sales-role: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-role
- …/taxonomy/domain-sales/sales-representative: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-representative
- …/taxonomy/domain-sales/sales-representative: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-representative
- …/taxonomy/domain-sales/sales-representative: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-representative
- …/taxonomy/domain-sales/sales-manager: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-manager
- …/taxonomy/domain-sales/sales-manager: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-manager
- …/taxonomy/domain-sales/sales-manager: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-manager
- …/taxonomy/domain-sales/sales-executive: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-executive
- …/taxonomy/domain-sales/sales-executive: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-executive
- …/taxonomy/domain-sales/sales-executive: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/sales-executive
- …/taxonomy/domain-sales/sales-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/sales-plan
- …/taxonomy/domain-sales/sales-plan: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-plan
- …/taxonomy/domain-sales/sales-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/sales-plan
- …/taxonomy/domain-sales/account-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/account-plan
- …/taxonomy/domain-sales/account-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/account-plan
- …/taxonomy/domain-sales/account-plan: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/account-plan
- …/taxonomy/domain-sales/territory-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/territory-plan
- …/taxonomy/domain-sales/territory-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/territory-plan
- …/taxonomy/domain-sales/territory-plan: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/territory-plan
- …/taxonomy/domain-sales/sales-incentive: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/sales-incentive
- …/taxonomy/domain-sales/sales-incentive: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-incentive
- …/taxonomy/domain-sales/sales-incentive: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/sales-incentive
- …/taxonomy/domain-sales/sales-record: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/sales-record
- …/taxonomy/domain-sales/sales-record: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/sales-record
- …/taxonomy/domain-sales/sales-record: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-record
- …/taxonomy/domain-sales/sales-measure: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/sales-measure
- …/taxonomy/domain-sales/sales-measure: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-measure
- …/taxonomy/domain-sales/sales-measure: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/sales-measure
- …/taxonomy/domain-sales/quota-attainment: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/quota-attainment
- …/taxonomy/domain-sales/quota-attainment: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/quota-attainment
- …/taxonomy/domain-sales/sales-forecast: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/sales-forecast
- …/taxonomy/domain-sales/sales-forecast: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-forecast
- …/taxonomy/domain-sales/sales-forecast: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/sales-forecast
- …/taxonomy/domain-sales/sales-cycle-length: vocabulary core-time was not in this run; dc:subject set to the expected IRI …/vocabulary/core-time/sales-cycle-length
- …/taxonomy/domain-sales/sales-cycle-length: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-cycle-length
- …/taxonomy/domain-sales/sales-cycle-length: vocabulary core-time was not in this run; dc:subject set to the expected IRI …/vocabulary/core-time/sales-cycle-length
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/average-opportunity-size
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/average-opportunity-size
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/average-opportunity-size
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/average-opportunity-size
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/worksite-employees-sold
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary core-location was not in this run; dc:subject set to the expected IRI …/vocabulary/core-location/worksite-employees-sold
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/worksite-employees-sold
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary domain-commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/domain-commercial-operations/worksite-employees-sold

**Review**
- …/taxonomy/domain-sales/selling-stage: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/selling-activity: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/objection-handling: linked vocabulary term is labelled "objection"
- …/taxonomy/domain-sales/objection-handling: linked vocabulary term is labelled "objection"
- …/taxonomy/domain-sales/objection-handling: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/client-handoff: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/buying-role: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/economic-buyer: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/buying-committee: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-role: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-representative: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-manager: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-executive: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-plan: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/account-plan: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/territory-plan: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-incentive: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-record: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-measure: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/quota-attainment: linked vocabulary term is labelled "quota"
- …/taxonomy/domain-sales/quota-attainment: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-forecast: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-cycle-length: linked vocabulary term is labelled "cycle"
- …/taxonomy/domain-sales/sales-cycle-length: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/average-opportunity-size: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/worksite-employees-sold: 3 vocabulary terms and none named like the concept; choose its primary term

### vocabulary/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×12, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `dct:conformsTo` ×1, `skos:editorialNote` ×1, `skos:changeNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales vocabulary" (add an entry under "assets" in the config to change it)

**Labels put in sentence case** (11): "quota" → "Quota"; "booking" → "Booking"; "prospecting" → "Prospecting"; "outreach" → "Outreach"; "cadence" → "Cadence" … and 6 more
