'''PEO Service Map: crosswalk to the PEO Service Landscape and proposed expansion (authored source, Draft 2026-10-23).

Read by build_service_map.py. Three parts:
  CROSSWALK   every PEO Service Landscape row (tools/peo-service-landscape.html) mapped to the L3 domain services
              that deliver it, with the fit (direct, partial, none) and what is missing;
  DELIVERY    offer and delivery models (co-employment, ASO, software only, EOR...): a dimension of the offer, not
              L3 services;
  PROPOSALS   L3 services to add, from three origins:
                catalog     Insperity sells it (landscape baseline) but the business model has no service for it;
                competitor  competitors deliver it and the model has no service for it;
                semantic    services the semantic knowledge layer and semantic governance make possible: compliance,
                            risk profiling, decision support, and metrology and assurance for agentic capabilities.
              New L1 domains, L2 bounded contexts and service lines are declared here too.

Every proposal is Draft and needs a business and compliance decision before it enters the business model.
'''

# ---- the semantic knowledge layer capabilities a proposal builds on ------------------------------------------
ENABLERS = {
    'ssot': ('Rules, constraints and logic (SSOT)', 'The governed register of rules, constraints and calculations, versioned, with impact analysis (SSOT Rules Map, SSOT Editor).'),
    'dq': ('Decision question baseline', 'The decision and competency questions each decision must answer, with its obligations, permissions and prohibitions.'),
    'ontology': ('Core domain ontology', 'The unifying ontology anchored on the process step: who performs it, what it consumes and produces, which rules govern it and which measures evaluate it (BFO-aligned).'),
    'shacl': ('Shapes and conformance', 'SHACL shapes and Part III conformance checks that validate data and assertions before they are used.'),
    'gateway': ('Semantic gateway', 'The requirements engineering semantic gateway: traced, reviewed, evidenced, measurable, owned and unflagged before admission.'),
    'agents': ('Governed agents', 'Agents behind a validation gate (SHACL, then rules, then policy enforcement), with circuit breakers, human review and recorded commits.'),
    'prov': ('Provenance and versioning', 'PROV-O change records, semantic versioning and named graphs for every asset and decision.'),
    'c360': ('Customer 360', 'Personas, jobs to be done, desired outcomes and their measured importance and satisfaction.'),
    'privacy': ('Privacy-preserving analytics', 'Purpose limitation, notice and consent, de-identification and aggregation thresholds, retention (the Privacy-Preserving People Analytics context).'),
    'measures': ('Measures and metrology', 'Measures attached to process steps (SIPOCM), with definitions, units, targets and measured values that can be traced and calibrated.'),
    'apqc': ('Process registry and assemblies', 'APQC-anchored processes and the service assemblies that show which internal steps deliver each service.'),
}

# ---- evidence found beyond the landscape ---------------------------------------------------------------------
EVIDENCE = {
    'adp-agents': ('ADP launches AI agents for payroll variance audits, tax registration, HR policy answers, analytics and talent actions (ADP, 2026-01-28)', 'https://mediacenter.adp.com/2026-01-28-ADP-R-Accelerates-AI-Leadership-with-Launch-of-New-AI-Agents-Designed-to-Solve-Workforce-Challenges'),
    'paychex-ewa': ('Tapcheck on-demand pay embedded in the Paychex HR PEO for worksite employees (Business Wire, 2026)', 'https://www.businesswire.com/news/home/20260401366206/en/Tapcheck-Teams-with-Paychex-to-Deliver-Seamless-Embedded-On-Demand-Pay-Solution-Giving-Instant-Access-to-Worksite-Employees'),
    'adp-wisely': ('ADP Wisely adds earned wage access (HCM Technology Report)', 'https://www.hcmtechnologyreport.com/adp-launches-new-version-of-wisely-including-earned-wage-access/'),
    'paychex-credits': ('Paychex Tax Credit Services: WOTC and location-based credits (Paychex investor relations)', 'https://investor.paychex.com/news-events/press-releases/detail/648/paychex-launches-tax-credit-services'),
    'trinet-clarus': ('TriNet acquires Clarus R+D and forms a tax credits business unit (Accounting Today, 2022)', 'https://www.accountingtoday.com/news/trinet-acquires-clarus-r-d'),
    'rippling-hr': ('Rippling HR Services: Compliance 360, handbook builder, automated filings, EPLI, role-based training (Rippling)', 'https://www.rippling.com/en-GB/products/hr/hr-services'),
    'rippling-headcount': ('Rippling Headcount Planning (SoftwareOne listing)', 'https://platform.softwareone.com/product/headcount-planning/PCP-2795-2585'),
    'justworks-contractors': ('Justworks pays international contractors in 50+ countries and converts them through its EOR (Justworks, 2025-07-31)', 'https://www.justworks.com/product-updates/now-offering-usd-payments-for-international-contractors'),
    'paychex-pep': ('Paychex introduces a pooled employer 401(k) plan (Paychex)', 'https://www.paychex.com/newsroom/news-releases/paychex-introduces-pooled-employer-plan-new-cost-effective-retirement-plan'),
    'colorado-ai': ('Colorado S.B. 26-189 replaces the Colorado AI Act; notice, adverse-action and record duties from 2027-01-01 (Littler)', 'https://www.littler.com/news-analysis/asap/colorado-amends-its-artificial-intelligence-law-substantially-reducing'),
    'illinois-ai': ('Illinois HB 3773: notice and anti-discrimination rules for AI in employment decisions from 2026-01-01 (Hunton)', 'https://www.hunton.com/hunton-employment-labor-perspectives/illinois-enacts-new-law-regulating-employer-use-of-artificial-intelligence'),
}

