#!/usr/bin/env python3
# ci-line: Football Pitches per Squared Squirrel, part 1 (Stage 1 the fixed ramp in order; every pool question's key recomputed from its data by units and dimensions, its unit the quantity asked, its named slips recomputed and none equal to the key, Stages 2-3 friendly whole numbers, at least 40 a stage, sessions easiest first; no nonsense unit or squirrel in any question, option, hint or worked line; no formula-triangle wording or drawing) | --part 1
# ci-line: Football Pitches per Squared Squirrel, part 2 (every stage played to its results screen at 1280 and 320 px: the worked example logs nothing, Stage 1's retry keeps the mark, the no-unit "squirrels" message loud, spaced from the unit buttons, marking nothing and cleared by picking a unit, the wrong unit marks nothing, named slips, the calculator in Stages 4-5 only, no sideways scroll) | --part 2
# ci-line: Football Pitches per Squared Squirrel, part 3 (fault-injection self-test: six of the twelve planted faults, each caught) | --part 3
# ci-line: Football Pitches per Squared Squirrel, part 4 (fault-injection self-test: the other six planted faults, each caught) | --part 4
# ci-deps: games/squared-squirrel/
"""Independent verification for Football Pitches per Squared Squirrel (games/squared-squirrel/), built 23 Oct 2026
(contract FOOTBALL-PITCHES, Jon). SR-30: checked from its first PR.

WHY THIS READS THE LIVE PAGE
-------------------------------------------------------------------------------
The game keeps every decision a student sees (Stage 1's fixed ramp, the pools, every key, every named slip, the worked
steps, the order a stage is served in) on window.SQS as plain functions, and its UI calls them through SQS. This script
loads the page under Playwright, reads THOSE pools and sessions, and recomputes everything here, in Python, from each
question's data and the contract's words, never from the game's own functions:

  Keys       every given quantity turned into base units by this script's own table (km = 1000 m, h = 3600 s,
             1 hour 30 minutes = 5400 s, cm3 = 1e-6 m3, ...), then the one product or quotient of the givens whose
             dimensions are the answer unit's (a speed is length / time): that is the quantity asked, and the key is it
             in the answer's unit. No combination with the answer unit's dimensions is a unit that does not fit the
             question. Compare questions: each option's rate the same way, the faster (the bigger speed) or the better
             value (the smaller price per kg). Stages 2-3 whole numbers; 4-5 to 1 d.p., half up; money to the penny.
  Slips      the contract's named wrong answers, recomputed here from the numbers as written: multiplied instead of
             divided and the reverse, divided the wrong way round, minutes read as decimals (1 h 30 min as 1.3 h;
             0.75 h as 75 minutes), a per-hour rate used with the minutes unconverted, m/s and km/h by 3.6 the wrong
             way or by the wrong factor. The game's list is exactly these; none gives the key at its precision.
  Friendly   Stages 2-3: every number whole, and each operation a times-table fact: a factor of 10 or less, or a
             division whose divisor or quotient is 10 or less.
  Ramp       Stage 1 is exactly the contract's ten questions, in its order, each wrong option with a reason.
  Sessions   SESSIONS seeds a stage: a worked example (not one of the 10), then 10 from the stage's pool, distinct,
             no nonsense unit, served in non-decreasing order of the measure (recomputed here from the
             contract's comment: the kind's rank, then the largest number written in the question).
  Static     no formula triangle: not the word, not a drawing (a polygon or a triangle character), not "cover up".
  Real units no question, option, hint, worked line, slip line or unit button says "squirrel" or "football pitch"
             (contract SQS-REAL-UNITS, Jon's play-test, 24 Oct 2026): squirrels live only in the title, the start
             screen's premise and the no-unit message, which must be loud (the accent, bold, body size, the unit
             buttons outlined) and clear as soon as a unit is picked.
  Play       every stage end to end at 1280x800 and 320x568, read from the page (canon 7.9).
"""
import argparse
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'squared-squirrel'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4', 'stage-5']
STAGE_N = {m: i + 1 for i, m in enumerate(MODES)}
CALC_STAGES = {'stage-4', 'stage-5'}
MIN_POOL = 40
SESSIONS = 40
SIZES = [(1280, 800), (320, 568)]
EPS = 1e-9

# Stage 1, the contract's words: (question, the right option, [wrong options]); question 10 typed: 4 mph.
RAMP = [
    ('“The sign says 30 mph.” What does it mean?', '30 miles every hour', ['30 hours every mile', '30 miles in total']),
    ('“Apples are £2 per kg.”', '£2 for each kg', ['£2 for all the apples', '2 kg for each £1']),
    ('Miles per hour is…', 'miles ÷ hours', ['hours ÷ miles', 'miles × hours']),
    ('km/h is…', 'km ÷ h', ['h ÷ km', 'km × h']),
    ('£/kg is said…', 'pounds per kilogram', ['kilograms per pound', 'pounds times kilograms']),
    ('m² means…', 'm × m', ['m × 2', 'm + m']),
    ('cm³ means…', 'cm × cm × cm', ['cm × 3', 'cm + cm + cm']),
    ('g/cm³ is…', 'g ÷ (cm × cm × cm)', ['(cm × cm × cm) ÷ g', 'g × cm × 3']),
    # Question 9 since contract SQS-REAL-UNITS (Jon's play-test, 24 Oct 2026): a real unit, not the title's.
    ('people/km² is…', 'people ÷ (km × km)', ['(km × km) ÷ people', 'people ÷ (km × 2)']),
]
RAMP_TYPED = ('12 miles in 3 hours. How many miles per hour?', 4, 'mph')
RAMP_EXAMPLE = ['Crisps are 80p per bag: 80p for each bag.', '“Per” means “for each”.']

# ---------------------------------------------------------------- units: this script's own table
# name -> (scale to base units, dimensions). P is a football pitch, Q a squirrel's length (a squared squirrel is Q^2).
BASE = {
    'km': (1000.0, {'L': 1}), 'miles': (1609.344, {'L': 1}), 'm': (1.0, {'L': 1}),
    'h': (3600.0, {'T': 1}), 'min': (60.0, {'T': 1}), 's': (1.0, {'T': 1}),
    'g': (1.0, {'M': 1}), 'kg': (1000.0, {'M': 1}), 'N': (1.0, {'F': 1}), 'gbp': (1.0, {'$': 1}),
    'pitch': (1.0, {'P': 1}), 'cm3': (1e-6, {'L': 3}), 'm2': (1.0, {'L': 2}), 'sq': (1.0, {'Q': 2}),
}
RATE = {'kmh': ('km', 'h'), 'mph': ('miles', 'h'), 'ms': ('m', 's'), 'gcm3': ('g', 'cm3'), 'Nm2': ('N', 'm2'),
        'gbpkg': ('gbp', 'kg'), 'gbpm': ('gbp', 'm'), 'psq': ('pitch', 'sq'), 'pph': ('pitch', 'h'), 'ppm': ('pitch', 'min')}
