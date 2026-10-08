#!/usr/bin/env python3
# ci-line: B1 | Probability Paradox (every key recomputed exactly; the assumptions each key needs stated (SR-18); every simulation measured against its item's exact answer; answer once and Next once, played in Chromium) |
"""Probability Paradox: every key recomputed, every assumption it needs stated, every simulation honest; answer once.

Three modes (Paradox Predictor, Conditional Calculator, Fallacy Spotter), each item a scenario and four options. The
banks are read from the live page, then:

  Banks: 12 paradox, 14 conditional, 12 fallacy items; four distinct options; the key (and every answer in an item's
    `accept` list) is an option.
  Keys (KEYS): every paradox and conditional item's answer recomputed exactly here from its own numbers, and the key
    states it; a fallacy item is reviewed (FALLACY: the reason its key is the one true option).
  Stated assumptions (SR-18: Probability Paradox states assumptions): each item whose key holds only under an
    assumption says it in the scenario (ASSUMED): the bus arrives at random (probability-paradox-t1-002; "depends on
    the schedule" was literally true), the Two-Child and Tuesday questions are asked (t1-006), Monty always opens a
    goat door and always offers the switch, and a "95% accurate" test says what 95% means.
  SR-18 rulings: the envelope, having seen £20, is "Cannot determine" (t1-001); Sleeping Beauty accepts 1/3 and 1/2
    (t1-003).
  The p-value (t1-007): the drug trial's Fisher exact p is stated two-sided, recomputed here.
  Regression to the mean (t1-004, Jon's ruling 8 Oct 2026): the one item keyed "Regression to the mean" is pinned
    (PINNED_RTM): its scenario selects on the lowest scores and gives a second paper of the same difficulty, its options
    are exactly the four ruled, and the key is the ruled one. In Chromium at 390px it fits with no sideways scroll,
    asking and after a wrong answer.
  Simulations (t1-005): each paradox item's simulate(type) run 20,000 times in the page (Math.random seeded); the share
    of its first outcome must be within 0.015 of the item's exact answer (EXACT) and of the expected bar it declares.
  Chromium: every item played with each option: an accepted answer is marked right on the page, any other wrong; after
    the mark, every option clicked and pressed with Enter changes nothing; with MaffsLock's real window, Next followed
    at once by a click on the new question marks nothing, and a double click on Next moves on once (t1-010: the old
    "Got it" button called nextQ twice, skipping a question); the session ends once.
KNOWN_OPEN holds register entries this script detects and this PR leaves open (reported, never failed; a stale one fails).
A self-test plants nine faults back into a copy of the page; each must FAIL naming its entry.

    python scripts/verify-probability-paradox.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys
from fractions import Fraction as F
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'probability-paradox'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'paradox': 12, 'conditional': 14, 'fallacy': 12}
TAG = 'probability-paradox-'


def fisher_two_sided(a, n1, b, n2):
    """Fisher's exact test, two-sided: the probability of every table no more likely than the observed one."""
    k, n = a + b, n1 + n2
    p = {x: F(comb(n1, x) * comb(n2, k - x), comb(n, k)) for x in range(max(0, k - n2), min(k, n1) + 1)}
    return sum(v for v in p.values() if v <= p[a])


def birthday(n):
    q = F(1)
    for i in range(n):
        q *= F(365 - i, 365)
    return 1 - q


def beats(x, y):
    return F(sum(1 for a in x for b in y if a > b), len(x) * len(y))


DICE_A, DICE_B, DICE_C = [2, 2, 4, 4, 9, 9], [1, 1, 6, 6, 8, 8], [3, 3, 5, 5, 7, 7]

# The exact answer of each paradox item's simulation: the probability of its first outcome (bar 0).
EXACT = {
    'monty': F(2, 3),                                     # switching wins
    'birthday': birthday(23),                             # a match among 23
    'coin': F(1, 2),
    'twochild': F(1, 3),                                  # asked "at least one boy?"
    'bertrand': F(2, 3),
    'falsepos': F(1, 1000) * F(99, 100) / (F(1, 1000) * F(99, 100) + F(999, 1000) * F(1, 100)),
    'tuesday': F(13, 27),
    'envelope': F(1, 2),                                  # before opening: switching wins half the time
    'simpson': F(1),
    'bus': 1 - math.exp(-1),                              # Poisson buses, mean gap 10: P(wait < 10)
    'dice': 1 - beats(DICE_C, DICE_A),                    # A beats C (no ties between A and C)
    'beauty': F(1, 3),                                    # wakings that are Heads
}

