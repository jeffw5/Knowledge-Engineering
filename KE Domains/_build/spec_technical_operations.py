'''Technical Operations: the shared assets of the operational area that provides the organization's technology, data and knowledge services (D26).'''
from dsl import V, C, K, P, S

DOMAIN = dict(
    key='technical-operations', level='area', area='technical-operations', folder='Technical Operations/technical-operations', title='Technical Operations',
    prefix='techops', subject='core-domain/information-technology', parent=None,
    vocabulary_description='A controlled vocabulary of the primitives that the Technical Operations domains share and that the core lacks.',
    taxonomy_description='A classification of the Technical Operations domains: business systems, artificial intelligence strategy and enterprise analytics, platform, data engineering, knowledge engineering and cybersecurity services.',
    ontology_description='The ontology of the Technical Operations operational area. It imports the core domain ontology and holds the classes two or more Technical Operations domains share; it has none yet.',
    version='0.1.0', changes=[('0.1.0', '2026-10-21', 'first release: the shared assets of the operational area, with a taxonomy of its domains (D26).')],
    shapes_description='SHACL shapes for what the Technical Operations domains share; none yet.',
)

VOCAB = [
    V('engineering', 'engineering', 'The disciplined design, construction and operation of systems to meet stated requirements.'),
    V('cybersecurity', 'cybersecurity', 'The protection of information systems, networks and data from attack, damage or unauthorized access.'),
]

TAXONOMY = [
    C('technical-operations-domain', 'Technical operations domain', 'A domain of the Technical Operations operational area: a department that provides technology, data or knowledge services to the organization.',
      ['core-domain/information-technology', 'core-domain/domain'], formalized='core:domain', primary='core-domain/domain'),
    C('business-systems-services-domain', 'Business systems services domain', "A technical operations domain that runs and supports the organization's business applications.",
      ['core-domain/business', 'core-asset/system', 'core-services/services', 'core-domain/domain'], broader='technical-operations-domain', primary='core-domain/domain'),
    C('artificial-intelligence-strategy-and-enterprise-analytics-services-domain', 'Artificial intelligence strategy and enterprise analytics services domain', "A technical operations domain that sets the organization's artificial intelligence strategy and provides its enterprise analytics.",
      ['core-logic/artificial-intelligence', 'core-party/strategy', 'core-party/enterprise', 'core-asset/analytics', 'core-services/services', 'core-domain/domain'], broader='technical-operations-domain', primary='core-domain/domain'),
    C('platform-services-domain', 'Platform services domain', "A technical operations domain that provides the shared computing platforms the organization's systems run on.",
      ['core-asset/platform', 'core-services/services', 'core-domain/domain'], broader='technical-operations-domain', primary='core-domain/domain'),
    C('data-engineering-services-domain', 'Data engineering services domain', "A technical operations domain that builds and runs the pipelines that collect, integrate and deliver the organization's data.",
      ['core-asset/data', 'technical-operations/engineering', 'core-services/services', 'core-domain/domain'], broader='technical-operations-domain', primary='core-domain/domain'),
    C('knowledge-engineering-services-domain', 'Knowledge engineering services domain', "A technical operations domain that builds and governs the organization's vocabularies, taxonomies, ontologies and knowledge graphs.",
      ['core-asset/knowledge', 'technical-operations/engineering', 'core-services/services', 'core-domain/domain'], broader='technical-operations-domain', primary='core-domain/domain'),
    C('cybersecurity-services-domain', 'Cybersecurity services domain', "A technical operations domain that protects the organization's information systems, networks and data.",
      ['technical-operations/cybersecurity', 'core-services/services', 'core-domain/domain'], broader='technical-operations-domain', primary='core-domain/domain'),
]

BROADMATCH = {}

CLASSES = []

PROPERTIES = []

SHAPES = []
