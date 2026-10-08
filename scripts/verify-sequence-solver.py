#!/usr/bin/env python3
# ci-line: B3 | Sequence Solver (every key recomputed from its own terms or formula, exactly; options distinct in value; every option marked in Chromium) |
"""Sequence Solver: every key recomputed from the sequence or formula in its own question; every option clicked.

The game (154 multiple-choice items: ks3 50, gcse 50, alevel 54) covers next terms, common differences and
ratios, nth terms, geometric terms, series, sums to infinity, sigma notation and recurrences. Its bank was keyed by
hand with no verifier; the resit audit of 4 Oct 2026 found alevel[49] (0.9 recurring as a sum, "What does this
sum equal?") offering "0.999..." beside the key 1 and marking it wrong: the same number, and the question's own
left-hand side (sequence-solver-r-001). gcse[6] offered -3n + 10 and 10 - 3n, equal in value (B11, audit F6).

KS3 and GCSE keys are computed from the item's own text: the shown terms (next terms by every simple rule that
fits them: arithmetic, geometric, constant second difference, Fibonacci-type, consecutive primes; all fitting
rules must agree), differences and ratios, a stated T_n formula read into SymPy, or a stated a, d, r. A-level
keys are computed here with exact fractions from the numbers in the item, each pinned to the words it reads;
the few whose answer is a formula or a sentence are a reviewed verdict, pinned too. Then, for every item:
  the key equals the answer; no wrong option equals it in value (SR-16); the four options are distinct strings
  and distinct in value (SR-4); and in Chromium (390x844) every option is clicked through handle(): the key
  marked right, the others wrong.
A self-test plants r-001 back (0.999... beside 1) and the B11 pair; each must FAIL naming its item.

    python scripts/verify-sequence-solver.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'sequence-solver'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'ks3': 50, 'gcse': 50, 'alevel': 54}
n = sp.Symbol('n', positive=True, integer=True)
INF = sp.oo


# ---------------------------------------------------------------- reading options and stems
def group(s, i):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '{') - (s[j] == '}')
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in %r' % s)


def tex(s):
    """A TeX expression (numbers, n, \\dfrac, ^, \\times, brackets) as Python text for SymPy."""
    out, i = '', 0
    s = s.replace('\\times', '*').replace('\u2212', '-')
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            a, j = group(s, i + m.end() - 1)
            b, k = group(s, j)
            out, i = out + '((%s)/(%s))' % (tex(a), tex(b)), k
            continue
        if s[i] == '{':
            a, j = group(s, i)
            out, i = out + '(%s)' % tex(a), j
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX in %r' % s)
        if s[i] == '^':
            out, i = out + '**', i + 1
            continue
        if s[i] in 'n(' and out.rstrip() and (out.rstrip()[-1].isdigit() or out.rstrip()[-1] in ')n'):
            out += '*'
        out, i = out + s[i], i + 1
    return out


def expr(s):
    try:
        return sp.nsimplify(sp.sympify(tex(s), locals={'n': n}), rational=True)
    except Exception as e:
        raise ValueError('cannot read %r: %s' % (s, e))


def number(s):
    """An option as an exact value: integers, decimals, '0.999...' (a recurring last digit), \\dfrac, \\infty."""
    t = s.strip().replace('\u2212', '-')
    if t in ('\\infty', '\u221e'):
        return INF
    m = re.fullmatch(r'(-?)(\d+)\.(\d*?)(\d)\4*\.\.\.', t)
    if m:
        sign, whole, pre, rep = m.groups()
        val = F(int(whole)) + (F(int(pre)) if pre else 0) / 10 ** len(pre) + F(int(rep), 9) / 10 ** len(pre)
        return sp.Rational(-val if sign else val)
    if re.fullmatch(r'-?\d+(\.\d+)?', t):
        return sp.Rational(t)
    m = re.fullmatch(r'(-?)\\dfrac\{(\d+)\}\{(\d+)\}', t)
    if m:
        v = sp.Rational(int(m.group(2)), int(m.group(3)))
        return -v if m.group(1) else v
    raise ValueError('not a number: %r' % s)


def terms(seq):
    """The numbers shown in a sequence line, with None for a gap ('__')."""
    out = []
    for p in seq.split(','):
        p = p.strip()
        if p in ('__', '...', ''):
            if p == '__':
                out.append(None)
            continue
        out.append(F(p))
    return out


def tn(item):
    """The T_n formula an item states (in seq or q), as SymPy in n."""
    for f in (item['seq'], item.get('q', '')):
        m = re.match(r'T_n = (.+)$', f or '')
        if m:
            return expr(m.group(1))
    raise ValueError('no T_n formula')


# ---------------------------------------------------------------- rules that fit shown terms
def is_prime(k):
    return k > 1 and all(k % p for p in range(2, int(k ** 0.5) + 1))


def next_terms(ts):
    """{rule: next term} for every simple rule that fits the shown terms."""
    out = {}
    d = [b - a for a, b in zip(ts, ts[1:])]
    if len(set(d)) == 1:
        out['arithmetic'] = ts[-1] + d[0]
    if all(t != 0 for t in ts[:-1]):
        r = [b / a for a, b in zip(ts, ts[1:])]
        if len(set(r)) == 1:
            out['geometric'] = ts[-1] * r[0]
    d2 = [b - a for a, b in zip(d, d[1:])]
    if len(ts) >= 4 and len(set(d2)) == 1 and d2[0] != 0:
        out['quadratic'] = ts[-1] + d[-1] + d2[0]
    if len(ts) >= 4 and all(ts[i] == ts[i - 1] + ts[i - 2] for i in range(2, len(ts))):
        out['fibonacci'] = ts[-1] + ts[-2]
    if all(t.denominator == 1 and is_prime(int(t)) for t in ts):
        ps = [p for p in range(2, int(ts[-1]) * 2 + 3) if is_prime(p)]
        i0 = ps.index(int(ts[0]))
        if [F(p) for p in ps[i0:i0 + len(ts)]] == ts:
            out['primes'] = F(ps[i0 + len(ts)])
    return out


def family_fits(name, ts):
    k = len(ts)
    seqs = {'Square numbers': [F(i * i) for i in range(1, k + 1)],
            'Triangular numbers': [F(i * (i + 1), 2) for i in range(1, k + 1)],
            'Triangular': [F(i * (i + 1), 2) for i in range(1, k + 1)],
            'Cube numbers': [F(i ** 3) for i in range(1, k + 1)],
            'Powers of 2': [F(2 ** i) for i in range(0, k)]}
    if name in seqs:
        return ts == seqs[name]
    rule = {'Arithmetic': 'arithmetic', 'Geometric': 'geometric', 'Quadratic': 'quadratic', 'Fibonacci': 'fibonacci'}[name]
    return rule in next_terms(ts)


# ---------------------------------------------------------------- answers
def V(x):
    return ('val', sp.nsimplify(x, rational=True) if x is not INF else INF)


def kth(item):
    m = re.search(r'Find the (\d+)(?:st|nd|rd|th) term', item['ask'])
    return int(m.group(1))


def ap(ts):
    d = {b - a for a, b in zip(ts, ts[1:])}
    if len(d) != 1:
        raise ValueError('the terms are not arithmetic')
    return ts[0], d.pop()


def gp(ts):
    r = {b / a for a, b in zip(ts, ts[1:])}
    if len(r) != 1:
        raise ValueError('the terms are not geometric')
    return ts[0], r.pop()


def NEXT(q):
    rules = next_terms([t for t in terms(q['seq']) if t is not None])
    if not rules:
        raise ValueError('no simple rule fits the terms')
    if len(set(rules.values())) != 1:
        raise ValueError('rules disagree on the next term: %s' % rules)
    return V(list(rules.values())[0])


def DIFF(q):
    return V(ap(terms(q['seq']))[1])


def RATIO(q):
    return V(gp(terms(q['seq']))[1])


def KTH(q):
    a, d = ap(terms(q['seq']))
    return V(a + (kth(q) - 1) * d)


def WHICH(q):
    a, d = ap(terms(q['seq']))
    x = F(re.search(r'equals (-?\d+)', q['ask']).group(1))
    k = (x - a) / d + 1
    return ('ord', int(k)) if k.denominator == 1 and k >= 1 else ('ord', None)


def TYPE(q):
    ts = terms(q['seq'])
    return ('family', ts)


def NTH(q):
    return ('expr', [t for t in terms(q['seq'])])


def SECOND(q):
    ts = terms(q['seq'])
    d = [b - a for a, b in zip(ts, ts[1:])]
    d2 = {b - a for a, b in zip(d, d[1:])}
    if len(d2) != 1:
        raise ValueError('second differences not constant')
    return V(d2.pop())


def TN_K(q):
    f = tn(q)
    ts = [t for t in terms(q['seq'])] if not q['seq'].startswith('T_n') else []
    for i, t in enumerate(ts, 1):
        if f.subs(n, i) != t:
            raise ValueError('T_n does not give the shown term %s' % t)
    return V(f.subs(n, kth(q)))


def IS_TERM(q):
    f, x = tn(q), int(re.search(r'Is (-?\d+) a term', q['ask']).group(1))
    sols = [s for s in sp.solve(sp.Eq(f, x), n) if s.is_integer and s >= 1]
    return ('yesno', int(sols[0]) if sols else None)


def FIRST_ABOVE(q):
    f, x = tn(q), int(re.search(r'above (-?\d+)', q['ask']).group(1))
    k = 1
    while f.subs(n, k) <= x:
        k += 1
    return ('first', (int(f.subs(n, k)), k))


def WHICH_N(q):
    f, x = tn(q), int(re.search(r'equals (-?\d+)', q['ask']).group(1))
    sols = [s for s in sp.solve(sp.Eq(f, x), n) if s.is_integer and s >= 1]
    return ('n=', int(sols[0]) if sols else None)


def GEN(q):
    f = tn(q)
    return ('list', [F(str(f.subs(n, k))) for k in range(1, 5)])


def GP_TERM(q):
    a = F(re.search(r'a = (-?[\d.]+)', q['seq']).group(1))
    r = F(re.search(r'r = (-?[\d.]+)', q['seq']).group(1))
    return V(a * r ** (kth(q) - 1))


def RATIO_TWO(q):
    m = re.fullmatch(r'The (\d)\w\w term is (\d+), the (\d)\w\w term is (\d+)\.', q['seq'])
    i, x, j, y = (int(g) for g in m.groups())
    r = sp.Rational(y, x) ** sp.Rational(1, j - i)
    return V(r)


def AP_FIRST_D(q):
    m = re.fullmatch(r'The first term is (-?\d+), the common difference is (-?\d+)\.', q['seq'])
    a, d = F(m.group(1)), F(m.group(2))
    return V(a + (kth(q) - 1) * d)


def FILL(q):
    ts = terms(q['seq'])
    gaps = [i for i, t in enumerate(ts) if t is None]
    first, last, k = ts[0], ts[-1], len(ts) - 1
    if 'geometric' in q['ask']:
        r = sp.Rational(last / first) ** sp.Rational(1, k)
        vals = [F(str(first * r ** i)) for i in range(k + 1)]
    else:
        d = (last - first) / k
        vals = [first + d * i for i in range(k + 1)]
    for i, t in enumerate(ts):
        if t is not None and vals[i] != t:
            raise ValueError('the filled sequence misses the shown term %s' % t)
    return ('list', vals)


KS3 = [NEXT] * 12 + [DIFF] * 6 + [KTH] * 8 + [WHICH] * 2 + [NEXT] * 10 + [TYPE] * 6 + [NEXT] * 6
GCSE = ([NTH] * 10 + [TN_K, IS_TERM, IS_TERM, FIRST_ABOVE, WHICH_N, SECOND] + [NTH] * 9 + [SECOND, TN_K, TN_K, TN_K, IS_TERM]
        + [RATIO] * 4 + [NEXT, TN_K, TN_K, GP_TERM, GP_TERM, GP_TERM, RATIO_TWO, RATIO_TWO]
        + [GEN, GEN, GEN, GEN, AP_FIRST_D, GEN, FILL, FILL])


def S_ap(a, d, k):
    return F(k, 2) * (2 * a + (k - 1) * d)


def S_gp(a, r, k):
    return a * (1 - r ** k) / (1 - r)


def first_exceeding(term, bound):
    k = 1
    while term(k) <= bound:
        k += 1
    return k


def rec(u1, step, k):
    u = u1
    for i in range(1, k):
        u = step(u, i)
    return u


def two_sums():
    a, d = sp.symbols('a d')
    s = sp.solve([sp.Eq(5 * (2 * a + 9 * d), 120), sp.Eq(10 * (2 * a + 19 * d), 440)], [a, d])
    return F(str(S_ap(F(str(s[a])), F(str(s[d])), 30)))


def half_up(v, dp):
    return F(str((Decimal(v.numerator) / Decimal(v.denominator)).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)))


H = F(1, 2)
# (words the item must carry, answer). Every A-level answer from the item's own numbers.
ALEVEL = [
    ('Find S\u2081\u2080 when a = 3, d = 4', V(S_ap(3, 4, 10))),
    ('Sum of first 20 terms if a = 5, l = 62', V(F(20, 2) * (5 + 62))),
    ('a = 2, d = 3|Find S\u2082\u2080', V(S_ap(2, 3, 20))),
    ('a = 10, d = -2|Find S\u2081\u2085', V(S_ap(10, -2, 15))),
    ('S_{10} = 200, a = 2|Find d', V((F(200) * 2 / 10 - 2 * 2) / 9)),
    ('5 + 8 + 11|Find S\u2083\u2080', V(S_ap(5, 3, 30))),
    ('a = 1, d = 1|Find S\u2081\u2080\u2080', V(S_ap(1, 1, 100))),
    ('a = 7, d = 5|first exceeds 100', ('n=', first_exceeding(lambda k: 7 + 5 * (k - 1), 100))),
    ('u_5 = 17, \\; u_{12} = 38.|Find d', V(F(38 - 17, 12 - 5))),
    ('u_5 = 17, d = 3|Find a', V(17 - 4 * 3)),
    ('last term } l|Which formula gives the sum?', ('verdict', 'S_n = \\dfrac{n}{2}(a + l)')),
    ('Sum of integers from 1 to } n|Formula', ('expr_n', sp.summation(sp.Symbol('r'), (sp.Symbol('r'), 1, n)))),
    ('Find S\u2085 when a = 3, r = 2', V(S_gp(3, 2, 5))),
    ('a = 1, r = 3|Find S\u2086', V(S_gp(1, 3, 6))),
    ('a = 100, r = 0.5|Find S\u2088 (2 d.p.)', V(half_up(S_gp(100, H, 8), 2))),
    ('a = 4, r = -2|Find S\u2086', V(S_gp(4, -2, 6))),
    ('a = 10, r = \\dfrac{1}{2}|Find S\u2084', V(S_gp(10, H, 4))),
    ('2 + 6 + 18 + 54|Find S\u2088', V(S_gp(2, 3, 8))),
    ('u_1 = 5, \\; u_4 = 40.|Find r', V(sp.Rational(40, 5) ** sp.Rational(1, 3))),
    ('u_3 = 12, \\; u_6 = 96|Find r', V(sp.Rational(96, 12) ** sp.Rational(1, 3))),
    ('u_3 = 12, r = 2|Find a', V(F(12, 4))),
    ('a = 5, r = 3|first exceeds 1000', ('n=', first_exceeding(lambda k: 5 * 3 ** (k - 1), 1000))),
    ('a = 8, r = \\dfrac{1}{4}|Find the 4th term', V(8 * F(1, 4) ** 3)),
    ('Sum of GP|Which formula when |r| < 1?', ('verdict', 'S_n = \\dfrac{a(1-r^n)}{1-r}')),   # sequence-solver-r-003 (jc)
    ('a = 10, r = 0.5', V(10 / (1 - H))),
    ('a = 6, r = \\dfrac{1}{3}', V(6 / (1 - F(1, 3)))),
    ('a = 100, r = 0.1', V(100 / (1 - F(1, 10)))),
    ('a = 4, r = -\\dfrac{1}{2}', V(4 / (1 + H))),
    ('a = 1, r = \\dfrac{2}{3}', V(1 / (1 - F(2, 3)))),
    ('S_\\infty = 12, \\; a = 4|Find r', V(1 - F(4, 12))),
    ('S_\\infty = 20, \\; r = 0.5|Find a', V(20 * (1 - H))),
    ('a = 5, r = 0.9|converge', ('converges', F(9, 10))),
    ('a = 3, r = 1.1|converge', ('converges', F(11, 10))),
    ('a = 2, r = -0.8|converge', ('converges', F(-8, 10))),
    ('\\sum_{r=1}^{5} r|Evaluate', V(sum(range(1, 6)))),
    ('\\sum_{r=1}^{4} r^2|Evaluate', V(sum(r * r for r in range(1, 5)))),
    ('\\sum_{r=1}^{5} 2r|Evaluate', V(sum(2 * r for r in range(1, 6)))),
    ('\\sum_{r=1}^{4} (3r + 1)|Evaluate', V(sum(3 * r + 1 for r in range(1, 5)))),
    ('\\sum_{r=0}^{3} 2^r|Evaluate', V(sum(2 ** r for r in range(0, 4)))),
    ('\\sum_{r=1}^{100} 1|Evaluate', V(100)),
    ('\\sum_{r=1}^{n} r = |Formula', ('expr_n', sp.summation(sp.Symbol('r'), (sp.Symbol('r'), 1, n)))),
    ('\\sum_{r=1}^{10} (2r - 1)|Evaluate', V(sum(2 * r - 1 for r in range(1, 11)))),
    ('\\sum_{r=1}^{\\infty} \\left(\\dfrac{1}{2}\\right)^r|Evaluate', V(H / (1 - H))),
    ('\\sum_{r=1}^{\\infty} 3 \\left(\\dfrac{1}{4}\\right)^r|Evaluate', V(3 * F(1, 4) / (1 - F(1, 4)))),
    ('u_{n+1} = u_n + 3, \\; u_1 = 5|Find u\u2084', V(rec(5, lambda u, i: u + 3, 4))),
    ('u_{n+1} = 2u_n, \\; u_1 = 3|Find u\u2085', V(rec(3, lambda u, i: 2 * u, 5))),
    ('u_{n+1} = u_n + n, \\; u_1 = 1|Find u\u2084', V(rec(1, lambda u, i: u + i, 4))),
    ('u_{n+1} = u_n^2 - 1, \\; u_1 = 2|Find u\u2083', V(rec(2, lambda u, i: u * u - 1, 3))),
    ('Prove S_n for a = 1, d = 1', ('verdict', 'Substitute: \\dfrac{n}{2}(2 + n - 1) = \\dfrac{n(n+1)}{2}')),
    ('0.\\dot{9} = \\displaystyle\\sum_{r=1}^{\\infty} 9 \\times 10^{-r}|What does this sum equal?',
     V(F(9, 10) / (1 - F(1, 10)))),
    ('a = 12, \\; S_\\infty = 36|Find r', V(1 - F(12, 36))),
    ('a + ar + ar^2 + \\cdots = \\dfrac{a}{1-r}|This requires', ('verdict', '|r| < 1')),
    ('\\sum_{r=1}^{20} (3r - 2)|Evaluate', V(sum(3 * r - 2 for r in range(1, 21)))),
    ('S_{10} = 120 \\text{ and } S_{20} = 440|Find S\u2083\u2080', V(two_sums())),
]
AUDIT = {('alevel', 49): 'sequence-solver-r-001', ('gcse', 6): 'B11, audit F6', ('alevel', 23): 'sequence-solver-r-003, jc'}


def value_of(kind, o):
    """An option's value for comparison, by the kind of answer."""
    if kind in ('val',):
        return number(o)
    if kind == 'ord':
        m = re.fullmatch(r'(\d+)(st|nd|rd|th)', o)
        if not m:
            raise ValueError('not an ordinal: %r' % o)
        return int(m.group(1))
    if kind == 'n=':
        m = re.fullmatch(r'n = (\d+)', o)
        if not m:
            raise ValueError('not "n = k": %r' % o)
        return int(m.group(1))
    if kind == 'yesno':
        if o == 'No':
            return None
        m = re.fullmatch(r'Yes \(n = (\d+)\)', o)
        if not m:
            raise ValueError('not Yes (n = k) / No: %r' % o)
        return int(m.group(1))
    if kind == 'first':
        m = re.fullmatch(r'(-?\d+) \(n = (\d+)\)', o)
        if not m:
            raise ValueError('not "x (n = k)": %r' % o)
        return (int(m.group(1)), int(m.group(2)))
    if kind == 'list':
        return [F(p.strip()) for p in o.split(',')]
    if kind in ('expr', 'expr_n'):
        return expr(o)
    if kind in ('verdict', 'converges', 'family'):
        return o
    raise ValueError(kind)


