#!/usr/bin/env python3
# ci-line: Estimation Golf (every key recomputed from its question, exactly, at its own precision; every key scores a Hole in One in Chromium) |
"""Estimation Golf: every key recomputed from its own question; every key typed scores a Hole in One in Chromium.

The game (56 items: year6 20, ks3 9, gcse 9, alevel 9, level4 9) asks for an estimate and scores it by how close
it is (BANDS: exact is a Hole in One, then 1%, 5%, 10% ...); the result panel shows "Actual answer". Its keys
were typed by hand with no verifier; the resit audit of 4 Oct 2026 found two wrong ones: level4[7] (a cylinder
60 mm across, 200 mm long, in cm^3) keyed 565.2, which is pi taken as 3.14 though nothing says so (180 pi =
565.49; estimation-golf-r-001), and alevel[1] (the gradient of x^3 at 3 by first principles with h = 0.001)
keyed 27, the limit, not the estimate asked for, ((3.001)^3 - 27) / 0.001 = 27.009001 (r-002).

KEYS computes every non-year6 key here, exactly (SymPy, fractions), from the numbers in its question, each
pinned to the words it reads; year6's facts are a reviewed table, pinned the same way. pi is the true pi unless
the question or its hint says pi = 3.14. Each key must equal its value rounded half up to the key's own decimal
places (or to the significant figures or rounding the question asks for), and the two audited items must be
keyed at their stated precision (alevel[1]: "3 decimal places"; level4[7]: 2 d.p.). The proximity scoring
itself is left alone (Jon's design; audit F3, F4 are open). In Chromium (390x844) every key is typed through
the game's own loadHole() and submitAnswer(): each must score a Hole in One, and the two old keys (27, 565.2)
must not.
A self-test plants the audit's two keys back; each must FAIL naming its item.

    python scripts/verify-estimation-golf.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'estimation-golf'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'year6': 20, 'ks3': 9, 'gcse': 9, 'alevel': 9, 'level4': 9}
R = sp.Rational


def PI(q):
    """pi as the question uses it: 3.14 only where the question or its hint says so."""
    return R(314, 100) if re.search(r'π\s*(≈|=)\s*3\.14', q['q'] + ' ' + q['hint']) else sp.pi


def sig(v, k):
    """v rounded half up to k significant figures."""
    d = Decimal(str(sp.N(v, 40)))
    return R(str(d.quantize(Decimal(1).scaleb(d.adjusted() - k + 1), rounding=ROUND_HALF_UP)))


def dp(v, k):
    """v rounded half up to k decimal places (k < 0: to tens, hundreds ...)."""
    d = Decimal(str(sp.N(v, 40)))
    return R(str(d.quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP)))


# (words the question must carry, exact value or rounding of it, precision rule)
# rule: 'own' = the key rounded to its own decimal places must equal the value; 'exact' = the value as is.
KEYS = {
    'year6': [(w, R(a), 'exact') for w, a in [
        ('days are in a year', 365), ('minutes are in an hour', 60), ('centimetres are in a metre', 100),
        ('players are on a football team', 11), ('teeth does an adult have', 32), ('legs does a spider have', 8),
        ('hours are in a day', 24), ('weeks are in a year', 52), ('bones are in the human body', 206),
        ('seconds are in a minute', 60), ('sides does a hexagon have', 6), ('tall is a door in centimetres', 200),
        ('months have exactly 30 days', 4), ('grams are in a kilogram', 1000), ('millilitres are in a litre', 1000),
        ('slices are in a typical large pizza', 8), ('letters are in the English alphabet', 26),
        ('How many continents are there', 7), ('pupils are in a typical school class', 30),
        ('dots are on a standard die', sum(range(1, 7)))]],
    'ks3': [
        ('Round 3,847 to the nearest hundred', dp(3847, -2), 'exact'),
        ('15% of 200', R(15, 100) * 200, 'exact'),
        ('seconds in one day', 60 * 60 * 24, 'exact'),
        ('√50 to 1 decimal place', dp(sp.sqrt(50), 1), 'exact'),
        ('millimetres in 3.5 metres', R(35, 10) * 1000, 'exact'),
        ('8 pencils cost 96p', R(96, 8), 'exact'),
        ('60 mph. How many miles in 30 minutes', 60 * R(1, 2), 'exact'),
        ('rectangle 7 cm × 9 cm', 63, 'exact'),
        ('12 apples weighs about 1.8 kg', R(1800, 12), 'exact'),
    ],
    'gcse': [
        ('Round 0.004857 to 2 significant figures', sig(R('0.004857'), 2), 'exact'),
        ('23% of 840', R(23, 100) * 840, 'exact'),
        ('heartbeats in a year (assume 70 bpm)', 70 * 60 * 24 * 365, 'exact'),
        ('∛125', 5, 'exact'),
        ('75 mph to km/h (1 mile ≈ 1.6 km)', 75 * R(16, 10), 'exact'),
        ('serves 4 and needs 320g flour', R(320, 4) * 7, 'exact'),
        ('90-litre bath at 6 litres/minute', R(90, 6), 'exact'),
        ('circle with radius 7 cm. (π ≈ 3.14)', R(314, 100) * 49, 'exact'),
        ('840 items per hour', 840 * R(75, 10), 'exact'),
    ],
    'alevel': [
        ('e to 4 significant figures', sig(sp.E, 4), 'exact'),
        ('gradient of y = x³ at x = 3', dp(((3 + R(1, 1000)) ** 3 - 27) / R(1, 1000), 3), 'exact'),
        ('∫₀¹ x² dx using the trapezium rule with 2 strips', R(1, 4) * (0 + 2 * R(1, 4) + 1), 'exact'),
        ('ln(10) to 2 decimal places', dp(sp.log(10), 2), 'exact'),
        ('speed (m/s) of sound in air at 20°C (≈ 343 m/s)', 343, 'exact'),
        ('a = 3, r = 0.5. Estimate the sum to infinity', 3 / (1 - R(1, 2)), 'exact'),
        ('sin(30°)', sp.sin(sp.pi / 6), 'exact'),
        ('radius 4 cm. Estimate its volume to the nearest whole number', None, 'sphere'),
        ('8^(2/3)', R(8) ** R(2, 3), 'exact'),
    ],
    'level4': [
        ('peak voltage 325 V', 325 / sp.sqrt(2), 'own'),
        ('length 2 m expands by 0.0024 m when heated 100°C', R(24, 10000) / (2 * 100) * 10 ** 6, 'exact'),
        ('velocity 340 m/s and wavelength 0.5 m', 340 / R(1, 2), 'exact'),
        ('length 4 m has a UDL of 5 kN/m', 5 * R(16, 8), 'exact'),
        ('100μF capacitor at 50 Hz', None, 'reactance'),
        ('falls from rest', R(981, 100) * 3, 'exact'),
        ('input power 500 W and output power 375 W', R(375, 500) * 100, 'exact'),
        ('diameter 60 mm and length 200 mm. Estimate its volume in cm³', None, 'cylinder'),
        ('0.1 m thick brick wall, area 2 m², thermal conductivity 0.6', R(1, 10) / (R(6, 10) * 2), 'own'),
    ],
}
AUDIT = {('level4', 7): 'estimation-golf-r-001', ('alevel', 1): 'estimation-golf-r-002'}
STATED = {('alevel', 1): 3, ('level4', 7): 2}      # the precision each audited key is held to
SAYS = {('alevel', 1): ['(f(3 + h) − f(3)) ÷ h with h = 0.001', 'Give your answer to 3 decimal places']}   # method and precision stated (r-002)
OLD = {('alevel', 1): '27', ('level4', 7): '565.2'}  # the audit's wrong keys: must not score a Hole in One


def places(x):
    s = repr(x) if isinstance(x, float) else str(x)
    return len(s.split('.')[1]) if '.' in s and 'e' not in s else 0


def value(lv, i, q, rule, v):
    if rule == 'sphere':
        return dp(R(4, 3) * PI(q) * 4 ** 3, 0)
    if rule == 'reactance':
        return 1 / (2 * PI(q) * 50 * R(100, 10 ** 6))
    if rule == 'cylinder':
        return PI(q) * 3 ** 2 * 20
    return v


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (a change needs KEYS reviewed)' % (counts, COUNTS))
        return
    for lv in COUNTS:
        for i, q in enumerate(bank[lv]):
            w = '%s[%d] (%s)%s' % (lv, i, q['q'], ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            words, v, rule = KEYS[lv][i]
            if words not in q['q']:
                fails.append('%s: the question must say "%s" for its key to hold' % (w, words))
                continue
            for words in SAYS.get((lv, i), []):
                if words not in q['q']:
                    fails.append('%s: the question must state "%s"' % (w, words))
            exact = value(lv, i, q, rule, v)
            key = R(repr(q['answer']) if isinstance(q['answer'], float) else str(q['answer']))
            k = STATED.get((lv, i))
            if k is not None:
                want = dp(exact, k)
            elif rule in ('own', 'reactance', 'cylinder'):
                want = dp(exact, places(q['answer']))
            else:
                want = sp.nsimplify(exact)
            if key != want:
                fails.append('%s: keyed %s, the answer is %s (%s)' % (w, q['answer'], want, sp.N(exact, 10)))


SWEEP_JS = r"""(old) => {
  window.setTimeout = () => 0;
  const out = [];
  const play = (q, typed) => {
    roundQuestions = [q]; hole = 0; scores = []; hintUsed = [false];
    buildScorecard(); loadHole();
    document.getElementById('answerInput').value = typed;
    submitAnswer();
    return document.getElementById('resultGrade').textContent;
  };
  for (const lv of Object.keys(QUESTIONS)) QUESTIONS[lv].forEach((q, i) => {
    const got = play(q, String(q.answer));
    if (!/Hole in One/.test(got)) out.push([lv, i, String(q.answer), got]);
    const o = old[lv + '|' + i];
    if (o !== undefined && o !== String(q.answer)) {
      const g2 = play(q, o);
      if (/Hole in One/.test(g2)) out.push([lv, i, o, 'the audit\'s wrong key still scores ' + g2]);
    }
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
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
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
            old = {'%s|%d' % k: v for k, v in OLD.items()}
            for lv, i, typed, what in page.evaluate(SWEEP_JS, old):
                fails.append('%s[%d]%s in Chromium: typed %s: %s' % (lv, i, ' (%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '', typed, what.strip()))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def run(html):
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    return fails, sum(len(bank[k]) for k in COUNTS) if bank else 0


PLANTS = [
    ('level4[7]', 'r-001: the cylinder keyed 565.2 (pi = 3.14)', 'answer: 565.49,', 'answer: 565.2,'),
    ('alevel[1]', 'r-002: the gradient keyed 27 (the limit)', 'answer: 27.009,', 'answer: 27,'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='check this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, count = run(html)
    print('%s: %d items, every key recomputed, every key typed in Chromium' % (SLUG, count))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-44s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep, _ = run(html.replace(old, new))
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
