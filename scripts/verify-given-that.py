#!/usr/bin/env python3
# ci-shards: Given That (every table, Venn and tree consistent with its totals; all 180 keys recomputed; free entry marked by MaffsAnswer: the exact fraction, or a decimal to 3 s.f., in Chromium; every Phase 1 working's counts and fraction; every wrong answer's Why card and its named slip against an independent classification; every item fitted at 320x568, 375x667, 390x844, 1366x768 and 1280x720 in normal and Aa; every Phase 2 fade, stored per item, judged against the condition, both drawings, with and without reduced motion; the first-try hint; every worked answer typeset; every unfaded diagram label and the start and results screens' text at 4.5:1 contrast) | | 3
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
  - the phase 2 explanation states the key's fraction;
  - the phase 1 explanation (contract GIVEN-THAT-FIT-WHY, 22 Nov 2026) states the key's own fraction, N/D of SPEC's
    quantities, and every number in it is one of those quantities, their sums or parts, or a number its question
    states (the item's labels taken out first);
  - the Why card's slip families, classified here from SPEC (families(), named()): Phase 1, the complement, one part
    where a total was needed or the reverse, a conditional ratio; Phase 2, the count over everyone, the condition
    reversed, the chance of the condition itself. A sentence only when exactly one family fits; a tie, for a written
    fraction, keeps the family whose own counts are the two written.
In Chromium (390x844), through the game's own functions: every multiple-choice option clicked (the key right,
the others wrong); every free-entry question says "as a fraction, or as a decimal to 3 significant figures"; its
key typed as a decimal is right, and as the fraction in lowest terms and unreduced (so the game's exact key,
exactOf(), is checked against the diagram); each other ratio from the diagram, typed as a decimal and as a
fraction, is wrong; the exact value typed unrounded is not marked ("format"); on a 3/7 item, 0.43 is wrong.
After every wrong answer that ends a phase (each wrong option, in Phase 2 as the last of two picks; every wrong ratio
typed, as a fraction and as a decimal) the Why card shows, its working is the stored explanation and its slip
sentence is exactly this file's; after a right answer, or a first wrong try in Phase 2, it does not.
The fit sweep (FIT_JS, fit_faults()): every item, both phases, at 320x568, 375x667, 390x844, 1366x768 and 1280x720,
normal and Aa: the last option (or the answer box and Submit) above the fold, or in Aa at 320x568 the first; options
two to a row on one line, 44px tall; no sideways scroll; the diagram whole (nothing scrolling in its box or past an
edge) and no count or label under MIN_PX; after each wrong answer the card between the feedback and Next, and on a
laptop Next above the fold. Reported, not failed: Next below the fold on a phone, and the PARKED items.
A self-test plants the audit's faults back into a copy of the page (r-001's Venn; F4's 30/90; r-002's 0.005
rule; r-004's decimals only), and GIVEN-THAT-FIT-WHY's three (a Phase 1 working with a wrong count; a slip named for
a value it does not give; the diagram box's old spacing at 320x568); each must FAIL naming its item.
The fade (contracts GIVEN-THAT-VENN-FADE and GIVEN-THAT-POLISH, 22 Nov 2026; FADE_JS, fade_faults()): every item stores
its Phase 2 fade (phase2.greyOut; "none" for a Bayes tree, whose condition is an outcome on every branch, so nothing
fades by design), and inferGreyOut is gone. Every item enters Phase 2 at 390x844 and 1366x768 (so the narrow and the
wide drawing of each Venn, table and tree), with and without reduced motion, and once the fade has finished: every
element marked "greyed" has a computed opacity of at most 0.3, and a 0.6s opacity transition (none with reduced
motion); every count, totals included, is faded exactly when it is outside the condition, judged against SPEC's
Phase 2 denominator (a Venn's set, a table's column or row, a tree's branch), never against the page's greyOut. The
reduced sample space is the condition's group and its own total: the other groups, the totals across them (a column
condition's Total column, a row condition's Total row), the grand total, a Venn's "Total" and a tree's root fade. Every
table cell's count must be the one SPEC's quantities give for its row and column. A Bayes tree fades nothing.
GIVEN-THAT-POLISH also: after a first wrong pick in Phase 2 the feedback is the slip's sentence (or "Not quite.") then
"One more try, for 1 point."; a conditional slip's sentence first says what was computed, in the item's own labels
("That's Poor among Year 9 only, P(Poor | Year 9). ..."), only where one group is pinned down; every worked answer
(the Why card's working and the Worked Answer panel) shows the stored text exactly, read back from its KaTeX, with
no a/b left as text. Plants: the Venn's fade rule removed; gcse_03's greyOut fading the condition's own column;
core_01 stored "none"; inferGreyOut restored with core_09's stored greyOut removed.
The contrast (contract GIVEN-THAT-SET-LABELS, 22 Nov 2026, Amendments 1 and 2; CONTRAST_JS, contrast_faults()): every
item's diagram in Phase 1 and Phase 2 (both drawings: 390x844 and 1366x768), the start screen before and after a level
is picked, and the results screen, normal and Aa. Every text element (an SVG text's fill, otherwise its colour, with
its own and its ancestors' opacity) has a WCAG contrast of at least 4.5:1 against what is painted beneath it: an SVG
shape in its drawing whose fill holds the text's centre, then each ancestor's background, layered until opaque. Faded
text (greyed, or inside a greyed element) and disabled controls are exempt. Plants: the set names' fill removed (must
be caught on every Venn), --muted back to #7a7f90 (4.22:1), Start Game's white text on the amber.

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


# Comparisons a worked answer got wrong (SWEEP-1, given-that-s1-001, s1-002): never again.
EXPLAIN_FORBIDS = {
    'alevel_10': [(r'Nearly half the flagged scripts are false positives', '47 of 92 flagged are false positives, over half')],
    'alevel_07': [(r'triples the risk', 'against on-time days (10/200) it is six times; three times only the overall rate')],
}


# ---------------------------------------------------------------------------------------------------------------
# The Why card's slips (contract GIVEN-THAT-FIT-WHY, 22 Nov 2026), classified here independently of the page's own
# slipFamilies(): from SPEC's quantities, each phase's families and their sentences, filled from the item's labels and
# counts. The page must name exactly the sentence this gives for every option (GCSE) and every wrong ratio typed.

def fmt(v):
    """The page's fmtCell for a count or probability: a whole number plainly, otherwise 2 d.p."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return str((D(v.numerator) / D(v.denominator)).quantize(D('0.01'), rounding=ROUND_HALF_UP))

def structure(d, num):
    """{name: (value, kind, parts, within)}: kind 'one' for a single cell, region or leaf, 'group' for a total."""
    S = {}
    if d['type'] == 'table':
        for i, r in enumerate(d['rows']):
            S['row[%s]' % r] = [num(d['rowTotals'][i]), 'group', [], []]
        for j, c in enumerate(d['cols']):
            S['col[%s]' % c] = [num(d['colTotals'][j]), 'group', [], []]
        for i, r in enumerate(d['rows']):
            for j, c in enumerate(d['cols']):
                k = 'cell[%s,%s]' % (r, c)
                S[k] = [num(d['values'][i][j]), 'one', [], ['row[%s]' % r, 'col[%s]' % c]]
                S['row[%s]' % r][2].append(k)
                S['col[%s]' % c][2].append(k)
        tot = 'grand'
        S[tot] = [num(d['grandTotal']), 'group', [], []]
    elif d['type'] == 'venn':
        oa, ob, ab, nb = (num(d[k]) for k in ('onlyA', 'onlyB', 'intersection', 'neither'))
        S.update({'onlyA': [oa, 'one', [], ['A']], 'onlyB': [ob, 'one', [], ['B']], 'AB': [ab, 'one', [], ['A', 'B']],
                  'neither': [nb, 'one', [], []], 'A': [oa + ab, 'group', ['onlyA', 'AB'], []],
                  'B': [ob + ab, 'group', ['onlyB', 'AB'], []], 'AorB': [oa + ob + ab, 'group', ['onlyA', 'AB', 'onlyB'], []]})
        tot = 'total'
        S[tot] = [num(d['total']), 'group', [], []]
    else:
        labs = {}
        for br in d['branches']:
            S['b[%s]' % br['label']] = [num(br['value']), 'group', [], []]
            for ch in br['children']:
                k = 'l[%s>%s]' % (br['label'], ch['label'])
                S[k] = [num(ch['value']), 'one', [], ['b[%s]' % br['label']]]
                S['b[%s]' % br['label']][2].append(k)
                labs.setdefault(ch['label'], []).append(k)
        for lab, ks in labs.items():
            S['L[%s]' % lab] = [sum((S[k][0] for k in ks), F(0)), 'group', list(ks), []]
            if len(ks) > 1:
                for k in ks:
                    S[k][3].append('L[%s]' % lab)
        tot = 'total'
        S[tot] = [num(d['total']), 'group', [], []]
    return S, tot

def among(q, x, m):
    """What a conditional slip computed, named from the item's own labels: a single x over a group m it belongs to is
    P(x's other label | m). '' where a label is a bare Yes or No (it names no group without its header); a branch's
    "(60%)" is left off."""
    d = q['data']
    ab = None
    if d['type'] == 'table':
        for r in d['rows']:
            for c in d['cols']:
                if x == 'cell[%s,%s]' % (r, c):
                    ab = (c, r) if m == 'row[%s]' % r else (r, c) if m == 'col[%s]' % c else None
    elif d['type'] == 'venn':
        A, B = d['setA']['label'], d['setB']['label']
        ab = {('AB', 'A'): (B, A), ('AB', 'B'): (A, B), ('onlyA', 'A'): ('not ' + B, A), ('onlyB', 'B'): ('not ' + A, B)}.get((x, m))
    else:
        for br in d['branches']:
            for ch in br['children']:
                if x == 'l[%s>%s]' % (br['label'], ch['label']):
                    ab = (ch['label'], br['label']) if m == 'b[%s]' % br['label'] else \
                         (br['label'], ch['label']) if m == 'L[%s]' % ch['label'] else None
    if not ab or any(s in ('Yes', 'No') for s in ab):
        return ''
    a, b = (re.sub(r'\s*\([^()]*%\)$', '', s) for s in ab)
    return "That's %s among %s only, P(%s | %s). " % (a, b, a, b)


def families(q, ph, spec, num):
    """[(family, value, sentence)] for one phase: the slips a wrong value can be named as."""
    S, tot = structure(q['data'], num)
    ns, ds = spec[ph]
    N = sum((S[n][0] for n in ns), F(0)); Dn = sum((S[n][0] for n in ds), F(0)); T = S[tot][0]
    key = N / Dn
    out = []
    def add(fam, a, b, line, pre=''):
        if a / b != key and a / b != 1:
            out.append((fam, a / b, (a, b), line, pre))
    if ph == 'p1':
        add('comp', Dn - N, Dn, "That's the chance it doesn't happen.")
        if ds != [tot]:
            return out
        if len(ns) == 1 and S[ns[0]][1] == 'one':
            for m in S[ns[0]][3]:
                add('part', S[m][0], T, "That's the whole group of %s: count only the %s in both." % (fmt(S[m][0]), fmt(N)))
        else:
            for n in ns:
                for c in ([n] if S[n][1] == 'one' else S[n][2]):
                    add('part', S[c][0], T, "That's only part of it: you need the total, %s, not just %s." % (fmt(N), fmt(S[c][0])))
        line = ("No condition here: use the whole table, which adds to 1." if T == 1
                else "No condition here: divide by everyone, %s." % fmt(T))
        for x, (v, kind, parts, within) in S.items():
            if kind == 'one':
                for m in within:
                    add('cond', v, S[m][0], line, among(q, x, m))
    else:
        if not (len(ns) == 1 and S[ns[0]][1] == 'one'):
            return out
        c = q['phase2']['condition']
        add('whole', N, T, 'Given that %s, only those %s count: divide by %s, not %s.' % (c, fmt(Dn), fmt(Dn), fmt(T)))
        for m in S[ns[0]][3]:
            if ds != [m]:
                add('reversed', N, S[m][0], "That's the other way round: we know %s, so divide by %s." % (c, fmt(Dn)),
                    among(q, ns[0], m))
        add('condition', Dn, T, "That's the chance that %s (%s out of %s); the question asks for the %s among those %s."
            % (c, fmt(Dn), fmt(T), fmt(N), fmt(Dn)))
    return out

def dp3(v):
    return 3 if not v > 0 or v >= F(1, 10) else 4 if v >= F(1, 100) else 5

def same(typed, places, v):
    """typed (a Fraction) names v: equal, or v rounded half up to the places typed, with at least dp3(v) places."""
    if typed == v:
        return True
    if places is None or places < dp3(v):
        return False
    r = (D(v.numerator) / D(v.denominator)).quantize(D(1).scaleb(-places), rounding=ROUND_HALF_UP)
    return F(str(r)) == typed

def hits_of(fams, typed, places=None, written=None):
    """The families a wrong value fits; a tie between families, for a written fraction a/b, keeps those whose own
    two counts are a and b."""
    hits = [(f, ab, line, pre) for f, v, ab, line, pre in fams if same(typed, places, v)]
    if len({h[0] for h in hits}) > 1 and written:
        hits = [h for h in hits if h[1] == written]
    return hits

def classify(fams, typed, places=None, written=None):
    """The sentence for a wrong value, or '' (no family, or more than one)."""
    return named(fams, typed, places, written)[1]


def named(fams, typed, places=None, written=None):
    """(family, sentence) for a wrong value, or ('', ''): exactly one family must fit, with one sentence. What was
    computed comes first only where it is one group: one prefix, or one once a written fraction's counts are matched."""
    hits = hits_of(fams, typed, places, written)
    if len({h[0] for h in hits}) == 1 and len({h[2] for h in hits}) == 1:
        pres = {h[3] for h in hits}
        if len(pres) > 1 and written:
            pres = {h[3] for h in hits if h[1] == written}
        return hits[0][0], (next(iter(pres)) if len(pres) == 1 else '') + hits[0][2]
    return '', ''


def explain_faults(q, sp_, qs):
    """[fault] for phase1.explanation: it must state the key's own fraction (N/D of SPEC's quantities; a probability
    table, whose total is 1, ends on N), and every number in it must be one of SPEC's quantities for the phase, their
    sums or their parts, or a number the question itself states (once the item's own labels are taken out)."""
    ex = q['phase1'].get('explanation')
    if not isinstance(ex, str) or not ex.strip():
        return ['has no phase1.explanation']
    S, tot = structure(q['data'], num)
    ns, ds = sp_['p1']
    N = sum((S[n][0] for n in ns), F(0)); Dn = sum((S[n][0] for n in ds), F(0))
    allowed = {N, Dn}
    for n in ns + ds:
        allowed.add(S[n][0])
        allowed.update(S[c][0] for c in S[n][2])
    d = q['data']
    labels = [d.get('title', ''), d.get('rowHeader', ''), d.get('colHeader', '')] + d.get('rows', []) + d.get('cols', [])
    if d['type'] == 'venn':
        labels += [d['setA']['label'], d['setB']['label']]
    if d['type'] == 'tree':
        labels += [b['label'] for b in d['branches']] + [c['label'] for b in d['branches'] for c in b['children']]
    text = ex
    for lab in sorted((x for x in labels if x), key=len, reverse=True):
        text = text.replace(lab, ' ')
    nums = lambda t: [F(x.replace(',', '')) for x in re.findall(r'\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?', t)]
    asked = set(nums(q['phase1']['question']))
    bad = []
    stray = [x for x in nums(text) if x not in allowed and x not in asked]
    if stray:
        bad.append('phase1.explanation %r has numbers that are not this question\'s counts: %s'
                   % (ex, ', '.join(str(float(x)) if x.denominator != 1 else str(x) for x in stray)))
    fr = [(F(a.replace(',', '')), F(b.replace(',', ''))) for a, b in re.findall(r'(\d[\d,]*(?:\.\d+)?)/(\d[\d,]*(?:\.\d+)?)', ex)]
    if Dn == 1:
        tail = nums(ex.rsplit('=', 1)[-1])
        if not tail or tail[-1] != N:
            bad.append('phase1.explanation %r does not end on the key %s' % (ex, fmt(N)))
    elif (N, Dn) not in fr:
        bad.append('phase1.explanation %r does not state the key\'s fraction %s/%s' % (ex, fmt(N), fmt(Dn)))
    return bad


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
            # s1-002 (R3): the 20,000 are office-building days, not alarm events (17,912 of them had no alarm)
            if q['id'] == 'core_12' and (d.get('total') != 20000 or 'alarm events' in d.get('title', '') or 'office-building days' not in d.get('title', '')):
                fails.append('core_12: the tree\'s %d are office-building days; its title %r must say so, not "alarm events" (given-that-s1-002)'
                             % (d.get('total', 0), d.get('title')))
            g = q['phase2'].get('greyOut')
            if not g:
                fails.append('%s p2: no stored greyOut (every item stores its Phase 2 fade; "none" for a Bayes tree)' % q['id'])
            elif fade_group(q) is None and g != 'none':
                fails.append('%s p2: a Bayes tree (SPEC\'s condition %s) must store greyOut "none", not %r'
                             % (q['id'], sp_['p2'][1], g))
            elif fade_group(q) is not None and g == 'none':
                fails.append('%s p2: stored greyOut "none", but SPEC\'s condition %s is a group the diagram can fade'
                             % (q['id'], sp_['p2'][1]))
            qs = quantities(d)
            for fault in explain_faults(q, sp_, qs):
                fails.append('%s p1: %s' % (q['id'], fault))
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
                for pat, why in EXPLAIN_FORBIDS.get(pd.get('id') or q.get('id'), []):
                    if re.search(pat, pd.get('explanation', '')):
                        fails.append('%s: the explanation says %r (%s)' % (w, pat, why))
                if ph == 'p2':
                    fr = re.findall(r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)', pd.get('explanation', ''))
                    if fr and not any(F(a) / F(b) == target for a, b in fr):
                        fails.append('%s: the explanation states no fraction equal to the key: %r' % (w, pd['explanation']))
                fams = families(q, ph, sp_, num)
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
                    mc = {}
                    for o, v in zip(opts[1:], vals[1:]):
                        m = re.match(r'\\tfrac\{([\d.]+)\}\{([\d.]+)\}$', o.strip())
                        fam, mc[o] = named(fams, v, None, (F(m.group(1)), F(m.group(2))) if m else None) if v is not None else ('', '')
                        if ph == 'p2':
                            HINT_FAMILY[(q['id'], o)] = fam
                        TALLY[('GCSE options', ph, fam or '(none)')] = TALLY.get(('GCSE options', ph, fam or '(none)'), 0) + 1
                        if ' only, P(' in mc[o]:
                            COMPUTED.append('%s %s %s' % (q['id'], ph, o))
                        if not fam:
                            UNNAMED.append('%s %s %s' % (q['id'], ph, o))
                    MC_SLIPS[(q['id'], ph)] = mc
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
                # What the Why card must say for each wrong ratio typed: as a fraction in lowest terms (so a tie between
                # families is broken only where these two numbers are one family's counts), and as the decimal at DP.
                expect = {}
                for r in wrong_fracs:
                    fam, expect['%d/%d' % (r.numerator, r.denominator)] = named(fams, r, None, (F(r.numerator), F(r.denominator)))
                    if ' only, P(' in expect['%d/%d' % (r.numerator, r.denominator)]:
                        COMPUTED.append('%s %s %d/%d' % (q['id'], ph, r.numerator, r.denominator))
                    TALLY[('typed ratios', ph, fam or '(none)')] = TALLY.get(('typed ratios', ph, fam or '(none)'), 0) + 1
                for o in others:
                    expect[str(o)] = classify(fams, F(str(o)), max(-o.as_tuple().exponent, 0))
                free[(lv, q['id'], ph)] = {'key': str(half_up(target, DP)), 'dp': DP, 'want4': want4,
                                           'exact4': format(exact4, 'f'), 'others': [str(o) for o in others],
                                           'fracs': ['%d/%d' % (target.numerator, target.denominator),
                                                     '%d/%d' % (3 * target.numerator, 3 * target.denominator)],
                                           'wrong_fracs': ['%d/%d' % (r.numerator, r.denominator) for r in wrong_fracs],
                                           'is37': target == F(3, 7), 'expect': expect}
    if not any(f['is37'] for f in free.values()):
        fails.append('bank: no free-entry item is 3/7 (the 3/7, 0.429, 0.43 check has nothing to run on)')
    return free


MC_SLIPS = {}   # (id, phase) -> {wrong option: the sentence the Why card must show, or ''}; filled by check_bank
TALLY = {}      # (where, phase, family) -> how many wrong values the card names so: the PR's per-family counts
UNNAMED = []    # the GCSE options no slip sentence names (no family fits, or two still do)
COMPUTED = []   # the wrong values whose sentence now names what was computed ("That's X among Y only, P(X | Y).")
# The contract's own examples (GIVEN-THAT-FIT-WHY, SUCCESS CONDITION), checked word for word.
EXAMPLE_WORK = {('gcse_01', 'p1'): '60 of the 100 students passed maths. P = 60/100.'}
EXAMPLE_SLIP = {('gcse_01', 'p2', '\\tfrac{30}{100}'): 'divide by 40, not 100',
                ('gcse_25', 'p1', '\\tfrac{50}{90}'): "That's Poor among Year 9 only, P(Poor | Year 9). No condition here: divide by everyone, 250."}
EXAMPLE_HINT = {('gcse_01', '\\tfrac{30}{100}'): 'Given that the student took the revision class, only those 40 count: '
                                                   'divide by 40, not 100. One more try, for 1 point.'}

FIT_SIZES = [(320, 568), (375, 667), (390, 844), (1366, 768), (1280, 720)]
# Parked for Jon's ruling (contract GIVEN-THAT-FIT-WHY, STOP IF: an item that cannot fit a required size; the standing
# STOP rules of 27 Oct 2026: park it with its measurements and carry on). Each entry is reported, never failed; an entry
# that now fits fails as stale, so the PR that fixes it takes it off. Measured 22 Nov 2026 in Chromium, real fonts.
PARKED = {
    ('core_10', 'p2', '320x568 Aa'): 'the answer box starts at 551, 23px below the 528 fold: the indented tree\'s labels '
                                     'wrap in OpenDyslexic, under a three-line banner and a three-line question',
    ('l4_07', 'p2', '320x568 Aa'): 'the answer box starts at 558, 30px below the 528 fold: three branches (ten rows of '
                                   'tree) under a two-line title, a three-line banner and the question',
}
MIN_PX = 11     # the smallest any count or label in a diagram may be drawn, in CSS pixels

FIT_JS = r"""(args) => {
  window.setTimeout = () => 0;
  const G = window.__gt, out = [];
  document.body.classList.toggle('accessible', !!args.aa);
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false; const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden'; };
  const top = el => el.getBoundingClientRect().top + scrollY, bot = el => el.getBoundingClientRect().bottom + scrollY;
  const fold = () => { const f = document.querySelector('.site-footer');
    return innerHeight - (f && getComputedStyle(f).position === 'fixed' && vis(f) ? f.getBoundingClientRect().height : 0); };
  const side = () => document.documentElement.scrollWidth > innerWidth;
  const open = (lv, q, ph) => { scrollTo(0, 0); G.set(lv, q); G.showQuestion(); if (ph === 'p2') G.toPhase2(q); };
  const pick = o => [...document.querySelectorAll('#answerArea .mcq-btn')].find(b => b.dataset.latex === o);
  // The diagram as drawn: nothing scrolling inside its box or running past its edge, no SVG text past its drawing's
  // edge, and the smallest text drawn (an SVG's text at its font size times the drawing's scale).
  function diagram() {
    const dc = document.getElementById('dataContainer'), dv = document.getElementById('dataVis'), bad = [];
    if (dc.scrollWidth > dc.clientWidth + 1) bad.push('the diagram scrolls inside its box (' + dc.scrollWidth + ' > ' + dc.clientWidth + ')');
    const box = dc.getBoundingClientRect();
    let px = 99, what = '';
    const small = (p, t) => { if (p < px) { px = p; what = t; } };
    dv.querySelectorAll('th, td, .tree-lab, .tree-count, .tree-pre').forEach(el => {
      if (!vis(el)) return;
      const r = el.getBoundingClientRect();
      if (r.right > box.right + 1 || r.left < box.left - 1) bad.push('"' + el.textContent.trim() + '" runs past the diagram box');
      small(parseFloat(getComputedStyle(el).fontSize), el.textContent.trim());
    });
    dv.querySelectorAll('svg').forEach(svg => {
      if (!vis(svg)) return;
      const vb = svg.viewBox.baseVal, sc = svg.getBoundingClientRect().width / vb.width;
      svg.querySelectorAll('text').forEach(t => {
        small(parseFloat(getComputedStyle(t).fontSize) * sc, t.textContent);
        const b = t.getBBox();
        if (b.x < vb.x - 0.5 || b.y < vb.y - 0.5 || b.x + b.width > vb.x + vb.width + 0.5 || b.y + b.height > vb.y + vb.height + 0.5)
          bad.push('"' + t.textContent + '" is cut off at its drawing\'s edge');
      });
    });
    return { bad: bad, px: Math.round(px * 10) / 10, what: what };
  }
  for (const lv of Object.keys(G.Q)) G.Q[lv].forEach((q) => {
    for (const ph of ['p1', 'p2']) {
      const pd = ph === 'p1' ? q.phase1 : q.phase2, mc = lv === 'gcse' && !!pd.options;
      open(lv, q, ph);
      const btns = [...document.querySelectorAll('#answerArea .mcq-btn')];
      const els = mc ? btns : [document.getElementById('freeInput'), document.querySelector('#answerArea .submit-btn')];
      const row = { id: q.id, ph: ph, top: Math.round(Math.min(...els.map(top))), bottom: Math.round(Math.max(...els.map(bot))),
                    fold: Math.round(fold()), side: side(), dia: diagram(), wrap: [], wrong: [] };
      // Two to a row only where every option fits its half on one line, 44px tall at least (ruling R3).
      btns.forEach(b => { if (b.scrollWidth > b.clientWidth + 1 || b.getBoundingClientRect().height < 44 - 0.5) row.wrap.push(b.dataset.latex); });
      for (const w of (args.wrongs[lv + '|' + q.id + '|' + ph] || [])) {
        open(lv, q, ph);
        if (mc) {
          if (ph === 'p2') pick(pd.options.slice(1).find(o => o !== w)).click();
          pick(w).click();
        } else {
          document.getElementById('freeInput').value = w;
          document.querySelector('#answerArea .submit-btn').click();
        }
        const nx = ph === 'p1' ? document.querySelector('#nextMount .maffs-next') : document.getElementById('nextBtn');
        const card = [...document.querySelectorAll('#whyRow > .maffs-ref')].find(vis), fb = document.getElementById('feedback');
        row.wrong.push({ w: w, next: vis(nx) ? Math.round(bot(nx)) : null, nextTop: vis(nx) ? Math.round(top(nx)) : null,
                         card: card ? { top: Math.round(top(card)), bottom: Math.round(bot(card)), open: card.open } : null,
                         fb: vis(fb) ? Math.round(bot(fb)) : null, fold: Math.round(fold()), side: side() });
      }
      out.push(row);
    }
  });
  return out;
}"""


FADE_SIZES = [(390, 844), (1366, 768)]     # the narrow drawings, then the wide ones

# Every item into Phase 2, its style flushed first so the fade runs as a student sees it; each fade's transition
# read while running, then finished; then every greyed element and every count (totals included) read as drawn
# (opacity through its ancestors up to the diagram), with the row, column, region or branch it is drawn under.
FADE_JS = r"""() => {
  const G = window.__gt, out = [], dv = document.getElementById('dataVis');
  const shown = el => el.getClientRects().length > 0;
  const eff = el => { let o = 1; for (let n = el; n && n !== dv; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity); return o; };
  const at = (el, a) => { const g = el.closest('[' + a + ']'); return g ? g.getAttribute(a) : null; };
  const key = el => ({ region: at(el, 'data-region'), row: el.getAttribute('data-row'), col: el.getAttribute('data-col'),
                       branch: at(el, 'data-branch') });
  const where = el => { const s = el.closest('svg,table,.tree-list'); return s ? (s.getAttribute('class') || s.tagName) : '?'; };
  for (const lv of Object.keys(G.Q)) for (const q of G.Q[lv]) {
    G.set(lv, q); G.showQuestion();
    dv.querySelectorAll('*').forEach(el => getComputedStyle(el).opacity);
    void dv.offsetHeight;
    G.toPhase2(q);
    const greyed = [...dv.querySelectorAll('.greyed')];
    const anims = document.getAnimations().filter(a => a.transitionProperty === 'opacity')
      .map(a => ({ el: a.effect.target, ms: a.effect.getTiming().duration }));
    document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} });
    const g = greyed.map(el => Object.assign(key(el), { tag: el.tagName.toLowerCase() + '.' + [...el.classList].join('.'),
      where: where(el), op: parseFloat(getComputedStyle(el).opacity), shown: shown(el),
      ms: (anims.find(a => a.el === el) || {}).ms || 0 }));
    const counts = [...dv.querySelectorAll('.venn-label, [data-region="total"], td, .tree-node-text, .tree-count')].map(el =>
      Object.assign(key(el), { text: el.textContent.trim(), where: where(el), op: eff(el) }));
    out.push({ lv: lv, id: q.id, type: q.data.type, greyed: g, counts: counts });
  }
  return out;
}"""


def fade_group(q):
    """The condition's own group from SPEC's Phase 2 denominator: (kind, name), or None for a Bayes tree (an outcome on
    every branch: no set of branches is the condition)."""
    den = SPEC[q['id']]['p2'][1]
    if len(den) != 1:
        return None
    d = den[0]
    if q['data']['type'] == 'venn' and d in ('A', 'B'):
        return 'venn', d
    m = re.fullmatch(r'(col|row|b)\[(.*)\]', d)
    if m and (q['data']['type'], m.group(1)) in (('table', 'col'), ('table', 'row'), ('tree', 'b')):
        return m.group(1), m.group(2)
    return None


def inside(group, c):
    """Is this count inside the condition's reduced sample space (its group, and the group's own total)?"""
    kind, name = group
    if kind == 'venn':
        return c['region'] in ({'onlyA', 'intersection'} if name == 'A' else {'onlyB', 'intersection'})
    if kind == 'col':
        return c['col'] == name
    if kind == 'row':
        return c['row'] == name
    return c['branch'] == name


def cell_count(d, row, col):
    """The count SPEC's quantities give for a table cell drawn under (row, col), "Total" for a total."""
    S, tot = structure(d, num)
    if row == 'Total' and col == 'Total':
        return S[tot][0]
    if row == 'Total':
        return S['col[%s]' % col][0]
    if col == 'Total':
        return S['row[%s]' % row][0]
    return S['cell[%s,%s]' % (row, col)][0]


def fade_faults(rows, bank, w, h, rm):
    """[fault] for every fade that is not the condition's."""
    fails, at = [], ' at %dx%d%s' % (w, h, ' (reduced motion)' if rm else '')
    byid = {q['id']: q for lv in bank for q in bank[lv]}
    for r in rows:
        lab = '%s p2%s' % (r['id'], at)
        q = byid[r['id']]
        name = lambda c: c['region'] or ('%s/%s' % (c['row'], c['col']) if c['row'] or c['col'] else c['branch'])
        for el in r['greyed']:
            if el['op'] > 0.3:
                fails.append('%s: %s "%s" (%s) is marked greyed but drawn at opacity %.2f (no rule fades it)'
                             % (lab, el['tag'], name(el), el['where'], el['op']))
            if el['shown'] and not rm and abs(el['ms'] - 600) > 1:
                fails.append('%s: %s "%s" fades in %dms, not the 0.6s the others use' % (lab, el['tag'], name(el), el['ms']))
            if rm and el['ms']:
                fails.append('%s: %s "%s" still fades over %dms with reduced motion on' % (lab, el['tag'], name(el), el['ms']))
        if r['type'] == 'table':
            for c in r['counts']:
                try:
                    want = fmt(cell_count(q['data'], c['row'], c['col']))
                except KeyError:
                    fails.append('%s: a cell drawn under row %r, column %r that SPEC\'s table does not have' % (lab, c['row'], c['col']))
                    continue
                if c['text'] != want:
                    fails.append('%s: the cell under %s/%s (%s) shows %s, SPEC\'s table has %s'
                                 % (lab, c['row'], c['col'], c['where'], c['text'], want))
        group = fade_group(q)
        if group is None:
            if r['greyed'] or any(c['op'] < 0.95 for c in r['counts']):
                fails.append('%s: a Bayes tree (every branch counts) but something fades' % lab)
            continue
        if not r['greyed']:
            fails.append('%s: nothing fades in Phase 2 (SPEC\'s condition %s)' % (lab, group[1]))
            continue
        for c in r['counts']:
            if inside(group, c) and c['op'] < 0.95:
                fails.append('%s: the count %s (%s, %s) is inside the condition (%s) but faded to %.2f'
                             % (lab, c['text'], name(c), c['where'], group[1], c['op']))
            if not inside(group, c) and c['op'] > 0.3:
                fails.append('%s: the count %s (%s, %s) is outside the condition (%s) but stays at %.2f'
                             % (lab, c['text'], name(c), c['where'], group[1], c['op']))
    return fails


def fade(fails, html, bank, sizes=None, motions=(False, True)):
    """The fade sweep: every item into Phase 2 at each FADE_SIZES size, with and without reduced motion."""
    from playwright.sync_api import sync_playwright
    hooked = hook(html)
    if hooked is None:
        fails.append('page: cannot find the end of the game script to expose its functions to the sweep')
        return
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for w, h in sizes or FADE_SIZES:
                for rm in motions:
                    ctx = browser.new_context(viewport={'width': w, 'height': h},
                                              reduced_motion='reduce' if rm else 'no-preference')
                    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
                    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                    bc.offline(ctx, base)
                    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                        status=200, content_type='text/html; charset=utf-8', body=hooked))
                    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
                    page = ctx.new_page()
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.goto(base + '/games/%s/?cb=fade' % SLUG, wait_until='load', timeout=20000)
                    page.wait_for_function('window.__gt && typeof katex !== "undefined"', timeout=15000)
                    rows = page.evaluate(FADE_JS)
                    fails.extend(fade_faults(rows, bank, w, h, rm))
                    if errors:
                        fails.append('page errors at %dx%d: %s' % (w, h, '; '.join(errors[:3])))
                    ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()



CONTRAST_SIZES = [(390, 844), (1366, 768)]     # the narrow drawings, then the wide ones
MIN_CONTRAST = 4.5                             # WCAG 2.2 AA (1.4.3), applied to every size of text

# Every text element in a root, read as drawn: its colour (an SVG text's fill, otherwise its colour) with the opacity
# of it and its ancestors, over the nearest painted background beneath it: any SVG shape in its drawing whose fill
# contains the text's centre (painted before it), then each ancestor's background colour, layered until one is
# opaque. Faded text (a "greyed" element or inside one) and disabled controls are exempt (WCAG 1.4.3's inactive
# components); the caller skips nothing else. Returns [label, text, fg rgb, bg rgb] with both colours composited.
CONTRAST_JS = r"""(rootSel) => {
  const out = [], roots = [...document.querySelectorAll(rootSel)];
  const rgba = s => { const m = (s || '').match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const v = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [v[0], v[1], v[2], v.length > 3 ? v[3] : 1]; };
  const opac = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity); return o; };
  const over = (top, a, bot) => top.map((c, i) => a * c + (1 - a) * bot[i]);
  const own = el => [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim());
  const SHAPES = 'rect,circle,ellipse,path,polygon';
  for (const root of roots) root.querySelectorAll('*').forEach(el => {
    const texts = own(el);
    if (!texts.length || !el.getClientRects().length) return;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') return;
    if (el.closest('.greyed') || el.closest(':disabled')) return;
    const range = document.createRange(); range.selectNodeContents(texts[0]);
    const r = range.getClientRects()[0] || el.getClientRects()[0];
    const x = r.left + r.width / 2, y = r.top + r.height / 2;
    const isSvg = el instanceof SVGElement;
    const fg = rgba(isSvg ? cs.fill : cs.color);
    const label = el.tagName.toLowerCase() + (el.getAttribute('class') ? '.' + el.getAttribute('class').trim().split(/\s+/).join('.') : '')
      + (el.id ? '#' + el.id : '');
    const text = el.textContent.trim().replace(/\s+/g, ' ').slice(0, 40);
    if (!fg) { out.push([label, text, null, null, isSvg ? cs.fill : cs.color]); return; }
    const layers = [];
    const svg = isSvg ? el.ownerSVGElement : null;
    if (svg) {
      const shapes = [...svg.querySelectorAll(SHAPES)].filter(sh =>
        (sh.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) && !el.contains(sh));
      for (const sh of shapes.reverse()) {
        const sc = getComputedStyle(sh), f = rgba(sc.fill);
        if (!f || !sh.getClientRects().length) continue;
        const p = new DOMPoint(x, y).matrixTransform(sh.getScreenCTM().inverse());
        if (!sh.isPointInFill(p)) continue;
        layers.push([f, f[3] * parseFloat(sc.fillOpacity) * opac(sh)]);
      }
    }
    for (let n = isSvg ? svg.parentElement : el; n; n = n.parentElement) {
      const b = rgba(getComputedStyle(n).backgroundColor);
      if (b && b[3] > 0) layers.push([b, b[3] * opac(n)]);
    }
    let i = layers.findIndex(l => l[1] >= 0.999);
    let bg = i < 0 ? [255, 255, 255] : layers[i][0].slice(0, 3);
    for (let j = (i < 0 ? layers.length : i) - 1; j >= 0; j--) bg = over(layers[j][0].slice(0, 3), layers[j][1], bg);
    out.push([label, text, over(fg.slice(0, 3), fg[3] * opac(el), bg), bg]);
  });
  return out;
}"""


def luminance(rgb):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


CONTRAST_TALLY = {}


def contrast_faults(rows, where):
    """[fault] for every text element under MIN_CONTRAST; counts each judged element into CONTRAST_TALLY."""
    fails = []
    for label, text, fg, bg, *raw in rows:
        kind = where.split(' at ')[0].split(' ')[0].rstrip(',')
        CONTRAST_TALLY[kind] = CONTRAST_TALLY.get(kind, 0) + 1
        if fg is None:
            fails.append('%s: %s "%s" has no colour to read (%s)' % (where, label, text, raw[0] if raw else '?'))
            continue
        cr = contrast_ratio(fg, bg)
        if cr < MIN_CONTRAST - 1e-9:
            fails.append('%s: %s "%s" is %.2f:1 (rgb%s on rgb%s), under %.1f:1'
                         % (where, label, text, cr, tuple(round(c) for c in fg), tuple(round(c) for c in bg), MIN_CONTRAST))
    return fails


def contrast(fails, html, sizes=None, modes=(False, True)):
    """The contrast sweep: every item's diagram in Phase 1 and Phase 2 (both drawings), the start screen (before and
    after a level is picked) and the results screen, at each CONTRAST_SIZES size, normal and Aa."""
    from playwright.sync_api import sync_playwright
    hooked = hook(html)
    if hooked is None:
        fails.append('page: cannot find the end of the game script to expose its functions to the sweep')
        return
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for w, h in sizes or CONTRAST_SIZES:
                for aa in modes:
                    at = ' at %dx%d%s' % (w, h, ' Aa' if aa else '')
                    ctx = browser.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce')
                    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
                    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                    bc.offline(ctx, base)
                    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                        status=200, content_type='text/html; charset=utf-8', body=hooked))
                    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
                    page = ctx.new_page()
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.goto(base + '/games/%s/?cb=contrast' % SLUG, wait_until='load', timeout=20000)
                    page.wait_for_function('window.__gt && typeof katex !== "undefined"', timeout=15000)
                    page.evaluate("(aa) => document.body.classList.toggle('accessible', aa)", aa)
                    fails.extend(contrast_faults(page.evaluate(CONTRAST_JS, '#startScreen'), 'start' + at))
                    page.click('#levelSelect .level-btn[data-level="gcse"]')
                    page.evaluate('() => document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} })')
                    fails.extend(contrast_faults(page.evaluate(CONTRAST_JS, '#startScreen'),
                                                 'start, a level picked' + at))
                    ids = page.evaluate("""() => { const G = window.__gt, o = [];
                      for (const lv of Object.keys(G.Q)) G.Q[lv].forEach((q, i) => o.push([lv, i, q.id])); return o; }""")
                    for lv, i, qid in ids:
                        for ph in ('p1', 'p2'):
                            page.evaluate("""([lv, i, ph]) => { const G = window.__gt, q = G.Q[lv][i];
                              G.set(lv, q); G.showQuestion(); if (ph === 'p2') G.toPhase2(q);
                              document.getAnimations().forEach(a => { try { a.finish(); } catch (e) {} }); }""",
                                          [lv, i, ph])
                            fails.extend(contrast_faults(page.evaluate(CONTRAST_JS, '#dataContainer'),
                                                         'diagram %s %s%s' % (qid, ph, at)))
                    page.evaluate('() => window.__gt.results(31)')
                    bc.wait_settled(page)
                    fails.extend(contrast_faults(page.evaluate(CONTRAST_JS, '#resultsScreen'), 'results' + at))
                    if errors:
                        fails.append('page errors%s: %s' % (at, '; '.join(errors[:3])))
                    ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()


