#!/usr/bin/env python3
# ci-line: B4 | Core Maths Paper 1 tax, NI and student loan (recomputed with uk_rates) |
"""Independent verification of core-maths-paper1's income tax, NI and student loan questions (canon §7.1.4).

Until 3 Oct 2026 two of these questions charged employee NI at 12%, the rate before January
2024 (todo §1.41), and the budget question keyed "No" on numbers that left £15.50 a month spare.
Nothing checked them: every rate was typed into the stem by hand. This script recomputes each
one with scripts/uk_rates.py, the one copy of the teaching year's figures; nothing numeric is
taken from the game except what the student sees (stem, table, options, the key's position,
the working).

The items are found by what they ask, not by position, and each must be found exactly once:
  INCOME TAX  "Personal allowance £A. Income tax R% on earnings above this up to £L. A worker
              earns £S." A is the allowance, R the basic rate, L the allowance plus the basic
              band; the key is the tax on S. Each distractor is a named error (Jon, 3 Oct 2026):
                - the rate on the whole salary (forgetting the allowance);
                - the rate on the allowance itself;
                - the higher rate on the taxable income.
  NI          "NI is charged at R% on earnings between £A and £B. A worker earns £S." R, A, B
              are the main rate, primary threshold and upper earnings limit; the key is the NI on
              S. Each distractor is a named error (Jon, 3 Oct 2026), and the three are exactly:
                - the rate on the whole salary (forgetting the threshold);
                - the basic income tax rate on the earnings above the threshold (wrong rate);
                - the annual key divided by 12 (a monthly figure for an annual question).
  BUDGET      "Marcus earns £S ... income tax (R% on earnings above £A) and NI (R2% on earnings
              above £B) ... monthly budget": rates and thresholds as above; take-home per month is
              recomputed and compared with the table's total; the key must be the "No" option
              exactly when take-home is below the budget, and the working must print both.
  STUDENT LOAN "Plan P student loan repayments are R% of earnings above £T. A graduate earns £S."
              The plan must be named (todo §1.44: it was not); R and T are that plan's 2025/26
              rate and threshold; the key is the repayment on S. Each distractor is a named error:
                - the rate on the whole salary (forgetting the threshold);
                - the annual key divided by 12 (a monthly figure for an annual question);
                - "£0 — earnings below threshold" (misjudging the comparison).
Every stem in the game that names income tax or NI must print only the teaching year's rates
and thresholds. Every '=' chain in these items' working must be arithmetically true
(stats_common.arith_problems).

A fault-injection self-test (the old 12% rate, a wrong key, an unnamed distractor, the old
£300 savings line, the old £27,295 loan threshold, an unnamed plan, Q21's old £4,628) must FAIL
each time; it runs unless --no-selftest.

    python scripts/verify-core-maths-paper1-tax.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import stats_common as st  # noqa: E402
import uk_rates as ur  # noqa: E402

SLUG = 'core-maths-paper1'

MONEY = re.compile(r'£\s?(\d[\d,]*(?:\.\d+)?)')
TAX_RX = re.compile(r'Personal allowance £([\d,]+)\. Income tax (\d+(?:\.\d+)?)% on earnings above this '
                    r'up to £([\d,]+)\. A worker earns £([\d,]+)\.')
NI_RX = re.compile(r'NI is charged at (\d+(?:\.\d+)?)% on earnings between £([\d,]+) and £([\d,]+)\. '
                   r'A worker earns £([\d,]+)\. How much NI do they pay annually\?')
LOAN_RX = re.compile(r'(?:Plan (\d) )?[Ss]tudent loan repayments are (\d+(?:\.\d+)?)% of earnings above '
                     r'£([\d,]+)\. A graduate earns £([\d,]+)\.')
BUDGET_RX = re.compile(r'earns £([\d,]+) per year\. After income tax \((\d+(?:\.\d+)?)% on earnings above '
                       r'£([\d,]+)\) and NI \((\d+(?:\.\d+)?)% on earnings above £([\d,]+)\)')
TAXNI_WORDS = re.compile(r'\bincome tax\b|\bNI\b|\bnational insurance\b|\bpersonal allowance\b', re.I)
PCT_NEAR_NI = re.compile(r'\bNI\b[^.%]{0,40}?(\d+(?:\.\d+)?)%|(\d+(?:\.\d+)?)%\s+NI\b')


def num(s):
    return F(s.replace(',', ''))


def pct(s):
    return F(s) / 100


def money_value(opt):
    """The amount an option leads with: '£137.70' -> 137.70; '£0 — earnings below threshold' -> 0."""
    m = MONEY.match(opt.strip())
    return num(m.group(1)) if m else None


def penny(x):
    d = Decimal(x.numerator) / Decimal(x.denominator)
    return F(d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def gbp(x):
    return '£{:,.2f}'.format(Decimal(x.numerator) / Decimal(x.denominator))


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, where, what, detail):
        self.fails.append('%s %s: %s' % (where, what, detail))


def check_arith(rep, where, q):
    for a, b, why in st.arith_problems(q.get('working', '')):
        rep.fail(where, 'working', '%r = %r is false (%s)' % (a, b, why))


def check_key_options(rep, where, q, key):
    vals = [money_value(o) for o in q['options']]
    if None in vals:
        rep.fail(where, 'options', 'an option is not a money amount: %r' % q['options'])
        return None
    if len(set(vals)) != len(vals):
        rep.fail(where, 'options', 'two options are equal in value: %r' % q['options'])
    if vals[q['correct']] != key:
        rep.fail(where, 'key', 'keyed %s, the recomputed answer is %s' % (q['options'][q['correct']], gbp(key)))
    for i, v in enumerate(vals):
        if i != q['correct'] and v == key:
            rep.fail(where, 'distractor', '%s equals the key' % q['options'][i])
    return vals


def check_tax(rep, q):
    w = 'INCOME TAX'
    m = TAX_RX.search(q['stem'])
    a, r, lim, s = num(m.group(1)), pct(m.group(2)), num(m.group(3)), num(m.group(4))
    if a != ur.PERSONAL_ALLOWANCE:
        rep.fail(w, 'allowance', 'states £%s, %s is £%s' % (a, ur.TEACHING_YEAR, ur.PERSONAL_ALLOWANCE))
    if r != ur.BASIC_RATE:
        rep.fail(w, 'rate', 'states %s%%, the basic rate is %s%%' % (r * 100, ur.percent(ur.BASIC_RATE)))
    if lim != ur.PERSONAL_ALLOWANCE + ur.BASIC_RATE_BAND:
        rep.fail(w, 'band', 'states £%s as the top of the basic band, %s is £%s'
                 % (lim, ur.TEACHING_YEAR, ur.PERSONAL_ALLOWANCE + ur.BASIC_RATE_BAND))
    if not ur.PERSONAL_ALLOWANCE < s <= ur.PERSONAL_ALLOWANCE + ur.BASIC_RATE_BAND:
        rep.fail(w, 'salary', '£%s is not a basic-rate salary, so the stem\'s single rate is wrong' % s)
    key = ur.income_tax(s)
    vals = check_key_options(rep, w, q, key)
    if vals is not None:
        check_named(rep, w, q, vals, {
            penny(s * ur.BASIC_RATE): 'the rate on the whole salary',
            penny(ur.PERSONAL_ALLOWANCE * ur.BASIC_RATE): 'the rate on the allowance',
            penny(ur.taxable_income(s) * ur.HIGHER_RATE): 'the higher rate on the taxable income',
        })
    check_arith(rep, w, q)


def check_named(rep, w, q, vals, named):
    got = [v for i, v in enumerate(vals) if i != q['correct']]
    for v in got:
        if v not in named:
            rep.fail(w, 'distractor', '%s comes from no named error (expected %s)'
                     % (gbp(v), ', '.join('%s = %s' % (gbp(k), e) for k, e in named.items())))
    for k, e in named.items():
        if k not in got:
            rep.fail(w, 'distractor', 'missing %s (%s)' % (gbp(k), e))


def check_loan(rep, q):
    w = 'STUDENT LOAN'
    m = LOAN_RX.search(q['stem'])
    plan, r, thr, s = m.group(1), pct(m.group(2)), num(m.group(3)), num(m.group(4))
    key_plan = 'plan%s' % plan if plan else None
    if key_plan not in ur.STUDENT_LOAN_THRESHOLDS:
        rep.fail(w, 'plan', 'the stem names %s; it must name a plan with a %s threshold (%s)'
                 % ('Plan %s' % plan if plan else 'no plan', ur.TEACHING_YEAR,
                    ', '.join(sorted(ur.STUDENT_LOAN_THRESHOLDS))))
        return
    if thr != ur.STUDENT_LOAN_THRESHOLDS[key_plan]:
        rep.fail(w, 'threshold', 'states £%s, the %s Plan %s threshold is £%s'
                 % (thr, ur.TEACHING_YEAR, plan, ur.STUDENT_LOAN_THRESHOLDS[key_plan]))
    if r != ur.STUDENT_LOAN_RATES[key_plan]:
        rep.fail(w, 'rate', 'states %s%%, Plan %s is %s%%' % (r * 100, plan, ur.percent(ur.STUDENT_LOAN_RATES[key_plan])))
    key = ur.student_loan(s, key_plan)
    if key == 0:
        rep.fail(w, 'salary', '£%s is below the threshold, so the key is £0: choose a salary above it' % s)
    vals = check_key_options(rep, w, q, key)
    if vals is not None:
        check_named(rep, w, q, vals, {
            penny(s * ur.STUDENT_LOAN_RATES[key_plan]): 'the rate on the whole salary',
            penny(key / 12): 'a monthly figure for an annual question',
            F(0): 'misjudging the comparison (below threshold)',
        })
    check_arith(rep, w, q)


def check_ni(rep, q):
    w = 'NI'
    m = NI_RX.search(q['stem'])
    r, a, b, s = pct(m.group(1)), num(m.group(2)), num(m.group(3)), num(m.group(4))
    if r != ur.NI_MAIN_RATE:
        rep.fail(w, 'rate', 'states %s%%, the %s employee main rate is %s%%'
                 % (r * 100, ur.TEACHING_YEAR, ur.percent(ur.NI_MAIN_RATE)))
    if (a, b) != (ur.NI_PRIMARY_THRESHOLD, ur.NI_UPPER_EARNINGS_LIMIT):
        rep.fail(w, 'thresholds', 'states £%s to £%s, %s is £%s to £%s'
                 % (a, b, ur.TEACHING_YEAR, ur.NI_PRIMARY_THRESHOLD, ur.NI_UPPER_EARNINGS_LIMIT))
    key = ur.employee_ni(s)
    vals = check_key_options(rep, w, q, key)
    if vals is None:
        return
    check_named(rep, w, q, vals, {
        penny(s * ur.NI_MAIN_RATE): 'the rate on the whole salary',
        penny((s - ur.NI_PRIMARY_THRESHOLD) * ur.BASIC_RATE): 'the income tax rate instead of NI',
        penny(key / 12): 'a monthly figure for an annual question',
    })
    check_arith(rep, w, q)


def check_budget(rep, q):
    w = 'BUDGET'
    m = BUDGET_RX.search(q['stem'])
    s, rt, at, rn, an = num(m.group(1)), pct(m.group(2)), num(m.group(3)), pct(m.group(4)), num(m.group(5))
    if rt != ur.BASIC_RATE or at != ur.PERSONAL_ALLOWANCE:
        rep.fail(w, 'income tax', 'states %s%% above £%s' % (rt * 100, at))
    if rn != ur.NI_MAIN_RATE or an != ur.NI_PRIMARY_THRESHOLD:
        rep.fail(w, 'NI', 'states %s%% above £%s, %s is %s%% above £%s'
                 % (rn * 100, an, ur.TEACHING_YEAR, ur.percent(ur.NI_MAIN_RATE), ur.NI_PRIMARY_THRESHOLD))
    if not ur.PERSONAL_ALLOWANCE < s <= ur.NI_UPPER_EARNINGS_LIMIT:
        rep.fail(w, 'salary', '£%s is outside the single-rate range the stem describes' % s)
    rows = (q.get('table') or {}).get('rows') or []
    budget = sum((money_value(r[1]) or F(0)) for r in rows)
    monthly = ur.take_home(s) / 12
    short = monthly < budget
    key_text = q['options'][q['correct']]
    if short != key_text.startswith('No'):
        rep.fail(w, 'key', 'take-home %s/month against a %s budget (%s), but the key is %r'
                 % (gbp(monthly), gbp(budget), 'short' if short else 'covered', key_text))
    for fig in (gbp(monthly), gbp(budget)):
        plain = fig[:-3] if fig.endswith('.00') else fig
        if fig not in q['working'] and plain not in q['working']:
            rep.fail(w, 'working', 'does not print %s' % fig)
    check_arith(rep, w, q)


KINDS = [('INCOME TAX', TAX_RX, check_tax), ('NI', NI_RX, check_ni), ('BUDGET', BUDGET_RX, check_budget),
         ('STUDENT LOAN', LOAN_RX, check_loan)]


def check_bank(rep, bank, verbose=False):
    for name, rx, fn in KINDS:
        hits = [q for q in bank if rx.search(q.get('stem', ''))]
        if len(hits) != 1:
            rep.fail(name, 'structure', 'found %d items matching its stem (expected 1): reworded? '
                     'Update this verifier with it' % len(hits))
            continue
        fn(rep, hits[0])
        if verbose:
            print('  checked %-10s Q%d' % (name, bank.index(hits[0]) + 1))
    # every tax/NI stem prints only the teaching year's NI rate and thresholds
    for i, q in enumerate(bank):
        text = q.get('stem', '') + ' ' + q.get('working', '')
        if not TAXNI_WORDS.search(text):
            continue
        for m in PCT_NEAR_NI.finditer(text):
            r = pct(m.group(1) or m.group(2))
            if r not in (ur.NI_MAIN_RATE, ur.NI_UPPER_RATE):
                rep.fail('Q%d' % (i + 1), 'NI rate', 'states NI at %s%%; %s is %s%% (%s%% above the UEL)'
                         % (r * 100, ur.TEACHING_YEAR, ur.percent(ur.NI_MAIN_RATE), ur.percent(ur.NI_UPPER_RATE)))


def load_bank():
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=8000)
            bank = page.evaluate('JSON.parse(JSON.stringify(QUESTIONS))')
            browser.close()
            if errors:
                sys.exit('page errors: %s' % '; '.join(errors))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank)

    def find(b, rx):
        return next(q for q in b if rx.search(q['stem']))

    def expect(name, fn):
        nonlocal ok
        b = copy.deepcopy(bank)
        fn(b)
        rep = Report()
        check_bank(rep, b)
        new = [f for f in rep.fails if f not in base.fails]
        caught = bool(new)
        ok = ok and caught
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + new[0][:110]) if caught else '*** MISSED ***'))

    def old_rate(b):
        q = find(b, NI_RX)
        q['stem'] = re.sub(r'charged at \d+%', 'charged at 12%', q['stem'])
    expect('old 12% NI rate (NI item)', old_rate)

    def old_rate_budget(b):
        q = find(b, BUDGET_RX)
        q['stem'] = re.sub(r'NI \(\d+%', 'NI (12%', q['stem'])
    expect('old 12% NI rate (budget item)', old_rate_budget)

    def wrong_key(b):
        q = find(b, NI_RX)
        q['correct'] = (q['correct'] + 1) % len(q['options'])
    expect('wrong key (NI item)', wrong_key)

    def unnamed(b):
        q = find(b, NI_RX)
        i = (q['correct'] + 1) % len(q['options'])
        q['options'][i] = '£1,244.40'
    expect('unnamed distractor (£1,244.40)', unnamed)

    def old_savings(b):
        q = find(b, BUDGET_RX)
        q['table']['rows'] = [r if r[0] != 'Savings' else ['Savings', '£300'] for r in q['table']['rows']]
    expect('old £300 savings (budget covered)', old_savings)

    def old_threshold(b):
        q = find(b, LOAN_RX)
        q['stem'] = re.sub(r'above £[\d,]+', 'above £27,295', q['stem'])
    expect('old £27,295 loan threshold', old_threshold)

    def no_plan(b):
        q = find(b, LOAN_RX)
        q['stem'] = re.sub(r'^Plan \d s', 'S', q['stem'])
    expect('loan plan not named', no_plan)

    def old_q21(b):
        q = find(b, TAX_RX)
        q['options'] = [o if o != '£7,400.00' else '£4,628.00' for o in q['options']]
    expect("Q21's old £4,628 distractor", old_q21)
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

    bank = load_bank()
    rep = Report()
    check_bank(rep, bank, args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    print('\n%s: %d FAIL(s); income tax, NI, budget and student loan items checked against %s (scripts/uk_rates.py)'
          % ('PASS' if ok else 'FAILED', len(rep.fails), ur.TEACHING_YEAR))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
