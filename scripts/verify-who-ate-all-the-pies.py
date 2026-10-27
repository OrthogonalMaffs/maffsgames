#!/usr/bin/env python3
# ci-line: Who Ate All the Pies?, part 1 (every question of the five stages over 20 seeds a slot, recomputed from its own printed numbers with exact fractions, never from the bank's or the game's code: fractions, amounts, every table angle, can-you-tell verdicts, totals; slips different from the answer; sectors make 360; the game's marking compared with an independent marker on thousands of probe answers; sessions of ten, easiest first) | --part 1
# ci-line: Who Ate All the Pies?, part 2 (all five stages played in the page at 390 px, worked example then ten questions with the keypad open: every drawn slice read back from its path against the data, labels and key text at least 12 px, a wrong table angle visibly leaves the circle open, one board submission a stage) | --part 2
# ci-line: Who Ate All the Pies?, part 3 (the first three questions of every stage at 375, 360, 320, 1280 and 1366 px, with a wide font: answer boxes, keys and Next above the fold, no sideways scroll) | --part 3
# ci-line: Who Ate All the Pies?, part 4 (fault-injection self-test: the planted faults, each caught) | --part 4
# ci-deps: games/who-ate-all-the-pies/ schools/assets/pie-game.js schools/assets/pie-chart-generator.js
"""Independent verification for Who Ate All the Pies? (games/who-ate-all-the-pies/), built 27 Oct 2026 (contract WHO-ATE-ALL-THE-PIES).
SR-30: checked from its first PR.

The game imports the pie-charts bank's generator (schools/assets/pie-chart-generator.js, canon 8.2.1) and adds only a thin layer
(schools/assets/pie-game.js). This script loads both under Playwright, asks for each stage's questions, and recomputes everything
here in Python, from the NUMBERS PRINTED in each question (its stem and its chart data), never from the bank's or the game's own
arithmetic, and compares:

  Stage 1  the fraction of the whole a slice is: angle / 360 in lowest terms (the other slice: (360 - angle) / 360).
  Stage 2  amount = total x angle / 360, a whole number.
  Stage 3  every table angle = frequency x 360 / total (a whole number), the angles make 360, the asked sector is the bank's answer.
  Stage 4  the verdict from the data alone: two charts with no totals: you can't tell; two totals given: the numbers of pies;
           one chart: the bigger angle. The right option is the one that says so.
  Stage 5  total = frequency x 360 / angle.
  Slips    every named wrong answer differs from the right one; no two the same.
  Marking  MaffsPieGame.mark() against an independent marker on probe answers (the key, each slip, the key nudged, an unsimplified
           fraction, random numbers, every option): same verdict, so a right value in the wrong form is 'format', never 'right'.
  Chart    the drawn slices, read back from each SVG path, match the data in degrees and make 360; every slice has a written key
           naming it; text is at least 12 px; a stage 3 chart drawn from typed angles that do not make 360 is flagged open.
  Page     one worked example then ten questions a stage; boxes, keys and Next above the fold at the sizes; no sideways scroll;
           a mark only for a right answer; one board submission a stage.
"""
import argparse
import math
import os
import random
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'who-ate-all-the-pies'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
MODULE = os.path.join(ROOT, 'schools', 'assets', 'pie-game.js')
BANKJS = os.path.join(ROOT, 'schools', 'assets', 'pie-chart-generator.js')
SEEDS = 20
CANT = "You can't tell"
BIG = (390, 844)
SMALL = [(375, 667), (360, 640), (320, 568), (1280, 720), (1366, 768)]


# ---------------------------------------------------------------- what the question prints
DEG = re.compile(r'\\\((\d+)\^\\circ\\\)')


def degs(text):
    return [int(x) for x in DEG.findall(text)]


def gcd_frac(n, d):
    f = Fraction(n, d)
    return f.numerator, f.denominator


