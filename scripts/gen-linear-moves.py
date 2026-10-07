#!/usr/bin/env python3
"""Generate Linear Equation Solver's move options (Jon's design, 7 Oct 2026).

The game asks "What is the optimal move here?" at every step, and a student may take any valid route. For each
question this script starts from its equation, searches every candidate move to depth 3, and writes the option sets
for every line a student can reach by an offered valid move, between the GENERATED MOVES markers of
games/linear-equation-solver/index.html. The QUESTIONS bank (equations, keyed moves, worked steps, answer options) is
read from the page and never changed here.

THE MOVE LANGUAGE. A move does one thing to both sides: + k, - k, x k or / k (never x 0 or / 0, SR-13). The
candidates at a line are built from the numbers written in it: every written number, its numerator and denominator,
its reciprocal, and 1, each used with + and -, and with x and / both signed. A both-sides move is always valid.

THE SEARCH. A line's x-side is held as layers applied to x, inner first (3x + 7 is [x3, +7]; 2(x + 3) is [+3, x2];
(x + 4)/3 is [+4, x1/3]); x k distributes over an outer + layer. A line is solved when x is alone. A route's cost is
(moves to solved, whether any intermediate line has a fractional constant), compared in that order.
  - optimal: a move that starts a cheapest route. Every move still tied is optimal (both -5 and x2 on x/2 + 5 = 11).
  - slower (amber): a valid move that is one move closer to solved but loses the fraction tie-break (/3 on
    3x + 7 = 22 gives x + 7/3 = 22/3).
  - any other valid move is legal but useless, and is never offered.
  "Fraction" means a fractional constant (a + layer or the other side). A coefficient does not count, because Jon's
  own example scores x/2 = 6 as fraction-free.

THE OPTIONS. Four per line where four honest ones exist: every optimal move (one per distinct line, the keyed move
first), one slower move where one exists, and genuine errors to fill (at least one). Each error is named:
  one-side  the move done to one side only (the x side, or the number side)
  xonly     only the x-term divided (or multiplied); the constant and the other side left alone
  constnot  the x-term and the other side divided, the constant not
  carry     carried across without changing it: x + 7 = 12 -> x = 12 + 7 (and x6 carried across as x6)
An error must give a different solution from the line it came from, so no valid move is ever red.
Each option shows the line the move produces with the number side unevaluated (x = 12 - 7), so the answer phase still
asks for the value.

THE PAGE'S FORM. MOVES[id] = {s: lines, r: optimal routes (the keyed route first)}; a line is [equation, hint,
options]; an option is [move, line, 'b' | 's', next line index (-1: x is alone)] or [move, line, 'e', code, ...]
(code x/n one side, c carry, o xonly, k constnot; o and k add the constant left alone and 'd'/'m'). The keyed (or
first optimal) option is first. The feedback sentences are worded by the page (feedback() in the game) from these
fields: storing them per option made the page three times its size and tier 4's tracing of it take minutes.

    python scripts/gen-linear-moves.py            # report only
    python scripts/gen-linear-moves.py --write    # write the MOVES block into the page
    python scripts/gen-linear-moves.py --check    # fail if the page differs from what this script writes
"""
import argparse
import json
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(os.path.dirname(HERE), 'games', 'linear-equation-solver', 'index.html')
BANK_START = '// >>> GENERATED BANK START'
BANK_END = '// >>> GENERATED BANK END'
START = '// >>> GENERATED MOVES START — built by scripts/gen-linear-moves.py, do not edit by hand'
END = '// >>> GENERATED MOVES END'
DEPTH = 3


# ------------------------------------------------------------------ reading the bank
def read_bank(html):
    block = html[html.index(BANK_START):html.index(BANK_END)]
    body = block[block.index('const QUESTIONS = {'):]
    body = body[body.index('[') :body.rindex(']') + 1]
    body = re.sub(r'([{,]\s*)([A-Za-z_]\w*):', r'\1"\2":', body)
    return json.loads(body)


# ------------------------------------------------------------------ TeX numbers
def tex_num(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = r'\frac{%d}{%d}' % (abs(v.numerator), v.denominator)
    return '-' + s if v < 0 else s


def paren(v):
    return '(%s)' % tex_num(v) if F(v) < 0 else tex_num(v)


NUM = r'-?(?:\\frac\{\d+\}\{\d+\}|\d+)'


def parse_num(s):
    s = s.strip()
    m = re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}', s)
    if m:
        return F(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1)
    return F(int(s))


