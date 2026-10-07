#!/usr/bin/env python3
# ci-line: B4 | Component Crusher (every key from what the student is shown, diagrams measured from the canvas, marking through MaffsAnswer in Chromium) |
"""Component Crusher: every key recomputed from what the student is shown, every diagram measured, every answer marked.

The game (45 scenarios: gcse, alevel, level4, 15 each) shows a vector diagram and asks typed or multiple-choice
sub-questions. The tranche 4 audit of 6 Oct 2026 found 10 of the 15 Level 4 scenarios never showing their
vectors or points (3D drawn on 2D axes cannot be read), a bearing keyed for the wrong vector (143.1 for 126.9),
an angle keyed 79.6 for 79.7, a true distractor (C on AB's perpendicular bisector), tolerances wider than the
stated precision, no precision stated, a velocity drawn as (3, -2) for i + 2j, an arrow AB drawn from the
origin, raw LaTeX options, and a faint grid with endpoints between its lines.

The scenarios are read from the live page, then for every sub-question:
  Key: KEYS below says how the key follows from what the student is shown: a 2D vector read off the diagram
    (its data, which the canvas check below holds to the drawing), a Level 4 point or vector from the
    scenario's `given` (shown in words), or numbers stated in the prompt (each pinned and checked to be in it).
    The key is recomputed exactly (SymPy) and, where the prompt states "to N d.p.", rounded half up; the
    sub-question must carry dp = N, and a prompt with no stated precision must have an exact key (SR-1).
  Multiple choice: the keyed option and every wrong option carry a reviewed verdict with its reason; a wrong
    option may never be true (SR-16).
  Level 4: every scenario whose prompts do not state their own numbers shows its `given` data in the
    scenario box, and every key that reads a point or vector reads it from there (audit t4-001).
  Diagram (Chromium, recorded canvas calls): each arrow is drawn from its `from` to its `to`; a 2D arrow ends on
    grid lines (every whole unit is drawn) unless its label states it (10N at 30°); AL12's arrow is the prompt's
    v; L1's AB starts at A.
  Marking (Chromium, 390x844, through checkNum/checkVec/checkMCQ): the key typed as asked is right; one unit
    in its last place off is wrong; at a stated precision, the unrounded value is not marked (SR-3, 'format');
    every wrong option is wrong and the keyed one right. Options with LaTeX are rendered, never raw.
A self-test plants three of the audit's own faults back into a copy of the page (t4-002: the bearing 143.1;
t4-001: a Level 4 scenario's given removed; t4-004: the perpendicular-bisector option); each must FAIL.

    python scripts/verify-component-crusher.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'component-crusher'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
AUDIT = {'L1': 't4-001, t4-009', 'L2': 't4-001, t4-003', 'L3': 't4-001', 'L4': 't4-001', 'L5': 't4-001', 'L6': 't4-001',
         'L8': 't4-001', 'L11': 't4-001', 'L12': 't4-001', 'L14': 't4-001', 'AL11': 't4-002', 'AL2': 't4-004',
         'AL5': 't4-007', 'AL12': 't4-008', 'AL3': 't4-010', 'AL10': 't4-012', 'AL14': 't4-012', 'L7': 't4-012'}


class S:
    """What the student is shown in one scenario."""

    def __init__(self, q):
        self.q = q

    def V(self, label):           # a drawn vector, to - from
        [v] = [v for v in self.q['vectors'] if v['label'] == label]
        return sp.Matrix([sp.nsimplify(t) - sp.nsimplify(f) for f, t in zip(v['from'], v['to'])])

    def P(self, label):           # a drawn point
        [p] = [p for p in self.q['points'] if p['l'] == label]
        return sp.Matrix([sp.nsimplify(c) for c in p['c']])

    def G(self, name):            # a Level 4 given (point or vector), shown in words
        return sp.Matrix([sp.nsimplify(c) for c in self.q['given'][name]])


def M(*c):
    return sp.Matrix([sp.nsimplify(x) for x in c])


def mag(v):
    return sp.sqrt(v.dot(v))


def ang(a, b):
    return sp.acos(a.dot(b) / (mag(a) * mag(b))) * 180 / sp.pi


def MC(correct_why, wrong):
    """A multiple-choice sub-question: the keyed option's reason, and each wrong option's reason it is false."""
    return ('mcq', correct_why, wrong)


# Each sub-question, in order: a function of S giving the exact key (a vector or a number), or MC(...).
# 'stated' lists text the prompt must contain when the key uses numbers the prompt states.
KEYS = {
    'G1': [lambda s: s.V('a'), lambda s: mag(s.V('a')), lambda s: s.V('a') + s.V('b'), lambda s: 2 * s.V('a') - s.V('b')],
    'G2': [lambda s: s.V('a') + s.V('b'), lambda s: mag(s.V('a') + s.V('b')), lambda s: 3 * s.V('b')],
    'G3': [lambda s: s.P('B') - s.P('A'), lambda s: s.P('C') - s.P('B'),
           MC('AB = BC: parallel, sharing B', {'No — they form a triangle': 'AB = BC, so the points are on one line',
                                               'Only if |AB| = |BC|': 'collinear needs parallel and a shared point, not equal lengths',
                                               'Cannot tell from vectors': 'the vectors show it'})],
    'G4': [lambda s: mag(s.V('a')), lambda s: -2 * s.V('a')],
    'G5': [lambda s: s.V('a') + s.V('b'), lambda s: mag(s.V('a') + s.V('b')),
           MC('b = (-3, -4) = -1/2 (6, 8)', {'No — they are perpendicular': 'a·b = -50, not 0',
                                             'Only if |a| = |b|': 'b = -a/2 whatever the lengths',
                                             'Cannot determine from diagram': 'the components show it'})],
    'G6': [lambda s: s.V(''), lambda s: -s.V('')],
    'G7': [lambda s: s.V('a') + s.V('b'), lambda s: 3 * s.V('a') - s.V('b'), lambda s: mag(s.V('a'))],
    'G8': [lambda s: s.P('B') - s.P('A'), lambda s: mag(s.P('B') - s.P('A'))],
    'G9': [lambda s: mag(s.V('p')), lambda s: s.V('p') / 2],
    'G10': [MC('(6, -8) = -2(-3, 4)', {'n = 2m': '2m = (-6, 8)', 'They are perpendicular': 'm·n = -50, not 0',
                                       'Cannot be expressed as a scalar multiple': 'n = -2m'}),
            lambda s: s.V('m') + s.V('n'), lambda s: mag(s.V('m') + s.V('n'))],
    'G11': [lambda s: 2 * s.V('a') + s.V('b'), lambda s: s.V('a') - 2 * s.V('b'), lambda s: mag(s.V('a') - 2 * s.V('b'))],
    'G12': [lambda s: s.P('B') - s.P('A'), lambda s: (s.P('B') - s.P('A')) / 2, lambda s: (s.P('A') + s.P('B')) / 2],
    'G13': [lambda s: mag(s.V('v'))],
    'G14': [lambda s: s.V('a') + 2 * s.V('b'), lambda s: 3 * s.V('a') - s.V('b')],
    'G15': [lambda s: s.V('a') + s.V('b') + s.V('-a'),
            MC('a + (-a) = 0', {'a and b are perpendicular': 'a·b = 5, not 0',
                                'The path forms a triangle': 'it ends at (-1, 4), not back at the start',
                                'Total is always zero': 'the total is b, (-1, 4)'})],
    'AL1': [lambda s: s.V('a').dot(s.V('b')), lambda s: ang(s.V('a'), s.V('b')), lambda s: s.V('a') / mag(s.V('a'))],
    'AL2': [lambda s: s.P('B') - s.P('A'), lambda s: s.P('C') - s.P('A'),
            MC('AC is half of AB, along it', {'C divides AB in the ratio 1 : 2': 'AC : CB = 1 : 1',
                                              'A, B, C form an equilateral triangle': 'they are on one line',
                                              'AC is perpendicular to AB': 'AC is parallel to AB'})],
    'AL3': [MC('through A = 2i + j, direction d', {
        '\\mathbf{r} = (3\\mathbf{i}-\\mathbf{j}) + t(2\\mathbf{i}+\\mathbf{j})': 'position and direction swapped',
        '\\mathbf{r} = t(2\\mathbf{i}+\\mathbf{j})': 'the line through O and A',
        '\\mathbf{r} = (2\\mathbf{i}+\\mathbf{j}) - t(3\\mathbf{i}+\\mathbf{j})': 'direction (-3, -1) is not parallel to (3, -1)'}),
            lambda s: s.P('A') + 3 * s.V('d')],
    'AL4': [lambda s: s.V('a').dot(s.V('b')), lambda s: ang(s.V('a'), s.V('b'))],
    'AL5': [lambda s: s.P('B') - s.P('A'), lambda s: mag(s.P('B') - s.P('A'))],
    'AL6': [lambda s: mag(s.V('p')), lambda s: s.V('p').dot(M(2, 1))],
    'AL7': [lambda s: s.V('a').dot(s.V('b')),
            MC('a·b = 1', {'Yes — they look perpendicular': 'a·b = 1, not 0', 'Only if |a| = |b|': 'lengths do not decide it',
                           'Cannot tell from dot product': 'a·b = 0 exactly when perpendicular'})],
    'AL8': [MC('b = -2a', {'They are perpendicular': 'a·b = -50', 'a·b = 0': 'a·b = -50', 'Cannot determine': 'b = -2a'}),
            lambda s: mag(s.V('a')), lambda s: mag(s.V('b'))],
    'AL9': [lambda s: s.V('F₁') + s.V('F₂'), lambda s: mag(s.V('F₁') + s.V('F₂'))],
    'AL10': [(lambda s: 10 * sp.cos(sp.pi / 6), ['10N at 30°']), (lambda s: 10 * sp.sin(sp.pi / 6), [])],
    'AL11': [lambda s: mag(s.V('v')),
             lambda s: (90 - sp.atan2(s.V('v')[1], s.V('v')[0]) * 180 / sp.pi) % 360],
    'AL12': [(lambda s: M(2, 3) + 5 * M(1, 2), ['r₀ = (2i+3j)', 'v = (i+2j)', 't = 5'])],
    'AL13': [lambda s: s.V('F₁') + s.V('F₂') + s.V('F₃'),
             MC('R = 0', {'The forces cancel in the i direction only': 'they cancel in both directions',
                          'All forces are equal': 'F₁, F₂, F₃ differ', 'The object accelerates': 'no net force, no acceleration'})],
    'AL14': [(lambda s: 15 * sp.sin(sp.pi / 3), ['15 m/s on bearing 060°']), (lambda s: 15 * sp.cos(sp.pi / 3), [])],
    'AL15': [(lambda s: M(3, 4) + 2 * M(0, -10), ['u = (3i+4j)', 'a = (0i-10j)', 't = 2']),
             (lambda s: mag(M(3, 4) + 2 * M(0, -10)), [])],
    'L1': [lambda s: s.G('B') - s.G('A'), lambda s: mag(s.G('B') - s.G('A'))],
    'L2': [lambda s: s.G('a').dot(s.G('b')), lambda s: ang(s.G('a'), s.G('b'))],
    'L3': [lambda s: s.G('F_1') + s.G('F_2') + s.G('F_3'), lambda s: mag(s.G('F_1') + s.G('F_2') + s.G('F_3'))],
    'L4': [lambda s: s.G('End') - s.G('Start'), lambda s: mag(s.G('End') - s.G('Start'))],
    'L5': [lambda s: mag(s.G('v')), lambda s: s.G('v').dot(M(2, 1, -1))],
    'L6': [lambda s: s.G('B') - s.G('A'), lambda s: s.G('C') - s.G('B'),
           MC('AB = BC, sharing B', {'No — different magnitudes': '|AB| = |BC|', 'Only in 2D': 'collinearity is the same test in 3D',
                                     'Cannot determine in 3D': 'AB = BC shows it'})],
    'L7': [(lambda s: 10 * sp.cos(sp.pi / 4), ['10N at 45°']), (lambda s: 10 * sp.sin(sp.pi / 4), [])],
    'L8': [lambda s: s.G('a').dot(s.G('b')), lambda s: mag(s.G('a')), lambda s: mag(s.G('b')), lambda s: ang(s.G('a'), s.G('b'))],
    'L9': [(lambda s: M(1 + 2 * 2, 3 - 2, 2 + 3 * 2), ['r = (1+2t)i + (3-t)j + (2+3t)k', 't = 2']),
           (lambda s: M(2, -1, 3), [])],
    'L10': [(lambda s: 500 * M(3, 4, 0)[0] / mag(M(3, 4, 0)), ['500N along \\(3\\mathbf{i}+4\\mathbf{j}\\)']),
            (lambda s: 500 * M(3, 4, 0)[1] / mag(M(3, 4, 0)), [])],
    'L11': [lambda s: s.G('F_1') + s.G('F_2') + s.G('F_3'),
            MC('R = 18k, vertical', {'The mast will topple': 'nothing in R says so', 'All forces are equal': 'they differ',
                                     'Net force is zero': 'R = 18k'})],
    'L12': [lambda s: mag(s.G('s')), lambda s: s.G('s').dot(M(1, 1, 1))],
    'L13': [(lambda s: M(2, 3, 1) + 3 * M(1, -1, 2), ['u = (2i+3j+k)', 'a = (i-j+2k)', 't = 3']),
            (lambda s: mag(M(2, 3, 1) + 3 * M(1, -1, 2)), [])],
    'L14': [lambda s: s.G('Q') - s.G('P'), lambda s: s.G('R') - s.G('Q'),
            MC('PQ = QR, sharing Q', {'No': 'PQ = QR', 'Only if magnitudes differ': 'they are equal', 'Insufficient information': 'PQ = QR shows it'})],
    'L15': [(lambda s: 5 - 3, ['F₁ = (ai+2j-k)', 'F₂ = (3i-j+bk)', 'Resultant = (5i+j+2k)']), (lambda s: 2 - (-1), [])],
}
# Level 4 scenarios whose prompts state their own numbers need no `given`.
L4_STATED = {'L7', 'L9', 'L10', 'L13', 'L15'}


def rnd(v, dp):
    return Decimal(str(sp.N(v, 40))).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)


def stated_dp(prompt):
    m = re.search(r'to ([12]) d\.p\.', prompt)
    return int(m.group(1)) if m else None


def check_bank(fails, scen, extra=None):
    plan = []
    for lv in ('gcse', 'alevel', 'level4'):
        for q in scen[lv]:
            sid = q['id']
            w = '%s%s' % (sid, ' (component-crusher-%s)' % AUDIT[sid] if sid in AUDIT else '')
            keys = KEYS.get(sid)
            if keys is None or len(keys) != len(q['sqs']):
                fails.append('%s: no reviewed KEYS for its %d sub-questions' % (w, len(q['sqs'])))
                continue
            st = S(q)
            if lv == 'level4' and sid not in L4_STATED and not q.get('given'):
                fails.append('%s: the scenario shows no data: its points and vectors are only drawn on a 2D projection' % w)
                continue
            for i, (sq, k) in enumerate(zip(q['sqs'], keys)):
                ww = '%s.%d' % (w, i + 1)
                if isinstance(k, tuple) and k[0] == 'mcq':
                    _, why, wrong = k
                    if set(sq['wrong']) != set(wrong):
                        fails.append('%s: wrong options %s, reviewed %s' % (ww, sq['wrong'], sorted(wrong)))
                    plan.append({'sid': sid, 'i': i, 'type': 'mcq', 'correct': sq['correct'], 'wrong': sq['wrong']})
                    continue
                fn, stated = (k if isinstance(k, tuple) else (k, []))
                for t in stated:
                    if t not in sq['prompt'] and t not in q['sqs'][0]['prompt']:
                        fails.append('%s: the key uses "%s", which the prompt does not state' % (ww, t))
                try:
                    v = fn(st)
                except (KeyError, ValueError, TypeError) as e:
                    fails.append('%s: the key cannot be read from what is shown (%s)' % (ww, e))
                    continue
                dp = stated_dp(sq['prompt'])
                if sq.get('dp') != dp:
                    fails.append('%s: the prompt states %s d.p., the sub-question marks at %s' % (ww, dp, sq.get('dp')))
                vals = list(v) if isinstance(v, sp.Matrix) else [v]
                stored = sq['answers'] if sq['type'] in ('vec2', 'vec3') else [sq['answer']]
                if len(vals) != len(stored):
                    fails.append('%s: %d components keyed, %d recomputed' % (ww, len(stored), len(vals)))
                    continue
                for a, b in zip(vals, stored):
                    if dp is None:
                        if not sp.nsimplify(a).is_Rational:
                            fails.append('%s: the key %s is not exact and the prompt states no precision (SR-1)' % (ww, sp.N(a, 8)))
                        elif sp.nsimplify(a) != sp.nsimplify(b):
                            fails.append('%s: keyed %s, recomputed %s' % (ww, b, a))
                    elif rnd(a, dp) != Decimal(str(b)).quantize(Decimal(1).scaleb(-dp)):
                        fails.append('%s: keyed %s, recomputed %s to %d d.p.' % (ww, b, rnd(a, dp), dp))
                plan.append({'sid': sid, 'i': i, 'type': sq['type'], 'keys': [str(x) for x in stored], 'dp': dp,
                             'exact': [str(sp.N(a, 12)) for a in vals]})
    return plan


SWEEP_JS = r"""(plan) => {
  const queue = []; window.setTimeout = (f) => { queue.push(f); return 0; }; window.setInterval = () => 0;
  const C = CanvasRenderingContext2D.prototype, rec = [];
  for (const k of ['moveTo', 'lineTo']) { const f = C[k]; C[k] = function(...a){ rec.push([k, a[0], a[1]]); return f.apply(this, a); }; }
  const all = {}; for (const lv of ['gcse','alevel','level4']) for (const q of SCENARIOS[lv]) all[q.id] = [lv, q];
  const out = {draw: {}, given: {}, marks: []};
  const open = (sid, i) => { const [lv, q] = all[sid]; G.level = lv; G.questions = [q]; G.qIdx = 0; G.score = 0; G.total = 0; G.correct = 0;
    rec.length = 0; loadScenario(); G.sqIdx = i; loadSQ(q); return q; };
  for (const sid of Object.keys(all)) {
    open(sid, 0);
    out.draw[sid] = rec.slice();
    const g = document.getElementById('scenarioGiven');
    out.given[sid] = g ? [...g.querySelectorAll('annotation')].map(a => a.textContent) : null;
    const cv = document.getElementById('vecCanvas');
    out.draw[sid] = {rec: out.draw[sid], w: parseFloat(cv.style.width), h: parseFloat(cv.style.height)};
  }
  const fbClass = () => { const f = document.querySelector('#sqFb .feedback'); return f ? f.className : ''; };
  for (const p of plan) {
    if (p.type === 'mcq') {
      for (const opt of [p.correct, ...p.wrong]) {
        const q = open(p.sid, p.i);
        const opts = document.getElementById('qBox')._opts;
        const k = opts.findIndex(o => o.text === opt);
        const btn = document.getElementById('mc' + k);
        const raw = !btn.querySelector('.katex') && /\\[A-Za-z]/.test(btn.textContent);
        btn.click();
        out.marks.push({sid: p.sid, i: p.i, typed: opt, got: /correct/.test(fbClass()) ? 'correct' : 'wrong', want: opt === p.correct ? 'correct' : 'wrong', raw});
      }
      continue;
    }
    const n = p.keys.length;
    const tries = [[p.keys, 'correct']];
    // one unit in the last place off, on the first component
    const unit = p.dp ? Math.pow(10, -p.dp) : 1;
    const off = p.keys.slice(); off[0] = (Number(off[0]) + unit).toFixed(p.dp || (String(off[0]).split('.')[1] || '').length);
    tries.push([off, 'wrong']);
    if (p.dp) { const ex = p.keys.slice(); ex[0] = Number(p.exact[0]).toFixed(p.dp + 3); tries.push([ex, 'unmarked']); }
    for (const [vals, want] of tries) {
      open(p.sid, p.i);
      for (let j = 0; j < n; j++) document.getElementById('v' + j).value = String(vals[j]);
      const before = G.total;
      if (p.type === 'num') checkNum(); else checkVec(n);
      const got = G.total === before ? 'unmarked' : (/correct/.test(fbClass()) ? 'correct' : 'wrong');
      out.marks.push({sid: p.sid, i: p.i, typed: vals.join(', '), got, want});
    }
  }
  return out;
}"""


KATEX_DIR = None   # --katex-dir: serve KaTeX from a local copy (a sandbox that refuses the CDN)


def check_page(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            # every request off the stub server is aborted, except KaTeX (options and the given data render with it)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof SCENARIOS === "object" && typeof loadScenario === "function"', timeout=8000)
            scen = page.evaluate('() => SCENARIOS')
            plan = check_bank(fails, scen)
            res = page.evaluate(SWEEP_JS, plan)
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    for m in res['marks']:
        if m['got'] != m['want']:
            fails.append('%s.%d in Chromium: typed/picked %r, marked %s, expected %s' % (m['sid'], m['i'] + 1, m['typed'], m['got'], m['want']))
        if m.get('raw'):
            fails.append('%s.%d in Chromium: an option shows raw LaTeX: %r (component-crusher-t4-010)' % (m['sid'], m['i'] + 1, m['typed']))
    for lv in ('gcse', 'alevel', 'level4'):
        for q in scen[lv]:
            sid = q['id']
            if lv == 'level4' and q.get('given'):
                shown = read_given(res['given'].get(sid) or [])
                want = {re.sub(r'_(\d)$', r'_{\1}', k): list(v) for k, v in q['given'].items()}
                if shown != want:
                    fails.append('%s in Chromium: the scenario box shows %s, the data is %s' % (sid, shown, want))
            check_drawing(fails, q, res['draw'][sid])
    if errors:
        fails.append('page errors: %s' % '; '.join(errors[:3]))
    return scen


def read_given(texs):
    """The scenario box's KaTeX sources read back to {name: coordinates}."""
    out = {}
    for t in texs:
        lhs, rhs = [x.strip() for x in t.split('=', 1)]
        name = re.sub(r'\\(mathbf|text)\{([^}]*)\}', r'\2', lhs)
        if rhs.startswith('('):
            out[name] = [int(x) for x in re.findall(r'-?\d+', rhs)]
        else:
            c = {'i': 0, 'j': 0, 'k': 0}
            for sg, num, u in re.findall(r'([+-]?)\s*(\d*)\\mathbf\{([ijk])\}', rhs):
                c[u] = (-1 if sg == '-' else 1) * (int(num) if num else 1)
            out[name] = [c['i'], c['j'], c['k']]
    return out


