#!/usr/bin/env python3
# ci-line: Shape Shifter (every translation, reflection and rotation image recomputed from its words; every rotation option classified; every vertex and every letter tapped on the real canvas in Chromium; each mode card's data-mode its own mode, a burst at random-mix starting Random Mix once, each card starting its mode once without a burst) |
"""Shape Shifter: translate, reflect and rotate a shape on a -5..5 grid; three static banks, four modes.

Banks, read from the page as served: TRANSLATION_QUESTIONS (15, tap the image's vertices), REFLECTION_QUESTIONS (15, tap
the image's vertices) and ROTATION_QUESTIONS (15, built by the page from 12 bases, four options A-D, tap a shape). A
session is 10 questions: one mode, or Random Mix (at least 3 of each mode, one extra).

Checks, independent of the game's code (the maths is integer-exact, so no Fraction is needed):
  Translation: the words ("Translate 3 right and 2 up") are parsed and the image is the shape moved by them; dx and dy
    stored in the item agree with the words; the shape is a triangle, a rectangle or a square as its type says; the
    shape and its image are on the grid (so every vertex can be tapped); the image is not the shape itself.
  Reflection: the axis in the words is the item's axis; the image is the shape with y (x-axis) or x (y-axis) negated;
    on the grid; not the shape itself as a set of vertices (shape-shifter-t3-003, fixed: the one item that was its own
    image now sits clear of the axis). The bank is the one Reflection and Random Mix both deal from (Sessions, below),
    so no mode can serve such an item.
  Rotation: the words ("Rotate 90 degrees clockwise about (0,0)") are parsed and the true image is turned here, a quarter
    turn clockwise as (x, y) -> (y, -x) about the centre and anticlockwise as (x, y) -> (-y, x). The item's key is that
    image. Four options, no two the same shape, exactly one the true image, none the shape itself; every wrong option is a
    named slip (the opposite turn, a reflection in an axis, or the same turn about (1,1)); all on the grid. The letter of
    each option lies inside its own shape, and no two letters sit on the same point.
  Sessions: startGame() in each of the four modes, dealt five times: 10 questions, all different, all from the right
    bank; Random Mix has at least 3 of each mode and each question comes from the bank of the mode it is labelled with.
  Marking, in Chromium (390x844), through the game's own canvas handlers (a click event at each grid point's pixel):
    translation and reflection: tapping the image's vertices in every order reads "Correct!" (and scores 1); every vertex
    replaced in turn by every one of the 121 grid points reads "Not quite" except the vertex itself; a vertex tapped
    twice, and each named whole-shape slip, read "Not quite" (translation: not moved, the opposite move, dx and dy
    swapped, only x moved, only y moved; reflection: not reflected, the other axis, through the origin). Rotation: every
    option's letter tapped over eight deals: the true image reads "Correct! (L)", any other reads "Not quite - correct
    answer was L" naming the true image's letter. A whole session played from this script's own answers scores 10/10 in
    each mode and 0/10 when every answer is wrong.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

Colour (t3-001, fixed in ESSENTIALS-FALSE-TEXT 4/4): after an answer the correct shape is stroked in the page's own
--green, at both drawing sites (the shape tapped and the rotation option), with a contrast of at least 3:1 against the
canvas background (WCAG 1.4.11), and the wrong-answer feedback names that colour, "correct shape shown in green".

Not asserted (open findings, left open): no 180 degree rotation ever built (t3-002), 15 items a mode (t3-004), the
shared board and no keyboard path (t3-005).

    python scripts/verify-shape-shifter.py [--no-selftest] [--against FILE]
"""
import argparse
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'shape-shifter'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
DEALS = 5
ROT_DEALS = 8
MODES = ('translation', 'reflection', 'rotation', 'mix')
# Expected failures: items that break a rule and whose finding stays open. The check fails on any other item that does,
# and fails if one of these stops failing (close the finding then).
EXPECTED = {}


def fs(shape):
    return frozenset((int(x), int(y)) for x, y in shape)


def on_grid(shape):
    return all(isinstance(v, int) and not isinstance(v, bool) and -5 <= v <= 5 for p in shape for v in p)


def area2(shape):
    n = len(shape)
    return sum(shape[i][0] * shape[(i + 1) % n][1] - shape[(i + 1) % n][0] * shape[i][1] for i in range(n))


def kind_ok(kind, shape):
    pts = [tuple(p) for p in shape]
    if len(set(pts)) != len(pts):
        return False
    if kind == 'triangle':
        return len(pts) == 3 and area2(pts) != 0
    if kind in ('rectangle', 'square') and len(pts) == 4:
        xs, ys = sorted({p[0] for p in pts}), sorted({p[1] for p in pts})
        if len(xs) != 2 or len(ys) != 2 or fs(pts) != fs([(x, y) for x in xs for y in ys]):
            return False
        return (xs[1] - xs[0] == ys[1] - ys[0]) if kind == 'square' else True
    return False