def table_of(stem):
    """'Steak 20, Mince 10, Vegetable 10. 40 pies ...' -> [(pie, freq)]: the table the stem prints."""
    m = re.search(r'matchday\. (.*?)\. (\d+) pies were sold in total', stem)
    rows = [(a.strip().lower(), int(b)) for a, b in re.findall(r'([A-Za-z ]+?) (\d+)(?:, |$)', m.group(1))]
    return rows, int(m.group(2))


def expected(q):
    """The right answer, from the printed numbers only: ('fraction', Fraction) | ('number', Fraction) | ('angles', [..]) | ('choice', text)."""
    st, stem, ch = q['stage'], q['stem'], q['charts']
    sec = lambda c, pie: next(s for s in c['sectors'] if s['pie'] == pie)
    if st == 1:
        a = degs(stem)[0]
        a = 360 - a if 'only one other sector' in stem else a
        return 'fraction', Fraction(a, 360)
    if st == 2:
        total = int(re.search(r'(\d+) pies were sold in total', stem).group(1))
        return 'number', Fraction(total * degs(stem)[0], 360)
    if st == 3:
        rows, total = table_of(stem)
        return 'angles', [Fraction(f * 360, total) for _, f in rows], rows, total
    if st == 5:
        m = re.search(r'sector is \\\((\d+)\^\\circ\\\) and (\d+) ', stem)
        return 'number', Fraction(int(m.group(2)) * 360, int(m.group(1)))
    # stage 4: the verdict from the data
    ask = q['ask']
    if len(ch) == 2:
        a, b = ch
        if a['total'] is None or b['total'] is None:
            return 'choice', CANT
        na = Fraction(a['total'] * sec(a, ask['pie'])['angle'], 360)
        nb = Fraction(b['total'] * sec(b, ask['pie'])['angle'], 360)
        if na == nb:
            return 'choice', 'They sold the same number'
        return 'choice', "Yes, it's the " + (ask['stands'][0] if na > nb else ask['stands'][1])
    p1, p2 = ask['pies']
    a1, a2 = sec(ch[0], p1)['angle'], sec(ch[0], p2)['angle']
    return 'choice', 'They sold the same number' if a1 == a2 else "Yes, it's " + (p1 if a1 > a2 else p2)


def check_question(q):
    errs = []
    tag = 's%d slot %d' % (q['stage'], q['slot'])
    for c in q['charts']:
        angs = [s['angle'] for s in c['sectors']]
        if any(a != int(a) or a <= 0 for a in angs) or sum(angs) != 360:
            errs.append('%s: sector angles %s do not make 360 in whole degrees' % (tag, angs))
        if len({s['pie'] for s in c['sectors']}) != len(angs):
            errs.append('%s: two sectors with the same name' % tag)
    try:
        exp = expected(q)
    except Exception as e:  # noqa: BLE001
        return errs + ['%s: could not read the printed numbers: %s' % (tag, e)]
    st = q['stage']
    # the angles printed in the stem are the chart's
    shown = [s['angle'] for c in q['charts'] for s in c['sectors'] if s.get('shown')]
    if st != 3 and shown and not set(degs(q['stem'])) <= set(a for c in q['charts'] for a in [s['angle'] for s in c['sectors']]):
        errs.append('%s: an angle in the stem is not on the chart' % tag)
    if st == 1:
        k = Fraction(q['key']['n'], q['key']['d'])
        if k != exp[1] or math.gcd(q['key']['n'], q['key']['d']) != 1:
            errs.append('%s: fraction %s, the printed angle gives %s in lowest terms' % (tag, q['key'], exp[1]))
        for s in q['slips']:
            if Fraction(s['n'], s['d']) == exp[1]:
                errs.append('%s: a slip is the right fraction' % tag)
    elif st in (2, 5):
        if Fraction(q['key']) != exp[1] or exp[1].denominator != 1:
            errs.append('%s: answer %s, the printed numbers give %s' % (tag, q['key'], exp[1]))
        for s in q['slips']:
            if Fraction(s['value']) == exp[1]:
                errs.append('%s: a slip is the right answer' % tag)
    elif st == 3:
        _, angles, rows, total = exp
        if [Fraction(a) for a in q['key']] != angles or any(a.denominator != 1 for a in angles) or sum(angles) != 360:
            errs.append('%s: table angles %s, the table gives %s' % (tag, q['key'], [str(a) for a in angles]))
        if sum(f for _, f in rows) != total or [s['pie'] for s in q['sectors']] != [p for p, _ in rows]:
            errs.append('%s: the table and the sectors differ' % tag)
        if Fraction(q['key'][q['askedIndex']]) != Fraction(q['bank']['answer']['value']):
            errs.append("%s: the asked sector's angle is not the bank's answer" % tag)
        for s in q['sectors']:
            vals = [Fraction(x['value']) for x in s['slips']]
            if Fraction(s['angle']) in vals or len(vals) != len(set(vals)):
                errs.append('%s: a slip for %s is the right angle or a repeat' % (tag, s['pie']))
    else:
        if q['options'][q['key']] != exp[1]:
            errs.append("%s: marked right is %r, the data says %r" % (tag, q['options'][q['key']], exp[1]))
        if CANT not in q['options'] or len(set(q['options'])) != len(q['options']):
            errs.append('%s: options %s' % (tag, q['options']))
        for s in q['slips']:
            if s['option'] == exp[1] or s['option'] not in q['options']:
                errs.append('%s: a slip names the right option or none' % tag)
    if not q['worked'] or any(not w for w in q['worked']):
        errs.append('%s: no worked answer' % tag)
    return errs


