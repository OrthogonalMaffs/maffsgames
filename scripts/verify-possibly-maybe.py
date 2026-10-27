#!/usr/bin/env python3
# ci-shards: Possibly, Maybe (the 60-question fixed-seed bank and 20 seeds of every slot recomputed from each question's own data and ask, never from the bank's or the game's code: counts of sectors and counters, listed outcomes by enumeration, products, complements, expected numbers, relative frequencies, the fair-dice rule, every tree probability by exact fractions; fractions typed in two boxes marked by value against an independent marker on probe answers; every picture read back from its SVG; the page played at six sizes; planted faults each caught) | | 5
# ci-deps: games/possibly-maybe/ schools/assets/probability-game.js schools/assets/probability-generator.js schools/assets/fraction-input.js
"""Independent verification for Possibly, Maybe (games/possibly-maybe/), built 27 Oct 2026 (contract POSSIBLY-MAYBE, Jon).
SR-30: checked from its first PR.

The game imports the probability bank (schools/assets/probability-generator.js, canon 8.2.1) and adds only a thin layer
(schools/assets/probability-game.js); fractions are typed in two boxes with the new shared MaffsFractionInput
(schools/assets/fraction-input.js). This script loads them under Playwright, asks for every stage's questions, and recomputes
each answer HERE in Python, with exact fractions and by enumerating outcomes, from the question's own data and `ask` (never from
the bank's or the game's own arithmetic):

  Stage 1  the sectors or counters of a colour over all of them; the word for 0, evens and 1; the word for an event or an arrow;
           a fraction as a decimal and a percentage and back (lowest terms asked); a card's chance by listing the cards; the one
           value outside 0 to 1; the largest of three forms; the least likely colour.
  Stage 2  1 - P; a table that adds to 1 and its missing entry; x and 2x; "or" adds, "neither" is the rest; counts that add up.
  Stage 3  outcomes by product and by listing every pair (dice, spinners, a coin and a dice, two coins), favourable over all.
  Stage 4  probability x trials; relative frequency; the larger number of trials; the fair-dice rule; the gambler's fallacy.
  Stage 5  tree probabilities: both, neither, one way, exactly one, at least one, the missing branch, three events, decimals.
  Slips    every named slip is a value different from the right answer, no two the same, each a legal typed answer.
  Marking  MaffsProbabilityGame.mark() against an independent marker on probe answers (the key, every equivalent fraction, each
           slip, off-by-one values, unreadable input, 2/4 for a lowest-terms question): the same verdict.
  Bank     60 questions with the fixed seed, 12 distinct to a stage; the game's files copy no bank question text.
  Pictures every drawn spinner, bag, scale, grid, table and tree read back from its SVG against its data; all text at least 12 px;
           nothing leaving the picture; a key naming every colour.
  Page     one worked example then ten questions a stage; boxes, keys and Next above the fold at 390x844, 375x667, 360x640, 320x568,
           1280x720 and 1366x768; no sideways scroll; a mark only for a right answer; 2/4 for 1/2 right, 2/4 for a lowest-terms
           question never marked; one board submission a stage.

Work is in units (the bank, the marking, one view of every question per size, one play per size, one per planted fault) so CI
runs it whole or in slices (# ci-shards, scripts/ci_shards.py).
"""
import argparse
import contextlib
import json
import os
import random
import re
import sys
from fractions import Fraction as F
from itertools import product
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'possibly-maybe'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
ASSETS = os.path.join(ROOT, 'schools', 'assets')
FILES = {'probability-game.js': os.path.join(ASSETS, 'probability-game.js'),
         'probability-generator.js': os.path.join(ASSETS, 'probability-generator.js'),
         'fraction-input.js': os.path.join(ASSETS, 'fraction-input.js')}
SEEDS = 20
CANT = "You can't tell"
BIG = (390, 844)
SMALL = [(375, 667), (360, 640), (320, 568), (1280, 720), (1366, 768)]
FOOT = 40


# ---------------------------------------------------------------------------------------------------------------------------
# What each question should say, worked out here from its own data and ask.
# ---------------------------------------------------------------------------------------------------------------------------
def prob(s):
    """A probability written as a fraction, a decimal or a percentage."""
    s = s.strip().replace('−', '-')
    if s.endswith('%'):
        return F(s[:-1]) / 100
    if '/' in s:
        a, b = s.split('/')
        return F(int(a), int(b))
    return F(s)


def fr(p):
    return F(p[0], p[1])


def cells(chart, row=0):
    return chart['rows'][row]


def event_word(e):
    t = {'The sun rises tomorrow': 'certain', 'You roll a 7 on an ordinary dice': 'impossible', 'A fair coin lands on heads': 'evens',
         'You roll a 6 on a fair dice': 'unlikely', 'You roll a number less than 6 on a fair dice': 'likely',
         'The next baby born is a girl or a boy': 'certain', 'A person picked at random has three heads': 'impossible',
         'You pick a red card from a pack with one red card and 19 blue cards': 'unlikely',
         'You pick a blue card from a pack with one red card and 19 blue cards': 'likely'}
    return t[e]


def prime(x):
    return x > 1 and all(x % k for k in range(2, int(x ** 0.5) + 1))


def card_fav(N, test):
    if test == 'even':
        f = lambda i: i % 2 == 0  # noqa: E731
    elif test == 'a multiple of 3':
        f = lambda i: i % 3 == 0  # noqa: E731
    elif test == 'a prime number':
        f = prime
    else:
        k = int(test.split(' ')[2])
        f = lambda i: i > k  # noqa: E731
    return sum(1 for i in range(1, N + 1) if f(i))


def eval_expr(s):
    """'0.3 x 0.8 + 0.7 x 0.2' with exact fractions (sum of products)."""
    return sum(_prod(t) for t in s.split(' + '))


def _prod(t):
    v = F(1)
    for x in t.split(' x '):
        v *= F(x)
    return v


