#!/usr/bin/env python3
# ci-line: E | Moments Master (every key recomputed with SymPy, options distinct in value, every option clicked in Chromium) |
"""Moments Master: every key recomputed with SymPy, options distinct in value, every option clicked in Chromium.

The tranche 5 audit (6 Oct 2026) found five keys that their own data contradicts (alevel :128, :134, :147 had no
answer as set; :141 keyed 50 N for 75 N; level4 :172/:173 keyed 6.5/3.5 kN for 5.375/4.625 kN), a distractor equal
to the key (5 kW beside 5000 W), and prose passed whole through KaTeX. Project Claude supplied replacement data for
:128, :134, :147 and :172/:173 (7 Oct 2026).

Keys. KEYS below holds, for every item with a numeric answer, the answer computed from the item's own data (SymPy,
  exact; angles in degrees), with its unit. The shown key must match it at the precision it is shown to (half a unit
  in its last place), in that unit. Every other item's key is a reviewed judgement, pinned by the item's content hash
  (REVIEWED): an edit fails until it is re-reviewed (--print-pins).
Options (SR-4, SR-16). No two options are equal in value, and no distractor equals the key: values are compared in
  SI (5 kW = 5000 W) and with their words (1 Nm clockwise is not 1 Nm anticlockwise). Where an item's distractors
  are named errors (REASONS), each is recomputed from its reason.
Claims. Every numeric equality or approximation written in a key or a working line (x = y, x \\approx y) holds.
  Every "Same ..." item quotes its predecessor's key.
Rendering. A string drawn by KaTeX keeps no prose outside \\text{} (B7: KaTeX drops the spaces).
Chromium (390x844 and 320x568). Every option of every item is clicked through the game's own handler: the key is
  marked right; any other option is marked wrong, shows the answer and waits for the shared Next control (MaffsNext,
  canon 7.6). No raw TeX on screen; the page never scrolls sideways.

A self-test plants two of the audit's own faults back (t5-008: R_B keyed 50 N; t5-004: '5 kW' beside 5000 W); each
must FAIL naming its item.

    python scripts/verify-moments-master.py [--no-selftest] [--against FILE] [--katex-dir DIR] [--print-pins]
"""
import argparse
import hashlib
import json
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'moments-master'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
R = sp.Rational
D = sp.pi / 180


def deg(a):
    return a * D


