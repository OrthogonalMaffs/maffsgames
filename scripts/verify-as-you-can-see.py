#!/usr/bin/env python3
# ci-line: As You Can See (the 60-question fixed-seed bank and 20 seeds of every slot recomputed from each question's own chart data and ask, never from the bank's or the game's code: pictogram rows, bar, dual and stacked heights, line readings, scatter correlation, line of best fit, outlier, every stage-5 flaw read off the chart; accepted intervals; slips outside them; the game's marking compared with an independent marker; every drawn chart read back from its SVG against its data; all five stages played in the page at 390 px and the first questions at 375, 360, 320, 1280 and 1366 px with a wide font; fault-injection self-test) |
# ci-deps: games/as-you-can-see/ schools/assets/reading-charts-game.js schools/assets/reading-charts-generator.js
"""Independent verification for As You Can See (games/as-you-can-see/), built 27 Oct 2026 (contract AS-YOU-CAN-SEE).
SR-30: checked from its first PR.

The game imports the reading-charts bank (schools/assets/reading-charts-generator.js, canon 8.2.1) and adds only a thin layer
(schools/assets/reading-charts-game.js). This script loads both under Playwright, asks for each stage's questions, and recomputes
everything here in Python from the CHART DATA and the `ask` of each question (never from the bank's or the game's own arithmetic):

  Stage 1  pictogram rows (quarters x key / 4): a row, a sum, a difference, all rows, busiest less quietest, symbols for a number,
           the key from a row, a changed key.
  Stage 2  bar heights: a bar, a difference, a sum, the highest; dual bars (a series, a difference, a total); stacked bars (a part is
           its own length, the whole bar, the same part in two bars).
  Stage 3  line readings: a reading, a change (with its direction), the peak, the trend, the steepest rise; "can you tell?" (an
           unmeasured time is always "You can't tell", a marked one never is).
  Stage 4  scatter graphs: Pearson r gives the correlation (and its strength); the line of best fit gives an estimate; the outlier is
           the one point far from the line; correlation is not cause; a value beyond the data is unreliable.
  Stage 5  the flaw is read off the chart (3D flag, area-scaled pictures, missing labels, an axis that does not start at 0, ticks
           that are not equally spaced, or none: fair) and the right option is the one that names it.
  Accepted intervals  a reading from a graph is right within half a minor gridline, a count or a difference exactly; every slip lies
           outside the interval; no two slips the same.
  Marking  MaffsChartsGame.mark() against an independent marker on probe answers (the key, the interval's edges and just beyond, each
           slip, random numbers, every option): the same verdict.
  Bank     60 questions with the fixed seed, 12 distinct to a stage; the game's files copy no bank question text.
  Charts   every drawn chart read back from its SVG paths and positions (bars and points through the numbers on the axes, pictogram
           symbols by their clipped width) against its data; all text at least 12 px, no label overlapping another or leaving the
           chart; a key naming each series of a dual or stacked bar.
  Page     one worked example then ten questions a stage; boxes, keys and Next above the fold at the sizes; no sideways scroll; a mark
           only for a right answer; one board submission a stage.

Work is in units (engine, one play per size, one per planted fault) so CI can run it whole, or in slices once SHARD merges.
"""
import argparse
import contextlib
import json
import math
import os
import random
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'as-you-can-see'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
MODULE = os.path.join(ROOT, 'schools', 'assets', 'reading-charts-game.js')
BANKJS = os.path.join(ROOT, 'schools', 'assets', 'reading-charts-generator.js')
SEEDS = 20
CANT = "You can't tell"
BIG = (390, 844)
SMALL = [(375, 667), (360, 640), (320, 568), (1280, 720), (1366, 768)]

# What each stage-5 flaw is called in the options (written here from the contract, not read from the bank).
LIE_TEXT = {
    'fair': 'Yes: it is a fair chart',
    'truncated': 'No: the axis does not start at 0',
    'uneven': 'No: the scale has uneven steps',
    'area': 'No: the pictures are scaled both ways',
    'threeD': 'No: the 3D bars are misleading',
    'nolabels': 'No: no title, labels or units',
}
READING_OPS = {'read', 'readS', 'seg', 'total', 'esty', 'estx', 'outlierY'}


# ---------------------------------------------------------------- recomputing an answer from the chart and the ask
def pearson(pts):
    n = len(pts)
    mx = sum(F(p['x']) for p in pts) / n
    my = sum(F(p['y']) for p in pts) / n
    sxy = sum((p['x'] - mx) * (p['y'] - my) for p in pts)
    sxx = sum((p['x'] - mx) ** 2 for p in pts)
    syy = sum((p['y'] - my) ** 2 for p in pts)
    return float(sxy) / math.sqrt(float(sxx) * float(syy))


def line_at(ch, x):
    return ch['line']['c'] + ch['line']['m'] * x


def flaw_of(ch):
    """The one thing wrong with a stage 5 chart (or 'fair'), read off its flags and ticks only."""
    found = []
    if ch['threeD']:
        found.append('threeD')
    if ch['areaScaled']:
        found.append('area')
    if ch['title'] is None and ch['yLabel'] is None or not ch['labelled']:
        found.append('nolabels')
    if ch['ticks'][0] != 0:
        found.append('truncated')
    steps = {ch['ticks'][i + 1] - ch['ticks'][i] for i in range(len(ch['ticks']) - 1)}
    if len(steps) > 1:
        found.append('uneven')
    return found


