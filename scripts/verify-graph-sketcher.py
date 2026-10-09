#!/usr/bin/env python3
# ci-line: Graph Sketcher (keys recomputed from each printed equation) |
"""Independent verification of graph-sketcher's keys (todo §1.36; audit §1.2 items 13-14).

Every scenario prints its model as an equation (eqLatex). That equation, not the game's
own fn, is the source of truth: it is parsed into SymPy (constants a context line
defines, such as ω = 100π, are substituted; angles are in degrees where the scenario says
so), and then

  - the game's fn, which draws the graph, must agree with the printed equation at every
    table x and at points across the x range;
  - every table value, given or keyed, must be the equation's value at that x, correctly
    rounded at the precision it is stored to;
  - every typed interpretation question is recomputed from the equation, as SPECS says
    the prompt asks (evaluate, solve, maximum, roots, turning point, gradient), and the
    key must be that value correctly rounded at the precision it is stored to. A turning
    point checks both coordinates; a roots key must list exactly the roots asked for.

The marking is then played in the page through the game's own functions: every table
cell and every typed question, answered with the true value, must be marked correct.
Tolerances are not checked here: they are the shared precision marker's business (§1.36).

A fault-injection self-test (a wrong cell, a wrong given value, a wrong reading key, a
graph that disagrees with its equation, a reworded prompt) must FAIL each time; it runs
unless --no-selftest.

    python scripts/verify-graph-sketcher.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import math
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication,
                                        parse_expr, standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'graph-sketcher'
TRANSFORMS = standard_transformations + (implicit_multiplication, convert_xor)
GREEK = {r'\omega': 'w', r'\varepsilon': 'q', r'\sigma': 'g', r'\theta': 'u'}


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, sid, what, detail):
        self.fails.append('%s %s: %s' % (sid, what, detail))


# --------------------------------------------------------------------------
#  the printed equation -> SymPy
# --------------------------------------------------------------------------
def _braces(s, i):
    """Index just past the {...} group starting at s[i] == '{'."""
    depth = 0
    for j in range(i, len(s)):
        depth += {'{': 1, '}': -1}.get(s[j], 0)
        if depth == 0:
            return j + 1
    raise ValueError('unbalanced braces in %r' % s)


def latex_to_text(tex):
    for k, v in GREEK.items():
        tex = tex.replace(k, v)
    tex = tex.replace(r'\times', '*').replace(r'\pi', ' pi ').replace(r'\sin', 'sin').replace(r'\cos', 'cos')
    tex = tex.replace('°', '').replace('−', '-')
    while r'\frac' in tex:
        i = tex.index(r'\frac')
        a0 = i + 5
        a1 = _braces(tex, a0)
        b1 = _braces(tex, a1)
        tex = tex[:i] + '((%s)/(%s))' % (tex[a0 + 1:a1 - 1], tex[a1 + 1:b1 - 1]) + tex[b1:]
    out, i = '', 0
    while i < len(tex):                      # e^{...} -> exp(...), ^{...} -> ^(...)
        if tex.startswith('e^{', i) and (i == 0 or not tex[i - 1].isalpha()):
            j = _braces(tex, i + 2)
            out += 'exp(%s)' % tex[i + 3:j - 1]
            i = j
        elif tex.startswith('^{', i):
            j = _braces(tex, i + 1)
            out += '^(%s)' % tex[i + 2:j - 1]
            i = j
        else:
            out += tex[i]
            i += 1
    return out


def parse_model(s, spec):
    left, right = s['eqLatex'].split('=', 1)
    text = latex_to_text(right)
    names = {c: sp.Symbol(c) for c in set(re.findall(r'[A-Za-z]', text)) - set('exppisincos')}
    names.update(pi=sp.pi, exp=sp.exp, sin=sp.sin, cos=sp.cos)
    expr = parse_expr(text, local_dict=names, transformations=TRANSFORMS)
    for name, val in spec.get('subs', {}).items():
        expr = expr.subs(sp.Symbol(name), val)
    if spec.get('degrees'):
        expr = expr.replace(sp.sin, lambda a: sp.sin(a * sp.pi / 180)).replace(sp.cos, lambda a: sp.cos(a * sp.pi / 180))
    free = sorted(expr.free_symbols, key=str)
    if len(free) != 1:
        raise ValueError('expected one variable in %r, found %s' % (s['eqLatex'], free))
    return free[0], expr


# --------------------------------------------------------------------------
#  SPECS: what each typed question asks, from its own prompt. Keyed by scenario id and
#  the question's index in iqs. 'has' must still be in the prompt (else the spec must be
#  re-derived). Kinds:
#    eval x       the value at x                 solve y    the x where the value is y
#    max / min    the greatest / least value     argmax     the x of the first maximum
#    roots        every x in range where f = 0   tp kind    (x, y) of a turning point
#    grad a b     (f(b) - f(a)) / (b - a)        year y0    solve, plus the base year
# --------------------------------------------------------------------------
SPECS = {
    'CM1': dict(iq={0: ('solve', 3, 'wind speed when wave height is 3 m'), 1: ('eval', 70, 'h when s = 70')}),
    'CM2': dict(iq={0: ('eval', 2.5, 'P when x = 2.5')}),
    'CM3': dict(iq={0: ('year', 200, 2010, 'the year when the population reaches 200,000'), 1: ('eval', 25, 'P when t = 25')},
                context='t = years since 2010'),
    'CM4': dict(iq={0: ('solve', 20, 'braking distance reaches 20 m')}),
    'CM5': dict(iq={0: ('solve', 30, 'average cost to fall to £30')}),
    'CM6': dict(iq={0: ('max', None, 'maximum volume')}),
    'CM7': dict(iq={0: ('solve', 40, 'reach 40 g')}),
    'CM8': dict(iq={0: ('max', None, 'maximum height')}),
    'CM9': dict(iq={0: ('eval', 50, 't when s = 50')}),
    'CM10': dict(iq={0: ('eval', 55, 'h when s = 55')}),
    'CM11': dict(iq={0: ('eval', 18, 'A when n = 18'), 1: ('eval', 30, 'A when n = 30')}),
    'CM12': dict(iq={0: ('max', None, 'maximum fuel efficiency')}),
    'CM13': dict(iq={0: ('eval', 5.5, 'P when x = 5.5')}),
    'CM14': dict(iq={0: ('eval', 8, 'P when V = 8')}),
    'CM15': dict(degrees=True, iq={0: ('max', None, 'maximum height'), 1: ('argmax', None, 'maximum height first reached')}),
    'AL1': dict(iq={0: ('roots', None, 'crosses the x-axis'), 1: ('tp', 'min', 'turning point')}),
    'AL2': dict(iq={0: ('roots', None, 'y = 0'), 1: ('tp', 'localmin', 'local minimum')}),
    'AL3': dict(iq={0: ('roots', None, 'crosses the x-axis')}),
    'AL5': dict(degrees=True, iq={0: ('tp', 'max', 'maximum'), 1: ('tp', 'min', 'minimum')}),
    'AL6': dict(iq={0: ('roots', None, 'all x-values where y = 0'), 1: ('min', None, 'y-coordinate of the local minimum')}),
    'AL7': dict(iq={0: ('roots', None, 'all roots'), 1: ('grad', (0, 4), 'gradient between x = 0 and x = 4')}),
    'AL9': dict(degrees=True, iq={0: ('roots2', None, 'first two positive roots'), 1: ('tp', 'firstmax', 'first maximum')}),
    'AL11': dict(iq={0: ('roots', None, 'all roots'), 1: ('tp', 'localmin', 'local minimum')}),
    'AL12': dict(iq={0: ('tp', 'max', 'maximum'), 1: ('roots', None, 'approximate roots')}),
    'AL13': dict(degrees=True, iq={0: ('tp', 'max', 'maximum')}),
    'AL14': dict(iq={0: ('tp', 'localmax', 'local maximum'), 1: ('tp', 'localmin', 'local minimum')}),
    'AL15': dict(iq={0: ('roots', None, 'crosses the x-axis')}),
    'L4_1': dict(iq={0: ('tp', 'max', 'maximum stress')}),
    'L4_2': dict(iq={0: ('solve', 6, 'V reach 6V')}),
    'L4_3': dict(iq={0: ('tp', 'firstmax', 'first maximum')}),
    'L4_4': dict(iq={0: ('solve', 50, 'resistance is 50')}),
    'L4_5': dict(iq={0: ('roots', None, 'deflection is zero'), 1: ('tp', 'max', 'maximum deflection')}),
    'L4_6': dict(iq={1: ('eval', 5, 'A when t = 5')}),
    'L4_7': dict(iq={0: ('tp', 'max', 'maximum height'), 1: ('rootpos', None, 'time of flight')}),
    'L4_8': dict(iq={0: ('max', None, 'maximum displacement')}),
    'L4_9': dict(iq={0: ('eval', 15, 'P when R = 15')}),
    'L4_10': dict(iq={1: ('solve', 0.5, 'x when G = 0.5')}),
    'L4_11': dict(iq={1: ('solve', 0.004, 'time when')}),
    'L4_12': dict(iq={0: ('eval', 4.5, 'Q when h = 4.5')}),
    'L4_13': dict(iq={0: ('solve', 50, 'drag force reaches 50 N')}),
    'L4_14': dict(subs={'w': 100 * sp.pi}, context='ω = 100π', iq={1: ('argmax', None, 'first maximum')}),
    'L4_15': dict(iq={0: ('solve', 100000, 'fatigue life of 100,000 cycles')}),
}


def numeric(f, var):
    return sp.lambdify(var, f, 'mpmath')


def grid(lo, hi, n=4000):
    return [lo + (hi - lo) * k / n for k in range(n + 1)]


def _bisect(g, a, b):
    ga = g(a)
    for _ in range(200):
        m = (a + b) / 2
        gm = g(m)
        if gm == 0 or b - a < 1e-15 * max(1, abs(m)):
            return m
        if (ga < 0) == (gm < 0):
            a, ga = m, gm
        else:
            b = m
    return (a + b) / 2


def roots_in(f, var, lo, hi):
    """Every root of f in [lo, hi]: sign changes bisected; touching (double) roots found
    where f' changes sign and f is zero there."""
    g = sp.lambdify(var, f, 'math')
    dg = sp.lambdify(var, sp.diff(f, var), 'math')
    xs = grid(lo, hi)
    scale = 1.0
    for x in xs[::40]:
        try:
            scale = max(scale, abs(g(x)))
        except (ZeroDivisionError, ValueError):
            pass
    found = []

    def add(r):
        try:
            near0 = abs(g(r)) < 1e-9 * scale
        except (ZeroDivisionError, ValueError):
            return
        if near0 and lo - 1e-12 <= r <= hi + 1e-12 and not any(abs(r - o) < 1e-7 * max(1, abs(hi - lo)) for o in found):
            found.append(r)

    def safe(h, x):
        try:
            return h(x)
        except (ZeroDivisionError, ValueError):
            return None
    vals = [safe(g, x) for x in xs]
    for (a, b), (ga, gb) in zip(zip(xs, xs[1:]), zip(vals, vals[1:])):
        if ga is None or gb is None:
            continue
        if ga == 0:
            add(a)
        elif (ga < 0) != (gb < 0) and abs(ga - gb) < 10 * scale:   # not a jump over an asymptote
            add(_bisect(g, a, b))
    dvals = [safe(dg, x) for x in xs]
    for (a, b), (da, db) in zip(zip(xs, xs[1:]), zip(dvals, dvals[1:])):
        if da is not None and db is not None and (da < 0) != (db < 0):
            add(_bisect(dg, a, b))
    if vals[-1] == 0:
        add(hi)
    return sorted(found)


