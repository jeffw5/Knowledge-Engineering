"""Customer 360 knowledge graph, release 0.2.0, for the KE Workbench.

The jobs-to-be-done model as a domain extension of the Baseline Core ontology:
client personas, functional, consumption-chain, emotional and social jobs, per-job job steps on the
universal job map, desired outcomes, plus the workflow classes the Customer 360 tools write at run time
(appreciative inquiry interviews, SME reviews and decisions, survey waves and scores) and the
requirements-gateway ontology (outcome requirements, gateway evaluations, demand items).

Standards: Semantic Governance v1.9 (Draft) Part III as encoded in assets/ke-rules.js
(lower-case hyphenated class and concept names, §3.11 asset headers).
Usage: python3 gen2.py <benchmark data.json> <out dir>"""
import json, re, os, sys, datetime, math

SRC, OUT = sys.argv[1], sys.argv[2]
D = json.load(open(SRC))
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
TODAY, STAMP = NOW.date().isoformat(), NOW.strftime('%Y-%m-%dT%H:%M:%SZ')
VER = "0.2.0"
AUTHOR = "Jeffrey Wallk"
BASE = "https://www.insperity.com/"
PUBLISHER = BASE + "resource/core/Organization/insperity"
CONFORMS = BASE + "standard/semantic-governance/1.9/"
BFO = "http://purl.obolibrary.org/obo/bfo/2020/bfo.owl"
SUBJECT = BASE + "taxonomy/core-domain/EnterpriseArchitecture"

NS = {
    "jtbd": BASE + "ontology/jobs-to-be-done/",
    "rg": BASE + "ontology/requirements-gateway/",
    "ob": BASE + "resource/outcome-benchmark/",
    "core": BASE + "ontology/core/",
    "jobvoc": BASE + "vocabulary/core-job/",
    "personavoc": BASE + "vocabulary/core-persona/",
    "processvoc": BASE + "vocabulary/core-process/",
    "requirementsvoc": BASE + "vocabulary/core-requirements/",
    "measurevoc": BASE + "vocabulary/core-measure/",
    "decisionvoc": BASE + "vocabulary/core-decision/",
    "theme": BASE + "vocabulary/benchmark-theme/",
    "metric": BASE + "vocabulary/outcome-metric-type/",
    "verdict": BASE + "vocabulary/review-verdict/",
    "flag": BASE + "vocabulary/review-flag/",
    "use": BASE + "vocabulary/approved-use/",
    "result": BASE + "vocabulary/review-decision-result/",
    "segment": BASE + "vocabulary/survey-segment/",
    "action": BASE + "vocabulary/outcome-action/",
    "phase": BASE + "vocabulary/inquiry-phase/",
    "check": BASE + "vocabulary/gateway-check/",
    "demand": BASE + "vocabulary/demand-status/",
    "hr": "http://example.org/hrservices/ddd#",
    "obo": "http://purl.obolibrary.org/obo/",
    "prov": "http://www.w3.org/ns/prov#",
}
GRAPH_BASE = BASE + "graph/outcome-benchmark/"
GRAPHS = {   # file → (graph, title)
    "00-jobs-to-be-done-ontology.ttl": (GRAPH_BASE + "ontology", "Jobs-to-be-done ontology"),
    "01-requirements-gateway-ontology.ttl": (GRAPH_BASE + "requirements-gateway-ontology", "Requirements gateway ontology"),
    "02-customer-360-vocabularies.ttl": (GRAPH_BASE + "vocabularies", "Customer 360 vocabularies"),
    "03-job-map-stages.ttl": (GRAPH_BASE + "job-map-stages", "Job map stages"),
    "04-client-personas.ttl": (GRAPH_BASE + "client-personas", "Client personas with emotional and social jobs"),
    "05-jobs-and-job-steps.ttl": (GRAPH_BASE + "jobs", "Functional jobs and their job steps"),
    "06-desired-outcomes.ttl": (GRAPH_BASE + "desired-outcomes", "Desired outcomes"),
    "07-service-traceability.ttl": (GRAPH_BASE + "service-traceability", "Traceability to the business model"),
    "08-survey-wave-example.ttl": (GRAPH_BASE + "survey-wave/example", "Example survey wave (generated scores)"),
}

PREFIXES = "".join(f"@prefix {k + ':':<17}<{v}> .\n" for k, v in {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#", "xsd": "http://www.w3.org/2001/XMLSchema#",
    "skos": "http://www.w3.org/2004/02/skos/core#", "dct": "http://purl.org/dc/terms/",
    "vaem": "http://www.linkedmodel.org/schema/vaem#", "vann": "http://purl.org/vocab/vann/", **NS}.items())

# ---------------------------------------------------------------- acronyms (§3.2)
ACR = [("FMLA", "Family and Medical Leave Act"), ("COBRA", "Consolidated Omnibus Budget Reconciliation Act"),
       ("OSHA", "Occupational Safety and Health Administration"), ("EEOC", "Equal Employment Opportunity Commission"),
       ("FCRA", "Fair Credit Reporting Act"), ("FSA", "flexible spending account"), ("HSA", "health savings account"),
       ("IRS", "Internal Revenue Service"), ("CPEO", "certified professional employer organization"),
       ("PEO", "professional employer organization"), ("CEO", "Chief Executive Officer"),
       ("IT", "Information Technology"), ("HR", "human resources")]
def expand(s):
    for a, full in ACR:
        s = re.sub(r"\b" + a + r"\b", full, s)
    return s.replace(" & ", " and ")

def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
def lit(s, lang="en"): return f'"{esc(s)}"@{lang}' if lang else f'"{esc(s)}"'
def plain(s): return f'"{esc(str(s))}"'
def dec(v): return f'"{v}"^^xsd:decimal'
def intl(v): return f'"{int(v)}"^^xsd:integer'
def lc_first(s): return s[0].lower() + s[1:]
def sentence(s):
    w = s.split(" ")
    return " ".join([w[0]] + [x if (len(re.sub('[^A-Za-z]', '', x)) > 1 and re.sub('[^A-Za-z]', '', x).isupper()) else x.lower() for x in w[1:]])

def block(subject, types, lines):
    body = "\n".join(l for l in lines if l).rstrip(" ;")
    return f"{subject}\n  a {', '.join(types)} ;\n{body} .\n"

def labels(text, alts=()):
    pref = expand(text)
    out = [f"  rdfs:label {lit(pref)} ;", f"  skos:prefLabel {lit(pref)} ;"]
    for a in dict.fromkeys(([text] if text != pref else []) + [x for x in alts if x]):
        if a != pref: out.append(f"  skos:altLabel {lit(a)} ;")
    return out

def stamp(status="Draft"):
    return [f"  core:hasLifecycleStatus core:{status} ;", f'  dct:created "{TODAY}"^^xsd:date ;',
            f'  dct:modified "{STAMP}"^^xsd:dateTime ;']