def expected(q):
    """The right answer from the chart and the ask only: ('number', Fraction) | ('choice', text)."""
    ch, ask, op = q['chart'], q['ask'], q['ask']['op']
    t = ch['type']
    if t == 'pictogram':
        per = F(ch['per'])
        val = {r['label']: F(r['q']) * per / 4 for r in ch['rows']}
        q4 = {r['label']: r['q'] for r in ch['rows']}
        if op == 'read':
            return 'number', val[ask['row']]
        if op == 'sum':
            return 'number', sum(val[r] for r in ask['rows'])
        if op == 'diff':
            return 'number', val[ask['a']] - val[ask['b']]
        if op == 'all':
            return 'number', sum(val.values())
        if op == 'range':
            return 'number', max(val.values()) - min(val.values())
        if op == 'draw':
            return 'number', F(ask['value']) / per
        if op == 'findkey':
            return 'number', F(ask['value']) / (F(q4[ask['row']]) / 4)
        if op == 'newkey':
            return 'number', val[ask['row']] / F(ask['newPer'])
    if t == 'bar':
        v = {c['label']: F(c['value']) for c in ch['cats']}
        if op == 'read':
            return 'number', v[ask['cat']]
        if op == 'diff':
            return 'number', v[ask['a']] - v[ask['b']]
        if op == 'sum':
            return 'number', sum(v[c] for c in ask['cats'])
        if op == 'highest':
            return 'choice', max(v, key=lambda k: v[k])
    if t == 'dual':
        si = {n: i for i, n in enumerate(ch['series'])}
        cv = {c['label']: [F(x) for x in c['values']] for c in ch['cats']}
        if op == 'readS':
            return 'number', cv[ask['cat']][si[ask['series']]]
        if op == 'diffS':
            return 'number', cv[ask['cat']][si[ask['more']]] - cv[ask['cat']][si[ask['less']]]
        if op == 'sumS':
            return 'number', sum(v[si[ask['series']]] for v in cv.values())
    if t == 'composite':
        si = {n: i for i, n in enumerate(ch['series'])}
        cv = {c['label']: [F(x) for x in c['values']] for c in ch['cats']}
        if op == 'seg':
            return 'number', cv[ask['cat']][si[ask['seg']]]
        if op == 'total':
            return 'number', sum(cv[ask['cat']])
        if op == 'segdiff':
            a, b = ask['cats']
            return 'number', cv[a][si[ask['seg']]] - cv[b][si[ask['seg']]]
    if t == 'line':
        pv = {p['label']: F(p['value']) for p in ch['points']}
        labs = [p['label'] for p in ch['points']]
        vals = [pv[l] for l in labs]
        if op == 'read':
            return 'number', pv[ask['pt']]
        if op == 'change':
            return 'number', abs(pv[ask['to']] - pv[ask['from']])
        if op == 'range':
            return 'number', max(vals) - min(vals)
        if op == 'peak':
            return 'choice', labs[vals.index(max(vals))]
        if op == 'trend':
            a, b = pv[ask['from']], pv[ask['to']]
            return 'choice', 'It goes up overall' if b > a else ('It goes down overall' if b < a else 'It stays about the same')
        if op in ('between', 'unmeasured'):
            return 'choice', CANT
        if op == 'compare':
            return 'choice', 'Yes' if pv[ask['a']] > pv[ask['b']] else 'No'
        if op == 'steepest':
            k = max(range(len(vals) - 1), key=lambda i: vals[i + 1] - vals[i])
            return 'choice', 'Between %s and %s' % (labs[k], labs[k + 1])
        if op == 'anyAbove':
            return 'choice', 'Yes' if any(v > ask['thr'] for v in vals) else 'No'
    if t == 'scatter':
        if op == 'corr':
            r = pearson(ch['points'])
            if abs(r) < 0.3:
                return 'choice', 'none'
            return 'choice', ('+' if r > 0 else '-') + ('strong' if abs(r) >= 0.8 else 'weak')
        if op == 'esty':
            return 'number', F(line_at(ch, ask['x']))
        if op == 'estx':
            return 'number', F(ask['y'] - ch['line']['c']) / ch['line']['m']
        if op == 'gradient':
            return 'number', F(abs(ch['line']['m']))
        if op in ('outlier', 'outlierY'):
            res = [(abs(p['y'] - line_at(ch, p['x'])), p) for p in ch['points']]
            res.sort(key=lambda r: -r[0])
            top = res[0][1]
            return ('choice', top.get('tag')) if op == 'outlier' else ('number', F(top['y']))
        if op == 'cause':
            return 'choice', 'cause'
        if op == 'beyond':
            return 'choice', 'beyond'
        if op == 'generalise':
            return 'choice', CANT
    if t == 'lying':
        fl = flaw_of(ch)
        return 'choice', LIE_TEXT[fl[0] if fl else 'fair']
    raise ValueError('no recomputation for %s %s' % (t, op))