def stationary(f, var, lo, hi):
    """[(x, y, 'max'|'min')] interior stationary points of f in (lo, hi), in order."""
    df = sp.diff(f, var)
    g = sp.lambdify(var, f, 'math')
    out = []
    for r in roots_in(df, var, lo, hi):
        if not (lo < r < hi):
            continue
        h = 1e-5 * max(1, abs(hi - lo))
        kind = 'max' if g(r) >= max(g(r - h), g(r + h)) else 'min' if g(r) <= min(g(r - h), g(r + h)) else None
        if kind:
            out.append((r, g(r), kind))
    return out


def answer_iq(kind, arg, f, var, lo, hi):
    g = sp.lambdify(var, f, 'math')
    if kind == 'eval':
        return float(f.subs(var, sp.nsimplify(arg)))
    if kind in ('solve', 'year'):
        target = arg[0] if kind == 'year' else arg
        rs = roots_in(f - sp.nsimplify(target), var, lo, hi)
        if len(rs) != 1:
            raise ValueError('%d solutions of value = %s in [%s, %s]' % (len(rs), target, lo, hi))
        return rs[0] + (arg[1] if kind == 'year' else 0)
    if kind in ('max', 'min', 'argmax'):
        pts = stationary(f, var, lo, hi)
        ends = [(lo, g(lo)), (hi, g(hi))]
        cands = [(x, y) for x, y, _ in pts] + ends
        best = max(cands, key=lambda p: p[1]) if kind != 'min' else min(cands, key=lambda p: p[1])
        if kind == 'argmax':
            top = best[1]
            return min(x for x, y in cands if abs(y - top) < 1e-9 * max(1, abs(top)))
        return best[1]
    if kind == 'grad':
        a, b = arg
        return (g(b) - g(a)) / (b - a)
    raise ValueError(kind)


