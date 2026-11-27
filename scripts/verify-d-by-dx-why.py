#!/usr/bin/env python3
# ci-shards: d by dx? Why? (the 60-item bank held to the contract's SHA-256 and counts; every question differentiated in sympy from its own terms; every decoy recomputed from its error key, allowed for its stage (ERR_STAGES) and no two options equal in value; every TeX string, prompt and board line of working re-rendered from its terms, every TeX string read back to its value and every working line equal in sympy to the function or its derivative; every item's two curves finite, inside its window and within 4 times each other's height; the start screen's three pairs each a function and its derivative, none a question in the game; one LINES line per error key; every stage played to the end with the table and in Pro; a right answer and a wrong one each draw the gradient function and wait for Next; the drawn curves read back from the page to f and f' within 1 px, never a decoy; the start screen's two pens at the same x, paused in a hidden tab, still with reduced motion; every item's asking, right and wrong screens above the fold at 375x667, 390x844, 1280x720 and 1366x768, normal and Aa, and at 320x568 normal, with the table and in Pro; the start screen at four sizes; fault-injection self-test) | | 4
# ci-deps: games/d-by-dx-why/ tools/d-by-dx-why/ schools/assets/plot.js
r"""Independent verification for d by dx? Why? (games/d-by-dx-why/), contracts D-BY-DX-BUILD (26 Nov 2026) and
D-BY-DX-GRAPH (27 Nov 2026). SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 60 items and the start screen's three pairs, the output of tools/d-by-dx-why/bank.py
embedded one a line. This script never runs or imports that generator: it reads ERR_STAGES and START_SHOW from its
source as data (ast: literals, and the two helper calls T(...) and F(...) worked out here), reads the bank from the
page, and works everything out again:

  Bank     the item lines hash to the contract's SHA-256; 60 items, 12 in each of five stages, ids and prompts unique,
           20 items in each of the three wordings. Each question is rebuilt in sympy from its "q" terms and
           differentiated by sympy; the answer's terms must be that derivative. Every decoy is recomputed from its err
           key and the question's terms (the expression that named error gives, written here, with sympy doing the
           calculus where the error is one). No two of an item's four options are equal in value (sympy). Every TeX
           string (the question, the answer, each decoy, with Stage 2's options written back in the question's form as
           fractions and roots) is rendered again from its terms by this script's own formatter and must equal the
           bank's; so must the prompt, from the item's wording, letter and dependent letter (itself worked out here).
           Every TeX string is also READ BACK by this script's own small TeX reader into sympy and must equal the
           value of its terms, so what the student sees means what the terms say. Every decoy's err key is one
           ERR_STAGES allows for the item's stage. "rows" is the table row or rows the item's stage and kind need.
  Working  every board line (label, left side, right side) is rebuilt from the item's own numbers and must equal the
           bank's. Then each line's right side is read back into sympy and must EQUAL its side: the question's
           function where the left side is f(..) or the dependent letter, its derivative where it is f'(..) or the
           stacked d../d.., and the same on every line that carries on from one. The last line is the answer.
  Graph    for every item, on its own window: both curves finite and inside its y-range at 401 samples, and neither
           curve more than 4 times the other's height (the contract's READABLE).
  Start    the page's START_SHOW is the generator's three pairs; each is a function and its derivative (sympy); none is
           a bank question in any letter (sympy); each is readable on its window as above; its two TeX strings are
           re-rendered and read back.
  Lines    LINES in the page has exactly the keys of ERR_STAGES; every key the bank uses has a line and no line is unused.
  KaTeX    in Chromium, every TeX string in the bank (prompts, options, working sides), the start screen's and the
           table's renders in KaTeX without an error.
  Play     in Chromium at 375 x 667 and 1280 x 720, each stage played to the end with the table and in Pro (ten runs a
           size): eight different items of that stage, four options each, every button's dataset.val the bank's TeX and
           its label KaTeX. With the question the graph holds the function alone; its panel is open from 1024 px and a
           closed "Graph" button on anything narrower. A right answer shows "Right:" and the answer, draws the
           gradient function, and waits on Next. A wrong answer marks the chosen option wrong and the answer right,
           shows exactly the LINES line for the chosen option's err key, the working line by line (label, left side,
           "=" and the right side), the item's table rows under "From the table:" and Next, with no "The answer is"
           line; the graph then holds the function and the gradient function and nothing else, and its button reads
           "See the gradient function"; opened by the student on a narrow screen, it is closed again by Next. The
           score is the right answers; one game_completed and one leaderboard submission on the run's board; no event
           but game_started, question_answered (with the item's id) and game_completed. The table as before: the
           contract's six rows, open at 1280 x 720, closed at 375 x 667, lit rows after a wrong answer, gone in Pro.
  Waits    at 375 x 667 on a fast clock (the page's setTimeout at 1/100 of its length): a right answer does not move
           on in 30 s, then Enter advances; the next, Space; a wrong answer waits the same.
  Graph    (in Chromium, "graph 1280x720" and "graph 375x667") for every item: with the question one curve, labelled
           as the prompt names it (f(t), or y, s or A), and the axes lettered with the item's own letters; once
           answered (a wrong option, each item a different one of its three) two curves, the second labelled f'(t) or
           the stacked d../d... Each curve's path is read from the page and every point of it mapped back through the
           path's own data attributes: it must lie within 1 px of the function (or of its derivative) worked out here
           from the item's terms, span the whole window and be sampled at least once for every 2 px. So the curve
           drawn after an answer is the derivative itself: not a decoy, not a tangent. The gradient function is seen
           to draw in (not there at once, finished within 3 s) on the first item of each stage. The two curves differ
           in width, and each colour is 3:1 or better on the panel behind it.
  Pens     the start screen at 1280 x 720: the two pens are read about every 140 ms while the first pair draws. At
           every reading they are at the same x, each on its own curve within 1 px; the equations are not yet written.
           When they finish (4 s by the page's own figure, never sooner) the pens go and y = ... and the stacked
           dy/dx = ... are written under the graph; 3 s later, never sooner, the next pair starts. A hidden tab stops the drawing where it is, and it carries on
           when the tab shows again. The third pair is followed by the first. With prefers-reduced-motion ("still
           1280x720"): the first pair finished and still, its labels and equations there, no pens, no second pair; and
           a gradient function is drawn at once.
  Fit      at 375 x 667, 390 x 844, 1280 x 720 and 1366 x 768, normal and Aa (the Aa button pressed, its fonts loaded),
           with the table and in Pro, for every item: the asking screen (the prompt on screen, the last option ending
           above the fold: the viewport less the 40 px footer, in page coordinates); the right-answer screen ("Right:",
           the marked answer and Next above the fold); and, for each of its three wrong options, the line, the
           working, the table rows and Next above the fold, the prompt and the two marked options on screen above it,
           the line shown that option's, the "=" signs of the working in one column, each label above its line below
           1024 px and beside it from 1024 px. The page never scrolls sideways. From 1024 px the graph is on screen
           above the fold beside the question; narrower, opening the graph's fold-out does not move Next. The options'
           maths is at least 1.35 times the body's size. The same at 320 x 568 in normal mode (canon §7.6.1's smallest
           phone; Aa there is canon's recorded exception), except that the table rows, which the page moves below Next
           on a screen 600 px tall or less (canon §7.6.1's fixed rule), need only be on the page.
  Start    "start <W>x<H> <normal|Aa>" at 320 x 568, 375 x 667, 1280 x 720 and 1920 x 1080: the picture is on the page,
           between 40% and the whole of its column wide; no start control (the Pro switch, the five stage buttons) that
           ends above the fold without the picture ends below it with the picture; at the two wide sizes every one of
           them ends above the fold; no sideways scroll.

Work units: "bank" (no browser), "katex 1280x720", "play <W>x<H>" (2), "waits 375x667", "graph <W>x<H>" (2),
"pens 1280x720", "still 1280x720", "fit <W>x<H> <normal|Aa> <table|pro>" (18), "start <W>x<H> <normal|Aa>" (8) and
"plant: <what>" (one per planted fault).

    python scripts/verify-d-by-dx-why.py              # every unit, then the self-test
    python scripts/verify-d-by-dx-why.py --selftest   # the planted faults only
"""
import argparse
import ast
import contextlib
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'd-by-dx-why'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
GENERATOR = os.path.join(ROOT, 'tools', SLUG, 'bank.py')
SHA256 = 'c6c0c8dce9658c16d4d37fa6094320a3cdeb84685203fa0d3f8e6d5d9bb7c960'   # contract D-BY-DX-GRAPH
STAGE_NAMES = ['Power terms', 'Rewrite first', 'Sin and cos', 'e and ln', 'Sums of terms']
MODES = ['stage-%d' % n for n in range(1, 6)] + ['pro-stage-%d' % n for n in range(1, 6)]
PER = 8
PER_STAGE = 12
FOOTER = 40
SIZES = [(375, 667), (390, 844), (1280, 720), (1366, 768)]
SMALL = (320, 568)   # canon §7.6.1's smallest phone: normal mode only (Aa at 320 x 568 is the recorded exception)
PLAY_SIZES = [(375, 667), (1280, 720)]
START_SIZES = [(320, 568), (375, 667), (1280, 720), (1920, 1080)]
WIDE = 1024          # the page's own breakpoint: the graph and the table beside the question from here
EVENTS = {'game_started', 'question_answered', 'game_completed'}
VARS = {'x', 'r', 't', 'z'}
FORMS = {'wrt', 'leib', 'fn'}
READABLE = 4         # the contract: neither curve more than 4 times the other's height over the item's window
SAMPLES = 400
DRAW_S, HOLD_S = 4.0, 3.0   # the start screen: about 4 s drawing a pair, about 3 s left to settle
# The table, as the contract gives it: [key, y, dy/dx], in this order, and the two headings.
TABLE_HEAD = [r"\(y\) or \(f(x)\)", r"\(\dfrac{dy}{dx}\) or \(f'(x)\)"]
TABLE = [['x', r'\(x\)', r'\(1\)'], ['axn', r'\(ax^{n}\)', r'\(anx^{n-1}\)'], ['sin', r'\(\sin ax\)', r'\(a\cos ax\)'],
         ['cos', r'\(\cos ax\)', r'\(-a\sin ax\)'], ['exp', r'\(e^{ax}\)', r'\(ae^{ax}\)'], ['ln', r'\(\ln ax\)', r'\(\frac{1}{x}\)']]


# ---------------------------------------------------------------- the page's bank and lines, read from its source
def block_lines(html, name):
    """The raw lines of a one-a-line array in the page (BANK, START_SHOW), each as the generator wrote it (the joining
    comma removed)."""
    m = re.search(r'\n  var %s = \[\n(.*?)\n  \];' % name, html, re.S)
    if not m:
        raise ValueError('no %s block in the page' % name)
    lines = m.group(1).split('\n')
    return [ln[:-1] if ln.endswith(',') else ln for ln in lines]


def bank_lines(html):
    return block_lines(html, 'BANK')


def lines_of(html):
    """The page's LINES object: {err key: line}."""
    m = re.search(r'\n  var LINES = \{\n(.*?)\n  \};', html, re.S)
    if not m:
        raise ValueError('no LINES object in the page')
    out = {}
    for ln in m.group(1).split('\n'):
        k = re.match(r'^\s+([a-z0-9_]+): (".*"),?$', ln)
        if not k:
            raise ValueError('a LINES line this script cannot read: %r' % ln[:60])
        if k.group(1) in out:
            raise ValueError('LINES has %s twice' % k.group(1))
        out[k.group(1)] = json.loads(k.group(2))
    return out


