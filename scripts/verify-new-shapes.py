#!/usr/bin/env python3
# ci-line: New Shapes (every formula, key, substitution and working step recomputed; the figure's labels checked against the item; every item answered right and wrong in Chromium) |
"""New Shapes: area of a parallelogram and a trapezium, volume of a prism, from a formula, a diagram and values.

Three static banks, read from the page as served: PARALLELOGRAM (15), TRAPEZIUM (20) and PRISM (15). Each item names a
formula, its variables and values, the variable asked for, the key and the working steps shown after a wrong answer
(KaTeX). The student types a whole number on the numpad; the mark is an exact match.

Checks, independent of the game's code:
  Formula: each item's name is one of three known formulas (A = b x h; A = 1/2 (a + b) x h; V = A x l), held in this
    file with its variables in order, result variable and section. The key is the formula worked out from the item's own
    values with fractions.Fraction, and is a whole number. formulaKatex is read as maths and gives the key.
  Working: the first step is the formula as printed; every later step has the same left-hand side and a right-hand
    side worth exactly the key; the substitution step uses the formula's own numbers plus the item's values and no
    others; the last step is "LHS = key".
  Bank: ids unique; section matches the formula; no formula with the same values twice.
  Sessions: startGame() at 10, 20 and 30 (three draws each) deals that many different items in the split 3/4/3,
    6/8/6 and 9/12/9 (parallelogram/trapezium/prism).
  Figure (SR-25: the words, the figure and the key agree), in Chromium: the diagram the game draws carries the item's
    own numbers: parallelogram labels "b = B" and "h = H", trapezium "a = ..", "b = .." and "h = ..", prism "A = .." in
    the cross-section and "l = .." under it, and its accessible description names the same values.
  Marking, in Chromium (390x844, KaTeX served from the pinned local copy), every item shown by the game's own
    loadQuestion() (formula TeX read from KaTeX's annotation, variables line, prompt): the key typed on the numpad and
    submitted reads "Correct!" and is counted; each wrong answer (key +-1 and the usual slips: adding for multiplying,
    forgetting the half, ...) reads "Not quite - the answer is [key]", is not counted, and shows the item's working.
The h label (SWEEP-1 new-shapes-s1-001, Part 2 #1): on every parallelogram and trapezium it sits just to the left of the dashed height
  line and wholly inside the figure, so it cannot be read as the slant length; the outline is measured in Chromium.
Not asserted, because the findings are still open and the redraw is a design call for Jon: the diagram's PROPORTIONS
(parallelogram always 180x100, trapezium top always half the base, prism cross-section always a square: t3-003,
t3-004, r-001) and the prism's l arrow, which spans the front width plus the depth rather than the depth edge (r-001,
t3-005). The numbers on the diagram are checked; its geometry is not.
The reveal screen (new-shapes-t3-007; Jon's ruling, 18 Oct 2026): it states what the bank teaches, the number of new
  area formulae (distinct "Area of ..." formulas) in words and the one volume formula, the prism's: "You now know two
  new area formulae and the volume of a prism." (It said "five area formulae and one volume formula".)
The score slot (new-shapes-t3-008): in a session played right, wrong, right, the header's "n/m" reads 0/0 before the
  first answer and then this file's own count of right answers over answers given (1/1, 1/2, 2/3), after each answer
  and on the next question; never questions done.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong key (first parallelogram 25), a wrong answer
marked right (within 1), a wrong working figure, a wrong formula text (prism V = A + l), a wrong number in the
diagram's description, the reveal screen's old "five area formulae" and the score slot counting questions done (t3-008).

    python scripts/verify-new-shapes.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from collections import Counter
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'new-shapes'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
SESSIONS = {10: (3, 4, 3), 20: (6, 8, 6), 30: (9, 12, 9)}
SECTIONS = ('parallelogram', 'trapezium', 'prism')
DEALS = 3
# name: (section, variables in order, result variable, the formula worked out by this file)
FORMULAS = {
    'Area of a parallelogram': ('parallelogram', ['b', 'h'], 'A', lambda v: v['b'] * v['h']),
    'Area of a trapezium': ('trapezium', ['a', 'b', 'h'], 'A', lambda v: F(1, 2) * (v['a'] + v['b']) * v['h']),
    'Volume of a prism': ('prism', ['A', 'l'], 'V', lambda v: v['A'] * v['l']),
}
SLIPS = {
    'Area of a parallelogram': {'adds': lambda v: v['b'] + v['h'], 'halves': lambda v: F(v['b'] * v['h'], 2)},
    'Area of a trapezium': {'forgets the half': lambda v: (v['a'] + v['b']) * v['h'],
                            'adds the three': lambda v: v['a'] + v['b'] + v['h'],
                            'multiplies the three': lambda v: v['a'] * v['b'] * v['h']},
    'Volume of a prism': {'adds': lambda v: v['A'] + v['l'], 'divides': lambda v: F(v['A'], v['l'])},
}


def to_python(rhs):
    s = re.sub(r'\\text\{(\w+)\}', r'\1', rhs)
    s = s.replace('\\tfrac{1}{2}', '(1/2)').replace('\\times', '*').replace('\\div', '/')
    s = re.sub(r'\^(\d+)', r'**\1', s)
    s = re.sub(r'(\d|\))\s*([A-Za-z(])', r'\1*\2', s)
    return re.sub(r'(?<![A-Za-z_])(\d+)', r'F(\1)', s)


def value(rhs, env):
    return eval(to_python(rhs), {'__builtins__': {}, 'F': F}, {k: F(v) for k, v in env.items()})


def split_step(step):
    lhs, _, rhs = step.partition(' = ')
    return lhs.strip(), rhs.strip()


def numbers(rhs):
    return Counter(re.findall(r'(?<![A-Za-z_])\d+', re.sub(r'\\text\{\w+\}', '', rhs)))


def check_item(fails, q):
    where = '%s (%s)' % (q['id'], q['formulaName'])
    if q['formulaName'] not in FORMULAS:
        fails.append('%s: formula not known to this verifier' % where)
        return
    section, names, resvar, fn = FORMULAS[q['formulaName']]
    vs = q['variables']
    if q.get('section') != section:
        fails.append('%s: section %r, expected %r' % (where, q.get('section'), section))
    if [v['name'] for v in vs] != names or q['resultVar'] != resvar:
        fails.append('%s: variables %r / result %r, expected %r / %r' % (
            where, [v['name'] for v in vs], q['resultVar'], names, resvar))
        return
    env = {v['name']: F(v['value']) for v in vs}
    key = fn(env)
    if key.denominator != 1:
        fails.append('%s: the formula gives %s, not a whole number' % (where, key))
    if F(q['answer']) != key:
        fails.append('%s: keyed %s, recomputed %s' % (where, q['answer'], key))
    steps = q['workingSteps']
    lhs, rhs = split_step(q['formulaKatex'])
    if lhs != resvar:
        fails.append('%s: the formula text starts %r, not the result variable' % (where, lhs))
    try:
        if value(rhs, env) != key:
            fails.append('%s: formula text %r with the values gives %s, not %s' % (where, q['formulaKatex'], value(rhs, env), key))
    except Exception as e:
        fails.append('%s: formula text %r could not be read: %s' % (where, q['formulaKatex'], e))
        return
    if not steps or steps[0] != q['formulaKatex']:
        fails.append('%s: the first working step is not the formula as printed' % where)
    for i, st in enumerate(steps[1:], 2):
        l2, r2 = split_step(st)
        if l2 != lhs:
            fails.append('%s: step %d starts %r, expected %r' % (where, i, l2, lhs))
        try:
            if value(r2, {}) != key:
                fails.append('%s: step %d (%s) is worth %s, not the key %s' % (where, i, st, value(r2, {}), key))
        except Exception as e:
            fails.append('%s: step %d (%s) could not be read: %s' % (where, i, st, e))
    if len(steps) >= 2:
        want = numbers(rhs) + Counter(str(v['value']) for v in vs)
        got = numbers(split_step(steps[1])[1])
        if got != want:
            fails.append('%s: the substitution step %r uses the numbers %s, expected %s' % (
                where, steps[1], dict(got), dict(want)))
    if steps and steps[-1] != '%s = %s' % (lhs, q['answer']):
        fails.append('%s: the last step is %r, not "%s = %s"' % (where, steps[-1], lhs, q['answer']))


def check_bank(fails, bank):
    ids, seen = set(), set()
    for q in bank:
        if q['id'] in ids:
            fails.append('%s: id repeated' % q['id'])
        ids.add(q['id'])
        k = (q['formulaName'], tuple(v['value'] for v in q['variables']))
        if k in seen:
            fails.append('%s: the same formula and values appear twice' % q['id'])
        seen.add(k)
        check_item(fails, q)


def wrong_answers(q):
    section, names, _, fn = FORMULAS[q['formulaName']]
    env = {v['name']: F(v['value']) for v in q['variables']}
    key = fn(env)
    out = {'key + 1': key + 1, 'key - 1': key - 1}
    for what, f in SLIPS[q['formulaName']].items():
        out[what] = F(f(env))
    return {k: v for k, v in out.items() if v != key and v.denominator == 1 and 0 <= v < 10 ** 7}


def figure_expected(q):
    """What the drawn diagram must say for this item: its labels in order, its SVG text, its accessible description."""
    v = {x['name']: x['value'] for x in q['variables']}
    if q['section'] == 'parallelogram':
        return {'labels': ['b = %d' % v['b'], 'h = %d' % v['h']], 'svg': [],
                'aria': 'Parallelogram with base %d and height %d' % (v['b'], v['h'])}
    if q['section'] == 'trapezium':
        return {'labels': ['a = %d' % v['a'], 'b = %d' % v['b'], 'h = %d' % v['h']], 'svg': [],
                'aria': 'Trapezium with parallel sides %d and %d, height %d' % (v['a'], v['b'], v['h'])}
    return {'labels': ['l = %d' % v['l']], 'svg': ['A = %d' % v['A']],
            'aria': 'Prism with cross-section area %d and length %d' % (v['A'], v['l'])}


MARK_JS = r"""(args) => {
  const [q, typed] = args;
  sessionQuestions = [q]; currentIndex = 0; correctCount = 0; revealShown = false;
  showScreen('gameScreen');
  loadQuestion();
  const tex = el => [...el.querySelectorAll('annotation')].map(a => a.textContent);
  const sc = document.getElementById('shapeContainer');
  const shown = {formula: tex(document.getElementById('formulaKatex')), vars: document.getElementById('varsLine').textContent,
                 prompt: document.getElementById('questionPrompt').textContent,
                 name: document.getElementById('formulaName').textContent,
                 labels: [...sc.querySelectorAll('.shape-label')].map(e => e.textContent),
                 svg: [...sc.querySelectorAll('svg text')].map(e => e.textContent),
                 aria: (sc.querySelector('[role=img]') || {getAttribute: () => null}).getAttribute('aria-label')};
  // Where the h label sits (SWEEP-1 new-shapes-s1-001; Part 2 #1): its four corners, the figure's outline and the dashed
  // height line's x, all in viewport pixels.
  const geom = (() => {
    const wrap = sc.querySelector('.shape-container');
    const hl = [...sc.querySelectorAll('.shape-label')].find(e => /^h = /.test(e.textContent));
    if (!wrap || !hl) return null;
    const L = hl.getBoundingClientRect(), pg = sc.querySelector('.parallelogram-shape');
    const corners = [[L.left, L.top], [L.right, L.top], [L.right, L.bottom], [L.left, L.bottom]];
    if (pg) {
      // the figure is scaled down on a phone (its rect is narrower than its 260 px), so offsets are scaled to the viewport
      const W = wrap.getBoundingClientRect(), k = W.width / wrap.offsetWidth, m = new DOMMatrix(getComputedStyle(pg).transform);
      const cx = pg.offsetLeft + pg.offsetWidth / 2, cy = pg.offsetTop + pg.offsetHeight / 2;
      const poly = [[0, 0], [1, 0], [1, 1], [0, 1]].map(([u, w]) => {
        const dx = (u - 0.5) * pg.offsetWidth, dy = (w - 0.5) * pg.offsetHeight;
        return [W.left + k * (cx + m.a * dx + m.c * dy), W.top + k * (cy + m.b * dx + m.d * dy)]; });
      return {corners: corners, poly: poly, scale: k, line: sc.querySelector('.parallelogram-height').getBoundingClientRect().left, right: L.right};
    }
    const svg = sc.querySelector('svg'), S = svg.getBoundingClientRect(), k = S.width / svg.viewBox.baseVal.width;
    const poly = svg.querySelector('polygon').getAttribute('points').trim().split(/\s+/)
      .map(pt => pt.split(',').map(Number)).map(([x, y]) => [S.left + k * x, S.top + k * y]);
    return {corners: corners, poly: poly, scale: k, line: svg.querySelector('line').getBoundingClientRect().left, right: L.right};
  })();
  shown.geom = geom;
  for (const ch of typed) numInput(ch);
  submitAnswer();
  MaffsLock.clearTimers();
  return {shown: shown, count: correctCount, ind: document.getElementById('feedbackIndicator').textContent.trim(),
          ws: [...document.querySelectorAll('#workingSteps > div')].map(d => tex(d).join(''))};
}"""
SCORE_JS = r"""(plan) => {
  const slot = () => document.getElementById('scoreNum').textContent + '/' + document.getElementById('scoreTotal').textContent;
  selectSession(10); startGame(); MaffsLock.clearTimers();
  const out = [['start', slot()]];
  plan.forEach((right, i) => {
    const q = sessionQuestions[currentIndex];
    for (const ch of String(right ? q.answer : q.answer + 1)) numInput(ch);
    submitAnswer(); MaffsLock.clearTimers();
    out.push(['after answer ' + (i + 1), slot()]);
    nextQuestion(); MaffsLock.clearTimers();
    out.push(['question ' + (i + 2) + ' shown', slot()]);
  });
  return out;
}"""
SCORE_PLAN = [True, False, True]
DEAL_JS = r"""() => { const out = {};
  for (const n of %s) { out[n] = []; selectSession(n);
    for (let k = 0; k < %d; k++) { startGame(); out[n].push(sessionQuestions.map(q => q.id)); MaffsLock.clearTimers(); } }
  return out; }""" % (list(SESSIONS), DEALS)


def inside(pt, poly):
    """Is pt inside the convex polygon (the same side of every edge)?"""
    signs = []
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        signs.append((x2 - x1) * (pt[1] - y1) - (y2 - y1) * (pt[0] - x1))
    return all(s >= 0 for s in signs) or all(s <= 0 for s in signs)


def check_h_label(fails, where, q, geom):
    """Part 2 #1: the h label sits beside the dashed height line, wholly inside the figure, so it cannot be read as the
    slant length (it sat over the slanted side of every parallelogram and trapezium)."""
    if q['section'] not in ('parallelogram', 'trapezium'):
        return
    if not geom:
        fails.append('%s: no h label to place' % where)
        return
    if not all(inside(c, geom['poly']) for c in geom['corners']):
        fails.append('%s: the h label is not wholly inside the figure: it crosses a slanted side' % where)
    gap = (geom['line'] - geom['right']) / geom['scale']   # in the figure's own pixels
    if not 0 <= gap <= 14:
        fails.append('%s: the h label is %.0f px from the dashed height line, not just to its left' % (where, gap))


def mark_all(fails, page, bank):
    for q in bank:
        section, names, resvar, fn = FORMULAS[q['formulaName']]
        env = {v['name']: F(v['value']) for v in q['variables']}
        key = fn(env)
        cases = [('the key', key, True)] + [(k, v, False) for k, v in wrong_answers(q).items()]
        want_fig = figure_expected(q)
        for what, val, right in cases:
            got = page.evaluate(MARK_JS, [q, str(int(val))])
            where = '%s, %s typed (%s)' % (q['id'], what, int(val))
            sh = got['shown']
            if what == 'the key':
                check_h_label(fails, where, q, sh.get('geom'))
            wantvars = ', '.join('%s = %s' % (v['name'], v['value']) for v in q['variables'])
            if sh['formula'] != [q['formulaKatex']] or sh['vars'] != wantvars or sh['prompt'] != 'What is %s?' % q['resultVar'] \
                    or sh['name'] != q['formulaName']:
                fails.append('%s: the question shows %r' % (where, sh))
            if (sh['labels'], sh['svg'], sh['aria']) != (want_fig['labels'], want_fig['svg'], want_fig['aria']):
                fails.append('%s: the diagram says labels %r, svg text %r, description %r; the item says %r' % (
                    where, sh['labels'], sh['svg'], sh['aria'], want_fig))
            if right:
                if not (got['ind'] == 'Correct!' and got['count'] == 1):
                    fails.append('%s: the key was not marked right (%r)' % (where, got))
            else:
                if not (got['ind'].startswith('Not quite') and got['ind'].endswith('the answer is %d' % key)
                        and got['count'] == 0 and got['ws'] == q['workingSteps']):
                    fails.append('%s: a wrong answer was not marked wrong with the verified answer and working (%r)' % (
                        where, got))


WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}


def check_score_slot(fails, page):
    got = page.evaluate(SCORE_JS, SCORE_PLAN)
    want, right = [('start', '0/0')], 0
    for i, r in enumerate(SCORE_PLAN):
        right += r
        want += [('after answer %d' % (i + 1), '%d/%d' % (right, i + 1)),
                 ('question %d shown' % (i + 2), '%d/%d' % (right, i + 1))]
    for (w, g) in zip(want, got):
        if tuple(g) != w:
            fails.append('score slot: at %s it reads %s, expected %s (right answers over answers given; t3-008)' % (
                w[0], g[1], w[1]))


def check_reveal(fails, bank, said):
    """The reveal line states the formulae the bank teaches (new-shapes-t3-007; Jon's ruling, 18 Oct 2026)."""
    names = {q['formulaName'] for q in bank}
    areas = sorted(n for n in names if n.startswith('Area of '))
    volumes = sorted(n for n in names if n.startswith('Volume of '))
    if volumes != ['Volume of a prism']:
        fails.append('reveal: the bank teaches volume formulae %r, not the prism\'s alone' % volumes)
        return
    want = 'You now know %s new area formulae and the volume of a prism.' % WORDS.get(len(areas), len(areas))
    if said != want:
        fails.append('reveal: the screen says %r; the bank teaches %d area formulae (%s) and the prism\'s volume: %r'
                     % (said, len(areas), ', '.join(areas), want))


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    bank = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)   # KaTeX from the pinned local copy
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof PARALLELOGRAM !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify([...PARALLELOGRAM, ...TRAPEZIUM, ...PRISM]))')
            check_bank(fails, bank)
            sec = {q['id']: q['section'] for q in bank}
            for n, deals in page.evaluate(DEAL_JS).items():
                for d in deals:
                    split = tuple(sum(1 for i in d if sec.get(i) == s) for s in SECTIONS)
                    if len(set(d)) != len(d) or split != SESSIONS[int(n)] or not set(d) <= set(sec):
                        fails.append('a %s-question session is %r (split %r, expected %r)' % (n, d[:4], split, SESSIONS[int(n)]))
            mark_all(fails, page, bank)
            check_score_slot(fails, page)
            check_reveal(fails, bank, page.evaluate("() => document.querySelector('#revealScreen .reveal-message strong').textContent"))
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return bank