TEXT = {'km': 'km', 'miles': 'miles', 'm': 'm', 'h': 'h', 'min': 'min', 's': 's', 'g': 'g', 'kg': 'kg', 'N': 'N',
        'gbp': '£', 'pitch': 'pitches', 'cm3': 'cm³', 'm2': 'm²', 'sq': 'squirrel²', 'kmh': 'km/h', 'mph': 'mph',
        'ms': 'm/s', 'gcm3': 'g/cm³', 'Nm2': 'N/m²', 'gbpkg': '£/kg', 'gbpm': '£/m', 'psq': 'pitches/squirrel²',
        'pph': 'pitches/h', 'ppm': 'pitches/min'}


def dims_mul(a, b, sign=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + sign * v
        if out[k] == 0:
            del out[k]
    return out


def unit(u):
    """(scale, dims) of a unit name, a rate built from its two parts."""
    if u in BASE:
        return BASE[u]
    a, b = RATE[u]
    return BASE[a][0] / BASE[b][0], dims_mul(BASE[a][1], BASE[b][1], -1)


def quantity(g):
    """A given quantity in base units: (value, dims). A time {h, m} is in seconds."""
    if g['u'] == 'hm':
        return 3600.0 * g['h'] + 60.0 * g['m'], {'T': 1}
    s, d = unit(g['u'])
    return g['v'] * s, d


def written(g):
    """A given's number as the question writes it (a time in hours, as a calculation would use it)."""
    return g['h'] + g['m'] / 60 if g['u'] == 'hm' else g['v']


def combine(given, ask):
    """The one product or quotient of the givens with the answer unit's dimensions: (value in the answer unit, op), or
    (None, reason)."""
    s, d = unit(ask)
    qs = [quantity(g) for g in given]
    if len(qs) == 1:
        cands = [('conv', qs[0])]
    else:
        (a, da), (b, db) = qs
        cands = [('mul', (a * b, dims_mul(da, db))), ('div', (a / b, dims_mul(da, db, -1))), ('rdiv', (b / a, dims_mul(db, da, -1)))]
    hit = [(op, v) for op, (v, dd) in cands if dd == d]
    if len(hit) != 1:
        return None, '%d ways to make %s from %s' % (len(hit), TEXT.get(ask, ask), [g['u'] for g in given])
    op, v = hit[0]
    return v / s, op


def rnd(x, dp):
    f = 10 ** dp
    return math.floor(x * f + 0.5 + 1e-9) / f


def precision(q):
    """(dp, money) from the stage and the unit, the contract's rule: whole numbers in Stages 2-3, 1 d.p. in 4-5, money
    (an answer in £ or £/kg) to the penny in 4-5."""
    if q['mode'] in ('stage-1', 'stage-2', 'stage-3'):
        return 0, False
    if q['unit'] in ('gbp', 'gbpkg', 'gbpm'):
        return 2, True
    return 1, False


def expected_key(q):
    dp, money = precision(q)
    if q.get('opts'):
        vals = []
        for o in q['opts']:
            v, op = combine(o['given'], q['unit'])
            if v is None:
                return None, None, op
            vals.append(v)
        pick = 'max' if q['unit'] in ('kmh', 'mph', 'ms') else 'min'   # faster; better value
        if q.get('pick') != pick:
            return None, None, 'compares by %s, not %s' % (q.get('pick'), pick)
        exact = max(vals) if pick == 'max' else min(vals)
        return exact, rnd(exact, dp), 'cmp'
    v, op = combine(q['given'], q['unit'])
    if v is None:
        return None, None, op
    return v, rnd(v, dp), op


# ---------------------------------------------------------------- the named slips (the contract's list)
def slips_of(given, ask, op):
    A = given[0]
    out = []
    if len(given) == 1:
        v = A['v']
        if A['u'] == 'ms' and ask == 'kmh':
            out = [('SD', v / 3.6), ('SF', v * 3600), ('SF', v / 1000)]
        elif A['u'] == 'kmh' and ask == 'ms':
            out = [('SD', v * 3.6), ('SF', v / 3600), ('SF', v * 1000)]
        elif A['u'] == 'ppm' and ask == 'pph':
            out = [('MU', v), ('DIV', v / 60)]
        return out
    B = given[1]
    a, b = written(A), written(B)
    hm = B if B['u'] == 'hm' else None
    if ask == 'min':   # a time asked in minutes: distance / rate hours, then x 60
        return [('MUL', a * b), ('REV', b / a * 60), ('MD', a / b * 100)]
    if op == 'div':
        out = [('MUL', a * b), ('REV', b / a)]
        if hm:
            out += [('MD', a / (hm['h'] + hm['m'] / 100)), ('MU', a / (60 * hm['h'] + hm['m']))]
    elif op == 'mul':
        out = [('DIV', a / b)]
        if hm:
            out += [('MD', a * (hm['h'] + hm['m'] / 100)), ('MU', a * (60 * hm['h'] + hm['m']))]
    return out


def expected_slips(q):
    if q.get('opts'):
        rates = []
        for o in q['opts']:
            a, t = o['given']
            T = written(t)
            rates.append({'r': a['v'] / T, 'MUL': a['v'] * T, 'REV': T / a['v'],
                          'MD': a['v'] / (t['h'] + t['m'] / 100) if t['u'] == 'hm' else None,
                          'MU': a['v'] / (60 * t['h'] + t['m']) if t['u'] == 'hm' else None})
        best = max if q['pick'] == 'max' else min
        w = best(rates, key=lambda r: r['r'])
        out = [('MUL', w['MUL']), ('REV', w['REV'])]
        for k in ('MD', 'MU'):
            vs = [r[k] for r in rates]
            if None not in vs:
                out.append((k, best(vs)))
        return out
    _, _, op = expected_key(q)
    return slips_of(q['given'], q['unit'], op)


# ---------------------------------------------------------------- the measure (the contract's comment)
def largest(q):
    gs = [g for o in q['opts'] for g in o['given']] if q.get('opts') else q['given']
    return max(max(g['h'], g['m']) if g['u'] == 'hm' else g['v'] for g in gs)


def rank(q):
    m = q['mode']
    if m == 'stage-3':
        return 0 if expected_key(q)[2] == 'mul' else 1
    if m == 'stage-4':
        if len(q['given']) == 1:
            return 1 if q['given'][0]['u'] == 'ppm' else 3
        t = q['given'][1]
        return 0 if t['m'] == 30 else 1 if t['m'] in (15, 45) else 2
    if m == 'stage-5':
        if q.get('opts'):
            return 2
        return 1 if q['unit'] == 'min' else 0
    return 0


def measure(q):
    return (rank(q), largest(q))


def nonsense(q):
    gs = [g for o in q['opts'] for g in o['given']] if q.get('opts') else q['given']
    return any(g['u'] in ('pitch', 'sq', 'psq', 'pph', 'ppm') for g in gs) or q['unit'] in ('pitch', 'sq', 'psq', 'pph', 'ppm')


def friendly(q, out, where):
    """Stages 2-3: every number whole; the operation a times-table fact."""
    nums = [g['v'] for g in q['given']]
    if any(abs(v - round(v)) > EPS for v in nums) or abs(q['key'] - round(q['key'])) > EPS:
        out.append('%s: not whole numbers (%s -> %s): Stages 2-3 are non-calculator' % (where, nums, q['key']))
        return
    a, b = nums
    op = expected_key(q)[2]
    ok = (min(a, b) <= 10) if op == 'mul' else (b <= 10 or q['key'] <= 10)
    if not ok:
        out.append('%s: %s %s %s is not a times-table fact' % (where, a, 'x' if op == 'mul' else '/', b))


# ---------------------------------------------------------------- the engine
def check_question(q, out, where):
    exact, key, why = expected_key(q)
    if exact is None:
        out.append('%s: the answer unit %s does not fit the question (%s)' % (where, TEXT.get(q['unit']), why))
        return
    dp, money = precision(q)
    if (q['dp'], q['money']) != ((0 if money else dp), money):
        out.append('%s: precision dp %s money %s; the stage asks %s' % (where, q['dp'], q['money'], 'money' if money else '%d d.p.' % dp))
    if abs(q['key'] - key) > 1e-9:
        out.append('%s: key %s, recomputed from its data %s' % (where, q['key'], key))
    if dp == 1 and 'to 1 decimal place' not in q['text']:
        out.append('%s: the question does not state its precision' % where)
    if money and 'to the nearest penny' not in q['text']:
        out.append('%s: the question does not state its precision (to the nearest penny)' % where)
    gs = [g for o in q['opts'] for g in o['given']] if q.get('opts') else q['given']
    for g in gs:   # every given number is written in the question
        s = ('%d hour' % g['h'] if g['h'] else '') if g['u'] == 'hm' else None
        if g['u'] == 'hm':
            if g['m'] and '%d minutes' % g['m'] not in q['text'] or (g['h'] and s not in q['text']):
                out.append('%s: the time %s h %s min is not in the question' % (where, g['h'], g['m']))
        else:
            v = g['v']
            reps = {('%.2f' % v), ('%g' % v), ('%d' % v if abs(v - round(v)) < EPS else '%g' % v)}
            if not any(re.search(r'(?<![\d.])' + re.escape(r) + r'(?![\d])', q['text']) for r in reps):
                out.append('%s: the given %s %s is not in the question %r' % (where, v, g['u'], q['text'][:80]))
    want = sorted((i, round(v, 6)) for i, v in expected_slips(q) if v > 0 and math.isfinite(v))
    got = sorted((e['id'], round(e['v'], 6)) for e in q['errors'])
    if want != got:
        out.append('%s: named slips %s, expected %s' % (where, got, want))
    for i, v in want:
        if rnd(v, dp) == key:
            out.append('%s: the named slip %s gives the key %s' % (where, i, key))
    if q['unit'] not in q['units'] or len(set(q['units'])) != len(q['units']):
        out.append('%s: the unit buttons %s do not offer the answer\'s unit once' % (where, q['units']))
    if q['mode'] in ('stage-2', 'stage-3'):
        friendly(q, out, where)


def check_steps(q, steps, answer_text, out, where):
    if not steps or not steps[-1]['text'].rstrip('.').endswith(answer_text):
        out.append('%s: the working does not end on the answer %r: %r' % (where, answer_text, steps[-1]['text'] if steps else None))
    for s in steps:
        if re.search(r'triangle', s['text'], re.I):
            out.append('%s: a step mentions a triangle' % where)


def check_ramp(page, out):
    got = page.evaluate('SQS.RAMP')
    if len(got) != 10:
        out.append('Stage 1 has %d questions, not the fixed ten' % len(got))
        return
    for i, (text, right, wrong) in enumerate(RAMP):
        r = got[i]
        if r.get('text') != text or r.get('right') != right or sorted(w[0] for w in r.get('wrong', [])) != sorted(wrong):
            out.append('Stage 1 question %d is %r (%r / %r), not the contract\'s %r' % (i + 1, r.get('text'), r.get('right'), r.get('wrong'), text))
        if any(not w[1].strip() for w in r.get('wrong', [])):
            out.append('Stage 1 question %d: a wrong option without its reason' % (i + 1))
    if got[9].get('text') != RAMP_TYPED[0] or not got[9].get('typed'):
        out.append('Stage 1 question 10 is not the typed %r' % RAMP_TYPED[0])
    if page.evaluate('SQS.RAMP_EXAMPLE') != RAMP_EXAMPLE:
        out.append('Stage 1\'s worked example is not the contract\'s: %s' % page.evaluate('SQS.RAMP_EXAMPLE'))
    for seed in range(1, 21):
        s = page.evaluate('s => SQS.buildSession(s, "stage-1")', seed)
        qs = [q for q in s['questions'] if not q.get('example')]
        texts = [q['text'] for q in qs]
        if texts != [r[0] for r in RAMP] + [RAMP_TYPED[0]]:
            out.append('Stage 1 seed %d: the questions are not in the contract\'s order: %s' % (seed, texts))
            break
        for q, (text, right, wrong) in zip(qs, RAMP):
            if sorted(o['text'] for o in q['options']) != sorted([right] + wrong) or [o['text'] for o in q['options'] if o['ok']] != [right]:
                out.append('Stage 1 seed %d: question %r offers %s' % (seed, text, [o['text'] for o in q['options']]))
        t = qs[9]
        if abs(t['key'] - RAMP_TYPED[1]) > EPS or t['unit'] != RAMP_TYPED[2]:
            out.append('Stage 1 question 10: key %s %s, not 4 mph' % (t['key'], t['unit']))
        if [q['index'] for q in qs if q.get('retry')] != [1, 2, 3]:
            out.append('Stage 1 seed %d: the questions tried again are %s, not 1-3' % (seed, [q['index'] for q in qs if q.get('retry')]))


def check_engine(page, out, sessions=SESSIONS):
    check_ramp(page, out)
    t = page.evaluate('(() => { const t = SQS.buildSession(1, "stage-1").questions[10]; return [t, SQS.steps(t), SQS.answerText(t)]; })()')
    check_question(t[0], out, 'stage-1 q10')
    pools = page.evaluate('SQS.pools()')
    sizes = {}
    for mode in MODES[1:]:
        P = pools[mode]
        sizes[mode] = len(P)
        ids = [q['id'] for q in P]
        content = {json.dumps([q.get('given'), q.get('opts'), q['unit']], sort_keys=True) for q in P}
        if len(set(ids)) != len(P) or len(content) != len(P):
            out.append('%s: %d questions but %d distinct' % (mode, len(P), len(content)))
        if len(P) < MIN_POOL:
            out.append('%s: %d questions in its pool, fewer than %d' % (mode, len(P), MIN_POOL))
        for q in P:
            check_question(q, out, '%s %s' % (mode, q['id'][:70]))
        for q in P:
            if nonsense(q):
                out.append('%s %s: a nonsense unit in a question (real contexts only)' % (mode, q['id'][:70]))
    # Every word a question can show, in every stage: no squirrel and no football pitch (the title, the start screen's
    # premise and the no-unit message aside, none of which is here).
    words = page.evaluate(r'''(() => {
      const out = [], P = SQS.pools();
      const add = (where, t) => out.push([where, String(t)]);
      SQS.RAMP.forEach((r, i) => { add('stage-1 q' + (i + 1), r.text); if (r.right) add('stage-1 q' + (i + 1), r.right);
        (r.wrong || []).forEach(w => { add('stage-1 q' + (i + 1), w[0]); add('stage-1 q' + (i + 1), w[1]); }); });
      SQS.RAMP_EXAMPLE.forEach(t => add('stage-1 example', t));
      const t = SQS.buildSession(1, 'stage-1').questions[10];
      const qs = [t].concat(...Object.keys(P).map(m => P[m]));
      for (const q of qs) {
        const w = (q.mode || '') + ' ' + (q.id || '').slice(0, 60);
        add(w, q.text); SQS.steps(q).forEach(s => add(w, s.text)); (q.units || []).forEach(u => add(w, SQS.unitText(u)));
        add(w, SQS.answerText(q)); add(w, SQS.rule(q, '1', q.unit));
        q.errors.forEach(e => { SQS.line(q, e.id).forEach(l => add(w, l)); add(w, SQS.example(q, e.id)); add(w, SQS.nudge(q, e.id)); });
      }
      document.querySelectorAll('.mode-btn').forEach(b => add('start screen stage button', b.textContent));
      return out; })()''')
    for where, t in words:
        if re.search(r'squirrel|football pitch', t, re.I):
            out.append('%s: shows %r: squirrels only in the title, the premise and the no-unit message' % (where, t[:90]))
    # The worked steps of every pool question end on its answer (read through the page in one call).
    st = page.evaluate('(() => { const P = SQS.pools(), out = []; for (const m in P) for (const q of P[m]) out.push([m, q.id, SQS.steps(q), SQS.answerText(q)]); return out; })()')
    for m, i, steps, ans in st:
        check_steps(None, steps, ans, out, '%s %s' % (m, i[:70]))
    for mode in MODES[1:]:
        ids = {q['id'] for q in pools[mode]}
        for seed in range(1, sessions + 1):
            s = page.evaluate('([s, m]) => SQS.buildSession(s, m)', [seed, mode])
            ex, qs = s['questions'][0], s['questions'][1:]
            where = '%s seed %d' % (mode, seed)
            if not ex.get('example') or ex['id'] in {q['id'] for q in qs}:
                out.append('%s: the worked example is missing or one of the 10' % where)
            if len(qs) != 10 or len({q['id'] for q in qs}) != 10 or any(q['id'] not in ids for q in qs):
                out.append('%s: %d questions, not 10 distinct from the pool' % (where, len(qs)))
            if any(nonsense(q) for q in qs):
                out.append('%s: a nonsense-unit question in the session' % where)
            ms = [measure(q) for q in qs]
            if ms != sorted(ms):
                out.append('%s: not easiest first by the measure: %s' % (where, ms))
            if [q['index'] for q in qs] != list(range(1, 11)):
                out.append('%s: indexes %s' % (where, [q['index'] for q in qs]))
            for q in qs:
                if sorted(q['buttons']) != sorted(q['units']):
                    out.append('%s: q%d\'s buttons %s are not its units %s' % (where, q['index'], q['buttons'], q['units']))
    return {'pools': sizes}


# ---------------------------------------------------------------- the page, statically
def static_checks(html, out):
    if 'name="robots" content="noindex"' in html:   # listed 24 Oct 2026 (Jon approved it after playing it)
        out.append('the page is noindex, but the game is listed')
    if not re.search(r'<script type="application/json" id="maffs-calc-stages">\{"stage-1": "not allowed", "stage-2": "not allowed", '
                     r'"stage-3": "not allowed", "stage-4": "scientific", "stage-5": "scientific"\}</script>', html):
        out.append('the calculator stage map is not Stages 1-3 not allowed, Stages 4-5 scientific')
    decl = re.search(r'MaffsLevel\.resolve\(\{(.*?)\}\)', html, re.S)
    if not decl or any("'%s'" % m not in decl.group(1) for m in MODES):
        out.append('MaffsLevel.resolve does not declare the boards %s' % MODES)
    # No formula triangles anywhere (contract FOOTBALL-PITCHES): no word, no drawing, no "cover up" method.
    for pat, what in [(r'triangle', 'the word "triangle"'), (r'<polygon', 'a polygon drawing'), (r'[△▲▵▴▽▼]', 'a triangle character'),
                      (r'cover (it )?up', '"cover up"'), (r'\bDST\b|\bFMV\b|\bPFA\b', 'a formula-triangle mnemonic')]:
        m = re.search(pat, html, re.I)
        if m:
            out.append('formula triangles: %s in the page (%r)' % (what, html[max(0, m.start() - 40):m.end() + 40]))


# ---------------------------------------------------------------- play
def open_page(pw, base, html, size):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.SQS && !!SQS.ui', timeout=10000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


def calc_shown(page):
    return page.evaluate("""() => { const w = document.getElementById('calcWrap'), c = document.querySelector('.maffs-calc');
        return { mounted: SQS.ui.calcMounted(), shown: !!c && !w.hidden && c.offsetParent !== null }; }""")


def squirrels(u):
    d = unit(u)[1]
    return 'squared squirrels' if d in ({'L': 2}, {'Q': 2}) else 'cubed squirrels' if d == {'L': 3} else 'squirrels'


def typed(q, v):
    dp, money = precision(q)
    if money:
        return '%.2f' % rnd(v, 2)
    return ('%.1f' % rnd(v, 1)) if dp else ('%d' % round(v))


def submit(page, box, value, unit_name):
    page.evaluate("([b, v]) => { document.querySelector(b).value = v; }", [box, value])
    if unit_name:
        page.click('.unit-btn[data-unit="%s"]' % unit_name)
    page.evaluate("document.getElementById('ansForm').requestSubmit()")


def sideways(page, size, out, where):
    sw = page.evaluate('document.documentElement.scrollWidth')
    if sw > size[0]:
        out.append('%s: sideways scroll (%d px wide at %d)' % (where, sw, size[0]))


def play_ramp(page, size, out, tag):
    right = 0
    for k in range(10):
        q = page.evaluate('SQS.ui.question()')
        where = '%s q%d' % (tag, k + 1)
        want = RAMP[k][0] if k < 9 else RAMP_TYPED[0]
        shown = page.inner_text('#qtext').strip()
        if shown != want:
            out.append('%s: shows %r, not the contract\'s %r (Stage 1 is a fixed ramp, in order)' % (where, shown, want))
        sideways(page, size, out, where)
        if k < 9:
            n0 = page.evaluate("window.__ev.filter(e => e[0] === 'question_answered').length")
            wrong_i = [i for i, o in enumerate(q['options']) if not o['ok']][0]
            right_i = [i for i, o in enumerate(q['options']) if o['ok']][0]
            if k in (0, 1, 2):   # a wrong first try: its reason, tried again, the mark kept
                page.click('#opts [data-i="%d"]' % wrong_i)
                evs = page.evaluate("window.__ev.filter(e => e[0] === 'question_answered')")
                if page.evaluate('SQS.ui.state()') != 'pick' or q['options'][wrong_i]['why'] not in page.inner_text('#msg'):
                    out.append('%s: a wrong first try did not show its reason and ask again' % where)
                if len(evs) != n0 + 1 or evs[-1][1].get('correct') is not False:
                    out.append('%s: a wrong first try logged %s, not one correct:false' % (where, evs[n0:]))
                page.click('#opts [data-i="%d"]' % right_i)
                if page.evaluate("window.__ev.filter(e => e[0] === 'question_answered').length") != n0 + 1:
                    out.append('%s: the retry logged a second question_answered' % where)
                if page.evaluate('SQS.ui.state()') != 'right':
                    out.append('%s: the right retry was not marked right (the mark kept)' % where)
                right += 1
            elif k == 4:         # a wrong answer after question 3: its reason, the answer, Next
                page.click('#opts [data-i="%d"]' % wrong_i)
                fb = page.evaluate("""() => { const f = document.querySelector('#feedback .fb');
                    return f ? [f.querySelector('.fb-line').textContent, f.querySelector('.fb-ans').textContent, !!f.querySelector('.fb-next button')] : null; }""")
                if page.evaluate('SQS.ui.state()') != 'wrong' or not fb or fb[0] != q['options'][wrong_i]['why'] or fb[1] != RAMP[k][1] or not fb[2]:
                    out.append('%s: a wrong answer did not show its reason, the answer and Next: %s' % (where, fb))
                else:
                    page.click('#feedback .fb-next button')
                continue
            else:
                page.click('#opts [data-i="%d"]' % right_i)
                right += 1
            page.wait_for_function("SQS.ui.state() !== 'right'", timeout=8000)
        else:
            right += play_typed(page, size, out, where, q, wrong=False, check_units=True)
    return right


# The no-unit message as shown (its own line under the unit buttons, above the keypad, and inside the window): its colour is the accent (read from an element painted in it), bold, at least the body
# text's size, 4.5:1 on the card, and every unit button outlined.
LOUD_JS = r"""() => {
  const m = document.getElementById('noUnitMsg'), cs = getComputedStyle(m), card = getComputedStyle(document.getElementById('qcard'));
  const accent = getComputedStyle(document.getElementById('stageLabel')).color;
  const rgb = c => (c.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
  const lum = c => { const v = rgb(c).map(x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  const a = lum(cs.color), b = lum(card.backgroundColor);
  const btns = [...document.querySelectorAll('#units .unit-btn')];
  return { accent: cs.color === accent, bold: parseInt(cs.fontWeight, 10) >= 700,
    size: parseFloat(cs.fontSize) >= parseFloat(getComputedStyle(document.querySelector('.qtext')).fontSize) - 0.5,
    contrast: Math.round((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05) * 100) / 100,
    seen: m.getBoundingClientRect().height > 0 && m.getBoundingClientRect().bottom <= window.innerHeight - 40 &&
      (!document.getElementById('kpHolder').firstElementChild || !document.getElementById('kpHolder').firstElementChild.offsetHeight ||
       m.getBoundingClientRect().bottom <= document.getElementById('kpHolder').getBoundingClientRect().top + 1),
    outlined: btns.length > 0 && btns.every(x => getComputedStyle(x).outlineStyle === 'solid' && parseFloat(getComputedStyle(x).outlineWidth) >= 2) };
}"""


# Room to breathe (Jon's play-test, 24 Oct 2026): with the no-unit highlight on, buttons in a row at least 8 px apart and
# far enough that their outlines (width plus the pulse's largest offset, from the page's own keyframes) never touch; the
# message 10 px below the buttons and 12 px above whatever follows it (the keypad or the Calculator toggle).
NEXT_JS = r"""() => { const n = [document.querySelector('#kpHolder > *'), document.querySelector('#calcWrap:not([hidden]) .maffs-calc-toggle')]
  .filter(e => e && e.offsetHeight)[0]; return n ? n.getBoundingClientRect().top + window.scrollY : null; }"""
LAYOUT_JS = r"""() => {
  const btns = [...document.querySelectorAll('#units .unit-btn')].map(b => b.getBoundingClientRect());
  const cs = getComputedStyle(document.querySelector('#units .unit-btn'));
  let off = parseFloat(cs.outlineOffset) || 0;
  for (const sh of document.styleSheets) { let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    for (const r of rules) if (r.type === CSSRule.KEYFRAMES_RULE && r.name === 'unitPulse')
      for (const k of r.cssRules) off = Math.max(off, parseFloat(k.style.outlineOffset) || 0); }
  const reach = (parseFloat(cs.outlineWidth) || 0) + off;
  let gap = Infinity;
  for (let i = 1; i < btns.length; i++) if (Math.abs(btns[i].top - btns[i - 1].top) < 2) gap = Math.min(gap, btns[i].left - btns[i - 1].right);
  for (let i = 0; i < btns.length; i++) for (let j = 0; j < btns.length; j++) if (btns[j].top > btns[i].bottom - 1)
    gap = Math.min(gap, btns[j].top - btns[i].bottom);
  const m = document.getElementById('noUnitMsg').getBoundingClientRect(), u = document.getElementById('units').getBoundingClientRect();
  const n = [document.querySelector('#kpHolder > *'), document.querySelector('#calcWrap:not([hidden]) .maffs-calc-toggle')].filter(e => e && e.offsetHeight)[0];
  return { gap: gap === Infinity ? null : Math.round(gap * 10) / 10, reach, above: Math.round((m.top - u.bottom) * 10) / 10,
    below: n ? Math.round((n.getBoundingClientRect().top - m.bottom) * 10) / 10 : null, height: m.height,
    small: btns.some(b => b.width < 43.5 || b.height < 43.5) };
}"""


def play_typed(page, size, out, where, q, wrong, check_units, named_n=None):
    box = '#ans4' if q['mode'] in CALC_STAGES else '#ans'
    if page.evaluate('SQS.ui.state()') != 'asking':
        out.append('%s: no answer box (%s)' % (where, page.evaluate('SQS.ui.state()')))
        return 0
    n0 = page.evaluate('window.__ev.length')
    key = typed(q, q['key'])
    if check_units:
        # No unit: the squirrels message, on the student's own number, and nothing marked.
        next0 = page.evaluate(NEXT_JS)
        submit(page, box, key, None)
        lay, next1 = page.evaluate(LAYOUT_JS), page.evaluate(NEXT_JS)
        if lay['gap'] is not None and (lay['gap'] < 8 or lay['gap'] <= 2 * lay['reach']):
            out.append('%s: the unit buttons are %s px apart with the highlight on (at least 8, and more than twice the outline\'s %s px reach)' % (where, lay['gap'], lay['reach']))
        if lay['small']:
            out.append('%s: a unit button is under 44 px' % where)
        if lay['above'] < 9.5 or (lay['below'] is not None and lay['below'] < 11.5):
            out.append('%s: the no-unit message has %s px above it and %s px below (at least 10 and 12)' % (where, lay['above'], lay['below']))
        if next0 is not None and next1 is not None and next1 - next0 > lay['height'] + 1:
            out.append('%s: showing the message moved what follows by %.1f px, more than its own %.1f px' % (where, next1 - next0, lay['height']))
        want = '%s %s? Pick the unit, or that\'s what the examiner will read.' % (key, squirrels(q['unit']))
        if page.inner_text('#noUnitMsg').strip() != want or page.evaluate('window.__ev.length') != n0 or page.evaluate('SQS.ui.state()') != 'asking':
            out.append('%s: an answer with no unit got %r and was %s; expected %r, not marked' % (
                where, page.inner_text('#noUnitMsg'), 'marked' if page.evaluate('window.__ev.length') != n0 else 'not marked', want))
        loud = page.evaluate(LOUD_JS)
        if not loud['accent'] or not loud['bold'] or not loud['size'] or loud['contrast'] < 4.5 or not loud['outlined'] or not loud['seen']:
            out.append('%s: the no-unit message is not loud: %s (the accent, bold, body size or larger, 4.5:1, the unit buttons outlined, above the keypad and in the window)' % (where, loud))
        other = [u for u in q['buttons'] if u != q['unit']][0]
        page.click('.unit-btn[data-unit="%s"]' % other)
        after = page.evaluate("() => ({ msg: document.getElementById('noUnitMsg').textContent, "
                              "need: document.getElementById('units').classList.contains('need') })")
        if after['msg'] or after['need']:
            out.append('%s: picking a unit did not clear the no-unit message and the outline: %s' % (where, after))
        page.evaluate("document.getElementById('ansForm').requestSubmit()")
        if 'Check the unit' not in page.inner_text('#msg') or page.evaluate('window.__ev.length') != n0:
            out.append('%s: the right number with the wrong unit was marked, or got no unit message' % where)
    val, named = key, None
    if wrong:
        dp, money = precision(q)
        prec = 2 if money else dp
        for e in q['errors']:
            if dp == 0 and abs(e['v'] - round(e['v'])) > EPS:
                continue
            val = typed(q, e['v'])
            named = [x['id'] for x in q['errors'] if rnd(x['v'], prec) == rnd(float(val), prec)][0]
            break
        if named is None:
            val = typed(q, q['key'] + 1)
    submit(page, box, val, q['unit'])
    sideways(page, size, out, where)
    st = page.evaluate('SQS.ui.state()')
    if not wrong:
        if st != 'right':
            out.append('%s: the key %s %s was not marked right (%s; %r)' % (where, val, q['unit'], st, page.inner_text('#msg')))
            return 0
        page.wait_for_function("SQS.ui.state() !== 'right'", timeout=8000)
        return 1
    if st != 'wrong':
        out.append('%s: a wrong answer %s was not marked wrong (%s)' % (where, val, st))
        return 0
    if named:
        named_n[0] += 1
    fb = page.evaluate("""() => { const f = document.querySelector('#feedback .fb'), l = f && f.querySelector('.fb-line');
        return f ? { err: l.getAttribute('data-err'), help: l.getAttribute('data-help'), line: l.textContent, steps: f.querySelectorAll('.steps li').length,
          ans: f.querySelector('.fb-ans').textContent, next: !!f.querySelector('.fb-next button') } : null; }""")
    want_help = ('example' if named_n[0] <= 3 else 'nudge') if named else 'rule'
    if not fb or [fb['err'], fb['help']] != [named, want_help] or not fb['steps'] or not fb['next']:
        out.append('%s: the wrong-answer screen is %s; expected the slip %s (%s), the working and Next' % (where, fb, named, want_help))
    elif re.search(r'triangle', fb['line'], re.I):
        out.append('%s: the wrong-answer line mentions a triangle' % where)
    page.click('#feedback .fb-next button')
    return 0


def play_stage(page, mode, size, out, before):
    tag = '%s at %dx%d' % (mode, size[0], size[1])
    if page.evaluate('SQS.ui.state()') != 'example':
        out.append('%s: the stage did not open on its worked example' % tag)
        return
    taps = 0
    while page.evaluate('SQS.ui.state()') == 'example' and taps < 20:
        step = page.evaluate("document.querySelector('#feedback .explain').getAttribute('data-step')")
        page.click('#stepBtn')
        taps += 1
        nxt = page.evaluate("(document.querySelector('#feedback .explain') || {getAttribute: () => null}).getAttribute('data-step')")
        if page.evaluate('SQS.ui.state()') == 'example' and nxt != str(int(step) + 1):
            out.append('%s: a tap did not reveal exactly one step' % tag)
    if page.evaluate("b => window.__ev.slice(b).filter(e => e[0] === 'question_answered').length", before):
        out.append('%s: the worked example logged a question_answered' % tag)
    c = calc_shown(page)
    if c['shown'] != (mode in CALC_STAGES):
        out.append('%s: the calculator %s' % (tag, 'is not shown' if mode in CALC_STAGES else 'is shown'))
    if mode not in CALC_STAGES and c['mounted'] and not page.evaluate('window.__calcplayed'):
        out.append('%s: the calculator is mounted before Stage 4 was played' % tag)
    badge = page.evaluate("document.getElementById('calcBadge').textContent")
    if badge != ('Scientific calculator required' if mode in CALC_STAGES else 'Non-calculator'):
        out.append('%s: the header badge reads %r' % (tag, badge))
    if mode == 'stage-1':
        right = play_ramp(page, size, out, tag)
    else:
        right, named_n = 0, [0]
        for k in range(10):
            q = page.evaluate('SQS.ui.question()')
            where = '%s q%d' % (tag, k + 1)
            if q['index'] != k + 1:
                out.append('%s: question %s shown' % (where, q['index']))
            right += play_typed(page, size, out, where, q, wrong=k in (2, 4, 6, 8), check_units=k in (0, 5), named_n=named_n)
    if page.evaluate('SQS.ui.state()') != 'done':
        out.append('%s: the results screen did not show (%s)' % (tag, page.evaluate('SQS.ui.state()')))
        return
    evs = page.evaluate('b => window.__ev.slice(b)', before)
    qas = [e for e in evs if e[0] == 'question_answered']
    if len(qas) != 10 or any(e[1].get('mode') != mode for e in qas):
        out.append('%s: %d question_answered, modes %s' % (tag, len(qas), sorted({e[1].get('mode') for e in qas})))
    done = [e for e in evs if e[0] == 'game_completed']
    if len(done) != 1 or done[0][1].get('mode') != mode or done[0][1].get('questions_correct') != right:
        out.append('%s: game_completed %s (expected %d right)' % (tag, done, right))
    sub = page.evaluate('window.__sub')
    if not sub or sub[-1][1] != mode:
        out.append('%s: the score went to %s, not the stage\'s board' % (tag, sub[-1][1] if sub else None))
    nxt = page.evaluate("(() => { const b = document.getElementById('nextStageBtn'); return b.hidden ? null : b.textContent; })()")
    want = 'Next: Stage %d' % (STAGE_N[mode] + 1) if mode != 'stage-5' else None
    if nxt != want:
        out.append('%s: the results offer %r, not %r' % (tag, nxt, want))
    if mode in CALC_STAGES:
        page.evaluate('window.__calcplayed = true')


def play(page, size, out):
    page.click('.mode-btn[data-mode="stage-1"]')
    before = page.evaluate('window.__ev.length')
    page.click('#startBtn')
    for mode in MODES:
        play_stage(page, mode, size, out, before)
        if mode != 'stage-5':
            if page.evaluate("document.getElementById('nextStageBtn').hidden"):
                return
            before = page.evaluate('window.__ev.length')
            page.click('#nextStageBtn')
    page.click('#againBtn')
    page.click('.mode-btn[data-mode="stage-2"]')
    page.click('#startBtn')
    if calc_shown(page)['shown']:
        out.append('at %dx%d: the calculator still shows in Stage 2 after Stage 5' % size)


def guarded(out, what, f):
    try:
        f()
    except Exception as e:  # noqa: BLE001 - any exception here is a finding
        out.append('%s threw: %s' % (what, str(e).splitlines()[0][:200]))


def check(html, out, engine=True, sizes=(), sessions=SESSIONS):
    from playwright.sync_api import sync_playwright
    static_checks(html, out)
    proc, base = bc.start_stub_server()
    info = {}
    try:
        with sync_playwright() as pw:
            if engine:
                br, page, errs = open_page(pw, base, html, (1280, 800))
                guarded(out, 'the engine checks', lambda: info.update(check_engine(page, out, sessions)))
                out.extend('page error: ' + e for e in errs)
                br.close()
            for size in sizes:
                br, page, errs = open_page(pw, base, html, size)
                guarded(out, 'play at %dx%d' % size, lambda: play(page, size, out))
                out.extend('page error at %dx%d: %s' % (size[0], size[1], e) for e in errs)
                info.setdefault('played', []).append('%dx%d' % size)
                br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, [(old, new), ...], what it needs to run, a pattern its finding must match). Every old text occurs