def check_chart(q, tag, errs):
    """The chart data itself: whole-number values on the gridlines, inside the axis, the shapes the stage needs."""
    ch, t = q['chart'], q['chart']['type']
    if t in ('bar', 'dual', 'composite'):
        if ch['max'] % ch['major'] or ch['major'] % ch['minor'] or ch['minor'] not in (2, 5, 10):
            errs.append('%s: scale max %s major %s minor %s' % (tag, ch['max'], ch['major'], ch['minor']))
        labels = [c['label'] for c in ch['cats']]
        if len(set(labels)) != len(labels):
            errs.append('%s: two bars with the same label' % tag)
        for c in ch['cats']:
            vs = [c['value']] if t == 'bar' else c['values']
            if any(v % ch['minor'] or v <= 0 for v in vs):
                errs.append('%s: a bar value %s is off the gridlines (%s)' % (tag, vs, ch['minor']))
            if (sum(vs) if t == 'composite' else max(vs)) > ch['max']:
                errs.append('%s: a bar is taller than the scale (%s of %s)' % (tag, vs, ch['max']))
        if t == 'bar':
            vs = [c['value'] for c in ch['cats']]
            if len(set(vs)) != len(vs):
                errs.append('%s: two bars the same height' % tag)
    if t == 'line':
        if ch['max'] % ch['major'] or any(p['value'] % ch['minor'] or not 0 < p['value'] < ch['max'] for p in ch['points']):
            errs.append('%s: a line reading is off the gridlines or the scale' % tag)
        if len(ch['mids']) != len(ch['points']) - 1:
            errs.append('%s: mids do not sit between the points' % tag)
        vs = [p['value'] for p in ch['points']]
        if q['ask']['op'] in ('peak',) and vs.count(max(vs)) != 1:
            errs.append('%s: the highest reading is not unique' % tag)
        if q['ask']['op'] == 'steepest':
            d = [vs[i + 1] - vs[i] for i in range(len(vs) - 1)]
            if d.count(max(d)) != 1 or max(d) <= 0:
                errs.append('%s: the steepest rise is not unique or not a rise' % tag)
        if q['ask']['op'] == 'change':
            pv = {p['label']: p['value'] for p in ch['points']}
            d = pv[q['ask']['to']] - pv[q['ask']['from']]
            if d == 0 or (d > 0) != (q['ask']['dir'] == 'rise'):
                errs.append('%s: the stem says %s but the change is %s' % (tag, q['ask']['dir'], d))
    if t == 'pictogram':
        per = ch['per']
        if any(r['q'] % 4 and (F(r['q']) * per / 4).denominator != 1 for r in ch['rows']):
            errs.append('%s: a part symbol does not make a whole number (%s each)' % (tag, per))
        if len({r['label'] for r in ch['rows']}) != len(ch['rows']) or any(r['q'] <= 0 for r in ch['rows']):
            errs.append('%s: pictogram rows' % tag)
    if t == 'scatter':
        pts = ch['points']
        if any(p['x'] != int(p['x']) or p['y'] != int(p['y']) or not 0 < p['x'] < ch['xMax'] or not 0 < p['y'] < ch['yMax'] for p in pts):
            errs.append('%s: a point is off the axes or off whole numbers' % tag)
        if len(pts) < 10 or len({(p['x'], p['y']) for p in pts}) != len(pts):
            errs.append('%s: too few points or a repeated point' % tag)
        if ch['line'] and (ch['line']['c'] != int(ch['line']['c']) or ch['line']['m'] != int(ch['line']['m'])):
            errs.append('%s: the line of best fit is not whole numbers' % tag)
        if q['ask']['op'] == 'corr':
            r = abs(pearson(pts))
            if not (r >= 0.8 or 0.45 <= r <= 0.78 or r < 0.25):
                errs.append('%s: |r| = %.2f is in no clear band' % (tag, r))
        if q['ask']['op'] in ('outlier', 'outlierY'):
            res = sorted((abs(p['y'] - line_at(ch, p['x'])) for p in pts), reverse=True)
            if res[0] < 0.2 * ch['yMax'] or res[1] > 0.13 * ch['yMax']:
                errs.append('%s: the outlier is not clearly one point (%s)' % (tag, res[:3]))
            tags = [p.get('tag') for p in pts if p.get('tag')]
            if sorted(tags) != ['A', 'B', 'C', 'D'] and q['ask']['op'] == 'outlier':
                errs.append('%s: point tags %s' % (tag, tags))
        if q['ask']['op'] in ('esty', 'estx') and ch['line']:
            if q['ask']['op'] == 'esty' and not 0 < line_at(ch, q['ask']['x']) < ch['yMax']:
                errs.append('%s: the line leaves the graph at the asked x' % tag)
            if q['ask']['op'] == 'estx' and not 0 < q['ask']['y'] < ch['yMax']:
                errs.append('%s: the asked y is off the graph' % tag)
        if q['ask']['op'] == 'beyond' and q['ask']['x'] <= ch['dataMax']:
            errs.append('%s: the asked x is not beyond the data (%s <= %s)' % (tag, q['ask']['x'], ch['dataMax']))
    if t == 'lying':
        fl = flaw_of(ch)
        if len(fl) > 1:
            errs.append('%s: more than one flaw: %s' % (tag, fl))
        if (fl[0] if fl else 'fair') != ch['flaw']:
            errs.append('%s: the chart says flaw %s, its drawing data says %s' % (tag, ch['flaw'], fl))
        vals = [i['value'] for i in ch['items']]
        if min(vals) < ch['ticks'][0] or max(vals) > ch['ticks'][-1]:
            errs.append('%s: a value is off the axis' % tag)


def check_question(q):
    errs = []
    tag = 's%d slot %d %s' % (q['stage'], q['slot'], q['kind'])
    try:
        kind, want = expected(q)
    except Exception as e:  # noqa: BLE001
        return ['%s: could not recompute the answer: %s %s' % (tag, type(e).__name__, e)]
    check_chart(q, tag, errs)
    a, ch = q['bank']['answer'], q['chart']
    # the accepted interval
    if a['type'] == 'number':
        if kind != 'number':
            errs.append('%s: a number answer where the chart gives a choice' % tag)
        else:
            if F(a['value']).limit_denominator(100) != want:
                errs.append('%s: answer %s, the chart gives %s' % (tag, a['value'], want))
            op = q['ask']['op']
            if ch['type'] == 'scatter':
                minor = ch['xMinor'] if op == 'estx' else ch['yMinor']
            else:
                minor = ch.get('minor')
            wtol = F(minor) / 2 if (op in READING_OPS and minor) else F(0)
            if F(a['tol']).limit_denominator(100) != wtol:
                errs.append('%s: tolerance %s, half a gridline is %s' % (tag, a['tol'], wtol))
            for s in q['slips']:
                if abs(F(s['value']).limit_denominator(100) - want) <= F(a['tol']).limit_denominator(100):
                    errs.append('%s: slip %s (%s) lies inside the accepted interval' % (tag, s['kind'], s['value']))
            vals = [s['value'] for s in q['slips']]
            if len(set(vals)) != len(vals):
                errs.append('%s: two slips the same' % tag)
    else:
        opts = q['options']
        if kind != 'choice':
            errs.append('%s: a choice where the chart gives a number' % tag)
        else:
            right = opts[q['key']]
            if want in ('cause', 'beyond'):
                good = right.startswith('Correlation does not show cause') if want == 'cause' else right.startswith('No:')
                if not good or sum(1 for o in opts if o.startswith('Correlation does not show cause' if want == 'cause' else 'No:')) != 1:
                    errs.append('%s: marked right is %r' % (tag, right))
            elif q['ask']['op'] == 'corr':
                sign = {'none': 'No correlation', '+strong': 'Strong positive', '-strong': 'Strong negative', '+weak': 'Weak positive', '-weak': 'Weak negative'}
                if want == '+strong' and q['slot'] <= 2:
                    ok = right.startswith('Positive')
                elif want == '-strong' and q['slot'] <= 2:
                    ok = right.startswith('Negative')
                elif want == 'none':
                    ok = right.startswith('No correlation')
                elif q['slot'] == 3:
                    ok = right.startswith(sign[want])
                else:
                    ok = False
                if not ok:
                    errs.append('%s: marked right is %r, the points give %s (r = %.2f)' % (tag, right, want, pearson(ch['points'])))
            elif right != want:
                errs.append('%s: marked right is %r, the chart gives %r' % (tag, right, want))
            if len(set(opts)) != len(opts):
                errs.append('%s: repeated options' % tag)
            for s in q['slips']:
                if s['option'] == right or s['option'] not in opts:
                    errs.append('%s: slip %s names the right option or none' % (tag, s['kind']))
            if CANT in opts and q['stage'] not in (3, 4):
                errs.append("%s: \"You can't tell\" outside stages 3 and 4" % tag)
    if not q['worked'] or any(not w for w in q['worked']):
        errs.append('%s: no worked answer' % tag)
    if not q['stem'] or not q['generic']:
        errs.append('%s: no stem' % tag)
    # the stem names what it asks about
    ask = q['ask']
    for key in ('row', 'cat', 'pt', 'a', 'b', 'from', 'to'):
        if key in ask and ask[key] not in q['stem']:
            errs.append('%s: the stem does not name %r' % (tag, ask[key]))
    for key in ('rows', 'cats'):
        for nm in ask.get(key, []):
            if nm not in q['stem']:
                errs.append('%s: the stem does not name %r' % (tag, nm))
    if ch['type'] in ('bar', 'dual', 'composite', 'line') and q['kind'] not in ('line-between', 'line-estimate', 'line-trend', 'line-compare', 'line-any-above', 'line-peak', 'line-steepest'):
        if not re.search(r'each gridline is (.*= )?%d\b' % ch['minor'], ' '.join(q['worked'])):
            errs.append('%s: the working does not say what a gridline is worth (%d)' % (tag, ch['minor']))
    if ch['type'] in ('bar', 'dual', 'composite', 'line') and re.search(r'gridline', q['stem']):
        errs.append('%s: the stem gives away the scale; reading it is part of the question' % tag)
    if ch['type'] == 'pictogram' and not ch['keyHidden'] and ('stands for %s ' % ch['per']) not in q['stem']:
        errs.append('%s: the stem does not give the key' % tag)
    return errs


