#!/usr/bin/env python3
# ci-line: Decimal Detective (Line-Up and Round Up keys recomputed, Place It start state, every answer marked in Chromium) |
"""Decimal Detective: every key recomputed, and every answer marked through the real page.

The bank (45 items, one level: 15 Line-Up, 15 Round Up, 15 Place It) was keyed by hand and never
verified. The resit correctness audit of 4 Oct 2026 found a free mark (Place It's marker started on
the answer for 4.5 and 5.5, with Check enabled: F1), identical cards in three Line-Up rows (F7) and
two equal distractors in one Round Up question, 9.5 and 9.50 (F6).

The bank is read from the live page (post any runtime patch), then:
  Line-Up: the sorted row recomputed with Decimal and compared value by value; the sorted row is the
    suspects rearranged; no two cards in a row are the same string (Jon, 4 Oct 2026); two cards
    equal in value (0.77, 0.770) differ only by zeros on the end, which is what their feedback says.
  Round Up: every key recomputed half up with Decimal from the instruction (nearest tenth, whole
    number, N decimal places, 1 significant figure) and written as that rounding writes it; four
    options, the key among them exactly once, no two equal in value (SR-4) unless the question is
    in FORM_ASKS, whose ask names the form that tells them apart.
  Place It: the value lies on the line, on its half-tick grid (20 steps a line; a target off the grid
    could never be placed).
  Marking, in Chromium: every item is shown through the game's own loadQuestion().
    Line-Up: the recomputed order is marked right, and with any equal pair swapped; one wrong
      order (two unequal neighbours swapped) is marked wrong; a row with an equal pair shows the
      note naming both cards, right or wrong.
    Round Up: every option clicked; only the key is marked right.
    Place It (Jon's ruling on audit F4, 5 Oct 2026; canon 7.1.2): on load the marker is off the line
      and Check is disabled, so no item can score with no placement; pressing Check anyway marks
      nothing. Then, at 1000px with a mouse, a real click on every one of the 21 grid positions of
      every item: the marker must sit on that position, no value may be visible (the marker's label
      empty, and no number in the Place It area but the tick labels), and Check must say "Correct!"
      only when the position is the value, otherwise "You placed P. T is here." with both positions
      on the line; a right answer shows the value with the marker. The arrow keys move a placed
      marker one step (nothing before a placement, nothing past an end, nothing after Check).
    Phones, on a touch profile at 320x568, 375x667 and 390x844: the step buttons are at least 44px
      each way and below the line; for every item, one tap three steps from the value, then the step
      buttons, reach it with no value visible, and Check marks it right; after a right and after a
      wrong answer the feedback and Next are on screen, above the 40px footer.
    The session is never finished, so nothing is submitted; every request off the stub server is
    aborted.
A fault-injection self-test must FAIL each time: identical cards in a row and an equal-value
distractor (patched bank copies), a wrong Round Up key, and three patched pages served in place of
the file: the marker starting at 50% with Check enabled, a one-step tolerance in the marking, and a
live value readout on the marker. It runs unless --no-selftest. The file is never touched.

    python scripts/verify-decimal-detective.py [--verbose] [--no-selftest] [--chromium PATH]
"""
import argparse
import copy
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'decimal-detective'
COUNTS = {'LINEUP': 15, 'ROUNDUP': 15, 'PLACEIT': 15}
NOTE = "{0} and {1} are equal: a zero on the end doesn't change the value."

# Round Up questions whose ask names the form, so two options equal in value are told apart by it
# (SR-4). (value, instruction) -> reason.
FORM_ASKS = {
    ('7.895', 'Round to 2 decimal places'):
        '7.90 is the key and 7.9 its 1 d.p. form: "2 decimal places" names the form (audit F6 note)',
}

# Place It: every line has 10 tick gaps, and the marker snaps to half a gap.
STEPS = 20
PHONES = [(320, 568), (375, 667), (390, 844)]
FOOTER = 40

