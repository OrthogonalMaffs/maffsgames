#!/usr/bin/env python3
# ci-shards: 3-gon Line-up (the 48-item bank held to the contract's SHA-256 and counts, the generator's file to its own; every line-up's congruent pair, every SSA decoy's two triangles, every drawing's marks, every stage 3 rule and every witness worked out again with this script's own triangle solver, never the generator; every label one per fact, clear of every edge, mark and other label, on its own side and inside or outside its triangle as it should be; LINES exactly the contract's fourteen, every one used; every stage played to the end, the score, one game_completed and one submission; every working line the contract's; every rendered label's ink box inside its bank box at four sizes (Amendment 1); every item's every answer, right or wrong, showing its own line(s), the answer lit, the working and Next above the fold at 375x667, 390x844, 1280x720 and 1366x768, normal and Aa; fault-injection self-test) | | 4
# ci-deps: games/3-gon-line-up/ tools/3-gon-line-up/
r"""Independent verification for 3-gon Line-up (games/3-gon-line-up/), contract 3-GON-LINE-UP-BUILD (28 Nov 2026).
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 48 items, the output of tools/3-gon-line-up/bank.py embedded one item a line. This script
never runs or imports that generator (it reads the file only to hold it to the contract's SHA-256). It reads the bank
from the page and works everything out again with its own code:

  Bank     the item lines hash to the contract's SHA-256; 12 items in each of the four stages, ids unique, suspects
           numbered 1 to 6 in order.
  Stage 1  in each line-up exactly one pair has equal sorted squared side lengths (whole numbers, exactly), and it is
           "pair"; the twin is the culprit under twin_op, then moved so its lowest corner is on 0 (twin_move says
           reflection for the four reflections); at least 5 reflected twins; s1-01's pair is 2 and 6; every corner on the
           0..8 grid; no flat triangle.
  Stages   each suspect's marks classified (SSS, SAS, ASA, AAS, RHS, or SSA and AAA, which prove nothing) and solved for
  2 and 4  its three sides by this script's own law of cosines and sines; exactly one pair is proven congruent (both a
           full criterion, solved sides equal) and it is "pair"; every SSA suspect fits two different triangles; every
           suspect's drawing, but the twin's and drawn_alike's, matches its marks (angles to 0.15 degrees, sides in
           proportion to 1%). The criterion recorded on the item and each suspect is the one worked out here.
  Stage 3  "answer" is the rule the marks satisfy (AAS answers ASA; AAA and SSA answer NOT_ENOUGH), "shown" is that
           classification (SAS_right: SAS with the right angle between the sides); A's drawing matches the marks; for SSA,
           A and B are the two different triangles the marks fit.
  Stage 4  witness_says is the pair when witness_right, else the culprit and the suspect witness_fooled_by names; "rule"
           is SSS, SAS, ASA or RHS and the culprit's criterion (AAS gives ASA).
  Labels   on every drawing: one per fact, the text "<n> cm" or "<n>°", a right angle only ever a "right" mark at its own
           corner; each box centred on its point, inside the view, clear of every edge by 0.12, a side's box outside the
           triangle and an angle's inside, clear of every other box by 0.12, clear of every arc (radius 0.4) and
           right-angle square (0.45 x sqrt 2) by 0.12, nearer its own corner or side than any other by 0.3, and an angle's
           within 55% of the shorter side at its corner.
  Lines    LINES in the page is exactly the contract's fourteen lines, word for word; every one is used by some answer
           this bank allows, none unused.
  Working  for every item the page's working line is the contract's, worked out here from the item.
  Labels   in Chromium, on every drawing of every item at 375x667, 390x844, 1280x720 and 1366x768: each triangle drawn at the
  drawn    bank's corners (y turned down), each label's text at its point in Outfit 600 at its size, anchored middle and
           central, and each rendered label's INK box (Amendment 1: the browser's own text measurement, never getBBox)
           inside its bank box turned into the drawing's coordinates; every arc of radius 0.4 and square of side 0.45 at
           its corner.
  Play     at 375x667 every stage played to the end: eight different items of that stage, Stage 1 opening with s1-01;
           right and wrong answers in turn; the score is the right answers, one game_completed, one submission on the
           run's board, and no events but game_started, question_answered (with the item's id) and game_completed.
  Fit      at the four sizes, normal and Aa: for every item, the right answer and every wrong choice (every wrong pair, every
           wrong button, both witness steps): the feedback, Next included, ends above the fold (the viewport less the 40 px
           footer, in page coordinates) and the page does not scroll sideways. At 375x667 normal, each screen is also
           read: exactly the expected LINES line(s) in order, the working, the true answer lit (the pair, or the button),
           Next.

Work units: "bank" (no browser), "working 375x667", "labels <W>x<H>" (four), "play 375x667", "fit <W>x<H> <normal|Aa>"
(eight) and "plant: <what>" (one per planted fault).

    python scripts/verify-3-gon-line-up.py              # every unit, then the self-test
    python scripts/verify-3-gon-line-up.py --selftest   # the planted faults only
"""
import argparse
import contextlib
import hashlib
import itertools
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = '3-gon-line-up'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
GENERATOR = os.path.join(ROOT, 'tools', SLUG, 'bank.py')
SHA256 = 'a69d0470842df22d3dab23dc0642679010d8b8f8574d7c5674d042b52bea3aa7'       # the bank's lines (contract step 2)
GEN_SHA256 = 'ea863565c7724dac54a839afd8e1116e160822d35ccd7a798cd1e66fd15b4d55'   # the generator's file (contract step 2)
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4']
PER = 8
FOOTER = 40
SIZES = [(375, 667), (390, 844), (1280, 720), (1366, 768)]
EVENTS = {'game_started', 'question_answered', 'game_completed'}
GAP, ARC, SQUARE, NEAR, ANGLE_REACH = 0.12, 0.4, 0.45, 0.3, 0.55
SLACK = 2e-3          # the bank rounds every coordinate to 3 decimal places
VIEW = (-2.0, -2.0, 8.0, 8.0)
FULL = {'SSS', 'SAS', 'ASA', 'AAS', 'RHS'}
RULES = ['SSS', 'SAS', 'ASA', 'RHS']

# Contract step 3i, word for word.
LINES_WANT = {
    'enlarged': "Same shape, different size. That's an enlargement: similar, not congruent.",
    'one_square_out': "Close, but one corner is a square out. Count the squares along each side.",
    'stranger': "That's a different triangle altogether.",
    'reflection_missed': "Flipped still counts: a reflection is congruent.",
    'one_differs': "One of the marks is different, so they can't be the same triangle.",
    'drawn_alike': "It looks identical, but a number is different. The picture lied; the numbers don't.",
    'angles_only': "Matching angles prove the shape, not the size. It could be an enlargement.",
    'angle_moved': "Same numbers, but the angle isn't between the same two sides. That doesn't prove it.",
    'angle_not_between': "SAS needs the angle between the two sides. This one isn't.",
    'no_hypotenuse': "RHS needs the hypotenuse, the side opposite the right angle. It isn't marked.",
    'not_enough_wrong': "There is enough: these marks match a rule.",
    'wrong_rule': "Not that rule. Check which sides and angles are marked, and where.",
    'witness_believed': "The witness was fooled.",
    'witness_doubted': "The witness was right this time.",
}