# ---------------------------------------------------------------- the independent marker
def py_mark(q, raws):
    a = q['bank']['answer']
    if a['type'] == 'choice':
        i = int(raws[0])
        if i == a['correct']:
            return 'right'
        return 'slip' if any(a['options'][i] == s['answer']['option'] for s in q['bank']['slips']) else 'wrong'
    x = F(raws[0])
    v, tol = F(a['value']).limit_denominator(100), F(a['tol']).limit_denominator(100)
    if abs(x - v) <= tol:
        return 'right'
    return 'slip' if any(abs(x - F(s['answer']['value']).limit_denominator(100)) <= tol for s in q['bank']['slips']) else 'wrong'


def probes(q, rng):
    a = q['bank']['answer']
    if a['type'] == 'choice':
        return [[str(i)] for i in range(len(a['options']))]
    v, tol = F(a['value']).limit_denominator(100), F(a['tol']).limit_denominator(100)
    out = [v, v + tol, v - tol, v + tol + F(1, 2), v - tol - F(1, 2), v + 1, v * 2, F(0)]
    for s in q['bank']['slips']:
        sv = F(s['answer']['value']).limit_denominator(100)
        out += [sv, sv + tol, sv - tol]
    out += [F(rng.randint(0, 400), 2) for _ in range(5)]
    return [[('%g' % float(x)) if x >= 0 else '0'] for x in out]


GEN_JS = """(args) => { const out = [], M = MaffsChartsGame, B = MaffsReadingCharts;
  for (let st = 1; st <= 5; st++) for (let slot = 0; slot < 12; slot++) for (let s = 1; s <= args.seeds; s++)
    out.push(M.adapt(B.question(st, slot, M.makeRng(st * 100003 + slot * 1009 + s))));
  const sessions = []; for (let st = 1; st <= 5; st++) for (let s = 1; s <= 15; s++) sessions.push(M.session(st, s * 7919 + 3, 10).map(q => [q.stage, q.slot, q.stem]));
  const fixed = B.bank().map(q => M.adapt(q)), again = B.bank().map(q => JSON.stringify(q));
  return { qs: out, sessions: sessions, fixed: fixed, repeat: JSON.stringify(B.bank().map(q => JSON.stringify(q))) === JSON.stringify(again.map(x => x)) , seed: B.FIXED_SEED }; }"""
MARK_JS = """(items) => items.map(([qi, raws]) => MaffsChartsGame.mark(window.__qs[qi], raws).kind)"""


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
    ctx.route(lambda url: url.split('?')[0].endswith('/reading-charts-game.js'), lambda route: route.fulfill(
        status=200, content_type='application/javascript; charset=utf-8', body=module))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.ACS && !!ACS.ui', timeout=10000)
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
    for q in qs:
        for e in check_question(q):
            bad += 1
            if bad <= 10:
                out.append(e)
    if bad > 10:
        out.append('... and %d more question findings' % (bad - 10))
    # the marking against the independent marker
    items, want = [], []
    for i, q in enumerate(qs):
        if i % SEEDS > 3:
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
    for need in ('right', 'wrong', 'slip'):
        if not kinds.get(need):
            out.append('no probe was ever expected to be %s: the probes miss that verdict' % need)
    # the fixed-seed bank: 60 questions, 12 distinct a stage, the same every time
    fixed = data['fixed']
    if len(fixed) != 60:
        out.append('the fixed-seed bank has %d questions, not 60' % len(fixed))
    for st in range(1, 6):
        keys = {json.dumps([q['stem'], q['chart']], sort_keys=True) for q in fixed if q['stage'] == st}
        kinds_st = {q['slot'] for q in fixed if q['stage'] == st}
        info['bank%d' % st] = len(keys)
        if len(keys) < 12 or len(kinds_st) != 12:
            out.append('stage %d: only %d distinct questions in the fixed bank' % (st, len(keys)))
        stems = {json.dumps([q['stem'], q['chart']], sort_keys=True) for q in qs if q['stage'] == st}
        info['distinct%d' % st] = len(stems)
        if len(stems) < 40:
            out.append('stage %d: only %d distinct questions over %d seeds' % (st, len(stems), SEEDS))
    for q in fixed:
        for e in check_question(q):
            out.append('fixed bank: ' + e)
    if not data['repeat']:
        out.append('the fixed-seed bank is not the same on a second call')
    for sess in data['sessions']:
        slots = [s for _, s, _ in sess]
        if len(sess) != 10 or slots != sorted(slots) or 0 in slots or len(set(slots)) != 10:
            out.append('session %s: not ten distinct slots in order, never the example slot' % slots)
            break
    # "you can't tell" is a genuine option in stages 3 and 4, right in some questions and wrong in others
    for st in (3, 4):
        sq = [q for q in qs if q['stage'] == st and q['type'] == 'choice']
        right = sum(1 for q in sq if q['options'][q['key']] == CANT)
        some = sum(1 for q in sq if CANT in q['options'])
        if not right or right == len(sq) or some <= right:
            out.append("stage %d: \"you can't tell\" must be right in some questions and an option that is wrong in others (%d right of %d choices)" % (st, right, len(sq)))
    # the named slips the contract lists are all present
    names = {s['kind'] for q in qs for s in q['slips']}
    for need in ('key-ignored', 'half-as-whole', 'half-as-one', 'gridline-high', 'segment-top', 'beyond-the-data', 'correlation-as-cause', 'truncated-face-value'):
        if need not in names:
            out.append('the named slip %r is never offered' % need)
    # bank first: no bank question text copied into the game's files
    html = open(GAME, encoding='utf-8').read()
    mod = open(MODULE, encoding='utf-8').read()
    for phrase in ('gaps between them', 'Each symbol stands for', 'Is the chart a fair way', 'line of best fit is drawn', 'You read the top of the part'):
        if phrase in html or phrase in mod:
            out.append('the game copies a bank phrase: %r' % phrase)
    return info


