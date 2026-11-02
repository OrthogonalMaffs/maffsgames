#!/usr/bin/env python3
# ci-shards: Chart drawings (every chart the reading-charts, pie-chart and probability banks draw is read back FROM THE SCREEN, by hit-testing what is really painted, and compared with its data: pictogram symbols whole, half and quarter by their visible width; bar and segment lengths, line and scatter points through the numbers on the axes; pie slices by the angle each one really covers; spinner wedges and counters visible; the pictogram key and the symbol counts in the worked steps; fault-injection self-test) | | 3
# ci-deps: games/as-you-can-see/ games/who-ate-all-the-pies/ games/possibly-maybe/ schools/assets/reading-charts-game.js schools/assets/reading-charts-generator.js schools/assets/pie-game.js schools/assets/probability-game.js schools/assets/probability-generator.js scripts/bank_common.py
"""Drawing against data, for every chart the banks generate (contract PICTOGRAM-DRAWING, 28 Oct 2026).

Why this exists. As You Can See drew a half symbol in the DOM (a <g data-q="2"> with a clip rectangle of the right width) but the
clip-path sat on the transformed path, so the cut rectangle was moved off the symbol and the half symbol was never painted. The
answer was right, the data was right, the attributes were right, and the picture showed one symbol instead of one and a half. The
per-game verifiers read attributes and path geometry; none of them asked what is on the screen.

So this script asks the screen. For each mark it samples a grid of points inside the mark's own fill and calls
document.elementFromPoint() on each: a point is painted only when the mark (or its pattern overlay or label in the same group)
is what the browser reports there. From that it reads back

  Pictograms  every symbol's visible width as a fraction of a whole symbol (4 = whole, 2 = half, 1 = quarter), summed per row
              and compared with the row's data; symbols per row; the key symbol whole; the key text "= 6 lunches" (no "Key:").
  Bars        every bar and every stacked or dual segment: painted, and its length through the numbers on the axis equals its data.
  Lines       every plotted point painted and at its value; scatter points painted and at their x and y.
  Pies        the angle each slice really covers (a ring of 360 points round the pie), equal to the slice's data angle and the
              question's sector; every slice painted.
  Spinners    wedges painted, one per sector, each covering 360 / n degrees; counters painted.
  Wording     in the pictogram stage, every number of symbols in a question, a worked step or a slip agrees in number
              ("1 symbol", "2 symbols", "1 whole symbol").

Work is in units (one per chart type and one per planted fault) so CI can run it whole or in slices (# ci-shards). The planted faults
include the original bug (the clip back on the transformed path) and the bug's cousin (the part symbol not drawn at all).
"""
import argparse
import contextlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACS = {'slug': 'as-you-can-see', 'ns': 'ACS', 'files': ['reading-charts-generator.js', 'reading-charts-game.js']}
PIE = {'slug': 'who-ate-all-the-pies', 'ns': 'PIE', 'files': ['pie-game.js']}
PRB = {'slug': 'possibly-maybe', 'ns': 'PM', 'files': ['probability-generator.js', 'probability-game.js']}
SIZE = (390, 844)
SEEDS = (1, 2, 3, 4, 5)


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def sources(g):
    s = {'index.html': read('games/%s/index.html' % g['slug'])}
    for name in g['files']:
        s[name] = read('schools/assets/' + name)
    return s


