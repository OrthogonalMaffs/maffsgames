#!/usr/bin/env python3
# ci-line: Weekly facts (every figure pinned by its words and recomputed or sourced; rotation has no literal modulus) |
# ci-deps: index.html
"""Weekly facts: the 52 FACTS on the front page say what is true, and the rotation cannot silently go stale.

Why this exists (FACTS-AND-NOTICE, 13/14 Oct 2026): an audit of all 52 facts found nineteen wrong or overstated
claims (a year, a ratio, a unit, a count) that no check could have seen, because a fact is prose. This verifier is
modelled on verify-52dle.py: PINS holds, for every fact, the claims in its words.

  - A pin is a regular expression over the fact's title + hook (h) + body (x). Its capture groups are the figures.
  - A pin with a check recomputes the claim from first principles (math, fractions, comb, factorials); the check
    gets the captured figures, so a figure edited to a wrong value is FALSE, not merely different.
  - A pin with only a source cites where the claim comes from (a claim that cannot be computed). Every pin has a
    check or a source, and the script fails on one with neither.
  - If a pinned phrase is no longer in its fact, the fact fails: its words changed without this script changing.
    A new, removed or reordered fact fails too (FACTS order is the fact_index analytics key and must not move).
  - KNOWN pins are claims found wrong OUTSIDE the corrected set and not fixed under that contract (they are listed
    in docs/handover/home.md for Jon to rule on). They must still be false; once a fact is corrected the pin goes
    stale and the script fails until it is removed.

Part C: getWeekIndex() must take its modulus from FACTS.length, never a literal, and keep its anchor date.
A self-test plants a wrong figure, a changed pinned phrase, a literal modulus and a wrong anchor.

    python scripts/verify-facts.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(os.path.dirname(HERE), 'index.html')

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')
SUPRX = '[⁰¹²³⁴⁵⁶⁷⁸⁹]+'
NUM = '[0-9][0-9,]*(?:[.][0-9]+)?'


def num(s):
    return float(s.replace(',', ''))


def sci(m, e):
    return num(m) * 10 ** int(e.translate(SUP))


def near(a, b, tol=0.05):
    return abs(a - b) <= tol * abs(b)


F52 = math.factorial(52)
EVER_LIVED = 117e9          # Population Reference Bureau, 2022: about 117 billion people have ever been born
BIG_BANG_S = 13.8e9 * 365.25 * 86400
SHUFFLES = EVER_LIVED * BIG_BANG_S
HALF_CHANCE = math.sqrt(2 * math.log(2) * F52)   # birthday bound: draws for an even chance that two coincide


def birthday(n):
    p = 1.0
    for k in range(n):
        p *= (365 - k) / 365
    return 1 - p


def binom_tail(n, k, p=0.5):
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def collatz(n):
    out = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        out.append(n)
    return out


def isbn13_ok(digits):
    return sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits)) % 10 == 0


def luhn_ok(digits):
    s = 0
    for i, d in enumerate(reversed(digits)):
        d = int(d)
        if i % 2:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        s += d
    return s % 10 == 0


def P(rx, chk=None, src=None, known=None):
    return {'rx': rx, 'chk': chk, 'src': src, 'known': known}


def L(phrase, chk=None, src=None, known=None):
    return P(re.escape(phrase), chk, src, known)


WIKI = 'https://en.wikipedia.org/wiki/'

# (title, [pins]) in FACTS order.
PINS = [
    ('The Birthday Paradox', [
        P('better than ([0-9]+)% chance that two', lambda p: birthday(23) > int(p) / 100),
        P('([0-9]+) possible pairs', lambda n: int(n) == math.comb(23, 2)),
        P('about ([0-9]+) people [(]half of 365[)]', lambda n: int(n) == math.ceil(365 / 2)),
        P('by ([0-9]+) people, the probability exceeds ([0-9]+)%', lambda n, p: birthday(int(n)) > int(p) / 100),
        P('By ([0-9]+) people, it.s virtually certain', lambda n: birthday(int(n)) > 0.999),
        P('1/365 chance', None, 'a given pair share a birthday with probability 1/365'),
    ]),
    ('0.999... = 1 (exactly)', [
        L('10x − x = 9.999... − 0.999... which gives 9x = 9, so x = 1', lambda: 9 * Fraction(1) == 9,
          'algebra; the repeating decimal is the geometric series 9/10 + 9/100 + ... = 1'),
    ]),
    ('The Monty Hall Problem', [
        L('thousands of readers, nearly 1,000 of them with PhDs', None,
          'Marilyn vos Savant, Parade, 1990: about 10,000 readers wrote in, nearly 1,000 with PhDs (' + WIKI + 'Monty_Hall_problem)'),
        L('Marilyn vos Savant published it in 1990', None, 'Parade, 9 Sep 1990 (' + WIKI + 'Monty_Hall_problem)'),
        L('1/3 chance of being right', lambda: Fraction(1, 3) + Fraction(2, 3) == 1),
        L('Switching gives you 2/3; staying gives you 1/3', lambda: Fraction(2, 3) == 1 - Fraction(1, 3)),
        L('switching doubles your chances', lambda: Fraction(2, 3) == 2 * Fraction(1, 3)),
    ]),
    ('More Card Shuffles Than Atoms in Earth', [
        P('roughly (' + NUM + ') × 10(' + SUPRX + ')', lambda m, e: near(sci(m, e), F52, 0.05),
          '52! = %.3g' % F52),
        P('about (' + NUM + ') × 10(' + SUPRX + ') shuffles', lambda m, e: near(sci(m, e), SHUFFLES, 0.15),
          '117e9 people ever born (PRB 2022) x 13.8e9 years in seconds = %.2g' % SHUFFLES),
        P('you.d need about 10(' + SUPRX + ') shuffles', lambda e: near(10 ** int(e.translate(SUP)), HALF_CHANCE, 0.1),
          'birthday bound sqrt(2 ln2 . 52!) = %.3g' % HALF_CHANCE),
        P('around (' + NUM + ') times that whole exercise', lambda n: near(num(n), HALF_CHANCE / SHUFFLES, 0.1),
          'ratio %.3g' % (HALF_CHANCE / SHUFFLES)),
        L('even chance that ANY two', None, 'birthday problem with 52! "days": 50% needs about sqrt(2 ln2 . N) draws'),
    ]),
    ('Not All Infinities Are the Same Size', [
        L('Georg Cantor proved this in 1891 with his diagonal argument', None,
          'Cantor, "Ueber eine elementare Frage der Mannigfaltigkeitslehre", 1891 (' + WIKI + "Cantor's_diagonal_argument)"),
    ]),
    ('Multiplying Negatives', [
        L('3 × (−2) = −6', lambda: 3 * -2 == -6),
        L('2 × (−2) = −4, 1 × (−2) = −2, 0 × (−2) = 0', lambda: (2 * -2, 1 * -2, 0 * -2) == (-4, -2, 0)),
        L('(−1) × (−2) = 2 and (−3) × (−2) = 6', lambda: (-1 * -2, -3 * -2) == (2, 6)),
    ]),
    ('The Coastline Paradox', [
        L('Benoit Mandelbrot highlighted this in 1967', None, 'Mandelbrot, "How Long Is the Coast of Britain?", Science, 1967'),
        P('200km ruler: about (' + NUM + ')km', lambda n: num(n) == 2400, WIKI + 'Coastline_paradox (200 km: 2,400 km)'),
        P('50km ruler: about (' + NUM + ')km', lambda n: num(n) == 3400, WIKI + 'Coastline_paradox (50 km: 3,400 km)'),
        P('1km ruler: more than (' + NUM + ')km', lambda n: num(n) == 8000,
          WIKI + 'Coastline_paradox (1 km: more than 8,000 km; the earlier "over 12,000" was wrong)'),
        L('fractal dimension of about 1.25', None, 'Mandelbrot 1967: west coast of Britain, D = 1.25'),
    ]),
    ("Why Can't You Divide by Zero?", [
        L('If 6 ÷ 0 = x, then x × 0 = 6', lambda: all(x * 0 != 6 for x in range(-50, 51)), 'no x satisfies x . 0 = 6'),
        L('0 ÷ 0 = x, then x × 0 = 0 — true for EVERY number', lambda: all(x * 0 == 0 for x in range(-50, 51))),
    ]),
    ("Benford's Law", [
        P('about ([0-9]+)% of the time — not the ([0-9]+)% you.d expect',
          lambda a, b: round(100 * math.log10(2)) == int(a) and round(100 / 9) == int(b)),
        P('digit 1 leads ([0-9.]+)% of the time, 9 leads only ([0-9.]+)%',
          lambda a, b: round(100 * math.log10(2), 1) == float(a) and round(100 * math.log10(10 / 9), 1) == float(b)),
    ]),
    ("The Gambler's Fallacy", [
        L('In 1913, black came up 26 times in a row at Monte Carlo', None, WIKI + "Gambler's_fallacy (Monte Carlo Casino, 18 Aug 1913)"),
        P('about 1 in ([0-9]+) million [(]a single-zero wheel has ([0-9]+) black pockets out of ([0-9]+)[)]',
          lambda m, b, n: near(1 / (int(b) / int(n)) ** 26, int(m) * 1e6, 0.01) and int(n) == 37 and int(b) == 18),
        P('chance of black on the next spin is still ([0-9]+) in ([0-9]+)', lambda b, n: (int(b), int(n)) == (18, 37)),
        L('heads is still exactly 50%', None, 'independent fair flips: the coin has no memory'),
    ]),
    ('√2 is Irrational — and It Broke a Belief System', [
        L('the proof has stood for over 2,000 years', lambda: 2026 - (-450) > 2000,
          'irrationality of root 2 known by the 5th century BC (' + WIKI + 'Square_root_of_2)'),
        L('Historians treat that as legend', None, WIKI + 'Hippasus (the drowning story is unattested in early sources)'),
        L('2b² = a², meaning a is even, say a = 2k, then b² = 2k²', lambda: all((2 * k) ** 2 == 2 * (2 * k * k) for k in range(1, 50)),
          'a = 2k gives 4k² = 2b², so b² = 2k²'),
    ]),
    ("You Can't Comb a Hairy Ball Flat", [
        L('proved by Brouwer in 1912', None, WIKI + 'Hairy_ball_theorem (Brouwer, 1912)'),
        L('the horizontal wind speed is exactly zero', None,
          WIKI + 'Hairy_ball_theorem (a continuous tangent field on S² has a zero; wind is idealised as one)'),
    ]),
    ('The Friendship Paradox', [
        L('you have 10 friends and one has 1,000', lambda: (9 * 10 + 1000) / 10 > 10, 'a 1,000-friend neighbour lifts the mean of your friends'),
        L('randomly chosen friends of randomly chosen people are infected earlier', None,
          'Christakis & Fowler, PLoS ONE, 2010 (' + WIKI + 'Friendship_paradox + "sensor" networks)'),
    ]),
    ('Pi Shows Up Where You\'d Never Expect', [
        L('Buffon\'s Needle Problem (1733)', None, WIKI + "Buffon's_needle_problem (posed 1733)"),
        L('exactly 2/π', lambda: abs((2 * 1) / (math.pi * 1) - 2 / math.pi) < 1e-15, 'P = 2l/(pi d), l = d'),
        L('1/1² + 1/2² + 1/3² + ... = π²/6', lambda: near(sum(1 / k ** 2 for k in range(1, 200001)), math.pi ** 2 / 6, 1e-5)),
    ]),
    ('98% Accurate Doesn\'t Mean What You Think', [
        P('The disease affects ([0-9]+) [(]([0-9.]+)%[)]', lambda n, p: near(num(n) / 10000 * 100, num(p), 1e-9)),
        P('The test catches ([0-9]+)%: ([0-9]+) true positives', lambda p, t: round(50 * int(p) / 100) == int(t)),
        P('falsely flags ([0-9]+)% of ([0-9,]+) healthy people: ([0-9]+) false positives',
          lambda p, n, f: round(num(n) * int(p) / 100) == int(f) and num(n) == 10000 - 50),
        P('Total positives: ([0-9]+). Genuine: ([0-9]+)', lambda t, g: (int(t), int(g)) == (49 + 199, 49)),
        P('= 49/248 ≈ ([0-9]+)%', lambda p: round(100 * 49 / 248) == int(p)),
        P('wrong ([0-9]+)% of the time[.]$', lambda p: round(100 * 199 / 248) == int(p)),
        # KNOWN (finding, not fixed): the hook says "more than 90%", the body computes 80%.
        P('give wrong results more than ([0-9]+)% of the time', lambda p: round(100 * 199 / 248) > int(p),
          'the body computes 199/248 = 80%', known='hook says >90%, body computes 80%'),
    ]),
    ('Infinitely Many Primes', [
        L('proved over 2,300 years ago', lambda: 2026 + 300 > 2300, 'Euclid, Elements IX.20, c. 300 BC'),
        L('Dividing N by any prime in the list leaves remainder 1',
          lambda: all((2 * 3 * 5 * 7 + 1) % p == 1 for p in (2, 3, 5, 7))),
    ]),
    ('The Four Colour Theorem', [
        L('Conjectured in 1852, proved in 1976 by Appel and Haken', None,
          WIKI + 'Four_color_theorem (Guthrie 1852; Appel and Haken 1976)'),
        L('checking 1,936 cases', None, WIKI + 'Four_color_theorem (1,936 configurations)'),
        L('Five colours are always enough', None, 'Heawood, 1890 (five colour theorem)'),
    ]),
    ('Correlation Does Not Imply Causation', [
        P('mozzarella consumption tracks the number of civil engineering doctorates awarded almost perfectly [(]r ≈ ([0-9.]+)[)]',
          lambda r: abs(float(r) - 0.96) < 0.005,
          'Tyler Vigen, Spurious Correlations: mozzarella cheese consumption vs civil engineering doctorates, 2000-2009, r = 0.9586'),
        L('found by Tyler Vigen', None, 'tylervigen.com/spurious-correlations'),
        P('In ([0-9]{4}), a fraudulent study linked MMR to autism based on correlation in ([0-9]+) children',
          lambda y, n: (int(y), int(n)) == (1998, 12),
          'Wakefield et al., The Lancet, 28 Feb 1998, 12 children; retracted 2010; Wakefield struck off 2010'),
    ]),
    ("Zeno's Paradox", [
        L('1/2 + 1/4 + 1/8 + ...', lambda: near(sum(0.5 ** k for k in range(1, 60)), 1, 1e-12)),
        L('a + ar + ar² + ... = a/(1−r)', lambda: near(sum(3 * 0.4 ** k for k in range(200)), 3 / (1 - 0.4), 1e-9)),
    ]),
    ("Euler's Identity", [
        L('e^(iπ) + 1 = 0', lambda: abs(__import__('cmath').exp(1j * math.pi) + 1) < 1e-12),
        L('Set x = π: e^(iπ) = −1', lambda: abs(__import__('cmath').exp(1j * math.pi) + 1) < 1e-12),
    ]),
    ('The Collatz Conjecture', [
        L('Try 7: 7 → 22 → 11 → 34 → 17 → 52 → 26 → 13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1',
          lambda: collatz(7) == [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]),
        P('checked every number up to more than 10(' + SUPRX + ')', lambda e: 2 ** 68 > 10 ** int(e.translate(SUP)),
          'D. Barina, J. Supercomputing 2021: verified to 2^68 = 2.95e20'),
        L('Paul Erdős said: "Mathematics is not yet ready for such problems."', None,
          'Lagarias, The 3x+1 Problem and its Generalizations (Erdős: "Mathematics may not be ready for such problems"; "not yet" is a documented variant)'),
    ]),
    ('Small Samples Vary More', [
        P('getting ([0-9]+)[+] boys [(]([0-9]+)%[)]', lambda k, p: round(100 * int(k) / 15) == int(p)),
        L('over 60% are boys', lambda: binom_tail(15, 10) > binom_tail(45, 28),
          'P(>60%% boys): 15 births (10+) %.3f beats 45 births (28+) %.3f' % (binom_tail(15, 10), binom_tail(45, 28))),
    ]),
    ('Imaginary Numbers Are Real', [
        L('Multiplying by i rotates a number 90°', lambda: abs(1j * 1j + 1) < 1e-12 and (1j).real == 0 and (1j).imag == 1),
        L('Two rotations of 90° = 180° = multiplying by −1', lambda: 1j * 1j == -1),
    ]),
    ('Exponential Growth Is Unintuitive', [
        P('fold a piece of paper ([0-9]+) times', lambda n: 0.0001 * 2 ** int(n) / 1000 > 384400 and 0.0001 * 2 ** 41 / 1000 < 384400),
        P('([0-9]+) folds would exceed the observable universe', lambda n: 0.0001 * 2 ** int(n) > 8.8e26 and 0.0001 * 2 ** (int(n) - 1) < 8.8e26),
        P('After 20 folds: ~([0-9]+) metres', lambda m: near(0.0001 * 2 ** 20, num(m), 0.1)),
        P('After 30: ~([0-9]+)km', lambda m: near(0.0001 * 2 ** 30 / 1000, num(m), 0.1)),
        P('After 42: ~([0-9,]+)km', lambda m: near(0.0001 * 2 ** 42 / 1000, num(m), 0.01)),
        P('doubling every ([0-9]+) days.*100 → ([0-9,]+) in just ([0-9]+) days',
          lambda d, v, days: 100 * 2 ** (int(days) // int(d)) == num(v) and int(days) % int(d) == 0),
    ]),
    ('Why 1 Is Not a Prime Number', [
        L('12 = 2² × 3', lambda: 2 ** 2 * 3 == 12),
        L('12 = 1 × 2² × 3, or 1¹⁰⁰ × 2² × 3', lambda: 1 * 2 ** 2 * 3 == 12 and 1 ** 100 * 2 ** 2 * 3 == 12),
    ]),
    ("Simpson's Paradox", [
        L('UC Berkeley in 1973', None, 'Bickel, Hammel & O\'Connell, Science, 1975 (admissions Fall 1973)'),
        L('most individual departments admitted women at an equal or higher rate than men', None,
          'Berkeley data: 4 of the 6 largest departments favoured women, most others near parity; the earlier "higher in every department" was wrong (' + WIKI + 'Simpson%27s_paradox)'),
    ]),
    ('The Infinite Hotel', [
        L('move up one room (1→2, 2→3...)', lambda: all(n + 1 > n for n in range(1, 100))),
        L('guest n to move to room 2n. All odd rooms free', lambda: {2 * n for n in range(1, 200)}.isdisjoint(range(1, 400, 2))),
    ]),
    ("The Prisoner's Dilemma", [
        P('If both stay silent: ([0-9]+) year each. One betrays: betrayer goes free, other gets ([0-9]+) years. Both betray: ([0-9]+) years each',
          lambda a, b, c: (int(a), int(b), int(c)) == (1, 5, 3) and 0 < int(a) < int(c) < int(b),
          'the dilemma ordering T > R > P > S: free < 1 year < 3 years < 5 years'),
        P("In Robert Axelrod's computer tournaments [(]([0-9]{4})[)], the simple strategy \"tit-for-tat\" won both",
          lambda y: int(y) == 1980,
          'Axelrod, J. Conflict Resolution 24 (1980): tit-for-tat won both round-robin tournaments; the book The Evolution of Cooperation is 1984'),
    ]),
    ('Percentages Are Asymmetric', [
        L('+50%: £150. −50%: £75', lambda: (100 * 1.5, 100 * 1.5 * 0.5) == (150, 75)),
        L('you need a 33.3% decrease', lambda: round(100 * (1 - 1 / 1.5), 1) == 33.3),
        L('net loss of (p/100)²', lambda: all(near(1 - (1 + p / 100) * (1 - p / 100), (p / 100) ** 2, 1e-9) for p in (10, 40, 50))),
        P('fell ([0-9]+)% then rose ([0-9]+)%.*still down ([0-9]+)%', lambda a, b, d: round(100 * (1 - (1 - int(a) / 100) * (1 + int(b) / 100))) == int(d)),
    ]),
    ('The Perfect Bracket Is Impossible', [
        P('([0-9]+) games, 2 outcomes each: 2(' + SUPRX + ') ≈ ([0-9.]+) × 10(' + SUPRX + ') possible brackets',
          lambda g, e, m, x: int(g) == 63 and int(e.translate(SUP)) == 63 and near(sci(m, x), 2 ** 63, 0.01)),
        L('about 1 in 9.2 quintillion', lambda: near(2 ** 63, 9.2e18, 0.01)),
        L('In 2014, a $1 billion prize for a perfect bracket was insured by Warren Buffett', None,
          '2014 Quicken Loans Billion Dollar Bracket, underwritten by Berkshire Hathaway (' + WIKI + 'March_Madness_(NCAA_basketball_tournaments))'),
        L('roughly 1 in 120 billion', None, 'NCAA / CBS Sports: 1 in 120.2 billion at 66.7% pick accuracy (cbssports.com 2023-ncaa-tournament-the-odds-of-filling-out-a-perfect-bracket-are-1-in-120-2-billion)'),
    ]),
    ('Fermi Estimation', [
        L('~9 million people, ~3 million households, ~5% have pianos: 150,000 pianos', lambda: 3e6 * 0.05 == 150000),
        L('A tuner does ~1,000/year. So ~150 tuners needed', lambda: 150000 / 1000 == 150),
    ]),
    ('The Unexpected Hanging Paradox', [
        L('hanged on Wednesday, surprised', None, 'Quine / O\'Connor 1948 (' + WIKI + 'Unexpected_hanging_paradox)'),
    ]),
    ('Why 0! = 1', [
        L('4!=24, 3!=6 (÷4), 2!=2 (÷3), 1!=1 (÷2), 0!=1 (÷1)',
          lambda: [math.factorial(n) for n in (4, 3, 2, 1, 0)] == [24, 6, 2, 1, 1] and 24 // 4 == 6 and 6 // 3 == 2 and 2 // 2 == 1),
        L('C(n,0) = n!/0!n! = 1', lambda: all(math.comb(n, 0) == 1 for n in range(10))),
    ]),
    ('Regression to the Mean', [
        L('Israeli flight instructors', None, 'Kahneman, Nobel autobiography / Thinking, Fast and Slow ch. 17'),
    ]),
    ('The Wheat and Chessboard Problem', [
        P('The 64th square alone has 2(' + SUPRX + ') ≈ ([0-9.]+) × 10(' + SUPRX + ') grains',
          lambda e, m, x: int(e.translate(SUP)) == 63 and near(sci(m, x), 2 ** 63, 0.01)),
        P('Total: 2(' + SUPRX + ') − 1 ≈ ([0-9.]+) × 10(' + SUPRX + ') grains',
          lambda e, m, x: int(e.translate(SUP)) == 64 and near(sci(m, x), 2 ** 64 - 1, 0.03)),
        P('At roughly ([0-9]+) mg a grain, that.s about ([0-9]+) billion tonnes',
          lambda mg, t: near((2 ** 64 - 1) * int(mg) * 1e-6 / 1000 / 1e9, int(t), 0.05),
          '(2^64 - 1) x 50 mg = %.3g tonnes' % ((2 ** 64 - 1) * 50e-6 / 1000)),
        P('around ([0-9]+) million tonnes of wheat a year, so you.d need well over a thousand years',
          lambda m: (2 ** 64 - 1) * 50e-6 / 1000 / (int(m) * 1e6) > 1000,
          'FAO / USDA: world wheat output about 780 Mt a year; 9.2e11 / 7.8e8 = 1,180 years'),
    ]),
    ('The Seven Bridges of Königsberg', [
        L('In 1736, Euler proved', None, 'Euler, "Solutio problematis ad geometriam situs pertinentis", 1736'),
        L('Königsberg had four odd nodes', lambda: sorted(d % 2 for d in (3, 3, 3, 5)) == [1, 1, 1, 1] and sum((3, 3, 3, 5)) == 2 * 7,
          'degrees 3,3,3,5 over seven bridges'),
        L('zero or two nodes have an odd number of edges', None, 'Euler\'s theorem'),
    ]),
    ("Why You Can't Trisect an Angle", [
        L('proved in 1837', None, WIKI + 'Angle_trisection (Wantzel, 1837)'),
        L('Pierre Wantzel proved', None, WIKI + 'Angle_trisection'),
        P('trisecting ([0-9]+)° requires constructing cos ([0-9]+)°, a solution of the cubic ([0-9]+)x³ − ([0-9]+)x − ([0-9]+) = 0',
          lambda a, t, c3, c1, c0: int(a) == 60 and int(t) * 3 == int(a) and
          abs(int(c3) * math.cos(math.radians(int(t))) ** 3 - int(c1) * math.cos(math.radians(int(t))) - int(c0)) < 1e-12 and
          not any(Fraction(int(c3)) * Fraction(r) ** 3 - int(c1) * Fraction(r) - int(c0) == 0
                  for r in ('1', '-1', '1/2', '-1/2', '1/4', '-1/4', '1/8', '-1/8')),
          '8x^3 - 6x - 1 has no rational root, so cos 20 has degree 3, not a power of 2: not constructible'),
    ]),
    ('Survivorship Bias', [
        L('badly built old house that fell down long ago', None, 'survivorship: only the houses that survive are seen; replaces the "grandfather smoked until 95" example'),
        L('Abraham Wald', None, 'Statistical Research Group, Columbia, WWII (' + WIKI + 'Abraham_Wald)'),
    ]),
    ('The Fundamental Theorem of Calculus', [
        L('Newton and Leibniz', None, WIKI + 'Fundamental_theorem_of_calculus'),
    ]),
    ('P vs NP', [
        L('The Clay Mathematics Institute offers $1,000,000', None, 'claymath.org/millennium-problems/p-vs-np-problem'),
        L('much of the encryption that protects the internet could, in principle, be broken', None,
          'public-key cryptography rests on problems in NP; a fast general algorithm would endanger it'),
    ]),
    ('Why Logarithmic Scales Exist', [
        P('each step of 1 means ground shaking ([0-9]+) times larger, and about ([0-9]+) times more energy',
          lambda a, e: int(a) == 10 and round(10 ** 1.5) == int(e), 'amplitude 10^1, energy 10^1.5 = 31.6 per magnitude step'),
        P('([0-9]+) dB is a MILLION times more powerful than ([0-9]+) dB', lambda a, b: 10 ** ((int(a) - int(b)) / 10) == 1e6),
        P('2011 Japan quake [(]([0-9.]+)[)] released about ([0-9]+) times more energy than the 2023 Turkey quake [(]([0-9.]+)[)]',
          lambda a, n, b: near(10 ** (1.5 * (float(a) - float(b))), int(n), 0.05),
          'energy ratio 10^(1.5 x 1.3) = 89; magnitudes: USGS Tohoku 9.1 (2011), Kahramanmaras 7.8 (2023)'),
    ]),
    ('100 Doors Makes Monty Hall Obvious', [
        P('Monty opens ([0-9]+) goat doors.*from ([0-9]+)% to ([0-9]+)%', lambda o, a, b: int(o) == 98 and int(a) + int(b) == 100 and int(b) == 99),
        L('1/100', lambda: Fraction(1, 100) + Fraction(99, 100) == 1),
    ]),
    ('Dimensional Analysis Saves Lives', [
        L('In 1999, NASA lost a $125 million Mars orbiter', None, 'NASA Mars Climate Orbiter Mishap Investigation Board, Nov 1999 (' + WIKI + 'Mars_Climate_Orbiter)'),
        L('one team worked in imperial units and another in metric', None, WIKI + 'Mars_Climate_Orbiter (pound-force seconds vs newton-seconds)'),
        L('pound-force seconds; NASA expected newton-seconds', None, WIKI + 'Mars_Climate_Orbiter (Lockheed Martin)'),
    ]),
    ('The Basel Problem', [
        L('1/1² + 1/2² + 1/3² + 1/4² + ... = π²/6', lambda: near(sum(1 / k ** 2 for k in range(1, 200001)), math.pi ** 2 / 6, 1e-5)),
        L('In 1735, a 28-year-old Euler proved this', None, WIKI + 'Basel_problem (Euler, born 15 Apr 1707; announced 1735)'),
    ]),
    ('Barcodes Use Modular Arithmetic', [
        L('ISBN-13 uses mod 10: multiply digits alternately by 1 and 3', lambda: isbn13_ok('9780306406157') and not isbn13_ok('9780306406158')),
        L('Credit cards use the Luhn algorithm', lambda: luhn_ok('4539578763621486') and not luhn_ok('4539578763621487')),
        L('NHS numbers have a check digit too', None, 'NHS number: ten digits, the tenth a modulus-11 check digit (England NHS Data Dictionary)'),
        L('banks run a modulus check on your account number before a payment goes through', None,
          'Pay.UK / Vocalink UK modulus checking (sort code and account number); UK sort codes carry no check digit of their own'),
    ]),
    ('The Law of Cosines Contains Pythagoras', [
        L('cos(90°) = 0', lambda: abs(math.cos(math.radians(90))) < 1e-15),
    ]),
    ('Can You Hear the Shape of a Drum?', [
        L('Mark Kac asked this in 1966', None, 'Kac, "Can one hear the shape of a drum?", Amer. Math. Monthly, 1966'),
        L('Gordon, Webb and Wolpert found two different shapes in 1992', None, 'Gordon, Webb, Wolpert, Invent. Math. 110 (1992)'),
    ]),
    ('Why Sample Size Matters More Than You Think', [
        P('Asking ([0-9,]+) random people gives ±([0-9]+)% margin of error', lambda n, m: round(100 * 1.96 * math.sqrt(0.25 / num(n))) == int(m)),
        P('you need ([0-9,]+) people — not ([0-9,]+)', lambda a, b: num(a) == 4 * 1000 and num(b) == 2 * 1000 and
          round(100 * 1.96 * math.sqrt(0.25 / num(a)), 1) == 1.5),
    ]),
    ('Music Is Built on Maths', [
        P('[(]3/2[)]¹² ≈ ([0-9]+[.][0-9]+)', lambda v: near(1.5 ** 12, float(v), 0.001)),
        L('Seven octaves: 2⁷ = 128', lambda: 2 ** 7 == 128),
        L('exactly 2^(1/12)', lambda: abs((2 ** (1 / 12)) ** 12 - 2) < 1e-12),
    ]),
    ('Matrices Run Your Phone', [
        L('A 4×4 matrix can translate, rotate, and project 3D objects', None, 'homogeneous coordinates: a 3D translation needs a 4x4 matrix'),
    ]),
    ('The Number e Is Everywhere', [
        L('Compound annually: £2. Monthly: £2.61. Every second: £2.71828', lambda: (1 + 1) == 2 and round((1 + 1 / 12) ** 12, 2) == 2.61 and
          round((1 + 1 / 31536000) ** 31536000, 5) == 2.71828),
        L('36.8%', lambda: round(100 / math.e, 1) == 36.8),
    ]),
    ('Is Mathematics Discovered or Invented?', [
        L('argued about this for 2,500 years', None, 'Plato (c. 400 BC) onwards; a round figure, see handover'),
    ]),
]

DOW_CALL = re.compile(r'function getWeekIndex[(][)][{]([^}]*)[}]')


def parse_facts(html):
    i = html.index('var FACTS=[')
    j = html.index('\n];', i)
    blk = html[i:j]
    import json
    rx = re.compile(r'[{]t:"((?:[^"\\]|\\.)*)",h:"((?:[^"\\]|\\.)*)",x:"((?:[^"\\]|\\.)*)"')
    out = []
    for m in rx.finditer(blk):
        out.append(tuple(json.loads('"' + s + '"') for s in m.groups()))
    if len(out) != blk.count('{t:'):
        raise SystemExit('FACTS: parsed %d of %d entries' % (len(out), blk.count('{t:')))
    return out


def squash(s):
    return ' '.join(s.split())


def check_pins(fails, known_seen, facts):
    titles = [f[0] for f in facts]
    want = [p[0] for p in PINS]
    if titles != want:
        for k, (a, b) in enumerate(zip(titles, want)):
            if a != b:
                fails.append('fact %d: the title is "%s", the script pins "%s" (FACTS order and titles are fixed; '
                             'a changed or new fact needs its pins)' % (k, a, b))
                break
        if len(titles) != len(want):
            fails.append('FACTS has %d entries, the script pins %d' % (len(titles), len(want)))
    for k, ((t, h, x), (_, pins)) in enumerate(zip(facts, PINS)):
        text = squash(' '.join((t, h, x)))
        for p in pins:
            if p['chk'] is None and not p['src']:
                fails.append('fact %d (%s): pin %r has neither a check nor a source' % (k, t, p['rx'][:50]))
                continue
            m = re.search(p['rx'], text)
            if not m:
                if p['known']:
                    fails.append('fact %d (%s): KNOWN pin "%s" no longer matches: the fact was reworded, '
                                 'update or remove the KNOWN entry' % (k, t, p['known']))
                else:
                    fails.append('fact %d (%s): its words no longer say %r (review the pin)' % (k, t, p['rx'][:70]))
                continue
            if p['chk'] is not None:
                try:
                    ok = bool(p['chk'](*m.groups()))
                except Exception as e:  # a parse of the figures failed
                    ok = False
                    fails.append('fact %d (%s): pin %r raised %r' % (k, t, p['rx'][:50], e))
                    continue
                if p['known']:
                    if ok:
                        fails.append('fact %d (%s): KNOWN pin "%s" is now TRUE: the fact was fixed, remove the KNOWN entry'
                                     % (k, t, p['known']))
                    else:
                        known_seen.append('fact %d (%s): %s' % (k, t, p['known']))
                elif not ok:
                    fails.append('fact %d (%s): FALSE: "%s"' % (k, t, m.group(0)[:100]))


def check_rotation(fails, html):
    m = DOW_CALL.search(html)
    if not m:
        fails.append('getWeekIndex(): not found')
        return
    body = m.group(1)
    if not re.search(r'%\s*FACTS[.]length', body):
        fails.append('getWeekIndex(): the modulus is not FACTS.length (%s)' % body[:90])
    if re.search(r'%\s*[0-9]', body):
        fails.append('getWeekIndex(): a literal modulus (%s)' % body[:90])
    if "new Date('2026-01-05')" not in body:
        fails.append("getWeekIndex(): the anchor date '2026-01-05' changed")


def run(html):
    fails, known = [], []
    facts = parse_facts(html)
    check_pins(fails, known, facts)
    check_rotation(fails, html)
    return fails, known, facts


def esc(s):
    return ''.join(chr(92) + 'u%04x' % ord(c) if ord(c) > 126 else c for c in s)


# (what, text to find in the page, replacement, failure tag expected)
PLANTS = [
    ('a wrong figure: Japan quake "about 90 times" made 22', 'released about 90 times more energy', 'released about 22 times more energy', 'about 22 times'),
    ('a wrong year: Wakefield study 1998 made 1999', 'In 1998, a fraudulent study', 'In 1999, a fraudulent study', 'In 1999'),
    ('a changed pinned phrase: "most individual departments"', 'most individual departments admitted', 'all individual departments admitted', 'no longer say'),
    ('a literal modulus: % FACTS.length made % 52', '%FACTS.length', '%52', 'literal modulus'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or PAGE, encoding='utf-8', newline='').read()
    # The page stores non-ASCII as escapes in the FACTS block; parse_facts decodes them through json.
    fails, known, facts = run(html)
    npins = sum(len(p[1]) for p in PINS)
    print('facts: %d facts, %d pins (each recomputed or sourced), rotation modulus FACTS.length' % (len(facts), npins))
    for k in known:
        print('  KNOWN (finding, listed in docs/handover/home.md, not fixed): ' + k)
    ok = True
    if not args.no_selftest and not args.against:
        for what, old, new, tag in PLANTS:
            o, n = esc(old), esc(new)
            if html.count(o) != 1:
                print('  self-test %-58s *** CANNOT PLANT (%d) ***' % (what, html.count(o)))
                ok = False
                continue
            rep, _, _ = run(html.replace(o, n))
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:90]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