def solve(q):
    """The right answer as ('frac', Fraction) | ('num', Fraction) | ('choice', option), from ask and chart."""
    a, ch, op = q['ask'], q['chart'], q['ask']['op']
    t = q['answer']['type']
    if op == 'share':
        if ch['type'] == 'spinner':
            n = sum(1 for s in ch['sectors'] if s['name'] == a['of'])
            return ('frac', F(n, len(ch['sectors'])))
        n = [i['count'] for i in ch['items'] if i['name'] == a['of']][0]
        return ('frac', F(n, sum(i['count'] for i in ch['items'])))
    if op == 'word-value':
        return ('choice', {'impossible': '0', 'evens': '1/2', 'certain': '1'}[a['word']])
    if op == 'word-event':
        return ('choice', event_word(a['event']))
    if op == 'place':
        at = F(str(a['at']))
        return ('choice', 'unlikely' if at < F(3, 10) else ('evens' if at == F(1, 2) else 'likely'))
    if op == 'frac-to-dec':
        return ('num', F(a['n'], a['d']))
    if op == 'frac-to-pct':
        return ('num', F(a['n'] * 100, a['d']))
    if op == 'dec-to-frac':
        return ('frac', F(a['h'], 100))
    if op == 'cards':
        return ('frac', F(card_fav(a['N'], a['test']), a['N']))
    if op == 'cannot-be':
        out = [v for v in [a['bad']] + a['good'] if not 0 <= prob(v) <= 1]
        assert out == [a['bad']], out
        return ('choice', a['bad'])
    if op == 'order':
        vals = [prob(v) for v in a['values']]
        return ('choice', 'Event ' + 'ABC'[vals.index(max(vals))])
    if op == 'least':
        cnt = {}
        for s in ch['sectors']:
            cnt[s['name']] = cnt.get(s['name'], 0) + 1
        low = min(cnt.values())
        assert list(cnt.values()).count(low) == 1
        return ('choice', [k for k, v in cnt.items() if v == low][0])
    if op == 'not-frac':
        return ('frac', 1 - F(a['n'], a['d']))
    if op == 'not-dec':
        return ('num', 1 - F(a['h'], 100))
    if op == 'not-pct':
        return ('num', 100 - F(a['p']))
    if op == 'not-bag':
        c = [i['count'] for i in ch['items']]
        assert c == a['counts']
        return ('frac', F(sum(c) - c[0], sum(c)))
    if op in ('table-missing-dec', 'table-missing-frac', 'table-missing-pct'):
        row = cells(ch)
        known = [prob(x) for x in row if x != '?']
        assert row.count('?') == 1
        m = 1 - sum(known)
        return ('frac' if t == 'fraction' else 'num', m * (100 if op.endswith('pct') else 1))
    if op == 'x2x':
        row = cells(ch)
        assert row[0] == 'x' and row[1] == '2x'
        c = prob(row[2])
        return ('num', 2 * (1 - c) / 3)
    if op == 'x2x-four':
        row = cells(ch)
        assert row[0] == 'x' and row[1] == '2x'
        return ('frac', (1 - prob(row[2]) - prob(row[3])) / 3)
    if op == 'either':
        return ('num', F(a['a'] + a['b'], 100))
    if op == 'neither':
        return ('num', 1 - F(a['a'] + a['b'], 100))
    if op == 'counts-missing':
        row = cells(ch)
        n1, n2, tot = int(row[0]), int(row[1]), int(row[3])
        assert row[2] == '?'
        return ('frac', F(tot - n1 - n2, tot))
    if op == 'product':
        v = 1
        for f in a['factors']:
            v *= f
        return ('num', F(v))
    if op == 'dice-sum':
        n = sum(1 for i, j in product(range(1, 7), repeat=2) if i + j == a['t'])
        return ('frac', F(n, 36))
    if op == 'dice-double':
        return ('frac', F(sum(1 for i, j in product(range(1, 7), repeat=2) if i == j), 36))
    if op == 'dice-over':
        f = (lambda s: s > a['th']) if a['more'] else (lambda s: s < a['th'])
        return ('frac', F(sum(1 for i, j in product(range(1, 7), repeat=2) if f(i + j)), 36))
    if op == 'spinner-grid':
        n = sum(1 for i, j in product(range(1, a['A'] + 1), range(1, a['B'] + 1)) if i + j == a['t'])
        return ('frac', F(n, a['A'] * a['B']))
    if op == 'coin-dice-even':
        return ('frac', F(sum(1 for c, d in product('HT', range(1, 7)) if c == 'H' and d % 2 == 0), 12))
    if op == 'two-coins':
        return ('frac', F(sum(1 for x in product('HT', repeat=2) if 'H' in x), 4))
    if op == 'eleven-totals':
        ways = {}
        for i, j in product(range(1, 7), repeat=2):
            ways[i + j] = ways.get(i + j, 0) + 1
        assert len(set(ways.values())) > 1 and len(ways) == 11
        return ('choice', 'No: the totals are not equally likely')
    if op == 'menu-chance':
        return ('frac', F(1, a['s'] * a['m']))
    if op == 'same-spinners':
        n = sum(1 for i, j in product(range(1, a['n'] + 1), repeat=2) if i + j == a['t'])
        return ('frac', F(n, a['n'] ** 2))
    if op == 'expected':
        return ('num', F(a['trials'] * a['n'], a['d']))
    if op == 'expected-pct':
        return ('num', F(a['trials'] * a['p'], 100))
    if op == 'rel-freq':
        return ('frac', F(a['k'], a['t']))
    if op == 'rel-freq-dec':
        return ('num', F(a['k'], a['t']))
    if op == 'more-reliable':
        big = max(a['a'], a['b'])
        right = [o for o in q['answer']['options'] if '(%d ' % big in o]
        assert len(right) == 1
        return ('choice', right[0])
    if op == 'fair':
        counts = [int(x) for x in cells(ch)]
        tot = sum(counts)
        if tot < 30:
            return ('choice', CANT)
        e = F(tot, 6)
        return ('choice', 'Probably not fair' if max(abs(c - e) for c in counts) / e > F(45, 100) else 'Probably fair')
    if op == 'gambler':
        return ('choice', '1/2')
    if op == 'expected-not':
        return ('num', F(a['days'] * (100 - a['p']), 100))
    if op == 'expected-from-rel':
        return ('num', F(a['trials'] * a['k'], a['t']))
    if op in ('tree-both', 'tree-neither', 'tree-yes-no', 'tree-no-yes', 'tree-exactly-one', 'tree-at-least', 'tree-missing'):
        P, Q = (fr(a['p']), fr(a['q'])) if 'p' in a else (None, fr(a['q']))
        if op == 'tree-both':
            return ('frac', P * Q)
        if op == 'tree-neither':
            return ('frac', (1 - P) * (1 - Q))
        if op == 'tree-yes-no':
            return ('frac', P * (1 - Q))
        if op == 'tree-no-yes':
            return ('frac', (1 - P) * Q)
        if op == 'tree-exactly-one':
            return ('frac', P * (1 - Q) + (1 - P) * Q)
        if op == 'tree-at-least':
            return ('frac', 1 - (1 - P) * (1 - Q))
        return ('frac', Q)
    if op == 'three-events':
        return ('frac', F(a['n'], a['d']) ** 3)
    if op == 'dec-product':
        return ('num', F(a['a'], 100) * F(a['b'], 100))
    if op == 'at-least-dec':
        return ('num', 1 - (1 - F(a['a'], 100)) * (1 - F(a['b'], 100)))
    if op == 'neither-dec':
        return ('num', (1 - F(a['a'], 100)) * (1 - F(a['b'], 100)))
    if op == 'which-sum':
        p, qq = F(a['p']), F(a['q'])
        want = p * (1 - qq) + (1 - p) * qq
        good = [o for o in q['answer']['options'] if eval_expr(o) == want]
        assert len(good) == 1, good
        return ('choice', good[0])
    raise AssertionError('no solver for op %r' % op)