# Each item's answer, recomputed: (a phrase identifying the item, the value its key must state, how to read it).
# 'frac' = the key is that fraction exactly; 'pct' = "About N%" to the nearest 5 (paradox) or N; 'dp2' = 2 d.p.
KEYS = [
    ('Monty Hall', F(2, 3), 'frac'),
    ('Birthday Problem', birthday(23), 'about'),
    ("Gambler's Fallacy", F(1, 2), 'frac'),
    ('Two-Child Problem', F(1, 3), 'frac'),
    ("Bertrand's Box", F(2, 3), 'frac'),
    ('False Positive Paradox', EXACT['falsepos'], 'about'),
    ('Tuesday variant', F(13, 27), 'frac'),
    ('Inspection Paradox', F(10), 'minutes'),             # E(wait) = E(gap) for a Poisson stream
    ('Sleeping Beauty', F(1, 3), 'frac'),
    ('5 red and 3 blue', F(4, 7), 'frac'),
    ('Find P(A | B)|P(A) = 0.4', F(2, 10) / F(5, 10), 'dec'),
    ('60% study Maths', F(25, 100) / F(60, 100), 'frac'),
    ('mutually exclusive events', F(3, 10) + F(4, 10), 'dec'),
    ('P(Rain) = 0.3', F(8, 10) * F(3, 10) + F(2, 10) * F(7, 10), 'dec'),
    ('2% of the population', F(95, 100) * F(2, 100) / (F(95, 100) * F(2, 100) + F(5, 100) * F(98, 100)), 'dp2'),
    ('Three coins are flipped', F(3, 4), 'frac'),
    ('P(A) = 0.6, P(B) = 0.3', F(4, 10) * F(7, 10), 'dec'),
    ('P(A only) = 0.15', F(15, 100) + F(10, 100), 'dec'),
    ('machines X and Y', F(3, 100) * F(6, 10) / (F(3, 100) * F(6, 10) + F(5, 100) * F(4, 10)), 'frac'),
    ('P(A) = 0.5, P(B', F(6, 10) * F(5, 10) / (F(6, 10) * F(5, 10) + F(2, 10) * F(5, 10)), 'frac'),
    ('52-card deck', F(4, 12), 'frac'),
    ('4 red, 3 green, 2 blue', (F(4 * 3) + F(3 * 2) + F(2 * 1)) / (9 * 8), 'frac'),
]

# Reviewed (8 Oct 2026): items with no number to recompute, and why the key is the one true option.
CONCEPT = {
    'Envelope Problem': 'SR-18: having seen £20, E(switch) depends on a prior the scenario does not give',
    "Simpson's Paradox": 'checked below from the steps\' own counts',
    'Non-transitive Dice': 'A beats B, B beats C, C beats A (5/9 each), checked below',
    'Are A and B independent': 'P(A)P(B) = 0.2 = P(A ∩ B)',
}
FALLACY = {
    "hasn't come up in 50 draws": 'independent draws: the gambler\'s fallacy',
    'The doctor says': 'base rate neglect',
    'got 7 heads': 'P(7+ heads in 10) = 0.17, checked below',
    'survived a plane crash': 'survivorship bias',
    'hot hand': 'debated since Miller and Sanjurjo (2015)',
    '60 hours a week': 'confusion of the inverse',
    'eat chocolate daily': 'correlation is not causation',
    'horoscope': 'confirmation bias',
    'the lowest scores on a test': 'regression to the mean: picked on the lowest scores (t1-004, pinned: PINNED_RTM)',
    'smoked all their life': 'one anecdote',
    'drug trial': 'a small sample; Fisher two-sided p checked below',
    'eat breakfast': 'causation from correlation',
}

# SR-18: the assumption each key needs, as words the scenario must contain (all of them), and the entry it was filed as.
ASSUMED = {
    'Inspection Paradox': (['at random', 'Poisson', 'no timetable'], TAG + 't1-002'),
    'Two-Child Problem': (['equally likely', 'You ask', 'The answer is yes'], TAG + 't1-006'),
    'Tuesday variant': (['equally likely', 'any day of the week', 'You ask', 'The answer is yes'], TAG + 't1-006'),
    'Monty Hall': (['always opens a door you did not pick that hides a goat', 'always offers'], TAG + 't1-009'),
    '2% of the population': (['95% of people with the disease test positive', '95% of people without it test negative'],
                             TAG + 't1-009'),
}

