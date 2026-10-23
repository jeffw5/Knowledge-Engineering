/* ==========================================================================
   KE Workbench — Customer 360 data layer
   One code path for every Customer 360 tool:
     • read: jobs-to-be-done, appreciative-inquiry and demand-planning triples
       from GraphDB (through proxy.py at /graphdb/), or — when GraphDB is not
       reachable — from the bundled Turtle in data/c360/ plus local drafts;
     • normalize the triples into personas, jobs, steps, outcomes, interviews
       and demand requests;
     • write: one named graph per interview or demand request (PUT Turtle);
     • score: study results (example or uploaded) and the Outcome Playbook's
       Fix / Innovate / Protect / Simplify rule.
   Requires assets/ke-turtle.js (parseTurtle). No other dependencies.
   ========================================================================== */
(function (root) {
  'use strict';
  var BASE = 'https://www.insperity.com/';
  var NS = {
    rdf: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', rdfs: 'http://www.w3.org/2000/01/rdf-schema#',
    owl: 'http://www.w3.org/2002/07/owl#', xsd: 'http://www.w3.org/2001/XMLSchema#',
    skos: 'http://www.w3.org/2004/02/skos/core#', dcterms: 'http://purl.org/dc/terms/', prov: 'http://www.w3.org/ns/prov#',
    jtbd: BASE + 'ontology/jobs-to-be-done/', ai: BASE + 'ontology/appreciative-inquiry/', dp: BASE + 'ontology/demand-planning/',
    ob: BASE + 'resource/outcome-benchmark/', air: BASE + 'resource/appreciative-inquiry/', dpr: BASE + 'resource/demand-planning/',
    theme: BASE + 'taxonomy/benchmark-theme/', metric: BASE + 'vocabulary/outcome-metric-type/',
    phase: BASE + 'vocabulary/inquiry-phase/', evid: BASE + 'vocabulary/evidence-status/', dtype: BASE + 'vocabulary/demand-type/',
    gstat: BASE + 'vocabulary/gateway-status/', grule: BASE + 'vocabulary/gateway-rule/',
    hr: 'http://example.org/hrservices/ddd#', core: BASE + 'ontology/core/'
  };
  var GRAPH_BASE = BASE + 'graph/customer-360/';
  var DEFAULT_GRAPH = 'urn:x-graphdb:default-graph';
  var LS = { localGraphs: 'c360-local-graphs', study: 'c360-study-results', review: 'c360-review' };
  var READ_NS = ['jtbd', 'ai', 'dp', 'ob', 'air', 'dpr', 'theme', 'metric', 'phase', 'evid', 'dtype', 'gstat', 'grule'];

  // ── small utilities ──────────────────────────────────────────────────
  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function lsJSON(k, d) { try { var v = JSON.parse(lsGet(k, 'null')); return v === null ? d : v; } catch (e) { return d; } }
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  function local(iri) { var s = String(iri).replace(/[\/#]+$/, ''); return s.slice(Math.max(s.lastIndexOf('/'), s.lastIndexOf('#')) + 1); }
  function humanize(n) { // GrossToNetPayrollService → Gross to net payroll service
    var s = local(n).replace(/[_-]+/g, ' ').replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/([A-Z]+)([A-Z][a-z])/g, '$1 $2');
    return s ? s[0].toUpperCase() + s.slice(1).replace(/\b([A-Z])([a-z]+)/g, function (m, a, b) { return a.toLowerCase() + b; }) : s;
  }
  function repo() { return lsGet('ke-repo', 'value-kb') || 'value-kb'; }
  function endpoint() { return '/graphdb/repositories/' + encodeURIComponent(repo()); }
  function slugId(prefix) { var d = new Date(); return prefix + '-' + d.toISOString().slice(2, 10).replace(/-/g, '') + '-' + Math.random().toString(36).slice(2, 6); }

  // ── GraphDB I/O ──────────────────────────────────────────────────────
  async function ping() {
    try {
      var r = await fetch('/graphdb/rest/repositories', { headers: { Accept: 'application/json' }, cache: 'no-store' });
      if (!r.ok) return false;
      var list = await r.json();
      return (Array.isArray(list) ? list : []).some(function (x) { return x.id === repo(); }) || (Array.isArray(list) && list.length > 0);
    } catch (e) { return false; }
  }
  async function sparql(q) {
    var r = await fetch(endpoint(), { method: 'POST', cache: 'no-store',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: 'application/sparql-results+json' },
      body: new URLSearchParams({ query: q }) });
    if (!r.ok) throw new Error('GraphDB query failed (HTTP ' + r.status + ')');
    return (await r.json()).results.bindings;
  }
  async function putGraph(graph, ttl) {
    var r = await fetch(endpoint() + '/statements?context=' + encodeURIComponent('<' + graph + '>'),
      { method: 'PUT', headers: { 'Content-Type': 'text/turtle' }, body: ttl });
    if (!r.ok) { var t = ''; try { t = await r.text(); } catch (e) {} throw new Error('GraphDB rejected the graph (HTTP ' + r.status + ')' + (t ? ': ' + t.slice(0, 200) : '')); }
    return true;
  }
  async function deleteGraph(graph) {
    var r = await fetch(endpoint() + '/statements?context=' + encodeURIComponent('<' + graph + '>'), { method: 'DELETE' });
    if (!r.ok) throw new Error('GraphDB could not delete the graph (HTTP ' + r.status + ')');
    return true;
  }
  function termFromBinding(b) {
    if (!b) return null;
    if (b.type === 'uri') return { t: 'iri', v: b.value };
    if (b.type === 'bnode') return { t: 'bnode', v: b.value };
    var o = { t: 'lit', v: b.value }; if (b['xml:lang']) o.lang = b['xml:lang']; if (b.datatype) o.dt = b.datatype; return o;
  }
  function readQuery() {
    var f = READ_NS.map(function (k) { return 'STRSTARTS(STR(?s), "' + NS[k] + '")'; }).join(' || ');
    return 'PREFIX jtbd: <' + NS.jtbd + '>\nPREFIX rdfs: <' + NS.rdfs + '>\nPREFIX skos: <' + NS.skos + '>\n' +
      'SELECT DISTINCT ?s ?p ?o ?g WHERE {\n' +
      '  { GRAPH ?g { ?s ?p ?o } FILTER(isIRI(?s) && (' + f + ')) }\n' +
      '  UNION { ?s a jtbd:client-persona . GRAPH ?g { ?s ?p ?o } FILTER(!STRSTARTS(STR(?s), "' + BASE + '")) }\n' +
      '  UNION { ?x jtbd:isAddressedByService ?s . GRAPH ?g { ?s ?p ?o } FILTER(?p IN (rdfs:label, skos:prefLabel, skos:definition)) }\n' +
      '}';
  }

  // ── bundled Turtle (offline) and local drafts ───────────────────────
  function dataRoot() { // tools/x.html → ../data/c360/ ; tools/peo-benchmark/x.html → ../../data/c360/
    if (typeof document === 'undefined') return '../data/c360/';
    var s = document.currentScript || document.querySelector('script[src*="c360-data.js"]');
    var src = s && s.getAttribute('src') || '../assets/c360-data.js';
    return src.replace(/assets\/c360-data\.js.*$/, '') + 'data/c360/';
  }
  var DATA_ROOT = dataRoot();
  var manifestCache = null;
  async function manifest() {
    if (manifestCache) return manifestCache;
    var r = await fetch(DATA_ROOT + 'manifest.json', { cache: 'no-store' });
    if (!r.ok) throw new Error('Bundled data not found at ' + DATA_ROOT);
    manifestCache = await r.json(); return manifestCache;
  }
  async function bundledQuads() {
    var m = await manifest(), quads = [];
    for (var i = 0; i < m.files.length; i++) {
      var f = m.files[i], txt = await (await fetch(DATA_ROOT + f.file, { cache: 'no-store' })).text();
      parseTurtle(txt).triples.forEach(function (t) { quads.push({ s: t.s, p: t.p, o: t.o, g: f.graph }); });
    }
    return quads;
  }
  async function loadBundledIntoGraphDB(kinds, onProgress) {
    var m = await manifest(), done = 0, files = m.files.filter(function (f) { return !kinds || kinds.indexOf(f.kind) >= 0; });
    for (var i = 0; i < files.length; i++) {
      var f = files[i], txt = await (await fetch(DATA_ROOT + f.file, { cache: 'no-store' })).text();
      await putGraph(f.graph, txt); done++;
      if (onProgress) onProgress(done, files.length, f);
    }
    return done;
  }
  // Local graphs: tools save drafts here (graph IRI → {ttl, title, kind, savedAt, publishedAt})
  function localGraphs() { return lsJSON(LS.localGraphs, {}); }
  function saveLocalGraph(graph, ttl, meta) {
    var all = localGraphs(); all[graph] = Object.assign({}, all[graph] || {}, meta || {}, { ttl: ttl, savedAt: Date.now() });
    return lsSet(LS.localGraphs, JSON.stringify(all));
  }
  function markPublished(graph) { var all = localGraphs(); if (all[graph]) { all[graph].publishedAt = Date.now(); lsSet(LS.localGraphs, JSON.stringify(all)); } }
  function removeLocalGraph(graph) { var all = localGraphs(); delete all[graph]; lsSet(LS.localGraphs, JSON.stringify(all)); }
  function localQuads(skipGraphs) {
    var all = localGraphs(), quads = [], bad = [];
    Object.keys(all).forEach(function (g) {
      if (skipGraphs && skipGraphs.has(g)) return;
      try { parseTurtle(all[g].ttl).triples.forEach(function (t) { quads.push({ s: t.s, p: t.p, o: t.o, g: g, local: true }); }); }
      catch (e) { bad.push(g); }
    });
    return { quads: quads, bad: bad };
  }

  // ── load: GraphDB first, bundled fallback, local drafts merged ──────
  async function load(opts) {
    opts = opts || {};
    var res = { source: 'bundled', quads: [], online: false, note: '', localDrafts: 0, graphs: new Set() };
    var online = opts.offline ? false : await ping();
    res.online = online;
    if (online) {
      try {
        var rows = await sparql(readQuery());
        rows.forEach(function (b) { res.quads.push({ s: termFromBinding(b.s), p: termFromBinding(b.p), o: termFromBinding(b.o), g: b.g && b.g.value }); });
        // Triples loaded without a named graph sit in GraphDB's default graph, which GRAPH ?g never matches.
        // If no persona came back that way, read the default graph too so a plain import still shows up.
        var hasPersona = res.quads.some(function (q) { return q.p.v === NS.rdf + 'type' && q.o.v === NS.jtbd + 'client-persona'; });
        if (!hasPersona) {
          var dflt = await sparql(readQuery().replace(/GRAPH \?g \{ (\?s \?p \?o) \}/g, '$1'));
          var seen = new Set(res.quads.map(function (q) { return q.s.v + '\u0001' + q.p.v + '\u0001' + q.o.v; }));
          dflt.forEach(function (b) { var q = { s: termFromBinding(b.s), p: termFromBinding(b.p), o: termFromBinding(b.o), g: DEFAULT_GRAPH };
            var k = q.s.v + '\u0001' + q.p.v + '\u0001' + q.o.v; if (!seen.has(k)) { seen.add(k); res.quads.push(q); } });
          if (dflt.length) res.note = 'Read from the default graph: load the files into their named graphs (Model Manager or the bundled-data loader) so drafts and reviews stay separable';
        }
        res.quads.forEach(function (q) { if (q.g) res.graphs.add(q.g); });
        res.source = 'graphdb';
      } catch (e) { res.note = e.message; online = false; res.online = false; }
    }
    if (res.source !== 'graphdb') {
      try { res.quads = await bundledQuads(); res.quads.forEach(function (q) { res.graphs.add(q.g); }); }
      catch (e) { res.note = (res.note ? res.note + ' · ' : '') + e.message; }
    }
    var lq = localQuads(res.source === 'graphdb' ? res.graphs : null);
    res.localDrafts = new Set(lq.quads.map(function (q) { return q.g; })).size;
    res.quads = res.quads.concat(lq.quads);
    res.model = buildModel(res.quads);
    return res;
  }

  // ── model ────────────────────────────────────────────────────────────
  function buildModel(quads) {
    var S = {}, R = NS.rdf + 'type';
    quads.forEach(function (q) {
      if (!q.s || q.s.t !== 'iri') return;
      var e = S[q.s.v] || (S[q.s.v] = { iri: q.s.v, types: new Set(), p: {}, graphs: new Set(), local: true });
      e.graphs.add(q.g); if (!q.local) e.local = false;   // local = every triple about it is an unpublished draft
      if (q.p.v === R && q.o.t === 'iri') e.types.add(q.o.v);
      var arr = e.p[q.p.v] || (e.p[q.p.v] = []);
      if (!arr.some(function (x) { return x.v === q.o.v && x.lang === q.o.lang; })) arr.push(q.o);
    });
    var J = NS.jtbd, A = NS.ai, D = NS.dp;
    function v1(e, p) { var a = e && e.p[p]; if (!a || !a.length) return ''; var en = a.filter(function (x) { return x.lang === 'en'; }); return (en[0] || a[0]).v; }
    function vs(e, p) { return ((e && e.p[p]) || []).map(function (x) { return x.v; }); }
    function lbl(iri) { var e = S[iri]; return (e && (v1(e, NS.skos + 'prefLabel') || v1(e, NS.rdfs + 'label'))) || humanize(iri); }
    function def(iri) { return v1(S[iri], NS.skos + 'definition'); }
    function has(e, t) { return e.types.has(t); }
    function ofType(t) { return Object.keys(S).filter(function (k) { return S[k].types.has(t); }).map(function (k) { return S[k]; }); }
    function graphOf(e) { return Array.from(e.graphs)[0] || ''; }
    // Evidence status: a later SME decision outranks the status written at capture time.
    var RANK = ['candidate', 'validated', 'benchmarked', 'retired'];
    function statusOf(e) { var best = '', r = -1; vs(e, J + 'hasEvidenceStatus').forEach(function (v) { var i = RANK.indexOf(local(v)); if (i > r) { r = i; best = v; } }); return best; }

    var M = { S: S, lbl: lbl, def: def, v1: v1, vs: vs, statusOf: statusOf, personas: [], jobs: {}, steps: [], outcomes: {}, mapSteps: {}, interviews: {}, demand: {}, themes: {}, metrics: {} };

    // universal steps
    M.steps = ofType(J + 'job-map-stage').map(function (e) {
      return { iri: e.iri, id: v1(e, J + 'hasIdentifier'), label: lbl(e.iri), order: +v1(e, J + 'hasStepOrder') || 99, def: def(e.iri) };
    }).sort(function (a, b) { return a.order - b.order; });
    M.stepByIri = {}; M.steps.forEach(function (s) { M.stepByIri[s.iri] = s; });

    // themes and metric types
    Object.keys(S).forEach(function (k) {
      if (k.indexOf(NS.theme) === 0 && S[k].types.has(NS.skos + 'Concept')) M.themes[k] = { iri: k, label: lbl(k), def: def(k) };
      if (k.indexOf(NS.metric) === 0 && S[k].types.has(NS.skos + 'Concept')) M.metrics[k] = { iri: k, label: lbl(k), def: def(k) };
    });

    // jobs (any subclass of JobToBeDone)
    var JOBT = { 'core-functional-job': 'core', 'consumption-chain-job': 'chain', 'emotional-job': 'emotional', 'social-job': 'social', 'job-to-be-done': 'job' };
    Object.keys(S).forEach(function (k) {
      var e = S[k], kind = null;
      Object.keys(JOBT).some(function (c) { if (e.types.has(J + c)) { kind = JOBT[c]; return true; } return false; });
      if (!kind) return;
      M.jobs[k] = { iri: k, id: v1(e, J + 'hasIdentifier') || local(k), label: lbl(k), stmt: v1(e, J + 'hasJobStatement') || lbl(k), kind: kind,
        executors: vs(e, J + 'hasJobExecutor'), participants: vs(e, J + 'hasJobParticipant'), outcomes: vs(e, J + 'hasDesiredOutcome'),
        mapSteps: vs(e, J + 'hasJobMapStep'), domains: vs(e, J + 'appliesToBusinessDomain'), status: statusOf(e),
        graph: graphOf(e), local: e.local, def: def(k) };
    });

    // outcomes
    ofType(J + 'desired-outcome').forEach(function (e) {
      var o = { iri: e.iri, id: v1(e, J + 'hasIdentifier') || local(e.iri), label: lbl(e.iri), stmt: v1(e, J + 'hasOutcomeStatement') || lbl(e.iri),
        job: vs(e, J + 'isOutcomeOfJob')[0] || '', step: vs(e, J + 'occursAtJobStep')[0] || '', mapStep: vs(e, J + 'relatesToJobMapStep')[0] || '',
        theme: vs(e, J + 'hasBenchmarkTheme')[0] || '', metric: vs(e, J + 'hasOutcomeMetricType')[0] || '', services: vs(e, J + 'isAddressedByService'),
        imp: v1(e, J + 'hasImportanceQuestion'), sat: v1(e, J + 'hasSatisfactionQuestion'), status: statusOf(e),
        graph: graphOf(e), local: e.local };
      M.outcomes[e.iri] = o;
      if (o.job && M.jobs[o.job] && M.jobs[o.job].outcomes.indexOf(e.iri) < 0) M.jobs[o.job].outcomes.push(e.iri);
    });
    // job → outcome links declared only on the job side
    Object.keys(M.jobs).forEach(function (k) { M.jobs[k].outcomes.forEach(function (oi) { if (M.outcomes[oi] && !M.outcomes[oi].job) M.outcomes[oi].job = k; }); });

    // job map steps
    ofType(J + 'job-map-step').forEach(function (e) {
      var m = { iri: e.iri, label: lbl(e.iri), stmt: v1(e, J + 'hasStepStatement') || lbl(e.iri), job: vs(e, J + 'isStepOfJob')[0] || '',
        step: vs(e, J + 'isPlacedAtJobStep')[0] || '', order: +v1(e, J + 'hasStepOrder') || 0, status: statusOf(e), graph: graphOf(e), local: e.local };
      M.mapSteps[e.iri] = m;
      if (m.job && M.jobs[m.job] && M.jobs[m.job].mapSteps.indexOf(e.iri) < 0) M.jobs[m.job].mapSteps.push(e.iri);
    });

    // personas
    M.personas = ofType(J + 'client-persona').map(function (e) {
      var ex = vs(e, J + 'executesJob'), pa = vs(e, J + 'participatesInJob');
      Object.keys(M.jobs).forEach(function (k) {
        if (M.jobs[k].executors.indexOf(e.iri) >= 0 && ex.indexOf(k) < 0) ex.push(k);
        if (M.jobs[k].participants.indexOf(e.iri) >= 0 && pa.indexOf(k) < 0) pa.push(k);
      });
      return { iri: e.iri, id: v1(e, J + 'hasIdentifier') || local(e.iri), label: lbl(e.iri), short: v1(e, J + 'hasShortName') || lbl(e.iri),
        alt: vs(e, NS.skos + 'altLabel'), def: def(e.iri), executes: ex, participates: pa, status: statusOf(e), graph: graphOf(e), local: e.local, e: e };
    }).sort(function (a, b) { return (a.id || a.label).localeCompare(b.id || b.label, undefined, { numeric: true }); });

    // interviews and excerpts
    ofType(A + 'persona-interview').forEach(function (e) {
      var iv = { iri: e.iri, id: v1(e, A + 'hasInterviewIdentifier') || local(e.iri), label: lbl(e.iri), persona: vs(e, A + 'interviewsPersona')[0] || '',
        date: v1(e, A + 'hasInterviewDate'), interviewer: v1(e, A + 'hasInterviewer'), profile: v1(e, A + 'hasParticipantProfile'),
        size: v1(e, A + 'hasCompanySizeBand'), industry: v1(e, A + 'hasIndustry'), topic: v1(e, A + 'hasAffirmativeTopic'),
        consent: v1(e, A + 'isConsentRecorded') === 'true', graph: graphOf(e), local: e.local, notes: [], excerpts: [] };
      vs(e, A + 'hasInterviewNote').forEach(function (n) { var ne = S[n]; if (ne) iv.notes.push({ iri: n, phase: vs(ne, A + 'hasInquiryPhase')[0] || '', text: v1(ne, A + 'hasNoteText') }); });
      vs(e, A + 'hasInterviewExcerpt').forEach(function (x) { var xe = S[x]; if (xe) iv.excerpts.push({ iri: x, phase: vs(xe, A + 'hasInquiryPhase')[0] || '', text: v1(xe, A + 'hasExcerptText'), evidenceFor: vs(xe, A + 'isEvidenceFor') }); });
      M.interviews[e.iri] = iv;
    });
    // evidence index: element IRI → excerpts
    M.evidence = {};
    Object.keys(M.interviews).forEach(function (k) {
      M.interviews[k].excerpts.forEach(function (x) { x.evidenceFor.forEach(function (t) { (M.evidence[t] = M.evidence[t] || []).push({ interview: k, excerpt: x }); }); });
    });

    // demand requests
    ofType(D + 'demand-request').forEach(function (e) {
      var r = { iri: e.iri, id: v1(e, D + 'hasRequestIdentifier') || local(e.iri), label: lbl(e.iri), statement: v1(e, D + 'hasRequirementStatement'),
        type: vs(e, D + 'hasDemandType')[0] || '', theme: vs(e, D + 'isOwnedByTheme')[0] || '', status: vs(e, D + 'hasGatewayStatus')[0] || '',
        value: +v1(e, D + 'hasValueScore') || 0, priority: +v1(e, D + 'hasPriorityScore') || 0, effort: v1(e, D + 'hasEffortEstimate'),
        wave: v1(e, D + 'hasRemeasureWave'), evidence: v1(e, D + 'hasEvidenceSource'), criteria: vs(e, D + 'hasAcceptanceCriterion'),
        personas: vs(e, D + 'servesPersona'), services: vs(e, D + 'changesService'), graph: graphOf(e), local: e.local, targets: [], checks: [] };
      vs(e, D + 'hasOutcomeTarget').forEach(function (t) { var te = S[t]; if (te) r.targets.push({ iri: t, outcome: vs(te, D + 'targetsOutcome')[0] || '',
        base: +v1(te, D + 'hasBaselineOpportunity'), sat: +v1(te, D + 'hasBaselineSatisfaction'), target: +v1(te, D + 'hasTargetOpportunity'), closure: +v1(te, D + 'hasExpectedGapClosure') }); });
      vs(e, D + 'hasGatewayCheck').forEach(function (c) { var ce = S[c]; if (ce) r.checks.push({ rule: vs(ce, D + 'appliesGatewayRule')[0] || '', passed: v1(ce, D + 'isCheckPassed') === 'true', finding: v1(ce, D + 'hasCheckFinding') }); });
      M.demand[e.iri] = r;
    });
    M.demandByOutcome = {};
    Object.keys(M.demand).forEach(function (k) { M.demand[k].targets.forEach(function (t) { (M.demandByOutcome[t.outcome] = M.demandByOutcome[t.outcome] || []).push(k); }); });
    M.outcomeById = {}; Object.keys(M.outcomes).forEach(function (k) { M.outcomeById[M.outcomes[k].id] = M.outcomes[k]; });
    return M;
  }

  // ── study scores and the playbook rule ───────────────────────────────
  // Scores: {PEO:{O001:[I,S,n]}, NONPEO:{…}, TOTAL?:{…}} on the 0–10 scale.
  function studyResults() {
    var saved = lsJSON(LS.study, null);
    if (saved && saved.R && saved.R.PEO) return { kind: 'file', name: saved.name || 'uploaded results', at: saved.at, R: saved.R };
    if (root.PEO && root.PEO.example) return { kind: 'example', name: 'Job Study example data', R: root.PEO.example };
    return null;
  }
  function saveStudyResults(name, R) { return lsSet(LS.study, JSON.stringify({ name: name, at: Date.now(), R: R })); }
  function clearStudyResults() { try { localStorage.removeItem(LS.study); } catch (e) {} }
  var opp = function (v) { return +(v[0] + Math.max(v[0] - v[1], 0)).toFixed(1); };
  function ci(v) { var n = v[2] || 1, pI = v[0] / 10, pS = v[1] / 10, vI = pI * (1 - pI) / n * 100, vS = pS * (1 - pS) / n * 100; return 1.96 * Math.sqrt(v[0] > v[1] ? 4 * vI + vS : vI); }
  // Same rule as the PEO Outcome Playbook's action matrix.
  function score(results, outcomeId) {
    if (!results || !results.R.PEO || !results.R.PEO[outcomeId] || !results.R.NONPEO || !results.R.NONPEO[outcomeId]) return null;
    var a = results.R.PEO[outcomeId], b = results.R.NONPEO[outcomeId], oa = opp(a), ob = opp(b);
    var g = +Math.sqrt(Math.pow(ci(a), 2) + Math.pow(ci(b), 2)).toFixed(1), d = +(oa - ob).toFixed(1), act = 'keep';
    if (a[1] > a[0]) act = 'simplify'; else if (oa >= 12 && d >= g) act = 'fix'; else if (oa >= 12 && ob >= 12) act = 'innovate'; else if (ob >= 12 && -d >= g) act = 'protect';
    return { peo: a, non: b, oPeo: oa, oNon: ob, gap: d, ci: g, sig: Math.abs(d) >= g, act: act, example: results.kind === 'example' };
  }
  var ACTIONS = { fix: ['Fix', 'PEO clients are under-served and significantly worse off than non-PEO employers.'],
    innovate: ['Innovate', 'Both segments are under-served (opportunity 12 or more).'],
    protect: ['Protect', 'Non-PEO employers are under-served and PEO clients significantly better served.'],
    simplify: ['Simplify', 'PEO clients are over-served: satisfaction exceeds importance.'],
    keep: ['Maintain', 'No action signal at current scores.'] };

  // ── review decisions (PEO Outcome Review CSV export) ────────────────
  function parseCSV(text) {
    var rows = [], row = [], cell = '', q = false, i = 0, c;
    text = String(text).replace(/^﻿/, '');
    for (; i < text.length; i++) {
      c = text[i];
      if (q) { if (c === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
      else if (c === '"') q = true;
      else if (c === ',') { row.push(cell); cell = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
      else cell += c;
    }
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    return rows.filter(function (r) { return r.some(function (x) { return x.trim() !== ''; }); });
  }
  function csvObjects(text) {
    var rows = parseCSV(text); if (!rows.length) return [];
    var head = rows[0].map(function (h) { return h.trim().toLowerCase(); });
    return rows.slice(1).map(function (r) { var o = {}; head.forEach(function (h, i) { o[h] = (r[i] || '').trim(); }); return o; });
  }
  function importReviewCSV(text, name) {
    var objs = csvObjects(text);
    if (!objs.length || !('item_id' in objs[0])) throw new Error('This is not a PEO Outcome Review export (no item_id column).');
    var items = {};
    objs.forEach(function (o) {
      var it = items[o.item_id] || (items[o.item_id] = { id: o.item_id, type: o.type, statement: o.statement, status: o.status, flags: [], verdicts: [], reviewers: 0,
        decision: o.final_decision || '', wording: o.final_wording || '', uses: (o.final_uses || '').split(/;\s*/).filter(Boolean) });
      if (o.reviewer) { it.reviewers++; if (o.verdict) it.verdicts.push({ role: o.role, verdict: o.verdict }); }
      (o.flags || '').split(/;\s*/).filter(Boolean).forEach(function (f) { if (it.flags.indexOf(f) < 0) it.flags.push(f); });
    });
    var rec = { name: name || 'review export', at: Date.now(), items: items };
    lsSet(LS.review, JSON.stringify(rec));
    return rec;
  }
  function reviewState() { return lsJSON(LS.review, null); }
  function clearReview() { try { localStorage.removeItem(LS.review); } catch (e) {} }

  // ── Turtle helpers for writers ──────────────────────────────────────
  function tl(s, lang) {
    var v = String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\r?\n/g, '\\n').replace(/\t/g, '\\t');
    return '"' + v + '"' + (lang === null ? '' : '@' + (lang || 'en'));
  }
  function tIri(iri) { return '<' + String(iri).replace(/[<>"{}|^`\\\s]/g, encodeURIComponent) + '>'; }
  function prefixBlock() {
    return ['rdf', 'rdfs', 'owl', 'xsd', 'skos', 'dcterms', 'prov', 'jtbd', 'ai', 'dp', 'ob', 'air', 'dpr', 'theme', 'metric', 'phase', 'evid', 'dtype', 'gstat', 'grule', 'hr']
      .map(function (k) { return '@prefix ' + (k + ':').padEnd(9) + '<' + NS[k] + '> .'; }).join('\n') + '\n';
  }
  // Acronyms are spelled out in preferred labels (Semantic Governance §3.2); the original wording goes in skos:altLabel.
  var ACR = [['FMLA', 'Family and Medical Leave Act'], ['COBRA', 'Consolidated Omnibus Budget Reconciliation Act'], ['OSHA', 'Occupational Safety and Health Administration'],
    ['EEOC', 'Equal Employment Opportunity Commission'], ['FCRA', 'Fair Credit Reporting Act'], ['ACA', 'Affordable Care Act'], ['FSA', 'flexible spending account'],
    ['HSA', 'health savings account'], ['IRS', 'Internal Revenue Service'], ['CPEO', 'certified professional employer organization'], ['PEO', 'professional employer organization'],
    ['PEOs', 'professional employer organizations'], ['CEO', 'Chief Executive Officer'], ['CFO', 'Chief Financial Officer'], ['HRIS', 'human resources information system'],
    ['PTO', 'paid time off'], ['SUTA', 'state unemployment tax'], ['PII', 'personal information'], ['IT', 'information technology'], ['HR', 'human resources'], ['AI', 'artificial intelligence']];
  function expand(s) { var out = String(s || ''); ACR.forEach(function (a) { out = out.replace(new RegExp('\\b' + a[0] + '\\b', 'g'), a[1]); }); return out.replace(/ & /g, ' and '); }
  function acronymsLeft(s) { return (String(s || '').match(/\b(?![IVX]+\b)[A-Z]{2,}s?\b/g) || []).filter(function (x, i, a) { return a.indexOf(x) === i; }); }
  // A camel-case local name from free text, without acronyms (§3.2): "Get HR answers" → "GetHrAnswers"
  function camel(text, max) {
    var w = String(text).replace(/[^A-Za-z0-9 ]+/g, ' ').trim().split(/\s+/).filter(Boolean).slice(0, max || 8);
    return w.map(function (x) { return x[0].toUpperCase() + x.slice(1).toLowerCase(); }).join('') || 'Item';
  }

  // ── status bar shared by the tools ───────────────────────────────────
  function statusHTML(res, extra) {
    var bits = [];
    if (res.source === 'graphdb') bits.push('<b>GraphDB</b> · ' + esc(repo()) + ' · ' + res.quads.length.toLocaleString() + ' triples from ' + res.graphs.size + (res.graphs.size === 1 ? ' graph' : ' graphs'));
    else bits.push('<b>' + (res.online ? 'GraphDB query failed' : 'GraphDB offline') + '</b> · showing the bundled schema and benchmark instances');
    if (res.localDrafts) bits.push(res.localDrafts + ' local draft graph' + (res.localDrafts > 1 ? 's' : '') + (res.source === 'graphdb' ? ' not yet published' : ''));
    if (res.note) bits.push('<span class="c360-err">' + esc(res.note) + '</span>');
    return bits.join(' · ') + (extra || '');
  }

  root.C360 = {
    NS: NS, BASE: BASE, GRAPH_BASE: GRAPH_BASE, LS: LS, esc: esc, local: local, humanize: humanize, repo: repo, endpoint: endpoint,
    ping: ping, sparql: sparql, putGraph: putGraph, deleteGraph: deleteGraph, load: load, buildModel: buildModel,
    manifest: manifest, loadBundledIntoGraphDB: loadBundledIntoGraphDB, dataRoot: function () { return DATA_ROOT; },
    localGraphs: localGraphs, saveLocalGraph: saveLocalGraph, removeLocalGraph: removeLocalGraph, markPublished: markPublished,
    studyResults: studyResults, saveStudyResults: saveStudyResults, clearStudyResults: clearStudyResults, score: score, opp: opp, ACTIONS: ACTIONS,
    parseCSV: parseCSV, csvObjects: csvObjects, importReviewCSV: importReviewCSV, reviewState: reviewState, clearReview: clearReview,
    tl: tl, tIri: tIri, prefixBlock: prefixBlock, camel: camel, expand: expand, acronymsLeft: acronymsLeft, slugId: slugId, statusHTML: statusHTML, lsGet: lsGet, lsSet: lsSet, lsJSON: lsJSON
  };
})(typeof window !== 'undefined' ? window : globalThis);
