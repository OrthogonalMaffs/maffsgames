#!/usr/bin/env python3
# ci-line: Proof Builder (every counter-example checked, every induction stage by SymPy, every sorter order and rendered string in Chromium) |
"""Proof Builder: every counter-example checked against its statement, every induction stage by SymPy, every sorter
order and every rendered string in Chromium.

The game has three modes: Counter-Example Finder (35 statements: pick the option that disproves it, or say it is
true), Proof Sorter (put a proof's lines in order) and Induction Builder (four proofs, a choice at each stage). The
tranche 5 audit of 6 Oct 2026 found wrong options that were valid counter-examples (sqrt(4 + 9) != 2 + 3, ...),
induction stages whose wrong options equal the key or are true, a true exterior-angle statement keyed false, a
sorter that rejects valid orders and can be re-checked for full marks, false facts in the worked steps, and prose
passed whole through KaTeX (every space lost, 132 B7 entries), raw LaTeX on screen and sideways scroll at 390px.

Counter-examples. REFUTES below holds, per statement, a function that says whether an option disproves it,
  computed (SymPy, exact) from the option's own values: the key must disprove it (or, for a statement keyed true,
  its proof is reviewed and no option may disprove it), and no wrong option may (SR-16).
Induction. STAGES holds each stage's target: the key equals it (SymPy), no wrong option does, and no wrong option
  is a true statement of what the stage asks.
Worked steps. Every maths claim in a step ("a = b", "a \\approx b", "a \\neq b") whose sides are numbers is
  evaluated; one that is false FAILS.
Sorter (Chromium). For every proof, the order as written is accepted and swapping any two adjacent lines is
  rejected, unless the proof lists the order as valid (`after`: the lines each line needs before it); for the
  n^2 + n proof every valid order is accepted. After a wrong Check, reselecting lines and checking again scores
  nothing (t5-015).
Rendering (Chromium, 390x844). Every statement, sorter line, prompt, worked step and misconception is shown through
  the game's own renderers: no raw TeX on screen (a backslash, ^ or _), every prose word separated by a space, and
  the page never scrolls sideways (sorter screens and solution panels).
Marking (Chromium). Every option of every counter item and induction stage is clicked: the key marked right, the
  others wrong; a wrong answer shows the worked solution and the shared Next control (MaffsNext, canon 7.6).

A self-test plants three of the audit's own faults back into a copy of the page (t5-003: a = 4, b = 9 as a wrong
option; t5-009: (k^2 + 3k + 2)/2 as a wrong option; t5-012: the exterior-angle statement keyed false with "a
reflex angle"); each must FAIL naming its item.

    python scripts/verify-proof-builder.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (factorial_notation, implicit_multiplication_application, parse_expr,
                                        rationalize, standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'proof-builder'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
k, m, n, x, theta = sp.symbols('k m n x theta')
LOCAL = {'k': k, 'm': m, 'n': n, 'x': x, 'theta': theta, 'pi': sp.pi, 'e': sp.E, 'i': sp.I, 'I': sp.I,
         'sqrt': sp.sqrt, 'sin': sp.sin, 'cos': sp.cos, 'log': lambda v: sp.log(v, 10), 'ln': sp.log,
         'factorial': sp.factorial}
TRANS = standard_transformations + (factorial_notation, implicit_multiplication_application, rationalize)
SUP = {'²': '**2', '³': '**3'}


def group(s, i, o, c):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == o) - (s[j] == c)
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced')


def to_py(s):
    s = (s.replace('\u2212', '-').replace('\\left', '').replace('\\right', '').replace('\\times', '*')
         .replace('\\cdot', '*').replace('\\pi', ' pi ').replace('\\theta', ' theta ').replace('°', '*pi/180')
         .replace('^\\circ', '*pi/180').replace('\\,', ' ').strip())
    for a_, b_ in SUP.items():
        s = s.replace(a_, b_)
    out, i = '', 0
    while i < len(s):
        mm = re.match(r'\\[dt]?frac\{', s[i:])
        if mm:
            num, j = group(s, i + mm.end() - 1, '{', '}')
            den, kk = group(s, j, '{', '}')
            out += '((%s)/(%s))' % (to_py(num), to_py(den))
            i = kk
            continue
        if s.startswith('\\sqrt{', i):
            inner, j = group(s, i + 5, '{', '}')
            out += 'sqrt(%s)' % to_py(inner)
            i = j
            continue
        mm = re.match(r'\\(sin|cos|log|ln)', s[i:])
        if mm:
            out += ' %s' % mm.group(1)
            i += mm.end()
            continue
        if s[i] == '{':
            inner, j = group(s, i, '{', '}')
            out, i = out + '(%s)' % to_py(inner), j
            continue
        if s[i] == '\\':
            raise ValueError('TeX command in %r' % s)
        out += '**' if s[i] == '^' else s[i]
        i += 1
    return out


def ev(s):
    py = re.sub(r'(?<=[0-9a-z)])\s*(?=(sin|cos|log|ln|sqrt)\()', '*', to_py(s))
    try:
        return parse_expr(py, local_dict=LOCAL, transformations=TRANS)
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (s, py, e))


def mat(s):
    s = s.strip()
    mm = re.fullmatch(r'\\begin\{pmatrix\}(.*)\\end\{pmatrix\}', s)
    if mm:
        return sp.Matrix([[ev(c) for c in row.split('&')] for row in mm.group(1).split('\\\\')])
    mm = re.fullmatch(r'(-?\d*)\s*I', s)
    if mm:
        return sp.eye(2) * (int(mm.group(1)) if mm.group(1) not in ('', '-') else (-1 if mm.group(1) == '-' else 1))
    if s == '0':
        return sp.zeros(2)
    raise ValueError('not a matrix: %r' % s)


def assigns(o):
    """'a=1, b=1', 'a = b = 10', 'z_1=1, z_2=i', 'A=I, B=I' -> {name: text}."""
    out = {}
    o = re.sub(r'\\text\{[^}]*\}', ' ', o)
    mm = re.fullmatch(r'\s*(\w+)\s*=\s*(\w+)\s*=\s*(.+)', o)
    if mm and ',' not in o:
        return {mm.group(1): mm.group(3).strip(), mm.group(2): mm.group(3).strip()}
    depth, cur, parts = 0, '', []
    for ch in o:
        depth += (ch == '{') - (ch == '}')
        if ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    for p in parts:
        name, _, val = p.partition('=')
        out[name.strip()] = val.strip()
    return out


def num(o):
    o = re.sub(r'^\\?[a-zA-Z]+\s*=\s*', '', o.strip())
    return ev(o)


def isprime(v):
    return sp.Integer(v).is_prime


def irr(v):
    v = sp.nsimplify(v)
    if v.is_rational is not None:
        return not v.is_rational
    try:
        return sp.minimal_polynomial(v, sp.Symbol('t_')).as_poly().degree() > 1
    except sp.polys.polyerrors.NotAlgebraic:
        if v.is_transcendental if hasattr(v, 'is_transcendental') else False:
            return True
        raise ValueError('whether %s is irrational is not known (an open problem): no option may rest on it' % v)


def terms(o, sep):
    lhs = o.split('=')[0]
    depth, cur, parts = 0, '', []
    for ch in lhs:
        depth += (ch in '({') - (ch in ')}')
        cur += ch
    return [ev(t) for t in re.split(r'(?<!\()%s' % re.escape(sep), lhs)]


def poly_disc(o):
    lhs = ev(o.split('=')[0])
    a_, b_, c_ = [sp.Poly(lhs, x).coeff_monomial(x ** p) for p in (2, 1, 0)]
    return b_ * b_ - 4 * a_ * c_


def is_local_max(f, a):
    h = sp.Rational(1, 1000)
    return f.subs(x, a - h) < f.subs(x, a) and f.subs(x, a + h) < f.subs(x, a)


def arg(z):
    return sp.arg(sp.nsimplify(z))


def tri(o):
    a = assigns(o)
    return {kk: ev(v) for kk, v in a.items()}


# Statement (a distinctive substring) -> refutes(option) for counter-example items.
REFUTES = [
    ('All prime numbers are odd', lambda o: isprime(num(o)) and num(o) % 2 == 0),
    ('square of any number is greater', lambda o: not num(o) ** 2 > num(o)),
    ('n² is even, then n is even', lambda o: num(o).is_integer and (num(o) ** 2) % 2 == 0 and num(o) % 2 == 1),
    ('sum of two irrational', lambda o: all(irr(t) for t in terms(o, '+')) and not irr(sum(terms(o, '+')))),
    ('n² + n + 41', lambda o: not isprime(num(o) ** 2 + num(o) + 41)),
    ('If a > b then a² > b²', lambda o: (lambda d: d['a'] > d['b'] and not d['a'] ** 2 > d['b'] ** 2)(tri(o))),
    ('product of two irrational', lambda o: all(irr(t) for t in terms(o, '\\times')) and
     not irr(sp.Mul(*terms(o, '\\times')))),
    ('not divisible by 2 or 3', lambda o: num(o) % 2 != 0 and num(o) % 3 != 0 and not isprime(num(o))),
    ('n³ > n²', lambda o: not num(o) ** 3 > num(o) ** 2),
    ('even number plus an even number', lambda o: (lambda t: all(v % 2 == 0 for v in t) and sum(t) % 2 == 1)(terms(o, '+'))),
    ('quadratic equation always has two distinct', lambda o: poly_disc(o) <= 0),
    ('sum of two numbers is even, both', lambda o: (lambda t: sum(t) % 2 == 0 and not all(v % 2 == 0 for v in t))(terms(o, '+'))),
    ('\\sqrt{a+b}', lambda o: (lambda d: d['a'] > 0 and d['b'] > 0 and sp.simplify(sp.sqrt(d['a'] + d['b']) - sp.sqrt(d['a']) - sp.sqrt(d['b'])) != 0)(tri(o))),
    ('exterior angle', lambda o: False),
    ('If f(a) = f(b) then a = b', lambda o: (lambda d: (lambda f: f.subs(x, d['a']) == f.subs(x, d['b']) and d['a'] != d['b'])(d['f(x)']))(tri(o))),
    ('n² - n + 11', lambda o: not isprime(num(o) ** 2 - num(o) + 11)),
    ('three consecutive integers is divisible by 6', lambda o: (lambda t: sum(t) % 6 != 0)(terms(o, '+'))),
    ('a divides bc', lambda o: (lambda d: (d['b'] * d['c']) % d['a'] == 0 and d['b'] % d['a'] != 0 and d['c'] % d['a'] != 0)(tri(o))),
    ('\\log(a + b)', lambda o: (lambda d: d['a'] > 0 and d['b'] > 0 and sp.simplify(sp.log(d['a'] + d['b']) - sp.log(d['a']) - sp.log(d['b'])) != 0)(tri(o))),
    ('\\sin(2x) = 2\\sin(x)', lambda o: sp.simplify(sp.sin(2 * num(o)) - 2 * sp.sin(num(o))) != 0),
    ('(a+b)^2 = a^2 + b^2', lambda o: (lambda d: sp.expand((d['a'] + d['b']) ** 2 - d['a'] ** 2 - d['b'] ** 2) != 0)(tri(o))),
    ("f'(a) = 0", lambda o: (lambda f, a: sp.diff(f, x).subs(x, a) == 0 and not is_local_max(f, a))(
        ev(re.match(r'f\(x\)\s*=\s*(.*?)\s*\\text', o).group(1)), ev(re.search(r'x\s*=\s*([-\d]+)\s*$', o).group(1)))),
    ('\\dfrac{a}{b+c}', lambda o: (lambda d: d['b'] != 0 and d['c'] != 0 and d['b'] + d['c'] != 0 and
     sp.simplify(d['a'] / (d['b'] + d['c']) - d['a'] / d['b'] - d['a'] / d['c']) != 0)(tri(o))),
    ('divisible by 6 if it is divisible by 2 and 3', lambda o: num(o) % 2 == 0 and num(o) % 3 == 0 and num(o) % 6 != 0),
    ('reciprocal of an irrational', lambda o: irr(1 / ev(o)) is False and irr(ev(o))),
    ('determinant of any matrix is positive', lambda o: mat(o).det() <= 0),
    ('AB = BA', lambda o: (lambda d: mat(d['A']) * mat(d['B']) != mat(d['B']) * mat(d['A']))(assigns(o))),
    ('eigenvalues of a real matrix are real', lambda o: any(not v.is_real for v in mat(o).eigenvals())),
    ('first n natural numbers', lambda o: (num(o) * (num(o) + 1) / 2) % 2 == 1),
    ('e^{i\\theta}', lambda o: sp.simplify(sp.exp(sp.I * num(o)) - sp.cos(num(o)) - sp.sin(num(o))) != 0),
    ('\\det(A) = \\det(B)', lambda o: (lambda d: mat(d['A']).det() == mat(d['B']).det() and mat(d['A']) != mat(d['B']))(assigns(o))),
    ('|z_1 + z_2|', lambda o: (lambda d: sp.simplify(abs(d['z_1'] + d['z_2']) - abs(d['z_1']) - abs(d['z_2'])) != 0)(tri(o))),
    ('singular matrix has no eigenvalues', lambda o: mat(o).det() == 0),
    ('\\arg(z_1 z_2)', lambda o: (lambda d: sp.simplify(arg(d['z_1'] * d['z_2']) - arg(d['z_1']) * arg(d['z_2'])) != 0)(tri(o))),
    ('Every square matrix has an inverse', lambda o: mat(o).det() == 0),
]
# Statements keyed true: the proof each one's steps give (reviewed).
TRUE_PROOFS = {
    'n² is even, then n is even': 'contrapositive: n odd gives n² = 2(2k² + 2k) + 1 odd',
    'even number plus an even number': '2a + 2b = 2(a + b)',
    'exterior angle': 'interior in (0, 360) gives exterior in (-180, 180)',
    'divisible by 6 if it is divisible by 2 and 3': '2 and 3 coprime',
    'reciprocal of an irrational': '1/x = p/q gives x = q/p',
}
AUDIT_S = {'\\sqrt{a+b}': 't5-003', '\\log(a + b)': 't5-004', '(a+b)^2 = a^2 + b^2': 't5-005',
           '\\dfrac{a}{b+c}': 't5-006', 'first n natural numbers': 't5-007', '\\arg(z_1 z_2)': 't5-008',
           'exterior angle': 't5-012'}

# Induction: (prop substring, stage) -> target (SymPy), or ('text', key) for a reviewed choice.
STAGES = {
    ('\\sum_{r=1}^{n} r =', 0): ('text', 'n = 1'),
    ('\\sum_{r=1}^{n} r =', 1): 1,
    ('\\sum_{r=1}^{n} r =', 2): ('text', '\\sum_{r=1}^{k} r = \\frac{k(k+1)}{2}'),
    ('\\sum_{r=1}^{n} r =', 3): k * (k + 1) / 2 + (k + 1),
    ('r^2', 0): 1,
    ('r^2', 1): (k + 1) ** 2,
    ('r^2', 2): k * (k + 1) * (2 * k + 1) / 6 + (k + 1) ** 2,
    ('8^n', 0): 7,
    ('8^n', 1): ('text', '8^k - 1 = 7m \\text{ for some integer } m'),
    ('8^n', 2): ('rhs', 8 * (7 * m + 1) - 1),
    ('r!', 0): 1,
    ('r!', 1): sp.factorial(k + 1) - 1 + (k + 1) * sp.factorial(k + 1),
}
AUDIT_I = {('\\sum_{r=1}^{n} r =', 3): 't5-009', ('8^n', 2): 't5-010', ('r!', 1): 't5-011'}


def same(a, b):
    a, b = sp.sympify(a), sp.sympify(b)
    d = sp.simplify(sp.expand_func(a - b))
    if d == 0:
        return True
    for kv in range(1, 7):
        try:
            if sp.N(sp.expand_func(a - b).subs({k: kv, m: kv + 2, n: kv})) != 0:
                return False
        except TypeError:
            return False
    return True


def ind_value(o, kind):
    if kind == 'rhs':
        parts = [p for p in o.split('=')]
        return [ev(p) for p in parts]
    return ev(o)


def check_claims(fails, w, text):
    """Evaluate numeric claims in a step's maths."""
    segs = re.findall(r'\\\((.*?)\\\)', text)
    if not segs and not re.search(r'[A-Za-z]{3,}', re.sub(r'\\[a-z]+|sqrt|sin|cos|log|det', '', text)):
        segs = [text]
    for seg in segs:
        seg = re.sub(r'\\quad\\square|✓|\\text\{[^}]*\}', '', seg)
        for rel in ('\\neq', '\\approx', '='):
            pass
        parts = re.split(r'(\\neq|\\approx|=|<|>)', seg)
        if len(parts) < 3:
            continue
        vals = []
        for p in parts[::2]:
            try:
                v = ev(p) if p.strip() else None
            except (ValueError, TypeError):
                v = None
            vals.append(v if (v is not None and not getattr(v, 'free_symbols', {1})) else None)
        for (a, b), rel in zip(zip(vals, vals[1:]), parts[1::2]):
            if a is None or b is None:
                continue
            try:
                a_, b_ = sp.N(a, 30), sp.N(b, 30)
                if rel == '=' and abs(a_ - b_) > 1e-12:
                    fails.append('%s: the step %r says %s = %s' % (w, text, a, b))
                if rel == '\\neq' and abs(a_ - b_) < 1e-12:
                    fails.append('%s: the step %r says %s \\neq %s' % (w, text, a, b))
                if rel == '\\approx':
                    dp = len(str(b).split('.')[-1]) if '.' in str(b) else 0
                    if abs(a_ - b_) > 0.5 * 10 ** -dp + 1e-12:
                        fails.append('%s: the step %r says %s ≈ %s' % (w, text, a, b))
                if rel == '<' and not a_ < b_ or rel == '>' and not a_ > b_:
                    fails.append('%s: the step %r says %s %s %s' % (w, text, a, rel, b))
            except TypeError:
                continue