KNOWN_OPEN = {}

# probability-paradox-t1-004 (Jon's ruling, 8 Oct 2026): regression to the mean needs selection on an extreme score,
# and "the test was easier" must be ruled out by the scenario, so exactly one option is defensible.
PINNED_RTM = {
    'words': ['the lowest scores', 'of the same difficulty'],
    'q': 'What else could explain the rise?',
    'opts': ['Regression to the mean',
             'The method must have worked: a 16-point rise is too big to be anything else',
             'The second paper was easier',
             'The highest scorers would have risen by the same amount'],
    'correct': 'Regression to the mean',
}


def find(bank, phrase):
    """The one item whose scenario (or scenario | question) contains phrase; '|' joins a question part."""
    parts = phrase.split('|')
    hits = [q for q in bank if parts[0] in (q['q'] if len(parts) > 1 else q['scenario'])
            and (len(parts) == 1 or parts[1] in q['scenario'])]
    return hits[0] if len(hits) == 1 else None


def states(key, want, how):
    """The key states want, read the way the item asks for it."""
    if how == 'frac':
        m = re.match(r'\s*(\d+)/(\d+)', key)
        return bool(m) and F(int(m.group(1)), int(m.group(2))) == want
    if how == 'dec':
        m = re.match(r'\s*(\d*\.\d+|\d+)', key)
        return bool(m) and F(m.group(1)) == want
    if how == 'dp2':
        m = re.match(r'\s*(\d*\.\d{2})\b', key)
        return bool(m) and abs(F(m.group(1)) - want) <= F(1, 200)
    if how == 'about':
        m = re.search(r'About (\d+)%', key)
        return bool(m) and abs(int(m.group(1)) - float(want) * 100) < 1.5
    if how == 'minutes':
        m = re.match(r'\s*(\d+) minutes', key)
        return bool(m) and F(m.group(1)) == want
    return False


