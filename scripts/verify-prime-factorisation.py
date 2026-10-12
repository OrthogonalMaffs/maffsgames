#!/usr/bin/env python3
# ci-line: Prime Sprint (every target factorised independently, every prime tap judged against a model in Chromium, the feedback and working recomputed) |
"""Prime Sprint (prime-factorisation): build the prime factorisation of a target by tapping primes.

The game is two static target banks, read from the page as served: NUMBERS_DEFAULT (28 targets, every level but Year 6)
and NUMBERS_YEAR6 (20 targets, ?level=year6), 8 dealt per session. The student taps a prime button; the tap is accepted
when the prime divides what is left (the target over the product so far), otherwise it costs a life. The factorisation
is complete when the product reaches the target. The game keeps no key: the right sequence is the target's prime
factorisation, which this script recomputes by trial division (the game's primeFactors() is never trusted).

Checks, independent of the game's code:
  Bank: every target an integer from 2 up; no target repeated within a bank; every prime factor of every target is on a
    button (the buttons read from the page must be exactly 2, 3, 5, 7, 11, 13), so every target can be finished.
  Dealing: startGame() five times at each level: 8 different targets from that level's bank.
  Play, in Chromium (390x844), at both levels, for every target: eleven tap sequences (the factorisation ascending and
    descending; each prime tapped one time too many; every button once in turn; and seeded random sequences over all six
    buttons, including taps that do not divide), each replayed against a model of the rule written here. After every tap
    the page's lives, product, the primes built and the feedback line must equal the model's; a completed target reads
    "T = p x q x ... (+200)" with the primes tapped, and scores 200 once; three wrong taps read
    "p is not a factor here. Out of lives: T = p x q x ..." with the recomputed ascending factorisation; while the
    product line is shown (the first three questions) it reads "Your product: P" with the model's P.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a target no button can finish (34 = 2 x 17), a tap
accepted when the prime divides the target but not what is left, a wrong factorisation shown when lives run out
(first prime dropped) and a wrong product line (one too many).

    python scripts/verify-prime-factorisation.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'prime-factorisation'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
BUTTONS = [2, 3, 5, 7, 11, 13]
BANKS = (('default', '', 'NUMBERS_DEFAULT'), ('year6', '&level=year6', 'NUMBERS_YEAR6'))
SESSIONS = 5
SESSION = 8
RANDOM_SEQS = 5
TIMES = ' × '


def factorise(n):
    """The prime factors of n in ascending order, by trial division."""
    out, d = [], 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out


def check_bank(fails, name, bank):
    if len(set(bank)) != len(bank):
        fails.append('%s: a target is repeated: %r' % (name, bank))
    for t in bank:
        if not isinstance(t, int) or isinstance(t, bool) or t < 2:
            fails.append('%s target %r is not an integer of at least 2' % (name, t))
            continue
        loose = [p for p in factorise(t) if p not in BUTTONS]
        if loose:
            fails.append('%s target %d has prime factor(s) %s that no button offers, so it cannot be finished' % (
                name, t, sorted(set(loose))))


def model(t, seq):
    """What the page must show after each tap in seq: (lives, product, primes built, feedback, score)."""
    rem, product, chosen, lives, locked, score, fb = t, 1, [], 3, False, 0, ''
    out = []
    for p in seq:
        if not locked:
            if rem % p != 0:
                lives -= 1
                if lives <= 0:
                    locked = True
                    fb = '%d is not a factor here. Out of lives: %d = %s' % (p, t, TIMES.join(map(str, factorise(t))))
                else:
                    fb = '%d is not a factor here!' % p
            else:
                rem //= p
                product *= p
                chosen.append(p)
                if rem == 1:
                    locked = True
                    score += 200
                    fb = '%d = %s  (+200)' % (t, TIMES.join(map(str, chosen)))
        out.append((lives, product, list(chosen), fb, score))
    return out


def sequences(t, rng):
    f = factorise(t)
    seqs = [list(f), list(reversed(f)), f + [f[0]], list(BUTTONS)]
    wrong = [p for p in BUTTONS if t % p]
    if wrong:
        seqs.append([wrong[0]] + f)
        seqs.append([wrong[-1], wrong[0], wrong[-1]] + f)
    for _ in range(RANDOM_SEQS):
        seqs.append([rng.choice(BUTTONS) for _ in range(12)])
    return seqs


PLAY_JS = r"""(args) => {
  const [t, seq] = args;
  questions = [t]; qNum = 0; score = 0; lives = 3; updateLivesDisplay();
  MaffsLock.newSession();
  loadQ();
  const out = [];
  for (const p of seq) {
    pressPrime(p);
    out.push([lives, product, chosenFactors.slice(), document.getElementById('feedback').textContent, score,
              document.getElementById('productDisplay').textContent,
              document.querySelectorAll('#livesDisplay .heart.lost').length]);
  }
  MaffsLock.clearTimers();
  return out;
}"""
DEAL_JS = r"""() => { const out = [];
  for (let k = 0; k < %d; k++) { startGame(); out.push(questions.slice()); MaffsLock.clearTimers(); }
  return out; }""" % SESSIONS


def play_bank(fails, page, name, bank):
    rng = random.Random(20261012)
    taps = 0
    for t in bank:
        for seq in sequences(t, rng):
            got = page.evaluate(PLAY_JS, [t, seq])
            want = model(t, seq)
            for i, (g, w) in enumerate(zip(got, want)):
                lives, product, chosen, fb, score, prodtxt, lost = g
                taps += 1
                where = '%s target %d, taps %s, after tap %d (%d)' % (name, t, seq, i + 1, seq[i])
                if (lives, product, chosen, fb, score) != w:
                    fails.append('%s: page shows lives %s, product %s, built %s, %r, score %s; model %r' % (
                        where, lives, product, chosen, fb, score, w))
                    break
                if prodtxt != 'Your product: %d' % w[1]:
                    fails.append('%s: product line %r, model %d' % (where, prodtxt, w[1]))
                    break
                if lost != 3 - w[0]:
                    fails.append('%s: %d hearts lost, model %d' % (where, lost, 3 - w[0]))
                    break
            if len(fails) > 25:
                return taps
    return taps


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {'taps': 0}
    try:
        with sync_playwright() as pw:
            for name, qs, var in BANKS:
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
                page.goto(base + '/games/%s/?cb=verify%s' % (SLUG, qs), wait_until='load', timeout=20000)
                page.wait_for_function('typeof pressPrime === "function" && typeof %s !== "undefined"' % var, timeout=15000)
                bank = page.evaluate('() => %s.slice()' % var)
                check_bank(fails, name, bank)
                buttons = page.evaluate("() => [...document.querySelectorAll('#primeBtns .prime-btn')].map(b => "
                                        "[+b.dataset.p, b.textContent.trim(), b.getAttribute('onclick')])")
                if [b[0] for b in buttons] != BUTTONS or any(
                        b[1] != str(b[0]) or b[2] != 'pressPrime(%d)' % b[0] for b in buttons):
                    fails.append('%s: the buttons are %r, expected the primes %r each pressing itself' % (
                        name, buttons, BUTTONS))
                for d in page.evaluate(DEAL_JS):
                    if len(d) != SESSION or len(set(d)) != SESSION or not set(d) <= set(bank):
                        fails.append('%s: a session is not %d different targets from the bank: %r' % (name, SESSION, d))
                stats['taps'] += play_bank(fails, page, name, bank)
                stats[name] = len(bank)
                if errors:
                    fails.append('%s page errors: %s' % (name, '; '.join(errors[:3])))
                browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a target no button can finish (34 = 2 x 17)', 'no button offers',
     [('var NUMBERS_YEAR6 = [12,18,20,24,', 'var NUMBERS_YEAR6 = [12,18,34,24,')]),
    ('a tap accepted that the remainder cannot take', 'model',
     [('if (remaining % p !== 0) {', 'if (currentTarget % p !== 0) {')]),
    ('a wrong factorisation shown when lives run out', 'model',
     [("primeFactors(currentTarget).join(' \\u00d7 ')", "primeFactors(currentTarget).slice(1).join(' \\u00d7 ')")]),
    ('a wrong product line (one too many)', 'product line',
     [("el.textContent = 'Your product: ' + product;", "el.textContent = 'Your product: ' + (product + 1);")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    st = play(fails, html)
    print('%s: %d default + %d Year 6 targets factorised independently; %d taps replayed against the model in Chromium'
          % (SLUG, st.get('default', 0), st.get('year6', 0), st['taps']))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-50s *** CANNOT PLANT (%r) ***' % (what, bad[0]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-50s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