# Every numeric key from the item's own data: (value, unit). The comment is the physics read from the item.
KEYS = {
    ('alevel', 0): (10 * 3, 'Nm'),
    ('alevel', 1): (25 * 2, 'Nm'),
    ('alevel', 2): (8 * R(9, 2), 'Nm'),
    ('alevel', 3): (R(60, 4), 'N'),
    ('alevel', 4): (R(100, 20), 'm'),
    ('alevel', 5): (50 * R(2, 5) * sp.sin(deg(30)), 'Nm'),
    ('alevel', 6): (40 * R(1, 2) * sp.sin(deg(60)), 'Nm'),
    ('alevel', 7): (0, 'Nm'),
    ('alevel', 10): (8 * 2 - 5 * 3, 'Nm anticlockwise'),        # 16 anticlockwise against 15 clockwise
    ('alevel', 12): (R(120, 2), 'N each'),
    ('alevel', 13): (R(80 * 2 + 50 * 1, 4), 'N'),
    ('alevel', 14): (130 - R(80 * 2 + 50 * 1, 4), 'N'),
    ('alevel', 15): (R(200 * 4 + 100 * 6, 8), 'N'),
    ('alevel', 16): (R(60 * 3, 2) / 1, 'N'),                     # G 1.5 m right of the support, W 1 m left of it
    ('alevel', 17): (R(30 * 2) / R(3, 2), 'kg'),
    ('alevel', 18): (R(150 * 2, 4), 'N'),                        # G 2 m from the left support, right support 4 m
    ('alevel', 20): (R(60 * 3, 100), 'm from the left end'),      # 40x = 60(3 - x)
    ('alevel', 21): ((2 * R(2, 5) - 1 * R(1, 10)) / 3, 'm right of pivot'),
    ('alevel', 22): (R(500 * 2, 3), 'N'),                         # G 2 m beyond C, P at A 3 m before C
    ('alevel', 23): (80 * R(3, 2) / 4, 'N'),
    ('alevel', 24): (80 - 80 * R(3, 2) / 4, 'N'),
    ('alevel', 25): (R(40 * 6, 120), 'm'),
    ('alevel', 26): (2, 'm from A'),
    ('alevel', 27): (8 - R(1, 4) * 8, 'm'),                       # R_B = W/4; W x = (W/4)(8) from A
    ('alevel', 28): (R(100 * 1 + 50 * 4, 4), 'N'),
    ('alevel', 29): (R(200 * 3, 8), 'N'),
    ('alevel', 30): (R(60 * 2, 3), 'N'),
    ('alevel', 31): (R(20 * 3, 60), 'm'),
    ('alevel', 32): (R(9, 5), 'm from A'),
    ('alevel', 33): (4 + R(90 * 1, 60), 'm'),                     # tipping about D: 90 x 1 = 60 (x - 4)
    ('alevel', 34): (R(100 * 2 + 200 * 3, 4), 'N'),
    ('alevel', 35): (200 * R(5, 2) * sp.cos(deg(60)) / (5 * sp.sin(deg(60))), 'N'),
    ('alevel', 36): (30 * 2 + 10 * 1, 'Nm'),
    ('alevel', 37): (15 * R(4, 5), 'Nm'),
    ('alevel', 39): (80 * R(3, 5) / R(6, 5), 'N'),
    ('level4', 0): (80 * R(3, 10), 'Nm'),
    ('level4', 1): (50 / R(1, 4), 'N'),
    ('level4', 2): (R(5, 2), 'kN'),
    ('level4', 3): (R(10 * 2, 6), 'kN'),
    ('level4', 4): (10 - R(10 * 2, 6), 'kN'),
    ('level4', 5): (2 * 3, 'kNm'),
    ('level4', 6): (R(2 * 1 + 5 * 4 + 3 * 7, 8), 'kN'),
    ('level4', 7): (10 - R(2 * 1 + 5 * 4 + 3 * 7, 8), 'kN'),
    ('level4', 8): (200 * R(15, 100), 'Nm'),
    ('level4', 9): (100 * R(2, 5) * sp.sin(deg(50)), 'Nm'),
    ('level4', 10): (20 * 12 + 8 * 6, 'kNm'),
    ('level4', 11): (2 * 6, 'kN'),
    ('level4', 12): (R(12, 2), 'kN'),
    ('level4', 13): (20 - R(20 * R(5, 2), 4), 'kN'),
    ('level4', 14): (50 * 100, 'W'),
    ('level4', 15): (2000 / (2 * sp.pi * 1500 / 60), 'Nm'),
    ('level4', 16): (500 * R(15, 100), 'Nm'),
    ('level4', 17): (600 * R(1, 5), 'Nm'),
    ('level4', 18): (R(4 * 1 + 6 * R(5, 2), 3), 'kN'),
    ('level4', 19): (R(80, 100), 'm'),
}

# Named-error distractors for the items this fix rewrote (Project Claude's data, and t5-004's replacement)
REASONS = {
    ('alevel', 16): [(R(60 * 3, 2) / 4, 'the load at the right end'), (60, 'distances ignored'),
                     (60 * R(5, 2), '60 x 2.5, the distance from the end')],
    ('alevel', 22): [(R(500 * 2, 7), 'the load at B'), (R(500 * 3, 2), 'arms swapped'), (500, 'distances ignored')],
    ('alevel', 28): [(R(50 * 4, 4), "the rod's weight left out"), (R(100 * 2 + 50 * 4, 4), 'the rod taken as uniform'),
                     (R(100 * 1, 4), 'the load at B left out')],
    ('alevel', 33): [(R(90, 60), 'the distance beyond D'), (4 + R(60, 90), 'weights swapped'), (6, 'reaches B')],
    ('level4', 6): [(R(52, 8), 'the old slip'), (5, 'half the load'), (10 - R(43, 8), 'R_A')],
    ('level4', 7): [(R(43, 8), 'R_B'), (5, 'half the load'), (10, 'the total load')],
    ('level4', 14): [(R(50, 100), 'T / omega'), (150, 'T + omega'), (2 * sp.pi * 100 * 50 / 60, 'P = 2 pi N T / 60, 100 taken as rpm')],
}

# Items that quote an earlier item's key
CHAIN = {('alevel', 14): ('alevel', 13), ('alevel', 24): ('alevel', 23), ('alevel', 31): ('alevel', 30),
         ('level4', 4): ('level4', 3), ('level4', 7): ('level4', 6), ('level4', 12): ('level4', 11)}