def translate(shape, dx, dy):
    return [(x + dx, y + dy) for x, y in shape]


def reflect(shape, axis):
    return [(-x, y) for x, y in shape] if axis == 'y' else [(x, -y) for x, y in shape]


def turn(shape, cx, cy, kind):
    out = []
    for x, y in shape:
        dx, dy = x - cx, y - cy
        if kind == 'cw':
            out.append((cx + dy, cy - dx))
        elif kind == 'ccw':
            out.append((cx - dy, cy + dx))
        else:
            out.append((cx - dx, cy - dy))
    return out


def parse_translation(desc):
    m = re.fullmatch(r'Translate (\d+) (left|right)(?: and (\d+) (up|down))?', desc)
    if not m:
        return None
    dx = int(m.group(1)) * (1 if m.group(2) == 'right' else -1)
    dy = 0 if m.group(3) is None else int(m.group(3)) * (1 if m.group(4) == 'up' else -1)
    return dx, dy


def parse_rotation(desc):
    m = re.fullmatch(r'Rotate (90° anticlockwise|90° clockwise|180°) about \((-?\d+),(-?\d+)\)', desc)
    if not m:
        return None
    kind = {'90° anticlockwise': 'ccw', '90° clockwise': 'cw', '180°': 'half'}[m.group(1)]
    return kind, int(m.group(2)), int(m.group(3))


def inside(px, py, poly):
    ins = False
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[i - 1]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
            ins = not ins
    return ins


def expect_or_fail(fails, expected_hit, mode, shape, msg):
    key = (mode, tuple(tuple(p) for p in shape))
    if key in EXPECTED:
        expected_hit.add(key)
    else:
        fails.append(msg)


def check_banks(fails, expected_hit, tq, rq, oq):
    seen = set()
    for i, q in enumerate(tq, 1):
        where = 'translation %d (%s)' % (i, q['desc'])
        d = parse_translation(q['desc'])
        if d is None:
            fails.append('%s: the words cannot be read as a translation' % where)
            continue
        if (q['dx'], q['dy']) != d:
            fails.append('%s: translation key (%s, %s) but the words say %s' % (where, q['dx'], q['dy'], d))
        if not on_grid(q['shape']) or not kind_ok(q['type'], q['shape']):
            fails.append('%s: translation shape %r is not a %s on the grid' % (where, q['shape'], q['type']))
            continue
        img = translate(q['shape'], *d)
        if not on_grid(img):
            fails.append('%s: translation image %r is off the grid, so it cannot be tapped' % (where, img))
        if fs(img) == fs(q['shape']):
            expect_or_fail(fails, expected_hit, 'translation', q['shape'], '%s: translation image is the shape itself' % where)
        k = ('t', fs(q['shape']), d)
        if k in seen:
            fails.append('%s: translation item repeated' % where)
        seen.add(k)
    for i, q in enumerate(rq, 1):
        where = 'reflection %d (%s)' % (i, q['desc'])
        m = re.fullmatch(r'Reflect in the (x|y)-axis', q['desc'])
        if not m:
            fails.append('%s: the words cannot be read as a reflection' % where)
            continue
        if m.group(1) != q['axis']:
            fails.append('%s: reflection key is the %s-axis but the words say the %s-axis' % (where, q['axis'], m.group(1)))
        if not on_grid(q['shape']) or not kind_ok(q['type'], q['shape']):
            fails.append('%s: reflection shape %r is not a %s on the grid' % (where, q['shape'], q['type']))
            continue
        img = reflect(q['shape'], m.group(1))
        if not on_grid(img):
            fails.append('%s: reflection image %r is off the grid' % (where, img))
        if fs(img) == fs(q['shape']):
            expect_or_fail(fails, expected_hit, 'reflection', q['shape'], '%s: reflection image is the shape itself' % where)
        k = ('r', fs(q['shape']), m.group(1))
        if k in seen:
            fails.append('%s: reflection item repeated' % where)
        seen.add(k)
    for i, q in enumerate(oq, 1):
        where = 'rotation %d (%s)' % (i, q['desc'])
        d = parse_rotation(q['desc'])
        if d is None:
            fails.append('%s: the words cannot be read as a rotation' % where)
            continue
        kind, cx, cy = d
        if (q['cx'], q['cy']) != (cx, cy):
            fails.append('%s: rotation centre (%s,%s) but the words say (%s,%s)' % (where, q['cx'], q['cy'], cx, cy))
        if not on_grid(q['shape']) or not kind_ok(q['type'], q['shape']):
            fails.append('%s: rotation shape %r is not a %s on the grid' % (where, q['shape'], q['type']))
            continue
        true = fs(turn(q['shape'], cx, cy, kind))
        if fs(q['correct']) != true:
            fails.append('%s: rotation key %r but turning the shape gives %r' % (where, sorted(fs(q['correct'])), sorted(true)))
        opts = [q['correct']] + list(q['wrongs'])
        if len(opts) != 4:
            fails.append('%s: rotation has %d options, not 4' % (where, len(opts)))
        if not all(on_grid(o) for o in opts):
            fails.append('%s: a rotation option is off the grid' % where)
        sets = [fs(o) for o in opts]
        if len(set(sets)) != len(sets):
            fails.append('%s: two rotation options are the same shape' % where)
        right = [k for k, s in enumerate(sets) if s == true]
        if right != [0]:
            fails.append('%s: rotation options equal the true image at %s, not just the key (option 0)' % (where, right))
        if fs(q['shape']) in sets:
            fails.append('%s: a rotation option is the shape itself' % where)
        slips = []
        for name, img in (('the opposite turn', turn(q['shape'], cx, cy, {'cw': 'ccw', 'ccw': 'cw', 'half': 'half'}[kind])),
                          ('a reflection in the x-axis', reflect(q['shape'], 'x')),
                          ('a reflection in the y-axis', reflect(q['shape'], 'y')),
                          ('the same turn about (1,1)', turn(q['shape'], 1, 1, kind))):
            slips.append(fs(img))
        for k, w in enumerate(q['wrongs'], 1):
            if fs(w) not in slips:
                fails.append('%s: rotation distractor %d %r is not a named slip' % (where, k, w))
        k = ('o', fs(q['shape']), d)
        if k in seen:
            fails.append('%s: rotation item repeated' % where)
        seen.add(k)


