#!/usr/bin/env python3
# ci-line: How Many Parts?, part 1 (pools, keys, every stage's own errors and options, every question's chocolate bar recomputed and read back from the page, the palette, sessions, both levels played at 320, 390 and 1280px) | --part 1
# ci-line: How Many Parts?, part 2 (every wrong-answer screen at 320x568, normal and Aa: the reason and Next above the fold; stage 1's bar, answer box and keypad in the window together) | --part 2
# ci-line: How Many Parts?, part 3 (every wrong-answer screen at 375x667 and 390x844, normal and Aa: the reason and Next above the fold) | --part 3
# ci-line: How Many Parts?, part 4 (every wrong-answer screen at 1280x800, normal and Aa: the reason and Next above the fold) | --part 4
# ci-line: How Many Parts?, part 5 (fault-injection self-test: seven planted faults in the engine, the bar and the palette, each caught) | --part 5
# ci-line: How Many Parts?, part 6 (fault-injection self-test: five planted faults in play and the stage 1 fit, each caught) | --part 6
# ci-deps: games/how-many-parts/
"""Independent verification for How Many Parts? (games/how-many-parts/), built 20 Oct 2026 (contract HOW-MANY-PARTS)
(verbatim in docs/history/contracts/) and rebuilt for its redesign, 21 Oct 2026 (contract HMP-CHOCOLATE and Jon's
rulings of that day, verbatim in docs/handover/contracts/2026-10-21-hmp-chocolate.md). SR-30: checked from its first PR.

WHY THIS READS THE LIVE PAGE
-------------------------------------------------------------------------------
The game keeps every decision a student sees (the pools, every key, every option and the error behind it, the
chocolate-bar model, the feedback lines) on window.HMP as plain functions, and its UI calls them through HMP. This
script loads the page under Playwright, drives THOSE functions, draws every question through the game's own screens,
and recomputes everything here, in Python, with exact fractions, from definitions written out below from the
contracts' words, never read back from the page.

WHAT IT ASSERTS
-------------------------------------------------------------------------------
  Pools      every stage's pool is exactly the questions this script enumerates from the stated parameters, less
             those the 20 Oct catalogue of errors filters out (one equal to the key, or, in stages 1-3, fewer than
             three with distinct values). HMP-CHOCOLATE keeps the pools as they were: that catalogue is the filter's
             only use. Each stage keeps at least 40.
  Lists      each stage's own errors (Jon, 21 Oct 2026), written out below, are the ONLY errors offered or named:
               1 (typed) the tops and the bottoms added or taken away (never a zero bottom); the other operation;
                 the tops taken away and the bottoms added; the count of parts given as a whole number
               2 the tops and the bottoms; the tops and the bigger bottom kept; a bottom changed but not its top; the
                 other operation (the taking-away versions too, never a zero or negative bottom)
               3 the tops and the bottoms; the bottoms multiplied and the tops added as they were (adding only); the
                 bottoms changed but not the tops; the other operation
               4 (typed) added instead of multiplying; the tops multiplied but a bottom kept; the top and the bottom
                 both multiplied by the whole number
               5 (typed) multiplied without turning the second fraction over; the first fraction turned over; the
                 whole number divided by the bottom
               6 (typed) the wholes and the parts multiplied separately; the smaller part taken from the larger; a
                 mixed number converted wrongly (whole + top instead of whole x bottom + top)
             No listed error equals its question's key, except the two stage 6 questions awaiting Jon's ruling
             (KNOWN_COLLISIONS, printed on every run).
  Questions  every pool entry over SEEDS seeds. Stages 2-3: the key in its simplest form; every other option a listed
             error of its stage, its value recomputed here, in its simplest form, named by the first listed error with
             that value, none equal in value to the key or to another option; four options, or three where fewer than
             three listed errors apply (SR-4 exception, Jon, 21 Oct 2026), counted per stage. Stages 1 and 4-6 typed:
             the key, its form (simplest, or a mixed number in stage 6), the boxes' key parts, the question's numbers.
             Every feedback line for a listed error starts from that error's value; the correct sum ends on the key in
             the asked form.
  The bar    every question's model recomputed here from its numbers (contract HMP-CHOCOLATE): adding, one bar of the
             common denominator's squares, the first number's then the second's (striped), side by side; taking away,
             the first number's squares with the taken ones eaten; different denominators, the pieces before cutting
             as grooves and one caption line; a fraction times a whole number, that many bars; a fraction times a
             fraction, one slab whose overlap is the product; "how many quarters in 3", the pieces outlined along 3
             bars; a fraction divided by a fraction, lots outlined along the bar; mixed numbers, whole bars plus a
             part bar. Then every question screen and every wrong-answer screen is drawn by the game and its SVG read
             back square by square: exactly one figure on the screen, every square's role and count as recomputed,
             every bar square at least 8px wide and every slab square at least 16px at 320px.
  Palette    every element of every screen drawn (start, each stage's question and wrong answer): no purple, and every
             colour one of the theme's (schools/assets/theme.css, light row) or the game's own tokens.
  Screens    the question screen holds the question, the bar when shown and the options or the answer box; the
             wrong-answer screen holds exactly one line, the bar, the correct sum and Next.
  Sessions   SESSIONS seeds per level: Foundation 5 per stage, Advanced 4, stages in order; no question twice; adding
             and taking away within one of half each in stages 1-3; the bar flagged on the first three of a stage only.
  Play       both levels, end to end, at 320x568, 390x844 and 1280x800, read from what the page shows (canon 7.9): the
             bar on the question exactly where flagged or after a wrong answer; a listed error gets the worked line
             the first three times, then the nudge; any other wrong answer the rule; a typed key in a form
             fractionForm sends back gets the message and nothing is marked; a right answer moves on by itself; the
             events at the level played and one score to that level's board. No sideways scroll.
  Phone fit  (canon 7.6.1) every pool entry, with every error it can carry and both help forms (and, typed, a wrong
             answer that is none), drawn by the game's own wrong-answer path at 320x568, 375x667, 390x844 and
             1280x800, normal and Aa: the line and Next above the fold (the viewport less the 40px footer); no
             sideways scroll. At 320x568, normal and Aa, every stage 1 question with its bar: the bar, the answer
             box, Check and the keypad all in the window together (Jon's ruling (3), 21 Oct 2026).
  Self-test  twelve faults planted into a copy of the page; each must FAIL (part 5 the seven in the engine, the bar and
             the palette; part 6 the five in play and the stage 1 fit).

    python scripts/verify-how-many-parts.py [--part 1-6] [--no-selftest] [--seeds N] [--sessions N] [--shots DIR]
    (CI runs the six parts side by side; no --part runs all six; --shots DIR saves one question and one wrong-answer
    screen per stage at 390px for Jon, and checks nothing)
"""
import argparse
import colorsys
import json
import os
import re
import sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'how-many-parts'
ROOT = os.path.dirname(HERE)
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
THEME = os.path.join(ROOT, 'schools', 'assets', 'theme.css')
BUILT = ['a', 'b', 'c', 'd', 'e', 'f']
SUMS = ['a', 'b', 'c']                 # the adding and taking-away stages (their pools hold sums, no kind)
MC = ['b', 'c']                        # multiple choice (stage 1 is typed: Jon's ruling (1), 21 Oct 2026)
FORM = {'a': 'simplest', 'd': 'simplest', 'e': 'simplest', 'f': 'mixed'}
LEVELS = {'ks3': {'per': 5, 'stages': ['a', 'b', 'c', 'd']}, 'gcse': {'per': 4, 'stages': ['a', 'b', 'c', 'd', 'e', 'f']}}
MAX_PARTS = 24
ORDER = ['TB', 'DN', 'KL', 'MD', 'MULT', 'OP']    # the 20 Oct catalogue's order (the pools' filter only)
SIZES = [(320, 568), (390, 844), (1280, 800)]
# Stage 6 questions where a listed error (a mixed number converted wrongly) equals the key: a student who converts
# wrongly is marked right. Reported to Jon on 21 Oct 2026; the pools stay as they are until he rules (HMP-CHOCOLATE
# keeps the pools). Printed on every run; any OTHER listed error equal to a key fails.
KNOWN_COLLISIONS = {('m', '/', 2, 1, 2, 1, 2, 3), ('m', '/', 2, 2, 3, 1, 1, 3)}


def lcm(a, b):
    return a * b // gcd(a, b)


def key_of(q):
    a, b, c, d = q['a'], q['b'], q['c'], q['d']
    return F(a, b) + F(c, d) if q['op'] == '+' else F(a, b) - F(c, d)


def named_errors(q):
    """{id: Fraction}: the 20 Oct catalogue (contract HOW-MANY-PARTS), now the pools' filter ONLY (HMP-CHOCOLATE keeps
    the pools as they were); what a student is offered is each stage's own list, sum_list below."""
    a, b, c, d, op = q['a'], q['b'], q['c'], q['d'], q['op']
    s = 1 if op == '+' else -1
    L = lcm(b, d)
    out = {}

    def put(i, n, m):
        if n > 0 and m > 0:
            out[i] = F(n, m)
    put('TB', a + s * c, b + s * d)            # added (took away) the tops and the bottoms
    if b != d:
        put('DN', a + s * c, L)                # changed a denominator without its numerator
        put('KL', a + s * c, max(b, d))        # kept the larger denominator
    put('MD', a + s * c, b * d)                # multiplied the denominators, added the numerators
    put('MULT', a * c, b * d)                  # multiplied the fractions
    other = abs(F(a, b) - s * F(c, d))         # the other operation (larger minus smaller)
    if other > 0:
        out['OP'] = other
    return out


def distinct(errs):
    seen, out = [], []
    for i in ORDER:
        if i in errs and errs[i] not in seen:
            seen.append(errs[i])
            out.append(i)
    return out


def stage_of(b, d):
    if b == d:
        return 'a'
    if b % d == 0 or d % b == 0:
        return 'b'
    return 'c'


