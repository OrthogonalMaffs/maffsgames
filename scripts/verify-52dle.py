#!/usr/bin/env python3
# ci-line: 52-dle (every clue ladder recomputed and narrowing to one number, the page's ladders the generator's output, daily, run, scoring, broken clues and exact marking played in Chromium) |
"""52-dle: every clue is true, every ladder narrows to one number, and the page plays the game the contract describes.

The game (contract 52DLE-REBUILD, 19-20 Nov 2026): a hidden number, KS3 (key ks3, "Foundation") 1-100 or GCSE 1-1000.
Clues are shown one at a time from a ladder of 3-5, written into the page as codes by scripts/gen-52dle.py. A daily
of one number per level per day (picked from the UK date and the level) and a run of five different numbers.

Checks, each recomputed here and never by the page's own code:
  generator  the page's ladder block is gen-52dle.py's output, and the ladders the page reads are the same.
  ladders    every ladder of every number at both levels, against the contract's item 3: 3-5 clues, every clue
             true of the number, more than one number left after each earlier clue and fewer than before, exactly
             one after the last; at most one digit clue (digit sum or last digit); no factor-count, cube or
             triangular clue at KS3; no clue that names the number (a band that starts or ends at it only for the
             numbers pinned in BAND_END, which have no ladder without one); every code one of the level's catalogue
             (times tables 3-10 or 3-12, aligned bands of 10 or 20, or 50, 100 or 200). Every KS3 number 1-100 has a
             ladder; the GCSE pool is the 928 the contract names.
  wording    every code the page uses, worded by the page, equals item 2's words (WORDS below).
  daily      the daily on a fixed date is the same over three page loads (the page's clock fixed to that instant)
             and differs from the next day's; 60 days give at least 40 different numbers; the UK date turns over at
             midnight in Europe/London (BST and GMT).
  run        200 runs (seeded): five different numbers each, every one from the pool with one of its ladders.
  scoring    worth(clues, wrong guesses, found): 100 - 20 a clue after the first - 10 a wrong guess, at least 10 if
             found, 0 if not; and a run played through the page totals what those give.
  closeness  the five bands are shares of the range: the same share of 100 and of 1000 (a fixed-size band fails).
  feedback   wrong guesses typed into the box: Higher or Lower, and exactly the revealed clues the guess breaks,
             each in the words given here.
  marking    exact match by MaffsAnswer.exact on the raw text: "23.9" never wins 23, "23" and "23.0" do; the box is a
             text box and "1,000" is never marked.
  facts      "Did you know?" for exactly the contract's 17 numbers, each fact recomputed (FACTS), and shown after
             the number is found or missed.
  play       a whole run and a whole daily played in Chromium: the events (one question_answered per number with
             question_id 52dle-<level>-<n>, attempts and correct; level and mode on every event), one submitScore
             for the run on its level's board and none for the daily; the daily's result is shown again on return.
Plants (each must FAIL by its named check): a false clue; a ladder leaving two numbers; two digit clues; a
fixed-size warmth band; a run with a repeated number.

    python scripts/verify-52dle.py [--no-selftest] [--against FILE]
"""
import argparse
import importlib.util
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = '52dle'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
TOP = {'ks3': 100, 'gcse': 1000}
GCSE_POOL = 928
# Numbers whose only ladders use a band starting or ending at the number itself (bands are inclusive; the start screen
# says so). Pinned: a new one fails here until it is reviewed.
BAND_END = {'ks3': {41, 61}, 'gcse': {201, 251, 401, 501, 601, 751, 801, 951}}

_spec = importlib.util.spec_from_file_location('gen52', os.path.join(HERE, 'gen-52dle.py'))
GEN = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(GEN)


# ---------- the clues, recomputed here ----------
def digit_sum(n):
    return sum(int(d) for d in str(n))


def is_square(n):
    return sp.integer_nthroot(n, 2)[1]


def is_cube(n):
    return sp.integer_nthroot(n, 3)[1]


def is_tri(n):
    return is_square(8 * n + 1)


def code_parts(code):
    m = re.fullmatch(r'([A-Za-z])(\d*)(?:-(\d+))?', code)
    if not m:
        return None
    return m.group(1), (int(m.group(2)) if m.group(2) else None), (int(m.group(3)) if m.group(3) else None)