def check_bank(fails, opens, banks):
    counts = {m: len(banks[m]) for m in COUNTS}
    if counts != COUNTS:
        fails.append('banks: %s items by mode, expected %s' % (counts, COUNTS))
    allq = [q for m in COUNTS for q in banks[m]]
    for q in allq:
        acc = q.get('accept') or [q['correct']]
        if len(q['opts']) != 4 or len(set(q['opts'])) != 4 or not set(acc) <= set(q['opts']) or q['correct'] not in acc:
            fails.append('%s: %d options, %d distinct; accepted %s, all options? %s' % (
                q['q'], len(q['opts']), len(set(q['opts'])), acc, set(acc) <= set(q['opts'])))
    para_cond = banks['paradox'] + banks['conditional']
    seen = set()
    for phrase, want, how in KEYS:
        q = find(para_cond, phrase)
        if not q:
            fails.append('KEYS "%s": no single item matches (re-review the table)' % phrase)
            continue
        seen.add(id(q))
        if not states(q['correct'], want, how):
            fails.append('"%s": the key "%s" does not state %s (recomputed from the item)' % (phrase, q['correct'], float(want)))
    for phrase in CONCEPT:
        q = find(para_cond, phrase.split('|')[0]) or find(para_cond, phrase + '|')
        if q:
            seen.add(id(q))
    for q in para_cond:
        if id(q) not in seen:
            fails.append('"%s": in neither KEYS nor CONCEPT: recompute its answer, or review it' % q['scenario'][:60])
    for q in banks['fallacy']:
        if not any(p in q['scenario'] for p in FALLACY):
            fails.append('fallacy "%s": not reviewed (FALLACY)' % q['scenario'][:60])
    # SR-18: the stated assumptions
    for phrase, (words, tag) in ASSUMED.items():
        q = find(para_cond, phrase)
        if q:
            missing = [w for w in words if w not in q['scenario'].replace('\\"', '"')]
            if missing:
                fails.append('%s "%s": the key holds only if %s, which the scenario does not say (SR-18): "%s"'
                             % (tag, phrase, ' / '.join(missing), re.sub('<[^>]+>', '', q['scenario'])))
    # SR-18 rulings
    env = find(banks['paradox'], 'Envelope Problem')
    if env and not env['correct'].startswith('Cannot determine'):
        fails.append('%s the envelope: keyed "%s"; having seen £20, E(switch) depends on how the amounts were chosen, '
                     'which the scenario does not give (SR-18: "can\'t tell")' % (TAG + 't1-001', env['correct']))
    sb = find(banks['paradox'], 'Sleeping Beauty')
    if sb:
        acc = sb.get('accept') or [sb['correct']]
        if not any(a.startswith('1/2') for a in acc) or not any(a.startswith('1/3') for a in acc):
            fails.append('%s Sleeping Beauty: accepts %s; SR-18 accepts both 1/3 and 1/2' % (TAG + 't1-003', acc))
    # Simpson's counts, the dice, John's coin, the drug trial's p
    simp = find(banks['paradox'], "Simpson's Paradox")
    if simp:
        A = (F(19, 20), F(60, 200), F(79, 220))
        B = (F(180, 200), F(5, 20), F(185, 220))
        if not (A[0] > B[0] and A[1] > B[1] and B[2] > A[2] and 19 + 60 == 79 and 180 + 5 == 185):
            fails.append("Simpson's Paradox: the steps' counts do not show the reversal")
    if not (beats(DICE_A, DICE_B) > F(1, 2) and beats(DICE_B, DICE_C) > F(1, 2) and beats(DICE_C, DICE_A) > F(1, 2)):
        fails.append('Non-transitive dice: the cycle does not hold')
    coin = [q for q in banks['fallacy'] if 'got 7 heads' in q['scenario']]
    p7 = F(sum(comb(10, k) for k in range(7, 11)), 1024)
    if coin and '0.17' not in coin[0]['explain']:
        fails.append('7 heads in 10: P(7+ heads) = %.4f, not stated as 0.17' % float(p7))
    drug = [q for q in banks['fallacy'] if 'drug trial' in q['scenario']]
    if drug:
        p = float(fisher_two_sided(3, 10, 1, 10))
        m = re.search(r'p ≈ (0\.\d+)', drug[0]['explain'])
        if not m or abs(float(m.group(1)) - p) > 0.005 or 'two-sided' not in drug[0]['explain']:
            fails.append('%s drug trial: the explanation gives p ≈ %s; Fisher\'s exact test, two-sided, is %.2f'
                         % (TAG + 't1-007', m.group(1) if m else '?', p))
    # t1-004: the regression item, pinned
    rtm = [q for q in banks['fallacy'] if q['correct'].startswith('Regression to')]
    if len(rtm) != 1:
        fails.append('%s %d fallacy items keyed regression to the mean (exactly one, as ruled)' % (TAG + 't1-004', len(rtm)))
    else:
        q, p = rtm[0], PINNED_RTM
        missing = [w for w in p['words'] if w not in q['scenario']]
        if missing or q['q'] != p['q'] or q['opts'] != p['opts'] or q['correct'] != p['correct'] or q.get('accept'):
            fails.append('%s the regression item "%s": %s (Jon\'s ruling, 8 Oct 2026: selection on the lowest scores, a '
                         'paper of the same difficulty, the four ruled options, keyed "%s")' % (
                             TAG + 't1-004', q['scenario'][:60],
                             'the scenario does not say %s' % ' / '.join(missing) if missing else
                             'question "%s", options %s, key "%s"' % (q['q'], q['opts'], q['correct']), p['correct']))
    for k, v in KNOWN_OPEN.items():
        opens.append('%s: %s' % (k, v))


# ---------------------------------------------------------------------------------------------------- Chromium
SEED = r"""(() => {
  let a = 20261008;
  Math.random = function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  try { localStorage.clear(); } catch (e) {}
  window.__done = 0;
})();"""

BANKS = """() => ({paradox: PARADOX_QUESTIONS, conditional: CONDITIONAL_QUESTIONS, fallacy: FALLACY_QUESTIONS})"""

SIMS = """() => PARADOX_QUESTIONS.map(q => { let c = [0, 0];
  for (let k = 0; k < 20000; k++) [].concat(simulate(q.sim.type)).forEach(x => { c[x]++; });
  return [q.sim.type, c[0] / (c[0] + c[1]), q.sim.expected[0]]; })"""

