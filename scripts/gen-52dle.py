#!/usr/bin/env python3
"""52-dle's clue ladders, found by exhaustive search and written into the page as data (contract 52DLE-REBUILD).

A ladder is 3 to 5 clues about one hidden number, shown one at a time, vague to precise. The rules (the
contract's item 3), applied to every candidate ladder:
  - every clue is true of the number;
  - after the last clue exactly one number in the level's range fits (KS3 1-100, GCSE 1-1,000);
  - after each earlier clue more than one fits, and fewer than before it (the first clue cuts the range);
  - at most ONE digit clue (digit sum or last digit);
  - no factor-count, cube or triangular clue at KS3;
  - no clue names the number: no clue whose own number IS the hidden number ("My last digit is 7" for 7,
    "I am in the 7 times table" for 7, "I have exactly 2 factors" for 2, "I have 1 digit" for 1).
A band is inclusive ("I am between 41 and 50" fits 41 and 50; the start screen says so). A band that starts or
ends at the hidden number is used only for a number with no ladder without one (KS3: 41 and 61, whose only
ladders need "between 41 and 50" or "between 61 and 70"), so the endpoint reading is needed as rarely as it can be.

The clue catalogue (item 2), each as a code the page turns into words:
  D<n> I have N digits        O / E  odd / even          P / p  prime / not prime     S / s  square / not
  M<k> / m<k> in / not in the k times table (KS3 k 3-10, GCSE 3-12)      U<n> My digits add up to N
  L<n> My last digit is N     B<a>-<b> I am between a and b (aligned bands: KS3 10 or 20, GCSE 50, 100 or 200)
  GCSE only: C / c cube / not cube; T / t triangular / not; F<n> I have exactly N factors.

The search: for each number, every set of 3 to 5 of its true, non-naming clues (at most one digit clue). A set's
order is fixed, not searched: clues are shown most vague first, a clue's vagueness being how many numbers in the
range it fits alone (ties by code), so each ladder reads vague to precise. A set is a ladder when that order meets
the rules. Of a number's ladders the shortest length is kept, and of those up to PER_NUMBER, picked by a seeded
shuffle (seed SEED) that prefers sets sharing no clue with one already picked. A number with no ladder of 5 clues
or fewer is left out of the level's pool (the contract: 72 at GCSE, none at KS3).

    python scripts/gen-52dle.py            # write the ladders into games/52dle/index.html
    python scripts/gen-52dle.py --check    # exit 1 if the page's ladders are not this script's output
    python scripts/gen-52dle.py --stats    # counts per level and length; nothing written
"""
import argparse
import itertools
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(os.path.dirname(HERE), 'games', '52dle', 'index.html')
SEED = 52
PER_NUMBER = 3
LEVELS = {'ks3': 100, 'gcse': 1000}
BEGIN = '/* 52DLE-LADDERS: written by scripts/gen-52dle.py; do not edit by hand */'
END = '/* 52DLE-LADDERS-END */'
DIGIT_CLUES = ('U', 'L')


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def n_factors(n):
    return sum(1 for d in range(1, n + 1) if n % d == 0)


