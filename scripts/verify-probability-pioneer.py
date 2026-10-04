#!/usr/bin/env python3
"""Probability Pioneer: every key checked, and every answer marked through the real page.

The bank (45 items, one level, played in full and in fixed order every session) was keyed by hand
and never verified; the resit correctness audit of 4 Oct 2026 found two wrong keys (F1 MATHS/GAMES,
F2 "equally likely => 0.5"), two Stage 1 keys or feedback lines that called a possible event
impossible or a likely one certain (F3, F4), two questions with distractors equal in value (F5,
F6) and one overstated law of large numbers (F8).

The bank is read from the live page (post any runtime patch), then:
  Stage 2 (multiple choice): every key recomputed exactly (Fraction) from the question's own
    words, by a reader for each question shape. A stem no reader understands FAILS: extend
    `stage2_value()`, never skip. Four options, the key among them exactly once, no two options
    equal in value (SR-4).
  Stages 1 and 3 (scale, true/false): judgement, not arithmetic, so each key is pinned in
    STAGE1_KEYS / STAGE3_KEYS below with the reason for it. An item missing from the table, a
    table entry missing from the bank, or a key that differs FAILS. Stage 1's feedback label must
    start with the scale point its key sits on and no item may accept a second point; Stage 3's
    explanation must open "Correct." exactly when the key is True (the explanation shows on every
    answer, so a flipped key with an unflipped explanation tells the student the opposite).
  Marking, in Chromium: every item is shown through the game's own functions and EVERY possible
    answer is clicked (5 scale points, 4 options, True and False): "Correct" must show for the key
    and "Not quite" for everything else, and Stage 2's feedback must carry the item's reason.
    The session is never finished, so nothing is submitted; every request off the stub server is
    aborted.
A fault-injection self-test (a wrong Stage 2 key, value-equal distractors, a flipped Stage 3 key,
an accepted second Stage 1 point) must FAIL each time on a patched copy; it runs unless
--no-selftest. The file is never touched.

    python scripts/verify-probability-pioneer.py [--verbose] [--no-selftest] [--chromium PATH]
"""
import argparse
import copy
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'probability-pioneer'
COUNTS = {'STAGE1': 10, 'STAGE2': 20, 'STAGE3': 15}

# ---------------------------------------------------------------------------------------------
# Stage 1: reviewed keys (event -> (scale value, reason)). Change one only with Jon's ruling.
# ---------------------------------------------------------------------------------------------
STAGE1_KEYS = {
    "You will breathe today": (1, "certain for anyone reading it"),
    "You will roll a 7 on a standard die": (0, "a standard die shows 1 to 6"),
    "It will rain somewhere in Britain this week": (0.75, "very likely but not certain; certain means it "
                                                         "must happen (audit F4, Jon 4 Oct 2026)"),
    "You will flip heads on a fair coin": (0.5, "1/2"),
    "A randomly chosen month starts with J": (0.25, "January, June, July: 3/12 = 1/4"),
    "You pick a red card from a standard pack": (0.5, "26/52"),
    "You roll an even number on a die": (0.5, "3/6"),
    "You win the lottery with one ticket": (0.25, "possible, about 1 in 45 million: the scale's nearest "
                                                  "point below even is Unlikely (audit F3, Jon 4 Oct 2026)"),
    "A baby born today is a boy": (0.5, "conventional at this level; the real figure is about 0.51 "
                                        "(audit F7, left as a judgement call)"),
    "The sun will rise tomorrow": (1, "certain"),
}

