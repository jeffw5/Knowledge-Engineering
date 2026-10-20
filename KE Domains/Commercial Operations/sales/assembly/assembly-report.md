# Sales assembly report

Built 2026-10-20T17:07:55Z by `_build/build_assembly.py`.

- **Sales assembly 0.3.0** (`https://www.insperity.com/resource/domain-sales/manifest/0.3.0`): Service › Process › Process step (D24).
- **Sales value map 0.1.0** (`https://www.insperity.com/resource/domain-sales/manifest/value-map-0.1.0`): a separate assembly that bridges the Sales assembly to the PEO buyer personas.

## Components

| Graph | Kind | Release | Version | Resources | Triples |
|---|---|---|---|---:|---:|
| `persona-graph-domain-commercial-operations-peo-buyer-personas-0.1.0` | persona graph | Sales value map | 0.1.0 | 289 | 3552 |
| `party-graph-domain-sales-sales-parties-0.1.0` | party graph | Sales assembly | 0.1.0 | 5 | 72 |
| `step-graph-domain-sales-census-request-0.1.0` | step graph | Sales assembly | 0.1.0 | 3 | 60 |
| `step-graph-domain-sales-census-validation-0.1.0` | step graph | Sales assembly | 0.1.0 | 4 | 73 |
| `step-graph-domain-sales-current-cost-collection-0.2.0` | step graph | Sales assembly | 0.2.0 | 4 | 74 |
| `step-graph-domain-sales-workforce-cost-forecasting-0.2.0` | step graph | Sales assembly | 0.2.0 | 3 | 61 |
| `step-graph-domain-sales-employment-cost-comparison-0.2.0` | step graph | Sales assembly | 0.2.0 | 3 | 63 |
| `step-graph-domain-sales-current-benefits-collection-0.1.0` | step graph | Sales assembly | 0.1.0 | 4 | 75 |
| `step-graph-domain-sales-benefits-plan-comparison-0.2.0` | step graph | Sales assembly | 0.2.0 | 3 | 63 |
| `process-graph-domain-sales-census-collection-0.1.0` | process graph | Sales assembly | 0.1.0 | 2 | 36 |
| `process-graph-domain-sales-employment-cost-analysis-0.1.0` | process graph | Sales assembly | 0.1.0 | 3 | 38 |
| `process-graph-domain-sales-benefits-plan-analysis-0.1.0` | process graph | Sales assembly | 0.1.0 | 2 | 36 |
| `service-graph-domain-sales-total-cost-of-employment-analysis-0.2.0` | service graph | Sales assembly | 0.2.0 | 4 | 35 |
| `service-graph-domain-sales-benefits-comparison-0.2.0` | service graph | Sales assembly | 0.2.0 | 4 | 35 |
| `manifest-domain-sales-0.3.0` | manifest | Sales assembly | 0.3.0 | 1 | 51 |
| `value-map-domain-sales-sales-buyer-value-0.1.0` | value map | Sales value map | 0.1.0 | 14 | 127 |
| `manifest-domain-sales-value-map-0.1.0` | manifest | Sales value map | 0.1.0 | 1 | 42 |

Superseded and moved to `archive/superseded-assembly-0.3.0/`: `manifest-domain-sales-0.2.0.ttl`, `process-graph-domain-sales-standard-selling-process-0.1.0.ttl`, `service-graph-domain-sales-benefits-comparison-0.1.0.ttl`, `service-graph-domain-sales-total-cost-of-employment-analysis-0.1.0.ttl`, `step-graph-domain-sales-benefits-plan-comparison-0.1.0.ttl`, `step-graph-domain-sales-census-collection-0.1.0.ttl`, `step-graph-domain-sales-current-cost-collection-0.1.0.ttl`, `step-graph-domain-sales-employment-cost-comparison-0.1.0.ttl`, `step-graph-domain-sales-workforce-cost-forecasting-0.1.0.ttl`, `manifest-domain-sales-0.2.0.trig`, `process-graph-domain-sales-standard-selling-process-0.1.0.trig`, `service-graph-domain-sales-benefits-comparison-0.1.0.trig`, `service-graph-domain-sales-total-cost-of-employment-analysis-0.1.0.trig`, `step-graph-domain-sales-benefits-plan-comparison-0.1.0.trig`, `step-graph-domain-sales-census-collection-0.1.0.trig`, `step-graph-domain-sales-current-cost-collection-0.1.0.trig`, `step-graph-domain-sales-employment-cost-comparison-0.1.0.trig`, `step-graph-domain-sales-workforce-cost-forecasting-0.1.0.trig`.

## How each service is assembled

### Total cost of employment analysis

Enabled by census collection and employment cost analysis; delivered by employment cost comparison.