HOOK = ('window.__gt={Q:QUESTIONS,set:function(lv,q){currentLevel=lv;sessionQuestions=[q];currentQIndex=0;'
        'phase2Attempt=0;startScreen.classList.remove("active");gameScreen.classList.add("active");'
        'gameHeader.style.display=""},showQuestion:showQuestion,toPhase2:transitionToPhase2,'
        'results:function(sc){totalScore=sc;showResults()}};\n')

SWEEP_JS = r"""(free) => {
  window.setTimeout = () => 0;
  const G = window.__gt, out = [], why = [], hint = [], worked = [];
  const fb = () => { const f = document.getElementById('feedback'); return {
      right: f.classList.contains('correct-fb'), wrong: f.classList.contains('wrong-fb'), text: f.textContent }; };
  const open = (lv, q, ph) => { G.set(lv, q); G.showQuestion(); if (ph === 'p2') G.toPhase2(q); };
  const vis = el => !!el && el.getClientRects().length > 0 && getComputedStyle(el).display !== 'none';
  // A worked answer as drawn: its text with each KaTeX run read back as its TeX source (work), and the words alone,
  // the KaTeX taken out (plain), where no a/b may be left.
  const read = el => {
    const k = el.cloneNode(true), p = el.cloneNode(true);
    k.querySelectorAll('.katex').forEach(x => { const a = x.querySelector('annotation');
      x.replaceWith(document.createTextNode(a ? a.textContent : '?')); });
    p.querySelectorAll('.katex').forEach(x => x.remove());
    return { work: k.textContent, plain: p.textContent };
  };
  const panel = () => { const e = document.querySelector('#explanation p'); return e && vis(e) ? read(e) : null; };
  // The Why card as a student sees it: is a copy showing, its slip sentence, and its working read back.
  const card = () => {
    const c = [...document.querySelectorAll('#whyRow > .maffs-ref')].find(vis);
    if (!c) return { shown: false, slip: '', work: '' };
    const s = c.querySelector('.why-slip'), w = c.querySelector('.why-work');
    let work = '';
    if (w) {
      const k = w.cloneNode(true);
      k.querySelectorAll('.katex').forEach(x => { const a = x.querySelector('annotation');
        x.replaceWith(document.createTextNode(a ? a.textContent : '?')); });
      work = k.textContent;
    }
    return Object.assign({ shown: true, slip: s ? s.textContent : '' }, w ? read(w) : { work: '', plain: '' });
  };
  const pick = o => [...document.querySelectorAll('#answerArea .mcq-btn')].find(b => b.dataset.latex === o);
  for (const lv of Object.keys(G.Q)) G.Q[lv].forEach((q) => {
    for (const ph of ['p1', 'p2']) {
      const pd = ph === 'p1' ? q.phase1 : q.phase2;
      if (lv === 'gcse' && pd.options) {
        for (const opt of pd.options) {
          open(lv, q, ph);
          const btn = pick(opt);
          if (!btn) { out.push([q.id, ph, opt, 'not on screen']); continue; }
          btn.click();
          const r = fb();
          if (r.right !== (opt === pd.options[0])) out.push([q.id, ph, opt, r.right ? 'marked right' : 'marked wrong']);
          if (opt === pd.options[0] && card().shown) out.push([q.id, ph, opt, 'the Why card shows after a right answer']);
          if (ph === 'p1' && opt !== pd.options[0]) why.push([q.id, ph, opt, card()]);
          if (ph === 'p2' && opt !== pd.options[0] && card().shown)
            out.push([q.id, ph, opt, 'the Why card shows after the first wrong try (Phase 2 has two)']);
          if (ph === 'p2' && opt !== pd.options[0]) hint.push([q.id, opt, r.text, r.wrong]);
          if (ph === 'p2' && opt === pd.options[0]) worked.push([q.id, ph, opt, panel()]);
        }
        if (ph === 'p2') for (const opt of pd.options.slice(1)) {
          // Phase 2 ends wrong on the second wrong try: the card names the last pick.
          open(lv, q, ph);
          pick(pd.options.slice(1).find(o => o !== opt)).click();
          pick(opt).click();
          why.push([q.id, ph, opt, card()]);
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
        const c = card();
        if (got !== 'wrong' && c.shown) out.push([q.id, ph, typed, 'the Why card shows after a ' + got + ' answer']);
        if (got === 'wrong' && typed in f.expect) why.push([q.id, ph, typed, c]);
        if (got === 'right' && ph === 'p2') worked.push([q.id, ph, typed, panel()]);
      }
    }
  });
  return { out: out, why: why, hint: hint, worked: worked };
}"""


