#!/usr/bin/env python3
# ci-line: B2 | Prisoner's Dilemma (C and D keys play a move, but never while initials or other text are being typed; Chromium) |
"""Prisoner's Dilemma: the C and D keys play moves, but text typed into a field never does.

The game plays the iterated dilemma against computer opponents, singly or as a tournament, with C and D as
keyboard shortcuts for Cooperate and Defect. The tranche 4 audit of 6 Oct 2026 found the shortcuts live under the
shared leaderboard's initials overlay: initials typed after one match played moves in the next ('CDX': round 0
-> 1, history ['cooperate']) (prisoners-dilemma-t4-002, HIGH; contract LISTED-HIGH, 9 Oct 2026: keyboard play is
ignored while the overlay is open). prisoners-dilemma-t4-001 (the board ranks whichever opponent is chosen) is
Jon's design decision and not checked here.

Checks, in Chromium (390x844), on a tournament's first match: C pressed on the page plays a move (the shortcut
still works); with the initials overlay open (the shared module's #mfg-initials-overlay, an input focused inside
it) typing "CDC" plays nothing; typing "dd" into any other text field plays nothing. A self-test plants main's
handler (no guard); it must FAIL.

    python scripts/verify-prisoners-dilemma.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'prisoners-dilemma'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')

FRESH_MATCH = """() => { document.querySelectorAll('#mfg-initials-overlay, #pdTestField').forEach(x => x.remove());
  startTournament(); return [roundNum, history.length]; }"""
OVERLAY = """() => { const o = document.createElement('div'); o.id = 'mfg-initials-overlay';
  o.innerHTML = '<input id="pdInitials" maxlength="3">'; document.body.appendChild(o);
  document.getElementById('pdInitials').focus(); }"""
FIELD = """() => { const f = document.createElement('input'); f.id = 'pdTestField'; document.body.appendChild(f); f.focus(); }"""
# A move made: the choice area locks and the reveal shows at once; roundNum and history follow the reveal.
STATE = """() => (MaffsLock.isLocked(document.getElementById('choiceArea'))
  || document.getElementById('revealArea').style.display === 'flex' || roundNum > 0 || history.length > 0)"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof startTournament === "function"', timeout=15000)

            # The shortcut itself still plays a move.
            page.evaluate(FRESH_MATCH)
            time.sleep(0.5)                                   # MaffsLock's fresh window on a new match
            page.locator('body').click(position={'x': 2, 'y': 2})
            page.keyboard.press('c')
            time.sleep(0.2)
            if not page.evaluate(STATE):
                fails.append('the C key no longer plays a move on the game screen')
            for what, setup, typed in (('the initials overlay', OVERLAY, 'CDC'), ('a text field', FIELD, 'dd')):
                page.evaluate(FRESH_MATCH)
                time.sleep(0.5)
                page.evaluate(setup)
                page.keyboard.type(typed)
                time.sleep(0.2)
                if page.evaluate(STATE):
                    fails.append('t4-002: typing %r into %s played a move in the match' % (typed, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('t4-002', "t4-002: main's keydown handler (no guard)",
     [("  if (document.getElementById('mfg-initials-overlay')) return;\n", ''),
      ("  if (e.target && e.target.closest && e.target.closest('input, textarea, select, [contenteditable]')) return;\n", '')]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    play(fails, html)
    print('%s: C plays on the game screen; typing in the initials overlay or a field plays nothing (Chromium)' % SLUG)
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
