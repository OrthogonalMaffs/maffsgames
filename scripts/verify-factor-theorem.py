#!/usr/bin/env python3
# ci-line: Factor Theorem (every key from its item's polynomial; ACCEPTED lists = page; every form marked in Chromium; answer buttons; A-Level only; no Practice submit) |
"""Factor Theorem: every key recomputed from its item's own polynomial; every typed answer marked by look-up.

The tranche 5 audit (6 Oct 2026) found comma blanks matched in any order, so (x - 2)(x + 3) passed for
(x - 3)(x + 2) (t5-001); typed algebra marked as an exact string, so a right answer with its factors in another
order, x^2 for x², a Greek letter by name or "x =" after an "x =" label was marked wrong (t5-002); T4(b) keyed a
factorisation that is not p(x) (t5-003); two keys that did not answer their question's ask (t5-006, t5-007); a
"Find k" with no k (t5-010), a hint naming a value that is not a root (t5-011) and Learn example 4's candidate list
(t5-012). Project Claude replaced T4 (7 Oct 2026): a = -19, b = 30, p(x) = (x - 3)(x - 2)(x + 5).

Keys. Each item's polynomial is read from its own prompt (SymPy). SPEC says what each answer is (a remainder, a
  parameter from the stated conditions, the full factorisation, the roots); every condition SPEC uses must appear
  in the item's text (NEEDS), so a changed number in the question fails here. A factorisation must multiply out to
  the polynomial with every factor linear. The ask must match the key: a typed answer to "factorise" is a
  factorisation, to "solve" / "find all values" the roots.
Scaffold blanks. STEPS gives each step's target (the value or expression its line works out, from the item's
  polynomial); the line is read with its blanks as unknowns and solved. Every solution is accepted, so a
  symmetric pair, (s + 1)(s + 2), takes either order and an asymmetric one, (x - 3)(x + 2), one only; the key
  must be a solution, and a one-blank line must have exactly one. Every other '=' in a line that reads as maths
  must equal its target too, and every shown working line must equal its value.
Hints. "Try x = r" names a root; "Quotient is Q" divides the polynomial to a linear factor; a factorisation
  "= (A)(B)" multiplies out to the line before; Learn example 4's candidates are +-(factors of 6)/(factors of 2).
ACCEPTED. The forms of each answer that are right are generated here and must equal the page's block (--write
  regenerates it): factors in any order, a repeated factor squared or written twice, roots in any order with
  "x =" on all, none or the first, a terminating decimal for a fraction, named values in any order. Each form is
  read back and must mean the key.
Chromium (390x844, KaTeX). Every practice item and test question is rendered and marked through the game's own
  Check: the key is marked right; sampled ACCEPTED forms, typed with spaces, a real minus sign, superscripts,
  "f(x) =" and upper case, are marked right; a factor or root with its sign flipped, and every order of a blank
  pair that is not a solution, are marked wrong; no item makes the page scroll sideways.

Answer buttons (FT-FIX, Jon 8-9 Oct 2026; t5-004, t5-005). Practice Q33 (the proof) and T9(c) (the interpretation)
  are four buttons each, marked by dataset.val: their options must be the contract's, word for word. Q33: each line's
  working is checked for every positive integer n, and only a line with f(a) = 0 that names (x - a) proves it; only
  the key may. T9(c): from s(t) in the question, every wrong option is false at every t it names (v = ds/dt and
  a = dv/dt are not 0 there, so no rest, turn or zero acceleration), and the key holds (single roots, v not 0); the
  explanation's v and its worked value are recomputed. In Chromium each option is chosen and marked once: the key
  right, the others wrong, the buttons off, the explanation shown, a wrong choice followed by the shared Next
  control; shown twenty times, the buttons come in more than one order. Every typed key is maths, never prose (one-
  letter names, Greek letters by name and "factor" only).
A-Level only (Jon, 9 Oct 2026). With no ?level, ?level=alevel, level4, xyz and __proto__, in a fresh page each: every
  event logs level 'alevel', the given value is never logged or submitted, Practice played to its end submits
  nothing (t5-014, t5-015), and the Test submits once, to factor_theorem_alevel.
A wrong answer waits on the shared Next control (canon 7.6), a right one on the Next Question button (t5-018's note).

A self-test plants the audit's faults back (t5-001: the pair (x - 2)(x + 3) accepted for Q6; t5-003: the old T4;
Q33's and T9(c)'s old free-text keys; a prose key; a Practice submit; ?level logged; a wrong answer advanced by the
Next button); each must FAIL naming its item.

    python scripts/verify-factor-theorem.py [--write] [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import itertools
import json
import os
import re
import sys
from collections import Counter
from fractions import Fraction

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication, parse_expr, split_symbols_custom,
                                        standard_transformations)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import bank_common as bc  # noqa: E402

SLUG = 'factor-theorem'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
START = '// >>> GENERATED ACCEPTED START\n'
END = '// >>> GENERATED ACCEPTED END\n'

x, s, w, th, lam, t = sp.symbols('x s omega theta lam t')
a, b, c, k, p, q = sp.symbols('a b c k p q')
VARS = {'x': x, 's': s, 'ω': w, 'θ': th, 'λ': lam, 't': t}
NAMES = {'omega': 'ω', 'theta': 'θ', 'lam': 'λ'}
LOCAL = {'x': x, 's': s, 'omega': w, 'theta': th, 'lam': lam, 't': t, 'a': a, 'b': b, 'c': c, 'k': k, 'p': p,
         'q': q, 'f': sp.Function('f'), 'd': sp.Symbol('d')}
TRANSFORMS = standard_transformations + (
    split_symbols_custom(lambda n: n not in ('omega', 'theta', 'lam') and not n.startswith('B')),
    implicit_multiplication, convert_xor)

# Where an audit item names an answer, failures there say so.
AUDIT = {'T4.0': 't5-003', 'T4.1': 't5-003', 'p24': 't5-006', 'p38': 't5-007', 'p20': 't5-010', 'p22': 't5-011',
         'p33': 't5-004', 'T9.2': 't5-005'}


def tag(uid):
    return '%s (factor-theorem-%s)' % (uid, AUDIT[uid]) if uid in AUDIT else uid


def canon(raw):
    """Python copy of the page's canon(); the sweep proves the two agree."""
    r = str(raw).lower()
    r = re.sub('[−–—]', '-', r).replace('²', '^2').replace('³', '^3').replace('½', '1/2')
    r = r.replace('omega', 'ω').replace('theta', 'θ').replace('lambda', 'λ')
    r = re.sub(r'\band\b', ',', r).replace(';', ',')
    r = re.sub('[\\s*×·]', '', r)
    r = re.sub(r'\.$', '', r)
    r = re.sub(r'^[a-zθωλ]\([a-zθωλ]\)=', '', r)
    return re.sub(r'^=', '', r)


def to_py(text):
    """Typed or TeX maths as SymPy input."""
    r = text.replace('\\(', '').replace('\\)', '')
    r = re.sub(r'\\text\{[^}]*\}', '', r)
    r = r.replace('\\lambda', 'lam').replace('\\omega', 'omega').replace('\\theta', 'theta')
    r = r.replace('λ', 'lam').replace('ω', 'omega').replace('θ', 'theta')
    r = re.sub('[−–—]', '-', r).replace('²', '^2').replace('³', '^3').replace('½', '(1/2)')
    r = r.replace('×', '*').replace('÷', '/').replace('·', '*')
    n = [0]

    def blank(_):
        n[0] += 1
        return ' B%d ' % (n[0] - 1)
    r = re.sub('___', blank, r)
    return r


def parse(text):
    return parse_expr(to_py(text), local_dict=dict(LOCAL, **{'B%d' % i: sp.Symbol('B%d' % i) for i in range(4)}),
                      transformations=TRANSFORMS, evaluate=True)


def cubic(text):
    """The polynomial an item's text states: the first maths with a cube, its side of any '=' with the cube."""
    segs = re.findall(r'\\\((.*?)\\\)', text) or [text]
    seg = next(z for z in segs if '^3' in z or '³' in z)
    for part in seg.split('='):
        if '^3' in part or '³' in part:
            seg = part
            break
    return sp.expand(parse(seg.split(',')[0]))


def var_of(F):
    for v in VARS.values():
        if F.has(v):
            return v
    raise ValueError(F)


def rq(val):
    """A rational as the page writes it: '-3', '1/2'."""
    val = sp.Rational(val)
    return str(val.p) if val.q == 1 else '%d/%d' % (val.p, val.q)


# ── what each answer is, from the item's polynomial and its stated conditions ──
def fact(F, sub=None):
    return ('fact', sp.expand(F.subs(sub or {})))


def roots(F, sub=None):
    G = sp.expand(F.subs(sub or {}))
    return ('roots', frozenset(sp.roots(sp.Poly(G, var_of(G))).keys()))


def num(v):
    return ('num', sp.Rational(v))


def solve1(F, conds, unknowns):
    sol = sp.solve(conds, unknowns, dict=True)
    assert len(sol) == 1, (conds, sol)
    return sol[0]


def at(F, r):
    return sp.expand(F.subs(var_of(F), r))


def quo(F, r):
    v = var_of(F)
    qq, rr = sp.div(F, v - r, v)
    assert rr == 0, (F, r)
    return sp.expand(qq)


