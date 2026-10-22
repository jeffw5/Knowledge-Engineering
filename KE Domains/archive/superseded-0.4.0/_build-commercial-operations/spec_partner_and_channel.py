"""Partner and channel: brokers, referral partners, alliances and the programs that work with them."""
from dsl import V, C, K, P, S

DOMAIN = dict(
    key='partner-and-channel', folder='partner-and-channel', title='Partner and channel', prefix='partnerchannel', subject='core-domain/commercial', parent='commercial-operations',
    vocabulary_description='A controlled vocabulary of the primitives of selling professional employer organization services through partners: alliances, programs, resellers, accountants, banks, franchises, associations and marketplaces.',
    taxonomy_description='A classification of channel partner types, sales channels, partner program elements, partner agreements, partner attribution, partner measures and technology integrations.',
    ontology_description='The partner and channel ontology. It extends the core domain ontology and the Commercial Operations ontology with the channel partner role borne by organizations and the partner programs that govern how partners refer, sell and are rewarded.',
    version='0.1.1', changes=[('0.1.0', '2026-10-20', 'first release.'), ('0.1.1', '2026-10-20', 'Domain ontologies and shapes now name the plain ontology IRIs in owl:imports, so the KE Workbench resolves them, and pin the version built against in dcterms:requires.')],
    shapes_description='SHACL shapes for channel partners and partner programs.',
)

VOCAB = [
    V('alliance', 'alliance', 'A formal relationship between organizations to pursue shared commercial goals.'),
    V('program', 'program', 'A coordinated set of activities, benefits and rules that parties join to pursue a shared goal over time.',
      promote='General primitive missing from the core (core-lifecycle holds "project" and "initiative").'),
    V('reseller', 'reseller', 'A role borne by a party that packages the organization\'s offerings with its own and sells them to its customers.'),
    V('accountant', 'accountant', 'A person or firm qualified to keep and audit financial accounts and to advise on tax.'),
    V('bank', 'bank', 'A financial institution that takes deposits, makes loans and provides payment services.'),
    V('franchise', 'franchise', 'A business licensed to operate under another organization\'s brand and system.'),
    V('association', 'association', 'An organization whose members share an industry, profession or interest.'),
    V('marketplace', 'marketplace', 'A platform where many sellers offer products or services to many buyers.'),
    V('co-marketing', 'co-marketing', 'A marketing effort that the organization and a partner plan, fund and run together.',
      scope='A multiword lexical unit (Baseline decision 3).'),
]

