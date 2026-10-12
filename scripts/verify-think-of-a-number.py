#!/usr/bin/env python3
# ci-line: Think of a Number (every item run forwards from its answer and backwards from its result, undo working recomputed, typed answers marked in Chromium) |
"""Think of a Number: "I think of a number... [one to three steps]. My answer is R. What was my number?"

A static bank, QUESTIONS = {oneStep, twoStep, threeStep} (50 items), read from the page as served. Each item holds the
steps ({operation, value, display}), the result R, the key (the number thought of) and undoSteps (the working shown
after a wrong answer). The student types a whole number on the numpad; the mark is an exact match.

Checks, independent of the game's code:
  Items: ids unique; one, two or three steps in the right list; each step an add, subtract, multiply or divide whose
    display reads exactly "I add V", "I subtract V", "I multiply it by V" or "I divide it by V".
  Key: starting from the key, every step run forwards with fractions.Fraction gives the result R; every intermediate is
    a whole number from 0 up (so a Year 6 student never meets a fraction or a negative), and the key is 1 to 9999 (the
    input takes four digits). Run backwards from R, the inverse of each step gives the same key, so the key is unique.
  Working: undoSteps has one line per step, last step first, each "A op B = C" with the inverse operation (add undone by
    subtract, and so on), B the step's value, A the running figure and C the next; the chain ends on the key. Minus, divide
    and times use the signs the game prints (U+2212, U+00F7, U+00D7).
  Sessions: buildQuestionSet(10), (20) and (30) give the 2/4/4, 4/8/8 and 6/12/12 split of one, two and three steps,
    every item different, all from the bank (three draws each).
  Marking, in Chromium (390x844), every item shown by the game's own showQuestion(): the puzzle text is "I think of a
    number...", each step's display and "My answer is R. What was my number?". The key typed on the numpad and Enter reads
    "Correct!" and "The number was K."; each of these wrong answers reads "Not quite" with the working
    "My answer was R.", "Undo: ..." for each line and "The number was K.": the result itself, the key plus and minus one,
    the result with every step run forwards again (the student who does not undo), and the steps undone in the order
    they were told (the student who does not reverse them), whichever of those differ from the key.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong key (9 for the first item), a wrong answer
marked right (within 1 of the key), a wrong undo figure (14 − 6 = 9) and a wrong step display (I add 7 for I add 6).

    python scripts/verify-think-of-a-number.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'think-of-a-number'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LISTS = (('oneStep', 1), ('twoStep', 2), ('threeStep', 3))
SPLITS = {10: (2, 4, 4), 20: (4, 8, 8), 30: (6, 12, 12)}
DEALS = 3
SIGN = {'add': '+', 'subtract': '−', 'multiply': '×', 'divide': '÷'}
INVERSE = {'add': 'subtract', 'subtract': 'add', 'multiply': 'divide', 'divide': 'multiply'}
DISPLAY = {'add': 'I add %d', 'subtract': 'I subtract %d', 'multiply': 'I multiply it by %d', 'divide': 'I divide it by %d'}


def apply(op, x, v):
    return {'add': x + v, 'subtract': x - v, 'multiply': x * v, 'divide': Fraction(x) / v}[op]


def run_forward(x, steps):
    out = [Fraction(x)]
    for s in steps:
        out.append(apply(s['operation'], out[-1], s['value']))
    return out


def undo_lines(result, steps):
    """The working a student should see: the steps undone last to first, with the running figure."""
    lines, cur = [], Fraction(result)
    for s in reversed(steps):
        inv = INVERSE[s['operation']]
        nxt = apply(inv, cur, s['value'])
        lines.append('%d %s %d = %d' % (cur, SIGN[inv], s['value'], nxt))
        cur = nxt
    return lines, cur


def check_items(fails, bank):
    ids = set()
    for name, n in LISTS:
        for q in bank[name]:
            where = '%s %s' % (name, q['id'])
            if q['id'] in ids:
                fails.append('%s: id repeated' % where)
            ids.add(q['id'])
            if len(q['steps']) != n:
                fails.append('%s: %d steps in the %s list' % (where, len(q['steps']), name))
                continue
            for s in q['steps']:
                if s['operation'] not in DISPLAY or not isinstance(s['value'], int) or s['value'] < 1:
                    fails.append('%s: odd step %r' % (where, s))
                elif s['display'] != DISPLAY[s['operation']] % s['value']:
                    fails.append('%s: step reads %r, should read %r' % (where, s['display'], DISPLAY[s['operation']] % s['value']))
            if any(s['operation'] not in DISPLAY for s in q['steps']):
                continue
            chain = run_forward(q['answer'], q['steps'])
            if chain[-1] != q['result']:
                fails.append('%s: %s run forwards from the key %s gives %s, not the result %s' % (
                    where, [s['display'] for s in q['steps']], q['answer'], chain[-1], q['result']))
            if any(v.denominator != 1 or v < 0 for v in chain):
                fails.append('%s: the chain %s leaves the whole numbers from 0 up' % (where, [str(v) for v in chain]))
            if not 1 <= q['answer'] <= 9999:
                fails.append('%s: key %r outside 1 to 9999' % (where, q['answer']))
            lines, back = undo_lines(q['result'], q['steps'])
            if back != q['answer']:
                fails.append('%s: undone from the result gives %s, not the key %s' % (where, back, q['answer']))
            if list(q['undoSteps']) != lines:
                fails.append('%s: undoSteps %r, recomputed %r' % (where, q['undoSteps'], lines))


def wrong_answers(q):
    key = q['answer']
    out = {'the result itself': Fraction(q['result']), 'key + 1': Fraction(key + 1), 'key - 1': Fraction(key - 1)}
    fwd = Fraction(q['result'])
    for s in q['steps']:
        fwd = apply(s['operation'], fwd, s['value'])
    out['steps run forwards again'] = fwd
    cur = Fraction(q['result'])
    for s in q['steps']:                 # undone first step first: the order told, not reversed
        cur = apply(INVERSE[s['operation']], cur, s['value'])
    out['steps undone in the order told'] = cur
    return {k: v for k, v in out.items() if v != key and v.denominator == 1 and 0 <= v <= 9999}


MARK_JS = r"""(args) => {
  const [q, typed] = args;
  currentQuestions = [q]; currentIndex = 0; correctCount = 0; stats = {oneStep:{total:0,correct:0},twoStep:{total:0,correct:0},threeStep:{total:0,correct:0}};
  showScreen('gameScreen');
  showQuestion();
  const puzzle = [...document.querySelectorAll('#puzzleSteps li')].map(li => li.textContent);
  for (const ch of typed) document.querySelector('#numpad [data-val="' + ch + '"]').click();
  document.querySelector('#numpad [data-val="enter"]').click();
  MaffsLock.clearTimers();
  return {puzzle: puzzle, title: document.getElementById('feedbackTitle').textContent,
          body: document.getElementById('feedbackBody').innerText, correct: correctCount};
}"""
SESSION_JS = r"""() => { const out = {};
  for (const n of [10, 20, 30]) { out[n] = [];
    for (let k = 0; k < %d; k++) out[n].push(buildQuestionSet(n).map(q => q.id)); }
  return out; }""" % DEALS


def mark_all(fails, page, bank):
    for name, n in LISTS:
        for q in bank[name]:
            key = q['answer']
            lines, _ = undo_lines(q['result'], q['steps'])
            cases = [('the key', key, True)] + [(k, v, False) for k, v in wrong_answers(q).items()]
            for what, val, right in cases:
                got = page.evaluate(MARK_JS, [q, str(int(val))])
                where = '%s %s, %s typed (%s)' % (name, q['id'], what, int(val))
                puz = got['puzzle']
                exp = ['"I think of a number..."'] + [s['display'] + '.' for s in q['steps']] + [
                    'My answer is %d. What was my number?' % q['result']]
                if puz != exp:
                    fails.append('%s: puzzle reads %r, expected %r' % (where, puz, exp))
                if right:
                    if not (got['title'] == 'Correct!' and got['correct'] == 1 and 'The number was %d.' % key in got['body']):
                        fails.append('%s: the key was not marked right (%r)' % (where, got))
                else:
                    body = [l.strip() for l in got['body'].split('\n') if l.strip()]
                    expb = ['Working backwards:', 'My answer was %d.' % q['result']] + ['Undo: ' + l for l in lines] + [
                        'The number was %d.' % key]
                    if not (got['title'] == 'Not quite' and got['correct'] == 0 and body == expb):
                        fails.append('%s: a wrong answer was not marked wrong with the recomputed working (%r; expected %r)' % (
                            where, got, expb))


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    bank = None
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
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof buildQuestionSet === "function"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            check_items(fails, bank)
            kind = {q['id']: n for name, n in LISTS for q in bank[name]}
            counts = page.evaluate("() => [...document.querySelectorAll('.session-btn')].map(b => +b.dataset.count)")
            if sorted(counts) != sorted(SPLITS):
                fails.append('session buttons offer %r, expected %r' % (counts, sorted(SPLITS)))
            for n, deals in page.evaluate(SESSION_JS).items():
                for d in deals:
                    split = tuple(sum(1 for i in d if kind.get(i) == k) for k in (1, 2, 3))
                    if len(d) != int(n) or len(set(d)) != len(d) or split != SPLITS[int(n)] or not set(d) <= set(kind):
                        fails.append('a %s-question session is %r (split %r, expected %r)' % (n, d, split, SPLITS[int(n)]))
            mark_all(fails, page, bank)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return bank


PLANTS = [
    ('a wrong key (9 for the first item)', 'run forwards from the key',
     [("result:14,answer:8,", "result:14,answer:9,")]),
    ('a wrong answer marked right (within 1 of the key)', 'was not marked wrong',
     [('const isCorrect = userAnswer === q.answer;', 'const isCorrect = Math.abs(userAnswer - q.answer) <= 1;')]),
    ('a wrong undo figure (14 - 6 = 9)', 'undoSteps',
     [("undoSteps:['14 \\u2212 6 = 8']", "undoSteps:['14 \\u2212 6 = 9']")]),
    ('a wrong step display (I add 7 for I add 6)', 'step reads',
     [("display:'I add 6'},{operation:'multiply',value:3", "display:'I add 7'},{operation:'multiply',value:3")]),
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
    print('%s: %s items recomputed forwards and backwards; each marked with the key and recomputed wrong answers in '
          'Chromium' % (SLUG, ' + '.join('%d %s' % (len(bank[n]), n) for n, _ in LISTS) if bank else '0'))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-52s *** CANNOT PLANT (%r) ***' % (what, bad[0]))
                ok = False
                continue
            planted = html
            for o, n in edits:
                planted = planted.replace(o, n)
            rep = []
            play(rep, planted)
            hit = [f for f in rep if tag in f]
            ok = ok and bool(hit)
            print('  self-test %-52s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails[:40]:
        print('FAIL  ' + f[:500])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
