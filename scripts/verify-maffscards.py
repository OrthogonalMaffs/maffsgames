#!/usr/bin/env python3
# ci-shards: MaffsCards game (games/maffscards/: every card pair on every category judged against cards.json, distance lowest; every how line ends on its value; hard Marvin's best category for every card in both decks; Marvin's share of best-category picks at easy and hard against MARVIN_BEST over 2,000 choices each; a simulated typical player's first-to-10 win rate in Jon's bands (easy 60-74%, hard 39-53%); Marvin's lines verbatim from the contract, every condition reachable, none repeated in 300 games; one tap never plays; the 100-round cap; the leaderboard only for first-to-10 wins, with the round count; game_completed's result and tally (correct, questions_answered, questions_correct, detail) for a won and a lost first-to-10 game and entire-deck games, adding up to the rounds played; full first-to-10 games against easy and hard in Chromium; the card and the reveal fit 320x568 in normal and Aa; challenge codes: encode and decode for all 8 settings over 1,003 seeds against this script's own, every single wrong character and neighbouring swap on 200 codes rejected; one key for each of Marvin's challenge decisions; two players with different strategies on one code get the same deal and the same Marvin for every (card, k) both reach, at all 8 settings; a challenge game never on the leaderboard, challenge true or false on both events, never the code; ?c= fills and never starts; normal seeded games equal to the page before challenges for 3 seeds; the challenge section and results line fit 320x568 in normal and Aa; today's deal: the date-to-code rule against this script's own for 400 days across both clock changes, the same code in two loads, main / ten / hard; every line of the pool verbatim from the contract and every number in one against cards.json; every state of the panel and every branch of the results line; never on the leaderboard, mode daily; the panel and results fit 320x568 and 375x667 in normal and Aa; the start art's three cards (96, 1, 89) equal to cards.json, each beating all 31 other main-deck cards in its category, the title in front, start screen only, no control pushed under the fold at 320x568, 375x667, 1280x720 and 1920x1080 in normal and Aa; DAILY-FIT: no unit reads the committed daily.json (a pinned not-played file); at those sizes with no result, Jon lost with the longest pool line and Jon won with a 240-character line, Play today's deal above Jon's line and above the fold where it can be, the art from 40% to full size and never smaller than the room needs; twenty-six planted faults caught) | | 3
# ci-deps: games/maffscards/ tools/maffscards/ data/maffscards.json schools/assets/firebase-leaderboard.js schools/assets/level.js schools/assets/answer-lock.js docs/handover/contracts/*2026-11-20-maffscards-game.md docs/history/contracts/*2026-11-20-maffscards-game.md docs/handover/contracts/*2026-11-25-daily-deal.md docs/history/contracts/*2026-11-25-daily-deal.md .claude/rules/game-roster.md scripts/plant_common.py
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

  challenge (MAFFSCARDS-CHALLENGE, 25 Nov 2026) "Challenge a friend": a 6-character code (5 data characters and a check
            character) carries the settings and a seed. In Chromium:
            codes: the page's encode and decode against this script's own for all 8 settings over 1,003 seeds (0, 1, the
              largest that takes all 8 settings and 1,000 drawn) and the top seed with the 7 settings that fit; every
              code 6 characters of ALPHABET; lower case and spaces round it read; wrong lengths and 0, 1, I, L, O
              rejected; on 200 codes every single wrong character (data and check) and every swap of two different
              neighbouring data characters rejected.
            streams: the 32-bit keys for 20 seeds x (the deal and all 48 cards) x 4 values of k all different;
              Marvin's challenge choice over 4,096 (seed, card, k) at each level his best as often as MARVIN_BEST
              plus chance; k changes the choice.
            fairness: for each of the 8 settings and 6 codes, the menu first set to the opposite settings, two
              scripted players at a time of three (always the first category; always the last; always the best
              on the card), each with its own rng seed:
              the code's settings, identical starting piles, and for every (Marvin card, k) both games reach, the
              same category, each equal to the page's own rule for that key; the same player twice with different
              rng seeds plays the identical game; no leaderboard call; both events carry challenge true and never
              the code; detail ends " · challenge" and adds up by this script's own judging; the results line.
            leaderboard: a rigged first-to-10 challenge win submits nothing; Play again is then a normal game with
              the same settings, challenge false, and its win is submitted.
            normal: seeded normal games (MC.seed) at 3 seeds give the deal, Marvin's choices and the whole run of
              rounds, lines and result recorded from the page before this change (main c788f401): NORMAL_GOLDEN,
              which --golden <page> prints again if cards.json or MARVIN_BEST ever changes.
            menu: ?c=CODE fills the box, sets the options and starts nothing; a bad code shows the message and starts
              nothing; Make a challenge code shows a code for the options showing and its link, the same code for
              the same rng seed; changing an option takes the made code away; Copy link copies or selects; Play it
              and Play the challenge start that code's game.
            fit (with the fit unit): the challenge section with a made code and the bad-code message, and a
              challenge game's results, inside 320x568 in normal and Aa with no sideways scroll at five sizes.

  today's deal (DAILY-DEAL, 25 Nov 2026): one deal a UK day, the same for everyone, with Jon's result beside it. Four units:
  pool      no browser: the page's dailyLines equal to THE LINE POOL in the saved contract (docs/.../2026-11-25-daily-deal.md),
            word for word, 11 won and 12 lost; every number and game name in a line held to games/maffscards/cards.json
            (POOL_FACTS: 100 once in pi's first 1,000 digits, 96's factors summing to 252, 88 as LXXXVIII, 64 a square and
            a cube, 1 with no largest prime factor, 89 once in the main deck and 8 from 81 with 100 further off, 9 = 3 x 3,
            first to 10) or to the roster (Some Thingies and Eigenvector Engine are listed games); a number in a line
            that no fact names fails.
  daily     in Chromium, twice (a device in London and one in Auckland): the day's code for 400 consecutive dates from
            25 Nov 2026 equal to this script's own rule (the date's characters through mix32, reduced to a seed, at main /
            ten / hard), all different, each reading back as main / ten / hard; the page's UK date at every half hour of
            those 400 days, and at the second each side of 23:00 and 24:00 UTC, equal to this script's own (BST from the
            last Sunday of March to the last Sunday of October, 01:00 UTC), with 15 instants written out by hand; with
            no hook, today is the UK's today; "Play today's deal" starts that day's code as a challenge game with the
            menu showing its settings, the same code and deal in both loads; a won daily game submits nothing, says so,
            sends mode 'daily' and challenge true on both events with detail ending " · challenge · daily", and never the
            code, the date, or Jon's line or rounds; Play again is today's deal again; a normal game afterwards is normal.
  dailyui   in Chromium with the page's date hook (MC.daily.setToday) and file hook (MC.daily.file): the panel above the
            Deck options with its date; "Jon hasn't played today's deal yet." for nulls, a stale date, tomorrow's date and
            every kind of invalid record; on 12 days running, won and lost with no line: the pool's line for the day
            (day number since 1 Jan 2026 modulo the pool's length, by this script's count), {N} filled in, and "Jon took
            N rounds." only when Jon won and the line lacks {N}; a Sheet line shown as plain text (markup included), at
            240 characters shown and at 241 replaced by the pool's; every branch of the results line (you won against
            Jon's more, the same and fewer rounds, Jon lost, Jon not played or stale; you lost against each). Then the
            file itself, fetched beside the page: two loads on one day show the same line, and a stale, missing,
            unreadable or failing file reads as not played with no error on screen. DAILY-POLISH (26 Nov 2026): each of
            those loads asks for daily.json once, as daily.json?t=<digits>, and no two loads ask with the same query
            string (the requests are read from the browser, not from the page), so a reload never shows a cached file.
  dailyfit  at 320x568 and 375x667, normal and Aa: the panel with a 240-character line and the rounds, with 240
            characters and no space, and not played: nothing off the screen, no sideways scroll, the button at least
            44 px, no text under 12 px, and the panel (with a line of words) no taller than the screen above the
            fold; a daily game's results with the longest results line above the fold.
  art       (MAFFSCARDS-START-ART, 25 Nov 2026) the start screen's three card tops behind the title. In Python, from
            cards.json: 96, 1 and 89 are main-deck cards and each beats all 31 others in its category (sum of factors,
            superpowers, largest prime factor), no ties. In Chromium at 320x568, 375x667, 1280x720 and 1920x1080, normal and Aa: the
            cards left to right are 96, 1, 89 with cards.json's nicknames; every number and nickname line shows (the
            topmost element at points along it is that text: not another card, the title or the bar); no card above
            the page; the title block opaque, title and subtitle 4.5:1 on it and in front of the art; aria-hidden; no
            sideways scroll; every control, the title and the subtitle above the fold with #mcArt hidden is above it with
            the art (section headings moved under the fold are reported, not failed). The rise runs once, not looping,
            and its class is gone by 1.7 s; the art is not shown in play or on the results.
            DAILY-FIT (26 Nov 2026, Amendment 1): at each size and font the panel in three states, set through the
            page's hooks: not played; Jon lost, on a day the pool gives its longest lost line; Jon won with a
            240-character line and the rounds. In each: the panel's order is the heading, the sentence, the Play
            button, then Jon's line and rounds; the art and its three cards show, at 40% to 100% of full size, height
            and cards together (read from the drawn height and width, never from --as). The art's size is judged by
            measurement, with --as set here to full size, the floor and one hundredth above the page's: Play today's
            deal and every start control a no-result day's full-size art keeps above the fold (the screen less the
            fixed footer) must be above it now wherever the floor would keep them there, and the art is no smaller
            than that needs. Play today's deal is above the fold at 375x667, and at 1280x720 and 1920x1080 in normal
            and Aa; at 320x568 and 375x667 Aa (under the fold on a no-result day too) it is no lower than with no
            result on the same day. A start control a line pushes under the fold is reported, never failed.
  pinned    open_page answers games/maffscards/daily.json with a pinned not-played file unless a unit passes its own; in
            dailyui every fetched-file case runs over a stand-in for the committed file that looks like a result for
            the day, and the page must never show it.

Plants (each must FAIL): distance judged highest-wins; a one-tap play; a repeated line of Marvin's; a submit after a
loss; Hard back to always best (MARVIN_BEST.hard 1); Easy never best (MARVIN_BEST.easy 0); the random branch choosing the
best category always; three on game_completed's tally; and for challenges: the check character ignored; Marvin's
challenge choice drawn from rng; the challenge deal shuffled from rng; the key a sum, not a hash; a challenge game
submitted to the leaderboard; a normal game drawing once more from rng; and for the start art, 89 changed to 98; and for
DAILY-FIT: Play today's deal back below Jon's line; the art's shrink switched off; open_page's default back to the
committed daily.json.
For today's deal (their own unit, dailyplants): the day's code from Math.random; a pool line changed by one word; W8's 252
changed to 250 in this script's facts table; a stale-date daily.json shown as today's; a 241-character line shown; a daily
game submitted to the leaderboard; daily.json asked for with no query string (DAILY-POLISH).

    python -X utf8 scripts/verify-maffscards.py [--selftest] [--only UNIT ...] [--shard I/K] [--list-units]