def key_of(ans):
    """The bank's answer as the same kind of tuple."""
    if ans['type'] == 'fraction':
        return ('frac', F(ans['num'], ans['den']))
    if ans['type'] == 'number':
        return ('num', F(ans['key']))
    return ('choice', ans['options'][ans['correct']])


def is_dec(s):
    return re.fullmatch(r'\d+(\.\d+)?', s) is not None


def check_question(q):
    """Everything this script can say about one question; returns a list of findings."""
    errs = []
    tag = 's%d slot %d %s' % (q['stage'], q['slot'], q['kind'])
    try:
        want = solve(q)
    except Exception as e:  # noqa: BLE001
        return ['%s: could not recompute (%s: %s)' % (tag, type(e).__name__, e)]
    got = key_of(q['answer'])
    if want != got:
        errs.append('%s: answer %s but the data gives %s (stem: %s)' % (tag, got[1], want[1], q['stem'][:70]))
    ans = q['answer']
    if ans['type'] == 'fraction':
        v = F(ans['num'], ans['den'])
        if not 0 < v <= 1:
            errs.append('%s: a probability answer %s outside 0 to 1' % (tag, v))
        if ans['den'] <= 0 or ans['num'] < 0:
            errs.append('%s: an illegal typed fraction %d/%d' % (tag, ans['num'], ans['den']))
        if ans['simplest'] and gcd(ans['num'], ans['den']) != 1:
            errs.append('%s: asks for lowest terms but the stored key %d/%d is not' % (tag, ans['num'], ans['den']))
    elif ans['type'] == 'number':
        if not re.fullmatch(r'\d+(\.\d+)?', ans['key']):
            errs.append('%s: the typed key %r is not a plain number' % (tag, ans['key']))
        if ans['unit'] == '%' and F(ans['key']) > 100:
            errs.append('%s: a percentage over 100' % tag)
    else:
        opts = ans['options']
        if len(set(opts)) != len(opts):
            errs.append('%s: repeated options' % tag)
        if not 0 <= ans['correct'] < len(opts):
            errs.append('%s: the right option index %s is not an option' % (tag, ans['correct']))
    # slips: different from the right answer, none repeated, each a legal typed answer, each with a line
    seen = []
    for s in q['slips']:
        sa = s['answer']
        if not s.get('line', '').strip():
            errs.append('%s: slip %s has no line' % (tag, s['kind']))
        if ans['type'] == 'fraction':
            if sa.get('den', 0) <= 0 or sa.get('num', -1) < 0:
                errs.append('%s: slip %s is not a typeable fraction %s/%s' % (tag, s['kind'], sa.get('num'), sa.get('den')))
                continue
            val = ('frac', F(sa['num'], sa['den']))
            if val[1] == F(ans['num'], ans['den']):
                errs.append('%s: slip %s equals the right answer' % (tag, s['kind']))
        elif ans['type'] == 'number':
            if not re.fullmatch(r'\d+(\.\d+)?', sa['key']):
                errs.append('%s: slip %s key %r is not typeable' % (tag, s['kind'], sa['key']))
                continue
            val = ('num', F(sa['key']))
            if val[1] == F(ans['key']):
                errs.append('%s: slip %s equals the right answer' % (tag, s['kind']))
        else:
            val = ('choice', sa['option'])
            if sa['option'] not in ans['options']:
                errs.append('%s: slip %s names an option that is not offered' % (tag, s['kind']))
            if sa['option'] == ans['options'][ans['correct']]:
                errs.append('%s: slip %s is the right option' % (tag, s['kind']))
        if val in seen:
            errs.append('%s: two slips the same (%s)' % (tag, s['kind']))
        seen.append(val)
    if not q['worked'] or not all(w.strip() for w in q['worked']):
        errs.append('%s: no working' % tag)
    # structure the contract names
    if q['stage'] == 1 and q['kind'] == 'cannot-be':
        pass
    return errs


# ---------------------------------------------------------------------------------------------------------------------------
# An independent marker, for the probes.
# ---------------------------------------------------------------------------------------------------------------------------
NUMRAW = re.compile(r'\d+(\.\d*)?|\.\d+')


def py_mark(q, raw):
    a = q['answer']
    raw = raw.strip()
    if a['type'] == 'choice':
        try:
            i = int(raw)
        except ValueError:
            return 'wrong'
        if i == a['correct']:
            return 'right'
        opt = a['options'][i] if 0 <= i < len(a['options']) else None
        return 'slip' if any(s['answer']['option'] == opt for s in q['slips']) else 'wrong'
    if a['type'] == 'number':
        if raw == '' or not NUMRAW.fullmatch(raw):
            return 'unreadable'
        v = F(raw if not raw.endswith('.') else raw[:-1])
        if v == F(a['key']):
            return 'right'
        return 'slip' if any(v == F(s['answer']['key']) for s in q['slips']) else 'wrong'
    if not re.fullmatch(r'\d+/\d+', raw):
        return 'unreadable'
    n, d = (int(x) for x in raw.split('/'))
    if d == 0:
        return 'unreadable'
    if F(n, d) == F(a['num'], a['den']):
        return 'format' if a['simplest'] and gcd(n, d) != 1 else 'right'
    return 'slip' if any(F(n, d) == F(s['answer']['num'], s['answer']['den']) for s in q['slips']) else 'wrong'


