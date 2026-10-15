#!/usr/bin/env python3
# ci-line: Better Value claims (every item's declared measure computed from its inputs; the key's claim true, every distractor's false; every text figure in its claim; KNOWN) |
"""Better Value: each item declares the measure "better" is judged by, and each conclusion what it claims.

Contract BV-CLAIMS (14 Oct 2026; verbatim with its amendment in docs/history/contracts/2026-10-14-bv-claims.md).
The game's items carry data the page never renders: `criterion` (the scenario's plain-words sentence saying
what the person wants), `measure`, `inputs` (the named quantities per option), optionally `provisional` (a
measure Jon has still to choose; see docs/handover/better-value-decisions.md), and on every conclusion a `claim`:
    {winner: 'A' | 'B' | 'equal' | null, figures: [{option, value, of}], threshold?, measure?, at?}
This script computes the measure for each option from the inputs and checks, for every item:
  - the key's claim is true: the right winner and every checked figure right;
  - every distractor's claim is false: a wrong winner or a wrong figure;
  - every number in a conclusion's text is a figure of its claim (or its threshold);
  - a null winner is reported as a judgement;
  - a distractor naming the key's winner with a wrong figure has an explanation stating the right figure
    (Jon's ruling: right verdict, wrong figure, is wrong only if the working shows the right figure);
  - a distractor whose claim names a measure of its own (claim.measure: "cheaper" read as the pack price, say)
    and is true under it is reported: a student reading the words can defend it;
  - an input the verdict depends on but the scenario never states (inputs.unstated) is reported.
Today's failures are listed in KNOWN, keyed by (id, reason, conclusion); a failure not in KNOWN fails, and a
KNOWN entry that no longer happens fails too, so KNOWN only shrinks as content is fixed.

Measures. Costs (lower wins): total_cost = the sum of the option's terms; unit_cost = that sum / per. Higher
wins: day_rate, hourly_rate, average and fuel_economy (sum / per); disposable_income (sum of terms, rent
negative); net_profit (sales - cost); roi ((sales - cost) / cost x 100). A term is amount x times / per, each
of times and per a number or the name of a shared input. crossover (the amendment): each option costs
fixed + per_unit x n; n* = (fixed_B - fixed_A) / (rate_A - rate_B); the winner beyond n* is the option with
the lower rate. Discrete: the threshold is the first whole n at which the winner is strictly cheaper ("above
v" means v + 1 is that n; "at least v" means v is); a whole n* is level there. Continuous: within +-0.1
(TOLERANCE). Equal rates: no crossover; equal fixed too: always equal; else the lower fixed always wins. A
threshold of null is "always". inputs.compare = 'payback' (core_038) compares each option's own payback,
fixed / per_unit, lower winning.

Figure kinds (`of`): measure (default; the option's measure, at the text's printed precision); difference
(|A - B| of the measure); total (the sum of the option's terms); amount:<term> (a term's amount as given);
term:<term> (a term's total); crossover (n*); first (the first whole n the winner is strictly cheaper);
given (a number in the scenario or deal cards); premise (a number in a stated reason; not checked).

Relation to verify-better-value.py: that verifier still recomputes every keyed and explanation figure and
plays every card in Chromium; its BREAK_EVEN check fails a threshold option that is TRUE read as a sufficient
condition ("worth it if you eat 15 or more"), which this script's crossover claims (the switch point) do not
cover. Both run.

    python scripts/verify-better-value-claims.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'better-value'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
TOLERANCE = F(1, 10)            # continuous crossover thresholds ("about 11.8 years"): within +-0.1
MEASURES = {'unit_cost': 'lower', 'total_cost': 'lower', 'day_rate': 'higher', 'hourly_rate': 'higher',
            'average': 'higher', 'fuel_economy': 'higher', 'disposable_income': 'higher', 'net_profit': 'higher',
            'roi': 'higher', 'crossover': 'lower'}
RATIO = {'unit_cost', 'day_rate', 'hourly_rate', 'average', 'fuel_economy'}
NUM = re.compile(r'(?<![\w.])(\d[\d,]*(?:\.\d+)?)')

# Today's failures. Empty since BV-CRITERIA (15 Oct 2026): the audit's content changes are made and every scenario
# but core_039's states its criterion (core_039's key holds whichever month you stop). A new failure fails; an entry
# is added only on Jon's ruling.
KNOWN = set()


# ---------------------------------------------------------------- reading the bank from the page source
def literal(node):
    t = node.type
    if t == 'ObjectExpression':
        out = {}
        for p in node.properties:
            k = p.key.name if p.key.type == 'Identifier' else p.key.value
            out[k] = literal(p.value)
        return out
    if t == 'ArrayExpression':
        return [literal(e) for e in node.elements]
    if t == 'Literal':
        if isinstance(node.value, bool) or node.value is None or isinstance(node.value, str):
            return node.value
        return F(node.raw)
    if t == 'UnaryExpression' and node.operator == '-':
        return -literal(node.argument)
    raise ValueError('not a literal: %s' % t)


def load(html):
    tree, _src = bc.parse_game_source(html)
    if tree is None:
        raise SystemExit('the game page does not parse')
    for name, init, _kind in bc.top_level_declarations(tree):
        if name == 'QUESTIONS':
            return literal(init)
    raise SystemExit('QUESTIONS not found')


# ---------------------------------------------------------------- arithmetic
def resolve(x, inputs):
    if isinstance(x, str):
        return resolve(inputs[x], inputs)
    if isinstance(x, list):
        out = F(1)
        for y in x:
            out *= resolve(y, inputs)
        return out
    return F(x)


def term_total(t, inputs):
    v = F(t['amount'])
    for x in t.get('times', []):
        v *= resolve(x, inputs)
    for x in t.get('per', []):
        v /= resolve(x, inputs)
    return v


def total(opt, inputs):
    return sum((term_total(t, inputs) for t in opt['terms']), F(0))


def measure_value(measure, q, o, inputs):
    opt = inputs[o]
    if measure == 'total_cost' or measure == 'disposable_income':
        return total(opt, inputs)
    if measure in RATIO:
        return total(opt, inputs) / resolve(opt['per'], inputs)
    if measure == 'net_profit':
        return F(opt['sales']) - F(opt['cost'])
    if measure == 'roi':
        return (F(opt['sales']) - F(opt['cost'])) / F(opt['cost']) * 100
    if measure.startswith('term:'):
        name = measure[5:]
        return sum((term_total(t, inputs) for t in opt['terms'] if t['name'] == name), F(0))
    raise ValueError(measure)


def direction(measure):
    return MEASURES.get(measure, 'lower')


def winner_of(va, vb, dirn):
    if va == vb:
        return 'equal'
    return 'A' if (va < vb) == (dirn == 'lower') else 'B'


def fixed_of(opt, inputs):
    f = opt['fixed']
    return sum((term_total(t, inputs) for t in f), F(0)) if isinstance(f, list) else F(f)


def crossover(inputs):
    """(n*, winner beyond, first whole n strictly cheaper) or (None, always-winner, None)."""
    fa, fb = fixed_of(inputs['A'], inputs), fixed_of(inputs['B'], inputs)
    ra, rb = F(inputs['A']['per_unit']), F(inputs['B']['per_unit'])
    if ra == rb:
        return None, ('equal' if fa == fb else ('A' if fa < fb else 'B')), None
    n = (fb - fa) / (ra - rb)
    beyond = 'A' if ra < rb else 'B'
    if n <= 0:
        return None, beyond, None
    first = n.numerator // n.denominator + 1 if n.denominator == 1 else -((-n.numerator) // n.denominator)
    return n, beyond, first


def cost_at(opt, inputs, n):
    return fixed_of(opt, inputs) + F(opt['per_unit']) * n


# ---------------------------------------------------------------- figures in text
def text_numbers(text):
    out = []
    for m in NUM.finditer(text):
        raw = m.group(1).replace(',', '')
        dp = len(raw.split('.')[1]) if '.' in raw else 0
        out.append((F(raw), dp))
    return out


def at_dp(v, dp):
    q = v * 10 ** dp
    whole = q.numerator // q.denominator
    if q - whole >= F(1, 2):
        whole += 1
    return F(whole, 10 ** dp)


def givens(q):
    text = q['scenario'] + ' ' + ' '.join('%s %s' % (d['key'], d['value'])
                                          for o in ('optionA', 'optionB') if o in q for d in q[o]['details'])
    return {v for v, _ in text_numbers(text)}


def dp_for(value, text):
    """The printed precision of `value` in the conclusion's text (it must be there)."""
    best = None
    for v, dp in text_numbers(text):
        if v == F(value):
            best = dp if best is None else max(best, dp)
    if best is None:
        s = str(float(F(value)))
        best = len(s.split('.')[1].rstrip('0')) if '.' in s else 0
    return best


