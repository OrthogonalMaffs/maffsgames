#!/usr/bin/env python3
# ci-line: E | Like Terms Collector (all 45 keys recomputed, SymPy; typed answers marked as exact whole numbers in Chromium at 390px) |
"""Independent verification of like-terms-collector (tranche 3 audit, like-terms-collector-t3-001).

The game has one level (year6), 45 items in three stages: Stage 1 (5) and Stage 2 (10) are typed,
two boxes each; Stage 3 (30) is four options.

Keys, recomputed with SymPy from what the student reads (the bank is read from the live page):
  - Stage 1: the prompt's pictures, one symbol per fruit in order of first appearance, matched to
    the labels in that order; each box's key is the coefficient of its fruit.
  - Stage 2: the prompt parsed as algebra; each box's key is the coefficient of its label.
  - Stage 3: the expression simplified; the key must equal it and no distractor may (canon SR-16:
    a true statement is never a wrong option); the four options are distinct.

Marking, in Chromium at 390x844, through the game's own Check button, read from the feedback it shows: item 1 typed 8.9 and 6.5 must be marked wrong, and the feedback must say a decimal is not
a whole number; 8 and 6 must be marked right. Every typed item's keys must be marked right, and
its first key plus 0.9 (a decimal parseInt would truncate back to the key) marked wrong. Marking
is MaffsAnswer.exact() (schools/assets/answer.js, canon §7.1.3); parseInt truncated 8.9 to 8.

A self-test plants the parseInt marking back into the served page and must FAIL; it runs unless
--no-selftest.

    python scripts/verify-like-terms-collector.py [--verbose] [--no-selftest] [--against FILE]

--against FILE serves FILE as the game page (e.g. main's copy, to show the check fails on it).
"""
import argparse
import os
import re
import sys

from sympy import Symbol, expand, sympify
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'like-terms-collector'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
TRANSFORMS = standard_transformations + (implicit_multiplication_application,)
# The fix's marking call, and the parseInt marking the self-test plants back in its place.
FIXED = "MaffsAnswer.exact(inp.value,q.answers[k])"
PLANTED = "(parseInt(inp.value,10)===q.answers[k]?'correct':'wrong')"


def algebra(text):
    return parse_expr(text.replace('−', '-'), transformations=TRANSFORMS)


def check_bank(fails, bank, verbose=False):
    s1, s2, s3 = bank['STAGE1'], bank['STAGE2'], bank['STAGE3']
    if (len(s1), len(s2), len(s3)) != (5, 10, 30):
        fails.append('bank: stages hold %d/%d/%d items, expected 5/10/30' % (len(s1), len(s2), len(s3)))
    for i, q in enumerate(s1):
        terms = [t.strip() for t in q['prompt'].split('+')]
        kinds, expr = [], 0
        for t in terms:
            m = re.match(r'^(\d+)\s+(\S+)$', t)
            if not m:
                fails.append('stage 1 item %d: term %r is not "<count> <picture>"' % (i + 1, t))
                break
            if m.group(2) not in kinds:
                kinds.append(m.group(2))
            expr += int(m.group(1)) * Symbol('f%d' % kinds.index(m.group(2)))
        if len(kinds) != len(q['labels']):
            fails.append('stage 1 item %d: %d kinds of picture for %d labels' % (i + 1, len(kinds), len(q['labels'])))
            continue
        want = [int(sympify(expr).coeff(Symbol('f%d' % k))) for k in range(len(kinds))]
        if want != q['answers']:
            fails.append('stage 1 item %d (%s): keyed %s, recomputed %s' % (i + 1, q['prompt'], q['answers'], want))
        elif verbose:
            print('  stage 1 item %-2d %s -> %s' % (i + 1, q['labels'], want))
    for i, q in enumerate(s2):
        e = expand(algebra(q['prompt']))
        want = [int(e.coeff(Symbol(l))) for l in q['labels']]
        if want != q['answers'] or expand(e - sum(w * Symbol(l) for w, l in zip(want, q['labels']))) != 0:
            fails.append('stage 2 item %d (%s): keyed %s, recomputed %s' % (i + 1, q['prompt'], q['answers'], want))
        elif verbose:
            print('  stage 2 item %-2d %s = %s' % (i + 1, q['prompt'], e))
    for i, q in enumerate(s3):
        e = expand(algebra(q['expr']))
        if expand(algebra(q['answer']) - e) != 0:
            fails.append('stage 3 item %d (%s): keyed %s, simplifies to %s' % (i + 1, q['expr'], q['answer'], e))
        for d in q['distractors']:
            if expand(algebra(d) - e) == 0:
                fails.append('stage 3 item %d (%s): distractor %s is also right (SR-16)' % (i + 1, q['expr'], d))
        opts = [q['answer']] + q['distractors']
        if len(opts) != 4 or len({str(expand(algebra(o))) for o in opts}) != 4:
            fails.append('stage 3 item %d (%s): options %s are not four distinct values' % (i + 1, q['expr'], opts))
        elif verbose:
            print('  stage 3 item %-2d %s = %s' % (i + 1, q['expr'], e))