TAXONOMY = [
    # partner types
    C('channel-partner-type', 'Channel partner type', 'A kind of organization that bears the channel partner role for the organization.',
      ['core-product/channel', 'core-role/partner'], formalized='partnerchannel:channel-partner'),
    C('benefits-broker', 'Benefits broker', 'A channel partner type that advises employers on benefits and may refer them to a professional employer organization.',
      ['domain-commercial-operations/benefit', 'core-role/broker'], broader='channel-partner-type'),
    C('insurance-broker', 'Insurance broker', 'A channel partner type that places insurance, including workers\' compensation, for employers.',
      ['domain-commercial-operations/insurance', 'core-role/broker'], broader='channel-partner-type'),
    C('accountant-partner', 'Accountant partner', 'A channel partner type that is an accounting firm advising small and mid-sized businesses on tax and payroll.',
      ['domain-partner-and-channel/accountant', 'core-role/partner'], broader='channel-partner-type', alt=['Accounting firm partner']),
    C('bank-partner', 'Bank partner', 'A channel partner type that is a bank referring its business clients.',
      ['domain-partner-and-channel/bank', 'core-role/partner'], broader='channel-partner-type'),
    C('franchise-partner', 'Franchise partner', 'A channel partner type that is a franchisor offering the organization\'s services to its franchises.',
      ['domain-partner-and-channel/franchise', 'core-role/partner'], broader='channel-partner-type'),
    C('association-partner', 'Association partner', 'A channel partner type that is an association offering the organization\'s services to its members.',
      ['domain-partner-and-channel/association', 'core-role/partner'], broader='channel-partner-type'),
    C('technology-partner', 'Technology partner', 'A channel partner type whose software integrates with the organization\'s technology.',
      ['core-asset/technology', 'core-role/partner'], broader='channel-partner-type'),
    C('alliance-partner', 'Alliance partner', 'A channel partner type that pursues shared commercial goals with the organization under an alliance.',
      ['domain-partner-and-channel/alliance', 'core-role/partner'], broader='channel-partner-type'),
    C('reseller', 'Reseller', 'A channel partner type that packages the organization\'s offerings with its own and sells them.',
      ['domain-partner-and-channel/reseller'], broader='channel-partner-type'),
    # channels
    C('sales-channel', 'Sales channel', 'A route through which the organization\'s offerings reach their buyers.',
      ['core-domain/sales', 'core-product/channel'], formalized='core:asset'),
    C('broker-channel', 'Broker channel', 'A sales channel in which brokers refer or place clients.',
      ['core-role/broker', 'core-product/channel'], broader='sales-channel'),
    C('referral-channel', 'Referral channel', 'A sales channel in which partners, clients or others refer potential clients.',
      ['domain-commercial-operations/referral', 'core-product/channel'], broader='sales-channel'),
    C('alliance-channel', 'Alliance channel', 'A sales channel in which alliance partners offer the organization\'s services to their customers or members.',
      ['domain-partner-and-channel/alliance', 'core-product/channel'], broader='sales-channel'),
    C('marketplace-channel', 'Marketplace channel', 'A sales channel in which buyers find the organization\'s offerings on a marketplace.',
      ['domain-partner-and-channel/marketplace', 'core-product/channel'], broader='sales-channel'),
    # program elements
    C('partner-program', 'Partner program', 'A directive that sets the activities, benefits and rules under which partners refer, sell and are rewarded.',
      ['core-role/partner', 'domain-partner-and-channel/program'], formalized='partnerchannel:partner-program'),
    C('partner-level', 'Partner level', 'A position in a partner program that sets the benefits and requirements that apply to a partner.',
      ['core-role/partner', 'core-measure/level'], broader='partner-program', alt=['Partner tier']),
    C('partner-enablement', 'Partner enablement', 'A partner program element that equips partners with the knowledge, content and tools to refer and sell.',
      ['core-role/partner', 'domain-commercial-operations/enablement'], broader='partner-program'),
    C('co-marketing', 'Co-marketing', 'A partner program element in which the organization and a partner plan, fund and run marketing together.',
      ['domain-partner-and-channel/co-marketing'], broader='partner-program'),
    C('opportunity-registration', 'Opportunity registration', 'A partner program element by which a partner registers an opportunity it sourced, securing credit and protection for it.',
      ['domain-commercial-operations/opportunity', 'domain-commercial-operations/registration'], broader='partner-program', alt=['Deal registration']),
    C('partner-incentive', 'Partner incentive', 'A partner program element that rewards partners for referrals and sales.',
      ['core-role/partner', 'domain-commercial-operations/incentive'], broader='partner-program'),
    C('referral-commission', 'Referral commission', 'A partner incentive paid for a referral that results in a sale.',
      ['domain-commercial-operations/referral', 'domain-commercial-operations/commission'], broader='partner-incentive', alt=['Referral fee']),
    C('broker-commission', 'Broker commission', 'A partner incentive paid to a broker for a client it placed, often for as long as it remains broker of record.',
      ['core-role/broker', 'domain-commercial-operations/commission'], broader='partner-incentive'),
    # agreements
    C('partner-agreement', 'Partner agreement', 'A commercial agreement between the organization and a partner.',
      ['core-role/partner', 'core-policy/agreement'], formalized='core:directive'),
    C('referral-agreement', 'Referral agreement', 'A partner agreement that sets the terms on which a partner refers potential clients and is paid for them.',
      ['domain-commercial-operations/referral', 'core-policy/agreement'], broader='partner-agreement'),
    C('alliance-agreement', 'Alliance agreement', 'A partner agreement that sets the terms of an alliance.',
      ['domain-partner-and-channel/alliance', 'core-policy/agreement'], broader='partner-agreement'),
    C('broker-of-record', 'Broker of record', 'A partner agreement, made by a letter from a client, that designates the broker who represents the client for its benefits or insurance.',
      ['core-role/broker', 'core-asset/record'], broader='partner-agreement', alt=['Broker of record letter']),
    # attribution
    C('partner-attribution', 'Partner attribution', 'An information asset that records the credit given to a partner for a lead, opportunity or sale.',
      ['core-role/partner', 'domain-commercial-operations/attribution'], formalized='core:information-asset'),
    C('partner-sourced-opportunity', 'Partner-sourced opportunity', 'A partner attribution of an opportunity that a partner brought to the organization.',
      ['core-role/partner', 'core-asset/source', 'domain-commercial-operations/opportunity'], broader='partner-attribution'),
    C('partner-influenced-opportunity', 'Partner-influenced opportunity', 'A partner attribution of an opportunity that a partner helped advance but did not source.',
      ['core-role/partner', 'domain-commercial-operations/influence', 'domain-commercial-operations/opportunity'], broader='partner-attribution'),
    # measures
    C('partner-measure', 'Partner measure', 'A measure of the performance of the partner channel.',
      ['core-role/partner', 'core-measure/measure'], formalized='core:measure'),
    C('partner-sourced-pipeline', 'Partner-sourced pipeline', 'A partner measure of the value of open opportunities that partners sourced.',
      ['core-role/partner', 'core-asset/source', 'domain-commercial-operations/pipeline'], broader='partner-measure'),
    C('partner-sourced-sales', 'Partner-sourced sales', 'A partner measure of the sales in a period that partners sourced.',
      ['core-role/partner', 'core-asset/source', 'domain-commercial-operations/sale'], broader='partner-measure'),
    C('referral-conversion-rate', 'Referral conversion rate', 'A partner measure of the share of referrals that become clients.',
      ['domain-commercial-operations/referral', 'domain-commercial-operations/conversion', 'core-measure/rate'], broader='partner-measure'),
    # integration
    C('technology-integration', 'Technology integration', 'A capability that connects a technology partner\'s software with the organization\'s, so that data and processes flow between them.',
      ['core-asset/technology', 'core-capability/integration'], formalized='core:capability'),
    C('marketplace-listing', 'Marketplace listing', 'A technology integration offered to buyers through a partner\'s marketplace.',
      ['domain-partner-and-channel/marketplace', 'core-capability/integration'], broader='technology-integration'),
]