# The planted Place It faults, each a page served in place of the file: (fixed text, planted text).
PATCHES = {
    'start': ('until 5 Oct 2026.\n  markerPos = null;',                       # the pre-4 Oct start
              'until 5 Oct 2026.\n  markerPos = 0.5;'),
    'tolerance': ("const isCorrect = MaffsNumberLine.placementCorrect({ placed: placed, target: data.value, mode: 'snapped' });",
                  'const isCorrect = Math.abs(placed - data.value) <= (data.max - data.min) / 20 + 1e-9;'),
    'readout': ("  marker.style.display = '';\n  document.getElementById('checkBtn').disabled = false;\n  setStepButtons();",
                "  marker.style.display = '';\n  document.getElementById('checkBtn').disabled = false;\n  setStepButtons();\n"
                "  document.getElementById('markerValue').textContent = formatPlaceit(placeitValue(placeItData, markerPos));"),
}


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, where, what, detail):
        self.fails.append('%s %s: %s' % (where, what, detail))


def round_key(value, instruction):
    """The rounded value as that rounding writes it, or None for an instruction not understood."""
    v = D(value)
    if instruction == 'Round to the nearest tenth':
        return str(v.quantize(D('0.1'), ROUND_HALF_UP))
    if instruction == 'Round to the nearest whole number':
        return str(v.quantize(D('1'), ROUND_HALF_UP))
    m = re.fullmatch(r'Round to (\d+) decimal places?', instruction)
    if m:
        return str(v.quantize(D(1).scaleb(-int(m.group(1))), ROUND_HALF_UP))
    if instruction == 'Round to 1 significant figure':
        r = v.quantize(D(1).scaleb(v.adjusted()), ROUND_HALF_UP)
        return str(int(r)) if r == r.to_integral_value() else str(r)
    return None


def num(s):
    try:
        return D(s)
    except Exception:
        return None


def check_bank(rep, bank, verbose=False):
    for name, n in COUNTS.items():
        if len(bank.get(name, [])) != n:
            rep.fail(name, 'count', '%d items, expected %d (a change to the bank needs this verifier '
                     'updated)' % (len(bank.get(name, [])), n))

    for i, q in enumerate(bank.get('LINEUP', []), 1):
        where = 'Line-Up %d %s' % (i, q['suspects'])
        sus, srt = q['suspects'], q['sorted']
        if sorted(sus) != sorted(srt):
            rep.fail(where, 'sorted', 'the sorted row %s is not the suspects rearranged' % srt)
        want = sorted(D(s) for s in sus)
        if [D(s) for s in srt] != want:
            rep.fail(where, 'key', 'sorted row %s, recomputed %s' % (srt, [str(x) for x in want]))
        dups = sorted(set(s for s in sus if sus.count(s) > 1))
        if dups:
            rep.fail(where, 'identical', 'cards %s appear more than once in the row (Jon, 4 Oct 2026)' % dups)
        for a in sus:
            for b in sus:
                if a < b and D(a) == D(b) and a.rstrip('0') != b.rstrip('0'):
                    rep.fail(where, 'equal-value', '%s and %s are equal but not by a zero on the end; '
                             'the feedback would be wrong' % (a, b))
        if verbose:
            print('  %s -> %s' % (where, srt))

    for i, q in enumerate(bank.get('ROUNDUP', []), 1):
        where = 'Round Up %d %s, %s' % (i, q['value'], q['instruction'].lower())
        key, opts = q['answer'], q['options']
        want = round_key(q['value'], q['instruction'])
        if want is None:
            rep.fail(where, 'unread', 'instruction %r not understood: extend round_key()' % q['instruction'])
        elif key != want:
            rep.fail(where, 'key', 'keyed %s, recomputed half up %s' % (key, want))
        if len(opts) != 4:
            rep.fail(where, 'options', '%d options, SR-4 wants four: %s' % (len(opts), opts))
        if opts.count(key) != 1:
            rep.fail(where, 'options', 'the key %s appears %d times in %s' % (key, opts.count(key), opts))
        if len(set(opts)) != len(opts):
            rep.fail(where, 'options', 'an option is repeated: %s' % opts)
        vals = {}
        for o in opts:
            v = num(o)
            if v is None:
                rep.fail(where, 'options', 'option %r is not a number' % o)
                continue
            if v in vals and vals[v] != o and (q['value'], q['instruction']) not in FORM_ASKS:
                rep.fail(where, 'value-equal', '%r and %r are equal in value (SR-4)' % (vals[v], o))
            vals.setdefault(v, o)
        if verbose:
            print('  %s: key %s, recomputed %s, options %s' % (where, key, want, opts))
    for value, instr in FORM_ASKS:
        if not any(q['value'] == value and q['instruction'] == instr for q in bank.get('ROUNDUP', [])):
            rep.fail('FORM_ASKS', 'stale', '(%s, %s) matches no question: re-read it' % (value, instr))

    for i, q in enumerate(bank.get('PLACEIT', []), 1):
        if not D(str(q['min'])) <= D(str(q['value'])) <= D(str(q['max'])):
            rep.fail('Place It %d' % i, 'range', '%s is not on the line %s to %s' % (q['value'], q['min'], q['max']))
        elif grid_index(q) is None:
            rep.fail('Place It %d' % i, 'grid', '%s is not on the half-tick grid of %s to %s (steps of %s): '
                     'it could never be placed' % (q['value'], q['min'], q['max'], fmt(step_of(q))))


