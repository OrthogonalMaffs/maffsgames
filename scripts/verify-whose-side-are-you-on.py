#!/usr/bin/env python3
# ci-shards: Whose Side Are You On? (every item of the four stages recomputed from the triangle's own geometry, never the game's labels: which side is HYP, OPP and ADJ, every fraction, every function against real trig; the feedback table and its wording; 50 or more distinct items a stage; seeded rounds: HYP first, every quadrant; every stage played with real taps at 320, 390 and 1280 px: tap bands 44 px deep, each side clicked along its length and in the gaps of its dashes or dots, double clicks answering once and filling one slot, a right answer held 2.0 s (timed) lit with its mark and its rule, the clock stopped, Stage 2's slots filled, cleared and refilled before Check, one answer a question, a slow right answer still right, no sideways scroll, Aa mode included, Next above the fold; the start screen and the sides' bios (contract WHOSE-SIDE-BIOS): the key's definitions, the closing line, the three bios, the subtitle, the Stages heading, stage list and scoring line compared with the contract's text, each key row a button that shows its bio by mouse and keyboard, the ramp's three strips measured from the WebP's pixels and each one's side worked out from the triangle they make (HYP the strip not through the right angle, OPP the strip not through the tip), real clicks along each strip showing that side's bio and ringing that strip in its line style, every point of each strip's tap region 44 px deep at 320 and 390 and no two regions overlapping; no character line anywhere, on the start screen or in play or on the results screen; every marked answer's panel recomputed from the geometry: Stage 1's rule sentence and misconception line, on Stages 2-4 the equation (sin, cos or tan of θ over its stacked fraction, numerator and denominator from FN, each in its side colour, at the fraction line's size) on right and wrong answers alike, with Stage 2's numbers and Stage 4's 'Use both' line under it on a wrong answer; at 1366x768 and 1920x1080 the figure at least half the screen's height and every control on screen with nothing to scroll; the triangle's fit (contract WHOSE-SIDE-FIT): a seeded round of every stage, as asked and after an answer, its content box (corners padded by half the tap band, labels, θ, the square) measured on screen reaching the 6g pad at both ends of its limiting axis within 1 px and the triangle at least 70% of the figure there at 1366x768 and 1920x1080, no label, θ or tap band clipped there and at 320 and 390; the question's last line of text above the first control below it and no text in the right-hand column over another element, every stage asking, wrong and right, at 1024x700, 1222x688, 1366x768, 1920x1080 and 1024x1366; Jon's ramp on the start screen (contract WHOSE-SIDE-ART): assets/start.webp at the card's width up to 600 px, centred, 1600x873 and under 450 KB, θ in KaTeX inside the angle at the ramp's tip and within 6% of it at 320, 390 and 1920 wide, the tip measured from the picture's own pixels, the arc centred on it, the first stage against the fold reported (phones, 1366x768, 1920x1080); fault-injection self-test: θ moved off the tip, a wrong label, a wrong function, bios swapped, a strip mapped to the wrong side, a character line in the panel, the rule missing, its fraction upside down or a sentence again, the old closing line, the scoring line removed, a small triangle, the old margin (as wasted space), the triangle centred (as a clipped label), the old grid rows (as text under a button) and more, each caught) | | 3
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
  Panel        each marked answer's rule (Stage 1's sentence; on Stages 2-4 the function the geometry needs and the two sides FN
               gives it, read back off the drawn equation: which word is on top, their colours) and the lines under it.
  Start screen the key, the closing line and the bios compared with the contract's text (WHOSE-SIDE-BIOS, 6 Nov 2026), held here,
               never read from the page; no character line anywhere (docs/whose-side-lines.md).
  Ramp strips  the three strips are measured from the WebP's pixels, and which is HYP, OPP and ADJ is worked out from the triangle
               their lines make: the corner at 90 degrees, and the tip where θ is.
  Start art    the ramp's tip is found from the WebP's own pixels (the red slope's lower edge fitted, the green base's top edge), and
               the θ the page draws, and its arc, are judged against that point (contract WHOSE-SIDE-ART, 6 Nov 2026).
In the page, a played round reads the drawn SVG back and compares it with the data; each tap goes through the real mouse.

    python scripts/verify-whose-side-are-you-on.py [--no-selftest] [--shard i/k] [--list-units]

Work units (contract SHARD, canon 7.8.1): the engine, a round of every stage at each size, the slow answer, Aa, the hold, the
lines, the bios, the large screen, the start art, the fit at each of four sizes, then one unit a plant; CI runs them in the parts ci-groups.py chooses, locally all of them.
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
# The start screen, verbatim from contract WHOSE-SIDE-BIOS (6 Nov 2026). Compared exactly, never read from the page.
SUBTITLE = "One side never moves. The other two can't stop being polite about it."   # unchanged: Jon has not decided on it
OPENING = 'Every side gets its name from the marked angle.'
KEY = [
    ('HYP', 'H', 'HYP, the longest side, across from the right angle.'),
    ('OPP', 'O', "OPP, across from θ: the only side that doesn't touch it."),
    ('ADJ', 'A', 'ADJ, next to θ, and not the hypotenuse.'),
]
BIO_DEFAULT = 'Tap a side of the ramp, or its name, to meet it.'
CLOSING = 'Put θ in the other corner and OPP and ADJ swap. HYP stays put.'
SCORING = 'Ten quick questions a stage. No lives: a faster right answer scores more, a slow one is still right.'
STAGES_HEADING = 'Stages'
STAGE_LIST = [('Tap the side', 'Find HYP, OPP or ADJ on the triangle, however it is turned.'),
              ('Build the fraction', 'Tap the sides into a fraction: OPP over HYP.'),
              ('Name it', 'Match each fraction to sin, cos or tan, then back again.'),
              ('Which function?', 'One side known, one side wanted: pick the function.')]   # unchanged (DO NOT TOUCH): main at 86b56ec
BIOS = {
    'HYP': [('Location', "Opposite the right angle. That's my spot, I earned it, and I'm not moving."), ('Length', 'Bigger than the other two. Always.'),
            ('Favourite number', 'The biggest one.')],
    'OPP': [('Location', "The only side that doesn't touch θ. I'm shy."), ('Length', 'Ask my friend Pythagoras, he always knows.'),
            ('Favourite number', "6. I'm opposite 1 on a dice.")],
    'ADJ': [('Location', "Right next to θ, and I'm not the hypotenuse. Personal space is overrated."),
            ('Length', "Always positive; other than that, I'm flexible. I can do a handstand, don't you know."), ('Favourite number', '52!')],
}
# Stage 1's rule sentence, right and wrong (item 6; HYP's and ADJ's worded as the key words them, OPP's the contract's example).
RULE1 = {'HYP': "That's HYP: the longest side, across from the right angle.", 'OPP': "That's OPP: the only side that doesn't touch θ.",
         'ADJ': "That's ADJ: next to θ, and not the hypotenuse."}
# Every character line taken out (docs/whose-side-lines.md): none may appear anywhere, on the start screen or in play.
OLD_LINES = ["I'm here. I'm always here.", "Oh, I'm opposite today? Splendid.", 'Then I shall stand beside it. After you.',
             "Move θ, and the polite two swap. HYP doesn't flinch.", 'Correct. I remain unmoved.', 'Spot on. Do carry on.', 'Marvellous. After you.',
             'I have been the hypotenuse since before you were born.', "Terribly sorry, I think you'll find we swapped.",
             'HYP nods, very slightly.', 'OPP and ADJ bow so politely they bump heads.', 'HYP shows emotion. Once. Never again.',
             'Sides labelled. HYP is quietly proud. He will never say so.', 'The polite two are still bowing at each other in the corridor. Shall we go again?']