def turning_point(which, f, var, lo, hi):
    g = sp.lambdify(var, f, 'math')
    pts = stationary(f, var, lo, hi)
    if which in ('localmax', 'localmin'):
        k = which[5:]
        c = [p for p in pts if p[2] == k]
        if len(c) != 1:
            raise ValueError('%d local %s points in range' % (len(c), k))
        return c[0][:2]
    if which == 'firstmax':
        cands = [(x, y) for x, y, k in pts if k == 'max'] + [(lo, g(lo))]
        top = max(y for _, y in cands)
        return min((p for p in cands if abs(p[1] - top) < 1e-9 * max(1, abs(top))), key=lambda p: p[0])
    k = which
    c = [p for p in pts if p[2] == k]
    if not c:
        raise ValueError('no %s in range' % k)
    best = max(c, key=lambda p: p[1]) if k == 'max' else min(c, key=lambda p: p[1])
    return best[:2]


# --------------------------------------------------------------------------
#  comparison: a key is right when it is the true value rounded at its own precision
# --------------------------------------------------------------------------
def decimals(v):
    s = repr(float(v))
    if 'e' in s:
        s = format(Decimal(s), 'f')
    return 0 if s.endswith('.0') else len(s.split('.')[1]) if '.' in s else 0


def rounds_to(key, true):
    dp = decimals(key)
    q = Decimal(1).scaleb(-dp)
    want = Decimal(repr(float(true))).quantize(q, rounding=ROUND_HALF_UP)
    return Decimal(repr(float(key))).quantize(q) == want, want


