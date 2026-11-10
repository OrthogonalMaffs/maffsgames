#!/usr/bin/env python3
# ci-shards: CAST Away (every question of the four stages recomputed independently: k read from the TeX the student sees, every solution of sin, cos or tan x = k found by a numeric root search in mpmath on the stated interval, never by the CAST rule, rounded half up to 1 d.p. or kept whole; keys, the shown alpha, Stage 2's quadrants and Stage 1's snap points (each on the curve); every option's set wrong and its named mistake true; every feedback rule fired by a planted typed answer, taps and quadrants; the working's arithmetic; sessions of 10 with their mix; the three walkthroughs word for word against the contract and their numbers recomputed; every stage played in the page at 390 px and the first questions at 375, 320, 1366 and 1280 px and in Aa mode: the controls and Next above the fold, no sideways scroll, one board submission a stage, the score right first time only, the character band on the start and results screens only and still under reduced motion; fault-injection self-test) | | 3
# ci-deps: games/cast-away/
r"""Independent verification for CAST Away (games/cast-away/), built 10 Nov 2026 (contract CAST-AWAY-BUILD, Project Claude).
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The game generates its questions in the page (CA.pool, CA.session) and solves them by the method it teaches: alpha = the
inverse of |k|, then the CAST rule, each form taken with its 360-degree neighbours and filtered to the interval. This script
never uses that rule. For every question it reads k from the question's own TeX (0.5, \tfrac{1}{\sqrt{2}}, -\sqrt{3}, ...),
evaluated exactly in mpmath at 50 digits, and finds every x in the stated interval (0 <= x < 360 or 0 <= x <= 360, degrees)
with f(x) = k by a root search: a float scan every 0.25 degrees for sign changes and near-zeros, each refined by bisection
in mpmath and accepted only if |f(x) - k| < 1e-30 (an asymptote of tan, a jump with no root, is refused). Then:

  Keys      a root that is a whole number of degrees (to 1e-30) is kept whole; otherwise it is rounded half up to 1 d.p.
            (Decimal, from 40 digits); a root within 1e-6 of a rounding tie fails (the key would be fragile). The game's
            keys must equal these exactly, in order, and its whole flag must say which kind they are.
  Alpha     the shown alpha (Stage 3's "from your calculator", the working's first line) is the inverse of |k|, computed
            here, at the key's precision.
  Quadrants Stage 2's key is the set of quadrants the roots lie in (none on an axis).
  Snaps     every point a Stage 1 tap can snap to lies on the curve and the line (f(x) = k to 1e-9); together they are the
            roots, plus 360 for an open interval whose 360 solves it (a tap there is the named mistake).
  Options   Stage 1: four distinct sets, the roots' once, every other set different from it and each the mistake it is
            named for, checked by its own definition here (another function's rule: the solutions of g(x) = sign(k) g(alpha);
            the wrong sign: the solutions of f(x) = -k; the calculator's negative angle: -alpha in place of its positive
            partner; 360 in an open interval; a missed solution: a proper subset; a 180-degree period for sin or cos; a value
            beyond 360). Stage 2: four pairs of forms, only the key's pair giving the roots when alpha is put in.
  Feedback  every rule fired by a planted answer built here and named as it should be: right in any order; a missed
            solution; another function's rule; the wrong sign; the calculator's negative angle kept; 360 when the interval
            stops before it; a value out of range; a 180-degree period; a value that solves nothing; "No solutions" when there
            are some; an answer when there are none; the format message for the right value at 2 d.p. (never marked); taps:
            a missed crossing and the open end at 360; quadrants: the other sign's, another function's, only one.
  Working   every "a +- b = c" in the full working is true, the alpha line is alpha, and the last line's solutions are the keys.
  Sessions  10 distinct equations from the pool, the stage's mix of kinds, at most 4 of one function.
  Walkthroughs  each step's text, with its TeX read back to plain text, equals the contract's script word for word, and the
            numbers in it are recomputed here: 30 and 150; 66.4, 113.6 and 246.4; -45, 135 and 315.
  Page      every stage played: one game_completed and one leaderboard submission a stage, on board stage-N, the score the
            questions right first time; the answer controls and Next above the fold; no sideways scroll; the stage's
            calculator badge in the header and the scientific calculator mounted; the keypad on a touch screen in the typed
            stages; the character band on the start and results screens only, drifting, and still under reduced motion.

Work units (contract SHARD): "engine" (the maths, on one 1280x800 page), "walk" (the walkthroughs and the start screen),
"full 390x844" (every stage played through), "first WxH" (the first questions of every stage at another size), "aa WxH"
(Aa mode at the gate's sizes) and "plant: <what>" (one per planted fault).

    python scripts/verify-cast-away.py                 # every unit
    python scripts/verify-cast-away.py --katex-dir DIR # a sandbox without the CDN: serve KaTeX 0.16.9 from a local dist/
"""
import argparse
import contextlib
import math
import mimetypes
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

import mpmath  # noqa: E402

mpmath.mp.dps = 50
SLUG = 'cast-away'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
FULL = (390, 844)
FIRST = [(375, 667), (320, 568), (1366, 768), (1280, 720)]
AA = [(375, 667), (390, 844)]
FOOTER = 40
MIN_DISTINCT = 40
KATEX_DIR = None
QUOTA = {1: {'std': 7, 'special': 3}, 2: {'std': 4, 'non': 6}, 3: {'non': 6, 'std': 2, 'special': 2},
         4: {'non': 6, 'std': 1, 'special': 2, 'impossible': 1}}
CALC = {1: 'optional', 2: 'optional', 3: 'optional', 4: 'scientific'}

