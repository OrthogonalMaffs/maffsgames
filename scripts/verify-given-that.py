#!/usr/bin/env python3
# ci-line: Given That (every table, Venn and tree consistent with its totals; all 180 keys recomputed; free entry marked by MaffsAnswer: the exact fraction, or a decimal to 3 s.f., in Chromium) |
"""Given That: every diagram checked against its own totals, every key recomputed, every answer marked in Chromium.

The game (90 questions, two phases each: gcse 25 multiple choice, alevel 25, core 20, level4 20 typed) shows a
two-way table, a Venn diagram or a frequency tree and asks for a probability, then a conditional one. Its bank
was keyed by hand with no verifier; the resit audit of 4 Oct 2026 found (given-that-r-001) alevel_18's Venn
drawn with only-P 20 while its stored P total and its key used 60 (20 + 45 = 65): a student reading the diagram
correctly was marked wrong. Free entry was marked within 0.005 of a stored 4 d.p. value with no precision
stated (r-002: correctly rounded answers rejected; r-003: named wrong answers on small probabilities accepted),
and two multiple-choice items offered two wrong options equal in value (audit F4, F5).

SPEC gives each phase's answer as named quantities of its own diagram (reviewed against the question's
words; a Yes/No table's headers are pinned, so the meaning of "Yes" cannot drift). Then, for every question:
  - the diagram is consistent: a table's cells add to its row and column totals and the grand total; a Venn's
    regions add to each stored set total and to the total; a tree's leaves add to their branch and the branches
    to the total; every "(x%)" in a branch label is its share of the total; the title's count is the total;
  - each phase's key (answerDisplay) equals the SPEC fraction exactly, and the stored decimal is it to 4 d.p.;
  - multiple choice: four distinct options, the key first, no wrong option equal in value to the key or to
    another option (SR-4, SR-16);
  - free entry: the answer is the exact fraction or a decimal to 3 significant figures, marked at the decimal
    places that keep three (3 d.p. from 0.1 up, 4 d.p. from 0.01, 5 d.p. below); no other ratio of two of the
    diagram's own counts rounds to the key unless it is equal in value (a wrong answer must not be accepted:
    r-003); at least one free-entry item is 3/7 (Jon's case: 3/7 and 0.429 right, 0.43 wrong);
  - the phase 2 explanation states the key's fraction.
In Chromium (390x844), through the game's own functions: every multiple-choice option clicked (the key right,
the others wrong); every free-entry question says "as a fraction, or as a decimal to 3 significant figures"; its
key typed as a decimal is right, and as the fraction in lowest terms and unreduced (so the game's exact key,
exactOf(), is checked against the diagram); each other ratio from the diagram, typed as a decimal and as a
fraction, is wrong; the exact value typed unrounded is not marked ("format"); on a 3/7 item, 0.43 is wrong.
A self-test plants the audit's faults back into a copy of the page (r-001's Venn; F4's 30/90; r-002's 0.005
rule; r-004's decimals only); each must FAIL naming its item.

    python scripts/verify-given-that.py [--no-selftest] [--against FILE]
"""
import argparse
import json
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'given-that'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'gcse': 25, 'alevel': 25, 'core': 20, 'level4': 20}


def T(p1n, p1d, p2n, p2d, headers=None):
    """A question's spec: each phase as (numerator quantities, denominator quantities), summed."""
    lst = lambda v: v if isinstance(v, list) else [v]
    return {'p1': (lst(p1n), lst(p1d)), 'p2': (lst(p2n), lst(p2d)), 'headers': headers}