def catalogue(level):
    """[(code, a bitmask of the numbers 1..top it is true of (bit n), the numbers it names)] for every clue."""
    top = LEVELS[level]
    rng = range(1, top + 1)
    squares = {k * k for k in range(1, 40)}
    cubes = {k ** 3 for k in range(1, 11)}
    tris = {k * (k + 1) // 2 for k in range(1, 50)}
    out = []

    def add(code, test, names=()):
        mask = 0
        for n in rng:
            if test(n):
                mask |= 1 << n
        out.append((code, mask, frozenset(names)))

    for d in range(1, len(str(top)) + 1):
        add('D%d' % d, lambda n, d=d: len(str(n)) == d, [d])
    add('O', lambda n: n % 2 == 1)
    add('E', lambda n: n % 2 == 0)
    add('P', is_prime)
    add('p', lambda n: not is_prime(n))
    add('S', lambda n: n in squares)
    add('s', lambda n: n not in squares)
    for k in range(3, (10 if level == 'ks3' else 12) + 1):
        add('M%d' % k, lambda n, k=k: n % k == 0, [k])
        add('m%d' % k, lambda n, k=k: n % k != 0, [k])
    for s in range(1, 28):
        add('U%d' % s, lambda n, s=s: sum(map(int, str(n))) == s, [s])
    for d in range(10):
        add('L%d' % d, lambda n, d=d: n % 10 == d, [d])
    for w in ((10, 20) if level == 'ks3' else (50, 100, 200)):
        for a in range(1, top + 1, w):
            b = min(a + w - 1, top)
            add('B%d-%d' % (a, b), lambda n, a=a, b=b: a <= n <= b, [a, b])
    if level == 'gcse':
        add('C', lambda n: n in cubes)
        add('c', lambda n: n not in cubes)
        add('T', lambda n: n in tris)
        add('t', lambda n: n not in tris)
        for f in range(1, 33):
            add('F%d' % f, lambda n, f=f: n_factors(n) == f, [f])
    return [c for c in out if c[1]]


def is_ladder(order, sets, top):
    """Do these clue codes, in this order, meet the narrowing rules? sets: code -> bitmask of the numbers it fits."""
    left = -1
    prev = top
    for i, code in enumerate(order):
        left &= sets[code]
        k = left.bit_count()
        if i == len(order) - 1:
            if k != 1:
                return False
        elif not 1 < k:
            return False
        if k >= prev:
            return False
        prev = k
    return True


def ladders_for(n, cat, top):
    """Every ladder (a tuple of codes, shown in that order) of the shortest length that has one, for n: first with
    no band that starts or ends at n; only where none exists, with such bands allowed (bands are inclusive)."""
    return ladders_where(n, cat, top, False) or ladders_where(n, cat, top, True)


def ladders_where(n, cat, top, band_ends):
    sets = {c: s for c, s, _ in cat}
    true = [c for c, s, names in cat if s >> n & 1 and (n not in names or (band_ends and c[0] == 'B'))]
    true.sort(key=lambda c: (-sets[c].bit_count(), c))           # most vague first; the order a ladder is shown in
    for k in (3, 4, 5):
        found = []
        for combo in itertools.combinations(true, k):
            if sum(1 for c in combo if c[0] in DIGIT_CLUES) > 1:
                continue
            m = -1
            for c in combo:
                m &= sets[c]
            if m != 1 << n:
                continue
            if is_ladder(combo, sets, top):
                found.append(combo)
        if found:
            return found
    return []


def pick(found, rng):
    """Up to PER_NUMBER ladders: a seeded shuffle, then those sharing no clue with one already picked first."""
    found = list(found)
    rng.shuffle(found)
    chosen = []
    for want_disjoint in (True, False):
        for lad in found:
            if len(chosen) >= PER_NUMBER:
                break
            if lad in chosen:
                continue
            if want_disjoint and any(set(lad) & set(c) for c in chosen):
                continue
            chosen.append(lad)
    return chosen


def build():
    """{level: {number: [ladder, ...]}} and {level: [numbers left out]}."""
    rng = random.Random(SEED)
    data, left_out = {}, {}
    for level, top in LEVELS.items():
        cat = catalogue(level)
        data[level], left_out[level] = {}, []
        for n in range(1, top + 1):
            found = ladders_for(n, cat, top)
            if found:
                data[level][n] = pick(found, rng)
            else:
                left_out[level].append(n)
    return data, left_out


def block(data):
    """The page's data block: per level, number -> its ladders, each a space-separated string of codes."""
    lines = [BEGIN, 'var LADDERS = {']
    for li, level in enumerate(LEVELS):
        lines.append('  %s: {' % level)
        nums = sorted(data[level])
        for i, n in enumerate(nums):
            ladders = '|'.join(' '.join(l) for l in data[level][n])
            lines.append('    %d: %s%s' % (n, json.dumps(ladders), ',' if i < len(nums) - 1 else ''))
        lines.append('  }%s' % (',' if li < len(LEVELS) - 1 else ''))
    lines.append('};')
    lines.append(END)
    return '\n'.join(lines)


def current(html):
    i, j = html.find(BEGIN), html.find(END)
    if i < 0 or j < 0:
        return None
    return html[i:j + len(END)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--stats', action='store_true')
    ap.add_argument('--page', default=PAGE)
    a = ap.parse_args()
    data, left_out = build()
    if a.stats or not a.check:
        for level in LEVELS:
            lengths = {}
            for n, ls in data[level].items():
                lengths.setdefault(len(ls[0]), 0)
                lengths[len(ls[0])] += 1
            print('%s: %d numbers with a ladder (by shortest length %s), %d left out%s' % (
                level, len(data[level]), dict(sorted(lengths.items())), len(left_out[level]),
                (': ' + ' '.join(map(str, left_out[level][:30])) + (' ...' if len(left_out[level]) > 30 else ''))
                if left_out[level] else ''))
    if a.stats:
        return 0
    if left_out['ks3']:
        print('STOP: a KS3 number has no ladder: %s' % left_out['ks3'])
        return 1
    html = open(a.page, encoding='utf-8').read()
    have = current(html)
    want = block(data)
    if have is None:
        print('FAIL: %s has no ladder block (%s ... %s)' % (a.page, BEGIN, END))
        return 1
    if a.check:
        if have != want:
            print('FAIL: the page\'s ladders are not gen-52dle.py\'s output: run python scripts/gen-52dle.py')
            return 1
        print('PASS: the page\'s ladders are gen-52dle.py\'s output (%s)' % ', '.join(
            '%s %d numbers' % (l, len(data[l])) for l in LEVELS))
        return 0
    if have != want:
        html = html.replace(have, want)
        with open(a.page, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print('wrote the ladders into %s (%d bytes)' % (a.page, len(html.encode('utf-8'))))
    else:
        print('the page\'s ladders are already current')
    return 0


if __name__ == '__main__':
    sys.exit(main())
