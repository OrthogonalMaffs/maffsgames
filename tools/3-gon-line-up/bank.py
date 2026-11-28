#!/usr/bin/env python3
"""3-gon Line-up: question bank generator (tools/three-gon-line-up/bank.py).

48 items, 12 per stage. Deterministic (fixed seed), standard library only.
Every claim the game makes is checked here from the triangles themselves:
  Stage 1  lattice triangles on squared paper; congruence = equal sorted squared side lengths (exact integers).
  Stages 2-4  marked facts (sides in cm, angles in degrees); a triangle is solved from its facts and two suspects
           are "proven congruent" only when both carry a full criterion (SSS, SAS, ASA, RHS) and the solved
           side lengths agree. Angles only (AAA) and an ambiguous two-sides-and-a-non-included-angle (SSA)
           prove nothing, and every SSA decoy is checked to have two genuine solutions, so it can never be
           secretly determined.
Run: python -X utf8 -I tools/3-gon-line-up/bank.py --out <file>  -> one item per line (JSON), the count, the
failure count (must be 0) and the sha256 of those lines.
"""
import json, math, random, sys, itertools, hashlib

R = random.Random(20261127)
FAIL = []
TOL = 1e-9

def fail(msg):
    FAIL.append(msg)

# ------------------------------------------------------------------ stage 1: squared paper
OPS = {  # the eight symmetries of the square grid; det -1 = reflection
    'rot0': (1, 0, 0, 1), 'rot90': (0, -1, 1, 0), 'rot180': (-1, 0, 0, -1), 'rot270': (0, 1, -1, 0),
    'refl_x': (1, 0, 0, -1), 'refl_y': (-1, 0, 0, 1), 'refl_diag': (0, 1, 1, 0), 'refl_anti': (0, -1, -1, 0),
}
REFLECTIONS = {'refl_x', 'refl_y', 'refl_diag', 'refl_anti'}
CELL = 8  # each suspect sits on an 8 x 8 grid

def apply(op, pts):
    a, b, c, d = OPS[op]
    return [(a * x + b * y, c * x + d * y) for x, y in pts]

def norm(pts):
    mx = min(p[0] for p in pts); my = min(p[1] for p in pts)
    return [(x - mx, y - my) for x, y in pts]

def fits(pts):
    return all(0 <= x <= CELL and 0 <= y <= CELL for x, y in pts)

def area2(p):
    (x1, y1), (x2, y2), (x3, y3) = p
    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

def sq_sides(p):
    return tuple(sorted((p[i][0] - p[j][0]) ** 2 + (p[i][1] - p[j][1]) ** 2 for i, j in ((0, 1), (1, 2), (0, 2))))

def scalene(p):
    s = sq_sides(p)
    return len(set(s)) == 3

def similar_ratio(p, q):
    a, b = sq_sides(p), sq_sides(q)
    r = [b[i] / a[i] for i in range(3)]
    return r[0] if abs(r[0] - r[1]) < TOL and abs(r[1] - r[2]) < TOL else None

def rand_tri(maxc):
    while True:
        p = [(R.randint(0, maxc), R.randint(0, maxc)) for _ in range(3)]
        if area2(p) >= 4 and scalene(p):
            return norm(p)

def stage1():
    items = []
    twin_ops = ['refl_x', 'refl_y', 'refl_diag', 'refl_anti', 'refl_x', 'refl_diag',   # 6 reflected twins
                'rot90', 'rot180', 'rot270', 'rot90', 'rot270', 'rot180']             # 6 rotated twins
    R.shuffle(twin_ops)
    n = 0
    while n < 12:
        base = rand_tri(4)
        if sq_sides(base) in [sq_sides(next(x['pts'] for x in it['suspects'] if x['role'] == 'culprit')) for it in items]:
            continue
        op = twin_ops[n]
        twin = norm(apply(op, base))
        if sorted(twin) == sorted(base):
            continue
        sus = [('culprit', base, 'rot0'), ('twin', twin, op)]
        big = norm(apply(R.choice(list(OPS)), [(2 * x, 2 * y) for x, y in base]))
        if not fits(big):
            continue
        sus.append(('enlarged', big, 'x2'))
        used = set()
        ok = True
        for k in ('one_square_out', 'one_square_out'):
            for _ in range(200):
                v = R.randrange(3)
                if v in used:
                    continue
                dx, dy = R.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                q = list(base); q[v] = (q[v][0] + dx, q[v][1] + dy)
                q = norm(apply(R.choice(list(OPS)), q))
                if area2(q) >= 2 and fits(q) and scalene(q):
                    used.add(v); sus.append((k, q, 'moved'))
                    break
            else:
                ok = False
        if not ok:
            continue
        sus.append(('stranger', norm(apply(R.choice(list(OPS)), rand_tri(5))), 'other'))
        # exactly one congruent pair, and nothing but the enlargement similar to the culprit
        pairs = [(i, j) for i, j in itertools.combinations(range(6), 2) if sq_sides(sus[i][1]) == sq_sides(sus[j][1])]
        if pairs != [(0, 1)]:
            continue
        if any(similar_ratio(base, s[1]) for s in sus[3:]):
            continue
        if any(not fits(s[1]) for s in sus):
            continue
        order = list(range(6)); R.shuffle(order)
        lineup = [None] * 6
        for pos, idx in enumerate(order):
            k, pts, how = sus[idx]
            lineup[pos] = {'n': pos + 1, 'role': k, 'pts': pts, 'how': how}
        pair = sorted(p['n'] for p in lineup if p['role'] in ('culprit', 'twin'))
        items.append({'id': 's1-%02d' % (n + 1), 'stage': 1, 'suspects': lineup, 'pair': pair,
                      'twin_move': 'reflection' if op in REFLECTIONS else 'rotation', 'twin_op': op})
        n += 1
    # the witness's own line-up: one item whose answer is 2 and 6
    it = items[0]
    if it['pair'] != [2, 6]:
        a, b = it['pair']
        mp = {a: 2, b: 6}
        others = [s for s in it['suspects'] if s['n'] not in (a, b)]
        rest = [p for p in range(1, 7) if p not in (2, 6)]
        for s, p in zip(others, rest):
            mp[s['n']] = p
        for s in it['suspects']:
            s['n'] = mp[s['n']]
        it['suspects'].sort(key=lambda s: s['n'])
        it['pair'] = [2, 6]
    return items