HOLD_MS = 2000
BIG_SIZES = [(1366, 768), (1920, 1080)]
# Contract WHOSE-SIDE-FIT (6 Nov 2026, Amendment 1): the fit is judged on a seeded round of every stage at these sizes (no wasted
# space at the two large sizes, nothing clipped at all four), the question text against the controls at TEXT_SIZES.
FIT_SIZES = [(1366, 768), (1920, 1080), (320, 568), (390, 844)]
TEXT_SIZES = [(1024, 700), (1222, 688), (1366, 768), (1920, 1080), (1024, 1366)]
FIT_SEED = 20261106
FIT_FLOOR = 0.70
# A fixed seed for the round's Math.random (canon 7.8.4: a gate never samples at random), set just before the stage starts.
SEED_JS = """(s) => { let a = s >>> 0; Math.random = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }"""
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


def expected_feedback(it, ok, tapped=None):
    """What the panel must carry for this item (contract WHOSE-SIDE-BIOS item 6, Jon's answers of 6 Nov), from the geometry alone:
    (the function whose equation is the rule, or None on Stage 1; the plain lines under it). On Stage 1 a wrong tap is `tapped`."""
    geo, theta, _ = geometry(it)
    role_by_id = {s['id']: k for k, s in geo.items()}
    v = it['verts']
    drawn = {k: dist(v[s['from']], v[s['to']]) for k, s in geo.items()}
    lens = {k: s['len'] for k, s in geo.items()}
    stage = it['stage']
    if stage == 1:
        return None, [RULE1[it['ask']]] if ok else [RULE1[it['ask']], SPEC_LINES[expected_why(it, role_by_id[tapped], tapped)]]
    if stage == 2:
        top, bottom = it['top'], it['bottom']
        fns = real_function(theta, drawn, top, bottom)
        line = '%s is %s and %s is %s, so %s over %s is %s over %s.' % (top, lens[top], bottom, lens[bottom], top, bottom, lens[top], lens[bottom])
        return (fns[0] if len(fns) == 1 else '?'), ([] if ok else [line])
    if stage == 3:
        if it['dir'] == 'name':
            fns = real_function(theta, drawn, it['top'], it['bottom'])
            return (fns[0] if len(fns) == 1 else '?'), []
        return it['fn'], []                                     # check_item has proven fn's sides against real trig
    pair = {it['knownRole'], it['wantedRole']}
    hits = [f for f, s in FN_SIDES.items() if set(s) == pair and abs(REAL[f](theta) - drawn[s[0]] / drawn[s[1]]) < 1e-9]
    return (hits[0] if len(hits) == 1 else '?'), ([] if ok else [SPEC_LINES['both']])


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


# Text as a student reads it: each KaTeX formula as its rendered glyphs (θ, not its hidden MathML and TeX source), spaces collapsed.
NORM_JS = """window.__norm = e => { if (!e) return null; const c = e.cloneNode(true);
  c.querySelectorAll('.katex').forEach(k => { const h = k.querySelector('.katex-html'); k.replaceWith(document.createTextNode(h ? h.textContent : '')); });
  return c.textContent.replace(/\\s+/g, ' ').trim(); };"""

# The marked panel: the verdict, its plain lines, and its rule read off the screen: the function's name as KaTeX drew it, and the
# two side words with their colours and boxes (so which is on top, and whether they are stacked over a fraction bar, is measured).
READ_FB = """() => { const f = document.querySelector('#feedback .fb'); if (!f) return null;
  const h = f.querySelector('.fb-head'), rules = Array.from(f.querySelectorAll('.fb-rule'));
  const out = {mark: h ? [h.dataset.mark, h.textContent] : null, lines: Array.from(f.querySelectorAll('.fb-line')).map(l => __norm(l)),
    rules: rules.length, rule: null};
  const r = rules[0];
  if (r) {
    const html = r.querySelector('.katex-html'), words = [];
    if (html) html.querySelectorAll('*').forEach(e => { if (e.children.length === 0 && /^(HYP|OPP|ADJ)$/.test(e.textContent.trim())) {
      const b = e.getBoundingClientRect(); words.push({w: e.textContent.trim(), colour: getComputedStyle(e).color, top: b.top, bottom: b.bottom, cx: (b.left + b.right) / 2}); } });
    const bar = html && html.querySelector('.frac-line'), bb = bar ? bar.getBoundingClientRect() : null;
    const fr = document.getElementById('fracline');
    out.rule = {fn: html ? Array.from(html.querySelectorAll('.mop')).map(e => e.textContent).join('|') : null, text: __norm(r), words: words,
      bar: bb ? [bb.top, bb.bottom] : null, size: getComputedStyle(r).fontSize, fracSize: getComputedStyle(fr).fontSize};
  }
  return out; }"""


def check_feedback(page, it, ok, label, fails, tapped=None):
    """Item 6 with Jon's answers: the verdict; on Stages 2-4 one rule, the equation `fn θ = top/bottom` stacked, top and bottom the
    sides FN_SIDES gives for the function the geometry needs, each in its side colour, at the fraction line's size; on Stage 1 no
    equation; and the plain lines expected_feedback works out, in order. Nothing else."""
    page.evaluate(NORM_JS)
    f = page.evaluate(READ_FB)
    if not f:
        fails.append('%s: no feedback panel' % label)
        return
    if f['mark'] != (['right', '✓Right'] if ok else ['wrong', '✗Not quite']):
        fails.append('%s: the verdict reads %s' % (label, f['mark']))
    fn, lines = expected_feedback(it, ok, tapped)
    if f['lines'] != lines:
        fails.append('%s: the panel\'s lines %s, should be %s' % (label, f['lines'], lines))
    if fn is None:
        if f['rules']:
            fails.append('%s: an equation on Stage 1: %s' % (label, f['rule']))
        return
    r = f['rule']
    if f['rules'] != 1 or not r:
        fails.append('%s: %d rule equations on a %s answer, should be 1 (%s)' % (label, f['rules'], 'right' if ok else 'wrong', fn))
        return
    top, bottom = FN_SIDES.get(fn, ('?', '?'))
    words = r['words']
    if r['fn'] != fn or not r['text'].replace(' ', '').startswith(fn + 'θ=') or len(words) != 2 or not r['bar']:
        fails.append('%s: the rule is %r (function %s, %d side words, fraction bar %s), should be %s θ = %s/%s stacked'
                     % (label, r['text'], r['fn'], len(words), r['bar'], fn, top, bottom))
        return
    up, down = sorted(words, key=lambda w: w['top'])
    stacked = up['bottom'] <= r['bar'][1] + 1 and down['top'] >= r['bar'][0] - 1 and abs(up['cx'] - down['cx']) < 12
    if (up['w'], down['w']) != (top, bottom) or not stacked:
        fails.append('%s: the rule\'s fraction is %s over %s%s, should be %s over %s' % (label, up['w'], down['w'], '' if stacked else ' (not stacked)', top, bottom))
    for w in words:
        if w['colour'] != rgb(COLOURS[w['w']]):
            fails.append('%s: %s in the rule is %s, not its side colour' % (label, w['w'], w['colour']))
    if r['size'] != r['fracSize']:
        fails.append('%s: the rule is %s, the fraction line %s' % (label, r['size'], r['fracSize']))