# Show one item as the game's next question (the game's own nextQ), in the given mode.
SHOW = """([m, idx]) => {
  startMode(m);
  const bank = {paradox: PARADOX_QUESTIONS, conditional: CONDITIONAL_QUESTIONS, fallacy: FALLACY_QUESTIONS}[m];
  pool = [bank[idx], bank[(idx + 1) % bank.length]]; qIdx = 0; total = 0; score = 0; correctN = 0;
  nextQ();
  return [...document.querySelectorAll('#options .opt-btn')].map(b => b.dataset.val);
}"""

CLICK = """(v) => { const b = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === v);
  b.click(); return {right: b.classList.contains('correct'), wrong: b.classList.contains('wrong'), score: score,
  correctN: correctN, revealed: [...document.querySelectorAll('#options .opt-btn.correct')].map(b => b.dataset.val)}; }"""

AGAIN = """() => { document.querySelectorAll('#options .opt-btn').forEach(b => {
  b.click(); b.focus();
  ['keydown', 'keypress', 'keyup'].forEach(t => b.dispatchEvent(new KeyboardEvent(t, {key: 'Enter', bubbles: true})));
  b.click(); }); return {score: score, correctN: correctN,
  marked: document.querySelectorAll('#options .opt-btn.correct, #options .opt-btn.wrong').length}; }"""

NEXT_SEL = '#solution .next-btn, #solution .maffs-next'


