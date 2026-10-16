/* KE Workbench — compact Turtle parser (RDF 1.1 Turtle, no RDF-star).
   parseTurtle(text, { base }) → { triples:[{s,p,o}], prefixes }
   Terms: { t:'iri', v } | { t:'bnode', v } | { t:'lit', v, lang?, dt? }
   Throws Error with a line number on malformed input. */
(function (root) {
  var RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#';
  var XSD = 'http://www.w3.org/2001/XMLSchema#';

  function unescapeStr(s, line) {
    return s.replace(/\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|[tbnrf"'\\])/g, function (_, e) {
      switch (e[0]) {
        case 't': return '\t'; case 'b': return '\b'; case 'n': return '\n';
        case 'r': return '\r'; case 'f': return '\f'; case '"': return '"';
        case "'": return "'"; case '\\': return '\\';
        default: return String.fromCodePoint(parseInt(e.slice(1), 16));
      }
    });
  }
  function unescapeLocal(s) { return s.replace(/\\([_~.\-!$&'()*+,;=\/?#@%])/g, '$1'); }

  function resolve(iri, base) {
    if (/^[a-zA-Z][\w+.-]*:/.test(iri)) return iri;
    try { return new URL(iri, base || 'urn:x-base:/').href; } catch (e) { return (base || '') + iri; }
  }

  var PN_LOCAL = /^((?:[\p{L}\p{N}_:%\-]|\\[_~.\-!$&'()*+,;=\/?#@%]|\.(?=[\p{L}\p{N}_:%\-\\]))*)/u;
  var PN_PREFIX = /^([\p{L}](?:[\p{L}\p{N}_\-]|\.(?=[\p{L}\p{N}_\-]))*)?:/u;

  function tokenize(src) {
    var toks = [], i = 0, line = 1, n = src.length, m;
    function push(type, val) { toks.push({ type: type, val: val, line: line }); }
    while (i < n) {
      var c = src[i];
      if (c === '\n') { line++; i++; continue; }
      if (c === ' ' || c === '\t' || c === '\r') { i++; continue; }
      if (c === '#') { while (i < n && src[i] !== '\n') i++; continue; }
      var rest = src.slice(i, i + 4096);
      if (c === '<') {
        m = /^<([^<>"{}|^`\\\s]*)>/.exec(src.slice(i));
        if (!m) throw new Error('Line ' + line + ': bad IRI');
        push('IRI', unescapeStr(m[1], line)); i += m[0].length; continue;
      }
      if (c === '"' || c === "'") {
        var q3 = src.substr(i, 3) === c + c + c, q = q3 ? c + c + c : c, j = i + q.length, buf = '';
        while (true) {
          if (j >= n) throw new Error('Line ' + line + ': unterminated string');
          if (src[j] === '\\') { buf += src.substr(j, 2); j += 2; continue; }
          if (src.substr(j, q.length) === q) break;
          if (!q3 && (src[j] === '\n' || src[j] === '\r')) throw new Error('Line ' + line + ': newline in string');
          if (src[j] === '\n') line++;
          buf += src[j]; j++;
        }
        push('STR', unescapeStr(buf, line)); i = j + q.length; continue;
      }
      if (c === '@') {
        m = /^@([a-zA-Z]+(?:-[a-zA-Z0-9]+)*)/.exec(rest);
        if (!m) throw new Error('Line ' + line + ': bad @ token');
        if (m[1] === 'prefix' || m[1] === 'base') push(m[1].toUpperCase(), '@'); else push('LANG', m[1].toLowerCase());
        i += m[0].length; continue;
      }
      if (c === '^' && src[i + 1] === '^') { push('^^'); i += 2; continue; }
      if ('.;,[]()'.indexOf(c) >= 0) {
        // a '.' followed by a digit is a decimal number, handled below
        if (!(c === '.' && /[0-9]/.test(src[i + 1] || ''))) { push(c); i++; continue; }
      }
      if (c === '_' && src[i + 1] === ':') {
        m = /^_:([\p{L}\p{N}_](?:[\p{L}\p{N}_\-]|\.(?=[\p{L}\p{N}_\-]))*)/u.exec(rest);
        if (!m) throw new Error('Line ' + line + ': bad blank node');
        push('BNODE', m[1]); i += m[0].length; continue;
      }
      m = /^[+-]?(?:[0-9]+\.[0-9]*[eE][+-]?[0-9]+|\.[0-9]+[eE][+-]?[0-9]+|[0-9]+[eE][+-]?[0-9]+|[0-9]*\.[0-9]+|[0-9]+)/.exec(rest);
      if (m && (c !== '.' || /[0-9]/.test(src[i + 1]))) {
        var num = m[0], dt = /[eE]/.test(num) ? 'double' : (num.indexOf('.') >= 0 ? 'decimal' : 'integer');
        push('NUM', { v: num, dt: XSD + dt }); i += num.length; continue;
      }
      m = /^(PREFIX|BASE)\b/i.exec(rest);
      if (m && !/^[A-Za-z]+:/.test(rest)) { push(m[1].toUpperCase(), 'sparql'); i += m[0].length; continue; }
      m = /^(true|false)\b/.exec(rest);
      if (m && rest[m[0].length] !== ':') { push('BOOL', m[1]); i += m[0].length; continue; }
      m = /^a(?=[\s<\["'(_#])/.exec(rest);
      if (m) { push('A'); i += 1; continue; }
      m = PN_PREFIX.exec(rest);
      if (m) {
        var after = rest.slice(m[0].length), lm = PN_LOCAL.exec(after);
        var local = lm ? lm[1] : '';
        push('PNAME', { prefix: m[1] || '', local: unescapeLocal(local) });
        i += m[0].length + local.length; continue;
      }
      throw new Error('Line ' + line + ': unexpected "' + rest.slice(0, 20).split('\n')[0] + '"');
    }
    toks.push({ type: 'EOF', line: line });
    return toks;
  }

  function parseTurtle(text, opts) {
    var toks = tokenize(text), k = 0, base = (opts && opts.base) || '', prefixes = {}, triples = [], bn = 0;
    function peek() { return toks[k]; }
    function next() { return toks[k++]; }
    function expect(type) { var t = next(); if (t.type !== type) throw new Error('Line ' + t.line + ': expected ' + type + ', found ' + t.type); return t; }
    function fresh() { return { t: 'bnode', v: 'b' + (++bn) }; }
    function iriOf(t) {
      if (t.type === 'IRI') return { t: 'iri', v: resolve(t.val, base) };
      if (t.type === 'PNAME') {
        if (!(t.val.prefix in prefixes)) throw new Error('Line ' + t.line + ': undefined prefix "' + t.val.prefix + ':"');
        return { t: 'iri', v: prefixes[t.val.prefix] + t.val.local };
      }
      return null;
    }
    function emit(s, p, o) { triples.push({ s: s, p: p, o: o }); }

    function collection() {
      var items = [];
      while (peek().type !== ')') { if (peek().type === 'EOF') throw new Error('Unterminated collection'); items.push(object()); }
      next();
      if (!items.length) return { t: 'iri', v: RDF + 'nil' };
      var head = fresh(), cur = head;
      items.forEach(function (it, idx) {
        emit(cur, { t: 'iri', v: RDF + 'first' }, it);
        var nx = idx === items.length - 1 ? { t: 'iri', v: RDF + 'nil' } : fresh();
        emit(cur, { t: 'iri', v: RDF + 'rest' }, nx);
        cur = nx;
      });
      return head;
    }
    function bnodePropList() {
      var b = fresh();
      if (peek().type !== ']') predicateObjectList(b);
      expect(']');
      return b;
    }
    function object() {
      var t = next();
      var iri = iriOf(t); if (iri) return iri;
      switch (t.type) {
        case 'BNODE': return { t: 'bnode', v: 'u_' + t.val };
        case '[': return bnodePropList();
        case '(': return collection();
        case 'NUM': return { t: 'lit', v: t.val.v, dt: t.val.dt };
        case 'BOOL': return { t: 'lit', v: t.val, dt: XSD + 'boolean' };
        case 'STR':
          var lit = { t: 'lit', v: t.val };
          if (peek().type === 'LANG') lit.lang = next().val;
          else if (peek().type === '^^') { next(); var d = iriOf(next()); if (!d) throw new Error('Line ' + t.line + ': bad datatype'); lit.dt = d.v; }
          return lit;
      }
      throw new Error('Line ' + t.line + ': unexpected ' + t.type + ' in object position');
    }
    function verb() {
      var t = next();
      if (t.type === 'A') return { t: 'iri', v: RDF + 'type' };
      var iri = iriOf(t); if (iri) return iri;
      throw new Error('Line ' + t.line + ': expected a predicate, found ' + t.type);
    }
    function predicateObjectList(s) {
      while (true) {
        var p = verb();
        emit(s, p, object());
        while (peek().type === ',') { next(); emit(s, p, object()); }
        if (peek().type !== ';') return;
        while (peek().type === ';') next();
        var ty = peek().type;
        if (ty === '.' || ty === ']' || ty === 'EOF') return;
      }
    }
    while (peek().type !== 'EOF') {
      var t = peek();
      if (t.type === 'PREFIX') {
        next();
        var pn = next(); if (pn.type !== 'PNAME' || pn.val.local) throw new Error('Line ' + pn.line + ': bad prefix declaration');
        var iri = expect('IRI'); prefixes[pn.val.prefix] = resolve(iri.val, base);
        if (t.val === '@') expect('.');
        continue;
      }
      if (t.type === 'BASE') {
        next(); base = resolve(expect('IRI').val, base);
        if (t.val === '@') expect('.');
        continue;
      }
      var subj;
      next();
      if (t.type === '[') {
        subj = bnodePropList();
        if (peek().type === '.') { next(); continue; }
      } else if (t.type === '(') {
        subj = collection();
      } else if (t.type === 'BNODE') {
        subj = { t: 'bnode', v: 'u_' + t.val };
      } else {
        subj = iriOf(t);
        if (!subj) throw new Error('Line ' + t.line + ': expected a subject, found ' + t.type);
      }
      predicateObjectList(subj);
      expect('.');
    }
    return { triples: triples, prefixes: prefixes };
  }

  root.parseTurtle = parseTurtle;
  if (typeof module !== 'undefined') module.exports = { parseTurtle: parseTurtle };
})(typeof window !== 'undefined' ? window : globalThis);