def step_of(q):
    return (F(str(q['max'])) - F(str(q['min']))) / STEPS


def grid_value(q, k):
    return F(str(q['min'])) + k * step_of(q)


def grid_index(q):
    """The value's grid position (0..20), or None when it is off the grid."""
    k = (F(str(q['value'])) - F(str(q['min']))) / step_of(q)
    return int(k) if k.denominator == 1 else None


def fmt(x):
    """A value as the game writes it (formatPlaceit: no trailing zeros)."""
    d = D(x.numerator) / D(x.denominator)
    t = format(d.normalize(), 'f')
    return t


# ---------------------------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------------------------
JS_LOAD = '''([type, data]) => { questions = [{type, data}]; currentQ = 0; answered = false; loadQuestion(); }'''
JS_ORDER = '''(order) => {
  const zone = document.getElementById('lineupZone');
  const cards = [...zone.querySelectorAll('.suspect-card')];
  for (const s of order) zone.appendChild(cards.splice(cards.findIndex(c => c.dataset.display === s), 1)[0]);
}'''
JS_FEEDBACK = '''() => { const f = document.getElementById('feedback');
  return f.style.display === 'none' ? null : f.textContent.trim(); }'''
# The marker's place and every number the student can see in the Place It area (the tick labels and,
# if any, a value label).
JS_PLACE = '''() => { const mv = document.getElementById('markerValue'), box = document.getElementById('placeItBox');
  const shown = mv && getComputedStyle(mv).display !== 'none' && mv.offsetParent !== null ? mv.textContent.trim() : '';
  return {pos: markerPos, k: markerPos === null ? null : Math.round(markerPos * 20),
          label: shown, numbers: (box.innerText.match(/\\d+(?:\\.\\d+)?/g) || []),
          ticks: [...box.querySelectorAll('.tick-label')].map(t => t.textContent.trim()),
          checkDisabled: document.getElementById('checkBtn').disabled}; }'''
JS_X = '''(k) => { const l = document.getElementById('numberLine').getBoundingClientRect();
  return [l.left + k / 20 * l.width, l.top + l.height / 2]; }'''
JS_FOLD = '''() => { const r = id => document.getElementById(id).getBoundingClientRect();
  return {fbTop: r('feedback').top, fbBottom: r('feedback').bottom, nextTop: r('nextBtn').top,
          nextBottom: r('nextBtn').bottom, nextShown: getComputedStyle(document.getElementById('nextBtn')).display !== 'none',
          fold: innerHeight - 40}; }'''