# ---- in the page ----------------------------------------------------------------------------------------------------
CLICK_JS = r"""
const clickG = (gx, gy) => {
  const r = canvas.getBoundingClientRect(), p = gridToPixel(gx, gy);
  canvas.dispatchEvent(new MouseEvent('click', {clientX: r.left + p[0], clientY: r.top + p[1], bubbles: true, cancelable: true}));
};
const fbText = () => document.getElementById('feedbackBar').textContent;
const show = (m, item) => { selectedMode = m; mode = m; questions = [item]; qIndex = 0; mixModes = []; loadQuestion(); };
"""
VERTEX_JS = CLICK_JS + r"""
return (args) => {
  const [m, item, expected, seqs] = args;
  const out = {orders: [], sweep: [], seqs: []};
  startGame(m);
  const run = (seq) => {
    show(m, item); const before = totalCorrect;
    for (const [gx, gy] of seq) clickG(gx, gy);
    return {fb: fbText(), d: totalCorrect - before, locked: MaffsLock.isLocked(gameEl)};
  };
  const n = expected.length;
  const perms = (a) => a.length < 2 ? [a] : a.flatMap((x, i) => perms(a.slice(0, i).concat(a.slice(i + 1))).map(p => [x].concat(p)));
  for (const p of perms(expected)) out.orders.push(run(p));
  for (let k = 0; k < n; k++) for (let gx = -5; gx <= 5; gx++) for (let gy = -5; gy <= 5; gy++) {
    const seq = expected.filter((_, j) => j !== k).concat([[gx, gy]]);
    const r = run(seq); r.k = k; r.gx = gx; r.gy = gy; out.sweep.push(r);
  }
  for (const s of seqs) { const r = run(s); r.seq = s; out.seqs.push(r); }
  MaffsLock.clearTimers();
  return out;
};
"""
WORDING_JS = CLICK_JS + r"""
return (args) => {
  const [m, item, expected, order] = args;
  startGame(m);
  show(m, item);
  const text = document.getElementById('instructionBar').textContent;
  // log every stroked path in the student's colour, with its points in the order they were joined
  const paths = []; let cur = null;
  const o = {beginPath: ctx.beginPath, moveTo: ctx.moveTo, lineTo: ctx.lineTo, stroke: ctx.stroke};
  ctx.beginPath = function () { cur = []; return o.beginPath.apply(this, arguments); };
  ctx.moveTo = function (x, y) { if (cur) cur.push([x, y]); return o.moveTo.apply(this, arguments); };
  ctx.lineTo = function (x, y) { if (cur) cur.push([x, y]); return o.lineTo.apply(this, arguments); };
  ctx.stroke = function () { if (cur && cur.length > 2 && this.strokeStyle === '#6366f1') paths.push(cur.slice());
                             return o.stroke.apply(this, arguments); };
  for (const k of order) clickG(expected[k][0], expected[k][1]);
  const fb = fbText();
  Object.assign(ctx, o);
  MaffsLock.clearTimers();
  return {text, fb, last: paths.length ? paths[paths.length - 1] : null,
          want: expected.map(p => gridToPixel(p[0], p[1]))};
};
"""
ROTATION_JS = CLICK_JS + r"""
return (args) => {
  const [item, deals] = args;
  const out = [];
  startGame('rotation');
  for (let d = 0; d < deals; d++) {
    show('rotation', item);
    const opts = rotationOptions.map(o => ({label: o.label, shape: o.shape.map(p => p.slice()), at: o.at.slice()}));
    const res = [];
    for (let i = 0; i < opts.length; i++) {
      show('rotation', item);
      // the same deal again is not possible (the options are shuffled on every show), so find option i by shape
      const target = JSON.stringify(opts[i].shape);
      const j = rotationOptions.findIndex(o => JSON.stringify(o.shape) === target);
      const before = totalCorrect;
      clickG(rotationOptions[j].at[0], rotationOptions[j].at[1]);
      res.push({shape: opts[i].shape, label: rotationOptions[j].label, fb: fbText(), d: totalCorrect - before,
                labels: rotationOptions.map(o => o.label), shapes: rotationOptions.map(o => o.shape),
                selected: selectedOption, ats: rotationOptions.map(o => o.at.slice())});
    }
    out.push({opts: opts, res: res});
  }
  MaffsLock.clearTimers();
  return out;
};
"""
SESSION_JS = r"""() => {
  const banks = {translation: TRANSLATION_QUESTIONS, reflection: REFLECTION_QUESTIONS, rotation: ROTATION_QUESTIONS};
  const out = {};
  for (const m of %s) { out[m] = [];
    for (let k = 0; k < %d; k++) {
      startGame(m);
      out[m].push({len: questions.length, selected: selectedMode, mixModes: mixModes.slice(),
        idx: questions.map((q, i) => { const mm = m === 'mix' ? mixModes[i] : m; return mm + ':' + banks[mm].indexOf(q); })});
    } }
  MaffsLock.clearTimers();
  return out; }""" % (list(MODES), DEALS)
