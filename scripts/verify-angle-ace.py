#!/usr/bin/env python3
# ci-line: E | Angle Ace (every diagram measured against its words and key; every option and reason marked in Chromium) |
"""Angle Ace: every diagram measured against its words and key, and every answer marked in Chromium.

The resit correctness audit of 4 Oct 2026 found every numeric key right (75/75) and the pictures wrong:
20 of 40 Starter and 22 of 35 GCSE diagrams had a fault, because each was hand-drawn per question as
canvas code, separate from the numbers it illustrated (audit class 6). Labels sat in the wrong region,
co-interior and alternate pairs were drawn as other pairs, angles were drawn far from their size and two
GCSE figures were unanswerable. Phase 2 accepted one reason where two were valid (F13, class 4).

Every diagram is now drawn by the game's drawFig() from the question's geometry (`fig`). This check does
NOT read `fig`: it reads what was drawn. Each item is rendered in Chromium at 320, 390 and 1280px with
every canvas call recorded, and from the recording alone:
  - lines (stroked segments of 40px or more) give the vertices (where two lines meet or cross), the rays
    at each vertex and the regions between neighbouring rays, each with its drawn size;
  - each label (a number with a degree sign, or a letter) belongs to its nearest vertex and the region its
    centre lies in. FAIL if a number differs from its region's drawn size by more than 1 degree, if x's
    region is not the keyed answer's size, if two labels share a region, if a label touches a line or
    another label or leaves the canvas, or if its region has no arc (or right-angle square) spanning it;
    and if any arc does not span exactly one region;
  - the angle facts the picture supports are derived from the drawn geometry and the given numbers
    (straight line, point, vertically opposite, alternate / corresponding / co-interior on two lines
    marked parallel, triangle, exterior angle, isosceles from tick marks). Alternate means opposite
    sides of the transversal, between the lines; co-interior the same side, between the lines;
    corresponding the same side, one at each line in the same position. FAIL if a fact gives x a value
    other than the key; the set of facts that give x in one step must equal the reasons the game
    accepts (`multiReason`, else `reason`). An item with no one-step fact must have a two-step route
    through one intermediate angle (the labelled y, if there is one) whose two facts are exactly the
    accepted reasons. A recognition item's two labelled angles must form the keyed pair;
  - no caption names the shape of the pair (F-shape, Z-shape, ...), on the canvas or in the prompt;
  - options: four distinct angles with the key once; recognition, the three pair names with the key once.
Marking, in Chromium, through the game's own handlers: every angle option, every recognition option and
every one of the nine reasons is marked, right exactly when it is the key or an accepted reason; the
phase-2 option builder always offers the keyed reason among four distinct reasons. Nothing reaches the
end screen or submits: endGame and setTimeout are stubbed and every request off the stub server aborted.

A fault-injection self-test must FAIL on each planted fault: a misplaced label, a wrong-sized angle, an
exterior "alternate" pair, a dropped valid reason, a dropped second two-step route and a wrong key. The file is never touched.

    python scripts/verify-angle-ace.py [--verbose] [--no-selftest] [--chromium PATH] [--against FILE]

--against FILE serves FILE as the game's page (e.g. main's copy before the rebuild); its failures are
listed per item, which names the audit's faulty items.
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'angle-ace'
LEVELS = ['year6', 'gcse']
COUNTS = {'year6': 40, 'gcse': 35}
WIDTHS = [(320, 568), (390, 844), (1280, 800)]
LINE_MIN = 40      # px: a stroked segment this long is a line of the figure; shorter strokes are marks
TOL = 1.0          # degrees: a label against its region, an arc against its region, x against the key
NEAR = 2.0         # px: points this close are the same point
PAIRS = {'Corresponding angles (equal)': 'CORR', 'Alternate angles (equal)': 'ALT',
         'Co-interior angles (sum to 180°)': 'COINT'}
# The two-step items, reviewed (Jon, 6 Oct 2026): (prompt, key) -> (every route the drawing allows, why).
# The game accepts the union of a item's routes; where the figure labels the intermediate angle (y), only
# the routes through it count. Change an entry only after re-reading the item and its drawing.
TWO_STEP = {
    ('Find angle x (two steps needed)', 118): (
        [('CORR', 'STRAIGHT')],
        'L625: y is labelled, so only the route through y: y = 62 (corresponding), x = 180 - y (straight line)'),
    ('Find angle x in the triangle', 105): (
        [('ALT', 'TRIANGLE'), ('ALT', 'STRAIGHT')],
        'L638: the 45 is alternate to the triangle angle at P, then the triangle; or the 30 is alternate '
        'to the angle at Q beside x, then the straight line (Jon, 6 Oct 2026: accept both routes)'),
}
SHAPE_RE = re.compile(r'\b[A-Z]-shape|\bshape\b', re.I)


# ---------------------------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------------------------
def ang(p, q):
    """Maths angle (degrees, anticlockwise from east) of p->q on a screen whose y runs down."""
    return math.degrees(math.atan2(p[1] - q[1], q[0] - p[0])) % 360


def adiff(a, b):
    """Smallest difference between two directions."""
    d = (a - b) % 360
    return min(d, 360 - d)


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def dist_to_seg(p, s):
    (x1, y1), (x2, y2) = s
    dx, dy = x2 - x1, y2 - y1
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((p[0] - x1) * dx + (p[1] - y1) * dy) / L))
    return dist(p, (x1 + t * dx, y1 + t * dy))


def seg_intersection(s, t):
    (x1, y1), (x2, y2) = s
    (x3, y3), (x4, y4) = t
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-9:
        return None
    a = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    b = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
    ea, eb = NEAR / max(dist(*s), 1e-9), NEAR / max(dist(*t), 1e-9)
    if -ea <= a <= 1 + ea and -eb <= b <= 1 + eb:
        return (x1 + a * (x2 - x1), y1 + a * (y2 - y1))
    return None


def seg_hits_box(s, b):
    """Liang-Barsky: does segment s touch box (x0, y0, x1, y1)?"""
    (px, py), (qx, qy) = s
    dx, dy = qx - px, qy - py
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, px - b[0]), (dx, b[2] - px), (-dy, py - b[1]), (dy, b[3] - py)):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def in_span(a, lo, hi):
    """Is direction a strictly inside the anticlockwise span lo..hi?"""
    return 0 < (a - lo) % 360 < (hi - lo)


# ---------------------------------------------------------------------------------------------
# the recording -> a measured figure
# ---------------------------------------------------------------------------------------------
class Fig:
    pass


def parse(rec):
    """Canvas calls -> lines, marks, arcs, fills and texts (user-space coordinates)."""
    segs, shorts, arcs, fills, texts = [], [], [], [], []
    sub, subs, parcs = [], [], []
    scale = 1.0
    for c in rec['log']:
        op = c[0]
        if op == 'setTransform':
            scale = c[1] or 1.0
        elif op == 'beginPath':
            sub, subs, parcs = [], [], []
        elif op == 'moveTo':
            sub = [(c[1], c[2])]
            subs.append(sub)
        elif op == 'lineTo':
            if not subs:
                sub = []
                subs.append(sub)
            sub.append((c[1], c[2]))
        elif op == 'closePath':
            if sub:
                sub.append(sub[0])
        elif op == 'arc':
            parcs.append(c[1:])
        elif op == 'stroke':
            for s in subs:
                path = [(s[i], s[i + 1]) for i in range(len(s) - 1) if dist(s[i], s[i + 1]) > 0.01]
                if len(path) == 1 and dist(*path[0]) >= LINE_MIN:
                    segs.append(path[0])
                elif path:
                    if all(dist(*p) >= LINE_MIN for p in path):
                        segs.extend(path)
                    else:
                        shorts.append(path)
            for a in parcs:
                arcs.append(a)
        elif op == 'fill':
            for s in subs:
                if len(s) >= 3:
                    fills.append(s)
        elif op == 'fillText':
            texts.append(c[1])
    F = Fig()
    F.W, F.H = rec['w'] / scale, rec['h'] / scale
    F.segs, F.shorts, F.arcs, F.fills, F.texts = segs, shorts, arcs, fills, texts
    return F


def measure(F):
    """Vertices, rays, regions, merged lines, marks and labels of a parsed figure."""
    # candidate points: every endpoint and every crossing of two lines
    cand = [p for s in F.segs for p in s]
    for i in range(len(F.segs)):
        for j in range(i + 1, len(F.segs)):
            x = seg_intersection(F.segs[i], F.segs[j])
            if x:
                cand.append(x)
    pts = []
    for p in cand:
        if not any(dist(p, q) <= NEAR for q in pts):
            pts.append(p)
    F.verts = []
    for p in pts:
        dirs = []
        for s in F.segs:
            if dist_to_seg(p, s) <= 1.5:
                for e in s:
                    if dist(p, e) > 3:
                        a = ang(p, e)
                        if not any(adiff(a, d) < 0.5 for d in dirs):
                            dirs.append(a)
        if len(dirs) >= 2 and not (len(dirs) == 2 and abs(adiff(dirs[0], dirs[1]) - 180) < 0.5):
            dirs.sort()
            regs = [(dirs[i], dirs[i + 1]) for i in range(len(dirs) - 1)] + [(dirs[-1], dirs[0] + 360)]
            F.verts.append({'p': p, 'dirs': dirs, 'regs': regs})
    # merged infinite lines: segments with one direction (mod 180) and one offset
    F.lines = []
    for s in F.segs:
        d = ang(*s) % 180
        for L in F.lines:
            if adiff(2 * d, 2 * L['d']) / 2 < 0.5 and dist_to_line(s[0], L['segs'][0]) < 1.5:
                L['segs'].append(s)
                break
        else:
            F.lines.append({'d': d, 'segs': [s]})
    # parallel marks: a small filled shape on a line, or an arrow glyph drawn on it (the old pages)
    marks = [tuple(sum(c) / len(f) for c in zip(*f)) for f in F.fills if max(dist(f[0], q) for q in f) < 20]
    marks += [(t['cx'], t['cy']) for t in F.texts if re.fullmatch(r'[▸>]+', t['text'].strip())]
    for L in F.lines:
        L['arrows'] = sum(1 for m in marks if dist_to_line(m, L['segs'][0]) < 9
                          and any(dist_to_seg(m, s) < 9 for s in L['segs']))
    # angle marks: arcs and right-angle squares, each as (vertex index, from, to)
    F.amarks, F.stray = [], []
    for (cx, cy, r, s, e, ccw) in F.arcs:
        vi = nearest_vertex(F, (cx, cy), NEAR)
        sd, ed = math.degrees(s), math.degrees(e)
        span = ((sd - ed) if ccw else (ed - sd)) % 360 or 360
        lo = (-ed) % 360 if not ccw else (-sd) % 360
        if vi is None:
            F.stray.append('an arc centred at (%.0f, %.0f) is at no vertex' % (cx, cy))
        else:
            F.amarks.append((vi, lo, lo + span, 'arc'))
    F.ticks = []
    for path in F.shorts:
        if len(path) == 2 and abs(dist(*path[0]) - dist(*path[1])) < 1 and \
                abs(adiff(ang(*path[0]), ang(*path[1])) - 90) < 2:
            a, b, c = path[0][0], path[0][1], path[1][1]
            v = (a[0] + c[0] - b[0], a[1] + c[1] - b[1])
            vi = nearest_vertex(F, v, NEAR)
            if vi is None:
                F.stray.append('a right-angle square at (%.0f, %.0f) is at no vertex' % v)
            else:
                a1, a2 = ang(v, a), ang(v, c)
                lo, hi = (a1, a2) if (a2 - a1) % 360 < 180 else (a2, a1)
                F.amarks.append((vi, lo, lo + (hi - lo) % 360, 'square'))
        elif len(path) == 1:
            F.ticks.append(path[0])
    # labels
    F.labels, F.captions = [], []
    for t in F.texts:
        txt = t['text'].strip()
        m = re.fullmatch(r'(\d+(?:\.\d+)?)°', txt)
        if m or re.fullmatch(r'[a-z]', txt):
            lab = {'text': txt, 'num': float(m.group(1)) if m else None, 'letter': None if m else txt,
                   'c': (t['cx'], t['cy']), 'box': t['box']}
            lab['v'] = nearest_vertex(F, lab['c'])
            if lab['v'] is not None:
                V = F.verts[lab['v']]
                a = ang(V['p'], lab['c'])
                lab['reg'] = next((k for k, (lo, hi) in enumerate(V['regs']) if in_span(a, lo, hi)), None)
            else:
                lab['reg'] = None
            F.labels.append(lab)
        elif not re.fullmatch(r'[▸>]+', txt):
            F.captions.append(txt)
    return F


def dist_to_line(p, s):
    (x1, y1), (x2, y2) = s
    L = math.hypot(x2 - x1, y2 - y1)
    return abs((x2 - x1) * (y1 - p[1]) - (x1 - p[0]) * (y2 - y1)) / L


def nearest_vertex(F, p, within=None):
    best = None
    for i, V in enumerate(F.verts):
        d = dist(p, V['p'])
        if (within is None or d <= within) and (best is None or d < best[0]):
            best = (d, i)
    return None if best is None else best[1]


def size(F, rid):
    lo, hi = F.verts[rid[0]]['regs'][rid[1]]
    return hi - lo


def find_region(F, vi, lo, hi):
    """The region of vertex vi spanning lo..hi (within TOL at both ends), or None."""
    for k, (a, b) in enumerate(F.verts[vi]['regs']):
        if adiff(a, lo) <= TOL and adiff(b, hi) <= TOL and abs((b - a) - (hi - lo)) <= 2 * TOL:
            return k
    return None


# ---------------------------------------------------------------------------------------------
# angle facts: what the drawn figure lets a student work out, one step at a time
# ---------------------------------------------------------------------------------------------
def has_dir(V, a):
    return any(adiff(d, a) < 0.75 for d in V['dirs'])


def region_between(F, vi, a, b):
    """The single region of vertex vi bounded by directions a then b anticlockwise, or None."""
    V = F.verts[vi]
    for k, (lo, hi) in enumerate(V['regs']):
        if adiff(lo, a) < 0.75 and adiff(hi, b) < 0.75:
            return k
    return None


def triangles(F):
    """Triples of vertices joined pairwise by a drawn line."""
    n = len(F.verts)

    def joined(i, j):
        p, q = F.verts[i]['p'], F.verts[j]['p']
        return all(any(dist_to_seg((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])), s) <= 1.5 for s in F.segs)
                   for t in (0.1, 0.3, 0.5, 0.7, 0.9))
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if joined(i, j) and joined(j, k) and joined(i, k):
                    out.append((i, j, k))
    return out


def interior_region(F, vi, u, w):
    """Region at vi of the triangle angle between the rays to vertices u and w (one region), or None."""
    P = F.verts[vi]['p']
    a1, a2 = ang(P, F.verts[u]['p']), ang(P, F.verts[w]['p'])
    lo, hi = (a1, a2) if (a2 - a1) % 360 < 180 else (a2, a1)
    k = region_between(F, vi, lo, hi)
    return None if k is None else (vi, k)


def parallel_pairs(F):
    out = []
    for i, A in enumerate(F.lines):
        for B in F.lines[i + 1:]:
            if adiff(2 * A['d'], 2 * B['d']) / 2 < 0.5 and dist_to_line(B['segs'][0][0], A['segs'][0]) > 10 \
                    and A['arrows'] and A['arrows'] == B['arrows']:
                out.append((A, B))
    return out


def on_line(p, L):
    return any(dist_to_seg(p, s) <= 1.5 for s in L['segs'])


def classify(F, g, t):
    """The parallel-lines relationship of regions g and t ('ALT', 'CORR', 'COINT') or None."""
    Vg, Vt = F.verts[g[0]], F.verts[t[0]]
    for A, B in parallel_pairs(F):
        for L1, L2 in ((A, B), (B, A)):
            if not (on_line(Vg['p'], L1) and on_line(Vt['p'], L2)):
                continue
            tdir = ang(Vg['p'], Vt['p'])
            if adiff(2 * tdir, 2 * L1['d']) / 2 < 0.5:
                continue
            # the transversal must be drawn between the two vertices
            if not any(dist_to_seg(Vg['p'], s) <= 1.5 and dist_to_seg(Vt['p'], s) <= 1.5 for s in F.segs):
                continue
            info = []
            for V, rid, Lown in ((Vg, g, L1), (Vt, t, L2)):
                lo, hi = V['regs'][rid[1]]
                along = [adiff(2 * x, 2 * Lown['d']) / 2 < 0.75 for x in (lo, hi)]
                across = [adiff(2 * x, 2 * tdir) / 2 < 0.75 for x in (lo, hi)]
                if not ((along[0] and across[1]) or (across[0] and along[1])):
                    return None
                mid = (lo + hi) / 2
                bis = (math.cos(math.radians(mid)), math.sin(math.radians(mid)))
                tv = (math.cos(math.radians(tdir)), math.sin(math.radians(tdir)))
                side = 1 if tv[0] * bis[1] - tv[1] * bis[0] > 0 else -1
                other = Vt['p'] if V is Vg else Vg['p']
                # interior: the region opens towards the other parallel line
                to_other = (other[0] - V['p'][0], -(other[1] - V['p'][1]))
                ld = (math.cos(math.radians(Lown['d'])), math.sin(math.radians(Lown['d'])))
                n = (-ld[1], ld[0])
                if n[0] * to_other[0] + n[1] * to_other[1] < 0:
                    n = (-n[0], -n[1])
                interior = n[0] * bis[0] + n[1] * bis[1] > 0
                info.append((side, interior))
            (s1, i1), (s2, i2) = info
            if i1 and i2:
                return 'COINT' if s1 == s2 else 'ALT'
            if s1 == s2 and i1 != i2:
                return 'CORR'
            return None
    return None


def derive(F, t, K, tri):
    """Every (fact, value) that gives region t in one step from the known regions K {rid: value}."""
    out = []
    vi, k = t
    V = F.verts[vi]
    regs = V['regs']
    # straight line: t and its neighbours fill the half-turn between two opposite rays
    for i, a in enumerate(V['dirs']):
        if not has_dir(V, a + 180):
            continue
        half = [j for j, (lo, hi) in enumerate(regs)
                if (lo - a) % 360 < 180 - 0.5 and 0.5 < (hi - a) % 360 <= 180 + 0.5]
        if k in half and abs(sum(hi - lo for j, (lo, hi) in enumerate(regs) if j in half) - 180) < 1:
            others = [(vi, j) for j in half if j != k]
            if all(o in K for o in others):
                out.append(('STRAIGHT', 180 - sum(K[o] for o in others)))
    # angles at a point
    others = [(vi, j) for j in range(len(regs)) if j != k]
    if others and all(o in K for o in others):
        out.append(('POINT', 360 - sum(K[o] for o in others)))
    # vertically opposite
    lo, hi = regs[k]
    j = region_between(F, vi, (lo + 180) % 360, (hi + 180) % 360)
    if j is not None and j != k and has_dir(V, lo + 180) and has_dir(V, hi + 180) and (vi, j) in K:
        out.append(('VERTOP', K[(vi, j)]))
    # parallel lines
    for g, v in K.items():
        if g[0] != vi:
            rel = classify(F, g, t)
            if rel:
                out.append((rel, 180 - v if rel == 'COINT' else v))
    # triangles: interior sum, exterior angle, isosceles base angles
    for T in tri:
        if vi not in T:
            continue
        u, w = [x for x in T if x != vi]
        ints = {x: interior_region(F, x, *[y for y in T if y != x]) for x in T}
        if ints[vi] == t and ints[u] in K and ints[w] in K:
            out.append(('TRIANGLE', 180 - K[ints[u]] - K[ints[w]]))
        for a_, b_ in ((u, w), (w, u)):
            P = V['p']
            ext = (ang(P, F.verts[b_]['p']) + 180) % 360
            if has_dir(V, ext):
                lo2, hi2 = ang(P, F.verts[a_]['p']), ext
                if (hi2 - lo2) % 360 > 180:
                    lo2, hi2 = hi2, lo2
                r = region_between(F, vi, lo2, hi2)
                if r == k and ints[u] in K and ints[w] in K:
                    out.append(('EXTERIOR', K[ints[u]] + K[ints[w]]))
        sides = {}
        for (a_, b_) in ((T[0], T[1]), (T[1], T[2]), (T[0], T[2])):
            P, Q = F.verts[a_]['p'], F.verts[b_]['p']
            M = ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
            sides[(a_, b_)] = sum(1 for s in F.ticks if dist(((s[0][0] + s[1][0]) / 2, (s[0][1] + s[1][1]) / 2), M) < 12
                                  and abs(adiff(ang(*s), ang(P, Q)) - 90) < 15)
        marked = [s for s, n in sides.items() if n]
        if len(marked) == 2 and sides[marked[0]] == sides[marked[1]]:
            apex = set(marked[0]) & set(marked[1])
            base = [x for x in T if x not in apex]
            if vi in base:
                other = [x for x in base if x != vi][0]
                if ints[vi] == t and ints[other] in K:
                    out.append(('ISOSC', K[ints[other]]))
    return out


# ---------------------------------------------------------------------------------------------
# one item
# ---------------------------------------------------------------------------------------------
def check_item(q, F, reasons, where, fail, notes=None):
    """All checks on one rendered item. `reasons` maps the game's REASONS keys to their strings."""
    measure(F)
    for s in F.stray:
        fail(where, 'arc', s)
    for c in F.captions:
        fail(where, 'caption', 'text on the diagram that is not an angle label: %r' % c)
    if SHAPE_RE.search(q.get('prompt', '')):
        fail(where, 'caption', 'the prompt names the shape of the pair: %r' % q['prompt'])
    labs = F.labels
    taken = {}
    for i, L in enumerate(labs):
        b = L['box']
        if b[0] < 0 or b[1] < 0 or b[2] > F.W or b[3] > F.H:
            fail(where, 'label', '%s runs off the canvas' % L['text'])
        g = (b[0] - 1, b[1] - 1, b[2] + 1, b[3] + 1)
        if any(seg_hits_box(s, g) for s in F.segs):
            fail(where, 'label', '%s touches a line' % L['text'])
        for M in labs[i + 1:]:
            o = M['box']
            if not (g[2] < o[0] or g[0] > o[2] or g[3] < o[1] or g[1] > o[3]):
                fail(where, 'label', '%s overlaps %s' % (L['text'], M['text']))
        if L['reg'] is None:
            fail(where, 'label', '%s lies in no region of a vertex (on a line, or at no vertex)' % L['text'])
            continue
        rid = (L['v'], L['reg'])
        if rid in taken:
            fail(where, 'label', '%s and %s are in the same angle (%.1f°)' % (taken[rid], L['text'], size(F, rid)))
        taken[rid] = L['text']
        if L['num'] is not None and abs(L['num'] - size(F, rid)) > TOL:
            fail(where, 'label', '%s is printed on an angle drawn %.1f°' % (L['text'], size(F, rid)))
        if not any(m[0] == rid[0] and find_region(F, m[0], m[1], m[2]) == rid[1] for m in F.amarks):
            fail(where, 'arc', '%s: no arc or right-angle square spans its angle (%.1f°)' % (L['text'], size(F, rid)))
    for (vi, lo, hi, kind) in F.amarks:
        k = find_region(F, vi, lo, hi)
        if k is None:
            fail(where, 'arc', 'an %s at a vertex spans %.1f°, not exactly one angle of the figure'
                 % (kind, (hi - lo)))
        elif (vi, k) not in taken and kind == 'arc':
            fail(where, 'arc', 'an arc spans an unlabelled angle (%.1f°)' % (hi - lo))
    # the givens: numbers, and right-angle squares with no number
    K = {(L['v'], L['reg']): L['num'] for L in labs if L['num'] is not None and L['reg'] is not None}
    for (vi, lo, hi, kind) in F.amarks:
        k = find_region(F, vi, lo, hi)
        if kind == 'square' and k is not None and (vi, k) not in K and (vi, k) not in taken:
            K[(vi, k)] = 90.0
    tri = triangles(F)
    letters = {L['letter']: (L['v'], L['reg']) for L in labs if L['letter'] and L['reg'] is not None}
    if q.get('isRecognition'):
        nums = [(L['v'], L['reg']) for L in labs if L['num'] is not None and L['reg'] is not None]
        want = PAIRS.get(q['answer'])
        if len(nums) != 2 or letters:
            fail(where, 'relationship', 'a recognition item needs exactly two numbered angles; drawn %d (%s)'
                 % (len(nums), ', '.join(L['text'] for L in labs)))
            return
        rel = classify(F, nums[0], nums[1])
        if rel != want:
            fail(where, 'relationship', 'keyed %r, drawn %s' % (q['answer'], describe(F, nums, rel)))
        return
    if 'x' not in letters:
        fail(where, 'x', 'no x label in any angle of the figure')
        return
    t = letters['x']
    key = float(q['answer'])
    if abs(size(F, t) - key) > TOL:
        fail(where, 'x', 'x is drawn %.1f°, the key is %g°' % (size(F, t), key))
    accepted = set(q.get('multiReason') or [q['reason']])
    name = {v: k for k, v in reasons.items()}
    acc = {name.get(r, r) for r in accepted}
    one = derive(F, t, K, tri)
    for r, v in one:
        if abs(v - key) > 0.5:
            fail(where, 'picture', 'the picture gives x = %g° by %s; the key is %g°' % (v, r, key))
    found = {r for r, v in one if abs(v - key) <= 0.5}
    if found:
        if found != acc:
            fail(where, 'reasons', 'the picture gives x in one step by %s; the game accepts %s'
                 % (sorted(found), sorted(acc)))
        if notes is not None:
            notes.append('%s: x = %g by %s' % (where, key, '/'.join(sorted(found))))
        return
    # Two steps, through one intermediate angle (Jon, 6 Oct 2026): the valid reasons are the union of every
    # two-step route the drawing allows, through the labelled intermediate (y) where the figure labels one,
    # through any angle where it does not. The routes must match the reviewed table TWO_STEP.
    zs = [letters[y] for y in letters if y != 'x'] or \
        [(vi, k) for vi, V in enumerate(F.verts) for k in range(len(V['regs'])) if (vi, k) not in K and (vi, k) != t]
    routes = set()
    for z in zs:
        for r1, vz in derive(F, z, K, tri):
            K2 = dict(K)
            K2[z] = vz
            for r2, vx in derive(F, t, K2, tri):
                if abs(vx - key) > 0.5:
                    fail(where, 'picture', 'the picture gives x = %g° by %s then %s; the key is %g°' % (vx, r1, r2, key))
                else:
                    routes.add(frozenset((r1, r2)))
    shown = ' or '.join(sorted('+'.join(sorted(r)) for r in routes))
    union = set().union(*routes) if routes else set()
    review = TWO_STEP.get((q.get('prompt'), q.get('answer')))
    if not routes:
        fail(where, 'picture', 'no angle fact, in one step or two, gives x from what is drawn')
        return
    if review is None:
        fail(where, 'reasons', 'a two-step item missing from TWO_STEP; drawn routes: %s (review, then add it)' % shown)
    elif routes != {frozenset(r) for r in review[0]}:
        fail(where, 'reasons', 'drawn routes %s differ from the reviewed TWO_STEP routes %s'
             % (shown, ' or '.join(sorted('+'.join(sorted(r)) for r in review[0]))))
    if union != acc:
        fail(where, 'reasons', 'two-step routes drawn: %s; the game must accept their union %s, it accepts %s'
             % (shown, sorted(union), sorted(acc)))
    elif notes is not None:
        notes.append('%s: x = %g in two steps by %s' % (where, key, shown))


