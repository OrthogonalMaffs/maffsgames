#!/usr/bin/env python3
# ci-line: E2 | Terrible Advice (every equation in the advice and the keys recomputed; every key recomputed from its own givens; no distractor ends on the key's value (SR-16); answer once and Next once, played in Chromium) |
# ci-deps: scripts/verify-spot-the-muppet.py
"""Terrible Advice: the maths every item shows, recomputed; one mark per question; Next once.

The same format as Spot the Muppet (a character's advice, four options, one keyed correct, two picks a question), with
its own bank and engine: a point for a right first pick only. The arithmetic, key and SR-16 checks are Spot the Muppet's
(scripts/verify-spot-the-muppet.py: equations(), numbers(), same()), applied to this bank:

  Bank: 18 KS3, 20 GCSE, 12 Core items; ids unique; four distinct options, exactly one keyed correct.
  Arithmetic: every equation chain in the advice and the key holds (a muppet's deliberate wrong sum is in MUPPET_SUMS;
    terrible-advice-t2-006: the key's £500 × 1.1249 = £562.43; t2-009: the advice's 1.05 × 20 = 21.05).
  Keys: every item in KEYS (recomputed) or CONCEPT (reviewed); the key states each value.
  SR-16: no distractor ends on the key's value; named true options (TRUE_OPTIONS) are gone (t2-001: gcse_006's
    second "Prudence is correct"; t2-003: core_007's "Wendy is correct — 70%", the weighted mean being 70% too;
    t2-010: core_004's simple-interest figure offered as a correction). The key states no false rule (t2-008).
  Arguments: core_002's argument must be invalid (t2-002, the valid marginal argument).
  The loan (Jon, 8 Oct 2026; t2-005): Spot the Muppet's LOAN check: the advice says APR; the key states the monthly
    rate, the payment and the total to the penny (a repayment loan, APR the effective annual rate); the distractors are
    the muppet's £333.33 and the two old keys (compound and simple interest on the whole sum), each with its method.
  Jokes: core_003 no longer prescribes televisions to patients (t2-007, SR-14 tier (c)).
  Chromium: every item played three ways: the key first (scores 1, logged once); a wrong pick then the key (the first
    pick marks nothing; scores 0, logged once, attempts 2); two wrong picks (scores 0, logged once; then every option
    clicked and pressed with Enter changes nothing). With MaffsLock's real fresh window (t2-004): Next's second click
    landing on the new question's option marks nothing; a double click on Next moves on once; the session ends once.
KNOWN_OPEN: register entries detected here and left open (reported, never failed; a stale one fails).
A self-test plants nine faults back into a copy of the page; each must FAIL naming its entry.

    python scripts/verify-terrible-advice.py [--no-selftest] [--against FILE]
"""
import argparse
import importlib.util
import math
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

_spec = importlib.util.spec_from_file_location('stm', os.path.join(HERE, 'verify-spot-the-muppet.py'))
stm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stm)

SLUG = 'terrible-advice'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'ks3': 18, 'gcse': 20, 'core': 12}
TAG = 'terrible-advice-'