# exactly once in the page. A key equal to a named slip needs the filter off too, or the filter alone would take
# every such question out of the pool (and nothing wrong would be served).
FILTER = ("    if (H.errorIsKey(q)) return false;\n", "")
PLANTS = [
    ('a key computed by multiplying where it should divide',
     [("      case 'divi': return G[0].v / G[1].v;", "      case 'divi': return G[0].v * G[1].v;"), FILTER], 'engine',
     r':divi:.*key \S+, recomputed from its data'),
    ('a Stage 1 question out of order',
     [("    var qs = H.RAMP.map(function (r, i) {", "    var qs = H.RAMP.slice(0, 2).concat([H.RAMP[3], H.RAMP[2]], H.RAMP.slice(4)).map(function (r, i) {")],
     'engine', r'not in the contract\'s order'),
    ('a named slip equal to a key (1 hour, so km x h = km / h)',
     [("['speed', 'km', 'h', 'kmh', [20, 30, 40, 50, 60, 70, 80, 90], [2, 3, 4, 5]],",
       "['speed', 'km', 'h', 'kmh', [20, 30, 40, 50, 60, 70, 80, 90], [1, 2, 3, 4, 5]],"), FILTER], 'engine',
     r'the named slip MUL gives the key'),
    ('the word "triangle" in a hint',
     [("'Per means divide, '", "'Per means divide (use the formula triangle), '")], 'static', r'formula triangles: the word'),
    ('a no-unit answer marked wrong',
     [("    if (!unit) { msg(H.noUnit(q, raw), true); return; }", "    if (!unit) { res = 'wrong'; unit = q.unit; }")], 'play',
     r'an answer with no unit got .* and was marked'),
    ('the calculator in Stage 2',
     [("    var on = H.STAGES[mode].calc === 'scientific';", "    var on = H.STAGES[mode].calc === 'scientific' || mode === 'stage-2';")], 'play',
     r'stage-2 .*the calculator is shown'),
    ('a Stage 4 key using 1.3 for 1 h 30 min',
     [("      case 'rate': return G[0].v / val(G[1]);", "      case 'rate': return G[0].v / (G[1].u === 'hm' ? H.decimalSlip(G[1]) : val(G[1]));"), FILTER],
     'engine', r'stage-4 .*:rate:.*key \S+, recomputed from its data'),
    # Room to breathe (Jon's play-test, 24 Oct 2026).
    ('the unit buttons with no gap',
     [(".units{flex-basis:100%;display:flex;flex-wrap:wrap;justify-content:center;gap:1.25rem}",
       ".units{flex-basis:100%;display:flex;flex-wrap:wrap;justify-content:center;gap:0}")], 'play', r'the unit buttons are 0(\.0)? px apart'),
    # Contract SQS-REAL-UNITS (Jon's play-test, 24 Oct 2026).
    ('a nonsense-unit question left in Stage 3',
     [("    gbpkg: { t: '£/kg', of: ['gbp', 'kg'] }, gbpm: { t: '£/m', of: ['gbp', 'm'] }\n  };",
       "    gbpkg: { t: '£/kg', of: ['gbp', 'kg'] }, gbpm: { t: '£/m', of: ['gbp', 'm'] },\n    pitch: { t: 'pitches' }, sq: { t: 'squirrel²', d: 2 }, psq: { t: 'pitches/squirrel²', of: ['pitch', 'sq'] }\n  };"),
      ("    ['price', 'gbp', 'm', 'gbpm', [2, 3, 4, 5], [3, 6, 10]]\n  ];",
       "    ['price', 'gbp', 'm', 'gbpm', [2, 3, 4, 5], [3, 6, 10]],\n    ['price', 'pitch', 'sq', 'psq', [2, 3], [2, 3]]\n  ];")], 'engine',
     r'stage-3 .*psq.*(a nonsense unit in a question|squirrel)'),
    ('the old Stage 1 question 9',
     [("{ text: 'people/km² is…', right: 'people ÷ (km × km)', wrong: [",
       "{ text: 'Football pitches per squared squirrel is…', right: 'football pitches ÷ (squirrel × squirrel)', wrong: [")], 'engine',
     r'Stage 1 question 9 is .*Football pitches'),
    ('the no-unit message in the old muted style',
     [(".msg.no-unit{color:var(--accent);font-weight:700;font-size:1.05rem}\n", "")], 'play', r'the no-unit message is not loud'),
    ('the message not clearing after a unit is picked',
     [("    if ($('noUnitMsg').textContent) msg('');   // picking a unit answers the no-unit message\n", "")], 'play',
     r'picking a unit did not clear the no-unit message'),
]


