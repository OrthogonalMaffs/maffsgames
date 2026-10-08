#!/usr/bin/env python3
# ci-line: B3 | Unit Converter (every key recomputed from its prompt, exact pi; precision stated; displayed numbers comma-grouped, marking unchanged; answer once; level key; score by correct answers only; calculator on a phone) |  && --selftest
"""Independent verification of Unit Converter (contract UC-FIX and its amendment, 8 Oct 2026; tranche 4 and resit audits,
docs/audits/findings/unit-converter.yml).

The bank is read from the served page (L, A, V, T, E: 58 items; GCSE serves 48, A-Level 38, Level 4 42).

  - KEYS (t4-004, r-001, r-002): every key is recomputed from the prompt's own numbers, exactly: a unit table of exact
    factors (a conversion the prompt defines, "1 inch = 2.54 cm", is read from the prompt), shapes from the numbers the
    prompt gives, pi exact unless the prompt says "pi ≈ 3.14". A key that is not the exact value fails unless the prompt
    states its precision ("Give your answer to N significant figures") and the key is the exact value rounded half up
    to it. The key's unit is the one asked for. Every distractor is wrong (not the exact value, not the key's value),
    and the four options are distinct. A worked figure written "N..." is the exact answer cut short, and 3.14 appears
    only where the prompt says pi ≈ 3.14.
  - "≈" (t4-006): never before an exact definition (1 inch = 2.54 cm, 1 foot = 0.3048 m, ...).
  - DISPLAY (t4-006; Jon's ruling, 9 Oct 2026: "One formatter function for all displayed numbers. Verifier proves
    marking unchanged on all 59 items and that every displayed number of 1,000 or more has a comma"; the bank has 58):
    in Chromium every item is rendered by the game's own nextQ(); each option's dataset.val is exactly a stored
    string (the key or a distractor), so marking compares what it always did; the key is marked right and every
    distractor wrong, read from the page's classes; every visible number of 1,000 or more on every screen (start,
    each question, each worked solution, results) has thousands commas, and the prompt, options and steps are the
    stored text with commas added and nothing else changed.
  - ANSWER ONCE (t4-001): with MaffsLock's real window, a wrong answer and then a click, Enter and Space on the key
    mark nothing more: the score stays 0, one question_answered for the question. A session ends once: one
    game_completed and one submit, whatever is pressed after.
  - LEVEL KEY (t4-003): ?level=constructor, __proto__, toString, xyz, l4, nonsense: the start screen at GCSE, nothing
    thrown or logged on load; Start logs and serves GCSE and the session submits under gcse. ?level=level4 serves
    only Level 4's items and logs and submits level4.
  - TIMER AND SCORE (t4-005, Jon's ruling, 8 Oct 2026): nothing on screen changes while a question waits 3 s (no
    visible clock); two sessions on the same questions with the same answers, one answered at once and one after
    25 s a question (Playwright's clock), score the same, and the score is 100 per correct answer.
  - CALCULATOR (Jon, 8 Oct 2026; canon §4.4): at 390x844 on a touch phone the badge shows; the calculator opens,
    works 2500 ÷ 1000 = 2.5 and closes, and while it is open the prompt and all four options are in the window and
    nothing scrolls sideways; at 1366x768 and 1920x1080 it docks beside the card.

    python scripts/verify-unit-converter.py [--against FILE] [--selftest]

--against FILE serves FILE as the game page (main's copy: it fails naming t4-001, the unstated roundings and the
level key). --selftest plants one fault per finding in copies of the page and requires each to be caught.
"""
import argparse
import os
import re
import sys
from collections import defaultdict
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'unit-converter'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LEVELS = {'gcse': ('L', 'A', 'V', 'T'), 'alevel': ('A', 'V', 'T'), 'level4': None}
SERVED = {'gcse': 48, 'alevel': 38, 'level4': 42}
PER_CORRECT = 100
# pi to 50 places, as a fraction: enough to round any key here to its stated figures without doubt
PI = F('3.14159265358979323846264338327950288419716939937510')