# ---------------------------------------------------------------- the independent marker
def py_mark(q, raws):
    st = q['stage']
    exp = expected(q)
    if st == 4:
        i = int(raws[0])
        if q['options'][i] == exp[1]:
            return 'right'
        return 'slip' if any(q['options'][i] == s['option'] for s in q['slips']) else 'wrong'
    if st == 1:
        n, d = int(raws[0]), int(raws[1])
        if d == 0:
            return 'unreadable'
        if Fraction(n, d) == exp[1]:
            return 'right' if (n, d) == (exp[1].numerator, exp[1].denominator) else 'format'
        return 'slip' if any(Fraction(n, d) == Fraction(s['n'], s['d']) for s in q['slips']) else 'wrong'
    if st in (2, 5):
        v = Fraction(int(raws[0]))
        if v == exp[1]:
            return 'right'
        return 'slip' if any(v == Fraction(s['value']) for s in q['slips']) else 'wrong'
    _, angles, rows, total = exp
    vals = [Fraction(int(r)) for r in raws]
    if vals == angles:
        return 'right'
    for v, a, (_, f) in zip(vals, angles, rows):
        if v == a:
            continue
        slips = set()
        pc = Fraction(f * 100, total)
        if pc.denominator == 1 and pc != a:
            slips.add(pc)
        if f * 360 != a:
            slips.add(Fraction(f * 360))
        if v in slips:
            return 'slip'
    return 'wrong'


def probes(q, rng):
    st = q['stage']
    exp = expected(q)
    if st == 4:
        return [[str(i)] for i in range(len(q['options']))]
    if st == 1:
        n, d = exp[1].numerator, exp[1].denominator
        out = [[n, d], [2 * n, 2 * d], [n + 1, d], [d, n], [n, d + 1]]
        out += [[s['n'], s['d']] for s in q['slips']] + [[s['n'] * 2, s['d'] * 2] for s in q['slips']]
        out += [[rng.randint(1, 9), rng.randint(1, 12)] for _ in range(8)]
        return [[str(a), str(b)] for a, b in out]
    if st in (2, 5):
        k = int(exp[1])
        out = [k, k + 1, k - 1, k * 2] + [int(s['value']) for s in q['slips']] + [rng.randint(1, 400) for _ in range(6)]
        return [[str(max(v, 0))] for v in out]
    _, angles, rows, total = exp
    a = [int(x) for x in angles]
    out = [list(a)]
    for i in range(len(a)):
        v = list(a)
        v[i] += 1
        out.append(v)
        v = list(a)
        v[i] = 0
        out.append(v)
        for s in q['sectors'][i]['slips']:
            v = list(a)
            v[i] = int(s['value'])
            out.append(v)
    if len(a) > 1:
        v = list(a)
        v[0], v[1] = v[1], v[0]
        out.append(v)
    out += [[rng.randint(1, 200) for _ in a] for _ in range(4)]
    return [[str(max(x, 0)) for x in v] for v in out]


