#!/usr/bin/env python3
# ci-line: Sequence Solver (every key recomputed from its own terms or formula, exactly; options distinct in value; every option marked in Chromium; no visible clock, score independent of time; every worked solution checked, Next above the fold) |
"""Sequence Solver: every key recomputed from the sequence or formula in its own question; every option clicked.

The game (154 multiple-choice items: ks3 50, gcse 45, alevel 59) covers next terms, common differences and
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
A fill-the-gaps ask must name the sequence type its key assumes (SR-17, sequence-solver-s1-001).
GCSE geometric items stay within A24 ("simple geometric progressions", r a rational number > 0): no negative or
zero ratio, and no ratio found from terms that are not next to each other. The five that went beyond it are A-level
items since SEQ-SOLVER-FIXES (Jon, 3 Nov 2026; sequence-solver-rr-002), each still keyed from its own terms.
The clock follows the Hidden Count-Up policy (timer-policy.md; Jon, 3 Nov 2026, rr-001), checked in Chromium on a
stubbed Date.now: the game screen does not change as time passes and has no Time label; every right answer scores
the same however long it took (1 s or 90 s); the results screen shows the total answering time.
Every item carries a worked solution (SEQ-SOLVER-WORKED, Jon, 3 Nov 2026), 1 to 3 steps, shown on a wrong answer under
the options and before Next. check_worked() reads it against the item, not the game's code: each "a = b = c" in its
maths is one value; the last step states the key (and a numeric key is its last number); a difference ("go up by"),
ratio ("multiplied by", "divided by", "common ratio is"), second difference or list of differences it states is
recomputed from the item's own terms. In Chromium a wrong answer shows the right option, then the worked solution, then
Next; a right answer shows none. The phone rule (canon 7.6.1) is measured on every wrong answer to every item.
A self-test plants r-001 back (0.999... beside 1), the B11 pair, gcse[44]'s old untyped ask ('Fill in the gaps'),
a negative ratio at GCSE, the HUD clock, a time multiplier in the score, a results line without the time, a missing
worked field, a last step that contradicts the key, a wrong difference, the worked solution not shown, and the phone
layout undone; each must FAIL naming its item.

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
COUNTS = {'ks3': 50, 'gcse': 45, 'alevel': 59}
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


def untex(s):
    """The text inside MaffsText's \\( \\) delimiters, which the game uses to mark maths (RAW-TEX-LAST-2)."""
    return s.replace('\\(', '').replace('\\)', '')


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
    for f in (untex(item['seq']), untex(item.get('q', ''))):
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
    ts = [t for t in terms(q['seq'])] if not untex(q['seq']).startswith('T_n') else []
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
    elif 'arithmetic' in q['ask']:
        d = (last - first) / k
        vals = [first + d * i for i in range(k + 1)]
    else:
        # SR-17 (SWEEP-1, sequence-solver-s1-001): a fill-the-gaps key holds only for the sequence type it assumes,
        # so the ask must name it.
        raise ValueError('the ask %r does not say whether the sequence is arithmetic or geometric (SR-17)' % q['ask'])
    for i, t in enumerate(ts):
        if t is not None and vals[i] != t:
            raise ValueError('the filled sequence misses the shown term %s' % t)
    return ('list', vals)


KS3 = [NEXT] * 12 + [DIFF] * 6 + [KTH] * 8 + [WHICH] * 2 + [NEXT] * 10 + [TYPE] * 6 + [NEXT] * 6
GCSE = ([NTH] * 10 + [TN_K, IS_TERM, IS_TERM, FIRST_ABOVE, WHICH_N, SECOND] + [NTH] * 9 + [SECOND, TN_K, TN_K, TN_K, IS_TERM]
        + [RATIO] * 3 + [NEXT, TN_K, TN_K, GP_TERM, GP_TERM]
        + [GEN, GEN, GEN, GEN, AP_FIRST_D, GEN, FILL])
# alevel[54:59]: the five geometric items moved from GCSE (SEQ-SOLVER-FIXES, rr-002), keyed from their own terms
ALEVEL_MOVED = [RATIO, GP_TERM, RATIO_TWO, RATIO_TWO, FILL]


