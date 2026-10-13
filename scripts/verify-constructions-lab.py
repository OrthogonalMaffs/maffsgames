#!/usr/bin/env python3
# ci-line: Constructions Lab (no marking to check: every task's figure, labels and stated results verified by constructing all ten with the game's own compass and ruler in Chromium) |
"""Constructions Lab: ten ruler-and-compass tasks drawn on a 700 x 600 canvas, with step-by-step instructions.

The game marks nothing: no task checks the construction and nothing writes a verdict (constructions-lab-t3-001, open). So there
is no key to recompute. This verifier checks what the game states and draws instead (contract VERIFIERS-20, STOP IF: "verify what
it states and draws, and report what cannot be verified"):

  Figure: each task's given figure is recorded as the page draws it (the context's moveTo/lineTo/arc/fillText during the task's
    own setup). Every letter the steps name (A, B, C, P, V) is drawn, and sits within 25 canvas units of the point it labels
    (an end of a given line, a given dot, or the vertex where two given lines meet). The constructions below find A, B, P, V
    from that drawing, not from numbers held here.
  Tools: the compass draws a circle centred on the first click through the second; Lock Radius repeats the last radius with one
    click; the ruler joins its two clicks; a click within 12 units of a crossing of two drawn circles, or of a drawn circle and a
    drawn line, lands exactly on it. Every crossing the game snaps to is recomputed here (circle-circle and circle-line in
    Python) and must agree to 1e-6. At 390 px wide the game's pixel-to-canvas mapping puts a tap within one CSS pixel of where
    it was aimed.
  Constructions: each task is built by its own steps with the game's tools (clicks on the real canvas), and what the steps say
    it makes is checked here: the perpendicular bisector of AB (tasks 1, 8) passes through the midpoint at right angles; the
    angle bisectors (tasks 2, 9) make equal angles with both arms; the perpendiculars from and at P (tasks 3, 4) are at right
    angles to the line and pass through P; "Angle BAC = 60°" (task 5) is the angle built; the triangle of task 6 is
    equilateral; the circle of task 7 is the stated distance from P, and the label and the steps state the same distance; the
    two lines of task 10 are each the stated distance from the given line, the label and steps agreeing.
  Statements: "Set compass to more than half the distance AB" is tested both ways: radii above half AB give crossings, a radius
    below half gives none.

Not verifiable, reported: whether a student's construction is right (nothing marks it, t3-001); the snap ignoring the given lines
and points (t3-002: the constructions here draw a ruler line along a given line first, so its crossings can be snapped); the
grid-dot spacing and the unbounded locus line (t3-004); the small-text and button sizes (t3-005).
No analytics or leaderboard request leaves the stub server (every other request is aborted).

    python scripts/verify-constructions-lab.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'constructions-lab'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
EPS = 1e-6

RECORD_JS = r"""(i) => {
  const rec = {segs: [], dots: [], labels: [], steps: TASKS[i].steps.slice(), name: TASKS[i].name};
  const c = ctx, saved = {moveTo: c.moveTo, lineTo: c.lineTo, arc: c.arc, fillText: c.fillText};
  let last = null;
  c.moveTo = function (x, y) { last = [x, y]; return saved.moveTo.call(c, x, y); };
  c.lineTo = function (x, y) { if (last) rec.segs.push([last[0], last[1], x, y]); last = [x, y]; return saved.lineTo.call(c, x, y); };
  c.arc = function (x, y, r, a0, a1) { if (r >= 5 && r <= 8) rec.dots.push([x, y]); return saved.arc.apply(c, arguments); };
  c.fillText = function (t, x, y) { rec.labels.push([t, x, y]); return saved.fillText.apply(c, arguments); };
  try { TASKS[i].setup(c); } finally { Object.assign(c, saved); }
  return rec;
}"""
PIN_JS = r"""() => { canvas.style.position = 'fixed'; canvas.style.left = '0px'; canvas.style.top = '0px';
  canvas.style.width = '700px'; canvas.style.zIndex = 9999; const r = canvas.getBoundingClientRect(); return [r.left, r.top, r.width]; }"""
DO_JS = r"""(acts) => {
  for (const a of acts) {
    if (a[0] === 'tool') setTool(a[1]);
    else if (a[0] === 'lock') toggleLockRadius();
    else if (a[0] === 'click') canvas.dispatchEvent(new MouseEvent('click', {clientX: a[1], clientY: a[2], bubbles: true}));
  }
  return JSON.parse(JSON.stringify(elements));
}"""


# ---- geometry, done here ------------------------------------------------------------------------------------------------
def cc(c1, c2):
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    if d == 0 or d > c1[2] + c2[2] or d < abs(c1[2] - c2[2]):
        return []
    a = (c1[2] ** 2 - c2[2] ** 2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, c1[2] ** 2 - a * a))
    mx, my = c1[0] + a * dx / d, c1[1] + a * dy / d
    return [(mx + h * dy / d, my - h * dx / d), (mx - h * dy / d, my + h * dx / d)]


def cl(c, l):
    (x1, y1, x2, y2) = l
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - c[0], y1 - c[1]
    a, b, k = dx * dx + dy * dy, 2 * (fx * dx + fy * dy), fx * fx + fy * fy - c[2] ** 2
    disc = b * b - 4 * a * k
    if disc < 0:
        return []
    s = math.sqrt(disc)
    return [(x1 + t * dx, y1 + t * dy) for t in ((-b - s) / (2 * a), (-b + s) / (2 * a))]


def angle_between(u, v):
    return math.degrees(math.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))))))


def dist_point_line(p, l):
    (x1, y1, x2, y2) = l
    return abs((x2 - x1) * (y1 - p[1]) - (x1 - p[0]) * (y2 - y1)) / math.hypot(x2 - x1, y2 - y1)


def near(p, q, tol=EPS):
    return math.hypot(p[0] - q[0], p[1] - q[1]) <= tol


class Board:
    """Drives the game's tools by clicks on the pinned 700 x 600 canvas and keeps the game's element list."""

    def __init__(self, page, fails, where):
        self.page, self.fails, self.where = page, fails, where
        self.els = []

    def run(self, acts):
        self.els = self.page.evaluate(DO_JS, acts)
        return self.els

    def arcs(self):
        return [(e['cx'], e['cy'], e['r']) for e in self.els if e['type'] == 'arc']

    def lines(self):
        return [(e['x1'], e['y1'], e['x2'], e['y2']) for e in self.els if e['type'] == 'line']

    def crossings(self):
        a, l = self.arcs(), self.lines()
        pts = [p for i in range(len(a)) for j in range(i + 1, len(a)) for p in cc(a[i], a[j])]
        pts += [p for c in a for ln in l for p in cl(c, ln)]
        return pts

    def snap_click(self, target):
        """A click at the whole pixel nearest a crossing computed here; the game must land on it exactly."""
        return ('click', round(target[0]), round(target[1]))

    def check_last(self, kind, want):
        e = self.els[-1]
        got = (e['cx'], e['cy']) if kind == 'arc' else (e['x2'], e['y2'])
        if not near(got, want):
            self.fails.append('tools: %s: the %s should land on the crossing %s, the game put it at %s' % (self.where, kind, want, got))
            return False
        return True


def label_points(rec):
    """Each single-letter label and the drawn feature it labels: line ends, dots, and vertices where two lines meet."""
    feats = [(s[0], s[1]) for s in rec['segs']] + [(s[2], s[3]) for s in rec['segs']] + [tuple(d) for d in rec['dots']]
    out = {}
    for t, x, y in rec['labels']:
        if len(t) == 1 and t.isalpha():
            best = min(feats, key=lambda f: math.hypot(f[0] - x, f[1] - y)) if feats else None
            out[t] = (best, math.hypot(best[0] - x, best[1] - y) if best else 1e9)
    return out


def bisector_line(page, fails, where, A, B):
    """Perpendicular bisector of AB with the game's tools: arcs of equal radius at A and B, ruler through both crossings."""
    bd = Board(page, fails, where)
    ab = math.hypot(B[0] - A[0], B[1] - A[1])
    r_pt = (round(A[0] + 0.75 * (B[0] - A[0])), round(A[1] + 0.75 * (B[1] - A[1])))
    bd.run([('tool', 'compass'), ('click', A[0], A[1]), ('click', r_pt[0], r_pt[1]), ('lock',), ('click', B[0], B[1]), ('lock',)])
    if len(bd.arcs()) != 2 or not near(bd.arcs()[0][:2], A) or abs(bd.arcs()[0][2] - bd.arcs()[1][2]) > EPS:
        fails.append('tools: %s: two equal arcs at A and B expected, got %r' % (where, bd.arcs()))
        return None
    xs = [p for p in cc(*bd.arcs()) if 0 <= p[0] <= 700 and 0 <= p[1] <= 600]
    if len(xs) != 2:
        fails.append('construction: %s: arcs of radius %.1f > AB/2 = %.1f should cross twice on the canvas, got %r' % (where, bd.arcs()[0][2], ab / 2, xs))
        return None
    bd.run([('tool', 'ruler'), bd.snap_click(xs[0])])
    bd.run([bd.snap_click(xs[1])])
    if not bd.check_last('line', xs[1]):
        return None
    ln = bd.lines()[-1]
    if not near((ln[0], ln[1]), xs[0]):
        fails.append('tools: %s: the ruler did not start on the crossing %s (got %s)' % (where, xs[0], ln[:2]))
    return ln