def true_of(code, n):
    t, a, b = code_parts(code)
    return {
        'D': lambda: len(str(n)) == a, 'O': lambda: n % 2 == 1, 'E': lambda: n % 2 == 0,
        'P': lambda: bool(sp.isprime(n)), 'p': lambda: not sp.isprime(n),
        'S': lambda: is_square(n), 's': lambda: not is_square(n),
        'M': lambda: n % a == 0, 'm': lambda: n % a != 0,
        'U': lambda: digit_sum(n) == a, 'L': lambda: n % 10 == a,
        'B': lambda: a <= n <= b,
        'C': lambda: is_cube(n), 'c': lambda: not is_cube(n),
        'T': lambda: is_tri(n), 't': lambda: not is_tri(n),
        'F': lambda: int(sp.divisor_count(n)) == a,
    }[t]()


def valid_code(code, level):
    """Is the code one of the level's catalogue (item 2)?"""
    p = code_parts(code)
    if not p:
        return False
    t, a, b = p
    top = TOP[level]
    if t in 'OEPpSs':
        return a is None and b is None
    if t in 'CcTtF' and level == 'ks3':
        return False
    if t in 'CcTt':
        return a is None and b is None
    if t == 'F':
        return a is not None and a >= 1 and b is None
    if t == 'D':
        return a is not None and 1 <= a <= len(str(top)) and b is None
    if t in 'Mm':
        return a is not None and 3 <= a <= (10 if level == 'ks3' else 12) and b is None
    if t == 'U':
        return a is not None and a >= 1 and b is None
    if t == 'L':
        return a is not None and 0 <= a <= 9 and b is None
    if t == 'B':
        if a is None or b is None:
            return False
        for w in ((10, 20) if level == 'ks3' else (50, 100, 200)):
            if (a - 1) % w == 0 and b == min(a + w - 1, top):
                return True
        return False
    return False


def names(code, n):
    """The numbers a clue states: its N, its k, or a band's two ends."""
    t, a, b = code_parts(code)
    return {x for x in (a, b) if x is not None}


def check_ladder(level, n, codes):
    """[fault] for one ladder of n at level, against item 3."""
    top = TOP[level]
    out = []
    if not 3 <= len(codes) <= 5:
        out.append('%d clues (3 to 5)' % len(codes))
    for c in codes:
        if not valid_code(c, level):
            out.append('"%s" is not in the %s catalogue' % (c, level))
    if out:
        return out
    for c in codes:
        if not true_of(c, n):
            out.append('false clue: "%s" is not true of %d' % (WORDS(c), n))
        if n in names(c, n) and not (c[0] == 'B' and n in BAND_END[level]):
            out.append('names the number: "%s"' % WORDS(c))
    digit = [c for c in codes if c[0] in 'UL']
    if len(digit) > 1:
        out.append('two digit clues: %s' % ', '.join('"%s"' % WORDS(c) for c in digit))
    left = set(range(1, top + 1))
    for i, c in enumerate(codes):
        before = len(left)
        left = {m for m in left if true_of(c, m)}
        if i == len(codes) - 1:
            if len(left) != 1:
                out.append('leaves %d numbers after the last clue (%s)' % (len(left), ', '.join(map(str, sorted(left)[:6]))))
        elif len(left) <= 1:
            out.append('only %d left after clue %d of %d' % (len(left), i + 1, len(codes)))
        if len(left) >= before:
            out.append('clue %d ("%s") narrows nothing (%d before, %d after)' % (i + 1, WORDS(c), before, len(left)))
    return out


# ---------- item 2's wording, written here ----------
def WORDS(code):
    t, a, b = code_parts(code)
    return {
        'D': 'I have %s digit%s' % (a, '' if a == 1 else 's'), 'O': 'I am odd', 'E': 'I am even',
        'P': 'I am a prime number', 'p': 'I am not a prime number',
        'S': 'I am a square number', 's': 'I am not a square number',
        'M': 'I am in the %s times table' % a, 'm': 'I am not in the %s times table' % a,
        'U': 'My digits add up to %s' % a, 'L': 'My last digit is %s' % a,
        'B': 'I am between %s and %s' % (a, b),
        'C': 'I am a cube number', 'c': 'I am not a cube number',
        'T': 'I am a triangular number', 't': 'I am not a triangular number',
        'F': 'I have exactly %s factors' % a,
    }[t]