def header_lines(iri_ns, prefix, title, description, kind, change):
    """§3.11 asset header (ontology or concept scheme)."""
    out = [f"  rdfs:label {lit(title)} ;", f"  skos:prefLabel {lit(title)} ;", f"  dct:title {lit(title)} ;",
           f"  dct:description {lit(description)} ;", f"  dct:subject <{SUBJECT}> ;",
           f'  vaem:namespace "{iri_ns}"^^xsd:anyURI ;', f'  vann:preferredNamespacePrefix "{prefix}" ;',
           '  dct:language "en" ;', f"  dct:publisher <{PUBLISHER}> ;", f"  dct:conformsTo <{CONFORMS}> ;"]
    if kind == "ontology": out.append(f"  dct:conformsTo <{BFO}> ;")
    out += [f"  skos:changeNote {lit(change)} ;", f'  owl:versionInfo "{VER}" ;', f"  owl:versionIRI <{iri_ns}{VER}/> ;",
            "  core:hasLifecycleStatus core:Draft ;", f'  dct:creator "{AUTHOR}" ;',
            f'  dct:created "{TODAY}"^^xsd:date ;', f'  dct:modified "{STAMP}"^^xsd:dateTime ;']
    return out

def file_header(fname, what):
    g, title = GRAPHS[fname]
    return (f"# {title}\n# Named graph: {g}  ·  Customer 360 release {VER}  ·  Draft\n# {what}\n"
            f"# Generated {STAMP} by gen_customer360.py · Standards: Semantic Governance v1.9 (Draft), Part III\n\n"
            + PREFIXES + "\n")

FILES = {}
def write(fname, text):
    FILES[fname] = text
    open(os.path.join(OUT, fname), "w").write(text)

# ================================================================ 00 jobs-to-be-done ontology
J_ONT = f"<{NS['jtbd']}>"
def cls(prefix, ont, name, label, definition, parents, primary=None, extra=()):
    return block(f"{prefix}:{name}", ["owl:Class"], [
        f"  rdfs:label {lit(label)} ;", f"  skos:prefLabel {lit(label)} ;", f"  skos:definition {lit(definition)} ;",
        "  rdfs:subClassOf " + ", ".join(parents) + " ;", f"  rdfs:isDefinedBy {ont} ;",
        f"  core:hasPrimaryTerm {primary} ;" if primary else "", *extra, *stamp()])
def prop(prefix, ont, kind, name, label, definition, dom, rng, extra=()):
    return block(f"{prefix}:{name}", [kind], [
        f"  rdfs:label {lit(label)} ;", f"  skos:prefLabel {lit(label)} ;", f"  skos:definition {lit(definition)} ;",
        f"  rdfs:domain {dom} ;", f"  rdfs:range {rng} ;", f"  rdfs:isDefinedBy {ont} ;", *extra, *stamp()])
OP, DP = "owl:ObjectProperty", "owl:DatatypeProperty"
GDC, PROC, ENT = "obo:BFO_0000031", "obo:BFO_0000015", "obo:BFO_0000001"
def jc(*a, **k): return cls("jtbd", J_ONT, *a, **k)
def jp(*a, **k): return prop("jtbd", J_ONT, *a, **k)

