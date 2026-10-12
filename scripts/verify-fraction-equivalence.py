#!/usr/bin/env python3
# ci-line: Fraction Snap (every pair's key and cross-multiplication recomputed, the generator drawn 20000 times, every pair marked both ways in Chromium) |
"""Fraction Snap (fraction-equivalence): is each pair of fractions equivalent? Every key recomputed, every
figure in the working recomputed, every pair marked both ways by the game's own guess().

Two sources of pairs, both read from the page as served:
  Year 6 (?level=year6): a static bank, YEAR6_BANK, 15 dealt per session from it.
  Every other level ("all"): generateQ(), a random generator: n1/d1 in simplest form with n1 < d1 (n1 1..9, d1 2..12),
    then either a multiple of it (x2..x6) or n1*m / (d1*m + 1..3).
The key is whether n1/d1 = n2/d2, recomputed here with fractions.Fraction (the game's own test is never called).

Checks:
  Bank: every pair's equiv flag equals the Fraction comparison; both numbers positive integers and the denominators
    only 2, 3, 4, 5, 6, 8 or 10 (the Year 6 rule in the bank's comment); no pair repeated (either order), but for the one recorded as open finding fraction-equivalence-v20-001 (1/4 vs 1/3
    and 1/3 vs 1/4, items 12 and 18; replacing one is new content); both kinds
    present; a pair whose two fractions are the same fraction written the same way is not allowed.
  Generator: 20000 draws in Chromium, each pair's equiv flag recomputed; every fraction proper and positive; the
    first fraction in simplest form; every multiplier 2 to 6 and every offset 1 to 3 reached; both kinds drawn; an
    equivalent pair is never offered with identical numbers (a x1 multiple). Reported: how many of each.
  Dealing: startGame() with ?level=year6, six times: each session's 15 pairs come from the bank, none twice.
  Marking, in Chromium (390x844), every bank pair and 400 generated pairs, each answered YES and answered NO through
    guess(): the right answer shows "CORRECT" in the feedback and puts the correct style on the button pressed; the
    wrong one shows exactly "WRONG - they are [NOT ]equivalent" (recomputed) and styles the key's button correct.
    The working line is recomputed for both: "n1xd2=A vs n2xd1=B -> EQUAL/NOT EQUAL" with A, B and the verdict.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong key in the bank (1/2 = 2/4 flagged not
equivalent), a wrong answer marked right (any answer), a wrong figure in the working (n1 x d1 for n1 x d2), and a
generator fault (an offset of 0, so an equivalent pair is labelled not equivalent).

    python scripts/verify-fraction-equivalence.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'fraction-equivalence'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
YEAR6_DENOMS = {2, 3, 4, 5, 6, 8, 10}
# A pair that is another pair written the other way round: recorded in the findings file, open (new content would be
# needed to replace it, which is Jon's call). Any other repeat fails.
EXPECTED_REPEATS = {frozenset([(1, 3), (1, 4)]): 'fraction-equivalence-v20-001'}
DRAWS = 20000
MARKED_DRAWS = 400
DEALS = 6
SESSION = 15


def equivalent(p):
    return Fraction(p['n1'], p['d1']) == Fraction(p['n2'], p['d2'])


def working(p, right_key):
    a, b = p['n1'] * p['d2'], p['n2'] * p['d1']
    return '%d×%d=%d vs %d×%d=%d → %s' % (p['n1'], p['d2'], a, p['n2'], p['d1'], b,
                                                          'EQUAL' if a == b else 'NOT EQUAL')


def check_pair(fails, where, p, year6):
    ok = all(isinstance(p.get(k), int) and not isinstance(p.get(k), bool) and p[k] > 0
             for k in ('n1', 'd1', 'n2', 'd2'))
    if not ok:
        fails.append('%s: a number is not a positive integer: %r' % (where, p))
        return False
    if p['equiv'] != equivalent(p):
        fails.append('%s: keyed %s, but %d/%d %s %d/%d' % (
            where, 'equivalent' if p['equiv'] else 'not equivalent', p['n1'], p['d1'],
            '=' if equivalent(p) else '≠', p['n2'], p['d2']))
    if year6 and not {p['d1'], p['d2']} <= YEAR6_DENOMS:
        fails.append('%s: a denominator outside 2, 3, 4, 5, 6, 8, 10: %r' % (where, p))
    if (p['n1'], p['d1']) == (p['n2'], p['d2']):
        fails.append('%s: the two fractions are written identically' % where)
    return True


def check_bank(fails, bank):
    seen = set()
    for i, p in enumerate(bank, 1):
        check_pair(fails, 'bank item %d' % i, p, True)
        k = frozenset([(p['n1'], p['d1']), (p['n2'], p['d2'])])
        if k in seen and k not in EXPECTED_REPEATS:
            fails.append('bank item %d: the pair is repeated' % i)
        seen.add(k)
    if {bool(p['equiv']) for p in bank} != {True, False}:
        fails.append('the bank does not hold both equivalent and non-equivalent pairs')


def check_draws(fails, draws):
    mults, offs = set(), set()
    kinds = {True: 0, False: 0}
    for i, p in enumerate(draws):
        if not check_pair(fails, 'draw %d' % i, p, False):
            continue
        kinds[equivalent(p)] += 1
        f1 = Fraction(p['n1'], p['d1'])
        if not (0 < f1 < 1 and p['n1'] == f1.numerator and p['d1'] == f1.denominator):
            fails.append('draw %d: the first fraction %d/%d is not proper and in simplest form' % (i, p['n1'], p['d1']))
        if not 0 < Fraction(p['n2'], p['d2']) < 1:
            fails.append('draw %d: the second fraction %d/%d is not proper' % (i, p['n2'], p['d2']))
        if equivalent(p):
            m = Fraction(p['n2'], p['n1'])
            mults.add(m)
        else:
            for m in range(2, 7):
                if p['n2'] == p['n1'] * m and 1 <= p['d2'] - p['d1'] * m <= 3:
                    mults.add(Fraction(m))
                    offs.add(p['d2'] - p['d1'] * m)
        if len(fails) > 20:
            break
    if mults != {Fraction(m) for m in range(2, 7)}:
        fails.append('generator: multipliers reached %s, not 2 to 6' % sorted(map(str, mults)))
    if offs != {1, 2, 3}:
        fails.append('generator: offsets reached %s, not 1 to 3' % sorted(offs))
    if min(kinds.values()) == 0:
        fails.append('generator: only one kind of pair drawn: %r' % kinds)
    return kinds


GEN_JS = "(n) => { const out = []; for (let i = 0; i < n; i++) out.push(generateQ()); return out; }"
MARK_JS = r"""(args) => {
  const [p, val] = args;
  generateQ = () => p;
  score = 0; streak = 0; qNum = 0;
  nextQ();
  guess(val);
  MaffsLock.clearTimers();
  const fb = document.getElementById('feedback');
  return {fb: fb.textContent, cls: fb.className, hint: document.getElementById('hint').textContent,
          yes: document.getElementById('btnYes').className, no: document.getElementById('btnNo').className};
}"""
DEAL_JS = r"""() => { const out = [];
  for (let k = 0; k < %d; k++) { startGame(); const d = [cur];
    for (let i = 1; i < %d; i++) d.push(generateQ());
    out.push(d); MaffsLock.clearTimers(); }
  return out; }""" % (DEALS, SESSION)


def mark_all(fails, page, items, tag):
    for p in items:
        key = equivalent(p)
        for val in (True, False):
            got = page.evaluate(MARK_JS, [p, val])
            where = '%s %d/%d vs %d/%d, %s' % (tag, p['n1'], p['d1'], p['n2'], p['d2'], 'YES' if val else 'NO')
            btn = got['yes'] if val else got['no']
            keybtn = got['yes'] if key else got['no']
            if val == key:
                if not (got['fb'].startswith('CORRECT') and 'correct' in got['cls'] and 'correct' in btn):
                    fails.append('%s: the right answer was not marked right (%r)' % (where, got))
            else:
                want = 'WRONG — they are %sequivalent' % ('' if key else 'NOT ')
                if not (got['fb'] == want and 'wrong' in got['cls'] and 'correct' in keybtn):
                    fails.append('%s: the wrong answer was not marked wrong as %r (%r)' % (where, want, got))
            if got['hint'] != working(p, key):
                fails.append('%s: working %r, recomputed %r' % (where, got['hint'], working(p, key)))


def open_page(pw, base, html, level):
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
    page.goto(base + '/games/%s/?cb=verify%s' % (SLUG, '&level=year6' if level else ''), wait_until='load', timeout=20000)
    page.wait_for_function('typeof YEAR6_BANK !== "undefined" && typeof guess === "function"', timeout=15000)
    return browser, page, errors


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser, page, errors = open_page(pw, base, html, True)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(YEAR6_BANK))')
            check_bank(fails, bank)
            for d in page.evaluate(DEAL_JS):
                keys = [(p['n1'], p['d1'], p['n2'], p['d2']) for p in d]
                inbank = {(p['n1'], p['d1'], p['n2'], p['d2']) for p in bank}
                if len(set(keys)) != len(keys) or not set(keys) <= inbank:
                    fails.append('a Year 6 session is not %d different pairs from the bank' % SESSION)
            mark_all(fails, page, bank, 'Year 6')   # last: marking replaces generateQ in the page
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            browser, page, errors = open_page(pw, base, html, False)
            draws = page.evaluate(GEN_JS, DRAWS)
            stats = check_draws(fails, draws)
            mark_all(fails, page, draws[:MARKED_DRAWS], 'generated')
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats['bank'] = len(bank)
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong key in the bank (1/2 = 2/4 flagged no)', 'keyed',
     '{ n1:1, d1:2, n2:2, d2:4, equiv:true }', '{ n1:1, d1:2, n2:2, d2:4, equiv:false }'),
    ('a wrong answer marked right (any answer)', 'was not marked wrong',
     'const correct=val===cur.equiv;', 'const correct=true;'),
    ('a wrong figure in the working (n1 × d1)', 'working',
     'const cross=cur.n1*cur.d2;', 'const cross=cur.n1*cur.d1;'),
    ('a generator fault (offset 0, re-roll guard gone)', 'keyed',
     [('d2=d1*mult+randInt(1,3);', 'd2=d1*mult+randInt(0,3);'), ('while(n1*d2===n2*d1);', 'while(false);')]),
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
    print('%s: %d bank pairs and %d generated draws recomputed (key and working); %d bank pairs and %d draws '
          'marked both ways in Chromium; draws: %s equivalent, %s not' % (
              SLUG, st.get('bank', 0), DRAWS, st.get('bank', 0), MARKED_DRAWS, st.get(True), st.get(False)))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, *edits in PLANTS:
            edits = edits[0] if isinstance(edits[0], list) else [tuple(edits)]
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-52s *** CANNOT PLANT (%r) ***' % (what, bad[0]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-52s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
