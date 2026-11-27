/* MaffsPlot: one pair of axes and the curves on it, drawn in SVG. One copy, for every game that only draws a graph
 * (Jon, 27 Nov 2026; contract D-BY-DX-GRAPH).
 *
 * WHY THIS EXISTS
 * ---------------
 * Y So Steep?, Graph Transformer, Graph Sketcher and Gradient Hunter each draw axes, a curve and labels on a canvas
 * of their own: the same job done four times, in four ways. This is the one plotter for that job. No canvas, no
 * library: an <svg> that scales with its box, and KaTeX (which the page already loads) for every piece of text.
 *
 * WHO USES IT
 * -----------
 *   games/d-by-dx-why/   the question's graph (f, then the gradient function f' drawn in over it once answered) and
 *                        the start screen (two pens drawing f and f' together).
 *   Still to come: integration's check step in the same game, and the four graphing games above where they only draw
 *   (docs/todo.md, PLOT-MIGRATE). Their dragging and tapping stays in their own pages: this reads no pointer.
 *
 * WHAT IT DRAWS
 * -------------
 *   var plot = MaffsPlot.create(mount, {
 *     x: [x0, x1], y: [y0, y1],    the window. The caller gives it; this never chooses one.
 *     ticks: 'num' | 'pi',         x ticks at nice numbers (1, 2 or 5 times a power of ten), or at multiples of pi/2
 *     xLabel: 't', yLabel: 's',    the axis letters, in TeX
 *     aria: 'Graph of ...'         what a screen reader is told (the picture is one image to it)
 *   });
 *   plot.add('f', fn, { tone: 1, label: 'f(t)' });                      a curve, there at once
 *   plot.add('d', fn, { tone: 2, label: "f'(t)", reveal: true });       a curve that draws in, left to right (0.6 s)
 *   plot.pens([{ id, fn, tone, label }, ...], { duration, hold, onLand, onDone });   curves drawn together at the same
 *                                    x, each with a blinking tip; onLand runs as they finish, onDone `hold` ms later
 *   plot.remove(id)  plot.clear()  plot.reset(opts)  plot.finish()  plot.pause()  plot.resume()  plot.destroy()
 *   plot.describe(text)              change what a screen reader is told
 *   plot.state()                     the window, the box and each curve's progress (for a verifier)
 *
 *   - Axes go through 0 where 0 is in the window, otherwise along the edge nearer 0; a light grid and ticks at the
 *     same steps. Tick labels, the axis letters and each curve's label (at the curve's right-hand end, in the curve's
 *     colour) are KaTeX in an HTML layer over the SVG.
 *   - A curve is a function of one number, sampled at least once for every 2 px of width. A value that is not finite
 *     breaks the line: the two sides are never joined across it.
 *   - Animation runs on animation frames, only while the plot is on screen and the tab is showing (a hidden tab or a
 *     closed fold-out pauses it, and it carries on from where it was). With prefers-reduced-motion nothing animates:
 *     a curve is there at once, pens have no tips.
 *
 * COLOURS
 * -------
 * From the page's CSS variables, with currentColor where a page sets none:
 *   --maffs-plot-1, --maffs-plot-2   the two curve tones (a page chooses each at 3:1 or better on its background)
 *   --maffs-plot-axis, --maffs-plot-grid
 * The tones never differ by colour alone: tone 2 is drawn wider, and a curve given `dash: true` is dashed.
 *
 * FOR A VERIFIER
 * --------------
 * The <svg> has a viewBox of 0 0 480 340. Each curve's <path class="maffs-plot-curve"> carries data-curve (its id),
 * data-tone, data-progress (0 to 1), the window as data-x0, data-x1, data-y0, data-y1 and the plot box as data-box
 * ("left top width height", viewBox units), so a point (px, py) of its `d` maps back to
 *   x = x0 + (px - left) / width * (x1 - x0),   y = y1 - (py - top) / height * (y1 - y0).
 * A pen's tip is <circle class="maffs-plot-tip" data-curve="..."> at the same coordinates.
 */
