#!/usr/bin/env python3
# ci-line: Expected Damage (every E(X) recomputed exactly, no ties, shown probabilities read back) |
"""Expected Damage: every expected value recomputed exactly, every key checked, every shown
probability read back from the page.

The bank (50 questions: ks3 15, gcse 20, core 15) was keyed by hand and never verified. The resit
correctness audit of 4 Oct 2026 found two ties keyed as one-track wins (F1: ed_gcse_011, E = 5 and
5; ed_gcse_018, E = 4 and 4), so a student who calculated correctly and chose the other track was
counted as not optimal. Jon's ruling (4 Oct 2026, SR-5): comparison questions never tie.

The bank is read from the live page (post any runtime patch), then for every question:
  Probabilities: each stored value is read as the exact fraction it stands for (the smallest
    denominator up to 1000 whose double is the stored number, so 1/3 is a third and 0.35 is 7/20),
    each in (0, 1]; a track sums to at most 1 (Fraction); escapeEventPossible is true exactly when a
    track sums below 1. (Audit F2, how the game DRAWS an outcome when a track sums below 1, is
    logged and not checked here.)
  Expected values: each track's E(X) recomputed exactly; the stored ev must equal it, the stored
    evDifference must equal |E(A) - E(B)|, higherEVOption must name the strictly higher track, and
    a tie FAILS (SR-5).
  Word problems: every percentage in a track's story equals one of that track's probabilities, its
    complement, the track's total or what is left of 100%.
  The page, in Chromium: every question is shown through the game's own loadQuestion(), and every
    outcome line under each track is read back: the probability shown (a %, or a fraction such as
    a third) and the Muppet count must equal the stored outcome exactly, in order. No choice is
    made, so nothing is drawn, scored or submitted; every request off the stub server is aborted.
A fault-injection self-test (a tie, and a wrong higherEVOption, on patched copies of the bank) must
FAIL each time; it runs unless --no-selftest. The file is never touched.

    python scripts/verify-expected-damage.py [--verbose] [--no-selftest] [--chromium PATH]
"""
import argparse
import copy
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'expected-damage'
COUNTS = {'ks3': 15, 'gcse': 20, 'core': 15}
SHOWN_FRACTIONS = {'⅓': F(1, 3), '⅔': F(2, 3), '¼': F(1, 4), '¾': F(3, 4), '½': F(1, 2)}


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, where, what, detail):
        self.fails.append('%s %s: %s' % (where, what, detail))


def exact(x):
    """The fraction a stored double stands for, or None if no denominator up to 1000 gives it."""
    f = F(x).limit_denominator(1000)
    return f if float(f) == x else None


def shown_value(text):
    """A probability as the page shows it: '35%', a fraction character, or 'a/b'."""
    text = text.strip()
    if text in SHOWN_FRACTIONS:
        return SHOWN_FRACTIONS[text]
    m = re.fullmatch(r'(\d+)%', text)
    if m:
        return F(int(m.group(1)), 100)
    m = re.fullmatch(r'(\d+)/(\d+)', text)
    if m:
        return F(int(m.group(1)), int(m.group(2)))
    return None


def track(rep, where, opt):
    """Check one track's probabilities; return (exact probabilities, their sum, E(X)) or None."""
    probs = []
    for o in opt['outcomes']:
        p = exact(o['probability'])
        if p is None:
            rep.fail(where, 'probability', '%r is not a fraction with denominator up to 1000' % o['probability'])
            return None
        if not 0 < p <= 1:
            rep.fail(where, 'probability', '%s is not in (0, 1]' % p)
        probs.append(p)
    total = sum(probs, F(0))
    if total > 1:
        rep.fail(where, 'sum', 'probabilities sum to %s, more than 1' % total)
    ev = sum((p * o['muppets'] for p, o in zip(probs, opt['outcomes'])), F(0))
    if exact(opt['ev']) != ev:
        rep.fail(where, 'ev', 'stored %s, recomputed %s' % (opt['ev'], ev))
    for m in re.finditer(r'(\d+(?:\.\d+)?)%', opt.get('description') or ''):
        pct = F(m.group(1)) / 100
        if pct not in set(probs) | {1 - p for p in probs} | {total, 1 - total}:
            rep.fail(where, 'story', 'the story says %s%%; the track stores %s (total %s)'
                     % (m.group(1), [str(p) for p in probs], total))
    return probs, total, ev