# ---------------------------------------------------------------- the page's bank and lines, read from its source
def bank_lines(html):
    """The raw item lines of the page's BANK, each as the generator wrote it (the joining comma removed)."""
    m = re.search(r'\n  var BANK = \[\n(.*?)\n  \];', html, re.S)
    if not m:
        raise ValueError('no BANK block in the page')
    return [ln[:-1] if ln.endswith(',') else ln for ln in m.group(1).split('\n')]


def lines_of(html):
    """The page's LINES object: {key: line}."""
    m = re.search(r'\n  var LINES = \{\n(.*?)\n  \};', html, re.S)
    if not m:
        raise ValueError('no LINES object in the page')
    out = {}
    for ln in m.group(1).split('\n'):
        k = re.match(r'^\s+([a-z0-9_]+): (".*"),?$', ln)
        if not k:
            raise ValueError('a LINES line this script cannot read: %r' % ln[:60])
        if k.group(1) in out:
            raise ValueError('LINES has %s twice' % k.group(1))
        out[k.group(1)] = json.loads(k.group(2))
    return out


# ---------------------------------------------------------------- geometry, this script's own
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angle_at(P, v):
    o = [P[j] for j in range(3) if j != v]
    a = (o[0][0] - P[v][0], o[0][1] - P[v][1])
    b = (o[1][0] - P[v][0], o[1][1] - P[v][1])
    c = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def pt_seg(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    L = vx * vx + vy * vy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L))
    return math.hypot(p[0] - a[0] - t * vx, p[1] - a[1] - t * vy)


def pt_box(p, b):
    dx = max(b[0] - p[0], 0.0, p[0] - b[2])
    dy = max(b[1] - p[1], 0.0, p[1] - b[3])
    return math.hypot(dx, dy)


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def segs_cross(p, q, r, s):
    d1, d2, d3, d4 = _cross(r, s, p), _cross(r, s, q), _cross(p, q, r), _cross(p, q, s)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def seg_box(a, b, box):
    """The exact distance from segment ab to the rectangle box (0 if they meet)."""
    x0, y0, x1, y1 = box
    if pt_box(a, box) == 0 or pt_box(b, box) == 0:
        return 0.0
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        if segs_cross(a, b, corners[i], corners[(i + 1) % 4]):
            return 0.0
    return min([pt_box(a, box), pt_box(b, box)] + [pt_seg(c, a, b) for c in corners])


def inside(p, P):
    s = [_cross(P[i], P[(i + 1) % 3], p) for i in range(3)]
    return all(x > 0 for x in s) or all(x < 0 for x in s)


def corners_of(b):
    return [(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]


def boxes_apart(a, b, gap):
    return a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1]


# ---------------------------------------------------------------- triangles from their marks, this script's own
def parts(facts):
    sides = {frozenset((f[1], f[2])): f[3] for f in facts if f[0] == 'side'}
    angs = {f[1]: f[2] for f in facts if f[0] == 'angle'}
    return sides, angs


def opposite(v):
    return frozenset({0, 1, 2} - {v})


def classify(facts):
    sides, angs = parts(facts)
    if len(sides) == 3 and not angs:
        return 'SSS'
    if len(angs) == 3 and not sides:
        return 'AAA'
    if len(sides) == 2 and len(angs) == 1:
        (v, a), = angs.items()
        if all(v in e for e in sides):
            return 'SAS'
        if a == 90 and opposite(v) in sides:
            return 'RHS'
        return 'SSA'
    if len(sides) == 1 and len(angs) == 2:
        (e,) = sides
        return 'ASA' if set(angs) == set(e) else 'AAS'
    return '?'


def rule_of(kind):
    return 'ASA' if kind == 'AAS' else kind if kind in FULL else 'NOT_ENOUGH'


def sides_by_vertex(facts):
    """{vertex: the side opposite it} for a full criterion, by the law of cosines and the law of sines."""
    sides, angs = parts(facts)
    kind = classify(facts)
    if kind == 'SSS':
        return {v: sides[opposite(v)] for v in range(3)}
    if kind == 'SAS':
        (v, a), = angs.items()
        p, q = [sides[e] for e in sides]
        return {w: (math.sqrt(p * p + q * q - 2 * p * q * math.cos(math.radians(a))) if w == v else sides[opposite(w)]) for w in range(3)}
    if kind == 'RHS':
        (v, _), = angs.items()
        h = sides[opposite(v)]
        leg = [x for e, x in sides.items() if e != opposite(v)][0]
        out = {v: h}
        for w in range(3):
            if w != v:
                out[w] = sides[opposite(w)] if opposite(w) in sides else math.sqrt(h * h - leg * leg)
        return out
    if kind in ('ASA', 'AAS'):
        A = dict(angs)
        A[({0, 1, 2} - set(A)).pop()] = 180 - sum(angs.values())
        (e, known), = sides.items()
        k = known / math.sin(math.radians(A[({0, 1, 2} - set(e)).pop()]))
        return {v: k * math.sin(math.radians(A[v])) for v in range(3)}
    return None


def solved(facts):
    s = sides_by_vertex(facts)
    return None if s is None else sorted(s.values())


def ssa_thirds(facts):
    """The third side of every triangle two sides and a non-included angle fit (0, 1 or 2 of them)."""
    sides, angs = parts(facts)
    (v, a), = angs.items()
    opp = sides.get(opposite(v))
    adj = [x for e, x in sides.items() if v in e]
    if opp is None or len(adj) != 1:
        return []
    b, A = adj[0], math.radians(a)
    disc = opp * opp - (b * math.sin(A)) ** 2
    if disc < -1e-12:
        return []
    r = math.sqrt(max(disc, 0.0))
    out = [c for c in {round(b * math.cos(A) + r, 9), round(b * math.cos(A) - r, 9)} if c > 1e-9]
    return sorted(out)


def drawing_matches(P, facts):
    """'' if the drawn triangle P has the marked angles (to 0.15 degrees) and its marked sides in proportion (to 1%)."""
    for f in facts:
        if f[0] == 'angle' and abs(angle_at(P, f[1]) - f[2]) > 0.15:
            return 'the angle at corner %d is drawn %.2f degrees, marked %d' % (f[1], angle_at(P, f[1]), f[2])
    ratios = [dist(P[f[1]], P[f[2]]) / f[3] for f in facts if f[0] == 'side']
    if ratios and max(ratios) / min(ratios) - 1 > 0.01:
        return 'its marked sides are drawn out of proportion (%.4f to %.4f a cm)' % (min(ratios), max(ratios))
    return ''


# ---------------------------------------------------------------- what the page should say (contract 3h and 3i)
SHARE = {'SSS': 'all three sides', 'SAS': 'two sides and the angle between them', 'ASA': 'two angles and the side between them',
         'RHS': 'a right angle, the hypotenuse and one other side'}


def role_n(q, role):
    return next(s['n'] for s in q['suspects'] if s['role'] == role)


def third_angle(facts):
    return 180 - sum(f[2] for f in facts if f[0] == 'angle')


