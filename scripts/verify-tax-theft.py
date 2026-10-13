#!/usr/bin/env python3
# ci-line: Tax Theft (every key recomputed from HMRC 2025/26 + money-answer format check) |
"""Independent verification of tax-theft (todo START item 4; canon §7.1.3).

Every key is recomputed here from HMRC's 2025/26 rules, never asked of the game:

  - personal allowance £12,570, reduced by £1 for every £2 of income over £100,000
    (zero at £125,140 and above);
  - income tax on TAXABLE income (salary minus the allowance): 20% on the first £37,700,
    40% up to £125,140, 45% above. The basic band does not widen when the allowance
    tapers (the game used to stretch it to a gross £50,270, under-taxing every salary
    over £100,000 by £500 to £2,514);
  - Class 1 employee NI on gross pay: 8% from £12,570 to £50,270, 2% above;
  - deductions = tax + NI; net monthly = (gross - deductions) / 12 to the nearest
    penny, half up.

Sources (checked 3 Oct 2026):
  https://www.gov.uk/government/publications/rates-and-allowances-income-tax/income-tax-rates-and-allowances-current-and-past
  https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2025-to-2026
  https://www.gov.uk/income-tax-rates/income-over-100000

Then every salary is PLAYED in the page (the salary is chosen by seeding the game's own
shuffle queue; nothing else is set). At every step:

  - the step's wording: the net step asks for the nearest penny; a medium/hard tax step
    teaches the band width on taxable income (the first £37,700);
  - the money-answer standard: the right amount wrongly written (1 d.p., 3 d.p., or
    "3050.0" for a whole-pound key) gets the format message with the student's own
    figure, and is neither marked nor recorded (no analytics event, score unchanged,
    the step does not advance); the right amount wrongly written and then corrected is
    accepted; a wrong amount (one penny or one pound out) is marked wrong;
  - the true key typed correctly (2 d.p., or plain pounds for a whole-pound key) is
    marked correct, and the feedback, payslip and completed-step line show it in full
    money form (£30,432.00).

The income tax table is read on every salary (Jon's ruling, 13 Oct 2026): on Hard it
states the bands as taxable income (the first £37,700 of it at the basic rate, from
uk_rates.py), never the gross £50,270; on Easy and Medium, with the full allowance, as
gross income. A wrong amount gets the factor-of-12 hint only when it is a twelfth of a key
above £0 (Hard's £130,000 allowance is £0, and £1 is not "divided by 12").

At the end the payslip is annual throughout (its Net Annual Pay row shows gross minus
deductions; no row is monthly), the completion screen's figures are checked, "You Keep"
says per year, and the closing line: Easy's is Jon's line, verbatim; "lost your personal
allowance entirely" only at £125,140 and above; below that it names the reduced allowance. The salary lists are checked too: hard is exactly 106k/114k/120k/130k,
medium holds 8 distinct salaries between £50,270 and £100,000, easy stays basic rate.

A fault-injection self-test (the old gross-threshold band method, a format check that
marks instead, the old closing line, the old gross table on Hard, the monthly net row, the
factor-of-12 hint on a £0 key, the old Easy line and the unlabelled "You Keep") patches the page and must FAIL each time; it runs
unless --no-selftest, and only when the main check passes.

    python scripts/verify-tax-theft.py [--verbose] [--no-selftest]
"""
import argparse
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import uk_rates as ur  # noqa: E402  (canon §7.1.4: the one copy of the rates)

SLUG = 'tax-theft'

# The game's TAX_RULES must equal the teaching year's figures (scripts/uk_rates.py, canon §7.1.4).
# The game holds rates as JS numbers (0.2, 0.08), so the rates are compared as floats.
HMRC = dict(personalAllowance=ur.PERSONAL_ALLOWANCE, paReducesAbove=ur.PA_TAPER_FROM,
            basicRateBand=ur.BASIC_RATE_BAND, higherRateLimit=ur.HIGHER_RATE_LIMIT,
            basicRate=float(ur.BASIC_RATE), higherRate=float(ur.HIGHER_RATE),
            additionalRate=float(ur.ADDITIONAL_RATE), niPrimaryThreshold=ur.NI_PRIMARY_THRESHOLD,
            niUpperLimit=ur.NI_UPPER_EARNINGS_LIMIT, niMainRate=float(ur.NI_MAIN_RATE),
            niHigherRate=float(ur.NI_UPPER_RATE))
