#!/usr/bin/env python3
# ci-line: Scale Factor Scaling (every key recomputed from the quantities its question states; every option marked in Chromium) |
"""Scale Factor Scaling: every key recomputed from what its question states, and nothing it does not state.

The game (46 multiple-choice items in four tiers: area, volume, reverse and context; gcse serves T1-T3, alevel
all four, level4 T2-T4) was keyed by hand with no verifier. The tranche 1 audit of 6 Oct 2026 found the paint
item (T4[4]) asking "how many litres for the larger shape?" with no original area or amount of paint, keyed
"4 litres per 10 m²" against its own rate of 10 m² per litre (scale-factor-scaling-t1-001, HIGH; contract
LISTED-HIGH, 9 Oct 2026: state the original quantity, chosen so the key holds).

TARGETS gives each item's answer as a computation on the quantities in its own prompt, with the words those
quantities come from (an edited prompt fails until its target is reviewed): no item may depend on a quantity it
does not state. Every option is read exactly (whole numbers, decimals, thousands commas, vulgar fractions,
ratios reduced by their gcd, and a unit). Then: the key equals the target in value and unit; no wrong option
does; the four options are distinct strings. In Chromium (390x844) every item is shown
through nextQ() and every option clicked through handleAnswer(): the key marked right, the others wrong.
A self-test plants the audit's paint item back into a copy of the page; it must FAIL naming T4[4].

    python scripts/verify-scale-factor-scaling.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'scale-factor-scaling'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'T1': 15, 'T2': 13, 'T3': 10, 'T4': 8}
VULGAR = {'½': F(1, 2), '⅓': F(1, 3), '¼': F(1, 4), '⅛': F(1, 8)}


def read(s):
    """('ratio', reduced tuple) | ('num', Fraction, unit)."""
    t = s.strip()
    if ':' in t:
        parts = [int(p) for p in t.split(':')]
        g = 0
        for p in parts:
            g = gcd(g, p)
        return ('ratio', tuple(p // g for p in parts))
    m = re.fullmatch(r'([½⅓¼⅛]|\d+/\d+|[\d,]*\.?\d+)\s*(.*)', t)
    if not m or not m.group(1):
        raise ValueError('cannot read %r' % s)
    n, unit = m.group(1), m.group(2).strip()
    if n in VULGAR:
        v = VULGAR[n]
    elif '/' in n:
        a, b = n.split('/')
        v = F(int(a), int(b))
    else:
        v = F(n.replace(',', ''))
    return ('num', v, unit)


def N(v, unit=''):
    return ('num', F(v), unit)


def R(*p):
    return ('ratio', tuple(p))


# (words the prompt must carry, the answer from them). Each tier in the page's order.
TARGETS = {
    'T1': [
        ('Length scale factor = 2. Area', N(2 ** 2)),
        ('Length scale factor = 3. Area', N(3 ** 2)),
        ('Length scale factor = 4. Area', N(4 ** 2)),
        ('Length scale factor = 5. Area', N(5 ** 2)),
        ('Length scale factor = 10. Area', N(10 ** 2)),
        ('Lengths double. Original area = 12 cm²', N(12 * 2 ** 2, 'cm²')),
        ('Lengths triple. Original area = 5 m²', N(5 * 3 ** 2, 'm²')),
        ('Scale factor = 4. Original area = 10 cm²', N(10 * 4 ** 2, 'cm²')),
        ('Lengths in ratio 2:5. Area ratio', R(4, 25)),
        ('Sides 3 cm and 9 cm. Area ratio', R(1, 9)),
        ('Length scale factor = ½. Area', N(F(1, 2) ** 2)),
        ('Length scale factor = ⅓. Area', N(F(1, 3) ** 2)),
        ('Lengths halved. Original area = 100 cm²', N(100 * F(1, 2) ** 2, 'cm²')),
        ('Scale factor = 1.5. Area', N(F(3, 2) ** 2)),
        ('Scale factor = 0.5. Original area = 64 m²', N(64 * F(1, 2) ** 2, 'm²')),
    ],
    'T2': [
        ('Length scale factor = 2. Volume', N(2 ** 3)),
        ('Length scale factor = 3. Volume', N(3 ** 3)),
        ('Length scale factor = 4. Volume', N(4 ** 3)),
        ('Length scale factor = 5. Volume', N(5 ** 3)),
        ('Length scale factor = 10. Volume', N(10 ** 3)),
        ('Lengths double. Original volume = 20 cm³', N(20 * 2 ** 3, 'cm³')),
        ('Lengths triple. Original volume = 10 m³', N(10 * 3 ** 3, 'm³')),
        ('Lengths in ratio 1:4. Volume ratio', R(1, 64)),
        ('Length scale factor = ½. Volume', N(F(1, 2) ** 3)),
        ('Length scale factor = ⅓. Volume', N(F(1, 3) ** 3)),
        ('Lengths halved. Volume = 1000 cm³', N(1000 * F(1, 2) ** 3, 'cm³')),
        ('Scale factor = 1.5. Volume', N(F(3, 2) ** 3)),
        ('1:20 scale. Real car volume = 4 m³', N(4 * F(1, 20) ** 3, 'm³')),
    ],
    'T3': [
        ('Area scale factor = 9. Linear', N(3)),
        ('Area scale factor = 25. Linear', N(5)),
        ('Area scale factor = 4. Linear', N(2)),
        ('Volume scale factor = 8. Linear', N(2)),
        ('Volume scale factor = 27. Linear', N(3)),
        ('Volume scale factor = 125. Linear', N(5)),
        ('Area ratio = 16:49. Length ratio', R(4, 7)),
        ('Volume ratio = 8:27. Length ratio', R(2, 3)),
        ('Volume ratio = 8:27. Area ratio', R(4, 9)),
        ('Area ratio = 9:25. Volume ratio', R(27, 125)),
    ],
    'T4': [
        ('A cube has side 5 cm, enlarged by SF 3. New volume', N(5 ** 3 * 3 ** 3, 'cm³')),
        ('Radius triples. New surface area factor', N(3 ** 2)),
        ('Heights 10 cm and 30 cm. Volume ratio', R(1, 27)),
        ('scale 1:50000. A lake is 4 cm² on the map. Real area', N(F(4 * 50000 ** 2, 100 ** 2), 'm²')),
        # 1 litre covers 10 m²: a 10 m² surface needs 1 litre; doubled, its area is 4 x 10 m², so 4 litres.
        ('covers 10 m² per litre. A shape with surface area 10 m²', N(F(10 * 2 ** 2, 10), 'litres')),
        ('1:100 scale weighs 50g. Same material', N(F(50 * 100 ** 3, 1000), 'kg')),
        ('Diameters 6 cm and 18 cm. Volume of small = 24 cm³', N(24 * (18 // 6) ** 3, 'cm³')),
        ('enlarged by SF 2.5. Original area = 60 cm²', N(60 * F(5, 2) ** 2, 'cm²')),
    ],
}


def check_bank(fails, bank):
    for t, n in COUNTS.items():
        items = bank.get(t, [])
        if len(items) != n:
            fails.append('%s: %d items, expected %d (a change needs TARGETS reviewed)' % (t, len(items), n))
            continue
        for i, q in enumerate(items):
            w = '%s[%d] (%s)' % (t, i, q['p'])
            words, target = TARGETS[t][i]
            if words not in q['p']:
                fails.append('%s: the prompt must say "%s" for its key to follow from what it states' % (w, words))
            opts = [q['c']] + list(q['d'])
            if len(opts) != 4 or len(set(opts)) != 4:
                fails.append('%s: the options %s are not four distinct strings' % (w, opts))
            try:
                vals = [read(o) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend read())' % (w, e))
                continue
            if vals[0] != target:
                fails.append('%s: keyed %s, the answer is %s' % (w, q['c'], target[1:]))
            for o, v in zip(opts[1:], vals[1:]):
                if v[:2] == target[:2]:
                    fails.append('%s: the wrong option %s is also right' % (w, o))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [], tiers = {T1, T2, T3, T4};
  for (const [t, items] of Object.entries(tiers)) items.forEach((q, i) => {
    for (const pick of [q.c, ...q.d]) {
      pool = [q]; qIdx = 0; total = 0; score = 0; correctN = 0;
      nextQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([t, i, pick, shown.length + ' options on screen']);
      if (document.getElementById('prompt').textContent !== q.p) out.push([t, i, pick, 'prompt not shown as written']);
      const btn = shown.find(x => x.dataset.val === pick);
      if (!btn) { out.push([t, i, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === q.c)) out.push([t, i, pick, right ? 'marked right' : 'marked wrong']);
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
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?level=alevel&cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof T4 !== "undefined"', timeout=15000)
            page.evaluate("() => show('game')")
            bank = page.evaluate('() => ({T1, T2, T3, T4})')
            for t, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d] in Chromium: option %s %s' % (t, i, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('T4[4]', 't1-001: the paint item with no original quantity',
     "{sec:'Context',p:'Paint covers 10 m² per litre. A shape with surface area 10 m² is enlarged so its dimensions double. How many litres for the larger shape?',c:'4 litres',d:['2 litres','8 litres','1 litre'],s:['Surface area scales by k² = 2² = 4','New surface area = 10 × 4 = 40 m²','40 ÷ 10 = 4 litres'],mc:'Paint covers area, so it scales by k², not k.'}", "{sec:'Context',p:'Paint covers 10 m² per litre. If dimensions double, how many litres for the larger shape?',c:'4 litres per 10 m²',d:['2 litres','8 litres','1 litre'],s:['Surface area scales by k² = 4','4× more paint needed']}"),
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
    print('%s: %d items, every key recomputed from what its prompt states, every option clicked in Chromium'
          % (SLUG, sum(len(v) for v in (bank or {}).values())))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