def BROKEN(code, g):
    """Why guess g breaks a clue it does not fit, in the page's words."""
    t, a, b = code_parts(code)
    return {
        'D': '%d does not have %s digit%s' % (g, a, '' if a == 1 else 's'),
        'O': '%d is not odd' % g, 'E': '%d is not even' % g,
        'P': '%d is not a prime number' % g, 'p': '%d is a prime number' % g,
        'S': '%d is not a square number' % g, 's': '%d is a square number' % g,
        'M': '%d is not in the %s times table' % (g, a), 'm': '%d is in the %s times table' % (g, a),
        'U': '%d’s digits add up to %d, not %s' % (g, digit_sum(g), a),
        'L': '%d’s last digit is %d, not %s' % (g, g % 10, a),
        'B': '%d is not between %s and %s' % (g, a, b),
        'C': '%d is not a cube number' % g, 'c': '%d is a cube number' % g,
        'T': '%d is not a triangular number' % g, 't': '%d is a triangular number' % g,
        'F': '%d has %d factors, not %s' % (g, int(sp.divisor_count(g)), a),
    }[t]


def worth(clues, wrong, found):
    return max(10, 100 - 20 * (clues - 1) - 10 * wrong) if found else 0


# ---------- Did you know? ----------
def fib(n):
    return sp.fibonacci(n)


def emirp(n):
    return sp.isprime(n) and sp.isprime(int(str(n)[::-1]))


def perfect(n):
    return sum(sp.divisors(n)) - n == n


def shared_birthday(n):
    q = sp.Integer(1)
    for k in range(n):
        q *= sp.Rational(365 - k, 365)
    return 1 - q


# The contract's 17 numbers; each fact's words pinned with what they claim of the number.
FACTS = {
    7: [('The 4th prime', lambda a: a == sp.prime(4)), ('days in a week', lambda a: a == 7)],
    13: [('I am the 6th prime', lambda a: a == sp.prime(6)), ('7th Fibonacci', lambda a: a == fib(7))],
    23: [('9th prime', lambda a: a == sp.prime(9)),
         ('smallest number of people needed for a better than even chance that two of them share a birthday',
          lambda a: a == next(n for n in range(2, 366) if shared_birthday(n) > sp.Rational(1, 2)))],
    28: [('second perfect number', lambda a: a == [n for n in range(2, 500) if perfect(n)][1]),
         ('My proper divisors (1,2,4,7,14) sum to me', lambda a: sp.divisors(a)[:-1] == [1, 2, 4, 7, 14] and sum(sp.divisors(a)[:-1]) == a)],
    31: [('11th prime', lambda a: a == sp.prime(11)), ('Reverse me and you get 13, also prime', lambda a: str(a)[::-1] == '13' and emirp(a))],
    37: [('permutable prime', lambda a: sp.isprime(a) and sp.isprime(int(str(a)[::-1]))),
         ('37, 73', lambda a: {a, int(str(a)[::-1])} == {37, 73})],
    42: [('6 × 7', lambda a: a == 6 * 7), ('Ten less than 52', lambda a: a == 52 - 10)],
    52: [('number of cards in a standard deck', lambda a: a == 52), ('52! ≈ 8 × 10⁶⁷', lambda a: 8e67 <= float(sp.factorial(a)) < 9e67)],
    53: [('16th prime', lambda a: a == sp.prime(16)), ('nearest prime greater than 52', lambda a: a == sp.nextprime(52))],
    64: [('8 squared', lambda a: a == 8 ** 2), ('4 cubed', lambda a: a == 4 ** 3),
         ('both a perfect square and a perfect cube below 100', lambda a: [n for n in range(2, 100) if sp.integer_nthroot(n, 6)[1]] == [a])],
    89: [('11th Fibonacci', lambda a: a == fib(11)), ('My reverse, 98, is NOT prime', lambda a: not sp.isprime(98) and str(a)[::-1] == '98'),
         ('largest two-digit Fibonacci', lambda a: a == max(f for f in map(fib, range(1, 20)) if 10 <= f < 100))],
    97: [('largest two-digit prime', lambda a: a == sp.prevprime(100)), ('79, is also prime', lambda a: emirp(a) and str(a)[::-1] == '79')],
    100: [('10 squared', lambda a: a == 10 ** 2)],
    144: [('12 squared', lambda a: a == 12 ** 2), ('12th Fibonacci', lambda a: a == fib(12))],
    271: [('first three digits of e', lambda a: a == int(str(sp.N(sp.E, 10)).replace('.', '')[:3]))],
    314: [('first three significant digits of π', lambda a: a == int(str(sp.N(sp.pi, 10)).replace('.', '')[:3]))],
    521: [('2⁵²¹ − 1 is a Mersenne prime', lambda a: a in (2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521)),
          ('I am the exponent', lambda a: a == 521)],
}