# ---- crosswalk: landscape row -> L3 domain services --------------------------------------------------------
# fit: direct (the services deliver the row), partial (part of it is missing: see gap), none (no service)
CROSSWALK = {
    'PAY.01': (['GrossToNetPayrollService', 'DirectDepositOffCycleService'], 'direct', ''),
    'PAY.02': (['MultiStateTaxFilingService', 'YearEndTaxDocService', 'CPEOComplianceMonitoringService'], 'direct', ''),
    'PAY.03': (['TimeCapturePunchService', 'TimesheetApprovalStagingService', 'CustomPTOAccrualService'], 'direct', ''),
    'PAY.04': ([], 'none', 'No expense reimbursement service, although Insperity sells one.'),
    'PAY.05': (['WageGarnishmentService'], 'partial', 'Unemployment claims administration has no service.'),
    'BEN.01': (['PEOMasterHealthPlanService', 'OpenEnrollmentLifeEventService'], 'direct', ''),
    'BEN.02': (['MultipleEmployerPlan401kService', 'SafeHarborEmployerMatchService', 'ConsolidatedForm5500AuditService', 'NondiscriminationComplianceTestingService'], 'direct', ''),
    'BEN.03': (['FlexibleSpendingAccountsService'], 'partial', 'Commuter benefits are not named.'),
    'BEN.04': (['VoluntaryAncillaryBenefitsService'], 'direct', ''),
    'BEN.05': (['COBRAAdministrationService'], 'partial', 'Affordable Care Act employer mandate and information reporting have no service.'),
    'BEN.06': ([], 'none', 'No individual coverage health reimbursement arrangement.'),
    'BEN.07': ([], 'none', 'No mental health or family-forming benefit.'),
    'RSK.01': (['WorkersCompMasterPolicyService', 'FNOIClaimsTriageService', 'ModifiedDutyReturnToWorkService'], 'direct', ''),
    'RSK.02': (['EPLIDefenseService'], 'direct', ''),
    'RSK.03': (['WorksiteSafetyHazardService', 'OSHA300ComplianceReportingService'], 'direct', ''),
    'RSK.04': (['MultiStateHandbookPolicyService', 'CPEOComplianceMonitoringService'], 'partial', 'No continuous monitoring of the client against changing law (Rippling sells this as Compliance 360).'),
    'RSK.05': (['StatutoryLeaveFMLAService'], 'direct', ''),
    'RSK.06': ([], 'none', 'No cyber liability coverage.'),
    'RSK.07': ([], 'none', 'No business insurance service, although Insperity sells business insurance.'),
    'HRA.01': (['ClientEscalationResolutionService', 'ClientHealthScoringRetentionService'], 'partial', 'The dedicated advisor relationship itself is not a service.'),
    'HRA.02': (['MultiStateHandbookPolicyService'], 'direct', ''),
    'HRA.03': (['EEOC_DOL_DefenseConsultService', 'EPLIDefenseService'], 'partial', 'Day-to-day employee relations advice and investigations are not a service; only agency defense is.'),
    'HRA.04': ([], 'none', 'No industry-packaged advisory.'),
    'HRA.05': (['OrganizationalScorecardService', 'LeadershipSuccessionPlanningService'], 'partial', 'Organizational planning advice is not a service.'),
    'TAL.01': (['RecruitingProcessOutsourcingService'], 'direct', ''),
    'TAL.02': (['RecruitingProcessOutsourcingService'], 'partial', 'Applicant tracking and job distribution are inside recruiting outsourcing only.'),
    'TAL.03': (['PreEmploymentScreeningService', 'FormI9EVerifyService'], 'direct', ''),
    'TAL.04': (['DigitalNewHireOnboardingService'], 'direct', ''),
    'TAL.05': (['Feedback360AppraisalCycleService', 'ContinuousPerformanceCheckInService', 'StrategicGoalAlignmentOKRService'], 'direct', ''),
    'TAL.06': (['CorporateLMSDeliveryService', 'InstructorLedVirtualTrainingService', 'SkillsGapTrainingPlanService', 'HarassmentPreventionTrainingService'], 'direct', ''),
    'TAL.07': (['MarketWageBenchmarkingService', 'MeritMatrixCompensationPlanningService', 'LeadershipSuccessionPlanningService'], 'direct', ''),
    'TAL.08': ([], 'none', 'No outplacement service, although Insperity sells one.'),
    'TEC.01': (['EmployeeSelfServicePortalService', 'ClientAdminPortalReportingService'], 'direct', ''),
    'TEC.02': (['HRISDataIntegrationConnectorService'], 'partial', 'The enterprise HCM path (HRScale on Workday) is an offer, not a service: see delivery models.'),
    'TEC.03': (['EmployeeSelfServicePortalService', 'MobileWorkforceAppService'], 'direct', ''),
    'TEC.04': (['ClientAdminPortalReportingService', 'WorkforceAnalyticsReportingService'], 'direct', ''),
    'TEC.05': ([], 'none', 'No agentic or AI-assisted service in the model.'),
    'TEC.06': ([], 'none', 'No device or application management.'),
    'TEC.07': (['HRISDataIntegrationConnectorService'], 'partial', 'The partner marketplace itself is not a service.'),
    'MOD.01': (['MasterServiceAgreementContractingService', 'CPEOComplianceMonitoringService'], 'direct', 'Delivery model.'),
    'MOD.02': ([], 'none', 'Delivery model: see delivery models.'),
    'MOD.03': ([], 'none', 'Delivery model: see delivery models.'),
    'MOD.04': ([], 'none', 'Delivery model and a new domain: see proposals.'),
    'MOD.05': ([], 'none', 'Commercial policy: see delivery models.'),
}