# id -> (what the answer is, text the conditions come from)
SPEC = {
    'p1': (lambda F: num(at(F, 2)), ['(x - 2)']),
    'p2': (lambda F: num(at(F, -1)), ['(x + 1)']),
    'p3': (lambda F: num(at(F, 1)), ['(x - 1)']),
    'p4': (fact, ['(x + 2)']),
    'p5': (lambda F: num(solve1(F, [at(F, 1) - 5], [a])[a]), ['(x - 1)', 'remainder is 5']),
    'p6': (fact, []), 'p7': (fact, ['(x + 3)']),
    'p8': (lambda F: num(solve1(F, [at(F, 2) - 12], [b])[b]), ['(x - 2)', 'remainder is 12']),
    'p9': (fact, []), 'p10': (fact, []), 'p11': (fact, []), 'p12': (fact, []),
    'p13': (lambda F: num(at(F.subs(solve1(F, [at(F, 2) - 14], [c])), -1)), ['f(2) = 14', '(x + 1)']),
    'p14': (roots, []), 'p15': (fact, []),
    'p16': (lambda F: ('params', solve1(F, [at(F, 1), at(F, -2)], [a, b])), ['(x - 1)', '(x + 2)']),
    'p17': (fact, []), 'p18': (fact, []), 'p19': (fact, []), 'p20': (fact, ['(x + 2)']),
    'p21': (fact, []), 'p22': (fact, []), 'p23': (roots, []), 'p24': (fact, []), 'p25': (fact, []),
    'p26': (fact, []), 'p27': (fact, []), 'p28': (fact, []), 'p29': (roots, []),
    'p30': (lambda F: ('params', solve1(F, [at(F, 2), at(F, -1) + 18], [a, b])), ['f(2) = 0', 'f(−1) = −18']),
    'p31': (fact, []), 'p32': (fact, []), 'p33': (None, []), 'p34': (roots, []), 'p35': (fact, []), 'p36': (fact, []),
    'p37': (lambda F: ('params+fact', solve1(F, [at(F, 1), at(F, -3)], [p, q]),
                       sp.expand(F.subs(solve1(F, [at(F, 1), at(F, -3)], [p, q])))), ['f(1) = 0', 'f(-3) = 0']),
    'p38': (fact, []), 'p39': (fact, []),
    'p40': (lambda F: ('params', solve1(F, [at(F, 1), at(F, -2), at(F, 5)], [a, b, c])), ['1, −2, and 5']),
    'T1.0': (lambda F: num(at(F, -1)), ['(x + 1)']), 'T1.1': (fact, []), 'T1.2': (roots, []),
    'T2.0': (lambda F: num(solve1(F, [at(F, 1)], [a])[a]), ['(x − 1) is a factor']),
    'T2.1': (lambda F: num(at(F.subs(solve1(F, [at(F, 1)], [a])), -2)), ['(x − 1) is a factor', '(x + 2)']),
    'T3.0': (lambda F: num(at(F, 1)), ['f(1)']), 'T3.1': (lambda F: num(at(F, sp.Rational(-1, 2))), ['(2x + 1)']),
    'T3.2': (fact, []), 'T3.3': (roots, []),
    'T4.0': (lambda F: ('params', solve1(F, [at(F, 3), at(F, 1) - 12], [a, b])),
             ['(x − 3)', 'remainder 12', '(x − 1)']),
    'T4.1': (lambda F: fact(F, solve1(F, [at(F, 3), at(F, 1) - 12], [a, b])),
             ['(x − 3)', 'remainder 12', '(x − 1)']),
    'T5.0': (roots, []),
    'T6.0': (lambda F: num(at(F, 3)), ['(x − 3)']), 'T6.1': (fact, []),
    'T7.0': (lambda F: num(at(F, 3)), ['(x − 3)']), 'T7.1': (fact, []), 'T7.2': (roots, []),
    'T8.0': (lambda F: num(solve1(F, [at(F, -2)], [k])[k]), ['(x + 2) is a factor']),
    'T8.1': (lambda F: fact(F, solve1(F, [at(F, -2)], [k])), ['(x + 2) is a factor']),
    'T8.2': (lambda F: roots(F, solve1(F, [at(F, -2)], [k])), ['(x + 2) is a factor']),
    'T9.0': (lambda F: num(at(F, 2)), ['s(2)']), 'T9.1': (roots, []), 'T9.2': (None, []),
    'T10.0': (lambda F: num(at(F, 2)), ['(x − 2)']), 'T10.1': (fact, []), 'T10.2': (roots, []),
    'T10.3': (lambda F: num(at(F, -1)), ['(x + 1)']),
}
# The test's parts carry the conditions for the later parts (T2(b) uses a from (a)): NEEDS are looked for in the
# question's prompt and all its labels.


# Scaffold steps: (item, step) -> (template or None, target). None: the line after its last '=' (or ':').
# A target is a function of the item's polynomial F (and its variable). 'word' steps are pinned.
def _p(F):
    return var_of(F)


STEPS = {
    (1, 0): ('B0', lambda F: 2), (1, 1): (None, lambda F: at(F, 2)), (1, 2): (None, lambda F: at(F, 2)),
    (1, 3): (None, lambda F: at(F, 2)),
    (2, 0): ('B0', lambda F: -1), (2, 1): (None, lambda F: at(F, -1)), (2, 2): (None, lambda F: at(F, -1)),
    (2, 3): (None, lambda F: at(F, -1)), (2, 4): (None, lambda F: at(F, -1)),
    (3, 0): ('B0', lambda F: 1), (3, 1): (None, lambda F: at(F, 1)), (3, 2): (None, lambda F: at(F, 1)),
    (3, 3): (None, lambda F: at(F, 1)),
    (4, 0): ('B0', lambda F: -2), (4, 1): (None, lambda F: at(F, -2)), (4, 2): (None, lambda F: at(F, -2)),
    (4, 3): (None, lambda F: at(F, -2)), (4, 4): ('word', 'factor'),
    (4, 5): (None, lambda F: _p(F) ** 3 / _p(F)),
    (4, 6): (None, lambda F: sp.expand(_p(F) ** 2 * (_p(F) + 2))),
    (4, 7): (None, lambda F: sp.expand((_p(F) ** 3 + _p(F) ** 2) - (_p(F) ** 3 + 2 * _p(F) ** 2))),
    (4, 8): (None, lambda F: -_p(F) ** 2 / _p(F)),
    (4, 9): ('-x**2 + B0', lambda F: sp.expand(-_p(F) * (_p(F) + 2))),
    (4, 10): (None, lambda F: sp.expand((-_p(F) ** 2 - 4 * _p(F)) - (-_p(F) ** 2 - 2 * _p(F)))),
    (4, 11): (None, lambda F: -2 * _p(F) / _p(F)), (4, 12): (None, lambda F: quo(F, -2)),
    (5, 0): ('B0', lambda F: 1), (5, 1): (None, lambda F: at(F, 1)), (5, 2): (None, lambda F: 5),
    (5, 3): (None, lambda F: solve1(F, [at(F, 1) - 5], [a])[a]),
    (6, 0): (None, lambda F: at(F, 1)), (6, 1): ('x - B0', lambda F: _p(F) - 1), (6, 2): (None, lambda F: _p(F) ** 2),
    (6, 3): (None, lambda F: quo(F, 1)), (6, 4): (None, lambda F: quo(F, 1)),
    (7, 0): (None, lambda F: at(F, -3)), (7, 1): (None, lambda F: 2 * _p(F) ** 2), (7, 2): (None, lambda F: quo(F, -3)),
    (7, 3): (None, lambda F: quo(F, -3)),
    (8, 0): (None, lambda F: 12), (8, 1): (None, lambda F: 2 * solve1(F, [at(F, 2) - 12], [b])[b]),
    (8, 2): (None, lambda F: solve1(F, [at(F, 2) - 12], [b])[b]),
    (9, 0): (None, lambda F: at(F, -2)), (9, 1): ('x + B0', lambda F: _p(F) + 2), (9, 2): (None, lambda F: quo(F, -2)),
    (9, 3): (None, lambda F: quo(F, -2)),
    (10, 0): (None, lambda F: at(F, 1)), (10, 1): (None, lambda F: at(F, 2)), (10, 2): (None, lambda F: at(F, 3)),
    (10, 3): (None, lambda F: F),
    (11, 0): (None, lambda F: at(F, 1)), (11, 1): ('x**2 + B0*x + B1', lambda F: quo(F, 1)), (11, 2): (None, lambda F: quo(F, 1)),
    (12, 0): (None, lambda F: at(F, 2)), (12, 1): (None, lambda F: quo(F, 2)), (12, 2): (None, lambda F: quo(F, 2)),
    (13, 0): ('B0', lambda F: solve1(F, [at(F, 2) - 14], [c])[c]),
    (13, 1): ('B0', lambda F: at(F.subs(solve1(F, [at(F, 2) - 14], [c])), -1)),
    (14, 0): (None, lambda F: at(F, 1)), (14, 1): (None, lambda F: quo(F, 1)), (14, 2): (None, lambda F: quo(F, 1)),
    (15, 0): (None, lambda F: at(F, 3)), (15, 1): (None, lambda F: quo(F, 3)), (15, 2): (None, lambda F: quo(F, 3)),
    (16, 0): ('B0', lambda F: (a + b).subs(solve1(F, [at(F, 1), at(F, -2)], [a, b]))),
    (16, 1): ('B0', lambda F: (4 * a - 2 * b).subs(solve1(F, [at(F, 1), at(F, -2)], [a, b]))),
    (16, 2): ('values', lambda F: [solve1(F, [at(F, 1), at(F, -2)], [a, b])[v] for v in (a, b)]),
    (17, 0): (None, lambda F: at(F, 1)), (17, 1): (None, lambda F: quo(F, 1)), (17, 2): (None, lambda F: quo(F, 1)),
    (18, 0): (None, lambda F: at(F, -1)), (18, 1): (None, lambda F: quo(F, -1)), (18, 2): (None, lambda F: quo(F, -1)),
    (19, 0): (None, lambda F: at(F, 1)), (19, 1): (None, lambda F: quo(F, 1)), (19, 2): (None, lambda F: quo(F, 1)),
    (20, 0): (None, lambda F: at(F, -2)), (20, 1): (None, lambda F: quo(F, -2)), (20, 2): (None, lambda F: quo(F, -2)),
}