def check_facts(fails, facts):
    got = sorted(int(k) for k in facts)
    if got != sorted(FACTS):
        fails.append('facts: "Did you know?" for %s, the contract names %s' % (got, sorted(FACTS)))
    for n, claims in FACTS.items():
        text = facts.get(str(n), '')
        for phrase, claim in claims:
            if phrase not in text:
                fails.append('facts: %d no longer says "%s" (review FACTS)' % (n, phrase))
            elif not claim(n):
                fails.append('facts: %d: "%s" is false' % (n, phrase))
        if '^' in text:
            fails.append('facts: %d writes a power with a caret' % n)


# ---------- static: the page's ladders against the generator and item 3 ----------
def page_ladders(html):
    block = GEN.current(html)
    if block is None:
        return None
    out = {}
    for level in ('ks3', 'gcse'):
        m = re.search(r'\n  %s: \{\n(.*?)\n  \}' % level, block, re.S)
        out[level] = {}
        for line in (m.group(1).split('\n') if m else []):
            mm = re.fullmatch(r'\s*(\d+): "([^"]*)",?', line)
            if mm:
                out[level][int(mm.group(1))] = [l.split(' ') for l in mm.group(2).split('|')]
    return out


def check_static(fails, html):
    data, _ = GEN.build()
    want = GEN.block(data)
    have = GEN.current(html)
    if have != want:
        fails.append('generator: the page\'s ladder block is not gen-52dle.py\'s output (run python scripts/gen-52dle.py)')
    lad = page_ladders(html)
    if lad is None:
        fails.append('ladders: the page has no ladder block')
        return None
    if sorted(lad['ks3']) != list(range(1, 101)):
        fails.append('ladders: KS3 numbers without a ladder: %s' % sorted(set(range(1, 101)) - set(lad['ks3'])))
    if len(lad['gcse']) != GCSE_POOL:
        fails.append('ladders: the GCSE pool has %d numbers, not %d' % (len(lad['gcse']), GCSE_POOL))
    n_lad = 0
    for level in ('ks3', 'gcse'):
        for n, ls in sorted(lad[level].items()):
            if not 1 <= n <= TOP[level]:
                fails.append('ladders: %s %d is outside 1-%d' % (level, n, TOP[level]))
            if len({tuple(l) for l in ls}) != len(ls):
                fails.append('ladders: %s %d repeats a ladder' % (level, n))
            for l in ls:
                n_lad += 1
                for f in check_ladder(level, n, l):
                    fails.append('ladders: %s %d [%s]: %s' % (level, n, ' '.join(l), f))
    return lad, n_lad


# ---------- Chromium ----------
CLOCK_INIT = r"""(() => {
  const FIX = %s; if (FIX === null) return;
  const RealDate = Date;
  class FixedDate extends RealDate { constructor(...a) { if (a.length) super(...a); else super(FIX); }
    static now() { return FIX; } }
  window.Date = FixedDate;
})();"""

RECORD_JS = r"""() => {
  window.__ev = []; window.__subs = [];
  window.mfg = function (e, p) { window.__ev.push([e, JSON.parse(JSON.stringify(p || {}))]); };
  if (window.MaffsLeaderboard) MaffsLeaderboard.submitScore = function (slug, lv, sc, n) { window.__subs.push([slug, lv, sc, n]); return Promise.resolve(); };
  return true;
}"""


def new_page(pw_ctx_maker, base, html, fixed_ms=None):
    ctx = pw_ctx_maker()
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script(CLOCK_INIT % ('null' if fixed_ms is None else str(fixed_ms)))
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    return ctx, page, errors


def load(page, base, query=''):
    page.goto(base + '/games/%s/%s' % (SLUG, query), wait_until='load', timeout=20000)
    page.wait_for_function('!!window.D52', timeout=15000)
    page.evaluate(RECORD_JS)