# ---- offer and delivery models (a dimension of the offer, not L3 services) ---------------------------------
DELIVERY = [
    ('co-employment', 'Full co-employment PEO', ['MOD.01'], 'HR360', 'The model assumes this offer.'),
    ('software-only', 'Payroll and HCM software without co-employment', ['MOD.03'], 'HRCore', 'Insperity sells it; the model should say which L3 services it includes.'),
    ('enterprise-hcm', 'Enterprise HCM inside the PEO', ['TEC.02'], 'HRScale (Workday)', 'Insperity sells it to 150-5,000 employee firms; ADP and Rippling are the only peers with a comparable path.'),
    ('middle-market', 'Co-employment with strategic HR added for a fee', ['HRA.05'], 'Workforce Synchronization', 'Insperity sells it; the strategic HR services it adds should be named.'),
    ('aso', 'Administrative services only (no co-employment)', ['MOD.02'], '', 'TriNet, Paychex, VensureHR and ADP sell it; Insperity does not.'),
    ('eor', 'International employer of record', ['MOD.04'], '', 'Justworks, TriNet, VensureHR and Rippling sell it; see the Global Employment domain proposal.'),
    ('published-pricing', 'Published per-employee pricing', ['MOD.05'], '', 'Only Justworks publishes prices. A transparent total-cost view (proposal D03) answers the same buyer questions without a price list.'),
]