LETTERS_JS = r"""() => {
  const out = [];
  startGame('rotation');
  for (const item of ROTATION_QUESTIONS) for (let d = 0; d < 8; d++) {
    questions = [item]; qIndex = 0; selectedMode = 'rotation'; mode = 'rotation'; loadQuestion();
    out.push({shapes: rotationOptions.map(o => o.shape.map(p => p.slice())), ats: rotationOptions.map(o => o.at.slice())});
  }
  MaffsLock.clearTimers();
  return out; }"""

def play_session(page, m, wrong):
    """Play one whole session of mode m from this script's own answers; return the final score text."""
    page.evaluate('(m) => { startGame(m); }', m)
    for qi in range(10):
        st = page.evaluate('() => ({mode: mode, q: JSON.parse(JSON.stringify(currentQ))})')
        md, q = st['mode'], st['q']
        if md == 'translation':
            d = parse_translation(q['desc'])
            ans = translate(q['shape'], *d)
            taps = [list(p) for p in ans]
            if wrong:
                taps = [list(p) for p in q['shape']]
        elif md == 'reflection':
            ans = reflect(q['shape'], re.search(r'(x|y)-axis', q['desc']).group(1))
            taps = [list(p) for p in ans]
            if wrong:
                taps = [list(p) for p in reflect(q['shape'], 'x' if re.search(r'(x|y)-axis', q['desc']).group(1) == 'y' else 'y')]
                if fs(taps) == fs(ans):
                    taps = [[-p[0], -p[1]] for p in ans]
        else:
            kind, cx, cy = parse_rotation(q['desc'])
            true = fs(turn(q['shape'], cx, cy, kind))
            ats = page.evaluate('() => rotationOptions.map(o => ({shape: o.shape, at: o.at}))')
            idx = [i for i, o in enumerate(ats) if fs(o['shape']) == true]
            pick = [i for i in range(len(ats)) if i not in idx][0] if wrong else idx[0]
            taps = [ats[pick]['at']]
        page.evaluate('''(taps) => { const r = canvas.getBoundingClientRect();
          for (const [gx, gy] of taps) { const p = gridToPixel(gx, gy);
            canvas.dispatchEvent(new MouseEvent('click', {clientX: r.left + p[0], clientY: r.top + p[1], bubbles: true, cancelable: true})); } }''', taps)
        page.evaluate('() => nextQuestion()')
    return page.evaluate('() => document.getElementById("finalScore").textContent')


