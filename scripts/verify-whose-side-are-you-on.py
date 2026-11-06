#!/usr/bin/env python3
# ci-line: Whose Side Are You On? (every item of the four stages recomputed from the triangle's own geometry, never the game's labels: which side is HYP, OPP and ADJ, every fraction, every function against real trig; the feedback table and its wording; 50 or more distinct items a stage; seeded rounds: HYP first, every quadrant; every stage played with real taps at 320, 390 and 1280 px: tap bands 44 px deep, each side clicked along its length and in the gaps of its dashes or dots, double clicks answering once and filling one slot, a right answer held 0.8 s lit with its mark, the clock stopped, Stage 2's slots filled, cleared and refilled before Check, one answer a question, a slow right answer still right, no sideways scroll, Aa mode included, Next above the fold; fault-injection self-test: a wrong label, a wrong function and more, each caught) |
"""Independent verification for Whose Side Are You On? (games/whose-side-are-you-on/), contract WHOSE-SIDE, 5 Nov 2026.
SR-30: checked from its first PR.

WHAT IS INDEPENDENT
-------------------------------------------------------------------------------
The page's generator hands over each item's vertices and its sides as ends in a shuffled order. This script takes only those
coordinates, and the corners the page marks, and works everything out with vector arithmetic of its own:

  Right angle  the corner the page marks is the one where the two sides meet at 90 degrees (dot product).
  Sides        HYP is the side not touching the right angle, and the longest; OPP is the side not touching theta; ADJ is the third.
               The game's own `roles` are compared with these, never used.
  Lengths      Stages 2-4: a true Pythagorean triple, drawn to scale (printed lengths proportional to drawn lengths).
  Fractions    each printed fraction, from the side lengths this script chose.
  Functions    from the measured angle theta: sin, cos and tan against the ratio, to 1e-9. A function is right only if it is the one
               real trig gives for those two sides, so a swapped table cannot pass.
  Feedback     which line a wrong tap gets is recomputed from the geometry, and the wording compared with the approved spec.
In the page, a played round reads the drawn SVG back and compares it with the data; each tap goes through the real mouse.

    python scripts/verify-whose-side-are-you-on.py [--no-selftest]
"""
import argparse
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = os.path.dirname(HERE)
SLUG = 'whose-side-are-you-on'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
MIN_ITEMS = 50
STOP_AT_FIRST = False
SIZES = [(320, 568), (390, 844), (1280, 800)]
SPEC_LINES = {
    'upright': 'Opposite means across from θ, not upright. Turn the triangle in your head.',
    'longest': 'Two sides touch θ. The longest one, across from the right angle, is always HYP.',
    'square': 'Label from θ, not from the square corner.',
    'both': 'Use both: the side you know AND the side you want.',
}
COLOURS = {'HYP': '#D55E00', 'OPP': '#0072B2', 'ADJ': '#009E73'}
DASH = {'HYP': False, 'OPP': True, 'ADJ': True}
FN_SIDES = {'sin': ('OPP', 'HYP'), 'cos': ('ADJ', 'HYP'), 'tan': ('OPP', 'ADJ')}
REAL = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def geometry(it):
    """{'HYP': side, 'OPP': side, 'ADJ': side}, the angle theta in radians, and the problems found, from coordinates alone."""
    v, bad = it['verts'], []
    r, t = it['right'], it['theta']
    if r == t:
        bad.append('theta marked on the right angle')
    a = [i for i in range(3) if i != r]
    u1 = (v[a[0]][0] - v[r][0], v[a[0]][1] - v[r][1])
    u2 = (v[a[1]][0] - v[r][0], v[a[1]][1] - v[r][1])
    cosr = (u1[0] * u2[0] + u1[1] * u2[1]) / (math.hypot(*u1) * math.hypot(*u2))
    if abs(cosr) > 1e-9:
        bad.append('the marked square corner is not 90 degrees')
    found = {}
    for s in it['sides']:
        ends = {s['from'], s['to']}
        if r not in ends:
            found['HYP'] = s
        elif t not in ends:
            found['OPP'] = s
        else:
            found['ADJ'] = s
    if set(found) != {'HYP', 'OPP', 'ADJ'}:
        bad.append('the three sides are not one of each: %s' % sorted(found))
        return found, 0, bad
    length = {k: dist(v[s['from']], v[s['to']]) for k, s in found.items()}
    if not (length['HYP'] > length['OPP'] and length['HYP'] > length['ADJ']):
        bad.append('the side across from the right angle is not the longest')
    others = [i for i in range(3) if i != t]
    w1 = (v[others[0]][0] - v[t][0], v[others[0]][1] - v[t][1])
    w2 = (v[others[1]][0] - v[t][0], v[others[1]][1] - v[t][1])
    theta = math.acos((w1[0] * w2[0] + w1[1] * w2[1]) / (math.hypot(*w1) * math.hypot(*w2)))
    return found, theta, bad


def real_function(theta, geo_len, top, bottom):
    """The function whose true value is top/bottom at theta, or None."""
    hits = [f for f in REAL if abs(REAL[f](theta) - geo_len[top] / geo_len[bottom]) < 1e-9]
    return hits


def upright_side(it):
    best, best_a = None, 31
    for s in it['sides']:
        p, q = it['verts'][s['from']], it['verts'][s['to']]
        a = math.degrees(math.atan2(abs(q[0] - p[0]), abs(q[1] - p[1])))
        if a < best_a:
            best_a, best = a, s['id']
    return best


def expected_why(it, role_of_tap, tapped):
    """The approved line for a wrong tap on Stage 1, from the spec's three cases."""
    if it['ask'] == 'HYP':
        return 'longest'
    if it['ask'] == 'OPP':
        return 'upright' if tapped == upright_side(it) else 'square'
    return 'longest' if role_of_tap == 'HYP' else 'square'


