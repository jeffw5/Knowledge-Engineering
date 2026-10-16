/* Sample Turtle for the Standards Conformance tool: a few terms written to the
   Semantic Governance v1.8 Part III standards, and a few that break them on purpose. */
window.KE_SAMPLE_TTL = `@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix core:    <https://www.insperity.com/ontology/core/> .
@prefix sm:      <https://www.insperity.com/ontology/service-model/> .
@prefix payroll: <https://www.insperity.com/ontology/payroll/> .
@prefix comp:    <https://www.insperity.com/taxonomy/compliance/> .

# ── Ontology header ─────────────────────────────────────────────
<https://www.insperity.com/ontology/service-model/> a owl:Ontology ;
    rdfs:label "Service model ontology"@en ;
    owl:versionInfo "0.1.0" ;
    owl:versionIRI <https://www.insperity.com/ontology/service-model/0.1.0/> .

# ── Conformant: the worked example from Section 3.7 ─────────────
sm:DocumentationStandards a owl:Class ;
    rdfs:label        "Documentation standards"@en ;
    skos:prefLabel    "Documentation standards"@en ;
    skos:altLabel     "Documentation guidelines"@en , "Documentation rules"@en ;
    skos:definition   """A software engineering artifact that specifies the required
                       content, structure, format, review, and retention of the
                       documentation produced during development."""@en ;
    skos:scopeNote    "Excludes coding standards and testing standards."@en ;
    rdfs:isDefinedBy <https://www.insperity.com/ontology/service-model/> ;
    rdfs:subClassOf   sm:SoftwareEngineeringArtifact ,
        [ a owl:Restriction ; owl:onProperty sm:appliesTo ;
          owl:someValuesFrom sm:SoftwareEngineeringWorkProduct ] ;
    owl:hasKey        ( sm:hasDocumentIdentifier ) ;
    core:hasLifecycleStatus core:Draft ;
    owl:versionInfo   "0.1.0" ;
    dcterms:created   "2026-10-13"^^xsd:date .

sm:SoftwareEngineeringArtifact a owl:Class ;
    rdfs:label "Software engineering artifact"@en ;
    skos:definition "A development artifact that is produced or used by software engineering work."@en ;
    rdfs:isDefinedBy <https://www.insperity.com/ontology/service-model/> ;
    rdfs:subClassOf core:Artifact .

sm:appliesTo a owl:ObjectProperty ;
    rdfs:label "applies to"@en ;
    skos:definition "A relation from a standard to the work product it governs."@en ;
    rdfs:isDefinedBy <https://www.insperity.com/ontology/service-model/> ;
    rdfs:domain sm:DocumentationStandards ;
    rdfs:range sm:SoftwareEngineeringWorkProduct .

sm:hasDocumentIdentifier a owl:DatatypeProperty ;
    rdfs:label "has document identifier"@en ;
    skos:definition "A data property that gives the stable identifier of a document."@en ;
    rdfs:isDefinedBy <https://www.insperity.com/ontology/service-model/> ;
    rdfs:domain sm:DocumentationStandards ;
    rdfs:range xsd:string .

# ── Breaks the standards on purpose ─────────────────────────────
sm:SE_Documentation a owl:Class ;
    rdfs:label "SE Documentation Guide" .

<http://example.org/legacy/PayrollThing> a owl:Class ;
    rdfs:label "Payroll thing"@en ;
    skos:definition "A legacy class defined outside the Company base URL."@en ;
    rdfs:subClassOf owl:Thing .

payroll:HasOwner a owl:ObjectProperty ;
    rdfs:label "has owner" ;
    skos:definition "Relates a payroll run to its owner."@en .

payroll:effectiveDate a owl:DatatypeProperty ;
    rdfs:label "Effective date"@en ;
    skos:definition "A data property giving the date a rule takes effect."@en ;
    rdfs:domain payroll:PayrollRun ; rdfs:range xsd:date .

<https://www.insperity.com/ontology/payroll/2.1.0/PayrollRun> a owl:Class ;
    rdfs:label "Payroll run"@en ;
    skos:definition "A process step that calculates and issues pay for one pay period."@en ;
    rdfs:subClassOf core:ProcessStep ;
    rdfs:isDefinedBy <https://www.insperity.com/ontology/payroll/> .

payroll:PEOClientAccount a owl:Class ;
    rdfs:label "PEO Client Account"@en ;
    skos:definition "Client account."@en ;
    rdfs:subClassOf core:Asset ;
    owl:equivalentClass [ a owl:Restriction ; owl:onProperty payroll:HasOwner ; owl:someValuesFrom core:Party ] .

# ── Taxonomy ───────────────────────────────────────────────────
<https://www.insperity.com/taxonomy/compliance/> a skos:ConceptScheme ;
    rdfs:label "Compliance taxonomy"@en ;
    owl:versionInfo "1.2" ;
    skos:hasTopConcept comp:WagesAndHours .

comp:WagesAndHours a skos:Concept ;
    skos:prefLabel "Wages and hours"@en ;
    skos:definition "A compliance category covering minimum wage, overtime, and hours worked."@en ;
    skos:notation "WH" ;
    skos:inScheme <https://www.insperity.com/taxonomy/compliance/> ;
    skos:topConceptOf <https://www.insperity.com/taxonomy/compliance/> .

comp:FamilyAndMedicalLeave a skos:Concept ;
    skos:prefLabel "Family and medical leave"@en , "FMLA leave"@en ;
    skos:altLabel "FMLA"@en ;
    skos:broader comp:WagesAndHours .
`;