# No character speaks: no quotation marks, none of the lines taken out, none of their old containers. On the start screen the
# subtitle (#subtitle) is exempt (Jon has not decided on it) and the bios are the sides' own; `scope` is what is read.
SPEECH_JS = """([scope, old]) => { const out = [], root = document.querySelector(scope); if (!root) return out;
  const c = root.cloneNode(true), sub = c.querySelector('#subtitle'); if (sub) sub.remove();
  c.querySelectorAll('.katex').forEach(k => { const h = k.querySelector('.katex-html'); k.replaceWith(document.createTextNode(h ? h.textContent : '')); });
  const text = c.textContent.replace(/\\s+/g, ' ');
  if (/[“”]/.test(text)) out.push('a quotation: ' + text.slice(Math.max(0, text.search(/[“”]/) - 40), text.search(/[“”]/) + 50));
  old.forEach(l => { if (text.includes(l)) out.push('a line taken out: ' + l); });
  if (root.querySelector('.fb-say, .fb-shout, .say, #resSay, .res-say, [data-say]')) out.push('a character line\\'s container');
  return out; }"""


def check_no_speech(page, scope, label, fails):
    for p in page.evaluate(SPEECH_JS, [scope, OLD_LINES]):
        fails.append('%s: %s' % (label, p))


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
            # the panel: the verdict, the rule (Stage 1's sentence, or the equation) and the lines under it, from the geometry
            check_feedback(page, it, False, '%s stage %d q%d' % (label, stage, n + 1), fails,
                           tapped=[s['id'] for s in it['sides'] if s['id'] != it['key']][0] if stage == 1 else None)
            check_no_speech(page, '#game', '%s stage %d q%d wrong' % (label, stage, n + 1), fails)
            btn = page.query_selector('.maffs-next-wrap button') or page.query_selector('.fb-next button')
            if not btn:
                fails.append('%s: no Next on a wrong answer' % label)
                return
            r = btn.bounding_box()
            if r['y'] + r['height'] > h - 40:
                fails.append('%s stage %d: Next below the fold, %.0f in %d' % (label, stage, r['y'] + r['height'], h))
            btn.click()
        else:
            check_feedback(page, it, True, '%s stage %d q%d' % (label, stage, n + 1), fails)
            check_no_speech(page, '#game', '%s stage %d q%d right' % (label, stage, n + 1), fails)
            page.wait_for_function("() => WS.ui.state() !== 'right'", timeout=4000)
    page.wait_for_function("() => document.querySelector('#results').classList.contains('active')", timeout=4000)
    check_no_speech(page, '#results', '%s stage %d results' % (label, stage), fails)
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
    """A right answer on each stage: lit, "Right" and its rule, no Next, for the real 2.0 s (Jon, 6 Nov), measured from the
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
                  rule: document.querySelectorAll('#feedback .fb-rule, #feedback .fb-line').length}; }""")
        if look['mark'] != '✓Right' or look['lit'] < 1 or look['next'] or look['bands'] or not look['rule']:
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


READ_START = """() => { const panel = document.querySelector('#menu .menu-info'), bio = document.getElementById('bio');
  const kids = panel ? Array.from(panel.children).map(e => e.tagName + (e.id ? '#' + e.id : '') + (e.className ? '.' + e.className.split(' ')[0] : '')) : [];
  return {sub: __norm(document.getElementById('subtitle')), kids: kids, para: panel ? Array.from(panel.querySelectorAll(':scope > p')).map(p => __norm(p)) : [],
    heading: __norm(panel && panel.querySelector(':scope > .mode-h')),
    stages: Array.from(document.querySelectorAll('#stageList [data-stage]')).map(b => [b.dataset.stage, __norm(b.querySelector('.t')), __norm(b.querySelector('.d'))]),
    rows: Array.from(document.querySelectorAll('#menu .key > *')).filter(e => e !== bio).map(r => ({tag: r.tagName, type: r.getAttribute('type'), role: r.dataset.role,
      pressed: r.getAttribute('aria-pressed'), letter: __norm(r.querySelector(':scope > b')), swatch: !!r.querySelector(':scope > svg line.' + r.dataset.role),
      def: __norm(r.querySelector('.def')), katex: r.querySelectorAll('.def .katex').length})),
    bioInKey: !!bio && bio.parentElement === document.querySelector('#menu .key'), bio: __norm(bio),
    closing: __norm(document.getElementById('closing')), closingKatex: document.querySelectorAll('#closing .katex').length}; }"""
READ_BIO = """() => { const b = document.getElementById('bio'), name = b.querySelector('.bio-name .w');
  return {role: b.dataset.role || null, name: name ? [name.textContent, getComputedStyle(name).color] : null,
    fields: Array.from(b.querySelectorAll('.bio-f')).map(f => [__norm(f.querySelector('.bio-k')), __norm(f.querySelector('.bio-v'))]),
    thetas: Array.from(b.querySelectorAll('.bio-v')).map(v => [v.querySelectorAll('.katex').length, /θ/.test(Array.from(v.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join(''))]),
    pressed: Array.from(document.querySelectorAll('#menu .key-row[aria-pressed="true"]')).map(r => r.dataset.role),
    rings: Array.from(document.querySelectorAll('#startSides [data-ring]')).filter(r => getComputedStyle(r).visibility === 'visible').map(r => r.dataset.ring)}; }"""
PANEL_KIDS = ['P', 'DIV#key.key', 'P#closing.closing', 'P', 'DIV.mode-h', 'DIV#stageList.stages']


def judge_bio(got, role, label, fails):
    """The bio for `role`, verbatim; its name in its side colour; θ drawn in KaTeX; that row alone pressed and that strip alone ringed."""
    want = [[k + ':', v] for k, v in BIOS[role]]
    if got['role'] != role or got['fields'] != want or not got['name'] or got['name'][0] != role or got['name'][1] != rgb(COLOURS[role]):
        fails.append('%s: the bio for %s reads %s %s %s, should be %s' % (label, role, got['role'], got['name'], got['fields'], want))
    if any(raw for _, raw in got['thetas']) or [n for n, _ in got['thetas']] != [v.count('θ') for _, v in BIOS[role]]:
        fails.append('%s: θ in the %s bio is not drawn in KaTeX: %s' % (label, role, got['thetas']))
    if got['pressed'] != [role] or got['rings'] != [role]:
        fails.append('%s: %s chosen, but the pressed rows are %s and the ringed strips %s' % (label, role, got['pressed'], got['rings']))


def check_start(page, fails):
    """Contract WHOSE-SIDE-BIOS items 1, 2 and 4: the panel's paragraphs, key, bio area and closing line against the contract's text;
    the stages heading, stage list and scoring line unchanged; each key row a button with its swatch and letter that shows its bio;
    no character line on the start screen (the subtitle exempt, and compared unchanged)."""
    page.evaluate(NORM_JS)
    got = page.evaluate(READ_START)
    if got['sub'] != SUBTITLE:
        fails.append('subtitle %r' % got['sub'])
    if got['kids'] != PANEL_KIDS:
        fails.append('the start panel holds %s, should be %s' % (got['kids'], PANEL_KIDS))
    if got['para'] != [OPENING, CLOSING, SCORING]:
        fails.append('the start panel\'s paragraphs are %s, should be %s' % (got['para'], [OPENING, CLOSING, SCORING]))
    if got['heading'] != STAGES_HEADING or [s[1:] for s in got['stages']] != [list(s) for s in STAGE_LIST] or [s[0] for s in got['stages']] != ['1', '2', '3', '4']:
        fails.append('the Stages heading or the stage list changed: %r %s' % (got['heading'], got['stages']))
    rows = [(r['role'], r['letter'], r['def']) for r in got['rows']]
    if rows != KEY:
        fails.append('the key reads %s, should be %s' % (rows, KEY))
    for r in got['rows']:
        if r['tag'] != 'BUTTON' or r['type'] != 'button' or r['pressed'] != 'false' or not r['swatch'] or r['katex'] != r['def'].count('θ'):
            fails.append('key row %s: %s %s, aria-pressed %s, swatch %s, %d KaTeX θ' % (r['role'], r['tag'], r['type'], r['pressed'], r['swatch'], r['katex']))
    if got['closing'] != CLOSING or got['closingKatex'] != 1:
        fails.append('closing line %r (%d KaTeX)' % (got['closing'], got['closingKatex']))
    if not got['bioInKey'] or got['bio'] != BIO_DEFAULT:
        fails.append('the bio area reads %r (in the key: %s), should be %r' % (got['bio'], got['bioInKey'], BIO_DEFAULT))
    check_no_speech(page, '#menu', 'start screen', fails)
    for role, _, _ in KEY:
        page.click('#menu .key-row[data-role="%s"]' % role)
        judge_bio(page.evaluate(READ_BIO), role, 'start screen, key row %s' % role, fails)
        check_no_speech(page, '#menu', 'start screen, %s chosen' % role, fails)
    page.evaluate('() => window.scrollTo(0, 0)')


