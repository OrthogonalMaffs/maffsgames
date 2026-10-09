#!/usr/bin/env python3
# ci-line: Better Value (every keyed figure and explanation figure recomputed, one true card in four, every card marked in Chromium) |
"""Better Value: every figure in every keyed conclusion and explanation recomputed; every card marked in Chromium.

The game (70 items: gcse 20, core 50) shows two deals and four conclusion cards, one keyed correct, and on a
wrong pick the explanation. Its bank was keyed by hand with no verifier; the resit audit of 4 Oct 2026 found
five Core conclusions whose figures were wrong (better-value-r-001 .. r-005): bv_core_009's bank loan costed
with no repayments (2000 x 1.08^2) and keyed dearer; bv_core_031 calling the rival cheaper per month at
£32 vs £31.33; bv_core_036's £518 (20 x £22 + 3 x £48 = £584; the 3 missed tickets are among the 20);
bv_core_037 keying premium's ROI as higher (344% vs 331%); bv_core_049's 8.8 hours (8.54). And r-009:
bv_core_033's explanation mixing pounds and pence (0.04d = 17 gives d = 425).

REVIEW gives each item, from its own numbers: the values its keyed conclusion must state (KEY), the other
values its explanation may state (ALSO), the verdict words the keyed card must carry and no other card may
(WIN), and, where the keyed card compares two figures "x vs y", which way round they must be (ORDER). Then:
  - exactly one card is keyed correct, and only it carries WIN;
  - every KEY value appears in the keyed card, to the precision it is printed (half up);
  - every figure in the keyed card and the explanation is a given (in the scenario or the deal cards), a
    KEY or ALSO value at its printed precision (pounds or pence), or a small count (40 or less);
  - every "Set equal:" line in an explanation solves (SymPy) to the value it states;
  - bv_core_009's stated repayment is the 8% APR (effective annual) payment on £2,000 over 24 months, to
    the penny;
  - in Chromium (390x844) every card of every item is clicked through pickConclusion(): the keyed card is
    marked right, every other card wrong, and the wrong pick shows that item's explanation.
A self-test plants three audit faults back into a copy of the page (r-003's £518, r-004's ROI key, r-005's
8.8 hours); each must FAIL naming its item.

    python scripts/verify-better-value.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP, getcontext
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

getcontext().prec = 40
SLUG = 'better-value'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'gcse': 20, 'core': 50}


def loan_payment(principal, apr, months):
    """The level monthly payment at an APR (effective annual rate), to the penny, half up."""
    m = (1 + D(apr)) ** (D(1) / D(12)) - 1
    p = D(principal) * m / (1 - (1 + m) ** -months)
    return p.quantize(D('0.01'), rounding=ROUND_HALF_UP)


P009 = loan_payment(2000, '0.08', 24)


def r(id_, key=(), also=(), win='', order=None):
    return id_, {'key': [F(str(k)) if not isinstance(k, F) else k for k in key],
                 'also': [F(str(a)) if not isinstance(a, F) else a for a in also], 'win': win, 'order': order}


# Each item from its own numbers (the deal cards and the scenario). ORDER: 'lt' when the keyed card's first
# "x vs y" has x < y (the cheaper side first), 'gt' when x > y.
REVIEW = dict([
    r('bv_gcse_001', [9 * 8, 3 * 21], [72 - 63], 'Slice House is cheaper', 'lt'),
    r('bv_gcse_002', [F('5.99') * 12], [F('71.88') - F('59.99')], 'Plan B is cheaper', 'lt'),
    r('bv_gcse_003', [F('4.50') + 2], [], 'Shop B is cheaper overall', 'lt'),
    r('bv_gcse_004', [5 * 80, 40 + 5 * 70], [5 * 70], 'Park B is cheaper', 'lt'),
    r('bv_gcse_005', [5 * F('2.50')], [F('12.50') - 6], 'Homemade is cheaper', 'lt'),
    r('bv_gcse_006', [3 + 5 * 2], [5 * 2, 1], 'Quick Cabs is cheaper', 'lt'),
    r('bv_gcse_007', [F('18.50') + F('3.99')], [23 - (F('18.50') + F('3.99'))], 'online store is cheaper', 'lt'),
    r('bv_gcse_008', [4 * 11], [44 - 40], 'Vue is cheaper', 'lt'),
    r('bv_gcse_009', [38 + F('4.99') + 3], [F('45.99') - 45], 'shop is cheaper overall', 'lt'),
    r('bv_gcse_010', [10 + 100 * F('0.20')], [100 * F('0.20')], 'unlimited plan is cheaper', 'lt'),
    r('bv_gcse_011', [25 + F('3.50')], [F('3.50') - 2], 'shop is cheaper', 'lt'),
    r('bv_gcse_012', [F(200, 40), F(10 * (5 + 8), 40)], [F(40, 4), 5 + 8, 10 * 13], 'Cars are cheaper — £3.25', 'lt'),
    r('bv_gcse_013', [20 + F('4.99')], [26 - (20 + F('4.99'))], 'deal store is cheaper overall', 'lt'),
    r('bv_gcse_014', [F(3, 2), F('6.50') / 5], [], 'Bag B is better value', 'lt'),
    r('bv_gcse_015', [F('3.60') / 12, F(5, 20)], [], 'Pack B is better value', 'lt'),
    r('bv_gcse_016', [F(54, 6), F(80, 9)], [], 'Job A pays better per hour', 'gt'),
    r('bv_gcse_017', [F('2.40') / 300, F('3.50') / 500], [], 'Bottle B is better value', 'lt'),
    r('bv_gcse_018', [F(8, 6), F(6, 4)], [], 'Car Park B is cheaper per hour', 'lt'),
    r('bv_gcse_019', [F(30) / F('2.50')], [], 'worth it if you eat 12 or more'),
    r('bv_gcse_020', [F(15, 1)], [16], 'saves money after more than 15 bottles'),
    r('bv_core_001', [12 * 35, 60 + 12 * 28], [12 * 28], 'Gym B is better value', 'lt'),
    r('bv_core_002', [18 * 29, 49 + 18 * 24], [18 * 24], 'Provider B is better value', 'lt'),
    r('bv_core_003', [260 * F('3.20'), 180 + 260 * F('0.40')], [260 * F('0.40')], 'subscription machine is better value', 'lt'),
    r('bv_core_004', [12 * 74], [12 * 74 - 820], 'Insurer A is better value', 'lt'),
    r('bv_core_005', [500 * F('0.45'), 5 * 38], [], 'Supplier B is better value', 'lt'),
    r('bv_core_006', [2 * 45], [2 * 45 - 75], 'annual pass is better value for two visits', 'lt'),
    r('bv_core_007', [36 * 120, 36 * (85 + 2000 * F('0.02'))], [85 + 2000 * F('0.02'), 2000 * F('0.02'), 36 * 125 - 36 * 120],
      'Lease A is better value', 'lt'),
    r('bv_core_008', [350 * F('0.28'), 350 * F('0.24') + 12], [350 * F('0.24')], 'Tariff B is better value', 'lt'),
    r('bv_core_009', [24 * F(str(P009)), 24 * 95], [F(str(P009)), 24 * 95 - 24 * F(str(P009)), F('1.08'), 2000 * F('1.08') ** 2],
      'The bank loan is cheaper', 'lt'),
    r('bv_core_010', [24 * 12 + 280, 30 + 24 * 25], [24 * 25, 24 * 12], 'SIM-only deal is better value', 'lt'),
    r('bv_core_011', [], [599 - 549], 'rival store is better value', 'lt'),
    r('bv_core_012', [3200 * F('0.27'), 3200 * F('0.31') - 50], [3200 * F('0.31')], 'standard tariff is better value', 'lt'),
    r('bv_core_013', [11 * 42, 12 * 40], [], 'free month deal is better value', 'lt'),
    r('bv_core_014', [], [2 * F('1.25'), 2 * F('1.40'), 4 * F('1.25'), 3 * F('1.40')],
      'Supermarket A is better value per bottle if you only need 2', 'lt'),
    r('bv_core_015', [28 + 6], [], 'second-hand book is better value', 'lt'),
    r('bv_core_016', [600 + 280], [], 'Decorator A was better value', 'lt'),
    r('bv_core_017', [F('3.60') / F('1.2'), F('6.75') / F('2.5')], [], 'large box is better value', 'lt'),
    r('bv_core_018', [F('6.84') / F('4.55')], [F('1.52') - F('6.84') / F('4.55')], 'Garage B is cheaper', 'lt'),
    r('bv_core_019', [F(18000, 12 * 5)], [12 * 5, 320 - 300], 'Contract A pays better', 'gt'),
    r('bv_core_020', [F('1.89') / F('0.75'), F('2.99') / F('1.25')], [F('0.75')], 'Brand B is better value', 'lt'),
    r('bv_core_021', [F(4200, 350), F(5100, 510)], [], 'January had better average giving', 'gt'),
    r('bv_core_022', [F(350, 40), F(420, 50)], [], 'Car B is more fuel efficient', 'gt'),
    r('bv_core_023', [F(240, 8), F(175, 6)], [], 'Builder A charges more per hour', 'gt'),
    r('bv_core_024', [F(85) / (F('2.80') - F('0.30'))], [F('2.80') - F('0.30')], 'After 34 coffees'),
    r('bv_core_025', [10], [F('9.60') / 3, F(30) / (F('9.60') / 3)], 'at least 10 return journeys'),
    r('bv_core_026', [F(4500, 380)], [12], 'pay for themselves after approximately 11.8 years'),
    r('bv_core_027', [F(8) / (F('0.15') - F('0.05'))], [F('0.15') - F('0.05')], 'above 80 minutes'),
    r('bv_core_028', [], [F('9.99') / F('12.50')], 'at least 1 film per month'),
    r('bv_core_029', [F(5000, 1200)], [5 * 1200, 5 * 1200 - 5000], 'after approximately 4.2 years'),
    r('bv_core_030', [F(120) / (F('0.12') - F(18, 200))], [F(18, 200), F('0.12') - F(18, 200)], 'more than 4,000 pages'),
    r('bv_core_031', [18 * 28 + 60, 12 * 32, F(18 * 28 + 60, 18)], [18 * 28], 'Per month the advertised deal is cheaper', 'lt'),
    r('bv_core_032', [1200 + 145 + 36 * F('5.99')], [36 * F('5.99'), 1200 + 145 + 36 * F('5.99') - 1050],
      'cash purchase is better value', 'lt'),
    r('bv_core_033', [F(42 - 25, 28 - 24)], [28 - 24, 42 - 25, 12 * 28, 12 * 28 + 25, 12 * 24, 12 * 24 + 42,
                                             (12 * 28 + 25) - (12 * 24 + 42), F((12 * 28 + 25) - (12 * 24 + 42)) * 365 / 100],
      'better value above 4.25 kWh per day'),
    r('bv_core_034', [F('74.99') + F('9.99')], [F('74.99') + F('4.99')], 'rival site is better value', 'lt'),
    r('bv_core_035', [12 * 12 + 60, 12 * 8 + 150 + 2 * 80], [12 * 12, 12 * 8, 2 * 80, (12 * 8 + 150 + 160) - (12 * 12 + 60)],
      'Policy A is better value', 'lt'),
    r('bv_core_036', [20 * 22 + 3 * 48], [20 * 22, 3 * 48, 20 * 48, 20 * 48 - (20 * 22 + 3 * 48)],
      'Advance tickets are better value', 'lt'),
    r('bv_core_037', [1120 - 260, 800 - 180, F(800 - 180, 180) * 100, F(1120 - 260, 260) * 100], [860 - 620],
      'Premium flyers give more net profit', 'gt'),
    r('bv_core_038', [F(1200, 195), F(450, 68)], [25 * 195, 25 * 68], 'Cavity wall insulation has the shorter payback', 'lt'),
    r('bv_core_039', [8], [12 * 45, 75 + 12 * 35, F(75, 45 - 35), 12 * (45 - 35), 12 * 35], 'rolling gym is better value from month 8'),
    r('bv_core_040', [250 * 55, 250 * 48 + 250 * 5 + 50 * 20], [5 * 50, 250 * 48, 250 * 5, 50 * 20, 500],
      'Nursery A is better value', 'lt'),
    r('bv_core_041', [36 * 350 + 3 * 900, 12000 + 3 * 800 + 3 * 1200], [3 * 800, 3 * 1200, 36 * 350, 3 * 900, 2700],
      'Leasing is better value over 3 years', 'lt'),
    r('bv_core_042', [500 * F('0.03')], [500 - 15], '0% credit card is better value'),
    r('bv_core_043', [], [F(16, 30), F(16, 30) * F('4.55'), F('3.76'), F('3.76') + 5, 22 * (F('3.76') + 5),
                          F(16, 30) * F('4.55') * F('1.55'), 193], 'bus pass is better value', 'lt'),
    r('bv_core_044', [], [F('29.99') * 12, 360, 250 - 80], 'gives £80 of usable value for £29.99'),
    r('bv_core_045', [3600 * F('0.26'), 1800 * F('0.29') + 1800 * F('0.33')], [1800, 1800 * F('0.29'), 1800 * F('0.33'), 180],
      'fixed tariff saves money', 'lt'),
    r('bv_core_046', [F(28000 * 5, 6 * 12) - 650, F(34000 * 5, 6 * 12) - 1200],
      [F(28000, 6), F(28000 * 5, 6), F(28000 * 5, 6 * 12), F(34000, 6), F(34000 * 5, 6), F(34000 * 5, 6 * 12)],
      'Manchester job gives more disposable income', 'gt'),
    r('bv_core_047', [9 * 15, 13 * 10], [5], 'Cleaner B is better value overall'),
    r('bv_core_048', [480 - 340], [500 - 250], 'Insurer A is better value'),
    r('bv_core_049', [(20 * 15 + F('180') / F('4.33')) / 40], [20 * 15, F('180') / F('4.33'), 20 * 15 + F('180') / F('4.33')],
      'Hiring becomes cheaper above approximately 8.5 hours'),
    r('bv_core_050', [825 - 790], [30 * F('27.50'), 40 + 30 * 25, 30 * F('0.75') * F('11.44'),
                                   40 + 30 * 25 + 30 * F('0.75') * F('11.44'), F('0.75')],
      'Meal prep saves £35 in direct costs'),
])
AUDIT = {'bv_core_009': 'better-value-r-001', 'bv_core_031': 'better-value-r-002', 'bv_core_036': 'better-value-r-003',
         'bv_core_037': 'better-value-r-004', 'bv_core_049': 'better-value-r-005', 'bv_core_033': 'better-value-r-009'}
CONSTANTS = [F(52), F(12), F('4.33'), F(365), F(100)]   # weeks, months, weeks per month, days, pence
SMALL = 40          # a count ("18 months", "year 12", "from bottle 16") is not checked as a figure

NUM = re.compile(r'(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(p\b)?')


def figures(text):
    """[(token, Fraction value, decimals, pence)] for every number in a text."""
    out = []
    for m in NUM.finditer(text):
        whole, frac, pence = m.group(1).replace(',', ''), m.group(2) or '', bool(m.group(3))
        out.append((m.group(0), F(whole + frac), len(frac) - 1 if frac else 0, pence))
    return out


def shown(v, dp):
    """v (a Fraction) rounded half up to dp places, as a Fraction."""
    q = D(v.numerator) / D(v.denominator)
    return F(str(q.quantize(D(1).scaleb(-dp), rounding=ROUND_HALF_UP)))


def matches(tok, values):
    _, val, dp, pence = tok
    for v in values:
        for cand in ((v, v * 100) if pence else (v, v * 100, v / 100)):
            if shown(cand, dp) == val:
                return True
    return False


def givens(q):
    text = q['scenario'] + ' ' + ' '.join('%s %s' % (d['key'], d['value'])
                                          for o in ('optionA', 'optionB') if o in q for d in q[o]['details'])
    return [v for _, v, _, _ in figures(text)] + CONSTANTS


SET_EQUAL = re.compile(r'Set equal: ([^→]+?) →')


def check_equations(fails, w, q):
    """Each 'Set equal: lhs = rhs →' line solves to the value its '→ x = v' states."""
    for m in SET_EQUAL.finditer(q['explanation']):
        lhs, rhs = m.group(1).split('=')
        tail = q['explanation'][m.end() - 1:]          # from the arrow that ends the equation
        sol = re.search(r'→ ([a-z]) = (\d+(?:\.\d+)?)', tail)
        if not sol:
            fails.append('%s: "Set equal: %s" states no solution' % (w, m.group(1)))
            continue
        var = sp.Symbol(sol.group(1))
        expr = lambda s: sp.sympify(re.sub(r'(\d)\s*([a-z])', r'\1*\2', s.replace('£', '').replace('p', '')),
                                     locals={var.name: var}, rational=True)
        try:
            got = sp.solve(sp.Eq(expr(lhs), expr(rhs)), var)
        except Exception as e:
            fails.append('%s: cannot read "Set equal: %s" (%s)' % (w, m.group(1), e))
            continue
        val = F(sol.group(2))
        dp = len(sol.group(2).split('.')[1]) if '.' in sol.group(2) else 0
        if len(got) != 1 or shown(F(str(sp.Rational(got[0]))), dp) != val:
            fails.append('%s: "Set equal: %s" solves to %s, not %s = %s' % (w, m.group(1), got, var, sol.group(2)))


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs REVIEW extended)' % (counts, COUNTS))
        return
    seen = set()
    for lv in COUNTS:
        for q in bank[lv]:
            w = '%s%s' % (q['id'], ' (%s)' % AUDIT[q['id']] if q['id'] in AUDIT else '')
            if q['id'] not in REVIEW:
                fails.append('%s: not in REVIEW' % w)
                continue
            seen.add(q['id'])
            rv = REVIEW[q['id']]
            cards = q['conclusions']
            keyed = [c['text'] for c in cards if c['correct'] is True]
            if len(cards) != 4 or len(keyed) != 1 or len({c['text'] for c in cards}) != 4:
                fails.append('%s: %d cards, %d keyed correct, %d distinct' % (w, len(cards), len(keyed), len({c['text'] for c in cards})))
                continue
            key = keyed[0]
            if rv['win'] not in key:
                fails.append('%s: the keyed card must say "%s": %r' % (w, rv['win'], key))
            for c in cards:
                if c['correct'] is not True and rv['win'] in c['text']:
                    fails.append('%s: a wrong card also says "%s": %r' % (w, rv['win'], c['text']))
            toks = figures(key)
            for v in rv['key']:
                if not any(matches(t, [v]) for t in toks):
                    fails.append('%s: the keyed card should state %s: %r' % (w, float(v), key))
            allowed = givens(q) + rv['key'] + rv['also']
            for where, text in (('keyed card', key), ('explanation', q['explanation'])):
                for t in figures(text):
                    if t[1] <= SMALL and t[2] == 0 and not t[3]:
                        continue
                    if not matches(t, allowed):
                        fails.append('%s: the %s states %s, which is not a given or a recomputed figure: %r'
                                     % (w, where, t[0], text))
            if rv['order']:
                m = re.search(r'£?([\d,]+(?:\.\d+)?)p?(?:/[a-z]+| per [a-z]+| [a-z]+)*? vs (?:approximately )?£?([\d,]+(?:\.\d+)?)', key)
                if m:
                    x, y = F(m.group(1).replace(',', '')), F(m.group(2).replace(',', ''))
                    if (rv['order'] == 'lt') != (x < y):
                        fails.append('%s: the keyed card compares %s vs %s the wrong way round for "%s"'
                                     % (w, m.group(1), m.group(2), rv['win']))
            check_equations(fails, w, q)
            if q['id'] == 'bv_core_009':
                rep = ' '.join(d['value'] for d in q['optionA']['details'])
                if '£%s/month' % P009 not in rep:
                    fails.append('%s: the bank loan must state its repayment, £%s/month (8%% APR over 24 months): %r'
                                 % (w, P009, rep))
    for id_ in sorted(set(REVIEW) - seen):
        fails.append('%s: in REVIEW but not in the bank' % id_)


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.scrollTo = () => 0;
  const out = [];
  for (const lv of ['gcse', 'core']) QUESTIONS[lv].forEach((q) => {
    q.conclusions.forEach((c) => {
      currentQuestions = [q]; qIndex = 0; score = 0; currentLevel = lv;
      renderQuestion();
      const card = [...document.querySelectorAll('#conclusionsGrid .conclusion-card')].find(x => x.textContent === c.text);
      if (!card) { out.push([q.id, c.text, 'not on screen']); return; }
      pickConclusion(card);
      const right = card.classList.contains('correct-pick'), wrong = card.classList.contains('incorrect-pick');
      if (right !== (c.correct === true) || wrong === right) out.push([q.id, c.text, right ? 'marked right' : 'marked wrong']);
      if (!right && document.getElementById('explanationText').textContent !== q.explanation)
        out.push([q.id, c.text, 'the wrong pick does not show the explanation']);
    });
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            for id_, text, what in page.evaluate(SWEEP_JS):
                fails.append('%s in Chromium: card %r %s' % (id_, text[:60], what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('bv_core_036', 'r-003: £518 keyed', "total \\u00a3584 vs", "total \\u00a3518 vs"),
    ('bv_core_037', 'r-004: premium keyed the better ROI',
     "Premium flyers give more net profit \\u2014 \\u00a3860 vs \\u00a3620 for standard, though standard has the higher "
     "return on investment (344% vs 331%)",
     "Premium flyers give better return on investment \\u2014 net profit \\u00a3860 vs \\u00a3620 for standard"),
    ('bv_core_049', 'r-005: 8.8 hours', "above approximately 8.5 hours per week", "above approximately 8.8 hours per week"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d items, every keyed and explanation figure recomputed, every card clicked in Chromium'
          % (SLUG, sum(len(bank[k]) for k in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-34s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-34s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
