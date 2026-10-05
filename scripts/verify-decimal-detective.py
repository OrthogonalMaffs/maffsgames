#!/usr/bin/env python3
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
  Place It: the value lies on the line.
  Marking, in Chromium: every item is shown through the game's own loadQuestion().
    Line-Up: the recomputed order is marked right, and with any equal pair swapped; one wrong
      order (two unequal neighbours swapped) is marked wrong; a row with an equal pair shows the
      note naming both cards, right or wrong.
    Round Up: every option clicked; only the key is marked right.
    Place It: on load the marker is off the line and Check is disabled, so no item can score with
      no placement; pressing Check anyway marks nothing. Then a real click on the line at the
      value places the marker, enables Check, and is marked right. (The tolerance around a placed
      marker, audit F2-F4, waits for Jon's ruling and is not checked here.)
    The session is never finished, so nothing is submitted; every request off the stub server is
    aborted.
A fault-injection self-test must FAIL each time: identical cards in a row and an equal-value
distractor (patched bank copies), a wrong Round Up key, and the marker starting at 50% with Check
enabled (a patched page served in place of the file). It runs unless --no-selftest. The file is
never touched.

    python scripts/verify-decimal-detective.py [--verbose] [--no-selftest] [--chromium PATH]
"""
import argparse
import copy
import os
import re
import sys
from decimal import Decimal as D, ROUND_HALF_UP

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

# The planted Place It fault: the pre-4 Oct start (marker at 50%, Check enabled).
START_FIXED = 'until 5 Oct 2026.\n  markerPos = null;'
START_PLANTED = 'until 5 Oct 2026.\n  markerPos = 0.5;'


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


def verdict(text):
    if text is None:
        return None
    return 'right' if text.startswith('Correct') else 'wrong' if text.startswith('Not quite') else text


def run_page(rep, chromium=None, verbose=False, patched_start=False):
    """Read the bank, then mark every item through the page. Returns (bank, actions)."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    page_url = base + '/games/' + SLUG + '/'
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(**({'executable_path': chromium} if chromium else {}))
            page = browser.new_page(viewport={'width': 1000, 'height': 900})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))

            def route(r):
                url = r.request.url
                if not url.startswith(base):
                    return r.abort()
                if patched_start and url.split('?')[0] == page_url:
                    with open(os.path.join(HERE, '..', 'games', SLUG, 'index.html'), encoding='utf-8') as f:
                        html = f.read()
                    assert html.count(START_FIXED) == 1, 'self-test patch out of date: %r' % START_FIXED
                    return r.fulfill(status=200, content_type='text/html',
                                     body=html.replace(START_FIXED, START_PLANTED))
                return r.continue_()
            page.route('**/*', route)
            page.goto(page_url + '?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof PLACEIT_QUESTIONS !== "undefined"', timeout=8000)
            bank = page.evaluate('JSON.parse(JSON.stringify({LINEUP: LINEUP_QUESTIONS, '
                                 'ROUNDUP: ROUNDUP_QUESTIONS, PLACEIT: PLACEIT_QUESTIONS}))')
            page.evaluate('startGame()')
            actions = 0

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

            for i, q in enumerate(bank['PLACEIT'], 1):
                where = 'Place It %d (%s on %s to %s)' % (i, q['value'], q['min'], q['max'])
                page.evaluate(JS_LOAD, ['placeit', q])
                start = page.evaluate('''() => ({pos: markerPos,
                  shown: getComputedStyle(document.getElementById('lineMarker')).display !== 'none',
                  disabled: document.getElementById('checkBtn').disabled,
                  scores: markerPos !== null && placeitCorrect(placeItData, markerPos)})''')
                if start['shown'] or start['pos'] is not None:
                    rep.fail(where, 'start', 'the marker starts on the line (at %s of it)' % start['pos'])
                if start['scores']:
                    rep.fail(where, 'start', 'the marker starts where the marking accepts it: a free mark')
                if not start['disabled']:
                    rep.fail(where, 'start', 'Check is enabled before the student has placed the marker')
                page.evaluate('checkAnswer()')
                if page.evaluate(JS_FEEDBACK) is not None:
                    rep.fail(where, 'start', 'Check with no placement marks the question: %r'
                             % page.evaluate(JS_FEEDBACK))
                    page.evaluate(JS_LOAD, ['placeit', q])
                box = page.locator('#numberLine').bounding_box()
                frac = float((D(str(q['value'])) - D(str(q['min']))) / (D(str(q['max'])) - D(str(q['min']))))
                page.mouse.click(box['x'] + frac * box['width'], box['y'] + box['height'] / 2)
                if page.evaluate("document.getElementById('checkBtn').disabled"):
                    rep.fail(where, 'placing', 'Check is still disabled after the marker is placed')
                    continue
                page.click('#checkBtn')
                text = page.evaluate(JS_FEEDBACK)
                actions += 1
                if verdict(text) != 'right':
                    rep.fail(where, 'marking', 'a click on the value shows %r (marker reads %s)'
                             % (text, page.inner_text('#markerValue')))
            if page.evaluate('window._mfgCompleted === true'):
                rep.fail('page', 'session', 'the session reached its end screen; it must not (nothing may submit)')
            browser.close()
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

    rep = Report()                                                              # the audit's F1
    run_page(rep, chromium, patched_start=True)
    record('Place It marker at 50%, Check enabled (page)', rep)
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
