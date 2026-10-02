"""Generate and verify the Linear Equation Solver's question bank.

The game (games/linear-equation-solver/) asks a learner for the *move* at each
stage, not the answer, so every question has to carry the inverse operation for
each step, the line the equation becomes after it, and a full worked solution
for when a step is missed. Hand-writing that is how arithmetic errors get into
a lesson, so the bank is generated here with exact Fraction arithmetic and
never edited by hand.

Two independent things happen in this file, and that is deliberate:

  * the questions are BUILT from structural templates, each of which knows the
    inverse operation it needs and the misconceptions worth offering as
    distractors
  * every question is then CHECKED by re-parsing the TeX that will actually
    ship and substituting the answer that will actually ship, so a bug in a
    template cannot hide behind the template that produced it

The checks are the same ones the escape-room banks are held to in spirit: an
answer that does not satisfy its own equation, an intermediate line that does
not balance, a missing or duplicated option, or a repeated equation all stop
the run rather than reaching a class.

Structures are varied on purpose. A bank that is fifty copies of "ax + b = c"
with different numbers reads as one question asked fifty times, so the
templates move the unknown across the equals sign, put the constant first,
wrap the x in a bracket, divide the whole side, and make the coefficient
negative or fractional.

Writes the bank straight into games/linear-equation-solver/index.html between
the GENERATED BANK markers. Nothing else in that file is touched.
"""
import pathlib, re, json
from fractions import Fraction as F

GAME = pathlib.Path(r"E:\jon\maffsgames\games\linear-equation-solver\index.html")
START = "// >>> GENERATED BANK START — built by scripts/gen-linear-equations.py, do not edit by hand"
END = "// >>> GENERATED BANK END"


# ---------------------------------------------------------------- formatting
def tex_num(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return (r'-\frac{%d}{%d}' % (-v.numerator, v.denominator)) if v < 0 \
        else (r'\frac{%d}{%d}' % (v.numerator, v.denominator))


def coef(a, var='x'):
    a = F(a)
    if a == 1:
        return var
    if a == -1:
        return '-' + var
    if a.denominator == 1:
        return '%d%s' % (a.numerator, var)
    return '%s%s' % (tex_num(a), var)


def signed(b):
    b = F(b)
    return (' + ' if b > 0 else ' - ') + tex_num(abs(b))


def op_sub(b):
    return r'-\,%s' % tex_num(abs(b))


def op_add(b):
    return r'+\,%s' % tex_num(abs(b))


def op_div(a):
    a = F(a)
    return (r'\div\,(%s)' % tex_num(a)) if a < 0 else (r'\div\,%s' % tex_num(a))


def op_mul(a):
    a = F(a)
    return (r'\times\,(%s)' % tex_num(a)) if a < 0 else (r'\times\,%s' % tex_num(a))


QS = []


def uniq(seq):
    out = []
    for s in seq:
        if s not in out:
            out.append(s)
    return out


def add_q(qid, tag, eq, ops, val, sol, extra):
    QS.append({'id': qid, 'tag': tag, 'eq': eq, 'ops': ops,
               'ans': {'correct': 'x = ' + tex_num(val)},
               'sol': sol, '_val': F(val), '_extra': [F(e) for e in extra]})


# ---------------------------------------------------------------- one-step
def one_add(qid, b, c, tag='One-step · integer'):
    """x + b = c"""
    val = F(c) - F(b)
    eq = 'x%s = %s' % (signed(b), tex_num(c))
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_div(b), op_mul(b)],
            'hint': '%s has been added to x. Subtract %s from both sides.' % (tex_num(b), tex_num(b))}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [F(c) + F(b), F(c), -val])


def one_sub(qid, b, c, tag='One-step · integer'):
    """x - b = c"""
    val = F(c) + F(b)
    eq = 'x - %s = %s' % (tex_num(b), tex_num(c))
    ops = [{'correct': op_add(b), 'opts': [op_add(b), op_sub(b), op_mul(b), op_div(b)],
            'hint': '%s has been taken from x. Add %s to both sides.' % (tex_num(b), tex_num(b))}]
    sol = [eq, r'\text{Add } %s \text{ to both sides}' % tex_num(b), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [F(c) - F(b), F(c), -val])