SPEC = {
    'gcse_01': T('row[Pass]', 'grand', 'cell[Pass,Yes]', 'col[Yes]', ('Maths result', 'Took revision class?')),
    'gcse_02': T('row[Yes]', 'grand', 'cell[Yes,Contact]', 'col[Contact]', ('Injured this season?', 'Sport')),
    'gcse_03': T('row[Late]', 'grand', 'cell[Late,Bus]', 'col[Bus]'),
    'gcse_04': T('row[Yes]', 'grand', 'cell[Yes,Female]', 'col[Female]', ('Owns a pet?', 'Gender')),
    'gcse_05': T('row[A/B]', 'grand', 'cell[A/B,Yes]', 'col[Yes]', ('Test grade', 'Completed all homework?')),
    'gcse_06': T('B', 'total', 'AB', 'A'),
    'gcse_07': T('A', 'total', 'AB', 'B'),
    'gcse_08': T('A', 'total', 'AB', 'B'),
    'gcse_09': T('B', 'total', 'AB', 'A'),
    'gcse_10': T('B', 'total', 'AB', 'A'),
    'gcse_11': T('row[High]', 'grand', 'cell[High,Sunny]', 'col[Sunny]'),
    'gcse_12': T('row[Yes]', 'grand', 'cell[Yes,Samsung]', 'col[Samsung]', ('Uses screen protector?', 'Phone brand')),
    'gcse_13': T('L[Win]', 'total', 'l[Heads>Win]', 'b[Heads]'),
    'gcse_14': T('L[Red]', 'total', 'l[Even>Red]', 'b[Even]'),
    'gcse_15': T('row[Hot]', 'grand', 'cell[Hot,Year 10]', 'col[Year 10]'),
    'gcse_16': T('B', 'total', 'AB', 'A'),
    'gcse_17': T('row[Yes]', 'grand', 'cell[Yes,Left]', 'col[Left]', ('Wears glasses?', 'Hand')),
    'gcse_18': T('L[Sour]', 'total', 'l[Red>Sour]', 'b[Red]'),
    'gcse_19': T('row[Yes]', 'grand', 'cell[Yes,Yes]', 'col[Yes]', ('Caught flu?', 'Had flu jab?')),
    'gcse_20': T('A', 'total', 'AB', 'B'),
    'gcse_21': T('L[Late]', 'total', 'l[Peak>Late]', 'b[Peak]'),
    'gcse_22': T('row[Yes]', 'grand', 'cell[Yes,Past papers]', 'col[Past papers]', ('Passed exam?', 'Main revision method')),
    'gcse_23': T('B', 'total', 'AB', 'A'),
    'gcse_24': T('L[Wins prize]', 'total', 'l[Gold ticket>Wins prize]', 'b[Gold ticket]'),
    'gcse_25': T('row[Poor]', 'grand', 'cell[Poor,Year 9]', 'col[Year 9]'),
    'alevel_01': T('row[Recovered]', 'grand', 'cell[Recovered,Treatment]', 'col[Treatment]'),
    'alevel_02': T('A', 'total', 'AB', 'B'),
    'alevel_03': T('L[Defective]', 'total', 'l[Machine A (60%)>Defective]', 'L[Defective]'),
    'alevel_04': T('row[STEM]', 'grand', 'cell[STEM,Male]', 'col[Male]'),
    'alevel_05': T('L[Forecast rain]', 'total', 'l[Actually rains>Forecast rain]', 'L[Forecast rain]'),
    'alevel_06': T('AorB', 'total', 'AB', 'A'),
    'alevel_07': T('row[Yes]', 'grand', 'cell[Yes,Late]', 'col[Late]', ('Missed a deadline?', 'Arrived late?')),
    'alevel_08': T('L[Tests positive]', 'total', 'l[Has disease (2%)>Tests positive]', 'L[Tests positive]'),
    'alevel_09': T('AorB', 'total', 'AB', 'A'),
    'alevel_10': T('L[Flagged]', 'total', 'l[Cheated (5%)>Flagged]', 'L[Flagged]'),
    'alevel_11': T('col[X]', 'grand', 'cell[Y,X]', 'row[Y]'),
    'alevel_12': T('L[Eligible]', 'total', 'l[Type A (42%)>Deferred]', 'L[Deferred]'),
    'alevel_13': T('AB', 'total', 'onlyB', 'B'),
    'alevel_14': T('cell[Yes,Yes]', 'col[Yes]', 'cell[Yes,Yes]', 'row[Yes]', ('Bought B?', 'Bought A?')),
    'alevel_15': T('L[Offered place]', 'total', 'l[Private school (15%)>Offered place]', 'L[Offered place]'),
    'alevel_16': T('col[X = 2]', 'grand', 'cell[Y = 2,X = 2]', 'row[Y = 2]'),
    'alevel_17': T('l[1st card Red>2nd Red]', 'total', 'l[1st card Red>2nd Red]', 'L[2nd Red]'),
    'alevel_18': T('AB', 'total', 'AB', 'B'),
    'alevel_19': T('row[Yes]', 'grand', 'cell[Yes,Under 30]', 'col[Under 30]', ('Prefers online?', 'Age group')),
    'alevel_20': T('L[Defective]', 'total', 'l[Supplier C (20%)>Defective]', 'L[Defective]'),
    'alevel_21': T('cell[Yes,Engineering]', 'grand', 'cell[Yes,Engineering]', 'col[Engineering]', ('Completed training?', 'Department')),
    'alevel_22': T('AB', 'total', 'AB', 'A'),
    'alevel_23': T('L[Flagged]', 'total', 'l[Spam (40%)>Flagged]', 'L[Flagged]'),
    'alevel_24': T("cell[B,A']", 'grand', 'cell[B,A]', 'row[B]'),
    'alevel_25': T('L[Tests positive]', 'total', 'l[Uses substance (1%)>Tests positive]', 'L[Tests positive]'),
    'core_01': T('row[Serious]', 'grand', 'cell[Serious,No]', 'col[No]', ('Injury', 'Seatbelt worn?')),
    'core_02': T('L[Positive result]', 'total', 'l[Pregnant (10%)>Positive result]', 'L[Positive result]'),
    'core_03': T('row[Dissatisfied]', 'grand', 'cell[Dissatisfied,5+ days]', 'col[5+ days]'),
    'core_04': T('L[Tests positive]', 'total', 'l[Has COVID (5%)>Tests positive]', 'L[Tests positive]'),
    'core_05': T('row[High]', 'grand', 'cell[High,High-fat]', 'col[High-fat]'),
    'core_06': T('L[Scanner alerts]', 'total', 'l[Contains prohibited item (0.2%)>Scanner alerts]', 'L[Scanner alerts]'),
    'core_07': T('row[Yes]', 'grand', 'cell[Yes,17-25]', 'col[17-25]', ('Made a claim?', 'Age group')),
    'core_08': T('L[Forecast rain]', 'total', 'l[Actually rains (30%)>Forecast rain]', 'L[Forecast rain]'),
    'core_09': T('row[Poor]', 'grand', 'cell[Poor,> 4 hours]', 'col[> 4 hours]'),
    'core_10': T('L[Mammogram positive]', 'total', 'l[Has breast cancer (1%)>Mammogram positive]', 'L[Mammogram positive]'),
    'core_11': T('row[Yes]', 'grand', 'cell[Yes,Engineering]', 'col[Engineering]', ('Completed?', 'Sector')),
    'core_12': T('L[Alarm sounds]', 'total', 'l[Real fire (0.5%)>Alarm sounds]', 'L[Alarm sounds]'),
    'core_13': T('row[Yes]', 'grand', 'cell[Yes,Online]', 'col[Online]', ('Support policy?', 'Survey method')),
    'core_14': T('L[Fails test]', 'total', 'l[Over limit (3%)>Fails test]', 'L[Fails test]'),
    'core_15': T('row[Pass]', 'grand', 'cell[Pass,Yes]', 'col[Yes]', ('Exam result', 'Had energy drink?')),
    'core_16': T('L[Hired]', 'total', 'l[Internal (25%)>Hired]', 'L[Hired]'),
    'core_17': T('row[E/U]', 'grand', 'cell[E/U,Uses phone]', 'col[Uses phone]'),
    'core_18': T('L[Drops out]', 'total', 'l[First generation (35%)>Drops out]', 'L[Drops out]'),
    'core_19': T('row[Yes]', 'grand', 'cell[Yes,Flat]', 'col[Flat]', ('Recycles regularly?', 'Household type')),
    'core_20': T(['l[Pass first time (60%)>No re-sit needed]', 'l[Fail first time (40%)>Pass re-sit]'], 'total',
                 'l[Fail first time (40%)>Pass re-sit]', 'b[Fail first time (40%)]'),
    'l4_01': T('L[Out of tolerance]', 'total', 'l[Line B (30%)>Out of tolerance]', 'L[Out of tolerance]'),
    'l4_02': T('row[Yes]', 'grand', 'cell[Yes,X-ray]', 'col[X-ray]', ('Defect found?', 'Inspection method')),
    'l4_03': T(['l[A fails (5%)>System fails]', 'l[A works (95%)>B fails \u2192 system fails]'], 'total',
               'l[A fails (5%)>System fails]', ['l[A fails (5%)>System fails]', 'l[A works (95%)>B fails \u2192 system fails]']),
    'l4_04': T('row[Major defect]', 'grand', 'cell[Major defect,Night]', 'col[Night]'),
    'l4_05': T('L[Inaccurate]', 'total', 'l[Uncalibrated (40%)>Inaccurate]', 'L[Inaccurate]'),
    'l4_06': T('row[Fail]', 'grand', 'cell[Fail,S460]', 'col[S460]'),
    'l4_07': T('L[Sudden failure]', 'total', 'l[Overload (25%)>Sudden failure]', 'L[Sudden failure]'),
    'l4_08': T('row[No]', 'grand', 'cell[No,M4]', 'col[M4]', ('Within tolerance?', 'CNC machine')),
    'l4_09': T('L[Passes 28-day strength]', 'total', 'l[7-day cure>Passes 28-day strength]', 'b[7-day cure]'),
    'l4_10': T('row[Yes]', 'grand', 'cell[Yes,Reactive]', 'col[Reactive]', ('Extended downtime (>4hrs)?', 'Maintenance type')),
    'l4_11': T(['l[Crack present (2%)>NDT detects]', 'l[No crack (98%)>NDT false positive]'], 'total',
               'l[Crack present (2%)>NDT detects]', ['l[Crack present (2%)>NDT detects]', 'l[No crack (98%)>NDT false positive]']),
    'l4_12': T('row[Thermal]', 'grand', 'cell[Thermal,Switching]', 'col[Switching]'),
    'l4_13': T('L[Accepted]', 'total', 'l[Bad batch (>2% defective)>Accepted]', 'L[Accepted]'),
    'l4_14': T('row[Yes]', 'grand', 'cell[Yes,Op C]', 'col[Op C]', ('Agrees with reference?', 'Operator')),
    'l4_15': T('L[Vibration alarm triggered]', 'total', 'l[Motor will fail (8%)>Vibration alarm triggered]', 'L[Vibration alarm triggered]'),
    'l4_16': T('row[Yes]', 'grand', 'cell[Yes,Quench & temper]', 'col[Quench & temper]', ('Meets hardness spec?', 'Treatment')),
    'l4_17': T('b[Error occurs (3%)]', 'total', 'l[Error occurs (3%)>EMI interference]', 'b[Error occurs (3%)]'),
    'l4_18': T('row[No]', 'grand', 'cell[No,Brand Z]', 'col[Brand Z]', ('Within \u00b14% accuracy?', 'Brand')),
    'l4_19': T('L[Warranty claim]', 'total', 'l[Budget (15%)>Warranty claim]', 'L[Warranty claim]'),
    'l4_20': T('row[No]', 'grand', 'cell[No,SAC305 (lead-free)]', 'col[SAC305 (lead-free)]', ('Survives 1000 cycles?', 'Solder type')),
}
AUDIT = {('alevel_18', 'p2'): 'given-that-r-001', ('gcse_14', 'p2'): 'audit F4, B11', ('gcse_23', 'p2'): 'audit F5, B11'}


