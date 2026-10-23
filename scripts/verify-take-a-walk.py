#!/usr/bin/env python3
# ci-line: Take a Walk, part 1 (every pool question's key recomputed from its drawn lengths, every missing length determined by the drawing and as many as its stage says, no named slip equal to its key, the worked steps ending on the key, sessions easiest first) | --part 1
# ci-line: Take a Walk, part 2 (every pool question drawn by the game and read back: its labels the data's, every side drawn to one scale within 1 px) | --part 2
# ci-line: Take a Walk, part 3 (every stage played to its results screen at 1280 and 320 px: the worked example logs nothing, walk or cover, the find-it-first tap, the unit, the calculator in Stage 4 only, no sideways scroll) | --part 3
# ci-line: Take a Walk, part 4 (fault-injection self-test: seven planted faults, each caught) | --part 4
# ci-deps: games/take-a-walk/
"""Independent verification for Take a Walk (games/take-a-walk/), built 23 Oct 2026 (contract TAKE-A-WALK, verbatim in
docs/handover/contracts/2026-10-23-take-a-walk.md; its calculator by stage, contract CALC-BY-STAGE). SR-30: checked from
its first PR.

WHY THIS READS THE LIVE PAGE
-------------------------------------------------------------------------------
The game keeps every decision a student sees (the pools, every shape and its labels, every key, every named slip, the
worked steps, the order a stage is served in) on window.TAW as plain functions, and its UI calls them through TAW. This
script loads the page under Playwright, reads THOSE pools and sessions, and recomputes everything here, in Python, from
the shapes' coordinates and the contract's words, never from the game's own functions:

  Keys       the perimeter as the sum of the boundary's pieces (sides and arcs, from their coordinates); the area by
             Green's theorem round the boundary (so it does not use the game's split into parts); working backwards,
             the asked length measured on the shape, and the given total checked against the shape. Stage 4 to 1 d.p.
             (half up), Stages 1-3 whole metres.
  Labels     every labelled side is its measured length; every dashed dimension is its line's length.
  Missing    a lone shape (square, rectangle, triangle, circle, semicircle, parallelogram) has none, and has the labels
             its formula needs; a compound shape's missing lengths are its unlabelled sides and arcs, exactly as many as
             its stage says (Stage 1 none, then 1, 2, 3), each determined by the drawing: on its axis, labelled sides
             and dimensions join its two grid lines (a weighted union-find over the lines, written here), and the
             distance they fix is the true one.
  Slips      the contract's named wrong answers, recomputed here from the geometry for each question they apply to;
             the game's list is exactly these, and none gives the key at the answer's precision.
  Steps      every question's working ends on the key with its unit; a missing length is found before it is used.
  Sessions   SESSIONS seeds a stage: a worked example (not one of the 10), then 10 from the stage's pool, distinct,
             served in non-decreasing order of the measure (working backwards last, then the fewest parts, then the
             largest length on the drawing, or the given total working backwards); the first with a missing length
             opens with the tap step.
  Drawn      every pool question drawn by the game: every side's drawn length is k times its true length within 1 px,
             one k for the whole shape; every label's text is its side's or dimension's value; the asked length is "?".
  Play       every stage end to end at 1280x800 and 320x568, read from the page (canon 7.9): the worked example's steps
             one tap at a time and no question_answered while it shows; Stage 1's walk-or-cover choice (a wrong choice
             plays its picture, logs nothing and asks again); the find-it-first tap (a labelled side highlights the
             sides to compare; the unlabelled one goes on); the right number with the wrong unit gets the unit message
             and is not marked; a wrong answer shows the picture, the line, the working and Next; the calculator is
             mounted and shown in Stage 4 only; no sideways scroll; one event of each kind, with the stage's mode, and
             one score to the stage's board; "Next: Stage N+1" on the results (none after 4).
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'take-a-walk'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4']
STAGE_N = {m: i + 1 for i, m in enumerate(MODES)}
DP = {'stage-1': 0, 'stage-2': 0, 'stage-3': 0, 'stage-4': 1}
LONE = {'sq', 'rect', 'rtri', 'itri', 'circle', 'semi', 'para'}
PARTS = {'sq': 1, 'rect': 1, 'rtri': 1, 'itri': 1, 'circle': 1, 'semi': 1, 'para': 1, 'L': 2, 'T': 2, 'house': 2,
         'rtrap': 2, 'U': 3, 'Tsb': 3, 'Tst': 3}
BACK = {'BA', 'BP', 'BT', 'BC', 'BH'}
MIN_POOL = 40
SESSIONS = 40
SIZES = [(1280, 800), (320, 568)]
EPS = 1e-6


def rnd(x, dp):
    """Half up to dp places (the game's precision rule)."""
    f = 10 ** dp
    return math.floor(x * f + 0.5 + 1e-9) / f


# ---------------------------------------------------------------- geometry, from coordinates
def ends(p):
    if p['t'] == 'L':
        return p['a'], p['b']
    c, r = p['c'], p['r']
    return ([c[0] + r * math.cos(p['a0']), c[1] + r * math.sin(p['a0'])],
            [c[0] + r * math.cos(p['a1']), c[1] + r * math.sin(p['a1'])])


def length(p):
    if p['t'] == 'L':
        return math.hypot(p['b'][0] - p['a'][0], p['b'][1] - p['a'][1])
    return p['r'] * abs(p['a1'] - p['a0'])


def perimeter(path):
    return sum(length(p) for p in path)


def area(path):
    """Green's theorem round the counterclockwise boundary: 1/2 of the integral of x dy - y dx."""
    s = 0.0
    for p in path:
        if p['t'] == 'L':
            (x1, y1), (x2, y2) = p['a'], p['b']
            s += x1 * y2 - x2 * y1
        else:
            (cx, cy), r, a0, a1 = p['c'], p['r'], p['a0'], p['a1']
            s += r * r * (a1 - a0) + r * cx * (math.sin(a1) - math.sin(a0)) - r * cy * (math.cos(a1) - math.cos(a0))
    return s / 2


def axis(p):
    a, b = ends(p)
    dx, dy = abs(b[0] - a[0]), abs(b[1] - a[1])
    if dx < EPS and dy < EPS:
        return None
    if dy < EPS:
        return 0
    if dx < EPS:
        return 1
    return None


def determined(sh, i):
    """Is piece i's span fixed by the drawing? A weighted union-find over the grid lines of its axis, joined by every
    labelled side and dimension on that axis. Returns the span it fixes, or None."""
    p = sh['path'][i]
    k = axis(p)
    if k is None:
        return None
    parent, off = {}, {}

    def key(v):
        return round(v * 1e6)

    def find(v):
        if parent.setdefault(v, v) == v:
            off.setdefault(v, 0.0)
            return v
        r = find(parent[v])
        off[v] = off[v] + off[parent[v]] if parent[v] != r else off[v]
        parent[v] = r
        return r

    def union(a, b, d):   # coordinate(b) - coordinate(a) = d
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        parent[rb] = ra
        off[rb] = off[a] + d - off[b]

    def rel(v):
        r = find(v)
        return r, off[v] if v != r else 0.0

    spans = []
    for j, q in enumerate(sh['path']):
        if q['t'] == 'L' and q['lab'] is not None and axis(q) == k:
            spans.append((q['a'][k], q['b'][k], q['lab']))
    for d in sh['dims']:
        if d['val'] is not None and abs(d['a'][1 - k] - d['b'][1 - k]) < EPS:
            spans.append((d['a'][k], d['b'][k], d['val']))
    for a, b, v in spans:
        union(key(a), key(b), v if b > a else -v)
    e0, e1 = ends(p)
    ra, oa = rel(key(e0[k]))
    rb, ob = rel(key(e1[k]))
    if ra != rb:
        return None
    return abs(ob - oa)


def missing_of(sh, fam):
    if fam in LONE:
        return []
    return [i for i, p in enumerate(sh['path']) if p['lab'] is None]


def span_of(p):
    a, b = ends(p)
    return math.hypot(b[0] - a[0], b[1] - a[1])


def bbox(path):
    xs, ys = [], []
    for p in path:
        if p['t'] == 'L':
            xs += [p['a'][0], p['b'][0]]
            ys += [p['a'][1], p['b'][1]]
        else:
            for j in range(65):
                t = p['a0'] + (p['a1'] - p['a0']) * j / 64
                xs.append(p['c'][0] + p['r'] * math.cos(t))
                ys.append(p['c'][1] + p['r'] * math.sin(t))
    return min(xs), max(xs), min(ys), max(ys)


def verts(path):
    return [p['a'] for p in path if p['t'] == 'L']


# ---------------------------------------------------------------- the named slips (the contract's list)
def triangle_of(q):
    """(base, perpendicular height, slant) of the question's triangle, measured on its coordinates."""
    sh, fam = q['shape'], q['fam']
    path = sh['path']
    if fam == 'rtri':
        legs = [length(p) for p in path if axis(p) is not None]
        hyp = [length(p) for p in path if axis(p) is None][0]
        base = [length(p) for p in path if axis(p) == 0][0]
        h = [length(p) for p in path if axis(p) == 1][0]
        return base, h, hyp
    if fam == 'itri':
        (x0, _), (x1, _) = path[0]['a'], path[0]['b']
        apex = path[1]['b']
        return abs(x1 - x0), apex[1], length(path[1])
    if fam == 'house':
        W = path[0]['b'][0]
        H = path[1]['b'][1]
        apex = path[2]['b']
        return W, apex[1] - H, length(path[2])
    if fam == 'rtrap':
        B = path[0]['b'][0] - path[1]['b'][0]
        return B, path[1]['b'][1], length(path[1])
    return None


def semis(q):
    return [p for p in q['shape']['path'] if p['t'] == 'C']


def expected_errors(q):
    """{id: value} of the named slips that apply to q, from the contract's list, measured on the shape."""
    sh, fam, ask = q['shape'], q['fam'], q['ask']
    path = sh['path']
    P, A = perimeter(path), area(path)
    out = {}
    x0, x1, y0, y1 = bbox(path)
    circle = fam == 'circle'
    if ask == 'A':
        out['PD' if circle else 'AS'] = P                      # added the sides (pi d for a cover)
        if fam in ('L', 'T', 'U', 'house', 'rtrap'):
            out['OB'] = (x1 - x0) * (y1 - y0)                   # from the outer sides
        if fam == 'L':                                          # the two full rectangles, overlapping
            v = verts(path)
            W, h2, a, Hf = v[1][0], v[2][1], v[3][0], v[4][1]
            out['OL'] = W * h2 + a * Hf
        if fam == 'T':
            v = verts(path)
            u, w, s, Tw, top = v[0][0], v[1][0] - v[0][0], v[2][1], v[3][0], v[4][1]
            out['OL'] = Tw * (top - s) + w * top
        t = triangle_of(q)
        if t:
            b, h, sl = t
            out['TH'] = A + b * h / 2                           # not halved
            out['SL'] = A - b * h / 2 + b * sl / 2              # the slant side for the height
        if fam == 'para':
            b, sl, h = length(path[0]), length(path[3]), path[2]['a'][1]
            out['SL'] = b * sl
        for p in semis(q):
            f = 1.0 if circle else 0.5
            r = p['r']
            rest = A - f * math.pi * r * r
            out['DR'] = rest + f * math.pi * (2 * r) ** 2       # the diameter as the radius
            out['SQ'] = rest + f * (math.pi * r) ** 2           # (pi r) squared
            if circle and sh['dims'][0]['kind'] == 'radius':
                out['RD'] = rest + f * math.pi * (r / 2) ** 2   # the radius as the diameter
    if ask == 'P':
        out['PR' if circle else 'PM'] = A                      # multiplied (pi r squared for a walk)
        if fam in ('rect', 'sq', 'para'):
            out['LW'] = P / 2                                   # two sides only
        miss = missing_of(sh, fam)
        straight = [i for i in miss if path[i]['t'] == 'L']
        if straight:
            out['MS'] = P - sum(length(path[i]) for i in straight)   # the unlabelled sides left out
            diff, any_ = 0.0, False
            for i in straight:
                near = nearest_label(sh, i)
                if near is not None and abs(near - length(path[i])) > EPS:
                    diff += near - length(path[i])
                    any_ = True
            if any_:
                out['NL'] = P + diff                            # copied from the nearest label
        joins = sum(abs(j['b'][0] - j['a'][0]) + abs(j['b'][1] - j['a'][1]) for j in sh['joins'])
        if joins:
            out['IJ'] = P + joins                               # an inside line walked
        for p in semis(q):
            if circle:
                if sh['dims'][0]['kind'] == 'diam':
                    out['DR'] = 2 * math.pi * 2 * p['r']
                else:
                    out['RD'] = math.pi * p['r']
            else:
                out['FC'] = P + math.pi * p['r']                # the full circle
                if fam == 'semi':
                    out['ND'] = math.pi * p['r']                # the straight side left out
    if ask == 'BP':
        out['LW'] = q['given'] - q['side']
    if ask == 'BT':
        out['TH'] = q['given'] / q['side']
    if ask == 'BC':
        out['DR'] = q['given'] / (2 * math.pi)
    if ask == 'BA':
        out['AS'] = q['given'] / 2 - q['side']
    return {k: v for k, v in out.items() if math.isfinite(v) and v > 0}


def nearest_label(sh, i):
    p = sh['path'][i]
    k = axis(p)
    m = ((p['a'][0] + p['b'][0]) / 2, (p['a'][1] + p['b'][1]) / 2)
    best, bd = None, float('inf')
    for j, s in enumerate(sh['path']):
        if j == i or s['t'] != 'L' or s['lab'] is None or axis(s) != k:
            continue
        n = ((s['a'][0] + s['b'][0]) / 2, (s['a'][1] + s['b'][1]) / 2)
        d = (n[0] - m[0]) ** 2 + (n[1] - m[1]) ** 2
        if d < bd - 1e-9:
            bd, best = d, s['lab']
    return best


# ---------------------------------------------------------------- the engine
def expected_key(q):
    sh, ask = q['shape'], q['ask']
    path = sh['path']
    if ask == 'P':
        return perimeter(path)
    if ask == 'A':
        return area(path)
    x0, x1, y0, y1 = bbox(path)
    return {'BA': y1 - y0, 'BP': y1 - y0, 'BT': y1 - y0, 'BH': y1 - y0, 'BC': x1 - x0}[ask]


def given_ok(q):
    """Working backwards: the total the question gives is the shape's, and the side it gives is the shape's."""
    sh, ask = q['shape'], q['ask']
    path = sh['path']
    x0, x1, y0, y1 = bbox(path)
    if ask == 'BA':
        return abs(q['given'] - area(path)) < EPS and abs(q['side'] - (x1 - x0)) < EPS
    if ask == 'BP':
        return abs(q['given'] - perimeter(path)) < EPS and abs(q['side'] - (x1 - x0)) < EPS
    if ask in ('BT', 'BH'):
        return abs(q['given'] - area(path)) < EPS and abs(q['side'] - length(path[0])) < EPS
    if ask == 'BC':
        return abs(q['given'] - rnd(perimeter(path), 1)) < EPS
    return True


def required_labels(q):
    """A lone shape carries what its formula needs."""
    sh, fam, ask = q['shape'], q['fam'], q['ask']
    path, dims = sh['path'], sh['dims']
    lab = [p['lab'] is not None for p in path]
    if ask in BACK:
        return True
    if fam in ('sq', 'rect'):
        return any(lab[i] for i in (0, 2)) and any(lab[i] for i in (1, 3))
    if fam == 'rtri':
        return all(lab)
    if fam == 'itri':
        return lab[0] and (ask == 'A' and any(d['kind'] == 'height' and d['val'] for d in dims) or ask == 'P' and lab[1] and lab[2])
    if fam == 'circle':
        return len(dims) == 1 and dims[0]['val'] is not None
    if fam == 'semi':
        return lab[0]
    if fam == 'para':
        return lab[0] and (lab[3] if ask == 'P' else any(d['kind'] == 'height' and d['val'] for d in dims))
    return True


def measure(q):
    labs = [p['lab'] for p in q['shape']['path'] if p['lab'] is not None] + \
        [d['val'] for d in q['shape']['dims'] if d['val'] is not None]
    back = q['ask'] in BACK
    return (1 if back else 0, PARTS[q['fam']], q['given'] if back else max(labs + [0]))


def check_question(q, mode, out, where):
    dp = DP[mode]
    sh = q['shape']
    exact = expected_key(q)
    if q['ask'] in BACK and not given_ok(q):
        out.append('%s: the given total or side is not the shape\'s' % where)
    want = rnd(exact, dp)
    if abs(q['key'] - want) > EPS:
        out.append('%s: key %s, recomputed %s' % (where, q['key'], want))
    if q['unit'] != ('m2' if q['ask'] == 'A' else 'm'):
        out.append('%s: unit %s' % (where, q['unit']))
    for i, p in enumerate(sh['path']):
        if p['t'] == 'L' and p['lab'] is not None and abs(p['lab'] - length(p)) > EPS:
            out.append('%s: side %d labelled %s, measured %s' % (where, i, p['lab'], length(p)))
        if p['t'] == 'C' and p['lab'] is not None:
            out.append('%s: an arc carries a label' % where)
    for j, d in enumerate(sh['dims']):
        if d['val'] is not None and abs(d['val'] - math.hypot(d['b'][0] - d['a'][0], d['b'][1] - d['a'][1])) > EPS:
            out.append('%s: dimension %d labelled %s, measured otherwise' % (where, j, d['val']))
    miss = missing_of(sh, q['fam'])
    if sorted(miss) != sorted(q['missing']):
        out.append('%s: missing %s, the drawing\'s unlabelled sides are %s' % (where, q['missing'], miss))
    if q['fam'] in LONE:
        if not required_labels(q):
            out.append('%s: a lone shape without the labels its formula needs' % where)
    elif q['ask'] not in BACK and len(miss) != STAGE_N[mode] - 1:
        out.append('%s: %d lengths missing; stage %d asks for %d' % (where, len(miss), STAGE_N[mode], STAGE_N[mode] - 1))
    for i in miss:
        span = determined(sh, i)
        if span is None or abs(span - span_of(sh['path'][i])) > EPS:
            out.append('%s: missing length %d is not determined by the drawing' % (where, i))
    exp = expected_errors(q)
    got = {e['id']: e['v'] for e in q['errors']}
    if set(exp) != set(got) or any(abs(exp[k] - got[k]) > 1e-6 for k in exp):
        out.append('%s: named slips %s, expected %s' % (where, sorted(got.items()), sorted(exp.items())))
    for k, v in exp.items():
        if abs(rnd(v, dp) - want) < EPS:
            out.append('%s: the named slip %s gives the key %s' % (where, k, want))


def check_steps(q, steps, out, where):
    last = steps[-1]['text']
    ans = ('%.1f' % q['key'] if q['dp'] else '%d' % round(q['key'])) + ' ' + ('m²' if q['unit'] == 'm2' else 'm')
    if ans not in last:
        out.append('%s: the working ends %r, not on %s' % (where, last[-60:], ans))
    for s in steps:
        for i in q['missing']:
            if i not in s.get('show', []) and s.get('anim') == 'walk' and q['ask'] == 'P':
                out.append('%s: a missing length used before it is found' % where)


def check_engine(page, out, sessions=SESSIONS):
    pools = page.evaluate('TAW.pools()')
    info = {'pools': {}}
    for mode in MODES:
        pool = pools[mode]
        info['pools'][mode] = len(pool)
        ids = [q['id'] for q in pool]
        if len(set(ids)) != len(ids):
            out.append('%s: a question twice in the pool' % mode)
        if len(pool) < MIN_POOL:
            out.append('%s: %d distinct questions, fewer than %d' % (mode, len(pool), MIN_POOL))
        steps = page.evaluate('m => TAW.pools()[m].map(q => { try { return TAW.steps(q); } catch (e) { return null; } })', mode)
        for q, st in zip(pool, steps):
            where = '%s %s' % (mode, q['id'][:60])
            if q['mode'] != mode:
                out.append('%s: in the wrong stage' % where)
            check_question(q, mode, out, where)
            if st is None:
                out.append('%s: the game could not build its working' % where)
            else:
                check_steps(q, st, out, where)
        by_id = {q['id']: q for q in pool}
        for seed in range(1, sessions + 1):
            s = page.evaluate('([s, m]) => TAW.buildSession(s, m)', [seed, mode])
            qs = s['questions']
            ex, ten = qs[0], qs[1:]
            where = '%s seed %d' % (mode, seed)
            if not ex.get('example') or len(ten) != 10 or any(x.get('example') for x in ten):
                out.append('%s: not a worked example then 10 questions' % where)
                continue
            if any(x['id'] not in by_id for x in qs):
                out.append('%s: a question not in the pool' % where)
            if len({x['id'] for x in qs}) != 11:
                out.append('%s: a question twice (or the example among the 10)' % where)
            ms = [measure(x) for x in ten]
            if any(ms[i] > ms[i + 1] for i in range(9)):
                out.append('%s: not easiest first: %s' % (where, ms))
            if [x['index'] for x in ten] != list(range(1, 11)):
                out.append('%s: numbered %s' % (where, [x['index'] for x in ten]))
            ff = [x['index'] for x in ten if x.get('findFirst')]
            want = [x['index'] for x in ten if x['missing']][:1]
            if ff != want:
                out.append('%s: the tap step on %s, the first with a missing length is %s' % (where, ff, want))
    return info


# ---------------------------------------------------------------- the drawing
NUM = r'(-?\d+(?:\.\d+)?)'


def path_points(d):
    """The M and L points and the A end points of an edge's d attribute, with the arcs' radii."""
    toks = re.findall(r'([MLA])([^MLAZ]*)', d)
    pts, radii = [], []
    for c, args in toks:
        v = [float(x) for x in re.findall(NUM, args)]
        if c in 'ML':
            pts.append(v[:2])
        else:
            radii.append(v[0])
            pts.append(v[5:7])
    return pts, radii


def check_drawn(page, out):
    svgs = page.evaluate("""() => { const P = TAW.pools(), out = {};
      for (const m in P) out[m] = P[m].map(q => TAW.draw(q, {})); return out; }""")
    pools = page.evaluate('TAW.pools()')
    n = 0
    for mode in MODES:
        for q, svg in zip(pools[mode], svgs[mode]):
            where = '%s %s' % (mode, q['id'][:60])
            n += 1
            k = float(re.search(r'data-k="([^"]+)"', svg).group(1))
            edges = re.findall(r'<path class="edge[^"]*" data-piece="(\d+)" d="([^"]+)"', svg)
            if len(edges) != len(q['shape']['path']):
                out.append('%s: %d sides drawn, %d in the data' % (where, len(edges), len(q['shape']['path'])))
                continue
            for i, d in edges:
                p = q['shape']['path'][int(i)]
                pts, radii = path_points(d)
                if p['t'] == 'L':
                    drawn = math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])
                    if abs(drawn - k * length(p)) > 1.0:
                        out.append('%s: side %s drawn %.1f px, %.2f m at %.2f px/m is %.1f' % (where, i, drawn, length(p), k, k * length(p)))
                else:
                    if any(abs(r - k * p['r']) > 1.0 for r in radii):
                        out.append('%s: arc %s drawn with radius %s px, %.2f m at %.2f px/m' % (where, i, radii, p['r'], k))
            for i, val in re.findall(r'<text class="lab[^"]*"[^>]*data-piece="(\d+)" data-val="([^"]+)"', svg):
                p = q['shape']['path'][int(i)]
                if p['lab'] is None or abs(float(val) - p['lab']) > EPS:
                    out.append('%s: side %s shows %s, labelled %s' % (where, i, val, p['lab']))
            shown = {int(i) for i in re.findall(r'<text class="lab[^"]*"[^>]*data-piece="(\d+)"', svg)}
            for i, p in enumerate(q['shape']['path']):
                if p['lab'] is not None and i not in shown:
                    out.append('%s: side %d labelled %s but drawn without its label' % (where, i, p['lab']))
                if p['lab'] is None and not p.get('ask') and i in shown:
                    out.append('%s: missing side %d drawn with a label' % (where, i))
            texts = dict(re.findall(r'<text class="lab dimlab[^"]*"[^>]*data-dim="(\d+)"[^>]*>([^<]*)</text>', svg))
            for j, d in enumerate(q['shape']['dims']):
                t = texts.get(str(j), '')
                if d['val'] is None and t != '?':
                    out.append('%s: the asked dimension %d shows %r, not ?' % (where, j, t))
                if d['val'] is not None and not re.search(r'(^|= )%s m$' % re.escape(('%g' % d['val'])), t):
                    out.append('%s: dimension %d shows %r, labelled %s' % (where, j, t, d['val']))
    return n


