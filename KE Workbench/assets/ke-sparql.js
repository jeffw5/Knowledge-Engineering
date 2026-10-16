/* ==========================================================================
   KE Workbench — SPARQL helpers shared by the Model Editors.
   All calls go through the proxy (/graphdb/...), never straight to :7200,
   so there are no CORS problems.
   ========================================================================== */
(function () {
  var NS = {
    rdf: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    rdfs: 'http://www.w3.org/2000/01/rdf-schema#',
    owl: 'http://www.w3.org/2002/07/owl#',
    skos: 'http://www.w3.org/2004/02/skos/core#',
    obo: 'http://purl.obolibrary.org/obo/',
    dct: 'http://purl.org/dc/terms/'
  };
  var PREFIXES = Object.keys(NS).map(function (k) { return 'PREFIX ' + k + ': <' + NS[k] + '>'; }).join('\n') + '\n';

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  function param(name) { try { return new URLSearchParams(location.search).get(name); } catch (e) { return null; } }

  function repo() {
    var el = document.getElementById('repoId');
    var v = (el && el.value && el.value.trim()) || param('repo') || lsGet('ke-repo') || 'value-kb';
    return v;
  }
  function endpoint() { return '/graphdb/repositories/' + encodeURIComponent(repo()); }

  async function select(q) {
    var res = await fetch(endpoint(), {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/sparql-results+json' },
      // infer=false: read only the statements that were actually written. With GraphDB's
      // default ruleset, inferred rdfs:subClassOf closure made every class show up under
      // all of its ancestors in the editors (e.g. Major defect under Issue as well as Defect).
      body: new URLSearchParams({ query: PREFIXES + q, infer: 'false' })
    });
    if (!res.ok) throw new Error('Query failed (' + res.status + '): ' + (await res.text()).slice(0, 300));
    var data = await res.json();
    return data.results.bindings.map(function (b) {
      var o = {}; Object.keys(b).forEach(function (k) { o[k] = b[k].value; o[k + '$'] = b[k]; }); return o;
    });
  }

  async function update(u) {
    var res = await fetch(endpoint() + '/statements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ update: PREFIXES + u })
    });
    if (!res.ok) throw new Error('Update failed (' + res.status + '): ' + (await res.text()).slice(0, 300));
    return true;
  }

  function iri(u) {
    if (!/^[a-z][a-z0-9+.-]*:[^\s<>"{}|\\^`]*$/i.test(u)) throw new Error('Not a valid IRI: ' + u);
    return '<' + u + '>';
  }
  function lit(s, lang) {
    var e = String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, '\\n').replace(/\r/g, '\\r');
    return '"' + e + '"' + (lang ? '@' + lang : '');
  }
  function localName(u) {
    var s = String(u || '').replace(/[\/#]+$/, '');
    var i = Math.max(s.lastIndexOf('/'), s.lastIndexOf('#'));
    return decodeURIComponent(i >= 0 ? s.slice(i + 1) : s);
  }
  function compliantHosts() {
    try {
      var v = JSON.parse(lsGet('ke-base-urls') || 'null');
      if (Array.isArray(v) && v.length) return v.map(function (s) { return String(s).toLowerCase(); });
    } catch (e) {}
    return ['https://www.insperity.com/', 'https://www.enablingvalue.com/'];
  }
  // Kind of an asset from its IRI. Standard IRIs carry the kind as a path segment
  // (…/vocabulary/core-asset/, …/taxonomy/core-issue/, …/ontology/core-asset/,
  // …/shapes/core-asset/); legacy IRIs carry it in the name (taxonomy-core-issue).
  function kindOf(u) {
    var n = String(u || '').toLowerCase();
    var m = n.match(/^[a-z]+:\/\/[^\/]+\/(vocabulary|taxonomy|ontology|shapes)\//);
    if (m) return { vocabulary: 'voc', taxonomy: 'tax', ontology: 'ont', shapes: 'shp' }[m[1]];
    if (/vocabular/.test(n)) return 'voc';
    if (/taxonom/.test(n)) return 'tax';
    if (/\/shapes?[\/-]/.test(n)) return 'shp';
    return 'ont';
  }

  /* All model assets (ConceptSchemes and Ontologies), wherever their type triple lives. */
  async function listAssets() {
    var rows = await select(
      'SELECT ?a (SAMPLE(?t) AS ?type) (SAMPLE(?l) AS ?label) WHERE {\n' +
      '  { ?a a ?t } UNION { GRAPH ?g { ?a a ?t } }\n' +
      '  FILTER(?t IN (skos:ConceptScheme, owl:Ontology))\n' +
      '  OPTIONAL { ?a rdfs:label|skos:prefLabel|dct:title ?l }\n' +
      '} GROUP BY ?a ORDER BY ?a');
    // Shapes graphs hold SHACL shapes, not classes or concepts, so the editors leave them out.
    return rows.map(function (r) {
      return { iri: r.a, type: r.type === NS.skos + 'ConceptScheme' ? 'scheme' : 'ontology',
               kind: kindOf(r.a), label: r.label || localName(r.a) };
    }).filter(function (a) { return a.kind !== 'shp'; });
  }

  function pickLabel(cands) {
    // cands: [{v, lang, src}] — prefer skos:prefLabel@en, then rdfs:label@en, then anything
    var order = function (c) {
      return (c.src === 'pref' ? 0 : 2) + (c.lang === 'en' ? 0 : c.lang === '' ? 0.5 : 1);
    };
    cands.sort(function (a, b) { return order(a) - order(b); });
    return cands.length ? cands[0].v : null;
  }

  window.KE_SPARQL = {
    NS: NS, PREFIXES: PREFIXES, repo: repo, endpoint: endpoint, select: select, update: update,
    iri: iri, lit: lit, localName: localName, kindOf: kindOf, compliantHosts: compliantHosts,
    listAssets: listAssets, pickLabel: pickLabel, param: param, lsGet: lsGet, lsSet: lsSet
  };
})();