def hook(html):
    """The page with its private functions exposed to the sweep (served copy only, never written)."""
    m = list(re.finditer(r'\n\}\)\(\);\n</script>\n<script src="\.\./\.\./schools/assets/teacher-invite\.js">', html.replace('\r\n', '\n')))
    if len(m) != 1:
        return None
    h = html.replace('\r\n', '\n')
    return h[:m[0].start()] + '\n' + HOOK + h[m[0].start():]


def tex_text(s):
    r"""A worked answer's KaTeX read back as text: \dfrac{a}{b} -> a/b, \approx -> ≈, \text{w} -> w and so on."""
    out, i = [], 0
    def group(j):
        depth, k = 0, j
        while True:
            depth += {'{': 1, '}': -1}.get(s[k], 0)
            k += 1
            if depth == 0:
                return s[j + 1:k - 1], k
    while i < len(s):
        if s.startswith('\\dfrac', i) or s.startswith('\\tfrac', i):
            a, i = group(i + 6)
            b, i = group(i)
            out.append(tex_text(a) + '/' + tex_text(b))
        elif s.startswith('\\text', i):
            a, i = group(i + 5)
            out.append(a)
        elif s.startswith('{,}', i):
            out.append(','); i += 3
        else:
            m = re.match(r'\\(approx|neq|times|mid|cap|%)', s[i:])
            if m:
                out.append({'approx': '≈', 'neq': '≠', 'times': '×', 'mid': '|', 'cap': '∩', '%': '%'}[m.group(1)])
                i += len(m.group(0))
            else:
                out.append(s[i]); i += 1
    return ''.join(out)