def vertex_checks(fails, page, mode, bank):
    for i, q in enumerate(bank, 1):
        if mode == 'translation':
            exp = translate(q['shape'], *parse_translation(q['desc']))
            names = [('not moved', q['shape']),
                     ('the opposite move', translate(q['shape'], -q['dx'], -q['dy'])),
                     ('dx and dy swapped', translate(q['shape'], q['dy'], q['dx'])),
                     ('only x moved', translate(q['shape'], q['dx'], 0)),
                     ('only y moved', translate(q['shape'], 0, q['dy']))]
        else:
            ax = re.search(r'(x|y)-axis', q['desc']).group(1)
            exp = reflect(q['shape'], ax)
            names = [('not reflected', q['shape']),
                     ('the other axis', reflect(q['shape'], 'x' if ax == 'y' else 'y')),
                     ('through the origin', [(-x, -y) for x, y in q['shape']])]
        exp = [list(p) for p in exp]
        dup = [exp[0]] * len(exp)
        seqs = [dup] + [[list(p) for p in s] for _, s in names if on_grid(s) and fs(s) != fs(exp)]
        label = [('a vertex tapped twice')] + [n for n, s in names if on_grid(s) and fs(s) != fs(exp)]
        res = page.evaluate(VERTEX_JS_FN, [mode, q, exp, seqs])
        where = '%s %d (%s)' % (mode, i, q['desc'])
        for r in res['orders']:
            if r['fb'] != 'Correct!' or r['d'] != 1:
                fails.append('%s: marking: the image tapped in some order reads %r (score %d)' % (where, r['fb'], r['d']))
                break
        bad = 'Not quite — correct shape shown in green'
        for r in res['sweep']:
            hit = [r['gx'], r['gy']] == exp[r['k']]
            want, d = ('Correct!', 1) if hit else (bad, 0)
            if r['fb'] != want or r['d'] != d or not r['locked']:
                fails.append('%s: marking: vertex %d tapped at (%d, %d) reads %r (score %d), expected %r' % (
                    where, r['k'], r['gx'], r['gy'], r['fb'], r['d'], want))
                break
        for lab, r in zip(label, res['seqs']):
            if r['fb'] != bad or r['d'] != 0:
                fails.append('%s: marking: %s reads %r (score %d), expected %r' % (where, lab, r['fb'], r['d'], bad))


def is_cyclic_order(got, want):
    """got visits the points of want in want's cyclic order, either way round (a simple outline, not a bow-tie)."""
    pts = [tuple(round(c, 3) for c in p) for p in got]
    if pts and pts[0] == pts[-1]:
        pts = pts[:-1]
    w = [tuple(round(c, 3) for c in p) for p in want]
    if sorted(pts) != sorted(w):
        return False
    n = len(w)
    for seq in (w, w[::-1]):
        for s in range(n):
            if [seq[(s + k) % n] for k in range(n)] == pts:
                return True
    return False


def wording_checks(fails, page, mode, bank):
    """R2/R3 (SWEEP-1 shape-shifter-s1-001, -002): the instruction gives the count (and, in reflections, the vertex on
    the mirror line), and a correct answer is drawn as the shape's own outline whatever order it was tapped in."""
    for i, q in enumerate(bank, 1):
        exp = [list(p) for p in (translate(q['shape'], *parse_translation(q['desc'])) if mode == 'translation'
                                 else reflect(q['shape'], re.search(r'(x|y)-axis', q['desc']).group(1)))]
        n = len(exp)
        where = '%s %d (%s)' % (mode, i, q['desc'])
        order = [0, 2, 1, 3] if n >= 4 else list(range(n))[::-1]
        r = page.evaluate(WORDING_JS_FN, [mode, q, exp, order])
        if 'tap all %d vertices' % n not in r['text']:
            fails.append('%s: wording: the instruction %r does not give the count (tap all %d vertices)' % (where, r['text'], n))
        if mode == 'reflection' and 'A vertex on the mirror line stays where it is' not in r['text']:
            fails.append('%s: wording: the instruction %r does not say a vertex on the mirror line stays put' % (where, r['text']))
        if r['fb'] != 'Correct!':
            fails.append('%s: wording: the image tapped in order %s reads %r' % (where, order, r['fb']))
        elif not r['last'] or not is_cyclic_order(r['last'], r['want']):
            fails.append('%s: wording: a correct answer tapped in order %s is joined as %r, not the shape\'s own outline'
                         % (where, order, r['last']))


def rotation_checks(fails, page, bank):
    for i, q in enumerate(bank, 1):
        kind, cx, cy = parse_rotation(q['desc'])
        true = fs(turn(q['shape'], cx, cy, kind))
        where = 'rotation %d (%s)' % (i, q['desc'])
        deals = page.evaluate(ROTATION_JS_FN, [q, ROT_DEALS])
        for dl in deals:
            for r in dl['res']:
                shp = fs(r['shape'])
                clicked_right = shp == true
                keyl = [lab for lab, s in zip(r['labels'], r['shapes']) if fs(s) == true]
                want = 'Correct! (%s)' % r['label'] if clicked_right else 'Not quite — correct answer was %s' % (keyl[0] if keyl else '?')
                if r['fb'] != want or r['d'] != (1 if clicked_right else 0):
                    fails.append('%s: marking: tapping letter %s (%s) reads %r (score %d), expected %r' % (
                        where, r['label'], 'the true image' if clicked_right else 'a distractor', r['fb'], r['d'], want))
                    break