def check_scenario(rep, s, fn_vals, verbose=False):
    sid = s['id']
    spec = SPECS.get(sid, {})
    try:
        var, f = parse_model(s, spec)
    except Exception as e:      # noqa: BLE001  (a parse failure is a finding, not a crash)
        rep.fail(sid, 'equation', 'cannot read %r: %s' % (s['eqLatex'], e))
        return
    if spec.get('context') and spec['context'] not in s.get('context', ''):
        rep.fail(sid, 'context', 'no longer says %r: the spec must be re-derived' % spec['context'])
    g = sp.lambdify(var, f, 'math')
    lo, hi = s['xRange']
    for x, y in fn_vals:
        try:
            want = g(x)
        except (ZeroDivisionError, ValueError):
            continue
        if y is None or abs(y - want) > 1e-9 * max(1, abs(want)):
            rep.fail(sid, 'graph', 'fn(%s) = %s but the printed equation gives %s' % (x, y, want))
            break
    for kind in ('given', 'answers'):
        for x_text, key in s[kind].items():
            true = g(float(x_text))
            ok, want = rounds_to(key, true)
            if not ok:
                rep.fail(sid, '%s[%s]' % (kind, x_text), 'stored %s, the equation gives %.6g (%s at that precision)'
                         % (key, true, want))
    typed = {i: iq for i, iq in enumerate(s['iqs']) if iq['type'] != 'mcq'}
    want_spec = spec.get('iq', {})
    for i in sorted(set(typed) | set(want_spec)):
        iq, sp_ = typed.get(i), want_spec.get(i)
        if iq is None or sp_ is None:
            rep.fail(sid, 'iq %d' % i, 'a typed question with no spec, or a spec with no typed question: '
                     'derive the spec from the prompt')
            continue
        kind, arg, has = sp_[0], sp_[1], sp_[-1]
        if kind == 'year':
            arg = (sp_[1], sp_[2])
        if has not in iq['prompt']:
            rep.fail(sid, 'iq %d' % i, 'prompt %r no longer says %r: re-derive the spec' % (iq['prompt'], has))
            continue
        try:
            if kind == 'tp':
                tx, ty = turning_point(arg, f, var, lo, hi)
                for name, key, true in (('x', iq['answer']['x'], tx), ('y', iq['answer']['y'], ty)):
                    ok, want = rounds_to(key, true)
                    if not ok:
                        rep.fail(sid, 'iq %d (%s)' % (i, name), 'keyed %s, the equation gives %.6g (%s)' % (key, true, want))
            elif kind in ('roots', 'roots2', 'rootpos'):
                rs = roots_in(f, var, lo, hi)
                if kind == 'roots2':
                    rs = [r for r in rs if r > 0][:2]
                elif kind == 'rootpos':
                    rs = [r for r in rs if r > 1e-9]
                    rs = rs[:1]
                keys = iq['answers'] if 'answers' in iq else [iq['answer']]
                if len(keys) != len(rs):
                    rep.fail(sid, 'iq %d' % i, 'keyed %s, the equation has roots %s' % (keys, ['%.6g' % r for r in rs]))
                else:
                    for key, true in zip(sorted(keys), rs):
                        ok, want = rounds_to(key, true)
                        if not ok:
                            rep.fail(sid, 'iq %d' % i, 'root keyed %s, the equation gives %.6g (%s)' % (key, true, want))
            else:
                true = answer_iq(kind, arg, f, var, lo, hi)
                ok, want = rounds_to(iq['answer'], true)
                if not ok:
                    rep.fail(sid, 'iq %d' % i, '%r keyed %s, the equation gives %.6g (%s at that precision)'
                             % (iq['prompt'], iq['answer'], true, want))
        except Exception as e:  # noqa: BLE001
            rep.fail(sid, 'iq %d' % i, 'cannot recompute %r: %s' % (iq['prompt'], e))
    if verbose:
        print('  %-5s %s = %s' % (sid, var, f))