def probes(q, rng):
    a = q['answer']
    out = []
    if a['type'] == 'choice':
        out = [str(i) for i in range(len(a['options']))] + ['x', '-1', str(len(a['options']))]
    elif a['type'] == 'number':
        k = F(a['key'])
        out = [a['key'], a['key'] + '0' if '.' in a['key'] else a['key'] + '.0', '%g' % (float(k) + 1), '%g' % (float(k) * 10), '0', '', 'abc', '1,250', '.', '12abc']
        for s in q['slips']:
            out.append(s['answer']['key'])
        out += [str(rng.randint(0, 200)), '%.2f' % rng.uniform(0, 2)]
    else:
        n, d = a['num'], a['den']
        out = ['%d/%d' % (n, d), '%d/%d' % (2 * n, 2 * d), '%d/%d' % (3 * n, 3 * d), '%d/%d' % (n // gcd(n, d), d // gcd(n, d)),
               '%d/%d' % (n + 1, d), '%d/%d' % (n, d + 1), '%d/%d' % (d, n) if n else '1/1', '', '5', '3/', '/4', '3/0', ' 3 / 8 ', '1/2', '0/5']
        for s in q['slips']:
            sn, sd = s['answer']['num'], s['answer']['den']
            out += ['%d/%d' % (sn, sd), '%d/%d' % (2 * sn, 2 * sd)]
        out += ['%d/%d' % (rng.randint(0, 40), rng.randint(1, 40)) for _ in range(3)]
    return out


# ---------------------------------------------------------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------------------------------------------------------
SVG_JS = """() => {
  const svg = [...document.querySelectorAll('#figure svg, #exFigure svg')].find(x => x.getClientRects().length);
  if (!svg) return null;
  const vb = svg.viewBox.baseVal, box = svg.getBoundingClientRect();
  const txt = [...svg.querySelectorAll('text')].map(t => ({ s: t.textContent, px: parseFloat(getComputedStyle(t).fontSize), x: t.getBBox().x, y: t.getBBox().y,
    w: t.getBBox().width, h: t.getBBox().height, dc: t.getAttribute('data-cell'), dp: t.getAttribute('data-p'), db: t.getAttribute('data-branch'),
    dl: t.getAttribute('data-leaf'), cls: t.getAttribute('class') || '' }));
  return {
    vb: [vb.width, vb.height], w: box.width, h: box.height,
    n: svg.getAttribute('data-n'), at: svg.getAttribute('data-at'), cols: svg.getAttribute('data-cols'), rows: svg.getAttribute('data-rows'),
    tree: svg.getAttribute('data-tree'),
    wedges: [...svg.querySelectorAll('.wedge')].map(w => w.getAttribute('data-colour')),
    discs: [...svg.querySelectorAll('.disc')].map(w => w.getAttribute('data-colour')),
    arrow: (() => { const p = svg.querySelector('[data-arrow]'); return p ? p.getBBox().x + p.getBBox().width / 2 : null; })(),
    line: (() => { const l = svg.querySelector('line.axis'); return l ? [l.x1.baseVal.value, l.x2.baseVal.value] : null; })(),
    txt: txt };
}"""


def open_page(pw, base, size, sources=None, touch=None):
    sources = sources or {}
    br = pw.chromium.launch()
    touch = size[0] <= 600 if touch is None else touch
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    if 'page' in sources:
        ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
            status=200, content_type='text/html; charset=utf-8', body=sources['page']))
    def serve(name):
        ctx.route(lambda url: url.split('?')[0].endswith('/' + name), lambda route: route.fulfill(
            status=200, content_type='application/javascript; charset=utf-8', body=sources[name]))
    for name in FILES:
        if name in sources:
            serve(name)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.PM && !!PM.ui', timeout=10000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


QUESTIONS_JS = """(seeds) => {
  const B = window.MaffsProbability, out = [];
  for (let st = 1; st <= 5; st++) for (let sl = 0; sl < 12; sl++) for (let seed = 1; seed <= seeds; seed++)
    out.push(B.question(st, sl, B.makeRng(seed * 7919 + st * 31 + sl)));
  return out;
}"""

MARK_JS = """(items) => {
  const B = window.MaffsProbability, G = window.MaffsProbabilityGame;
  return items.map(([bankQ, raw]) => { const q = G.adapt(bankQ); const r = G.mark(q, [raw]); return r.kind; });
}"""


def check_bank(page, out, seeds=SEEDS):
    qs = page.evaluate(QUESTIONS_JS, seeds)
    per = {}
    for q in qs:
        out.extend(check_question(q))
    fixed = page.evaluate("() => MaffsProbability.bank()")
    if len(fixed) != 60:
        out.append('the fixed-seed bank has %d questions, not 60' % len(fixed))
    for st in range(1, 6):
        mine = [q for q in fixed if q['stage'] == st]
        stems = {q['stem'] for q in mine}
        kinds = {q['kind'] for q in mine}
        if len(stems) < 12 or len(kinds) < 12:
            out.append('stage %d: only %d distinct stems and %d kinds in the fixed bank, not 12' % (st, len(stems), len(kinds)))
        per[st] = (len(stems), len(kinds))
    for q in fixed:
        out.extend(check_question(q))
    # the twelve slots really are twelve different questions at every seed
    for st in range(1, 6):
        for si in range(min(seeds, 8)):
            ss = {q['stem'] for i, q in enumerate(qs) if q['stage'] == st and i % seeds == si}
            if len(ss) < 12:
                out.append('stage %d seed %d: only %d distinct stems over the 12 slots' % (st, si + 1, len(ss)))
    return {'questions': len(qs), 'fixed': per}