def one_addr(qid, b, c, tag='One-step · integer'):
    """b + x = c — the unknown written second"""
    val = F(c) - F(b)
    eq = '%s + x = %s' % (tex_num(b), tex_num(c))
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_div(b), op_mul(b)],
            'hint': 'x has %s added to it, whichever way round it is written. Subtract %s.'
                    % (tex_num(b), tex_num(b))}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [F(c) + F(b), F(b) - F(c), F(c)])


def one_mul(qid, a, c, tag='One-step · integer'):
    """a x = c"""
    val = F(c) / F(a)
    eq = '%s = %s' % (coef(a), tex_num(c))
    ops = [{'correct': op_div(a), 'opts': [op_div(a), op_mul(a), op_sub(a), op_add(a)],
            'hint': 'x is multiplied by %s. Divide both sides by %s.' % (tex_num(a), tex_num(a))}]
    sol = [eq, r'\text{Divide both sides by } %s' % tex_num(a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol,
          [F(c) * F(a), F(a) / F(c) if F(c) else F(0), F(c) - F(a)])


def one_div(qid, a, c, tag='One-step · integer'):
    """x/a = c"""
    val = F(c) * F(a)
    eq = r'\frac{x}{%s} = %s' % (tex_num(a), tex_num(c))
    ops = [{'correct': op_mul(a), 'opts': [op_mul(a), op_div(a), op_add(a), op_sub(a)],
            'hint': 'x is divided by %s. Multiply both sides by %s.' % (tex_num(a), tex_num(a))}]
    sol = [eq, r'\text{Multiply both sides by } %s' % tex_num(a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [F(c) / F(a), F(c) + F(a), F(c) - F(a)])


def one_negdiv(qid, a, c, tag='One-step · negative'):
    """-x/a = c — the minus sign in front of the fraction"""
    val = -F(c) * F(a)
    eq = r'-\frac{x}{%s} = %s' % (tex_num(a), tex_num(c))
    ops = [{'correct': op_mul(-a), 'opts': [op_mul(-a), op_mul(a), op_div(-a), op_div(a)],
            'hint': 'The whole fraction is negative. Multiply both sides by %s.' % tex_num(-a)}]
    sol = [eq, r'\text{Multiply both sides by } %s' % tex_num(-a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [-val, F(c) * F(a), F(c) / F(a)])


def one_fracmul(qid, p, q, c, tag='One-step · fractional'):
    """(p/q) x = c"""
    a, recip = F(p, q), F(q, p)
    val = F(c) / a
    eq = '%s = %s' % (coef(a), tex_num(c))
    ops = [{'correct': op_mul(recip), 'opts': [op_mul(recip), op_mul(a), op_div(recip), op_add(a)],
            'hint': 'Multiplying by %s undoes multiplying by %s.' % (tex_num(recip), tex_num(a))}]
    sol = [eq, r'\text{Multiply both sides by } %s' % tex_num(recip), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [F(c) * a, F(c), F(c) + a])


def one_rhs(qid, b, c, tag='One-step · unknown on the right'):
    """c = x + b — the unknown on the right-hand side"""
    val = F(c) - F(b)
    eq = '%s = x%s' % (tex_num(c), signed(b))
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_div(b), op_mul(b)],
            'hint': 'It does not matter which side x is on. Subtract %s from both sides.' % tex_num(b)}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b),
           '%s = x' % tex_num(val), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [F(c) + F(b), F(c), -val])


# ---------------------------------------------------------------- two-step
def _first_move(b, alt_ops):
    """The move that clears a trailing constant, and how to describe it."""
    if F(b) > 0:
        return (op_sub(b), [op_sub(b), op_add(b)] + alt_ops,
                r'\text{Subtract } %s \text{ from both sides}' % tex_num(b),
                'Clear the %s first: subtract %s from both sides.' % (tex_num(b), tex_num(b)))
    return (op_add(b), [op_add(b), op_sub(b)] + alt_ops,
            r'\text{Add } %s \text{ to both sides}' % tex_num(abs(b)),
            'Clear the %s first: add %s to both sides.' % (signed(b).strip(), tex_num(abs(b))))


