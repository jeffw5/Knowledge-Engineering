/* ==========================================================================
   KE Workbench — PEO Outcome Review runtime (local)
   Gives tools/peo-outcome-review.html the three services it used to get from
   claude.ai — a shared review store, the reviewer's identity and file
   downloads — from inside the workbench:
     • store: GraphDB through proxy.py (/graphdb/). One named graph per
       reviewer (…/graph/customer-360/review/reviewer/{id}) holding that
       reviewer's item reviews, and one per final decision
       (…/review/decision/{item}). Records follow the outcome review ontology
       and vocabulary (data/c360/15-, 16-). Everyone using the same GraphDB
       repository sees the same reviews; the page re-reads every 15 seconds.
       When GraphDB is off, reviews are kept in this browser and published the
       next time GraphDB is reachable.
     • identity: a reviewer profile (name, whether you record final decisions)
       kept in this browser.
     • downloads: a normal browser download.
   Exposes window.KE_REVIEW_RUNTIME.use('db' | 'user' | 'downloads'), the same
   shape the page's code expects, and window.KE_REVIEW_STORE for other tools.
   ========================================================================== */
(function (root) {
  'use strict';
  var BASE = 'https://www.insperity.com/';
  var NS = { rdf: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', xsd: 'http://www.w3.org/2001/XMLSchema#', owl: 'http://www.w3.org/2002/07/owl#',
    rdfs: 'http://www.w3.org/2000/01/rdf-schema#', orv: BASE + 'ontology/outcome-review/', orvv: BASE + 'vocabulary/outcome-review/',
    orvr: BASE + 'resource/outcome-review/', ob: BASE + 'resource/outcome-benchmark/', theme: BASE + 'taxonomy/benchmark-theme/' };
  var GRAPH = BASE + 'graph/customer-360/review/';
  var LS_PROFILE = 'c360-reviewer', LS_LOCAL = 'c360-review-local', LS_CACHE = 'c360-review-cache', POLL_MS = 15000;

  // ── code ↔ concept maps (codes are the page's; concepts are orvv:) ─────
  var C = {
    role: { business: 'business-reviewer', compliance: 'compliance-reviewer' },
    verdict: { approve: 'approve', edits: 'approve-with-edits', discuss: 'needs-discussion', reject: 'reject' },
    flag: { regulated: 'regulated-topic', legal: 'legal-advice', tax: 'tax-advice', privacy: 'privacy-sensitivity', substantiate: 'needs-substantiation', bias: 'bias-risk', coemploy: 'co-employment-unclear' },
    use: { survey: 'survey-instrument', sales: 'internal-sales-guidance', marketing: 'external-marketing-claims' },
    keep: { keep: 'keep-in-study', merge: 'merge-with-another', drop: 'drop-from-study' },
    status: { accepted: 'accepted', dropped: 'dropped' }
  };
  var STAGE = { DEF: 'DefineStep', LOC: 'LocateStep', PRE: 'PrepareStep', CON: 'ConfirmStep', EXE: 'ExecuteStep', MON: 'MonitorStep', MOD: 'ModifyStep', CONC: 'ConcludeStep' };
  var THEME = { 'Payroll': 'payroll', 'Benefits': 'benefits', 'HR Compliance': 'human-resources-compliance', 'Talent Management': 'talent-management',
    'Training': 'training', 'Coaching': 'coaching', 'Monitoring': 'monitoring', 'Measurement': 'measurement', 'Values Stewardship': 'values-stewardship',
    'PEO Relationship': 'professional-employer-organization-relationship', 'HR Technology & Data': 'human-resources-technology-and-data' };
  var PERSONA = { P1: 'BusinessOwner', P2: 'FinanceLeader', P3: 'HumanResourcesLeader', P4: 'OperationsAndSafetyLeader', P5: 'PeopleManager', P6: 'WorksiteEmployee', P7: 'SystemsAdministrator' };
  function inv(m) { var o = {}; Object.keys(m).forEach(function (k) { o[m[k]] = k; }); return o; }
  var R = {}; Object.keys(C).forEach(function (k) { R[k] = inv(C[k]); });
  var R_STAGE = inv(STAGE), R_THEME = inv(THEME);

  function itemIri(id) {
    if (PERSONA[id]) return NS.ob + PERSONA[id];
    if (/^[JC]\d+$/.test(id)) return NS.ob + 'Job-' + id;
    if (/^O\d+$/.test(id)) return NS.ob + 'Outcome-' + id;
    return null;
  }
  function typeOf(id) { return /^P/.test(id) ? 'persona' : /^[JC]/.test(id) ? 'job' : 'outcome'; }

  // ── small utilities ────────────────────────────────────────────────────
  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v === null ? d : v; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function lsJSON(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function repo() { return lsGet('ke-repo', 'value-kb') || 'value-kb'; }
  function endpoint() { return '/graphdb/repositories/' + encodeURIComponent(repo()); }
  function slug(s) { return String(s || '').toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 48) || 'reviewer'; }
  function lit(s) { return '"' + String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\r?\n/g, '\\n').replace(/\t/g, '\\t') + '"'; }
  function iso(t) { return new Date(t || Date.now()).toISOString().replace(/\.\d{3}Z$/, 'Z'); }
  function err(code, msg) { var e = new Error(msg || code); e.code = code; return e; }

  // ── profile ────────────────────────────────────────────────────────────
  function profile() { var p = lsJSON(LS_PROFILE, null); return p && p.id && p.name ? p : null; }
  function setProfile(name, decider) {
    var old = profile(), p = { id: slug(name), name: String(name).trim(), decider: !!decider };
    if (old && old.id === p.id && old.role) p.role = old.role;
    lsSet(LS_PROFILE, JSON.stringify(p)); return p;
  }
  function clearProfile() { try { localStorage.removeItem(LS_PROFILE); } catch (e) {} }
  function rememberRole(role) { var p = profile(); if (p) { p.role = role; lsSet(LS_PROFILE, JSON.stringify(p)); } }

  // ── state: reviewers {uid:{role,name,decider,at}}, items {uid:{item:body}}, decisions {item:body}
  var S = { reviewers: {}, items: {}, decisions: {} }, online = null, lastError = '';

  // ── GraphDB I/O ────────────────────────────────────────────────────────
  async function ping() {
    try { var r = await fetch('/graphdb/rest/repositories', { headers: { Accept: 'application/json' }, cache: 'no-store' }); return r.ok; }
    catch (e) { return false; }
  }
  async function sparql(q) {
    var r = await fetch(endpoint(), { method: 'POST', cache: 'no-store',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: 'application/sparql-results+json' }, body: new URLSearchParams({ query: q }) });
    if (!r.ok) throw err('unavailable', 'GraphDB query failed (HTTP ' + r.status + ')');
    return (await r.json()).results.bindings;
  }
  async function putGraph(g, ttl) {
    var r = await fetch(endpoint() + '/statements?context=' + encodeURIComponent('<' + g + '>'), { method: 'PUT', headers: { 'Content-Type': 'text/turtle' }, body: ttl });
    if (!r.ok) throw err('unavailable', 'GraphDB rejected the review (HTTP ' + r.status + ')');
  }
  async function deleteGraph(g) {
    var r = await fetch(endpoint() + '/statements?context=' + encodeURIComponent('<' + g + '>'), { method: 'DELETE' });
    if (!r.ok) throw err('unavailable', 'GraphDB could not remove the decision (HTTP ' + r.status + ')');
  }
  var PREFIXES = ['rdf', 'rdfs', 'owl', 'xsd', 'orv', 'orvv', 'orvr', 'ob', 'theme'].map(function (k) { return '@prefix ' + k + ': <' + NS[k] + '> .'; }).join('\n') + '\n\n';

  // ── Turtle writers ─────────────────────────────────────────────────────
  function reviewerTTL(uid) {
    var rv = S.reviewers[uid] || {}, me = 'orvr:reviewer-' + uid, out = [PREFIXES];
    var lines = ['rdfs:label ' + lit('Reviewer ' + uid) + '@en', 'orv:hasReviewerIdentifier ' + lit(uid), 'orv:hasReviewerName ' + lit(rv.name || uid),
      'orv:isDecisionMaker "' + (!!rv.decider) + '"^^xsd:boolean', 'orv:hasRecordedTime "' + iso(rv.at) + '"^^xsd:dateTime'];
    if (C.role[rv.role]) lines.push('orv:hasReviewRole orvv:' + C.role[rv.role]);
    out.push(me + ' a owl:NamedIndividual, orv:reviewer ;\n    ' + lines.join(' ;\n    ') + ' .\n');
    var items = S.items[uid] || {};
    Object.keys(items).sort().forEach(function (id) {
      var b = items[id], iri = itemIri(id), L = ['rdfs:label ' + lit('Review of ' + id) + '@en', 'orv:hasItemIdentifier ' + lit(id), 'orv:isReviewedBy ' + me,
        'orv:hasRecordedTime "' + iso(b.at) + '"^^xsd:dateTime'];
      if (iri) L.push('orv:concernsItem <' + iri + '>');
      if (C.role[b.role]) L.push('orv:hasReviewRole orvv:' + C.role[b.role]);
      if (C.verdict[b.verdict]) L.push('orv:hasVerdict orvv:' + C.verdict[b.verdict]);
      if (b.wording) L.push('orv:hasSuggestedWording ' + lit(b.wording) + '@en');
      if (b.comment) L.push('orv:hasReviewComment ' + lit(b.comment) + '@en');
      if (C.keep[b.keep]) L.push('orv:hasStudyDisposition orvv:' + C.keep[b.keep]);
      if (b.merge) L.push('orv:hasDuplicateOf ' + lit(b.merge));
      if (STAGE[b.step]) L.push('orv:hasSuggestedJobMapStage ob:' + STAGE[b.step]);
      if (THEME[b.theme]) L.push('orv:hasSuggestedTheme theme:' + THEME[b.theme]);
      (b.flags || []).forEach(function (f) { if (C.flag[f]) L.push('orv:hasRiskFlag orvv:' + C.flag[f]); });
      (b.uses || []).forEach(function (u) { if (C.use[u]) L.push('orv:hasApprovedUse orvv:' + C.use[u]); });
      out.push('orvr:review-' + uid + '-' + id + ' a owl:NamedIndividual, orv:item-review ;\n    ' + L.join(' ;\n    ') + ' .\n');
    });
    return out.join('\n');
  }
  function decisionTTL(id) {
    var d = S.decisions[id], iri = itemIri(id);
    var L = ['rdfs:label ' + lit('Final decision on ' + id) + '@en', 'orv:hasItemIdentifier ' + lit(id), 'orv:hasRecordedTime "' + iso(d.at) + '"^^xsd:dateTime'];
    if (iri) L.push('orv:concernsItem <' + iri + '>');
    if (C.status[d.status]) L.push('orv:hasDecisionStatus orvv:' + C.status[d.status]);
    if (d.by) L.push('orv:isDecidedBy orvr:reviewer-' + d.by);
    if (d.wording) L.push('orv:hasFinalWording ' + lit(d.wording) + '@en');
    if (d.note) L.push('orv:hasDecisionNote ' + lit(d.note) + '@en');
    (d.uses || []).forEach(function (u) { if (C.use[u]) L.push('orv:hasApprovedUse orvv:' + C.use[u]); });
    return PREFIXES + 'orvr:decision-' + id + ' a owl:NamedIndividual, orv:review-decision ;\n    ' + L.join(' ;\n    ') + ' .\n';
  }

  // ── reading from GraphDB (quads → state) ───────────────────────────────
  function fromQuads(rows) {
    var subj = {};
    rows.forEach(function (b) {
      var s = b.s.value, p = b.p.value, o = b.o.value;
      var e = subj[s] || (subj[s] = { types: [], p: {} });
      if (p === NS.rdf + 'type') e.types.push(o);
      (e.p[p] = e.p[p] || []).push(o);
    });
    function v1(e, k) { var a = e.p[NS.orv + k]; return a && a.length ? a[0] : ''; }
    function vs(e, k) { return e.p[NS.orv + k] || []; }
    function code(map, iri) { return iri ? map[iri.slice(iri.lastIndexOf('/') + 1)] || '' : ''; }
    var st = { reviewers: {}, items: {}, decisions: {} }, uidOf = {};
    Object.keys(subj).forEach(function (s) {
      var e = subj[s];
      if (e.types.indexOf(NS.orv + 'reviewer') >= 0) {
        var uid = v1(e, 'hasReviewerIdentifier') || s.slice((NS.orvr + 'reviewer-').length); uidOf[s] = uid;
        st.reviewers[uid] = { role: code(R.role, v1(e, 'hasReviewRole')) || null, name: v1(e, 'hasReviewerName') || uid,
          decider: v1(e, 'isDecisionMaker') === 'true', at: Date.parse(v1(e, 'hasRecordedTime')) || 0 };
      }
    });
    Object.keys(subj).forEach(function (s) {
      var e = subj[s];
      if (e.types.indexOf(NS.orv + 'item-review') >= 0) {
        var uid = uidOf[v1(e, 'isReviewedBy')] || String(v1(e, 'isReviewedBy')).replace(NS.orvr + 'reviewer-', ''), id = v1(e, 'hasItemIdentifier');
        if (!uid || !id) return;
        var b = { item: id, type: typeOf(id), role: code(R.role, v1(e, 'hasReviewRole')), verdict: code(R.verdict, v1(e, 'hasVerdict')),
          wording: v1(e, 'hasSuggestedWording'), comment: v1(e, 'hasReviewComment'), at: Date.parse(v1(e, 'hasRecordedTime')) || 0 };
        var keep = code(R.keep, v1(e, 'hasStudyDisposition')); if (keep) b.keep = keep;
        if (v1(e, 'hasDuplicateOf')) b.merge = v1(e, 'hasDuplicateOf');
        var stg = v1(e, 'hasSuggestedJobMapStage'); if (stg) b.step = R_STAGE[stg.slice(NS.ob.length)] || '';
        var th = v1(e, 'hasSuggestedTheme'); if (th) b.theme = R_THEME[th.slice(NS.theme.length)] || '';
        var fl = vs(e, 'hasRiskFlag').map(function (x) { return code(R.flag, x); }).filter(Boolean);
        var us = vs(e, 'hasApprovedUse').map(function (x) { return code(R.use, x); }).filter(Boolean);
        if (b.role === 'compliance') { b.flags = fl; b.uses = us; }
        (st.items[uid] = st.items[uid] || {})[id] = b;
        if (!st.reviewers[uid]) st.reviewers[uid] = { role: b.role, name: uid, decider: false, at: b.at };
      }
      if (e.types.indexOf(NS.orv + 'review-decision') >= 0) {
        var did = v1(e, 'hasItemIdentifier'); if (!did) return;
        st.decisions[did] = { item: did, status: code(R.status, v1(e, 'hasDecisionStatus')), wording: v1(e, 'hasFinalWording'), note: v1(e, 'hasDecisionNote'),
          uses: vs(e, 'hasApprovedUse').map(function (x) { return code(R.use, x); }).filter(Boolean),
          by: uidOf[v1(e, 'isDecidedBy')] || String(v1(e, 'isDecidedBy')).replace(NS.orvr + 'reviewer-', ''), at: Date.parse(v1(e, 'hasRecordedTime')) || 0 };
      }
    });
    return st;
  }
  async function readRemote() {
    var rows = await sparql('SELECT ?g ?s ?p ?o WHERE { GRAPH ?g { ?s ?p ?o } FILTER(STRSTARTS(STR(?g), "' + GRAPH + '")) }');
    return fromQuads(rows);
  }

  // ── local (browser) store, used when GraphDB is off ────────────────────
  function readLocal() { var l = lsJSON(LS_LOCAL, null); return l && l.reviewers ? l : { reviewers: {}, items: {}, decisions: {}, removed: [] }; }
  function writeLocal(l) { lsSet(LS_LOCAL, JSON.stringify(l)); }
  function hasLocal() { var l = readLocal(); return Object.keys(l.items).length || Object.keys(l.decisions).length || (l.removed || []).length || Object.keys(l.reviewers).length; }

  // Publish what was saved while GraphDB was off: this reviewer's graph and any decisions.
  async function publishLocal() {
    var l = readLocal(); if (!hasLocal()) return 0;
    var n = 0;
    Object.keys(l.reviewers).forEach(function (uid) { S.reviewers[uid] = Object.assign({}, S.reviewers[uid] || {}, l.reviewers[uid]); });
    for (var uid in l.items) { S.items[uid] = Object.assign({}, S.items[uid] || {}, l.items[uid]); }
    for (var u2 in Object.assign({}, l.reviewers, l.items)) { await putGraph(GRAPH + 'reviewer/' + u2, reviewerTTL(u2)); n++; }
    for (var id in l.decisions) { S.decisions[id] = l.decisions[id]; await putGraph(GRAPH + 'decision/' + id, decisionTTL(id)); n++; }
    for (var i = 0; i < (l.removed || []).length; i++) { delete S.decisions[l.removed[i]]; await deleteGraph(GRAPH + 'decision/' + l.removed[i]); n++; }
    try { localStorage.removeItem(LS_LOCAL); } catch (e) {}
    return n;
  }

  async function refresh() {
    var was = online; online = await ping();
    if (online) {
      try {
        if (hasLocal()) { var cur = await readRemote(); S = cur; await publishLocal(); }
        S = await readRemote(); lastError = '';
        lsSet(LS_CACHE, JSON.stringify(S));   // last shared state, shown while GraphDB is off
      } catch (e) { lastError = e.message || String(e); online = false; }
    }
    if (!online) {   // last shared state from GraphDB, with what was saved here since
      var c = lsJSON(LS_CACHE, null) || { reviewers: {}, items: {}, decisions: {} }, l = readLocal();
      Object.keys(l.reviewers).forEach(function (u) { c.reviewers[u] = Object.assign({}, c.reviewers[u] || {}, l.reviewers[u]); });
      Object.keys(l.items).forEach(function (u) { c.items[u] = Object.assign({}, c.items[u] || {}, l.items[u]); });
      Object.keys(l.decisions).forEach(function (id) { c.decisions[id] = l.decisions[id]; });
      (l.removed || []).forEach(function (id) { delete c.decisions[id]; });
      S = c;
    }
    if (was !== online) try { document.dispatchEvent(new CustomEvent('ke-review-store', { detail: { online: online } })); } catch (e) {}
    emit();
  }

  // ── writes ─────────────────────────────────────────────────────────────
  async function writeReviewer(uid) {
    if (online) return putGraph(GRAPH + 'reviewer/' + uid, reviewerTTL(uid));
    var l = readLocal(); l.reviewers[uid] = S.reviewers[uid]; l.items[uid] = S.items[uid] || {}; writeLocal(l);
  }
  async function writeDecision(id) {
    if (online) return putGraph(GRAPH + 'decision/' + id, decisionTTL(id));
    var l = readLocal(); l.decisions[id] = S.decisions[id]; l.removed = (l.removed || []).filter(function (x) { return x !== id; }); writeLocal(l);
  }
  async function removeDecision(id) {
    if (online) return deleteGraph(GRAPH + 'decision/' + id);
    var l = readLocal(); delete l.decisions[id]; (l.removed = l.removed || []).push(id); writeLocal(l);
  }

  // ── the db facade the page uses ────────────────────────────────────────
  var listeners = [];
  function snap(docs) { return { docs: docs.map(function (d) { return { id: d[0], data: function () { return Object.assign({}, d[1]); } }; }) }; }
  function emitOne(l) {
    try {
      if (l.path === 'rv') l.cb(snap(Object.keys(S.reviewers).map(function (k) { return [k, S.reviewers[k]]; })));
      else if (l.path === 'decisions') l.cb(snap(Object.keys(S.decisions).map(function (k) { return [k, S.decisions[k]]; })));
      else { var m = /^rv\/([^/]+)\/items$/.exec(l.path); if (m) { var it = S.items[m[1]] || {}; l.cb(snap(Object.keys(it).map(function (k) { return [k, it[k]]; }))); } }
    } catch (e) {}
  }
  function emit() { listeners.slice().forEach(emitOne); }
  function doc(path) {
    var m;
    return {
      get: async function () {
        if ((m = /^rv\/([^/]+)$/.exec(path))) {
          var pr = profile(), mine = pr && pr.id === m[1] && pr.role ? { role: pr.role } : null;
          return { exists: !!(S.reviewers[m[1]] || mine), data: function () { return Object.assign({}, mine || {}, S.reviewers[m[1]] || {}); } };
        }
        if ((m = /^decisions\/([^/]+)$/.exec(path))) return { exists: !!S.decisions[m[1]], data: function () { return Object.assign({}, S.decisions[m[1]]); } };
        if ((m = /^rv\/([^/]+)\/items\/([^/]+)$/.exec(path))) { var x = (S.items[m[1]] || {})[m[2]]; return { exists: !!x, data: function () { return Object.assign({}, x); } }; }
        return { exists: false, data: function () { return {}; } };
      },
      set: async function (obj) {
        var p = profile(); if (!p) throw err('invalid_argument', 'No reviewer profile');
        if ((m = /^rv\/([^/]+)$/.exec(path))) {
          if (m[1] !== p.id) throw err('invalid_argument');
          S.reviewers[m[1]] = Object.assign({}, S.reviewers[m[1]] || {}, obj, { name: p.name, decider: p.decider }); if (obj.role) rememberRole(obj.role); await writeReviewer(m[1]);
        } else if ((m = /^rv\/([^/]+)\/items\/([^/]+)$/.exec(path))) {
          if (m[1] !== p.id) throw err('invalid_argument');
          S.reviewers[m[1]] = Object.assign({ role: obj.role }, S.reviewers[m[1]] || {}, { name: p.name, decider: p.decider, at: Date.now() });
          (S.items[m[1]] = S.items[m[1]] || {})[m[2]] = obj; await writeReviewer(m[1]);
        } else if ((m = /^decisions\/([^/]+)$/.exec(path))) {
          if (!p.decider) throw err('invalid_argument');
          S.decisions[m[1]] = obj; await writeDecision(m[1]);
        }
        emit();
      },
      delete: async function () {
        var p = profile();
        if ((m = /^decisions\/([^/]+)$/.exec(path))) { if (!p || !p.decider) throw err('invalid_argument'); delete S.decisions[m[1]]; await removeDecision(m[1]); emit(); }
      }
    };
  }
  var db = {
    doc: doc,
    collection: function (path) {
      return {
        doc: function (id) { return doc(path + '/' + id); },
        onSnapshot: function (cb) { var l = { path: path, cb: cb }; listeners.push(l); emitOne(l); return function () { listeners = listeners.filter(function (x) { return x !== l; }); }; }
      };
    }
  };
  var user = {
    me: async function () { var p = profile(); return p ? { id: p.id, name: p.name, avatarUrl: '', canEdit: p.decider, isOwner: false } : { id: null, name: '', avatarUrl: '', canEdit: false, isOwner: false }; },
    can: async function () { return true; },
    profiles: async function (ids) { var o = {}; (ids || []).forEach(function (id) { var r = S.reviewers[id]; var p = profile(); o[id] = { name: (r && r.name) || id, isMe: !!(p && p.id === id) }; }); return o; }
  };
  var downloads = {
    save: async function (o) {
      var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([o.data], { type: o.filename && /\.csv$/i.test(o.filename) ? 'text/csv' : 'text/plain' }));
      a.download = o.filename || 'download.txt'; document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    }
  };

  var started = false;
  async function start() { if (started) return; started = true; await refresh(); setInterval(function () { if (!document.hidden) refresh(); }, POLL_MS); }

  root.KE_REVIEW_RUNTIME = {
    use: async function (name) { await start(); return name === 'db' ? db : name === 'user' ? user : name === 'downloads' ? downloads : null; }
  };
  root.KE_REVIEW_STORE = {
    profile: profile, setProfile: setProfile, clearProfile: clearProfile, refresh: refresh, readRemote: readRemote,
    status: function () { return { online: online, repo: repo(), error: lastError, pending: !!hasLocal() }; },
    GRAPH: GRAPH, NS: NS, itemIri: itemIri, fromQuads: fromQuads
  };
})(typeof window !== 'undefined' ? window : globalThis);
