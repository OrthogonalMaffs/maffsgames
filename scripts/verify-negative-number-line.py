#!/usr/bin/env python3
# ci-line: Negative Number Line (keys recomputed, every placement marked by real taps, every target reached on three phones) |
"""Negative Number Line: every key recomputed, Place It marked by exact match through real taps,
and every target reachable on a phone.

The bank (45 items: 15 Place It, 15 Order Them, 15 Calculate) was keyed by hand and never verified.
The resit correctness audit of 4 Oct 2026 found Place It accepting anything within 0.5 of the target
on a line that snaps to 0.5 and labels the marker: 0 and 1 marked right for 0.5, -2.5 for -3 (F1,
F2). PR #36 made the match exact; at 390px wide a 0.5 step is then 7.4px, too small to hit with a
finger, so (Jon, 5 Oct 2026) the placed marker also moves by 0.5 with step buttons and the arrow
keys, and the marking rule lives in the shared helper schools/assets/number-line.js
(MaffsNumberLine, canon 7.1.2).

The bank is read from the live page, then:
  Place It: targets distinct, on the line, on the 0.5 grid (a target off the grid can never be
    placed).
  Order Them: four distinct numbers on the line; the key is them sorted (Fraction).
  Calculate: the key is start + val or start - val; start and key on the line. (Distractors that
    lie off the line are logged LOW in the audit and not checked here.)
  The helper, in the page: snapped placements match exactly (0.1 + 0.2 counts as 0.3; 0 and 1 do
    not count as 0.5; nothing placed is false); any other mode ('continuous') throws "must snap (canon
    §7.1.2)": the mode was removed on Jon's ruling on audit DD F4 (5 Oct 2026).
  Marking, in Chromium at 1000px with a mouse: for every target, a real click on every one of the
    41 positions on the line; the marker must read that position, and Confirm must say "Correct!"
    only when it is the target, otherwise "You placed P; T is here." The arrow keys move a placed
    marker by 0.5 (and nothing before a placement, nor past an end).
  Phones, in Chromium on a touch profile at 320x568, 375x667 and 390x844: the step buttons are at
    least 44px each way and below the line; the marker's value is shown above the line, at least
    16px; Confirm, and after a wrong answer the feedback and Next, end above the fold (canon 7.6.1); for every target, one tap 1.5 units away and then the step buttons reach the target, and
    Confirm marks it right.
  The session is never finished, so nothing is submitted; every request off the stub server is
  aborted.
A fault-injection self-test must FAIL each time: a 0.5 tolerance planted in the helper (a patched
number-line.js served in place of the file, so a game marking anywhere else would not be caught),
and wrong Calculate and Order Them keys (patched copies of the bank). It runs unless --no-selftest.
No file is touched.

    python scripts/verify-negative-number-line.py [--verbose] [--no-selftest] [--chromium PATH]
"""
import argparse
import copy
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'negative-number-line'
COUNTS = {'PLACE': 15, 'ORDER': 15, 'CALC': 15}
LO, HI = -10, 10
POSITIONS = [F(k, 2) for k in range(2 * LO, 2 * HI + 1)]
PHONES = [(320, 568), (375, 667), (390, 844)]
HELPER = 'schools/assets/number-line.js'
EXACT_RULE = 'return Math.abs(opts.placed - opts.target) < EPS;'
PLANTED_RULE = 'return Math.abs(opts.placed - opts.target) <= 0.5;'


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, where, what, detail):
        self.fails.append('%s %s: %s' % (where, what, detail))