# Jon's start-screen illustration and the θ over it (contract WHOSE-SIDE-ART, 6 Nov 2026).
ART = os.path.join(ROOT, 'games', SLUG, 'assets', 'start.webp')
ART_SIZE, ART_MAX_BYTES = (1600, 873), 450 * 1024
ART_SIZES = [(320, 568), (390, 844), (1920, 1080)]
ART_TOL = 0.06               # θ within 6% of the image's width of the tip
FOLD_SIZES = [(320, 568), (375, 667), (390, 844)]
BIG_FOLD_SIZES = [(1366, 768), (1920, 1080)]   # reported too (Amendment 1)
ART_MAX_W = 600              # the picture's cap, centred (Amendment 1, 6 Nov 2026)
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
    want = min(pw, ART_MAX_W)                              # the card's width, capped at 600 px and centred on it
    if abs(iw - want) > 1 or abs(ix - (px + (pw - want) / 2)) > 1 or abs(ih - iw * ART_SIZE[1] / ART_SIZE[0]) > 1.5:
        fails.append('art %s: the picture is %.0f px wide at x %.0f; wanted %.0f, centred on the card (%.0f at x %.0f), height auto' % (
            label, iw, ix, want, pw, px))
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
        combos += [(s, False) for s in FOLD_SIZES + BIG_FOLD_SIZES if s not in sizes] + [(s, True) for s in FOLD_SIZES]
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
        if (w, h) in FOLD_SIZES + BIG_FOLD_SIZES and report:
            print('  start fold %s: first stage ends at %.0f, fold %.0f (%s; reported, not judged)' % (
                label, got['start'], got['fold'], 'above' if got['start'] <= got['fold'] else 'below'))
        ctx.close()


# The ramp's three strips (contract WHOSE-SIDE-BIOS item 3), measured here from the WebP's own pixels: each strip's pixels picked
# out by colour only to tell the three apart (red: R > 190, G < 110, B < 90; green: G > 140, R < 130, B < 110; blue: B - R > 25,
# B - G > 25, R < 140), and a line fitted through each by total least squares. Which strip is which side is then worked out from
# the triangle the three lines make, never from the colours or the page's labels: HYP is the strip that does not pass through the
# right-angled corner, OPP the strip that does not pass through the tip (the corner MEASURE_TIP finds, where θ is), ADJ the other.
MEASURE_STRIPS = """async () => {
  const img = document.querySelector('#startArt img'); await img.decode();
  const W = img.naturalWidth, H = img.naturalHeight, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); g.drawImage(img, 0, 0); const d = g.getImageData(0, 0, W, H).data;
  const cls = {red: (r, gg, b) => r > 190 && gg < 110 && b < 90, green: (r, gg, b) => gg > 140 && r < 130 && b < 110,
               blue: (r, gg, b) => b - r > 25 && b - gg > 25 && r < 140};
  const out = {};
  for (const k in cls) { let n = 0, sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
    for (let y = 0; y < H; y += 2) for (let x = 0; x < W; x += 2) { const i = (y * W + x) * 4;
      if (cls[k](d[i], d[i + 1], d[i + 2])) { n++; sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y; } }
    const mx = sx / n, my = sy / n, a = sxx / n - mx * mx, b = sxy / n - mx * my, cc = syy / n - my * my;
    const ang = 0.5 * Math.atan2(2 * b, a - cc);
    out[k] = {n: n, c: [mx, my], d: [Math.cos(ang), Math.sin(ang)], spread: Math.sqrt(Math.max(0, (a + cc) / 2 - Math.sqrt(((a - cc) / 2) ** 2 + b * b)))}; }
  return out; }"""


def meet_lines(p, q):
    (a, u), (b, v) = p, q
    det = u[0] * -v[1] - u[1] * -v[0]
    t = ((b[0] - a[0]) * -v[1] - (b[1] - a[1]) * -v[0]) / det
    return (a[0] + t * u[0], a[1] + t * u[1])


def strip_roles(strips, tip):
    """{role: (colour, centreline point, direction, corner at one end, corner at the other)} from the three fitted lines, or a problem."""
    lines = {k: (v['c'], v['d']) for k, v in strips.items()}
    ks = sorted(lines)
    corners = {}
    for i in range(3):
        for j in range(i + 1, 3):
            corners[(ks[i], ks[j])] = meet_lines(lines[ks[i]], lines[ks[j]])
    right = [pair for pair in corners if abs(lines[pair[0]][1][0] * lines[pair[1]][1][0] + lines[pair[0]][1][1] * lines[pair[1]][1][1]) < 0.02]
    if len(right) != 1:
        return None, 'no single right-angled corner among %s' % {k: v[1] for k, v in lines.items()}
    near = min(corners, key=lambda pair: math.hypot(corners[pair][0] - tip['x'], corners[pair][1] - tip['y']))
    if near == right[0] or math.hypot(corners[near][0] - tip['x'], corners[near][1] - tip['y']) > 80:
        return None, 'the tip (%.0f, %.0f) is not a corner of the strips\' triangle %s' % (tip['x'], tip['y'], corners)
    hyp = [k for k in ks if k not in right[0]][0]
    opp = [k for k in ks if k not in near][0]
    adj = [k for k in ks if k not in (hyp, opp)][0]
    out = {}
    for role, k in (('HYP', hyp), ('OPP', opp), ('ADJ', adj)):
        ends = [corners[pair] for pair in corners if k in pair]
        out[role] = (k, lines[k][0], lines[k][1], ends[0], ends[1])
    return out, None


def inside(poly, x, y):
    hit, n = False, len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


# The room across a strip at one of its points, from the WebP's pixels: how far the line through it, square to the strip, runs each
# way before it meets another strip's paint or the picture's edge (image px). A tap region can be no deeper than that without
# overlapping another strip; where the room is under 44 px on screen (near the tip, where the strips meet), it is judged against
# the room instead, within ROOM_TOL, and reported.
ROOM_JS = """async ([x, y, nx, ny, own]) => {
  if (!window.__px) { const img = document.querySelector('#startArt img'); await img.decode();
    const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight; const g = c.getContext('2d'); g.drawImage(img, 0, 0);
    window.__px = {W: c.width, H: c.height, d: g.getImageData(0, 0, c.width, c.height).data}; }
  const {W, H, d} = window.__px;
  const cls = (px, py) => { const i = (py * W + px) * 4, r = d[i], gg = d[i + 1], b = d[i + 2];
    return r > 190 && gg < 110 && b < 90 ? 'red' : gg > 140 && r < 130 && b < 110 ? 'green' : b - r > 25 && b - gg > 25 && r < 140 ? 'blue' : null; };
  const run = s => { for (let k = 0; k < 2000; k += 0.5) { const px = Math.round(x + s * nx * k), py = Math.round(y + s * ny * k);
    if (px < 0 || py < 0 || px >= W || py >= H) return k; const c = cls(px, py); if (c && c !== own) return k; } return 2000; };
  return [run(1), run(-1)]; }"""