def fs(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def generator_data(name):
    """A top-level value from the generator's source, as data. The file is never run: its syntax tree is read, and only
    literals, a leading minus and the two helper calls are worked out, here: T(kind, a, b, ...) is a term (the kind, then
    each number as "p" or "p/q") and F(p, q) is a fraction."""
    def ev(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.List):
            return [ev(e) for e in n.elts]
        if isinstance(n, ast.Set):
            return {ev(e) for e in n.elts}
        if isinstance(n, ast.Dict):
            return {ev(k): ev(v) for k, v in zip(n.keys, n.values)}
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and not n.keywords:
            args = [ev(a) for a in n.args]
            if n.func.id == 'T':
                return [args[0]] + [fs(a) for a in args[1:]]
            if n.func.id == 'F':
                return Fraction(*args)
        raise ValueError('%s in the generator holds something this script does not read as data (line %d)' % (name, n.lineno))
    tree = ast.parse(open(GENERATOR, encoding='utf-8').read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ev(node.value)
    raise ValueError('no %s in %s' % (name, GENERATOR))


def err_stages():
    return generator_data('ERR_STAGES')


# ---------------------------------------------------------------- this script's own TeX, from an item's terms
def ftex(x, big=False):
    """A whole number as its digits; a fraction with the sign in front, stacked large (\\dfrac) on the line and small
    (\\frac) in a power or an angle."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + ('\\dfrac{%d}{%d}' if big else '\\frac{%d}{%d}') % (abs(x.numerator), x.denominator)


def root(v, p):
    """v to a positive fractional power m/k, as a root: the k-th root of v^m."""
    inner = v if p.numerator == 1 else '%s^{%d}' % (v, p.numerator)
    return '\\sqrt{%s}' % inner if p.denominator == 2 else '\\sqrt[%d]{%s}' % (p.denominator, inner)


def body(t, v, back=False):
    """One term without its sign: (the sign is negative, the TeX of its size). back: a power term written back in the
    question's form (Stage 2's options): a negative power as a fraction over a positive power, a fractional one as a root."""
    kind, a = t[0], [Fraction(s) for s in t[1:]]
    c, size = a[0], abs(a[0])
    front = '' if size == 1 else ftex(size, big=True)   # a coefficient of 1 is not written in front of a letter or function
    inside = (lambda m: v if m == 1 else ftex(m) + v)    # 3x, or x when the multiple is 1
    if kind == 'const' or (kind == 'pow' and a[1] == 0):
        s = ftex(size, big=True)
    elif kind == 'pow' and back:
        n = abs(a[1])
        power = root(v, n) if n.denominator > 1 else (v if n == 1 else '%s^{%d}' % (v, n.numerator))
        if a[1] > 0:
            s = front + power
        else:
            s = '\\dfrac{%d}{%s%s}' % (size.numerator, '' if size.denominator == 1 else str(size.denominator), power)
    elif kind == 'pow':
        s = front + (v if a[1] == 1 else '%s^{%s}' % (v, ftex(a[1])))
    elif kind == 'sin':
        s = front + '\\sin ' + inside(a[1])
    elif kind == 'cos':
        s = front + '\\cos ' + inside(a[1])
    elif kind == 'exp':
        s = front + 'e^{%s}' % inside(a[1])
    elif kind == 'ln':
        s = front + '\\ln ' + inside(a[1])
    elif kind == 'xexp':
        s = front + v + 'e^{%s-1}' % inside(a[1])
    elif kind == 'over':
        s = '\\dfrac{%s}{%s}' % (ftex(size), inside(a[1]))
    elif kind == 'overpow':
        s = '\\dfrac{%s}{%s%s}' % (ftex(size), ftex(a[1]), v if a[2] == 1 else '%s^{%s}' % (v, ftex(a[2])))
    elif kind == 'recipln':
        s = '\\dfrac{%s}{\\ln %s}' % (ftex(size), inside(a[1]))
    else:
        raise ValueError('a term kind this script does not know: %r' % kind)
    return c < 0, s


def render(terms, v, back=False):
    out = ''
    for i, t in enumerate(terms):
        neg, s = body(t, v, back)
        out += ('-' if neg else ('+' if i else '')) + s
    return out


def written(q):
    """The question as it is written. Stages 1 and 3-5: its terms as they stand. Stage 2: a negative whole power as a
    stacked fraction over the letter's power, a fractional power as a root."""
    v, terms = q['var'], q['q']
    if q['stage'] != 2:
        return render(terms, v)
    c, p = Fraction(terms[0][1]), Fraction(terms[0][2])
    if p.denominator == 1:
        n = -p.numerator
        return ('-' if c < 0 else '') + '\\dfrac{%d}{%s}' % (abs(c).numerator, v if n == 1 else '%s^%d' % (v, n))
    rt = '\\sqrt{%s^{%d}}' % (v, p.numerator) if p.denominator == 2 else '\\sqrt[%d]{%s^{%d}}' % (p.denominator, v, p.numerator)
    return ('' if c == 1 else ftex(c)) + rt


def dep_of(q, place):
    """The dependent letter (Jon, 27 Nov 2026: not always x and y): f in the f(..) wording; otherwise A for r, s for the
    t items in an even place in their stage, y for the rest."""
    if q['form'] == 'fn':
        return 'f'
    v = q['var']
    return 'A' if v == 'r' else ('s' if v == 't' and place % 2 == 0 else 'y')


def f_name(q):
    return 'f(%s)' % q['var'] if q['form'] == 'fn' else q['dep']


def d_name(q):
    return "f'(%s)" % q['var'] if q['form'] == 'fn' else '\\dfrac{d%s}{d%s}' % (q['dep'], q['var'])


def prompt_of(q, qtex):
    v, y = q['var'], q['dep']
    if q['form'] == 'wrt':
        return 'Differentiate \\(%s = %s\\) with respect to \\(%s\\)' % (y, qtex, v)
    if q['form'] == 'leib':
        return '\\(%s = %s\\). Find \\(\\dfrac{d%s}{d%s}\\)' % (y, qtex, y, v)
    return "If \\(f(%s) = %s\\), find \\(f'(%s)\\)" % (v, qtex, v)


def power_down(c, n, v):
    """c v^n with the power brought down and one taken off it, before any tidying."""
    p = '%s^{%s-1}' % (v, ftex(n))
    if c == 1:
        return ftex(n, big=True) + p
    second = ftex(n, big=True)
    return '%s \\times %s\\,%s' % (ftex(c, big=True), '(%s)' % second if n < 0 else second, p)


def power_lines(c, n, v):
    return [('power down, take one off', 'd', power_down(c, n, v)),
            ('tidy up', '', render([['pow', fs(c * n), fs(n - 1)]], v))]


def working_of(q, ans_tex):
    """The item's board lines, rebuilt from its own terms: [(label, side, right side)], side 'f' the function, 'd' its
    derivative, '' a line that carries on."""
    v, st, terms = q['var'], q['stage'], q['q']
    nums = [Fraction(s) for s in terms[0][1:]]
    if st == 1:
        c, n = nums
        w = [('the letter goes, the number stays', 'd', ftex(c))] if n == 1 else power_lines(c, n, v)
    elif st == 2:
        c, p = nums
        first = 'rewrite as a power' if p.denominator == 1 else 'root to a power: its number on the bottom'
        w = [(first, 'f', render(terms, v))] + power_lines(c, p, v) + [('write it back', '', ans_tex)]
    elif st == 3:
        c, a = nums
        angle = v if a == 1 else ftex(a) + v
        if terms[0][0] == 'sin':
            w = [('a out front, and in the angle', 'd', '%s\\cos %s' % (ftex(a), angle) if c == 1 else '%s \\times %s\\cos %s' % (ftex(c), ftex(a), angle))]
        else:
            w = [('a out front; cos gives a minus', 'd', '-%s\\sin %s' % (ftex(a), angle) if c == 1 else '%s \\times (%s)\\sin %s' % (ftex(c), ftex(-a), angle))]
        if c != 1:
            w.append(('tidy up', '', ans_tex))
    elif st == 4:
        c, a = nums
        if terms[0][0] == 'exp':
            e = 'e^{%s}' % (v if a == 1 else ftex(a) + v)
            w = [('a comes down; the power stays', 'd', ftex(a) + e if c == 1 else '%s \\times %s%s' % (ftex(c), ftex(a), e))]
        else:
            w = [('ln: the a cancels', 'd', '\\dfrac{1}{%s}' % v if c == 1 else '%s \\times \\dfrac{1}{%s}' % (ftex(c), v))]
        if c != 1:
            w.append(('tidy up', '', ans_tex))
    else:
        p = Fraction(terms[0][1])
        c, n = Fraction(terms[1][1]), Fraction(terms[1][2])
        const = len(terms) == 3
        w = [('each term on its own' + ('; a number alone goes to 0' if const else ''), 'd',
              '%s + %s' % (ftex(p), power_down(c, n, v)) + (' + 0' if const else '')),
             ('tidy up', '', ans_tex)]
    return w


def lhs_of(q, side):
    return f_name(q) if side == 'f' else (d_name(q) if side == 'd' else '')


# ---------------------------------------------------------------- the calculus, in sympy
def expr(terms, v):
    """An item's terms as one sympy expression in the positive symbol v."""
    import sympy as sp
    total = sp.Integer(0)
    for t in terms:
        kind, a = t[0], [sp.Rational(s) for s in t[1:]]
        c = a[0]
        if kind == 'const':
            total += c
        elif kind == 'pow':
            total += c * v ** a[1]
        elif kind == 'sin':
            total += c * sp.sin(a[1] * v)
        elif kind == 'cos':
            total += c * sp.cos(a[1] * v)
        elif kind == 'exp':
            total += c * sp.exp(a[1] * v)
        elif kind == 'ln':
            total += c * sp.log(a[1] * v)
        elif kind == 'over':
            total += c / (a[1] * v)
        elif kind == 'overpow':
            total += c / (a[1] * v ** a[2])
        elif kind == 'recipln':
            total += c / sp.log(a[1] * v)
        elif kind == 'xexp':
            total += c * v * sp.exp(a[1] * v - 1)
        else:
            raise ValueError('a term kind this script does not know: %r' % kind)
    return total


def same(a, b):
    import sympy as sp
    return sp.simplify(a - b) == 0


def fvalue(terms, x):
    """An item's terms at the number x, in floating point (for the curves); a ValueError or an overflow is not finite."""
    try:
        s = 0.0
        for t in terms:
            k, a = t[0], [float(Fraction(y)) for y in t[1:]]
            c = a[0]
            if k == 'const':
                s += c
            elif k == 'pow':
                s += c * x ** a[1]
            elif k == 'sin':
                s += c * math.sin(a[1] * x)
            elif k == 'cos':
                s += c * math.cos(a[1] * x)
            elif k == 'exp':
                s += c * math.exp(a[1] * x)
            elif k == 'ln':
                s += c * math.log(a[1] * x)
            elif k == 'over':
                s += c / (a[1] * x)
            elif k == 'overpow':
                s += c / (a[1] * x ** a[2])
            elif k == 'recipln':
                s += c / math.log(a[1] * x)
            elif k == 'xexp':
                s += c * x * math.exp(a[1] * x - 1)
            else:
                return float('nan')
        return s if isinstance(s, float) else float('nan')
    except (ValueError, ZeroDivisionError, OverflowError):
        return float('nan')


class TexReader:
    """This script's own reader of the bank's TeX, into sympy: enough of TeX for a line of this game and no more.
    Numbers, the item's letter, e, + and -, juxtaposition and \\times, ^ with a group or one character, brackets,
    \\frac and \\dfrac, \\sqrt with or without an index, and \\sin, \\cos, \\ln of a multiple of the letter."""
    TOKEN = re.compile(r'\\[a-zA-Z]+|\\,|\d+|[a-zA-Z]|[{}()\[\]^+\-]|\s+|.')

    def __init__(self, tex, v):
        import sympy as sp
        self.sp, self.v, self.tex = sp, v, tex
        self.toks = [t for t in self.TOKEN.findall(tex) if not t.isspace() and t != '\\,']
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def take(self, want=None):
        t = self.peek()
        if t is None or (want is not None and t != want):
            raise ValueError('TeX this script cannot read: %r (at %r, wanted %r)' % (self.tex, t, want))
        self.i += 1
        return t

    def value(self):
        e = self.sum()
        if self.peek() is not None:
            raise ValueError('TeX this script cannot read: %r (at %r)' % (self.tex, self.peek()))
        return e

    def sum(self):
        sign = 1
        if self.peek() in ('+', '-'):
            sign = -1 if self.take() == '-' else 1
        total = sign * self.product()
        while self.peek() in ('+', '-'):
            op = self.take()
            total = total + self.product() if op == '+' else total - self.product()
        return total

    def product(self):
        val, n = self.sp.Integer(1), 0
        while True:
            t = self.peek()
            if t is None or t in ('+', '-', '}', ')', ']'):
                break
            if t == '\\times':
                self.take()
                continue
            val, n = val * self.power(), n + 1
        if not n:
            raise ValueError('TeX this script cannot read: %r (nothing where a term should be)' % self.tex)
        return val

    def power(self):
        base = self.atom()
        if self.peek() == '^':
            self.take()
            base = base ** self.group()
        return base

    def group(self):
        if self.peek() == '{':
            self.take()
            e = self.sum()
            self.take('}')
            return e
        return self.atom()

    def atom(self):
        sp, t = self.sp, self.take()
        if t.isdigit():
            return sp.Integer(int(t))
        if t == self.v.name:
            return self.v
        if t == 'e':
            return sp.E
        if t in ('\\frac', '\\dfrac'):
            top = self.group()
            return top / self.group()
        if t == '\\sqrt':
            k = sp.Integer(2)
            if self.peek() == '[':
                self.take()
                k = self.sum()
                self.take(']')
            return self.group() ** (1 / k)
        if t == '(':
            e = self.sum()
            self.take(')')
            return e
        if t in ('\\sin', '\\cos', '\\ln'):
            mult = sp.Integer(1)
            if self.peek() is not None and (self.peek().isdigit() or self.peek() in ('\\frac', '\\dfrac')):
                mult = self.atom()
            self.take(self.v.name)
            return {'\\sin': sp.sin, '\\cos': sp.cos, '\\ln': sp.log}[t](mult * self.v)
        raise ValueError('TeX this script cannot read: %r (at %r)' % (self.tex, t))


def read_tex(tex, v):
    return TexReader(tex, v).value()


def shape(q):
    """What kind of question the item's terms make, for its stage; None if they are not one of the stage's kinds."""
    t, st = q['q'], q['stage']
    kinds = [x[0] for x in t]
    n = [[Fraction(s) for s in x[1:]] for x in t]
    if st == 1 and kinds == ['pow'] and n[0][1].denominator == 1 and n[0][1] >= 1:
        return 'linear' if n[0][1] == 1 else 'power'
    if st == 2 and kinds == ['pow'] and n[0][1].denominator == 1 and n[0][1] <= -1:
        return 'fraction'
    if st == 2 and kinds == ['pow'] and n[0][1].denominator in (2, 3) and n[0][1] > 0 and n[0][0] >= 1 and n[0][0].denominator == 1:
        return 'root'
    if st == 3 and kinds in (['sin'], ['cos']) and n[0][1] > 1:
        return kinds[0]
    if st == 4 and kinds in (['exp'], ['ln']) and n[0][1] > 1:
        return kinds[0]
    if st == 5 and kinds in (['pow', 'pow'], ['pow', 'pow', 'const']) and n[0][1] == 1 and n[1][1].denominator == 1 and n[1][1] >= 2:
        return 'sum'
    return None


def rows_of(q, kind):
    return {'linear': ['x'], 'power': ['axn'], 'fraction': ['axn'], 'root': ['axn'], 'sin': ['sin'], 'cos': ['cos'],
            'exp': ['exp'], 'ln': ['ln'], 'sum': ['x', 'axn']}[kind]


def slip(q, kind, err, v):
    """The expression the named error gives on this question, worked out here from the question's own terms; None if
    that error has no meaning for this kind of question."""
    import sympy as sp
    t = q['q']
    R = sp.Rational
    c = R(t[0][1])
    k = R(t[0][2]) if len(t[0]) > 2 else None
    if kind == 'power':
        return {'power_kept': c * k * v ** k,                    # multiplied by the power, the power left as it was
                'coeff_lost': k * v ** (k - 1),                  # the number in front dropped
                'new_power_used': c * (k - 1) * v ** (k - 1),    # multiplied by the new power
                }.get(err)
    if kind == 'linear':
        return {'kept_variable': c * v, 'coeff_lost': sp.Integer(1), 'treated_as_constant': sp.Integer(0)}.get(err)
    if kind == 'fraction':
        return {'sign_lost': c * abs(k) * v ** (k - 1),          # the power brought down without its minus
                'power_wrong_way': c * k * v ** (k + 1),         # one added to the power
                'bottom_differentiated': c / sp.diff(v ** (-k), v),   # the bottom differentiated where it stands
                }.get(err)
    if kind == 'root':
        return {'root_upside_down': c * (1 / k) * v ** (1 / k - 1),   # the root's number on top of the power
                'power_kept': c * k * v ** k,
                'power_wrong_way': c * k * v ** (k + 1)}.get(err)
    if kind in ('sin', 'cos'):
        g, s = (sp.cos, 1) if kind == 'sin' else (sp.sin, -1)
        return {'a_forgotten': s * c * g(k * v),                 # the angle's number not brought out
                'sign_slip': -sp.diff(expr(t, v), v),            # the derivative with the wrong sign
                'a_dropped_from_angle': s * c * k * g(v),        # brought out, and lost from the angle
                }.get(err)
    if kind == 'exp':
        return {'a_forgotten': c * sp.exp(k * v),
                'integrated_instead': sp.integrate(expr(t, v), v),
                'power_rule_used': c * k * v * sp.exp(k * v - 1)}.get(err)
    if kind == 'ln':
        return {'a_kept': c * k / v, 'a_divided': c / (k * v), 'ln_flipped': c / sp.log(k * v)}.get(err)
    if kind == 'sum':
        b, n = R(t[1][1]), R(t[1][2])
        right = c + b * n * v ** (n - 1)
        got = {'kept_variable': c * v + b * n * v ** (n - 1),
               'power_kept': c + b * n * v ** n,
               'coeff_lost': c + n * v ** (n - 1)}
        if len(t) == 3:
            got['constant_kept'] = right + R(t[2][1])
        return got.get(err)
    return None


def check_curves(tag, f_terms, d_terms, graph, out):
    """A pair of curves on a window: finite and inside the y-range at every sample, and neither more than READABLE times
    the other's height."""
    try:
        (lo, hi), (ylo, yhi) = graph['x'], graph['y']
    except Exception:  # noqa: BLE001
        out.append('%s: its graph window %r is not {"x": [lo, hi], "y": [lo, hi]}' % (tag, graph))
        return
    if not (lo < hi and ylo < yhi) or graph.get('ticks') not in ('num', 'pi'):
        out.append('%s: its graph window %r is not a window with ticks "num" or "pi"' % (tag, graph))
        return
    top = {}
    for name, terms in (('the function', f_terms), ('the gradient function', d_terms)):
        ys = [fvalue(terms, lo + (hi - lo) * i / SAMPLES) for i in range(SAMPLES + 1)]
        bad = [i for i, y in enumerate(ys) if not math.isfinite(y)]
        if bad:
            out.append('%s: %s is not finite at %g, inside its window' % (tag, name, lo + (hi - lo) * bad[0] / SAMPLES))
            return
        if min(ys) < ylo - 1e-9 or max(ys) > yhi + 1e-9:
            out.append('%s: %s runs from %g to %g, outside its y-range %g to %g' % (tag, name, min(ys), max(ys), ylo, yhi))
        top[name] = max(abs(y) for y in ys)
    a, b = top['the function'], top['the gradient function']
    if not a or not b or max(a / b, b / a) > READABLE + 1e-9:
        out.append('%s: one curve is more than %d times the other\'s height (%g and %g) over its window' % (tag, READABLE, a, b))


# ---------------------------------------------------------------- the bank
def check_bank(html, out, info):
    import sympy as sp
    raw = bank_lines(html)
    digest = hashlib.sha256(''.join(ln + '\n' for ln in raw).encode('utf-8')).hexdigest()
    if digest != SHA256:
        out.append('bank: the item lines hash to %s, the contract says %s' % (digest, SHA256))
    items = [json.loads(ln) for ln in raw]
    if len(items) != 60:
        out.append('bank: %d items, not 60' % len(items))
    count = Counter(q.get('stage') for q in items)
    if count != {n: PER_STAGE for n in range(1, 6)}:
        out.append('bank: items a stage %s, not 12 in each of stages 1 to 5' % dict(count))
    forms = Counter(q.get('form') for q in items)
    if set(forms) != FORMS or set(forms.values()) != {20}:
        out.append('bank: wordings %s, not 20 items in each of wrt, leib and fn' % dict(forms))
    for what in ('id', 'prompt'):
        for val, n in Counter(q.get(what) for q in items).items():
            if n > 1:
                out.append('bank: %s %r appears %d times' % (what, val, n))
    seq = Counter()
    allowed = err_stages()
    lines = lines_of(html)
    used = set()
    for q in items:
        iid = q.get('id')
        try:
            st = q['stage']
            seq[st] += 1
            if iid != 's%d-%02d' % (st, seq[st]):
                out.append('%s: id should be s%d-%02d (its stage, then its place in it)' % (iid, st, seq[st]))
            if q['var'] not in VARS or q['form'] not in FORMS:
                out.append('%s: letter %r or wording %r is not one the game uses' % (iid, q.get('var'), q.get('form')))
                continue
            if q['dep'] != dep_of(q, seq[st]):
                out.append('%s: dependent letter %r, should be %r' % (iid, q.get('dep'), dep_of(q, seq[st])))
            kind = shape(q)
            if kind is None:
                out.append('%s: its terms %s are not a stage %d question' % (iid, q['q'], st))
                continue
            back = st == 2
            if q['back'] is not back:
                out.append('%s: "back" is %r; only Stage 2\'s options are written back in the question\'s form' % (iid, q['back']))
            v = sp.Symbol(q['var'], positive=True)
            qtex = written(q)
            func = expr(q['q'], v)
            if q['qtex'] != qtex:
                out.append('%s: question tex %r, rendered from its terms %r' % (iid, q['qtex'], qtex))
            if not same(read_tex(q['qtex'], v), func):
                out.append('%s: question tex %r does not read back to its terms' % (iid, q['qtex']))
            if q['prompt'] != prompt_of(q, qtex):
                out.append('%s: prompt %r, rebuilt %r' % (iid, q['prompt'], prompt_of(q, qtex)))
            deriv = sp.diff(func, v)
            ans = q['answer']
            if not same(expr(ans['terms'], v), deriv):
                out.append('%s: answer %r is not the derivative, which sympy gives as %s' % (iid, ans['tex'], sp.simplify(deriv)))
            ans_tex = render(ans['terms'], q['var'], back)
            if ans['tex'] != ans_tex:
                out.append('%s: answer tex %r, rendered from its terms %r' % (iid, ans['tex'], ans_tex))
            if len(q['decoys']) != 3:
                out.append('%s: %d decoys, not 3' % (iid, len(q['decoys'])))
            for d in q['decoys']:
                used.add(d['err'])
                if d['err'] not in allowed:
                    out.append('%s: %s is not a key of ERR_STAGES' % (iid, d['err']))
                elif st not in allowed[d['err']]:
                    out.append('%s: %s is not allowed in stage %d' % (iid, d['err'], st))
                if d['tex'] != render(d['terms'], q['var'], back):
                    out.append('%s: decoy %s tex %r, rendered from its terms %r' % (iid, d['err'], d['tex'], render(d['terms'], q['var'], back)))
                want = slip(q, kind, d['err'], v)
                if want is None:
                    out.append('%s: this script has no %s error for a %s question' % (iid, d['err'], kind))
                elif not same(expr(d['terms'], v), want):
                    out.append('%s: decoy %s is %r, recomputed %s' % (iid, d['err'], d['tex'], sp.simplify(want)))
            opts = [ans] + q['decoys']
            if len({d['err'] for d in q['decoys']}) != len(q['decoys']):
                out.append('%s: an error key is used twice' % iid)
            for o in opts:
                if not same(read_tex(o['tex'], v), expr(o['terms'], v)):
                    out.append('%s: option tex %r does not read back to its terms' % (iid, o['tex']))
            for i in range(len(opts)):
                for j in range(i + 1, len(opts)):
                    if opts[i]['tex'] == opts[j]['tex'] or same(expr(opts[i]['terms'], v), expr(opts[j]['terms'], v)):
                        out.append('%s: options %r and %r are equal in value' % (iid, opts[i]['tex'], opts[j]['tex']))
            if q['rows'] != rows_of(q, kind):
                out.append('%s: rows %s, a %s question needs %s' % (iid, q['rows'], kind, rows_of(q, kind)))
            # The working: rebuilt line for line, then every right side read back and held equal to its side.
            work = [{'why': w, 'lhs': lhs_of(q, side), 'rhs': rhs} for w, side, rhs in working_of(q, ans_tex)]
            if q['working'] != work:
                out.append('%s: working %r, rebuilt %r' % (iid, q['working'], work))
            side = None
            for n, w in enumerate(q['working'], 1):
                if w['lhs']:
                    side = 'f' if w['lhs'] == f_name(q) else ('d' if w['lhs'] == d_name(q) else None)
                    if side is None:
                        out.append('%s: working line %d has %r on the left, which is neither %r nor %r' % (iid, n, w['lhs'], f_name(q), d_name(q)))
                        break
                elif side is None:
                    out.append('%s: working line %d carries on from nothing (no left side yet)' % (iid, n))
                    break
                if not same(read_tex(w['rhs'], v), func if side == 'f' else deriv):
                    out.append('%s: working line %d (%s = %s) is not equal to the %s' % (
                        iid, n, w['lhs'] or '...', w['rhs'], 'function' if side == 'f' else 'derivative'))
            if q['working'] and (side != 'd' or q['working'][-1]['rhs'] != ans['tex']):
                out.append('%s: the working does not end on the answer %r' % (iid, ans['tex']))
            check_curves(iid, q['q'], ans['terms'], q['graph'], out)
        except Exception as e:  # noqa: BLE001
            out.append('%s: an item this script cannot read: %s' % (iid, str(e).splitlines()[0][:160]))
    for k in sorted(set(allowed) - set(lines)):
        out.append('lines: no LINES line for %s' % k)
    for k in sorted(set(lines) - set(allowed)):
        out.append('lines: LINES has %s, which ERR_STAGES does not' % k)
    for k in sorted(set(lines) - used):
        out.append('lines: the LINES line for %s is never used by the bank' % k)
    for k, val in lines.items():
        if not val.strip():
            out.append('lines: the LINES line for %s is empty' % k)
    for n, name in enumerate(STAGE_NAMES, 1):
        if not re.search(r'data-stage="%d"><span class="n">%d</span><span><span class="t">%s</span>' % (n, n, re.escape(name)), html):
            out.append('start: stage %d is not named %r' % (n, name))
    check_start_show(html, items, out, info)
    info['bank'] = len(items)
    return items


def start_show(html):
    return [json.loads(ln) for ln in block_lines(html, 'START_SHOW')]


def check_start_show(html, items, out, info):
    """The start screen's pairs: the generator's, each a function and its derivative, none a question in the game."""
    import sympy as sp
    x = sp.Symbol('x', positive=True)
    want = generator_data('START_SHOW')
    pairs = start_show(html)
    if len(pairs) != 3 or len(want) != 3:
        out.append('start screen: %d pairs in the page and %d in the generator, not 3' % (len(pairs), len(want)))
    for n, (p, w) in enumerate(zip(pairs, want), 1):
        tag = 'start screen: pair %d' % n
        try:
            if p['q'] != w['q'] or p['d'] != w['d'] or [float(a) for a in p['graph']['x']] != [float(a) for a in w['x']]:
                out.append('%s is not the generator\'s (%s, %s on %s)' % (tag, w['q'], w['d'], w['x']))
            f, d = expr(p['q'], x), expr(p['d'], x)
            if not same(sp.diff(f, x), d):
                out.append('%s: %r is not the derivative of %r' % (tag, p['dtex'], p['qtex']))
            for q in items:
                near = all(abs(fvalue(p['q'], t) - fvalue(q['q'], t)) < 1e-6 for t in (0.37, 1.7))
                if near and same(f, expr(q['q'], x)):   # the bank's question in the letter x: equal in any letter
                    out.append('%s is a question in the game (%s)' % (tag, q['id']))
            for key, terms in (('qtex', p['q']), ('dtex', p['d'])):
                if p[key] != render(terms, 'x'):
                    out.append('%s: %s %r, rendered from its terms %r' % (tag, key, p[key], render(terms, 'x')))
                if not same(read_tex(p[key], x), expr(terms, x)):
                    out.append('%s: %s %r does not read back to its terms' % (tag, key, p[key]))
            check_curves(tag, p['q'], p['d'], p['graph'], out)
        except Exception as e:  # noqa: BLE001
            out.append('%s: a pair this script cannot read: %s' % (tag, str(e).splitlines()[0][:160]))
    info['show'] = len(pairs)


# ---------------------------------------------------------------- the page
# The page's setTimeout at 1/100 of its length, set before any of its scripts: 30 s of the page's time in 0.3 s.
FAST_CLOCK_INIT = """(() => { const st = window.setTimeout;
  window.setTimeout = function (f, ms) { const a = [].slice.call(arguments, 2); return st.apply(window, [f, (ms || 0) / 100].concat(a)); }; })();"""


def open_page(pw, base, html, size, aa=False, fast=False, still=False):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch,
                         reduced_motion='reduce' if still else 'no-preference')
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(FAST_CLOCK_INIT if fast else bc.NO_NEXT_FLOOR_INIT)   # the fast clock keeps the real floors
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
    page.wait_for_function('!!window.DDX && !!DDX.ui', timeout=15000)
    page.evaluate("""async () => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); };
        if (document.fonts && document.fonts.ready) await document.fonts.ready; }""")
    if aa:
        page.evaluate("document.getElementById('a11yToggle').click()")
        page.evaluate("async () => { if (document.fonts && document.fonts.ready) await document.fonts.ready; }")
    return br, page, errors


