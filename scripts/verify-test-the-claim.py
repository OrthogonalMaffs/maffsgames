#!/usr/bin/env python3
# ci-line: B1 | Test the Claim (independent recomputation of every key) |
"""Independent verification for test-the-claim (docs/todo.md §1.14, §1.26).

WHY THIS IS NOT LIKE verify-graph-transformer.py
----------------------------------------------------------------------------
The Graph Transformer verifier runs the game's own curve-match code against its own
puzzles, because there the risk is a puzzle the game's rules cannot solve. Here the risk
is the opposite: the AUTHORED NUMBERS are wrong (a critical region, a tail probability,
a p-value, a verdict), so any value or function taken from the game would only ever
confirm itself. This script therefore reads the bank's RAW PARAMETERS -- n, p0, x,
lambda0, mu0, sigma, xbar, r, the significance level and the tail -- and recomputes
everything else from first principles:

  binomial   exact rational arithmetic, fractions.Fraction and math.comb
  Poisson    decimal.Decimal at 60 digits (the only irrational is e^-lambda)
  Normal     statistics.NormalDist for critical values and tail probabilities
  PMCC       the exact null distribution of r (regularised incomplete beta), inverted
             by bisection -- not a copy of any table. It is then held against the rows
             of the exam booklet the game uses (BOOKLET below): Jon's ruling of
             30 Sep 2026 is that the game must match what the student has in the exam,
             so a disagreement between exact computation and the booklet FAILS.

No scipy, no numpy, and nothing is copied from the game except the bank itself.

WHAT IS RUN FROM THE GAME, AND WHY
----------------------------------------------------------------------------
Three pieces of game code are executed in a bare node vm, only to learn what the game
MARKS CORRECT -- a key cannot be checked without the key:

  generateWrongContexts   the Step 6 distractors
  buildStep4              which Step 4 statement is marked correct, in both methods
  buildStep6              which Step 6 evidence / action / context is marked correct

Nothing they return is trusted. Each marked-correct statement is compared with the
verdict this script computes itself: a Step 4 option saying "the p-value is less than
the significance level" must be true of the recomputed p-value, a Step 6 "sufficient
evidence" must match the recomputed decision, and so on. Every other game function is
stubbed out (K() returns its input; buildRenderedSelect records its options).

CRITICAL-REGION CONVENTION (AQA / Edexcel / OCR A-level Statistics)
----------------------------------------------------------------------------
  * one tail   lower: the LARGEST c with P(X <= c) <= alpha
               upper: the SMALLEST c with P(X >= c) <= alpha
  * two tails  the same, at alpha/2 on each side; a tail with no such c has no
               critical region (stored as -1; step 3 accepts a blank Lower box for it)
  * the actual significance level is the total probability of the region, and is
               always <= the nominal level; it is printed in --verbose
  * p-value    one tail: the probability of the observed value and everything more
               extreme in the direction of H1. TWO tails: the game asks for the
               probability in the tail on the observed side, and Step 4 compares it
               with HALF the significance level, labelled "the probability in the tail",
               not "the p-value" (Jon's ruling, 30 Sep 2026)

WHAT IT CHECKS, PER ITEM
----------------------------------------------------------------------------
  hypotheses     H0/H1 text matches the parameters and the tail; the marked option is
                 that text; no distractor spells the same hypothesis
  distribution   the stated distribution matches the parameters; the marked option is it
  binomial and   every value in givenCDF; the critical boundary/boundaries; crTailAlpha;
  Poisson        every probability and every "a < b" claim inside crExplanation; the
                 p-value and its pValueExpr; inCR; reject. A probability the student
                 needs but is not shown is a WARN when the scenario tells them to use
                 their calculator, and a FAIL when it does not
  Normal         z, z (2 d.p.) and the worked formula; both critical-value tables;
                 crStatement; pValue, pValueExpr and crExplanation (canonical text, see
                 normal_fields); inCR; reject
  correlation    the critical value against exact computation AND the booklet row; the
                 PMCC table the game shows; pValue, pValueExpr, crExplanation (see
                 corr_fields); inCR; reject
  every item     the stored p-value sits on the same side of the comparison level as the
                 verdict; Step 4 and Step 6 mark true statements; the Step 6 distractors
                 never repeat the correct conclusion; the scenario states n, x, alpha and
                 the parameters it claims

Output is `FAIL [category] <id> <field>: stated <a>, computed <b>`. Exit 1 on any
FAIL. A fault-injection self-test runs first on every invocation, and the run aborts if
any injected fault is NOT caught.

    python scripts/verify-test-the-claim.py              # verify, run self-test
    python scripts/verify-test-the-claim.py --verbose    # also print every item's numbers
    python scripts/verify-test-the-claim.py --file X     # verify a different copy of the page
"""
import argparse
import copy
import json
import os
import re
import subprocess
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from statistics import NormalDist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stats_common import (PREC, D, to_dec, rnd, fmt, Binomial, Poisson, as_dec,  # noqa: E402
                          lower_cr, upper_cr, tail_prob, r_two_tail_p, r_critical, r_cv_txt)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'games', 'test-the-claim', 'index.html')
OPTIONS_JS = os.path.join(ROOT, 'schools', 'assets', 'options.js')

# Pearson Edexcel Level 3 AS and A level Statistics, "Statistical formulae and tables",
# Issue 1, August 2017, Table 8: Critical Values of the Product Moment Correlation
# Coefficient. Transcribed for the sample sizes the game uses; columns are the
# TWO-tail significance levels 20%, 10%, 5%, 2%, 1% (one tail: 10%, 5%, 2.5%, 1%, 0.5%).
# All 260 cells of that table (n = 4..100) were compared with r_critical() on
# 30 Sep 2026 and agree to 4 d.p. An item on an n not listed here FAILS until its row
# is added from the booklet.
BOOKLET_TWO_TAIL = (20, 10, 5, 2, 1)
BOOKLET = {
    10: ('0.4428', '0.5494', '0.6319', '0.7155', '0.7646'),
    12: ('0.3981', '0.4973', '0.5760', '0.6581', '0.7079'),
    15: ('0.3507', '0.4409', '0.5140', '0.5923', '0.6411'),
    18: ('0.3170', '0.4000', '0.4683', '0.5425', '0.5897'),
    20: ('0.2992', '0.3783', '0.4438', '0.5155', '0.5614'),
    25: ('0.2653', '0.3365', '0.3961', '0.4622', '0.5052'),
    30: ('0.2407', '0.3061', '0.3610', '0.4226', '0.4629'),
}