# The contract's scripts (CAST-AWAY-BUILD, item 6), word for word.
CONTRACT_WALK = {
    'sin': ('Solve sin x = 0.5 for 0° ≤ x < 360°.', [
        "Your calculator says sin⁻¹(0.5) = 30°. That's one answer.",
        "But look at the graph: the line y = 0.5 crosses the sine curve twice between 0° and 360°.",
        "Sine is positive in the S and A quadrants — the first two.",
        "In the S quadrant the angle is 180° − 30° = 150°.",
        "Check the interval: 30° and 150° are both in it.",
        "x = 30° or x = 150°. Not one. Not infinity. Two."]),
    'cos': ('Solve cos x = −0.4 for 0° ≤ x < 360°, to 1 d.p.', [
        "Start with the size: cos⁻¹(0.4) = 66.4°. Call it α.",
        "The answer is negative, so cosine must be negative: the S and T quadrants.",
        "In S: 180° − 66.4° = 113.6°.",
        "In T: 180° + 66.4° = 246.4°.",
        "On the graph, y = −0.4 crosses the cosine curve at exactly those two places.",
        "x = 113.6° or x = 246.4°."]),
    'tan': ('Solve tan x = −1 for 0° ≤ x ≤ 360°.', [
        "Your calculator says tan⁻¹(−1) = −45°. That's not in the interval — don't stop there.",
        "Take the size: α = 45°.",
        "Tangent is negative in the S and C quadrants.",
        "In S: 180° − 45° = 135°. In C: 360° − 45° = 315°.",
        "The dashed lines at 90° and 270° are asymptotes: the graph never touches them, and it crosses y = −1 once between each pair.",
        "x = 135° or x = 315°."]),
}
# The numbers each walkthrough must show: (function, k, closed, the calculator's reading, alpha, the solutions).
WALK_MATHS = {'sin': ('sin', mpmath.mpf('0.5'), False, '30', '30', ['30', '150']),
              'cos': ('cos', mpmath.mpf('-0.4'), False, None, '66.4', ['113.6', '246.4']),
              'tan': ('tan', mpmath.mpf(-1), True, '-45', '45', ['135', '315'])}


# ---------------------------------------------------------------- the independent maths
def tex_value(t):
    """The exact value of k as the student reads it: a decimal, \\tfrac{a}{b}, \\sqrt{n}, with a leading minus."""
    t = t.strip()
    if t.startswith('-'):
        return -tex_value(t[1:])
    m = re.fullmatch(r'\\tfrac\{(.*)\}\{(.*)\}', t)
    if m:
        return tex_value(m.group(1)) / tex_value(m.group(2))
    m = re.fullmatch(r'\\sqrt\{(\d+)\}', t)
    if m:
        return mpmath.sqrt(int(m.group(1)))
    if re.fullmatch(r'\d+(\.\d+)?', t):
        return mpmath.mpf(t)
    raise ValueError('cannot read k from %r' % t)


def fx(fn, d):
    r = mpmath.mpf(d) * mpmath.pi / 180
    return mpmath.sin(r) if fn == 'sin' else mpmath.cos(r) if fn == 'cos' else mpmath.tan(r)


def ff(fn, d):
    r = math.radians(d)
    return math.sin(r) if fn == 'sin' else math.cos(r) if fn == 'cos' else math.tan(r)


_ROOTS = {}


def roots(fn, k, closed):
    """Every x in [0, 360) or [0, 360] with fn(x) = k, by a scan and bisection; never by a rule."""
    key = (fn, mpmath.nstr(k, 45), closed)
    if key in _ROOTS:
        return _ROOTS[key]
    kf = float(k)
    step = 0.25
    xs = [i * step for i in range(int(360 / step) + 1)]
    out = []

    def add(x):
        if not any(abs(x - y) < mpmath.mpf('1e-20') for y in out):
            out.append(x)

    def on_curve(x):
        if fn == 'tan' and abs(float(x) % 180 - 90) < 1e-9:
            return False
        return abs(fx(fn, x) - k) < mpmath.mpf('1e-30')
    prev = None
    for x in xs:
        gx = ff(fn, x) - kf if not (fn == 'tan' and abs(x % 180 - 90) < 1e-12) else None
        if gx is not None and abs(gx) < 1e-9 and on_curve(x):
            add(mpmath.mpf(x))
        if prev is not None and gx is not None and prev[1] is not None and prev[1] * gx < 0 and abs(prev[1]) < 50 and abs(gx) < 50:
            a, b = mpmath.mpf(prev[0]), mpmath.mpf(x)
            ga = fx(fn, a) - k
            for _ in range(200):
                m = (a + b) / 2
                gm = fx(fn, m) - k
                if gm == 0 or (b - a) < mpmath.mpf('1e-45'):
                    break
                if (ga < 0) == (gm < 0):
                    a, ga = m, gm
                else:
                    b = m
            m = (a + b) / 2
            if on_curve(m):
                add(m)
        prev = (x, gx)
    out = sorted(x for x in out if x >= 0 and (x <= 360 if closed else x < 360 - mpmath.mpf('1e-20')))
    _ROOTS[key] = out
    return out


def is_whole(x):
    return abs(x - mpmath.nint(x)) < mpmath.mpf('1e-30')


def half_up(x, places=1):
    d = Decimal(mpmath.nstr(x, 40, strip_zeros=False))
    return d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def tie(x):
    t = x * 10 - mpmath.floor(x * 10)
    return abs(t - mpmath.mpf('0.5')) < mpmath.mpf('1e-6')


def key_of(x, whole):
    return int(mpmath.nint(x)) if whole else half_up(x)


def as_num(v):
    """A page number (int or float) as an exact Decimal, for comparing with this script's keys."""
    return Decimal(repr(v)) if isinstance(v, float) else Decimal(v)


def inv(fn, m):
    v = mpmath.asin(m) if fn == 'sin' else mpmath.acos(m) if fn == 'cos' else mpmath.atan(m)
    return v * 180 / mpmath.pi


def expected(q):
    """(keys, whole, roots, alpha) recomputed for a page question."""
    k = tex_value(q['tex'])
    rs = roots(q['fn'], k, q['closed'])
    whole = all(is_whole(r) for r in rs) if rs else True
    alpha = inv(q['fn'], abs(k)) if abs(k) <= 1 or q['fn'] == 'tan' else None
    return [key_of(r, whole) for r in rs], whole, rs, alpha, k


def quadrant(x):
    x = float(x) % 360
    if abs(x % 90) < 1e-9:
        return None
    return 'A' if x < 90 else 'S' if x < 180 else 'T' if x < 270 else 'C'


def keyset(xs, whole):
    return sorted(Decimal(int(x)) if whole else Decimal(x) for x in xs)


def fmt(v, whole):
    return str(int(v)) if whole else str(Decimal(v).quantize(Decimal('0.1')))