# ---------------------------------------------------------------------------------------------
# Stage 3: reviewed keys (statement -> (key, reason)).
# ---------------------------------------------------------------------------------------------
STAGE3_KEYS = {
    "P(event) is always between 0 and 1 inclusive": (True, "definition"),
    "If P(A) = 0.3, then P(not A) = 0.7": (True, "P(not A) = 1 - P(A)"),
    "Rolling heads 5 times makes tails more likely next": (False, "independent flips; gambler's fallacy"),
    "P(impossible event) = 0": (True, "definition"),
    "P(certain event) = 1": (True, "definition"),
    "You can have P(event) = 1.5": (False, "a probability never exceeds 1"),
    "If two outcomes are equally likely, each has probability 0.5": (
        False, "only when there are exactly two outcomes: two faces of a dice are equally likely, "
               "each 1/6 (audit F2, Jon 4 Oct 2026)"),
    "P(A) + P(not A) always equals 1": (True, "complementary events"),
    "A probability of 0.9 means the event will definitely happen": (False, "only 1 is certain"),
    "The more times you repeat an experiment, the closer the results tend to get to the theoretical probability": (
        True, "law of large numbers, stated as a tendency, not a guarantee (audit F8)"),
    "A fair die gives each number probability exactly 1/6": (True, "six equally likely outcomes"),
    "P(rolling 7 on a standard die) = 7/6": (False, "impossible, so 0; and 7/6 > 1"),
    "Probability can be written as a fraction, decimal or percentage": (True, "1/2, 0.5, 50%"),
    "If P(rain) = 0.4, it will rain on exactly 4 out of every 10 days": (False, "a long-run proportion, "
                                                                           "not a guarantee for any 10 days"),
    "Two events with the same probability are equally likely": (True, "definition of equally likely"),
}

# ---------------------------------------------------------------------------------------------
# Stage 2: each stem read by the reader for its shape. Sample spaces are listed in full and the
# event counted, so the key is recomputed, never restated.
# ---------------------------------------------------------------------------------------------
DIE = range(1, 7)
VOWELS = set('AEIOU')
COLOURS = {'red': 'R', 'blue': 'B', 'green': 'G', 'yellow': 'Y'}
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
DECK = [(r, s) for s in SUITS for r in RANKS]


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, n))


def prob(space, event):
    space = list(space)
    return F(sum(1 for x in space if event(x)), len(space))


def die_event(text):
    """The event a dice stem asks for, as a predicate, or None."""
    m = re.fullmatch(r'(?:a )?(\d+)', text)
    if m:
        return lambda x, n=int(m.group(1)): x == n
    m = re.fullmatch(r'(\d+) or (\d+)', text)
    if m:
        return lambda x, a=int(m.group(1)), b=int(m.group(2)): x in (a, b)
    m = re.fullmatch(r'less than (\d+)', text)
    if m:
        return lambda x, n=int(m.group(1)): x < n
    m = re.fullmatch(r'greater than (\d+)', text)
    if m:
        return lambda x, n=int(m.group(1)): x > n
    m = re.fullmatch(r'(?:a )?multiple of (\d+)', text)
    if m:
        return lambda x, n=int(m.group(1)): x % n == 0
    return {'odd': lambda x: x % 2 == 1, 'even': lambda x: x % 2 == 0,
            'prime': is_prime, 'square number': lambda x: int(x ** 0.5) ** 2 == x}.get(text)


def bag(text):
    """'3 red, 7 blue' or '5R, 3G, 2Y' -> list of colour letters."""
    out = []
    for part in text.split(','):
        m = re.fullmatch(r'\s*(\d+)\s*([A-Za-z]+)\s*', part)
        if not m:
            return None
        word = m.group(2)
        letter = COLOURS.get(word.lower(), word.upper() if len(word) == 1 else None)
        if letter is None:
            return None
        out += [letter] * int(m.group(1))
    return out


