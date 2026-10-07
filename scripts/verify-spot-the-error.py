#!/usr/bin/env python3
"""Spot the Error: every worked step, key, phrase and explanation checked, and every item played in Chromium.

The game (110 items: ks3 35, gcse 45, level4 30) shows a word problem and some worked steps. Stage 1: the
student taps the step that contains the error; Stage 2: the phrase in the problem that was misread. Its bank
was written by hand and never verified; the tranche 1 audit of 6 Oct 2026 found a correct step keyed as the
error (gcse_044), steps with no false maths keyed as the error (ks3_016, l4_023: SR-18, a strategy choice is
not an error), a true statement keyed while a false one was marked correct (gcse_020), a second false step
marked correct (l4_002), a wrong Stage 2 key (ks3_024), explanations that teach a wrong answer (ks3_019) or
use a number the question never gave (ks3_025), and hand-typed figures that were wrong (gcse_006).

The model every item is held to: the key is the FIRST step that departs from correct working; every step
before it is correct; the steps after it carry the error forward, so they are held only to their own
arithmetic. The bank is read from the live page, then:

  Arithmetic. Every "A = B = C" chain of numbers in every step and every explanation is evaluated exactly
    (SymPy; a written decimal must be its left side rounded half up at the places written; units are
    converted where both sides carry one). Any false link outside the key step FAILS: a second false step
    (l4_002), or an explanation figure that is wrong (gcse_006, canon: verifiers recompute explanation
    figures, not just keys).
  The key. ITEMS below holds a reviewed entry per item: the key step, the misread phrase, the true answer
    and, for each step up to the key, what is true at that step: a number computed from the question's own
    figures (the step's written value must equal it before the key and must not at the key), or a reviewed
    verdict with its reason (and a SymPy or arithmetic check where one exists). So a key step that states a
    true value FAILS (gcse_044), as does a correct step before the key that is wrong.
  The answer. Each explanation must state the item's true answer, computed in ITEMS from numbers in the
    question (a number the question does not give FAILS: ks3_025).
  Stage 2. Exactly one phrase is the misreading, and it is the pinned one (ks3_024); every phrase appears
    in the problem.
  Shape. Steps numbered 1..n, the key among them, exactly the key marked correct:false.
  Chromium (390x844). Every item is shown through the game's own showStage1/showStage2: every step card and
    tappable phrase is on screen with its own text; a wrong step and a wrong phrase are not marked correct
    and do not advance; the key step and the misread phrase are marked correct; the explanation shown is the
    item's own. Nothing is submitted (the session is never finished) and every request off the stub server
    is aborted.

An item in the bank with no ITEMS entry, or an entry with no item, FAILS: review it and add it, never skip.
A self-test plants three of the audit's own faults back into a copy of the page (gcse_044's equivalent arc
formula as the key, l4_002's log 12 - log 2 = log 10 as a correct step, ks3_024's Stage 2 key on the wrong
phrase); each must FAIL naming its item through a check other than the REVIEWED pin. It runs unless
--no-selftest.

    python scripts/verify-spot-the-error.py [--verbose] [--no-selftest] [--against FILE]

--against FILE serves FILE as the game page (e.g. main's copy, to show the check fails on it).
"""
import argparse
import math
import os
import re
import sys
from fractions import Fraction

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'spot-the-error'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'ks3': 35, 'gcse': 45, 'level4': 30}
# Register entries (docs/audits/findings/spot-the-error.yml) by bank item, so a failure names the finding.
AUDIT = {
    'ste_ks3_019': 't1-001', 'ste_ks3_024': 't1-002', 'ste_ks3_016': 't1-003', 'ste_gcse_044': 't1-004',
    'ste_gcse_020': 't1-005', 'ste_gcse_001': 't1-006', 'ste_gcse_027': 't1-007', 'ste_gcse_006': 't1-008',
    'ste_l4_002': 't1-009', 'ste_l4_023': 't1-010', 'ste_gcse_028': 't1-011, t1-016', 'ste_gcse_031': 't1-012, t1-017',
    'ste_ks3_025': 't1-013', 'ste_ks3_012': 't1-015', 'ste_l4_024': 't1-018', 'ste_gcse_009': 't1-019',
}

# ---------------------------------------------------------------------------------------------------------
# Reading numbers out of the steps
# ---------------------------------------------------------------------------------------------------------
SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')
VULGAR = {'½': '1/2', '¼': '1/4', '¾': '3/4', '⅓': '1/3', '⅙': '1/6'}
FUNCS = r'\b(sqrt|pi|sin|cos|tan|asin|acos|atan|log|rad|deg|binomial|factorial)\b'
LOC = {'rad': lambda d: d * sp.pi / 180, 'deg': lambda r: r * 180 / sp.pi, 'sqrt': sp.sqrt,
       'binomial': sp.binomial, 'factorial': sp.factorial, 'pi': sp.pi, 'sin': sp.sin, 'cos': sp.cos,
       'tan': sp.tan, 'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan, 'log': lambda v: sp.log(v, 10)}
UNITS = (r'(?:\s*(?:cm²|m²|cm|mm|km/h|km|ml|m/s|m|kg|g|litres?|miles per litre|miles|hours|seconds|days|'
         r'years|times heavier|students|seats|parts|%|°))+$')
SCALE = {'mm': sp.Rational(1, 1000), 'cm': sp.Rational(1, 100), 'm': 1, 'km': 1000,
         'ml': sp.Rational(1, 1000), 'litre': 1, 'litres': 1}


def norm(s):
    """A step's text as SymPy syntax: £, thousands commas, ×, ÷, −, superscripts, √, π, %, nCr, degrees."""
    s = s.replace('−', '-').replace('×', '*').replace('÷', '/').replace('·', '*').replace('£', '')
    for _ in range(2):
        s = re.sub(r'(\d),(\d{3})(?!\d)', r'\1\2', s)
    for ch, frac in VULGAR.items():
        s = re.sub(r'(\d)' + ch, r'(\1+' + frac + ')', s).replace(ch, '(' + frac + ')')
    s = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)', lambda m: '**(' + m.group(1).translate(SUP) + ')', s)
    s = re.sub(r'(\d+(?:\.\d+)?)% of', r'(\1/100)*', s)
    s = re.sub(r'(\d+/\d+) of', r'(\1)*', s)
    s = re.sub(r'(\d+)C(\d+)', r'binomial(\1,\2)', s)
    s = re.sub(r'(\d+)!', r'factorial(\1)', s)
    s = s.replace('√(', 'sqrt(')
    s = re.sub(r'√(\d+(?:\.\d+)?)', r'sqrt(\1)', s)
    s = s.replace('π', 'pi')
    s = re.sub(r'(sin|cos|tan)\s*\(?\s*(-?\d+(?:\.\d+)?)\s*°\s*\)?', r'\1(rad(\2))', s)
    s = re.sub(r'arc(sin|cos|tan)\(([^)]*)\)', r'deg(a\1(\2))', s)
    s = re.sub(r'(\d)\s*(sqrt|pi|\()', r'\1*\2', s)
    return s.replace('°', '')


