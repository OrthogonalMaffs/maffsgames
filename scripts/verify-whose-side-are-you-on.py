#!/usr/bin/env python3
# ci-shards: Whose Side Are You On? (every item of the four stages recomputed from the triangle's own geometry, never the game's labels: which side is HYP, OPP and ADJ, every fraction, every function against real trig; the feedback table and its wording; 50 or more distinct items a stage; seeded rounds: HYP first, every quadrant; every stage played with real taps at 320, 390 and 1280 px: tap bands 44 px deep, each side clicked along its length and in the gaps of its dashes or dots, double clicks answering once and filling one slot, a right answer held 2.0 s (timed) lit with its mark and a character's line, the clock stopped, Stage 2's slots filled, cleared and refilled before Check, one answer a question, a slow right answer still right, no sideways scroll, Aa mode included, Next above the fold; Jon's characters (contract WHOSE-SIDE-PERSONALITY): the start screen, subtitle, right, wrong, streak and results lines compared with the contract's text, the right line never twice running, the Stage 1 speaker recomputed from the geometry; at 1366x768 and 1920x1080 the figure at least half the screen's height and every control on screen with nothing to scroll; Jon's ramp on the start screen (contract WHOSE-SIDE-ART): assets/start.webp at the card's width, 1600x873 and under 450 KB, θ in KaTeX inside the angle at the ramp's tip and within 6% of it at 320, 390 and 1920 wide, the tip measured from the picture's own pixels, the arc centred on it, the first stage against the fold reported; fault-injection self-test: θ moved off the tip, a wrong label, a wrong function, a wrong line, a missing shout-out, a small triangle and more, each caught) | | 3
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
  Characters   which character speaks over a wrong tap on Stage 1 is recomputed from the geometry; every line is compared with
               the contract's text (WHOSE-SIDE-PERSONALITY, 6 Nov 2026), held here, never read from the page.
  Start art    the ramp's tip is found from the WebP's own pixels (the red slope's lower edge fitted, the green base's top edge), and
               the θ the page draws, and its arc, are judged against that point (contract WHOSE-SIDE-ART, 6 Nov 2026).
In the page, a played round reads the drawn SVG back and compares it with the data; each tap goes through the real mouse.

    python scripts/verify-whose-side-are-you-on.py [--no-selftest] [--shard i/k] [--list-units]

Work units (contract SHARD, canon 7.8.1): the engine, a round of every stage at each size, the slow answer, Aa, the hold, the
lines, the large screen, the start art, then one unit a plant; CI runs them in the parts ci-groups.py chooses, locally all of them.
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
# Jon's characters and lines, verbatim from contract WHOSE-SIDE-PERSONALITY (6 Nov 2026). Compared exactly, never read from the page.
SUBTITLE = "One side never moves. The other two can't stop being polite about it."
LEGEND = [
    ('HYP', 'HYP, the longest side, across from the right angle.', '“I\'m here. I\'m always here.”'),
    ('OPP', 'OPP, across from θ.', '“Oh, I\'m opposite today? Splendid.”'),
    ('ADJ', 'ADJ, next to θ.', '“Then I shall stand beside it. After you.”'),
]
CLOSING = "Move θ, and the polite two swap. HYP doesn't flinch."
RIGHT_SAYS = ['HYP: “Correct. I remain unmoved.”', 'OPP: “Spot on. Do carry on.”', 'ADJ: “Marvellous. After you.”']
WRONG_SAYS = {
    'hyp': 'HYP: “I have been the hypotenuse since before you were born.”',
    'swap': 'OPP and ADJ: “Terribly sorry, I think you\'ll find we swapped.”',
}
SHOUTS = {3: 'HYP nods, very slightly.', 5: 'OPP and ADJ bow so politely they bump heads.', 10: 'HYP shows emotion. Once. Never again.'}
RESULT_SAYS = {'high': 'Sides labelled. HYP is quietly proud. He will never say so.',
               'low': 'The polite two are still bowing at each other in the corridor. Shall we go again?'}
HOLD_MS = 2000
BIG_SIZES = [(1366, 768), (1920, 1080)]
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


def expected_who(it, role_of_tap):
    """Which character speaks over a wrong tap on Stage 1, from the contract's two cases: HYP whenever HYP is asked for or tapped,
    the polite two when OPP and ADJ are mixed up. role_of_tap comes from geometry(), never from the game's own roles."""
    return 'hyp' if it['ask'] == 'HYP' or role_of_tap == 'HYP' else 'swap'


