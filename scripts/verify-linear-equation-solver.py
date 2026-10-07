#!/usr/bin/env python3
# ci-line: E | Linear Equation Solver (every move's class re-derived with SymPy, every option clicked in Chromium) |
"""Linear Equation Solver: every move's class re-derived with SymPy, every option clicked in Chromium.

Jon's design of 7 Oct 2026: the game asks "What is the optimal move here?" at each line of the working. An optimal
move (one that starts a route to x = value in the fewest moves, ties broken by keeping fractions out of every
intermediate line; every move still tied is optimal) scores full; a valid but slower move scores amber (half the points
at stake, streak kept); a wrong option is a genuine invalid error, named in the feedback. SR-13 stands: no valid move
is ever marked wrong. The tranche 4 audit (6 Oct) found every valid alternative move marked wrong against one keyed move
(t4-001; r-001 and r-002 are its two halves), and 11 hints showing raw TeX (t4-002).

This script holds the page's MOVES (written by gen-linear-moves.py) to its own reading, built independently: its own
TeX parser, its own search, SymPy for every value and solution set.

Bank. Every equation is solved by its keyed answer; every keyed line has the same solution; the answer options are
  distinct in value (SR-4); the worked solution ends on the answer.
Lines and moves. A line's x-side is read into a tree (a bracket stays a bracket; x k distributes over a sum, as a
  student writes it). The candidate moves at a line are + k, - k, x k and / k for every number written in it (with
  its numerator, denominator and reciprocal, and 1; x and / both signed). The search finds the cheapest route to x
  alone (moves, then fractional constants in any intermediate line) by iterative deepening to depth 3.
  - every option marked 'best' starts a cheapest route; every 'slow' option is one move closer but loses the
    fraction tie-break; no option is a valid move that is neither (legal but useless moves are not offered);
  - every distinct optimal line is offered (up to the four-option limit), and a slower move is offered wherever one
    exists; at least one error; four options, except where four honest ones do not exist (SHORT);
  - a valid option's line is its move applied to both sides (SymPy), and the line it leads to is that line evaluated;
  - every error gives a different solution from its line (so no valid move is red) and is the error it is named:
    one-side, carry, xonly or constnot, reproduced from the option's own move;
  - following the keyed option from the question's equation gives the bank's keyed moves and lines; the routes the
    worked solution names are exactly the optimal routes, the keyed one first;
  - every hint names an optimal move; every slower or wrong option's feedback names exactly the optimal moves, and a
    slower option's feedback quotes the line it leads to.
Chromium (390x844, touch). Every option of every line is clicked through the page's own handler: an optimal move is
  marked right at no cost, a slower move amber at 12.5 points with feedback and Next, an error wrong at 25 with its
  named feedback and Next; the trail shows the line the student's own move gave (after an error, the keyed move's).
  Every hint, option and feedback is read as shown: no raw TeX, no sideways scroll. Then Jon's four cases are played
  by tapping: -7 on x + 7 = 12 full (100), x2 on x/2 + 5 = 11 full (100), /3 on 3x + 7 = 22 amber (88, streak kept),
  the carry-across slip on x + 7 = 12 red (75, worked solution).
Generator. The page's MOVES is exactly what scripts/gen-linear-moves.py writes from the page's own bank.

A self-test plants the old single-key marking (only the keyed move counts) and a mislabelled error (the slower /3 on
3x + 7 = 22 offered as an error); each must FAIL. Run against main's page (--against), it fails naming t4-001, r-001,
r-002 and t4-002.

    python scripts/verify-linear-equation-solver.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'linear-equation-solver'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
X = sp.Symbol('x')
R = sp.Rational
DEPTH = 3
# Lines where four honest options do not exist: -x = c has one optimal line (x(-1) and /(-1) give the same line), no
# slower move, and two errors (either side alone); carrying it across gives the same line as the x side alone.
SHORT = re.compile(r'^-x = -?\d+$')
ID = 'linear-equation-solver-'


# ------------------------------------------------------------------ reading TeX
def tokens(t):
    t = t.replace(r'\,', ' ').replace(r'\left', '').replace(r'\right', '')
    out, i = [], 0
    while i < len(t):
        c = t[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < len(t) and t[j].isdigit():
                j += 1
            out.append(('n', R(int(t[i:j]))))
            i = j
        elif c in 'x+-(){}=':
            out.append((c, None))
            i += 1
        elif t.startswith(r'\times', i):
            out.append(('*', None))
            i += 6
        elif t.startswith(r'\div', i):
            out.append(('/', None))
            i += 4
        elif t.startswith(r'\frac', i):
            out.append(('frac', None))
            i += 5
        else:
            raise ValueError('cannot read %r in %r' % (t[i:], t))
    return out


class P:
    """Recursive descent over a TeX line or side -> tree: ('num', q) | ('x',) | ('add', [t]) | ('mul', q, t)."""

    def __init__(self, t):
        self.t, self.i = tokens(t), 0

    def peek(self):
        return self.t[self.i][0] if self.i < len(self.t) else None

    def take(self, k):
        if self.peek() != k:
            raise ValueError('expected %s at %d' % (k, self.i))
        self.i += 1

    def expr(self):
        terms = [self.term()]
        while self.peek() in ('+', '-'):
            sign = self.peek()
            self.i += 1
            t = self.term()
            terms.append(t if sign == '+' else mul(t, -1))
        return add(terms)

    def term(self):
        t = self.unary()
        while True:
            k = self.peek()
            if k in ('*', '/'):
                self.i += 1
                u = self.unary()
                if u[0] != 'num':
                    raise ValueError('x and / only by numbers')
                t = mul(t, u[1] if k == '*' else 1 / u[1])
            elif k in ('x', '(', 'frac') and t[0] == 'num':      # implicit: 3x, 2(x + 3), \frac{2}{3}x
                u = self.unary()
                t = bracket(u, t[1])
            else:
                return t

    def unary(self):
        if self.peek() == '-':
            self.i += 1
            return mul(self.unary(), -1)
        return self.atom()

    def atom(self):
        k = self.peek()
        if k == 'n':
            v = self.t[self.i][1]
            self.i += 1
            return ('num', v)
        if k == 'x':
            self.i += 1
            return ('x',)
        if k == '(':
            self.i += 1
            e = self.expr()
            self.take(')')
            return e
        if k == 'frac':
            self.i += 1
            self.take('{')
            a = self.expr()
            self.take('}')
            self.take('{')
            b = self.expr()
            self.take('}')
            if b[0] != 'num':
                raise ValueError('a denominator must be a number')
            return bracket(a, 1 / b[1])
        raise ValueError('unexpected %r' % k)

    def done(self):
        if self.i != len(self.t):
            raise ValueError('trailing tokens')


def side(t):
    p = P(t)
    e = p.expr()
    p.done()
    return e


def line(t):
    a, b = t.split('=')
    return side(a), side(b)


# ------------------------------------------------------------------ trees
def add(terms):
    flat = []
    for t in terms:
        flat += t[1] if t[0] == 'add' else [t]
    nums = sum((t[1] for t in flat if t[0] == 'num'), R(0))
    rest = [t for t in flat if t[0] != 'num']
    out = rest + ([('num', nums)] if nums != 0 or not rest else [])
    return out[0] if len(out) == 1 else ('add', out)


def mul(t, k):
    k = R(k)
    if t[0] == 'num':
        return ('num', t[1] * k)
    if t[0] == 'x':
        return t if k == 1 else ('mul', k, t)
    if t[0] == 'mul':
        c = t[1] * k
        return t[2] if c == 1 else ('mul', c, t[2])
    return add([mul(u, k) for u in t[1]])


def bracket(t, k):
    """A number times a sum as written, 2(x + 3) or (x + 4)/3: the bracket stays (a move's x k distributes; reading
    a line never does)."""
    return ('mul', R(k), t) if t[0] == 'add' else mul(t, k)


def sym(t):
    if t[0] == 'num':
        return t[1]
    if t[0] == 'x':
        return X
    if t[0] == 'mul':
        return t[1] * sym(t[2])
    return sp.Add(*[sym(u) for u in t[1]])


def has_x(t):
    return t[0] == 'x' or (t[0] == 'mul' and has_x(t[2])) or (t[0] == 'add' and any(has_x(u) for u in t[1]))


class Line:
    def __init__(self, a, b):
        if has_x(a) == has_x(b):
            raise ValueError('x must be on exactly one side')
        self.side = 'L' if has_x(a) else 'R'
        self.xs, self.c = (a, b) if self.side == 'L' else (b, a)
        if self.c[0] != 'num':
            raise ValueError('the number side must be a number')
        # x = 5 and 5 = x are the same solved line
        self.key = (repr(self.xs), self.c[1], 'L' if self.xs == ('x',) else self.side)

    @staticmethod
    def of(t):
        return Line(*line(t))

    def solved(self):
        return self.xs == ('x',)

    def value(self):
        return sp.solve(sp.Eq(sym(self.xs), self.c[1]), X)

    def fractional(self):
        out = [self.c[1]]

        def walk(t):
            if t[0] == 'add':
                out.extend(u[1] for u in t[1] if u[0] == 'num')
                for u in t[1]:
                    walk(u)
            elif t[0] == 'mul':
                walk(t[2])
        walk(self.xs)
        return any(v.q != 1 for v in out)

    def numbers(self):
        vals = [self.c[1]]

        def walk(t):
            if t[0] == 'num':
                vals.append(t[1])
            elif t[0] == 'mul':
                vals.append(t[1])
                walk(t[2])
            elif t[0] == 'add':
                for u in t[1]:
                    walk(u)
        walk(self.xs)
        out = {R(1)}
        for v in vals:
            if v != 0:
                v = abs(v)
                out |= {v, R(v.p), R(v.q), 1 / v}
        return out

    def move(self, mv):
        op, k = mv
        if op in '+-':
            k = k if op == '+' else -k
            a, b = add([self.xs, ('num', k)]), ('num', self.c[1] + k)
        else:
            k = k if op == '*' else 1 / k
            a, b = mul(self.xs, k), ('num', self.c[1] * k)
        return Line(a, b) if self.side == 'L' else Line(b, a)


def candidates(ln):
    out = []
    for w in ln.numbers():
        out += [('+', w), ('-', w)]
        for s in (w, -w):
            if s != 1:
                out += [('*', s), ('/', s)]
    return out


_memo = {}


def cost_within(ln, d):
    """Cheapest (moves, fractions) route of exactly the fewest moves <= d, or None."""
    if ln.solved():
        return (0, False)
    if d == 0:
        return None
    key = (ln.key, d)
    if key not in _memo:
        best = None
        for mv in candidates(ln):
            nx = ln.move(mv)
            rest = cost_within(nx, d - 1)
            if rest is not None:
                c = (1 + rest[0], (nx.fractional() and not nx.solved()) or rest[1])
                best = c if best is None or c < best else best
        _memo[key] = best
    return _memo[key]


def cost(ln):
    for d in range(DEPTH + 1):       # iterative deepening: the first depth with a route is the fewest moves
        c = cost_within(ln, d)
        if c is not None:
            return c
    return None


def classify(ln):
    """-> (cost, {line key: (Line, [moves])} optimal, same for slower)."""
    here = cost(ln)
    opt, slow = {}, {}
    for mv in candidates(ln):
        nx = ln.move(mv)
        rest = cost_within(nx, here[0] - 1)
        if rest is None:
            continue
        c = (1 + rest[0], (nx.fractional() and not nx.solved()) or rest[1])
        bucket = opt if c == here else slow if c[0] == here[0] else None
        if bucket is not None:
            bucket.setdefault(nx.key, (nx, []))[1].append(mv)
    return here, opt, slow


def read_op(t):
    t = t.replace(' ', '')
    m = re.fullmatch(r'([+-])\\,(.+)', t)
    if m:
        v = side(m.group(2))
        return (m.group(1), v[1])
    m = re.fullmatch(r'\\(times|div)\\,(.+)', t)
    if m:
        v = side(m.group(2))
        return ('*' if m.group(1) == 'times' else '/', v[1])
    raise ValueError('cannot read move %r' % t)


def apply_sym(e, mv):
    op, k = mv
    return {'+': e + k, '-': e - k, '*': e * k, '/': e / k}[op]


INV = {'+': '-', '-': '+', '*': '/', '/': '*'}


def eq(a, b):
    return sp.simplify(a - b) == 0


# ------------------------------------------------------------------ the static checks
def check_bank(fails, bank):
    for q in bank:
        qid = q['id']
        try:
            ln = Line.of(q['eq'])
            v = Line.of(q['ans']['correct']).value()
            if ln.value() != v:
                fails.append('%s: %s is not solved by %s' % (qid, q['eq'], q['ans']['correct']))
            for o in q['ops']:
                if o.get('line') and Line.of(o['line']).value() != v:
                    fails.append('%s: the keyed line %s does not have the same solution' % (qid, o['line']))
            vals = [tuple(Line.of(a).value()) for a in q['ans']['opts']]
            if len(set(vals)) != len(vals) or q['ans']['correct'] not in q['ans']['opts']:
                fails.append('%s: answer options not distinct in value, or the answer missing (SR-4)' % qid)
            if re.sub(r'\s', '', q['sol'][-1]) != re.sub(r'\s', '', q['ans']['correct']):
                fails.append('%s: the worked solution does not end on the answer' % qid)
        except ValueError as e:
            fails.append('%s: %s' % (qid, e))


KINDS = {'x': 'one-side', 'n': 'one-side', 'c': 'carry', 'o': 'xonly', 'k': 'constnot'}


def expand(moves):
    """The page's compact MOVES -> {qid: {'s': [{'eq', 'hint', 'o': [option]}], 'routes'}}. A line is [eq, hint,
    options]; an option is [move, line, 'b' | 's', next] or [move, line, 'e', code, constant, 'd' | 'm']; the first
    option is the keyed one."""
    out = {}
    for qid, m in moves.items():
        states = []
        for eq_, hint, opts in m['s']:
            os_ = []
            for n, a in enumerate(opts):
                o = {'op': a[0], 'show': a[1], 'key': n == 0,
                     'cls': {'b': 'best', 's': 'slow', 'e': 'err'}.get(a[2], a[2])}
                if a[2] == 'e':
                    o.update({'err': KINDS.get(a[3], a[3]), 'code': a[3], 'args': a[4:]})
                else:
                    o['to'] = a[3]
                os_.append(o)
            states.append({'eq': eq_, 'hint': hint, 'o': os_})
        out[qid] = {'s': states, 'routes': m['r']}
    return out


def check_moves(fails, bank, moves):
    stats = {'lines': 0, 'options': 0, 'best': 0, 'slow': 0, 'err': 0}
    for q in bank:
        qid = q['id']
        m = moves.get(qid)
        if not m:
            fails.append('%s: no options in MOVES' % qid)
            continue
        try:
            check_question(fails, q, m, stats)
        except (ValueError, KeyError, IndexError, TypeError) as e:
            fails.append('%s: cannot be checked: %s' % (qid, e))
    return stats


def tag(cls):
    return ' (%sr-001, %st4-001)' % (ID, ID) if cls == 'best' else ' (%sr-002, %st4-001)' % (ID, ID)


def check_question(fails, q, m, stats):
    qid = q['id']
    states = m['s']
    if states[0]['eq'] != q['eq']:
        fails.append("%s: MOVES starts at %s, not the question's %s" % (qid, states[0]['eq'], q['eq']))
    v = Line.of(q['ans']['correct']).value()
    for si, st in enumerate(states):
        stats['lines'] += 1
        where = '%s at %s' % (qid, st['eq'])
        ln = Line.of(st['eq'])
        if ln.value() != v:
            fails.append('%s: this line does not have the answer %s' % (where, q['ans']['correct']))
        here, opt, slow = classify(ln)
        opts = st['o']
        stats['options'] += len(opts)
        shows = [o['show'] for o in opts]
        if len(set(shows)) != len(shows):
            fails.append('%s: two options show the same line' % where)
        best_ops = []
        offered = {}
        for o in opts:
            stats[o['cls']] = stats.get(o['cls'], 0) + 1
            mv = read_op(o['op'])
            a, b = line(o['show'])
            sl, sr = (sym(a), sym(b))
            orig_l, orig_r = (sym(ln.xs), ln.c[1]) if ln.side == 'L' else (ln.c[1], sym(ln.xs))
            if o['cls'] in ('best', 'slow'):
                if not (eq(sl, apply_sym(orig_l, mv)) and eq(sr, apply_sym(orig_r, mv))):
                    fails.append('%s: option %s is not %s done to both sides' % (where, o['show'], o['op']))
                nx = ln.move(mv)
                bucket = opt if o['cls'] == 'best' else slow
                if nx.key not in bucket:
                    real = 'optimal' if nx.key in opt else 'slower' if nx.key in slow else 'neither optimal nor slower'
                    fails.append('%s: %s is offered as %s but is %s%s' % (
                        where, o['op'], o['cls'], real, tag('best' if nx.key in opt else 'slow')))
                offered[nx.key] = o['cls']
                if o['cls'] == 'best':
                    best_ops.append(o['op'])
                if o['to'] == -1:
                    if not nx.solved():
                        fails.append('%s: %s ends the moves but x is not alone' % (where, o['op']))
                else:
                    tgt = Line.of(states[o['to']]['eq'])
                    if tgt.key != nx.key:
                        fails.append('%s: %s leads to %s, but the move gives %s' % (where, o['op'],
                                                                                    states[o['to']]['eq'], o['show']))
            else:
                # an error: a different solution (so no valid move is red), and the error it is named
                try:
                    wrong = sp.solve(sp.Eq(sl, sr), X)
                except Exception:
                    wrong = None
                if wrong == v:
                    fails.append('%s: %s is marked wrong but is a valid move (SR-13)%s' % (where, o['show'], tag('best')))
                xs_old, n_old = (orig_l, orig_r) if ln.side == 'L' else (orig_r, orig_l)
                xs_new, n_new = (sl, sr) if ln.side == 'L' else (sr, sl)
                kind = o.get('err')
                ok = False
                if kind == 'one-side':
                    ok = (eq(xs_new, apply_sym(xs_old, mv)) and eq(n_new, n_old)) or \
                         (eq(xs_new, xs_old) and eq(n_new, apply_sym(n_old, mv)))
                elif kind == 'carry':
                    ok = eq(xs_new, apply_sym(xs_old, mv)) and eq(n_new, apply_sym(n_old, (INV[mv[0]], mv[1])))
                elif kind in ('xonly', 'constnot') and mv[0] in '*/':
                    kk = mv[1] if mv[0] == '*' else 1 / mv[1]
                    a_ = sp.Poly(xs_old, X).coeff_monomial(X)
                    b_ = sp.Poly(xs_old, X).coeff_monomial(1)
                    ok = eq(xs_new, a_ * kk * X + b_) and b_ != 0 and \
                        eq(n_new, n_old if kind == 'xonly' else n_old * kk)
                    # the feedback's figures: the constant left alone, and whether the move divides or multiplies
                    divides = abs(kk.p) == 1 and kk.q != 1
                    if len(o['args']) != 2 or side(o['args'][0])[1] != abs(b_) or \
                            o['args'][1] != ('d' if divides else 'm'):
                        fails.append('%s: the error %s carries %s for its feedback; the constant is %s and the move %s'
                                     % (where, o['show'], o['args'], abs(b_), 'divides' if divides else 'multiplies'))
                if kind == 'one-side' and o['code'] != ('x' if eq(n_new, n_old) else 'n'):
                    ok = False
                if not ok:
                    fails.append('%s: the error %s is labelled %r but is not that error' % (where, o['show'], o['code']))
        # completeness: every distinct optimal line offered up to the limit; a slower move wherever one exists
        n_slow = 1 if slow else 0
        want_best = min(len(opt), 4 - n_slow - 1)
        if sum(1 for c in offered.values() if c == 'best') != want_best:
            fails.append('%s: %d optimal moves offered, %d distinct optimal lines exist' % (
                where, sum(1 for c in offered.values() if c == 'best'), len(opt)))
        if slow and 'slow' not in offered.values():
            fails.append('%s: a slower move exists but none is offered' % where)
        if not any(o['cls'] == 'err' for o in opts):
            fails.append('%s: no error offered' % where)
        if len(opts) != 4 and not (len(opts) == 3 and SHORT.match(st['eq'])):
            fails.append('%s: %d options' % (where, len(opts)))
        if sum(1 for o in opts if o.get('key')) != 1 or not next(o for o in opts if o.get('key'))['cls'] == 'best':
            fails.append('%s: not exactly one keyed option, or the keyed option is not optimal' % where)
        # the hint names an optimal move (the feedback is checked as shown, in the Chromium sweep)
        nums = set()
        for o in opts:
            if o['cls'] == 'best':
                nums.add(str(abs(read_op(o['op'])[1].p)))
        if not any(n in st['hint'] for n in nums):
            fails.append('%s: the hint names no optimal move' % where)
    # the keyed route, and the routes the worked solution names
    st, ln = states[0], Line.of(states[0]['eq'])
    for i, kop in enumerate(q['ops']):
        k = next(o for o in st['o'] if o.get('key'))
        if read_op(k['op']) != read_op(kop['correct']):
            fails.append('%s: the keyed option at %s is %s, the bank keys %s' % (qid, st['eq'], k['op'], kop['correct']))
        if kop.get('line'):
            if k['to'] < 0 or Line.of(states[k['to']]['eq']).key != Line.of(kop['line']).key:
                fails.append('%s: the keyed route leaves the bank line %s' % (qid, kop['line']))
                return
            st = states[k['to']]
        elif k['to'] != -1:
            fails.append('%s: the keyed route does not end where the bank does' % qid)
    routes = []

    def walk(ln, path):
        if ln.solved():
            routes.append(tuple(path))
            return
        _, opt, _ = classify(ln)
        for key, (nx, ms) in opt.items():
            walk(nx, path + [nx.key])
    walk(Line.of(q['eq']), [])
    page = []
    for r in m['routes']:
        page.append(tuple(Line.of(l_).key for _, l_ in r))
    if sorted(map(repr, routes)) != sorted(map(repr, page)):
        fails.append('%s: the worked solution names %d routes; %d optimal routes exist' % (qid, len(page), len(routes)))
    keyed = tuple(Line.of(o.get('line') or q['ans']['correct']).key for o in q['ops'])
    if page and page[0] != keyed:
        fails.append("%s: the worked solution's first route is not the keyed route" % qid)


# ------------------------------------------------------------------ Chromium
SWEEP_JS = r"""() => {
  const out = {marks: [], shown: [], wide: []};
  const vis = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(x => x.remove()); return c.textContent; };
  const tex = el => { const a = el && el.querySelectorAll('annotation'); return a && a.length ? a[a.length - 1].textContent : null; };
  const raw = s => /[\\^_{}]/.test(s);
  const realTimeout = window.setTimeout; window.setTimeout = () => 0;
  try {
    startGame();
    for (const q of QUESTIONS.gcse) {
      currentQ = q; moves = MOVES[q.id];
      // a line in MOVES is [equation, hint, options]; an option's [1] is the line it shows
      moves.s.forEach((st, si0) => {
        const eqt = st[0];
        // the hint, as shown
        si = si0; phase = 'op'; qPenalty = 0; renderPhase(); useHint();
        const h = vis(document.getElementById('hintPanel'));
        if (raw(h)) out.shown.push([q.id, eqt, 'hint', h]);
        if (document.documentElement.scrollWidth > innerWidth) out.wide.push([q.id, eqt, document.documentElement.scrollWidth]);
        st[2].forEach(a => {
          const show = a[1];
          si = si0; phase = 'op'; qPenalty = 0; qMissed = false;
          document.getElementById('workCard').innerHTML = '<div class="work-line" id="liveLine"></div>';
          renderPhase();
          const btn = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === show);
          if (!btn) { out.marks.push([q.id, eqt, show, 'not shown']); return; }
          const label = vis(btn);
          if (raw(label)) out.shown.push([q.id, eqt, 'option', label]);
          btn.click();
          const fb = document.getElementById('moveFb');
          const fbText = fb.classList.contains('show') ? vis(fb) : '';
          if (raw(fbText)) out.shown.push([q.id, eqt, 'feedback', fbText]);
          if (document.documentElement.scrollWidth > innerWidth) out.wide.push([q.id, eqt, document.documentElement.scrollWidth]);
          const lines = document.querySelectorAll('#workCard .work-line');
          out.marks.push([q.id, eqt, show, btn.classList.contains('correct') ? 'right' : btn.classList.contains('slow') ? 'amber' :
            btn.classList.contains('wrong') ? 'wrong' : 'unmarked', qPenalty, fbText,
            !!fb.querySelector('.maffs-next-wrap'), tex(lines[lines.length - 1]),
            [...fb.querySelectorAll('annotation')].map(x => x.textContent)]);
          if (window.MaffsNext) MaffsNext.clear(fb);
        });
      });
    }
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""