t = [file_header("00-jobs-to-be-done-ontology.ttl", "Load first. Domain extension of the core ontology for the Customer 360 tools."),
     block(J_ONT, ["owl:Ontology"], header_lines(NS["jtbd"], "jtbd", "Jobs-to-be-done ontology",
        "A domain ontology that extends the core persona, job, job step and desired outcome classes for outcome-driven research: "
        "client personas and their functional, consumption-chain, emotional and social jobs, the universal job map, "
        "appreciative inquiry interviews that discover them, subject-matter expert reviews and decisions, and the survey waves that score each desired outcome.",
        "ontology", f"{VER} ({TODAY}): realigned as an extension of the core ontology (persona, job, job step, desired outcome, measure, decision); "
        "lower-case hyphenated class names; job steps are per job, the eight universal steps become job map stages; adds interviews, reviews, decisions, survey waves and scores.")
        + [f"  owl:imports <{NS['core']}> ;"]),
     "# ---- Classes ----------------------------------------------------------\n",
     jc("client-persona", "Client persona", "A persona that describes a role at or within a client company that executes, or takes part in, jobs a human resources partner helps get done.", ["core:persona"], "personavoc:persona"),
     jc("job-to-be-done", "Job to be done", "A job that a client persona is trying to get done, stated without naming the product or service that might help.", ["core:job"], "jobvoc:job"),
     jc("core-functional-job", "Core functional job", "A job to be done that is a main functional task the client hires a human resources partner to help with.", ["jtbd:job-to-be-done"]),
     jc("consumption-chain-job", "Consumption chain job", "A job to be done that the client carries out to choose, adopt, use or renew the provider relationship itself.", ["jtbd:job-to-be-done"]),
     jc("emotional-job", "Emotional job", "A job to be done that states how the job executor wants to feel while getting functional jobs done.", ["jtbd:job-to-be-done"], "jobvoc:emotional"),
     jc("social-job", "Social job", "A job to be done that states how the job executor wants to be seen by others while getting functional jobs done.", ["jtbd:job-to-be-done"]),
     jc("job-step", "Job step", "A job step that is one stage of one job to be done, placed on the universal job map.", ["core:job-step"], "processvoc:step"),
     jc("job-map-stage", "Job map stage", "A generically dependent continuant that names one of the eight universal stages every job passes through, from define to conclude.", [GDC]),
     jc("desired-outcome", "Desired outcome", "A desired outcome that a client persona uses to judge success at a job step, written as direction, metric, object of control and contextual clarifier.", ["core:desired-outcome"], "jobvoc:desired-outcome"),
     jc("appreciative-inquiry-interview", "Appreciative inquiry interview", "A process in which an interviewer asks a client persona what works at its best, what it hopes for and what it needs, to discover jobs, job steps and desired outcomes.", [PROC]),
     jc("interview-note", "Interview note", "A generically dependent continuant that records one observation or quote from an appreciative inquiry interview, tagged with its inquiry phase.", [GDC]),
     jc("subject-matter-review", "Subject-matter review", "A process in which one business or compliance subject-matter expert judges the wording, placement and permitted uses of a persona, job or desired outcome.", [PROC]),
     jc("review-decision", "Review decision", "A decision that accepts or drops a persona, job or desired outcome after its subject-matter reviews, with its final wording and approved uses.", ["core:decision"], "decisionvoc:decision"),
     jc("survey-wave", "Survey wave", "A process in which the outcome benchmark survey is fielded once and its importance and satisfaction ratings are collected.", [PROC]),
     jc("outcome-score", "Outcome score", "A measure that states the importance and satisfaction one survey segment gave a desired outcome in one survey wave.", ["core:measure"], "measurevoc:measure"),
     "[] a owl:AllDisjointClasses ;\n  owl:members ( jtbd:core-functional-job jtbd:consumption-chain-job jtbd:emotional-job jtbd:social-job ) .\n",
     "# ---- Object properties --------------------------------------------------\n",
     jp(OP, "executesJob", "executes job", "A relation between a client persona and a job its typical executor is responsible for getting done.", "jtbd:client-persona", "jtbd:job-to-be-done", ["  rdfs:subPropertyOf core:performsJob ;", "  owl:inverseOf jtbd:hasJobExecutor ;"]),
     jp(OP, "hasJobExecutor", "has job executor", "A relation between a job and a client persona responsible for getting it done.", "jtbd:job-to-be-done", "jtbd:client-persona"),
     jp(OP, "participatesInJob", "participates in job", "A relation between a client persona and a job it takes part in without being responsible for it.", "jtbd:client-persona", "jtbd:job-to-be-done", ["  owl:inverseOf jtbd:hasJobParticipant ;"]),
     jp(OP, "hasJobParticipant", "has job participant", "A relation between a job and a client persona that takes part in it without being responsible for it.", "jtbd:job-to-be-done", "jtbd:client-persona"),
     jp(OP, "atJobMapStage", "at job map stage", "A relation between a job step or desired outcome and the universal job map stage it belongs to.", ENT, "jtbd:job-map-stage"),
     jp(OP, "isOutcomeOfJob", "is outcome of job", "A relation between a desired outcome and the job whose success it measures, through its job step.", "jtbd:desired-outcome", "jtbd:job-to-be-done", ["  owl:inverseOf jtbd:hasDesiredOutcome ;"]),
     jp(OP, "hasDesiredOutcome", "has desired outcome", "A relation between a job and a desired outcome mapped to one of its job steps.", "jtbd:job-to-be-done", "jtbd:desired-outcome"),
     jp(OP, "hasOutcomeMetricType", "has outcome metric type", "A relation between a desired outcome and the kind of measure it uses, such as speed or stability.", "jtbd:desired-outcome", "skos:Concept"),
     jp(OP, "hasBenchmarkTheme", "has benchmark theme", "A relation between a desired outcome and the service-line theme under which its results are reported and acted on.", "jtbd:desired-outcome", "skos:Concept"),
     jp(OP, "isAddressedByService", "is addressed by service", "A relation between a desired outcome and a domain service of the business model that helps the client achieve it.", "jtbd:desired-outcome", "owl:Thing"),
     jp(OP, "appliesToBusinessDomain", "applies to business domain", "A relation between a job and a business domain of the business model whose services support it.", "jtbd:job-to-be-done", "owl:Thing"),
     jp(OP, "interviewsPersona", "interviews persona", "A relation between an appreciative inquiry interview and the client persona the interviewee represents.", "jtbd:appreciative-inquiry-interview", "jtbd:client-persona"),
     jp(OP, "isNoteOf", "is note of", "A relation between an interview note and the appreciative inquiry interview it was taken in.", "jtbd:interview-note", "jtbd:appreciative-inquiry-interview"),
     jp(OP, "inInquiryPhase", "in inquiry phase", "A relation between an interview note and the phase of the appreciative inquiry cycle it belongs to.", "jtbd:interview-note", "skos:Concept"),
     jp(OP, "isEvidencedBy", "is evidenced by", "A relation between a job, job step or desired outcome and the interview or interview note it was discovered in.", ENT, ENT, ["  rdfs:subPropertyOf prov:wasDerivedFrom ;"]),
     jp(OP, "reviewsElement", "reviews element", "A relation between a subject-matter review and the persona, job or desired outcome it judges.", "jtbd:subject-matter-review", ENT),
     jp(OP, "hasReviewVerdict", "has review verdict", "A relation between a subject-matter review and the verdict the reviewer gave.", "jtbd:subject-matter-review", "skos:Concept"),
     jp(OP, "raisesFlag", "raises flag", "A relation between a subject-matter review and a compliance risk the reviewer flagged.", "jtbd:subject-matter-review", "skos:Concept"),
     jp(OP, "approvesUse", "approves use", "A relation between a review or decision and a purpose for which the statement may be used.", ENT, "skos:Concept"),
     jp(OP, "hasSuggestedStage", "has suggested stage", "A relation between a business review and the job map stage the reviewer would move the outcome to.", "jtbd:subject-matter-review", "jtbd:job-map-stage"),
     jp(OP, "hasSuggestedTheme", "has suggested theme", "A relation between a business review and the benchmark theme the reviewer would report the outcome under.", "jtbd:subject-matter-review", "skos:Concept"),
     jp(OP, "decidesElement", "decides element", "A relation between a review decision and the persona, job or desired outcome it accepts or drops.", "jtbd:review-decision", ENT),
     jp(OP, "hasDecisionResult", "has decision result", "A relation between a review decision and its result, accepted or dropped.", "jtbd:review-decision", "skos:Concept"),
     jp(OP, "inSurveyWave", "in survey wave", "A relation between an outcome score and the survey wave whose ratings it summarizes.", "jtbd:outcome-score", "jtbd:survey-wave"),
     jp(OP, "hasSurveySegment", "has survey segment", "A relation between an outcome score and the group of respondents it summarizes.", "jtbd:outcome-score", "skos:Concept"),
     "# ---- Data properties ----------------------------------------------------\n",
     jp(DP, "hasIdentifier", "has identifier", "A data property that gives the stable benchmark identifier of an element, such as J01 or O001.", ENT, "xsd:string"),
     jp(DP, "hasShortName", "has short name", "A data property that gives the short name used for an element in charts and survey module names.", ENT, "xsd:string"),
     jp(DP, "hasJobStatement", "has job statement", "A data property that gives the solution-agnostic wording of a job as used in the survey.", "jtbd:job-to-be-done", "xsd:string"),
     jp(DP, "hasOutcomeStatement", "has outcome statement", "A data property that gives the exact survey wording of a desired outcome, acronyms included.", "jtbd:desired-outcome", "xsd:string"),
     jp(DP, "hasImportanceQuestion", "has importance question", "A data property that gives the survey question asking how important a desired outcome is to the respondent.", "jtbd:desired-outcome", "xsd:string"),
     jp(DP, "hasSatisfactionQuestion", "has satisfaction question", "A data property that gives the survey question asking how satisfied the respondent is with achieving a desired outcome today.", "jtbd:desired-outcome", "xsd:string"),
     jp(DP, "hasStageOrder", "has stage order", "A data property that gives the position of a job map stage or job step on the job map, starting at one.", ENT, "xsd:positiveInteger"),
     jp(DP, "hasTypicalTitles", "has typical titles", "A data property that lists job titles commonly held by people who fit a client persona.", "jtbd:client-persona", "xsd:string"),
     jp(DP, "hasPersonaContext", "has persona context", "A data property that describes the working situation a client persona is in.", "jtbd:client-persona", "xsd:string"),
     jp(DP, "hasBuyingRole", "has buying role", "A data property that describes the part a client persona plays in choosing and keeping the provider.", "jtbd:client-persona", "xsd:string"),
     jp(DP, "hasPersonaGoal", "has persona goal", "A data property that states the overall goal a client persona is pursuing at work.", "jtbd:client-persona", "xsd:string"),
     jp(DP, "hasSurveyTarget", "has survey target", "A data property that gives the number of respondents the benchmark survey aims to reach for a client persona.", "jtbd:client-persona", "xsd:integer"),
     jp(DP, "hasInterviewDate", "has interview date", "A data property that gives the date an appreciative inquiry interview took place.", "jtbd:appreciative-inquiry-interview", "xsd:date"),
     jp(DP, "hasInterviewerName", "has interviewer name", "A data property that names the person who conducted an appreciative inquiry interview.", "jtbd:appreciative-inquiry-interview", "xsd:string"),
     jp(DP, "hasIntervieweeRole", "has interviewee role", "A data property that gives the job title of the interviewee, never the interviewee's name.", "jtbd:appreciative-inquiry-interview", "xsd:string"),
     jp(DP, "hasCompanySizeBand", "has company size band", "A data property that gives the employee-count band of the interviewee's company.", "jtbd:appreciative-inquiry-interview", "xsd:string"),
     jp(DP, "hasIndustry", "has industry", "A data property that gives the industry of the interviewee's company.", "jtbd:appreciative-inquiry-interview", "xsd:string"),
     jp(DP, "hasCurrentServiceModel", "has current service model", "A data property that describes how the interviewee's company handles human resources today.", "jtbd:appreciative-inquiry-interview", "xsd:string"),
     jp(DP, "hasInterviewSummary", "has interview summary", "A data property that gives the interviewer's short summary of what the interview revealed.", "jtbd:appreciative-inquiry-interview", "xsd:string"),
     jp(DP, "hasNoteText", "has note text", "A data property that gives the text of an interview note.", "jtbd:interview-note", "xsd:string"),
     jp(DP, "isQuote", "is quote", "A data property that is true when an interview note records the interviewee's own words.", "jtbd:interview-note", "xsd:boolean"),
     jp(DP, "hasReviewerName", "has reviewer name", "A data property that names the person who carried out a review or recorded a decision.", ENT, "xsd:string"),
     jp(DP, "hasReviewerRole", "has reviewer role", "A data property that gives the role a reviewer acted in, business or compliance.", "jtbd:subject-matter-review", "xsd:string"),
     jp(DP, "hasSuggestedWording", "has suggested wording", "A data property that gives the wording a reviewer or decision proposes for the statement.", ENT, "xsd:string"),
     jp(DP, "hasStudyRecommendation", "has study recommendation", "A data property that records whether a business reviewer would keep, merge or drop an outcome from the study.", "jtbd:subject-matter-review", "xsd:string"),
     jp(DP, "hasDuplicateOf", "has duplicate of", "A data property that lists the identifiers of outcomes a reviewer considers duplicates of this one.", "jtbd:subject-matter-review", "xsd:string"),
     jp(DP, "hasReviewComment", "has review comment", "A data property that gives a reviewer's or decision maker's explanation.", ENT, "xsd:string"),
     jp(DP, "hasRecordedAt", "has recorded at", "A data property that gives the moment a review, decision or evaluation was recorded.", ENT, "xsd:dateTime"),
     jp(DP, "hasWaveLabel", "has wave label", "A data property that gives the name of a survey wave as shown in the tools.", "jtbd:survey-wave", "xsd:string"),
     jp(DP, "hasFieldedDate", "has fielded date", "A data property that gives the date a survey wave closed.", "jtbd:survey-wave", "xsd:date"),
     jp(DP, "hasSourceFileName", "has source file name", "A data property that names the results file a survey wave was loaded from.", "jtbd:survey-wave", "xsd:string"),
     jp(DP, "isExampleData", "is example data", "A data property that is true when a survey wave holds generated example scores rather than survey results.", "jtbd:survey-wave", "xsd:boolean"),
     jp(DP, "hasImportanceScore", "has importance score", "A data property that gives the share of respondents rating an outcome important (4 or 5 of 5), divided by ten.", "jtbd:outcome-score", "xsd:decimal"),
     jp(DP, "hasSatisfactionScore", "has satisfaction score", "A data property that gives the share of respondents satisfied (4 or 5 of 5) with an outcome, divided by ten.", "jtbd:outcome-score", "xsd:decimal"),
     jp(DP, "hasRespondentCount", "has respondent count", "A data property that gives the number of respondents behind an outcome score.", "jtbd:outcome-score", "xsd:integer"),
     ]