def verdict(text):
    if text is None:
        return None
    return 'right' if text.startswith('Correct') else 'wrong' if text.startswith('Not quite') else text


def open_page(pw, base, chromium, viewport, touch, patch):
    page_url = base + '/games/' + SLUG + '/'
    browser = pw.chromium.launch(**({'executable_path': chromium} if chromium else {}))
    ctx = browser.new_context(viewport={'width': viewport[0], 'height': viewport[1]},
                              has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))

    def route(r):
        url = r.request.url
        if not url.startswith(base):
            return r.abort()
        if patch and url.split('?')[0] == page_url:
            fixed, planted = PATCHES[patch]
            with open(os.path.join(HERE, '..', 'games', SLUG, 'index.html'), encoding='utf-8') as f:
                html = f.read()
            assert html.count(fixed) == 1, 'self-test patch out of date: %r' % fixed
            return r.fulfill(status=200, content_type='text/html', body=html.replace(fixed, planted))
        return r.continue_()
    page.route('**/*', route)
    page.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)  # FONT-FIT: KaTeX and the text faces from scripts/fonts/, the fonts students see
    page.goto(page_url + '?cb=verify', wait_until='load', timeout=20000)
    page.wait_for_function('typeof PLACEIT_QUESTIONS !== "undefined" && window.MaffsNumberLine', timeout=8000)
    page.evaluate('startGame()')
    return browser, page, errors


def no_value_shown(rep, where, st):
    """Before Check: no value on the marker, and no number in the Place It area but the tick labels."""
    if st['label']:
        rep.fail(where, 'readout', 'the marker shows %r before Check' % st['label'])
    extra = [n for n in st['numbers'] if n not in st['ticks']]
    if extra:
        rep.fail(where, 'readout', 'numbers other than the tick labels are visible before Check: %s' % extra)


def start_state(rep, page, q, where):
    page.evaluate(JS_LOAD, ['placeit', q])
    st = page.evaluate('''() => ({pos: markerPos,
      shown: getComputedStyle(document.getElementById('lineMarker')).display !== 'none',
      disabled: document.getElementById('checkBtn').disabled})''')
    if st['shown'] or st['pos'] is not None:
        rep.fail(where, 'start', 'the marker starts on the line (at %s of it)' % st['pos'])
    if not st['disabled']:
        rep.fail(where, 'start', 'Check is enabled before the student has placed the marker')
    page.evaluate('checkAnswer()')
    if page.evaluate(JS_FEEDBACK) is not None:
        rep.fail(where, 'start', 'Check with no placement marks the question: %r' % page.evaluate(JS_FEEDBACK))


def desktop_placeit(rep, page, items):
    """Every grid position of every item, a real click, then Check. Returns the number of clicks."""
    clicks = 0
    for i, q in enumerate(items, 1):
        where = 'Place It %d (%s on %s to %s)' % (i, q['value'], q['min'], q['max'])
        start_state(rep, page, q, where)
        target = F(str(q['value']))
        for k in range(STEPS + 1):
            v = grid_value(q, k)
            page.evaluate(JS_LOAD, ['placeit', q])
            x, y = page.evaluate(JS_X, k)
            page.mouse.click(x, y)
            st = page.evaluate(JS_PLACE)
            if st['k'] != k:
                rep.fail(where, 'tap', 'a click on %s placed the marker at step %s, not %d' % (fmt(v), st['k'], k))
                continue
            no_value_shown(rep, where + ' at ' + fmt(v), st)
            if st['checkDisabled']:
                rep.fail(where, 'placing', 'Check is still disabled after the marker is placed')
                continue
            page.click('#checkBtn')
            clicks += 1
            text = page.evaluate(JS_FEEDBACK) or ''
            after = page.evaluate(JS_PLACE)
            ring = page.evaluate("getComputedStyle(document.getElementById('targetMarker')).display !== 'none'")
            if v == target:
                if verdict(text) != 'right':
                    rep.fail(where, 'marking', 'the marker on the value shows %r' % text)
                elif after['label'] != fmt(target):
                    rep.fail(where, 'after Check', 'a right answer shows %r with the marker, not %s'
                             % (after['label'], fmt(target)))
            else:
                want = 'You placed %s. %s is here.' % (fmt(v), fmt(target))
                if verdict(text) != 'wrong':
                    rep.fail(where, 'marking', 'the marker on %s shows %r: only the value may be marked right'
                             % (fmt(v), text))
                elif want not in text:
                    rep.fail(where, 'feedback', 'the marker on %s shows %r, without %r' % (fmt(v), text, want))
                if not ring:
                    rep.fail(where, 'after Check', 'the value\'s position is not shown on the line')
    return clicks