def stage2_value(stem):
    """The exact probability a Stage 2 stem asks for, or None if no reader understands it."""
    m = re.fullmatch(r'P\((.*)\)', stem)
    if not m:
        return None
    s = m.group(1)
    # dice: "rolling X", "X on a die", "rolling X on a (fair) die/dice"
    m = re.fullmatch(r'(?:rolling )?(.+?)(?: on a (?:fair )?(?:die|dice))?', s)
    if m and (s.startswith('rolling ') or re.search(r' on a (?:fair )?(?:die|dice)$', s)):
        ev = die_event(m.group(1))
        if ev:
            return prob(DIE, ev)
    # a fair coin
    if s == 'flipping tails':
        return prob('HT', lambda x: x == 'T')
    if s == 'flipping heads':
        return prob('HT', lambda x: x == 'H')
    if s == 'heads twice in a row':
        return prob([a + b for a in 'HT' for b in 'HT'], lambda x: x == 'HH')
    # a bag of counters: "red from 3 red, 7 blue", "picking red from ...", "green from 5R, 3G, 2Y"
    m = re.fullmatch(r'(?:picking )?(red|blue|green|yellow) from (.+)', s)
    if m:
        b = bag(m.group(2))
        if b:
            return prob(b, lambda x, c=COLOURS[m.group(1)]: x == c)
    # letters: "vowel from A, B, C, D, E", "consonant from M, A, T, H, S"
    m = re.fullmatch(r'(vowel|consonant) from ((?:[A-Z], )*[A-Z])', s)
    if m:
        letters = m.group(2).split(', ')
        want = m.group(1) == 'vowel'
        return prob(letters, lambda x: (x in VOWELS) == want)
    # cards: "heart from 52 cards", "face card from 52"
    m = re.fullmatch(r'(heart|diamond|club|spade|face card) from 52(?: cards)?', s)
    if m:
        if m.group(1) == 'face card':
            return prob(DECK, lambda c: c[0] in 'JQK')
        return prob(DECK, lambda c, suit=m.group(1) + 's': c[1] == suit)
    # a whole number from a range: "even from 1–8"
    m = re.fullmatch(r'(even|odd) from (\d+)–(\d+)', s)
    if m:
        want = 0 if m.group(1) == 'even' else 1
        return prob(range(int(m.group(2)), int(m.group(3)) + 1), lambda x: x % 2 == want)
    # a letter of one word that is also in another: "letter in MATHS also in GAMES"
    m = re.fullmatch(r'letter in ([A-Z]+) also in ([A-Z]+)', s)
    if m:
        return prob(m.group(1), lambda x, other=m.group(2): x in other)
    return None


def option_value(text):
    try:
        return F(text)
    except (ValueError, ZeroDivisionError):
        return None


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, where, what, detail):
        self.fails.append('%s %s: %s' % (where, what, detail))