GEN_JS = """(args) => { const out = [], M = MaffsPieGame, B = MaffsPieCharts;
  for (let st = 1; st <= 5; st++) for (let slot = 0; slot < 12; slot++) for (let s = 1; s <= args.seeds; s++)
    out.push(M.adapt(B.question(st, slot, M.makeRng(st * 100003 + slot * 1009 + s))));
  const sessions = []; for (let st = 1; st <= 5; st++) for (let s = 1; s <= 15; s++) sessions.push(M.session(st, s * 7919 + 3, 10).map(q => [q.stage, q.slot, q.stem]));
  return { qs: out, sessions: sessions }; }"""
MARK_JS = """(items) => items.map(([qi, raws]) => MaffsPieGame.mark(window.__qs[qi], raws).kind)"""


# ---------------------------------------------------------------- the page and module under Playwright
def open_page(pw, base, html, module, size):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    ctx.route(lambda url: url.split('?')[0].endswith('/pie-game.js'), lambda route: route.fulfill(
        status=200, content_type='application/javascript; charset=utf-8', body=module))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.PIE && !!PIE.ui', timeout=10000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


def check_engine(page, out):
    data = page.evaluate(GEN_JS, {'seeds': SEEDS})
    qs = data['qs']
    page.evaluate('(qs) => { window.__qs = qs; }', qs)
    rng = random.Random(11)
    info = {}
    bad = 0
    for i, q in enumerate(qs):
        for e in check_question(q):
            bad += 1
            if bad <= 8:
                out.append(e)
    if bad > 8:
        out.append('... and %d more question findings' % (bad - 8))
    items, want = [], []
    for i, q in enumerate(qs):
        if q['slot'] % 3 or i % SEEDS > 5:        # a third of the slots, six seeds each, keeps the probe run short
            continue
        for raws in probes(q, rng):
            items.append([i, raws])
            want.append(py_mark(q, raws))
    got = page.evaluate(MARK_JS, items)
    diffs = [(items[k], want[k], got[k]) for k in range(len(items)) if want[k] != got[k]]
    for (it, w, g) in diffs[:5]:
        q = qs[it[0]]
        out.append('s%d slot %d: mark() said %s for %s, an independent marker says %s' % (q['stage'], q['slot'], g, it[1], w))
    if len(diffs) > 5:
        out.append('... and %d more marking differences' % (len(diffs) - 5))
    info['probes'] = len(items)
    kinds = {}
    for k in want:
        kinds[k] = kinds.get(k, 0) + 1
    for need in ('right', 'wrong', 'slip', 'format'):
        if not kinds.get(need):
            out.append('no probe was ever expected to be %s: the probes miss that verdict' % need)
    # variety and sessions
    for st in range(1, 6):
        stems = {q['stem'] for q in qs if q['stage'] == st}
        info['distinct%d' % st] = len(stems)
        if len(stems) < 30:
            out.append('stage %d: only %d distinct questions over %d seeds' % (st, len(stems), SEEDS))
        if not any(q['stage'] == st for q in qs):
            out.append('stage %d: no questions' % st)
    for sess in data['sessions']:
        slots = [s for _, s, _ in sess]
        if len(sess) != 10 or slots != sorted(slots) or 0 in slots or len(set(slots)) != 10:
            out.append('session %s: not ten distinct slots in order, never the example slot' % slots)
            break
    cants = sum(1 for q in qs if q['stage'] == 4 and q['options'][q['key']] == CANT)
    if not cants or cants == sum(1 for q in qs if q['stage'] == 4):
        out.append("stage 4: \"you can't tell\" must be right in some questions and wrong in others (%d right)" % cants)
    return info


