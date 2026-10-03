#!/usr/bin/env python3
"""Independent verification of every calculation question in circle-theorem-spotter (todo §1.3).

Until 3 Oct 2026 two keys were wrong and nothing caught them: Q48 ("centre = 2x, circumference
= x + 15", keyed 15) had no solution at all, and its key came from setting the two angles equal,
the misconception the game exists to correct; Q19 asked for the angle on the MAJOR arc, keyed the
minor-arc angle (110°, where the answer is 70°), and its figure drew the point on the minor arc.

The bank is read from the page source (esprima), never from a copy. For every question:
  - options: four, distinct, the key not among the distractors, and no two options equal in value
    (40° and 40, 13 cm and \\sqrt{169} cm);
  - a calculation question (its key is a number, with ° or cm or as a \\sqrt) is solved again from
    the values the student is shown, using the circle theorem for its figure, with SymPy: each
    figure label becomes an expression ('72°' -> 72, 'x + 30' -> x + 30, '?' -> the unknown),
    the theorem gives the equations, and the solution must be unique and equal the key. A
    question whose ask starts "Find" must be a calculation question, and every calculation
    question must be one this script can solve (an unsolvable shape FAILS, never skips);
  - every angle in degrees the text states appears as a label in the figure;
  - any question that says "major arc" or "minor arc" agrees with its figure: where the text
    places a point on the circle, the figure draws it on that arc (for the angle-at-the-centre
    figure, by its `inside` flag); "subtended at the centre by the minor arc" needs a centre
    angle under 180°. Where the text names the arc, the key is derived from the TEXT's arc.
A fault-injection self-test (Q48's old numbers, Q19's old `inside` flag, a distractor equal to
its key, a changed key) must FAIL each time; it runs unless --no-selftest.

    python scripts/verify-circle-theorem-spotter.py [--file PATH] [--verbose] [--no-selftest]
"""
import argparse
import copy
import os
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'circle-theorem-spotter'
PAGE = os.path.join(bc.GAMES_DIR, SLUG, 'index.html')

X, Y, ANS = sp.symbols('x y ANS')
SYMS = {'x': X, 'y': Y}
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
NUMERIC_KEY = re.compile(r'^\s*(?:-?\d+(?:\.\d+)?|\\sqrt\{\d+\})\s*(?:°|cm)?\s*$')


class Unsolvable(Exception):
    pass


# --- reading the bank ------------------------------------------------------------------------

def to_py(node):
    if node.type == 'ObjectExpression':
        return {bc.literal_key(p.key): to_py(p.value) for p in node.properties}
    if node.type == 'ArrayExpression':
        return [to_py(e) for e in node.elements]
    if node.type == 'Literal':
        return node.value
    if node.type == 'UnaryExpression' and node.operator == '-':
        return -to_py(node.argument)
    raise ValueError(f'unexpected {node.type} in the bank at line {node.loc.start.line}')


def load_bank(path):
    with open(path, encoding='utf-8') as fh:
        tree, _src = bc.parse_game_source(fh.read())
    if tree is None:
        raise SystemExit(f'FAIL    {path}: the page script does not parse')
    for name, init, _kind in bc.top_level_declarations(tree):
        if name == 'QUESTIONS':
            out = []
            for level in init.properties:
                for i, el in enumerate(level.value.elements):
                    out.append((f'{bc.literal_key(level.key)} Q{i + 1}', el.loc.start.line, to_py(el)))
            return out
    raise SystemExit(f'FAIL    {path}: no top-level QUESTIONS')


# --- values ----------------------------------------------------------------------------------

def clean(s):
    return s.replace('&deg;', '').replace('&minus;', '-').replace('°', '').replace('−', '-').strip()


def label_expr(lab):
    """A figure label as SymPy: '?' is the unknown, otherwise a number or an expression in x, y."""
    s = clean(lab)
    if s == '?':
        return ANS
    s = re.sub(r'\s*cm$', '', s)
    return parse_expr(s, local_dict=SYMS, transformations=TRANSFORMS)


def option_value(opt):
    """An option's numeric value, or None for a worded option."""
    if not NUMERIC_KEY.match(opt):
        return None
    s = re.sub(r'\s*(°|cm)\s*$', '', opt.strip())
    m = re.match(r'\\sqrt\{(\d+)\}$', s)
    return sp.sqrt(int(m.group(1))) if m else sp.nsimplify(s)


def stated_lengths(text):
    return {m.group(1): sp.nsimplify(m.group(2))
            for m in re.finditer(r'\b([A-Z]{2})\s*=\s*(?:[a-z ]+=\s*)?(\d+(?:\.\d+)?)\s*(?:cm)?\b', text)}


def pair(a, b):
    return frozenset((a, b))