def keys_placeit(rep, page, q):
    page.evaluate(JS_LOAD, ['placeit', q])
    page.keyboard.press('ArrowRight')
    if page.evaluate('markerPos') is not None:
        rep.fail('arrow keys', 'before placing', 'ArrowRight placed a marker before the student did')
    for k, key, want in ((0, 'ArrowRight', 1), (5, 'ArrowLeft', 4), (0, 'ArrowLeft', 0), (STEPS, 'ArrowRight', STEPS)):
        page.evaluate(JS_LOAD, ['placeit', q])
        page.mouse.click(*page.evaluate(JS_X, k))
        page.keyboard.press(key)
        got = page.evaluate(JS_PLACE)['k']
        if got != want:
            rep.fail('arrow keys', key, 'from step %d gave step %s, expected %d' % (k, got, want))
    page.evaluate(JS_LOAD, ['placeit', q])
    page.mouse.click(*page.evaluate(JS_X, 3))
    page.click('#checkBtn')
    page.keyboard.press('ArrowRight')
    if page.evaluate(JS_PLACE)['k'] != 3:
        rep.fail('arrow keys', 'after answering', 'ArrowRight moved the marker after Check')


def tap_line(page, k):
    """A real tap on grid position k, relative to the line (Playwright scrolls it into view first)."""
    box = page.locator('#numberLine').bounding_box()
    page.locator('#numberLine').tap(position={'x': k / STEPS * box['width'], 'y': box['height'] / 2}, force=True)


