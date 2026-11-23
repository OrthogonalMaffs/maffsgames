"""The one copy of the contrast measurement (contract SITE-CONTRAST, 22 Nov 2026; canon 7.5).

Every check that measures text contrast imports this module: scripts/check-contrast.py (every game, site-wide),
scripts/check-answer-count.py (the answer-count lines) and scripts/check-teacher-invite.py (the teacher line). Before
it, the same page-side code was copied into the last two, and nothing measured a game's own text at all.

Python side
  ratio(fg, bg)            the WCAG 2 contrast ratio of two sRGB colours (hex strings or (r, g, b) tuples)
  is_large(size, weight)   WCAG's large text: at least 24 px, or at least 18.66 px (14 pt) and bold (700 or more)
  required(size, weight)   3.0 for large text, else 4.5 (AA)
  lightness_fix(...)       the nearest colour of the same hue and saturation (HSL, lightness only) that reaches a
                           target ratio against every background given, or None when no lightness does

Page side
  CONTRAST_JS              an expression that defines (once) and returns window.__mc:
    __mc.measure(el, opts) one element's text colour against what is behind it (opts {opacity: false}: colours
                           alone, for a caller measuring a line on a screen that may not be showing, whose
                           opacity is then an animation's or a hidden screen's, not the reader's):
                             - the background: the element's own and its ancestors' background colours, composited
                               through translucent layers down to the first opaque one, on white (the canvas) if none
                               is opaque; SVG text instead takes the painted SVG shapes beneath it at its own centre
                               (their fill, fill-opacity and opacity) before its HTML ancestors;
                             - the text colour: its computed color (fill for SVG text) at its alpha times its
                               effective opacity (its own and every ancestor's opacity multiplied), composited over
                               that background;
                             - unmeasurable (with the reason) when the background chain meets a background-image
                               (a gradient is one), the text is painted with background-clip:text, an SVG fill is a
                               paint server, or a canvas, video or img lies behind the text above the first opaque
                               background. The ratio is still computed (on the colours alone) for callers that only
                               ever measured colours, but an unmeasurable result is never a pass.
    __mc.scan()            every visible element that directly holds text on the page as it stands (not hidden,
                           clipped, transparent, or painted over at its centre by an opaque box): a list of
                           records, each "measured", "exempt" (disabled, aria-hidden but for KaTeX's drawn maths,
                           effective opacity <= 0.5)
                           or "unmeasurable", with its text, colours, ratio, size, weight and the ratio it needs.
"""
import colorsys

LARGE_PX = 24.0          # 18 pt
LARGE_BOLD_PX = 18.66    # 14 pt, with a weight of 700 or more
AA_NORMAL = 4.5
AA_LARGE = 3.0
FADED = 0.5              # effective opacity at or below this is faded by design (exempt, counted)


def parse(c):
    """'#abc', '#aabbcc' or (r, g, b) -> (r, g, b) as ints 0-255."""
    if isinstance(c, (tuple, list)):
        return tuple(int(round(v)) for v in c[:3])
    s = c.strip().lstrip("#")
    if len(s) in (3, 4):
        s = "".join(ch * 2 for ch in s[:3])
    if len(s) not in (6, 8):
        raise ValueError("not a hex colour: %r" % c)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def luminance(c):
    """WCAG 2 relative luminance (the sRGB transfer threshold as WCAG 2 states it, 0.03928)."""
    def f(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = parse(c)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)


def composite(fg, alpha, bg):
    """fg at alpha over an opaque bg -> (r, g, b) floats."""
    f, b = parse(fg), parse(bg)
    return tuple(f[i] * alpha + b[i] * (1 - alpha) for i in range(3))


def is_large(size_px, weight):
    return size_px >= LARGE_PX or (size_px >= LARGE_BOLD_PX and int(weight) >= 700)


def required(size_px, weight):
    return AA_LARGE if is_large(size_px, weight) else AA_NORMAL


def lightness_fix(colour, backgrounds, target=4.6, step=0.0005):
    """The colour of the same hue and saturation (HSL), lightness only, nearest to `colour` that reaches `target`
    against every background in `backgrounds`; `colour` itself when it already does; None when no lightness does.
    Both directions are searched and the smaller move wins (a grey on a dark page lightens, on a light page darkens)."""
    bgs = [parse(b) for b in backgrounds]
    r, g, b = (v / 255.0 for v in parse(colour))
    h, l, s = colorsys.rgb_to_hls(r, g, b)

    def at(lv):
        return to_hex(tuple(v * 255 for v in colorsys.hls_to_rgb(h, lv, s)))

    def ok(hx):
        return all(ratio(hx, bg) >= target for bg in bgs)

    if ok(to_hex(parse(colour))):
        return to_hex(parse(colour))
    best = None
    for direction in (1, -1):
        lv = l
        while 0.0 <= lv <= 1.0:
            hx = at(lv)
            if ok(hx):
                if best is None or abs(lv - l) < best[0]:
                    best = (abs(lv - l), hx)
                break
            lv += direction * step
    return best and best[1]


