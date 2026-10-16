/* ==========================================================================
   KE Workbench bridge — loaded at the top of every tool page.
   1. Theme: applies data-theme="light|dark" on <html> and keeps it in sync
      with the workbench (postMessage + storage event).
   2. Navigation: inside the workbench, window.open()/window.close() and
      target="_blank" links to local tool pages become workbench tabs.
   3. Settings: the workbench repository ID is handed to tools that have a
      #repoId field.
   Pages still work stand-alone: without the shell, nothing is intercepted.
   ========================================================================== */
(function () {
  var root = document.documentElement;
  var LS_THEME = 'ke-theme', LS_REPO = 'ke-repo';

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  function initialTheme() {
    var t = lsGet(LS_THEME);
    if (t === 'light' || t === 'dark') return t;
    try { return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; } catch (e) { return 'light'; }
  }
  function applyTheme(t) {
    if (t !== 'light' && t !== 'dark') return;
    root.setAttribute('data-theme', t);
    root.style.colorScheme = t;
    try { document.dispatchEvent(new CustomEvent('ke-theme', { detail: t })); } catch (e) {}
  }
  applyTheme(initialTheme());

  window.addEventListener('message', function (ev) {
    var d = ev.data;
    if (!d || typeof d !== 'object') return;
    if (d.type === 'ke-theme') applyTheme(d.theme);
  });
  window.addEventListener('storage', function (ev) {
    if (ev.key === LS_THEME && ev.newValue) applyTheme(ev.newValue);
  });

  // ── Am I inside the workbench shell? ──────────────────────────────────────
  var shell = null;
  try { if (window.top !== window && window.top.KE_SHELL) shell = window.top; } catch (e) { shell = null; }
  if (!shell) return;
  root.classList.add('ke-embedded');
  var directChild = (window.parent === window.top);

  function toAbs(url) { try { return new URL(url, location.href); } catch (e) { return null; } }
  function isLocalPage(u) {
    return u && u.origin === location.origin && /\.(html?|pdf)$/i.test(u.pathname);
  }
  function openInShell(u, name) {
    shell.postMessage({ type: 'ke-open', url: u.pathname + u.search + u.hash, name: name || '' }, '*');
  }

  // window.open → workbench tab. Returns a stand-in so "popup blocked" checks pass.
  var nativeOpen = window.open;
  window.open = function (url, name, features) {
    var u = toAbs(url || '');
    if (isLocalPage(u)) {
      openInShell(u, name);
      return { closed: false, focus: function () {}, close: function () {}, postMessage: function () {} };
    }
    return nativeOpen.apply(window, arguments);
  };

  // window.close → close this workbench tab (only for top-level tool frames;
  // nested frames such as the metadata editor inside Model Manager keep the
  // browser's normal no-op behaviour).
  if (directChild) {
    window.close = function () { shell.postMessage({ type: 'ke-close' }, '*'); };
  }

  // target=_blank links to local pages → workbench tab
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a || ev.defaultPrevented || ev.button !== 0 || ev.metaKey || ev.ctrlKey || ev.shiftKey) return;
    var u = toAbs(a.getAttribute('href'));
    if (a.target === '_blank' && isLocalPage(u)) { ev.preventDefault(); openInShell(u, ''); }
  }, true);

  // Shared repository ID
  document.addEventListener('DOMContentLoaded', function () {
    var repo = lsGet(LS_REPO);
    var el = document.getElementById('repoId');
    if (repo && el && el.tagName === 'INPUT' && !new URLSearchParams(location.search).get('repo')) el.value = repo;
    if (directChild) shell.postMessage({ type: 'ke-title', title: document.title }, '*');
  });
})();
