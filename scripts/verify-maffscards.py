#!/usr/bin/env python3
# ci-line: MaffsCards game (games/maffscards/: every card pair on every category judged against cards.json, distance lowest; every how line ends on its value; hard Marvin's best category for every card in both decks; Marvin's share of best-category picks at easy and hard against MARVIN_BEST over 2,000 choices each; a simulated typical player's first-to-10 win rate in Jon's bands (easy 60-74%, hard 39-53%); Marvin's lines verbatim from the contract, every condition reachable, none repeated in 300 games; one tap never plays; the 100-round cap; the leaderboard only for first-to-10 wins, with the round count; game_completed's result and tally (correct, questions_answered, questions_correct, detail) for a won and a lost first-to-10 game and entire-deck games, adding up to the rounds played; full first-to-10 games against easy and hard in Chromium; the card and the reveal fit 320x568 in normal and Aa; ten planted faults caught) |
# ci-deps: games/maffscards/ tools/maffscards/ data/maffscards.json schools/assets/firebase-leaderboard.js schools/assets/level.js schools/assets/answer-lock.js docs/handover/contracts/ docs/history/contracts/ scripts/plant_common.py
r"""Independent verification for MaffsCards online (games/maffscards/), contract MAFFSCARDS-GAME, 20 Nov 2026.
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page reads games/maffscards/cards.json (tools/maffscards/gen.py's output, checked against data/maffscards.json by
tools/maffscards/check.py) and judges every round itself. This script judges every round again in Python from
cards.json, never from the page:

  data      cards.json against data/maffscards.json (identical once the how lines are taken out); every how line
            starts with its number and ends on its value; every one of Marvin's lines equal to the contract's text
            (docs/.../2026-11-20-maffscards-game.md, parts 3 and 4); every set of lines (category x Marvin wins, loses,
            ties) and every card line reachable by a pair of cards in the main deck; LOWER_IS_BETTER holds
            'maffscards' in schools/assets/firebase-leaderboard.js.
  rules     in Chromium: the page's judgement of all 48 x 48 pairs on all 6 categories equal to Python's (highest wins,
            distance lowest, equal is a tie); Marvin's best category for every card of both decks equal to the rule (the
            category in which his card beats the most other cards of the deck in use, ties to the higher row); the
            card lines win over the sets when their conditions hold, and a used line is never shown again (none when
            a set is used up); one tap on a row never plays, a second row moves the highlight, a second tap on the
            row or on "Play <label>: <value>" plays; Marvin's choice is shown ("Marvin plays <label>") before the
            reveal; the reveal waits on Next; the 100-round cap ends the entire-deck game (more cards wins, equal is a
            draw with the draw line); the leaderboard gets a score only for a first-to-10 game the player wins, the
            round count, on the board '<deck>-<marvin>'; analytics sends game_started and game_completed only, and
            game_completed carries (MARVIN-LOG, 25 Nov 2026) won and, in the Sheet's own columns, correct (the
            player won), questions_answered (rounds played), questions_correct (rounds the player won) and detail
            'you <won> · Marvin <lost> · ties <tied> · <win|loss|draw> · <why>', checked for a won and a lost
            first-to-10 game and entire-deck games at the cap against the tally the test set up, and for the two
            played games against this script's own count of the rounds; won + lost + tied = rounds played.
  marvin    (MARVIN-BALANCE, 25 Nov 2026) Marvin plays his best category with probability MARVIN_BEST[level] (easy 0.30,
            hard 0.60), otherwise one of the six at random. In Chromium, seeded first-to-10 games until Marvin has chosen
            2,000 times at each level: the share of his choices equal to his best (by this script's rule) within 3
            percentage points of MARVIN_BEST + (1 - MARVIN_BEST) x 1/6, the chance a random pick of six is the best one.
  balance   in Python, seeded, with this script's judge and best-category rule and the MARVIN_BEST the page declares:
            2,000 first-to-10 games on the main deck at each level, a model player who plays their card's best category
            half the time and otherwise one at random; the player chooses first, the round's winner chooses next, a tie
            goes to the middle pile and the chooser stays. The player must win 60-74% on easy and 39-53% on hard (Jon's
            targets, 60-70% and 40-50%, with room for sampling).
  sim       300 seeded games (entire deck and first to 10, both decks, easy and hard): every game ends, no line of
            Marvin's twice in one game, every set and card line seen.
  play      a full first-to-10 game against easy and one against hard, by real clicks at 390x844 on a touch screen:
            every reveal's values, how lines and winner checked against Python, Next always waited for.
  fit       at 320x568 in normal and Aa mode (fonts served from scripts/fonts/): every card's six rows and its Play
            button above the fold with the longer start line showing; the reveal's values, how lines, the longest of
            Marvin's lines and Next above the fold for the longest how lines of every category; and no sideways
            scroll at 320x568, 375x667, 390x844, 1366x768 and 1280x720.

Plants (each must FAIL): distance judged highest-wins; a one-tap play; a repeated line of Marvin's; a submit after a
loss; Hard back to always best (MARVIN_BEST.hard 1); Easy never best (MARVIN_BEST.easy 0); the random branch choosing the
best category always.

    python -X utf8 scripts/verify-maffscards.py [--selftest]
"""
import argparse
import glob
import json
import random
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'maffscards'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
CARDS = os.path.join(ROOT, 'games', SLUG, 'cards.json')
DATA = os.path.join(ROOT, 'data', 'maffscards.json')
LEADERBOARD_JS = os.path.join(ROOT, 'schools', 'assets', 'firebase-leaderboard.js')
CONTRACT = '2026-11-20-maffscards-game.md'
BOARDS = ['main-easy', 'main-hard', 'all48-easy', 'all48-hard']
SET_NAMES = {'SOF': 'sof', 'LPF': 'lpf', 'ROMAN': 'roman', 'DIST': 'dist', 'POWERS': 'powers', 'PI': 'pi'}
CARD_IDS = ['64-played', '1-wins-pi', '1-powers', '28-sof', '88-roman', '37-loses', '100-pi']
FIT_SIZES = [(320, 568)]
SIDEWAYS_SIZES = [(320, 568), (375, 667), (390, 844), (1366, 768), (1280, 720)]
SIMS = 300
CHOICES = 2000                       # Marvin's choices sampled in the page, per level
BALANCE_GAMES = 2000                 # simulated first-to-10 games, per level
PLAYER_BEST = 0.5                    # the model player plays their best category half the time
BANDS = {'easy': (0.60, 0.74), 'hard': (0.39, 0.53)}   # Jon, 25 Nov 2026: 60-70% and 40-50%, with room for sampling