def check_item(it, fails):
    def fail(msg):
        fails.append('%s: %s' % (it['id'], msg))
    geo, theta, bad = geometry(it)
    for b in bad:
        fail(b)
    if bad:
        return
    ids = {k: s['id'] for k, s in geo.items()}
    if ids != it['roles']:
        fail('labels %s disagree with the geometry %s' % (it['roles'], ids))
    lens = {k: s['len'] for k, s in geo.items()}
    if lens['HYP'] ** 2 != lens['OPP'] ** 2 + lens['ADJ'] ** 2:
        fail('lengths %s are not a Pythagorean triple' % lens)
    v = it['verts']
    drawn = {k: dist(v[s['from']], v[s['to']]) for k, s in geo.items()}
    if abs(drawn['OPP'] / drawn['HYP'] - lens['OPP'] / lens['HYP']) > 1e-9 or abs(drawn['ADJ'] / drawn['HYP'] - lens['ADJ'] / lens['HYP']) > 1e-9:
        fail('not drawn to scale')
    stage = it['stage']
    if stage == 1:
        if it['key'] != ids[it['ask']]:
            fail('key %s, but the %s is side %s' % (it['key'], it['ask'], ids[it['ask']]))
    elif stage == 2:
        if it['keyTop'] != ids[it['top']] or it['keyBottom'] != ids[it['bottom']]:
            fail('fraction keys disagree with the geometry')
        if it['frac'] != [lens[it['top']], lens[it['bottom']]]:
            fail('fraction %s, not %s over %s' % (it['frac'], lens[it['top']], lens[it['bottom']]))
    elif stage == 3:
        if it['dir'] == 'name':
            if it['frac'] != [lens[it['top']], lens[it['bottom']]]:
                fail('printed fraction %s is wrong' % it['frac'])
            if it['key'] not in real_function(theta, drawn, it['top'], it['bottom']):
                fail('%s over %s is not %s of theta' % (it['top'], it['bottom'], it['key']))
        else:
            top, bottom = it['key'].split('/')
            if it['fn'] not in real_function(theta, drawn, top, bottom):
                fail('%s of theta is not %s' % (it['fn'], it['key']))
    else:
        if it['known'] != ids[it['knownRole']] or it['wanted'] != ids[it['wantedRole']]:
            fail('known or wanted side disagrees with the geometry')
        pair = {it['knownRole'], it['wantedRole']}
        hits = [f for f, s in FN_SIDES.items() if set(s) == pair and abs(REAL[f](theta) - drawn[s[0]] / drawn[s[1]]) < 1e-9]
        if hits != [it['key']]:
            fail('known %s and wanted %s need %s, the key says %s' % (it['knownRole'], it['wantedRole'], hits, it['key']))