def check_drawing(fails, q, d):
    """Each arrow's shaft is drawn from tx/ty(from) to tx/ty(to), with the page's own axis map."""
    import math
    sid, rec = q['id'], d['rec']
    w, h = d['w'], d['h']
    pad = {'l': 40, 'r': 15, 't': 15, 'b': 30}
    pw, ph = w - pad['l'] - pad['r'], h - pad['t'] - pad['b']
    x0, x1, y0, y1 = (-2, 10, -10, 10) if q.get('grid3d') else (q['grid']['x'][0], q['grid']['x'][1], q['grid']['y'][0], q['grid']['y'][1])
    tx = lambda x: pad['l'] + (x - x0) / (x1 - x0) * pw
    ty = lambda y: pad['t'] + (1 - (y - y0) / (y1 - y0)) * ph
    segs = [(rec[i][1:], rec[i + 1][1:]) for i in range(len(rec) - 1) if rec[i][0] == 'moveTo' and rec[i + 1][0] == 'lineTo']
    if q.get('grid3d') is not True:
        for x in range(math.ceil(x0), int(math.floor(x1)) + 1):
            if not any(abs(a[0] - tx(x)) < 1e-6 and abs(b[0] - tx(x)) < 1e-6 for a, b in segs):
                fails.append('%s: no grid line at x = %d (component-crusher-t4-013)' % (sid, x))
                break
    for v in q['vectors']:
        def proj(p):
            if q.get('grid3d'):
                return (p[0] + p[2] * 0.8 * math.cos(math.pi / 6), p[1] + p[2] * 0.8 * math.sin(math.pi / 6))
            return (p[0], p[1])
        (fx, fy), (ex, ey) = proj(v['from']), proj(v['to'])
        A, B = (tx(fx), ty(fy)), (tx(ex), ty(ey))
        found = any(abs(a[0] - A[0]) < 1e-6 and abs(a[1] - A[1]) < 1e-6 and abs(b[0] - B[0]) < 1e-6 and abs(b[1] - B[1]) < 1e-6
                    for a, b in segs)
        if not found:
            fails.append('%s%s: the arrow %r from %s to %s is not drawn there'
                         % (sid, ' (component-crusher-%s)' % AUDIT[sid] if sid in AUDIT else '', v['label'], v['from'], v['to']))
        if not q.get('grid3d') and not re.search(r'\d', v['label'] or ''):
            if any(abs(c - round(c)) > 1e-9 for c in list(v['from']) + list(v['to'])):
                fails.append('%s: the arrow %r ends between grid lines' % (sid, v['label']))


PLANTS = [
    ('AL11', 't4-002: the bearing keyed 143.1', "answer:126.9,dp:1}", "answer:143.1,dp:1}"),
    ('L2', 't4-001: a Level 4 scenario with its given removed', "   given:{a:[2,1,-2],b:[3,-2,1]},\n", ""),
    ('AL2', 't4-004: the true option "C is on the perpendicular bisector"',
     "'C divides AB in the ratio 1 : 2'", "'C is on the perpendicular bisector'"),
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
    scen = check_page(fails, html)
    n = sum(len(q['sqs']) for lv in scen for q in scen[lv]) if scen else 0
    print('%s: %d sub-questions in 45 scenarios: keys from what is shown, diagrams measured, every answer marked in Chromium'
          % (SLUG, n))
    ok = True
    if not args.no_selftest and not args.against:
        for sid, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-62s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            check_page(rep, html.replace(old, new))
            hit = [f for f in rep if f.startswith(sid + ' ') or f.startswith(sid + '.')]
            ok = ok and bool(hit)
            print('  self-test %-62s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
