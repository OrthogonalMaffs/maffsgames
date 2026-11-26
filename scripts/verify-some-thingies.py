#!/usr/bin/env python3
# ci-shards: Some Thingies (the thingies' accessories by colour, a medal in pro, nothing moving under reduced motion; the start screen's crowd, the conga line and Sarge never pushing Start or Next below the fold; the winner crowd growing and never scoring, every thingy drawn (CROWD-FILL: 16 px until the screen is full, then shrinking to fit, never under 6 px, nothing above it moving, the cheer by its size, the count on the results screen; at 1280x720, 1904x864 and 375x667 in both looks); Stage 4's thingy in glasses reacting beside every question and each fact drawn as plates only after marking, a plates of b, shrunk or dropped so Next stays above the fold and the crowd keeps its size (SOME-THINGIES-FACTS: all 192 items at 320x568, 375x667 and 1280x720, both looks, normal and Aa); the character beside the question, Sarge and the thingy in glasses, one measured size from 48 to 96 px beside the question where the room allows, else the top row at 22 px, the same before and after marking, never costing the fold, the fact picture or the crowd, the largest that fits (SOME-THINGIES-HOST: every Stage 3 and 4 item at 320x568, 375x667, 1366x768 and 1920x955, both looks, normal and Aa); Stage 3 drawn as thingies coloured by column with gaps after the 5th, fitting 360 px; the scaffold fading 3, 2, 1 steps, never scoring; winner stays on: at least 10, then to the first wrong or End; the bank's SHA-256 and counts against the contract's and the generator's; all 369 items recomputed: groups x each, the sum's terms, rows x cols, a x b, product / b; every decoy distinct and never the answer, no decoy sum with the answer's total, no groups decoy equal to the groups; the fragment never sent or stored; in both looks every item on screen with its picture counted, every option marked by dataset.val alone, right and wrong, one LINES string then the worked maths; the array turned round after marking; the greeting for each fragment; read aloud on local voices only against a mocked speechSynthesis; every item of every mode and stage above the fold at 360x640 in both looks, speaker showing, as question 1 and 11 (arrays also 5 and 8): every control at every step, then Next after every right-answer line and every decoy (fit_common's sweep, nothing sampled); every mode and stage played in both looks at 360x640, the largest picture, array and sum fitting 360 px; one board submission on stage-N or pro-stage-N, no payload naming the look; fault-injection self-test) | | 1
# ci-deps: games/some-thingies/ tools/some-thingies/
r"""Independent verification for Some Thingies (games/some-thingies/), contract SOME-THINGIES, 21 Nov 2026.
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 369 items made by tools/some-thingies/bank.py (the contract's generator, saved byte for
byte). This script never uses the page's numbers to check the page's numbers:

  Bank      the page's items, written one a line as json.dumps(item, separators=(",", ":")) with a newline after each,
            have the SHA-256 the contract states, and so does the generator's own output. Counts main 22/28/36/96, pro
            23/30/38/96 (369); ids unique. Every answer recomputed here: groups x each (Stage 1 and Stage 2 adding,
            whose sum is groups terms, each equal to each); answer_sum is each, groups times; rows x cols; a x b;
            product / b (a whole number). Every number item has 3 decoys, distinct, positive, none the answer; every
            groups-to-sum item 3 decoy sums, distinct, none the answer's sum, none with the answer's total; every adding
            item 2 groups decoys, distinct, neither the groups. Each item uses its mode's tables (main 2, 5, 10; pro 3,
            4, 8); pictures hold at most 50 thingies; a sum at most 6 terms.
  Source    the greeting is never written with innerHTML; location.hash is read once; no sessionStorage; no mfg() payload
            or storage write names the look, the fragment or the class name.
  Marking   in each look, every item in the page, twice (right, then wrong), from ST.ui.preview: the picture counted from
            the DOM (Stage 1: groups plates of each thingies; Stage 3: rows x cols dots in rows rows); the options' values
            (dataset.val) are the answer and its decoys (sums joined with "+"; Stage 2 adding: first groups and its two
            groups decoys); every option's text blanked before the pick, so only dataset.val can mark it; right only for
            the answer (Stage 2 adding: and the right count); one line, from LINES (right, or the item type's wrong line),
            then the worked maths, built here from the item; Stage 3's array turned round to cols rows of rows.
  Greeting  "#kids/Example" and "#kids/Example%20Class" -> "Welcome, Example Class!"; "#KIDS" and "#kids" -> the kid look and
            its welcome; "#kids/<script>" -> the kid look, no class greeting, nothing injected; no hash or "#kidsx" ->
            the grown-up look.
  Read aloud against a mocked speechSynthesis: no speaker without a local voice; only a local voice passed to speak();
            nothing spoken before a tap; the question read in words from the item; never the greeting.
  Play      every mode and stage in each look at 360 x 640 (the kid look from #kids/Example): 10 different items of that
            mode and stage, right and wrong, played to the end (the fold is Fit's, every item); one game_completed with
            the score, one board submission [slug, 'stage-N' or 'pro-stage-N', score, 10]; question_answered per item with
            its id; only game_started, question_answered and game_completed; no mfg() payload, localStorage or
            sessionStorage value containing "kids", "Example" or "#". The largest picture (50 thingies), the largest array
            (10 x 5 and 5 x 10) and the longest sum (6 terms) on screen at 360 x 640 with every option above the fold and
            no sideways scroll.
  Fit       every item above the fold (PRIMARY-FIT-SWEEP, scripts/fit_common.py): all 369 in each look at 360 x 640
            with a local voice, so the speaker shows, the real fonts and the settled layout: each previewed as question 1
            and as question 11 (winner stays on: the overtime line, End), Stage 3's arrays also as question 5 and 8 (the
            scaffold's three shapes), walked step by step (the lots counted, right and wrong; the rows and each row, right
            and wrong), every control measured at every step, then Next after every feedback variant: each LINES.right
            line (ST.ui.answer's line argument; Stage 3's right answer is Sarge's line) and each decoy (ST.ui.pick). The
            picture never wider than its card, no sideways scroll. Nothing sampled: the same items and variants every run.

SOME-THINGIES-TWEAKS (Jon, 21 Nov 2026):
  Stage 3   every array cell a thingy (an svg with its body, two eyes, two pupils), never a dot; coloured by column (by
            row once turned round) from one fixed set of 10 distinct colours, the same colour for each k everywhere; a
            gap of 0.6-0.8 of a thingy after the 5th column and the 5th row, the ordinary gaps smaller; the 5 x 10 and
            10 x 5 arrays at 360 x 640 with their options above the fold, no sideways scroll, thingies at least 18 px.
  Scaffold  in a Stage 3 run, questions 1-4 ask rows, each row, then the total; 5-7 show the rows label from the start
            and ask each row, then the total; 8+ the total only; each step labels the array with the right number,
            right or wrong, and never changes the score.
  Winner    10 right then a wrong ends the run at 11 answered, score 10, one submission [slug, board, 10, 11]; a wrong
            at question 3 does not end it; End at question 12 ends it with the score so far; no End button before
            question 11; "n/10" then "n" in the HUD; 50 questions of main Stage 1 use all 22 items before any repeats and
            never serve one twice in a row. Every play run ends at the wrong at question 11 (wrong at 2, 5 and 8 go on).

SOME-THINGIES-PERSONALITY (Jon, 21 Nov 2026):
  Thingies  every thingy (plates, conga, array, crowds; not Sarge) wears the accessory for its colour and no other,
            read from its SVG's shapes (k1 bow, k2 spiky hair, k3 cap, k4 flower, k5 sprout, k6 glasses, k7 headphones,
            k8 top hat, k9 beanie, k10 moustache), and a medal exactly in pro mode; nothing animates under reduced
            motion (document.getAnimations()).
  Scenes    the start screen's crowd (12-16 thingies) keeps the first Start button above the fold at every phone-fit size,
            both looks; the conga line (no line before a groups-to-sum item is marked) is g groups of n, one colour each
            in order, one group per line at 360 px and at 320 px (or stepped aside after marking at 320 x 568), with Next
            above the fold; Sarge beside the array where the card gives him a size, else in the top row (SOME-THINGIES-HOST),
            Next above the fold for every array, his line on a right answer.
  Crowd     none in questions 1-10; from 11 the cheer and one more thingy per right answer, in colour order, every one
            drawn; the score always the game's; the run-ending wrong answer makes it faint, with the faint line.

CROWD-FILL (Jon, 25-26 Nov 2026), at 1280 x 720, 1904 x 864 and 375 x 667, in each look:
  Crowd     a run of 135 right answers: after every answer and on every new question the crowd holds exactly one thingy
            for each right answer after question 10, in colour order, with no "+n" and no text but the cheer; every
            thingy the same size, measured here from the DOM against the fold (the screen, less the fixed footer):
            16 px while the card, crowd and all, ends above the fold; smaller only when 16 px would not, and then the
            largest half pixel that fits (one half pixel more, set here, must not fit); never under 6 px, where the
            rows carry on and the page may scroll. Then the crowd at 300 to 12,000 (ST.ui.crowd, the page's hook for
            this) until each of the three states has been seen: full size, shrunk to fit, and the floor with the card
            past the fold; back at 125 it is 16 px again; a shorter window shrinks it (re-measured on resize). At
            every step everything in the card above the crowd is where it is with the crowd taken out, and ends above
            the crowd's top. The cheer is the contract's line for the largest of 1, 10, 20, 30, 50, 75, 100 reached
            (written out here, not read from the page), checked at every size from 0 to 125. The accessory and the
            medal (pro) at full size and shrunk. The slip: the crowd faints with the faint line, still whole, nothing
            animating. The overtime line at question 11 and the menu note carry Jon's tagline; the results screen
            reads "You collected n thingies." (kids "!"), "1 thingy" for one, and nothing for none. The time to draw
            and size the crowd of 120 (the median of five) is printed (and fails over 500 ms: the contract's stop is
            50 ms).

SOME-THINGIES-FACTS (Jon, 26 Nov 2026), Stage 4, at 320 x 568, 375 x 667 and 1280 x 720, in each look, normal and Aa
(the page's own Aa button), the speaker showing and the real fonts (fit_common.open_phone):
  Beside    on all 192 Stage 4 items (Main and Pro), right (the longest LINES.right line) and wrong: #sargeMini holds
            exactly one thingy, colour 6 in glasses (two lenses drawn), a medal exactly in Pro, no text, on the first
            screen; before marking and on the next question it carries neither reaction and its waiting mouth shows;
            after a right answer react-right and the smile, after a wrong one react-wrong and the puzzled mouth.
  Picture   none before marking or on the next question. After marking, where it shows: the plates and the thingies
            on each counted from the DOM against this script's own (a x b: a plates of b; ? x b = product: product / b
            plates of b), each plate one colour in the fixed order, every thingy one size from 10 to 18 px and inside
            its plate, the picture between the options and the working, never wider than its card, carrying the
            reaction; shrunk only as far as the room needs (one pixel more, set here, must not fit). Where it does
            not show: a stand-in the size of the picture at 10 px (built here from the CSS's proportions) put in its
            place must push Next past the fold, so it is dropped only where it could not fit.
  Fold      Next above the fold (the screen less the fixed footer) on every item, right and wrong; no sideways scroll.
            The counts of items showing and dropping the picture are printed per look, size and mode of reading.
  Crowd     past question 10 (as question 12, by ST.ui.preview and ST.ui.crowd): each mode's smallest fact and its
            largest (a x b, and the missing number) with 60 in the crowd, the largest also with 1 and with a crowd
            big enough to have shrunk to fit (which must be seen). After marking the crowd is the size CROWD-FILL
            gives the card with the picture taken out (16 px and fitting, or the largest half pixel that fits,
            checked here), so the picture did not change it; and where the picture shows, the card, crowd and all,
            still ends above the fold: the picture fits the room the crowd leaves. Whether the crowd is the same size
            before and after marking is counted and printed: the marking's own feedback (and a right answer's new
            thingy) can resize a crowd that already fills the screen, as it did before this contract.

SOME-THINGIES-HOST (Jon, 26 Nov 2026; SR-35), Stages 3 and 4, Main and Pro, at 320 x 568, 375 x 667, 1366 x 768 and
1920 x 955, in each look, normal and Aa (fit_common.open_phone: the speaker showing, the real fonts):
  Size      every item as question 1, right (the LINES.right line that takes the most height, measured here) and wrong,
            played three times: as the page sizes the character, forced into the top row (as before this contract) and
            forced one pixel bigger (48 px where the page chose the top row). On every screen (each step asked, after
            marking) one character shows: in the top row alone at 22 px (card data-host "mini"), or at the card's size
            from 48 to 96 px, Sarge beside the array and inside the picture's width, the thingy in glasses beside the sum
            line, left of it, the sum not wider than its room; the drawn size the card's (one size for both characters);
            the same size on every screen, before and after marking, right and wrong.
  Fold      the options on every asking screen and Next after marking above the fold, no sideways scroll (against the
            layout width: a phone zooms out to show an overflow); where it fails in the top row too, main loses the fold:
            the item must be on HOST_KNOWN (CI's figures) and the character in the top row; an entry whose fold now holds
            is stale. Stage 3's array marked but not yet turned (built here from the array as it stood: reduced motion
            turns it at once): the character may not push Next lower than the fold or than it is in the top row.
  Room      the character changes nothing the top row leaves: the fact picture shown or dropped alike and at the same
            size, the sum as high. The largest that fits: one pixel more must break one of these rules on the item.
  Crowd     past question 10 (as question 12), sampled as SOME-THINGIES-FACTS samples (each mode's smallest and largest
            item of each stage with 60 in the crowd, the largest also with 1 and with a crowd big enough to shrink,
            which must be seen): the crowd the same size before and after marking as in the top row, the fold held.

Work units: "bank" (no browser), "scenes", "marking grown", "marking kids", "greeting", "read aloud", "play grown 360x640",
"play kids 360x640", "winner 360x640", "crowd <look> <W>x<H>" (one per look and CROWD-FILL size), "facts <look> <W>x<H> <normal|Aa>" (one per look, SOME-THINGIES-FACTS size and reading mode), "host <look> <W>x<H> <normal|Aa>" (one per look, SOME-THINGIES-HOST size and reading mode), "fit <look> <mode>-<stage>" (one per look, mode and stage), and "plant: <what>" (one per planted fault).

    python scripts/verify-some-thingies.py              # every unit, then the self-test
    python scripts/verify-some-thingies.py --selftest   # the planted faults only
"""
import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402
import fit_common as fc  # noqa: E402

SLUG = 'some-thingies'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
GENERATOR = os.path.join(ROOT, 'tools', SLUG, 'bank.py')
SHA = '9319d31df002f75fb6f10416124d609ddf03135e6482470b5c7250c5a5730b7e'
COUNTS = {('main', 1): 22, ('main', 2): 28, ('main', 3): 36, ('main', 4): 96,
          ('pro', 1): 23, ('pro', 2): 30, ('pro', 3): 38, ('pro', 4): 96}
TABLES = {'main': (2, 5, 10), 'pro': (3, 4, 8)}
MODES = ['main-1', 'main-2', 'main-3', 'main-4', 'pro-1', 'pro-2', 'pro-3', 'pro-4']
PHONE = (360, 640)
WINNER = 'winner %dx%d' % PHONE
SCENES = 'scenes'
TURN = 'turn'
# CROWD-FILL: the contract's sizes, the mode each plays (pro for the medal), and its lines, written out here.
CROWD_SIZES = [((1280, 720), 'pro-4'), ((1904, 864), 'main-1'), ((375, 667), 'pro-1')]
CROWD_UNITS = ['crowd %s %dx%d' % (look, sz[0], sz[1]) for look in ('grown', 'kids') for sz, _ in CROWD_SIZES]
CHEERS = {
    'grown': {0: 'A crowd is gathering.', 1: 'A crowd is gathering.', 10: 'Word is spreading.', 20: "Someone's selling hot dogs.",
              30: 'The thingies have formed a fan club.', 50: "Stadium capacity reached. They've opened another stadium.",
              75: 'Thingies are queuing round the block. The block is concerned.', 100: 'Every thingy on Earth is here. Some came from Mars.'},
    'kids': {0: 'The crowd goes wild!', 1: 'The crowd goes wild!', 10: 'More thingies are coming!', 20: 'The thingies are dancing!',
             30: 'A thingy party!', 50: 'Fifty thingies! Wow!', 75: 'The whole town is here!', 100: 'Thingies from space!'},
}
# SOME-THINGIES-FACTS: the contract's sizes, each in both looks, normal and Aa; the crowd its past-question-10 cases
# use to fill the screen.
FACT_SIZES = [(320, 568), (375, 667), (1280, 720)]
FACT_UNITS = ['facts %s %dx%d %s' % (look, sz[0], sz[1], aa) for look in ('grown', 'kids') for sz in FACT_SIZES for aa in ('normal', 'Aa')]
FACT_CROWD_BIG = {False: 500, True: 1300}   # by the screen: a phone, a wide screen
# SOME-THINGIES-HOST: the contract's sizes, each in both looks, normal and Aa; the character's sizes (the page's own).
HOST_SIZES = [(320, 568), (375, 667), (1366, 768), (1920, 955)]
HOST_UNITS = ['host %s %dx%d %s' % (look, sz[0], sz[1], aa) for look in ('grown', 'kids') for sz in HOST_SIZES for aa in ('normal', 'Aa')]
HOST_MIN, HOST_MAX = 48, 96
# Items where main already loses the fold (options or Next under it, right and wrong both played): the character stays in
# the top row there. CI's own figures (the container's fallback fonts differ): (unit, item) -> what main loses, where.
HOST_KNOWN = {
}
TAGLINE = 'how many thingies can you collect'
MENU_NOTE = 'At least 10 questions, then see how many thingies you can collect: keep going until a slip, or press End. A point for each one right.'


def cheer_for(look, n):
    return CHEERS[look][max(t for t in CHEERS[look] if t <= n)]