# ---------------------------------------------------------------- one claim
def judge(q, k, c):
    """(true?, [wrong figure (computed, dp)], winner the measure gives) for claim of conclusion k (0-based)."""
    claim = c['claim']
    inputs = dict(q['inputs'])
    if claim.get('at'):
        inputs.update(claim['at'])
    measure = claim.get('measure') or q['measure']
    text = c['text']
    wrong = []
    if measure == 'crossover':
        return judge_crossover(q, claim, inputs, text)
    va, vb = measure_value(measure, q, 'A', inputs), measure_value(measure, q, 'B', inputs)
    truth = winner_of(va, vb, direction(measure))
    for f in claim['figures']:
        kind = f.get('of', 'measure')
        dp = dp_for(f['value'], text)
        want = None
        if kind == 'measure':
            want = va if f['option'] == 'A' else vb
        elif kind == 'difference':
            want = abs(va - vb)
        elif kind == 'total':
            want = total(inputs[f['option']], inputs)
        elif kind.startswith('amount:'):
            ts = [t for t in inputs[f['option']]['terms'] if t['name'] == kind[7:]]
            want = abs(F(ts[0]['amount'])) if ts else None
        elif kind.startswith('term:'):
            ts = [t for t in inputs[f['option']]['terms'] if t['name'] == kind[5:]]
            want = abs(term_total(ts[0], inputs)) if ts else None
        elif kind == 'given':
            if F(f['value']) not in givens(q):
                wrong.append((None, dp))
            continue
        elif kind == 'premise':
            continue
        if want is None or at_dp(want, dp) != F(f['value']):
            wrong.append((want, dp))
    return claim['winner'] == truth and not wrong, wrong, truth