CONTRAST_JS = r"""(() => {
  if (window.__mc) return window.__mc;
  const LARGE = %(large)s, LARGE_BOLD = %(large_bold)s, NORMAL = %(normal)s, BIG = %(big)s, FADED = %(faded)s;
  const rgb = s => {
    const m = String(s || '').match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const v = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    return v.length < 3 ? null : {r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1};
  };
  const lum = x => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(x.r) + 0.7152 * f(x.g) + 0.0722 * f(x.b); };
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };
  const over = (L, a, bg) => ({r: L.r * a + bg.r * (1 - a), g: L.g * a + bg.g * (1 - a), b: L.b * a + bg.b * (1 - a)});
  const hex = c => '#' + [c.r, c.g, c.b].map(v => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
  const desc = e => {
    if (!e || !e.tagName) return '?';
    let s = e.tagName.toLowerCase();
    if (e.id) s += '#' + e.id;
    const cl = typeof e.className === 'string' ? e.className : (e.className && e.className.baseVal) || '';
    if (cl.trim()) s += '.' + cl.trim().split(/\s+/).slice(0, 2).join('.');
    return s;
  };
  const opacityOf = el => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity); return o; };
  const SHAPES = {rect: 1, circle: 1, ellipse: 1, path: 1, polygon: 1, polyline: 1};
  const BEHIND = {CANVAS: 1, VIDEO: 1, IMG: 1};
  // The point to look behind: the centre of the element's first text, else of its box.
  const centre = el => {
    let r = null;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) {
      const rg = document.createRange(); rg.selectNodeContents(n); const q = rg.getBoundingClientRect();
      if (q.width > 0 && q.height > 0) { r = q; break; }
    }
    r = r || el.getBoundingClientRect();
    return {x: r.left + r.width / 2, y: r.top + r.height / 2};
  };
  // The paint stack at el's centre, top first, split at el: null when the point is off screen or el is not hit there.
  const stackAt = el => {
    const c = centre(el);
    if (c.x < 0 || c.y < 0 || c.x >= innerWidth || c.y >= innerHeight) return null;
    const stack = document.elementsFromPoint(c.x, c.y), i = stack.indexOf(el);
    return i < 0 ? null : {above: stack.slice(0, i), below: stack.slice(i + 1)};
  };
  const opaqueBox = e => { const b = rgb(getComputedStyle(e).backgroundColor); return !!(b && b.a >= 0.99) || !!BEHIND[e.tagName]; };
  // Not on screen: an opaque box that is neither its ancestor nor its descendant is painted over its text (a card's
  // turned-away face under the face showing, a panel under a modal).
  const covered = el => {
    const s = stackAt(el);
    return !!s && s.above.some(e => !el.contains(e) && !(e instanceof SVGElement) && opaqueBox(e));
  };
  function measure(el, opts) {
    const withOpacity = !(opts && opts.opacity === false);
    const cs = getComputedStyle(el), svg = el instanceof SVGElement;
    let unmeasurable = null, opaque = false, stop = null;
    const layers = [];          // top first: {c, a}
    const take = (e, ecs) => {
      if (ecs.backgroundImage && ecs.backgroundImage !== 'none' && !unmeasurable) unmeasurable = 'background-image on ' + desc(e);
      const b = rgb(ecs.backgroundColor);
      if (b && b.a > 0) { layers.push({c: b, a: b.a}); if (b.a >= 0.99) { opaque = true; stop = e; } }
    };
    const s = stackAt(el);
    // SVG text: the SVG shapes painted beneath it, down to the first HTML box.
    if (svg && s) {
      for (const e of s.below) {
        if (!(e instanceof SVGElement) || opaque) break;
        if (!SHAPES[e.tagName.toLowerCase()]) continue;
        const ecs = getComputedStyle(e), f = ecs.fill;
        if (/url\(/.test(f)) { unmeasurable = unmeasurable || 'SVG paint server behind the text (' + desc(e) + ')'; continue; }
        const fc = rgb(f);
        if (fc && fc.a > 0) {
          const a = fc.a * parseFloat(ecs.fillOpacity) * opacityOf(e);
          if (a > 0) { layers.push({c: fc, a: a}); if (a >= 0.99) { opaque = true; stop = e; } }
        }
      }
    }
    // The ancestry method: its own background, then its ancestors', to the first opaque one.
    for (let e = el; e && !opaque; e = e.parentElement) {
      if (e instanceof SVGElement && e.tagName.toLowerCase() !== 'svg') continue;
      take(e, getComputedStyle(e));
    }
    // A picture painted beneath the text, above that background: unmeasurable.
    if (s) {
      for (const e of s.below) {
        if (e === stop) break;
        if (BEHIND[e.tagName]) { unmeasurable = unmeasurable || e.tagName.toLowerCase() + ' behind the text'; break; }
        if (!e.contains(el) && !(e instanceof SVGElement) && opaqueBox(e)) break;
      }
    }
    let bg = {r: 255, g: 255, b: 255};
    for (let i = layers.length - 1; i >= 0; i--) bg = over(layers[i].c, layers[i].a, bg);
    let c;
    if (svg) {
      if (/url\(/.test(cs.fill)) unmeasurable = unmeasurable || 'SVG text filled with a paint server';
      c = rgb(cs.fill) || rgb(cs.color);
      if (c) c.a *= parseFloat(cs.fillOpacity);
    } else {
      if (/text/.test(cs.webkitBackgroundClip || '') || /text/.test(cs.backgroundClip || '')) unmeasurable = unmeasurable || 'text painted with background-clip:text';
      c = rgb(cs.color);
    }
    if (!c) return {unmeasurable: 'colour not in rgb(): ' + (svg ? cs.fill : cs.color), ratio: null};
    const opacity = withOpacity ? opacityOf(el) : 1;
    const fg = over(c, c.a * opacity, bg);
    const size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10) || 400;
    const large = size >= LARGE || (size >= LARGE_BOLD && weight >= 700);
    return {ratio: ratio(fg, bg), fg: hex(fg), bg: hex(bg), colour: hex(c), alpha: c.a, opacity: opacity,
            size: size, weight: weight, large: large, need: large ? BIG : NORMAL, unmeasurable: unmeasurable};
  }
  const clipped = el => {
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.clip && cs.clip !== 'auto' && cs.position === 'absolute') return true;
      if (cs.clipPath && /inset\(\s*50%%|circle\(\s*0/.test(cs.clipPath)) return true;
      if (e !== el && /hidden|clip/.test(cs.overflow)) { const r = e.getBoundingClientRect(); if (r.width < 2 || r.height < 2) return true; }
    }
    return false;
  };
  function holdsText(el) {
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return n.textContent.replace(/\s+/g, ' ').trim();
    return '';
  }
  function scan() {
    const out = [], sx = scrollX, sy = scrollY, H = innerHeight;
    const els = [];
    for (const el of document.querySelectorAll('body *')) {
      const tag = el.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT' || tag === 'TEMPLATE' || tag === 'OPTION' || tag === 'TITLE') continue;
      const text = holdsText(el);
      if (!text) continue;
      if (!el.checkVisibility({visibilityProperty: true, contentVisibilityAuto: true})) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2 || clipped(el)) continue;
      const cs = getComputedStyle(el), c = rgb(el instanceof SVGElement ? cs.fill : cs.color);
      if (c && c.a === 0 && !/text/.test(cs.webkitBackgroundClip || '')) continue;    // transparent text: not shown
      els.push({el: el, text: text, top: r.top + sy});
    }
    // Look behind each element with it on screen (elementsFromPoint sees only the viewport), a screenful at a time.
    els.sort((a, b) => a.top - b.top);
    let at = null;
    for (const it of els) {
      const el = it.el;
      if (at === null || it.top < at || it.top > at + H * 0.8) { at = Math.max(0, it.top - H * 0.1); window.scrollTo({left: 0, top: at, behavior: 'instant'}); at = scrollY; }
      if (covered(el)) continue;                          // painted over by an opaque box: not on screen
      const rec = {el: desc(el), parent: desc(el.parentElement), text: it.text.slice(0, 60)};
      // aria-hidden is exempt, except KaTeX's visible maths: KaTeX marks its drawn output .katex-html aria-hidden and
      // gives screen readers the MathML copy instead, so that text is on screen and is measured.
      const hid = el.closest('[aria-hidden="true"]');
      if (hid && !hid.classList.contains('katex-html')) rec.exempt = 'aria-hidden';
      else if (el.closest('button:disabled, input:disabled, select:disabled, textarea:disabled, fieldset:disabled, [aria-disabled="true"]')) rec.exempt = 'disabled';
      const m = measure(el);
      Object.assign(rec, m);
      if (!rec.exempt && m.opacity !== undefined && m.opacity <= FADED) rec.exempt = 'faded (opacity ' + m.opacity.toFixed(2) + ')';
      rec.kind = rec.exempt ? 'exempt' : m.unmeasurable ? 'unmeasurable' : (m.ratio + 1e-9 >= m.need ? 'pass' : 'fail');
      out.push(rec);
    }
    window.scrollTo({left: sx, top: sy, behavior: 'instant'});
    return out;
  }
  window.__mc = {rgb: rgb, lum: lum, ratio: ratio, measure: measure, scan: scan};
  return window.__mc;
})()""" % {"large": LARGE_PX, "large_bold": LARGE_BOLD_PX, "normal": AA_NORMAL, "big": AA_LARGE, "faded": FADED}