def check_bank(rep, bank, scale, verbose=False):
    """Every data check. bank = {'STAGE1': [...], 'STAGE2': [...], 'STAGE3': [...]};
    scale = {value: name} read from the page's scale labels."""
    for name, n in COUNTS.items():
        if len(bank.get(name, [])) != n:
            rep.fail(name, 'count', '%d items, expected %d (a change to the bank needs this verifier '
                     'updated)' % (len(bank.get(name, [])), n))

    # Stage 1
    seen = set()
    for i, q in enumerate(bank.get('STAGE1', []), 1):
        where = 'Stage 1 Q%d' % i
        ev = q.get('event')
        seen.add(ev)
        if ev not in STAGE1_KEYS:
            rep.fail(where, 'unreviewed', '%r is not in STAGE1_KEYS: review it and pin its key' % ev)
            continue
        want, why = STAGE1_KEYS[ev]
        if q.get('answer') != want:
            rep.fail(where, 'key', '%r keyed %s (%s), reviewed key %s (%s): %s'
                     % (ev, q.get('answer'), scale.get(q.get('answer'), '?'), want, scale.get(want, '?'), why))
        if q.get('answer') not in scale:
            rep.fail(where, 'scale', 'keyed %s, which is not a point on the scale %s' % (q.get('answer'), sorted(scale)))
        if 'accept' in q or 'acceptLabel' in q:
            rep.fail(where, 'accept', '%r also accepts %s: one point is right' % (ev, q.get('accept')))
        label = q.get('label', '')
        point = scale.get(q.get('answer'))
        if point and not (label == point or label.startswith(point + ':')):
            rep.fail(where, 'feedback', 'the feedback label %r does not start with the keyed point %r'
                     % (label, point))
        if verbose:
            print('  %s %-48s %-4s %s' % (where, ev, q.get('answer'), label))
    for ev in STAGE1_KEYS:
        if ev not in seen:
            rep.fail('Stage 1', 'missing', 'STAGE1_KEYS has %r, the bank does not (reworded? re-review)' % ev)

    # Stage 2
    for i, q in enumerate(bank.get('STAGE2', []), 1):
        where = 'Stage 2 Q%d' % i
        stem, key, opts = q.get('q', ''), q.get('answer'), q.get('options', [])
        want = stage2_value(stem)
        if want is None:
            rep.fail(where, 'unread', '%r: no reader understands this stem; extend stage2_value()' % stem)
        elif option_value(key) != want:
            rep.fail(where, 'key', '%r keyed %s, recomputed %s' % (stem, key, want))
        if len(opts) != 4:
            rep.fail(where, 'options', '%d options, SR-4 wants four: %s' % (len(opts), opts))
        if opts.count(key) != 1:
            rep.fail(where, 'options', 'the key %s appears %d times in %s' % (key, opts.count(key), opts))
        vals = {}
        for o in opts:
            v = option_value(o)
            if v is None:
                rep.fail(where, 'options', 'option %r is not a number this verifier can read' % o)
                continue
            if v in vals:
                rep.fail(where, 'value-equal', '%r and %r are equal in value (%s)' % (vals[v], o, v))
            vals[v] = o
        if verbose:
            print('  %s %-40s key %-5s recomputed %s  %s' % (where, stem, key, want, opts))

    # Stage 3
    seen = set()
    for i, q in enumerate(bank.get('STAGE3', []), 1):
        where = 'Stage 3 Q%d' % i
        st = q.get('statement')
        seen.add(st)
        if st not in STAGE3_KEYS:
            rep.fail(where, 'unreviewed', '%r is not in STAGE3_KEYS: review it and pin its key' % st)
            continue
        want, why = STAGE3_KEYS[st]
        if q.get('answer') is not want:
            rep.fail(where, 'key', '%r keyed %s, reviewed key %s: %s' % (st, q.get('answer'), want, why))
        opens = q.get('explanation', '').startswith('Correct.')
        if opens != (q.get('answer') is True):
            rep.fail(where, 'feedback', 'keyed %s but the explanation %s "Correct.": %r'
                     % (q.get('answer'), 'opens' if opens else 'does not open', q.get('explanation', '')[:70]))
        if verbose:
            print('  %s %-5s %s' % (where, q.get('answer'), st))
    for st in STAGE3_KEYS:
        if st not in seen:
            rep.fail('Stage 3', 'missing', 'STAGE3_KEYS has %r, the bank does not (reworded? re-review)' % st)


# ---------------------------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------------------------
JS_SHOW = '''([stage, i]) => {
  currentStage = stage; questionIndex = i;
  if (stage === 1) showStage1Question(); else if (stage === 2) showStage2Question(); else showStage3Question();
}'''