def judge_crossover(q, claim, inputs, text):
    wrong = []
    if inputs.get('compare') == 'payback':
        pa = F(inputs['A']['fixed']) / F(inputs['A']['per_unit'])
        pb = F(inputs['B']['fixed']) / F(inputs['B']['per_unit'])
        truth = winner_of(pa, pb, 'lower')
        for f in claim['figures']:
            kind = f.get('of', 'measure')
            if kind in ('premise', 'given'):
                continue
            want = pa if f['option'] == 'A' else pb
            dp = dp_for(f['value'], text)
            if at_dp(want, dp) != F(f['value']):
                wrong.append((want, dp))
        return claim['winner'] == truth and not wrong, wrong, truth
    n, beyond, first = crossover(inputs)
    th = claim.get('threshold')
    ok = True
    if th is None or th.get('value') is None:
        # "always": true only when the lines never cross and the claimed option always wins
        ok = n is None and claim['winner'] == beyond
    elif claim['winner'] == 'equal':
        v = F(th['value'])
        ok = cost_at(inputs['A'], inputs, v) == cost_at(inputs['B'], inputs, v)
    else:
        v = F(th['value'])
        if n is None:
            ok = False
        elif th.get('discrete', True):
            ok = (v + 1 == first) if th.get('from') == 'above' else (v == first)
        else:
            ok = abs(v - n) <= TOLERANCE
        ok = ok and claim['winner'] == beyond
    for f in claim['figures']:
        kind = f.get('of', 'measure')
        dp = dp_for(f['value'], text)
        if kind == 'first':
            if first is None or F(f['value']) != first:
                wrong.append((first, 0))
        elif kind == 'crossover':
            if n is None or abs(F(f['value']) - n) > TOLERANCE:
                wrong.append((n, dp))
        elif kind == 'given':
            if F(f['value']) not in givens(q):
                wrong.append((None, dp))
    return ok and not wrong, wrong, beyond