# Every TeX string the page can show, rendered by the page's own KaTeX with errors thrown.
KATEX_JS = r"""() => {
  const bad = [], seen = new Set();
  const one = (where, tex) => { if (seen.has(tex)) return; seen.add(tex);
    try { katex.renderToString(tex, { throwOnError: true }); } catch (e) { bad.push(where + ': ' + tex + ' (' + String(e.message).slice(0, 80) + ')'); } };
  const mixed = (where, s) => { const re = /\\\(([\s\S]*?)\\\)/g; let m; while ((m = re.exec(s))) one(where, m[1]); };
  if (typeof katex === 'undefined') return { n: 0, bad: ['KaTeX is not loaded'] };
  for (const q of DDX.bank()) {
    mixed(q.id + ' prompt', q.prompt); one(q.id + ' question', q.qtex); one(q.id + ' answer', q.answer.tex);
    q.decoys.forEach(d => one(q.id + ' decoy ' + d.err, d.tex));
    q.working.forEach(w => { if (w.lhs) one(q.id + ' working', w.lhs); one(q.id + ' working', '{}= ' + w.rhs); });
  }
  DDX.startShow().forEach((p, i) => { one('start pair ' + (i + 1), 'y = ' + p.qtex); one('start pair ' + (i + 1), '\\dfrac{dy}{dx} = ' + p.dtex); });
  DDX.TABLE_HEAD.forEach(h => mixed('table heading', h));
  DDX.TABLE.forEach(r => { mixed('table row ' + r[0], r[1]); mixed('table row ' + r[0], r[2]); });
  return { n: seen.size, bad };
}"""

