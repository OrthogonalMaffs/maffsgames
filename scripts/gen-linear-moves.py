#!/usr/bin/env python3
"""Linear Equation Solver: every move phase's options, classified by search (Jon's design, 7 Oct 2026).

    python scripts/gen-linear-moves.py            # check: the page's MOVES block equals what this builds
    python scripts/gen-linear-moves.py --write    # rebuild the block between the GENERATED MOVES markers
    python scripts/gen-linear-moves.py --report   # every question's start options, one line each

The game asks "What is the optimal move here?" at each move phase. This script decides, for every question
and every state a student can reach, which moves are on offer and what each one is:

  optimal  a valid move that reaches x = <value> in the fewest further steps. Ties are broken by not
           introducing fractions: a move whose shortest route has a line with a non-integer number that
           is not already in the starting equation loses to one whose route has none. Every move still
           tied is optimal (green, full marks).
  slower   a valid move that is not optimal: more steps, or a fraction the optimal move avoids (amber,
           half marks, streak kept, "This works, but it's slower").
  error    a genuine slip, which changes the solution (red, with its reason): the move applied to one side
           only; only the x-term divided; one term divided but not the constant; the carry-across slip
           (a term or factor taken to the other side without being inverted: x - 7 = 5 -> x = 5 - 7).

A VALID move applies the inverse of an operation present in the equation to both whole sides: subtract an
added constant (add a subtracted one), divide by a multiplier, multiply by a divisor, multiply by -1 to clear
a sign. Moves that are legal but undo nothing (adding 7 to both sides of x + 7 = 12) are never offered (Jon,
7 Oct 2026: SR-13 stands; the wrong inverse is shown as the carry-across slip).

Each phase shows four options: the optimal moves (one or two), one slower move where one exists, and genuine
errors for the rest (at least one). Options are written as the move applied, the way a teacher writes it on
the board (3x + 7 - 7 = 22 - 7), so a slip is visible as the slip a student makes.

Every question's states are generated: the start, every line a valid option leads to, and the line the
optimal move leads to after an error (the game continues from there). The game looks options up; it never
decides a class itself. scripts/verify-linear-equation-solver.py re-derives every class independently.

Stdlib only (fractions). Reads the question bank (eq, ops, ans) from the page; writes only between
"// >>> GENERATED MOVES START" and "// >>> GENERATED MOVES END".
"""
import argparse, json, os, re, sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, 'games', 'linear-equation-solver', 'index.html')
START = '// >>> GENERATED MOVES START — built by scripts/gen-linear-moves.py, do not edit by hand'
END = '// >>> GENERATED MOVES END'
DEPTH = 3