write("00-jobs-to-be-done-ontology.ttl", "\n".join(t))

# ================================================================ 01 requirements gateway ontology
R_ONT = f"<{NS['rg']}>"
def rc(*a, **k): return cls("rg", R_ONT, *a, **k)
def rp(*a, **k): return prop("rg", R_ONT, *a, **k)
t = [file_header("01-requirements-gateway-ontology.ttl", "The hand-off from measured outcomes into demand planning."),
     block(R_ONT, ["owl:Ontology"], header_lines(NS["rg"], "rg", "Requirements gateway ontology",
        "A domain ontology for the requirements engineering semantic gateway: requirements derived from the measured gap on a desired outcome, "
        "the gateway evaluation that admits or holds each requirement against its admission checks, and the demand items it hands to demand planning, "
        "traced back to persona, job, job step, desired outcome and survey wave and forward to the wave that re-measures them.",
        "ontology", f"{VER} ({TODAY}): first release, for the Customer 360 Requirements Gateway tool.")
        + [f"  owl:imports <{NS['core']}>, <{NS['jtbd']}> ;"]),
     rc("outcome-requirement", "Outcome requirement", "A requirement that states the change a product or service must make so that clients better achieve one desired outcome.", ["core:requirement"], "requirementsvoc:requirement"),
     rc("gateway-evaluation", "Gateway evaluation", "A decision in which the requirements gateway checks an outcome requirement against its admission checks before it reaches demand planning.", ["core:decision"], "decisionvoc:decision"),
     rc("demand-item", "Demand item", "A generically dependent continuant that records a requested investment in demand planning, with its priority, status and the opportunity it is expected to close.", [GDC]),
     rp(OP, "tracesToOutcome", "traces to outcome", "A relation between an outcome requirement and the desired outcome whose gap it addresses.", "rg:outcome-requirement", "jtbd:desired-outcome"),
     rp(OP, "hasRecommendedAction", "has recommended action", "A relation between an outcome requirement and the kind of work the measured gap calls for: fix, innovate, protect or simplify.", "rg:outcome-requirement", "skos:Concept"),
     rp(OP, "basedOnSurveyWave", "based on survey wave", "A relation between an outcome requirement and the survey wave whose scores justify it.", "rg:outcome-requirement", "jtbd:survey-wave"),
     rp(OP, "isOwnedByTheme", "is owned by theme", "A relation between an outcome requirement and the service-line theme accountable for it.", "rg:outcome-requirement", "skos:Concept"),
     rp(OP, "isAllocatedToService", "is allocated to service", "A relation between an outcome requirement and a domain service expected to deliver the change.", "rg:outcome-requirement", "owl:Thing"),
     rp(OP, "evaluatesRequirement", "evaluates requirement", "A relation between a gateway evaluation and the outcome requirement it checks.", "rg:gateway-evaluation", "rg:outcome-requirement"),
     rp(OP, "passesCheck", "passes check", "A relation between a gateway evaluation and an admission check the requirement met.", "rg:gateway-evaluation", "skos:Concept"),
     rp(OP, "failsCheck", "fails check", "A relation between a gateway evaluation and an admission check the requirement did not meet.", "rg:gateway-evaluation", "skos:Concept"),
     rp(OP, "realizesRequirement", "realizes requirement", "A relation between a demand item and the admitted outcome requirement it asks demand planning to fund.", "rg:demand-item", "rg:outcome-requirement"),
     rp(OP, "hasDemandStatus", "has demand status", "A relation between a demand item and its current status in demand planning.", "rg:demand-item", "skos:Concept"),
     rp(OP, "isRemeasuredIn", "is remeasured in", "A relation between a demand item and the later survey wave that measures whether the gap closed.", "rg:demand-item", "jtbd:survey-wave"),
     rp(DP, "hasRequirementStatement", "has requirement statement", "A data property that gives the wording of an outcome requirement.", "rg:outcome-requirement", "xsd:string"),
     rp(DP, "hasAcceptanceCriterion", "has acceptance criterion", "A data property that states how the next survey wave will show the requirement was met.", "rg:outcome-requirement", "xsd:string"),
     rp(DP, "hasOpportunityScore", "has opportunity score", "A data property that gives the opportunity score, from zero to twenty, that justified a requirement or demand item.", ENT, "xsd:decimal"),
     rp(DP, "hasGapToNonClients", "has gap to non-clients", "A data property that gives the opportunity for clients minus the opportunity for employers without a provider, with its sign.", "rg:outcome-requirement", "xsd:decimal"),
     rp(DP, "isAdmitted", "is admitted", "A data property that is true when a gateway evaluation admits the requirement to demand planning.", "rg:gateway-evaluation", "xsd:boolean"),
     rp(DP, "hasPriorityRank", "has priority rank", "A data property that gives the rank of a demand item in the demand planning queue, one being highest.", "rg:demand-item", "xsd:integer"),
     rp(DP, "hasExpectedOpportunityClosed", "has expected opportunity closed", "A data property that gives the opportunity a demand item is expected to remove if it is delivered.", "rg:demand-item", "xsd:decimal"),
     rp(DP, "hasDemandNote", "has demand note", "A data property that records a demand planner's note on a demand item.", "rg:demand-item", "xsd:string"),
     ]