# Text keys, reviewed (7 Oct 2026); the pin is the item's content hash. alevel[40] is the gate (t5-012, Jon's call).
REVIEWED = {
    ('alevel', 8): '8135a2e1', ('alevel', 9): '96350667', ('alevel', 11): 'a52353dc', ('alevel', 19): '61d9081d',
    ('alevel', 38): '43817fd7', ('alevel', 40): '534029c5', ('alevel', 41): '7d1e4443', ('alevel', 42): '9dc7885c',
    ('alevel', 43): '8fe28f06', ('alevel', 44): '2fd5eebf', ('alevel', 45): '03101a1b', ('alevel', 46): '563f4e34',
    ('alevel', 47): '9b5659b5', ('alevel', 48): '6b368ea2',
}

TAGS = {('alevel', 16): 't5-005', ('alevel', 22): 't5-006', ('alevel', 28): 't5-008', ('alevel', 33): 't5-007',
        ('level4', 6): 't5-002', ('level4', 7): 't5-003', ('level4', 14): 't5-004', ('alevel', 19): 't5-013',
        ('alevel', 40): 't5-013'}


def where(lvl, i):
    t = TAGS.get((lvl, i))
    return '%s[%d]%s' % (lvl, i, ' (moments-master-%s)' % t if t else '')


