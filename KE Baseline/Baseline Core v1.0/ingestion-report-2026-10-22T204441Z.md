# Ingestion report

Run 2026-10-22T20:44:41Z · base URL `https://www.insperity.com/` · author Jeffrey Wallk · version 0.1.0 (Draft)

Standards: Semantic Governance: Services, Architecture & Integration v1.9 (Draft), Part III

## Outputs

| Asset | IRI | Terms | Triples | Turtle | TriG | From |
|---|---|---|---|---|---|---|
| Domain sales ontology | `https://www.insperity.com/ontology/domain-sales/` | 4 | 92 | `ontology-domain-sales-0.1.0.ttl` | `ontology-domain-sales-0.1.0.trig` | ontology-domain-sales-0.4.0.ttl |
| Domain sales shapes | `https://www.insperity.com/shapes/domain-sales/` | 3 | 84 | `shapes-domain-sales-0.1.0.ttl` | `shapes-domain-sales-0.1.0.trig` | shapes-domain-sales-0.4.0.ttl |
| Domain sales taxonomy | `https://www.insperity.com/taxonomy/domain-sales/` | 59 | 922 | `taxonomy-domain-sales-0.1.0.ttl` | `taxonomy-domain-sales-0.1.0.trig` | taxonomy-domain-sales-0.4.0.ttl |
| Domain sales vocabulary | `https://www.insperity.com/vocabulary/domain-sales/` | 13 | 181 | `vocabulary-domain-sales-0.1.0.ttl` | `vocabulary-domain-sales-0.1.0.trig` | vocabulary-domain-sales-0.4.0.ttl |

Change record: `ttl/change-record-2026-10-22T204441Z.ttl` and `trig/change-record-2026-10-22T204441Z.trig`. Crosswalk of every legacy IRI: `crosswalk.csv`.

## Conformance after ingestion

**ontology-domain-sales-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

**shapes-domain-sales-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

**taxonomy-domain-sales-0.1.0.ttl** — 38 errors, 11 warnings, 0 info
- Taxonomy term in a vocabulary (§3.11): `…/taxonomy/domain-sales/buying-committee` linked to …/vocabulary/commercial-operations/buying-committee, …/vocabulary/core-governance/buying-committee, which is in no vocabulary; `…/taxonomy/domain-sales/buying-role` linked to …/vocabulary/commercial-operations/buying-role, …/vocabulary/core-role/buying-role, which is in no vocabulary; `…/taxonomy/domain-sales/economic-buyer` linked to …/vocabulary/commercial-operations/economic-buyer, …/vocabulary/core-value/economic-buyer, which is in no vocabulary; `…/taxonomy/domain-sales/influencer` linked to …/vocabulary/commercial-operations/influencer, …/vocabulary/commercial-operations/influencer, which is in no vocabulary; `…/taxonomy/domain-sales/sales-measure` linked to …/vocabulary/core-domain/sales-measure, …/vocabulary/core-measure/sales-measure, which is in no vocabulary; `…/taxonomy/domain-sales/average-opportunity-size` linked to …/vocabulary/commercial-operations/average-opportunity-size, …/vocabulary/core-measure/average-opportunity-size, which is in no vocabulary (+43 more)

**vocabulary-domain-sales-0.1.0.ttl** — 0 errors, 0 warnings, 0 info

## What changed, by asset

On every asset and term the governance fields were rebuilt, not copied: `dct:creator` and (on asset headers) `dct:contributor` are Jeffrey Wallk only; `dct:created` keeps the source date (or the run time when the source had none); `dct:modified` is 2026-10-22T20:44:41Z; `owl:versionInfo` is 0.1.0; lifecycle status is Draft. Labels and definitions were re-tagged `@en`. The source values of those fields are not counted below.

### ontology/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×5, `skos:changeNote` ×4, `dct:conformsTo` ×2, `dct:requires` ×2, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `skos:editorialNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales ontology" (add an entry under "assets" in the config to change it)

**Unresolved links**
- …/ontology/domain-sales/selling-process: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-process
- …/ontology/domain-sales/selling-process: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-process
- …/ontology/domain-sales/selling-step: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-step
- …/ontology/domain-sales/selling-step: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/selling-step
- …/ontology/domain-sales/sales-service: vocabulary core-services was not in this run; dc:subject set to the expected IRI …/vocabulary/core-services/sales-service
- …/ontology/domain-sales/sales-service: vocabulary core-services was not in this run; dc:subject set to the expected IRI …/vocabulary/core-services/sales-service

