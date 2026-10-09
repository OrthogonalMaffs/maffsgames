#!/usr/bin/env python3
# ci-line: Binomial Blaster (every key and option evaluated with SymPy, every item marked in Chromium) |
"""Binomial Blaster: every key and option evaluated with SymPy; every item marked in Chromium.

The game (100 multiple-choice items: alevel 50, alevel2 50) covers nCr, binomial coefficients and expansions,
estimates from the first few terms, validity ranges and series for any n. Its bank was keyed by hand; the
tranche 5 audit of 6 Oct 2026 found 6 of 50 A-Level and 5 of 50 Year 2 items marking a correct answer wrong:
estimates keyed with the wrong number of terms (or the calculator value) while the three-term value was a
distractor or missing, the coefficient of x keyed for x², a Pascal-rule item whose distractor equalled its
key, an approximation keyed with the true value, a coefficient of 5 for -3, n = -2 and a = -3 for a pair of
equations whose solution is n = 9, a = 2/3, a false reason keyed, and estimates with no method stated.

Every option is read into SymPy (read() below; an option it cannot read FAILS: extend read(), never skip).
TARGETS says what each item asks for, computed from the item itself: a value, a polynomial or the first terms
of a series, an expression identical for every n, an interval |x| < k, an estimate from the first N terms
(the exact sum of those terms), or a reviewed verdict. Then:
  the key equals the target; no wrong option equals it (SR-16), and for an estimate no wrong option is the
  key rounded to fewer places (a true value at another precision: SR-1, SR-17); the options are distinct in
  value; an estimate's ask states its method ("first N terms" or "these three terms"); and, in Chromium
  (390x844), every item is shown through showQ() and every option clicked through handle(): the key marked
  right, the others wrong. Options are assembled by MaffsOptions.build() (four distinct, the key once).
A self-test plants three of the audit's own faults back into a copy of the page (t5-003: (1.01)^5 keyed
1.05101; t5-007: (2x+3)^3 keyed 54; t5-012: the coefficient keyed 5); each must FAIL naming its item.

    python scripts/verify-binomial-blaster.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, rationalize,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'binomial-blaster'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'alevel': 50, 'alevel2': 50}
x, n, r, a, b = sp.symbols('x n r a b')
LOCAL = {'x': x, 'n': n, 'r': r, 'a': a, 'b': b, 'binomial': sp.binomial, 'factorial': sp.factorial, 'sqrt': sp.sqrt}
TRANS = standard_transformations + (implicit_multiplication_application, rationalize)


def group(s, i):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '{') - (s[j] == '}')
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in %r' % s)


def read(s):
    """An option's TeX as SymPy; ValueError when it cannot be read."""
    s = s.replace('\u2212', '-').replace('\\left', '').replace('\\right', '')
    s = re.sub(r'\s*[+-]\s*\\cdots\s*$', '', s)
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            p, j = group(s, i + m.end() - 1)
            q, k = group(s, j)
            out, i = out + '((%s)/(%s))' % (read(p), read(q)), k
            continue
        if s.startswith('\\binom{', i):
            p, j = group(s, i + 6)
            q, k = group(s, j)
            out, i = out + 'binomial(%s,%s)' % (read(p), read(q)), k
            continue
        if s.startswith('\\sqrt{', i):
            p, j = group(s, i + 5)
            out, i = out + 'sqrt(%s)' % read(p), j
            continue
        if s.startswith('\\cdot', i):
            out, i = out + '*', i + 5
            continue
        if s[i] == '{':
            p, j = group(s, i)
            out, i = out + '(%s)' % read(p), j
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX command in %r' % s)
        if s[i] == '!':
            m2 = re.search(r'([A-Za-z0-9]+|\([^()]*\))$', out)
            out = out[:m2.start()] + 'factorial(%s)' % m2.group(1)
            i += 1
            continue
        out, i = out + ('**' if s[i] == '^' else s[i]), i + 1
    try:
        return parse_expr(out, local_dict=LOCAL, transformations=TRANS)
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (s, out, e))