HARD = [106000, 114000, 120000, 130000]
EASY_LINE = 'But at least the potholes get fixed, right?'   # Jon's line, verbatim (13 Oct 2026)
TWELFTH_HINT = 'divided by 12'


def gbp(n):
    return '£{:,}'.format(n)


def tax_table(diff):
    """What the income tax table must say, and must not, from uk_rates.py (Jon's ruling, 13 Oct 2026)."""
    pa, band, top = ur.PERSONAL_ALLOWANCE, ur.BASIC_RATE_BAND, ur.HIGHER_RATE_LIMIT
    rates = ['%d%%' % (r * 100) for r in (ur.BASIC_RATE, ur.HIGHER_RATE, ur.ADDITIONAL_RATE)]
    if diff == 'hard':
        need = ['Taxable Income', '%s, less £1 for every £2 of income over %s' % (gbp(pa), gbp(ur.PA_TAPER_FROM)),
                'The first %s of taxable income' % gbp(band),
                '%s – %s of taxable income' % (gbp(band + 1), gbp(top)),
                'Taxable income over %s' % gbp(top)]
        bar = [gbp(pa + band), gbp(pa + band + 1), 'Annual Income']   # the gross bands, wrong once the allowance tapers
    else:
        need = ['Annual Income', 'Up to %s' % gbp(pa), '%s – %s' % (gbp(pa + 1), gbp(pa + band)),
                '%s – %s' % (gbp(pa + band + 1), gbp(top)), 'Over %s' % gbp(top)]
        bar = []
    return need + rates, bar
FORMAT_MSG = ('Right amount, but money always has two decimal places. In the exam, '
              '£{raw} loses the mark. Fix it and resubmit.')
TITLES = {'Reduced Personal Allowance': 'pa', 'Taxable Income': 'taxable', 'Income Tax': 'tax',
          'National Insurance': 'ni', 'Total Deductions': 'deductions', 'Net Monthly Pay': 'net'}
PAYSLIP = {'pa': 'payPA', 'taxable': 'payTaxable', 'tax': 'payTax', 'ni': 'payNI',
           'deductions': 'payDeductions', 'net': 'payNet'}


def keys(gross):
    """Every step's key as an exact Fraction of pounds, from HMRC's rules (scripts/uk_rates.py)."""
    pa = ur.personal_allowance(gross)
    taxable = ur.taxable_income(gross)
    tax = ur.income_tax(gross)
    ni = ur.employee_ni(gross)
    deductions = tax + ni
    exact = (gross - deductions) / 12
    net = Decimal(exact.numerator) / Decimal(exact.denominator)
    net = F(net.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    return dict(pa=F(pa), taxable=F(taxable), tax=tax, ni=ni, deductions=deductions, net=net,
                net_exact=exact)


def money(k):
    """Full money form: £30,432.00."""
    return '£{:,.2f}'.format(Decimal(k.numerator) / Decimal(k.denominator))


def plain(k, dp=2):
    return '{:.{}f}'.format(Decimal(k.numerator) / Decimal(k.denominator), dp)


def wrong_forms(k):
    """The right amount, wrongly written."""
    whole = k.denominator == 1
    forms = [plain(k, 3)]
    if whole:
        forms.append(plain(k, 1))
    elif (k * 100).numerator % 10 == 0:
        forms.append(plain(k, 1))         # 114.40 -> 114.4
    return forms


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, sid, what, detail):
        self.fails.append('%s %s: %s' % (sid, what, detail))


INIT = """(() => {
  const st = window.setTimeout;
  window.setTimeout = function(f, d, ...a) { return st(f, d === 800 ? 0 : d, ...a); };
})();"""

WRAP_MFG = """(() => {
  window.__mfg = [];
  const o = window.mfg;
  window.mfg = function(name) { window.__mfg.push(name); return o ? o.apply(this, arguments) : undefined; };
})()"""

STATE = """() => ({
  idx: currentStepIndex,
  title: document.getElementById('stepTitle').textContent,
  instruction: document.getElementById('stepInstruction').textContent,
  bands: document.getElementById('stepBands').style.display === 'none' ? '' : document.getElementById('stepBands').textContent,
  fbClass: document.getElementById('feedback').className,
  fbText: document.getElementById('feedback').textContent,
  input: document.getElementById('stepInput').value,
  events: window.__mfg.length,
  correct: _ttCorrectCount,
  done: document.getElementById('completionScreen').style.display === 'block',
  completed: Array.from(document.querySelectorAll('#completedSteps .completed-step')).map(e => e.textContent)
})"""