(function () {
  'use strict';
  if (window.MaffsPlot) return;

  var NS = 'http://www.w3.org/2000/svg';
  var VW = 480, VH = 340;                               // the viewBox
  var BOX = { l: 46, t: 28, w: 364, h: 280 };           // the plot box inside it: room for labels left, right, above, below
  var REVEAL_MS = 600;
  var uid = 0;

  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function injectStyleOnce() {
    if (document.getElementById('maffs-plot-style')) return;
    var st = document.createElement('style');
    st.id = 'maffs-plot-style';
    st.textContent =
      '.maffs-plot{position:relative;width:100%;container-type:inline-size;line-height:1;}' +
      '.maffs-plot-svg{display:block;width:100%;height:auto;overflow:visible;}' +
      '.maffs-plot-grid line{stroke:var(--maffs-plot-grid,currentColor);stroke-opacity:.16;stroke-width:1;}' +
      '.maffs-plot-axes line{stroke:var(--maffs-plot-axis,currentColor);stroke-opacity:.8;stroke-width:1.6;}' +
      '.maffs-plot-axes polygon{fill:var(--maffs-plot-axis,currentColor);fill-opacity:.8;}' +
      '.maffs-plot-curve{fill:none;stroke-linecap:round;stroke-linejoin:round;}' +
      '.maffs-plot-curve[data-tone="1"]{stroke:var(--maffs-plot-1,currentColor);stroke-width:2.6;}' +
      '.maffs-plot-curve[data-tone="2"]{stroke:var(--maffs-plot-2,currentColor);stroke-width:4.4;}' +
      '.maffs-plot-curve[data-dash]{stroke-dasharray:11 7;}' +
      '.maffs-plot-tip{stroke:none;animation:maffs-plot-blink .8s ease-in-out infinite;}' +
      '.maffs-plot-tip[data-tone="1"]{fill:var(--maffs-plot-1,currentColor);}' +
      '.maffs-plot-tip[data-tone="2"]{fill:var(--maffs-plot-2,currentColor);}' +
      '@keyframes maffs-plot-blink{0%,100%{opacity:1;}50%{opacity:.3;}}' +
      '.maffs-plot-labels{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;' +
      'font-size:11px;font-size:clamp(10.5px,3.3cqw,15px);}' +
      '.maffs-plot-labels>span{position:absolute;white-space:nowrap;}' +
      '.maffs-plot-labels .katex{font-size:1em;}' +
      '.maffs-plot-tick{color:var(--maffs-plot-axis,currentColor);opacity:.9;}' +
      '.maffs-plot-tick-x{transform:translate(-50%,0);}' +
      '.maffs-plot-tick-y{transform:translate(-100%,-50%);}' +
      '.maffs-plot-letter{font-size:1.2em;color:var(--maffs-plot-axis,currentColor);}' +
      '.maffs-plot-letter-x{transform:translate(0,-50%);}' +
      '.maffs-plot-letter-y{transform:translate(-50%,-100%);}' +
      '.maffs-plot-name{font-size:1.2em;font-weight:700;transform:translate(0,-50%);opacity:0;transition:opacity .25s;}' +
      '.maffs-plot-name.is-on{opacity:1;}' +
      '.maffs-plot-name[data-tone="1"]{color:var(--maffs-plot-1,currentColor);}' +
      '.maffs-plot-name[data-tone="2"]{color:var(--maffs-plot-2,currentColor);}' +
      '@media (prefers-reduced-motion: reduce){.maffs-plot-tip{animation:none;}.maffs-plot-name{transition:none;}}';
    document.head.appendChild(st);
  }

  function svg(name, attrs, parent) {
    var el = document.createElementNS(NS, name);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  }
  function num(v) { return (Math.round(v * 100) / 100).toString(); }

  // TeX into an element: KaTeX where the page has it, the bare string where it does not.
  function tex(el, s) {
    if (window.katex && typeof window.katex.render === 'function') {
      try { window.katex.render(String(s), el, { throwOnError: false }); return; } catch (e) { /* fall through */ }
    }
    el.textContent = String(s);
  }

  /* A step of 1, 2 or 5 times a power of ten that gives at most `most` gaps across the span. */
  function niceStep(span, most) {
    var raw = span / most, p = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / p;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p;
  }
  // The multiples of step in [lo, hi], each with its label in TeX.
  function numTicks(lo, hi, most) {
    var step = niceStep(hi - lo, most), dec = Math.max(0, -Math.floor(Math.log(step) / Math.LN10 + 1e-9));
    var out = [], eps = step * 1e-6;
    for (var k = Math.ceil((lo - eps) / step); k * step <= hi + eps; k++) {
      var v = k * step;
      out.push({ v: v, tex: String(parseFloat(v.toFixed(dec))) });
    }
    return out;
  }
  // Multiples of pi/2 (of pi, or of 2 pi, when there would be more than eight), each named in pi.
  function piTicks(lo, hi) {
    var h = Math.PI / 2, m = 1;
    while ((hi - lo) / (h * m) > 8) m *= 2;
    var out = [], eps = 1e-9;
    for (var k = Math.ceil(lo / (h * m) - eps); k * h * m <= hi + eps; k++) {
      var n = k * m;                                   // the tick is n times pi/2
      var a = Math.abs(n), sign = n < 0 ? '-' : '', t;
      if (n === 0) t = '0';
      else if (a % 2 === 0) t = sign + (a === 2 ? '' : String(a / 2)) + '\\pi';
      else t = sign + '\\frac{' + (a === 1 ? '' : String(a)) + '\\pi}{2}';
      out.push({ v: n * h, tex: t });
    }
    return out;
  }

  function create(mount, opts) {
    if (!mount) return null;
    injectStyleOnce();
    var id = 'maffs-plot-' + (++uid);
    var root = document.createElement('div');
    root.className = 'maffs-plot';
    root.setAttribute('role', 'img');
    mount.appendChild(root);

    var win, el, layer, curves = [], anim = null, frame = 0, last = 0;
    var held = false, seen = true, destroyed = false, io = null, ro = null;

    function X(x) { return BOX.l + (x - win.x0) / (win.x1 - win.x0) * BOX.w; }
    function Y(y) { return BOX.t + (win.y1 - y) / (win.y1 - win.y0) * BOX.h; }
    function pct(v, of) { return (v / of * 100).toFixed(3) + '%'; }
    function span(cls, left, top, s) {
      var e = document.createElement('span');
      e.className = cls;
      e.style.left = pct(left, VW);
      e.style.top = pct(top, VH);
      if (s != null) tex(e, s);
      layer.appendChild(e);
      return e;
    }

    function build(o) {
      o = o || {};
      win = { x0: +o.x[0], x1: +o.x[1], y0: +o.y[0], y1: +o.y[1], ticks: o.ticks === 'pi' ? 'pi' : 'num' };
      stopAnim();
      curves = [];
      root.innerHTML = '';
      root.setAttribute('aria-label', o.aria || 'A graph');
      el = svg('svg', { 'class': 'maffs-plot-svg', viewBox: '0 0 ' + VW + ' ' + VH, 'aria-hidden': 'true', focusable: 'false' }, root);
      var defs = svg('defs', {}, el);
      svg('rect', { x: BOX.l, y: BOX.t, width: BOX.w, height: BOX.h }, svg('clipPath', { id: id + '-box' }, defs));
      el._defs = defs;
      layer = document.createElement('div');
      layer.className = 'maffs-plot-labels';
      layer.setAttribute('aria-hidden', 'true');
      root.appendChild(layer);

      // The axes: through 0 where 0 is in the window, otherwise along the edge nearer 0.
      var ax = win.y0 <= 0 && 0 <= win.y1 ? 0 : (win.y0 > 0 ? win.y0 : win.y1);     // the x-axis is the line y = ax
      var ay = win.x0 <= 0 && 0 <= win.x1 ? 0 : (win.x0 > 0 ? win.x0 : win.x1);     // the y-axis is the line x = ay
      var both = ax === 0 && ay === 0;                  // the axes cross at 0: it is written once at most
      var xt = win.ticks === 'pi' ? piTicks(win.x0, win.x1) : numTicks(win.x0, win.x1, 5);
      var yt = numTicks(win.y0, win.y1, 6);
      var grid = svg('g', { 'class': 'maffs-plot-grid' }, el), axes = svg('g', { 'class': 'maffs-plot-axes' }, el);
      var b = BOX.t + BOX.h, r = BOX.l + BOX.w, i, t;
      for (i = 0; i < xt.length; i++) {
        t = xt[i];
        svg('line', { x1: num(X(t.v)), y1: BOX.t, x2: num(X(t.v)), y2: b, 'data-grid': 'x' }, grid);
        svg('line', { x1: num(X(t.v)), y1: num(Y(ax) - 4), x2: num(X(t.v)), y2: num(Y(ax) + 4), 'data-tick': 'x', 'data-v': t.v }, axes);
        if (both && Math.abs(t.v) < 1e-9) continue;      // never under the crossing: the y-axis's 0 stands for both
        span('maffs-plot-tick maffs-plot-tick-x', X(t.v), Y(ax) + 7, t.tex).setAttribute('data-v', t.v);
      }
      for (i = 0; i < yt.length; i++) {
        t = yt[i];
        svg('line', { x1: BOX.l, y1: num(Y(t.v)), x2: r, y2: num(Y(t.v)), 'data-grid': 'y' }, grid);
        svg('line', { x1: num(X(ay) - 4), y1: num(Y(t.v)), x2: num(X(ay) + 4), y2: num(Y(t.v)), 'data-tick': 'y', 'data-v': t.v }, axes);
        if (both && win.x0 < 0 && Math.abs(t.v) < 1e-9) continue;   // nor on the x-axis's own line, when the y-axis is inside the window
        span('maffs-plot-tick maffs-plot-tick-y', X(ay) - 7, Y(t.v), t.tex).setAttribute('data-v', t.v);
      }
      svg('line', { x1: BOX.l, y1: num(Y(ax)), x2: r + 6, y2: num(Y(ax)), 'data-axis': 'x', 'data-at': ax }, axes);
      svg('line', { x1: num(X(ay)), y1: b, x2: num(X(ay)), y2: BOX.t - 6, 'data-axis': 'y', 'data-at': ay }, axes);
      svg('polygon', { points: [r + 12, Y(ax), r + 4, Y(ax) - 4, r + 4, Y(ax) + 4].map(num).join(' ') }, axes);
      svg('polygon', { points: [X(ay), BOX.t - 12, X(ay) - 4, BOX.t - 4, X(ay) + 4, BOX.t - 4].map(num).join(' ') }, axes);
      if (o.xLabel != null) span('maffs-plot-letter maffs-plot-letter-x', r + 16, Y(ax), o.xLabel).setAttribute('data-axis', 'x');
      if (o.yLabel != null) span('maffs-plot-letter maffs-plot-letter-y', X(ay), BOX.t - 14, o.yLabel).setAttribute('data-axis', 'y');

      el._curves = svg('g', { 'class': 'maffs-plot-curves', 'clip-path': 'url(#' + id + '-box)' }, el);
      el._tips = svg('g', { 'class': 'maffs-plot-tips' }, el);
      settle();
    }

    // How many samples: at least one for every 2 px of the plot's width on screen, and never fewer than 480.
    function samples() {
      var w = root.getBoundingClientRect().width || 0;
      return Math.max(480, Math.ceil(w / 2));
    }
    // The path of one curve: a new sub-path after every value that is not finite, so the line is never joined across it.
    function trace(c) {
      var n = samples(), d = '', open = false, count = 0, end = null;
      for (var i = 0; i <= n; i++) {
        var x = win.x0 + (win.x1 - win.x0) * i / n, y;
        try { y = c.fn(x); } catch (e) { y = NaN; }
        var py = typeof y === 'number' && isFinite(y) ? Y(y) : NaN;
        if (!isFinite(py) || Math.abs(py) > 1e5) { open = false; continue; }
        d += (open ? 'L' : 'M') + num(X(x)) + ' ' + num(py);
        open = true;
        count++;
        if (y >= win.y0 && y <= win.y1) end = { x: x, y: y };
      }
      c.n = n;
      c.count = count;
      c.end = end;
      c.path.setAttribute('d', d);
      c.path.setAttribute('data-samples', n);
    }
    function addCurve(cid, fn, o) {
      o = o || {};
      remove(cid);
      var tone = o.tone === 2 ? 2 : 1;
      var clip = svg('clipPath', { id: id + '-c-' + (++uid) }, el._defs);
      var rect = svg('rect', { x: BOX.l - 8, y: BOX.t - 8, width: 0, height: BOX.h + 16 }, clip);
      var g = svg('g', { 'clip-path': 'url(#' + clip.id + ')' }, el._curves);
      var path = svg('path', { 'class': 'maffs-plot-curve', 'data-curve': cid, 'data-tone': tone, 'data-progress': 0,
        'data-x0': win.x0, 'data-x1': win.x1, 'data-y0': win.y0, 'data-y1': win.y1,
        'data-box': [BOX.l, BOX.t, BOX.w, BOX.h].join(' ') }, g);
      if (o.dash) path.setAttribute('data-dash', '');
      var c = { id: cid, fn: fn, tone: tone, label: o.label, path: path, g: g, clip: clip, rect: rect, p: 0, name: null, tip: null };
      trace(c);
      if (o.label != null) {
        c.name = span('maffs-plot-name', 0, 0, o.label);
        c.name.setAttribute('data-curve', cid);
        c.name.setAttribute('data-tone', tone);
      }
      curves.push(c);
      return c;
    }
    // How much of a curve shows: everything left of the x that is p of the way across the window.
    function progress(c, p) {
      c.p = p;
      c.path.setAttribute('data-progress', (Math.round(p * 1000) / 1000).toString());
      c.rect.setAttribute('width', num(p >= 1 ? BOX.w + 16 : 8 + BOX.w * p));
      if (c.name) c.name.classList.toggle('is-on', p >= 1);
      if (!c.tip) return;
      var x = win.x0 + (win.x1 - win.x0) * p, y;
      try { y = c.fn(x); } catch (e) { y = NaN; }
      var on = p < 1 && typeof y === 'number' && isFinite(y) && y >= win.y0 && y <= win.y1;
      c.tip.setAttribute('data-x', x);
      if (on) { c.tip.setAttribute('cx', num(X(x))); c.tip.setAttribute('cy', num(Y(y))); c.tip.removeAttribute('display'); }
      else c.tip.setAttribute('display', 'none');
    }
    function dropTip(c) { if (c.tip && c.tip.parentNode) c.tip.parentNode.removeChild(c.tip); c.tip = null; }

    /* The labels at the right-hand ends: each beside its curve's last point in the window, moved apart (and clear of the
       x-axis's letter) where two would overlap. Positions are worked out as fractions of the box, so a zoomed page is
       laid out the same. */
    function settle() {
      if (destroyed || !layer) return;
      var box = root.getBoundingClientRect();
      if (!box.height) return;
      var items = [], i, c, e;
      var fixed = layer.querySelector('.maffs-plot-letter-x');
      if (fixed) items.push({ el: fixed, y: parseFloat(fixed.style.top) / 100, h: fixed.getBoundingClientRect().height / box.height, fixed: true });
      for (i = 0; i < curves.length; i++) {
        c = curves[i];
        if (!c.name || !c.end) continue;
        e = c.end;
        c.name.style.left = pct(Math.min(X(e.x) + (e.x >= win.x1 - 1e-9 ? 16 : 8), VW - 40), VW);
        items.push({ el: c.name, y: Y(e.y) / VH, h: c.name.getBoundingClientRect().height / box.height, fixed: false });
      }
      items.sort(function (a, b) { return a.y - b.y; });
      var gap = 2 / Math.max(box.height, 1), pass, need, d;
      for (pass = 0; pass < 4; pass++) {
        for (i = 1; i < items.length; i++) {
          need = (items[i - 1].h + items[i].h) / 2 + gap;
          d = need - (items[i].y - items[i - 1].y);
          if (d > 0) { if (items[i].fixed) items[i - 1].y -= d; else items[i].y += d; }
        }
        for (i = items.length - 2; i >= 0; i--) {
          need = (items[i + 1].h + items[i].h) / 2 + gap;
          d = need - (items[i + 1].y - items[i].y);
          if (d > 0) { if (items[i].fixed) items[i + 1].y += d; else items[i].y -= d; }
        }
      }
      for (i = 0; i < items.length; i++) {
        if (items[i].fixed) continue;
        var half = items[i].h / 2;
        items[i].el.style.top = (Math.max(half, Math.min(1 - half, items[i].y)) * 100).toFixed(3) + '%';
      }
    }

    // ---- animation: one at a time, on animation frames, only while the plot shows
    function paused() { return held || !seen || document.hidden; }
    function stopAnim() {
      if (frame) { cancelAnimationFrame(frame); frame = 0; }
      anim = null;
    }
    function land() {                                    // the curves are all there: tips go, labels show
      if (!anim || anim.landed) return;
      anim.landed = true;
      for (var i = 0; i < anim.curves.length; i++) { dropTip(anim.curves[i]); progress(anim.curves[i], 1); }
      settle();
      if (typeof anim.onLand === 'function') anim.onLand();
    }
    function done() {
      var a = anim;
      stopAnim();
      if (a && typeof a.onDone === 'function') a.onDone();
    }
    function tick(ts) {
      frame = 0;
      if (!anim || destroyed) return;
      if (!paused()) {
        anim.t += last ? Math.min(ts - last, 100) : 0;   // a long gap (a tab that was away) counts as one frame
        last = ts;
        if (anim.t < anim.duration) {
          for (var i = 0; i < anim.curves.length; i++) progress(anim.curves[i], anim.t / anim.duration);
        } else {
          land();
          if (anim.t >= anim.duration + anim.hold) { done(); return; }
        }
      } else last = 0;
      frame = requestAnimationFrame(tick);
    }
    function start(list, o, tips) {
      finish();
      o = o || {};
      var still = reducedMotion();
      anim = { curves: list, t: 0, duration: still ? 0 : Math.max(0, o.duration), hold: Math.max(0, o.hold || 0), onLand: o.onLand, onDone: o.onDone, landed: false };
      for (var i = 0; i < list.length; i++) {
        if (tips && !still) {
          list[i].tip = svg('circle', { 'class': 'maffs-plot-tip', r: 5.5, 'data-curve': list[i].id, 'data-tone': list[i].tone }, el._tips);
        }
        progress(list[i], 0);
      }
      if (still) land();
      last = 0;
      if (still && !anim.hold) { done(); return; }
      frame = requestAnimationFrame(tick);
    }
    function finish() {
      if (!anim) return;
      land();
      done();
    }

    function add(cid, fn, o) {
      o = o || {};
      var c = addCurve(cid, fn, o);
      if (o.reveal) start([c], { duration: typeof o.duration === 'number' ? o.duration : REVEAL_MS, onDone: o.onDone }, false);
      else { progress(c, 1); settle(); }
      return api;
    }
    function pens(list, o) {
      o = o || {};
      finish();
      var made = [];
      for (var i = 0; i < list.length; i++) made.push(addCurve(list[i].id, list[i].fn, list[i]));
      start(made, { duration: typeof o.duration === 'number' ? o.duration : 4000, hold: o.hold, onLand: o.onLand, onDone: o.onDone }, true);
      return api;
    }
    function remove(cid) {
      for (var i = curves.length - 1; i >= 0; i--) {
        var c = curves[i];
        if (c.id !== cid) continue;
        if (anim && anim.curves.indexOf(c) !== -1) stopAnim();
        dropTip(c);
        if (c.g.parentNode) c.g.parentNode.removeChild(c.g);
        if (c.clip.parentNode) c.clip.parentNode.removeChild(c.clip);
        if (c.name && c.name.parentNode) c.name.parentNode.removeChild(c.name);
        curves.splice(i, 1);
      }
      return api;
    }
    function clear() {
      stopAnim();
      while (curves.length) remove(curves[0].id);
      return api;
    }
    function state() {
      return {
        window: { x: [win.x0, win.x1], y: [win.y0, win.y1], ticks: win.ticks },
        box: [BOX.l, BOX.t, BOX.w, BOX.h], viewBox: [VW, VH],
        curves: curves.map(function (c) { return { id: c.id, tone: c.tone, progress: c.p, samples: c.n, points: c.count, tip: !!c.tip }; }),
        animating: !!anim, landed: !!(anim && anim.landed), paused: paused(), still: reducedMotion()
      };
    }
    function destroy() {
      destroyed = true;
      stopAnim();
      if (io) io.disconnect();
      if (ro) ro.disconnect();
      document.removeEventListener('visibilitychange', onShow);
      if (root.parentNode) root.parentNode.removeChild(root);
    }
    function onShow() { last = 0; }

    var api = {
      el: root, add: add, pens: pens, remove: remove, clear: clear, finish: finish, state: state, destroy: destroy,
      reset: function (o) { build(o); return api; },
      describe: function (text) { root.setAttribute('aria-label', text); return api; },
      pause: function () { held = true; return api; },
      resume: function () { held = false; last = 0; return api; }
    };

    build(opts);
    document.addEventListener('visibilitychange', onShow);
    // On screen or not: an animation waits while the plot is out of sight (below the fold, or in a closed fold-out).
    if (typeof IntersectionObserver === 'function') {
      seen = false;
      io = new IntersectionObserver(function (es) { seen = es[es.length - 1].isIntersecting; last = 0; });
      io.observe(root);
    }
    // The box changed size (first shown, a resized window): the labels are placed again, and a curve is sampled again
    // if the box is now wide enough to need more points.
    if (typeof ResizeObserver === 'function') {
      ro = new ResizeObserver(function () {
        var n = samples();
        for (var i = 0; i < curves.length; i++) if (curves[i].n < n) trace(curves[i]);
        settle();
      });
      ro.observe(root);
    }
    if (document.fonts && document.fonts.ready && typeof document.fonts.ready.then === 'function') {
      document.fonts.ready.then(function () { settle(); });
    }
    return api;
  }

  window.MaffsPlot = { create: create, reducedMotion: reducedMotion, VIEW: [VW, VH], BOX: [BOX.l, BOX.t, BOX.w, BOX.h], REVEAL_MS: REVEAL_MS };
})();