def check_engine(page, fails, sample=None):
    """Every item, or with `sample` (a self-test plant, which needs no more to be caught) that many a stage."""
    lines = page.evaluate('() => WS.LINE')
    if lines != SPEC_LINES:
        fails.append('feedback wording differs from the approved spec: %s' % lines)
    orientations = set()
    for stage in (1, 2, 3, 4):
        # A sample is drawn in the page: sending a whole bank across for each plant is most of a self-test's time.
        items = page.evaluate('([n, k]) => { const b = WS.gen.bank(n); return k ? b.filter((_, i) => i % Math.floor(b.length / k) === 0) : b; }', [stage, sample])
        ids = {i['id'] for i in items}
        if len(ids) != len(items):
            fails.append('stage %d: repeated items' % stage)
        if max(len(i) for i in ids) > 40:           # analytics.js cuts question_id at 40, and two items must never share one
            fails.append('stage %d: a question id over 40 characters' % stage)
        if len(ids) < MIN_ITEMS:
            fails.append('stage %d: only %d distinct items' % (stage, len(ids)))
        corners = set()
        for it in items:
            check_item(it, fails)
            orientations.add(it['orient'])
            # measured, not read from the game's own turn index: where the right angle sits on screen around the triangle's middle
            v, r = it['verts'], it['right']
            corners.add((v[r][0] > sum(p[0] for p in v) / 3, v[r][1] > sum(p[1] for p in v) / 3))
        if len(corners) != 4:
            fails.append('stage %d: the right angle sits in only %d of the four quadrants' % (stage, len(corners)))
        if not sample:
            print('  stage %d: %d items recomputed from the geometry' % (stage, len(items)))
    turns = {o.split('.')[0] for o in orientations}
    if turns != {'0', '1', '2', '3'} or len({o.split('.')[2] for o in orientations}) != 2 or len({o.split('.')[3] for o in orientations}) != 2:
        fails.append('orientations missing: %s' % sorted(orientations)[:5])
    if sample:
        return
    # Feedback: 400 Stage 1 items, both wrong sides of each.
    items = page.evaluate('() => WS.gen.bank(1)')
    random.Random(7).shuffle(items)
    for it in items[:400]:
        geo, _, _ = geometry(it)
        role_by_id = {s['id']: k for k, s in geo.items()}
        for s in it['sides']:
            if s['id'] == it['key']:
                continue
            got = page.evaluate('([q, t]) => WS.gen.whyTap(q, t)', [it, s['id']])
            want = expected_why(it, role_by_id[s['id']], s['id'])
            if got != want:
                fails.append('%s: tap on %s gets %s, should be %s' % (it['id'], s['id'], got, want))
    # Sessions: 300 seeded rounds.
    rnd = random.Random(11)
    for stage in (1, 2, 3, 4):
        for _ in range(300 // 4):
            seed = rnd.randrange(2 ** 32)
            deck = page.evaluate('([n, s]) => WS.gen.session(n, s, 10)', [stage, seed])
            if len(deck) != 10 or len({d['id'] for d in deck}) != 10:
                fails.append('stage %d seed %d: a round is not 10 distinct items' % (stage, seed))
                continue
            for it in deck:
                check_item(it, fails)
            if {d['orient'].split('.')[0] for d in deck} != {'0', '1', '2', '3'}:
                fails.append('stage %d seed %d: a round misses a quadrant' % (stage, seed))
            if stage == 1 and [d['ask'] for d in deck[:3]] != ['HYP'] * 3:
                fails.append('stage 1 seed %d: HYP does not come first' % seed)
            if stage == 1 and {d['ask'] for d in deck[3:]} != {'OPP', 'ADJ'}:
                fails.append('stage 1 seed %d: OPP and ADJ not both asked' % seed)
            if stage == 3 and ([d['dir'] for d in deck] != ['name'] * 5 + ['pick'] * 5):
                fails.append('stage 3 seed %d: names first, then the reverse' % seed)
    # Speed feeds the score and never makes it zero.
    fast, slow = page.evaluate('() => [WS.gen.scoreFor(1), WS.gen.scoreFor(600)]')
    if not (fast > slow >= 1):
        fails.append('score: fast %s, slow %s' % (fast, slow))


def drawn_sides(page):
    return page.evaluate("""() => {
      const out = {};
      document.querySelectorAll('#figure line.side').forEach(l => { const c = getComputedStyle(l);
        out[l.dataset.side] = {x1:+l.getAttribute('x1'),y1:+l.getAttribute('y1'),x2:+l.getAttribute('x2'),y2:+l.getAttribute('y2'),
          lit:l.classList.contains('lit'), stroke:c.stroke, dash:c.strokeDasharray}; });
      return out; }""")


def check_labels(page, label, fails):
    """No label touches a side, the theta or the edge of the figure, measured on the page."""
    problems = page.evaluate("""() => {
      const out = [], svg = document.querySelector('#figure svg'), W = +svg.getAttribute('width'), H = +svg.getAttribute('height');
      const svgBox = svg.getBoundingClientRect(), lines = Array.from(svg.querySelectorAll('line.side'));
      const th = document.querySelector('#figure [data-theta]').getBoundingClientRect();
      svg.querySelectorAll('text[data-label]').forEach(t => {
        const b = t.getBoundingClientRect(), x0 = b.left - svgBox.left, y0 = b.top - svgBox.top, x1 = x0 + b.width, y1 = y0 + b.height;
        if (x0 < 0 || y0 < 0 || x1 > W || y1 > H) out.push(t.textContent + ' leaves the figure');
        lines.forEach(l => { const a = [+l.getAttribute('x1'), +l.getAttribute('y1')], c = [+l.getAttribute('x2'), +l.getAttribute('y2')];
          for (let i = 0; i <= 200; i++) { const x = a[0] + (c[0] - a[0]) * i / 200, y = a[1] + (c[1] - a[1]) * i / 200;
            if (x > x0 - 1 && x < x1 + 1 && y > y0 - 1 && y < y1 + 1) { out.push(t.textContent + ' touches side ' + l.dataset.side); break; } } });
        if (b.left < th.right && b.right > th.left && b.top < th.bottom && b.bottom > th.top) out.push(t.textContent + ' touches theta');
      });
      const tx = th.left + th.width / 2 - svgBox.left, ty = th.top + th.height / 2 - svgBox.top;
      lines.forEach(l => { const x1 = +l.getAttribute('x1'), y1 = +l.getAttribute('y1'), x2 = +l.getAttribute('x2'), y2 = +l.getAttribute('y2');
        const dx = x2 - x1, dy = y2 - y1, u = Math.max(0, Math.min(1, ((tx - x1) * dx + (ty - y1) * dy) / (dx * dx + dy * dy)));
        if (Math.hypot(tx - (x1 + u * dx), ty - (y1 + u * dy)) < 8) out.push('theta sits on side ' + l.dataset.side); });
      return out; }""")
    for p in problems:
        fails.append('%s: %s' % (label, p))


def check_colour_use(page, label, fails):
    """Amendment 2: the three side colours on the sides and the HYP/OPP/ADJ words only; no green or red anywhere; right and wrong
    are a symbol and a word. Every visible element's colours are read from the page, the footer's included."""
    problems = page.evaluate("""() => {
      const root = getComputedStyle(document.documentElement), hex = n => { const d = document.createElement('i');
        d.style.color = root.getPropertyValue(n).trim(); document.body.appendChild(d); const c = getComputedStyle(d).color; d.remove(); return c; };
      const sides = ['--hyp', '--opp', '--adj'].map(hex), bad = sides.concat(['--correct', '--wrong'].map(hex)), out = [];
      const allowed = e => e.closest('.w, .katex') || e.matches('line.side, line.HYP, line.OPP, line.ADJ') || e.closest('#figure text');
      document.querySelectorAll('body *').forEach(e => {
        if (e.closest('script, style') || !e.getClientRects().length) return;
        const c = getComputedStyle(e), hasText = Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
        const used = [c.backgroundColor, c.fill !== 'none' ? c.fill : ''];
        if (hasText) used.push(c.color);
        if (parseFloat(c.borderLeftWidth)) used.push(c.borderLeftColor);
        if (parseFloat(c.borderTopWidth)) used.push(c.borderTopColor);
        if (c.stroke !== 'none' && e.closest('svg')) used.push(c.stroke);
        if (used.some(u => bad.includes(u)) && !allowed(e)) out.push((e.id || e.className.baseVal || e.className || e.tagName) + ' uses ' + used.filter(u => bad.includes(u))[0]);
      });
      return out.slice(0, 3); }""")
    for p in problems:
        fails.append('%s: %s' % (label, p))


def on_side_points(ax, ay, bx, by, role, count):
    """Points on a side, on screen, from one end: the middles of the gaps in the line its role is drawn with (the page's dash pattern)
    and otherwise evenly along it, none within 6 px of an end."""
    length = math.hypot(bx - ax, by - ay)
    if role == 'OPP':
        ds = [16 + 20 * k for k in range(100) if 6 < 16 + 20 * k < length - 6]     # 12 on, 8 off: the middle of each gap
    elif role == 'ADJ':
        ds = [6 + 11 * k for k in range(100) if 6 < 6 + 11 * k < length - 6]       # 1 on, 10 off
    else:
        ds = [length * (k + 1) / (count + 1) for k in range(count)]
    if len(ds) > count:
        ds = [ds[round(i * (len(ds) - 1) / (count - 1))] for i in range(count)]
    return [(ax + (bx - ax) * d / length, ay + (by - ay) * d / length) for d in ds]


def bands_on_screen(page):
    return page.evaluate("""() => Array.from(document.querySelectorAll('#figure .hit')).map(b => {
      const s = b.getScreenCTM(), c = getComputedStyle(b); return {val:b.dataset.val, width:+b.getAttribute('stroke-width') * s.a, pe:c.pointerEvents, dash:c.strokeDasharray,
        x1:+b.getAttribute('x1')+s.e,y1:+b.getAttribute('y1')+s.f,x2:+b.getAttribute('x2')+s.e,y2:+b.getAttribute('y2')+s.f}; })""")


def slot_vals(page):
    return page.evaluate("() => { const t = document.getElementById('slotTop'), b = document.getElementById('slotBottom'), c = document.getElementById('checkBtn'); return t ? [t.dataset.val || null, b.dataset.val || null, c.disabled] : [null, null, null]; }")


def check_hit_lines(page, label, fails):
    bands = bands_on_screen(page)
    if len(bands) != 3:
        fails.append('%s: %d tap bands, not one a side' % (label, len(bands)))
    for b in bands:
        if b['width'] < 44 or b['pe'] != 'stroke' or b['dash'] != 'none':
            fails.append('%s: tap band %.1f px, pointer-events %s, dashes %s' % (label, b['width'], b['pe'], b['dash']))
    painted = page.evaluate("() => Array.from(document.querySelectorAll('#figure line.side, #figure .square, #figure .arc, #figure text, #figure .theta')).filter(e => getComputedStyle(e).pointerEvents !== 'none').length")
    if painted:
        fails.append('%s: %d painted parts of the figure take pointer events' % (label, painted))
    return {b['val']: b for b in bands}


def check_stage2_clicks(page, it, geo, label, fails):
    """Every side clicked for real along its length, in the gaps of its own line style, each click filling the top slot with that side."""
    bands = check_hit_lines(page, label, fails)
    if int(label.rsplit('q', 1)[1]) > 3:            # the first three questions of a round; the turns are dealt evenly, so these vary
        return
    for role, s in geo.items():
        b = bands.get(s['id'])
        if not b:
            continue
        for x, y in on_side_points(b['x1'], b['y1'], b['x2'], b['y2'], role, 5):
            page.mouse.click(x, y)
            got = slot_vals(page)[0]
            if got != s['id']:
                fails.append('%s: a click on %s at (%.0f, %.0f) gave %s' % (label, role, x, y, got))
                if got:
                    page.click('#slotTop')
                continue
            page.click('#slotTop')
            if slot_vals(page)[0] is not None:
                fails.append('%s: tapping the full top slot did not empty it' % label)
                return


def double_click_slots(page, box, role_by_id, label, fails):
    """A double click on one side fills one slot only, and a further tap on it does nothing."""
    for side, b in box.items():
        pts = on_side_points(b['x1'], b['y1'], b['x2'], b['y2'], role_by_id[side], 5)
        x, y = pts[len(pts) // 2]
        page.mouse.dblclick(x, y)
        if slot_vals(page) != [side, None, True]:
            fails.append('%s: a double click on %s gave slots %s' % (label, role_by_id[side], slot_vals(page)))
            return
        page.mouse.click(x, y)
        if slot_vals(page) != [side, None, True]:
            fails.append('%s: a further tap moved %s: %s' % (label, role_by_id[side], slot_vals(page)))
            return
        page.click('#slotTop')
        if slot_vals(page)[0] is not None:
            fails.append('%s: the slot did not empty after a double click' % label)
            return


def rgb(hexa):
    return 'rgb(%d, %d, %d)' % tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))