KEYS = {
    'ta_ks3_001': (F(30, 100) * 80,),
    'ta_ks3_002': (F(60, 5) * 2, F(60, 5) * 3),
    'ta_ks3_003': (F(1, 2) + F(1, 3),),
    'ta_ks3_004': (F(400) * F(11, 10) * F(9, 10),),
    'ta_ks3_005': (F(3 + 7 + 8 + 2 + 10, 5),),
    'ta_ks3_006': (F(300, 4) * 7,),
    'ta_ks3_007': (F(1, 2) * 8 * 5,),
    'ta_ks3_008': ((1 - F(8, 10) * F(7, 10)) * 100,),
    'ta_ks3_009': (F(16 * 2),),
    'ta_ks3_010': (F(3, 4) * 48,),
    'ta_ks3_011': (F(3 * 25000, 100),),
    'ta_ks3_012': (F(180 - 80 - 60),),
    'ta_ks3_013': (F(24 * 15),),
    'ta_ks3_015': (F(2 * (9 + 4)),),
    'ta_ks3_016': (F(350, 7) * 2, F(350, 7) * 5),
    'ta_ks3_018': (F(3), F(7)),
    'ta_gcse_001': (F(85) / F(85, 100),),
    'ta_gcse_002': (F(500) * F(104, 100) ** 3,),
    'ta_gcse_003': (F(3), F(4)),
    'ta_gcse_004': (F(50, 200) * 100,),
    'ta_gcse_005': (1 - F(5, 6) ** 6,),
    'ta_gcse_006': (F(240, 100) + F(5, 100),),
    'ta_gcse_007': (F(5), F(-5)),
    'ta_gcse_008': (F(480, 400), F(715, 650)),             # pence per gram, 400 g and 650 g
    'ta_gcse_010': (F(5),),
    'ta_gcse_011': (math.pi * 5 ** 2,),
    'ta_gcse_012': (F(7 - 3, 6 - 2),),
    'ta_gcse_014': (math.degrees(math.asin(0.6)),),
    'ta_gcse_017': (F(10),),                               # sqrt(6^2 + 8^2)
    'ta_gcse_018': (F(1, 2) * F(1, 6),),
    'ta_gcse_020': (F(3), F(7, 2)),                        # 3x + 2y = 16, x + 2y = 10
    'ta_core_001': (F(10) * F(1, 10) - 2,),
    'ta_core_002': (F(350, 500), F(480, 750)),
    'ta_core_004': (1000 * 1.05 ** 20,),
    'ta_core_005': (F(40), F(60)),
    'ta_core_006': (F(150, 120) * 100,),
    'ta_core_007': (F(60 * 10 + 70 * 30 + 80 * 10, 50),),
    'ta_core_008': (F(360) / F(120, 100),),
    'ta_core_009': (F(2000, 15 - 5),),
    'ta_core_012': (stm.amortised(12000, 0.06, 36),),
}

CONCEPT = {
    'ta_ks3_014': 'independent flips: P(tails) stays 0.5',
    'ta_ks3_017': '3,400,000 = 3.4 x 10^6',
    'ta_gcse_009': 'x^3 x x^4 = x^7',
    'ta_gcse_013': 'x^2 + 5x + 6 = (x + 2)(x + 3)',
    'ta_gcse_015': '(x + 3)^2 = x^2 + 6x + 9',
    'ta_gcse_016': '5, 8, 11, 14: nth term 3n + 2',
    'ta_gcse_019': '0.00057 = 5.7 x 10^-4',
    'ta_core_003': 'TVs and life expectancy: wealth drives both',
    'ta_core_010': 'a least-squares line passes through the mean point',
    'ta_core_011': 'bias towards heads is a one-tailed test',
}

MUPPET_SUMS = {
    ('ta_ks3_003', '½ + ⅓ = ⅖'): 'adds the tops and the bottoms',
}

# An option that is true as written must not be keyed wrong: each named here was, and is gone.
TRUE_OPTIONS = {
    'ta_gcse_006': ('Prudence is correct — upper bound is 2.45m', TAG + 't2-001'),
    'ta_core_007': ('Wendy is correct — the overall average is 70%', TAG + 't2-003'),
    'ta_core_004': ('Penny is wrong — £1,000 × 5% × 20 = £1,000 (simple interest, the original amount doubles)', TAG + 't2-010'),
}
# A key must not state a false rule.
FALSE_RULES = {'ta_gcse_007': ('always have a positive and negative solution', TAG + 't2-008')}
# A distractor that ends on the key's values but is false as a whole (reviewed): it is not SR-16's shape.
SR16_REVIEWED = {'ta_gcse_008': 'quotes the right unit prices (1.2p/g, 1.1p/g) with the wrong conclusion (the 400g)'}
ARITH_ENTRY = {'ta_gcse_002': TAG + 't2-006', 'ta_core_004': TAG + 't2-009'}

KNOWN_OPEN = {}

# The loan (Jon, 8 Oct 2026; terrible-advice-t2-005): Spot the Muppet's check (stm.check_loan), on this bank's item.
LOAN = {'ta_core_012': (12000, 0.06, 36, TAG + 't2-005')}