# ------------------------------------------------------------------ stages 2-4: marked facts
# A fact is ('side', i, j, value) or ('angle', i, value) on vertices 0, 1, 2.
def solve(facts):
    """Side lengths (a=BC opposite 0, b=CA opposite 1, c=AB opposite 2) from a full criterion, else None."""
    sides = {frozenset((f[1], f[2])): f[3] for f in facts if f[0] == 'side'}
    angs = {f[1]: f[2] for f in facts if f[0] == 'angle'}
    kind = criterion(facts)
    if kind is None:
        return None
    def opp(v):  # side opposite vertex v
        return frozenset({0, 1, 2} - {v})
    if kind == 'SSS':
        L = {v: sides[opp(v)] for v in range(3)}
    elif kind in ('SAS', 'RHS'):
        if kind == 'SAS':
            v = next(iter(angs)); s1, s2 = [sides[e] for e in sides]
            third = math.sqrt(s1 * s1 + s2 * s2 - 2 * s1 * s2 * math.cos(math.radians(angs[v])))
            L = {}
            for w in range(3):
                L[w] = third if w == v else sides[opp(w)]
        else:
            v = next(iter(angs))  # right angle; hypotenuse opposite it
            h = sides[opp(v)]
            leg = [sides[e] for e in sides if e != opp(v)][0]
            other = math.sqrt(h * h - leg * leg)
            L = {v: h}
            for w in range(3):
                if w != v:
                    L[w] = sides[opp(w)] if opp(w) in sides else other
    elif kind in ('ASA', 'AAS'):
        A = dict(angs); w = ({0, 1, 2} - set(A)).pop(); A[w] = 180 - sum(angs.values())
        e = next(iter(sides)); known = sides[e]; v_opp = ({0, 1, 2} - set(e)).pop()
        k = known / math.sin(math.radians(A[v_opp]))
        L = {v: k * math.sin(math.radians(A[v])) for v in range(3)}
    return tuple(sorted(L.values()))

def criterion(facts):
    sides = [frozenset((f[1], f[2])) for f in facts if f[0] == 'side']
    angs = {f[1]: f[2] for f in facts if f[0] == 'angle'}
    if len(sides) == 3 and not angs:
        return 'SSS'
    if len(sides) == 2 and len(angs) == 1:
        v = next(iter(angs))
        between = all(v in e for e in sides)
        if between:
            return 'SAS'
        if angs[v] == 90 and frozenset({0, 1, 2} - {v}) in sides:
            return 'RHS'
        return None  # SSA
    if len(sides) == 1 and len(angs) == 2:
        e = sides[0]
        if set(angs) == set(e):
            return 'ASA'
        return 'AAS'  # Jon, 28 Nov 2026: in the bank, answered as ASA once the third angle is found
    return None

def ssa_ambiguous(facts):
    """Two sides and a non-included, non-right angle: true when two different triangles fit."""
    angs = {f[1]: f[2] for f in facts if f[0] == 'angle'}
    v = next(iter(angs)); A = math.radians(angs[v])
    sides = {frozenset((f[1], f[2])): f[3] for f in facts if f[0] == 'side'}
    a = sides.get(frozenset({0, 1, 2} - {v}))
    b = [sides[e] for e in sides if v in e][0]
    if not (a is not None and angs[v] < 90 and b * math.sin(A) < a - TOL and a < b - TOL):
        return False
    # both triangles must be readable when drawn: no angle under 15 degrees in either
    for pick in (0, 1):
        L = full_sides(facts, pick)
        x, y, z = L[0], L[1], L[2]
        for p, q, r in ((x, y, z), (y, z, x), (z, x, y)):
            if math.degrees(math.acos(max(-1, min(1, (q * q + r * r - p * p) / (2 * q * r))))) < 15:
                return False
    return True

