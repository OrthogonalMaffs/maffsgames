/* MaffsLargeScreen: a game fills a large screen (SR-34's goal; contract LARGE-SCREEN-LAYER, 26 Nov 2026).
 *
 * Most games lay out in a 680-900 px column, so on a 1920 px screen two thirds is empty and the text is small. This
 * scales the whole page up with CSS zoom on <html>, choosing the zoom for THIS page and THIS window when the page
 * loads and whenever the window changes size. A page gets it from one tag, written just before </head> by
 * scripts/apply-large-screen.py from the lists in scripts/check-large-screen.py and from data/large-screen.json:
 *
 *   <script src="/schools/assets/large-screen.js" data-need="742" data-pointer="none"></script>
 *
 *   data-need     the page's measured height need in CSS px (scripts/measure-large-screen.py): the lowest edge of
 *                 the answer controls, and of Next after an answer, on every screen the measurement reached.
 *   data-pointer  "none": the page reads no pointer position. "verified": it does, and a measured drag test under
 *                 zoom is on the check's POINTER_VERIFIED list. "held": it does, and is not verified.
 *
 * The zoom is the largest z, rounded DOWN to a step of 0.05, that meets every rule; under 1.1 there is no zoom.
 *
 *   a. Only on big screens: no zoom when the window is under 1500 px wide.
 *   b. The laptop floor (Jon, 26 Nov 2026, Amendment 1): the effective window (window / z) is never smaller than
 *      1280 x 720, the smallest laptop size every game is already verified at. So whatever holds on a 1280 x 720
 *      laptop (answer controls and Next above the fold, a start screen a game fits to the window) holds zoomed.
 *   c. Never across the page's own breakpoints. Media queries read the real window while a zoomed page is laid out in
 *      window / z px, so for every width and height threshold T in the page's readable stylesheets, window / z stays
 *      on the same side of T as the window itself: every media query then answers as it would on an unzoomed
 *      window of the effective size. Cross-origin sheets (KaTeX, Google Fonts) cannot be read and are skipped; a
 *      same-origin sheet that cannot be read, or a size condition this cannot parse, means no zoom.
 *   d. Height budget: window height / z >= data-need, for a game whose answer controls and Next need more than 720.
 *   e. Pointer safety: under zoom a pointer's clientX is in screen px while style.left is in zoomed px, so a page
 *      that positions things from the pointer is zoomed only when data-pointer is "verified". No tag value, or
 *      "held", means no zoom; so does a page marked "none" whose inline script turns out to read the pointer.
 *   f. At most 1.6.
 *
 * Viewport units. Under zoom 1vh is still 1% of the real window in CSS px, and CSS px are drawn z times larger, so
 * 100vh ends z times below the bottom of the screen. While zoomed, every vh / vw / vmin / vmax length in the page's
 * readable style rules is divided by z in place (through the CSSOM, never the file) and put back when the zoom
 * changes, so body{min-height:100vh} still ends at the bottom of the screen.
 *
 * Engines. Everything above assumes what Chromium does: under zoom on <html>, innerWidth and innerHeight keep the
 * real window, getBoundingClientRect answers in screen px, and viewport units are zoomed. After setting a zoom this
 * measures a probe element; if the engine answers any other way the zoom is taken off again (reason "engine").
 *
 * Opt out: <html data-large-screen="off">, only with a reason in the check's OPT_OUT list.
 *
 * window.MaffsLargeScreen.state() reports the zoom, the rule that limited it and what was read (for the check).
 */
