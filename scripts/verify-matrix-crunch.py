#!/usr/bin/env python3
# ci-line: Matrix Crunch (one answer per question, an option or the singular flag: Enter and Tab+Enter never mark again; both levels; Chromium) |
"""Matrix Crunch: one answer per question, whether an option or the Flag as Singular button.

Determinants, inverses and Cramer's rule in three stages; from Stage 2 a Flag as Singular button answers a question
instead of an option (+25 if the matrix is singular, a life lost if not). The tranche 6 audit of 7 Oct 2026 found
(contract LISTED-HIGH, item 13, 9 Oct 2026):
  matrix-crunch-t6-001  options locked by a CSS class only: Enter after a right answer scored again (96 -> 383,
                        streak 4); Tab+Enter on the revealed key turned a wrong answer right.
  matrix-crunch-t6-002  the flag re-fired on Enter: a singular flag + Enter x3 scored 25 -> 100 and skipped four
                        questions; a wrong flag + Enter x2 lost all three lives on one question.
Both were fixed on main by F1 batch 11 (#200: one MaffsLock covers the options and the flag). The shared answer-lock
check never presses the flag, so this keeps both paths.

SWEEP-1 (batch 11) adds a check of the question bank itself, read from the page's own QUESTIONS (both levels):
  s1-001  a singular-system "What happens?" item has no wrong option that is a bare solution of its system (a true
          statement; SR-16): they read "Exactly one solution, x = 3, y = 0", a false claim.
  s1-002  no context or worked step points at another question ("Same circuit.", "D = 5 (from above)"): the pool is
          shuffled, so each item restates what it needs.
  s1-003  the wrong-flag text names the question, not "this matrix" (Cramer items have a system, no matrix).
  s1-004  every key is recomputed from the item's own matrix or system: determinant = ad - bc, inverse = adjugate / det
          (or the Singular key exactly when det = 0), Cramer's x or y by solving the system; a singular flag agrees
          with det = 0. A plant restores each old text and must be caught.
Not checked: worked steps, misconception texts, distractor origins, option distinctness (t6-006), contexts.

Checks, in Chromium (390x844), each level (further, level4), on real questions with the real lock and timers:
the key clicked then Enter x3 scores once; a wrong option then Tab+Enter on the key leaves the score as it was; at
Stage 2, a singular question flagged then Enter x3 scores +25 once and moves on exactly one question; a non-singular
question flagged then Enter x2 costs exactly one life. A self-test removes the lock from each path; each must FAIL.

    python scripts/verify-matrix-crunch.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import json
import os
import re
import sys
import time
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'matrix-crunch'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
KATEX_DIR = None
FRESH = 0.6          # past MaffsLock's fresh window on a new question

STATE = "() => [score, totalAnswered, lives]"
# Put a question of the wanted kind next, at the wanted stage, and show it.
SETUP = """([st, sing]) => { startGame(); stage = st; updateStage(); buildPool();
  const all = [...QUESTIONS[level].det, ...QUESTIONS[level].inv, ...QUESTIONS[level].cramer];
  const q = all.find(x => !!x.singular === sing);
  pool.unshift(q); totalAnswered = 0; nextQ(); }"""


def page_for(pw, base, html, level):
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
    if KATEX_DIR:
        ctx.route(lambda url: '/katex@' in url and '/dist/' in url, lambda route: route.fulfill(
            path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
    else:
        ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)     # KaTeX from the pinned local copy
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?level=%s&cb=verify' % (SLUG, level), wait_until='load', timeout=20000)
    page.wait_for_function('typeof startGame === "function" && typeof katex !== "undefined"', timeout=15000)
    return browser, page, errors


def play(fails, html):
    if re.search(r'class="hud-label">Time<', html) or 'id="timer"' in html:   # R7 (s1-008): Hidden Count-Up
        fails.append('hud: the running Time is on the HUD; Hidden Count-Up means it is never shown (R7, matrix-crunch-s1-008)')
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for level in ('further', 'level4'):
                browser, page, errors = page_for(pw, base, html, level)
                if page.evaluate('() => level') != level:
                    fails.append('%s: ?level=%s did not select the level' % (level, level))
                opts = page.locator('#options .opt-btn')

                # t6-001: the key, then Enter x3.
                page.evaluate(SETUP, [1, False])
                time.sleep(FRESH)
                key = page.evaluate('() => currentQ.correct')
                vals = [opts.nth(k).get_attribute('data-val') for k in range(opts.count())]
                s0 = page.evaluate(STATE)
                opts.nth(vals.index(key)).click()
                s1 = page.evaluate(STATE)
                for _ in range(3):
                    page.keyboard.press('Enter')
                time.sleep(0.2)
                s2 = page.evaluate(STATE)
                if s1[0] <= s0[0] or s2 != s1:
                    fails.append('t6-001 (%s): the key clicked then Enter x3: [score, question, lives] %s -> %s -> %s '
                                 '(expected one mark)' % (level, s0, s1, s2))

                # t6-001: a wrong option, then Tab+Enter on the revealed key.
                page.evaluate(SETUP, [1, False])
                time.sleep(FRESH)
                key = page.evaluate('() => currentQ.correct')
                vals = [opts.nth(k).get_attribute('data-val') for k in range(opts.count())]
                s0 = page.evaluate(STATE)
                opts.nth(next(k for k, v in enumerate(vals) if v != key)).click()
                opts.nth(vals.index(key)).focus()
                page.keyboard.press('Enter')
                time.sleep(0.2)
                s1 = page.evaluate(STATE)
                if s1[0] != s0[0]:
                    fails.append('t6-001 (%s): a wrong option then Tab+Enter on the key: score %s -> %s (expected '
                                 'unchanged)' % (level, s0[0], s1[0]))

                # t6-002: a singular question flagged at Stage 2, then Enter x3.
                page.evaluate(SETUP, [2, True])
                time.sleep(FRESH)
                s0 = page.evaluate(STATE)
                page.locator('#flagBtn').click()
                for _ in range(3):
                    page.keyboard.press('Enter')
                time.sleep(1.6)                               # the game moves on 1.2 s after a right flag
                s1 = page.evaluate(STATE)
                if s1[0] - s0[0] != 25 or s1[1] - s0[1] != 1 or s1[2] != s0[2]:
                    fails.append('t6-002 (%s): a singular question flagged then Enter x3: [score, question, lives] '
                                 '%s -> %s (expected +25, one question on, no life lost)' % (level, s0, s1))

                # t6-002: a non-singular question flagged, then Enter x2.
                page.evaluate(SETUP, [2, False])
                time.sleep(FRESH)
                s0 = page.evaluate(STATE)
                page.locator('#flagBtn').click()
                for _ in range(2):
                    page.keyboard.press('Enter')
                time.sleep(0.2)
                s1 = page.evaluate(STATE)
                if s0[2] - s1[2] != 1:
                    fails.append('t6-002 (%s): a wrong flag then Enter x2: lives %d -> %d (expected one life lost)'
                                 % (level, s0[2], s1[2]))
                browser.close()
                if errors:
                    fails.append('%s: page errors: %s' % (level, '; '.join(errors[:3])))
    finally:
        proc.terminate()
        proc.wait()


def num(t):
    """A key or matrix entry as a Fraction: 3, -1, 0.75, \\dfrac{9}{5}, \\frac{1}{2}; None if it is not one."""
    t = t.strip()
    m = re.fullmatch(r'(-?)\\d?frac\{(-?[\d.]+)\}\{(-?[\d.]+)\}', t)
    if m:
        v = Fraction(m.group(2)) / Fraction(m.group(3))
        return -v if m.group(1) else v
    try:
        return Fraction(t)
    except (ValueError, ZeroDivisionError):
        return None


def parse_eq(eq):
    """'3I_1 + 2I_2 = 10' -> ([('I_1', 3), ('I_2', 2)], 10)."""
    lhs, rhs = eq.split('=')
    terms = []
    for sign, co, var in re.findall(r'([+-]?)\s*(\d*\.?\d*)\s*([A-Za-z](?:_\d)?)', lhs):
        c = Fraction(co) if co else Fraction(1)
        terms.append((var, -c if sign == '-' else c))
    return terms, Fraction(rhs.strip())


def solve(sys_):
    """Solve a 2x2 system by Cramer's rule; (vars, D, [x, y]) or (vars, 0, None) when singular."""
    (t1, r1), (t2, r2) = parse_eq(sys_[0]), parse_eq(sys_[1])
    vs = [v for v, _ in t1]
    a, b, c, d = t1[0][1], t1[1][1], dict(t2)[vs[0]], dict(t2)[vs[1]]
    D = a * d - b * c
    if D == 0:
        return vs, (a, b, r1), (c, d, r2), 0, None
    return vs, (a, b, r1), (c, d, r2), D, [(r1 * d - b * r2) / D, (a * r2 - r1 * c) / D]