ROOM_TOL = 1.5
BIO_SIZES = [(320, 568), (390, 844), (1366, 768)]
DEPTH_SIZES = [(320, 568), (390, 844)]
RING_STYLE_JS = """(role) => { const r = document.querySelector('#startSides [data-ring="' + role + '"]'), c = getComputedStyle(r);
  return [c.stroke, c.strokeDasharray, c.strokeLinecap, getComputedStyle(document.body).color]; }"""


def check_bios(browser, base, fails, route=None, sizes=BIO_SIZES, report=True):
    """Item 3 and 4: each strip's side worked out from the picture's geometry; real clicks along each strip show that side's bio,
    press its key row and ring that strip alone in its line style in the text colour; at 320 and 390, from 10% to 90% along each
    strip, its tap region is at least 44 px deep across it, or, where the other strips' paint and the picture's edge leave less
    room (near the tip), as deep as that room within ROOM_TOL; 5% from each corner reported; no two regions overlap; the regions are hidden from assistive tech and out of the
    tab order, while Tab reaches all three key rows and Enter and Space choose them."""
    strips = roles = None
    for w, h in sizes:
        ctx = browser.new_context(viewport={'width': w, 'height': h})
        page = ctx.new_page()
        if route:
            page.route('**/games/%s/**' % SLUG, route)
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex')
        bc.wait_settled(page)
        page.evaluate(NORM_JS)
        label = 'bios %dx%d' % (w, h)
        if roles is None:
            strips, tip = page.evaluate(MEASURE_STRIPS), page.evaluate(MEASURE_TIP)
            if any(v['n'] < 1000 or v['spread'] > 15 for v in strips.values()):
                fails.append('bios: the strips could not be measured from the picture: %s' % strips)
                ctx.close()
                return
            roles, problem = strip_roles(strips, tip)
            if problem:
                fails.append('bios: %s' % problem)
                ctx.close()
                return
            if report:
                print('  bios: strips measured from the WebP: %s' % ', '.join('%s = the %s strip, %s to %s' % (
                    r, v[0], '(%.0f, %.0f)' % v[3], '(%.0f, %.0f)' % v[4]) for r, v in roles.items()))
            polys = page.evaluate("() => Array.from(document.querySelectorAll('#startSides [data-tap]')).map(p => p.getAttribute('points').trim().split(/\\s+/).map(q => q.split(',').map(Number)))")
            over = sum(1 for y in range(1, 873, 4) for x in range(1, 1600, 4) if sum(inside(pl, x + 0.37, y + 0.29) for pl in polys) > 1)
            if over:
                fails.append('bios: the tap regions overlap at %d sampled points of the picture' % over)
        if page.evaluate("() => { const s = document.getElementById('startSides'); return !s || s.getAttribute('aria-hidden') !== 'true' || !!s.querySelector('[tabindex], a, button'); }"):
            fails.append('%s: the ramp\'s tap regions are not hidden from assistive tech and out of the tab order' % label)
        art = page.evaluate("() => { const r = document.querySelector('#startArt img').getBoundingClientRect(); return [r.left, r.top, r.width]; }")
        sc = art[2] / ART_SIZE[0]
        mins, limited, corners = {}, [], []
        for role, (colour, c0, dvec, e0, e1) in roles.items():
            nvec = (-dvec[1], dvec[0])
            for t in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95):
                ix, iy = e0[0] + (e1[0] - e0[0]) * t, e0[1] + (e1[1] - e0[1]) * t
                page.evaluate('() => window.scrollTo(0, 0)')    # a tap on the ramp scrolls its bio into view
                if (w, h) in DEPTH_SIZES:
                    # across the strip through this point: the run of screen pixels that land on the same tap region
                    depth = page.evaluate("""([x, y, nx, ny]) => { const at = (k) => { const e = document.elementFromPoint(x + nx * k, y + ny * k);
                        return e && e.closest('[data-tap]'); }, mid = at(0); if (!mid) return 0; let a = 0, b = 0;
                      while (a < 200 && at(-(a + 0.5)) === mid) a += 0.5; while (b < 200 && at(b + 0.5) === mid) b += 0.5; return a + b; }""",
                                          [art[0] + ix * sc, art[1] + iy * sc, nvec[0], nvec[1]])
                    room = sum(page.evaluate(ROOM_JS, [ix, iy, nvec[0], nvec[1], colour])) * sc
                    need = min(44, room)
                    if t in (0.05, 0.95):       # within 5% of a corner two strips share the room: reported, not judged
                        corners.append('%s %.0f%%: %.1f px' % (role, 100 * t, depth))
                        continue
                    mins[role] = min(mins.get(role, 999), depth)
                    if room < 44:
                        limited.append('%s %.0f%%: %.1f px deep, room %.1f' % (role, 100 * t, depth, room))
                    if depth < need - ROOM_TOL:
                        fails.append('%s: %s\'s tap region is %.1f px deep across the strip %.0f%% along it; %s' % (
                            label, role, depth, 100 * t, 'it should be 44' if need == 44 else 'the strips leave room for %.1f' % room))
                if t in (0.2, 0.5, 0.8):
                    page.mouse.click(art[0] + ix * sc, art[1] + iy * sc)
                    judge_bio(page.evaluate(READ_BIO), role, '%s, the %s strip %.0f%% along' % (label, colour, 100 * t), fails)
            stroke, dash, cap, text = page.evaluate(RING_STYLE_JS, role)
            parts = [float(v.replace('px', '')) for v in dash.replace(',', ' ').split()] if dash != 'none' else []
            style_ok = (not parts) if role == 'HYP' else (len(parts) == 2 and parts[0] >= 6 and parts[1] >= 4) if role == 'OPP' else (
                len(parts) == 2 and parts[0] <= 2 and parts[1] >= 6 and cap == 'round')
            if stroke != text or not style_ok:
                fails.append('%s: the %s ring is %s, dashes %s, caps %s; wanted the text colour %s in %s\'s line style' % (label, role, stroke, dash, cap, text, role))
        if report and mins:
            print('  bios %dx%d: shallowest tap region across each strip, 10-90%% along: %s; under 44 px of room: %s; 5%% from a corner (reported): %s' % (
                w, h, ', '.join('%s %.1f px' % kv for kv in mins.items()), '; '.join(limited) or 'none', ', '.join(corners)))
        check_no_speech(page, '#menu', label, fails)
        # the keyboard: Tab from the top reaches the three key rows in order; Enter and Space choose
        page.evaluate('() => { window.scrollTo(0, 0); document.activeElement && document.activeElement.blur(); }')
        seen = []
        for _ in range(40):
            page.keyboard.press('Tab')
            r = page.evaluate("() => { const a = document.activeElement; return a && a.classList.contains('key-row') ? a.dataset.role : (a && a.closest('#startSides') ? 'ramp' : null); }")
            if r == 'ramp':
                fails.append('%s: Tab lands on the ramp\'s tap regions' % label)
            if r and r != 'ramp' and r not in seen:
                seen.append(r)
                page.keyboard.press('Enter' if len(seen) % 2 else 'Space')
                judge_bio(page.evaluate(READ_BIO), r, '%s, the %s row by keyboard (%s)' % (label, r, 'Enter' if len(seen) % 2 else 'Space'), fails)
            if len(seen) == 3:
                break
        if seen != ['HYP', 'OPP', 'ADJ']:
            fails.append('%s: Tab reaches the key rows %s, should be HYP, OPP, ADJ' % (label, seen))
        ctx.close()