def bound(s):
    """'|x| < k' as k; anything else None."""
    m = re.fullmatch(r'\|x\| < (.+)', s.strip())
    return read(m.group(1)) if m else None


def same(p, q):
    if p.free_symbols - {n, r, x, a, b} or q.free_symbols - {n, r, x, a, b}:
        return False
    d = sp.simplify(p - q)
    if d == 0:
        return True
    for nv in range(3, 9):          # identities in n, r: integer points where factorials are defined
        for rv in range(0, 3):
            for xv in (sp.Rational(1, 3), sp.Rational(2, 7)):
                try:
                    if sp.N((p - q).subs({n: nv, r: rv, x: xv, a: 2, b: 3}), 30) != 0:
                        return False
                except TypeError:
                    return False
    return True


def coeff(expr, k):
    return sp.expand(expr).coeff(x, k)


def series(expr, terms):
    return sp.series(expr, x, 0, terms).removeO()


def est(f, h, terms):
    """The first `terms` terms of the expansion of f(1 + x) at x = h, exactly."""
    return sp.expand(series(f, terms)).subs(x, h)


def V(v):
    return ('val', sp.nsimplify(v))


def R(s):
    return sp.Rational(s)


TARGETS = {
    'alevel': [V(10), V(20), V(1), V(7), V(28), V(120), ('expr', sp.Integer(1)), ('expr', n), V(15), V(20),
               ('poly', (1 + x) ** 3), V(6), V(10), V(-4), ('poly', (1 + 2 * x) ** 3), V(24), V(27), ('poly', (2 + x) ** 3),
               V(24), V(24), V(120), V(28), V(495), V(15), V(-35), V(90), V(270), V(40), V(54), V(-160), V(R('15/4')),
               V(40), V(81), V(6), V(9),
               ('est', est((1 + x) ** 5, R('0.01'), 3)), ('est', est((1 - x) ** 4, R('0.02'), 3)),
               ('est', est(8 * (1 + x / 2) ** 3, R('0.01'), 3)), ('est', est((1 - x) ** 10, R('0.01'), 3)),
               ('est', est((1 + x) ** 3, R('0.05'), 3)), V(sp.binomial(6, 3)), ('expr', n + 1),
               ('expr', sp.binomial(n, r) * x ** r), ('verdict', 'Symmetry', 'nCr = nC(n-r) is the symmetry of the rows'),
               V(16), ('expr', 2 ** n), V(64), V(10), ('poly', (x - 1) ** 4), V(36)],
    'alevel2': [('series', (1 + x) ** R('1/2'), 3), ('series', (1 + x) ** -1, 3), ('series', (1 + x) ** -2, 3),
                ('series', (1 - x) ** -1, 3), ('series', (1 - x) ** -2, 3), V(6), V(R('-1/9')), ('series', (1 + x) ** R('-1/2'), 3),
                ('series', (1 - 2 * x) ** -1, 3), V(R('3/2')), V(R('-9/8')), ('series', (1 - x) ** R('1/2'), 3),
                ('series', (1 + 4 * x) ** -1, 3), V(27), ('series', (4 + x) ** R('1/2'), 3),
                ('bound', 1), ('bound', R('1/2')), ('bound', R('1/3')), ('bound', 4), ('bound', 2), ('bound', 4),
                ('bound', R('1/5')), ('bound', 9), ('series', (1 - x) ** -1, 4), ('expr', -x),
                ('est', est((1 + x) ** R('1/2'), R('0.02'), 3)), ('est', est((1 + x) ** -1, R('0.03'), 3)),
                ('est', est((1 - x) ** -1, R('0.02'), 3)), ('est', 2 * est((1 + x) ** R('1/2'), R('0.02'), 3)),
                ('est', est((1 - x) ** -2, R('0.03'), 3)), V(R('1/3')), V(R('3/8')),
                ('est', 1 + R('0.1') / 2 - R('0.1') ** 2 / 8), ('est', 1 - R('0.1') + R('0.1') ** 2),
                ('est', est((1 + x) ** -2, R('0.05'), 2)), V(R('1/2')), V((3 / (1 + x)).subs(x, R('1/2'))),
                ('verdict', '\\dfrac{n(n-1)\\cdots(n-r+1)}{r!}', 'n! is not defined for non-integer n; the falling product is'),
                ('verdict', 'It is a GP with ratio -x', 'a GP converges only for |ratio| < 1'),
                V(coeff(series(3 / ((1 - x) * (1 + 2 * x)), 3), 1)), V(6), ('solve', n), ('solve', a),
                V(coeff(series(sp.sqrt((1 + x) / (1 - x)), 3), 1)), V(coeff(series(sp.sqrt((1 + x) / (1 - x)), 3), 2)),
                ('verdict', 'n! \\text{ is undefined for negative } n', 'the factorial is defined only for whole numbers 0, 1, 2 ...'),
                ('verdict', 'An infinite series', 'for n not 0, 1, 2 ... the coefficients never reach zero'),
                ('verdict', 'Diverges', 'at x = 1 the partial sums are 1, 0, 1, 0 ...; at x = -1 the terms grow'),
                ('expr', x), V(1)],
}
COEFF_ASK = re.compile(r'Coefficient of x([²³⁴]?)|Constant term')
# The words an item must carry for its target to be the one above.
PINNED = {('alevel', 40): 'is row 0', ('alevel2', 41): '27x^2', ('alevel2', 42): '27x^2', ('alevel2', 40): 'product a',
          ('alevel2', 46): '\\{0, 1, 2, \\ldots\\}', ('alevel2', 36): '\\dfrac{3}{(1+x)(1-2x)}'}