BROADMATCH = {
    'channel-partner-type': 'taxonomy/core-role/partner',
    'benefits-broker': 'taxonomy/core-role/broker',
    'insurance-broker': 'taxonomy/core-role/broker',
    'partner-agreement': 'taxonomy/domain-commercial-operations/commercial-agreement',
    'partner-attribution': 'taxonomy/domain-commercial-operations/attribution',
    'partner-measure': 'taxonomy/core-measure/key-performance-indicator',
    'referral-commission': 'taxonomy/domain-commercial-operations/referral',
}

CLASSES = [
    K('channel-partner', 'Channel partner', 'A role borne by an organization that refers, sells or integrates with the organization\'s offerings under a partner agreement.',
      ['core:role'], 'core-role/partner',
      [('some', 'core:roleOf', 'core:organization')]),
    K('partner-program', 'Partner program', 'A directive that sets the activities, benefits and rules under which channel partners refer, sell and are rewarded.',
      ['core:directive'], 'domain-partner-and-channel/program',
      [('some', 'core:governs', 'partnerchannel:channel-partner')]),
]

PROPERTIES = []

SHAPES = [
    S('channel-partner', 'Channel partner shape', 'A shape that checks the channel partner role is borne by an organization.', 'partnerchannel:channel-partner',
      [dict(path='core:roleOf', cls='core:organization', min=1, msg='A channel partner role must be borne by an organization.')]),
    S('partner-program', 'Partner program shape', 'A shape that checks a partner program governs channel partners.', 'partnerchannel:partner-program',
      [dict(path='core:governs', min=1, msg='A partner program should govern the channel partners enrolled in it.', warn=True)]),
]