# ------------------------------------------------------------------ numbers and TeX
def tex_num(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return (r'-\frac{%d}{%d}' % (-v.numerator, v.denominator)) if v < 0 \
        else (r'\frac{%d}{%d}' % (v.numerator, v.denominator))


def paren(v):
    """A number as a factor or an operand that follows an operator: negatives in brackets."""
    return '(%s)' % tex_num(v) if F(v) < 0 else tex_num(v)


def words_num(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return '%s%d/%d' % ('-' if v < 0 else '', abs(v.numerator), v.denominator)


# ------------------------------------------------------------------ states
# A state is a dict: form ('lin' p*x + q, 'br' k(x + b), 'ov' (x + b)/k), the numbers, the constant c on
# the other side, xside 'L' or 'R', order ('xq' or 'qx' for lin) and style ('over' writes p = +-1/n as
# \frac{x}{n}).
def S(form, xside, c, **kw):
    s = {'form': form, 'xside': xside, 'c': F(c), 'order': kw.get('order', 'xq'), 'style': kw.get('style', 'coef')}
    for k in ('p', 'q', 'k', 'b'):
        if k in kw:
            s[k] = F(kw[k])
    return s


def key(s):
    return line(s)


def solved(s):
    return s['form'] == 'lin' and s['p'] == 1 and s['q'] == 0


def value(s):
    """The solution of the state's equation."""
    if s['form'] == 'lin':
        return (s['c'] - s['q']) / s['p']
    if s['form'] == 'br':
        return s['c'] / s['k'] - s['b']
    return s['c'] * s['k'] - s['b']


def coef_tex(p, style):
    if p == 1:
        return 'x'
    if p == -1:
        return '-x'
    if p.denominator == 1:
        return '%dx' % p.numerator
    if style == 'over' and abs(p.numerator) == 1:
        return ('-' if p < 0 else '') + r'\frac{x}{%d}' % p.denominator
    return tex_num(p) + 'x'


def xside_tex(s):
    f = s['form']
    if f == 'br':
        return '%s(x %s %s)' % (tex_num(s['k']), '+' if s['b'] > 0 else '-', tex_num(abs(s['b'])))
    if f == 'ov':
        return r'\frac{x %s %s}{%s}' % ('+' if s['b'] > 0 else '-', tex_num(abs(s['b'])), tex_num(s['k']))
    p, q = s['p'], s['q']
    if q == 0:
        return coef_tex(p, s['style'])
    if s['order'] == 'qx':
        return '%s %s %s' % (tex_num(q), '-' if p < 0 else '+', coef_tex(abs(p), s['style']))
    return '%s %s %s' % (coef_tex(p, s['style']), '+' if q > 0 else '-', tex_num(abs(q)))


def eqn(xs, other, xside):
    return '%s = %s' % ((xs, other) if xside == 'L' else (other, xs))


def line(s):
    return eqn(xside_tex(s), tex_num(s['c']), s['xside'])


def numbers(s):
    """Every number written in the state's line (absolute values)."""
    out = {abs(s['c'])}
    if s['form'] == 'lin':
        out |= {abs(s['p']), abs(s['q'])}
    else:
        out |= {abs(s['k']), abs(s['b'])}
    return out


# ------------------------------------------------------------------ parsing the shipped start equations
NUM = r'-?(?:\\frac\{\d+\}\{\d+\}|\d+)'


def num(t):
    t = t.strip()
    neg = t.startswith('-')
    t = t.lstrip('-').strip()
    m = re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}', t)
    v = F(int(m.group(1)), int(m.group(2))) if m else F(int(t))
    return -v if neg else v


def parse_coef(t):
    """'x', '-x', '3x', '\\frac{2}{3}x', '\\frac{x}{4}', '-\\frac{x}{3}' -> (p, style)."""
    t = t.replace(' ', '')
    neg = t.startswith('-')
    t = t[1:] if neg else t
    m = re.fullmatch(r'\\frac\{x\}\{(\d+)\}', t)
    if m:
        p, style = F(1, int(m.group(1))), 'over'
    elif t == 'x':
        p, style = F(1), 'coef'
    else:
        m = re.fullmatch(r'(\\frac\{\d+\}\{\d+\}|\d+)x', t)
        if not m:
            raise ValueError('coefficient ' + t)
        p, style = num(m.group(1)), 'coef'
    return (-p if neg else p), style


def parse_side(t):
    t = t.strip()
    m = re.fullmatch(r'(\d+)\(x ([+-]) (\d+)\)', t)
    if m:
        return {'form': 'br', 'k': F(int(m.group(1))), 'b': F(int(m.group(3))) * (1 if m.group(2) == '+' else -1)}
    m = re.fullmatch(r'\\frac\{x ([+-]) (\d+)\}\{(\d+)\}', t)
    if m:
        return {'form': 'ov', 'k': F(int(m.group(3))), 'b': F(int(m.group(2))) * (1 if m.group(1) == '+' else -1)}
    if 'x' not in t:
        return None
    # lin: "<coef> [+-] <num>" or "<num> [+-] <coef>" or "<coef>"
    m = re.fullmatch(r'(.*x\}?|-?\\frac\{x\}\{\d+\}) ([+-]) (\d+)', t)
    if m:
        p, style = parse_coef(m.group(1))
        return {'form': 'lin', 'p': p, 'q': F(int(m.group(3))) * (1 if m.group(2) == '+' else -1), 'order': 'xq', 'style': style}
    m = re.fullmatch(r'(\d+) ([+-]) (.*x)', t)
    if m:
        p, style = parse_coef(m.group(3))
        return {'form': 'lin', 'p': p if m.group(2) == '+' else -p, 'q': F(int(m.group(1))), 'order': 'qx', 'style': style}
    p, style = parse_coef(t)
    return {'form': 'lin', 'p': p, 'q': F(0), 'order': 'xq', 'style': style}


def parse_eq(t):
    l, r = [x.strip() for x in t.split('=')]
    pl, pr = parse_side(l), parse_side(r)
    xside, side, other = ('L', pl, r) if pl else ('R', pr, l)
    s = {'xside': xside, 'c': num(other), 'order': 'xq', 'style': 'coef'}
    s.update(side)
    return s


# ------------------------------------------------------------------ valid moves (inverse operations)
def mul_state(s, k):
    """Both whole sides multiplied by k (division is k = 1/m)."""
    f = s['form']
    if f == 'lin':
        p, q = s['p'] * k, s['q'] * k
        return dict(s, p=p, q=q, c=s['c'] * k)
    # br: k(x + b) / k = x + b ; ov: (x + b)/k * k = x + b
    return {'form': 'lin', 'p': F(1), 'q': s['b'], 'c': s['c'] * k, 'xside': s['xside'], 'order': 'xq', 'style': 'coef'}


def add_state(s, d):
    return dict(s, q=s['q'] + d, c=s['c'] + d)


def valid_moves(s):
    """[(move, next state)]: every inverse of an operation present, applied to both whole sides."""
    out = []
    f = s['form']
    if f == 'br':
        k = F(1) / s['k']
        out.append((('mul', k), mul_state(s, k)))
        return out
    if f == 'ov':
        out.append((('mul', s['k']), mul_state(s, s['k'])))
        return out
    p, q = s['p'], s['q']
    if q != 0:
        out.append((('add', -q), add_state(s, -q)))
    if p != 1:
        sg = -1 if p < 0 else 1
        a, b = abs(p.numerator), p.denominator
        ks = set()
        for i in ((0, 1) if sg < 0 else (0,)):
            for j in ((0, 1) if b > 1 else (0,)):
                for l in ((0, 1) if a > 1 else (0,)):
                    if i or j or l:
                        ks.add(F(sg ** i * b ** j, a ** l))
        for k in sorted(ks, key=lambda k: (abs(k - 1 / p) != 0, abs(k), k)):
            out.append((('mul', k), mul_state(s, k)))
    return out


def new_fraction(s, start_numbers):
    return any(v.denominator != 1 and v not in start_numbers for v in numbers(s))


def search(s, depth, start_numbers, memo):
    """(fewest further steps, whether some shortest route has no line introducing a fraction) or (None, False)."""
    k = (key(s), depth)
    if k in memo:
        return memo[k]
    if solved(s):
        memo[k] = (0, True)
        return memo[k]
    best, clean = None, False
    if depth > 0:
        for _m, t in valid_moves(s):
            n, c = search(t, depth - 1, start_numbers, memo)
            if n is None:
                continue
            c = c and (solved(t) or not new_fraction(t, start_numbers))
            if best is None or n + 1 < best:
                best, clean = n + 1, c
            elif n + 1 == best:
                clean = clean or c
    memo[k] = (best, clean)
    return memo[k]


def classify(s, start_numbers, memo):
    """[(move, next, total steps, clean)], the optimal set, the slower set."""
    rows = []
    for m, t in valid_moves(s):
        n, c = search(t, DEPTH - 1, start_numbers, memo)
        if n is None:
            continue
        c = c and (solved(t) or not new_fraction(t, start_numbers))
        rows.append((m, t, n + 1, c))
    best = min(r[2] for r in rows)
    tied = [r for r in rows if r[2] == best]
    if any(r[3] for r in tied):
        tied = [r for r in tied if r[3]]
    opt = []
    for r in tied:                       # equal as moves (x(-1) and /(-1)) are one move
        if all(key(r[1]) != key(o[1]) for o in opt):
            opt.append(r)
    slow = [r for r in rows if all(key(r[1]) != key(o[1]) for o in opt)]
    return rows, opt, slow


# ------------------------------------------------------------------ move text: applied form, trail, words
def op_tex(m):
    kind, v = m
    if kind == 'add':
        return (r'+\,%s' if v > 0 else r'-\,%s') % tex_num(abs(v))
    if v.denominator == 1:
        return r'\times\,%s' % paren(v)
    if v.numerator in (1, -1):
        return r'\div\,%s' % paren(F(v.numerator * v.denominator))
    return r'\times\,%s' % paren(v)


def op_words(m):
    kind, v = m
    if kind == 'add':
        return ('add %s to both sides' if v > 0 else 'subtract %s from both sides') % words_num(abs(v))
    if v.denominator == 1 or v.numerator not in (1, -1):
        return 'multiply both sides by %s' % words_num(v)
    return 'divide both sides by %s' % words_num(F(v.numerator * v.denominator))


def is_div(m):
    return m[0] == 'mul' and m[1].denominator != 1 and m[1].numerator in (1, -1)


def term_tex(s):
    """The x-side's terms as written: [x-term, constant-term or None] (lin only)."""
    p, q = s['p'], s['q']
    xt = coef_tex(p, s['style'])
    return xt, (None if q == 0 else q)


def applied(s, m, scope='both'):
    """The move written out: scope 'both', 'x' (the x-side only) or 'other' (the other side only)."""
    kind, v = m
    xs, other = xside_tex(s), tex_num(s['c'])
    if kind == 'add':
        tail = ' %s %s' % ('+' if v > 0 else '-', tex_num(abs(v)))
        X = xs + tail if scope in ('both', 'x') else xs
        O = other + tail if scope in ('both', 'other') else other
        return eqn(X, O, s['xside'])
    if is_div(m):
        d = F(v.numerator * v.denominator)
        dt = tex_num(d)

        def over(t):
            return r'\frac{%s}{%s}' % (t, dt)
        if s['form'] == 'lin' and s['q'] != 0:
            xt, q = term_tex(s)
            if s['order'] == 'qx':
                Xd = '%s %s %s' % (over(tex_num(q)), '-' if s['p'] < 0 else '+', over(coef_tex(abs(s['p']), s['style'])))
            else:
                Xd = '%s %s %s' % (over(xt), '+' if q > 0 else '-', over(tex_num(abs(q))))
        else:
            Xd = over(xs)
        X = Xd if scope in ('both', 'x') else xs
        O = over(other) if scope in ('both', 'other') else other
        return eqn(X, O, s['xside'])
    # multiply
    f = paren(v) + r' \times '
    if s['form'] == 'lin' and s['q'] != 0:
        xt, q = term_tex(s)
        if s['order'] == 'qx':
            Xm = '%s%s %s %s%s' % (f, paren(q), '-' if s['p'] < 0 else '+', f, coef_tex(abs(s['p']), s['style']))
        else:
            Xm = '%s%s %s %s%s' % (f, '(' + xt + ')' if xt.startswith('-') else xt, '+' if q > 0 else '-', f, tex_num(abs(q)))
    elif s['form'] == 'lin':
        xt = coef_tex(s['p'], s['style'])
        Xm = f + ('(' + xt + ')' if xt.startswith('-') else xt)
    else:
        Xm = f + xs
    X = Xm if scope in ('both', 'x') else xs
    O = f + paren(s['c']) if scope in ('both', 'other') else other
    return eqn(X, O, s['xside'])


# ------------------------------------------------------------------ genuine errors
def err_value(kind, s, m):
    """The solution of the equation the slip leaves, or None if the slip does not apply here."""
    v = m[1]
    if kind in ('one-side', 'other-side'):
        if m[0] == 'add':
            t = add_state(s, v) if kind == 'one-side' else s
            c = s['c'] if kind == 'one-side' else s['c'] + v
            t = dict(t, c=c)
            return value(t), applied(s, m, 'x' if kind == 'one-side' else 'other')
        t = mul_state(s, v)
        t = dict(t, c=s['c']) if kind == 'one-side' else dict(s, c=s['c'] * v)
        return value(t), applied(s, m, 'x' if kind == 'one-side' else 'other')
    if kind == 'carry':
        # the term or factor crosses the equals sign without being inverted
        if m[0] == 'add':
            if s['form'] != 'lin' or s['q'] == 0 or v != -s['q']:
                return None
            t = dict(s, q=F(0), c=s['c'] + s['q'])
            other = '%s %s %s' % (tex_num(s['c']), '+' if s['q'] > 0 else '-', tex_num(abs(s['q'])))
            return value(t), eqn(coef_tex(s['p'], s['style']), other, s['xside'])
        f = s['form']
        if f == 'lin' and s['q'] == 0 and v == 1 / s['p']:
            p = s['p']
            t = dict(s, p=F(1), c=s['c'] * p)
            if p.denominator == 1:
                other = r'%s \times %s' % (tex_num(s['c']), paren(p))
            elif abs(p.numerator) == 1:
                other = r'\frac{%s}{%s}' % (tex_num(s['c']), tex_num(F(p.denominator) * (1 if p > 0 else -1)))
            else:
                other = r'%s \times %s' % (tex_num(p), paren(s['c']))
            return value(t), eqn('x', other, s['xside'])
        if f == 'br':
            t = {'form': 'lin', 'p': F(1), 'q': s['b'], 'c': s['c'] * s['k']}
            xs = 'x %s %s' % ('+' if s['b'] > 0 else '-', tex_num(abs(s['b'])))
            return value(t), eqn(xs, r'%s \times %s' % (tex_num(s['c']), tex_num(s['k'])), s['xside'])
        if f == 'ov':
            t = {'form': 'lin', 'p': F(1), 'q': s['b'], 'c': s['c'] / s['k']}
            xs = 'x %s %s' % ('+' if s['b'] > 0 else '-', tex_num(abs(s['b'])))
            return value(t), eqn(xs, r'\frac{%s}{%s}' % (tex_num(s['c']), tex_num(s['k'])), s['xside'])
        return None
    if kind in ('x-only', 'const-kept'):
        # a multiplicative move applied to the x-term only (and to the other side for const-kept)
        if s['form'] != 'lin' or s['q'] == 0 or m[0] != 'mul':
            return None
        t = dict(s, p=s['p'] * v, c=s['c'] * v if kind == 'const-kept' else s['c'])
        xt, q = term_tex(s)
        if is_div(m):
            d = tex_num(F(v.numerator * v.denominator))
            xpart = r'\frac{%s}{%s}' % (coef_tex(abs(s['p']), s['style']) if s['order'] == 'qx' else xt, d)
            o = r'\frac{%s}{%s}' % (tex_num(s['c']), d) if kind == 'const-kept' else tex_num(s['c'])
        else:
            f = paren(v) + r' \times '
            xpart = f + (coef_tex(abs(s['p']), s['style']) if s['order'] == 'qx' else ('(' + xt + ')' if xt.startswith('-') else xt))
            o = f + paren(s['c']) if kind == 'const-kept' else tex_num(s['c'])
        if s['order'] == 'qx':
            X = '%s %s %s' % (tex_num(q), '-' if s['p'] < 0 else '+', xpart)
        else:
            X = '%s %s %s' % (xpart, '+' if q > 0 else '-', tex_num(abs(q)))
        return value(t), eqn(X, o, s['xside'])
    raise ValueError(kind)


REASON = {
    'one-side': 'That changes one side only. Whatever you do to one side, do to the other, or the two sides stop being equal.',
    'other-side': 'That changes one side only. Whatever you do to one side, do to the other, or the two sides stop being equal.',
    'carry': None,       # built per move (names the term)
    'x-only': None,
    'const-kept': None,
}


def reason(kind, s, m):
    v = m[1]
    if kind in ('one-side', 'other-side'):
        return REASON[kind]
    if kind == 'carry':
        if m[0] == 'add':
            q = s['q']
            return ('The %s crossed the equals sign without changing: it is %s on this side, so moving it '
                    'across means %s.') % (words_num(abs(q)), 'added' if q > 0 else 'taken away',
                                           op_words(m))
        return 'The %s crossed the equals sign without being undone. To undo it, %s.' % (
            'multiplier' if (s['form'] in ('lin', 'br') and not (s['form'] == 'lin' and abs(s['p'].numerator) == 1 and s['p'].denominator > 1)) else 'divisor',
            op_words(m))
    what = 'divided' if is_div(m) else 'multiplied'
    if kind == 'x-only':
        return 'Only the x-term was %s. Every term on both sides has to be %s, or the balance breaks.' % (what, what)
    return 'The %s was not %s. %s a side means %s every term on it, the %s included.' % (
        words_num(abs(s['q'])), what, 'Dividing' if is_div(m) else 'Multiplying',
        'dividing' if is_div(m) else 'multiplying', words_num(abs(s['q'])))


def hint_for(s, opt):
    m = opt[0][0]
    kind, v = m
    if kind == 'add':
        q = s['q']
        return '%s has been %s x. Undo it: %s.' % (words_num(abs(q)), 'added to' if q > 0 else 'taken from', op_words(m))
    return 'Undo what is done to x: %s.' % op_words(m)


# ------------------------------------------------------------------ building one question
def build(q):
    start = parse_eq(q['eq'])
    if line(start) != q['eq']:
        raise SystemExit('%s: the start line rebuilds as %r, not %r' % (q['id'], line(start), q['eq']))
    start_numbers = numbers(start)
    memo = {}
    states, todo = {}, [(key(start), start)]
    keyed = keyed_route(q, start)
    while todo:
        k, s = todo.pop(0)
        if k in states or solved(s):
            continue
        rows, opt, slow = classify(s, start_numbers, memo)
        offered = [('opt', r) for r in opt[:2]]
        if slow:
            # one slower move: fewest steps first, then the one that brings in a fraction (the "other order"),
            # then the move list's own order
            pick = sorted(slow, key=lambda r: (r[2], r[2] != opt[0][2], not r[3], valid_moves(s).index((r[0], r[1]))))[0]
            offered.append(('slow', pick))
        sol = value(s)
        errs, seen = [], {key(r[1]) for _c, r in offered}
        prio = []
        for _c, r in offered:
            m = r[0]
            prio += [('carry', m)] if _c == 'opt' else []
        for _c, r in offered:
            prio += [('const-kept', r[0]), ('x-only', r[0])]
        for _c, r in offered:
            prio += [('one-side', r[0]), ('other-side', r[0])] if _c == 'opt' else []
        for kind, m in prio:
            got = err_value(kind, s, m)
            if got is None:
                continue
            val, tex = got
            if val == sol or tex in seen or any(tex == e['t'] for e in errs):
                continue
            errs.append({'t': tex, 'c': 'err', 'kind': kind, 'why': reason(kind, s, m)})
            if len(offered) + len(errs) == 4:
                break
        if not errs:
            raise SystemExit('STOP: %s at %s has no genuine-error option' % (q['id'], k))
        opts = []
        best = opt[0][2]
        opt_words = [op_words(r[0]) for r in opt]
        for c, r in offered:
            m, t, n, clean = r
            o = {'t': applied(s, m), 'c': c, 'op': op_tex(m), 'w': op_words(m), 'n': key(t), 'steps': n}
            if c == 'slow':
                o['why'] = ('It needs %d steps; the optimal move needs %d.' % (n, best)) if n > best else \
                    'It brings in fractions; the optimal move keeps whole numbers.'
            opts.append(o)
            if not solved(t):
                todo.append((key(t), t))
        opts += errs
        st = {'line': k, 'opts': opts, 'best': opt_words, 'hint': hint_for(s, opt)}
        if k in keyed:
            st['keyed'] = keyed[k]
        states[k] = st
        # after an error the game continues along the first optimal move (the keyed one where it is optimal)
        for r in opt:
            if not solved(r[1]):
                todo.append((key(r[1]), r[1]))
    # the keyed move must be optimal at every keyed state
    for k, i in keyed.items():
        st = states[k]
        kop = q['ops'][i]['correct']
        if not any(o['c'] == 'opt' and o['op'] == kop for o in st['opts']):
            raise SystemExit('STOP: %s phase %d keyed %s is not optimal at %s (optimal: %s)' % (
                q['id'], i + 1, kop, k, st['best']))
    # the optimal moves first in each state's list, so the game's error path continues along the keyed move
    for k, st in states.items():
        if 'keyed' in st:
            kop = q['ops'][st['keyed']]['correct']
            st['opts'].sort(key=lambda o: (o['c'] != 'opt', o.get('op') != kop))
    return {'start': key(start), 'states': states, 'alt': alt_routes(q, start, start_numbers)}


def keyed_route(q, start):
    """{state line: phase index} along the keyed moves; each keyed line must equal the bank's own line."""
    out, s = {}, start
    for i, op in enumerate(q['ops']):
        out[line(s)] = i
        m = next((m for m, _t in valid_moves(s) if op_tex(m) == op['correct']), None)
        if m is None:
            raise SystemExit('%s: keyed move %s is not a valid move at %s' % (q['id'], op['correct'], line(s)))
        s = [t for mm, t in valid_moves(s) if mm == m][0]
        if 'line' in op and line(s) != op['line']:
            raise SystemExit('%s: keyed line %r, generated %r' % (q['id'], op['line'], line(s)))
    if not solved(s):
        raise SystemExit('%s: the keyed moves end at %s' % (q['id'], line(s)))
    return out


def alt_routes(q, start, start_numbers):
    """Every optimal route other than the keyed one, as worked-solution lines."""
    memo, routes = {}, []

    def walk(s, path):
        if solved(s):
            routes.append(path)
            return
        _rows, opt, _slow = classify(s, start_numbers, memo)
        for m, t, _n, _c in opt:
            walk(t, path + [(m, t)])
    walk(start, [])
    keyed = [op['correct'] for op in q['ops']]
    out = []
    for r in routes:
        if [op_tex(m) for m, _t in r] == keyed:
            continue
        steps = [line(start)]
        for m, t in r:
            steps.append(r'\text{%s}' % (op_words(m)[0].upper() + op_words(m)[1:]))
            steps.append(line(t) if not solved(t) else 'x = %s' % tex_num(value(t)))
        out.append(steps)
    return out


# ------------------------------------------------------------------ the page
def read_bank(html):
    out = []
    for m in re.finditer(r'\{id:"(\w+)", tag:"[^"]+", eq:"((?:[^"\\]|\\.)*)", ops:\[(.*?)\], ans:', html):
        ops = []
        for o in re.finditer(r'\{correct:"((?:[^"\\]|\\.)*)"(.*?)\}(?=,\{correct|$)', m.group(3)):
            d = {'correct': json.loads('"%s"' % o.group(1))}
            ln = re.search(r'line:"((?:[^"\\]|\\.)*)"', o.group(2))
            if ln:
                d['line'] = json.loads('"%s"' % ln.group(1))
            ops.append(d)
        out.append({'id': m.group(1), 'eq': json.loads('"%s"' % m.group(2)), 'ops': ops})
    return out


def render(moves):
    rows = ['const MOVES = {']
    for qid, mv in moves.items():
        rows.append('  %s: %s,' % (json.dumps(qid), json.dumps(mv, ensure_ascii=False, separators=(',', ':'))))
    rows.append('};')
    return '\n'.join(rows)


def build_all(html):
    bank = read_bank(html)
    if len(bank) != 141:
        raise SystemExit('read %d questions, expected 141' % len(bank))
    return {q['id']: build(q) for q in bank}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--game', default=GAME)
    a = ap.parse_args()
    html = open(a.game, encoding='utf-8').read()
    moves = build_all(html)
    block = START + '\n' + render(moves) + '\n' + END
    if a.report:
        for qid, mv in moves.items():
            st = mv['states'][mv['start']]
            print('%-4s %-28s %s' % (qid, st['line'], ' | '.join('%s:%s' % (o['c'], o['t']) for o in st['opts'])))
        n = sum(len(mv['states']) for mv in moves.values())
        print('%d questions, %d states, %d with an alternative optimal route' % (
            len(moves), n, sum(1 for mv in moves.values() if mv['alt'])))
    has = START in html and END in html
    if a.write:
        if has:
            html = html[:html.index(START)] + block + html[html.index(END) + len(END):]
        else:
            anchor = '// >>> GENERATED BANK END'
            html = html.replace(anchor, anchor + '\n\n' + block, 1)
        open(a.game, 'w', encoding='utf-8').write(html)
        print('wrote %d questions' % len(moves))
        return 0
    if not has or html[html.index(START):html.index(END) + len(END)] != block:
        print('FAIL: the page\'s MOVES block differs from what gen-linear-moves.py builds (run --write)')
        return 1
    print('PASS: MOVES matches the generator (%d questions)' % len(moves))
    return 0


if __name__ == '__main__':
    sys.exit(main())