def collected_line(look, n):
    return 'You collected %d %s%s' % (n, 'thingy' if n == 1 else 'thingies', '!' if look == 'kids' else '.')
# SOME-THINGIES-PERSONALITY: the accessory for each of the 10 colours (k1..k10, #866's fixed order: red, orange, amber,
# green, teal, sky, indigo, purple, pink, brown). Jon's three: the oranges' spiky hair, the blues' glasses, the purples'
# top hat; the other seven in the contract's order. Each is told by its own shape, read here from the SVG.
ACC = {1: 'bow', 2: 'hair', 3: 'cap', 4: 'flower', 5: 'sprout', 6: 'glasses', 7: 'headphones', 8: 'tophat', 9: 'beanie', 10: 'moustache'}
ACC_SHAPE = {'bow': '.a-bow', 'hair': '.a-hair', 'cap': '.a-cap', 'flower': '.a-petal', 'sprout': '.a-leaf', 'glasses': '.a-lens',
             'headphones': '.a-band', 'tophat': '.a-hatband', 'beanie': '.a-beanie', 'moustache': '.a-tache'}
# Every phone-fit size (scripts/measure-phone-fit.py: phones, and the laptop mode's two).
FIT_SIZES = [(320, 568), (375, 667), (390, 844), (1366, 768), (1280, 720)]
# Every thingy in scope: which colour (k), which accessory its SVG says and which shapes it holds, and a medal or not.
THINGIES_JS = r"""(scope) => [...document.querySelectorAll(scope + ' svg.th:not(.sarge)')].map(t => {
  const k = +(((t.getAttribute('class') || '').match(/\bk(\d+)\b/) || [])[1] || 0);
  const shapes = %s.filter(([n, sel]) => t.querySelector(sel)).map(([n]) => n);
  return { k: k, acc: t.dataset.acc || null, shapes: shapes, medal: !!t.querySelector('.medal') }; })""" % json.dumps(sorted(ACC_SHAPE.items()))
RUNNING_JS = "() => document.getAnimations().filter(a => a.playState === 'running').map(a => (a.animationName || a.constructor.name) + ' on ' + (a.effect && a.effect.target ? (a.effect.target.getAttribute('class') || a.effect.target.tagName) : '?'))"


def check_thingies(page, scope, pro, what, out):
    """Every thingy in scope wears its colour's accessory (and no other), and a medal exactly in pro mode."""
    for t in page.evaluate(THINGIES_JS, scope):
        want = ACC.get(t['k'])
        if not want or t['acc'] != want or t['shapes'] != [want]:
            out.append('%s: a thingy of colour %s wears %s (shapes %s), expected %s' % (what, t['k'], t['acc'], t['shapes'], want))
            return
        if t['medal'] != pro:
            out.append('%s: a thingy %s a medal in %s mode' % (what, 'wears' if t['medal'] else 'has no', 'pro' if pro else 'main'))
            return


def still(page, what, out):
    """Reduced motion: nothing animating."""
    run = page.evaluate(RUNNING_JS)
    if run:
        out.append('%s: %d animations running under reduced motion (%s)' % (what, len(run), ', '.join(sorted(set(run))[:3])))
PER = 10
EVENTS = {'game_started', 'question_answered', 'game_completed'}
WRONG_KEY = {'groups': 'groups', 'sum-to-groups': 'sum', 'groups-to-sum': 'pick', 'array': 'array', 'fact': 'fact', 'missing': 'missing'}
# The largest pictures and the longest sum (contract step 9), on screen at 360 x 640.
LARGEST = ['m1-5x10', 'm1-10x5', 'm3-10r5c', 'm3-5r10c', 'm2a-6x5', 'p2a-6x8', 'p1-6x8', 'm2b-5x10']


def board_of(m):
    md, st = m.split('-')
    return ('pro-' if md == 'pro' else '') + 'stage-' + st


# ---------------------------------------------------------------- the bank (no browser)
def bank_of(html):
    m = re.search(r'\n  var QUESTIONS = \[\n(.*?)\n  \];', html, re.S)
    if not m:
        raise ValueError('no QUESTIONS array in the page')
    items = []
    for line in m.group(1).split('\n'):
        line = line.strip().rstrip(',')
        if line:
            items.append(json.loads(line))
    return items


def blob(items):
    return ''.join(json.dumps(i, separators=(',', ':')) + '\n' for i in items)


def total(q):
    """The item's answer, computed here from its own parts."""
    t = q['type']
    if t == 'groups':
        return q['groups'] * q['each']
    if t == 'sum-to-groups':
        n = 0
        for x in q['sum']:
            n += x
        return n
    if t == 'groups-to-sum':
        return q['groups'] * q['each']
    if t == 'array':
        return q['rows'] * q['cols']
    if t == 'fact':
        return q['a'] * q['b']
    if t == 'missing':
        return q['product'] // q['b']
    raise ValueError('unknown type %r' % t)


def key_of(q):
    return '+'.join(str(x) for x in q['answer_sum']) if q['type'] == 'groups-to-sum' else str(q['answer'])


