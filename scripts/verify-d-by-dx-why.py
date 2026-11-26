#!/usr/bin/env python3
# ci-shards: d by dx? Why? (the 60-item bank held to the contract's SHA-256 and counts; every question differentiated in sympy from its own terms; every decoy recomputed from its error key, allowed for its stage (ERR_STAGES) and no two options equal in value; every TeX string re-rendered from its terms; table rows and working lines rebuilt; one LINES line per error key, none unused; every stage played to the end with the table and in Pro, right and wrong marked, each wrong option showing its own line, the answer, the working and its table rows; the table open at 1280x720, closed at 375x667, gone in Pro; every item's wrong-answer screen above the fold at 375x667, 390x844, 1280x720 and 1366x768, normal and Aa, and at 320x568 normal, with the table and in Pro; fault-injection self-test) | | 3
# ci-deps: games/d-by-dx-why/ tools/d-by-dx-why/
r"""Independent verification for d by dx? Why? (games/d-by-dx-why/), contract D-BY-DX-BUILD, 26 Nov 2026.
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 60 items, the output of tools/d-by-dx-why/bank.py embedded one item a line. This script
never runs or imports that generator. It reads the bank from the page and works everything out again:

  Bank     the item lines hash to the contract's SHA-256; 60 items, 12 in each of five stages, ids and prompts unique.
           Each question is rebuilt in sympy from its "q" terms and differentiated by sympy; the answer's terms must be
           that derivative. Every decoy is recomputed from its err key and the question's terms (the expression that named
           error gives, written here, with sympy doing the calculus where the error is one: the sign slip is minus the
           derivative, "integrated instead" is sympy's integral). No two of an item's four options are equal in value
           (sympy, not the generator's four sample points). Every TeX string (the question, the answer, each decoy) is
           rendered again from its terms by this script's own formatter and must equal the bank's; so must the prompt,
           from the item's form and letter. Every decoy's err key is one ERR_STAGES allows for the item's stage
           (ERR_STAGES is read from the generator's source as data, by ast, never by running it). "rows" is the table
           row or rows the item's stage and kind need. Every working line is rebuilt from the item's own numbers (each
           product, each power less one, the rewritten power), so every sum in it is true.
  Lines    LINES in the page has exactly the keys of ERR_STAGES; every key the bank uses has a line and no line is unused.
  KaTeX    in Chromium, every TeX string in the bank (prompts, options, working lines) and the table renders in KaTeX
           without an error.
  Play     in Chromium at 375 x 667 and 1280 x 720, each stage played to the end with the table and in Pro (ten runs a
           size): eight different items of that stage, four options each, every button's dataset.val the bank's TeX and
           its label KaTeX; a right answer shows "Right:" and the answer and moves on by itself; a wrong answer marks
           the chosen option wrong and the answer right, shows exactly the LINES line for the chosen option's err key,
           "The answer is" and the answer, every working line, the item's table rows under "From the table:" and Next;
           the score is the right answers; one game_completed and one leaderboard submission on the run's board
           (stage-N, or pro-stage-N); no event but game_started, question_answered (with the item's id) and
           game_completed. With the table: it is the contract's six rows and two headings, open at 1280 x 720, closed
           but present at 375 x 667, and after a wrong answer exactly the item's rows are lit in it (none before, none
           after Next). In Pro: no table anywhere in the page while a question is asked. The Pro switch is off on load
           and nothing about it is stored.
  Fit      at 375 x 667, 390 x 844, 1280 x 720 and 1366 x 768, normal and Aa (the Aa button pressed, its fonts loaded),
           with the table and in Pro, for every item and each of its three wrong options: the line, the answer, the
           working, the table rows and Next all end above the fold (the viewport less the 40 px footer, in page
           coordinates), the prompt and the two marked options are on screen above it, the line shown is that option's,
           and the page does not scroll sideways. The same at 320 x 568 in normal mode (canon §7.6.1's smallest phone;
           Aa there is canon's recorded exception), except that the table rows, which the page moves below Next on a
           screen 600 px tall or less (canon §7.6.1's fixed rule), need only be on the page.

Work units: "bank" (no browser), "katex 1280x720", "play 375x667", "play 1280x720",
"fit <W>x<H> <normal|Aa> <table|pro>" (18: the four sizes in both modes, and 320 x 568 normal) and "plant: <what>" (one
per planted fault).

    python scripts/verify-d-by-dx-why.py              # every unit, then the self-test
    python scripts/verify-d-by-dx-why.py --selftest   # the planted faults only
"""
import argparse
import ast
import contextlib
import hashlib
import json
import os
import re
import sys
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
SHA256 = 'a8ecdc0582e0f336832726f8f4bf9f8782ef9f944b2efe5148d864658428a14e'   # contract D-BY-DX-BUILD
STAGE_NAMES = ['Power terms', 'Rewrite first', 'Sin and cos', 'e and ln', 'Sums of terms']
MODES = ['stage-%d' % n for n in range(1, 6)] + ['pro-stage-%d' % n for n in range(1, 6)]
PER = 8
PER_STAGE = 12
FOOTER = 40
SIZES = [(375, 667), (390, 844), (1280, 720), (1366, 768)]
SMALL = (320, 568)   # canon §7.6.1's smallest phone: normal mode only (Aa at 320 x 568 is the recorded exception)
PLAY_SIZES = [(375, 667), (1280, 720)]
EVENTS = {'game_started', 'question_answered', 'game_completed'}
VARS = {'x', 'r', 't', 'z'}
FORMS = {'wrt', 'bare', 'fn'}
# The table, as the contract gives it: [key, y, dy/dx], in this order, and the two headings.
TABLE_HEAD = [r"\(y\) or \(f(x)\)", r"\(\dfrac{dy}{dx}\) or \(f'(x)\)"]
TABLE = [['x', r'\(x\)', r'\(1\)'], ['axn', r'\(ax^{n}\)', r'\(anx^{n-1}\)'], ['sin', r'\(\sin ax\)', r'\(a\cos ax\)'],
         ['cos', r'\(\cos ax\)', r'\(-a\sin ax\)'], ['exp', r'\(e^{ax}\)', r'\(ae^{ax}\)'], ['ln', r'\(\ln ax\)', r'\(\frac{1}{x}\)']]