def check_bank(rep, bank, verbose=False):
    for level, n in COUNTS.items():
        if len(bank.get(level, [])) != n:
            rep.fail(level, 'count', '%d questions, expected %d (a change to the bank needs this verifier '
                     'updated)' % (len(bank.get(level, [])), n))
    for level, qs in bank.items():
        for q in qs:
            where = q['id']
            a = track(rep, where + ' Track A', q['optionA'])
            b = track(rep, where + ' Track B', q['optionB'])
            if a is None or b is None:
                continue
            short = a[1] < 1 or b[1] < 1
            if q['escapeEventPossible'] != short:
                rep.fail(where, 'escape', 'escapeEventPossible is %s, but the totals are %s and %s'
                         % (q['escapeEventPossible'], a[1], b[1]))
            ea, eb = a[2], b[2]
            if ea == eb:
                rep.fail(where, 'tie', 'E(A) = E(B) = %s: a comparison never ties (SR-5)' % ea)
            else:
                want = 'A' if ea > eb else 'B'
                if q['higherEVOption'] != want:
                    rep.fail(where, 'key', 'keyed %s, but E(A) = %s and E(B) = %s'
                             % (q['higherEVOption'], ea, eb))
            if exact(q['evDifference']) != abs(ea - eb):
                rep.fail(where, 'evDifference', 'stored %s, recomputed %s' % (q['evDifference'], abs(ea - eb)))
            if verbose:
                print('  %-12s E(A) %-6s E(B) %-6s keyed %s' % (where, ea, eb, q['higherEVOption']))


# ---------------------------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------------------------
JS_SHOW = '''(q) => {
  sessionQuestions = [q]; questionIndex = 0; loadQuestion();
  const read = side => [...document.querySelectorAll('#outcomes' + side + ' > div')].map(d => {
    const p = d.querySelector('.prob'), m = d.querySelector('.muppet-count');
    return {prob: p ? p.textContent : null, text: d.textContent, count: m ? m.textContent : null};
  });
  return {A: read('A'), B: read('B')};
}'''


JS_PLAY = r"""([lv, mode, seed]) => {
  let a = seed >>> 0;
  Math.random = function () {                       // mulberry32: the dice differ with the seed
    a = (a + 0x6D2B79F5) >>> 0; let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  window.setTimeout = function () { return 0; };
  MaffsLock.timer = function (fn) { fn(); return 0; };   // the trolley and the outcome run at once
  window.mfg = function () {};
  currentLevel = lv; startGame();
  let best = 0, chosen = 0;
  for (let i = 0; i < sessionQuestions.length; i++) {
    const q = sessionQuestions[i];
    const pick = mode === 'best' ? q.higherEVOption : (q.higherEVOption === 'A' ? 'B' : 'A');
    best += (q.higherEVOption === 'A' ? q.optionA : q.optionB).ev;
    chosen += (pick === 'A' ? q.optionA : q.optionB).ev;
    selectOption(pick);
    MaffsLock.clearTimers();
    nextQuestion();
  }
  return {opt: document.getElementById('revealOptScore').textContent, you: document.getElementById('revealYourEv').textContent,
          best, chosen, fmt: String(Math.round(best * 100) / 100), fmtChosen: String(Math.round(chosen * 100) / 100),
          text: document.querySelector('.reveal-scores').textContent.replace(/\s+/g, ' ').trim()};
}"""

S1_HTML = (("the rest is an escape: nobody is hit", 'the start screen must say a track whose chances total under 100% leaves the rest as an escape (R2, expected-damage-s1-001)'),
           ('A certain track against a gamble, or two gambles.', 'the Foundation preview must describe its tracks truthfully (R3, expected-damage-s1-007)'),
           ('Gambles with two or three outcomes', "the GCSE preview must say gambles can have three outcomes (R3, expected-damage-s1-007)"),
           ('(he is not one of them)', 'gcse_007 must say whether the man is one of the 7 (R2, expected-damage-s1-004)'),
           ('(he is not counted)', 'gcse_013 must say the man is not counted (R2, expected-damage-s1-004)'))