def want_working(q):
    if q['stage'] == 1:
        C, T = role_n(q, 'culprit'), role_n(q, 'twin')
        if q['twin_move'] == 'reflection':
            return 'Flip number %d over and it fits exactly on number %d. A reflection is still congruent.' % (C, T)
        turn = {'rot90': 'a quarter turn anticlockwise', 'rot270': 'a quarter turn clockwise', 'rot180': 'a half turn'}[q['twin_op']]
        return 'Turn number %d %s and it fits exactly on number %d.' % (C, turn, T)
    if q['stage'] == 3:
        k = q['shown']
        if k == 'SAS_right':
            return 'two sides and the angle between them: a right angle between two sides is SAS, not RHS'
        if k == 'AAS':
            return ("Find the third angle first: angles in a triangle add up to 180°, so it's %d°. Now the side is between two "
                    "known angles: ASA." % third_angle(q['facts']))
        if k == 'AAA':
            return 'Same angles fix the shape, not the size: one could be an enlargement of the other. Not enough evidence.'
        if k == 'SSA':
            return "The angle isn't between the two sides, so the same marks fit two different triangles. Look at A and B: not enough evidence."
        return SHARE[k]
    return s2_line(q)


def s2_line(q):
    C, T = role_n(q, 'culprit'), role_n(q, 'twin')
    cul = next(s for s in q['suspects'] if s['role'] == 'culprit')
    if q['criterion'] == 'AAS':
        R = 'two angles and a side; the third angle is %d°, so the side is between two known angles: ASA' % third_angle(cul['facts'])
    else:
        R = SHARE[q['criterion']]
    return '%d and %d share %s. That proves it, whatever the pictures look like.' % (C, T, R)


def pair_keys(q, said):
    """The LINES keys for accusing the pair `said` (sorted), in order: each wrongly accused suspect's role, once, by
    number; in Stage 1, reflection_missed when the reflected twin was left out."""
    keys = []
    for n in said:
        if n in q['pair']:
            continue
        role = next(s['role'] for s in q['suspects'] if s['n'] == n)
        if role not in keys:
            keys.append(role)
    if q['stage'] == 1 and q['twin_move'] == 'reflection' and role_n(q, 'twin') not in said:
        keys.append('reflection_missed')
    return keys


def rule_key(q, val):
    if val == 'NOT_ENOUGH':
        return 'not_enough_wrong'
    if q['answer'] == 'NOT_ENOUGH':
        return 'angles_only' if q['shown'] == 'AAA' else 'angle_not_between'
    if val == 'RHS' and q['shown'] == 'SAS_right':
        return 'no_hypotenuse'
    if val == 'SAS' and q['shown'] == 'RHS':
        return 'angle_not_between'
    return 'wrong_rule'


def scenarios(q):
    """Every way to answer item q: (steps, right, keys, work, lit). steps are the presses ('pick n', 'accuse', 'rule v',
    'judge v'); lit is what must be marked right on the board ('pair' or a button's value)."""
    out = []
    pairs = [list(p) for p in itertools.combinations(range(1, 7), 2)]

    def accuse(p, pre=()):
        return list(pre) + ['pick %d' % p[0], 'pick %d' % p[1], 'accuse']
    if q['stage'] in (1, 2):
        for p in pairs:
            right = p == q['pair']
            out.append((accuse(p), right, [] if right else pair_keys(q, p), [want_working(q)], 'pair'))
    elif q['stage'] == 3:
        for v in RULES + ['NOT_ENOUGH']:
            right = v == q['answer']
            out.append((['rule ' + v], right, [] if right else [rule_key(q, v)], [want_working(q)], q['answer']))
    else:
        w = s2_line(q)
        if q['witness_right']:
            out.append((['judge wrong'], False, ['witness_doubted'], [w], 'pair'))
            for v in RULES:
                right = v == q['rule']
                out.append((['judge right', 'rule ' + v], right, [] if right else ['wrong_rule'], [w], q['rule']))
        else:
            F = role_n(q, q['witness_fooled_by'])
            out.append((['judge right'], False, ['witness_believed'],
                        ['The witness was fooled by number %d.' % F, LINES_WANT[q['witness_fooled_by']], w], 'pair'))
            for p in pairs:
                right = p == q['pair']
                out.append((accuse(p, ['judge wrong']), right, [] if right else pair_keys(q, p), [w], 'pair'))
    return out


# ---------------------------------------------------------------- the bank
def label_faults(P, facts, labels):
    """Every way the labels on one drawing break the contract's rules (5a, Labels)."""
    bad = []
    texted = [l for l in labels if l['type'] != 'right']
    rights = [l for l in labels if l['type'] == 'right']
    if len(labels) != len(facts):
        bad.append('%d labels for %d facts' % (len(labels), len(facts)))
    for f in facts:
        if f[0] == 'angle' and f[2] == 90:
            if sum(1 for l in rights if l['vertex'] == f[1]) != 1:
                bad.append('the right angle at corner %d is not drawn as one "right" mark' % f[1])
        elif sum(1 for l in texted if list(l['fact']) == list(f)) != 1:
            bad.append('the fact %s has not exactly one label' % (f,))
    for l in rights:
        if not any(f[0] == 'angle' and f[2] == 90 and f[1] == l['vertex'] for f in facts):
            bad.append('a right-angle mark at corner %d, which is not marked 90' % l['vertex'])
    edges = [(P[0], P[1]), (P[1], P[2]), (P[2], P[0])]
    marks = [(P[f[1]], SQUARE * math.sqrt(2) if f[2] == 90 else ARC) for f in facts if f[0] == 'angle']
    for l in texted:
        f, b, t = l['fact'], l['box'], l['text']
        want = ('%d cm' % f[3]) if f[0] == 'side' else ('%d°' % f[2])
        if t != want or l['type'] != f[0]:
            bad.append('label %r for %s should read %r' % (t, f, want))
        if f[0] == 'angle' and f[2] == 90:
            bad.append('a right angle written as text (%r)' % t)
        c = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        if dist(c, (l['x'], l['y'])) > SLACK:
            bad.append('label %s: its box is not centred on its point' % t)
        if b[0] < VIEW[0] - SLACK or b[1] < VIEW[1] - SLACK or b[2] > VIEW[2] + SLACK or b[3] > VIEW[3] + SLACK:
            bad.append('label %s leaves the view' % t)
        near = min(seg_box(p, q, b) for p, q in edges)
        if near < GAP - SLACK:
            bad.append('label %s is %.3f from an edge (it must clear every edge by %g)' % (t, near, GAP))
        inn = [inside(k, P) for k in corners_of(b)]
        if f[0] == 'side' and (any(inn) or inside(c, P)):
            bad.append('side label %s is inside the triangle' % t)
        if f[0] == 'angle' and not all(inn):
            bad.append('angle label %s is not inside its triangle' % t)
        for v, reach in marks:
            if pt_box(v, b) < reach + GAP - SLACK:
                bad.append('label %s is %.3f from the arc or square at corner (%g, %g), needs %.3f' % (t, pt_box(v, b) - reach, v[0], v[1], GAP))
        if f[0] == 'angle':
            v = f[1]
            dv = dist(c, P[v])
            others = [dist(c, P[j]) for j in range(3) if j != v]
            if not dv < min(others) - NEAR:
                bad.append('angle label %s is not nearer its own corner than another by %g (%.3f against %.3f)' % (t, NEAR, dv, min(others)))
            short = min(dist(P[v], P[j]) for j in range(3) if j != v)
            if dv > ANGLE_REACH * short + SLACK:
                bad.append('angle label %s is %.3f from its corner, beyond 55%% of the shorter side there (%.3f)' % (t, dv, ANGLE_REACH * short))
        else:
            own = pt_seg(c, P[f[1]], P[f[2]])
            rest = [pt_seg(c, P[i], P[j]) for i, j in ((0, 1), (1, 2), (0, 2)) if {i, j} != {f[1], f[2]}]
            if not own < min(rest) - NEAR:
                bad.append('side label %s is not nearer its own side than another by %g' % (t, NEAR))
    for a, b in itertools.combinations(texted, 2):
        if not boxes_apart(a['box'], b['box'], GAP - SLACK):
            bad.append('labels %s and %s are closer than %g' % (a['text'], b['text'], GAP))
    return bad