# Exact factors to SI (m, m², m³, Pa, N, m³/s, m/s). Every one is a definition, not a measurement.
UNITS = {
    'mm': (F(1, 1000), 1), 'cm': (F(1, 100), 1), 'm': (F(1), 1), 'km': (F(1000), 1),
    'mm²': (F(1, 10**6), 2), 'cm²': (F(1, 10**4), 2), 'm²': (F(1), 2), 'km²': (F(10**6), 2), 'hectare': (F(10**4), 2),
    'mm³': (F(1, 10**9), 3), 'cm³': (F(1, 10**6), 3), 'm³': (F(1), 3), 'litres': (F(1, 1000), 3),
    'litre': (F(1, 1000), 3), 'ml': (F(1, 10**6), 3),
    'Pa': (F(1), 'P'), 'kPa': (F(1000), 'P'), 'MPa': (F(10**6), 'P'), 'GPa': (F(10**9), 'P'), 'bar': (F(10**5), 'P'),
    'N/mm²': (F(10**6), 'P'), 'N': (F(1), 'N'), 'kN': (F(1000), 'N'), 'MN': (F(10**6), 'N'),
    'cm³/s': (F(1, 10**6), 'Q'), 'm³/s': (F(1), 'Q'), 'm/s': (F(1), 'v'), 'km/h': (F(1000, 3600), 'v'),
}
ALIASES = {'metres': 'm', 'inches': 'inch', 'feet': 'foot', 'litre': 'litres'}
# Exact definitions a prompt may quote: "≈" before one of these is wrong (t4-006).
EXACT_DEFS = {('inch', 'cm'): F('2.54'), ('foot', 'm'): F('0.3048'), ('mile', 'm'): F('1609.344')}
NUM = r'(\d[\d,]*(?:\.\d+)?)'


def num(s):
    return F(s.replace(',', ''))


def dec(x):
    """A fraction as the decimal a student reads (every value here terminates within 12 places)."""
    return ('%.12f' % float(x)).rstrip('0').rstrip('.')


def fmt(s):
    """The ruled display: thousands commas in every run of 4+ whole-number digits (not after a point or comma)."""
    return re.sub(r'(^|[^\d.,])(\d{4,})', lambda m: m.group(1) + '{:,}'.format(int(m.group(2))), s)


def bare_thousands(text):
    """Every number of 1,000 or more in text shown without its commas."""
    return [m.group(2) for m in re.finditer(r'(^|[^\d.,])(\d{4,})', text)]


def unit_key(u):
    return ALIASES.get(u, u)


class Value:
    """coef × pi^k, exact."""
    def __init__(self, coef, k=0):
        self.coef, self.k = F(coef), k

    def approx(self):
        return self.coef * PI ** self.k


def round_sf(x, n):
    """x rounded half up to n significant figures, exactly."""
    if x == 0:
        return x
    e = 0
    a = abs(x)
    while a >= 10:
        a /= 10
        e += 1
    while a < 1:
        a *= 10
        e -= 1
    scale = F(10) ** (n - 1 - e)
    r = F(int(abs(x) * scale + F(1, 2))) / scale
    return r if x > 0 else -r


def defined_units(p):
    """Conversions the prompt defines, "(1 inch = 2.54 cm)", with the sign used."""
    out = {}
    for m in re.finditer(r'1 (inch|foot|mile) (=|≈) ' + NUM + r' (cm|m)\b', p):
        out[m.group(1)] = (num(m.group(3)) * UNITS[m.group(4)][0], m.group(2), (m.group(1), m.group(4)),
                           num(m.group(3)))
    return out


def lengths(p):
    return [(num(m.group(1)) * UNITS[m.group(2)][0]) for m in re.finditer(NUM + r' (mm|cm|km|m)\b', p)]


def recompute(q):
    """The exact answer to q's prompt, in SI, and the unit asked for; or (None, reason)."""
    p = q['p']
    defs = defined_units(p)
    use314 = bool(re.search(r'π ≈ 3\.14', p))
    pi = Value(F('3.14')) if use314 else Value(1, 1)

    def times_pi(v):
        return Value(v * pi.coef, pi.k)
    m = (re.match(r'^Convert ' + NUM + r' (\S+?) to (\S+?)(?: \(.*\))?(?:\. .*)?$', p) or
         re.match(r'^Stress = ' + NUM + r' (\S+?)\. Convert to (\S+?)\.$', p))
    if m:
        x, u1, u2 = num(m.group(1)), unit_key(m.group(2)), unit_key(m.group(3))
        if u1 == 'mph':
            if 'mile' not in defs:
                return None, None, 'mph with no mile defined'
            si = x * defs['mile'][0] / 3600
        elif u1 in ('inch', 'foot'):
            if u1 not in defs:
                return None, None, '%s with no definition in the prompt' % u1
            si = x * defs[u1][0]
        elif u1 in UNITS:
            si = x * UNITS[u1][0]
        else:
            return None, None, 'unknown unit %r' % u1
        return Value(si), u2, None
    m = re.match(r'^A tank holds ' + NUM + r' (\S+)\. How many (litres)\?$', p)
    if m:
        return Value(num(m.group(1)) * UNITS[m.group(2)][0]), m.group(3), None
    ask = re.search(r'(?:Area|Volume|area) in (\S+?)\?|Volume in (litres)\?', p)
    if not ask:
        return None, None, 'no unit asked'
    u2 = ask.group(1) or ask.group(2)
    ls = lengths(p.split('?')[0])
    low = p.lower()
    if re.search(r'rectangle|floor|sheet metal', low) and len(ls) == 2:
        return Value(ls[0] * ls[1]), u2, None
    if 'square has side' in low and len(ls) == 1:
        return Value(ls[0] ** 2), u2, None
    if re.search(r'box|room|swimming pool', low) and len(ls) == 3:
        return Value(ls[0] * ls[1] * ls[2]), u2, None
    if 'cube has side' in low and len(ls) == 1:
        return Value(ls[0] ** 3), u2, None
    if low.startswith('circle: radius') and len(ls) == 1:
        return times_pi(ls[0] ** 2), u2, None
    if low.startswith('cylinder: radius') and len(ls) == 2:
        return times_pi(ls[0] ** 2 * ls[1]), u2, None
    if low.startswith('pipe: diameter') and len(ls) == 2:
        return times_pi((ls[0] / 2) ** 2 * ls[1]), u2, None
    if 'shaft has diameter' in low and len(ls) == 1:
        return times_pi((ls[0] / 2) ** 2), u2, None
    return None, None, 'no rule reads this prompt'