def two_mul_add(qid, a, b, c, tag='Two-step · integer'):
    """a x + b = c"""
    mid = F(c) - F(b)
    val = mid / F(a)
    eq = '%s%s = %s' % (coef(a), signed(b), tex_num(c))
    line1 = '%s = %s' % (coef(a), tex_num(mid))
    o1, opts1, w1, h1 = _first_move(b, [op_div(a), op_mul(a)])
    ops = [{'correct': o1, 'opts': opts1, 'hint': h1, 'line': line1},
           {'correct': op_div(a), 'opts': [op_div(a), op_mul(a), op_sub(a), op_add(a)],
            'hint': 'x is multiplied by %s. Divide both sides by %s.' % (tex_num(a), tex_num(a))}]
    sol = [eq, w1, line1, r'\text{Divide both sides by } %s' % tex_num(a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, (F(c) + F(b)) / F(a), F(c) / F(a)])


def two_const_first(qid, b, a, c, tag='Two-step · constant first'):
    """b + a x = c"""
    mid = F(c) - F(b)
    val = mid / F(a)
    eq = '%s + %s = %s' % (tex_num(b), coef(a), tex_num(c))
    line1 = '%s = %s' % (coef(a), tex_num(mid))
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_div(a), op_mul(a)],
            'hint': 'The %s is on its own, so clear it first: subtract %s.' % (tex_num(b), tex_num(b)),
            'line': line1},
           {'correct': op_div(a), 'opts': [op_div(a), op_mul(a), op_sub(a), op_add(a)],
            'hint': 'x is multiplied by %s. Divide both sides by %s.' % (tex_num(a), tex_num(a))}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b), line1,
           r'\text{Divide both sides by } %s' % tex_num(a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, (F(c) + F(b)) / F(a), F(c) / F(a)])


def two_rhs(qid, c, a, b, tag='Two-step · unknown on the right'):
    """c = a x + b"""
    mid = F(c) - F(b)
    val = mid / F(a)
    eq = '%s = %s%s' % (tex_num(c), coef(a), signed(b))
    line1 = '%s = %s' % (tex_num(mid), coef(a))
    o1, opts1, w1, h1 = _first_move(b, [op_div(a), op_mul(a)])
    ops = [{'correct': o1, 'opts': opts1,
            'hint': h1 + ' The x being on the right changes nothing.', 'line': line1},
           {'correct': op_div(a), 'opts': [op_div(a), op_mul(a), op_sub(a), op_add(a)],
            'hint': 'x is multiplied by %s. Divide both sides by %s.' % (tex_num(a), tex_num(a))}]
    sol = [eq, w1, line1, r'\text{Divide both sides by } %s' % tex_num(a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, (F(c) + F(b)) / F(a), F(c) / F(a)])


def two_div_add(qid, a, b, c, tag='Two-step · integer'):
    """x/a + b = c"""
    mid = F(c) - F(b)
    val = mid * F(a)
    eq = r'\frac{x}{%s}%s = %s' % (tex_num(a), signed(b), tex_num(c))
    line1 = r'\frac{x}{%s} = %s' % (tex_num(a), tex_num(mid))
    o1, opts1, w1, h1 = _first_move(b, [op_mul(a), op_div(a)])
    ops = [{'correct': o1, 'opts': opts1, 'hint': h1, 'line': line1},
           {'correct': op_mul(a), 'opts': [op_mul(a), op_div(a), op_add(a), op_sub(a)],
            'hint': 'x is divided by %s. Multiply both sides by %s.' % (tex_num(a), tex_num(a))}]
    sol = [eq, w1, line1, r'\text{Multiply both sides by } %s' % tex_num(a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, (F(c) + F(b)) * F(a), mid / F(a)])