# ---------------------------------------------------------------- the page played
SVG_JS = """() => [...document.querySelectorAll('#figure svg, #exFigure svg')].filter(svg => svg.getBoundingClientRect().width > 0).map(svg => {
  const sr = svg.getBoundingClientRect(), W = Number(svg.getAttribute('width'));
  const texts = [...svg.querySelectorAll('text')].map(t => { const b = t.getBoundingClientRect(); return { s: t.textContent, x: b.left - sr.left, r: b.right - sr.left, t: b.top - sr.top, b: b.bottom - sr.top,
      cx: (b.left + b.right) / 2 - sr.left, cy: (b.top + b.bottom) / 2 - sr.top, size: parseFloat(getComputedStyle(t).fontSize) * (sr.width / (W || sr.width)), cat: t.dataset.cat || null, tick: t.dataset.tick || null, key: t.parentNode.dataset ? t.parentNode.dataset.key || null : null }; });
  const rects = [...svg.querySelectorAll('rect.bar')].map(r => { const b = r.getBoundingClientRect(); return { v: r.dataset.v === undefined ? null : Number(r.dataset.v), top: b.top - sr.top, bot: b.bottom - sr.top, h: b.height, w: b.width, cat: r.parentNode.dataset ? r.parentNode.dataset.cat || null : null, pic: r.dataset.pic || null }; });
  const dots = [...svg.querySelectorAll('circle.dot, circle.pt')].map(c => { const b = c.getBoundingClientRect(); return { cx: (b.left + b.right) / 2 - sr.left, cy: (b.top + b.bottom) / 2 - sr.top, v: c.dataset.v === undefined ? null : Number(c.dataset.v),
      x: c.dataset.x === undefined ? null : Number(c.dataset.x), y: c.dataset.y === undefined ? null : Number(c.dataset.y), pt: c.dataset.pt || null }; });
  const syms = [...svg.querySelectorAll('g[data-q]')].map(g => { const p = g.querySelector('path'), cr = g.querySelector('clipPath rect'), b = p.getBoundingClientRect();
      return { row: g.dataset.row, q: Number(g.dataset.q), clip: cr ? Number(cr.getAttribute('width')) : null, full: b.width }; });
  const keyTexts = [...svg.querySelectorAll('g[data-key] text')].map(t => t.textContent);
  const grid = [...svg.querySelectorAll('line[data-ax]')].map(l => { const b = l.getBoundingClientRect(); return { ax: l.dataset.ax, v: Number(l.dataset.gv), p: l.dataset.ax === 'y' ? (b.top + b.bottom) / 2 - sr.top : (b.left + b.right) / 2 - sr.left }; });
  const fit = svg.querySelector('line[data-fit]');
  return { W: W, H: Number(svg.getAttribute('height')), texts, grid, rects, dots, syms, keyTexts, hasFit: !!fit, label: svg.getAttribute('aria-label') }; })"""


def scale_from_ticks(texts, axis):
    """(slope, offset) of value -> pixel from the numbers printed on an axis (y: centre y; x: centre x), or None."""
    pts = []
    for t in texts:
        if re.fullmatch(r'-?\d+(\.\d+)?', t['s'].strip()):
            pts.append((float(t['s']), t['cy'] if axis == 'y' else t['cx']))
    return pts


def lin(pts):
    """Least-squares slope and intercept through (value, pixel) pairs."""
    n = len(pts)
    if n < 2:
        return None
    mx, my = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    if sxx == 0:
        return None
    m = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
    return m, my - m * mx


def read_value(scale, px):
    return (px - scale[1]) / scale[0]