def parse_xterm(s):
    """'x', '-x', '6x', '-4x', '\\frac{x}{4}', '-\\frac{x}{3}', '\\frac{2}{3}x' -> coefficient."""
    s = s.replace(' ', '')
    neg = s.startswith('-')
    t = s[1:] if neg else s
    if t == 'x':
        a = F(1)
    elif re.fullmatch(r'\d+x', t):
        a = F(int(t[:-1]))
    elif re.fullmatch(r'\\frac\{x\}\{\d+\}', t):
        a = F(1, int(re.search(r'\{(\d+)\}$', t).group(1)))
    elif re.fullmatch(r'\\frac\{\d+\}\{\d+\}x', t):
        p, q = re.findall(r'\d+', t)
        a = F(int(p), int(q))
    else:
        return None
    return -a if neg else a


def parse_side(s):
    """A side of a bank line -> ('const', c) or ('x', layers)."""
    s = s.strip()
    if re.fullmatch(NUM, s.replace(' ', '')):
        return ('const', parse_num(s))
    m = re.fullmatch(r'(\d+)\((x)\s*([+-])\s*(\d+)\)', s.replace(' ', ''))
    if m:
        b = F(int(m.group(4))) * (1 if m.group(3) == '+' else -1)
        return ('x', norm([('+', b), ('*', F(int(m.group(1))))]))
    m = re.fullmatch(r'\\frac\{x([+-])(\d+)\}\{(\d+)\}', s.replace(' ', ''))
    if m:
        b = F(int(m.group(2))) * (1 if m.group(1) == '+' else -1)
        return ('x', norm([('+', b), ('*', F(1, int(m.group(3))))]))
    a = parse_xterm(s)
    if a is not None:
        return ('x', norm([('*', a)]))
    # x-term +/- constant, or constant +/- x-term (top-level + or - between terms)
    parts = re.split(r'\s([+-])\s', s)
    if len(parts) == 3:
        left, sign, right = parts
        sg = 1 if sign == '+' else -1
        a = parse_xterm(left)
        if a is not None:
            return ('x', norm([('*', a), ('+', sg * parse_num(right))]))
        a = parse_xterm(right)
        if a is not None:
            return ('x', norm([('*', sg * a), ('+', parse_num(left))]))
    raise ValueError('cannot read side %r' % s)


def parse_line(t):
    lhs, rhs = t.split('=')
    a, b = parse_side(lhs), parse_side(rhs)
    if a[0] == 'x' and b[0] == 'const':
        return State(tuple(a[1]), b[1], 'L')
    if b[0] == 'x' and a[0] == 'const':
        return State(tuple(b[1]), a[1], 'R')
    raise ValueError('cannot read line %r' % t)


# ------------------------------------------------------------------ layers
def norm(layers):
    out = []
    for kind, v in layers:
        v = F(v)
        if out and out[-1][0] == kind:
            prev = out.pop()
            v = prev[1] + v if kind == '+' else prev[1] * v
        if (kind == '+' and v == 0) or (kind == '*' and v == 1):
            continue
        out.append((kind, v))
    # merging can expose a new neighbour pair or identity; repeat until stable
    return out if out == list(layers) else norm(out)


def mul(layers, k):
    layers = list(layers)
    if not layers:
        return [('*', F(k))]
    kind, v = layers[-1]
    if kind == '*':
        return layers[:-1] + [('*', v * k)]
    return mul(layers[:-1], k) + [('+', v * k)]


class State:
    __slots__ = ('L', 'c', 'side')

    def __init__(self, layers, c, side):
        self.L, self.c, self.side = tuple(norm(layers)), F(c), side

    def key(self):
        return (self.L, self.c, self.side)

    def __eq__(self, o):
        return self.key() == o.key()

    def __hash__(self):
        return hash(self.key())

    def solved(self):
        return not self.L

    def value(self):
        v = self.c
        for kind, k in reversed(self.L):
            v = v - k if kind == '+' else v / k
        return v

    def fractional(self):
        return self.c.denominator != 1 or any(kind == '+' and v.denominator != 1 for kind, v in self.L)

    def numbers(self):
        out = {F(1)}
        for v in [k for _, k in self.L] + [self.c]:
            if v == 0:
                continue
            v = abs(v)
            out |= {v, F(v.numerator), F(v.denominator), 1 / v}
        return out