# --- where the figure puts its points ---------------------------------------------------------

def on_arc(a, b, p):
    """'minor' or 'major': which arc of chord AB (positions in degrees) the point p lies on."""
    span = (b - a) % 360                       # the arc from a anticlockwise to b
    inside = 0 < (p - a) % 360 < span
    arc = span if inside else 360 - span
    return 'minor' if arc < 180 else 'major'


def figure_arc(fig):
    """{point name: 'minor' | 'major'} for the points on the circle this figure places."""
    t = fig['t']
    names = fig.get('names')
    nm = lambda i, d: (names[i] if names and i < len(names) else d)  # noqa: E731
    if t == 'centreCirc':
        deg = fig['deg']
        marked = 'minor' if deg < 180 else 'major'
        other = 'major' if marked == 'minor' else 'minor'
        return {nm(2, 'C'): marked if fig.get('inside') else other}
    if t == 'sameSegment':
        return {nm(2, 'C'): on_arc(fig['A'], fig['B'], fig['C']),
                nm(3, 'D'): on_arc(fig['A'], fig['B'], fig['D'])}
    if t == 'altSegment':
        return {nm(2, 'C'): on_arc(fig['A'], fig['B'], fig['C'])}
    return {}


def text_arc_claims(text):
    """[(kind, arc, point)]: kind 'point' (a named point lies on that arc), 'opposite' (the angle
    at the circumference is subtended by that arc, so its vertex is on the other arc), or 'centre'
    (the angle at the centre is subtended by that arc). point is None when the text names none."""
    out = []
    for m in re.finditer(r'\b(major|minor)\s+arc', text, re.I):
        arc = m.group(1).lower()
        before = text[:m.start()]
        if re.search(r'subtended\s+at\s+the\s+centre\s+by\s+the\s*$', before, re.I):
            out.append(('centre', arc, None))
        elif re.search(r'subtended\s+by\s+the\s*$', before, re.I):
            out.append(('opposite', arc, None))
        else:
            pts = re.findall(r'\b([A-Z])\b(?:\s+and\s+([A-Z])\b)?[^.]*?$', before)
            names = [p for grp in pts[-1:] for p in grp if p] if pts else []
            if not names:
                names = [None]
            out.extend(('point', arc, p) for p in names)
    return out


def text_point_arc(fig, text):
    """The arc the TEXT puts the figure's circumference point on, or None if it does not say."""
    pts = figure_arc(fig)
    flip = {'major': 'minor', 'minor': 'major'}
    for kind, arc, point in text_arc_claims(text):
        if kind == 'opposite':
            return flip[arc]
        if kind == 'point' and (point is None or point in pts):
            return arc
    return None


# --- the theorems ------------------------------------------------------------------------------

def solve(eqs, target):
    syms = sorted(set().union(*(e.free_symbols for e in eqs)) | target.free_symbols, key=str)
    sols = sp.solve(eqs, syms, dict=True)
    vals = {sp.nsimplify(sp.simplify(target.subs(s))) for s in sols}
    vals = {v for v in vals if not v.free_symbols}
    if not sols:
        raise Unsolvable('the stated values have no solution')
    if len(vals) != 1:
        raise Unsolvable(f'the stated values do not fix one answer ({sorted(map(str, vals))})')
    return vals.pop()


def ask_target(ask, extra=None):
    """The unknown: x or y for 'Find x', else the '?' label, or a sum the ask names."""
    m = re.match(r'Find ([xy])\b', ask)
    if m:
        return SYMS[m.group(1)]
    if extra is not None:
        return extra
    return ANS