def wait_asking(page):
    page.wait_for_function("() => WS.ui.state() === 'asking' && !MaffsLock.isFresh()", timeout=8000)


def play_round(page, stage, wrong_at, label, fails):
    """One whole round with real mouse taps, wrong at the question indices in wrong_at."""
    page.evaluate("""(n) => { window.__answers = 0;
      if (!window.__mfgWrapped) { const real = window.mfg; window.__mfgWrapped = true;
        window.mfg = function (name, params) { if (name === 'question_answered') window.__answers++; if (real) return real.apply(this, arguments); }; }
      document.querySelector('#stageList [data-stage="' + n + '"]').click(); }""", stage)
    w, h = page.viewport_size['width'], page.viewport_size['height']
    streak, score = 0, 0
    for n in range(10):
        if STOP_AT_FIRST and fails:                 # a self-test plant, caught: the rest of its round proves nothing more
            return
        wait_asking(page)
        it = page.evaluate('() => WS.ui.question()')
        check_item(it, fails)
        geo, _, bad = geometry(it)
        if bad:
            return
        ids = {k: s['id'] for k, s in geo.items()}
        sw = page.evaluate('() => document.documentElement.scrollWidth')
        if sw > w:
            fails.append('%s stage %d: sideways scroll %d' % (label, stage, sw))
        # the drawing is the data: same triangle, right angle square and theta present, tap bands 44 px deep
        d = drawn_sides(page)
        if set(d) != {s['id'] for s in it['sides']}:
            fails.append('%s: drawn sides differ from the data' % label)
        for k, s in geo.items():
            line = d[s['id']]
            scale = float(page.evaluate("() => document.querySelector('#figure svg').dataset.scale"))
            p, q = it['verts'][s['from']], it['verts'][s['to']]
            if abs(math.hypot(line['x2'] - line['x1'], line['y2'] - line['y1']) - dist(p, q) * scale) > 1:
                fails.append('%s: side %s drawn %s, data %s' % (label, k, line, dist(p, q) * scale))
        if not page.evaluate("() => !!document.querySelector('#figure [data-square]') && !!document.querySelector('#figure [data-theta] .katex') && !!document.querySelector('#figure [data-arc]')"):
            fails.append('%s: the square, the arc or the KaTeX theta is missing' % label)
        check_labels(page, '%s stage %d asking' % (label, stage), fails)
        check_colour_use(page, '%s stage %d asking' % (label, stage), fails)
        wrong = n in wrong_at
        if stage in (1, 2):
            box = check_hit_lines(page, '%s stage %d' % (label, stage), fails)
            role_by_id = {v: k for k, v in ids.items()}

            def tap(side):
                # the middle-most point of the side's own gaps (a solid side: its middle), as a real click
                b = box[side]
                pts = on_side_points(b['x1'], b['y1'], b['x2'], b['y2'], role_by_id[side], 5)
                page.mouse.click(*pts[len(pts) // 2])
            if stage == 1:
                other = [s['id'] for s in it['sides'] if s['id'] != it['key']][0]
                pick = other if wrong else ids[it['ask']]
                if n in (0, 2):                     # a double click, right (question 1) and wrong (question 3): one answer each
                    b = box[pick]
                    pts = on_side_points(b['x1'], b['y1'], b['x2'], b['y2'], role_by_id[pick], 5)
                    page.mouse.dblclick(*pts[len(pts) // 2])
                else:
                    tap(pick)
            else:
                top, bottom = ids[it['top']], ids[it['bottom']]
                third = ids[({'HYP', 'OPP', 'ADJ'} - {it['top'], it['bottom']}).pop()]
                prompt = ' '.join(page.evaluate("() => document.getElementById('ask').textContent").split())
                want_prompt = '%s over %s: tap the top side, then the bottom. Tap a box to empty it, then press Check.' % (it['top'], it['bottom'])
                if prompt != want_prompt:
                    fails.append('%s: Stage 2 prompt %r' % (label, prompt))
                if page.evaluate("() => document.querySelectorAll('#ask .w').length") != 2:
                    fails.append('%s: the two side words in the prompt are not coloured' % label)
                if slot_vals(page) != [None, None, True]:
                    fails.append('%s: Stage 2 does not start with two empty slots and Check off' % label)
                check_stage2_clicks(page, it, geo, '%s q%d' % (label, n + 1), fails)
                if n < 2:
                    double_click_slots(page, check_hit_lines(page, label, fails), role_by_id, '%s q%d' % (label, n + 1), fails)
                if n % 2 == 0 and not wrong:
                    # fills a slot wrongly, clears it, refills it correctly: marked right, and nothing is marked before Check
                    tap(third)
                    if slot_vals(page) != [third, None, True]:
                        fails.append('%s: one slot full should leave Check off: %s' % (label, slot_vals(page)))
                    tap(bottom)
                    if slot_vals(page) != [third, bottom, False]:
                        fails.append('%s: both slots full should turn Check on: %s' % (label, slot_vals(page)))
                    if page.evaluate('() => WS.ui.state()') != 'asking':
                        fails.append('%s: marked before Check' % label)
                        return
                    page.click('#slotTop')
                    if slot_vals(page) != [None, bottom, True]:
                        fails.append('%s: clearing a slot should empty it and turn Check off: %s' % (label, slot_vals(page)))
                    tap(top)
                else:
                    tap(top)
                    tap(third if wrong else bottom)
                if slot_vals(page) != [top, third if wrong else bottom, False]:
                    fails.append('%s: slots %s before Check' % (label, slot_vals(page)))
                r = page.query_selector('#checkBtn').bounding_box()
                if r['y'] + r['height'] > h - 40 or r['height'] < 44:
                    fails.append('%s: Check is below the fold or small: %s' % (label, r))
                if n == 1:                          # a double click on Check marks once
                    page.mouse.dblclick(r['x'] + r['width'] / 2, r['y'] + r['height'] / 2)
                else:
                    page.click('#checkBtn')
        else:
            want = it['key']
            opts = page.query_selector_all('#opts .opt')
            vals = [o.get_attribute('data-val') for o in opts]
            if len(set(vals)) != 3 or want not in vals:
                fails.append('%s: options %s lack the key %s' % (label, vals, want))
            for o in opts:
                r = o.bounding_box()
                if r['height'] < 44:
                    fails.append('%s: option %.0f px tall' % (label, r['height']))
                if r['y'] + r['height'] > h - 40:
                    fails.append('%s stage %d: last option below the fold, %.0f in %d' % (label, stage, r['y'] + r['height'], h))
            target = [o for o in opts if (o.get_attribute('data-val') == want) != wrong][0]
            if n in (0, 2):                         # a double click on an option answers once
                r = target.bounding_box()
                page.mouse.dblclick(r['x'] + r['width'] / 2, r['y'] + r['height'] / 2)
            else:
                target.click()
        try:
            page.wait_for_function("() => WS.ui.state() === 'right' || WS.ui.state() === 'wrong'", timeout=4000)
        except Exception:
            fails.append('%s stage %d q%d: the tap marked nothing' % (label, stage, n + 1))
            return
        got = page.evaluate('() => WS.ui.state()')
        page.wait_for_timeout(60)                   # room for a second click's effect to land, if it is going to
        answers = page.evaluate('() => window.__answers')
        if answers != n + 1:
            fails.append('%s stage %d q%d: %d answers logged so far, should be %d' % (label, stage, n + 1, answers, n + 1))
        if got != ('wrong' if wrong else 'right'):
            fails.append('%s stage %d q%d: state %s, expected %s' % (label, stage, n + 1, got, 'wrong' if wrong else 'right'))
        streak = 0 if wrong else streak + 1
        if page.evaluate('() => WS.ui.streak()') != streak:
            fails.append('%s: streak %s, expected %s' % (label, page.evaluate('() => WS.ui.streak()'), streak))
        new_score = page.evaluate('() => WS.ui.score()')
        if (new_score > score) == wrong:
            fails.append('%s: score %s to %s on a %s answer' % (label, score, new_score, 'wrong' if wrong else 'right'))
        score = new_score
        check_labels(page, '%s stage %d marked' % (label, stage), fails)
        check_colour_use(page, '%s stage %d marked' % (label, stage), fails)
        mark = page.evaluate("() => { const h = document.querySelector('.fb-head'); return h ? [h.dataset.mark, h.textContent] : null; }")
        if mark != (['wrong', '✗Not quite'] if wrong else ['right', '✓Right']):
            fails.append('%s stage %d: the mark reads %s' % (label, stage, mark))
        d = drawn_sides(page)
        if wrong:
            lit = {'stage': stage}
            if stage == 1:
                only = d[ids[it['ask']]]
                if not only['lit'] or only['stroke'] != rgb(COLOURS[it['ask']]) or (only['dash'] != 'none') != DASH[it['ask']]:
                    fails.append('%s: the correct side is not lit in its colour and line: %s' % (label, only))
                letter = page.evaluate('(id) => { const t = document.querySelector(\'#figure [data-label="\' + id + \'"]\'); return t ? t.textContent : null; }', ids[it['ask']])
                if letter != it['ask'][0]:
                    fails.append('%s: lit side letter %s' % (label, letter))
                line = page.evaluate("() => document.querySelector('.fb-line').dataset.plain")
                role_by_id = {v: k for k, v in ids.items()}
                other = [s['id'] for s in it['sides'] if s['id'] != it['key']][0]
                if line != SPEC_LINES[expected_why(it, role_by_id[other], other)]:
                    fails.append('%s: feedback %r' % (label, line))
            if stage == 4:
                line = page.evaluate("() => document.querySelector('.fb-line').dataset.plain")
                if line != SPEC_LINES['both']:
                    fails.append('%s: stage 4 feedback %r' % (label, line))
            btn = page.query_selector('.maffs-next-wrap button') or page.query_selector('.fb-next button')
            if not btn:
                fails.append('%s: no Next on a wrong answer' % label)
                return
            r = btn.bounding_box()
            if r['y'] + r['height'] > h - 40:
                fails.append('%s stage %d: Next below the fold, %.0f in %d' % (label, stage, r['y'] + r['height'], h))
            btn.click()
        else:
            page.wait_for_function("() => WS.ui.state() !== 'right'", timeout=4000)
    page.wait_for_function("() => document.querySelector('#results').classList.contains('active')", timeout=4000)
    if page.evaluate('() => document.documentElement.scrollWidth') > w:
        fails.append('%s stage %d: sideways scroll on results' % (label, stage))
    subs = page.evaluate('() => { const n = window.__sub.length; window.__sub = []; return n; }')
    if subs != 1:
        fails.append('%s stage %d: %d board submissions a round' % (label, stage, subs))
    page.wait_for_function('() => !MaffsLock.isFresh()', timeout=4000)
    page.click('#menuBtn')
    page.wait_for_function("() => document.querySelector('#menu').classList.contains('active') && !MaffsLock.isFresh()", timeout=4000)


def check_slow(page, fails):
    """Speed never marks wrong: a right answer after a long wait is right, and scores at least 1."""
    page.evaluate("""() => { const real = performance.now.bind(performance); let extra = 0; window.__skip = (s) => { extra += s * 1000; };
      performance.now = () => real() + extra; WS.ui.start(1); }""")
    wait_asking(page)
    page.evaluate('() => window.__skip(3600)')
    page.evaluate('() => WS.ui.answer(true)')
    page.wait_for_function("() => WS.ui.state() === 'right'", timeout=3000)
    if page.evaluate('() => WS.ui.score()') < 1 or page.evaluate('() => WS.ui.streak()') != 1:
        fails.append('a slow right answer was not marked right')


def check_aa(browser, base, fails):
    """Aa mode: no sideways scroll on any stage at the phone sizes, asking and on a wrong answer."""
    for w, h in ((320, 568), (375, 667), (390, 844)):
        ctx = browser.new_context(viewport={'width': w, 'height': h})
        ctx.add_init_script("localStorage.setItem('mfg_accessible', 'true');")
        ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
        page = ctx.new_page()
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex && document.body.classList.contains("accessible")')
        for stage in (1, 2, 3, 4):
            page.evaluate('(n) => WS.ui.start(n)', stage)
            wait_asking(page)
            for when in ('asking', 'wrong'):
                if when == 'wrong':
                    page.evaluate('() => WS.ui.answer(false)')
                    page.wait_for_function("() => WS.ui.state() === 'wrong'", timeout=4000)
                sw = page.evaluate('() => document.documentElement.scrollWidth')
                if sw > w:
                    fails.append('Aa %dx%d stage %d %s: sideways scroll %d' % (w, h, stage, when, sw))
        ctx.close()


def check_hold(browser, base, fails, route=None, stages=(1, 2, 3, 4)):
    """A right answer on each stage: lit, "Right", no Next, for the real 0.8 s; taps ignored; then the next question by itself. An hour
    jumped during the hold must not reach the clock or the score. Real timers here: run_page's fast pause would hide all of this."""
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page = ctx.new_page()
    if route:
        page.route('**/games/%s/**' % SLUG, route)
    page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
    page.wait_for_function('() => !!window.WS && !!window.katex')
    page.evaluate("""() => { const real = performance.now.bind(performance); let extra = 0; window.__skip = (s) => { extra += s * 1000; };
      performance.now = () => real() + extra; }""")
    for stage in stages:
        page.evaluate('(n) => WS.ui.start(n)', stage)
        wait_asking(page)
        first = page.evaluate('() => WS.ui.question()')
        page.evaluate('() => WS.ui.answer(true)')
        page.wait_for_function("() => WS.ui.state() === 'right'", timeout=3000)
        score = page.evaluate('() => WS.ui.score()')
        look = page.evaluate("""() => { const h = document.querySelector('.fb-head');
          return {mark: h ? h.textContent : null, lit: document.querySelectorAll('#figure line.side.lit').length,
                  next: document.querySelectorAll('.maffs-next-wrap button, .fb-next button').length, bands: document.querySelectorAll('#figure .hit').length, time: document.getElementById('hudTime').textContent}; }""")
        if look['mark'] != '✓Right' or look['lit'] < 1 or look['next'] or look['bands']:
            fails.append('stage %d hold: %s' % (stage, look))
        page.evaluate('() => window.__skip(3600)')          # an hour passes on the clock's own time source, during the hold
        page.wait_for_timeout(600)
        # taps and clicks during the hold: nothing moves
        page.mouse.click(195, 300)
        held = page.evaluate('() => [WS.ui.state(), WS.ui.question().id, document.getElementById("hudTime").textContent, WS.ui.score()]')
        if held != ['right', first['id'], look['time'], score]:
            fails.append('stage %d: during the hold %s, expected right, %s, %s, %s' % (stage, held, first['id'], look['time'], score))
        try:
            page.wait_for_function("(id) => WS.ui.state() === 'asking' && WS.ui.question().id !== id", arg=first['id'], timeout=1500)
        except Exception:
            fails.append('stage %d: no next question after the hold' % stage)
            continue
        page.wait_for_timeout(600)
        shown = page.evaluate('() => document.getElementById("hudTime").textContent')
        if int(shown.split(':')[0]) >= 30:
            fails.append('stage %d: the clock ran during the hold: %s' % (stage, shown))
        wait_asking(page)
        page.evaluate('() => WS.ui.answer(true)')
        page.wait_for_function("() => WS.ui.state() === 'right'", timeout=3000)
        if page.evaluate('() => WS.ui.score()') - score < 40:   # 5 seconds or less on the question scores far above this; an hour would not
            fails.append('stage %d: the hold reached the score: %s after %s' % (stage, page.evaluate('() => WS.ui.score()'), score))
        page.wait_for_function("() => WS.ui.state() !== 'right'", timeout=3000)
    ctx.close()


def check_colours(page, fails):
    tokens = page.evaluate("""() => { const c = getComputedStyle(document.documentElement);
      return {HYP:c.getPropertyValue('--hyp').trim(), OPP:c.getPropertyValue('--opp').trim(), ADJ:c.getPropertyValue('--adj').trim()}; }""")
    if tokens != COLOURS:
        fails.append('side colours changed: %s' % tokens)
    words = page.evaluate("""() => Array.from(document.querySelectorAll('#menu .w')).map(w => [w.textContent, getComputedStyle(w).color, parseFloat(getComputedStyle(w).fontSize), getComputedStyle(w).fontWeight])""")
    for word, colour, px, weight in words:
        if colour != rgb(COLOURS[word]):
            fails.append('word %s is %s' % (word, colour))
        if px < 19 or int(weight) < 700:
            fails.append('word %s is %.1f px at weight %s: not large bold text' % (word, px, weight))


def run_page(browser, base, fails, route=None, sizes=SIZES, engine=True, stages=(1, 2, 3, 4)):
    ctx = browser.new_context(viewport={'width': sizes[0][0], 'height': sizes[0][1]})
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    # Test only: the 800 ms pause on a right answer runs at 250 ms (check_hold keeps the real one), so a round is not mostly waiting.
    ctx.add_init_script("(() => { const st = window.setTimeout; window.setTimeout = (f, ms, ...a) => st(f, ms === 800 ? 250 : ms, ...a); })();")
    for w, h in sizes:
        page = ctx.new_page()
        page.set_viewport_size({'width': w, 'height': h})
        if route:
            page.route('**/games/%s/**' % SLUG, route)
        errors = []
        page.on('pageerror', lambda e, errs=errors: errs.append(str(e)))
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex')
        page.evaluate("""() => { window.__sub = []; window.MaffsLeaderboard = window.MaffsLeaderboard || {};
          MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
        if engine and (w, h) == sizes[0]:
            check_engine(page, fails, sample=None if stages == (1, 2, 3, 4) else 200)
            check_colours(page, fails)
        for stage in stages:
            if stages != (1, 2, 3, 4) and fails:    # a self-test plant already caught: no need to play it out
                break
            play_round(page, stage, {2, 3, 7}, '%dx%d' % (w, h), fails)
        if errors:
            fails.append('%dx%d: page errors %s' % (w, h, errors[:2]))
        page.close()
    if stages == (1, 2, 3, 4):
        page = ctx.new_page()
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex')
        check_slow(page, fails)
    ctx.close()


PLANTS = [
    ('a wrong label: HYP is given to a leg', "side('HYP', 1, 2, t[2], 0);\n    side(thetaAtA ? 'ADJ' : 'OPP', 0, 1, a, 1);",
     "side('OPP', 1, 2, t[2], 0);\n    side(thetaAtA ? 'ADJ' : 'HYP', 0, 1, a, 1);"),
    ('a wrong label: OPP and ADJ swapped', "side(thetaAtA ? 'ADJ' : 'OPP', 0, 1, a, 1);", "side(thetaAtA ? 'OPP' : 'ADJ', 0, 1, a, 1);"),
    ('a wrong function: sin and cos swapped', "FN = { sin: ['OPP', 'HYP'], cos: ['ADJ', 'HYP'],", "FN = { sin: ['ADJ', 'HYP'], cos: ['OPP', 'HYP'],"),
    ('a wrong function on Stage 4', "both.indexOf('OPP') >= 0 ? 'sin' : 'cos'", "both.indexOf('OPP') >= 0 ? 'cos' : 'sin'"),
    ('a fraction printed upside down', "it.frac = [lenOf(tri, p[0]), lenOf(tri, p[1])];", "it.frac = [lenOf(tri, p[1]), lenOf(tri, p[0])];"),
    ('feedback reworded', "Label from θ, not from the square corner.", "Label from the square corner."),
    ('a thin tap band', "'stroke-width': 44,", "'stroke-width': 30,"),
    ('a label on its line', "var clear = Math.abs(nx) * t.hw + Math.abs(ny) * t.hh + 7;", "var clear = 2;"),
    ('green feedback', ".fb-head{font-weight:700;font-size:1.05rem;color:var(--text)}", ".fb-head{font-weight:700;font-size:1.05rem;color:var(--correct)}"),
    ('a side colour on the score', ".hud-val{font-family:var(--font-num);", ".hud-val{color:var(--adj);font-family:var(--font-num);"),
    ('no word on a right answer', "(ok ? 'Right' : 'Not quite')", "(ok ? '' : 'Not quite')"),
    ('a dash-only hit area', "'stroke-width': 44,", "'stroke-width': 44, 'stroke-dasharray': '12 8',", 'stage 2'),
    ('a painted line that takes the tap', ".figure .side,.figure .square,.figure .arc{pointer-events:none}", ".figure .square,.figure .arc{pointer-events:none}", 'stage 2'),
    ('Stage 2 marks with no Check', "    showSlot(slot); refreshSlots();\n  }\n  function clearSlot", "    showSlot(slot); refreshSlots();\n    if (top.dataset.val && bottom.dataset.val) checkSlots();\n  }\n  function clearSlot", 'stage 2'),
    ('a full slot that will not empty', "    delete slot.dataset.val;\n", "", 'stage 2'),
    ('Check on with one slot empty', "$('checkBtn').disabled = !(top.dataset.val && bottom.dataset.val);", "$('checkBtn').disabled = !(top.dataset.val || bottom.dataset.val);", 'stage 2'),
    ('the old Stage 2 prompt', " Tap a box to empty it, then press Check.", "", 'stage 2'),
    ('the old behaviour: one side in both slots', " || top.dataset.val === val || bottom.dataset.val === val) return;", ") return;", 'stage 2'),
    ('the old behaviour: a second tap answers again', [("    if (state !== 'asking') return;\n    if (stage === 1) {\n      if (!MaffsLock.lock($('qarea'))) return;\n", "    if (stage === 1) {\n"),
                                                     ("draw.reserve = ok ? RESERVE[stage] : reserveFeedback();", "draw.tap = true; draw.reserve = ok ? RESERVE[stage] : reserveFeedback();")], None),
    ('a shorter hold', "MaffsLock.timer(advance, 800);", "MaffsLock.timer(advance, 200);", 'hold'),
    ('Next on a right answer', "      MaffsLock.timer(advance, 800);\n", "      fb.querySelector('.fb').insertAdjacentHTML('beforeend', '<div class=\"fb-next\"><button type=\"button\">Next</button></div>');\n      MaffsLock.timer(advance, 800);\n", 'hold'),
    ('the clock runs during the hold', "    askedAt = now();\n    tick();\n", "    tick();\n", 'hold'),
    ('a changed colour', "--opp:#0072B2", "--opp:#0072C2"),
    ('a small coloured word', ".w{font-weight:700;font-size:19px;", ".w{font-weight:700;font-size:15px;"),
]


def self_test(browser, base, src):
    global STOP_AT_FIRST
    STOP_AT_FIRST = True
    problems = 0
    for plant in PLANTS:
        name, old, new = plant[:3]
        try:
            if isinstance(old, list):               # a plant of several edits
                planted = src
                for o, n in old:
                    planted = pc.apply_plant(planted, o, n, name=name)
            else:
                planted = pc.apply_plant(src, old, new, name=name)
        except pc.StalePlant as e:
            print('  %s' % e)
            problems += 1
            continue

        def route(r, body=planted):
            return lambda rt: (rt.fulfill(status=200, content_type='text/html; charset=utf-8', body=body)
                               if rt.request.resource_type == 'document' else rt.continue_())
        found, err = [], None
        try:
            if len(plant) > 3 and plant[3] == 'hold':
                check_hold(browser, base, found, route=route(None), stages=(1,))
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else None
                problems += 0 if found else 1
                if not found:
                    print('  NOT CAUGHT: %s' % name)
                continue
            run_page(browser, base, found, route=route(None), sizes=SIZES[:1], stages=(2,) if len(plant) > 3 else (1,))
        except Exception as e:      # a plant that stops play is caught only if it left findings; an error alone is never a catch
            err = None if found else e
        if pc.is_caught(found, err):
            print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110]))
        else:
            print('  NOT CAUGHT: %s (%s)' % (name, err))
            problems += 1
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    fails, plants = [], 0
    proc, base = bc.start_stub_server()
    src = open(GAME, encoding='utf-8', newline='').read()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            run_page(browser, base, fails)
            check_aa(browser, base, fails)
            check_hold(browser, base, fails)
            plants = 0 if args.no_selftest else self_test(browser, base, src)
            browser.close()
    finally:
        proc.terminate()
    for f in fails[:30]:
        print('FAIL', f)
    print('%d failures; %d plants not caught' % (len(fails), plants))
    return 1 if fails or plants else 0


if __name__ == '__main__':
    sys.exit(main())