# ---- new service lines, L1 domains and L2 bounded contexts --------------------------------------------------
NEW_LINES = [
    ('ServiceLineGlobalWorkforce', 'Global Workforce', 'Hiring and paying people outside the United States, and managing contractors.'),
    ('ServiceLineBusinessInsurance', 'Business Insurance', 'Commercial insurance beyond workers’ compensation and employment practices liability.'),
    ('ServiceLineComplianceIntelligence', 'Compliance Intelligence', 'Knowing which obligations apply, proving they are met, and checking decisions against them before they take effect.'),
    ('ServiceLineRiskIntelligence', 'Risk Intelligence', 'Profiling and forecasting the client’s employer risk so it can be priced, prevented and explained.'),
    ('ServiceLineDecisionIntelligence', 'Decision Intelligence', 'Governed, explainable support for the recurring people and cost decisions clients make.'),
    ('ServiceLineAgenticAssurance', 'Agentic Assurance', 'Agents that answer and act with measured, calibrated accuracy, guardrails and a provenance record.'),
]
NEW_DOMAINS = [
    ('WorkforceIntelligenceAssuranceDomain', 9, 'Workforce Intelligence, Risk & Agentic Assurance',
     'A proposed L1 domain that turns the semantic knowledge layer and semantic governance into client services: compliance intelligence, employer risk profiling, decision support, and measured, governed agents.'),
    ('GlobalEmploymentDomain', 10, 'Global Employment & Contingent Workforce',
     'A proposed L1 domain for employing people outside the United States through an employer of record and for engaging and paying contractors.'),
]
# id, label, L1 (existing or new)
NEW_CONTEXTS = [
    ('PayAccessSpendSubDomain', 'Pay Access & Employee Spend', 'WorkforceAdminDomain'),
    ('EmployerTaxIncentivesSubDomain', 'Employer Tax Credits & Incentives', 'WorkforceAdminDomain'),
    ('CommercialInsuranceSubDomain', 'Commercial Insurance & Risk Transfer', 'ComplianceRiskDomain'),
    ('WorkforceTransitionsSubDomain', 'Workforce Transitions', 'TalentManagementDomain'),
    ('IndustryPracticesSubDomain', 'Industry Practices', 'ClientRelationshipDomain'),
    ('RegulatoryIntelligenceSubDomain', 'Regulatory Intelligence & Compliance Assurance', 'WorkforceIntelligenceAssuranceDomain'),
    ('EmployerRiskProfilingSubDomain', 'Employer Risk Profiling', 'WorkforceIntelligenceAssuranceDomain'),
    ('DecisionIntelligenceSubDomain', 'Decision Intelligence & Workforce Data Products', 'WorkforceIntelligenceAssuranceDomain'),
    ('AgenticAssuranceSubDomain', 'Agentic Assurance & Metrology', 'WorkforceIntelligenceAssuranceDomain'),
    ('InternationalEmploymentSubDomain', 'International Employment', 'GlobalEmploymentDomain'),
    ('ContingentWorkforceSubDomain', 'Contingent Workforce', 'GlobalEmploymentDomain'),
]


def P(id, label, context, line, origin, rec, rows=(), competitors=(), evidence=(), enablers=(), addresses=(), why='', extends=''):
    return dict(id=id, label=label, context=context, line=line, origin=origin, rec=rec, rows=list(rows), competitors=list(competitors),
                evidence=list(evidence), enablers=list(enablers), addresses=list(addresses), why=why, extends=extends)