def valid_facts(f):
    """A full criterion that describes a real triangle (angles positive, legs shorter than hypotenuse)."""
    k = criterion(f)
    if k is None:
        return True
    try:
        L = solve(f)
    except ValueError:
        return False
    if k in ('ASA', 'AAS') and sum(x[2] for x in f if x[0] == 'angle') >= 160:
        return False
    return all(x > 0.5 for x in L) and valid_tri(L)

def rule_answer(kind):
    """The button a student presses for a criterion: AAS is ASA once the third angle is found."""
    return 'ASA' if kind == 'AAS' else kind

def proven_equal(f1, f2):
    s1, s2 = solve(f1), solve(f2)
    return s1 is not None and s2 is not None and all(abs(x - y) < 1e-7 for x, y in zip(s1, s2))

def shape_from_sides(L):
    """Vertex coordinates for side lengths L[v] (opposite v): A at origin, B on the x axis."""
    a, b, c = L[0], L[1], L[2]
    x = (b * b + c * c - a * a) / (2 * c)
    y = math.sqrt(max(b * b - x * x, 0))
    return [(0.0, 0.0), (c, 0.0), (x, y)]

def full_sides(facts, ssa_pick=0):
    """Side lengths by vertex for drawing (any fact set, SSA and AAA included)."""
    s = solve(facts)
    sides = {frozenset((f[1], f[2])): f[3] for f in facts if f[0] == 'side'}
    angs = {f[1]: f[2] for f in facts if f[0] == 'angle'}
    if s is not None:
        # recover per-vertex lengths consistently
        crit = criterion(facts)
        if crit == 'SSS':
            return {v: sides[frozenset({0, 1, 2} - {v})] for v in range(3)}
        if crit in ('ASA', 'AAS'):
            A = dict(angs); w = ({0, 1, 2} - set(A)).pop(); A[w] = 180 - sum(angs.values())
            e = next(iter(sides)); v_opp = ({0, 1, 2} - set(e)).pop()
            k = sides[e] / math.sin(math.radians(A[v_opp]))
            return {v: k * math.sin(math.radians(A[v])) for v in range(3)}
        if crit == 'SAS':
            v = next(iter(angs)); s1, s2 = [sides[e] for e in sides]
            third = math.sqrt(s1 * s1 + s2 * s2 - 2 * s1 * s2 * math.cos(math.radians(angs[v])))
            return {w: (third if w == v else sides[frozenset({0, 1, 2} - {w})]) for w in range(3)}
        if crit == 'RHS':
            v = next(iter(angs)); h = sides[frozenset({0, 1, 2} - {v})]
            out = {v: h}
            leg = [x for e, x in sides.items() if e != frozenset({0, 1, 2} - {v})][0]
            for w in range(3):
                if w != v:
                    e = frozenset({0, 1, 2} - {w})
                    out[w] = sides[e] if e in sides else math.sqrt(h * h - leg * leg)
            return out
    if len(angs) == 3:  # AAA: draw at a size of 6 for the longest side
        k = 6 / max(math.sin(math.radians(x)) for x in angs.values())
        return {v: k * math.sin(math.radians(angs[v])) for v in range(3)}
    # SSA: angle at v, adjacent side b, opposite side a; two solutions for the third side
    v = next(iter(angs)); A = math.radians(angs[v])
    a = sides[frozenset({0, 1, 2} - {v})]
    adj_e = [e for e in sides if v in e][0]; b = sides[adj_e]
    disc = math.sqrt(a * a - (b * math.sin(A)) ** 2)
    c = b * math.cos(A) + (disc if ssa_pick == 0 else -disc)
    w_b = ({0, 1, 2} - adj_e).pop()  # vertex opposite the adjacent side b
    out = {v: a, w_b: b}
    out[({0, 1, 2} - {v, w_b}).pop()] = c
    return out

def drawing(facts, op, distort=0.0, ssa_pick=0):
    L = full_sides(facts, ssa_pick)
    pts = shape_from_sides(L)
    if distort:
        pts = [(x + R.uniform(-distort, distort) * 3, y + R.uniform(-distort, distort) * 3) for x, y in pts]
    a, b, c, d = OPS[op]
    pts = [(a * x + b * y, c * x + d * y) for x, y in pts]
    mx = min(p[0] for p in pts); my = min(p[1] for p in pts)
    pts = [(x - mx, y - my) for x, y in pts]
    sc = 1.0 / max(max(p[0] for p in pts), max(p[1] for p in pts))
    return [(x * sc, y * sc) for x, y in pts]

