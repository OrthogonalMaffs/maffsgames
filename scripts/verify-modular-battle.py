#!/usr/bin/env python3
# ci-line: Modular Battle (all 408 questions the generator can draw, each driven through the game's own generator: key, options, dot grid and feedback figures recomputed; every option pressed in Chromium) |
"""Modular Battle: "a mod b = ?", 90 seconds, multiple choice, with a dot-grid scaffold that withdraws and returns.

Generated, not banked: `generateQ()` draws a from 10..60 and b from 2..9 with `randInt`, so there are 51 x 8 = 408 questions.
Coverage: every one of the 408 is driven through the game's own `generateQ()` and `loadQuestion()` by steering the two
`Math.random` draws that pick a and b (the shuffles that follow use the real `Math.random`); 20,000 free draws of
`generateQ()` must land only on those 408 and reach all of them.

Checks, independent of the game's code (Python's divmod):
  Question: the text is "a mod b = ?".
  Options: min(4, b) buttons (b - 1 wrong remainders exist, at most 3 are shown), all different, each a whole number from 0 to
    b - 1 (a remainder that could happen), exactly one equal to a mod b (SR-4/SR-16).
  Dot grid, while the scaffold shows: floor(a / b) groups of b dots, then one group of a mod b red dots (none when it divides),
    and the label "a dots in groups of b - q full groups, and what is left over:" (or "nothing left over:").
  Feedback, through the game's own buttons (each option pressed): the key reads "CORRECT! a÷b=q rR" (+10); any other reads
    "WRONG! a÷b=q remainder R" with the key's button shown correct, no score, and the Next control.
  Scaffold: shown at the start; withdrawn after 2 right; back after 2 wrong in a row; withdrawn again after 2 more right.
  Session: on a controlled clock the game ends at 90 seconds with the final score and "n correct answers" for n right.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

Not asserted (open findings, left open): the start text and button say 60 seconds (modular-battle-t4-001); the portal card and spec
map (t4-002, t4-003, outside the game's folder); the scaffold's label and red dots show the answer while it is on (t4-004, a design call).

    python scripts/verify-modular-battle.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'modular-battle'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
A_RANGE = range(10, 61)
B_RANGE = range(2, 10)
FREE_DRAWS = 20000

STEER_JS = r"""() => {
  if (window.__steer) return;
  window.__steer = [];
  const R = Math.random;
  Math.random = () => (window.__steer.length ? window.__steer.shift() : R());
}"""
ONE_JS = r"""([a, b, k]) => {
  // the two draws generateQ makes: randInt(10, 60) then randInt(2, 9)
  const pick = (lo, hi, v) => (v - lo + 0.5) / (hi - lo + 1);
  score = 0; scaffoldOn = true; scaffoldCorrect = 0; scaffoldWrongStreak = 0;
  window.__steer = [pick(10, 60, a), pick(2, 9, b)];
  loadQuestion();
  const q = document.getElementById('qText').textContent;
  const btns = [...document.querySelectorAll('#answerRow .choice-btn')];
  const grid = document.getElementById('dotGrid');
  const groups = [...grid.querySelectorAll('.dot-group')].map(g => ({left: g.classList.contains('leftover'),
    n: g.querySelectorAll('.dot').length, red: g.querySelectorAll('.dot.remainder').length}));
  const info = {q: q, cur: [currentA, currentB, currentAns], opts: btns.map(b => b.textContent), shown: grid.style.display,
                groups: groups, label: document.getElementById('dotLabel').textContent};
  if (k < 0) return info;
  const target = btns[k];
  target.click();
  info.pressed = target.textContent;
  info.cls = target.className;
  info.keycls = btns.filter(b => b !== target).map(b => [b.textContent, b.className]);
  info.fb = document.getElementById('feedback').textContent;
  info.score = score;
  info.next = document.getElementById('feedback').parentNode.querySelectorAll('button:not(.choice-btn)').length;
  MaffsLock.clearTimers();
  return info;
}"""
FREE_JS = r"""(n) => { const seen = {}; let bad = null;
  for (let i = 0; i < n; i++) { const q = generateQ(); const k = q.a + ',' + q.b; seen[k] = (seen[k] || 0) + 1;
    if (q.ans !== q.a % q.b && !bad) bad = q; }
  return {seen: seen}; }"""
SCAFFOLD_JS = r"""(plan) => {
  startGame(); clearInterval(gameTimer);
  const out = [document.getElementById('dotGrid').style.display];
  for (const right of plan) {
    const btns = [...document.querySelectorAll('#answerRow .choice-btn')];
    const b = right ? btns.find(x => +x.textContent === currentAns) : btns.find(x => +x.textContent !== currentAns);
    b.click();
    MaffsLock.clearTimers();
    loadQuestion();
    // a question over 60 never draws dots, but a is at most 60, so the grid's display is the scaffold's state
    out.push(document.getElementById('dotGrid').style.display);
  }
  return out;
}"""


def expected_label(a, b):
    q, r = divmod(a, b)
    return ('%d dots in groups of %d — %d full groups, and what is left over:' % (a, b, q) if r
            else '%d dots in groups of %d — %d full groups, nothing left over:' % (a, b, q))


def check_one(fails, a, b, info, k):
    q, r = divmod(a, b)
    where = '%d mod %d' % (a, b)
    if info['q'] != '%d mod %d = ?' % (a, b) or info['cur'][:2] != [a, b]:
        fails.append('question: steering to %s showed %r (a, b = %r)' % (where, info['q'], info['cur'][:2]))
        return False
    if info['cur'][2] != r:
        fails.append('key: %s is keyed %r, the remainder is %d' % (where, info['cur'][2], r))
    opts = info['opts']
    vals = [int(o) if re.fullmatch(r'\d+', o) else None for o in opts]
    if len(opts) != min(4, b) or len(set(opts)) != len(opts) or None in vals or any(not 0 <= v < b for v in vals):
        fails.append('options: %s shows %r: expected %d different whole numbers from 0 to %d' % (where, opts, min(4, b), b - 1))
    if vals.count(r) != 1:
        fails.append('options: %s shows %r: %d of them equal the remainder %d' % (where, opts, vals.count(r), r))
    if k < 0:
        if info['shown'] != 'flex':
            fails.append('dots: %s: the scaffold is not shown on a fresh question' % where)
        full = [g for g in info['groups'] if not g['left']]
        left = [g for g in info['groups'] if g['left']]
        if len(full) != q or any(g['n'] != b or g['red'] for g in full) or \
                (r and (len(left) != 1 or left[0]['n'] != r or left[0]['red'] != r)) or (not r and left):
            fails.append('dots: %s: groups drawn %r, expected %d groups of %d and %d red' % (where, info['groups'], q, b, r))
        if info['label'] != expected_label(a, b):
            fails.append('dots: %s: label %r, expected %r' % (where, info['label'], expected_label(a, b)))
        return True
    right = int(info['pressed']) == r
    if right:
        want = 'CORRECT! %d÷%d=%d r%d' % (a, b, q, r)
        ok = info['fb'] == want and 'correct' in info['cls'].split() and info['score'] == 10
    else:
        want = 'WRONG! %d÷%d=%d remainder %d' % (a, b, q, r)
        keyb = [c for t, c in info['keycls'] if int(t) == r]
        ok = (info['fb'] == want and 'wrong' in info['cls'].split() and info['score'] == 0 and info['next'] >= 1
              and keyb and 'correct' in keyb[0].split())
    if not ok:
        fails.append('%s: %s, pressing %s reads %r (score %d), expected %r' % (
            'marking' if info['fb'].split('!')[0] != want.split('!')[0] else 'feedback', where, info['pressed'], info['fb'], info['score'], want))
    return True


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {}
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
            page.clock.install()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof generateQ === "function" && typeof loadQuestion === "function"', timeout=15000)
            # free draws: only the 408, and all of them
            seen = page.evaluate(FREE_JS, FREE_DRAWS)['seen']
            want = {'%d,%d' % (a, b) for a in A_RANGE for b in B_RANGE}
            extra = sorted(set(seen) - want)
            missing = sorted(want - set(seen))
            if extra:
                fails.append('range: generateQ drew %d pairs outside a 10..60, b 2..9, e.g. %s' % (len(extra), extra[:3]))
            if missing:
                fails.append('range: %d of the 408 pairs never drawn in %d draws, e.g. %s' % (len(missing), FREE_DRAWS, missing[:3]))
            page.evaluate('() => { startGame(); clearInterval(gameTimer); }')
            page.evaluate(STEER_JS)
            n = 0
            for a in A_RANGE:
                for b in B_RANGE:
                    info = page.evaluate(ONE_JS, [a, b, -1])
                    if not check_one(fails, a, b, info, -1):
                        continue
                    for k in range(len(info['opts'])):
                        check_one(fails, a, b, page.evaluate(ONE_JS, [a, b, k]), k)
                    n += 1
            seq = page.evaluate(SCAFFOLD_JS, [True, True, False, False, True, True])
            want_seq = ['flex', 'flex', 'none', 'none', 'flex', 'flex', 'none']
            if seq != want_seq:
                fails.append('scaffold: shown/hidden over right, right, wrong, wrong, right, right reads %r, expected %r' % (seq, want_seq))
            # a whole session on the clock: right answers until 90 seconds
            page.evaluate('() => { startGame(); }')
            got = 0
            for _ in range(5):
                page.evaluate('() => { const b = [...document.querySelectorAll("#answerRow .choice-btn")].find(x => +x.textContent === currentAns); b.click(); }')
                got += 1
                page.clock.run_for(1300)
            page.clock.run_for(90000)
            end = page.evaluate('() => ({over: document.getElementById("gameOver").classList.contains("visible"), score: document.getElementById("finalScore").textContent, detail: document.getElementById("goDetail").textContent, t: timeLeft})')
            if not end['over'] or end['score'] != str(10 * got) or end['detail'] != '%d correct answers' % got or end['t'] != 0:
                fails.append('session: after %d right answers and 90 seconds the end reads %r' % (got, end))
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'pairs': n}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong key ((a+1) mod b)', 'key:', [("const ans = a % b;", "const ans = (a + 1) % b;")]),
    ('the key offered twice (SR-4/16)', 'options:', [("for(let r = 0; r < mod; r++) { if(r !== correct) wrong.push(r); }",
                                                     "for(let r = 0; r < mod; r++) { wrong.push(r); }")]),
    ('a wrong quotient in the feedback (rounded up)', 'feedback:',
     [("${Math.floor(currentA/currentB)} remainder ${currentAns}", "${Math.ceil(currentA/currentB)} remainder ${currentAns}")]),
    ('the dot grid groups rounded', 'dots:', [("const groups = Math.floor(a / b);", "const groups = Math.round(a / b);")]),
    ('a drawn outside 10..60', 'range:', [("const a = randInt(10, 60);", "const a = randInt(10, 61);")]),
    ('the scaffold never withdraws', 'scaffold:', [("if(scaffoldCorrect >= 2) scaffoldOn = false;", "if(scaffoldCorrect >= 99) scaffoldOn = false;")]),
    ('a low guess marked right', 'marking:', [("  if(val === currentAns) {\n    score += 10;", "  if(val <= currentAns) {\n    score += 10;")]),
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
    print('%s: %d of 408 questions driven through the game\'s generator, each key, option set, dot grid and feedback recomputed and '
          'every option pressed in Chromium; %d free draws; the scaffold and a 90-second session checked' % (SLUG, st.get('pairs', 0), FREE_DRAWS))
    print('  not asserted (open): the 60-second wording (t4-001), portal and spec map (t4-002, t4-003), the scaffold showing the answer (t4-004)')
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-58s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            found = [f for f in rep if f.startswith(tag) or (' ' + tag) in f]
            ok = ok and bool(found)
            print('  self-test %-58s %s' % (what, ('caught: ' + found[0][:100]) if found else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
