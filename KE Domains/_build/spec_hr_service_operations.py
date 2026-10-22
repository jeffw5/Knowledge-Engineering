'''HR Service Operations: the shared assets of the operational area that delivers the external services of the HR Services & PEO Enterprise Business Model (D25, D26).'''
from dsl import V, C, K, P, S

DOMAIN = dict(
    key='hr-service-operations', level='area', area='hr-service-operations', folder='HR Service Operations/hr-service-operations', title='Human Resources Service Operations', alt_title='HR Service Operations',
    prefix='hrserviceops', subject='core-domain/human-resource', parent=None,
    vocabulary_description='A controlled vocabulary of the primitives that the HR Service Operations domains share and that the core lacks.',
    taxonomy_description='A classification of the HR Service Operations domains, the L1 domains of the HR Services & PEO Enterprise Business Model.',
    ontology_description='The ontology of the HR Service Operations operational area. It imports the core domain ontology and holds the classes two or more HR Service Operations domains share; it has none yet.',
    version='0.1.0', changes=[('0.1.0', '2026-10-21', 'first release: the shared assets of the operational area, with a taxonomy of its domains (D26).')],
    shapes_description='SHACL shapes for what the HR Service Operations domains share; none yet.',
)

VOCAB = [
    V('administration', 'administration', 'The organized performance of the routine work of running an activity, such as payroll or benefits, on behalf of others.'),
    V('retirement', 'retirement', 'The period after a worker leaves the workforce, and the savings and plans that provide for it.'),
    V('sponsorship', 'sponsorship', 'The act of establishing and maintaining a benefit plan and bearing the duties of its sponsor.'),
    V('government', 'government', 'The bodies that make, administer and enforce law and regulation for a jurisdiction.'),
    V('talent', 'talent', 'The skills and abilities of the people an employer attracts, develops and retains.'),
    V('coaching', 'coaching', 'Guidance given to a person over time to improve their performance or development.'),
    V('culture', 'culture', 'The shared values, beliefs and behaviors that characterize an organization.'),
    V('ethics', 'ethics', 'The principles of right conduct that govern a person or an organization.'),
    V('stewardship', 'stewardship', "The responsible care and management of something entrusted to one's keeping."),
    V('experience', 'experience', 'What a person perceives and feels in their interactions with an organization, its services and its tools.'),
]

TAXONOMY = [
    C('hr-service-operations-domain', 'Human resources service operations domain', 'A domain of the HR Service Operations operational area: an L1 domain of the HR Services & PEO Enterprise Business Model that delivers external services to clients and their worksite employees.',
      ['core-domain/human-resource', 'core-services/services', 'core-process/operation', 'core-domain/domain'], formalized='core:domain', primary='core-domain/domain'),
    C('workforce-administration-and-payroll-domain', 'Workforce administration and payroll domain', 'A human resources service operations domain that pays worksite employees and administers time, attendance and leave.',
      ['core-party/workforce', 'hr-service-operations/administration', 'commercial-operations/payroll', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('employee-benefits-and-retirement-sponsorship-domain', 'Employee benefits and retirement sponsorship domain', 'A human resources service operations domain that sponsors and administers health, welfare and retirement plans for worksite employees.',
      ['core-role/employee', 'commercial-operations/benefit', 'hr-service-operations/retirement', 'hr-service-operations/sponsorship', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('government-compliance-and-employer-risk-management-domain', 'Government compliance and employer risk management domain', "A human resources service operations domain that manages the employer's compliance with employment law and its co-employment, workers' compensation and safety risk.",
      ['hr-service-operations/government', 'core-domain/compliance', 'core-role/employer', 'core-domain/risk', 'core-process/management', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('talent-management-and-organizational-development-domain', 'Talent management and organizational development domain', 'A human resources service operations domain that helps clients recruit, onboard, develop and retain their people.',
      ['hr-service-operations/talent', 'core-process/management', 'core-party/organization', 'core-product/development', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('client-relationship-and-business-development-domain', 'Client relationship and business development domain', 'A human resources service operations domain that wins, onboards and retains the clients the external services are delivered to.',
      ['core-role/client', 'core-party/relationship', 'core-domain/business', 'core-product/development', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('hr-technology-platform-and-employee-experience-domain', 'Human resources technology platform and employee experience domain', 'A human resources service operations domain that provides the self-service platform, integrations and analytics through which clients and worksite employees use the services.',
      ['core-domain/human-resource', 'core-asset/technology', 'core-asset/platform', 'core-role/employee', 'hr-service-operations/experience', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('workforce-development-coaching-and-performance-measurement-domain', 'Workforce development, coaching and performance measurement domain', 'A human resources service operations domain that delivers training and coaching and measures performance and development.',
      ['core-party/workforce', 'core-product/development', 'hr-service-operations/coaching', 'core-measure/performance', 'core-process/measurement', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
    C('organizational-values-culture-and-ethics-stewardship-domain', 'Organizational values, culture and ethics stewardship domain', "A human resources service operations domain that promotes, monitors and measures an organization's values and culture without violating privacy.",
      ['core-party/organization', 'core-value/value', 'hr-service-operations/culture', 'hr-service-operations/ethics', 'hr-service-operations/stewardship', 'core-domain/domain'], broader='hr-service-operations-domain', primary='core-domain/domain'),
]

BROADMATCH = {}

CLASSES = []

PROPERTIES = []

SHAPES = []
