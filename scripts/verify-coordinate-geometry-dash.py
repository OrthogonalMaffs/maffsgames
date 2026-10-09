#!/usr/bin/env python3
# ci-line: B2 | Coordinate Geometry Dash (every key recomputed from its question; exactly one correct option, equations compared as curves; every option marked in Chromium) |
"""Coordinate Geometry Dash: every key recomputed from its question, and exactly one option correct.

The game (45 multiple-choice items: gcse 24, alevel 21) asks for midpoints, gradients, lines, distances,
intersections, circles, tangents and parametric curves, each over a canvas. Its bank was keyed by hand with
no verifier. The tranche 1 audit of 6 Oct 2026 found alevel[13] (x = 3t, y = 4/t) offering xy = 12, y = 12/x
and x = 12/y, all correct, and keying "All equivalent", so each correct equation was marked wrong
(coordinate-geometry-dash-t1-001, HIGH; contract LISTED-HIGH, 9 Oct 2026: exactly one option keyed correct,
and no unkeyed option correct).

TARGETS gives each item's answer as a computation on the numbers in its own question, with the words those
numbers come from (an edited question fails until its target is reviewed), and how its options are read:
a point, a number, an equation, a centre and radius, or a fixed phrase. Equations are compared as curves:
two are the same when, with denominators cleared, one is a constant multiple of the other (so y = 12/x and
xy = 12 are the same equation). Then: the key equals the target; no other option does; and in Chromium
(390x844) every item is shown through nextQ() and every option clicked through handleAnswer(): the key
marked right, the others wrong. A self-test plants the audit's item back into a copy of the page; it must
FAIL naming alevel[13].

    python scripts/verify-coordinate-geometry-dash.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'coordinate-geometry-dash'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
X, Y = sp.symbols('x y')
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
SUBS = [('−', '-'), ('²', '**2'), ('³', '**3'), ('½', '(1/2)'), ('⅓', '(1/3)'), ('¾', '(3/4)')]
Q = sp.Rational


def expr(s):
    t = s.strip()
    for a, b in SUBS:
        t = t.replace(a, b)
    t = re.sub(r'√(\d+)', r' sqrt(\1)', t)
    if '∞' in t or not t:
        raise ValueError(s)
    return parse_expr(t, local_dict={'x': X, 'y': Y, 'sqrt': sp.sqrt}, transformations=TRANSFORMS)


def read_num(s):
    return sp.nsimplify(expr(s))


def read_point(s):
    m = re.fullmatch(r'\((.*),(.*)\)', s.strip())
    if not m:
        raise ValueError(s)
    return (read_num(m.group(1)), read_num(m.group(2)))


def read_eq(s):
    lhs, rhs = s.split('=')
    return sp.numer(sp.together(sp.expand(expr(lhs) - expr(rhs))))


def same_curve(p, q):
    r = sp.cancel(p / q)
    return not r.free_symbols and r != 0


def read_cr(s):
    m = re.fullmatch(r'(\(.*\)),\s*r\s*=\s*(.*)', s.strip())
    if not m:
        raise ValueError(s)
    return read_point(m.group(1)) + (read_num(m.group(2)),)


READ = {'point': read_point, 'num': read_num, 'eq': read_eq, 'cr': read_cr, 'text': lambda s: s.strip()}


def equal(kind, a, b):
    if kind == 'eq':
        return same_curve(a, b)
    if kind in ('point', 'cr'):
        return len(a) == len(b) and all(sp.simplify(u - v) == 0 for u, v in zip(a, b))
    if kind == 'num':
        return sp.simplify(a - b) == 0
    return a == b


def mid(a, b):
    return (Q(a[0] + b[0], 2), Q(a[1] + b[1], 2))


def grad(a, b):
    return None if a[0] == b[0] else Q(b[1] - a[1], b[0] - a[0])


def dist(a, b):
    return sp.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def line(m, p):
    return Y - (m * (X - p[0]) + p[1])


def circle(c, r2):
    return (X - c[0]) ** 2 + (Y - c[1]) ** 2 - r2


def centre_radius(eq):
    """x^2 + y^2 + Dx + Ey + F = 0 -> (centre x, centre y, radius)."""
    p = sp.Poly(sp.expand(eq), X, Y)
    d, e, f = p.coeff_monomial(X), p.coeff_monomial(Y), p.coeff_monomial(1)
    return (-d / 2, -e / 2, sp.sqrt(d ** 2 / 4 + e ** 2 / 4 - f))


def crossings(curve, ln):
    """How many real points the circle and the line share."""
    return len({s for s in sp.solve([curve, ln], [X, Y], dict=False) if all(v.is_real for v in s)})


def text(s):
    return ('text', s)


def area(p, q, r):
    return abs(Q((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]), 2))


def para(xt, yt):
    """The Cartesian equation of x = xt(t), y = yt(t), from the parameters (t eliminated by resultant)."""
    t = sp.Symbol('t')
    return sp.resultant(sp.numer(sp.together(X - xt(t))), sp.numer(sp.together(Y - yt(t))), t)


def dydx(xt, yt, at):
    t = sp.Symbol('t')
    return (sp.diff(yt(t), t) / sp.diff(xt(t), t)).subs(t, at)


# (words the ctx must carry, (reader, target)). In the page's order.
G = [
    ('A = (2, 3) and B = (6, 7)', ('point', mid((2, 3), (6, 7)))),
    ('A = (−3, 4) and B = (5, −2)', ('point', mid((-3, 4), (5, -2)))),
    ('A = (0, 0) and B = (8, 6)', ('point', mid((0, 0), (8, 6)))),
    ('A = (1, 2) and B = (5, 6)', ('num', grad((1, 2), (5, 6)))),
    ('A = (2, 1) and B = (6, 7)', ('num', grad((2, 1), (6, 7)))),
    ('A = (−2, 4) and B = (4, 1)', ('num', grad((-2, 4), (4, 1)))),
    ('A = (1, 3) and B = (1, 7)', text('Undefined (vertical)' if grad((1, 3), (1, 7)) is None else '?')),
    ('A = (1, 3) and B = (5, 3)', ('num', grad((1, 3), (5, 3)))),
    ('Line through (1, 1) with gradient 2', ('eq', line(2, (1, 1)))),
    ('Line through (2, 3) with gradient −1', ('eq', line(-1, (2, 3)))),
    ('the line through (1, 2) and (3, 8)', ('eq', line(grad((1, 2), (3, 8)), (1, 2)))),
    ('y = 2x + 1. Line B: y = 2x − 3', text('Parallel')),                       # equal gradients, different c
    ('Line A has gradient 2. Line B has gradient −½.', text('Perpendicular' if 2 * Q(-1, 2) == -1 else '?')),
    ('Line L: y = 3x + 1. Find the line perpendicular to L through (2, 5).', ('eq', line(Q(-1, 3), (2, 5)))),
    ('A = (1, 2) and B = (4, 6)', ('num', dist((1, 2), (4, 6)))),
    ('A = (−3, 1) and B = (1, 4)', ('num', dist((-3, 1), (1, 4)))),
    ('A = (0, 0) and B = (5, 5)', ('num', dist((0, 0), (5, 5)))),
    ('Which line is shown?', ('eq', line(grad((0, 2), (4, 4)), (0, 2)))),     # its q: through (0, 2) and (4, 4)
    ('y = −2x + 3', ('point', (Q(3, 2), 0))),                                   # -2x + 3 = 0
    ('A = (1, 2), B = (3, 4), C = (5, 6)',
     text('Yes — all on y = x + 1' if grad((1, 2), (3, 4)) == grad((3, 4), (5, 6)) == 1 and 2 == 1 + 1 else '?')),
    ('Line 1: y = x + 1. Line 2: y = −x + 5', ('point', tuple(sp.solve([Y - X - 1, Y + X - 5], [X, Y]).values()))),
    ('Line 1: y = 2x − 1. Line 2: y = ½x + 2',
     ('point', tuple(sp.solve([Y - 2 * X + 1, Y - X / 2 - 2], [X, Y]).values()))),
    ('Line L has gradient 2.', ('num', Q(-1, 2))),
    ('vertices (1,1), (5,1), (5,4)', ('num', dist((1, 1), (5, 4)))),
]
L = [
    ('Circle with centre (3, 4) and radius 3', ('eq', circle((3, 4), 9))),
    ('x² + y² = 25', ('cr', centre_radius(X ** 2 + Y ** 2 - 25))),
    ('(x−2)² + (y−3)² = 16', text({-1: 'Inside', 0: 'On the circle', 1: 'Outside'}[
        sp.sign(circle((2, 3), 16).subs({X: 6, Y: 3}))])),
    ('x² + y² − 6x − 4y = 0', ('cr', centre_radius(X ** 2 + Y ** 2 - 6 * X - 4 * Y))),
    ('x² + y² − 2x + 4y − 20 = 0', ('cr', centre_radius(X ** 2 + Y ** 2 - 2 * X + 4 * Y - 20))),
    ('Circle centre (3, 4). Point P = (6, 4)', text('Undefined (vertical)' if grad((3, 4), (6, 4)) == 0 else '?')),
    ('Circle centre (2, 3). Point P = (5, 4)', ('num', -1 / grad((2, 3), (5, 4)))),
    ('x² + y² = 25. Find the tangent at (3, 4).', ('eq', line(-1 / grad((0, 0), (3, 4)), (3, 4)))),
    ('Circle: (x−2)² + (y−2)² = 8. Line: y = x', text({2: '2', 1: '1 (tangent)', 0: '0'}[
        crossings(circle((2, 2), 8), Y - X)])),
    ('Circle: (x−3)² + (y−3)² = 9. Line: y = 9',
     text('No — line is above the circle' if crossings(circle((3, 3), 9), Y - 9) == 0 and 9 > 3 + 3 else '?')),
    ('parametrically: x = t, y = t²', ('eq', para(lambda t: t, lambda t: t ** 2))),
    ('x = 2cos t, y = 2sin t', ('eq', X ** 2 + Y ** 2 - 4)),                  # cos^2 + sin^2 = 1
    ('x = t + 1, y = t² − 2', ('eq', para(lambda t: t + 1, lambda t: t ** 2 - 2))),
    ('x = 3t, y = 4/t, t > 0', ('eq', para(lambda t: 3 * t, lambda t: 4 / t))),
    ('x = t, y = t³', ('num', dydx(lambda t: t, lambda t: t ** 3, 2))),
    ('x = 2t + 1, y = t² − 3', ('num', dydx(lambda t: 2 * t + 1, lambda t: t ** 2 - 3, 1))),
    ('Centre (1, 2), point (4, 6) on the circle', ('eq', circle((1, 2), dist((1, 2), (4, 6)) ** 2))),
    ('A = (1, 0), B = (5, 4)', ('eq', circle(mid((1, 0), (5, 4)), (dist((1, 0), (5, 4)) / 2) ** 2))),
    ('Line: y = 2x − 1. Circle: (x−2)² + (y−3)² = 5',
     text({2: 'Positive (2 points)', 1: '0 (tangent)', 0: 'Negative (no intersection)'}[
         crossings(circle((2, 3), 5), Y - 2 * X + 1)])),
    ('A = (−2, 3) and B = (4, −1)', ('eq', line(-1 / grad((-2, 3), (4, -1)), mid((-2, 3), (4, -1))))),
    ('vertices (0,0), (6,0), (3,5)', ('num', area((0, 0), (6, 0), (3, 5)))),
]
TARGETS = {'gcse': G, 'alevel': L}
AUDIT = {('alevel', 13): 'coordinate-geometry-dash-t1-001'}


def check_bank(fails, bank):
    for lv, targets in TARGETS.items():
        items = bank.get(lv, [])
        if len(items) != len(targets):
            fails.append('%s: %d items, expected %d (a change needs TARGETS reviewed)' % (lv, len(items), len(targets)))
            continue
        for i, q in enumerate(items):
            w = '%s[%d] (%s | %s)%s' % (lv, i, q['ctx'], q['q'], ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            words, (kind, target) = targets[i]
            if words not in q['ctx'] + ' ' + q['q']:
                fails.append('%s: the question must say "%s" for its target to hold' % (w, words))
            key = q.get('correct_override') or q['correct']
            opts = list(q['opts'])
            if len(opts) != 4 or len(set(opts)) != 4 or key not in opts:
                fails.append('%s: the options %s are not four distinct strings including the key' % (w, opts))
                continue
            right = []
            for o in opts:
                try:
                    v = READ[kind](o)
                except Exception:
                    continue                         # not a reading of this kind ("Undefined", "∞"): not the target
                if equal(kind, v, target):
                    right.append(o)
            if key not in right:
                fails.append('%s: keyed %s, the answer is %s' % (w, key, target))
            for o in right:
                if o != key:
                    fails.append('%s: the unkeyed option %s is also correct' % (w, o))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [], banks = {gcse: Q_GCSE, alevel: Q_ALEVEL};
  for (const [lv, items] of Object.entries(banks)) items.forEach((q, i) => {
    const key = q.correct_override || q.correct;
    for (const pick of q.opts) {
      pool = [q]; qIdx = 0; total = 0; score = 0; correctN = 0; level = lv;
      nextQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([lv, i, pick, shown.length + ' options on screen']);
      const btn = shown.find(x => x.dataset.val === pick);
      if (!btn) { out.push([lv, i, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === key)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?level=alevel&cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof Q_ALEVEL !== "undefined"', timeout=15000)
            page.evaluate("() => show('game')")
            bank = page.evaluate('() => ({gcse: Q_GCSE, alevel: Q_ALEVEL})')
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d] in Chromium: option %s %s' % (lv, i, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('alevel[13]', 't1-001: three correct equations, keyed "All equivalent"',
     'opts:["xy = 12","xy = 7","y = 12x","x = 3y/4"],correct:"xy = 12"',
     'opts:["xy = 12","y = 12/x","x = 12/y","All equivalent"],correct:"All equivalent"'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items, every key recomputed, every option read and clicked in Chromium'
          % (SLUG, sum(len(v) for v in (bank or {}).values())))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