def value(seg):
    """The exact value of a segment that is purely numeric (units allowed), else None."""
    t = seg.strip().strip('\'"').rstrip('.,').strip()
    t = re.sub(r'(sin|cos|tan)\s*\(?\s*(-?\d+(?:\.\d+)?)\s*°\s*\)?', r'\1(rad(\2))', t)
    t = re.sub(UNITS, '', t).strip()
    n = norm(t)
    if not t or re.search(r'[A-Za-z]', re.sub(FUNCS, '', n)):
        return None
    try:
        v = sp.sympify(n, locals=LOC, rational=True)
    except Exception:
        return None
    if not isinstance(v, sp.Expr) or v.free_symbols:
        return None
    return v


def resolution(seg):
    """The unit of the last written digit of a literal decimal (0.01 for 53.96, 10**5 for 1.34 x 10^8), else None."""
    t = re.sub(UNITS, '', seg.strip().strip('\'"').rstrip('.').strip()).strip()
    n = norm(t).replace(' ', '')
    m = re.fullmatch(r'-?\d+\.(\d+)', n)
    if m:
        return Fraction(1, 10 ** len(m.group(1)))
    m = re.fullmatch(r'\d+(?:\.(\d+))?\*10\*\*\((-?\d+)\)', n)
    if m:
        return Fraction(10) ** (int(m.group(2)) - len(m.group(1) or ''))
    return None


def unit(seg):
    m = re.search(r'(mm|cm|km|ml|litres?|m)[.,]?\s*$', seg.strip().strip('\'"'))
    return m.group(1) if m else None


def equal(a, b, res):
    """a == b exactly, or (res given) a rounded half away from zero at res equals b."""
    a, b = sp.sympify(a), sp.sympify(b)
    if not (a.is_real and b.is_real):
        return sp.simplify(a - b) == 0
    if res is None:
        return abs(sp.N(a - b, 60)) < sp.Float('1e-40')
    av = Fraction(str(sp.N(a, 60)))
    q = av / res
    r = math.floor(abs(q) + Fraction(1, 2)) * (1 if q >= 0 else -1)
    return r * res == Fraction(str(sp.N(b, 60)))


def depth0_split(text):
    out, depth, cur = [], 0, ''
    for i, ch in enumerate(text):
        depth += ch in '([' and 1 or ch in ')]' and -1 or 0
        if ch == ',' and depth == 0 and text[i + 1:i + 2] == ' ':
            out.append(cur)
            cur = ''
        else:
            cur += ch
    return out + [cur]


def chains(text):
    """[[(segment text, value or None), ...], ...]: one list per '=' chain, clause by clause."""
    out = []
    for part in re.split(r'(?<=[^\d])\.\s+|;\s+|:\s+|\s(?:so|then|and|but|not|giving)\s', text):
        for clause in depth0_split(part):
            segs = re.split(r'\s*(?:=|≈)\s*', clause)
            out.append([(s.strip(), value(s)) for s in segs])
    return out


def claims(text):
    """Every link between two numeric neighbours in a chain: (left, right, true?)."""
    out = []
    for ch in chains(text):
        units = {unit(s) for s, v in ch if v is not None and unit(s) in SCALE}
        for (s1, v1), (s2, v2) in zip(ch, ch[1:]):
            if v1 is None or v2 is None:
                continue
            u1, u2 = unit(s1), unit(s2)
            if len(units) > 1 and (u1 in SCALE) != (u2 in SCALE):
                continue
            a, b = v1, v2
            if u1 in SCALE and u2 in SCALE and u1 != u2:
                a, b = a * SCALE[u1], b * SCALE[u2]
            out.append((s1, s2, equal(a, b, resolution(s2))))
    return out


def written(text):
    """(segment, value) of the last numeric segment of the step: what the step says its quantity is."""
    last = None
    for ch in chains(text):
        for s, v in ch:
            if v is not None:
                last = (s, v)
    return last


def numbers_in(text):
    """Every number written in the text (bare, or a numeric segment of a chain) as (value, resolution)."""
    t = norm(text)
    out = [(v, resolution(s)) for ch in chains(text) for s, v in ch if v is not None]
    for m in re.finditer(r'-?\d+(?:\.\d+)?(?:/\d+)?(?:\*10\*\*\(-?\d+\))?', t):
        v = value(m.group(0))
        if v is not None:
            out.append((v, resolution(m.group(0))))
    return out


# ---------------------------------------------------------------------------------------------------------
# The reviewed table
# ---------------------------------------------------------------------------------------------------------
class R:
    """A reviewed verdict on a step that has no single number to compare: True = correct working."""

    def __init__(self, ok, why='', check=None):
        self.ok, self.why, self.check = ok, why, check


class A:
    """An answer that is not a number: the explanation must contain `text`, and `check` must hold."""

    def __init__(self, text, check):
        self.text, self.check = text, check


x, y, t, n, lam, s_, a_, c_ = sp.symbols('x y t n lam s a c')


def same(e1, e2):
    return sp.simplify(sp.sympify(e1) - sp.sympify(e2)) == 0


def I(key, phrase, answer, steps, extra=()):  # noqa: E743
    return {'key': key, 'phrase': phrase, 'answer': answer, 'steps': steps, 'extra': set(extra)}