def a24(fn, q):
    """Why a GCSE item goes beyond A24's simple geometric progressions (r rational and > 0), or None."""
    r = None
    if fn is RATIO:
        r = gp(terms(q['seq']))[1]
    elif fn is GP_TERM:
        r = F(re.search(r'r = (-?[\d.]+)', q['seq']).group(1))
    elif fn is NEXT:
        ts = [t for t in terms(q['seq']) if t is not None]
        if 'geometric' in next_terms(ts) and ts[0] != 0:
            r = gp(ts)[1]
    elif fn is RATIO_TWO:
        return 'the common ratio from two terms that are not next to each other (an A-level method)'
    elif fn is FILL and 'geometric' in q['ask']:
        return 'a geometric gap fill needs the ratio from terms that are not next to each other (an A-level method)'
    if r is not None and r <= 0:
        return 'a common ratio of %s (A24 needs r > 0)' % r
    return None


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
    ('Find S_{10} when a = 3, d = 4', V(S_ap(3, 4, 10))),
    ('Sum of first 20 terms if a = 5, l = 62', V(F(20, 2) * (5 + 62))),
    ('a = 2, d = 3|Find S_{20}', V(S_ap(2, 3, 20))),
    ('a = 10, d = -2|Find S_{15}', V(S_ap(10, -2, 15))),
    ('S_{10} = 200, a = 2|Find d', V((F(200) * 2 / 10 - 2 * 2) / 9)),
    ('5 + 8 + 11|Find S_{30}', V(S_ap(5, 3, 30))),
    ('a = 1, d = 1|Find S_{100}', V(S_ap(1, 1, 100))),
    ('a = 7, d = 5|first exceeds 100', ('n=', first_exceeding(lambda k: 7 + 5 * (k - 1), 100))),
    ('u_5 = 17, \\; u_{12} = 38.|Find d', V(F(38 - 17, 12 - 5))),
    ('u_5 = 17, d = 3|Find a', V(17 - 4 * 3)),
    ('last term } l|Which formula gives the sum?', ('verdict', 'S_n = \\dfrac{n}{2}(a + l)')),
    ('Sum of integers from 1 to } n|Formula', ('expr_n', sp.summation(sp.Symbol('r'), (sp.Symbol('r'), 1, n)))),
    ('Find S_5 when a = 3, r = 2', V(S_gp(3, 2, 5))),
    ('a = 1, r = 3|Find S_6', V(S_gp(1, 3, 6))),
    ('a = 100, r = 0.5|Find S_8 (2 d.p.)', V(half_up(S_gp(100, H, 8), 2))),
    ('a = 4, r = -2|Find S_6', V(S_gp(4, -2, 6))),
    ('a = 10, r = \\dfrac{1}{2}|Find S_4', V(S_gp(10, H, 4))),
    ('2 + 6 + 18 + 54|Find S_8', V(S_gp(2, 3, 8))),
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
    ('u_{n+1} = u_n + 3, \\; u_1 = 5|Find u_4', V(rec(5, lambda u, i: u + 3, 4))),
    ('u_{n+1} = 2u_n, \\; u_1 = 3|Find u_5', V(rec(3, lambda u, i: 2 * u, 5))),
    ('u_{n+1} = u_n + n, \\; u_1 = 1|Find u_4', V(rec(1, lambda u, i: u + i, 4))),
    ('u_{n+1} = u_n^2 - 1, \\; u_1 = 2|Find u_3', V(rec(2, lambda u, i: u * u - 1, 3))),
    ('Prove S_n for a = 1, d = 1', ('verdict', 'Substitute: \\(\\dfrac{n}{2}(2 + n - 1) = \\dfrac{n(n+1)}{2}\\)')),
    ('0.\\dot{9} = \\displaystyle\\sum_{r=1}^{\\infty} 9 \\times 10^{-r}|What does this sum equal?',
     V(F(9, 10) / (1 - F(1, 10)))),
    ('a = 12, \\; S_\\infty = 36|Find r', V(1 - F(12, 36))),
    ('a + ar + ar^2 + \\cdots = \\dfrac{a}{1-r}|This requires', ('verdict', '|r| < 1')),
    ('\\sum_{r=1}^{20} (3r - 2)|Evaluate', V(sum(3 * r - 2 for r in range(1, 21)))),
    ('S_{10} = 120 \\text{ and } S_{20} = 440|Find S_{30}', V(two_sums())),
]
AUDIT = {('alevel', 49): 'sequence-solver-r-001', ('gcse', 6): 'B11, audit F6', ('alevel', 23): 'sequence-solver-r-003, jc'}


