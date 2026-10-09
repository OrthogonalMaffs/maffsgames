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

Checks, in Chromium (390x844), each level (further, level4), on real questions with the real lock and timers:
the key clicked then Enter x3 scores once; a wrong option then Tab+Enter on the key leaves the score as it was; at
Stage 2, a singular question flagged then Enter x3 scores +25 once and moves on exactly one question; a non-singular
question flagged then Enter x2 costs exactly one life. A self-test removes the lock from each path; each must FAIL.

    python scripts/verify-matrix-crunch.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys
import time

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
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?level=%s&cb=verify' % (SLUG, level), wait_until='load', timeout=20000)
    page.wait_for_function('typeof startGame === "function" && typeof katex !== "undefined"', timeout=15000)
    return browser, page, errors


def play(fails, html):
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


PLANTS = [
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
    print('%s: one answer per question in both levels, by option and by the singular flag (Chromium)' % SLUG)
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
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