def new_page(browser, base, html, fresh_zero, width=1280):
    ctx = browser.new_context(viewport={'width': width, 'height': 900 if width > 600 else 844})
    ctx.add_init_script(SEED)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    if fresh_zero:
        ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    pat = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
    ctx.route(lambda u: bool(pat.search(u)), lambda r: r.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function("typeof PARADOX_QUESTIONS !== 'undefined' && typeof startMode === 'function'", timeout=8000)
    return ctx, page, errors


def sims(fails, page):
    for typ, share, declared in page.evaluate(SIMS):
        exact = float(EXACT[typ])
        if abs(share - exact) > 0.015:
            tag = TAG + 't1-005 ' if typ in ('bus', 'beauty') else ''
            fails.append('%sthe %s simulation shows %.3f for its first bar; the item\'s exact answer is %.3f'
                         % (tag, typ, share, exact))
        if abs(declared - exact) > 0.015:
            fails.append('the %s item declares an expected bar of %s; the exact answer is %.3f' % (typ, declared, exact))


def play(fails, page, banks):
    for m in COUNTS:
        for idx, q in enumerate(banks[m]):
            acc = set(q.get('accept') or [q['correct']])
            for v in q['opts']:
                page.evaluate(SHOW, [m, idx])
                r = page.evaluate(CLICK, v)
                right = v in acc
                if (r['right'], r['wrong']) != (right, not right) or r['correctN'] != (1 if right else 0):
                    tag = TAG + 't1-001 ' if 'Envelope' in q['scenario'] and right else (
                        TAG + 't1-003 ' if 'Sleeping Beauty' in q['scenario'] and right else '')
                    fails.append('%s%s "%s": "%s" was marked %s; it is %s' % (
                        tag, m, re.sub('<[^>]+>', '', q['scenario'])[:50], v,
                        'right' if r['right'] else 'wrong' if r['wrong'] else 'nothing', 'right' if right else 'wrong'))
                if set(r['revealed']) != acc | ({v} if right else set()):
                    fails.append('%s "%s": after "%s" the page shows %s as right (%s)' % (
                        m, re.sub('<[^>]+>', '', q['scenario'])[:50], v, r['revealed'], sorted(acc)))
            if idx == 0:
                page.evaluate(SHOW, [m, idx])
                page.evaluate(CLICK, q['correct'])
                a = page.evaluate(AGAIN)
                if a['correctN'] != 1 or a['marked'] != 1:
                    fails.append('%s answer once (%s): after a mark, clicking and pressing Enter on the options marked '
                                 '%d options and counted %d right (1, 1)' % (TAG + 't1-010', m, a['marked'], a['correctN']))


def next_once(fails, page):
    """With MaffsLock's real fresh window: Next, then at once an option of the new question: nothing marked; a double
    click on Next moves on once (probability-paradox-t1-010); the session ends once."""
    tag = TAG + 't1-010'
    settle = "() => !window.MaffsLock || !MaffsLock.isFresh()"
    wrong = ("() => { const q = currentQ; const ok = q.accept || [q.correct]; [...document.querySelectorAll('#options .opt-btn')]"
             ".find(b => !ok.includes(b.dataset.val)).click(); }")
    ready = "() => { const b = document.querySelector('%s'); return b && !b.disabled; }" % NEXT_SEL
    for m in ('conditional', 'paradox'):
        page.evaluate(SHOW, [m, 0])
        page.wait_for_function(settle, timeout=5000)
        page.evaluate(wrong)
        page.wait_for_function(ready, timeout=15000)
        page.evaluate("() => { document.querySelector('%s').click(); document.querySelector('#options .opt-btn').click(); }" % NEXT_SEL)
        s1 = page.evaluate("() => ({qIdx: qIdx, marked: document.querySelectorAll('#options .opt-btn.correct, #options .opt-btn.wrong').length})")
        if s1['qIdx'] != 2 or s1['marked']:
            fails.append('%s (%s): Next, then a click landing on the new question\'s option: question %d, %d options marked '
                         '(2, 0: the new question is answered unseen)' % (tag, m, s1['qIdx'], s1['marked']))
        page.evaluate(SHOW, [m, 0])
        page.wait_for_function(settle, timeout=5000)
        page.evaluate(wrong)
        page.wait_for_function(ready, timeout=15000)
        page.dblclick(NEXT_SEL)
        page.wait_for_timeout(100)
        s2 = page.evaluate("() => ({qIdx: qIdx, ended: document.getElementById('results').classList.contains('active')})")
        if s2['qIdx'] != 2 or s2['ended']:
            fails.append('%s (%s): a double click on Next moved to question %d%s (one advance, to 2)'
                         % (tag, m, s2['qIdx'], ', and ended the session' if s2['ended'] else ''))
    # a right answer: the game's own Next pressed twice (a double Enter on it) moves on once
    for m in ('conditional', 'paradox'):
        page.evaluate(SHOW, [m, 0])
        page.wait_for_function(settle, timeout=5000)
        page.evaluate("() => { const q = currentQ; const ok = q.accept || [q.correct]; [...document.querySelectorAll("
                      "'#options .opt-btn')].find(b => ok.includes(b.dataset.val)).click(); }")
        page.wait_for_function("() => !!document.querySelector('#solution.show .next-btn')", timeout=15000)
        page.evaluate("() => { const b = document.querySelector('#solution .next-btn'); b.click(); b.click(); }")
        s3 = page.evaluate("() => ({qIdx: qIdx, ended: document.getElementById('results').classList.contains('active')})")
        if s3['qIdx'] != 2 or s3['ended']:
            fails.append('%s (%s): after a right answer, Next pressed twice moved to question %d%s (one advance, to 2)'
                         % (tag, m, s3['qIdx'], ', and ended the session' if s3['ended'] else ''))
    # the session ends once: game_completed counted (an end-of-game count, not a mark)
    page.evaluate(SHOW, ['fallacy', 0])
    page.evaluate("() => { window.__n = 0; const o = window.mfg; window.mfg = function (e) { if (e === 'game_completed') "
                  "window.__n++; return o && o.apply(this, arguments); }; endGame(); endGame(); }")
    n = page.evaluate('() => window.__n')
    if n != 1:
        fails.append('%s the session ended %d times (once: game_completed and submitScore)' % (tag, n))


def phone(fails, page, banks):
    """t1-004: the regression item at 390px, asking and after a wrong answer (its explanation shown): no sideways scroll."""
    idx = [i for i, q in enumerate(banks['fallacy']) if q['correct'].startswith('Regression to')]
    if len(idx) != 1:
        return
    wide = "() => document.documentElement.scrollWidth"
    page.evaluate(SHOW, ['fallacy', idx[0]])
    w1 = page.evaluate(wide)
    q = banks['fallacy'][idx[0]]
    page.evaluate(CLICK, max((o for o in q['opts'] if o != q['correct']), key=len))  # the longest wrong option
    page.wait_for_function("() => document.getElementById('solution').classList.contains('show')", timeout=5000)
    w2 = page.evaluate(wide)
    if max(w1, w2) > 390:
        fails.append('%s the regression item at 390px: the page is %d px wide asking, %d px after a wrong answer (390)'
                     % (TAG + 't1-004', w1, w2))


def run(html):
    from playwright.sync_api import sync_playwright
    fails, opens = [], []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx, page, errors = new_page(browser, base, html, True)
            banks = page.evaluate(BANKS)
            check_bank(fails, opens, banks)
            sims(fails, page)
            play(fails, page, banks)
            ctx.close()
            ctx, page, errors2 = new_page(browser, base, html, False)
            next_once(fails, page)
            ctx.close()
            ctx, page, errors3 = new_page(browser, base, html, True, width=390)
            phone(fails, page, banks)
            ctx.close()
            errs = [e for e in errors + errors2 + errors3 if 'firebase' not in e.lower()]
            if errs:
                fails.append('page errors: %s' % '; '.join(errs[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return fails, opens, banks


# t1-004's item as ruled, and as it was before the ruling (planted back whole)
RTM_NEW = ('{scenario:"A teacher picks the ten students with the lowest scores on a test (average 41%) for a new revision '
           'method. On a second paper of the same difficulty, the group\'s average rises to 57%. The teacher says the '
           'method worked.",\nq:"What else could explain the rise?",\nopts:["Regression to the mean","The method must '
           'have worked: a 16-point rise is too big to be anything else","The second paper was easier","The highest '
           'scorers would have risen by the same amount"],correct:"Regression to the mean",\nexplain:"Students picked for '
           'scoring lowest include some who had an unlucky day. On the next paper their luck evens out, so the group\'s '
           'average rises even if nothing changed. The top scorers would tend to fall back for the same reason. To know '
           'whether the method worked, compare with similar low scorers who did not get it."},')
RTM_OLD = ('{scenario:"A student scores 95% on a test after scoring 60%. The teacher implements a new method and claims '
           'credit.",\nq:"What alternative explanation should be considered?",\nopts:["Regression to the mean","The '
           'method definitely worked","The test was easier","Random chance only"],correct:"Regression to the mean",\nexplain:'
           '"Extreme scores tend to be followed by more typical ones, even without any intervention. A student scoring '
           '60% was probably having a bad day — their next score would likely be higher regardless of the teaching '
           'method."},')

PLANTS = [
    (TAG + 't1-001', 't1-001: the envelope keyed £20',
     'correct:"Cannot determine — it depends on how the amounts were chosen",', 'correct:"£20 — switching doesn\'t help",'),
    (TAG + 't1-002', 't1-002: the bus without its assumption',
     'Buses arrive at random, independently of each other, at an average rate of one every 10 minutes (a Poisson '
     'process): there is no timetable.', 'Buses arrive every 10 minutes on average.'),
    (TAG + 't1-003', 't1-003: Sleeping Beauty 1/3 only',
     'accept:["1/3 — she\'s woken more often on Tails","1/2 — the coin is fair"],\n', ''),
    (TAG + 't1-005', 't1-005: the bus simulation in one gap',
     'let t=-10*Math.log(1-r());', 'let t=-10*Math.log(1-r());return(r()*t)<10?0:1;'),
    (TAG + 't1-005', 't1-005: Sleeping Beauty per experiment',
     'return r()<0.5?[0]:[1,1];', 'return r()<0.5?[0]:[1];'),
    (TAG + 't1-006', 't1-006: the Two-Child question not asked',
     'You ask the parent, \\"Is at least one of them a boy?\\" The answer is yes.', 'You learn that at least one of them is a boy.'),
    (TAG + 't1-007', 't1-007: the one-sided p',
     "(p ≈ 0.58 by Fisher's exact test, two-sided)", "(p ≈ 0.29 by Fisher's exact test)"),
    (TAG + 't1-004', 't1-004: the old regression item', RTM_NEW, RTM_OLD),
    (TAG + 't1-010', 't1-010: no lock on the options',
     "  if(!MaffsLock.lock(document.getElementById('options')))return;\n", ''),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, opens, banks = run(html)
    print('%s: %s items: every key recomputed, every assumption stated, every simulation measured; each option played '
          'in Chromium; answer once, Next once' % (SLUG, '+'.join(str(len(banks[m])) for m in COUNTS)))
    for o in opens:
        print('open  ' + o)
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-44s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            hit = [f for f in run(html.replace(old, new))[0] if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
