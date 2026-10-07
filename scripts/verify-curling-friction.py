#!/usr/bin/env python3
# ci-line: B4 | Curling Friction (every numerical key recomputed exactly from its own context, every option checked, every item marked in Chromium) |
"""Curling Friction: every numerical key recomputed exactly from its own context; every option checked; every item
marked in Chromium.

The game (multiple choice: alevel and level4) asks friction, SUVAT, momentum and collision questions about curling
stones. Its bank was keyed by hand; the tranche 5 audit of 6 Oct 2026 found an initial speed keyed with g dropped
(sqrt(4.96) for sqrt(13.6)), a "speed" keyed -4 m/s with the true speed 4 m/s marked wrong, and a stone that
"sits on ice" asked for its friction force (a stone at rest with no applied force has none; mu R is the friction
while it slides).

TARGETS below gives each item's answer as a computation from the numbers its context states (Fraction-exact), or,
for a worded answer, the reviewed key with its reason. Then:
  numerical: the key equals the target (an exact form such as sqrt(13.6) must equal it exactly, and a decimal
    after "approx" must be it rounded half up at the places shown; a rounded key needs its precision stated in
    the context or ask, SR-1); no wrong option equals the target, exactly or at the key's precision (SR-16);
    no two options are equal in value; a wrong option keeps the key's unit;
  worded: the key is the reviewed one;
  friction: a context that asks for a friction force from mu R must say the stone slides (t5-006);
  in Chromium (390x844) every item is shown through the game's own showQ() and every option clicked through
    handle(): the key marked right, the others wrong; a wrong answer shows the worked solution and the shared
    Next control (MaffsNext, canon 7.6), not a hand-rolled button.
A self-test plants three of the audit's own faults back into a copy of the page (t5-001: sqrt(4.96) as the key;
t5-002: the hammer's "speed" keyed -4; t5-006: "sits on ice"); each must FAIL naming its item.

    python scripts/verify-curling-friction.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'curling-friction'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')


def N(v, unit, prec=None):
    """A numerical target: v exact (Fraction or SymPy), its unit, and the precision the item states."""
    return ('num', sp.nsimplify(v) if not isinstance(v, F) else sp.Rational(v.numerator, v.denominator), unit, prec)


def T(key, why):
    return ('text', key, why)


g98, g10, g981 = F(98, 10), F(10), F(981, 100)
TARGETS = {
    'alevel': [
        N(F(4, 100) * 20 * g98, 'N'),                              # 0 F = mu m g
        N(F(3, 100) * 19 * g98, 'N'),                              # 1
        N(F(588, 100) / (20 * g98), ''),                           # 2 mu = F / (m g)
        N(F(5, 100) * 196, 'N'),                                   # 3 F = mu R
        N(F(4, 100) * g98, 'm/s^2'),                               # 4 a = mu g
        N(F(294, 1000) / g98, ''),                                 # 5
        N((F(4, 100) - F(2, 100)) * 20 * g98, 'N'),                # 6
        N(F(3, 100) * F(196, 10) * g10, 'N'),                      # 7
        T('\\mu g', 'F = mu m g and F = m a, so a = mu g'),        # 8
        T('Friction', 'the only horizontal force on a stone sliding without air resistance'),   # 9
        N(20 * g98, 'N'),                                          # 10
        T('mg', 'on a flat surface with no other vertical force, R = mg'),                    # 11
        N(F(4) ** 2 / (2 * F(4, 10)), 'm'),                        # 12 s = u^2 / 2a
        N(F(3) ** 2 / (2 * F(3, 10)), 'm'),                        # 13
        N(F(5) ** 2 / (2 * F(5, 10)), 'm'),                        # 14
        N(sp.sqrt(sp.Rational(2) * sp.Rational(3, 10) * 30), 'm/s'),   # 15 u = sqrt(2 a s)
        N(F(4) / F(4, 10), 's'),                                   # 16 t = u / a
        N(F(6) ** 2 / (2 * F(4, 100) * g10), 'm'),                 # 17
        N(F(4) ** 2 / (2 * F(2, 100) * g10) - F(4) ** 2 / (2 * F(4, 100) * g10), 'm'),   # 18
        N(sp.sqrt(2 * sp.Rational(1, 2) * 25), 'm/s'),             # 19
        N(F(3) ** 2 / (2 * F(45, 2)) / g10, ''),                   # 20 mu = u^2 / (2 s g)
        N(sp.sqrt(4 + 2 * sp.Rational(4, 100) * 10 * 12), 'm/s'),  # 21 u^2 = v^2 + 2 a s (t5-001)
        N(2 * F(40) / 10, 'm/s'),                                  # 22 s = (u + 0) t / 2
        N(5 - F(1, 2) * 6, 'm/s'),                                 # 23
        N(20 * 3, 'kg m/s'),                                       # 24
        N(19 * F(9, 2), 'kg m/s'),                                 # 25
        N(F(80, 20), 'm/s'),                                       # 26
        T('A stops, B moves at 4 m/s', 'equal masses, perfectly elastic: the velocities exchange'),   # 27
        N(3, 'm/s'),                                               # 28 equal masses, elastic: B takes A's speed
        N(0, 'm/s'),                                               # 29
        N(F(20 * 5, 40), 'm/s'),                                   # 30
        N(F(2 * 20, 30) * 4, 'm/s'),                               # 31 v_B = 2 m_A u / (m_A + m_B)
        N(F(20 * 4, 30), 'm/s'),                                   # 32
        N(5 - 2, 'm/s'),                                           # 33
        N(100, 'kg m/s'),                                          # 34
        N(20 * 3, 'Ns'),                                           # 35
        N(F(60) / F(1, 10), 'N'),                                  # 36
        T('Momentum AND kinetic energy', 'definition of a perfectly elastic collision'),          # 37
        T('Momentum only', 'kinetic energy is not conserved when bodies stick'),                  # 38
        T('Perfectly inelastic collision', 'bodies that stick together'),                         # 39
        T('Yes — elastic collision', 'KE 160 J before and after'),                                # 40
        T('160 J before, 80 J after — energy lost', '1/2 x 20 x 16 = 160; 1/2 x 40 x 4 = 80'),     # 41
        T('Heat and sound', 'the KE lost in an inelastic collision'),                             # 42
        N(F(1, 2) * 20 * 16, 'J'),                                 # 43
        N(0, 'm/s'),                                               # 44
        N(F(20 * 3 + 20 * 1, 40), 'm/s'),                          # 45
        N(F(5) ** 2 / (2 * F(5, 100) * g10), 'm'),                 # 46
        N(sp.sqrt(25 - 2 * sp.Rational(4, 10) * 20), 'm/s'),       # 47
        N(3, 'm/s'),                                               # 48
        N(F(3) ** 2 / (2 * F(4, 100) * g10), 'm'),                 # 49
        N(sp.sqrt(2 * sp.Rational(4, 10) * 30), 'm/s'),            # 50
        T('22.5 m with, 11.25 m without', '9 / (2 x 0.2) = 22.5; 9 / (2 x 0.4) = 11.25'),         # 51
        N(F(200) / (F(4, 100) * 20 * g10), 'm'),                   # 52 KE = mu m g d
        T('Loss in kinetic energy', 'the work-energy principle'),                                 # 53
        N(F(4) ** 2 / (2 * F(3, 10)), 'm'),                        # 54
        T('Equal in magnitude, opposite in direction', "Newton's third law"),                     # 55
    ],
    'level4': [
        N(F(4, 100) * 20 * g981, 'N', ('sf', 3)),                  # 0
        N(F(35, 1000) * g981, 'm/s^2', ('sf', 3)),                 # 1
        N(F(36) / (2 * F(4, 100) * g981), 'm', ('sf', 3)),         # 2
        N(F(1, 10) * 50 * g981, 'N'),                              # 3
        N(F(4) / (2 * F(4905, 100) / 50), 'm', ('sf', 3)),         # 4
        N(F(20 * 5, 40), 'm/s', ('sf', 3)),                        # 5
        N(F(1500 * 20 + 1000 * 10, 2500), 'm/s'),                  # 6
        N(F(2 - 6, 8) * 8, 'm/s'),                                 # 7 velocity, original direction positive (t5-002)
        N(F(1, 2) * (-8 - 10), 'Ns'),                              # 8
        N(F(120, 20), 'm/s'),                                      # 9
        N(100 * (1 - F(1, 2) * 40 * 4 / (F(1, 2) * 20 * 16)), '%'),  # 10
        N(F(4 - 1, 5), ''),                                        # 11
        T('Perfectly elastic', 'e = 1'),                                                          # 12
        T('Perfectly inelastic', 'e = 0'),                                                        # 13
        N(F(125, 10) / (25 * 10), ''),                             # 14
        N(20 * F(4, 8), 'N'),                                      # 15
        N(F(4, 100) * 20 * 10 * 30, 'J'),                          # 16
        N(F(1, 2) * 20 * 25, 'J'),                                 # 17
        N((60 - F(15, 100) * 30 * 10) / 30, 'm/s^2'),              # 18
        T('0.0563 \\leq \\mu \\leq 0.0643', 'mu = u^2 / (2 g s) = 1.8 / s for s from 28 to 32: 0.05625 to 0.06429'),  # 19
    ],
}
AUDIT = {('alevel', 0): 't5-006', ('alevel', 21): 't5-001', ('level4', 7): 't5-002'}
UNIT_NAMES = {'N', 'm', 's', 'J', 'Ns', 'm/s', 'm/s^2', 'kg m/s', '%', ''}


def opt_value(o):
    """An option as (exact SymPy value or None, decimal shown after approx or None, unit)."""
    s = o.replace('\\text{', '').replace('}', ' ').replace('{', '').replace('\\%', '%').replace('−', '-')
    s = re.sub(r'\(it bounces back\)|\(bounces back\)', '', s)
    approx = None
    if '\\approx' in s:
        s, a = s.split('\\approx')
        am = re.search(r'(-?\d+(?:\.\d+)?)\s*(.*)$', a)
        approx, aunit = am.group(1), am.group(2)
        s = s.strip() + ' ' + aunit
    m = re.match(r'\s*\\sqrt(-?[\d.]+)(.*)$', s.replace('\\sqrt ', '\\sqrt'))
    if m:
        return sp.sqrt(sp.nsimplify(m.group(1))), approx, norm_unit(m.group(2))
    m = re.match(r'\s*\\dfrac\s*(-?[\d.]+)\s+(-?[\d.]+)(.*)$', s)
    if m:
        return sp.nsimplify(m.group(1)) / sp.nsimplify(m.group(2)), approx, norm_unit(m.group(3))
    m = re.match(r'\s*(-?\d+(?:\.\d+)?)\s*(.*)$', s)
    if not m:
        return None, approx, ''
    return sp.nsimplify(m.group(1)), approx, norm_unit(m.group(2))


def norm_unit(u):
    return re.sub(r'\s+', ' ', re.sub(r'\s*\^\s*', '^', u)).strip()


def rounded(v, prec):
    d = Decimal(str(sp.N(v, 40)))
    if prec[0] == 'dp':
        return d.quantize(Decimal(1).scaleb(-prec[1]), rounding=ROUND_HALF_UP)
    if d == 0:
        return d
    e = d.adjusted() - prec[1] + 1
    return d.quantize(Decimal(1).scaleb(e), rounding=ROUND_HALF_UP)


def dp_of(text):
    m = re.search(r'-?\d+\.(\d+)', text)
    return len(m.group(1)) if m else 0


def check_bank(fails, bank):
    for lv in TARGETS:
        items = bank.get(lv, [])
        if len(items) != len(TARGETS[lv]):
            fails.append('%s: %d items, TARGETS has %d (review the new items and extend TARGETS)'
                         % (lv, len(items), len(TARGETS[lv])))
            continue
        for i, (q, tg) in enumerate(zip(items, TARGETS[lv])):
            w = '%s[%d] (%s | %s)%s' % (lv, i, q['ctx'][:60], q['ask'],
                                       ' (curling-friction-%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            opts = [q['correct']] + q['d']
            if len(set(opts)) != 4:
                fails.append('%s: %d options, not 4 distinct' % (w, len(set(opts))))
            if re.search(r'friction force', q['ask'], re.I) and 'μ' in q['ctx'] and not re.search(r'slid|moving|sweep', q['ctx'], re.I):
                fails.append('%s: asks a friction force from mu R but never says the stone slides (at rest with no'
                             ' applied force there is no friction)' % w)
            if tg[0] == 'text':
                if q['correct'] != tg[1]:
                    fails.append('%s: keyed %s, reviewed %s (%s)' % (w, q['correct'], tg[1], tg[2]))
                continue
            _, target, unit, prec = tg
            vals = [opt_value(o) for o in opts]
            exact, approx, kunit = vals[0]
            if exact is None:
                fails.append('%s: the key %s cannot be read' % (w, q['correct']))
                continue
            stated = prec or ((('dp', dp_of(approx)) if approx else None))
            if prec is None and approx is None and not sp.nsimplify(exact).equals(target):
                # a rounded key with no stated precision
                r = ('dp', dp_of(q['correct']))
                if Decimal(str(sp.N(exact, 40))) == rounded(target, r):
                    fails.append('%s: the key %s is rounded but the item states no precision (SR-1)' % (w, q['correct']))
                else:
                    fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], sp.N(target, 8)))
                continue
            if prec:
                if 's.f.' not in q['ask'] + q['ctx'] and 'significant' not in q['ask'] + q['ctx'] and prec[0] == 'sf':
                    fails.append('%s: the key is rounded to %d s.f. but the item does not say so (SR-1)' % (w, prec[1]))
                if Decimal(str(sp.N(exact, 40))) != rounded(target, prec) or \
                        (prec[0] == 'sf' and len(re.sub(r'[^0-9]', '', q['correct'].split('\\')[0]).lstrip('0')) != prec[1]
                         and not q['correct'].startswith('2.50')):
                    if Decimal(str(sp.N(exact, 40))) != rounded(target, prec):
                        fails.append('%s: keyed %s, the answer is %s (%s)' % (w, q['correct'], rounded(target, prec), prec))
            else:
                if not sp.simplify(exact - target) == 0:
                    fails.append('%s: keyed %s, the answer is %s' % (w, q['correct'], sp.N(target, 8)))
                if approx is not None and Decimal(approx) != rounded(target, ('dp', dp_of(approx))):
                    fails.append('%s: the key shows %s, the answer rounds to %s' % (w, approx, rounded(target, ('dp', dp_of(approx)))))
            if re.search(r'\bspeed\b', q['ask'], re.I) and exact < 0:
                fails.append('%s: asks for a speed and keys %s; a speed is never negative (ask for the velocity, with'
                             ' a stated positive direction)' % (w, q['correct']))
            if kunit != unit and not (unit == 'm/s' and kunit.startswith('m/s')):
                fails.append('%s: the key\'s unit %r, expected %r' % (w, kunit, unit))
            for o, (ev, av, ou) in zip(opts[1:], vals[1:]):
                if ev is None:
                    continue
                if sp.simplify(ev - target) == 0 or (stated and Decimal(str(sp.N(ev, 40))) == rounded(target, stated)):
                    fails.append('%s: the wrong option %s equals the answer (SR-16)' % (w, o))
            for a in range(len(vals)):
                for b in range(a + 1, len(vals)):
                    if vals[a][0] is not None and vals[b][0] is not None and sp.simplify(vals[a][0] - vals[b][0]) == 0 \
                            and vals[a][2] == vals[b][2]:
                        fails.append('%s: options %s and %s are equal in value' % (w, opts[a], opts[b]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.requestAnimationFrame = () => 0;
  const out = [];
  for (const lv of ['alevel', 'level4']) QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.d]) {
      level = lv; questions = [q]; qIdx = 0; totalQ = 1; score = 0; streak = 0; correctCount = 0;
      document.getElementById('progress').innerHTML = '<div class="pip current"></div>';
      showQ();
      const b = [...document.querySelectorAll('#options .opt-btn')].find(x => x.dataset.val === pick);
      if (!b) { out.push([lv, i, pick, 'not on screen']); continue; }
      b.click();
      const right = b.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
      if (pick !== q.correct) {
        const sol = document.getElementById('solution');
        if (!sol.classList.contains('show')) out.push([lv, i, pick, 'no worked solution shown']);
        if (sol.querySelector('.next-btn')) out.push([lv, i, pick, 'a hand-rolled Next button (canon 7.6: MaffsNext)']);
        if (!sol.querySelector('button')) out.push([lv, i, pick, 'no Next control']);
        if (window.MaffsNext) MaffsNext.clear(sol); sol.className = 'solution';
      }
    }
  });
  return out;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            page.evaluate("() => { document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));"
                          " document.getElementById('game').classList.add('active'); }")
            for lv, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d] in Chromium: option %s %s' % (lv, i, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('alevel[21]', 't5-001: sqrt(4.96) keyed for the initial speed',
     "correct:'\\\\sqrt{13.6} \\\\approx 3.69 \\\\text{ m/s}',d:['\\\\sqrt{4.96} \\\\approx 2.23 \\\\text{ m/s}'",
     "correct:'\\\\sqrt{4.96} \\\\approx 2.23 \\\\text{ m/s}',d:['\\\\sqrt{13.6} \\\\approx 3.69 \\\\text{ m/s}'"),
    ('level4[7]', 't5-002: the hammer\'s "speed" keyed -4', "ask:'Velocity of the hammer after the collision (take its original direction as positive)'",
     "ask:'Speed of hammer after (equal mass formula not valid here)'"),
    ('alevel[0]', 't5-006: the stone "sits on ice"', 'A 20 kg curling stone slides across the ice.',
     'A 20 kg curling stone sits on ice.'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank:
        check_bank(fails, bank)
    print('%s: %d items, every numerical key recomputed exactly, every option clicked in Chromium'
          % (SLUG, sum(len(v) for v in bank.values()) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-48s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-48s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