### shapes/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×4, `skos:changeNote` ×4, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `dct:conformsTo` ×1, `skos:editorialNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1, `dct:requires` ×1

**Written during ingestion**
- Title written: "Domain sales shapes" (add an entry under "assets" in the config to change it)

**Filled from existing metadata**
- owl:imports …/ontology/core/ added (referenced by the model)

**Moved**
- …/shapes/domain-sales/selling-step-shape → …/shapes/domain-sales/selling-step-shape
- …/shapes/domain-sales/sales-service-shape → …/shapes/domain-sales/sales-service-shape
- …/shapes/domain-sales/quota-shape → …/shapes/domain-sales/quota-shape

### taxonomy/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×60, `dct:source` ×18, `skos:changeNote` ×4, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `dct:conformsTo` ×1, `skos:editorialNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales taxonomy" (add an entry under "assets" in the config to change it)

**Unresolved links**
- …/taxonomy/domain-sales/selling-stage: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/selling-stage
- …/taxonomy/domain-sales/selling-stage: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/selling-stage
- …/taxonomy/domain-sales/selling-stage: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/selling-stage
- …/taxonomy/domain-sales/qualify: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/qualify
- …/taxonomy/domain-sales/qualify: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/qualify
- …/taxonomy/domain-sales/evaluate: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/evaluate
- …/taxonomy/domain-sales/evaluate: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/evaluate
- …/taxonomy/domain-sales/propose: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/propose
- …/taxonomy/domain-sales/propose: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/propose
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
- …/taxonomy/domain-sales/census-request: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/census-request
- …/taxonomy/domain-sales/census-request: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/census-request
- …/taxonomy/domain-sales/census-request: vocabulary core-issue was not in this run; dc:subject set to the expected IRI …/vocabulary/core-issue/census-request
- …/taxonomy/domain-sales/census-validation: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/census-validation
- …/taxonomy/domain-sales/census-validation: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/census-validation
- …/taxonomy/domain-sales/census-validation: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/census-validation
- …/taxonomy/domain-sales/current-benefits-collection: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/current-benefits-collection
- …/taxonomy/domain-sales/current-benefits-collection: vocabulary core-time was not in this run; dc:subject set to the expected IRI …/vocabulary/core-time/current-benefits-collection
- …/taxonomy/domain-sales/current-cost-collection: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/current-cost-collection
- …/taxonomy/domain-sales/current-cost-collection: vocabulary core-time was not in this run; dc:subject set to the expected IRI …/vocabulary/core-time/current-cost-collection
- …/taxonomy/domain-sales/workforce-cost-forecasting: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/workforce-cost-forecasting
- …/taxonomy/domain-sales/workforce-cost-forecasting: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/workforce-cost-forecasting
- …/taxonomy/domain-sales/workforce-cost-forecasting: vocabulary core-party was not in this run; dc:subject set to the expected IRI …/vocabulary/core-party/workforce-cost-forecasting
- …/taxonomy/domain-sales/workforce-cost-forecasting: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/workforce-cost-forecasting
- …/taxonomy/domain-sales/employment-cost-comparison: vocabulary core-party was not in this run; dc:subject set to the expected IRI …/vocabulary/core-party/employment-cost-comparison
- …/taxonomy/domain-sales/employment-cost-comparison: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/employment-cost-comparison
- …/taxonomy/domain-sales/benefits-plan-comparison: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/benefits-plan-comparison
- …/taxonomy/domain-sales/benefits-plan-comparison: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/benefits-plan-comparison
- …/taxonomy/domain-sales/sales-process: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/sales-process
- …/taxonomy/domain-sales/sales-process: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-process
- …/taxonomy/domain-sales/sales-process: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/sales-process
- …/taxonomy/domain-sales/census-collection: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/census-collection
- …/taxonomy/domain-sales/employment-cost-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/employment-cost-analysis
- …/taxonomy/domain-sales/employment-cost-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/employment-cost-analysis
- …/taxonomy/domain-sales/employment-cost-analysis: vocabulary core-party was not in this run; dc:subject set to the expected IRI …/vocabulary/core-party/employment-cost-analysis
- …/taxonomy/domain-sales/employment-cost-analysis: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/employment-cost-analysis
- …/taxonomy/domain-sales/benefits-plan-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/benefits-plan-analysis
- …/taxonomy/domain-sales/benefits-plan-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/benefits-plan-analysis
- …/taxonomy/domain-sales/benefits-plan-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/benefits-plan-analysis
- …/taxonomy/domain-sales/benefits-plan-analysis: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/benefits-plan-analysis
- …/taxonomy/domain-sales/sales-service: vocabulary core-services was not in this run; dc:subject set to the expected IRI …/vocabulary/core-services/sales-service
- …/taxonomy/domain-sales/sales-service: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-service
- …/taxonomy/domain-sales/sales-service: vocabulary core-services was not in this run; dc:subject set to the expected IRI …/vocabulary/core-services/sales-service
- …/taxonomy/domain-sales/total-cost-of-employment-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/total-cost-of-employment-analysis
- …/taxonomy/domain-sales/total-cost-of-employment-analysis: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/total-cost-of-employment-analysis
- …/taxonomy/domain-sales/total-cost-of-employment-analysis: vocabulary core-party was not in this run; dc:subject set to the expected IRI …/vocabulary/core-party/total-cost-of-employment-analysis
- …/taxonomy/domain-sales/total-cost-of-employment-analysis: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/total-cost-of-employment-analysis
- …/taxonomy/domain-sales/benefits-comparison: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/benefits-comparison
- …/taxonomy/domain-sales/buying-role: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/buying-role
- …/taxonomy/domain-sales/buying-role: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/buying-role
- …/taxonomy/domain-sales/buying-role: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/buying-role
- …/taxonomy/domain-sales/economic-buyer: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/economic-buyer
- …/taxonomy/domain-sales/economic-buyer: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/economic-buyer
- …/taxonomy/domain-sales/economic-buyer: vocabulary core-value was not in this run; dc:subject set to the expected IRI …/vocabulary/core-value/economic-buyer
- …/taxonomy/domain-sales/influencer: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/influencer
- …/taxonomy/domain-sales/influencer: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/influencer
- …/taxonomy/domain-sales/buying-committee: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/buying-committee
- …/taxonomy/domain-sales/buying-committee: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/buying-committee
- …/taxonomy/domain-sales/buying-committee: vocabulary core-governance was not in this run; dc:subject set to the expected IRI …/vocabulary/core-governance/buying-committee
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
- …/taxonomy/domain-sales/account-plan: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/account-plan
- …/taxonomy/domain-sales/account-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/account-plan
- …/taxonomy/domain-sales/territory-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/territory-plan
- …/taxonomy/domain-sales/territory-plan: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/territory-plan
- …/taxonomy/domain-sales/territory-plan: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/territory-plan
- …/taxonomy/domain-sales/sales-incentive: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/sales-incentive
- …/taxonomy/domain-sales/sales-incentive: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/sales-incentive
- …/taxonomy/domain-sales/sales-incentive: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-incentive
- …/taxonomy/domain-sales/sales-record: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/sales-record
- …/taxonomy/domain-sales/sales-record: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/sales-record
- …/taxonomy/domain-sales/sales-record: vocabulary core-domain was not in this run; dc:subject set to the expected IRI …/vocabulary/core-domain/sales-record
- …/taxonomy/domain-sales/current-cost-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/current-cost-report
- …/taxonomy/domain-sales/current-cost-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/current-cost-report
- …/taxonomy/domain-sales/current-cost-report: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/current-cost-report
- …/taxonomy/domain-sales/current-cost-report: vocabulary core-time was not in this run; dc:subject set to the expected IRI …/vocabulary/core-time/current-cost-report
- …/taxonomy/domain-sales/workforce-cost-forecast: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/workforce-cost-forecast
- …/taxonomy/domain-sales/workforce-cost-forecast: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/workforce-cost-forecast
- …/taxonomy/domain-sales/workforce-cost-forecast: vocabulary core-party was not in this run; dc:subject set to the expected IRI …/vocabulary/core-party/workforce-cost-forecast
- …/taxonomy/domain-sales/workforce-cost-forecast: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/workforce-cost-forecast
- …/taxonomy/domain-sales/cost-comparison: vocabulary core-product was not in this run; dc:subject set to the expected IRI …/vocabulary/core-product/cost-comparison
- …/taxonomy/domain-sales/census-template: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/census-template
- …/taxonomy/domain-sales/census-template: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/census-template
- …/taxonomy/domain-sales/census-template: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/census-template
- …/taxonomy/domain-sales/census-validation-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/census-validation-report
- …/taxonomy/domain-sales/census-validation-report: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/census-validation-report
- …/taxonomy/domain-sales/census-validation-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/census-validation-report
- …/taxonomy/domain-sales/census-validation-report: vocabulary core-process was not in this run; dc:subject set to the expected IRI …/vocabulary/core-process/census-validation-report
- …/taxonomy/domain-sales/current-benefits-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/current-benefits-report
- …/taxonomy/domain-sales/current-benefits-report: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/current-benefits-report
- …/taxonomy/domain-sales/current-benefits-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/current-benefits-report
- …/taxonomy/domain-sales/current-benefits-report: vocabulary core-time was not in this run; dc:subject set to the expected IRI …/vocabulary/core-time/current-benefits-report
- …/taxonomy/domain-sales/benefits-comparison-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/benefits-comparison-report
- …/taxonomy/domain-sales/benefits-comparison-report: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/benefits-comparison-report
- …/taxonomy/domain-sales/benefits-comparison-report: vocabulary core-asset was not in this run; dc:subject set to the expected IRI …/vocabulary/core-asset/benefits-comparison-report
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
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/average-opportunity-size
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/average-opportunity-size
- …/taxonomy/domain-sales/average-opportunity-size: vocabulary core-measure was not in this run; dc:subject set to the expected IRI …/vocabulary/core-measure/average-opportunity-size
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/worksite-employees-sold
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary commercial-operations was not in this run; dc:subject set to the expected IRI …/vocabulary/commercial-operations/worksite-employees-sold
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary core-location was not in this run; dc:subject set to the expected IRI …/vocabulary/core-location/worksite-employees-sold
- …/taxonomy/domain-sales/worksite-employees-sold: vocabulary core-role was not in this run; dc:subject set to the expected IRI …/vocabulary/core-role/worksite-employees-sold