def num(v):
    """A stored count or probability as an exact Fraction (0.12 is 12/100, never a binary float)."""
    return F(str(v))


def quantities(d):
    """{name: Fraction} for every count (or probability) the diagram shows or implies."""
    out = {}
    if d['type'] == 'table':
        for i, r in enumerate(d['rows']):
            for j, c in enumerate(d['cols']):
                out['cell[%s,%s]' % (r, c)] = num(d['values'][i][j])
            out['row[%s]' % r] = num(d['rowTotals'][i])
        for j, c in enumerate(d['cols']):
            out['col[%s]' % c] = num(d['colTotals'][j])
        out['grand'] = num(d['grandTotal'])
    elif d['type'] == 'venn':
        oa, ob, ab, nb = (num(d[k]) for k in ('onlyA', 'onlyB', 'intersection', 'neither'))
        out.update({'onlyA': oa, 'onlyB': ob, 'AB': ab, 'neither': nb, 'A': oa + ab, 'B': ob + ab,
                    'AorB': oa + ob + ab, 'total': num(d['total'])})
    else:
        for br in d['branches']:
            out['b[%s]' % br['label']] = num(br['value'])
            for ch in br['children']:
                out['l[%s>%s]' % (br['label'], ch['label'])] = num(ch['value'])
        for lab in {ch['label'] for br in d['branches'] for ch in br['children']}:
            out['L[%s]' % lab] = sum((num(ch['value']) for br in d['branches'] for ch in br['children'] if ch['label'] == lab), F(0))
        out['total'] = num(d['total'])
    return out