# ---------------------------------------------------------------- the page's bank and lines, read from its source
def bank_lines(html):
    """The raw item lines of the page's BANK, each as the generator wrote it (the joining comma removed)."""
    m = re.search(r'\n  var BANK = \[\n(.*?)\n  \];', html, re.S)
    if not m:
        raise ValueError('no BANK block in the page')
    lines = m.group(1).split('\n')
    return [ln[:-1] if ln.endswith(',') else ln for ln in lines]


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


def err_stages():
    """ERR_STAGES from the generator's source, as data: the dict literal is read by ast, the file is never run."""
    tree = ast.parse(open(GENERATOR, encoding='utf-8').read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ERR_STAGES' for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('no ERR_STAGES in %s' % GENERATOR)


# ---------------------------------------------------------------- this script's own TeX, from an item's terms
def ftex(x):
    """A whole number as its digits; anything else as a fraction with the sign in front."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + '\\frac{%d}{%d}' % (abs(x.numerator), x.denominator)


def body(t, v):
    """One term without its sign: (the sign is negative, the TeX of its size)."""
    kind, a = t[0], [Fraction(s) for s in t[1:]]
    c, size = a[0], abs(a[0])
    front = '' if size == 1 else ftex(size)           # a coefficient of 1 is not written in front of a letter or function
    inside = (lambda m: v if m == 1 else ftex(m) + v)  # 3x, or x when the multiple is 1
    if kind == 'const' or (kind == 'pow' and a[1] == 0):
        s = ftex(size)
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
        s = '\\frac{%s}{%s}' % (ftex(size), inside(a[1]))
    elif kind == 'overpow':
        s = '\\frac{%s}{%s%s}' % (ftex(size), ftex(a[1]), v if a[2] == 1 else '%s^{%s}' % (v, ftex(a[2])))
    elif kind == 'recipln':
        s = '\\frac{%s}{\\ln %s}' % (ftex(size), inside(a[1]))
    else:
        raise ValueError('a term kind this script does not know: %r' % kind)
    return c < 0, s


def render(terms, v):
    out = ''
    for i, t in enumerate(terms):
        neg, s = body(t, v)
        out += ('-' if neg else ('+' if i else '')) + s
    return out


def written(q):
    """The question as it is written. Stages 1 and 3-5: its terms as they stand. Stage 2: a negative whole power as a
    fraction over the letter's power, a fractional power as a root."""
    v, terms = q['var'], q['q']
    if q['stage'] != 2:
        return render(terms, v)
    c, p = Fraction(terms[0][1]), Fraction(terms[0][2])
    if p.denominator == 1:
        n = -p.numerator
        return ('-' if c < 0 else '') + '\\frac{%d}{%s}' % (abs(c), v if n == 1 else '%s^%d' % (v, n))
    root = '\\sqrt{%s^{%d}}' % (v, p.numerator) if p.denominator == 2 else '\\sqrt[%d]{%s^{%d}}' % (p.denominator, v, p.numerator)
    return ('' if c == 1 else ftex(c)) + root


def prompt_of(q, qtex):
    v = q['var']
    if q['form'] == 'wrt':
        return 'Differentiate with respect to \\(%s\\): \\(y = %s\\)' % (v, qtex)
    if q['form'] == 'bare':
        return 'Differentiate: \\(%s\\)' % qtex
    return "If \\(f(%s) = %s\\), find \\(f'(%s)\\)" % (v, qtex, v)


def last_line(q, qtex, ans):
    v = q['var']
    if q['form'] == 'wrt':
        return '\\(\\dfrac{dy}{d%s} = %s\\)' % (v, ans)
    if q['form'] == 'fn':
        return "\\(f'(%s) = %s\\)" % (v, ans)
    return '\\(\\dfrac{d}{d%s}\\left(%s\\right) = %s\\)' % (v, qtex, ans)


def power_lines(c, n):
    return ['Bring the power down: \\(%s \\times %s = %s\\)' % (ftex(c), '(%s)' % ftex(n) if n < 0 else ftex(n), ftex(c * n)),
            'Take one off the power: \\(%s - 1 = %s\\)' % (ftex(n), ftex(n - 1))]


def working_of(q, qtex, ans):
    """The item's working lines, rebuilt from its own terms: every product and every power is worked out here."""
    v, st, terms = q['var'], q['stage'], q['q']
    nums = [Fraction(s) for s in terms[0][1:]]
    if st == 1:
        c, n = nums
        if n == 1:
            w = ['\\(%s\\) on its own differentiates to \\(1\\), so the \\(%s\\) goes and the number stays: \\(%s \\times 1 = %s\\)' % (v, v, ftex(c), ftex(c * 1))]
        else:
            w = power_lines(c, n)
    elif st == 2:
        c, p = nums
        w = ['Rewrite first: \\(%s = %s\\)' % (qtex, render(terms, v)) + ('' if p.denominator == 1 else " (the root's number goes on the bottom of the power)")]
        w += power_lines(c, p)
    elif st == 3:
        c, a = nums
        if terms[0][0] == 'sin':
            w = ['\\(\\sin a%s \\to a\\cos a%s\\): the \\(%s\\) comes out front and stays in the angle' % (v, v, ftex(a))]
        else:
            w = ['\\(\\cos a%s \\to -a\\sin a%s\\): the \\(%s\\) comes out front, stays in the angle, and cos gives a minus' % (v, v, ftex(a))]
        if c != 1:
            w.append('\\(%s \\times %s = %s\\)' % (ftex(c), ftex(a), ftex(c * a)))
    elif st == 4:
        c, a = nums
        if terms[0][0] == 'exp':
            w = ['\\(e^{a%s} \\to ae^{a%s}\\): the \\(%s\\) comes down and the power stays the same' % (v, v, ftex(a))]
            if c != 1:
                w.append('\\(%s \\times %s = %s\\)' % (ftex(c), ftex(a), ftex(c * a)))
        else:
            w = ['\\(\\ln a%s \\to \\frac{1}{%s}\\): the \\(%s\\) cancels out, \\(\\frac{%s}{%s%s} = \\frac{1}{%s}\\)' % (v, v, ftex(a), ftex(a), ftex(a), v, v)]
            if c != 1:
                w.append('\\(%s \\times \\frac{1}{%s} = \\frac{%s}{%s}\\)' % (ftex(c), v, ftex(c), v))
    else:
        p = Fraction(terms[0][1])
        c, n = Fraction(terms[1][1]), Fraction(terms[1][2])
        w = ['Differentiate each term on its own:',
             '\\(%s \\to %s\\)' % (render([terms[0]], v), ftex(p)),
             '\\(%s \\to %s\\)' % (render([terms[1]], v), render([['pow', str(c * n), str(n - 1)]], v))]
        if len(terms) == 3:
            w.append("\\(%s\\) on its own is a constant: it doesn't change, so it differentiates to \\(0\\)" % ftex(Fraction(terms[2][1])))
    return w + [last_line(q, qtex, ans)]


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
            kind = shape(q)
            if kind is None:
                out.append('%s: its terms %s are not a stage %d question' % (iid, q['q'], st))
                continue
            v = sp.Symbol(q['var'], positive=True)
            qtex = written(q)
            if q['qtex'] != qtex:
                out.append('%s: question tex %r, rendered from its terms %r' % (iid, q['qtex'], qtex))
            if q['prompt'] != prompt_of(q, qtex):
                out.append('%s: prompt %r, rebuilt %r' % (iid, q['prompt'], prompt_of(q, qtex)))
            deriv = sp.diff(expr(q['q'], v), v)
            ans = q['answer']
            if not same(expr(ans['terms'], v), deriv):
                out.append('%s: answer %r is not the derivative, which sympy gives as %s' % (iid, ans['tex'], sp.simplify(deriv)))
            if ans['tex'] != render(ans['terms'], q['var']):
                out.append('%s: answer tex %r, rendered from its terms %r' % (iid, ans['tex'], render(ans['terms'], q['var'])))
            if len(q['decoys']) != 3:
                out.append('%s: %d decoys, not 3' % (iid, len(q['decoys'])))
            for d in q['decoys']:
                used.add(d['err'])
                if d['err'] not in allowed:
                    out.append('%s: %s is not a key of ERR_STAGES' % (iid, d['err']))
                elif st not in allowed[d['err']]:
                    out.append('%s: %s is not allowed in stage %d' % (iid, d['err'], st))
                if d['tex'] != render(d['terms'], q['var']):
                    out.append('%s: decoy %s tex %r, rendered from its terms %r' % (iid, d['err'], d['tex'], render(d['terms'], q['var'])))
                want = slip(q, kind, d['err'], v)
                if want is None:
                    out.append('%s: this script has no %s error for a %s question' % (iid, d['err'], kind))
                elif not same(expr(d['terms'], v), want):
                    out.append('%s: decoy %s is %r, recomputed %s' % (iid, d['err'], d['tex'], sp.simplify(want)))
            opts = [ans] + q['decoys']
            if len({d['err'] for d in q['decoys']}) != len(q['decoys']):
                out.append('%s: an error key is used twice' % iid)
            for i in range(len(opts)):
                for j in range(i + 1, len(opts)):
                    if opts[i]['tex'] == opts[j]['tex'] or same(expr(opts[i]['terms'], v), expr(opts[j]['terms'], v)):
                        out.append('%s: options %r and %r are equal in value' % (iid, opts[i]['tex'], opts[j]['tex']))
            if q['rows'] != rows_of(q, kind):
                out.append('%s: rows %s, a %s question needs %s' % (iid, q['rows'], kind, rows_of(q, kind)))
            work = working_of(q, qtex, render(ans['terms'], q['var']))
            if q['working'] != work:
                out.append('%s: working %r, rebuilt %r' % (iid, q['working'], work))
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
    info['bank'] = len(items)
    return items


# ---------------------------------------------------------------- the page
def open_page(pw, base, html, size, aa=False):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
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
    q.working.forEach(w => mixed(q.id + ' working', w));
  }
  DDX.TABLE_HEAD.forEach(h => mixed('table heading', h));
  DDX.TABLE.forEach(r => { mixed('table row ' + r[0], r[1]); mixed('table row ' + r[0], r[2]); });
  return { n: seen.size, bad };
}"""

# What is on screen: the options, the feedback after an answer, and the table.
SCREEN_JS = r"""() => {
  const opts = [...document.querySelectorAll('#opts .opt')].map(b => ({ val: b.dataset.val, cls: b.className, off: b.disabled,
    katex: b.querySelectorAll('.katex').length, shown: b.getBoundingClientRect().height > 0 }));
  const fb = document.querySelector('#feedback .fb');
  const err = fb && fb.querySelector('.fb-err'), ans = fb && fb.querySelector('.fb-ans'), head = fb && fb.querySelector('.fb-head');
  const rows = fb && fb.querySelector('.fb-rows');
  const t = document.getElementById('dtable');
  const cell = (el) => { const a = el.querySelector('annotation'); return a ? a.textContent : null; };
  return { state: DDX.ui.state(), mode: DDX.ui.mode(), q: DDX.ui.question(), score: DDX.ui.score(), opts,
           why: fb ? fb.dataset.why : null, err: fb ? fb.dataset.err || null : null, errText: err ? err.textContent : null,
           head: head ? head.textContent : null, headTex: head ? cell(head) : null,
           ansText: ans ? ans.textContent : null, ansTex: ans ? cell(ans) : null,
           worked: fb ? fb.querySelectorAll('.worked .w-line').length : 0,
           rowsHead: rows && rows.querySelector('.fb-rows-h') ? rows.querySelector('.fb-rows-h').textContent : null,
           rows: rows ? [...rows.querySelectorAll('.fb-row[data-row]')].map(r => r.dataset.row) : null,
           rowsTex: rows ? [...rows.querySelectorAll('.fb-row')].map(r => [...r.querySelectorAll('.c')].map(cell)) : null,
           next: !!document.querySelector('#feedback .maffs-next'),
           katexErrors: document.querySelectorAll('.katex-error').length,
           tables: document.querySelectorAll('#game table.dt').length,
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
    if t['open'] != (size[0] >= 1024):
        out.append('%s: the table is %s at %dx%d (open from 1024 px wide, a closed panel on anything narrower)' % ((tag, 'open' if t['open'] else 'closed') + size))
    if t['label'] != 'Derivative table':
        out.append('%s: the table\'s panel is labelled %r' % (tag, t['label']))
    if t['head'] != [tex_in(h) for h in TABLE_HEAD] or t['rows'] != [[r[0]] + tex_in(r[1]) + tex_in(r[2]) for r in TABLE]:
        out.append('%s: the table is not the contract\'s (headings %s, rows %s)' % (tag, t['head'], t['rows']))
    if t['open'] and not t['cellsShown']:
        out.append('%s: the open table has a row that is not showing' % tag)
    if t['lit'] != lit:
        out.append('%s: the table\'s lit rows are %s, should be %s' % (tag, t['lit'], lit))


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
        if k % 2 == 0:
            page.evaluate(PRESS_JS, q['answer']['tex'])
            a = page.evaluate(SCREEN_JS)
            right += 1
            if a['why'] != 'right' or not (a['head'] or '').startswith('Right: ') or a['headTex'] != q['answer']['tex']:
                out.append('%s: the right answer shows %r (%s), not "Right: " and the answer' % (tag, a['head'], a['why']))
            if a['next']:
                out.append('%s: a right answer waits on Next' % tag)
            try:
                page.wait_for_function('(id) => DDX.ui.state() === "over" || (DDX.ui.state() === "asking" && DDX.ui.question().id !== id)', arg=q['id'], timeout=4000)
            except Exception:  # noqa: BLE001
                out.append('%s: a right answer did not move on by itself' % tag)
                return
        else:
            d = q['decoys'][(k // 2) % 3]
            page.evaluate(PRESS_JS, d['tex'])
            a = page.evaluate(SCREEN_JS)
            check_wrong(tag, q, d, a, lines, out)
            check_table(tag, a, size, out, [r[0] for r in TABLE if r[0] in q['rows']])
            if a['score'] != right:
                out.append('%s: a wrong answer changed the score to %d' % (tag, a['score']))
            page.evaluate('DDX.ui.next()')
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
    shown = page.evaluate("() => ({ score: document.getElementById('resScore').textContent, of: document.getElementById('resOf').textContent, on: document.getElementById('results').classList.contains('active') })")
    if not shown['on'] or shown['score'] != str(right) or shown['of'] != 'out of %d' % PER:
        out.append('%s: the results screen shows %s, expected %d out of %d' % (tag, shown, right, PER))
    page.evaluate("document.getElementById('menuBtn').click()")


def check_wrong(tag, q, d, a, lines, out):
    """A wrong answer's screen: the chosen option's own line, the answer, the working, the table rows, Next, the marks."""
    if a['why'] != 'wrong':
        out.append('%s: %r is marked %s, not wrong' % (tag, d['tex'], a['why']))
        return
    if a['err'] != d['err'] or a['errText'] != lines.get(d['err']):
        out.append('%s: choosing %r (%s) shows the line %r, not the LINES line for %s' % (tag, d['tex'], d['err'], a['errText'], d['err']))
    if not (a['ansText'] or '').startswith('The answer is ') or a['ansTex'] != q['answer']['tex']:
        out.append('%s: a wrong answer shows %r, not "The answer is " and the answer' % (tag, a['ansText']))
    if a['worked'] != len(q['working']):
        out.append('%s: %d working lines shown, the item has %d' % (tag, a['worked'], len(q['working'])))
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


# One item's wrong-answer screen for one wrong option, measured in page coordinates once the layout has settled.
FIT_JS = r"""async ([id, val, pro]) => {
  DDX.ui.preview(id, pro);
  const frame = () => new Promise(r => requestAnimationFrame(() => r()));
  await frame();
  const b = [...document.querySelectorAll('#opts .opt')].find(x => x.dataset.val === val);
  if (!b) return null;
  b.click();
  await frame(); await frame();
  const y = window.scrollY, box = (el) => { if (!el) return null; const r = el.getBoundingClientRect(); return r.width && r.height ? [Math.round(r.top + y), Math.round(r.bottom + y)] : null; };
  const fb = document.querySelector('#feedback .fb');
  const marked = [...document.querySelectorAll('#opts .opt.is-wrong, #opts .opt.is-right')].map(box);
  return { fold: window.innerHeight - 40, wide: document.documentElement.scrollWidth, view: document.documentElement.clientWidth,
           err: fb ? fb.dataset.err || null : null, errText: fb && fb.querySelector('.fb-err') ? fb.querySelector('.fb-err').textContent : null,
           table: !!document.getElementById('dtable'),
           parts: { 'the prompt': box(document.getElementById('ask')), 'the line': box(fb && fb.querySelector('.fb-err')),
                    'the answer': box(fb && fb.querySelector('.fb-ans')), 'the working': box(fb && fb.querySelector('.worked')),
                    'the table rows': box(fb && fb.querySelector('.fb-rows')),
                    'Next': box(document.querySelector('#feedback .maffs-next')) },
           marked };
}"""


def check_fit(page, items, size, aa, pro, lines, out, info):
    worst, n = None, 0
    mode = '%s, %s' % ('Aa' if aa else 'normal', 'Pro' if pro else 'with the table')
    for q in items:
        for d in q['decoys']:
            tag = '%s, choosing %r (%s), at %dx%d %s' % (q['id'], d['tex'], d['err'], size[0], size[1], mode)
            r = page.evaluate(FIT_JS, [q['id'], d['tex'], pro])
            n += 1
            if r is None:
                out.append('%s: that option is not on screen' % tag)
                continue
            if r['table'] == pro:
                out.append('%s: the table is %s' % (tag, 'in the page during a Pro question' if pro else 'not in the page'))
            if r['err'] != d['err'] or r['errText'] != lines.get(d['err']):
                out.append('%s: shows the line %r, not the LINES line for %s' % (tag, r['errText'], d['err']))
            if r['wide'] > r['view']:
                out.append('%s: the page scrolls sideways (%d px wide in %d)' % (tag, r['wide'], r['view']))
            for name, b in r['parts'].items():
                if b is None:
                    out.append('%s: %s is not on screen' % (tag, name))
                elif name == 'the table rows' and size[1] <= 600:
                    pass   # canon §7.6.1's fixed rule: on a screen 600 px tall or less the rows sit below Next (there, not gated)
                elif b[0] < 0 or b[1] > r['fold']:
                    out.append('%s: %s ends at %d px, below the fold at %d px' % (tag, name, b[1], r['fold']))
            if len(r['marked']) != 2 or any(b is None or b[0] < 0 or b[1] > r['fold'] for b in r['marked']):
                out.append('%s: the chosen option and the answer are not both on screen above the fold (%s)' % (tag, r['marked']))
            nb = r['parts'].get('Next')
            if nb and (worst is None or r['fold'] - nb[1] < worst[0]):
                worst = (r['fold'] - nb[1], q['id'], d['err'])
    info.setdefault('fit', []).append((size, mode, n, worst))


def fit_units():
    return (['fit %dx%d %s %s' % (s[0], s[1], a, t) for s in SIZES for a in ('normal', 'Aa') for t in ('table', 'pro')]
            + ['fit %dx%d normal %s' % (SMALL[0], SMALL[1], t) for t in ('table', 'pro')])


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
        lines = lines_of(html)
    except Exception as e:  # noqa: BLE001
        out.append('the page\'s bank or LINES cannot be read: %s' % str(e).splitlines()[0][:200])
        return info
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    part = uid.split(' ')
                    size = tuple(int(x) for x in part[1].split('x'))
                    aa = len(part) > 2 and part[2] == 'Aa'
                    br, page, errs = open_page(pw, base, html, size, aa)
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
                        else:
                            check_fit(page, items[:sample] if sample else items, size, aa, part[3] == 'pro', lines, out, info)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


PLANT_SAMPLE = 8

S101 = '"id":"s1-01","stage":1,"var":"x","form":"wrt","q":[["pow","5","4"]],"qtex":"5x^{4}","prompt":"Differentiate with respect to \\\\(x\\\\): \\\\(y = 5x^{4}\\\\)",'

# Each plant: (what, [(old, new)], the unit it needs, the pattern its finding must match). The eight the contract names.
PLANTS = [
    ('a wrong answer', [(S101 + '"answer":{"tex":"20x^{3}","terms":[["pow","20","3"]]}', S101 + '"answer":{"tex":"21x^{3}","terms":[["pow","21","3"]]}')],
     'bank', r"s1-01: answer '21x\^\{3\}' is not the derivative, which sympy gives as 20\*x\*\*3"),
    ('a decoy equal in value to its answer', [('"answer":{"tex":"-6x^{-3}","terms":[["pow","-6","-3"]]},"decoys":[{"err":"sign_lost","tex":"6x^{-3}","terms":[["pow","6","-3"]]}',
                                               '"answer":{"tex":"-6x^{-3}","terms":[["pow","-6","-3"]]},"decoys":[{"err":"sign_lost","tex":"-\\\\frac{6}{1x^{3}}","terms":[["overpow","-6","1","3"]]}')],
     'bank', r"s2-01: options '-6x\^\{-3\}' and '-\\\\frac\{6\}\{1x\^\{3\}\}' are equal in value"),
    ("a tex string that doesn't match its terms", [(S101 + '"answer":{"tex":"20x^{3}","terms":[["pow","20","3"]]},"decoys":[{"err":"power_kept","tex":"20x^{4}"',
                                                    S101 + '"answer":{"tex":"20x^{3}","terms":[["pow","20","3"]]},"decoys":[{"err":"power_kept","tex":"20x^{5}"')],
     'bank', r"s1-01: decoy power_kept tex '20x\^\{5\}', rendered from its terms '20x\^\{4\}'"),
    ('a missing LINES key', [('    ln_flipped: "ln of ax differentiates to 1/x, not 1 over the ln.",\n', '')],
     'bank', r'no LINES line for ln_flipped'),
    ('the wrong line shown for a decoy', [("'<div class=\"fb-err\">' + esc(LINES[err]) + '</div>'", "'<div class=\"fb-err\">' + esc(LINES[Q.decoys[0].err]) + '</div>'")],
     'play 375x667', r'shows the line .*, not the LINES line for '),
    ('a decoy err key its stage does not allow (sign_slip in Stage 1)',
     [(S101 + '"answer":{"tex":"20x^{3}","terms":[["pow","20","3"]]},"decoys":[{"err":"power_kept","tex":"20x^{4}"',
       S101 + '"answer":{"tex":"20x^{3}","terms":[["pow","20","3"]]},"decoys":[{"err":"sign_slip","tex":"20x^{4}"')],
     'bank', r's1-01: sign_slip is not allowed in stage 1'),
    ('the table shown during a Pro question', [('    setTable(!isPro(m));\n', '    setTable(true);\n')],
     'play 375x667', r'pro-stage-1 question 1 .*: the table is in the page during a Pro question'),
    ('the working pushed below the fold', [('.worked{font-size:.94rem;line-height:1.45}', '.worked{font-size:.94rem;line-height:1.45;padding-top:420px}')],
     'fit 375x667 normal table', r'the working ends at \d+ px, below the fold at 627 px'),
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
                check(src, got, [unit_id], sample=PLANT_SAMPLE)   # a fit plant needs only the first items' screens
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
    units = ['bank', 'katex 1280x720'] + ['play %dx%d' % s for s in PLAY_SIZES] + fit_units()
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
        print('%s: %d items, the contract\'s hash and counts; every question differentiated in sympy; every decoy, TeX string, table row and working line recomputed from the item\'s own terms; ERR_STAGES, LINES and equal-value options checked' % (SLUG, info['bank']))
    if 'katex' in info:
        print('%s: %d different TeX strings rendered by KaTeX without an error' % (SLUG, info['katex']))
    for size in info.get('played', []):
        print('%s: %d runs played to the end at %dx%d (five stages, with the table and in Pro; right and wrong marked, each wrong option\'s own line and table rows)' % (SLUG, len(MODES), size[0], size[1]))
    for size, mode, n, worst in info.get('fit', []):
        print('%s: %d wrong-answer screens at %dx%d (%s); the least room under Next: %s' % (SLUG, n, size[0], size[1], mode, ('%d px (%s, %s)' % worst) if worst else 'none measured'))
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