def parse_option(s):
    m = re.match(r'^' + NUM + r' (\S+)$', s)
    return (num(m.group(1)), unit_key(m.group(2))) if m else (None, None)


def items(bank):
    return [(name, i, q) for name in ('L', 'A', 'V', 'T', 'E') for i, q in enumerate(bank[name])]


def check_bank(rep, bank, verbose=False):
    """Static checks on the bank: keys, precision, options, worked figures, "≈"."""
    n = 0
    for name, i, q in items(bank):
        where = '%s[%d] %s' % (name, i, q['p'][:48])
        n += 1
        p = q['p']
        for unit, (val, sign, pair, given) in defined_units(p).items():
            if sign == '≈' and EXACT_DEFS.get(pair) == given:
                rep[('t4-006', where)].append('"1 %s ≈ %s %s" is exact by definition: "=", not "≈"'
                                              % (unit, dec(given), pair[1]))
        v, u2, why = recompute(q)
        if v is None:
            rep[('verifier', where)].append('cannot recompute: ' + why)
            continue
        fac = UNITS[unit_key(u2)][0]
        exact = Value(v.coef / fac, v.k)
        kv, ku = parse_option(q['c'])
        if kv is None or ku != unit_key(u2):
            rep[('key', where)].append('key %r is not a number in the asked unit %s' % (q['c'], u2))
            continue
        sf = re.search(r'Give your answer to (\d+) significant figures\.', p)
        if exact.k == 0 and kv == exact.coef:
            pass
        elif sf and kv == round_sf(exact.approx(), int(sf.group(1))):
            pass
        elif sf:
            rep[('key', where)].append('key %s is not the exact value %s to %s s.f.' % (dec(kv), float(exact.approx()),
                                                                                       sf.group(1)))
        elif abs(kv - exact.approx()) / exact.approx() < F(1, 100):
            rep[('t4-004', where)].append('key %s is %s rounded, and the prompt states no precision'
                                          % (q['c'], float(exact.approx())))
        else:
            rep[('key', where)].append('key %s, recomputed %s' % (q['c'], float(exact.approx())))
        opts = [q['c']] + q['d']
        vals = []
        for d in q['d']:
            dv, du = parse_option(d)
            if du != ku:
                rep[('distractor', where)].append('%r is not in the asked unit' % d)
                continue
            if (exact.k == 0 and dv == exact.coef) or dv == kv:
                rep[('distractor', where)].append('%r is the right answer' % d)
            vals.append(dv)
        if len(opts) != 4 or len(set(vals + [kv])) != 4:
            rep[('distractor', where)].append('options %s are not four distinct values' % opts)
        for st in q.get('s', []):
            for m in re.finditer(NUM + r'\.\.\.', st):
                shown = m.group(1).replace(',', '')
                decimals = len(shown.split('.')[1]) if '.' in shown else 0
                cut = F(int(exact.approx() * 10 ** decimals)) / 10 ** decimals
                if num(shown) != cut:
                    rep[('working', where)].append('"%s..." is not the exact answer %s cut short'
                                                   % (m.group(1), float(exact.approx())))
            if '3.14' in st and not re.search(r'π ≈ 3\.14', p):
                rep[('t4-004', where)].append('the working uses 3.14 for π, which the prompt does not state: %r' % st)
        if verbose:
            print('  %-60s key %-14s exact %s' % (where, q['c'], float(exact.approx())))
    return n