def two_bracket(qid, a, b, c, tag='Two-step · brackets'):
    """a(x + b) = c"""
    mid = F(c) / F(a)
    val = mid - F(b)
    inner = 'x%s' % signed(b)
    eq = '%s(%s) = %s' % (tex_num(a), inner, tex_num(c))
    line1 = '%s = %s' % (inner, tex_num(mid))
    if F(b) > 0:
        o2, w2 = op_sub(b), r'\text{Subtract } %s \text{ from both sides}' % tex_num(b)
        h2, opts2 = 'Now subtract %s from both sides.' % tex_num(b), [op_sub(b), op_add(b), op_div(b), op_mul(b)]
    else:
        o2, w2 = op_add(b), r'\text{Add } %s \text{ to both sides}' % tex_num(abs(b))
        h2, opts2 = 'Now add %s to both sides.' % tex_num(abs(b)), [op_add(b), op_sub(b), op_div(b), op_mul(b)]
    ops = [{'correct': op_div(a), 'opts': [op_div(a), op_mul(a), op_sub(b), op_add(b)],
            'hint': 'The whole bracket is multiplied by %s. Divide both sides by %s first.'
                    % (tex_num(a), tex_num(a)), 'line': line1},
           {'correct': o2, 'opts': opts2, 'hint': h2}]
    sol = [eq, r'\text{Divide both sides by } %s' % tex_num(a), line1, w2, 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, F(c) - F(a) * F(b), mid + F(b)])


def two_fracbracket(qid, a, b, c, tag='Two-step · brackets'):
    """(x + b)/a = c"""
    mid = F(c) * F(a)
    val = mid - F(b)
    inner = 'x%s' % signed(b)
    eq = r'\frac{%s}{%s} = %s' % (inner, tex_num(a), tex_num(c))
    line1 = '%s = %s' % (inner, tex_num(mid))
    if F(b) > 0:
        o2, w2 = op_sub(b), r'\text{Subtract } %s \text{ from both sides}' % tex_num(b)
        h2, opts2 = 'Now subtract %s from both sides.' % tex_num(b), [op_sub(b), op_add(b), op_div(b), op_mul(b)]
    else:
        o2, w2 = op_add(b), r'\text{Add } %s \text{ to both sides}' % tex_num(abs(b))
        h2, opts2 = 'Now add %s to both sides.' % tex_num(abs(b)), [op_add(b), op_sub(b), op_div(b), op_mul(b)]
    ops = [{'correct': op_mul(a), 'opts': [op_mul(a), op_div(a), op_sub(b), op_add(b)],
            'hint': 'The whole of %s is divided by %s. Multiply both sides by %s first.'
                    % (inner, tex_num(a), tex_num(a)), 'line': line1},
           {'correct': o2, 'opts': opts2, 'hint': h2}]
    sol = [eq, r'\text{Multiply both sides by } %s' % tex_num(a), line1, w2, 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, F(c) - F(b), mid + F(b)])


def two_const_sub(qid, b, a, c, tag='Two-step · negative'):
    """b - a x = c"""
    mid = F(c) - F(b)
    val = mid / F(-a)
    eq = '%s - %s = %s' % (tex_num(b), coef(a), tex_num(c))
    line1 = '%s = %s' % (coef(-a), tex_num(mid))
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_div(a), op_mul(a)],
            'hint': 'Subtract %s from both sides. The x term is negative, and that is fine.' % tex_num(b),
            'line': line1},
           {'correct': op_div(-a), 'opts': [op_div(-a), op_div(a), op_mul(-a), op_mul(a)],
            'hint': 'x is multiplied by %s. Divide both sides by %s.' % (tex_num(-a), tex_num(-a))}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b), line1,
           r'\text{Divide both sides by } %s' % tex_num(-a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [-val, mid, (F(b) + F(c)) / F(a)])


def two_negmul_add(qid, a, b, c, tag='Two-step · negative'):
    """-a x + b = c"""
    mid = F(c) - F(b)
    val = mid / F(-a)
    eq = '%s%s = %s' % (coef(-a), signed(b), tex_num(c))
    line1 = '%s = %s' % (coef(-a), tex_num(mid))
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_div(-a), op_mul(-a)],
            'hint': 'Clear the %s first: subtract %s from both sides.' % (tex_num(b), tex_num(b)),
            'line': line1},
           {'correct': op_div(-a), 'opts': [op_div(-a), op_div(a), op_mul(-a), op_mul(a)],
            'hint': 'Divide both sides by %s. Dividing by a negative changes the sign.' % tex_num(-a)}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b), line1,
           r'\text{Divide both sides by } %s' % tex_num(-a), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [-val, mid, mid / F(a)])