def consistency(d):
    """[fault] for a diagram whose parts do not add up to the totals it states."""
    bad = []
    if d['type'] == 'table':
        v = [[num(x) for x in row] for row in d['values']]
        for i, r in enumerate(d['rows']):
            if sum(v[i], F(0)) != num(d['rowTotals'][i]):
                bad.append('row %s adds to %s, its total says %s' % (r, sum(v[i], F(0)), d['rowTotals'][i]))
        for j, c in enumerate(d['cols']):
            if sum((v[i][j] for i in range(len(v))), F(0)) != num(d['colTotals'][j]):
                bad.append('column %s adds to %s, its total says %s' % (c, sum((v[i][j] for i in range(len(v))), F(0)), d['colTotals'][j]))
        if sum((num(t) for t in d['rowTotals']), F(0)) != num(d['grandTotal']) or \
                sum((num(t) for t in d['colTotals']), F(0)) != num(d['grandTotal']):
            bad.append('the totals do not add to the grand total %s' % d['grandTotal'])
    elif d['type'] == 'venn':
        oa, ob, ab, nb, tot = (num(d[k]) for k in ('onlyA', 'onlyB', 'intersection', 'neither', 'total'))
        if oa + ab != num(d['setA']['total']):
            bad.append('the %s regions add to %s, the stored %s total is %s' % (d['setA']['label'], oa + ab, d['setA']['label'], d['setA']['total']))
        if ob + ab != num(d['setB']['total']):
            bad.append('the %s regions add to %s, the stored %s total is %s' % (d['setB']['label'], ob + ab, d['setB']['label'], d['setB']['total']))
        if oa + ob + ab + nb != tot:
            bad.append('the regions add to %s, the total is %s' % (oa + ob + ab + nb, tot))
    else:
        tot = num(d['total'])
        if sum((num(b['value']) for b in d['branches']), F(0)) != tot:
            bad.append('the branches add to %s, the total is %s' % (sum((num(b['value']) for b in d['branches']), F(0)), tot))
        for b in d['branches']:
            if sum((num(c['value']) for c in b['children']), F(0)) != num(b['value']):
                bad.append('branch %s: its leaves add to %s, not %s' % (b['label'], sum((num(c['value']) for c in b['children']), F(0)), b['value']))
            m = re.search(r'\((\d+(?:\.\d+)?)%\)', b['label'])
            if m and F(m.group(1)) != num(b['value']) / tot * 100:
                bad.append('branch %s: %s is %s%% of %s' % (b['label'], b['value'], float(num(b['value']) / tot * 100), tot))
    m = re.match(r'([\d,]+) ', d.get('title', ''))
    total = d.get('grandTotal', d.get('total'))
    if m and F(m.group(1).replace(',', '')) != num(total):
        bad.append('the title says %s, the total is %s' % (m.group(1), total))
    return bad


