#!/usr/bin/env python3
# ci-line: B2 | Truth Buster (every key reviewed against its statement's own words, SR-18; every reveal figure recomputed; all 60 played in Chromium) |
"""Truth Buster: every key reviewed against its statement as written, every figure recomputed, every item played.

The game (60 statements, three tiers of 20; a session deals 7 + 7 + 6) asks "Always True" or "Not Always True",
then reveals why. Its keys are judgements on statements, so they cannot be recomputed from data. The tranche 3
audit of 6 Oct 2026 found keys that held only under an unstated setting (a triangle's angles keyed false by
leaving the plane, t1_008 keyed by assuming it; parallel lines; the square root of -1), an open problem keyed
false as if disproved (pi contains every digit sequence), a theorem keyed true without the condition it needs
(sphere eversion), and reveal texts with false figures or titles. SR-18 (Jon, 6 Oct 2026): Truth Buster's
statements are worded so the key holds as written. The bank is read from the live page, then:

  Keys. KEYS below holds every item's reviewed key and the reason for it. Where the key depends on a setting
    or condition, the entry names the words the statement must contain for the key to hold as written
    (`needs`); a statement without them FAILS (the audit's fault shape). Where a key can be checked by
    computation (SymPy, exact arithmetic, enumeration), the check runs.
  Pins. A key is a judgement on the words, so REVIEWED holds each item's content hash from the review: any
    edit FAILS until its entry is re-reviewed (then --print-pins, and paste).
  Figures. FIGURES holds every numerical or algebraic claim in each reveal title, reveal text and
    counterexample, each with a check that recomputes it. Every "=", "≈", "≠", "<" and ">" in those fields must
    lie inside a listed claim, so a new or edited figure with no check FAILS (verifiers recompute explanation
    figures, not just keys). Facts that cannot be computed (dates, a published count) sit in SOURCED with the
    source they were checked against.
  Chromium (390x844). Every item is shown through the game's own renderQuestion(); both answers are pressed
    on a fresh render: the key is marked "Correct", the other "Incorrect", and the reveal shows the item's own
    title, text and counterexample. Nothing is submitted and every request off the stub server is aborted.

A self-test plants three of the audit's own faults back into a copy of the page (t3-001: pi's statement
without "has been proved"; t3-003: sphere eversion without "pass through itself"; t3-005: "(-0.3)^2 = 0.09,
smaller than 0.3"); each must FAIL naming its item through a check other than the REVIEWED pin. It runs
unless --no-selftest.

    python scripts/verify-truth-buster.py [--verbose] [--no-selftest] [--against FILE] [--print-pins]

--against FILE serves FILE as the game page (e.g. main's copy, to show the check fails on it).
"""
import argparse
import itertools
import math
import os
import re
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'truth-buster'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'tier1': 20, 'tier2': 20, 'tier3': 20}
FIELDS = ('revealTitle', 'revealText', 'counterexample')
AUDIT = {
    'tb_t2_018': 't3-001', 'tb_t3_001': 't3-002', 'tb_t3_002': 't3-002', 'tb_t3_012': 't3-002', 'tb_t1_008': 't3-002',
    'tb_t3_004': 't3-003', 'tb_t1_002': 't3-004', 'tb_t1_015': 't3-005', 'tb_t1_017': 't3-006', 'tb_t1_014': 't3-007',
    'tb_t2_006': 't3-008', 'tb_t2_017': 't3-009', 'tb_t3_013': 't3-010', 'tb_t3_003': 't3-011', 'tb_t2_013': 't3-012',
    'tb_t1_007': 't3-015', 'tb_t1_013': 't3-015', 'tb_t2_009': 't3-015', 'tb_t2_014': 't3-015', 'tb_t3_007': 't3-015',
    'tb_t3_010': 't3-015', 'tb_t3_017': 't3-015', 'tb_t2_020': 't3-015', 'tb_t3_008': 't3-015', 'tb_t3_009': 't3-015',
}

x, n, m, g = sp.symbols('x n m g')
xr = sp.Symbol('xr', real=True)


def K(answer, why, needs=(), check=None):
    return {'answer': answer, 'why': why, 'needs': needs, 'check': check}


def mult9_reversed():
    return all(int(str(k)[::-1]) % 9 == 0 for k in range(9, 100000, 9))


def birthday():
    p = F(1)
    for k in range(23):
        p *= F(365 - k, 365)
    return p


def primes_upto(N):
    return [p for p in range(2, N + 1) if all(p % d for d in range(2, int(p ** 0.5) + 1))]