def describe(F, rids, rel):
    return 'a %s pair' % rel if rel else 'a pair that is not alternate, corresponding or co-interior ' \
        '(%s)' % ', '.join('%.1f°' % size(F, r) for r in rids)


def check_options(q, where, fail):
    if q.get('isRecognition'):
        o = q.get('recognitionOpts') or []
        if sorted(o) != sorted(PAIRS) or o.count(q['answer']) != 1:
            fail(where, 'options', 'recognition options %r' % o)
        return
    o = q.get('angleOpts') or []
    if len(o) != 4 or len(set(o)) != 4 or o.count(q['answer']) != 1:
        fail(where, 'options', 'angle options %r, key %r' % (o, q['answer']))


# ---------------------------------------------------------------------------------------------
# the page
# ---------------------------------------------------------------------------------------------
RECORDER = r'''
(() => {
  const P = CanvasRenderingContext2D.prototype, rec = () => window.__AA_REC;
  const log = (...a) => { if (rec()) window.__AA_LOG.push(a); };
  for (const m of ['beginPath', 'closePath', 'stroke', 'fill']) {
    const f = P[m]; P[m] = function (...a) { log(m); return f.apply(this, a); };
  }
  for (const m of ['moveTo', 'lineTo']) {
    const f = P[m]; P[m] = function (x, y) { log(m, x, y); return f.apply(this, arguments); };
  }
  const arc = P.arc; P.arc = function (x, y, r, s, e, ccw) { log('arc', x, y, r, s, e, !!ccw); return arc.apply(this, arguments); };
  const st = P.setTransform; P.setTransform = function (a) { log('setTransform', typeof a === 'number' ? a : 1); return st.apply(this, arguments); };
  const ft = P.fillText; P.fillText = function (text, x, y) {
    if (rec()) {
      const w = this.measureText(text).width, px = parseFloat((this.font.match(/(\d+(?:\.\d+)?)px/) || [0, 15])[1]);
      const cx = this.textAlign === 'left' || this.textAlign === 'start' ? x + w / 2 : this.textAlign === 'right' || this.textAlign === 'end' ? x - w / 2 : x;
      const bl = this.textBaseline, cy = bl === 'middle' ? y : bl === 'top' || bl === 'hanging' ? y + px / 2 : bl === 'bottom' ? y - px / 2 : y - 0.35 * px;
      window.__AA_LOG.push(['fillText', {text: String(text), cx, cy, box: [cx - w / 2, cy - px / 2, cx + w / 2, cy + px / 2]}]);
    }
    return ft.apply(this, arguments);
  };
})();
'''