write("01-requirements-gateway-ontology.ttl", "\n".join(t))

# ================================================================ 02 vocabularies
THEME_DEF = {th["name"]: th.get("desc", "") for th in D["themes"]}
THEMES = {   # benchmark name -> (local, label, alts)
    "Payroll": ("payroll", "Payroll", []), "Benefits": ("benefits", "Benefits", []),
    "HR Compliance": ("human-resources-compliance", "Human resources compliance", ["HR compliance"]),
    "Talent Management": ("talent-management", "Talent management", []),
    "Training": ("training", "Training", []), "Coaching": ("coaching", "Coaching", []),
    "Monitoring": ("monitoring", "Monitoring", []), "Measurement": ("measurement", "Measurement", []),
    "Values Stewardship": ("values-stewardship", "Values stewardship", []),
    "PEO Relationship": ("professional-employer-organization-relationship", "Professional employer organization relationship", ["PEO relationship"]),
    "HR Technology & Data": ("human-resources-technology-and-data", "Human resources technology and data", ["HR technology and data"]),
}
METRIC = {"Speed": ("speed", "Speed", "An outcome metric type that measures the time required to complete part of a job."),
          "Stability": ("stability", "Stability", "An outcome metric type that measures the likelihood that part of a job goes wrong or goes right."),
          "Cost & exposure": ("cost-and-exposure", "Cost and exposure", "An outcome metric type that measures the money spent or the liability carried in getting a job done."),
          "Effort": ("effort", "Effort", "An outcome metric type that measures the work or administrative burden a job places on its executor."),
          "Output": ("output", "Output", "An outcome metric type that measures a count or rate produced while getting a job done.")}