def work_faults(fails, lab, c, stored):
    """A worked answer as drawn: the stored text exactly (spacing aside), and no a/b left in the words."""
    if re.sub(r'\s+', '', tex_text(c['work'])) != re.sub(r'\s+', '', stored):
        fails.append('%s: the worked answer reads %r, not the stored %r' % (lab, tex_text(c['work'])[:90], stored[:90]))
    if re.search(r'\d\s*/\s*\d', c['plain']):
        fails.append('%s: the worked answer shows an ASCII fraction: %r' % (lab, c['plain'][:90]))


def hint_faults(fails, hints):
    """After a first wrong pick in Phase 2: the slip's sentence as a hint (or "Not quite."), then the second try."""
    for id_, opt, text, wrong in hints:
        want = (MC_SLIPS.get((id_, 'p2'), {}).get(opt) or 'Not quite.') + ' One more try, for 1 point.'
        if text.strip() != want:
            fails.append('%s p2 in Chromium: first wrong pick %s: the feedback reads %r, not %r' % (id_, opt, text[:120], want))
        TALLY[('first-try hints', 'p2', named_family(id_, opt))] = TALLY.get(('first-try hints', 'p2', named_family(id_, opt)), 0) + 1


HINT_FAMILY = {}   # (id, wrong option) -> its Phase 2 family, for the hint tally


