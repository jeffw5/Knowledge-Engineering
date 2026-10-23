/* ==========================================================================
   KE Workbench — Customer 360 data layer.
   Reads and writes the Customer 360 knowledge graph in GraphDB (through the
   proxy, via KE_SPARQL): client personas, jobs, job steps, desired outcomes,
   appreciative inquiry interviews, SME reviews and decisions, survey waves and
   scores, outcome requirements, gateway evaluations and demand items.
   Model: data/customer-360/<release>/ (ontology/jobs-to-be-done/ extends core).
   Every tool in the Customer 360 group loads this file after ke-sparql.js.
   ========================================================================== */
(function () {
  'use strict';
  var RELEASE = '0.2.0';
  var B = 'https://www.insperity.com/';
  var XSD = 'http://www.w3.org/2001/XMLSchema#';
  var NS = {
    jtbd: B + 'ontology/jobs-to-be-done/', rg: B + 'ontology/requirements-gateway/',
    ob: B + 'resource/outcome-benchmark/', rgr: B + 'resource/requirements-gateway/',
    core: B + 'ontology/core/', theme: B + 'vocabulary/benchmark-theme/', metric: B + 'vocabulary/outcome-metric-type/',
    verdict: B + 'vocabulary/review-verdict/', flag: B + 'vocabulary/review-flag/', use: B + 'vocabulary/approved-use/',
    result: B + 'vocabulary/review-decision-result/', segment: B + 'vocabulary/survey-segment/',
    action: B + 'vocabulary/outcome-action/', phase: B + 'vocabulary/inquiry-phase/', check: B + 'vocabulary/gateway-check/',
    demand: B + 'vocabulary/demand-status/', hr: 'http://example.org/hrservices/ddd#',
    prov: 'http://www.w3.org/ns/prov#', xsd: XSD, skos: 'http://www.w3.org/2004/02/skos/core#',
    rdfs: 'http://www.w3.org/2000/01/rdf-schema#', rdf: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    owl: 'http://www.w3.org/2002/07/owl#', dct: 'http://purl.org/dc/terms/'
  };
  var PX = ['jtbd', 'rg', 'ob', 'rgr', 'core', 'theme', 'metric', 'verdict', 'flag', 'use', 'result', 'segment', 'action', 'phase', 'check', 'demand', 'hr', 'prov', 'xsd']
    .map(function (k) { return 'PREFIX ' + k + ': <' + NS[k] + '>'; }).join('\n') + '\n';
  var GB = B + 'graph/outcome-benchmark/';
  var G = {
    reviews: GB + 'reviews', decisions: GB + 'review-decisions',
    interview: function (key) { return GB + 'interview/' + key; },
    wave: function (key) { return GB + 'survey-wave/' + key; },
    requirements: B + 'graph/requirements-gateway/requirements',
    demand: B + 'graph/demand-planning/demand-items'
  };
  var DATA_DIR = '../data/customer-360/' + RELEASE + '/';

  /* ---- controlled vocabularies (codes the pages use ↔ concept local names) ---- */
  var CODES = {
    verdict: { approve: 'approve', edits: 'approve-with-edits', discuss: 'needs-discussion', reject: 'reject' },
    flag: { regulated: 'regulated-topic', legal: 'legal-advice', tax: 'tax-advice', privacy: 'privacy-sensitivity',
            substantiate: 'needs-substantiation', bias: 'bias-risk', coemploy: 'co-employment-unclear' },
    use: { survey: 'survey-instrument', sales: 'internal-sales-guidance', marketing: 'external-marketing-claims' },
    result: { accepted: 'accepted', dropped: 'dropped' },
    segment: { PEO: 'provider-clients', NONPEO: 'non-clients', TOTAL: 'total-market' },
    action: { fix: 'fix', inn: 'innovate', pro: 'protect', sim: 'simplify', keep: 'maintain' },
    phase: { discover: 'discover', dream: 'dream', design: 'design', destiny: 'destiny' },
    check: { accepted: 'review-accepted', use: 'use-approved', measured: 'measured', k5: 'privacy-threshold',
             material: 'material-opportunity', owner: 'owner-assigned', flags: 'flags-resolved', dup: 'not-duplicate' },
    demand: { submitted: 'submitted', triaged: 'triaged', planned: 'planned', 'in-delivery': 'in-delivery',
              delivered: 'delivered', remeasured: 'remeasured', declined: 'declined' }
  };
  function codeOf(kind, iri) {
    var local = String(iri || '').slice(NS[kind].length), m = CODES[kind];
    for (var k in m) if (m[k] === local) return k;
    return local || null;
  }
  function conceptOf(kind, code) { return NS[kind] + (CODES[kind][code] || code); }
  var METRIC_NAME = { speed: 'Speed', stability: 'Stability', 'cost-and-exposure': 'Cost & exposure', effort: 'Effort', output: 'Output' };

  /* ---- small helpers ---- */
  var KS = function () { if (!window.KE_SPARQL) throw new Error('ke-sparql.js must load before ke-c360.js'); return window.KE_SPARQL; };
  /* proxy.py can drop a connection when many queries arrive at once: retry network failures (not query errors) twice */
  async function retry(fn) {
    for (var i = 0; ; i++) {
      try { return await fn(); }
      catch (e) { if (i >= 2 || !(e instanceof TypeError)) throw e; await new Promise(function (r) { setTimeout(r, 250 * (i + 1)); }); }
    }
  }
  function sel(q) { return retry(function () { return KS().select(PX + q); }); }
  function upd(u) { return retry(function () { return KS().update(PX + u); }); }
  function local(iri) { var s = String(iri || ''); var i = Math.max(s.lastIndexOf('/'), s.lastIndexOf('#')); return s.slice(i + 1); }
  function slug(s) { return String(s || '').toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'x'; }
  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function nowIso() { return new Date().toISOString().replace(/\.\d+Z$/, 'Z'); }
  function today() { return new Date().toISOString().slice(0, 10); }
  function uid(n) { var a = 'abcdefghjkmnpqrstuvwxyz23456789', s = ''; for (var i = 0; i < (n || 5); i++) s += a[Math.floor(Math.random() * a.length)]; return s; }
  function lcFirst(s) { return s ? s[0].toLowerCase() + s.slice(1) : s; }
  var ACR = [['FMLA', 'Family and Medical Leave Act'], ['COBRA', 'Consolidated Omnibus Budget Reconciliation Act'],
    ['OSHA', 'Occupational Safety and Health Administration'], ['EEOC', 'Equal Employment Opportunity Commission'],
    ['FCRA', 'Fair Credit Reporting Act'], ['FSA', 'flexible spending account'], ['HSA', 'health savings account'],
    ['IRS', 'Internal Revenue Service'], ['CPEO', 'certified professional employer organization'],
    ['PEO', 'professional employer organization'], ['CEO', 'Chief Executive Officer'], ['CFO', 'Chief Financial Officer'],
    ['IT', 'Information Technology'], ['HR', 'human resources'], ['PTO', 'paid time off'], ['ACA', 'Affordable Care Act'],
    ['EPLI', 'employment practices liability insurance'], ['ROI', 'return on investment'], ['KPI', 'key performance indicator']];
  /* Spell acronyms out for a preferred label (§3.2); the original wording stays in altLabel and the statement. */
  function expand(s) {
    var out = String(s || '');
    ACR.forEach(function (a) {
      out = out.replace(new RegExp('\\b' + a[0] + '(s?)\\b(?=(\\s+\\S\\S)?)', 'g'), function (m, pl, next, at) {
        var e = a[1];
        if (next && /^\s+[A-Z][a-z]/.test(next)) e = e.replace(/\b[a-z]/g, function (c) { return c.toUpperCase(); });   // title-case context
        else if (at === 0) e = e[0].toUpperCase() + e.slice(1);                                                       // start of the label
        return e + pl;
      });
    });
    return out.replace(/ & /g, ' and ');
  }

  /* ---- Turtle building (full IRIs, so the same text serves INSERT DATA and a PUT) ---- */
  function I(u) { return '<' + u + '>'; }
  function L(s, lang) { return KS().lit(s, lang === undefined ? 'en' : lang); }
  function Lp(s) { return KS().lit(String(s)); }
  function Ld(s, t) { return KS().lit(String(s)) + '^^<' + XSD + t + '>'; }
  function TB() { var lines = []; return {
    add: function (s, p, o) { if (o === null || o === undefined || o === '') return this; lines.push(s + ' ' + p + ' ' + o + ' .'); return this; },
    text: function () { return lines.join('\n') + '\n'; }, size: function () { return lines.length; } }; }
  var P_ = function (pre, l) { return I(NS[pre] + l); };
  var A = I(NS.rdf + 'type'), LABEL = I(NS.rdfs + 'label'), PREF = I(NS.skos + 'prefLabel'), ALT = I(NS.skos + 'altLabel'),
      DEF = I(NS.skos + 'definition'), CREATED = I(NS.dct + 'created'), MODIFIED = I(NS.dct + 'modified'), STATUS = P_('core', 'hasLifecycleStatus'),
      NAMED = I(NS.owl + 'NamedIndividual');
  function labelTriples(t, s, text) {
    var pref = expand(text);
    t.add(s, LABEL, L(pref)).add(s, PREF, L(pref));
    if (pref !== text) t.add(s, ALT, L(text));
  }

  async function putGraph(graph, turtle) {
    var r = await fetch(KS().endpoint() + '/statements?context=' + encodeURIComponent('<' + graph + '>'), {
      method: 'PUT', headers: { 'Content-Type': 'text/turtle' }, body: turtle });
    if (!r.ok) throw new Error('Saving to GraphDB failed (' + r.status + '): ' + (await r.text()).slice(0, 300));
  }
  async function dropGraph(graph) { await upd('DROP SILENT GRAPH ' + I(graph)); }

  /* ======================================================================
     Connection and release
     ====================================================================== */
  async function status() {
    try {
      var rows = await sel('SELECT (COUNT(DISTINCT ?p) AS ?np) (COUNT(DISTINCT ?o) AS ?no) WHERE { { ?p a jtbd:client-persona } UNION { ?o a jtbd:desired-outcome } }');
      var r = rows[0] || {};
      return { ok: true, loaded: +r.np > 0, personas: +r.np || 0, outcomes: +r.no || 0, repo: KS().repo() };
    } catch (e) { return { ok: false, loaded: false, error: String(e.message || e), repo: KS().repo() }; }
  }
  async function loadRelease(onStep) {
    var man = await (await fetch(DATA_DIR + 'manifest.json', { cache: 'no-store' })).json();
    for (var i = 0; i < man.graphs.length; i++) {
      var g = man.graphs[i]; if (onStep) onStep(i + 1, man.graphs.length, g.title);
      var ttl = await (await fetch(DATA_DIR + g.file, { cache: 'no-store' })).text();
      await putGraph(g.graph, ttl);
    }
    return man;
  }

  /* ======================================================================
     Model: personas, jobs, steps, outcomes, themes, stages, services, waves
     ====================================================================== */
  function firstBy(rows, key) { var m = new Map(); rows.forEach(function (r) { if (!m.has(r[key])) m.set(r[key], r); }); return [...m.values()]; }
  function multi(rows, key, val) { var m = {}; rows.forEach(function (r) { if (r[val]) { (m[r[key]] = m[r[key]] || new Set()).add(r[val]); } }); return m; }
  function stat(iri) { return iri ? local(iri) : 'Draft'; }
  function idSort(a, b) {
    var ka = String(a.id), kb = String(b.id), ra = /^[A-Z]\d/.test(ka) ? 0 : 1, rb = /^[A-Z]\d/.test(kb) ? 0 : 1;
    if (ra !== rb) return ra - rb;
    var pa = ka[0] === 'C' && /^C\d/.test(ka) ? 1 : 0, pb = kb[0] === 'C' && /^C\d/.test(kb) ? 1 : 0;
    if (pa !== pb) return pa - pb;
    return ka.localeCompare(kb, undefined, { numeric: true });
  }

  async function model() {
    var EN = 'FILTER(!BOUND(?x) || LANG(?x) = "" || LANGMATCHES(LANG(?x), "en"))';
    var q = await Promise.all([
      sel('SELECT ?p ?id ?name ?alt ?short ?titles ?context ?buying ?goal ?target ?st ?def WHERE { ?p a jtbd:client-persona ; jtbd:hasIdentifier ?id .' +
          ' OPTIONAL { ?p skos:prefLabel ?name } OPTIONAL { ?p skos:altLabel ?alt } OPTIONAL { ?p jtbd:hasShortName ?short } OPTIONAL { ?p jtbd:hasTypicalTitles ?titles }' +
          ' OPTIONAL { ?p jtbd:hasPersonaContext ?context } OPTIONAL { ?p jtbd:hasBuyingRole ?buying } OPTIONAL { ?p jtbd:hasPersonaGoal ?goal }' +
          ' OPTIONAL { ?p jtbd:hasSurveyTarget ?target } OPTIONAL { ?p core:hasLifecycleStatus ?st } OPTIONAL { ?p skos:definition ?def } } ORDER BY ?id'),
      sel('SELECT ?j ?type ?id ?stmt ?label ?st ?ev ?g ?def WHERE { GRAPH ?g { ?j a ?type ; jtbd:hasIdentifier ?id } ' +
          'VALUES ?type { jtbd:core-functional-job jtbd:consumption-chain-job jtbd:emotional-job jtbd:social-job }' +
          ' OPTIONAL { ?j jtbd:hasJobStatement ?stmt } OPTIONAL { ?j skos:prefLabel ?label } OPTIONAL { ?j core:hasLifecycleStatus ?st }' +
          ' OPTIONAL { ?j jtbd:isEvidencedBy ?ev } OPTIONAL { ?j skos:definition ?def } }'),
      sel('SELECT DISTINCT ?j ?p ?rel WHERE { { ?j jtbd:hasJobExecutor ?p BIND("ex" AS ?rel) } UNION { ?p jtbd:executesJob ?j BIND("ex" AS ?rel) }' +
          ' UNION { ?j jtbd:hasJobParticipant ?p BIND("part" AS ?rel) } UNION { ?p jtbd:participatesInJob ?j BIND("part" AS ?rel) } }'),
      sel('SELECT ?s ?j ?id ?label ?stage ?order ?st ?ev ?g WHERE { GRAPH ?g { ?s a jtbd:job-step } ?s core:isStepOf ?j .' +
          ' OPTIONAL { ?s jtbd:hasIdentifier ?id } OPTIONAL { ?s skos:prefLabel ?label } OPTIONAL { ?s jtbd:atJobMapStage ?stage }' +
          ' OPTIONAL { ?s jtbd:hasStageOrder ?order } OPTIONAL { ?s core:hasLifecycleStatus ?st } OPTIONAL { ?s jtbd:isEvidencedBy ?ev } }'),
      sel('SELECT ?o ?id ?stmt ?label ?step ?job ?stage ?theme ?metric ?st ?ev ?g ?iq ?sq WHERE { GRAPH ?g { ?o a jtbd:desired-outcome ; jtbd:hasIdentifier ?id }' +
          ' OPTIONAL { ?o jtbd:hasOutcomeStatement ?stmt } OPTIONAL { ?o skos:prefLabel ?label } OPTIONAL { ?o core:outcomeOf ?step }' +
          ' OPTIONAL { ?o jtbd:isOutcomeOfJob ?job } OPTIONAL { ?o jtbd:atJobMapStage ?stage } OPTIONAL { ?o jtbd:hasBenchmarkTheme ?theme }' +
          ' OPTIONAL { ?o jtbd:hasOutcomeMetricType ?metric } OPTIONAL { ?o core:hasLifecycleStatus ?st } OPTIONAL { ?o jtbd:isEvidencedBy ?ev }' +
          ' OPTIONAL { ?o jtbd:hasImportanceQuestion ?iq } OPTIONAL { ?o jtbd:hasSatisfactionQuestion ?sq } }'),
      sel('SELECT ?o ?svc ?label ?dom WHERE { ?o jtbd:isAddressedByService ?svc OPTIONAL { ?svc rdfs:label ?label } OPTIONAL { ?svc dct:isPartOf ?dom } }'),
      sel('SELECT ?j ?d ?label ?n WHERE { ?j jtbd:appliesToBusinessDomain ?d OPTIONAL { ?d rdfs:label ?label } OPTIONAL { ?d skos:notation ?n } }'),
      sel('SELECT ?s ?id ?label ?order ?def WHERE { ?s a jtbd:job-map-stage ; jtbd:hasIdentifier ?id OPTIONAL { ?s skos:prefLabel ?label } OPTIONAL { ?s jtbd:hasStageOrder ?order } OPTIONAL { ?s skos:definition ?def } } ORDER BY ?order'),
      sel('SELECT ?c ?label ?def ?scope WHERE { ?c skos:inScheme <' + NS.theme + '> ; skos:prefLabel ?label OPTIONAL { ?c skos:definition ?def } OPTIONAL { ?c skos:scopeNote ?scope } }'),
      sel('SELECT ?w ?id ?label ?ex ?date ?file ?mod (COUNT(?sc) AS ?n) WHERE { ?w a jtbd:survey-wave ; jtbd:hasIdentifier ?id OPTIONAL { ?w jtbd:hasWaveLabel ?label }' +
          ' OPTIONAL { ?w jtbd:isExampleData ?ex } OPTIONAL { ?w jtbd:hasFieldedDate ?date } OPTIONAL { ?w jtbd:hasSourceFileName ?file } OPTIONAL { ?w dct:modified ?mod }' +
          ' OPTIONAL { ?sc jtbd:inSurveyWave ?w } } GROUP BY ?w ?id ?label ?ex ?date ?file ?mod ORDER BY DESC(?date)')
    ]);
    void EN;
    var M = { release: RELEASE, byIri: {}, P: {}, J: {}, O: {}, STAGE: {}, THEME: {}, SVC: {}, DOM: {} };

    M.stages = q[7].map(function (r, i) {
      var desc = (r.def || '').replace(/^A job map stage in which the job executor works to /, '').replace(/\.$/, '');
      return { id: r.id, iri: r.s, name: r.label || r.id, desc: desc ? desc[0].toUpperCase() + desc.slice(1) : '', n: +(r.order || i + 1) };
    });
    M.stages.forEach(function (s) { M.STAGE[s.id] = s; M.byIri[s.iri] = s; });

    M.themes = firstBy(q[8], 'c').map(function (r) {
      return { name: r.label, iri: r.c, local: local(r.c), desc: (r.def || '').replace(/^A benchmark theme covering /, '').replace(/^./, function (c) { return c.toUpperCase(); }), added: !!r.scope };
    }).sort(function (a, b) { return a.added - b.added || THEME_ORDER.indexOf(a.local) - THEME_ORDER.indexOf(b.local); });
    M.themes.forEach(function (t) { M.THEME[t.name] = t; M.byIri[t.iri] = t; });

    M.personas = firstBy(q[0], 'p').map(function (r) {
      var alts = q[0].filter(function (x) { return x.p === r.p && x.alt; }).map(function (x) { return x.alt; });
      return { id: r.id, iri: r.p, name: r.name || r.id, short: r.short || r.id, alts: [...new Set(alts)], titles: r.titles || '', context: r.context || '',
               buying: r.buying || '', goal: r.goal || '', target: +(r.target || 0), status: stat(r.st), def: r.def || '', emotional: [], emoJobs: [] };
    });
    M.personas.forEach(function (p) { M.P[p.id] = p; M.byIri[p.iri] = p; });

    var KIND = { 'core-functional-job': 'core', 'consumption-chain-job': 'chain', 'emotional-job': 'emotional', 'social-job': 'social' };
    var evJ = multi(q[1], 'j', 'ev');
    M.jobs = firstBy(q[1], 'j').map(function (r) {
      var type = KIND[local(r.type)];
      return { id: r.id, iri: r.j, type: type, kind: type === 'chain' ? 'chain' : 'core', stmt: r.stmt || r.label || r.id, label: r.label || r.stmt,
               def: r.def || '', ex: [], part: [], dom: [], steps: [], out: [], svc: [], status: stat(r.st),
               evidence: [...(evJ[r.j] || [])], captured: !!(evJ[r.j] && evJ[r.j].size), graph: r.g };
    }).sort(idSort);
    M.jobs.forEach(function (j) { M.J[j.id] = j; M.byIri[j.iri] = j; });
    q[2].forEach(function (r) {
      var j = M.byIri[r.j], p = M.byIri[r.p]; if (!j || !p || !j.steps) return;
      var arr = r.rel === 'ex' ? j.ex : j.part; if (arr.indexOf(p.id) < 0) arr.push(p.id);
    });
    M.jobs.forEach(function (j) {
      j.part = j.part.filter(function (x) { return j.ex.indexOf(x) < 0; });
      if (j.type === 'emotional' || j.type === 'social') j.ex.forEach(function (pid) { var p = M.P[pid]; if (p) { p.emotional.push(j.stmt); p.emoJobs.push(j.id); } });
    });

    var evS = multi(q[3], 's', 'ev');
    M.jobSteps = firstBy(q[3], 's').map(function (r) {
      var j = M.byIri[r.j], st = M.byIri[r.stage];
      return { iri: r.s, id: r.id || local(r.s), job: j ? j.id : null, stage: st ? st.id : null, name: r.label || '', order: +(r.order || (st ? st.n : 99)),
               status: stat(r.st), evidence: [...(evS[r.s] || [])], captured: !!(evS[r.s] && evS[r.s].size), out: [], graph: r.g };
    });
    M.jobSteps.forEach(function (s) { M.byIri[s.iri] = s; var j = M.J[s.job]; if (j) j.steps.push(s); });
    M.jobs.forEach(function (j) { j.steps.sort(function (a, b) { return a.order - b.order || a.captured - b.captured; }); });

    var evO = multi(q[4], 'o', 'ev'), themeOf = {}, metricOf = {};
    q[4].forEach(function (r) { if (r.theme) themeOf[r.o] = r.theme; if (r.metric) metricOf[r.o] = r.metric; });
    M.outcomes = firstBy(q[4], 'o').map(function (r) {
      var step = M.byIri[r.step], job = M.byIri[r.job] || (step && M.J[step.job]), stage = M.byIri[r.stage] || (step && M.STAGE[step.stage]);
      var th = M.byIri[themeOf[r.o]], mt = metricOf[r.o];
      return { id: r.id, iri: r.o, job: job ? job.id : null, step: stage ? stage.id : null, stepIri: r.step || null, t: r.stmt || r.label, label: r.label,
               svc: [], theme: th ? th.name : '', m: mt ? (METRIC_NAME[local(mt)] || local(mt)) : '', status: stat(r.st),
               evidence: [...(evO[r.o] || [])], captured: !!(evO[r.o] && evO[r.o].size), graph: r.g, iq: r.iq || '', sq: r.sq || '' };
    }).sort(idSort);
    M.outcomes.forEach(function (o) {
      M.O[o.id] = o; M.byIri[o.iri] = o;
      var j = M.J[o.job]; if (j) j.out.push(o.id);
      var s = M.byIri[o.stepIri]; if (s && s.out) s.out.push(o.id);
    });

    q[5].forEach(function (r) {
      var o = M.byIri[r.o]; if (!o) return; var id = local(r.svc);
      if (!M.SVC[id]) { M.SVC[id] = { id: id, iri: r.svc, label: r.label || id, dom: r.dom ? local(r.dom) : '' }; }
      if (o.svc.indexOf(id) < 0) o.svc.push(id);
      var j = M.J[o.job]; if (j && j.svc.indexOf(id) < 0) j.svc.push(id);
    });
    M.services = Object.values(M.SVC);
    q[6].forEach(function (r) {
      var j = M.byIri[r.j], id = local(r.d); if (!M.DOM[id]) M.DOM[id] = { id: id, iri: r.d, label: r.label || id, n: +(r.n || 0) };
      if (j && j.dom.indexOf(id) < 0) j.dom.push(id);
    });
    M.domains = Object.values(M.DOM).sort(function (a, b) { return a.n - b.n; });
    M.jobs.forEach(function (j) { j.svc.sort(); });

    M.waves = q[9].map(function (r) {
      return { iri: r.w, id: r.id, label: r.label || r.id, example: r.ex === 'true', date: r.date || '', file: r.file || '', n: +(r.n || 0), modified: r.mod || '' };
    });
    return M;
  }
  var THEME_ORDER = ['payroll', 'benefits', 'human-resources-compliance', 'talent-management', 'training', 'coaching', 'monitoring', 'measurement', 'values-stewardship',
                     'professional-employer-organization-relationship', 'human-resources-technology-and-data'];

  /* ======================================================================
     Survey waves and scores
     ====================================================================== */
  function pickWave(M, preferred) {
    var want = preferred || lsGet('ke-c360-wave', '');
    var w = M.waves.find(function (x) { return x.iri === want && x.n > 0; });
    return w || M.waves.find(function (x) { return !x.example && x.n > 0; }) || M.waves.find(function (x) { return x.n > 0; }) || null;
  }
  function setWave(iri) { lsSet('ke-c360-wave', iri || ''); }
  async function scores(waveIri) {
    var R = { PEO: {}, NONPEO: {}, TOTAL: {} };
    if (!waveIri) return R;
    var rows = await sel('SELECT ?oid ?seg ?imp ?sat ?n WHERE { ?sc jtbd:inSurveyWave <' + waveIri + '> ; core:measures ?o ; jtbd:hasSurveySegment ?seg ;' +
      ' jtbd:hasImportanceScore ?imp ; jtbd:hasSatisfactionScore ?sat . OPTIONAL { ?sc jtbd:hasRespondentCount ?n } ?o jtbd:hasIdentifier ?oid }');
    rows.forEach(function (r) { var s = codeOf('segment', r.seg); if (R[s]) R[s][r.oid] = [+r.imp, +r.sat, +(r.n || 0)]; });
    return R;
  }
  /* rows: [{oid, segment:'PEO'|'NONPEO'|'TOTAL', imp, sat, n}] */
  async function saveWave(wave, rows, M) {
    var key = wave.id || ('wave-' + today() + '-' + uid(4)), g = G.wave(key), w = I(NS.ob + 'SurveyWave-' + slug(key));
    var t = TB();
    t.add(w, A, NAMED).add(w, A, P_('jtbd', 'survey-wave'));
    labelTriples(t, w, wave.label || ('Survey wave ' + key));
    t.add(w, DEF, L('A survey wave of the outcome benchmark, loaded from a results file.'))
     .add(w, P_('jtbd', 'hasIdentifier'), Lp(key)).add(w, P_('jtbd', 'hasWaveLabel'), L(wave.label || key))
     .add(w, P_('jtbd', 'isExampleData'), Ld(!!wave.example, 'boolean')).add(w, P_('jtbd', 'hasFieldedDate'), Ld(wave.date || today(), 'date'))
     .add(w, P_('jtbd', 'hasSourceFileName'), wave.file ? Lp(wave.file) : null)
     .add(w, STATUS, P_('core', 'Draft')).add(w, CREATED, Ld(today(), 'date')).add(w, MODIFIED, Ld(nowIso(), 'dateTime'));
    var segId = { PEO: 'clients', NONPEO: 'non-clients', TOTAL: 'total' }, miss = 0;
    rows.forEach(function (r) {
      var o = M.O[r.oid]; if (!o) { miss++; return; }
      var sc = I(NS.ob + 'Score-' + slug(key) + '-' + r.oid + '-' + segId[r.segment]);
      t.add(sc, A, NAMED).add(sc, A, P_('jtbd', 'outcome-score')).add(sc, P_('core', 'measures'), I(o.iri)).add(sc, P_('jtbd', 'inSurveyWave'), w)
       .add(sc, P_('jtbd', 'hasSurveySegment'), I(conceptOf('segment', r.segment)))
       .add(sc, P_('jtbd', 'hasImportanceScore'), Ld(r.imp, 'decimal')).add(sc, P_('jtbd', 'hasSatisfactionScore'), Ld(r.sat, 'decimal'))
       .add(sc, P_('jtbd', 'hasRespondentCount'), Ld(Math.round(r.n || 0), 'integer'));
    });
    await putGraph(g, t.text());
    return { iri: NS.ob + 'SurveyWave-' + slug(key), graph: g, unknown: miss };
  }

  /* ======================================================================
     Analysis shared by Job Study, Playbook and Requirements Gateway
     ====================================================================== */
  var opp = function (v) { return +(v[0] + Math.max(v[0] - v[1], 0)).toFixed(1); };
  var ciOf = function (v) { var n = v[2] || 1, pI = v[0] / 10, pS = v[1] / 10, vI = pI * (1 - pI) / n * 100, vS = pS * (1 - pS) / n * 100; return 1.96 * Math.sqrt(v[0] > v[1] ? 4 * vI + vS : vI); };
  /* Classify every outcome with scores for both segments: fix / inn / pro / sim / keep (Playbook chapter 2 rules). */
  function analyze(M, R) {
    return M.outcomes.filter(function (o) { return R.PEO[o.id] && R.NONPEO[o.id]; }).map(function (o) {
      var a = R.PEO[o.id], b = R.NONPEO[o.id], oa = opp(a), ob = opp(b), g = +Math.sqrt(Math.pow(ciOf(a), 2) + Math.pow(ciOf(b), 2)).toFixed(1);
      var d = +(oa - ob).toFixed(1), act = 'keep';
      if (a[1] > a[0]) act = 'sim'; else if (oa >= 12 && d >= g) act = 'fix'; else if (oa >= 12 && ob >= 12) act = 'inn'; else if (ob >= 12 && -d >= g) act = 'pro';
      var j = M.J[o.job] || { ex: [] };
      return Object.assign({}, o, { peo: a, non: b, oP: oa, oN: ob, gap: d, ci: g, sig: Math.abs(d) >= g, act: act, ex: j.ex });
    });
  }

  /* Survey modules: each persona rates the outcomes of the jobs it executes; split above 80 items (benchmark design). */
  function modules(M, outIds) {
    var MAXI = 80, out = [], has = outIds ? new Set(outIds) : null;
    M.personas.forEach(function (p) {
      var js = M.jobs.filter(function (j) { return (j.type === 'core' || j.type === 'chain') && j.ex.indexOf(p.id) >= 0; })
        .map(function (j) { return { id: j.id, n: j.out.filter(function (o) { return !has || has.has(o); }).length }; }).filter(function (j) { return j.n; });
      if (!js.length) return;
      var total = js.reduce(function (a, j) { return a + j.n; }, 0), nmod = Math.max(1, Math.ceil(total / MAXI)), bins = [];
      for (var i = 0; i < nmod; i++) bins.push([]);
      js.sort(function (a, b) { return b.n - a.n; }).forEach(function (j) {
        var b = bins.reduce(function (m, x) { return x.reduce(function (s, y) { return s + y.n; }, 0) < m.reduce(function (s, y) { return s + y.n; }, 0) ? x : m; }, bins[0]); b.push(j); });
      bins.forEach(function (b, i) {
        var items = b.reduce(function (s, y) { return s + y.n; }, 0), n = p.target || 100;
        out.push({ persona: p.id, name: p.short + (nmod > 1 ? ' ' + String.fromCharCode(65 + i) : ''), jobs: b.map(function (x) { return x.id; }).sort(),
                   items: items, minutes: Math.round(items * 2 * 6 / 60 + 4), n: n,
                   ci: +(1.96 * Math.sqrt(125 / n)).toFixed(1), ci_cell: +(1.96 * Math.sqrt(125 / (n / 2))).toFixed(1) });
      });
    });
    return out;
  }

  /* The benchmark's own data shape (window.PEO in the original pages), restricted to outcomes scored in R
     and not dropped in review. */
  function benchmarkShape(M, R, dropped) {
    var drop = dropped || new Set();
    var outs = M.outcomes.filter(function (o) { return R.PEO[o.id] && R.NONPEO[o.id] && !drop.has(o.id) && o.job && o.step; });
    var keep = new Set(outs.map(function (o) { return o.id; }));
    var jobs = M.jobs.filter(function (j) { return (j.type === 'core' || j.type === 'chain') && j.out.some(function (o) { return keep.has(o); }); })
      .map(function (j) { return { id: j.id, kind: j.kind, stmt: j.stmt, dom: j.dom.slice(), ex: j.ex.slice(), part: j.part.slice(),
        out: j.out.filter(function (o) { return keep.has(o); }), svc: [...new Set(outs.filter(function (o) { return o.job === j.id; }).flatMap(function (o) { return o.svc; }))].sort() }; });
    return {
      steps: M.stages.map(function (s) { return { id: s.id, name: s.name, desc: s.desc }; }),
      personas: M.personas.map(function (p) { return { id: p.id, name: p.name, short: p.short, titles: p.titles, context: p.context, buying: p.buying, goal: p.goal, emotional: p.emotional.slice() }; }),
      jobs: jobs,
      outcomes: outs.map(function (o) { return { id: o.id, job: o.job, step: o.step, t: o.t, svc: o.svc.slice(), theme: o.theme, m: o.m }; }),
      services: M.services.map(function (s) { var d = M.DOM[s.dom]; return { id: s.id, label: s.label, dom: s.dom, sub: '', subLabel: d ? d.label : '', theme: '' }; }),
      domains: M.domains.map(function (d) { return { id: d.id, label: d.label, n: d.n }; }),
      themes: M.themes.map(function (t) { return { name: t.name, added: t.added, sl: '', desc: t.desc }; }),
      modules: modules(M, [...keep]),
      example: { PEO: R.PEO, NONPEO: R.NONPEO, TOTAL: R.TOTAL }
    };
  }

  /* ======================================================================
     Reviews and decisions
     ====================================================================== */
  function itemIri(M, id) { var x = M.P[id] || M.J[id] || M.O[id]; return x ? x.iri : NS.ob + 'Item-' + slug(id); }
  async function reviews(M) {
    var rows = await sel('SELECT ?r ?elid ?name ?role ?verdict ?wording ?comment ?keep ?dup ?stage ?theme ?at ' +
      '(GROUP_CONCAT(DISTINCT STR(?f); separator=" ") AS ?flags) (GROUP_CONCAT(DISTINCT STR(?u); separator=" ") AS ?uses) WHERE {' +
      ' GRAPH <' + G.reviews + '> { ?r a jtbd:subject-matter-review ; jtbd:reviewsElement ?el ; jtbd:hasReviewerName ?name ; jtbd:hasReviewerRole ?role .' +
      ' OPTIONAL { ?r jtbd:hasReviewVerdict ?verdict } OPTIONAL { ?r jtbd:hasSuggestedWording ?wording } OPTIONAL { ?r jtbd:hasReviewComment ?comment }' +
      ' OPTIONAL { ?r jtbd:hasStudyRecommendation ?keep } OPTIONAL { ?r jtbd:hasDuplicateOf ?dup } OPTIONAL { ?r jtbd:hasSuggestedStage ?stage }' +
      ' OPTIONAL { ?r jtbd:hasSuggestedTheme ?theme } OPTIONAL { ?r jtbd:hasRecordedAt ?at } OPTIONAL { ?r jtbd:raisesFlag ?f } OPTIONAL { ?r jtbd:approvesUse ?u } }' +
      ' ?el jtbd:hasIdentifier ?elid } GROUP BY ?r ?elid ?name ?role ?verdict ?wording ?comment ?keep ?dup ?stage ?theme ?at');
    var out = {}, stageIds = {}, themeNames = {};
    rows.forEach(function (r) {
      var rv = { name: r.name, role: r.role, verdict: codeOf('verdict', r.verdict), wording: r.wording || '', comment: r.comment || '',
                 keep: r.keep || '', merge: r.dup || '', step: r.stage && M && M.byIri[r.stage] ? M.byIri[r.stage].id : '', themeIri: r.theme || '',
                 theme: r.theme && M && M.byIri[r.theme] ? M.byIri[r.theme].name : '',
                 flags: (r.flags || '').split(' ').filter(Boolean).map(function (x) { return codeOf('flag', x); }),
                 uses: (r.uses || '').split(' ').filter(Boolean).map(function (x) { return codeOf('use', x); }),
                 at: r.at ? Date.parse(r.at) : 0 };
      (out[r.elid] = out[r.elid] || {})[slug(r.name)] = rv;
    });
    void stageIds; void themeNames;
    return out;
  }
  async function saveReview(M, itemId, rv) {
    var r = I(NS.ob + 'Review-' + slug(itemId) + '-' + slug(rv.name)), t = TB();
    t.add(r, A, NAMED).add(r, A, P_('jtbd', 'subject-matter-review'))
     .add(r, LABEL, L((rv.role === 'compliance' ? 'Compliance' : 'Business') + ' review of ' + itemId + ' by ' + rv.name))
     .add(r, P_('jtbd', 'reviewsElement'), I(itemIri(M, itemId))).add(r, P_('jtbd', 'hasReviewerName'), Lp(rv.name))
     .add(r, P_('jtbd', 'hasReviewerRole'), Lp(rv.role)).add(r, P_('jtbd', 'hasReviewVerdict'), rv.verdict ? I(conceptOf('verdict', rv.verdict)) : null)
     .add(r, P_('jtbd', 'hasSuggestedWording'), rv.wording ? L(rv.wording) : null).add(r, P_('jtbd', 'hasReviewComment'), rv.comment ? L(rv.comment) : null)
     .add(r, P_('jtbd', 'hasStudyRecommendation'), rv.keep ? Lp(rv.keep) : null).add(r, P_('jtbd', 'hasDuplicateOf'), rv.merge ? Lp(rv.merge) : null)
     .add(r, P_('jtbd', 'hasSuggestedStage'), rv.step && M.STAGE[rv.step] ? I(M.STAGE[rv.step].iri) : null)
     .add(r, P_('jtbd', 'hasSuggestedTheme'), rv.theme && M.THEME[rv.theme] ? I(M.THEME[rv.theme].iri) : null)
     .add(r, P_('jtbd', 'hasRecordedAt'), Ld(nowIso(), 'dateTime'));
    (rv.flags || []).forEach(function (f) { t.add(r, P_('jtbd', 'raisesFlag'), I(conceptOf('flag', f))); });
    (rv.uses || []).forEach(function (u) { t.add(r, P_('jtbd', 'approvesUse'), I(conceptOf('use', u))); });
    await upd('DELETE WHERE { GRAPH <' + G.reviews + '> { ' + r + ' ?p ?o } } ;\nINSERT DATA { GRAPH <' + G.reviews + '> {\n' + t.text() + '} }');
  }
  async function decisions() {
    var rows = await sel('SELECT ?d ?elid ?res ?wording ?note ?by ?at (GROUP_CONCAT(DISTINCT STR(?u); separator=" ") AS ?uses) WHERE {' +
      ' GRAPH <' + G.decisions + '> { ?d a jtbd:review-decision ; jtbd:decidesElement ?el ; jtbd:hasDecisionResult ?res .' +
      ' OPTIONAL { ?d jtbd:hasSuggestedWording ?wording } OPTIONAL { ?d jtbd:hasReviewComment ?note } OPTIONAL { ?d jtbd:hasReviewerName ?by }' +
      ' OPTIONAL { ?d jtbd:hasRecordedAt ?at } OPTIONAL { ?d jtbd:approvesUse ?u } } ?el jtbd:hasIdentifier ?elid }' +
      ' GROUP BY ?d ?elid ?res ?wording ?note ?by ?at');
    var out = {};
    rows.forEach(function (r) {
      out[r.elid] = { status: codeOf('result', r.res), wording: r.wording || '', note: r.note || '', by: r.by || '', at: r.at ? Date.parse(r.at) : 0,
                      uses: (r.uses || '').split(' ').filter(Boolean).map(function (x) { return codeOf('use', x); }), item: r.elid };
    });
    return out;
  }
  async function saveDecision(M, itemId, d) {
    var s = I(NS.ob + 'Decision-' + slug(itemId));
    var del = 'DELETE WHERE { GRAPH <' + G.decisions + '> { ' + s + ' ?p ?o } }';
    if (!d || d.status === 'open') { await upd(del); return; }
    var t = TB();
    t.add(s, A, NAMED).add(s, A, P_('jtbd', 'review-decision'))
     .add(s, LABEL, L((d.status === 'accepted' ? 'Accepted' : 'Dropped') + ': ' + itemId))
     .add(s, P_('jtbd', 'decidesElement'), I(itemIri(M, itemId))).add(s, P_('jtbd', 'hasDecisionResult'), I(conceptOf('result', d.status)))
     .add(s, P_('jtbd', 'hasSuggestedWording'), d.wording ? L(d.wording) : null).add(s, P_('jtbd', 'hasReviewComment'), d.note ? L(d.note) : null)
     .add(s, P_('jtbd', 'hasReviewerName'), d.by ? Lp(d.by) : null).add(s, P_('jtbd', 'hasRecordedAt'), Ld(nowIso(), 'dateTime'));
    (d.uses || []).forEach(function (u) { t.add(s, P_('jtbd', 'approvesUse'), I(conceptOf('use', u))); });
    await upd(del + ' ;\nINSERT DATA { GRAPH <' + G.decisions + '> {\n' + t.text() + '} }');
  }
  function reviewer() {
    try { return JSON.parse(lsGet('ke-c360-reviewer', '{}')) || {}; } catch (e) { return {}; }
  }
  function setReviewer(r) { lsSet('ke-c360-reviewer', JSON.stringify(r || {})); }

  /* ======================================================================
     Appreciative inquiry interviews (one named graph each)
     ====================================================================== */
  async function interviews() {
    var rows = await sel('SELECT ?i ?g ?id ?pid ?date ?who ?role ?size ?industry ?model ?summary ?mod ' +
      '(COUNT(DISTINCT ?n) AS ?notes) (COUNT(DISTINCT ?j) AS ?jobs) (COUNT(DISTINCT ?s) AS ?steps) (COUNT(DISTINCT ?o) AS ?outs) WHERE {' +
      ' GRAPH ?g { ?i a jtbd:appreciative-inquiry-interview ; jtbd:hasIdentifier ?id .' +
      ' OPTIONAL { ?i jtbd:hasInterviewDate ?date } OPTIONAL { ?i jtbd:hasInterviewerName ?who }' +
      ' OPTIONAL { ?i jtbd:hasIntervieweeRole ?role } OPTIONAL { ?i jtbd:hasCompanySizeBand ?size } OPTIONAL { ?i jtbd:hasIndustry ?industry }' +
      ' OPTIONAL { ?i jtbd:hasCurrentServiceModel ?model } OPTIONAL { ?i jtbd:hasInterviewSummary ?summary } OPTIONAL { ?i dct:modified ?mod }' +
      ' OPTIONAL { ?n jtbd:isNoteOf ?i } OPTIONAL { ?j a ?jt FILTER(?jt IN (jtbd:core-functional-job, jtbd:consumption-chain-job, jtbd:emotional-job, jtbd:social-job)) }' +
      ' OPTIONAL { ?s a jtbd:job-step } OPTIONAL { ?o a jtbd:desired-outcome } }' +
      ' OPTIONAL { ?i jtbd:interviewsPersona ?pp . ?pp jtbd:hasIdentifier ?pid } } GROUP BY ?i ?g ?id ?pid ?date ?who ?role ?size ?industry ?model ?summary ?mod ORDER BY DESC(?date) DESC(?mod)');
    return rows.map(function (r) {
      return { iri: r.i, graph: r.g, id: r.id, key: r.g.slice((GB + 'interview/').length), persona: r.pid || '', date: r.date || '', interviewer: r.who || '',
               role: r.role || '', size: r.size || '', industry: r.industry || '', model: r.model || '', summary: r.summary || '', modified: r.mod || '',
               counts: { notes: +r.notes, jobs: +r.jobs, steps: +r.steps, outcomes: +r.outs } };
    });
  }
  /* Read one interview graph back into the editor's shape. */
  async function interview(M, key) {
    var g = G.interview(key);
    var rows = await sel('SELECT ?s ?p ?o WHERE { GRAPH <' + g + '> { ?s ?p ?o } }');
    var subj = {};
    rows.forEach(function (r) { var e = subj[r.s] = subj[r.s] || {}; (e[r.p] = e[r.p] || []).push(r.o); });
    var v = function (e, pre, l) { return e && e[NS[pre] + l] ? e[NS[pre] + l][0] : ''; };
    var vs = function (e, pre, l) { return e && e[NS[pre] + l] ? e[NS[pre] + l] : []; };
    var types = function (e) { return (e[NS.rdf + 'type'] || []).map(local); };
    var it = { key: key, graph: g, notes: [], jobs: [], steps: [], outcomes: [] }, iiri = null;
    Object.keys(subj).forEach(function (s) {
      var e = subj[s], ty = types(e);
      if (ty.indexOf('appreciative-inquiry-interview') >= 0) {
        iiri = s; var p = M.byIri[v(e, 'jtbd', 'interviewsPersona')];
        Object.assign(it, { iri: s, id: v(e, 'jtbd', 'hasIdentifier'), persona: p ? p.id : '', date: v(e, 'jtbd', 'hasInterviewDate'),
          interviewer: v(e, 'jtbd', 'hasInterviewerName'), role: v(e, 'jtbd', 'hasIntervieweeRole'), size: v(e, 'jtbd', 'hasCompanySizeBand'),
          industry: v(e, 'jtbd', 'hasIndustry'), model: v(e, 'jtbd', 'hasCurrentServiceModel'), summary: v(e, 'jtbd', 'hasInterviewSummary') });
      }
    });
    Object.keys(subj).forEach(function (s) {
      var e = subj[s], ty = types(e), ref = local(s).split('-').pop(),
          ev = vs(e, 'jtbd', 'isEvidencedBy').filter(function (x) { return /\/Note-/.test(x); }).map(function (x) { return local(x).split('-').pop(); });
      if (ty.indexOf('interview-note') >= 0) {
        it.notes.push({ iri: s, ref: ref, n: +v(e, 'jtbd', 'hasStageOrder') || 0, phase: codeOf('phase', v(e, 'jtbd', 'inInquiryPhase')) || 'discover',
                        text: v(e, 'jtbd', 'hasNoteText'), quote: v(e, 'jtbd', 'isQuote') === 'true' });
      } else if (ty.some(function (x) { return /-job$/.test(x); })) {
        var kind = { 'core-functional-job': 'core', 'consumption-chain-job': 'chain', 'emotional-job': 'emotional', 'social-job': 'social' }[ty.find(function (x) { return /-job$/.test(x); })];
        it.jobs.push({ iri: s, ref: ref, id: v(e, 'jtbd', 'hasIdentifier'), kind: kind, stmt: v(e, 'jtbd', 'hasJobStatement'), evidence: ev });
      } else if (ty.indexOf('job-step') >= 0) {
        var st = M.byIri[v(e, 'jtbd', 'atJobMapStage')];
        it.steps.push({ iri: s, ref: ref, id: v(e, 'jtbd', 'hasIdentifier'), jobIri: v(e, 'core', 'isStepOf'), stage: st ? st.id : 'EXE',
                        name: (e[NS.rdfs + 'label'] || [''])[0], stmt: v(e, 'jtbd', 'hasJobStatement') || (e[NS.skos + 'altLabel'] || e[NS.rdfs + 'label'] || [''])[0], evidence: ev });
      } else if (ty.indexOf('desired-outcome') >= 0) {
        var st2 = M.byIri[v(e, 'jtbd', 'atJobMapStage')], th = M.byIri[v(e, 'jtbd', 'hasBenchmarkTheme')];
        it.outcomes.push({ iri: s, ref: ref, id: v(e, 'jtbd', 'hasIdentifier'), jobIri: v(e, 'jtbd', 'isOutcomeOfJob'), stepIri: v(e, 'core', 'outcomeOf'),
                           stage: st2 ? st2.id : 'EXE', stmt: v(e, 'jtbd', 'hasOutcomeStatement'), metric: local(v(e, 'jtbd', 'hasOutcomeMetricType')) || 'speed',
                           theme: th ? th.name : '', evidence: ev });
      }
    });
    it.notes.sort(function (a, b) { return a.n - b.n; });
    // captured steps keep their human-entered name in hasJobStatement-free form: label is "<Stage>: <name>"
    it.steps.forEach(function (s) { s.name = String(s.name).replace(/^[A-Z][a-z]+: /, ''); });
    var jobRef = {}; it.jobs.forEach(function (j) { jobRef[j.iri] = j.ref; });
    var stepRef = {}; it.steps.forEach(function (s) { stepRef[s.iri] = s.ref; });
    var jobKey = function (iri) { return jobRef[iri] || (M.byIri[iri] ? M.byIri[iri].id : ''); };
    it.steps.forEach(function (s) { s.job = jobKey(s.jobIri); });
    it.outcomes.forEach(function (o) { o.job = jobKey(o.jobIri); o.step = stepRef[o.stepIri] || ''; });
    void iiri;
    return it;
  }
  function newInterviewKey() { return 'ai-' + today().replace(/-/g, '') + '-' + uid(4); }
  /* Write the whole interview graph: the interview, its notes, and every job, job step and desired outcome captured in it. */
  async function saveInterview(M, it) {
    var key = it.key || newInterviewKey(), g = G.interview(key), base = NS.ob, K = slug(key), t = TB();
    var IV = I(base + 'Interview-' + K), p = M.P[it.persona];
    var shortId = key.toUpperCase().replace(/^AI-\d{8}-/, 'AI-');
    t.add(IV, A, NAMED).add(IV, A, P_('jtbd', 'appreciative-inquiry-interview'));
    var title = 'Appreciative inquiry interview with ' + (it.role || 'an interviewee') + (p ? ' (' + p.short + ')' : '') + ', ' + (it.date || today());
    labelTriples(t, IV, title);
    t.add(IV, DEF, L('An appreciative inquiry interview that explores the jobs, job steps and desired outcomes of the ' + (p ? lcFirst(expand(p.name)) : 'client') + ' persona.'))
     .add(IV, P_('jtbd', 'hasIdentifier'), Lp(shortId)).add(IV, P_('jtbd', 'interviewsPersona'), p ? I(p.iri) : null)
     .add(IV, P_('jtbd', 'hasInterviewDate'), Ld(it.date || today(), 'date')).add(IV, P_('jtbd', 'hasInterviewerName'), it.interviewer ? Lp(it.interviewer) : null)
     .add(IV, P_('jtbd', 'hasIntervieweeRole'), it.role ? Lp(it.role) : null).add(IV, P_('jtbd', 'hasCompanySizeBand'), it.size ? Lp(it.size) : null)
     .add(IV, P_('jtbd', 'hasIndustry'), it.industry ? Lp(it.industry) : null).add(IV, P_('jtbd', 'hasCurrentServiceModel'), it.model ? Lp(it.model) : null)
     .add(IV, P_('jtbd', 'hasInterviewSummary'), it.summary ? L(it.summary) : null)
     .add(IV, STATUS, P_('core', 'Draft')).add(IV, CREATED, Ld(it.created || today(), 'date')).add(IV, MODIFIED, Ld(nowIso(), 'dateTime'));
    var noteIri = {};
    (it.notes || []).forEach(function (n, i) {
      if (!String(n.text || '').trim()) return;
      n.ref = n.ref || ('n' + uid(5));
      var N = I(base + 'Note-' + K + '-' + n.ref); noteIri[n.ref] = N; n.iri = N.slice(1, -1);
      t.add(N, A, NAMED).add(N, A, P_('jtbd', 'interview-note')).add(N, LABEL, L((n.quote ? 'Quote' : 'Note') + ' ' + (i + 1) + ' (' + n.phase + ')'))
       .add(N, P_('jtbd', 'hasStageOrder'), Ld(i + 1, 'positiveInteger'))
       .add(N, P_('jtbd', 'isNoteOf'), IV).add(N, P_('jtbd', 'inInquiryPhase'), I(conceptOf('phase', n.phase || 'discover')))
       .add(N, P_('jtbd', 'hasNoteText'), L(n.text)).add(N, P_('jtbd', 'isQuote'), Ld(!!n.quote, 'boolean'));
    });
    function evid(s, ev) {
      var any = false;
      (ev || []).forEach(function (r) { var N = noteIri[r]; if (N) { t.add(s, P_('jtbd', 'isEvidencedBy'), N); any = true; } });
      if (!any) t.add(s, P_('jtbd', 'isEvidencedBy'), IV);
    }
    var KCLS = { core: 'core-functional-job', chain: 'consumption-chain-job', emotional: 'emotional-job', social: 'social-job' };
    var jobIri = {};
    (it.jobs || []).forEach(function (j, i) {
      if (!String(j.stmt || '').trim()) return;
      j.ref = j.ref || ('j' + uid(5));
      var J = I(base + 'Job-' + K + '-' + j.ref), jid = shortId + '-' + j.ref.toUpperCase(); jobIri[j.ref] = J.slice(1, -1); j.iri = J.slice(1, -1); j.id = jid;
      t.add(J, A, NAMED).add(J, A, P_('jtbd', KCLS[j.kind] || 'core-functional-job'));
      labelTriples(t, J, j.stmt);
      var genus = { core: 'A core functional job', chain: 'A consumption chain job', emotional: 'An emotional job', social: 'A social job' }[j.kind] || 'A core functional job';
      t.add(J, DEF, L(genus + ' discovered in interview ' + shortId + ': ' + lcFirst(expand(j.stmt)).replace(/\.$/, '') + '.'))
       .add(J, P_('jtbd', 'hasIdentifier'), Lp(jid)).add(J, P_('jtbd', 'hasJobStatement'), L(j.stmt))
       .add(J, P_('jtbd', 'hasJobExecutor'), p ? I(p.iri) : null).add(J, STATUS, P_('core', 'Draft'))
       .add(J, CREATED, Ld(today(), 'date')).add(J, MODIFIED, Ld(nowIso(), 'dateTime'));
      evid(J, j.evidence);
    });
    function resolveJob(ref) { return jobIri[ref] || (M.J[ref] ? M.J[ref].iri : null); }
    var stepIri = {};
    (it.steps || []).forEach(function (s, i) {
      var jIri = resolveJob(s.job); if (!jIri || !String(s.name || '').trim()) return;
      s.ref = s.ref || ('s' + uid(5));
      var S = I(base + 'Step-' + K + '-' + s.ref), st = M.STAGE[s.stage] || M.stages[4]; stepIri[s.ref] = S.slice(1, -1); s.iri = S.slice(1, -1);
      t.add(S, A, NAMED).add(S, A, P_('jtbd', 'job-step'));
      labelTriples(t, S, st.name + ': ' + s.name);
      t.add(S, DEF, L('A job step discovered in interview ' + shortId + ' in which the executor works to ' + lcFirst(expand(s.name)).replace(/\.$/, '') + '.'))
       .add(S, P_('jtbd', 'hasIdentifier'), Lp(shortId + '-' + s.ref.toUpperCase())).add(S, P_('core', 'isStepOf'), I(jIri))
       .add(S, P_('jtbd', 'atJobMapStage'), I(st.iri)).add(S, P_('jtbd', 'hasStageOrder'), Ld(st.n, 'positiveInteger'))
       .add(S, STATUS, P_('core', 'Draft')).add(S, CREATED, Ld(today(), 'date')).add(S, MODIFIED, Ld(nowIso(), 'dateTime'));
      evid(S, s.evidence);
    });
    (it.outcomes || []).forEach(function (o, i) {
      var jIri = resolveJob(o.job); if (!jIri || !String(o.stmt || '').trim()) return;
      o.ref = o.ref || ('o' + uid(5));
      var O = I(base + 'Outcome-' + K + '-' + o.ref), st = M.STAGE[o.stage] || M.stages[4], oid = shortId + '-' + o.ref.toUpperCase(); o.iri = O.slice(1, -1); o.id = oid;
      var sIri = stepIri[o.step] || (M.J[o.job] ? (M.J[o.job].steps.find(function (x) { return x.stage === st.id && !x.captured; }) || {}).iri : null);
      var jstmt = M.J[o.job] ? M.J[o.job].stmt : ((it.jobs || []).find(function (x) { return x.ref === o.job; }) || {}).stmt || 'get the job done';
      t.add(O, A, NAMED).add(O, A, P_('jtbd', 'desired-outcome'));
      labelTriples(t, O, o.stmt);
      t.add(O, DEF, L('A desired outcome discovered in interview ' + shortId + ' that a client uses, in the ' + st.name.toLowerCase() + ' step, to judge how well they ' + lcFirst(expand(jstmt)).replace(/\.$/, '') + '.'))
       .add(O, P_('jtbd', 'hasIdentifier'), Lp(oid)).add(O, P_('jtbd', 'hasOutcomeStatement'), L(o.stmt))
       .add(O, P_('core', 'outcomeOf'), sIri ? I(sIri) : null).add(O, P_('jtbd', 'isOutcomeOfJob'), I(jIri)).add(O, P_('jtbd', 'atJobMapStage'), I(st.iri))
       .add(O, P_('jtbd', 'hasOutcomeMetricType'), I(NS.metric + (o.metric || 'speed')))
       .add(O, P_('jtbd', 'hasBenchmarkTheme'), o.theme && M.THEME[o.theme] ? I(M.THEME[o.theme].iri) : null)
       .add(O, P_('jtbd', 'hasImportanceQuestion'), L('When you ' + lcFirst(jstmt).replace(/\.$/, '') + ', how important is it to ' + lcFirst(o.stmt).replace(/\.$/, '') + '?'))
       .add(O, P_('jtbd', 'hasSatisfactionQuestion'), L('How satisfied are you with your current ability to ' + lcFirst(o.stmt).replace(/\.$/, '') + '?'))
       .add(O, STATUS, P_('core', 'Draft')).add(O, CREATED, Ld(today(), 'date')).add(O, MODIFIED, Ld(nowIso(), 'dateTime'));
      evid(O, o.evidence);
    });
    await putGraph(g, t.text());
    return { key: key, graph: g, iri: IV.slice(1, -1), id: shortId, triples: t.size() };
  }
  async function deleteInterview(key) { await dropGraph(G.interview(key)); }

  /* ODI outcome statement: direction + metric + object of control + contextual clarifier. */
  var METRIC_PHRASE = { speed: 'the time required to', stability: 'the likelihood that', 'cost-and-exposure': 'the cost of', effort: 'the effort required to', output: 'the number of' };
  function composeOutcome(direction, metric, object, clarifier) {
    var obj = String(object || '').trim().replace(/\.$/, ''); if (!obj) return '';
    var phrase = METRIC_PHRASE[metric] || '';
    if (metric === 'stability' && /^(missing|losing|failing|paying|choosing|setting|filing|being|getting|misclassifying|miscalculating|exceeding|forfeiting)\b/i.test(obj)) phrase = 'the likelihood of';
    if (new RegExp('^' + phrase.replace(/ (to|that|of)$/, ''), 'i').test(obj)) phrase = '';
    var s = (direction || 'Minimize') + ' ' + (phrase ? phrase + ' ' : '') + obj;
    var c = String(clarifier || '').trim().replace(/\.$/, '');
    if (c) {
      c = c.replace(/^,\s*/, '');
      if (/^e\.g\./i.test(c)) s += ', ' + c;
      else if (/^(when|for|during|before|after|across|in|on|so|without|while|under|by|from|to|with|at)\b/i.test(c)) s += ' ' + c;
      else s += ', e.g., ' + c;
    }
    return s;
  }

  /* ======================================================================
     Requirements gateway and demand planning
     ====================================================================== */
  var DEMAND_ORDER = ['submitted', 'triaged', 'planned', 'in-delivery', 'delivered', 'remeasured', 'declined'];
  async function requirements() {
    var rows = await sel('SELECT ?r ?id ?oid ?stmt ?crit ?act ?wave ?theme ?opp ?gap ?ev ?adm ?at ' +
      '(GROUP_CONCAT(DISTINCT STR(?pc); separator=" ") AS ?pass) (GROUP_CONCAT(DISTINCT STR(?fc); separator=" ") AS ?fail) ' +
      '(GROUP_CONCAT(DISTINCT STR(?svc); separator=" ") AS ?svcs) WHERE { GRAPH <' + G.requirements + '> {' +
      ' ?r a rg:outcome-requirement ; jtbd:hasIdentifier ?id ; rg:tracesToOutcome ?o . OPTIONAL { ?r rg:hasRequirementStatement ?stmt }' +
      ' OPTIONAL { ?r rg:hasAcceptanceCriterion ?crit } OPTIONAL { ?r rg:hasRecommendedAction ?act } OPTIONAL { ?r rg:basedOnSurveyWave ?wave }' +
      ' OPTIONAL { ?r rg:isOwnedByTheme ?theme } OPTIONAL { ?r rg:hasOpportunityScore ?opp } OPTIONAL { ?r rg:hasGapToNonClients ?gap }' +
      ' OPTIONAL { ?r rg:isAllocatedToService ?svc }' +
      ' OPTIONAL { ?ev rg:evaluatesRequirement ?r OPTIONAL { ?ev rg:isAdmitted ?adm } OPTIONAL { ?ev jtbd:hasRecordedAt ?at }' +
      ' OPTIONAL { ?ev rg:passesCheck ?pc } OPTIONAL { ?ev rg:failsCheck ?fc } } }' +
      ' ?o jtbd:hasIdentifier ?oid } GROUP BY ?r ?id ?oid ?stmt ?crit ?act ?wave ?theme ?opp ?gap ?ev ?adm ?at');
    return rows.map(function (r) {
      return { iri: r.r, id: r.id, outcome: r.oid, stmt: r.stmt || '', criterion: r.crit || '', action: codeOf('action', r.act), wave: r.wave || '',
               themeIri: r.theme || '', opp: +(r.opp || 0), gap: +(r.gap || 0), admitted: r.adm === 'true', at: r.at ? Date.parse(r.at) : 0,
               pass: (r.pass || '').split(' ').filter(Boolean).map(function (x) { return codeOf('check', x); }),
               fail: (r.fail || '').split(' ').filter(Boolean).map(function (x) { return codeOf('check', x); }),
               services: (r.svcs || '').split(' ').filter(Boolean).map(local) };
    });
  }
  /* req: {outcome, action, wave(iri), waveId, theme(name), opp, gap, stmt, criterion, services[], pass[], fail[], admitted, by} */
  async function saveRequirement(M, req) {
    var o = M.O[req.outcome], wk = slug(req.waveId || local(req.wave)), id = 'REQ-' + req.outcome + '-' + wk;
    var R = I(NS.rgr + 'Requirement-' + slug(req.outcome) + '-' + wk), E = I(NS.rgr + 'Evaluation-' + slug(req.outcome) + '-' + wk), t = TB();
    t.add(R, A, NAMED).add(R, A, P_('rg', 'outcome-requirement'));
    labelTriples(t, R, req.stmt);
    t.add(R, DEF, L('An outcome requirement derived from the measured gap on desired outcome ' + req.outcome + '.'))
     .add(R, P_('jtbd', 'hasIdentifier'), Lp(id)).add(R, P_('rg', 'hasRequirementStatement'), L(req.stmt))
     .add(R, P_('rg', 'hasAcceptanceCriterion'), req.criterion ? L(req.criterion) : null)
     .add(R, P_('rg', 'tracesToOutcome'), I(o.iri)).add(R, P_('rg', 'hasRecommendedAction'), I(conceptOf('action', req.action)))
     .add(R, P_('rg', 'basedOnSurveyWave'), I(req.wave)).add(R, P_('rg', 'isOwnedByTheme'), req.theme && M.THEME[req.theme] ? I(M.THEME[req.theme].iri) : null)
     .add(R, P_('rg', 'hasOpportunityScore'), Ld(req.opp, 'decimal')).add(R, P_('rg', 'hasGapToNonClients'), Ld(req.gap, 'decimal'))
     .add(R, STATUS, P_('core', req.admitted ? 'Candidate' : 'Draft')).add(R, CREATED, Ld(today(), 'date')).add(R, MODIFIED, Ld(nowIso(), 'dateTime'));
    (req.services || []).forEach(function (s) { var sv = M.SVC[s]; if (sv) t.add(R, P_('rg', 'isAllocatedToService'), I(sv.iri)); });
    t.add(E, A, NAMED).add(E, A, P_('rg', 'gateway-evaluation')).add(E, LABEL, L('Gateway evaluation of ' + id))
     .add(E, P_('rg', 'evaluatesRequirement'), R).add(E, P_('rg', 'isAdmitted'), Ld(!!req.admitted, 'boolean'))
     .add(E, P_('jtbd', 'hasReviewerName'), req.by ? Lp(req.by) : null).add(E, P_('jtbd', 'hasRecordedAt'), Ld(nowIso(), 'dateTime'));
    (req.pass || []).forEach(function (c) { t.add(E, P_('rg', 'passesCheck'), I(conceptOf('check', c))); });
    (req.fail || []).forEach(function (c) { t.add(E, P_('rg', 'failsCheck'), I(conceptOf('check', c))); });
    await upd('DELETE WHERE { GRAPH <' + G.requirements + '> { ' + R + ' ?p ?o } } ;\nDELETE WHERE { GRAPH <' + G.requirements + '> { ' + E + ' ?p ?o } } ;\n' +
      'INSERT DATA { GRAPH <' + G.requirements + '> {\n' + t.text() + '} }');
    return { iri: R.slice(1, -1), id: id };
  }
  async function demandItems() {
    var rows = await sel('SELECT ?d ?id ?req ?rid ?status ?rank ?exp ?opp ?note ?rem ?mod WHERE { GRAPH <' + G.demand + '> {' +
      ' ?d a rg:demand-item ; jtbd:hasIdentifier ?id ; rg:realizesRequirement ?req ; rg:hasDemandStatus ?status .' +
      ' OPTIONAL { ?d rg:hasPriorityRank ?rank } OPTIONAL { ?d rg:hasExpectedOpportunityClosed ?exp } OPTIONAL { ?d rg:hasOpportunityScore ?opp }' +
      ' OPTIONAL { ?d rg:hasDemandNote ?note } OPTIONAL { ?d rg:isRemeasuredIn ?rem } OPTIONAL { ?d dct:modified ?mod } }' +
      ' OPTIONAL { ?req jtbd:hasIdentifier ?rid } } ORDER BY ?rank');
    return firstBy(rows, 'd').map(function (r) {
      return { iri: r.d, id: r.id, req: r.req, reqId: r.rid || '', status: codeOf('demand', r.status), rank: +(r.rank || 0), expected: +(r.exp || 0),
               opp: +(r.opp || 0), note: r.note || '', remeasuredIn: r.rem || '', modified: r.mod || '' };
    });
  }
  async function saveDemandItem(d) {
    var D = I(d.iri || (NS.rgr + 'Demand-' + slug(d.id))), t = TB();
    t.add(D, A, NAMED).add(D, A, P_('rg', 'demand-item'));
    labelTriples(t, D, d.label || ('Demand item ' + d.id));
    t.add(D, DEF, L('A demand item that asks demand planning to fund requirement ' + d.reqId + '.'))
     .add(D, P_('jtbd', 'hasIdentifier'), Lp(d.id)).add(D, P_('rg', 'realizesRequirement'), I(d.req))
     .add(D, P_('rg', 'hasDemandStatus'), I(conceptOf('demand', d.status || 'submitted')))
     .add(D, P_('rg', 'hasPriorityRank'), d.rank ? Ld(d.rank, 'integer') : null)
     .add(D, P_('rg', 'hasExpectedOpportunityClosed'), Ld(d.expected || 0, 'decimal')).add(D, P_('rg', 'hasOpportunityScore'), Ld(d.opp || 0, 'decimal'))
     .add(D, P_('rg', 'hasDemandNote'), d.note ? L(d.note) : null).add(D, P_('rg', 'isRemeasuredIn'), d.remeasuredIn ? I(d.remeasuredIn) : null)
     .add(D, STATUS, P_('core', 'Draft')).add(D, CREATED, Ld(d.created || today(), 'date')).add(D, MODIFIED, Ld(nowIso(), 'dateTime'));
    await upd('DELETE WHERE { GRAPH <' + G.demand + '> { ' + D + ' ?p ?o } } ;\nINSERT DATA { GRAPH <' + G.demand + '> {\n' + t.text() + '} }');
    return D.slice(1, -1);
  }

  /* ======================================================================
     Boot: status banner with a one-click release load, then hand the page its data
     ====================================================================== */
  function banner(html, tone) {
    var el = document.getElementById('c360-banner');
    if (!el) {
      el = document.createElement('div'); el.id = 'c360-banner';
      el.style.cssText = 'margin:12px auto;max-width:1180px;padding:12px 16px;border-radius:8px;font:13px/1.5 system-ui,-apple-system,sans-serif;' +
        'border:1px solid var(--ke-line,#d5dbe1);background:var(--ke-surface,#fff);color:var(--ke-ink,#1f2933);display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center';
      document.body.insertBefore(el, document.body.firstChild);
    }
    el.style.borderColor = tone === 'bad' ? 'var(--ke-bad,#c13232)' : tone === 'warn' ? 'var(--ke-warn,#a86a00)' : 'var(--ke-line,#d5dbe1)';
    el.innerHTML = html; el.hidden = false; return el;
  }
  function clearBanner() { var el = document.getElementById('c360-banner'); if (el) el.remove(); }
  /* Acronym expansions configured for ingestion (ingest/ke-ingest.config.json via proxy.py), so captured labels follow the same policy. */
  async function loadPolicy() {
    try {
      var r = await fetch('/api/ingest/policy', { cache: 'no-store' }); if (!r.ok) return;
      var j = await r.json(), exp = (j.acronyms && j.acronyms.expansions) || j.expansions || {};
      Object.keys(exp).forEach(function (k) { if (!ACR.some(function (a) { return a[0] === k.toUpperCase(); })) ACR.push([k.toUpperCase(), exp[k]]); });
    } catch (e) {}
  }
  async function boot(start) {
    banner('<span>Reading the Customer 360 graph from GraphDB…</span>');
    loadPolicy();
    var s = await status();
    if (!s.ok) {
      banner('<b>GraphDB is not reachable.</b><span>Start GraphDB on :7200 and run <code>python3 proxy.py</code> in the KE Workbench folder, then reload. (' +
        String(s.error).replace(/[<>&]/g, '') + ')</span>', 'bad');
      return;
    }
    if (!s.loaded) {
      var el = banner('<b>The Customer 360 graph is not in repository ' + s.repo + ' yet.</b><span>Load release ' + RELEASE +
        ' (personas, jobs, job steps, desired outcomes, vocabularies and the example survey wave) into its own named graphs.</span>' +
        '<button id="c360-load" style="font:inherit;padding:5px 12px;border-radius:6px;border:1px solid currentColor;background:transparent;cursor:pointer">Load into GraphDB</button><span id="c360-load-msg"></span>', 'warn');
      el.querySelector('#c360-load').onclick = async function () {
        this.disabled = true; var msg = el.querySelector('#c360-load-msg');
        try { await loadRelease(function (i, n, t) { msg.textContent = 'Loading ' + i + ' of ' + n + ': ' + t + '…'; }); location.reload(); }
        catch (e) { msg.textContent = String(e.message || e); this.disabled = false; }
      };
      return;
    }
    try { var M = await model(); clearBanner(); await start(M); }
    catch (e) { banner('<b>Could not read the Customer 360 graph.</b><span>' + String(e.message || e).replace(/[<>&]/g, '') + '</span>', 'bad'); console.error(e); }
  }

  window.KE_C360 = {
    RELEASE: RELEASE, NS: NS, G: G, CODES: CODES, DATA_DIR: DATA_DIR, DEMAND_ORDER: DEMAND_ORDER, METRIC_NAME: METRIC_NAME,
    status: status, loadRelease: loadRelease, model: model, boot: boot, banner: banner, clearBanner: clearBanner,
    pickWave: pickWave, setWave: setWave, scores: scores, saveWave: saveWave, analyze: analyze, opp: opp, ci: ciOf, modules: modules, benchmarkShape: benchmarkShape,
    reviews: reviews, saveReview: saveReview, decisions: decisions, saveDecision: saveDecision, reviewer: reviewer, setReviewer: setReviewer,
    interviews: interviews, interview: interview, saveInterview: saveInterview, deleteInterview: deleteInterview, newInterviewKey: newInterviewKey,
    composeOutcome: composeOutcome, requirements: requirements, saveRequirement: saveRequirement, demandItems: demandItems, saveDemandItem: saveDemandItem,
    expand: expand, slug: slug, local: local, lcFirst: lcFirst, today: today, nowIso: nowIso, uid: uid, codeOf: codeOf, conceptOf: conceptOf
  };
})();