KEYS = {
    # ---------------- Tier 1 ----------------
    'tb_t1_001': K(False, 'a rhombus with 60° and 120° angles has four equal sides'),
    'tb_t1_002': K(False, '10 × 0.3 = 3 < 10', check=lambda: 10 * F(3, 10) < 10),
    'tb_t1_003': K(True, 'in a triangle the larger side is opposite the larger angle (Euclid I.18-19)'),
    'tb_t1_004': K(False, '(−3)(−4) = 12 > 0', check=lambda: (-3) * (-4) > 0),
    'tb_t1_005': K(True, 'a rectangle has two pairs of parallel sides'),
    'tb_t1_006': K(False, '√0.09 = 0.3 > 0.09', check=lambda: sp.sqrt(sp.Rational(9, 100)) > sp.Rational(9, 100)),
    'tb_t1_007': K(True, 'the average of two fractions lies between them and is a fraction'),
    'tb_t1_008': K(False, 'on a flat surface the angles sum to 180°, so two right angles leave 0°',
                   needs=('flat surface',)),
    'tb_t1_009': K(False, 'area scales by 4', check=lambda: sp.simplify(sp.pi * (2 * x) ** 2 / (sp.pi * x ** 2)) == 4),
    'tb_t1_010': K(False, '2 is prime and even'),
    'tb_t1_011': K(True, '2n + 2m + 1 = 2(n + m) + 1', check=lambda: sp.expand(2 * n + 2 * m + 1 - 2 * (n + m) - 1) == 0),
    'tb_t1_012': K(False, 'x² − 2x + 1 = 0 has one solution', check=lambda: len(sp.solve(x ** 2 - 2 * x + 1, x)) == 1),
    'tb_t1_013': K(False, 'a 1 × 9 rectangle and a 5 × 5 square: perimeters 20 and 20, areas 9 and 25'),
    'tb_t1_014': K(False, '1/10 < 1/2', check=lambda: F(1, 10) < F(1, 2)),
    'tb_t1_015': K(False, '0.4² = 0.16 < 0.4', check=lambda: F(2, 5) ** 2 < F(2, 5)),
    'tb_t1_016': K(True, 'a square has four right angles'),
    'tb_t1_017': K(False, '0.2 < 5, its reciprocal', check=lambda: F(1, 5) < 1 / F(1, 5)),
    'tb_t1_018': K(True, 'reversing digits keeps the digit sum', check=mult9_reversed),
    'tb_t1_019': K(False, '√2 + (−√2) = 0', check=lambda: sp.sqrt(2) + (-sp.sqrt(2)) == 0),
    'tb_t1_020': K(False, 'y = x³ passes through (0, 0) and is not proportional'),
    # ---------------- Tier 2 ----------------
    'tb_t2_001': K(False, '√((−5)²) = 5', check=lambda: sp.sqrt((-5) ** 2) != -5),
    'tb_t2_002': K(False, 'f(x) = x²: f(4) = f(−4)', check=lambda: 4 ** 2 == (-4) ** 2),
    'tb_t2_003': K(True, 'differentiability at a point implies continuity there'),
    'tb_t2_004': K(False, 'the harmonic series diverges', check=lambda: sp.summation(1 / n, (n, 1, sp.oo)) == sp.oo),
    'tb_t2_005': K(True, 'eˣ − x has minimum 1, at x = 0',
                   check=lambda: sp.minimum(sp.exp(xr) - xr, xr, sp.S.Reals) == 1),
    'tb_t2_006': K(False, 'the x-axis and the line x = 0, z = 1 are skew'),
    'tb_t2_007': K(False, 'a continuous distribution gives probability 0 to outcomes that can occur'),
    'tb_t2_008': K(False, '√2 × √2 = 2', check=lambda: sp.sqrt(2) * sp.sqrt(2) == 2),
    'tb_t2_009': K(True, 'the Extreme Value Theorem, on a closed and bounded interval', needs=('closed interval [a, b]',)),
    'tb_t2_010': K(False, 'similar is not congruent'),
    'tb_t2_011': K(False, 'ln is defined only for x > 0 in the reals'),
    'tb_t2_012': K(False, 'two ages that differ by a constant have r = 1 and neither causes the other'),
    'tb_t2_013': K(True, 'the derivative, where it exists, is the exact rate of change',
                   needs=('Where a function has a derivative',)),
    'tb_t2_014': K(True, 'Intermediate Value Theorem; real coefficients needed (x + i has no real root)',
                   needs=('real coefficients',)),
    'tb_t2_015': K(True, 'the Monotone Convergence Theorem'),
    'tb_t2_016': K(True, 'sin(nπ) = 0 for every integer n', check=lambda: sp.sin(n * sp.pi).subs(n, 7) == 0),
    'tb_t2_017': K(False, 'division by zero is undefined, not infinite'),
    'tb_t2_018': K(False, 'unproved: π is not known to be normal; the statement claims a proof',
                   needs=('It has been proved',)),
    'tb_t2_019': K(False, 'x² and x² + 5 have the same derivative',
                   check=lambda: sp.diff(x ** 2, x) == sp.diff(x ** 2 + 5, x)),
    'tb_t2_020': K(True, 'the reals are uncountable (Cantor)'),
    # ---------------- Tier 3 ----------------
    'tb_t3_001': K(False, 'a spherical triangle can have three 90° angles', needs=('on every surface, flat or curved',)),
    'tb_t3_002': K(False, 'in projective geometry every two lines meet', needs=('whatever kind of geometry',)),
    'tb_t3_003': K(True, 'the Jordan curve theorem', needs=('simple closed curve', 'in the plane')),
    'tb_t3_004': K(True, 'Smale: a sphere can be everted by a regular homotopy, passing through itself',
                   needs=('pass through itself',)),
    'tb_t3_005': K(True, 'n ↔ 2n is a bijection'),
    'tb_t3_006': K(False, 'the partial sums grow without bound', check=lambda: sp.summation(n, (n, 1, 100)) == 5050),
    'tb_t3_007': K(True, 'Brouwer, on the closed disc', needs=('closed disc',)),
    'tb_t3_008': K(False, 'a torus has F + V − E = 0'),
    'tb_t3_009': K(False, 'the coastline paradox: the length depends on the measuring scale'),
    'tb_t3_010': K(True, 'the Four Colour Theorem, for maps of connected regions in the plane',
                   needs=('one connected piece', 'flat sheet')),
    'tb_t3_011': K(True, 'Euclid'),
    'tb_t3_012': K(False, 'i is a square root of −1 in the complex numbers', needs=('in any number system',),
                   check=lambda: sp.I ** 2 == -1),
    'tb_t3_013': K(True, 'the hairy ball theorem'),
    'tb_t3_014': K(False, 'P(shared) = 1 − 365!/(342! 365^23) ≈ 0.507 > 0.5', needs=('equally likely',),
                   check=lambda: 1 - birthday() > F(1, 2)),
    'tb_t3_015': K(False, 'a Möbius strip has one side'),
    'tb_t3_016': K(False, 'Goldbach is unproved; the statement claims a proof', needs=('has been proved',)),
    'tb_t3_017': K(False, 'in ZFC, separation from a universal set gives Russell\'s paradox', needs=('ZFC',)),
    'tb_t3_018': K(False, 'Gödel: a consistent, sufficiently strong system has true unprovable statements'),
    'tb_t3_019': K(True, 'V_d / 2^d → 0', check=lambda: sp.limit(sp.pi ** (n / 2) / sp.gamma(n / 2 + 1) / 2 ** n, n, sp.oo) == 0),
    'tb_t3_020': K(False, 'e is defined exactly'),
}