def named_family(id_, opt):
    return HINT_FAMILY.get((id_, opt)) or '(none: "Not quite.")'


def why_faults(fails, seen, free, ex_text):
    """Every wrong answer's Why card: shown, its working the phase's stored explanation (Phase 2's unchanged), and its
    slip sentence exactly the one this verifier's own classification gives (or none)."""
    named = {}
    for id_, ph, wrong, c in seen:
        if not c['shown']:
            fails.append('%s %s in Chromium: wrong answer %s: no Why card' % (id_, ph, wrong))
            continue
        work = tex_text(c['work'])
        work_faults(fails, '%s %s in Chromium: wrong answer %s: the Why card' % (id_, ph, wrong), c, ex_text[(id_, ph)])
        if (id_, ph) in MC_SLIPS:
            want = MC_SLIPS[(id_, ph)].get(wrong)
        else:
            lv = next(k[0] for k in free if k[1] == id_ and k[2] == ph)
            want = free[(lv, id_, ph)]['expect'].get(wrong)
        if want is None:
            continue
        if (id_, ph, wrong) in EXAMPLE_SLIP and EXAMPLE_SLIP[(id_, ph, wrong)] not in c['slip']:
            fails.append('%s %s in Chromium: wrong answer %s: the card does not name the contract\'s slip %r: %r'
                         % (id_, ph, wrong, EXAMPLE_SLIP[(id_, ph, wrong)], c['slip']))
        if (id_, ph) in EXAMPLE_WORK and re.sub(r'\s+', '', work) != re.sub(r'\s+', '', EXAMPLE_WORK[(id_, ph)]):
            fails.append('%s %s in Chromium: the card shows %r, not the contract\'s %r' % (id_, ph, work, EXAMPLE_WORK[(id_, ph)]))
        if c['slip'] != want:
            fails.append('%s %s in Chromium: wrong answer %s: the Why card names %r; by computation it is %r'
                         % (id_, ph, wrong, c['slip'], want or '(no slip)'))
        named[(id_, ph, wrong)] = c['slip']
    return named