# ---------------------------------------------------------------- play
def open_page(pw, base, html, size):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.TAW && !!TAW.ui', timeout=10000)
    page.evaluate("""() => { TAW.ui.speed(0); window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


def ev_count(page, name):
    return page.evaluate('n => window.__ev.filter(e => e[0] === n).length', name)


def calc_shown(page):
    return page.evaluate("""() => { const w = document.getElementById('calcWrap'), c = document.querySelector('.maffs-calc');
        return { mounted: TAW.ui.calcMounted(), shown: !!c && !w.hidden && c.offsetParent !== null }; }""")


def tap_piece(page, i):
    page.evaluate("i => document.querySelector('#figure .hit[data-piece=\"' + i + '\"]').dispatchEvent(new MouseEvent('click', { bubbles: true }))", i)


def play_stage(page, mode, size, out, before, wrong_at=(2, 4, 5, 7)):
    """One stage, from its worked example to its results. `before`: the event count before the stage was started."""
    tag = '%s at %dx%d' % (mode, size[0], size[1])
    st = page.evaluate('TAW.ui.state()')
    if st != 'example':
        out.append('%s: the stage did not open on its worked example (%s)' % (tag, st))
        return
    taps = 0
    while page.evaluate('TAW.ui.state()') == 'example' and taps < 40:
        step = page.evaluate("document.querySelector('#feedback .explain').getAttribute('data-step')")
        page.click('#stepBtn')
        taps += 1
        nxt = page.evaluate("(document.querySelector('#feedback .explain') || {getAttribute: () => null}).getAttribute('data-step')")
        if page.evaluate('TAW.ui.state()') == 'example' and nxt != str(int(step) + 1):
            out.append('%s: a tap did not reveal exactly one step (%s -> %s)' % (tag, step, nxt))
    qa = page.evaluate("b => window.__ev.slice(b).filter(e => e[0] === 'question_answered').length", before)
    if qa:
        out.append('%s: the worked example logged %d question_answered' % (tag, qa))
    c = calc_shown(page)
    if (mode == 'stage-4') != c['shown'] or (mode != 'stage-4' and c['shown']):
        out.append('%s: the calculator %s' % (tag, 'is not shown' if mode == 'stage-4' else 'is shown'))
    if mode != 'stage-4' and c['mounted'] and not page.evaluate('window.__stage4played'):
        out.append('%s: the calculator is mounted before Stage 4 was played' % tag)
    badge = page.evaluate("document.getElementById('calcBadge').textContent")
    want = 'Scientific calculator required' if mode == 'stage-4' else 'Non-calculator'
    if badge != want:
        out.append('%s: the header badge reads %r, not %r' % (tag, badge, want))
    named_n = 0
    for k in range(10):
        q = page.evaluate('TAW.ui.question()')
        where = '%s q%d' % (tag, k + 1)
        if q['index'] != k + 1:
            out.append('%s: question %s shown' % (where, q['index']))
        state = page.evaluate('TAW.ui.state()')
        if mode == 'stage-1':
            if state != 'choose':
                out.append('%s: Stage 1 does not ask walk or cover first (%s)' % (where, state))
            else:
                kind = page.evaluate('TAW.kindOf(TAW.ui.question())')
                if k == 0:
                    n0 = page.evaluate('window.__ev.length')
                    page.click('#choice [data-kind="%s"]' % ('cover' if kind == 'walk' else 'walk'))
                    if page.evaluate('TAW.ui.state()') != 'choose' or page.evaluate('window.__ev.length') != n0:
                        out.append('%s: a wrong choice did not ask again, or logged an event' % where)
                    if page.evaluate("document.querySelector('#figure .pitch').getAttribute('data-anim')") != ('cover' if kind == 'walk' else 'walk').replace('cover', 'mow'):
                        out.append('%s: a wrong choice did not play its picture' % where)
                page.click('#choice [data-kind="%s"]' % kind)
        elif state == 'choose':
            out.append('%s: walk or cover asked after Stage 1' % where)
        state = page.evaluate('TAW.ui.state()')
        if q.get('findFirst'):
            if state != 'tap' or 'Click the side with missing information.' not in page.inner_text('#promptLine'):
                out.append('%s: the first question with a missing length does not open with the tap step' % where)
            else:
                labelled = [i for i, p in enumerate(q['shape']['path']) if p['lab'] is not None][0]
                tap_piece(page, labelled)
                if page.evaluate('TAW.ui.state()') != 'tap' or not page.evaluate("document.querySelectorAll('#figure .edge.cmp, #figure .dim.cmp').length"):
                    out.append('%s: a wrong tap did not highlight the sides to compare' % where)
                tap_piece(page, q['missing'][0])
                if page.evaluate('TAW.ui.state()') != 'asking':
                    out.append('%s: tapping the missing side did not go on' % where)
        elif state == 'tap':
            out.append('%s: a tap step on a question that is not the first with a missing length' % where)
        if page.evaluate('TAW.ui.state()') != 'asking':
            out.append('%s: no answer box (%s)' % (where, page.evaluate('TAW.ui.state()')))
            return
        box = '#ans4' if mode == 'stage-4' else '#ans'
        n0 = page.evaluate('window.__ev.length')
        fmt = ('%.1f' % q['key']) if q['dp'] else '%d' % round(q['key'])
        if k == 0:   # the right number with the wrong unit: the unit message, nothing marked
            page.evaluate("([b, v]) => { document.querySelector(b).value = v; }", [box, fmt])
            page.click('.unit-btn[data-unit="%s"]' % ('m' if q['unit'] == 'm2' else 'm2'))
            page.evaluate("document.getElementById('ansForm').requestSubmit()")
            if 'Check the unit' not in page.inner_text('#msg') or page.evaluate('window.__ev.length') != n0:
                out.append('%s: the right number with the wrong unit was marked, or got no unit message' % where)
        wrong = k in wrong_at
        val = fmt
        named = None
        if wrong:
            errs = [e for e in q['errors']]
            v = errs[0]['v'] if errs else q['key'] + 1
            whole = abs(v - round(v)) < EPS
            val = ('%.1f' % rnd(v, 1)) if q['dp'] else ('%d' % round(v) if whole else '%d' % (round(q['key']) + 1))
            if errs and (q['dp'] or whole):
                named = errs[0]['id']
                named_n += 1
        page.evaluate("([b, v]) => { document.querySelector(b).value = v; }", [box, val])
        page.click('.unit-btn[data-unit="%s"]' % q['unit'])
        page.evaluate("document.getElementById('ansForm').requestSubmit()")
        st = page.evaluate('TAW.ui.state()')
        sw = page.evaluate('document.documentElement.scrollWidth')
        if sw > size[0]:
            out.append('%s: sideways scroll (%d px wide at %d)' % (where, sw, size[0]))
        if wrong:
            if st != 'wrong':
                out.append('%s: a wrong answer was not marked wrong (%s)' % (where, st))
                return
            fb = page.evaluate("""() => { const f = document.querySelector('#feedback .fb');
                return f ? { line: !!f.querySelector('.fb-line'), pic: !!f.querySelector('.pitch[data-anim]'), steps: f.querySelectorAll('.steps li').length,
                  ans: (f.querySelector('.fb-ans') || {}).textContent, next: !!f.querySelector('.fb-next button') } : null; }""")
            if not fb or not (fb['line'] and fb['pic'] and fb['steps'] and fb['next']) or fb['ans'] != fmt + ' ' + ('m²' if q['unit'] == 'm2' else 'm'):
                out.append('%s: the wrong-answer screen is missing its picture, line, working, answer or Next: %s' % (where, fb))
            # A named slip: its own line, the worked line for the first three in a session, then the nudge.
            got = page.evaluate("""() => { const l = document.querySelector('#feedback .fb-line');
                return l ? [l.getAttribute('data-err'), l.getAttribute('data-help')] : [null, null]; }""")
            want_help = ('example' if named_n <= 3 else 'nudge') if named else 'rule'
            if got != [named, want_help]:
                out.append('%s: the wrong-answer line is %s, expected %s' % (where, got, [named, want_help]))
            page.click('#feedback .fb-next button')
        else:
            if st != 'right':
                out.append('%s: the key %s %s was not marked right (%s; %r)' % (where, val, q['unit'], st, page.inner_text('#msg')))
                return
            page.wait_for_function("TAW.ui.state() !== 'right'", timeout=8000)
    if page.evaluate('TAW.ui.state()') != 'done':
        out.append('%s: the results screen did not show' % tag)
        return
    evs = page.evaluate('b => window.__ev.slice(b)', before)
    qas = [e for e in evs if e[0] == 'question_answered']
    if len(qas) != 10 or any(e[1].get('mode') != mode for e in qas):
        out.append('%s: %d question_answered, modes %s' % (tag, len(qas), sorted({e[1].get('mode') for e in qas})))
    done = [e for e in evs if e[0] == 'game_completed']
    if len(done) != 1 or done[0][1].get('mode') != mode:
        out.append('%s: game_completed %s' % (tag, done))
    sub = page.evaluate('window.__sub')
    if not sub or sub[-1][1] != mode:
        out.append('%s: the score went to %s, not the stage\'s board' % (tag, sub[-1][1] if sub else None))
    nxt = page.evaluate("(() => { const b = document.getElementById('nextStageBtn'); return b.hidden ? null : b.textContent; })()")
    want = 'Next: Stage %d' % (STAGE_N[mode] + 1) if mode != 'stage-4' else None
    if nxt != want:
        out.append('%s: the results offer %r, not %r' % (tag, nxt, want))
    if mode == 'stage-4':
        page.evaluate('window.__stage4played = true')


def play(page, size, out):
    page.click('.mode-btn[data-mode="stage-1"]')
    before = page.evaluate('window.__ev.length')
    page.click('#startBtn')
    for mode in MODES:
        play_stage(page, mode, size, out, before)
        if mode != 'stage-4':
            if page.evaluate("document.getElementById('nextStageBtn').hidden"):
                return
            before = page.evaluate('window.__ev.length')
            page.click('#nextStageBtn')
    # Back to Stage 2 after Stage 4: the calculator hides again.
    page.click('#againBtn')
    page.click('.mode-btn[data-mode="stage-2"]')
    page.click('#startBtn')
    if calc_shown(page)['shown']:
        out.append('at %dx%d: the calculator still shows in Stage 2 after Stage 4' % size)


def static_checks(html, out):
    if 'name="robots" content="noindex"' not in html:
        out.append('the page is not noindex (the game is unlisted)')
    if not re.search(r'<script type="application/json" id="maffs-calc-stages">\{"stage-1": "not allowed", "stage-2": "not allowed", '
                     r'"stage-3": "not allowed", "stage-4": "scientific"\}</script>', html):
        out.append('the calculator stage map is not Stages 1-3 not allowed, Stage 4 scientific')
    decl = re.search(r'MaffsLevel\.resolve\(\{(.*?)\}\)', html, re.S)
    if not decl or any("'%s'" % m not in decl.group(1) for m in MODES):
        out.append('MaffsLevel.resolve does not declare the boards %s' % MODES)


def guarded(out, what, f):
    try:
        f()
    except Exception as e:  # noqa: BLE001 - any exception here is a finding
        out.append('%s threw: %s' % (what, str(e).splitlines()[0][:200]))


def check(html, out, engine=True, drawn=False, sizes=(), sessions=SESSIONS):
    from playwright.sync_api import sync_playwright
    static_checks(html, out)
    proc, base = bc.start_stub_server()
    info = {}
    try:
        with sync_playwright() as pw:
            if engine or drawn:
                br, page, errs = open_page(pw, base, html, (1280, 800))
                if engine:
                    guarded(out, 'the engine checks', lambda: info.update(check_engine(page, out, sessions)))
                if drawn:
                    guarded(out, 'the drawing checks', lambda: info.update({'drawn': check_drawn(page, out)}))
                out.extend('page error: ' + e for e in errs)
                br.close()
            for size in sizes:
                br, page, errs = open_page(pw, base, html, size)
                guarded(out, 'play at %dx%d' % size, lambda: play(page, size, out))
                out.extend('page error at %dx%d: %s' % (size[0], size[1], e) for e in errs)
                info.setdefault('played', []).append('%dx%d' % size)
                br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, [(old, new), ...], what it needs to run, a pattern its finding must match). Every old text occurs
# exactly once in the page. The l + w key needs the filter off too: it equals the "two sides only" slip, so the filter
# alone would take every such question out of the pool (and nothing wrong would be served).
PLANTS = [
    ('a key computed as l + w (a rectangle\'s perimeter)',
     [("    if (ask === 'P') exact = H.perimeter(sh);", "    if (ask === 'P') exact = sh.fam === 'rect' ? H.perimeter(sh) / 2 : H.perimeter(sh);"),
      ("    if (H.errorIsKey(q)) return false;\n", "    if (H.errorIsKey(q) && q.fam !== 'rect') return false;\n")], 'engine', r':rect:P:.*: key \S+, recomputed'),
    ('a Stage 3 question whose missing length the drawing cannot determine',
     [("[[2, 5], [4, 1], [0, 3]].forEach", "[[2, 5], [4, 1], [0, 2]].forEach"),
      ("    return q.missing.every(function (i) {", "    return q.fam === 'L' || q.missing.every(function (i) {")], 'engine', r'is not determined by the drawing'),
    ('a named wrong answer equal to the key (the filter cut)',
     [("    if (H.errorIsKey(q)) return false;\n", "")], 'engine', r'the named slip \w+ gives the key'),
    ('a Stage 1 question with a missing length',
     [("make('stage-1', H.F.L(W, Hf, a, h2, []), k, n++)", "make('stage-1', H.F.L(W, Hf, a, h2, [2]), k, n++)"),
      ("    if (!H.lone(q.shape) && !H.BACK[q.ask] && q.missing.length !== S.missing) return false;\n", "")], 'engine',
     r'stage-1 .*1 lengths missing; stage 1 asks for 0'),
    ('the worked example logging an event',
     [("  function askExample() {\n    state = 'example';\n",
       "  function askExample() {\n    state = 'example';\n    ev('question_answered', { game_slug: SLUG, level: level, mode: q.mode, question_index: 0, correct: true });\n")], 'play',
     r'the worked example logged'),
    ('a reversed order (hardest first)',
     [("if (a[i] !== b[i]) return a[i] - b[i];", "if (a[i] !== b[i]) return b[i] - a[i];")], 'engine', r'not easiest first'),
    ('the calculator mounted at Stage 2',
     [("    var on = H.STAGES[mode].calc === 'scientific';", "    var on = H.STAGES[mode].calc === 'scientific' || mode === 'stage-2';")], 'play',
     r'stage-2 .*the calculator'),
]


def selftest(html):
    ok = True
    for what, edits, kind, want in PLANTS:
        planted = html
        bad = False
        for old, new in edits:
            if planted.count(old) != 1:
                bad = True
                break
            planted = planted.replace(old, new)
        if bad:
            print('  self-test %-62s *** CANNOT PLANT ***' % what)
            ok = False
            continue
        got = []
        check(planted, got, engine=kind == 'engine', sizes=[(1280, 800)] if kind == 'play' else [], sessions=8)
        hit = [g for g in got if re.search(want, g)]
        ok = ok and bool(hit)
        print('  self-test %-62s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***' + (' (other findings: %s)' % got[0][:80] if got else '')))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', choices=['1', '2', '3', '4'], help='one of the four parts CI runs side by side (default: all)')
    ap.add_argument('--sessions', type=int, default=SESSIONS)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    part = args.part
    out = []
    info = {}
    if part in (None, '1', '2', '3'):
        info = check(html, out, engine=part in (None, '1'), drawn=part in (None, '2'),
                     sizes=SIZES if part in (None, '3') else [], sessions=args.sessions)
    if 'pools' in info:
        print('%s: pools %s; %d sessions a stage' % (SLUG, info['pools'], args.sessions))
    if 'drawn' in info:
        print('%s: %d questions drawn and read back' % (SLUG, info['drawn']))
    if 'played' in info:
        print('%s: every stage played at %s' % (SLUG, ', '.join(info['played'])))
    ok = True
    if part in (None, '4'):
        ok = selftest(html)
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
