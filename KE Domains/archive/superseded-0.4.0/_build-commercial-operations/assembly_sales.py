"""Sales assembly: the components the Sales domain is assembled from (design decisions D17–D24).

Service assembly (manifest Sales assembly <VERSION>): Service › Process › Process step, each tier in its own named graph
  party graph     who takes part in selling: the sales organization, the sales advisor agent, and the roles of the
                  people inside and outside the organization (sales representative, prospect, broker)
  step graphs     one per reusable selling step, with its SIPOCM: suppliers outside the process (has supplier), inputs
                  (core:consumes), the step and who performs it, outputs (core:produces), customers outside the process
                  (has customer) and measures (core:measuredBy)
  process graphs  one per sales process: the process and the steps it is built from (core:hasStep), in order
                  (core:precedes)
  service graphs  one per sales service: the service, the processes that enable it (core:supports) and the step that
                  is its delivery (core:deliveryOf)
  manifest        the release: which component graphs, at which versions, make up the Sales assembly

Value map (manifest Sales value map <VALUE_MAP_VERSION>), a separate assembly (D24): the PEO buyer persona graph of the
Commercial Operations container (personas, jobs, job steps, desired outcomes) and the value-map graph, which bridges
selling steps to the job steps they address (core:addresses) and records what each service delivers today (delivered
outcomes with their measured baselines). The service assembly never refers to the persona graph.

References: 'step:x', 'record:x', 'service:x', 'process:x', 'party:x', 'role:x', 'agent:x', 'measure:x' are Sales
resources; 'js:CA-J1.3' is a job step of the persona graph; classes and concepts use the build prefixes.
Inside a process, the supplier of an input and the customer of an output are derived from the data flow: whoever
performs the step that produces the input, or that consumes the output (D24). 'suppliers' and 'customers' name only
the parties or roles outside the assembled processes.
"""

VERSION = '0.3.0'             # the Sales assembly release this manifest describes
VALUE_MAP_VERSION = '0.1.0'   # the Sales value map release
SUPERSEDED = ['process-graph/standard-selling-process', 'step-graph/census-collection']   # graphs the 0.3.0 release removes

PARTY_GRAPH = dict(
    id='sales-parties', label='Sales parties', version='0.1.0',
    definition='The parties, agents and roles that take part in the sales processes: who performs the selling steps, and the roles of those outside the organization who supply their inputs and receive their outputs.',
    resources=[
        ('party:sales-organization', 'core:organization', ['partytax:commercial'], 'Sales organization',
         'The part of the organization that sells its offerings and performs the manual work of selling steps.', {}),
        ('role:sales-representative', 'core:role', ['salestax:sales-representative'], 'Sales representative role',
         'The role borne by a person who pursues opportunities and carries a quota.', {}),
        ('agent:sales-advisor', 'core:information-asset', ['assettax:software-asset'], 'Sales advisor agent',
         'A digital agent that performs the automated work of selling steps and advises sales representatives (PEO Sales Advisor).',
         {'alt': ['PEO Sales Advisor']}),
        ('role:prospect', 'core:role', ['roletax:prospect'], 'Prospect role',
         'The role borne by an organization that is evaluating the organization\'s offerings: it supplies the census and the documents of its current costs and plans, and receives the comparisons.', {}),
        ('role:broker', 'core:role', ['roletax:broker'], 'Broker role',
         'The role borne by a party that places the prospect\'s benefit plans today and may supply their documents on the prospect\'s behalf.', {}),
    ])