def report_notes(bank):
    """Reported, never failed: "=" before a value that is not the exact definition (filed as t4-007)."""
    notes = []
    for name, i, q in items(bank):
        for unit, (val, sign, pair, given) in defined_units(q['p']).items():
            if sign == '=' and pair in EXACT_DEFS and EXACT_DEFS[pair] != given:
                notes.append('%s[%d]: "1 %s = %s %s" is not exact (1 %s = %s %s); the key holds either way'
                             % (name, i, unit, dec(given), pair[1], unit, dec(EXACT_DEFS[pair]), pair[1]))
    return notes


# --- Chromium -----------------------------------------------------------------------------------------------------

HOOKS = """(() => { window.__ev = []; window.__sub = []; let inner;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (e, p) { window.__ev.push([e, p]); return inner && inner.apply(this, arguments); }; },
    set(v) { inner = v; } });
  Object.defineProperty(window, 'MaffsLeaderboard', { configurable: true,
    get() { return { submitScore() { window.__sub.push([...arguments]); return Promise.resolve(); } }; }, set(v) {} });
})();"""
SEED = """(() => { let s = 1234567; Math.random = function () { s |= 0; s = s + 0x6D2B79F5 | 0;
  let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
  return ((t ^ t >>> 14) >>> 0) / 4294967296; }; })();"""
# Visible text of an element: what a student can read (hidden screens and elements excluded).
VISIBLE_TEXT = """(sel) => { const out = [];
  const w = document.createTreeWalker(document.querySelector(sel), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode, e = n.parentElement;
    if (!n.textContent.trim() || !e || !e.checkVisibility()) continue;
    const st = getComputedStyle(e); if (st.visibility === 'hidden' || +st.opacity === 0) continue;
    out.push(n.textContent); }
  return out.join(' | '); }"""
# Every item rendered by the game's own nextQ() and every option pressed once. Returns, per item: the shown prompt,
# context, each option's dataset.val, text and mark, the worked steps shown after a wrong option, and the visible text.
SWEEP = """(groups) => {
  const out = [], game = document.getElementById('game'), opts = document.getElementById('options');
  const reset = () => { if (window.MaffsLock) MaffsLock.screen(game); };
  for (const [name, i] of groups) {
    const q = eval(name)[i];
    const item = { name, i, options: [] };
    const vals = [q.c, ...q.d];
    for (const v of vals) {
      reset(); pool = [q]; qIdx = 0; score = 0; correctN = 0; total = 0; nextQ();
      if (!item.prompt) {
        item.prompt = document.getElementById('prompt').textContent;
        item.context = document.getElementById('context').textContent;
        item.shown = [...opts.querySelectorAll('.opt-btn')].map(b => [b.dataset.val, b.textContent]);
      }
      const b = [...opts.querySelectorAll('.opt-btn')].find(x => x.dataset.val === v)
        || [...opts.querySelectorAll('.opt-btn')].find(x => x.textContent.replace(/,/g, '') === v.replace(/,/g, ''));
      if (!b) { item.options.push([v, null, null]); continue; }
      b.click();
      const right = b.classList.contains('correct') && !b.classList.contains('wrong');
      const wrong = b.classList.contains('wrong');
      item.options.push([v, right, wrong]);
      if (wrong && !item.steps) {
        item.steps = [...document.querySelectorAll('#solution .step')].map(s => s.textContent);
        item.mc = (document.querySelector('#solution .misconception') || {}).textContent || '';
        item.visible = VIS('#game');
      }
    }
    out.push(item);
  }
  reset();
  return out;
}"""


def new_context(browser, viewport=(1280, 900), mobile=False, fresh=False, seed=False):
    ctx = browser.new_context(reduced_motion='reduce', viewport={'width': viewport[0], 'height': viewport[1]},
                              is_mobile=mobile, has_touch=mobile)
    if not fresh:
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script(HOOKS)
    if seed:
        ctx.add_init_script(SEED)
    return ctx


def open_page(ctx, base, src, query='', errors=None):
    page = ctx.new_page()
    errs = [] if errors is None else errors
    page.on('pageerror', lambda e: errs.append(str(e).splitlines()[0]))
    page.route('**/games/%s/**' % SLUG, lambda r: r.fulfill(status=200, content_type='text/html; charset=utf-8',
                                                             body=src))
    page.goto('%s/games/%s/%s' % (base.rstrip('/'), SLUG, query))
    page.wait_for_function("typeof startGame === 'function' && typeof L !== 'undefined'")
    page.evaluate('(f) => { window.VIS = eval(f); }', VISIBLE_TEXT)
    return page, errs


def read_bank(page):
    return page.evaluate("() => ({L, A, V, T, E})")