def expected_pools():
    pools = {'a': [], 'b': [], 'c': []}
    for b in range(2, 13):
        for d in range(2, 13):
            st = stage_of(b, d)
            if st == 'c' and lcm(b, d) > MAX_PARTS:
                continue
            for a in range(1, b):
                if st != 'a' and gcd(a, b) != 1:
                    continue
                for c in range(1, d):
                    if st != 'a' and gcd(c, d) != 1:
                        continue
                    for op in '+-':
                        q = {'a': a, 'b': b, 'op': op, 'c': c, 'd': d}
                        k = key_of(q)
                        if not (0 < k < 1):
                            continue
                        e = named_errors(q)
                        if any(v == k for v in e.values()) or len(distinct(e)) < 3:
                            continue
                        pools[st].append((a, b, op, c, d))
    return pools


# ---------------------------------------------------------------------------------------------------------------
# Stages d-f (typed): the kinds, their keys, and the 20 Oct catalogue (the pools' filter only), written out here

def propers(maxd):
    return [(a, b) for b in range(2, maxd + 1) for a in range(1, b) if gcd(a, b) == 1]


def mixed_value(w, a, b):
    return w + F(a, b)


def typed_value(q):
    k = q['kind']
    if k == 'xw':
        return F(q['a'], q['b']) * q['n']
    if k == 'xf':
        return F(q['a'], q['b']) * F(q['c'], q['d'])
    if k == 'dw':
        return F(q['n'] * q['m'])
    if k == 'df':
        return F(q['a'], q['b']) / F(q['c'], q['d'])
    x, y = mixed_value(q['w1'], q['a'], q['b']), mixed_value(q['w2'], q['c'], q['d'])
    return {'+': x + y, '-': x - y, 'x': x * y, '/': x / y}[q['op']]