def check_marking(page, out, seeds=6):
    qs = page.evaluate(QUESTIONS_JS, seeds)
    rng = random.Random(5)
    items, expect, tags = [], [], []
    for q in qs:
        for raw in probes(q, rng):
            items.append([q, raw])
            expect.append(py_mark(q, raw))
            tags.append('s%d %s %r' % (q['stage'], q['kind'], raw))
    got = []
    for i in range(0, len(items), 600):
        got += page.evaluate(MARK_JS, items[i:i + 600])
    bad = 0
    for g, e, t in zip(got, expect, tags):
        if g != e:
            bad += 1
            if bad <= 25:
                out.append('mark() said %s, the independent marker says %s for %s' % (g, e, t))
    if bad > 25:
        out.append('... and %d more marking differences' % (bad - 25))
    # the game's files copy no bank question text
    return {'probes': len(items)}


def check_files(out):
    game = open(GAME, encoding='utf-8').read() + open(FILES['probability-game.js'], encoding='utf-8').read()
    for phrase in ['impossible and certain', 'A bag has ', 'Two fair dice are rolled', 'tree diagram shows two independent', 'goalkeeper faces']:
        if phrase in game:
            out.append('the game copies bank question text: %r' % phrase)


# ---------------------------------------------------------------------------------------------------------------------------
# Pictures read back from the SVG
# ---------------------------------------------------------------------------------------------------------------------------
def check_svg(fig, q, out, where):
    ch = q['chart']
    for t in fig['txt']:
        if t['px'] < 12 - 1e-6:
            out.append('%s: chart text %r is %.1f px, under 12' % (where, t['s'][:20], t['px']))
        if t['x'] < -0.5 or t['x'] + t['w'] > fig['vb'][0] + 0.5 or t['y'] < -0.5 or t['y'] + t['h'] > fig['vb'][1] + 0.5:
            out.append('%s: chart text %r leaves the picture' % (where, t['s'][:20]))
    texts = [t['s'] for t in fig['txt']]
    if ch['type'] == 'spinner':
        want = sorted(s['name'] for s in ch['sectors'])
        if sorted(fig['wedges']) != want:
            out.append('%s: wedges drawn %s, data %s' % (where, sorted(fig['wedges']), want))
        for s in ch['sectors']:
            if s['letter'] != s['name'][0].upper():
                out.append('%s: sector letter %s for %s' % (where, s['letter'], s['name']))
        letters = [t['s'] for t in fig['txt'] if 'lt' in t['cls']]
        if sorted(letters) != sorted(s['name'][0].upper() for s in ch['sectors']):
            out.append('%s: the letters drawn in the sectors do not match their colours: %s' % (where, sorted(letters)))
        for nm in set(want):
            if not any(('%s = %s' % (nm[0].upper(), nm)) in x for x in texts):
                out.append('%s: no key for %s' % (where, nm))
    elif ch['type'] == 'bag':
        want = sorted(i['name'] for i in ch['items'] for _ in range(i['count']))
        if sorted(fig['discs']) != want:
            out.append('%s: counters drawn %s, data %s' % (where, sorted(fig['discs']), want))
    elif ch['type'] == 'numberline':
        x0, x1 = fig['line']
        exp = x0 + ch['at'] * (x1 - x0)
        if fig['arrow'] is None or abs(fig['arrow'] - exp) > 1.0:
            out.append('%s: the arrow is at x=%s, the data puts it at %.1f' % (where, fig['arrow'], exp))
    elif ch['type'] == 'grid':
        got = [t['dc'] for t in fig['txt'] if t['dc'] is not None]
        want = [ch['corner'] or ''] + ch['colHead'] + [x for i, rh in enumerate(ch['rowHead']) for x in [rh] + ch['cells'][i]]
        if got != want:
            out.append('%s: the grid cells drawn do not match the data' % where)
    elif ch['type'] == 'table':
        got = [t['dc'] for t in fig['txt'] if t['dc'] is not None]
        want = ch['head'] + [x for r in ch['rows'] for x in r]
        if got != want:
            out.append('%s: the table cells drawn %s, data %s' % (where, got, want))
    elif ch['type'] == 'tree':
        b1 = [t['dp'] for t in fig['txt'] if t['db'] == '1']
        b2 = [t['dp'] for t in fig['txt'] if t['db'] == '2']
        w1 = [x['p'] for x in ch['first']]
        w2 = [x['p'] for row in ch['second'] for x in row]
        if b1 != w1 or b2 != w2:
            out.append('%s: tree branch labels %s %s, data %s %s' % (where, b1, b2, w1, w2))
        shown1 = [t['s'] for t in fig['txt'] if t['db'] == '1']
        shown2 = [t['s'] for t in fig['txt'] if t['db'] == '2']
        if shown1 != w1 or shown2 != w2:
            out.append('%s: a tree branch is labelled %s %s, the data says %s %s' % (where, shown1, shown2, w1, w2))
        # the labels agree with the question's own ask (never read from the chart alone)
        a = q['ask']
        if 'p' in a and ch['first'][0]['p'] != '%d/%d' % tuple(a['p']):
            out.append('%s: the tree says P(first Yes) = %s, the ask says %s' % (where, ch['first'][0]['p'], a['p']))
        if 'q' in a and q['ask']['op'] != 'tree-missing' and ch['second'][0][0]['p'] != '%d/%d' % tuple(a['q']):
            out.append('%s: the tree says P(second Yes) = %s, the ask says %s' % (where, ch['second'][0][0]['p'], a['q']))
        if len(shown1) != 2 or len(shown2) != 4:
            out.append('%s: a tree with %d first and %d second branch labels' % (where, len(shown1), len(shown2)))