def check_display(rep, page, bank):
    """Every item rendered and marked; marking compares the stored strings; every shown number grouped (t4-006)."""
    start = page.evaluate("() => VIS('#menu')")
    for b in bare_thousands(start):
        rep[('t4-006', 'start screen')].append('%s shown without commas' % b)
    page.evaluate("() => startGame()")
    groups = [[name, i] for name, i, _ in items(bank)]
    got = page.evaluate(SWEEP, groups)
    stored = {(name, i): q for name, i, q in items(bank)}
    for it in got:
        q = stored[(it['name'], it['i'])]
        where = '%s[%d] %s' % (it['name'], it['i'], q['p'][:48])
        vals = sorted(v for v, _ in it['shown'])
        if vals != sorted([q['c']] + q['d']):
            rep[('marking', where)].append('dataset.val %s is not the stored options %s' % (vals, [q['c']] + q['d']))
        for v, text in it['shown']:
            if text != fmt(v):
                rep[('t4-006', where)].append('option %r is shown as %r, not %r' % (v, text, fmt(v)))
        if it['prompt'] != fmt(q['p']):
            rep[('t4-006', where)].append('prompt shown as %r, not %r' % (it['prompt'], fmt(q['p'])))
        for v, right, wrong in it['options']:
            want = v == q['c']
            if right is None:
                rep[('marking', where)].append('no option with dataset.val %r' % v)
            elif right is not want or wrong is want:
                rep[('marking', where)].append('%r marked %s, expected %s' % (v, 'right' if right else 'wrong' if wrong
                                                                            else 'nothing', 'right' if want else 'wrong'))
        if it.get('steps') is not None and it['steps'] != [fmt(s) for s in q.get('s', [])]:
            rep[('t4-006', where)].append('worked steps shown as %s' % it['steps'])
        for text in [it['prompt'], it['context'], it.get('visible') or ''] + [t for _, t in it['shown']]:
            for b in bare_thousands(text):
                rep[('t4-006', where)].append('%s shown without commas' % b)
        if 'Use a calculator.' not in (it['context'] or ''):
            rep[('calculator', where)].append('the question does not say "Use a calculator." (canon §4.4)')
    return len(got)


def check_served(rep, page, bank):
    for lv, n in SERVED.items():
        got = page.evaluate("""(lv) => { level = lv; startGame(); const p = pool.length;
          const bank = lv === 'gcse' ? [...L, ...A, ...V, ...T] : lv === 'alevel' ? [...A, ...V, ...T]
            : [...L.slice(0, 4), ...A.slice(0, 5), ...V, ...T, ...E];
          return [bank.length, p, pool.every(q => bank.includes(q))]; }""", lv)
        if got[0] != n or got[1] != 20 or not got[2]:
            rep[('bank', lv)].append('bank %d (expected %d), session %d (20), from its own bank %s' % (got[0], n, got[1],
                                                                                                      got[2]))


def settle(page):
    page.wait_for_function("() => !window.MaffsLock || !MaffsLock.isFresh()")


def check_lock(rep, browser, base, src):
    """t4-001: a wrong answer, then the key pressed by click, Enter and Space, marks nothing more."""
    ctx = new_context(browser, fresh=True)
    page, errors = open_page(ctx, base, src)
    page.evaluate("() => { level = 'gcse'; startGame(); }")
    settle(page)
    page.evaluate("() => { const k = currentQ.c; [...document.querySelectorAll('#options .opt-btn')]"
                  ".find(b => b.dataset.val !== k).click(); }")
    for how in ('click', 'Enter', 'Space'):
        if how == 'click':
            page.evaluate("() => { const k = currentQ.c; [...document.querySelectorAll('#options .opt-btn')]"
                          ".find(b => b.dataset.val === k).click(); }")
        else:
            page.evaluate("() => { const k = currentQ.c; const b = [...document.querySelectorAll('#options .opt-btn')]"
                          ".find(x => x.dataset.val === k); b.removeAttribute('disabled'); b.focus(); }")
            page.keyboard.press(how)
    st = page.evaluate("""() => ({score: document.getElementById('score').textContent,
      correct: document.getElementById('correctCount').textContent,
      answered: __ev.filter(e => e[0] === 'question_answered').length})""")
    if st != {'score': '0', 'correct': '0', 'answered': 1}:
        rep[('t4-001', 'answer once')].append('a wrong answer, then the revealed key clicked and pressed with Enter and '
                                              'Space: score %s, correct %s, %d question_answered (0, 0, 1)'
                                              % (st['score'], st['correct'], st['answered']))
    # play to the end; press the last answer and every button again: the session ends once
    page.evaluate("() => { pool = pool.slice(0, 2); }")
    for _ in range(6):
        if page.evaluate("document.getElementById('results').classList.contains('active')"):
            break
        nxt = page.query_selector('#solution .maffs-next, #solution .next-btn')
        if nxt and nxt.is_visible():
            page.evaluate("(b) => b.click()", nxt)
        else:
            settle(page)
            page.evaluate("() => { const k = currentQ.c; const b = [...document.querySelectorAll('#options .opt-btn')]"
                          ".find(x => x.dataset.val === k); b.click(); b.click(); }")
        page.wait_for_timeout(1200)
    page.evaluate("() => { try { endGame(); endGame(); } catch (e) {} }")
    st = page.evaluate("() => ({done: __ev.filter(e => e[0] === 'game_completed').length, sub: __sub.length})")
    if st != {'done': 1, 'sub': 1}:
        rep[('t4-001', 'session end')].append('%d game_completed and %d submits for one session (1 and 1)'
                                              % (st['done'], st['sub']))
    if errors:
        rep[('page', 'lock')].append('; '.join(errors[:2]))
    ctx.close()