# ---------------------------------------------------------------- the rules, in Python
def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def measure(cats, card, key):
    v = card[key]
    return len(v) if cats[key]['measure'] == 'length' else v


def judge(cats, key, a, b):
    """'a', 'b' or 'tie': highest wins, except where the category's winner is lowest (distance)."""
    x, y = measure(cats, a, key), measure(cats, b, key)
    if x == y:
        return 'tie'
    if cats[key]['winner'] == 'lowest':
        return 'a' if x < y else 'b'
    return 'a' if x > y else 'b'


def hard_choice(cats, order, card, pool):
    best, best_n = None, -1
    for key in order:
        n = sum(1 for o in pool if o['n'] != card['n'] and judge(cats, key, card, o) == 'a')
        if n > best_n:
            best, best_n = key, n
    return best


def card_line_holds(cid, cat, you, mar, outcome):
    """The contract's card-line conditions (part 4); outcome is Marvin's: W, L or D."""
    return {
        '64-played': you == 64 or mar == 64,
        '1-wins-pi': cat == 'pi' and you == 1 and outcome == 'L',
        '1-powers': cat == 'powers' and 1 in (you, mar),
        '28-sof': cat == 'sof' and 28 in (you, mar),
        '88-roman': cat == 'roman' and 88 in (you, mar),
        '37-loses': mar == 37 and outcome == 'L',
        '100-pi': cat == 'pi' and 100 in (you, mar),
    }[cid]


# ---------------------------------------------------------------- the contract's lines
def contract_file():
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*' + CONTRACT)):
            return f
    return None


def contract_lines():
    """Marvin's lines from the contract's parts 3 and 4, in the page's JSON shape."""
    f = contract_file()
    if f is None:
        return None
    text = open(f, encoding='utf-8').read()
    out = {'sets': {}, 'cards': [], 'start': [], 'marvinWins': [], 'playerWins': [], 'draw': []}
    for line in text.split('\n'):
        m = re.match(r'^(SOF|LPF|ROMAN|DIST|POWERS|PI) ([WLD]): (.*)$', line)
        if m:
            out['sets'].setdefault(SET_NAMES[m.group(1)], {})[m.group(2)] = m.group(3).split(' | ')
            continue
        for head, key in (('CARD LINES: ', 'cards'), ('START: ', 'start'), ('MARVIN WINS THE GAME: ', 'marvinWins'),
                          ('PLAYER WINS THE GAME: ', 'playerWins'), ('DRAW (entire deck, cap reached): ', 'draw')):
            if line.startswith(head):
                parts = line[len(head):].split(' | ')
                if key == 'cards':
                    out['cards'] = [dict(zip(('when', 'text'), p.split(': ', 1))) for p in parts]
                else:
                    out[key] = parts
    return out