def apply(st, mv):
    op, k = mv
    if op == '+':
        return State(list(st.L) + [('+', k)], st.c + k, st.side)
    if op == '-':
        return State(list(st.L) + [('+', -k)], st.c - k, st.side)
    if op == '*':
        return State(mul(st.L, k), st.c * k, st.side)
    return State(mul(st.L, 1 / k), st.c / k, st.side)


def candidates(st):
    out = []
    for w in sorted(st.numbers()):
        out += [('+', w), ('-', w)]
        for s in (w, -w):
            if s != 1:
                out += [('*', s), ('/', s)]
    return out


# ------------------------------------------------------------------ the search
_memo = {}


def best(st, depth):
    """Cheapest (moves, fractions) route from st to solved within depth moves, or None."""
    if st.solved():
        return (0, False)
    if depth == 0:
        return None
    key = (st, depth)
    if key in _memo:
        return _memo[key]
    found = None
    for mv in candidates(st):
        nxt = apply(st, mv)
        rest = best(nxt, depth - 1)
        if rest is None:
            continue
        cost = (1 + rest[0], (nxt.fractional() and not nxt.solved()) or rest[1])
        if found is None or cost < found:
            found = cost
    _memo[key] = found
    return found


def cheapest(st):
    """Iterative deepening: the first depth with a route is the fewest moves, so deeper routes are never searched."""
    for d in range(DEPTH + 1):
        found = best(st, d)
        if found is not None:
            return found
    return None


def classify(st):
    """-> (dist, {next_state: [moves]} for optimal, same for slower)."""
    here = cheapest(st)
    if here is None:
        raise ValueError('no route within %d moves from %r' % (DEPTH, st.key()))
    opt, slow = {}, {}
    for mv in candidates(st):
        nxt = apply(st, mv)
        rest = best(nxt, here[0] - 1)
        if rest is None:
            continue
        cost = (1 + rest[0], (nxt.fractional() and not nxt.solved()) or rest[1])
        if cost == here:
            opt.setdefault(nxt, []).append(mv)
        elif cost[0] == here[0]:
            slow.setdefault(nxt, []).append(mv)
    return here, opt, slow


# ------------------------------------------------------------------ display
def coef_tex(a):
    a = F(a)
    if a == 1:
        return 'x'
    if a == -1:
        return '-x'
    if a.denominator == 1:
        return '%dx' % a.numerator
    if abs(a.numerator) == 1:
        return ('-' if a < 0 else '') + r'\frac{x}{%d}' % a.denominator
    return tex_num(a) + 'x'


def xside_tex(L):
    L = list(L)
    if not L:
        return 'x'
    if len(L) == 1 and L[0][0] == '*':
        return coef_tex(L[0][1])
    if L[-1][0] == '+':
        inner = xside_tex(L[:-1])
        b = L[-1][1]
        return '%s %s %s' % (inner, '+' if b > 0 else '-', tex_num(abs(b)))
    inner, a = xside_tex(L[:-1]), L[-1][1]
    if a.denominator == 1:
        return '%s(%s)' % (('-' if a == -1 else tex_num(a)), inner)
    if abs(a.numerator) == 1:
        return ('-' if a < 0 else '') + r'\frac{%s}{%d}' % (inner, a.denominator)
    return r'%s(%s)' % (tex_num(a), inner)


def line_tex(st, other=None):
    o = tex_num(st.c) if other is None else other
    x = xside_tex(st.L)
    return '%s = %s' % (x, o) if st.side == 'L' else '%s = %s' % (o, x)


def op_tex(mv):
    op, k = mv
    if op in '+-':
        return '%s\\,%s' % (op, tex_num(k))
    sym = r'\times' if op == '*' else r'\div'
    return '%s\\,%s' % (sym, paren(k))


def parse_op(t):
    t = t.replace(' ', '')
    m = re.fullmatch(r'([+-])\\,(.+)', t)
    if m:
        return (m.group(1), parse_num(m.group(2)))
    m = re.fullmatch(r'\\(times|div)\\,\(?(.+?)\)?', t)
    if m:
        return ('*' if m.group(1) == 'times' else '/', parse_num(m.group(2)))
    raise ValueError('cannot read move %r' % t)


def worked(c, mv):
    """The number side after mv, written out (unevaluated)."""
    op, k = mv
    if op == '+':
        return '%s + %s' % (tex_num(c), tex_num(k))
    if op == '-':
        return '%s - %s' % (tex_num(c), tex_num(k))
    if op == '*':
        return r'%s \times %s' % (tex_num(c), paren(k))
    if k.denominator == 1 and k > 0 and c.denominator == 1:
        return (r'\frac{%d}{%d}' if c >= 0 else r'-\frac{%d}{%d}') % (abs(c.numerator), k.numerator)
    return r'%s \div %s' % (tex_num(c), paren(k))