def submit(page, raw):
    """Enter raw, press Check, and read the result, all in one page task, so the
    (shortened) advance timer can neither redraw the step nor clear the input between
    them. The input is type="number": a valid number string is kept exactly as typed."""
    return page.evaluate('(raw) => { document.getElementById("stepInput").value = raw;'
                         ' checkAnswer(); return (' + STATE + ')(); }', raw)


def wait_advance(page, idx):
    page.wait_for_function('(i) => currentStepIndex > i || '
                           'document.getElementById("completionScreen").style.display === "block"',
                           arg=idx, timeout=5000)


def play(page, rep, diff, gross, verbose=False, probes=True):
    sid = '%s %d' % (diff, gross) + ('' if probes else ' [keys]')
    k = keys(gross)
    page.evaluate('([d, g]) => { usedSalaries[d] = [g]; startGame(d); }', [diff, gross])
    table = page.evaluate("document.getElementById('taxTable').textContent")
    need, bar = tax_table(diff)
    for t in need:
        if t not in table:
            rep.fail(sid, 'tax table', 'does not say %r: %r' % (t, table[:200]))
    for t in bar:
        if t in table:
            rep.fail(sid, 'tax table', 'states the gross band %r on Hard, where the bands are taxable income' % t)
    want_steps = 6 if diff == 'hard' else 5
    n = page.evaluate('steps.length')
    if n != want_steps:
        rep.fail(sid, 'steps', 'has %d steps, expected %d' % (n, want_steps))
    for i in range(n):
        s = page.evaluate(STATE)
        if s['done'] or s['idx'] != i:
            rep.fail(sid, 'flow', 'expected step %d, game is at %s' % (i, 'the end' if s['done'] else s['idx']))
            return
        sk = TITLES.get(s['title'])
        if sk is None:
            rep.fail(sid, 'step %d' % i, 'unknown step title %r' % s['title'])
            return
        key = k[sk]
        where = '%s (%s)' % (sid, sk)
        # Wording
        penny = 'Give your answer to the nearest penny.'
        needs_rounding = sk == 'net' and k['net_exact'] != k['net']
        if sk == 'net' and penny not in s['instruction']:
            rep.fail(where, 'wording', 'the net step does not say %r' % penny)
        if needs_rounding and penny not in s['instruction']:
            rep.fail(where, 'wording', 'needs rounding but does not say %r' % penny)
        if sk == 'tax' and diff != 'easy':
            if 'first £37,700 of taxable income' not in s['bands']:
                rep.fail(where, 'band method', 'bands do not teach the first £37,700 of taxable income: %r' % s['bands'][:160])
            if 'taxable income' not in s['instruction']:
                rep.fail(where, 'band method', 'instruction does not say the bands apply to taxable income: %r' % s['instruction'])
        # Format check: right amount, wrongly written
        for raw in (wrong_forms(key) if probes else []):
            before = page.evaluate(STATE)
            after = submit(page, raw)
            if after['idx'] != i or after['done']:
                rep.fail(where, 'format', '%s (right amount, wrong form) was accepted as correct' % raw)
                return
            if after['fbText'] != FORMAT_MSG.format(raw=raw) or 'format' not in after['fbClass']:
                rep.fail(where, 'format', '%s gave %r [%s], not the format message' % (raw, after['fbText'][:100], after['fbClass']))
            if after['events'] != before['events'] or after['correct'] != before['correct']:
                rep.fail(where, 'format', '%s was recorded (events %d->%d)' % (raw, before['events'], after['events']))
        # Wrong amounts: a penny out, and a pound out
        for delta in ((F(1, 100), F(1)) if probes else ()):
            raw = plain(key + delta)
            after = submit(page, raw)
            if after['idx'] != i or after['done']:
                rep.fail(where, 'wrong', '%s (key %s) was accepted' % (raw, plain(key)))
                return
            if 'wrong' not in after['fbClass']:
                rep.fail(where, 'wrong', '%s was not marked wrong: %r' % (raw, after['fbText'][:100]))
            if TWELFTH_HINT in after['fbText'] and not (key > 0 and abs(key + delta - key / 12) <= 2):
                rep.fail(where, 'hint', '%s (key %s) got the factor-of-12 hint: %r' % (raw, plain(key), after['fbText'][:100]))
        # The right answer, rightly written
        raw = str(key.numerator) if (key.denominator == 1 and i % 2 == 0) else plain(key)
        after = submit(page, raw)
        if 'correct' not in after['fbClass'] or after['fbText'] != 'Correct — ' + money(key):
            rep.fail(where, 'key', 'typed %s (HMRC); the game said %r' % (raw, after['fbText'][:100]))
            if probes:
                return
            if 'correct' not in after['fbClass']:
                # Keys pass only: the key is already failed; type the game's own figure
                # purely to reach the later steps and the closing line.
                own = page.evaluate('(() => { const s = steps[currentStepIndex];'
                                    ' return s.key !== undefined ? (s.key / 100).toFixed(2) : String(Math.round(s.expected)); })()')
                if 'correct' not in submit(page, own)['fbClass']:
                    return
        wait_advance(page, i)
        shown = page.evaluate('(id) => document.getElementById(id).textContent', PAYSLIP[sk])
        # The payslip is annual: its net row is the year's net pay (Jon's ruling, 13 Oct 2026)
        want = ('−' if sk in ('tax', 'ni', 'deductions') else '') + money(gross - k['deductions'] if sk == 'net' else key)
        if shown != want:
            rep.fail(where, 'payslip', 'shows %r, expected %r' % (shown, want))
        line = page.evaluate(STATE)['completed'][-1]
        if not line.endswith(money(key)):
            rep.fail(where, 'completed step', '%r does not end in %s' % (line, money(key)))
        if verbose:
            print('  %-24s %-11s %s' % (sid, sk, money(key)))
    page.wait_for_function('document.getElementById("completionScreen").style.display === "block"', timeout=5000)
    end = page.evaluate("""() => ({tax: sumTax.textContent, ni: sumNI.textContent,
        keep: sumKeep.textContent, wry: wryLine.textContent,
        keepLabel: sumKeep.parentElement.querySelector('.stat-label').textContent,
        rows: Array.from(document.querySelectorAll('.payslip-row .label')).map(e => e.textContent),
        period: Array.from(document.querySelectorAll('.payslip-meta dt')).find(d => d.textContent === 'Period').nextElementSibling.textContent})""")
    if end['period'] != 'Annual' or any('month' in r.lower() for r in end['rows']) or 'Net Annual Pay' not in end['rows']:
        rep.fail(sid, 'payslip', 'not annual throughout: period %r, rows %r' % (end['period'], end['rows']))
    if 'per year' not in end['keepLabel'].lower():
        rep.fail(sid, 'completion keep', '"You Keep" is not labelled per year: %r' % end['keepLabel'])
    if diff == 'easy' and end['wry'] != EASY_LINE:
        rep.fail(sid, 'closing line', '%r, not Jon\'s line %r' % (end['wry'], EASY_LINE))
    for name, want in (('tax', money(k['tax'])), ('ni', money(k['ni'])),
                       ('keep', money(gross - k['deductions']))):
        if end[name] != want:
            rep.fail(sid, 'completion ' + name, 'shows %r, expected %r' % (end[name], want))
    if diff == 'hard':
        entirely = 'lost your personal allowance entirely' in end['wry']
        if gross >= 125140 and not entirely:
            rep.fail(sid, 'allowance line', 'PA is zero but the line says %r' % end['wry'])
        if gross < 125140 and (entirely or 'reduced' not in end['wry'] or money(k['pa']) not in end['wry']):
            rep.fail(sid, 'allowance line', 'PA is reduced to %s but the line says %r' % (money(k['pa']), end['wry']))