VOCABS = [  # prefix, title, description, terms [(local, label, definition, alts, notation)]
    ("theme", "Benchmark theme vocabulary", "A controlled vocabulary of the service-line themes under which outcome benchmark results are reported and acted on: the business model's nine core service lines plus two themes the benchmark adds.",
     [(v[0], v[1], "A benchmark theme covering " + re.sub(r'\.\s+(\w)', lambda m: '; ' + m.group(1).lower(), lc_first(expand(THEME_DEF.get(k) or k)).rstrip('.')) + ".", v[2] + ([k] if k != v[1] and k not in v[2] else []), None) for k, v in THEMES.items()]),
    ("metric", "Outcome metric type vocabulary", "A controlled vocabulary of the kinds of measure a desired outcome statement uses.",
     [(v[0], v[1], v[2], [k] if k != v[1] else [], None) for k, v in METRIC.items()]),
    ("verdict", "Review verdict vocabulary", "A controlled vocabulary of the verdicts a subject-matter expert gives a persona, job or desired outcome in review.",
     [("approve", "Approve", "A review verdict that accepts the statement as written.", [], "approve"),
      ("approve-with-edits", "Approve with edits", "A review verdict that accepts the statement once the suggested wording is applied.", [], "edits"),
      ("needs-discussion", "Needs discussion", "A review verdict that holds the statement until the reviewers resolve a question together.", [], "discuss"),
      ("reject", "Reject", "A review verdict that recommends the statement is not used.", [], "reject")]),
    ("flag", "Review flag vocabulary", "A controlled vocabulary of the compliance risks a reviewer can flag on a statement.",
     [("regulated-topic", "Regulated topic", "A review flag that marks a statement touching insurance, benefits or other licensed advice.", [], "regulated"),
      ("legal-advice", "Could read as legal advice", "A review flag that marks a statement a reader could take as legal advice.", [], "legal"),
      ("tax-advice", "Could read as tax advice", "A review flag that marks a statement a reader could take as tax advice.", [], "tax"),
      ("privacy-sensitivity", "Privacy or employee-data sensitivity", "A review flag that marks a statement involving employee personal data or monitoring.", [], "privacy"),
      ("needs-substantiation", "Claim needs substantiation", "A review flag that marks a statement implying a claim that needs evidence before use.", [], "substantiate"),
      ("bias-risk", "Bias or discrimination risk", "A review flag that marks a statement that could encourage biased or discriminatory practice.", [], "bias"),
      ("co-employment-unclear", "Co-employment responsibility unclear", "A review flag that marks a statement where it is unclear whether the client or the provider is responsible.", [], "coemploy")]),
    ("use", "Approved use vocabulary", "A controlled vocabulary of the purposes compliance can approve a statement for.",
     [("survey-instrument", "Survey instrument", "An approved use that allows the statement in the benchmark survey.", [], "survey"),
      ("internal-sales-guidance", "Internal sales guidance and agent", "An approved use that allows the statement in internal sales guidance and the sales advisory agent.", [], "sales"),
      ("external-marketing-claims", "External marketing claims", "An approved use that allows the statement in material that leaves the company.", [], "marketing")]),
    ("result", "Review decision result vocabulary", "A controlled vocabulary of the results a review decision can record.",
     [("accepted", "Accepted", "A review decision result that admits the statement into the governed model.", [], "accepted"),
      ("dropped", "Dropped", "A review decision result that removes the statement from the study and the tools.", [], "dropped")]),
    ("segment", "Survey segment vocabulary", "A controlled vocabulary of the respondent groups the benchmark survey reports separately.",
     [("provider-clients", "Clients of a professional employer organization", "A survey segment of employers that use a professional employer organization today.", ["PEO clients"], "A"),
      ("non-clients", "Employers without a professional employer organization", "A survey segment of employers that run human resources without a professional employer organization.", ["Non-PEO employers"], "P"),
      ("total-market", "Total market", "A survey segment of every respondent, clients and non-clients together.", [], "T")]),
    ("action", "Outcome action vocabulary", "A controlled vocabulary of the kinds of work a measured outcome gap calls for.",
     [("fix", "Fix", "An outcome action for an outcome on which clients are under-served and significantly worse off than employers without a provider.", [], "fix"),
      ("innovate", "Innovate", "An outcome action for an outcome on which both clients and non-clients are under-served.", [], "inn"),
      ("protect", "Protect and market", "An outcome action for an outcome on which non-clients are under-served and clients are significantly better served.", [], "pro"),
      ("simplify", "Simplify", "An outcome action for an outcome on which clients are more satisfied than they rate it important.", [], "sim"),
      ("maintain", "Maintain", "An outcome action for an outcome that needs no change.", [], "keep")]),
    ("phase", "Inquiry phase vocabulary", "A controlled vocabulary of the four phases of the appreciative inquiry cycle used to structure persona interviews.",
     [("discover", "Discover", "An inquiry phase in which the interviewee describes what works at its best and the moments it is proud of.", [], "1"),
      ("dream", "Dream", "An inquiry phase in which the interviewee describes what the job would look like if it went perfectly.", [], "2"),
      ("design", "Design", "An inquiry phase in which the interviewee describes what would need to be true, step by step, to get there.", [], "3"),
      ("destiny", "Destiny", "An inquiry phase in which the interviewee describes how they would know it worked and what they would measure.", [], "4")]),
    ("check", "Gateway check vocabulary", "A controlled vocabulary of the admission checks the requirements gateway applies before a requirement reaches demand planning.",
     [("review-accepted", "Review accepted", "A gateway check that the desired outcome was accepted in subject-matter review.", [], "accepted"),
      ("use-approved", "Use approved", "A gateway check that compliance approved the outcome for at least internal sales guidance.", [], "use"),
      ("measured", "Measured", "A gateway check that the outcome has scores for both survey segments in the chosen wave.", [], "measured"),
      ("privacy-threshold", "Privacy threshold", "A gateway check that every reported segment has at least five respondents.", [], "k5"),
      ("material-opportunity", "Material opportunity", "A gateway check that the opportunity for the targeted segment is at least twelve, or the gap is statistically significant.", [], "material"),
      ("owner-assigned", "Owner assigned", "A gateway check that the outcome has a theme and at least one service accountable for it.", [], "owner"),
      ("flags-resolved", "Compliance flags resolved", "A gateway check that every compliance flag raised in review is answered in the decision note.", [], "flags"),
      ("not-duplicate", "Not a duplicate", "A gateway check that no open demand item already traces to the same outcome.", [], "dup")]),
    ("demand", "Demand status vocabulary", "A controlled vocabulary of the statuses a demand item moves through in demand planning, ending with re-measurement in a later survey wave.",
     [("submitted", "Submitted", "A demand status for an item the gateway has handed to demand planning.", [], "1"),
      ("triaged", "Triaged", "A demand status for an item demand planning has sized and prioritized.", [], "2"),
      ("planned", "Planned", "A demand status for an item funded in a planning increment.", [], "3"),
      ("in-delivery", "In delivery", "A demand status for an item a delivery team is working on.", [], "4"),
      ("delivered", "Delivered", "A demand status for an item whose change is live for clients.", [], "5"),
      ("remeasured", "Remeasured", "A demand status for an item whose outcome a later survey wave has scored again.", [], "6"),
      ("declined", "Declined", "A demand status for an item demand planning chose not to fund.", [], "0")]),
]
t = [file_header("02-customer-360-vocabularies.ttl", "Controlled vocabularies used by the Customer 360 tools.")]
for pre, title, desc, terms in VOCABS:
    S = f"<{NS[pre]}>"
    t.append(block(S, ["skos:ConceptScheme"], header_lines(NS[pre], pre + "voc" if pre in ("theme", "metric") else pre, title, desc, "scheme",
        f"{VER} ({TODAY}): created for the Customer 360 tools.") + ["  skos:hasTopConcept " + ", ".join(f"{pre}:{x[0]}" for x in terms) + " ;"]))
    for local, label, definition, alts, notation in terms:
        lines = [f"  rdfs:label {lit(label)} ;", f"  skos:prefLabel {lit(label)} ;"] + [f"  skos:altLabel {lit(a)} ;" for a in alts]
        lines += [f"  skos:definition {lit(definition)} ;", f"  skos:inScheme {S} ;", f"  skos:topConceptOf {S} ;"]
        if notation: lines.append(f"  skos:notation {plain(notation)} ;")
        if pre == "theme" and local in ("professional-employer-organization-relationship", "human-resources-technology-and-data"):
            lines.append('  skos:scopeNote "Added by the outcome benchmark: the business model\'s service-line layer does not cover these services."@en ;')
        t.append(block(f"{pre}:{local}", ["skos:Concept"], lines + [f'  owl:versionInfo "{VER}" ;'] + stamp()))
write("02-customer-360-vocabularies.ttl", "\n".join(t))

# ================================================================ helpers for instances
P = {p["id"]: p for p in D["personas"]}
J = {j["id"]: j for j in D["jobs"]}
STAGES = D["steps"]
STAGE_NAME = {s["id"]: s["name"] for s in STAGES}
PERSONA_NAME = {"P1": "BusinessOwner", "P2": "FinanceLeader", "P3": "HumanResourcesLeader", "P4": "OperationsAndSafetyLeader",
                "P5": "PeopleManager", "P6": "WorksiteEmployee", "P7": "SystemsAdministrator"}