def near(v, shown, places):
    """v rounded half up at `places` decimals equals shown."""
    q = sp.Rational(str(sp.N(v, 50))) * 10 ** places
    return math.floor(q + sp.Rational(1, 2)) == sp.Rational(str(shown)) * 10 ** places


def recip_beats():
    pts = [F(k, 10) for k in range(-50, 51) if k]
    return all((p > 1 / p) == (p > 1 or -1 < p < 0) for p in pts)


def sq_shrinks():
    pts = [F(k, 10) for k in range(-50, 51)]
    return all((p * p <= p) == (0 <= p <= 1) for p in pts)


def skew():
    d1, d2 = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0])
    s, t = sp.symbols('s t')
    meet = sp.solve(list(sp.Matrix([s, 0, 0]) - sp.Matrix([0, t, 1])), [s, t], dict=True)
    return d1.cross(d2) != sp.zeros(3, 1) and meet == []


def goldbach_small():
    P = set(primes_upto(10))
    return all(a in P and b in P for a, b in [(2, 2), (3, 3), (3, 5), (3, 7), (5, 5)]) and \
        [2 + 2, 3 + 3, 3 + 5, 3 + 7, 5 + 5] == [4, 6, 8, 10, 10]


# Every claim in the reveal fields, with a check that recomputes it. A snippet must appear verbatim.
FIGURES = {
    'tb_t1_002': [('10 × 0.5 = 5', lambda: 10 * F(1, 2) == 5), ('10 × −2 = −20', lambda: 10 * -2 == -20),
                  ('10 × 0.3 = 3', lambda: 10 * F(3, 10) == 3)],
    'tb_t1_004': [('(−3) × (−4) = +12', lambda: (-3) * (-4) == 12)],
    'tb_t1_006': [('√0.25 = 0.5', lambda: sp.sqrt(sp.Rational(1, 4)) == sp.Rational(1, 2)),
                  ('√1 = 1', lambda: sp.sqrt(1) == 1),
                  ('√0.09 = 0.3, and 0.3 > 0.09', lambda: sp.sqrt(sp.Rational(9, 100)) == sp.Rational(3, 10)
                   and F(3, 10) > F(9, 100))],
    'tb_t1_009': [('Area = πr²', lambda: True), ('area = π(2r)² = 4πr²', lambda: sp.expand(sp.pi * (2 * x) ** 2) == 4 * sp.pi * x ** 2),
                  ('Radius 3: area = 9π', lambda: sp.pi * 3 ** 2 == 9 * sp.pi),
                  ('Radius 6: area = 36π', lambda: sp.pi * 6 ** 2 == 36 * sp.pi)],
    'tb_t1_011': [('2n + 2m + 1 = 2(n+m) + 1', lambda: sp.expand(2 * (n + m) + 1) == 2 * n + 2 * m + 1)],
    'tb_t1_012': [('x² − 2x + 1 = 0 factorises as (x−1)² = 0', lambda: sp.factor(x ** 2 - 2 * x + 1) == (x - 1) ** 2),
                  ('only one solution: x = 1', lambda: sp.solve(x ** 2 - 2 * x + 1, x) == [1]),
                  ('x² + 1 = 0 has no real solutions', lambda: sp.solveset(xr ** 2 + 1, xr, sp.S.Reals) == sp.S.EmptySet),
                  ('positive = two solutions, zero = one, negative = none in the reals', lambda: True),
                  ('x² − 2x + 1 = 0 has exactly one solution: x = 1', lambda: sp.solve(x ** 2 - 2 * x + 1, x) == [1])],
    'tb_t1_013': [('A 1×9 rectangle (perimeter 20, area 9) vs a 5×5 square (perimeter 20, area 25)',
                   lambda: (2 * (1 + 9), 1 * 9, 4 * 5, 5 * 5) == (20, 9, 20, 25))],
    'tb_t1_014': [('8 > 3', lambda: 8 > 3), ('1/10 < 1/2, despite 10 > 2', lambda: F(1, 10) < F(1, 2) and 10 > 2)],
    'tb_t1_015': [('0.5² = 0.25', lambda: F(1, 2) ** 2 == F(1, 4)), ('0² = 0 and 1² = 1', lambda: (0 ** 2, 1 ** 2) == (0, 1)),
                  ('Every number from 0 to 1 gets smaller or stays the same when squared', sq_shrinks),
                  ('(−0.3)² = 0.09, which is bigger than −0.3', lambda: F(-3, 10) ** 2 == F(9, 100) and F(9, 100) > F(-3, 10)),
                  ('0.4² = 0.16, and 0.16 < 0.4', lambda: F(2, 5) ** 2 == F(4, 25) and F(4, 25) < F(2, 5))],
    'tb_t1_017': [('5 > 1/5', lambda: 5 > F(1, 5)), ('1/3 < 3', lambda: F(1, 3) < 3),
                  ('−0.5 is bigger than its reciprocal, −2, but −2 is smaller than its reciprocal, −0.5',
                   lambda: F(-1, 2) > 1 / F(-1, 2) and F(-2) < 1 / F(-2)),
                  ('only when it is greater than 1 or between −1 and 0', recip_beats),
                  ('Reciprocal of 0.2 is 5, and 5 > 0.2', lambda: 1 / F(1, 5) == 5 and 5 > F(1, 5))],
    'tb_t1_018': [('81 reversed is 18, and 18 = 2×9', lambda: 18 == 2 * 9),
                  ('729 reversed is 927 = 103×9', lambda: 927 == 103 * 9)],
    'tb_t1_019': [('√2 + (−√2) = 0', lambda: sp.sqrt(2) - sp.sqrt(2) == 0),
                  ('(1 + √2) + (1 − √2) = 2', lambda: sp.simplify((1 + sp.sqrt(2)) + (1 - sp.sqrt(2))) == 2)],
    'tb_t1_020': [('y = x² passes through the origin', lambda: 0 ** 2 == 0), ('y = kx', lambda: True),
                  ('y = x³ passes through the origin but 1³:2³ = 1:8', lambda: (1 ** 3, 2 ** 3) == (1, 8))],
    'tb_t2_001': [('If x = −3, then x² = 9, and √9 = 3, not −3', lambda: (-3) ** 2 == 9 and sp.sqrt(9) == 3),
                  ('√(x²) = |x|', lambda: sp.sqrt(xr ** 2) == sp.Abs(xr)),
                  ('writing √(x²) = x', lambda: sp.sqrt(xr ** 2) != xr),
                  ('x = −5: x² = 25, √25 = 5 ≠ −5', lambda: (-5) ** 2 == 25 and sp.sqrt(25) == 5)],
    'tb_t2_002': [('f(x) = x² gives f(3) = f(−3) = 9, but 3 ≠ −3', lambda: 3 ** 2 == (-3) ** 2 == 9),
                  ('f(x) = x²: f(4) = f(−4) = 16', lambda: 4 ** 2 == (-4) ** 2 == 16)],
    'tb_t2_003': [('exists at x = a', lambda: True),
                  ('|x| is continuous at x = 0 but not differentiable there (the gradient jumps from −1 to +1)',
                   lambda: sp.limit(sp.Abs(x) / x, x, 0, '-') == -1 and sp.limit(sp.Abs(x) / x, x, 0, '+') == 1)],
    'tb_t2_005': [('eˣ > x for all real x', lambda: sp.minimum(sp.exp(xr) - xr, xr, sp.S.Reals) == 1),
                  ('the tangent line at x=0 lies entirely below the curve',
                   lambda: sp.minimum(sp.exp(xr) - 1 - xr, xr, sp.S.Reals) == 0),
                  ('gives eˣ > x for all x', lambda: True)],
    'tb_t2_006': [('The x-axis (y=0, z=0) and the line x=0, z=1, y=t are skew', skew)],
    'tb_t2_007': [('P = 0 but not impossible', lambda: True)],
    'tb_t2_008': [('√2 × √2 = 2', lambda: sp.sqrt(2) ** 2 == 2), ('√3 × √3 = 3', lambda: sp.sqrt(3) ** 2 == 3)],
    'tb_t2_011': [('only defined for x > 0', lambda: True)],
    'tb_t2_012': [('correlate with r = 1 exactly', lambda: True), ('r = 0.959 (2000–2009)', lambda: True)],
    'tb_t2_013': [('|x| has none at x = 0', lambda: sp.limit(sp.Abs(x) / x, x, 0, '-') != sp.limit(sp.Abs(x) / x, x, 0, '+'))],
    'tb_t2_014': [('x³ + x + 1 = 0 always has a solution', lambda: len(sp.real_roots(x ** 3 + x + 1)) == 1)],
    'tb_t2_016': [('sin(x) = 0 whenever x = nπ', lambda: all(sp.sin(k * sp.pi) == 0 for k in range(-5, 6)))],
    'tb_t2_017': [('10/0.001 = 10,000 but 10/(−0.001) = −10,000', lambda: 10 / F(1, 1000) == 10000 and 10 / F(-1, 1000) == -10000),
                  ('1/0.001 = 1,000 but 1/(−0.001) = −1,000', lambda: 1 / F(1, 1000) == 1000 and 1 / F(-1, 1000) == -1000)],
    'tb_t2_019': [('If f’(x) = g’(x), then f(x) = g(x) + c', lambda: True),
                  ('f(x) = x² and g(x) = x² + 5 both have derivative 2x',
                   lambda: sp.diff(x ** 2, x) == sp.diff(x ** 2 + 5, x) == 2 * x)],
    'tb_t3_001': [('three 90° angles: sum = 270°', lambda: 3 * 90 == 270)],
    'tb_t3_008': [('A cube: 6+8−12=2', lambda: 6 + 8 - 12 == 2), ('A tetrahedron: 4+4−6=2', lambda: 4 + 4 - 6 == 2),
                  ('gives F+V−E=0', lambda: 2 - 2 * 1 == 0), ('A shape with two holes gives −2', lambda: 2 - 2 * 2 == -2),
                  ('F+V−E = 2−2g', lambda: True), ('A torus: F+V−E = 0', lambda: 2 - 2 * 1 == 0)],
    'tb_t3_012': [('defined by i² = −1', lambda: sp.I ** 2 == -1 and (-sp.I) ** 2 == -1)],
    'tb_t3_014': [('23 people gives >50% chance', lambda: 1 - birthday() > F(1, 2)),
                  ('a >50% chance', lambda: True),
                  ('23 people give 253 pairs', lambda: math.comb(23, 2) == 253),
                  ('(365/365)×(364/365)×...×(343/365) ≈ 0.493', lambda: near(birthday(), '0.493', 3)),
                  ('P(shared birthday) ≈ 50.7%', lambda: near(100 * (1 - birthday()), '50.7', 1))],
    'tb_t3_016': [('4=2+2, 6=3+3, 8=3+5, 10=3+7 or 5+5', goldbach_small)],
    'tb_t3_019': [('π/4 ≈ 78.5%', lambda: near(100 * sp.pi / 4, '78.5', 1)),
                  ('π/6 ≈ 52.4%', lambda: near(100 * sp.pi / 6, '52.4', 1)),
                  ('In 10 dimensions: less than 0.25%', lambda: 100 * sp.pi ** 5 / 120 / 2 ** 10 < sp.Rational(1, 4))],
    'tb_t3_020': [('e = 2.71828...', lambda: math.floor(sp.E * 10 ** 5) == 271828)],
}
# Facts that cannot be computed: each is in the text verbatim and was checked against its source.
SOURCED = {
    'tb_t2_012': [('r = 0.959', 'CRAN spuriouscorrelations 0.2 (CC0), mozzarella_consumption; r recomputed in PR #62')],
    'tb_t2_020': [('in 1874', 'Cantor, Crelle 77 (1874)'), ('of 1891', 'Cantor, Jahresbericht DMV 1 (1891)')],
    'tb_t3_009': [('about 2,800 km measured in 100 km steps, about 3,400 km in 50 km steps',
                   'Wikipedia, Coastline paradox (Richardson/Mandelbrot), checked 7 Oct 2026'),
                  ('17,820 km', 'Ordnance Survey: Great Britain 11,072.76 miles (17,820 km); Wikipedia, '
                                'Coastline of the United Kingdom, checked 7 Oct 2026')],
    'tb_t3_010': [('conjectured in 1852', 'Guthrie, 1852'), ('proved in 1976', 'Appel and Haken, 1976'),
                  ('1,936 special cases', 'Appel and Haken\'s 1,936 reducible configurations')],
    'tb_t3_016': [('up to 4×10¹⁸', 'Oliveira e Silva, Herzog and Pardi, Math. Comp. 83 (2014)'),
                  ('First proposed in 1742', 'Goldbach to Euler, 7 June 1742')],
}