def parse_inverse(key):
    m = re.fullmatch(r'(?:\\dfrac\{(.+?)\}\{(.+?)\})?\\begin\{pmatrix\}(.*)\\end\{pmatrix\}', key)
    if not m:
        return None
    k = Fraction(1) if m.group(1) is None else num(m.group(1)) / num(m.group(2))
    rows = [[num(e) for e in r.split('&')] for r in m.group(3).split('\\\\')]
    if any(e is None for r in rows for e in r):
        return None
    return [[k * e for e in r] for r in rows]


def check_bank(fails, html):
    """Read QUESTIONS from the page and check the s1-001..s1-004 rules; returns nothing, appends to fails."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser, page, _ = page_for(pw, base, html, 'further')
            bank = json.loads(page.evaluate('() => JSON.stringify(QUESTIONS)'))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    for level, groups in bank.items():
        for kind, items in groups.items():
            for i, q in enumerate(items):
                ref = '%s %s[%d]' % (level, kind, i)
                for text in [q.get('ctx', '')] + list(q.get('steps', [])):
                    if re.search(r'^\s*same\b|\bfrom above\b|\bas above\b|\bthe above\b', text, re.I):
                        fails.append('s1-002 (%s): %r points at another question' % (ref, text))
                key = q['correct']
                if kind in ('det', 'inv') and all(isinstance(e, (int, float)) for r in q['m'] for e in r):
                    (a, b), (c, d) = [[Fraction(str(e)) for e in r] for r in q['m']]
                    det = a * d - b * c
                    if bool(q.get('singular')) != (det == 0):
                        fails.append('s1-004 (%s): singular flag %r but det = %s' % (ref, q.get('singular'), det))
                    if kind == 'det' and num(key) != det:
                        fails.append('s1-004 (%s): det key %s but ad - bc = %s' % (ref, key, det))
                    if kind == 'inv':
                        if det == 0:
                            if not key.startswith('Singular'):
                                fails.append('s1-004 (%s): det 0 but key %r' % (ref, key))
                        elif parse_inverse(key) != [[d / det, -b / det], [-c / det, a / det]]:
                            fails.append('s1-004 (%s): inverse key %s is not the adjugate over det %s' % (ref, key, det))
                if kind == 'cramer':
                    vs, e1, e2, D, sol = solve(q['sys'])
                    if bool(q.get('singular')) != (D == 0):
                        fails.append('s1-004 (%s): singular flag %r but D = %s' % (ref, q.get('singular'), D))
                    if sol is not None:
                        ask = q['ask'].replace('\u2081', '_1').replace('\u2082', '_2')
                        hits = [k for k, v in enumerate(vs) if re.search(r'(?<![A-Za-z])%s(?![\w])' % re.escape(v), ask)]
                        want = [num(part) for part in key.split('=')]
                        if len(hits) != 1:
                            fails.append('s1-004 (%s): cannot tell which unknown %r asks for' % (ref, q['ask']))
                        elif any(w != sol[hits[0]] for w in want):
                            fails.append('s1-004 (%s): key %s but %s = %s' % (ref, key, vs[hits[0]], sol[hits[0]]))
                    elif q['ask'] == 'What happens?':
                        for o in q['d']:
                            m = re.fullmatch(r'x = (-?[\d.]+), y = (-?[\d.]+)', o)
                            if m:
                                x, y = Fraction(m.group(1)), Fraction(m.group(2))
                                if e1[0] * x + e1[1] * y == e1[2] and e2[0] * x + e2[1] * y == e2[2]:
                                    fails.append('s1-001 (%s): wrong option %r is a true solution of the system'
                                                 % (ref, o))
    if 'This matrix is not singular' in html or 'This question is not singular (D \\u2260 0)' not in html:
        fails.append('s1-003: the wrong-flag text must say "This question is not singular (D \u2260 0)"')


BANK_PLANTS = [
    ('s1-001', 's1-001: a true solution as a wrong option (Further)',
     [("'Exactly one solution, x = 3, y = 0','Exactly one solution, x = 0, y = 3'", "'x = 3, y = 0','x = 0, y = 3'")]),
    ('s1-001', 's1-001: a true solution as a wrong option (Level 4)',
     [("'Exactly one solution, x = 5, y = 0','No solution','Exactly one solution, x = 0, y = 5'",
       "'x = 5, y = 0','No solution','x = 0, y = 5'")]),
    ('s1-002', 's1-002: "Same circuit."',
     [("ctx:'Kirchhoff\\'s voltage law gives these mesh equations. Solve for the currents.',ask:'Find I\\u2082",
       "ctx:'Same circuit.',ask:'Find I\\u2082")]),
    ('s1-002', 's1-002: "D = 5 (from above)"',
     [("steps:['D = \\\\det\\\\begin{pmatrix}2&1\\\\\\\\1&3\\\\end{pmatrix} = 5','D_y", "steps:['D = 5 (from above)','D_y")]),
    ('s1-003', 's1-003: "This matrix is not singular"',
     [("This question is not singular (D \\u2260 0).", "This matrix is not singular \u2014 its determinant is not zero.")]),
    ('s1-004', 's1-004: a wrong Cramer key',
     [(r"correct:'\\dfrac{9}{5}'", r"correct:'\\dfrac{8}{5}'")]),
    ('s1-004', 's1-004: a wrong determinant key',
     [("correct:'5.25'", "correct:'5.5'")]),
    ('s1-004', 's1-004: a wrong inverse key',
     [(r"correct:'\\dfrac{1}{10}\\begin{pmatrix}3&-1\\\\-2&4\\end{pmatrix}'",
       r"correct:'\\dfrac{1}{10}\\begin{pmatrix}3&1\\\\-2&4\\end{pmatrix}'")]),
]


PLANTS = [
    ('hud:', 's1-008: the HUD Time back', [('<div class="hud-item"><div class="hud-label">Score</div>', '<div class="hud-item"><div class="hud-label">Time</div><div class="hud-val" id="timer">0</div></div><div class="hud-item"><div class="hud-label">Score</div>')]),
    ('t6-001', 't6-001: options with no lock (CSS class only)',
     [('function handleAnswer(btn){\n  if(!answerLock())return;\n', 'function handleAnswer(btn){\n')]),
    ('t6-002', 't6-002: the flag with no lock',
     [('function flagSingular(){\n  if(!answerLock())return;\n', 'function flagSingular(){\n')]),
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
    play(fails, html)
    check_bank(fails, html)
    print('%s: one answer per question in both levels, by option and by the singular flag; bank keys recomputed (Chromium)' % SLUG)
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, swaps in PLANTS:
            planted = html
            for new, old in swaps:
                if planted.count(new) != 1:
                    planted = None
                    break
                planted = planted.replace(new, old)
            if planted is None:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            play(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
        for tag, what, swaps in BANK_PLANTS:
            planted = html
            for new, old in swaps:
                if planted.count(new) != 1:
                    planted = None
                    break
                planted = planted.replace(new, old)
            if planted is None:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
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