def fit(unit, facts):
    """Scale the unit shape as large as its labels allow (6 down to 3.5 units), centred in VIEW.
    Returns (points, labels) or (None, None)."""
    cxv = VIEW[0] + VIEW[2] / 2; cyv = VIEW[1] + VIEW[3] / 2
    for sc in (6.8, 6.4, 6.0, 5.6, 5.2, 4.8):
        P = [(x * sc, y * sc) for x, y in unit]
        mx = (min(p[0] for p in P) + max(p[0] for p in P)) / 2; my = (min(p[1] for p in P) + max(p[1] for p in P)) / 2
        P = [(round(x - mx + cxv, 3), round(y - my + cyv, 3)) for x, y in P]
        if not all(VIEW[0] + 0.3 <= x <= VIEW[0] + VIEW[2] - 0.3 and VIEW[1] + 0.3 <= y <= VIEW[1] + VIEW[3] - 0.3 for x, y in P):
            continue
        labels = place_labels(P, facts)
        if labels is not None:
            return P, labels
    return None, None

def has_right(facts):
    return any(f[0] == 'angle' and f[2] == 90 for f in facts)


# ------------------------------------------------------------------ labels: placed and proven clear here, never by the page
# The page draws each suspect in an SVG whose viewBox is VIEW (drawing units), with label text at FONT units,
# so a label that clears every edge here clears it at every screen size.
VIEW = (-2.0, -2.0, 10.0, 10.0)   # x, y, width, height; the triangle itself spans 0..6
FONT = 0.75                       # label font size in drawing units: 12.4 px on a 165 px phone cell
CHAR = 0.62 * FONT                # conservative width of one character
GAP = 0.12                        # minimum clearance between a label box and any edge or other label
ARC = 0.4                         # the page's angle arc radius at a marked vertex
SQUARE = 0.45                     # the page's right-angle square side

def label_text(f):
    return ('%d cm' % f[3]) if f[0] == 'side' else ('%d°' % f[2])

ANGLE_FONT = 0.68                 # angle labels: 11.2 px on a 165 px phone cell

def box_at(cx, cy, text):
    f = ANGLE_FONT if text.endswith('\u00b0') else FONT
    w = 0.62 * f * len(text) + 0.2; h = 1.1 * f
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)

def seg_box_dist(p, q, b):
    """Shortest distance from segment pq to box b (0 if they touch)."""
    x0, y0, x1, y1 = b
    def clamp(v, lo, hi): return max(lo, min(hi, v))
    best = float('inf')
    for t in [i / 40 for i in range(41)]:
        x = p[0] + (q[0] - p[0]) * t; y = p[1] + (q[1] - p[1]) * t
        dx = max(x0 - x, 0, x - x1); dy = max(y0 - y, 0, y - y1)
        best = min(best, math.hypot(dx, dy))
    # box corners to the segment, for long boxes beside short edges
    for cx, cy in ((x0, y0), (x0, y1), (x1, y0), (x1, y1)):
        vx, vy = q[0] - p[0], q[1] - p[1]
        t = clamp(((cx - p[0]) * vx + (cy - p[1]) * vy) / (vx * vx + vy * vy), 0, 1)
        best = min(best, math.hypot(cx - p[0] - t * vx, cy - p[1] - t * vy))
    return best

def boxes_clear(a, b):
    return a[2] + GAP <= b[0] or b[2] + GAP <= a[0] or a[3] + GAP <= b[1] or b[3] + GAP <= a[1]

def inside_tri(pt, P):
    def s(a, b, c): return (a[0] - c[0]) * (b[1] - c[1]) - (b[0] - c[0]) * (a[1] - c[1])
    d1, d2, d3 = s(pt, P[0], P[1]), s(pt, P[1], P[2]), s(pt, P[2], P[0])
    return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))

def in_view(b):
    x, y, w, h = VIEW
    return b[0] >= x and b[1] >= y and b[2] <= x + w and b[3] <= y + h


def seg_pt_dist(p, q, c):
    vx, vy = q[0] - p[0], q[1] - p[1]
    t = max(0, min(1, ((c[0] - p[0]) * vx + (c[1] - p[1]) * vy) / (vx * vx + vy * vy)))
    return math.hypot(c[0] - p[0] - t * vx, c[1] - p[1] - t * vy)

def belongs(P, f, c):
    """A label centre c is unmistakably its fact's: an angle label is nearer its own vertex than any other and
    within 45% of the shorter side at that vertex; a side label is nearer its own edge than either other edge."""
    if f[0] == 'angle':
        v = f[1]; dv = math.hypot(c[0] - P[v][0], c[1] - P[v][1])
        near = min(math.hypot(P[v][0] - P[j][0], P[v][1] - P[j][1]) for j in range(3) if j != v)
        others = [math.hypot(c[0] - P[j][0], c[1] - P[j][1]) for j in range(3) if j != v]
        return dv < min(others) - 0.3 and dv <= 0.55 * near
    own = seg_pt_dist(P[f[1]], P[f[2]], c)
    rest = [seg_pt_dist(P[i], P[j], c) for i, j in ((0, 1), (1, 2), (0, 2)) if {i, j} != {f[1], f[2]}]
    return own < min(rest) - 0.3

def pt_box_dist(p, b):
    dx = max(b[0] - p[0], 0, p[0] - b[2]); dy = max(b[1] - p[1], 0, p[1] - b[3])
    return math.hypot(dx, dy)