def result_say(right):
    """The results screen's character line for `right` correct out of 10: 8-10 and 0-5 have one, 6-7 none."""
    return RESULT_SAYS['high'] if right >= 8 else RESULT_SAYS['low'] if right <= 5 else None


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
    # Who speaks over a wrong tap on Stage 1: recomputed from the geometry for both wrong sides of each item (all of them, or a
    # sample of 60 in a self-test), never from the game's roles.
    items = page.evaluate('() => WS.gen.bank(1)')
    random.Random(5).shuffle(items)
    for it in items[:60 if sample else len(items)]:
        geo, _, _ = geometry(it)
        role_by_id = {s['id']: k for k, s in geo.items()}
        for s in it['sides']:
            if s['id'] == it['key']:
                continue
            got = page.evaluate('([q, t]) => WS.gen.whoSays(q, t)', [it, s['id']])
            if got != expected_who(it, role_by_id[s['id']]):
                fails.append('%s: a wrong tap on %s (%s) gets %s speaking, should be %s' % (it['id'], s['id'], role_by_id[s['id']], got, expected_who(it, role_by_id[s['id']])))
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


LAST_RIGHT = {}       # per page: the last right-answer line shown, which the next must differ from


def feedback_says(page):
    """The feedback's character line (its data and its text as rendered), its streak shout-out, and whether the line sits above
    the teaching line."""
    return page.evaluate("""() => { const f = document.querySelector('#feedback .fb'); if (!f) return null;
      const s = f.querySelector('.fb-say'), sh = f.querySelector('.fb-shout'), ln = f.querySelector('.fb-line');
      const txt = e => e ? e.textContent.replace(/\\s+/g, ' ').trim() : null;
      return {say: s ? s.dataset.say : null, sayText: txt(s), shout: sh ? sh.dataset.say : null, shoutText: txt(sh),
              above: !!(s && ln && (s.compareDocumentPosition(ln) & Node.DOCUMENT_POSITION_FOLLOWING))}; }""")


def check_right_says(page, streak, label, fails):
    """A right answer: one of Jon's three lines, never the one shown last; the shout-out exactly at a streak of 3, 5 or 10."""
    f = feedback_says(page)
    if not f or f['say'] not in RIGHT_SAYS or f['sayText'] != f['say']:
        fails.append('%s: right-answer line %s' % (label, f and (f['say'], f['sayText'])))
        return
    key = id(page)
    if LAST_RIGHT.get(key) == f['say']:
        fails.append('%s: the same right-answer line twice running: %s' % (label, f['say']))
    LAST_RIGHT[key] = f['say']
    want = SHOUTS.get(streak)
    if f['shout'] != want or f['shoutText'] != want:
        fails.append('%s: at a streak of %d the shout-out is %r, should be %r' % (label, streak, f['shoutText'], want))