def working(q):
    """The worked maths as plain text, built here from the item (contract step 3)."""
    t = q['type']
    if t in ('groups', 'sum-to-groups', 'groups-to-sum'):
        g, n = q['groups'], q['each']
        a = g * n
        if g <= 6:
            return '%d groups of %d = %s = %d' % (g, n, ' + '.join([str(n)] * g), a)
        return '%d groups of %d = %d' % (g, n, a)
    if t == 'array':
        r, c = q['rows'], q['cols']
        return '%d × %d = %d × %d = %d' % (r, c, c, r, r * c)
    if t == 'fact':
        return '%d × %d = %d' % (q['a'], q['b'], q['a'] * q['b'])
    return '%d × %d = %d' % (q['product'] // q['b'], q['b'], q['product'])


def check_item(q, out):
    i, t = q['id'], q['type']
    tables = TABLES.get(q['mode'], ())
    if t == 'missing':
        if q['product'] % q['b']:
            out.append('%s: %d is not a multiple of %d' % (i, q['product'], q['b']))
    want = total(q)
    if t == 'sum-to-groups':
        if len(q['sum']) != q['groups'] or any(x != q['each'] for x in q['sum']):
            out.append('%s: the sum %s is not %d groups of %d' % (i, q['sum'], q['groups'], q['each']))
        if q['groups'] * q['each'] != want:
            out.append('%s: the sum totals %d, not %d x %d' % (i, want, q['groups'], q['each']))
        gd = q['groups_decoys']
        if len(gd) != 2 or len(set(gd)) != 2 or q['groups'] in gd or min(gd) < 1:
            out.append('%s: groups decoys %s (2 distinct, positive, never %d)' % (i, gd, q['groups']))
    if t == 'groups-to-sum':
        if q['answer_sum'] != [q['each']] * q['groups']:
            out.append('%s: answer_sum %s is not %d groups of %d' % (i, q['answer_sum'], q['groups'], q['each']))
        ds = q['decoy_sums']
        if len(ds) != 3 or len({tuple(d) for d in ds}) != 3:
            out.append('%s: decoy sums %s (3 distinct)' % (i, ds))
        for d in ds:
            if d == q['answer_sum']:
                out.append('%s: a decoy sum is the answer' % i)
            s = 0
            for x in d:
                s += x
            if s == want:
                out.append('%s: decoy sum %s has the answer\'s total %d' % (i, '+'.join(map(str, d)), want))
            if len(d) > 6:
                out.append('%s: decoy sum %s has %d terms (at most 6)' % (i, d, len(d)))
    else:
        if q['answer'] != want:
            out.append('%s: answer %d, recomputed %d' % (i, q['answer'], want))
        d = q['decoys']
        if len(d) != 3 or len(set(d)) != 3 or min(d) < 1:
            out.append('%s: decoys %s (3 distinct, positive)' % (i, d))
        if q['answer'] in d:
            out.append('%s: a decoy equals the answer' % i)
    # The mode's tables.
    if t in ('groups', 'sum-to-groups', 'groups-to-sum'):
        n = q['each']
    elif t == 'array':
        n = q['cols'] if q['cols'] in tables else q['rows']
    elif t == 'fact':
        n = q['b'] if q['b'] in tables else q['a']
    else:
        n = q['b']
    if n not in tables:
        out.append('%s: no factor from the %s tables %s' % (i, q['mode'], tables))
    if t in ('groups', 'array') and want > 50:
        out.append('%s: %d in one picture (at most 50)' % (i, want))
    if t == 'sum-to-groups' and len(q['sum']) > 6:
        out.append('%s: a sum of %d terms (at most 6)' % (i, len(q['sum'])))


def generator_items():
    spec = importlib.util.spec_from_file_location('st_bank', GENERATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.bank()


def check_bank(html, out, info):
    items = bank_of(html)
    sha = hashlib.sha256(blob(items).encode()).hexdigest()
    if sha != SHA:
        out.append('the bank\'s SHA-256 is %s, the contract\'s %s' % (sha[:16], SHA[:16]))
    gsha = hashlib.sha256(blob(generator_items()).encode()).hexdigest()
    if gsha != SHA:
        out.append('tools/some-thingies/bank.py makes SHA-256 %s, the contract\'s %s' % (gsha[:16], SHA[:16]))
    c = Counter((q['mode'], q['stage']) for q in items)
    if dict(c) != COUNTS:
        out.append('counts %s, expected %s (369)' % (dict(sorted(c.items())), COUNTS))
    ids = [q['id'] for q in items]
    for d in sorted(k for k, v in Counter(ids).items() if v > 1):
        out.append('%s: id used twice' % d)
    for q in items:
        try:
            check_item(q, out)
        except Exception as e:  # noqa: BLE001
            out.append('%s: could not be checked (%s)' % (q.get('id'), e))
    info['bank'] = len(items)


def check_source(html, out):
    """The fragment, the look and the class name stay in the page."""
    js = '\n'.join(re.findall(r'<script>(.*?)</script>', html, re.S))
    if re.search(r'innerHTML\s*=[^;\n]*(greeting\(|CLASS_NAME|\bfrag\b|\bnm\b)', js):
        out.append('the greeting (the class name) is written with innerHTML')
    if js.count('location.hash') != 1:
        out.append('location.hash is read %d times, not once' % js.count('location.hash'))
    if 'sessionStorage' in js:
        out.append('the page uses sessionStorage')
    for m in re.finditer(r'\b(?:lsSet|localStorage\.setItem)\(([^;\n]*)', js):
        if re.search(r'LOOK|CLASS_NAME|\bfrag\b|\bnm\b|hash', m.group(1)):
            out.append('a storage write names the look or the fragment: %s' % m.group(0)[:80])
    for m in re.finditer(r'\bev\((\'[a-z_]+\'), \{([^}]*)\}', js):
        if re.search(r'LOOK|CLASS_NAME|\bfrag\b|\bnm\b|hash', m.group(2)):
            out.append('an mfg() payload names the look or the fragment: %s' % m.group(1))


# ---------------------------------------------------------------- the browser
def open_page(pw, base, html, size, frag='', query='?cb=verify', init=None):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    # Record every mfg() call from the first one: analytics.js's own mfg is wrapped as it is defined.
    ctx.add_init_script("""(() => { window.__ev = []; let real = null;
      Object.defineProperty(window, 'mfg', { configurable: true,
        get() { return function (n, p) { window.__ev.push([n, JSON.parse(JSON.stringify(p || {}))]); }; },
        set(v) { real = v; } }); })();""")
    if init:
        ctx.add_init_script(init)
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/%s%s' % (SLUG, query, frag), wait_until='load', timeout=30000)
    page.wait_for_function('!!window.ST && !!ST.ui', timeout=15000)
    page.emulate_media(reduced_motion='reduce')   # the array then turns at once: the marking checks run without waiting
    page.evaluate("""() => { window.__sub = [];
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


# What is on screen for the item, read from the DOM (never from ST's own view of the item).
SCREEN_JS = r"""() => {
  const $ = (id) => document.getElementById(id);
  const vals = (id) => [...$(id).querySelectorAll('.opt')].map(b => b.dataset.val);
  const plates = [...$('pic').querySelectorAll('.plate')].map(p => p.querySelectorAll('svg.th').length);
  // Stage 3: every cell of the array, its row and column from where it is drawn, what it is and its colour.
  const cells = [...$('pic').querySelectorAll('.arr .arow > *')];
  const box = (e) => e.getBoundingClientRect();
  const tops = [...new Set(cells.map(d => Math.round(box(d).top)))].sort((a, b) => a - b);
  const lefts = [...new Set(cells.map(d => Math.round(box(d).left)))].sort((a, b) => a - b);
  const arr = { n: cells.length, thingies: cells.filter(c => c.matches('svg.th') && c.querySelector('ellipse.b') && c.querySelectorAll('.eyes circle').length === 4).length,
                rows: tops.length, cols: lefts.length, cells: [], size: cells.length ? box(cells[0]).width : 0 };
  for (const c of cells) {
    const k = ((c.getAttribute('class') || '').match(/\bk(\d+)\b/) || [])[1];
    const body = c.querySelector('ellipse');
    arr.cells.push([tops.indexOf(Math.round(box(c).top)) + 1, lefts.indexOf(Math.round(box(c).left)) + 1, k ? +k : null,
                    body ? getComputedStyle(body).fill : null]);
  }
  // Gaps, in thingies: after column 1 and column 5, after row 1 and row 5 (from the cells of the first row and column).
  const at = (r, c) => cells.find(x => tops.indexOf(Math.round(box(x).top)) + 1 === r && lefts.indexOf(Math.round(box(x).left)) + 1 === c);
  const gapC = (c) => (at(1, c) && at(1, c + 1)) ? (box(at(1, c + 1)).left - box(at(1, c)).right) / arr.size : null;
  const gapR = (r) => (at(r, 1) && at(r + 1, 1)) ? (box(at(r + 1, 1)).top - box(at(r, 1)).bottom) / arr.size : null;
  arr.gc1 = gapC(1); arr.gc5 = gapC(5); arr.gr1 = gapR(1); arr.gr5 = gapR(5);
  arr.top = ($('arrTop') || {}).textContent || ''; arr.side = ($('arrSide') || {}).textContent || '';
  const ann = (el) => [...el.querySelectorAll('annotation')].map(a => a.textContent).join(' ');
  return { state: ST.ui.state(), plates: plates, arr: arr, dots: cells.length, rows: tops.length, cols: lefts.length,
           sum: ann($('sum')), opts1: $('opts1').hidden ? null : vals('opts1'), opts: $('opts').hidden ? null : vals('opts'),
           say: $('say').textContent, sayKey: $('say').dataset.say || null,
           learn: ($('learn') || {}).dataset ? ($('learn').dataset.learn || null) : null,
           lines: $('feedback').querySelectorAll('.say').length, score: ST.ui.score() };
}"""
BLANK_JS = "(id) => document.getElementById(id).querySelectorAll('.opt').forEach(b => { b.textContent = ''; })"
PICK_JS = """([id, v]) => { const box = document.getElementById(id); MaffsLock.fresh(box, 0);
  const b = [...box.querySelectorAll('.opt')].find(x => x.dataset.val === v); if (b) b.click(); return !!b; }"""


def all_lines(L):
    out = []
    for v in L.values():
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, list):
            out.extend(v)
        elif isinstance(v, dict):
            out.extend(v.values())
    return out


def words(s):
    return len(re.sub(r'\{(name|n)\}', '', s).split())


def check_marking(page, html, look, out, info):
    lines = page.evaluate('ST.lines()')
    L = lines[look]
    if look == 'grown':
        for k, s in (('kids.' + k2, v) for k2, v in lines['kids'].items() if isinstance(v, str)):
            if words(s) > 6:
                out.append('LINES.%s has %d words' % (k, words(s)))
        for k2 in ('right',):
            for j, s in enumerate(lines['kids'][k2]):
                if words(s) > 6:
                    out.append('LINES.kids.%s.%d has %d words' % (k2, j, words(s)))
        for k2, s in list(lines['kids']['wrong'].items()) + [('stages.' + a, b) for a, b in lines['kids']['stages'].items()] + [('cheers.' + a, b) for a, b in lines['kids']['cheers'].items()]:
            if words(s) > 6:
                out.append('LINES.kids.wrong.%s has %d words' % (k2, words(s)))
    every = set(all_lines(L))
    items = bank_of(html)
    marked = 0
    fills = {}
    for n, q in enumerate(items):
        i, t = q['id'], q['type']
        for right in (True, False):
            # As question 8: Stage 3's scaffold is gone by then (check_winner covers questions 1-7).
            page.evaluate('([id, at]) => ST.ui.preview(id, at)', [i, 8])
            s = page.evaluate(SCREEN_JS)
            if right:
                # The picture, counted from the DOM.
                if t == 'groups' and s['plates'] != [q['each']] * q['groups']:
                    out.append('%s: the picture shows plates of %s, expected %d plates of %d' % (i, s['plates'], q['groups'], q['each']))
                if t == 'array':
                    check_array(i, q, s['arr'], False, out, fills)
                if t == 'fact' and s['sum'].replace(' ', '') != '%d\\times%d={?}' % (q['a'], q['b']):
                    out.append('%s: the question reads %r' % (i, s['sum']))
                if t == 'missing' and s['sum'].replace(' ', '') != '{?}\\times%d=%d' % (q['b'], q['product']):
                    out.append('%s: the question reads %r' % (i, s['sum']))
                if t == 'sum-to-groups' and s['sum'].replace(' ', '') != '+'.join([str(q['each'])] * q['groups']):
                    out.append('%s: the sum reads %r' % (i, s['sum']))
            # Stage 2 adding: part 1, how many lots.
            if t == 'sum-to-groups':
                want1 = sorted([str(q['groups'])] + [str(x) for x in q['groups_decoys']])
                if sorted(s['opts1'] or []) != want1:
                    out.append('%s: the how-many options are %s, expected %s' % (i, s['opts1'], want1))
                    continue
                page.evaluate(BLANK_JS, 'opts1')
                pick1 = str(q['groups']) if right else str(q['groups_decoys'][n % 2])
                page.evaluate(PICK_JS, ['opts1', pick1])
                s = page.evaluate(SCREEN_JS)
            if t == 'groups-to-sum':
                want = sorted(['+'.join(map(str, x)) for x in [q['answer_sum']] + q['decoy_sums']])
            else:
                want = sorted([str(q['answer'])] + [str(x) for x in q['decoys']])
            if sorted(s['opts'] or []) != want:
                out.append('%s: the options are %s, expected %s' % (i, s['opts'], want))
                continue
            if s['state'] != 'ask':
                out.append('%s: state %r before the pick' % (i, s['state']))
                continue
            key = key_of(q)
            # Right: the key. Wrong: a decoy, except on an adding item, where the count was wrong and the total is right.
            if right or t == 'sum-to-groups':
                pick = key
            else:
                pick = [v for v in want if v != key][n % 3]
            page.evaluate(BLANK_JS, 'opts')
            page.evaluate(PICK_JS, ['opts', pick])
            s = page.evaluate(SCREEN_JS)
            exp = 'done' if right else 'wrong'
            if s['state'] != exp:
                out.append('%s: option %s marked %s, expected %s' % (i, pick, s['state'], exp))
                continue
            if s['score'] != (1 if right else 0):
                out.append('%s: score %d after a %s answer' % (i, s['score'], 'right' if right else 'wrong'))
            # One line from LINES, then the working.
            if right and t == 'array' and s['say'] != L['sarge']:
                out.append("%s: the right line %r, expected Sarge's (LINES.%s.sarge)" % (i, s['say'], look))
            if right and t != 'array' and s['say'] not in L['right']:
                out.append('%s: the right line %r is not one of LINES.%s.right' % (i, s['say'], look))
            if not right and s['say'] != L['wrong'][WRONG_KEY[t]]:
                out.append('%s: the wrong line %r, expected LINES.%s.wrong.%s' % (i, s['say'], look, WRONG_KEY[t]))
            # One line at a time: the line is one LINES string, and the working under it holds none.
            fbtext = page.evaluate("document.getElementById('feedback').textContent")
            hits = [x for x in every if len(x) > 3 and x in fbtext]
            if s['say'] not in every or hits:
                out.append('%s: feedback holds %d LINES strings (the line %r, under it %s)' % (i, (s['say'] in every) + len(hits), s['say'], hits))
            if right or n % 7 == 0:
                check_thingies(page, '#game', q['mode'] == 'pro', '%s (%s, marked)' % (i, look), out)
                still(page, '%s (%s, marked)' % (i, look), out)
            if s['learn'] != working(q):
                out.append('%s: the working shown is %r, expected %r' % (i, s['learn'], working(q)))
            if t == 'array' and right:
                a = page.evaluate(SCREEN_JS)['arr']
                if a['rows'] != q['cols'] or a['cols'] != q['rows']:
                    out.append('%s: after marking the array is %d rows of %d, expected it turned round to %d rows of %d' % (i, a['rows'], a['cols'], q['cols'], q['rows']))
                else:
                    check_array(i + ' (turned)', {'rows': q['cols'], 'cols': q['rows']}, a, True, out, fills)
            marked += 1
    # One fixed set of 10 distinct colours, k1..k10, the same everywhere (check_array records each one's fill).
    if sorted(fills) != list(range(1, 11)) or len(set(fills.values())) != 10:
        out.append('the array colours: %d of the 10 seen, %d distinct (%s)' % (len(fills), len(set(fills.values())), fills))
    info['marked'] = info.get('marked', 0) + marked


def check_array(i, q, a, turned, out, fills):
    """Stage 3's picture (Jon's option C): rows x cols thingies, coloured by column (by row once turned round, the
    colours following their thingies), from one fixed set; a gap of about 0.7 of a thingy after the 5th column and the
    5th row, the ordinary gaps smaller."""
    r, c = q['rows'], q['cols']
    if a['n'] != r * c or a['thingies'] != a['n']:
        out.append('%s: Stage 3 draws %d cells, %d of them thingies, expected %d thingies' % (i, a['n'], a['thingies'], r * c))
        return
    if a['rows'] != r or a['cols'] != c:
        out.append('%s: the array is %d rows of %d, expected %d of %d' % (i, a['rows'], a['cols'], r, c))
        return
    for row, col, k, fill in a['cells']:
        want = row if turned else col
        if k != want:
            out.append('%s: the thingy at row %d, column %d has colour %s, expected %d' % (i, row, col, k, want))
            return
        if fills.setdefault(k, fill) != fill:
            out.append('%s: colour %d is %s here, %s elsewhere' % (i, k, fill, fills[k]))
            return
    g = {'gc1': a['gc1'], 'gc5': a['gc5'], 'gr1': a['gr1'], 'gr5': a['gr5']}
    if c > 1 and not (0.05 <= g['gc1'] <= 0.35):
        out.append('%s: the gap between columns is %.2f of a thingy' % (i, g['gc1']))
    if c > 5 and not (0.6 <= g['gc5'] <= 0.8):
        out.append('%s: the gap after the 5th column is %.2f of a thingy, expected about 0.7' % (i, g['gc5'] or -1))
    if r > 1 and not (0.2 <= g['gr1'] <= 0.45):
        out.append('%s: the gap between rows is %.2f of a thingy' % (i, g['gr1']))
    if r > 5 and not (0.6 <= g['gr5'] <= 0.8):
        out.append('%s: the gap after the 5th row is %.2f of a thingy, expected about 0.7' % (i, g['gr5'] or -1))


GREETINGS = [
    ('', 'grown', None),
    ('#kidsx', 'grown', None),
    ('#kids', 'kids', None),
    ('#KIDS', 'kids', None),
    ('#kids/Example', 'kids', 'Welcome, Example Class!'),
    ('#kids/Example%20Class', 'kids', 'Welcome, Example Class!'),
    ('#kids/%3Cscript%3Ealert(1)%3C%2Fscript%3E', 'kids', None),
    ('#kids/<script>', 'kids', None),
]


def check_greeting(pw, base, html, out):
    for frag, look, greet in GREETINGS:
        br, page, errs = open_page(pw, base, html, PHONE, frag)
        try:
            L = page.evaluate('ST.lines()')[look]
            got = page.evaluate("""() => ({ kids: document.body.classList.contains('look-kids'),
                welcome: document.getElementById('welcome').textContent, title: document.getElementById('titleLine').textContent,
                tags: document.querySelectorAll('#welcome *').length, look: ST.LOOK })""")
            want = greet or L['welcome']
            if got['kids'] != (look == 'kids') or got['look'] != look:
                out.append('greeting %r: the %s look, expected the %s look' % (frag, got['look'], look))
            if got['welcome'] != want or got['tags']:
                out.append('greeting %r: the welcome reads %r, expected %r' % (frag, got['welcome'], want))
            if got['title'] != L['title']:
                out.append('greeting %r: the title line reads %r' % (frag, got['title']))
            if errs:
                out.append('greeting %r: page error %s' % (frag, errs[0][:120]))
        finally:
            br.close()


# ---------------------------------------------------------------- every item above the fold (PRIMARY-FIT-SWEEP)
PIC = ('#pic', '#qcard')   # the picture must never be wider than its card
NEXT = '#feedback .maffs-next, #nextBtn'
# The sweep's stepper (scripts/fit_common.py sweep()): every item, previewed by itself as question 1 and as question 11
# (winner stays on: the overtime line, End), Stage 3's arrays also as question 5 and 8 (the scaffold's three shapes),
# walked step by step with the real buttons' handlers (the lots counted, the rows and each row, right and wrong), every
# control measured at every step, then Next after every feedback variant: each LINES.right line (ST.ui.answer's line
# argument; Stage 3's right answer is Sarge's one line) and each decoy (ST.ui.pick). The speaker shows throughout.
FIT_STEPPER = r"""{
  at(q) { return q.type === 'array' ? [1, 5, 8, 11] : [1, 11]; },
  key(q) { return q.type === 'groups-to-sum' ? q.answer_sum.join('+') : String(q.answer); },
  decoys(q) { return q.type === 'groups-to-sum' ? q.decoy_sums.map(d => d.join('+')) : q.decoys.map(String); },
  variants(id) {
    const q = ST.bank().find(x => x.id === id), lines = ST.lines()[ST.LOOK].right.length, vs = [];
    for (const at of this.at(q)) {
      if (q.type === 'array') vs.push('@' + at + ' right');
      else for (let i = 0; i < lines; i++) vs.push('@' + at + ' right ' + i);
      for (const d of this.decoys(q)) vs.push('@' + at + ' wrong ' + d);
      if (q.type === 'sum-to-groups') vs.push('@' + at + ' miscount, right');
      if (q.type === 'array' && at < 8) vs.push('@' + at + ' steps wrong, right');
    }
    return vs;
  },
  run(id, v, m) {
    const ui = ST.ui, st = () => ui.state();
    const at = +v.slice(1, v.indexOf(' ')), w = v.slice(v.indexOf(' ') + 1);
    ui.preview(id, at);
    const q = ui.question();
    if (!q || q.id !== id || ui.qi() !== at) throw new Error('preview did not show ' + id + ' as question ' + at);
    if (document.getElementById('speakBtn').hidden) throw new Error('the speaker is hidden');
    if (st() === 'count') {
      m('#speakBtn, #pic, #sum, #opts1 .opt', 'how many lots');
      ui.count(String(w.startsWith('miscount') ? q.groups_decoys[0] : q.groups));
    }
    while (st() === 'rows' || st() === 'cols') {
      const k = st(), n = k === 'rows' ? q.rows : q.cols;
      m('#speakBtn, #pic, #opts1 .opt', k === 'rows' ? 'how many rows' : 'how many in each row');
      ui.step(String(w.startsWith('steps wrong') ? n + 1 : n));
    }
    if (st() !== 'ask') throw new Error('no options: the state is ' + st());
    m('#speakBtn, #pic, #sum, #opts .opt, #endBtn', 'the options');
    const r = w.replace(/^(miscount|steps wrong), /, '');
    if (r === 'right') ui.answer(true);
    else if (r.startsWith('right ')) ui.answer(true, +r.slice(6));
    else ui.pick(r.slice(6));
    const right = r.startsWith('right') && !w.startsWith('miscount');
    if (st() !== (right ? 'done' : 'wrong')) throw new Error('marking left the state ' + st());
    if (r.startsWith('right ') && document.getElementById('say').dataset.say !== 'right.' + r.slice(6))
      throw new Error('the right line is ' + document.getElementById('say').dataset.say + ', not right.' + r.slice(6));
    m('#speakBtn, %s', 'Next');
  }
}""" % NEXT


def check_fit(pw, base, html, look, m, out, info):
    """Every item of mode-stage m in one look at 360 x 640, the speaker showing: every control at every step and Next after
    every feedback variant above the fold, the picture never wider than its card (fit_common.sweep)."""
    frag = '#kids/Example' if look == 'kids' else ''
    br, page, errs = fc.open_phone(pw, base, html, SLUG, '!!window.ST && !!ST.ui', frag, PHONE)
    try:
        if page.evaluate("document.body.classList.contains('look-kids')") != (look == 'kids'):
            out.append('fit %s %s: the page is not in the %s look' % (look, m, look))
        md, st = m.split('-')
        ids = [q['id'] for q in page.evaluate('ST.bank()') if q['mode'] == md and str(q['stage']) == st]
        got = fc.sweep(page, ids, FIT_STEPPER, out, 'fit %s %dx%d' % (look, PHONE[0], PHONE[1]), pic=PIC)
        if not ids or got['items'] != len(ids):
            out.append('fit %s %s: %d of %d items measured' % (look, m, got['items'], len(ids)))
        for k in ('items', 'variants', 'measures'):
            info.setdefault('fit', {}).setdefault(k, 0)
            info['fit'][k] += got[k]
    finally:
        out.extend('page error (fit %s %s): %s' % (look, m, e) for e in errs if 'production host' not in e)
        br.close()


def bad_in_storage(page):
    dump = page.evaluate("""() => { const o = {};
      for (const s of [localStorage, sessionStorage]) for (let i = 0; i < s.length; i++) o[s.key(i)] = s.getItem(s.key(i));
      return JSON.stringify(o); }""")
    return [b for b in ('kids', 'Example', '#') if b in dump]


def play(page, look, m, out):
    L = page.evaluate('ST.lines()')[look]
    page.evaluate("() => { window.__ev = []; window.__sub = []; }")
    page.evaluate('(m) => ST.ui.start(m)', m)
    md, st = m.split('-')
    tag = '%s %s' % (look, m)
    # Wrong at questions 2, 5, 8 and 11: the first three never end the run; the wrong at 11 does (winner stays on).
    seen, right, k = [], 0, 0
    for _ in range(120):
        s = page.evaluate('ST.ui.state()')
        if s == 'over':
            break
        if s in ('count', 'rows', 'cols', 'ask'):
            q = page.evaluate('ST.ui.question()')
            seen.append(q['id'])
            ok = k % 3 != 1
            page.evaluate('(r) => ST.ui.answer(r)', ok)
            right += 1 if ok else 0
            k += 1
            continue
        page.evaluate('ST.ui.next()')
    if page.evaluate('ST.ui.state()') != 'over':
        out.append('%s: the run did not finish' % tag)
        return
    pre = ('m' if md == 'main' else 'p') + st
    n = len(seen)
    if n != 11 or len(set(seen)) != n or any(not (x.startswith(pre + '-') or x.startswith(pre + 'a-') or x.startswith(pre + 'b-')) for x in seen):
        out.append('%s: the run served %s, expected 11 different %s stage %s items (wrong at 2, 5 and 8 go on; wrong at 11 ends it)' % (tag, seen, md, st))
    PER_ = n
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    evm = '%s-stage-%s' % (md, st)
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('level') != 'year6' or done[0].get('mode') != evm:
        out.append('%s: game_completed %s, expected one with score %d, mode %s' % (tag, done, right, evm))
    if sub != [[SLUG, board_of(m), right, PER_]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d of %d' % (tag, sub, board_of(m), right, PER_))
    if not done or done[0].get('questions_answered') != PER_ or done[0].get('questions_correct') != right:
        out.append('%s: game_completed counts %s, expected %d answered, %d correct' % (tag, done, PER_, right))
    qa = [p for n_, p in ev if n_ == 'question_answered']
    if len(qa) != PER_ or [p.get('question_id') for p in qa] != seen or any(p.get('mode') != evm or p.get('level') != 'year6' for p in qa):
        out.append('%s: question_answered %s, expected one per item with its id' % (tag, [p.get('question_id') for p in qa]))
    names = sorted({n for n, _ in ev})
    if not set(names) <= EVENTS:
        out.append('%s: events %s (only %s)' % (tag, names, sorted(EVENTS)))
    blobtxt = json.dumps(ev)
    for bad in ('kids', 'Example', '#'):
        if bad in blobtxt:
            out.append('%s: an mfg() payload contains %r' % (tag, bad))
    if bad_in_storage(page):
        out.append('%s: browser storage holds %s' % (tag, bad_in_storage(page)))
    if page.evaluate("document.getElementById('endLine').textContent") != L['overtime_end']:
        out.append('%s: the end line reads %r, expected LINES.%s.overtime_end' % (tag, page.evaluate("document.getElementById('endLine').textContent"), look))
    if page.evaluate("document.getElementById('resScore').textContent") != str(right) or \
            page.evaluate("document.getElementById('resOf').textContent") != '%d answered' % PER_:
        out.append('%s: the end screen does not show %d and "%d answered"' % (tag, right, PER_))
    page.evaluate("document.getElementById('menuBtn').click()")


# ---------------------------------------------------------------- winner stays on and the Stage 3 scaffold
def hud(page):
    return page.evaluate("""() => ({ q: document.getElementById('hudQ').textContent, end: !document.getElementById('endBtn').hidden,
        endShown: document.getElementById('endBtn').getBoundingClientRect().width > 0, state: ST.ui.state(), score: ST.ui.score(),
        qi: ST.ui.qi(), id: (ST.ui.question() || {}).id })""")


def check_winner(page, look, out):
    tag = look + ' winner'
    # (1) 10 right, then a wrong at 11: the run ends there, 11 answered, score 10, submitted once.
    page.evaluate("() => { window.__ev = []; window.__sub = []; }")
    page.evaluate("ST.ui.start('main-4')")
    ids = []
    for k in range(1, 12):
        h = hud(page)
        ids.append(h['id'])
        if h['qi'] != k:
            out.append('%s: question %d is numbered %s' % (tag, k, h['qi']))
            return
        want_q = '%d/10' % k if k <= 10 else str(k)
        if h['q'] != want_q:
            out.append('%s: the HUD reads %r at question %d, expected %r' % (tag, h['q'], k, want_q))
        if h['end'] != (k > 10) or (k > 10 and not h['endShown']):
            out.append('%s: the End button is %s at question %d' % (tag, 'shown' if h['end'] else 'hidden', k))
        page.evaluate('(r) => ST.ui.answer(r)', k <= 10)
        if k == 11:
            nb = page.evaluate("(document.querySelector('#feedback .maffs-next') || {}).textContent || ''")
            if 'See results' not in nb:
                out.append('%s: after the wrong at question 11 the button reads %r, expected "See results →"' % (tag, nb))
        page.evaluate('ST.ui.next()')
    st = page.evaluate('ST.ui.state()')
    sub = page.evaluate('window.__sub')
    if st != 'over' or page.evaluate('ST.ui.answered()') != 11 or page.evaluate('ST.ui.score()') != 10:
        out.append('%s: 10 right then a wrong: state %s, %d answered, score %d; expected over, 11, 10' % (tag, st, page.evaluate('ST.ui.answered()'), page.evaluate('ST.ui.score()')))
    if sub != [[SLUG, 'stage-4', 10, 11]]:
        out.append('%s: 10 right then a wrong: the leaderboard got %s, expected [[%r, stage-4, 10, 11]]' % (tag, sub, SLUG))
    page.evaluate("document.getElementById('menuBtn').click()")

    # (2) a wrong at question 3 does not end the run; (3) End at question 12 ends it with the score so far.
    page.evaluate("() => { window.__ev = []; window.__sub = []; }")
    page.evaluate("ST.ui.start('pro-1')")
    right = 0
    for k in range(1, 12):
        ok = k != 3
        page.evaluate('(r) => ST.ui.answer(r)', ok)
        right += ok
        page.evaluate('ST.ui.next()')
        if k == 3 and page.evaluate('ST.ui.state()') == 'over':
            out.append('%s: a wrong answer at question 3 ended the run' % tag)
            return
    h = hud(page)
    if h['qi'] != 12 or not h['end']:
        out.append('%s: at question 12 the run is at %s, End %s' % (tag, h['qi'], 'shown' if h['end'] else 'hidden'))
        return
    page.evaluate('ST.ui.end()')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in page.evaluate('window.__ev') if n == 'game_completed']
    if page.evaluate('ST.ui.state()') != 'over' or sub != [[SLUG, 'pro-stage-1', right, 11]] or len(done) != 1 or \
            done[0].get('questions_answered') != 11 or done[0].get('questions_correct') != right:
        out.append('%s: End at question 12: state %s, board %s, game_completed %s; expected score %d of 11 answered, once' % (tag, page.evaluate('ST.ui.state()'), sub, done, right))
    page.evaluate("document.getElementById('menuBtn').click()")

    # (4) the supply: no repeat until every item is used, never the item just answered (main Stage 1 has 22).
    # And the crowd (SOME-THINGIES-PERSONALITY): none in questions 1-10; from 11 the cheer, and one thingy more per right
    # answer after question 10, the next colour in order, every one drawn (CROWD-FILL: no cap, no "+n"); the score is the
    # game's, never the crowd's; the run-ending wrong answer makes the crowd faint, with the faint line.
    Lw = page.evaluate('ST.lines()')[look]
    CROWD_JS = """() => { const c = document.getElementById('crowd'); const m = document.getElementById('crowdMore');
        return { n: c.querySelectorAll('svg.th').length, more: m ? m.textContent : null, line: (document.getElementById('crowdLine') || {}).textContent || null,
                 faint: c.classList.contains('faint'), ks: [...c.querySelectorAll('svg.th')].map(t => +((t.getAttribute('class').match(/\\bk(\\d+)\\b/) || [])[1])) }; }"""
    page.evaluate("ST.ui.start('main-1')")
    ids = []
    for k in range(1, 63):
        ids.append(page.evaluate('ST.ui.question().id'))
        page.evaluate('ST.ui.answer(true)')
        c = page.evaluate(CROWD_JS)
        want = max(0, k - 10)
        shown = want
        if c['n'] != want or c['more'] is not None:
            out.append('%s: after %d right the crowd draws %d thingies and %r, expected %d and no "+n"' % (tag, k, c['n'], c['more'], want))
            break
        if c['ks'] != [(j % 10) + 1 for j in range(shown)]:
            out.append('%s: after %d right the crowd\'s colours are %s, not the fixed order' % (tag, k, c['ks'][:12]))
            break
        if k > 10 and c['line'] != cheer_for(look, want):
            out.append('%s: with %d in the crowd the cheer is %r, expected %r' % (tag, want, c['line'], cheer_for(look, want)))
            break
        if page.evaluate('ST.ui.score()') != k:
            out.append('%s: after %d right the score is %d (the crowd must never change it)' % (tag, k, page.evaluate('ST.ui.score()')))
            break
        page.evaluate('ST.ui.next()')
    if len(set(ids[:22])) != 22:
        out.append('%s: the first 22 questions repeat an item before all are used' % tag)
    for a, b in zip(ids, ids[1:]):
        if a == b:
            out.append('%s: %s served twice in a row' % (tag, a))
            break
    page.evaluate('() => { window.__sub = []; }')
    page.evaluate('ST.ui.answer(false)')
    c = page.evaluate(CROWD_JS)
    if not c['faint'] or c['line'] != Lw['faint'] or c['n'] != 52:
        out.append('%s: the run-ending wrong: crowd faint %s, line %r, %d shown; expected fainted, LINES.%s.faint, 52' % (tag, c['faint'], c['line'], c['n'], look))
    still(page, '%s (the crowd fainted)' % tag, out)
    page.evaluate('ST.ui.next()')
    if page.evaluate('ST.ui.score()') != 62 or page.evaluate('window.__sub') != [[SLUG, 'stage-1', 62, 63]]:
        out.append('%s: 62 right then a wrong: score %d, board %s; expected 62 of 63' % (tag, page.evaluate('ST.ui.score()'), page.evaluate('window.__sub')))
    page.evaluate("document.getElementById('menuBtn').click()")

    # (5) the Stage 3 scaffold: questions 1-4 three steps, 5-7 two (the rows label from the start), 8+ the total only;
    # each step labels the array with the right number, right or wrong, and never changes the score.
    L = page.evaluate('ST.lines()')[look]
    page.evaluate("ST.ui.start('pro-3')")
    for k in range(1, 13):
        q = page.evaluate('ST.ui.question()')
        lab = lambda: page.evaluate(SCREEN_JS)['arr']
        rows_lab, cols_lab = L['label_rows'].replace('{n}', str(q['rows'])), L['label_cols'].replace('{n}', str(q['cols']))
        want = ['rows', 'cols', 'ask'] if k <= 4 else ['cols', 'ask'] if k <= 7 else ['ask']
        got = []
        a0 = lab()
        if k in (5, 6, 7) and a0['side'] != rows_lab:
            out.append('%s question %d: the rows label is %r at the start, expected %r' % (tag, k, a0['side'], rows_lab))
        if k >= 8 and (a0['side'] or a0['top']):
            out.append('%s question %d: labels %r / %r with no steps' % (tag, k, a0['side'], a0['top']))
        for _ in range(4):
            s = page.evaluate('ST.ui.state()')
            got.append(s)
            if s == 'ask':
                break
            before = page.evaluate('ST.ui.score()')
            v = q['rows'] if s == 'rows' else q['cols']
            wrong_step = k % 2 == 0
            page.evaluate('(v) => ST.ui.step(v)', str(v + 1 if wrong_step else v))
            if page.evaluate('ST.ui.score()') != before:
                out.append('%s question %d: a step changed the score (%d -> %d)' % (tag, k, before, page.evaluate('ST.ui.score()')))
            a1 = lab()
            want_lab = rows_lab if s == 'rows' else cols_lab
            if (a1['side'] if s == 'rows' else a1['top']) != want_lab:
                out.append('%s question %d: after the %s step the label reads %r, expected %r' % (tag, k, s, a1['side'] if s == 'rows' else a1['top'], want_lab))
        if got != want:
            out.append('%s question %d: the steps were %s, expected %s' % (tag, k, got, want))
        before = page.evaluate('ST.ui.score()')
        page.evaluate('ST.ui.answer(true)')
        if page.evaluate('ST.ui.score()') != before + 1:
            out.append('%s question %d: the total right scored %d' % (tag, k, page.evaluate('ST.ui.score()') - before))
        page.evaluate('ST.ui.next()')
    page.evaluate('ST.ui.end()')
    page.evaluate("document.getElementById('menuBtn').click()")


# ---------------------------------------------------------------- CROWD-FILL
# The crowd as drawn, measured from the DOM: how many thingies, their sizes, the card's end against the fold, whether one
# half pixel more would fit (set here, measured, put back), and everything in the card above the crowd with the crowd in
# and with it taken out.
CROWD_FILL_JS = r"""() => { const $ = (id) => document.getElementById(id);
  const c = $('crowd'), card = $('qcard'), ths = [...c.querySelectorAll('svg.th')];
  const f = document.querySelector('.site-footer');
  const fold = innerHeight - (f && getComputedStyle(f).position === 'fixed' ? f.getBoundingClientRect().height : 0);
  const end = () => card.getBoundingClientRect().bottom + scrollY;
  const ws = ths.map(t => t.getBoundingClientRect().width), hs = ths.map(t => t.getBoundingClientRect().height);
  const w = ws.length ? Math.min(...ws) : 0, wmax = ws.length ? Math.max(...ws) : 0;
  const line = $('crowdLine');
  const o = { n: ths.length, w: w, wmax: wmax, hmin: hs.length ? Math.min(...hs) : 0, hmax: hs.length ? Math.max(...hs) : 0,
              end: end(), fold: fold, fits: end() <= fold + 0.5, line: line ? line.textContent : null,
              other: c.textContent.replace(line ? line.textContent : '', '').trim(), more: !!c.querySelector('.more, #crowdMore'),
              faint: c.classList.contains('faint'), scrolls: document.documentElement.scrollHeight > innerHeight,
              order: ths.every((t, i) => (t.getAttribute('class') || '').split(/\s+/).includes('k' + ((i % 10) + 1))),
              shown: getComputedStyle(c).display !== 'none' };
  const above = () => { const a = []; for (let e = card.firstElementChild; e && e !== c; e = e.nextElementSibling) { const r = e.getBoundingClientRect();
      a.push([e.id || e.className, Math.round(r.left * 10), Math.round((r.top + scrollY) * 10), Math.round(r.width * 10), Math.round(r.height * 10)]); }
    const nb = document.querySelector('#feedback .maffs-next, #nextBtn'); if (nb) { const r = nb.getBoundingClientRect(); a.push(['Next', Math.round(r.left * 10), Math.round((r.top + scrollY) * 10), Math.round(r.width * 10), Math.round(r.height * 10)]); }
    return a; };
  const withCrowd = above();
  o.aboveEnd = Math.max(...withCrowd.map(r => (r[2] + r[4]) / 10));
  o.top = c.getBoundingClientRect().top + scrollY;
  if (ths.length && w < 16) { const was = c.style.getPropertyValue('--ts'); c.style.setProperty('--ts', (w + 0.5) + 'px'); o.biggerFits = end() <= fold + 0.5; c.style.setProperty('--ts', was); }
  const d = c.style.display; c.style.display = 'none'; const without = above(); c.style.display = d;
  o.moved = withCrowd.filter((r, i) => JSON.stringify(r) !== JSON.stringify(without[i])).map(r => r[0]);
  return o; }"""
FRAMES_JS = "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"


def crowd_judge(tag, c, want, look, out, seen, cheer=True):
    """One view of the crowd against the contract. Returns False at the first finding (the unit stops there)."""
    n0 = len(out)
    if c['n'] != want or c['more'] or c['other']:
        out.append('%s: the crowd draws %d thingies%s, expected %d and no "+n"' % (tag, c['n'], (' and %r' % c['other']) if c['other'] or c['more'] else '', want))
    elif want and not c['order']:
        out.append('%s: the crowd\'s colours are not in the fixed order' % tag)
    elif want:
        if c['w'] < 6 - 0.01 or c['hmin'] < 6 - 0.01:
            out.append('%s: thingies are drawn at %.1f px, below the 6 px floor (%d in the crowd)' % (tag, min(c['w'], c['hmin']), want))
        elif c['wmax'] - c['w'] > 0.01 or c['hmax'] - c['hmin'] > 0.01 or abs(c['w'] - c['hmin']) > 0.01 or c['wmax'] > 16.01:
            out.append('%s: thingies are not one size (%.1f to %.1f px wide, %.1f to %.1f px tall; 16 px at most)' % (tag, c['w'], c['wmax'], c['hmin'], c['hmax']))
        elif c['w'] > 15.99:
            seen.add('full')
            if not c['fits']:
                out.append('%s: %d thingies at 16 px end at %.0f px, past the fold at %.0f px: they should have shrunk' % (tag, want, c['end'], c['fold']))
        elif c['biggerFits']:
            out.append('%s: %d thingies are %.1f px though %.1f px fits above the fold: shrunk further than the room needs' % (tag, want, c['w'], c['w'] + 0.5))
        elif c['fits']:
            seen.add('shrunk')
        elif c['w'] > 6.01:
            out.append('%s: %d thingies at %.1f px end at %.0f px, past the fold at %.0f px, above the 6 px floor' % (tag, want, c['w'], c['end'], c['fold']))
        else:
            seen.add('floor')
    if len(out) == n0 and c['moved']:
        out.append('%s: with %d in the crowd, %s is not where it is without the crowd' % (tag, want, ', '.join(c['moved'])))
    if len(out) == n0 and c['shown'] and c['top'] < c['aboveEnd'] - 0.5:
        out.append('%s: the crowd starts at %.0f px, over the card\'s content, which ends at %.0f px' % (tag, c['top'], c['aboveEnd']))
    if len(out) == n0 and cheer and c['line'] != cheer_for(look, want):
        out.append('%s: with %d in the crowd the cheer is %r, expected %r' % (tag, want, c['line'], cheer_for(look, want)))
    return len(out) == n0


def check_crowd(pw, base, html, look, size, mode, out, info):
    tag = 'crowd %s %dx%d' % (look, size[0], size[1])
    br, page, errs = open_page(pw, base, html, size, '#kids/Example' if look == 'kids' else '')
    seen, cheered = set(), set()
    view = lambda: (page.evaluate(FRAMES_JS), page.evaluate(CROWD_FILL_JS))[1]
    results = lambda: page.evaluate("""() => { const e = document.getElementById('collected');
        return { on: document.getElementById('results').classList.contains('active'), hidden: e.hidden || getComputedStyle(e).display === 'none', text: e.textContent,
                 after: !!(document.getElementById('endLine').compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING) }; }""")
    try:
        L = page.evaluate('ST.lines()')[look]
        note = page.evaluate("document.getElementById('menuNote').textContent")
        if note != MENU_NOTE:
            out.append('%s: the menu note reads %r, expected the contract\'s' % (tag, note))
        # No crowd, no line: 10 right, a slip at 11.
        page.evaluate("(m) => ST.ui.start(m)", mode)
        for k in range(1, 12):
            if k == 11:
                say = page.evaluate("document.getElementById('say').textContent")
                if say != L['overtime'] or TAGLINE not in say.lower():
                    out.append('%s: at question 11 the line is %r, expected LINES.%s.overtime with Jon\'s tagline' % (tag, say, look))
            page.evaluate('(r) => ST.ui.answer(r)', k <= 10)
            page.evaluate('ST.ui.next()')
        r = results()
        if not r['on'] or not r['hidden'] or r['text']:
            out.append('%s: a run with no crowd: the results screen\'s collected line is %r (hidden %s), expected none' % (tag, r['text'], r['hidden']))
        page.evaluate("document.getElementById('menuBtn').click()")
        # One thingy: 11 right, a slip at 12.
        page.evaluate("(m) => ST.ui.start(m)", mode)
        for k in range(1, 13):
            page.evaluate('(r) => ST.ui.answer(r)', k <= 11)
            page.evaluate('ST.ui.next()')
        r = results()
        if not r['on'] or r['hidden'] or r['text'] != collected_line(look, 1) or not r['after']:
            out.append('%s: a run with one in the crowd: the results screen reads %r (hidden %s), expected %r under the end line' % (tag, r['text'], r['hidden'], collected_line(look, 1)))
        page.evaluate("document.getElementById('menuBtn').click()")

        # The long run: 135 right answers, the crowd judged after each answer and on each new question.
        page.evaluate("(m) => ST.ui.start(m)", mode)
        ok = True
        for k in range(1, 136):
            want = max(0, k - 10)
            page.evaluate('ST.ui.answer(true)')
            if want == 120:
                # Drawing and sizing the crowd of 120, laid out: the median of five.
                ms = page.evaluate("""() => { const ts = []; for (let i = 0; i < 5; i++) { const t = performance.now(); ST.ui.crowd(120); document.body.offsetHeight; ts.push(performance.now() - t); }
                    return ts.sort((a, b) => a - b)[2]; }""")
                info.setdefault('crowd ms', []).append(ms)
                if ms > 500:
                    out.append('%s: drawing the crowd of 120 took %.0f ms' % (tag, ms))
            c = view()
            if k <= 10:
                if c['n'] or c['line'] is not None:
                    out.append('%s: a crowd (%d thingies, line %r) at question %d' % (tag, c['n'], c['line'], k))
                    ok = False
            else:
                ok = crowd_judge('%s after %d right' % (tag, k), c, want, look, out, seen)
                cheered.add(want)
            if ok and page.evaluate('ST.ui.score()') != k:
                out.append('%s: after %d right the score is %d (the crowd must never change it)' % (tag, k, page.evaluate('ST.ui.score()')))
                ok = False
            if not ok:
                break
            if want in (1, 55, 125):
                check_thingies(page, '#crowd', mode.startswith('pro'), '%s (%d in the crowd)' % (tag, want), out)
            page.evaluate('ST.ui.next()')
            if k >= 10 and not crowd_judge('%s question %d' % (tag, k + 1), view(), want, look, out, seen):
                ok = False
                break
        if ok and not {0, 1, 9, 10, 20, 30, 50, 75, 100} <= (cheered | {0}):
            out.append('%s: the cheer was not checked at every threshold' % tag)
        if ok:
            # Thousands, by the page's hook, until full size, shrunk to fit and the floor have each been seen.
            for n in (300, 700, 1500, 3000, 6000, 12000):
                if page.evaluate('(n) => ST.ui.crowd(n)', n) != n:
                    out.append('%s: ST.ui.crowd(%d) did not set the crowd' % (tag, n))
                    ok = False
                    break
                c = view()
                ok = crowd_judge('%s at %d' % (tag, n), c, n, look, out, seen)
                if not ok:
                    break
                if 'shrunk' in seen and n <= 3000 and c['w'] < 15.99:
                    check_thingies(page, '#crowd', mode.startswith('pro'), '%s (%d in the crowd, %.1f px)' % (tag, n, c['w']), out)
                if 'floor' in seen:
                    if not c['scrolls']:
                        out.append('%s at %d: at the floor, past the fold, the page does not scroll' % (tag, n))
                    break
            if ok and seen != {'full', 'shrunk', 'floor'}:
                out.append('%s: saw only %s of full size, shrunk to fit and the floor' % (tag, sorted(seen)))
        if ok:
            # A shorter window shrinks it (resize); the first size brings it back; back at 125 it is 16 px again.
            page.evaluate('ST.ui.crowd(300)')
            a = view()
            # Short enough that the crowd as it is ends 40 px past the new fold (or 200 px shorter, if that is shorter),
            # and HOST_MAX px more: the character beside the question gives way first (SOME-THINGIES-HOST), which can
            # free up to that much before the crowd has to shrink.
            page.set_viewport_size({'width': size[0], 'height': int(min(size[1] - 200, size[1] - (a['fold'] - a['end']) - 40 - HOST_MAX))})
            b = view()
            ok = crowd_judge('%s at 300, the window shorter' % tag, b, 300, look, out, seen)
            if ok and not b['w'] < a['w']:
                out.append('%s: 300 thingies are %.1f px, and %.1f px in a shorter window: not re-measured on resize' % (tag, a['w'], b['w']))
            page.set_viewport_size({'width': size[0], 'height': size[1]})
            page.evaluate('ST.ui.crowd(125)')
            c = view()
            ok = ok and crowd_judge('%s back at 125' % tag, c, 125, look, out, seen)
        if ok:
            # The slip: the crowd faints, whole; then the results screen counts it.
            page.evaluate('ST.ui.answer(false)')
            c = view()
            if not c['faint'] or c['line'] != L['faint']:
                out.append('%s: the run-ending wrong: crowd faint %s, line %r; expected fainted, LINES.%s.faint' % (tag, c['faint'], c['line'], look))
            crowd_judge('%s fainted' % tag, c, 125, look, out, seen, cheer=False)
            still(page, '%s (the crowd fainted)' % tag, out)
            page.evaluate('ST.ui.next()')
            r = results()
            if not r['on'] or r['hidden'] or r['text'] != collected_line(look, 125) or not r['after']:
                out.append('%s: after 125 in the crowd the results screen reads %r (hidden %s), expected %r under the end line' % (tag, r['text'], r['hidden'], collected_line(look, 125)))
            if page.evaluate('ST.ui.score()') != 135:
                out.append('%s: 135 right then a slip: the score is %d' % (tag, page.evaluate('ST.ui.score()')))
    except Exception as e:  # noqa: BLE001
        out.append('%s threw: %s' % (tag, str(e).splitlines()[0][:220]))
    out.extend('page error (%s): %s' % (tag, e) for e in errs if 'production host' not in e)
    br.close()
    info['crowd'] = info.get('crowd', 0) + 1


# SOME-THINGIES-FACTS. A list of plays in one call (as fit_common's sweep: a round trip a play would cost more than the
# plays). Each play is one Stage 4 item, played once: previewed as question `at` (past question 10 with `crowd` in the
# crowd), read before marking, answered (right with the given LINES.right line, or the first decoy), read again, then
# Next and read a third time. Everything is read from the DOM. g and n are this script's own plates and thingies a
# plate (never the page's). Where the page shows no picture, a stand-in the size of the picture at the 10 px floor
# (the plates' boxes, from the CSS: thingies 10 px, gaps a ninth, padding 1/4.5 and 1/3.6, a 2 px border, a third
# between plates) is put where the picture goes, to see whether it really would not fit. The crowd is judged with the
# picture hidden: the size CROWD-FILL gives the card without it. Two frames are waited after the marking of every play
# past question 10 and of one play in 20 before it, so what the page changes after the marking itself (its
# ResizeObserver) is read too; the other plays are read at once, as the student first sees them.
FACT_JS = r"""async (plays) => { const all = []; let count = 0;
 for (const [id, right, line, at, crowd, g, n] of plays) { all.push(await (async () => {
  const $ = (i) => document.getElementById(i);
  const frames = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const f = document.querySelector('.site-footer');
  const fold = () => innerHeight - (f && getComputedStyle(f).position === 'fixed' ? f.getBoundingClientRect().height : 0);
  const card = $('qcard'), p = $('pic'), c = $('crowd');
  const end = () => card.getBoundingClientRect().bottom + scrollY;
  // The character beside the question: the quiz-show host where the card is .host-big (SOME-THINGIES-HOST), else the top row's.
  const mini = () => { const m = card.classList.contains('host-big') ? $('host') : $('sargeMini'), ths = [...m.querySelectorAll('svg')], t = ths[0] || null, r = t ? t.getBoundingClientRect() : null;
    const on = (sel) => !!t && !!t.querySelector(sel) && getComputedStyle(t.querySelector(sel)).display !== 'none';
    return { n: ths.length, acc: t ? (t.dataset.acc || null) : null, k: t ? +(((t.getAttribute('class') || '').match(/\bk(\d+)\b/) || [])[1] || 0) : 0,
             lenses: t ? t.querySelectorAll('.a-lens').length : 0, medal: !!(t && t.querySelector('.medal')), text: m.textContent.trim(),
             vis: !!r && r.width >= 16 && r.height >= 16 && getComputedStyle(m).display !== 'none' && getComputedStyle(m).visibility !== 'hidden' && r.top >= 0 && r.bottom + scrollY <= fold() && r.left >= 0 && r.right <= innerWidth,
             right: m.classList.contains('react-right'), wrong: m.classList.contains('react-wrong'), happy: on('.m-happy'), puzzled: on('.m-puzzled'), wait: on('.m-wait') }; };
  const pic = () => { const pls = [...p.querySelectorAll('.plate')], ths = [...p.querySelectorAll('svg.th')];
    const ws = ths.map(t => t.getBoundingClientRect().width), hs = ths.map(t => t.getBoundingClientRect().height);
    const pr = p.getBoundingClientRect(), cr = card.getBoundingClientRect();
    const ks = pls.map(x => [...new Set([...x.querySelectorAll('svg.th')].map(t => ((t.getAttribute('class') || '').match(/\bk(\d+)\b/) || [])[1]))].join(','));
    const inside = pls.every(x => { const b = x.getBoundingClientRect(); return [...x.querySelectorAll('svg.th')].every(t => { const r = t.getBoundingClientRect(); return r.left >= b.left - 0.5 && r.right <= b.right + 0.5 && r.top >= b.top - 0.5 && r.bottom <= b.bottom + 0.5; }); });
    return { plates: pls.map(x => x.querySelectorAll('svg.th').length), thingies: ths.length, kids: p.children.length, text: p.textContent.trim(), ks: ks, inside: inside,
             wmin: ws.length ? Math.min(...ws) : 0, wmax: ws.length ? Math.max(...ws) : 0, hmin: hs.length ? Math.min(...hs) : 0, hmax: hs.length ? Math.max(...hs) : 0,
             wider: ths.length ? (pr.left < cr.left - 0.5 || pr.right > cr.right + 0.5) : false, top: pr.top + scrollY, bottom: pr.bottom + scrollY,
             right: p.classList.contains('react-right'), wrong: p.classList.contains('react-wrong') }; };
  const crowdNow = () => { const ths = [...c.querySelectorAll('svg.th')], ws = ths.map(t => t.getBoundingClientRect().width);
    return { n: ths.length, w: ws.length ? Math.min(...ws) : 0, wmax: ws.length ? Math.max(...ws) : 0, end: end(), fold: fold() }; };
  ST.ui.preview(id, at);
  if (at > 10) ST.ui.crowd(crowd);
  const q = ST.ui.question();
  const o = { id: q ? q.id : null, qi: ST.ui.qi(), quiz: card.classList.contains('quiz'), before: { mini: mini(), pic: pic(), crowd: crowdNow(), state: ST.ui.state() } };
  if (right) ST.ui.answer(true, line); else ST.ui.answer(false);
  if (at > 10 || count++ % 20 === 0) await frames();
  const nb = document.querySelector('#feedback .maffs-next, #nextBtn');
  const sayEl = $('say'), fbEl = $('feedback');
  o.after = { mini: mini(), pic: pic(), crowd: crowdNow(), state: ST.ui.state(), next: nb ? nb.getBoundingClientRect().bottom + scrollY : null, fold: fold(),
              sideways: document.documentElement.scrollWidth - innerWidth, fact: p.dataset.fact || null,
              optsEnd: $('opts').getBoundingClientRect().bottom + scrollY, fbTop: fbEl.getBoundingClientRect().top + scrollY };
  const hasCrowd = o.after.crowd.n > 0;
  const over = () => !nb || nb.getBoundingClientRect().bottom + scrollY > fold() + 0.5 || (hasCrowd && end() > fold() + 0.5);
  if (o.after.pic.plates.length) {
    // Shrunk: one pixel more must not fit.
    if (o.after.pic.wmin < 17.99) { const was = p.style.getPropertyValue('--ps'); p.style.setProperty('--ps', (Math.round(o.after.pic.wmin) + 1) + 'px'); o.after.biggerFits = !over(); p.style.setProperty('--ps', was); }
  } else {
    const cols = n <= 5 ? n : Math.ceil(n / 2), rows = n <= 5 ? 1 : 2, s = 10;
    const box = document.createElement('div');
    box.style.cssText = 'display:flex;flex-wrap:wrap;justify-content:center;align-items:center;max-width:100%;order:1;gap:' + (s / 3) + 'px';
    for (let i = 0; i < g; i++) { const d = document.createElement('div'); d.style.cssText = 'flex:none;box-sizing:border-box;width:' + (cols * s + (cols - 1) * s / 9 + 2 * s / 3.6 + 4) + 'px;height:' + (rows * s + (rows - 1) * s / 9 + 2 * s / 4.5 + 4) + 'px'; box.appendChild(d); }
    card.insertBefore(box, p);
    o.after.floorFits = !over();
    box.remove();
  }
  // The crowd, with the picture hidden: full size and fitting, or the largest half pixel that fits, or the floor.
  if (hasCrowd) { const d = p.style.display; p.style.display = 'none';
    const cw = o.after.crowd.w, was = c.style.getPropertyValue('--ts');
    o.after.bare = { fits: end() <= fold() + 0.5 };
    if (cw < 15.99) { c.style.setProperty('--ts', (cw + 0.5) + 'px'); o.after.bare.biggerFits = end() <= fold() + 0.5; c.style.setProperty('--ts', was); }
    p.style.display = d; }
  ST.ui.next();
  o.then = { mini: mini(), pic: pic(), state: ST.ui.state() };
  return o; })()); }
 return all; }"""


def fact_plates(q):
    """This script's own picture for a Stage 4 item: (plates, thingies a plate). a x b is a plates of b; ? x b = product
    is product / b plates of b."""
    return (q['a'], q['b']) if q['type'] == 'fact' else (q['product'] // q['b'], q['b'])


def fact_judge(tag, q, right, at, crowd, o, pro, out):
    """One Stage 4 play against the contract. Returns 'shown' or 'dropped' (None when the play itself went wrong)."""
    g, n = fact_plates(q)
    if o['id'] != q['id'] or o['qi'] != at or o['before']['state'] != 'ask' or o['after']['state'] != ('done' if right else 'wrong'):
        out.append('%s: the play went wrong (item %s, question %s, states %s then %s)' % (tag, o['id'], o['qi'], o['before']['state'], o['after']['state']))
        return None
    # The thingy beside the question.
    # (Past question 10 a wrong answer ends the run: Next goes to the results, so there is no next question to read.)
    ended = at > PER and not right
    b, a, t = o['before']['mini'], o['after']['mini'], o['then']['mini']
    for when, m in (('before marking', b), ('after marking', a)) + (() if ended else (('on the next question', t),)):
        if m['n'] != 1 or m['acc'] != 'glasses' or m['k'] != 6 or m['lenses'] != 2 or m['text']:
            out.append('%s: %s the thingy beside the question is %d thingies (accessory %s, colour %s, %d lenses, text %r), expected one in glasses and no text'
                       % (tag, when, m['n'], m['acc'], m['k'], m['lenses'], m['text']))
            return None
        if m['medal'] != pro:
            out.append('%s: %s the thingy beside the question %s a medal in %s mode' % (tag, when, 'wears' if m['medal'] else 'has no', 'pro' if pro else 'main'))
            return None
        if not m['vis']:
            out.append('%s: %s the thingy beside the question is not on screen (hidden, under 16 px or off the first screen)' % (tag, when))
            return None
    for when, m in (('before marking', b),) + (() if ended else (('on the next question', t),)):
        if m['right'] or m['wrong'] or m['happy'] or m['puzzled'] or not m['wait']:
            out.append('%s: %s the thingy beside the question already reacts (react-right %s, react-wrong %s)' % (tag, when, m['right'], m['wrong']))
    how = 'right' if right else 'wrong'
    if a['right'] != right or a['wrong'] == right or a['happy'] != right or a['puzzled'] == right or a['wait']:
        out.append('%s: the thingy beside the question does not react after a %s answer (react-right %s, react-wrong %s; smiling %s, puzzled %s)'
                   % (tag, how, a['right'], a['wrong'], a['happy'], a['puzzled']))
    # The picture: none before marking or on the next question; after marking, g plates of n, or none.
    for when, pc_ in (('before marking', o['before']['pic']),) + (() if ended else (('on the next question', o['then']['pic']),)):
        if pc_['thingies'] or pc_['kids'] or pc_['text']:
            out.append('%s: a picture %s (%d plates, %d thingies): it gives the answer away' % (tag, when, len(pc_['plates']), pc_['thingies']))
    pic_, res = o['after']['pic'], 'dropped'
    if pic_['plates'] or pic_['thingies'] or pic_['kids']:
        res = 'shown'
        if pic_['plates'] != [n] * g or pic_['thingies'] != g * n or pic_['kids'] != g or pic_['text']:
            out.append('%s: after marking the picture draws %d plates of %s (%d thingies), expected %d plates of %d'
                       % (tag, len(pic_['plates']), sorted(set(pic_['plates'])) or 0, pic_['thingies'], g, n))
        elif pic_['ks'] != [str((i % 10) + 1) for i in range(g)]:
            out.append('%s: the plates are not one colour each in the fixed order (%s)' % (tag, pic_['ks']))
        elif pic_['wmax'] - pic_['wmin'] > 0.01 or pic_['hmax'] - pic_['hmin'] > 0.01 or abs(pic_['wmin'] - pic_['hmin']) > 0.01:
            out.append('%s: the picture\'s thingies are not one size (%.1f to %.1f px wide, %.1f to %.1f px tall)' % (tag, pic_['wmin'], pic_['wmax'], pic_['hmin'], pic_['hmax']))
        elif pic_['wmin'] < 10 - 0.01 or pic_['wmax'] > 18.01:
            out.append('%s: the picture\'s thingies are %.1f px, outside 10 to 18 px' % (tag, pic_['wmin']))
        elif not pic_['inside']:
            out.append('%s: a thingy is drawn outside its plate at %.0f px' % (tag, pic_['wmin']))
        elif pic_['wider']:
            out.append('%s: the picture is wider than its card' % tag)
        elif o['after'].get('biggerFits'):
            out.append('%s: the picture is %.0f px though %.0f px fits: shrunk further than the room needs' % (tag, pic_['wmin'], pic_['wmin'] + 1))
        elif pic_['right'] != right or pic_['wrong'] == right:
            out.append('%s: the picture does not carry the %s reaction' % (tag, how))
        elif pic_['top'] < o['after']['optsEnd'] - 0.5 or pic_['bottom'] > o['after']['fbTop'] + 0.5:
            out.append('%s: the picture is not between the options and the working' % tag)
    elif o['after'].get('floorFits'):
        out.append('%s: no picture after marking, though %d plates of %d at 10 px would leave Next above the fold' % (tag, g, n))
    elif o['after']['fact'] != 'off':
        out.append('%s: no picture after marking and #pic does not say so (data-fact %r)' % (tag, o['after']['fact']))
    # Next, and the page's width.
    if o['after']['next'] is None:
        out.append('%s: no Next after marking' % tag)
    elif o['after']['next'] > o['after']['fold'] + 0.5:
        out.append('%s: Next ends at %.0f px, below the fold at %.0f px (picture %s%s)' % (tag, o['after']['next'], o['after']['fold'], res, (' at %.0f px' % pic_['wmin']) if res == 'shown' else ''))
    if o['after']['sideways'] > 0:
        out.append('%s: the page scrolls sideways by %d px after marking' % (tag, o['after']['sideways']))
    # The crowd: the size CROWD-FILL gives the card without the picture, and the picture inside the room it leaves.
    cr = o['after']['crowd']
    if at > 10 and cr['n']:
        bare = o['after']['bare']
        if cr['wmax'] - cr['w'] > 0.01:
            out.append('%s: the crowd of %d is not one size' % (tag, cr['n']))
        elif cr['w'] > 15.99 and not bare['fits']:
            out.append('%s: the crowd of %d is 16 px and, with the picture taken out, ends past the fold: it should have shrunk' % (tag, cr['n']))
        elif cr['w'] <= 15.99 and bare.get('biggerFits'):
            out.append('%s: the crowd of %d is %.1f px though %.1f px fits with the picture taken out: the picture changed the crowd\'s size' % (tag, cr['n'], cr['w'], cr['w'] + 0.5))
        elif cr['w'] <= 15.99 and cr['w'] > 6.01 and not bare['fits']:
            out.append('%s: the crowd of %d at %.1f px ends past the fold with the picture taken out' % (tag, cr['n'], cr['w']))
        elif res == 'shown' and cr['end'] > cr['fold'] + 0.5:
            out.append('%s: with the picture the card ends at %.0f px, past the fold at %.0f px: the picture does not fit the room the crowd of %d leaves' % (tag, cr['end'], cr['fold'], cr['n']))
    return res


def check_facts(pw, base, html, look, size, aa, out, info):
    """SOME-THINGIES-FACTS: every Stage 4 item, Main and Pro, in one look at one size, normal or Aa, the speaker showing
    (fit_common.open_phone: the real fonts, a local voice), right (the longest LINES.right line) and wrong."""
    tag = 'facts %s %dx%d %s' % (look, size[0], size[1], aa)
    br, page, errs = fc.open_phone(pw, base, html, SLUG, '!!window.ST && !!ST.ui', '#kids/Example' if look == 'kids' else '', size)
    try:
        if page.evaluate("document.body.classList.contains('look-kids')") != (look == 'kids'):
            out.append('%s: the page is not in the %s look' % (tag, look))
        if aa == 'Aa':
            page.evaluate("document.getElementById('a11yToggle').click()")
        if page.evaluate("document.body.classList.contains('accessible')") != (aa == 'Aa'):
            out.append('%s: the page is not in %s mode' % (tag, aa))
        page.evaluate('document.fonts.ready.then(() => 1)')
        lines = page.evaluate('ST.lines()')[look]['right']
        longest = max(range(len(lines)), key=lambda i: len(lines[i]))
        items = [q for q in page.evaluate('ST.bank()') if q['stage'] == 4]
        if len(items) != 192 or {q['type'] for q in items} != {'fact', 'missing'}:
            out.append('%s: %d Stage 4 items of types %s, expected 192 facts and missing numbers' % (tag, len(items), sorted({q['type'] for q in items})))
        n0, both, dropped, smallest = len(out), 0, [], 18.0
        # Past question 10 first: each mode's smallest fact and its largest (a x b, and the missing number) with 60 in
        # the crowd, the largest also with 1 and, after a wrong answer (the crowd stays as it was), with a crowd big
        # enough to have shrunk to fit, which must be seen. Each half of the unit stops once it has four findings.
        seen = Counter()
        for md in ('main', 'pro'):
            mine = sorted((q for q in items if q['mode'] == md), key=lambda q: (fact_plates(q)[0] * fact_plates(q)[1], q['id']))
            big = [x for x in mine if fact_plates(x)[0] * fact_plates(x)[1] == fact_plates(mine[-1])[0] * fact_plates(mine[-1])[1]]
            top = [x for x in big if x['type'] == 'fact'][0]
            cases = [(q, 60, r) for q in (mine[0], top, [x for x in big if x['type'] == 'missing'][0]) for r in (True, False)]
            cases += [(top, 1, True), (top, 1, False), (top, FACT_CROWD_BIG[size[0] > 600], False)]
            for q, crowd, right in cases:
                if len(out) - n0 > 3:
                    break
                g, n = fact_plates(q)
                o = page.evaluate(FACT_JS, [[q['id'], right, longest, 12, crowd, g, n]])[0]
                t2 = '%s %s as question 12, %d in the crowd (%s)' % (tag, q['id'], crowd, 'right' if right else 'wrong')
                if o['before']['crowd']['n'] != crowd or o['after']['crowd']['n'] != crowd + (1 if right else 0):
                    out.append('%s: the crowd holds %d then %d' % (t2, o['before']['crowd']['n'], o['after']['crowd']['n']))
                    continue
                res = fact_judge(t2, q, right, 12, crowd, o, md == 'pro', out)
                seen['picture %s' % res] += 1
                seen['crowd ' + ('the same size before and after marking' if abs(o['before']['crowd']['w'] - o['after']['crowd']['w']) < 0.01 else 'resized by the marking itself')] += 1
                if o['after']['crowd']['w'] < 15.99:
                    seen['crowd shrunk to fit'] += 1
        if len(out) == n0 and not seen['crowd shrunk to fit']:
            out.append('%s: no crowd was seen shrunk to fit (%d thingies): the picture was never tried against a full screen' % (tag, FACT_CROWD_BIG[size[0] > 600]))
        info.setdefault('facts crowd', []).append((tag, dict(seen)))
        # Every Stage 4 item as question 1, right and wrong.
        plays = [[q['id'], right, longest, 1, 0] + list(fact_plates(q)) for q in items for right in (True, False)]
        played, n1 = [], len(out)
        for i in range(0, len(plays), 64):
            if len(out) - n1 > 3:
                break
            played += page.evaluate(FACT_JS, plays[i:i + 64])
            for k in range(i // 2, len(played) // 2):
                q, got = items[k], []
                for right in (True, False):
                    o = played[2 * k + (0 if right else 1)]
                    if not o['quiz']:
                        out.append('%s %s: the card is not in its Stage 4 scene' % (tag, q['id']))
                    got.append(fact_judge('%s %s (%s)' % (tag, q['id'], 'right' if right else 'wrong'), q, right, 1, 0, o, q['mode'] == 'pro', out))
                    if got[-1] == 'shown':
                        smallest = min(smallest, o['after']['pic']['wmin'])
                if got == ['shown', 'shown']:
                    both += 1
                elif 'dropped' in got:
                    dropped.append(q['id'])
        if len(played) == len(plays):
            info.setdefault('facts', []).append((tag, both, len(dropped), len(items), smallest, ', '.join(dropped)))
        still(page, tag, out)
    except Exception as e:  # noqa: BLE001
        out.append('%s threw: %s' % (tag, str(e).splitlines()[0][:220]))
    out.extend('page error (%s): %s' % (tag, e) for e in errs if 'production host' not in e)
    br.close()


HOST_JS = r"""async (plays) => { const all = []; let count = 0;
 for (const [id, at, right, line, crowd, force] of plays) { all.push(await (async () => {
  const $ = (i) => document.getElementById(i);
  const frames = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const f = document.querySelector('.site-footer');
  const fold = () => innerHeight - (f && getComputedStyle(f).position === 'fixed' ? f.getBoundingClientRect().height : 0);
  const card = $('qcard'), p = $('pic'), c = $('crowd');
  const end = (e) => e.getBoundingClientRect().bottom + scrollY;
  const box = (e) => { const r = e.getBoundingClientRect(); return { l: r.left, r: r.right, t: r.top + scrollY, b: r.bottom + scrollY, w: r.width, h: r.height }; };
  // The character: which of the three places shows it, its drawn box, and where the question is.
  const who = () => { const els = { mini: $('sargeMini'), host: $('host'), wide: $('sargeWide') }, shown = [];
    for (const k of Object.keys(els)) { const e = els[k], t = e && e.querySelector('svg');
      if (t && getComputedStyle(e).display !== 'none' && t.getBoundingClientRect().width > 0) shown.push(k); }
    const k = shown[0], t = k ? els[k].querySelector('svg') : null, arr = $('arr'), w = p.querySelector('.arr-wrap');
    return { data: card.dataset.host || null, shown: shown, box: t ? box(t) : null, sarge: !!(t && t.classList.contains('sarge')),
             card: box(card), qhead: box(card.querySelector('.qhead')), sum: $('sum').textContent.trim() ? box($('sum')) : null,
             arr: arr ? box(arr) : null, wrap: w ? box(w) : null, pic: box(p), sumOver: $('sum').scrollWidth > $('sum').clientWidth + 1 }; };
  const optsLow = () => Math.max(0, ...[...document.querySelectorAll('#opts .opt, #opts1 .opt')].filter(b => b.offsetParent).map(end));
  const crowdNow = () => { const ths = [...c.querySelectorAll('svg.th')], ws = ths.map(t => t.getBoundingClientRect().width);
    return { n: ths.length, w: ws.length ? Math.min(...ws) : 0, wmax: ws.length ? Math.max(...ws) : 0 }; };
  const picNow = () => { const ths = [...p.querySelectorAll('.plate svg.th')];
    return { fact: p.dataset.fact || null, n: ths.length, w: ths.length ? ths[0].getBoundingClientRect().width : 0 }; };
  ST.ui.preview(id, at);
  if (at > 10) ST.ui.crowd(crowd);
  // A size forced here (0: the top row), after the page has chosen its own, to judge the page's choice against.
  if (force !== null) { card.classList.toggle('host-big', force > 0); if (force > 0) card.style.setProperty('--host', force + 'px'); card.dataset.host = force > 0 ? String(force) : 'mini'; }
  const q = ST.ui.question(), o = { id: q ? q.id : null, qi: ST.ui.qi(), fold: fold(), asks: [], sumH: $('sum').getBoundingClientRect().height };
  o.before = who(); o.crowdBefore = crowdNow();
  while (ST.ui.state() === 'rows' || ST.ui.state() === 'cols') { o.asks.push({ low: optsLow(), who: who() }); ST.ui.step(String(ST.ui.state() === 'rows' ? q.rows : q.cols)); }
  o.asks.push({ low: optsLow(), who: who() });
  // Stage 3: the array as it stands before it turns round, to show it again with the feedback (reduced motion turns it
  // at once, so the 780 ms a student sees it marked but not yet turned is built here).
  const was = p.querySelector('.arr-wrap') ? p.querySelector('.arr-wrap').cloneNode(true) : null;
  if (right) ST.ui.answer(true, line); else ST.ui.answer(false);
  if (at > 10 || count++ % 20 === 0) await frames();
  const nb = document.querySelector('#feedback .maffs-next, #nextBtn');
  o.after = who(); o.state = ST.ui.state(); o.next = nb ? end(nb) : null;
  // Sideways against the layout width: a phone zooms out to show what overflows, so innerWidth grows with it.
  o.sideways = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  o.crowd = crowdNow(); o.pic = picNow(); o.sumAfter = $('sum').getBoundingClientRect().height;
  if (was && nb) { const turned = [...p.childNodes]; p.replaceChildren(was); o.turning = end(nb); p.replaceChildren(...turned); }
  return o; })()); }
 return all; }"""
TALLEST_JS = r"""() => { const s = document.getElementById('say'), was = s.textContent, L = ST.lines()[ST.LOOK]['right'];
  let best = 0, top = -1; L.forEach((t, i) => { s.textContent = t; const h = s.getBoundingClientRect().height; if (h > top) { top = h; best = i; } });
  s.textContent = was; return best; }"""


def host_box(tag, o, when, w, q, out):
    """The character's size and place on one screen (SOME-THINGIES-HOST). Returns its size (0 for the top row) or None."""
    s3 = q['type'] == 'array'
    if w['data'] == 'mini':
        if w['shown'] != ['mini'] or not w['box'] or abs(w['box']['w'] - 22) > 0.5 or abs(w['box']['h'] - 22) > 0.5:
            out.append('%s %s: in the top row the character shows as %s (%s px), expected the top row\'s alone at 22 px'
                       % (tag, when, w['shown'], '%.1f' % w['box']['w'] if w['box'] else '-'))
            return None
        b, h = w['box'], w['qhead']
        if b['t'] < h['t'] - 0.5 or b['b'] > h['b'] + 0.5:
            out.append('%s %s: the character is not in the card\'s top row' % (tag, when))
        return 0
    try:
        sz = int(w['data'])
    except (TypeError, ValueError):
        out.append('%s %s: the card gives the character no size (data-host %r)' % (tag, when, w['data']))
        return None
    want = 'wide' if s3 else 'host'
    if not HOST_MIN <= sz <= HOST_MAX:
        out.append('%s %s: the character is given %d px, outside %d to %d' % (tag, when, sz, HOST_MIN, HOST_MAX))
    if w['shown'] != [want]:
        out.append('%s %s: at %d px the character shows as %s, expected %s alone' % (tag, when, sz, w['shown'], 'Sarge beside the array' if s3 else 'the host beside the sum'))
        return None
    b = w['box']
    if abs(b['w'] - sz) > 0.5 or abs(b['h'] - sz) > 0.5:
        out.append('%s %s: %s is drawn at %.0f px, not the %d px the card gives (one size for both characters)'
                   % (tag, when, 'Sarge' if s3 else 'the thingy in glasses', b['w'], sz))
    c = w['card']
    if b['l'] < c['l'] - 0.5 or b['r'] > c['r'] + 0.5:
        out.append('%s %s: the character is drawn outside the card' % (tag, when))
    if s3:
        a, wr, pc_ = w['arr'], w['wrap'], w['pic']
        if not a or b['l'] < a['r'] - 0.5 or b['t'] < wr['t'] - 0.5 or b['b'] > wr['b'] + 0.5:
            out.append('%s %s: Sarge is not beside the array' % (tag, when))
        elif any(x['l'] < pc_['l'] - 0.5 or x['r'] > pc_['r'] + 0.5 for x in (wr, a, b)):
            out.append('%s %s: the array and Sarge are wider than their room (the picture\'s width)' % (tag, when))
    else:
        m = w['sum']
        if not m or b['r'] > m['l'] + 0.5 or not b['t'] - 0.5 <= (m['t'] + m['b']) / 2 <= b['b'] + 0.5:
            out.append('%s %s: the thingy in glasses is not beside the sum line' % (tag, when))
        elif w['sumOver']:
            out.append('%s %s: beside the thingy in glasses the sum is wider than its room' % (tag, when))
    return sz


def host_play(tag, q, o, out, m=None):
    """One play's screens: (size, the fold's findings as (screen, end, fold)). Size None when the play went wrong. m: the
    same play with the character in the top row, against which Stage 3's marked array before it turns is judged: the
    character may not push Next lower there than the fold or than it is without it (a screen today's measurements, under
    reduced motion, never see)."""
    if o['id'] != q['id']:
        out.append('%s: the play went wrong (item %s)' % (tag, o['id']))
        return None, []
    sizes, lost = [], []
    for k, a in enumerate(o['asks']):
        sizes.append(host_box(tag, o, 'asking (screen %d)' % (k + 1), a['who'], q, out))
        if a['low'] > o['fold'] + 0.5:
            lost.append(('the options on asking screen %d' % (k + 1), a['low']))
    sizes.append(host_box(tag, o, 'after marking', o['after'], q, out))
    if o['next'] is None:
        out.append('%s: no Next after marking' % tag)
    elif o['next'] > o['fold'] + 0.5:
        lost.append(('Next', o['next']))
    if o['sideways'] > 0:
        lost.append(('the page (sideways by %d px)' % o['sideways'], o['fold'] + o['sideways']))
    if m is not None and o.get('turning') is not None and m.get('turning') is not None and o['turning'] > max(o['fold'], m['turning']) + 0.5:
        lost.append(('Next before the array turns round (%.0f px in the top row)' % m['turning'], o['turning']))
    if None in sizes:
        return None, lost
    if len(set(sizes)) != 1:
        out.append('%s: the character\'s size changed at marking: %s px before, %s px after' % (tag, sizes[0] or 22, sizes[-1] or 22))
        return None, lost
    return sizes[0], lost


def host_same(o, m):
    """Whether the play o kept everything the play m (the top row, as before this contract) gave: the fact picture, the
    crowd, the sum on as many lines."""
    return (o['pic']['fact'] == m['pic']['fact'] and o['pic']['n'] == m['pic']['n'] and abs(o['pic']['w'] - m['pic']['w']) < 0.01
            and abs(o['crowd']['w'] - m['crowd']['w']) < 0.01 and abs(o['crowdBefore']['w'] - m['crowdBefore']['w']) < 0.01
            and abs(o['sumH'] - m['sumH']) < 0.5)


def check_host(pw, base, html, look, size, aa, out, info):
    """SOME-THINGIES-HOST: every Stage 3 and Stage 4 item, Main and Pro, in one look at one size, normal or Aa (the speaker
    showing, the real fonts: fit_common.open_phone), right (the tallest LINES.right line here) and wrong, three times:
    as the page sizes the character, with it forced into the top row (as before this contract) and forced one pixel
    bigger (48 px where the page chose the top row)."""
    tag = 'host %s %dx%d %s' % (look, size[0], size[1], aa)
    br, page, errs = fc.open_phone(pw, base, html, SLUG, '!!window.ST && !!ST.ui', '#kids/Example' if look == 'kids' else '', size)
    n0 = len(out)
    try:
        if aa == 'Aa':
            page.evaluate("document.getElementById('a11yToggle').click()")
        if page.evaluate("document.body.classList.contains('accessible')") != (aa == 'Aa') or page.evaluate("document.body.classList.contains('look-kids')") != (look == 'kids'):
            out.append('%s: the page is not in the %s look, %s' % (tag, look, aa))
        page.evaluate('document.fonts.ready.then(() => 1)')
        items = [q for q in page.evaluate('ST.bank()') if q['stage'] in (3, 4)]
        page.evaluate('(id) => ST.ui.preview(id, 1)', [q['id'] for q in items if q['stage'] == 4][0])
        line = page.evaluate(TALLEST_JS)
        sizes, known, lost_main = Counter(), set(), []

        def play(batch):
            got = []
            for i in range(0, len(batch), 48):
                got += page.evaluate(HOST_JS, batch[i:i + 48])
            return got
        # Every item as question 1, right and wrong: as the page sizes it, and in the top row.
        plays = [[q['id'], 1, right, line, 0, force] for q in items for right in (True, False) for force in (None, 0)]
        got = play(plays)
        chosen = {}
        def hard():
            # Findings so far, less the known-list ones (every one of those is wanted, to copy into HOST_KNOWN).
            return sum(1 for f in out[n0:] if 'put it on HOST_KNOWN' not in f)
        for k, q in enumerate(items):
            if hard() > 12:
                break
            res = []
            for j, right in enumerate((True, False)):
                o, m = got[4 * k + 2 * j], got[4 * k + 2 * j + 1]
                t2 = '%s %s (%s)' % (tag, q['id'], 'right' if right else 'wrong')
                sz, lost = host_play(t2, q, o, out, m)
                _, lost_m = host_play(t2 + ' in the top row', q, m, [])
                if sz is None:
                    continue
                res.append(sz)
                if lost and lost_m:
                    # Main loses the fold here too: it must be on the known list, and the character stays in the top row.
                    key = (tag, q['id'])
                    known.add(key)
                    lost_main.append('%s: %s' % (t2, '; '.join('%s ends at %.0f px, the fold at %.0f px' % (w, e, o['fold']) for w, e in lost_m)))
                    if key not in HOST_KNOWN:
                        out.append('%s: main loses the fold here too (%s): put it on HOST_KNOWN with these figures, or fix it'
                                   % (t2, '; '.join('%s ends at %.0f px, the fold at %.0f px' % (w, e, o['fold']) for w, e in lost_m)))
                    if sz:
                        out.append('%s: main loses the fold here, but the character is at %d px, not in the top row' % (t2, sz))
                elif lost:
                    out.append('%s: with the character at %s px, %s ends at %.0f px, below the fold at %.0f px (it fits there in the top row)'
                               % (t2, sz or 22, lost[0][0], lost[0][1], o['fold']))
                elif not host_same(o, m):
                    out.append('%s: the character at %d px changed what the top row leaves (picture %s at %.1f px, crowd %.1f px, sum %.0f px high; in the top row %s at %.1f px, %.1f px, %.0f px)'
                               % (t2, sz, o['pic']['fact'], o['pic']['w'], o['crowd']['w'], o['sumH'], m['pic']['fact'], m['pic']['w'], m['crowd']['w'], m['sumH']))
            if len(set(res)) > 1:
                out.append('%s %s: the character is %s px when answered right and %s px when answered wrong: the size must not depend on the answer'
                           % (tag, q['id'], res[0] or 22, res[1] or 22))
            elif res:
                chosen[q['id']] = res[0]
                sizes[(q['stage'], res[0])] += 1
        # The largest that fits: one pixel more (48 px for the top row) must cost the fold, the picture, the crowd or
        # the sum's line, or not fit its room, on one of the item's screens.
        plays = [[q['id'], 1, right, line, 0, chosen[q['id']] + 1 if chosen[q['id']] else HOST_MIN]
                 for q in items if q['id'] in chosen and chosen[q['id']] < HOST_MAX for right in (True, False)]
        bigger = play(plays)
        ix = {(p[0], p[2]): b for p, b in zip(plays, bigger)}
        for q in items:
            if q['id'] not in chosen or chosen[q['id']] >= HOST_MAX or hard() > 12:
                continue
            ok, fb = True, HOST_MIN if not chosen[q['id']] else chosen[q['id']] + 1
            for j, right in enumerate((True, False)):
                b, m = ix[(q['id'], right)], got[4 * items.index(q) + 2 * j + 1]
                sink = []
                sz, lost = host_play('', q, b, sink, m)
                ok = ok and not sink and not lost and host_same(b, m)
            if ok:
                out.append('%s %s: the character is %s though %d px fits every screen of it' % (tag, q['id'], ('%d px' % chosen[q['id']]) if chosen[q['id']] else 'in the top row', fb))
        for key in HOST_KNOWN:
            if key[0] == tag and key not in known:
                out.append('%s %s: on HOST_KNOWN, but main\'s fold holds here now: take it off the list (stale)' % key)
        # Past question 10 (as question 12), sampled as SOME-THINGIES-FACTS samples: each mode's smallest and largest
        # item of each stage with 60 in the crowd, the largest also with 1 and with a crowd big enough to shrink: the
        # crowd the same size before and after marking as with the character in the top row, and the fold held.
        seen, plays = Counter(), []
        for md in ('main', 'pro'):
            for st in (3, 4):
                key = (lambda x: x['rows'] * x['cols']) if st == 3 else (lambda x: fact_plates(x)[0] * fact_plates(x)[1])
                mine = sorted((x for x in items if x['mode'] == md and x['stage'] == st), key=lambda x: (key(x), x['id']))
                for q, crowd, right in [(mine[0], 60, True), (mine[0], 60, False), (mine[-1], 60, True), (mine[-1], 60, False),
                                        (mine[-1], 1, True), (mine[-1], 1, False), (mine[-1], FACT_CROWD_BIG[size[0] > 600], False)]:
                    plays += [[q['id'], 12, right, line, crowd, None], [q['id'], 12, right, line, crowd, 0]]
        crowd_got = play(plays)
        for k in range(0, len(plays), 2):
            o, m = crowd_got[k], crowd_got[k + 1]
            q = [x for x in items if x['id'] == plays[k][0]][0]
            t2 = '%s %s as question 12, %d in the crowd (%s)' % (tag, q['id'], plays[k][4], 'right' if plays[k][2] else 'wrong')
            sz, lost = host_play(t2, q, o, out, m)
            _, lost_m = host_play(t2, q, m, [])
            if sz is None:
                continue
            seen['%s px' % sz if sz else 'top row'] += 1
            if lost and not lost_m:
                out.append('%s: with the character at %s px, %s ends at %.0f px, below the fold at %.0f px (it fits there in the top row)'
                           % (t2, sz or 22, lost[0][0], lost[0][1], o['fold']))
            if abs(o['crowdBefore']['w'] - m['crowdBefore']['w']) > 0.01 or abs(o['crowd']['w'] - m['crowd']['w']) > 0.01:
                out.append('%s: the crowd is %.1f then %.1f px with the character at %s px, %.1f then %.1f px without it'
                           % (t2, o['crowdBefore']['w'], o['crowd']['w'], sz or 22, m['crowdBefore']['w'], m['crowd']['w']))
            if o['crowd']['w'] < 15.99:
                seen['crowd shrunk to fit'] += 1
        if len(out) == n0 and not seen['crowd shrunk to fit']:
            out.append('%s: no crowd was seen shrunk to fit: the character was never tried against a full screen' % tag)
        info.setdefault('host', []).append((tag, dict(sizes), dict(seen), lost_main))
        still(page, tag, out)
    except Exception as e:  # noqa: BLE001
        out.append('%s threw: %s' % (tag, str(e).splitlines()[0][:220]))
    out.extend('page error (%s): %s' % (tag, e) for e in errs if 'production host' not in e)
    br.close()


CONGA_JS = r"""() => { const line = document.getElementById('conga');
  if (!line) return null;
  return [...line.querySelectorAll('.cgroup')].map(g => { const r = g.getBoundingClientRect();
    return { top: Math.round(r.top), n: g.querySelectorAll('svg.th').length,
             ks: [...new Set([...g.querySelectorAll('svg.th')].map(t => +((t.getAttribute('class').match(/\bk(\d+)\b/) || [])[1])))] }; }); }"""
SARGE_JS = r"""() => { const vis = (e) => !!e && e.getBoundingClientRect().width > 0 && getComputedStyle(e).display !== 'none';
  return { mini: vis(document.querySelector('#sargeMini svg.sarge')), wide: vis(document.querySelector('#sargeWide svg.sarge')),
           host: document.getElementById('qcard').dataset.host }; }"""
START_JS = r"""() => { const f = document.querySelector('.site-footer'); const fold = innerHeight - (getComputedStyle(f).position === 'fixed' ? f.getBoundingClientRect().height : 0);
  const b = document.querySelector('#stageList .stage-btn'); return { bottom: b.getBoundingClientRect().bottom + scrollY, fold: fold,
  crowd: document.querySelectorAll('#crowdStart svg.th').length, sw: document.documentElement.scrollWidth > innerWidth }; }"""


def check_scenes(pw, base, html, out, info):
    """The start screen's crowd at every phone-fit size, the conga line and Sarge (SOME-THINGIES-PERSONALITY)."""
    items = bank_of(html)
    for look, frag in (('grown', ''), ('kids', '#kids/Example')):
        for size in FIT_SIZES + [PHONE]:
            tag = '%s %dx%d' % (look, size[0], size[1])
            br, page, errs = open_page(pw, base, html, size, frag)
            try:
                page.evaluate('window.scrollTo(0, 0)')
                st = page.evaluate(START_JS)
                if st['crowd'] < 12 or st['crowd'] > 16:
                    out.append('%s: the start screen\'s crowd has %d thingies (12-16)' % (tag, st['crowd']))
                if st['bottom'] > st['fold'] + 0.5 or st['sw']:
                    out.append('%s: the start screen\'s crowd pushes Start to %.0f px, below the fold at %.0f px' % (tag, st['bottom'], st['fold']))
                check_thingies(page, '#crowdStart', False, '%s start screen' % tag, out)
                still(page, '%s start screen' % tag, out)
                if size not in ((320, 568), PHONE, (1280, 720)):
                    continue
                phone = size[0] < 600
                # Stage 2, the conga line: every adding and groups-to-sum item; one group per line at 360 px.
                for q in items:
                    if q['type'] not in ('sum-to-groups', 'groups-to-sum'):
                        continue
                    i = q['id']
                    page.evaluate('([id, at]) => ST.ui.preview(id, at)', [i, 1])
                    cg = page.evaluate(CONGA_JS)
                    if q['type'] == 'groups-to-sum' and cg is not None:
                        out.append('%s %s: the conga line shows before marking (it would give the answer away)' % (tag, i))
                    if q['type'] == 'sum-to-groups':
                        page.evaluate("ST.ui.count(String(ST.ui.question().groups))")
                    page.evaluate('ST.ui.answer(false)')
                    fc.fit(page, '#feedback .maffs-next, #nextBtn', '%s %s (Next, the conga line)' % (tag, i), out, pic=PIC)
                    cg = page.evaluate(CONGA_JS)
                    off = page.evaluate("document.getElementById('pic').dataset.conga === 'off'")
                    if cg is None and not (off and size == (320, 568)):
                        out.append('%s %s: no conga line after marking' % (tag, i))
                        continue
                    if cg is None:
                        continue
                    if [g['n'] for g in cg] != [q['each']] * q['groups'] or [g['ks'] for g in cg] != [[(j % 10) + 1] for j in range(q['groups'])]:
                        out.append('%s %s: the conga line is %s, expected %d groups of %d, one colour each in order' % (tag, i, [(g['n'], g['ks']) for g in cg], q['groups'], q['each']))
                    if phone and size[0] <= 360 and len({g['top'] for g in cg}) != len(cg):
                        out.append('%s %s: the conga line puts %d groups on %d lines (one group per line on a phone)' % (tag, i, len(cg), len({g['top'] for g in cg})))
                    check_thingies(page, '#pic', q['mode'] == 'pro', '%s %s conga' % (tag, i), out)
                # Stage 3, the parade ground: Sarge beside the array where the card gives him a size (SOME-THINGIES-HOST),
                # else in the top row; Next after marking above the fold for every array, as question 1 (labels on) and
                # as question 8.
                for q in items:
                    if q['type'] != 'array':
                        continue
                    for at in (1, 8):
                        page.evaluate('([id, at]) => ST.ui.preview(id, at)', [q['id'], at])
                        sg = page.evaluate(SARGE_JS)
                        big = sg.pop('host') != 'mini'
                        if sg != {'mini': not big, 'wide': big}:
                            out.append('%s %s: Sarge %s, expected %s' % (tag, q['id'], sg, 'beside the array' if big else 'in the top row'))
                        page.evaluate('(r) => ST.ui.answer(r)', at == 1)
                        fc.fit(page, '#feedback .maffs-next, #nextBtn', '%s %s as question %d (Next, with Sarge)' % (tag, q['id'], at), out, pic=PIC)
                        if at == 1 and page.evaluate("document.getElementById('say').textContent") != page.evaluate('ST.lines()')[look]['sarge']:
                            out.append('%s %s: Sarge does not say his line on a right answer' % (tag, q['id']))
                    if len(out) > 60:
                        break
            except Exception as e:  # noqa: BLE001
                out.append('scenes %s threw: %s' % (tag, str(e).splitlines()[0][:200]))
            out.extend('page error (scenes %s): %s' % (tag, e) for e in errs if 'production host' not in e)
            br.close()
    info['scenes'] = True


TURN_WATCH_JS = r"""() => { window.__turn = null; const arr = document.getElementById('arr');
  new MutationObserver(() => {
    if (window.__turn || !arr.classList.contains('turning')) return;
    const t = document.getElementById('arrTop'), s = document.getElementById('arrSide');
    const shown = (e) => !!e && e.textContent.trim() !== '' && parseFloat(getComputedStyle(e).opacity) > 0.01;
    window.__turn = { top: shown(t) ? t.textContent : null, side: shown(s) ? s.textContent : null, mid: null };
    // Halfway through the turn (300 of 600 ms): each thingy's net rotation, the array's angle plus its own.
    const ang = (e) => { const m = getComputedStyle(e).transform; if (!m || m === 'none') return 0;
      const v = m.match(/matrix\(([^)]+)\)/); if (!v) return NaN; const p = v[1].split(',').map(Number);
      return Math.atan2(p[1], p[0]) * 180 / Math.PI; };
    setTimeout(() => { const ths = [...arr.querySelectorAll('svg.th')];
      const pick = [ths[0], ths[Math.floor(ths.length / 2)], ths[ths.length - 1]].filter(Boolean);
      window.__turn.mid = { arr: ang(arr), net: pick.map(th => ang(arr) + ang(th)) }; }, 300);
  }).observe(arr, { attributes: true, attributeFilter: ['class'] }); }"""


def check_turn(pw, base, html, out, info):
    """SOME-THINGIES-TURN-LABELS (Jon, 21 Nov 2026): with full motion, the scaffold's labels are gone (empty, or faded
    to nothing) the moment the array starts to turn, and the turned array never shows the old rows or columns; Next is
    there at once (the fade never delays it). With reduced motion, the turned array is drawn at once with no labels."""
    for size, motion in (((1280, 800), 'no-preference'), (PHONE, 'no-preference'), (PHONE, 'reduce')):
        tag = 'turn %dx%d %s' % (size[0], size[1], 'full motion' if motion != 'reduce' else 'reduced motion')
        br, page, errs = open_page(pw, base, html, size)
        try:
            page.emulate_media(reduced_motion=motion)
            for qid in ('m3-4r5c', 'p3-8r6c', 'm3-10r5c'):
                page.evaluate('([id, at]) => ST.ui.preview(id, at)', [qid, 1])
                q = page.evaluate('ST.ui.question()')
                page.evaluate("ST.ui.step(String(ST.ui.question().rows))")
                page.evaluate("ST.ui.step(String(ST.ui.question().cols))")
                a = page.evaluate(SCREEN_JS)['arr']
                if not a['top'] or not a['side']:
                    out.append('%s %s: the labels are not up before marking (%r, %r)' % (tag, qid, a['top'], a['side']))
                    continue
                page.evaluate(TURN_WATCH_JS)
                page.evaluate('ST.ui.answer(true)')
                if not page.evaluate("!!document.querySelector('#nextBtn')"):
                    out.append('%s %s: Next is not there at once after marking' % (tag, qid))
                page.wait_for_function("document.getElementById('pic').dataset.turned === '1'", timeout=5000)
                seen = page.evaluate('window.__turn')
                if motion != 'reduce':
                    if seen is None:
                        out.append('%s %s: the array never turned' % (tag, qid))
                    elif seen['top'] or seen['side']:
                        out.append('%s %s: labels still showing as the turn starts (%r, %r)' % (tag, qid, seen['top'], seen['side']))
                    if seen is not None:
                        mid = seen.get('mid')
                        if not mid or not (10 <= abs(mid['arr']) <= 80):
                            out.append('%s %s: no mid-turn sample (the array at %s degrees)' % (tag, qid, mid and round(mid['arr'], 1)))
                        elif any(not (abs(n) <= 3) for n in mid['net']):
                            out.append('%s %s: a thingy is not upright mid-turn (array %.0f degrees, thingies net %s)' % (tag, qid, mid['arr'], [round(n) for n in mid['net']]))
                a = page.evaluate(SCREEN_JS)['arr']
                old = {str(q['rows']), str(q['cols'])}
                stale = [x for x in (a['top'], a['side']) if x.strip() and any(n in x for n in old)]
                if stale:
                    out.append('%s %s: the turned array shows a label from before the turn: %s' % (tag, qid, stale))
                if a['rows'] != q['cols'] or a['cols'] != q['rows']:
                    out.append('%s %s: after the turn the array is %d rows of %d' % (tag, qid, a['rows'], a['cols']))
        finally:
            br.close()
        out.extend('page error (%s): %s' % (tag, e) for e in errs if 'production host' not in e)
    info['turn'] = True


def check_largest(page, look, out):
    for i in LARGEST:
        for at in (1, 8):
            page.evaluate('([id, at]) => ST.ui.preview(id, at)', [i, at])
            q = page.evaluate('ST.ui.question()')
            if not q or q['id'] != i:
                out.append('largest: %s is not in the bank' % i)
                break
            # Stage 3 as question 1: both steps answered, so both labels are on and the total's options are showing.
            if q['type'] == 'array' and at == 1:
                page.evaluate("ST.ui.step(String(ST.ui.question().rows))")
                page.evaluate("ST.ui.step(String(ST.ui.question().cols))")
            fc.fit(page, '#opts1 .opt, #opts .opt', '%s %s as question %d at %dx%d (largest)' % (look, i, at, PHONE[0], PHONE[1]), out, pic=PIC)
            if q['type'] == 'array':
                a = page.evaluate(SCREEN_JS)['arr']
                if a['size'] < 18:
                    out.append('%s %s at %dx%d: the thingies are %.0f px (at least 18 to read)' % (look, i, PHONE[0], PHONE[1], a['size']))
            if q['type'] != 'array':
                break


# ---------------------------------------------------------------- read aloud, against a mocked speechSynthesis
SPEECH_MOCK = """(() => { const cfg = %s; window.__spoken = [];
  const voices = cfg.slice(), listeners = [];
  const synth = { getVoices() { return voices.slice(); },
    speak(u) { window.__spoken.push({ text: u.text, local: !!(u.voice && u.voice.localService === true) }); },
    cancel() {}, addEventListener(n, f) { if (n === 'voiceschanged') listeners.push(f); } };
  Object.defineProperty(window, 'speechSynthesis', { value: synth, configurable: true });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; };
})();"""
REMOTE = {'name': 'Cloud UK', 'lang': 'en-GB', 'localService': False}
LOCAL = {'name': 'Device US', 'lang': 'en-US', 'localService': True}


def check_speech(pw, base, html, out, info):
    for cfg, shown in (([], False), ([REMOTE], False), ([REMOTE, LOCAL], True)):
        br, page, errs = open_page(pw, base, html, PHONE, '#kids/Example', init=SPEECH_MOCK % json.dumps(cfg))
        try:
            page.evaluate("ST.ui.preview('m1-3x5')")
            hidden = page.evaluate("document.getElementById('speakBtn').hidden")
            if hidden == shown:
                out.append('read aloud with voices %s: the speaker is %s' % ([v['name'] for v in cfg], 'hidden' if hidden else 'shown'))
            if page.evaluate('window.__spoken.length'):
                out.append('read aloud: spoke %s before any tap' % page.evaluate('window.__spoken'))
            if not shown:
                continue
            for qid, at, want in (('m1-3x5', 1, '3 groups of 5. How many thingies?'), ('m3-4r5c', 8, '4 rows of 5. How many thingies?'),
                                  ('m3-4r5c', 1, 'How many rows?'), ('m3-4r5c', 5, 'How many in each row?'),
                                  ('p4-3x4', 1, '3 times 4 equals what?'), ('p4-q7x8', 1, 'What times 8 equals 56?'),
                                  ('m2a-3x5', 1, '5 plus 5 plus 5. How many 5s?')):
                page.evaluate('([id, at]) => ST.ui.preview(id, at)', [qid, at])
                page.evaluate("window.__spoken = []; document.getElementById('speakBtn').click()")
                sp = page.evaluate('window.__spoken')
                if [x['text'] for x in sp] != [want]:
                    out.append('read aloud %s: spoke %s, expected %r' % (qid, [x['text'] for x in sp], want))
                if any(not x['local'] for x in sp):
                    out.append('read aloud: a voice that is not local was passed to speak()')
                if any('Example' in x['text'] or 'Welcome' in x['text'] for x in sp):
                    out.append('read aloud: the greeting was spoken')
            info['speech'] = True
        finally:
            br.close()


def check(html, out, units, shard=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info = {}
    if 'bank' in units:
        with unit('bank'):
            try:
                check_bank(html, out, info)
                check_source(html, out)
            except Exception as e:  # noqa: BLE001
                out.append('the bank checks threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u != 'bank']
    if not browser:
        return info
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    if uid == 'read aloud':
                        try:
                            check_speech(pw, base, html, out, info)
                        except Exception as e:  # noqa: BLE001
                            out.append('read aloud threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    if uid == TURN:
                        try:
                            check_turn(pw, base, html, out, info)
                        except Exception as e:  # noqa: BLE001
                            out.append('turn threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    if uid == SCENES:
                        try:
                            check_scenes(pw, base, html, out, info)
                        except Exception as e:  # noqa: BLE001
                            out.append('scenes threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    if uid.startswith('crowd '):
                        _, look, wh = uid.split(' ')
                        sz = tuple(int(x) for x in wh.split('x'))
                        check_crowd(pw, base, html, look, sz, dict(CROWD_SIZES)[sz], out, info)
                        continue
                    if uid.startswith('host '):
                        _, look, wh, aa = uid.split(' ')
                        check_host(pw, base, html, look, tuple(int(x) for x in wh.split('x')), aa, out, info)
                        continue
                    if uid.startswith('facts '):
                        _, look, wh, aa = uid.split(' ')
                        check_facts(pw, base, html, look, tuple(int(x) for x in wh.split('x')), aa, out, info)
                        continue
                    if uid.startswith('fit '):
                        _, look, m = uid.split(' ')
                        try:
                            check_fit(pw, base, html, look, m, out, info)
                        except Exception as e:  # noqa: BLE001
                            out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                        continue
                    if uid == 'greeting':
                        try:
                            check_greeting(pw, base, html, out)
                            info['greeting'] = len(GREETINGS)
                        except Exception as e:  # noqa: BLE001
                            out.append('greeting threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    look = 'kids' if ' kids' in uid else 'grown'
                    frag = '#kids/Example' if look == 'kids' else ''
                    size = PHONE if uid.startswith('play') else (1280, 800)
                    br, page, errs = open_page(pw, base, html, size, frag)
                    try:
                        if page.evaluate("document.body.classList.contains('look-kids')") != (look == 'kids'):
                            out.append('%s: the page is not in the %s look' % (uid, look))
                        if uid.startswith('marking'):
                            check_marking(page, html, look, out, info)
                        elif uid.startswith('winner'):
                            check_winner(page, look, out)
                            info['winner'] = True
                        else:
                            check_largest(page, look, out)
                            for m in MODES:
                                play(page, look, m, out)
                            info['played'] = info.get('played', 0) + len(MODES)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


# Each plant: (what, edit(html) -> html, the unit it needs, the pattern its finding must match). The contract's five,
# and marking by the option's text.
def edit(old, new):
    return lambda html, what: pc.apply_plant(html, old, new, name=what)


PLANTS = [
    ('a wrong answer',
     edit('{"id":"m1-2x2","mode":"main","stage":1,"type":"groups","groups":2,"each":2,"answer":4,"decoys":[6,2,5],',
          '{"id":"m1-2x2","mode":"main","stage":1,"type":"groups","groups":2,"each":2,"answer":3,"decoys":[6,2,5],'),
     'bank', r'm1-2x2: answer 3, recomputed 4'),
    ('a decoy equal to its answer',
     edit('{"id":"m3-2r5c","mode":"main","stage":3,"type":"array","rows":2,"cols":5,"answer":10,"decoys":[7,15,5]}',
          '{"id":"m3-2r5c","mode":"main","stage":3,"type":"array","rows":2,"cols":5,"answer":10,"decoys":[7,15,10]}'),
     'bank', r'm3-2r5c: a decoy equals the answer'),
    ('a decoy sum with the right total',
     edit('"answer_sum":[5,5],"decoy_sums":[[5,5,5],[7,7],[2,5]]}',
          '"answer_sum":[5,5],"decoy_sums":[[5,5,5],[7,7],[4,6]]}'),
     'bank', r"m2b-2x5: decoy sum 4\+6 has the answer's total 10"),
    ('a missing item',
     edit('    {"id":"p4-q2x3","mode":"pro","stage":4,"type":"missing","b":3,"product":6,"answer":2,"decoys":[3,1,4]},\n', ''),
     'bank', r'counts .*expected'),
    ('the fragment sent in an mfg() call',
     edit("ev('game_started', { game_slug: SLUG, level: level, mode: evMode(mode) });",
          "ev('game_started', { game_slug: SLUG, level: level, mode: evMode(mode), cls: CLASS_NAME || '' });"),
     'play kids %dx%d' % PHONE, r"an mfg\(\) payload contains 'Example'"),
    ('an option marked by its text',
     edit('var b = e.currentTarget, val = b.dataset.val, key = keyOf(Q);', 'var b = e.currentTarget, val = b.textContent, key = keyOf(Q);'),
     'marking grown', r'option \S+ marked wrong, expected done'),
    # SOME-THINGIES-TWEAKS' four.
    ('a run that ends at the first wrong before question 10',
     edit('runOver = !right && qi > PER;', 'runOver = !right;'),
     WINNER, r'a wrong answer at question 3 ended the run'),
    ('an End button visible at question 5',
     edit("$('endBtn').hidden = qi <= PER;", "$('endBtn').hidden = qi <= 4;"),
     WINNER, r'the End button is shown at question 5'),
    ('a step answer that changes the score',
     edit("    var kind = state;\n    steps++;\n", "    var kind = state;\n    steps++;\n    score++;\n"),
     WINNER, r'a step changed the score'),
    ('a dot drawn instead of a thingy',
     edit("for (var j = 1; j <= c; j++) h += thingy(turned ? i : j, j === 6 ? ' c6' : '');",
          "for (var j = 1; j <= c; j++) h += j === 1 ? '<i class=\"k1\"></i>' : thingy(turned ? i : j, j === 6 ? ' c6' : '');"),
     'marking grown', r'Stage 3 draws \d+ cells, \d+ of them thingies'),
    # SOME-THINGIES-PERSONALITY's three.
    ('a thingy with the wrong accessory for its colour',
     edit("    var a = ACCESSORY[k];", "    var a = ACCESSORY[k === 6 ? 2 : k];"),
     SCENES, r'a thingy of colour 6 wears hair'),
    ('an animation running under reduced motion',
     edit("@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}", ""),
     SCENES, r'animations running under reduced motion'),
    ('the crowd changing the score',
     edit("if (right && qi > PER) { crowdN++; drawCrowd(); }", "if (right && qi > PER) { crowdN++; score++; drawCrowd(); }"),
     WINNER, r'the score is \d+ \(the crowd must never change it\)'),
    # CROWD-FILL's three.
    ('the crowd capped at 48 again',
     edit("for (var i = 0; i < crowdN; i++) h += thingy((i % 10) + 1);", "for (var i = 0; i < Math.min(crowdN, 48); i++) h += thingy((i % 10) + 1);"),
     'crowd grown 375x667', r'after 59 right: the crowd draws 48 thingies, expected 49'),
    ('a thingy drawn below 6 px',
     edit("var CROWD_FULL = 16, CROWD_FLOOR = 6, crowdN = 0;", "var CROWD_FULL = 16, CROWD_FLOOR = 4, crowdN = 0;"),
     'crowd kids 375x667', r'thingies are drawn at [45]\.\d px, below the 6 px floor'),
    ('the cheer stuck on its first line',
     edit("if (crowdN >= t) line = L.cheers[t];", "if (crowdN >= t && t < 10) line = L.cheers[t];"),
     'crowd grown 375x667', r"with 10 in the crowd the cheer is 'A crowd is gathering\.', expected 'Word is spreading\.'"),
    # SOME-THINGIES-TURN-LABELS.
    ('labels left visible during the turn',
     lambda html, what: pc.apply_plant(pc.apply_plant(html,
         "    arr.parentNode.classList.add('labels-off');\n", "", name=what),
         "      $('arrTop').textContent = ''; $('arrSide').textContent = '';\n", "", name=what),
     TURN, r'labels still showing as the turn starts'),
    ('a thingy not counter-rotated',
     edit(".arr.turning .th{transform:rotate(-90deg)}", ""),
     TURN, r'a thingy is not upright mid-turn'),
    # SOME-THINGIES-FACTS: the contract's four, and the picture taking the crowd's room.
    ('the fact pictured before it is marked',
     edit("else if (t === 'fact') { setSum(", "else if (t === 'fact') { plates(Q.a, Q.b); setSum("),
     'facts grown 375x667 normal', r'a picture before marking \(\d+ plates, \d+ thingies\)'),
    ('b plates of a in place of a plates of b',
     edit("q.type === 'fact' ? [q.a, q.b] :", "q.type === 'fact' ? [q.b, q.a] :"),
     'facts kids 375x667 normal', r'after marking the picture draws \d+ plates of \[\d+\] \(\d+ thingies\), expected \d+ plates of \d+'),
    ('the picture never shrunk or dropped',
     edit("p.style.setProperty('--ps', sz + 'px'); if (!over()) return; }", "p.style.setProperty('--ps', sz + 'px'); return; }"),
     'facts grown 320x568 normal', r'Next ends at \d+ px, below the fold at \d+ px \(picture shown at 18 px\)'),
    ('the thingy beside the question left without its reaction',
     edit("['pic', 'sargeMini', 'host'].forEach(function (id) { $(id).classList.add(right ? 'react-right' : 'react-wrong'); });",
          "['pic'].forEach(function (id) { $(id).classList.add(right ? 'react-right' : 'react-wrong'); });"),
     'facts kids 1280x720 Aa', r'the thingy beside the question does not react after a right answer'),
    ('the picture drawn without looking at the crowd',
     edit("    var crowd = !!$('crowd').querySelector('.th');\n    function over() {", "    var crowd = false;\n    function over() {"),
     'facts grown 375x667 Aa', r'the picture does not fit the room the crowd of \d+ leaves'),
    # SOME-THINGIES-HOST's three.
    ('the character fixed at 96 px whatever the room',
     edit("    setHost(best);\n  }\n  function roomChanged()", "    setHost(HOST_MAX);\n  }\n  function roomChanged()"),
     'host grown 320x568 normal', r'with the character at 96 px, .* below the fold at \d+ px \(it fits there in the top row\)|the array and Sarge are wider than their room'),
    ('the character\'s size changing at marking',
     edit("    fitCrowd();\n    factPic();\n    if (window.MaffsScroll)",
          "    fitCrowd();\n    factPic();\n    if ($('qcard').classList.contains('host-big')) setHost(HOST_MIN);\n    if (window.MaffsScroll)"),
     'host grown 1920x955 normal', r"the character's size changed at marking: 96 px before, 48 px after"),
    ('Sarge left at 30 px while the thingy in glasses grows',
     edit(".host .th,.sarge-wide .th{width:var(--host);height:var(--host)}", ".host .th{width:var(--host);height:var(--host)}.sarge-wide .th{width:30px;height:30px}"),
     'host kids 1366x768 normal', r'Sarge is drawn at 30 px, not the \d+ px the card gives'),
    # PRIMARY-FIT-SWEEP: the fold, on one item and one feedback variant only (a sample would miss it most runs).
    ('Next below the fold after one right-answer line only (right.4, m1-3x2)',
     edit("    if (Q.type === 'array') turnArray();\n",
          "    if (Q.id === 'm1-3x2' && sayKey === 'right.4') fb.querySelector('.fb-next').style.paddingTop = '300px';\n    if (Q.type === 'array') turnArray();\n"),
     'fit grown main-1', r'^fit grown 360x640 m1-3x2 \[@1 right 4\] \(Next\): .* below the fold'),
    ('Next below the fold after one decoy of one item at question 11 only (p4-1x3, 4)',
     edit("    if (Q.type === 'array') turnArray();\n",
          "    if (Q.id === 'p4-1x3' && qi === 11 && btn.dataset.val === '4') fb.querySelector('.fb-next').style.paddingTop = '300px';\n    if (Q.type === 'array') turnArray();\n"),
     'fit kids pro-4', r'^fit kids 360x640 p4-1x3 \[@11 wrong 4\] \(Next\): .* below the fold'),
]


def selftest(html, plants=None, shard=None):
    ok = True
    for what, plant, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = plant(html, what)
            except pc.StalePlant as e:
                print('  self-test %-48s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id])
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-48s %s' % (what, ('caught: ' + hit[0][:90]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = ['bank', 'marking grown', 'marking kids', 'greeting', 'read aloud', 'play grown %dx%d' % PHONE, 'play kids %dx%d' % PHONE, WINNER, SCENES, TURN]
    units += CROWD_UNITS
    units += FACT_UNITS
    units += HOST_UNITS
    units += ['fit %s %s' % (look, m) for look in ('grown', 'kids') for m in MODES]
    if args.selftest:
        units = []
    mine = shard.pick(units + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    run = [u for u in units if u in mine]
    info = check(html, out, run, shard) if run else {}
    if 'bank' in info:
        print('%s: %d items, SHA-256 as the contract states (the page and the generator), every answer and decoy recomputed' % (SLUG, info['bank']))
    if 'marked' in info:
        print('%s: %d item plays marked (every option by dataset.val, right and wrong, one line then the working)' % (SLUG, info['marked']))
    if 'greeting' in info:
        print('%s: %d fragments read for the look and the greeting' % (SLUG, info['greeting']))
    if 'speech' in info:
        print('%s: read aloud against a mocked speechSynthesis: hidden without a local voice, local voices only, nothing before a tap, words from the item' % SLUG)
    if 'scenes' in info:
        print('%s: the start screen crowd (Start above the fold at every phone-fit size), the conga line (one group per line on a phone, Next above the fold) and Sarge (Next above the fold), every thingy in its own colour\'s accessory, nothing moving under reduced motion' % SLUG)
    if 'winner' in info:
        print('%s: winner stays on (at least 10, then to the first wrong or End; no End before 11; the supply never repeats at once) and the Stage 3 scaffold (3, 2, then 1 steps; steps never score)' % SLUG)
    if 'crowd' in info:
        print('%s: the crowd at %d size-and-look pairs: every thingy drawn through 135 right answers and to the floor, 16 px until the screen is full, then the largest size that fits, never under 6 px, nothing above it moved; the cheer by its size; the count on the results screen; the crowd of 120 drawn and sized in %s ms'
              % (SLUG, info['crowd'], ', '.join('%.1f' % m for m in info.get('crowd ms', []))))
    for tag, both, drop, n, smallest, which in info.get('facts', []):
        print('%s: %s: of %d Stage 4 items, %d show the fact as plates after a right and after a wrong answer, %d drop it%s; the smallest picture %.0f px; Next above the fold on every one; the thingy in glasses beside each, reacting'
              % (SLUG, tag, n, both, drop, (' (%s)' % which) if which else '', smallest))
    for tag, sizes, seen, lost in info.get('host', []):
        print('%s: %s: the character beside the question, by stage and size (0 = the top row): %s; past question 10: %s%s'
              % (SLUG, tag, ', '.join('Stage %d %s %d' % (k[0], ('%d px' % k[1]) if k[1] else 'top row', v) for k, v in sorted(sizes.items())),
                 ', '.join('%s %d' % kv for kv in sorted(seen.items())), ('; main loses the fold: ' + ' | '.join(lost)) if lost else ''))
    for tag, seen in info.get('facts crowd', []):
        print('%s: %s, past question 10: %s' % (SLUG, tag, ', '.join('%s %d' % kv for kv in sorted(seen.items()))))
    if 'fit' in info:
        print('%s: every item above the fold at %dx%d, speaker showing: %d item views, %d feedback variants, %d controls measured (the looks and stages in this shard)'
              % (SLUG, PHONE[0], PHONE[1], info['fit']['items'], info['fit']['variants'], info['fit']['measures']))
    if 'played' in info:
        print('%s: %d runs played at %dx%d (every mode and stage, the looks in this shard), the largest pictures and sum fitting' % (SLUG, info['played'], PHONE[0], PHONE[1]))
    ok = selftest(html, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
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