def play(fails, html, free, ex_text):
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
            bc.offline(ctx, base)
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=hooked))
            ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)     # KaTeX from the pinned local copy
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('window.__gt && typeof katex !== "undefined"', timeout=15000)
            if not page.evaluate('() => !!window.MaffsAnswer'):
                fails.append('page (given-that-r-002): free entry is not marked by MaffsAnswer (schools/assets/answer.js not loaded)')
            got = page.evaluate(SWEEP_JS, args)
            for id_, ph, typed, what in got['out']:
                lab = '%s %s' % (id_, ph)
                fails.append('%s%s in Chromium: %s%s' % (lab, ' (%s)' % AUDIT[(id_, ph)] if (id_, ph) in AUDIT else '',
                                                          ('typed %s: ' % typed) if typed else '', what))
            why_faults(fails, got['why'], free, ex_text)
            hint_faults(fails, got['hint'])
            for (id_, opt), want in EXAMPLE_HINT.items():
                if not any(h[0] == id_ and h[1] == opt and h[2].strip() == want for h in got['hint']):
                    fails.append('%s p2 in Chromium: first wrong pick %s does not show the contract\'s %r' % (id_, opt, want))
            for id_, ph, typed, c in got['worked']:
                if c is None:
                    fails.append('%s %s in Chromium: right answer %s: no Worked Answer shown' % (id_, ph, typed))
                else:
                    work_faults(fails, '%s %s in Chromium: right answer %s: the Worked Answer' % (id_, ph, typed), c, ex_text[(id_, ph)])
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()


def fit_wrongs(free, bank):
    """The wrong answers the fit sweep makes, per (level, id, phase): every wrong option (GCSE; in Phase 2 each as
    the last of two picks), or, typed, one wrong ratio for each slip sentence (the card is as tall as its sentence)
    and one that names none."""
    out = {}
    for lv in bank:
        for q in bank[lv]:
            for ph, key in (('p1', 'phase1'), ('p2', 'phase2')):
                pd = q[key]
                if lv == 'gcse' and pd.get('options'):
                    out['%s|%s|%s' % (lv, q['id'], ph)] = pd['options'][1:]
                    continue
                f = free.get((lv, q['id'], ph))
                if not f:
                    continue
                by = {}
                for typed, line in f['expect'].items():
                    if '/' in typed:
                        by.setdefault(line, typed)
                out['%s|%s|%s' % (lv, q['id'], ph)] = list(by.values()) + ([] if '' in by else ['987654'])
    return out


def fit_faults(rows, w, h, aa):
    """Judge one size and mode (canon 7.6.1; ruling R2; contract GIVEN-THAT-FIT-WHY step 2). Gated: the last option
    (or the answer box and Submit) above the fold, except Aa at 320x568 where they must start above it; on a laptop
    Next above the fold after every wrong answer; no sideways scroll; every diagram whole, nothing smaller than MIN_PX;
    options two to a row only on one line; the Why card between the feedback and Next. Reported, not gated: Next below
    the fold on a phone."""
    size = '%dx%d%s' % (w, h, ' Aa' if aa else '')
    laptop = w >= 900
    fails, report = [], []
    gate = [r for r in rows if not (aa and (w, h) == (320, 568))]
    if gate:
        m = min(gate, key=lambda r: r['fold'] - r['bottom'])
        report.append('%s: the tightest asking screen is %s %s, its last control %dpx above the fold'
                      % (size, m['id'], m['ph'], m['fold'] - m['bottom']))
    for r in rows:
        lab = '%s %s at %s' % (r['id'], r['ph'], size)
        if aa and (w, h) == (320, 568):
            parked = PARKED.get((r['id'], r['ph'], size))
            if r['top'] > r['fold']:
                (report if parked else fails).append('%s: the options start at %d, below the fold %d%s'
                                                    % (lab, r['top'], r['fold'], ' (parked: Jon to rule)' if parked else ''))
            elif parked:
                fails.append('%s: parked as not fitting, but the options now start at %d, above the fold %d: take it '
                             'off PARKED' % (lab, r['top'], r['fold']))
        elif r['bottom'] > r['fold']:
            fails.append('%s: the last answer control ends at %d, below the fold %d' % (lab, r['bottom'], r['fold']))
        if r['side']:
            fails.append('%s: the asking screen scrolls sideways' % lab)
        for b in r['dia']['bad']:
            fails.append('%s: %s' % (lab, b))
        if r['dia']['px'] < MIN_PX:
            fails.append('%s: the diagram draws %r at %spx, under %dpx' % (lab, r['dia']['what'], r['dia']['px'], MIN_PX))
        for o in r['wrap']:
            fails.append('%s: option %s does not fit its half of the row on one line, 44px tall' % (lab, o))
        for x in r['wrong']:
            wl = '%s, wrong answer %s' % (lab, x['w'])
            if x['side']:
                fails.append('%s: the feedback screen scrolls sideways' % wl)
            if x['next'] is None or x['card'] is None or x['fb'] is None:
                fails.append('%s: %s' % (wl, 'no Next' if x['next'] is None else 'no Why card' if x['card'] is None else 'no feedback'))
                continue
            # The order (canon 7.6.1): the feedback, then the card, then Next. Collapsed, the card sits beside Next on its
            # line (its top a few pixels below Next's); open, above it. Never below Next.
            if not (x['fb'] <= x['card']['top'] + 1 and x['card']['top'] < x['next']):
                fails.append('%s: the Why card is not between the feedback and Next (feedback ends %d, card %d-%d, Next %d)'
                             % (wl, x['fb'], x['card']['top'], x['card']['bottom'], x['nextTop']))
            if x['next'] > x['fold']:
                (fails if laptop else report).append('%s: Next ends at %d, below the fold %d%s'
                                                     % (wl, x['next'], x['fold'], ' (card open)' if x['card']['open'] else ''))
    return fails, report