def check_level(rep, browser, base, src):
    """t4-003: an unknown key leaves the start screen at GCSE; a valid key is served, logged and submitted."""
    ctx = new_context(browser)
    for bad in ('constructor', '__proto__', 'toString', 'xyz', 'l4', 'nonsense'):
        page, errors = open_page(ctx, base, src, '?level=' + bad)
        st = page.evaluate("""() => ({start: document.getElementById('menu').classList.contains('active'),
          level: String(level), active: [...document.querySelectorAll('.level-btn.active')].map(b => b.dataset.level),
          logged: __ev.length})""")
        try:
            page.evaluate("() => { startGame(); pool = pool.slice(0, 1); }")
            page.evaluate("() => { const k = currentQ.c; [...document.querySelectorAll('#options .opt-btn')]"
                          ".find(b => b.dataset.val === k).click(); }")
            page.wait_for_function("document.getElementById('results').classList.contains('active')", timeout=5000)
            sent = page.evaluate("""() => ({started: (__ev.find(e => e[0] === 'game_started') || [0, {}])[1].level,
              sub: __sub.map(s => s[1])})""")
        except Exception as ex:
            errors.append(str(ex).splitlines()[0])
            sent = None
        ok = (st == {'start': True, 'level': 'gcse', 'active': ['gcse'], 'logged': 0} and not errors
              and sent == {'started': 'gcse', 'sub': ['gcse']})
        if not ok:
            rep[('t4-003', '?level=' + bad)].append('on load %s; after Start %s; errors %s (the start screen at GCSE, '
                                                    'nothing logged; then gcse logged and submitted)'
                                                    % (st, sent, errors[:1]))
        page.close()
    page, errors = open_page(ctx, base, src, '?level=level4')
    st = page.evaluate("""() => { startGame(); const lv4 = [...L.slice(0, 4), ...A.slice(0, 5), ...V, ...T, ...E];
      return {active: [...document.querySelectorAll('.level-btn.active')].map(b => b.dataset.level),
        started: (__ev.find(e => e[0] === 'game_started') || [0, {}])[1].level, own: pool.every(q => lv4.includes(q)),
        e: pool.some(q => E.includes(q))}; }""")
    if st != {'active': ['level4'], 'started': 'level4', 'own': True, 'e': True}:
        rep[('t4-003', '?level=level4')].append('%s (Level 4 chosen, logged, and served its own bank)' % st)
    page.close()
    ctx.close()


def play_session(page, pattern, wait_ms):
    """Answer the session's questions per pattern (True right), wait_ms of clock before each answer; the score."""
    page.evaluate("() => { level = 'gcse'; startGame(); }")
    for right in pattern:
        page.clock.run_for(wait_ms)
        page.evaluate("""(r) => { const k = currentQ.c; [...document.querySelectorAll('#options .opt-btn')]
          .find(b => r ? b.dataset.val === k : b.dataset.val !== k).click(); }""", right)
        if right:
            page.clock.run_for(1100)
        else:
            # Next's floor runs on the page's (fake) clock: let it pass, then press Next and let the advance land
            page.clock.run_for(3100)
            page.evaluate("() => { const b = document.querySelector('#solution .maffs-next, #solution .next-btn'); "
                          "b.click(); }")
            page.clock.run_for(100)
    page.clock.run_for(1100)
    return page.evaluate("() => ({score: score, correct: correctN, done: "
                         "document.getElementById('results').classList.contains('active')})")


