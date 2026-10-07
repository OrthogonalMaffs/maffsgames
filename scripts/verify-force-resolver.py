#!/usr/bin/env python3
# ci-line: E | Force Resolver (every key recomputed with SymPy, options distinct in value, every option clicked in Chromium) |
"""Force Resolver: every key recomputed with SymPy, options distinct in value, every option clicked in Chromium.

The tranche 5 audit (6 Oct 2026) found keys that their own data contradicts (level4 :179 keyed 1.79 m/s^2 for 1.40;
:189 a truss with no equilibrium force; alevel :164 keyed the 60 degree string's tension; :147 keyed "No" for a
particle that slides), distractors equal to their keys (50 cos 30 N beside 25 root 3 N, 12 cos 0 N beside 12 N),
duplicate-value wrong options, figures worked with g = 9.8 under a stated 9.81, an unstated g, and rounding at the
wrong place. Project Claude supplied replacement data for :189 (7 Oct 2026).

Keys. KEYS below holds, for every item with a numeric answer, the answer computed from the item's own data (SymPy,
  exact; angles in degrees; where an item gives a trig value, that value), with its unit. The shown key must match it
  at the precision it is shown to, in that unit. A text key that quotes figures (FIGS) has each figure recomputed.
  Every other text key is a reviewed judgement, pinned by the item's content hash (REVIEWED; --print-pins).
Options (SR-4, SR-16). No two options are equal in value (an option written as an expression, 25 root 3 N, is
  evaluated), and no distractor equals the key. Where this fix wrote a distractor (REASONS), it is recomputed from
  its named error.
Claims. Every numeric equality or approximation written in a key or a working line holds; every "Same ..." item
  quotes its predecessor's key.
Chromium (390x844 and 320x568). Every option of every item is clicked through the game's own handler: the key is
  marked right; any other option is marked wrong, shows the answer and waits for the shared Next control (MaffsNext,
  canon 7.6). No raw TeX on screen; the page never scrolls sideways.

A self-test plants two of the audit's own faults back (t5-002: the rope item keyed 1.79; t5-005: '50 cos 30 N' beside
the key 25 root 3 N); each must FAIL naming its item.

    python scripts/verify-force-resolver.py [--no-selftest] [--against FILE] [--katex-dir DIR] [--print-pins]
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

SLUG = 'force-resolver'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
R = sp.Rational
D = sp.pi / 180
SIN, COS, TAN, ATAN, SQRT = sp.sin, sp.cos, sp.tan, sp.atan, sp.sqrt


def deg(a):
    return a * D


def sd(a):
    return SIN(deg(a))


def cd(a):
    return COS(deg(a))


G10, G98, G981 = 10, R(98, 10), R(981, 100)
MS2 = 'm/s^2'

# Every numeric key from the item's own data: (value, unit).
KEYS = {
    ('alevel', 0): (10 * cd(30), 'N'), ('alevel', 1): (10 * sd(30), 'N'), ('alevel', 2): (20 * cd(45), 'N'),
    ('alevel', 3): (50 * cd(60), 'N'), ('alevel', 4): (50 * sd(60), 'N'), ('alevel', 5): (12 * cd(0), 'N'),
    ('alevel', 6): (12 * cd(90), 'N'), ('alevel', 7): (SQRT(8 ** 2 + 6 ** 2), 'N'),
    ('alevel', 8): (ATAN(R(6, 8)) / D, '°'), ('alevel', 9): (SQRT(5 ** 2 + 12 ** 2), 'N'),
    ('alevel', 10): (100 * R(8, 10), 'N'), ('alevel', 11): (100 * R(6, 10), 'N'),           # the given 0.8 and 0.6
    ('alevel', 12): (R(20, 5), MS2), ('alevel', 13): (3 * 2, 'N'), ('alevel', 14): (R(24, 8), 'kg'),
    ('alevel', 15): (R(30, 10), MS2), ('alevel', 16): ((30 - R(2, 10) * 10 * G10) / 10, MS2),
    ('alevel', 18): (800 * (G10 + 2), 'N'), ('alevel', 19): (800 * (G10 - R(3, 2)), 'N'),
    ('alevel', 20): ((756 - 70 * G98) / 70, MS2 + ' upward'), ('alevel', 21): (60 * G10, 'N'),
    ('alevel', 22): (5 * G10 * sd(30), 'N'), ('alevel', 23): (5 * G10 * cd(30), 'N'),
    ('alevel', 24): (G10 * sd(30), MS2), ('alevel', 25): (G10 * sd(45), MS2),
    ('alevel', 26): (10 * G10 * (sd(30) - R(3, 10) * cd(30)), 'N'), ('alevel', 27): (TAN(deg(30)), ''),
    ('alevel', 28): (2 * G10 * sd(20), 'N'), ('alevel', 29): (8 * G10 * sd(30) + 8 * 2, 'N'),
    ('alevel', 30): (G98 * (R('0.643') - R(2, 10) * R('0.766')), MS2),                    # the given 0.643, 0.766
    ('alevel', 35): (R((3 - 2) * G10, 5), MS2), ('alevel', 36): (2 * (G10 + 2), 'N'),
    ('alevel', 37): (R((5 - 3) * G10, 8), MS2), ('alevel', 38): (R(6 * G10, 10), MS2), ('alevel', 39): (4 * 6, 'N'),
    ('alevel', 40): ((6 * G10 - R(1, 4) * 4 * G10) / 10, MS2),
    ('alevel', 42): ((3 * G10 - 2 * G10 * sd(30)) / 5, MS2), ('alevel', 44): (R(4800 - 300, 1600), MS2),
    ('alevel', 45): (SQRT(3 ** 2 + 4 ** 2), 'N'), ('alevel', 46): (SQRT(5 ** 2 + 12 ** 2), 'N'),
    # 10 N hangs from strings at 30 and 60 degrees: T30 cos 30 = T60 cos 60; T30 sin 30 + T60 sin 60 = 10
    ('alevel', 47): (10 * cd(60) / (sd(30) * cd(60) + sd(60) * cd(30)), 'N'),
    ('alevel', 50): (5 * G10, 'N'), ('alevel', 51): (40, 'N'),
    ('level4', 0): (500 * R('0.906'), 'N'), ('level4', 1): (500 * R('0.423'), 'N'),
    ('level4', 2): (2 / cd(40), 'kN'), ('level4', 3): (10 / TAN(deg(50)), 'kN'),
    ('level4', 4): (SQRT(300 ** 2 + 400 ** 2), 'N'), ('level4', 5): (ATAN(R(400, 300)) / D, '°'),
    ('level4', 6): (80 * G981 * sd(15), 'N'), ('level4', 7): (200 * G981 * (sd(20) + R(3, 10) * cd(20)), 'N'),
    ('level4', 8): ((200 * cd(35) - R(1, 4) * (50 * G981 - 200 * sd(35))) / 50, MS2),
    ('level4', 9): (5 / sd(30), 'kN'), ('level4', 10): (R(6000 - 1000, 2000), MS2),
    ('level4', 11): (500 * R(5, 2) + 200, 'N'), ('level4', 12): (8 / sd(60), 'kN'),
    ('level4', 13): (250 * cd(20), 'N'), ('level4', 14): (3 / (2 * cd(45)), 'kN'),
    ('level4', 17): (60 * G981 / 2, 'N'), ('level4', 18): (SQRT(10 ** 2 + 8 ** 2), 'kN'),
}

# Figures quoted inside a text key: each (value, decimals) must appear in it
FIGS = {
    ('alevel', 32): [(5 * G10 * sd(30), 0), (R(4, 10) * 5 * G10 * cd(30), 1)],
    ('level4', 15): [(12 * G981 * sd(25), 1), (R(35, 100) * 12 * G981 * cd(25), 1)],
    ('alevel', 17): [(10 - 4, 0), (R(10 - 4, 2), 0)],
}

# The distractors this fix wrote, each from its named error
REASONS = {
    ('alevel', 4): [(50 * SQRT(3), 'sin 60 taken as root 3')],
    ('alevel', 5): [(1, 'cos 0 = 1, the 12 left out')],
    ('alevel', 22): [(5 * sd(30), 'g left out')],
    ('alevel', 23): [(5 * cd(30), 'g left out')],
    ('alevel', 47): [(10 * cd(30) / (sd(30) * cd(60) + sd(60) * cd(30)), "the 60 degree string's tension")],
    ('level4', 7): [(200 * G981 * sd(20), 'no friction'), (200 * G981, 'mg'), (R(3, 10) * 200 * G981 * cd(20), 'friction only')],
    ('level4', 8): [(R(200, 50), 'no friction, the whole 200 N'), ((200 * cd(35) - R(1, 4) * 50 * G981) / 50, 'the rope does not lift: R = mg'),
                    (200 * cd(35) / 50, 'no friction')],
    ('level4', 13): [(250 / cd(20), 'divided by cos 20')],
    ('level4', 18): [(18, 'the forces added'), (2, 'subtracted'), (SQRT(10 ** 2 - 8 ** 2), 'root (10^2 - 8^2)')],
}

# The verdict a text key must give (each item's FIGS decide it: 25 > 17.3 and 49.8 > 37.3, so it slides)
VERDICT = {('alevel', 32): 'Yes', ('level4', 15): 'Yes'}

CHAIN = {('alevel', 36): ('alevel', 35), ('alevel', 39): ('alevel', 38), ('level4', 11): ('level4', 10)}

REVIEWED = {
    ('alevel', 31): '9961b5b3', ('alevel', 33): '6259496e', ('alevel', 34): '3a70ffc8', ('alevel', 41): '8194136d',
    ('alevel', 43): '231e59e2', ('alevel', 48): '5ac7988b', ('alevel', 49): 'ea4371ce', ('level4', 16): 'd7cdb64c',
    ('level4', 19): 'c25764d0',
}

TAGS = {('level4', 8): 't5-002', ('level4', 18): 't5-003', ('alevel', 47): 't5-004', ('alevel', 23): 't5-005',
        ('alevel', 5): 't5-006', ('alevel', 32): 't5-007', ('level4', 7): 't5-011', ('alevel', 31): 't5-012',
        ('alevel', 35): 't5-013', ('alevel', 6): 'f0-001', ('alevel', 4): 't5-014', ('alevel', 22): 't5-014',
        ('level4', 13): 't5-014', ('alevel', 11): 't5-014', ('level4', 1): 't5-014', ('level4', 15): 't5-014',
        ('level4', 9): 't5-014'}


def where(lvl, i):
    t = TAGS.get((lvl, i))
    return '%s[%d]%s' % (lvl, i, ' (force-resolver-%s)' % t if t else '')


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
    """A single quantity -> (value, unit, decimals): '5.375 \\text{ kN}', '25\\sqrt{3} \\approx 43.3 \\text{ N}' (the
    value after the last = or \\approx), '36.9°', '4 \\text{ m/s}^2 \\text{ upward}', or an expression with a unit,
    '10\\tan 30° \\text{ N}' (evaluated; decimals 6). None for anything else (text, two quantities, a symbol)."""
    s = opt
    for sep in ('\\approx', '='):
        if sep in s:
            s = s.rsplit(sep, 1)[1]
    s = s.strip()
    unit = ' '.join(x.strip() for x in re_findall(r'\\text\{([^{}]*)\}', s))
    head = re.sub(r'\\text\{[^{}]*\}', ' ', s)
    power = re.search(r'\^\{?2\}?', head)
    head = re.sub(r'\^\{?2\}?\s*$', '', head.strip()) if power else head
    unit = (unit.replace('m/s', 'm/s^2', 1) if power and 'm/s' in unit else unit).strip()
    if head.strip().endswith('°') and re.fullmatch(r'-?\d+(?:\.\d+)?°', head.strip()):
        num = head.strip()[:-1]
        return R(num), '°', len(num.split('.')[1]) if '.' in num else 0
    m = re.fullmatch(r'\s*(-?\d+(?:\.\d+)?)\s*', head)
    if m:
        if re.search(r'\d', unit.replace('^2', '')):
            return None
        num = m.group(1)
        return R(num), unit, len(num.split('.')[1]) if '.' in num else 0
    v = latex_value(head)
    if v is None or not unit or re.search(r'\d', unit.replace('^2', '')):
        return None
    return sp.nsimplify(v) if v.is_Rational else v, unit, 6


def re_findall(p, s):
    return re.findall(p, s)


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
            elif (lvl, i) in FIGS:
                if (lvl, i) in VERDICT and not it['correct'].startswith(VERDICT[(lvl, i)]):
                    fails.append('%s: the key %r should say %s' % (w, it['correct'], VERDICT[(lvl, i)]))
                for v, dec in FIGS[(lvl, i)]:
                    want = ('%.' + str(dec) + 'f') % float(sp.N(v, 30))
                    if not re.search(r'(?<![\d.])' + re.escape(want) + r'(?![\d])', it['correct']):
                        fails.append('%s: the key %r should quote %s' % (w, it['correct'], want))
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
                    # the same value in SI with the same words; or a figure that an option written as an expression
                    # rounds to (43.3 N beside 25 root 3 N)
                    same = a and b and a[1] == b[1] and (a[0] == b[0] or (
                        qs[j][2] == 6 and qs[k][2] < 6 and close(b[0], a[0], qs[k][2])) or (
                        qs[k][2] == 6 and qs[j][2] < 6 and close(a[0], b[0], qs[j][2])))
                    if same:
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
                                     'force-resolver-t5-014)' % (w, s))
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
                        fails.append('%s at %dpx: raw TeX on screen: %r (force-resolver-t5-014)' % (
                            where(lvl, i), vw, m.group(0) if m else raw[:60]))
                    seen = set()
                    for i, sw in res['wide']:
                        if i not in seen:
                            seen.add(i)
                            fails.append('%s at %dpx: the page scrolls sideways (%dpx; force-resolver-t5-014)' % (
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
    ('level4[8]', 't5-002: the rope item keyed 1.79',
     "correct:'1.40 \\\\text{ m/s}^2'", "correct:'1.79 \\\\text{ m/s}^2'"),
    ('alevel[23]', "t5-005: '50 cos 30 N' beside 25 root 3",
     "d:['25 \\\\text{ N}','50 \\\\text{ N}','4.33 \\\\text{ N}']},", "d:['25 \\\\text{ N}','50 \\\\text{ N}','50\\\\cos 30° \\\\text{ N}']},"),
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