def fit(fails, html, free, bank, sizes=None, modes=(False, True)):
    """The fit sweep: every item, both phases, at every size in FIT_SIZES, normal and Aa."""
    from playwright.sync_api import sync_playwright
    hooked = hook(html)
    if hooked is None:
        fails.append('page: cannot find the end of the game script to expose its functions to the sweep')
        return []
    wrongs = fit_wrongs(free, bank)
    reports = []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for w, h in sizes or FIT_SIZES:
                for aa in modes:
                    ctx = browser.new_context(viewport={'width': w, 'height': h})
                    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
                    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
                    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                    bc.offline(ctx, base)
                    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                        status=200, content_type='text/html; charset=utf-8', body=hooked))
                    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
                    page = ctx.new_page()
                    errors = []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.goto(base + '/games/%s/?cb=fit' % SLUG, wait_until='load', timeout=20000)
                    page.wait_for_function('window.__gt && typeof katex !== "undefined"', timeout=15000)
                    # Every face the sweep will draw in (the text faces, Aa's OpenDyslexic, KaTeX's) loaded first, so
                    # the measurements read the real layout: one item of each kind drawn, then settled.
                    page.evaluate("""(aa) => { document.body.classList.toggle('accessible', aa); const G = window.__gt;
                      for (const lv of Object.keys(G.Q)) for (const q of G.Q[lv].slice(0, 6)) { G.set(lv, q); G.showQuestion(); G.toPhase2(q); } }""", aa)
                    bc.wait_settled(page)
                    rows = page.evaluate(FIT_JS, {'aa': aa, 'wrongs': wrongs})
                    f, rep = fit_faults(rows, w, h, aa)
                    fails.extend(f)
                    reports.extend(rep)
                    if errors:
                        fails.append('page errors at %dx%d%s: %s' % (w, h, ' Aa' if aa else '', '; '.join(errors[:3])))
                    ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return reports


def load_bank(html):
    tree, _ = bc.parse_game_source(html)
    if tree is None:
        return None
    for name, init, _ in bc.iife_scoped_declarations(tree):
        if name == 'QUESTIONS':
            return bc.static_bank_value(name, init, tree)
    return None


def run(html, stages=('bank', 'play', 'fit'), fit_sizes=None, fit_modes=(False, True)):
    """The checks, by stage: 'bank' (always), 'play' (every answer marked, every Why card read, at 390x844), 'fade'
    (every Phase 2 fade against SPEC) and 'fit' (the fit sweep). A self-test plant runs only the stage that must catch it."""
    fails = []
    TALLY.clear()
    del UNNAMED[:]
    del COMPUTED[:]
    bank = load_bank(html)
    if bank is None:
        return ['bank: QUESTIONS not found in the page'], 0
    if 'inferGreyOut' in html:
        fails.append('page: inferGreyOut is back: every fade must come from the item\'s stored phase2.greyOut')
    free = check_bank(fails, bank)
    ex_text = {(q['id'], ph): q[key].get('explanation', '') for lv in bank for q in bank[lv]
               for ph, key in (('p1', 'phase1'), ('p2', 'phase2'))}
    if 'play' in stages:
        play(fails, html, free, ex_text)
    if 'fade' in stages:
        fade(fails, html, bank)
    if 'contrast' in stages:
        CONTRAST_TALLY.clear()
        contrast(fails, html, fit_sizes, fit_modes)
    global FIT_REPORT
    FIT_REPORT = fit(fails, html, free, bank, fit_sizes, fit_modes) if 'fit' in stages else []
    return fails, sum(len(v) for v in bank.values())


FIT_REPORT = []


# inferGreyOut as it was on main before GIVEN-THAT-POLISH (873befe), for the plant that restores it.
OLD_INFER = (
    '/* ---------- INFER GREY-OUT for non-GCSE questions ---------- */\n'
    'function inferGreyOut(q){\n'
    '  if(q.phase2.greyOut)return; // already set\n'
    '  const d=q.data;\n'
    '  const cond=q.phase2.condition.toLowerCase();\n'
    "  if(d.type==='table'){\n"
    '    // Try to match condition to a column name using word-boundary-aware matching\n'
    '    const matchedCols=[];\n'
    '    d.cols.forEach(c=>{\n'
    '      const cl=c.toLowerCase();\n'
    '      // Use word boundary regex to avoid "male" matching inside "female"\n'
    "      const re=new RegExp('\\\\b'+cl.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+'\\\\b');\n"
    '      if(re.test(cond))matchedCols.push(c);\n'
    '    });\n'
    '    if(matchedCols.length===1){\n'
    '      const others=d.cols.filter(c=>c!==matchedCols[0]);\n'
    "      q.phase2.greyOut=others.map(c=>'col_'+c).join(',');\n"
    '    } else if(matchedCols.length>1){\n'
    '      // Multiple matches — try exact match (longest match wins)\n'
    '      const sorted=[...matchedCols].sort((a,b)=>b.length-a.length);\n'
    '      const best=sorted[0];\n'
    '      const others=d.cols.filter(c=>c!==best);\n'
    "      q.phase2.greyOut=others.map(c=>'col_'+c).join(',');\n"
    '    }\n'
    "  } else if(d.type==='venn'){\n"
    '    // For Venn, condition typically references set A or set B\n'
    '    const labelA=d.setA.label.toLowerCase();\n'
    '    const labelB=d.setB.label.toLowerCase();\n'
    '    if(cond.includes(labelA)&&!cond.includes(labelB)){\n'
    "      q.phase2.greyOut='onlyB,neither';\n"
    '    } else if(cond.includes(labelB)&&!cond.includes(labelA)){\n'
    "      q.phase2.greyOut='onlyA,neither';\n"
    "    } else if(cond.includes('a ')||cond.includes('a)')||cond==='event a occurs'||cond.includes(' a ')){\n"
    "      q.phase2.greyOut='onlyB,neither';\n"
    "    } else if(cond.includes('b ')||cond.includes('b)')||cond.includes(' b ')){\n"
    "      q.phase2.greyOut='onlyA,neither';\n"
    '    }\n'
    "  } else if(d.type==='tree'){\n"
    '    // For trees, check if the condition matches exactly ONE main branch\n'
    '    const branches=d.branches.filter(b=>b.value>0);\n'
    '    // Use word-boundary matching on the branch label (strip parenthetical percentages)\n'
    '    const matchedBranches=branches.filter(b=>{\n'
    "      const bl=b.label.toLowerCase().split('(')[0].trim();\n"
    '      if(bl.length<2)return false; // skip very short labels\n'
    "      const re=new RegExp('\\\\b'+bl.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&')+'\\\\b');\n"
    '      return re.test(cond);\n'
    '    });\n'
    '    if(matchedBranches.length===1){\n'
    '      // Condition IS this branch — grey others\n'
    '      const others=branches.filter(b=>b!==matchedBranches[0]);\n'
    "      q.phase2.greyOut=others.map(b=>'branch_'+b.label).join(',');\n"
    '    } else {\n'
    '      // Condition might be a leaf outcome (e.g. "tests positive", "defective")\n'
    '      // Find which leaf label matches, then we need to keep all branches that lead to that outcome\n'
    "      // In this case we don't grey branches — all branches are relevant for Bayes' theorem\n"
    '      // No grey-out needed (all branches contribute to the condition)\n'
    '    }\n'
    '  }\n'
    '}\n'
    '\n'
)

