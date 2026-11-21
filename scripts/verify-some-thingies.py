#!/usr/bin/env python3
# ci-shards: Some Thingies (the thingies' accessories by colour, a medal in pro, nothing moving under reduced motion; the start screen's crowd, the conga line and Sarge never pushing Start or Next below the fold; the winner crowd growing, capped and never scoring; Stage 3 drawn as thingies coloured by column with gaps after the 5th, fitting 360 px; the scaffold fading 3, 2, 1 steps, never scoring; winner stays on: at least 10, then to the first wrong or End; the bank's SHA-256 and counts against the contract's and the generator's; all 369 items recomputed: groups x each, the sum's terms, rows x cols, a x b, product / b; every decoy distinct and never the answer, no decoy sum with the answer's total, no groups decoy equal to the groups; the fragment never sent or stored; in both looks every item on screen with its picture counted, every option marked by dataset.val alone, right and wrong, one LINES string then the worked maths; the array turned round after marking; the greeting for each fragment; read aloud on local voices only against a mocked speechSynthesis; every mode and stage played in both looks at 360x640, the largest picture, array and sum fitting 360 px; one board submission on stage-N or pro-stage-N, no payload naming the look; fault-injection self-test) | | 1
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
  Greeting  "#kids/Maple" and "#kids/Maple%20Class" -> "Welcome, Maple Class!"; "#KIDS" and "#kids" -> the kid look and
            its welcome; "#kids/<script>" -> the kid look, no class greeting, nothing injected; no hash or "#kidsx" ->
            the grown-up look.
  Read aloud against a mocked speechSynthesis: no speaker without a local voice; only a local voice passed to speak();
            nothing spoken before a tap; the question read in words from the item; never the greeting.
  Play      every mode and stage in each look at 360 x 640 (the kid look from #kids/Maple): 10 different items of that
            mode and stage, right and wrong; options and Next above the fold, no sideways scroll; one game_completed with
            the score, one board submission [slug, 'stage-N' or 'pro-stage-N', score, 10]; question_answered per item with
            its id; only game_started, question_answered and game_completed; no mfg() payload, localStorage or
            sessionStorage value containing "kids", "Maple" or "#". The largest picture (50 thingies), the largest array
            (10 x 5 and 5 x 10) and the longest sum (6 terms) on screen at 360 x 640 with every option above the fold and
            no sideways scroll.

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
            above the fold; Sarge in the top row on a phone and beside the array on a wide screen, Next above the fold for
            every array, his line on a right answer.
  Crowd     none in questions 1-10; from 11 the cheer and one more thingy per right answer, in colour order, 48 shown and
            "+n" beyond; the score always the game's; the run-ending wrong answer makes it faint, with the faint line.

Work units: "bank" (no browser), "scenes", "marking grown", "marking kids", "greeting", "read aloud", "play grown 360x640",
"play kids 360x640", "winner 360x640", and "plant: <what>" (one per planted fault).

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
        for k2, s in list(lines['kids']['wrong'].items()) + [('stages.' + a, b) for a, b in lines['kids']['stages'].items()]:
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
    ('#kids/Maple', 'kids', 'Welcome, Maple Class!'),
    ('#kids/Maple%20Class', 'kids', 'Welcome, Maple Class!'),
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


FIT_JS = r"""(sel) => {
  const f = document.querySelector('.site-footer');
  const fixed = f && getComputedStyle(f).position === 'fixed';
  const fold = window.innerHeight - (fixed ? f.getBoundingClientRect().height : 0);
  const els = [...document.querySelectorAll(sel)].filter(e => e.getBoundingClientRect().height > 0);
  const bottom = els.length ? Math.max(...els.map(e => e.getBoundingClientRect().bottom + window.scrollY)) : null;
  const pic = document.getElementById('pic').getBoundingClientRect(), card = document.getElementById('qcard').getBoundingClientRect();
  return { n: els.length, bottom: bottom, fold: fold, sw: document.documentElement.scrollWidth, vw: window.innerWidth,
           picOut: pic.width > 0 && (pic.right > card.right + 0.5 || pic.left < card.left - 0.5) };
}"""


def fit(page, sel, what, out):
    page.evaluate('window.scrollTo(0, 0)')
    f = page.evaluate(FIT_JS, sel)
    if not f['n']:
        out.append('%s: nothing on screen for %s' % (what, sel))
    elif f['bottom'] > f['fold'] + 0.5:
        out.append('%s: %s ends at %.0f px, below the fold at %.0f px' % (what, sel, f['bottom'], f['fold']))
    if f['sw'] > f['vw']:
        out.append('%s: the page scrolls sideways (%d > %d)' % (what, f['sw'], f['vw']))
    if f['picOut']:
        out.append('%s: the picture is wider than the card' % what)


def bad_in_storage(page):
    dump = page.evaluate("""() => { const o = {};
      for (const s of [localStorage, sessionStorage]) for (let i = 0; i < s.length; i++) o[s.key(i)] = s.getItem(s.key(i));
      return JSON.stringify(o); }""")
    return [b for b in ('kids', 'Maple', '#') if b in dump]


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
            if k < 2:
                fit(page, '#opts .opt' if s == 'ask' else '#opts1 .opt', '%s %s (the options)' % (tag, q['id']), out)
            ok = k % 3 != 1
            page.evaluate('(r) => ST.ui.answer(r)', ok)
            if k < 2:
                fit(page, '#feedback .maffs-next, #nextBtn', '%s %s (Next)' % (tag, q['id']), out)
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
    for bad in ('kids', 'Maple', '#'):
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
    # answer after question 10, the next colour in order; 48 shown at most, "+n" beyond; the score is the game's, never
    # the crowd's; the run-ending wrong answer makes the crowd faint, with the faint line.
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
        shown = min(want, 48)
        if c['n'] != shown or (want > 48) != (c['more'] is not None) or (want > 48 and c['more'] != '+%d' % (want - 48)):
            out.append('%s: after %d right the crowd shows %d thingies and %r, expected %d%s' % (tag, k, c['n'], c['more'], shown, ' and +%d' % (want - 48) if want > 48 else ''))
            break
        if c['ks'] != [(j % 10) + 1 for j in range(shown)]:
            out.append('%s: after %d right the crowd\'s colours are %s, not the fixed order' % (tag, k, c['ks'][:12]))
            break
        if k > 10 and c['line'] != Lw['cheer']:
            out.append('%s: at question %d the crowd line is %r, expected LINES.%s.cheer' % (tag, k, c['line'], look))
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
    if not c['faint'] or c['line'] != Lw['faint'] or c['n'] != 48:
        out.append('%s: the run-ending wrong: crowd faint %s, line %r, %d shown; expected fainted, LINES.%s.faint, 48' % (tag, c['faint'], c['line'], c['n'], look))
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


CONGA_JS = r"""() => { const line = document.getElementById('conga');
  if (!line) return null;
  return [...line.querySelectorAll('.cgroup')].map(g => { const r = g.getBoundingClientRect();
    return { top: Math.round(r.top), n: g.querySelectorAll('svg.th').length,
             ks: [...new Set([...g.querySelectorAll('svg.th')].map(t => +((t.getAttribute('class').match(/\bk(\d+)\b/) || [])[1])))] }; }); }"""
SARGE_JS = r"""() => { const vis = (e) => !!e && e.getBoundingClientRect().width > 0 && getComputedStyle(e).display !== 'none';
  return { mini: vis(document.querySelector('#sargeMini svg.sarge')), wide: vis(document.querySelector('#sargeWide svg.sarge')) }; }"""
START_JS = r"""() => { const f = document.querySelector('.site-footer'); const fold = innerHeight - (getComputedStyle(f).position === 'fixed' ? f.getBoundingClientRect().height : 0);
  const b = document.querySelector('#stageList .stage-btn'); return { bottom: b.getBoundingClientRect().bottom + scrollY, fold: fold,
  crowd: document.querySelectorAll('#crowdStart svg.th').length, sw: document.documentElement.scrollWidth > innerWidth }; }"""


def check_scenes(pw, base, html, out, info):
    """The start screen's crowd at every phone-fit size, the conga line and Sarge (SOME-THINGIES-PERSONALITY)."""
    items = bank_of(html)
    for look, frag in (('grown', ''), ('kids', '#kids/Maple')):
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
                    fit(page, '#feedback .maffs-next, #nextBtn', '%s %s (Next, the conga line)' % (tag, i), out)
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
                # Stage 3, the parade ground: Sarge beside the array on a wide screen, in the top row on a phone; Next
                # after marking above the fold for every array, as question 1 (labels on) and as question 8.
                for q in items:
                    if q['type'] != 'array':
                        continue
                    for at in (1, 8):
                        page.evaluate('([id, at]) => ST.ui.preview(id, at)', [q['id'], at])
                        sg = page.evaluate(SARGE_JS)
                        if sg != {'mini': phone, 'wide': not phone}:
                            out.append('%s %s: Sarge %s, expected %s' % (tag, q['id'], sg, 'in the top row' if phone else 'beside the array'))
                        page.evaluate('(r) => ST.ui.answer(r)', at == 1)
                        fit(page, '#feedback .maffs-next, #nextBtn', '%s %s as question %d (Next, with Sarge)' % (tag, q['id'], at), out)
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
            fit(page, '#opts1 .opt, #opts .opt', '%s %s as question %d at %dx%d (largest)' % (look, i, at, PHONE[0], PHONE[1]), out)
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
        br, page, errs = open_page(pw, base, html, PHONE, '#kids/Maple', init=SPEECH_MOCK % json.dumps(cfg))
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
                if any('Maple' in x['text'] or 'Welcome' in x['text'] for x in sp):
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
                    if uid == 'greeting':
                        try:
                            check_greeting(pw, base, html, out)
                            info['greeting'] = len(GREETINGS)
                        except Exception as e:  # noqa: BLE001
                            out.append('greeting threw: %s' % str(e).splitlines()[0][:220])
                        continue
                    look = 'kids' if ' kids' in uid else 'grown'
                    frag = '#kids/Maple' if look == 'kids' else ''
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
     'play kids %dx%d' % PHONE, r"an mfg\(\) payload contains 'Maple'"),
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
    # SOME-THINGIES-TURN-LABELS.
    ('labels left visible during the turn',
     lambda html, what: pc.apply_plant(pc.apply_plant(html,
         "    arr.parentNode.classList.add('labels-off');\n", "", name=what),
         "      $('arrTop').textContent = ''; $('arrSide').textContent = '';\n", "", name=what),
     TURN, r'labels still showing as the turn starts'),
    ('a thingy not counter-rotated',
     edit(".arr.turning .th{transform:rotate(-90deg)}", ""),
     TURN, r'a thingy is not upright mid-turn'),
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