NUMERIC = '[0-9\\s+\\-−()²³]+'   # arithmetic only: digits, signs, brackets, powers


def rhs(label):
    seg = label.split('=')[-1]
    return seg.split(':')[-1]


def try_parse(text):
    try:
        return parse(text)
    except Exception:
        return None


def solve_blanks(template, target, nblank, v):
    """Every assignment of the blanks that makes template == target (finitely many, else None)."""
    Bs = [sp.Symbol('B%d' % i) for i in range(nblank)]
    diff = sp.expand(template - target)
    eqs = sp.Poly(diff, v).coeffs() if diff.has(v) else [diff]
    sols = sp.solve(eqs, Bs, dict=True)
    out = set()
    for sol in sols:
        if any(B not in sol for B in Bs) or any(sol[B].free_symbols - {v} for B in Bs):
            return None
        out.add(tuple(sp.simplify(sol[B]) for B in Bs))
    return out


def blank_text(val, key_part):
    """The accepted entry for one blank: a number as the page writes it; an expression as its key, canonical."""
    val = sp.sympify(val)
    return rq(val) if val.is_Rational else canon(key_part)


# ── reading an answer back: what a typed form means ──
FACTOR = re.compile(r'\(([^()]+)\)(?:\^(\d))?')


def read_fact(r):
    if not r or FACTOR.sub('', r):
        return None
    out = Counter()
    for m in FACTOR.finditer(r):
        e = sp.expand(parse(m.group(1)))
        out[e] += int(m.group(2) or 1)
    return out


def read_num(r):
    try:
        return sp.Rational(Fraction(r)) if re.fullmatch(r'-?\d+(\.\d+)?(/\d+)?', r) else None
    except (ValueError, ZeroDivisionError):
        return None


def meaning(r, v):
    """('num', q) / ('fact', product) / ('roots', set) / ('params', dict) / ('params+fact', dict, product)."""
    n = read_num(r)
    if n is not None:
        return ('num', n)
    f = read_fact(r)
    if f is not None:
        return ('factors', f)
    items = r.split(',')
    rts, params, fac = [], {}, None
    vname = next((nm for nm, sym in VARS.items() if sym == v), None) if v is not None else None
    for it in items:
        m = re.fullmatch(r'([a-zθωλ])=(.+)', it)
        if m and m.group(1) == vname and read_num(m.group(2)) is not None:
            rts.append(read_num(m.group(2)))
        elif m and m.group(1) in 'abckpq' and read_num(m.group(2)) is not None:
            if m.group(1) in params:
                return None
            params[m.group(1)] = read_num(m.group(2))
        elif read_num(it) is not None:
            rts.append(read_num(it))
        elif read_fact(it) is not None and fac is None:
            fac = read_fact(it)
        else:
            return None
    if rts and not params and fac is None:
        return ('roots', frozenset(rts)) if len(set(rts)) == len(rts) else None
    if params and not rts:
        d = {LOCAL[k_]: v_ for k_, v_ in params.items()}
        return ('params', d) if fac is None else ('params+factors', d, fac)
    return None


def factors_mean(f, product):
    """A factor Counter is the full factorisation of product: linear factors, multiplied out exactly."""
    if any(sp.Poly(e, var_of(product)).degree() != 1 for e in f):
        return False
    return sp.expand(sp.Mul(*[e ** m for e, m in f.items()]) - product) == 0


def agrees(mn, truth):
    if mn is None:
        return False
    if truth[0] == 'fact':
        return mn[0] == 'factors' and factors_mean(mn[1], truth[1])
    if truth[0] == 'params+fact':
        return mn[0] == 'params+factors' and mn[1] == truth[1] and factors_mean(mn[2], truth[2])
    return mn[0] == truth[0] and mn[1] == truth[1]


# ── the forms of an answer that are right, generated from its key ──
def fact_forms(r):
    toks = [(m.group(1), int(m.group(2) or 1)) for m in FACTOR.finditer(r)]
    choices = []
    for inner, m in toks:
        opts = [['(%s)' % inner] * m]
        if m > 1:
            opts.append(['(%s)^%d' % (inner, m)])
        choices.append(opts)
    out = set()
    for pick in itertools.product(*choices):
        for perm in set(itertools.permutations([tk for grp in pick for tk in grp])):
            out.add(''.join(perm))
    return out


def num_forms(val):
    val = sp.Rational(val)
    out = {rq(val)}
    den = val.q
    while den % 2 == 0:
        den //= 2
    while den % 5 == 0:
        den //= 5
    if den == 1 and val.q != 1:
        out.add(str(Fraction(val.p, val.q).numerator / Fraction(val.p, val.q).denominator).rstrip('0'))
    return out


def list_forms(r, vname):
    items = r.split(',')
    out = set()
    rootlike = [re.fullmatch(r'%s=(.+)' % re.escape(vname), it) if vname else None for it in items]
    if items and all(rootlike):
        vals = [m.group(1) for m in rootlike]
        for perm in itertools.permutations(vals):
            for forms in itertools.product(*[num_forms(read_num(z)) for z in perm]):
                out.add(','.join('%s=%s' % (vname, z) for z in forms))
                out.add(','.join(forms))
                out.add(','.join(['%s=%s' % (vname, forms[0])] + list(forms[1:])))
        return out
    parts = []
    for it in items:
        if read_fact(it) is not None:
            parts.append(sorted(fact_forms(it)))
        else:
            parts.append([it])
    for perm in itertools.permutations(range(len(items))):
        for pick in itertools.product(*[parts[i] for i in perm]):
            out.add(','.join(pick))
    return out


def forms(key, v):
    r = canon(key)
    if read_num(r) is not None:
        return {rq(read_num(r))}
    if read_fact(r) is not None:
        return fact_forms(r)
    vname = next((nm for nm, sym in VARS.items() if sym == v), None)
    return list_forms(r, vname)


# ── the checks ──
def units(content):
    """Every marked answer: (uid, item, text the conditions come from, key, polynomial)."""
    out = []
    for it in content['practice']['questions']:
        uid = 'p%d' % it['id']
        F = None if it['id'] == 33 else cubic(it['prompt'])
        out.append((uid, it, it['prompt'], it['finalAnswer'], F))
    for it in content['test']['questions']:
        F = cubic(it['prompt'])
        text = it['prompt'] + ' ' + ' '.join(pt['label'] for pt in it['parts'])
        for i, pt in enumerate(it['parts']):
            out.append(('%s.%d' % (it['id'], i), pt, text, pt['answer'], F))
    return out


ASK_ROOTS = re.compile(r'\b(solve|state all roots|find all values)\b', re.I)
ASK_FACT = re.compile(r'factoris', re.I)