def numbers_in_explanation(q):
    return text_numbers(q['explanation'])


def explains(q, want, dp):
    """The explanation states `want` at its own printed precision (the wrong figure's dp does not matter)."""
    return any(v == at_dp(want, edp) for v, edp in numbers_in_explanation(q))


# ---------------------------------------------------------------- the checks
def check(bank):
    found = []          # (id, reason, k, detail); k is 1-based for a conclusion, 0 for the item
    for q in [q for lv in bank.values() for q in lv]:
        qid = q['id']
        for field in ('criterion', 'measure', 'inputs'):
            if field not in q:
                found.append((qid, 'schema', 0, 'no %s' % field))
        if 'measure' not in q or 'inputs' not in q:
            continue
        if q['measure'] not in MEASURES:
            found.append((qid, 'schema', 0, 'unknown measure %r' % q['measure']))
            continue
        if q.get('provisional'):
            found.append((qid, 'provisional-measure', 0, 'measure %s is provisional (decisions doc)' % q['measure']))
        for name in q['inputs'].get('unstated', []):
            found.append((qid, 'quantity-unstated', 0, 'the verdict depends on %r, which the scenario does not state' % name))
        keys = [k for k, c in enumerate(q['conclusions']) if c['correct']]
        key_winner = q['conclusions'][keys[0]]['claim']['winner'] if len(keys) == 1 and 'claim' in q['conclusions'][keys[0]] else None
        for k, c in enumerate(q['conclusions']):
            if 'claim' not in c:
                found.append((qid, 'schema', k + 1, 'no claim'))
                continue
            claim = c['claim']
            # every number in the text is a figure of the claim or its threshold
            values = {F(f['value']) for f in claim['figures']}
            th = claim.get('threshold') or {}
            if th.get('value') is not None:
                values.add(F(th['value']))
            for v, dp in text_numbers(c['text']):
                if not any(at_dp(x, dp) == v or x == v for x in values):
                    found.append((qid, 'text-figure', k + 1, '%s in %r is not in its claim' % (v, c['text'])))
            if claim['winner'] is None:
                found.append((qid, 'judgement', k + 1, '%r names no checkable winner' % c['text']))
                continue
            true, wrong, truth = judge(q, k, c)
            own = claim.get('measure')
            if c['correct']:
                if not true:
                    found.append((qid, 'key-false', k + 1, 'the key %r: the measure gives %s%s'
                                  % (c['text'], truth, ', wrong figure(s) %s' % [(str(w), dp) for w, dp in wrong] if wrong else '')))
            elif true:
                found.append((qid, 'true-under-own-measure' if own else 'distractor-true', k + 1,
                              '%r is true%s' % (c['text'], ' read as %s' % own if own else '')))
            elif claim['winner'] == key_winner and wrong and not own:
                for want, dp in wrong:
                    if want is not None and not explains(q, want, dp):
                        found.append((qid, 'uncorrected-figure', k + 1, '%r has the key\'s winner and a wrong figure; '
                                      'the explanation never states %s' % (c['text'], at_dp(want, dp))))
    return found


def report(found):
    fails = []
    seen = {(i, r, k) for i, r, k, _ in found}
    for i, r, k, d in found:
        if (i, r, k) not in KNOWN:
            fails.append('%s C%s %s: %s' % (i, k, r, d))
    for e in sorted(KNOWN - seen):
        fails.append('%s C%s %s: in KNOWN but no longer happens; remove it from KNOWN' % e)
    return fails