def typed_errors(q):
    """{id: value}: the 20 Oct catalogue for the typed kinds (the pools' filter only; typed_list below is what is named)."""
    k = q['kind']
    out = {}

    def put(i, v):
        if v is not None and v > 0:
            out[i] = v
    if k == 'xw':
        a, b, n = q['a'], q['b'], q['n']
        put('XW_BOTH', F(a * n, b * n))              # the top and the bottom times n (an equal fraction)
        put('XW_BOT', F(a, b * n))                   # the bottom times n
        put('XW_ADD', F(a + n, b))                   # n added to the top
    elif k == 'xf':
        x, y = F(q['a'], q['b']), F(q['c'], q['d'])
        L = lcm(q['b'], q['d'])
        put('XF_ADD', x + y)                         # added instead of multiplying
        put('XF_TB', F(q['a'] * q['c'], q['b'] + q['d']))      # tops multiplied, bottoms added
        put('XF_COMMON', F((q['a'] * L // q['b']) * (q['c'] * L // q['d']), L))   # a common bottom first
        put('XF_CROSS', F(q['a'] * q['d'], q['b'] * q['c']))   # across the diagonals
    elif k == 'dw':
        put('DW_DIV', F(q['n'], q['m']))             # n divided by m
        put('DW_REV', F(q['m'], q['n']))             # m divided by n
    elif k == 'df':
        a, b, c, d = q['a'], q['b'], q['c'], q['d']
        put('DF_NOFLIP', F(a * c, b * d))            # multiplied without turning the second over
        put('DF_FLIP1', F(b * c, a * d))             # turned the first over instead
        put('DF_FLIPBOTH', F(b * d, a * c))          # turned both over
    else:
        op, w1, a, b, w2, c, d = q['op'], q['w1'], q['a'], q['b'], q['w2'], q['c'], q['d']
        x, y, fx, fy = mixed_value(w1, a, b), mixed_value(w2, c, d), F(a, b), F(c, d)
        if op == 'x':
            put('M_SEP', w1 * w2 + fx * fy)          # wholes and fractions multiplied separately (Jon: an error)
        if op == '/':
            put('M_SEPD', F(w1, w2) + fx / fy)       # wholes and fractions divided separately
        if op == '-' and fx < fy:
            put('M_SWAP', (w1 - w2) + fy - fx)       # the smaller fraction from the bigger
        if op == '+':
            put('M_TB', w1 + w2 + F(a + c, b + d))   # wholes added, then the tops and the bottoms
        if op == '-' and b > d and a > c:
            put('M_TB', w1 - w2 + F(a - c, b - d))
        if op in '+-':
            put('M_DROPW', fx + fy if op == '+' else fx - fy)   # the whole numbers left out
        if op == '/':
            put('M_NOFLIP', x * y)
            put('M_FLIP1', y / x)
        if op == 'x':
            put('M_WHOLES', F(w1 * w2))
            put('M_ADD', x + y)
    return out


def tkey(q):
    k = q['kind']
    if k == 'xw':
        return (k, q['a'], q['b'], q['n'])
    if k == 'dw':
        return (k, q['n'], q['m'])
    if k in ('xf', 'df'):
        return (k, q['a'], q['b'], q['c'], q['d'])
    return (k, q['op'], q['w1'], q['a'], q['b'], q['w2'], q['c'], q['d'])


def expected_typed_pools():
    """Every model at most 24 parts across: a/b x n with b <= 8, n 2-6; a/b x c/d with b, d <= 6 and b x d <= 24 (the
    area model); n / (1/m) with n, m 2-8 and n x m <= 24; a/b / c/d with b, d <= 6 and lcm <= 24; mixed numbers with
    wholes 1-2, adding and taking away over denominators up to 6 with lcm <= 6, multiplying and dividing over
    denominators up to 4, the answer at least 1 with its simplest denominator at most 12. Less any question where a
    named error equals the key."""
    raw = {'d': [], 'e': [], 'f': []}
    for a, b in propers(8):
        for n in range(2, 7):
            raw['d'].append({'kind': 'xw', 'a': a, 'b': b, 'n': n})
    for a, b in propers(6):
        for c, d in propers(6):
            if b * d <= 24:
                raw['d'].append({'kind': 'xf', 'a': a, 'b': b, 'c': c, 'd': d})
            if lcm(b, d) <= 24:
                raw['e'].append({'kind': 'df', 'a': a, 'b': b, 'c': c, 'd': d})
    for n in range(2, 9):
        for m in range(2, 9):
            if n * m <= 24:
                raw['e'].append({'kind': 'dw', 'n': n, 'm': m})
    for wmax, maxd, ops in ((2, 6, '+-'), (2, 4, 'x/')):
        ms = [(w, a, b) for w in range(1, wmax + 1) for a, b in propers(maxd)]
        for x in ms:
            for y in ms:
                for op in ops:
                    q = {'kind': 'm', 'op': op, 'w1': x[0], 'a': x[1], 'b': x[2], 'w2': y[0], 'c': y[1], 'd': y[2]}
                    if op in '+-' and lcm(x[2], y[2]) > 6:
                        continue
                    k = typed_value(q)
                    if k < 1 or k.denominator > 12:
                        continue
                    raw['f'].append(q)
    return {st: sorted(tkey(q) for q in qs if not any(v == typed_value(q) for v in typed_errors(q).values()))
            for st, qs in raw.items()}


# ---------------------------------------------------------------------------------------------------------------
# Each stage's own errors (Jon, 21 Oct 2026), written out here from the contract's words, in the page's order

def sum_list(q, st):
    """{id: Fraction} for stages 1-3: the listed errors that apply (a positive top and bottom), in list order."""
    a, b, c, d, op = q['a'], q['b'], q['c'], q['d'], q['op']
    s = 1 if op == '+' else -1
    L = lcm(b, d)
    out = {}

    def put(i, n, m):
        if n > 0 and m > 0:
            out[i] = F(n, m)

    def other():
        v = abs(F(a, b) - s * F(c, d))
        if v > 0:
            out['OP'] = v
    put('TB', a + s * c, b + s * d)            # the tops and the bottoms (never a zero or negative bottom)
    if st == 'a':
        other()                                # the other operation
        if op == '-':
            put('TABB', a - c, b + d)          # the tops taken away, the bottoms added
        put('COUNT', a + s * c, 1)             # the count of parts as a whole number
    elif st == 'b':
        put('KL', a + s * c, max(b, d))        # the tops, and the bigger bottom kept
        put('DN', a + s * c, L)                # a bottom changed but not its top
        other()
    else:
        if op == '+':
            put('MD', a + c, b * d)            # the bottoms multiplied, the tops added as they were
        put('DN', a + s * c, L)                # the bottoms changed but not the tops
        other()
    return out


def typed_list(q):
    """{id: Fraction} for stages 4-6, in list order."""
    k, out = q['kind'], {}

    def put(i, v):
        if v is not None and v > 0:
            out[i] = v
    if k in ('xw', 'xf'):
        put('D_ADD', F(q['a'], q['b']) + (q['n'] if k == 'xw' else F(q['c'], q['d'])))   # added instead of multiplying
        if k == 'xf':
            put('D_KEEPB', F(q['a'] * q['c'], q['b']))     # the tops multiplied, a bottom kept
            put('D_KEEPD', F(q['a'] * q['c'], q['d']))
        else:
            put('XW_BOTH', F(q['a'] * q['n'], q['b'] * q['n']))   # top and bottom both times the whole number
    elif k in ('df', 'dw'):
        if k == 'df':
            put('DF_NOFLIP', F(q['a'] * q['c'], q['b'] * q['d']))   # multiplied without turning the second over
            put('DF_FLIP1', F(q['b'] * q['c'], q['a'] * q['d']))    # turned the first over
        else:
            put('DW_DIV', F(q['n'], q['m']))                       # the whole number divided by the bottom
    else:
        op, w1, a, b, w2, c, d = q['op'], q['w1'], q['a'], q['b'], q['w2'], q['c'], q['d']
        if op == 'x':
            put('M_SEP', w1 * w2 + F(a, b) * F(c, d))              # wholes and parts multiplied separately
        if op == '-' and F(a, b) < F(c, d):
            put('M_SWAP', (w1 - w2) + F(c, d) - F(a, b))           # the smaller part taken from the larger
        x, y = F(w1 + a, b), F(w2 + c, d)                          # whole + top over the bottom: converted wrongly
        put('M_CONV', {'+': x + y, '-': x - y, 'x': x * y, '/': x / y}[op])
    return out


LIST_IDS = {'a': {'TB', 'OP', 'TABB', 'COUNT'}, 'b': {'TB', 'KL', 'DN', 'OP'}, 'c': {'TB', 'MD', 'DN', 'OP'},
            'd': {'D_ADD', 'D_KEEPB', 'D_KEEPD', 'XW_BOTH'}, 'e': {'DF_NOFLIP', 'DF_FLIP1', 'DW_DIV'},
            'f': {'M_SEP', 'M_SWAP', 'M_CONV'}}


def listed(q):
    return sum_list(q, q['stage']) if q['stage'] in SUMS else typed_list(q)


def value_of(q):
    return key_of(q) if q['stage'] in SUMS else typed_value(q)


def qkey(q):
    return (q['a'], q['b'], q['op'], q['c'], q['d']) if q['stage'] in SUMS else tkey(q)


# ---------------------------------------------------------------------------------------------------------------
# The chocolate bar, recomputed from the question's numbers (contract HMP-CHOCOLATE)
#   bars: a list of strings, one per bar, one letter a square: a (first number), b (second, striped), e (eaten),
#   o (a piece outlined to be counted), - (a square not in the sum); slab: (cols, rows, a, c)

PARTS_NAME = {2: 'halves', 3: 'thirds', 4: 'quarters', 5: 'fifths', 6: 'sixths', 7: 'sevenths', 8: 'eighths',
              9: 'ninths', 10: 'tenths', 11: 'elevenths', 12: 'twelfths', 14: 'fourteenths', 15: 'fifteenths',
              16: 'sixteenths', 18: 'eighteenths', 20: 'twentieths', 21: 'twenty-firsts', 22: 'twenty-seconds',
              24: 'twenty-fourths'}


def runs(total, size):
    return [size] * (total // size)


def split(cells, L):
    return [cells[i:i + L] for i in range(0, len(cells), L)]


def whole_bars(v):
    w, r = divmod(v.numerator, v.denominator)
    den = v.denominator
    return ['a' * den] * w + (['a' * r + '-' * (den - r)] if r else [])


def expected_model(q, full):
    """{'kind', 'bars' | 'slab', 'groups', 'lots', 'cut'}: what the drawing must show."""
    st = q['stage']
    if st in SUMS:
        a, b, c, d, op = q['a'], q['b'], q['c'], q['d'], q['op']
        L = lcm(b, d)
        A, C = a * L // b, c * L // d
        pa, pc = L // b, L // d
        if op == '+':
            cells = 'a' * A + 'b' * C + '-' * (L - A - C)
            rest = L - A - C
            g = runs(A, pa) + runs(C, pc) + ([rest] if rest else [])    # the pieces counted; the rest one run
        else:
            cells = 'a' * (A - C) + 'e' * C + '-' * (L - A)
            g = runs(L, pa)
        return {'kind': 'bars', 'bars': [cells], 'groups': [g], 'lots': [[]], 'cut': b != d, 'L': L}
    k = q['kind']
    if k == 'xw':
        return {'kind': 'bars', 'bars': ['a' * q['a'] + '-' * (q['b'] - q['a'])] * q['n'], 'cut': False}
    if k == 'xf':
        return {'kind': 'slab', 'slab': (q['b'], q['d'], q['a'], q['c']), 'cut': False}
    if k == 'dw':
        return {'kind': 'bars', 'bars': ['o' * q['m']] * q['n'], 'cut': False}
    if k == 'df':
        L = lcm(q['b'], q['d'])
        A, C = q['a'] * L // q['b'], q['c'] * L // q['d']
        lots = [[s, min(C, A - s)] for s in range(0, A, C)]
        return {'kind': 'bars', 'bars': ['a' * A + '-' * (L - A)], 'groups': [[n for _, n in lots] + ([L - A] if L > A else [])],
                'lots': [lots], 'cut': q['b'] != q['d'], 'L': L}
    op, w1, a, b, w2, c, d = q['op'], q['w1'], q['a'], q['b'], q['w2'], q['c'], q['d']
    if op in '+-':
        L = lcm(b, d)
        X, Y = (w1 * b + a) * L // b, (w2 * d + c) * L // d
        if op == '+':
            n = -(-(X + Y) // L) * L
            cells = 'a' * X + 'b' * Y + '-' * (n - X - Y)
        else:
            n = -(-X // L) * L
            cells = 'a' * (X - Y) + 'e' * Y + '-' * (n - X)
        return {'kind': 'bars', 'bars': split(cells, L), 'cut': b != d, 'L': L}
    return {'kind': 'bars', 'bars': whole_bars(typed_value(q) if full else F(w1 * b + a, b)), 'cut': False}


def model_value(q, m):
    """What the drawing says the answer is, read from the squares alone."""
    if m['kind'] == 'slab':
        cols, rows, a, c = m['slab']
        return F(a * c, cols * rows)
    bars = m['bars']
    if q['stage'] in SUMS or q.get('kind') == 'm' and q['op'] in '+-':
        L = m['L']
        return F(sum(x.count('a') + x.count('b') for x in bars), L)
    if q['kind'] == 'xw':
        return F(sum(x.count('a') for x in bars), len(bars[0]))
    if q['kind'] == 'dw':
        return F(sum(x.count('o') for x in bars))
    if q['kind'] == 'df':
        return F(bars[0].count('a'), q['c'] * m['L'] // q['d'])
    return None


def page_model(m):
    """The page's HMP.model data in the same letters."""
    if m['kind'] == 'slab':
        return {'kind': 'slab', 'slab': (m['cols'], m['rows'], m['a'], m['c']), 'caption': m['caption']}
    letter = {'a': 'a', 'b': 'b', 'eaten': 'e', 'o': 'o', '': '-'}
    return {'kind': 'bars', 'bars': [''.join(letter.get(c, '?') for c in b['cells']) for b in m['bars']],
            'groups': [b['groups'] for b in m['bars']], 'lots': [b['lots'] for b in m['bars']], 'caption': m['caption']}


def check_model(q, m, full, out, where):
    """m: page_model() of HMP.model (or of the SVG read back). The drawing must be exactly the recomputed one, and say
    the answer."""
    want = expected_model(q, full)
    if m['kind'] != want['kind']:
        out.append('%s: a %s model, expected a %s' % (where, m['kind'], want['kind']))
        return
    if m['kind'] == 'slab':
        if tuple(m['slab']) != want['slab']:
            out.append('%s: the slab is %s (cols, rows, shaded columns, shaded rows), expected %s' % (where, m['slab'], want['slab']))
        elif model_value(q, want) != typed_value(q):
            out.append('%s: the slab overlap %s is not the product %s' % (where, model_value(q, want), typed_value(q)))
        return
    if m['bars'] != want['bars']:
        out.append('%s: %d bar(s) %s, expected %d: %s' % (where, len(m['bars']), m['bars'], len(want['bars']), want['bars']))
        return
    if any(len(x) > MAX_PARTS for x in m['bars']):
        out.append('%s: a bar of more than %d squares' % (where, MAX_PARTS))
    if 'groups' in want and m.get('groups') is not None and m['groups'] != want['groups']:
        out.append('%s: the pieces before cutting are %s, expected %s' % (where, m['groups'], want['groups']))
    if 'lots' in want and m.get('lots') is not None and m['lots'] != want['lots']:
        out.append('%s: the lots outlined are %s, expected %s' % (where, m['lots'], want['lots']))
    if 'caption' in m and bool(m['caption']) != want['cut']:
        out.append('%s: caption %r where the pieces %s cut' % (where, m['caption'], 'are' if want['cut'] else 'are not'))
    if m.get('caption') and want.get('L') and PARTS_NAME.get(want['L'], '') not in m['caption']:
        out.append('%s: the caption %r does not name the %s' % (where, m['caption'], PARTS_NAME.get(want['L'])))
    v = model_value(q, want)
    if v is not None and v != value_of(q) and not (q.get('kind') == 'm' and q['op'] in 'x/'):
        out.append('%s: the bar says %s, the key is %s' % (where, v, value_of(q)))
    if q.get('kind') == 'm' and q['op'] in 'x/' and full:
        got = sum(F(x.count('a'), len(x)) for x in m['bars'])
        if got != typed_value(q):
            out.append('%s: the answer bars show %s, the key is %s' % (where, got, typed_value(q)))


# ---------------------------------------------------------------------------------------------------------------
# The engine (no UI)

def frac_of(val):
    n, _, m = val.partition('/')
    return F(int(n), int(m) if m else 1)


def simplest_text(fr):
    return str(fr.numerator) if fr.denominator == 1 else '%d/%d' % (fr.numerator, fr.denominator)


TEX_FRAC = re.compile(r'\\dfrac\{(\d+)\}\{(\d+)\}')
MIXED_TEX = re.compile(r'^(\d*)\\dfrac\{(\d+)\}\{(\d+)\}$')


def tex_value(t):
    m = TEX_FRAC.fullmatch(t.strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    if re.fullmatch(r'\d+', t.strip()):
        return int(t), 1
    return None


def tex_frac(t):
    """A TeX value ('\\dfrac{a}{b}', '2\\dfrac{a}{b}', '12') as a Fraction, or None."""
    t = t.strip()
    m = MIXED_TEX.match(t)
    if m:
        return (int(m.group(1)) if m.group(1) else 0) + F(int(m.group(2)), int(m.group(3)))
    return F(int(t)) if re.fullmatch(r'\d+', t) else None


def mixed_tex_of(v):
    w, r = divmod(v.numerator, v.denominator)
    if r == 0:
        return str(w)
    return '%s\\dfrac{%d}{%d}' % (w or '', r, v.denominator)


def first_value(line):
    """The first value between § marks in a feedback line ('§\\dfrac{5}{14}§' or '§3§'), as a Fraction."""
    m = re.search(r'§([^§]*)§', line)
    if not m:
        return None
    return tex_frac(m.group(1))


def check_pools(page, out):
    got = page.evaluate("() => { const o = {}; for (const s of ['a','b','c']) o[s] = HMP.POOLS[s].map(q => [q.a, q.b, q.op, q.c, q.d]);"
                        " for (const s of ['d','e','f']) o[s] = HMP.POOLS[s]; return o; }")
    want = expected_pools()
    tw = expected_typed_pools()
    for st in ('d', 'e', 'f'):
        g = sorted(tkey(q) for q in got[st])
        if g != tw[st]:
            extra, miss = sorted(set(g) - set(tw[st])), sorted(set(tw[st]) - set(g))
            out.append('pool %s: serves %d entries this script leaves out (%s...), leaves out %d it should serve (%s...)'
                       % (st, len(extra), extra[:3], len(miss), miss[:3]))
        if len(g) != len(set(g)):
            out.append('pool %s: an entry appears twice' % st)
        if len(g) < 40:
            out.append('pool %s: %d entries (the contract asks at least 40)' % (st, len(g)))
    for st in SUMS:
        g = [tuple(x) for x in got[st]]
        if sorted(g) != sorted(want[st]):
            extra = sorted(set(g) - set(want[st]))
            miss = sorted(set(want[st]) - set(g))
            out.append('pool %s: serves %d entries this script leaves out (%s...), leaves out %d it should serve (%s...)'
                       % (st, len(extra), extra[:3], len(miss), miss[:3]))
        if len(g) != len(set(g)):
            out.append('pool %s: an entry appears twice' % st)
        n_add = sum(1 for x in g if x[2] == '+')
        if len(g) < 40 or n_add < 15 or len(g) - n_add < 15:
            out.append('pool %s: %d entries (%d adding, %d taking away): the contract asks at least 40, each kind 15'
                       % (st, len(g), n_add, len(g) - n_add))
    return {st: len(got[st]) for st in BUILT}


QUESTIONS_JS = r"""(seeds) => {
  const out = [];
  const tryOr = (f) => { try { return f(); } catch (e) { return 'THROWS: ' + e; } };
  for (const st of ['a', 'b', 'c', 'd', 'e', 'f']) for (const src of HMP.POOLS[st]) for (const s of (HMP.FORM[st] ? [1] : seeds)) {
    const q = HMP.makeQuestion(src, st, HMP.mulberry32(s * 7919 + (src.a || 0) * 131 + (src.b || 0) * 17 + (src.c || 0) * 5 + (src.d || 0)));
    const ids = q.typed ? HMP.listErrors(q).map(e => e.id) : q.choices.map(c => c.err);
    out.push({ q, part: HMP.model(q, false), full: HMP.model(q, true), sum: HMP.sumLine(q), rule: HMP.rule(q),
               listed: HMP.listErrors(q).map(e => e.id),
               ex: ids.map(id => ({ id, ex: tryOr(() => HMP.example(q, id)), nudge: tryOr(() => HMP.nudge(q, id)) })) });
  }
  return out;
}"""


def check_options(q, out, where, three):
    """Stages 2-3: every option but the key a listed error of the stage, recomputed; four options, or three where
    fewer than three listed errors apply."""
    k = key_of(q)
    if frac_of(q['keyVal']) != k or q['keyVal'] != simplest_text(k) or tex_value(q['keyTex']) != (k.numerator, k.denominator):
        out.append('%s: key %s (%s), recomputed %s in its simplest form' % (where, q['keyVal'], q['keyTex'], simplest_text(k)))
    errs = sum_list(q, q['stage'])
    firsts = []
    for i, v in errs.items():
        if v != k and v not in [x for _, x in firsts]:
            firsts.append((i, v))
    want_n = min(3, len(firsts))
    ch = q['choices']
    if len(ch) != want_n:
        out.append('%s: %d options besides the key; %d listed error(s) apply with distinct values, so %d' % (where, len(ch), len(firsts), want_n))
    if want_n == 2:
        three[q['stage']] = three.get(q['stage'], 0) + 1
    if want_n < 2:
        out.append('%s: fewer than two listed errors apply (%s): the question cannot have three options' % (where, list(errs)))
    vals = [k]
    for c in ch:
        v = frac_of(c['val'])
        if c['val'] != simplest_text(v) or tex_value(c['tex']) != (v.numerator, v.denominator):
            out.append('%s: option %s (%s) is not shown in its simplest form' % (where, c['val'], c['tex']))
        if c['err'] not in LIST_IDS[q['stage']]:
            out.append('%s: option %s is the error %s, which is not on stage %s\'s list' % (where, c['val'], c['err'], q['stage']))
        elif c['err'] not in errs:
            out.append('%s: option %s names %s, which does not apply here' % (where, c['val'], c['err']))
        elif errs[c['err']] != v:
            out.append('%s: option %s names %s, whose value is %s' % (where, c['val'], c['err'], errs[c['err']]))
        elif [i for i, x in firsts if x == v][:1] != [c['err']]:
            out.append('%s: option %s is named %s, but %s comes first on the list with that value' % (where, c['val'], c['err'], [i for i, x in firsts if x == v]))
        if v == k:
            out.append('%s: option %s is equal in value to the key %s' % (where, c['val'], simplest_text(k)))
        elif v in vals[1:]:
            out.append('%s: option %s twice' % (where, c['val']))
        vals.append(v)


def check_typed(item, out, where, collisions):
    q = item['q']
    k = value_of(q)
    form = FORM[q['stage']]
    if q.get('form') != form or not q.get('typed') or q.get('choices'):
        out.append('%s: form %s, typed %s, options %s (typed, %s)' % (where, q.get('form'), q.get('typed'), q.get('choices'), form))
    if frac_of(q['keyVal']) != k:
        out.append('%s: key %s, recomputed %s' % (where, q['keyVal'], simplest_text(k)))
    want_tex = mixed_tex_of(k) if form == 'mixed' else (str(k.numerator) if k.denominator == 1 else '\\dfrac{%d}{%d}' % (k.numerator, k.denominator))
    if q['keyTex'] != want_tex:
        out.append('%s: the key is shown as %s, not %s' % (where, q['keyTex'], want_tex))
    kp = q['keyParts']
    if form == 'mixed':
        w, r = divmod(k.numerator, k.denominator)
        ok = kp == {'whole': w, 'num': r, 'den': k.denominator}
    else:
        ok = kp == {'num': k.numerator, 'den': k.denominator}
    if not ok:
        out.append('%s: keyParts %s for the key %s (%s form)' % (where, kp, k, form))
    want_ask = ('As a mixed number, in its simplest form.' if form == 'mixed' else 'Simplest form.' if q['stage'] == 'a'
                else 'Simplest form, or a whole number.')
    if q.get('ask') != want_ask:
        out.append('%s: the question asks %r, not %r' % (where, q.get('ask'), want_ask))
    if q.get('kind') == 'dw' and q.get('lead') != 'How many %s are in %d?' % (PARTS_NAME[q['m']], q['n']):
        out.append('%s: the division is not framed as "how many %s are in %d?" (%r)' % (where, PARTS_NAME[q['m']], q['n'], q.get('lead')))
    nums = [int(x) for x in re.findall(r'\d+', q['sumTex'])]
    want = ([q['a'], q['b'], q['c'], q['d']] if q['stage'] == 'a' else
            {'xw': [q.get('a'), q.get('b'), q.get('n')], 'xf': [q.get('a'), q.get('b'), q.get('c'), q.get('d')],
             'dw': [q.get('n'), 1, q.get('m')], 'df': [q.get('a'), q.get('b'), q.get('c'), q.get('d')],
             'm': [q.get('w1'), q.get('a'), q.get('b'), q.get('w2'), q.get('c'), q.get('d')]}[q['kind']])
    if nums != want:
        out.append('%s: the sum shows %s, the question is %s' % (where, q['sumTex'], want))
    errs = listed(q)
    if item['listed'] != list(errs):
        out.append('%s: the page lists errors %s here, recomputed %s' % (where, item['listed'], list(errs)))
    hit = [i for i, v in errs.items() if v == k]
    if hit:
        if q['stage'] != 'a' and tkey(q) in KNOWN_COLLISIONS:
            collisions.add(tkey(q))
        else:
            out.append('%s: the listed error(s) %s equal the key %s: that slip would be marked right' % (where, hit, k))


def check_feedback(item, out, where):
    q = item['q']
    k = value_of(q)
    errs = listed(q)
    form = FORM.get(q['stage'], 'simplest')
    want_end = mixed_tex_of(k) if form == 'mixed' and q.get('typed') else (str(k.numerator) if k.denominator == 1 else '\\dfrac{%d}{%d}' % (k.numerator, k.denominator))
    if item['sum'].split('=')[-1].strip() != want_end:
        out.append('%s: the correct sum ends on %s, not the key %s' % (where, item['sum'].split('=')[-1].strip(), want_end))
    if item['sum'].count(q['sumTex']) != 1 or not item['sum'].startswith(q['sumTex']):
        out.append('%s: the correct sum %r does not start from the question %r once' % (where, item['sum'], q['sumTex']))
    for e in item['ex']:
        for kind in ('ex', 'nudge'):
            if str(e[kind]).startswith('THROWS') or not e[kind]:
                out.append('%s: the %s line for %s: %s' % (where, kind, e['id'], e[kind]))
        if e['id'] in errs and not str(e['ex']).startswith('THROWS') and first_value(e['ex']) != errs[e['id']]:
            out.append('%s: the worked line for %s starts from %s, the error gives %s' % (where, e['id'], first_value(e['ex']), errs[e['id']]))
    if not item['rule']:
        out.append('%s: no rule line for a wrong answer that is no listed error' % where)
    if (q['stage'] in SUMS or q.get('kind') == 'm' and q['op'] in '+-') and not item['rule'].startswith('The denominator says how many parts.'):
        out.append('%s: the rule line %r is not the premise' % (where, item['rule']))


def check_engine(page, out, seeds):
    sizes = check_pools(page, out)
    items = page.evaluate(QUESTIONS_JS, list(range(1, seeds + 1)))
    three, collisions = {}, set()
    for it in items:
        q = it['q']
        n0 = len(out)
        where = '%s %s' % (q['stage'], qkey(q))
        if q.get('typed'):
            check_typed(it, out, where, collisions)
        else:
            check_options(q, out, where, three)
        check_feedback(it, out, where)
        check_model(q, page_model(it['part']), False, out, where + ' (question)')
        check_model(q, page_model(it['full']), True, out, where + ' (feedback)')
        if len(out) - n0 and len(out) > 200:
            break
    for c in sorted(KNOWN_COLLISIONS - collisions):
        out.append('KNOWN_COLLISIONS names %s, which no longer collides: take it out' % (c,))
    seeds_per = max(1, seeds)
    return sizes, len(items), {st: (n // seeds_per, sizes[st]) for st, n in sorted(three.items())}, sorted(collisions)


# Every pool entry drawn by the game: its question screen with the bar (HMP.ui.ask), then its wrong-answer screen
# (HMP.ui.preview, its first listed error or, typed, a wrong answer that is none). The figure on each read back from
# the SVG: per bar its squares' roles, its pieces (data-groups), its outlined lots; a slab's squares row by row.
DRAWN_JS = r"""() => {
  const out = [];
  const read = (root) => {
    const figs = [...root.querySelectorAll('figure.choc')].filter(f => f.getClientRects().length);
    const res = { n: figs.length };
    if (!figs.length) return res;
    const f = figs[0], svg = f.querySelector('svg'), cap = f.querySelector('figcaption');
    res.caption = cap ? cap.textContent : null;
    const cells = [...svg.querySelectorAll('[data-cell]')];
    res.minW = Math.min(...cells.map(c => c.getBoundingClientRect().width));
    if (svg.dataset.model === 'slab') {
      const cols = +svg.dataset.cols, rows = +svg.dataset.rows, t = cells.map(c => c.dataset.cell);
      res.kind = 'slab';
      res.slabCells = t; res.cols = cols; res.rows = rows;
      return res;
    }
    res.kind = 'bars';
    res.bars = [...svg.querySelectorAll('g[data-bar]')].map(g => ({
      cells: [...g.querySelectorAll('[data-cell]')].map(c => c.dataset.cell),
      groups: g.dataset.groups.split(',').map(Number),
      lots: [...g.querySelectorAll('[data-lot]')].map(l => l.dataset.lot.split(',').map(Number)) }));
    return res;
  };
  for (const st of ['a', 'b', 'c', 'd', 'e', 'f']) for (const src of HMP.POOLS[st]) {
    HMP.ui.ask(src, st);
    const qScreen = read(document.getElementById('qcard'));
    const q = HMP.ui.question();
    const errs = q.typed ? HMP.listErrors(q).map(e => e.id) : q.choices.map(c => c.err);
    HMP.ui.preview(src, st, errs.length ? errs[0] : null, errs.length ? 'example' : null);
    const fb = document.querySelector('#feedback .fb');
    const kids = fb ? [...fb.children].map(c => c.tagName.toLowerCase() === 'figure' ? 'figure' : c.className) : [];
    const wScreen = read(document.getElementById('qcard'));
    out.push({ st, src, q: HMP.ui.question(), qScreen, wScreen, kids });
  }
  return out;
}"""


def svg_model(r):
    """A read-back figure in page_model()'s letters."""
    if r['kind'] == 'slab':
        t = r['slabCells']
        cols, rows = r['cols'], r['rows']
        a = sum(1 for c in range(cols) if t[c] in ('a', 'ab'))
        cc = sum(1 for i in range(rows) if t[i * cols] in ('bs', 'ab'))
        grid_ok = all(t[i * cols + j] == ('ab' if j < a and i < cc else 'a' if j < a else 'bs' if i < cc else '')
                      for i in range(rows) for j in range(cols))
        return {'kind': 'slab', 'slab': (cols, rows, a, cc) if grid_ok else ('a slab not shaded in whole columns and rows', t),
                'caption': r['caption']}
    letter = {'a': 'a', 'b': 'b', 'eaten': 'e', 'o': 'o', '': '-'}
    return {'kind': 'bars', 'bars': [''.join(letter.get(c, '?') for c in b['cells']) for b in r['bars']],
            'groups': [b['groups'] for b in r['bars']], 'lots': [b['lots'] for b in r['bars']], 'caption': r['caption']}


def check_drawn(page, out, min_px):
    """Every question screen and wrong-answer screen, drawn by the game and its figure read back."""
    page.click('#startBtn')
    wait_for(page, "() => HMP.ui.state() === 'asking'")
    n = 0
    for d in page.evaluate(DRAWN_JS):
        q = d['q']
        q['stage'] = d['st']
        where = '%s %s' % (d['st'], qkey(dict(d['src'], stage=d['st'])))
        n0 = len(out)
        for name, scr, full in (('question screen', d['qScreen'], False), ('wrong-answer screen', d['wScreen'], True)):
            if scr['n'] != 1:
                out.append('%s: %d chocolate figures on the %s (exactly one)' % (where, scr['n'], name))
                continue
            check_model(q, svg_model(scr), full, out, '%s, %s' % (where, name))
            floor = 16 if scr['kind'] == 'slab' else min_px
            if scr['minW'] < floor:
                out.append('%s, %s: a square is %.1fpx wide (at least %d)' % (where, name, scr['minW'], floor))
        if d['kids'] != ['fb-line', 'figure', 'fb-sum', 'fb-next']:
            out.append('%s: the wrong-answer screen holds %s (exactly the line, the bar, the correct sum and Next)' % (where, d['kids']))
        n += 2
        if len(out) - n0 and len(out) > 300:
            break
    return n


# ---------------------------------------------------------------------------------------------------------------
# The palette: no purple, and nothing outside the theme's and the game's own colours

TOKEN = re.compile(r'--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})')


def hexrgb(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def palette(html):
    """The theme's light-row tokens and the game's own (its first :root rule), as RGB triples, with white and the
    near-black text KaTeX and a browser default can give."""
    theme = open(THEME, encoding='utf-8').read()
    light = re.sub(r':root\[data-theme="dark"\][^{]*\{[^}]*\}', '', theme)
    game_root = re.search(r':root\{([^}]*)\}', html).group(1)
    cols = {hexrgb(v) for _, v in TOKEN.findall(light)} | {hexrgb(v) for _, v in TOKEN.findall(game_root)}
    return cols | {(255, 255, 255), (0, 0, 0)}


def is_purple(rgb):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in rgb))
    return 255 <= h * 360 <= 330 and s >= 0.25 and 0.12 <= l <= 0.92


COLOURS_JS = r"""() => {
  const props = ['color', 'background-color', 'border-top-color', 'border-right-color', 'border-bottom-color',
                 'border-left-color', 'outline-color', 'fill', 'stroke', 'stop-color'];
  const seen = {};
  for (const el of document.querySelectorAll('.container, .container *')) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || !el.getClientRects().length && !el.closest('svg')) continue;
    for (const p of props) {
      const v = cs.getPropertyValue(p);
      const m = /rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/.exec(v);
      if (!m || (m[4] !== undefined && +m[4] === 0)) continue;
      const key = m[1] + ',' + m[2] + ',' + m[3];
      if (!seen[key]) seen[key] = (el.tagName.toLowerCase() + (el.className && el.className.baseVal === undefined ? '.' + String(el.className).split(' ')[0] : el.getAttribute('class') ? '.' + el.getAttribute('class').split(' ')[0] : '') + ' ' + p);
    }
  }
  return seen;
}"""

SAMPLES = {'a': {'a': 5, 'b': 7, 'op': '-', 'c': 2, 'd': 7}, 'b': {'a': 1, 'b': 4, 'op': '+', 'c': 3, 'd': 8},
           'c': {'a': 1, 'b': 2, 'op': '+', 'c': 1, 'd': 3}, 'd': {'kind': 'xf', 'a': 2, 'b': 3, 'c': 3, 'd': 4},
           'e': {'kind': 'dw', 'n': 3, 'm': 4}, 'f': {'kind': 'm', 'op': '+', 'w1': 1, 'a': 1, 'b': 2, 'w2': 2, 'c': 1, 'd': 3}}
EXTRA = [('d', {'kind': 'xw', 'a': 2, 'b': 5, 'n': 3}), ('e', {'kind': 'df', 'a': 2, 'b': 3, 'c': 1, 'd': 4}),
         ('f', {'kind': 'm', 'op': '-', 'w1': 2, 'a': 1, 'b': 2, 'w2': 1, 'c': 1, 'd': 3}),
         ('f', {'kind': 'm', 'op': 'x', 'w1': 1, 'a': 1, 'b': 2, 'w2': 2, 'c': 1, 'd': 2}),
         ('f', {'kind': 'm', 'op': '/', 'w1': 1, 'a': 1, 'b': 2, 'w2': 1, 'c': 1, 'd': 3})]


def screens(page, each):
    """Calls each(name) on the start screen, then on every sample's question and wrong-answer screens."""
    each('start')
    page.click('#startBtn')
    wait_for(page, "() => HMP.ui.state() === 'asking'")
    for st, src in list(SAMPLES.items()) + EXTRA:
        page.evaluate("([s, q]) => HMP.ui.ask(q, s)", [st, src])
        each('%s question %s' % (st, json.dumps(src)))
        page.evaluate("""([s, q]) => { const x = HMP.makeQuestion(q, s, HMP.mulberry32(1)); const e = HMP.listErrors(x);
            HMP.ui.preview(q, s, e.length ? e[0].id : null, 'example'); }""", [st, src])
        each('%s wrong %s' % (st, json.dumps(src)))


def check_palette(page, html, out):
    pal = palette(html)
    bad = {}

    def each(name):
        for rgb, where in page.evaluate(COLOURS_JS).items():
            t = tuple(int(x) for x in rgb.split(','))
            if is_purple(t):
                bad.setdefault('purple rgb(%s) on %s' % (rgb, where), name)
            elif t not in pal:
                bad.setdefault('rgb(%s) on %s is not one of the theme\'s or the game\'s colours' % (rgb, where), name)
    screens(page, each)
    for k, v in sorted(bad.items()):
        out.append('palette: %s (%s)' % (k, v))


# ---------------------------------------------------------------------------------------------------------------
# Sessions

SESSIONS_JS = r"""(n) => {
  const out = [];
  for (const lv of ['ks3', 'gcse']) for (let s = 1; s <= n; s++) out.push(HMP.buildSession(s * 104729 + 3, lv));
  return out;
}"""


def check_sessions(page, out, n):
    for sess in page.evaluate(SESSIONS_JS, n):
        lv = sess['level']
        L = LEVELS[lv]
        stages = [s for s in L['stages'] if s in BUILT]
        qs = sess['questions']
        tag = '%s seed %d' % (lv, sess['seed'])
        if sess['stages'] != stages or len(qs) != L['per'] * len(stages):
            out.append('%s: stages %s, %d questions; expected %s, %d' % (tag, sess['stages'], len(qs), stages, L['per'] * len(stages)))
            continue
        for i, st in enumerate(stages):
            block = qs[i * L['per']:(i + 1) * L['per']]
            if any(q['stage'] != st for q in block):
                out.append('%s: stage %s out of order' % (tag, st))
            per, first = L['per'], (L['per'] + 1) // 2
            if st in ('d', 'e', 'f'):
                plan = (['xw'] * first + ['xf'] * (per - first) if st == 'd' else ['dw'] * first + ['df'] * (per - first)
                        if st == 'e' else [['+', '-', 'x', '/'][j % 4] for j in range(per)])
                got_plan = [q['op'] if q['kind'] == 'm' else q['kind'] for q in block]
                if got_plan != plan:
                    out.append('%s: stage %s serves %s, expected %s' % (tag, st, got_plan, plan))
                keys = [tkey(q) for q in block]
            else:
                subs = sum(1 for q in block if q['op'] == '-')
                if subs not in (per // 2, (per + 1) // 2):
                    out.append('%s: stage %s takes away on %d of %d' % (tag, st, subs, per))
                keys = [(q['a'], q['b'], q['op'], q['c'], q['d']) for q in block]
                if (st == 'a') != bool(block[0].get('typed')):
                    out.append('%s: stage %s is %s (stage 1 typed, 2 and 3 multiple choice)' % (tag, st, 'typed' if block[0].get('typed') else 'multiple choice'))
            if len(set(keys)) != len(keys):
                out.append('%s: stage %s repeats a question' % (tag, st))
            flags = [q['bar'] for q in block]
            if flags != [j < 3 for j in range(L['per'])]:
                out.append('%s: stage %s flags the bar on %s (the first 3 only)' % (tag, st, flags))
        if [q['index'] for q in qs] != list(range(1, len(qs) + 1)):
            out.append('%s: question numbers %s' % (tag, [q['index'] for q in qs]))


# ---------------------------------------------------------------------------------------------------------------
# Play, in Chromium

INIT = r"""
window.__ev = [];
window.__sub = [];
Object.defineProperty(window, 'mfg', { configurable: true, get() { return (n, p) => window.__ev.push([n, p]); }, set(v) {} });
const __st = window.setTimeout;
// Game timers at a quarter of their length (the right-answer pause, Next's fallback); the worked example's
// "no fallback" stays as long as it is.
window.setTimeout = function (f, ms, ...a) { return __st(f, ms >= 2147483647 ? ms : (ms || 0) / 4, ...a); };
"""

STATE_JS = r"""() => {
  const fb = document.querySelector('#feedback');
  const line = fb.querySelector('.fb-line');
  const vis = el => !!el && el.getClientRects().length > 0;
  return {
    state: HMP.ui.state(), index: HMP.ui.index(), q: HMP.ui.question(),
    screen: ['menu', 'game', 'results'].find(s => document.getElementById(s).classList.contains('active')),
    qbarsVisible: vis(document.querySelector('#qbars figure.choc')),
    figures: [...document.querySelectorAll('#qcard figure.choc')].filter(vis).length,
    right: !!fb.querySelector('.fb-quick'), wrong: !!fb.querySelector('.fb.wrong'),
    help: line ? line.getAttribute('data-help') : null, helpErr: line ? line.getAttribute('data-err') : null,
    sum: !!fb.querySelector('.fb-sum .katex'), next: !!fb.querySelector('.fb-next button'),
    kids: [...(fb.querySelector('.fb') || { children: [] }).children].map(c => c.tagName.toLowerCase() === 'figure' ? 'figure' : c.className),
    optH: [...document.querySelectorAll('#options .opt')].map(b => b.getBoundingClientRect().height),
    optKatex: [...document.querySelectorAll('#options .opt')].every(b => !!b.querySelector('.katex')),
    promptKatex: !!document.querySelector('#prompt .katex'),
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    inputs: [...document.querySelectorAll('#typedForm input')].filter(i => i.offsetParent !== null).length,
    inputH: [...document.querySelectorAll('#typedForm input, #checkBtn')].filter(i => i.offsetParent !== null).map(i => i.getBoundingClientRect().height),
    msg: document.getElementById('msg').textContent
  };
}"""


def typed_entries(q, value, form):
    """Box contents (whole, num, den) for a value in the asked form."""
    if form == 'mixed':
        w, r = divmod(value.numerator, value.denominator)
        return (str(w), str(r) if r else '', str(value.denominator) if r else '')
    return ('', str(value.numerator), str(value.denominator) if value.denominator != 1 else '')


def type_answer(page, entries):
    page.evaluate("""(e) => { const ids = ['tWhole', 'tNum', 'tDen'];
        ids.forEach((id, i) => { document.getElementById(id).value = e[i]; });
        document.getElementById('typedForm').requestSubmit(); }""", list(entries))


def wait_for(page, js, ms=8000):
    page.wait_for_function(js, timeout=ms)


def play(page, level, size, out, wrong_at=(1, 2, 4, 7, 8)):
    """One full session at `level`: a listed error on the questions numbered in wrong_at (where one applies), right on
    the rest. A typed question first gets its key in a form fractionForm sends back: the message, nothing marked. The
    last typed question gets a wrong value that is no listed error: the rule line. Returns the number played."""
    tag = '%s %dx%d' % (level, size[0], size[1])
    page.evaluate("() => { window.__ev.length = 0; window.__sub.length = 0; }")
    page.click('.level-btn[data-level="%s"]' % level)
    page.click('#startBtn')
    wait_for(page, "() => HMP.ui.state() === 'asking'")
    named, seen_after_wrong = 0, False
    n = page.evaluate("() => HMP.ui.session().questions.length")
    for i in range(1, n + 1):
        wait_for(page, "() => HMP.ui.state() === 'asking' && HMP.ui.index() === %d" % i)
        s = page.evaluate(STATE_JS)
        q = s['q']
        where = '%s Q%d (%s %s)' % (tag, i, q['stage'], qkey(q))
        want_bar = q['bar'] or seen_after_wrong
        if s['qbarsVisible'] != want_bar:
            out.append('%s: the bar is %s on the question; expected %s (first 3 of a stage: %s; after a wrong answer: %s)'
                       % (where, 'shown' if s['qbarsVisible'] else 'missing', 'shown' if want_bar else 'none', q['bar'], seen_after_wrong))
        if s['figures'] > 1:
            out.append('%s: %d chocolate figures on the question screen' % (where, s['figures']))
        if s['overflow'] > 0:
            out.append('%s: the page scrolls sideways by %dpx' % (where, s['overflow']))
        typed = bool(q.get('typed'))
        if not s['promptKatex'] or (not typed and not s['optKatex']):
            out.append('%s: a fraction is not drawn by KaTeX' % where)
        errs = listed(q)
        k = value_of(q)
        wrongs = [v for v in errs.values() if v != k]
        rule = False
        if typed:
            form = FORM[q['stage']]
            if s['optH']:
                out.append('%s: options on a typed question' % where)
            want_inputs = 3 if form == 'mixed' else 2
            if s['inputs'] != want_inputs or min(s['inputH'] or [0]) < 44:
                out.append('%s: %d answer boxes shown (want %d), heights %s (each at least 44px)' % (where, s['inputs'], want_inputs, s['inputH']))
            if form == 'mixed' and k.denominator != 1:
                fmt = ('', str(k.numerator), str(k.denominator))
            elif form == 'mixed':
                fmt = ('', str(2 * k.numerator), '2')
            else:
                fmt = ('', str(2 * k.numerator), str(2 * k.denominator))
            n_ev = len(page.evaluate("() => window.__ev"))
            type_answer(page, fmt)
            page.wait_for_timeout(60)
            g = page.evaluate(STATE_JS)
            if g['state'] != 'asking' or not g['msg'] or len(page.evaluate("() => window.__ev")) != n_ev:
                out.append('%s: the key in the wrong form %s was %s (want the format message, nothing marked): msg %r'
                           % (where, fmt, g['state'], g['msg']))
                if g['state'] != 'asking':
                    out.append('%s: (play stopped here)' % where)
                    prepare(page, reload=True)
                    return n
            go_wrong = i in wrong_at and bool(wrongs)
            if go_wrong:
                type_answer(page, typed_entries(q, wrongs[0], form))
            elif i == n:
                bad = next(v for v in (k + 1, k + 2, k + 3) if v not in errs.values())
                rule, go_wrong = True, True
                type_answer(page, typed_entries(q, bad, form))
            else:
                type_answer(page, typed_entries(q, k, form))
        else:
            want_opts = len(q['choices']) + 1
            if len(s['optH']) != want_opts or want_opts not in (3, 4) or min(s['optH']) < 44:
                out.append('%s: options %s (%d, each at least 44px tall)' % (where, s['optH'], want_opts))
            if s['inputs']:
                out.append('%s: answer boxes on a multiple-choice question' % where)
            go_wrong = i in wrong_at
            page.evaluate("""(w) => { const key = HMP.ui.question().keyVal;
                [...document.querySelectorAll('#options .opt')].find(b => w ? b.dataset.val !== key : b.dataset.val === key).click(); }""", go_wrong)
        wait_for(page, "() => !!document.querySelector('#feedback .fb-quick, #feedback .fb.wrong')")
        f = page.evaluate(STATE_JS)
        if go_wrong:
            if not rule:
                named += 1
            if not f['wrong'] or f['right']:
                out.append('%s: a wrong answer was not marked wrong' % where)
            if f['kids'] != ['fb-line', 'figure', 'fb-sum', 'fb-next']:
                out.append('%s: the wrong-answer screen holds %s (the line, the bar, the correct sum, Next)' % (where, f['kids']))
            if f['figures'] != 1:
                out.append('%s: %d chocolate figures on the wrong-answer screen (exactly one)' % (where, f['figures']))
            if not f['sum']:
                out.append('%s: the correct sum is not drawn by KaTeX' % where)
            want_help = 'rule' if rule else 'example' if named <= 3 else 'nudge'
            if f['help'] != want_help:
                out.append('%s: %s got %s, expected %s' % (where, 'a wrong answer that is no listed error' if rule else
                                                            'listed error %d' % named, f['help'], want_help))
            if f['overflow'] > 0:
                out.append('%s: the feedback scrolls sideways by %dpx' % (where, f['overflow']))
            if not f['next']:
                out.append('%s: no Next after a wrong answer' % where)
            else:
                page.wait_for_timeout(150)
                if page.evaluate("() => HMP.ui.index()") != i or page.evaluate("() => HMP.ui.state()") != 'wrong':
                    out.append('%s: a wrong answer moved on without Next' % where)
                page.click('#feedback .fb-next button')
            seen_after_wrong = True
        else:
            if not f['right'] or f['wrong']:
                out.append('%s: the key was not marked right' % where)
            seen_after_wrong = False
    wait_for(page, "() => document.getElementById('results').classList.contains('active')")
    ev = page.evaluate("() => window.__ev")
    sub = page.evaluate("() => window.__sub")
    names = [e[0] for e in ev]
    if names.count('game_started') != 1 or names.count('game_completed') != 1 or names.count('question_answered') != n:
        out.append('%s: events %s' % (tag, {x: names.count(x) for x in set(names)}))
    for name, p in ev:
        if p.get('game_slug') != SLUG or p.get('level') != level or 'mode' not in p:
            out.append('%s: %s sent %s' % (tag, name, p))
    modes = [p['mode'] for nm, p in ev if nm == 'question_answered']
    stages = [s for s in LEVELS[level]['stages'] if s in BUILT]
    if modes != [s for s in stages for _ in range(LEVELS[level]['per'])]:
        out.append('%s: question_answered modes %s' % (tag, modes))
    if sub != [[SLUG, level, sub[0][2] if sub else None, n]]:
        out.append('%s: submitScore calls %s (one, to %s, for %d questions)' % (tag, sub, level, n))
    page.click('#againBtn')
    return n


# ---------------------------------------------------------------------------------------------------------------
# Phone fit (canon 7.6.1), normal and Aa

PHONES = [(320, 568), (375, 667), (390, 844), (1280, 800)]
PART_SIZES = {'2': [(320, 568)], '3': [(375, 667), (390, 844)], '4': [(1280, 800)]}
FOOTER = 40   # the fixed site footer (canon 7.6.1: measure against the viewport less it)

PHONE_JS = r"""(fold) => {
  const bad = [], r = el => el.getBoundingClientRect();
  let n = 0, tight = 0;
  for (const st of ['a', 'b', 'c', 'd', 'e', 'f']) for (const src of HMP.POOLS[st]) {
    const q0 = HMP.makeQuestion(src, st, HMP.mulberry32(1));
    const shapes = [];
    const ids = q0.typed ? HMP.listErrors(q0).map(e => e.id) : q0.choices.map(c => c.err);
    for (const id of ids) for (const help of ['example', 'nudge']) shapes.push([id, help]);
    if (q0.typed) shapes.push([null, null]);
    for (const [eid, help] of shapes) {
      HMP.ui.preview(src, st, eid, help);
      window.scrollTo(0, 0);
      n++;
      const fb = document.querySelector('#feedback .fb');
      const where = st + ' ' + JSON.stringify(src) + ' ' + eid + ' ' + help;
      const line = fb.querySelector('.fb-line'), nx = fb.querySelector('.fb-next button'), fig = fb.querySelector('figure.choc');
      if (!nx || !line || !fig) { bad.push(where + ': the line, the bar or Next is missing'); continue; }
      if (r(line).top < 0) bad.push(where + ': the line starts above the screen');
      if (r(line).bottom > fold + 0.5) bad.push(where + ': the line ends at ' + Math.round(r(line).bottom) + 'px, below the fold at ' + fold + 'px');
      if (r(nx).bottom > fold + 0.5) bad.push(where + ': Next ends at ' + Math.round(r(nx).bottom) + 'px, below the fold at ' + fold + 'px');
      if (r(nx).height < 44) bad.push(where + ': Next is ' + r(nx).height + 'px tall');
      if (document.documentElement.scrollWidth > window.innerWidth) bad.push(where + ': scrolls sideways by ' + (document.documentElement.scrollWidth - window.innerWidth) + 'px');
      const sum = fb.querySelector('.fb-sum');
      if (fb.classList.contains('tight')) {
        // the bar moved after Next because it would have pushed Next below the fold: visual order line, sum, Next, bar
        tight++;
        if (!(r(line).bottom <= r(sum).top + 0.5 && r(sum).bottom <= r(nx).top + 0.5 && r(nx).bottom <= r(fig).top + 0.5)) bad.push(where + ': (tight) not drawn line, sum, Next, then the bar');
      } else if (!(r(line).bottom <= r(fig).top + 0.5 && r(fig).bottom <= r(sum).top + 0.5 && r(sum).bottom <= r(nx).top + 0.5)) {
        bad.push(where + ': not drawn line, bar, sum, Next');
      }
      if (bad.length > 4000) return { n, tight, bad };
    }
  }
  return { n, tight, bad };
}"""

# Jon's ruling (3), 21 Oct 2026: on stage 1 at 320px the bar and the keypad fit together. Every stage 1 question,
# asked with its bar: the bar, the answer boxes, Check and the keypad all inside the window (above the footer).
FIT_JS = r"""(fold) => {
  const bad = [], r = el => el.getBoundingClientRect();
  let n = 0;
  for (const src of HMP.POOLS.a) {
    HMP.ui.ask(src, 'a');
    window.scrollTo(0, 0);
    n++;
    const parts = { bar: document.querySelector('#qbars figure.choc'), boxes: document.querySelector('#typedForm'),
                    check: document.getElementById('checkBtn'), keypad: document.querySelector('#kpHolder > *') };
    const where = 'a ' + JSON.stringify(src);
    for (const [k, el] of Object.entries(parts)) {
      if (!el || !el.getClientRects().length) { bad.push(where + ': no ' + k + ' on the question'); continue; }
      if (r(el).top < 0 || r(el).bottom > fold + 0.5) bad.push(where + ': the ' + k + ' spans ' + Math.round(r(el).top) + '-' + Math.round(r(el).bottom) + 'px, outside the window (0-' + fold + 'px)');
    }
    if (document.documentElement.scrollWidth > window.innerWidth) bad.push(where + ': scrolls sideways');
    if (bad.length > 200) break;
  }
  return { n, bad };
}"""


def check_phone(page, size, out, aa):
    page.click('#startBtn')
    wait_for(page, "() => HMP.ui.state() === 'asking'")
    tag = '%dx%d%s' % (size[0], size[1], ' Aa' if aa else '')
    res = page.evaluate(PHONE_JS, size[1] - FOOTER)
    for b in res['bad']:
        out.append('phone %s: %s' % (tag, b))
    n = '%d (%d with the bar after Next)' % (res['n'], res['tight'])
    if size == (320, 568):
        fit = page.evaluate(FIT_JS, size[1] - FOOTER)
        for b in fit['bad']:
            out.append('stage 1 fit %s: %s' % (tag, b))
        if not page.evaluate("() => !!(HMP.ui.keypad() && HMP.ui.keypad().enabled && HMP.ui.keypad().enabled())"):
            out.append('stage 1 fit %s: the keypad is not drawn on this touch screen' % tag)
    return n


def open_page(pw, base, html, size, aa=False):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script(INIT)
    if aa:
        ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    prepare(page)
    if aa and not page.evaluate("() => document.body.classList.contains('accessible')"):
        errors.append('Aa mode did not switch on')
    return br, page, errors


def prepare(page, reload=False):
    """Wait for the game (reloading it first when a play stopped half way), and record what it would submit: the
    leaderboard is blocked here."""
    if reload:
        page.reload(wait_until='load', timeout=20000)
    page.wait_for_function('!!window.HMP && !!HMP.ui && typeof katex !== "undefined"', timeout=10000)
    page.evaluate("""() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")


def static_checks(html, out):
    if 'name="robots" content="noindex"' not in html:
        out.append('the page is not noindex (the game is unlisted)')
    # Typed fractions are marked only by the shared MaffsAnswer.fractionForm (FRACTION-FORM): no other marker.
    if 'MaffsAnswer.fractionForm(raw, q.keyParts, { form: q.form })' not in html:
        out.append('the typed answer is not marked by MaffsAnswer.fractionForm against the key')
    if re.search(r'MaffsAnswer\.(exact|decimal|money|fraction|fractionOrDecimal|parse)\(', html):
        out.append('the page marks a typed answer with something other than MaffsAnswer.fractionForm')
    if re.search(r'<img\b|\.(png|jpe?g|webp|gif)\b', html.split('<body>')[1].split('<footer')[0], re.I):
        out.append('the game uses an image file (the chocolate is drawn in SVG in the page)')


def guarded(out, what, f):
    """Runs a check; a check that throws (a page error inside it, a timeout) is a failure, never a crash."""
    try:
        f()
    except Exception as e:  # noqa: BLE001 - any exception here is a finding
        out.append('%s threw: %s' % (what, str(e).splitlines()[0][:200]))


def check(html, out, seeds=3, sessions=100, sizes=SIZES, engine=True, plays=True, phones=PHONES, aa_modes=(False, True)):
    from playwright.sync_api import sync_playwright
    static_checks(html, out)
    proc, base = bc.start_stub_server()
    info = {}
    try:
        with sync_playwright() as pw:
            for n, size in enumerate(sizes):
                br, page, errors = open_page(pw, base, html, size)
                try:
                    if engine and n == 0:
                        guarded(out, 'the engine', lambda: info.update(zip(('pools', 'questions', 'three', 'collisions'), check_engine(page, out, seeds))))
                        guarded(out, 'the sessions', lambda: check_sessions(page, out, sessions))
                        guarded(out, 'the drawn screens', lambda: info.update(drawn=check_drawn(page, out, 8)))
                        prepare(page, reload=True)
                        guarded(out, 'the palette', lambda: check_palette(page, html, out))
                        prepare(page, reload=True)
                    if plays:
                        for lv in ('ks3', 'gcse'):
                            guarded(out, 'play %s %dx%d' % (lv, size[0], size[1]), lambda: info.setdefault('played', []).append(
                                '%s %dx%d: %d' % (lv, size[0], size[1], play(page, lv, size, out))))
                            prepare(page, reload=True)
                    if errors:
                        out.append('page errors at %dx%d: %s' % (size[0], size[1], '; '.join(errors[:3])))
                finally:
                    br.close()
            for size in phones:
                for aa in aa_modes:
                    br, page, errors = open_page(pw, base, html, size, aa)
                    try:
                        guarded(out, 'the phone fit at %dx%d' % size, lambda: info.setdefault('phone', []).append(
                            '%dx%d%s: %s' % (size[0], size[1], ' Aa' if aa else '', check_phone(page, size, out, aa))))
                        if errors:
                            out.append('page errors at %dx%d: %s' % (size[0], size[1], '; '.join(errors[:3])))
                    finally:
                        br.close()
    finally:
        proc.terminate()
        proc.wait()
    return info


def shots(html, folder):
    """One question and one wrong-answer screen per stage at 390x844, for Jon. Checks nothing."""
    from playwright.sync_api import sync_playwright
    os.makedirs(folder, exist_ok=True)
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            br, page, errors = open_page(pw, base, html, (390, 844))
            try:
                names, seen = [], {}

                def each(name):
                    # 'start', or '<stage> question|wrong {...}': a1-question.png, a1-wrong.png, d2-question.png, ...
                    parts = name.split(' ')
                    if len(parts) == 1:
                        fn = 'start.png'
                    else:
                        if parts[1] == 'question':
                            seen[parts[0]] = seen.get(parts[0], 0) + 1
                        fn = '%s%d-%s.png' % (parts[0], seen[parts[0]], parts[1])
                    names.append(fn)
                    page.evaluate("() => window.scrollTo(0, 0)")
                    page.screenshot(path=os.path.join(folder, fn))
                screens(page, each)
                print('%d screenshots in %s' % (len(names), folder))
            finally:
                br.close()
    finally:
        proc.terminate()
        proc.wait()


# Each plant: (what, old, new, which checks catch it).
PLANTS = [
    ('the filter cut: a pool entry the 20 Oct catalogue removes is served',
     'H.servable = function (q) { return !H.errorIsKey(q) && (!!q.kind || H.filterDistinct(q).length >= 3); };',
     'H.servable = function (q) { return !!q.kind || H.filterDistinct(q).length >= 3; };', 'engine'),
    ('the typed stages\' filter cut',
     "  ['d', 'e', 'f'].forEach(function (st) { H.POOLS[st] = H.POOLS[st].filter(H.servable); });", "", 'engine'),
    ('the key shown unsimplified (stages 2-3)',
     '    q.keyTex = H.tex(k);\n', '    q.keyTex = H.tex([k[0] * 2, k[1] * 2]);\n', 'engine'),
    ('an off-list error offered (stage 2): the fractions multiplied',
     "    b: [E_TB,\n",
     "    b: [E_TB, { id: 'MULT', f: function (q) { return [q.a * q.c, q.b * q.d]; }, name: function () { return 'You multiplied the fractions'; } },\n",
     'engine'),
    ('two bars on an adding question',
     "      return { kind: 'bars', bars: [bar(cells, g)], caption: H.cutCaption(q.b, q.d) };",
     "      return { kind: 'bars', bars: [bar(cells, g), bar(cells, g)], caption: H.cutCaption(q.b, q.d) };", 'engine'),
    ('a wrong square count (the second number one square short)',
     "        cells = fill(L, [['a', A], ['b', C]]);", "        cells = fill(L, [['a', A], ['b', Math.max(0, C - 1)]]);", 'engine'),
    ('a purple fill (the first number\'s squares)', '--choc-a:#9a6233', '--choc-a:#8b5cf6', 'engine'),
    ('a typed key in the wrong form marked right (unsimplified, or not a mixed number)',
     "    if (res === 'format' || res === 'unreadable') {",
     "    if (res === 'format') res = 'correct';\n    if (res === 'unreadable') {", 'play'),
    ('the bar not redrawn after a wrong answer', '    barNext = true;\n', '\n', 'play'),
    ('the wrong-answer screen without its bar', "    h += renderModel(H.model(q, true));\n", '\n', 'play'),
    ('no worked line for a listed error', 'H.HELP_EXAMPLES = 3;', 'H.HELP_EXAMPLES = 0;', 'play'),
    ('stage 1 laid out as on 20 Oct (the answer box under the sum, Check under the keypad)',
     "    var inline = q.typed && q.form !== 'mixed';", "    var inline = false;", 'fit'),
]


def selftest(html, kinds=('engine', 'play', 'fit')):
    ok = True
    for what, old, new, kind in PLANTS:
        if kind not in kinds:
            continue
        if html.count(old) != 1:
            print('  self-test %-60s *** CANNOT PLANT ***' % what)
            ok = False
            continue
        got = []
        check(html.replace(old, new), got, seeds=1, sessions=5, sizes=[(390, 844)] if kind != 'fit' else [],
              engine=kind == 'engine', plays=kind == 'play', phones=[(320, 568)] if kind == 'fit' else [],
              aa_modes=(True,) if kind == 'fit' else ())
        got = [g for g in got if not g.startswith('the page')]
        ok = ok and bool(got)
        print('  self-test %-60s %s' % (what, ('caught: ' + got[0][:110]) if got else '*** MISSED ***'))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--seeds', type=int, default=3, help='seeds per pool entry in stages 2-3 (default 3)')
    ap.add_argument('--sessions', type=int, default=100, help='sessions per level (default 100)')
    ap.add_argument('--part', choices=['1', '2', '3', '4', '5', '6'], help='one of the six parts CI runs side by side (default: all)')
    ap.add_argument('--shots', metavar='DIR', help='save one question and one wrong-answer screen per stage at 390px; check nothing')
    args = ap.parse_args()
    html = open(GAME, encoding='utf-8').read()
    if args.shots:
        shots(html, args.shots)
        return 0
    out = []
    one = args.part in (None, '1')
    phones = PART_SIZES[args.part] if args.part in ('2', '3', '4') else PHONES if args.part is None else []
    selftests = args.part in (None, '5', '6') and not args.no_selftest
    info = check(html, out, seeds=args.seeds, sessions=args.sessions, sizes=SIZES if one else [],
                 engine=one, plays=one, phones=phones) if (one or phones) else {}
    if one:
        print('%s: pools %s (after the filter); %d questions checked; %d screens drawn and read back; %d sessions per level; played %s'
              % (SLUG, info.get('pools'), info.get('questions', 0), info.get('drawn', 0), args.sessions, ', '.join(info.get('played', []))))
        print('three-option questions (fewer than three listed errors apply), of each pool: %s'
              % ', '.join('stage %s %d of %d (%.1f%%)' % (st, n, tot, 100.0 * n / tot) for st, (n, tot) in info.get('three', {}).items()))
        for c in info.get('collisions', []):
            print('KNOWN (awaiting Jon\'s ruling, HMP-CHOCOLATE): %s: a mixed number converted wrongly gives the key' % (c,))
    if phones:
        print('%s: wrong-answer screens measured %s' % (SLUG, ', '.join(info.get('phone', []))))
    ok = True
    if selftests:
        ok = selftest(html, {'5': ('engine',), '6': ('play', 'fit')}.get(args.part, ('engine', 'play', 'fit')))
    for f in out[:int(os.environ.get("HMP_SHOW", "60"))]:
        print('FAIL  ' + f)
    if len(out) > int(os.environ.get("HMP_SHOW", "60")):
        print("FAIL  ... and %d more" % (len(out) - int(os.environ.get("HMP_SHOW", "60"))))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