# ---------------------------------------------------------------- the page played
SVG_JS = """() => [...document.querySelectorAll('#figure svg, #exFigure svg')].filter(svg => svg.getBoundingClientRect().width > 0).map(svg => ({
  closed: svg.dataset.closed, sum: Number(svg.dataset.sum),
  slices: [...svg.querySelectorAll('g[data-pie]')].map(g => { const p = g.querySelector('path'); return { pie: g.dataset.pie, angle: Number(g.dataset.angle),
      a0: Number(g.dataset.a0), a1: Number(g.dataset.a1), d: p ? p.getAttribute('d') : null }; }),
  keys: [...svg.querySelectorAll('g[data-key] text')].map(t => t.textContent),
  fonts: [...svg.querySelectorAll('text')].map(t => parseFloat(getComputedStyle(t).fontSize) * (svg.getBoundingClientRect().width / Number(svg.getAttribute('data-w') || svg.getBoundingClientRect().width))),
  gap: !!svg.querySelector('.gap'), over: !!svg.querySelector('.over') }))"""


def read_path(d):
    """The angle (degrees clockwise from twelve o'clock) of the start and end of a slice, read from its SVG path."""
    m = re.match(r'M([\d.]+) ([\d.]+) L([\d.]+) ([\d.]+) A[\d.]+ [\d.]+ 0 [01] 1 ([\d.]+) ([\d.]+) Z', d)
    cx, cy, x0, y0, x1, y1 = [float(v) for v in m.groups()]
    ang = lambda x, y: (math.degrees(math.atan2(x - cx, cy - y)) + 360) % 360
    a0, a1 = ang(x0, y0), ang(x1, y1)
    return a0, (a1 - a0) % 360


def check_svgs(svgs, q, out, where, typed=None):
    for k, s in enumerate(svgs):
        if not s['slices']:
            continue
        total = 0
        for sl in s['slices']:
            span = sl['a1'] - sl['a0']
            if sl['d']:
                a0, got = read_path(sl['d'])
                if abs(got - span) > 0.6 or abs(((a0 - sl['a0'] + 180) % 360) - 180) > 0.6:
                    out.append('%s: slice %s drawn %.1f degrees from %.1f, its data says %.1f from %.1f' % (where, sl['pie'], got, a0, span, sl['a0']))
            if typed is None and abs(span - sl['angle']) > 1e-6 and q['type'] != 'angles':
                out.append('%s: slice %s drawn %.1f, the question says %s' % (where, sl['pie'], span, sl['angle']))
            total += span
        if typed is None and q['type'] != 'angles' and abs(total - 360) > 0.6:
            out.append('%s: the drawn slices make %.1f degrees' % (where, total))
        names = {t.split(' ')[0] if t.split(' ')[0] in ('steak', 'mince', 'vegetable') else t for t in s['keys']}
        for sl in s['slices']:
            if not any(t.startswith(sl['pie'].replace('cheese and onion', 'cheese & onion')) for t in s['keys']):
                out.append('%s: slice %s has no written key' % (where, sl['pie']))
        if s['fonts'] and min(s['fonts']) < 12 - 1e-6:
            out.append('%s: chart text %.1f px (needs 12 or more)' % (where, min(s['fonts'])))


def fill(page, vals):
    # the phone keypad makes the boxes read-only, so type the way its keys do: set the value, fire "input"
    page.evaluate("""(vals) => { [...document.querySelectorAll('#answer input')].forEach((el, i) => {
        el.value = String(vals[i]); el.dispatchEvent(new Event('input', { bubbles: true })); }); }""", [str(v) for v in vals])


