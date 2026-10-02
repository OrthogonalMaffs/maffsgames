// Read-only instrumentation, test-only, never committed. Traps the global
// `katex` the CDN script sets, and wraps render/renderToString so every string
// handed to KaTeX is logged once with its options, its caller stack and the
// visual text KaTeX actually produced (.katex-html only: the hidden MathML
// annotation keeps the source's spaces and would mask the defect).
(function () {
  if (window.__kxHooked) return;
  window.__kxHooked = true;
  var seen = Object.create(null);
  function frames() {
    var st = (new Error()).stack || '';
    var out = [];
    st.split('\n').slice(3).forEach(function (l) {
      var m = l.match(/at (?:(.*?) \()?(.*?):(\d+):(\d+)\)?\s*$/);
      if (!m) return;
      var file = m[2].replace(/^https?:\/\/[^/]+/, '').replace(/\?.*$/, '');
      if (/kx_hook|katex(\.min)?\.js/.test(file)) return;
      out.push({fn: m[1] || '(anon)', file: file, line: +m[3]});
    });
    return out.slice(0, 8);
  }
  function visualOf(node) {
    var v = node && node.querySelector ? node.querySelector('.katex-html') : null;
    return v ? v.textContent : (node ? node.textContent : '');
  }
  function log(kind, s, opts, visual) {
    var fr = frames();
    var key = kind + '\u0001' + s + '\u0001' + (opts && opts.displayMode ? 1 : 0) + '\u0001' +
      (fr[0] ? fr[0].file + ':' + fr[0].line : '') + '\u0001' + (fr[1] ? fr[1].line : '') + '\u0001' + (window.__kxMode || '');
    if (seen[key]) return;
    seen[key] = 1;
    try {
      if (window.__kxlog) window.__kxlog({kind: kind, s: String(s), display: !!(opts && opts.displayMode),
        visual: visual, frames: fr, mode: window.__kxMode || null});
    } catch (e) {}
  }
  function wrap(k) {
    if (!k || k.__kxWrapped) return k;
    var rts = k.renderToString, r = k.render;
    k.renderToString = function (s, opts) {
      var out = rts.apply(this, arguments);
      try {
        var t = document.createElement('template');
        t.innerHTML = out;
        log('renderToString', s, opts, visualOf(t.content));
      } catch (e) {}
      return out;
    };
    k.render = function (s, el, opts) {
      var out = r.apply(this, arguments);
      try { log('render', s, opts, visualOf(el)); } catch (e) {}
      return out;
    };
    k.__kxWrapped = true;
    return k;
  }
  var real;
  try {
    Object.defineProperty(window, 'katex', {
      configurable: true,
      get: function () { return real; },
      set: function (v) { real = wrap(v); }
    });
  } catch (e) {}
})();