NODE_DRIVER = r"""
const fs = require('fs'), vm = require('vm');
const html = fs.readFileSync(process.argv[1], 'utf8');
const optionsJs = fs.readFileSync(process.argv[2], 'utf8');
const unshuffled = process.argv[3] === 'unshuffled';
function grab(name) {
  const s = html.indexOf('function ' + name + '(');
  if (s < 0) { console.error(name + ' not found'); process.exit(2); }
  return html.slice(s, html.indexOf('\n}\n', s) + 3);
}
const start = html.indexOf('const QUESTIONS = {');
const endMark = html.indexOf('CORR_CV[n][10] = ');
if (start < 0 || endMark < 0) { console.error('bank markers not found'); process.exit(2); }
const bankSrc = html.slice(start, html.indexOf('});', endMark) + 3);
const ctx = { console };
vm.createContext(ctx);
ctx.window = ctx;
// Seeded, so the shuffle sample below is the same on every run: no flaky CI.
vm.runInContext(`(function () { let a = 20260930; Math.random = function () {
  a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
  t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; })();`, ctx);
vm.runInContext(optionsJs, ctx);
// Self-test hook: an options builder that keeps the author's order, i.e. an unshuffled build.
if (unshuffled) vm.runInContext('MaffsOptions.build = function (c, d) { return [c].concat(d); };', ctx);
vm.runInContext(bankSrc + '\n' +
  ['generateWrongContexts', 'shuffleWithCorrect', 'stepHeader', 'pRoute', 'buildScenario', 'buildStep3', 'buildStep4', 'buildStep6']
    .map(grab).join('\n') + `
var state = { mode: null, method: 'cr' };
var __sel = {}, __dom = {};
function K(s) { return s; }
function $(id) { return __dom[id] || (__dom[id] = { innerHTML: '', value: '' }); }
function buildRenderedSelect(id, opts) { __sel[id] = opts; return ''; }
globalThis.__bank = JSON.parse(JSON.stringify({ Q: QUESTIONS, C: CORR_CV }));
globalThis.__wrong = {}; globalThis.__ui = {};
for (const m of Object.keys(QUESTIONS)) { for (const q of QUESTIONS[m]) {
  state.mode = m;
  __wrong[q.id] = generateWrongContexts(q);
  const ui = {};
  for (const meth of ['cr', 'pvalue']) {
    state.method = meth; __sel = {};
    buildStep4(q);
    ui['step4_' + meth] = __sel.step4Select[q._step4Correct];
  }
  __sel = {};
  buildStep6(q);
  ui.compA = __sel.compASelect[q._compACorrect];
  ui.compB = __sel.compBSelect[q._compBCorrect];
  ui.compC = __sel.compCSelect[q._compCShuffle.correctIdx];
  ui.compCOptions = __sel.compCSelect;
  // Step 6 loaded LOADS times: where the correct option lands, and how often it appears.
  ui.shuffle = { A: [], B: [], C: [] };
  const want = { A: ui.compA, B: ui.compB, C: ui.compC };
  for (let i = 0; i < 20; i++) {
    __sel = {};
    buildStep6(q);
    const got = { A: [__sel.compASelect, q._compACorrect], B: [__sel.compBSelect, q._compBCorrect],
                  C: [__sel.compCSelect, q._compCShuffle.correctIdx] };
    for (const k of ['A', 'B', 'C']) {
      const [opts, idx] = got[k];
      ui.shuffle[k].push({ pos: idx, marked: opts[idx], count: opts.filter(o => o === want[k]).length });
    }
  }
  buildScenario(q);
  ui.scenarioHtml = __dom.scenarioPanel.innerHTML;
  state.method = 'pvalue'; q._zCalcDone = true;
  ui.step3_pvalue = buildStep3(q);
  delete q._zCalcDone;
  __ui[q.id] = ui;
} }`, ctx);
process.stdout.write(JSON.stringify({ Q: ctx.__bank.Q, C: ctx.__bank.C, wrong: ctx.__wrong, ui: ctx.__ui }));
"""