def pin(item):
    return hashlib.sha1(json.dumps(item, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:8]


# ------------------------------------------------------------------ reading values
def latex_value(t):
    """A numeric TeX expression -> SymPy, or None."""
    s = t.replace('\\left', '').replace('\\right', '').replace('\\,', ' ').replace('\\;', ' ')
    s = re.sub(r'\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
    s = re.sub(r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)', s)
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace('\\pi', ' pi ').replace('°', '*pi/180')
    s = re.sub(r'\\(sin|cos|tan)\s*', r'\1 ', s)
    s = re.sub(r'(?<=[\d)])\s*(?=[(a-z])', '*', s.strip())
    s = re.sub(r'(sin|cos|tan)\s+([\d.*/pi ]+)', r'\1(\2)', s)
    if re.search(r'[A-Za-z_\\]', re.sub(r'\b(sqrt|pi|sin|cos|tan)\b', '', s)):
        return None
    try:
        return sp.nsimplify(sp.sympify(s), rational=True) if 'pi' not in s and 'sqrt' not in s and 'sin' not in s \
            and 'cos' not in s else sp.sympify(s)
    except (sp.SympifyError, TypeError, SyntaxError):
        return None


PREFIX = {'kN': ('N', 1000), 'kNm': ('Nm', 1000), 'kW': ('W', 1000)}


def quantity(opt):
    """'5.375 \\text{ kN}' -> (5.375, 'kN', decimals, words) for a single quantity, else None."""
    s = opt
    for sep in ('\\approx', '='):
        if sep in s:
            s = s.rsplit(sep, 1)[1]
    m = re.fullmatch(r'\s*(-?\d+(?:\.\d+)?)\s*(?:\\text\{\s*([^{}]*)\})?\s*', s)
    if not m:
        return None
    num, unit = m.group(1), (m.group(2) or '').strip()
    if re.search(r'\d', unit):
        return None
    dec = len(num.split('.')[1]) if '.' in num else 0
    return R(num), unit, dec


def si(q):
    v, unit, _ = q
    first, _, rest = unit.partition(' ')
    base, f = PREFIX.get(first, (first, 1))
    return v * f, (base + ' ' + rest).strip()


def close(shown, exact, dec):
    return abs(sp.N(exact - shown, 30)) <= R(1, 2) * R(10) ** -dec + R(1, 10 ** 12)


# ------------------------------------------------------------------ the static checks
def check_bank(fails, bank, print_pins=False):
    for lvl in ('alevel', 'level4'):
        for i, it in enumerate(bank[lvl]):
            w = where(lvl, i)
            opts = [it['correct']] + list(it['d'])
            if (lvl, i) in KEYS:
                val, unit = KEYS[(lvl, i)]
                q = quantity(it['correct'])
                if q is None:
                    fails.append('%s: the key %r is not a single quantity' % (w, it['correct']))
                elif q[1] != unit or not close(q[0], val, q[2]):
                    fails.append('%s: keyed %s %s; its data gives %s %s' % (w, q[0], q[1], sp.N(val, 6), unit))
            elif (lvl, i) in REVIEWED:
                if print_pins or REVIEWED[(lvl, i)] != pin(it):
                    fails.append('%s: a reviewed text key, changed since review (pin %s, now %s): re-review it' % (
                        w, REVIEWED[(lvl, i)], pin(it)))
            else:
                fails.append('%s: no computed key and not reviewed: %r' % (w, it['correct']))
            # options distinct in value; no distractor equal to the key (SR-4, SR-16)
            qs = [quantity(o) for o in opts]
            sis = [si(x) if x else None for x in qs]
            if len(set(opts)) != len(opts):
                fails.append('%s: two options are the same' % w)
            for j in range(len(opts)):
                for k in range(j + 1, len(opts)):
                    a, b = sis[j], sis[k]
                    if a and b and a == b:          # the same value in SI, with the same words
                        fails.append('%s: %r and %r are equal in value (SR-4, SR-16)' % (w, opts[j], opts[k]))
            if (lvl, i) in KEYS and qs[0]:
                # a distractor equals the key if it is the key's exact value (in SI), or the key rounded to the
                # distractor's own precision when that is at least as fine as the key's ('6 m' beside 5.5 m is not)
                val, unit = KEYS[(lvl, i)]
                kv, ku = si((val, unit, 0))
                for o, x in zip(it['d'], qs[1:]):
                    if not x or si(x)[1] != ku:
                        continue
                    xv = si(x)[0]
                    if xv == kv or (x[1] == qs[0][1] and x[2] >= qs[0][2] and close(x[0], val, x[2])):
                        fails.append('%s: the distractor %r equals the key %s %s (SR-16)' % (w, o, sp.N(val, 6), unit))
            if (lvl, i) in REASONS:
                got = sorted((quantity(o) for o in it['d']), key=lambda x: x[0] if x else 0)
                for (v, why) in REASONS[(lvl, i)]:
                    if not any(x and close(x[0], v, x[2]) for x in got):
                        fails.append('%s: no distractor is %s (%s)' % (w, sp.N(v, 6), why))
            # every numeric claim written in a key or a working line
            for s in [it['correct'], it.get('q') or '']:
                for part in re.split(r'\\text\{[^{}]*\}', s):
                    sides = re.split(r'=|\\approx', part)
                    vals = [latex_value(x) for x in sides if x.strip()]
                    nums = [v for v in vals if v is not None]
                    if len(nums) >= 2:
                        last = sides[-1].strip()
                        dec = len(last.split('.')[1]) if re.fullmatch(r'-?\d+\.\d+', last) else 0
                        for v in nums[:-1]:
                            if not close(nums[-1], v, dec) and not close(v, nums[-1], 3):
                                fails.append('%s: %r: %s is not %s' % (w, s, sp.N(v, 6), sp.N(nums[-1], 6)))
            # KaTeX-drawn strings keep no prose outside \text{} (B7)
            for s in opts + ([it['q']] if it.get('q') else []):
                if '\\' in s or '^' in s or '{' in s:
                    bare = re.sub(r'\\text\{[^{}]*\}', ' ', s)
                    bare = re.sub(r'\\[A-Za-z]+', ' ', bare)
                    if re.search(r'[A-Za-z]{2,}\s+[A-Za-z]{2,}', bare):
                        fails.append('%s: %r is drawn by KaTeX with prose outside \\text{} (its spaces are lost; '
                                     'moments-master-t5-013)' % (w, s))
    for (lvl, i), (plvl, p) in CHAIN.items():
        prev = quantity(bank[plvl][p]['correct'])
        quoted = [R(x) for x in re.findall(r'= (\d+(?:\.\d+)?)', bank[lvl][i]['ctx'])]
        if prev is None or prev[0] not in quoted:
            fails.append('%s: follows %s but does not quote its key %s' % (
                where(lvl, i), where(plvl, p), prev[0] if prev else bank[plvl][p]['correct']))


# ------------------------------------------------------------------ Chromium
SWEEP_JS = r"""(lvl) => {
  const out = {rows: [], shown: [], wide: []};
  const vis = el => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(x => x.remove()); return c.textContent; };
  const realTimeout = window.setTimeout; window.setTimeout = () => 0;
  try {
    level = lvl; startGame();
    QUESTIONS[lvl].forEach((it, i) => {
      [it.correct, ...it.d].forEach(v => {
        questions = [it]; qIdx = 0; showQ();
        const card = document.getElementById('game');
        const raw = vis(card);
        if (/[\\^_{}]/.test(raw)) out.shown.push([i, raw.replace(/\s+/g, ' ')]);
        if (document.documentElement.scrollWidth > innerWidth) out.wide.push([i, document.documentElement.scrollWidth]);
        const btn = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === v);
        if (!btn) { out.rows.push([i, v, 'not shown']); return; }
        btn.click();
        const fb = document.getElementById('fb');      // absent on a page from before this fix
        out.rows.push([i, v, btn.classList.contains('correct') ? 'right' : btn.classList.contains('wrong') ? 'wrong' : 'unmarked',
          fb && fb.classList.contains('show') ? vis(fb) : '', !!(fb && fb.querySelector('.maffs-next-wrap')),
          document.querySelectorAll('#options .opt-btn').length]);
        if (document.documentElement.scrollWidth > innerWidth) out.wide.push([i, document.documentElement.scrollWidth]);
      });
    });
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    bank = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for vw, vh in ((390, 844), (320, 568)):
                ctx = browser.new_context(viewport={'width': vw, 'height': vh}, has_touch=True, is_mobile=True)
                page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
                ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
                if KATEX_DIR:
                    ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                        path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
                ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=html))
                ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
                page = ctx.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
                page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
                bank = page.evaluate('QUESTIONS')
                for lvl in ('alevel', 'level4'):
                    res = page.evaluate(SWEEP_JS, lvl)
                    for row in res['rows']:
                        i, v = row[0], row[1]
                        it = bank[lvl][i]
                        w = '%s at %dpx' % (where(lvl, i), vw)
                        if row[2] == 'not shown':
                            fails.append('%s: the option %r is not on screen' % (w, v))
                            continue
                        mark, fb, nxt, n = row[2:]
                        want = 'right' if v == it['correct'] else 'wrong'
                        if mark != want:
                            fails.append('%s: %r is marked %s' % (w, v, mark))
                        if want == 'wrong' and (not fb or 'Answer' not in fb or not nxt):
                            fails.append('%s: a wrong answer does not show the answer and wait for Next (canon 7.6)' % w)
                        if n != 4:
                            fails.append('%s: %d options on screen' % (w, n))
                    for i in sorted({i for i, _ in res['shown']}):
                        raw = next(r for j, r in res['shown'] if j == i)
                        m = re.search(r'.{0,30}[\\^_{}].{0,30}', raw)
                        fails.append('%s at %dpx: raw TeX on screen: %r (moments-master-t5-015)' % (
                            where(lvl, i), vw, m.group(0) if m else raw[:60]))
                    seen = set()
                    for i, sw in res['wide']:
                        if i not in seen:
                            seen.add(i)
                            fails.append('%s at %dpx: the page scrolls sideways (%dpx; moments-master-t5-013)' % (
                                where(lvl, i), vw, sw))
                if errors:
                    fails.append('page errors: %s' % '; '.join(errors[:3]))
                ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return bank


PLANTS = [
    ('alevel[28]', 't5-008: R_B keyed 50 N',
     "correct:'75 \\\\text{ N}',d:['50 \\\\text{ N}','100 \\\\text{ N}','25 \\\\text{ N}']},",
     "correct:'50 \\\\text{ N}',d:['75 \\\\text{ N}','100 \\\\text{ N}','25 \\\\text{ N}']},"),
    ('level4[14]', "t5-004: '5 kW' beside 5000 W", "'524 \\\\text{ W}'", "'5 \\\\text{ kW}'"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    ap.add_argument('--print-pins', action='store_true', help='print the content pins of the reviewed text items')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank:
        if args.print_pins:
            for (lvl, i) in sorted(REVIEWED):
                print("    ('%s', %d): '%s'," % (lvl, i, pin(bank[lvl][i])))
            return 0
        check_bank(fails, bank)
    print('%s: every key recomputed with SymPy, options distinct in value, every option clicked in Chromium' % SLUG)
    ok = True
    if not args.no_selftest and not args.against:
        for prefix, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-34s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(prefix)]
            ok = ok and bool(hit)
            print('  self-test %-34s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