# ---------------------------------------------------------------- the screen, read back
PAINT_JS = r"""
window.__paint = function (el, cols, rows) {
  // Grid points inside el's own fill; a point counts as painted when what the browser reports there is el, something inside it,
  // or something else in the same group (a pattern overlay, a label). Returns the painted extent as fractions of the box width.
  const b = el.getBoundingClientRect(), m = el.getScreenCTM(); if (!m || b.width <= 0) return { fill: 0, hit: 0 };
  const inv = m.inverse(), svg = el.ownerSVGElement;
  let fill = 0, hit = 0, minX = 9, maxX = -9;
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
    const x = b.left + b.width * (i + 0.5) / cols, y = b.top + b.height * (j + 0.5) / rows;
    const p = new DOMPoint(x, y).matrixTransform(inv);
    if (!el.isPointInFill(p)) continue;
    fill++;
    const e = document.elementFromPoint(x, y);
    if (e && e !== svg && (e === el || el.contains(e) || e.parentNode === el.parentNode || (e.parentNode && e.parentNode.parentNode === el.parentNode))) {
      hit++; const f = (x - b.left) / b.width; minX = Math.min(minX, f); maxX = Math.max(maxX, f + 1 / cols);
    }
  }
  return { fill: fill, hit: hit, minX: minX, maxX: maxX, w: b.width, h: b.height };
};
window.__figures = () => [...document.querySelectorAll('#figure svg, #exFigure svg')].filter(s => s.getClientRects().length);
window.__ring = function (svg) {
  // The angle each pie slice really covers: 360 points on a circle at 85% of the radius, clockwise from 12 o'clock.
  const first = svg.querySelector('g[data-pie] path, g[data-pie] circle'); if (!first) return { slices: {}, none: true };
  let cx, cy, r;
  if (first.tagName === 'circle') { cx = +first.getAttribute('cx'); cy = +first.getAttribute('cy'); r = +first.getAttribute('r'); }
  else { const mm = /^M\s*([-\d.]+)[ ,]+([-\d.]+)/.exec(first.getAttribute('d')), aa = /A\s*([-\d.]+)/.exec(first.getAttribute('d')); cx = +mm[1]; cy = +mm[2]; r = +aa[1]; }
  const m = svg.getScreenCTM(), got = {};
  for (let a = 0; a < 360; a++) {
    const t = (a + 0.5) * Math.PI / 180, pt = new DOMPoint(cx + 0.85 * r * Math.sin(t), cy - 0.85 * r * Math.cos(t)).matrixTransform(m);
    const e = document.elementFromPoint(pt.x, pt.y), g = e && e.closest ? e.closest('g[data-pie]') : null;
    if (g && svg.contains(g)) got[g.dataset.pie] = (got[g.dataset.pie] || 0) + 1;
  }
  const sw = parseFloat(getComputedStyle(first).strokeWidth) || 0, scale = Math.sqrt(m.a * m.a + m.b * m.b);
  return { slices: got, none: false, tol: (sw * scale / 0.85 / (r * scale)) * 57.3 + 1.5 };
};
"""

PICT_JS = r"""() => { const svg = window.__figures()[0]; if (!svg) return null; svg.scrollIntoView({ block: 'center' });
  const syms = [...svg.querySelectorAll('g[data-q]')].map(g => { const p = g.querySelector('path'), pr = window.__paint(p, 28, 14);
      return { row: g.dataset.row, q: Number(g.dataset.q), fill: pr.fill, hit: pr.hit, minX: pr.minX, maxX: pr.maxX }; });
  const texts = [...svg.querySelectorAll('text')].map(t => ({ s: t.textContent, key: t.dataset.keyText || null, cat: t.dataset.cat || null }));
  return { syms: syms, texts: texts }; }"""