def check_params(rep, sal, rules, year):
    if sal['hard'] != HARD:
        rep.fail('salaries', 'hard', '%r, expected %r (hard is not to change)' % (sal['hard'], HARD))
    med = sal['medium']
    if len(med) != 8 or len(set(med)) != 8:
        rep.fail('salaries', 'medium', 'expected 8 distinct salaries: %r' % med)
    for g in med:
        if not 50270 < g < 100000:
            rep.fail('salaries', 'medium %d' % g, 'outside medium (higher rate, full allowance: £50,271 to £99,999)')
    for g in sal['easy']:
        if not 12570 < g <= 50270:
            rep.fail('salaries', 'easy %d' % g, 'not a basic-rate salary')
    for name, v in HMRC.items():
        if rules.get(name) != v:
            rep.fail('TAX_RULES', name, '%r, HMRC %s is %r' % (rules.get(name), ur.TEACHING_YEAR, v))
    if rules.get('taxYear') != ur.TEACHING_YEAR or year != ur.TEACHING_YEAR:
        rep.fail('tax year', 'stated', 'game says %r / payslip %r, expected %s'
                 % (rules.get('taxYear'), year, ur.TEACHING_YEAR))


def run(patch_js=None, only=None, verbose=False):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    rep = Report()
    played = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context()
            ctx.add_init_script(INIT)
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof SALARIES !== "undefined" && typeof startGame === "function"', timeout=8000)
            page.evaluate(WRAP_MFG)
            if patch_js:
                page.evaluate(patch_js)
            sal = page.evaluate('JSON.parse(JSON.stringify(SALARIES))')
            rules = page.evaluate('JSON.parse(JSON.stringify(TAX_RULES))')
            year = page.evaluate("Array.from(document.querySelectorAll('.payslip-meta dt')).find(d => d.textContent === 'Tax Year').nextElementSibling.textContent")
            if only is None:
                check_params(rep, sal, rules, year)
            for diff in ('easy', 'medium', 'hard'):
                for g in sal[diff]:
                    if only and (diff, g) not in only:
                        continue
                    # Keys pass first (only the HMRC answer is typed), so a game that
                    # fails a probe still has every key, wording and closing line checked
                    play(page, rep, diff, g, False, probes=False)
                    play(page, rep, diff, g, verbose)
                    played += 1
            browser.close()
            if errors:
                rep.fail('page', 'errors', '; '.join(errors[:5]))
    finally:
        proc.terminate()
        proc.wait()
    return rep, played