def two_negx_add(qid, b, c, tag='Two-step · negative'):
    """-x + b = c"""
    mid = F(c) - F(b)
    val = -mid
    eq = '-x%s = %s' % (signed(b), tex_num(c))
    line1 = '-x = %s' % tex_num(mid)
    ops = [{'correct': op_sub(b), 'opts': [op_sub(b), op_add(b), op_mul(-1), op_div(-1)],
            'hint': 'Subtract %s from both sides to leave the x term alone.' % tex_num(b),
            'line': line1},
           {'correct': op_mul(-1), 'opts': [op_mul(-1), op_mul(1), op_add(mid), op_sub(mid)],
            'hint': 'You have -x, not x. Multiply both sides by -1.'}]
    sol = [eq, r'\text{Subtract } %s \text{ from both sides}' % tex_num(b), line1,
           r'\text{Multiply both sides by } -1', 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, F(c) + F(b), -F(c) - F(b)])


def two_fracmul_add(qid, p, q, b, c, tag='Two-step · fractional'):
    """(p/q) x + b = c"""
    a, recip = F(p, q), F(q, p)
    mid = F(c) - F(b)
    val = mid / a
    eq = '%s%s = %s' % (coef(a), signed(b), tex_num(c))
    line1 = '%s = %s' % (coef(a), tex_num(mid))
    o1, opts1, w1, h1 = _first_move(b, [op_mul(recip), op_mul(a)])
    ops = [{'correct': o1, 'opts': opts1, 'hint': h1, 'line': line1},
           {'correct': op_mul(recip), 'opts': [op_mul(recip), op_mul(a), op_div(recip), op_add(recip)],
            'hint': 'Multiplying by %s undoes multiplying by %s.' % (tex_num(recip), tex_num(a))}]
    sol = [eq, w1, line1, r'\text{Multiply both sides by } %s' % tex_num(recip), 'x = ' + tex_num(val)]
    add_q(qid, tag, eq, ops, val, sol, [mid, mid * a, (F(c) + F(b)) / a])


# ════════════════════════════════════════════════════════════════ THE BANK
# A — one-step, integer
for i, (b, c) in enumerate([(7, 12), (9, 4), (15, 8), (6, 31), (24, 11), (13, 13),
                            (8, 3), (19, 40)], 1):
    one_add('A%d' % i, b, c)
for i, (b, c) in enumerate([(9, 4), (5, 12), (14, 6), (3, 20), (11, 2), (17, 17), (6, 25)], 1):
    one_sub('B%d' % i, b, c)
for i, (b, c) in enumerate([(12, 30), (5, 2), (21, 9), (8, 41)], 1):
    one_addr('C%d' % i, b, c)
for i, (a, c) in enumerate([(6, 42), (9, 54), (7, 91), (11, 88), (4, 100), (3, 51)], 1):
    one_mul('D%d' % i, a, c)
for i, (a, c) in enumerate([(4, 9), (7, 3), (5, 12), (6, 7), (9, 4), (2, 17)], 1):
    one_div('E%d' % i, a, c)

# B — one-step, negative and fractional
for i, (a, c) in enumerate([(-4, 20), (5, -35), (-3, -27), (-7, 42), (8, -56)], 1):
    one_mul('F%d' % i, a, c, tag='One-step · negative')
for i, (a, c) in enumerate([(3, -6), (5, -4), (2, -13)], 1):
    one_div('G%d' % i, a, c, tag='One-step · negative')
for i, (a, c) in enumerate([(3, 5), (4, -2)], 1):
    one_negdiv('H%d' % i, a, c)
for i, (a, c) in enumerate([(8, 12), (10, -4), (6, 15), (4, 10), (9, -6)], 1):
    one_mul('I%d' % i, a, c, tag='One-step · fractional')
for i, (p, q, c) in enumerate([(2, 3, 8), (3, 5, 9), (4, 7, 12), (5, 2, 15), (2, 9, 6)], 1):
    one_fracmul('J%d' % i, p, q, c)
for i, (b, c) in enumerate([(7, 12), (4, 19), (13, 5), (9, -2)], 1):
    one_rhs('K%d' % i, b, c)

# C — two-step, integer
for i, (a, b, c) in enumerate([(3, 7, 22), (5, -4, 31), (2, 9, 25), (7, -12, 30),
                               (4, 11, 39), (6, -5, 37), (8, 3, 59), (9, -7, 65),
                               (5, 13, 48), (3, -8, 16), (12, 5, 41), (7, 6, 62)], 1):
    two_mul_add('L%d' % i, a, b, c)