def check_svgs(svgs, q, out, where):
    ch = q['chart']
    for s in svgs:
        for t in s['texts']:
            if t['s'].strip() and t['size'] < 12 - 1e-6:
                out.append('%s: chart text %.1f px (needs 12 or more): %r' % (where, t['size'], t['s'][:20]))
                break
        # no label leaves the chart or sits on another label
        boxes = [t for t in s['texts'] if t['s'].strip()]
        for t in boxes:
            if t['x'] < -1 or t['r'] > s['W'] + 1:
                out.append('%s: label %r leaves the chart (%.0f..%.0f of %d)' % (where, t['s'][:20], t['x'], t['r'], s['W']))
                break
        hit = None
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if a['x'] < b['r'] - 1 and b['x'] < a['r'] - 1 and a['t'] < b['b'] - 2 and b['t'] < a['b'] - 2:
                    hit = (a['s'], b['s'])
                    break
            if hit:
                break
        if hit:
            out.append('%s: labels %r and %r overlap' % (where, hit[0][:18], hit[1][:18]))
        t = ch['type']
        yt = [(g['v'], g['p']) for g in s['grid'] if g['ax'] == 'y']
        # every number printed on the up axis sits level with its own gridline
        for tx in s['texts']:
            if re.fullmatch(r'\d+(\.\d+)?', tx['s'].strip()) and tx['cat'] is None and tx['r'] <= 36.5 and tx['t'] > 14:
                near = [g for g in s['grid'] if g['ax'] == 'y' and g['v'] == float(tx['s'])]
                if near and abs(near[0]['p'] - tx['cy']) > 9:
                    out.append('%s: the number %s is not level with its gridline (%.0f px out)' % (where, tx['s'], abs(near[0]['p'] - tx['cy'])))
                    break
        if t in ('bar', 'dual', 'composite', 'lying') and ch.get('form') != 'pics':
            ys = lin(yt)
            if not ys:
                out.append('%s: the up axis has no numbers' % where)
                continue
            if t == 'lying':
                ticks = ch['ticks']
                # the numbers printed are the ticks, equally spaced on the page
                nums = sorted(v for v, _ in yt)
                if nums != sorted(ticks):
                    out.append('%s: axis numbers %s, the chart says %s' % (where, nums, ticks))
                else:
                    pos = {v: y for v, y in yt}
                    step = [pos[ticks[i]] - pos[ticks[i + 1]] for i in range(len(ticks) - 1)]
                    if max(step) - min(step) > 1.5:
                        out.append('%s: the ticks are not equally spaced on the page: %s' % (where, [round(x, 1) for x in step]))
                continue
            bars = [r for r in s['rects'] if r['v'] is not None]
            for r in (bars if t != 'composite' else []):
                got = read_value(ys, r['top'])
                if abs(got - r['v']) > 0.6:
                    out.append('%s: a bar drawn up to %.1f on the axis, its data says %s' % (where, got, r['v']))
                    break
            # the data attributes agree with the chart data
            want = []
            for c in ch['cats']:
                if t == 'bar':
                    want.append(c['value'])
                else:
                    want += c['values']
            have = [r['v'] for r in bars]
            if sorted(have) != sorted(want):
                out.append('%s: bars drawn %s, the chart data is %s' % (where, sorted(have), sorted(want)))
            if t in ('dual', 'composite'):
                for nm in ch['series']:
                    if nm not in s['keyTexts']:
                        out.append('%s: series %r has no written key' % (where, nm))
            if t == 'composite':
                # a part's drawn length is its own value, not its top
                for r in bars:
                    if abs(abs(read_value(ys, r['top']) - read_value(ys, r['bot'])) - r['v']) > 0.6:
                        out.append('%s: a stacked part is drawn %.1f long, its data says %s' % (where, abs(read_value(ys, r['top']) - read_value(ys, r['bot'])), r['v']))
                        break
        elif t == 'line':
            ys = lin(yt)
            if not ys:
                out.append('%s: the up axis has no numbers' % where)
                continue
            for d in s['dots']:
                if d['v'] is not None and abs(read_value(ys, d['cy']) - d['v']) > 0.6:
                    out.append('%s: a point drawn at %.1f, its data says %s' % (where, read_value(ys, d['cy']), d['v']))
                    break
            if sorted(d['v'] for d in s['dots']) != sorted(p['value'] for p in ch['points']):
                out.append('%s: points drawn %s, the chart data is %s' % (where, sorted(d['v'] for d in s['dots']), sorted(p['value'] for p in ch['points'])))
        elif t == 'scatter':
            ys = lin(yt)
            xs = lin([(g['v'], g['p']) for g in s['grid'] if g['ax'] == 'x'])
            if not ys or not xs:
                out.append('%s: a scatter axis has no numbers' % where)
                continue
            bad = [d for d in s['dots'] if d['x'] is not None and (abs(read_value(xs, d['cx']) - d['x']) > 0.6 * ch['xMax'] / 10 or abs(read_value(ys, d['cy']) - d['y']) > 0.6 * max(1, ch['yMax'] / 50))]
            if bad:
                out.append('%s: a point is drawn at (%.1f, %.1f), its data says (%s, %s)' % (where, read_value(xs, bad[0]['cx']), read_value(ys, bad[0]['cy']), bad[0]['x'], bad[0]['y']))
            if len([d for d in s['dots'] if d['x'] is not None]) != len(ch['points']):
                out.append('%s: %d points drawn, the data has %d' % (where, len([d for d in s['dots'] if d['x'] is not None]), len(ch['points'])))
            if bool(ch['line']) != s['hasFit']:
                out.append('%s: the line of best fit is %s the data' % (where, 'drawn but not in' if s['hasFit'] else 'in the data but not drawn from'))
        elif t == 'pictogram':
            rows = {}
            for sy in s['syms']:
                if sy['row'] == 'key':
                    continue
                rows[sy['row']] = rows.get(sy['row'], 0) + sy['q']
                if sy['q'] < 4 and sy['clip'] is None:
                    out.append('%s: a %d-quarter symbol is drawn whole (no cut)' % (where, sy['q']))
                if sy['clip'] is not None and abs(sy['clip'] / (sy['full'] + 0.0) - sy['q'] / 4) > 0.12:
                    out.append('%s: a %d-quarter symbol is drawn %.2f of a whole symbol wide' % (where, sy['q'], sy['clip'] / sy['full']))
            want = {r['label']: r['q'] for r in ch['rows']}
            if rows != want:
                out.append('%s: pictogram rows drawn %s, the data is %s' % (where, rows, want))
            if not ch['keyHidden']:
                kt = [x['s'] for x in s['texts'] if x['s'].startswith('= ')]
                if not kt or kt[0] != '= %s %s' % (ch['per'], ch['what']):
                    out.append('%s: the key text %s does not say = %s %s' % (where, kt, ch['per'], ch['what']))
                if any(x['s'].startswith('Key:') for x in s['texts']):
                    out.append('%s: a stray "Key:" is on the chart' % where)
    return


def fill(page, vals):
    page.evaluate("""(vals) => { [...document.querySelectorAll('#answer input')].forEach((el, i) => {
        el.value = String(vals[i]); el.dispatchEvent(new Event('input', { bubbles: true })); }); }""", [str(v) for v in vals])


def check_screen(page, q, out, where, qtag, fold):
    """The question on screen: the answer controls and the keypad above the fold, no sideways scroll, the chart read back."""
    m = page.evaluate("""() => { const r = [...document.querySelectorAll('#answer input, #answer button, #kpHolder button')].filter(x => x.offsetParent).map(x => x.getBoundingClientRect());
        return { last: r.length ? Math.max(...r.map(x => x.bottom)) : 0, sw: document.documentElement.scrollWidth, iw: innerWidth, right: r.length ? Math.max(...r.map(x => x.right)) : 0 }; }""")
    if m['last'] > fold + 0.5:
        out.append('%s %s (%s): answer controls end at %d, below the fold (%d)' % (where, qtag, q['kind'], m['last'], fold))
    if m['sw'] > m['iw'] or m['right'] > m['iw'] + 0.5:
        out.append('%s %s: sideways scroll or a control off the screen (%d > %d)' % (where, qtag, max(m['sw'], m['right']), m['iw']))
    fig = page.evaluate(SVG_JS)
    if not fig:
        out.append('%s %s: no chart on screen' % (where, qtag))
    else:
        check_svgs(fig, {'chart': q['chart'], 'ask': q['ask']}, out, '%s %s (%s)' % (where, qtag, q['kind']))