# Every typed item, loaded through the game's own loadQuestion(); answers typed into its boxes and
# marked by its own Check button. Returns the mark it gave each attempt (MARK).
SWEEP_JS = """async (attempts) => {
  const out = [];
  for (const a of attempts) {
    currentStage = a.stage; currentQ = a.q; loadQuestion();
    document.getElementById('ans0').value = a.v[0];
    document.getElementById('ans1').value = a.v[1];
    document.getElementById('checkBtn').click();
    // Wait for the game's own mark to land (up to 5 s) before reading it; never read it straight off the click.
    for (let t = 0; MARK() === null && t < 250; t++) await new Promise(r => setTimeout(r, 20));
    out.push(MARK());
  }
  return out;
}"""
# The mark the game gave: showFeedback() sets the icon's class synchronously ('correct' or 'incorrect'); null if
# Check marked nothing. (Not the analytics event: analytics.js can replace window.mfg after a hook is installed,
# which made the first run on main see no event, 6 Oct 2026.)
MARK_JS = """() => { window.MARK = () => {
  const panel = document.getElementById('feedbackPanel'), icon = document.getElementById('feedbackIcon');
  if (!panel.classList.contains('correct-fb') && !panel.classList.contains('incorrect-fb')) return null;
  return icon.classList.contains('correct'); }; }"""


# Reading the mark: a check run on main once read it straight after page.click('#checkBtn') and saw nothing
# ("marked correct=None", run 37626794263, attempt 1; the rerun passed). A flaky check is a test fault: wait for the
# game's own marking to land, as the 6 Oct fix did for the analytics event. The self-test serves a copy whose
# showFeedback() marks DEFER ms late: the waiting read must still see every mark, and a read straight off the
# click must see none (proof the plant exercises the early read).
# The early read is made in the same page task as the click (8 Oct 2026): a timer cannot fire inside one
# synchronous task, so it sees no mark on any runner. As a separate Playwright call after page.click it raced the
# DEFER timer, and a slow runner let the mark land first (main went red once on this self-test; contract DET's rule:
# a verdict never depends on timing).
DEFER = 300
SHOW_FEEDBACK = 'function showFeedback(correct,detail){'
DEFERRED = ('function showFeedback(correct,detail){setTimeout(function(){_showFeedbackNow(correct,detail)},%d)}'
            'function _showFeedbackNow(correct,detail){' % DEFER)