SORTED9 = [9, 11, 14, 14, 14, 15, 17, 18, 20]
ITEMS = {
    # ---------------- KS3 ----------------
    'ste_ks3_001': I(1, 'share the winnings in the ratio', '2*180/(2+3+5)', {1: '2+3+5'}),
    'ste_ks3_002': I(2, 'reduced by 20%', '65*(100-20)/100', {1: '20*65/100', 2: '65*(100-20)/100'}),
    'ste_ks3_003': I(2, 'one-third of the remainder', '48-48*3/4-(48-48*3/4)/3',
                     {1: '48-48*3/4', 2: '(48-48*3/4)/3'}),
    'ste_ks3_004': I(1, 'travels 240 miles on a full tank of 30 litres', '180/(240/30)', {1: '240/30'}),
    'ste_ks3_005': I(1, 'what percentage walk to school', '18/30*100', {1: '18/30*100'}),
    'ste_ks3_006': I(2, 'nth term', A('4n − 3', lambda: [4 * k - 3 for k in (1, 2, 3)] == [1, 5, 9]),
                     {1: '5-1', 2: R(False, '4n gives 4, 8, 12; the nth term is 4n - 3',
                                     lambda: [4 * k for k in (1, 2, 3)] == [1, 5, 9])}),
    'ste_ks3_007': I(1, 'area of reflective material', '40*35/2', {1: '40*35/2'}),
    'ste_ks3_008': I(3, 'age of the seventh player', '7*17.5-6*17', {1: '6*17', 2: '7*17.5', 3: '7*17.5-6*17'}),
    'ste_ks3_009': I(1, 'ratio 1:4', '500/(1+4)', {1: '1+4'}),
    'ste_ks3_010': I(2, 'estimates the probability of picking red', '24/80', {1: '24', 2: '24/80'}),
    'ste_ks3_011': I(2, 'full capacity of the tank', '360/(3/8)',
                     {1: R(True, 'restates the question: 3/8 of the tank is 360 litres'), 2: '360/(3/8)'}, extra=[8]),
    'ste_ks3_012': I(2, '4% simple interest per year', '250*4/100*3', {1: '250*4/100', 2: '250*4/100*3'}),
    'ste_ks3_013': I(2, 'a scale of 1:50,000', '6.4*50000',
                     {1: R(True, '1:50,000 means 1 cm on the map is 50,000 cm'), 2: '6.4*50000'}),
    'ste_ks3_014': I(3, 'angle on the other side of the junction', '180-47',
                     {1: R(True, 'the roads form a straight line'), 2: '180-47', 3: '180-47'}),
    'ste_ks3_015': I(1, 'total length of fencing needed', '2*(85+62)', {1: '2*(85+62)'}),
    'ste_ks3_016': I(1, 'Monday she walks 2⅓ miles', '(2*3+1)/3+(1*4+3)/4+(3*6+1)/6',
                     {1: R(False, '2⅓ = 7/3, not 6/3', lambda: 2 + Fraction(1, 3) == Fraction(6, 3))}, extra=[6]),
    'ste_ks3_017': I(1, 'next align', 'ilcm(420,315)',
                     {1: R(False, 'they align after the LCM of the periods, not the HCF')}),
    'ste_ks3_018': I(2, 'Each row has 2 more seats than the one before', '20+(15-1)*2', {1: '2', 2: '20+(15-1)*2'}),
    'ste_ks3_019': I(2, '600 g of oats', '600/4', {1: R(True, 'the ratio 4:1 is oats:butter'), 2: '600/4'}),
    'ste_ks3_020': I(2, 'percentage increase in average attendance', '(5040-4500)/4500*100',
                     {1: '5040-4500', 2: '(5040-4500)/4500*100'}),
    'ste_ks3_021': I(2, 'area of the pond', 'pi*(4.2/2)**2', {1: '4.2/2', 2: 'pi*(4.2/2)**2'}),
    'ste_ks3_022': I(2, 'height after the 4th bounce', '160/2**4',
                     {1: R(True, 'the heights halve: 160, 80, 40, 20'), 2: '160/2**4'}, extra=[16]),
    'ste_ks3_023': I(2, 'finds the median', '14',
                     {1: R(True, 'sorted correctly',
                           lambda: sorted([14, 18, 9, 14, 20, 11, 14, 17, 15]) == SORTED9),
                      2: R(False, 'the median of 9 values is the 5th, not the 4th', lambda: (9 + 1) // 2 == 4)}),
    'ste_ks3_024': I(3, '30° more than s', '(180-30)/4+30',
                     {1: R(True, 's + 2s + (s + 30) = 180 is the angle sum'), 2: '(180-30)/4',
                      3: R(False, 'the third angle is s + 30 = 67.5°, not s', lambda: 37.5 == 37.5 + 30)}),
    'ste_ks3_025': I(2, 'The rest study German', '400*(1-2/5-1/4)', {1: '2/5+1/4', 2: '400*(1-2/5-1/4)'}, extra=[5]),
    'ste_ks3_026': I(1, 'how far is left', '142-87', {1: '142-87'}),
    'ste_ks3_027': I(2, 'finds the hypotenuse', 'sqrt(6**2+8**2)', {1: '6**2+8**2', 2: 'sqrt(6**2+8**2)'}),
    'ste_ks3_028': I(1, 'quadrilateral', '360-80-110-95',
                     {1: R(False, 'angles in a quadrilateral sum to 360°', lambda: (4 - 2) * 180 == 180)}),
    'ste_ks3_029': I(1, '150 km in 2 hours', '225/(150/2)', {1: '150/2'}),
    'ste_ks3_030': I(1, 'area to buy topsoil', 'pi*3.5**2', {1: 'pi*3.5**2'}),
    'ste_ks3_031': I(1, 'find the median', '5',
                     {1: R(False, 'the middle of the sorted list is 5', lambda: sorted([5, 2, 8, 4, 6, 1, 9])[3] == 4)}),
    'ste_ks3_032': I(1, 'rounded to 1 decimal place', '3.5',
                     {1: R(False, '3.45 rounds half up to 3.5', lambda: equal(sp.Rational('3.45'), sp.Rational('3.4'),
                                                                               Fraction(1, 10)))}, extra=[3.5]),
    'ste_ks3_033': I(1, 'converts this to millilitres', '1.5*1000', {1: '1.5*1000'}),
    'ste_ks3_034': I(1, 'real length', '8*25000/100000', {1: '8*25000/100000'}, extra=[100000]),
    'ste_ks3_035': I(1, '3(x + 4)', '3*(2+4)', {1: '3*(2+4)'}),
    # ---------------- GCSE ----------------
    'ste_gcse_001': I(1, 'after a 10% reduction', '76.50/(1-10/100)', {1: '76.50/(1-10/100)-76.50'}),
    'ste_gcse_002': I(2, 'compound interest', '2000*(1+3.5/100)**3',
                      {1: '2000*3.5/100', 2: '2000*(1+3.5/100)**3-2000'}),
    'ste_gcse_003': I(3, 'vector OM in terms of a and c', A('½a + c', lambda: same((a_ + c_) - a_ / 2, a_ / 2 + c_)),
                      {1: R(True, 'BC = OC - OB = c - (a + c)', lambda: same(c_ - (a_ + c_), -a_)),
                       2: R(True, 'BM is half of BC'),
                       3: R(False, 'vectors are added, not multiplied: OM = OB + BM')}),
    'ste_gcse_004': I(2, 'without replacement', '5/10*4/9', {1: '5/10', 2: '4/9'}, extra=[9]),
    'ste_gcse_005': I(1, '3 × 10⁸ m/s', '4.013*10**16/(3*10**8)',
                      {1: R(False, 'time = distance ÷ speed')}),
    'ste_gcse_006': I(2, 'angle of depression to a boat', '80/tan(rad(34))',
                      {1: R(True, 'alternate angles'),
                       2: R(False, 'the 80 m height is opposite the 34° angle at the boat, so tan 34° = 80 ÷ d')}),
    'ste_gcse_007': I(2, 'similar in shape', '50*(12/8)**3', {1: '12/8', 2: '(12/8)**3'}),
    'ste_gcse_008': I(1, 'interquartile range', '9.1-4.8', {1: '9.1-4.8'}),
    'ste_gcse_009': I(4, 'returns 1 tin and 1 roll', '33.75-(167-4*33.75)',
                      {1: R(True, 'the two equations', lambda: 5 * 32 + 4 * Fraction('1.75') == 167),
                       2: '4*33.75', 3: '167-4*33.75', 4: '33.75-(167-4*33.75)'}),
    'ste_gcse_010': I(2, 'exact side length in simplified surd form', A('3√5', lambda: same(3 * sp.sqrt(5), sp.sqrt(45))),
                      {1: 'sqrt(45)', 2: 'sqrt(45)'}),
    'ste_gcse_011': I(1, 'cyclic quadrilateral', '(180-10+18)/8',
                      {1: R(False, 'opposite angles of a cyclic quadrilateral sum to 180°')}, extra=[8]),
    'ste_gcse_012': I(1, 'gradient', '(13-5)/(6-2)', {1: '(13-5)/(6-2)'}),
    'ste_gcse_013': I(2, 'finds side b', '10*sin(rad(45))/sin(rad(30))',
                      {1: R(True, 'the sine rule'), 2: '10*sin(rad(45))/sin(rad(30))'}),
    'ste_gcse_014': I(2, 'percentage profit', '(520-400)/400*100', {1: '520-400', 2: '(520-400)/400*100'}),
    'ste_gcse_015': I(2, 'lower bound of the area', '(8.4-0.05)*(5.2-0.05)',
                      {1: R(True, 'half a millimetre below each', lambda: (Fraction('8.4') - Fraction('0.05'),
                                                                          Fraction('5.2') - Fraction('0.05'))
                            == (Fraction('8.35'), Fraction('5.15'))),
                       2: '(8.4-0.05)*(5.2-0.05)'}, extra=[0.05]),
    'ste_gcse_016': I(2, '(3 × 10⁴) × (2 × 10³)', '10**4*10**3', {1: '3*2', 2: '10**4*10**3'}),
    'ste_gcse_017': I(1, 'complete the square',
                      A('(x + 4)² − 13', lambda: same((x + 4) ** 2 - 13, x ** 2 + 8 * x + 3)),
                      {1: R(False, '(x + 8)² + 3 − 64 is not x² + 8x + 3',
                            lambda: same((x + 8) ** 2 + 3 - 64, x ** 2 + 8 * x + 3))}),
    'ste_gcse_018': I(1, 'log(5) + log(4)', 'log(5*4)', {1: 'log(5)+log(4)'}),
    'ste_gcse_019': I(2, 'quadratic formula',
                      A('(5 ± √17) ÷ 4', lambda: set(sp.solve(2 * x ** 2 - 5 * x + 1, x))
                        == {(5 + sp.sqrt(17)) / 4, (5 - sp.sqrt(17)) / 4}),
                      {1: R(True, 'a, b, c read from 2x² − 5x + 1'),
                       2: R(False, 'the denominator is 2a = 4', lambda: 2 * 2 == 2)}),
    'ste_gcse_020': I(1, 'gf(2)', '(2*2+3)**2', {1: R(False, 'gf(2) means g(f(2)), not f(g(2))')}),
    'ste_gcse_021': I(2, 'solves the inequality', A('x < −4', lambda: all(-3 * v > 12 for v in (-5, -4.5, -100))
                                                    and not -3 * -3 > 12),
                      {1: R(True, 'restates the inequality'),
                       2: R(False, 'dividing by −3 reverses the inequality')}),
    'ste_gcse_022': I(1, 'find 2a', A('6i + 4j', lambda: (2 * 3, 2 * 2) == (6, 4)),
                      {1: R(False, '2a is the vector 6i + 4j, not a number')}),
    'ste_gcse_023': I(2, 'area of the field is 198 m²', A('w(w + 7) = 198', lambda: 11 * (11 + 7) == 198),
                      {1: R(True, 'length w + 7, width w'), 2: R(False, '198 m² is the area, not the perimeter')}),
    'ste_gcse_024': I(2, 'how far up the wall the ladder reaches', 'sqrt(6**2-1.8**2)',
                      {1: R(True, 'the ladder is the hypotenuse'), 2: '6**2-1.8**2'}),
    'ste_gcse_025': I(1, 'angle of incline', 'deg(atan(0.9/6))', {1: '0.9/6'}),
    'ste_gcse_026': I(2, 'how many times heavier', '5.97*10**24/(7.34*10**22)',
                      {1: '5.97*10**24+7.34*10**22', 2: '5.97*10**24/(7.34*10**22)'}),
    'ste_gcse_027': I(1, 'after its value increased by 17%', '292500/(1+17/100)',
                      {1: '292500-292500/(1+17/100)'}),
    'ste_gcse_028': I(3, 'eliminates a', '(5*47-3*53)/(5*5-3*2)',
                      {1: '5*47', 2: '3*53', 3: '(5*47-3*53)/(5*5-3*2)'}),
    'ste_gcse_029': I(3, 'angle ACB where C is any point on the major arc', '136/2',
                      {1: R(True, 'the angle at the centre theorem'), 2: '136/2', 3: '136/2'}),
    'ste_gcse_030': I(2, 'at least one day', '1-(1-0.3)**2', {1: '0.3*0.3', 2: '1-(1-0.3)**2'}),
    'ste_gcse_031': I(2, 'bearing to return', '180+deg(atan(22/15))',
                      {1: 'deg(atan(22/15))', 2: '180+deg(atan(22/15))'}),
    'ste_gcse_032': I(2, 'westward displacement', '-30*sin(rad(250))',
                      {1: R(True, 'a bearing is measured clockwise from north'), 2: '-30*sin(rad(250))'}),
    'ste_gcse_033': I(1, 'IQR', '41-23', {1: '41-23'}),
    'ste_gcse_034': I(1, 'frequency', '3*10', {1: '3*10'}),
    'ste_gcse_035': I(1, 'cosine rule', 'sqrt(8**2+6**2-2*8*6*cos(rad(60)))',
                      {1: R(False, 'the cosine rule is c² = a² + b² − 2ab cos C')}),
    'ste_gcse_036': I(2, 'two days', '1-0.4', {1: R(True, '0.4 and 0.6 sum to 1'), 2: '1-0.4'}),
    'ste_gcse_037': I(1, 'perpendicular', '-1/3', {1: '-1/3'}),
    'ste_gcse_038': I(1, 'expand', A('x² + 8x + 15', lambda: same((x + 3) * (x + 5), x ** 2 + 8 * x + 15)),
                      {1: R(False, 'the 3 × 5 term is missing', lambda: same((x + 3) * (x + 5), x ** 2 + 8 * x))}),
    'ste_gcse_039': I(1, 'equation', A('(x − 3)² + (y + 2)² = 25', lambda: 5 ** 2 == 25),
                      {1: R(False, 'the right-hand side is r² = 25')}),
    'ste_gcse_040': I(1, 'rationalise', '6/sqrt(3)', {1: '6/sqrt(3)'}),
    'ste_gcse_041': I(1, 'fg(x)', A('3x + 2', lambda: same((3 * x) + 2, 3 * x + 2)),
                      {1: R(False, 'fg(x) = f(g(x)), not f(x) × g(x)')}),
    'ste_gcse_042': I(2, 'nth term', A('3n + 2', lambda: [3 * k + 2 for k in (1, 2, 3, 4)] == [5, 8, 11, 14]),
                      {1: '8-5', 2: R(False, '3n + 5 gives 8 first', lambda: [3 * k + 5 for k in (1, 2)] == [5, 8])}),
    'ste_gcse_043': I(2, 'make t the subject', A('(v − u) ÷ a', lambda: True),
                      {1: R(True, 'u subtracted from both sides'), 2: R(False, 'divide by a, do not multiply')}),
    'ste_gcse_044': I(1, 'arc length', '72/360*2*pi*10', {1: '72/360*2*pi*10'}),
    'ste_gcse_045': I(3, 'by substitution', '2',
                      {1: R(True, 'y from the second equation', lambda: 4 * 2 - 3 == 5),
                       2: R(True, 'substituted into the first'), 3: '2'}),
    # ---------------- Level 4 ----------------
    'ste_l4_001': I(1, 'rate of change of y with respect to x',
                    A('12x² − 10x + 2', lambda: same(sp.diff(4 * x ** 3 - 5 * x ** 2 + 2 * x - 7, x),
                                                     12 * x ** 2 - 10 * x + 2)),
                    {1: R(False, 'the derivative of −7 is 0')}),
    'ste_l4_002': I(1, 'log(8) + log(4) − log(2)', 'log(8*4/2)', {1: 'log(8)+log(4)'}, extra=[16]),
    'ste_l4_003': I(3, 'multiplies', A('5 + j', lambda: (2 + 3j) * (1 - 1j) == 5 + 1j),
                    {1: R(True, 'every pair multiplied'), 2: R(True, 'collected'), 3: R(False, 'j² = −1')}),
    'ste_l4_004': I(2, 'distance s travelled from t = 0',
                    A('t³ + t² + c', lambda: same(sp.integrate(3 * t ** 2 + 2 * t, t), t ** 3 + t ** 2)),
                    {1: R(True, 'distance is the integral of velocity'),
                     2: R(False, '∫3t² dt = t³', lambda: same(sp.integrate(3 * t ** 2, t), 3 * t ** 2 / 2))}),
    'ste_l4_005': I(3, 'product rule',
                    A('x²cos(x) + 2x·sin(x)', lambda: same(sp.diff(x ** 2 * sp.sin(x), x),
                                                         x ** 2 * sp.cos(x) + 2 * x * sp.sin(x))),
                    {1: R(True, 'u and v chosen'),
                     2: R(True, 'du/dx and dv/dx', lambda: same(sp.diff(x ** 2, x), 2 * x)
                          and same(sp.diff(sp.sin(x), x), sp.cos(x))),
                     3: R(False, 'the product rule is u v′ + v u′')}),
    'ste_l4_006': I(1, 'determinant det(A)', '2*4-3*1', {1: '2*4-3*1'}),
    'ste_l4_007': I(1, 'sum to infinity', '3/(1-0.5)', {1: '3/(1-0.5)'}),
    'ste_l4_008': I(1, 'evaluates', A('2x² + x + c', lambda: same(sp.integrate(4 * x + 1, x), 2 * x ** 2 + x)),
                    {1: R(False, '∫4x dx = 2x²', lambda: same(sp.integrate(4 * x + 1, x), 4 * x ** 2 + x))}),
    'ste_l4_009': I(1, 'finds dy/dx', A('6(2x + 5)²', lambda: same(sp.diff((2 * x + 5) ** 3, x), 6 * (2 * x + 5) ** 2)),
                    {1: R(False, 'the chain rule multiplies by 2',
                          lambda: same(sp.diff((2 * x + 5) ** 3, x), 3 * (2 * x + 5) ** 2))}),
    'ste_l4_010': I(1, 'finds dy/dx', A('2x + 2y(dy/dx) = 0', lambda: True),
                    {1: R(False, 'd/dx(y²) = 2y dy/dx')}),
    'ste_l4_011': I(1, 'S∞', A('does not exist', lambda: abs(2) >= 1),
                    {1: R(False, 'with r = 2 the series diverges')}),
    'ste_l4_012': I(1, 'coefficient of x²', 'binomial(5,2)', {1: 'binomial(5,2)'}),
    'ste_l4_013': I(2, 'eigenvalues', A('(4−λ)(3−λ) − (1)(2) = 0',
                                         lambda: same(sp.Matrix([[4 - lam, 1], [2, 3 - lam]]).det(),
                                                      (4 - lam) * (3 - lam) - 2)),
                    {1: R(True, 'the characteristic equation'),
                     2: R(False, 'the off-diagonal product is subtracted',
                          lambda: same(sp.Matrix([[4 - lam, 1], [2, 3 - lam]]).det(), (4 - lam) * (3 - lam) + 2))}),
    'ste_l4_014': I(1, 'partial fractions', A('A/(x+1) + B/(x−1)', lambda: True),
                    {1: R(False, 'the second denominator is x − 1')}),
    'ste_l4_015': I(1, 'De Moivre', A('cos120° + j·sin120°', lambda: 4 * 30 == 120),
                    {1: R(False, 'the power multiplies both arguments')}),
    'ste_l4_016': I(2, 'eigenvalue equation', A('(A − λI)v = 0', lambda: True),
                    {1: R(True, 'λ = 2 or 5', lambda: set(sp.Matrix([[3, 1], [2, 4]]).eigenvals()) == {2, 5}),
                     2: R(False, 'eigenvectors solve (A − λI)v = 0')}),
    'ste_l4_017': I(4, 'definite integral', '(3**3/3+2*3)-(1**3/3+2*1)',
                    {1: R(True, 'the antiderivative', lambda: same(sp.integrate(x ** 2 + 2, x), x ** 3 / 3 + 2 * x)),
                     2: '27/3+6', 3: '1/3+2', 4: '(27/3+6)-(1/3+2)'}),
    'ste_l4_018': I(1, 'cover-up method', '(3*(-1)+1)/((-1)-2)', {1: R(False, 'the root of x + 1 is x = −1')}),
    'ste_l4_019': I(2, 'chain rule', A('30x(3x²+1)⁴', lambda: same(sp.diff((3 * x ** 2 + 1) ** 5, x),
                                                                   30 * x * (3 * x ** 2 + 1) ** 4)),
                    {1: R(True, 'u and y chosen'),
                     2: R(False, 'du/dx = 6x', lambda: same(sp.diff(3 * x ** 2 + 1, x), 3 * x ** 2))}),
    'ste_l4_020': I(2, 'modulus-argument form', 'deg(sp.arg(-3+3*sp.I))',
                    {1: 'sqrt(9+9)', 2: 'deg(sp.arg(-3+3*sp.I))'}),
    'ste_l4_021': I(2, 'A⁻¹', A('(1/10)[[4,−2],[−1,3]]', lambda: sp.Matrix([[3, 2], [1, 4]]).inv()
                               == sp.Matrix([[4, -2], [-1, 3]]) / 10),
                    {1: '3*4-2*1', 2: R(False, 'the adjugate negates the off-diagonal',
                                        lambda: sp.Matrix([[3, 2], [1, 4]]).inv() == sp.Matrix([[4, 1], [2, 3]]) / 10)}),
    'ste_l4_022': I(2, 'classifies', A('minimum', lambda: sp.diff(x ** 3 - 3 * x, x, 2).subs(x, 1) > 0),
                    {1: R(True, 'dy/dx = 0 at x = 1', lambda: sp.diff(x ** 3 - 3 * x, x).subs(x, 1) == 0),
                     2: R(False, 'd²y/dx² > 0 is a minimum')}),
    'ste_l4_023': I(2, 'integration by parts',
                    A('x·sin(x) + cos(x) + c', lambda: same(sp.diff(x * sp.sin(x) + sp.cos(x), x), x * sp.cos(x))),
                    {1: R(True, 'u = x, dv = cos(x) dx'),
                     2: R(False, '∫cos(x) dx = sin(x)', lambda: same(sp.integrate(sp.cos(x), x), -sp.sin(x)))}),
    'ste_l4_024': I(1, 'x³ term', A('160x³', lambda: sp.binomial(6, 3) * 2 ** 3 == 160),
                    {1: R(False, 'the x³ term uses (2x)³')}),
    'ste_l4_025': I(1, 'Maclaurin series for cos(x)', A('1 − x²/2! + x⁴/4!', lambda: same(
        sp.series(sp.cos(x), x, 0, 5).removeO(), 1 - x ** 2 / 2 + x ** 4 / 24)),
                    {1: R(False, 'cos(x) has only even powers')}),
    'ste_l4_026': I(2, 'dy/dx', A('2t/2 = t', lambda: same(sp.diff(t ** 2, t) / sp.diff(2 * t, t), t)),
                    {1: R(True, 'dx/dt = 2, dy/dt = 2t'),
                     2: R(False, 'dy/dx = (dy/dt) ÷ (dx/dt)', lambda: same(sp.diff(t ** 2, t) / sp.diff(2 * t, t), 1 / t))}),
    'ste_l4_027': I(1, 'identifies r', '12/(1-6/12)', {1: '6/12'}),
    'ste_l4_028': I(1, '|z|', 'sqrt(3**2+4**2)', {1: 'sqrt(3**2+4**2)'}),
    'ste_l4_029': I(2, 'Cramer’s rule', '(7*4-3*9)/(2*4-3*1)', {1: '2*4-3*1', 2: '7*4-3*9'}),
    'ste_l4_030': I(1, 'implicitly', A('2xy + x²(dy/dx) = 0', lambda: True),
                    {1: R(False, 'the product rule on x²y gives a dy/dx term')}),
}
ALWAYS_GIVEN = {0, 1, 2, 3, 4, 10, 100, 180, 360, 1000}
# The content hash (bank_common.content_hash, first 12) of each item as it was when its ITEMS entry was
# reviewed. A verdict (R) reads no text, so any edit to an item fails here until its entry is re-reviewed;
# then print the new hashes with --print-pins and paste them in. Never update a pin without re-reviewing.
REVIEWED = {
    'ste_ks3_001': '584e30a88257',
    'ste_ks3_002': '187f546d13c7',
    'ste_ks3_003': 'fa267e76250a',
    'ste_ks3_004': '76e671a0e605',
    'ste_ks3_005': '8842c2ca631e',
    'ste_ks3_006': 'd287abfec3e8',
    'ste_ks3_007': '1281b5feb8db',
    'ste_ks3_008': '7a98ff34f38b',
    'ste_ks3_009': 'd29b983b0c69',
    'ste_ks3_010': '45f440cd3133',
    'ste_ks3_011': '76ede7acb9b8',
    'ste_ks3_012': 'c03a14a2832c',
    'ste_ks3_013': 'a14387abf09b',
    'ste_ks3_014': 'a62a91a5c79b',
    'ste_ks3_015': '72d9def52399',
    'ste_ks3_016': 'cfbb8bb4b1e2',
    'ste_ks3_017': '1ce71348ac94',
    'ste_ks3_018': '490558dcb982',
    'ste_ks3_019': '482b74ab51de',
    'ste_ks3_020': 'bf4107db2f1c',
    'ste_ks3_021': 'e0c832822923',
    'ste_ks3_022': '0541979049f7',
    'ste_ks3_023': '2b8080ce3788',
    'ste_ks3_024': '892ab861d77a',
    'ste_ks3_025': 'f514fc8d60b8',
    'ste_ks3_026': '0dc4ef4018d2',
    'ste_ks3_027': '8289b3860101',
    'ste_ks3_028': '5cdbcd03ee88',
    'ste_ks3_029': 'de558e234ece',
    'ste_ks3_030': '274f79b10f05',
    'ste_ks3_031': 'dc4293979ee1',
    'ste_ks3_032': 'f00903e1aa9a',
    'ste_ks3_033': '1f5ff8caf0cf',
    'ste_ks3_034': '0fa0aa373838',
    'ste_ks3_035': '1a691af2147c',
    'ste_gcse_001': '5d7209f61e84',
    'ste_gcse_002': '04aedcab7565',
    'ste_gcse_003': '45fafa0fb443',
    'ste_gcse_004': '55ccbe102420',
    'ste_gcse_005': '6c5de7d9e0d5',
    'ste_gcse_006': '2bf2a2d72cf4',
    'ste_gcse_007': '006486856736',
    'ste_gcse_008': 'e39ea5ee395d',
    'ste_gcse_009': '591bb13130ca',
    'ste_gcse_010': '5b96c7f20bcb',
    'ste_gcse_011': 'a5351a901a55',
    'ste_gcse_012': '3edc665cd23f',
    'ste_gcse_013': 'da861b114433',
    'ste_gcse_014': '73b8475934c6',
    'ste_gcse_015': '676d0750ee47',
    'ste_gcse_016': '7ca12a8e4a0f',
    'ste_gcse_017': 'af85c312f892',
    'ste_gcse_018': '162ebf3db525',
    'ste_gcse_019': '31e511df7db8',
    'ste_gcse_020': '0117d5e4e025',
    'ste_gcse_021': '6f40b1eb3c47',
    'ste_gcse_022': '5645d7648f2f',
    'ste_gcse_023': 'ce94c6d88dc0',
    'ste_gcse_024': '84d5a89f4a77',
    'ste_gcse_025': 'a2b6979c953a',
    'ste_gcse_026': '58a4a37339d7',
    'ste_gcse_027': 'c333dd77fe54',
    'ste_gcse_028': '318945a1c9b2',
    'ste_gcse_029': '42db90b661ef',
    'ste_gcse_030': '41d64d927c72',
    'ste_gcse_031': 'b494f8d1b539',
    'ste_gcse_032': '86bef2bdcc11',
    'ste_gcse_033': '40a4bb32778a',
    'ste_gcse_034': 'ac0b7a1bd1fa',
    'ste_gcse_035': '03860881df55',
    'ste_gcse_036': '9c8ec73ceff1',
    'ste_gcse_037': '6c199b6b9fd2',
    'ste_gcse_038': '0da4c63d515f',
    'ste_gcse_039': 'be22cbd17226',
    'ste_gcse_040': '9f00ae03bba5',
    'ste_gcse_041': '8f4d2a787bd3',
    'ste_gcse_042': '54fdd1d31523',
    'ste_gcse_043': '0b4710c95db6',
    'ste_gcse_044': 'a62fb8cc69ab',
    'ste_gcse_045': '93fe36c23cf0',
    'ste_l4_001': 'b8a7013c5450',
    'ste_l4_002': 'c0f9ef5cb7b4',
    'ste_l4_003': '6c1ccd0fe165',
    'ste_l4_004': 'df8e9adab6ea',
    'ste_l4_005': '380bf1e6e82d',
    'ste_l4_006': '0372f25ac0f9',
    'ste_l4_007': '50885519b13b',
    'ste_l4_008': 'b71be65a1a69',
    'ste_l4_009': '3d1392479371',
    'ste_l4_010': '7be4577f4f89',
    'ste_l4_011': '8b4a025b92a2',
    'ste_l4_012': '54e22cc73d52',
    'ste_l4_013': '344dcfd2ea87',
    'ste_l4_014': '5c870f1bd180',
    'ste_l4_015': 'fdb0f12ffa4b',
    'ste_l4_016': 'd54441ab91c3',
    'ste_l4_017': '72004c2c8506',
    'ste_l4_018': 'd5c492309545',
    'ste_l4_019': '23f48e24e3ff',
    'ste_l4_020': '67a7b660c1bb',
    'ste_l4_021': '51038849e4c1',
    'ste_l4_022': '5336fff87fd8',
    'ste_l4_023': 'fec20c11170e',
    'ste_l4_024': '78db0d6e4ab1',
    'ste_l4_025': 'c504d28608dc',
    'ste_l4_026': 'af4303cf877b',
    'ste_l4_027': 'db538ee5933f',
    'ste_l4_028': 'd48f0a70226e',
    'ste_l4_029': '6bc3f179ef71',
    'ste_l4_030': 'a4a86515295b',
}


def evaluate(expr):
    return sp.sympify(expr, locals=dict(LOC, sp=sp, ilcm=sp.ilcm), rational=True)


def where(qid):
    return '%s%s' % (qid, ' (spot-the-error-%s)' % AUDIT[qid] if qid in AUDIT else '')


def check_bank(fails, bank, verbose=False):
    ids = [q['id'] for q in bank]
    if len(set(ids)) != len(ids):
        fails.append('bank: duplicate ids')
    counts = {lv: sum(q['level'] == lv for q in bank) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs ITEMS reviewed)' % (counts, COUNTS))
    for qid in sorted(set(ITEMS) - set(ids)):
        fails.append('%s: in ITEMS but not in the bank' % qid)
    for q in bank:
        qid, w = q['id'], where(q['id'])
        it = ITEMS.get(qid)
        if it is None:
            fails.append('%s: no reviewed ITEMS entry (review the item and add it; never skip)' % qid)
            continue
        steps, key = q['steps'], q['errorStepId']
        if REVIEWED.get(qid) != bc.content_hash(q)[:12]:
            fails.append('%s: the item has changed since its ITEMS entry was reviewed (re-review it, then update '
                         'REVIEWED from --print-pins)' % w)
        if [s['id'] for s in steps] != list(range(1, len(steps) + 1)):
            fails.append('%s: steps are not numbered 1..%d' % (w, len(steps)))
        if key != it['key']:
            fails.append('%s: the bank keys step %s, the reviewed key is step %d (%s)'
                         % (w, key, it['key'], steps[it['key'] - 1]['content'] if it['key'] <= len(steps) else '?'))
        if [s['id'] for s in steps if not s['correct']] != [key]:
            fails.append('%s: correct:false is set on steps %s, expected only the key (%s)'
                         % (w, [s['id'] for s in steps if not s['correct']], key))
        # Arithmetic: every link outside the key step, and in the explanation, is true.
        for s in steps:
            for left, right, ok in claims(s['content']):
                if not ok and s['id'] != key:
                    fails.append('%s step %d: "%s = %s" is false, and the step is not the key (a second error)'
                                 % (w, s['id'], left, right))
        for left, right, ok in claims(q['explanation']):
            if not ok:
                fails.append('%s explanation: "%s = %s" is false' % (w, left, right))
        # Every step up to the key: correct before it, departing at it.
        for sid in range(1, min(key, len(steps)) + 1):
            content = steps[sid - 1]['content']
            exp = it['steps'].get(sid)
            at_key = sid == key
            if exp is None:
                fails.append('%s step %d: no reviewed expectation in ITEMS' % (w, sid))
                continue
            if isinstance(exp, R):
                if exp.ok == at_key:
                    fails.append('%s step %d: reviewed as %s but it is %s the key'
                                 % (w, sid, 'correct' if exp.ok else 'an error', 'the' if at_key else 'before'))
                if exp.check is not None and bool(exp.check()) != exp.ok:
                    fails.append('%s step %d: the check for "%s" says the step is %s'
                                 % (w, sid, exp.why, 'correct' if exp.check() else 'wrong'))
                continue
            wr = written(content)
            if wr is None:
                fails.append('%s step %d: no number to compare in "%s"' % (w, sid, content))
                continue
            truth = evaluate(exp)
            match = equal(truth, wr[1], resolution(wr[0]))
            false_link = any(not ok for _, _, ok in claims(content))
            if at_key and match and not false_link:
                fails.append('%s step %d (the key): "%s" is true (%s = %s), so the student must tap a correct step'
                             % (w, sid, content, exp, sp.N(truth, 6)))
            if not at_key and not match:
                fails.append('%s step %d: "%s" says %s, the true value is %s, but the step is before the key'
                             % (w, sid, content, wr[0], sp.N(truth, 6)))
        # The answer the explanation teaches.
        ans = it['answer']
        if isinstance(ans, A):
            if ans.text not in q['explanation']:
                fails.append('%s explanation: does not state the answer %s' % (w, ans.text))
            if not ans.check():
                fails.append('%s: the reviewed answer %s does not check' % (w, ans.text))
        else:
            truth = evaluate(ans)
            if not any(equal(truth, v, r) for v, r in numbers_in(q['explanation'])):
                fails.append('%s explanation: does not state the answer %s (= %s)' % (w, ans, sp.N(truth, 6)))
            given = {Fraction(str(v)) for v, _ in numbers_in(q['text'])}
            for m in re.findall(r'(?<![\w.])\d+(?:\.\d+)?', re.sub(r'rad\(\d+\)', '', ans)):
                f = Fraction(m)
                if f not in given and f not in ALWAYS_GIVEN and float(f) not in {float(e) for e in it['extra']}:
                    fails.append('%s: the answer uses %s, which the question does not give' % (w, m))
        # Stage 2: one misread phrase, the pinned one, every phrase in the problem.
        errs = [p['phrase'] for p in q['errorPhrases'] if p['isError']]
        if errs != [it['phrase']]:
            fails.append('%s Stage 2: the misread phrase is keyed as %s, reviewed as [%r]' % (w, errs, it['phrase']))
        for p in q['errorPhrases']:
            if q['text'].count(p['phrase']) < 1:
                fails.append('%s Stage 2: phrase %r is not in the problem' % (w, p['phrase']))
        if verbose:
            print('  %-14s key %d  %s' % (qid, key, steps[key - 1]['content'][:70]))


# ---------------------------------------------------------------------------------------------------------
# Chromium: every item through the game's own stages
# ---------------------------------------------------------------------------------------------------------
SWEEP_JS = r"""() => {
  window.setTimeout = (f) => { f(); return 0; };   // the game's pauses, run at once
  const out = [];
  const cards = () => [...document.querySelectorAll('#stageContent .step-card')];
  const taps = () => [...document.querySelectorAll('#stageContent .phrase-tap')];
  const stageText = () => document.getElementById('stagePill').textContent;
  for (const q of Q) {
    const r = {id: q.id, problems: []};
    currentQ = q; stage = 1; s1Attempts = 0; s2Attempts = 0; questionPoints = 0; qIndex = 0; totalQ = 1;
    document.getElementById('explanationBox').innerHTML = '';
    showStage1();
    const cs = cards();
    const shown = cs.map(c => c.textContent);
    q.steps.forEach((s, i) => { if (shown[i] !== s.id + '.' + s.content) r.problems.push('step ' + s.id + ' shows ' + JSON.stringify(shown[i])); });
    if (cs.length !== q.steps.length) r.problems.push(cs.length + ' step cards for ' + q.steps.length + ' steps');
    const wrong = q.steps.findIndex(s => s.id !== q.errorStepId);
    if (wrong >= 0) {
      cs[wrong].click();
      if (cs[wrong].classList.contains('correct-pick') || !stageText().startsWith('Stage 1'))
        r.problems.push('tapping step ' + q.steps[wrong].id + ' (not the key) was marked correct');
    }
    const k = q.steps.findIndex(s => s.id === q.errorStepId);
    cs[k].click();
    if (!cs[k].classList.contains('correct-pick')) r.problems.push('tapping the key step was not marked correct');
    if (!stageText().startsWith('Stage 2')) { r.problems.push('Stage 2 did not open after the key step'); out.push(r); continue; }
    const ts = taps();
    const want = q.errorPhrases.map(p => p.phrase).sort(), got = ts.map(e => e.textContent).sort();
    if (JSON.stringify(want) !== JSON.stringify(got)) r.problems.push('tappable phrases ' + JSON.stringify(got) + ', expected ' + JSON.stringify(want));
    const bad = ts.find(e => !q.errorPhrases.some(p => p.isError && p.phrase === e.textContent));
    if (bad) {
      bad.click();
      if (bad.classList.contains('correct-pick') || document.querySelector('#explanationBox .explanation'))
        r.problems.push('tapping ' + JSON.stringify(bad.textContent) + ' (not the misread) was marked correct');
    }
    const good = ts.find(e => q.errorPhrases.some(p => p.isError && p.phrase === e.textContent));
    if (!good) r.problems.push('the misread phrase is not tappable');
    else {
      good.click();
      if (!good.classList.contains('correct-pick')) r.problems.push('tapping the misread phrase was not marked correct');
      const ex = document.querySelector('#explanationBox .explanation');
      if (!ex || !ex.textContent.startsWith(q.explanation)) r.problems.push('the explanation shown is not the item\'s own');
    }
    out.push(r);
  }
  return out;
}"""


def play(fails, html):
    """Read the bank from the served page and play every item. Returns the bank (or None)."""
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
            page.wait_for_function('typeof Q !== "undefined" && typeof showStage1 === "function"', timeout=8000)
            bank = page.evaluate('() => Q')
            page.click('.level-btn[data-level="ks3"]')
            page.click('#startBtn')
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


# Three of the audit's own faults, planted back into a copy of the page: (item, what, old text, planted text).
PLANTS = [
    ('ste_gcse_044', 'gcse_044: the equivalent arc formula keyed as the error (t1-004)',
     'Arc length = (72/360) \\u00d7 \\u03c0 \\u00d7 10 = 6.28 cm',
     'Arc length = (72/180) \\u00d7 \\u03c0 \\u00d7 10 = 12.57 cm'),
    ('ste_l4_002', 'l4_002: log(12) - log(2) = log(10) marked correct (t1-009)',
     "log(12) \\u2212 log(2) = log(6)'", "log(12) \\u2212 log(2) = log(10) = 1'"),
    ('ste_ks3_024', 'ks3_024: the Stage 2 key on the wrong phrase (t1-002)',
     "{phrase:'one angle is twice the smallest angle',isError:false},{phrase:'30\\u00b0 more than s',isError:true}",
     "{phrase:'one angle is twice the smallest angle',isError:true},{phrase:'30\\u00b0 more than s',isError:false}"),
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
        for q in bank:
            print("    '%s': '%s'," % (q['id'], bc.content_hash(q)[:12]))
        print('}')
        return 0
    if bank is not None:
        check_bank(fails, bank, args.verbose)
    print('%s: %d items reviewed (keys, steps, explanations, phrases), every item played in Chromium at 390px'
          % (SLUG, len(bank) if bank else 0))

    ok = True
    if not args.no_selftest and not args.against:
        for qid, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-62s *** CANNOT PLANT: text not found once ***' % what)
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            # The pin catches any edit; a plant counts only when a substantive check names the item too.
            hit = [f for f in rep if f.startswith(qid) and 'changed since' not in f]
            ok = ok and bool(hit)
            print('  self-test %-62s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))

    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
