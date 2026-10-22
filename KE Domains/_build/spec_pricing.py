"""Pricing and contracts: quoting, underwriting and contracting professional employer organization services."""
from dsl import V, C, K, P, S

DOMAIN = dict(
    key='pricing', level='domain', area='commercial-operations', folder='Commercial Operations/pricing', title='Domain Pricing', prefix='pricing', subject='core-domain/commercial', parent=None, replaces='domain-pricing-and-contracts',
    vocabulary_description='A controlled vocabulary of the primitives of pricing and underwriting professional employer organization services: quotes, prices, fees, discounts, census data, workers\' compensation class codes and experience modification factors, loss runs and employer burden.',
    taxonomy_description='A classification of pricing components and models, quotes, underwriting inputs and outcomes, and pricing review. Contract management, agreement terms and statuses are in Domain Legal.',
    ontology_description='The pricing ontology. It extends the core domain ontology and the Commercial Operations ontology with quotes for opportunities, and underwriting and its decisions, which consume the Commercial Operations census. Agreements and their clauses are in Domain Legal (Business Operations).',
    version='0.3.0', changes=[('0.1.0', '2026-10-20', 'first release.'), ('0.2.0', '2026-10-20', 'Census moved to the Commercial Operations container (D2). Domain ontologies and shapes now name the plain ontology IRIs in owl:imports, so the KE Workbench resolves them, and pin the version built against in dcterms:requires.'), ('0.3.0', '2026-10-21', "Restructured to the operational areas and the naming standard (D26, D27): titled 'Domain Pricing Vocabulary', '… Taxonomy', '… Ontology' and '… Shapes', at …/<kind>/domain-pricing/ (formerly Pricing and contracts, …/<kind>/domain-pricing-and-contracts/). Contract management steps, agreement terms and agreement statuses, with the term and signature primitives, moved to Domain Legal (Business Operations); pricing review stays here.")],
    shapes_description='SHACL shapes for quotes and underwriting decisions.',
)

VOCAB = [
    V('quote', 'quote', 'A statement of the prices at which the organization offers an offering to a prospect or client, valid for a stated period.'),
    V('price', 'price', 'An amount of money asked or paid for an offering or a unit of it.'),
    V('fee', 'fee', 'A charge for a service, set as a fixed amount, an amount per worker or a share of payroll.'),
    V('discount', 'discount', 'A reduction from a standard price.'),
    V('underwriting', 'underwriting', 'The assessment of the risk of covering a client, used to decide whether, and at what price, to offer coverage.'),
    V('class-code', 'class code', 'A code that classifies a worker\'s occupation by its workers\' compensation risk and sets the rate applied to that worker\'s pay.',
      scope='A multiword lexical unit (Baseline decision 3).'),
    V('experience-modification-factor', 'experience modification factor', 'A factor that adjusts an employer\'s workers\' compensation premium up or down from the base rate according to its claims history relative to similar employers.',
      alt=['experience mod', 'EMR'], scope='A multiword lexical unit (Baseline decision 3).'),
    V('loss-run', 'loss run', 'A report from an insurer of an employer\'s history of insurance claims, used in underwriting.',
      scope='A multiword lexical unit (Baseline decision 3).'),
    V('burden', 'burden', 'The total cost an employer bears for a worker beyond wages, including employment taxes, insurance and benefits.'),
    V('percentage', 'percentage', 'A ratio expressed as a number of parts per hundred.',
      promote='General primitive missing from the core (core-measure holds "ratio" and "rate").'),
]