def play_stage(page, st, size, out, n, full):
    w, h = size
    fold = h - 40
    where = '%dx%d stage %d' % (w, h, st)
    page.evaluate('window.__ev = []; window.__sub = []')
    if full:                                           # the worked example, step by step, then the questions
        page.evaluate('PIE.ui.start(%d, true)' % st)
        page.wait_for_selector('#exBtn', state='visible')
        steps = 0
        while 'Start the questions' not in page.inner_text('#exBtn') and steps < 12:
            page.click('#exBtn')
            steps += 1
            page.wait_for_timeout(60)
        ex = page.evaluate(SVG_JS)
        if steps < 2 or not page.query_selector('#exSteps li'):
            out.append('%s: the worked example has no steps' % where)
        page.click('#exBtn')
    else:
        page.evaluate('PIE.ui.start(%d)' % st)
    expect = 0
    for qn in range(n):
        page.wait_for_function("PIE.ui.state() === 'asking'", timeout=8000)
        q = page.evaluate('PIE.ui.question()')
        page.wait_for_timeout(120)
        m = page.evaluate("""() => { const r = [...document.querySelectorAll('#answer input, #answer button, #kpHolder button')].filter(x => x.offsetParent).map(x => x.getBoundingClientRect());
            return { last: r.length ? Math.max(...r.map(x => x.bottom)) : 0, sw: document.documentElement.scrollWidth, iw: innerWidth, right: r.length ? Math.max(...r.map(x => x.right)) : 0 }; }""")
        if m['last'] > fold + 0.5:
            out.append('%s q%d: answer controls end at %d, below the fold (%d)' % (where, qn, m['last'], fold))
        if m['sw'] > m['iw'] or m['right'] > m['iw'] + 0.5:
            out.append('%s q%d: sideways scroll or a control off the screen (%d > %d)' % (where, qn, max(m['sw'], m['right']), m['iw']))
        check_svgs(page.evaluate(SVG_JS), q, out, '%s q%d' % (where, qn))
        kind = 'right'
        if qn == 1:
            kind = 'slip'
        elif qn == 2:
            kind = 'wrong'
        key = q['key']
        note = None
        if q['type'] == 'choice':
            if kind == 'right':
                pick = key
            elif kind == 'slip' and q['slips']:
                pick = q['options'].index(q['slips'][0]['option'])
                note = q['slips'][0]['line']
            else:
                kind, pick = 'wrong', next(i for i in range(len(q['options'])) if i != key and not any(q['options'][i] == s['option'] for s in q['slips']))
            page.click('#answer [data-opt="%d"]' % pick)
        else:
            if q['type'] == 'fraction':
                sol = [key['n'], key['d']]
                bad = [key['n'], key['d'] + 1]
                if kind == 'slip' and q['slips']:
                    bad, note = [q['slips'][0]['n'], q['slips'][0]['d']], q['slips'][0]['line']
                elif kind == 'slip':
                    kind = 'wrong'
            elif q['type'] == 'number':
                sol, bad = [key], [key + 7]
                if kind == 'slip' and q['slips']:
                    bad, note = [q['slips'][0]['value']], q['slips'][0]['line']
                elif kind == 'slip':
                    kind = 'wrong'
            else:
                sol = list(key)
                bad = list(key)
                bad[0] += 5                                # one angle wrong: the chart cannot close
                if kind == 'slip':
                    kind = 'wrong'
            fill(page, sol if kind == 'right' else bad)
            if q['type'] == 'angles' and kind != 'right' and not page.query_selector('#figure[hidden]'):
                svgs = page.evaluate(SVG_JS)
                if not svgs or svgs[0]['closed'] != 'false' or not (svgs[0]['gap'] or svgs[0]['over']):
                    out.append('%s q%d: angles that do not make 360 did not leave the circle visibly open: %s' % (where, qn, svgs and (svgs[0]['closed'], svgs[0]['sum'])))
            page.click('#checkBtn')
        page.wait_for_timeout(150)
        ok = kind == 'right'
        if ok:
            expect += 1
        if int(page.inner_text('#hudScore')) != expect:
            out.append('%s q%d: marks show %s, expected %d (a wrong answer scored, or a right one did not)' % (where, qn, page.inner_text('#hudScore'), expect))
        fb = page.evaluate("""() => { const n = document.querySelector('.maffs-next, #nextBtn'), l = document.querySelector('.fb-line');
            return { next: n ? n.getBoundingClientRect().bottom : null, line: l ? l.textContent : '', done: !!document.querySelector('.fb.done') }; }""")
        if fb['next'] is None or fb['next'] > fold + 0.5:
            out.append('%s q%d (%s): Next is %s, below the fold (%d)' % (where, qn, kind, fb['next'], fold))
        if fb['done'] != ok:
            out.append('%s q%d (%s): the feedback says %s' % (where, qn, kind, 'right' if fb['done'] else 'not right'))
        if note:                                           # the slip's own words (its plain text between the TeX bits) are on screen
            plain = max(re.split(r'\\\(.*?\\\)', note), key=len).strip()
            if plain and re.sub(r'\s+', ' ', plain) not in re.sub(r'\s+', ' ', fb['line']):
                out.append('%s q%d: the named slip was not shown: %r (the line says %r)' % (where, qn, plain[:40], fb['line'][:60]))
        if not fb['line'].strip():
            out.append('%s q%d: no feedback line' % (where, qn))
        if ok:
            page.evaluate("document.getElementById('nextBtn').click()")
        else:
            page.evaluate("document.querySelector('.maffs-next').click()")
        page.wait_for_timeout(100)
    if full and n >= 10:
        page.wait_for_function("document.getElementById('results').classList.contains('active')", timeout=8000)
        sub = page.evaluate('window.__sub')
        comp = [p for nm, p in page.evaluate('window.__ev') if nm == 'game_completed']
        if len(sub) != 1 or sub[0][0] != SLUG or sub[0][1] != 'stage-%d' % st or sub[0][2] != expect:
            out.append('%s: the leaderboard got %s, the marks were %d on stage-%d' % (where, sub, expect, st))
        if len(comp) != 1 or comp[0].get('score') != expect or comp[0].get('mode') != 'stage-%d' % st:
            out.append('%s: game_completed says %s, the marks were %d' % (where, comp, expect))
        if int(page.inner_text('#resScore')) != expect:
            out.append('%s: the results screen shows %s, not %d' % (where, page.inner_text('#resScore'), expect))
        if st == 3 and 'protractor' not in page.inner_text('#resStats'):
            out.append('%s: the results do not say that protractor drawing is practised on paper' % where)
        if st < 5 and 'Next: Stage %d' % (st + 1) not in page.inner_text('#nextStageBtn'):
            out.append('%s: no "Next: Stage %d" button' % (where, st + 1))
        allowed = {'game_slug', 'level', 'mode', 'question_index', 'correct', 'score', 'questions_answered', 'questions_correct', 'previous_best'}
        for nm, p in page.evaluate('window.__ev'):
            if set(p) - allowed:
                out.append('%s: an event field outside the existing events: %s' % (where, sorted(set(p) - allowed)))
                break
    return expect


