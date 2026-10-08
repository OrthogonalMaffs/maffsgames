#!/usr/bin/env python3
# ci-line: E | Word Problem Decoder (one category scheme, SR-18: every phrase marked right under exactly the topics that fit it, played in Chromium; answer once) |
"""Word Problem Decoder: each highlighted phrase is right under exactly the topics that fit it; answer once.

A student reads a word problem with one phrase highlighted (or two or three, one at a time) and picks the maths topic
it signals from four options. Jon's ruling (SR-18, 6 Oct 2026): one category scheme, both accepted where both fit.

  Bank: 50 KS3 and 60 GCSE items; every phrase is in its item's text; every topic (and every `also` topic) is one the
    level offers, and no phrase lists a topic twice.
  The scheme (PARENT_TOPIC, reviewed): a Reverse Percentage phrase is a Percentages phrase, a Standard Form phrase is a
    Number & Place Value phrase. The KS3 bank, which offers neither kind, keys those shapes under the parent
    (ks3_013, ks3_015, ks3_023); so a GCSE phrase keyed the kind is right under the parent too
    (word-problem-decoder-t1-003, t1-004).
  ACCEPT (reviewed, 8 Oct 2026): every phrase with a second topic that genuinely fits, with its reason. Every other
    phrase fits its keyed topic only.
  Chromium: every phrase played with each topic it accepts on the buttons, and with three that it does not: the page
    marks each accepted topic right and each other one wrong (so the marking is tested, whatever the page's code).
    After a mark, every option clicked again and pressed with Enter changes nothing (word-problem-decoder-t1-005: a
    second Enter credited the next phrase unseen); the session ends once.
A self-test plants three faults back into a copy of the page (no lock; the scheme off; gcse_017's second topic off);
each must FAIL naming its entry.

    python scripts/verify-word-problem-decoder.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'word-problem-decoder'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'ks3': 50, 'gcse': 60}
TAG = 'word-problem-decoder-'
PCT, NPV, RP = 'Percentages', 'Number & Place Value', 'Ratio & Proportion'
EQ, SIM = 'Algebra — Equations & Inequalities', 'Algebra — Simultaneous Equations'

PARENT_TOPIC = {'Reverse Percentage': PCT, 'Standard Form': NPV}

# (item id, phrase index) -> ({every topic it accepts}, the register entry, the reason). Reviewed 8 Oct 2026.
ACCEPT = {
    ('wpd_ks3_006', 1): ({NPV, RP}, 't1-001', '£2.50 per 100g is a unit rate'),
    ('wpd_ks3_022', 0): ({'Fractions', RP}, 't1-010', 'scaling a recipe from 12 to 20 biscuits is proportion'),
    ('wpd_ks3_046', 0): ({'Geometry — Angles', 'Algebra — Forming Expressions'}, 't1-010',
                         'the angles are x, 2x and x + 30: forming expressions is a main step'),
    ('wpd_gcse_013', 0): ({'Surds & Bounds', 'Geometry — Pythagoras & Trigonometry'}, 't1-010',
                          'the hypotenuse is found by Pythagoras, then simplified as a surd'),
    ('wpd_gcse_017', 0): ({EQ, SIM}, 't1-002', 'two unknowns and two conditions (gcse_021 keys the same shape Simultaneous)'),
    ('wpd_gcse_022', 0): ({SIM, EQ}, 't1-010', '"twice as fast" gives y = 2x, so one unknown is enough'),
    ('wpd_gcse_039', 0): ({'Geometry — Similarity & Congruence', RP}, 't1-010',
                          'a scale of 1:200 is a ratio (ks3_003 keys a map scale Ratio & Proportion)'),
    ('wpd_gcse_060', 1): ({EQ, RP}, 't1-010', 'the average speed is distance ÷ time, a compound measure'),
}
for _n in range(1, 6):
    ACCEPT[('wpd_gcse_%03d' % _n, 0)] = ({'Reverse Percentage', PCT}, 't1-003', 'a reverse percentage is a percentage problem')
for _n in range(6, 10):
    ACCEPT[('wpd_gcse_%03d' % _n, 0)] = ({'Standard Form', NPV}, 't1-004', 'standard form is number and place value')

# The KS3 phrases that key the scheme's kinds under the parent (the kind is not a KS3 topic).
KS3_PARENT = {('wpd_ks3_013', 0): PCT, ('wpd_ks3_015', 0): PCT, ('wpd_ks3_023', 0): NPV}


def check_bank(fails, data):
    bank, ks3, gcse = data['bank'], set(data['ks3']), set(data['ks3']) | set(data['gcse'])
    counts = {lv: sum(1 for q in bank if q['level'] == lv) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s' % (counts, COUNTS))
    ids = [q['id'] for q in bank]
    if len(set(ids)) != len(ids):
        fails.append('bank: duplicate ids')
    seen = set()
    for q in bank:
        offered = ks3 if q['level'] == 'ks3' else gcse
        for i, h in enumerate(q['highlights']):
            key = (q['id'], i)
            seen.add(key)
            if h['phrase'] not in q['text']:
                fails.append('%s phrase %d: "%s" is not in the text' % (q['id'], i + 1, h['phrase']))
            topics = [h['topic']] + list(h.get('also') or [])
            if len(set(topics)) != len(topics) or not set(topics) <= offered:
                fails.append('%s phrase %d: topics %s (each once, each one the %s level offers)' % (q['id'], i + 1, topics, q['level']))
            if key in KS3_PARENT and h['topic'] != KS3_PARENT[key]:
                fails.append('%s: keyed %s; the scheme files this shape under %s at KS3' % (q['id'], h['topic'], KS3_PARENT[key]))
    for key in set(ACCEPT) - seen:
        fails.append('ACCEPT %s phrase %d: no such phrase (re-review the table)' % (key[0], key[1] + 1))


INIT = r"""(() => {
  try { localStorage.clear(); } catch (e) {}
  // The sweep renders each phrase itself: the game's own advance timers never run (they would move it on mid-test).
  window.setTimeout = function () { return 0; };
  window.__ev = [];
  let inner;
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (e, p) { window.__ev.push([e, p]); return inner && inner.apply(this, arguments); }; },
    set(v) { inner = v; } });
})();"""

DATA = """() => ({bank: QUESTIONS, ks3: KS3_TOPICS, gcse: GCSE_EXTRA_TOPICS})"""

# Render one phrase with the given topics on the buttons (getDistractors is the game's own; replaced for the test).
SHOW = """([id, k, opts]) => {
  window.__ev.length = 0;
  const q = QUESTIONS.find(q => q.id === id);
  currentLevel = q.level;
  const others = opts.filter(t => t !== q.highlights[k].topic);
  getDistractors = () => others;
  phraseQueue = [{question: q, highlightIndex: k, phraseNum: 1, totalInQ: 1}];
  totalPhrases = 1; phraseIndex = 0; correctCount = 0;
  showScreen('game'); showPhrase();
  return [...document.querySelectorAll('#optionsGrid .option-btn')].map(b => b.textContent);
}"""

CLICK = """(t) => { const b = [...document.querySelectorAll('#optionsGrid .option-btn')].find(b => b.textContent === t);
  b.click(); const qa = window.__ev.filter(e => e[0] === 'question_answered');
  return {n: qa.length, correct: qa.length ? qa[qa.length - 1][1].correct : null, idx: phraseIndex}; }"""

AGAIN = """() => { document.querySelectorAll('#optionsGrid .option-btn').forEach(b => {
  b.click(); b.focus();
  ['keydown', 'keypress', 'keyup'].forEach(t => b.dispatchEvent(new KeyboardEvent(t, {key: 'Enter', bubbles: true})));
  b.click(); });
  return {n: window.__ev.filter(e => e[0] === 'question_answered').length, idx: phraseIndex,
    done: window.__ev.filter(e => e[0] === 'game_completed').length}; }"""


def play(fails, page, data):
    bank = data['bank']
    ks3, gcse = list(data['ks3']), list(data['ks3']) + list(data['gcse'])
    lock_tested = False
    for q in bank:
        offered = ks3 if q['level'] == 'ks3' else gcse
        for k, h in enumerate(q['highlights']):
            key = (q['id'], k)
            want, tag, why = ACCEPT.get(key, ({h['topic']}, None, None))
            others = [t for t in offered if t not in want][:3]
            for t in sorted(want) + others:
                opts = [t] + [o for o in ([h['topic']] + others) if o != t][:3]
                shown = page.evaluate(SHOW, [q['id'], k, opts])
                if t not in shown:
                    fails.append('%s phrase %d: could not put "%s" on the buttons (%s)' % (q['id'], k + 1, t, shown))
                    continue
                r = page.evaluate(CLICK, t)
                right = t in want
                if r['n'] != 1 or r['correct'] != right:
                    who = (TAG + tag + ' ') if tag and right else ''
                    fails.append('%s%s phrase %d ("%s"): "%s" was marked %s; it is %s%s'
                                 % (who, q['id'], k + 1, h['phrase'], t,
                                    {True: 'right', False: 'wrong', None: 'nothing'}[r['correct']] if r['n'] == 1 else '%d times' % r['n'],
                                    'right' if right else 'wrong', (' (' + why + ')') if why and right else ''))
                if not lock_tested:
                    lock_tested = True
                    a = page.evaluate(AGAIN)
                    if a['n'] != 1 or a['idx'] != 1:
                        fails.append('%s: after a mark, clicking and pressing Enter on the options marked %d more and '
                                     'moved %d phrases (none; once): the next phrase is answered unseen'
                                     % (TAG + 't1-005', a['n'] - 1, a['idx'] - 1))
    # the session ends once
    page.evaluate(SHOW, [bank[0]['id'], 0, [bank[0]['highlights'][0]['topic']]])
    page.evaluate("() => { endGame(); endGame(); }")
    done = page.evaluate("() => window.__ev.filter(e => e[0] === 'game_completed').length")
    if done != 1:
        fails.append('the session ended %d times (once: game_completed and submitScore)' % done)


def run(html):
    from playwright.sync_api import sync_playwright
    fails = []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
            ctx.add_init_script(INIT)
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            pat = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
            ctx.route(lambda u: bool(pat.search(u)), lambda r: r.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function("typeof QUESTIONS !== 'undefined' && typeof showPhrase === 'function'", timeout=8000)
            data = page.evaluate(DATA)
            check_bank(fails, data)
            play(fails, page, data)
            errs = [e for e in errors if 'firebase' not in e.lower()]
            if errs:
                fails.append('page errors: %s' % '; '.join(errs[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return fails, data


PLANTS = [
    (TAG + 't1-005', 't1-005: no lock on the options', '  if (!MaffsLock.lock(optionsGrid)) return;\n', ''),
    (TAG + 't1-003', 't1-003: the scheme off',
     "const PARENT_TOPIC = {'Reverse Percentage': 'Percentages', 'Standard Form': 'Number & Place Value'};",
     'const PARENT_TOPIC = {};'),
    (TAG + 't1-002', "t1-002: gcse_017's second topic off",
     "topic:'Algebra — Equations & Inequalities',also:['Algebra — Simultaneous Equations'],",
     "topic:'Algebra — Equations & Inequalities',"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, data = run(html)
    print('%s: %d items, %d phrases: each marked right under exactly the topics that fit it (SR-18), played in '
          'Chromium; answer once' % (SLUG, len(data['bank']), sum(len(q['highlights']) for q in data['bank'])))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-40s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            hit = [f for f in run(html.replace(old, new))[0] if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-40s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