(function () {
  'use strict';
  var MIN_W = 1500, EFF_W = 1280, EFF_H = 720, MAX_Z = 1.6, MIN_Z = 1.1, STEPS = 20, EPS = 1e-9;
  var doc = document, root = doc.documentElement;
  var tag = doc.currentScript;
  var need = tag ? parseFloat(tag.getAttribute('data-need')) : NaN;
  var pointer = tag ? tag.getAttribute('data-pointer') : null;
  var applied = 1, patched = [], state = { zoom: 1, by: 'not run' };

  // ---- the page's own breakpoints, through the CSSOM
  var UNIT = { px: 1, em: 16, rem: 16 };
  var CLASSIC = /(min|max)-(?:device-)?(width|height)\s*:\s*([\d.]+)(px|r?em)?(?![\w.%])/g;
  var RANGE_A = /\b(?:device-)?(width|height)\s*(<=|>=|<|>)\s*([\d.]+)(px|r?em)\b/g;      // (width >= 600px)
  var RANGE_B = /([\d.]+)(px|r?em)\s*(<=|>=|<|>)\s*(?:device-)?(width|height)\b/g;         // (600px <= width)
  var FEATURE = /(?:^|[^a-z-])((?:min-|max-)?(?:device-)?(?:width|height))\b/g;
  var FLIP = { '<': '>', '>': '<', '<=': '>=', '>=': '<=' };
  var KIND = { '>=': 'ge', '<=': 'le', '>': 'gt', '<': 'lt' };

  // Every size threshold in one media query list; ok false when it holds a size condition this did not read.
  function parseMedia(text) {
    var t = String(text || '').toLowerCase(), out = [], m, features = 0, bad = 0;
    FEATURE.lastIndex = 0;
    while (FEATURE.exec(t)) features++;
    CLASSIC.lastIndex = 0;
    while ((m = CLASSIC.exec(t))) {
      if (!m[4] && parseFloat(m[3]) !== 0) bad++;                // a length with no unit is only ever 0
      out.push({ dim: m[2], kind: m[1] === 'min' ? 'ge' : 'le', t: parseFloat(m[3]) * (UNIT[m[4]] || 0) });
    }
    RANGE_A.lastIndex = 0;
    while ((m = RANGE_A.exec(t))) out.push({ dim: m[1], kind: KIND[m[2]], t: parseFloat(m[3]) * UNIT[m[4]] });
    RANGE_B.lastIndex = 0;
    while ((m = RANGE_B.exec(t))) out.push({ dim: m[4], kind: KIND[FLIP[m[3]]], t: parseFloat(m[1]) * UNIT[m[2]] });
    return { list: out, ok: !bad && out.length >= features };
  }

  function sameOrigin(href) {
    try { return new URL(href, location.href).origin === location.origin; } catch (e) { return false; }
  }

  // Walk every readable rule. onMedia(text) for each media condition; onStyle(style) for each declaration block.
  function walkSheets(onMedia, onStyle, problems) {
    function rules(list) {
      for (var i = 0; list && i < list.length; i++) {
        var r = list[i];
        if (r.media && r.media.mediaText) onMedia(r.media.mediaText);                         // @media, @import
        if (r.styleSheet) sheet(r.styleSheet, r.href);                                        // @import
        if (r.style && onStyle) onStyle(r.style);
        if (r.cssRules) rules(r.cssRules);
      }
    }
    function sheet(s, href) {
      href = s.href || href || '';
      if (s.media && s.media.mediaText) onMedia(s.media.mediaText);
      var list;
      try { list = s.cssRules; } catch (e) { list = null; }
      if (!list) {
        if (!href || sameOrigin(href)) problems.push('unreadable stylesheet ' + (href || '(inline)'));
        return;                                                    // cross-origin: skipped by rule c
      }
      rules(list);
    }
    for (var i = 0; i < doc.styleSheets.length; i++) sheet(doc.styleSheets[i]);
  }

  function readThresholds() {
    var seen = {}, list = [], problems = [];
    walkSheets(function (text) {
      var p = parseMedia(text);
      if (!p.ok) problems.push('unread size condition in "' + text + '"');
      p.list.forEach(function (x) {
        var key = x.dim + x.kind + x.t;
        if (!seen[key] && x.t > 0) { seen[key] = 1; list.push(x); }
      });
    }, null, problems);
    return { list: list, problems: problems };
  }

  // ---- the rule
  // The largest whole number of steps k (z = k / STEPS) with z <= limit, or z < limit when strict.
  function steps(limit, strict) {
    return strict ? Math.ceil(limit * STEPS - EPS) - 1 : Math.floor(limit * STEPS + EPS);
  }

  function choose(W, H, th) {
    if (root.getAttribute('data-large-screen') === 'off') return { zoom: 1, by: 'opt-out' };
    if (W < MIN_W) return { zoom: 1, by: 'a: window under ' + MIN_W + ' px wide' };
    if (!(need > 0)) return { zoom: 1, by: 'd: no measured height need on the tag' };
    if (pointer !== 'none' && pointer !== 'verified') return { zoom: 1, by: 'e: pointer use not verified' };
    if (!window.CSS || !CSS.supports || !CSS.supports('zoom', '1.2')) return { zoom: 1, by: 'engine: no CSS zoom' };
    if (th.problems.length) return { zoom: 1, by: 'c: ' + th.problems[0] };
    var best = { k: steps(MAX_Z, false), by: 'f: upper limit ' + MAX_Z };
    function cap(k, by) { if (k < best.k) best = { k: k, by: by }; }
    cap(steps(W / EFF_W, false), 'b: effective width ' + EFF_W);
    cap(steps(H / EFF_H, false), 'b: effective height ' + EFF_H);
    cap(steps(H / need, false), 'd: height need ' + need);
    th.list.forEach(function (x) {
      var v = x.dim === 'width' ? W : H;
      var name = (x.kind === 'ge' ? 'min-' + x.dim + ':' : x.kind === 'le' ? 'max-' + x.dim + ':' : x.dim + (x.kind === 'gt' ? ' > ' : ' < ')) + x.t + 'px';
      // ge and lt change answer AT T (v >= T against v < T): the effective size may equal T. le and gt change just
      // above T: the effective size must stay above it.
      if ((x.kind === 'ge' || x.kind === 'lt') && v >= x.t) cap(steps(v / x.t, false), 'c: breakpoint ' + name);
      if ((x.kind === 'le' || x.kind === 'gt') && v > x.t) cap(steps(v / x.t, true), 'c: breakpoint ' + name);
    });
    var z = best.k / STEPS;
    if (z < MIN_Z - EPS) return { zoom: 1, by: best.by, held: 'under ' + MIN_Z };
    return { zoom: z, by: best.by };
  }

  // ---- viewport units, divided back by z in place
  var VUNIT = /(-?\d*\.?\d+)([sld]?v(?:h|w|min|max))\b/g;
  function unpatch() {
    patched.forEach(function (p) { try { p.style.setProperty(p.prop, p.value, p.priority); } catch (e) { /* rule gone */ } });
    patched = [];
  }
  function patchUnits(z) {
    walkSheets(function () {}, function (style) {
      for (var i = 0; i < style.length; i++) {
        var prop = style[i], value = style.getPropertyValue(prop);
        VUNIT.lastIndex = 0;
        if (!value || !VUNIT.test(value)) continue;
        VUNIT.lastIndex = 0;
        var priority = style.getPropertyPriority(prop);
        try {
          style.setProperty(prop, value.replace(VUNIT, 'calc($1$2 / ' + z + ')'), priority);
          patched.push({ style: style, prop: prop, value: value, priority: priority });
        } catch (e) { /* a read-only rule: left as it is */ }
      }
    }, []);
  }

  // ---- does this engine zoom the way the rule assumes?
  function engineOk(z, W, H) {
    var p = doc.createElement('div');
    p.style.cssText = 'position:absolute;left:0;top:0;width:100px;height:100vh;visibility:hidden;pointer-events:none';
    root.appendChild(p);
    var r = p.getBoundingClientRect();
    root.removeChild(p);
    var near = function (a, b) { return Math.abs(a - b) <= 1; };
    if (!near(window.innerWidth, W) || !near(window.innerHeight, H)) return 'engine: the window size changes under zoom';
    if (!near(r.width, 100 * z)) return 'engine: getBoundingClientRect is not in screen px under zoom (' + r.width + ' for ' + (100 * z) + ')';
    if (near(r.height, H * z)) return 'vh zoomed';
    if (near(r.height, H)) return 'vh not zoomed';
    return 'engine: 100vh is ' + r.height + ' px under zoom ' + z + ' on a ' + H + ' px window';
  }

  var unitsMode = null;
  function set(z) {
    unpatch();
    unitsMode = null;
    if (z > 1) { root.style.zoom = String(z); root.style.setProperty('--maffs-large-zoom', String(z)); }
    else { root.style.removeProperty('zoom'); root.style.removeProperty('--maffs-large-zoom'); }
    applied = z;
  }

  function inlinePointerUse() {
    var s = doc.scripts;
    for (var i = 0; i < s.length; i++) {
      if (!s[i].src && /\b(?:client|page)[XY]\b/.test(s[i].textContent || '')) return true;
    }
    return false;
  }

  function run() {
    // The window's size and the sheets' conditions read the same zoomed or not (engineOk holds the engine to that),
    // so nothing is unzoomed to measure: a second run that chooses the same zoom changes nothing on screen.
    var W = window.innerWidth, H = window.innerHeight, th = readThresholds();
    var c = choose(W, H, th);
    if (c.zoom > 1 && pointer === 'none' && inlinePointerUse()) c = { zoom: 1, by: 'e: the page reads the pointer and its tag says it does not' };
    if (c.zoom !== applied) {
      set(c.zoom);
      if (c.zoom > 1) {
        var e = engineOk(c.zoom, W, H);
        if (e.indexOf('engine') === 0) { set(1); c = { zoom: 1, by: e, wanted: c.zoom }; }
        else unitsMode = e;
      }
    }
    unpatch();                                          // rules that arrived since the last run are divided too
    if (applied > 1 && unitsMode === 'vh zoomed') patchUnits(applied);
    state = { zoom: applied, by: c.by, held: c.held || null, wanted: c.wanted || null, units: unitsMode, window: [W, H],
              need: need > 0 ? need : null, pointer: pointer, thresholds: th.list, problems: th.problems, patched: patched.length };
    return state;
  }

  var queued = false;
  function later() {
    if (queued) return;
    queued = true;
    (window.requestAnimationFrame || window.setTimeout)(function () { queued = false; run(); });
  }

  run();
  window.addEventListener('resize', later);
  // Sheets and scripts further down the page are not there yet when the tag runs: read again once they are.
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', run);
  window.addEventListener('load', run);

  window.MaffsLargeScreen = {
    state: function () { return JSON.parse(JSON.stringify(state)); },
    refresh: run
  };
})();