def selftest():
    lines, ok = [], True
    one = [('hard', 106000)]

    def expect(name, patch, only=one):
        nonlocal ok
        rep, _ = run(patch, only=only)
        caught = bool(rep.fails)
        ok = ok and caught
        lines.append('  self-test %-40s %s' % (name, ('caught: ' + rep.fails[0][:110]) if caught else '*** MISSED ***'))

    expect('gross-threshold band method', """(() => { const real = computeKeys;
        computeKeys = function(g) { const k = real(g);
          const pa = getPA(g); k.tax = (50270 - pa) * 20 + (Math.min(g, 125140) - 50270) * 40 + Math.max(0, g - 125140) * 45;
          k.deductions = k.tax + k.ni; k.net = Math.floor((g * 100 - k.deductions + 6) / 12); return k; }; })()""")
    expect('format check marks instead', """(() => { const real = moneyResult;
        moneyResult = function(raw, key) { const r = real(raw, key); return r === 'format' ? 'correct' : r; }; })()""")
    expect('old closing line for a reduced allowance', "WRY_LINES.hardReduced = WRY_LINES.hard")
    expect('the gross tax table on Hard', "(() => { renderTaxTable = (function (r) { return function () { r('easy'); }; })(renderTaxTable); })()")
    expect('the payslip\'s monthly net row', """(() => { const real = checkAnswer;
        document.getElementById('payNet').previousElementSibling.textContent = 'Net Monthly Pay';
        checkAnswer = function () { const s = steps[currentStepIndex]; real();
          if (s.id === 'net' && document.getElementById('feedback').className.indexOf('correct') >= 0)
            document.getElementById('payNet').textContent = fmtPence(s.key); }; })()""")
    expect('the factor-of-12 hint on a £0 key', """(() => { getHint = (function (real) { return function (v, e, s) {
        if (s.id !== 'net' && Math.abs(v - e / 12) <= 2) return 'Have you accidentally divided by 12? Work in annual figures first.';
        return real(v, e, s); }; })(getHint); })()""", only=[('hard', 130000)])
    expect('the old Easy closing line', "WRY_LINES.easy = 'Welcome to adulthood.'", only=[('easy', 14000)])
    expect('"You Keep" with no period', "sumKeep.parentElement.querySelector('.stat-label').textContent = 'You Keep'")
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    rep, played = run(verbose=args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        if ok:
            s_ok, lines = selftest()
            print('\nFault-injection self-test (patched page; the file is never touched):')
            for ln in lines:
                print(ln)
            ok = ok and s_ok
        else:
            print('\nFault-injection self-test skipped: the main check failed.')
    bad = {f.split(' ')[1] for f in rep.fails if f.split(' ')[0] in ('easy', 'medium', 'hard')}
    print('\n%s: %d FAIL(s); %d of %d salaries played have a FAIL' % ('PASS' if ok else 'FAILED', len(rep.fails), len(bad), played))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