def check(fails, content):
    """Every key, scaffold step and hint; returns the ACCEPTED lists computed from the keys."""
    accepted = {}
    for uid, it, text, key, F in units(content):
        spec, needs = SPEC[uid]
        for n in needs:
            if n not in text:
                fails.append('%s: its condition %r is not in the question as written' % (tag(uid), n))
        if spec is None:
            # an answer-button item (Jon, FT-FIX): marked by dataset.val, never as typed text; check_options
            if not it.get('options'):
                fails.append('%s: %r is typed and marked as a string; it must be four answer buttons' % (tag(uid), key))
            continue
        bad = prose(key)
        if bad:
            fails.append('%s: the key %r is prose (%s), which typed marking cannot mark' % (tag(uid), key, ', '.join(bad)))
            continue
        try:
            truth = spec(F)
        except (AssertionError, ValueError, IndexError) as e:
            fails.append('%s: its stated conditions do not fix one answer (%s)' % (tag(uid), e))
            continue
        v = var_of(F)
        if not agrees(meaning(canon(key), v), truth):
            fails.append('%s: keyed %r; its data gives %s' % (tag(uid), key, show(truth)))
            continue
        fs = forms(key, v)
        for f_ in sorted(fs):
            if not agrees(meaning(f_, v), truth):
                fails.append('%s: accepted form %r does not mean the key' % (tag(uid), f_))
        if not it.get('scaffoldSteps'):
            accepted[uid] = sorted(fs)
        # the ask matches the key (typed answers: practice without a scaffold, test parts)
        ask = it.get('label') or (it['prompt'] if not it.get('scaffoldSteps') else '')
        if ask:
            if ASK_FACT.search(ask) and truth[0] not in ('fact', 'params+fact'):
                fails.append('%s: asks to factorise; keyed %r' % (tag(uid), key))
            if ASK_ROOTS.search(ask) and truth[0] != 'roots' and not ASK_FACT.search(ask) and uid[0] == 'p':
                fails.append('%s: asks for the roots; keyed %r' % (tag(uid), key))
            if ASK_ROOTS.search(ask) and ASK_FACT.search(ask) and truth[0] != 'roots':
                fails.append('%s: asks to factorise and to solve; keyed only %r' % (tag(uid), key))
        if uid == 'p20' and re.search(r'\bk\b', it['prompt']) and not F.has(k):
            fails.append('p20 (factor-theorem-t5-010): asks for k; its polynomial has no k')
    for it in content['practice']['questions']:
        if it['id'] == 33:
            continue
        F = cubic(it['prompt'])
        v = var_of(F)
        check_hints(fails, it, F, v)
        for i, st in enumerate(it.get('scaffoldSteps') or []):
            uid = 'p%d.%d' % (it['id'], i)
            if (it['id'], i) not in STEPS:
                fails.append('%s: a scaffold step with no STEPS entry (add its target)' % uid)
                continue
            tmpl, target = STEPS[(it['id'], i)]
            label = st['label']
            nblank = label.count('___')
            if st.get('display'):
                val = try_parse(rhs(label))
                if val is None or sp.expand(val - target(F)) != 0:
                    fails.append('%s: the shown line %r is not %s' % (uid, label, target(F)))
                continue
            parts = [z.strip() for z in st['answer'].split(',')]
            bad = prose(st['answer'])
            if bad:
                fails.append('%s: the key %r is prose (%s)' % (uid, st['answer'], ', '.join(bad)))
            if nblank != len(parts):
                fails.append('%s: %d blanks but %d answers' % (uid, nblank, len(parts)))
                continue
            if tmpl == 'word':
                if st['answer'] != target:
                    fails.append('%s: keyed %r, pinned %r' % (uid, st['answer'], target))
                accepted[uid] = [canon(target)]
                continue
            if tmpl == 'values':
                sols = {tuple(sp.Rational(z) for z in target(F))}
            else:
                tv = target(F)
                tm = parse(tmpl) if tmpl else try_parse(rhs(label))
                if tm is None:
                    fails.append('%s: the line %r does not read as maths' % (uid, label))
                    continue
                keyx = [parse(z) for z in parts]
                if any(e.has(v) for e in keyx):
                    # an expression in the blank (x^2, -2x): the key put in must make the line true
                    sub = {sp.Symbol('B%d' % i): e for i, e in enumerate(keyx)}
                    sols = {tuple(keyx)} if sp.expand(tm.subs(sub) - tv) == 0 else set()
                else:
                    sols = solve_blanks(tm, tv, nblank, v)
                if not sols:
                    fails.append('%s: no value of the blank%s makes %r true' % (uid, 's' * (nblank > 1), label))
                    continue
                # every other '=' that reads as maths equals the target too
                # a line with a second statement ('..., so 2b = ___') is checked by its blank only
                segs = label.split('=')[:-1] if ',' not in label else []
                for sg in segs[1:]:
                    sg = sg.split(':')[-1].split(',')[0]
                    numeric = re.fullmatch(NUMERIC, sg) and re.search(r'\d', sg)
                    val = try_parse(sg) if numeric else None
                    if val is not None and sp.sympify(tv).is_number and sp.expand(val - tv) != 0:
                        fails.append('%s: %r is %s, not %s' % (uid, sg.strip(), val, tv))
            keyt = tuple(sp.sympify(parse(z)) for z in parts)
            if not any(all(sp.expand(kv - sv) == 0 for kv, sv in zip(keyt, sol)) for sol in sols):
                fails.append('%s: keyed %r; the line gives %s%s' % (
                    uid, st['answer'], ' or '.join(', '.join(str(z) for z in sol) for sol in sols),
                    ' (factor-theorem-t5-001)' if nblank > 1 else ''))
                continue
            if nblank == 1 and len(sols) != 1:
                fails.append('%s: the line %r has more than one answer' % (uid, label))
            accepted[uid] = sorted('|'.join(blank_text(val, kp) for val, kp in zip(sol, parts)) for sol in sols)
    check_learn(fails, content)
    check_options(fails, content)
    return accepted


# A typed key is maths: its words are only variable and function names (one letter), the Greek letters by name, and
# this vocabulary. Any other word is prose, which a typed box cannot mark (t5-004, t5-005).
VOCAB = {'omega', 'theta', 'lambda', 'lam', 'factor'}


def prose(key):
    return [w for w in re.findall(r'[A-Za-z]+', str(key)) if len(w) > 1 and w.lower() not in VOCAB]


# ── the answer-button items, as Jon's FT-FIX contract states them (8 Oct 2026) ──
Q33_OPTIONS = [
    '\\(f(2) = 2^n - 2^n = 0\\), so by the factor theorem \\((x - 2)\\) is a factor.',
    '\\(f(-2) = (-2)^n - 2^n = 0\\), so \\((x - 2)\\) is a factor.',
    '\\(f(2) = 0\\), so \\((x + 2)\\) is a factor.',
    '\\(f(0) = -2^n\\), so \\((x - 2)\\) is a factor.']
T9C_OPTIONS = [
    'The object is at the origin (displacement zero) at t = 2, 3 and 4, passing through it each time.',
    'The object is at rest at t = 2, 3 and 4.',
    'The object changes direction at t = 2, 3 and 4.',
    "The object's acceleration is zero at t = 2 and 4."]
nn = sp.Symbol('n', positive=True, integer=True)
PROOF = re.compile(r'^f\((-?\d+)\) = (.+), so (?:by the factor theorem )?\(x ([+-]) (\d+)\) is a factor\.$')


def proof_holds(option, poly):
    """A Q33 line proves (x - 2) | poly for every positive integer n: each '=' in its working holds for every n, the
    value is 0, and the factor it names is (x - a) for the a it evaluated at. (holds, why not)."""
    m = PROOF.match(option.replace('\\(', '').replace('\\)', ''))
    if not m:
        return None, 'cannot read it'
    pt = int(m.group(1))
    val = poly.subs(x, pt)
    for side in m.group(2).split('='):
        e = sp.sympify(side.strip().replace('^', '**'), locals={'n': nn})
        if sp.simplify(e - val) != 0:
            return False, '%s is not f(%d) = %s for every n' % (side.strip(), pt, val)
    if sp.simplify(val) != 0:
        return False, 'f(%d) = %s is not 0' % (pt, val)
    root = int(m.group(4)) * (1 if m.group(3) == '-' else -1)
    if root != pt:
        return False, 'f(%d) = 0 makes (x - %d) a factor, not the one named' % (pt, pt)
    return True, ''


def motion_claim(option, S, tv):
    """A T9(c) line about s(t): (true overall, [named t where it is true])."""
    ts = [int(z) for z in re.findall(r'\d+', option.split(' at t = ', 1)[1])] if ' at t = ' in option else []
    V, A = sp.diff(S, tv), sp.diff(S, tv, 2)
    if option.startswith('The object is at the origin (displacement zero)'):
        each = [S.subs(tv, z) == 0 and V.subs(tv, z) != 0 for z in ts]       # a single root: s changes sign
    elif option.startswith('The object is at rest'):
        each = [V.subs(tv, z) == 0 for z in ts]
    elif option.startswith('The object changes direction'):
        each = [V.subs(tv, z) == 0 and V.subs(tv, z - sp.Rational(1, 100)) * V.subs(tv, z + sp.Rational(1, 100)) < 0
                for z in ts]
    elif option.startswith("The object's acceleration is zero"):
        each = [A.subs(tv, z) == 0 for z in ts]
    else:
        return None, []
    return bool(ts) and all(each), [z for z, ok in zip(ts, each) if ok]