def read_mark(page, timeout=5000):
    """The game's mark once it has landed; None if Check marked nothing within the timeout. The mark is taken
    from the same page task that saw it land (MAIN-RED, 8 Oct 2026), never from a second call after it."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    try:
        h = page.wait_for_function('() => { const m = MARK(); return m === null ? null : { m: m }; }', timeout=timeout)
    except PlaywrightTimeout:
        return None
    return h.json_value()['m']


def play(fails, against=None, planted=False, deferred=None):
    """deferred: a list; when given, showFeedback is served DEFER ms late and each item-1 read made straight
    off the click is appended to it."""
    from playwright.sync_api import sync_playwright
    html = open(against or GAME, encoding='utf-8').read()
    if deferred is not None:
        if html.count(SHOW_FEEDBACK) != 1:
            fails.append('self-test: %s is not in the page once, so the late mark could not be planted' % SHOW_FEEDBACK)
            return None
        html = html.replace(SHOW_FEEDBACK, DEFERRED)
    if planted:
        if FIXED not in html:
            fails.append('self-test: the marking call %s is not in the page, so nothing could be planted' % FIXED)
            return None
        html = html.replace(FIXED, PLANTED)
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: a sweep answers at once
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            errors = []

            def fresh():
                page = ctx.new_page()
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
                page.wait_for_function('typeof STAGE1 !== "undefined" && typeof checkInputAnswer === "function"',
                                       timeout=8000)
                page.evaluate(MARK_JS)
                page.click('.start-btn')
                page.wait_for_selector('#ans0', state='visible')
                # Type only once the question has settled: loadInputQuestion() focuses #ans0 on a 50 ms timer. Typed
                # earlier, that timer could fire inside fill('#ans1') (fill selects the box, then inserts the text
                # in a second step), so "6.5" went into #ans0 ("8.965", #ans1 empty) and Check marked nothing:
                # main red after #180 (47ee9b9, run 37811456669 attempt 1, "marked correct=None"), and likely the
                # earlier one-off failures after #89 and #109. The page's own focus is the signal, not a delay.
                page.wait_for_function("() => document.activeElement && document.activeElement.id === 'ans0'",
                                       timeout=8000)
                return page

            bank = None
            # Item 1, typed as a student types, at 390px.
            for typed, want in ((('8.9', '6.5'), False), (('8', '6'), True)):
                page = fresh()
                if bank is None:
                    bank = page.evaluate('() => ({STAGE1, STAGE2, STAGE3})')
                page.fill('#ans0', typed[0])
                page.fill('#ans1', typed[1])
                if deferred is not None:
                    # Click and read in one task: the deferred mark cannot have landed yet, however slow the runner.
                    deferred.append(page.evaluate("() => { document.getElementById('checkBtn').click(); return MARK(); }"))
                else:
                    page.click('#checkBtn')
                got = read_mark(page)
                fb = page.evaluate("() => document.getElementById('feedbackDetail').textContent")
                if got is not want:
                    fails.append('item 1: typed %s/%s, marked correct=%s, expected %s'
                                 % (typed[0], typed[1], got, want))
                if not want and not re.search(r'not (a )?whole number', fb):
                    fails.append('item 1: typed %s/%s, the feedback does not say why: %r'
                                 % (typed[0], typed[1], fb.strip()[:120]))
                page.close()
            # Every typed item: the keys marked right; the first key plus 0.9 marked wrong.
            page = fresh()
            attempts, labels = [], []
            for stage, name in ((0, 'STAGE1'), (1, 'STAGE2')):
                for q, item in enumerate(bank[name]):
                    k = item['answers']
                    attempts.append({'stage': stage, 'q': q, 'v': [str(k[0]), str(k[1])]})
                    labels.append(('stage %d item %d' % (stage + 1, q + 1), '%s/%s' % (k[0], k[1]), True))
                    attempts.append({'stage': stage, 'q': q, 'v': ['%d.9' % k[0], str(k[1])]})
                    labels.append(('stage %d item %d' % (stage + 1, q + 1), '%d.9/%s' % (k[0], k[1]), False))
            got = page.evaluate(SWEEP_JS, attempts)
            for (where, typed, want), g in zip(labels, got):
                if g is not want:
                    fails.append('%s: typed %s, marked correct=%s, expected %s' % (where, typed, g, want))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()

    fails = []
    bank = play(fails, args.against)
    if bank is not None:
        check_bank(fails, bank, args.verbose)
    print('%s: %d keys recomputed (SymPy), 15 typed items marked in Chromium at 390px'
          % (SLUG, sum(len(bank[k]) for k in bank) if bank else 0))

    ok = True
    if not args.no_selftest and not args.against:
        planted = []
        play(planted, planted=True)
        caught = any('item' in f for f in planted)
        ok = caught
        print('  self-test %-40s %s' % ('parseInt marking planted back',
                                        ('caught: ' + planted[0][:100]) if caught else '*** MISSED ***'))
        late, early = [], []
        play(late, deferred=early)
        held = not late and early and all(e is None for e in early)
        ok = ok and held
        print('  self-test %-40s %s' % ('mark landing %d ms after Check' % DEFER,
                                        'read only once it landed' if held else
                                        '*** %s ***' % ('early read: ' + str(early) if late == [] else late[0][:100])))
        bad = dict(bank['STAGE2'][0]) if bank else None
        if bad:
            rep = []
            check_bank(rep, dict(bank, STAGE2=[dict(bad, answers=[bad['answers'][0] + 1, bad['answers'][1]])]
                                 + bank['STAGE2'][1:]))
            ok = ok and bool(rep)
            print('  self-test %-40s %s' % ('a wrong Stage 2 key', ('caught: ' + rep[0][:100]) if rep else '*** MISSED ***'))
            q3 = bank['STAGE3'][0]
            rep = []
            check_bank(rep, dict(bank, STAGE3=[dict(q3, distractors=[q3['answer'].replace(' + ', '+')] + q3['distractors'][1:])]
                                 + bank['STAGE3'][1:]))
            ok = ok and bool(rep)
            print('  self-test %-40s %s' % ('a true distractor (SR-16)', ('caught: ' + rep[0][:100]) if rep else '*** MISSED ***'))

    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