PLANTS = [
    ('alevel_18 p2', 'r-001: only-P 20 drawn beside a P total of 60',
     'setB:{label:"P",total:60},onlyA:35,onlyB:15,intersection:45,neither:55',
     'setB:{label:"P",total:60},onlyA:35,onlyB:20,intersection:45,neither:50'),
    ('gcse_14 p2', 'F4: 30/90 beside 60/180',
     '"\\\\tfrac{60}{180}","\\\\tfrac{30}{180}","\\\\tfrac{90}{180}"', '"\\\\tfrac{60}{180}","\\\\tfrac{30}{90}","\\\\tfrac{90}{180}"'),
    ('core_04 p1', "r-002/r-003: marked within 0.005, no precision",
     "result=MaffsAnswer.fractionOrDecimal(raw,ex[0],ex[1],dp);",
     "result=Math.abs(parseFloat(raw)-phaseData.answer)<=0.005?'correct':'wrong';"),
    ('alevel_10 p2', 's1-001: "Nearly half ... false positives"', "Just over half the flagged scripts (47 of 92) are false positives.",
     "Nearly half the flagged scripts are false positives."),
    ('core_12', 's1-002: the title calls 20,000 days alarm events', 'title:"20,000 office-building days (1 year)"',
     'title:"20,000 alarm events in office buildings (1 year)"'),
    ('alevel_01 p1', "r-004: decimals only, the fraction unreadable",
     "result=MaffsAnswer.fractionOrDecimal(raw,ex[0],ex[1],dp);",
     "result=MaffsAnswer.decimal(raw,(ex[0]/ex[1]).toFixed(dp),dp);"),
    # GIVEN-THAT-FIT-WHY's three (contract step 6).
    ('gcse_01 p1', 'Phase 1 working with a wrong count (50 for 60)',
     'explanation:"60 of the 100 students passed maths. P = 60/100."',
     'explanation:"50 of the 100 students passed maths. P = 60/100."'),
    ('~the Why card names', 'a slip named for a value it does not give',
     "add('comp',rSub(D,N),D,", "add('comp',rSub(D,N),N,"),
    # The diagram box's spacing as it was before this contract (padding and margin 20px, its title 14px with a 16px
    # gap): padding alone is 40px, and the tightest item at 320x568 has 60px to spare, so the title's gap goes back too.
    ('~at 320x568: the last answer control', "the diagram's padding restored (20px), options below the fold",
     '.data-container{padding:6px 6px 8px;margin-bottom:6px;border-radius:10px}\n.data-title{font-size:12.5px;line-height:1.3;margin-bottom:4px}',
     '.data-container{padding:20px;margin-bottom:20px;border-radius:10px}\n.data-title{font-size:14px;line-height:1.6;margin-bottom:16px}'),
    # GIVEN-THAT-VENN-FADE's two (contract step 3).
    ('gcse_06 p2', "the Venn's fade rule removed", '.venn-label.greyed,.venn-set-label.greyed{opacity:0.2}', ''),
    ('gcse_03 p2', "a greyOut fading the condition's own column (Bus)", 'greyOut:"col_Car,col_Cycle"', 'greyOut:"col_Bus,col_Cycle"'),
    # GIVEN-THAT-POLISH's (contract step 6; the first above is its "a stored greyOut that fades inside the condition").
    ('core_01 p2', 'a non-Bayes item stored "none"', 'phase2:{greyOut:"col_Yes",condition:"the casualty',
     'phase2:{greyOut:"none",condition:"the casualty'),
    ('~inferGreyOut is back', "inferGreyOut restored, core_09's stored greyOut removed",
     [('phase2:{greyOut:"col_< 2 hours,col_2-4 hours",condition:"the teenager', 'phase2:{condition:"the teenager'),
      ('/* ---------- RENDER ANSWER AREA ---------- */', OLD_INFER + '/* ---------- RENDER ANSWER AREA ---------- */'),
      ('  // Grey-out animation\n', '  inferGreyOut(q);\n  // Grey-out animation\n')], None),
    # GIVEN-THAT-SET-LABELS's (contract step 3; Amendments 1 and 2).
    ('~venn-set-label', "the set names' fill removed (SVG's default black)",
     "font-weight:700;text-anchor:middle;fill:var(--text);dominant-baseline", "font-weight:700;text-anchor:middle;dominant-baseline"),
    ('~ is 4.22:1 (', 'the old muted grey (#7a7f90, 4.22:1)', '--muted:#8a8fa0;', '--muted:#7a7f90;'),
    ('~#startBtn', "Start Game's white text on the amber back", "background:var(--accent);color:#0f1117;font-family:'Outfit',sans-serif;font-size:17px",
     "background:var(--accent);color:#fff;font-family:'Outfit',sans-serif;font-size:17px"),
]
# A plant that must be caught on every item of a kind: the ids, from the page's bank, each must be named in a fault.
PLANT_EVERY = {"the set names' fill removed (SVG's default black)":
               lambda bank: [q['id'] for lv in bank for q in bank[lv] if q['data']['type'] == 'venn']}
# The stage each plant needs: the bank's own checks catch most; marking and slips need the play; the layout the fit.
PLANT_STAGES = {'r-002/r-003: marked within 0.005, no precision': ('play',),
                'r-004: decimals only, the fraction unreadable': ('play',),
                'a slip named for a value it does not give': ('play',),
                "the diagram's padding restored (20px), options below the fold": ('fit',),
                "the Venn's fade rule removed": ('fade',),
                "a greyOut fading the condition's own column (Bus)": ('fade',),
                "the set names' fill removed (SVG's default black)": ('contrast',),
                'the old muted grey (#7a7f90, 4.22:1)': ('contrast',),
                "Start Game's white text on the amber back": ('contrast',)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='check this file as the game page')
    bc.shard_args(ap)
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    # Work units (ci_shards, canon 7.8.1): the bank and the play at 390x844, the fit sweep a size at a time (both
    # modes), and each plant. With no --shard, all of them.
    shard = bc.Shard(__file__, args)
    checks = ['bank and play', 'fade', 'contrast'] + ['fit %dx%d' % s for s in FIT_SIZES]
    plants = [] if args.no_selftest or args.against else ['plant: ' + p[1] for p in PLANTS]
    mine = shard.pick(checks + plants)
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, report, n, tally, unnamed, computed = [], [], 0, {}, [], []
    for u in checks:
        if u not in mine:
            continue
        with shard.unit(u):
            if u == 'bank and play':
                f, n = run(html, ('bank', 'play'))
                tally, unnamed, computed = dict(TALLY), list(UNNAMED), list(COMPUTED)
            elif u == 'fade':
                f, n = run(html, ('bank', 'fade'))
                bk = load_bank(html) or {}
                bayes = [q['id'] for lv in bk for q in bk[lv] if fade_group(q) is None]
                print('  fade: %d items into Phase 2 at %s, with and without reduced motion, every one judged against '
                      'SPEC: %d fade their condition\'s outside, %d Bayes trees store "none" (by design): %s'
                      % (n, ', '.join('%dx%d' % s for s in FADE_SIZES), n - len(bayes), len(bayes), ', '.join(bayes)))
            elif u == 'contrast':
                f, n = run(html, ('bank', 'contrast'))
                print('  contrast: every text element at least %.1f:1 against what is painted beneath it, at %s, normal '
                      'and Aa (faded and disabled exempt): %s judged'
                      % (MIN_CONTRAST, ', '.join('%dx%d' % s for s in CONTRAST_SIZES),
                         ', '.join('%s %d' % kv for kv in sorted(CONTRAST_TALLY.items()))))
            else:
                w, h = (int(x) for x in u.split()[1].split('x'))
                f, n = run(html, ('bank', 'fit'), [(w, h)])
                report += FIT_REPORT
        fails += [x for x in f if x not in fails]       # the bank's own faults come back from every unit: once each
    print('%s: %d questions (%d phases): every diagram, key and option checked; every answer marked in Chromium; '
          'every wrong answer\'s Why card checked; fitted at %s in normal and Aa'
          % (SLUG, n, 2 * n, ', '.join(u.split()[1] for u in checks if u.startswith('fit ') and u in mine) or 'no size in this part'))
    if tally:
        print('  slips named, by family (wrong values; GCSE options, then every wrong ratio a typed level can take):')
        for (where, ph, fam), k in sorted(tally.items()):
            print('    %-13s %s %-10s %d' % (where, ph, fam, k))
        print('  GCSE options with no slip sentence (%d): %s' % (len(unnamed), ', '.join(unnamed)))
        print('  wrong values whose sentence names what was computed (%d): %s' % (len(computed), ', '.join(computed)))
    if report:
        print('  reported, not gated (%d): the tightest asking screen at each size, Next below the fold on a phone, '
              'and the parked items' % len(report))
        for r in report:
            print('    ' + r)
    ok = True
    for tag, what, old, new in PLANTS:
        if 'plant: ' + what not in mine:
            continue
        with shard.unit('plant: ' + what):
            pairs = old if isinstance(old, list) else [(old, new)]
            planted = html
            for o, n_ in pairs:
                if planted.count(o) != 1:
                    break
                planted = planted.replace(o, n_)
            else:
                o = None
            if o is not None:
                print('  self-test %-48s *** CANNOT PLANT (%d) ***' % (what, planted.count(o)))
                ok = False
                continue
            stages = ('bank',) + PLANT_STAGES.get(what, ())
            rep, _ = run(planted, stages, [(320, 568)], (False,))
            hit = [f for f in rep if (tag[1:] in f if tag.startswith('~') else f.startswith(tag))]
            if hit and what in PLANT_EVERY:
                need = PLANT_EVERY[what](load_bank(planted) or {})
                missed = [i for i in need if not any(('diagram %s ' % i) in f for f in hit)]
                if missed or not need:
                    print('  self-test %-48s *** caught on %d of %d: missed %s ***'
                          % (what, len(need) - len(missed), len(need), ', '.join(missed)))
                    hit = []
                else:
                    hit = ['every one of the %d: ' % len(need) + hit[0]]
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