def browser_checks(fails, html, lad):
    from playwright.sync_api import sync_playwright
    import datetime
    proc, base = bc.start_stub_server()
    played = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            mk = lambda: browser.new_context(viewport={'width': 390, 'height': 844})
            ctx, page, errors = new_page(mk, base, html)
            load(page, base)

            # generator: the ladders the page reads
            got = page.evaluate('() => D52.ladders()')
            for level in ('ks3', 'gcse'):
                read = {int(k): [l.split(' ') for l in v.split('|')] for k, v in got.get(level, {}).items()}
                if lad and read != lad[level]:
                    fails.append('generator: the ladders the page reads at %s differ from its block' % level)

            # wording: every code in use, worded by the page
            codes = sorted({c for level in ('ks3', 'gcse') for ls in (lad or {}).get(level, {}).values() for l in ls for c in l})
            words = page.evaluate('(cs) => cs.map(c => D52.words(c))', codes)
            for c, w in zip(codes, words):
                if w != WORDS(c):
                    fails.append('wording: code %s reads "%s", item 2 gives "%s"' % (c, w, WORDS(c)))

            # closeness: shares of the range
            for d, band in ((0, 1), (1, 1), (2, 2), (5, 2), (6, 3), (15, 3), (16, 4), (40, 4), (41, 5), (99, 5)):
                for level, scale in (('ks3', 1), ('gcse', 10)):
                    b = page.evaluate('([l, d]) => D52.warmth(l, d).band', [level, d * scale])
                    if b != band:
                        fails.append('closeness: %s, %d away is band %s, not %d (a band is a share of the range, not a fixed size)' % (level, d * scale, b, band))

            # scoring
            for clues, wrong, found in ((1, 0, True), (2, 0, True), (3, 2, True), (5, 5, True), (5, 0, True), (1, 5, True), (3, 1, False), (1, 0, False)):
                got_w = page.evaluate('([c, w, f]) => D52.worth(c, w, f)', [clues, wrong, found])
                if got_w != worth(clues, wrong, found):
                    fails.append('scoring: %d clues, %d wrong, %s: %s points, not %d' % (clues, wrong, 'found' if found else 'missed', got_w, worth(clues, wrong, found)))

            # run: five different numbers, seeded
            runs = page.evaluate(r'''(k) => { let s = 7; const r0 = Math.random;
                Math.random = () => { s = (s * 1103515245 + 12345) %% 2147483648; return s / 2147483648; };
                const out = []; for (let i = 0; i < k; i++) out.push([D52.runPick('ks3'), D52.runPick('gcse')]);
                Math.random = r0; return out; }'''.replace('%%', '%'), 200)
            for pair in runs:
                for level, run in zip(('ks3', 'gcse'), pair):
                    ns = [x['n'] for x in run]
                    if len(ns) != 5 or len(set(ns)) != 5:
                        fails.append('run: %s run %s is not five different numbers' % (level, ns))
                        break
                    for x in run:
                        if lad and (x['n'] not in lad[level] or x['ladder'] not in lad[level][x['n']]):
                            fails.append('run: %s %d with a ladder not its own: %s' % (level, x['n'], x['ladder']))
                else:
                    continue
                break

            # daily: a pure function of the date and level
            day0 = datetime.date(2026, 11, 20)
            dates = [(day0 + datetime.timedelta(days=k)).isoformat() for k in range(60)]
            picks = page.evaluate('(ds) => ds.map(d => [D52.dailyPick(d, "ks3"), D52.dailyPick(d, "gcse")])', dates)
            for level, i in (('ks3', 0), ('gcse', 1)):
                ns = [p[i]['n'] for p in picks]
                if ns[0] == ns[1]:
                    fails.append('daily: %s gives %d on both %s and %s' % (level, ns[0], dates[0], dates[1]))
                if len(set(ns)) < 40:
                    fails.append('daily: %s gives only %d different numbers in 60 days' % (level, len(set(ns))))
                for p in picks:
                    if lad and p[i]['ladder'] not in lad[level].get(p[i]['n'], []):
                        fails.append('daily: %s %d with a ladder not its own' % (level, p[i]['n']))
                        break
            for iso, want in (('2026-03-28T23:30:00Z', '2026-03-28'), ('2026-03-29T23:30:00Z', '2026-03-30'),
                              ('2026-10-24T23:30:00Z', '2026-10-25'), ('2026-10-25T23:30:00Z', '2026-10-25'),
                              ('2026-11-20T23:59:00Z', '2026-11-20'), ('2026-06-30T23:00:00Z', '2026-07-01')):
                got_d = page.evaluate('(s) => D52.ukDate(s)', iso)
                if got_d != want:
                    fails.append('daily: %s is %s in the UK, the page says %s' % (iso, want, got_d))

            # facts
            check_facts(fails, page.evaluate('() => D52.FACTS'))

            # marking and feedback, in the page: 23 at KS3 (its first ladder), every clue shown
            def preview(level, n, k=0):
                page.evaluate('([l, n, k]) => D52.ui.preview(l, n, k)', [level, n, k])
                page.wait_for_function('D52.ui.state() === "asking"', timeout=5000)

            def guess(raw):
                page.evaluate('(r) => D52.ui.guess(r)', raw)
                page.wait_for_timeout(20)

            preview('ks3', 23)
            if page.get_attribute('#guess', 'type') != 'text':
                fails.append('marking: the guess box is type="%s", not a text box' % page.get_attribute('#guess', 'type'))
            for raw in ('23.9', '1,000', '', '0', '101', 'abc'):
                guess(raw)
                if page.evaluate('() => D52.ui.state()') != 'asking' or page.evaluate('() => document.querySelectorAll("#guesses .guess").length'):
                    fails.append('marking: typing %r for 23 was marked' % raw)
            for raw in ('23', '23.0', ' 23 '):
                preview('ks3', 23)
                guess(raw)
                if page.evaluate('() => D52.ui.state()') != 'done':
                    fails.append('marking: typing %r for 23 did not find it' % raw)
            # broken clues: sample wrong guesses against every revealed clue
            for level, n, sample in (('ks3', 23, (40, 29, 5, 99, 22)), ('ks3', 64, (49, 60, 81, 8)),
                                     ('gcse', 271, (272, 300, 199, 1000, 7)), ('gcse', 144, (121, 150, 400))):
                for k in range(len(lad[level][n]) if lad else 1):
                    preview(level, n, k)
                    ladder = page.evaluate('() => D52.ui.ladder()')
                    for _ in range(len(ladder) - 1):
                        page.evaluate('() => D52.ui.clue()')
                    if page.evaluate('() => D52.ui.shown()') != len(ladder):
                        fails.append('feedback: Next clue did not reveal all %d clues of %d' % (len(ladder), n))
                    for g in sample[:5]:
                        if g == n:
                            continue
                        guess(str(g))
                        if page.evaluate('() => D52.ui.state()') != 'asking':
                            break
                        got_b = page.evaluate('() => [...document.querySelectorAll("#guesses .guess:first-child .g-broken li")].map(e => e.textContent)')
                        want_b = [BROKEN(c, g) for c in ladder if not true_of(c, g)]
                        if got_b != want_b:
                            fails.append('feedback: %s %d [%s], guess %d: shows %s, the clues it breaks are %s' % (level, n, ' '.join(ladder), g, got_b, want_b))
                        d = page.evaluate('() => document.querySelector("#guesses .guess:first-child .g-dir").dataset.dir')
                        if d != ('higher' if g < n else 'lower'):
                            fails.append('feedback: %s %d, guess %d says %s' % (level, n, g, d))
            # a fact after a number found, and none after one without
            preview('ks3', 7)
            guess('7')
            if not page.evaluate('() => !!document.querySelector("#feedback [data-fact=\'7\']")'):
                fails.append('facts: no "Did you know?" after 7 is found')
            preview('ks3', 8)
            page.evaluate('() => D52.ui.answer(false)')
            if page.evaluate('() => D52.ui.state()') != 'missed' or page.evaluate('() => !!document.querySelector("#feedback .dyk")'):
                fails.append('facts: 8 missed: state %s, a fact shown' % page.evaluate('() => D52.ui.state()'))
            if not page.evaluate('() => !!document.querySelector("#feedback .maffs-next")'):
                fails.append('pause: a missed number does not wait on MaffsNext')
            ctx.close()

            # a whole run played: found, found with a clue and a wrong guess, missed, found, found
            for level in ('ks3', 'gcse'):
                ctx, page, errs = new_page(mk, base, html)
                load(page, base, '?level=%s' % level)
                page.evaluate('() => D52.ui.start("run")')
                items = page.evaluate('() => D52.ui.items()')
                expect = 0
                for k, it in enumerate(items):
                    page.wait_for_function('D52.ui.state() === "asking"', timeout=5000)
                    if k == 1:
                        page.evaluate('() => D52.ui.clue()')
                        wrong = it['n'] + 1 if it['n'] < TOP[level] else it['n'] - 1
                        page.evaluate('(r) => D52.ui.guess(r)', str(wrong))
                        page.evaluate('() => D52.ui.answer(true)')
                        expect += worth(2, 1, True)
                    elif k == 2:
                        page.evaluate('() => D52.ui.answer(false)')
                    else:
                        page.evaluate('() => D52.ui.answer(true)')
                        expect += worth(1, 0, True)
                    page.wait_for_timeout(30)
                    page.evaluate('() => D52.ui.next()')
                page.wait_for_function('D52.ui.state() === "over"', timeout=5000)
                total = page.evaluate('() => D52.ui.total()')
                if total != expect:
                    fails.append('play: %s run scored %s, the rule gives %d' % (level, total, expect))
                if page.inner_text('#resScore').strip() != str(expect):
                    fails.append('play: %s run results show %s' % (level, page.inner_text('#resScore')))
                evs = page.evaluate('() => window.__ev')
                subs = page.evaluate('() => window.__subs')
                qa = [p for e, p in evs if e == 'question_answered']
                if [p.get('question_index') for p in qa] != [1, 2, 3, 4, 5]:
                    fails.append('play: %s run question_index %s' % (level, [p.get('question_index') for p in qa]))
                for p, it, k in zip(qa, items, range(5)):
                    want = {'question_id': '52dle-%s-%d' % (level, it['n']), 'correct': k != 2,
                            'attempts': 2 if k == 1 else (6 if k == 2 else 1), 'level': level, 'mode': 'run', 'game_slug': SLUG}
                    bad = {kk: (p.get(kk), v) for kk, v in want.items() if p.get(kk) != v}
                    if bad:
                        fails.append('play: %s run question_answered %d: %s' % (level, k + 1, bad))
                for e, p in evs:
                    if p.get('level') != level or (e in ('game_started', 'game_completed', 'question_answered') and p.get('mode') != 'run'):
                        fails.append('play: %s run event %s carries level %s, mode %s' % (level, e, p.get('level'), p.get('mode')))
                gc = [p for e, p in evs if e == 'game_completed']
                if len(gc) != 1 or gc[0].get('score') != expect or gc[0].get('questions_correct') != 4:
                    fails.append('play: %s run game_completed %s' % (level, gc))
                if subs != [[SLUG, level, expect, 5]]:
                    fails.append('play: %s run submitted %s, not one score to the %s board' % (level, subs, level))
                played += 1
                errors += errs
                ctx.close()

            # a whole daily, its clock fixed: the same number over three loads, then its result shown again
            fixed = 1795694400000   # 2026-11-26T12:00:00Z
            seen = []
            for k in range(3):
                ctx, page, errs = new_page(mk, base, html, fixed)
                load(page, base, '?level=gcse')
                page.evaluate('() => D52.ui.start("daily")')
                seen.append(page.evaluate('() => [D52.ui.number(), D52.ui.ladder()]'))
                errors += errs
                if k < 2:
                    ctx.close()
            if any(s != seen[0] for s in seen):
                fails.append('daily: three loads on one date gave %s' % seen)
            want_pick = page.evaluate('() => D52.dailyPick("2026-11-26", "gcse")')
            if seen[0] != [want_pick['n'], want_pick['ladder']]:
                fails.append('daily: the daily played is %s, the day\'s pick is %s' % (seen[0], want_pick))
            page.evaluate('() => D52.ui.clue()')
            page.evaluate('() => D52.ui.answer(true)')
            page.wait_for_timeout(30)
            page.evaluate('() => D52.ui.next()')
            page.wait_for_function('D52.ui.state() === "over"', timeout=5000)
            evs = page.evaluate('() => window.__ev')
            subs = page.evaluate('() => window.__subs')
            if subs:
                fails.append('daily: submitted %s to a leaderboard (the daily has none)' % subs)
            qa = [p for e, p in evs if e == 'question_answered']
            if len(qa) != 1 or qa[0].get('mode') != 'daily' or qa[0].get('level') != 'gcse' or qa[0].get('question_id') != '52dle-gcse-%d' % seen[0][0]:
                fails.append('daily: question_answered %s' % qa)
            if page.inner_text('#resScore').strip() != str(worth(2, 0, True)):
                fails.append('daily: the result shows %s, not %d' % (page.inner_text('#resScore'), worth(2, 0, True)))
            if not page.inner_text('#shareGrid').strip():
                fails.append('daily: no share grid')
            # back to the menu, and the daily again: the result, not a new game
            page.evaluate('() => document.getElementById("menuBtn").click()')
            n_started = len([e for e, _ in page.evaluate('() => window.__ev') if e == 'game_started'])
            page.evaluate('() => D52.ui.start("daily")')
            if page.evaluate('() => D52.ui.state()') != 'over' or len([e for e, _ in page.evaluate('() => window.__ev') if e == 'game_started']) != n_started:
                fails.append('daily: played again on the same day, it started a new game instead of showing the result')
            played += 1
            ctx.close()
            browser.close()
            errors = [e for e in errors if 'firebase' not in e.lower()]
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()
    return played