for i, (a, b, c) in enumerate([(2, 5, 11), (3, -4, 2), (5, 7, 12), (4, -9, 1),
                               (6, 3, 8), (7, -2, 5)], 1):
    two_div_add('M%d' % i, a, b, c)
for i, (a, b, c) in enumerate([(2, 3, 16), (5, -2, 35), (3, 4, 27), (4, -5, 28),
                               (6, 2, 42), (7, -3, 49), (2, 9, 30), (3, -6, 15)], 1):
    two_bracket('N%d' % i, a, b, c)
for i, (a, b, c) in enumerate([(3, 4, 5), (2, -6, 7), (5, 3, 4), (4, -7, 2),
                               (6, 5, 3), (3, -2, 9)], 1):
    two_fracbracket('O%d' % i, a, b, c)
for i, (b, a, c) in enumerate([(7, 3, 22), (5, 4, 29), (11, 6, 47), (9, 2, 25),
                               (13, 5, 38), (4, 8, 60), (6, 7, 55)], 1):
    two_const_first('P%d' % i, b, a, c)
for i, (c, a, b) in enumerate([(22, 3, 7), (31, 5, -4), (19, 2, 9), (43, 6, -5),
                               (37, 4, 13), (58, 9, 4)], 1):
    two_rhs('Q%d' % i, c, a, b)

# D — two-step, negatives
for i, (a, b, c) in enumerate([(3, 14, 5), (2, -7, -19), (6, 25, 7), (4, 9, -11),
                               (5, 18, 3), (8, 30, 6)], 1):
    two_mul_add('R%d' % i, a, b, c, tag='Two-step · negative')
for i, (b, a, c) in enumerate([(5, 2, 13), (10, 3, 1), (8, 4, 24), (7, 5, 32), (12, 2, 20)], 1):
    two_const_sub('S%d' % i, b, a, c)
for i, (a, b, c) in enumerate([(4, 9, 33), (3, 5, 20), (6, 11, 47)], 1):
    two_negmul_add('T%d' % i, a, b, c)
for i, (b, c) in enumerate([(6, 10), (9, 15), (4, 11), (12, 20)], 1):
    two_negx_add('U%d' % i, b, c)
for i, (a, b, c) in enumerate([(4, 9, 5), (3, 8, 2), (5, 6, 1)], 1):
    two_div_add('V%d' % i, a, b, c, tag='Two-step · negative')
for i, (a, b, c) in enumerate([(3, 8, 9), (2, -5, -24), (4, 7, 12), (5, -3, -20)], 1):
    two_bracket('W%d' % i, a, b, c, tag='Two-step · negative')

# E — two-step, fractional answers and fractional coefficients
for i, (a, b, c) in enumerate([(2, 1, 8), (4, -3, 7), (6, 5, 12), (3, 2, 6),
                               (8, -1, 3), (10, 7, 13), (9, 4, 10), (4, 5, 8),
                               (6, -7, 2), (8, 3, 10)], 1):
    two_mul_add('X%d' % i, a, b, c, tag='Two-step · fractional')
for i, (p, q, b, c) in enumerate([(2, 3, 4, 10), (3, 4, -2, 7), (2, 5, -3, 5),
                                  (5, 6, 4, 14), (3, 8, -1, 5), (4, 5, 6, 18)], 1):
    two_fracmul_add('Y%d' % i, p, q, b, c)


# ------------------------------------------------- answer options, then checks
for q in QS:
    val = q['_val']
    cands = [val] + q['_extra'] + [val + 1, val - 1, val * 2, -val, val + 2, val - 3]
    opts = uniq(['x = ' + tex_num(v) for v in cands])[:4]
    q['ans']['opts'] = opts
    del q['_val'], q['_extra']