def check_bank(fails, opens, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s' % (counts, COUNTS))
    items = [q for lv in COUNTS for q in bank.get(lv, [])]
    ids = [q['id'] for q in items]
    if len(set(ids)) != len(ids):
        fails.append('bank: duplicate ids')
    seen_sums, open_seen = set(), set()
    for q in items:
        qid, opts = q['id'], q['options']
        keys = [o for o in opts if o['correct']]
        if len(opts) != 4 or len(keys) != 1 or len({o['text'] for o in opts}) != 4:
            fails.append('%s: %d options, %d keyed correct, %d distinct (4, 1, 4)' % (qid, len(opts), len(keys), len({o['text'] for o in opts})))
            continue
        key = keys[0]['text']
        for where, text in (('advice', q['advice']), ('key', key)):
            for written, vals in stm.equations(text, q['advice']):
                for a, b in zip(vals, vals[1:]):
                    if a is None or b is None or stm.holds(a, b):
                        continue
                    if where == 'advice' and (qid, written) in MUPPET_SUMS:
                        seen_sums.add((qid, written))
                        continue
                    tag = ARITH_ENTRY.get(qid, '')
                    fails.append('%s%s: the %s says "%s", which does not hold (%s vs %s)'
                                 % (tag + ' ' if tag else '', qid, where, written, round(float(a[0]), 4), round(float(b[0]), 4)))
        if qid in KEYS:
            want = KEYS[qid]
            got = stm.numbers(key)
            missing = [w for w in want if not any(stm.same(g, w) for g in got)]
            written = [next((g[0] for g in got if stm.same(g, w)), None) for w in want]
            if missing:
                if qid in KNOWN_OPEN:
                    open_seen.add(qid)
                    opens.append('%s %s: %s' % (KNOWN_OPEN[qid][0], qid, KNOWN_OPEN[qid][1]))
                else:
                    fails.append('%s: the key does not state %s (recomputed from the item): "%s"'
                                 % (qid, ', '.join(str(round(float(w), 4)) for w in missing), key))
            for o in opts:
                if o['correct']:
                    continue
                tail = stm.numbers(o['text'])[-len(want):]
                if qid in SR16_REVIEWED:
                    continue
                if None not in written and len(tail) == len(want) and all(g[0] == w for g, w in zip(tail, written)):
                    fails.append('SR-16 %s: the distractor "%s" ends on the key\'s value, by a wrong method; a true '
                                 'statement is never a wrong option' % (qid, o['text']))
        elif qid not in CONCEPT:
            fails.append('%s: in neither KEYS nor CONCEPT: recompute its answer, or review it and give the reason' % qid)
        if qid in TRUE_OPTIONS:
            text, tag = TRUE_OPTIONS[qid]
            if any(o['text'] == text and not o['correct'] for o in opts):
                fails.append('%s %s: "%s" is true as written and keyed wrong (SR-16)' % (tag, qid, text))
        if qid in FALSE_RULES and FALSE_RULES[qid][0] in key:
            fails.append('%s %s: the key states a false rule ("...%s")' % (FALSE_RULES[qid][1], qid, FALSE_RULES[qid][0]))
        for o in opts:
            if not o['correct'] and re.search(r' is correct \u2014', o['text']):
                adv = stm.numbers(q['advice'])
                for g in stm.numbers(o['text']):
                    if not any(stm.same(a, g[0]) and a[1] == g[1] for a in adv):
                        fails.append('%s: "%s" states %s, which the advice never says' % (qid, o['text'], float(g[0])))
    for q in items:
        if q['id'] in LOAN:
            stm.check_loan(fails, q, *LOAN[q['id']])
        # core_003 (Jon, 8 Oct 2026; terrible-advice-t2-007, SR-14 tier (c)): the joke is a bigger telly, not patients
        if q['id'] == 'ta_core_003' and re.search(r'patient|prescrib', q['advice'], re.I):
            fails.append('%s ta_core_003: the advice still prescribes televisions to patients (SR-14 tier (c)): "%s"'
                         % (TAG + 't2-007', q['advice']))
    for q in items:
        if q['id'] != 'ta_core_002':
            continue
        extra = re.search(r'£([\d.]+) for (\d+)ml extra', q['advice'])
        small = re.search(r'paying £([\d.]+) for (\d+)ml', q['advice'])
        if extra and small and F(extra.group(1)) / int(extra.group(2)) < F(small.group(1)) / int(small.group(2)):
            fails.append('%s %s: the advice compares the extra %sml\'s price per ml with the small bottle\'s: a valid '
                         'marginal argument, which the key calls the wrong method' % (TAG + 't2-002', q['id'], extra.group(2)))
    for k in set(MUPPET_SUMS) - seen_sums:
        fails.append('MUPPET_SUMS %s "%s" is stale: no such wrong sum in the advice' % k)
    for qid in set(KNOWN_OPEN) - open_seen:
        fails.append('KNOWN_OPEN %s (%s) no longer reproduces: close it in the register and remove it here' % (qid, KNOWN_OPEN[qid][0]))


LOAD = """([lv, ids]) => {
  window.__ev.length = 0;
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById('startScreen').classList.add('active');
  currentLevel = lv; sessionLength = ids.length;
  startGame();
  sessionQuestions = ids.map(id => QUESTIONS[lv].find(q => q.id === id));
  currentIndex = 0; score = 0;
  showQuestion();
  window.__ev.length = 0;
}"""

STATE = stm.STATE
PICK = stm.PICK
AGAIN = stm.AGAIN


def sweep(fails, page, bank):
    for lv in COUNTS:
        for q in bank[lv]:
            qid = q['id']
            other = next(x['id'] for x in bank[lv] if x['id'] != qid)
            page.evaluate(LOAD, [lv, [qid, other]])
            page.evaluate(PICK, True)
            s = page.evaluate(STATE)
            if s['score'] != 1 or len(s['qa']) != 1 or not s['qa'][0]['correct'] or s['qa'][0].get('attempts') != 1:
                fails.append('%s: its key, picked first: score %d, logged %s (1; once, correct, attempts 1)' % (qid, s['score'], s['qa']))
            page.evaluate(LOAD, [lv, [qid, other]])
            page.evaluate(PICK, False)
            s = page.evaluate(STATE)
            if s['score'] != 0 or s['qa'] or s['open'] != 3:
                fails.append('answer once %s: a first wrong pick (a retry) logged %s, score %d, %d options left (nothing, 0, 3)'
                             % (qid, s['qa'], s['score'], s['open']))
            page.evaluate(PICK, True)
            s = page.evaluate(STATE)
            if s['score'] != 0 or len(s['qa']) != 1 or not s['qa'][0]['correct'] or s['qa'][0].get('attempts') != 2:
                fails.append('%s: a wrong pick then its key: score %d, logged %s (0, a point for a right first pick only; '
                             'once, correct, attempts 2)' % (qid, s['score'], s['qa']))
            page.evaluate(LOAD, [lv, [qid, other]])
            page.evaluate(PICK, False)
            page.evaluate(PICK, False)
            s0 = page.evaluate(STATE)
            if s0['score'] != 0 or len(s0['qa']) != 1 or s0['qa'][0]['correct'] or s0['open']:
                fails.append('%s: two wrong picks: score %d, logged %s, %d options open (0; once, wrong; none)'
                             % (qid, s0['score'], s0['qa'], s0['open']))
            page.evaluate(AGAIN)
            s1 = page.evaluate(STATE)
            if (s1['score'], len(s1['qa']), s1['done']) != (s0['score'], len(s0['qa']), s0['done']):
                fails.append('%s %s: clicking and pressing Enter on the marked question\'s options changed score %d -> %d, '
                             'question_answered %d -> %d' % (TAG + 't2-004', qid, s0['score'], s1['score'], len(s0['qa']), len(s1['qa'])))


def lock_window(fails, page, bank):
    tag = TAG + 't2-004'
    gcse = [q['id'] for q in bank['gcse']]
    page.evaluate(LOAD, ['gcse', gcse[:3]])
    page.wait_for_timeout(350)
    page.evaluate(PICK, True)
    stm.next_shown(page)
    before = page.evaluate(STATE)
    page.evaluate("() => { document.getElementById('nextBtn').click(); document.querySelector('#optionsGrid .option-card').click(); }")
    after = page.evaluate(STATE)
    if after['idx'] != 1 or after['marked'] or len(after['qa']) != len(before['qa']) or after['open'] != 4:
        fails.append('%s: the second click of a double click on Next, landing on the new question\'s option, %s'
                     % (tag, 'answered it unseen' if len(after['qa']) > len(before['qa']) else 'spent a pick (%d of 4 open)' % after['open']))
    page.evaluate(LOAD, ['gcse', gcse[:3]])
    page.wait_for_timeout(350)
    page.evaluate(PICK, True)
    stm.next_shown(page)
    page.dblclick('#nextBtn')
    page.wait_for_timeout(100)
    s = page.evaluate(STATE)
    if s['idx'] != 1 or s['marked']:
        fails.append('%s: a double click on Next moved %d questions and marked %d options (1, 0)' % (tag, s['idx'], s['marked']))
    page.evaluate(LOAD, ['gcse', gcse[:1]])
    page.wait_for_timeout(350)
    page.evaluate(PICK, True)
    stm.next_shown(page)
    page.evaluate("() => { const b = document.getElementById('nextBtn'); b.click(); b.click(); advanceQuestion(); }")
    s = page.evaluate(STATE)
    if s['done'] != 1:
        fails.append('the session ended %d times (once: game_completed and submitScore)' % s['done'])


def new_page(browser, base, html, fresh_zero):
    ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
    ctx.add_init_script(stm.INIT)
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
    page.wait_for_function("typeof QUESTIONS !== 'undefined' && typeof startGame === 'function'", timeout=8000)
    return ctx, page, errors


def run(html):
    from playwright.sync_api import sync_playwright
    fails, opens = [], []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx, page, errors = new_page(browser, base, html, True)
            bank = page.evaluate('() => QUESTIONS')
            check_bank(fails, opens, bank)
            sweep(fails, page, bank)
            ctx.close()
            ctx, page, errors2 = new_page(browser, base, html, False)
            lock_window(fails, page, bank)
            ctx.close()
            errs = [e for e in errors + errors2 if 'firebase' not in e.lower()]
            if errs:
                fails.append('page errors: %s' % '; '.join(errs[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return fails, opens, bank


D = '\\u2014'
PLANTS = [
    (TAG + 't2-004', 't2-004: no fresh window on a new question',
     "  MaffsLock.fresh(document.getElementById('gameScreen'));\n", ''),
    (TAG + 't2-001', "t2-001: gcse_006's second true option",
     "{text:'Prudence is wrong " + D + " upper bound is 2.49m',correct:false}",
     "{text:'Prudence is correct " + D + " upper bound is 2.45m',correct:false}"),
    (TAG + 't2-002', 't2-002: core_002 a valid marginal argument',
     'The big one only costs \\u00a31.30 more, and \\u00a31.30 is less than \\u00a33.50, so obviously the big bottle is better value.',
     'The difference in price is \\u00a31.30 for 250ml extra. That\\\'s better than paying \\u00a33.50 for 500ml so obviously the big bottle is better value.'),
    (TAG + 't2-003', "t2-003: core_007's 'Wendy is correct — 70%'",
     "{text:'Wendy is correct in both method and answer',correct:false}",
     "{text:'Wendy is correct " + D + " the overall average is 70%',correct:false}"),
    (TAG + 't2-006', 't2-006: gcse_002 500 x 1.1249 = 562.43',
     '\\u00a3500 \\u00d7 1.124864 = \\u00a3562.43', '\\u00a3500 \\u00d7 1.1249 = \\u00a3562.43'),
    (TAG + 't2-009', 't2-009: core_004 1.05 x 20 = 21.05',
     '\\u00d7 1.05 \\u00d7 20 = \\u00a31,000 \\u00d7 21 = \\u00a321,000.', '\\u00d7 1.05 \\u00d7 20 = \\u00a31,000 \\u00d7 21.05 = \\u00a321,050.'),
    (TAG + 't2-005', 't2-005: core_012 the key gives about £397 a month',
     '\\u2248 \\u00a3364.20 a month (total \\u00a313,111.19)', '\\u2248 \\u00a3397 a month (total \\u00a314,292.19)'),
    (TAG + 't2-005', "t2-005: core_012's advice says 6% per year",
     'over 3 years at 6% APR.', 'over 3 years at 6% per year.'),
    (TAG + 't2-007', 't2-007: core_003 prescribing televisions',
     "I\\'m telling everyone I know to buy a bigger telly.", "I\\'m prescribing televisions to all my patients."),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, opens, bank = run(html)
    print('%s: %d items: every equation in the advice and the keys, every key recomputed, no true option keyed wrong; '
          'each item played three ways in Chromium; Next and the fresh window' % (SLUG, sum(len(bank.get(lv, [])) for lv in COUNTS)))
    for o in opens:
        print('open  ' + o)
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            hit = [f for f in run(html.replace(old, new))[0] if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