JS_RENDER = '''([lv, i]) => {
  const q = QUESTIONS_BY_LEVEL[lv][i];
  window.__AA_LOG = []; window.__AA_REC = true;
  currentQ = q;
  if (q.fig) drawFig(q); else { canvas.width = 600; canvas.height = 360; canvas.style.height = ''; ctx.setTransform(1, 0, 0, 1, 0, 0); q.draw(q); }
  window.__AA_REC = false;
  return {log: window.__AA_LOG, w: canvas.width, h: canvas.height};
}'''

JS_MARK = '''([lv, i]) => {
  const q = QUESTIONS_BY_LEVEL[lv][i], out = {angle: [], reason: [], recog: [], builder: []};
  const show = () => { pool = [q]; qIdx = 0; total = 0; nextQ(); };
  const fake = v => { const b = document.createElement('button'); b.className = 'opt-btn'; b.dataset.val = v;
                      document.getElementById('options').appendChild(b); return b; };
  if (q.isRecognition) {
    for (const v of q.recognitionOpts) { show(); const b = fake(v); handleRecognition(b); out.recog.push([v, b.classList.contains('correct')]); }
    return out;
  }
  for (const v of q.angleOpts) {
    show();
    const b = [...document.querySelectorAll('#options .opt-btn')].find(x => x.dataset.val === String(v));
    if (!b) { out.angle.push([v, null]); continue; }
    b.click(); out.angle.push([v, b.classList.contains('correct')]);
  }
  for (let n = 0; n < 6; n++) {
    show(); angleCorrect = true; showPhase2();
    out.builder.push([...document.querySelectorAll('#options .opt-btn')].map(x => x.dataset.val));
  }
  for (const r of Object.values(REASONS)) {
    show(); angleCorrect = true; showPhase2();
    document.getElementById('options').innerHTML = '';
    const b = fake(r); handlePhase2(b); out.reason.push([r, b.classList.contains('correct')]);
  }
  return out;
}'''