def check_pages(base, html, module, sizes, out, n, full, font=False):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for size in sizes:
            br, page, errs = open_page(pw, base, html, module, size)
            if font:
                page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')
            try:
                for st in range(1, 6):
                    play_stage(page, st, size, out, n, full)
                    page.evaluate("document.getElementById('menuBtn') && document.getElementById('menuBtn').click()")
                    page.evaluate("document.querySelector('#menu') && document.querySelector('#menu').classList.add('active')")
            except Exception as e:  # noqa: BLE001
                out.append('play at %dx%d threw: %s' % (size[0], size[1], str(e).splitlines()[0][:220]))
            out.extend('page error at %dx%d: %s' % (size[0], size[1], e) for e in errs)
            br.close()


def check(html, module, out, engine=True, big=False, small=(), quick=False):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    info = {}
    try:
        if engine:
            with sync_playwright() as pw:
                br, page, errs = open_page(pw, base, html, module, (1280, 800))
                try:
                    info.update(check_engine(page, out))
                except Exception as e:  # noqa: BLE001
                    out.append('the engine checks threw: %s' % str(e).splitlines()[0][:200])
                out.extend('page error: ' + e for e in errs)
                br.close()
        if big:
            check_pages(base, html, module, [BIG], out, 3 if quick else 10, True)
        if small:
            check_pages(base, html, module, small, out, 3, False, font=True)
    finally:
        proc.terminate()
    return info