TAXONOMY = [
    # pricing components
    C('pricing-component', 'Pricing component', 'A measure that is one of the amounts or rates from which the price of a professional employer organization offering is built.',
      ['core-decision/pricing', 'core-asset/component'], formalized='core:measure', primary='core-asset/component'),
    C('service-fee', 'Service fee', 'A pricing component charged for the organization\'s services, separate from pass-through costs.',
      ['core-services/services', 'domain-pricing/fee'], broader='pricing-component', alt=['Administrative fee']),
    C('per-worksite-employee-per-month-fee', 'Per worksite employee per month fee', 'A service fee charged as a fixed amount for each worksite employee each month.',
      ['core-location/worksite', 'core-role/employee', 'core-time/month', 'domain-pricing/fee'], broader='service-fee', alt=['PEPM fee']),
    C('percentage-of-payroll-fee', 'Percentage of payroll fee', 'A service fee charged as a percentage of the client\'s gross payroll.',
      ['domain-pricing/percentage', 'commercial-operations/payroll', 'domain-pricing/fee'], broader='service-fee'),
    C('benefits-rate', 'Benefits rate', 'A pricing component that is the amount charged per covered person for a benefit.',
      ['commercial-operations/benefit', 'core-measure/rate'], broader='pricing-component'),
    C('workers-compensation-rate', 'Workers\' compensation rate', 'A pricing component that is the rate charged per unit of pay for workers\' compensation, set by class code and adjusted by the experience modification factor.',
      ['commercial-operations/workers-compensation', 'core-measure/rate'], broader='pricing-component'),
    C('unemployment-insurance-rate', 'Unemployment insurance rate', 'A pricing component that is the state unemployment insurance tax rate applied to taxable wages.',
      ['commercial-operations/unemployment', 'commercial-operations/insurance', 'core-measure/rate'], broader='pricing-component'),
    C('employer-burden', 'Employer burden', 'A pricing component that is the total cost the client would bear for its workers beyond wages.',
      ['core-role/employer', 'domain-pricing/burden'], broader='pricing-component', alt=['Burden rate']),
    C('discount', 'Discount', 'A pricing component that reduces a standard price.',
      ['domain-pricing/discount'], broader='pricing-component'),
    # pricing models
    C('pricing-model', 'Pricing model', 'A directive that sets how the price of an offering is built from its pricing components.',
      ['core-decision/pricing', 'core-asset/model'], formalized='core:directive'),
    C('bundled-pricing', 'Bundled pricing', 'A pricing model that charges one price for a bundle of services, without showing the cost of each.',
      ['core-product/bundle', 'core-decision/pricing'], broader='pricing-model'),
    C('unbundled-pricing', 'Unbundled pricing', 'A pricing model that charges a service fee and passes through the cost of each component separately.',
      ['core-product/bundle', 'core-decision/pricing'], broader='pricing-model', alt=['Itemized pricing'],
      scope='Built from the same primitives as bundled pricing; the difference is in the definition.'),
    C('per-worksite-employee-pricing', 'Per worksite employee pricing', 'A pricing model that charges the service fee per worksite employee per period.',
      ['core-location/worksite', 'core-role/employee', 'core-decision/pricing'], broader='pricing-model'),
    C('percentage-of-payroll-pricing', 'Percentage of payroll pricing', 'A pricing model that charges the service fee as a percentage of payroll.',
      ['domain-pricing/percentage', 'commercial-operations/payroll', 'core-decision/pricing'], broader='pricing-model'),
    # quotes
    C('quote', 'Quote', 'An information asset that states the prices at which the organization offers an offering to a prospect or client, valid for a stated period.',
      ['domain-pricing/quote'], formalized='pricing:quote'),
    C('benefits-quote', 'Benefits quote', 'A quote of the rates for the benefit plans offered to a client\'s worksite employees.',
      ['commercial-operations/benefit', 'domain-pricing/quote'], broader='quote'),
    C('workers-compensation-quote', 'Workers\' compensation quote', 'A quote of the workers\' compensation rates for a client\'s class codes.',
      ['commercial-operations/workers-compensation', 'domain-pricing/quote'], broader='quote'),
    C('renewal-quote', 'Renewal quote', 'A quote of the prices offered to an existing client for a further term.',
      ['core-event/renewal', 'domain-pricing/quote'], broader='quote'),
    # underwriting inputs
    C('underwriting-input', 'Underwriting input', 'An information asset consumed by underwriting to assess the risk of covering a client.',
      ['domain-pricing/underwriting', 'core-process/inputs'], formalized='core:information-asset', primary='core-process/inputs'),
    C('loss-run', 'Loss run', 'An underwriting input that reports the client\'s history of insurance claims.',
      ['domain-pricing/loss-run'], broader='underwriting-input'),
    C('class-code', 'Class code', 'An underwriting input that classifies a worker\'s occupation by its workers\' compensation risk.',
      ['domain-pricing/class-code'], broader='underwriting-input'),
    C('experience-modification-factor', 'Experience modification factor', 'An underwriting input that adjusts the client\'s workers\' compensation premium for its claims history.',
      ['domain-pricing/experience-modification-factor'], broader='underwriting-input'),
    C('underwriting-guideline', 'Underwriting guideline', 'An underwriting input that states the criteria and limits underwriters apply.',
      ['domain-pricing/underwriting', 'core-rules/guideline'], broader='underwriting-input'),
    # underwriting outcomes
    C('underwriting-outcome', 'Underwriting outcome', 'A decision reached by underwriting on whether, and on what terms, to offer coverage.',
      ['domain-pricing/underwriting', 'core-job/outcome'], formalized='pricing:underwriting-decision'),
    C('underwriting-approval', 'Underwriting approval', 'An underwriting outcome that accepts the client at the quoted prices.',
      ['domain-pricing/underwriting', 'core-process/approval'], broader='underwriting-outcome'),
    C('conditional-approval', 'Conditional approval', 'An underwriting outcome that accepts the client on conditions, such as a higher rate or a deposit.',
      ['core-rules/condition', 'core-process/approval'], broader='underwriting-outcome'),
    C('underwriting-denial', 'Underwriting denial', 'An underwriting outcome that declines to offer coverage.',
      ['domain-pricing/underwriting', 'core-event/denial'], broader='underwriting-outcome', alt=['Declination']),
    C('pricing-exception', 'Pricing exception', 'An underwriting outcome that approves a price or term outside the standard pricing model.',
      ['core-decision/pricing', 'core-issue/exception'], broader='underwriting-outcome'),
    # contract management
    C('pricing-review', 'Pricing review', 'A process step that reviews and approves non-standard prices or terms before a proposal or agreement is offered.',
      ['core-decision/pricing', 'core-governance/review'], formalized='core:process-step', alt=['Deal desk review']),
    # terms
    # statuses
]