def run_page(rep, chromium=None, verbose=False):
    """Read the bank and the scale, then click every answer to every item. Returns (bank, scale)."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(**({'executable_path': chromium} if chromium else {}))
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.route('**/*', lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof STAGE3 !== "undefined"', timeout=8000)
            bank = page.evaluate('JSON.parse(JSON.stringify({STAGE1, STAGE2, STAGE3}))')
            scale = {}
            for v, aria in page.evaluate('''[...document.querySelectorAll('#scaleLabels .scale-label')]
                                             .map(l => [parseFloat(l.dataset.value), l.getAttribute('aria-label')])'''):
                scale[int(v) if v == int(v) else v] = aria.split(',')[0]
            page.evaluate('startGame()')
            clicks = 0

            def verdict(sel):
                page.wait_for_selector(sel + '.show', timeout=3000)
                return page.inner_text(sel.replace('Feedback', 'FeedbackInd')).strip()

            for i, q in enumerate(bank['STAGE1']):
                for v, name in scale.items():
                    page.evaluate(JS_SHOW, [1, i])
                    page.click('#scaleLabels .scale-label[data-value="%s"]' % v)
                    page.click('#scaleConfirmBtn')
                    got = verdict('#scaleFeedback')
                    clicks += 1
                    want = 'Correct' if v == q['answer'] else 'Not quite'
                    if got != want:
                        rep.fail('Stage 1 Q%d' % (i + 1), 'marking', '%r: %s (%s) shows %r, expected %r'
                                 % (q['event'], name, v, got, want))
            for i, q in enumerate(bank['STAGE2']):
                for opt in q['options']:
                    page.evaluate(JS_SHOW, [2, i])
                    page.locator('#mcqGrid .mcq-btn', has_text=re.compile('^' + re.escape(opt) + '$')).click()
                    got = verdict('#mcqFeedback')
                    clicks += 1
                    want = 'Correct' if opt == q['answer'] else 'Not quite'
                    if got != want:
                        rep.fail('Stage 2 Q%d' % (i + 1), 'marking', '%r: %s shows %r, expected %r'
                                 % (q['q'], opt, got, want))
                    text = page.inner_text('#mcqFeedbackText')
                    if q.get('why') and q['why'] not in text:
                        rep.fail('Stage 2 Q%d' % (i + 1), 'feedback', 'the reason %r is not shown: %r' % (q['why'], text))
            for i, q in enumerate(bank['STAGE3']):
                for pick, btn in ((True, '#btnTrue'), (False, '#btnFalse')):
                    page.evaluate(JS_SHOW, [3, i])
                    page.click(btn)
                    got = verdict('#tfFeedback')
                    clicks += 1
                    want = 'Correct' if pick is q['answer'] else 'Not quite'
                    if got != want:
                        rep.fail('Stage 3 Q%d' % (i + 1), 'marking', '%r: %s shows %r, expected %r'
                                 % (q['statement'], pick, got, want))
            if page.evaluate('window._mfgCompleted === true'):
                rep.fail('page', 'session', 'the session reached its end screen; it must not (nothing may submit)')
            browser.close()
            for e in errors:
                rep.fail('page', 'error', e)
            if verbose:
                print('  %d answers clicked and marked in Chromium' % clicks)
            return bank, scale, clicks
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank, scale):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank, scale)

    def expect(name, fn):
        nonlocal ok
        b = copy.deepcopy(bank)
        fn(b)
        rep = Report()
        check_bank(rep, b, scale)
        new = [f for f in rep.fails if f not in base.fails]
        ok = ok and bool(new)
        lines.append('  self-test %-38s %s' % (name, ('caught: ' + new[0][:100]) if new else '*** MISSED ***'))

    def find(items, field, text):
        return next(q for q in items if text in q[field])

    def wrong_key(b):
        find(b['STAGE2'], 'q', 'MATHS also in GAMES')['answer'] = '2/5'      # the audit's F1
    expect('wrong Stage 2 key (MATHS/GAMES 2/5)', wrong_key)

    def value_equal(b):
        q = find(b['STAGE2'], 'q', 'heads twice in a row')                     # the audit's F6
        q['options'] = ['1/4', '1/2', '1/8', '2/4']
    expect('value-equal distractors (1/2, 2/4)', value_equal)

    def flipped(b):
        find(b['STAGE3'], 'statement', 'equally likely, each has')['answer'] = True   # the audit's F2
    expect('changed Stage 3 key (0.5 statement True)', flipped)

    def second_point(b):
        q = find(b['STAGE1'], 'event', 'lottery')                              # the audit's F3
        q.update(answer=0, accept=0.25, label='Impossible', acceptLabel='Unlikely')
    expect('Stage 1 lottery keyed Impossible', second_point)
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
    bank, scale, clicks = run_page(rep, args.chromium, args.verbose)
    check_bank(rep, bank, scale, args.verbose)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, scale)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    print('\n%s: %d FAIL(s); %d items (Stage 2 keys recomputed, Stages 1 and 3 against the reviewed '
          'tables), %d answers marked in Chromium'
          % ('PASS' if ok else 'FAILED', len(rep.fails), sum(len(v) for v in bank.values()), clicks))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