def clear_of_marks(bx, P, facts):
    """A label box stays outside every arc (radius ARC) and every right-angle square (reach SQUARE*sqrt2) the page draws."""
    for f in facts:
        if f[0] == 'angle':
            reach = SQUARE * math.sqrt(2) if f[2] == 90 else ARC
            if pt_box_dist(P[f[1]], bx) < reach + GAP:
                return False
    return True

def place_labels(P, facts):
    """Label centres for each fact, or None if any label cannot be placed clear.
    Side labels sit outside the edge on its outward normal; angle labels sit inside the angle on its bisector."""
    edges = [(P[0], P[1]), (P[1], P[2]), (P[2], P[0])]
    cx = sum(p[0] for p in P) / 3; cy = sum(p[1] for p in P) / 3
    placed = []; rights = []
    for f in facts:
        if f[0] == 'angle' and f[2] == 90:
            rights.append({'type': 'right', 'vertex': f[1]}); continue
        text = label_text(f); ok = None
        if f[0] == 'side':
            a, b = P[f[1]], P[f[2]]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            nx, ny = -(b[1] - a[1]), b[0] - a[0]; L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
            if (mx - cx) * nx + (my - cy) * ny < 0:
                nx, ny = -nx, -ny
            for k in range(3, 40):
                d = k * 0.1
                bx = box_at(mx + nx * d, my + ny * d, text)
                if all(seg_box_dist(p, q, bx) >= GAP for p, q in edges) and in_view(bx) and clear_of_marks(bx, P, facts) \
                        and all(boxes_clear(bx, o[1]) for o in placed) and belongs(P, f, ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2)):
                    ok = bx; break
        else:
            v = P[f[1]]; o = [P[j] for j in range(3) if j != f[1]]
            u1 = ((o[0][0] - v[0]), (o[0][1] - v[1])); u2 = ((o[1][0] - v[0]), (o[1][1] - v[1]))
            l1, l2 = math.hypot(*u1), math.hypot(*u2)
            bx_, by_ = u1[0] / l1 + u2[0] / l2, u1[1] / l1 + u2[1] / l2; lb = math.hypot(bx_, by_)
            bx_, by_ = bx_ / lb, by_ / lb
            for k in range(6, 60):
                d = k * 0.1
                bx = box_at(v[0] + bx_ * d, v[1] + by_ * d, text)
                corners = ((bx[0], bx[1]), (bx[0], bx[3]), (bx[2], bx[1]), (bx[2], bx[3]))
                if all(inside_tri(c, P) for c in corners) and all(seg_box_dist(p, q, bx) >= GAP for p, q in edges) \
                        and clear_of_marks(bx, P, facts) \
                        and all(boxes_clear(bx, o[1]) for o in placed) and belongs(P, f, ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2)):
                    ok = bx; break
            # no fallback outside the vertex: a label there reads as the exterior angle
        if ok is None:
            return None
        placed.append((f, ok))
    return rights + [{'type': f[0], 'fact': list(f), 'text': label_text(f), 'x': round((b[0] + b[2]) / 2, 3),
                      'y': round((b[1] + b[3]) / 2, 3), 'box': [round(v, 3) for v in b]} for f, b in placed]

def valid_tri(L):
    a, b, c = L
    return a + b > c + 0.5 and b + c > a + 0.5 and a + c > b + 0.5

def min_angle_ok(facts):
    L = full_sides(facts)
    a, b, c = L[0], L[1], L[2]
    for x, y, z in ((a, b, c), (b, c, a), (c, a, b)):
        cosx = (y * y + z * z - x * x) / (2 * y * z)
        if math.degrees(math.acos(max(-1, min(1, cosx)))) < 20:
            return False
    return True

def make_culprit(kind):
    for _ in range(10000):
        if kind == 'SSS':
            s = sorted(R.sample(range(4, 13), 3))
            if s[0] + s[1] <= s[2] + 1:
                continue
            f = [('side', 1, 2, s[0]), ('side', 0, 2, s[1]), ('side', 0, 1, s[2])]
        elif kind == 'SAS':
            p, q = R.sample(range(5, 13), 2); ang = R.choice(range(35, 121, 5))
            f = [('side', 0, 1, p), ('side', 0, 2, q), ('angle', 0, ang)]
        elif kind == 'ASA':
            a1, a2 = R.choice(range(35, 86, 5)), R.choice(range(35, 86, 5))
            if a1 == a2 or a1 + a2 > 140:
                continue
            f = [('angle', 0, a1), ('angle', 1, a2), ('side', 0, 1, R.choice(range(5, 13)))]
        elif kind == 'AAS':
            a1, a2 = R.choice(range(35, 86, 5)), R.choice(range(35, 86, 5))
            if a1 == a2 or a1 + a2 > 140:
                continue
            f = [('angle', 0, a1), ('angle', 1, a2), ('side', 1, 2, R.choice(range(5, 13)))]  # BC: not between A and B
        elif kind == 'RHS':
            h = R.choice(range(9, 16)); leg = R.choice(range(4, h - 2))
            f = [('angle', 2, 90), ('side', 0, 1, h), ('side', 1, 2, leg)]
        if min_angle_ok(f):
            return f
    raise RuntimeError(kind)