def check_screen(page, q, out, where, qtag, fold):
    """The question on screen: the answer controls and the keypad above the fold, no sideways scroll, the picture read back."""
    m = page.evaluate("""() => { const r = [...document.querySelectorAll('#answer input, #answer button, #kpHolder button')].filter(x => x.offsetParent).map(x => x.getBoundingClientRect());
        return { last: r.length ? Math.max(...r.map(x => x.bottom)) : 0, sw: document.documentElement.scrollWidth, iw: innerWidth, right: r.length ? Math.max(...r.map(x => x.right)) : 0 }; }""")
    if m['last'] > fold + 0.5:
        out.append('%s %s (%s): answer controls end at %d, below the fold (%d)' % (where, qtag, q['kind'], m['last'], fold))
    if m['sw'] > m['iw'] or m['right'] > m['iw'] + 0.5:
        out.append('%s %s: sideways scroll or a control off the screen (%d > %d)' % (where, qtag, max(m['sw'], m['right']), m['iw']))
    if q['chart']:
        fig = page.evaluate(SVG_JS)
        if not fig:
            out.append('%s %s: no picture on screen' % (where, qtag))
        else:
            check_svg(fig, q, out, '%s %s (%s)' % (where, qtag, q['kind']))
    elif page.evaluate("() => !!document.querySelector('#figure svg')"):
        out.append('%s %s (%s): a picture on a question that has none' % (where, qtag, q['kind']))


def font(page):
    page.add_style_tag(content='body,button,input{font-family:Verdana,"DejaVu Sans",sans-serif!important}')


def fit_all(base, size, out, seeds=(1,), sources=None):
    """Every kind of question (all 12 slots of all 5 stages) on its own at one size: fit, picture read-back, the feedback after a
    wrong answer with Next above the fold, and 2/4 for a lowest-terms question never marked."""
    from playwright.sync_api import sync_playwright
    fold = size[1] - FOOT
    where = '%dx%d' % size
    with sync_playwright() as pw:
        br, page, errs = open_page(pw, base, size, sources)
        if size[0] <= 600:
            font(page)
        try:
            for st in range(1, 6):
                for slot in range(12):
                    for seed in seeds:
                        page.evaluate('PM.ui.preview(%d, %d, %d)' % (st, slot, seed))
                        page.wait_for_function("PM.ui.state() === 'asking'", timeout=8000)
                        q = page.evaluate('PM.ui.question()')
                        page.wait_for_timeout(30)
                        tag = 's%d slot %d' % (st, slot)
                        check_screen(page, q, out, where + ' ' + tag, 'seed %d' % seed, fold)
                        if q['type'] == 'fraction' and q['simplest']:
                            n, d = q['key']['num'], q['key']['den']
                            page.evaluate("PM.ui.type('%d/%d')" % (2 * n, 2 * d))
                            page.wait_for_timeout(40)
                            if page.evaluate('PM.ui.state()') != 'asking' or int(page.inner_text('#hudScore')) != 0:
                                out.append('%s %s: an unsimplified fraction was marked on a lowest-terms question' % (where, tag))
                            elif 'simplify' not in page.inner_text('#msg').lower():
                                out.append('%s %s: no "simplify it fully" message for an unsimplified fraction' % (where, tag))
                        page.evaluate('PM.ui.answer(false)')
                        page.wait_for_timeout(50)
                        nb = page.evaluate("() => { const n = document.querySelector('.maffs-next, #nextBtn'); return n ? n.getBoundingClientRect().bottom : null; }")
                        if nb is None or nb > fold + 0.5:
                            out.append('%s %s (%s): after a wrong answer Next is %s, below the fold (%d)' % (where, tag, q['kind'], nb, fold))
            if size[0] <= 600:
                tap_test(page, size, out)
        except Exception as e:  # noqa: BLE001
            out.append('every-question view at %s threw: %s' % (where, (str(e).splitlines() or [type(e).__name__])[0][:220]))
        out.extend('page error at %s: %s' % (where, e) for e in errs)
        br.close()


def tap_test(page, size, out):
    """A real tap on the numerator, the keys, the denominator: the boxes hold what was tapped."""
    page.evaluate('PM.ui.preview(1, 1 + 3, 1)')           # stage 1 slot 4: a bag, a fraction
    q = page.evaluate('PM.ui.question()')
    if q['type'] != 'fraction':
        out.append('the tap test expected a fraction question, got %s' % q['type'])
        return
    boxes = page.query_selector_all('.mfi-in')
    if len(boxes) != 2:
        out.append('a fraction question shows %d boxes, not two' % len(boxes))
        return
    def key(label):
        page.locator('#kpHolder button', has_text=re.compile('^%s$' % label)).first.tap()
    boxes[0].tap(); key('3'); key('4')
    boxes[1].tap(); key('8')
    got = page.evaluate("() => [...document.querySelectorAll('.mfi-in')].map(b => b.value)")
    if got != ['34', '8']:
        out.append('tapping 3 4 in the top box and 8 in the bottom gave %s' % got)