def check_bank(html, out, info):
    lines = bank_lines(html)
    blob = ''.join(ln + '\n' for ln in lines)
    got = hashlib.sha256(blob.encode('utf-8')).hexdigest()
    if got != SHA256:
        out.append('bank: the item lines hash to %s, not the contract\'s %s' % (got, SHA256))
    gen = hashlib.sha256(open(GENERATOR, 'rb').read()).hexdigest()
    if gen != GEN_SHA256:
        out.append('bank: tools/%s/bank.py hashes to %s, not the contract\'s %s' % (SLUG, gen, GEN_SHA256))
    items = [json.loads(ln) for ln in lines]
    by = {s: [q for q in items if q['stage'] == s] for s in (1, 2, 3, 4)}
    for s, qs in by.items():
        if len(qs) != 12:
            out.append('bank: stage %d has %d items, not 12' % (s, len(qs)))
    ids = [q['id'] for q in items]
    if len(set(ids)) != len(ids):
        out.append('bank: ids repeat')
    for q in by[1] + by[2] + by[4]:
        if [s['n'] for s in q['suspects']] != [1, 2, 3, 4, 5, 6]:
            out.append('%s: suspects are not numbered 1 to 6 in order' % q['id'])
        if sorted(q['pair']) != q['pair'] or len(q['pair']) != 2:
            out.append('%s: pair %s is not two numbers in order' % (q['id'], q['pair']))

    # Stage 1: squared paper, exact whole numbers.
    ops = {'rot90': (0, -1, 1, 0), 'rot180': (-1, 0, 0, -1), 'rot270': (0, 1, -1, 0), 'refl_x': (1, 0, 0, -1),
           'refl_y': (-1, 0, 0, 1), 'refl_diag': (0, 1, 1, 0), 'refl_anti': (0, -1, -1, 0)}

    def sq(P):
        return sorted((P[i][0] - P[j][0]) ** 2 + (P[i][1] - P[j][1]) ** 2 for i, j in ((0, 1), (1, 2), (0, 2)))
    reflected = 0
    for q in by[1]:
        S = q['suspects']
        found = [[a['n'], b['n']] for a, b in itertools.combinations(S, 2) if sq(a['pts']) == sq(b['pts'])]
        if found != [q['pair']]:
            out.append('%s: congruent pairs %s, the bank says %s' % (q['id'], found, q['pair']))
        if sorted([role_n(q, 'culprit'), role_n(q, 'twin')]) != q['pair']:
            out.append('%s: pair %s is not the culprit and the twin' % (q['id'], q['pair']))
        for s in S:
            if any(not (isinstance(c, int) and 0 <= c <= 8) for p in s['pts'] for c in p):
                out.append('%s: suspect %d has a corner off the 0..8 grid' % (q['id'], s['n']))
            (x1, y1), (x2, y2), (x3, y3) = s['pts']
            if (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1) == 0:
                out.append('%s: suspect %d is flat' % (q['id'], s['n']))
        op = q['twin_op']
        if op not in ops:
            out.append('%s: twin_op %r' % (q['id'], op))
            continue
        a, b, c, d = ops[op]
        cul = next(s for s in S if s['role'] == 'culprit')['pts']
        t = [(a * x + b * y, c * x + d * y) for x, y in cul]
        mx, my = min(p[0] for p in t), min(p[1] for p in t)
        t = sorted([[x - mx, y - my] for x, y in t])
        if t != sorted(next(s for s in S if s['role'] == 'twin')['pts']):
            out.append('%s: the twin is not the culprit under %s, then moved' % (q['id'], op))
        if (q['twin_move'] == 'reflection') != op.startswith('refl'):
            out.append('%s: twin_move %s for %s' % (q['id'], q['twin_move'], op))
        reflected += q['twin_move'] == 'reflection'
    if reflected < 5:
        out.append('stage 1: %d reflected twins, fewer than 5' % reflected)
    if by[1] and by[1][0]['id'] == 's1-01' and by[1][0]['pair'] != [2, 6]:
        out.append('s1-01: pair %s, not 2 and 6 (the witness\'s own line-up)' % by[1][0]['pair'])
    if not any(q['id'] == 's1-01' for q in by[1]):
        out.append('stage 1 has no s1-01')

    # Stages 2 and 4: marks, solved here.
    for q in by[2] + by[4]:
        S = q['suspects']
        for s in S:
            kind = classify(s['facts'])
            if s['criterion'] != kind:
                out.append('%s: suspect %d is recorded %s, its marks are %s' % (q['id'], s['n'], s['criterion'], kind))
            if kind == 'SSA' and len(ssa_thirds(s['facts'])) != 2:
                out.append('%s: SSA suspect %d fits %d triangle(s), not two' % (q['id'], s['n'], len(ssa_thirds(s['facts']))))
            if s['role'] not in ('twin', 'drawn_alike'):
                why = drawing_matches(s['pts'], s['facts'])
                if why:
                    out.append('%s: suspect %d (%s): %s' % (q['id'], s['n'], s['role'], why))
            for why in label_faults(s['pts'], s['facts'], s['labels']):
                out.append('%s #%d: %s' % (q['id'], s['n'], why))
        proven = [[a['n'], b['n']] for a, b in itertools.combinations(S, 2)
                  if classify(a['facts']) in FULL and classify(b['facts']) in FULL
                  and all(abs(x - y) < 1e-6 for x, y in zip(solved(a['facts']), solved(b['facts'])))]
        if proven != [q['pair']]:
            out.append('%s: proven congruent pairs %s, the bank says %s' % (q['id'], proven, q['pair']))
        if sorted([role_n(q, 'culprit'), role_n(q, 'twin')]) != q['pair']:
            out.append('%s: pair %s is not the culprit and the twin' % (q['id'], q['pair']))
        cul = next(s for s in S if s['role'] == 'culprit')
        if q['criterion'] != classify(cul['facts']):
            out.append('%s: criterion %s, the culprit\'s marks are %s' % (q['id'], q['criterion'], classify(cul['facts'])))
    for q in by[4]:
        cul = next(s for s in q['suspects'] if s['role'] == 'culprit')
        want_rule = rule_of(classify(cul['facts']))
        if q['rule'] not in RULES or q['rule'] != want_rule:
            out.append('%s: rule %s, the culprit\'s marks give %s' % (q['id'], q['rule'], want_rule))
        if q['witness_right']:
            if q['witness_says'] != q['pair'] or q['witness_fooled_by'] is not None:
                out.append('%s: the witness is right but says %s (pair %s)' % (q['id'], q['witness_says'], q['pair']))
        else:
            fb = q['witness_fooled_by']
            dec = [s['n'] for s in q['suspects'] if s['role'] == fb]
            if not dec or q['witness_says'] != sorted([role_n(q, 'culprit'), dec[0]]):
                out.append('%s: the witness says %s, not the culprit and the %s' % (q['id'], q['witness_says'], fb))
            if q['witness_says'] == q['pair']:
                out.append('%s: a fooled witness names the real pair' % q['id'])

    # Stage 3.
    for q in by[3]:
        kind = classify(q['facts'])
        shown = q['shown']
        want_shown = 'SAS_right' if kind == 'SAS' and any(f[0] == 'angle' and f[2] == 90 for f in q['facts']) else kind
        if shown != want_shown:
            out.append('%s: shown %s, its marks are %s' % (q['id'], shown, want_shown))
        if q['answer'] != rule_of(kind):
            out.append('%s: answer %s, the marks give %s' % (q['id'], q['answer'], rule_of(kind)))
        why = drawing_matches(q['pts_a'], q['facts'])
        if why:
            out.append('%s A: %s' % (q['id'], why))
        if kind == 'SSA':
            th = ssa_thirds(q['facts'])
            if len(th) != 2:
                out.append('%s: SSA fits %d triangle(s), not two' % (q['id'], len(th)))
            else:
                why = drawing_matches(q['pts_b'], q['facts'])
                if why:
                    out.append('%s B: %s' % (q['id'], why))
                sides, angs = parts(q['facts'])
                (v, _), = angs.items()
                e3 = [e for e in (frozenset((0, 1)), frozenset((1, 2)), frozenset((0, 2))) if e not in sides][0]
                ea = list(sides)[0]
                got = []
                for P in (q['pts_a'], q['pts_b']):
                    unit = dist(P[min(ea)], P[max(ea)]) / sides[ea]
                    got.append(dist(P[min(e3)], P[max(e3)]) / unit)
                if not (any(abs(got[0] - t) < 0.02 * t for t in th) and any(abs(got[1] - t) < 0.02 * t for t in th)
                        and abs(got[0] - got[1]) > 0.02 * max(got)):
                    out.append('%s: A and B are not the two triangles the marks fit (third sides %s, drawn %s)' % (
                        q['id'], [round(t, 3) for t in th], [round(g, 3) for g in got]))
        for tag, P, L in (('A', q['pts_a'], q['labels_a']), ('B', q['pts_b'], q['labels_b'])):
            for why in label_faults(P, q['facts'], L):
                out.append('%s %s: %s' % (q['id'], tag, why))

    # Lines: exactly the contract's, every one used by some answer.
    try:
        lines = lines_of(html)
    except ValueError as e:
        out.append('lines: %s' % e)
        lines = {}
    for k in sorted(set(LINES_WANT) - set(lines)):
        out.append('lines: no LINES line for %s' % k)
    for k in sorted(set(lines) - set(LINES_WANT)):
        out.append('lines: LINES has %s, which the contract does not' % k)
    for k in sorted(set(lines) & set(LINES_WANT)):
        if lines[k] != LINES_WANT[k]:
            out.append('lines: LINES %s reads %r, not the contract\'s %r' % (k, lines[k], LINES_WANT[k]))
    used = set()
    for q in items:
        for _, right, keys, work, _ in scenarios(q):
            used.update(keys)
            for w in work:
                if w in LINES_WANT.values():
                    used.add(next(k for k, v in LINES_WANT.items() if v == w))
    for k in sorted(set(LINES_WANT) - used):
        out.append('lines: %s is never shown by any answer in this bank' % k)
    info['bank'] = len(items)
    return items