BARS_JS = r"""() => { const svg = window.__figures()[0]; if (!svg) return null; svg.scrollIntoView({ block: 'center' });
  const gy = [...svg.querySelectorAll('line[data-ax="y"]')].map(l => { const b = l.getBoundingClientRect(); return { v: Number(l.dataset.gv), p: (b.top + b.bottom) / 2 }; });
  const gx = [...svg.querySelectorAll('line[data-ax="x"]')].map(l => { const b = l.getBoundingClientRect(); return { v: Number(l.dataset.gv), p: (b.left + b.right) / 2 }; });
  const bars = [...svg.querySelectorAll('rect.bar')].filter(r => r.dataset.v !== undefined).map(r => { const b = r.getBoundingClientRect(), pr = window.__paint(r, 6, 6);
      return { v: Number(r.dataset.v), h: b.height, fill: pr.fill, hit: pr.hit }; });
  const dots = [...svg.querySelectorAll('circle.dot')].map(c => { const b = c.getBoundingClientRect(), pr = window.__paint(c, 5, 5);
      return { v: Number(c.dataset.v), cy: (b.top + b.bottom) / 2, fill: pr.fill, hit: pr.hit }; });
  const pts = [...svg.querySelectorAll('circle.pt')].map(c => { const b = c.getBoundingClientRect(), pr = window.__paint(c, 5, 5);
      return { x: Number(c.dataset.x), y: Number(c.dataset.y), cx: (b.left + b.right) / 2, cy: (b.top + b.bottom) / 2, fill: pr.fill, hit: pr.hit }; });
  return { gy: gy, gx: gx, bars: bars, dots: dots, pts: pts }; }"""

PIE_JS = r"""() => { const out = window.__figures().map(svg => { svg.scrollIntoView({ block: 'center' });
    const r = window.__ring(svg);
    return { slices: r.slices, none: r.none, tol: r.tol, data: [...svg.querySelectorAll('g[data-pie]')].map(g => ({ pie: g.dataset.pie, angle: Number(g.dataset.angle) })) }; });
  return out; }"""

SPIN_JS = r"""() => { const svg = window.__figures()[0]; if (!svg) return null; svg.scrollIntoView({ block: 'center' });
  const w = [...svg.querySelectorAll('.wedge')].map(x => { const pr = window.__paint(x, 14, 14); return { colour: x.dataset.colour, fill: pr.fill, hit: pr.hit }; });
  const d = [...svg.querySelectorAll('.disc')].map(x => { const pr = window.__paint(x, 5, 5); return { colour: x.dataset.colour, fill: pr.fill, hit: pr.hit }; });
  let ring = null;
  const first = svg.querySelector('path.wedge');
  if (first) { const mm = /^M\s*([-\d.]+)[ ,]+([-\d.]+)/.exec(first.getAttribute('d')), aa = /A\s*([-\d.]+)/.exec(first.getAttribute('d')), m = svg.getScreenCTM(), cx = +mm[1], cy = +mm[2], r = +aa[1], got = {};
    for (let a = 0; a < 360; a++) { const t = (a + 0.5) * Math.PI / 180, pt = new DOMPoint(cx + 0.9 * r * Math.sin(t), cy - 0.9 * r * Math.cos(t)).matrixTransform(m);
      const e = document.elementFromPoint(pt.x, pt.y), el = e && e.closest ? e.closest('.wedge') : null;
      if (el && svg.contains(el)) { const k = [...svg.querySelectorAll('.wedge')].indexOf(el); got[k] = (got[k] || 0) + 1; } }
    ring = got; }
  return { n: Number(svg.getAttribute('data-n')), wedges: w, discs: d, ring: ring }; }"""

WALK_JS = r"""(q) => { const out = []; (function walk(v) { if (typeof v === 'string') out.push(v); else if (Array.isArray(v)) v.forEach(walk); else if (v && typeof v === 'object') Object.values(v).forEach(walk); })(q); return out; }"""


# ---------------------------------------------------------------- the page under Playwright
def open_page(pw, base, g, srcs, size=SIZE):
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=True, is_mobile=True)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % g['slug'])
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=srcs['index.html']))
    def serve(name):                      # a route handler takes exactly one argument (a default argument would be passed the request)
        ctx.route(lambda url: url.split('?')[0].endswith('/' + name), lambda route: route.fulfill(
            status=200, content_type='application/javascript; charset=utf-8', body=srcs[name]))
    for name in g['files']:
        serve(name)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % g['slug'], wait_until='load', timeout=20000)
    page.wait_for_function('!!window.%s && !!%s.ui' % (g['ns'], g['ns']), timeout=10000)
    page.evaluate("""() => { window.mfg = () => {}; window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = () => Promise.resolve(); }""")
    page.evaluate('() => {' + PAINT_JS + '}')
    return br, page, errors