def check_task(fails, page, i, rec):
    where = 'task %d (%s)' % (i + 1, rec['name'])
    labs = label_points(rec)
    steps = ' '.join(rec['steps'])
    named = sorted(set(re.findall(r'\b([ABCPV])\b', steps + ' ' + rec['name'])) & {'A', 'B', 'C', 'P', 'V'})
    for n in named:
        if (n == 'C' and i in (4, 5)) or (n == 'B' and i == 4):
            continue        # constructed by the steps (task 5's B and C, task 6's C), not given
        if n == 'P' and i == 1:
            continue        # P and Q are where the arc crosses the arms, made by the student
        if n not in labs:
            fails.append('figure: %s: the steps name %s but the figure does not label it' % (where, n))
        elif labs[n][1] > 25:
            fails.append('figure: %s: the label %s is %.0f units from the nearest drawn point' % (where, n, labs[n][1]))
    page.evaluate('(i) => { loadTask(i); }', i)
    P = lambda n: labs[n][0]    # noqa: E731
    if i in (0, 7):
        A, B = P('A'), P('B')
        ln = bisector_line(page, fails, where, A, B)
        if ln:
            M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
            ang = angle_between((ln[2] - ln[0], ln[3] - ln[1]), (B[0] - A[0], B[1] - A[1]))
            if dist_point_line(M, ln) > EPS or abs(ang - 90) > EPS:
                fails.append('construction: %s: the line built is %.6f from the midpoint and at %.6f° to AB' % (where, dist_point_line(M, ln), ang))
        # "more than half the distance AB": a radius under half gives no crossing
        page.evaluate('(i) => { loadTask(i); }', i)
        bd = Board(page, fails, where)
        r_pt = (round(A[0] + 0.45 * (B[0] - A[0])), round(A[1] + 0.45 * (B[1] - A[1])))
        bd.run([('tool', 'compass'), ('click', A[0], A[1]), ('click', r_pt[0], r_pt[1]), ('lock',), ('click', B[0], B[1]), ('lock',)])
        if cc(*bd.arcs()):
            fails.append('statement: %s: arcs under half AB cross, so "more than half" would not be needed' % where)
    elif i in (1, 8):
        V = P('A') if i == 1 else P('V')
        arms = [s for s in rec['segs'] if near((s[0], s[1]), V, 1) or near((s[2], s[3]), V, 1)]
        if len(arms) != 2:
            fails.append('figure: %s: expected two given lines meeting at the vertex, found %d' % (where, len(arms)))
            return
        ends = [(s[2], s[3]) if near((s[0], s[1]), V, 1) else (s[0], s[1]) for s in arms]
        bd = Board(page, fails, where)
        # a ruler line along each arm, so the arc's crossings with the arms can be snapped (t3-002)
        acts = [('tool', 'ruler')]
        for e in ends:
            acts += [('click', V[0], V[1]), ('click', e[0], e[1])]
        acts += [('tool', 'compass'), ('click', V[0], V[1]), ('click', V[0] + 100, V[1])]
        bd.run(acts)
        arc0 = bd.arcs()[0]
        pq = []
        for ln in bd.lines():
            pts = [p for p in cl(arc0, ln) if (p[0] - V[0]) * (ln[2] - ln[0]) + (p[1] - V[1]) * (ln[3] - ln[1]) > 0]
            pq.append(pts[0])
        # compass at P with a radius, lock it, compass at Q
        bd.run([bd.snap_click(pq[0])])
        if not near((bd.page.evaluate('() => firstClick && [firstClick.x, firstClick.y]') or (0, 0)), pq[0]):
            fails.append('tools: %s: the compass centre did not snap to where the arc crosses the arm (%s)' % (where, pq[0]))
            return
        # radius 60: an arc of about 90 would cross the arm 10 units from the vertex, and the ruler's click at V would snap there
        bd.run([('click', round(pq[0][0] + 60), round(pq[0][1])), ('lock',), bd.snap_click(pq[1]), ('lock',)])
        a1, a2 = bd.arcs()[1], bd.arcs()[2]
        if not near(a1[:2], pq[0]) or not near(a2[:2], pq[1]) or abs(a1[2] - a2[2]) > EPS:
            fails.append('tools: %s: equal arcs at P and Q expected, got %r %r' % (where, a1, a2))
            return
        xs = cc(a1, a2)
        inner = max(xs, key=lambda p: math.hypot(p[0] - V[0], p[1] - V[1]))
        bd.run([('tool', 'ruler'), ('click', V[0], V[1]), bd.snap_click(inner)])
        if not bd.check_last('line', inner):
            return
        ln = bd.lines()[-1]
        if not near((ln[0], ln[1]), V):
            fails.append('tools: %s: the ruler did not start at the vertex %s (got %s)' % (where, V, ln[:2]))
            return
        u = (ln[2] - ln[0], ln[3] - ln[1])
        a, b = angle_between(u, (ends[0][0] - V[0], ends[0][1] - V[1])), angle_between(u, (ends[1][0] - V[0], ends[1][1] - V[1]))
        if abs(a - b) > EPS:
            fails.append('construction: %s: the line built makes %.6f° and %.6f° with the arms, not equal' % (where, a, b))
    elif i in (2, 3):
        Pp = P('P')
        base = max(rec['segs'], key=lambda s: math.hypot(s[2] - s[0], s[3] - s[1]))
        bd = Board(page, fails, where)
        acts = [('tool', 'ruler'), ('click', base[0], base[1]), ('click', base[2], base[3]), ('tool', 'compass'), ('click', Pp[0], Pp[1])]
        foot = (Pp[0], base[1])
        rp = (Pp[0] + 200, base[1]) if i == 2 else (Pp[0] + 100, Pp[1])
        acts += [('click', rp[0], rp[1])]
        bd.run(acts)
        xy = sorted(cl(bd.arcs()[0], bd.lines()[0]))
        if len(xy) != 2:
            fails.append('construction: %s: the arc from P does not cross the line twice' % where)
            return
        bd.run([bd.snap_click(xy[0]), ('click', round(xy[0][0] + 1.5 * (xy[1][0] - xy[0][0]) / 2 + 60), round(xy[0][1])), ('lock',),
                bd.snap_click(xy[1]), ('lock',)])
        a1, a2 = bd.arcs()[1], bd.arcs()[2]
        xs = [p for p in cc(a1, a2) if 0 <= p[0] <= 700 and 0 <= p[1] <= 600]
        if not xs:
            fails.append('construction: %s: the arcs from X and Y do not cross on the canvas' % where)
            return
        far = max(xs, key=lambda p: math.hypot(p[0] - Pp[0], p[1] - Pp[1]))
        bd.run([('tool', 'ruler'), ('click', Pp[0], Pp[1]), bd.snap_click(far)])
        if not bd.check_last('line', far):
            return
        ln = bd.lines()[-1]
        ang = angle_between((ln[2] - ln[0], ln[3] - ln[1]), (base[2] - base[0], base[3] - base[1]))
        if abs(ang - 90) > EPS or dist_point_line(Pp, ln) > EPS or dist_point_line(foot, ln) > EPS:
            fails.append('construction: %s: the line built is at %.6f° to the line, %.6f from P' % (where, ang, dist_point_line(Pp, ln)))
    elif i == 4:
        A = P('A')
        base = rec['segs'][0]
        far_end = max([(base[0], base[1]), (base[2], base[3])], key=lambda e: math.hypot(e[0] - A[0], e[1] - A[1]))
        u = ((far_end[0] - A[0]) / math.hypot(far_end[0] - A[0], far_end[1] - A[1]), (far_end[1] - A[1]) / math.hypot(far_end[0] - A[0], far_end[1] - A[1]))
        B = (A[0] + 200 * u[0], A[1] + 200 * u[1])
        bd = Board(page, fails, where)
        bd.run([('tool', 'compass'), ('click', A[0], A[1]), ('click', round(B[0]), round(B[1])), ('lock',), ('click', round(B[0]), round(B[1])), ('lock',)])
        C = min(cc(*bd.arcs()), key=lambda p: p[1])
        bd.run([('tool', 'ruler'), ('click', A[0], A[1]), bd.snap_click(C)])
        if not bd.check_last('line', C):
            return
        built = angle_between((C[0] - A[0], C[1] - A[1]), u)
        m = re.search(r'Angle BAC = (\d+)°', steps)
        if not m or abs(built - int(m.group(1))) > EPS or abs(built - 60) > EPS:
            fails.append('statement: %s: the steps say %r; the angle built is %.6f°' % (where, m.group(0) if m else None, built))
    elif i == 5:
        A, B = P('A'), P('B')
        bd = Board(page, fails, where)
        bd.run([('tool', 'compass'), ('click', A[0], A[1]), ('click', B[0], B[1]), ('lock',), ('click', B[0], B[1]), ('lock',)])
        C = min(cc(*bd.arcs()), key=lambda p: p[1])
        bd.run([('tool', 'ruler'), ('click', A[0], A[1]), bd.snap_click(C), ('click', B[0], B[1]), bd.snap_click(C)])
        if not bd.check_last('line', C):
            return
        s = [math.hypot(B[0] - A[0], B[1] - A[1]), math.hypot(C[0] - A[0], C[1] - A[1]), math.hypot(C[0] - B[0], C[1] - B[1])]
        if 'equilateral' not in steps or max(s) - min(s) > EPS:
            fails.append('statement: %s: the triangle built has sides %r' % (where, s))
    elif i == 6:
        Pp = P('P')
        lab = [t for t, x, y in rec['labels'] if 'px' in t]
        d1 = re.search(r'(\d+)px from P', ' '.join(lab))
        d2 = re.search(r'radius to (\d+) pixels', steps)
        d3 = re.search(r'exactly (\d+)px from P', steps)
        ds = {int(d.group(1)) for d in (d1, d2, d3) if d}
        if len(ds) != 1 or not (d1 and d2 and d3):
            fails.append('statement: %s: the label and steps state the distance as %r' % (where, [d.group(0) if d else None for d in (d1, d2, d3)]))
            return
        r = ds.pop()
        bd = Board(page, fails, where)
        bd.run([('tool', 'compass'), ('click', Pp[0], Pp[1]), ('click', Pp[0] + r, Pp[1])])
        c = bd.arcs()[0]
        if not near(c[:2], Pp) or abs(c[2] - r) > EPS:
            fails.append('construction: %s: the circle built is %r, expected centre P %s radius %d' % (where, c, Pp, r))
    elif i == 9:
        base = rec['segs'][0]
        lab = [t for t, x, y in rec['labels'] if 'px' in t]
        d1 = re.search(r'(\d+)px from the line', ' '.join(lab))
        d2 = re.findall(r'(\d+)px (above|below)', steps)
        if not d1 or len(d2) < 1 or any(int(d) != int(d1.group(1)) for d, _ in d2) or 'TWO parallel lines' not in steps:
            fails.append('statement: %s: the label says %r, the steps %r' % (where, d1.group(0) if d1 else None, d2))
            return
        k = int(d1.group(1))
        bd = Board(page, fails, where)
        bd.run([('tool', 'ruler'), ('click', base[0], base[1] - k), ('click', base[2], base[3] - k),
                ('click', base[0], base[1] + k), ('click', base[2], base[3] + k)])
        for ln in bd.lines():
            if abs(dist_point_line((ln[0], ln[1]), base) - k) > EPS or abs(dist_point_line((ln[2], ln[3]), base) - k) > EPS:
                fails.append('construction: %s: a line built is not %dpx from the given line: %r' % (where, k, ln))