PERSONA_DEF = {
    "P1": "A client persona who owns or runs a small or mid-sized client company and makes the final decision on its human resources provider and cost.",
    "P2": "A client persona who funds payroll, pays employer taxes and keeps the books, and judges the provider on total cost and accuracy.",
    "P3": "A client persona who runs human resources operations across every discipline, often as a team of one, and uses the provider every day.",
    "P4": "A client persona who is responsible for worksites where injury risk and workers' compensation cost matter to the business.",
    "P5": "A client persona who supervises a team and handles its hiring, time approval, coaching and performance conversations.",
    "P6": "A client persona who works for the client company and experiences the provider through pay, benefits, self-service and answers to questions.",
    "P7": "A client persona who connects employee data to other business systems and is accountable for its access and security."}
SURVEY_TARGET = {"P1": 200, "P2": 200, "P3": 200, "P4": 100, "P5": 200, "P6": 300, "P7": 100}
def pn(pid): return f"ob:{PERSONA_NAME[pid]}"
def jn(jid): return f"ob:Job-{jid}"
def sn(jid, st): return f"ob:Job-{jid}-{STAGE_NAME[st]}Step"
def on(oid): return f"ob:Outcome-{oid}"
def stage(st): return f"ob:{STAGE_NAME[st]}Stage"

# emotional / social jobs per persona
EMO = []
for p in D["personas"]:
    for i, e in enumerate(p["emotional"]):
        kind = "social" if re.match(r"^Be (seen|regarded|known)", e) else "emotional"
        EMO.append({"id": f"{p['id']}-{'S' if kind == 'social' else 'E'}{i+1}", "persona": p["id"], "kind": kind, "t": e})

# ================================================================ 03 stages
t = [file_header("03-job-map-stages.ttl", "The eight universal job map stages.")]
for i, s in enumerate(STAGES):
    lines = labels(s["name"]) + [f"  skos:definition {lit('A job map stage in which the job executor works to ' + lc_first(s['desc']) + '.')} ;",
             f"  jtbd:hasIdentifier {plain(s['id'])} ;", f'  jtbd:hasStageOrder "{i+1}"^^xsd:positiveInteger ;']
    t.append(block(stage(s["id"]), ["owl:NamedIndividual", "jtbd:job-map-stage"], lines + stamp()))
write("03-job-map-stages.ttl", "\n".join(t))

# ================================================================ 04 personas + emotional/social jobs
t = [file_header("04-client-personas.ttl", f"{len(D['personas'])} client personas and their {len(EMO)} emotional and social jobs.")]
for p in D["personas"]:
    ex = [j["id"] for j in D["jobs"] if p["id"] in j["ex"]] + [e["id"] for e in EMO if e["persona"] == p["id"]]
    pa = [j["id"] for j in D["jobs"] if p["id"] in j["part"]]
    lines = labels(p["name"], [p["short"]]) + [
        f"  skos:definition {lit(PERSONA_DEF[p['id']])} ;", f"  jtbd:hasIdentifier {plain(p['id'])} ;",
        f"  jtbd:hasShortName {plain(p['short'])} ;", f"  jtbd:hasTypicalTitles {lit(p['titles'])} ;",
        f"  jtbd:hasPersonaContext {lit(p['context'])} ;", f"  jtbd:hasBuyingRole {lit(p['buying'])} ;",
        f"  jtbd:hasPersonaGoal {lit(p['goal'])} ;", f"  jtbd:hasSurveyTarget {intl(SURVEY_TARGET[p['id']])} ;",
        "  jtbd:executesJob " + ", ".join(jn(x) for x in ex) + " ;",
        "  core:performsJob " + ", ".join(jn(x) for x in ex) + " ;"]
    if pa: lines.append("  jtbd:participatesInJob " + ", ".join(jn(x) for x in pa) + " ;")
    t.append(block(pn(p["id"]), ["owl:NamedIndividual", "jtbd:client-persona"], lines + stamp()))
for e in EMO:
    kind = "jtbd:social-job" if e["kind"] == "social" else "jtbd:emotional-job"
    genus = "A social job" if e["kind"] == "social" else "An emotional job"
    lines = labels(e["t"]) + [f"  skos:definition {lit(genus + ' of the ' + lc_first(expand(P[e['persona']]['name'])).replace(' / ', ' or ') + ' persona: ' + lc_first(expand(e['t'])) + '.')} ;",
             f"  jtbd:hasIdentifier {plain(e['id'])} ;", f"  jtbd:hasJobStatement {lit(e['t'])} ;", f"  jtbd:hasJobExecutor {pn(e['persona'])} ;"]
    t.append(block(jn(e["id"]), ["owl:NamedIndividual", kind], lines + stamp()))
write("04-client-personas.ttl", "\n".join(t))

# ================================================================ 05 jobs + per-job steps
t = [file_header("05-jobs-and-job-steps.ttl", f"{len(D['jobs'])} functional and consumption-chain jobs, each with its eight job steps.")]
for j in D["jobs"]:
    kind = "jtbd:core-functional-job" if j["kind"] == "core" else "jtbd:consumption-chain-job"
    genus = "A core functional job" if j["kind"] == "core" else "A consumption chain job"
    lines = labels(j["stmt"]) + [
        f"  skos:definition {lit(genus + ' in which the client persona needs to ' + lc_first(expand(j['stmt'])) + '.')} ;",
        f"  jtbd:hasIdentifier {plain(j['id'])} ;", f"  jtbd:hasJobStatement {lit(j['stmt'])} ;",
        "  jtbd:hasJobExecutor " + ", ".join(pn(x) for x in j["ex"]) + " ;"]
    if j["part"]: lines.append("  jtbd:hasJobParticipant " + ", ".join(pn(x) for x in j["part"]) + " ;")
    lines.append("  core:hasStep " + ", ".join(sn(j["id"], s["id"]) for s in STAGES) + " ;")
    lines.append("  jtbd:hasDesiredOutcome " + ",\n      ".join(on(o) for o in j["out"]) + " ;")
    t.append(block(jn(j["id"]), ["owl:NamedIndividual", kind], lines + stamp()))
    outs = [o for o in D["outcomes"] if o["job"] == j["id"]]
    for i, s in enumerate(STAGES):
        so = [o for o in outs if o["step"] == s["id"]]
        label = f"{s['name']}: {lc_first(j['stmt'])}"
        lines = labels(label) + [
            f"  skos:definition {lit('A job step in which the executor of the job to ' + lc_first(expand(j['stmt'])) + ' works to ' + lc_first(s['desc']) + '.')} ;",
            f"  jtbd:hasIdentifier {plain(j['id'] + '-' + s['id'])} ;", f"  core:isStepOf {jn(j['id'])} ;",
            f"  jtbd:atJobMapStage {stage(s['id'])} ;", f'  jtbd:hasStageOrder "{i+1}"^^xsd:positiveInteger ;']
        if i + 1 < len(STAGES): lines.append(f"  core:precedes {sn(j['id'], STAGES[i+1]['id'])} ;")
        if so: lines.append("  core:hasOutcome " + ", ".join(on(o["id"]) for o in so) + " ;")
        t.append(block(sn(j["id"], s["id"]), ["owl:NamedIndividual", "jtbd:job-step"], lines + stamp()))