| Process | Step | Suppliers | Inputs | Performed by | Outputs | Customers | Measures |
|---|---|---|---|---|---|---|---|
| Census collection | Census request | — | — | Sales organization | Census template | Prospect role (outside) | Census turnaround time |
| Census collection | Census validation | Prospect role (outside) | Census | Sales advisor agent | Census; Census validation report | Prospect role (outside); Current cost collection; Workforce cost forecasting; Current benefits collection; Benefits plan comparison | Census validation failure rate |
| Employment cost analysis | Current cost collection | Prospect role (outside); Census validation | Census; Current cost documents | Sales organization, Sales advisor agent | Current cost report | Workforce cost forecasting; Employment cost comparison | Current cost report completeness |
| Employment cost analysis | Workforce cost forecasting | Census validation; Current cost collection | Census; Current cost report | Sales advisor agent | Workforce cost forecast | Employment cost comparison | Forecast turnaround time |
| Employment cost analysis | Employment cost comparison (delivery) | Current cost collection; Workforce cost forecasting | Current cost report; Workforce cost forecast | Sales organization, Sales advisor agent | Cost comparison | Prospect role (outside) | Time to cost comparison |

### Benefits comparison

Enabled by census collection and benefits plan analysis; delivered by benefits plan comparison.

| Process | Step | Suppliers | Inputs | Performed by | Outputs | Customers | Measures |
|---|---|---|---|---|---|---|---|
| Census collection | Census request | — | — | Sales organization | Census template | Prospect role (outside) | Census turnaround time |
| Census collection | Census validation | Prospect role (outside) | Census | Sales advisor agent | Census; Census validation report | Prospect role (outside); Current cost collection; Workforce cost forecasting; Current benefits collection; Benefits plan comparison | Census validation failure rate |
| Benefits plan analysis | Current benefits collection | Prospect role (outside); Broker role (outside); Census validation | Census; Current plan documents | Sales organization, Sales advisor agent | Current benefits report | Benefits plan comparison | Plan document completeness |
| Benefits plan analysis | Benefits plan comparison (delivery) | Census validation; Current benefits collection | Census; Current benefits report | Sales organization, Sales advisor agent | Benefits comparison report | Prospect role (outside) | Plan comparison time |

Suppliers and customers marked *(outside)* are stated with has supplier and has customer; the others are derived from the data flow: the step that produces an input, or that consumes an output (D24).

## Checks

- Errors: **0** · warnings: **42**.
- For each manifest: every instance is typed by a core or domain class and classified by an existing taxonomy concept; every graph refers only to the core, the Commercial Operations container and its own domain; every resource referred to is defined by a component in that manifest. The Sales assembly does not refer to the persona graph or the value map.
- SHACL: 35 node shapes (core, Commercial Operations, Sales and the other domains) run over the Sales assembly, and again over the assembly with the value map, after the ontologies' owl:inverseOf pairs are applied.

**Sales assembly:** 36 findings.

| Severity | Shape | Finding | Focus nodes |
|---|---|---|---|
| warn | `process-shape` (core) | A process should have at least one process step. | 7: step/census-request, step/census-validation, step/current-cost-collection, step/workforce-cost-forecasting, step/employment-cost-comparison, step/current-benefits-collection … |
| warn | `asset-shape` (core) | An asset should have a lifecycle. | 28: sales-parties/, agent/sales-advisor, census-request/, record/census-template, census-validation/, record/census … |
| warn | `census-shape` (domain-commercial-operations) | A census must be about the employees it lists. | 1: record/census |

**Added by the value map:** 6 findings.

| Severity | Shape | Finding | Focus nodes |
|---|---|---|---|
| warn | `asset-shape` (core) | An asset should have a lifecycle. | 6: peo-buyer-personas/, job-study/js-ca, job-study/js-hr, sales-buyer-value/, value-map-0.1.0/, manifest/value-map-0.1.0 |

## Assembly measures

A node's **joins** are the parts it is joined from, less one (n parts take n − 1 joins). Primitives are atoms (0 joins); a taxonomy concept is joined from its primitives; a step from its concepts and its SIPOCM (suppliers, inputs, performers and role, outputs, customers, measures); a process from its concepts and its steps; a service from its concept, the processes that enable it and its delivery step. The value map is not counted.

**Assembly index (modeled pathway)** is the number of joins in the service's closure, each shared part counted once. It is the length of the pathway the model records, so it is an upper bound on the true assembly index (the shortest possible pathway). **Without reuse** counts every part again wherever it is used. **Copy number** is how many services contain a part.

| Service | Nodes in closure | Primitives | Assembly index (modeled) | Without reuse | Saved by reuse |
|---|---:|---:|---:|---:|---:|
| Total cost of employment analysis | 76 | 27 | 77 | 110 | 33 |
| Benefits comparison | 72 | 26 | 65 | 91 | 26 |

Assembled together, the two services take **115** joins, against **142** built separately: **27** joins (19%) are saved because the services share parts.

**Shared parts** (copy number > 1): 52 — 23 primitives, 17 concepts, 3 records, 2 steps, 2 measures, 2 roles, 1 process, 1 agent, 1 party. The shared processes, steps and records are the platform candidates (Baseline decision 14):

