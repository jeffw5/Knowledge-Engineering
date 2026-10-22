'''Business Operations: the shared assets of the operational area that runs the organization's own business (D26).'''
from dsl import V, C, K, P, S

DOMAIN = dict(
    key='business-operations', level='area', area='business-operations', folder='Business Operations/business-operations', title='Business Operations',
    prefix='businessops', subject='core-domain/business', parent=None,
    vocabulary_description='A controlled vocabulary of the primitives that the Business Operations domains share and that the core lacks.',
    taxonomy_description='A classification of the Business Operations domains: finance, accounting, human resources, billing and accounts receivable, compliance, legal and security.',
    ontology_description='The ontology of the Business Operations operational area. It imports the core domain ontology and holds the classes two or more Business Operations domains share; it has none yet.',
    version='0.1.0', changes=[('0.1.0', '2026-10-21', 'first release: the shared assets of the operational area, with a taxonomy of its domains (D26).')],
    shapes_description='SHACL shapes for what the Business Operations domains share; none yet.',
)

VOCAB = [
    V('accounting', 'accounting', "The recording, classification and reporting of an organization's financial transactions."),
    V('billing', 'billing', 'The preparation and issue of invoices for the services an organization provides.'),
    V('accounts-receivable', 'accounts receivable', 'The amounts owed to an organization by its clients for services delivered and invoiced.', scope='A multiword lexical unit (Baseline decision 3).'),
]

TAXONOMY = [
    C('business-operations-domain', 'Business operations domain', "A domain of the Business Operations operational area: a department that runs the organization's own business.",
      ['core-domain/business', 'core-domain/domain'], formalized='core:domain', primary='core-domain/domain'),
    C('finance-domain', 'Finance domain', "A business operations domain that plans, funds and controls the organization's financial resources.",
      ['core-domain/finance', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
    C('accounting-domain', 'Accounting domain', "A business operations domain that records, classifies and reports the organization's financial transactions.",
      ['business-operations/accounting', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
    C('human-resources-domain', 'Human resources domain', "A business operations domain that manages the organization's own employees.",
      ['core-domain/human-resource', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
    C('billing-and-accounts-receivable-domain', 'Billing and accounts receivable domain', 'A business operations domain that invoices clients for service fees and collects what they owe.',
      ['business-operations/billing', 'business-operations/accounts-receivable', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
    C('compliance-domain', 'Compliance domain', 'A business operations domain that keeps the organization in conformance with the laws, regulations and standards that apply to it.',
      ['core-domain/compliance', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
    C('legal-domain', 'Legal domain', "A business operations domain that gives legal advice and manages the organization's agreements and legal matters.",
      ['core-domain/legal', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
    C('security-domain', 'Security domain', "A business operations domain that protects the organization's people, premises and information.",
      ['core-domain/security', 'core-domain/domain'], broader='business-operations-domain', primary='core-domain/domain'),
]

BROADMATCH = {}

CLASSES = []

PROPERTIES = []

SHAPES = []