**Review**
- …/taxonomy/domain-sales/selling-stage: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/selling-activity: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/objection-handling: linked vocabulary term is labelled "objection"
- …/taxonomy/domain-sales/objection-handling: linked vocabulary term is labelled "objection"
- …/taxonomy/domain-sales/objection-handling: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/client-handoff: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/census-request: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/census-validation: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/current-benefits-collection: linked vocabulary term is labelled "collection"
- …/taxonomy/domain-sales/current-benefits-collection: linked vocabulary term is labelled "collection"
- …/taxonomy/domain-sales/current-benefits-collection: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/current-cost-collection: linked vocabulary term is labelled "collection"
- …/taxonomy/domain-sales/current-cost-collection: linked vocabulary term is labelled "collection"
- …/taxonomy/domain-sales/current-cost-collection: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/workforce-cost-forecasting: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/employment-cost-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/employment-cost-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/employment-cost-comparison: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/benefits-plan-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/benefits-plan-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/benefits-plan-comparison: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-process: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/census-collection: linked vocabulary term is labelled "collection"
- …/taxonomy/domain-sales/census-collection: linked vocabulary term is labelled "collection"
- …/taxonomy/domain-sales/census-collection: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/employment-cost-analysis: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/benefits-plan-analysis: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-service: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/total-cost-of-employment-analysis: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/benefits-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/benefits-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/benefits-comparison: 2 vocabulary terms and none named like the concept; choose its primary term
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
- …/taxonomy/domain-sales/current-cost-report: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/workforce-cost-forecast: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/cost-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/cost-comparison: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/cost-comparison: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/census-template: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/census-validation-report: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/current-benefits-report: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/benefits-comparison-report: linked vocabulary term is labelled "comparison"
- …/taxonomy/domain-sales/benefits-comparison-report: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-measure: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/quota-attainment: linked vocabulary term is labelled "quota"
- …/taxonomy/domain-sales/quota-attainment: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-forecast: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/sales-cycle-length: linked vocabulary term is labelled "cycle"
- …/taxonomy/domain-sales/sales-cycle-length: 3 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/average-opportunity-size: 2 vocabulary terms and none named like the concept; choose its primary term
- …/taxonomy/domain-sales/worksite-employees-sold: 3 vocabulary terms and none named like the concept; choose its primary term

### vocabulary/domain-sales

Removed properties: `<https://www.insperity.com/ontology/core/hasLifecycleStatus>` ×14, `skos:changeNote` ×4, `dct:subject` ×1, `<http://www.linkedmodel.org/schema/vaem#namespace>` ×1, `<http://purl.org/vocab/vann/preferredNamespacePrefix>` ×1, `dct:language` ×1, `dct:publisher` ×1, `dct:conformsTo` ×1, `skos:editorialNote` ×1, `owl:versionIRI` ×1, `dct:identifier` ×1, `dct:isPartOf` ×1

**Written during ingestion**
- Title written: "Domain sales vocabulary" (add an entry under "assets" in the config to change it)

**Labels put in sentence case** (13): "quota" → "Quota"; "booking" → "Booking"; "prospecting" → "Prospecting"; "outreach" → "Outreach"; "cadence" → "Cadence" … and 8 more