PLANTS = [
    ('a wrong key (the first parallelogram 25)', 'keyed',
     [("variables:[{name:'b',value:6},{name:'h',value:4}],resultVar:'A',answer:24", "variables:[{name:'b',value:6},{name:'h',value:4}],resultVar:'A',answer:25")]),
    ('a wrong answer marked right (within 1 of the key)', 'not marked wrong',
     [('var isCorrect = userAnswer === q.answer;', 'var isCorrect = Math.abs(userAnswer - q.answer) <= 1;')]),
    ('a wrong working figure (6 x 4 changed to 6 x 5)', 'step',
     [("'A = 6 \\\\times 4','A = 24'", "'A = 6 \\\\times 5','A = 24'")]),
    ('a wrong formula text (prism V = A + l)', 'formula text',
     [("formulaKatex:'V = A \\\\times l',variables:[{name:'A',value:12},{name:'l',value:5}]", "formulaKatex:'V = A + l',variables:[{name:'A',value:12},{name:'l',value:5}]")]),
    ('the parallelogram h label back over the slanted side', 'h label',
     [("hLabel.style.right = '126px';", "hLabel.style.left = '168px';")]),
    ('the trapezium h label back across the slanted side', 'h label',
     [("hLabel.style.right = '81px';", "hLabel.style.right = '20px';")]),
    ('a wrong number in the diagram description', 'the diagram says',
     [("' and height ' + h);", "' and height ' + b);")]),
    ('the reveal screen\'s old count (t3-007)', 'reveal:',
     [('You now know two new area formulae and the volume of a prism.',
       'You now know five area formulae and one volume formula.')]),
    ('the score slot counting questions done (t3-008)', 'score slot',
     [("document.getElementById('scoreNum').textContent = correctCount;", "document.getElementById('scoreNum').textContent = answered;")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    print('%s: %d items recomputed (formula, key, substitution, every working step, the diagram\'s numbers); each answered '
          'right and wrong in Chromium; sessions of %s dealt %d times' % (
              SLUG, len(bank or []), '/'.join(map(str, SESSIONS)), DEALS))
    print('  not asserted (open findings r-001, t3-003, t3-004, t3-005): the diagram\'s proportions and the prism\'s l arrow')
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-52s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-52s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
