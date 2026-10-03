#!/usr/bin/env python3
"""Independent verification of better-value's tax-and-NI rule of thumb (canon §7.1.4, todo §1.43).

Until 3 Oct 2026 bv_core_046 told students "Tax and NI are approximately 25% of gross salary";
at 2025/26 rates the real share is 15.4% at £28,000 and 17.6% at £34,000. better-value stays an
estimation game (Jon), so the question keeps a rule of thumb, but the rule must be true.

Every better-value question whose scenario mentions tax or NI is checked (and there must be at
least one, or the question was reworded and this verifier is blind):
  - its stated rule ("roughly a sixth", "approximately 25%", ...) is within TOLERANCE percentage
    points of the true share (income tax + employee NI, scripts/uk_rates.py) at every salary it gives;
  - disposable income per month (salary less the rule's share, divided by 12, less the monthly rent)
    is recomputed for each job, and the correct conclusion prints those two figures (to the £);
  - the job with more disposable income is the same under the rule and under the true rates (so a
    student using the rule reaches the right answer), and the correct conclusion names it;
  - every Tax/NI detail row states the same rule as the scenario.
A fault-injection self-test (the old 25%, a wrong printed figure, a rule that flips the winner)
must FAIL each time; it runs unless --no-selftest.

    python scripts/verify-better-value-tax.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import uk_rates as ur  # noqa: E402

SLUG = 'better-value'
TOLERANCE = F(2, 100)       # "within about 2 percentage points" (Jon, 3 Oct 2026)

TAX_WORDS = re.compile(r'\btax\b|\bNI\b|national insurance', re.I)
WORD_FRACTIONS = {'half': F(1, 2), 'third': F(1, 3), 'quarter': F(1, 4), 'fifth': F(1, 5),
                  'sixth': F(1, 6), 'seventh': F(1, 7), 'eighth': F(1, 8)}
RULE_WORDS = re.compile(r'\b(?:a|one)\s+(' + '|'.join(WORD_FRACTIONS) + r')\b', re.I)
RULE_PCT = re.compile(r'(\d+(?:\.\d+)?)\s*%')
RULE_FRAC = re.compile(r'\b1\s*/\s*(\d+)\b')
JOB = re.compile(r'£([\d,]+) salary in ([A-Z][a-z]+) \(average rent £([\d,]+)/month\)')
MONEY = re.compile(r'£([\d,]+(?:\.\d+)?)')


def rule_of(text):
    """The share a piece of text states, as a Fraction, or None."""
    m = RULE_WORDS.search(text)
    if m:
        return WORD_FRACTIONS[m.group(1).lower()]
    m = RULE_FRAC.search(text)
    if m:
        return F(1, int(m.group(1)))
    m = RULE_PCT.search(text)
    return F(m.group(1)) / 100 if m else None


def true_share(gross):
    return (ur.income_tax(gross) + ur.employee_ni(gross)) / gross


def disposable(gross, rent, share):
    return gross * (1 - share) / 12 - rent


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, qid, what, detail):
        self.fails.append('%s %s: %s' % (qid, what, detail))


def check_question(rep, q, verbose=False):
    qid = q.get('id', '?')
    scen = q.get('scenario', '')
    rule = rule_of(scen[scen.lower().find('tax'):] if 'tax' in scen.lower() else scen)
    if rule is None:
        rep.fail(qid, 'rule', 'mentions tax/NI but states no share this verifier can read')
        return
    jobs = [(m.group(2), F(m.group(1).replace(',', '')), F(m.group(3).replace(',', ''))) for m in JOB.finditer(scen)]
    if len(jobs) != 2:
        rep.fail(qid, 'structure', 'expected two "£X salary in Place (average rent £Y/month)" jobs, found %d' % len(jobs))
        return
    for opt in ('optionA', 'optionB'):
        for d in (q.get(opt) or {}).get('details', []):
            if TAX_WORDS.search(d.get('key', '')) and rule_of(d.get('value', '')) != rule:
                rep.fail(qid, 'detail', '%s %s says %r, the scenario says %s' % (opt, d['key'], d['value'], rule))
    for place, gross, rent in jobs:
        ts = true_share(gross)
        if abs(ts - rule) > TOLERANCE:
            rep.fail(qid, 'rule', '%s %s at £%s: the rule says %.1f%%, the true %s share is %.1f%% '
                     '(%.1f points out; tolerance %d)' % (place, 'tax+NI', gross, float(rule) * 100,
                                                          ur.TEACHING_YEAR, float(ts) * 100,
                                                          abs(float(ts - rule)) * 100, int(TOLERANCE * 100)))
        if verbose:
            print('  %s %-11s £%s: rule %.1f%%, true %.1f%%, disposable £%.2f (rule) / £%.2f (true)'
                  % (qid, place, gross, float(rule) * 100, float(ts) * 100,
                     float(disposable(gross, rent, rule)), float(disposable(gross, rent, ts))))
    by_rule = {p: disposable(g, r, rule) for p, g, r in jobs}
    by_true = {p: disposable(g, r, true_share(g)) for p, g, r in jobs}
    win_rule = max(by_rule, key=by_rule.get)
    win_true = max(by_true, key=by_true.get)
    if win_rule != win_true:
        rep.fail(qid, 'winner', 'the rule makes %s better, the true %s rates make %s better'
                 % (win_rule, ur.TEACHING_YEAR, win_true))
    correct = [c for c in q.get('conclusions', []) if c.get('correct')]
    if len(correct) != 1:
        rep.fail(qid, 'key', '%d conclusions marked correct' % len(correct))
        return
    text = correct[0]['text']
    if win_true not in text:
        rep.fail(qid, 'key', 'the correct conclusion %r does not name %s' % (text, win_true))
    printed = [F(m.replace(',', '')) for m in MONEY.findall(text)]
    want = [round(by_rule[p]) for p, _, _ in sorted(jobs, key=lambda j: -by_rule[j[0]])]
    if [round(x) for x in printed] != want:
        rep.fail(qid, 'figures', 'the correct conclusion prints %s; the rule gives %s'
                 % (', '.join('£%s' % x for x in printed), ', '.join('£%s' % w for w in want)))


def tax_questions(bank):
    return [q for q in bank if TAX_WORDS.search(q.get('scenario', ''))
            and JOB.search(q.get('scenario', ''))]


def check_bank(rep, bank, verbose=False):
    qs = tax_questions(bank)
    if not qs:
        rep.fail('bank', 'structure', 'no salary question mentions tax/NI: reworded? Update this verifier')
    for q in qs:
        check_question(rep, q, verbose)
    return qs


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
            bank = page.evaluate('Object.values(JSON.parse(JSON.stringify(QUESTIONS))).flat()')
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
    qs = check_bank(base, bank)

    def expect(name, fn):
        nonlocal ok
        b = copy.deepcopy(qs)
        fn(b[0])
        rep = Report()
        check_bank(rep, b)
        new = [f for f in rep.fails if f not in base.fails]
        caught = bool(new)
        ok = ok and caught
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + new[0][:110]) if caught else '*** MISSED ***'))

    def old_rule(q):
        q['scenario'] = re.sub(r'roughly a sixth|approximately \d+%', 'approximately 25%', q['scenario'])
        for opt in ('optionA', 'optionB'):
            for d in q[opt]['details']:
                if TAX_WORDS.search(d['key']):
                    d['value'] = '25%'
    expect('old 25% rule (scenario + details)', old_rule)

    def wrong_figure(q):
        c = next(c for c in q['conclusions'] if c['correct'])
        c['text'] = re.sub(r'£([\d,]+)', lambda m: '£%d' % (int(m.group(1).replace(',', '')) + 50), c['text'], count=1)
    expect('wrong printed figure (+£50)', wrong_figure)

    def flips(q):
        # London rent cut so far that the rule and the true rates disagree on the winner
        q['scenario'] = q['scenario'].replace('(average rent £1,200/month)', '(average rent £1,020/month)')
    expect('rent that flips the winner', flips)
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
    qs = check_bank(rep, bank, args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest and qs:
        s_ok, lines = selftest(bank)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    print('\n%s: %d FAIL(s); %d tax question(s) of %d checked against %s (scripts/uk_rates.py)'
          % ('PASS' if ok else 'FAILED', len(rep.fails), len(qs), len(bank), ur.TEACHING_YEAR))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