def letter_checks(fails, page):
    for n, d in enumerate(page.evaluate(LETTERS_JS)):
        for k, (sh, at) in enumerate(zip(d['shapes'], d['ats'])):
            if not inside(at[0], at[1], sh):
                fails.append('letters: deal %d: the letter of option %d is not inside its shape (%r at %r)' % (n, k, sh, at))
                return
        for a, b in itertools.combinations(d['ats'], 2):
            if abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9:
                fails.append('letters: deal %d: two letters sit on the same point %r' % (n, a))
                return


def session_checks(fails, page, nbank):
    res = page.evaluate(SESSION_JS)
    for m, deals in res.items():
        for d in deals:
            if d['len'] != 10 or d['selected'] != m:
                fails.append('session %s: %d questions (mode %s), expected 10' % (m, d['len'], d['selected']))
            idx = d['idx']
            if len(set(idx)) != len(idx) or any(s.endswith(':-1') for s in idx):
                fails.append('session %s: questions repeat or are not from the bank: %r' % (m, idx))
            if m == 'mix':
                counts = {k: sum(1 for s in idx if s.startswith(k + ':')) for k in ('translation', 'reflection', 'rotation')}
                if min(counts.values()) < 3 or sum(counts.values()) != 10:
                    fails.append('session mix: modes %r, expected at least 3 of each in 10' % counts)
            else:
                if any(not s.startswith(m + ':') for s in idx):
                    fails.append('session %s: a question from another bank: %r' % (m, idx))


def luminance(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def colour_checks(fails, html):
    """t3-001: the correct shape after an answer is drawn in the page's --green at both sites, at least 3:1 against
    the canvas (WCAG 1.4.11), and the feedback names the colour it is drawn in."""
    green = re.search(r'--green:\s*(#[0-9a-fA-F]{6})', html)
    canvas = re.search(r'canvas\{[^}]*background:\s*(#[0-9a-fA-F]{6})', html)
    sites = {'the shape tapped': re.search(r"const target = expectedVertices;\s*drawShape\(target,\s*'([^']+)'", html),
             'the rotation option': re.search(r"opt\.correct\)\s*\{\s*drawShape\(opt\.shape,\s*'([^']+)'", html)}
    named = re.search(r"correct shape shown in (\w+)'", html)
    if not (green and canvas and named and all(sites.values())):
        fails.append('colour: cannot read --green, the canvas background, both correct-shape drawing sites and the feedback')
        return
    for where, m in sites.items():
        col = m.group(1).lower()
        if col != green.group(1).lower():
            fails.append('colour: the correct shape (%s) is drawn in %s, not the page\'s --green %s' % (where, col, green.group(1)))
        elif not col.startswith('#') or contrast(col, canvas.group(1)) < 3:
            fails.append('colour: the correct shape (%s) in %s is under 3:1 against the canvas %s' % (where, col, canvas.group(1)))
    if named.group(1) != 'green':
        fails.append('colour: the feedback says the correct shape is shown in %s, but it is drawn in --green' % named.group(1))


# The mode cards' data-mode attributes (contract SHAPE-SHIFTER-DATA-MODE, Jon, 25 Oct 2026): burst.js opens a burst at a
# mode by pressing the start screen's [data-mode="<name>"] once. Each card's attribute names its own onclick mode, in
# the cards' order, Random Mix as random-mix.
CARD_MODES = [('translation', 'translation'), ('reflection', 'reflection'), ('rotation', 'rotation'), ('random-mix', 'mix')]
CARD = re.compile(r'<div class="mode-card(?: [^"]*)?"([^>]*)>')   # a card, not the mode-cards row round them
# game_started recorded once per call however many wrappers stand round mfg (burst.js wraps it): the outermost call only.
MFG_RECORDER = """(() => { let real = null, depth = 0; window.__starts = [];
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { const cur = real; return function (n, p) {
      if (!depth && n === 'game_started') window.__starts.push(p && p.mode);
      depth++; try { if (typeof cur === 'function') return cur.apply(this, arguments); } catch (e) {} finally { depth--; } }; },
    set(v) { real = v; } }); })();"""


def mode_card_checks(fails, html, browser, base):
    got = []
    for attrs in CARD.findall(html):
        dm = re.search(r'data-mode="([^"]*)"', attrs)
        oc = re.search(r"onclick=\"startGame\('([^']*)'\)\"", attrs)
        got.append((dm.group(1) if dm else None, oc.group(1) if oc else None))
    if got != CARD_MODES:
        fails.append('mode cards: the cards are %s (data-mode, onclick mode); expected %s, in that order' % (got, CARD_MODES))
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)

    def fresh(query):
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        ctx.add_init_script(MFG_RECORDER)
        ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
        ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
            status=200, content_type='text/html; charset=utf-8', body=html))
        page = ctx.new_page()
        page.goto(base + '/games/%s/%s' % (SLUG, query), wait_until='load', timeout=20000)
        page.wait_for_function('typeof startGame === "function"', timeout=15000)
        return ctx, page

    state = """() => ({ selected: selectedMode, game: document.getElementById('gameScreen').classList.contains('active'),
        menu: document.getElementById('startScreen').classList.contains('active'), starts: window.__starts,
        burst: !!(window.MaffsBurst && MaffsBurst.active()) })"""
    # A burst at random-mix: burst.js presses the Random Mix card once, and the game starts Random Mix.
    ctx, page = fresh('?burst=5&from=six-ps&topic=transformations&mode=random-mix&cb=verify')
    try:
        page.wait_for_timeout(1500)
        st = page.evaluate(state)
        if not (st['burst'] and st['selected'] == 'mix' and st['game'] and not st['menu'] and st['starts'] == ['mix']):
            fails.append('mode cards: a burst at mode=random-mix did not start Random Mix once (the game\'s state: %r)' % st)
    finally:
        ctx.close()
    # Played normally: no card is pressed for the student, and each card, clicked, starts its own mode once.
    for dm, mode in CARD_MODES:
        ctx, page = fresh('?cb=verify')
        try:
            page.wait_for_timeout(300)
            st = page.evaluate(state)
            if st['burst'] or st['starts'] or not st['menu']:
                fails.append('mode cards: without a burst the menu did not wait for the student (%r)' % st)
            page.click('.mode-card[data-mode="%s"]' % dm, timeout=5000)
            page.wait_for_timeout(200)
            st = page.evaluate(state)
            if not (st['selected'] == mode and st['game'] and st['starts'] == [mode]):
                fails.append('mode cards: clicking the %s card did not start %s once (the game\'s state: %r)' % (dm, mode, st))
        except Exception as e:
            fails.append('mode cards: the %s card could not be clicked: %s' % (dm, str(e).splitlines()[0]))
        finally:
            ctx.close()


