#!/usr/bin/env python3
# ci-shards: Some Thingies (the bank's SHA-256 and counts against the contract's and the generator's; all 369 items recomputed: groups x each, the sum's terms, rows x cols, a x b, product / b; every decoy distinct and never the answer, no decoy sum with the answer's total, no groups decoy equal to the groups; the fragment never sent or stored; in both looks every item on screen with its picture counted, every option marked by dataset.val alone, right and wrong, one LINES string then the worked maths; the array turned round after marking; the greeting for each fragment; read aloud on local voices only against a mocked speechSynthesis; every mode and stage played in both looks at 360x640, the largest picture, array and sum fitting 360 px; one board submission on stage-N or pro-stage-N, no payload naming the look; fault-injection self-test) | | 1
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

Work units: "bank" (no browser), "marking grown", "marking kids", "greeting", "read aloud", "play grown 360x640",
"play kids 360x640", and "plant: <what>" (one per planted fault).

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
  const dots = [...$('pic').querySelectorAll('.arr i')];
  const tops = new Set(dots.map(d => Math.round(d.getBoundingClientRect().top)));
  const lefts = new Set(dots.map(d => Math.round(d.getBoundingClientRect().left)));
  const ann = (el) => [...el.querySelectorAll('annotation')].map(a => a.textContent).join(' ');
  return { state: ST.ui.state(), plates: plates, dots: dots.length, rows: tops.size, cols: lefts.size,
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
        for k2, s in lines['kids']['wrong'].items():
            if words(s) > 6:
                out.append('LINES.kids.wrong.%s has %d words' % (k2, words(s)))
    every = set(all_lines(L))
    items = bank_of(html)
    marked = 0
    for n, q in enumerate(items):
        i, t = q['id'], q['type']
        for right in (True, False):
            page.evaluate('(id) => ST.ui.preview(id)', i)
            s = page.evaluate(SCREEN_JS)
            if right:
                # The picture, counted from the DOM.
                if t == 'groups' and s['plates'] != [q['each']] * q['groups']:
                    out.append('%s: the picture shows plates of %s, expected %d plates of %d' % (i, s['plates'], q['groups'], q['each']))
                if t == 'array' and (s['dots'] != q['rows'] * q['cols'] or s['rows'] != q['rows'] or s['cols'] != q['cols']):
                    out.append('%s: the array shows %d dots in %d rows and %d columns, expected %d x %d' % (i, s['dots'], s['rows'], s['cols'], q['rows'], q['cols']))
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
            if right and s['say'] not in L['right']:
                out.append('%s: the right line %r is not one of LINES.%s.right' % (i, s['say'], look))
            if not right and s['say'] != L['wrong'][WRONG_KEY[t]]:
                out.append('%s: the wrong line %r, expected LINES.%s.wrong.%s' % (i, s['say'], look, WRONG_KEY[t]))
            # One line at a time: the line is one LINES string, and the working under it holds none.
            fbtext = page.evaluate("document.getElementById('feedback').textContent")
            hits = [x for x in every if len(x) > 3 and x in fbtext]
            if s['say'] not in every or hits:
                out.append('%s: feedback holds %d LINES strings (the line %r, under it %s)' % (i, (s['say'] in every) + len(hits), s['say'], hits))
            if s['learn'] != working(q):
                out.append('%s: the working shown is %r, expected %r' % (i, s['learn'], working(q)))
            if t == 'array':
                a = page.evaluate(SCREEN_JS)
                if a['dots'] != q['rows'] * q['cols'] or a['rows'] != q['cols'] or a['cols'] != q['rows']:
                    out.append('%s: after marking the array is %d rows of %d, expected it turned round to %d rows of %d' % (i, a['rows'], a['cols'], q['cols'], q['rows']))
            marked += 1
    info['marked'] = info.get('marked', 0) + marked


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
    seen, right, k = [], 0, 0
    for _ in range(80):
        s = page.evaluate('ST.ui.state()')
        if s == 'over':
            break
        if s in ('count', 'ask'):
            q = page.evaluate('ST.ui.question()')
            seen.append(q['id'])
            if k < 2:
                fit(page, '#opts1 .opt' if s == 'count' else '#opts .opt', '%s %s (the options)' % (tag, q['id']), out)
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
    if len(seen) != PER or len(set(seen)) != PER or any(not (x.startswith(pre + '-') or x.startswith(pre + 'a-') or x.startswith(pre + 'b-')) for x in seen):
        out.append('%s: the run served %s, not %d different %s stage %s items' % (tag, seen, PER, md, st))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    evm = '%s-stage-%s' % (md, st)
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('level') != 'year6' or done[0].get('mode') != evm:
        out.append('%s: game_completed %s, expected one with score %d, mode %s' % (tag, done, right, evm))
    if sub != [[SLUG, board_of(m), right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d' % (tag, sub, board_of(m), right))
    qa = [p for n, p in ev if n == 'question_answered']
    if len(qa) != PER or [p.get('question_id') for p in qa] != seen or any(p.get('mode') != evm or p.get('level') != 'year6' for p in qa):
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
    if page.evaluate("document.getElementById('endLine').textContent") != L['end']:
        out.append('%s: the end line reads %r' % (tag, page.evaluate("document.getElementById('endLine').textContent")))
    if page.evaluate("document.getElementById('resScore').textContent") != str(right):
        out.append('%s: the end screen does not show %d' % (tag, right))
    page.evaluate("document.getElementById('menuBtn').click()")


def check_largest(page, look, out):
    for i in LARGEST:
        page.evaluate('(id) => ST.ui.preview(id)', i)
        q = page.evaluate('ST.ui.question()')
        if not q or q['id'] != i:
            out.append('largest: %s is not in the bank' % i)
            continue
        fit(page, '#opts1 .opt, #opts .opt', '%s %s at %dx%d (largest)' % (look, i, PHONE[0], PHONE[1]), out)


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
            for qid, want in (('m1-3x5', '3 groups of 5. How many thingies?'), ('m3-4r5c', '4 rows of 5. How many dots?'),
                              ('p4-3x4', '3 times 4 equals what?'), ('p4-q7x8', 'What times 8 equals 56?'),
                              ('m2a-3x5', '5 plus 5 plus 5. How many 5s?')):
                page.evaluate('(id) => ST.ui.preview(id)', qid)
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
    units = ['bank', 'marking grown', 'marking kids', 'greeting', 'read aloud', 'play grown %dx%d' % PHONE, 'play kids %dx%d' % PHONE]
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