PROPOSALS = [
    # ---- Insperity sells it; the business model has no service ----
    P('C01', 'Employee Expense Reimbursement Service', 'PayAccessSpendSubDomain', 'Payroll', 'catalog', 'pursue', ['PAY.04'], ['tri', 'rip'],
      why='Insperity lists expense management as a product; add it to the model so it can be traced to jobs and delivered through the payroll steps it touches.'),
    P('C02', 'Outplacement & Career Transition Service', 'WorkforceTransitionsSubDomain', 'Talent Management', 'catalog', 'pursue', ['TAL.08'], [],
      addresses=['O089'], why='Insperity is the only provider in the landscape that offers outplacement. It belongs in the model, next to the separation questions it answers.'),
    P('C03', 'Business Insurance Brokerage Service', 'CommercialInsuranceSubDomain', 'Business Insurance', 'catalog', 'pursue', ['RSK.07'], ['pay'],
      why='Insperity sells business insurance; the model has no service for it, so it cannot be bundled with risk profiling or renewals.'),
    P('C04', 'Partner Marketplace Service', 'DataIntegrationAnalyticsSubDomain', 'HR Technology & Data', 'catalog', 'pursue', ['TEC.07'], ['adp'],
      addresses=['O179'], why='Insperity MarketPlace exists; naming it as a service lets connectors and partner offers be governed like any other service.'),
    # ---- competitors deliver it; the model has no service ----
    P('M01', 'Earned Wage Access Service', 'PayAccessSpendSubDomain', 'Payroll', 'competitor', 'partner', [], ['pay', 'adp'], ['paychex-ewa', 'adp-wisely'],
      ['ssot', 'agents'], ['O009'], why='Paychex embedded on-demand pay in its PEO in 2026 and ADP offers it through Wisely. A partner can supply the funding; the pay rules and limits belong in the rules register.'),
    P('M02', 'Unemployment Claims Administration Service', 'PayrollTaxSubDomain', 'Payroll', 'competitor', 'pursue', ['PAY.05'], ['adp', 'pay'], [],
      ['ssot', 'dq'], ['O016'], why='ADP and Paychex list it. Each unemployment claim affects the state unemployment rate the co-employer pays.'),
    P('M03', 'Employer Tax Credit Identification & Recovery Service', 'EmployerTaxIncentivesSubDomain', 'Payroll', 'competitor', 'pursue', [], ['pay', 'tri'],
      ['paychex-credits', 'trinet-clarus'], ['ssot', 'dq', 'shacl'], ['O016', 'O102'],
      why='Paychex screens every payroll client for hiring and location credits; TriNet bought an R&D credit business. Eligibility is a set of rules over hires, locations and wages that the rules register can evaluate for every client.'),
    P('M04', 'Affordable Care Act Employer Mandate & Information Reporting Service', 'HealthWelfareSponsorshipSubDomain', 'Benefits', 'competitor', 'pursue', ['BEN.05'], ['tri'], [],
      ['ssot', 'shacl'], ['O079'], why='TriNet names it; the model covers continuation coverage but not measurement periods, affordability tests or the annual reporting.'),
    P('M05', 'Commuter Benefits', 'HealthWelfareSponsorshipSubDomain', 'Benefits', 'competitor', 'pursue', ['BEN.03'], ['rip', 'jw'], [], [], ['O041'],
      extends='FlexibleSpendingAccountsService', why='Add to the tax-advantaged accounts service rather than a new service.'),
    P('M06', 'Individual Coverage Health Reimbursement Arrangement Service', 'HealthWelfareSponsorshipSubDomain', 'Benefits', 'competitor', 'monitor', ['BEN.06'], ['jw'], [],
      ['ssot'], ['O039', 'O040', 'O044'], why='Only Justworks offers it, through a partner, launched in 2026. Watch take-up; it competes with the master health plan.'),
    P('M07', 'Mental Health & Family-Forming Benefits Service', 'HealthWelfareSponsorshipSubDomain', 'Benefits', 'competitor', 'partner', ['BEN.07'], ['jw'], [], [],
      ['O036', 'O043'], why='Justworks bundles these in its top tier; they answer the candidate and retention questions on benefits.'),
    P('M08', 'Pooled Employer Plan Option', 'RetirementMEP401kSubDomain', 'Benefits', 'competitor', 'monitor', [], ['pay'], ['paychex-pep'], [], ['O055', 'O059'],
      extends='MultipleEmployerPlan401kService', why='Paychex offers a pooled employer plan. Compare fiduciary allocation and cost against the existing multiple employer plan before changing anything.'),
    P('M09', 'Cyber Liability Insurance Service', 'CommercialInsuranceSubDomain', 'Business Insurance', 'competitor', 'partner', ['RSK.06'], ['pay'], [], [], ['O183'],
      why='Paychex lists cyber liability in its Oasis offer. A partner product, priced from the client risk profile (R01).'),
    P('M10', 'Dedicated HR Business Partner Service', 'ClientSuccessAccountMgmtSubDomain', 'PEO Relationship', 'competitor', 'pursue', ['HRA.01'], ['adp', 'tri', 'pay', 'rip', 'ven'], [],
      ['c360', 'prov'], ['O211', 'O213', 'O082'], why='Every provider names the advisor relationship; in the model it is only implied by escalation and retention. Making it a service lets its outcomes be measured.'),
    P('M11', 'Employee Relations Advisory & Investigation Service', 'EmployerLiabilityPracticesSubDomain', 'HR Compliance', 'competitor', 'pursue', ['HRA.03'], ['adp', 'tri', 'pay', 'rip'], [],
      ['dq', 'ssot', 'prov'], ['O081', 'O083', 'O085'], why='Competitors advise before a claim; the model only defends after one.'),
    P('M12', 'Industry Practice Advisory Service', 'IndustryPracticesSubDomain', 'PEO Relationship', 'competitor', 'pursue', ['HRA.04'], ['tri', 'ven'], [],
      ['ontology', 'ssot', 'c360'], ['O212', 'O216'], why='TriNet sells seven industry teams. Industry rule sets and process variants can be modeled once and reused, so an industry practice is a configuration, not a separate team.'),
    P('M13', 'Applicant Tracking & Job Distribution Service', 'TalentAcquisitionOnboardingSubDomain', 'Talent Management', 'competitor', 'pursue', ['TAL.02'], ['pay', 'ven', 'adp', 'rip'], [], [],
      ['O101', 'O106'], why='Most competitors sell applicant tracking on its own; the model has it only inside recruiting outsourcing.'),
    P('M14', 'Headcount & Workforce Planning Service', 'DataIntegrationAnalyticsSubDomain', 'Measurement', 'competitor', 'pursue', [], ['rip'], ['rippling-headcount'],
      ['ontology', 'measures'], ['O171', 'O176'], why='Rippling sells headcount planning. Workforce plans join headcount, cost and budget, which the knowledge layer already relates.'),
    P('M15', 'Device & Application Management Service', 'DigitalSelfServiceExperienceSubDomain', 'HR Technology & Data', 'competitor', 'decline', ['TEC.06'], ['rip'], [], [],
      ['O110', 'O186'], why='Only Rippling offers it and it sits outside the PEO’s role. Answer the first-day access and offboarding questions through identity integration and the partner marketplace instead.'),
    P('M16', 'International Employer of Record Service', 'InternationalEmploymentSubDomain', 'Global Workforce', 'competitor', 'partner', ['MOD.04'], ['jw', 'tri', 'ven', 'rip'],
      ['justworks-contractors'], ['ssot', 'ontology'], [], why='Four of the six competitors offer it. A partner network can carry the local employment; the knowledge layer holds each country’s rules.'),
    P('M17', 'International Contractor Management & Payments Service', 'ContingentWorkforceSubDomain', 'Global Workforce', 'competitor', 'partner', [], ['jw'],
      ['justworks-contractors'], ['ssot'], ['O019'], why='Justworks pays contractors in 50+ countries and converts them to employees through its EOR.'),
    # ---- made possible by the semantic knowledge layer and semantic governance ----
    P('S01', 'Regulatory Change Intelligence Service', 'RegulatoryIntelligenceSubDomain', 'Compliance Intelligence', 'semantic', 'pursue', ['RSK.04'], ['rip', 'adp'],
      ['rippling-hr', 'adp-agents'], ['ssot', 'ontology', 'prov'], ['O071', 'O072', 'O077', 'O078', 'O011'],
      why='Matches the client’s footprint (states, cities, headcount thresholds, industry) against the versioned rules register and tells the client which obligations changed, when they take effect and which of their process steps they govern. Rippling’s Compliance 360 flags violations; this explains the obligation and its source.'),
    P('S02', 'Obligation-to-Control Mapping & Audit Evidence Service', 'RegulatoryIntelligenceSubDomain', 'Compliance Intelligence', 'semantic', 'pursue', [], [], [],
      ['ontology', 'ssot', 'shacl', 'prov'], ['O079', 'O080', 'O184', 'O062'],
      why='Each obligation is linked to the process steps it governs, the control that meets it and the record that proves it, so an agency or auditor request becomes a query that returns an evidence pack with its provenance.'),
    P('S03', 'Pre-Payroll Rule Validation Service', 'RegulatoryIntelligenceSubDomain', 'Compliance Intelligence', 'semantic', 'pursue', [], ['adp'], ['adp-agents'],
      ['shacl', 'ssot', 'agents'], ['O004', 'O005', 'O022', 'O028', 'O003'],
      why='Every pay run is checked against minimum wage, overtime, break, final-pay and accrual rules for each employee’s jurisdiction before funds are released. ADP’s payroll agent audits variances; this checks against the rules themselves and cites them.'),
    P('S04', 'Worker Classification Decision Service', 'RegulatoryIntelligenceSubDomain', 'Compliance Intelligence', 'semantic', 'pursue', [], [], [],
      ['dq', 'ssot', 'prov'], ['O076'], why='Exempt and contractor tests differ by state. A decision model asks the decision questions, applies the rules and records the rationale.'),
    P('S05', 'Automated Employment Decision Compliance Service', 'RegulatoryIntelligenceSubDomain', 'Compliance Intelligence', 'semantic', 'pursue', [], [],
      ['illinois-ai', 'colorado-ai'], ['ssot', 'privacy', 'prov', 'measures'], ['O107', 'O127', 'O162'],
      why='Clients that use AI in hiring, pay or performance decisions now owe notices, adverse-action steps and records (Illinois from 2026, Colorado from 2027). The service inventories the client’s decision tools, issues the notices, measures disparate impact and keeps the records.'),
    P('S06', 'Pay Equity & Pay Transparency Compliance Service', 'RegulatoryIntelligenceSubDomain', 'Compliance Intelligence', 'semantic', 'pursue', [], [], [],
      ['ssot', 'measures', 'privacy'], ['O119', 'O123'], why='Pay transparency rules vary by state and city; pay gaps need job-related explanations. The rules register and the job architecture make both checkable.'),
    P('R01', 'Client Employer Risk Profile Service', 'EmployerRiskProfilingSubDomain', 'Risk Intelligence', 'semantic', 'pursue', [], [], [],
      ['ontology', 'measures', 'prov', 'c360'], ['O216', 'O221', 'O097', 'O038'],
      why='One profile per client, built from compliance posture, workers’ compensation class and claims, employment practices signals, turnover, tax history and benefits experience. Underwriting, pricing and the advisor use the same explained profile, and the client sees risks before they become costs.'),
    P('R02', 'Workers’ Compensation Class & Claims Risk Analytics Service', 'EmployerRiskProfilingSubDomain', 'Risk Intelligence', 'semantic', 'pursue', [], [], [],
      ['ontology', 'measures'], ['O090', 'O092', 'O093', 'O097'], why='Checks each employee’s class code against duties and predicts injury risk by worksite, feeding the safety survey.'),
    P('R03', 'Employment Practices Exposure Early Warning Service', 'EmployerRiskProfilingSubDomain', 'Risk Intelligence', 'semantic', 'pursue', [], [], [],
      ['dq', 'measures', 'privacy'], ['O083', 'O084', 'O089', 'O132'], why='Watches terminations, complaints, documentation gaps and rating patterns for exposure, within the privacy safeguards, and alerts the advisor.'),
    P('R04', 'Benefits Cost & Renewal Risk Forecast Service', 'EmployerRiskProfilingSubDomain', 'Risk Intelligence', 'semantic', 'pursue', [], [], [],
      ['measures', 'ontology'], ['O038', 'O040', 'O221'], why='Forecasts the client’s renewal from plan mix, demographics and claims trend, months before renewal.'),
    P('D01', 'Governed Decision Support Service', 'DecisionIntelligenceSubDomain', 'Decision Intelligence', 'semantic', 'pursue', [], [], [],
      ['dq', 'ssot', 'prov', 'agents'], ['O020', 'O081', 'O124', 'O212'],
      why='Decision models for recurring decisions (leave eligibility, discipline, offers, pay changes): the decision questions to answer, the rules that apply, a recommended course and the rationale recorded for later review.'),
    P('D02', 'Benefits Plan Design Optimizer Service', 'DecisionIntelligenceSubDomain', 'Decision Intelligence', 'semantic', 'pursue', [], [], [],
      ['measures', 'c360'], ['O036', 'O037', 'O054', 'O065'], why='Optimizes plan mix and contributions against budget, employee preferences and peer benchmarks; the same model helps employees choose a plan.'),
    P('D03', 'Total Cost of Employment Scenario Service', 'DecisionIntelligenceSubDomain', 'Decision Intelligence', 'semantic', 'pursue', ['MOD.05'], ['jw'], [],
      ['ontology', 'measures', 'apqc'], ['O032', 'O176', 'O196', 'O220'],
      why='Publishes the internal total cost of employment model to clients: the fully loaded cost of an employee, of a workforce change and of the PEO itself. It answers the price-transparency questions Justworks answers with a price list.'),
    P('D04', 'Workforce Benchmark Data Product', 'DecisionIntelligenceSubDomain', 'Decision Intelligence', 'semantic', 'pursue', [], [], [],
      ['privacy', 'measures', 'ontology'], ['O103', 'O117', 'O175'], why='Peer benchmarks for pay, turnover, benefits and safety across the client base, de-identified and aggregated under the existing thresholds.'),
    P('D05', 'Client Workforce Knowledge Graph Service', 'DecisionIntelligenceSubDomain', 'Decision Intelligence', 'semantic', 'pursue', [], [], [],
      ['ontology', 'shacl', 'privacy'], ['O171', 'O173', 'O178', 'O180'],
      why='A governed semantic layer over the client’s HR data and the business systems it connects to, so ad hoc questions get consistent answers and field mappings are validated, not guessed.'),
    P('A01', 'Grounded HR Policy & Pay Answer Agent Service', 'AgenticAssuranceSubDomain', 'Agentic Assurance', 'semantic', 'pursue', ['TEC.05'], ['adp', 'pay'], ['adp-agents'],
      ['agents', 'ssot', 'prov', 'measures'], ['O008', 'O082', 'O190', 'O212'],
      why='Answers employee and manager questions from the client’s own handbook, the jurisdiction’s rules and the employee’s pay data, citing the rule and version behind each answer. ADP launched an HR policy agent in 2026; the difference is grounding and measured accuracy.'),
    P('A02', 'Agent Accuracy Measurement & Calibration Service', 'AgenticAssuranceSubDomain', 'Agentic Assurance', 'semantic', 'pursue', [], [], [],
      ['measures', 'c360', 'prov'], ['O172', 'O212'],
      why='Metrology for agents: reference question sets drawn from the 250 customer questions, measured accuracy, groundedness and citation validity with uncertainty, drift tracking, and a measurement record for every agent release. It is what lets a client or a regulator trust an agent’s answer.'),
    P('A03', 'Agent Guardrail & Circuit-Breaker Service', 'AgenticAssuranceSubDomain', 'Agentic Assurance', 'semantic', 'pursue', [], [], [],
      ['agents', 'shacl', 'ssot', 'measures'], ['O003', 'O006', 'O214'],
      why='Every agent action passes the validation gate (shapes, then rules, then policy). When measured error rates cross a threshold the circuit breaker stops the agent and routes the work to a person.'),
    P('A04', 'Decision Provenance & Explainability Ledger Service', 'AgenticAssuranceSubDomain', 'Agentic Assurance', 'semantic', 'pursue', [], [], ['colorado-ai'],
      ['prov', 'ssot'], ['O080', 'O083', 'O124', 'O217'],
      why='A provenance record for every agent action and decision: inputs, rules and versions, model, reviewer and outcome. It meets the record-keeping duties of the new automated decision laws and lets a decision be explained or reversed.'),
    P('A05', 'Client AI and Agent Governance Service', 'AgenticAssuranceSubDomain', 'Agentic Assurance', 'semantic', 'pursue', [], [], ['illinois-ai', 'colorado-ai'],
      ['privacy', 'gateway', 'measures'], ['O161', 'O162', 'O164'],
      why='Helps clients inventory and govern their own AI tools that touch employee data: purpose, risk tier, notices, monitoring and measured performance, using the same gateway the PEO uses on itself.'),
]