# selling steps (all in the Evaluate stage for these services). mode: who performs it (Manual: the sales organization;
# Automated: the sales advisor agent; Hybrid: both). consumes: record refs, or (ref, class, concept, label, definition)
# for an input from outside the assembly, defined in this step graph. measures: (id, label, definition, unit,
# direction, dimension concept).
STEPS = [
    dict(id='census-request', label='Census request', version='0.1.0',
         definition='The standard selling step that asks the prospect for its employee census and sends the template of the minimum fields that quoting and comparison need.',
         stage='salestax:evaluate', kind='salestax:census-request', mode='Manual',
         consumes=[],
         produces=[('record:census-template', 'core:information-asset', 'salestax:census-template', 'Census template',
                    'The list of the minimum census fields the prospect is asked to send, with their formats.')],
         suppliers=[], customers=['role:prospect'],
         measures=[('census-turnaround-time', 'Census turnaround time', 'The days from the census request to a census that passes validation.', 'days', 'minimize', 'measuretax:speed')]),
    dict(id='census-validation', label='Census validation', version='0.1.0',
         definition='The standard selling step that checks the census the prospect sent against the minimum field set, returns the failures to be corrected, and releases the validated census to cost analysis, benefits comparison and quoting.',
         stage='salestax:evaluate', kind='salestax:census-validation', mode='Automated',
         consumes=['record:census'],
         produces=[('record:census', 'commercialops:census', 'commercialopstax:census', 'Census',
                    'The prospect\'s employee census, limited to the minimum set of fields that quoting and comparison need; validated by this step.'),
                   ('record:census-validation-report', 'core:information-asset', 'salestax:census-validation-report', 'Census validation report',
                    'The fields and rows of a census that failed validation, with what must be corrected.')],
         suppliers=['role:prospect'], customers=['role:prospect'],
         measures=[('census-validation-failure-rate', 'Census validation failure rate', 'The share of censuses received that fail validation.', '% of censuses', 'minimize', 'measuretax:validity')]),
    dict(id='current-cost-collection', label='Current cost collection', version='0.2.0',
         definition='The standard selling step that assembles what the prospect spends today to employ its workforce, pre-filled from the census.',
         stage='salestax:evaluate', kind='salestax:current-cost-collection', mode='Hybrid',
         consumes=['record:census',
                   ('record:current-cost-documents', 'core:information-asset', 'assettax:document', 'Current cost documents',
                    'The payroll registers, benefit invoices, insurance policies and broker statements in which the prospect\'s costs today are recorded.')],
         produces=[('record:current-cost-report', 'core:information-asset', 'salestax:current-cost-report', 'Current cost report',
                    'What the prospect spends today on payroll fees, benefits, workers\' compensation, unemployment insurance and broker fees, with the source of each line.')],
         suppliers=['role:prospect'], customers=[],
         measures=[('current-cost-report-completeness', 'Current cost report completeness', 'The share of the lines of the current cost report that cite their source.', '% of lines', 'maximize', 'measuretax:completeness')]),
    dict(id='workforce-cost-forecasting', label='Workforce cost forecasting', version='0.2.0',
         definition='The standard selling step that reruns the cost model at other headcounts and flags regulatory thresholds the prospect would cross.',
         stage='salestax:evaluate', kind='salestax:workforce-cost-forecasting', mode='Automated',
         consumes=['record:census', 'record:current-cost-report'],
         produces=[('record:workforce-cost-forecast', 'core:information-asset', 'salestax:workforce-cost-forecast', 'Workforce cost forecast',
                    'The projected cost of employment at each headcount scenario, today and under the offering, with the thresholds crossed.')],
         suppliers=[], customers=[],
         measures=[('forecast-turnaround-time', 'Forecast turnaround time', 'The minutes from a complete current cost report to the workforce cost forecast.', 'minutes', 'minimize', 'measuretax:speed')]),
    dict(id='employment-cost-comparison', label='Employment cost comparison', version='0.2.0',
         definition='The standard selling step that sets the prospect\'s all-in cost per employee today beside its cost under the organization\'s offering and hands the comparison to the buyer.',
         stage='salestax:evaluate', kind='salestax:employment-cost-comparison', mode='Hybrid',
         consumes=['record:current-cost-report', 'record:workforce-cost-forecast'],
         produces=[('record:cost-comparison', 'core:information-asset', 'salestax:cost-comparison', 'Cost comparison',
                    'The prospect\'s cost of employment today beside its cost under the offering, every line citing its source and assumptions.')],
         suppliers=[], customers=['role:prospect'],
         measures=[('time-to-cost-comparison', 'Time to cost comparison', 'The days from a validated census to the cost comparison handed to the prospect.', 'days', 'minimize', 'measuretax:speed')]),
    dict(id='current-benefits-collection', label='Current benefits collection', version='0.1.0',
         definition='The standard selling step that collects the plan documents, rates and contributions of the benefit plans the prospect\'s employees have today.',
         stage='salestax:evaluate', kind='salestax:current-benefits-collection', mode='Hybrid',
         consumes=['record:census',
                   ('record:current-plan-documents', 'core:information-asset', 'assettax:document', 'Current plan documents',
                    'The summaries of benefits and coverage, rate sheets and contribution schedules of the prospect\'s current benefit plans.')],
         produces=[('record:current-benefits-report', 'core:information-asset', 'salestax:current-benefits-report', 'Current benefits report',
                    'The benefit plans the prospect\'s employees have today, with their rates, contributions and networks.')],
         suppliers=['role:prospect', 'role:broker'], customers=[],
         measures=[('plan-document-completeness', 'Plan document completeness', 'The share of the prospect\'s current plans for which every document needed for comparison was received.', '% of plans', 'maximize', 'measuretax:completeness')]),
    dict(id='benefits-plan-comparison', label='Benefits plan comparison', version='0.2.0',
         definition='The standard selling step that sets the benefit plans the prospect\'s employees have today beside those they would see, with the per-paycheck change for each employee.',
         stage='salestax:evaluate', kind='salestax:benefits-plan-comparison', mode='Hybrid',
         consumes=['record:census', 'record:current-benefits-report'],
         produces=[('record:benefits-comparison-report', 'core:information-asset', 'salestax:benefits-comparison-report', 'Benefits comparison report',
                    'The prospect\'s current benefit plans beside the plans its employees would see, with the per-paycheck cost change and network disruption.')],
         suppliers=[], customers=['role:prospect'],
         measures=[('plan-comparison-time', 'Plan comparison time', 'The minutes to set the prospect\'s current plans beside the plans its employees would see.', 'minutes', 'minimize', 'measuretax:speed')]),
]