def check_results_say(page, right, label, fails):
    want = result_say(right)
    got = page.evaluate("() => { const e = document.getElementById('resSay'); return e && e.getClientRects().length ? e.textContent.replace(/\\s+/g, ' ').trim() : null; }")
    if got != want:
        fails.append('%s: %d right: the results line is %r, should be %r' % (label, right, got, want))
    above = page.evaluate("() => { const s = document.getElementById('resSay'), n = document.getElementById('resScore'); return !!(s && (s.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_FOLLOWING)); }")
    if want and not above:
        fails.append('%s: the results line is not above the score' % label)


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
                f = feedback_says(page)
                want_say = WRONG_SAYS[expected_who(it, role_by_id[other])]
                if not f or f['say'] != want_say or f['sayText'] != want_say or not f['above']:
                    fails.append('%s: a wrong tap on %s for %s: character line %s, should be %r above the teaching line' % (label, role_by_id[other], it['ask'], f, want_say))
            elif feedback_says(page)['say'] is not None:
                fails.append('%s stage %d: a character line on a wrong answer outside Stage 1: %s' % (label, stage, feedback_says(page)['say']))
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
            check_right_says(page, streak, '%s stage %d q%d' % (label, stage, n + 1), fails)
            page.wait_for_function("() => WS.ui.state() !== 'right'", timeout=4000)
    page.wait_for_function("() => document.querySelector('#results').classList.contains('active')", timeout=4000)
    check_results_say(page, 10 - len(wrong_at), '%s stage %d' % (label, stage), fails)
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
    """A right answer on each stage: lit, "Right" and a character's line, no Next, for the real 2.0 s (Jon, 6 Nov), measured from the
    answer to the next question; taps ignored; then the next question by itself. An hour jumped during the hold must not reach the
    clock or the score. Real timers here: run_page's fast pause would hide all of this."""
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
                  next: document.querySelectorAll('.maffs-next-wrap button, .fb-next button').length, bands: document.querySelectorAll('#figure .hit').length, time: document.getElementById('hudTime').textContent,
                  say: (document.querySelector('#feedback .fb-say') || {dataset: {}}).dataset.say || null}; }""")
        if look['mark'] != '✓Right' or look['lit'] < 1 or look['next'] or look['bands'] or look['say'] not in RIGHT_SAYS:
            fails.append('stage %d hold: %s' % (stage, look))
        page.evaluate('() => window.__skip(3600)')          # an hour passes on the clock's own time source, during the hold
        page.wait_for_timeout(600)
        # taps and clicks during the hold: nothing moves
        page.mouse.click(195, 300)
        held = page.evaluate('() => [WS.ui.state(), WS.ui.question().id, document.getElementById("hudTime").textContent, WS.ui.score()]')
        if held != ['right', first['id'], look['time'], score]:
            fails.append('stage %d: during the hold %s, expected right, %s, %s, %s' % (stage, held, first['id'], look['time'], score))
        try:
            page.wait_for_function("(id) => WS.ui.state() === 'asking' && WS.ui.question().id !== id", arg=first['id'], timeout=3000)
        except Exception:
            fails.append('stage %d: no next question after the hold' % stage)
            continue
        page.wait_for_timeout(600)
        shown = page.evaluate('() => document.getElementById("hudTime").textContent')
        if int(shown.split(':')[0]) >= 30:
            fails.append('stage %d: the clock ran during the hold: %s' % (stage, shown))
        wait_asking(page)
        # The hold, timed in the page from the answer to the next question (wall clock, not the game's own time source).
        held_ms = page.evaluate("""() => new Promise(done => { const id = WS.ui.question().id, t0 = Date.now(); let right = false, score = null;
          WS.ui.answer(true);
          (function poll() { const s = WS.ui.state(), dt = Date.now() - t0;
            if (s === 'right' && !right) { right = true; score = WS.ui.score(); }
            if (right && s === 'asking' && WS.ui.question().id !== id) return done([dt, score]);
            if (dt > 6000) return done([-1, score]);
            requestAnimationFrame(poll); })(); })""")
        if not (HOLD_MS - 30 <= held_ms[0] <= HOLD_MS + 400):
            fails.append('stage %d: a right answer held %d ms, should be %d' % (stage, held_ms[0], HOLD_MS))
        if (held_ms[1] or 0) - score < 40:   # 5 seconds or less on the question scores far above this; an hour would not
            fails.append('stage %d: the hold reached the score: %s after %s' % (stage, held_ms[1], score))
    ctx.close()


def stub_board(page):
    """Every round this script finishes submits to a stand-in, never the live leaderboard: with Firebase reachable (CI) the real
    submitScore asks for initials over the results screen and would write to the board. Submissions are counted in window.__sub."""
    page.evaluate("""() => { window.__sub = []; window.MaffsLeaderboard = window.MaffsLeaderboard || {};
      MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")


def check_start(page, fails):
    """The start screen and subtitle, compared with the contract's text exactly; the legend keeps its line sample and letter."""
    got = page.evaluate("""() => { const t = e => e ? e.textContent.replace(/\\s+/g, ' ').trim() : null;
      return {sub: t(document.querySelector('#menu .header .sub')), closing: t(document.getElementById('closing')),
        rows: Array.from(document.querySelectorAll('#menu .key [role=listitem]')).map(r => [r.dataset.role, t(r.querySelector('.def')), t(r.querySelector('.say')),
          !!r.previousElementSibling && r.previousElementSibling.tagName === 'B' && !!r.previousElementSibling.previousElementSibling.querySelector('line.' + r.dataset.role)]),
        para: Array.from(document.querySelectorAll('#menu .menu-info > p')).map(p => t(p)), stages: document.querySelectorAll('#stageList [data-stage]').length}; }""")
    if got['sub'] != SUBTITLE:
        fails.append('subtitle %r' % got['sub'])
    rows = [r[:3] for r in got['rows']]
    if rows != [list(r) for r in LEGEND] or not all(r[3] for r in got['rows']):
        fails.append('start-screen legend %s' % got['rows'])
    if got['closing'] != CLOSING:
        fails.append('closing line %r' % got['closing'])
    if not any(p.startswith('Ten quick questions a stage.') for p in got['para']) or got['stages'] != 4:
        fails.append('the "Ten quick questions" line or the stage list is missing: %s, %d stages' % (got['para'], got['stages']))


# Jon's start-screen illustration and the θ over it (contract WHOSE-SIDE-ART, 6 Nov 2026).
ART = os.path.join(ROOT, 'games', SLUG, 'assets', 'start.webp')
ART_SIZE, ART_MAX_BYTES = (1600, 873), 450 * 1024
ART_SIZES = [(320, 568), (390, 844), (1920, 1080)]
ART_TOL = 0.06               # θ within 6% of the image's width of the tip
FOLD_SIZES = [(320, 568), (375, 667), (390, 844)]
# The tip, measured here from the picture's own pixels, never from the page's numbers: the red slope's lower edge is fitted by
# least squares along the slope, the green base's top edge is its median row, and the tip is where the two meet. The strips are
# picked out by colour (red: R > 190, G < 110, B < 90; green: G > 140, R < 130, B < 110).
MEASURE_TIP = """async () => {
  const img = document.querySelector('#startArt img');
  if (!img) return null;
  await img.decode();
  const W = img.naturalWidth, H = img.naturalHeight, c = document.createElement('canvas');
  c.width = W; c.height = H;
  const g = c.getContext('2d'); g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, W, H).data, px = (x, y) => { const i = (y * W + x) * 4; return [d[i], d[i + 1], d[i + 2]]; };
  const red = (x, y) => { const [r, gg, b] = px(x, y); return r > 190 && gg < 110 && b < 90; };
  const green = (x, y) => { const [r, gg, b] = px(x, y); return gg > 140 && r < 130 && b < 110; };
  const pts = [];
  for (let x = 400; x <= 1300; x += 10) { let lo = -1; for (let y = 0; y < H; y++) if (red(x, y)) lo = y; if (lo >= 0) pts.push([x, lo]); }
  const n = pts.length, sx = pts.reduce((s, p) => s + p[0], 0), sy = pts.reduce((s, p) => s + p[1], 0);
  const sxx = pts.reduce((s, p) => s + p[0] * p[0], 0), sxy = pts.reduce((s, p) => s + p[0] * p[1], 0);
  const m = (n * sxy - sx * sy) / (n * sxx - sx * sx), k = (sy - m * sx) / n;
  const tops = [];
  for (let x = 300; x <= 1300; x += 10) { for (let y = 0; y < H; y++) if (green(x, y)) { tops.push(y); break; } }
  tops.sort((a, b) => a - b);
  const base = tops[Math.floor(tops.length / 2)];
  return {W: W, H: H, m: m, k: k, base: base, x: (base - k) / m, y: base, n: n};
}"""
READ_ART = """() => {
  const wrap = document.getElementById('startArt'), img = wrap && wrap.querySelector('img'), th = document.getElementById('startTheta');
  const panel = document.querySelector('#menu .panel'), path = wrap && wrap.querySelector('path[data-arc]'), svg = wrap && wrap.querySelector('svg');
  const box = e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; };
  const f = document.querySelector('footer.site-footer'), fold = innerHeight - (f ? f.getBoundingClientRect().height : 0);
  const first = document.querySelector('#stageList [data-stage]');
  return {src: img ? img.getAttribute('src') : null, complete: !!img && img.complete, nat: img ? [img.naturalWidth, img.naturalHeight] : null,
    first: !!wrap && wrap === document.querySelector('#menu .header').nextElementSibling,
    img: img ? box(img) : null, panel: panel ? box(panel) : null, svg: svg ? box(svg) : null, vb: svg ? svg.getAttribute('viewBox') : null,
    radius: wrap ? [getComputedStyle(wrap).borderTopLeftRadius, panel ? getComputedStyle(panel).borderTopLeftRadius : null] : null,
    theta: th ? box(th) : null, katex: !!(th && th.querySelector('.katex')), thetaText: th ? th.textContent : null,
    colour: th ? getComputedStyle(th).color : null, text: getComputedStyle(document.body).color,
    font: th ? parseFloat(getComputedStyle(th).fontSize) : 0, arc: path ? path.getAttribute('d') : null,
    sw: document.documentElement.scrollWidth, vw: innerWidth, fold: fold, start: first ? first.getBoundingClientRect().bottom : null};
}"""


def check_art_static(fails):
    """The WebP itself: 1600 x 873 and under 450 KB (its pixels are read in the browser, below)."""
    size = os.path.getsize(ART) if os.path.isfile(ART) else None
    if size is None:
        fails.append('art: %s is missing' % os.path.relpath(ART, ROOT))
    elif size >= ART_MAX_BYTES:
        fails.append('art: start.webp is %d bytes, not under %d' % (size, ART_MAX_BYTES))
    return size


def judge_art(got, tip, label, fails):
    """One size: the picture at the top of the start screen at the card's width, θ in KaTeX over it, inside the angle at the tip,
    within ART_TOL of it, and the arc centred on the tip between the base and the slope, opening to the left."""
    if not got['src'] or not got['src'].endswith('assets/start.webp') or not got['complete'] or tuple(got['nat'] or ()) != ART_SIZE:
        fails.append('art %s: the start screen does not show assets/start.webp at 1600x873 (%s, %s)' % (label, got['src'], got['nat']))
        return
    if not got['first']:
        fails.append('art %s: the picture is not at the top of the start screen, under the title' % label)
    ix, iy, iw, ih = got['img']
    px, _, pw, _ = got['panel']
    if abs(ix - px) > 1 or abs(iw - pw) > 1 or abs(ih - iw * ART_SIZE[1] / ART_SIZE[0]) > 1.5:
        fails.append('art %s: the picture is %.0f px wide at x %.0f, the card %.0f at x %.0f (or its height is not auto)' % (label, iw, ix, pw, px))
    if got['radius'][0] != got['radius'][1]:
        fails.append('art %s: corners %s, the card %s' % (label, got['radius'][0], got['radius'][1]))
    if got['sw'] > got['vw']:
        fails.append('art %s: sideways scroll %d' % (label, got['sw']))
    s = iw / ART_SIZE[0]                                   # CSS px per image px
    if got['svg'] is None or got['vb'] != '0 0 1600 873' or any(abs(a - b) > 1 for a, b in zip(got['svg'], got['img'])):
        fails.append('art %s: the arc layer does not cover the picture in its coordinates (%s, %s)' % (label, got['svg'], got['vb']))
    if not got['katex'] or (got['thetaText'] or '').strip()[:1] != 'θ':
        fails.append('art %s: θ is not drawn in KaTeX over the picture (%r)' % (label, got['thetaText']))
        return
    if got['colour'] != got['text'] or got['font'] < 14:
        fails.append('art %s: θ is %s at %.1f px (the text colour %s, 14 px or more, wanted)' % (label, got['colour'], got['font'], got['text']))
    tx, ty, tw, th = got['theta']
    if tx < ix or ty < iy or tx + tw > ix + iw or ty + th > iy + ih:
        fails.append('art %s: θ is not on the picture (%s inside %s)' % (label, got['theta'], got['img']))
    cx, cy = (tx + tw / 2 - ix) / s, (ty + th / 2 - iy) / s    # θ's centre, in image pixels
    off = math.hypot(cx - tip['x'], cy - tip['y']) / ART_SIZE[0]
    if off > ART_TOL:
        fails.append('art %s: θ at (%.0f, %.0f) is %.1f%% of the width from the tip (%.0f, %.0f); at most %.0f%%' % (
            label, cx, cy, 100 * off, tip['x'], tip['y'], 100 * ART_TOL))
    slope_y = tip['m'] * cx + tip['k']
    if not (cx < tip['x'] and slope_y < cy < tip['base']):
        fails.append('art %s: θ at (%.0f, %.0f) is not inside the angle between the slope and the base' % (label, cx, cy))
    nums = [float(v) for v in (got['arc'] or '').replace(',', ' ').split() if v.replace('.', '', 1).replace('-', '', 1).isdigit()]
    if len(nums) != 9:
        fails.append('art %s: the arc %r is not one circular arc' % (label, got['arc']))
        return
    x0, y0, r, _, _, _, _, x1, y1 = nums
    ang = math.degrees(math.atan(tip['m']))              # the slope's rise, from the fit
    d0, d1 = math.hypot(x0 - tip['x'], y0 - tip['y']), math.hypot(x1 - tip['x'], y1 - tip['y'])
    a0 = math.degrees(math.atan2(tip['y'] - y0, tip['x'] - x0))
    a1 = math.degrees(math.atan2(tip['y'] - y1, tip['x'] - x1))
    if (abs(d0 - r) > 8 or abs(d1 - r) > 8 or x0 >= tip['x'] or x1 >= tip['x'] or abs(a0) > 2 or abs(a1 - ang) > 2
            or math.hypot(cx - tip['x'], cy - tip['y']) >= r):
        fails.append('art %s: the arc %r is not centred on the tip (%.0f, %.0f) from the base to the slope (%.1f deg), opening left, '
                     'with θ inside it' % (label, got['arc'], tip['x'], tip['y'], ang))


def check_art(browser, base, fails, route=None, sizes=ART_SIZES, report=True):
    """Jon's ramp on the start screen with θ at its tip, at 320, 390 and 1920 wide; the tip measured from the WebP's pixels. Then
    where the first stage button ends against the fold at the phone sizes, normal and Aa: reported, never judged (it was already
    below the fold at 320x568 on main before the picture: the start screen is report-only, measure-phone-fit.py's R4)."""
    if check_art_static(fails) is None:
        return
    tip, combos = None, [(s, False) for s in sizes]
    if report:
        combos += [(s, False) for s in FOLD_SIZES if s not in sizes] + [(s, True) for s in FOLD_SIZES]
    for (w, h), aa in combos:
        ctx = browser.new_context(viewport={'width': w, 'height': h})
        if aa:
            ctx.add_init_script("localStorage.setItem('mfg_accessible', 'true');")
        page = ctx.new_page()
        if route:
            page.route('**/games/%s/**' % SLUG, route)
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex' + (' && document.body.classList.contains("accessible")' if aa else ''))
        bc.wait_settled(page)
        if tip is None:
            tip = page.evaluate(MEASURE_TIP)
            if not tip or tip['n'] < 60 or not (0.45 < tip['m'] < 0.62) or not (1200 < tip['x'] < 1450 and 680 < tip['y'] < 790):
                fails.append('art: the ramp\'s tip could not be measured from the picture (%s)' % tip)
                ctx.close()
                return
            print('  art: tip measured at (%.1f, %.1f), slope %.2f deg' % (tip['x'], tip['y'], math.degrees(math.atan(tip['m']))))
        got = page.evaluate(READ_ART)
        label = '%dx%d%s' % (w, h, ' Aa' if aa else '')
        if (w, h) in sizes and not aa:
            judge_art(got, tip, label, fails)
        if (w, h) in FOLD_SIZES and report:
            print('  start fold %s: first stage ends at %.0f, fold %.0f (%s; reported, not judged)' % (
                label, got['start'], got['fold'], 'above' if got['start'] <= got['fold'] else 'below'))
        ctx.close()


def check_says(browser, base, fails, route=None):
    """Whole rounds answered through the lock hint, at speed: a perfect Stage 1 round (every right-answer line, never the same twice
    running, the shout-outs at 3, 5 and 10 and nowhere else, the 8-10 results line), a round of four right (the Stage 1 speaker for
    each wrong tap from the geometry, the 0-5 line) and one of six right (no results line)."""
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script("(() => { const st = window.setTimeout; window.setTimeout = (f, ms, ...a) => st(f, ms === %d ? 200 : ms, ...a); })();" % HOLD_MS)
    page = ctx.new_page()
    if route:
        page.route('**/games/%s/**' % SLUG, route)
    page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
    page.wait_for_function('() => !!window.WS && !!window.katex')
    stub_board(page)
    for stage, wrong_at in ((1, set()), (1, {0, 2, 4, 5, 6, 8}), (3, {1, 5, 6, 9})):
        page.evaluate('(n) => WS.ui.start(n)', stage)
        streak = 0
        for n in range(10):
            label = 'lines stage %d q%d' % (stage, n + 1)
            wait_asking(page)
            it = page.evaluate('() => WS.ui.question()')
            wrong = n in wrong_at
            page.evaluate('(r) => WS.ui.answer(r)', not wrong)
            page.wait_for_function("() => WS.ui.state() === 'right' || WS.ui.state() === 'wrong'", timeout=4000)
            if wrong:
                streak = 0
                if stage == 1:
                    geo, _, _ = geometry(it)
                    role_by_id = {s['id']: k for k, s in geo.items()}
                    tapped = [s['id'] for s in it['sides'] if s['id'] != it['key']][0]      # the side WS.ui.answer(false) taps
                    want = WRONG_SAYS[expected_who(it, role_by_id[tapped])]
                    f = feedback_says(page)
                    if not f or f['say'] != want or f['sayText'] != want or not f['above'] or f['shout']:
                        fails.append('%s: wrong tap on %s for %s: %s, should be %r above the teaching line' % (label, role_by_id[tapped], it['ask'], f, want))
                page.click('.maffs-next-wrap button, .fb-next button')
            else:
                streak += 1
                check_right_says(page, streak, label, fails)
                page.wait_for_function("() => WS.ui.state() !== 'right'", timeout=4000)
        page.wait_for_function("() => document.querySelector('#results').classList.contains('active')", timeout=4000)
        check_results_say(page, 10 - len(wrong_at), 'lines stage %d' % stage, fails)
        if page.evaluate('() => { const n = window.__sub.length; window.__sub = []; return n; }') != 1:
            fails.append('lines stage %d: not one board submission' % stage)
        page.wait_for_function('() => !MaffsLock.isFresh()', timeout=4000)
        page.click('#menuBtn')
    ctx.close()


def check_big(browser, base, fails, route=None, sizes=BIG_SIZES, stages=(1, 2, 3, 4)):
    """Large screens (contract item 8): the figure's drawn height at least half the screen, the question and every answer control
    on screen with nothing to scroll, before and after a wrong answer (Next too), and the right-answer line in view during the hold.
    The triangle inside keeps its shape, so its own height varies with its proportions; the figure it fills is what is sized."""
    for w, h in sizes:
        ctx = browser.new_context(viewport={'width': w, 'height': h})
        ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
        page = ctx.new_page()
        if route:
            page.route('**/games/%s/**' % SLUG, route)
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex')
        for stage in stages:
            for when in ('asking', 'wrong', 'right'):
                page.evaluate('(n) => WS.ui.start(n)', stage)
                wait_asking(page)
                if when != 'asking':
                    page.evaluate('(r) => WS.ui.answer(r)', when == 'right')
                    page.wait_for_function('(s) => WS.ui.state() === s', arg=when, timeout=4000)
                    page.wait_for_timeout(100)
                m = page.evaluate("""() => { const b = e => e.getBoundingClientRect(), svg = document.querySelector('#figure svg');
                  const shown = s => Array.from(document.querySelectorAll(s)).filter(e => e.getClientRects().length);
                  const ctl = shown('#figure .hit, #slotTop, #slotBottom, #checkBtn, #opts .opt, #ask, .maffs-next-wrap button, .fb-next button, #feedback .fb-head, #feedback .fb-say');
                  return {svgH: svg ? b(svg).height : 0, bottom: Math.max(...ctl.map(e => b(e).bottom)), top: Math.min(...ctl.map(e => b(e).top)), n: ctl.length,
                    next: shown('.maffs-next-wrap button, .fb-next button').length, say: shown('#feedback .fb-say').length,
                    sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth}; }""")
                label = '%dx%d stage %d %s' % (w, h, stage, when)
                if m['svgH'] < 0.5 * h:
                    fails.append('%s: the figure is drawn %.0f px tall, under half the screen (%d)' % (label, m['svgH'], h))
                if m['bottom'] > h - 40 or m['top'] < 0:
                    fails.append('%s: the question or a control is off screen (%.0f to %.0f, fold %d)' % (label, m['top'], m['bottom'], h - 40))
                if m['sh'] > h or m['sw'] > w:
                    fails.append('%s: the page scrolls (%d x %d in %d x %d)' % (label, m['sw'], m['sh'], w, h))
                if when == 'wrong' and not m['next']:
                    fails.append('%s: no Next' % label)
                if when == 'right' and not m['say']:
                    fails.append('%s: no right-answer line in view' % label)
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
    # Test only: the 2.0 s pause on a right answer runs at 250 ms (check_hold keeps the real one), so a round is not mostly waiting.
    ctx.add_init_script("(() => { const st = window.setTimeout; window.setTimeout = (f, ms, ...a) => st(f, ms === %d ? 250 : ms, ...a); })();" % HOLD_MS)
    for w, h in sizes:
        page = ctx.new_page()
        page.set_viewport_size({'width': w, 'height': h})
        if route:
            page.route('**/games/%s/**' % SLUG, route)
        errors = []
        page.on('pageerror', lambda e, errs=errors: errs.append(str(e)))
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex')
        stub_board(page)
        if engine and (w, h) == sizes[0]:
            check_engine(page, fails, sample=None if stages == (1, 2, 3, 4) else 200)
            check_colours(page, fails)
            check_start(page, fails)
        for stage in stages:
            if stages != (1, 2, 3, 4) and fails:    # a self-test plant already caught: no need to play it out
                break
            play_round(page, stage, {2, 3, 7}, '%dx%d' % (w, h), fails)
        if errors:
            fails.append('%dx%d: page errors %s' % (w, h, errors[:2]))
        page.close()
    ctx.close()


def one_page(browser, base, size=SIZES[0]):
    ctx = browser.new_context(viewport={'width': size[0], 'height': size[1]})
    page = ctx.new_page()
    page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
    page.wait_for_function('() => !!window.WS && !!window.katex')
    return ctx, page


def run_engine(browser, base, fails):
    """Every item of every stage from the geometry, the sessions, the speakers, the colours and the start screen."""
    ctx, page = one_page(browser, base)
    check_engine(page, fails)
    check_colours(page, fails)
    check_start(page, fails)
    ctx.close()


def run_slow(browser, base, fails):
    ctx, page = one_page(browser, base)
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
    ('a label on its line', "var clear = Math.abs(nx) * t.hw + Math.abs(ny) * t.hh + 7 * g;", "var clear = 2;"),
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
    ('a shorter hold', "MaffsLock.timer(advance, HOLD_MS);", "MaffsLock.timer(advance, 200);", 'hold'),
    ('the old 0.8 s hold', "var HOLD_MS = 2000;", "var HOLD_MS = 800;", 'hold'),
    ('Next on a right answer', "      MaffsLock.timer(advance, HOLD_MS);\n", "      fb.querySelector('.fb').insertAdjacentHTML('beforeend', '<div class=\"fb-next\"><button type=\"button\">Next</button></div>');\n      MaffsLock.timer(advance, HOLD_MS);\n", 'hold'),
    ('the clock runs during the hold', "    askedAt = now();\n    tick();\n", "    tick();\n", 'hold'),
    ('a changed colour', "--opp:#0072B2", "--opp:#0072C2"),
    ('a small coloured word', ".w{font-weight:700;font-size:19px;", ".w{font-weight:700;font-size:15px;"),
    # contract WHOSE-SIDE-PERSONALITY: Jon's lines, the speaker rule, the shout-outs, the results line, the large screen
    ('a wrong line', "since before you were born.", "since you were born."),
    ('a start-screen line reworded', "Oh, I'm opposite today? Splendid.", "Oh, I'm opposite today!"),
    ('the subtitle reworded', "The other two can't stop being polite about it.", "The other two are polite about it."),
    ('the wrong speaker: HYP tapped, the polite two answer', "return it.ask === 'HYP' || tapped === it.roles.HYP ? 'hyp' : 'swap';", "return it.ask === 'HYP' ? 'hyp' : 'swap';"),
    ('a missing streak shout-out at 5', " 5: 'OPP and ADJ bow so politely they bump heads.',", "", 'says'),
    ('the same right-answer line twice running', "    if (lastRight >= 0 && i >= lastRight) i++;\n", "    i = 0;\n", 'says'),
    ('no results line at 8-10 right', "var resLine = rightCount >= 8 ? SAYS.high : rightCount <= 5", "var resLine = rightCount >= 11 ? SAYS.high : rightCount <= 5", 'says'),
    ('a small triangle at 1920x1080', "var H = Math.max(240, Math.floor(window.innerHeight - below - top - pad));", "var H = 400;", 'big'),
    # contract WHOSE-SIDE-ART: θ over the ramp's tip
    ('θ at the square corner', "left:77.49%;top:81.50%;", "left:14.5%;top:81.5%;", 'art'),
    ('θ off the tip, on the concrete', "left:77.49%;top:81.50%;", "left:91%;top:80%;", 'art'),
    ('θ slid up the slope, 7.5% from the tip', "left:77.49%;top:81.50%;", "left:76.2%;top:77.6%;", 'art'),
    ('the arc centred off the tip', 'd="M 1155.2 733 A 170 170 0 0 1 1175.6 652.3"', 'd="M 1055.2 733 A 170 170 0 0 1 1075.6 652.3"', 'art'),
    ('θ in plain text, not KaTeX', "    $('startTheta').innerHTML = THETA();", "", 'art'),
]


