#!/usr/bin/env python3
# ci-line: Core Maths Paper 2B (Q28's policy recomputed from its table, no wrong option picking the same policy; every option marked in Chromium) |
"""Core Maths Paper 2B: no wrong option picks the key's answer for another reason.

36 exam-style multiple-choice questions (S3.4, S3.9, S3.10). The tranche 2 audit of 6 Oct 2026 found Q28 (two
risks, one affordable insurance policy) keyed "Data breach - higher expected loss" with option D "Data breach -
larger potential loss": the same policy, for the risk-aversion reason Q27 and Q34 teach, marked wrong
(core-maths-paper2b-t2-001, HIGH; contract LISTED-HIGH and Jon's ruling, 9 Oct 2026: rewrite option D so it
does not pick the same policy as the key).

Checks: Q28's choice recomputed from its own table and premiums (the policy whose premium is below its expected
loss, the greater benefit); the key picks it; no other option picks it. Every option of every question clicked
in Chromium (390x844) through selectAnswer(), the mark read from the button: right exactly for the key.
A self-test plants the old option D; it must FAIL naming Q28.

    python scripts/verify-core-maths-paper2b.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'core-maths-paper2b'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNT = 36


def money(s):
    return F(re.sub(r'[^\d.]', '', s))


def check_bank(fails, bank):
    if len(bank) != COUNT:
        fails.append('bank: %d questions, expected %d' % (len(bank), COUNT))
    hits = [i for i, q in enumerate(bank) if 'only afford one insurance policy' in (q.get('stemAfterTable') or '')]
    if len(hits) != 1:
        fails.append('Q28 not found once (%s)' % hits)
        return
    n = hits[0]
    q = bank[n]
    w = 'Q%d (t2-001)' % (n + 1)
    rows = {r[0].split()[0]: F(r[1]) * money(r[2]) for r in q['table']['rows']}      # Equipment, Data: E(loss)
    prem = {k.split()[0].capitalize(): money(v)
            for k, v in re.findall(r'(equipment|data breach) cover at £([\d,]+)', q['stemAfterTable'], re.I)}
    if set(prem) != set(rows):
        fails.append('%s: premiums %s do not match the risks %s' % (w, prem, rows))
        return
    benefit = {k: rows[k] - prem[k] for k in rows}
    best = max(benefit, key=benefit.get)
    if benefit[best] <= 0:
        fails.append('%s: no policy is worth buying on expected value (%s)' % (w, benefit))
    key = q['options'][q['correct']]
    if not key.startswith(best):
        fails.append('%s: keyed %r; the policy with the larger expected benefit is %s (%s)' % (w, key, best, benefit))
    for i, o in enumerate(q['options']):
        if i != q['correct'] and o.startswith(best):
            fails.append('%s: the wrong option %r picks the same policy as the key' % (w, o))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0;
  const out = [];
  QUESTIONS.forEach((q, n) => q.options.forEach((_, i) => {
    currentQ = n; answers = []; score = 0;
    showQuestion();
    const btn = [...document.querySelectorAll('#optionsContainer .option-btn')].find(b => b.dataset.val === String(i));
    if (!btn) { out.push([n, i, 'not on screen']); return; }
    btn.click();
    const right = btn.classList.contains('correct');
    if (right !== (i === q.correct)) out.push([n, i, right ? 'marked right' : 'marked wrong']);
  }));
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QUESTIONS')
            page.evaluate("() => { document.querySelector('.start-btn').click(); }")
            for n, i, what in page.evaluate(SWEEP_JS):
                fails.append('Q%d in Chromium: option %s %s' % (n + 1, 'ABCD'[i], what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


def esc(x):
    """The page writes non-ASCII characters as JS escapes (a backslash, u, four hex digits)."""
    return ''.join(c if ord(c) < 128 else chr(92) + 'u%04x' % ord(c) for c in x)


PLANTS = [
    ('Q28 (t2-001)', 't2-001: option D "Data breach - larger potential loss"',
     "'Neither — both premiums cost more than the expected loss']", "'Data breach — larger potential loss']"),
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
    print('%s: %d questions, Q28 recomputed from its table, every option marked in Chromium' % (SLUG, len(bank or [])))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            new, old = esc(new), esc(old)
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(new, old))
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