# The content hash of each item when its KEYS / FIGURES entry was reviewed (see the docstring).
REVIEWED = {
    'tb_t1_001': '018efb7b75df',
    'tb_t1_002': 'f25dd054309f',
    'tb_t1_003': '42d687e0ccc0',
    'tb_t1_004': 'ae90fd5813d1',
    'tb_t1_005': 'cf643aa9a372',
    'tb_t1_006': 'f4e8f9c6fa8b',
    'tb_t1_007': '4514ca232890',
    'tb_t1_008': 'd08da9d9579f',
    'tb_t1_009': '5219a40b491f',
    'tb_t1_010': '06b0b6917599',
    'tb_t1_011': 'b8cf22dec688',
    'tb_t1_012': 'f62aa0c59cda',
    'tb_t1_013': 'cff6a4b282ba',
    'tb_t1_014': 'a82535c4ebc9',
    'tb_t1_015': '01ee754b5394',
    'tb_t1_016': 'c61097a7b865',
    'tb_t1_017': 'dff70bc18d5a',
    'tb_t1_018': 'bdeaea1c7d18',
    'tb_t1_019': '1936bb9b1667',
    'tb_t1_020': '385b5f0433f0',
    'tb_t2_001': '9bc30d157820',
    'tb_t2_002': 'c2be238c2ffa',
    'tb_t2_003': '3a911805cbc6',
    'tb_t2_004': '57644826ec2e',
    'tb_t2_005': 'b139074ff44a',
    'tb_t2_006': '70668eea7c15',
    'tb_t2_007': '1a230e42ca7b',
    'tb_t2_008': '0a2c832abc12',
    'tb_t2_009': '6f3f4e8d2d73',
    'tb_t2_010': 'fbd9dcd5b72a',
    'tb_t2_011': '74a9da13924a',
    'tb_t2_012': '0419bf8f0d07',
    'tb_t2_013': '3b633700c38e',
    'tb_t2_014': '8f5385df2c88',
    'tb_t2_015': '197d32853b8b',
    'tb_t2_016': '820cc2155338',
    'tb_t2_017': '1671c3ebf991',
    'tb_t2_018': 'd28ee1d85943',
    'tb_t2_019': '1ac17a3d73ef',
    'tb_t2_020': '1168fbc05bd8',
    'tb_t3_001': '9a869320805f',
    'tb_t3_002': 'ac875d930474',
    'tb_t3_003': '5f6862675417',
    'tb_t3_004': '51710b215e1c',
    'tb_t3_005': 'a12d1cf40da9',
    'tb_t3_006': '9c70fb47fd93',
    'tb_t3_007': 'b73c577d7931',
    'tb_t3_008': '1e1314fb4006',
    'tb_t3_009': 'c3b9ddbfa09e',
    'tb_t3_010': 'c10a2419f454',
    'tb_t3_011': '2ebf0d007378',
    'tb_t3_012': '93e99064296e',
    'tb_t3_013': '560c9f5ab2c2',
    'tb_t3_014': 'cf6e2a9e7cd2',
    'tb_t3_015': 'f7c61b4b3fd6',
    'tb_t3_016': '0503a08b239a',
    'tb_t3_017': '149ce5b1cab9',
    'tb_t3_018': 'afdb43aa0178',
    'tb_t3_019': 'fd70880004c8',
    'tb_t3_020': '9a78278d035a',
}