def play_stage(page, st, size, out, n, full):
    w, h = size
    fold = h - FOOT
    where = '%dx%d stage %d' % (w, h, st)
    page.evaluate('window.__ev = []; window.__sub = []')
    if full:                                           # the worked example, step by step, then the questions
        page.evaluate('PM.ui.start(%d, true)' % st)
        page.wait_for_selector('#exBtn', state='visible')
        steps = 0
        while 'Start the questions' not in page.inner_text('#exBtn') and steps < 12:
            page.click('#exBtn')
            steps += 1
            page.wait_for_timeout(50)
        if steps < 2 or not page.query_selector('#exSteps li'):
            out.append('%s: the worked example has no steps' % where)
        page.click('#exBtn')
    else:
        page.evaluate('PM.ui.start(%d)' % st)
    expect = 0
    for qn in range(n):
        page.wait_for_function("PM.ui.state() === 'asking'", timeout=8000)
        q = page.evaluate('PM.ui.question()')
        page.wait_for_timeout(80)
        check_screen(page, q, out, where, 'q%d' % qn, fold)
        kind = 'right'
        if qn == 1:
            kind = 'slip'
        elif qn == 2:
            kind = 'wrong'
        key = q['key']
        note = None
        if q['type'] == 'choice':
            if kind == 'right':
                pick = key
            elif kind == 'slip' and q['slips']:
                pick = q['options'].index(q['slips'][0]['option'])
                note = q['slips'][0]['line']
            else:
                free = [i for i in range(len(q['options'])) if i != key and not any(q['options'][i] == s['option'] for s in q['slips'])]
                if free:
                    kind, pick = 'wrong', free[0]
                else:                                         # every wrong option is a named slip: take one
                    pick = next(i for i in range(len(q['options'])) if i != key)
                    kind = 'slip'
                    note = next(s['line'] for s in q['slips'] if s['option'] == q['options'][pick])
            page.evaluate('PM.ui.type(%d)' % pick)
        else:
            if q['type'] == 'fraction':
                good = '%d/%d' % (key['num'], key['den'])
                if not q['simplest'] and qn % 2 == 1:
                    good = '%d/%d' % (2 * key['num'], 2 * key['den'])        # an equivalent fraction is equal
                bad = '%d/%d' % (key['num'] + 7, key['den'] + 11)
                if kind == 'slip' and q['slips']:
                    bad, note = '%d/%d' % (q['slips'][0]['num'], q['slips'][0]['den']), q['slips'][0]['line']
                elif kind == 'slip':
                    kind = 'wrong'
            else:
                good = key
                bad = str(float(key) + 7.5)
                if kind == 'slip' and q['slips']:
                    bad, note = q['slips'][0]['key'], q['slips'][0]['line']
                elif kind == 'slip':
                    kind = 'wrong'
            page.evaluate('PM.ui.type(%s)' % json.dumps(good if kind == 'right' else bad))
        page.wait_for_timeout(120)
        ok = kind == 'right'
        if ok:
            expect += 1
        if int(page.inner_text('#hudScore')) != expect:
            out.append('%s q%d: marks show %s, expected %d (a wrong answer scored, or a right one did not)' % (where, qn, page.inner_text('#hudScore'), expect))
        fb = page.evaluate("""() => { const n = document.querySelector('.maffs-next, #nextBtn'), l = document.querySelector('.fb-line');
            return { next: n ? n.getBoundingClientRect().bottom : null, line: l ? l.textContent : '', done: !!document.querySelector('.fb.done') }; }""")
        if fb['next'] is None or fb['next'] > fold + 0.5:
            out.append('%s q%d (%s, %s): Next is %s, below the fold (%d)' % (where, qn, q['kind'], kind, fb['next'], fold))
        if fb['done'] != ok:
            out.append('%s q%d (%s): the feedback says %s' % (where, qn, kind, 'right' if fb['done'] else 'not right'))
        if note and re.sub(r'\s+', ' ', note).strip() not in re.sub(r'\s+', ' ', fb['line']):
            out.append('%s q%d: the named slip was not shown: %r (the line says %r)' % (where, qn, note[:40], fb['line'][:60]))
        if not fb['line'].strip():
            out.append('%s q%d: no feedback line' % (where, qn))
        if ok:
            page.evaluate("document.getElementById('nextBtn').click()")
        else:
            page.evaluate("document.querySelector('.maffs-next').click()")
        page.wait_for_timeout(70)
    if full and n >= 10:
        page.wait_for_function("document.getElementById('results').classList.contains('active')", timeout=8000)
        sub = page.evaluate('window.__sub')
        comp = [p for nm, p in page.evaluate('window.__ev') if nm == 'game_completed']
        if len(sub) != 1 or sub[0][0] != SLUG or sub[0][1] != 'stage-%d' % st or sub[0][2] != expect:
            out.append('%s: the leaderboard got %s, the marks were %d on stage-%d' % (where, sub, expect, st))
        if len(comp) != 1 or comp[0].get('score') != expect or comp[0].get('mode') != 'stage-%d' % st:
            out.append('%s: game_completed says %s, the marks were %d' % (where, comp, expect))
        if int(page.inner_text('#resScore')) != expect:
            out.append('%s: the results screen shows %s, not %d' % (where, page.inner_text('#resScore'), expect))
        if st < 5 and 'Next: Stage %d' % (st + 1) not in page.inner_text('#nextStageBtn'):
            out.append('%s: no "Next: Stage %d" button' % (where, st + 1))
        allowed = {'game_slug', 'level', 'mode', 'question_index', 'correct', 'score', 'questions_answered', 'questions_correct', 'previous_best'}
        for nm, p in page.evaluate('window.__ev'):
            if set(p) - allowed:
                out.append('%s: an event field outside the existing events: %s' % (where, sorted(set(p) - allowed)))
                break
    return expect


def play_size(base, size, out, n, full, sources=None, stages=range(1, 6)):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        br, page, errs = open_page(pw, base, size, sources)
        if size[0] <= 600:
            font(page)
        try:
            for st in stages:
                play_stage(page, st, size, out, n, full)
                page.evaluate("document.getElementById('menuBtn') && document.getElementById('menuBtn').click()")
        except Exception as e:  # noqa: BLE001
            out.append('play at %dx%d threw: %s' % (size[0], size[1], (str(e).splitlines() or [type(e).__name__])[0][:220]))
        out.extend('page error at %dx%d: %s' % (size[0], size[1], e) for e in errs)
        br.close()