def says_full(mv):
    op, k = mv
    if op == '+':
        return r'add \(%s\) to both sides' % tex_num(k)
    if op == '-':
        return r'subtract \(%s\) from both sides' % tex_num(k)
    return r'%s both sides by \(%s\)' % ('multiply' if op == '*' else 'divide', tex_num(k))


def tidy(t):
    return re.sub(r'\s+', '', t)


# ------------------------------------------------------------------ errors
INVERT = {'+': '-', '-': '+', '*': '/', '/': '*'}


def error_options(st, mv, nxt):
    """Named invalid lines for a base move. Each: (kind, show, wrong-solution line state)."""
    out = []
    op, k = mv
    xs = xside_tex(st.L)
    # one side only: the x side, then the number side
    out.append(('one-side', line_tex(nxt, tex_num(st.c)), State(nxt.L, st.c, st.side), 'x'))
    out.append(('one-side', ('%s = %s' % (xs, worked(st.c, mv))) if st.side == 'L'
                else '%s = %s' % (worked(st.c, mv), xs), State(st.L, apply(st, mv).c, st.side), 'num'))
    # carried across unchanged: the move removes the outer layer, the number side gets that layer's own operation
    if st.L and len(nxt.L) == len(st.L) - 1 and tuple(nxt.L) == st.L[:-1]:
        wrong = (INVERT[op], k)
        out.append(('carry', line_tex(nxt, worked(st.c, wrong)), State(nxt.L, apply(State((), st.c, 'L'), wrong).c,
                                                                         st.side), None))
    # a multiplying move on (a x + b): only the x-term, or the x-term and the number side but not the constant
    if op in '*/' and len(st.L) == 2 and st.L[0][0] == '*' and st.L[1][0] == '+':
        kk = k if op == '*' else 1 / k
        a, b = st.L[0][1], st.L[1][1]
        if a * kk == 1:
            only = State([('+', b)], st.c, st.side)
            out.append(('xonly', line_tex(only), only, None))
            cn = State([('+', b)], st.c * kk, st.side)
            out.append(('constnot', line_tex(cn, worked(st.c, mv)), cn, None))
    return out


def error_fields(kind, which, st, mv):
    """What the page needs to word an error's feedback (the wording itself is the page's, ERR_TEXT): the code, and
    for xonly/constnot the constant left alone and whether the move divides or multiplies."""
    if kind == 'one-side':
        return ['x' if which == 'x' else 'n']
    if kind == 'carry':
        return ['c']
    op, k = mv
    verb = 'd' if op == '/' or (op == '*' and abs(k.numerator) == 1 and k.denominator != 1) else 'm'
    return ['o' if kind == 'xonly' else 'k', tex_num(abs(st.L[1][1])), verb]


def pack(o):
    """An option as the page holds it: [move, line, 'b' | 's', next line (-1: x is alone)] or
    [move, line, 'e', error code, ...]. The keyed (or first optimal) option is always first."""
    if o['cls'] == 'err':
        return [o['op'], o['show'], 'e'] + o['fields']
    return [o['op'], o['show'], 'b' if o['cls'] == 'best' else 's', o['to']]


def by_tex(a):
    """'multiplied by 6' or, for a coefficient 1/n, 'divided by n'."""
    a = F(a)
    if abs(a.numerator) == 1 and a.denominator != 1:
        return r'divided by \(%s\)' % tex_num(1 / a)
    return r'multiplied by \(%s\)' % tex_num(a)


def hint_text(st, mv):
    op, k = mv
    if op in '+-':
        b = k if op == '-' else -k        # the constant this move clears
        what = (r'\(%s\) is added on the x side' % tex_num(b)) if b > 0 else (
            r'\(%s\) is taken away on the x side' % tex_num(-b))
        return what[0].upper() + what[1:] + ': ' + says_full(mv) + '.'
    if len(st.L) == 1:
        a = st.L[0][1]
        if a == -1:
            return r'You have \(-x\), not \(x\): %s.' % says_full(mv)
        return r'x is %s: %s to undo it.' % (by_tex(a), says_full(mv))
    if st.L[-1][0] == '*':
        return r'The whole of \(%s\) is %s: %s.' % (xside_tex(st.L[:-1]), by_tex(st.L[-1][1]), says_full(mv))
    a = st.L[0][1]
    if a == -1:
        return r'Multiplying both sides by \(-1\) turns \(-x\) into \(x\) in one move.'
    return r'%s: \(%s\) becomes x, and every other term is %s too.' % (
        says_full(mv)[0].upper() + says_full(mv)[1:], coef_tex(a), 'multiplied' if op == '*' else 'divided')