def run_all(html, lad_override=None):
    fails = []
    res = check_static(fails, html)
    lad, n_lad = res if res else (None, 0)
    played = browser_checks(fails, html, lad)
    return fails, lad, n_lad, played


# ---------- plants ----------
def first_ladder_line(html, level, n):
    block = GEN.current(html)
    m = re.search(r'\n  %s: \{\n(.*?)\n  \}' % level, block, re.S)
    for line in m.group(1).split('\n'):
        if re.match(r'\s*%d: "' % n, line):
            return line
    return None


def plant_ladder(html, level, n, new_first):
    """The page with n's first ladder at level replaced by new_first (a list of codes)."""
    line = first_ladder_line(html, level, n)
    head, ladders = re.match(r'(\s*\d+: ")([^"]*)', line).groups()
    rest = ladders.split('|')[1:]
    new = line.replace(head + ladders, head + '|'.join([' '.join(new_first)] + rest))
    return html.replace(line, new)


def two_left(level, n, ladder):
    """n's ladder with its last clue swapped for another true clue that leaves exactly two numbers."""
    top = TOP[level]
    for code, mask, nm in GEN.catalogue(level):
        cand = ladder[:-1] + [code]
        if code in ladder or not true_of(code, n):
            continue
        left = set(range(1, top + 1))
        for c in cand:
            left = {m for m in left if true_of(c, m)}
        if len(left) == 2:
            return cand
    return None