def load_bank(page, unshuffled=False):
    r = subprocess.run(['node', '-e', NODE_DRIVER, page, OPTIONS_JS] + (['unshuffled'] if unshuffled else []),
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit('node could not read the bank: ' + r.stderr.strip())
    return json.loads(r.stdout)


# --------------------------------------------------------------------------
#  exact arithmetic
# --------------------------------------------------------------------------
def js_num(x):
    """How the game's JS prints a JSON number: 496, 65.5, -0.6."""
    return str(int(x)) if float(x) == int(float(x)) else repr(float(x))


ALPHA_TXT = {1: '0.01', 5: '0.05', 10: '0.10'}
HALF_TXT = {1: '0.005', 5: '0.025', 10: '0.05'}





# --------------------------------------------------------------------------
#  report
# --------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.fails, self.warns = [], []

    def fail(self, cat, iid, field, stated, computed, why=''):
        self.fails.append((cat, iid, field, stated, computed, why))

    def warn(self, iid, msg):
        self.warns.append((iid, msg))


def _num_tok(m):
    try:
        return str(Decimal(m.group(0)).normalize())
    except Exception:
        return m.group(0)


def norm(s):
    """Whitespace-, comma- and trailing-zero-insensitive form, so 'p = 0.20' equals 'p = 0.2'."""
    s = re.sub(r'\s+', '', str(s).replace('{,}', '').replace('\\,', '').replace('\\!', ''))
    return re.sub(r'\d+\.?\d*', _num_tok, s)


def num_present(text, value):
    """Is `value` present as a standalone number in the text? (commas ignored)"""
    for t in re.findall(r'\d[\d,]*\.?\d*', text):
        t = t.replace(',', '').rstrip('.')
        try:
            if Decimal(t) == D(value):
                return True
        except Exception:
            pass
    return False


# direction cues found in the scenario prose; only a UNIQUE contradicting cue fails
LOWER = re.compile(r'\b(decreas\w*|fall\w*|fallen|below|lower|fewer|reduc\w*)\b', re.I)
UPPER = re.compile(r'\b(increas\w*|exceed\w*|higher|greater|more than|improv\w*|towards heads)\b', re.I)
TWO = re.compile(r'\b(differs?|changed?|correlation between|correlate with)\b', re.I)
CALC_LINE = re.compile(r"calculator's (binomial|Poisson) distribution functions")


# --------------------------------------------------------------------------
#  common checks (all four modes)
# --------------------------------------------------------------------------
def check_common(rep, mode, q, wrong):
    iid = q['id']
    tail, td = q['tail'], q['tailDir']
    if (tail == 'one') != (td in ('lower', 'upper')) or (tail == 'two') != (td == 'two'):
        rep.fail('STRUCTURE', iid, 'tail/tailDir', f'{tail}/{td}', 'one+lower|upper or two+two')
    if q['inCR'] != q['reject']:
        rep.fail('KEY', iid, 'inCR vs reject', f"inCR={q['inCR']} reject={q['reject']}", 'equal',
                 'Step 4 and Step 5 would contradict each other')
    if q['sig'] not in (1, 5, 10):
        rep.fail('STRUCTURE', iid, 'sig', q['sig'], '1, 5 or 10')

    for h, correct_key in (('h0', 'h0Correct'), ('h1', 'h1Correct')):
        opts = q[h + 'Distractors']
        ci = q[correct_key]
        if norm(opts[ci]) != norm(q[h + 'Latex']):
            rep.fail('KEY', iid, f'{h}Distractors[{correct_key}]', opts[ci], q[h + 'Latex'],
                     'the option marked correct is not the stated hypothesis')
        for i, o in enumerate(opts):
            if i != ci and norm(o) == norm(opts[ci]):
                rep.fail('DISTRACTOR', iid, f'{h}Distractors[{i}]', o, f'!= {opts[ci]}', 'repeats the correct answer')

    dopts, dci = q['distDistractors'], q['distCorrect']
    if norm(dopts[dci]) != norm(q['distStatement']):
        rep.fail('KEY', iid, 'distDistractors[distCorrect]', dopts[dci], q['distStatement'])
    for i, o in enumerate(dopts):
        if i != dci and norm(o) == norm(dopts[dci]):
            rep.fail('DISTRACTOR', iid, f'distDistractors[{i}]', o, f'!= {dopts[dci]}', 'repeats the correct answer')

    ctx = q['conclusionContext']
    ws = wrong.get(iid, [])
    for i, w in enumerate(ws):
        if norm(w) == norm(ctx):
            rep.fail('DISTRACTOR', iid, f'Step 6 wrong context [{i}]', w, f'!= {ctx}',
                     'generateWrongContexts() returned the correct conclusion unchanged')
    if len({norm(w) for w in ws}) != len(ws):
        rep.fail('DISTRACTOR', iid, 'Step 6 wrong contexts', ws, 'all distinct')

    cues = {k for k, rx in (('lower', LOWER), ('upper', UPPER), ('two', TWO)) if rx.search(q['scenario'])}
    if mode != 'correlation' and len(cues) == 1 and td not in cues:
        rep.fail('SCENARIO', iid, 'tailDir', td, cues.pop(), 'scenario prose asks the other way')
    if mode != 'correlation' and not (num_present(q['scenario'], q['sig']) and '%' in q['scenario']):
        rep.fail('SCENARIO', iid, 'significance level', f"{q['sig']}%", 'not in scenario text')


def check_h(rep, iid, q, sym, val, td):
    """H0 is `sym = val`; H1 is `sym op val` with op fixed by the tail."""
    if norm(q['h0Latex']) != norm(f'{sym} = {val}'):
        rep.fail('KEY', iid, 'h0Latex', q['h0Latex'], f'{sym} = {val}')
    op = {'lower': '<', 'upper': '>', 'two': '\\neq'}[td]
    if norm(q['h1Latex']) != norm(f'{sym} {op} {val}'):
        rep.fail('KEY', iid, 'h1Latex', q['h1Latex'], f'{sym} {op} {val}')


def check_verdict(rep, iid, q, in_cr, basis):
    for f in ('inCR', 'reject'):
        if q[f] != in_cr:
            rep.fail('KEY', iid, f, q[f], in_cr, basis)


def tail_only(q):
    """Jon's convention, 30 Sep 2026: a "p-value" is two-sided on a two-tailed test and is
    compared with alpha; a "probability in the tail" is one tail and is compared with alpha/2.
    Correlation items (the only ones carrying nSample) give the exam's two-sided p-value;
    two-tailed binomial, Poisson and Normal items ask for one tail."""
    return q['tail'] == 'two' and 'nSample' not in q


def compare_level(q):
    """What Step 4 compares the p-value route with: alpha, or alpha/2 for one tail."""
    return Fraction(q['sig'], 100) / (2 if tail_only(q) else 1)


def check_p_side(rep, iid, q, p):
    """The comparison Step 4 makes in p-value mode must agree with the verdict."""
    level = to_dec(compare_level(q))
    if abs(as_dec(p) - level) < Decimal('0.00005'):
        rep.fail('AMBIGUOUS', iid, 'p vs level', fmt(p, 6), str(level), 'within rounding of the boundary')
    if (as_dec(p) < level) != q['inCR']:
        rep.fail('KEY', iid, 'p-value comparison', f"inCR={q['inCR']}", f'p={fmt(p, 4)} vs {level.normalize()}',
                 'the p-value route and the critical-region route reach different verdicts')


def check_ui(rep, iid, q, ui, p, in_cr):
    """What the game marks correct in Steps 4 and 6, held against the recomputed verdict."""
    if ui is None:
        rep.fail('STRUCTURE', iid, 'ui', 'missing', 'Step 4/6 keys')
        return
    sig = q['sig']
    less = 'less than' if as_dec(p) < to_dec(compare_level(q)) else 'not less than'
    if tail_only(q):
        want = f'The probability in the tail is {less} half the significance level ({js_num(sig / 2)}%)'
    else:
        want = f'The p-value is {less} the significance level ({sig}%)'
    if ui['step4_pvalue'] != want:
        rep.fail('KEY', iid, 'Step 4 (p-value) marked correct', ui['step4_pvalue'], want)
    want = f"The test statistic {'lies' if in_cr else 'does not lie'} in the critical region"
    if ui['step4_cr'] != want:
        rep.fail('KEY', iid, 'Step 4 (critical region) marked correct', ui['step4_cr'], want)
    want = f"There is {'sufficient' if in_cr else 'insufficient'} evidence at the {sig}% significance level to..."
    if ui['compA'] != want:
        rep.fail('KEY', iid, 'Step 6 evidence marked correct', ui['compA'], want)
    # The context is H1's claim, so the action is "support" whether or not H0 is rejected:
    # "(in)sufficient evidence ... to support the claim that <H1>".
    if ui['compB'] != '...support the claim that...':
        rep.fail('KEY', iid, 'Step 6 action marked correct', ui['compB'], '...support the claim that...',
                 'the context offered is the H1 statement, which is supported, never rejected')
    if ui['compC'] != q['conclusionContext']:
        rep.fail('KEY', iid, 'Step 6 context marked correct', ui['compC'], q['conclusionContext'])
    if ui['compCOptions'].count(q['conclusionContext']) != 1:
        rep.fail('DISTRACTOR', iid, 'Step 6 context options', ui['compCOptions'].count(q['conclusionContext']),
                 1, 'the correct conclusion must appear exactly once')
    # Every Step 6 dropdown is shuffled: over 20 seeded loads the correct option must land in
    # more than one position, appear exactly once, and be the one the key marks.
    for k, name in (('A', 'evidence'), ('B', 'action'), ('C', 'context')):
        loads = ui['shuffle'][k]
        if any(l['count'] != 1 for l in loads):
            rep.fail('DISTRACTOR', iid, f'Step 6 {name} options', [l['count'] for l in loads], 'exactly once on every load')
        if any(l['marked'] != loads[0]['marked'] for l in loads):
            rep.fail('KEY', iid, f'Step 6 {name} key across loads', sorted({l['marked'] for l in loads}), 'one correct option')
        if len({l['pos'] for l in loads}) < 2:
            rep.fail('SHUFFLE', iid, f'Step 6 {name} position', f"always {loads[0]['pos']} in {len(loads)} loads",
                     'varies', 'an unshuffled dropdown gives the answer away by its position')


# --------------------------------------------------------------------------
#  discrete modes
# --------------------------------------------------------------------------
LABEL = re.compile(r'P\(X\s*\\(leq|geq)\s*(\d+)\)')
EXPLAIN_P = re.compile(r'P\(X\s*\\(leq|geq)\s*(\d+)\)\s*=\s*(0\.\d+)')
EXPLAIN_CMP = re.compile(r'(0\.\d+)\s*([<>])\s*(0\.\d+)')


def check_discrete(rep, mode, q, verbose):
    iid, td, x = q['id'], q['tailDir'], q['x']
    if mode == 'binomial':
        dist = Binomial(q['n'], q['p0'])
        sym, val = 'p', q['p0']
        want_dist = f"X \\sim B({q['n']},\\, {q['p0']})"
        for f in ('n', 'x'):
            if not num_present(q['scenario'], q[f]):
                rep.fail('SCENARIO', iid, f, q[f], 'not in scenario text')
    else:
        lam = D(q['lambda0'])
        if q.get('requiresScaling'):
            lam = D(q['lambda0']) * D(q['scaleFactor'])
            for f in ('scaledLambda', 'scalingAnswer'):
                if D(q[f]) != lam:
                    rep.fail('KEY', iid, f, q[f], str(lam))
        dist = Poisson(lam)
        sym, val = '\\lambda', (int(lam) if lam == lam.to_integral() else lam)
        want_dist = f'X \\sim \\text{{Po}}({val})'
        for f in ('x', 'lambda0'):
            if not num_present(q['scenario'], q[f]):
                rep.fail('SCENARIO', iid, f, q[f], 'not in scenario text')
    check_h(rep, iid, q, sym, val, td)
    if norm(q['distStatement']) != norm(want_dist):
        rep.fail('KEY', iid, 'distStatement', q['distStatement'], want_dist)

    # ---- critical region under the convention -------------------------------
    alpha_tot = Fraction(q['sig'], 100)
    two = q['tail'] == 'two'
    a_tail = alpha_tot / 2 if two else alpha_tot
    a_txt = to_dec(a_tail).normalize()
    if D(q['crTailAlpha']) != to_dec(a_tail):
        rep.fail('KEY', iid, 'crTailAlpha', q['crTailAlpha'], str(a_txt), f'{"two" if two else "one"}-tailed at {q["sig"]}%')
    lo = lower_cr(dist, a_tail) if td in ('lower', 'two') else None
    hi = upper_cr(dist, a_tail) if td in ('upper', 'two') else None
    exp_direction = {'lower': 'leq', 'upper': 'geq', 'two': 'two'}[td]
    if q['crDirection'] != exp_direction:
        rep.fail('STRUCTURE', iid, 'crDirection', q['crDirection'], exp_direction)
    if td == 'two':
        got_lo, got_hi = q.get('crBoundaryLower'), q.get('crBoundaryUpper')
        exp_lo = -1 if lo is None else lo
        if got_lo != exp_lo:
            rep.fail('KEY', iid, 'crBoundaryLower', got_lo, exp_lo,
                     f'largest c with P(X<=c)<={a_txt}' if lo is not None else f'no c has P(X<=c)<={a_txt}; expect the -1 sentinel')
        if hi is None:
            rep.fail('KEY', iid, 'crBoundaryUpper', got_hi, 'none', 'no upper critical region exists')
        elif got_hi != hi:
            rep.fail('KEY', iid, 'crBoundaryUpper', got_hi, hi, f'smallest c with P(X>=c)<={a_txt}')
        if lo is not None and hi is not None and str(q['crBoundary']) != f'{lo} or {hi}':
            rep.fail('KEY', iid, 'crBoundary (label)', q['crBoundary'], f'{lo} or {hi}')
        if lo is None or hi is None:
            want = [hi] if lo is None else [lo]
            if [int(t) for t in re.findall(r'-?\d+', str(q['crBoundary']))] != want:
                rep.fail('KEY', iid, 'crBoundary (label)', q['crBoundary'], f'none / {want[0]}')
        in_cr = (lo is not None and x <= lo) or (hi is not None and x >= hi)
        size = (as_dec(dist.le(lo)) if lo is not None else Decimal(0)) + (as_dec(dist.ge(hi)) if hi is not None else Decimal(0))
        cr_text = (f'X<={lo}' if lo is not None else '-') + (f' or X>={hi}' if hi is not None else '')
    elif td == 'lower':
        if lo is None:
            rep.fail('KEY', iid, 'crBoundary', q['crBoundary'], 'none', 'no critical region exists at this level')
        elif q['crBoundary'] != lo:
            rep.fail('KEY', iid, 'crBoundary', q['crBoundary'], lo, f'largest c with P(X<=c)<={a_txt}')
        in_cr = lo is not None and x <= lo
        size = as_dec(dist.le(lo)) if lo is not None else Decimal(0)
        cr_text = f'X<={lo}'
    else:
        if hi is None:
            rep.fail('KEY', iid, 'crBoundary', q['crBoundary'], 'none', 'no critical region exists at this level')
        elif q['crBoundary'] != hi:
            rep.fail('KEY', iid, 'crBoundary', q['crBoundary'], hi, f'smallest c with P(X>=c)<={a_txt}')
        in_cr = hi is not None and x >= hi
        size = as_dec(dist.ge(hi)) if hi is not None else Decimal(0)
        cr_text = f'X>={hi}'
    if size > to_dec(alpha_tot):
        rep.fail('KEY', iid, 'actual significance level', str(rnd(size, 4)), f'<= {alpha_tot}')
    check_verdict(rep, iid, q, in_cr, f'x={x} against CR {cr_text}')

    # ---- p-value: tail probability on the observed side --------------------
    if td in ('lower', 'upper'):
        pdir = 'leq' if td == 'lower' else 'geq'
    else:
        pdir = 'leq' if as_dec(x) < as_dec(dist.mean()) else 'geq'
    pv = tail_prob(dist, pdir, x)
    if fmt(pv, 4) != format(D(q['pValue']), '.4f'):
        rep.fail('KEY', iid, 'pValue', q['pValue'], fmt(pv, 4), f'P(X {"<=" if pdir == "leq" else ">="} {x})')
    want_expr = f'P(X \\{pdir} {x}) = {fmt(pv, 4)}'
    if q['pValueExpr'] != want_expr:
        rep.fail('KEY', iid, 'pValueExpr', q['pValueExpr'], want_expr,
                 'the game renders this string through KaTeX as the hint after a wrong p-value')
    check_p_side(rep, iid, q, pv)

    # ---- every stated probability ------------------------------------------
    have = set()
    for c in q['givenCDF']:
        m = LABEL.fullmatch(c['label'])
        if not m:
            rep.fail('PROBABILITY', iid, f"givenCDF label {c['label']}", c['label'], 'P(X \\leq k) or P(X \\geq k)')
            continue
        d_, k_ = m.group(1), int(m.group(2))
        have.add((d_, k_))
        comp = fmt(tail_prob(dist, d_, k_), 4)
        if comp != c['val']:
            rep.fail('PROBABILITY', iid, f"givenCDF {c['label']}", c['val'], comp)
    for m in EXPLAIN_P.finditer(q['crExplanation']):
        d_, k_, v_ = m.group(1), int(m.group(2)), m.group(3)
        comp = fmt(tail_prob(dist, d_, k_), 4)
        if comp != v_:
            rep.fail('PROBABILITY', iid, f'crExplanation P(X \\{d_} {k_})', v_, comp)
    for m in EXPLAIN_CMP.finditer(q['crExplanation']):
        a_, op, b_ = D(m.group(1)), m.group(2), D(m.group(3))
        if not ((a_ < b_) if op == '<' else (a_ > b_)):
            rep.fail('PROBABILITY', iid, 'crExplanation comparison', m.group(0), 'true inequality')
    if not q['crExplanation'].strip() or re.search(r'assume|Need further|closest|nearest', q['crExplanation']):
        rep.fail('KEY', iid, 'crExplanation', q['crExplanation'][:70] + '...', 'a worked, finished explanation',
                 'draft prose shipped as the hint shown after a wrong answer')

    # ---- answerability: can the student find the boundary from the values shown? ----
    missing = []

    def need(d_, k_, why):
        if (d_, k_) not in have:
            missing.append(f"P(X {'<=' if d_ == 'leq' else '>='} {k_}) to {why}")

    if td in ('lower', 'two'):
        if lo is not None:
            need('leq', lo, 'confirm the lower boundary')
            need('leq', lo + 1, 'see the next value fail')
        else:
            need('leq', 0, 'see that no lower critical region exists')
    if td in ('upper', 'two') and hi is not None:
        need('geq', hi, 'confirm the upper boundary')
        if hi - 1 >= 0:
            need('geq', hi - 1, 'see the next value fail')
    need(pdir, x, 'find the p-value')
    if missing:
        if CALC_LINE.search(q['scenario']):
            rep.warn(iid, 'not shown, calculator line present: ' + '; '.join(missing))
        else:
            rep.fail('GIVENS', iid, 'givenCDF', 'absent: ' + '; '.join(missing), 'shown, or a calculator line',
                     "the student cannot derive these from the values displayed; show them, or tell the "
                     "student to use their calculator's distribution functions (Jon's ruling, 30 Sep 2026)")

    if verbose:
        print(f'  {iid:4} {mode:8} {q["tail"]}-tail {q["sig"]:>2}%  CR {cr_text:18} '
              f'actual size {fmt(size, 4)}  tail p {fmt(pv, 4)}  x={x}  {"REJECT" if in_cr else "do not reject"}')
    return in_cr, pv


# --------------------------------------------------------------------------
#  Normal (z-test)
# --------------------------------------------------------------------------
ND = NormalDist()
Q_ONE = {1: 0.99, 5: 0.95, 10: 0.90}
Q_TWO = {1: 0.995, 5: 0.975, 10: 0.95}


def z_exact(q):
    with localcontext() as c:
        c.prec = PREC
        return (D(q['xbar']) - D(q['mu0'])) * Decimal(q['n']).sqrt() / D(q['sigma'])


def normal_cv(q):
    return ND.inv_cdf(Q_TWO[q['sig']] if q['tailDir'] == 'two' else Q_ONE[q['sig']])


def normal_tail(q):
    """(direction, probability) of the tail the p-value lives in, from the exact z."""
    z = float(z_exact(q))
    d = q['tailDir']
    side = 'leq' if d == 'lower' or (d == 'two' and z < 0) else 'geq'
    p = ND.cdf(z) if side == 'leq' else 1 - ND.cdf(z)
    return side, Decimal(repr(p))


def normal_fields(q):
    """The canonical pValue / pValueExpr / crExplanation for a Normal item. The game's
    text was generated from this function (30 Sep 2026), so any drift fails here."""
    side, p = normal_tail(q)
    cv = fmt(Decimal(repr(normal_cv(q))), 4)
    sig, td = q['sig'], q['tailDir']
    if td == 'lower':
        ex = f'P(Z \\leq -{cv}) = {ALPHA_TXT[sig]} \\text{{, so the critical region is }} Z \\leq -{cv}'
    elif td == 'upper':
        ex = f'P(Z \\geq {cv}) = {ALPHA_TXT[sig]} \\text{{, so the critical region is }} Z \\geq {cv}'
    else:
        ex = f'P(Z \\geq {cv}) = {HALF_TXT[sig]} \\text{{ in each tail, so the critical region is }} |Z| \\geq {cv}'
    return {
        'pValue': fmt(p, 4),
        'pValueExpr': f"P(\\bar{{X}} \\{side} {js_num(q['xbar'])}) = {fmt(p, 4)}",
        'crExplanation': ex,
    }


def check_new_fields(rep, iid, q, want):
    for f, w in want.items():
        got = q.get(f)
        if got is None:
            rep.fail('KEY', iid, f, 'missing', w, 'the game shows "undefined" to the student')
        elif f == 'pValue':
            if format(D(got), '.4f') != w:
                rep.fail('KEY', iid, f, got, w)
        elif got != w:
            rep.fail('KEY', iid, f, got, w)


def check_normal(rep, q, verbose):
    iid, td = q['id'], q['tailDir']
    mu, sg, n, xb = D(q['mu0']), D(q['sigma']), q['n'], D(q['xbar'])
    z = z_exact(q)
    for key in ('mu0', 'sigma', 'n', 'xbar'):
        if not num_present(q['scenario'], q[key]):
            rep.fail('SCENARIO', iid, key, q[key], 'not in scenario text')
    check_h(rep, iid, q, '\\mu', q['mu0'], td)
    want_dist = f"\\bar{{X}} \\sim N\\!\\left({q['mu0']},\\, \\frac{{{q['sigma']}^2}}{{{n}}}\\right)"
    if norm(q['distStatement']) != norm(want_dist):
        rep.fail('KEY', iid, 'distStatement', q['distStatement'], want_dist)
    if abs(D(q['zStat']) - z) >= Decimal('0.00005'):
        rep.fail('KEY', iid, 'zStat', q['zStat'], fmt(z, 4))
    if q['zStatExact'] != fmt(z, 2):
        rep.fail('KEY', iid, 'zStatExact', q['zStatExact'], fmt(z, 2))
    m = re.search(r'\\frac\{(?P<a>[\d.]+) - (?P<b>[\d.]+)\}\{(?P<s>[\d.]+)/\\sqrt\{(?P<n>\d+)\}\} = '
                  r'\\frac\{(?P<num>-?[\d.]+)\}\{(?P<den>[\d.]+)\} = (?P<z>-?[\d.]+)$', q['zFormula'])
    if not m:
        rep.fail('KEY', iid, 'zFormula', q['zFormula'], 'z = (xbar - mu)/(sigma/sqrt n) = num/den = z')
    else:
        g = m.groupdict()
        if D(g['a']) != xb or D(g['b']) != mu or D(g['s']) != sg or int(g['n']) != n:
            rep.fail('KEY', iid, 'zFormula inputs', q['zFormula'], f'{xb} - {mu} over {sg}/sqrt({n})')
        with localcontext() as c:
            c.prec = PREC
            se = sg / Decimal(n).sqrt()
        if D(g['num']) != xb - mu:
            rep.fail('KEY', iid, 'zFormula numerator', g['num'], str(xb - mu))
        dp = len(g['den'].split('.')[1]) if '.' in g['den'] else 0
        if g['den'] != fmt(se, dp):
            rep.fail('KEY', iid, 'zFormula denominator', g['den'], fmt(se, dp))
        if g['z'] != fmt(z, 2):
            rep.fail('KEY', iid, 'zFormula result', g['z'], fmt(z, 2))

    for name, table, src in (('cvOneTail', q['cvOneTail'], Q_ONE), ('cvTwoTail', q['cvTwoTail'], Q_TWO)):
        for k, p in src.items():
            comp = fmt(Decimal(repr(ND.inv_cdf(p))), 4)
            stated = table.get(str(k))
            if stated is None or format(D(stated), '.4f') != comp:
                rep.fail('CRITICAL', iid, f'{name}[{k}]', stated, comp)
    cv_x = normal_cv(q)
    cv_s = fmt(Decimal(repr(cv_x)), 4)
    if td == 'two':
        want_st, in_cr = f'|Z| \\geq {cv_s}', abs(float(z)) >= cv_x
    elif td == 'lower':
        want_st, in_cr = f'Z \\leq -{cv_s}', float(z) <= -cv_x
    else:
        want_st, in_cr = f'Z \\geq {cv_s}', float(z) >= cv_x
    if norm(q['crStatement']) != norm(want_st):
        rep.fail('CRITICAL', iid, 'crStatement', q['crStatement'], want_st)
    if abs(abs(float(z)) - cv_x) < 5e-3:
        rep.fail('AMBIGUOUS', iid, 'z vs critical value', fmt(z, 4), cv_s, 'within rounding of the boundary')
    check_verdict(rep, iid, q, in_cr, f'z={fmt(z, 4)} against {want_st}')
    check_new_fields(rep, iid, q, normal_fields(q))
    _, p = normal_tail(q)
    check_p_side(rep, iid, q, p)
    if verbose:
        print(f'  {iid:4} normal   {q["tail"]}-tail {q["sig"]:>2}%  z={fmt(z, 4):>8}  {want_st:16} '
              f'tail p {fmt(p, 4)}  {"REJECT" if in_cr else "do not reject"}')
    return in_cr, p


# --------------------------------------------------------------------------
#  correlation
# --------------------------------------------------------------------------
def booklet_selfcheck(rep):
    """Exact computation must reproduce the transcribed booklet rows; if it ever does
    not, one of the two is wrong and the game cannot be checked against either."""
    for n, row in BOOKLET.items():
        for a, b in zip(BOOKLET_TWO_TAIL, row):
            c = r_cv_txt(n, a / 100)
            if c != b:
                rep.fail('CRITICAL', f'BOOKLET[{n}]', f'{a}% two-tail', b, c, 'booklet and exact computation disagree')


def booklet_cv(n, alpha_two_pct):
    return BOOKLET[n][BOOKLET_TWO_TAIL.index(alpha_two_pct)] if n in BOOKLET else None


def corr_alpha_two(q):
    """Two-tail column the item reads: a one-tail test at s% reads the 2s% two-tail column."""
    return q['sig'] if q['tailDir'] == 'two' else 2 * q['sig']


def corr_tail(q):
    """(side, p-value). Two-tailed: the two-sided p-value P(|R| >= |r|), as the exam prints it."""
    n, r, td = q['nSample'], q['r'], q['tailDir']
    if td == 'two':
        return 'abs', Decimal(repr(r_two_tail_p(n, abs(r))))
    side = 'leq' if td == 'lower' else 'geq'
    return side, Decimal(repr(r_two_tail_p(n, abs(r)) / 2))


def corr_fields(q):
    """Canonical pValue / pValueExpr / crExplanation for a correlation item."""
    n, sig, td = q['nSample'], q['sig'], q['tailDir']
    side, p = corr_tail(q)
    cv = r_cv_txt(n, corr_alpha_two(q) / 100)
    region = {'two': f'|r| \\geq {cv}', 'upper': f'r \\geq {cv}', 'lower': f'r \\leq -{cv}'}[td]
    tl = 'two' if td == 'two' else 'one'
    return {
        'pValue': fmt(p, 4),
        'pValueExpr': (f"P(|R| \\geq {js_num(abs(q['r']))}) = {fmt(p, 4)}" if side == 'abs'
                       else f"P(R \\{side} {js_num(q['r'])}) = {fmt(p, 4)}"),
        'crExplanation': f'n = {n},\\ {sig}\\% \\text{{ {tl}-tailed: critical value }} {cv} '
                         f'\\text{{, so the critical region is }} {region}',
    }


def check_corr_table(rep, table):
    for n_s, row in sorted(table.items(), key=lambda kv: int(kv[0])):
        n = int(n_s)
        for sig in (5, 1):
            for key, a2 in (('two', sig), ('one', 2 * sig)):
                comp = r_cv_txt(n, a2 / 100)
                got = row[str(sig)][key]
                if format(D(got), '.4f') != comp:
                    rep.fail('CRITICAL', f'CORR_CV[{n}]', f'{sig}% {key}-tail', got, comp)
                bk = booklet_cv(n, a2)
                if bk is None:
                    rep.fail('CRITICAL', f'CORR_CV[{n}]', 'booklet row', 'absent', f'Table 8 row n={n}',
                             'transcribe the row into BOOKLET before the game uses this n')
                elif format(D(got), '.4f') != bk:
                    rep.fail('CRITICAL', f'CORR_CV[{n}]', f'{sig}% {key}-tail vs booklet', got, bk)
        got10 = row['10']['two']
        if format(D(got10), '.4f') != r_cv_txt(n, 0.10):
            rep.fail('CRITICAL', f'CORR_CV[{n}]', '10% two-tail', got10, r_cv_txt(n, 0.10))


def given_p_sentence(q, p):
    """The one sentence the scenario adds on a correlation item (Jon, 30 Sep 2026): the exam
    prints a PMCC p-value in the question, because a student cannot find one."""
    return f' The p-value for this test is {fmt(p, 4)}.'


def check_given_p(rep, iid, q, p, ui):
    if ui is None:
        return
    want = given_p_sentence(q, p)
    if want not in ui['scenarioHtml']:
        got = re.search(r'The (p-value|probability in the tail) for this test is [\d.]+\.', ui['scenarioHtml'])
        rep.fail('KEY', iid, 'scenario p-value', got.group(0) if got else 'absent', want.strip(),
                 'the p-value route needs the value the exam would print')
    if fmt(p, 4) not in ui['step3_pvalue'] or 'pvInput' in ui['step3_pvalue']:
        rep.fail('KEY', iid, 'Step 3 (p-value route)', 'asks for the p-value' if 'pvInput' in ui['step3_pvalue']
                 else 'does not show it', f'shows the given {fmt(p, 4)}')


def check_corr(rep, q, table, verbose, ui=None):
    iid, td, n, r, sig = q['id'], q['tailDir'], q['nSample'], q['r'], q['sig']
    if not num_present(q['scenario'], n):
        rep.fail('SCENARIO', iid, 'n', n, 'not in scenario text')
    if norm(q['h0Latex']) != norm('\\rho = 0'):
        rep.fail('KEY', iid, 'h0Latex', q['h0Latex'], '\\rho = 0')
    op = {'lower': '<', 'upper': '>', 'two': '\\neq'}[td]
    if norm(q['h1Latex']) != norm(f'\\rho {op} 0'):
        rep.fail('KEY', iid, 'h1Latex', q['h1Latex'], f'\\rho {op} 0')
    a2 = corr_alpha_two(q)
    cv = r_critical(n, a2 / 100)
    cv_s = r_cv_txt(n, a2 / 100)
    if format(D(q['criticalValue']), '.4f') != cv_s:
        rep.fail('CRITICAL', iid, 'criticalValue', q['criticalValue'], cv_s, f'{sig}% {"two" if td == "two" else "one"}-tail, n={n}')
    bk = booklet_cv(n, a2)
    if bk is None:
        rep.fail('CRITICAL', iid, 'booklet row', 'absent', f'Table 8 row n={n}')
    elif format(D(q['criticalValue']), '.4f') != bk:
        rep.fail('CRITICAL', iid, 'criticalValue vs booklet', q['criticalValue'], bk)
    shown = table.get(str(n), {}).get(str(sig), {}).get('two' if td == 'two' else 'one')
    if shown is None:
        rep.fail('CRITICAL', iid, 'PMCC table shown to the student', 'null', cv_s,
                 f'no {sig}% {"two" if td == "two" else "one"}-tail entry for n={n}')
    elif D(shown) != D(q['criticalValue']):
        rep.fail('CRITICAL', iid, 'criticalValue vs PMCC table shown', q['criticalValue'], shown)
    in_cr = abs(r) >= cv if td == 'two' else (r >= cv if td == 'upper' else r <= -cv)
    if abs(abs(r) - cv) < 5e-4:
        rep.fail('AMBIGUOUS', iid, 'r vs critical value', r, cv_s, 'within rounding of the boundary')
    check_verdict(rep, iid, q, in_cr, f'r={r} against critical value {cv_s}')
    check_new_fields(rep, iid, q, corr_fields(q))
    _, p = corr_tail(q)
    check_p_side(rep, iid, q, p)
    check_given_p(rep, iid, q, p, ui)
    if verbose:
        print(f'  {iid:4} corr     {q["tail"]}-tail {sig:>2}%  n={n:<3} r={r:>6}  cv={cv_s}  tail p {fmt(p, 4)}  '
              f'{"REJECT" if in_cr else "do not reject"}')
    return in_cr, p


# --------------------------------------------------------------------------
#  driver
# --------------------------------------------------------------------------
def verify(data, verbose=False):
    rep = Report()
    booklet_selfcheck(rep)
    Q, C, wrong, ui = data['Q'], data['C'], data['wrong'], data.get('ui', {})
    for mode, items in Q.items():
        if verbose:
            print(f'[{mode}] {len(items)} items')
        for q in items:
            check_common(rep, mode, q, wrong)
            if mode in ('binomial', 'poisson'):
                in_cr, p = check_discrete(rep, mode, q, verbose)
            elif mode == 'normal':
                in_cr, p = check_normal(rep, q, verbose)
            elif mode == 'correlation':
                in_cr, p = check_corr(rep, q, C, verbose, ui.get(q['id']))
            else:
                rep.fail('STRUCTURE', q['id'], 'mode', mode, 'binomial|poisson|normal|correlation')
                continue
            check_ui(rep, q['id'], q, ui.get(q['id']), p, in_cr)
    check_corr_table(rep, C)
    return rep


def item_counts(data):
    return {m: len(v) for m, v in data['Q'].items()}


def failing_items(rep):
    return sorted({f[1] for f in rep.fails if not f[1].startswith(('CORR_CV', 'BOOKLET'))})


def print_report(rep, data):
    total = sum(item_counts(data).values())
    order = ('KEY', 'CRITICAL', 'PROBABILITY', 'DISTRACTOR', 'SHUFFLE', 'GIVENS', 'SCENARIO', 'STRUCTURE', 'AMBIGUOUS')
    for cat in order:
        for cat_, iid, field, stated, computed, why in rep.fails:
            if cat_ == cat:
                print(f'FAIL [{cat_}] {iid} {field}: stated {stated!r}, computed {computed!r}' + (f'  -- {why}' if why else ''))
    for iid, msg in rep.warns:
        print(f'WARN {iid}: {msg}')
    bad = failing_items(rep)
    print(f'\n{total} items ({", ".join(f"{m} {c}" for m, c in item_counts(data).items())}); '
          f'{len(bad)} with at least one FAIL, {len(rep.fails)} FAILs, {len(rep.warns)} WARNs')
    if bad:
        print('items failing: ' + ', '.join(bad))
    print('PASS' if not rep.fails else 'FAIL')


# --------------------------------------------------------------------------
#  fault injection -- every invocation; an injected fault that is NOT caught aborts the run
# --------------------------------------------------------------------------
def find(data, iid):
    for items in data['Q'].values():
        for q in items:
            if q['id'] == iid:
                return q
    raise KeyError(iid)


SELFTEST_ITEMS = ('B1', 'B2', 'P1', 'P2', 'N1', 'C1')

FAULTS = [
    # (item, description, mutation(data, item), field that must be reported)
    ('B1', 'critical value moved by one', lambda d, q: q.__setitem__('crBoundary', q['crBoundary'] + 1), 'crBoundary'),
    ('P1', 'critical value moved by one', lambda d, q: q.__setitem__('crBoundary', q['crBoundary'] + 1), 'crBoundary'),
    ('B1', 'a displayed probability changed', lambda d, q: q['givenCDF'][0].__setitem__('val', '0.0353'), 'givenCDF'),
    ('P2', 'a displayed probability changed', lambda d, q: q['givenCDF'][1].__setitem__('val', '0.0319'), 'givenCDF'),
    ('P2', 'verdict flipped (inCR and reject)', lambda d, q: (q.__setitem__('inCR', False), q.__setitem__('reject', False)), 'inCR'),
    ('B2', 'reject flipped alone', lambda d, q: q.__setitem__('reject', False), 'reject'),
    ('B1', 'p-value changed', lambda d, q: q.__setitem__('pValue', 0.1771), 'pValue'),
    ('N1', 'a normal critical value changed', lambda d, q: q['cvOneTail'].__setitem__('5', 1.7449), 'cvOneTail[5]'),
    ('N1', 'the z statistic changed', lambda d, q: q.__setitem__('zStatExact', '-1.00'), 'zStatExact'),
    ('N1', 'a normal p-value changed', lambda d, q: q.__setitem__('pValue', 0.0328), 'pValue'),
    ('N1', 'a normal explanation removed', lambda d, q: q.pop('crExplanation'), 'crExplanation'),
    ('C1', 'a correlation critical value changed', lambda d, q: q.__setitem__('criticalValue', 0.5240), 'criticalValue'),
    ('C1', 'a correlation p-value changed', lambda d, q: q.__setitem__('pValue', 0.0217), 'pValue'),
    ('B1', 'a distractor repeats the correct hypothesis', lambda d, q: q['h0Distractors'].__setitem__(1, 'p = 0.20'), 'h0Distractors[1]'),
    ('B2', 'Step 6 marks "reject the claim" correct', lambda d, q: d['ui']['B2'].__setitem__('compB', '...reject the claim that...'), 'Step 6 action'),
    ('P2', 'Step 6 shows the correct conclusion twice',
     lambda d, q: d['ui']['P2']['compCOptions'].append(q['conclusionContext']), 'Step 6 context options'),
    ('C1', 'the scenario states the wrong p-value', lambda d, q: d['ui']['C1'].__setitem__(
        'scenarioHtml', d['ui']['C1']['scenarioHtml'].replace(f"{q['pValue']:.4f}", '0.9999')), 'scenario p-value'),
    ('P2', 'Step 4 compares with the wrong side', lambda d, q: d['ui']['P2'].__setitem__(
        'step4_pvalue', 'The p-value is not less than the significance level (5%)'), 'Step 4 (p-value)'),
]


def selftest(data, page):
    for iid in SELFTEST_ITEMS:
        q = find(data, iid)
        mode = next(m for m, items in data['Q'].items() if q in items)
        rep = verify({'Q': {mode: [q]}, 'C': data['C'], 'wrong': data['wrong'], 'ui': data.get('ui', {})})
        real = [f for f in rep.fails if f[1] == iid]
        if real:
            sys.exit(f'self-test item {iid} is not clean on this bank ({real[0][2]}); choose another fixture')
    ok = True
    for iid, desc, mutate, field in FAULTS:
        bank = copy.deepcopy(data)
        mutate(bank, find(bank, iid))
        hit = [f for f in verify(bank).fails if f[1] == iid and field in f[2]]
        print(f'  fault injection {iid:3} {desc:46} -> {"caught" if hit else "MISSED"}')
        ok &= bool(hit)
    bank = copy.deepcopy(data)
    bank['C']['15']['5']['two'] = 0.5240
    hit = [f for f in verify(bank).fails if f[1] == 'CORR_CV[15]']
    print(f'  fault injection PMCC table entry changed{" " * 24}-> {"caught" if hit else "MISSED"}')
    ok &= bool(hit)
    # a code-level fault: the game's own page, with an options builder that does not shuffle
    rep = verify(load_bank(page, unshuffled=True))
    hit = {f[2] for f in rep.fails if f[0] == 'SHUFFLE'}
    need = {'Step 6 evidence position', 'Step 6 action position', 'Step 6 context position'}
    print(f'  fault injection unshuffled Step 6 build{" " * 25}-> {"caught" if need <= hit else "MISSED"}'
          f' ({sum(1 for f in rep.fails if f[0] == "SHUFFLE")} position FAILs)')
    return ok and need <= hit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', default=PAGE)
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()

    data = load_bank(args.file)
    if not args.no_selftest:
        print('self-test (fault injection on an in-memory copy of the bank):')
        if not selftest(data, args.file):
            sys.exit('SELF-TEST FAILED: the verifier missed an injected fault, so its PASS cannot be trusted')
        print()
    rep = verify(data, args.verbose)
    print_report(rep, data)
    sys.exit(1 if rep.fails else 0)


if __name__ == '__main__':
    main()