def check_options(fails, content):
    q33 = next(q for q in content['practice']['questions'] if q['id'] == 33)
    t9 = next(q for q in content['test']['questions'] if q['id'] == 'T9')
    for uid, it, stated, key in (('p33', q33, Q33_OPTIONS, q33.get('finalAnswer')),
                                 ('T9.2', t9['parts'][2], T9C_OPTIONS, t9['parts'][2].get('answer'))):
        opts = it.get('options')
        if not opts:
            continue        # reported in check(): typed and marked as a string
        if opts != stated:
            fails.append('%s: its options are not the four the contract states: %r' % (tag(uid), opts))
        if key not in opts:
            fails.append('%s: the key %r is not one of its options' % (tag(uid), key))
        if not it.get('explain'):
            fails.append('%s: no explanation shown after marking' % tag(uid))
    if q33.get('options'):
        if 'Which line proves it?' not in q33['prompt']:
            fails.append('p33 (factor-theorem-t5-004): the prompt does not ask "Which line proves it?"')
        poly = x ** nn - 2 ** nn
        for o in q33['options']:
            ok, why = proof_holds(o, poly)
            if ok is None:
                fails.append('p33: the option %r: %s' % (o, why))
            elif ok != (o == q33['finalAnswer']):
                fails.append('p33 (factor-theorem-t5-004): the option %r %s' % (
                    o, 'proves it but is not the key' if ok else 'is keyed, but %s' % why))
        ex = q33.get('explain', '')
        if '\\(a = 2\\)' not in ex or '\\(2^n - 2^n = 0\\)' not in ex:
            fails.append('p33: the explanation does not name a = 2 and 2^n - 2^n = 0')
    pc = t9['parts'][2]
    if pc.get('options'):
        S = cubic(t9['prompt'])
        for o in pc['options']:
            ok, true_at = motion_claim(o, S, t)
            if ok is None:
                fails.append('T9.2: the option %r: cannot check it' % o)
            elif o == pc['answer'] and not ok:
                fails.append('T9.2 (factor-theorem-t5-005): the key %r is not true of s(t) = %s' % (o, S))
            elif o != pc['answer'] and true_at:
                fails.append('T9.2 (factor-theorem-t5-005): the option %r is true at t = %s' % (
                    o, ', '.join(map(str, true_at))))
        V = sp.diff(S, t)
        ex = pc.get('explain', '')
        m = re.search(r'\\\(v = ([^\\]*?)\\\) is not zero', ex)
        if not m or sp.expand(parse(m.group(1)) - V) != 0:
            fails.append('T9.2: the explanation\'s v is not ds/dt = %s' % V)
        m = re.search(r'at \\\(t = (-?\d+)\\\), \\\(v = (-?\d+)\\\)', ex)
        if not m or V.subs(t, int(m.group(1))) != int(m.group(2)):
            fails.append('T9.2: the explanation\'s worked v value is wrong (v = %s)' % V)


def show(truth):
    if truth[0] == 'fact':
        return 'f = %s' % sp.factor(truth[1])
    if truth[0] == 'params+fact':
        return '%s, %s' % (truth[1], sp.factor(truth[2]))
    return str(truth[1])


TRY = re.compile(r'[Tt]ry (?:fractions too: )?([xsωθ]) = ([−\-]?[\d½/]+)\s*$')
QUOT = re.compile(r'(?:[Qq]uotient is|you get|to get) ([^,]+?)\s*$')


def check_hints(fails, it, F, v):
    prev = None
    for h in it['hints']:
        m = re.match(r'[a-zA-Zωθ]\(([^)]*)\) = (.*)$', h)
        if m:
            r = try_parse(m.group(1))
            for sg in m.group(2).split(',')[0].split('='):
                if r is not None and r.is_number and at(F, r).is_number and re.fullmatch(NUMERIC, sg):
                    if sp.expand(parse(sg) - at(F, r)) != 0:
                        fails.append('p%d: the hint %r: %s is not f(%s) = %s' % (it['id'], h, sg.strip(), r, at(F, r)))
        m = TRY.search(h)
        if m:
            r = parse(m.group(2).replace('−', '-'))
            if at(F, r) != 0:
                fails.append('p%d: the hint %r names %s, but f(%s) = %s%s' % (
                    it['id'], h, r, r, at(F, r), ' (factor-theorem-t5-011)' if it['id'] == 22 else ''))
        m = QUOT.search(h)
        if m:
            Q = try_parse(m.group(1).replace('to get', ''))
            if Q is not None:
                qq, rr = sp.div(F, Q, v)
                if rr != 0 or sp.Poly(qq, v).degree() != 1:
                    fails.append('p%d: the hint %r: %s does not divide f to a linear factor' % (it['id'], h, Q))
                prev = Q
        m = re.search(r'=\s*(\([^=]*\)[^=]*)$', h)
        if m and read_fact(canon(m.group(1).split('—')[0])) is not None:
            f = read_fact(canon(m.group(1).split('—')[0]))
            lhs = h.split('=')[0]
            L = try_parse(re.sub(r'^.*?(?:\bis\b|\bget\b|:)\s*', '', lhs)) if re.search(r'\^|²', lhs) else prev
            if L is not None and sp.expand(sp.Mul(*[e ** n for e, n in f.items()]) - L) != 0:
                fails.append('p%d: the hint %r does not multiply out to %s' % (it['id'], h, L))


def check_learn(fails, content):
    ex = content['learn']['examples'][3]
    first = ex['steps'][0]
    F = cubic(first['working'])
    lead, const = sp.Poly(F, x).LC(), sp.Poly(F, x).TC()
    want = {sp.Rational(sg * pp, qq) for pp in sp.divisors(abs(const)) for qq in sp.divisors(abs(lead)) for sg in (1, -1)}
    m = re.search(r'which is (.*)\.$', first['explain'])
    got = set()
    if m:
        for tok in m.group(1).split(','):
            z = tok.strip().replace('±', '').replace('½', '1/2').replace('⅓', '1/3')
            got |= {sp.Rational(z), -sp.Rational(z)}
    if got != want:
        fails.append("Learn example 4: the values to try are %s (factor-theorem-t5-012)" % sorted(want))


# ── Chromium ──
SWEEP_JS = r"""(cases) => {
  const out = [];
  // what a student reads in the question card: KaTeX's hidden MathML removed
  const seen = (area) => { const c = area.cloneNode(true); c.querySelectorAll('.katex-mathml, input').forEach(e => e.remove()); return c.textContent; };
  const show = (sec) => {
    document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
    document.getElementById('sec-' + sec).classList.add('active');
  };
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;   // each case renders and clicks at once; LOCK_JS keeps the real window
  for (const cs of cases) {
    show(cs.mode);
    if (cs.mode === 'practice') {
      practiceState = { qIdx: cs.q, score: 0, maxScore: 0, hintsTotal: 0, answers: [], started: true };
      renderPractice();
      const area = document.getElementById('practice-area');
      for (const [sel, val] of cs.fill) {
        const els = [...area.querySelectorAll(sel)];
        if (!els.length) { out.push([cs.tag, 'no box ' + sel]); continue; }
        if (els.length === val.length) els.forEach((e, i) => { e.value = val[i]; });
        else els[0].value = val.join(', ');
      }
      document.getElementById('checkBtn').click();
      const marks = cs.read.map(sel => [...area.querySelectorAll(sel)].map(e => e.classList.contains('correct-input') ? 'right' : e.classList.contains('wrong-input') ? 'wrong' : 'none'));
      out.push([cs.tag, marks, document.getElementById('feedback').textContent, document.documentElement.scrollWidth, document.getElementById('hintBtn').disabled, seen(area)]);
    } else {
      testState = { qIdx: cs.q, score: 0, maxScore: 0, startTime: Date.now(), answers: [], started: true };
      renderTest();
      const area = document.getElementById('test-area');
      cs.fill.forEach(([sel, val]) => { area.querySelector(sel).value = val[0]; });
      (cs.pick || []).forEach(([sel, val]) => { const b = [...area.querySelectorAll(sel + ' .opt-btn')].find(e => e.dataset.val === val); if (b) b.click(); });
      document.getElementById('tCheckBtn').click();
      const marks = cs.read.map(sel => [...area.querySelectorAll(sel)].map(e => e.classList.contains('correct-input') ? 'right' : e.classList.contains('wrong-input') ? 'wrong' : 'none'));
      out.push([cs.tag, marks, document.getElementById('t-feedback').textContent, document.documentElement.scrollWidth, false, seen(area)]);
    }
  }
  return out;
}"""

LEARN_JS = r"""() => {
  const out = [];
  document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
  document.getElementById('sec-learn').classList.add('active');
  CONTENT.learn.examples.forEach((ex, i) => {
    learnState.exampleIdx = i; learnState.stepIdx = ex.steps.length - 1; renderLearn();
    out.push([i, document.documentElement.scrollWidth]);
  });
  return out;
}"""

ENTER_JS = r"""() => {
  document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
  document.getElementById('sec-practice').classList.add('active');
  const qi = CONTENT.practice.questions.findIndex(q => q.id === 21);
  practiceState = { qIdx: qi, score: 0, maxScore: 0, hintsTotal: 0, answers: [], started: true };
  renderPractice();
  const box = document.getElementById('final-answer');
  box.value = CONTENT.practice.questions[qi].finalAnswer;
  box.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
  return document.getElementById('feedback').textContent;
}"""

# Answer once (canon 7.6.0, MaffsLock), with the real 300 ms window: Check clicked twice and Enter mark once; Next
# clicked twice moves one question; a test question submitted twice scores once; each end screen submits once.
LOCK_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const settle = () => wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 50);
  const show = (sec) => {
    document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
    document.getElementById('sec-' + sec).classList.add('active');
  };
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const res = {};
  show('practice');
  const qs = CONTENT.practice.questions, qi = qs.findIndex(q => q.id === 21);
  practiceState = { qIdx: qi, score: 0, maxScore: 0, hintsTotal: 0, answers: [], started: true };
  renderPractice();
  await settle();
  const box = document.getElementById('final-answer');
  box.value = qs[qi].finalAnswer;
  const check = document.getElementById('checkBtn');
  check.click(); check.click();
  box.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
  res.practice = [practiceState.score, practiceState.maxScore, practiceState.answers.length];
  res.qi = qi;
  return res;
}"""
# part 2, after a real double click on Next (the mouse, at the button: the second click lands on the new question)
LOCK2_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const settle = () => wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 50);
  const show = (sec) => {
    document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
    document.getElementById('sec-' + sec).classList.add('active');
  };
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const res = {};
  const qs = CONTENT.practice.questions;
  show('test');
  testState = { qIdx: 0, score: 0, maxScore: 0, startTime: Date.now(), answers: [], started: true };
  renderTest();
  await settle();
  CONTENT.test.questions[0].parts.forEach((pt, i) => { document.getElementById('tpart-' + i).value = pt.answer; });
  const sub = document.getElementById('tCheckBtn');
  sub.click(); sub.click();
  res.test = [testState.score, testState.maxScore, testState.answers.length, CONTENT.test.questions[0].marks];
  practiceState.qIdx = qs.length; renderPractice(); renderPractice();
  testState.qIdx = CONTENT.test.questions.length; renderTest(); renderTest();
  res.submits = submits;
  return res;
}"""