def one_differs(f):
    g = list(f); i = R.randrange(len(g)); x = g[i]
    if x[0] == 'side':
        g[i] = (x[0], x[1], x[2], x[3] + R.choice([-1, 1, 2]))
    else:
        if x[2] == 90:
            return one_differs(f)
        g[i] = (x[0], x[1], x[2] + R.choice([-5, 5, 10]))
    return g

def angles_only(f):
    angs = {x[1]: x[2] for x in f if x[0] == 'angle'}
    w = ({0, 1, 2} - set(angs)).pop(); angs[w] = 180 - sum(angs.values())
    return [('angle', v, angs[v]) for v in range(3)]

def angle_moved(f):
    """SAS -> same two sides and angle, the angle moved to a vertex where it is not between them (SSA)."""
    p = [x for x in f if x[0] == 'side']; ang = [x for x in f if x[0] == 'angle'][0][2]
    # sides AB = p0 (0-1), AC = p1 (0-2); put the angle at B: adjacent sides there are AB and BC
    # culprit: AB = p, AC = q, angle at A. Decoy: the same AB, AC and angle, but the angle at C,
    # where it sits between CA and CB, so it is not between the two marked sides.
    return [('side', 0, 1, p[0][3]), ('side', 0, 2, p[1][3]), ('angle', 2, ang)]

USED_CULPRITS = set()

def suspects_for(kind):
    while True:
        cul = make_culprit(kind)
        key = tuple(sorted(map(str, cul)))
        if key in USED_CULPRITS:
            continue
        decoys = []
        decoys.append(('drawn_alike', one_differs(cul), 'alike'))
        decoys.append(('one_differs', one_differs(cul), 'plain'))
        if kind in ('ASA', 'AAS'):
            decoys.append(('angles_only', angles_only(cul), 'plain'))
        elif kind == 'SAS':
            m = angle_moved(cul)
            if criterion(m) is not None or not ssa_ambiguous(m):
                continue
            decoys.append(('angle_moved', m, 'plain'))
        else:
            decoys.append(('one_differs', one_differs(cul), 'plain'))
        other = make_culprit(R.choice(['SSS', 'SAS', 'ASA', 'RHS']))
        decoys.append(('stranger', other, 'plain'))
        sus = [('culprit', cul, 'plain'), ('twin', cul, 'twin')] + decoys
        sus_key = key
        facts = [s[1] for s in sus]
        if not all(valid_facts(f) for f in facts) or not all(min_angle_ok(f) for f in facts if criterion(f)):
            continue
        pairs = [(i, j) for i, j in itertools.combinations(range(6), 2) if proven_equal(facts[i], facts[j])]
        if pairs != [(0, 1)]:
            continue
        # no decoy may repeat the culprit's facts exactly
        if any(sorted(map(str, f)) == sorted(map(str, cul)) for f in facts[2:]):
            continue
        USED_CULPRITS.add(sus_key)
        return sus

def lay_out(sus):
    order = list(range(6)); R.shuffle(order)
    out = []
    for pos, idx in enumerate(order):
        role, facts, style = sus[idx]
        op = R.choice(list(OPS)) if role != 'culprit' else 'rot0'
        if role == 'twin':
            op = R.choice(['refl_x', 'refl_y', 'rot90', 'rot180', 'refl_diag', 'rot270'])
        out.append({'n': pos + 1, 'role': role, 'facts': [list(f) for f in facts],
                    'criterion': criterion(facts) or ('AAA' if len(facts) == 3 and all(f[0] == 'angle' for f in facts) else 'SSA'),
                    'unit': drawing(facts, op, distort=0.35 if role == 'twin' and not has_right(facts) else 0.0)})
    # drawn_alike copies the culprit's shape exactly: the picture lies, the numbers don't
    cul = next(s for s in out if s['role'] == 'culprit')
    for s in out:
        if s['role'] == 'drawn_alike':
            s['unit'] = cul['unit']
    for s in out:
        s['pts'], s['labels'] = fit(s.pop('unit'), [tuple(f) for f in s['facts']])
        if s['labels'] is None:
            return None
    return out

def stage2():
    kinds = ['SSS'] * 3 + ['SAS'] * 3 + ['ASA'] * 4 + ['RHS'] * 2
    items = []
    for n, k in enumerate(kinds):
        lineup = None
        for _try in range(500):
            lineup = lay_out(suspects_for(k))
            if lineup is not None:
                break
        else:
            raise RuntimeError('no labelable line-up for ' + k)
        pair = sorted(s['n'] for s in lineup if s['role'] in ('culprit', 'twin'))
        items.append({'id': 's2-%02d' % (n + 1), 'stage': 2, 'criterion': k, 'suspects': lineup, 'pair': pair})
    return items