CI runs it as SHARD parts (# ci-shards; scripts/ci_shards.py): its work units are data, balance, rules, marvin, sim, play,
challenge, fit, art, pool, daily, dailyui, dailyfit and the planted faults (selftest, and dailyplants for today's deal), each in exactly one part (contract VERIFIER-SPLIT, 25 Nov 2026). With no
--shard every unit and the plants run, as before; --only runs the named units without the plants (local use).
"""
import argparse
import datetime as dt
import glob
import hashlib
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


# Challenge codes (MAFFSCARDS-CHALLENGE). TOP_SEED fits with settings 0 to 6; TOP_SEED - 1 with all 8.
ALPHABET = '23456789ABCDEFGHJKMNPQRSTUVWXYZ'
CODE_SPAN = 31 ** 5
TOP_SEED = (CODE_SPAN - 1) // 8
BAD_CODE = "That code doesn't work. Check each letter and number."
NO_BOARD = "Challenge games don't go on the leaderboard."
# index = the code's settings number: bit 1 deck, bit 2 length, bit 4 Marvin
SETTINGS = [{'deck': d, 'length': n, 'marvin': m} for m in ('easy', 'hard') for n in ('ten', 'deck') for d in ('main', 'all')]
FAIR_SEEDS = [5, 31, 1234, 271828, 1414213, 3141592]    # six codes for each of the 8 settings
# The scripted players of the fairness check: (name, strategy, the rng seed its lines draw from). The fourth is the third once more.
PLAYERS = [('always the first category', 'first', 101), ('always the last category', 'last', 202),
           ('always the best on the card', 'best', 303), ('always the best on the card, again', 'best', 404)]
# Normal seeded games as main c788f401's page (before challenges) played them; python scripts/verify-maffscards.py
# --golden <page.html> prints this again. you, mar: the starting piles; marvin: his card and choice each time he
# chose; digest: the start line, every round (cards, category, winner, line), the end line, the result and the rounds.
NORMAL_CASES = [(3, {'deck': 'main', 'length': 'ten', 'marvin': 'easy'}), (11, {'deck': 'all', 'length': 'deck', 'marvin': 'hard'}),
                (20261125, {'deck': 'main', 'length': 'deck', 'marvin': 'hard'})]
NORMAL_GOLDEN = {
    3: {'you': [94, 37, 11, 93, 1, 55, 28, 36, 53, 33, 96, 77, 17, 43, 7, 2],
        'mar': [68, 61, 51, 27, 49, 100, 89, 21, 60, 48, 74, 26, 88, 64, 46, 71],
        'marvin': '61:lpf 51:pi 49:dist 100:sof 89:pi 60:dist 48:dist 74:powers 26:pi 88:pi 46:pi 61:roman 27:dist',
        'digest': '0ae637133acc4787'},
    11: {'you': [5, 61, 46, 43, 33, 80, 2, 59, 1, 94, 87, 60, 48, 66, 36, 28, 21, 73, 100, 53, 64, 71, 88, 95],
         'mar': [7, 27, 77, 68, 34, 96, 63, 75, 17, 26, 47, 93, 19, 51, 37, 4, 13, 49, 55, 92, 11, 38, 89, 74],
         'marvin': '96:sof 63:dist 75:pi 93:sof 51:lpf 37:lpf 4:sof 49:dist 55:sof 74:pi 96:roman 80:sof 47:lpf 87:roman 19:lpf '
                   '66:sof 37:dist 36:dist 13:pi 73:dist 88:dist 33:roman 7:pi 96:sof 61:lpf 80:pi 47:lpf 46:roman 87:sof 77:roman '
                   '66:sof 75:lpf 63:lpf 89:lpf 60:sof 7:pi 4:pi 93:sof 88:roman 28:dist 96:dist 100:sof 61:lpf 55:powers 27:sof '
                   '92:sof 47:dist 64:pi 87:pi 59:lpf 74:lpf 66:sof 5:pi 36:dist 43:lpf 94:sof 13:powers',
         'digest': 'c36282aa15d8f3f3'},
    20261125: {'you': [21, 11, 7, 74, 53, 71, 60, 48, 96, 49, 33, 27, 43, 37, 26, 36],
               'mar': [17, 88, 1, 51, 100, 89, 68, 55, 46, 93, 61, 94, 77, 2, 64, 28],
               'marvin': '88:roman 1:powers 51:lpf 89:lpf 68:lpf 55:powers 46:powers 93:sof 61:lpf 94:pi 28:roman 17:powers 21:lpf 11:pi '
                         '1:pi 7:powers 100:sof 53:dist',
               'digest': 'c2624d64b3c184ea'},
}


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


def py_encode(seed, bits):
    """This script's own encoder: five base-31 data characters for seed * 8 + bits, then the check character."""
    v = seed * 8 + bits
    if not 0 <= v < CODE_SPAN:
        return None
    d = []
    for _ in range(5):
        d.insert(0, v % 31)
        v //= 31
    return ''.join(ALPHABET[x] for x in d) + ALPHABET[sum((i + 1) * x for i, x in enumerate(d)) % 31]


def py_decode(text):
    """(seed, bits), or None for a code that must be rejected."""
    code = text.strip().upper()
    if len(code) != 6 or any(ch not in ALPHABET for ch in code):
        return None
    d = [ALPHABET.index(ch) for ch in code]
    if sum((i + 1) * x for i, x in enumerate(d[:5])) % 31 != d[5]:
        return None
    v = 0
    for x in d[:5]:
        v = v * 31 + x
    return v // 8, v % 8


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
# DAILY-FIT (26 Nov 2026): no unit reads the committed games/maffscards/daily.json, which the maffscards-daily workflow
# rewrites on any day Jon plays. open_page answers the page's request for it with this pinned file unless a unit passes its
# own. PIN_DAILY is True always; one planted fault (check()'s pin=False) turns it off to prove the check for it works.
NOT_PLAYED_FILE = (200, json.dumps({'date': None, 'result': None, 'rounds': None, 'line': None}))
PIN_DAILY = True


def open_page(br, base, html, size, aa=False, still=True, fonts=False, query='?cb=verify', daily=None, tz=None, live=None, seen=None):
    """daily: (status, body) to answer games/maffscards/daily.json with; None: the pinned not-played file (never the
    committed one). live: a (status, body) standing in for the committed file, under the pin, for the check that the
    pin holds. tz: the device's time zone. seen: a list that gets the address of every request the browser makes."""
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch,
                         reduced_motion='reduce' if still else 'no-preference', **({'timezone_id': tz} if tz else {}))
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    if aa:
        ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
    bc.offline(ctx, base)
    if fonts:
        ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    file_url = re.compile(r'/games/%s/daily\.json(\?.*)?$' % SLUG)
    if live is not None:            # registered first, so the pin below (the later route runs first) covers it
        ctx.route(lambda url: bool(file_url.search(url)), lambda route: route.fulfill(
            status=live[0], content_type='application/json; charset=utf-8', body=live[1]))
    if daily is None and PIN_DAILY:
        daily = NOT_PLAYED_FILE
    if daily is not None:
        ctx.route(lambda url: bool(file_url.search(url)), lambda route: route.fulfill(
            status=daily[0], content_type='application/json; charset=utf-8', body=daily[1]))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    if seen is not None:
        page.on('request', lambda r: seen.append(r.url))
    page.goto(base + '/games/%s/%s' % (SLUG, query), wait_until='load', timeout=30000)
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


# ---------------------------------------------------------------- challenge a friend (MAFFSCARDS-CHALLENGE)
TRACE_JS = r"""([seed, settings]) => {
  MC.seed(seed); Object.keys(settings).forEach(k => MC.ui.set(k, settings[k])); MC.ui.start();
  const keys = ['sof', 'lpf', 'roman', 'dist', 'powers', 'pi'], g0 = MC.ui.game();
  const out = { you: g0.you, mar: g0.mar, marvin: [], rounds: [], start: document.getElementById('say').textContent };
  for (let i = 0; i < 3000 && MC.ui.state() !== 'over'; i++) {
    const s = MC.ui.state();
    if (s === 'choosing') { const k = keys[(seed + i) % 6]; MC.ui.tap(k); MC.ui.tap(k); }
    else if (s === 'marvin') { out.marvin.push([MC.ui.game().mar[0], MC.ui.selected()]); MC.ui.play(); }
    else if (s === 'reveal') { const r = MC.ui.last(); out.rounds.push([r.you, r.marvin, r.cat, r.winner, r.quip]); MC.ui.next(); }
  }
  const g = MC.ui.game();
  out.state = MC.ui.state(); out.end = document.getElementById('resQuip').textContent; out.result = g.result; out.round = g.round;
  return out;
}"""


def golden_of(t):
    """A normal game's trace as NORMAL_GOLDEN keeps it."""
    rest = json.dumps([t['start'], t['rounds'], t['end'], t['result'], t['round']], ensure_ascii=False, sort_keys=True)
    return {'you': t['you'], 'mar': t['mar'], 'marvin': ' '.join('%d:%s' % (n, k) for n, k in t['marvin']),
            'digest': hashlib.sha256(rest.encode('utf-8')).hexdigest()[:16]}


def check_normal(page, out, info):
    """A normal game is what it was before challenges: the same deal, the same Marvin, the same draws in the same order."""
    for seed, settings in NORMAL_CASES:
        t = page.evaluate(TRACE_JS, [seed, settings])
        got, want = golden_of(t), NORMAL_GOLDEN.get(seed)
        if t['state'] != 'over' or want is None:
            out.append('normal game, seed %d: %s' % (seed, 'no recorded game to compare with' if want is None else 'did not end'))
            continue
        for part, what in (('you', 'the player\'s starting pile'), ('mar', 'Marvin\'s starting pile'), ('marvin', 'Marvin\'s choices'),
                           ('digest', 'the run of rounds, lines and result')):
            if got[part] != want[part]:
                out.append('normal game, seed %d: %s is not what the page before challenges gave: %r, recorded %r' % (seed, what, got[part], want[part]))
                break
    info['normal'] = len(NORMAL_CASES)


def check_codes(page, out, info):
    if page.evaluate('MC.challenge.ALPHABET') != ALPHABET or len(ALPHABET) != 31 or set('01ILO') & set(ALPHABET):
        out.append('challenge codes: the page\'s ALPHABET is not the contract\'s 31 characters')
    rnd = random.Random(20261125)
    seeds = [0, 1, TOP_SEED - 1] + [rnd.randrange(TOP_SEED) for _ in range(1000)]
    pairs = [[sd, b] for sd in seeds for b in range(8)] + [[TOP_SEED, b] for b in range(7)]
    got = page.evaluate("""([pairs, settings]) => pairs.map(([sd, b]) => { const c = MC.challenge.encode(sd, settings[b]);
        return [c, c && MC.challenge.decode(c), c && MC.challenge.decode('  ' + c.toLowerCase() + ' ')]; })""", [pairs, SETTINGS])
    bad = 0
    for (sd, b), (code, back, loose) in zip(pairs, got):
        want = py_encode(sd, b)
        full = dict(SETTINGS[b], code=want, seed=sd)
        if code != want or not re.match('^[%s]{6}$' % ALPHABET, code or '') or back != full or loose != full or py_decode(want) != (sd, b):
            bad += 1
            if bad <= 5:
                out.append('challenge codes: seed %d, settings %d: the page made %r and read it back as %r (lower case, spaced: %r); expected %r and %r'
                           % (sd, b, code, back, loose, want, full))
    over = page.evaluate("""([top, settings]) => [MC.challenge.encode(top, settings[7]), MC.challenge.encode(top + 1, settings[0]),
        MC.challenge.encode(-1, settings[0]), MC.challenge.encode(1.5, settings[0]), MC.challenge.seeds]""", [TOP_SEED, SETTINGS])
    if over[:4] != [None] * 4 or over[4] != TOP_SEED:
        out.append('challenge codes: a seed that does not fit in five characters made a code, or the page draws seeds past %d: %r' % (TOP_SEED - 1, over))
    good = py_encode(123456, 5)
    wrong = ['', good[:5], good + '2', ' ', 'ABC', good[:2] + ' ' + good[2:]] + [good[:i] + ch + good[i + 1:] for i in (0, 3, 5) for ch in '01ILO']
    took = page.evaluate('a => a.map(t => MC.challenge.decode(t) !== null)', wrong) + [page.evaluate('MC.challenge.decode(null) !== null')]
    for t, yes in zip(wrong + [None], took):
        if yes:
            out.append('challenge codes: %r accepted (wrong length or a character outside ALPHABET)' % (t,))
    # one wrong character, or two different neighbouring data characters swapped: never a code
    muts = []
    for i, sd in enumerate(seeds[3:203]):
        code = py_encode(sd, i % 8)
        for pos in range(6):
            for ch in ALPHABET:
                if ch != code[pos]:
                    muts.append(('data character %d changed' % (pos + 1) if pos < 5 else 'the check character changed', code, code[:pos] + ch + code[pos + 1:]))
        for pos in range(4):
            if code[pos] != code[pos + 1]:
                muts.append(('data characters %d and %d swapped' % (pos + 1, pos + 2), code, code[:pos] + code[pos + 1] + code[pos] + code[pos + 2:]))
    took = page.evaluate('a => a.map(t => MC.challenge.decode(t) !== null)', [m[2] for m in muts])
    shown = {}
    for (kind, code, mut), yes in zip(muts, took):
        if py_decode(mut) is not None:
            out.append('challenge codes: this script\'s own decoder takes %r (%s, from %s)' % (mut, kind, code))
        if yes:
            shown[kind] = shown.get(kind, 0) + 1
            if shown[kind] <= 2:
                out.append('challenge codes: %s: %r, from %s, accepted' % (kind, mut, code))
    info['codes'] = (len(pairs), len(muts), sum(1 for m in muts if 'swapped' in m[0]))


def check_streams(page, game, out, info):
    """One key for each decision, and Marvin's challenge choice his usual rule: best as often as MARVIN_BEST, else any of six."""
    cats = {c['key']: c for c in game['categories']}
    order = [c['key'] for c in game['categories']]
    pool = [c for c in game['cards'] if c['deck'] == 'main']
    if any(c['n'] == 0 for c in game['cards']):
        out.append('challenge streams: a card is numbered 0, the number the deal\'s key uses')
    ns = [0] + [c['n'] for c in game['cards']]
    keys = page.evaluate('ns => { const o = []; for (let sd = 0; sd < 20; sd++) for (const n of ns) for (let k = 0; k < 4; k++) o.push(MC.challenge.key(sd, n, k)); return o; }', ns)
    if any(not isinstance(k, (int, float)) or k != int(k) or not 0 <= k < 2 ** 32 for k in keys):
        out.append('challenge streams: a key is not a 32-bit integer')
    elif len(set(keys)) != len(keys):
        out.append('challenge streams: %d keys for %d (seed, card, k), not all different: decisions would share a generator' % (len(set(keys)), len(keys)))
    best = {c['n']: hard_choice(cats, order, c, pool) for c in pool}
    declared = page.evaluate('MC.marvinBest')
    trios = [[sd, c['n'], k] for sd in range(64) for c in pool for k in (0, 1)]
    for level in ('easy', 'hard'):
        got = page.evaluate("([level, trios]) => trios.map(t => MC.challenge.choice(t[0], level, 'main', t[1], t[2]))", [level, trios])
        share = sum(1 for (sd, n, k), key in zip(trios, got) if key == best[n]) / len(got)
        want = declared[level] + (1 - declared[level]) / len(order)
        info.setdefault('streams', []).append((level, share, want, len(got)))
        if abs(share - want) > 0.03:
            out.append('challenge streams: Marvin %s: %.1f%% of %d challenge choices are his best category, expected %.1f%%' % (level, 100 * share, len(got), 100 * want))
        if set(got) != set(order):
            out.append('challenge streams: Marvin %s chose only %r in %d challenge choices' % (level, sorted(set(got)), len(got)))
        if level == 'easy':
            moved = sum(1 for i in range(0, len(got), 2) if got[i] != got[i + 1]) / (len(got) / 2)
            if moved < 0.5:
                out.append('challenge streams: Marvin\'s second choice with a card differs from his first only %.0f%% of the time: k does not give a new generator' % (100 * moved))


FAIR_JS = r"""([code, strategy, best, rngSeed, other]) => {
  MC.seed(rngSeed); window.__ev = []; window.__sub = [];
  Object.keys(other).forEach(k => MC.ui.set(k, other[k]));        // the menu on the opposite settings: the code's must win
  if (!MC.challenge.start(code)) return null;
  const g0 = MC.ui.game(), marvin = [], rounds = [];
  const pressed = [...document.querySelectorAll('.opt-btn[aria-pressed="true"]')].map(b => b.dataset.val);
  for (let i = 0; i < 3000 && MC.ui.state() !== 'over'; i++) {
    const s = MC.ui.state();
    if (s === 'choosing') { const k = strategy === 'first' ? 'sof' : strategy === 'last' ? 'pi' : best[MC.ui.game().you[0]]; MC.ui.tap(k); MC.ui.tap(k); }
    else if (s === 'marvin') { marvin.push([MC.ui.game().mar[0], MC.ui.selected()]); MC.ui.play(); }
    else if (s === 'reveal') { const r = MC.ui.last(); rounds.push([r.you, r.marvin, r.cat, r.winner]); MC.ui.next(); }
  }
  const g = MC.ui.game(), line = document.getElementById('chLine');
  return { challenge: g0.challenge, settings: { deck: g0.deck, length: g0.length, marvin: g0.marvin }, pressed: pressed, you: g0.you, mar: g0.mar,
    marvin: marvin, rounds: rounds, state: MC.ui.state(), result: g.result, round: g.round, ev: window.__ev, sub: window.__sub,
    chLine: line.hidden ? null : line.textContent, lbNote: document.getElementById('lbNote').textContent };
}"""


def decisions(marvin):
    """{(card, k): category}: k counted here, how many times Marvin had already chosen with that card."""
    seen, out = {}, {}
    for n, key in marvin:
        k = seen.get(n, 0)
        seen[n] = k + 1
        out[(n, k)] = key
    return out


def check_fair(page, game, out, info):
    cats = {c['key']: c for c in game['categories']}
    order = [c['key'] for c in game['categories']]
    by = {c['n']: c for c in game['cards']}
    total_shared = total_again = games = won_ten = 0
    for bits, settings in enumerate(SETTINGS):
        pool = [c for c in game['cards'] if settings['deck'] == 'all' or c['deck'] == 'main']
        best = {str(c['n']): hard_choice(cats, order, c, pool) for c in pool}
        other = SETTINGS[7 - bits]
        tag = '%s %s %s' % (settings['deck'], settings['length'], settings['marvin'])
        shared, deals, differed = 0, [], False
        for sd in FAIR_SEEDS:
            code = py_encode(sd, bits)
            played = [page.evaluate(FAIR_JS, [code, strat, best, rs, other]) for name, strat, rs in PLAYERS]
            if None in played:
                out.append('challenge fairness: code %s (%s) did not start a game' % (code, tag))
                continue
            for who, g in zip((pl[0] for pl in PLAYERS), played):
                games += 1
                what = 'challenge fairness: code %s (%s), %s' % (code, tag, who)
                if g['state'] != 'over':
                    out.append('%s: the game did not end' % what)
                    continue
                if g['challenge'] != code or g['settings'] != settings or g['pressed'] != [settings['deck'], settings['length'], settings['marvin']]:
                    out.append('%s: playing %r at %r with the menu showing %r, not the code\'s settings' % (what, g['challenge'], g['settings'], g['pressed']))
                if sorted(g['you'] + g['mar']) != sorted(x['n'] for x in pool) or len(g['you']) != len(g['mar']):
                    out.append('%s: the starting piles are not the deck dealt one each' % what)
                if g['sub']:
                    out.append('challenge leaderboard: code %s (%s), %s: submitted %r' % (code, tag, who, g['sub']))
                names = [e[0] for e in g['ev']]
                if names != ['game_started', 'game_completed'] or any(e[1].get('challenge') is not True for e in g['ev']):
                    out.append('%s: events %r, expected game_started and game_completed, each with challenge true' % (what, [(e[0], e[1].get('challenge')) for e in g['ev']]))
                elif code in json.dumps(g['ev']):
                    out.append('%s: an event carries the code itself' % what)
                else:
                    tally = {'a': 0, 'b': 0, 'tie': 0}
                    for y, m, key, winner in g['rounds']:
                        tally[judge(cats, key, by[y], by[m])] += 1
                    res = g['result']
                    outcome = {'you': 'win', 'marvin': 'loss', 'draw': 'draw'}[res['winner']]
                    line = 'you %d · Marvin %d · ties %d · %s · %s · challenge' % (tally['a'], tally['b'], tally['tie'], outcome, res['why'])
                    if g['ev'][1][1].get('detail') != line or g['ev'][1][1].get('questions_answered') != len(g['rounds']):
                        out.append('%s: game_completed detail %r over %r rounds, expected %r over %d' % (what, g['ev'][1][1].get('detail'), g['ev'][1][1].get('questions_answered'), line, len(g['rounds'])))
                    won_ten += res == {'winner': 'you', 'why': 'ten'}
                want_line = 'Challenge %s: %d rounds. Your friend plays the same deal with the same code.' % (code, len(g['rounds']))
                if g['chLine'] != want_line or g['lbNote'] != NO_BOARD:
                    out.append('%s: the results say %r and %r, expected %r and %r' % (what, g['chLine'], g['lbNote'], want_line, NO_BOARD))
                # every choice Marvin made is the page's rule for (seed, his card, k), with k counted here
                d = decisions(g['marvin'])
                trios = sorted(d)
                rule = page.evaluate('([sd, level, deck, trios]) => trios.map(t => MC.challenge.choice(sd, level, deck, t[0], t[1]))',
                                     [sd, settings['marvin'], settings['deck'], [list(t) for t in trios]])
                off = [(t, d[t], r) for t, r in zip(trios, rule) if d[t] != r]
                if off:
                    out.append('%s: Marvin with card %d (k %d) played %s, the rule for that key gives %s' % (what, off[0][0][0], off[0][0][1], off[0][1], off[0][2]))
            first, last, bestp, again = played
            for i, a in enumerate(played[:3]):         # every pair of the three different players
                for b in played[i + 1:3]:
                    if a['you'] != b['you'] or a['mar'] != b['mar']:
                        out.append('challenge fairness: code %s (%s): the two starting piles differ: %r / %r against %r / %r' % (code, tag, a['you'], a['mar'], b['you'], b['mar']))
                    da, db = decisions(a['marvin']), decisions(b['marvin'])
                    both = sorted(set(da) & set(db))
                    shared += len(both)
                    total_again += sum(1 for n, k in both if k > 0)
                    for n, k in both:
                        if da[(n, k)] != db[(n, k)]:
                            out.append('challenge fairness: code %s (%s): Marvin with card %d (k %d) played %s against one player and %s against the other' % (code, tag, n, k, da[(n, k)], db[(n, k)]))
                            break
                    differed = differed or a['rounds'] != b['rounds']
            if bestp['rounds'] != again['rounds'] or bestp['result'] != again['result'] or bestp['marvin'] != again['marvin'] or bestp['you'] != again['you']:
                out.append('challenge fairness: code %s (%s): the same player twice (rng seeds 303 and 404) did not play the same game' % (code, tag))
            deals.append((first['you'], first['mar']))
        if len(deals) == len(FAIR_SEEDS) and len({json.dumps(x) for x in deals}) != len(deals):
            out.append('challenge fairness: %s: different codes gave the same deal' % tag)
        if not differed:
            out.append('challenge fairness: %s: the strategies played the same rounds, so nothing was tested' % tag)
        if shared < 10:
            out.append('challenge fairness: %s: only %d (Marvin card, k) reached by both players over %d codes' % (tag, shared, len(FAIR_SEEDS)))
        total_shared += shared
    info['fair'] = (games, total_shared, total_again, won_ten)


def check_board(page, out, info):
    """A won first-to-10 challenge game submits nothing; Play again is a normal game, and its win is submitted."""
    code = py_encode(77, 0)
    page.evaluate("c => { MC.seed(5); MC.ui.set('deck', 'all'); window.__ev = []; window.__sub = []; MC.challenge.start(c); }", code)
    page.evaluate("MC.ui.rig([64, 1], [2, 7], 13, {you: 9, marvin: 3}, 0); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
    g = page.evaluate("""[MC.ui.state(), MC.ui.game().result, window.__sub, window.__ev, document.getElementById('lbNote').textContent,
        document.getElementById('chLine').hidden ? null : document.getElementById('chLine').textContent]""")
    if g[0] != 'over' or g[1] != {'winner': 'you', 'why': 'ten'}:
        out.append('challenge leaderboard: the rigged challenge game ended %r, not won at 10' % g[:2])
        return
    if g[2]:
        out.append('challenge leaderboard: a won first-to-10 challenge game submitted %r' % g[2])
    flags = [(e[0], e[1].get('challenge')) for e in g[3]]
    if flags != [('game_started', True), ('game_completed', True)]:
        out.append('challenge events: a challenge game sent %r, expected game_started and game_completed with challenge true' % flags)
    elif g[3][1][1].get('detail') != 'you 10 · Marvin 3 · ties 0 · win · ten · challenge' or code in json.dumps(g[3]):
        out.append('challenge events: game_completed detail %r (the code must never be sent)' % g[3][1][1].get('detail'))
    want = 'Challenge %s: 13 rounds. Your friend plays the same deal with the same code.' % code
    if g[4] != NO_BOARD or g[5] != want:
        out.append('challenge results: %r and %r, expected %r and %r' % (g[5], g[4], want, NO_BOARD))
    page.evaluate('window.__ev = []; window.__sub = []')
    page.click('#againBtn')
    n = page.evaluate("[MC.ui.state(), MC.ui.game().challenge, MC.ui.game().deck, MC.ui.game().length, MC.ui.game().marvin, window.__ev.map(e => [e[0], e[1].challenge])]")
    if n[0] not in ('choosing', 'marvin') or n[1] is not None or n[2:5] != ['main', 'ten', 'easy'] or n[5] != [['game_started', False]]:
        out.append('challenge, Play again: %r, expected a normal game at the code\'s settings with challenge false' % n)
        return
    page.evaluate("MC.ui.rig([64, 1], [2, 7], 13, {you: 9, marvin: 3}, 0); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
    g = page.evaluate("""[window.__sub, window.__ev.map(e => [e[0], e[1].challenge, e[1].detail]), document.getElementById('chLine').hidden,
        document.getElementById('lbNote').textContent]""")
    if g[0] != [['maffscards', 'main-easy', 13, 13]]:
        out.append('challenge, Play again: the normal game\'s win submitted %r, expected the main-easy score 13' % g[0])
    if g[1] != [['game_started', False, None], ['game_completed', False, 'you 10 · Marvin 3 · ties 0 · win · ten']] or not g[2] or g[3] != 'Leaderboard score: 13 rounds (fewer is better).':
        out.append('challenge, Play again: the normal game sent %r and its results say %r (challenge line hidden: %r)' % (g[1], g[3], g[2]))
    info['board'] = True


MENU_JS = r"""() => { const $ = id => document.getElementById(id), g = MC.ui.game();
  return { state: MC.ui.state(), challenge: g && g.challenge, input: $('chInput').value, msg: $('chMsg').hidden ? null : $('chMsg').textContent,
    pressed: [...document.querySelectorAll('.opt-btn[aria-pressed="true"]')].map(b => b.dataset.val),
    out: !$('chOut').hidden, code: $('chCode').textContent, link: $('chLink').value, copy: $('chCopy').textContent,
    selected: document.activeElement === $('chLink') && $('chLink').selectionStart === 0 && $('chLink').selectionEnd === $('chLink').value.length,
    started: window.__ev.filter(e => e[0] === 'game_started').length }; }"""


def check_menu(br, base, html, out, info):
    # a link: the code in the box, its settings on the menu, nothing started
    code = py_encode(424242, 7)
    ctx, page, errs = open_page(br, base, html, (390, 844), query='?c=' + code.lower())
    page.wait_for_timeout(400)
    m = page.evaluate(MENU_JS)
    if m['state'] != 'menu' or m['challenge'] is not None or m['started'] or m['input'] != code or m['pressed'] != ['all', 'deck', 'hard'] or m['msg'] is not None:
        out.append('challenge link: ?c=%s gave %r, expected the code in the box, the options all / deck / hard and no game' % (code.lower(), m))
    page.click('#chGo')
    m = page.evaluate(MENU_JS)
    if m['challenge'] != code or m['started'] != 1:
        out.append('challenge link: Play the challenge after ?c= did not start that code\'s game: %r' % m)
    out.extend('page error (challenge link): %s' % e for e in errs if 'production host' not in e)
    ctx.close()

    # a bad code, in a link and typed: the message, and nothing started
    wrong = code[:5] + ('2' if code[5] != '2' else '3')
    ctx, page, errs = open_page(br, base, html, (390, 844), query='?c=' + wrong)
    m = page.evaluate(MENU_JS)
    if m['state'] != 'menu' or m['msg'] != BAD_CODE or m['input'] != wrong or m['pressed'] != ['main', 'ten', 'easy']:
        out.append('challenge link: the bad code ?c=%s gave %r, expected the message, the default options and no game' % (wrong, m))
    for typed, key in (('ABCDE', 'click'), (wrong, 'click'), ('', 'click'), (wrong.lower(), 'Enter')):
        page.fill('#chInput', typed)
        if key == 'click':
            page.click('#chGo')
        else:
            page.press('#chInput', 'Enter')
        m = page.evaluate(MENU_JS)
        if m['state'] != 'menu' or m['msg'] != BAD_CODE or m['started'] or m['challenge'] is not None:
            out.append('challenge menu: the bad code %r (%s) gave %r, expected the message %r and no game' % (typed, key, m, BAD_CODE))
    # Make a challenge code: a code for the options showing, and its link; the same code for the same rng seed
    page.evaluate('MC.seed(7)')
    page.click('#chMake')
    m1 = page.evaluate(MENU_JS)
    page.evaluate('MC.seed(7)')
    page.click('#chMake')
    m2 = page.evaluate(MENU_JS)
    d = py_decode(m1['code'])
    if not m1['out'] or d is None or d[1] != 0 or m1['link'] != base + '/games/%s/?c=%s' % (SLUG, m1['code']) or m2['code'] != m1['code'] or m1['state'] != 'menu':
        out.append('challenge menu: Make a challenge code showed %r with the link %r (again: %r), expected one code for main / ten / easy and its link' % (m1['code'], m1['link'], m2['code']))
    page.click('.opt-btn[data-val="hard"]')
    if page.evaluate(MENU_JS)['out']:
        out.append('challenge menu: the made code stays on show after an option changed')
    page.click('#chMake')
    m = page.evaluate(MENU_JS)
    d = py_decode(m['code'])
    if d is None or d[1] != 4:
        out.append('challenge menu: a code made with Marvin on hard is %r, which reads as %r' % (m['code'], d))
    page.click('#chCopy')
    page.wait_for_timeout(300)
    c = page.evaluate(MENU_JS)
    if not (c['copy'] == 'Copied' or c['selected']):
        out.append('challenge menu: Copy link neither copied the link nor selected it: %r' % c)
    page.click('#chPlay')
    p = page.evaluate(MENU_JS)
    if p['challenge'] != m['code'] or p['started'] != 1 or p['state'] not in ('choosing', 'marvin'):
        out.append('challenge menu: Play it did not start the made code %r: %r' % (m['code'], p))
    out.extend('page error (challenge menu): %s' % e for e in errs if 'production host' not in e)
    ctx.close()

    # a typed code, lower case with a space round it: that code's game
    code = py_encode(99, 3)
    ctx, page, errs = open_page(br, base, html, (390, 844))
    page.fill('#chInput', ' ' + code.lower() + ' ')
    page.click('#chGo')
    m = page.evaluate(MENU_JS)
    if m['challenge'] != code or m['pressed'] != ['all', 'deck', 'easy'] or m['msg'] is not None or m['started'] != 1:
        out.append('challenge menu: the typed code %r gave %r, expected its game at all / deck / easy' % (code.lower(), m))
    out.extend('page error (challenge typed): %s' % e for e in errs if 'production host' not in e)
    ctx.close()
    info['menu'] = True


def check_challenge(br, base, html, game, out, info):
    ctx, page, errs = open_page(br, base, html, (1280, 800))
    for name, fn, args in (('codes', check_codes, (page, out, info)), ('streams', check_streams, (page, game, out, info)),
                           ('fairness', check_fair, (page, game, out, info)), ('leaderboard', check_board, (page, out, info)),
                           ('normal', check_normal, (page, out, info))):
        try:
            fn(*args)
        except Exception as e:  # noqa: BLE001
            out.append('challenge %s threw: %s' % (name, str(e).splitlines()[0][:200]))
    out.extend('page error (challenge): %s' % e for e in errs if 'production host' not in e)
    ctx.close()
    try:
        check_menu(br, base, html, out, info)
    except Exception as e:  # noqa: BLE001
        out.append('challenge menu threw: %s' % str(e).splitlines()[0][:200])


CH_FIT_JS = r"""() => {
  window.scrollTo(0, 0);
  const foot = document.querySelector('.site-footer');
  const fixed = foot && getComputedStyle(foot).position === 'fixed';
  const fold = innerHeight - (fixed ? foot.getBoundingClientRect().height : 0);
  const shown = e => !!e && !!e.offsetParent;
  const box = document.getElementById('chOut'), sec = document.getElementById('challenge');
  const parts = shown(sec) ? [sec, ...sec.querySelectorAll('*')].filter(shown) : [];
  const wide = parts.filter(e => { const r = e.getBoundingClientRect(); return r.left < -1 || r.right > innerWidth + 1; }).map(e => e.id || e.className || e.tagName);
  const small = parts.filter(e => /^(BUTTON|INPUT)$/.test(e.tagName) && e.getBoundingClientRect().height < 44).map(e => e.id);
  const bottom = id => { const e = document.getElementById(id); return shown(e) ? e.getBoundingClientRect().bottom + scrollY : null; };
  return { fold: fold, sideways: document.documentElement.scrollWidth > innerWidth + 1, wide: wide, small: small,
           made: shown(box) ? box.getBoundingClientRect().height : null,
           results: ['chLine', 'lbNote', 'againBtn', 'menuBtn'].map(bottom) };
}"""


def check_challenge_fit(br, base, html, out, info):
    """The challenge section (a made code, the bad-code message) and a challenge game's results on a 320x568 phone, normal and Aa."""
    code = py_encode(77, 0)
    for size in SIDEWAYS_SIZES:
        for aa in (False, True):
            tag = '%dx%d%s' % (size[0], size[1], ' Aa' if aa else '')
            ctx, page, errs = open_page(br, base, html, size, aa=aa, fonts=True)
            page.evaluate("document.fonts.ready.then(() => 0)")
            page.click('#chMake')
            page.fill('#chInput', 'WWWWWW')
            page.click('#chGo')
            f = page.evaluate(CH_FIT_JS)
            if f['sideways'] or f['wide']:
                out.append('challenge fit %s: the menu scrolls sideways or a part of the challenge section runs off the screen: %r' % (tag, f['wide']))
            if f['small']:
                out.append('challenge fit %s: a button or box under 44 px tall: %r' % (tag, f['small']))
            if f['made'] is None or page.evaluate("document.getElementById('chMsg').hidden"):
                out.append('challenge fit %s: the made code or the bad-code message is not showing' % tag)
            elif size in FIT_SIZES and f['made'] > f['fold']:
                out.append('challenge fit %s: the made code, its link and its buttons are %.0f px tall, more than the %.0f px above the fold' % (tag, f['made'], f['fold']))
            page.evaluate("c => { MC.challenge.start(c); MC.ui.rig([64, 1], [2, 7], 13, {you: 9, marvin: 3}, 0); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next(); }", code)
            r = page.evaluate(CH_FIT_JS)
            if r['sideways']:
                out.append('challenge fit %s: a challenge game\'s results scroll sideways' % tag)
            if None in r['results']:
                out.append('challenge fit %s: a part of a challenge game\'s results is not shown: %r' % (tag, r['results']))
            elif size in FIT_SIZES:
                over = max(r['results']) - r['fold']
                if over > 0:
                    out.append('challenge fit %s: a challenge game\'s results end at %.0f px, below the fold at %.0f px' % (tag, max(r['results']), r['fold']))
                info.setdefault('chfit', []).append('%s: the made code block %.0f px tall; a challenge game\'s results end %.0f px above the fold' % (tag, f['made'] or 0, -over))
            out.extend('page error (challenge fit %s): %s' % (tag, e) for e in errs if 'production host' not in e)
            ctx.close()


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


# ---------------------------------------------------------------- the start art (MAFFSCARDS-START-ART)
# Jon, 25 Nov 2026: three card tops fanned behind the title, 96, 1 and 89 left to right, each with the category in which
# it beats every other main-deck card (Project Claude's measurement, recomputed here from cards.json).
ART = [(96, 'sof'), (1, 'powers'), (89, 'lpf')]
ART_SIZES = [(320, 568), (375, 667), (1280, 720), (1920, 1080)]
# DAILY-FIT: where Play today's deal must be above the fold (the screen less the fixed footer), as (size, Aa). At the
# others (Jon's Amendment 1, 26 Nov 2026: it is under the fold there on a no-result day too) it must be no lower than on a
# no-result day.
ART_PLAY_STRICT = {((375, 667), False), ((1280, 720), False), ((1280, 720), True), ((1920, 1080), False), ((1920, 1080), True)}
ART_FLOOR = 0.4
ART_DAY = '2027-03-05'
ART_LONG_LINE = ('Marvin wants a recount, a rematch and an apology. ' * 6)[:239] + '.'
PLAY = 'Play today\u2019s deal'
# The start screen as it stands, and what the art's size does to it, all measured: the art's scale read from its drawn
# height and its cards' drawn width against their full sizes (never from --as); the bottom of Play today's deal and of
# every start control at the page's own scale, at full size, at the floor and one hundredth above the page's scale.
ART_STATE_JS = r"""() => {
  window.scrollTo(0, 0);
  const art = document.getElementById('mcArt'), foot = document.querySelector('.site-footer');
  const fold = innerHeight - (foot && getComputedStyle(foot).position === 'fixed' ? foot.getBoundingClientRect().height : 0);
  const wide = matchMedia('(min-width:640px)').matches, fullH = wide ? 30 : 64, fullW = wide ? 124 : 96;
  const els = [['Play today\u2019s deal', document.getElementById('ddPlay')]];
  document.querySelectorAll('#optDeck .opt-btn, #optLength .opt-btn, #optMarvin .opt-btn').forEach(b => els.push([b.firstChild.textContent.trim(), b]));
  els.push(['Deal the cards', document.getElementById('startBtn')]);
  const bottoms = () => { const o = {}; els.forEach(([n, e]) => { o[n] = e.getBoundingClientRect().bottom + scrollY; }); return o; };
  const card = art.querySelector('.art-card.c');
  const was = art.style.getPropertyValue('--as');
  // In CSS px: under the large-screen layer's zoom a rect is in screen px, z times larger (LARGE-SCREEN-LAYER, Amendment 1).
  const z = parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
  const scale = art.getBoundingClientRect().height / z / fullH, cardScale = card.offsetWidth / fullW;
  const o = { fold: fold, scale: scale, cardScale: cardScale, shown: art.getClientRects().length > 0 && getComputedStyle(art).visibility === 'visible' && +getComputedStyle(art).opacity > 0,
              cardsShown: [...art.querySelectorAll('.art-card')].every(c => c.offsetWidth > 0 && c.offsetHeight > 0 && c.getBoundingClientRect().top < art.getBoundingClientRect().bottom),
              status: document.getElementById('ddStatus').textContent, rounds: document.getElementById('ddRounds').hidden ? null : document.getElementById('ddRounds').textContent,
              order: [...document.querySelectorAll('#daily > *')].map(e => e.id || (e.querySelector('#ddPlay') ? 'play' : e.className || e.tagName.toLowerCase())),
              now: bottoms() };
  const at = (k) => { art.style.setProperty('--as', String(k)); return bottoms(); };
  o.full = at(1); o.floor = at(0.4); o.more = at(Math.min(1, Math.round(scale * 100 + 1) / 100));
  if (was) art.style.setProperty('--as', was); else art.style.removeProperty('--as');
  return o;
}"""
ART_JS = r"""() => {
  const art = document.getElementById('mcArt'), head = document.querySelector('#menu .header');
  if (!art || !head) return { missing: true };
  art.style.pointerEvents = 'auto';               // elementFromPoint skips pointer-events: none; restored below
  // A point shows the text only if the topmost element there is that text (not another card, the title or the bar).
  const shows = (el) => {
    const r = el.getBoundingClientRect(), pts = [];
    const rg = document.createRange(); rg.selectNodeContents(el);
    for (const b of rg.getClientRects()) for (const fx of [0.3, 0.5, 0.7]) pts.push([b.left + b.width * fx, b.top + b.height / 2]);
    const hidden = pts.filter(([x, y]) => { const t = document.elementFromPoint(x, y); return !t || (t !== el && !el.contains(t)); });
    return { n: pts.length, hidden: hidden.map(p => p.map(Math.round)), top: r.top, bottom: r.bottom };
  };
  const cards = [...art.querySelectorAll('.art-card')].map(c => {
    const r = c.getBoundingClientRect(), num = c.querySelector('.art-num'), nick = c.querySelector('.art-nick');
    return { x: (r.left + r.right) / 2, top: r.top, num: num ? num.textContent : null, nick: nick ? nick.textContent : null,
             numShows: num ? shows(num) : null, nickShows: nick ? shows(nick) : null };
  });
  const hr = head.getBoundingClientRect(), h1 = head.querySelector('h1'), sub = head.querySelector('.sub');
  art.style.pointerEvents = '';
  const at = (el) => { const r = el.getBoundingClientRect(), t = document.elementFromPoint((r.left + r.right) / 2, (r.top + r.bottom) / 2); return !!t && (t === el || el.contains(t)); };
  return { inMenu: !!art.closest('#menu'), aria: art.getAttribute('aria-hidden'), shown: art.getClientRects().length > 0,
           cards: cards, headTop: hr.top, bg: getComputedStyle(head).backgroundColor,
           h1: getComputedStyle(h1).color, sub: getComputedStyle(sub).color, h1Front: at(h1), subFront: at(sub),
           sideways: document.documentElement.scrollWidth > innerWidth + 1 };
}"""
# The start screen's controls, title and subtitle (kind 'c'): any above the fold without the art must stay above it with
# the art. Section headings and labels (kind 'h') are reported when they move under the fold, not failed: running text
# always crosses the fold when anything is added above it, and a heading whose buttons are already below is that kind.
ART_FOLD_JS = r"""() => {
  const out = {};
  const name = (e, i) => (e.id ? '#' + e.id : e.tagName.toLowerCase() + (e.className ? '.' + String(e.className).split(' ')[0] : '')) + ' ' + i;
  [['c', '.topbar a, .topbar button, #menu h1, #menu .sub, #menu button, #menu input, #menu a'], ['h', '#menu .mode-h, #menu .ch-lab']].forEach(([kind, sel]) => {
    document.querySelectorAll(sel).forEach((e, i) => {
      const r = e.getBoundingClientRect();
      if (r.height > 0) out[kind + ' ' + name(e, i) + (e.id ? '' : ' "' + e.textContent.trim().slice(0, 24) + '"')] = r.bottom;
    });
  });
  return { fold: innerHeight, bottoms: out };
}"""


def _rgb(c):
    m = re.match(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)', c)
    return (float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)) if m.group(4) else 1.0) if m else None


def _contrast(a, b):
    def lum(c):
        ch = [v / 255 for v in c[:3]]
        ch = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_art(br, base, html, game, out, info):
    """The start art: its cards equal cards.json's, each unbeatable in its category (recomputed here), the title in front,
    on the start screen only, aria-hidden, and nothing above the fold pushed below it at ART_SIZES, normal and Aa."""
    cats = {c['key']: c for c in game['categories']}
    main = [c for c in game['cards'] if c['deck'] == 'main']
    if len(main) != 32:
        out.append('art: the main deck has %d cards, not 32' % len(main))
    for n, key in ART:
        card = next((c for c in main if c['n'] == n), None)
        if card is None:
            out.append('art: %d is not in the main deck' % n)
            continue
        others = [o for o in main if o is not card]
        not_beaten = [o['n'] for o in others if judge(cats, key, card, o) != 'a']
        if not_beaten:
            out.append('art: %d on %s does not beat %s (it must beat all %d others, no ties)' % (n, key, not_beaten, len(others)))
        info.setdefault('art', []).append('%d beats all %d other main-deck cards on %s (%s)' % (n, len(others), cats[key]['label'], measure(cats, card, key)))
    want = [(n, next(c['nickname'] for c in game['cards'] if c['n'] == n)) for n, _ in ART]
    # DAILY-FIT: the three states of the panel. Lost: the pool's longest lost line, on a day the page's rule picks it.
    pool = (daily_pool() or ({'won': [], 'lost': []}, {}))[0]
    longest = max(pool['lost'] or [''], key=len)
    lost_day = next((d.isoformat() for d in (DAILY_START + dt.timedelta(days=i) for i in range(DAILY_DAYS)) if pool['lost'] and pool_line(pool, 'lost', d.isoformat()) == longest), None)
    if lost_day is None:
        out.append('art: no day in %d on which the pool gives its longest lost line' % DAILY_DAYS)
        lost_day = ART_DAY
    states = [('not played', ART_DAY, None, NOT_PLAYED, None),
              ('Jon lost, the longest pool line', lost_day, {'date': lost_day, 'result': 'lost', 'rounds': 19, 'line': None}, longest.replace('{N}', '19'), None),
              ('Jon won, a 240-character line', ART_DAY, {'date': ART_DAY, 'result': 'won', 'rounds': 100, 'line': ART_LONG_LINE}, ART_LONG_LINE, 'Jon took 100 rounds.')]
    frames = "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
    for size in ART_SIZES:
        for aa in (False, True):
            tag = '%dx%d%s' % (size[0], size[1], ' Aa' if aa else '')
            ctx, page, errs = open_page(br, base, html, size, aa=aa, fonts=True)
            page.evaluate('MC.daily.ready')
            page.evaluate("document.fonts.ready.then(() => 0)")
            base_above = None
            for what, day, file, status, rounds in states:
                # The no-result panel on this state's own day first (a longer date can wrap the panel's heading).
                page.evaluate('([o, d]) => { MC.daily.setToday(d); MC.daily.file(o); }', [None, day])
                page.evaluate(frames)
                base_play = page.evaluate(ART_STATE_JS)['now'][PLAY]
                page.evaluate('([o, d]) => { MC.daily.setToday(d); MC.daily.file(o); }', [file, day])
                page.evaluate(frames)
                st = page.evaluate(ART_STATE_JS)
                t = 'art %s, %s' % (tag, what)
                fold = st['fold']
                up = lambda b: b <= fold + 0.5
                if st['status'] != status or st['rounds'] != rounds:
                    out.append('%s: the panel reads %r and %r, not the state under test' % (t, st['status'][:40], st['rounds']))
                    continue
                if st['order'] != ['mode-h', 'p', 'play', 'ddStatus', 'ddRounds']:
                    out.append("%s: the panel's order is %s, expected the heading, the sentence, the Play button, then Jon's line and rounds" % (t, st['order']))
                if not st['shown'] or not st['cardsShown']:
                    out.append('%s: the art or one of its cards is not showing' % t)
                if st['scale'] < ART_FLOOR - 0.005 or st['cardScale'] < ART_FLOOR - 0.005 or st['scale'] > 1.005 or abs(st['scale'] - st['cardScale']) > 0.02:
                    out.append('%s: the art is at %.0f%% of its height and its cards at %.0f%% of their width (together, from %d%% to 100%%)' % (t, 100 * st['scale'], 100 * st['cardScale'], 100 * ART_FLOOR))
                if base_above is None:              # the no-result day: what its full-size art keeps above the fold
                    base_above = [k for k, b in st['full'].items() if up(b) and k != PLAY]
                # What the art answers for: Play today's deal and the no-result day's controls, where the floor would keep them.
                keep = [k for k in base_above + [PLAY] if up(st['floor'][k])]
                lost_now = [k for k in keep if not up(st['now'][k])]
                if lost_now:
                    out.append('%s: with the art at %.0f%%, under the fold though a smaller art would keep it above: %s' % (t, 100 * st['scale'], ', '.join('%s (%.0f px under)' % (k, st['now'][k] - fold) for k in lost_now)))
                elif st['scale'] < 0.995 and all(up(st['more'][k]) for k in keep):
                    out.append('%s: the art is at %.0f%% though one hundredth more keeps everything it answers for above the fold' % (t, 100 * st['scale']))
                play = st['now'][PLAY]
                if (size, aa) in ART_PLAY_STRICT:
                    if not up(play):
                        out.append("%s: Play today's deal ends at %.0f px, %.0f px under the fold at %.0f px" % (t, play, play - fold, fold))
                elif play > base_play + 0.5:
                    out.append("%s: Play today's deal ends at %.0f px, lower than on a no-result day (%.0f px)" % (t, play, base_play))
                under = ['%s %.0f px' % (k, st['now'][k] - fold) for k in base_above if not up(st['now'][k])]
                if file is None and under:
                    out.append('%s: above the fold with a full-size art, under it now: %s' % (t, ', '.join(under)))
                info.setdefault('artstates', []).append("%s: art %.0f%%; Play today's deal %s%s" % (
                    t, 100 * st['scale'], ('%.0f px above the fold' % max(0, fold - play)) if up(play) else ('%.0f px under the fold' % (play - fold)),
                    ('; REPORTED, under the fold because of the line: ' + ', '.join(under)) if under else ''))
            page.evaluate('([o, d]) => { MC.daily.setToday(d); MC.daily.file(o); }', [None, ART_DAY])
            page.evaluate(frames)
            if page.evaluate(ART_STATE_JS)['scale'] < 0.9:
                out.append('art %s: the art is under 90%% of its size on a no-result day' % tag)
            a = page.evaluate(ART_JS)
            if a.get('missing'):
                out.append('art %s: no #mcArt or no title block on the start screen' % tag)
                ctx.close()
                continue
            got = [(c['num'], c['nick']) for c in sorted(a['cards'], key=lambda c: c['x'])]
            if got != [(str(n), k) for n, k in want]:
                out.append('art: the numbers left to right are %r, not cards.json\'s %r (%s)' % (got, [(str(n), k) for n, k in want], tag))
            if not a['inMenu'] or a['aria'] != 'true' or not a['shown']:
                out.append('art %s: not shown on the start screen, or not aria-hidden="true" (in the menu %s, aria-hidden %r)' % (tag, a['inMenu'], a['aria']))
            for c in a['cards']:
                for part in ('numShows', 'nickShows'):
                    sh = c[part]
                    if sh is None or sh['hidden']:
                        out.append('art %s: card %s\'s %s is covered at %r' % (tag, c['num'], 'number' if part == 'numShows' else 'nickname', sh and sh['hidden']))
                if c['top'] < 0:
                    out.append('art %s: card %s starts above the page (%.0f px)' % (tag, c['num'], c['top']))
            bg, h1, sub = _rgb(a['bg']), _rgb(a['h1']), _rgb(a['sub'])
            if not bg or bg[3] < 1:
                out.append('art %s: the title block is not solid (background %s)' % (tag, a['bg']))
            else:
                for what, col in (('title', h1), ('subtitle', sub)):
                    if _contrast(col, bg) < 4.5:
                        out.append('art %s: the %s is %.2f:1 on the title block, under 4.5:1' % (tag, what, _contrast(col, bg)))
            if not (a['h1Front'] and a['subFront']):
                out.append('art %s: the title or subtitle is not in front of the art' % tag)
            if a['sideways']:
                out.append('art %s: the start screen scrolls sideways' % tag)
            with_art = page.evaluate(ART_FOLD_JS)
            page.add_style_tag(content='#mcArt{display:none!important}')
            without = page.evaluate(ART_FOLD_JS)
            fold = with_art['fold']
            pushed = [k for k, b in without['bottoms'].items() if b <= fold + 0.5 and with_art['bottoms'].get(k, 1e9) > fold + 0.5]
            if [k for k in pushed if k.startswith('c ')]:
                out.append('art %s: above the fold without the art, below it with the art: %s' % (tag, ', '.join(k[2:] for k in pushed if k.startswith('c '))))
            above = [k for k, b in without['bottoms'].items() if b <= fold + 0.5 and k.startswith('c ')]
            h1 = [k for k in without['bottoms'] if k.startswith('c h1 ')][0]
            info.setdefault('artfit', []).append('%s: the title %.0f px lower; the lowest control above the fold ends %.0f px above it without the art, %.0f px with it%s'
                                                 % (tag, with_art['bottoms'][h1] - without['bottoms'][h1],
                                                    fold - max([without['bottoms'][k] for k in above] or [0]),
                                                    fold - max([with_art['bottoms'].get(k, 1e9) for k in above] or [0]),
                                                    ''.join('; heading now under the fold: ' + k[2:] for k in pushed if k.startswith('h '))))
            out.extend('page error (art %s): %s' % (tag, e) for e in errs if 'production host' not in e)
            ctx.close()
    # The start screen only: not in play, not on the results. And the rise runs once (motion allowed), never looping.
    ctx, page, errs = open_page(br, base, html, (390, 844), still=False)
    anim = page.evaluate("() => { const c = document.querySelector('#mcArt .art-card'); const s = getComputedStyle(c); return [s.animationName, s.animationIterationCount]; }")
    if anim[0] != 'none' and anim[1] != '1':
        out.append('art: the rise animation repeats (%s, iteration count %s)' % tuple(anim))
    page.wait_for_timeout(1700)
    if page.evaluate("document.getElementById('mcArt').classList.contains('rise')"):
        out.append('art: the rise class is still on after 1.7 s, so the rise would replay when the menu shows again')
    out.extend('page error (art rise): %s' % e for e in errs if 'production host' not in e)
    ctx.close()
    ctx, page, errs = open_page(br, base, html, (390, 844))
    page.evaluate("MC.seed(2); MC.ui.start()")
    if page.evaluate("document.getElementById('mcArt').getClientRects().length > 0"):
        out.append('art: shown during play')
    page.evaluate("MC.ui.rig([64, 5], [2], 30, {you: 9, marvin: 9}); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
    if not page.evaluate("document.getElementById('results').classList.contains('active')"):
        out.append('art: the rigged game did not reach the results')
    elif page.evaluate("document.getElementById('mcArt').getClientRects().length > 0"):
        out.append('art: shown on the results')
    out.extend('page error (art screens): %s' % e for e in errs if 'production host' not in e)
    ctx.close()


# ---------------------------------------------------------------- today's deal (DAILY-DEAL, 25 Nov 2026)
DAILY_CONTRACT = '2026-11-25-daily-deal.md'
ROSTER = os.path.join(ROOT, '.claude', 'rules', 'game-roster.md')
DAILY_BITS = 4                       # main deck, first to 10, Marvin hard: the settings number of every day's code
DAILY_START = dt.date(2026, 11, 25)  # 400 days from here take in the clock changes of 28 March and 31 October 2027
DAILY_DAYS = 400
LINE_MAX = 240
NOT_PLAYED = "Jon hasn't played today's deal yet."
DAILY_SIZES = [(320, 568), (375, 667)]
DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# Instants whose UK date is known without any rule (written out by hand): GMT days end at 24:00 UTC, BST days at 23:00 UTC.
UK_ANCHORS = [('2027-01-10T23:59:59', '2027-01-10'), ('2027-01-11T00:00:00', '2027-01-11'), ('2027-03-27T23:30:00', '2027-03-27'),
              ('2027-03-28T00:59:59', '2027-03-28'), ('2027-03-28T22:59:59', '2027-03-28'), ('2027-03-28T23:00:00', '2027-03-29'),
              ('2027-06-01T22:59:59', '2027-06-01'), ('2027-06-01T23:00:00', '2027-06-02'), ('2027-10-30T23:00:00', '2027-10-31'),
              ('2027-10-31T00:59:59', '2027-10-31'), ('2027-10-31T23:00:00', '2027-10-31'), ('2027-10-31T23:59:59', '2027-10-31'),
              ('2027-11-01T00:00:00', '2027-11-01'), ('2026-12-31T23:59:59', '2026-12-31'), ('2027-01-01T00:00:00', '2027-01-01')]
# Every number and every game name in the pool, as (the line, the words that state it, the kind of fact, its values).
# check_pool holds each to games/maffscards/cards.json (or the roster, or arithmetic), and fails a line that holds a
# number no fact covers. {N} is Jon's round count, filled in by the page.
POOL_FACTS = [
    ('W2', '9 should be a prime number', 'not prime', (9, 3, 3)),
    ('W5', 'an extra 89 card', 'once in the main deck', (89,)),
    ('W6', 'Some Thingies', 'roster', ('Some Thingies',)),
    ('W7', '100 appears only once', 'card', (100, 'pi', 1)),
    ('W7', 'the first 1,000 digits of pi', 'pi digits', (1000,)),
    ('W8', "96's factors add up to 252", 'card', (96, 'sof', 252)),
    ('W9', 'LXXXVIII', 'card', (88, 'roman', 'LXXXVIII')),
    ('W10', '64. Being a square AND a cube', 'powers', (64, ('square', 'cube'))),
    ('W11', "1's largest prime factor. There isn't one", 'card', (1, 'lpf', 0)),
    ('L3', 'Marvin 10', 'first to', (10,)),
    ('L7', 'Eigenvector Engine', 'roster', ('Eigenvector Engine',)),
    ('L10', '89 being exactly 8 from the nearest square', 'distance', (89, 8, 81, 100)),
    ('L11', 'the first 1,000 digits of pi', 'pi digits', (1000,)),
]


def mix32(h):
    """The page's 32-bit hash step (the murmur3 finaliser), in this script's own arithmetic."""
    h &= 0xFFFFFFFF
    h ^= h >> 16
    h = (h * 0x85EBCA6B) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xC2B2AE35) & 0xFFFFFFFF
    return h ^ (h >> 16)


def py_day_code(date):
    """The day's code by this script's own rule: the date's characters chained through mix32, reduced to a seed that takes all 8 settings."""
    h = 0
    for ch in date:
        h = mix32(h + ord(ch))
    return py_encode(h % (CODE_SPAN // 8), DAILY_BITS)


def uk_date(now):
    """The UK calendar date at a UTC datetime, with no time zone database: BST from 01:00 UTC on the last Sunday of March
    to 01:00 UTC on the last Sunday of October."""
    def last_sunday(month):
        d = dt.date(now.year, month, 31)
        return dt.datetime.combine(d - dt.timedelta(days=(d.weekday() + 1) % 7), dt.time(1))
    return (now + dt.timedelta(hours=1 if last_sunday(3) <= now < last_sunday(10) else 0)).date()


def ms_of(now):
    return int((now - dt.datetime(1970, 1, 1)).total_seconds() * 1000)


def day_label(date):
    d = dt.date.fromisoformat(date)
    return '%s %d %s' % (DAY_NAMES[d.weekday()], d.day, MONTH_NAMES[d.month - 1])


def daily_pool():
    """THE LINE POOL from the saved contract: ({'won': [...], 'lost': [...]}, {'W1': text, ...}), or None with no file."""
    for d in ('docs/handover/contracts', 'docs/history/contracts'):
        for f in glob.glob(os.path.join(ROOT, d, '*' + DAILY_CONTRACT)):
            pool, by = {'won': [], 'lost': []}, {}
            for line in open(f, encoding='utf-8').read().split('\n'):
                m = re.match(r'^([WL])(\d+) (.+)$', line)
                if m:
                    lines = pool['won' if m.group(1) == 'W' else 'lost']
                    lines.append(m.group(3))
                    by[m.group(1) + m.group(2)] = m.group(3)
                    if int(m.group(2)) != len(lines):
                        return {'won': [], 'lost': []}, {}          # not numbered 1, 2, 3...: not the pool
            return pool, by
    return None


def page_daily_lines(html):
    m = re.search(r'<script type="application/json" id="dailyLines">(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None


def pool_line(pool, result, date):
    """The pool's line for a result on a date: the day number since 1 January 2026, modulo the pool's length."""
    n = (dt.date.fromisoformat(date) - dt.date(2026, 1, 1)).days
    return pool[result][n % len(pool[result])]


def listed_games():
    """Names of the roster's listed games: every numbered row above the Unlisted section."""
    names, listed = set(), True
    for line in open(ROSTER, encoding='utf-8').read().split('\n'):
        if line.startswith('## '):
            listed = not re.match(r'## (Unlisted|Withdrawn)\b', line)
        m = re.match(r'^\| \d+ \| ([^|]+?) \| `[a-z0-9-]+` \|', line)
        if m and listed:
            names.add(m.group(1))
    return names


def check_pool(html, out, info, facts=None):
    """The page's dailyLines against the contract, word for word; every number and game name in a line against the cards."""
    facts = POOL_FACTS if facts is None else facts
    got, want = page_daily_lines(html), daily_pool()
    if want is None:
        out.append('daily pool: the contract file *%s is not in docs/handover/contracts/ or docs/history/contracts/' % DAILY_CONTRACT)
        return
    pool, by = want
    if len(pool['won']) != 11 or len(pool['lost']) != 12:
        out.append('daily pool: the contract holds %d won and %d lost lines, not 11 and 12' % (len(pool['won']), len(pool['lost'])))
    if got is None:
        out.append('daily pool: the page has no dailyLines block')
        return
    if sorted(got) != ['lost', 'won']:
        out.append('daily pool: dailyLines holds %r, not won and lost' % sorted(got))
    for result in ('won', 'lost'):
        mine = got.get(result) or []
        if len(mine) != len(pool[result]):
            out.append('daily pool: %d %s lines in the page, %d in the contract' % (len(mine), result, len(pool[result])))
        for i, (a, b) in enumerate(zip(mine, pool[result])):
            if a != b:
                out.append("daily pool: %s line %d is not the contract's: %r, the contract's %r" % (result, i + 1, a, b))
    game = load(CARDS)
    cards = {c['n']: c for c in game['cards']}
    main = [c['n'] for c in game['cards'] if c['deck'] == 'main']
    listed = listed_games()
    for lid, words, kind, v in facts:
        line = by.get(lid)
        if line is None or words not in line:
            out.append('daily pool: %s: the line does not say %r: %r' % (lid, words, line))
            continue
        why = None
        if kind == 'card':
            n, key, val = v
            if n not in main or cards[n][key] != val:
                why = 'cards.json gives %d %s %r, not %r (main deck: %s)' % (n, key, cards.get(n, {}).get(key), val, n in main)
        elif kind == 'powers':
            n, names = v
            if n not in main or not set(names) <= set(cards[n]['powers']) or round(n ** 0.5) ** 2 != n or round(n ** (1 / 3)) ** 3 != n:
                why = 'cards.json gives %d the superpowers %r, the line needs %r' % (n, cards.get(n, {}).get('powers'), list(names))
        elif kind == 'once in the main deck':
            if main.count(v[0]) != 1:
                why = '%d is in the main deck %d times, not once' % (v[0], main.count(v[0]))
        elif kind == 'distance':
            n, d, below, above = v
            lo = int(n ** 0.5) ** 2
            hi = (int(n ** 0.5) + 1) ** 2
            if (lo, hi) != (below, above) or n - lo != d or not n - lo < hi - n or cards.get(n, {}).get('dist') != d:
                why = '%d lies between the squares %d and %d, %d and %d away; cards.json gives its distance as %r, the line says %d' % (
                    n, lo, hi, n - lo, hi - n, cards.get(n, {}).get('dist'), d)
        elif kind == 'not prime':
            n, a, b = v
            if a * b != n or not 1 < a < n:
                why = '%d is not %d x %d' % (n, a, b)
        elif kind == 'pi digits':
            if game.get('pi_decimals') != v[0]:
                why = "cards.json counts in pi's first %r digits, not %d" % (game.get('pi_decimals'), v[0])
        elif kind == 'first to':
            if not re.search(r"var SLUG = 'maffscards', TEN = %d," % v[0], html):
                why = 'the page does not play first to %d' % v[0]
        elif kind == 'roster':
            if v[0] not in listed:
                why = '%r is not the roster name of a listed game' % v[0]
        else:
            why = 'no rule for a %r fact' % kind
        if why:
            out.append('daily pool: %s: %r does not hold: %s' % (lid, words, why))
    # no number in any line without a fact that names it
    for lid, line in sorted(by.items()):
        said = ' '.join(f[1] for f in facts if f[0] == lid)
        for num in re.findall(r'\d+(?:,\d{3})*', line):
            if not re.search(r'(?<![\d,])%s(?![\d,])' % re.escape(num), said):
                out.append('daily pool: %s holds the number %s and no fact in this script checks it' % (lid, num))
    info['pool'] = (len(got.get('won') or []), len(got.get('lost') or []), len(facts))


DAILY_PLAY_JS = r"""([date, piles, round, wins, ties]) => {
  MC.seed(9); window.__ev = []; window.__sub = [];
  MC.daily.setToday(date);
  MC.ui.set('deck', 'all'); MC.ui.set('length', 'deck'); MC.ui.set('marvin', 'easy');     // the opposite settings: the deal's must win
  document.getElementById('ddPlay').click();
  const g0 = MC.ui.game(), daily = MC.daily.playing();
  const pressed = [...document.querySelectorAll('.opt-btn[aria-pressed="true"]')].map(b => b.dataset.val);
  if (!g0) return null;
  MC.ui.rig(piles[0], piles[1], round, wins, ties); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next();
  const $ = id => document.getElementById(id), g = MC.ui.game();
  return { code: g0.challenge, daily: daily, pressed: pressed, you: g0.you, mar: g0.mar, settings: [g0.deck, g0.length, g0.marvin],
    state: MC.ui.state(), result: g.result, round: g.round, ev: window.__ev, sub: window.__sub,
    line: $('chLine').hidden ? null : $('chLine').textContent, lbNote: $('lbNote').textContent, marks: $('chLine').children.length };
}"""
# A daily game won in round 13 (64's sum of factors, 127, beats 2's 3) and one lost in round 15.
WIN_13 = [[[64, 1], [2, 7]], 13, {'you': 9, 'marvin': 3}, 0]
LOSS_15 = [[[2, 1], [64, 7]], 15, {'you': 3, 'marvin': 9}, 2]


def check_daily(br, base, html, game, out, info):
    """The date-to-code rule, the same code in two loads, the code's settings; off the board; analytics."""
    dates = [(DAILY_START + dt.timedelta(days=i)).isoformat() for i in range(DAILY_DAYS)]
    want = [py_day_code(d) for d in dates]
    if None in want or len(set(want)) != len(want) or any(py_decode(c)[1] != DAILY_BITS for c in want if c):
        out.append("daily rule: this script's own codes for %d days are not %d different main / ten / hard codes" % (DAILY_DAYS, DAILY_DAYS))
    # every half hour of the 400 days, and the second each side of 23:00 and 24:00 UTC (UK midnight in summer and winter)
    start = dt.datetime.combine(DAILY_START, dt.time(0))
    stamps = [start + dt.timedelta(minutes=30 * i) for i in range(DAILY_DAYS * 48)]
    for i in range(DAILY_DAYS):
        day = start + dt.timedelta(days=i)
        stamps += [day + dt.timedelta(hours=23) - dt.timedelta(seconds=1), day + dt.timedelta(hours=23),
                   day + dt.timedelta(hours=24) - dt.timedelta(seconds=1)]
    anchors = [(dt.datetime.fromisoformat(s), d) for s, d in UK_ANCHORS]
    for when, d in anchors:
        if uk_date(when).isoformat() != d:
            out.append("daily rule: this script's own UK date at %s UTC is %s, not %s" % (when.isoformat(), uk_date(when), d))
    loads = []
    for tz, rng_seed in (('Europe/London', 1), ('Pacific/Auckland', 2)):
        ctx, page, errs = open_page(br, base, html, (1280, 800), tz=tz)
        page.evaluate('MC.daily.ready')
        tag = 'daily rule (a device in %s)' % tz
        got = page.evaluate('ds => ds.map(d => MC.daily.code(d))', dates)
        bad = [(d, g, w) for d, g, w in zip(dates, got, want) if g != w]
        for d, g, w in bad[:3]:
            out.append("%s: the code for %s is %r, this script's own rule gives %r" % (tag, d, g, w))
        if len(set(got)) != len(got):
            out.append('%s: %d days share a code with another day' % (tag, len(got) - len(set(got))))
        back = page.evaluate('cs => cs.map(c => { const d = MC.challenge.decode(c); return d && [d.deck, d.length, d.marvin].join(" "); })', got)
        if set(back) != {'main ten hard'}:
            out.append('%s: a day\'s code does not read back as main / ten / hard: %r' % (tag, sorted(set(str(b) for b in back))[:3]))
        at = page.evaluate('ms => ms.map(m => MC.daily.at(m))', [ms_of(s) for s in stamps])
        off = [(s, a) for s, a in zip(stamps, at) if a != uk_date(s).isoformat()]
        for s, a in off[:3]:
            out.append('%s: at %s UTC the page says the UK date is %s, it is %s' % (tag, s.isoformat(), a, uk_date(s)))
        hand = page.evaluate('ms => ms.map(m => MC.daily.at(m))', [ms_of(w) for w, d in anchors])
        for (w, d), a in zip(anchors, hand):
            if a != d:
                out.append('%s: at %s UTC the page says the UK date is %s, it is %s' % (tag, w.isoformat(), a, d))
        # no hook: today is the UK's today (read either side of the page's own reading, in case midnight falls between)
        before = uk_date(dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)).isoformat()
        today = page.evaluate('MC.daily.today()')
        if today not in (before, uk_date(dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)).isoformat()):
            out.append('%s: with no hook the page\'s today is %s, the UK date is %s' % (tag, today, before))
        # the button plays the day's code, as a challenge, with the deal's settings on the menu; off the board; analytics
        day = dates[7]
        page.evaluate("o => MC.daily.file(o)", {'date': day, 'result': 'won', 'rounds': 77, 'line': 'Zebra crossing, Marvin.'})
        g = page.evaluate(DAILY_PLAY_JS, [day] + WIN_13)
        loads.append(g)
        if g is None or g['code'] != py_day_code(day) or not g['daily'] or g['settings'] != ['main', 'ten', 'hard'] or g['pressed'] != ['main', 'ten', 'hard']:
            out.append("%s: Play today's deal on %s started %r, expected the day's code %s as a daily game at main / ten / hard with the menu showing it"
                       % (tag, day, g and [g['code'], g['daily'], g['settings'], g['pressed']], py_day_code(day)))
        if g is None:
            ctx.close()
            continue
        if g['state'] != 'over' or g['result'] != {'winner': 'you', 'why': 'ten'}:
            out.append('daily board: the rigged daily game ended %r, not won at 10' % [g['state'], g['result']])
        if g['sub']:
            out.append('daily board: a won daily game submitted %r to the leaderboard' % g['sub'])
        if g['lbNote'] != NO_BOARD:
            out.append('daily board: the leaderboard note reads %r, expected %r' % (g['lbNote'], NO_BOARD))
        sent = [(e[0], e[1].get('mode'), e[1].get('challenge')) for e in g['ev']]
        detail = 'you 10 · Marvin 3 · ties 0 · win · ten · challenge · daily'
        if sent != [('game_started', 'daily', True), ('game_completed', 'daily', True)]:
            out.append("daily analytics: a daily game sent %r, expected game_started and game_completed with mode 'daily' and challenge true" % sent)
        elif g['ev'][1][1].get('detail') != detail or g['ev'][1][1].get('level') != 'main-hard':
            out.append('daily analytics: game_completed detail %r on level %r, expected %r on main-hard' % (g['ev'][1][1].get('detail'), g['ev'][1][1].get('level'), detail))
        dumped = json.dumps(g['ev'], ensure_ascii=False)
        for what, secret in (('the code', g['code'] or '?'), ('the date', day), ("Jon's line", 'Zebra'), ("Jon's rounds", '77')):
            if secret in dumped:
                out.append('daily analytics: an event carries %s (%s)' % (what, secret))
        # Play again: today's deal again, the same code and the same deal
        page.evaluate('window.__ev = []; window.__sub = []')
        page.click('#againBtn')
        n = page.evaluate("[MC.ui.state(), MC.ui.game().challenge, MC.daily.playing(), MC.ui.game().you, window.__ev.map(e => [e[0], e[1].mode, e[1].challenge])]")
        if n[0] not in ('choosing', 'marvin') or n[1] != py_day_code(day) or not n[2] or n[3] != g['you'] or n[4] != [['game_started', 'daily', True]]:
            out.append("daily, Play again: %r, expected today's deal again (%s, the same piles, mode 'daily')" % (n, py_day_code(day)))
        # and a normal game afterwards is a normal game: its own modes, challenge false, on the board
        page.evaluate("MC.ui.next(); window.__ev = []; window.__sub = []; MC.ui.set('deck', 'main'); MC.ui.set('length', 'ten'); MC.ui.set('marvin', 'easy'); MC.ui.start();"
                      " MC.ui.rig([64, 1], [2, 7], 13, {you: 9, marvin: 3}, 0); MC.ui.tap('sof'); MC.ui.tap('sof'); MC.ui.next()")
        n = page.evaluate("[MC.daily.playing(), window.__sub, window.__ev.map(e => [e[0], e[1].mode, e[1].challenge, e[1].detail || null])]")
        if n != [False, [['maffscards', 'main-easy', 13, 13]], [['game_started', 'first-to-10', False, None],
                                                              ['game_completed', 'first-to-10', False, 'you 10 · Marvin 3 · ties 0 · win · ten']]]:
            out.append('daily, a normal game afterwards: %r, expected a first-to-10 game with challenge false and its score submitted' % n)
        out.extend('page error (%s): %s' % (tag, e) for e in errs if 'production host' not in e)
        ctx.close()
    if len(loads) == 2 and None not in loads and (loads[0]['code'] != loads[1]['code'] or loads[0]['you'] != loads[1]['you'] or loads[0]['mar'] != loads[1]['mar']):
        out.append('daily rule: two page loads on the same date gave different codes or deals: %r and %r' % (loads[0]['code'], loads[1]['code']))
    info['daily'] = (len(dates), len(stamps))


STATUS_JS = r"""() => { const $ = id => document.getElementById(id);
  return { date: $('ddDate').textContent, status: $('ddStatus').textContent, rounds: $('ddRounds').hidden ? null : $('ddRounds').textContent,
           marks: $('ddStatus').children.length + $('ddRounds').children.length, button: $('ddPlay').textContent,
           shown: !!$('daily').offsetParent, above: !!($('daily').compareDocumentPosition($('optDeck')) & Node.DOCUMENT_POSITION_FOLLOWING) }; }"""


def check_daily_ui(br, base, html, out, info):
    """Every state of the panel and every branch of a daily game's results line, with the page's clock hook."""
    want = daily_pool()
    if not want or not want[0]['won'] or not want[0]['lost']:
        out.append('daily status: no line pool in the contract file to check against')
        return
    pool = want[0]
    today = '2027-03-05'
    ctx, page, errs = open_page(br, base, html, (1280, 800))
    page.evaluate('MC.daily.ready')

    def panel(file, date=today):
        return page.evaluate('([o, d]) => { MC.daily.setToday(d); MC.daily.file(o); return (%s)(); }' % STATUS_JS, [file, date])

    def expect(what, got, status, rounds):
        if got['status'] != status or got['rounds'] != rounds or got['marks']:
            out.append('daily status, %s: the panel says %r and %r (%d elements inside), expected %r and %r as plain text'
                       % (what, got['status'], got['rounds'], got['marks'], status, rounds))

    first = panel(None)
    if not first['shown'] or not first['above'] or first['button'] != "Play today's deal" or first['date'] != day_label(today):
        out.append("daily status: the panel is not above the Deck options with the date %r and the button \"Play today's deal\": %r" % (day_label(today), first))
    for date in ('2026-11-26', '2027-01-01', '2027-02-28', '2028-02-29', '2027-10-31'):
        got = panel(None, date)['date']
        if got != day_label(date):
            out.append('daily status: on %s the panel\'s date reads %r, expected %r' % (date, got, day_label(date)))
    won = {'date': today, 'result': 'won', 'rounds': 14, 'line': None}
    lost = {'date': today, 'result': 'lost', 'rounds': 31, 'line': None}
    # not played: nulls, a stale date, tomorrow's, and every kind of invalid content
    idle = [('all nulls', {'date': None, 'result': None, 'rounds': None, 'line': None}), ('no file contents', None),
            ("a stale date (yesterday's result)", dict(won, date='2027-03-04')), ("tomorrow's date", dict(won, date='2027-03-06')),
            ('a stale date with a line', dict(lost, date='2026-03-05', line='Old news.')), ('no date', dict(won, date=None)),
            ('a result that is neither won nor lost', dict(won, result='drew')), ('no result', dict(won, result=None)),
            ('rounds as text', dict(won, rounds='14')), ('rounds not whole', dict(won, rounds=14.5)), ('no rounds', dict(won, rounds=None)),
            ('a win in 9 rounds', dict(won, rounds=9)), ('a win in 101 rounds', dict(won, rounds=101)), ('a loss in 201 rounds', dict(lost, rounds=201)),
            ('a list, not a record', [today, 'won', 14, None]), ('a string, not a record', 'won'), ('a number, not a record', 14)]
    for what, file in idle:
        expect('not played, %s' % what, panel(file), NOT_PLAYED, None)
    # won and lost with no line, on 12 days running (every line of both pools): the pool's line for the day, {N} filled in,
    # and "Jon took N rounds." only when Jon won and the line does not say it
    seen = set()
    for i in range(12):
        date = (dt.date.fromisoformat(today) + dt.timedelta(days=i)).isoformat()
        for rec in (won, lost):
            raw = pool_line(pool, rec['result'], date)
            seen.add(raw)
            text = raw.replace('{N}', str(rec['rounds']))
            took = 'Jon took %d rounds.' % rec['rounds'] if rec['result'] == 'won' and '{N}' not in raw else None
            got = panel(dict(rec, date=date), date)
            expect('%s with no line on %s (the pool line %r)' % (rec['result'], date, raw[:40]), got, text, took)
            if '{N}' in got['status']:
                out.append('daily status, %s on %s: {N} is left in the line: %r' % (rec['result'], date, got['status']))
    if len(seen) != len(pool['won']) + len(pool['lost']):
        out.append('daily status: 12 days running showed %d different pool lines, not all %d' % (len(seen), len(pool['won']) + len(pool['lost'])))
    if not any('{N}' in t for t in pool['won']) or all('{N}' in t for t in pool['won']):
        out.append('daily status: the won pool does not hold lines both with and without {N}, so one branch is untested')
    # a line from the Sheet
    fallback_won, fallback_lost = pool_line(pool, 'won', today), pool_line(pool, 'lost', today)
    took14 = None if '{N}' in fallback_won else 'Jon took 14 rounds.'
    fb_won = fallback_won.replace('{N}', '14')
    long240 = ('Marvin is sulking. ' * 13)[:LINE_MAX - 1] + '.'
    cases = [('won with a Sheet line', dict(won, line='Beat that, Marvin.'), 'Beat that, Marvin.', 'Jon took 14 rounds.'),
             ('won with a Sheet line holding {N}', dict(won, line='I took {N}. Beat {N}.'), 'I took 14. Beat 14.', None),
             ('won with a Sheet line with spaces round it', dict(won, line='  Beat that.  '), 'Beat that.', 'Jon took 14 rounds.'),
             ('won with a Sheet line of markup', dict(won, line='<b>Bold</b> <img src=x onerror=alert(1)> & co'), '<b>Bold</b> <img src=x onerror=alert(1)> & co', 'Jon took 14 rounds.'),
             ('won with a 240-character line', dict(won, line=long240), long240, 'Jon took 14 rounds.'),
             ('won with a 241-character line (the pool line shown)', dict(won, line=long240 + '!'), fb_won, took14),
             ('won with an empty line', dict(won, line=''), fb_won, took14),
             ('won with a line of spaces', dict(won, line='   '), fb_won, took14),
             ('won with a line that is a number', dict(won, line=7), fb_won, took14),
             ('lost with a Sheet line', dict(lost, line='A tactical loss in {N}.'), 'A tactical loss in 31.', None),
             ('lost with a 241-character line (the pool line shown)', dict(lost, line='x' * (LINE_MAX + 1)), fallback_lost.replace('{N}', '31'), None),
             ('lost with no line', lost, fallback_lost.replace('{N}', '31'), None)]
    if len(long240) != LINE_MAX:
        out.append('daily status: the test line is %d characters, not %d' % (len(long240), LINE_MAX))
    for what, file, status, rounds in cases:
        expect(what, panel(file), status, rounds)

    # the results line of a daily game: every branch
    jon_won = lambda n: dict(won, rounds=n)                      # noqa: E731
    branches = [
        ('you won in 13, Jon in 14', WIN_13, jon_won(14), 'You took 13 rounds. Jon took 14: you beat him.'),
        ('you won in 13, Jon in 13', WIN_13, jon_won(13), 'You took 13 rounds. Jon took 13: you matched him.'),
        ('you won in 13, Jon in 12', WIN_13, jon_won(12), 'You took 13 rounds. Jon took 12: he beat you.'),
        ('you won in 13, Jon lost', WIN_13, lost, 'You took 13 rounds. Jon lost to Marvin today. You did what Jon could not.'),
        ('you won in 13, Jon has not played', WIN_13, None, 'You took 13 rounds. ' + NOT_PLAYED),
        ("you won in 13, Jon's result is yesterday's", WIN_13, dict(jon_won(12), date='2027-03-04'), 'You took 13 rounds. ' + NOT_PLAYED),
        ('you lost, Jon lost', LOSS_15, lost, 'Marvin beat you too.'),
        ('you lost, Jon won', LOSS_15, jon_won(14), 'Marvin won this time.'),
        ('you lost, Jon has not played', LOSS_15, None, 'Marvin won this time. ' + NOT_PLAYED),
    ]
    for what, rig, file, line in branches:
        page.evaluate('o => MC.daily.file(o)', file)
        g = page.evaluate(DAILY_PLAY_JS, [today] + rig)
        if g is None or g['state'] != 'over' or not g['daily']:
            out.append('daily results, %s: the daily game did not start or did not end' % what)
        elif g['line'] != line or g['marks']:
            out.append('daily results, %s: the results line reads %r, expected %r as plain text' % (what, g['line'], line))
        page.evaluate("document.getElementById('menuBtn').click()")
    out.extend('page error (daily status): %s' % e for e in errs if 'production host' not in e)
    ctx.close()

    # the file itself, fetched beside the page: two loads on one day show the same line; missing and unreadable files are "not played"
    day = '2027-07-19'
    body = json.dumps({'date': day, 'result': 'lost', 'rounds': 22, 'line': None})
    line = pool_line(pool, 'lost', day)
    files = [('the file for today, first load', (200, body), 'Europe/London', line),
             ('the file for today, a second load on another device', (200, body), 'America/Los_Angeles', line),
             ("the file with a Sheet line", (200, json.dumps({'date': day, 'result': 'won', 'rounds': 12, 'line': 'Twelve. Beat it.'})), None, 'Twelve. Beat it.'),
             ("yesterday's file, a stale date", (200, body.replace(day, '2027-07-18')), None, NOT_PLAYED),
             ('a missing file', (404, 'Not found'), None, NOT_PLAYED),
             ('a file that is not JSON', (200, '{"date": "%s", "result": "lost"' % day), None, NOT_PLAYED),
             ('an empty file', (200, ''), None, NOT_PLAYED),
             ('a server error', (500, body), None, NOT_PLAYED),
             ("open_page's pinned file, all nulls", None, None, NOT_PLAYED)]
    asked = []                      # DAILY-POLISH: the query string each load asked for daily.json with
    for what, daily, tz, status in files:
        # Under every one, a stand-in for the committed file that looks like today's result: it must never reach the page.
        seen = []
        ctx, page, errs = open_page(br, base, html, (390, 844), daily=daily, tz=tz, live=(200, json.dumps({'date': day, 'result': 'lost', 'rounds': 19, 'line': 'THE COMMITTED FILE'})), seen=seen)
        page.evaluate('MC.daily.ready')
        reqs = [u.split('/games/%s/' % SLUG, 1)[1] for u in seen if re.search(r'/games/%s/daily\.json' % SLUG, u)]
        if len(reqs) != 1 or not re.fullmatch(r'daily\.json\?t=[0-9]+', reqs[0]):
            out.append('daily request, %s: the page asked for %r, expected daily.json?t=<digits> once, so that a reload never shows a cached file' % (what, reqs))
        else:
            asked.append(reqs[0])
        got = page.evaluate('d => { MC.daily.setToday(d); return (%s)(); }' % STATUS_JS, day)
        if got['status'] == 'THE COMMITTED FILE':
            out.append('daily status, %s: the page read the committed daily.json, not the file this script pins' % what)
        elif got['status'] != status or page.evaluate("!document.getElementById('loadMsg').hidden"):
            out.append('daily status, %s: the panel says %r, expected %r and no error on screen' % (what, got['status'], status))
        if not page.evaluate("document.getElementById('startBtn').disabled === false && document.getElementById('ddPlay').disabled === false"):
            out.append('daily status, %s: a start button is disabled' % what)
        out.extend('page error (daily status, %s): %s' % (what, e) for e in errs if 'production host' not in e)
        ctx.close()
    if len(asked) == len(files) and len(set(asked)) != len(asked):
        out.append('daily request: %d loads asked for daily.json with only %d different query strings: %r' % (len(asked), len(set(asked)), asked))
    info['dailyui'] = (len(idle), 24 + len(cases), len(branches), len(files))


DAILY_FIT_JS = r"""() => {
  window.scrollTo(0, 0);
  const foot = document.querySelector('.site-footer');
  const fixed = foot && getComputedStyle(foot).position === 'fixed';
  const fold = innerHeight - (fixed ? foot.getBoundingClientRect().height : 0);
  const shown = e => !!e && !!e.offsetParent;
  const sec = document.getElementById('daily');
  const parts = shown(sec) ? [sec, ...sec.querySelectorAll('*')].filter(shown) : [];
  const wide = parts.filter(e => { const r = e.getBoundingClientRect(); return r.left < -1 || r.right > innerWidth + 1; }).map(e => e.id || e.className || e.tagName);
  const small = parts.filter(e => e.tagName === 'BUTTON' && e.getBoundingClientRect().height < 44).map(e => e.id);
  const tiny = parts.filter(e => e.children.length === 0 && e.textContent.trim() && parseFloat(getComputedStyle(e).fontSize) < 12).map(e => e.id || e.tagName);
  const bottom = id => { const e = document.getElementById(id); return shown(e) ? e.getBoundingClientRect().bottom + scrollY : null; };
  return { fold: fold, sideways: document.documentElement.scrollWidth > innerWidth + 1, wide: wide, small: small, tiny: tiny,
           panel: shown(sec) ? sec.getBoundingClientRect().height : null, results: ['chLine', 'lbNote', 'againBtn', 'menuBtn'].map(bottom) };
}"""


def check_daily_fit(br, base, html, out, info):
    """The panel with the longest lines it can show, and a daily game's results with the longest results line, on small phones."""
    lines = page_lines(html) or {}
    day = '2027-03-05'
    long_words = ('Marvin wants a recount, a rematch and an apology. ' * 6)[:LINE_MAX - 1] + '.'
    files = [('a 240-character line and the rounds', {'date': day, 'result': 'won', 'rounds': 100, 'line': long_words}),
             ('240 characters with no space', {'date': day, 'result': 'won', 'rounds': 100, 'line': 'W' * LINE_MAX}),
             ('not played', None)]
    for size in DAILY_SIZES:
        for aa in (False, True):
            tag = '%dx%d%s' % (size[0], size[1], ' Aa' if aa else '')
            ctx, page, errs = open_page(br, base, html, size, aa=aa, fonts=True)
            page.evaluate('MC.daily.ready')
            page.evaluate("document.fonts.ready.then(() => 0)")
            tallest = 0
            for what, file in files:
                page.evaluate('([o, d]) => { MC.daily.setToday(d); MC.daily.file(o); }', [file, day])
                f = page.evaluate(DAILY_FIT_JS)
                if f['panel'] is None:
                    out.append('daily fit %s, %s: the panel is not showing' % (tag, what))
                    continue
                if f['sideways'] or f['wide']:
                    out.append('daily fit %s, %s: the menu scrolls sideways or a part of the panel runs off the screen: %r' % (tag, what, f['wide']))
                if f['small']:
                    out.append('daily fit %s, %s: a button under 44 px tall: %r' % (tag, what, f['small']))
                if f['tiny']:
                    out.append('daily fit %s, %s: text under 12 px: %r' % (tag, what, f['tiny']))
                if f['panel'] > f['fold'] and ' ' in ((file or {}).get('line') or ' '):      # a line of words; one unbroken word need only wrap
                    out.append('daily fit %s, %s: the panel is %.0f px tall, more than the %.0f px above the fold' % (tag, what, f['panel'], f['fold']))
                tallest = max(tallest, f['panel'] if ' ' in ((file or {}).get('line') or ' ') else 0)
            # the results: the longest results line, the longer of Marvin's end lines, both buttons above the fold
            page.evaluate('o => MC.daily.file(o)', {'date': day, 'result': 'lost', 'rounds': 200, 'line': None})
            g = page.evaluate(DAILY_PLAY_JS, [day, [[64, 1], [2, 7]], 100, {'you': 9, 'marvin': 80}, 10])
            want = 'You took 100 rounds. Jon lost to Marvin today. You did what Jon could not.'
            if g is None or g['line'] != want:
                out.append('daily fit %s: the daily game\'s results line is %r, expected the longest, %r' % (tag, g and g['line'], want))
            page.evaluate("t => { const q = document.getElementById('resQuip'); q.hidden = false; q.innerHTML = '<span class=\"who\">Marvin:</span> ' + t; }",
                          max(lines.get('playerWins') or [''], key=len))
            r = page.evaluate(DAILY_FIT_JS)
            if r['sideways']:
                out.append('daily fit %s: a daily game\'s results scroll sideways' % tag)
            if None in r['results']:
                out.append('daily fit %s: a part of a daily game\'s results is not shown: %r' % (tag, r['results']))
            else:
                over = max(r['results']) - r['fold']
                if over > 0:
                    out.append('daily fit %s: a daily game\'s results end at %.0f px, below the fold at %.0f px' % (tag, max(r['results']), r['fold']))
                info.setdefault('dailyfit', []).append('%s: the panel at most %.0f px tall; a daily game\'s results end %.0f px above the fold' % (tag, tallest, -over))
            out.extend('page error (daily fit %s): %s' % (tag, e) for e in errs if 'production host' not in e)
            ctx.close()


# ---------------------------------------------------------------- run
def check(html, out, units, facts=None, pin=True):
    """pin=False (one planted fault only): open_page's default goes back to the committed daily.json."""
    global PIN_DAILY
    PIN_DAILY = pin
    try:
        return _check(html, out, units, facts)
    finally:
        PIN_DAILY = True


def _check(html, out, units, facts=None):
    info = {}
    game = load(CARDS)
    if 'pool' in units:
        check_pool(html, out, info, facts)
    if 'data' in units:
        check_data(html, out, info)
    if 'balance' in units:
        try:
            check_balance(html, out, info)
        except Exception as e:  # noqa: BLE001
            out.append('balance threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u not in ('data', 'balance', 'pool')]
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
                if 'challenge' in browser:
                    guarded('challenge', check_challenge, br, base, html, game, out, info)
                if 'fit' in browser:
                    guarded('fit', check_fit, br, base, html, game, out, info)
                    guarded('challenge fit', check_challenge_fit, br, base, html, out, info)
                if 'art' in browser:
                    guarded('art', check_art, br, base, html, game, out, info)
                if 'daily' in browser:
                    guarded('daily', check_daily, br, base, html, game, out, info)
                if 'dailyui' in browser:
                    guarded('daily status', check_daily_ui, br, base, html, out, info)
                if 'dailyfit' in browser:
                    guarded('daily fit', check_daily_fit, br, base, html, out, info)
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
    # MAFFSCARDS-CHALLENGE
    ('the check character ignored', [("if (chCheck(d) !== d[5]) return null;", "if (false) return null;")],
     ['challenge'], r'^challenge codes: .* accepted$'),
    ("Marvin's challenge choice drawn from rng", [("var gen = seeded(chKey(seed, card.n, k));", "var gen = rng;")],
     ['challenge'], r'^challenge fairness: .* played \w+ against one player and \w+ against the other$'),
    ('the challenge deal shuffled from rng', [("cards = ch ? shuffleBy(pool.slice(), seeded(chKey(ch.seed, 0, 0))) : shuffle(pool.slice());", "cards = shuffle(pool.slice());")],
     ['challenge'], r'^challenge fairness: .* the two starting piles differ'),
    ('the challenge key a sum, not a hash', [("return mix32(mix32(mix32(seed + 0x9E3779B9 | 0) + n | 0) + k | 0);", "return (seed + n + k) >>> 0;")],
     ['challenge'], r'^challenge streams: \d+ keys for \d+ \(seed, card, k\), not all different'),
    ('a challenge game submitted to the leaderboard', [("    if (G.challenge) return null;\n", "")],
     ['challenge'], r'^challenge leaderboard: a won first-to-10 challenge game submitted'),
    ('a normal game drawing once more from rng', [("function marvinChoice(level, card, pool) { return rng()", "function marvinChoice(level, card, pool) { rng(); return rng()")],
     ['challenge'], r'^normal game, seed \d+: '),
    # MAFFSCARDS-START-ART
    ('a start-art card number changed (89 to 98)', [('<span class="art-num">89</span>', '<span class="art-num">98</span>')],
     ['art'], r"^art: the numbers left to right are "),
    # DAILY-FIT
    ("Play today's deal back below Jon's line",
     [("""        <div class="ch-row"><button class="btn solid" id="ddPlay" type="button">Play today's deal</button></div>
        <p class="dd-status" id="ddStatus">Jon hasn't played today's deal yet.</p>
        <p id="ddRounds" hidden></p>
""", """        <p class="dd-status" id="ddStatus">Jon hasn't played today's deal yet.</p>
        <p id="ddRounds" hidden></p>
        <div class="ch-row"><button class="btn solid" id="ddPlay" type="button">Play today's deal</button></div>
""")],
     ['art'], r"^art 375x667, Jon won, a 240-character line: Play today's deal ends at \d+ px, \d+ px under the fold"),
    ("the art's shrink switched off",
     [("    function size(k) { art.style.setProperty('--as', String(k / 100)); }", "    function size(k) { art.style.setProperty('--as', '1'); }")],
     ['art'], r"^art 1280x720, Jon won, a 240-character line: with the art at 100%, under the fold though a smaller art would keep it above"),
    ("open_page's default back to the committed daily.json", [],
     ['dailyui'], r"^daily status, open_page's pinned file, all nulls: the page read the committed daily.json", {'pin': False}),
]
# DAILY-DEAL: the unit "dailyplants". A fifth item is passed to check(): W8's fact is planted in this script's table, not the page.
DAILY_PLANTS = [
    ("the day's code from Math.random", [("return h % CH_SEEDS; }", "return Math.floor(Math.random() * CH_SEEDS); }")],
     ['daily'], r"^daily rule \(a device in [\w/]+\): the code for \d{4}-\d\d-\d\d is "),
    ('a pool line changed by one word', [("Marvin has requested a recount. Can you take fewer?", "Marvin has demanded a recount. Can you take fewer?")],
     ['pool'], r"^daily pool: won line 4 is not the contract's"),
    ("W8's 252 changed to 250 in the facts table", [],
     ['pool'], r"^daily pool: W8: the line does not say \"96's factors add up to 250\"",
     {'facts': [("W8", "96's factors add up to 250", 'card', (96, 'sof', 250)) if f[0] == 'W8' else f for f in POOL_FACTS]}),
    ("a stale-date daily.json shown as today's", [("if (!d || typeof d !== 'object' || d.date !== today) return null;", "if (!d || typeof d !== 'object') return null;")],
     ['dailyui'], r"^daily status, not played, a stale date \(yesterday's result\): "),
    ('a 241-character line shown', [("j.line.length <= DAILY_LINE_MAX ?", "j.line.length <= DAILY_LINE_MAX + 1 ?")],
     ['dailyui'], r'^daily status, won with a 241-character line \(the pool line shown\): '),
    ('a daily game submitted to the leaderboard', [("challenge: ch ? ch.code : null, seed:", "challenge: ch && !daily ? ch.code : null, seed:")],
     ['daily'], r'^daily board: a won daily game submitted '),
    # DAILY-POLISH
    ('daily.json asked for with no query string', [("x.open('GET', 'daily.json?t=' + Date.now());", "x.open('GET', 'daily.json');")],
     ['dailyui'], r"^daily request, the file for today, first load: the page asked for \['daily\.json'\], expected daily\.json\?t=<digits> once"),
]


def selftest(html, plants=None):
    ok = True
    for plant in (PLANTS if plants is None else plants):
        what, edits, units, want = plant[:4]
        opts = plant[4] if len(plant) > 4 else {}
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
            check(src, got, units, **opts)
        except Exception as e:  # noqa: BLE001
            err = e
        hit = [g for g in got if re.search(want, g)]
        caught = pc.is_caught(hit, err)
        print('  self-test %-34s %s' % (what, ('caught: ' + hit[0][:100]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:100] if got else '') + (' (error: %s)' % err if err else '')))
        ok = caught and ok
    return ok


def print_golden(html):
    """NORMAL_GOLDEN as the given page plays NORMAL_CASES: for recording it again after a change to the deck or MARVIN_BEST."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            ctx, page, errs = open_page(br, base, html, (1280, 800))
            print('NORMAL_GOLDEN = {')
            for seed, settings in NORMAL_CASES:
                g = golden_of(page.evaluate(TRACE_JS, [seed, settings]))
                print('    %d: {%s},' % (seed, ',\n        '.join('%r: %r' % (k, g[k]) for k in ('you', 'mar', 'marvin', 'digest'))))
            print('}')
            br.close()
    finally:
        proc.terminate()
    return 0


# The work units, in run order (contract VERIFIER-SPLIT, 25 Nov 2026): CI runs them as SHARD parts (scripts/ci_shards.py),
# each unit in exactly one part; the planted faults are the last unit, "selftest". A local run with no --shard runs them all.
UNITS = ['data', 'balance', 'rules', 'marvin', 'sim', 'play', 'challenge', 'fit', 'art', 'pool', 'daily', 'dailyui', 'dailyfit']
PLANT_UNITS = ['selftest', 'dailyplants']       # the planted faults: the first twenty, and today's deal's seven


def merge_info(info, part):
    """One unit's findings into the run's: lists extended, the rest set (no two units write the same scalar key)."""
    for k, v in part.items():
        if isinstance(v, list) and isinstance(info.get(k), list):
            info[k].extend(v)
        else:
            info[k] = v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    ap.add_argument('--only', nargs='*', help='run only these units (local use; no plants): ' + ' '.join(UNITS))
    ap.add_argument('--golden', metavar='PAGE', help='print NORMAL_GOLDEN as this page (an index.html) plays the normal seeded games')
    bc.shard_args(ap)
    args = ap.parse_args()
    if args.golden:
        return print_golden(open(args.golden, encoding='utf-8').read())
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    shard = bc.Shard(__file__, args)
    mine = shard.pick(UNITS + PLANT_UNITS)
    plan = PLANT_UNITS if args.selftest else (list(args.only) if args.only else mine)
    html = open(GAME, encoding='utf-8').read()
    out = []
    info = {}
    for uid in plan:
        if uid in PLANT_UNITS:
            continue
        with shard.unit(uid):
            merge_info(info, check(html, out, [uid]))
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
    if 'codes' in info:
        print('%s: challenge codes: %d (seed, settings) made and read back equal to this script\'s own; %d wrong codes rejected (every single wrong character, and %d neighbouring swaps)'
              % ((SLUG,) + info['codes']))
    for level, share, want, n in info.get('streams', []):
        print('%s: challenge Marvin %s: %.1f%% of %d choices his best category, expected %.1f%%' % (SLUG, level, 100 * share, n, 100 * want))
    if 'fair' in info:
        print('%s: challenge fairness: %d games at 8 settings x %d codes; %d times two players reached the same (Marvin card, k), every one the same category (%d with k above 0); %d won to 10, none submitted'
              % (SLUG, info['fair'][0], len(FAIR_SEEDS), info['fair'][1], info['fair'][2], info['fair'][3]))
    if 'normal' in info:
        print('%s: %d normal seeded games equal to the page before challenges (deal, Marvin\'s choices, every round and line)' % (SLUG, info['normal']))
    if info.get('menu'):
        print('%s: challenge menu: ?c= fills and never starts; bad codes show the message; a made code, its link, Copy link, Play it and a typed code checked' % SLUG)
    for f in info.get('chfit', []):
        print('%s: challenge fit %s' % (SLUG, f))
    for f in info.get('art', []):
        print('%s: start art: %s' % (SLUG, f))
    for f in info.get('artstates', []):
        print('%s: start %s' % (SLUG, f))
    for f in info.get('artfit', []):
        print('%s: start art fit %s' % (SLUG, f))
    if 'pool' in info:
        print('%s: today\'s deal: %d won and %d lost lines equal to the contract; %d facts in them hold against cards.json and the roster; no number unchecked' % ((SLUG,) + info['pool']))
    if 'daily' in info:
        print('%s: today\'s deal: the code for %d days equal to this script\'s own rule, all different, all main / ten / hard; the UK date right at %d instants across both clock changes; two loads the same; off the leaderboard; mode daily'
              % ((SLUG,) + info['daily']))
    if 'dailyui' in info:
        print('%s: today\'s deal: %d not-played records, %d won and lost panels, %d results lines and %d files as fetched, each as the contract words it; each of those loads asked for daily.json?t= with its own query string' % ((SLUG,) + info['dailyui']))
    for f in info.get('dailyfit', []):
        print('%s: today\'s deal fit %s' % (SLUG, f))
    ok = True
    if 'selftest' in plan:
        with shard.unit('selftest'):
            ok = selftest(html)
    if 'dailyplants' in plan:
        with shard.unit('dailyplants'):
            ok = selftest(html, DAILY_PLANTS) and ok
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