def derive(q):
    """The answer the stated values give, by the figure's theorem. Raises Unsolvable."""
    fig, text = q['fig'], q['ctx'] + ' ' + q['ask']
    t = fig['t']
    L = {k: label_expr(v) for k, v in fig.items() if k.endswith('Lab') and isinstance(v, str)}

    if t == 'centreCirc':
        if 'centreLab' not in L or 'circLab' not in L:
            raise Unsolvable('centreCirc needs both a centre and a circumference label')
        side = text_point_arc(fig, text) or figure_arc(fig)[(fig.get('names') or 'ABC')[2]]
        # The labelled centre angle stands on the arc AWAY from C when C is outside it.
        marked_minor = fig['deg'] < 180
        c_inside = (side == 'minor') == marked_minor
        rel = sp.Eq(L['circLab'], (360 - L['centreLab']) / 2 if c_inside else L['centreLab'] / 2)
        return solve([rel], ask_target(q['ask']))

    if t == 'semicircle':
        names = fig.get('names') or ['A', 'B', 'C']
        if 'Find' in q['ask'] and re.search(r'Find ([A-Z]{2})$', q['ask']):
            sides = stated_lengths(q['ctx'])
            want = re.search(r'Find ([A-Z]{2})$', q['ask']).group(1)
            diam = pair(names[0], names[1])
            known = {pair(*k): v for k, v in sides.items()}
            if pair(*want) == diam:
                legs = [v for k, v in known.items() if k != diam]
                return sp.sqrt(sum(v ** 2 for v in legs))
            hyp = known.get(diam)
            legs = [v for k, v in known.items() if k != diam]
            if hyp is None or len(legs) != 1:
                raise Unsolvable('semicircle side: need the diameter and one other side')
            return sp.sqrt(hyp ** 2 - legs[0] ** 2)
        a = L.get('aLab', sp.Symbol('a'))
        b = L.get('bLab', sp.Symbol('b'))
        c = L.get('cLab', sp.Symbol('c'))
        return solve([sp.Eq(c, 90), sp.Eq(a + b + c, 180)], ask_target(q['ask']))

    if t == 'cyclicQuad':
        names = fig.get('names') or ['A', 'B', 'C', 'D']
        labs = fig.get('labs', {})
        v = [label_expr(labs[n]) if n in labs else sp.Symbol('v' + n) for n in names]
        extra = None
        m = re.match(r'Find angle ([A-Z]) \+ angle ([A-Z])$', q['ask'])
        if m:
            extra = v[names.index(m.group(1))] + v[names.index(m.group(2))]
        return solve([sp.Eq(v[0] + v[2], 180), sp.Eq(v[1] + v[3], 180)], ask_target(q['ask'], extra))

    if t == 'sameSegment':
        return solve([sp.Eq(L['cLab'], L['dLab'])], ask_target(q['ask']))

    if t == 'altSegment':
        if 'altLab' in L:
            return solve([sp.Eq(L['tanLab'], L['altLab'])], ask_target(q['ask']))
        if 'oLab' in L:     # the centre angle on the chord is twice the alternate-segment angle
            return solve([sp.Eq(L['oLab'], 2 * L['tanLab'])], ask_target(q['ask']))
        raise Unsolvable('altSegment with no unknown label')

    if t == 'tangentRadius':
        if 'rightLab' in L:
            return solve([sp.Eq(L['rightLab'], 90)], ANS)
        if 'oabLab' in L:
            return solve([sp.Eq(L['oabLab'] + L['batLab'], 90)], ANS)
        if L.get('opLab') == ANS:    # OA ⟂ PA, so OP is the hypotenuse
            return sp.sqrt(L['oaLab'] ** 2 + L['paLab'] ** 2)
        raise Unsolvable('tangentRadius with no unknown label')

    if t == 'twoTangents':
        if 'oLab' in L:     # quadrilateral OAPB has two right angles
            return solve([sp.Eq(L['pLab'] + L['oLab'], 180)], ANS)
        if 'poaLab' in L:   # OP bisects the angle between the tangents
            return solve([sp.Eq(2 * L['poaLab'], L['pLab'])], ANS)
        sides = stated_lengths(q['ctx'])
        m = re.search(r'\b([A-Z]{2})\?', q['ask'])
        if m and len(sides) == 1:   # tangents from one point are equal
            return next(iter(sides.values()))
        raise Unsolvable('twoTangents: no theorem shape recognised')

    if t == 'chordBisect':
        r, c, d = L.get('radLab'), L.get('chordLab'), L.get('distLab')
        if None in (r, c, d):
            raise Unsolvable('chordBisect needs radius, chord and distance labels')
        if d == ANS:
            return sp.sqrt(r ** 2 - (c / 2) ** 2)
        return solve([sp.Eq(r ** 2, d ** 2 + (c / 2) ** 2)], ANS)

    raise Unsolvable(f'no theorem for figure type {t!r}')


# --- the checks --------------------------------------------------------------------------------