def where(qid):
    return '%s%s' % (qid, ' (truth-buster-%s)' % AUDIT[qid] if qid in AUDIT else '')


def check_bank(fails, bank, verbose=False):
    counts = {t: len(bank.get(t, [])) for t in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by tier, expected %s (a change needs KEYS reviewed)' % (counts, COUNTS))
    items = [q for t in COUNTS for q in bank.get(t, [])]
    ids = [q['id'] for q in items]
    for qid in sorted(set(KEYS) - set(ids)):
        fails.append('%s: in KEYS but not in the bank' % qid)
    for q in items:
        qid, w = q['id'], where(q['id'])
        k = KEYS.get(qid)
        if k is None:
            fails.append('%s: no reviewed KEYS entry (review the item and add it; never skip)' % qid)
            continue
        if REVIEWED.get(qid) != bc.content_hash(q):
            fails.append('%s: the item has changed since its entry was reviewed (re-review it, then update '
                         'REVIEWED from --print-pins)' % w)
        if q['answer'] is not k['answer']:
            fails.append('%s: keyed %s, reviewed as %s (%s)' % (w, q['answer'], k['answer'], k['why']))
        for need in k['needs']:
            if need not in q['statement']:
                fails.append('%s: the key holds only with "%s" in the statement (SR-18), which reads "%s"'
                             % (w, need, q['statement']))
        if k['check'] is not None and not k['check']():
            fails.append('%s: the check for the key (%s) fails' % (w, k['why']))
        # Figures: every claim listed, found and true; every relation sign in the fields covered.
        covered = {f: [False] * len(q.get(f, '')) for f in FIELDS}
        for snippet, check in FIGURES.get(qid, []) + [(s, None) for s, _ in SOURCED.get(qid, [])]:
            found = False
            for f in FIELDS:
                txt = q.get(f, '')
                for mt in re.finditer(re.escape(snippet), txt):
                    found = True
                    covered[f][mt.start():mt.end()] = [True] * (mt.end() - mt.start())
            if not found:
                fails.append('%s: the reviewed claim "%s" is not in the reveal' % (w, snippet))
            elif check is not None and not check():
                fails.append('%s: "%s" is false' % (w, snippet))
        for f in FIELDS:
            txt = q.get(f, '')
            for mt in re.finditer(r'[=≈≠<>]', txt):
                if not covered[f][mt.start()]:
                    a = max(0, mt.start() - 30)
                    fails.append('%s %s: "...%s..." is a claim with no check in FIGURES' % (w, f, txt[a:mt.end() + 20]))
        if verbose:
            print('  %-10s %-5s %s' % (qid, q['answer'], q['statement'][:80]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;   // the Next button's pause: nothing is advanced here
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  const items = [...QUESTIONS.tier1, ...QUESTIONS.tier2, ...QUESTIONS.tier3];
  for (const q of items) {
    const r = {id: q.id, problems: []};
    for (const said of [true, false]) {
      S.session = [q]; S.qIdx = 0; S.correct = 0; S.tierScores = [0, 0, 0];
      renderQuestion();
      if (document.getElementById('statementText').textContent !== q.statement) r.problems.push('statement not shown');
      document.getElementById(said ? 'btnTrue' : 'btnFalse').click();
      const ind = document.getElementById('revealIndicator').textContent;
      const want = said === q.answer ? '✓ Correct' : '✗ Incorrect';
      if (ind !== want) r.problems.push('pressing ' + (said ? 'Always True' : 'Not Always True') + ' shows ' + JSON.stringify(ind) + ', expected ' + JSON.stringify(want));
      if (document.getElementById('revealTitle').textContent !== q.revealTitle) r.problems.push('reveal title not the item\'s own');
      if (document.getElementById('revealText').textContent !== q.revealText) r.problems.push('reveal text not the item\'s own');
      const cb = document.getElementById('counterBox');
      if (q.counterexample && (cb.style.display === 'none' || cb.textContent !== q.counterexample)) r.problems.push('counterexample not shown');
    }
    out.push(r);
  }
  return out;
}"""


# canon 7.6.1, Jon (7 Oct 2026): on a phone, after an answer, Next is above the fold (the fixed 40px footer) and the
# whole reveal is on screen, for every item, without the student scrolling. Next's place is measured as soon as the
# answer is given (it keeps its place while it waits out its 3 s).
FIT_JS = r"""() => {
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  for (const q of [...QUESTIONS.tier1, ...QUESTIONS.tier2, ...QUESTIONS.tier3]) {
    S.session = [q]; S.qIdx = 0;
    renderQuestion(); window.scrollTo(0, 0);
    document.getElementById('btnTrue').click();
    document.getElementById('nextBtn').classList.add('visible');   // where Next is once its 3 s are up
    const nb = document.getElementById('nextBtn').getBoundingClientRect();
    const rp = document.getElementById('revealPanel').getBoundingClientRect();
    out.push([q.id, Math.round(nb.bottom), Math.round(rp.top), window.innerHeight - 40, nb.height > 0]);
  }
  return out;
}"""
# Answer once (MaffsLock; truth-buster-t3-013): both answers pressed counts the first only; at a tier boundary two Enter
# presses on Next move one question.
LOCK_JS = r"""() => {
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;   // the student has read the reveal; the window is not under test here
  startGame();
  S.qIdx = 6; renderQuestion();
  const before = S.correct;
  const q = S.session[6];
  document.getElementById(q.answer ? 'btnFalse' : 'btnTrue').click();
  document.getElementById(q.answer ? 'btnTrue' : 'btnFalse').click();
  const res = { counted: S.correct - before };
  S.revealTime = Date.now() - 4000;
  const nb = document.getElementById('nextBtn');
  nb.classList.add('visible'); nb.focus();
  return res;
}"""


def fit(fails, html, sizes=((390, 844),), strict=True):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    report = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for vw, vh in sizes:
                ctx = browser.new_context(viewport={'width': vw, 'height': vh}, has_touch=True, is_mobile=True)
                page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
                ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=html))
                page = ctx.new_page()
                page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
                page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=8000)
                page.click('.start-btn')
                rows = page.evaluate(FIT_JS)
                bad = [r for r in rows if r[1] > r[3] or r[2] < 0]
                report[(vw, vh)] = (len(rows), bad, max(r[1] for r in rows), min(r[2] for r in rows), rows[0][3])
                if strict and (vw, vh) == (390, 844):
                    for qid, bottom, top, foldline, _ in bad:
                        fails.append('%s at 390x844: after an answer %s (canon 7.6.1)' % (where(qid), (
                            'Next is under the fold (%dpx > %dpx)' % (bottom, foldline)) if bottom > foldline else
                            'the reveal starts above the screen (%dpx)' % top))
                ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return report


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
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof renderQuestion === "function"', timeout=8000)
            bank = page.evaluate('() => QUESTIONS')
            page.click('.start-btn')
            lk = page.evaluate(LOCK_JS)
            page.keyboard.press('Enter')
            page.keyboard.press('Enter')
            page.wait_for_timeout(1500)
            moved = page.evaluate('S.qIdx') - 6
            if lk['counted'] > 0:
                fails.append('both answers pressed: the second was counted (truth-buster-t3-013)')
            if moved != 1:
                fails.append('two Enter presses on Next at the tier boundary moved %d questions (truth-buster-t3-013)' % moved)
            page.reload(wait_until='load')
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof renderQuestion === "function"', timeout=8000)
            page.click('.start-btn')
            for r in page.evaluate(SWEEP_JS):
                for p in r['problems']:
                    fails.append('%s in Chromium: %s' % (where(r['id']), p))
            browser.close()
            game_errors = [e for e in errors if 'firebase' not in e.lower()]
            if game_errors:
                fails.append('page errors: %s' % '; '.join(game_errors))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def u(s):
    """A text as the page source writes it (non-ASCII as \\uXXXX)."""
    return ''.join('\\u%04x' % ord(c) if ord(c) > 126 else c for c in s)


PLANTS = [
    ('tb_t2_018', 't3-001: pi statement without "has been proved"',
     u('It has been proved that the number π contains'), u('The number π contains')),
    ('tb_t3_004', 't3-003: sphere eversion without "pass through itself"',
     u(', if it is allowed to pass through itself.'), '.'),
    ('tb_t1_015', 't3-005: "(-0.3)^2 = 0.09, smaller than 0.3"',
     u('(−0.3)² = 0.09, which is bigger than −0.3'), u('(−0.3)² = 0.09, smaller than 0.3')),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--print-pins', action='store_true', help='print REVIEWED for the current bank (after review)')
    args = ap.parse_args()

    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None and args.print_pins:
        print('REVIEWED = {')
        for t in COUNTS:
            for q in bank[t]:
                print("    '%s': '%s'," % (q['id'], bc.content_hash(q)))
        print('}')
        return 0
    if bank is not None:
        check_bank(fails, bank, args.verbose)
    measured = fit(fails, html, sizes=((390, 844), (375, 667), (320, 568)))
    for (vw, vh), (n, bad, lowest, top, foldline) in sorted(measured.items(), reverse=True):
        print('  phone fit %dx%d: %d items, Next above the fold (%dpx) on %d; lowest Next bottom %dpx; highest reveal '
              'top %dpx%s' % (vw, vh, n, foldline, n - len(bad), lowest, top, '' if (vw, vh) == (390, 844) else
                               ' (reported; Jon asked for 390x844)'))
    print('%s: %d statements, keys reviewed and pinned, %d figures recomputed, every item played in Chromium at 390px'
          % (SLUG, sum(len(bank[t]) for t in COUNTS) if bank else 0, sum(len(v) for v in FIGURES.values())))

    ok = True
    if not args.no_selftest and not args.against:
        for qid, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-58s *** CANNOT PLANT: text not found once ***' % what)
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(qid) and 'changed since' not in f]
            ok = ok and bool(hit)
            print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))

    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