def plants(html):
    lad = page_ladders(html)
    l23 = lad['ks3'][23][0]
    false = ['E'] + l23[1:] if l23[0] != 'E' else ['O'] + l23[1:]
    out = [
        ('ladders: ks3 23', 'a false clue (even for 23)', plant_ladder(html, 'ks3', 23, false), 'false clue'),
        ('ladders: ks3 23', 'a ladder leaving two numbers', plant_ladder(html, 'ks3', 23, two_left('ks3', 23, l23)), 'leaves 2 numbers'),
    ]
    # two digit clues: a ladder with a digit clue gains the other one, true of n, before its last clue
    for n, ls in sorted(lad['ks3'].items()):
        l = ls[0]
        dig = [c for c in l if c[0] in 'UL']
        if len(dig) == 1 and len(l) < 5:
            other = ('L%d' % (n % 10)) if dig[0][0] == 'U' else ('U%d' % digit_sum(n))
            if other not in l and n not in names(other, n):
                out.append(('ladders: ks3 %d' % n, 'two digit clues', plant_ladder(html, 'ks3', n, l[:-1] + [other, l[-1]]), 'two digit clues'))
                break
    out.append(('closeness: gcse', 'a fixed-size warmth band', html.replace('WARMTH[i][0] * top', 'WARMTH[i][0] * 100'), 'closeness'))
    out.append(('run: ', 'a run with a repeated number', html.replace('out.push({ n: p[i], ladder', 'out.push({ n: p[0], ladder')
                .replace('var ls = laddersOf(lv, p[i]);', 'var ls = laddersOf(lv, p[0]);'), 'five different'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, lad, n_lad, played = run_all(html)
    print('%s: %d ladders for %d KS3 and %d GCSE numbers recomputed against item 3; wording, closeness, scoring, 400 runs, '
          '120 dailies, marking and broken clues checked in Chromium; %d whole games played'
          % (SLUG, n_lad, len((lad or {}).get('ks3', {})), len((lad or {}).get('gcse', {})), played))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, bad, word in plants(html):
            if bad == html:
                print('  self-test %-34s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep, _, _, _ = run_all(bad)
            hit = [f for f in rep if f.startswith(tag) and word in f]
            ok = ok and bool(hit)
            print('  self-test %-34s %s' % (what, ('caught: ' + hit[0][:120]) if hit else '*** MISSED *** ' + '; '.join(rep[:2])[:200]))
    for f in fails[:60]:
        print('FAIL  ' + f)
    if len(fails) > 60:
        print('FAIL  ... and %d more' % (len(fails) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
