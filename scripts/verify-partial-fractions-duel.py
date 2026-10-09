#!/usr/bin/env python3
# ci-line: Partial Fractions Duel (every key solved from its own stem with SymPy, every option checked and clicked) |
"""Partial Fractions Duel: every key solved from its own stem with SymPy; every option checked and clicked.

The game (50 multiple-choice items, one bank) asks for partial-fraction coefficients, decomposition forms,
proper/improper, and long-division quotients and remainders. Its bank was keyed by hand; the tranche 5 audit
of 6 Oct 2026 found four wrong keys (A = 1/2 for -1/2, A = 1 for 5/7, C = 11/6 for -11/6, remainder 2 for 3),
two "wrong" forms that are valid equivalent decompositions, Find B/C items whose stem never showed the form,
and a fraction not in lowest terms.

Every item is read from its TeX (read() below; one it cannot read FAILS: extend read(), never skip):
  "Find A/B/C ...": the stem must state the decomposition (fraction = form); SymPy solves the identity for
    the letters and the key must equal the asked letter; no wrong option may equal it (SR-16).
  "Find the remainder" (fraction = q + ?/den): solved the same way, ? as the unknown.
  "Form of decomposition": the key is the standard form (one term per linear factor, A/(f) + B/(f)^2 for a
    repeated one) and can represent the fraction; every wrong option must be unable to (a valid equivalent
    form is a true statement: SR-16).
  "Proper or improper": from the degrees. "Quotient" / "Perform long division": SymPy's polynomial division.
  "What method": a reviewed verdict. Every fraction asked about is in lowest terms; the options are distinct
    in value. In Chromium (390x844) every item is shown through showQ() and every option clicked through
    handle(): the key marked right, the others wrong; options come from MaffsOptions.build().
A self-test plants three of the audit's own faults back (t5-001: A keyed 1/2; t5-004: remainder keyed 2;
t5-005: the valid form (Ax+B)/(x-1)^2 + C/(x+2) as a wrong option), and Play Again without MaffsLock.screen (a
double click on it opened /leaderboards/); each must FAIL naming its item.

    python scripts/verify-partial-fractions-duel.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, rationalize,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'partial-fractions-duel'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNT = 50
x, A, B, C, Q = sp.symbols('x A B C Q')
LOCAL = {'x': x, 'A': A, 'B': B, 'C': C, 'Q': Q}
TRANS = standard_transformations + (implicit_multiplication_application, rationalize)
AUDIT = {8: 't5-001', 12: 't5-002', 27: 't5-003', 46: 't5-004', 38: 't5-005', 39: 't5-006'}


def group(s, i):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '{') - (s[j] == '}')
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in %r' % s)


def read(s):
    s = s.replace('\u2212', '-').replace('?', 'Q')
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            p, j = group(s, i + m.end() - 1)
            q, k = group(s, j)
            out, i = out + '((%s)/(%s))' % (read(p), read(q)), k
            continue
        if s[i] == '{':
            p, j = group(s, i)
            out, i = out + '(%s)' % read(p), j
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX command in %r' % s)
        out, i = out + ('**' if s[i] == '^' else s[i]), i + 1
    try:
        return parse_expr(out, local_dict=LOCAL, transformations=TRANS)
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (s, out, e))


def solve_identity(lhs, rhs, unknowns):
    """The values of the unknowns making lhs == rhs for all x; None if there are none."""
    num = sp.numer(sp.together(lhs - rhs))
    eqs = sp.Poly(sp.expand(num), x).all_coeffs()
    sol = sp.solve(eqs, unknowns, dict=True)
    return sol[0] if sol else None


def standard_form(frac):
    """A/(f) for each linear factor, A/f + B/f^2 for a squared one (letters A, B, C in order)."""
    terms, letters = [], iter([A, B, C, sp.Symbol('D'), sp.Symbol('E')])
    _, factors = sp.factor_list(sp.denom(frac))
    for f, e in factors:
        for k in range(1, e + 1):
            terms.append(next(letters) / f ** k)
    return terms


def check_bank(fails, bank):
    if len(bank) != COUNT:
        fails.append('bank: %d items, expected %d' % (len(bank), COUNT))
    for i, q in enumerate(bank):
        w = 'item %d (%s | %s)%s' % (i, q['q'], q['ask'], ' (partial-fractions-duel-%s)' % AUDIT[i] if i in AUDIT else '')
        opts = [q['correct']] + q['d']
        ask = q['ask']
        if len(set(opts)) != 4:
            fails.append('%s: the options are not four distinct strings' % w)
        try:
            parts = [read(p) for p in q['q'].split('=')]
        except ValueError as e:
            fails.append('%s: %s (extend read())' % (w, e))
            continue
        frac = parts[0]
        if sp.gcd(sp.numer(sp.together(frac)), sp.denom(sp.together(frac))) != 1 or \
                sp.degree(sp.gcd(*[sp.Poly(t, x) for t in (sp.numer(frac), sp.denom(frac))]).as_expr(), x) > 0:
            fails.append('%s: the fraction is not in lowest terms' % w)
        if ask.startswith('What method'):
            if q['correct'] != 'Substitution or comparing coefficients':
                fails.append('%s: keyed %r; partial fractions are found by substitution or comparing coefficients' % (w, q['correct']))
            continue
        if 'proper or improper' in ask:
            want = 'Improper' if sp.degree(sp.numer(frac), x) >= sp.degree(sp.denom(frac), x) else 'Proper'
            if q['correct'] != want:
                fails.append('%s: keyed %s, it is %s' % (w, q['correct'], want))
            continue
        try:
            vals = [read(o) for o in opts]
        except ValueError as e:
            fails.append('%s: %s (extend read())' % (w, e))
            continue
        if ask.startswith('Form of decomposition'):
            std = sorted(str(sp.factor(sp.denom(t))) for t in standard_form(frac))
            got = sorted(str(sp.factor(sp.denom(t))) for t in sp.Add.make_args(vals[0]))
            if got != std:
                fails.append('%s: keyed %s, the standard form has denominators %s' % (w, q['correct'], std))
            for o, v in zip(opts, vals):
                ok = solve_identity(frac, v, sorted(v.free_symbols - {x}, key=str)) is not None
                if o == q['correct'] and not ok:
                    fails.append('%s: the keyed form cannot represent the fraction' % w)
                if o != q['correct'] and ok:
                    fails.append('%s: the wrong option %s is a valid form of the fraction (SR-16)' % (w, o))
            continue
        if re.match(r'Find [ABC]\b', ask) or 'remainder' in ask:
            if len(parts) != 2:
                fails.append('%s: the stem does not state the decomposition form (fraction = form)' % w)
                continue
            letter = Q if 'remainder' in ask else sp.Symbol(ask.split()[1])
            sol = solve_identity(frac, parts[1], sorted(parts[1].free_symbols - {x}, key=str))
            if sol is None:
                fails.append('%s: the stated form cannot represent the fraction' % w)
                continue
            target = sol[letter]
        elif 'uotient' in ask or 'long division' in ask:
            qt, rm = sp.div(sp.numer(sp.together(frac)), sp.denom(sp.together(frac)), x)
            target = qt if 'uotient' in ask else qt + rm / sp.denom(sp.together(frac))
        else:
            fails.append('%s: no rule for this ask (extend check_bank)' % w)
            continue
        if sp.simplify(vals[0] - target) != 0:
            fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], target))
        for o, v in zip(opts[1:], vals[1:]):
            if sp.simplify(v - target) == 0:
                fails.append('%s: the wrong option %s is also right (SR-16)' % (w, o))
        for p in range(4):
            for k in range(p + 1, 4):
                if sp.simplify(vals[p] - vals[k]) == 0:
                    fails.append('%s: options %s and %s are equal in value' % (w, opts[p], opts[k]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  QUESTIONS.alevel.forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      questions = [q]; qIdx = 0; totalQ = 1; score = 0; correctCount = 0; streak = 0;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([i, pick, shown.length + ' options on screen']);
      const b = shown.find(x => x.dataset.val === pick);
      if (!b) { out.push([i, pick, 'not on screen']); continue; }
      b.click();
      const right = b.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([i, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""
# Answer once (canon 7.6.0, MaffsLock; partial-fractions-duel-t5-007): with the real 300 ms window, the key clicked and then Enter three times
# on it counts once, and the results screen submits once.
LOCK_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const q = QUESTIONS.alevel[22];
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

# Play Again (canon 7.6.0, MaffsLock.screen): it shows the menu, whose "Global leaderboard" link and Start button
# are under the pointer at some widths. The second click of a double click, or a click on either within the 300 ms
# window, must do nothing: before the fix a double click on Play Again at 1280x900 opened /leaderboards/.
TO_RESULTS_JS = r"""() => {
  window.MaffsLeaderboard = { submitScore: () => Promise.resolve() };
  startGame(); end();
  const b = document.querySelector('#results .play-again'); b.scrollIntoView({ block: 'center' });
  const r = b.getBoundingClientRect();
  return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
}"""
MENU_RECTS_JS = r"""() => ['#menu a[href="/leaderboards/"]', '#menu .play-again'].map(sel => {
  const r = document.querySelector(sel).getBoundingClientRect();
  return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
})"""
STATE_JS = r"""() => ({ menu: document.getElementById('menu').classList.contains('active'),
                     game: document.getElementById('game').classList.contains('active') })"""


def check_play_again(fails, page, url):
    """The second click after Play Again (a double click, or a click on the menu's link or Start) is dropped."""
    page.set_viewport_size({'width': 1280, 'height': 900})
    for how in ('a double click on Play Again', 'Play Again, then the leaderboard link and Start at once'):
        page.goto(url, wait_until='load', timeout=20000)
        page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
        r = page.evaluate(TO_RESULTS_JS)
        if how.startswith('a double'):
            page.mouse.dblclick(r['x'], r['y'])
        else:
            page.mouse.click(r['x'], r['y'])
            for q in page.evaluate(MENU_RECTS_JS):
                page.mouse.click(q['x'], q['y'])
        page.wait_for_timeout(400)
        if '/games/%s/' % SLUG not in page.url:
            fails.append('Play Again: %s opened %s (MaffsLock.screen on the menu)' % (how, page.url))
            continue
        st = page.evaluate(STATE_JS)
        if not st['menu'] or st['game']:
            fails.append('Play Again: %s left the menu (%s; MaffsLock.screen on the menu)' % (how, st))


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
            bank = page.evaluate('() => QUESTIONS.alevel')
            lk = page.evaluate(LOCK_JS)
            if lk['correct'] != 1:
                fails.append('the key clicked, then Enter three times on it, counted %d times (partial-fractions-duel-t5-007)' % lk['correct'])
            if lk['submits'] != 1:
                fails.append('the results screen submitted %d scores (MaffsLock.finishOnce)' % lk['submits'])
            page.reload(wait_until='load')
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            for i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('item %d in Chromium: option %s %s' % (i, pick, what))
            check_play_again(fails, page, base + '/games/%s/?cb=verify' % SLUG)
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('item 8 ', 't5-001: A keyed 1/2', "correct:'-\\\\dfrac{1}{2}',d:['\\\\dfrac{1}{2}','1','\\\\dfrac{5}{2}']",
     "correct:'\\\\dfrac{1}{2}',d:['-\\\\dfrac{1}{2}','1','\\\\dfrac{5}{2}']"),
    ('item 46 ', 't5-004: remainder keyed 2', "correct:'3',d:['2','5','0']", "correct:'2',d:['3','5','0']"),
    ('item 38 ', 't5-005: a valid equivalent form as a wrong option',
     "'\\\\dfrac{A}{x-1}+\\\\dfrac{B}{x-1}+\\\\dfrac{C}{x+2}'", "'\\\\dfrac{Ax+B}{(x-1)^2}+\\\\dfrac{C}{x+2}'"),
    ('Play Again: ', 't5-007: Play Again without MaffsLock.screen',
     "function showMenu(){show('menu');MaffsLock.screen(document.getElementById('menu'))}",
     "function showMenu(){show('menu')}"),
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
    print('%s: %d items solved from their stems (SymPy), every option clicked in Chromium' % (SLUG, len(bank) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-52s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-52s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