def check_lines(browser, base, fails, route=None, stages=(1, 2, 3, 4)):
    """Item 5 and 6 at speed through the lock hint: rounds of every stage, right and wrong, each panel's verdict, rule and lines
    recomputed from the geometry, and no character line in play or on the results screen."""
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script("(() => { const st = window.setTimeout; window.setTimeout = (f, ms, ...a) => st(f, ms === %d ? 200 : ms, ...a); })();" % HOLD_MS)
    page = ctx.new_page()
    if route:
        page.route('**/games/%s/**' % SLUG, route)
    page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
    page.wait_for_function('() => !!window.WS && !!window.katex')
    stub_board(page)
    for stage in stages:
        for wrong_at in ({0, 2, 4, 5, 6, 8}, {1, 3, 7, 9}):
            if STOP_AT_FIRST and fails:
                break
            page.evaluate('(n) => WS.ui.start(n)', stage)
            for n in range(10):
                label = 'lines stage %d q%d' % (stage, n + 1)
                wait_asking(page)
                it = page.evaluate('() => WS.ui.question()')
                wrong = n in wrong_at
                page.evaluate('(r) => WS.ui.answer(r)', not wrong)
                page.wait_for_function("() => WS.ui.state() === 'right' || WS.ui.state() === 'wrong'", timeout=4000)
                tapped = [s['id'] for s in it['sides'] if s['id'] != it['key']][0] if stage == 1 and wrong else None   # the side WS.ui.answer(false) taps
                check_feedback(page, it, not wrong, label, fails, tapped=tapped)
                check_no_speech(page, '#game', label, fails)
                if wrong:
                    page.click('.maffs-next-wrap button, .fb-next button')
                else:
                    page.wait_for_function("() => WS.ui.state() !== 'right'", timeout=4000)
            page.wait_for_function("() => document.querySelector('#results').classList.contains('active')", timeout=4000)
            check_no_speech(page, '#results', 'lines stage %d results' % stage, fails)
            if page.evaluate('() => { const n = window.__sub.length; window.__sub = []; return n; }') != 1:
                fails.append('lines stage %d: not one board submission' % stage)
            page.wait_for_function('() => !MaffsLock.isFresh()', timeout=4000)
            page.click('#menuBtn')
    ctx.close()


# The figure's content box, worked out here from what is on screen (contract WHOSE-SIDE-FIT, item 4a and Amendment 1): the corners
# (the side lines' ends) padded by 22 px, half the 44 px tap band; each label's box at its drawn centre with the contract's half-size,
# (characters x 5.8 + 2) x g by 11g lit, (characters x 4.6 + 2) x g by 9g otherwise; θ's box as drawn; the right-angle square's
# points. Also each label's, θ's and each tap band's own box against the figure's edge.
FIT_JS = """() => {
  const f = document.getElementById('figure'), svg = f.querySelector('svg'), r = svg.getBoundingClientRect();
  const W = +svg.getAttribute('width'), H = +svg.getAttribute('height'), g = parseFloat(f.style.getPropertyValue('--g')) || 1;
  const bx = [], by = [], add = (x, y, hx, hy) => { bx.push(x - hx, x + hx); by.push(y - hy, y + hy); };
  const cx = [], cy = [], clip = [], inside = (x0, y0, x1, y1) => x0 >= -0.5 && y0 >= -0.5 && x1 <= W + 0.5 && y1 <= H + 0.5;
  svg.querySelectorAll('line.side').forEach(l => { [[+l.getAttribute('x1'), +l.getAttribute('y1')], [+l.getAttribute('x2'), +l.getAttribute('y2')]].forEach(p => {
    cx.push(p[0]); cy.push(p[1]); add(p[0], p[1], 22, 22); }); });
  svg.querySelectorAll('text[data-label]').forEach(t => {
    const lit = /\\b(HYP|OPP|ADJ)\\b/.test(t.getAttribute('class') || ''), n = t.textContent.length;
    add(+t.getAttribute('x'), +t.getAttribute('y'), (n * (lit ? 5.8 : 4.6) + 2) * g, (lit ? 11 : 9) * g);
    const b = t.getBoundingClientRect();
    if (!inside(b.left - r.left, b.top - r.top, b.right - r.left, b.bottom - r.top)) clip.push('label ' + t.textContent);
  });
  const th = f.querySelector('[data-theta]').getBoundingClientRect();
  add((th.left + th.right) / 2 - r.left, (th.top + th.bottom) / 2 - r.top, th.width / 2, th.height / 2);
  if (!inside(th.left - r.left, th.top - r.top, th.right - r.left, th.bottom - r.top)) clip.push('theta');
  const sq = svg.querySelector('[data-square]');
  (sq ? sq.getAttribute('points').trim().split(/\\s+/) : []).forEach(p => { const q = p.split(',').map(Number); add(q[0], q[1], 0, 0); });
  svg.querySelectorAll('.hit').forEach(b => {
    const x1 = +b.getAttribute('x1'), y1 = +b.getAttribute('y1'), x2 = +b.getAttribute('x2'), y2 = +b.getAttribute('y2');
    const L = Math.hypot(x2 - x1, y2 - y1), h = +b.getAttribute('stroke-width') / 2, nx = (y1 - y2) / L * h, ny = (x2 - x1) / L * h;
    const xs = [x1 + nx, x1 - nx, x2 + nx, x2 - nx], ys = [y1 + ny, y1 - ny, y2 + ny, y2 - ny];
    if (!inside(Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys))) clip.push('tap band ' + b.dataset.val);
  });
  return {W: W, H: H, g: g, x0: Math.min(...bx), x1: Math.max(...bx), y0: Math.min(...by), y1: Math.max(...by),
    tw: Math.max(...cx) - Math.min(...cx), th: Math.max(...cy) - Math.min(...cy), clip: clip, id: WS.ui.question().id}; }"""


def judge_fit(m, label, fails, reach=True):
    """Amendment 1: on the drawing's limiting axis the content box reaches the 6g pad at both ends, within 1 px, and the triangle
    fills at least 70% of the figure on that axis; at every size nothing is clipped. Returns the triangle's fill on that axis."""
    pad = 6 * m['g']
    on_x = (m['x1'] - m['x0']) / (m['W'] - 2 * pad) >= (m['y1'] - m['y0']) / (m['H'] - 2 * pad)
    lo, hi, size, tri = (m['x0'], m['x1'], m['W'], m['tw']) if on_x else (m['y0'], m['y1'], m['H'], m['th'])
    ends = (lo - pad, size - pad - hi)
    fill = tri / size
    if reach:
        if max(ends) > 1:
            fails.append('%s %s: %.1f and %.1f px of slack on the limiting axis (%s) inside the %.0f px pad: wasted space'
                         % (label, m['id'], ends[0], ends[1], 'x' if on_x else 'y', pad))
        if min(ends) < -1:
            fails.append('%s %s: the drawing runs %.1f px past the %.0f px pad on the %s axis'
                         % (label, m['id'], -min(ends), pad, 'x' if on_x else 'y'))
        if fill < FIT_FLOOR:
            fails.append('%s %s: the triangle fills %.1f%% of the figure on its limiting axis, under the %d%% floor'
                         % (label, m['id'], 100 * fill, 100 * FIT_FLOOR))
    if m['clip']:
        fails.append('%s %s: clipped by the figure\'s edge: %s' % (label, m['id'], ', '.join(m['clip'])))
    return fill


def seeded_start(page, stage, seed=FIT_SEED):
    page.evaluate(SEED_JS, seed)
    page.evaluate('(n) => WS.ui.start(n)', stage)