# ---------------------------------------------------------------- self-test
def S(s):
    """Page-source form of a text: non-ASCII as \\uXXXX, as the game file writes it."""
    return ''.join(c if ord(c) < 128 else '\\u%04x' % ord(c) for c in s)


PLANTS = [
    # (what, expected (id, reason, k), old, new)
    ('a true distractor', ('bv_core_001', 'distractor-true', 1),
     S("{text:'Gym A is better value — total cost £420 vs £396 for Gym B',correct:false,claim:{winner:'A',figures:[{option:'A',value:420},{option:'B',value:396}]}}"),
     S("{text:'Gym B is better value — total £396 vs £420 for Gym A',correct:false,claim:{winner:'B',figures:[{option:'B',value:396},{option:'A',value:420}]}}")),
    ('a wrong key figure', ('bv_core_002', 'key-false', 2),
     S("{text:'Provider B is better value — total cost £481 vs £522 for Provider A',correct:true,claim:{winner:'B',figures:[{option:'B',value:481},"),
     S("{text:'Provider B is better value — total cost £491 vs £522 for Provider A',correct:true,claim:{winner:'B',figures:[{option:'B',value:491},")),
    ('a text figure not in its claim', ('bv_core_003', 'text-figure', 2),
     S("{text:'The subscription machine is better value — annual cost £284 vs £832 for the coffee shop'"),
     S("{text:'The subscription machine is better value — annual cost £294 vs £832 for the coffee shop'")),
    ('the key\'s winner, a wrong figure, no correction', ('bv_gcse_013', 'uncorrected-figure', 1),
     S("explanation:'Deal store: £20 + £4.99 = £24.99."), S("explanation:'Deal store: £20 + £4.99.")),
    ('an off-by-one discrete threshold', ('bv_gcse_019', 'key-false', 1),
     S("more than 12 lunches per month — from the 13th lunch onwards',correct:true,claim:{winner:'A',figures:[{option:null,value:13,of:'first'}],threshold:{value:12,"),
     S("more than 13 lunches per month — from the 14th lunch onwards',correct:true,claim:{winner:'A',figures:[{option:null,value:14,of:'first'}],threshold:{value:13,")),
    ('a wrong winner beyond the crossover', ('bv_core_027', 'key-false', 1),
     "{text:'Tariff B becomes better value above 80 minutes of calls per month',correct:true,claim:{winner:'B',",
     "{text:'Tariff A becomes better value above 80 minutes of calls per month',correct:true,claim:{winner:'A',"),
    ('"always cheaper" where the lines cross', ('bv_core_024', 'key-false', 3),
     S("{text:'The café is always cheaper',correct:false,"), S("{text:'The café is always cheaper',correct:true,")),
]
# Must stay unflagged: a right-verdict, wrong-figure distractor whose explanation states the right figure.
CONTROLS = [('bv_gcse_013', 1), ('bv_gcse_012', 1), ('bv_core_031', 1), ('bv_gcse_007', 4), ('bv_core_032', 3)]


def selftest(html):
    ok = True
    clean = {(i, k) for i, r, k, _ in check(load(html)) if r == 'uncorrected-figure'}
    for c in CONTROLS:
        hit = c in clean
        ok = ok and not hit
        print('  control %-50s %s' % ('%s C%d: wrong figure, corrected' % c, '*** FLAGGED ***' if hit else 'not flagged'))
    for what, want, old, new in PLANTS:
        if html.count(old) != 1:
            print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
            ok = False
            continue
        found = check(load(html.replace(old, new)))
        hit = [d for i, r, k, d in found if (i, r, k) == want]
        ok = ok and bool(hit)
        print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:90]) if hit else '*** MISSED ***'))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='check this file instead of the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    bank = load(html)
    found = check(bank)
    n = sum(len(v) for v in bank.values())
    print('%s claims: %d items, %d conclusions; %d known failure(s) (KNOWN)'
          % (SLUG, n, sum(len(q['conclusions']) for v in bank.values() for q in v), len(KNOWN)))
    fails = report(found)
    ok = True
    if not args.no_selftest and not args.against:
        ok = selftest(html)
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught, or a control was flagged')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