def fmt(v):
    """The game's formatNum(): an integer as itself, otherwise to 1 d.p."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else '%.1f' % float(v)


def check_bank(rep, bank, verbose=False):
    for name, n in COUNTS.items():
        if len(bank.get(name, [])) != n:
            rep.fail(name, 'count', '%d items, expected %d (a change to the bank needs this verifier '
                     'updated)' % (len(bank.get(name, [])), n))
    place = [F(str(t)) for t in bank.get('PLACE', [])]
    if len(set(place)) != len(place):
        rep.fail('Place It', 'targets', 'a target is repeated: %s' % [fmt(t) for t in place])
    for t in place:
        if not LO <= t <= HI or (2 * t).denominator != 1:
            rep.fail('Place It %s' % fmt(t), 'target', 'not one of the line\'s positions (%d to %d in 0.5s)' % (LO, HI))
    for i, q in enumerate(bank.get('ORDER', []), 1):
        nums = [F(str(x)) for x in q['nums']]
        where = 'Order Them %d %s' % (i, [fmt(x) for x in nums])
        if len(nums) != 4 or len(set(nums)) != 4:
            rep.fail(where, 'numbers', 'not four distinct numbers')
        if any(not LO <= x <= HI for x in nums):
            rep.fail(where, 'numbers', 'a number is off the line')
        if [F(str(x)) for x in q['answer']] != sorted(nums):
            rep.fail(where, 'key', 'keyed %s, sorted %s' % (q['answer'], [fmt(x) for x in sorted(nums)]))
    for i, q in enumerate(bank.get('CALC', []), 1):
        where = 'Calculate %d (%s %s %s)' % (i, q['start'], q['op'], q['val'])
        if q['op'] not in ('add', 'subtract'):
            rep.fail(where, 'op', 'unknown operation %r' % q['op'])
            continue
        want = F(str(q['start'])) + (1 if q['op'] == 'add' else -1) * F(str(q['val']))
        if F(str(q['answer'])) != want:
            rep.fail(where, 'key', 'keyed %s, recomputed %s' % (q['answer'], fmt(want)))
        if not (LO <= F(str(q['start'])) <= HI and LO <= want <= HI):
            rep.fail(where, 'line', 'the start or the answer is off the line')
        if verbose:
            print('  %s = %s' % (where, fmt(want)))


# ---------------------------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------------------------
JS_LOAD = '''(t) => { questions = [{type: 'place', data: t}]; qIndex = 0; showQuestion(); }'''
JS_X = '''(v) => { const s = document.getElementById('placeNL').getBoundingClientRect();
  return [s.left + valueToX(v) / 680 * s.width, s.top + s.height / 2]; }'''
JS_STATE = '''() => ({placed: placedValue,
  readout: (document.querySelector('#placeReadout b') || {}).textContent || null,
  feedback: document.getElementById('feedbackBar').textContent.trim()})'''
JS_HELPER = '''() => {
  const pc = (p, t) => MaffsNumberLine.placementCorrect({placed: p, target: t, mode: 'snapped'});
  const out = {cases: [[0.5, 0.5, pc(0.5, 0.5)], [0, 0.5, pc(0, 0.5)], [1, 0.5, pc(1, 0.5)],
    [-2.5, -3, pc(-2.5, -3)], [0.1 + 0.2, 0.3, pc(0.1 + 0.2, 0.3)], [null, 0.5, pc(null, 0.5)]]};
  try { MaffsNumberLine.placementCorrect({placed: 0.5, target: 0.5, mode: 'continuous'}); out.cont = 'no throw'; }
  catch (e) { out.cont = e.message; }
  return out; }'''
HELPER_WANT = [True, False, False, False, True, False]


def open_page(pw, base, chromium, viewport, touch, patched_helper):
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
        if patched_helper and url.split('?')[0].endswith('/' + HELPER):
            with open(os.path.join(HERE, '..', HELPER), encoding='utf-8') as f:
                js = f.read()
            assert js.count(EXACT_RULE) == 1, 'self-test patch out of date: %r' % EXACT_RULE
            return r.fulfill(status=200, content_type='application/javascript', body=js.replace(EXACT_RULE, PLANTED_RULE))
        return r.continue_()
    page.route('**/*', route)
    page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
    page.wait_for_function('typeof PLACE_QUESTIONS !== "undefined" && window.MaffsNumberLine', timeout=8000)
    page.evaluate('startGame()')
    return browser, page, errors


def desktop_pass(rep, page, targets, verbose):
    """Every target, a real click on every position, then Confirm. Returns the number of clicks."""
    clicks = 0
    for t in targets:
        tf = F(str(t))
        for v in POSITIONS:
            page.evaluate(JS_LOAD, t)
            x, y = page.evaluate(JS_X, float(v))
            page.mouse.click(x, y)
            page.click('#placeConfirm')
            st = page.evaluate(JS_STATE)
            clicks += 1
            where = 'Place It %s' % fmt(tf)
            if st['placed'] is None or F(str(st['placed'])) != v or st['readout'] != fmt(v):
                rep.fail(where, 'tap', 'a click on %s placed %s (reads %s)' % (fmt(v), st['placed'], st['readout']))
                continue
            want = 'Correct!' if v == tf else 'You placed %s; %s is here.' % (fmt(v), fmt(tf))
            if st['feedback'] != want:
                rep.fail(where, 'marking', 'the marker on %s shows %r, expected %r' % (fmt(v), st['feedback'], want))
    if verbose:
        print('  %d clicks marked at 1000px' % clicks)
    return clicks


def keys_pass(rep, page):
    page.evaluate(JS_LOAD, -3)
    page.keyboard.press('ArrowRight')
    if page.evaluate('placedValue') is not None:
        rep.fail('arrow keys', 'before placing', 'ArrowRight placed a marker before the student did')
    for start, key, want in ((0, 'ArrowRight', 0.5), (0, 'ArrowLeft', -0.5), (10, 'ArrowRight', 10), (-10, 'ArrowLeft', -10)):
        page.evaluate(JS_LOAD, -3)
        x, y = page.evaluate(JS_X, start)
        page.mouse.click(x, y)
        page.keyboard.press(key)
        got = page.evaluate('placedValue')
        if got != want:
            rep.fail('arrow keys', key, 'from %s gave %s, expected %s' % (start, got, want))
    page.evaluate(JS_LOAD, -3)
    x, y = page.evaluate(JS_X, -3)
    page.mouse.click(x, y)
    page.click('#placeConfirm')
    page.keyboard.press('ArrowRight')
    if page.evaluate('placedValue') != -3:
        rep.fail('arrow keys', 'after answering', 'ArrowRight moved the marker after Confirm')


def phone_pass(rep, page, targets, size, verbose):
    """Layout at one phone size, then every target reached with one tap and the step buttons."""
    tag = '%dx%d' % size
    page.evaluate(JS_LOAD, targets[0])
    x, y = page.evaluate(JS_X, 0)
    page.touchscreen.tap(x, y)
    m = page.evaluate('''() => {
      const r = id => { const b = document.getElementById(id).getBoundingClientRect();
                        return {l: b.left, r: b.right, t: b.top, b: b.bottom, w: b.width, h: b.height}; };
      const val = document.querySelector('#placeReadout b');
      return {line: r('placeNL'), wrap: r('placeNLWrap'), left: r('stepLeft'), right: r('stepRight'),
              readout: r('placeReadout'), confirm: r('placeConfirm'),
              font: val ? parseFloat(getComputedStyle(val).fontSize) : 0,
              step: document.getElementById('placeNL').getBoundingClientRect().width * 620 / 680 / 40,
              vh: innerHeight}; }''')
    for side in ('left', 'right'):
        b = m[side]
        if b['w'] < 44 or b['h'] < 44:
            rep.fail(tag, 'step button', 'the %s button is %.0fx%.0fpx, under 44px' % (side, b['w'], b['h']))
        if b['t'] < m['wrap']['b']:
            rep.fail(tag, 'step button', 'the %s button overlaps the number line (top %.0f, line box ends %.0f)'
                     % (side, b['t'], m['wrap']['b']))
    if m['readout']['b'] > m['line']['t']:
        rep.fail(tag, 'readout', 'the marker value is not above the line (bottom %.0f, line top %.0f)'
                 % (m['readout']['b'], m['line']['t']))
    if m['font'] < 16:
        rep.fail(tag, 'readout', 'the marker value is %.1fpx, under 16px' % m['font'])
    if m['confirm']['b'] > m['vh'] - 40:
        rep.fail(tag, 'fold', 'with a marker placed, Confirm ends at %.0f, below the fold %.0f'
                 % (m['confirm']['b'], m['vh'] - 40))
    print('  %s: snap step %.1fpx; step buttons %.0fx%.0fpx, %.0fpx below the line box; value %.0fpx, '
          '%.0fpx above the line; Confirm bottom %.0f of %d' % (tag, m['step'], m['left']['w'], m['left']['h'],
          m['left']['t'] - m['wrap']['b'], m['font'], m['line']['t'] - m['readout']['b'], m['confirm']['b'], m['vh']))

    # Canon 7.6.1: after a wrong answer the reason and Next sit above the fold (the 40px footer is fixed).
    page.evaluate(JS_LOAD, targets[0])
    x, y = page.evaluate(JS_X, float(F(str(targets[0])) + (1 if targets[0] < HI else -1)))
    page.touchscreen.tap(x, y)
    page.tap('#placeConfirm')
    fold = page.evaluate('''() => ({fb: document.getElementById('feedbackBar').getBoundingClientRect().bottom,
      next: document.getElementById('nextBtn').getBoundingClientRect().bottom, fold: innerHeight - 40})''')
    for name in ('fb', 'next'):
        if fold[name] > fold['fold']:
            rep.fail(tag, 'fold', 'after a wrong answer the %s ends at %.0f, below the fold %.0f (canon 7.6.1)'
                     % ('feedback' if name == 'fb' else 'Next button', fold[name], fold['fold']))
    print('  %s: after a wrong answer, feedback ends %.0f and Next %.0f; fold %.0f'
          % (tag, fold['fb'], fold['next'], fold['fold']))

    presses = 0
    for t in targets:
        tf = F(str(t))
        where = '%s Place It %s' % (tag, fmt(tf))
        page.evaluate(JS_LOAD, t)
        off = tf + (F(3, 2) if tf + F(3, 2) <= HI else F(-3, 2))
        x, y = page.evaluate(JS_X, float(off))
        page.touchscreen.tap(x, y)
        st = page.evaluate(JS_STATE)
        if st['placed'] is None:
            rep.fail(where, 'tap', 'a tap on the line placed no marker')
            continue
        for _ in range(40):
            cur = F(str(st['placed']))
            if cur == tf:
                break
            page.tap('#stepRight' if cur < tf else '#stepLeft')
            presses += 1
            st = page.evaluate(JS_STATE)
            if st['readout'] != fmt(F(str(st['placed']))):
                rep.fail(where, 'readout', 'the value shown %s is not the marker %s' % (st['readout'], st['placed']))
        if F(str(st['placed'])) != tf:
            rep.fail(where, 'reach', 'the step buttons did not reach the target (stuck at %s)' % st['placed'])
            continue
        page.tap('#placeConfirm')
        fb = page.evaluate(JS_STATE)['feedback']
        if fb != 'Correct!':
            rep.fail(where, 'marking', 'reached with the step buttons, Confirm shows %r' % fb)
    if verbose:
        print('  %s: %d targets reached, %d step-button taps' % (tag, len(targets), presses))


def run_page(rep, chromium=None, verbose=False, patched_helper=False):
    """Returns (bank, clicks). The self-test run (patched_helper) does the desktop marking only."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser, page, errors = open_page(pw, base, chromium, (1000, 900), False, patched_helper)
            bank = page.evaluate('JSON.parse(JSON.stringify({PLACE: PLACE_QUESTIONS, ORDER: ORDER_QUESTIONS, '
                                 'CALC: CALC_QUESTIONS}))')
            if not patched_helper:
                h = page.evaluate(JS_HELPER)
                for (p, t, got), want in zip(h['cases'], HELPER_WANT):
                    if got is not want:
                        rep.fail('MaffsNumberLine', 'snapped', 'placed %s, target %s gave %s, expected %s' % (p, t, got, want))
                if 'must snap (canon §7.1.2)' not in h['cont']:
                    rep.fail('MaffsNumberLine', 'continuous', 'expected a throw "must snap (canon §7.1.2)", got %r' % h['cont'])
            clicks = desktop_pass(rep, page, bank['PLACE'], verbose)
            if not patched_helper:
                keys_pass(rep, page)
            browser.close()
            if not patched_helper:
                for size in PHONES:
                    browser, page, errs = open_page(pw, base, chromium, size, True, False)
                    phone_pass(rep, page, bank['PLACE'], size, verbose)
                    browser.close()
                    errors += errs
            for e in errors:
                rep.fail('page', 'error', e)
            return bank, clicks
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank, chromium):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank)

    def record(name, rep, baseline):
        nonlocal ok
        new = [f for f in rep.fails if f not in baseline]
        ok = ok and bool(new)
        lines.append('  self-test %-42s %s' % (name, ('caught: ' + new[0][:100]) if new else '*** MISSED ***'))

    def expect(name, fn):
        b = copy.deepcopy(bank)
        fn(b)
        rep = Report()
        check_bank(rep, b)
        record(name, rep, base.fails)

    def calc_key(b):
        b['CALC'][0]['answer'] += 1
    expect('wrong Calculate key (first item + 1)', calc_key)

    def order_key(b):
        a = b['ORDER'][0]['answer']
        a[0], a[1] = a[1], a[0]
    expect('wrong Order Them key (first two swapped)', order_key)

    rep = Report()                                                              # the audit's F1, F2
    run_page(rep, chromium, patched_helper=True)
    record('0.5 tolerance planted in the helper', rep, [])
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
    bank, clicks = run_page(rep, args.chromium, args.verbose)
    check_bank(rep, bank, args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, args.chromium)
        print('\nFault-injection self-test (patched copies; no file is touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    print('\n%s: %d FAIL(s); %d items (Order Them and Calculate keys recomputed), %d placements marked in '
          'Chromium, every target reached on three phones' % ('PASS' if ok else 'FAILED', len(rep.fails),
                                                              sum(len(v) for v in bank.values()), clicks))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