def check_fit(browser, base, fails, route=None, sizes=FIT_SIZES, stages=(1, 2, 3, 4), report=True, stop_on=None):
    """Item 4a with Amendment 1: every item of a seeded round of each stage, as asked and as redrawn after an answer (all three
    sides lit), its content box measured from the screen. At 1366x768 and 1920x1080 no wasted space and the floor; at every size
    nothing clipped, and no label on a side or on θ (check_labels). A self-test plant stops at its first finding containing stop_on."""
    def stop():
        return STOP_AT_FIRST and any(stop_on in f for f in fails) if stop_on else STOP_AT_FIRST and fails
    for w, h in sizes:
        big = (w, h) in BIG_SIZES
        ctx = browser.new_context(viewport={'width': w, 'height': h})
        ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
        page = ctx.new_page()
        if route:
            page.route('**/games/%s/**' % SLUG, route)
        page.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
        page.wait_for_function('() => !!window.WS && !!window.katex')
        stub_board(page)
        fills = []
        for stage in stages:
            seeded_start(page, stage)
            for n in range(10):
                wait_asking(page)
                bc.wait_settled(page, 50)
                label = '%dx%d stage %d asking' % (w, h, stage)
                fills.append(judge_fit(page.evaluate(FIT_JS), label, fails, reach=big))
                if big:
                    check_labels(page, label, fails)
                page.evaluate('() => WS.ui.answer(false)')
                page.wait_for_function("() => WS.ui.state() === 'wrong'", timeout=4000)
                bc.wait_settled(page, 50)
                judge_fit(page.evaluate(FIT_JS), '%dx%d stage %d answered' % (w, h, stage), fails, reach=big)
                page.click('.maffs-next-wrap button, .fb-next button')
                if stop():
                    break
            if stop():
                break
            page.wait_for_function("() => document.querySelector('#results').classList.contains('active')", timeout=4000)
        if report and fills:
            fills.sort()
            print('  fit %dx%d: triangle fill on the limiting axis, median %.3f, minimum %.3f (%d items as asked)'
                  % (w, h, fills[len(fills) // 2], fills[0], len(fills)))
        ctx.close()


# Item 4b: the bottom of the question's last line of text (a Range over its text, not #ask's box) against the top of the first
# control below it, and no text in the right-hand column overlapping another element there. KaTeX's hidden MathML is not text on screen.
TEXT_JS = """() => {
  const shown = e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
  const leaves = [...new Set(Array.from(document.querySelectorAll('#ask, #fracline, #opts .opt, #slotTop, #slotBottom, #checkBtn, #feedback .fb-head, #feedback .fb-rule, #feedback .fb-line, .fb-next button, .maffs-next-wrap button')))].filter(shown);
  const textRects = el => { const out = [], tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); let n;
    while ((n = tw.nextNode())) { if (!n.textContent.trim() || n.parentElement.closest('.katex-mathml')) continue;
      const rg = document.createRange(); rg.selectNodeContents(n); for (const x of rg.getClientRects()) if (x.width > 0 && x.height > 0) out.push(x); }
    return out; };
  const name = e => e.id || (e.className && e.className.baseVal === undefined ? e.className.split(' ')[0] : e.tagName);
  const ask = document.getElementById('ask'), res = {askBottom: null, ctlTop: null, ctl: null, overlaps: []};
  if (leaves.includes(ask)) {
    const rs = textRects(ask), at = ask.getBoundingClientRect().top;
    res.askBottom = Math.max(...rs.map(x => x.bottom));
    leaves.filter(e => e !== ask && !ask.contains(e) && e.getBoundingClientRect().top >= at).forEach(e => {
      const t = e.getBoundingClientRect().top; if (res.ctlTop === null || t < res.ctlTop) { res.ctlTop = t; res.ctl = name(e); } });
  }
  leaves.forEach(a => { const rs = textRects(a); leaves.forEach(b => {
    if (a === b || a.contains(b) || b.contains(a)) return;
    const bb = b.getBoundingClientRect();
    if (rs.some(x => x.left < bb.right - 0.5 && x.right > bb.left + 0.5 && x.top < bb.bottom - 0.5 && x.bottom > bb.top + 0.5))
      res.overlaps.push(name(a) + ' text over ' + name(b)); }); });
  return res; }"""


def check_big(browser, base, fails, route=None, sizes=TEXT_SIZES, stages=(1, 2, 3, 4), report=True):
    """Large screens (contract WHOSE-SIDE-PERSONALITY item 8, WHOSE-SIDE-FIT item 4b): for every stage, asking, wrong and right,
    the question's text ends at or above the first control below it and no text in the right-hand column overlaps another element
    there; the question and every answer control on screen with nothing to scroll, Next after a wrong answer and the rule
    in view during the hold; at 1366x768 and 1920x1080 the figure's box at least half the screen's height (its content is
    check_fit's)."""
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
                seeded_start(page, stage)
                wait_asking(page)
                if when != 'asking':
                    page.evaluate('(r) => WS.ui.answer(r)', when == 'right')
                    page.wait_for_function('(s) => WS.ui.state() === s', arg=when, timeout=4000)
                bc.wait_settled(page, 100)
                m = page.evaluate("""() => { const b = e => e.getBoundingClientRect(), svg = document.querySelector('#figure svg');
                  const shown = s => Array.from(document.querySelectorAll(s)).filter(e => e.getClientRects().length);
                  const ctl = shown('#figure .hit, #slotTop, #slotBottom, #checkBtn, #opts .opt, #ask, .maffs-next-wrap button, .fb-next button, #feedback .fb-head, #feedback .fb-rule, #feedback .fb-line');
                  return {svgH: svg ? b(svg).height : 0, bottom: Math.max(...ctl.map(e => b(e).bottom)), top: Math.min(...ctl.map(e => b(e).top)), n: ctl.length,
                    next: shown('.maffs-next-wrap button, .fb-next button').length, rule: shown('#feedback .fb-rule, #feedback .fb-line').length,
                    sh: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth}; }""")
                t = page.evaluate(TEXT_JS)
                label = '%dx%d stage %d %s' % (w, h, stage, when)
                if t['askBottom'] is not None and t['ctlTop'] is not None and t['askBottom'] > t['ctlTop'] + 0.5:
                    fails.append('%s: the question\'s text runs to %.0f, under %s from %.0f' % (label, t['askBottom'], t['ctl'], t['ctlTop']))
                for o in t['overlaps'][:2]:
                    fails.append('%s: %s' % (label, o))
                if report and stage == 4 and when == 'asking':
                    print('  text %dx%d stage 4: the question ends at %s, the buttons start at %s' % (
                        w, h, '%.0f' % t['askBottom'] if t['askBottom'] is not None else '-', '%.0f' % t['ctlTop'] if t['ctlTop'] is not None else '-'))
                if (w, h) in BIG_SIZES and m['svgH'] < 0.5 * h:
                    fails.append('%s: the figure is drawn %.0f px tall, under half the screen (%d)' % (label, m['svgH'], h))
                if m['bottom'] > h - 40 or m['top'] < 0:
                    fails.append('%s: the question or a control is off screen (%.0f to %.0f, fold %d)' % (label, m['top'], m['bottom'], h - 40))
                if m['sh'] > h or m['sw'] > w:
                    fails.append('%s: the page scrolls (%d x %d in %d x %d)' % (label, m['sw'], m['sh'], w, h))
                if when == 'wrong' and not m['next']:
                    fails.append('%s: no Next' % label)
                if when == 'right' and not m['rule']:
                    fails.append('%s: no rule in view on a right answer' % label)
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
    # contract WHOSE-SIDE-PERSONALITY's subtitle, kept (WHOSE-SIDE-BIOS: Jon has not decided on it); its other lines are retired with them
    ('the subtitle reworded', "The other two can't stop being polite about it.", "The other two are polite about it."),
    # the large screen
    ('a small triangle at 1920x1080', "var H = Math.max(240, Math.floor(window.innerHeight - below - top - pad));", "var H = 400;", 'big'),
    # contract WHOSE-SIDE-FIT (Amendment 1): each must be caught by the check named in its last field, not by another
    ('the old margin restored (mx = 2*hw + 10g)',
     "    var k = fitScale(), c = extent(place(k, 0, 0)), ox = W / 2 - (c.x0 + c.x1) / 2, oy = H / 2 - (c.y0 + c.y1) / 2;\n",
     "    var mx = 30 * g, my = 30 * g;\n    Object.keys(texts).forEach(function (id) { mx = Math.max(mx, 2 * texts[id].hw + 10 * g); my = Math.max(my, 2 * texts[id].hh + 10 * g); });\n"
     "    var k = Math.min((W - 2 * mx) / bw, (H - 2 * my) / bh), ox = (W - bw * k) / 2, oy = (H - bh * k) / 2;\n", 'fit', 'wasted space'),
    ('the triangle centred, not the drawing, a label pushed off the edge',
     "ox = W / 2 - (c.x0 + c.x1) / 2, oy = H / 2 - (c.y0 + c.y1) / 2;", "ox = (W - bw * k) / 2, oy = (H - bh * k) / 2;", 'fit', 'clipped'),
    ('the grid rows reverted to 1fr auto auto auto auto 1fr',
     "grid-template-rows:minmax(0,1fr) auto auto auto auto minmax(0,1fr);", "grid-template-rows:1fr auto auto auto auto 1fr;", 'text', "question's text runs"),
    # contract WHOSE-SIDE-ART: θ over the ramp's tip
    ('θ at the square corner', "left:77.49%;top:81.50%;", "left:14.5%;top:81.5%;", 'art'),
    ('θ off the tip, on the concrete', "left:77.49%;top:81.50%;", "left:91%;top:80%;", 'art'),
    ('θ slid up the slope, 7.5% from the tip', "left:77.49%;top:81.50%;", "left:76.2%;top:77.6%;", 'art'),
    ('the arc centred off the tip', 'd="M 1155.2 733 A 170 170 0 0 1 1175.6 652.3"', 'd="M 1055.2 733 A 170 170 0 0 1 1075.6 652.3"', 'art'),
    ('θ in plain text, not KaTeX', "    $('startTheta').innerHTML = THETA();", "", 'art'),
    ('the picture uncapped on a large screen', "max-width:600px;margin-left:auto;margin-right:auto;", "", 'art'),
    # contract WHOSE-SIDE-BIOS: the start screen's text, the ramp's strips and the rule in the panel
    ('the key\'s ADJ definition reverted to "next to θ."', 'ADJ</span>, next to <span class="th">θ</span>, and not the hypotenuse.</span>', 'ADJ</span>, next to <span class="th">θ</span>.</span>', 'start'),
    ("OPP's and ADJ's bios swapped", [('    OPP: [[\'Location\', "The only side', '    ADJ: [[\'Location\', "The only side'),
                                      ('    ADJ: [[\'Location\', "Right next', '    OPP: [[\'Location\', "Right next')], None, 'start'),
    ('the old closing line restored', 'Put <span class="th">θ</span> in the other corner and <span class="w OPP">OPP</span> and <span class="w ADJ">ADJ</span> swap. <span class="w HYP">HYP</span> stays put.',
     'Move <span class="th">θ</span>, and the polite two swap. <span class="w HYP">HYP</span> doesn\'t flinch.', 'start'),
    ('the scoring line removed', '      <p>Ten quick questions a stage. No lives: a faster right answer scores more, a slow one is still right.</p>\n', '', 'start'),
    ('a strip mapped to the wrong role', [('data-tap="HYP"', 'data-tap="X"'), ('data-tap="ADJ"', 'data-tap="HYP"'), ('data-tap="X"', 'data-tap="ADJ"')], None, 'bios'),
    ('a character line left in the right-answer panel', "fb.innerHTML = '<div class=\"fb done\">' + head(true) + rule + '</div>';",
     "fb.innerHTML = '<div class=\"fb done\">' + head(true) + rule + '<div class=\"fb-line\">OPP: “Spot on. Do carry on.”</div></div>';", 'lines'),
    ('the rule missing on a right answer', "fb.innerHTML = '<div class=\"fb done\">' + head(true) + rule + '</div>';", "fb.innerHTML = '<div class=\"fb done\">' + head(true) + '</div>';", 'lines'),
    ('numerator and denominator swapped', "fracWords(FN[fn][0], FN[fn][1])", "fracWords(FN[fn][1], FN[fn][0])", 'lines'),
    ('the equation shown as a sentence again', "'<div class=\"fb-rule\">' + tex('\\\\' + fn + '\\\\theta=' + fracWords(FN[fn][0], FN[fn][1])) + '</div>'",
     "'<div class=\"fb-rule\">' + rich(fn + ' θ is ' + FN[fn][0] + ' over ' + FN[fn][1] + '.') + '</div>'", 'lines'),
    ('the misconception line dropped from a wrong tap', "[RULE1[Q.ask], LINE[whyTap(Q, val)]]", "[RULE1[Q.ask]]", 'lines'),
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
            if len(plant) > 3 and plant[3] == 'start':     # the start screen's text, read as run_engine reads it
                ctx = browser.new_context(viewport={'width': SIZES[0][0], 'height': SIZES[0][1]})
                pg = ctx.new_page()
                pg.route('**/games/%s/**' % SLUG, route(None))
                pg.goto('%s/games/%s/?cb=%d' % (base, SLUG, random.randrange(10 ** 9)))
                pg.wait_for_function('() => !!window.WS && !!window.katex')
                check_start(pg, found)
                ctx.close()
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            if len(plant) > 3 and plant[3] == 'art':
                check_art(browser, base, found, route=route(None), report=False)
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            if len(plant) > 3 and plant[3] == 'bios':
                check_bios(browser, base, found, route=route(None), sizes=BIO_SIZES[:1], report=False)
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            if len(plant) > 3 and plant[3] in ('lines', 'big'):
                (check_lines(browser, base, found, route=route(None)) if plant[3] == 'lines'
                 else check_big(browser, base, found, route=route(None), sizes=[(1920, 1080)], stages=(1,), report=False))
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(found), found[0][:110])) if found else print('  NOT CAUGHT: %s' % name)
                return 0 if found else 1
            if len(plant) > 3 and plant[3] in ('fit', 'text'):     # caught only by the finding its fifth field names
                (check_fit(browser, base, found, route=route(None), sizes=[(1920, 1080)], stages=(3,), report=False, stop_on=plant[4]) if plant[3] == 'fit'
                 else check_big(browser, base, found, route=route(None), sizes=[(1920, 1080)], stages=(4,), report=False))
                mine = [f for f in found if plant[4] in f]
                print('  planted, caught: %s (%d findings; first: %s)' % (name, len(mine), mine[0][:110])) if mine else print(
                    '  NOT CAUGHT: %s (no "%s" finding; %d others%s)' % (name, plant[4], len(found), (': ' + found[0][:90]) if found else ''))
                return 0 if mine else 1
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
    units = ['engine'] + ['play %dx%d' % s for s in SIZES] + ['slow', 'aa', 'hold', 'lines', 'bios', 'big', 'art'] + ['fit %dx%d' % s for s in FIT_SIZES]
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
                     ('hold', lambda: check_hold(browser, base, fails)), ('lines', lambda: check_lines(browser, base, fails)),
                     ('bios', lambda: check_bios(browser, base, fails)),
                     ('big', lambda: check_big(browser, base, fails)), ('art', lambda: check_art(browser, base, fails))]
            work += [('fit %dx%d' % s, lambda s=s: check_fit(browser, base, fails, sizes=[s])) for s in FIT_SIZES]
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