# sales processes: (id, label, definition, kind concept, steps in order, version)
PROCESSES = [
    ('census-collection', 'Census collection',
     'The sales process that requests the prospect\'s employee census and validates it against the minimum field set, for cost analysis, benefits comparison and quoting.',
     'salestax:census-collection', ['step:census-request', 'step:census-validation'], '0.1.0'),
    ('employment-cost-analysis', 'Employment cost analysis',
     'The sales process that establishes what the prospect spends today to employ its workforce, projects it as headcount grows, and compares it with the cost under the organization\'s offering.',
     'salestax:employment-cost-analysis', ['step:current-cost-collection', 'step:workforce-cost-forecasting', 'step:employment-cost-comparison'], '0.1.0'),
    ('benefits-plan-analysis', 'Benefits plan analysis',
     'The sales process that collects the benefit plans the prospect\'s employees have today and compares them with the plans they would see.',
     'salestax:benefits-plan-analysis', ['step:current-benefits-collection', 'step:benefits-plan-comparison'], '0.1.0'),
]

# sales services: (id, label, definition, kind concept, delivery step, enabling processes, version)
SERVICES = [
    ('total-cost-of-employment-analysis', 'Total cost of employment analysis',
     'The sales service that shows the prospect what it costs to employ its workforce today, as it grows, and under the organization\'s offering.',
     'salestax:total-cost-of-employment-analysis', 'step:employment-cost-comparison',
     ['process:census-collection', 'process:employment-cost-analysis'], '0.2.0'),
    ('benefits-comparison', 'Benefits comparison',
     'The sales service that shows the prospect\'s employees\' benefit plans today beside the plans they would see.',
     'salestax:benefits-comparison', 'step:benefits-plan-comparison',
     ['process:census-collection', 'process:benefits-plan-analysis'], '0.2.0'),
]

# value map: the job steps of the buyer personas each selling step addresses (core:addresses)
ADDRESSES = {
    'step:census-request': ['js:CA-J3.4'],
    'step:census-validation': ['js:CA-J2.3'],
    'step:current-cost-collection': ['js:CA-J2.1'],
    'step:workforce-cost-forecasting': ['js:CA-J2.2'],
    'step:employment-cost-comparison': ['js:CA-J1.3'],
    'step:benefits-plan-comparison': ['js:HR-J1.3'],
}
