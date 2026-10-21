#!/usr/bin/env python3
# ci-line: Circle Theorem Spotter (every calculation key re-solved, SymPy + arc wording vs figure; each tangent angle drawn on the side the theorem needs, in Chromium) |
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
  - every figure with a marked tangent angle is rendered by the page's own FIG.render in Chromium
    and measured from the SVG it draws (SWEEP-1, circle-theorem-spotter-s1-001, Jon's ruling 13 Oct
    2026, SR-25): the angle between the tangent and a chord AB that the alternate segment theorem
    equates to the angle at C lies on the OTHER side of AB from C; the angle BAT beside a radius OA
    (90 degrees minus angle OAB) lies on B's side of OA. The marked arc must run from ray AB to ray AT,
    T being where the figure labels the tangent.
A fault-injection self-test (Q48's old numbers, Q19's old `inside` flag, a distractor equal to
its key, a changed key, and the old tangent figures planted back into the page) must FAIL each
time; it runs unless --no-selftest.

    python scripts/verify-circle-theorem-spotter.py [--file PATH] [--verbose] [--no-selftest]
"""
import argparse
import copy
import json
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


def load_bank_text(src):
    return load_bank(None, src)


def load_bank(path, src=None):
    if src is None:
        with open(path, encoding='utf-8') as fh:
            src = fh.read()
    tree, _src = bc.parse_game_source(src)
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


# --- the tangent figures, as drawn (Chromium) -----------------------------------------------------

FIG_JS = r"""() => {
  const out = [];
  QUESTIONS.gcse.forEach((q, i) => {
    const f = q.fig || {};
    if (!((f.t === 'altSegment' && f.tanLab) || (f.t === 'tangentRadius' && f.batLab))) return;
    const doc = new DOMParser().parseFromString(FIG.render(f), 'text/html');   // labels carry HTML entities (&deg;)
    const c = doc.querySelector('circle');
    const t = [...doc.querySelectorAll('text')].filter(e => e.textContent === 'T')
      .map(e => [+e.getAttribute('x'), +e.getAttribute('y')]);
    const arcs = [...doc.querySelectorAll('path')].map(e => e.getAttribute('d'));
    out.push({ i, ctx: q.ctx, fig: f, cx: +c.getAttribute('cx'), cy: +c.getAttribute('cy'),
               r: +c.getAttribute('r'), t, arcs });
  });
  return out;
}"""


def _side(p, q, r):
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 1e-9) - (v < -1e-9)


def _dir(v, p):
    import math
    return math.degrees(math.atan2(p[1] - v[1], p[0] - v[0])) % 360


def tangent_side_fails(figs):
    """[fail] for each tangent angle drawn on the wrong side (the figures FIG_JS reads)."""
    import math
    fails = []
    for g in figs:
        f, where = g['fig'], 'Q%d (%s)' % (g['i'] + 1, g['ctx'])
        pt = lambda d: (g['cx'] + g['r'] * math.cos(math.radians(d)), g['cy'] - g['r'] * math.sin(math.radians(d)))
        A, B, O = pt(270 if f.get('A') is None else f['A']), pt(f['B']), (g['cx'], g['cy'])
        if len(g['t']) != 1:
            fails.append('figure: %s: the tangent is labelled T %d times' % (where, len(g['t'])))
            continue
        T = (g['t'][0][0], g['t'][0][1] + 8)          # the label sits 8 px above the tangent's end
        # the marked arc at A runs from ray AB to ray AT
        want = sorted([_dir(A, B), _dir(A, T)])
        found = False
        for d in g['arcs']:
            m = re.match(r'M([-\d.]+) ([-\d.]+) A[-\d.]+ [-\d.]+ 0 \d \d ([-\d.]+) ([-\d.]+)', d or '')
            if not m:
                continue
            s_, e_ = (float(m.group(1)), float(m.group(2))), (float(m.group(3)), float(m.group(4)))
            if abs(math.dist(A, s_) - math.dist(A, e_)) > 0.5 or math.dist(A, s_) > 60:
                continue
            got = sorted([_dir(A, s_), _dir(A, e_)])
            if all(min(abs(a - b), 360 - abs(a - b)) < 2.5 for a, b in zip(got, want)):
                found = True
        if not found:
            fails.append('figure: %s: no marked arc runs from ray AB to ray AT' % where)
        if f['t'] == 'altSegment':
            C = pt(f['C'])
            if _side(A, B, T) == _side(A, B, C):
                fails.append('figure: %s: the tangent-chord angle is marked on C\'s side of AB, so the theorem gives '
                             'the angle at C as 180 degrees minus the label (SR-25)' % where)
        elif _side(O, A, T) != _side(O, A, B):
            fails.append('figure: %s: angle BAT is marked across OA from B, so it is 90 degrees PLUS angle OAB '
                         '(SR-25)' % where)
    return fails


def read_tangent_figures(html):
    """The page's tangent figures, rendered in Chromium from html (the page, or a planted copy)."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context()
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda u: not u.startswith(base) and '/katex@' not in u, lambda r: r.abort())
            ctx.route(lambda u: bool(page_url.search(u)), lambda r: r.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            pg = ctx.new_page()
            pg.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
            figs = pg.evaluate(FIG_JS)
            browser.close()
    finally:
        proc.terminate()
    return figs


# The old figures (before 13 Oct 2026), planted back: each must fail.
FIG_PLANTS = [
    ('the old alternate-segment figure (T always at t.a)',
     "const E = side(t.p, B, t.a) === side(t.p, B, C) ? t.b : t.a;", "const E = t.a;"),
    ('the old tangent-radius figure (T always at t.a)',
     "const E = o.B !== undefined && side(O, t.p, P(o.B)) !== side(O, t.p, t.a) ? t.b : t.a;", "const E = t.a;"),
]


def check_text(html, bank):
    """SWEEP-1 rulings (13 Oct 2026): what the page says is true of what it shows."""
    out = []
    # the <meta> description is generated from data/games.json (home lane); this checks what the page itself shows
    flat = re.sub(r'\s+', ' ', re.sub(r'<meta[^>]*>', '', html))
    if 'all seven circle theorems' in flat:   # s1-008 (R3): the options name eight properties
        out.append('text: the start screen says "all seven circle theorems"; the options name eight properties (circle-theorem-spotter-s1-008)')
    if re.search(r'class="hud-label">Time<', html) or 'id="timer"' in html or 'setInterval(tick' in html:
        out.append('hud: Hidden Count-Up (timer policy) means no running Time in the HUD (R7, circle-theorem-spotter-s1-007)')
    for _, _, q in bank:
        opts = [q['correct']] + list(q['d'])
        if any(re.search(r'\\sqrt\{\d+\} cm', o) for o in opts):   # s1-006 (R1): "cm" in a root's TeX is italic maths
            out.append('option: %r writes "cm" as maths run into the root; use \\text{ cm} (circle-theorem-spotter-s1-006)' % opts)
        if q['ask'].startswith('Which theorem') and re.search(r'\b(?:What|what|How|how)\b[^.?]*\?\s*$', q['ctx']):
            out.append('item: the context asks %r but the ask is "Which theorem?" (circle-theorem-spotter-s1-005)' % q['ctx'][:70])
        if 'what shape' in q['ctx']:   # s1-010: the key is a fact about the chord, not a shape
            out.append('item: the context asks "what shape" but the key is %r (circle-theorem-spotter-s1-010)' % q['correct'])
        if q['fig'].get('t') == 'semicircle' and q['ask'] == 'Which theorem does this diagram show?' and 'Angle at centre theorem' in q['d']:
            out.append('item: the semicircle figure offers "Angle at centre theorem" (the 180 degree case), a true option (R5, circle-theorem-spotter-s1-003)')
    return out

COPY = 'Spot and apply the circle theorems, with a diagram on every question.'
CARD = 'The circle theorems. Name the theorem, calculate the angle, state the reason.'


def read_copies(page_html):
    """Every hand-copied statement of the game's scope: games.json, the page <meta>s, the portal cards."""
    root = os.path.dirname(HERE)
    games = json.load(open(os.path.join(root, 'data', 'games.json'), encoding='utf-8'))
    games = games.get('games', games) if isinstance(games, dict) else games
    desc = next(g['description'] for g in games if g.get('slug') == SLUG)
    metas = re.findall(r'<meta (?:name="description"|property="og:description") content="([^"]*)"', page_html)
    portal = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
    cards = [re.search(r'class="card-desc">([^<]*)<', c).group(1)
             for c in re.findall(r'<a href="games/%s/[^>]*class="game-card".*?</a>' % SLUG, portal, re.S)]
    return {'games.json': [desc], 'meta': metas, 'portal card': cards}


def check_copies(copies):
    """s1-008: the options name eight properties, so no copy may count the theorems ('seven' or any figure)."""
    out = []
    want = {'games.json': COPY, 'meta': COPY + ' For GCSE. Free, no sign-up.', 'portal card': CARD}
    n = {'games.json': 1, 'meta': 2, 'portal card': 2}
    for where, texts in copies.items():
        if len(texts) != n[where]:
            out.append('copies: expected %d %s text(s), found %d' % (n[where], where, len(texts)))
        for t in texts:
            if re.search(r'seven', t, re.I):
                out.append('copies: %s says "seven": %r (circle-theorem-spotter-s1-008)' % (where, t))
            elif t != want[where]:
                out.append('copies: %s reads %r, expected %r' % (where, t, want[where]))
    return out


def copy_plants(copies):
    for where in copies:
        c = copy.deepcopy(copies)
        c[where][0] = c[where][0].replace('the circle', 'all seven circle', 1).replace('The circle', 'All seven circle', 1)
        yield 'old "all seven" back in %s' % where, c


TEXT_PLANTS = [
    ('"all seven circle theorems" back', "GCSE Higher — the circle theorems.", "GCSE Higher — all seven circle theorems."),
    ('the HUD Time back', '<div class="hud-item"><div class="hud-label">Score</div>', '<div class="hud-item"><div class="hud-label">Time</div><div class="hud-val" id="timer">0s</div></div><div class="hud-item"><div class="hud-label">Score</div>'),
    ('\\sqrt{119} cm back', "'\\\\sqrt{119}\\\\text{ cm}'", "'\\\\sqrt{119} cm'"),
    ('Q9 asking for an angle again', "The angle subtended at the circumference by the same arc is marked ?.", "What is the angle subtended at the circumference by the same arc?"),
    ('Q22 asking "what shape" again', "ctx:'The angle at the centre is 180°.'", "ctx:'If the angle at the centre is 180°, what shape is formed?'"),
    ('the true semicircle option back', "d:['Angles in same segment','Alternate segment theorem','Tangent-radius']}", "d:['Angle at centre theorem','Alternate segment theorem','Tangent-radius']}"),
]


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
    html = open(PAGE, encoding='utf-8').read()
    for name, old, new in TEXT_PLANTS:
        if html.count(old) != 1:
            print(f'self-test CANNOT PLANT {name}')
            bad.append(name)
            continue
        planted = html.replace(old, new)
        fails = check_text(planted, load_bank_text(planted))
        print(f'self-test {"caught " if fails else "MISSED "} {name}' + (f': {fails[0][:100]}' if fails else ''))
        if not fails:
            bad.append(name)
    for name, c in copy_plants(read_copies(html)):
        fails = check_copies(c)
        print(f'self-test {"caught " if fails else "MISSED "} {name}' + (f': {fails[0][:100]}' if fails else ''))
        if not fails:
            bad.append(name)
    for name, old, new in FIG_PLANTS:
        if html.count(old) != 1:
            print(f'self-test CANNOT PLANT {name}')
            bad.append(name)
            continue
        fails = tangent_side_fails(read_tangent_figures(html.replace(old, new)))
        print(f'self-test {"caught " if fails else "MISSED "} {name}' + (f': {fails[0]}' if fails else ''))
        if not fails:
            bad.append(name)
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
    figs = read_tangent_figures(open(args.file, encoding='utf-8').read())
    fails += tangent_side_fails(figs)
    fails += check_text(open(args.file, encoding='utf-8').read(), bank)
    fails += check_copies(read_copies(open(args.file, encoding='utf-8').read()))
    if len(figs) < 9:
        fails.append('figure: only %d tangent figures with a marked tangent angle read (expected 9)' % len(figs))
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
          f'options and arc wording checked; {len(figs)} tangent figures measured in Chromium')
    return 0


if __name__ == '__main__':
    sys.exit(main())
