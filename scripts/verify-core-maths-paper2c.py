#!/usr/bin/env python3
# ci-line: Core Maths Paper 2C (every option marked against its key or accepted set; Jon's rulings on Q12 and Q35; a double-tap on Next answers nothing; Chromium) |
"""Core Maths Paper 2C: every option is marked as its item says, and a double-tap on Next answers nothing.

36 exam-style multiple-choice questions (S3.4, S3.11, S3.12, S3.13). The tranche 4 audit of 6 Oct 2026 found
(contract LISTED-HIGH and Jon's rulings, 9 Oct 2026):
  core-maths-paper2c-t4-001  a double-tap on Next answered the next question unseen. Fixed on main by F1 batch 10
                             (MaffsLock: Next acts once, on an answered question; options fresh-locked). Kept here.
  core-maths-paper2c-t4-002  Q12, a minimum between (2, 7) and (6, 7) keyed 4 "by symmetry", f never said to be
                             a quadratic (3 and 5 were possible). The stem now says "f is a quadratic".
  core-maths-paper2c-t4-003  Q35, option D "Yes - but only when k > 0" is true (a doubling time exists only for
                             growth). Jon's ruling (16:21): D is accepted alongside the key, both marked right, the
                             explanation saying why; the other two are wrong.

Checks: every question's options clicked in Chromium (390x844) through selectAnswer(), the mark read from the
button: right exactly when the option is the key or in the item's accept set; RULED pins Q12's words and Q35's
accepted pair and explanation; then a real session (real timers), Q1 answered and Next tapped with a second tap
on the next question's first option at once (a double-tap): the second question must be on screen, unanswered. A self-test plants each finding back; each must FAIL.

    python scripts/verify-core-maths-paper2c.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'core-maths-paper2c'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNT = 36


def check_bank(fails, bank):
    if len(bank) != COUNT:
        fails.append('bank: %d questions, expected %d' % (len(bank), COUNT))
    q12 = [i for i, q in enumerate(bank) if '(2, 7) and (6, 7)' in q['stem']]
    q35 = [i for i, q in enumerate(bank) if 'doubling time is constant regardless' in q['stem']]
    if len(q12) != 1 or len(q35) != 1:
        fails.append('Q12 or Q35 not found once (%s, %s)' % (q12, q35))
        return
    q = bank[q12[0]]
    if 'f is a quadratic' not in q['stem'] or q['options'][q['correct']] != '4':
        fails.append('Q%d (t4-002): the stem must say "f is a quadratic" for the key 4 to hold by symmetry'
                     % (q12[0] + 1))
    q = bank[q35[0]]
    d = q['options'].index('Yes — but only when k > 0') if 'Yes — but only when k > 0' in q['options'] else None
    accepted = sorted(q.get('accept') or [q['correct']])
    if d is None or accepted != sorted({q['correct'], d}):
        fails.append('Q%d (t4-003): accepted %s; Jon\'s ruling accepts the key and "Yes - but only when k > 0" (%s)'
                     % (q35[0] + 1, accepted, sorted({q['correct'], d if d is not None else -1})))
    elif not re.search(r'[Bb]oth', q['working']) or 'k > 0' not in q['working']:
        fails.append('Q%d (t4-003): the explanation must say why both are right' % (q35[0] + 1))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [];
  QUESTIONS.forEach((q, n) => {
    const ok = q.accept || [q.correct];
    q.options.forEach((_, i) => {
      currentQ = n; answers = []; score = 0;
      showQuestion();
      const btn = [...document.querySelectorAll('#optionsContainer .option-btn')].find(b => b.dataset.val === String(i));
      if (!btn) { out.push([n, i, 'not on screen']); return; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== ok.includes(i)) out.push([n, i, right ? 'marked right' : 'marked wrong']);
    });
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            bank = None
            for sweep in (True, False):
                ctx = browser.new_context(viewport={'width': 390, 'height': 844})
                if sweep:
                    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
                ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
                ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                    status=200, content_type='text/html; charset=utf-8', body=html))
                page = ctx.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
                page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=15000)
                if sweep:
                    bank = page.evaluate('() => QUESTIONS')
                    page.evaluate("() => { document.querySelector('.start-btn').click(); }")
                    for n, i, what in page.evaluate(SWEEP_JS):
                        fails.append('Q%d in Chromium: option %s %s' % (n + 1, 'ABCD'[i], what))
                else:
                    # t4-001: a real session; Q1 answered, then Next double-clicked as a student would.
                    page.locator('.start-btn').click()
                    page.wait_for_selector('#optionsContainer .option-btn', timeout=10000)
                    time.sleep(0.5)                                  # MaffsLock's fresh window
                    page.locator('#optionsContainer .option-btn').first.click()
                    page.wait_for_selector('#nextBtn.visible', timeout=10000)
                    # The double-tap: Next, then at once a tap on the next question's option under the finger.
                    page.locator('#nextBtn').click()
                    page.locator('#optionsContainer .option-btn').first.click(timeout=2000)
                    time.sleep(0.8)
                    q, answered = page.evaluate('() => [currentQ, answers.length]')
                    if q != 1 or answered != 1:
                        fails.append('t4-001: a double-tap on Next left question %d on screen with %d answered '
                                     '(expected Q2, 1 answered)' % (q + 1, answered))
                ctx.close()
                if errors:
                    fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            return bank
    finally:
        proc.terminate()
        proc.wait()


def esc(x):
    """The page writes non-ASCII characters as JS escapes (a backslash, u, four hex digits)."""
    return ''.join(c if ord(c) < 128 else chr(92) + 'u%04x' % ord(c) for c in x)


# (the text the failure must start with, what is planted, [(today's text, the fault), ...]).
PLANTS = [
    ('Q12 (t4-002)', 't4-002: Q12 without "f is a quadratic"',
     [("stem:'f is a quadratic. The graph of y = f(x)", "stem:'The graph of y = f(x)")]),
    ('Q35 (t4-003)', "t4-003: Q35 with D not accepted", [('    accept:[1,3],\n', '')]),
    ('t4-001', 't4-001: no fresh lock on a new question (before F1 batch 10)',
     [('  MaffsLock.fresh(container);   // a new question', '  // a new question'),
      ('  MaffsLock.fresh(oc);\n  currentQ++;', '  currentQ++;')]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank is not None:
        check_bank(fails, bank)
    print('%s: %d questions, every option marked in Chromium; Next double-tapped in a real session'
          % (SLUG, len(bank or [])))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, swaps in PLANTS:
            planted_html = html
            for new, old in swaps:
                new, old = esc(new), esc(old)
                if planted_html.count(new) != 1:
                    break
                planted_html = planted_html.replace(new, old)
            else:
                new = None
            if new is not None:
                print('  self-test %-46s *** CANNOT PLANT ***' % what)
                ok = False
                continue
            rep = []
            planted = play(rep, planted_html)
            if planted is not None:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