def stage3():
    plan = ['SSS', 'SSS', 'SAS', 'SAS_right', 'ASA', 'AAS', 'RHS', 'RHS', 'AAA', 'AAA', 'SSA', 'SSA']
    items = []
    for n, k in enumerate(plan):
        it = None
        for _try in range(3000):
            it = stage3_item(n, k)
            if it is not None and all(sorted(map(str, it['facts'])) != sorted(map(str, x['facts'])) for x in items):
                break
            it = None
        else:
            raise RuntimeError('no labelable stage 3 item ' + k)
        items.append(it)
    return items

def stage3_item(n, k):
    if True:
        while True:
            if k == 'SAS_right':
                p, q = R.sample(range(5, 13), 2)
                f = [('side', 0, 1, p), ('side', 0, 2, q), ('angle', 0, 90)]
                ans = 'SAS'
            elif k == 'AAA':
                f = angles_only(make_culprit('ASA')); ans = 'NOT_ENOUGH'
            elif k == 'SSA':
                # angle at C, adjacent side AC = b, opposite side AB = a, with b sin C < a < b (two triangles)
                C = R.choice(range(30, 61, 5)); bb = R.choice(range(8, 14))
                lo = math.floor(bb * math.sin(math.radians(C))) + 1
                if lo > bb - 1:
                    continue
                f = [('side', 0, 1, R.randint(lo, bb - 1)), ('side', 0, 2, bb), ('angle', 2, C)]
                if criterion(f) is not None or not ssa_ambiguous(f):
                    continue
                ans = 'NOT_ENOUGH'
            else:
                f = make_culprit(k); ans = rule_answer(k)
            break
        pa, la = fit(drawing(f, 'rot0'), f)
        if la is None:
            return None
        got = rule_answer(criterion(f)) if criterion(f) else 'NOT_ENOUGH'
        if got != ans:
            fail('%s-%d classify %s != %s' % (k, n, got, ans))
        # the second triangle: same facts on a turned or flipped drawing; for SSA, the other solution
        second, lb = fit(drawing(f, R.choice(['refl_x', 'rot90', 'rot180', 'refl_y', 'rot270']),
                                 ssa_pick=1 if k == 'SSA' else 0,
                                 distort=0.0 if k == 'SSA' or has_right(f) else 0.25), f)
        if lb is None:
            return None
        return {'id': 's3-%02d' % (n + 1), 'stage': 3, 'facts': [list(x) for x in f], 'answer': ans,
                'shown': k, 'pts_a': pa, 'labels_a': la, 'pts_b': second, 'labels_b': lb}

def stage4():
    plan = [('SSS', True), ('SAS', True), ('ASA', True), ('RHS', True), ('AAS', True),
            ('ASA', 'angles_only'), ('AAS', 'angles_only'), ('SAS', 'angle_moved'), ('SAS', 'angle_moved'),
            ('SSS', 'drawn_alike'), ('ASA', 'drawn_alike'), ('RHS', 'one_differs')]
    items = []
    for n, (k, claim) in enumerate(plan):
        lineup = None
        for _try in range(500):
            lineup = lay_out(suspects_for(k))
            if lineup is not None:
                break
        else:
            raise RuntimeError('no labelable line-up for ' + k)
        pair = sorted(s['n'] for s in lineup if s['role'] in ('culprit', 'twin'))
        if claim is True:
            said = pair; right = True
        else:
            cul = next(s['n'] for s in lineup if s['role'] == 'culprit')
            dec = next(s['n'] for s in lineup if s['role'] == claim)
            said = sorted([cul, dec]); right = False
        items.append({'id': 's4-%02d' % (n + 1), 'stage': 4, 'criterion': k, 'rule': rule_answer(k), 'suspects': lineup, 'pair': pair,
                      'witness_says': said, 'witness_right': right, 'witness_fooled_by': None if right else claim})
    return items

