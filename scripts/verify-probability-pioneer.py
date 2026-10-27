#!/usr/bin/env python3
# ci-line: Probability Pioneer (Stage 2 keys recomputed, Stages 1 and 3 pinned, every answer marked in Chromium) |
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
ASSUMPTIONS = ('Unless a question says otherwise, every dice has six faces and is fair, every coin is fair, '
               'and every pick is made at random.')

# ---------------------------------------------------------------------------------------------
# Stage 1: reviewed keys (event -> (scale value, reason)). Change one only with Jon's ruling.
# ---------------------------------------------------------------------------------------------
STAGE1_KEYS = {
    "You will roll a number less than 7 on a standard dice": (1, "all six faces are below 7: 6/6", (6, 6)),
    "You will roll a 7 on a standard dice": (0, "a standard dice shows 1 to 6: 0/6", (0, 6)),
    "You pick a card that is not a heart from a standard pack": (0.75, "52 - 13 = 39 cards: 39/52 = 3/4", (39, 52)),
    "You will flip heads on a fair coin": (0.5, "1/2", (1, 2)),
    "A randomly chosen month starts with J": (0.25, "January, June, July: 3/12 = 1/4", (3, 12)),
    "You pick a red card from a standard pack": (0.5, "26/52", (26, 52)),
    "You roll an even number on a dice": (0.5, "3/6", (3, 6)),
    "You flip two fair coins and get two heads": (0.25, "HH is 1 of HH, HT, TH, TT: 1/4", (1, 4)),
    "You roll a number greater than 2 on a dice": (0.75, "3, 4, 5 and 6: 4/6 = 2/3, more than a half, less than 1", (4, 6)),
    "A randomly chosen month has fewer than 32 days": (1, "no month has more than 31 days: 12/12", (12, 12)),
}

