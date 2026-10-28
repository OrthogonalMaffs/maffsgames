#!/usr/bin/env python3
# ci-shards: It's on Sale! (every question of the five stages over 40 seeds a slot recomputed from its own params with exact fractions, never from the module's code: answer, every named slip, the numbers in the stem, the worked lines; sessions of 10 slots easiest first with the example never among them; the game's marking against an independent marker on thousands of typed answers: format, unreadable, slip, wrong, right; every stage played in the page at 390 px, a full stage each, and at 375 px, the first questions: worked example, typed answers on the tag with the keypad open, a format answer never marked, a named slip, the calculator note and badge by stage, the Stage 5 calculator open; answer box, Check and Next above the fold; no sideways scroll; one submission a stage; every stage played at 360, 320, 1280 and 1366 px, the first questions: the same checks, the short phones and the two laptop sizes; fault-injection self-test: the planted faults, each caught, including a wrong new price, a reverse percentage worked the wrong way round and a format answer marked right) | | 4
# ci-deps: games/its-on-sale/ schools/assets/percentages-money-generator.js
"""Independent verification for It's on Sale! (games/its-on-sale/), built 27 Oct 2026 (contract ITS-ON-SALE, Jon).
SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The questions come from the bank's generator (schools/assets/percentages-money-generator.js, imported by the game, canon 8.2.1).
This script loads that file and the page under Playwright, asks for each stage's questions by slot and seed, and recomputes in
Python, from each question's own `params` and with exact fractions, never from the generator's integer code:

  Answer    stage 1 p% of B; stage 2 B -+ p% of B; stage 3 the percentage change |N - O| / O x 100; stage 4 the original from
            N = k% of it; stage 5 simple interest P r y / 100, compound and depreciation P (100 -+ r)^y / 100^y rounded half up to
            the penny, interest or total as asked.
  Slips     every named slip's value is recomputed by its kind, differs from the answer and from every other slip.
  Stem      the amounts, the percentage and the years in the wording are the params' (a stem that says 20% over a 30% sum fails).
  Worked    at least two lines, and the answer written out in them.
  Session   10 distinct slots of 1 to 11, ascending (easiest first), the worked example (slot 0) never among them; no repeated
            stem within a session.
  Marking   the game's mark() against an independent marker on typed answers (the answer in every accepted form, a wrong form
            of it, one penny and ten pence out, every slip, junk): the same verdict for every one: right, format (never
            marked), unreadable (never marked), slip (named) or wrong.
  Page      every stage played; the answer box, Check and the keypad (or, in stage 5, the open calculator) above the fold at
            five phone and laptop sizes; no sideways scroll; a format answer never marked; one board submission a stage.

Work units (contract SHARD; CI runs a slice with --shard i/k, scripts/ci-groups.py chooses k): "engine" (the bank and the
marking, on one 1280x800 page), "full 390x844" (every stage played through at 390 px), "first WxH" (the first questions of
every stage at one of the other five sizes) and "plant: <what>" (one per planted fault). It was merged on 27 Oct 2026 with
four hand-made parts (--part 1..4), which ci-groups.py refuses since SHARD.
"""
import argparse
import contextlib
import math
import os
import random
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'its-on-sale'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
MODULE = os.path.join(ROOT, 'schools', 'assets', 'percentages-money-generator.js')
GEN_SRC = 'percentages-money-generator.js'
SEEDS = 40
SIZES = [(390, 844), (375, 667), (360, 640), (320, 568), (1280, 720), (1366, 768)]
FULL = {(390, 844)}                    # the sizes at which a whole stage is played; the others play the first questions
BOARD = {n: 'stage-%d' % n for n in range(1, 6)}


def half_up(x):                         # a Fraction to the nearest penny, halves up
    return math.floor(x + Fraction(1, 2))