def run_page(rep, chromium=None, verbose=False, html=None):
    """Read the bank, then read back every outcome line the page shows. Returns (bank, lines)."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(**({'executable_path': chromium} if chromium else {}))
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the playthrough answers at once
            page.route('**/*', lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
            if html is not None:
                page.route(re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG), lambda r: r.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=html))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=8000)
            bank = page.evaluate('JSON.parse(JSON.stringify(QUESTIONS))')
            lines = 0
            for level in bank:
                page.evaluate('(lv) => { currentLevel = lv; startGame(); }', level)
                for q in bank[level]:
                    shown = page.evaluate(JS_SHOW, q)
                    for side in 'AB':
                        outs = q['option' + side]['outcomes']
                        rows = shown[side]
                        where = '%s Track %s' % (q['id'], side)
                        if len(rows) != len(outs):
                            rep.fail(where, 'shown', '%d outcome lines shown, %d stored' % (len(rows), len(outs)))
                            continue
                        for o, r in zip(outs, rows):
                            lines += 1
                            if r['prob'] is None:
                                m = re.fullmatch(r'Certain: (\d+) Muppets?', r['text'].strip())
                                got, count = (F(1), int(m.group(1))) if m else (None, None)
                            else:
                                got, count = shown_value(r['prob']), int(r['count'])
                            if got is None or got != exact(o['probability']) or count != o['muppets']:
                                rep.fail(where, 'shown', 'the page shows %r; stored %s chance of %s'
                                         % (r['text'], exact(o['probability']), o['muppets']))
            # R3, Part 2 #10 (SWEEP-1 expected-damage-s1-002): optimal play is the sum of the better tracks' E(X), never a roll
            seen = {}
            for mode in ('best', 'worst'):
                for seed in (1, 2, 3):
                    for level in bank:
                        page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
                        page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=8000)
                        got = page.evaluate(JS_PLAY, [level, mode, seed])
                        key = (level, mode)
                        seen.setdefault(key, set()).add(got['opt'])
                        where = '%s %s seed %d' % (level, mode, seed)
                        if got['opt'] != got['fmt']:
                            rep.fail(where, 'reveal', 'optimal play shows %r, the better tracks\' E(X) sum to %s' % (got['opt'], got['fmt']))
                        if got['you'] != got['fmtChosen']:
                            rep.fail(where, 'reveal', 'your choices show %r, the tracks chosen sum to %s' % (got['you'], got['fmtChosen']))
                        if mode == 'best' and got['you'] != got['opt']:
                            rep.fail(where, 'reveal', 'always choosing the higher E(X) shows %r against optimal %r' % (got['you'], got['opt']))
                        if mode == 'worst' and not got['chosen'] < got['best']:
                            rep.fail(where, 'reveal', 'always choosing the lower E(X) is not below optimal (%s v %s)' % (got['chosen'], got['best']))
            browser.close()
            for e in errors:
                rep.fail('page', 'error', e)
            if verbose:
                print('  %d outcome lines read back from the page' % lines)
            return bank, lines
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank):
    lines, ok = [], True
    base = Report()
    check_bank(base, bank)

    def expect(name, fn):
        nonlocal ok
        b = copy.deepcopy(bank)
        fn(b)
        rep = Report()
        check_bank(rep, b)
        new = [f for f in rep.fails if f not in base.fails]
        ok = ok and bool(new)
        lines.append('  self-test %-40s %s' % (name, ('caught: ' + new[0][:100]) if new else '*** MISSED ***'))

    def find(b, qid):
        return next(q for qs in b.values() for q in qs if q['id'] == qid)

    def tie(b):                                                                 # the audit's F1
        q = find(b, 'ed_gcse_011')
        q['optionB']['outcomes'][1]['muppets'] = 1
        q['optionB']['ev'], q['evDifference'] = 5.0, 0.0
    expect('a tie (ed_gcse_011 back to 5 and 5)', tie)

    def wrong_key(b):
        q = find(b, 'ed_ks3_001')
        q['higherEVOption'] = 'A' if q['higherEVOption'] == 'B' else 'B'
    expect('wrong higherEVOption (ed_ks3_001 flipped)', wrong_key)
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--chromium', help='Chromium executable (a cloud sandbox: /opt/pw-browsers/chromium)')
    args = ap.parse_args()

    rep = Report()
    bank, shown = run_page(rep, args.chromium, args.verbose)
    check_bank(rep, bank, args.verbose)
    html = open(os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html'), encoding='utf-8').read()
    for need, why in S1_HTML:
        if need not in html:
            rep.fail('start screen', 'wording', why)
    if 'stand and welcome it' in html:
        rep.fail('ed_core_004', 'wording', 'four people "stand and welcome" the trolley: reads as choosing to be hit, for laughs (SR-14, R6, expected-damage-s1-003)')
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank)
        for what, today, old, tag in (
                ('optimal play rolled again (s1-002)', 'optimalScore += optOpt.ev;', 'optimalScore += (Math.random() < 0.5 ? 0 : 10);', 'reveal'),
                ('the escape line removed (s1-001)', "<br>If a track's chances add up to less than 100%, the rest is an escape: nobody is hit.", '', 'wording'),
                ('gcse_013 with the man uncounted again (s1-004)', ' (he is not counted)', '', 'wording')):
            if html.count(today) != 1:
                lines.append('  self-test %-40s *** CANNOT PLANT ***' % what)
                s_ok = False
                continue
            planted = html.replace(today, old)
            r2 = Report()
            if tag == 'reveal':
                run_page(r2, args.chromium, False, html=planted)
            else:
                for need, why in S1_HTML:
                    if need not in planted:
                        r2.fail('start screen', 'wording', why)
            hit = [f for f in r2.fails if tag in f]
            s_ok = s_ok and bool(hit)
            lines.append('  self-test %-40s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    print('\n%s: %d FAIL(s); %d questions (every E(X) recomputed exactly), %d outcome lines read back '
          'from the page' % ('PASS' if ok else 'FAILED', len(rep.fails), sum(len(v) for v in bank.values()), shown))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
