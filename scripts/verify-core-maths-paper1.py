#!/usr/bin/env python3
"""Independent verification of every core-maths-paper1 question (all 36), from the question's own data.

Until 6 Oct 2026 only the tax, NI and student loan items had a verifier (verify-core-maths-paper1-tax.py,
which checks the stated rates against uk_rates). The tranche 2 audit
(docs/audits/audit-tranche2-2026-10-06.md) found four faults in the other 32: Q32 keyed "B by £44.70" (the
answer is £34.67, which no option offered), Q9 keyed "Yes" to "more than half scored above the median",
Q7 offering a second option with the key's classification, and Q1 keying an IQR by a method the question
never named. This script recomputes every key it can from the stem, table and chart data the student sees.

Items are found by what they ask (a stem pattern), not by position, and each rule must match exactly one
question; a question no rule matches FAILS, so a new question needs a rule here.

For every COMPUTED item:
  - the key is recomputed exactly (Fraction, or Decimal rounded half up to the precision the money or the
    question states);
  - every option is read as a value of the same kind (a number, money, a class interval, a classification,
    an error interval, "Account X by £y"); an option that cannot be read FAILS;
  - exactly one option equals the key in value, and it is the keyed one; no two options are equal in value.
For every item: no two options are the same text; the key's text is a real option.
Verdict items (Yes/No) are recomputed; Q9's verdict must be carried by one option only (Jon's ruling of
6 Oct 2026, 19:15: a true statement is never a wrong option).

Not computed (judgement items, pinned with the reviewed key text; changing one fails until this table is
re-reviewed):
  Q3  batch choice (consistency is the SD; a judgement of which reason is "the" reason)
  Q8  sampling bias (which bias is "most significant")
  Q10 salary advert (the stated £37,000 IS recomputed as the mean; "potentially misleading" is judgement)
  Q11 two classes, same mean (which statement is "most accurate")
  Q13 survey design (which response "best explains")
  Q14 the sports drink claim (which question is "most important")
  Q17 removing an outlier (the stated mean IS recomputed; "significantly" / "very little" is judgement)
  Q18 correlation and causation (which criticism is "most appropriate")
Q7's classification of each variable comes from a reviewed table (CLASSIFY), the definitions taught at GCSE.
Q21, Q30, Q31 and Q36 are recomputed here from the figures their stems state; whether those figures are the
teaching year's rates is verify-core-maths-paper1-tax.py's job (uk_rates). Q27's CPI figures are taken as
stated (whether they are true is the quoted-statistics audit's, todo).

Pictures (SR-6): each histogram's and the box plot's data are read from the page's own renderers and the keys
are computed from them; the box plot's five numbers must equal the stem's; every chart line not drawn over a
filled shape must contrast at least 3:1 with the question card (WCAG 1.4.11), which Q9's whiskers did not
(drawn in the card's own colour). The stem-and-leaf diagram is read from its rendered table.
Marking: every key is clicked through the page's own selectAnswer() and must be marked correct.

A fault-injection self-test (Q32's old options and key, Q7's old option C, Q1 with no method named, Q9's old
key, Q9's old whisker colour, a wrong key on a computed item) must FAIL each time; it runs unless
--no-selftest.

    python scripts/verify-core-maths-paper1.py [--verbose] [--no-selftest]
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

SLUG = 'core-maths-paper1'
MIN_CONTRAST = 3.0


# ── readers ──────────────────────────────────────────────────────────────────

def num(s):
    """Exact Fraction from a printed number ('3.9', '12,570', '−16')."""
    s = s.replace(',', '').replace('−', '-').strip()
    return F(Decimal(s))


def money_all(s):
    return [num(m) for m in re.findall(r'£\s?(\d[\d,]*(?:\.\d+)?)', s)]


def penny(x):
    """Exact value rounded half up to the penny, as a Fraction."""
    d = (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return F(d)


def round_to(x, dp):
    q = Decimal(1).scaleb(-dp)
    return F((Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP))


def plain_number(opt):
    m = re.fullmatch(r'\s*(-?\d[\d,]*(?:\.\d+)?)\s*', opt.replace('−', '-'))
    return num(m.group(1)) if m else None


def single_money(opt):
    """An option that is one sum of money and nothing else that could be a second value."""
    vals = money_all(opt)
    if len(vals) == 1 and re.fullmatch(r'\s*£\s?[\d,]+(?:\.\d+)?\s*', opt):
        return vals[0]
    m = re.fullmatch(r'\s*\$\s?(\d[\d,]*(?:\.\d+)?)\s*', opt)
    return num(m.group(1)) if m else None


def percent_opt(opt):
    m = re.fullmatch(r'\s*(\d+(?:\.\d+)?)%\s*', opt)
    return num(m.group(1)) if m else None


def class_label(opt):
    m = re.fullmatch(r'\s*(\d+)\s*[–-]\s*(\d+)\s*', opt)
    return (int(m.group(1)), int(m.group(2))) if m else None


def lead_numbers(text):
    return [num(t) for t in re.findall(r'-?\d+(?:\.\d+)?', text.replace(',', ''))]


# ── the report ───────────────────────────────────────────────────────────────

class Report:
    def __init__(self):
        self.fails, self.notes = [], []

    def fail(self, qid, what, msg):
        self.fails.append('%s %s: %s' % (qid, what, msg))


def check_values(rep, qid, q, key, reader, what='key'):
    """Exactly one option equals key in value, it is the keyed one; no two options equal in value."""
    vals = []
    for i, o in enumerate(q['options']):
        v = reader(o)
        if v is None:
            rep.fail(qid, 'unreadable option', '%r cannot be read as a value of this question\'s kind' % o)
            return
        vals.append(v)
    hits = [i for i, v in enumerate(vals) if v == key]
    if len(hits) != 1:
        rep.fail(qid, what, '%d options equal the recomputed %s %s (options %s)'
                 % (len(hits), what, fmt_val(key), q['options']))
    elif hits[0] != q['correct']:
        rep.fail(qid, what, 'keyed %r, but the recomputed %s is %s, option %r'
                 % (q['options'][q['correct']], what, fmt_val(key), q['options'][hits[0]]))
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if vals[i] == vals[j]:
                rep.fail(qid, 'value-equal options', '%r and %r are the same value' % (q['options'][i], q['options'][j]))


def fmt_val(v):
    if isinstance(v, F):
        return str(float(v)) if v.denominator != 1 else str(v.numerator)
    return repr(v)


def verdict(rep, qid, q, word, unique=False):
    """The keyed option opens with the right verdict. With unique, no other option opens with it either:
    where the bare verdict is the whole answer, a second option with it is the right answer for a wrong
    reason (Jon, 6 Oct 2026: such an option names the fault in its own text, or goes). Without unique, a
    verdict word may open a false claim ("Yes, but only if ...")."""
    starts = [i for i, o in enumerate(q['options']) if re.match(r'\s*%s\b' % word, o)]
    if q['correct'] not in starts:
        rep.fail(qid, 'verdict', 'keyed %r, but the answer is "%s"' % (q['options'][q['correct']], word))
    elif unique and len(starts) != 1:
        rep.fail(qid, 'verdict', '%d options say "%s"; only one may: %s' % (len(starts), word, q['options']))


# ── the rules: one per question, found by what it asks ───────────────────────

def r_iqr(rep, qid, q, ctx):
    if not re.search(r'\(n\s*\+\s*1\)\s*/\s*4', q['stem']):
        rep.fail(qid, 'method', 'no quartile method named; inclusive, (n + 1)/4 and calculator methods give '
                 'different IQRs (Jon, 6 Oct 2026: a contested convention is stated in the question)')
        return
    data = sorted(lead_numbers(re.search(r'are:\s*([\d,\s.]+)\.', q['stem']).group(1)))
    n = len(data)

    def at(pos):
        lo = int(pos)
        frac = pos - lo
        return data[lo - 1] + frac * (data[lo] - data[lo - 1]) if frac else data[lo - 1]
    lq, uq = at(F(n + 1, 4)), at(F(3 * (n + 1), 4))
    check_values(rep, qid, q, uq - lq, plain_number, 'IQR')


def r_grouped_mean(rep, qid, q, ctx):
    rows = q['table']['rows']
    tot = sum(num(f) for _, f in rows)
    stated = re.search(r'number of hours per week (\d+) adults', q['stem'])
    if stated and num(stated.group(1)) != tot:
        rep.fail(qid, 'table', 'frequencies sum to %s, the stem says %s' % (tot, stated.group(1)))
    mean = sum(num(f) * (lead_numbers(c)[0] + lead_numbers(c)[1]) / 2 for c, f in rows) / tot
    check_values(rep, qid, q, mean, plain_number, 'estimated mean')


def r_hist_between(rep, qid, q, ctx):
    a, b = (int(x) for x in re.search(r'between (\d+) and (\d+) minutes', q['stem']).groups())
    bars = ctx['charts'][q['svg']]['args']['bars']
    freq = 0
    for bar in bars:
        x0, x1, fd = bar['x0'], bar['x1'], F(Decimal(str(bar['fd'])))
        if a <= x0 and x1 <= b:
            freq += fd * (x1 - x0)
        elif x0 < b and a < x1:
            rep.fail(qid, 'chart', 'class %s-%s straddles the asked range %s-%s' % (x0, x1, a, b))
    check_values(rep, qid, q, freq, plain_number, 'frequency')


def r_stratified(rep, qid, q, ctx):
    total = num(re.search(r'employs (\d+) workers', q['stem']).group(1))
    size = num(re.search(r'sample of (\d+)', q['stem']).group(1))
    group = re.search(r'come from the (\w+) shift', q['stem']).group(1)
    count = num(re.search(r'(\d+) %s shift' % group, q['stem']).group(1))
    check_values(rep, qid, q, count / total * size, plain_number, 'sample size')


def r_cf_median(rep, qid, q, ctx):
    n = num(re.search(r'weights of (\d+) parcels', q['stem']).group(1))
    pts = [(num(c), num(b)) for c, b in re.findall(r'(\d+) below (\d+) kg', q['stem'])]
    prev, cls = 0, None
    for cf, bound in pts:
        if cf >= n / 2:
            cls = ('between', prev, bound)
            break
        prev = bound

    def read(o):
        m = re.fullmatch(r'\s*Between (\d+) kg and (\d+) kg\s*', o)
        if m:
            return ('between', num(m.group(1)), num(m.group(2)))
        m = re.fullmatch(r'\s*Exactly (\d+) kg\s*', o)
        return ('exactly', num(m.group(1))) if m else None
    check_values(rep, qid, q, cls, read, 'median class')


# Reviewed definitions (GCSE): the four variables Q7 names.
CLASSIFY = [(r'shoe size', 'QD'), (r'colour', 'QL'), (r'time', 'QC'), (r'siblings', 'QD')]


def r_classify(rep, qid, q, ctx):
    names = [s.strip() for s in re.search(r'collects:\s*(.*?)\.\s*Which', q['stem']).group(1).split(',')]
    truth = []
    for name in names:
        hit = [c for rx, c in CLASSIFY if re.search(rx, name)]
        if len(hit) != 1:
            rep.fail(qid, 'variable', '%r is not in the reviewed CLASSIFY table' % name)
            return
        truth.append(hit[0])
    terms = {'quantitative discrete': 'QD', 'discrete': 'QD', 'quantitative continuous': 'QC',
             'continuous': 'QC', 'qualitative': 'QL', 'quantitative': 'Q?'}

    def read(o):
        if re.fullmatch(r'\s*All four are quantitative\s*', o):
            return ('Q?',) * len(names)
        parts = [p.strip().lower() for p in o.split(',')]
        if len(parts) != len(names) or any(p not in terms for p in parts):
            return None
        return tuple(terms[p] for p in parts)
    check_values(rep, qid, q, tuple(truth), read, 'classification')


def r_boxplot_claim(rep, qid, q, ctx):
    five = [num(x) for x in re.search(r'Min: (\d+), LQ: (\d+), Median: (\d+), UQ: (\d+), Max: (\d+)', q['stem']).groups()]
    drawn = [F(Decimal(str(v))) for v in ctx['charts'][q['svg']]['args']['five']]
    if drawn != five:
        rep.fail(qid, 'chart', 'box plot drawn with %s, the stem says %s' % ([float(v) for v in drawn], [float(v) for v in five]))
    claimed = num(re.search(r'more than half the class scored above (\d+)', q['stem']).group(1))
    if claimed != five[2]:
        rep.fail(qid, 'rule', 'the claim is not about the median; extend this rule')
        return
    # At most half the values can lie strictly above a median, so "more than half" is false.
    verdict(rep, qid, q, 'No', unique=True)


def r_salary(rep, qid, q, ctx):
    sal = money_all(q['stem'].split('A recruitment')[0])
    stated = money_all(q['stem'].split('A recruitment')[1])[0]
    if sum(sal) / len(sal) != stated:
        rep.fail(qid, 'stem', 'the advertised average £%s is not the mean £%s' % (stated, sum(sal) / len(sal)))
    pinned(rep, qid, q)


def r_hist_most(rep, qid, q, ctx):
    bars = ctx['charts'][q['svg']]['args']['bars']
    freqs = [(F(Decimal(str(b['fd']))) * (b['x1'] - b['x0']), (b['x0'], b['x1'])) for b in bars]
    top = max(f for f, _ in freqs)
    winners = [c for f, c in freqs if f == top]
    if len(winners) != 1:
        rep.fail(qid, 'tie', 'classes %s tie on the highest frequency %s' % (winners, top))
        return
    check_values(rep, qid, q, winners[0], class_label, 'modal class')


def r_stemleaf(rep, qid, q, ctx):
    html = ctx['charts'][q['svg']]['svg']
    rows = re.findall(r'<td class="left-col">(.*?)</td><td class="stem-col">(\d+)</td><td class="right-col">(.*?)</td>', html)
    a, b = [], []
    for left, stem, right in rows:
        a += [int(stem) * 10 + int(x) for x in re.findall(r'\d', left)]
        b += [int(stem) * 10 + int(x) for x in re.findall(r'\d', right)]
    stated = int(re.search(r'\((\d+) values each\)', q['stem']).group(1))
    if len(a) != stated or len(b) != stated:
        rep.fail(qid, 'chart', 'the diagram has %d and %d values, the stem says %d each' % (len(a), len(b), stated))

    def med(v):
        v = sorted(v)
        k = len(v)
        return F(v[k // 2]) if k % 2 else F(v[k // 2 - 1] + v[k // 2], 2)
    check_values(rep, qid, q, abs(med(a) - med(b)), plain_number, 'difference of medians')


def r_percentile(rep, qid, q, ctx):
    n = num(re.search(r'Heights of (\d+) students', q['stem']).group(1))
    p1, p2 = (num(x) for x in re.findall(r'(\d+)th percentile', q['stem'])[:2])
    check_values(rep, qid, q, (p2 - p1) / 100 * n, plain_number, 'count')


def r_reaction(rep, qid, q, ctx):
    vals = lead_numbers(re.search(r'for 8 people:\s*([\d,\s]+)\.', q['stem']).group(1))
    stated = num(re.search(r'Mean = ([\d.]+) ms', q['stem']).group(1))
    if round_to(sum(vals) / len(vals), 1) != stated:
        rep.fail(qid, 'stem', 'stated mean %s; the data give %s' % (stated, float(sum(vals) / len(vals))))
    pinned(rep, qid, q)


def r_simple(rep, qid, q, ctx):
    m = re.search(r'£([\d,]+) is invested at ([\d.]+)% simple interest .*? after (\d+) years', q['stem'])
    p, r, t = num(m.group(1)), num(m.group(2)) / 100, num(m.group(3))
    check_values(rep, qid, q, penny(p * r * t), single_money, 'interest')


def r_compound_value(rep, qid, q, ctx):
    m = re.search(r'£([\d,]+) is invested for (\d+) years at ([\d.]+)% compound', q['stem'])
    p, n, r = num(m.group(1)), int(m.group(2)), num(m.group(3)) / 100
    check_values(rep, qid, q, penny(p * (1 + r) ** n), single_money, 'value')


def r_income_tax(rep, qid, q, ctx):
    m = re.search(r'Personal allowance £([\d,]+)\. Income tax (\d+)% .*? earns £([\d,]+)', q['stem'])
    a, r, s = num(m.group(1)), num(m.group(2)) / 100, num(m.group(3))
    check_values(rep, qid, q, penny(r * (s - a)), single_money, 'income tax')


def r_vat(rep, qid, q, ctx):
    m = re.search(r'£(\d+) for labour plus £(\d+) for parts\. VAT is charged at (\d+)%', q['stem'])
    a, b, v = num(m.group(1)), num(m.group(2)), num(m.group(3)) / 100
    check_values(rep, qid, q, penny((a + b) * (1 + v)), single_money, 'bill')


def r_exchange(rep, qid, q, ctx):
    m = re.search(r'£1 = \$([\d.]+)\. Bank charges ([\d.]+)% commission\..*?exchanging £(\d+)', q['stem'])
    rate, c, s = num(m.group(1)), num(m.group(2)) / 100, num(m.group(3))
    check_values(rep, qid, q, penny(s * (1 - c) * rate), single_money, 'dollars')


def r_reverse(rep, qid, q, ctx):
    m = re.search(r'After a (\d+)% increase, .*? costs £([\d,]+)', q['stem'])
    r, price = num(m.group(1)) / 100, num(m.group(2))
    check_values(rep, qid, q, penny(price / (1 + r)), single_money, 'original price')


def r_aer(rep, qid, q, ctx):
    i = num(re.search(r'nominal rate of ([\d.]+)% per year, compounded monthly', q['stem']).group(1)) / 100
    if not re.search(r'to 2 decimal places', q['stem']):
        rep.fail(qid, 'precision', 'no precision stated')
    check_values(rep, qid, q, round_to(((1 + i / 12) ** 12 - 1) * 100, 2), percent_opt, 'AER')


def r_priya(rep, qid, q, ctx):
    pay = money_all(q['stem'])[0]
    pct = num(re.search(r'save (\d+)%', q['stem']).group(1)) / 100
    left = pay - sum(money_all(c)[0] for _, c in q['table']['rows'])
    if left >= pct * pay:
        verdict(rep, qid, q, 'Yes')
        key = q['options'][q['correct']]
        if money_all(key)[:2] != [left, pct * pay]:
            rep.fail(qid, 'figures', 'the key states %s; remaining is £%s and the target £%s'
                     % (money_all(key), fmt_val(left), fmt_val(pct * pay)))
    else:
        verdict(rep, qid, q, 'No')


def r_cpi(rep, qid, q, ctx):
    base = money_all(q['stem'])[0]
    rates = [num(x) / 100 for x in re.findall(r'([\d.]+)% in \d{4}', q['stem'])]
    v = base
    for r in rates:
        v *= 1 + r
    check_values(rep, qid, q, penny(v), single_money, 'cost')


def r_error_interval(rep, qid, q, ctx):
    m = re.search(r'measured as ([\d.]+) cm, rounded to (\d+) decimal place', q['stem'])
    x, dp = num(m.group(1)), int(m.group(2))
    h = F(1, 2 * 10 ** dp)
    key = (x - h, True, x + h, False)

    def read(o):
        m2 = re.fullmatch(r'\s*([\d.]+) (≤|<) l (≤|<) ([\d.]+)\s*', o)
        if not m2:
            return None
        return (num(m2.group(1)), m2.group(2) == '≤', num(m2.group(4)), m2.group(3) == '≤')
    check_values(rep, qid, q, key, read, 'error interval')


def r_years(rep, qid, q, ctx):
    m = re.search(r'invests £([\d,]+) at ([\d.]+)% compound .*? exceed £([\d,]+)', q['stem'])
    p, r, target = num(m.group(1)), num(m.group(2)) / 100, num(m.group(3))
    n = 0
    while p * (1 + r) ** n <= target:      # terminates: r > 0, so the value grows without bound
        n += 1
    check_values(rep, qid, q, F(n), plain_number, 'years')


def r_ni(rep, qid, q, ctx):
    m = re.search(r'NI is charged at (\d+)% on earnings between £([\d,]+) and £([\d,]+)\. A worker earns £([\d,]+)', q['stem'])
    r, lo, hi, s = num(m.group(1)) / 100, num(m.group(2)), num(m.group(3)), num(m.group(4))
    check_values(rep, qid, q, penny(r * (min(s, hi) - lo)), single_money, 'NI')


def r_loan(rep, qid, q, ctx):
    m = re.search(r'repayments are (\d+)% of earnings above £([\d,]+)\. A graduate earns £([\d,]+)', q['stem'])
    r, t, s = num(m.group(1)) / 100, num(m.group(2)), num(m.group(3))

    def read(o):
        if re.match(r'\s*£0 — earnings below threshold', o):
            return F(0)
        return single_money(o)
    check_values(rep, qid, q, penny(r * max(s - t, 0)), read, 'repayment')


def r_two_accounts(rep, qid, q, ctx):
    m = re.search(r'Account A: ([\d.]+)% (simple|compound) .*?Account B: ([\d.]+)% (simple|compound) .*?'
                  r'invests £([\d,]+) for (\d+) years', q['stem'])
    p, t = num(m.group(5)), int(m.group(6))

    def interest(rate, kind):
        r = num(rate) / 100
        return p * r * t if kind == 'simple' else p * (1 + r) ** t - p
    ia, ib = penny(interest(m.group(1), m.group(2))), penny(interest(m.group(3), m.group(4)))
    key = ('same', F(0)) if ia == ib else (('A', ia - ib) if ia > ib else ('B', ib - ia))

    def read(o):
        m2 = re.fullmatch(r'\s*Account (A|B) by £([\d,]+(?:\.\d+)?)\s*', o)
        if m2:
            return (m2.group(1), num(m2.group(2)))
        return ('same', F(0)) if re.fullmatch(r'\s*Both give the same total interest\s*', o) else None
    check_values(rep, qid, q, key, read, 'difference')
    w = q.get('working', '')
    for amt in (ia, ib, key[1]):
        if '£{:,.2f}'.format(float(amt)) not in w:
            rep.fail(qid, 'working', 'the working does not state £%s: %r' % ('{:,.2f}'.format(float(amt)), w))


def r_mortgage(rep, qid, q, ctx):
    m = re.search(r'borrow £([\d,]+) on a (\d+)-year .*? Monthly repayment: £([\d,]+)', q['stem'])
    p, n, mth = num(m.group(1)), num(m.group(2)), num(m.group(3))
    total = mth * 12 * n

    def read(o):
        v = money_all(o)
        return tuple(v) if len(v) == 2 and o.startswith('Total') else None
    check_values(rep, qid, q, (total, total - p), read, 'total and interest')


def r_real_terms(rep, qid, q, ctx):
    pay = num(re.search(r'salary increases by ([\d.]+)%', q['stem']).group(1))
    inf = num(re.search(r'inflation the same year is ([\d.]+)%', q['stem']).group(1))
    verdict(rep, qid, q, 'Fallen' if pay < inf else 'Improved' if pay > inf else 'Unchanged')


def r_euros(rep, qid, q, ctx):
    m = re.search(r'returns with (\d+) euros\. Rate: £1 = €([\d.]+)\. .*?£([\d.]+) flat fee plus ([\d.]+)% commission', q['stem'])
    e, rate, fee, c = num(m.group(1)), num(m.group(2)), num(m.group(3)), num(m.group(4)) / 100
    s = e / rate
    check_values(rep, qid, q, penny(s - c * s - fee), single_money, 'pounds')


def r_marcus(rep, qid, q, ctx):
    m = re.search(r'earns £([\d,]+) per year\. After income tax \((\d+)% on earnings above £([\d,]+)\) and NI '
                  r'\((\d+)% on earnings above £([\d,]+)\)', q['stem'])
    s, t, ta, ni, na = (num(x) for x in m.groups())
    take = (s - t / 100 * (s - ta) - ni / 100 * (s - na)) / 12
    budget = sum(money_all(c)[0] for _, c in q['table']['rows'])
    verdict(rep, qid, q, 'Yes' if take >= budget else 'No')


# Judgement items: the reviewed key text (see the module docstring).
PINNED = {
    r'Two batches of components': 'Batch A, because it has a smaller standard deviation',
    r'surveys the first 40 people outside a cinema': 'People visiting a cinema on a Saturday afternoon may watch less TV than average',
    r'A recruitment advert states': 'Mean — potentially misleading, because it is heavily influenced by the outlier',
    r'Class X: mean 62': 'Class X performed better on average because their median is higher',
    r'survey students about a new homework policy': 'Library visitors may be more academically engaged and have different views on homework — a stratified random sample would be better',
    r'sports drink company': 'Was there a control group that did not use the product?',
    r'Reaction times \(ms\)': 'The mean would decrease significantly; the median would change very little',
    r'Eating breakfast causes': 'Correlation between breakfast habits and earnings does not imply causation',
}


def pinned(rep, qid, q):
    for rx, key in PINNED.items():
        if re.search(rx, q['stem']):
            if q['options'][q['correct']] != key:
                rep.fail(qid, 'pinned key', 'keyed %r; the reviewed key is %r (re-review and update PINNED to change it)'
                         % (q['options'][q['correct']], key))
            return
    rep.fail(qid, 'pinned key', 'no PINNED entry')


def r_pinned(rep, qid, q, ctx):
    pinned(rep, qid, q)


RULES = [
    ('IQR', r'interquartile range', r_iqr),
    ('grouped mean', r'What is the estimated mean', r_grouped_mean),
    ('batch choice', r'Two batches of components', r_pinned),
    ('histogram range', r'How many patients waited between', r_hist_between),
    ('stratified sample', r'stratified sample', r_stratified),
    ('CF median', r'cumulative frequency table', r_cf_median),
    ('classification', r'classifies all four', r_classify),
    ('sampling bias', r'surveys the first 40 people', r_pinned),
    ('box plot claim', r'more than half the class scored above', r_boxplot_claim),
    ('salary advert', r'A recruitment advert states', r_salary),
    ('two classes', r'Class X: mean', r_pinned),
    ('histogram modal', r'Which age group had the most visitors', r_hist_most),
    ('survey design', r'new homework policy', r_pinned),
    ('sports drink', r'sports drink company', r_pinned),
    ('stem and leaf', r'stem-and-leaf', r_stemleaf),
    ('percentiles', r'25th percentile', r_percentile),
    ('reaction times', r'Reaction times \(ms\)', r_reaction),
    ('causation', r'Eating breakfast causes', r_pinned),
    ('simple interest', r'simple interest per year\. What is the total interest', r_simple),
    ('compound value', r'compound interest per annum\. What is the value', r_compound_value),
    ('income tax', r'^Personal allowance', r_income_tax),
    ('VAT', r'VAT is charged', r_vat),
    ('exchange', r'Bank charges [\d.]+% commission', r_exchange),
    ('reverse percentage', r'increase, a train season ticket', r_reverse),
    ('AER', r'what is the AER', r_aer),
    ('saving', r'save \d+% of her take-home', r_priya),
    ('CPI', r'CPI inflation', r_cpi),
    ('error interval', r'error interval', r_error_interval),
    ('years to exceed', r'How many complete years', r_years),
    ('NI', r'^NI is charged', r_ni),
    ('student loan', r'student loan repayments', r_loan),
    ('two accounts', r'Account A: .*Account B:', r_two_accounts),
    ('mortgage', r'repayment mortgage', r_mortgage),
    ('real terms', r'standard of living', r_real_terms),
    ('euros', r'returns with \d+ euros', r_euros),
    ('budget', r'monthly budget\. Is his plan achievable', r_marcus),
]


# ── pictures ─────────────────────────────────────────────────────────────────

def _lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def parse_colour(s):
    s = s.strip()
    m = re.fullmatch(r'#([0-9a-fA-F]{6})', s)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', s)
    return tuple(int(x) for x in m.groups()) if m else None


def attrs(tag):
    return dict(re.findall(r'([\w-]+)="([^"]*)"', tag))


def check_chart_contrast(rep, qid, svg, bg):
    """Every <line> not drawn inside a filled <rect> must contrast >= 3:1 with the card it sits on."""
    rects = []
    for t in re.findall(r'<rect\b[^>]*>', svg):
        a = attrs(t)
        x, y, w, h = (float(a[k]) for k in ('x', 'y', 'width', 'height'))
        rects.append((x, y, x + w, y + h))
    for t in re.findall(r'<line\b[^>]*>', svg):
        a = attrs(t)
        x1, y1, x2, y2 = (float(a[k]) for k in ('x1', 'y1', 'x2', 'y2'))
        inside = any(min(x1, x2) >= rx0 - 0.5 and max(x1, x2) <= rx1 + 0.5 and min(y1, y2) >= ry0 - 0.5
                     and max(y1, y2) <= ry1 + 0.5 for rx0, ry0, rx1, ry1 in rects)
        col = parse_colour(a.get('stroke', ''))
        if inside or col is None:
            continue
        c = contrast(col, bg)
        if c < MIN_CONTRAST:
            rep.fail(qid, 'chart', 'a line from (%g,%g) to (%g,%g) is stroked %s, %.2f:1 against the card %s '
                     '(needs %.0f:1; it cannot be seen)' % (x1, y1, x2, y2, a.get('stroke'), c,
                                                           '#%02x%02x%02x' % bg, MIN_CONTRAST))


# ── the bank ─────────────────────────────────────────────────────────────────

def check_bank(rep, bank, ctx, verbose=False):
    used = {}
    for i, q in enumerate(bank):
        qid = 'Q%d' % (i + 1)
        opts = q['options']
        if not (0 <= q['correct'] < len(opts)):
            rep.fail(qid, 'key', 'correct index %r is not an option' % q['correct'])
            continue
        norm = [re.sub(r'\s+', ' ', o).strip().lower() for o in opts]
        if len(set(norm)) != len(norm):
            rep.fail(qid, 'duplicate options', 'two options are the same text: %s' % opts)
        hits = [r for r in RULES if re.search(r[1], q['stem'])]
        if len(hits) != 1:
            rep.fail(qid, 'rule', '%d rules match this question (exactly one must): %r'
                     % (len(hits), q['stem'][:80]))
            continue
        name, _, fn = hits[0]
        used[name] = used.get(name, 0) + 1
        fn(rep, qid, q, ctx)
        if q.get('svg'):
            check_chart_contrast(rep, qid, ctx['charts'][q['svg']]['svg'], ctx['bg'])
        if verbose:
            print('  %-4s %-20s keyed %r' % (qid, name, opts[q['correct']]))
    for name, _, _ in RULES:
        if used.get(name, 0) != 1:
            rep.fail('bank', 'rule', 'rule %r matched %d questions (exactly one)' % (name, used.get(name, 0)))
    for qid, ok, why in ctx.get('marking', []):
        if not ok:
            rep.fail(qid, 'marking', why)


CAPTURE = r"""() => {
  const out = {};
  const oh = window.renderHistogram, ob = window.renderBoxPlot;
  window.renderHistogram = function (bars) { out.args = {bars: bars}; return oh.apply(this, arguments); };
  window.renderBoxPlot = function () { out.args = {five: Array.from(arguments)}; return ob.apply(this, arguments); };
  const charts = {};
  for (const q of QUESTIONS) if (q.svg) { out.args = null; const s = renderSVG(q.svg); charts[q.svg] = {svg: s, args: out.args}; }
  window.renderHistogram = oh; window.renderBoxPlot = ob;
  return {charts: JSON.parse(JSON.stringify(charts)),
          bg: getComputedStyle(document.querySelector('.q-card')).backgroundColor};
}"""

MARK = r"""() => {
  const res = [];
  document.getElementById('questionArea').style.display = 'block';
  for (let i = 0; i < QUESTIONS.length; i++) {
    currentQ = i; showQuestion();
    const btn = document.querySelectorAll('#optionsContainer .option-btn')[QUESTIONS[i].correct];
    btn.click();
    res.push([i, btn.classList.contains('correct')]);
  }
  return {res: res, score: score};
}"""


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
            cap = page.evaluate(CAPTURE)
            page.evaluate('startGame()')
            mk = page.evaluate(MARK)
            browser.close()
            if errors:
                sys.exit('page errors: %s' % '; '.join(errors))
    finally:
        proc.terminate()
        proc.wait()
    marking = [('Q%d' % (i + 1), ok, 'clicking the key %r was not marked correct' % bank[i]['options'][bank[i]['correct']])
               for i, ok in mk['res']]
    if mk['score'] != len(bank):
        marking.append(('bank', False, 'all keys clicked, score %s of %d' % (mk['score'], len(bank))))
    return bank, {'charts': cap['charts'], 'bg': parse_colour(cap['bg']), 'marking': marking}


# ── self-test ────────────────────────────────────────────────────────────────

def selftest(bank, ctx):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank, ctx)

    def find(b, rx):
        return next(q for q in b if re.search(rx, q['stem']))

    def expect(name, fn):
        nonlocal ok
        b, c = copy.deepcopy(bank), copy.deepcopy(ctx)
        fn(b, c)
        rep = Report()
        check_bank(rep, b, c)
        new = [f for f in rep.fails if f not in base.fails]
        caught = bool(new)
        ok = ok and caught
        lines.append('  self-test %-36s %s' % (name, ('caught: ' + new[0][:110]) if caught else '*** MISSED ***'))

    def q32_old(b, c):
        q = find(b, r'Account A: .*Account B:')
        q['options'] = ['Account A by £5.30', 'Account B by £44.70', 'Account A by £24.70',
                        'Both give the same total interest']
        q['correct'] = 1
        q['working'] = ('A: 5000 × 0.035 × 3 = £525.00. B: 5000 × 1.036³ − 5000 = '
                        '£569.70. Account B wins by £44.70.')
    expect("Q32's old options and key (£44.70)", q32_old)

    def q7_old(b, c):
        q = find(b, r'classifies all four')
        others = [i for i in range(len(q['options'])) if i != q['correct']]
        q['options'][others[1]] = 'Discrete, qualitative, continuous, discrete'
    expect("Q7's old option C", q7_old)

    def q1_old(b, c):
        q = find(b, r'interquartile range')
        q['stem'] = re.sub(r'\s*[Uu]sing the \(n \+ 1\)/4 method,?', '', q['stem'])
    expect('Q1 with no quartile method named', q1_old)

    def q9_old(b, c):
        q = find(b, r'more than half the class scored above')
        q['options'] = ['Yes — by definition, 50% of values lie at or above the median',
                        'No — the median means most students scored below 51',
                        'Yes — the upper quartile is above 51 so most students scored above it',
                        'Cannot be determined from a box plot']
        q['correct'] = 0
    expect("Q9's old key (Yes)", q9_old)

    def q9_whiskers(b, c):
        q = find(b, r'more than half the class scored above')
        svg = c['charts'][q['svg']]['svg']
        c['charts'][q['svg']]['svg'] = re.sub(r'(<line\b[^>]*?)stroke="#[0-9a-fA-F]{6}"', r'\1stroke="#1e293b"', svg)
    expect("Q9's old whisker colour (#1e293b)", q9_whiskers)

    def wrong_key(b, c):
        q = find(b, r'compound interest per annum')
        q['correct'] = (q['correct'] + 1) % len(q['options'])
    expect('wrong key (Q20)', wrong_key)

    def q4_chart(b, c):
        q = find(b, r'How many patients waited between')
        c['charts'][q['svg']]['args']['bars'][1]['fd'] = 3.0
    expect('Q4 histogram bar changed', q4_chart)
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

    bank, ctx = load_bank()
    rep = Report()
    check_bank(rep, bank, ctx, args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, ctx)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    part = (r_salary, r_reaction)
    print('\n%s: %d FAIL(s); %d questions: %d computed, %d computed in part and pinned, %d pinned; '
          'every key clicked through the page'
          % ('PASS' if ok else 'FAILED', len(rep.fails), len(bank),
             sum(1 for r in RULES if r[2] is not r_pinned and r[2] not in part),
             sum(1 for r in RULES if r[2] in part), sum(1 for r in RULES if r[2] is r_pinned)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