def display_value(s):
    """answerDisplay as an exact Fraction: \\tfrac{a}{b} (a, b may be decimals), a plain decimal, or 'x = v'."""
    s = s.strip()
    m = re.match(r'\\tfrac\{([\d.]+)\}\{([\d.]+)\}', s)
    if m:
        return F(m.group(1)) / F(m.group(2))
    if re.fullmatch(r'\d+(\.\d+)?', s):
        return F(s)
    raise ValueError('cannot read answerDisplay %r' % s)


def half_up(v, dp):
    """An exact Fraction rounded half up to dp places, as a Decimal."""
    return (D(v.numerator) / D(v.denominator)).quantize(D(1).scaleb(-dp), rounding=ROUND_HALF_UP)


def dp_for(answer):
    """The game's dpFor(): the decimal places that keep three significant figures."""
    a = F(str(answer))
    return 3 if not a > 0 or a >= F(1, 10) else 4 if a >= F(1, 100) else 5


def ratios(qs):
    """Every ratio a/b of two of the diagram's quantities with 0 < b and a <= b: the probabilities a student
    could read off it by a slip (the wrong total, the wrong cell, the reverse condition)."""
    vals = sorted(set(qs.values()))
    return {a / b for a in vals for b in vals if b > 0 and a <= b}


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s questions by level, expected %s (a change needs SPEC reviewed)' % (counts, COUNTS))
        return {}
    free = {}
    for lv in COUNTS:
        for q in bank[lv]:
            d = q['data']
            if q['id'] not in SPEC:
                fails.append('%s: not in SPEC' % q['id'])
                continue
            sp_ = SPEC[q['id']]
            tag = lambda ph: '%s %s%s' % (q['id'], ph, ' (%s)' % AUDIT[(q['id'], ph)] if (q['id'], ph) in AUDIT else '')
            for fault in consistency(d):
                fails.append('%s: %s' % (tag('p2') if q['id'] == 'alevel_18' else q['id'], fault))
            if sp_['headers'] and (d.get('rowHeader'), d.get('colHeader')) != sp_['headers']:
                fails.append('%s: the table headers %r are not the reviewed %r' % (q['id'], (d.get('rowHeader'), d.get('colHeader')), sp_['headers']))
            qs = quantities(d)
            for ph, key in (('p1', 'phase1'), ('p2', 'phase2')):
                pd = q[key]
                w = tag(ph)
                try:
                    ns, ds = sp_[ph]
                    target = sum((qs[n] for n in ns), F(0)) / sum((qs[n] for n in ds), F(0))
                except KeyError as e:
                    fails.append('%s: SPEC names %s, which the diagram does not have' % (w, e))
                    continue
                try:
                    shown = display_value(pd['answerDisplay'])
                except ValueError as e:
                    fails.append('%s: %s' % (w, e))
                    continue
                if shown != target:
                    fails.append('%s: keyed %s = %s, the answer from the diagram is %s = %s'
                                 % (w, pd['answerDisplay'], shown, target, float(target)))
                stored = D(str(pd['answer']))
                places = max(-stored.as_tuple().exponent, 0)
                if half_up(target, places) != stored:
                    fails.append('%s: stored answer %s is not the key %s rounded to %d d.p.'
                                 % (w, pd['answer'], float(target), places))
                if ph == 'p2':
                    fr = re.findall(r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)', pd.get('explanation', ''))
                    if fr and not any(F(a) / F(b) == target for a, b in fr):
                        fails.append('%s: the explanation states no fraction equal to the key: %r' % (w, pd['explanation']))
                if lv == 'gcse' and pd.get('options'):
                    opts = pd['options']
                    vals = []
                    for o in opts:
                        try:
                            vals.append(display_value(o))
                        except ValueError as e:
                            fails.append('%s: %s' % (w, e))
                            vals.append(None)
                    if len(opts) != 4 or len(set(opts)) != 4 or opts[0] != pd['answerDisplay']:
                        fails.append('%s: options %s are not four distinct with the key first' % (w, opts))
                    for o, v in zip(opts[1:], vals[1:]):
                        if v is not None and v == target:
                            fails.append('%s: the wrong option %s equals the key (SR-16)' % (w, o))
                    for i in range(4):
                        for k in range(i + 1, 4):
                            if vals[i] is not None and vals[i] == vals[k]:
                                fails.append('%s: options %s and %s are equal in value (SR-4)' % (w, opts[i], opts[k]))
                    continue
                DP = dp_for(pd['answer'])
                if DP != dp_for(target):
                    fails.append('%s: the stored %s asks for %d d.p., the exact key needs %d' % (w, pd['answer'], DP, dp_for(target)))
                slips = sorted(r for r in ratios(qs) if r != target and half_up(r, DP) == half_up(target, DP))
                for r in slips:
                    fails.append('%s: %s (another ratio from the diagram) also rounds to the key %s at %d d.p.'
                                 % (w, r, half_up(target, DP), DP))
                others = sorted({half_up(r, DP) for r in ratios(qs) if half_up(r, DP) != half_up(target, DP)})
                # The exact value typed to 4 d.p.: right if the key needs no rounding, otherwise a value that
                # rounds to the key but is not it ('format', not marked).
                exact4 = half_up(target, 4).normalize()
                want4 = 'right' if F(str(exact4)) == F(str(half_up(target, DP))) else \
                    'unmarked' if half_up(F(str(exact4)), DP) == half_up(target, DP) else 'wrong'
                wrong_fracs = sorted(r for r in ratios(qs) if r != target)
                free[(lv, q['id'], ph)] = {'key': str(half_up(target, DP)), 'dp': DP, 'want4': want4,
                                           'exact4': format(exact4, 'f'), 'others': [str(o) for o in others],
                                           'fracs': ['%d/%d' % (target.numerator, target.denominator),
                                                     '%d/%d' % (3 * target.numerator, 3 * target.denominator)],
                                           'wrong_fracs': ['%d/%d' % (r.numerator, r.denominator) for r in wrong_fracs],
                                           'is37': target == F(3, 7)}
    if not any(f['is37'] for f in free.values()):
        fails.append('bank: no free-entry item is 3/7 (the 3/7, 0.429, 0.43 check has nothing to run on)')
    return free