# main's page (before MOVES): every option of every phase, through its own handler, and every hint as shown
OLD_SWEEP_JS = r"""() => {
  const out = {marks: [], shown: []};
  const vis = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(x => x.remove()); return c.textContent; };
  const realTimeout = window.setTimeout; window.setTimeout = () => 0;
  try {
    startGame();
    for (const q of QUESTIONS.gcse) {
      currentQ = q;
      phases = q.ops.map((o, i) => ({type: 'op', i: i})).concat([{type: 'ans'}]);
      q.ops.forEach((op, i) => {
        phaseIdx = i; renderPhase(); useHint();
        const h = vis(document.getElementById('hintPanel'));
        if (/[\\^_{}]/.test(h)) out.shown.push([q.id, i, h]);
        (op.opts || []).forEach(v => {
          phaseIdx = i; renderPhase();
          const btn = [...document.querySelectorAll('.opt-btn')].find(b => b.dataset.val === v);
          btn.click();
          out.marks.push([q.id, i, v, btn.classList.contains('wrong') ? 'wrong' : 'right']);
        });
      });
    }
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""

KATEX_DIR = None


def page_context(pw, base, html):
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
    bc_page = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
    if KATEX_DIR:
        ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
            path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
    ctx.route(lambda url: bool(bc_page.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    return browser, ctx


def open_page(ctx, base, errors):
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
    return page


# Jon's four cases, tapped with the game's real timers: (question, the options' lines in order, the question's score,
# the streak after it, what it shows)
CASES = [
    ('A1', ['x = 12 - 7', 'x = 5'], 100, 1, 'the optimal move -7 on x + 7 = 12 scores full'),
    ('M1', ['x + 10 = 11 \\times 2', 'x = 22 - 10', 'x = 12'], 100, 1, 'x2 on x/2 + 5 = 11 scores full'),
    ('L1', ['x + \\frac{7}{3} = \\frac{22}{3}', 'x = \\frac{22}{3} - \\frac{7}{3}', 'x = 5'], 88, 1,
     '/3 on 3x + 7 = 22 scores amber (half the 25 at stake), streak kept'),
    ('A1', ['x = 12 + 7', 'x = 5'], 75, 0, 'the carry-across slip on x + 7 = 12 is marked wrong'),
]


def play_cases(fails, ctx, base):
    from playwright.sync_api import TimeoutError as PWTimeout
    errors = []
    for qid, taps, want, want_streak, what in CASES:
        page = open_page(ctx, base, errors)
        page.evaluate('id => { startGame(); pool = [QUESTIONS.gcse.find(q => q.id === id)]; loadQuestion(); }', qid)
        for val in taps:
            page.wait_for_function('v => [...document.querySelectorAll("#options .opt-btn")].some(b => b.dataset.val === v'
                                   ' && !b.classList.contains("disabled"))', arg=val, timeout=8000)
            target = page.locator('#options .opt-btn[data-val="%s"]' % val.replace('\\', '\\\\'))
            target.scroll_into_view_if_needed()
            target.tap()
            # an optimal move shows no Next (it moves on by itself); a slower or wrong one does, above the footer
            nxt = page.locator('#moveFb .maffs-next-wrap button')
            try:
                nxt.wait_for(state='visible', timeout=1500)
            except PWTimeout:
                continue
            box = nxt.bounding_box()
            if box['y'] + box['height'] > 844 - 40:
                fails.append('%s (%s): Next is below the fold at 390x844' % (qid, what))
            nxt.tap()
        sol = page.locator('#solution.show .next-btn')
        if want_streak == 0:
            sol.wait_for(state='visible', timeout=8000)
        else:
            page.wait_for_function('document.getElementById("streakVal").textContent !== "0"', timeout=8000)
        score = int(page.locator('#score').text_content())
        streak = int(page.locator('#streakVal').text_content())
        if score != want or streak != want_streak:
            fails.append('%s: %s: the page scored %d with streak %d, expected %d with streak %d (%st4-001)' % (
                qid, what, score, streak, want, want_streak, ID))
        page.close()
    if errors:
        fails.append('page errors while playing: %s' % '; '.join(errors[:3]))


def play(fails, html, cases=True):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser, ctx = page_context(pw, base, html)
            errors = []
            page = open_page(ctx, base, errors)
            has_moves = page.evaluate('typeof MOVES !== "undefined"')
            bank = page.evaluate('QUESTIONS.gcse')
            moves = page.evaluate('MOVES') if has_moves else None
            if not has_moves:
                old = page.evaluate(OLD_SWEEP_JS)
                for qid, i, h in old['shown']:
                    fails.append('%s step %d: the hint shows raw TeX: %r (%st4-002)' % (qid, i + 1, h[:60], ID))
                old_marks(fails, bank, old['marks'])
            else:
                res = page.evaluate(SWEEP_JS)
                sweep(fails, expand(moves), res)
                if cases:
                    play_cases(fails, ctx, base)
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank, moves
    finally:
        proc.terminate()
        proc.wait()


def old_marks(fails, bank, marks):
    """On a page with no MOVES: every option clicked; a valid move that makes progress and is marked wrong FAILS."""
    by = {q['id']: q for q in bank}
    for qid, i, val, mark in marks:
        if mark != 'wrong':
            continue
        q = by[qid]
        ln = Line.of(q['eq'])
        for k in range(i):
            ln = ln.move(read_op(q['ops'][k]['correct']))
        _, opt, slow = classify(ln)
        nx = ln.move(read_op(val))
        if nx.key in opt or nx.key in slow:
            fails.append('%s at %s: %s is %s but marked wrong%s' % (
                qid, q['eq'] if i == 0 else q['ops'][i - 1]['line'], val,
                'optimal' if nx.key in opt else 'a valid slower move', tag('best' if nx.key in opt else 'slow')))


PHRASE = {'slow': "it's slower", 'x': 'to the side with x only', 'n': 'to the number side only', 'c': 'across without',
          'o': 'only the x-term', 'k': 'but not the'}


def check_feedback(o, st, text, tex):
    """The feedback as shown: the words for its kind, and every figure in it (the maths segments, in order)
    recomputed; it ends by naming exactly the optimal moves. Returns what is wrong, or None."""
    ln = Line.of(st['eq'])
    mv = read_op(o['op'])
    code = 'slow' if o['cls'] == 'slow' else o['code']
    if PHRASE[code] not in text.replace('’', "'"):
        return 'does not say %r' % PHRASE[code]
    best = [b['op'] for b in st['o'] if b['cls'] == 'best']
    t = [re.sub(r'\s', '', x) for x in tex]
    if t[len(t) - len(best):] != [re.sub(r'\s', '', b) for b in best] or 'Quickest here' not in text:
        return 'does not end by naming the optimal moves %s' % best
    figs = tex[:len(tex) - len(best)]
    n_old = ln.c[1]
    if code == 'slow':
        ok = len(figs) == 1 and Line.of(figs[0]).key == ln.move(mv).key
    elif code in ('x', 'n'):
        ok = len(figs) == 1 and read_op(figs[0]) == mv
    elif code == 'c':
        if len(figs) != 3:
            return 'should name the number carried and the two number sides'
        named = side(figs[0])[1] if mv[0] in '+-' else None
        moved_ok = (named == mv[1]) if mv[0] in '+-' else read_op(figs[0]) == (INV[mv[0]], mv[1])
        ok = moved_ok and eq(sym(side(figs[1])), apply_sym(n_old, mv)) and \
            eq(sym(side(figs[2])), apply_sym(n_old, (INV[mv[0]], mv[1])))
    else:
        b_ = abs(sp.Poly(sym(ln.xs), X).coeff_monomial(1))
        ok = side(figs[0])[1] == b_ and (len(figs) == 1 if code == 'k' else
                                         len(figs) == 2 and side(figs[1])[1] == n_old)
    return None if ok else 'has a wrong figure (%s)' % ', '.join(figs)


def sweep(fails, moves, res):
    by = {}
    for qid, m in moves.items():
        for st in m['s']:
            for o in st['o']:
                by[(qid, st['eq'], o['show'])] = (o, m['s'])
    want = {'best': ('right', 0, False), 'slow': ('amber', 12.5, True), 'err': ('wrong', 25, True)}
    for row in res['marks']:
        qid, eqt, show = row[:3]
        if row[3] == 'not shown':
            fails.append('%s at %s: the option %s is not on screen' % (qid, eqt, show))
            continue
        mark, pen, fb_text, has_next, trail, fb_tex = row[3:]
        has_fb = bool(fb_text)
        o, states = by[(qid, eqt, show)]
        w_mark, w_pen, w_fb = want[o['cls']]
        if (mark, pen, has_fb, has_next) != (w_mark, w_pen, w_fb, w_fb):
            fails.append('%s at %s: %s (%s) is marked %s at %s points%s%s%s' % (
                qid, eqt, show, o['cls'], mark, pen, '' if has_fb == w_fb else ', feedback wrong',
                '' if has_next == w_fb else ', Next wrong', tag('best' if o['cls'] == 'best' else 'slow')
                if mark == 'wrong' and o['cls'] != 'err' else ''))
        if has_fb and w_fb:
            try:
                why = check_feedback(o, states[[s['eq'] for s in states].index(eqt)], fb_text, fb_tex)
            except (ValueError, IndexError, KeyError) as e:
                why = 'cannot be read (%s)' % e
            if why:
                fails.append('%s at %s: the feedback on %s %s: %r' % (qid, eqt, show, why, fb_text[:120]))
        follow = o if o['cls'] != 'err' else next(x for x in states[[s['eq'] for s in states].index(eqt)]['o']
                                                   if x.get('key'))
        expect = states[follow['to']]['eq'] if follow['to'] >= 0 else follow['show']
        if trail is None or re.sub(r'\s', '', trail) != re.sub(r'\s', '', expect):
            fails.append('%s at %s: after %s the trail shows %r, not %r' % (qid, eqt, show, trail, expect))
    seen = set()
    for qid, eqt, what, text in res['shown']:
        if (qid, eqt, what) not in seen:
            seen.add((qid, eqt, what))
            fails.append('%s at %s: the %s shows raw TeX: %r (%st4-002)' % (qid, eqt, what, text[:70], ID))
    for qid, eqt, w in res['wide'][:5]:
        fails.append('%s at %s: the page scrolls sideways at 390px (%dpx)' % (qid, eqt, w))


# ------------------------------------------------------------------ self-test
PLANTS = [
    ('only the keyed move counts (the old single-key marking)', 'M1 at',
     [(None, "if(o.cls === 'e'){", "if(!o.key){"), (None, "if(ob && ob.cls === 'b')", "if(ob && ob.key)")]),
    ('the slower /3 on 3x + 7 = 22 offered as an error', 'L1 at',
     [('"L1":', '["\\\\div\\\\,3","x + \\\\frac{7}{3} = \\\\frac{22}{3}","s",2]',
       '["\\\\div\\\\,3","x + \\\\frac{7}{3} = \\\\frac{22}{3}","e","k","7","d"]')]),
]


def run(html, fails, cases=True):
    bank, moves = play(fails, html, cases)
    if bank:
        check_bank(fails, bank)
        if moves is not None:
            # the page is what the generator writes (MOVES is never edited by hand)
            import importlib.util
            spec = importlib.util.spec_from_file_location('gen_linear_moves', os.path.join(HERE, 'gen-linear-moves.py'))
            gen = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gen)
            _, generated, report = gen.generate(html)
            if report['stop'] or generated != moves:
                fails.append("the page's MOVES is not what scripts/gen-linear-moves.py generates (run it with --write)")
            return check_moves(fails, bank, expand(moves))
        fails.append('the page has no MOVES: each move phase marks one keyed option, so valid moves are marked wrong '
                     '(%st4-001)' % ID)
    return None


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
    stats = run(html, fails)
    print('%s: every move class re-derived with SymPy, every option clicked in Chromium' % SLUG)
    if stats:
        print('  %(lines)d lines, %(options)d options: %(best)d optimal, %(slow)d slower, %(err)d errors' % stats)
    ok = True
    if not args.no_selftest and not args.against:
        for what, prefix, edits in PLANTS:
            planted = html
            for anchor, old, new in edits:
                # within the anchored question's MOVES record (one line) if an anchor is given, else the whole page
                at = planted.index(anchor) if anchor else 0
                end = planted.index('\n', at) if anchor else len(planted)
                if planted[at:end].count(old) != 1:
                    print('  self-test %-58s *** CANNOT PLANT (%d) ***' % (what, planted[at:end].count(old)))
                    ok = False
                    break
                planted = planted[:at] + planted[at:end].replace(old, new) + planted[end:]
            else:
                rep = []
                run(planted, rep, cases=False)
                hit = [f for f in rep if f.startswith(prefix)]
                ok = ok and bool(hit)
                print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