def value_of(kind, o):
    """An option's value for comparison, by the kind of answer."""
    o = untex(o)
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
        if untex(q['correct']) != untex(target[1]):
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


# ---------------------------------------------------------------- worked solutions (SEQ-SOLVER-WORKED, Jon, 3 Nov 2026)
# A wrong answer shows the item's `worked` lines (1 to 3) under the options, before Next. Each line is checked against the
# item itself, never against the game's code: every "a = b = c" in its maths evaluates to one value; the last line states
# the key; and a difference, ratio or list of differences it states is recomputed from the item's own terms.
MATHSEG = re.compile(r'\\\((.*?)\\\)')
NUM = r'(-?\d+(?:\.\d+)?)'


def numeric(part):
    """One side of an '=' as an exact value, or None when it is not a single number (a letter, a list, an ellipsis)."""
    t = part.strip()
    bare = re.sub(r'\\(?:dfrac|frac|times|div|left|right)', '', t)
    if not t or re.search(r'[A-Za-z]|,|\.\.\.|\\cdots', bare):
        return None
    return expr(t.replace('\\div', '/').replace('\\left', '').replace('\\right', ''))


def first_diffs(ts):
    return [b - a for a, b in zip(ts, ts[1:])]


def shown_terms(q):
    """The item's terms when its sequence line is a list of numbers (a trailing gap dropped), else None."""
    try:
        ts = terms(untex(q['seq']))
    except (ValueError, ZeroDivisionError):
        return None
    while ts and ts[-1] is None:
        ts.pop()
    return ts if len(ts) >= 3 and None not in ts else None


