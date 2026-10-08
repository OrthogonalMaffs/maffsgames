#!/usr/bin/env python3
# ci-line: B3 | Proportion Blaster (every key recomputed from its stem, options distinct in value, every option marked in Chromium) |
"""Proportion Blaster: every key recomputed from the question's own numbers; every option clicked in Chromium.

The game (100 multiple-choice items: gcse 50, alevel 50) covers direct and inverse proportion, sharing in a
ratio, combining ratios, reverse percentages and compound growth. Its bank was keyed by hand with no verifier;
the resit audit of 4 Oct 2026 found alevel[47] (:242, a : b : c from a : b = 1 : 4 and b : c = 2 : 3) keyed
450/11, which is c's unscaled 3 over the scaled 11 parts: c is 900/11 and no option was correct
(proportion-blaster-r-001). It also found four items whose wrong options were equal in value to each other
(audit F2-F5, B11 ledger): gcse[16] 10 and sqrt(100), gcse[44] 3:4:5 and 6:8:10, gcse[45] 5:4:3 and 10:8:6,
alevel[30] 2:5:7 and 6:15:21; and alevel[47]'s 50 and 150/3.

TARGETS gives each item's answer as a computation on the numbers in its own text; PINNED holds the words each
computation reads, so an edited stem fails until its target is reviewed. Every option is read exactly (numbers,
money, percentages, TeX fractions and roots, the symbols a and b, ratios reduced by their gcd). Then:
  the key equals the target (or one of the targets, for x^2 = c); no wrong option equals any target (SR-16);
  the four options are distinct strings and distinct in value (SR-4); and, in Chromium (390x844), every item
  is shown through showQ() and every option clicked through handle(): the key marked right, the others wrong.
A self-test plants the audit's fault back into a copy of the page (r-001: c keyed 450/11) and one value-equal
pair (F2: sqrt(100) beside 10); each must FAIL naming its item.

    python scripts/verify-proportion-blaster.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F
from math import gcd

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'proportion-blaster'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'gcse': 50, 'alevel': 50}
A, B = sp.symbols('a b', positive=True)


def group(s, i):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '{') - (s[j] == '}')
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in %r' % s)


def tex(s):
    """A TeX option as a SymPy expression in a and b; ValueError when it cannot be read."""
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            p, j = group(s, i + m.end() - 1)
            q, k = group(s, j)
            out, i = out + '((%s)/(%s))' % (tex(p), tex(q)), k
            continue
        if s.startswith('\\sqrt{', i):
            p, j = group(s, i + 5)
            out, i = out + 'sqrt(%s)' % tex(p), j
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX in %r' % s)
        if s[i] in 'ab' and out and (out[-1].isdigit() or out[-1] == ')'):
            out += '*'
        out, i = out + s[i], i + 1
    try:
        return sp.nsimplify(sp.sympify(out, locals={'a': A, 'b': B, 'sqrt': sp.sqrt}), rational=True)
    except Exception as e:
        raise ValueError('cannot read %r: %s' % (s, e))


def read(s):
    """('ratio', reduced tuple) | ('num', SymPy value). Money and percentages read as their number."""
    t = s.replace('\u2212', '-').strip()
    if ':' in t:
        parts = [int(p) for p in t.split(':')]
        g = 0
        for p in parts:
            g = gcd(g, p)
        return ('ratio', tuple(p // g for p in parts))
    t = t.replace('\u00a3', '').replace(',', '').replace('\\%', '').replace('%', '')
    if t.startswith('+'):
        t = t[1:]
    if re.fullmatch(r'-?\d+(\.\d+)?', t):
        return ('num', sp.Rational(t))
    return ('num', tex(t))


def R(*p):
    return ('ratio', tuple(p))


def N(v):
    return ('num', sp.nsimplify(v, rational=True))


def money2(v):
    """v to 2 d.p., half up, exactly."""
    return sp.Rational(int(v * 100 + sp.Rational(1, 2)), 100)


# Each item's answer from its own numbers: (words its stem must carry, [targets]).
G = [
    ('x = 3, y = 12.', [N(F(12, 3))]),
    ('x = 5, y = 20.', [N(F(20, 5) * 8)]),
    ('x = 4, y = 10.', [N(25 / F(10, 4))]),
    ('x = 2, y = 14.', [N(F(14, 2))]),
    ('x = 6, y = 18.', [N(F(18, 6) * 10)]),
    ('3 kg costs \u00a312.', [N(F(12, 3) * 7)]),
    ('x = 8, y = 24.', [N(F(24, 8) * 5)]),
    ('In 4 seconds, d = 20 m.', [N(F(20, 4) * 7)]),
    ('x = 10, y = 4.', [N(F(4, 10))]),
    ('x = 10, y = 4.', [N(6 / F(4, 10))]),
    ('Q = 5, P = 35.', [N(F(35, 5) * 12)]),
    ('x = 3, y = 15.', [N(F(15, 3) * F(1, 2))]),
    ('x = 2, y = 12.', [N(F(12, 4))]),
    ('x = 3, y = 45.', [N(F(45, 9))]),
    ('x = 2, y = 20.', [N(F(20, 4) * 25)]),
    ('x = 4, y = 48.', [N(F(48, 16) * 36)]),
    ('x = 3, y = 36.', [N(5), N(-5)]),                     # x^2 = 100/4 = 25
    ('v = 3, E = 27.', [N(F(27, 9) * 25)]),
    ('x = 5, y = 50.', [N(F(50, 25))]),
    ('x = 1, y = 7.', [N(7 * 16)]),
    ('r = 3, A = 18.', [N(F(18, 9) * 100)]),
    ('x = 2, y = 8.', [N(5), N(-5)]),                      # x^2 = 50/2 = 25
    ('x = 2, y = 10.', [N(2 * 10)]),
    ('x = 4, y = 5.', [N(F(4 * 5, 10))]),
    ('x = 3, y = 6.', [N(3 * 6)]),
    ('x = 3, y = 6.', [N(F(18, 9))]),
    ('x = 5, y = 8.', [N(F(40, 4))]),
    ('t = 2, s = 30.', [N(F(60, 6))]),
    ('x = 6, y = 4.', [N(F(24, 8))]),
    ('x = 10, y = 3.', [N(F(30, 6))]),
    ('V = 4, P = 25.', [N(F(100, 10))]),
    ('x = 2, y = 5.', [N(5 * 4)]),
    ('x = 2, y = 5.', [N(F(20, 16))]),
    ('x = 1, y = 12.', [N(F(12, 9))]),
    ('Share \u00a360 in the ratio 2 : 3.', [N(60 * F(3, 5))]),
    ('Share \u00a3150 in the ratio 3 : 2.', [N(150 * F(2, 5))]),
    ('Share 48 sweets in the ratio 5 : 3.', [N(48 * F(5, 8))]),
    ('3 : 5. There are 120 students.', [N(120 * F(5, 8))]),
    ('ratio 4 : 7. B gets \u00a335.', [N(35 * F(4, 7))]),
    ('x : y = 2 : 5. x + y = 42.', [N(42 * F(2, 7))]),
    ('Share \u00a3200 in the ratio 1 : 3 : 4.', [N(200 * F(4, 8))]),
    ('Share \u00a3200 in the ratio 1 : 3 : 4.', [N(200 * F(1, 8))]),
    ('1 : 2 : 3. You need 180 kg total.', [N(180 * F(2, 6))]),
    ('5 : 2. You have 350 g of flour.', [N(350 * F(2, 5))]),
    ('a : b = 3 : 4. The ratio b : c = 2 : 5.', [R(3, 4, 10)]),   # b = 4 = 2 x 2, so c = 5 x 2
    ('x : y = 5 : 8. y : z = 4 : 3.', [R(5, 8, 6)]),               # y = 8 = 4 x 2, so z = 3 x 2
    ('20% increase, the new price is \u00a360.', [N(60 / F(120, 100))]),
    ('15% decrease, the value is \u00a3170.', [N(170 / F(85, 100))]),
    ('10% each year. It cost \u00a320,000.', [N(20000 * F(9, 10) ** 2)]),
    ('5% per year from 8000.', [N(8000 * F(105, 100) ** 3)]),
]
L = [
    ('x = 2, y = 24.', [N(F(24, 8))]),
    ('x = 2, y = 24.', [N(F(24, 8) * 27)]),
    ('x = 9, y = 6.', [N(F(6, 3))]),
    ('x = 9, y = 6.', [N(F(6, 3) * 5)]),
    ('x = 4, y = 10.', [N((F(25) / F(10, 2)) ** 2)]),
    ('l = 4, T = 6.', [N(F(6, 2) * 4)]),
    ('x = 4, y = 16.', [N(F(16, 8))]),                    # 4^(3/2) = 8
    ('d = 2, F = 10.', [N(F(10 * 4, 25))]),
    ('x = 2, y = 5.', [N(5 * 8)]),
    ('x = 2, y = 5.', [N(F(40, 64))]),
    ('r = 3, V = 108.', [N(F(108, 27) * 125)]),
    ('x = a, y = b.', [N(9 * B)]),
    ('x = a, y = b.', [N(B / 2)]),
    ('Q = 16, P = 20.', [N((F(30) / F(20, 4)) ** 2)]),
    ('When x doubles, y multiplies by 8.', [N(3)]),
    ('x = 2, y = 18.', [N(F(18, 9))]),
    ('x = 2, y = 18.', [N(2 * 25)]),
    ('x = 3, y = 5.', [N(5 * 2)]),
    ('x = 3, y = 5.', [N(F(10, 5))]),
    ('A = 0.5, R = 4.', [N(F(2) / F(1, 4))]),
    ('x = 3, z = 2, y = 9.', [N(F(9 * 2, 9))]),
    ('k = 2.', [N(F(2 * 16, 8))]),
    ('F = 10 when m = 5, r = 2.', [N(F(10 * 4, 5))]),
    ('(2, 12) and (4, 48)', [N(2)]),                      # 48/12 = 4 = 2^n
    ('(1, 5) and (2, 40)', [N(3)]),                       # 40/5 = 8 = 2^n
    ('When x = 1, y = 5. When x = 3, y = 11.', [N(F(11 - 5, 3 - 1))]),
    ('When x = 1, y = 5. When x = 3, y = 11.', [N(5 - 3)]),
    ('When x = 0, y = 3. When x = 2, y = 11.', [N(F(11 - 3, 4))]),
    ('When x triples, y is multiplied by 9.', [N(2)]),
    ('When x is halved, y is multiplied by 4.', [N(-2)]),
    ('a : b = 2 : 5 and b : c = 3 : 7.', [R(6, 15, 35)]),        # b = 15: a = 2 x 3, c = 7 x 5
    ('x : y = 4 : 3 and x + y = 35.', [N(35 * F(4, 7))]),
    ('After a 25% increase, a value becomes 200.', [N(200 / F(125, 100))]),
    ('decreases by 20% then increases by 20%.', [N((F(8, 10) * F(12, 10) - 1) * 100)]),
    ('\u00a35000 is invested at 3% compound', [N(money2(sp.Rational(5000) * sp.Rational(103, 100) ** 4))]),
    ('If x increases by 50%', [N(50)]),
    ('y \u221d x\u00b2. If x increases by 50%', [N((F(3, 2) ** 2 - 1) * 100)]),
    ('y \u221d 1/x. If x doubles', [N(F(1, 2))]),
    ('y \u221d 1/x\u00b2. If x triples', [N(F(1, 9))]),
    ('y \u221d \u221ax. If x quadruples', [N(2)]),
    ('doubling x quadruples y.', [N(2)]),
    ('tripling x multiplies y by 27.', [N(3)]),
    ('\u00a38000 depreciates 15% per year.', [N(8000 * F(85, 100) ** 3)]),
    ('doubles every 20 minutes. Start: 500.', [N(500 * 2 ** 3)]),
    ('When x = a, y = b. Find y when x = a/2.', [N(B / 4)]),
    ('When x = a, y = b. Find y when x = a/3.', [N(3 * B)]),
    ('ratio 2 : 3. The difference between shares is \u00a340.', [N(40 * 5)]),
    ('a : b = 1 : 4. b : c = 2 : 3. a + b + c = 150.', [N(150 * F(6, 11))]),   # 1:4 and 4:6, so 1 : 4 : 6
    ('x is proportional to z\u00b3.', [N(2 ** 6)]),
    ('When Q = 2, P = 12. When Q = 4, P = 48.', [N(2)]),
]
TARGETS = {'gcse': G, 'alevel': L}
# The words in the ask each target reads (the stem's numbers are pinned above).
ASKS = {('gcse', 0): 'Find k', ('gcse', 1): 'x = 8', ('gcse', 2): 'y = 25', ('gcse', 5): '7 kg', ('gcse', 6): 'x = 5',
        ('gcse', 7): 't = 7', ('gcse', 9): 'y = 6', ('gcse', 10): 'Q = 12', ('gcse', 11): 'x = 0.5',
        ('gcse', 14): 'x = 5', ('gcse', 15): 'x = 6', ('gcse', 16): 'y = 100', ('gcse', 17): 'v = 5',
        ('gcse', 19): 'x = 4', ('gcse', 20): 'r = 10', ('gcse', 21): 'y = 50', ('gcse', 23): 'x = 10',
        ('gcse', 25): 'x = 9', ('gcse', 26): 'y = 4', ('gcse', 27): 't = 6', ('gcse', 28): 'x = 8',
        ('gcse', 29): 'y = 6', ('gcse', 30): 'V = 10', ('gcse', 32): 'x = 4', ('gcse', 33): 'x = 3',
        ('gcse', 34): 'larger', ('gcse', 35): 'smaller', ('gcse', 36): 'larger', ('gcse', 37): 'girls',
        ('gcse', 38): 'A get', ('gcse', 39): 'Find x', ('gcse', 40): 'largest', ('gcse', 41): 'smallest',
        ('gcse', 42): 'sand', ('gcse', 43): 'sugar', ('gcse', 48): '2 years', ('gcse', 49): '3 years',
        ('alevel', 1): 'x = 3', ('alevel', 3): 'x = 25', ('alevel', 4): 'y = 25', ('alevel', 5): 'l = 16',
        ('alevel', 7): 'd = 5', ('alevel', 9): 'x = 4', ('alevel', 10): 'r = 5', ('alevel', 11): 'x = 3a',
        ('alevel', 12): 'x = 2a', ('alevel', 13): 'P = 30', ('alevel', 16): 'x = 4', ('alevel', 18): 'x = 6',
        ('alevel', 19): 'A = 0.25', ('alevel', 21): 'x = 4, z = 8', ('alevel', 25): 'Find a',
        ('alevel', 26): 'Find b', ('alevel', 27): 'Find a', ('alevel', 31): 'Find x', ('alevel', 34): '4 years (2 d.p.)',
        ('alevel', 42): '3 years', ('alevel', 43): '1 hour', ('alevel', 47): 'Find c'}
AUDIT = {('alevel', 47): 'proportion-blaster-r-001', ('gcse', 16): 'audit F2, B11', ('gcse', 44): 'audit F3, B11',
         ('gcse', 45): 'audit F4, B11', ('alevel', 30): 'audit F5, B11'}


def eq(p, q):
    if p[0] != q[0]:
        return False
    if p[0] == 'ratio':
        return p[1] == q[1]
    return sp.simplify(p[1] - q[1]) == 0


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs TARGETS reviewed)' % (counts, COUNTS))
        return
    for lv in COUNTS:
        for i, q in enumerate(bank[lv]):
            w = '%s[%d] (%s | %s)%s' % (lv, i, q['ctx'], q['ask'],
                                       ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            words, targets = TARGETS[lv][i]
            if words not in q['ctx']:
                fails.append('%s: the stem must say "%s" for its target to hold' % (w, words))
            if (lv, i) in ASKS and ASKS[(lv, i)] not in q['ask']:
                fails.append('%s: the ask must say "%s" for its target to hold' % (w, ASKS[(lv, i)]))
            opts = [q['correct']] + q['d']
            if len(opts) != 4 or len(set(opts)) != 4:
                fails.append('%s: the options %s are not four distinct strings' % (w, opts))
            try:
                vals = [read(o) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend read())' % (w, e))
                continue
            if not any(eq(vals[0], t) for t in targets):
                fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], ' or '.join(str(t[1]) for t in targets)))
            for o, v in zip(opts[1:], vals[1:]):
                if any(eq(v, t) for t in targets):
                    fails.append('%s: the wrong option %s is also right (SR-16)' % (w, o))
            for p in range(len(opts)):
                for k in range(p + 1, len(opts)):
                    if eq(vals[p], vals[k]):
                        fails.append('%s: options %s and %s are equal in value (SR-4)' % (w, opts[p], opts[k]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  for (const lv of ['gcse', 'alevel']) QUESTIONS[lv].forEach((q, i) => {
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
KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once (F1 batch 8)
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
    ('alevel[47]', 'r-001: c keyed 450/11, no option correct',
     "correct:'\\\\dfrac{900}{11}',d:['\\\\dfrac{450}{11}','90','50']",
     "correct:'\\\\dfrac{450}{11}',d:['50','60','\\\\dfrac{150}{3}']"),
    ('gcse[16]', 'F2: sqrt(100) beside 10',
     "d:['10','\\\\dfrac{100}{36}','25']", "d:['10','\\\\dfrac{100}{36}','\\\\sqrt{100}']"),
    ('gcse[45]', 'F4: 10 : 8 : 6 beside 5 : 4 : 3',
     "d:['5 : 4 : 3','5 : 8 : 3','5 : 12 : 3']", "d:['5 : 4 : 3','5 : 8 : 3','10 : 8 : 6']"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items, every key recomputed, every option read and clicked in Chromium'
          % (SLUG, sum(len(bank[k]) for k in COUNTS) if bank else 0))
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