# The plants in two CI lines (24 Oct 2026: one line of all twelve took 212 s, over ci-groups' per-line limit), balanced by
# kind: the slow ones that play the game alternate between part 3 and part 4, and so do the quick ones.
def plants_for(part):
    heavy = [p for p in PLANTS if p[2] == 'play']
    light = [p for p in PLANTS if p[2] != 'play']
    return heavy[0::2] + light[1::2] if part == '3' else heavy[1::2] + light[0::2]


def selftest(html, plants=None):
    ok = True
    for what, edits, kind, want in (PLANTS if plants is None else plants):
        planted = html
        bad = False
        for old, new in edits:
            if planted.count(old) != 1:
                bad = True
                break
            planted = planted.replace(old, new)
        if bad:
            print('  self-test %-58s *** CANNOT PLANT ***' % what)
            ok = False
            continue
        got = []
        if kind == 'static':
            static_checks(planted, got)
        else:
            check(planted, got, engine=kind == 'engine', sizes=[(1280, 800)] if kind == 'play' else [], sessions=6)
        hit = [g for g in got if re.search(want, g)]
        ok = ok and bool(hit)
        print('  self-test %-58s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***' + (' (other findings: %s)' % got[0][:100] if got else '')))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--part', choices=['1', '2', '3', '4'], help='one of the four parts CI runs side by side (default: all)')
    ap.add_argument('--sessions', type=int, default=SESSIONS)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    part = args.part
    out = []
    info = {}
    if part in (None, '1', '2'):
        info = check(html, out, engine=part in (None, '1'), sizes=SIZES if part in (None, '2') else [], sessions=args.sessions)
    if 'pools' in info:
        print('%s: pools %s (Stage 1 the fixed ramp of 10); %d sessions a stage' % (SLUG, info['pools'], args.sessions))
    if 'played' in info:
        print('%s: every stage played at %s' % (SLUG, ', '.join(info['played'])))
    ok = True
    if part in (None, '3', '4'):
        ok = selftest(html, None if part is None else plants_for(part))
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