def money(p):
    return '£' + (str(p // 100) if p % 100 == 0 else '%d.%02d' % (p // 100, p % 100))


# ---------------------------------------------------------------- recompute a question from its params
def expected(q):
    st, p = q['stage'], q['params']
    if st == 1:
        return {'money': Fraction(p['base'] * p['pct'], 100)}, []
    if st == 2:
        x = Fraction(p['base'] * p['pct'], 100)
        ans = p['base'] - x if p['dir'] == 'dec' else p['base'] + x
        return {'money': ans}, [('only_percentage', {'money': x})]
    if st == 3:
        O, N = p['old'], p['new']
        v = Fraction(abs(N - O) * 100, O)
        over = Fraction(abs(N - O) * 100, N)
        slips = []
        if (over * 100).denominator == 1 and over != v:        # only where a student can type it exactly
            slips.append(('over_new', {'value': over}))
        return {'value': v}, slips
    if st == 4:
        k = 100 - p['pct'] if p['dir'] == 'dec' else 100 + p['pct']
        ans = Fraction(p['newp'] * 100, k)
        wrong = Fraction(p['newp'] * (100 - p['pct'] if p['dir'] == 'dec' else 100 + p['pct']), 100)
        slips = [('off_sale_price', {'money': wrong})] if wrong.denominator == 1 and wrong != ans else []
        return {'money': ans}, slips
    P, r, y, qty, kind = p['principal'], p['rate'], p['years'], p['qty'], p['kind']
    if kind == 'simple':
        I = Fraction(P * r * y, 100)
        ans = I if qty == 'interest' else P + I
        comp = half_up(Fraction(P) * (100 + r) ** y / Fraction(100) ** y)
        return {'money': ans}, [('compound_for_simple', {'money': comp - P if qty == 'interest' else comp})]
    m = 100 - r if kind == 'depreciation' else 100 + r
    amount = half_up(Fraction(P) * m ** y / Fraction(100) ** y)
    q0 = P if qty == 'interest' else 0
    ans = amount - q0
    slips = []
    if kind == 'compound':
        slips.append(('simple_for_compound', {'money': half_up(Fraction(P * 100 + P * r * y, 100)) - q0}))
        slips.append(('times_years', {'money': half_up(Fraction(P * m * y, 100)) - q0}))
        if r < 10:
            slips.append(('multiplier_digit', {'money': half_up(Fraction(P) * (100 + r * 10) ** y / Fraction(100) ** y) - q0}))
    else:
        slips.append(('depreciation_added', {'money': half_up(Fraction(P) * (100 + r) ** y / Fraction(100) ** y) - q0}))
        if r % 10 == 0:
            slips.append(('multiplier_digit', {'money': half_up(Fraction(P) * r ** y / Fraction(100) ** y) - q0}))
    return {'money': ans}, [(k, v) for k, v in slips if v['money'] != ans]


def friendly_expected(q, ans):
    """The bank header's rule, recomputed here from the params (CALC-OPTIONAL, 28 Oct 2026): the hint shows only where every step is
    one easy mental step, that is a percentage of 10, 25 or 50 and a whole number of pounds in every amount of the working. Stages 4
    and 5 are never friendly."""
    st, p = q['stage'], q['params']
    if st == 1:
        pct, amounts = p['pct'], [p['base'], Fraction(p['base'] * p['pct'], 100)]
    elif st == 2:
        x = Fraction(p['base'] * p['pct'], 100)
        pct, amounts = p['pct'], [p['base'], x, p['base'] - x if p['dir'] == 'dec' else p['base'] + x]
    elif st == 3:
        pct, amounts = ans['value'], [p['old'], abs(p['new'] - p['old']), p['new']]
    else:
        return False
    return pct in (10, 25, 50) and all(Fraction(a) % 100 == 0 for a in amounts)


def val(a):                              # an expected answer: {'money': pence} or {'value': percent}
    return a.get('money') if 'money' in a else a.get('value')


def bval(a):                             # the bank's answer: {'pence': n} or {'value': v}
    return a['pence'] if 'pence' in a else a['value']


def check_question(q):
    errs = []
    tag = 's%d slot %d' % (q['stage'], q['slot'])
    try:
        ans, slips = expected(q)
    except (KeyError, ZeroDivisionError, TypeError) as e:
        return ['%s: params could not be read (%s)' % (tag, e)]
    a = q['answer']
    if 'money' in ans:
        if a.get('type') != 'money' or Fraction(a['pence']) != ans['money'] or ans['money'].denominator != 1:
            errs.append('%s: answer %s but the params give %s pence' % (tag, a, ans['money']))
    else:
        if a.get('type') != 'percent' or Fraction(str(a['value'])) != ans['value']:
            errs.append('%s: answer %s but the params give %s%%' % (tag, a, ans['value']))
    if (q['stage'] == 3) != (a.get('type') == 'percent'):
        errs.append('%s: only stage 3 has a percentage answer' % tag)
    # the slips: every expected one is present with the recomputed value; none equals the answer or another slip
    seen = [val(ans)]
    have = {s['kind']: s for s in q['slips']}
    for kind, v in slips:
        got = have.get(kind)
        if not got:
            errs.append('%s: the slip %s is missing' % (tag, kind))
            continue
        gv = Fraction(str(bval(got['answer'])))
        if gv != val(v):
            errs.append('%s: slip %s is %s but the params give %s' % (tag, kind, gv, val(v)))
    for s in q['slips']:
        gv = Fraction(str(bval(s['answer'])))
        if gv in seen:
            errs.append('%s: slip %s has the value of the answer or of another slip' % (tag, s['kind']))
        seen.append(gv)
        if not s['line'] or len(s['line']) > 330:
            errs.append('%s: slip %s has no line, or a long one' % (tag, s['kind']))
        if s['kind'] not in [k for k, _ in slips]:
            errs.append('%s: an unexpected slip %s' % (tag, s['kind']))
    # the stem carries the params' numbers
    p, st, stem = q['params'], q['stage'], q['stem']
    need = []
    if st == 1:
        need = [money(p['base']), '%d%%' % p['pct']]
    elif st == 2:
        need = [money(p['base']), '%d%%' % p['pct'], 'reduced by' if p['dir'] == 'dec' else 'goes up by']
    elif st == 3:
        need = [money(p['old']), money(p['new'])]
    elif st == 4:
        need = [money(p['newp']), '%d%%' % p['pct'], 'reduction' if p['dir'] == 'dec' else 'rise']
    else:
        need = [money(p['principal']), '%d%%' % p['rate'], '%d years' % p['years'],
                {'simple': 'simple interest', 'compound': 'compound interest', 'depreciation': 'falls by'}[p['kind']]]
        if p['kind'] != 'depreciation':
            need.append('interest is earned' if p['qty'] == 'interest' else 'is in the account')
        need.append('nearest penny') if p['kind'] != 'simple' else None
    for n in need:
        if n and n not in stem:
            errs.append('%s: the stem %r does not say %r' % (tag, stem[:70], n))
    # the worked lines
    w = q['worked']
    if len(w) < 2 or any(not l for l in w):
        errs.append('%s: fewer than two worked lines' % tag)
    text = ' '.join(w)
    written = money(int(ans['money'])) if 'money' in ans else '%s%%' % (ans['value'].numerator if ans['value'].denominator == 1 else float(ans['value']))
    if written not in text:
        errs.append('%s: the answer %s is not written out in the worked lines' % (tag, written))
    if (st == 5) != (q['calc'] == 'calculator'):
        errs.append('%s: calc field %r' % (tag, q['calc']))
    if st == 5 and q['friendly']:
        errs.append('%s: a stage 5 question marked friendly' % tag)
    if q['friendly'] != friendly_expected(q, ans):
        errs.append('%s: friendly is %s, recomputed %s' % (tag, q['friendly'], friendly_expected(q, ans)))
    return errs


# ---------------------------------------------------------------- the independent marker
JUNK = ['', 'abc', '12abc', '1,250', '--', '.']


def py_judge(q, key, raw):
    s = raw.strip()
    if s.startswith('£'):
        s = s[1:]
    if q['answer']['type'] == 'money':
        if not re.fullmatch(r'\d+(\.\d+)?|\.\d+', s):
            return 'unreadable'
        v = Fraction(s)
        if v * 100 != Fraction(str(key['pence'])):
            return 'wrong'
        whole = key['pence'] % 100 == 0
        return 'correct' if (re.fullmatch(r'\d+\.\d\d', s) or (whole and re.fullmatch(r'\d+', s))) else 'format'
    if not re.fullmatch(r'\d+(\.\d+)?|\.\d+', raw.strip()):
        return 'unreadable'
    return 'correct' if Fraction(raw.strip()) == Fraction(str(key['value'])) else 'wrong'


def py_mark(q, raw):
    r = py_judge(q, q['answer'], raw)
    if r == 'correct':
        return 'right'
    if r in ('format', 'unreadable'):
        return r
    for s in q['slips']:
        if py_judge(q, s['answer'], raw) == 'correct':
            return 'slip'
    return 'wrong'


def probes_for(q, rng):
    a = q['answer']
    out = list(JUNK)
    if a['type'] == 'money':
        p = a['pence']
        pounds = '%d.%02d' % (p // 100, p % 100)
        out += [pounds, '£' + pounds, pounds + '0', '%.1f' % (p / 100), '%d' % (p // 100), '%d.0' % (p // 100), '%d.%02d' % ((p + 1) // 100, (p + 1) % 100),
                '%d.%02d' % ((p - 1) // 100, (p - 1) % 100), '%d.%02d' % ((p + 10) // 100, (p + 10) % 100), '0.00', '%d' % (p // 100 + 1)]
        for s in q['slips']:
            sp = s['answer']['pence']
            out += ['%d.%02d' % (sp // 100, sp % 100), '%d' % (sp // 100)]
        for _ in range(4):
            sp = rng.randint(1, 3000000)
            out.append('%d.%02d' % (sp // 100, sp % 100))
    else:
        v = a['value']
        out += [str(v), '%s.0' % v, '%s.00' % v, str(v + 1), str(v - 1), '0', str(v) + '%']
        for s in q['slips']:
            out += [str(s['answer']['value'])]
        for _ in range(3):
            out.append(str(rng.randint(1, 99)))
    return list(dict.fromkeys(out))


GEN_JS = """(args) => {
  const G = MaffsPercentagesMoney, out = [];
  function rng(seed) { let s = seed >>> 0; return () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  for (let st = 1; st <= 5; st++) for (let sl = 0; sl < G.SLOTS; sl++) for (let seed = 1; seed <= args.seeds; seed++) out.push(G.question(st, sl, rng(seed * 7919 + st * 31 + sl)));
  const sessions = [];
  for (let st = 1; st <= 5; st++) for (let s = 1; s <= 30; s++) sessions.push({ stage: st, qs: IOS.session(st, s * 977 + 3).map(q => ({ slot: q.slot, stem: q.stem })) });
  const ex = [1, 2, 3, 4, 5].map(st => IOS.example(st).slot);
  return { qs: out, sessions, ex };
}"""
PROBE_JS = """(items) => items.map(([q, raw]) => IOS.mark(q, raw).kind)"""


# ---------------------------------------------------------------- the page and module under Playwright
def open_page(pw, base, html, module, size):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    ctx.route(lambda url: url.split('?')[0].endswith('/' + GEN_SRC), lambda route: route.fulfill(
        status=200, content_type='application/javascript; charset=utf-8', body=module))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
    page.wait_for_function('!!window.IOS && !!IOS.ui', timeout=10000)
    page.evaluate("""() => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); }; }""")
    return br, page, errors


def check_engine(page, out):
    data = page.evaluate(GEN_JS, {'seeds': SEEDS})
    info = {}
    rng = random.Random(11)
    qs = data['qs']
    stems = {}
    bad = 0
    for q in qs:
        stems.setdefault(q['stage'], set()).add(q['stem'])
        for e in check_question(q):
            bad += 1
            if bad <= 8:
                out.append(e)
    if bad > 8:
        out.append('... and %d more findings in the questions' % (bad - 8))
    for st in range(1, 6):
        info[st] = len(stems[st])
        if len(stems[st]) < 30:
            out.append('stage %d: only %d distinct questions over %d seeds a slot' % (st, len(stems[st]), SEEDS))
    for s in data['sessions']:
        sl = [q['slot'] for q in s['qs']]
        if len(sl) != 10 or sl != sorted(sl) or len(set(sl)) != 10 or 0 in sl or max(sl) > 11:
            out.append('stage %d session slots %s: want 10 distinct, ascending, within 1-11, never 0' % (s['stage'], sl))
            break
        if len({q['stem'] for q in s['qs']}) != 10:
            out.append('stage %d: a repeated question in one session' % s['stage'])
            break
    if data['ex'] != [0] * 5:
        out.append('the worked examples are not slot 0: %s' % data['ex'])
    # the marker
    items, want = [], []
    for q in qs[::3]:
        for raw in probes_for(q, rng):
            items.append([q, raw])
            want.append(py_mark(q, raw))
    got = page.evaluate(PROBE_JS, items)
    diffs = [(items[i][1], items[i][0]['stem'][:60], want[i], got[i]) for i in range(len(items)) if want[i] != got[i]]
    for raw, stem, w, g in diffs[:5]:
        out.append('mark(%r) for %r said %s; the independent marker says %s' % (raw, stem, g, w))
    if len(diffs) > 5:
        out.append('... and %d more marking differences' % (len(diffs) - 5))
    kinds = {}
    for k in want:
        kinds[k] = kinds.get(k, 0) + 1
    for need in ('right', 'format', 'unreadable', 'slip', 'wrong'):
        if not kinds.get(need):
            out.append('the probes never produced a %s verdict' % need)
    info['probes'] = len(items)
    return info


# ---------------------------------------------------------------- the page played
def typed(page, raw):
    page.evaluate("""(raw) => { const b = [...document.querySelectorAll('#ans, #ansc')].find(x => x.offsetParent); b.value = raw; }""", raw)
    page.evaluate("document.getElementById('checkBtn').click()")


def clean(t):
    return re.sub(r'\s+', ' ', t)


def play_stage(page, st, size, out, nq):
    w, h = size
    fold = h - 40
    where = '%dx%d stage %d' % (w, h, st)
    page.evaluate('window.__ev = []; window.__sub = []')
    page.evaluate('IOS.ui.start(%d, false)' % st)
    page.wait_for_timeout(150)
    ex = page.evaluate("IOS.example(%d)" % st)
    steps = 0
    while page.evaluate("document.getElementById('example').classList.contains('active')") and steps < 12:
        shown = page.evaluate("document.querySelectorAll('#exSteps li').length")
        if shown != steps + 1:
            out.append('%s: the worked example shows %d lines at step %d' % (where, shown, steps + 1))
        if page.evaluate("window.__ev.length") != 0:
            out.append('%s: the worked example logged an event: %s' % (where, page.evaluate('window.__ev')))
        page.evaluate("document.getElementById('exNext').click()")
        page.wait_for_timeout(60)
        steps += 1
    if steps != len(ex['worked']):
        out.append('%s: the worked example took %d presses for %d lines' % (where, steps, len(ex['worked'])))
    page.wait_for_function("IOS.ui.state() === 'asking'", timeout=8000)
    badge = page.evaluate("document.getElementById('calcBadge').textContent.trim()")
    want_badge = 'Calculator required' if st == 5 else 'Calculator optional'
    if badge != want_badge:
        out.append('%s: the header badge reads %r, not %r' % (where, badge, want_badge))
    if st == 5 and not page.evaluate('IOS.ui.calcMounted()'):
        out.append('%s: no calculator in stage 5' % where)
    if st != 5 and not page.evaluate('IOS.ui.calcOptionalMounted()'):
        out.append('%s: no calculator behind a toggle in an optional stage' % where)
    expect = 0
    marked = 0
    for qn in range(nq):
        page.wait_for_function("IOS.ui.state() === 'asking'", timeout=8000)
        page.wait_for_timeout(120)
        q = page.evaluate('IOS.ui.question()')
        info = page.evaluate("""() => { const vis = x => x && x.offsetParent;
            const els = [...document.querySelectorAll('#ansForm button, #ansForm input, #kpHolder button, .maffs-keypad button, #calcWrap button, #calcOpt .maffs-calc-toggle')].filter(vis).map(x => x.getBoundingClientRect());
            const note = document.getElementById('tryNote');
            return { last: Math.max(...els.map(x => x.bottom)), sw: document.documentElement.scrollWidth, iw: innerWidth, right: Math.max(...els.map(x => x.right)),
                     note: vis(note), tog: vis(document.querySelector('#calcOpt .maffs-calc-toggle')), togOpen: !!document.querySelector('#calcOpt .maffs-calc-toggle.open'),
                     pre: vis(document.getElementById('unitPre')), post: vis(document.getElementById('unitPost')) }; }""")
        if info['last'] > fold + 0.5:
            out.append('%s q%d: the answer box, Check or the keys end at %d, below the fold (%d)' % (where, qn, info['last'], fold))
        if info['sw'] > info['iw'] or info['right'] > info['iw'] + 0.5:
            out.append('%s q%d: sideways scroll or a control off the screen' % (where, qn))
        if bool(info['note']) != bool(q['friendly'] and q['calc'] == 'optional'):
            out.append('%s q%d: the "try without a calculator" note shows %s for friendly=%s' % (where, qn, info['note'], q['friendly']))
        if st != 5 and (not info['tog'] or info['togOpen']):
            out.append('%s q%d: the calculator toggle is %s in an optional stage' % (where, qn, 'open' if info['togOpen'] else 'not on the screen'))
        if st == 5 and info['tog']:
            out.append('%s q%d: the optional calculator shows in the required stage' % (where, qn))
        if bool(info['pre']) != (q['answer']['type'] == 'money') or bool(info['post']) != (q['answer']['type'] == 'percent'):
            out.append('%s q%d: the tag shows the wrong unit (£ %s, %% %s)' % (where, qn, info['pre'], info['post']))
        if st == 5 and qn == 0:                 # the calculator open: it and the answer box still above the fold
            if page.evaluate("!!(document.querySelector('.maffs-calc-toggle') && document.querySelector('.maffs-calc-toggle').offsetParent)"):
                page.evaluate("document.querySelector('.maffs-calc-toggle').click()")
                page.wait_for_timeout(250)
                m = page.evaluate("""() => { const e = [...document.querySelectorAll('#ansForm button, #ansForm input, #calcWrap button, .maffs-calc button, .maffs-keypad button')].filter(x => x.offsetParent).map(x => x.getBoundingClientRect());
                    return Math.max(...e.map(x => x.bottom)); }""")
                if m > fold + 0.5 and w <= 600:
                    out.append('%s: with the calculator open the keys end at %d, below the fold (%d)' % (where, m, fold))
                page.evaluate("document.querySelector('.maffs-calc-toggle').click()")
                page.wait_for_timeout(150)
        if st != 5 and qn == 0 and info['tog']:      # the toggle opens a working calculator: 12 x 379 / 100 = 45.48
            page.evaluate("document.querySelector('#calcOpt .maffs-calc-toggle').click()")
            page.wait_for_timeout(200)
            res = page.evaluate("""() => { const k = t => [...document.querySelectorAll('#calcOpt .maffs-calc-key')].find(x => x.textContent.trim() === t);
                for (const t of ['1','2','×','3','7','9','÷','1','0','0','=']) { const b = k(t); if (!b) return 'no key ' + t; b.click(); }
                return document.querySelector('#calcOpt .maffs-calc-result').textContent.trim(); }""")
            if res != '45.48':
                out.append('%s: the optional-stage calculator gave %r for 12 x 379 / 100, not 45.48' % (where, res))
            page.evaluate("document.querySelector('#calcOpt .maffs-calc-toggle').click()")
            page.wait_for_timeout(150)
        kind = 'right'
        if qn == 1:
            kind = 'format' if (q['answer']['type'] == 'money' and q['answer']['pence'] % 100 != 0 and q['answer']['pence'] % 10 == 0) else 'slip'
        if kind == 'slip' and not q['slips']:
            kind = 'wrong'
        if qn == 2:
            kind = 'wrong'
        note = None
        a = q['answer']
        right_raw = ('%d.%02d' % (a['pence'] // 100, a['pence'] % 100) if a['pence'] % 100 else str(a['pence'] // 100)) if a['type'] == 'money' else str(a['value'])
        if kind == 'format':
            typed(page, '%.1f' % (a['pence'] / 100))
            page.wait_for_timeout(150)
            if page.evaluate('IOS.ui.state()') != 'asking' or int(page.inner_text('#hudScore')) != expect or not page.inner_text('#msg').strip():
                out.append('%s q%d: a one-decimal money answer was marked, or gave no message' % (where, qn))
            kind = 'right'
        if kind == 'right':
            typed(page, right_raw)
        elif kind == 'slip':
            s = q['slips'][0]
            sa = s['answer']
            typed(page, ('%d.%02d' % (sa['pence'] // 100, sa['pence'] % 100)) if 'pence' in sa else str(sa['value']))
            note = clean(s['line'])[:24]
        else:
            typed(page, ('%d.%02d' % ((a['pence'] + 7) // 100, (a['pence'] + 7) % 100)) if a['type'] == 'money' else str(a['value'] + 7))
        # a wrong typed value must not coincide with a slip: if it does, the verdict is a slip, still not right
        page.wait_for_timeout(200)
        ok = kind == 'right'
        marked += 1
        if ok:
            expect += 1
        if int(page.inner_text('#hudScore')) != expect:
            out.append('%s q%d: score shows %s, expected %d' % (where, qn, page.inner_text('#hudScore'), expect))
        fb = page.evaluate("""() => { const n = document.querySelector('.maffs-next, #nextBtn'), l = document.querySelector('.fb-line');
            return { next: n ? n.getBoundingClientRect().bottom : null, line: l ? l.textContent : '', right: !!document.querySelector('.fb.done'), panel: document.querySelector('.fb') ? document.querySelector('.fb').textContent : '' }; }""")
        if fb['next'] is None or fb['next'] > fold + 0.5:
            out.append('%s q%d (%s): Next is %s, below the fold (%d)' % (where, qn, kind, fb['next'], fold))
        if fb['right'] != ok:
            out.append('%s q%d (%s): the feedback says %s' % (where, qn, kind, 'right' if fb['right'] else 'not right'))
        if note and note not in clean(fb['panel']):
            out.append('%s q%d: the feedback does not carry the slip line %r' % (where, qn, note))
        if not ok and 'How it goes' not in fb['panel']:
            out.append('%s q%d: a wrong answer showed no worked lines' % (where, qn))
        if ok:
            page.evaluate("document.getElementById('nextBtn').click()")
        else:
            page.evaluate("document.querySelector('.maffs-next').click()")
        page.wait_for_timeout(100)
    if nq == 10:
        page.wait_for_function("document.getElementById('results').classList.contains('active')", timeout=8000)
        sub = page.evaluate('window.__sub')
        comp = [p for n, p in page.evaluate('window.__ev') if n == 'game_completed']
        if len(sub) != 1 or sub[0][0] != SLUG or sub[0][1] != BOARD[st] or sub[0][2] != expect or sub[0][3] != marked:
            out.append('%s: the leaderboard got %s, the score was %d of %d answers on %s' % (where, sub, expect, marked, BOARD[st]))
        if len(comp) != 1 or comp[0].get('score') != expect or comp[0].get('level') != 'gcse' or comp[0].get('mode') != BOARD[st]:
            out.append('%s: game_completed says %s, the score was %d' % (where, comp, expect))
        if int(page.inner_text('#resScore')) != expect:
            out.append('%s: the results screen shows %s, not %d' % (where, page.inner_text('#resScore'), expect))
        nxt = page.evaluate("(() => { const b = document.getElementById('nextStageBtn'); return b.offsetParent ? b.textContent.trim() : null; })()")
        if (st < 5 and nxt != 'Next: Stage %d' % (st + 1)) or (st == 5 and nxt):
            out.append('%s: the "next stage" button reads %r' % (where, nxt))
        allowed = {'game_slug', 'level', 'mode', 'question_index', 'correct'}
        for n, p in page.evaluate('window.__ev'):
            if n == 'question_answered' and set(p) - allowed:
                out.append('question_answered carries a field outside the existing events: %s' % sorted(set(p) - allowed))
                break
        page.evaluate("document.getElementById('menuBtn').click()")


def size_unit(size):
    return '%s %dx%d' % ('full' if size in FULL else 'first', size[0], size[1])


def check_pages(base, html, module, sizes, out, stages=range(1, 6), unit=None):
    from playwright.sync_api import sync_playwright
    unit = unit or (lambda uid: contextlib.nullcontext())
    with sync_playwright() as pw:
        for size in sizes:
            with unit(size_unit(size)):
                br, page, errs = open_page(pw, base, html, module, size)
                try:
                    for st in stages:
                        play_stage(page, st, size, out, 10 if size in FULL else 3)
                except Exception as e:  # noqa: BLE001
                    out.append('play at %dx%d threw: %s' % (size[0], size[1], str(e).splitlines()[0][:220]))
                out.extend('page error at %dx%d: %s' % (size[0], size[1], e) for e in errs if 'production host' not in e)
                br.close()


def check(html, module, out, engine=True, sizes=(), stages=range(1, 6), shard=None):
    """shard: time each piece as its work unit ("engine", "full 390x844", "first WxH"); the self-test passes none."""
    from playwright.sync_api import sync_playwright
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    proc, base = bc.start_stub_server()
    info = {}
    try:
        if engine:
            with unit('engine'), sync_playwright() as pw:
                br, page, errs = open_page(pw, base, html, module, (1280, 800))
                try:
                    info.update(check_engine(page, out))
                except Exception as e:  # noqa: BLE001
                    out.append('the engine checks threw: %s' % str(e).splitlines()[0][:200])
                out.extend('page error: ' + e for e in errs)
                br.close()
        if sizes:
            check_pages(base, html, module, sizes, out, stages, unit=unit)
    finally:
        proc.terminate()
    return info


# Each plant: (what, file ('module' or 'page'), [(old, new)], kind ('engine' or 'play'), pattern its finding must match).
PLANTS = [
    ('a wrong new price (a reduction worked as a rise)', 'module',
     [("var N = dec_ ? B - m.x : B + m.x;", "var N = B + m.x;")], 'engine', r'(answer .* but the params give|mark\(\))'),
    ('a reverse percentage worked the wrong way round (a reduction treated as a rise)', 'module',
     [("k = dec_ ? 100 - p : 100 + p, N = O / 100 * k", "k = 100 + p, N = O / 100 * k")], 'engine', r'(answer .* but the params give|does not say|mark\(\))'),
    ('a format answer marked right (one decimal accepted)', 'page',
     [("if (r === 'format') return { kind: 'format', msg: MaffsAnswer.message('format', raw, { currency: '£' }) };", "if (r === 'format') return { kind: 'right' };")], 'engine', r'mark\(.*said right'),
    ('a slip with the value of the answer (a compound answer for simple interest)', 'module',
     [("var wrong = qty === 'interest' ? cv - P : cv;\n      if (wrong !== key) slips.push", "var wrong = key;\n      if (true) slips.push")], 'engine', r'(has the value of the answer|is .* but the params give)'),
    ('the worked example dealt among the questions (slot 0 included)', 'page',
     [("for (i = 1; i < G.SLOTS; i++) slots.push(i);", "for (i = 0; i < G.SLOTS; i++) slots.push(i);")], 'engine', r'session slots'),
    ('a wrong answer scoring (the page)', 'page',
     [("marked++; if (ok) { rightCount++; score++; }", "marked++; score++; if (ok) { rightCount++; }")], 'play', r'(score shows|the leaderboard got|game_completed says)'),
    ('the friendly rule loosened (20% counted as an easy step)', 'module',
     [("var EASY_PCT = [10, 25, 50];", "var EASY_PCT = [10, 20, 25, 50];")], 'engine', r'friendly is'),
    ('no calculator offered in an optional stage (the toggle hidden)', 'page',
     [("$('calcOptWrap').hidden = on;", "$('calcOptWrap').hidden = true;")], 'play', r'toggle'),
    ('the calculator note on every item (not only the friendly ones)', 'page',
     [("$('tryNote').hidden = !(Q.calc === 'optional' && Q.friendly);", "$('tryNote').hidden = !(Q.calc === 'optional');")], 'play', r'note shows'),
]


# Each plant is a work unit of its own (contract SHARD), dealt into CI parts by its time.
def selftest(html, module, plants=None, shard=None):
    ok = True
    for what, which, edits, kind, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            ok = plant_one(html, module, what, which, edits, kind, want) and ok
    return ok


def plant_one(html, module, what, which, edits, kind, want):
    src = module if which == 'module' else html
    for old, new in edits:
        if src.count(old) != 1:
            print('  self-test %-84s *** CANNOT PLANT ***' % what)
            return False
        src = src.replace(old, new)
    got = []
    h2, m2 = (html, src) if which == 'module' else (src, module)
    check(h2, m2, got, engine=kind == 'engine', sizes=[(390, 844)] if kind == 'play' else [], stages=(1, 3))
    hit = [g for g in got if re.search(want, g)]
    print('  self-test %-84s %s' % (what, ('caught: ' + hit[0][:80]) if hit else '*** MISSED ***' + (' (other: %s)' % got[0][:80] if got else '')))
    return bool(hit)


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    mine = shard.pick(['engine'] + [size_unit(size) for size in SIZES] + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    module = open(MODULE, encoding='utf-8').read()
    out = []
    sizes = [size for size in SIZES if size_unit(size) in mine]
    info = {}
    if 'engine' in mine or sizes:
        info = check(html, module, out, engine='engine' in mine, sizes=sizes, shard=shard)
    if info:
        print('%s: distinct questions a stage over %d seeds a slot: %s; probe answers marked both ways: %s' % (
            SLUG, SEEDS, {k: v for k, v in info.items() if isinstance(k, int)}, info.get('probes')))
    if sizes:
        print('%s: every stage played at %s' % (SLUG, ', '.join('%dx%d' % s for s in sizes)))
    ok = selftest(html, module, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
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