# The answer-button items (Q33, T9(c)), through the game's own Check and Submit: each option chosen once; the marks
# read from the buttons' classes; the explanation and, on a wrong choice, the shared Next control (canon 7.6). And
# the order: shown twenty times, the options come in more than one order.
OPTIONS_JS = r"""() => {
  const out = { cases: [], orders: {}, empty: null };
  const seen = (el) => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(e => e.remove()); return c.textContent; };
  const show = (sec) => {
    document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
    document.getElementById('sec-' + sec).classList.add('active');
  };
  const vis = e => !!e && e.offsetParent !== null;
  const read = (group, val, area, fb, nextId) => {
    const btn = [...group.querySelectorAll('.opt-btn')].find(e => e.dataset.val === val);
    return { val, mark: btn.classList.contains('opt-right') ? 'right' : btn.classList.contains('opt-wrong') ? 'wrong' : 'none',
             right: [...group.querySelectorAll('.opt-btn.opt-right')].map(e => e.dataset.val),
             off: [...group.querySelectorAll('.opt-btn')].every(e => e.disabled),
             explain: !!area.querySelector('.opt-explain'), fb: document.getElementById(fb).textContent,
             next: vis(document.getElementById(nextId)), maffsNext: vis(area.querySelector('.maffs-next')),
             text: seen(area), sw: document.documentElement.scrollWidth };
  };
  show('practice');
  const qs = CONTENT.practice.questions, qi = qs.findIndex(q => q.options);
  if (qi >= 0) {
    const pa = document.getElementById('practice-area');
    const order = new Set();
    for (let k = 0; k < 20; k++) {
      practiceState = { qIdx: qi, score: 0, maxScore: 0, hintsTotal: 0, answers: [], started: true }; renderPractice();
      order.add([...pa.querySelectorAll('.opt-btn')].map(e => e.dataset.val).join('|'));
    }
    out.orders.p = order.size;
    document.getElementById('checkBtn').click();
    out.empty = [document.getElementById('feedback').textContent, practiceState.answers.length];
    for (const val of qs[qi].options) {
      practiceState = { qIdx: qi, score: 0, maxScore: 0, hintsTotal: 0, answers: [], started: true }; renderPractice();
      const g = pa.querySelector('.opt-group');
      [...g.querySelectorAll('.opt-btn')].find(e => e.dataset.val === val).click();
      document.getElementById('checkBtn').click();
      out.cases.push(Object.assign({ uid: 'p' + qs[qi].id, key: qs[qi].finalAnswer, score: practiceState.score }, read(g, val, pa, 'feedback', 'nextQBtn')));
    }
  }
  show('test');
  const ts = CONTENT.test.questions, ti = ts.findIndex(q => q.parts.some(p => p.options));
  if (ti >= 0) {
    const ta = document.getElementById('test-area'), tq = ts[ti], pi = tq.parts.findIndex(p => p.options);
    const order = new Set();
    for (let k = 0; k < 20; k++) {
      testState = { qIdx: ti, score: 0, maxScore: 0, startTime: Date.now(), answers: [], started: true }; renderTest();
      order.add([...ta.querySelectorAll('.opt-btn')].map(e => e.dataset.val).join('|'));
    }
    out.orders.t = order.size;
    for (const val of tq.parts[pi].options) {
      testState = { qIdx: ti, score: 0, maxScore: 0, startTime: Date.now(), answers: [], started: true }; renderTest();
      tq.parts.forEach((p, i) => { if (!p.options) document.getElementById('tpart-' + i).value = p.answer; });
      const g = document.getElementById('tpart-' + pi);
      [...g.querySelectorAll('.opt-btn')].find(e => e.dataset.val === val).click();
      document.getElementById('tCheckBtn').click();
      out.cases.push(Object.assign({ uid: tq.id + '.' + pi, key: tq.parts[pi].answer, score: testState.score, of: tq.marks }, read(g, val, ta, 't-feedback', 'tNextBtn')));
    }
  }
  return out;
}"""

# A wrong typed answer waits on the shared Next control (canon 7.6; the audit's class 11 note in t5-018).
WRONG_NEXT_JS = r"""() => {
  const vis = e => !!e && e.offsetParent !== null;
  document.querySelectorAll('.section').forEach(e => e.classList.remove('active'));
  document.getElementById('sec-practice').classList.add('active');
  const qi = CONTENT.practice.questions.findIndex(q => q.id === 21);
  practiceState = { qIdx: qi, score: 0, maxScore: 0, hintsTotal: 0, answers: [], started: true };
  renderPractice();
  document.getElementById('final-answer').value = '(x+9)';
  document.getElementById('checkBtn').click();
  return { next: vis(document.getElementById('nextQBtn')), maffsNext: vis(document.querySelector('#practice-area .maffs-next')) };
}"""

