#!/usr/bin/env python3
# ci-line: Formula Plug-In (every formula, substitution and step of the working recomputed; every item answered right and wrong in Chromium) |
"""Formula Plug-In: "A = l x w, l = 8, w = 5. What is A?", a typed whole number, the working shown after a miss.

A static bank, QUESTIONS (50 items), read from the page as served. Each item names a formula (formulaName,
formulaKatex), its variables and values, the variable asked for (resultVar), the key and the working steps shown
after a wrong answer (KaTeX, one line per step). The mark is an exact match on the typed number.

Checks, independent of the game's code:
  Formula: the item's name is one of ten known formulas (rectangle area and perimeter, triangle area, speed, distance,
    square perimeter and area, cuboid volume, cost, mean), each with its variables in order and its result variable.
    The key is that formula worked out from the item's own values with fractions.Fraction (this file's table, never the
    game's), and is a whole number.
  Formula text: formulaKatex is read as maths (\\times, \\div, \\tfrac{1}{2}, 2(l + w), 4s, s^2, \\text{Sum}) and, with
    the item's values put in, gives the key; its left-hand side is the result variable.
  Working: the first step is the formula as printed; every later step has the same left-hand side and a right-hand side
    worth exactly the key; the second step uses the item's values and the formula's own numbers and no others (the
    numbers in it are those in the formula plus the variables' values); the last step is "LHS = key".
  Bank: ids unique; no formula with the same values twice.
  Sessions: startGame() at 10, 20 and 30 (three draws each) deals that many different items from the bank.
  Chromium (390x844, KaTeX served from the pinned local copy), every item shown by the game's own loadQuestion(): the
    formula card's TeX (read from KaTeX's own annotation) is formulaKatex, the variables line is "l = 8, w = 5", and the
    prompt "What is A?". The key typed on the numpad and submitted reads "Correct!" and is counted; each wrong answer
    (the key plus and minus one, and the answer a student gets from the usual slip: adding for multiplying, dropping the
    half, multiplying for adding, squaring for doubling, and so on, where it differs from the key) reads "Not quite - the
    answer is [key]" and is not counted, and its working steps shown are the item's, each as the TeX of a KaTeX line.
  Header (formula-plug-in-t3-005; Jon's ruling, 19 Oct 2026): in a 10-question session played right, wrong, right, the
    header reads "Q{n} of {N} · {right} right": n the question on screen, N the session length, right this file's own
    count of right answers. Read at Q1 before any answer, after each answer and when the next question is shown (Q1 of
    10 · 0 right, Q1 of 10 · 1 right, Q2 of 10 · 1 right, ...).
No analytics or leaderboard request leaves the stub server (every other request is aborted).

A self-test plants faults in a copy of the page and each must FAIL: a wrong key (the first rectangle area 41), a wrong
answer marked right (within 1 of the key), a wrong working figure (A = 8 x 5 changed to 8 x 6) and a wrong formula
text (the triangle's half dropped), the Mean prompt, the header counting answers given as right, and the header's
question number off by one (t3-005 follow-up).

    python scripts/verify-formula-plug-in.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys
from collections import Counter
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'formula-plug-in'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
SESSIONS = (10, 20, 30)
DEALS = 3
# name: (variables in order, result variable, the formula worked out by this file)
FORMULAS = {
    'Area of a rectangle': (['l', 'w'], 'A', lambda v: v['l'] * v['w']),
    'Perimeter of a rectangle': (['l', 'w'], 'P', lambda v: 2 * (v['l'] + v['w'])),
    'Area of a triangle': (['b', 'h'], 'A', lambda v: F(1, 2) * v['b'] * v['h']),
    'Speed': (['D', 'T'], 'S', lambda v: v['D'] / v['T']),
    'Distance': (['S', 'T'], 'D', lambda v: v['S'] * v['T']),
    'Perimeter of a square': (['s'], 'P', lambda v: 4 * v['s']),
    'Area of a square': (['s'], 'A', lambda v: v['s'] ** 2),
    'Volume of a cuboid': (['l', 'w', 'h'], 'V', lambda v: v['l'] * v['w'] * v['h']),
    'Cost': (['n', 'p'], 'C', lambda v: v['n'] * v['p']),
    'Mean': (['Sum', 'n'], 'Mean', lambda v: v['Sum'] / v['n']),
}
# The usual slips, per formula: a wrong answer a student could plausibly type.
SLIPS = {
    'Area of a rectangle': {'adds instead of multiplying': lambda v: v['l'] + v['w']},
    'Perimeter of a rectangle': {'adds without doubling': lambda v: v['l'] + v['w'],
                                 'multiplies (area)': lambda v: v['l'] * v['w']},
    'Area of a triangle': {'forgets the half': lambda v: v['b'] * v['h'], 'adds': lambda v: v['b'] + v['h']},
    'Speed': {'multiplies': lambda v: v['D'] * v['T'], 'divides the wrong way': lambda v: F(v['T'], v['D'])},
    'Distance': {'adds': lambda v: v['S'] + v['T'], 'divides': lambda v: v['S'] / v['T']},
    'Perimeter of a square': {'squares': lambda v: v['s'] ** 2, 'doubles': lambda v: 2 * v['s']},
    'Area of a square': {'doubles': lambda v: 2 * v['s'], 'four times': lambda v: 4 * v['s']},
    'Volume of a cuboid': {'adds': lambda v: v['l'] + v['w'] + v['h'], 'two sides only': lambda v: v['l'] * v['w']},
    'Cost': {'adds': lambda v: v['n'] + v['p']},
    'Mean': {'multiplies': lambda v: v['Sum'] * v['n'], 'subtracts': lambda v: v['Sum'] - v['n']},
}


def to_python(rhs):
    s = re.sub(r'\\text\{(\w+)\}', r'\1', rhs)
    s = s.replace('\\tfrac{1}{2}', '(1/2)').replace('\\times', '*').replace('\\div', '/')
    s = re.sub(r'\^(\d+)', r'**\1', s)
    s = re.sub(r'(\d)\s*([A-Za-z(])', r'\1*\2', s)
    return re.sub(r'(?<![A-Za-z_])(\d+)', r'F(\1)', s)


def value(rhs, env):
    return eval(to_python(rhs), {'__builtins__': {}, 'F': F}, {k: F(v) for k, v in env.items()})


def split_step(step):
    lhs, _, rhs = step.partition(' = ')
    return lhs.strip(), rhs.strip()


def numbers(rhs):
    return Counter(re.findall(r'(?<![A-Za-z_])\d+', re.sub(r'\\text\{\w+\}', '', rhs)))


def check_item(fails, q):
    where = '%s (%s)' % (q['id'], q['formulaName'])
    if q['formulaName'] not in FORMULAS:
        fails.append('%s: formula not known to this verifier' % where)
        return
    names, resvar, fn = FORMULAS[q['formulaName']]
    vs = q['variables']
    if [v['name'] for v in vs] != names or q['resultVar'] != resvar:
        fails.append('%s: variables %r / result %r, expected %r / %r' % (
            where, [v['name'] for v in vs], q['resultVar'], names, resvar))
        return
    env = {v['name']: F(v['value']) for v in vs}
    key = fn(env)
    if key.denominator != 1:
        fails.append('%s: the formula gives %s, not a whole number' % (where, key))
    if F(q['answer']) != key:
        fails.append('%s: keyed %s, recomputed %s' % (where, q['answer'], key))
    steps = q['workingSteps']
    lhs, rhs = split_step(q['formulaKatex'])
    fl = lhs
    if lhs != ('\\text{Mean}' if resvar == 'Mean' else resvar):
        fails.append('%s: the formula text starts %r, not the result variable' % (where, lhs))
    try:
        if value(rhs, env) != key:
            fails.append('%s: formula text %r with the values gives %s, not %s' % (where, q['formulaKatex'], value(rhs, env), key))
    except Exception as e:
        fails.append('%s: formula text %r could not be read: %s' % (where, q['formulaKatex'], e))
        return
    if not steps or steps[0] != q['formulaKatex']:
        fails.append('%s: the first working step is not the formula as printed' % where)
    for i, st in enumerate(steps[1:], 2):
        l2, r2 = split_step(st)
        if l2 != fl:
            fails.append('%s: step %d starts %r, expected %r' % (where, i, l2, fl))
        try:
            if value(r2, {}) != key:
                fails.append('%s: step %d (%s) is worth %s, not the key %s' % (where, i, st, value(r2, {}), key))
        except Exception as e:
            fails.append('%s: step %d (%s) could not be read: %s' % (where, i, st, e))
    if len(steps) >= 2:
        want = numbers(rhs) + Counter(str(v['value']) for v in vs)
        got = numbers(split_step(steps[1])[1])
        if got != want:
            fails.append('%s: the substitution step %r uses the numbers %s, expected %s' % (
                where, steps[1], dict(got), dict(want)))
    if steps and steps[-1] != '%s = %s' % (fl, q['answer']):
        fails.append('%s: the last step is %r, not "%s = %s"' % (where, steps[-1], fl, q['answer']))


def check_bank(fails, bank):
    ids, seen = set(), set()
    for q in bank:
        if q['id'] in ids:
            fails.append('%s: id repeated' % q['id'])
        ids.add(q['id'])
        k = (q['formulaName'], tuple(v['value'] for v in q['variables']))
        if k in seen:
            fails.append('%s: the same formula and values appear twice' % q['id'])
        seen.add(k)
        check_item(fails, q)


def wrong_answers(q):
    names, _, fn = FORMULAS[q['formulaName']]
    env = {v['name']: F(v['value']) for v in q['variables']}
    key = fn(env)
    out = {'key + 1': key + 1, 'key - 1': key - 1}
    for what, f in SLIPS[q['formulaName']].items():
        out[what] = F(f(env))
    return {k: v for k, v in out.items() if v != key and v.denominator == 1 and 0 <= v < 10 ** 7}


MARK_JS = r"""(args) => {
  const [q, typed] = args;
  sessionQuestions = [q]; currentIndex = 0; correctCount = 0; revealShown = false;
  showScreen('gameScreen');
  loadQuestion();
  const tex = el => [...el.querySelectorAll('annotation')].map(a => a.textContent);
  const shown = {formula: tex(document.getElementById('formulaKatex')), vars: document.getElementById('varsLine').textContent,
                 prompt: document.getElementById('questionPrompt').textContent,
                 name: document.getElementById('formulaName').textContent};
  for (const ch of typed) numInput(ch);
  submitAnswer();
  MaffsLock.clearTimers();
  return {shown: shown, count: correctCount, ind: document.getElementById('feedbackIndicator').textContent.trim(),
          ws: [...document.querySelectorAll('#workingSteps > div')].map(d => tex(d).join('')),
          wsShown: document.getElementById('workingSteps').style.display};
}"""
SCORE_JS = r"""(plan) => {
  const slot = () => document.querySelector('.score-display').textContent;
  selectSession(10); startGame(); MaffsLock.clearTimers();
  const out = [['Q1 shown', slot()]];
  plan.forEach((right, i) => {
    const q = sessionQuestions[currentIndex];
    for (const ch of String(right ? q.answer : q.answer + 1)) numInput(ch);
    submitAnswer(); MaffsLock.clearTimers();
    out.push(['after answer ' + (i + 1), slot()]);
    nextQuestion(); MaffsLock.clearTimers();
    out.push(['Q' + (i + 2) + ' shown', slot()]);
  });
  return out;
}"""
SCORE_PLAN = [True, False, True]
DEAL_JS = r"""() => { const out = {};
  for (const n of %s) { out[n] = []; selectSession(n);
    for (let k = 0; k < %d; k++) { startGame(); out[n].push(sessionQuestions.map(q => q.id)); MaffsLock.clearTimers(); } }
  return out; }""" % (list(SESSIONS), DEALS)


def mark_all(fails, page, bank):
    for q in bank:
        names, resvar, fn = FORMULAS[q['formulaName']]
        env = {v['name']: F(v['value']) for v in q['variables']}
        key = fn(env)
        cases = [('the key', key, True)] + [(k, v, False) for k, v in wrong_answers(q).items()]
        for what, val, right in cases:
            got = page.evaluate(MARK_JS, [q, str(int(val))])
            where = '%s, %s typed (%s)' % (q['id'], what, int(val))
            sh = got['shown']
            wantvars = ', '.join('%s = %s' % (v['name'], v['value']) for v in q['variables'])
            if sh['formula'] != [q['formulaKatex']] or sh['vars'] != wantvars or sh['prompt'] != 'What is %s?' % (q['resultVar'] if len(q['resultVar']) == 1 else 'the ' + q['resultVar'].lower()) \
                    or sh['name'] != q['formulaName']:
                fails.append('%s: the question shows %r' % (where, sh))
            if right:
                if not (got['ind'] == 'Correct!' and got['count'] == 1):
                    fails.append('%s: the key was not marked right (%r)' % (where, got))
            else:
                if not (got['ind'].startswith('Not quite') and got['ind'].endswith('the answer is %d' % key)
                        and got['count'] == 0 and got['ws'] == q['workingSteps']):
                    fails.append('%s: a wrong answer was not marked wrong with the verified answer and working (%r)' % (
                        where, got))


def check_score_slot(fails, page):
    got = page.evaluate(SCORE_JS, SCORE_PLAN)
    head = lambda n, right: 'Q%d of 10 · %d right' % (n, right)
    want, right = [('Q1 shown', head(1, 0))], 0
    for i, r in enumerate(SCORE_PLAN):
        right += r
        want += [('after answer %d' % (i + 1), head(i + 1, right)), ('Q%d shown' % (i + 2), head(i + 2, right))]
    for (w, g) in zip(want, got):
        if tuple(g) != w:
            fails.append('header: at %s it reads %r, expected %r (question on screen of session length, right answers; t3-005 follow-up)' % (
                w[0], g[1], w[1]))


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
            ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)   # KaTeX from the pinned local copy
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            check_bank(fails, bank)
            ids = {q['id'] for q in bank}
            for n, deals in page.evaluate(DEAL_JS).items():
                for d in deals:
                    if len(d) != min(int(n), len(bank)) or len(set(d)) != len(d) or not set(d) <= ids:
                        fails.append('a %s-question session is not that many different bank items: %r' % (n, d[:5]))
            mark_all(fails, page, bank)
            check_score_slot(fails, page)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return bank


PLANTS = [
    ('a wrong key (the first rectangle area 41)', 'keyed',
     [("variables:[{name:'l',value:8},{name:'w',value:5}],resultVar:'A',answer:40", "variables:[{name:'l',value:8},{name:'w',value:5}],resultVar:'A',answer:41")]),
    ('a wrong answer marked right (within 1 of the key)', 'not marked wrong',
     [('const isCorrect = userAnswer === q.answer;', 'const isCorrect = Math.abs(userAnswer - q.answer) <= 1;')]),
    ('a wrong working figure (8 x 5 changed to 8 x 6)', 'step',
     [("'A = 8 \\\\times 5','A = 40'", "'A = 8 \\\\times 6','A = 40'")]),
    ('a wrong formula text (the triangle half dropped)', 'formula text',
     [("formulaKatex:'A = \\\\tfrac{1}{2} \\\\times b \\\\times h',variables:[{name:'b',value:6}", "formulaKatex:'A = b \\\\times h',variables:[{name:'b',value:6}")]),
    ('the Mean prompt "What is Mean?" (R1, formula-plug-in-s1-001)', 'the question shows',
     [("'What is ' + (q.resultVar.length > 1 ? 'the ' + q.resultVar.toLowerCase() : q.resultVar) + '?';", "'What is ' + q.resultVar + '?';")]),
    ('the header counting answers given as right (t3-005 follow-up)', 'header:',
     [("document.getElementById('scoreNum').textContent = correctCount;", "document.getElementById('scoreNum').textContent = currentIndex + 1;")]),
    ('the header question number off by one (t3-005 follow-up)', 'header:',
     [("document.getElementById('qNum').textContent = currentIndex + 1;", "document.getElementById('qNum').textContent = currentIndex;")]),
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
    print('%s: %d items recomputed (formula, key, substitution, every working step); each answered right and wrong in '
          'Chromium; sessions of %s dealt %d times' % (SLUG, len(bank or []), '/'.join(map(str, SESSIONS)), DEALS))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            bad = [o for o, n in edits if html.count(o) != 1]
            if bad:
                print('  self-test %-52s *** CANNOT PLANT (%r) ***' % (what, bad[0][:60]))
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
        print('FAIL  ' + f[:400])
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