# ------------------------------------------------------------------ building one question
def prefer(moves, keyed=None):
    """One move per resulting line: the keyed move; else a whole-number operand; then - and +; then / before x,
    except for -1 and a fraction, where x is the usual way to write it (x(-1), x 3/2)."""
    if keyed in moves:
        return keyed

    def rank(m):
        op, k = m
        times_first = abs(k) == 1 or k.denominator != 1
        order = {'-': 0, '+': 1, '*': 2 if times_first else 3, '/': 3 if times_first else 2}[op]
        return (k.denominator != 1, order, abs(k))
    return sorted(moves, key=rank)[0]


def rot(seq, n):
    n %= len(seq)
    return seq[n:] + seq[:n]


def build(q, qi, report):
    keyed_route = [parse_op(o['correct']) for o in q['ops']]
    bank_lines = [o.get('line') for o in q['ops']]
    start = parse_line(q['eq'])
    v = start.value()
    states, index, routes = [], {}, []
    bank_at = {start: 0}            # a state on the keyed route -> how many keyed moves made
    st = start
    for i, mv in enumerate(keyed_route):
        st = apply(st, mv)
        if i + 1 < len(keyed_route):
            want = parse_line(bank_lines[i])
            if want != st:
                raise ValueError('%s: keyed move %d gives %s, the bank says %s' % (q['id'], i + 1, line_tex(st),
                                                                                    bank_lines[i]))
            bank_at[st] = i + 1
    if not st.solved() or st.value() != v:
        raise ValueError('%s: the keyed route does not solve the equation' % q['id'])

    def visit(st, tex):
        if st in index:
            return index[st]
        index[st] = len(states)
        rec = {}
        states.append(rec)
        here, opt, slow = classify(st)
        key_mv = keyed_route[bank_at[st]] if st in bank_at else None
        if key_mv is not None:
            hit = [n for n, ms in opt.items() if key_mv in ms]
            if not hit:
                report['stop'].append('%s: the keyed move %s at %s is not optimal (optimal: %s)' % (
                    q['id'], op_tex(key_mv), tex, ', '.join(op_tex(prefer(ms)) for ms in opt.values())))
        # one option per distinct line; the keyed (or first) optimal line first
        opt_items = sorted(opt.items(), key=lambda it: (key_mv not in it[1], tidy(line_tex(it[0]))))
        best_moves = [prefer(ms, key_mv) for _, ms in opt_items]
        slow_items = sorted(slow.items(), key=lambda it: tidy(line_tex(it[0])))
        n_slow = 1 if slow_items else 0
        n_opt = min(len(opt_items), 4 - n_slow - 1)
        opts, seen = [], set()
        for j, (nxt, ms) in enumerate(opt_items[:n_opt]):
            mv = best_moves[j]
            opts.append({'op': op_tex(mv), 'show': line_tex(nxt, worked(st.c, mv)), 'cls': 'best', '_nxt': nxt, '_mv': mv, 'key': j == 0})
        for nxt, ms in slow_items[:n_slow]:
            mv = prefer(ms)
            opts.append({'op': op_tex(mv), 'show': line_tex(nxt, worked(st.c, mv)), 'cls': 'slow', '_nxt': nxt,
                         '_mv': mv})
        for o in opts:
            seen.add(tidy(o['show']))
            seen.add(o['_nxt'])
        # errors, from the keyed/first optimal move, then the others, then the slower move
        bases = [(o['_mv'], o['_nxt']) for o in opts]
        cands = []
        for mv, nxt in bases:
            for kind, show, wst, which in error_options(st, mv, nxt):
                cands.append((kind, show, wst, which, mv))
        order = rot(['carry', 'constnot', 'one-side', 'xonly'], qi + len(states))
        cands.sort(key=lambda c: order.index(c[0]))
        for kind, show, wst, which, mv in cands:
            if len(opts) >= 4:
                break
            if tidy(show) in seen or wst in seen or wst.value() == v:
                continue
            seen.add(tidy(show))
            seen.add(wst)
            opts.append({'op': op_tex(mv), 'show': show, 'cls': 'err', 'err': kind,
                         'fields': error_fields(kind, which, st, mv)})
        if not any(o['cls'] == 'err' for o in opts):
            raise ValueError('%s: no genuine error for %s' % (q['id'], tex))
        if len(opts) < 4:
            report['short'].append('%s at %s: %d options' % (q['id'], tex, len(opts)))
        hint = hint_text(st, best_moves[0])
        if len(best_moves) > 1:
            hint += ' Or: ' + hint_text(st, best_moves[1])[0].lower() + hint_text(st, best_moves[1])[1:]
        rec.update({'eq': tex, 'hint': hint, 'o': opts})
        for o in opts:
            if o['cls'] == 'err':
                continue
            nxt = o.pop('_nxt')
            o.pop('_mv')
            if nxt.solved():
                o['to'] = -1
            else:
                ntex = bank_lines[bank_at[nxt] - 1] if nxt in bank_at else line_tex(nxt)
                o['to'] = visit(nxt, ntex)
        return index[st]

    visit(start, q['eq'])

    # every tied optimal route from the start, as (move, line) pairs
    def walk(st, path):
        if st.solved():
            routes.append(path)
            return
        _, opt, _ = classify(st)
        key_mv = keyed_route[bank_at[st]] if st in bank_at else None
        for nxt, ms in sorted(opt.items(), key=lambda it: tidy(line_tex(it[0]))):
            line = (bank_lines[bank_at[nxt] - 1] if nxt in bank_at else line_tex(nxt)) if not nxt.solved() \
                else 'x = ' + tex_num(v)
            walk(nxt, path + [[op_tex(prefer(ms, key_mv)), line]])
    walk(start, [])
    keyed = [[o['correct'], o.get('line') or 'x = ' + tex_num(v)] for o in q['ops']]
    routes.sort(key=lambda r: r != keyed)
    if [tidy(a) + '|' + tidy(b) for a, b in routes[0]] != [tidy(a) + '|' + tidy(b) for a, b in keyed]:
        report['stop'].append('%s: the keyed route is not among the optimal routes' % q['id'])
    for o in (o for s in states for o in s['o']):
        report['count'][o.get('err', o['cls'])] = report['count'].get(o.get('err', o['cls']), 0) + 1
    report['routes'] += len(routes) > 1
    return {'s': [[s['eq'], s['hint'], [pack(o) for o in s['o']]] for s in states], 'r': routes}