def check_worked(fails, w, q):
    lines = q.get('worked')
    if not isinstance(lines, list) or not 1 <= len(lines) <= 3 or not all(isinstance(x, str) and x.strip() for x in lines):
        fails.append('%s: no worked solution of 1 to 3 steps (worked = %r)' % (w, lines))
        return
    for line in lines:
        if re.search('[–—]', line):
            fails.append('%s: a dash in the worked step "%s" (canon 7.1: no dash before a number)' % (w, line))
        for seg in MATHSEG.findall(line):
            if re.search(r'[<>]|\\geq|\\leq|\\neq', seg):
                continue
            vals = []
            for part in seg.split('='):
                try:
                    v = numeric(part)
                except ValueError as e:
                    fails.append('%s: cannot read "%s" in the worked step "%s" (%s)' % (w, part.strip(), line, e))
                    continue
                if v is not None:
                    vals.append((part.strip(), v))
            for p_, v in vals[1:]:
                if sp.simplify(v - vals[0][1]) != 0:
                    fails.append('%s: worked step "%s": %s is not %s' % (w, line, p_, vals[0][0]))
    norm = lambda x: re.sub(r'\s+', '', untex(x)).lower().rstrip('.')
    last, key = lines[-1], q['correct']
    if norm(key) not in norm(last):
        fails.append('%s: the last worked step "%s" does not state the key %s' % (w, last, key))
    elif re.fullmatch(NUM, key):
        nums = re.findall(r'(?<![\d.])' + NUM, untex(last))
        if not nums or F(nums[-1]) != F(key):
            fails.append('%s: the last worked step "%s" ends on %s, not the key %s' % (w, last, nums[-1] if nums else 'no number', key))
    ts = shown_terms(q)
    text = untex(' '.join(lines))
    if ts is None:
        return
    for m in re.finditer(r'go (up|down) by ' + NUM.replace('-?', ''), text):
        said = F(m.group(2)) * (1 if m.group(1) == 'up' else -1)
        try:
            d = ap(ts)[1]
        except ValueError:
            fails.append('%s: the worked solution says the terms go %s by %s, but %s is not arithmetic' % (w, m.group(1), m.group(2), q['seq']))
            continue
        if said != d:
            fails.append('%s: the worked solution says the terms go %s by %s; the difference of %s is %s' % (w, m.group(1), m.group(2), q['seq'], d))
    for m in re.finditer(r'common difference is ' + NUM, text):
        if F(m.group(1)) != ap(ts)[1]:
            fails.append('%s: the worked solution says the common difference is %s; it is %s' % (w, m.group(1), ap(ts)[1]))
    for m in re.finditer(r'(?:common ratio is|multiplied by|divided by) (-?\\dfrac\{\d+\}\{\d+\}|-?\d+(?:\.\d+)?)', text):
        said = number(m.group(1))
        if m.group(0).startswith('divided'):
            said = 1 / said
        try:
            r = sp.Rational(gp(ts)[1])
        except ValueError:
            fails.append('%s: the worked solution states a ratio, but %s is not geometric' % (w, q['seq']))
            continue
        if said != r:
            fails.append('%s: the worked solution says "%s"; the ratio of %s is %s' % (w, m.group(0), q['seq'], r))
    for m in re.finditer(r'second differences are (?:all )?' + NUM, text, re.I):
        d2 = set(first_diffs(first_diffs(ts)))
        if d2 != {F(m.group(1))}:
            fails.append('%s: the worked solution says the second differences are %s; they are %s' % (w, m.group(1), sorted(d2)))
    for m in re.finditer(r'(?:First differences:|gaps are|gaps grow by one each time:) (-?\d+(?:, -?\d+)+)', text):
        said = [F(x) for x in m.group(1).split(', ')]
        if said != first_diffs(ts)[:len(said)]:
            fails.append('%s: the worked solution lists the differences %s; they are %s' % (w, m.group(1), ', '.join(map(str, first_diffs(ts)))))


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
            if re.fullmatch(r'a = -?[\d.]+, r = -?[\d.]+', untex(q['seq'])) and 'ar^{n-1}' not in q.get('q', ''):
                fails.append('%s: an a/r item without the T_n = ar^{n-1} line leaves the type to the letter r (R2, sequence-solver-s1-004)' % w)
            try:
                if lv == 'alevel' and i >= len(ALEVEL):
                    target = ALEVEL_MOVED[i - len(ALEVEL)](q)
                elif lv == 'alevel':
                    words, target = ALEVEL[i]
                    text = (q.get('q', '') + '|' + q['ask']).replace('\\(', '').replace('\\)', '')   # MaffsText delimiters
                    for part in words.split('|'):
                        if part not in text:
                            raise ValueError('the item must say "%s" for its answer to hold' % part)
                else:
                    target = plans[lv][i](q)
                    why = a24(plans[lv][i], q) if lv == 'gcse' else None
                    if why:
                        fails.append('%s: beyond GCSE A24, %s; it belongs at A-level (sequence-solver-rr-002)' % (w, why))
            except (ValueError, AttributeError, IndexError) as e:
                fails.append('%s: %s' % (w, e))
                continue
            check_item(fails, w, q, target)
            check_worked(fails, w, q)


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
      // R8 (SWEEP-1 sequence-solver-s1-002, -003): no raw TeX on screen, and prose is never set in maths mode
      const vis = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(n => n.remove()); return c.textContent; };
      const promptText = vis(document.getElementById('prompt'));
      if (/\\|[A-Za-z]_[A-Za-z{]/.test(promptText)) out.push([lv, i, pick, 'raw TeX in the prompt: ' + promptText]);
      for (const o of shown) {
        if (/\\/.test(vis(o))) out.push([lv, i, o.dataset.val, 'raw TeX in an option: ' + vis(o)]);
        const bare = o.dataset.val.replace(/\\\(.*?\\\)/g, '').replace(/\\text\{[^}]*\}/g, '').replace(/\\[a-zA-Z]+/g, '');
        if (o.querySelector('.katex') && !/\\\(/.test(o.dataset.val) && /\b[A-Z][a-z]+\b|[a-z]{3,}/.test(bare))
          out.push([lv, i, o.dataset.val, 'prose set in maths mode (spaces lost, italic): ' + vis(o)]);
      }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
      // SEQ-SOLVER-WORKED: a wrong answer shows the right option, then the worked solution, then Next; a right one shows none
      const wk = document.getElementById('worked'), nx = document.querySelector('#nextMount button');
      if (pick === q.correct) {
        if (!wk.hidden) out.push([lv, i, pick, 'a worked solution shown on a right answer']);
      } else if (wk.hidden || wk.querySelectorAll('li').length !== (q.worked || []).length) {
        out.push([lv, i, pick, 'no worked solution on screen after a wrong answer']);
      } else {
        const key = document.querySelector('#options .opt-btn.correct').getBoundingClientRect(), wb = wk.getBoundingClientRect();
        if (!nx) out.push([lv, i, pick, 'no Next after a wrong answer']);
        else if (!(key.bottom <= wb.top + 1 && wb.bottom <= nx.getBoundingClientRect().top + 1))
          out.push([lv, i, pick, 'the order on screen is not: the right option, the worked solution, Next']);
        if (/\\/.test(vis(wk))) out.push([lv, i, pick, 'raw TeX in the worked solution: ' + vis(wk)]);
      }
    }
  });
  return out;
}"""


# The clock (timer-policy.md, Hidden Count-Up; Jon, 3 Nov 2026, SEQ-SOLVER-FIXES, sequence-solver-rr-001). Date.now is
# stubbed so the run is exact: a full 20-question GCSE round, every answer right, alternately 1 s and 90 s.
TIME_JS = r"""async () => {
  const out = [];
  let T = 1.7e12; Date.now = () => T;
  window.setTimeout = () => 0; window.setInterval = () => 0;   // adv() is called here, never by a timer
  const frames = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const seen = el => el.innerText;
  level = 'gcse';
  startGame();
  const game = document.getElementById('game');
  await frames();
  const before = seen(game);
  T += 7000; await frames();
  if (seen(game) !== before) out.push(['clock', 'the game screen changes as time passes (a visible clock)']);
  for (const el of game.querySelectorAll('*')) {
    if (el.offsetParent !== null && /^\s*time\s*$/i.test(el.textContent)) out.push(['clock', 'a "' + el.textContent.trim() + '" label on the game screen']);
  }
  const gains = [];
  for (let i = 0; i < totalQ; i++) {
    T += i % 2 ? 90000 : 1000;
    const q = questions[qIdx], was = score;
    const btn = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === q.correct);
    if (!btn) { out.push(['score', 'question ' + (i + 1) + ': the key is not on screen']); return out; }
    btn.click();
    gains.push(score - was);
    if (/time/i.test(seen(game))) out.push(['clock', 'question ' + (i + 1) + ': the game screen mentions time: ' + seen(game).replace(/\s+/g, ' ').slice(0, 80)]);
    adv();
  }
  if (new Set(gains).size !== 1 || gains[0] <= 0)
    out.push(['score', 'a right answer scores ' + gains[0] + ' after 1 s and ' + gains[1] + ' after 90 s (the score must not use time)']);
  const res = document.getElementById('results');
  if (!res.classList.contains('active')) out.push(['results', 'the results screen is not shown after ' + totalQ + ' answers']);
  const total = 7 + 10 * 1 + 10 * 90;   // the 7 s probe above is question 1's answering time too: 917 s
  const want = Math.floor(total / 60) + 'm ' + total % 60 + 's';
  if (!res.innerText.includes(want)) out.push(['results', 'the results screen does not show the total time ' + want + ': ' + res.innerText.replace(/\s+/g, ' ').slice(0, 120)]);
  return out;
}"""


# The phone rule (canon 7.6.1), measured on every wrong answer to every item (each wrong option leaves a different pair
# on screen): Next ends above the fold (the viewport less the 40px fixed footer), with no sideways scroll, at 320 x 568,
# 375 x 667 and 390 x 844, and in Aa mode at 375 x 667 and 390 x 844. Aa at 320 x 568 is canon's recorded exception:
# reported, not failed. Transitions are switched off so the settled layout is what is measured.
FIT_SIZES = [(False, 320, 568), (False, 375, 667), (False, 390, 844), (True, 375, 667), (True, 390, 844), (True, 320, 568)]
FIT_JS = r"""(aa) => {
  window.setTimeout = () => 0;
  const st = document.createElement('style'); st.textContent = '*{transition:none!important;animation:none!important}';
  document.head.appendChild(st);
  document.body.classList.toggle('accessible', aa);
  show('game');
  const out = [], fold = innerHeight - 40, W = document.documentElement.clientWidth;
  for (const lv of ['ks3', 'gcse', 'alevel']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of q.d) {
      questions = [q]; qIdx = 0; totalQ = 1; level = lv;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ(); scrollTo(0, 0);
      [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === pick).click();
      const nx = document.querySelector('#nextMount button');
      const bottom = nx ? Math.round(nx.getBoundingClientRect().bottom) : 1e6;
      if (bottom > fold || document.documentElement.scrollWidth > W)
        out.push([lv, i, pick, bottom - Math.round(fold), document.documentElement.scrollWidth > W]);
    }
  });
  return out;
}"""
NOTES = []


def context(browser, base, html, lock_fresh):
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    if lock_fresh:
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # the sweep clicks as soon as showQ() renders
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    # KaTeX comes from the pinned local copy, never the CDN (the verifier needs no outside host)
    ctx.route(lambda url: url.startswith(bc.KATEX_CDN), lambda route: (
        route.fulfill(**bc.real_font_response(route.request.url)) if bc.real_font_response(route.request.url)
        else route.abort()))
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
    return page, errors


def play(fails, html, fit=True):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page, errors = context(browser, base, html, True)
            bank = page.evaluate('() => QUESTIONS')
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d]%s in Chromium: option %s %s' % (lv, i, ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '', pick, what))
            page, errors2 = context(browser, base, html, True)
            for tag, what in page.evaluate(TIME_JS):
                fails.append('%s: %s (Hidden Count-Up, sequence-solver-rr-001)' % (tag, what))
            for aa, wd, ht in (FIT_SIZES if fit else []):
                page, more = context(browser, base, html, True)
                errors2 += more
                page.set_viewport_size({'width': wd, 'height': ht})
                over = page.evaluate(FIT_JS, aa)
                where = '%s at %d x %d' % ('Aa' if aa else 'normal mode', wd, ht)
                if aa and wd == 320:
                    NOTES.append('fit, %s (canon 7.6.1, the recorded exception): Next below the fold on %d of 462 wrong answers, worst %dpx'
                                 % (where, len(over), max([o[3] for o in over] or [0])))
                    continue
                for lv, i, pick, by, side in over[:5]:
                    fails.append('fit: %s[%d], wrong option %s, %s: %s (the phone rule, canon 7.6.1)'
                                 % (lv, i, pick, where, 'sideways scroll' if side and by <= 0 else 'Next %dpx below the fold' % by))
                if len(over) > 5:
                    fails.append('fit: %s: %d more wrong answers over the fold' % (where, len(over) - 5))
            browser.close()
            if errors or errors2:
                fails.append('page errors: %s' % '; '.join((errors + errors2)[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def run(html, fit=True):
    fails = []
    bank = play(fails, html, fit)
    if bank is not None:
        check_bank(fails, bank)
    return fails, sum(len(bank[k]) for k in COUNTS) if bank else 0


HUD_CLOCK = '<div class="hud-item"><div class="hud-label">Time</div><div class="hud-val" id="timer">0</div></div>'
PLANTS = [
    ('alevel[49]', 'r-001: 0.999... beside the key 1', [("correct:'1',d:['10','\\\\dfrac{9}{10}','\\\\infty']",
     "correct:'1',d:['0.999...','\\\\dfrac{9}{10}','\\\\infty']")]),
    ('gcse[6]', 'B11: 10 - 3n beside -3n + 10', [("d:['\\\\(-3n + 10\\\\)','\\\\(3n + 7\\\\)','\\\\(-3n + 7\\\\)']",
     "d:['\\\\(-3n + 10\\\\)','\\\\(10 - 3n\\\\)','\\\\(-3n + 7\\\\)']")]),
    ('alevel[48]', 'R8: raw TeX in the prompt', [("ask:'Prove \\\\(S_n\\\\) for \\\\(a = 1, d = 1\\\\) gives \\\\(\\\\dfrac{n(n+1)}{2}\\\\)'",
     "ask:'Prove S_n for a = 1, d = 1 gives \\\\dfrac{n(n+1)}{2}'")]),
    ('alevel[32]', 'R8: a prose key set in maths mode', [("correct:'No, \\\\(|r| \\\\geq 1\\\\)'", "correct:'No, |r| \\\\geq 1'")]),
    ('alevel[55]', 'R2: a/r item without the formula line', [("{seq:'\\\\(a = 2, r = -2\\\\)',q:'T_n = ar^{n-1}',", "{seq:'\\\\(a = 2, r = -2\\\\)',q:'',")]),
    ('gcse[44]', 'SR-17: fill the gaps, type unstated', [("ask:'If arithmetic, fill the gaps'", "ask:'Fill in the gaps'")]),
    ('gcse[30]', 'rr-002: a negative ratio back at GCSE', [("{seq:'3, 6, 12, 24, ...',ask:'What is the common ratio?',correct:'2',d:['3','4','6']",
     "{seq:'1, -3, 9, -27, ...',ask:'What is the common ratio?',correct:'-3',d:['3','-9','9']")]),
    ('clock', 'rr-001: the HUD clock back', [
     ('<div class="hud-item"><div class="hud-label">Streak</div><div class="hud-val" id="streak">0</div></div>',
      '<div class="hud-item"><div class="hud-label">Streak</div><div class="hud-val" id="streak">0</div></div>' + HUD_CLOCK),
     ("  qStartTime=Date.now();   // silent: nothing on screen reads it until the results\n",
      "  qStartTime=Date.now();const el=document.getElementById('timer');const tick=()=>{el.textContent=Math.floor((Date.now()-qStartTime)/1000);requestAnimationFrame(tick)};requestAnimationFrame(tick);\n")]),
    ('score', 'rr-001: time back in the score', [("score+=BASE;",
     "score+=Math.max(1,Math.round(BASE/(1+0.15*Math.log(1+(Date.now()-qStartTime)/1000))));")]),
    ('results', 'rr-001: no time on the results screen', [(" · Time: ${_m>0?_m+'m '+_s+'s':_s+'s'}`;", "`;")]),
    # SEQ-SOLVER-WORKED
    ('ks3[0]', 'WORKED: a missing worked field', [(",worked:['The terms go up by 2 each time.','So the next term is \\\\(8 + 2 = 10\\\\).']}", "}")]),
    ('ks3[1]', 'WORKED: last step contradicts the key', [("So the next term is \\\\(20 + 5 = 25\\\\).", "So the next term is \\\\(20 + 6 = 26\\\\).")]),
    ('ks3[2]', 'WORKED: a wrong difference', [("'The terms go up by 4 each time.','So the next term is \\\\(15 + 4 = 19\\\\).'",
                                              "'The terms go up by 3 each time.','So the next term is \\\\(15 + 4 = 19\\\\).'")]),
    ('ks3[0]', 'WORKED: not shown on a wrong answer', [("else{showWorked(q);MaffsNext.wrong(", "else{MaffsNext.wrong(")]),
    ('fit', 'WORKED: the phone rule undone', [("  #game.fb-open .opt-btn.disabled:not(.correct):not(.wrong){display:none}\n", "")], True),
]


def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument('--no-selftest', action='store_true')
    ap_.add_argument('--against', help='check this file as the game page')
    args = ap_.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, count = run(html)
    print('%s: %d items, every key recomputed, every option read and clicked in Chromium; every worked solution checked; '
          'every wrong answer measured at three phone sizes' % (SLUG, count))
    for n_ in NOTES[:1]:
        print('  note: ' + n_)
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, swaps, *fit in PLANTS:
            bad = [old for old, _ in swaps if html.count(old) != 1]
            if bad:
                print('  self-test %-38s *** CANNOT PLANT (%d) ***' % (what, html.count(bad[0])))
                ok = False
                continue
            planted = html
            for old, new in swaps:
                planted = planted.replace(old, new)
            rep, _ = run(planted, fit=bool(fit))   # the phone measurement runs only for the plant that needs it
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