def check(bank, verbose=False):
    fails, solved = [], 0
    for qid, line, q in bank:
        where = f'{qid} (index.html:{line})'
        opts = [q['correct']] + list(q['d'])
        if len(q['d']) != 3:
            fails.append(f'{where}: {len(opts)} options, not 4')
        if len(set(opts)) != len(opts):
            fails.append(f'{where}: options repeat ({opts})')
        if q['correct'] in q['d']:
            fails.append(f'{where}: the key {q["correct"]!r} is also a distractor')
        vals = [option_value(o) for o in opts]
        for i in range(len(opts)):
            for j in range(i + 1, len(opts)):
                if vals[i] is not None and vals[j] is not None and sp.simplify(vals[i] - vals[j]) == 0 \
                        and opts[i] != opts[j]:
                    what = 'equals the key in value' if i == 0 else 'are equal in value'
                    fails.append(f'{where}: {opts[j]!r} {what} {opts[i]!r}' if i == 0
                                 else f'{where}: {opts[i]!r} and {opts[j]!r} {what}')

        text = q['ctx'] + ' ' + q['ask']
        labels = {clean(v) for k, v in q['fig'].items() if k.endswith('Lab') and isinstance(v, str)}
        labels |= {clean(v) for v in q['fig'].get('labs', {}).values()}
        for deg in re.findall(r'(\d+(?:\.\d+)?)°', q['ctx']):
            if deg not in labels:
                fails.append(f'{where}: the text states {deg}° but the figure does not label it')

        pts = figure_arc(q['fig'])
        for kind, arc, point in text_arc_claims(text):
            if kind == 'centre':
                continue    # checked against the derived centre angle below
            drawn = pts.get(point) if point else (next(iter(pts.values())) if len(pts) == 1 else None)
            if kind == 'opposite':
                arc = {'major': 'minor', 'minor': 'major'}[arc]
            if drawn is None:
                fails.append(f'{where}: the text says {arc} arc but the figure places no such point'
                             f'{" " + point if point else ""}')
            elif drawn != arc:
                flag = ' (its `inside` flag)' if q['fig']['t'] == 'centreCirc' else ''
                fails.append(f'{where}: the text puts {point or "the point"} on the {arc} arc, '
                             f'the figure draws it on the {drawn} arc{flag}')

        calc = bool(NUMERIC_KEY.match(q['correct']))
        if q['ask'].startswith('Find') and not calc:
            fails.append(f'{where}: asks "Find" but its key {q["correct"]!r} is not a number')
        if not calc:
            continue
        try:
            got = derive(q)
        except Unsolvable as e:
            fails.append(f'{where}: {e} ("{q["ctx"]}" / "{q["ask"]}")')
            continue
        except Exception as e:  # a shape this script cannot read is a failure, never a skip
            fails.append(f'{where}: could not derive ({type(e).__name__}: {e})')
            continue
        solved += 1
        for kind, arc, _p in text_arc_claims(text):
            if kind == 'centre' and (got < 180) != (arc == 'minor'):
                fails.append(f'{where}: the {arc} arc subtends {got}° at the centre')
        key = option_value(q['correct'])
        if sp.simplify(got - key) != 0:
            fails.append(f'{where}: keyed {q["correct"]!r}, the stated values give {got} '
                         f'("{q["ctx"]}" / "{q["ask"]}")')
        elif verbose:
            print(f'ok      {where}: {q["ask"]} = {q["correct"]}')
    return fails, solved


def selftest(bank):
    """Each injected fault must FAIL."""
    def find(pred):
        return next(i for i, (_, _, q) in enumerate(bank) if pred(q))

    def fault_old_q48(b):
        q = b[find(lambda q: q['fig']['t'] == 'centreCirc' and q['ask'] == 'Find x')][2]
        q['fig'].update(centreLab='2x', circLab='x + 15')
        q['correct'], q['d'] = '15', ['30', '7.5', '45']

    def fault_old_q19(b):
        q = b[find(lambda q: 'MAJOR arc side' in q['ctx'])][2]
        q['fig']['inside'] = True

    def fault_distractor(b):
        q = b[find(lambda q: q['correct'] == '108°')][2]
        q['d'][0] = '108'

    def fault_key(b):
        q = b[find(lambda q: q['correct'] == '108°')][2]
        q['correct'] = '107°'

    base = set(check(bank)[0])
    bad = []
    for name, fault in [('old Q48 numbers', fault_old_q48), ('Q19 inside:true', fault_old_q19),
                        ('a distractor equal to its key', fault_distractor), ('a changed key', fault_key)]:
        b = copy.deepcopy(bank)
        fault(b)
        fails = [f for f in check(b)[0] if f not in base]    # the fault must add a failure
        print(f'self-test {"caught " if fails else "MISSED "} {name}' + (f': {fails[0]}' if fails else ''))
        if not fails:
            bad.append(name)
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--file', default=PAGE, help='the page to check (default: the live game file)')
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()

    bank = load_bank(args.file)
    fails, solved = check(bank, args.verbose)
    for f in fails:
        print(f'FAIL    {f}')
    missed = [] if args.no_selftest else selftest(bank)
    for m in missed:
        print(f'FAIL    self-test did not catch: {m}')
    if fails or missed:
        print(f'\nFAILED: {len(fails)} finding(s), {len(missed)} self-test miss(es); '
              f'{len(bank)} questions, {solved} calculations solved')
        return 1
    print(f'\nPASS: {len(bank)} questions, {solved} calculation questions solved independently, '
          f'options and arc wording checked')
    return 0


if __name__ == '__main__':
    sys.exit(main())