def play(fails, html, expected_hit, cards=True):
    from playwright.sync_api import sync_playwright
    colour_checks(fails, html)
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof ROTATION_QUESTIONS !== "undefined" && typeof startGame === "function"', timeout=15000)
            tq = page.evaluate('() => JSON.parse(JSON.stringify(TRANSLATION_QUESTIONS))')
            rq = page.evaluate('() => JSON.parse(JSON.stringify(REFLECTION_QUESTIONS))')
            oq = page.evaluate('() => JSON.parse(JSON.stringify(ROTATION_QUESTIONS))')
            check_banks(fails, expected_hit, tq, rq, oq)
            session_checks(fails, page, (len(tq), len(rq), len(oq)))
            letter_checks(fails, page)
            page.evaluate('() => { startGame("translation"); }')
            vertex_checks(fails, page, 'translation', tq)
            vertex_checks(fails, page, 'reflection', rq)
            wording_checks(fails, page, 'translation', tq)
            wording_checks(fails, page, 'reflection', rq)
            rotation_checks(fails, page, oq)
            for m in MODES:
                good = play_session(page, m, False)
                if good != '10/10':
                    fails.append('session %s played from the script\'s own answers scores %r, expected 10/10' % (m, good))
                bad = play_session(page, m, True)
                if bad != '0/10':
                    fails.append('session %s played with every answer wrong scores %r, expected 0/10' % (m, bad))
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            if cards:   # the bank plants need none of it; only the main run and the mode-card plants pay for it
                mode_card_checks(fails, html, browser, base)
            browser.close()
            stats = {'translation': len(tq), 'reflection': len(rq), 'rotation': len(oq)}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong translation key (dx 3 for "2 right")', 'translation key',
     [("{ shape:[[1,1],[3,1],[2,3]], desc:'Translate 2 right and 1 up', dx:2, dy:1, type:'triangle' }",
       "{ shape:[[1,1],[3,1],[2,3]], desc:'Translate 2 right and 1 up', dx:3, dy:1, type:'triangle' }")]),
    ('a wrong reflection axis (x-axis item keyed y)', 'reflection key',
     [("{ shape:[[2,-1],[4,-1],[3,2]], axis:'x', desc:'Reflect in the x-axis', type:'triangle' }",
       "{ shape:[[2,-1],[4,-1],[3,2]], axis:'y', desc:'Reflect in the x-axis', type:'triangle' }")]),
    ('the rotation turn reversed (the old r-001 fault)', 'rotation key',
     [("const rx = Math.round(dx * Math.cos(rad) - dy * Math.sin(rad) + cx);",
       "const rx = Math.round(dx * Math.cos(rad) + dy * Math.sin(rad) + cx);"),
      ("const ry = Math.round(dx * Math.sin(rad) + dy * Math.cos(rad) + cy);",
       "const ry = Math.round(-dx * Math.sin(rad) + dy * Math.cos(rad) + cy);")]),
    ('a second correct rotation option (key filter removed)', 'rotation options',
     [("shapeFits(w) && !shapesEqual(w, correct) &&", "shapeFits(w) && true &&")]),
    ('a wrong letter in the rotation feedback', 'marking: tapping letter',
     [("const correctLabel = rotationOptions.find(o => o.correct).label;",
       "const correctLabel = rotationOptions.find(o => !o.correct).label;")]),
    ('a wrong vertex marked right (y ignored)', 'marking: vertex',
     [("placedVertices[i][0] === expectedVertices[j][0] && placedVertices[i][1] === expectedVertices[j][1]",
       "placedVertices[i][0] === expectedVertices[j][0]")]),
    ('a correct answer joined in tap order (bow-tie)', 'wording',
     [("const joined = (MaffsLock.isLocked(gameEl) && lastVertexAnswerCorrect) ? expectedVertices : placedVertices;",
       "const joined = placedVertices;")]),
    ('the vertex count missing from the instruction', 'wording',
     [("— tap all ${expectedVertices.length} vertices of the new shape`;", "— tap each vertex position`;")]),
    ('the y-axis reflection computed as the x-axis', 'marking',
     [("if (axis === 'y') return shape.map(([x,y]) => [-x, y]);", "if (axis === 'y') return shape.map(([x,y]) => [x, -y]);")]),
    ('the correct shape drawn in navy again (t3-001)', 'colour',
     [("drawShape(target, '#22c55e', 'rgba(34,197,94,0.3)', 2);", "drawShape(target, '#1a2744', 'rgba(26,39,68,0.3)', 2);")]),
    ('the feedback naming navy again (t3-001)', 'colour',
     [("correct shape shown in green';", "correct shape shown in navy';")]),
    ('the Random Mix card without its data-mode (a burst lands on the menu)', 'mode cards',
     [('<div class="mode-card mix" data-mode="random-mix" onclick="startGame(\'mix\')">',
       '<div class="mode-card mix" onclick="startGame(\'mix\')">')]),
    ('a card whose data-mode names another mode', 'mode cards',
     [('<div class="mode-card" data-mode="rotation" onclick="startGame(\'rotation\')">',
       '<div class="mode-card" data-mode="reflection" onclick="startGame(\'rotation\')">')]),
    ('a reflection item that is its own image (the old t3-003 square)', 'reflection image is the shape itself',
     [("{ shape:[[-4,1],[-2,1],[-2,3],[-4,3]], axis:'x', desc:'Reflect in the x-axis', type:'rectangle' },",
       "{ shape:[[-4,-1],[-2,-1],[-2,1],[-4,1]], axis:'x', desc:'Reflect in the x-axis', type:'rectangle' },")]),
]
VERTEX_JS_FN = '(function(){' + VERTEX_JS + '})()'
ROTATION_JS_FN = '(function(){' + ROTATION_JS + '})()'
WORDING_JS_FN = '(function(){' + WORDING_JS + '})()'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    hit = set()
    st = play(fails, html, hit)
    for k in EXPECTED:
        if k not in hit:
            fails.append('expected failure %s (%s) no longer occurs: close the finding and remove it from EXPECTED' % (EXPECTED[k], k[0]))
    print('%s: %d translation, %d reflection and %d rotation items recomputed from their words; every vertex of every translation '
          'and reflection answer tapped at all 121 grid points, every rotation letter tapped over %d deals, %d sessions dealt per mode, '
          'in Chromium' % (SLUG, st.get('translation', 0), st.get('reflection', 0), st.get('rotation', 0), ROT_DEALS, DEALS))
    for k, v in sorted(EXPECTED.items()):
        print('  expected failure left open: %s (%s item with shape %s)' % (v, k[0], list(k[1])))
    print('  correct shape after an answer drawn in --green at both sites, %.2f:1 against the canvas; the feedback names it (t3-001)'
          % contrast(re.search(r'--green:\s*(#[0-9a-fA-F]{6})', html).group(1),
                     re.search(r'canvas\{[^}]*background:\s*(#[0-9a-fA-F]{6})', html).group(1)))
    print('  not asserted (open): no 180 degree rotation built (t3-002), 15 items a mode (t3-004), board and keyboard (t3-005)')
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-58s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted, set(), cards=tag == 'mode cards')
            found = [f for f in rep if tag in f]
            ok = ok and bool(found)
            print('  self-test %-58s %s' % (what, ('caught: ' + found[0][:100]) if found else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
