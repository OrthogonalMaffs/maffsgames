#!/usr/bin/env python3
# ci-line: Scale Factor Scaling (every key recomputed from the quantities its question states; every option marked in Chromium) |
"""Scale Factor Scaling: every key recomputed from what its question states, and nothing it does not state.

The game (now "But It's Only Half the Size!", slug unchanged; 54 multiple-choice items in five tiers: area,
volume, reverse, context and more; gcse serves T1-T3 and T5, alevel and level4 all five; contract HALF-THE-SIZE,
23 Nov 2026) was keyed by hand with no verifier. The tranche 1 audit of 6 Oct 2026 found the paint
item (T4[4]) asking "how many litres for the larger shape?" with no original area or amount of paint, keyed
"4 litres per 10 m²" against its own rate of 10 m² per litre (scale-factor-scaling-t1-001, HIGH; contract
LISTED-HIGH, 9 Oct 2026: state the original quantity, chosen so the key holds).

TARGETS gives each item's answer as a computation on the quantities in its own prompt, with the words those
quantities come from (an edited prompt fails until its target is reviewed): no item may depend on a quantity it
does not state. Every option is read exactly (whole numbers, decimals, thousands commas, vulgar fractions,
ratios reduced by their gcd, and a unit). Then: the key equals the target in value and unit; no wrong option
does; the four options are distinct strings and no two are equal in value (SR-4; B11-CLEAR, 12 Oct 2026: none
expected, so EQUAL_PAIRS is empty and any equal pair fails). In Chromium (390x844) every item is shown
through nextQ() and every option clicked through handleAnswer(): the key marked right, the others wrong.
KaTeX (HALF-THE-SIZE): every item's worked solution (showExplain), served KaTeX from scripts/fonts/katex/, shows no
raw \\( or \\), no .katex-error, and a .katex in every step or note authored with \\( \\); every fraction option a/b
shows a .katex. A self-test plants the audit's faults back into a copy of the page, and a step's broken TeX; each
must FAIL naming its item.

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
COUNTS = {'T1': 15, 'T2': 13, 'T3': 10, 'T4': 8, 'T5': 8}
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
# SWEEP-1 (13 Oct 2026; SR-17): each prompt's words state what its key assumes: a LENGTH scale factor
# (s1-001), corresponding sides (s1-002), similar solids (s1-003). The old wording fails the words check.
TARGETS = {
    'T1': [
        ('length scale factor 2. By what factor does the area', N(2 ** 2)),
        ('length scale factor 3. By what factor has its area', N(3 ** 2)),
        ('length scale factor 4. By what factor does the area', N(4 ** 2)),
        ('length scale factor 5. What is the area scale factor', N(5 ** 2)),
        ('length scale factor 10 to cover the whole classroom wall. What is the area scale factor', N(10 ** 2)),
        ('A 12 cm² stamp showing a famous goat is enlarged so every length doubles', N(12 * 2 ** 2, 'cm²')),
        ('A 5 m² trampoline is rebuilt for an elephant, with every length 3 times as long', N(5 * 3 ** 2, 'm²')),
        ('A 10 cm² biscuit is enlarged with length scale factor 4', N(10 * 4 ** 2, 'cm²')),
        ('are similar, with lengths in the ratio 2 : 5. What is the ratio of their areas', R(2 ** 2, 5 ** 2)),
        ('Two similar triangular sandwiches have corresponding sides of 3 cm and 9 cm', R(1, (9 // 3) ** 2)),
        ('comes out with every length halved. By what factor has the area', N(F(1, 2) ** 2)),
        ('one third as long in every direction. What is the area scale factor', N(F(1, 3) ** 2)),
        ('A 100 cm² beach towel goes on the wrong wash and every length halves', N(100 * F(1, 2) ** 2, 'cm²')),
        ('length scale factor 1.5. By what factor has their area', N(F(3, 2) ** 2)),
        ('A 64 m² bouncy castle slowly deflates until every length is 0.5 times', N(64 * F(1, 2) ** 2, 'm²')),
    ],
    'T2': [
        ('twice as long in every direction as the normal one. How many times as much jelly', N(2 ** 3)),
        ('3 times as long in every direction. By what factor does the volume', N(3 ** 3)),
        ('length scale factor 4 to scare off the neighbours. What is the volume scale factor', N(4 ** 3)),
        ('length scale factor 5 for a very large bath. What is the volume scale factor', N(5 ** 3)),
        ('length scale factor 10 for a horse with a sweet tooth. What is the volume scale factor', N(10 ** 3)),
        ('A 20 cm³ meatball is made with every length doubled', N(20 * 2 ** 3, 'cm³')),
        ('A 10 m³ hot tub is rebuilt 3 times as long in every direction', N(10 * 3 ** 3, 'm³')),
        ('are similar, with lengths in the ratio 1 : 4. What is the ratio of their volumes', R(1 ** 3, 4 ** 3)),
        ('comes out with every length halved. "But it\'s only half the size!" By what factor has its volume', N(F(1, 2) ** 3)),
        ('making every length one third as long. What is the volume scale factor', N(F(1, 3) ** 3)),
        ('A 1000 cm³ sandcastle bucket is copied for a toddler, with every length halved', N(1000 * F(1, 2) ** 3, 'cm³')),
        ('length scale factor 1.5. By what factor has its volume', N(F(3, 2) ** 3)),
        ("built to a scale of 1 : 20. The real car's volume is 4 m³", N(4 * F(1, 20) ** 3, 'm³')),
    ],
    'T3': [
        ('is the same shape as yours, with 9 times the area. What is the length scale factor', N(3)),  # 3 ** 2 = 9
        ('is the same shape as the original photo, with 25 times the area. What is the length scale factor', N(5)),  # 5 ** 2 = 25
        ('is similar to a sadder, smaller pancake, with 4 times the area. What is the length scale factor', N(2)),  # 2 ** 2 = 4
        ('is similar to a small one and holds 8 times as much. What is the length scale factor', N(2)),  # 2 ** 3 = 8
        ("is similar to the kids' size and holds 27 times as much. What is the length scale factor", N(3)),  # 3 ** 3 = 27
        ('keeping its shape, until it holds 125 times its original volume. What is the length scale factor', N(5)),  # 5 ** 3 = 125
        ('Two similar paddling pools have floor areas in the ratio 16 : 49. What is the ratio of their lengths', R(4, 7)),  # 4 ** 2 : 7 ** 2 = 16 : 49
        ('Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of their lengths', R(2, 3)),  # 2 ** 3 : 3 ** 3 = 8 : 27
        ('Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of the areas', R(2 ** 2, 3 ** 2)),  # lengths 2 : 3 from 8 : 27
        ('Two similar snowmen have surface areas in the ratio 9 : 25', R(3 ** 3, 5 ** 3)),  # lengths 3 : 5 from 9 : 25
    ],
    'T4': [
        ('A 5 cm cube of cheese is enlarged with scale factor 3', N(5 ** 3 * 3 ** 3, 'cm³')),
        ('enlarged so its radius triples. By what factor does its surface area', N(3 ** 2)),
        ('Two similar bottles of very fizzy pop are 10 cm and 30 cm tall', R(1, (30 // 10) ** 3)),
        ('with scale 1 : 50 000, a crocodile-filled lake covers 4 cm²', N(F(4 * 50000 ** 2, 100 ** 2), 'm²')),
        ('Paint covers 10 m² per litre. A shed with surface area 10 m²', N(F(10 * 2 ** 2, 10), 'litres')),  # 1 litre covers 10 m²; doubled, the area is 4 x 10 m²
        ('A 1 : 100 model of the school weighs 50 g. The real school is made of the same stuff', N(F(50 * 100 ** 3, 1000), 'kg')),
        ('Two similar ice-cream cones have diameters of 6 cm and 18 cm. The small one holds 24 cm³', N(24 * (18 // 6) ** 3, 'cm³')),
        ("enlarged with scale factor 2.5. The original's area is 60 cm²", N(60 * F(5, 2) ** 2, 'cm²')),
    ],
    'T5': [
        ("length scale factor 2 for a giant's breakfast. The normal slice has 15 cm² of butter", N(15 * 2 ** 2, 'cm²')),
        ('with every length 6 times as long. What is the area scale factor', N(6 ** 2)),
        ('A 2 cm³ chocolate button is enlarged so every length is 3 times as long', N(2 * 3 ** 3, 'cm³')),
        ('with every length 0.8 times what it was. By what factor has its area', N(F(4, 5) ** 2)),
        ("is similar to your teacher's and 4 times as tall. The teacher's holds 300 ml", N(F(300 * 4 ** 3, 1000), 'litres')),
        ('Two similar garden ponds have lengths in the ratio 3 : 7. What is the ratio of their surface areas', R(3 ** 2, 7 ** 2)),
        ('Two similar sandcastles have volumes in the ratio 1 : 64. What is the ratio of their heights', R(1, 4)),  # 1 ** 3 : 4 ** 3 = 1 : 64
        ('gets a similar bed with 4 times the floor area. How many times as long', N(2)),  # 2 ** 2 = 4
    ],
}


# Items allowed two options equal in value, as (tier, index): only a question whose ask names the form that
# separates them (SR-4's exception). None: B11-CLEAR (12 Oct 2026) replaced T1[8]'s 4:10 and T1[9]'s 3:9.
EQUAL_PAIRS = set()


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
            for a in range(4):
                for b in range(a + 1, 4):
                    if vals[a] == vals[b] and (t, i) not in EQUAL_PAIRS:
                        fails.append('%s: the options %s and %s are equal in value (SR-4)' % (w, opts[a], opts[b]))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [], tiers = {T1, T2, T3, T4, T5};
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


# HALF-THE-SIZE (23 Nov 2026): the worked solution and the fraction options render through KaTeX.
KATEX_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [], tiers = {T1, T2, T3, T4, T5};
  const bare = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(m => m.remove()); return c.textContent; };
  for (const [t, items] of Object.entries(tiers)) items.forEach((q, i) => {
    pool = [q]; qIdx = 0; total = 0; score = 0; correctN = 0;
    nextQ();
    for (const b of document.querySelectorAll('#options .opt-btn'))
      if (/^\d+\/\d+$/.test(b.dataset.val) && !b.querySelector('.katex')) out.push([t, i, 'the fraction option ' + b.dataset.val + ' is not KaTeX']);
    showExplain(q);
    const sol = document.getElementById('solution');
    const text = bare(sol);
    if (text.includes('\\(') || text.includes('\\)')) out.push([t, i, 'raw \\( \\) in the worked solution: ' + text.slice(0, 90)]);
    if (sol.querySelector('.katex-error')) out.push([t, i, 'a .katex-error in the worked solution: ' + sol.querySelector('.katex-error').textContent.slice(0, 90)]);
    const parts = [...sol.querySelectorAll('.step, .misconception')], src = [...(q.s || []), ...(q.mc ? [q.mc] : [])];
    parts.forEach((el, k) => { if ((src[k] || '').includes('\\(') && !el.querySelector('.katex')) out.push([t, i, 'no KaTeX in ' + JSON.stringify(src[k])]); });
  });
  return out;
}"""


