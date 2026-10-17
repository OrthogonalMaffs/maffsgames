#!/usr/bin/env python3
# ci-line: Factor Race (every pair's key and factor counts recomputed, the KS3 pair table rebuilt and compared, every pair answered both ways in Chromium) |
"""Factor Race: two numbers, tap the one with more factors.

Two sources of pairs, both read from the page as served:
  Year 6 (?level=year6): YEAR6_BANK, 20 pairs, 10 dealt per session.
  KS3 (the default): VALID_PAIRS, built at load from every ordered pair in [2, 60] whose factor counts differ, and
    generatePair() picks one uniformly.
The game keeps no key: the right card is the one with more factors, which this script recomputes by counting the
divisors of each number with its own loop (the game's getFactors() is never trusted for a key).

Checks:
  Year 6 bank: both numbers 1 to 50 (the bank's rule), the two factor counts differ (a tie has no right card), no pair
    repeated in either order, and a session deals 10 different pairs from the bank (five sessions).
  KS3 table: VALID_PAIRS equals, as a set and in size, the pairs recomputed here (a, b in 2..60 with different divisor
    counts); no pair appears twice.
  KS3 draws: 20000 generatePair() calls, every pair in the table; reported: how many distinct pairs were reached.
  Marking, in Chromium (390x844), every Year 6 pair and 600 KS3 pairs (every 5th of the table, from an offset), each
    answered by tapping card A and by tapping card B through guess(): the card with more factors is marked right
    ("CORRECT!", the card styled correct, 10 points); the other is marked wrong ("WRONG! a has X factors; b has Y."
    with the recomputed counts, the key card styled correct). Both cards then read "X factors" and "Y factors". A time-out
    reads "TOO SLOW! a has X factors; b has Y." and scores nothing.
  Start screen: the time it states per question is the countdown's, TIME_PER_Q (it said 5 seconds against a 30 s
    countdown: factor-race-t3-001).
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a tie in the Year 6 bank (12 against 18, both with
6 factors), a wrong answer marked right (any card), a wrong factor count shown (the divisor loop drops n itself), a
bad pair table (equal counts admitted) and the start screen's old "5 seconds".

    python scripts/verify-factor-race.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'factor-race'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LO, HI = 2, 60
YEAR6_MAX = 50
DRAWS = 20000
STRIDE = 5
SESSIONS = 5
SESSION = 10


def nfactors(n):
    """The number of divisors of n, counted by trying every integer from 1 to n."""
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def check_bank(fails, bank):
    seen = set()
    for i, q in enumerate(bank, 1):
        a, b = q['a'], q['b']
        where = 'Year 6 item %d (%d, %d)' % (i, a, b)
        if not all(isinstance(x, int) and 1 <= x <= YEAR6_MAX for x in (a, b)):
            fails.append('%s: a number outside 1 to %d' % (where, YEAR6_MAX))
            continue
        if nfactors(a) == nfactors(b):
            fails.append('%s: both have %d factors, so neither card is right' % (where, nfactors(a)))
        k = frozenset([a, b])
        if k in seen:
            fails.append('%s: the pair is repeated' % where)
        seen.add(k)


def check_table(fails, table):
    want = {(a, b) for a in range(LO, HI + 1) for b in range(LO, HI + 1) if nfactors(a) != nfactors(b)}
    got = [tuple(p) for p in table]
    if len(set(got)) != len(got):
        fails.append('KS3 table: a pair appears twice')
    extra, missing = set(got) - want, want - set(got)
    if extra:
        fails.append('KS3 table: %d pairs that should not be there, e.g. %r (equal factor counts or out of range)' % (
            len(extra), sorted(extra)[:3]))
    if missing:
        fails.append('KS3 table: %d pairs missing, e.g. %r' % (len(missing), sorted(missing)[:3]))
    return want


GEN_JS = "(n) => { const out = []; for (let i = 0; i < n; i++) { const p = generatePair(); out.push([p.a, p.b]); } return out; }"
TABLE_JS = "() => VALID_PAIRS.map(p => [p[0], p[1]])"
MARK_JS = r"""(args) => {
  const [a, b, choice, slow] = args;
  generatePair = () => ({a: a, b: b, fa: getFactors(a), fb: getFactors(b)});
  score = 0; streak = 0; qNum = 0;
  nextQuestion();
  if (slow) timeOut(); else guess(choice);
  MaffsLock.clearTimers();
  return {fb: document.getElementById('feedback').textContent, cls: document.getElementById('feedback').className,
          score: score, ca: document.getElementById('cardA').className, cb: document.getElementById('cardB').className,
          fa: document.getElementById('factorsA').textContent, fbb: document.getElementById('factorsB').textContent};
}"""
DEAL_JS = r"""() => { const out = [];
  for (let k = 0; k < %d; k++) { startGame(); const d = [[currentPair.a, currentPair.b]];
    for (let i = 1; i < %d; i++) { const p = generatePair(); d.push([p.a, p.b]); }
    out.push(d); MaffsLock.clearTimers(); }
  return out; }""" % (SESSIONS, SESSION)


def mark(fails, page, pairs, tag):
    for a, b in pairs:
        ca, cb = nfactors(a), nfactors(b)
        if ca == cb:
            continue
        key = 0 if ca > cb else 1
        for choice in (0, 1):
            got = page.evaluate(MARK_JS, [a, b, choice, False])
            where = '%s %d vs %d, card %s tapped' % (tag, a, b, 'AB'[choice])
            mine, other = (got['ca'], got['cb']) if choice == 0 else (got['cb'], got['ca'])
            if choice == key:
                if not (got['fb'].startswith('CORRECT!') and 'correct' in got['cls'] and got['score'] == 10
                        and 'correct' in mine):
                    fails.append('%s: the right card was not marked right (%r)' % (where, got))
            else:
                want = 'WRONG! %d has %d factors; %d has %d.' % (a, ca, b, cb)
                keycard = other
                if not (got['fb'] == want and 'wrong' in got['cls'] and got['score'] == 0
                        and 'wrong' in mine and 'correct' in keycard):
                    fails.append('%s: the wrong card was not marked wrong as %r (%r)' % (where, want, got))
            if got['fa'] != '%d factors' % ca or got['fbb'] != '%d factors' % cb:
                fails.append('%s: the cards read %r / %r, not %d / %d factors' % (where, got['fa'], got['fbb'], ca, cb))
        got = page.evaluate(MARK_JS, [a, b, 0, True])
        want = 'TOO SLOW! %d has %d factors; %d has %d.' % (a, ca, b, cb)
        if got['fb'] != want or got['score'] != 0:
            fails.append('%s %d vs %d, time-out: %r, expected %r' % (tag, a, b, got['fb'], want))


def open_page(pw, base, html, qs):
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
    page.goto(base + '/games/%s/?cb=verify%s' % (SLUG, qs), wait_until='load', timeout=20000)
    page.wait_for_function('typeof YEAR6_BANK !== "undefined" && typeof guess === "function"', timeout=15000)
    return browser, page, errors


# The seconds per question the start screen states, and the countdown the game runs.
STATED_JS = """() => {
  const m = document.getElementById('startScreen').textContent.match(/You have (\\d+) seconds per question/);
  return { seconds: m ? Number(m[1]) : null, countdown: TIME_PER_Q };
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser, page, errors = open_page(pw, base, html, '&level=year6')
            bank = page.evaluate('() => JSON.parse(JSON.stringify(YEAR6_BANK))')
            check_bank(fails, bank)
            inbank = {frozenset([q['a'], q['b']]) for q in bank}
            for d in page.evaluate(DEAL_JS):
                keys = [frozenset(p) for p in d]
                if len(d) != SESSION or len(set(keys)) != len(keys) or not set(keys) <= inbank:
                    fails.append('a Year 6 session is not %d different pairs from the bank: %r' % (SESSION, d))
            mark(fails, page, [(q['a'], q['b']) for q in bank], 'Year 6')
            if errors:
                fails.append('Year 6 page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            browser, page, errors = open_page(pw, base, html, '')
            said = page.evaluate(STATED_JS)
            if said['seconds'] is None or said['seconds'] * 1000 != said['countdown']:
                fails.append('start screen states %s seconds per question; the countdown is %s ms (TIME_PER_Q)' % (
                    said['seconds'], said['countdown']))
            table = page.evaluate(TABLE_JS)
            want = check_table(fails, table)
            draws = page.evaluate(GEN_JS, DRAWS)
            bad = [d for d in draws if tuple(d) not in want]
            if bad:
                fails.append('generatePair drew %d pairs outside the table, e.g. %r' % (len(bad), bad[:3]))
            sample = [tuple(p) for p in table[3::STRIDE]]
            mark(fails, page, sample, 'KS3')
            if errors:
                fails.append('KS3 page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'bank': len(bank), 'table': len(table), 'reached': len({tuple(d) for d in draws}),
                     'marked': len(sample)}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a tie in the Year 6 bank (12 against 18)', 'neither card is right',
     [('{ a: 12, b: 8 }', '{ a: 12, b: 18 }')]),
    ('a wrong answer marked right (any card)', 'not marked wrong',
     [('const correct = (choice === 0 && aMore) || (choice === 1 && !aMore);', 'const correct = true;')]),
    ('a wrong factor count shown (n itself dropped)', 'factors',
     [('for(let i = 1; i <= n; i++) if(n % i === 0) f.push(i);', 'for(let i = 1; i < n; i++) if(n % i === 0) f.push(i);')]),
    ('a bad pair table (equal counts admitted)', 'KS3 table',
     [('if (counts[a] !== counts[b]) pairs.push([a, b]);', 'if (true) pairs.push([a, b]);')]),
    ('the start screen\'s old "5 seconds"', 'start screen states',
     [('You have 30 seconds per question', 'You have 5 seconds per question')]),
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
    print('%s: %d Year 6 pairs; KS3 table of %d pairs rebuilt and compared; %d draws reached %d distinct pairs; '
          '%d Year 6 + %d KS3 pairs answered both ways and timed out in Chromium' % (
              SLUG, st.get('bank', 0), st.get('table', 0), DRAWS, st.get('reached', 0), st.get('bank', 0),
              st.get('marked', 0)))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-50s *** CANNOT PLANT (%r) ***' % (what, bad[0]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-50s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