def engine(base, out, sources=None, seeds=SEEDS, marking=True, bank=True):
    from playwright.sync_api import sync_playwright
    info = {}
    with sync_playwright() as pw:
        br, page, errs = open_page(pw, base, (1280, 800), sources)
        try:
            if bank:
                info.update(check_bank(page, out, seeds))
            if marking:
                info.update(check_marking(page, out, max(2, seeds // 4)))
        except Exception as e:  # noqa: BLE001
            out.append('the engine checks threw: %s' % (str(e).splitlines() or [type(e).__name__])[0][:200])
        out.extend('page error: ' + e for e in errs)
        br.close()
    return info


# ---------------------------------------------------------------------------------------------------------------------------
# Planted faults: (what, file, [(old, new)], kind, pattern the finding must match). 'engine' plants run the bank and marking
# checks; 'view' plants look at every question at one size; 'play' plants play stages.
# ---------------------------------------------------------------------------------------------------------------------------
PLANTS = [
    ('P(not A) answered as P(A) (the bank)', 'probability-generator.js',
     [("{ op: 'not-frac', n: n, d: d }, frac(d - n, d),", "{ op: 'not-frac', n: n, d: d }, frac(n, d),")], 'engine', r'not-frac: answer'),
    ('two dice totals counted unordered (21 outcomes)', 'probability-generator.js',
     [("{ op: 'dice-sum', t: t }, frac(fav, 36),", "{ op: 'dice-sum', t: t }, frac(unord, 21),")], 'engine', r'dice-sum: answer'),
    ('expected number as trials minus the answer', 'probability-generator.js',
     [("{ op: 'expected', n: n, d: d, trials: trials }, numA(key),", "{ op: 'expected', n: n, d: d, trials: trials }, numA(trials - key),")], 'engine', r'expected-dec: answer'),
    ('"at least one" answered as P(none)', 'probability-generator.js',
     [("{ op: 'tree-at-least', p: P, q: Q }, frac(D - pn * qn, D),", "{ op: 'tree-at-least', p: P, q: Q }, frac(pn * qn, D),")], 'engine', r'tree-at-least: answer'),
    ('a named slip equal to the right answer', 'probability-generator.js',
     [("[slipF('part-to-part', counts[0], t - counts[0], 'That compares ' + names[0] + ' with the others (' + (counts[0] > t - counts[0] ? 'and gives more than 1, which a probability never is' : 'ratio style') + '). The bottom is ALL the counters, ' + t + '.')]);",
       "[slipF('part-to-part', counts[0], t, 'planted')]);"),
      ("if (s.answer.den === 0 || same(s.answer, right)) return;", "if (s.answer.den === 0) return;")], 'engine', r'slip part-to-part equals the right answer'),
    ('equivalent fractions not accepted (the game)', 'probability-game.js',
     [("var key = reduce(q.key.num, q.key.den);", "var key = q.key;")], 'engine', r'mark\(\) said'),
    ('lowest terms not enforced (the game)', 'probability-game.js',
     [("if (q.simplest) {", "if (false) {")], 'engine', r'mark\(\) said'),
    ('a sector drawn with the wrong letter (the page)', 'page',
     [("class: 'lt', x: (cx + rr * Math.cos(am)).toFixed(1), y: (cy + rr * Math.sin(am) + 4).toFixed(1), 'text-anchor': 'middle' }, s.letter));",
       "class: 'lt', x: (cx + rr * Math.cos(am)).toFixed(1), y: (cy + rr * Math.sin(am) + 4).toFixed(1), 'text-anchor': 'middle' }, 'R'));")], 'view', r'(letters drawn|sector letter)'),
    ('a tree branch labelled with the wrong probability', 'page',
     [("'text-anchor': 'middle' }, b.p));", "'text-anchor': 'middle' }, ch.first[0].p));")], 'view', r'tree branch'),
    ('chart text under 12 px', 'page',
     [(".charts text{font-family:var(--font-num);font-size:12px;", ".charts text{font-family:var(--font-num);font-size:10px;")], 'view', r'chart text .* px'),
    ('a wrong answer counted as a mark (the page)', 'page',
     [("answered++; if (ok) { rightCount++; marks++; }", "answered++; marks++; if (ok) { rightCount++; }")], 'play', r'(marks show|the leaderboard got|game_completed says)'),
    ('the numerator and denominator swapped (the shared input)', 'fraction-input.js',
     [("return n === '' && d === '' ? '' : n + '/' + d;", "return n === '' && d === '' ? '' : d + '/' + n;")], 'play', r'(marks show|feedback says)'),
    ('a lowest-terms question marked on 2/4 (the page counts a format answer)', 'page',
     [("if (r.kind === 'unreadable' || r.kind === 'format') {", "if (r.kind === 'unreadable') {")], 'view', r'unsimplified fraction was marked'),
]


def run_plant(plant):
    what, which, edits, kind, want = plant
    srcs = {'page': open(GAME, encoding='utf-8').read()}
    srcs.update({n: open(p, encoding='utf-8').read() for n, p in FILES.items()})
    src = srcs[which]
    for old, new in edits:
        if src.count(old) != 1:
            print('  self-test %-72s *** CANNOT PLANT (%r) ***' % (what, old[:50]))
            return False
        src = src.replace(old, new)
    srcs[which] = src
    got = []
    proc, base = bc.start_stub_server()
    try:
        if kind == 'engine':
            engine(base, got, srcs, seeds=8)
        elif kind == 'view':
            fit_all(base, (375, 667), got, sources=srcs)
        else:
            play_size(base, BIG, got, 4, True, sources=srcs, stages=[1, 2])
    finally:
        proc.terminate()
    hit = [g for g in got if re.search(want, g)]
    print('  self-test %-72s %s' % (what, ('caught: ' + hit[0][:90]) if hit else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '')))
    return bool(hit)


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    shard = bc.Shard(__file__, args)
    units = ['bank', 'marking'] + ['view %dx%d' % s for s in [BIG] + SMALL] + ['play %dx%d' % BIG] + \
        ['first %dx%d' % s for s in SMALL[:3]] + ['plant: ' + p[0] for p in PLANTS]
    if args.list_units:
        print('\n'.join(units))
        return 0
    mine = shard.pick(units)
    out = []
    ok = True
    proc, base = bc.start_stub_server()
    try:
        if 'bank' in mine:
            with shard.unit('bank'):
                check_files(out)
                info = engine(base, out, None, SEEDS, marking=False)
            print('%s: %s' % (SLUG, info))
        if 'marking' in mine:
            with shard.unit('marking'):
                info = engine(base, out, None, SEEDS, bank=False)
            print('%s: %s' % (SLUG, info))
        for size in [BIG] + SMALL:
            uid = 'view %dx%d' % size
            if uid in mine:
                with shard.unit(uid):
                    fit_all(base, size, out, seeds=(1, 2) if size == BIG else (1,))
                print('%s: every kind of question viewed at %dx%d' % (SLUG, size[0], size[1]))
        if 'play %dx%d' % BIG in mine:
            with shard.unit('play %dx%d' % BIG):
                play_size(base, BIG, out, 10, True)
            print('%s: all five stages played at %dx%d' % (SLUG, BIG[0], BIG[1]))
        for size in SMALL[:3]:
            uid = 'first %dx%d' % size
            if uid in mine:
                with shard.unit(uid):
                    play_size(base, size, out, 3, False)
                print('%s: three questions a stage at %dx%d' % (SLUG, size[0], size[1]))
    finally:
        proc.terminate()
    for p in PLANTS:
        if 'plant: ' + p[0] in mine:
            with shard.unit('plant: ' + p[0]):
                ok = run_plant(p) and ok
    for f in out[:60]:
        print('FAIL  ' + f)
    if len(out) > 60:
        print('FAIL  ... and %d more' % (len(out) - 60))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