def check_item(fails, w, q, target):
    kind = target[0]
    opts = [q['correct']] + q['d']
    if len(q['d']) != 3 or len(set(opts)) != 4:
        fails.append('%s: the options %s are not four distinct strings' % (w, opts))
    if kind == 'verdict':
        if q['correct'] != target[1]:
            fails.append('%s: keyed %r, reviewed %r' % (w, q['correct'], target[1]))
        return
    if kind == 'converges':
        conv = abs(target[1]) < 1
        if q['correct'].startswith('Yes') != conv:
            fails.append('%s: keyed %r, but the series %s (|r| = %s)' % (w, q['correct'], 'converges' if conv else 'diverges', abs(target[1])))
        for o in q['d']:
            if o.startswith('Yes') == conv and o.startswith('Yes'):
                fails.append('%s: the wrong option %r also says it converges' % (w, o))
        return
    if kind == 'family':
        ts = target[1]
        if not family_fits(q['correct'], ts):
            fails.append('%s: keyed %r, which does not fit %s' % (w, q['correct'], q['seq']))
        for o in q['d']:
            if family_fits(o, ts):
                fails.append('%s: the wrong option %r also fits %s' % (w, o, q['seq']))
        return
    try:
        vals = [value_of(kind, o) for o in opts]
    except ValueError as e:
        fails.append('%s: %s (extend value_of())' % (w, e))
        return
    if kind == 'expr':
        ts = target[1]
        fits = lambda e: all(sp.simplify(e.subs(n, i) - t) == 0 for i, t in enumerate(ts, 1))
        if not fits(vals[0]):
            fails.append('%s: keyed %s, which does not give %s' % (w, q['correct'], q['seq']))
        for o, v in zip(opts[1:], vals[1:]):
            if fits(v):
                fails.append('%s: the wrong option %s also gives %s (SR-16)' % (w, o, q['seq']))
        same = lambda a, b: sp.simplify(a - b) == 0
    elif kind == 'expr_n':
        if sp.simplify(vals[0] - target[1]) != 0:
            fails.append('%s: keyed %s, the formula is %s' % (w, q['correct'], target[1]))
        for o, v in zip(opts[1:], vals[1:]):
            if sp.simplify(v - target[1]) == 0:
                fails.append('%s: the wrong option %s equals the formula (SR-16)' % (w, o))
        same = lambda a, b: sp.simplify(a - b) == 0
    else:
        want = target[1]
        if vals[0] != want:
            fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], want))
        for o, v in zip(opts[1:], vals[1:]):
            if v == want:
                fails.append('%s: the wrong option %s equals the answer (SR-16)' % (w, o))
        same = lambda a, b: a == b
    for i in range(4):
        for k in range(i + 1, 4):
            if same(vals[i], vals[k]):
                fails.append('%s: options %s and %s are equal in value (SR-4)' % (w, opts[i], opts[k]))


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs this script reviewed)' % (counts, COUNTS))
        return
    plans = {'ks3': KS3, 'gcse': GCSE}
    for lv in COUNTS:
        for i, q in enumerate(bank[lv]):
            w = '%s[%d] (%s | %s | %s)%s' % (lv, i, q['seq'], q.get('q', ''), q['ask'],
                                             ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            try:
                if lv == 'alevel':
                    words, target = ALEVEL[i]
                    text = q.get('q', '') + '|' + q['ask']
                    for part in words.split('|'):
                        if part not in text:
                            raise ValueError('the item must say "%s" for its answer to hold' % part)
                else:
                    target = plans[lv][i](q)
            except (ValueError, AttributeError, IndexError) as e:
                fails.append('%s: %s' % (w, e))
                continue
            check_item(fails, w, q, target)


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  for (const lv of ['ks3', 'gcse', 'alevel']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      questions = [q]; qIdx = 0; totalQ = 1; level = lv; score = 0; correctCount = 0; streak = 0;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([lv, i, pick, shown.length + ' options on screen']);
      const btn = shown.find(x => x.dataset.val === pick);
      if (!btn) { out.push([lv, i, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
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
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # the sweep clicks as soon as showQ() renders
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d]%s in Chromium: option %s %s' % (lv, i, ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '', pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def run(html):
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    return fails, sum(len(bank[k]) for k in COUNTS) if bank else 0


PLANTS = [
    ('alevel[49]', 'r-001: 0.999... beside the key 1', "correct:'1',d:['10','\\\\dfrac{9}{10}','\\\\infty']",
     "correct:'1',d:['0.999...','\\\\dfrac{9}{10}','\\\\infty']"),
    ('gcse[6]', 'B11: 10 - 3n beside -3n + 10', "d:['-3n + 10','3n + 7','-3n + 7']", "d:['-3n + 10','10 - 3n','-3n + 7']"),
]


def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument('--no-selftest', action='store_true')
    ap_.add_argument('--against', help='check this file as the game page')
    args = ap_.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, count = run(html)
    print('%s: %d items, every key recomputed, every option read and clicked in Chromium' % (SLUG, count))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-38s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep, _ = run(html.replace(old, new))
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-38s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