# ---- independent verification: re-parse the TeX that will actually ship ----
def tex_to_expr(t):
    s = t.replace(r'\,', '').replace(r'\times', '*').replace(r'\div', '/')
    pat = re.compile(r'\\frac\{([^{}]*)\}\{([^{}]*)\}')
    while pat.search(s):
        s = pat.sub(lambda m: '((%s)/(%s))' % (m.group(1), m.group(2)), s)
    s = re.sub(r'(\d)\s*x', r'\1*x', s)
    s = re.sub(r'(\d)\s*\(', r'\1*(', s)
    s = re.sub(r'\)\s*x', r')*x', s)
    s = re.sub(r'\)\s*\(', r')*(', s)
    s = re.sub(r'(?<![\w.])(\d+)(?![\w.])', r'F(\1)', s)
    return s


def ev(t, x=None):
    return eval(tex_to_expr(t), {'__builtins__': {}}, {'F': F, 'x': x})


problems = []
for q in QS:
    xv = ev(q['ans']['correct'][3:].strip())
    lhs, rhs = q['eq'].split('=')
    if F(ev(lhs, xv)) != F(ev(rhs, xv)):
        problems.append('%s: answer does not satisfy %s' % (q['id'], q['eq']))
    if q['sol'][-1].replace(' ', '') != q['ans']['correct'].replace(' ', ''):
        problems.append('%s: worked solution ends on %r, answer is %r'
                        % (q['id'], q['sol'][-1], q['ans']['correct']))
    for n, o in enumerate(q['ops']):
        if o['correct'] not in o['opts']:
            problems.append('%s: op%d correct option missing' % (q['id'], n))
        if len(set(o['opts'])) != 4:
            problems.append('%s: op%d has duplicate options' % (q['id'], n))
        if 'line' in o:
            l, r = o['line'].split('=')
            if F(ev(l, xv)) != F(ev(r, xv)):
                problems.append('%s: intermediate line %r does not balance' % (q['id'], o['line']))
    if q['ans']['correct'] not in q['ans']['opts']:
        problems.append('%s: answer missing from its own options' % q['id'])
    if len(set(q['ans']['opts'])) != 4:
        problems.append('%s: duplicate answer options' % q['id'])
    if 'line' in q['ops'][-1]:
        problems.append('%s: last move must not reveal the answer line' % q['id'])

if len(set(q['id'] for q in QS)) != len(QS):
    problems.append('duplicate question id')
if len(set(q['eq'] for q in QS)) != len(QS):
    seen = {}
    for q in QS:
        seen.setdefault(q['eq'], []).append(q['id'])
    problems += ['duplicate equation %r in %s' % (e, ids) for e, ids in seen.items() if len(ids) > 1]

if problems:
    print('BANK REJECTED — %d problem(s):' % len(problems))
    for p in problems[:40]:
        print('  ', p)
    raise SystemExit(1)


# ------------------------------------------------------------------- emit
def js(o):
    return json.dumps(o, ensure_ascii=False)


rows = []
for q in QS:
    parts = ['id:%s' % js(q['id']), 'tag:%s' % js(q['tag']), 'eq:%s' % js(q['eq'])]
    ops = []
    for o in q['ops']:
        p = ['correct:%s' % js(o['correct']), 'opts:%s' % js(o['opts']), 'hint:%s' % js(o['hint'])]
        if 'line' in o:
            p.append('line:%s' % js(o['line']))
        ops.append('{' + ', '.join(p) + '}')
    parts.append('ops:[' + ','.join(ops) + ']')
    parts.append('ans:{correct:%s,opts:%s}' % (js(q['ans']['correct']), js(q['ans']['opts'])))
    parts.append('sol:%s' % js(q['sol']))
    rows.append('  {' + ', '.join(parts) + '}')

bank = 'const QUESTIONS = {\n  gcse: [\n' + ',\n'.join(rows) + '\n  ]\n};'

html = GAME.read_text(encoding='utf-8')
i, j = html.index(START), html.index(END)
GAME.write_text(html[:i + len(START)] + '\n' + bank + '\n' + html[j:], encoding='utf-8', newline='\n')

one = sum(1 for q in QS if len(q['ops']) == 1)
print('questions        :', len(QS), '(%d one-step, %d two-step)' % (one, len(QS) - one))
print('distinct shapes  :', len(set(q['tag'] for q in QS)))
print('negative answers :', sum(1 for q in QS if '-' in q['ans']['correct']))
print('fraction answers :', sum(1 for q in QS if 'frac' in q['ans']['correct']))
print('all checks passed; bank written to', GAME)