def fit_all(base, html, module, size, out, seeds=(1,), wrong=True):
    """Every kind of question (all 12 slots of all 5 stages) on its own at one size: fit, chart read-back, and the feedback after
    a wrong answer with Next above the fold."""
    from playwright.sync_api import sync_playwright
    fold = size[1] - 40
    where = '%dx%d' % size
    with sync_playwright() as pw:
        br, page, errs = open_page(pw, base, html, module, size)
        page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')
        try:
            for st in range(1, 6):
                for slot in range(12):
                    for seed in seeds:
                        page.evaluate('ACS.ui.preview(%d, %d, %d)' % (st, slot, seed))
                        page.wait_for_function("ACS.ui.state() === 'asking'", timeout=8000)
                        q = page.evaluate('ACS.ui.question()')
                        page.wait_for_timeout(40)
                        check_screen(page, q, out, where + ' s%d slot %d' % (st, slot), 'seed %d' % seed, fold)
                        if wrong:
                            page.evaluate('ACS.ui.answer(false)')
                            page.wait_for_timeout(60)
                            nb = page.evaluate("() => { const n = document.querySelector('.maffs-next, #nextBtn'); return n ? n.getBoundingClientRect().bottom : null; }")
                            if nb is None or nb > fold + 0.5:
                                out.append('%s s%d slot %d (%s): after a wrong answer Next is %s, below the fold (%d)' % (where, st, slot, q['kind'], nb, fold))
        except Exception as e:  # noqa: BLE001
            out.append('every-question view at %s threw: %s' % (where, str(e).splitlines()[0][:220]))
        out.extend('page error at %s: %s' % (where, e) for e in errs)
        br.close()


def play_stage(page, st, size, out, n, full):
    w, h = size
    fold = h - 40
    where = '%dx%d stage %d' % (w, h, st)
    page.evaluate('window.__ev = []; window.__sub = []')
    if full:                                           # the worked example, step by step, then the questions
        page.evaluate('ACS.ui.start(%d, true)' % st)
        page.wait_for_selector('#exBtn', state='visible')
        steps = 0
        while 'Start the questions' not in page.inner_text('#exBtn') and steps < 12:
            page.click('#exBtn')
            steps += 1
            page.wait_for_timeout(60)
        if steps < 2 or not page.query_selector('#exSteps li'):
            out.append('%s: the worked example has no steps' % where)
        page.click('#exBtn')
    else:
        page.evaluate('ACS.ui.start(%d)' % st)
    expect = 0
    for qn in range(n):
        page.wait_for_function("ACS.ui.state() === 'asking'", timeout=8000)
        q = page.evaluate('ACS.ui.question()')
        page.wait_for_timeout(100)
        check_screen(page, q, out, where, 'q%d' % qn, fold)
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
            bad = key + max(7, q['tol'] * 4 + 3)
            if kind == 'slip' and q['slips']:
                bad, note = q['slips'][0]['value'], q['slips'][0]['line']
            elif kind == 'slip':
                kind = 'wrong'
            fill(page, [key if kind == 'right' else bad])
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
            out.append('%s q%d (%s, %s): Next is %s, below the fold (%d)' % (where, qn, q['kind'], kind, fb['next'], fold))
        if fb['done'] != ok:
            out.append('%s q%d (%s): the feedback says %s' % (where, qn, kind, 'right' if fb['done'] else 'not right'))
        if note and re.sub(r'\s+', ' ', note).strip() not in re.sub(r'\s+', ' ', fb['line']):
            out.append('%s q%d: the named slip was not shown: %r (the line says %r)' % (where, qn, note[:40], fb['line'][:60]))
        if not fb['line'].strip():
            out.append('%s q%d: no feedback line' % (where, qn))
        if ok:
            page.evaluate("document.getElementById('nextBtn').click()")
        else:
            page.evaluate("document.querySelector('.maffs-next').click()")
        page.wait_for_timeout(80)
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
        if st < 5 and 'Next: Stage %d' % (st + 1) not in page.inner_text('#nextStageBtn'):
            out.append('%s: no "Next: Stage %d" button' % (where, st + 1))
        allowed = {'game_slug', 'level', 'mode', 'question_index', 'correct', 'score', 'questions_answered', 'questions_correct', 'previous_best'}
        for nm, p in page.evaluate('window.__ev'):
            if set(p) - allowed:
                out.append('%s: an event field outside the existing events: %s' % (where, sorted(set(p) - allowed)))
                break
    return expect


def play_size(base, html, module, size, out, n, full, font=False, stages=range(1, 6)):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br, page, errs = open_page(pw, base, html, module, size)
        if font:
            page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')
        try:
            for st in stages:
                play_stage(page, st, size, out, n, full)
                page.evaluate("document.getElementById('menuBtn') && document.getElementById('menuBtn').click()")
        except Exception as e:  # noqa: BLE001
            out.append('play at %dx%d threw: %s' % (size[0], size[1], str(e).splitlines()[0][:220]))
        out.extend('page error at %dx%d: %s' % (size[0], size[1], e) for e in errs)
        br.close()


def run_engine(base, html, module, out):
    from playwright.sync_api import sync_playwright
    info = {}
    with sync_playwright() as pw:
        br, page, errs = open_page(pw, base, html, module, (1280, 800))
        try:
            info.update(check_engine(page, out))
        except Exception as e:  # noqa: BLE001
            out.append('the engine checks threw: %s' % str(e).splitlines()[0][:200])
        out.extend('page error: ' + e for e in errs)
        br.close()
    return info