def run_page(chromium=None, against=None, patches=None):
    """Render every item at every width and mark every answer. Returns (banks, reasons, renders, marks)."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    page_url = base + '/games/' + SLUG + '/'
    body = open(against, encoding='utf-8').read() if against else None
    renders, marks = {}, {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(**({'executable_path': chromium} if chromium else {}))
            for wi, (w, h) in enumerate(WIDTHS):
                page = browser.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.add_init_script(RECORDER)

                def route(r):
                    u = r.request.url.split('?')[0]
                    if body is not None and u in (page_url, page_url + 'index.html'):
                        return r.fulfill(status=200, content_type='text/html; charset=utf-8', body=body)
                    return r.continue_() if r.request.url.startswith(base) else r.abort()
                page.route('**/*', route)
                page.goto(page_url + '?cb=verify', wait_until='load', timeout=20000)
                page.wait_for_function('typeof QUESTIONS_BY_LEVEL !== "undefined"', timeout=8000)
                if patches:
                    page.evaluate(patches)
                page.evaluate('window.endGame = () => { window.__AA_ENDED = true; };'
                              'window.setTimeout = () => 0;')
                page.evaluate('startGame()')
                if wi == 0:
                    banks = page.evaluate('''JSON.parse(JSON.stringify(Object.fromEntries(Object.entries(QUESTIONS_BY_LEVEL)
                                            .map(([k, v]) => [k, v.map(q => Object.assign({}, q, {draw: undefined}))]))))''')
                    reasons = page.evaluate('REASONS')
                for lv in LEVELS:
                    for i in range(len(banks.get(lv, []))):
                        renders[(lv, i, w)] = page.evaluate(JS_RENDER, [lv, i])
                        if wi == 1:
                            marks[(lv, i)] = page.evaluate(JS_MARK, [lv, i])
                if page.evaluate('window.__AA_ENDED === true'):
                    errors.append('the session reached its end screen; it must not (nothing may submit)')
                page.close()
                if errors:
                    raise RuntimeError('page errors at %dpx: %s' % (w, errors[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return banks, reasons, renders, marks


def check_marks(q, m, where, fail):
    if q.get('isRecognition'):
        for v, ok in m['recog']:
            if ok != (v == q['answer']):
                fail(where, 'marking', 'recognition option %r marked %s' % (v, 'right' if ok else 'wrong'))
        return
    for v, ok in m['angle']:
        if ok is None:
            fail(where, 'marking', 'angle option %s is not offered as a button' % v)
        elif ok != (v == q['answer']):
            fail(where, 'marking', 'angle %s marked %s' % (v, 'right' if ok else 'wrong'))
    acc = set(q.get('multiReason') or [q['reason']])
    for r, ok in m['reason']:
        if ok != (r in acc):
            fail(where, 'marking', 'reason %r marked %s' % (r, 'right' if ok else 'wrong'))
    for opts in m['builder']:
        if len(opts) != 4 or len(set(opts)) != 4 or q['reason'] not in opts:
            fail(where, 'marking', 'phase 2 offered %r' % opts)


class Report:
    def __init__(self):
        self.fails = []

    def __call__(self, where, kind, msg):
        line = '%s [%s] %s' % (where, kind, msg)
        if line not in self.fails:
            self.fails.append(line)


def label(lv, i, q):
    return '%s[%d] (%s, key %s)' % (lv, i, q.get('prompt', '')[:40], q.get('answer'))


def check_all(rep, banks, reasons, renders, marks, notes=None):
    for lv in LEVELS:
        bank = banks.get(lv, [])
        if lv in COUNTS and len(bank) != COUNTS[lv]:
            rep(lv, 'count', '%d items, expected %d' % (len(bank), COUNTS[lv]))
        for i, q in enumerate(bank):
            where = label(lv, i, q)
            check_options(q, where, rep)
            for (w, h) in WIDTHS:
                check_item(q, parse(renders[(lv, i, w)]), reasons, where + ' @%dpx' % w, rep,
                           notes if w == 390 else None)
            if (lv, i) in marks:
                check_marks(q, marks[(lv, i)], where, rep)


# ---------------------------------------------------------------------------------------------
# fault injection
# ---------------------------------------------------------------------------------------------
def selftest(banks, reasons, renders, marks, extra):
    """Each planted fault must add a FAIL. `extra` holds renders made with a patched page."""
    import copy
    lines, ok = [], True
    base = Report()
    check_all(base, banks, reasons, renders, marks)

    def expect(name, b=banks, r=renders, m=marks):
        nonlocal ok
        rep = Report()
        check_all(rep, b, reasons, r, m)
        new = [f for f in rep.fails if f not in base.fails]
        ok = ok and bool(new)
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + new[0][:110]) if new else '*** MISSED ***'))

    item = ('year6', 0, 390)     # x and 40° on a straight line
    rec = renders[item]

    # a misplaced label: the 40° label reflected across the vertex's vertical, into x's angle
    r2 = copy.deepcopy(renders)
    F = measure(parse(rec))
    V = F.verts[0]['p']
    for c in r2[item]['log']:
        if c[0] == 'fillText' and c[1]['text'] == '40°':
            d = c[1]['cx'] - V[0]
            c[1]['cx'] -= 2 * d
            c[1]['box'] = [c[1]['box'][0] - 2 * d, c[1]['box'][1], c[1]['box'][2] - 2 * d, c[1]['box'][3]]
    expect('misplaced label (40° in x\'s angle)', r=r2)

    # a wrong-sized angle: the ray between 40° and x turned 25° anticlockwise
    r2 = copy.deepcopy(renders)
    log = r2[item]['log']
    for k, c in enumerate(log):
        if c[0] == 'lineTo' and log[k - 1][0] == 'moveTo' and dist((log[k - 1][1], log[k - 1][2]), V) < 1:
            L = dist(V, (c[1], c[2]))
            a = math.radians(ang(V, (c[1], c[2])) + 25)
            c[1], c[2] = V[0] + L * math.cos(a), V[1] - L * math.sin(a)
            break
    expect('wrong-sized angle (ray turned 25°)', r=r2)

    # an exterior "alternate" pair, drawn by the game itself from patched data
    expect('exterior "alternate" pair', r={**renders, **extra})

    # a valid reason dropped (audit F13): angles at a point AND on a straight line give x = 180
    b2 = copy.deepcopy(banks)
    i = next(i for i, q in enumerate(b2['year6']) if q.get('multiReason') and q['answer'] == 180)
    del b2['year6'][i]['multiReason']
    expect('valid reason not accepted (F13)', b=b2, m={k: v for k, v in marks.items() if k != ('year6', i)})

    # a second two-step route not accepted: L638 without "angles on a straight line" (Jon, 6 Oct 2026)
    if 'gcse' in LEVELS:
        b2 = copy.deepcopy(banks)
        i = next(i for i, q in enumerate(b2['gcse']) if q['prompt'] == 'Find angle x in the triangle')
        b2['gcse'][i]['multiReason'] = [r for r in b2['gcse'][i]['multiReason'] if r != reasons['STRAIGHT']]
        expect('second two-step route dropped', b=b2, m={k: v for k, v in marks.items() if k != ('gcse', i)})

    # a wrong key
    b2 = copy.deepcopy(banks)
    b2['year6'][0]['answer'] = 130
    b2['year6'][0]['angleOpts'] = [130, 40, 120, 160]
    expect('wrong key (140 keyed 130)', b=b2, m={k: v for k, v in marks.items() if k != ('year6', 0)})
    return ok, lines


PATCH_EXTERIOR = '''(() => {
  const q = QUESTIONS_BY_LEVEL.year6.find(q => q.isRecognition && q.answer.startsWith('Alternate'));
  q.fig = {t: 'par', m: [['T', 'ur', q.fig.m[0][2]], ['B', 'll', q.fig.m[0][2]]]};
  window.__AA_PATCHED = QUESTIONS_BY_LEVEL.year6.indexOf(q);
})()'''


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--chromium', help='Chromium executable (a cloud sandbox: /opt/pw-browsers/chromium)')
    ap.add_argument('--against', help='serve this file as the game page instead of the repo copy')
    args = ap.parse_args()

    banks, reasons, renders, marks = run_page(args.chromium, args.against)
    rep, notes = Report(), []
    check_all(rep, banks, reasons, renders, marks, notes)
    if args.against:
        by_item = {}
        for f in rep.fails:
            by_item.setdefault(f.split(' @')[0].split(' [')[0], []).append(f)
        for it, fs in by_item.items():
            print(it)
            for f in fs:
                print('    ' + f.split(') ', 1)[-1] if ') ' in f else f)
        print('\n%d item(s) fail, of %d' % (len(by_item), sum(len(banks.get(lv, [])) for lv in LEVELS)))
        return 1 if rep.fails else 0
    for f in rep.fails:
        print('FAIL ' + f)
    if args.verbose:
        for n in notes:
            print('  ' + n)
    ok = not rep.fails
    if not args.no_selftest:
        _, _, extra_r, _ = run_page(args.chromium, None, PATCH_EXTERIOR)
        extra = {k: v for k, v in extra_r.items()
                 if banks['year6'][k[1]].get('isRecognition') and banks['year6'][k[1]]['answer'].startswith('Alternate')}
        first = min(k[1] for k in extra)
        extra = {k: v for k, v in extra.items() if k[1] == first}
        s_ok, lines = selftest(banks, reasons, renders, marks, extra)
        print('\nFault-injection self-test (planted in recordings or a patched page; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    n = sum(len(banks.get(lv, [])) for lv in LEVELS)
    print('\n%s: %d FAIL(s); %d items (%s) measured at %s px; every option and reason marked in Chromium'
          % ('PASS' if ok else 'FAILED', len(rep.fails), n, ', '.join(LEVELS), '/'.join(str(w) for w, _ in WIDTHS)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