# ?level (Jon, 9 Oct 2026, FT-FIX answers): every URL plays A-Level. In a fresh page per URL, events and leaderboard
# submissions recorded: Practice played to its end, then the Test (T1 answered, then its end screen).
HOOKS = """(() => { window.__ev = []; window.__sub = []; let inner;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (e, p) { window.__ev.push([e, p]); return inner && inner.apply(this, arguments); }; },
    set(v) { inner = v; } });
  Object.defineProperty(window, 'MaffsLeaderboard', { configurable: true,
    get() { return { submitScore() { window.__sub.push([...arguments]); return Promise.resolve(); } }; }, set(v) {} });
})();"""
LEVEL_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const settle = () => wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 50);
  document.querySelector('[data-section="practice"]').click();
  practiceState.qIdx = CONTENT.practice.questions.length; renderPractice();
  const practiceSubs = window.__sub.length;
  document.querySelector('[data-section="test"]').click();
  await settle();
  CONTENT.test.questions[0].parts.forEach((pt, i) => { document.getElementById('tpart-' + i).value = pt.answer; });
  document.getElementById('tCheckBtn').click();
  testState.qIdx = CONTENT.test.questions.length; renderTest();
  return { ev: window.__ev, sub: window.__sub, practiceSubs, badge: document.querySelector('.topbar-right .badge-lp').textContent };
}"""
LEVEL_URLS = ('', '?level=alevel', '?level=level4', '?level=xyz', '?level=__proto__')

KATEX_DIR = None
STATS = {}


def decorate(form):
    """A form as a student might type it: spaces, a real minus sign, superscripts, a label, upper case."""
    if read_num(form) is not None:
        return [form, ' %s ' % form]
    out = [form, re.sub(r'([+\-=,])', r' \1 ', form)]
    out.append(form.replace('-', '−').replace('^2', '²'))
    if form.startswith('('):
        out.append('f(x) = ' + form.replace(')(', ') × ('))
    out.append(form.upper().replace('Ω', 'OMEGA').replace('Θ', 'THETA').replace('Λ', 'LAMBDA'))
    return [z.replace('ω', 'omega').replace('θ', 'theta').replace('λ', 'lambda') for z in out]


def flip(form):
    """A wrong form: the first sign in a factor or root flipped."""
    if read_fact(form) is not None:
        return re.sub(r'\(([^()]*?)([+-])', lambda m: '(%s%s' % (m.group(1), '+' if m.group(2) == '-' else '-'), form,
                      count=1)
    m = re.search(r'(=|^|,)(-?)(\d)', form)
    if m:
        return form[:m.start(2)] + ('' if m.group(2) else '-') + form[m.start(3):]
    return None


def cases_for(content, accepted):
    cases = []
    tests = content['test']['questions']
    for qi, it in enumerate(content['practice']['questions']):
        uid = 'p%d' % it['id']
        if it.get('options'):
            continue        # answer buttons: OPTIONS_JS
        steps = it.get('scaffoldSteps') or []
        if steps:
            keyed = [('#scaffold-%d input' % i, [z.strip() for z in st['answer'].split(',')])
                     for i, st in enumerate(steps) if not st.get('display')]
            cases.append({'mode': 'practice', 'q': qi, 'tag': (uid, 'key'), 'fill': keyed,
                          'read': [sel for sel, _ in keyed]})
            for j, (sel, val) in enumerate(keyed):
                if len(val) < 2:
                    continue
                sid = '%s.%s' % (uid, re.search(r'-(\d+)', sel).group(1))
                good = {tuple(e.split('|')) for e in accepted.get(sid, [])}
                for perm in set(itertools.permutations(val)):
                    if tuple(perm) in good or list(perm) == val:
                        continue
                    fill = [(s2, list(perm) if s2 == sel else v2) for s2, v2 in keyed]
                    cases.append({'mode': 'practice', 'q': qi, 'tag': (sid, 'wrong order', '(%s)' % ', '.join(perm)),
                                  'fill': fill, 'read': [sel]})
                for perm in good - {tuple(val)}:
                    fill = [(s2, list(perm) if s2 == sel else v2) for s2, v2 in keyed]
                    cases.append({'mode': 'practice', 'q': qi, 'tag': (sid, 'other order', '(%s)' % ', '.join(perm)),
                                  'fill': fill, 'read': [sel]})
        else:
            for form in typed_forms(accepted.get(uid, [canon(it['finalAnswer'])]), it['finalAnswer'], uid):
                cases.append({'mode': 'practice', 'q': qi, 'tag': (uid,) + form[1:], 'fill': [('#final-answer', [form[0]])],
                              'read': ['#final-answer']})
    for qi, it in enumerate(tests):
        per, typed = [], [i for i, pt in enumerate(it['parts']) if not pt.get('options')]
        for i in typed:
            uid = '%s.%d' % (it['id'], i)
            pt = it['parts'][i]
            per.append(typed_forms(accepted.get(uid, [canon(pt['answer'])]), pt['answer'], uid))
        # an answer-button part is answered with its key here; OPTIONS_JS marks each of its options
        chosen = [('#tpart-%d' % i, pt['answer']) for i, pt in enumerate(it['parts']) if pt.get('options')]
        for n in range(max(len(z) for z in per)):
            pick = [z[n % len(z)] for z in per]
            cases.append({'mode': 'test', 'q': qi, 'tag': [('%s.%d' % (it['id'], i),) + pk[1:] for i, pk in zip(typed, pick)],
                          'fill': [('#tpart-%d' % i, [pk[0]]) for i, pk in zip(typed, pick)], 'pick': chosen,
                          'read': ['#tpart-%d' % i for i in typed]})
    return cases


def typed_forms(acc, key, uid):
    """(typed text, 'right'|'wrong', why) for one answer: the key, sampled accepted forms decorated, one flipped."""
    out = [(key, 'right', 'key')]
    step = max(1, len(acc) // 4)
    for f_ in acc[::step][:4]:
        for d in decorate(f_)[1:]:
            out.append((d, 'right', 'form'))
    for f_ in acc[:1]:
        if read_num(f_) == 0:
            continue
        fl = flip(f_)
        if fl and fl not in acc:
            out.append((fl, 'wrong', 'sign flipped'))
    return out


def play(fails, html, accepted, sweep=True):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    content = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof CONTENT !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            page.wait_for_function('document.getElementById("practice-area").innerHTML.length > 0', timeout=15000)
            content = page.evaluate('CONTENT')
            if not sweep:
                ctx.close()
                browser.close()
                return content
            if accepted is None:
                accepted = check([], content)
            if page.evaluate('typeof canon') == 'function':
                probe = sorted({d for fs in accepted.values() for f_ in fs[:3] for d in decorate(f_)})
                got = page.evaluate('(xs) => xs.map(canon)', probe)
                for raw, js in zip(probe, got):
                    if js != canon(raw):
                        fails.append('canon(%r): the page gives %r, this script %r' % (raw, js, canon(raw)))
            cases = cases_for(content, accepted)
            res = page.evaluate(SWEEP_JS, cases)
            STATS['cases'] = len(cases)
            wide = set()
            raw_seen = set()
            for cs, row in zip(cases, res):
                if row[1] and isinstance(row[1], str):
                    fails.append('%s: %s' % (cs['tag'], row[1]))
                    continue
                m = re.search(r'.{0,25}(\^|\\[a-z(]|_\{).{0,25}', row[5])
                if m and (cs['mode'], cs['q']) not in raw_seen:
                    raw_seen.add((cs['mode'], cs['q']))
                    fails.append('%s %d: raw TeX on screen: %r (factor-theorem-t5-019)' % (cs['mode'], cs['q'] + 1, m.group(0)))
                marks, fb, sw, hint_off = row[1], row[2], row[3], row[4]
                if sw > 390:
                    wide.add((cs['mode'], cs['q'], sw))
                if cs['mode'] == 'practice':
                    tg = cs['tag']
                    if tg[1] in ('wrong order', 'other order'):
                        want = 'wrong' if tg[1] == 'wrong order' else 'right'
                    else:
                        want = tg[1]
                    if tg[-1] == 'key' and tg[1] == 'right':
                        if not all(z == 'right' for z in marks[0]):
                            fails.append('%s: the key %r is not marked right (factor-theorem-t5-002)' % (
                                tag(tg[0]), cs['fill'][0][1][0]))
                        elif not hint_off:
                            fails.append('%s: the hint button is live after marking (factor-theorem-t5-018)' % tg[0])
                        continue
                    if tg[1] == 'key':
                        bad = [m for m in marks if any(z != 'right' for z in m)]
                        if bad or not fb.startswith('Correct'):
                            fails.append('%s: the key is not marked right (%s)' % (tag(tg[0]), fb))
                        if not hint_off:
                            fails.append('%s: the hint button is live after marking (factor-theorem-t5-018)' % tg[0])
                        continue
                    got = 'right' if all(z == 'right' for z in marks[0]) else 'wrong'
                    if got != want:
                        if 'order' in tg[1]:
                            fails.append('%s: the %s %s is marked %s (factor-theorem-t5-001)' % (tg[0], tg[1], tg[2], got))
                        else:
                            fails.append('%s: %r (%s) is marked %s (factor-theorem-%s)' % (
                                tag(tg[0]), cs['fill'][0][1][0], tg[2], got, 't5-002' if want == 'right' else 't5-001'))
                else:
                    for (uid, kind, why), mk, (_, val) in zip([tuple(z) for z in cs['tag']], marks, cs['fill']):
                        got = 'right' if mk and mk[0] == 'right' else 'wrong'
                        if got != kind:
                            fails.append('%s: %r (%s) is marked %s (factor-theorem-%s)' % (
                                tag(uid), val[0], why, got, 't5-002' if kind == 'right' else 't5-001'))
            for mode, qi, sw in sorted(wide):
                fails.append('%s %d at 390px: the page scrolls sideways (%dpx; factor-theorem-t5-018)' % (mode, qi + 1, sw))
            if page.evaluate('typeof enterSubmits') == 'function':
                ent = page.evaluate(ENTER_JS)
                if not ent.startswith('Correct'):
                    fails.append('p21: Enter in the answer box does not check it (%r; factor-theorem-t5-018)' % ent)
            lk = page.evaluate(LOCK_JS)
            nxt = page.locator('#nextQBtn')
            nxt.scroll_into_view_if_needed()
            bb = nxt.bounding_box()
            page.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
            page.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
            lk['moved'] = page.evaluate('practiceState.qIdx') - lk['qi']
            lk.update(page.evaluate(LOCK2_JS))
            if lk['practice'] != [3, 3, 1]:
                fails.append('p21: Check clicked twice and Enter: score, out of, answers = %s, not [3, 3, 1] (MaffsLock)' % (
                    lk['practice'],))
            if lk['moved'] != 1:
                fails.append('p21: Next clicked twice moved %d questions (MaffsLock)' % lk['moved'])
            m = lk['test']
            if m[:3] != [m[3], m[3], 1]:
                fails.append('T1: submitted twice: score, out of, answers = %s, not [%d, %d, 1] (MaffsLock)' % (m[:3], m[3], m[3]))
            if lk['submits'] != 1:
                fails.append('the two end screens, each shown twice, submitted %d scores, not 1: the Test once, Practice '
                             'never (MaffsLock; factor-theorem-t5-014)' % lk['submits'])
            for i, sw in page.evaluate(LEARN_JS):
                if sw > 390:
                    fails.append('Learn example %d at 390px: the page scrolls sideways (%dpx; factor-theorem-t5-018)' % (
                        i + 1, sw))
            check_option_play(fails, page.evaluate(OPTIONS_JS))
            wn = page.evaluate(WRONG_NEXT_JS)
            if wn['next'] or not wn['maffsNext']:
                fails.append('wrong answer (p21): advanced by %s, not the shared Next control (canon 7.6; '
                             'factor-theorem-t5-018)' % ('the Next Question button' if wn['next'] else 'nothing'))
            # the narrowest phone: every question and Learn example, the keys typed in
            ctx.set_default_timeout(20000)
            page.set_viewport_size({'width': 320, 'height': 568})
            keyed = [cs for cs in cases if cs['mode'] == 'test' or cs['tag'][-1] == 'key']
            seen = set()
            for cs, row in zip(keyed, page.evaluate(SWEEP_JS, keyed)):
                if not isinstance(row[1], str) and row[3] > 320 and (cs['mode'], cs['q']) not in seen:
                    seen.add((cs['mode'], cs['q']))
                    fails.append('%s %d at 320px: the page scrolls sideways (%dpx)' % (cs['mode'], cs['q'] + 1, row[3]))
            for i, sw in page.evaluate(LEARN_JS):
                if sw > 320:
                    fails.append('Learn example %d at 320px: the page scrolls sideways (%dpx)' % (i + 1, sw))
            ctx.add_init_script(HOOKS)
            for q in LEVEL_URLS:
                pg = ctx.new_page()
                pg.on('pageerror', lambda e: errors.append(str(e)))
                pg.goto(base + '/games/%s/%s' % (SLUG, q), wait_until='load', timeout=20000)
                pg.wait_for_function('typeof katex !== "undefined" && document.getElementById("test-area").innerHTML.length > 0',
                                     timeout=15000)
                check_level(fails, q, pg.evaluate(LEVEL_JS))
                pg.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return content


def check_option_play(fails, res):
    for side, n in sorted(res['orders'].items()):
        if n < 2:
            fails.append('%s: the answer buttons came in one order in 20 showings (not shuffled)' % (
                'p33' if side == 'p' else 'T9.2'))
    if res['empty'] and (res['empty'][1] or 'Choose' not in res['empty'][0]):
        fails.append('p33: Check with no answer chosen: %r, %d marked' % tuple(res['empty']))
    for cs in res['cases']:
        uid, right = cs['uid'], cs['val'] == cs['key']
        want = 'right' if right else 'wrong'
        if cs['mark'] != want:
            fails.append('%s: the option %r is marked %s, not %s' % (tag(uid), cs['val'], cs['mark'], want))
        if cs['right'] != [cs['key']]:
            fails.append('%s: after marking, the buttons shown right are %r, not the key' % (uid, cs['right']))
        if not cs['off']:
            fails.append('%s: the buttons are live after marking' % uid)
        if not cs['explain']:
            fails.append('%s: no explanation after marking' % uid)
        if right and (cs['maffsNext'] or not cs['next']):
            fails.append('%s: a right answer is not followed by the Next Question button' % uid)
        if not right and (cs['next'] or not cs['maffsNext']):
            fails.append('%s: a wrong answer is not followed by the shared Next control (canon 7.6)' % uid)
        if uid[0] == 'p' and cs['score'] != (3 if right else 0):
            fails.append('%s: the option %r scored %d' % (uid, cs['val'], cs['score']))
        if uid[0] == 'T' and cs['score'] != (cs['of'] if right else cs['of'] - 1):
            fails.append('%s: with the other parts right, the option %r scored %d of %d' % (uid, cs['val'], cs['score'], cs['of']))
        m = re.search(r'.{0,25}(\^|\\[a-z(]|_\{).{0,25}', cs['text'])
        if m:
            fails.append('%s: raw TeX on screen: %r' % (uid, m.group(0)))
        if cs['sw'] > 390:
            fails.append('%s at 390px: the page scrolls sideways (%dpx)' % (uid, cs['sw']))


def check_level(fails, q, res):
    given = q.split('=', 1)[1] if '=' in q else None
    where = 'level: %s' % (q or 'no ?level')
    levels = sorted({str(p.get('level')) for e, p in res['ev'] if p and 'level' in p})
    kinds = [e for e, _ in res['ev']]
    if levels != ['alevel']:
        fails.append('%s logged level %s, not only alevel (factor-theorem-t5-013)' % (where, levels))
    for need in ('game_started', 'question_answered', 'game_completed'):
        if need not in kinds:
            fails.append('%s: no %s event (the game did not play)' % (where, need))
    if given and given != 'alevel' and given in json.dumps(res['ev']) + json.dumps(res['sub']):
        fails.append('%s: the value %r was logged or submitted (factor-theorem-t5-013)' % (where, given))
    if res['practiceSubs']:
        fails.append('Practice: finishing it submitted %r to the leaderboard (factor-theorem-t5-014, t5-015)' % (
            res['sub'][:res['practiceSubs']],))
    tests = [z for z in res['sub'][res['practiceSubs']:]]
    if [z[:2] for z in tests] != [['factor-theorem', 'alevel']]:
        fails.append('%s: the Test submitted %r, not once to factor_theorem_alevel (factor-theorem-t5-015)' % (where, tests))
    if res['badge'].strip() != 'A-Level':
        fails.append('%s: the badge says %r' % (where, res['badge']))


def block(accepted):
    lines = ['const ACCEPTED = {']
    for uid in sorted(accepted, key=lambda u: (u[0], [int(z) for z in re.findall(r'\d+', u)])):
        lines.append('  %s: %s,' % (json.dumps(uid), json.dumps(accepted[uid], ensure_ascii=False)))
    lines.append('};')
    return '\n'.join(lines) + '\n'


def page_block(html):
    if START not in html or END not in html:
        return None
    return html[html.index(START) + len(START):html.index(END)]


def verify(html):
    """All checks on one copy of the page: (fails, accepted computed)."""
    fails = []
    content = play(fails, html, None)
    if content is None:
        return fails, None
    accepted = check(fails, content)
    pb = page_block(html)
    if pb is None:
        fails.append('the page has no ACCEPTED block: its typed answers are compared as strings '
                      '(factor-theorem-t5-001, t5-002)')
    elif pb != block(accepted):
        cur = {}
        for m in re.finditer(r'^  "([^"]+)": (\[.*\]),$', pb, re.M):
            cur[m.group(1)] = json.loads(m.group(2))
        for uid in sorted(set(cur) | set(accepted)):
            if cur.get(uid) != accepted.get(uid):
                extra = sorted(set(cur.get(uid, [])) - set(accepted.get(uid, [])))
                fails.append('%s: the page accepts %s, which the key does not give (%s)' % (
                    tag(uid), extra, 'factor-theorem-t5-001' if uid.count('.') and uid[0] == 'p' else 'run --write')
                    if extra else '%s: the page\'s ACCEPTED list differs (run --write)' % tag(uid))
    return fails, accepted


PLANTS = [
    ('p6.4', 't5-001: (x - 2)(x + 3) accepted for Q6', '"p6.4": ["-2|-3", "3|2"]', '"p6.4": ["-2|-3", "2|3", "3|2"]'),
    ('T4', 't5-003: the old T4',
     "has a factor (x \\u2212 3) and leaves remainder 12 when divided by (x \\u2212 1). Find a and b.',marks:3,"
     "answer:'a=-19, b=30',answerLabel:'a, b ='},\n          {label:'(b) Fully factorise p(x).',marks:1,"
     "answer:'(x-3)(x-2)(x+5)'",
     "has a factor (x \\u2212 3) and leaves remainder 20 when divided by (x \\u2212 1). Find a and b.',marks:3,"
     "answer:'a=-23, b=42',answerLabel:'a, b ='},\n          {label:'(b) Fully factorise p(x).',marks:1,"
     "answer:'(x-3)(x+7)(x-2)'"),
    ('p33', "t5-004: Q33's old free-text key",
     r"finalAnswer:'\\(f(2) = 2^n - 2^n = 0\\), so by the factor theorem \\((x - 2)\\) is a factor.'," "\n        options:[",
     "finalAnswer:'f(2) = 2^n - 2^n = 0',\n        _options:["),
    ('T9.2', "t5-005: T9(c)'s old free-text key",
     "answer:'The object is at the origin (displacement zero) at t = 2, 3 and 4, passing through it each time.',"
     "\n            options:[",
     "answer:'object crosses origin at t=2, 3, 4',answerLabel:'Interpretation:',\n            _options:["),
    ('T6.0', 'a typed key that is prose', "answer:'12',answerLabel:'Remainder ='", "answer:'twelve',answerLabel:'Remainder ='"),
    ('Practice', 't5-014: a Practice submit', "mode: 'practice' });\n  }\n});",
     "mode: 'practice' });\n  }\n  if (window.MaffsLeaderboard) MaffsLeaderboard.submitScore(CONTENT.slug, 'alevel', "
     "practiceState.score, questions.length).catch(function(){});\n});"),
    ('level', 't5-013: ?level read and logged', "mfg('game_started', { game_slug: CONTENT.slug, level: 'alevel', mode: mode });",
     "mfg('game_started', { game_slug: CONTENT.slug, level: new URLSearchParams(location.search).get('level') || 'alevel', "
     "mode: mode });"),
    ('wrong answer', 't5-018: a wrong answer advanced by the Next button',
     "    if (correct) {\n      document.getElementById('nextQBtn').style.display = 'block';",
     "    if (true) {\n      document.getElementById('nextQBtn').style.display = 'block';"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='write the ACCEPTED block computed from the keys')
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    if args.write:
        content = play([], html, None, sweep=False)
        fails = []
        accepted = check(fails, content)
        for f_ in fails:
            print('FAIL  ' + f_)
        if fails:
            print('not written: fix the keys first')
            return 1
        new = html[:html.index(START) + len(START)] + block(accepted) + html[html.index(END):]
        open(GAME, 'w', encoding='utf-8', newline='\n').write(new)
        print('wrote ACCEPTED: %d answers, %d forms' % (len(accepted), sum(len(v) for v in accepted.values())))
        return 0
    fails, accepted = verify(html)
    print('%s: every key from its polynomial, ACCEPTED lists computed (%d answers, %d forms), %d markings in Chromium' % (
        SLUG, len(accepted or {}), sum(len(v) for v in (accepted or {}).values()), STATS.get('cases', 0)))
    ok = True
    if not args.no_selftest and not args.against:
        for prefix, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-40s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep, _ = verify(html.replace(old, new))
            hit = [f_ for f_ in rep if f_.startswith(prefix)]
            ok = ok and bool(hit)
            print('  self-test %-40s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f_ in fails:
        print('FAIL  ' + f_)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