def phone_placeit(rep, page, items, size, verbose):
    """Layout at one phone size; every item reached with one tap and the step buttons; the fold."""
    tag = '%dx%d' % size
    page.evaluate(JS_LOAD, ['placeit', items[0]])
    page.evaluate('window.scrollTo(0, 0)')
    tap_line(page, 0)
    page.evaluate('window.scrollTo(0, 0)')
    m = page.evaluate('''() => { const r = id => { const b = document.getElementById(id).getBoundingClientRect();
        return {t: b.top, b: b.bottom, w: b.width, h: b.height}; };
      return {line: r('numberLine'), wrap: document.querySelector('.number-line-wrap').getBoundingClientRect().bottom,
              left: r('stepLeft'), right: r('stepRight'), check: r('checkBtn'), fold: innerHeight - 40}; }''')
    if m['check']['b'] > m['fold']:
        rep.fail(tag, 'fold', 'with a marker placed, Check ends at %.0f, under the footer (%.0f)' % (m['check']['b'], m['fold']))
    for side in ('left', 'right'):
        b = m[side]
        if b['w'] < 44 or b['h'] < 44:
            rep.fail(tag, 'step button', 'the %s button is %.0fx%.0fpx, under 44px' % (side, b['w'], b['h']))
        if b['t'] < m['wrap']:
            rep.fail(tag, 'step button', 'the %s button overlaps the number line (top %.0f, line box ends %.0f)'
                     % (side, b['t'], m['wrap']))
    print('  %s: grid step %.1fpx; step buttons %.0fx%.0fpx, %.0fpx below the line box; Check ends %.0f, fold %.0f'
          % (tag, m['line']['w'] / STEPS, m['left']['w'], m['left']['h'], m['left']['t'] - m['wrap'],
             m['check']['b'], m['fold']))

    presses, worst, fold = 0, None, m['fold']
    for i, q in enumerate(items, 1):
        where = '%s Place It %d (%s on %s to %s)' % (tag, i, q['value'], q['min'], q['max'])
        kt = grid_index(q)
        for right in (True, False):
            page.evaluate(JS_LOAD, ['placeit', q])
            page.evaluate('window.scrollTo(0, 0)')
            k0 = kt + 3 if kt + 3 <= STEPS else kt - 3
            tap_line(page, k0)
            st = page.evaluate(JS_PLACE)
            if st['k'] is None:
                rep.fail(where, 'tap', 'a tap on the line placed no marker')
                break
            goal = kt if right else (kt - 1 if kt > 0 else kt + 1)
            for _ in range(STEPS + 5):
                if st['k'] == goal:
                    break
                page.tap('#stepRight' if st['k'] < goal else '#stepLeft')
                presses += 1
                st = page.evaluate(JS_PLACE)
                no_value_shown(rep, where, st)
            if st['k'] != goal:
                rep.fail(where, 'reach', 'the step buttons did not reach step %d (stuck at %s)' % (goal, st['k']))
                break
            page.tap('#checkBtn')
            text = page.evaluate(JS_FEEDBACK)
            if verdict(text) != ('right' if right else 'wrong'):
                rep.fail(where, 'marking', 'reached step %d with the step buttons, Check shows %r' % (goal, text))
            f = page.evaluate(JS_FOLD)
            if not f['nextShown'] or f['nextTop'] < 0 or f['nextBottom'] > f['fold'] or f['fbTop'] < 0:
                rep.fail(where, 'fold', 'after a %s answer the feedback (%.0f-%.0f) and Next (%.0f-%.0f) are not '
                         'both on screen above the footer (%.0f)' % ('right' if right else 'wrong', f['fbTop'],
                         f['fbBottom'], f['nextTop'], f['nextBottom'], f['fold']))
            worst = max(worst or 0, f['nextBottom'])
    print('  %s: %d items reached right and wrong, %d step-button taps; Next ends by %.0f, fold %.0f '
          '(innerHeight - %dpx footer)' % (tag, len(items), presses, worst or 0, fold, FOOTER))