# What is on screen: the options, the feedback after an answer, the table and the graph.
SCREEN_JS = r"""() => {
  const opts = [...document.querySelectorAll('#opts .opt')].map(b => ({ val: b.dataset.val, cls: b.className, off: b.disabled,
    katex: b.querySelectorAll('.katex').length, shown: b.getBoundingClientRect().height > 0 }));
  const fb = document.querySelector('#feedback .fb');
  const err = fb && fb.querySelector('.fb-err'), head = fb && fb.querySelector('.fb-head');
  const rows = fb && fb.querySelector('.fb-rows');
  const t = document.getElementById('dtable');
  const cell = (el) => { const a = el && el.querySelector('annotation'); return a ? a.textContent : null; };
  const g = DDX.ui.graph(), next = document.querySelector('#feedback .maffs-next');
  return { state: DDX.ui.state(), mode: DDX.ui.mode(), q: DDX.ui.question(), score: DDX.ui.score(), opts,
           why: fb ? fb.dataset.why : null, err: fb ? fb.dataset.err || null : null, errText: err ? err.textContent : null,
           head: head ? head.textContent : null, headTex: head ? cell(head) : null,
           fbText: fb ? fb.textContent : '', oldAnswer: fb ? fb.querySelectorAll('.fb-ans').length : 0,
           worked: fb ? [...fb.querySelectorAll('.worked .w-line')].map(l => ({ why: l.querySelector('.w-why') ? l.querySelector('.w-why').textContent : null,
             lhs: cell(l.querySelector('.w-lhs')), rhs: cell(l.querySelector('.w-rhs')) })) : [],
           rowsHead: rows && rows.querySelector('.fb-rows-h') ? rows.querySelector('.fb-rows-h').textContent : null,
           rows: rows ? [...rows.querySelectorAll('.fb-row[data-row]')].map(r => r.dataset.row) : null,
           rowsTex: rows ? [...rows.querySelectorAll('.fb-row')].map(r => [...r.querySelectorAll('.c')].map(cell)) : null,
           next: !!next, nextOff: next ? next.disabled : null,
           katexErrors: document.querySelectorAll('.katex-error').length,
           tables: document.querySelectorAll('#game table.dt').length,
           graph: { there: g.there, open: g.open, label: g.label, curves: g.plot ? g.plot.curves.map(c => c.id) : null,
                    paths: [...document.querySelectorAll('#dgraph path.maffs-plot-curve')].map(p => p.dataset.curve) },
           table: t ? { open: t.open, shown: t.querySelector('summary').getBoundingClientRect().height > 0,
                        label: [...t.querySelectorAll('summary span')].find(s => s.getBoundingClientRect().height > 0)?.textContent || null,
                        head: [...t.querySelectorAll('thead th')].map(th => [...th.querySelectorAll('annotation')].map(a => a.textContent)),
                        rows: [...t.querySelectorAll('tbody tr')].map(r => [r.dataset.row].concat([...r.querySelectorAll('td')].map(cell))),
                        lit: [...t.querySelectorAll('tbody tr.hl')].map(r => r.dataset.row),
                        cellsShown: t.open ? [...t.querySelectorAll('td')].every(td => td.getBoundingClientRect().height > 0) : null } : null };
}"""
PRESS_JS = r"""(val) => { const b = [...document.querySelectorAll('#opts .opt')].find(x => x.dataset.val === val); if (!b) return false; b.click(); return true; }"""


def tex_in(s):
    """The TeX inside each \\( \\) of a mixed string, in order."""
    return re.findall(r'\\\((.*?)\\\)', s, re.S)


def check_table(tag, s, size, out, lit):
    """A question's table: there, the contract's, open from 1024 px, and only these rows lit; or, in Pro, not there."""
    pro = s['mode'].startswith('pro-')
    t = s['table']
    if pro:
        if t is not None or (s['state'] == 'asking' and s['tables']):
            out.append('%s: the table is in the page during a Pro question' % tag)
        return
    if t is None or not t['shown']:
        out.append('%s: no table on screen (Pro is off)' % tag)
        return
    if t['open'] != (size[0] >= WIDE):
        out.append('%s: the table is %s at %dx%d (open from 1024 px wide, a closed panel on anything narrower)' % ((tag, 'open' if t['open'] else 'closed') + size))
    if t['label'] != 'Derivative table':
        out.append('%s: the table\'s panel is labelled %r' % (tag, t['label']))
    if t['head'] != [tex_in(h) for h in TABLE_HEAD] or t['rows'] != [[r[0]] + tex_in(r[1]) + tex_in(r[2]) for r in TABLE]:
        out.append('%s: the table is not the contract\'s (headings %s, rows %s)' % (tag, t['head'], t['rows']))
    if t['open'] and not t['cellsShown']:
        out.append('%s: the open table has a row that is not showing' % tag)
    if t['lit'] != lit:
        out.append('%s: the table\'s lit rows are %s, should be %s' % (tag, t['lit'], lit))