# ---------------------------------------------------------------- the page
def open_page(pw, base, html, size, aa=False, reduced=False, touch=None):
    br = pw.chromium.launch()
    if touch is None:
        touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch,
                         reduced_motion='reduce' if reduced else 'no-preference')
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    if aa:
        ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    if KATEX_DIR:
        def kx(route):
            path = route.request.url.split('/dist/', 1)[1].split('?')[0]
            fp = os.path.join(KATEX_DIR, path)
            if os.path.exists(fp):
                route.fulfill(status=200, body=open(fp, 'rb').read(), content_type=mimetypes.guess_type(fp)[0] or 'application/octet-stream')
            else:
                route.abort()
        ctx.route(re.compile(r'https://cdn\.jsdelivr\.net/npm/katex@0\.16\.9/dist/.*'), kx)
    ctx.route(lambda url: not url.startswith(base) and 'cdn.jsdelivr.net/npm/katex' not in url, lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
    page.wait_for_function('!!window.CA && !!CA.ui', timeout=15000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


# ---------------------------------------------------------------- engine checks
def check_question(q, out, info):
    tag = q['id']
    try:
        keys, whole, rs, alpha, k = expected(q)
    except ValueError as e:
        out.append('%s: %s' % (tag, e))
        return None
    if abs(float(k) - q['k']) > 1e-12:
        out.append('%s: the page computes k = %r but its TeX %r is %s' % (tag, q['k'], q['tex'], mpmath.nstr(k, 15)))
    if q['kind'] == 'impossible':
        if rs or abs(k) <= 1 or q['fn'] == 'tan':
            out.append('%s: marked impossible but has roots %s' % (tag, [mpmath.nstr(r, 8) for r in rs]))
        if q['keys']:
            out.append('%s: keys %s for an equation with no solutions' % (tag, q['keys']))
        return (keys, whole, rs, alpha, k)
    if not rs:
        out.append('%s: no solutions found here but the game says %s' % (tag, q['keys']))
        return None
    for r in rs:
        if not whole and tie(r):
            out.append('%s: the root %s is within 1e-6 of a rounding tie' % (tag, mpmath.nstr(r, 20)))
    if [as_num(v) for v in q['keys']] != [Decimal(v) for v in keys]:
        out.append('%s: keys %s, but the solutions of %s x = %s in the interval are %s' % (tag, q['keys'], q['fn'], q['tex'], [str(v) for v in keys]))
    if bool(q['whole']) != whole:
        out.append('%s: whole is %s, but the roots %s' % (tag, q['whole'], 'are whole' if whole else 'are not whole'))
    if len(q['sols']) != len(rs) or any(abs(a - float(b)) > 1e-7 for a, b in zip(q['sols'], rs)):
        out.append('%s: exact solutions %s differ from %s' % (tag, q['sols'], [mpmath.nstr(r, 10) for r in rs]))
    a_exp = key_of(alpha, whole)
    if as_num(q['alphaShown']) != Decimal(a_exp):
        out.append('%s: the shown alpha is %s, but the inverse of |k| is %s' % (tag, q['alphaShown'], a_exp))
    if not whole and tie(alpha):
        out.append('%s: alpha %s is near a rounding tie' % (tag, mpmath.nstr(alpha, 20)))
    if q['stage'] == 2:
        quads = sorted(quadrant(r) for r in rs)
        if None in quads:
            out.append('%s: Stage 2 question with a solution on an axis' % tag)
        elif q['quads'] != quads:
            out.append('%s: quadrants %s, but the solutions lie in %s' % (tag, q['quads'], quads))
    return (keys, whole, rs, alpha, k)


def other_rule(fn, g, k, alpha, closed, whole):
    """Another function's rule, by its definition here: the solutions of g(x) = sign(k) * g(alpha)."""
    s = -1 if k < 0 else 1
    return [key_of(r, whole) for r in roots(g, s * fx(g, alpha), closed)]


def sign_rule(fn, k, closed, whole):
    return [key_of(r, whole) for r in roots(fn, -k, closed)]


def true_mistake(q, m, exp, out, tag):
    """The set m['set'] is the mistake m['why'] names."""
    keys, whole, rs, alpha, k = exp
    S = sorted(Decimal(str(v)) for v in m['set'])
    K = sorted(Decimal(v) for v in keys)
    w = m['why']
    ok = True
    if S == K:
        out.append('%s: option %s (%s) equals the solutions' % (tag, m['set'], w))
        return False
    if w == 'fn':
        ok = S == sorted(Decimal(v) for v in other_rule(q['fn'], m['fn2'], k, alpha, q['closed'], whole))
    elif w == 'sign':
        ok = S == sorted(Decimal(v) for v in sign_rule(q['fn'], k, q['closed'], whole))
    elif w == 'neg':
        na = -Decimal(key_of(alpha, whole))
        ok = k < 0 and na in S and all(x in K for x in S if x != na) and len(S) == len(K)
    elif w == 'end360':
        ok = not q['closed'] and Decimal(360) in S and [x for x in S if x != 360] == K
    elif w == 'missed':
        ok = len(S) < len(K) and all(x in K for x in S)
    elif w == 'period':
        ok = q['fn'] != 'tan' and all(any(abs(x - y) in (0, 180) for y in K) for x in S) and all(x in S for x in K)
    elif w == 'range':
        ok = any(x > 360 for x in S) and all(x in K for x in S if x <= 360)
    else:
        ok = False
    if not ok:
        out.append('%s: option %s is named %s%s, which it is not' % (tag, m['set'], w, ' (' + m.get('fn2', '') + ')' if w == 'fn' else ''))
    return ok


def check_engine(page, out):
    info = {}
    for n in (1, 2, 3, 4):
        pool = page.evaluate('n => CA.pool(n)', n)
        ids = set(q['id'] for q in pool)
        if len(ids) != len(pool):
            out.append('stage %d: repeated question ids' % n)
        eqs = set()
        exps = {}
        for q in pool:
            if q['stage'] != n:
                out.append('%s: in the stage %d pool' % (q['id'], n))
            if n == 1 and q['kind'] not in ('std', 'special'):
                out.append('%s: Stage 1 is standard values only' % q['id'])
            if n == 2 and q['kind'] in ('special', 'impossible'):
                out.append('%s: Stage 2 has an axis value' % q['id'])
            if q['kind'] == 'impossible' and n != 4:
                out.append('%s: no solutions outside Stage 4' % q['id'])
            e = check_question(q, out, info)
            if e is not None:
                exps[q['id']] = e
                eqs.add((q['fn'], mpmath.nstr(e[4], 30)))
        distinct = len(ids)
        info[n] = {'questions': distinct, 'equations': len(eqs)}
        if distinct < MIN_DISTINCT:
            out.append('stage %d: %d distinct questions (fewer than %d)' % (n, distinct, MIN_DISTINCT))
        # sessions
        for seed in range(1, 201):
            s = page.evaluate('([n, s]) => CA.session(n, s)', [n, seed])
            kinds = {}
            fns = {}
            for q in s:
                kinds[q['kind']] = kinds.get(q['kind'], 0) + 1
                fns[q['fn']] = fns.get(q['fn'], 0) + 1
            if len(s) != 10 or len(set(q['eq'] for q in s)) != 10 or any(q['id'] not in ids for q in s):
                out.append('stage %d seed %d: the session is not 10 distinct pool questions' % (n, seed))
            if kinds != QUOTA[n]:
                out.append('stage %d seed %d: the session mix is %s, not %s' % (n, seed, kinds, QUOTA[n]))
            if max(fns.values()) > 4:
                out.append('stage %d seed %d: %s' % (n, seed, fns))
        # options
        if n == 1:
            snaps = page.evaluate('ids => ids.map(id => CA.snaps(1, id))', [q['id'] for q in pool])
            for q, sn in zip(pool, snaps):
                keys, whole, rs, alpha, k = exps.get(q['id'], (None,) * 5)
                if rs is None:
                    continue
                for x in sn:
                    if abs(fx(q['fn'], x) - k) > mpmath.mpf('1e-9'):
                        out.append('%s: the snap point %s is not on the curve' % (q['id'], x))
                want = [float(r) for r in rs] + ([360.0] if not q['closed'] and any(r == 0 for r in rs) else [])
                if sorted(round(x, 6) for x in sn) != sorted(round(x, 6) for x in want):
                    out.append('%s: snap points %s, the crossings are %s' % (q['id'], sn, want))
            for seed in (1, 2, 3):
                opts = page.evaluate('([ids, s]) => ids.map(id => CA.options(1, id, s))', [[q['id'] for q in pool], seed])
                for q, os_ in zip(pool, opts):
                    exp = exps.get(q['id'])
                    if exp is None:
                        continue
                    if len(os_) != 4 or len(set(o['id'] for o in os_)) != 4:
                        out.append('%s: Stage 1 shows %d distinct options' % (q['id'], len(set(o['id'] for o in os_))))
                    K = sorted(Decimal(v) for v in exp[0])
                    rights = [o for o in os_ if sorted(Decimal(str(v)) for v in o['set']) == K]
                    if len(rights) != 1 or rights[0]['why'] != 'right':
                        out.append('%s: the solutions are among the options %d times' % (q['id'], len(rights)))
                    for o in os_:
                        if o['why'] != 'right':
                            true_mistake(q, o, exp, out, q['id'])
        if n == 2:
            opts = page.evaluate('ids => ids.map(id => CA.options(2, id, 1))', [q['id'] for q in pool])
            FORM = {'a': lambda a: a, '180-a': lambda a: 180 - a, '180+a': lambda a: 180 + a, '360-a': lambda a: 360 - a}
            for q, os_ in zip(pool, opts):
                exp = exps.get(q['id'])
                if exp is None:
                    continue
                keys, whole, rs, alpha, k = exp
                K = sorted(Decimal(v) for v in keys)
                good = [o for o in os_ if sorted(Decimal(key_of(FORM[f](alpha), whole)) for f in o['forms']) == K]
                if len(os_) != 4 or len(set(o['id'] for o in os_)) != 4 or len(good) != 1 or good[0]['why'] != 'right':
                    out.append('%s: Stage 2 options: %d of %d give the solutions' % (q['id'], len(good), len(os_)))
        # feedback rules, planted
        if n in (3, 4):
            check_feedback(page, n, pool, exps, out, info)
        if n == 1:
            check_taps(page, pool, exps, out)
        if n == 2:
            check_quads(page, pool, exps, out)
        check_working(page, n, pool, exps, out)
    return info


def plant_list(q, exp):
    """[(raws, none, the kind or why the game must answer)] for one typed question."""
    keys, whole, rs, alpha, k = exp
    F = lambda v: fmt(v, whole)  # noqa: E731
    P = []
    if q['kind'] == 'impossible':
        return [([], True, 'right'), (['90'], False, 'impossible'), (['abc'], False, 'unreadable'), ([], False, 'empty')]
    K = [Decimal(v) for v in keys]
    P.append(([F(v) for v in reversed(keys)], False, 'right'))
    if whole:
        P.append(([str(v) + '.0' for v in keys], False, 'right'))
    P.append(([], True, 'nonebut'))
    P.append(([F(keys[0]), F(keys[0])], False, 'twice'))
    P.append((['abc'], False, 'unreadable'))
    P.append(([], False, 'empty'))
    if len(keys) >= 2:
        P.append(([F(v) for v in keys[:-1]], False, 'missed'))
    if not whole:
        P.append(([F(keys[0]) + '1'] + [F(v) for v in keys[1:]], False, 'format'))
    fnsets = {}
    for g in ('sin', 'cos', 'tan'):
        if g != q['fn']:
            fnsets[g] = [Decimal(v) for v in other_rule(q['fn'], g, k, alpha, q['closed'], whole)]
    sgn = [Decimal(v) for v in sign_rule(q['fn'], k, q['closed'], whole)] if k != 0 else []
    taken = set(K)
    for g, S in fnsets.items():
        for v in S:
            if v not in taken:
                P.append(([F(x) for x in keys[:-1]] + [str(v)], False, 'fn'))
                break
    allfn = set(x for S in fnsets.values() for x in S)
    for v in sgn:
        if v not in taken and v not in allfn:
            P.append(([F(x) for x in keys[:-1]] + [str(v)], False, 'sign'))
            break
    if k < 0 and q['fn'] in ('sin', 'tan'):     # cosine's calculator angle is positive (180 - alpha)
        na = -Decimal(key_of(alpha, whole))
        partner = Decimal(360) + na
        rest = [str(x) for x in K if x != partner]
        if partner in K:
            P.append(([str(na)] + rest, False, 'neg'))
    if not q['closed'] and Decimal(0) in K:
        P.append(([F(v) for v in keys] + ['360'], False, 'end360'))
    P.append(([F(v) for v in keys] + ['400' if whole else '400.5'], False, 'range'))
    if q['fn'] != 'tan':
        for x in K:
            for y in (x + 180, x - 180):
                if 0 <= y < (361 if q['closed'] else 360) and y not in taken and y not in allfn and y not in sgn:
                    P.append(([str(v) for v in K] + [str(y)], False, 'period'))
                    break
            else:
                continue
            break
    period = set(y for x in K for y in (x + 180, x - 180))
    for c in ([7, 11, 13, 17, 19, 23] if whole else ['7.7', '11.3', '13.9', '17.1', '19.4']):
        c = Decimal(c)
        if c not in taken and c not in allfn and c not in sgn and c not in period:
            P.append(([str(c)], False, 'notsol'))
            break
    return P


def check_feedback(page, n, pool, exps, out, info):
    items, want = [], []
    for q in pool:
        exp = exps.get(q['id'])
        if exp is None:
            continue
        for raws, none, w in plant_list(q, exp):
            items.append([n, q['id'], raws, none])
            want.append(w)
    got = page.evaluate('items => items.map(([n, id, raws, none]) => CA.markTyped(n, id, raws, none))', items)
    fired = {}
    for (nn, qid, raws, none), w, r in zip(items, want, got):
        name = r.get('why') or r['kind']
        if r['kind'] in ('format', 'unreadable', 'empty', 'twice'):
            name = r['kind']
        if r['kind'] == 'right':
            name = 'right'
        if name != w:
            out.append('%s: typed %s%s: the game says %s, it should say %s' % (qid, raws, ' and No solutions' if none else '', name, w))
        else:
            fired[w] = fired.get(w, 0) + 1
    info.setdefault('fired', {})
    for w, c in fired.items():
        info['fired'][w] = info['fired'].get(w, 0) + c
    # 'period' is not required here: a typed value 180 degrees from a solution always solves another named mistake too
    # (another function's rule or the wrong sign), which the game names first; Stage 1's options carry it (true_mistake).
    for w in (['right', 'missed', 'fn', 'sign', 'neg', 'end360', 'range', 'notsol', 'nonebut', 'format', 'unreadable', 'twice', 'empty']
              + (['impossible'] if n == 4 else [])):
        if not fired.get(w):
            out.append('stage %d: the feedback rule %r never fired on a planted answer' % (n, w))


def check_taps(page, pool, exps, out):
    items, want = [], []
    for q in pool:
        exp = exps.get(q['id'])
        if exp is None:
            continue
        rs = [float(r) for r in exp[2]]
        items.append([q['id'], rs]); want.append('right')
        if len(rs) >= 2:
            items.append([q['id'], rs[:-1]]); want.append('missed')
        items.append([q['id'], []]); want.append('missed')
        if not q['closed'] and 0.0 in rs:
            items.append([q['id'], rs + [360.0]]); want.append('end360')
    got = page.evaluate('items => items.map(([id, t]) => CA.markTaps(1, id, t))', items)
    seen = set()
    for (qid, t), w, r in zip(items, want, got):
        name = 'right' if r['kind'] == 'right' else r.get('why')
        if name != w:
            out.append('%s: taps at %s: the game says %s, it should say %s' % (qid, t, name, w))
        seen.add(name)
    for w in ('right', 'missed', 'end360'):
        if w not in seen:
            out.append('stage 1: the tap rule %r never fired' % w)


def check_quads(page, pool, exps, out):
    items, want = [], []
    for q in pool:
        exp = exps.get(q['id'])
        if exp is None:
            continue
        keys, whole, rs, alpha, k = exp
        key = sorted(quadrant(r) for r in rs)
        items.append([q['id'], key]); want.append('right')
        items.append([q['id'], key[:1]]); want.append('quadmissed')
        other = sorted(quadrant(r) for r in roots(q['fn'], -k, q['closed']))
        items.append([q['id'], other]); want.append('quadsign')
        for g in ('sin', 'cos', 'tan'):
            if g == q['fn']:
                continue
            s = -1 if k < 0 else 1
            gq = sorted(quadrant(r) for r in roots(g, s * fx(g, mpmath.mpf(45)), True))
            if gq not in (key, other):
                items.append([q['id'], gq]); want.append('quadfn')
    got = page.evaluate('items => items.map(([id, p]) => CA.markQuads(2, id, p))', items)
    seen = set()
    for (qid, p), w, r in zip(items, want, got):
        name = 'right' if r['kind'] == 'right' else r.get('why')
        if name != w:
            out.append('%s: quadrants %s: the game says %s, it should say %s' % (qid, p, name, w))
        seen.add(name)
    for w in ('right', 'quadmissed', 'quadsign', 'quadfn'):
        if w not in seen:
            out.append('stage 2: the quadrant rule %r never fired' % w)


ARITH = re.compile(r'(-?\d+(?:\.\d+)?)\^\\circ\s*([-+])\s*(-?\d+(?:\.\d+)?)\^\\circ\s*=\s*(-?\d+(?:\.\d+)?)\^\\circ')
XEQ = re.compile(r'x = (-?\d+(?:\.\d+)?)\^\\circ')


def check_arith(text, tag, out):
    for a, op, b, c in ARITH.findall(text):
        a, b, c = Decimal(a), Decimal(b), Decimal(c)
        if (a + b if op == '+' else a - b) != c:
            out.append('%s: the working says %s %s %s = %s' % (tag, a, op, b, c))


def check_working(page, n, pool, exps, out):
    lines = page.evaluate('([n, ids]) => ids.map(id => CA.working(n, id))', [n, [q['id'] for q in pool]])
    for q, L in zip(pool, lines):
        exp = exps.get(q['id'])
        if exp is None or not L:
            continue
        keys, whole, rs, alpha, k = exp
        text = ' '.join(L)
        check_arith(text, q['id'], out)
        if q['kind'] == 'impossible':
            if 'no solutions' not in L[-1]:
                out.append('%s: the working does not say there are no solutions' % q['id'])
            continue
        m = re.search(r'\\alpha = \\(sin|cos|tan)\^\{-1\}.*?= (-?\d+(?:\.\d+)?)\^\\circ', L[0])
        if not m or Decimal(m.group(2)) != Decimal(key_of(alpha, whole)):
            out.append('%s: the working\'s alpha line %r' % (q['id'], L[0]))
        last = sorted(Decimal(x) for x in XEQ.findall(L[-1]))
        if last != sorted(Decimal(v) for v in keys):
            out.append('%s: the working ends with %s, the solutions are %s' % (q['id'], last, keys))


# ---------------------------------------------------------------- the walkthroughs
def plain(t):
    """A walkthrough line with its maths read back to plain text (the TeX between \\( and \\))."""
    def m(s):
        s = s.replace('\\sin', 'sin').replace('\\cos', 'cos').replace('\\tan', 'tan')
        s = s.replace('^{-1}', '⁻¹').replace('^\\circ', '°').replace('\\le', '≤').replace('\\alpha', 'α')
        s = s.replace('-', '−')
        return s
    parts = re.split(r'\\\(|\\\)', t)
    return ''.join(m(p) if i % 2 else p for i, p in enumerate(parts))


def check_walk(page, out, info):
    walk = page.evaluate('CA.WALK')
    for fn, (ask, steps) in CONTRACT_WALK.items():
        w = walk.get(fn)
        if not w:
            out.append('walkthrough %s: missing' % fn)
            continue
        if plain(w['ask']) != ask:
            out.append('walkthrough %s: %r is not the contract\'s %r' % (fn, plain(w['ask']), ask))
        got = [plain(s['text']) for s in w['steps']]
        if len(got) != 6:
            out.append('walkthrough %s: %d steps, not 6' % (fn, len(got)))
        for i, (g, c) in enumerate(zip(got, steps)):
            if g != c:
                out.append('walkthrough %s step %d: %r, the contract says %r' % (fn, i + 1, g, c))
            check_arith(w['steps'][i]['text'], 'walkthrough %s step %d' % (fn, i + 1), out)
        # the numbers, recomputed
        f, k, closed, calc, a, sols = WALK_MATHS[fn]
        rs = roots(f, k, closed)
        whole = all(is_whole(r) for r in rs)
        mine = [str(key_of(r, whole)) for r in rs]
        if mine != sols:
            out.append('walkthrough %s: the solutions are %s, the script says %s (STOP IF: report to Jon)' % (fn, mine, sols))
        alpha = inv(f, abs(k))
        if str(key_of(alpha, is_whole(alpha))) != a:
            out.append('walkthrough %s: alpha is %s, the script says %s' % (fn, key_of(alpha, is_whole(alpha)), a))
        if calc is not None:
            c = inv(f, k)
            if str(key_of(c, is_whole(c))) != calc:
                out.append('walkthrough %s: the calculator gives %s, the script says %s' % (fn, key_of(c, is_whole(c)), calc))
        nums = set(re.findall(r'−?\d+(?:\.\d+)?', ' '.join(steps)))
        allowed = set(sols) | {a, '180', '360', '0', '90', '270', '0.5', '0.4', '1', '−0.4', '−1'} | ({calc.replace('-', '−')} if calc else set())
        for x in nums:
            if x not in allowed:
                out.append('walkthrough %s: the number %s in the script is not one recomputed here' % (fn, x))
        wq = page.evaluate('fn => CA.walkQ(fn)', fn)
        if [str(as_num(v)) for v in wq['keys']] != sols:
            out.append('walkthrough %s: the figures light %s, the solutions are %s' % (fn, wq['keys'], sols))
        info.setdefault('walk', {})[fn] = sols


# ---------------------------------------------------------------- playing in the page
FOLD_JS = """(sel) => { const els = [...document.querySelectorAll(sel)].filter(e => e.offsetParent !== null && getComputedStyle(e).visibility !== 'hidden');
  if (!els.length) return null; return Math.max(...els.map(e => e.getBoundingClientRect().bottom + window.scrollY)); }"""
ASK_SEL = '#ansBlock .opt, #doneBtn, #ans1, #ans2, #ans3, #checkBtn, #noneBtn, #kpHolder .maffs-keypad-panel'
NEXT_SEL = '#feedback .maffs-next, #feedback #nextBtn'


def fold_checks(page, size, out, tag, aa):
    fold = size[1] - FOOTER
    page.evaluate('window.scrollTo(0, 0)')
    a = page.evaluate(FOLD_JS, ASK_SEL)
    if a is None:
        out.append('%s: no answer controls on screen' % tag)
    elif a > fold + 0.5 and not (aa and size == (320, 568)):
        out.append('%s: the answer controls end at %d, below the fold at %d' % (tag, a, fold))
    if page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'):
        out.append('%s: the page scrolls sideways' % tag)


def next_check(page, size, out, tag, aa):
    fold = size[1] - FOOTER
    page.evaluate('window.scrollTo(0, 0)')
    nx = page.evaluate(FOLD_JS, NEXT_SEL)
    if nx is None:
        out.append('%s: no Next after the question' % tag)
    elif nx > fold + 0.5 and not (aa and size == (320, 568)):
        out.append('%s: Next ends at %d, below the fold at %d' % (tag, nx, fold))
    if page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 1'):
        out.append('%s: the page scrolls sideways after answering' % tag)


def play_stage(page, st, size, out, nq, aa=False):
    tag0 = '%s%dx%d stage %d' % ('Aa ' if aa else '', size[0], size[1], st)
    page.evaluate("() => { window.__ev = []; window.__sub = []; }")
    page.evaluate('n => CA.ui.start(n)', st)
    badge = page.evaluate("[document.getElementById('calcBadge').getAttribute('data-calc'), document.getElementById('calcBadge').textContent]")
    if badge[0] != CALC[st]:
        out.append('%s: the header badge says %s, the stage is %s' % (tag0, badge, CALC[st]))
    if not page.evaluate("document.getElementById('calc').classList.contains('scientific') && [...document.querySelectorAll('#calc button')].some(b => b.textContent === 'sin⁻¹')"):
        out.append('%s: the scientific calculator is not mounted' % tag0)
    if page.evaluate("!!document.querySelector('#game .band, #game .drift')") or page.evaluate("(() => { const b = document.getElementById('bandMenu'); return !!(b && b.offsetParent); })()"):
        out.append('%s: the character band shows during a question' % tag0)
    right = 0
    for i in range(nq):
        if page.evaluate('CA.ui.state()') != 'asking':
            out.append('%s: question %d is not asking (%s)' % (tag0, i + 1, page.evaluate('CA.ui.state()')))
            return
        tag = '%s q%d (%s)' % (tag0, i + 1, page.evaluate('CA.ui.question().id'))
        fold_checks(page, size, out, tag, aa)
        if st >= 3 and size[0] <= 600 and not page.evaluate("(() => { const k = document.querySelector('#kpHolder .maffs-keypad'); return !!(k && !k.hidden && k.offsetParent); })()"):
            out.append('%s: no keypad on a touch screen' % tag)
        if st <= 2:
            q = page.evaluate('CA.ui.question()')
            if st == 1:
                for s in q['sols']:
                    page.evaluate('d => CA.ui.tap(d)', s)
            else:
                for x in q['quads']:
                    page.evaluate('x => CA.ui.quad(x)', x)
            page.evaluate("document.getElementById('doneBtn').click()")
            if page.evaluate('CA.ui.step()') != 1:
                out.append('%s: the first step, answered right, did not move on' % tag)
            fold_checks(page, size, out, tag + ' step 2', aa)
        ok = i % 3 != 1
        page.evaluate('r => CA.ui.answer(r)', ok)
        right += 1 if ok else 0
        next_check(page, size, out, tag, aa)
        page.evaluate("() => { const b = document.querySelector('#feedback .maffs-next, #feedback #nextBtn'); if (b) b.click(); }")
    if nq < 10:
        return
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    qa = [p for n_, p in ev if n_ == 'question_answered']
    gc = [p for n_, p in ev if n_ == 'game_completed']
    if len(qa) != 10 or sum(1 for p in qa if p['correct']) != right:
        out.append('%s: %d question_answered, %d correct; %d were right first time' % (tag0, len(qa), sum(1 for p in qa if p['correct']), right))
    if len(gc) != 1 or gc[0]['score'] != right or gc[0]['mode'] != 'stage-%d' % st:
        out.append('%s: game_completed says %s; the score is %d' % (tag0, gc, right))
    if len(sub) != 1 or sub[0][1] != 'stage-%d' % st or sub[0][2] != right:
        out.append('%s: the leaderboard got %s; expected one submission of %d on stage-%d' % (tag0, sub, right, st))
    if page.evaluate('CA.ui.state()') != 'over':
        out.append('%s: the stage did not end' % tag0)
    if not page.evaluate("(() => { const b = document.getElementById('bandResults'); return !!(b && b.offsetParent && b.querySelectorAll('svg').length === 3); })()"):
        out.append('%s: no character band on the results screen' % tag0)
    nb = page.evaluate(FOLD_JS, '#nextStageBtn, #againBtn')
    if nb is not None and nb > size[1] - FOOTER:
        out.append('%s: the results buttons end at %d, below the fold' % (tag0, nb))
    page.evaluate("document.getElementById('menuBtn').click()")


def check_start(page, size, out, reduced):
    tag = 'start %dx%d%s' % (size[0], size[1], ' reduced motion' if reduced else '')
    band = page.evaluate("""(() => { const b = document.getElementById('bandMenu'); if (!b || !b.offsetParent) return null;
        const svgs = b.querySelectorAll('svg'); const names = [...svgs].map(s => s.textContent.trim());
        const d = b.querySelector('.drift'); const cs = d ? getComputedStyle(d) : null;
        return {n: svgs.length, names: names, anim: cs ? cs.animationName : null, asym: b.querySelectorAll('svg:nth-child(2) .bas').length}; })()""")
    if not band or band['n'] != 3 or band['names'] != ['sin x', 'tan x', 'cos x'] or not band['asym']:
        out.append('%s: the character band is %s (sin, tan with dashed asymptotes, cos)' % (tag, band))
    elif reduced and band['anim'] not in ('none', None):
        out.append('%s: the band still moves under reduced motion (%s)' % (tag, band['anim']))
    elif not reduced and band['anim'] != 'drift':
        out.append('%s: the band does not drift (%s)' % (tag, band['anim']))
    tl = page.evaluate("document.getElementById('tagline').textContent")
    if tl != "Your calculator says one. The graph says infinity. Make up your mind: it's two.":
        out.append('%s: the tagline is %r' % (tag, tl))
    if page.evaluate("document.querySelector('#menu h1').textContent") != 'CAST Away':
        out.append('%s: the title' % tag)
    wb = page.evaluate(FOLD_JS, '#watchBtns .btn')
    if wb is None or wb > size[1] - FOOTER:
        out.append('%s: "Watch one first" ends at %s, below the fold' % (tag, wb))


def check_walk_play(page, size, out):
    for fn in ('sin', 'cos', 'tan'):
        page.evaluate("() => { window.__ev = []; }")
        page.evaluate("document.querySelector('[data-watch=\"%s\"]').click()" % fn)
        for i in range(6):
            if page.evaluate('CA.ui.walkStep()') != i:
                out.append('walkthrough %s: on step %d, expected %d' % (fn, page.evaluate('CA.ui.walkStep()') + 1, i + 1))
            nx = page.evaluate(FOLD_JS, '#wtNext')
            if nx is None or nx > size[1] - FOOTER:
                out.append('walkthrough %s step %d at %dx%d: Next ends at %s, below the fold' % (fn, i + 1, size[0], size[1], nx))
            page.evaluate("document.getElementById('wtNext').click()")
        if page.evaluate("document.getElementById('menu').classList.contains('active')") is not True:
            out.append('walkthrough %s: the last Next does not return to the stages' % fn)
        if page.evaluate('window.__ev.length'):
            out.append('walkthrough %s: sends %s (it is unscored)' % (fn, page.evaluate('window.__ev')))


def size_unit(kind, size):
    return '%s %dx%d' % (kind, size[0], size[1])


def check(html, out, units, shard=None):
    from playwright.sync_api import sync_playwright
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    proc, base = bc.start_stub_server()
    info = {}
    try:
        with sync_playwright() as pw:
            for uid in units:
                with unit(uid):
                    kind, _, rest = uid.partition(' ')
                    if kind == 'engine':
                        br, page, errs = open_page(pw, base, html, (1280, 800))
                        try:
                            info.update(check_engine(page, out))
                        except Exception as e:  # noqa: BLE001
                            out.append('the engine checks threw: %s' % str(e).splitlines()[0][:200])
                    elif kind == 'walk':
                        br, page, errs = open_page(pw, base, html, (375, 667))
                        try:
                            check_walk(page, out, info)
                            check_start(page, (375, 667), out, False)
                            check_walk_play(page, (375, 667), out)
                        except Exception as e:  # noqa: BLE001
                            out.append('the walkthrough checks threw: %s' % str(e).splitlines()[0][:200])
                        br.close()
                        br, page, errs2 = open_page(pw, base, html, (375, 667), reduced=True)
                        check_start(page, (375, 667), out, True)
                        errs += errs2
                    else:
                        w, h = (int(x) for x in rest.split('x'))
                        aa = kind == 'aa'
                        br, page, errs = open_page(pw, base, html, (w, h), aa=aa)
                        try:
                            for st in (1, 2, 3, 4):
                                play_stage(page, st, (w, h), out, 10 if kind == 'full' else 3, aa)
                        except Exception as e:  # noqa: BLE001
                            out.append('play at %s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, [(old, new)], the unit it needs, the pattern its finding must match).
PLANTS = [
    ("cosine given sine's rule for a positive value", [("cos: { pos: ['a', '360-a'], neg: ['180-a', '180+a'] },", "cos: { pos: ['a', '180-a'], neg: ['180-a', '180+a'] },")], 'engine', r'keys .* but the solutions'),
    ('360 kept in an open interval', [("if (closed ? x > 360 + 1e-9 : x > 360 - 1e-9) return;", "if (x > 360 + 1e-9) return;")], 'engine', r'keys .* but the solutions'),
    ('keys rounded down, not half up', [("function r1(x) { var v = Math.round(x * 10) / 10;", "function r1(x) { var v = Math.floor(x * 10) / 10;")], 'engine', r'(keys|alpha) .*'),
    ('a distractor equal to the solutions', [("if (!m.set.length || id === kid || seen[id]) return false;", "if (!m.set.length || seen[id]) return false;")], 'engine', r'(equals the solutions|distinct options|among the options)'),
    ('a format answer marked right', [("else if (fmtHit) return { kind: 'format', msg: MaffsAnswer.message('format', raw, { dp: 1 }) };", "else if (fmtHit) matched.push(-1);")], 'engine', r'should say format'),
    ("the calculator's negative angle not named", [("var order = ['neg', 'range', 'fn', 'sign', 'period'];", "var order = ['range', 'fn', 'sign', 'period'];")], 'engine', r'should say neg'),
    ('a Stage 1 snap point off the curve', [("function snaps(q) { var s = q.sols.slice();", "function snaps(q) { var s = q.sols.map(function (x) { return x + 5; });")], 'engine', r'snap point'),
    ('a walkthrough number wrong (113.5)', [("'In S: \\\\(180^\\\\circ - 66.4^\\\\circ = 113.6^\\\\circ\\\\).'", "'In S: \\\\(180^\\\\circ - 66.4^\\\\circ = 113.5^\\\\circ\\\\).'")], 'walk', r'walkthrough cos step 3'),
    ('a walkthrough word changed', [("Not one. Not infinity. Two.", "Not one. Not infinite. Two.")], 'walk', r'walkthrough sin step 6'),
    ('the band moving under reduced motion', [("@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}", "")], 'walk', r'reduced motion'),
    ('a wrong answer scoring', [("marked++; if (first) { rightCount++; score++; }", "marked++; score++; if (first) { rightCount++; }")], 'full 390x844', r'(game_completed says|the leaderboard got)'),
    ('Show me at the first wrong try, before a second try', [("if (tries >= 2) $('showBtn').hidden = false;", "$('showBtn').hidden = false;")], 'engine', r'Show me'),
]


def check_show_rule(page, out):
    """'Show me' appears after two wrong tries, not one (contract item 5), on a typed question."""
    page.evaluate("CA.ui.preview(3, CA.pool(3)[0].id)")
    page.evaluate("() => { document.getElementById('ans1').value = '400'; document.getElementById('checkBtn').click(); }")
    if page.evaluate("!document.getElementById('showBtn').hidden"):
        out.append('Show me is offered after one wrong try')
    page.evaluate("() => { document.getElementById('ans1').value = '401'; document.getElementById('checkBtn').click(); }")
    if page.evaluate("document.getElementById('showBtn').hidden"):
        out.append('Show me is not offered after two wrong tries')
    page.evaluate("document.getElementById('showBtn').click()")
    if not page.evaluate("!!document.querySelector('#feedback .worked li') && !!document.querySelector('#feedback .maffs-next')"):
        out.append('Show me does not show the working and wait on Next')


_orig_engine = check_engine


def check_engine(page, out):  # noqa: F811  (the engine unit also checks the two-tries rule in the page)
    info = _orig_engine(page, out)
    check_show_rule(page, out)
    return info


def selftest(html, plants=None, shard=None):
    ok = True
    for what, edits, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = html
                for old, new in edits:
                    src = pc.apply_plant(src, old, new, name=what)
            except pc.StalePlant as e:
                print('  self-test %-70s *** %s ***' % (what, e))
                ok = False
                continue
            got = []
            err = None
            try:
                check(src, got, [unit_id])
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-70s %s' % (what, ('caught: ' + hit[0][:80]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:80] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    global KATEX_DIR
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--katex-dir', default=None, help="serve KaTeX 0.16.9's dist/ from here (a sandbox without the CDN)")
    args = ap.parse_args()
    KATEX_DIR = args.katex_dir
    shard = bc.Shard(__file__, args)
    play = ['engine', 'walk', size_unit('full', FULL)] + [size_unit('first', s) for s in FIRST] + [size_unit('aa', s) for s in AA]
    mine = shard.pick(play + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    units = [u for u in play if u in mine]
    info = check(html, out, units, shard) if units else {}
    for n in (1, 2, 3, 4):
        if n in info:
            print('%s: stage %d: %d distinct questions, %d distinct equations (by value), every key recomputed' % (SLUG, n, info[n]['questions'], info[n]['equations']))
    if 'fired' in info:
        print('%s: feedback rules fired by planted answers: %s' % (SLUG, dict(sorted(info['fired'].items()))))
    if 'walk' in info:
        print('%s: walkthroughs word for word, numbers recomputed: %s' % (SLUG, info['walk']))
    played = [u for u in units if u not in ('engine', 'walk')]
    if played:
        print('%s: played: %s' % (SLUG, ', '.join(played)))
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