def with_page(base, g, srcs, fn, out):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br, page, errors = open_page(pw, base, g, srcs)
        try:
            fn(page)
        finally:
            br.close()
        for e in errors[:3]:
            out.append('%s: page error %s' % (g['slug'], e))


# ---------------------------------------------------------------- the units
def plural_faults(strings, where, out):
    """Counts of symbols agree in number: 1 symbol, 2 symbols, 1 whole symbol, 4.5 symbols."""
    for s in strings:
        for m in re.finditer(r'(?<![\d.])(\d+(?:\.\d+)?) (whole )?(symbols?)\b', s):
            n, word = float(m.group(1)), m.group(3)
            if (n == 1 and word != 'symbol') or (n != 1 and word != 'symbols'):
                out.append('%s: "%s" does not agree in number' % (where, m.group(0)))


def unit_pictograms(base, out):
    def run(page):
        n = 0
        for slot in range(1, 12):
            for seed in SEEDS:
                where = 'pictogram slot %d seed %d' % (slot, seed)
                page.evaluate('ACS.ui.preview(1, %d, %d)' % (slot, seed))
                page.wait_for_timeout(40)
                q = page.evaluate('ACS.ui.question()')
                plural_faults(page.evaluate(WALK_JS, q), where, out)
                ch = q['chart']
                if ch['type'] != 'pictogram':
                    out.append('%s: stage 1 slot is not a pictogram' % where)
                    continue
                got = page.evaluate(PICT_JS)
                if not got:
                    out.append('%s: no chart on the screen' % where)
                    continue
                n += 1
                quarters, count = {}, {}
                for s in got['syms']:
                    if s['row'] == 'key':
                        if s['hit'] < 0.8 * s['fill'] or s['fill'] < 10:
                            out.append('%s: the key symbol is not painted whole' % where)
                        continue
                    if s['fill'] < 10:
                        out.append('%s: a %d-quarter symbol of %s has no area' % (where, s['q'], s['row']))
                        continue
                    if s['hit'] == 0:
                        out.append('%s: a %d-quarter symbol of %s is in the picture but not painted (the half or quarter symbol vanishes)' % (where, s['q'], s['row']))
                        continue
                    seen = round(s['maxX'] * 4)
                    if seen != s['q'] or s['minX'] > 0.16:
                        out.append('%s: a symbol of %s is drawn %d quarters wide (from %.2f), its data says %d' % (where, s['row'], seen, s['minX'], s['q']))
                    quarters[s['row']] = quarters.get(s['row'], 0) + seen
                    count[s['row']] = count.get(s['row'], 0) + 1
                for row in ch['rows']:
                    if quarters.get(row['label'], 0) != row['q']:
                        out.append('%s: %s is drawn as %d quarters of a symbol, the data is %d' % (where, row['label'], quarters.get(row['label'], 0), row['q']))
                    if count.get(row['label'], 0) != -(-row['q'] // 4):
                        out.append('%s: %s has %d symbols drawn, the data needs %d' % (where, row['label'], count.get(row['label'], 0), -(-row['q'] // 4)))
                keyt = [t for t in got['texts'] if t['key']]
                want = '= ' + ('?' if ch['keyHidden'] else '%s %s' % (ch['per'], ch['what']))
                if not keyt or keyt[0]['s'] != want:
                    out.append('%s: the key reads %r, it should read %r' % (where, keyt[0]['s'] if keyt else None, want))
                if any(t['s'].startswith('Key:') for t in got['texts']):
                    out.append('%s: a stray "Key:" is on the chart' % where)
        if n < 50:
            out.append('pictograms: only %d charts were checked' % n)
    with_page(base, ACS, sources(ACS), run, out)
    return 'pictograms: stage 1, all 11 slots over %d seeds read back from the screen' % len(SEEDS)


def scale(grid):
    """Pixels per unit and the pixel of zero, from the numbered gridlines on an axis."""
    if len(grid) < 2:
        return None
    a, b = grid[0], grid[-1]
    if a['v'] == b['v']:
        return None
    k = (b['p'] - a['p']) / (b['v'] - a['v'])
    return k, a['p'] - k * a['v']


def unit_bars(base, out):
    def run(page):
        n = 0
        for stage in (2, 3, 4):
            for slot in range(1, 12):
                for seed in SEEDS[:3]:
                    where = 'stage %d slot %d seed %d' % (stage, slot, seed)
                    page.evaluate('ACS.ui.preview(%d, %d, %d)' % (stage, slot, seed))
                    page.wait_for_timeout(30)
                    got = page.evaluate(BARS_JS)
                    if not got:
                        continue
                    n += 1
                    sy, sx = scale(got['gy']), scale(got['gx'])
                    for b in got['bars']:
                        if b['fill'] < 4 or b['hit'] < 0.6 * b['fill']:
                            out.append('%s: a bar of %s is not painted' % (where, b['v']))
                        elif sy and abs(abs(b['h'] / sy[0]) - b['v']) > max(0.011 * abs(b['v']), 0.011):
                            out.append('%s: a bar is %.2f long on the axis, its data is %s' % (where, abs(b['h'] / sy[0]), b['v']))
                    for d in got['dots']:
                        if d['fill'] < 4 or d['hit'] < 0.6 * d['fill']:
                            out.append('%s: a plotted point (%s) is not painted' % (where, d['v']))
                        elif sy and abs((d['cy'] - sy[1]) / sy[0] - d['v']) > max(0.011 * abs(d['v']), 0.011):
                            out.append('%s: a plotted point is at %.2f on the axis, its data is %s' % (where, (d['cy'] - sy[1]) / sy[0], d['v']))
                    for p in got['pts']:
                        if p['fill'] < 4 or p['hit'] < 0.6 * p['fill']:
                            out.append('%s: a scatter point (%s, %s) is not painted' % (where, p['x'], p['y']))
                        elif sx and sy and (abs((p['cx'] - sx[1]) / sx[0] - p['x']) > max(0.011 * abs(p['x']), 0.011) or abs((p['cy'] - sy[1]) / sy[0] - p['y']) > max(0.011 * abs(p['y']), 0.011)):
                            out.append('%s: a scatter point is at (%.2f, %.2f), its data is (%s, %s)' % (where, (p['cx'] - sx[1]) / sx[0], (p['cy'] - sy[1]) / sy[0], p['x'], p['y']))
        if n < 60:
            out.append('bars: only %d charts were checked' % n)
    with_page(base, ACS, sources(ACS), run, out)
    return 'bars, lines and scatter: stages 2-4, every slot over 3 seeds, every mark painted and at its value'


def pie_questions(page, stage, out, where_prefix):
    page.evaluate('PIE.ui.start(%d)' % stage)
    for qn in range(10):
        page.wait_for_function("PIE.ui.state() === 'asking'", timeout=8000)
        page.wait_for_timeout(100)
        q = page.evaluate('PIE.ui.question()')
        if stage == 3:                       # stage 3 draws the pie from the angles the student types: right ones, then read it
            page.evaluate('PIE.ui.answer(true)')
            page.wait_for_timeout(150)
            yield qn, q
        else:
            yield qn, q
            page.evaluate('PIE.ui.answer(true)')
        page.wait_for_selector('#nextBtn, #nextStageBtn', state='visible', timeout=8000)
        if qn < 9:
            page.evaluate("document.getElementById('nextBtn').click()")


def unit_pies(base, out):
    def run(page):
        n = 0
        for stage in range(1, 6):
            for qn, q in pie_questions(page, stage, out, 'pie'):
                where = 'pies stage %d q%d' % (stage, qn)
                figs = page.evaluate(PIE_JS)
                charts = q['charts']
                if len(figs) != len(charts):
                    out.append('%s: %d charts on the screen, the question has %d' % (where, len(figs), len(charts)))
                    continue
                for fig, ch in zip(figs, charts):
                    n += 1
                    if fig['none']:
                        out.append('%s: a pie is on the screen with no slice' % where)
                        continue
                    secs = [s for s in ch['sectors'] if s['angle'] and s['angle'] > 0]
                    if len(fig['data']) != len(secs):
                        out.append('%s: %d slices drawn, the data has %d' % (where, len(fig['data']), len(secs)))
                    for s in secs:
                        seen = fig['slices'].get(s['pie'], 0)
                        if abs(seen - s['angle']) > fig['tol']:
                            out.append('%s: the %s slice covers %d degrees on the screen, its data is %s' % (where, s['pie'], seen, s['angle']))
        if n < 40:
            out.append('pies: only %d pies were checked' % n)
    with_page(base, PIE, sources(PIE), run, out)
    return 'pies: five stages, ten questions each, every slice measured by the angle it covers on the screen'


def unit_spinners(base, out):
    def run(page):
        n = 0
        for stage in range(1, 6):
            for slot in range(1, 12):
                for seed in (1, 2):
                    where = 'probability stage %d slot %d seed %d' % (stage, slot, seed)
                    page.evaluate('PM.ui.preview(%d, %d, %d)' % (stage, slot, seed))
                    page.wait_for_timeout(30)
                    q = page.evaluate('PM.ui.question()')
                    got = page.evaluate(SPIN_JS)
                    ch = q.get('chart')
                    if not got or not ch:
                        continue
                    n += 1
                    if ch['type'] == 'spinner':
                        if len(got['wedges']) != len(ch['sectors']):
                            out.append('%s: %d wedges drawn, the data has %d sectors' % (where, len(got['wedges']), len(ch['sectors'])))
                        for w in got['wedges']:
                            if w['fill'] < 4 or w['hit'] < 0.5 * w['fill']:
                                out.append('%s: a %s wedge is not painted' % (where, w['colour']))
                        if got['ring'] is not None:
                            want = 360 / float(len(ch['sectors']))
                            for k in range(len(ch['sectors'])):
                                seen = got['ring'].get(str(k), got['ring'].get(k, 0))
                                if abs(seen - want) > 3:
                                    out.append('%s: wedge %d covers %d degrees on the screen, it should cover %.0f' % (where, k, seen, want))
                    for d in got['discs']:
                        if d['fill'] < 4 or d['hit'] < 0.5 * d['fill']:
                            out.append('%s: a %s counter is not painted' % (where, d['colour']))
        if n < 15:
            out.append('spinners: only %d pictures were checked' % n)
    with_page(base, PRB, sources(PRB), run, out)
    return 'spinners and bags: stages 1-5, every slot over 2 seeds, wedges by the angle they cover, counters painted'


UNITS = [('pictograms', unit_pictograms), ('bars', unit_bars), ('pies', unit_pies), ('spinners', unit_spinners)]


# ---------------------------------------------------------------- planted faults
CLIP = ("    if (quarters < 4) { var w = el('g', { 'clip-path': 'url(#' + cp + ')', 'data-cut': 1 }); w.appendChild(p); g.appendChild(w); } else g.appendChild(p);\n")
PLANTS = [
    ('the original bug: the clip back on the transformed path (a half symbol vanishes)', ACS, 'index.html',
     [(CLIP, "    if (quarters < 4) p.setAttribute('clip-path', 'url(#' + cp + ')');\n    g.appendChild(p);\n")], 'pictograms', r'(not painted|drawn 0 quarters|quarters of a symbol)'),
    ('the part symbol not drawn at all', ACS, 'index.html',
     [("if (part) symbol(svg, id, ch.shape, x, cy, r, part, row.label);", "if (false) symbol(svg, id, ch.shape, x, cy, r, part, row.label);")], 'pictograms', r'quarters of a symbol|symbols drawn'),
    ('a half symbol drawn as a whole one (no cut)', ACS, 'index.html',
     [("var g = el('g', { 'data-q': quarters, 'data-row': tag });\n    var cp", "var g = el('g', { 'data-q': quarters, 'data-row': tag }); quarters = 4;\n    var cp")], 'pictograms', r'(quarters wide|quarters of a symbol)'),
    ('the stray "Key:" back in the key text', ACS, 'index.html',
     [("'= ' + (ch.keyHidden", "'Key: = ' + (ch.keyHidden")], 'pictograms', r'(Key:|key reads)'),
    ('"1 symbols": counts that do not agree in number', ACS, 'reading-charts-generator.js',
     [("(n === 1 ? 'symbol' : 'symbols')", "'symbols'")], 'pictograms', r'does not agree in number'),
    ('a bar drawn at 80% of its height', ACS, 'index.html',
     [("cg.firstChild.setAttribute('data-v', c.value);", "cg.firstChild.setAttribute('data-v', c.value); cg.firstChild.setAttribute('height', String(c.value / ch.max * plot.h * 0.8));")], 'bars', r'long on the axis'),
    ('a bar hidden', ACS, 'index.html',
     [("cg.firstChild.setAttribute('data-v', c.value);", "cg.firstChild.setAttribute('data-v', c.value); cg.firstChild.setAttribute('style', 'display:none');")], 'bars', r'(is not painted|long on the axis)'),
    ('a pie slice drawn 10% too narrow', PIE, 'index.html',
     [("var a0 = acc, a1 = Math.min(360, acc + ang);", "var a0 = acc, a1 = Math.min(360, acc + ang * 0.9);")], 'pies', r'degrees on the screen'),
    ('every pie slice hidden', PIE, 'index.html',
     [("g = el('g', { 'data-pie': s.pie,", "g = el('g', { style: 'display:none', 'data-pie': s.pie,")], 'pies', r'(degrees on the screen|no slice)'),
    ('a spinner wedge hidden', PRB, 'index.html',
     [("el('path', { class: 'wedge k-' + s.name,", "el('path', { style: 'display:none', class: 'wedge k-' + s.name,")], 'spinners', r'(is not painted|degrees on the screen)'),
]


def run_plant(base, plant):
    what, g, fname, edits, unit, want = plant
    srcs = sources(g)
    for old, new in edits:
        if srcs[fname].count(old) != 1:
            print('  self-test %-78s *** CANNOT PLANT (%d matches) ***' % (what, srcs[fname].count(old)))
            return False
        srcs[fname] = srcs[fname].replace(old, new)
    got = []
    fn = dict(UNITS)[unit]
    # the same unit, on the planted sources
    orig = globals()['sources']
    globals()['sources'] = lambda gg, _s=srcs, _g=g, _o=orig: _s if gg is _g else _o(gg)
    try:
        fn(base, got)
    finally:
        globals()['sources'] = orig
    hit = [x for x in got if re.search(want, x)]
    print('  self-test %-78s %s' % (what, ('caught: ' + hit[0][:80]) if hit else '*** MISSED ***' + (' (other: %s)' % got[0][:80] if got else '')))
    return bool(hit)


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    shard = bc.Shard(__file__, args)
    units = [u[0] for u in UNITS] + ['plant: ' + p[0] for p in PLANTS]
    if args.list_units:
        print('\n'.join(units))
        return 0
    mine = shard.pick(units)
    out = []
    proc, base = bc.start_stub_server()
    ok = True
    try:
        for name, fn in UNITS:
            if name in mine:
                with shard.unit(name):
                    print(fn(base, out))
        for p in PLANTS:
            if 'plant: ' + p[0] in mine:
                with shard.unit('plant: ' + p[0]):
                    ok = run_plant(base, p) and ok
    finally:
        proc.terminate()
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('FAIL  ... and %d more' % (len(out) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