# ---------------------------------------------------------------- the page
def open_page(pw, base, html, size, aa=False):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    if aa:
        ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
    bc.offline(ctx, base)
    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % re.escape(SLUG))
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
    page.wait_for_function('!!window.G3 && !!G3.ui', timeout=15000)
    page.evaluate("""async () => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); };
        if (document.fonts && document.fonts.ready) await document.fonts.ready; }""")
    bc.wait_settled(page)
    if aa and not page.evaluate("document.body.classList.contains('accessible')"):
        errors.append('Aa mode did not come on from its stored preference')
    return br, page, errors


# One press: 'pick n', 'accuse', 'rule v' or 'judge v'.
PRESS_JS = r"""(s) => { const [k, v] = s.split(' ');
  if (k === 'pick') return G3.ui.pick(Number(v));
  if (k === 'accuse') { G3.ui.accuse(); return true; }
  if (k === 'rule') return G3.ui.rule(v);
  if (k === 'judge') return G3.ui.judge(v);
  return false; }"""

# What is on screen after an answer: the feedback, what is lit, and how low it all reaches.
SCREEN_JS = r"""() => {
  const fb = document.querySelector('#feedback .fb');
  const foot = document.querySelector('.site-footer');
  const fold = innerHeight - (foot && getComputedStyle(foot).position === 'fixed' ? foot.getBoundingClientRect().height : 0);
  const next = document.querySelector('#feedback .maffs-next');
  const low = Math.max(...[fb, next].filter(Boolean).map(e => e.getBoundingClientRect().bottom + scrollY));
  return {
    state: G3.ui.state(), score: G3.ui.score(), why: fb ? fb.dataset.why : null,
    head: fb && fb.querySelector('.fb-head') ? fb.querySelector('.fb-head').textContent : null,
    errs: fb ? [...fb.querySelectorAll('.fb-err')].map(e => [e.dataset.key, e.textContent]) : [],
    work: fb ? [...fb.querySelectorAll('.worked .w-line')].map(e => e.textContent) : [],
    next: !!next,
    litPair: [...document.querySelectorAll('#lineup .suspect.is-right')].map(b => Number(b.dataset.val)),
    wrongPair: [...document.querySelectorAll('#lineup .suspect.is-wrong')].map(b => Number(b.dataset.val)),
    litBtn: [...document.querySelectorAll('#rules .choice.is-right, #judge .choice.is-right')].map(b => b.dataset.val),
    locked: [...document.querySelectorAll('#lineup .suspect, #rules .choice')].filter(b => b.getClientRects().length).every(b => b.disabled),
    low: Math.round(low), fold: Math.round(fold), sw: document.documentElement.scrollWidth, vw: innerWidth };
}"""


def answer(page, steps):
    for s in steps:
        if page.evaluate("G3.ui.state()") != 'asking':
            break
        if not page.evaluate(PRESS_JS, s):
            return 'the press %r found nothing to press' % s
    return ''


def read_screen(tag, q, sc, a, out, content):
    steps, right, keys, work, lit = sc
    if a['why'] != ('right' if right else 'wrong'):
        out.append('%s: marked %s, should be %s' % (tag, a['why'], 'right' if right else 'wrong'))
        return
    if not a['next']:
        out.append('%s: no Next' % tag)
    if a['low'] > a['fold']:
        out.append('%s: the feedback and Next end at %d px, below the fold at %d px' % (tag, a['low'], a['fold']))
    if a['sw'] > a['vw']:
        out.append('%s: the page scrolls sideways (%d px wide at %d)' % (tag, a['sw'], a['vw']))
    if not content:
        return
    if right:
        if a['head'] != 'Right: ' + work[0]:
            out.append('%s: the right answer shows %r, not %r' % (tag, a['head'], 'Right: ' + work[0]))
    else:
        if [k for k, _ in a['errs']] != keys or [t for _, t in a['errs']] != [LINES_WANT[k] for k in keys]:
            out.append('%s: shows the line(s) %s, not the LINES line(s) for %s' % (tag, a['errs'], keys))
        if a['work'] != work:
            out.append('%s: the working reads %s, not %s' % (tag, a['work'], work))
    if lit == 'pair':
        if sorted(a['litPair']) != q['pair']:
            out.append('%s: the line-up lights %s, not the pair %s' % (tag, a['litPair'], q['pair']))
    elif a['litBtn'][-1:] != [lit]:
        out.append('%s: the buttons light %s, not %s' % (tag, a['litBtn'], lit))
    if not a['locked']:
        out.append('%s: the choices are not locked once answered' % tag)