HOOK = ('window.__gt={Q:QUESTIONS,set:function(lv,q){currentLevel=lv;sessionQuestions=[q];currentQIndex=0;'
        'phase2Attempt=0},showQuestion:showQuestion,toPhase2:transitionToPhase2};\n')

SWEEP_JS = r"""(free) => {
  window.setTimeout = () => 0;
  const G = window.__gt, out = [];
  const fb = () => { const f = document.getElementById('feedback'); return {
      right: f.classList.contains('correct-fb'), wrong: f.classList.contains('wrong-fb'), text: f.textContent }; };
  const open = (lv, q, ph) => { G.set(lv, q); G.showQuestion(); if (ph === 'p2') G.toPhase2(q); };
  for (const lv of Object.keys(G.Q)) G.Q[lv].forEach((q) => {
    for (const ph of ['p1', 'p2']) {
      const pd = ph === 'p1' ? q.phase1 : q.phase2;
      if (lv === 'gcse' && pd.options) {
        for (const opt of pd.options) {
          open(lv, q, ph);
          const btn = [...document.querySelectorAll('#answerArea .mcq-btn')].find(b => b.dataset.latex === opt);
          if (!btn) { out.push([q.id, ph, opt, 'not on screen']); continue; }
          btn.click();
          const r = fb();
          if (r.right !== (opt === pd.options[0])) out.push([q.id, ph, opt, r.right ? 'marked right' : 'marked wrong']);
        }
        continue;
      }
      const f = free[lv + '|' + q.id + '|' + ph];
      if (!f) { out.push([q.id, ph, '', 'free entry the bank check did not see']); continue; }
      const tries = [[f.key, 'right'], [f.exact4, f.want4]]
        .concat(f.fracs.map(o => [o, 'right']), f.others.map(o => [o, 'wrong']), f.wrong_fracs.map(o => [o, 'wrong']),
                f.is37 ? [['3/7', 'right'], ['0.429', 'right'], ['0.43', 'wrong']] : []);
      open(lv, q, ph);
      if (!document.getElementById('questionText').textContent.endsWith(
          ' Give your answer as a fraction, or as a decimal to 3 significant figures.'))
        out.push([q.id, ph, '', 'the question does not state its precision (a fraction, or 3 s.f.)']);
      if (document.getElementById('freeInput').placeholder !== 'e.g. 3/7 or 0.429')
        out.push([q.id, ph, '', 'the placeholder does not show both forms']);
      for (const [typed, want] of tries) {
        open(lv, q, ph);
        const input = document.getElementById('freeInput');
        input.value = typed;
        document.querySelector('#answerArea .submit-btn').click();
        const r = fb(), marked = input.disabled;
        const got = !marked ? 'unmarked' : r.right ? 'right' : 'wrong';
        if (got !== want) out.push([q.id, ph, typed, 'expected ' + want + ', got ' + got + ' (' + r.text.slice(0, 60) + ')']);
      }
    }
  });
  return out;
}"""