def generate(html):
    report = {'stop': [], 'short': [], 'count': {}, 'routes': 0}
    bank = read_bank(html)
    moves = {}
    for qi, q in enumerate(bank):
        moves[q['id']] = build(q, qi, report)
    return bank, moves, report


def emit(moves):
    rows = ['  %s: %s' % (json.dumps(k), json.dumps(v, ensure_ascii=False, separators=(',', ':')))
            for k, v in moves.items()]
    return 'const MOVES = {\n' + ',\n'.join(rows) + '\n};'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--page', default=GAME)
    args = ap.parse_args()
    html = open(args.page, encoding='utf-8').read()
    bank, moves, report = generate(html)
    block = emit(moves)
    n_states = sum(len(m['s']) for m in moves.values())
    n_opts = sum(len(s[2]) for m in moves.values() for s in m['s'])
    print('questions %d, lines %d, options %d: %s; MOVES %d bytes' % (
        len(bank), n_states, n_opts, ', '.join('%s %d' % kv for kv in sorted(report['count'].items())), len(block)))
    print('questions with more than one optimal route: %d' % report['routes'])
    for s in report['short']:
        print('  short (no fourth honest option): ' + s)
    for s in report['stop']:
        print('STOP  ' + s)
    if report['stop']:
        return 1
    if START in html:
        i, j = html.index(START), html.index(END)
        current = html[i + len(START) + 1:j].rstrip('\n')
    else:
        current = None
    if args.check:
        if current != block:
            print('FAIL  the page\'s MOVES block differs from what gen-linear-moves.py writes (run --write)')
            return 1
        print('PASS  the page matches the generator')
    if args.write:
        if current is None:
            raise SystemExit('no GENERATED MOVES markers in the page')
        html = html[:i + len(START)] + '\n' + block + '\n' + html[j:]
        with open(args.page, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print('written to %s' % args.page)
    return 0


if __name__ == '__main__':
    sys.exit(main())