# Each plant: (what, file, [(old, new)], kind, pattern its finding must match).
PLANTS = [
    ('a wrong amount (stage 2 and 5 key one too many)', 'module',
     [("      q.key = b.answer.value;\n      q.slips = b.slips.map(function (s) { return { kind: s.kind, value: s.answer.value, line: s.line }; });",
       "      q.key = b.answer.value + 1;\n      q.slips = b.slips.map(function (s) { return { kind: s.kind, value: s.answer.value, line: s.line }; });")], 'engine',
     r'(answer .*the printed numbers give|mark\(\) said)'),
    ("a can't-tell verdict reversed (stage 4 marks the next option right)", 'module',
     [("      q.key = b.answer.correct;\n      q.options", "      q.key = (b.answer.correct + 1) % b.answer.options.length;\n      q.options")], 'engine',
     r"(marked right is|mark\(\) said)"),
    ('an unsimplified fraction accepted as right', 'module',
     [("return { kind: 'format', why: 'Right value, but simplify it fully", "return { kind: 'right', why: 'Right value, but simplify it fully")], 'engine',
     r'mark\(\) said right'),
    ('a slice drawn off its data (a sector drawn ten per cent wide)', 'page',
     [("var a0 = acc, a1 = Math.min(360, acc + ang);", "var a0 = acc, a1 = Math.min(360, acc + ang * 1.1);")], 'play',
     r'(drawn|the drawn slices)'),
    ('a table chart that claims to close whatever the angles', 'page',
     [("var closed = Math.abs(sum - 360) < 1e-9;", "var closed = true;")], 'play',
     r'did not leave the circle visibly open'),
    ('a wrong answer counted as a mark (the page)', 'page',
     [("answered++; if (ok) { rightCount++; marks++; }", "answered++; marks++; if (ok) { rightCount++; }")], 'play',
     r'(marks show|the leaderboard got|game_completed says)'),
    ('chart text under 12 px', 'page',
     [(".charts text{font-family:var(--font-num);font-size:12.5px;", ".charts text{font-family:var(--font-num);font-size:10px;")], 'play',
     r'chart text .* px'),
]


def selftest(html, module, plants=None):
    ok = True
    for what, which, edits, kind, want in (PLANTS if plants is None else plants):
        src = module if which == 'module' else html
        bad = False
        for old, new in edits:
            if src.count(old) != 1:
                bad = True
                break
            src = src.replace(old, new)
        if bad:
            print('  self-test %-72s *** CANNOT PLANT ***' % what)
            ok = False
            continue
        got = []
        h2, m2 = (html, src) if which == 'module' else (src, module)
        check(h2, m2, got, engine=kind == 'engine', big=kind == 'play', quick=True)
        hit = [g for g in got if re.search(want, g)]
        ok = ok and bool(hit)
        print('  self-test %-72s %s' % (what, ('caught: ' + hit[0][:90]) if hit else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '')))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', choices=['1', '2', '3', '4'], help='one of the four parts CI runs side by side (default: all)')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    module = open(MODULE, encoding='utf-8').read()
    part = args.part
    out = []
    info = check(html, module, out, engine=part in (None, '1'), big=part in (None, '2'), small=SMALL if part in (None, '3') else ())
    if info:
        print('%s: %s' % (SLUG, info))
    if part in (None, '2'):
        print('%s: all five stages played at %dx%d' % (SLUG, BIG[0], BIG[1]))
    if part in (None, '3'):
        print('%s: three questions a stage at %s' % (SLUG, ', '.join('%dx%d' % s for s in SMALL)))
    ok = True
    if part in (None, '4'):
        ok = selftest(html, module)
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('FAIL  ... and %d more' % (len(out) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
