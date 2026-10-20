#!/usr/bin/env python3
# ci-line: Weekly fact "100 Doors" (the front-page card shows its summary and expanded text exactly, with its button and Share, at 320, 390 and 1280 px, with no overflow) |
# ci-deps: index.html
"""Browser test for the "Monty Hall, With 100 Doors" weekly fact (contracts MONTY-CARD, 19 Oct 2026, and
MONTY-100-RETITLE, 20 Oct 2026: the title no longer says "Obvious", and the expanded text is Jon's 20 Oct wording).

    python scripts/test-fact-monty.py [--against FILE]

The card used to say "Monty opens 98 goat doors" without the setup (a car behind one door, goats behind the rest)
or the condition that makes switching win (the host knows where the car is and opens only goat doors; at random it
would be 50/50). Its words are now Jon's, held exactly here. The front page shows one fact a week
(getWeekIndex()), so this test shows this one by pointing getWeekIndex at it and calling loadFact(), the page's own
code, then reads the card at 320x568, 390x844 and 1280x900:

  summary   collapsed: #factTitle is the title and #factHook the summary, exactly; the expansion is closed. At 1280 px
            the summary must be shown. At 600 px and below the page's compact mode (compactSecondary, .cmp-on)
            hides it with no way to open it: that is the layout, which MONTY-CARD may not touch, so it is
            printed, not failed (Jon, 19 Oct 2026: ship the text, test truthfully; the phone gap is reported)
  expanded  after the page's own "Read more" (toggleFact): #factText is the expanded text, exactly; the button reads
            "Test your probability intuition →" and links to games/probability-paradox/; Share is shown
  fit       in both states: no sideways scroll on the page, and the title, summary, expanded text and both
            buttons lie inside the card

verify-facts.py separately recomputes every figure in the card's words (MONTY-CARD pins).
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

PAGE = os.path.join(os.path.dirname(HERE), 'index.html')
TITLE = 'Monty Hall, With 100 Doors'
SUMMARY = ('100 doors: a car behind one, goats behind the other 99. You pick one. The host, who knows where the car '
           'is, opens 98 of the others, all goats. Should you switch? Switching wins 99 times in 100.')
EXPANDED = ("You pick door 1. The host opens every other door except door 57. Why did he skip 57? Either your door "
            "hides the car, which happens 1 time in 100, or 57 does, which happens the other 99 times. Switching is "
            "the same as swapping your one door for all 99 others; the host has just opened the empty ones for you. "
            "The catch: he must know where the car is. If he opened doors at random and happened to show only goats, "
            "it would be 50/50. Three doors work the same way (switching wins 2 times in 3); it just doesn't feel "
            "as clear.")
BUTTON = 'Test your probability intuition →'
WIDTHS = ((320, 568), (390, 844), (1280, 900))

SHOW = """(title) => { const i = FACTS.findIndex(f => f.t === title); if (i < 0) return -1;
  window.getWeekIndex = () => i; loadFact(); return i; }"""
READ = """() => { const $ = id => document.getElementById(id), card = $('factCard').getBoundingClientRect();
  const vis = el => !!el && el.offsetParent !== null && getComputedStyle(el).display !== 'none';
  const inside = el => { const r = el.getBoundingClientRect(); return r.left >= card.left - 0.5 && r.right <= card.right + 0.5; };
  const out = [];
  for (const id of ['factTitle', 'factHook', 'factText', 'factGameBtn', 'factShareBtn']) {
    const el = $(id); if (vis(el) && (!inside(el) || el.scrollWidth > el.clientWidth + 1)) out.push(id + ' leaves the card');
  }
  if (document.documentElement.scrollWidth > document.documentElement.clientWidth) out.push('the page scrolls sideways by ' +
    (document.documentElement.scrollWidth - document.documentElement.clientWidth) + ' px');
  return { title: $('factTitle').textContent, hook: $('factHook').textContent, text: $('factText').textContent,
           open: $('factExpansion').classList.contains('open'), textShown: vis($('factText')), hookShown: vis($('factHook')),
           btn: vis($('factGameBtn')) ? [$('factGameBtn').textContent, $('factGameBtn').getAttribute('href')] : null,
           share: vis($('factShareBtn')) ? $('factShareBtn').textContent : null, fit: out }; }"""


def run(html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    faults, notes = [], []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for w, h in WIDTHS:
                ctx = browser.new_context(viewport={'width': w, 'height': h})
                ctx.route(lambda u: not u.startswith(base) and not bc.is_font_cdn(u), lambda r: r.abort())
                ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)   # Outfit from the pinned copy
                if html is not None:
                    ctx.route(re.compile(r'^%s/(\?[^/]*)?$' % re.escape(base)), lambda r: r.fulfill(
                        status=200, content_type='text/html; charset=utf-8', body=html))
                page = ctx.new_page()
                page.goto(base + '/?cb=monty%d' % w, wait_until='load', timeout=30000)
                page.wait_for_function('typeof FACTS !== "undefined" && typeof loadFact === "function"', timeout=15000)
                if page.evaluate(SHOW, TITLE) < 0:
                    faults.append('no fact titled %r' % TITLE)
                    ctx.close()
                    break
                page.wait_for_timeout(150)
                closed = page.evaluate(READ)
                page.click('#factToggle')
                page.wait_for_timeout(200)
                opened = page.evaluate(READ)
                ctx.close()
                at = '%d px' % w
                if closed['title'] != TITLE:
                    faults.append('%s: the title reads %r' % (at, closed['title']))
                if closed['hook'] != SUMMARY:
                    faults.append('%s: the summary reads %r, want %r' % (at, closed['hook'], SUMMARY))
                if w > 600 and not closed['hookShown']:
                    faults.append('%s: the summary is not shown' % at)
                if w <= 600:
                    notes.append('%s: summary %s (compact mode)' % (at, 'shown' if closed['hookShown'] else 'hidden'))
                if not opened['textShown']:
                    faults.append('%s: expanded, the text is not shown' % at)
                if closed['open'] or closed['textShown']:
                    faults.append('%s: the expanded text shows before "Read more"' % at)
                if not opened['open'] or opened['text'] != EXPANDED:
                    faults.append('%s: expanded, the text reads %r, want %r' % (at, opened['text'], EXPANDED))
                if opened['hook'] != SUMMARY:
                    faults.append('%s: expanded, the summary reads %r' % (at, opened['hook']))
                if opened['btn'] != [BUTTON, 'games/probability-paradox/']:
                    faults.append('%s: the button is %r, want %r to games/probability-paradox/' % (at, opened['btn'], BUTTON))
                if opened['share'] != 'Share':
                    faults.append('%s: Share is %r' % (at, opened['share']))
                for state, r in (('summary', closed), ('expanded', opened)):
                    for f in r['fit']:
                        faults.append('%s, %s: %s' % (at, state, f))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return faults, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--against', help='serve this file as the front page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    html = open(args.against, encoding='utf-8').read() if args.against else None
    faults, notes = run(html)
    print('Weekly fact %r: summary and expanded text, button and Share, at %s px' % (
        TITLE, ', '.join(str(w) for w, _ in WIDTHS)))
    for n in notes:
        print('  note  ' + n)
    for f in faults:
        print('  FAIL  ' + f[:400])
    print('PASS' if not faults else 'FAIL')
    return 1 if faults else 0


if __name__ == '__main__':
    sys.exit(main())