def check_timer_and_score(rep, browser, base, src):
    """t4-005: no visible clock; the score depends on correct answers only."""
    ctx = new_context(browser)
    page, errors = open_page(ctx, base, src)
    page.evaluate("() => { level = 'gcse'; startGame(); }")
    page.wait_for_timeout(300)
    before = page.evaluate("() => VIS('#game')")
    page.wait_for_timeout(3000)
    after = page.evaluate("() => VIS('#game')")
    labels = page.evaluate("() => [...document.querySelectorAll('#game .hud-label')].filter(e => e.checkVisibility())"
                           ".map(e => e.textContent.trim().toLowerCase())")
    if before != after or 'time' in labels:
        rep[('t4-005', 'visible clock')].append('the question screen changes while it waits (%r -> %r), or shows a Time '
                                                'item %s: the timer is to be hidden' % (before[:80], after[:80], labels))
    ctx.close()
    pattern = [i % 3 != 1 for i in range(20)]
    scores = []
    for wait in (0, 25000):
        ctx = new_context(browser, seed=True)
        ctx_page, errs = open_page(ctx, base, src)
        ctx_page.clock.install()
        scores.append(play_session(ctx_page, pattern, wait))
        ctx.close()
    want = {'score': PER_CORRECT * sum(pattern), 'correct': sum(pattern), 'done': True}
    if scores[0] != scores[1] or scores[0] != want:
        rep[('t4-005', 'score')].append('the same answers scored %s answered at once and %s after 25 s each (both %s: '
                                        '%d per correct answer, no time)' % (scores[0], scores[1], want, PER_CORRECT))


def check_phone(rep, browser, base, src):
    """The badge, and the calculator on a 390x844 touch phone; docked on a desktop."""
    ctx = new_context(browser, (390, 844), mobile=True)
    page, errors = open_page(ctx, base, src)
    if not page.evaluate("() => { const b = document.querySelector('#menu .calc-badge[data-calc=\"required\"]'); "
                         "return !!b && b.checkVisibility() && b.textContent === 'Calculator required'; }"):
        rep[('calculator', 'badge')].append('the start screen shows no "Calculator required" badge')
    page.evaluate("() => { level = 'gcse'; startGame(); pool = [T[3], T[3]]; qIdx = 0; nextQ(); }")
    if not page.query_selector('.maffs-calc-toggle'):
        rep[('calculator', '390x844')].append('no calculator on the question screen')
        ctx.close()
        return
    page.tap('.maffs-calc-toggle')
    for key in ('2', '5', '0', '0', '÷', '1', '0', '0', '0', '='):
        page.tap('.maffs-calc-key:text-is("%s")' % key)
    res = page.evaluate("() => document.querySelector('.maffs-calc-result').textContent.trim()")
    fit = page.evaluate("""() => { const v = innerHeight - 40, R = e => e.getBoundingClientRect();
      const els = [document.getElementById('prompt'), ...document.querySelectorAll('#options .opt-btn')];
      return {inView: els.every(e => R(e).top >= 0 && R(e).bottom <= v), sw: document.documentElement.scrollWidth}; }""")
    close = page.query_selector('.maffs-calc-close')
    page.tap('.maffs-calc-close' if close and close.is_visible() else '.maffs-calc-toggle')
    closed = page.evaluate("() => document.querySelector('.maffs-calc-panel').hidden")
    if res != '2.5' or not fit['inView'] or fit['sw'] > 390 or not closed:
        rep[('calculator', '390x844')].append('2500 ÷ 1000 gave %r (2.5); prompt and options in view with it open: %s; '
                                              'page %d px wide (390); closed: %s' % (res, fit['inView'], fit['sw'],
                                                                                     closed))
    ctx.close()
    for w, h in ((1366, 768), (1920, 1080)):
        ctx = new_context(browser, (w, h))
        page, errors = open_page(ctx, base, src)
        page.evaluate("() => { level = 'gcse'; startGame(); }")
        page.click('.maffs-calc-toggle')
        if not page.evaluate("() => document.querySelector('.maffs-calc').classList.contains('docked')"):
            rep[('calculator', '%dx%d' % (w, h))].append('the calculator does not dock beside the card')
        ctx.close()


ALL = ('bank', 'display', 'lock', 'level', 'timer', 'phone')


def verify(src, only=ALL, verbose=False):
    """All checks on one copy of the page; {(finding, where): [messages]}, the item count, notes."""
    from playwright.sync_api import sync_playwright
    rep = defaultdict(list)
    n, notes = 0, []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = new_context(browser)
            page, errors = open_page(ctx, base, src)
            bank = read_bank(page)
            if 'bank' in only:
                n = check_bank(rep, bank, verbose)
                notes = report_notes(bank)
                check_served(rep, page, bank)
            if 'display' in only:
                n = check_display(rep, page, bank)
            if errors:
                rep[('page', 'errors')].append('; '.join(errors[:3]))
            ctx.close()
            if 'lock' in only:
                check_lock(rep, browser, base, src)
            if 'level' in only:
                check_level(rep, browser, base, src)
            if 'timer' in only:
                check_timer_and_score(rep, browser, base, src)
            if 'phone' in only:
                check_phone(rep, browser, base, src)
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return rep, n, notes


