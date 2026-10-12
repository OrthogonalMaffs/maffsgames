#!/usr/bin/env python3
# ci-line: Prime or Composite (every key, hint and explanation recomputed; every number marked both ways in Chromium) |
"""Prime or Composite: every key recomputed, every hint and explanation figure recomputed, every number marked
both ways by the game's own marking.

The game is a static bank of numbers (QUESTIONS, read from the page as served), each with a one-line hint. The
student taps PRIME or COMPOSITE (a two-way choice, so two options and exactly one right); the game's key is its own
isPrime(), which this script never calls.

Checks, independent of the game's code:
  Bank: every n an integer of at least 2, no number repeated, both classes present, a hint on every item.
  Key: primality by trial division in Python (this file), cross-checked against SymPy where it is installed.
  Hints: each hint is one of a small set of claim shapes, and the claim is recomputed from n: "a x b" and
    "Think: a^2" (the product), "Divisible by a and b" (divisible by each), "Two digits" and its kind (the digit
    count; "odd"; "Even number"), "Smallest prime", "Largest two-digit prime", "First four-digit prime", "Largest
    four-digit prime", "Mersenne prime" (2^p - 1 and prime) and "Fermat prime" (2^(2^k) + 1 and prime). A hint of
    any other shape fails, so a new hint is classified here before it can ship.
  Explanation: after the right button the box begins "Correct."; after the wrong one "Wrong."; for a prime it says
    there are no divisors but 1 and itself; for a composite it names the first three divisors from 2 up (and an
    ellipsis exactly when there are more than three), recomputed by listing the divisors in Python.
  Marking, in Chromium (390x844), every number in the bank: loaded as the only question, the key's button
    answers the number right (the streak dot is a hit, the streak is 1, accuracy 100%) and the other button
    answers it wrong (a miss, streak 0, accuracy 0%). The marking reads the game's own buttons and status; no
    rendered text is compared for the mark.
  Deal: startGame() five times: each deal holds every number in the bank exactly once, with 6 then 7 first.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong key (91 taken as prime), a wrong
answer marked right (the composite button always right), a wrong hint figure (7 x 11 for 91), a wrong worked
divisor (the explanation drops the first divisor) and a wrong class of hint ("Mersenne prime" on 131).

    python scripts/verify-prime-or-composite.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'prime-or-composite'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
DEALS = 5
WORDS = {'single': 1, 'one': 1, 'two': 2, 'three': 3, 'four': 4}


def is_prime(n):
    """Trial division by every integer from 2 to n - 1: slow and obviously right."""
    return n >= 2 and all(n % d for d in range(2, n))


def divisors(n):
    """Every divisor from 2 up to n // 2 (1 and n are left out, as the explanation words it)."""
    return [d for d in range(2, n // 2 + 1) if n % d == 0]


def explanation(n, right):
    lead = '✓ Correct. ' if right else '✗ Wrong. '
    if is_prime(n):
        return lead + '%d is prime — no divisors other than 1 and itself.' % n
    ds = divisors(n)
    return lead + '%d is composite — divisible by %s%s.' % (n, ', '.join(map(str, ds[:3])),
                                                              '…' if len(ds) > 3 else '')


def hint_problem(n, hint):
    """None when the hint's claim about n is true; otherwise what is wrong. A shape not known is a problem."""
    h = hint.strip()
    m = re.fullmatch(r'(\d+) × (\d+)(?: = \?| — it breaks apart)', h)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return None if a * b == n else '%d x %d = %d, not %d' % (a, b, a * b, n)
    m = re.fullmatch(r'Think: (\d+)²', h)
    if m:
        a = int(m.group(1))
        return None if a * a == n else '%d squared is %d, not %d' % (a, a * a, n)
    m = re.fullmatch(r'Think: (\d+) × (\d+)', h)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return None if a * b == n else '%d x %d = %d, not %d' % (a, b, a * b, n)
    m = re.fullmatch(r'Divisible by (\d+)(?: and (\d+))?\??', h)
    if m:
        bad = [int(g) for g in m.groups() if g and n % int(g)]
        return None if not bad else '%d is not divisible by %s' % (n, bad)
    m = re.fullmatch(r'(Single|Two|Three|Four) digits?(, odd)?', h)
    if m:
        want = WORDS[m.group(1).lower()]
        if len(str(n)) != want:
            return '%d has %d digits, not %d' % (n, len(str(n)), want)
        return None if not m.group(2) or n % 2 else '%d is not odd' % n
    if h == 'Even number':
        return None if n % 2 == 0 else '%d is not even' % n
    primes = [k for k in range(2, 10000) if is_prime(k)]
    claims = {
        'Smallest prime': lambda: n == min(primes),
        'Largest two-digit prime?': lambda: n == max(k for k in primes if k < 100),
        'First four-digit prime?': lambda: n == min(k for k in primes if k >= 1000),
        'Largest four-digit prime?': lambda: n == max(k for k in primes if k < 10000),
        'Mersenne prime': lambda: is_prime(n) and any(n == 2 ** p - 1 for p in range(2, 14)),
        'Fermat prime': lambda: is_prime(n) and any(n == 2 ** (2 ** k) + 1 for k in range(0, 5)),
    }
    if h in claims:
        return None if claims[h]() else 'the claim "%s" is false for %d' % (h, n)
    return 'hint shape not known to this verifier: %r (classify it in hint_problem)' % h


def check_bank(fails, bank):
    seen = set()
    for i, q in enumerate(bank, 1):
        n = q.get('n')
        where = 'item %d (n=%r)' % (i, n)
        if not isinstance(n, int) or isinstance(n, bool) or n < 2:
            fails.append('%s: n is not an integer of at least 2' % where)
            continue
        if n in seen:
            fails.append('%s: the number is repeated' % where)
        seen.add(n)
        if not q.get('hint'):
            fails.append('%s: no hint' % where)
            continue
        p = hint_problem(n, q['hint'])
        if p:
            fails.append('%s: hint %r: %s' % (where, q['hint'], p))
    kinds = {is_prime(q['n']) for q in bank if isinstance(q.get('n'), int)}
    if kinds != {True, False}:
        fails.append('the bank does not hold both primes and composites')
    try:
        import sympy
        for q in bank:
            if isinstance(q.get('n'), int) and sympy.isprime(q['n']) != is_prime(q['n']):
                fails.append('n=%d: trial division and SymPy disagree on primality' % q['n'])
    except ImportError:
        pass


MARK_JS = r"""(args) => {
  const [n, hint, clickPrime] = args;
  questions = [{n: n, hint: hint}]; qIdx = 0; score = 0; streak = 0; maxStreak = 0; correct = 0; total = 0;
  gameActive = true;
  buildStreakBar(); nextQuestion();
  document.getElementById(clickPrime ? 'btn-prime' : 'btn-composite').click();
  return {dot: (document.getElementById('sd0') || {}).className || '',
          streak: document.getElementById('sv-streak').textContent,
          acc: document.getElementById('sv-acc').textContent,
          box: document.getElementById('explain-box').textContent};
}"""
DEAL_JS = r"""() => {
  const out = [];
  for (let k = 0; k < %d; k++) { startGame(); out.push(questions.map(q => q.n));
    gameActive = false; MaffsLock.clearTimers(); }
  return [out, QUESTIONS.map(q => q.n)];
}""" % DEALS


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    bank = None
    try:
        with sync_playwright() as pw:
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
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof startGame === "function"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            check_bank(fails, bank)
            for q in bank:
                n, key = q['n'], is_prime(q['n'])
                for press in (True, False):
                    right = press == key
                    got = page.evaluate(MARK_JS, [n, q['hint'], press])
                    where = 'n=%d, %s pressed' % (n, 'PRIME' if press else 'COMPOSITE')
                    if right and not ('hit' in got['dot'] and got['streak'] == '1' and got['acc'] == '100%'):
                        fails.append('%s: the right answer was not marked right (%r)' % (where, got))
                    if not right and not ('miss' in got['dot'] and got['streak'] == '0' and got['acc'] == '0%'):
                        fails.append('%s: the wrong answer was not marked wrong (%r)' % (where, got))
                    if got['box'].removesuffix('Next \u2192') != explanation(n, right):  # a wrong answer adds the Next button
                        fails.append('%s: explanation %r, recomputed %r' % (where, got['box'], explanation(n, right)))
            deals, served = page.evaluate(DEAL_JS)
            for d in deals:
                if sorted(d) != sorted(served) or d[:2] != [6, 7]:
                    fails.append('a deal is not the whole bank once each, 6 then 7 first: %r' % d[:6])
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()
    return bank


PLANTS = [
    ('a wrong key (91 taken as prime)', 'n=91',
     'function isPrime(n){', 'function isPrime(n){if(n===91)return true;'),
    ('a wrong answer marked right (any answer)', 'was not marked wrong',
     'markResult(isPrimeAnswer===isPrime(q.n),false);', 'markResult(true,false);'),
    ('a wrong hint figure (7 × 11 for 91)', 'hint',
     'hint:"7 × 13 = ?"', 'hint:"7 × 11 = ?"'),
    ('a wrong worked divisor (first one dropped)', 'explanation',
     'f.slice(0,3).join', 'f.slice(1,4).join'),
    ('a false hint class (Mersenne on 131)', 'hint',
     '{n:131,  hint:"Three digits"}', '{n:131,  hint:"Mersenne prime"}'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    print('%s: %d numbers recomputed (key, hint, explanation), each marked both ways in Chromium; %d deals'
          % (SLUG, len(bank or []), DEALS))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            play(rep, html.replace(old, new))
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
