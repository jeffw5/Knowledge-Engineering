/* KE Workbench — Semantic Governance v2.3 structural rules (amendments A1–A6, A9).
   Loaded after ke-rules.js, which calls KE_STRUCT.structuralRules from runChecks. The same rules as ingest/structural_checks.py.
   entities: [{ iri, kind, types:Set, p:{pred:[terms]}, graphs }] from ke-rules; quads: [{ s, p, o, g }]. */
(function (root) {
  var RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', RDFS = 'http://www.w3.org/2000/01/rdf-schema#', OWL = 'http://www.w3.org/2002/07/owl#',
      SKOS = 'http://www.w3.org/2004/02/skos/core#', DCT = 'http://purl.org/dc/terms/', CORE = 'https://www.insperity.com/ontology/core/';
  function vals(e, p) { return e.p[p] || []; }
  function lits(e, p) { return vals(e, p).filter(function (o) { return o.t === 'lit'; }); }
  function localName(iri) { var s = iri.replace(/[\/#]+$/, ''), i = Math.max(s.lastIndexOf('/'), s.lastIndexOf('#')); return s.slice(i + 1); }
  function anyLabel(e) { var l = lits(e, SKOS + 'prefLabel').concat(lits(e, RDFS + 'label')), en = l.filter(function (x) { return x.lang === 'en'; }); return (en[0] || l[0] || {}).v || ''; }
  var BASE_IRI = 'https://www.insperity.com/', BFO_RX = /^https?:\/\/purl\.obolibrary\.org\/obo\/BFO_/;
  var DERIV = [RDFS + 'subClassOf', SKOS + 'broader', DCT + 'subject', CORE + 'hasPrimaryTerm', CORE + 'formalizedBy'];
  var CORRESP = [SKOS + 'exactMatch', SKOS + 'closeMatch', SKOS + 'broadMatch', SKOS + 'narrowMatch', SKOS + 'relatedMatch'];
  var LEXICAL = ['http://www.w3.org/2008/05/skos-xl#altLabel', 'http://www.w3.org/2008/05/skos-xl#prefLabel', CORE + 'labels'];
  var EDGE_TYPE = {}; DERIV.forEach(function (p) { EDGE_TYPE[p] = 'derivation'; }); CORRESP.forEach(function (p) { EDGE_TYPE[p] = 'correspondence'; }); LEXICAL.forEach(function (p) { EDGE_TYPE[p] = 'lexicalization'; });
  var PARENT_PREDS = [RDFS + 'subClassOf', SKOS + 'broader', SKOS + 'broadMatch'];
  var UP_PREDS = [RDFS + 'subClassOf', SKOS + 'broader', CORE + 'formalizedBy'];     // forward derivation edges that lead to a parent class
  var PENDING_PRED = CORE + 'hasResolutionState', PENDING = CORE + 'pending';
  // Allowed-edge matrix (A4), default deny; provisional (ingest/ke-ingest.config.json "allowedEdges" in the build)
  var MATRIX = {
    core: { core: ['derivation', 'correspondence'], reference: ['derivation', 'correspondence'] },
    domain: { core: ['derivation', 'correspondence'], domain: ['derivation', 'correspondence'], reference: ['derivation', 'correspondence'] },
    enterprise: { core: ['derivation', 'correspondence'], domain: ['derivation', 'correspondence'], enterprise: ['derivation', 'correspondence'], reference: ['derivation', 'correspondence'] },
    customer: { core: ['derivation', 'correspondence'], domain: ['derivation', 'correspondence'], enterprise: ['derivation', 'correspondence'], customer: ['derivation', 'correspondence'], reference: ['correspondence'] }
  };
  function pathOf(iri) { return iri.indexOf(BASE_IRI) === 0 ? iri.slice(BASE_IRI.length).split(/[?#]/)[0].split('/').filter(Boolean) : null; }
  function tenantOf(iri) { var p = pathOf(iri), m = p && p[1] && /(?:^|-)customer-(t[0-9a-f]{8})(?:-|$)/.exec(p[1]); return m ? m[1] : null; }
  function tierOf(iri) {
    if (!iri) return 'other';
    if (BFO_RX.test(iri) || /^https?:\/\/(purl\.obolibrary\.org|www\.w3\.org|purl\.org)\//.test(iri)) return 'reference';
    var p = pathOf(iri); if (!p || !p.length || /^(graph|standard|catalog|resource|record-graph|party-graph)$/.test(p[0])) return 'other';
    var seg = p[1] || ''; if (!seg) return 'other';
    if (tenantOf(iri)) return 'customer';
    if (/^core(-|$)/.test(seg)) return 'core';
    if (/^enterprise(-|$)/.test(seg) || /^lexicon-enterprise/.test(seg)) return 'enterprise';
    return 'domain';
  }
  function assetOf(iri) { var p = pathOf(iri); return p && p.length > 1 && /^(vocabulary|taxonomy|ontology|shapes|lexicon|mapping)$/.test(p[0]) ? BASE_IRI + p[0] + '/' + p[1] + '/' : null; }
  function kindOfAsset(a) { var m = a && /insperity\.com\/([a-z]+)\//.exec(a); return m ? m[1] : ''; }

  // returns findings [{rule, sev, sec, iri, kind, label, detail}] and rule summaries
  function structuralRules(entities, quads, opts) {
    var matrix = (opts && opts.matrix) || MATRIX, byIri = new Map(entities.map(function (e) { return [e.iri, e]; }));
    var out = [], sum = {};
    function R(id, sec, sev, title, desc) { sum[id] = { id: id, sec: sec, sev: sev, title: title, desc: desc, checked: 0, failed: 0 }; }
    R('derivation-bfo', '3.7', 'error', 'Derivation path to BFO', 'Every concept, class and primitive has a derivation path to the BFO root; a primitive declares the BFO class it specializes (v2.3 A1, A6). A path that leaves the loaded graphs is not counted as a failure.');
    R('primitive-site', '3.7', 'error', 'Primitives minted at the core or a top-level domain', 'A primitive is minted only in the core or a top-level domain; a sub-domain, enterprise or customer asset requests one (v2.3 A2, A5).');
    R('polyhierarchy', '3.7', 'info', 'More than two parents', 'Multiple parents are kept to the minimum the meaning requires; more than two is reported to the data steward (v2.3 A3).');
    R('edge-matrix', '3.1', 'error', 'Allowed-edge matrix', 'An edge between tiers is a derivation, correspondence or lexicalization edge the matrix allows; any edge not listed is rejected (v2.3 A4).');
    R('tenant-derivation', '3.2', 'error', 'Customer concept derives from a core or domain class', 'Every local concept in a customer asset has a derivation edge to a core or domain class; a customer asset is never an ontology and mints no primitive (v2.3 A5).');
    R('label-resolution', '3.4', 'error', 'Label resolves to one concept in its scope', 'Every label resolves to exactly one concept in its scope, or the term is pending (v2.3 A6, A8).');
    R('tenant-isolation', '3.2', 'error', 'Tenant graphs isolated', 'No edge, import or query path joins two tenant graphs; core, domain and enterprise assets never refer to a tenant (v2.3 A9).');
    R('core-immutable', '3.7', 'error', 'Core terms immutable', 'A deprecated core term names its replacement with core:supersededBy (v2.3 A1).');
    function fail(rule, e, detail) { sum[rule].failed++; out.push({ rule: rule, sev: sum[rule].sev, sec: sum[rule].sec, iri: e.iri, kind: e.kind, label: anyLabel(e), detail: detail }); }
    function iris(e, p) { return vals(e, p).filter(function (o) { return o.t === 'iri'; }).map(function (o) { return o.v; }); }
    var memo = {};
    function reach(iri, seen) {             // 'yes' | 'no' | 'unknown'
      if (BFO_RX.test(iri)) return 'yes';
      if (memo[iri]) return memo[iri];
      var e = byIri.get(iri); if (!e) return 'unknown';
      seen = seen || {}; if (seen[iri]) return 'no'; seen[iri] = 1;
      var unk = false;
      for (var i = 0; i < UP_PREDS.length; i++) { var t = iris(e, UP_PREDS[i]);
        for (var j = 0; j < t.length; j++) { var r = reach(t[j], seen); if (r === 'yes') return (memo[iri] = 'yes'); if (r === 'unknown') unk = true; } }
      return unk ? 'unknown' : (memo[iri] = 'no');
    }
    var terms = entities.filter(function (e) { return (e.kind === 'concept' || e.kind === 'class') && e.iri.indexOf(BASE_IRI) === 0; });
    terms.forEach(function (e) {
      var a = assetOf(e.iri) || '', tier = tierOf(e.iri), prim = e.kind === 'concept' && kindOfAsset(a) === 'vocabulary';
      sum['derivation-bfo'].checked++;
      if (reach(e.iri) === 'no') fail('derivation-bfo', e, prim ? 'Primitive declares no BFO parent (core:formalizedBy or rdfs:subClassOf to a class that reaches BFO)' : 'No derivation path to the BFO root');
      var parents = {}; PARENT_PREDS.forEach(function (p) { iris(e, p).forEach(function (t) { if (t !== OWL + 'Thing') parents[t] = 1; }); });
      var np = Object.keys(parents).length; sum.polyhierarchy.checked++;
      if (np > 2) fail('polyhierarchy', e, np + ' parents: report to the data steward');
      if (prim) { sum['primitive-site'].checked++;
        var scope = (pathOf(a) || [])[1] || '';
        if (tier === 'domain' && scope.indexOf('.') >= 0) fail('primitive-site', e, 'Primitive minted in the nested domain ' + scope + ': request it from the top-level parent');
        else if (tier === 'enterprise' || tier === 'customer') fail('primitive-site', e, 'Primitive minted at the ' + tier + ' tier: only the core or a top-level domain mints primitives'); }
      if (tier === 'core') { var dep = lits(e, OWL + 'deprecated').some(function (l) { return l.v === 'true'; });
        if (dep) { sum['core-immutable'].checked++; if (!iris(e, CORE + 'supersededBy').length) fail('core-immutable', e, 'Deprecated core term has no core:supersededBy'); } }
      if (tier === 'customer' && e.kind === 'concept') { sum['tenant-derivation'].checked++;
        var ups = []; [RDFS + 'subClassOf', SKOS + 'broader', CORE + 'formalizedBy'].forEach(function (p) { ups = ups.concat(iris(e, p)); });
        if (!ups.some(function (t) { var x = tierOf(t); return x === 'core' || x === 'domain' || BFO_RX.test(t); })) fail('tenant-derivation', e, 'Customer concept has no derivation edge to a core or domain class'); }
    });
    entities.forEach(function (e) { if (e.kind === 'ontology' && tierOf(e.iri) === 'customer' && kindOfAsset(e.iri) === 'ontology') { sum['tenant-derivation'].checked++; fail('tenant-derivation', e, 'A customer-tier asset holds labels and local concepts, never an ontology'); } });
    // edges (A4, A9)
    var seenEdge = {};
    quads.forEach(function (q) {
      if (q.s.t !== 'iri' || q.o.t !== 'iri' || q.s.v.indexOf(BASE_IRI) !== 0) return;
      var et = EDGE_TYPE[q.p.v], imp = q.p.v === OWL + 'imports'; if (!et && !imp) return;
      var fa = assetOf(q.s.v) || q.s.v, ta = assetOf(q.o.v) || q.o.v, tt = tierOf(q.o.v); if (tt === 'other' || fa === ta) return;
      var ft = tierOf(q.s.v), e = byIri.get(q.s.v) || { iri: q.s.v, kind: 'term', p: {}, types: new Set() };
      var key = q.s.v + '|' + q.p.v + '|' + q.o.v; if (seenEdge[key]) return; seenEdge[key] = 1;
      var fte = tenantOf(fa), tte = tenantOf(ta); sum['tenant-isolation'].checked++;
      if (tte && fte && tte !== fte) { fail('tenant-isolation', e, 'Edge to another tenant (' + tte + '): no path joins two tenant graphs'); return; }
      if (tte && (ft === 'core' || ft === 'domain' || ft === 'enterprise')) { fail('tenant-isolation', e, ft.charAt(0).toUpperCase() + ft.slice(1) + ' asset refers to tenant ' + tte + ': tenant graphs may refer to core, domain and enterprise, never the reverse'); return; }
      if (imp) return;
      sum['edge-matrix'].checked++;
      var ok = (matrix[ft] || {})[tt]; if (!ok || ok.indexOf(et) < 0) fail('edge-matrix', e, et.charAt(0).toUpperCase() + et.slice(1) + ' edge ' + localName(q.p.v) + ' from the ' + ft + ' tier to the ' + tt + ' tier is not in the allowed-edge matrix');
    });
    // label resolution within a scope
    var labels = {};
    terms.forEach(function (e) { if (e.kind !== 'concept') return; var g = assetOf(e.iri) || '', pend = iris(e, PENDING_PRED).indexOf(PENDING) >= 0;
      [SKOS + 'prefLabel', SKOS + 'altLabel'].forEach(function (p) { lits(e, p).forEach(function (l) { var k = g + '|' + l.v.trim().toLowerCase() + '|' + (l.lang || ''); (labels[k] = labels[k] || {})[e.iri] = pend; }); }); });
    Object.keys(labels).forEach(function (k) { var ids = Object.keys(labels[k]); sum['label-resolution'].checked++;
      if (ids.length > 1 && !ids.every(function (i) { return labels[k][i]; })) ids.forEach(function (i) { fail('label-resolution', byIri.get(i), 'Label "' + k.split('|')[1] + '" resolves to ' + ids.length + ' concepts in this scope'); }); });
    return { findings: out, summary: Object.keys(sum).map(function (k) { return sum[k]; }) };
  }


  root.KE_STRUCT = { structuralRules: structuralRules, tierOf: tierOf, tenantOf: tenantOf, assetOf: assetOf, MATRIX: MATRIX,
    PREDICATES: [RDFS + 'subClassOf', SKOS + 'broader', SKOS + 'broadMatch', SKOS + 'exactMatch', SKOS + 'closeMatch', SKOS + 'narrowMatch', SKOS + 'relatedMatch',
      OWL + 'imports', OWL + 'deprecated', CORE + 'supersededBy', CORE + 'hasResolutionState', CORE + 'formalizedBy',
      'http://www.w3.org/2008/05/skos-xl#altLabel', 'http://www.w3.org/2008/05/skos-xl#prefLabel'] };
})(typeof window !== 'undefined' ? window : globalThis);