def text_fails(html):
    """SWEEP-1 rulings (13 Oct 2026): R7, the timer policy lists this game under Hidden Count-Up, so the HUD shows no running Time."""
    out = []
    if re.search(r'class="hud-label">Time<', html) or 'id="timer"' in html:
        out.append('hud: the running Time is on the HUD; Hidden Count-Up means it is never shown (R7, scale-factor-scaling-s1-005)')
    return out


def notation_fails(html):
    """scale-factor-scaling-s1-004 (R1): fractions are written one way, as a/b; the glyphs (1/2 and a half glyph) are not mixed in one option set."""
    return ['notation: a fraction glyph (%s) is in the page; write it as a/b' % ''.join(sorted(set(re.findall('[\u00bd\u2153\u00bc\u215b\u2154\u00be]', html))))] if re.search('[\u00bd\u2153\u00bc\u215b\u2154\u00be]', html) else []


def play(fails, html):
    fails.extend(text_fails(html) + notation_fails(html))
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            bc.offline(ctx, base)   # KaTeX's CDN files answered from scripts/fonts/katex/; everything else off the stub server aborted
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?level=alevel&cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof T5 !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            page.evaluate("() => show('game')")
            bank = page.evaluate('() => ({T1, T2, T3, T4, T5})')
            for t, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d] in Chromium: option %s %s' % (t, i, pick, what))
            for t, i, what in page.evaluate(KATEX_JS):
                fails.append('%s[%d] KaTeX: %s' % (t, i, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


# (the item the failure must name, what is planted, today's text, main's text before LISTED-HIGH).
PLANTS = [
    ('hud:', 's1-005: the HUD Time back', '<div class="hud-item"><div class="hud-label">Correct</div>',
     '<div class="hud-item"><div class="hud-label">Time</div><div class="hud-val" id="timer">0</div></div><div class="hud-item"><div class="hud-label">Correct</div>'),
    ('notation:', 's1-004: a fraction glyph back', "c:'1/4',d:['1/2','1/8','1/16']", "c:'\u00bc',d:['1/2','1/8','1/16']"),
    ('T4[4]', 't1-001: the paint item with no original quantity',
     "{sec:'Context',p:'Paint covers 10 m² per litre. A shed with surface area 10 m² is rebuilt with every length doubled, for a very large lawnmower. How many litres does the new shed need?',c:'4 litres',d:['2 litres','8 litres','1 litre'],s:['Surface area scales by \\\\(k^2 = 2^2 = 4\\\\)','New surface area \\\\(= 10 \\\\times 4 = 40\\\\) m²','\\\\(40 \\\\div 10 = 4\\\\) litres'],mc:'Paint covers area, so it scales by \\\\(k^2\\\\), not \\\\(k\\\\).'}", "{sec:'Context',p:'Paint covers 10 m² per litre. If dimensions double, how many litres for the larger shape?',c:'4 litres per 10 m²',d:['2 litres','8 litres','1 litre'],s:['Surface area scales by k² = 4','4× more paint needed']}"),
    ('T1[8]', 'SR-4: two wrong options equal in value (4:10 = 2:5)',
     "c:'4:25',d:['2:5','8:125','4:5']", "c:'4:25',d:['2:5','8:125','4:10']"),
    ('T1[7]', 's1-001: "Scale factor" with no "length" (40 cm² is then right)',
     "biscuit is enlarged with length scale factor 4", "biscuit is enlarged with scale factor 4"),
    ('T3[8]', 's1-003: a ratio item that does not say similar',
     "Two similar pies hold gravy in the ratio 8 : 27. What is the ratio of the areas", "Two pies hold gravy in the ratio 8 : 27. What is the ratio of the areas"),
    ('T1[1]', 'HALF-THE-SIZE: a step\'s TeX broken (KaTeX error)',
     "s:['\\\\(k^2 = 3^2 = 9\\\\)']", "s:['\\\\(k^2 = 3^2 = \\\\dfrac{9}\\\\)']"),
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