# Each plant: (what, file, [(old, new)], kind, [stages to play], pattern its finding must match).
PLANTS = [
    ('a wrong pictogram value (the key is ignored in a row)', 'bank',
     [("function val(ch, i) { return ch.rows[i].q * ch.per / 4; }", "function val(ch, i) { return ch.rows[i].q; }")], 'engine', [],
     r'(answer .*the chart gives|mark\(\) said)'),
    ('a tolerance of a whole gridline (wrong readings accepted)', 'bank',
     [("function tolOf(ch) { return ch.minor / 2; }", "function tolOf(ch) { return ch.minor; }")], 'engine', [],
     r'(tolerance|inside the accepted interval|mark\(\) said)'),
    ('a slip that lies inside the accepted interval (a gridline slip one half-gridline out)', 'bank',
     [("slipN('gridline-high', v + m,", "slipN('gridline-high', v + m / 4,"), ("bad = Math.abs(s.answer.value - answer.value) <= answer.tol + 1e-9 || s.answer.value < 0;", "bad = false;")], 'engine', [],
     r'slip gridline-high .* inside the accepted interval'),
    ("a stage 4 line drawn for the wrong correlation sign (the estimate off)", 'bank',
     [("function lineY(ch, x) { return ch.line.c + ch.line.m * x; }", "function lineY(ch, x) { return ch.line.c + ch.line.m * x + 5; }")], 'engine', [],
     r'(answer .*the chart gives|mark\(\) said|outlier)'),
    ('a stage 5 flaw named wrongly (a truncated axis called uneven)', 'bank',
     [("truncated: 'No: the axis does not start at 0',", "truncated: 'No: the scale has uneven steps',")], 'engine', [],
     r'(marked right is|repeated options)'),
    ("the game's marking ignoring the interval (an exact match only)", 'module',
     [("if (within(x, q.key, q.tol)) return { kind: 'right'", "if (x === q.key) return { kind: 'right'")], 'engine', [],
     r'mark\(\) said'),
    ('a correlation marked right for the wrong sign (stage 4)', 'bank',
     [("var right = TYPE3[sgn === 1 ? 0 : (sgn === -1 ? 1 : 2)];", "var right = TYPE3[sgn === 1 ? 1 : (sgn === -1 ? 0 : 2)];")], 'engine', [],
     r'(marked right is|r = )'),
    ("a bar drawn 10 per cent too tall", 'page',
     [("fillRect(cg, id, 0, cx - w / 2, plot.bot - c.value / ch.max * plot.h, w, c.value / ch.max * plot.h);", "fillRect(cg, id, 0, cx - w / 2, plot.bot - c.value * 1.1 / ch.max * plot.h, w, c.value * 1.1 / ch.max * plot.h);")], 'play', [2],
     r'a bar drawn up to'),
    ('a half symbol drawn as a whole one', 'page',
     [("if (quarters < 4) {\n      var cl", "if (quarters < 0) {\n      var cl")], 'play', [1],
     r'(symbol is drawn|pictogram rows drawn|drawn whole)'),
    ('a wrong answer counted as a mark (the page)', 'page',
     [("answered++; if (ok) { rightCount++; marks++; }", "answered++; marks++; if (ok) { rightCount++; }")], 'play', [1],
     r'(marks show|the leaderboard got|game_completed says)'),
    ('chart text under 12 px', 'page',
     [(".charts text{font-family:var(--font-num);font-size:12px;", ".charts text{font-family:var(--font-num);font-size:10px;")], 'play', [2],
     r'chart text .* px'),
]


def apply_plant(html, module, bank, which, edits):
    srcs = {'page': html, 'module': module, 'bank': bank}
    src = srcs[which]
    for old, new in edits:
        if src.count(old) != 1:
            return None
        src = src.replace(old, new)
    srcs[which] = src
    return srcs['page'], srcs['module'], srcs['bank']


def run_plant(plant, html, module, bank, shard=None):
    what, which, edits, kind, stages, want = plant
    planted = apply_plant(html, module, bank, which, edits)
    if planted is None:
        print('  self-test %-72s *** CANNOT PLANT ***' % what)
        return False
    h2, m2, b2 = planted
    got = []
    proc, base = bc.start_stub_server()
    try:
        # the bank is served from the planted source for the page and the engine alike
        if kind == 'engine':
            run_engine_planted(base, h2, m2, b2, got)
        else:
            play_planted(base, h2, m2, b2, got, stages)
    finally:
        proc.terminate()
    hit = [g for g in got if re.search(want, g)]
    print('  self-test %-72s %s' % (what, ('caught: ' + hit[0][:90]) if hit else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '')))
    return bool(hit)


def run_engine_planted(base, html, module, bank, out):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br, page, errs = open_page_bank(pw, base, html, module, bank, (1280, 800))
        try:
            check_engine(page, out)
        except Exception as e:  # noqa: BLE001
            out.append('the engine checks threw: %s' % str(e).splitlines()[0][:200])
        br.close()


def play_planted(base, html, module, bank, out, stages):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br, page, errs = open_page_bank(pw, base, html, module, bank, BIG)
        try:
            for st in stages:
                play_stage(page, st, BIG, out, 3, True)
                page.evaluate("document.getElementById('menuBtn') && document.getElementById('menuBtn').click()")
        except Exception as e:  # noqa: BLE001
            out.append('play threw: %s' % str(e).splitlines()[0][:200])
        br.close()


def open_page_bank(pw, base, html, module, bank, size):
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]})
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(status=200, content_type='text/html; charset=utf-8', body=html))
    ctx.route(lambda url: url.split('?')[0].endswith('/reading-charts-game.js'), lambda route: route.fulfill(status=200, content_type='application/javascript; charset=utf-8', body=module))
    ctx.route(lambda url: url.split('?')[0].endswith('/reading-charts-generator.js'), lambda route: route.fulfill(status=200, content_type='application/javascript; charset=utf-8', body=bank))
    page = ctx.new_page()
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.ACS && !!ACS.ui', timeout=10000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, []


class _Plain:
    """Stand-in for bank_common's Shard until SHARD (#578) merges: every unit, in order."""
    def __init__(self, args):
        self.spec = getattr(args, 'shard', None)

    def pick(self, units):
        return list(units)

    def unit(self, uid):
        return contextlib.nullcontext()


def main():
    ap = argparse.ArgumentParser()
    if hasattr(bc, 'shard_args'):
        bc.shard_args(ap)
    else:
        ap.add_argument('--shard', default=None)
        ap.add_argument('--list-units', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    shard = bc.Shard(__file__, args) if hasattr(bc, 'Shard') else _Plain(args)
    units = ['engine', 'full %dx%d' % BIG] + ['first %dx%d' % s for s in SMALL] + ['plant: ' + p[0] for p in PLANTS]
    if args.list_units:
        print('\n'.join(units))
        return 0
    mine = shard.pick(units)
    html = open(GAME, encoding='utf-8').read()
    module = open(MODULE, encoding='utf-8').read()
    bank = open(BANKJS, encoding='utf-8').read()
    out = []
    proc, base = bc.start_stub_server()
    try:
        if 'engine' in mine:
            with shard.unit('engine'):
                info = run_engine(base, html, module, out)
            print('%s: %s' % (SLUG, info))
        if 'full %dx%d' % BIG in mine:
            with shard.unit('full %dx%d' % BIG):
                play_size(base, html, module, BIG, out, 10, True)
            print('%s: all five stages played at %dx%d' % (SLUG, BIG[0], BIG[1]))
        for size in SMALL:
            uid = 'first %dx%d' % size
            if uid in mine:
                with shard.unit(uid):
                    play_size(base, html, module, size, out, 3, False, font=True)
                print('%s: three questions a stage at %dx%d' % (SLUG, size[0], size[1]))
    finally:
        proc.terminate()
    ok = True
    for p in PLANTS:
        if 'plant: ' + p[0] in mine:
            with shard.unit('plant: ' + p[0]):
                ok = run_plant(p, html, module, bank) and ok
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