def check_graph_panel(tag, s, size, out, answered, opened=False):
    """The graph's panel on a question: there (Pro or not), open from 1024 px, the function alone until the answer and
    the function and the gradient function after it; its closed button says which."""
    g = s['graph']
    want = ['f', 'd'] if answered else ['f']
    if not g['there']:
        out.append('%s: no graph in the page' % tag)
        return
    if g['open'] != (size[0] >= WIDE or opened):
        out.append('%s: the graph\'s panel is %s at %dx%d (open from 1024 px wide, closed until the student opens it on anything narrower)' % ((tag, 'open' if g['open'] else 'closed') + size))
    if g['label'] != ('See the gradient function' if answered else 'Graph'):
        out.append('%s: the graph\'s button reads %r %s' % (tag, g['label'], 'after an answer' if answered else 'while the question stands'))
    if g['curves'] != want or g['paths'] != want:
        out.append('%s: the graph holds %s (the page draws %s), should be %s' % (tag, g['curves'], g['paths'], want))


def play(page, m, lines, size, out):
    st = int(m[-1])
    pro = m.startswith('pro-')
    page.evaluate('() => { window.__ev = []; window.__sub = []; }')
    # Through the start screen itself: the Pro switch set as the run needs, then the stage's own button.
    if page.evaluate("document.getElementById('proBtn').getAttribute('aria-pressed') === 'true'") != pro:
        page.evaluate("document.getElementById('proBtn').click()")
    page.evaluate("(n) => document.querySelector('#stageList .stage-btn[data-stage=\"' + n + '\"]').click()", st)
    seen, right = [], 0
    for k in range(PER):
        s = page.evaluate(SCREEN_JS)
        q = s['q']
        tag = '%s question %d (%s) at %dx%d' % ((m, k + 1, q and q['id']) + size)
        if s['state'] != 'asking' or not q:
            out.append('%s: no question on screen (state %s)' % (tag, s['state']))
            return
        if s['mode'] != m:
            out.append('%s: the run is on board %s' % (tag, s['mode']))
        seen.append(q['id'])
        if q['stage'] != st:
            out.append('%s: a stage %d item' % (tag, q['stage']))
        want = sorted([q['answer']['tex']] + [d['tex'] for d in q['decoys']])
        if sorted(o['val'] for o in s['opts']) != want or len(s['opts']) != 4 or any(o['katex'] < 1 for o in s['opts']):
            out.append('%s: options %s, should be the four %s, each button\'s dataset.val the bank\'s tex and its label KaTeX' % (tag, [(o['val'], o['katex']) for o in s['opts']], want))
        if s['katexErrors']:
            out.append('%s: KaTeX shows %d error(s)' % (tag, s['katexErrors']))
        check_table(tag, s, size, out, [])
        check_graph_panel(tag, s, size, out, answered=False)
        opened = False
        if k % 2 == 0:
            page.evaluate(PRESS_JS, q['answer']['tex'])
            a = page.evaluate(SCREEN_JS)
            right += 1
            if a['why'] != 'right' or not (a['head'] or '').startswith('Right: ') or a['headTex'] != q['answer']['tex']:
                out.append('%s: the right answer shows %r (%s), not "Right: " and the answer' % (tag, a['head'], a['why']))
            if a['state'] != 'done' or not a['next']:
                out.append('%s: a right answer does not wait on Next (state %s)' % (tag, a['state']))
                return
        else:
            d = q['decoys'][(k // 2) % 3]
            page.evaluate(PRESS_JS, d['tex'])
            a = page.evaluate(SCREEN_JS)
            check_wrong(tag, q, d, a, lines, out)
            check_table(tag, a, size, out, [r[0] for r in TABLE if r[0] in q['rows']])
            if a['score'] != right:
                out.append('%s: a wrong answer changed the score to %d' % (tag, a['score']))
            if size[0] < WIDE and k == 1:
                # The student opens the fold-out to see the gradient function; Next must close it again.
                page.evaluate("document.querySelector('#dgraph summary').click()")
                a = page.evaluate(SCREEN_JS)
                opened = True
        check_graph_panel(tag, a, size, out, answered=True, opened=opened)
        page.evaluate('DDX.ui.next()')
        if page.evaluate('DDX.ui.state()') not in ('asking', 'over'):
            out.append('%s: Next did not move on' % tag)
            return
    tag = '%s at %dx%d' % ((m,) + size)
    if page.evaluate('DDX.ui.state()') != 'over':
        out.append('%s: the run did not finish after %d questions' % (tag, PER))
        return
    if len(set(seen)) != PER:
        out.append('%s: the run served %s, not %d different items' % (tag, seen, PER))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    started = [p for n, p in ev if n == 'game_started']
    if len(started) != 1 or started[0].get('mode') != m or started[0].get('level') != 'level3':
        out.append('%s: game_started %s, expected one with mode %s, level level3' % (tag, started, m))
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('mode') != m or done[0].get('level') != 'level3':
        out.append('%s: game_completed %s, expected one with score %d, mode %s, level level3' % (tag, done, right, m))
    if sub != [[SLUG, m, right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d of %d' % (tag, sub, m, right, PER))
    qa = [p for n, p in ev if n == 'question_answered']
    if [p.get('question_id') for p in qa] != seen or [p.get('correct') for p in qa] != [k % 2 == 0 for k in range(PER)] or any(p.get('mode') != m for p in qa):
        out.append('%s: question_answered events %s do not match the run' % (tag, [(p.get('question_id'), p.get('correct'), p.get('mode')) for p in qa]))
    extra = sorted({n for n, _ in ev} - EVENTS)
    if extra:
        out.append('%s: events the contract does not allow: %s' % (tag, extra))
    shown = page.evaluate("() => ({ score: document.getElementById('resScore').textContent, of: document.getElementById('resOf').textContent, on: document.getElementById('results').classList.contains('active'), graph: !!document.getElementById('dgraph') })")
    if not shown['on'] or shown['score'] != str(right) or shown['of'] != 'out of %d' % PER:
        out.append('%s: the results screen shows %s, expected %d out of %d' % (tag, shown, right, PER))
    if shown['graph']:
        out.append('%s: the graph is still in the page on the results screen' % tag)
    page.evaluate("document.getElementById('menuBtn').click()")


def check_wrong(tag, q, d, a, lines, out):
    """A wrong answer's screen: the chosen option's own line, the working, the table rows, Next, the marks."""
    if a['why'] != 'wrong':
        out.append('%s: %r is marked %s, not wrong' % (tag, d['tex'], a['why']))
        return
    if a['err'] != d['err'] or a['errText'] != lines.get(d['err']):
        out.append('%s: choosing %r (%s) shows the line %r, not the LINES line for %s' % (tag, d['tex'], d['err'], a['errText'], d['err']))
    if a['oldAnswer'] or 'The answer is' in a['fbText']:
        out.append('%s: a wrong answer still shows a "The answer is" line' % tag)
    want = [{'why': w['why'], 'lhs': w['lhs'] or None, 'rhs': '{}= ' + w['rhs']} for w in q['working']]
    if a['worked'] != want:
        out.append('%s: the working shown is %s, the item\'s is %s' % (tag, a['worked'], want))
    want = [r[0] for r in TABLE if r[0] in q['rows']]
    if a['rowsHead'] != 'From the table:' or a['rows'] != want or a['rowsTex'] != [tex_in(r[1]) + tex_in(r[2]) for r in TABLE if r[0] in q['rows']]:
        out.append('%s: the table rows shown are %s under %r, should be %s under "From the table:"' % (tag, a['rows'], a['rowsHead'], want))
    if a['katexErrors']:
        out.append('%s: KaTeX shows %d error(s)' % (tag, a['katexErrors']))
    if not a['next']:
        out.append('%s: no Next after a wrong answer' % tag)
    marks = {o['val']: o['cls'] for o in a['opts']}
    if 'is-wrong' not in marks.get(d['tex'], '') or 'is-right' not in marks.get(q['answer']['tex'], '') or not all(o['off'] for o in a['opts']):
        out.append('%s: the chosen option is not marked wrong, the answer right and every option locked (%s)' % (tag, marks))


def check_switch(page, size, out):
    """The Pro switch: a button with aria-pressed, off on load, labelled as the contract says, and stored nowhere."""
    s = page.evaluate("""() => { const b = document.getElementById('proBtn'); const before = b ? b.getAttribute('aria-pressed') : null;
        const keys = () => { const k = []; for (let i = 0; i < localStorage.length; i++) k.push(localStorage.key(i)); for (let i = 0; i < sessionStorage.length; i++) k.push(sessionStorage.key(i)); return k.sort(); };
        const k0 = keys(); if (b) b.click(); const on = b ? b.getAttribute('aria-pressed') : null; const k1 = keys(); if (b) b.click();
        return { tag: b ? b.tagName : null, label: b ? b.textContent : null, before, on, after: b ? b.getAttribute('aria-pressed') : null,
                 stored: JSON.stringify(k0) !== JSON.stringify(k1), cookie: document.cookie, table: !!document.getElementById('dtable') }; }""")
    if s['tag'] != 'BUTTON' or s['label'] != 'Pro: no table' or s['before'] != 'false' or s['on'] != 'true' or s['after'] != 'false':
        out.append('switch at %dx%d: the Pro switch is %s' % (size + (s,)))
    if s['stored']:
        out.append('switch at %dx%d: pressing the Pro switch stores something' % size)
    if s['table']:
        out.append('switch at %dx%d: the table is in the page on the start screen' % size)


# ---------------------------------------------------------------- waiting for Next, on a fast clock
def check_waits(page, size, out):
    """A right answer never moves on by itself: 30 s of the page's time (0.3 s on the fast clock), then Enter; then
    Space; then a wrong answer, which waits the same."""
    page.evaluate("DDX.ui.start('stage-1')")
    for n, (right, key) in enumerate([(True, 'Enter'), (True, 'Space'), (False, 'Enter')], 1):
        what = 'a right answer' if right else 'a wrong answer'
        q = page.evaluate('DDX.ui.question()')
        tag = 'waits at %dx%d, question %d (%s)' % (size + (n, q and q['id']))
        if not q or page.evaluate('DDX.ui.state()') != 'asking':
            out.append('%s: no question on screen' % tag)
            return
        page.evaluate('(r) => DDX.ui.answer(r)', right)
        page.wait_for_timeout(330)                      # 33 s of the page's timers
        s = page.evaluate("() => { const b = document.querySelector('#feedback .maffs-next'); const q = DDX.ui.question(); "
                          "return { state: DDX.ui.state(), id: q && q.id, next: !!b, off: b ? b.disabled : null, d: (DDX.ui.graph().plot || { curves: [] }).curves.map(c => c.id) }; }")
        if s['state'] != ('done' if right else 'wrong') or s['id'] != q['id']:
            out.append('%s: %s moved on by itself within 30 s (state %s, item %s)' % (tag, what, s['state'], s['id']))
            return
        if not s['next'] or s['off']:
            out.append('%s: after %s, Next is %s' % (tag, what, 'still held 30 s on' if s['next'] else 'not there'))
            return
        if s['d'] != ['f', 'd']:
            out.append('%s: after %s the graph holds %s, not the function and the gradient function' % (tag, what, s['d']))
        page.keyboard.press(key)
        try:
            page.wait_for_function('(id) => DDX.ui.state() === "asking" && DDX.ui.question().id !== id', arg=q['id'], timeout=3000)
        except Exception:  # noqa: BLE001
            out.append('%s: %s did not advance after %s' % (tag, key, what))
            return


# ---------------------------------------------------------------- the graph, read back from the page
# The graph's own parts: each curve's path with the data it carries, each label, the axis letters, the size on screen.
READ_GRAPH = r"""
  const readGraph = (host) => {
    const svg = host && host.querySelector('svg.maffs-plot-svg');
    const tex = (n) => { const a = n.querySelector('annotation'); return a ? a.textContent : n.textContent; };
    const behind = (e) => { for (; e; e = e.parentElement) { const c = getComputedStyle(e).backgroundColor; if (c && c !== 'transparent' && !/, 0\)$/.test(c)) return c; } return 'rgb(255, 255, 255)'; };
    if (!svg) return null;
    const r = svg.getBoundingClientRect();
    return { width: r.width, viewBox: svg.getAttribute('viewBox'), bg: behind(svg),
      paths: [...svg.querySelectorAll('path')].map(p => { const cs = getComputedStyle(p); return { id: p.dataset.curve || null, tone: p.dataset.tone, d: p.getAttribute('d') || '',
        x0: +p.dataset.x0, x1: +p.dataset.x1, y0: +p.dataset.y0, y1: +p.dataset.y1, box: (p.dataset.box || '').split(' ').map(Number),
        progress: +p.dataset.progress, samples: +p.dataset.samples, stroke: cs.stroke, wide: parseFloat(cs.strokeWidth) }; }),
      tips: [...svg.querySelectorAll('.maffs-plot-tip')].map(c => ({ id: c.dataset.curve, x: +c.dataset.x, cx: +c.getAttribute('cx'), cy: +c.getAttribute('cy'), shown: c.getAttribute('display') !== 'none' })),
      names: [...host.querySelectorAll('.maffs-plot-name')].map(n => ({ id: n.dataset.curve, tex: tex(n), on: n.classList.contains('is-on') })),
      letters: Object.fromEntries([...host.querySelectorAll('.maffs-plot-letter')].map(n => [n.dataset.axis, tex(n)])) };
  };
"""
GRAPH_JS = r"""async ([id, val, pro, wait]) => {""" + READ_GRAPH + r"""
  DDX.ui.preview(id, pro);
  const frame = () => new Promise(r => requestAnimationFrame(() => r()));
  await frame(); await frame();
  const host = document.getElementById('dgraph');
  if (!host) return null;
  const panel = () => { const g = DDX.ui.graph(); return { open: g.open, label: g.label }; };
  const asking = { panel: panel(), graph: readGraph(host) };
  const b = [...document.querySelectorAll('#opts .opt')].find(x => x.dataset.val === val);
  if (!b) return { asking, answered: null };
  b.click();
  await frame();
  const closed = !host.open;
  const at = panel();
  if (closed) host.querySelector('summary').click();        // a narrow screen: the student opens it
  await frame(); await frame();
  const first = readGraph(host);
  let drew = null;
  if (wait) {                                               // the gradient function draws in, and finishes
    const t0 = performance.now();
    const p = () => { const d = host.querySelector('path[data-curve="d"]'); return d ? +d.dataset.progress : -1; };
    while (p() < 1 && performance.now() - t0 < 3000) await frame();
    drew = { start: (first.paths.find(x => x.id === 'd') || {}).progress, end: p(), ms: performance.now() - t0 };
  }
  return { asking, answered: { panel: at, graph: readGraph(host), drew, state: DDX.ui.state() } };
}"""


def path_points(d):
    return [(float(a), float(b)) for a, b in re.findall(r'[ML]\s*(-?\d+(?:\.\d+)?)[ ,](-?\d+(?:\.\d+)?)', d)]


def luminance(css):
    rgb = [int(float(x)) / 255 for x in re.findall(r'[\d.]+', css)[:3]]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_curve(tag, what, p, terms, window, width, out):
    """One drawn curve against the terms it should be the graph of. Every point of the path is mapped back to (x, y)
    through the path's own data attributes; it must be within 1 px of the value worked out here, the path must span the
    window in one unbroken line and hold at least one point for every 2 px of its width on screen."""
    if [p['x0'], p['x1'], p['y0'], p['y1']] != [float(window['x'][0]), float(window['x'][1]), float(window['y'][0]), float(window['y'][1])]:
        out.append('%s: %s is drawn on the window %s, the item\'s is %s' % (tag, what, [p['x0'], p['x1'], p['y0'], p['y1']], window))
        return None
    if len(p['box']) != 4 or not width:
        out.append('%s: %s carries no plot box, or the graph has no width on screen' % (tag, what))
        return None
    left, top, w, h = p['box']
    scale = width / 480.0                                   # CSS px for one viewBox unit
    pts = path_points(p['d'])
    need = math.ceil(w * scale / 2)
    if len(pts) < max(need, 2) or p['d'].count('M') != 1:
        out.append('%s: %s has %d points in %d piece(s); it needs one unbroken line of at least %d (one for every 2 px)' % (tag, what, len(pts), p['d'].count('M'), need))
        return None
    if abs(pts[0][0] - left) > 0.02 or abs(pts[-1][0] - (left + w)) > 0.02 or any(b[0] <= a[0] for a, b in zip(pts, pts[1:])):
        out.append('%s: %s does not run left to right across the whole window (from %g to %g of %g to %g)' % (tag, what, pts[0][0], pts[-1][0], left, left + w))
        return None
    worst = 0.0
    for px, py in pts:
        x = p['x0'] + (px - left) / w * (p['x1'] - p['x0'])
        y = fvalue(terms, x)
        want = top + (p['y1'] - y) / (p['y1'] - p['y0']) * h
        worst = max(worst, abs(py - want) * scale) if math.isfinite(want) else float('inf')
    return worst


def check_graphs(page, items, size, lines, out, info):
    """Every item's graph: the function with the question, the function and the gradient function after a wrong answer."""
    worst, n = 0.0, 0
    for k, q in enumerate(items):
        d = q['decoys'][k % 3]
        tag = '%s at %dx%d, graph' % ((q['id'],) + size)
        r = page.evaluate(GRAPH_JS, [q['id'], d['tex'], k % 2 == 1, k % PER_STAGE == 0])
        n += 1
        if r is None or r['asking']['graph'] is None:
            out.append('%s: no graph in the page with the question' % tag)
            continue
        a = r['asking']
        wide = size[0] >= WIDE
        if a['panel']['open'] != wide or a['panel']['label'] != 'Graph':
            out.append('%s: with the question its panel is %s and reads %r (open from 1024 px, a closed "Graph" button on anything narrower)' % (tag, 'open' if a['panel']['open'] else 'closed', a['panel']['label']))
        g = a['graph']
        if [p['id'] for p in g['paths']] != ['f']:
            out.append('%s: with the question it draws %s, not the function alone' % (tag, [p['id'] for p in g['paths']]))
        if [(x['id'], x['tex']) for x in g['names']] != [('f', f_name(q))] or g['letters'] != {'x': q['var'], 'y': q['dep']}:
            out.append('%s: the curve is labelled %s and the axes %s; the prompt names %r, the letters are %r and %r' % (tag, [(x['id'], x['tex']) for x in g['names']], g['letters'], f_name(q), q['var'], q['dep']))
        b = r['answered']
        if b is None:
            out.append('%s: the option %r is not on screen' % (tag, d['tex']))
            continue
        if b['state'] != 'wrong' or b['panel']['label'] != 'See the gradient function':
            out.append('%s: after a wrong answer (state %s) its button reads %r' % (tag, b['state'], b['panel']['label']))
        g = b['graph']
        if g is None or [p['id'] for p in g['paths']] != ['f', 'd'] or g['tips']:
            out.append('%s: after an answer it draws %s, not the function and the gradient function and nothing else' % (tag, g and [p['id'] for p in g['paths']]))
            continue
        if [(x['id'], x['tex']) for x in g['names']] != [('f', f_name(q)), ('d', d_name(q))]:
            out.append('%s: after an answer the curves are labelled %s, should be %r and %r' % (tag, [(x['id'], x['tex']) for x in g['names']], f_name(q), d_name(q)))
        f, dv = g['paths']
        for what, p, terms, miss in (('the function\'s curve', f, q['q'], 'is not the function'), ('the gradient function\'s curve', dv, q['answer']['terms'], 'is not the answer\'s')):
            off = check_curve(tag, what, p, terms, q['graph'], g['width'], out)
            if off is not None and off > 1.0:
                out.append('%s: %s %s: it is up to %.1f px from it' % (tag, what, miss, off))
            elif off is not None:
                worst = max(worst, off)
        if not (dv['wide'] > f['wide']) and not (dv['wide'] < f['wide']):
            out.append('%s: the two curves are the same width (%s px): they differ by colour alone' % (tag, f['wide']))
        for what, p in (('the function', f), ('the gradient function', dv)):
            if contrast(p['stroke'], g['bg']) < 3.0:
                out.append('%s: %s is drawn in %s on %s, a contrast of %.2f:1 (3:1 or better)' % (tag, what, p['stroke'], g['bg'], contrast(p['stroke'], g['bg'])))
        if b['drew'] is not None:
            w = b['drew']
            if not (w['start'] is not None and w['start'] < 1) or w['end'] != 1:
                out.append('%s: the gradient function did not draw in (progress %s at first, %s after %d ms)' % (tag, w['start'], w['end'], w['ms']))
    info.setdefault('graphs', []).append((size, n, worst))


# ---------------------------------------------------------------- the start screen: the pens
PENS_JS = r"""() => {""" + READ_GRAPH + r"""
  const s = DDX.ui.show(), host = document.getElementById('startPlot');
  const cell = (id) => { const a = document.getElementById(id).querySelector('annotation'); return a ? a.textContent : null; };
  return { pair: s.pair, written: s.written, plot: s.plot, graph: readGraph(host), eqs: [cell('startEqF'), cell('startEqD')],
           shown: getComputedStyle(document.getElementById('startEqs')).visibility === 'visible', now: performance.now() };
}"""
HIDE_JS = "() => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => true }); document.dispatchEvent(new Event('visibilitychange')); }"
SHOW_JS = "() => { delete document.hidden; document.dispatchEvent(new Event('visibilitychange')); }"


def check_pair_curves(tag, s, pair, out):
    g = s['graph']
    if g is None or [p['id'] for p in g['paths']] != ['f', 'd']:
        out.append('%s: the picture draws %s, not a function and its gradient function' % (tag, g and [p['id'] for p in g['paths']]))
        return False
    for what, p, terms in (('the function\'s curve', g['paths'][0], pair['q']), ('the gradient function\'s curve', g['paths'][1], pair['d'])):
        off = check_curve(tag, what, p, terms, pair['graph'], g['width'], out)
        if off is not None and off > 1.0:
            out.append('%s: %s is up to %.1f px from the pair\'s own' % (tag, what, off))
    return True


def check_pens(page, pairs, size, out, info):
    tag = 'pens at %dx%d' % size
    page.evaluate('DDX.ui.showPair(0)')
    seen, s, t_land = [], None, None
    t0 = time.monotonic()
    while time.monotonic() - t0 < DRAW_S + 10:
        s = page.evaluate(PENS_JS)
        if s['pair'] != 0 or not s['plot']:
            out.append('%s: the first pair is not the one drawing (pair %s)' % (tag, s['pair']))
            return
        g = s['graph']
        if not s['plot']['landed'] and g and len(g['tips']) == 2 and [p['id'] for p in g['paths']] == ['f', 'd']:
            a, b = g['tips']
            p = [x['progress'] for x in g['paths']]
            seen.append(p[0])
            if a['x'] != b['x'] or abs(a['cx'] - b['cx']) > 0.011 or p[0] != p[1]:
                out.append('%s: the two pens are not at the same x (%s and %s, progress %s)' % (tag, a['x'], b['x'], p))
                return
            for tip, path, terms in ((a, g['paths'][0], pairs[0]['q']), (b, g['paths'][1], pairs[0]['d'])):
                left, top, w, h = path['box']
                y = fvalue(terms, tip['x'])
                want = top + (path['y1'] - y) / (path['y1'] - path['y0']) * h
                inside = path['y0'] <= y <= path['y1']
                if tip['shown'] != inside or (inside and abs(tip['cy'] - want) * g['width'] / 480.0 > 1.0) or abs(tip['cx'] - (left + w * p[0])) > 0.6:
                    out.append('%s: the %s pen is not on its curve at x = %g (drawn at %s, %s; its curve is at %.2f)' % (tag, tip['id'], tip['x'], tip['cx'], tip['cy'], want))
                    return
            if s['written'] or s['shown']:
                out.append('%s: the equations are written before the pens have finished' % tag)
                return
        if s['plot']['landed']:
            t_land = time.monotonic() - t0
            break
        page.wait_for_timeout(140)
    if t_land is None or len([p for p in seen if 0 < p < 1]) < 10 or seen != sorted(seen):
        out.append('%s: the first pair was not seen drawing left to right and finishing (%d readings, finished after %s s)' % (tag, len(seen), t_land))
        return
    # Never quicker than its time; a slow machine draws fewer frames and may take longer, so only the page's own figure is exact.
    declared = page.evaluate('[DDX.SHOW_DRAW_MS, DDX.SHOW_HOLD_MS]')
    if declared != [DRAW_S * 1000, HOLD_S * 1000] or t_land < DRAW_S - 1.0:
        out.append('%s: the first pair took %.1f s to draw and the page says %s ms (about %g s drawing, %g s still)' % (tag, t_land, declared, DRAW_S, HOLD_S))
    g = s['graph']
    want = ['y = ' + pairs[0]['qtex'], '\\dfrac{dy}{dx} = ' + pairs[0]['dtex']]
    if g['tips'] or not s['written'] or not s['shown'] or s['eqs'] != want:
        out.append('%s: when the pens finish there should be no pens and %s written under the graph (pens %d, written %s, %s)' % (tag, want, len(g['tips']), s['written'], s['eqs']))
    if [(n['id'], n['tex'], n['on']) for n in g['names']] != [('f', 'y', True), ('d', '\\dfrac{dy}{dx}', True)] or g['letters'] != {'x': 'x', 'y': 'y'}:
        out.append('%s: the finished curves are labelled %s on axes %s' % (tag, g['names'], g['letters']))
    check_pair_curves(tag + ', pair 1', s, pairs[0], out)
    # The next pair, about 3 s after the first finished.
    try:
        page.wait_for_function('DDX.ui.show().pair === 1', timeout=int((HOLD_S + 10) * 1000))
    except Exception:  # noqa: BLE001
        out.append('%s: the second pair did not start within %.1f s of the first finishing' % (tag, HOLD_S + 10))
        return
    held = time.monotonic() - t0 - t_land
    if held < HOLD_S - 1.0:
        out.append('%s: the finished pair was left %.1f s (about %g s)' % (tag, held, HOLD_S))
    # A hidden tab: the drawing stops where it is, and carries on when the tab shows again.
    page.wait_for_timeout(500)
    page.evaluate(HIDE_JS)
    page.wait_for_timeout(250)
    p1 = page.evaluate(PENS_JS)['graph']['paths'][0]['progress']
    page.wait_for_timeout(500)
    p2 = page.evaluate(PENS_JS)['graph']['paths'][0]['progress']
    page.evaluate(SHOW_JS)
    page.wait_for_timeout(500)
    p3 = page.evaluate(PENS_JS)['graph']['paths'][0]['progress']
    if not (0 < p1 < 1) or p2 != p1 or not p3 > p2:
        out.append('%s: a hidden tab should stop the drawing and a shown one carry on (progress %s, %s while hidden, %s after)' % (tag, p1, p2, p3))
    check_pair_curves(tag + ', pair 2', page.evaluate(PENS_JS), pairs[1], out)
    # The third pair, and round again to the first.
    page.evaluate('DDX.ui.showPair(2)')
    check_pair_curves(tag + ', pair 3', page.evaluate(PENS_JS), pairs[2], out)
    try:
        page.wait_for_function('DDX.ui.show().pair === 0', timeout=int((DRAW_S + HOLD_S + 20) * 1000))
    except Exception:  # noqa: BLE001
        out.append('%s: the third pair was not followed by the first again' % tag)
    info['pens'] = (len(seen), t_land, held)


def check_still(page, pairs, items, size, out, info):
    """prefers-reduced-motion: the first pair finished and still; a gradient function drawn at once."""
    tag = 'reduced motion at %dx%d' % size
    s = page.evaluate(PENS_JS)
    g = s['graph']
    ok = (s['pair'] == 0 and g and not g['tips'] and [p['progress'] for p in g['paths']] == [1, 1] and s['written'] and s['shown']
          and s['eqs'] == ['y = ' + pairs[0]['qtex'], '\\dfrac{dy}{dx} = ' + pairs[0]['dtex']] and all(n['on'] for n in g['names']) and len(g['names']) == 2)
    if not ok:
        out.append('%s: the start screen should show the first pair finished, with its labels and equations and no pens (pair %s, %s)' % (tag, s['pair'], g and [(p['id'], p['progress']) for p in g['paths']]))
    else:
        check_pair_curves(tag, s, pairs[0], out)
    page.wait_for_timeout(int((HOLD_S + 0.8) * 1000))
    s = page.evaluate(PENS_JS)
    if s['pair'] != 0 or s['graph']['tips'] or [p['progress'] for p in s['graph']['paths']] != [1, 1]:
        out.append('%s: the picture moved on (pair %s)' % (tag, s['pair']))
    q = items[0]
    r = page.evaluate(GRAPH_JS, [q['id'], q['answer']['tex'], False, True])
    d = r and r['answered'] and r['answered']['drew']
    if not d or d['start'] != 1 or d['end'] != 1:
        out.append('%s: after an answer the gradient function should be there at once (%s)' % (tag, d))
    info['still'] = True


# ---------------------------------------------------------------- fit
# One item's screens, measured in page coordinates once the layout has settled: the asking screen (ask), then the screen
# after pressing the option `val` (the answer, or a wrong option).
FIT_JS = r"""async ([id, val, pro, ask]) => {
  DDX.ui.preview(id, pro);
  const frame = () => new Promise(r => requestAnimationFrame(() => r()));
  await frame();
  const box = (el) => { if (!el) return null; const y = window.scrollY, r = el.getBoundingClientRect(); return r.width && r.height ? [Math.round(r.top + y), Math.round(r.bottom + y)] : null; };
  const px = (el, k) => parseFloat(getComputedStyle(el)[k]);
  const all = [...document.querySelectorAll('#opts .opt')];
  const b = all.find(x => x.dataset.val === val);
  if (!b) return null;
  const host = document.getElementById('dgraph');
  let asking = null;
  if (ask) {
    await frame();
    const k = all[0].querySelector('.katex');
    asking = { prompt: box(document.getElementById('ask')), opts: all.map(box), graph: box(host), graphOpen: !!(host && host.open),
               maths: k ? px(k, 'fontSize') / px(document.body, 'fontSize') : 0,
               wide: document.documentElement.scrollWidth, view: document.documentElement.clientWidth };
  }
  b.click();
  await frame(); await frame();
  const fb = document.querySelector('#feedback .fb');
  const marked = [...document.querySelectorAll('#opts .opt.is-wrong, #opts .opt.is-right')].map(box);
  const left = (el) => Math.round(el.getBoundingClientRect().left * 10) / 10;
  const lines = fb ? [...fb.querySelectorAll('.w-line')].map(l => { const w = l.querySelector('.w-why').getBoundingClientRect(), r = l.querySelector('.w-rhs').getBoundingClientRect();
    return { eq: left(l.querySelector('.w-rhs')), whyRight: w.right, whyBottom: w.bottom, whyTop: w.top, rhsLeft: r.left, rhsTop: r.top, rhsBottom: r.bottom }; }) : [];
  const out = { fold: window.innerHeight - 40, wide: document.documentElement.scrollWidth, view: document.documentElement.clientWidth,
           why: fb ? fb.dataset.why : null, err: fb ? fb.dataset.err || null : null, errText: fb && fb.querySelector('.fb-err') ? fb.querySelector('.fb-err').textContent : null,
           table: !!document.getElementById('dtable'), asking, lines,
           graph: box(host), graphOpen: !!(host && host.open),
           parts: { 'the prompt': box(document.getElementById('ask')), 'the "Right" line': box(fb && fb.querySelector('.fb-head')), 'the line': box(fb && fb.querySelector('.fb-err')),
                    'the working': box(fb && fb.querySelector('.worked')),
                    'the table rows': box(fb && fb.querySelector('.fb-rows')),
                    'Next': box(document.querySelector('#feedback .maffs-next')) },
           marked, nextOpen: null };
  if (host && !host.open) {                                 // the student opens the graph's fold-out: Next must not move
    host.open = true;
    await frame();
    out.nextOpen = box(document.querySelector('#feedback .maffs-next'));
    out.graphOpened = box(host);
    host.open = false;
  }
  return out;
}"""


def check_fit(page, items, size, aa, pro, lines, out, info):
    worst, n = None, 0
    mode = '%s, %s' % ('Aa' if aa else 'normal', 'Pro' if pro else 'with the table')
    wide = size[0] >= WIDE
    for q in items:
        for k, d in enumerate([q['answer']] + q['decoys']):
            right = k == 0
            tag = '%s, choosing %r (%s), at %dx%d %s' % (q['id'], d['tex'], 'the answer' if right else d['err'], size[0], size[1], mode)
            r = page.evaluate(FIT_JS, [q['id'], d['tex'], pro, right])
            n += 1
            if r is None:
                out.append('%s: that option is not on screen' % tag)
                continue
            fold = r['fold']
            if r['table'] == pro:
                out.append('%s: the table is %s' % (tag, 'in the page during a Pro question' if pro else 'not in the page'))
            if r['wide'] > r['view']:
                out.append('%s: the page scrolls sideways (%d px wide in %d)' % (tag, r['wide'], r['view']))
            a = r['asking']
            if a is not None:
                atag = '%s, the question, at %dx%d %s' % (q['id'], size[0], size[1], mode)
                if a['prompt'] is None or a['prompt'][0] < 0 or len(a['opts']) != 4 or any(o is None or o[1] > fold for o in a['opts']):
                    out.append('%s: the prompt and all four options are not on screen above the fold at %d px (prompt %s, options %s)' % (atag, fold, a['prompt'], a['opts']))
                if a['wide'] > a['view']:
                    out.append('%s: the page scrolls sideways (%d px wide in %d)' % (atag, a['wide'], a['view']))
                if a['maths'] < 1.35:
                    out.append('%s: the options\' maths is %.2f times the body\'s size (at least 1.35)' % (atag, a['maths']))
                if a['graph'] is None or a['graphOpen'] != wide or (wide and (a['graph'][0] < 0 or a['graph'][1] > fold)):
                    out.append('%s: the graph is %s at %s (from 1024 px: open, on screen above the fold at %d px; narrower: a closed button)' % (atag, 'open' if a['graphOpen'] else 'closed', a['graph'], fold))
            if (r['why'] != 'right') if right else (r['err'] != d['err'] or r['errText'] != lines.get(d['err'])):
                out.append('%s: shows %s' % (tag, 'no "Right" (%s)' % r['why'] if right else 'the line %r, not the LINES line for %s' % (r['errText'], d['err'])))
            for name, b in r['parts'].items():
                if (name == 'the "Right" line') != right and name not in ('the prompt', 'Next'):
                    continue                                 # a right answer shows the prompt, "Right" and Next; a wrong one the rest
                if b is None:
                    out.append('%s: %s is not on screen' % (tag, name))
                elif name == 'the table rows' and size[1] <= 600:
                    pass   # canon §7.6.1's fixed rule: on a screen 600 px tall or less the rows sit below Next (there, not gated)
                elif b[0] < 0 or b[1] > fold:
                    out.append('%s: %s ends at %d px, below the fold at %d px' % (tag, name, b[1], fold))
            want = 1 if right else 2
            if len(r['marked']) != want or any(b is None or b[0] < 0 or b[1] > fold for b in r['marked']):
                out.append('%s: %s on screen above the fold (%s)' % (tag, 'the marked answer is not' if right else 'the chosen option and the answer are not both', r['marked']))
            if not right:
                eqs = [ln['eq'] for ln in r['lines']]
                if len(eqs) != len(q['working']) or max(eqs) - min(eqs) > 1.0:
                    out.append('%s: the working\'s "=" signs are not in one column (at %s px)' % (tag, eqs))
                for i, ln in enumerate(r['lines'], 1):
                    beside = ln['whyRight'] <= ln['rhsLeft'] + 0.5 and ln['whyTop'] < ln['rhsBottom'] and ln['whyBottom'] > ln['rhsTop']
                    above = ln['whyBottom'] <= ln['rhsTop'] + 0.5
                    if not (beside if wide else above):
                        out.append('%s: the label of working line %d is not %s its line' % (tag, i, 'beside' if wide else 'above'))
            if wide and (r['graph'] is None or not r['graphOpen'] or r['graph'][0] < 0 or r['graph'][1] > fold):
                out.append('%s: the graph is not open on screen above the fold (%s)' % (tag, r['graph']))
            if not wide and (r['graphOpen'] or r['graph'] is None or r['nextOpen'] != r['parts']['Next']):
                out.append('%s: the graph\'s fold-out should be a closed button on the page, and opening it should not move Next (%s, Next %s then %s)' % (
                    tag, 'open' if r['graphOpen'] else r['graph'], r['parts']['Next'], r['nextOpen']))
            nb = r['parts'].get('Next')
            if nb and (worst is None or fold - nb[1] < worst[0]):
                worst = (fold - nb[1], q['id'], 'right' if right else d['err'])
    info.setdefault('fit', []).append((size, mode, n, worst))


def fit_units():
    return (['fit %dx%d %s %s' % (s[0], s[1], a, t) for s in SIZES for a in ('normal', 'Aa') for t in ('table', 'pro')]
            + ['fit %dx%d normal %s' % (SMALL[0], SMALL[1], t) for t in ('table', 'pro')])


START_JS = r"""async () => {
  if (document.fonts && document.fonts.ready) await document.fonts.ready;
  const frame = () => new Promise(r => requestAnimationFrame(() => r()));
  await frame(); await frame();
  const art = document.getElementById('startShow'), side = document.querySelector('.menu-side'), menu = document.getElementById('menu');
  const ctl = [document.getElementById('proBtn'), ...document.querySelectorAll('#stageList .stage-btn')];
  const ends = () => ctl.map(e => Math.round(e.getBoundingClientRect().bottom + window.scrollY));
  if (!art || ctl.length !== 6) return null;
  const withArt = ends(), r = art.getBoundingClientRect(), svg = art.querySelector('svg.maffs-plot-svg');
  const col = (getComputedStyle(side).display === 'contents' ? menu : side).getBoundingClientRect().width;
  const out = { fold: window.innerHeight - 40, withArt, art: [Math.round(r.top + window.scrollY), Math.round(r.bottom + window.scrollY), r.width], col,
                svg: svg ? svg.getBoundingClientRect().width : 0, wide: document.documentElement.scrollWidth, view: document.documentElement.clientWidth };
  art.style.display = 'none';
  await frame();
  out.without = ends();
  art.style.display = '';
  return out;
}"""


def check_start_fit(page, size, aa, out, info):
    tag = 'start screen at %dx%d %s' % (size + ('Aa' if aa else 'normal',))
    r = page.evaluate(START_JS)
    if r is None:
        out.append('%s: the picture, the Pro switch or the five stage buttons are not there' % tag)
        return
    names = ['the Pro switch'] + ['the Stage %d button' % n for n in range(1, 6)]
    if not r['svg'] or r['art'][2] < 0.4 * r['col'] - 0.5 or r['art'][2] > r['col'] + 0.5:
        out.append('%s: the picture is %.0f px wide in a column of %.0f px (between 40%% and the whole of it)' % (tag, r['art'][2], r['col']))
    if r['wide'] > r['view']:
        out.append('%s: the page scrolls sideways (%d px wide in %d)' % (tag, r['wide'], r['view']))
    for name, a, b in zip(names, r['without'], r['withArt']):
        if a <= r['fold'] < b:
            out.append('%s: the picture pushes %s below the fold (it ends at %d px without it, %d px with it; the fold is at %d px)' % (tag, name, a, b, r['fold']))
        elif size[0] >= WIDE and b > r['fold']:
            out.append('%s: %s ends at %d px, below the fold at %d px' % (tag, name, b, r['fold']))
    info.setdefault('start', []).append((size, 'Aa' if aa else 'normal', r['art'], r['withArt'][-1], r['fold']))


def start_units():
    return ['start %dx%d %s' % (s[0], s[1], a) for s in START_SIZES for a in ('normal', 'Aa')]


def check(html, out, units, shard=None, sample=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info, items = {}, None
    if 'bank' in units:
        with unit('bank'):
            try:
                items = check_bank(html, out, info)
            except Exception as e:  # noqa: BLE001
                out.append('the bank checks threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u != 'bank']
    if not browser:
        return info
    try:
        items = [json.loads(ln) for ln in bank_lines(html)]
        pairs = start_show(html)
        lines = lines_of(html)
    except Exception as e:  # noqa: BLE001
        out.append('the page\'s bank, START_SHOW or LINES cannot be read: %s' % str(e).splitlines()[0][:200])
        return info
    some = items[:sample] if sample else items
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    part = uid.split(' ')
                    size = tuple(int(x) for x in part[1].split('x'))
                    aa = len(part) > 2 and part[2] == 'Aa'
                    br, page, errs = open_page(pw, base, html, size, aa, fast=part[0] == 'waits', still=part[0] == 'still')
                    try:
                        if part[0] == 'katex':
                            r = page.evaluate(KATEX_JS)
                            out.extend('katex: %s' % b for b in r['bad'])
                            info['katex'] = r['n']
                        elif part[0] == 'play':
                            check_switch(page, size, out)
                            for m in MODES:
                                play(page, m, lines, size, out)
                            info.setdefault('played', []).append(size)
                        elif part[0] == 'waits':
                            check_waits(page, size, out)
                            info['waits'] = size
                        elif part[0] == 'graph':
                            check_graphs(page, some, size, lines, out, info)
                        elif part[0] == 'pens':
                            check_pens(page, pairs, size, out, info)
                        elif part[0] == 'still':
                            check_still(page, pairs, items, size, out, info)
                        elif part[0] == 'start':
                            check_start_fit(page, size, aa, out, info)
                        else:
                            check_fit(page, some, size, aa, part[3] == 'pro', lines, out, info)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


PLANT_SAMPLE = 8

# Each plant: (what, [(old, new)], the unit it needs, the pattern its finding must match). The eight of D-BY-DX-BUILD,
# then the five of D-BY-DX-GRAPH.
DRAW = "plot.add('d', curve(Q.answer.terms), {"
PLANTS = [
    ('a wrong answer', [('"answer":{"tex":"20x^{3}","terms":[["pow","20","3"]]}', '"answer":{"tex":"21x^{3}","terms":[["pow","21","3"]]}')],
     'bank', r"s1-01: answer '21x\^\{3\}' is not the derivative, which sympy gives as 20\*x\*\*3"),
    ('a decoy equal in value to its answer', [('{"err":"sign_lost","tex":"\\\\dfrac{6}{x^{3}}","terms":[["pow","6","-3"]]}',
                                               '{"err":"sign_lost","tex":"-\\\\dfrac{6}{1x^{3}}","terms":[["overpow","-6","1","3"]]}')],
     'bank', r"s2-01: options '-\\\\dfrac\{6\}\{x\^\{3\}\}' and '-\\\\dfrac\{6\}\{1x\^\{3\}\}' are equal in value"),
    ("a tex string that doesn't match its terms", [('{"err":"power_kept","tex":"20x^{4}"', '{"err":"power_kept","tex":"20x^{5}"')],
     'bank', r"s1-01: decoy power_kept tex '20x\^\{5\}', rendered from its terms '20x\^\{4\}'"),
    ('a missing LINES key', [('    ln_flipped: "ln of ax differentiates to 1/x, not 1 over the ln.",\n', '')],
     'bank', r'no LINES line for ln_flipped'),
    ('the wrong line shown for a decoy', [("'<div class=\"fb-err\">' + esc(LINES[err]) + '</div>'", "'<div class=\"fb-err\">' + esc(LINES[Q.decoys[0].err]) + '</div>'")],
     'play 375x667', r'shows the line .*, not the LINES line for '),
    ('a decoy err key its stage does not allow (sign_slip in Stage 1)',
     [('{"err":"power_kept","tex":"20x^{4}"', '{"err":"sign_slip","tex":"20x^{4}"')],
     'bank', r's1-01: sign_slip is not allowed in stage 1'),
    ('the table shown during a Pro question', [('    setTable(!isPro(m));\n', '    setTable(true);\n')],
     'play 375x667', r'pro-stage-1 question 1 .*: the table is in the page during a Pro question'),
    ('the working pushed below the fold', [('.w-lhs{text-align:right}', '.w-lhs{text-align:right}.worked{padding-top:420px}')],
     'fit 375x667 normal table', r'the working ends at \d+ px, below the fold at 627 px'),
    ('a decoy drawn on the graph', [(DRAW, "plot.add('d', curve(Q.decoys[0].terms), {")],
     'graph 1280x720', r"the gradient function's curve is not the answer's"),
    ('a right answer that advances by itself', [('label: label, floorMs: REVEAL_MS });\n', 'label: label, floorMs: REVEAL_MS });\n      MaffsLock.timer(advance, 1000);\n')],
     'waits 375x667', r'a right answer moved on by itself within 30 s'),
    ('a START_SHOW pair equal to a bank question',
     [('{"q":[["pow","1","3"],["pow","-3","1"]],"d":[["pow","3","2"],["const","-3"]],', '{"q":[["pow","5","1"],["pow","2","3"]],"d":[["const","5"],["pow","6","2"]],')],
     'bank', r'start screen: pair 1 is a question in the game \(s5-01\)'),
    ('a working line that is not equal to its side', [('{"why":"tidy up","lhs":"","rhs":"20x^{3}"}', '{"why":"tidy up","lhs":"","rhs":"21x^{3}"}')],
     'bank', r's1-01: working line 2 \(\.\.\. = 21x\^\{3\}\) is not equal to the derivative'),
    ("f' drawn as a tangent at a point",
     [(DRAW, "plot.add('d', (function () { var a = (Q.graph.x[0] + Q.graph.x[1]) / 2, m = value(Q.answer.terms, a), c = value(Q.q, a); "
             "return function (x) { return c + m * (x - a); }; })(), {")],
     'graph 1280x720', r"the gradient function's curve is not the answer's"),
]


def selftest(html, plants=None, shard=None):
    ok = True
    for what, edits, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = html
                for old, new in edits:
                    src = pc.apply_plant(src, old, new, name=what)
            except pc.StalePlant as e:
                print('  self-test %-68s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id], sample=PLANT_SAMPLE)   # a fit or graph plant needs only the first items' screens
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-68s %s' % (what, ('caught: ' + hit[0][:110]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = (['bank', 'katex 1280x720'] + ['play %dx%d' % s for s in PLAY_SIZES] + ['waits 375x667']
             + ['graph %dx%d' % s for s in reversed(PLAY_SIZES)] + ['pens 1280x720', 'still 1280x720'] + fit_units() + start_units())
    if args.selftest:
        units = []
    mine = shard.pick(units + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    run = [u for u in units if u in mine]
    info = check(html, out, run, shard) if run else {}
    if 'bank' in info:
        print('%s: %d items, the contract\'s hash and counts; every question differentiated in sympy; every decoy, TeX string and working line recomputed from the item\'s own terms, read back and held equal to its side; every pair of curves readable on its window; %d start-screen pairs; ERR_STAGES, LINES and equal-value options checked' % (SLUG, info['bank'], info.get('show', 0)))
    if 'katex' in info:
        print('%s: %d different TeX strings rendered by KaTeX without an error' % (SLUG, info['katex']))
    for size in info.get('played', []):
        print('%s: %d runs played to the end at %dx%d (five stages, with the table and in Pro; right and wrong marked and waiting on Next, each wrong option\'s own line, working and table rows, the graph before and after)' % (SLUG, len(MODES), size[0], size[1]))
    if 'waits' in info:
        print('%s: a right answer and a wrong one each waited 30 s of the page\'s time at %dx%d, then moved on at Enter or Space' % ((SLUG,) + info['waits']))
    for size, n, worst in info.get('graphs', []):
        print('%s: %d graphs read back at %dx%d (the function, then the function and the gradient function); the farthest point from its curve: %.2f px' % (SLUG, n, size[0], size[1], worst))
    if 'pens' in info:
        print('%s: the start screen\'s pens read %d times while drawing, at the same x each time; drawn in %.1f s, left %.1f s; hidden tab, third pair and the loop checked' % ((SLUG,) + info['pens']))
    if 'still' in info:
        print('%s: with reduced motion the first pair is finished and still, and a gradient function is drawn at once' % SLUG)
    for size, mode, n, worst in info.get('fit', []):
        print('%s: %d asking, right and wrong screens at %dx%d (%s); the least room under Next: %s' % (SLUG, n, size[0], size[1], mode, ('%d px (%s, %s)' % worst) if worst else 'none measured'))
    for size, mode, art, last, fold in info.get('start', []):
        print('%s: the start screen at %dx%d (%s): the picture %.0f px wide from %d to %d px; Stage 5\'s button ends at %d px, the fold is at %d px' % (SLUG, size[0], size[1], mode, art[2], art[0], art[1], last, fold))
    ok = selftest(html, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
    for f in out[:80]:
        print('FAIL  ' + f)
    if len(out) > 80:
        print('FAIL  ... and %d more' % (len(out) - 80))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