def mapping_checks(fails, page):
    """At phone width: a tap aimed at a canvas point lands within one CSS pixel of it, by the game's own mapping."""
    page.set_viewport_size({'width': 390, 'height': 844})
    page.evaluate('() => { loadTask(0); }')
    res = page.evaluate(r"""() => { const r = canvas.getBoundingClientRect(), s = r.width / 700, out = [];
      for (const [x, y] of [[0, 0], [200, 200], [350, 300], [500, 200], [699, 599], [123, 456]]) {
        clearAll(); setTool('point');
        canvas.dispatchEvent(new MouseEvent('click', {clientX: r.left + x * s, clientY: r.top + y * s, bubbles: true}));
        const e = elements[elements.length - 1]; out.push([x, y, e.x, e.y, 1 / s]); }
      return out; }""")
    for x, y, gx, gy, unit in res:
        if abs(gx - x) > unit + 1e-9 or abs(gy - y) > unit + 1e-9:
            fails.append('tools: at 390 px a tap aimed at (%d, %d) lands at (%.2f, %.2f), more than one CSS pixel (%.2f units) away' % (x, y, gx, gy, unit))
            break
    page.set_viewport_size({'width': 1280, 'height': 900})


def play(fails, html):
    from playwright.sync_api import sync_playwright
    # R3 (SWEEP-1 constructions-lab-s1-001, -002): the tutorial says the ruler's line carries on past both points
    # (it is drawn 800 units beyond each), and task 9 calls its bisector the locus only inside the angle drawn
    if 'A straight line is drawn through both points and carries on past them' not in html:
        fails.append('tutorial: the ruler step must say the line carries on past both points (it is drawn 800 units beyond each)')
    if 'The line from V through this point is the locus inside this angle' not in html:
        fails.append('statement: task 9 must call the bisector the locus inside this angle (two lines have two bisectors)')
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof TASKS !== "undefined" && typeof loadTask === "function"', timeout=15000)
            n = page.evaluate('() => TASKS.length')
            if n != 10:
                fails.append('figure: %d tasks, expected 10' % n)
            mapping_checks(fails, page)
            page.evaluate('() => { loadTask(0); }')
            left, top, width = page.evaluate(PIN_JS)
            if (left, top, width) != (0, 0, 700):
                fails.append('harness: could not pin the canvas at (0, 0), 700 wide: %r' % ((left, top, width),))
            for i in range(n):
                rec = page.evaluate(RECORD_JS, i)
                check_task(fails, page, i, rec)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'tasks': n}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('the tutorial says the ruler line is drawn between the points', 'tutorial:',
     [("3. A straight line is drawn through both points and carries on past them<br>", "3. A straight line is drawn between them<br>")]),
    ('task 9 calls one bisector the whole locus', 'statement:',
     [("'The line from V through this point is the locus inside this angle'", "'The line from V through this point is the locus'")]),
    ('circle-circle crossings mirrored (wrong point)', 'tools:',
     [("return[{x:mx+h*dy/d,y:my-h*dx/d},{x:mx-h*dy/d,y:my+h*dx/d}];", "return[{x:mx+h*dy/d,y:my+h*dx/d},{x:mx-h*dy/d,y:my-h*dx/d}];")]),
    ('no snapping (snap distance 0.1)', 'tools:', [("const SNAP_DIST=12;", "const SNAP_DIST=0.1;")]),
    ('the compass radius 5% long', 'construction:',
     [("const r=Math.sqrt((snapped.x-firstClick.x)**2+(snapped.y-firstClick.y)**2);", "const r=1.05*Math.sqrt((snapped.x-firstClick.x)**2+(snapped.y-firstClick.y)**2);")]),
    ('"Angle BAC = 45°" stated for the 60° construction', 'statement:', [("'Angle BAC = 60° (equilateral triangle property)'", "'Angle BAC = 45° (equilateral triangle property)'")]),
    ('the steps state 100 pixels, the label 120px', 'statement:', [("'Set the radius to 120 pixels (use the grid lines as a guide)'", "'Set the radius to 100 pixels (use the grid lines as a guide)'")]),
    ('label B drawn far from B', 'figure:', [("drawLabel(c,190,215,'A');drawLabel(c,505,215,'B')", "drawLabel(c,190,215,'A');drawLabel(c,505,415,'B')")]),
    ('the tap mapping off by 2 units', 'tools:', [("return{x:(clientX-rect.left)*s,y:(clientY-rect.top)*s};", "return{x:(clientX-rect.left)*s+2,y:(clientY-rect.top)*s};")]),
    ('Lock Radius ignored (single click radius 50)', 'tools:',
     [("elements.push({type:'arc',cx:snapped.x,cy:snapped.y,r:lockedRadius});", "elements.push({type:'arc',cx:snapped.x,cy:snapped.y,r:50});")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    st = play(fails, html)
    print('%s: all %d tasks constructed with the game\'s own tools in Chromium; figures, labels, snapped crossings and every stated '
          'result checked' % (SLUG, st.get('tasks', 0)))
    print('  not verifiable (reported): the game marks no construction (t3-001); snap ignores given lines and points (t3-002); '
          'grid spacing and the unbounded locus line (t3-004); text and button sizes (t3-005)')
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-58s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            found = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(found)
            print('  self-test %-58s %s' % (what, ('caught: ' + found[0][:100]) if found else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