def show(rep):
    for (finding, where), msgs in sorted(rep.items()):
        for m in msgs:
            print('FAIL  %s  %s: %s' % (finding, where, m))


# One plant per finding: (label, finding id it must be reported under, checks to run, old text, planted text).
PLANTS = [
    ('t4-001: options locked by a CSS class only (no MaffsLock.lock)', 't4-001', ('lock',),
     "if(!MaffsLock.lock(document.getElementById('options')))return;", ''),
    ('t4-004: the cylinder\'s precision unstated', 't4-004', ('bank',),
     "Volume in cm³? Give your answer to 3 significant figures.',", "Volume in cm³?',"),
    ('t4-003: ?level read without validation', 't4-003', ('level',),
     "if(Object.prototype.hasOwnProperty.call(LEVELS,pa.get('level')||''))setLevel(pa.get('level'));",
     "if(pa.get('level'))setLevel(pa.get('level'));"),
    ('t4-005: a time-weighted score', 't4-005', ('timer',),
     "score+=PER_CORRECT;",
     "score+=Math.max(1,Math.round(PER_CORRECT/(1+0.15*Math.log(1+(Date.now()-(window.__qs||Date.now()))/1000))));"),
    ('t4-005: a visible clock in the HUD', 't4-005', ('timer',),
     "<div class=\"hud-item\"><div class=\"hud-label\">Correct</div>",
     "<div class=\"hud-item\"><div class=\"hud-label\">Time</div><div class=\"hud-val\" id=\"clk\">0</div></div>"
     "<script>setInterval(()=>{const e=document.getElementById('clk');if(e)e.textContent=+e.textContent+1},1000)</script>"
     "<div class=\"hud-item\"><div class=\"hud-label\">Correct</div>"),
    ('t4-006: no formatter (numbers shown as stored)', 't4-006', ('display',),
     "function fmt(s){return String(s).replace(", "function fmt(s){return String(s);String(s).replace("),
    ('marking: dataset.val set to the formatted text', 'marking', ('display',),
     "b.dataset.val=v;b.textContent=fmt(v);", "b.dataset.val=fmt(v);b.textContent=fmt(v);"),
    ('t4-006: "1 inch ≈ 2.54 cm" back', 't4-006', ('bank',),
     "(1 inch = 2.54 cm)", "(1 inch ≈ 2.54 cm)"),
    ('a wrong key (60 mph keyed 26.9 m/s)', 'key', ('bank',),
     "c:'26.8 m/s',d:['60 m/s'", "c:'26.9 m/s',d:['60 m/s'"),
    ('the calculator not mounted', 'calculator', ('phone',),
     "if(window.MaffsCalc)MaffsCalc.mount(", "if(false)MaffsCalc.mount("),
]
# the time-weighted plant needs each question's start time
PLANT_EXTRA = {'t4-005: a time-weighted score': ("document.getElementById('qNum').textContent=total;",
                                                 "window.__qs=Date.now();document.getElementById('qNum').textContent=total;")}


def selftest():
    src = open(GAME, encoding='utf-8').read()
    ok = True
    for label, finding, only, old, new in PLANTS:
        if src.count(old) != 1:
            print('  self-test %-58s *** the text to plant over is not in the page once ***' % label)
            ok = False
            continue
        planted = src.replace(old, new)
        if label in PLANT_EXTRA:
            a, b = PLANT_EXTRA[label]
            planted = planted.replace(a, b)
        rep, _, _ = verify(planted, only)
        hits = [m for (f, w), ms in rep.items() if f == finding for m in ms]
        ok = ok and bool(hits)
        print('  self-test %-58s %s' % (label, ('caught: ' + hits[0][:90]) if hits else '*** MISSED ***'))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()
    if args.selftest:
        ok = selftest()
        print('PASS' if ok else 'FAILED: a planted fault was not caught')
        return 0 if ok else 1
    src = open(args.against or GAME, encoding='utf-8').read()
    rep, n, notes = verify(src, verbose=args.verbose)
    print('%s: %d items; keys recomputed exactly, every option marked in Chromium; lock, level key, score, '
          'calculator' % (SLUG, n))
    for note in notes:
        print('NOTE  ' + note)
    show(rep)
    print('FAILED' if rep else 'PASS')
    return 1 if rep else 0


if __name__ == '__main__':
    sys.exit(main())