write("05-jobs-and-job-steps.ttl", "\n".join(t))

# ================================================================ 06 outcomes
t = [file_header("06-desired-outcomes.ttl", f"{len(D['outcomes'])} desired outcomes with their job step, theme, metric type and survey items.")]
for o in D["outcomes"]:
    j = J[o["job"]]
    lines = labels(o["t"]) + [
        f"  skos:definition {lit('A desired outcome that a client uses, in the ' + STAGE_NAME[o['step']].lower() + ' step, to judge how well they ' + lc_first(expand(j['stmt'])) + '.')} ;",
        f"  jtbd:hasIdentifier {plain(o['id'])} ;", f"  jtbd:hasOutcomeStatement {lit(o['t'])} ;",
        f"  core:outcomeOf {sn(j['id'], o['step'])} ;", f"  jtbd:isOutcomeOfJob {jn(j['id'])} ;",
        f"  jtbd:atJobMapStage {stage(o['step'])} ;", f"  jtbd:hasBenchmarkTheme theme:{THEMES[o['theme']][0]} ;",
        f"  jtbd:hasOutcomeMetricType metric:{METRIC[o['m']][0]} ;",
        f"  jtbd:hasImportanceQuestion {lit('When you ' + lc_first(j['stmt']) + ', how important is it to ' + lc_first(o['t']) + '?')} ;",
        f"  jtbd:hasSatisfactionQuestion {lit('How satisfied are you with your current ability to ' + lc_first(o['t']) + '?')} ;"]
    t.append(block(on(o["id"]), ["owl:NamedIndividual", "jtbd:desired-outcome"], lines + stamp()))
write("06-desired-outcomes.ttl", "\n".join(t))

# ================================================================ 07 traceability (+ reference labels)
t = [file_header("07-service-traceability.ttl", "Links jobs to business-model domains and outcomes to domain services. The hr: IRIs are the\n# HR Services & PEO business model's current identifiers; their labels are carried here so the tools can show them.")]
t.append("# ---- Reference labels for business-model domains and services ----------\n")
for d in D["domains"]:
    t.append(f"hr:{d['id']} rdfs:label {lit(d['label'].replace('HR ', 'Human Resources ').replace(' & ', ' and '))} ;\n  skos:notation {plain(d['n'])} .\n")
for s in D["services"]:
    t.append(f"hr:{s['id']} rdfs:label {lit(s['label'])} ;\n  dct:isPartOf hr:{s['dom']} .\n")
t.append("# ---- Traceability --------------------------------------------------------\n")
for j in D["jobs"]:
    t.append(f"{jn(j['id'])} jtbd:appliesToBusinessDomain " + ", ".join(f"hr:{d}" for d in j["dom"]) + " .\n")
for o in D["outcomes"]:
    t.append(f"{on(o['id'])} jtbd:isAddressedByService " + ", ".join(f"hr:{s}" for s in o["svc"]) + " .\n")
write("07-service-traceability.ttl", "\n".join(t))

# ================================================================ 08 example survey wave
EX = D["example"]
SEG = {"PEO": "provider-clients", "NONPEO": "non-clients", "TOTAL": "total-market"}
SEGID = {"PEO": "clients", "NONPEO": "non-clients", "TOTAL": "total"}
WAVE = "ob:SurveyWave-example"
t = [file_header("08-survey-wave-example.ttl", "Generated example scores so the study, playbook and gateway can be exercised before the survey is fielded.")]
t.append(block(WAVE, ["owl:NamedIndividual", "jtbd:survey-wave"], labels("Example wave (generated scores)") + [
    f"  skos:definition {lit('A survey wave that holds generated example importance and satisfaction scores for every desired outcome, not survey results.')} ;",
    f"  jtbd:hasIdentifier {plain('example')} ;", f"  jtbd:hasWaveLabel {lit('Example wave (generated scores)')} ;",
    '  jtbd:isExampleData "true"^^xsd:boolean ;', f'  jtbd:hasFieldedDate "{TODAY}"^^xsd:date ;'] + stamp()))
for seg, rows in EX.items():
    if seg not in SEG: continue
    for oid, (imp, sat, n) in rows.items():
        t.append(f"ob:Score-example-{oid}-{SEGID[seg]} a owl:NamedIndividual, jtbd:outcome-score ;\n"
                 f"  core:measures {on(oid)} ; jtbd:inSurveyWave {WAVE} ; jtbd:hasSurveySegment segment:{SEG[seg]} ;\n"
                 f"  jtbd:hasImportanceScore {dec(imp)} ; jtbd:hasSatisfactionScore {dec(sat)} ; jtbd:hasRespondentCount {intl(n)} .\n")
write("08-survey-wave-example.ttl", "\n".join(t))

# ================================================================ combined TriG + manifest
def body_of(txt):
    return "\n".join("  " + l if l else l for l in txt.splitlines() if not l.startswith("@prefix") and not l.startswith("#")).strip("\n")
trig = [f"# Customer 360 knowledge graph {VER}: every graph in one TriG file for a one-step GraphDB import.\n# Generated {STAMP}\n\n" + PREFIXES]
for fname, (g, title) in GRAPHS.items():
    trig.append(f"# ---- {fname}: {title}\n<{g}> {{\n{body_of(FILES[fname])}\n}}\n")
open(os.path.join(OUT, f"customer-360-{VER}.trig"), "w").write("\n".join(trig))
manifest = {"release": VER, "generated": STAMP, "trig": f"customer-360-{VER}.trig",
            "graphs": [{"file": f, "graph": g, "title": title} for f, (g, title) in GRAPHS.items()],
            "runtimeGraphs": {"interviews": GRAPH_BASE + "interview/", "reviews": GRAPH_BASE + "reviews",
                              "decisions": GRAPH_BASE + "review-decisions", "surveyWaves": GRAPH_BASE + "survey-wave/",
                              "requirements": BASE + "graph/requirements-gateway/requirements",
                              "demand": BASE + "graph/demand-planning/demand-items"},
            "counts": {"personas": len(D["personas"]), "jobs": len(D["jobs"]), "emotionalAndSocialJobs": len(EMO),
                       "jobSteps": len(D["jobs"]) * len(STAGES), "stages": len(STAGES), "outcomes": len(D["outcomes"]),
                       "themes": len(THEMES), "scores": sum(len(v) for k, v in EX.items() if k in SEG)}}
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print(json.dumps(manifest["counts"]))