def check_fit(page, items, size, aa, out, info):
    content = size == (375, 667) and not aa
    n, worst = 0, None
    for q in items:
        all_sc = scenarios(q)
        for sc in all_sc:
            if not content and not sc[1] and sc is not next(s for s in all_sc if not s[1] and s[2] == sc[2] and s[3] == sc[3]):
                continue      # away from 375x667 normal, one wrong answer for each set of lines and working (the screens are the same)
            page.evaluate('(id) => G3.ui.preview(id)', q['id'])
            tag = '%s %s%s %s' % (q['id'], '%dx%d' % size, ' Aa' if aa else '', ' then '.join(sc[0]))
            why = answer(page, sc[0])
            if why:
                out.append('%s: %s' % (tag, why))
                continue
            a = page.evaluate(SCREEN_JS)
            read_screen(tag, q, sc, a, out, content)
            n += 1
            room = a['fold'] - a['low']
            if worst is None or room < worst[0]:
                worst = (room, q['id'], ' then '.join(sc[0]))
    info.setdefault('fit', []).append(('%dx%d%s' % (size + (' Aa' if aa else '',)), n, worst))


# THE INK BOX (contract 3-GON-LINE-UP-BUILD, Amendment 1, 28 Nov 2026). getBBox() is not used for the containment check:
# it measures Outfit's full font box, 1.21 to 1.28 em tall, against the bank's 1.1 em box, so every one of the 468 labels
# "left" its box by 0.03 to 0.07 units at the top and bottom while its glyphs, 0.72 em tall, sat about 0.13 em inside it
# (and at least 0.137 units inside at the sides). Jon's rule is that a label never visibly clashes, so the check tests ink:
# the browser's own text measurement (canvas measureText's actualBoundingBox), in the label's own computed font, weight
# and size, centred (text-anchor middle) on the label's rendered x, with dominant-baseline central placing the middle of
# the font's ascent-to-descent box on its rendered y (the alphabetic baseline is then y + (ascent - descent) / 2). Checked
# against the rendered pixels of "9 cm", "12 cm" and "135°" drawn 100 times larger: within 0.01 units, never smaller.
LABELS_JS = r"""async () => {
  const svgs = [...document.querySelectorAll('svg.tri')].filter(s => s.getClientRects().length);
  const c = document.createElement('canvas').getContext('2d');
  const ink = async (t) => {
    const cs = getComputedStyle(t), size = +t.getAttribute('font-size'), x = +t.getAttribute('x'), y = +t.getAttribute('y');
    const font = cs.fontWeight + ' 100px ' + cs.fontFamily;
    await document.fonts.load(font, t.textContent);
    c.font = font; c.textAlign = 'center'; c.textBaseline = 'alphabetic';
    const m = c.measureText(t.textContent), k = size / 100;
    const base = y + (m.fontBoundingBoxAscent - m.fontBoundingBoxDescent) * k / 2;
    return [x - m.actualBoundingBoxLeft * k, base - m.actualBoundingBoxAscent * k, x + m.actualBoundingBoxRight * k, base + m.actualBoundingBoxDescent * k];
  };
  const out = [];
  for (const s of svgs) {
    const texts = [];
    for (const t of s.querySelectorAll('text.lab')) {
      const cs = getComputedStyle(t);
      texts.push({ text: t.textContent, x: +t.getAttribute('x'), y: +t.getAttribute('y'), size: +t.getAttribute('font-size'),
        font: cs.fontFamily, weight: cs.fontWeight, anchor: cs.textAnchor, baseline: cs.dominantBaseline, box: await ink(t) });
    }
    out.push({ vb: s.getAttribute('viewBox'), poly: s.querySelector('polygon.edge').getAttribute('points'), texts,
      arcs: [...s.querySelectorAll('path.arc')].map(p => p.getAttribute('d')),
      squares: [...s.querySelectorAll('path.sq')].map(p => p.getAttribute('d')) });
  }
  return out;
}"""