# ---------------------------------------------------------------------------------------------
# Stage 3: reviewed keys (statement -> (key, reason)).
# ---------------------------------------------------------------------------------------------
STAGE3_KEYS = {
    "P(event) is always between 0 and 1 inclusive": (True, "definition"),
    "If P(A) = 0.3, then P(not A) = 0.7": (True, "P(not A) = 1 - P(A)"),
    "Flipping heads 5 times makes tails more likely next": (False, "independent flips; gambler's fallacy"),
    "The probability of an impossible event is 0": (True, "definition"),
    "The probability of a certain event is 1": (True, "definition"),
    "A probability can be 1.5": (False, "a probability never exceeds 1"),
    "On a fair dice, rolling a 1 and rolling a 2 are equally likely, so each has probability 0.5.": (
        False, "equally likely outcomes share the probability among all six faces, 1/6 each "
               "(audit F2, Jon 4 Oct 2026; reworded PHRASING-FIX-2, Jon 15 Oct 2026)"),
    "P(A) + P(not A) always equals 1": (True, "complementary events"),
    "A probability of 0.9 means the event will definitely happen": (False, "only 1 is certain"),
    "The more times you repeat an experiment, the closer the results tend to get to the theoretical probability": (
        True, "law of large numbers, stated as a tendency, not a guarantee (audit F8)"),
    "A fair six-sided dice gives each number probability exactly 1/6": (True, "six equally likely outcomes"),
    "The probability of rolling a 7 on an ordinary dice is 7/6": (False, "impossible, so 0; and 7/6 > 1"),
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


def die_phrase(text):
    """'a number less than 3' -> 'less than 3', 'an odd number' -> 'odd', 'a 1 or a 2' -> '1 or 2'."""
    t = text.strip()
    t = re.sub(r'^an? number (?=less|greater)', '', t)
    t = re.sub(r'^an? (odd|even|prime) number$', r'\1', t)
    t = re.sub(r'^a (square number)$', r'\1', t)
    t = re.sub(r'^a (\d+) or a (\d+)$', r'\1 or \2', t)
    return t


def stage2_value(stem):
    """The exact probability a Stage 2 stem asks for, or None if no reader understands it. The stems are the exam's wording (a
    sentence of context, how the thing is chosen, then 'Write down the probability that/of ...'), never P(...) notation."""
    s = stem.strip()
    m = re.fullmatch(r'A fair dice is rolled\. Write down the probability of rolling (.+)\.', s)
    if m:
        ev = die_event(die_phrase(m.group(1)))
        return prob(DIE, ev) if ev else None
    m = re.fullmatch(r'A fair coin is flipped\. Write down the probability of getting (heads|tails)\.', s)
    if m:
        return prob('HT', lambda x, w=m.group(1)[0].upper(): x == w)
    if s == 'A fair coin is flipped twice. Write down the probability of getting heads both times.':
        return prob([a + b for a in 'HT' for b in 'HT'], lambda x: x == 'HH')
    m = re.fullmatch(r'A bag contains (.+?)\. A counter is taken at random\. Write down the probability that the counter is (red|blue|green|yellow)\.', s)
    if m:
        colours = []
        for n, w in re.findall(r'(\d+) (red|blue|green|yellow) counters?', m.group(1)):
            colours += [COLOURS[w]] * int(n)
        if colours:
            return prob(colours, lambda x, c=COLOURS[m.group(2)]: x == c)
    m = re.fullmatch(r'Five cards show the letters (.+?)\. A card is taken at random\. Write down the probability that the letter is a (vowel|consonant)\.', s)
    if m:
        letters = re.findall(r'[A-Z]', m.group(1))
        want = m.group(2) == 'vowel'
        return prob(letters, lambda x: (x in VOWELS) == want)
    m = re.fullmatch(r'A card is taken at random from a pack of 52 playing cards\. Write down the probability that the card is a '
                     r'(heart|diamond|club|spade|picture card \(J, Q or K\))\.', s)
    if m:
        if m.group(1).startswith('picture card'):
            return prob(DECK, lambda c: c[0] in 'JQK')
        return prob(DECK, lambda c, suit=m.group(1) + 's': c[1] == suit)
    m = re.fullmatch(r'A number is chosen at random from ((?:\d+, )*\d+)\. Write down the probability that the number is (even|odd)\.', s)
    if m:
        want = 0 if m.group(2) == 'even' else 1
        return prob([int(x) for x in m.group(1).split(', ')], lambda x: x % 2 == want)
    m = re.fullmatch(r'A letter is chosen at random from the word ([A-Z]+)\. Write down the probability that the letter is also in the word ([A-Z]+)\.', s)
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

    # Wording (R1, R2; SWEEP-1 probability-pioneer-s1-001 to -004): the assumptions are stated on the start
    # screen, every die or coin question names its object, colours are written out, "picture card" says what it
    # is, and a coin is flipped, not rolled.
    if ASSUMPTIONS not in ' '.join(bank.get('START', '').split()):
        rep.fail('start screen', 'assumptions', 'the line %r is missing (SR-17)' % ASSUMPTIONS)
    for i, q in enumerate(bank.get('STAGE2', []), 1):
        stem = q.get('q', '')
        if re.search(r'\d\s*[RGYB]\b', stem) or 'face card' in stem:
            rep.fail('Stage 2 Q%d' % i, 'wording', '%r uses a bare colour letter or "face card"' % stem)
        if re.search(r'rolling|flipping|heads|tails', stem) and not re.search(r'\b(die|dice|coin)\b', stem):
            rep.fail('Stage 2 Q%d' % i, 'wording', '%r does not say what is rolled or flipped (SR-17)' % stem)
    for where_, text_ in ([('Stage 1 Q%d' % i, x.get('event', '') + ' ' + x.get('label', '')) for i, x in enumerate(bank.get('STAGE1', []), 1)]
                          + [('Stage 2 Q%d' % i, x.get('q', '')) for i, x in enumerate(bank.get('STAGE2', []), 1)]
                          + [('Stage 3 Q%d' % i, x.get('statement', '') + ' ' + x.get('explanation', '')) for i, x in enumerate(bank.get('STAGE3', []), 1)]):
        if re.search(r'\bdie\b', text_):
            rep.fail(where_, 'wording', '%r says "die": it is "dice", for one or many (Jon, 27 Oct 2026)' % text_[:60])
        for ev_ in re.findall(r'P\(([^()]*)\)', text_):
            if len(re.findall(r'[A-Za-z]{2,}', ev_)) >= 2:
                rep.fail(where_, 'wording', 'P(%s) holds a situation: write it as a sentence, keep P( ) for short events like P(red)' % ev_)
        if where_.startswith('Stage 2') and 'P(' in text_:
            rep.fail(where_, 'wording', '%r uses P( ): a Stage 2 question is worded as the exam words it' % text_[:60])
    for i, q in enumerate(bank.get('STAGE3', []), 1):
        if re.search(r'rolling heads|rolling tails', q.get('statement', ''), re.I):
            rep.fail('Stage 3 Q%d' % i, 'wording', '%r: a coin is flipped, not rolled' % q['statement'])

    # Stage 1
    seen = set()
    for i, q in enumerate(bank.get('STAGE1', []), 1):
        where = 'Stage 1 Q%d' % i
        ev = q.get('event')
        seen.add(ev)
        if ev not in STAGE1_KEYS:
            rep.fail(where, 'unreviewed', '%r is not in STAGE1_KEYS: review it and pin its key' % ev)
            continue
        want, why, pn = STAGE1_KEYS[ev]
        if q.get('p') != list(pn):
            rep.fail(where, 'probability', '%r stores p = %r, reviewed probability %r (%s)' % (ev, q.get('p'), list(pn), why))
        elif not (isinstance(q['p'][0], int) and isinstance(q['p'][1], int) and q['p'][1] > 0 and 0 <= q['p'][0] <= q['p'][1]):
            rep.fail(where, 'probability', 'p = %r is not [favourable, possible]' % (q['p'],))
        else:
            pf = F(q['p'][0], q['p'][1])
            band = 'impossible' if pf == 0 else 'certain' if pf == 1 else 'even chance' if pf == F(1, 2) else 'unlikely' if pf < F(1, 2) else 'likely'
            point = (scale.get(q.get('answer')) or '').lower()
            if band != point:
                rep.fail(where, 'band', '%r: probability %s is %s, but the keyed point is %r' % (ev, pf, band, point))
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
            page.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.route('**/*', lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof STAGE3 !== "undefined"', timeout=8000)
            bank = page.evaluate('JSON.parse(JSON.stringify({STAGE1, STAGE2, STAGE3, START: document.getElementById("startScreen").innerText}))')
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
        find(b['STAGE2'], 'q', 'word MATHS')['answer'] = '2/5'      # the audit's F1
    expect('wrong Stage 2 key (MATHS/GAMES 2/5)', wrong_key)

    def value_equal(b):
        q = find(b['STAGE2'], 'q', 'flipped twice')                     # the audit's F6
        q['options'] = ['1/4', '1/2', '1/8', '2/4']
    expect('value-equal distractors (1/2, 2/4)', value_equal)

    def flipped(b):
        find(b['STAGE3'], 'statement', 'equally likely, so each has')['answer'] = True   # the audit's F2
    expect('changed Stage 3 key (0.5 statement True)', flipped)

    def second_point(b):
        q = find(b['STAGE1'], 'event', 'two fair coins')                              # the audit's F3
        q.update(answer=0, accept=0.25, label='Impossible', acceptLabel='Unlikely')
    expect('Stage 1 lottery keyed Impossible', second_point)

    def no_assumptions(b):
        b['START'] = b['START'].replace(ASSUMPTIONS, '')
    expect('assumptions line removed (SR-17)', no_assumptions)

    def face_card(b):
        find(b['STAGE2'], 'q', 'picture card')['q'] = 'A card is taken at random from a pack of 52 playing cards. Write down the probability that the card is a face card.'
    expect('"face card" back in Stage 2', face_card)

    def unnamed_coin(b):
        find(b['STAGE2'], 'q', 'getting tails')['q'] = 'Write down the probability of getting tails.'
    expect('coin question with no coin named', unnamed_coin)
    def band_wrong(b):
        find(b['STAGE1'], 'event', 'not a heart')['p'] = [13, 52]                  # rule (g): the word must follow the number
    expect('Stage 1 probability outside its band', band_wrong)

    def no_p(b):
        del find(b['STAGE1'], 'event', 'month starts with J')['p']
    expect('Stage 1 item with no stored probability', no_p)

    def opinion_event(b):
        find(b['STAGE1'], 'event', 'two fair coins')['event'] = 'It will rain somewhere in Britain this week'
    expect('Stage 1 event that is an opinion', opinion_event)

    def long_p(b):
        find(b['STAGE3'], 'statement', 'impossible event')['statement'] = 'P(rolling 7 on a standard dice) = 7/6'
    expect('P( ) holding a situation, "die" kept', long_p)

    def die_back(b):
        find(b['STAGE2'], 'q', 'less than 3')['q'] = 'A fair die is rolled. Write down the probability of rolling a number less than 3.'
    expect('"die" back in Stage 2', die_back)
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