def self_test(browser, base, src, shard, mine):
    """Each plant is its own work unit: those in `mine` run, each timed by shard.unit()."""
    global STOP_AT_FIRST
    STOP_AT_FIRST = True
    problems = 0
    for plant in PLANTS:
        if 'plant: ' + plant[0] not in mine:
            continue
        with shard.unit('plant: ' + plant[0]):
            problems += one_plant(browser, base, src, plant)
    return problems


def one_plant(browser, base, src, plant):
    """0 if the plant was caught, 1 if not (or stale)."""
    if True:
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
            return 1

        def route(r, body=planted):
            return lambda rt: (rt.fulfill(status=200, content_type='text/html; charset=utf-8', body=body)
                               if rt.request.resource_type == 'document' else rt.continue_())
        found, err = [], None
        try:
            if len(plant) > 3 and plant[3] == 'art':
                check_art(browser, base, found, route=route(None), report=False)
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            if len(plant) > 3 and plant[3] in ('says', 'big'):
                (check_says(browser, base, found, route=route(None)) if plant[3] == 'says'
                 else check_big(browser, base, found, route=route(None), sizes=[(1920, 1080)], stages=(1,)))
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            if len(plant) > 3 and plant[3] == 'hold':
                check_hold(browser, base, found, route=route(None), stages=(1,))
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else None
                if not found:
                    print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            run_page(browser, base, found, route=route(None), sizes=SIZES[:1], stages=(2,) if len(plant) > 3 else (1,))
        except Exception as e:      # a plant that stops play is caught only if it left findings; an error alone is never a catch
            err = None if found else e
        if pc.is_caught(found, err):
            print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110]))
        else:
            print('  NOT CAUGHT: %s (%s)' % (name, err))
            return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    bc.shard_args(ap)
    args = ap.parse_args()
    units = ['engine'] + ['play %dx%d' % s for s in SIZES] + ['slow', 'aa', 'hold', 'lines', 'big', 'art']
    if not args.no_selftest:
        units += ['plant: ' + plant[0] for plant in PLANTS]
    shard = bc.Shard(__file__, args)
    mine = shard.pick(units)
    fails, plants = [], 0
    proc, base = bc.start_stub_server()
    src = open(GAME, encoding='utf-8', newline='').read()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            work = [('engine', lambda: run_engine(browser, base, fails))]
            work += [('play %dx%d' % s, lambda s=s: run_page(browser, base, fails, sizes=[s], engine=False)) for s in SIZES]
            work += [('slow', lambda: run_slow(browser, base, fails)), ('aa', lambda: check_aa(browser, base, fails)),
                     ('hold', lambda: check_hold(browser, base, fails)), ('lines', lambda: check_says(browser, base, fails)),
                     ('big', lambda: check_big(browser, base, fails)), ('art', lambda: check_art(browser, base, fails))]
            for uid, fn in work:
                if uid in mine:
                    with shard.unit(uid):
                        fn()
            plants = self_test(browser, base, src, shard, mine)
            browser.close()
    finally:
        proc.terminate()
    for f in fails[:30]:
        print('FAIL', f)
    print('%d failures; %d plants not caught' % (len(fails), plants))
    return 1 if fails or plants else 0


if __name__ == '__main__':
    sys.exit(main())
