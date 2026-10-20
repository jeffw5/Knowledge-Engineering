/* KE Workbench — Standards Conformance rules.
   Each rule encodes a Part III / Appendix E standard from Semantic Governance v1.9 (§3.11 metadata included).
   runChecks(quads, { bases }) → { rules:[{...rule, checked, failed}], findings:[...], stats }
   quads: [{ s, p, o, g }] with terms { t:'iri'|'bnode'|'lit', v, lang?, dt? } */
(function (root) {
  var RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', RDFS = 'http://www.w3.org/2000/01/rdf-schema#',
      OWL = 'http://www.w3.org/2002/07/owl#', SKOS = 'http://www.w3.org/2004/02/skos/core#',
      SH = 'http://www.w3.org/ns/shacl#', DCT = 'http://purl.org/dc/terms/', XSD = 'http://www.w3.org/2001/XMLSchema#',
      CORE = 'https://www.insperity.com/ontology/core/';
  var P = {
    type: RDF + 'type', label: RDFS + 'label', pref: SKOS + 'prefLabel', alt: SKOS + 'altLabel',
    def: SKOS + 'definition', sub: RDFS + 'subClassOf', isDef: RDFS + 'isDefinedBy', dom: RDFS + 'domain',
    rng: RDFS + 'range', inScheme: SKOS + 'inScheme', topOf: SKOS + 'topConceptOf', hasTop: SKOS + 'hasTopConcept',
    ver: OWL + 'versionInfo', verIri: OWL + 'versionIRI', eq: OWL + 'equivalentClass', dju: OWL + 'disjointUnionOf',
    broader: SKOS + 'broader', narrower: SKOS + 'narrower', related: SKOS + 'related',
    // links to the vocabulary term (§3.11): core:hasPrimaryTerm + dcterms:subject; dc:subject (Dublin Core 1.1) is the legacy form
    primary: CORE + 'hasPrimaryTerm', subject: DCT + 'subject', dcSubject: 'http://purl.org/dc/elements/1.1/subject', formalizedBy: CORE + 'formalizedBy',
    desc: DCT + 'description', title: DCT + 'title', comment: RDFS + 'comment',
    // §3.11 asset header fields
    vaemNs: 'http://www.linkedmodel.org/schema/vaem#namespace', nsPrefix: 'http://purl.org/vocab/vann/preferredNamespacePrefix',
    language: DCT + 'language', creator: DCT + 'creator', publisher: DCT + 'publisher', conformsTo: DCT + 'conformsTo',
    source: DCT + 'source', created: DCT + 'created', modified: DCT + 'modified', issued: DCT + 'issued'
  };
  var SUBJECT_PREDS = [P.primary, P.subject, P.dcSubject];
  // Predicates whose IRI objects must point at a term that exists (broken-reference rule)
  var REF_PREDICATES = ['broader', 'narrower', 'related', 'primary', 'subject', 'dcSubject', 'sub', 'dom', 'rng', 'inScheme', 'topOf', 'hasTop'].map(function (k) { return P[k]; });
  // Predicates the GraphDB loader needs to fetch
  var PREDICATES = Object.keys(P).map(function (k) { return P[k]; });

  var EXTERNAL = [/^https?:\/\/www\.w3\.org\//, /^https?:\/\/purl\.org\//, /^https?:\/\/xmlns\.com\//, /^https?:\/\/purl\.obolibrary\.org\//,
    /^https?:\/\/schema\.org\//, /^https?:\/\/www\.linkedmodel\.org\//, /^https?:\/\/qudt\.org\//, /^https?:\/\/www\.omg\.org\//,
    /^https?:\/\/spec\.edmcouncil\.org\//, /^https?:\/\/www\.ontologydesignpatterns\.org\//, /^urn:/];
  var AREAS = ['ontology', 'vocabulary', 'taxonomy', 'mapping', 'shapes', 'resource', 'graph', 'change', 'requirement'];

  function kindOf(e) {
    var t = e.types;
    if (t.has(OWL + 'Ontology')) return 'ontology';
    if (t.has(SKOS + 'ConceptScheme')) return 'scheme';
    if (t.has(SKOS + 'Concept')) return 'concept';
    if (t.has(OWL + 'ObjectProperty')) return 'objprop';
    if (t.has(OWL + 'DatatypeProperty')) return 'dataprop';
    if (t.has(OWL + 'AnnotationProperty')) return 'annprop';
    if (t.has(OWL + 'Class') || t.has(RDFS + 'Class')) return 'class';
    if (t.has(SH + 'NodeShape')) return 'shape';
    if (t.has(OWL + 'NamedIndividual')) return 'individual';
    return null;
  }
  var KIND_LABEL = { ontology: 'Ontology', scheme: 'Concept scheme', concept: 'Concept', objprop: 'Object property',
    dataprop: 'Data property', annprop: 'Annotation property', class: 'Class', shape: 'Shape', individual: 'Individual' };
  var TERM = { class: 1, objprop: 1, dataprop: 1, concept: 1 };
  var PROP = { objprop: 1, dataprop: 1 };

  function localName(iri) {
    var s = iri.replace(/[\/#]+$/, '');
    var i = Math.max(s.lastIndexOf('/'), s.lastIndexOf('#'));
    return decodeURIComponentSafe(s.slice(i + 1));
  }
  function decodeURIComponentSafe(s) { try { return decodeURIComponent(s); } catch (e) { return s; } }
  function vals(e, p) { return e.p[p] || []; }
  function lits(e, p) { return vals(e, p).filter(function (o) { return o.t === 'lit'; }); }
  function prefLabels(e) { return lits(e, P.pref).length ? lits(e, P.pref) : lits(e, P.label); }
  function anyLabel(e) { var l = prefLabels(e); var en = l.filter(function (x) { return x.lang === 'en'; }); return (en[0] || l[0] || {}).v || ''; }
  function concepKind(e) { return /\/taxonomy\//.test(e.iri) ? 'taxonomy' : /\/vocabulary\//.test(e.iri) ? 'vocabulary' : null; }

  var ACRONYM = /\b(?![IVX]+\b)[A-Z]{2,}s?\b/;          // PEO, FMLA, HRs — not roman numerals
  var CAMEL_ACRONYM = /[A-Z]{2,}(?=[A-Z][a-z]|$|[0-9_-])|[A-Z]{3,}/;

  // ── Acronym and organization policy (ingest/ke-ingest.config.json via /api/ingest/policy) ──
  var STOP = { and: 1, of: 1, the: 1, for: 1, to: 1, in: 1, on: 1, '&': 1, a: 1, an: 1 };
  function policyFrom(j) {
    j = j || {};
    var approved = {}; (j.approved || []).forEach(function (a) { approved[String(a).toUpperCase()] = 1; });
    var exp = {}; Object.keys(j.expansions || {}).forEach(function (k) { exp[k.toUpperCase()] = j.expansions[k]; });
    var orgs = (j.organizations || []).map(function (o) {
      return { name: o.name, replacement: o.replacement || 'the organization', removeTerms: o.removeTerms !== false,
               rx: new RegExp(o.patterns.map(function (x) { return '(?:' + x + ')'; }).join('|'), 'i') };
    });
    return { approved: approved, expansions: exp, orgs: orgs };
  }
  var ACRONYM_G = /\b(?![IVX]+\b)[A-Z]{2,}s?\b/g;
  function acronymsIn(label, pol) {
    var out = [], m; ACRONYM_G.lastIndex = 0;
    while ((m = ACRONYM_G.exec(label || ''))) {
      var t = m[0];
      if (pol && (pol.approved[t.toUpperCase()] || (/s$/.test(t) && pol.approved[t.slice(0, -1).toUpperCase()]))) continue;
      out.push(t);
    }
    return out;
  }
  function orgHit(text, pol) {
    if (!pol) return null;
    for (var i = 0; i < pol.orgs.length; i++) { var m = pol.orgs[i].rx.exec(text || ''); if (m) return { org: pol.orgs[i], hit: m[0] }; }
    return null;
  }
  function initials(ph) {
    var w = ph.split(/[\s\/&,-]+/).filter(function (x) { return x && !STOP[x.toLowerCase()]; });
    return { ini: w.map(function (x) { return x[0]; }).join('').toUpperCase(), n: w.length };
  }
  function expansionFor(tok, alts, defs, pol) {
    var key = tok.toUpperCase();
    if (pol && pol.expansions[key]) return { text: pol.expansions[key], from: 'config' };
    for (var i = 0; i < (alts || []).length; i++) {
      var a = initials(alts[i]); if (a.n > 1 && a.ini === key && !/^[A-Z0-9-]+$/.test(alts[i].trim())) return { text: alts[i].trim(), from: 'alternative label' };
    }
    for (var j = 0; j < (defs || []).length; j++) {
      var m = /\b(acronym|abbreviation)\s+for\s+(.+?)(?:,\s+(?:this|that|a|an|the|is|which)\b|\s+is\b|[.;(])/i.exec(defs[j]);
      if (m) { var d = initials(m[2].trim()); if (d.n > 1 && (d.ini === key || (m[1].toLowerCase() === 'abbreviation' && d.ini[0] === key[0] && d.n <= 5))) return { text: m[2].trim(), from: 'definition' }; }
    }
    return null;
  }
  function sentenceCase(label) {
    return String(label).trim().split(/\s+/).map(function (w, i) {
      var core = w.replace(/[^A-Za-z]/g, '');
      if (i === 0) return core.length > 1 && core === core.toUpperCase() ? w : w.charAt(0).toUpperCase() + w.slice(1);
      return core.length > 1 && core === core.toUpperCase() ? w : w.toLowerCase();
    }).join(' ');
  }
  function expandLabel(label, alts, defs, pol) {
    var out = label, done = [];
    acronymsIn(label, pol).forEach(function (tok) {
      var plural = /s$/.test(tok) && tok.length > 2, e = plural ? expansionFor(tok.slice(0, -1), alts, defs, pol) : null;
      if (e) e = { text: e.text + 's', from: e.from }; else e = expansionFor(tok, alts, defs, pol);
      if (!e) return;
      var rx = new RegExp('(?:-|(?<![\\w]))' + tok.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![\\w])'), m = rx.exec(out);
      if (!m) return;
      out = out.slice(0, m.index) + (m[0][0] === '-' ? ' ' : '') + e.text + out.slice(m.index + m[0].length);
      done.push({ acronym: tok, text: e.text, from: e.from });
    });
    out = out.replace(/\b(\w+)(\s+\1\b)+/gi, '$1');
    return { label: done.length ? sentenceCase(out) : label, done: done };
  }
  function genericText(text, pol) {
    if (!pol) return text;
    pol.orgs.forEach(function (o) {
      var src = o.rx.source;
      text = text.replace(new RegExp('(?:' + src + ")(?:['’]s)", 'gi'), o.replacement + "'s")
        .replace(new RegExp('(?:' + src + ')(?=\\s+[A-Z][a-z])', 'g'), o.replacement + "'s")   // "Verizon Data Marketplace" → "the organization's Data Marketplace"
        .replace(new RegExp(src, 'gi'), o.replacement);
    });
    text = text.replace(/\b(an|a|the) (the organization)/gi, '$2');
    return text.replace(/(^|[.!?]\s+)the organization/g, function (m, p1) { return p1 + 'The organization'; });
  }

  function rules(ctx) {
    var bases = ctx.bases, primary = bases[0];
    function underBase(iri) { var u = iri.toLowerCase(); return bases.some(function (b) { return u.indexOf(b.toLowerCase()) === 0; }); }
    function baseOf(iri) { var u = iri.toLowerCase(); return bases.filter(function (b) { return u.indexOf(b.toLowerCase()) === 0; })[0]; }
    function segs(iri) { var b = baseOf(iri); return b ? iri.slice(b.length).split(/[?#]/)[0].split('/').filter(Boolean) : []; }

    return [
      { id: 'base-url', sec: '3.2', sev: 'error', title: 'Company base URL',
        desc: 'Every identifier lives under the base URL (' + primary + ').',
        applies: function (e) { return !!e.kind; },
        check: function (e) { return underBase(e.iri) ? null : 'Outside the compliant base URLs: ' + e.iri.replace(/^(https?:\/\/[^\/]+\/?).*/, '$1'); } },

      { id: 'uri-pattern', sec: '3.2', sev: 'warn', title: 'URI pattern',
        desc: 'Slash-based namespaces: /{ontology|vocabulary|taxonomy|mapping|shapes|resource}/{domain}/{Term}, domain in lower-case hyphenated words.',
        applies: function (e) { return !!e.kind && underBase(e.iri); },
        check: function (e) {
          if (e.iri.indexOf('#') >= 0) return 'Hash namespace — use slash-based IRIs so each term resolves on its own';
          var s = segs(e.iri);
          if (!s.length) return 'No path after the base URL';
          if (AREAS.indexOf(s[0]) < 0) return 'First path segment "' + s[0] + '" is not one of ' + AREAS.slice(0, 6).join(', ');
          var want = e.kind === 'concept' || e.kind === 'scheme' ? ['vocabulary', 'taxonomy'] : e.kind === 'shape' ? ['shapes'] : (TERM[e.kind] || PROP[e.kind] || e.kind === 'ontology' || e.kind === 'annprop') ? ['ontology'] : null;
          if (want && want.indexOf(s[0]) < 0) return KIND_LABEL[e.kind] + ' is under /' + s[0] + '/ — expected /' + want.join('/ or /') + '/';
          if (s.length > 1 && !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(s[1]) && !/^\d+\.\d+/.test(s[1])) return 'Domain segment "' + s[1] + '" should be lower-case words joined by hyphens';
          if ((TERM[e.kind] || e.kind === 'shape') && s.length > 3 && !/^\d+\.\d+/.test(s[2])) return 'Hierarchy in the path — keep {domain}/{Term} and move the hierarchy into rdfs:subClassOf or skos:broader';
          return null;
        } },

      { id: 'name-case', sec: '3.2', sev: 'warn', title: 'Identifier case',
        desc: 'Classes and taxonomy concepts UpperCamelCase; object properties lowerCamelCase; data properties has-/is- prefix; vocabulary terms lower-case hyphenated; shapes end in Shape.',
        applies: function (e) { return (TERM[e.kind] || e.kind === 'shape') && !!localName(e.iri); },
        check: function (e) {
          var n = localName(e.iri);
          if (/[_:\s]/.test(n)) return '"' + n + '" contains underscores, colons or spaces';
          if (e.kind === 'class' && !/^[A-Z][A-Za-z0-9]*$/.test(n)) return 'Class "' + n + '" should be UpperCamelCase';
          if (e.kind === 'objprop' && !/^[a-z][A-Za-z0-9]*$/.test(n)) return 'Object property "' + n + '" should be a lowerCamelCase verb phrase';
          if (e.kind === 'dataprop' && !/^(has|is)[A-Z][A-Za-z0-9]*$/.test(n)) return 'Data property "' + n + '" should be lowerCamelCase with a has- or is- prefix';
          if (e.kind === 'shape' && !/^[A-Z][A-Za-z0-9]*Shape$/.test(n)) return 'Shape "' + n + '" should be the target class name plus Shape';
          if (e.kind === 'concept') {
            var ck = concepKind(e);
            if (ck === 'taxonomy' && !/^[A-Z][A-Za-z0-9]*$/.test(n)) return 'Taxonomy concept "' + n + '" should be UpperCamelCase';
            if (ck === 'vocabulary' && !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(n)) return 'Vocabulary term "' + n + '" should be lower-case words joined by hyphens';
          }
          return null;
        } },

      { id: 'acronym-id', sec: '3.2', sev: 'error', title: 'No acronyms in identifiers',
        desc: 'Identifiers use full words: ProfessionalEmployerOrganization, not PEO.',
        applies: function (e) { return (TERM[e.kind] || e.kind === 'shape' || e.kind === 'individual') && !!localName(e.iri); },
        check: function (e) { var n = localName(e.iri), m = n.match(CAMEL_ACRONYM) || n.match(/(^|[_-])([A-Z]{2,})(?=[_-]|$)/);
          return m ? 'Identifier "' + n + '" contains the acronym "' + (m[2] || m[0]).replace(/[^A-Z]/g, '') + '"' : null; } },

      { id: 'acronym-label', sec: '3.2', sev: 'error', title: 'No acronyms in preferred labels',
        desc: 'Acronyms belong in skos:altLabel only, so search still finds them. Approved names (Appendix F) are allowed.',
        applies: function (e) { return !!e.kind && prefLabels(e).length > 0; },
        check: function (e) { for (var i = 0; i < prefLabels(e).length; i++) { var l = prefLabels(e)[i], bad = acronymsIn(l.v, ctx.policy);
            if (bad.length) return 'Preferred label "' + l.v + '" contains "' + bad.join('", "') + '" — spell it out and move the acronym to skos:altLabel'; }
          return null; } },

      { id: 'org-content', sec: '3.2', sev: 'error', title: "No other organization's content",
        desc: 'Labels, definitions and descriptions do not name another organization (the organizations list in the ingestion configuration).',
        applies: function (e) { return !!e.kind && !!ctx.policy && ctx.policy.orgs.length > 0; },
        check: function (e) {
          var fields = [['pref', 'label'], ['label', 'label'], ['alt', 'alternative label'], ['def', 'definition'], ['desc', 'description'], ['comment', 'comment'], ['title', 'title']];
          for (var i = 0; i < fields.length; i++) {
            var ls = lits(e, P[fields[i][0]]);
            for (var j = 0; j < ls.length; j++) { var h = orgHit(ls[j].v, ctx.policy); if (h) return fields[i][1] + ' names ' + h.org.name + ' ("' + h.hit + '")'; }
          }
          return null; } },

      { id: 'broken-ref', sec: '3.7', sev: 'error', title: 'No broken references',
        desc: 'Parents, children, related terms, linked vocabulary terms, domains and ranges point at terms that exist in their model.',
        applies: function (e) { return !!e.kind && !!ctx.defined; },
        check: function (e) {
          for (var i = 0; i < REF_PREDICATES.length; i++) {
            if (ctx.vocab && SUBJECT_PREDS.indexOf(REF_PREDICATES[i]) >= 0) continue;     // reported by vocab-term instead
            if (REF_PREDICATES[i] === P.subject && !/\/taxonomy\//.test(e.iri)) continue;   // a header's dcterms:subject names a domain concept elsewhere
            var os = vals(e, REF_PREDICATES[i]);
            for (var j = 0; j < os.length; j++) {
              var o = os[j]; if (o.t !== 'iri' || ctx.defined.has(o.v)) continue;
              if (ctx.assets.some(function (a) { return o.v !== a && o.v.indexOf(a) === 0; }))
                return localName(REF_PREDICATES[i]) + ' points at ' + localName(o.v) + ', which does not exist in its model';
            }
          }
          return null; } },


      { id: 'vocab-term', sec: '3.11', sev: 'error', title: 'Taxonomy term in a vocabulary',
        desc: 'Every taxonomy concept names its vocabulary term with core:hasPrimaryTerm (and dcterms:subject), and that term exists in one of the vocabularies.',
        applies: function (e) { return !!ctx.vocab && (e.kind === 'class' || e.kind === 'concept') && /\/taxonomy\//.test(e.iri); },
        check: function (e) {
          var s = []; SUBJECT_PREDS.forEach(function (p) { s = s.concat(vals(e, p).filter(function (o) { return o.t === 'iri'; })); });
          if (!s.length) return 'Not in any vocabulary: no core:hasPrimaryTerm or dcterms:subject link to a vocabulary term';
          if (!s.some(function (o) { return ctx.vocab.has(o.v); })) return 'Linked to ' + localName(s[0].v) + ', which is in no vocabulary';
          return null; } },

      { id: 'primary-term', sec: '3.11', sev: 'warn', title: 'Primary vocabulary term',
        desc: 'A taxonomy concept names exactly one vocabulary term with core:hasPrimaryTerm; dc:subject (Dublin Core 1.1) is replaced by dcterms:subject.',
        applies: function (e) { return e.kind === 'concept' && /\/taxonomy\//.test(e.iri) && SUBJECT_PREDS.some(function (p) { return vals(e, p).length; }); },
        check: function (e) {
          var pt = vals(e, P.primary);
          if (!pt.length) return 'No core:hasPrimaryTerm' + (vals(e, P.dcSubject).length ? ' (linked with legacy dc:subject; re-ingest or relink)' : '');
          if (pt.length > 1) return pt.length + ' primary terms — keep one, the rest as dcterms:subject';
          return null; } },

      { id: 'skos-taxonomy', sec: '3.11', sev: 'warn', title: 'Taxonomies stay in SKOS',
        desc: 'A taxonomy is a skos:ConceptScheme of skos:Concept terms; inherited meaning comes from the ontology class each concept is formalized by.',
        applies: function (e) { return (e.kind === 'class' || e.kind === 'ontology') && /\/taxonomy\//.test(e.iri) && underBase(e.iri); },
        check: function (e) { return e.kind === 'class' ? 'OWL class in a taxonomy — re-ingest to convert it to a SKOS concept' : 'Taxonomy declared as owl:Ontology — it should be a skos:ConceptScheme'; } },

      { id: 'header-fields', sec: '3.11', sev: 'warn', title: 'Asset header fields',
        desc: 'Vocabulary, taxonomy and ontology headers carry vaem:namespace, vann:preferredNamespacePrefix, title, description, subject, language, creator, publisher, created, modified, version, version IRI and conformsTo; taxonomies add dcterms:source.',
        applies: function (e) { return (e.kind === 'ontology' || e.kind === 'scheme') && underBase(e.iri); },
        check: function (e) {
          var want = [['vaemNs', 'vaem:namespace'], ['nsPrefix', 'vann:preferredNamespacePrefix'], ['title', 'dcterms:title'], ['desc', 'dcterms:description'],
                      ['subject', 'dcterms:subject'], ['language', 'dcterms:language'], ['creator', 'dcterms:creator'], ['publisher', 'dcterms:publisher'],
                      ['created', 'dcterms:created'], ['modified', 'dcterms:modified'], ['verIri', 'owl:versionIRI'], ['conformsTo', 'dcterms:conformsTo']];
          if (/\/taxonomy\//.test(e.iri)) want.push(['source', 'dcterms:source']);
          var miss = want.filter(function (w) { return !vals(e, P[w[0]]).length; }).map(function (w) { return w[1]; });
          return miss.length ? 'Missing ' + miss.join(', ') : null; } },

      { id: 'valid-date', sec: '3.11', sev: 'error', title: 'Valid dates (ISO 8601)',
        desc: 'dcterms:created, modified and issued are valid xsd:date (2026-10-14) or xsd:dateTime (2026-10-14T09:30:00Z) values.',
        applies: function (e) { return !!e.kind && [P.created, P.modified, P.issued].some(function (p) { return vals(e, p).length; }); },
        check: function (e) {
          var ps = [P.created, P.modified, P.issued];
          for (var i = 0; i < ps.length; i++) { var ls = lits(e, ps[i]);
            for (var j = 0; j < ls.length; j++) { var l = ls[j];
              if (l.dt === XSD + 'dateTime' && !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})?$/.test(l.v)) return localName(ps[i]) + ' "' + l.v + '" is not a valid xsd:dateTime' + (/^\d{4}-\d{2}-\d{2}$/.test(l.v) ? ' (a date alone is xsd:date)' : '');
              if (l.dt === XSD + 'date' && !/^\d{4}-\d{2}-\d{2}(Z|[+-]\d{2}:\d{2})?$/.test(l.v)) return localName(ps[i]) + ' "' + l.v + '" is not a valid xsd:date'; } }
          return null; } },

      { id: 'label', sec: '3.7', sev: 'error', title: 'Label present, tagged @en',
        desc: 'rdfs:label and skos:prefLabel, one per language, tagged with a language.',
        applies: function (e) { return !!TERM[e.kind] || e.kind === 'scheme' || e.kind === 'ontology'; },
        check: function (e) {
          var all = lits(e, P.label).concat(lits(e, P.pref));
          if (!all.length) return 'No rdfs:label or skos:prefLabel';
          var untagged = all.filter(function (l) { return !l.lang; });
          if (untagged.length) return 'Label "' + untagged[0].v + '" has no language tag (add @en)';
          return null;
        } },

      { id: 'sentence-case', sec: '3.2', sev: 'warn', title: 'Sentence-case labels',
        desc: 'Preferred labels are written in sentence case: "Pay period", not "Pay Period".',
        applies: function (e) { return !!TERM[e.kind] && prefLabels(e).length > 0; },
        check: function (e) {
          var bad = prefLabels(e).filter(function (l) {
            var w = l.v.trim().split(/\s+/); if (w.length < 2) return false;
            var caps = w.slice(1).filter(function (x) { return /^[A-Z][a-z]/.test(x) && x.length > 2; });
            return caps.length >= Math.max(1, Math.ceil((w.length - 1) / 2));
          });
          return bad.length ? 'Label "' + bad[0].v + '" looks like Title Case' : null;
        } },

      { id: 'definition', sec: '3.7', sev: 'error', title: 'Definition present',
        desc: 'Every class, concept and property carries one skos:definition.',
        applies: function (e) { return !!TERM[e.kind]; },
        check: function (e) { var d = lits(e, P.def);
          if (!d.length) return 'No skos:definition';
          if (d.filter(function (x) { return x.lang === 'en'; }).length > 1) return 'More than one English definition';
          return null; } },

      { id: 'genus', sec: '3.7', sev: 'info', title: 'Genus plus differentia',
        desc: 'One sentence, ISO 704 form: "A [parent] that [distinguishing feature]".',
        applies: function (e) { return !!TERM[e.kind] && lits(e, P.def).length > 0; },
        check: function (e) {
          var d = lits(e, P.def)[0].v.replace(/\s+/g, ' ').trim();
          if (!/^(A|An)\s/.test(d)) return 'Definition does not open with "A …" / "An …" (genus first)';
          if ((d.replace(/\b(e\.g|i\.e|etc)\./g, '').match(/[.!?](\s|$)/g) || []).length > 1) return 'Definition runs to more than one sentence';
          if (d.split(' ').length < 6) return 'Definition is very short — add the distinguishing feature';
          return null;
        } },

      { id: 'parent', sec: '3.7', sev: 'error', title: 'Named parent class',
        desc: 'At least one named rdfs:subClassOf parent (not owl:Thing); the hierarchy carries the meaning.',
        applies: function (e) { return e.kind === 'class'; },
        check: function (e) { var named = vals(e, P.sub).filter(function (o) { return o.t === 'iri' && o.v !== OWL + 'Thing'; });
          return named.length ? null : 'No named rdfs:subClassOf parent'; } },

      { id: 'defined-by', sec: '3.7', sev: 'warn', title: 'rdfs:isDefinedBy',
        desc: 'The IRI of the ontology that owns the term.',
        applies: function (e) { return e.kind === 'class' || !!PROP[e.kind]; },
        check: function (e) { return vals(e, P.isDef).length ? null : 'No rdfs:isDefinedBy'; } },

      { id: 'domain-range', sec: '3.10', sev: 'warn', title: 'Property domain and range',
        desc: 'Every property has a domain and range (and edges draw in the editor).',
        applies: function (e) { return !!PROP[e.kind]; },
        check: function (e) { var miss = [];
          if (!vals(e, P.dom).length) miss.push('rdfs:domain'); if (!vals(e, P.rng).length) miss.push('rdfs:range');
          return miss.length ? 'Missing ' + miss.join(' and ') : null; } },

      { id: 'avoid-axioms', sec: '3.7', sev: 'info', title: 'Restricted OWL constructs',
        desc: 'owl:equivalentClass only with Architecture approval; avoid owl:disjointUnionOf.',
        applies: function (e) { return e.kind === 'class'; },
        check: function (e) {
          if (vals(e, P.dju).length) return 'Uses owl:disjointUnionOf — use subclasses plus owl:AllDisjointClasses';
          if (vals(e, P.eq).length) return 'Uses owl:equivalentClass — needs Architecture approval (forces run-time inference)';
          return null; } },

      { id: 'in-scheme', sec: '3.9', sev: 'error', title: 'Concept in scheme, one preferred label',
        desc: 'Every concept has skos:inScheme and exactly one skos:prefLabel per language.',
        applies: function (e) { return e.kind === 'concept'; },
        check: function (e) {
          var problems = [];
          if (!vals(e, P.inScheme).length && !vals(e, P.topOf).length) problems.push('no skos:inScheme');
          var byLang = {}; lits(e, P.pref).forEach(function (l) { var k = l.lang || '(none)'; byLang[k] = (byLang[k] || 0) + 1; });
          if (!lits(e, P.pref).length) problems.push('no skos:prefLabel');
          Object.keys(byLang).forEach(function (k) { if (byLang[k] > 1) problems.push(byLang[k] + ' preferred labels for ' + k); });
          return problems.length ? problems.join('; ') : null; } },

      { id: 'versioned-term', sec: '3.3', sev: 'error', title: 'No version in term IRIs',
        desc: 'Only ontology and vocabulary releases get versioned IRIs; class, property and concept IRIs never do.',
        applies: function (e) { return !!TERM[e.kind]; },
        check: function (e) { var m = e.iri.match(/\/v?\d+\.\d+(\.\d+)?\//); return m ? 'Term IRI contains a version segment "' + m[0] + '"' : null; } },

      { id: 'version-format', sec: '3.3', sev: 'warn', title: 'Semantic version on releases',
        desc: 'Ontologies and schemes carry owl:versionInfo as MAJOR.MINOR.PATCH and an owl:versionIRI for the release (§3.3, §3.11).',
        applies: function (e) { return e.kind === 'ontology' || e.kind === 'scheme'; },
        check: function (e) { var v = lits(e, P.ver);
          if (!v.length) return 'No owl:versionInfo';
          if (!/^\d+\.\d+\.\d+$/.test(v[0].v.trim())) return 'owl:versionInfo "' + v[0].v + '" is not MAJOR.MINOR.PATCH';
          if (!vals(e, P.verIri).length) return 'No owl:versionIRI for this release';
          return null; } }
    ];
  }

  // Graph-level rule: one concept scheme per taxonomy graph / file
  function graphRule(entities) {
    var byGraph = {};
    entities.forEach(function (e) { if (e.kind === 'scheme' && /\/taxonomy\//.test(e.iri)) e.graphs.forEach(function (g) { (byGraph[g] = byGraph[g] || []).push(e); }); });
    var findings = [], checked = 0;
    Object.keys(byGraph).forEach(function (g) {
      checked++;
      var schemes = byGraph[g];
      if (schemes.length > 1) findings.push({ iri: g, kind: 'graph', detail: schemes.length + ' taxonomy concept schemes in one graph — declare exactly one' });
      schemes.forEach(function (s) {
        var hasTop = (s.p[P.hasTop] || []).length || entities.some(function (c) { return (c.p[P.topOf] || []).some(function (o) { return o.v === s.iri; }); });
        if (!hasTop) findings.push({ iri: s.iri, kind: 'scheme', detail: 'No top concepts flagged (skos:hasTopConcept / skos:topConceptOf)' });
      });
    });
    return { rule: { id: 'one-scheme', sec: 'E.3', sev: 'error', title: 'One scheme per taxonomy, top concepts flagged',
      desc: 'Declare exactly one skos:ConceptScheme per taxonomy and flag its top concepts.' }, findings: findings, checked: checked };
  }

  function buildEntities(quads) {
    var map = new Map();
    quads.forEach(function (q) {
      if (!q.s || q.s.t !== 'iri') return;
      var e = map.get(q.s.v);
      if (!e) { e = { iri: q.s.v, types: new Set(), p: {}, graphs: new Set() }; map.set(q.s.v, e); }
      e.graphs.add(q.g || 'default');
      if (q.p.v === P.type && q.o.t === 'iri') e.types.add(q.o.v);
      (e.p[q.p.v] = e.p[q.p.v] || []).push(q.o);
    });
    var out = [];
    map.forEach(function (e) {
      e.kind = kindOf(e);
      if (!e.kind) return;
      if (EXTERNAL.some(function (rx) { return rx.test(e.iri); })) return;   // references to external vocabularies
      out.push(e);
    });
    return out;
  }

  function runChecks(quads, opts) {
    var bases = (opts && opts.bases && opts.bases.length) ? opts.bases : ['https://www.insperity.com/'];
    var entities = buildEntities(quads);
    var defined = new Set(entities.map(function (e) { return e.iri; }));
    var assets = entities.filter(function (e) { return e.kind === 'ontology' || e.kind === 'scheme'; })
      .map(function (e) { return e.iri.replace(/[\/#]?$/, e.iri.slice(-1) === '#' ? '#' : '/'); });
    var R = rules({ bases: bases, policy: opts && opts.policy ? (opts.policy.orgs ? opts.policy : policyFrom(opts.policy)) : null,
                    defined: defined, assets: assets,
                    vocab: opts && opts.vocab ? (opts.vocab instanceof Set ? opts.vocab : new Set(opts.vocab)) : null }), findings = [], summary = [];
    R.forEach(function (r) {
      var checked = 0, failed = 0;
      entities.forEach(function (e) {
        if (!r.applies(e)) return;
        checked++;
        var msg = r.check(e);
        if (msg) { failed++; findings.push({ rule: r.id, sev: r.sev, sec: r.sec, iri: e.iri, kind: e.kind, label: anyLabel(e), detail: msg }); }
      });
      summary.push({ id: r.id, sec: r.sec, sev: r.sev, title: r.title, desc: r.desc, checked: checked, failed: failed });
    });
    var g = graphRule(entities);
    g.findings.forEach(function (f) { findings.push({ rule: g.rule.id, sev: g.rule.sev, sec: g.rule.sec, iri: f.iri, kind: f.kind, label: '', detail: f.detail }); });
    summary.push(Object.assign({}, g.rule, { checked: g.checked, failed: g.findings.length }));
    var kinds = {}; entities.forEach(function (e) { kinds[e.kind] = (kinds[e.kind] || 0) + 1; });
    return { rules: summary, findings: findings, stats: { entities: entities.length, kinds: kinds, triples: quads.length } };
  }

  root.KE_RULES = { runChecks: runChecks, PREDICATES: PREDICATES, KIND_LABEL: KIND_LABEL, localName: localName,
                    policyFrom: policyFrom, acronymsIn: acronymsIn, orgHit: orgHit, expansionFor: expansionFor,
                    expandLabel: expandLabel, genericText: genericText, sentenceCase: sentenceCase, REF_PREDICATES: REF_PREDICATES,
                    SUBJECT_PREDS: SUBJECT_PREDS, P: P };
  if (typeof module !== 'undefined') module.exports = root.KE_RULES;
})(typeof window !== 'undefined' ? window : globalThis);