def check(bank):
    by = {s: [i for i in bank if i['stage'] == s] for s in (1, 2, 3, 4)}
    for s, its in by.items():
        if len(its) != 12:
            fail('stage %d has %d items' % (s, len(its)))
    for it in by[1]:
        S = it['suspects']
        pairs = [(a['n'], b['n']) for a, b in itertools.combinations(S, 2) if sq_sides(a['pts']) == sq_sides(b['pts'])]
        if [sorted(p) for p in pairs] != [it['pair']]:
            fail('%s: congruent pairs %s' % (it['id'], pairs))
        for x in S:
            if not fits(x['pts']) or area2(x['pts']) == 0:
                fail('%s: suspect %d off grid or flat' % (it['id'], x['n']))
    if sum(1 for it in by[1] if it['twin_move'] == 'reflection') < 5:
        fail('stage 1: fewer than 5 reflected twins')
    for it in by[2] + by[4]:
        S = it['suspects']
        pairs = [sorted((a['n'], b['n'])) for a, b in itertools.combinations(S, 2) if proven_equal(a['facts'], b['facts'])]
        if pairs != [it['pair']]:
            fail('%s: proven pairs %s' % (it['id'], pairs))
        for x in S:
            if x['criterion'] == 'SSA' and not ssa_ambiguous(x['facts']):
                fail('%s: SSA suspect %d is not ambiguous' % (it['id'], x['n']))
    for it in by[3]:
        c = criterion(it['facts'])
        got = rule_answer(c) if c else 'NOT_ENOUGH'
        if got != it['answer']:
            fail('%s: answer %s, facts say %s' % (it['id'], it['answer'], got))
        if it['shown'] == 'SSA' and not ssa_ambiguous(it['facts']):
            fail('%s: SSA not ambiguous' % it['id'])
    def label_ok(P, facts, labels, where):
        if labels is None or len(labels) != len(facts):
            fail('%s: labels missing' % where); return
        edges = [(P[0], P[1]), (P[1], P[2]), (P[2], P[0])]
        for l in labels:
            if l['type'] == 'right' and not any(f[0] == 'angle' and f[2] == 90 and f[1] == l['vertex'] for f in facts):
                fail('%s: right-angle marker on a corner that is not marked 90' % where)
        for f in facts:
            if f[0] == 'angle' and f[2] == 90 and not any(l['type'] == 'right' and l['vertex'] == f[1] for l in labels):
                fail('%s: a 90 degree angle without its square marker' % where)
        texted = [l for l in labels if l['type'] != 'right']
        bxs = [tuple(l['box']) for l in texted]
        for l, b in zip(texted, bxs):
            if l['type'] == 'angle' and not all(inside_tri(c, P) for c in ((b[0], b[1]), (b[0], b[3]), (b[2], b[1]), (b[2], b[3]))):
                fail('%s: angle label %s is not inside its triangle' % (where, l['text']))
            if l['type'] == 'side' and any(inside_tri(c, P) for c in ((b[0], b[1]), (b[0], b[3]), (b[2], b[1]), (b[2], b[3]))):
                fail('%s: side label %s is inside the triangle' % (where, l['text']))
            if not clear_of_marks((b[0] - 2e-3, b[1] - 2e-3, b[2] + 2e-3, b[3] + 2e-3), P, facts):
                fail('%s: label %s crosses an angle arc or a right-angle square' % (where, l['text']))
            if not belongs(P, l['fact'], (l['x'], l['y'])):
                fail('%s: label %s is nearer another vertex or edge than its own' % (where, l['text']))
            if any(seg_box_dist(p, q, b) < GAP - 2e-3 for p, q in edges) or not in_view((b[0] + 2e-3, b[1] + 2e-3, b[2] - 2e-3, b[3] - 2e-3)):
                fail('%s: label %s touches an edge or leaves the view' % (where, l['text']))
        for a, b in itertools.combinations(bxs, 2):
            if not boxes_clear(a, b):
                fail('%s: labels overlap' % where)
    for it in by[2] + by[4]:
        for x in it['suspects']:
            label_ok(x['pts'], x['facts'], x.get('labels'), '%s #%d' % (it['id'], x['n']))
    for it in by[3]:
        label_ok(it['pts_a'], it['facts'], it.get('labels_a'), it['id'] + ' A')
        label_ok(it['pts_b'], it['facts'], it.get('labels_b'), it['id'] + ' B')
    if not any(i['shown'] == 'AAS' for i in by[3]) or not any(i['criterion'] == 'AAS' for i in by[4]):
        fail('AAS missing from stage 3 or stage 4')
    for i in by[4]:
        if i['rule'] not in ('SSS', 'SAS', 'ASA', 'RHS'):
            fail('%s: rule %s is not a button' % (i['id'], i['rule']))
    s3keys = [tuple(sorted(map(str, i['facts']))) for i in by[3]]
    if len(set(s3keys)) != len(s3keys):
        fail('stage 3 repeats an item')
    ck = [tuple(sorted(map(str, next(x for x in i['suspects'] if x['role'] == 'culprit')['facts']))) for i in by[2] + by[4]]
    if len(set(ck)) != len(ck):
        fail('stages 2 and 4 repeat a culprit')
    s1k = [sq_sides(next(x for x in i['suspects'] if x['role'] == 'culprit')['pts']) for i in by[1]]
    if len(set(s1k)) != len(s1k):
        fail('stage 1 repeats a culprit shape')
    ids = [i['id'] for i in bank]
    if len(set(ids)) != len(ids):
        fail('duplicate ids')
    if by[1][0]['pair'] != [2, 6]:
        fail('s1-01 is not the witness line-up (2 and 6)')

if __name__ == '__main__':
    bank = stage1() + stage2() + stage3() + stage4()
    check(bank)
    blob = ''.join(json.dumps(i, separators=(',', ':'), ensure_ascii=False) + '\n' for i in bank)
    print('total', len(bank))
    print('failures', len(FAIL))
    print('sha256', hashlib.sha256(blob.encode('utf-8')).hexdigest())
    for f in FAIL:
        print('FAIL', f)
    if '--out' in sys.argv:
        open(sys.argv[sys.argv.index('--out') + 1], 'w', encoding='utf-8', newline='\n').write(blob)
    sys.exit(1 if FAIL else 0)