def check_bank(rep, bank, fn_vals, verbose=False):
    scenarios = [s for lvl in bank.values() for s in lvl]
    for sid in SPECS:
        if sid not in {s['id'] for s in scenarios}:
            rep.fail(sid, 'spec', 'no scenario with this id any more')
    for s in scenarios:
        check_scenario(rep, s, fn_vals.get(s['id'], []), verbose)
    return scenarios


def true_answers(s):
    """What a correct student types, at 6 s.f.: every cell and every typed question."""
    spec = SPECS.get(s['id'], {})
    var, f = parse_model(s, spec)
    g = sp.lambdify(var, f, 'math')
    lo, hi = s['xRange']
    sig = lambda v: float('%.6g' % v)  # noqa: E731
    cells = {x: sig(g(float(x))) for x in s['answers']}
    iqs = {}
    for i, iq in enumerate(s['iqs']):
        if iq['type'] == 'mcq' or i not in spec.get('iq', {}):
            continue
        sp_ = spec['iq'][i]
        kind = sp_[0]
        if kind == 'tp':
            x, y = turning_point(sp_[1], f, var, lo, hi)
            iqs[i] = dict(x=sig(x), y=sig(y))
        elif kind in ('roots', 'roots2', 'rootpos'):
            rs = roots_in(f, var, lo, hi)
            rs = [r for r in rs if r > 0][:2] if kind == 'roots2' else [r for r in rs if r > 1e-9][:1] if kind == 'rootpos' else rs
            iqs[i] = dict(text=', '.join('%.6g' % r for r in rs)) if kind != 'rootpos' else dict(value=sig(rs[0]))
        else:
            arg = (sp_[1], sp_[2]) if kind == 'year' else sp_[1]
            iqs[i] = dict(value=sig(answer_iq(kind, arg, f, var, lo, hi)))
        iqs[i]['reliable'] = 'yes' if iq.get('reliable') else 'no'
    return cells, iqs