def page_lines(html):
    m = re.search(r'<script type="application/json" id="marvinLines">(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None


# ---------------------------------------------------------------- data checks (no browser)
HOW_END = {'sof': r'= (\d+)$', 'lpf': r'(?:largest prime |: )(\d+)$', 'roman': r': (\d+) letters?$',
           'dist': r'(?:= |: )(\d+)$', 'powers': r': (\d+)$', 'pi': r" appears (\d+) times? in pi's first 1,000 digits$"}


def check_data(html, out, info):
    game, data = load(CARDS), load(DATA)
    stripped = json.loads(json.dumps(game))
    for c in stripped['cards']:
        c.pop('how', None)
    if stripped != data:
        out.append('cards.json is not data/maffscards.json once the how lines are taken out')
    cats = {c['key']: c for c in game['categories']}
    n_how = 0
    for c in game['cards']:
        for key in cats:
            line = c.get('how', {}).get(key, '')
            m = re.search(HOW_END[key], line)
            if not m or int(m.group(1)) != measure(cats, c, key) or not re.match(r'%d\b' % c['n'], line):
                out.append('card %d %s: how line %r does not run from %d to the value %d' % (c['n'], key, line, c['n'], measure(cats, c, key)))
            n_how += 1
    info['how'] = n_how

    want, got = contract_lines(), page_lines(html)
    if want is None:
        out.append('the contract file *%s is not in docs/handover/contracts/ or docs/history/contracts/' % CONTRACT)
    elif got is None:
        out.append('the page has no marvinLines block')
    else:
        for k in ('start', 'marvinWins', 'playerWins', 'draw'):
            if got.get(k) != want[k]:
                out.append("Marvin's %s lines %r, the contract's %r" % (k, got.get(k), want[k]))
        for key in cats:
            for o in 'WLD':
                if got['sets'].get(key, {}).get(o) != want['sets'].get(key, {}).get(o):
                    out.append("Marvin's %s %s lines %r, the contract's %r" % (key, o, got['sets'].get(key, {}).get(o), want['sets'].get(key, {}).get(o)))
        if [c['text'] for c in got['cards']] != [c['text'] for c in want['cards']] or [c['id'] for c in got['cards']] != CARD_IDS:
            out.append("Marvin's card lines are not the contract's, in its order")
        if [c['when'] for c in want['cards']] != [c['when'] for c in got['cards']]:
            out.append("Marvin's card-line conditions are not the contract's: %r" % [c['when'] for c in want['cards']])
        info['lines'] = sum(len(v) for s in got['sets'].values() for v in s.values()) + len(got['cards'])

    # every set and card line reachable in the main deck: a pair with that outcome where no card line holds
    main = [c for c in game['cards'] if c['deck'] == 'main']
    for key in cats:
        for o in 'WLD':
            if not any(o == {'a': 'L', 'b': 'W', 'tie': 'D'}[judge(cats, key, y, m)]
                       and not any(card_line_holds(cid, key, y['n'], m['n'], o) for cid in CARD_IDS)
                       for y in main for m in main if y['n'] != m['n']):
                out.append('%s %s: no pair of main-deck cards reaches this set of lines' % (key, o))
    for cid in CARD_IDS:
        if not any(card_line_holds(cid, key, y['n'], m['n'], {'a': 'L', 'b': 'W', 'tie': 'D'}[judge(cats, key, y, m)])
                   for key in cats for y in main for m in main if y['n'] != m['n']):
            out.append('card line %s: no pair of main-deck cards reaches it' % cid)

    src = open(LEADERBOARD_JS, encoding='utf-8').read()
    m = re.search(r'var LOWER_IS_BETTER = \{([^}]*)\}', src)
    if not m or not re.search(r"'maffscards'\s*:\s*true", m.group(1)):
        out.append("schools/assets/firebase-leaderboard.js: LOWER_IS_BETTER does not hold 'maffscards'")
    if re.search('top' + r'\s+' + 'trumps', html, re.I):
        out.append('the page names the registered trade mark the game must never use')


# ---------------------------------------------------------------- the browser
def open_page(br, base, html, size, aa=False, still=True, fonts=False):
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch,
                         reduced_motion='reduce' if still else 'no-preference')
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    if aa:
        ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
    bc.offline(ctx, base)
    if fonts:
        ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
    page.wait_for_function('!!window.MC && MC.loaded()', timeout=15000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return ctx, page, errors


def check_completed(what, p, want, out):
    """game_completed's result and tally (MARVIN-LOG). want: (winner, why, you, marvin, ties, rounds), from the test, never the page."""
    winner, why, you, mar, ties, rounds = want
    outcome = {'you': 'win', 'marvin': 'loss', 'draw': 'draw'}[winner]
    line = 'you %d · Marvin %d · ties %d · %s · %s' % (you, mar, ties, outcome, why)
    if you + mar + ties != rounds:
        out.append('game_completed, %s: the test tally %d + %d + %d is not %d rounds' % (what, you, mar, ties, rounds))
    if p.get('correct') is not (winner == 'you'):
        out.append('game_completed, %s: correct %r on a %s' % (what, p.get('correct'), outcome))
    if p.get('won') is not (winner == 'you'):
        out.append('game_completed, %s: won %r on a %s' % (what, p.get('won'), outcome))
    if p.get('questions_answered') != rounds or p.get('score') != rounds:
        out.append('game_completed, %s: questions_answered %r, score %r, expected %d rounds played' % (what, p.get('questions_answered'), p.get('score'), rounds))
    if p.get('questions_correct') != you:
        out.append('game_completed, %s: questions_correct %r, expected the player\'s %d rounds won' % (what, p.get('questions_correct'), you))
    d = p.get('detail')
    m = re.match(r'^you (\d+) · Marvin (\d+) · ties (\d+) · (win|loss|draw) · (\w+)$', d or '')
    if not m:
        out.append('game_completed, %s: detail %r is not "you N · Marvin N · ties N · win|loss|draw · why"' % (what, d))
    elif sum(int(x) for x in m.group(1, 2, 3)) != p.get('questions_answered'):
        out.append('game_completed, %s: detail %r does not add up to %r rounds played' % (what, d, p.get('questions_answered')))
    elif d != line:
        out.append('game_completed, %s: detail %r, expected %r' % (what, d, line))


def check_rules(page, game, out, info):
    cats = {c['key']: c for c in game['categories']}
    order = [c['key'] for c in game['categories']]
    by = {c['n']: c for c in game['cards']}
    got = page.evaluate('MC.judgeAll()')
    bad = [(a, b, k, j) for a, b, k, j in got if judge(cats, k, by[a], by[b]) != j]
    for a, b, k, j in bad[:5]:
        out.append('judge %s: %d against %d, the page says %s, the rule %s' % (k, a, b, j, judge(cats, k, by[a], by[b])))
    if len(got) != 48 * 48 * 6:
        out.append('judge: %d judgements, not %d' % (len(got), 48 * 48 * 6))
    info['pairs'] = len(got)
    for deck in ('main', 'all'):
        pool = [c for c in game['cards'] if deck == 'all' or c['deck'] == 'main']
        for n, k in page.evaluate('d => MC.hardAll(d)', deck):
            want = hard_choice(cats, order, by[n], pool)
            if k != want:
                out.append('hard Marvin, %s deck, card %d: chooses %s, the rule %s' % (deck, n, k, want))
    # card lines win over the sets; a used line is never shown again; a used-up set shows none
    q = page.evaluate("""() => { const u = {}, x = {cat: 'pi', you: {n: 1}, marvin: {n: 2}, outcome: 'L'};
        const a = MC.quipFor(x, u), b = MC.quipFor(x, u), c = MC.quipFor(x, u), d = MC.quipFor(x, u), e = MC.quipFor(x, u);
        return [a, b, c, d, e].map(r => r && r.from); }""")
    if q[0] != 'card:1-wins-pi' or q[1:4].count('pi L') != 3 or q[4] is not None:
        out.append("Marvin's lines: 1 winning on pi five times gave %r (the card line, the three pi L lines, then none)" % q)

    def fresh(settings):
        page.evaluate("""s => { MC.seed(5); Object.keys(s).forEach(k => MC.ui.set(k, s[k])); MC.ui.start();
            window.__ev = []; window.__sub = []; }""", settings)

    # one tap never plays
    fresh({'deck': 'main', 'length': 'ten', 'marvin': 'easy'})
    page.click('.mc-row[data-key="sof"]')
    s1 = page.evaluate("[MC.ui.state(), MC.ui.selected(), document.getElementById('playBtn').hidden, document.getElementById('playBtn').textContent]")
    top = by[page.evaluate('MC.ui.game().you[0]')]
    label = 'Play Sum of factors: %d' % top['sof']
    if s1[0] != 'choosing' or s1[1] != 'sof' or s1[2] or s1[3] != label:
        out.append('one tap on Sum of factors: %r, expected still choosing with the button %r' % (s1, label))
    else:                                          # the rest needs the card still on screen
        page.click('.mc-row[data-key="dist"]')
        s2 = page.evaluate("[MC.ui.state(), MC.ui.selected(), [...document.querySelectorAll('.mc-row[aria-pressed=\"true\"]')].map(r => r.dataset.key)]")
        if s2 != ['choosing', 'dist', ['dist']]:
            out.append('a tap on a second row: %r, expected the highlight moved to dist and nothing played' % s2)
        elif page.click('.mc-row[data-key="dist"]') or page.evaluate('MC.ui.state()') != 'reveal':
            out.append('a second tap on the same row did not play it')
        else:
            page.wait_for_timeout(2500)
            if page.evaluate('MC.ui.state()') != 'reveal':
                out.append('the reveal moved on by itself (it must wait on Next)')
    fresh({'deck': 'main', 'length': 'ten', 'marvin': 'easy'})
    page.click('.mc-row[data-key="pi"]')
    if page.evaluate('MC.ui.state()') == 'choosing':
        page.click('#playBtn')
        if page.evaluate('MC.ui.state()') != 'reveal' or page.evaluate('MC.ui.last().cat') != 'pi':
            out.append('the Play button did not play the highlighted row')

    # Marvin chooses: "Marvin plays <label>" before the reveal
    fresh({'deck': 'main', 'length': 'ten', 'marvin': 'hard'})
    page.evaluate("MC.ui.rig([2, 7], [64, 1], 2)")
    # Marvin wins this round on sum of factors (64: 127 against 2: 3), so he chooses the next
    page.evaluate("MC.ui.tap('sof'); MC.ui.tap('sof')")
    page.evaluate('MC.ui.next()')
    st = page.evaluate("[MC.ui.state(), document.getElementById('say').textContent, document.getElementById('reveal').hidden]")
    if st[0] != 'marvin' or not re.match(r'^Marvin plays (Sum of factors|Largest prime factor|Roman numeral length|Distance to nearest square|Superpowers|Times in pi\'s first 1,000 digits)$', st[1]) or not st[2]:
        out.append("Marvin's turn: %r, expected \"Marvin plays <label>\" with his card still face down" % st)

    # the 100-round cap: the entire-deck game ends after round 100; equal cards is a draw, with the draw line
    fresh({'deck': 'main', 'length': 'deck', 'marvin': 'easy'})
    tie = next((y['n'], m['n']) for y in game['cards'] for m in game['cards']
               if y['deck'] == m['deck'] == 'main' and y['n'] != m['n'] and judge(cats, 'lpf', y, m) == 'tie')
    page.evaluate('a => MC.ui.rig([a[0], 11, 17], [a[1], 53, 61], 100, {you: 40, marvin: 39}, 20)', list(tie))
    page.evaluate("MC.ui.tap('lpf'); MC.ui.tap('lpf'); MC.ui.next()")
    g = page.evaluate("[MC.ui.state(), MC.ui.game().result, document.getElementById('resQuip').textContent, document.getElementById('resTitle').textContent]")
    if g[0] != 'over' or g[1] != {'winner': 'draw', 'why': 'cap'} or not g[2].endswith('Unsettling.') or g[3] != 'A draw':
        out.append('the 100-round cap with equal cards: %r, expected a draw after round 100 with the draw line' % g)
    done = page.evaluate("window.__ev.filter(e => e[0] === 'game_completed').map(e => e[1])")
    if len(done) != 1:
        out.append('entire deck, draw at the cap: %d game_completed events, expected 1' % len(done))
    else:                                          # the last round a tie: 40 + 39 + 21 = 100
        check_completed('entire deck, draw at the cap', done[0], ('draw', 'cap', 40, 39, 21, 100), out)
    fresh({'deck': 'main', 'length': 'deck', 'marvin': 'easy'})
    page.evaluate('MC.ui.rig([64, 11, 17], [2, 53, 61], 100, {you: 45, marvin: 49}, 5)')
    page.evaluate("MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
    g = page.evaluate("[MC.ui.game().result, window.__sub.length, window.__ev.filter(e => e[0] === 'game_completed').map(e => e[1])]")
    if g[0] != {'winner': 'you', 'why': 'cap'} or g[1]:
        out.append('the 100-round cap, more cards: %r, expected a win at the cap and no leaderboard score' % g[:2])
    if len(g[2]) != 1:
        out.append('entire deck, win at the cap: %d game_completed events, expected 1' % len(g[2]))
    else:                                          # more cards wins the deck game, whatever the rounds: 46 + 49 + 5 = 100
        check_completed('entire deck, win at the cap', g[2][0], ('you', 'cap', 46, 49, 5, 100), out)

    # the leaderboard: a first-to-10 win only, the rounds taken, on '<deck>-<marvin>'
    # each case: settings, piles, round, wins and ties before the round, the leaderboard call, then game_completed's
    # (winner, why, you, marvin, ties, rounds) after it (the round is won on sum of factors, 64's 127 against 2's 3)
    cases = [({'deck': 'main', 'length': 'ten', 'marvin': 'easy'}, [64, 1], [2, 7], 13, {'you': 9, 'marvin': 3}, 0, [['maffscards', 'main-easy', 13, 13]],
              ('you', 'ten', 10, 3, 0, 13)),
             ({'deck': 'all', 'length': 'ten', 'marvin': 'hard'}, [64, 1], [2, 7], 10, {'you': 9, 'marvin': 0}, 0, [['maffscards', 'all48-hard', 10, 10]],
              ('you', 'ten', 10, 0, 0, 10)),
             ({'deck': 'main', 'length': 'ten', 'marvin': 'easy'}, [2, 1], [64, 7], 15, {'you': 3, 'marvin': 9}, 2, [],
              ('marvin', 'ten', 3, 10, 2, 15)),
             ({'deck': 'main', 'length': 'ten', 'marvin': 'easy'}, [64], [2], 12, {'you': 5, 'marvin': 6}, 0, [],
              ('you', 'out', 6, 6, 0, 12))]
    for settings, you, mar, rnd, wins, ties, want, tally in cases:
        fresh(settings)
        page.evaluate('a => MC.ui.rig(a[0], a[1], a[2], a[3], a[4])', [you, mar, rnd, wins, ties])
        page.evaluate("MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
        got = page.evaluate("[MC.ui.state(), window.__sub, MC.ui.game().result, window.__ev.filter(e => e[0] === 'game_completed').map(e => e[1])]")
        what = '%s %s, %s' % (settings['deck'], settings['marvin'], 'won' if want else 'not won to 10')
        if got[0] != 'over' or got[1] != want:
            out.append('leaderboard, %s: submitted %r (result %r), expected %r' % (what, got[1], got[2], want))
        if len(got[3]) != 1:
            out.append('game_completed, first to 10, %s: %d events, expected 1' % (what, len(got[3])))
        else:
            check_completed('first to 10, %s, %s' % (what, tally[0] + ' ' + tally[1]), got[3][0], tally, out)
    allowed = page.evaluate("b => b.map(k => MaffsLevel.allows('maffscards', k))", BOARDS)
    if not all(allowed):
        out.append('MaffsLevel does not allow every board: %r' % dict(zip(BOARDS, allowed)))


CHOICES_JS = r"""([marvin, want]) => {
  const keys = ['sof', 'lpf', 'roman', 'dist', 'powers', 'pi'], got = [];
  for (let seed = 1; got.length < want && seed < 5000; seed++) {
    MC.seed(seed); MC.ui.set('deck', 'main'); MC.ui.set('length', 'ten'); MC.ui.set('marvin', marvin); MC.ui.start();
    for (let i = 0; i < 2000 && MC.ui.state() !== 'over' && got.length < want; i++) {
      const s = MC.ui.state();
      if (s === 'choosing') { const k = keys[(seed + i) % 6]; MC.ui.tap(k); MC.ui.tap(k); }
      else if (s === 'marvin') { got.push([MC.ui.selected(), MC.ui.game().mar[0]]); MC.ui.play(); }
      else if (s === 'reveal') MC.ui.next();
    }
  }
  return got;
}"""


def declared_best(html):
    """MARVIN_BEST as the page declares it: {'easy': p, 'hard': p}."""
    m = re.search(r'var MARVIN_BEST = \{ easy: ([\d.]+), hard: ([\d.]+) \};', html)
    if not m:
        raise ValueError('no MARVIN_BEST declaration in the page')
    return {'easy': float(m.group(1)), 'hard': float(m.group(2))}


def check_marvin(page, game, out, info):
    """Marvin's choices in the page: the share equal to his best category against MARVIN_BEST plus chance."""
    cats = {c['key']: c for c in game['categories']}
    order = [c['key'] for c in game['categories']]
    pool = [c for c in game['cards'] if c['deck'] == 'main']
    by = {c['n']: c for c in game['cards']}
    best = {c['n']: hard_choice(cats, order, c, pool) for c in pool}
    declared = page.evaluate('MC.marvinBest')
    chance = 1 / len(order)
    for level in ('easy', 'hard'):
        got = page.evaluate(CHOICES_JS, [level, CHOICES])
        if len(got) < CHOICES:
            out.append('marvin %s: only %d choices sampled' % (level, len(got)))
            continue
        share = sum(1 for k, n in got if k == best[n]) / len(got)
        want = declared[level] + (1 - declared[level]) * chance
        info.setdefault('marvin', []).append((level, share, want, declared[level]))
        if abs(share - want) > 0.03:
            out.append('marvin %s: %.1f%% of %d choices are his best category, expected %.1f%% (MARVIN_BEST %.2f + %.2f x 1/6 by chance)'
                       % (level, 100 * share, len(got), 100 * want, declared[level], 1 - declared[level]))
        if any(k not in cats for k, n in got) or any(n not in by for k, n in got):
            out.append('marvin %s: a choice outside the six categories or the deck' % level)


def check_balance(html, out, info):
    """A model player against Marvin, in Python: the first-to-10 win rate at each level against Jon's bands."""
    game = load(CARDS)
    cats = {c['key']: c for c in game['categories']}
    order = [c['key'] for c in game['categories']]
    pool = [c for c in game['cards'] if c['deck'] == 'main']
    best = {c['n']: hard_choice(cats, order, c, pool) for c in pool}
    declared = declared_best(html)
    for level in ('easy', 'hard'):
        rng = random.Random(25112026 + (level == 'hard'))
        wins = 0
        for _ in range(BALANCE_GAMES):
            cards = pool[:]
            rng.shuffle(cards)
            you, mar, mid = cards[0::2], cards[1::2], []
            won = {'you': 0, 'marvin': 0}
            chooser = 'you'
            while True:
                if won['you'] >= 10 or won['marvin'] >= 10 or not you or not mar:
                    break
                a, b = you[0], mar[0]
                if chooser == 'you':
                    key = best[a['n']] if rng.random() < PLAYER_BEST else rng.choice(order)
                else:
                    key = best[b['n']] if rng.random() < declared[level] else rng.choice(order)
                r = judge(cats, key, a, b)
                you.pop(0)
                mar.pop(0)
                if r == 'a':
                    you += [a, b] + mid
                    mid = []
                    won['you'] += 1
                    chooser = 'you'
                elif r == 'b':
                    mar += [b, a] + mid
                    mid = []
                    won['marvin'] += 1
                    chooser = 'marvin'
                else:
                    mid += [a, b]
            if won['you'] >= 10 or (won['marvin'] < 10 and len(you) > len(mar)):
                wins += 1
        rate = wins / BALANCE_GAMES
        lo, hi = BANDS[level]
        info.setdefault('balance', []).append((level, rate, declared[level]))
        if not lo <= rate <= hi:
            out.append('balance %s: a typical player (best category half the time) wins %.1f%% of %d first-to-10 games against MARVIN_BEST %.2f, outside %d-%d%%'
                       % (level, 100 * rate, BALANCE_GAMES, declared[level], 100 * lo, 100 * hi))


SIM_JS = r"""([seed, settings]) => {
  MC.seed(seed); Object.keys(settings).forEach(k => MC.ui.set(k, settings[k])); MC.ui.start();
  const keys = ['sof', 'lpf', 'roman', 'dist', 'powers', 'pi'];
  const froms = [];
  for (let i = 0; i < 2000 && MC.ui.state() !== 'over'; i++) {
    const s = MC.ui.state();
    if (s === 'choosing') { const k = keys[(seed + i) % 6]; MC.ui.tap(k); MC.ui.tap(k); }
    else if (s === 'marvin') MC.ui.play();
    else if (s === 'reveal') { const r = MC.ui.last(); froms.push(r.quipFrom); MC.ui.next(); }
  }
  const g = MC.ui.game();
  return { state: MC.ui.state(), quips: g.quips, froms: froms, result: g.result, round: g.round, wins: g.wins };
}"""


def check_sim(page, out, info):
    seen, n = set(), 0
    for i in range(SIMS):
        settings = {'deck': ('main', 'all')[i % 2], 'length': ('deck', 'ten', 'deck')[i % 3], 'marvin': ('easy', 'hard')[(i // 2) % 2]}
        r = page.evaluate(SIM_JS, [i + 1, settings])
        n += 1
        if r['state'] != 'over':
            out.append('sim %d %r: the game did not end (round %d)' % (i + 1, settings, r['round']))
            continue
        lines = [q for q in r['quips'] if q]
        if len(lines) != len(set(lines)):
            dup = next(q for q in lines if lines.count(q) > 1)
            out.append('sim %d %r: Marvin said %r twice in one game' % (i + 1, settings, dup))
        if settings['length'] == 'deck' and r['round'] > 100:
            out.append('sim %d: the entire-deck game ran to round %d' % (i + 1, r['round']))
        seen.update(f for f in r['froms'] if f)
    want = {'%s %s' % (k, o) for k in SET_NAMES.values() for o in 'WLD'} | {'card:' + c for c in CARD_IDS}
    missing = sorted(want - seen)
    if missing:
        out.append('in %d games these of Marvin\'s line sets never came up: %s' % (SIMS, ', '.join(missing)))
    info['sims'] = n


def check_play(page, game, marvin, out, info):
    """A whole first-to-10 game by real clicks: rows tapped twice or tapped then Play, Marvin's card turned, Next."""
    cats = {c['key']: c for c in game['categories']}
    by = {c['n']: c for c in game['cards']}
    page.evaluate("s => { MC.seed(s === 'hard' ? 11 : 3); MC.ui.set('deck', 'main'); MC.ui.set('length', 'ten'); MC.ui.set('marvin', s); window.__ev = []; window.__sub = []; }", marvin)
    page.click('#startBtn')
    rounds, tally = 0, {'you': 0, 'marvin': 0, 'tie': 0}   # this script's own count, from its judgement of each reveal
    for i in range(400):
        st = page.evaluate('MC.ui.state()')
        if st == 'over':
            break
        if st == 'choosing':
            key = ['pi', 'sof', 'dist', 'lpf', 'roman', 'powers'][i % 6]
            page.click('.mc-row[data-key="%s"]' % key)
            if page.evaluate('MC.ui.state()') != 'choosing':
                out.append('play vs %s: one tap played' % marvin)
            if i % 2:
                page.click('.mc-row[data-key="%s"]' % key)
            else:
                page.click('#playBtn')
        elif st == 'marvin':
            page.click('#playBtn')
        elif st == 'reveal':
            r = page.evaluate("""() => { const r = MC.ui.last();
                r.vals = [...document.querySelectorAll('#rvGrid .rv-val')].map(e => e.textContent);
                r.how = [...document.querySelectorAll('#rvGrid .rv-how')].map(e => e.textContent);
                r.win = [...document.querySelectorAll('#rvGrid .rv-side.win')].map(e => e.classList.contains('you') ? 'you' : 'marvin');
                r.quipShown = document.getElementById('quip').hidden ? null : document.getElementById('quip').textContent;
                r.nextShown = !!document.getElementById('nextBtn').offsetParent; return r; }""")
            y, m, k = by[r['you']], by[r['marvin']], r['cat']
            j = {'a': 'you', 'b': 'marvin', 'tie': 'tie'}[judge(cats, k, y, m)]

            def shown(c):
                return 'none' if k == 'lpf' and c['lpf'] == 0 else str(measure(cats, c, k))
            if r['winner'] != j or r['win'] != ([] if j == 'tie' else [j]):
                out.append('play vs %s: %d against %d on %s: the page says %s (highlighted %r), the rule %s' % (marvin, y['n'], m['n'], k, r['winner'], r['win'], j))
            if r['vals'] != [shown(y), shown(m)] or r['how'] != [y['how'][k], m['how'][k]]:
                out.append('play vs %s: the reveal shows %r / %r, the cards say %r / %r' % (marvin, r['vals'], r['how'], [shown(y), shown(m)], [y['how'][k], m['how'][k]]))
            if (r['quip'] is None) != (r['quipShown'] is None) or (r['quip'] and not r['quipShown'].endswith(r['quip'])):
                out.append('play vs %s: Marvin\'s line %r, shown %r' % (marvin, r['quip'], r['quipShown']))
            if not r['nextShown']:
                out.append('play vs %s: no Next on the reveal' % marvin)
            rounds += 1
            tally[j] += 1
            page.click('#nextBtn')
            page.wait_for_function("MC.ui.state() !== 'moving'", timeout=5000)
        else:
            page.wait_for_timeout(30)
    g = page.evaluate("[MC.ui.state(), MC.ui.game(), window.__ev.map(e => [e[0], e[1].level, e[1].score, e[1].won]), window.__sub, window.__ev.map(e => e[1])]")
    st, gm, ev, sub, params = g
    if st != 'over':
        out.append('play vs %s: the game did not end in 400 steps' % marvin)
        return
    if max(gm['wins'].values()) != 10 or gm['result']['why'] != 'ten':
        out.append('play vs %s: ended %r with wins %r, not at 10 rounds won' % (marvin, gm['result'], gm['wins']))
    names = [e[0] for e in ev]
    if names != ['game_started', 'game_completed']:
        out.append('play vs %s: analytics sent %r, expected game_started and game_completed only' % (marvin, names))
    elif ev[1][1] != 'main-' + marvin or ev[1][2] != gm['round'] or ev[1][3] != (gm['result']['winner'] == 'you'):
        out.append('play vs %s: game_completed %r' % (marvin, ev[1]))
    else:
        winner = 'you' if tally['you'] == 10 else 'marvin' if tally['marvin'] == 10 else 'draw'
        check_completed('play vs %s' % marvin, params[1], (winner, 'ten', tally['you'], tally['marvin'], tally['tie'], rounds), out)
    want = [['maffscards', 'main-' + marvin, gm['round'], gm['round']]] if gm['result']['winner'] == 'you' else []
    if sub != want:
        out.append('play vs %s: submitted %r, expected %r' % (marvin, sub, want))
    lines = [q for q in gm['quips'] if q]
    if len(lines) != len(set(lines)):
        out.append('play vs %s: a line of Marvin\'s repeated' % marvin)
    info.setdefault('played', []).append('%s: %d rounds, %s won %d-%d, %d tied' % (marvin, rounds, gm['result']['winner'], gm['wins']['you'], gm['wins']['marvin'], tally['tie']))


FIT_JS = r"""() => {
  window.scrollTo(0, 0);
  const foot = document.querySelector('.site-footer');
  const fixed = foot && getComputedStyle(foot).position === 'fixed';
  const fold = innerHeight - (fixed ? foot.getBoundingClientRect().height : 0);
  const bottom = sel => { const e = document.querySelector(sel); if (!e || !e.offsetParent) return null; return e.getBoundingClientRect().bottom + scrollY; };
  const rows = [...document.querySelectorAll('#yourCard .mc-row')].map(e => e.getBoundingClientRect().bottom + scrollY);
  const reveal = ['#rvGrid', '#rvOut', '#quip', '#nextBtn'].map(bottom);
  return { fold: fold, rows: rows.length ? Math.max(...rows) : null, play: bottom('#playBtn'), reveal: reveal,
           sideways: document.documentElement.scrollWidth > innerWidth + 1 };
}"""


def check_fit(br, base, html, game, out, info):
    cats = {c['key']: c for c in game['categories']}
    lines = page_lines(html)
    all_lines = [t for s in lines['sets'].values() for v in s.values() for t in v] + [c['text'] for c in lines['cards']]
    longest_line = max(all_lines, key=len)
    longest_start = max(lines['start'], key=len)
    measured = 0
    for size in FIT_SIZES:
        for aa in (False, True):
            tag = '%dx%d%s' % (size[0], size[1], ' Aa' if aa else '')
            ctx, page, errs = open_page(br, base, html, size, aa=aa, fonts=True)
            page.evaluate("document.fonts.ready.then(() => 0)")
            page.evaluate("MC.seed(1); MC.ui.set('length', 'ten'); MC.ui.set('deck', 'all'); MC.ui.start()")
            worst = None
            for c in game['cards']:
                other = 64 if c['n'] != 64 else 2
                page.evaluate('a => MC.ui.rig([a[0], 5], [a[1], 13], 1)', [c['n'], other])
                page.evaluate("t => { document.getElementById('say').innerHTML = '<span class=\"who\">Marvin:</span> ' + t; }", longest_start)
                page.evaluate("MC.ui.tap('pi')")
                f = page.evaluate(FIT_JS)
                over = max(f['rows'], f['play']) - f['fold']
                if worst is None or over > worst[0]:
                    worst = (over, c['n'], f)
                measured += 1
            if worst[0] > 0:
                out.append('%s: card %d\'s rows and Play end at %.0f px, below the fold at %.0f px' % (tag, worst[1], max(worst[2]['rows'], worst[2]['play']), worst[2]['fold']))
            info.setdefault('fit', []).append('%s card: worst %.0f px under the fold (card %d)' % (tag, -worst[0], worst[1]))
            worst = None
            for key in cats:
                two = sorted(game['cards'], key=lambda c: -len(c['how'][key]))[:2]
                page.evaluate('a => MC.ui.rig([a[0], 5], [a[1], 13], 2)', [two[0]['n'], two[1]['n']])
                page.evaluate("k => { MC.ui.tap(k); MC.ui.tap(k); }", key)
                page.evaluate("t => { const q = document.getElementById('quip'); q.hidden = false; q.innerHTML = '<span class=\"who\">Marvin:</span> ' + t;"
                              " document.getElementById('rvOut').textContent = 'A tie: 116 and 116. Both cards go to the middle pile.'; }", longest_line)
                f = page.evaluate(FIT_JS)
                if None in f['reveal']:
                    out.append('%s reveal on %s: a part is not shown: %r' % (tag, key, f['reveal']))
                    continue
                over = max(f['reveal']) - f['fold']
                if worst is None or over > worst[0]:
                    worst = (over, key, f)
                measured += 1
            if worst and worst[0] > 0:
                out.append('%s: the reveal on %s ends at %.0f px, below the fold at %.0f px' % (tag, worst[1], max(worst[2]['reveal']), worst[2]['fold']))
            if worst:
                info['fit'].append('%s reveal: worst %.0f px under the fold (%s)' % (tag, -worst[0], worst[1]))
            out.extend('page error (fit %s): %s' % (tag, e) for e in errs if 'production host' not in e)
            ctx.close()
    for size in SIDEWAYS_SIZES:
        for aa in (False, True):
            ctx, page, errs = open_page(br, base, html, size, aa=aa, fonts=True)
            for step in ('menu', 'choose', 'reveal', 'results'):
                if step == 'choose':
                    page.evaluate("MC.seed(2); MC.ui.start(); MC.ui.rig([1, 5], [96, 13], 1); MC.ui.tap('powers')")
                elif step == 'reveal':
                    page.evaluate("MC.ui.tap('powers')")
                elif step == 'results':
                    page.evaluate("MC.ui.rig([64, 5], [2], 30, {you: 9, marvin: 9}); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
                if page.evaluate(FIT_JS)['sideways']:
                    out.append('%dx%d%s: the %s screen scrolls sideways' % (size[0], size[1], ' Aa' if aa else '', step))
            ctx.close()
    info['fit_n'] = measured


# ---------------------------------------------------------------- run
def check(html, out, units):
    info = {}
    game = load(CARDS)
    if 'data' in units:
        check_data(html, out, info)
    if 'balance' in units:
        try:
            check_balance(html, out, info)
        except Exception as e:  # noqa: BLE001
            out.append('balance threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u not in ('data', 'balance')]
    if not browser:
        return info
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            try:
                def guarded(name, fn, *a):
                    """A unit that throws is a finding (named), not a crash: the other units still run."""
                    try:
                        fn(*a)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (name, str(e).splitlines()[0][:200]))
                if 'rules' in browser or 'sim' in browser or 'marvin' in browser:
                    ctx, page, errs = open_page(br, base, html, (1280, 800))
                    if 'rules' in browser:
                        guarded('rules', check_rules, page, game, out, info)
                    if 'marvin' in browser:
                        guarded('marvin', check_marvin, page, game, out, info)
                    if 'sim' in browser:
                        ctx.close()
                        ctx, page, errs2 = open_page(br, base, html, (1280, 800))
                        errs += errs2
                        guarded('sim', check_sim, page, out, info)
                    out.extend('page error (rules): %s' % e for e in errs if 'production host' not in e)
                    ctx.close()
                if 'play' in browser:
                    for marvin, still in (('easy', False), ('hard', True)):
                        ctx, page, errs = open_page(br, base, html, (390, 844), still=still)
                        guarded('play vs ' + marvin, check_play, page, game, marvin, out, info)
                        out.extend('page error (play %s): %s' % (marvin, e) for e in errs if 'production host' not in e)
                        ctx.close()
                if 'fit' in browser:
                    guarded('fit', check_fit, br, base, html, game, out, info)
            finally:
                br.close()
    finally:
        proc.terminate()
    return info


PLANTS = [
    ('distance judged highest-wins', [("var lowWins = BYKEY[key].winner === 'lowest';", "var lowWins = false;")],
     ['rules'], r'^judge dist: '),
    ('a one-tap play', [("if (sel === key) { play(); return; }", "if (true) { sel = key; play(); return; }")],
     ['rules'], r'^one tap on Sum of factors'),
    ("a repeated line of Marvin's", [(".filter(function (t) { return !used[t]; });", ".filter(function (t) { return true; });")],
     ['sim'], r'twice in one game'),
    ('a submit after a loss', [("if (G.length !== 'ten' || G.result.winner !== 'you' || G.result.why !== 'ten') return null;",
                                "if (G.length !== 'ten' || G.result.why !== 'ten') return null;")],
     ['rules'], r'^leaderboard, main easy, not won to 10: submitted \[\[\'maffscards\''),
    ('Hard back to always best (MARVIN_BEST.hard 1)', [('var MARVIN_BEST = { easy: 0.30, hard: 0.60 };', 'var MARVIN_BEST = { easy: 0.30, hard: 1 };')],
     ['balance'], r'^balance hard: .* outside 39-53%'),
    ('Easy never best (MARVIN_BEST.easy 0)', [('var MARVIN_BEST = { easy: 0.30, hard: 0.60 };', 'var MARVIN_BEST = { easy: 0, hard: 0.60 };')],
     ['balance'], r'^balance easy: .* outside 60-74%'),
    ('the random branch choosing the best always', [('return rng() < MARVIN_BEST[level] ? hardChoice(card, pool) : easyChoice();',
                                                     'return rng() < MARVIN_BEST[level] ? hardChoice(card, pool) : hardChoice(card, pool);')],
     ['marvin'], r'^marvin (easy|hard): [\d.]+% of \d+ choices are his best category, expected'),
    ('game_completed correct true on a loss', [("correct: res.winner === 'you', questions_answered:", "correct: true, questions_answered:")],
     ['rules'], r"^game_completed, first to 10, main easy, not won to 10, marvin ten: correct True on a loss"),
    ("questions_correct counting Marvin's wins", [("questions_correct: G.wins.you,", "questions_correct: G.wins.marvin,")],
     ['rules'], r"^game_completed, .*: questions_correct \d+, expected the player's"),
    ('a detail that does not add up (ties not counted)', [("else { G.mid.push(you, mar); G.ties++; }", "else { G.mid.push(you, mar); }")],
     ['rules'], r'^game_completed, entire deck, draw at the cap: detail .* does not add up to 100 rounds played'),
]


def selftest(html):
    ok = True
    for what, edits, units, want in PLANTS:
        try:
            src = html
            for old, new in edits:
                src = pc.apply_plant(src, old, new, name=what)
        except pc.StalePlant as e:
            print('  self-test %-34s *** %s ***' % (what, e))
            ok = False
            continue
        got, err = [], None
        try:
            check(src, got, units)
        except Exception as e:  # noqa: BLE001
            err = e
        hit = [g for g in got if re.search(want, g)]
        caught = pc.is_caught(hit, err)
        print('  self-test %-34s %s' % (what, ('caught: ' + hit[0][:100]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:100] if got else '') + (' (error: %s)' % err if err else '')))
        ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    ap.add_argument('--only', nargs='*', help='run only these units: data balance rules marvin sim play fit')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    units = [] if args.selftest else (args.only or ['data', 'balance', 'rules', 'marvin', 'sim', 'play', 'fit'])
    info = check(html, out, units) if units else {}
    if 'how' in info:
        print('%s: cards.json is the data plus %d how lines, each ending on its value; %d of Marvin\'s lines equal to the contract; every set and card line reachable' % (SLUG, info['how'], info.get('lines', 0)))
    if 'pairs' in info:
        print('%s: %d judgements equal to the rule; Marvin\'s best category right for every card of both decks; one tap never plays; the cap, the leaderboard and analytics checked' % (SLUG, info['pairs']))
    for level, share, want, p in info.get('marvin', []):
        print('%s: Marvin %s (MARVIN_BEST %.2f): %.1f%% of %d choices his best category, expected %.1f%% (%.2f + %.2f x 1/6, the chance a random pick of six is the best)'
              % (SLUG, level, p, 100 * share, CHOICES, 100 * want, p, 1 - p))
    for level, rate, p in info.get('balance', []):
        lo, hi = BANDS[level]
        print('%s: a typical player (best category half the time) wins %.1f%% of %d first-to-10 games against %s Marvin (MARVIN_BEST %.2f; band %d-%d%%)'
              % (SLUG, 100 * rate, BALANCE_GAMES, level, p, 100 * lo, 100 * hi))
    if 'sims' in info:
        print('%s: %d seeded games, none with a line of Marvin\'s twice, every set and card line seen' % (SLUG, info['sims']))
    for p in info.get('played', []):
        print('%s: played by clicks against %s' % (SLUG, p))
    for f in info.get('fit', []):
        print('%s: fit %s' % (SLUG, f))
    ok = True
    if args.selftest or not args.only:
        ok = selftest(html)
    for f in out[:80]:
        print('FAIL  ' + f)
    if len(out) > 80:
        print('FAIL  ... and %d more' % (len(out) - 80))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