BROADMATCH = {
    'pricing-model': 'taxonomy/core-product/pricing-models-and-structures',
    'discount': 'taxonomy/core-product/discounts-and-promotions',
    'underwriting-outcome': 'taxonomy/core-decision/eligibility-determination',
    'pricing-exception': 'taxonomy/core-decision/exception-decision',
    'quote': 'taxonomy/commercial-operations/proposal',
    'pricing-review': 'taxonomy/core-services/contract-management',
}

CLASSES = [
    K('quote', 'Quote', 'An information asset that states the prices at which the organization offers an offering to a prospect or client in pursuit of an opportunity, valid for a stated period.',
      ['core:information-asset'], 'domain-pricing/quote',
      [('some', 'core:concerns', 'commercialops:opportunity'), ('only', 'core:hasComponent', 'core:measure')],
      scope='Its components are the pricing components (measures); a proposal (Commercial Operations) presents one or more quotes.'),
    K('underwriting', 'Underwriting', 'A process that assesses the risk of covering a client and decides whether, and at what price, to offer coverage.',
      ['core:process'], 'domain-pricing/underwriting',
      [('some', 'core:hasStep', 'core:process-step'), ('only', 'core:governedBy', 'core:directive')]),
    K('underwriting-decision', 'Underwriting decision', 'A decision, made in underwriting, on whether and on what terms to offer coverage to a client.',
      ['core:decision'], 'core-decision/decision',
      [('some', 'core:consumes', 'core:information-asset'), ('only', 'core:governedBy', 'core:directive')],
      scope='Kept as a class because it carries its own axioms; it consumes the census, loss runs, class codes and experience modification factor (Baseline decision 8).'),
]

PROPERTIES = []

SHAPES = [
    S('quote', 'Quote shape', 'A shape that checks a quote names the opportunity it prices and is built from pricing components.', 'pricing:quote',
      [dict(path='core:concerns', cls='commercialops:opportunity', min=1, msg='A quote must be for an opportunity.'),
       dict(path='core:hasComponent', cls='core:measure', min=1, msg='A quote should list the pricing components it is built from.', warn=True)]),
    S('underwriting-decision', 'Underwriting decision shape', 'A shape that checks an underwriting decision names its inputs and the guideline that governs it.', 'pricing:underwriting-decision',
      [dict(path='core:consumes', cls='core:information-asset', min=1, msg='An underwriting decision should name the inputs it consumed (census, loss run, class codes).', warn=True),
       dict(path='core:governedBy', cls='core:directive', min=1, msg='An underwriting decision should name the underwriting guideline that governs it.', warn=True)]),
]