def hook(html):
    """The page with its private functions exposed to the sweep (served copy only, never written)."""
    m = list(re.finditer(r'\n\}\)\(\);\n</script>\n<script src="\.\./\.\./schools/assets/teacher-invite\.js">', html.replace('\r\n', '\n')))
    if len(m) != 1:
        return None
    h = html.replace('\r\n', '\n')
    return h[:m[0].start()] + '\n' + HOOK + h[m[0].start():]


def play(fails, html, free):
    from playwright.sync_api import sync_playwright
    hooked = hook(html)
    if hooked is None:
        fails.append('page: cannot find the end of the game script to expose its functions to the sweep')
        return
    args = {'%s|%s|%s' % k: v for k, v in free.items()}
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=hooked))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('window.__gt && typeof katex !== "undefined"', timeout=15000)
            if not page.evaluate('() => !!window.MaffsAnswer'):
                fails.append('page (given-that-r-002): free entry is not marked by MaffsAnswer (schools/assets/answer.js not loaded)')
            for id_, ph, typed, what in page.evaluate(SWEEP_JS, args):
                lab = '%s %s' % (id_, ph)
                fails.append('%s%s in Chromium: %s%s' % (lab, ' (%s)' % AUDIT[(id_, ph)] if (id_, ph) in AUDIT else '',
                                                          ('typed %s: ' % typed) if typed else '', what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()


def load_bank(html):
    tree, _ = bc.parse_game_source(html)
    if tree is None:
        return None
    for name, init, _ in bc.iife_scoped_declarations(tree):
        if name == 'QUESTIONS':
            return bc.static_bank_value(name, init, tree)
    return None


def run(html):
    fails = []
    bank = load_bank(html)
    if bank is None:
        return ['bank: QUESTIONS not found in the page'], 0
    free = check_bank(fails, bank)
    play(fails, html, free)
    return fails, sum(len(v) for v in bank.values())


PLANTS = [
    ('alevel_18 p2', 'r-001: only-P 20 drawn beside a P total of 60',
     'setB:{label:"P",total:60},onlyA:35,onlyB:15,intersection:45,neither:55',
     'setB:{label:"P",total:60},onlyA:35,onlyB:20,intersection:45,neither:50'),
    ('gcse_14 p2', 'F4: 30/90 beside 60/180',
     '"\\\\tfrac{60}{180}","\\\\tfrac{30}{180}","\\\\tfrac{90}{180}"', '"\\\\tfrac{60}{180}","\\\\tfrac{30}{90}","\\\\tfrac{90}{180}"'),
    ('core_04 p1', "r-002/r-003: marked within 0.005, no precision",
     "result=MaffsAnswer.fractionOrDecimal(raw,ex[0],ex[1],dp);",
     "result=Math.abs(parseFloat(raw)-phaseData.answer)<=0.005?'correct':'wrong';"),
    ('alevel_01 p1', "r-004: decimals only, the fraction unreadable",
     "result=MaffsAnswer.fractionOrDecimal(raw,ex[0],ex[1],dp);",
     "result=MaffsAnswer.decimal(raw,(ex[0]/ex[1]).toFixed(dp),dp);"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='check this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, n = run(html)
    print('%s: %d questions (%d phases): every diagram, key and option checked; every answer marked in Chromium'
          % (SLUG, n, 2 * n))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-48s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep, _ = run(html.replace(old, new))
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-48s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
