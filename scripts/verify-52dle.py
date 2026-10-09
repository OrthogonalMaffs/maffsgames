#!/usr/bin/env python3
# ci-line: 52-dle (every puzzle's number recomputed from its clue and hints; every guess marked exactly in Chromium) |
"""52-dle: a guess wins only when it IS the day's number, and every puzzle's number is what its words say.

The game shows one of 20 puzzles a day (a clue, three hints, a category) and gives six guesses at a whole number.
The tranche 2 audit of 6 Oct 2026 found the guess read by parseInt(), which cuts a decimal before the
exact-match check: 23.9 won the 23 puzzle and 314.16 won the pi puzzle (52dle-t2-001, HIGH; contract
LISTED-HIGH, 9 Oct 2026). The guess is now marked by the shared MaffsAnswer.exact() on the raw typed text.

Checks:
  every puzzle: the number its clue and hints describe, recomputed (FACTS: each claim pinned by its words, so
  an edited clue fails until its fact is reviewed); and in Chromium (390x844), for every puzzle, guesses typed
  into the box and submitted through the Guess button, the mark read from the guess row the student sees:
  the number itself, and the number written with a trailing ".0", are an exact match; the number with ".9"
  added, a decimal above it, one more and one less are not; an empty box is not marked at all.
A self-test plants main's parseInt() back into a copy of the page and a wrong number into one puzzle; each
must FAIL naming its puzzle.

    python scripts/verify-52dle.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = '52dle'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')


def fib(n):
    return sp.fibonacci(n)


def is_fib(n):
    return any(fib(k) == n for k in range(1, 40))


def nth_prime(n):
    return sp.prime(n)


def emirp(n):
    return sp.isprime(n) and sp.isprime(int(str(n)[::-1]))


def perfect(n):
    return sum(sp.divisors(n)) - n == n


# Each puzzle's number from its own words: [(words the clue or hints must carry, claim about a)].
FACTS = {
    52: [('I am the number of cards in a standard deck', lambda a: a == 52), ('52! ≈ 8 × 10⁶⁷', lambda a: 8e67 <= float(sp.factorial(a)) < 9e67),
         ('I am less than 100', lambda a: a < 100), ('I am even', lambda a: a % 2 == 0), ('I am 4 × 13', lambda a: a == 4 * 13)],
    89: [('11th Fibonacci', lambda a: a == fib(11)), ('My reverse, 98, is NOT prime', lambda a: not sp.isprime(98) and str(a)[::-1] == '98'),
         ('largest two-digit Fibonacci', lambda a: a == max(f for f in map(fib, range(1, 20)) if 10 <= f < 100)),
         ('between 80 and 100', lambda a: 80 < a < 100), ('I am odd', lambda a: a % 2 == 1)],
    31: [('11th prime', lambda a: a == nth_prime(11)), ('emirp', emirp), ('less than 40', lambda a: a < 40),
         ('digits sum to 4', lambda a: sum(map(int, str(a))) == 4)],
    271: [('first three digits of e', lambda a: a == int(str(sp.N(sp.E, 10)).replace('.', '')[:3])),
          ('between 200 and 300', lambda a: 200 < a < 300), ('contain the digit 7', lambda a: '7' in str(a))],
    314: [('first three significant digits of π', lambda a: a == int(str(sp.N(sp.pi, 10)).replace('.', '')[:3])),
          ('between 300 and 320', lambda a: 300 < a < 320), ('100 × (π to 2 d.p.)', lambda a: a == 100 * sp.Rational('3.14'))],
    144: [('12 squared', lambda a: a == 12 ** 2), ('12th Fibonacci', lambda a: a == fib(12)), ('perfect square', lambda a: sp.sqrt(a).is_Integer)],
    97: [('largest two-digit prime', lambda a: a == sp.prevprime(100)), ('79, is also prime', lambda a: emirp(a) and str(a)[::-1] == '79'),
         ('digits sum to 16', lambda a: sum(map(int, str(a))) == 16)],
    53: [('16th prime', lambda a: a == nth_prime(16)), ('one more than 52', lambda a: a == 53),
         ('nearest prime greater than 52', lambda a: a == sp.nextprime(52))],
    42: [('6 × 7', lambda a: a == 6 * 7), ('Ten less than 52', lambda a: a == 52 - 10), ('between 40 and 45', lambda a: 40 < a < 45)],
    1618: [('first four digits', lambda a: a == int(str(sp.N(sp.GoldenRatio, 10)).replace('.', '')[:4])),
           ('between 1600 and 1650', lambda a: 1600 < a < 1650)],
    2704: [('52 squared', lambda a: a == 52 ** 2), ('between 2700 and 2710', lambda a: 2700 < a < 2710)],
    13: [('I am the 6th prime', lambda a: a == nth_prime(6)), ('7th Fibonacci', lambda a: a == fib(7)), ('12 + 1', lambda a: a == 13)],
    37: [('permutable prime', lambda a: sp.isprime(a) and sp.isprime(int(str(a)[::-1]))), ('between 30 and 40', lambda a: 30 < a < 40)],
    100: [('10 squared', lambda a: a == 10 ** 2), ('between 90 and 110', lambda a: 90 < a < 110)],
    7: [('4th prime', lambda a: a == nth_prime(4)), ('days in a week', lambda a: a == 7), ('less than 10', lambda a: a < 10)],
    28: [('second perfect number', lambda a: a == [n for n in range(2, 500) if perfect(n)][1]),
         ('(1,2,4,7,14)', lambda a: sp.divisors(a)[:-1] == [1, 2, 4, 7, 14]), ('between 20 and 35', lambda a: 20 < a < 35)],
    1597: [('17th Fibonacci', lambda a: a == fib(17)), ('also prime', lambda a: sp.isprime(a)),
           ('between 1500 and 1600', lambda a: 1500 < a < 1600)],
    64: [('8 squared', lambda a: a == 8 ** 2), ('4 cubed', lambda a: a == 4 ** 3),
         ('both a perfect square and a perfect cube below 100',
          lambda a: [n for n in range(2, 100) if sp.integer_nthroot(n, 6)[1]] == [a])],
    23: [('9th prime', lambda a: a == nth_prime(9)), ('between 20 and 30', lambda a: 20 < a < 30)],
    521: [('2^521 − 1 is a Mersenne prime', lambda a: a in (2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521)),
          ('between 500 and 530', lambda a: 500 < a < 530)],
}


def check_facts(fails, puzzles):
    if sorted(p['a'] for p in puzzles) != sorted(FACTS):
        fails.append('puzzles: numbers %s, FACTS covers %s (a new puzzle needs its facts)'
                     % (sorted(p['a'] for p in puzzles), sorted(FACTS)))
    for k, p in enumerate(puzzles):
        words = ' '.join([p['clue']] + list(p['hints']))
        # Which number the words describe: the FACTS entry whose first phrase they carry.
        described = [n for n, facts in FACTS.items() if facts[0][0] in words]
        if described != [p['a']]:
            fails.append('puzzle %d (%s): its words describe %s' % (k, p['a'], described or 'no number in FACTS'))
        for phrase, claim in FACTS.get(p['a'], []):
            if phrase not in words:
                fails.append('puzzle %d (%s): its words no longer say "%s" (review FACTS)' % (k, p['a'], phrase))
            elif not claim(p['a']):
                fails.append('puzzle %d (%s): "%s" is false for %s' % (k, p['a'], phrase, p['a']))


# Each case: (what is typed, an exact match?). The number itself and its ".0" form are the same number.
def cases(a):
    return [(str(a), True), (str(a) + '.0', True), (str(a) + '.9', False), ('%s.16' % a, False),
            (str(a + 1), False), (str(a - 1), False), ('', None)]


SWEEP_JS = r"""(cases) => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  const input = document.getElementById('guess-input'), area = document.getElementById('input-area');
  PUZZLES.forEach((p, k) => {
    for (const [typed, exact] of cases[k]) {
      try { localStorage.clear(); } catch (e) {}
      puzzle = p; state = defaultState(); renderGuesses();
      area.style.pointerEvents = ''; area.style.opacity = ''; document.getElementById('submit-btn').disabled = false;
      MaffsLock.fresh(area);
      input.value = typed;
      document.getElementById('submit-btn').click();
      const rows = [...document.querySelectorAll('#guess-history .guess-row')];
      if (exact === null) {
        if (rows.length) out.push([k, typed, 'an empty box was marked']);
        continue;
      }
      if (rows.length !== 1) { out.push([k, typed, rows.length + ' guess rows after one guess']); continue; }
      const shown = rows[0].querySelector('.guess-feedback').textContent.trim();
      const hit = shown === 'Exact match.';
      if (hit !== exact) out.push([k, typed, (hit ? 'marked an exact match' : 'not marked an exact match') + ' (row: ' + rows[0].textContent.replace(/\s+/g, ' ').trim() + ')']);
    }
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep guesses at once
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof PUZZLES !== "undefined"', timeout=15000)
            puzzles = page.evaluate('() => PUZZLES')
            for k, typed, what in page.evaluate(SWEEP_JS, [cases(p['a']) for p in puzzles]):
                fails.append('puzzle %d (%s): typed %r: %s' % (k, puzzles[k]['a'], typed, what))
            browser.close()
            errors = [e for e in errors if 'firebase' not in e.lower()]
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return puzzles
    finally:
        proc.terminate()
        proc.wait()


# (the puzzle the failure must name, what is planted, today's text, the fault).
PLANTS = [
    ('puzzle ', 't2-001: the guess read by parseInt()',
     'const raw = input.value.trim();', 'const raw = String(parseInt(input.value.trim()));'),
    ('puzzle 1 (88)', 'a wrong number: 88 for the 11th Fibonacci', '{a:89,', '{a:88,'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    puzzles = play(fails, html)
    if puzzles is not None:
        check_facts(fails, puzzles)
    print('%s: %d puzzles, every number recomputed from its words, %d guesses marked in Chromium'
          % (SLUG, len(puzzles or []), sum(len(cases(p['a'])) for p in puzzles or [])))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
            if planted is not None:
                check_facts(rep, planted)
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