# --------------------------------------------------------------------------
#  the page: fn values, and the marking played through the game's own functions
# --------------------------------------------------------------------------
FN_JS = """(id) => {
  const s = Object.values(SCENARIOS).flat().find(q => q.id === id);
  const [lo, hi] = s.xRange, xs = s.tableX.slice();
  for (let k = 0; k <= 40; k++) xs.push(lo + (hi - lo) * k / 40);
  return xs.map(x => { const y = s.fn(x); return [x, Number.isFinite(y) ? y : null]; });
}"""

PLAY_JS = """async (a) => {
  const q = Object.values(SCENARIOS).flat().find(s => s.id === a.id);
  const realTimeout = window.setTimeout;
  window.setTimeout = () => 0;            // a correct answer schedules the next screen
  const out = {cells: {}, iqs: {}};
  try {
    G.questions = [q]; G.qIdx = 0; G.level = a.level;
    buildTable(q);
    for (const [x, v] of Object.entries(a.cells)) {
      const inp = document.querySelector('input[data-x="' + x + '"]');
      if (!inp) { out.cells[x] = 'no input'; continue; }
      inp.value = String(v); checkCell(inp);
      out.cells[x] = inp.parentElement.classList.contains('correct-cell') ? 'ok' : 'rejected';
    }
    document.getElementById('qBox').style.display = 'block';
    for (const [i, v] of Object.entries(a.iqs)) {
      G.iqIdx = Number(i); loadIQ(q);
      const iq = q.iqs[G.iqIdx];
      if (iq.type === 'tp') {
        document.getElementById('iqTpX').value = String(v.x);
        document.getElementById('iqTpY').value = String(v.y);
        checkTPIQ();
      } else {
        document.getElementById('iqInput').value = v.text !== undefined ? v.text : String(v.value);
        if (iq.type === 'extrap') { document.getElementById('iqReliable').value = v.reliable; checkExtrapIQ(); }
        else if (iq.type === 'roots') checkRootsIQ();
        else checkReadIQ();
      }
      out.iqs[i] = document.getElementById('iqFb').textContent;
    }
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""


def check_played(rep, scenarios, played):
    for s in scenarios:
        r = played.get(s['id'])
        if r is None:
            continue
        for x, res in r['cells'].items():
            if res != 'ok':
                rep.fail(s['id'], 'marking (cell %s)' % x, 'the true value was %s' % res)
        for i, text in r['iqs'].items():
            if 'Correct' not in text:
                rep.fail(s['id'], 'marking (iq %s)' % i, 'typed the true value; the game said %r' % text.strip()[:100])


def load(patch_js=None, play=True):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof SCENARIOS !== "undefined" && typeof checkTPIQ === "function"', timeout=8000)
            if patch_js:
                page.evaluate(patch_js)
            bank = page.evaluate('JSON.parse(JSON.stringify(SCENARIOS))')
            fn_vals, played = {}, {}
            for lvl, items in bank.items():
                for s in items:
                    fn_vals[s['id']] = page.evaluate(FN_JS, s['id'])
                    if not play:
                        continue
                    try:
                        cells, iqs = true_answers(s)
                    except Exception:  # noqa: BLE001  (reported by check_scenario)
                        continue
                    played[s['id']] = page.evaluate(PLAY_JS, dict(id=s['id'], level=lvl, cells=cells,
                                                                  iqs={str(k): v for k, v in iqs.items()}))
            browser.close()
            if errors:
                sys.exit('page errors: %s' % '; '.join(errors[:5]))
            return bank, fn_vals, played
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank, fn_vals, played):
    lines, ok = [], True
    base = Report()
    check_played(base, check_bank(base, bank, fn_vals), played)
    clean = [s for lvl in bank.values() for s in lvl if not any(f.startswith(s['id'] + ' ') for f in base.fails)]

    def expect(name, fn):
        nonlocal ok
        rep = Report()
        fn(rep)
        rep.fails = [f for f in rep.fails if f not in base.fails]
        caught = bool(rep.fails)
        ok = ok and caught
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + rep.fails[0][:110]) if caught else '*** MISSED ***'))

    if not clean:
        return False, ['  self-test skipped: no clean scenario']

    def mutate(fn):
        b = copy.deepcopy(bank)
        target = next(s for lvl in b.values() for s in lvl if s['id'] == clean[0]['id'])
        fn(target)
        return b

    def first(d):
        return next(iter(d))

    expect('wrong table cell', lambda rep: check_bank(rep, mutate(lambda s: s['answers'].__setitem__(
        first(s['answers']), s['answers'][first(s['answers'])] + 1.3)), fn_vals))
    expect('wrong given value', lambda rep: check_bank(rep, mutate(lambda s: s['given'].__setitem__(
        first(s['given']), s['given'][first(s['given'])] + 2.7)), fn_vals))
    reader = next(s for s in clean if any(iq['type'] in ('read', 'extrap') for iq in s['iqs']))
    def wrong_read(s):
        if s['id'] != reader['id']:
            return
        iq = next(iq for iq in s['iqs'] if iq['type'] in ('read', 'extrap'))
        iq['answer'] = round(iq['answer'] * 1.2 + 1, 3)
    b = copy.deepcopy(bank)
    for lvl in b.values():
        for s in lvl:
            wrong_read(s)
    expect('wrong reading key', lambda rep: check_bank(rep, b, fn_vals))
    bad_fn = dict(fn_vals)
    bad_fn[clean[0]['id']] = [(x, (y or 0) + 0.5) for x, y in fn_vals[clean[0]['id']]]
    expect('graph disagrees with its equation', lambda rep: check_bank(rep, bank, bad_fn))
    reworded = next(s for s in clean if SPECS.get(s['id'], {}).get('iq'))
    def reword(s):
        if s['id'] == reworded['id']:
            k = min(SPECS[s['id']]['iq'])
            s['iqs'][k]['prompt'] = 'Estimate something else entirely.'
    b2 = copy.deepcopy(bank)
    for lvl in b2.values():
        for s in lvl:
            reword(s)
    expect('reworded prompt', lambda rep: check_bank(rep, b2, fn_vals))
    _, _, lie = load("""(() => { const s = Object.values(SCENARIOS).flat().find(q => q.id === %r);
        const k = Object.keys(s.answers)[0]; s.answers[k] = s.answers[k] + 5; })()""" % clean[0]['id'])
    expect('cell marked against a wrong key', lambda rep: check_played(rep, [clean[0]], lie))
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    bank, fn_vals, played = load()
    rep = Report()
    scenarios = check_bank(rep, bank, fn_vals, args.verbose)
    check_played(rep, scenarios, played)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, fn_vals, played)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    bad = {f.split(' ', 1)[0] for f in rep.fails}
    print('\n%s: %d FAIL(s) across %d of %d scenarios' % ('PASS' if ok else 'FAILED', len(rep.fails), len(bad), len(scenarios)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