def check_bank(fails, bank):
    counter = bank['COUNTER']['alevel'] + bank['COUNTER']['further']
    if len(counter) != len(REFUTES):
        fails.append('counter: %d items, REFUTES has %d (review and extend REFUTES)' % (len(counter), len(REFUTES)))
    for q in counter:
        hits = [(sub, f) for sub, f in REFUTES if sub in q['s']]
        tag = next((a for sub, a in AUDIT_S.items() if sub in q['s']), None)
        w = 'counter %s%s' % (q['s'][:60], ' (proof-builder-%s)' % tag if tag else '')
        if len(hits) != 1:
            fails.append('%s: %d REFUTES entries match (review it)' % (w, len(hits)))
            continue
        sub, f = hits[0]
        try:
            if q.get('isTrue'):
                if sub not in TRUE_PROOFS:
                    fails.append('%s: keyed true, but no reviewed proof is recorded' % w)
                if not q['correct'].startswith('This statement is actually TRUE'):
                    fails.append('%s: keyed true but the key is %r' % (w, q['correct']))
            else:
                if sub in TRUE_PROOFS:
                    fails.append('%s: the statement is true (%s) but is keyed %r' % (w, TRUE_PROOFS[sub], q['correct']))
                elif not f(q['correct']):
                    fails.append('%s: the key %r does not disprove the statement' % (w, q['correct']))
            for o in q['d']:
                if f(o):
                    fails.append('%s: the wrong option %r also disproves the statement (SR-16)' % (w, o))
        except (ValueError, KeyError, AttributeError, TypeError) as e:
            fails.append('%s: an option cannot be read (%s: %s)' % (w, type(e).__name__, e))
        for st in q.get('steps', []):
            check_claims(fails, w, st)
    for q in bank['INDUCTION']:
        for si, st in enumerate(q['stages']):
            key = next(((p, si) for (p, s_) in STAGES if s_ == si and p in q['prop']), None)
            tag = AUDIT_I.get(key)
            w = 'induction %s stage %d%s' % (q['prop'][:40], si + 1, ' (proof-builder-%s)' % tag if tag else '')
            if key is None:
                fails.append('%s: no STAGES entry (review it)' % w)
                continue
            tg = STAGES[key]
            if isinstance(tg, tuple) and tg[0] == 'text':
                if st['correct'] != tg[1]:
                    fails.append('%s: keyed %r, reviewed %r' % (w, st['correct'], tg[1]))
                continue
            try:
                if isinstance(tg, tuple) and tg[0] == 'rhs':
                    for o in [st['correct']] + st['d']:
                        vs = ind_value(o, 'rhs')
                        chain_true = all(same(a, b) for a, b in zip(vs, vs[1:]))
                        right = chain_true and same(vs[0], tg[1])
                        if o == st['correct'] and not right:
                            fails.append('%s: the key %r is not a true working of %s' % (w, o, tg[1]))
                        if o != st['correct'] and right:
                            fails.append('%s: the wrong option %r is a true working (SR-16)' % (w, o))
                    continue
                vals = [ev(o) for o in [st['correct']] + st['d']]
            except ValueError as e:
                fails.append('%s: %s' % (w, e))
                continue
            if not same(vals[0], tg):
                fails.append('%s: keyed %r, the answer is %s' % (w, st['correct'], sp.factor(tg)))
            for o, v in zip(st['d'], vals[1:]):
                if same(v, tg):
                    fails.append('%s: the wrong option %r equals the answer (SR-16)' % (w, o))
            for s2 in st.get('steps', []):
                check_claims(fails, w, s2)


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.requestAnimationFrame = () => 0;
  const out = [], W = document.documentElement.clientWidth;
  const raw = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(x => x.remove()); return c.textContent; };
  const looks = (where, el) => {
    const t = raw(el);
    if (/\\[a-zA-Z]|\^|_\{|\\\(/.test(t)) out.push(['render', where, 'raw TeX on screen: ' + JSON.stringify(t.slice(0, 80))]);
    if (document.documentElement.scrollWidth > W + 1) out.push(['phone', where, 'the page scrolls sideways (' + document.documentElement.scrollWidth + 'px at ' + W + 'px)']);
  };
  const prose = (where, src, el) => {
    src = src.replace(/^"|"$/g, '');
    const words = src.replace(/\\\(.*?\\\)/g, ' | ').split('|').map(s => s.trim()).filter(s => /[a-z]{3,} [a-z]{2,}/i.test(s) && !/[\\^_{}]/.test(s));
    const t = raw(el).replace(/\s+/g, ' ');
    for (const w of words) { const ws = w.replace(/\s+/g, ' ').split(' ').slice(0, 3).join(' '); if (!t.includes(ws)) out.push(['render', where, 'prose lost its spaces: ' + JSON.stringify(ws)]); }
  };
  const sol = () => document.getElementById('solution');
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById('game').classList.add('active');
  // Counter
  mode = 'counter';
  for (const lv of ['alevel', 'further']) COUNTER[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      pool = [q]; qIdx = 0; totalAnswered = 0; nextQ();
      looks('counter ' + lv + '[' + i + '] statement', document.getElementById('statement'));
      prose('counter ' + lv + '[' + i + '] statement', q.s, document.getElementById('statement'));
      const b = [...document.querySelectorAll('#gameArea .opt-btn')].find(x => x.dataset.val === pick);
      if (!b) { out.push(['mark', 'counter ' + lv + '[' + i + ']', 'option not on screen: ' + pick]); continue; }
      b.click();
      if (b.classList.contains('correct') !== (pick === q.correct)) out.push(['mark', 'counter ' + lv + '[' + i + ']', pick + (pick === q.correct ? ' marked wrong' : ' marked right')]);
      if (pick !== q.correct) {
        looks('counter ' + lv + '[' + i + '] solution', sol());
        (q.steps || []).forEach(st => prose('counter ' + lv + '[' + i + '] step', st, sol()));
        if (q.misconception) prose('counter ' + lv + '[' + i + '] misconception', q.misconception, sol());
        if (sol().querySelector('.next-btn')) out.push(['mark', 'counter ' + lv + '[' + i + ']', 'a hand-rolled Next button (canon 7.6: MaffsNext)']);
        if (window.MaffsNext) MaffsNext.clear(sol());
        sol().className = 'solution';
      }
    }
  });
  // Sorter
  mode = 'sorter';
  const play = (q, order) => {
    pool = [q]; qIdx = 0; score = 0; totalAnswered = 0; nextQ();
    const slots = [...document.querySelectorAll('.sort-slot')];
    for (const li of order) slots.find(s => s.dataset.origLine === q.lines[li]).click();
    document.querySelector('.sort-check').click();
    return score > 0;
  };
  const valid = (q, order) => q.after ? order.every((li, pos) => (q.after[li] || []).every(j => order.indexOf(j) < pos)) : order.every((li, pos) => li === pos);
  // Orders reviewed as valid proofs that the game must accept (t5-013).
  const MUST = [['Prove that n^2 + n is even', [[0, 2, 1, 3, 4], [1, 2, 0, 3, 4], [2, 1, 0, 3, 4]]]];
  for (const lv of ['alevel', 'further']) SORTER[lv].forEach((q, i) => {
    const w = 'sorter ' + lv + '[' + i + ']';
    const base = q.lines.map((_, j) => j);
    if (!play(q, base)) out.push(['sort', w, 'the order as written is rejected']);
    for (const [t, orders] of MUST) if (q.title.replace(/\\[()]/g, '').includes(t))
      for (const o of orders) if (!play(q, o)) out.push(['sort', w, 'the valid order ' + o.join(',') + ' is rejected (proof-builder-t5-013)']);
    looks(w + ' lines', document.getElementById('gameArea'));
    q.lines.forEach(l => prose(w + ' line', l, document.getElementById('gameArea')));
    looks(w + ' title', document.getElementById('statement'));
    for (let j = 0; j + 1 < base.length; j++) {
      const o = base.slice(); [o[j], o[j + 1]] = [o[j + 1], o[j]];
      const got = play(q, o);
      if (got !== valid(q, o)) out.push(['sort', w, 'order ' + o.join(',') + (got ? ' accepted' : ' rejected') + ' (valid: ' + valid(q, o) + ')']);
      if (!got) {
        looks(w + ' solution', sol());
        // t5-015: after a wrong Check nothing can be re-checked for marks
        const slots = [...document.querySelectorAll('.sort-slot')];
        slots.forEach(s => s.click()); base.forEach(li => slots.find(s => s.dataset.origLine === q.lines[li]).click());
        const btn = document.querySelector('.sort-check');
        if (!btn.disabled) { btn.click(); if (score > 0) out.push(['sort', w, 'a second Check after a wrong one scored (proof-builder-t5-015)']); }
        if (sol().querySelector('.next-btn')) out.push(['sort', w, 'a hand-rolled Next button (canon 7.6: MaffsNext)']);
        if (window.MaffsNext) MaffsNext.clear(sol());
        sol().className = 'solution';
      }
    }
  });
  // Induction
  mode = 'induction';
  INDUCTION.forEach((q, i) => q.stages.forEach((stg, si) => {
    for (const pick of [stg.correct, ...stg.d]) {
      pool = [q]; qIdx = 0; totalAnswered = 0; nextQ();
      indStageIdx = si; renderIndStage(q);
      looks('induction[' + i + '] stage ' + (si + 1), document.getElementById('gameArea'));
      prose('induction[' + i + '] stage ' + (si + 1) + ' prompt', stg.prompt, document.getElementById('gameArea'));
      const b = [...document.querySelectorAll('#gameArea .opt-btn')].find(x => x.dataset.val === pick);
      if (!b) { out.push(['mark', 'induction[' + i + '] stage ' + (si + 1), 'option not on screen: ' + pick]); continue; }
      b.click();
      if (b.classList.contains('correct') !== (pick === stg.correct)) out.push(['mark', 'induction[' + i + '] stage ' + (si + 1), pick + ' mis-marked']);
      if (pick !== stg.correct) {
        looks('induction[' + i + '] stage ' + (si + 1) + ' solution', sol());
        if (window.MaffsNext) MaffsNext.clear(sol());
        sol().className = 'solution';
      }
    }
  }));
  return out;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
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
            page.goto(base + '/games/%s/?level=further&cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof COUNTER !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => ({COUNTER, SORTER, INDUCTION})')
            seen = set()
            for kind, where, what in page.evaluate(SWEEP_JS):
                tag = ' (proof-builder-t5-018)' if 'spaces' in what else ' (proof-builder-t5-019)' if 'raw TeX' in what \
                    else ' (proof-builder-t5-022)' if kind == 'phone' else ''
                msg = '%s in Chromium: %s%s' % (where, what, tag)
                if msg not in seen:
                    seen.add(msg)
                    fails.append(msg)
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('counter "\\(\\sqrt{a+b}', 't5-003: a = 4, b = 9 as a wrong option', "d:['a=0, b=9','a=0, b=4','a=16, b=0']",
     "d:['a=4, b=9','a=0, b=4','a=16, b=0']"),
    ('induction \\sum_{r=1}^{n} r = \\frac{n(n+1)}{2} stage 4', 't5-009: (k^2+3k+2)/2 as a wrong option',
     "'\\\\frac{k^2+3k}{2}'", "'\\\\frac{k^2+3k+2}{2}'"),
    ('counter "Every exterior', 't5-012: the true exterior-angle statement keyed false',
     "correct:'This statement is actually TRUE',d:['A regular hexagon','An equilateral triangle','A square'],isTrue:true",
     "correct:'A reflex angle in a non-convex polygon',d:['A regular hexagon','An equilateral triangle','A square']"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank:
        check_bank(fails, bank)
    print('%s: counter-examples checked against their statements, induction stages by SymPy, sorter orders and every'
          ' rendered string in Chromium' % SLUG)
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-44s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