| Part | Kind | Copy number | Joins in its closure |
|---|---|---:|---:|
| Census collection | process | 2 | 27 |
| Census validation | step | 2 | 13 |
| Census request | step | 2 | 10 |
| Census validation report | record | 2 | 2 |
| Sales advisor agent | agent | 2 | 1 |
| Census turnaround time | measure | 2 | 1 |
| Census validation failure rate | measure | 2 | 1 |
| Census template | record | 2 | 1 |
| Sales representative role | role | 2 | 1 |
| Sales organization | party | 2 | 0 |
| Census | record | 2 | 0 |
| Prospect role | role | 2 | 0 |

All parts, with copy number and joins: `assembly-measures.csv`.

## Value map (Sales value map 0.1.0)

A separate assembly (D24). For each job step a service's steps address (core:addresses, in the value-map graph), each desired outcome (persona graph) is compared with what the service delivers today (delivered outcome, value-map graph). Same job step, same metric card. These results will be shown on the Value Mapping page.

| Service | Job step | Desired outcome | Target | Baseline | Status |
|---|---|---|---:|---:|---|
| Total cost of employment analysis | CA-J3.4 Protect employee data shared during the sale | Minimize the number of people outside the deal team who can see our census (unauthorized viewers) | 0 |  | Not yet measured |
| Total cost of employment analysis | CA-J3.4 Protect employee data shared during the sale | Minimize the time it takes to confirm where our data is stored and who can access it (minutes) | 5 |  | Not yet measured |
| Total cost of employment analysis | CA-J3.4 Protect employee data shared during the sale | Maximize the share of shared documents carrying an access label (% labelled) | 100 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.3 Provide clean census data for quoting | Minimize the share of census uploads that fail validation (% failed uploads) | 10 | 38 | Value gap |
| Total cost of employment analysis | CA-J2.3 Provide clean census data for quoting | Minimize the time it takes to fix a rejected census (hours) | 1 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.3 Provide clean census data for quoting | Minimize the amount of employee personal data shared beyond what quoting needs (fields beyond minimum set) | 0 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.1 Establish our current all-in cost per employee | Minimize the time it takes to assemble our current all-in cost (payroll fees, benefits, workers’ comp, SUTA, broker fees) (hours) | 2 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.1 Establish our current all-in cost per employee | Minimize the likelihood of leaving a cost category out of the baseline (omitted categories per baseline) | 0 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.1 Establish our current all-in cost per employee | Minimize the variance between our baseline and what we actually paid last year (% variance to GL) | 3 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.2 Project cost as headcount grows | Minimize the time it takes to see cost at a different headcount (minutes) | 5 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.2 Project cost as headcount grows | Minimize the likelihood of crossing a regulatory threshold (such as ACA 50 FTE) without warning (unflagged threshold crossings) | 0 |  | Not yet measured |
| Total cost of employment analysis | CA-J2.2 Project cost as headcount grows | Maximize the accuracy of projected first-year cost (% variance to actual) | 5 |  | Not yet measured |
| Total cost of employment analysis | CA-J1.3 Compare total cost against our current stack | Minimize the time from first cost question to a binding quote (days) | 10 | 16 | Value gap |
| Total cost of employment analysis | CA-J1.3 Compare total cost against our current stack | Minimize the likelihood that the signed price differs from the quoted price (re-quotes per deal) | 0 |  | Not yet measured |
| Total cost of employment analysis | CA-J1.3 Compare total cost against our current stack | Maximize the share of cost lines that show their source and assumptions (% of cost lines cited) | 100 |  | Not yet measured |
| Benefits comparison | CA-J3.4 Protect employee data shared during the sale | Minimize the number of people outside the deal team who can see our census (unauthorized viewers) | 0 |  | Not yet measured |
| Benefits comparison | CA-J3.4 Protect employee data shared during the sale | Minimize the time it takes to confirm where our data is stored and who can access it (minutes) | 5 |  | Not yet measured |
| Benefits comparison | CA-J3.4 Protect employee data shared during the sale | Maximize the share of shared documents carrying an access label (% labelled) | 100 |  | Not yet measured |
| Benefits comparison | CA-J2.3 Provide clean census data for quoting | Minimize the share of census uploads that fail validation (% failed uploads) | 10 | 38 | Value gap |
| Benefits comparison | CA-J2.3 Provide clean census data for quoting | Minimize the time it takes to fix a rejected census (hours) | 1 |  | Not yet measured |
| Benefits comparison | CA-J2.3 Provide clean census data for quoting | Minimize the amount of employee personal data shared beyond what quoting needs (fields beyond minimum set) | 0 |  | Not yet measured |
| Benefits comparison | HR-J1.3 Compare benefit plans employees will see | Minimize the time it takes to compare current plans with PEO plans (minutes) | 20 | 34 | Value gap |
| Benefits comparison | HR-J1.3 Compare benefit plans employees will see | Maximize the share of employees whose per-paycheck cost change is shown (% of employees) | 100 |  | Not yet measured |
| Benefits comparison | HR-J1.3 Compare benefit plans employees will see | Minimize the share of employees whose current doctors fall out of network (% of employees) | 5 |  | Not yet measured |

4 value gaps, 0 met, 20 not yet measured. All rows: `value-gaps.csv`.
