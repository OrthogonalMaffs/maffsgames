#!/usr/bin/env python3
# ci-line: Percentage Flip (every key and every figure in the working recomputed; typed answers marked right and wrong in Chromium, both ways round) |
"""Percentage Flip: "What is P% of N?", a typed answer, then the card flips to show the answer and the working.

Two static banks, read from the page as served: QUESTIONS_DEFAULT (12 items, every level but Year 6) and
QUESTIONS_YEAR6 (20 items, served at ?level=year6). Each item is {q, a, w}: the question, the key and the working.

Checks, independent of the game's code:
  Key: P and N are read from the question's own words and a = P/100 x N is recomputed with fractions.Fraction.
  Working: each working line has one of a small set of shapes (below), and every figure in it is recomputed from P and
    N: a percentage's value, a division, a multiplication, a sum; the last figure is the key. A working of any shape
    not listed fails, so a new working is classified here before it ships.
        "P% = ÷K → N÷K = A"            P/100 = 1/K and N/K = A
        "100% = the whole thing!"       P = 100 and the key is N
        "10% = T, × M = A"              T = N/10, T x M = A, 10 x M = P
        "50% = 50%+25% → a+b = A"       the pieces add to P%, a and b are those pieces of N
        "10% = T, 5% = F → T+F = A"     both pieces right, 10 + 5 = P
        "10% = T, 30% = U, 5% = F → A"  each stated piece right, pieces (without the 10%) add to P
        "10% = T, 5% = F"               each stated piece right, the last is the key
  Bank: no question repeated within a bank; a number, not text, for every key.
  Dealing: startGame() five times at each level: 10 different questions from that level's bank.
  Marking, in Chromium (390x844), every item at its level, answered through the game's own checkAnswer() and flipCard():
    the key typed: "CORRECT! +10 ..." and 10 points; the key plus or minus 1, a tenth of the key and ten times the key
    (where different), the key plus or minus 0.5, and the complement (100-P)% of N (the student who takes the wrong end
    of the percentage; where different): "WRONG ..." and no points. Flipping the card without checking first marks the
    same typed answers the same way and a wrong one reads "WRONG — answer is [key]". The back of the card shows the
    verified key and the verified working text.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong key (43 for 35% of 120), a wrong answer marked
right (any typed answer), a second correct answer (a tolerance of 1), and a wrong figure in a working (7 for 6).

    python scripts/verify-percentage-flip.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'percentage-flip'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
BANKS = (('default', ''), ('year6', '&level=year6'))
DEALS = 5
NUM = r'(\d+(?:\.\d+)?)'


def F(s):
    return Fraction(s)


def fmt(v):
    """How JavaScript prints a number: 40 as '40', 8.5 as '8.5'."""
    v = Fraction(v)
    return str(v.numerator) if v.denominator == 1 else repr(float(v))


def parse_question(q):
    m = re.fullmatch(r'What is ' + NUM + r'% of ' + NUM + r'\?', q)
    return (F(m.group(1)), F(m.group(2))) if m else None


def working_problem(w, p, n, a):
    """None when every figure in the working is right for 'p% of n = a'; otherwise what is wrong."""
    pc = lambda x: Fraction(x) / 100 * n  # the value of x% of n
    m = re.fullmatch(NUM + r'% = ÷' + NUM + r' → ' + NUM + r'÷' + NUM + ' = ' + NUM, w)
    if m:
        x, k, nn, kk, ans = map(F, m.groups())
        bad = []
        if x != p or x / 100 != 1 / k:
            bad.append('%s%% is not 1/%s of the whole' % (fmt(x), fmt(k)))
        if nn != n or kk != k or nn / kk != ans or ans != a:
            bad.append('%s÷%s is %s, not %s' % (fmt(nn), fmt(kk), fmt(nn / kk), fmt(ans)))
        return '; '.join(bad) or None
    if w == '100% = the whole thing!':
        return None if p == 100 and a == n else '100% claimed for %s%%' % fmt(p)
    m = re.fullmatch(r'10% = ' + NUM + r', × ' + NUM + ' = ' + NUM, w)
    if m:
        t, mult, ans = map(F, m.groups())
        bad = []
        if t != pc(10):
            bad.append('10%% of %s is %s, not %s' % (fmt(n), fmt(pc(10)), fmt(t)))
        if t * mult != ans or ans != a:
            bad.append('%s × %s is %s, not %s (key %s)' % (fmt(t), fmt(mult), fmt(t * mult), fmt(ans), fmt(a)))
        if 10 * mult != p:
            bad.append('10%% × %s is %s%%, not %s%%' % (fmt(mult), fmt(10 * mult), fmt(p)))
        return '; '.join(bad) or None
    m = re.fullmatch(NUM + r'% = ' + NUM + r'%\+' + NUM + r'% → ' + NUM + r'\+' + NUM + ' = ' + NUM, w)
    if m:
        x, y, z, u, v, ans = map(F, m.groups())
        bad = []
        if y + z != x or x != p:
            bad.append('%s%%+%s%% is not %s%%' % (fmt(y), fmt(z), fmt(p)))
        if u != pc(y) or v != pc(z) or u + v != ans or ans != a:
            bad.append('the pieces %s and %s are not %s%% and %s%% of %s summing to %s' % (
                fmt(u), fmt(v), fmt(y), fmt(z), fmt(n), fmt(a)))
        return '; '.join(bad) or None
    m = re.fullmatch(r'10% = ' + NUM + r', 5% = ' + NUM + r' → ' + NUM + r'\+' + NUM + ' = ' + NUM, w)
    if m:
        t, f, u, v, ans = map(F, m.groups())
        bad = []
        if t != pc(10) or f != pc(5):
            bad.append('10%% or 5%% of %s wrong (%s, %s)' % (fmt(n), fmt(t), fmt(f)))
        if (u, v) != (t, f) or u + v != ans or ans != a or p != 15:
            bad.append('%s+%s is %s, not %s as %s%% (key %s)' % (fmt(u), fmt(v), fmt(u + v), fmt(ans), fmt(p), fmt(a)))
        return '; '.join(bad) or None
    m = re.fullmatch(r'10% = ' + NUM + r', 30% = ' + NUM + r', 5% = ' + NUM + ' → ' + NUM, w)
    if m:
        t, u, f, ans = map(F, m.groups())
        bad = []
        if (t, u, f) != (pc(10), pc(30), pc(5)):
            bad.append('a stated piece is wrong: 10%% %s, 30%% %s, 5%% %s of %s' % (fmt(t), fmt(u), fmt(f), fmt(n)))
        if u + f != ans or ans != a or p != 35:
            bad.append('%s+%s is %s, not %s as %s%% (key %s)' % (fmt(u), fmt(f), fmt(u + f), fmt(ans), fmt(p), fmt(a)))
        return '; '.join(bad) or None
    m = re.fullmatch(r'10% = ' + NUM + r', 5% = ' + NUM, w)
    if m:
        t, f = map(F, m.groups())
        bad = []
        if (t, f) != (pc(10), pc(5)):
            bad.append('a stated piece is wrong (%s, %s)' % (fmt(t), fmt(f)))
        if p != 5 or f != a:
            bad.append('the last figure %s is not the key %s for %s%%' % (fmt(f), fmt(a), fmt(p)))
        return '; '.join(bad) or None
    return 'working shape not known to this verifier: %r (classify it in working_problem)' % w


def check_bank(fails, name, bank):
    seen = set()
    for i, it in enumerate(bank, 1):
        where = '%s item %d (%s)' % (name, i, it.get('q'))
        pn = parse_question(it['q'])
        if pn is None:
            fails.append('%s: the question is not "What is P%% of N?"' % where)
            continue
        p, n = pn
        if it['q'] in seen:
            fails.append('%s: the question is repeated' % where)
        seen.add(it['q'])
        if isinstance(it['a'], bool) or not isinstance(it['a'], (int, float)):
            fails.append('%s: the key is not a number: %r' % (where, it['a']))
            continue
        key = p * n / 100
        if Fraction(str(it['a'])) != key:
            fails.append('%s: keyed %s, recomputed %s' % (where, it['a'], fmt(key)))
        prob = working_problem(it['w'], p, n, key)
        if prob:
            fails.append('%s: working %r: %s' % (where, it['w'], prob))


def wrong_answers(p, n, key):
    out = {'key + 1': key + 1, 'key - 1': key - 1, 'key + 0.5': key + Fraction(1, 2), 'key - 0.5': key - Fraction(1, 2),
           'a tenth of the key': key / 10, 'ten times the key': key * 10,
           'the other end, (100-P)% of N': (100 - p) * n / 100}
    return {k: v for k, v in out.items() if v != key and v >= 0}


MARK_JS = r"""(args) => {
  const [item, typed, flipFirst] = args;
  questions = [item]; qNum = 0; score = 0; correct = 0; flipped = false;
  MaffsLock.newSession();
  loadQuestion();
  document.getElementById('answerInput').value = typed;
  if (flipFirst) flipCard(); else checkAnswer();
  MaffsLock.clearTimers();
  return {fb: document.getElementById('feedback').textContent, cls: document.getElementById('feedback').className,
          score: score, back: document.getElementById('answerText').textContent,
          working: document.getElementById('workingsText').textContent};
}"""
DEAL_JS = r"""() => { const out = [];
  for (let k = 0; k < %d; k++) { startGame(); out.push(questions.map(q => q.q)); MaffsLock.clearTimers(); }
  return out; }""" % DEALS


def mark_all(fails, page, bank, name):
    for it in bank:
        pn = parse_question(it['q'])
        if pn is None:
            continue
        p, n = pn
        key = p * n / 100
        cases = [('the key', key, True)] + [(k, v, False) for k, v in wrong_answers(p, n, key).items()]
        for what, val, right in cases:
            for flip in (False, True):
                got = page.evaluate(MARK_JS, [it, fmt(val), flip])
                where = '%s %s, %s typed (%s), %s' % (name, it['q'], what, fmt(val), 'flipped first' if flip else 'checked')
                if right:
                    if not (got['fb'].startswith('CORRECT! +10') and 'correct' in got['cls'] and got['score'] == 10):
                        fails.append('%s: the key was not marked right (%r)' % (where, got))
                else:
                    ok = got['fb'].startswith('WRONG') and 'wrong' in got['cls'] and got['score'] == 0
                    if flip:
                        ok = ok and got['fb'] == 'WRONG — answer is %s' % fmt(key)
                    if not ok:
                        fails.append('%s: a wrong answer was not marked wrong (%r)' % (where, got))
            if got['back'] != fmt(key) or got['working'] != it['w']:
                fails.append('%s %s: the back of the card shows %r / %r, not the verified key and working' % (
                    name, it['q'], got['back'], got['working']))


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    counts = {}
    try:
        with sync_playwright() as pw:
            for name, qs in BANKS:
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
                page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof checkAnswer === "function"', timeout=15000)
                bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
                check_bank(fails, name, bank)
                texts = {it['q'] for it in bank}
                for d in page.evaluate(DEAL_JS):
                    if len(d) != 10 or len(set(d)) != 10 or not set(d) <= texts:
                        fails.append('%s: a session is not 10 different questions from the bank: %r' % (name, d))
                mark_all(fails, page, bank, name)
                if errors:
                    fails.append('%s page errors: %s' % (name, '; '.join(errors[:3])))
                counts[name] = len(bank)
                browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return counts


PLANTS = [
    ('a wrong key (43 for 35% of 120)', 'keyed',
     [('{q:"What is 35% of 120?", a:42', '{q:"What is 35% of 120?", a:43')]),
    ('a wrong answer marked right (any typed answer)', 'not marked wrong',
     [('const _isOk = Math.abs(userVal - correctVal) < 0.01;', 'const _isOk = true;')]),
    ('a second correct answer (tolerance of 1)', 'not marked wrong',
     [('const _isOk = Math.abs(userVal - correctVal) < 0.01;', 'const _isOk = Math.abs(userVal - correctVal) < 1;')]),
    ('a wrong figure in a working (7 for 6)', 'working',
     [('w:"10% = 8.5, × 6 = 51"', 'w:"10% = 8.5, × 7 = 51"')]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    counts = play(fails, html)
    print('%s: %s questions recomputed (key and working); each answered right and wrong, checked and flipped, in Chromium; '
          '%d deals each' % (SLUG, ' + '.join('%d %s' % (v, k) for k, v in counts.items()), DEALS))
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