def run_page(rep, chromium=None, verbose=False, patch=None):
    """Read the bank, then mark every item through the page. Returns (bank, actions).
    A self-test run (patch) does the desktop Place It pass only."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser, page, errors = open_page(pw, base, chromium, (1000, 900), False, patch)
            bank = page.evaluate('JSON.parse(JSON.stringify({LINEUP: LINEUP_QUESTIONS, '
                                 'ROUNDUP: ROUNDUP_QUESTIONS, PLACEIT: PLACEIT_QUESTIONS}))')
            actions = 0
            if patch:
                actions += desktop_placeit(rep, page, bank['PLACEIT'])
                browser.close()
                return bank, actions

            for i, q in enumerate(bank['LINEUP'], 1):
                where = 'Line-Up %d' % i
                right = sorted(q['suspects'], key=D)
                orders = [(right, 'right')]
                for a in range(4):
                    if D(right[a]) == D(right[a + 1]):
                        swapped = right[:a] + [right[a + 1], right[a]] + right[a + 2:]
                        orders.append((swapped, 'right'))
                a = next(a for a in range(4) if D(right[a]) != D(right[a + 1]))
                orders.append((right[:a] + [right[a + 1], right[a]] + right[a + 2:], 'wrong'))
                notes = [NOTE.format(*sorted((x, y), key=len)) for k, x in enumerate(q['suspects'])
                         for y in q['suspects'][k + 1:] if x != y and D(x) == D(y)]
                for order, want in orders:
                    page.evaluate(JS_LOAD, ['lineup', q])
                    page.evaluate(JS_ORDER, order)
                    page.click('#checkBtn')
                    text = page.evaluate(JS_FEEDBACK)
                    actions += 1
                    if verdict(text) != want:
                        rep.fail(where, 'marking', 'order %s shows %r, expected %s' % (order, text, want))
                    for n in notes:
                        if n not in (text or ''):
                            rep.fail(where, 'feedback', 'order %s: the note %r is not shown' % (order, n))

            for i, q in enumerate(bank['ROUNDUP'], 1):
                where = 'Round Up %d (%s)' % (i, q['value'])
                for opt in q['options']:
                    page.evaluate(JS_LOAD, ['roundup', q])
                    page.click('.option-btn[data-option="%s"]' % opt)
                    page.click('#checkBtn')
                    text = page.evaluate(JS_FEEDBACK)
                    actions += 1
                    want = 'right' if opt == q['answer'] else 'wrong'
                    if verdict(text) != want:
                        rep.fail(where, 'marking', 'option %s shows %r, expected %s' % (opt, text, want))

            placeable = [q for q in bank['PLACEIT'] if grid_index(q) is not None]
            actions += desktop_placeit(rep, page, placeable)
            keys_placeit(rep, page, placeable[0])
            if page.evaluate('window._mfgCompleted === true'):
                rep.fail('page', 'session', 'the session reached its end screen; it must not (nothing may submit)')
            browser.close()
            for size in PHONES:
                browser, page, errs = open_page(pw, base, chromium, size, True, None)
                phone_placeit(rep, page, placeable, size, verbose)
                browser.close()
                errors += errs
            for e in errors:
                rep.fail('page', 'error', e)
            if verbose:
                print('  %d answers marked in Chromium' % actions)
            return bank, actions
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank, chromium):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank)

    def record(name, rep):
        nonlocal ok
        new = [f for f in rep.fails if f not in base.fails]
        ok = ok and bool(new)
        lines.append('  self-test %-44s %s' % (name, ('caught: ' + new[0][:100]) if new else '*** MISSED ***'))

    def expect(name, fn):
        b = copy.deepcopy(bank)
        fn(b)
        rep = Report()
        check_bank(rep, b)
        record(name, rep)

    def find(items, field, text):
        return next(q for q in items if q[field] == text)

    def identical(b):                                                           # the audit's F7
        q = next(q for q in b['LINEUP'] if '1.909' in q['suspects'])
        q['suspects'] = ['1.9' if s == '1.909' else s for s in q['suspects']]
        q['sorted'] = ['1.9' if s == '1.909' else s for s in q['sorted']]
    expect('identical cards in a row (1.9, 1.9)', identical)

    def value_equal(b):                                                         # the audit's F6
        find(b['ROUNDUP'], 'value', '9.50')['options'] = ['9', '10', '9.5', '9.50']
    expect('equal-value distractors (9.5, 9.50)', value_equal)

    def wrong_key(b):                                                           # double rounding
        q = find(b['ROUNDUP'], 'value', '3.45')
        q['answer'], q['options'] = '4', ['3', '4', '3.5', '3.45']
    expect('wrong Round Up key (3.45 -> 4)', wrong_key)

    def off_grid(b):                                                            # a target that cannot be placed
        b['PLACEIT'][0]['value'] = 0.33
    expect('Place It target off the half-tick grid (0.33)', off_grid)

    for patch, name in (('start', 'Place It marker at 50%, Check enabled (page)'),        # the audit's F1
                        ('tolerance', 'Place It one-step tolerance (page)'),               # F2, F3
                        ('readout', 'Place It live value readout (page)')):                # F4
        rep = Report()
        run_page(rep, chromium, patch=patch)
        record(name, rep)
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--chromium', help='Chromium executable (a cloud sandbox: /opt/pw-browsers/chromium)')
    args = ap.parse_args()

    rep = Report()
    bank, actions = run_page(rep, args.chromium, args.verbose)
    check_bank(rep, bank, args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, args.chromium)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    print('\n%s: %d FAIL(s); %d items (Line-Up and Round Up keys recomputed with Decimal), '
          '%d answers marked in Chromium'
          % ('PASS' if ok else 'FAILED', len(rep.fails), sum(len(v) for v in bank.values()), actions))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