AUDIT = {('alevel', 9): 't5-002', ('alevel', 35): 't5-003', ('alevel', 36): 't5-004', ('alevel', 38): 't5-005',
         ('alevel', 39): 't5-006', ('alevel', 49): 't5-007', ('alevel', 37): 't5-008', ('alevel', 40): 't5-009',
         ('alevel2', 32): 't5-011', ('alevel2', 39): 't5-012', ('alevel2', 41): 't5-013', ('alevel2', 42): 't5-014',
         ('alevel2', 45): 't5-015', ('alevel2', 28): 't5-016', ('alevel2', 33): 't5-019', ('alevel2', 46): 't5-020',
         ('alevel2', 37): 't5-021', ('alevel2', 40): 't5-022', ('alevel2', 30): 't5-022'}


def roundings(v):
    """v rounded half up at 1 .. (its own places - 1) decimal places."""
    places = -Decimal(str(v)).as_tuple().exponent
    return {Decimal(str(v)).quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP) for k in range(0, max(places, 0))}


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs TARGETS reviewed)' % (counts, COUNTS))
        return
    for lv in COUNTS:
        for i, q in enumerate(bank[lv]):
            w = '%s[%d] (%s | %s)%s' % (lv, i, q['q'], q['ask'],
                                       ' (binomial-blaster-%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            t = TARGETS[lv][i]
            if (lv, i) in PINNED and PINNED[(lv, i)] not in q['q'] + ' ' + q['ask']:
                fails.append('%s: the item must say "%s" for its key to hold' % (w, PINNED[(lv, i)]))
            opts = [q['correct']] + q['d']
            if len(set(opts)) != 4:
                fails.append('%s: the options %s are not four distinct strings' % (w, opts))
            if t[0] == 'verdict':
                if q['correct'] != t[1]:
                    fails.append('%s: keyed %r, reviewed %r (%s)' % (w, q['correct'], t[1], t[2]))
                continue
            if t[0] == 'bound':
                ks = [bound(o) for o in opts]
                if ks[0] is None or ks[0] != t[1]:
                    fails.append('%s: keyed %s, valid for |x| < %s' % (w, q['correct'], t[1]))
                for o, k in zip(opts[1:], ks[1:]):
                    if k is not None and k == t[1]:
                        fails.append('%s: the wrong option %s is also right' % (w, o))
                continue
            try:
                vals = [read(o) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend read())' % (w, e))
                continue
            if t[0] == 'val':
                target = t[1]
            elif t[0] == 'poly':
                target = sp.expand(t[1])
            elif t[0] == 'series':
                target = sp.expand(series(t[1], t[2]))
            elif t[0] == 'expr':
                target = t[1]
            elif t[0] == 'solve':
                # (1 + ax)^n = 1 + c1 x + c2 x^2: na = c1 and n(n-1)a^2/2 = c2, read from the item itself
                m = re.search(r'1 \+ (\d+)x \+ (\d+)x\^2', q['q'])
                c1, c2 = int(m.group(1)), int(m.group(2))
                sol = sp.solve([n * a - c1, n * (n - 1) * a ** 2 / 2 - c2], [n, a], dict=True)
                if len(sol) != 1:
                    fails.append('%s: 1 + %dx + %dx^2 gives %d solutions for n and a' % (w, c1, c2, len(sol)))
                    continue
                target = sol[0][t[1]]
            elif t[0] == 'est':
                target = t[1]
                if not re.search(r'first \d terms|these three terms', q['ask']):
                    fails.append('%s: an estimate must state its method (SR-17)' % w)
            if not same(sp.expand(vals[0]), sp.expand(target)):
                fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], target))
            for o, v in zip(opts[1:], vals[1:]):
                if same(sp.expand(v), sp.expand(target)):
                    fails.append('%s: the wrong option %s is also right (SR-16)' % (w, o))
                if t[0] == 'est' and Decimal(o) in roundings(q['correct']):
                    fails.append('%s: the wrong option %s is the key %s rounded: a true value at another precision'
                                 % (w, o, q['correct']))
            for p in range(4):
                for k in range(p + 1, 4):
                    if same(sp.expand(vals[p]), sp.expand(vals[k])):
                        fails.append('%s: options %s and %s are equal in value' % (w, opts[p], opts[k]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  for (const lv of ['alevel', 'alevel2']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      questions = [q]; qIdx = 0; totalQ = 1; level = lv; score = 0; correctCount = 0; streak = 0;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([lv, i, pick, shown.length + ' options on screen']);
      const btn = shown.find(x => x.dataset.val === pick);
      if (!btn) { out.push([lv, i, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""
# Answer once (canon 7.6.0, MaffsLock; binomial-blaster-t5-017): with the real 300 ms window, the key clicked and then Enter three times
# on it counts once, and the results screen submits once.
LOCK_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const q = QUESTIONS.alevel2[36];
  startGame();
  questions = [q, q]; qIdx = 0; totalQ = 2; score = 0; correctCount = 0;
  showQ();
  await wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 50);
  const key = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === q.correct);
  key.click(); key.focus();
  for (let k = 0; k < 3; k++) { key.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true })); key.click(); }
  const res = { correct: correctCount };
  if (window.MaffsLock) MaffsLock.clearTimers();
  end(); end();
  res.submits = submits;
  return res;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            lk = page.evaluate(LOCK_JS)
            if lk['correct'] != 1:
                fails.append('the key clicked, then Enter three times on it, counted %d times (binomial-blaster-t5-017)' % lk['correct'])
            if lk['submits'] != 1:
                fails.append('the results screen submitted %d scores (MaffsLock.finishOnce)' % lk['submits'])
            page.reload(wait_until='load')
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d] in Chromium: option %s %s' % (lv, i, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('alevel[35]', 't5-003: (1.01)^5 keyed 1.05101', "correct:'1.051',d:['1.05101','1.0501','0.951']",
     "correct:'1.05101',d:['1.051','1.0501','0.951']"),
    ('alevel[49]', 't5-007: (2x+3)^3 keyed 54', "correct:'36',d:['54','108','18']", "correct:'54',d:['36','108','18']"),
    ('alevel2[39]', 't5-012: the coefficient keyed 5', "correct:'-3',d:['3','9','-6']", "correct:'5',d:['3','9','-6']"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items, every option evaluated (SymPy) and clicked in Chromium' % (SLUG, sum(len(bank[k]) for k in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-42s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-42s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