def check_drawn(tag, P, labels, got, out, info):
    """One drawing as rendered: corners, label texts and boxes, arcs and squares."""
    if got['vb'] != '-2 -2 10 10':
        out.append('%s: viewBox %r' % (tag, got['vb']))
    pts = [tuple(float(c) for c in p.split(',')) for p in got['poly'].split()]
    if len(pts) != 3 or any(abs(a[0] - b[0]) > 1e-3 or abs(a[1] - (6 - b[1])) > 1e-3 for a, b in zip(pts, P)):
        out.append('%s: the triangle is drawn at %s, not the bank\'s corners turned (%s)' % (tag, pts, P))
    texted = [l for l in labels if l['type'] != 'right']
    if [t['text'] for t in got['texts']] != [l['text'] for l in texted]:
        out.append('%s: labels %s, the bank has %s' % (tag, [t['text'] for t in got['texts']], [l['text'] for l in texted]))
        return
    for t, l in zip(got['texts'], texted):
        if abs(t['x'] - l['x']) > 1e-3 or abs(t['y'] - (6 - l['y'])) > 1e-3:
            out.append('%s: label %s drawn at (%g, %g), not the bank\'s point turned' % (tag, t['text'], t['x'], t['y']))
        if (t['size'] != (0.75 if l['type'] == 'side' else 0.68) or not t['font'].startswith('Outfit') or t['weight'] != '600'
                or t['anchor'] != 'middle' or t['baseline'] != 'central'):
            out.append('%s: label %s drawn at font-size %g, %s %s, anchor %s, baseline %s (the contract: %g, Outfit 600, middle, central)'
                       % (tag, t['text'], t['size'], t['font'], t['weight'], t['anchor'], t['baseline'], 0.75 if l['type'] == 'side' else 0.68))
        b = l['box']
        want = (b[0], 6 - b[3], b[2], 6 - b[1])
        r = t['box']
        over = max(want[0] - r[0], r[2] - want[2], want[1] - r[1], r[3] - want[3])
        info['ink_worst'] = max(info.get('ink_worst', -9), over)
        if over > 1e-3:
            out.append('%s: label %s\'s ink is at x %.3f..%.3f, y %.3f..%.3f, outside its bank box x %.3f..%.3f, y %.3f..%.3f (by %.3f)'
                       % ((tag, t['text']) + tuple(r[i] for i in (0, 2, 1, 3)) + tuple(want[i] for i in (0, 2, 1, 3)) + (over,)))
    Q = [(p[0], 6 - p[1]) for p in P]
    nums = lambda d: [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', d)]  # noqa: E731
    angles = [l for l in labels if l['type'] == 'angle']
    if len(got['arcs']) != len(angles):
        out.append('%s: %d arcs for %d marked angles' % (tag, len(got['arcs']), len(angles)))
    for d, l in zip(got['arcs'], angles):
        v = Q[l['fact'][1]]
        x = nums(d)
        if abs(dist((x[0], x[1]), v) - ARC) > 2e-3 or abs(dist((x[-2], x[-1]), v) - ARC) > 2e-3 or x[2] != ARC:
            out.append('%s: the arc for %s is not radius %g at its corner' % (tag, l['text'], ARC))
    rights = [l for l in labels if l['type'] == 'right']
    if len(got['squares']) != len(rights):
        out.append('%s: %d right-angle squares for %d right angles' % (tag, len(got['squares']), len(rights)))
    for d, l in zip(got['squares'], rights):
        v = Q[l['vertex']]
        x = nums(d)
        if abs(dist((x[0], x[1]), v) - SQUARE) > 2e-3 or abs(dist((x[4], x[5]), v) - SQUARE) > 2e-3:
            out.append('%s: the right-angle square at corner %d is not of side %g' % (tag, l['vertex'], SQUARE))


def check_labels(page, items, size, out, info):
    n = 0
    for q in items:
        if q['stage'] == 1:
            continue
        page.evaluate('(id) => G3.ui.preview(id)', q['id'])
        got = page.evaluate(LABELS_JS)
        if q['stage'] == 3:
            want = [('%s A' % q['id'], q['pts_a'], q['labels_a']), ('%s B' % q['id'], q['pts_b'], q['labels_b'])]
        else:
            want = [('%s #%d' % (q['id'], s['n']), s['pts'], s['labels']) for s in q['suspects']]
        if len(got) != len(want):
            out.append('%s at %dx%d: %d drawings, not %d' % ((q['id'],) + size + (len(got), len(want))))
            continue
        for (tag, P, L), g in zip(want, got):
            check_drawn('%s at %dx%d' % ((tag,) + size), P, L, g, out, info)
            n += 1
    info.setdefault('labels', []).append((size, n))


def check_working(page, items, out, info):
    for q in items:
        got = page.evaluate('(id) => G3.working(id)', q['id'])
        if got != want_working(q):
            out.append('%s: the working reads %r, not %r' % (q['id'], got, want_working(q)))
    info['working'] = len(items)


def play(page, m, items, out):
    st = int(m[-1])
    page.evaluate('() => { window.__ev = []; window.__sub = []; }')
    page.evaluate("(m) => document.querySelector('#stageList .stage-btn[data-mode=\"' + m + '\"]').click()", m)
    seen, right = [], 0
    for k in range(PER):
        q = page.evaluate('G3.ui.question()')
        tag = '%s question %d (%s)' % (m, k + 1, q and q['id'])
        if page.evaluate('G3.ui.state()') != 'asking' or not q:
            out.append('%s: no question on screen' % tag)
            return
        seen.append(q['id'])
        if q['stage'] != st:
            out.append('%s: a stage %d item' % (tag, q['stage']))
        sc = scenarios(q)
        pick = [s for s in sc if s[1]][0] if k % 2 == 0 else [s for s in sc if not s[1]][k % len([s for s in sc if not s[1]])]
        why = answer(page, pick[0])
        if why:
            out.append('%s: %s' % (tag, why))
            return
        a = page.evaluate(SCREEN_JS)
        read_screen(tag, q, pick, a, out, True)
        right += pick[1]
        if a['score'] != right:
            out.append('%s: the score reads %d, expected %d' % (tag, a['score'], right))
        page.evaluate('G3.ui.next()')
    if page.evaluate('G3.ui.state()') != 'over':
        out.append('%s: the run did not finish after %d questions' % (m, PER))
        return
    if len(set(seen)) != PER:
        out.append('%s: the run served %s, not %d different items' % (m, seen, PER))
    if st == 1 and seen[0] != 's1-01':
        out.append('%s: the run opened with %s, not s1-01' % (m, seen[0]))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('mode') != m or done[0].get('level') != 'gcse':
        out.append('%s: game_completed %s, expected one with score %d, mode %s, level gcse' % (m, done, right, m))
    if sub != [[SLUG, m, right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d of %d' % (m, sub, m, right, PER))
    qa = [p for n, p in ev if n == 'question_answered']
    if [p.get('question_id') for p in qa] != seen or [p.get('correct') for p in qa] != [k % 2 == 0 for k in range(PER)]:
        out.append('%s: question_answered events %s do not match the run' % (m, [(p.get('question_id'), p.get('correct')) for p in qa]))
    started = [p for n, p in ev if n == 'game_started']
    if len(started) != 1 or started[0].get('mode') != m:
        out.append('%s: game_started %s' % (m, started))
    extra = sorted({n for n, _ in ev} - EVENTS)
    if extra:
        out.append('%s: events the contract does not allow: %s' % (m, extra))
    shown = page.evaluate("() => ({ score: document.getElementById('resScore').textContent, of: document.getElementById('resOf').textContent, on: document.getElementById('results').classList.contains('active') })")
    if not shown['on'] or shown['score'] != str(right) or shown['of'] != 'out of %d' % PER:
        out.append('%s: the results screen shows %s, expected %d out of %d' % (m, shown, right, PER))
    page.evaluate("document.getElementById('menuBtn').click()")


def check(html, out, units, shard=None, sample=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info = {}
    if 'bank' in units:
        with unit('bank'):
            try:
                check_bank(html, out, info)
            except Exception as e:  # noqa: BLE001
                out.append('the bank checks threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u != 'bank']
    if not browser:
        return info
    try:
        items = [json.loads(ln) for ln in bank_lines(html)]
    except Exception as e:  # noqa: BLE001
        out.append('the page\'s bank cannot be read: %s' % str(e).splitlines()[0][:200])
        return info
    every = items
    if sample:
        items = [q for s in (1, 2, 3, 4) for q in [x for x in items if x['stage'] == s][:sample]]
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    parts_ = uid.split(' ')
                    size = tuple(int(x) for x in parts_[1].split('x'))
                    aa = len(parts_) > 2 and parts_[2] == 'Aa'
                    br, page, errs = open_page(pw, base, html, size, aa)
                    try:
                        if uid.startswith('working'):
                            check_working(page, every, out, info)   # cheap: always every item
                        elif uid.startswith('labels'):
                            check_labels(page, items, size, out, info)
                        elif uid.startswith('play'):
                            for m in MODES:
                                play(page, m, items, out)
                            info['played'] = len(MODES)
                        else:
                            check_fit(page, items, size, aa, out, info)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


# ---------------------------------------------------------------- the self-test: the contract's eight plants (5e) and Amendment 1's ninth
PLANT_SAMPLE = 2
PLANTS = [
    ('a second congruent pair in a stage 1 line-up',
     [('{"n":4,"role":"stranger","pts":[[5,0],[0,0],[3,5]],"how":"other"}', '{"n":4,"role":"stranger","pts":[[4,3],[1,0],[0,3]],"how":"other"}')],
     'bank', r'^s1-01: congruent pairs \[\[2, 4\], \[2, 6\], \[4, 6\]\]'),
    ('an SSA decoy made unambiguous', [], 'bank', r'SSA suspect \d fits 1 triangle\(s\), not two'),
    ('a label moved onto an edge', [], 'bank', r'is 0\.000 from an edge'),
    ('an angle label moved beside another vertex', [], 'bank', r'angle label .* is not nearer its own corner'),
    ('a label moved onto its arc', [], 'bank', r'from the arc or square at corner'),
    ('a stage 3 answer changed', [], 'bank', r'^s3-01: answer SAS, the marks give SSS'),
    # Amendment 1: one label's bank y moved by 0.2 units (its box left where it was), so the drawn ink leaves the box.
    ('a label\'s bank y moved by 0.2 units', [], 'labels 375x667', r"^s2-01 #1 at 375x667: label .*'s ink is at .* outside its bank box"),
    ('the turn wording swapped (clockwise for anticlockwise)',
     [("rot90: 'a quarter turn anticlockwise', rot270: 'a quarter turn clockwise'", "rot90: 'a quarter turn clockwise', rot270: 'a quarter turn anticlockwise'")],
     'working 375x667', r'the working reads .*a quarter turn clockwise.*, not .*a quarter turn anticlockwise'),
    ('a wrong LINES line shown for a decoy',
     [("var role = suspectN(Q, n).role;", "var role = suspectN(Q, n).role === 'one_differs' ? 'drawn_alike' : suspectN(Q, n).role;")],
     'fit 375x667 normal', r'shows the line\(s\) .*drawn_alike.*, not the LINES line\(s\) for \[\'one_differs\'\]'),
]


def _bank_plants(html):
    """The five bank plants that move one label or one number: built from the page's own lines, so each changes exactly
    one item and leaves the rest as they are."""
    lines = bank_lines(html)
    items = [json.loads(ln) for ln in lines]
    built = {}

    def swap(q_id, mutate):
        i = next(k for k, q in enumerate(items) if q['id'] == q_id)
        q = json.loads(lines[i])
        mutate(q)
        return [(lines[i], json.dumps(q, separators=(',', ':'), ensure_ascii=False))]

    # An SSA decoy (angle_moved) whose side opposite the angle is made as long as the side beside it: one triangle.
    q2 = next(q for q in items if q['stage'] in (2, 4) and any(s['criterion'] == 'SSA' for s in q['suspects']))

    def unambiguous(q):
        s = next(x for x in q['suspects'] if x['criterion'] == 'SSA')
        sides, angs = parts(s['facts'])
        (v, _), = angs.items()
        adj = [x for e, x in sides.items() if v in e][0]
        for f in s['facts']:
            if f[0] == 'side' and v not in (f[1], f[2]):
                f[3] = adj + 2
    built['an SSA decoy made unambiguous'] = swap(q2['id'], unambiguous)
    q = items[12]   # s2-01: its first suspect's first side label, moved onto that side's midpoint

    def onto_edge(q):
        s = q['suspects'][0]
        l = next(x for x in s['labels'] if x['type'] == 'side')
        a, b = s['pts'][l['fact'][1]], s['pts'][l['fact'][2]]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        dx, dy = mx - l['x'], my - l['y']
        l['x'], l['y'] = round(mx, 3), round(my, 3)
        l['box'] = [round(l['box'][0] + dx, 3), round(l['box'][1] + dy, 3), round(l['box'][2] + dx, 3), round(l['box'][3] + dy, 3)]
    built['a label moved onto an edge'] = swap(q['id'], onto_edge)
    qa = next(q for q in items if q['stage'] == 2 and any(l['type'] == 'angle' for s in q['suspects'] for l in s['labels']))

    def other_vertex(q):
        s = next(x for x in q['suspects'] if any(l['type'] == 'angle' for l in x['labels']))
        l = next(x for x in s['labels'] if x['type'] == 'angle')
        v = l['fact'][1]
        w = [j for j in range(3) if j != v][0]
        P = s['pts']
        cx, cy = sum(p[0] for p in P) / 3, sum(p[1] for p in P) / 3
        nx, ny = P[w][0] + 0.35 * (cx - P[w][0]), P[w][1] + 0.35 * (cy - P[w][1])
        dx, dy = nx - l['x'], ny - l['y']
        l['x'], l['y'] = round(nx, 3), round(ny, 3)
        l['box'] = [round(l['box'][0] + dx, 3), round(l['box'][1] + dy, 3), round(l['box'][2] + dx, 3), round(l['box'][3] + dy, 3)]
    built['an angle label moved beside another vertex'] = swap(qa['id'], other_vertex)

    def onto_arc(q):
        s = next(x for x in q['suspects'] if any(l['type'] == 'angle' for l in x['labels']))
        l = next(x for x in s['labels'] if x['type'] == 'angle')
        V = s['pts'][l['fact'][1]]
        ux, uy = l['x'] - V[0], l['y'] - V[1]
        k = math.hypot(ux, uy)
        nx, ny = V[0] + ux / k * ARC, V[1] + uy / k * ARC
        dx, dy = nx - l['x'], ny - l['y']
        l['x'], l['y'] = round(nx, 3), round(ny, 3)
        l['box'] = [round(l['box'][0] + dx, 3), round(l['box'][1] + dy, 3), round(l['box'][2] + dx, 3), round(l['box'][3] + dy, 3)]
    built['a label moved onto its arc'] = swap(qa['id'], onto_arc)

    def y_moved(q):
        l = next(x for x in q['suspects'][0]['labels'] if x['type'] == 'side')
        l['y'] = round(l['y'] + 0.2, 3)
    built["a label's bank y moved by 0.2 units"] = swap(q['id'], y_moved)

    def answer_changed(q):
        q['answer'] = 'SAS'
    built['a stage 3 answer changed'] = swap('s3-01', answer_changed)
    return built


def selftest(html, plants=None, shard=None):
    ok = True
    built = _bank_plants(html)
    for what, edits, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = html
                for old, new in (edits or built.get(what, [])):
                    src = pc.apply_plant(src, old, new, name=what)
                if src == html:
                    raise pc.StalePlant(what, 'nothing was planted')
            except pc.StalePlant as e:
                print('  self-test %-62s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id], sample=PLANT_SAMPLE)
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-62s %s' % (what, ('caught: ' + hit[0][:110]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:110] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = (['bank', 'working 375x667'] + ['labels %dx%d' % s for s in SIZES] + ['play 375x667']
             + ['fit %dx%d %s' % (s + (m,)) for s in SIZES for m in ('normal', 'Aa')])
    if args.selftest:
        units = []
    mine = shard.pick(units + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    run = [u for u in units if u in mine]
    info = check(html, out, run, shard) if run else {}
    if 'bank' in info:
        print('%s: %d items, the contract\'s hashes and counts; every pair, SSA decoy, drawing, rule, witness and label worked out again here; LINES the contract\'s fourteen, every one used' % (SLUG, info['bank']))
    if 'working' in info:
        print('%s: the working line of all %d items is the contract\'s' % (SLUG, info['working']))
    for size, n in info.get('labels', []):
        print('%s: %d drawings at %dx%d: corners, label points, arcs and squares the bank\'s' % (SLUG, n, size[0], size[1]))
    if 'ink_worst' in info:
        print('%s: every label\'s ink inside its bank box; the least room at any edge: %.3f drawing units' % (SLUG, -info['ink_worst']))
    if 'played' in info:
        print('%s: %d stages played to the end at 375x667 (right and wrong in turn)' % (SLUG, info['played']))
    for tag, n, worst in info.get('fit', []):
        print('%s: %d answer screens at %s; the least room under Next: %s' % (SLUG, n, tag, ('%d px (%s, %s)' % worst) if worst else 'none measured'))
    ok = selftest(html, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
    for f in out[:80]:
        print('FAIL  ' + f)
    if len(out) > 80:
        print('FAIL  ... and %d more' % (len(out) - 80))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
