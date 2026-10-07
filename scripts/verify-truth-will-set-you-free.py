#!/usr/bin/env python3
# ci-line: E | The Truth Will Set You Free (every truth table from its key, distractors not equivalent, scoring by correct cells, MaffsLock) |
"""The Truth Will Set You Free: every truth table recomputed from its key expression; scoring credits correct cells only.

The tranche 6 audit (6 Oct 2026) found every truth-table cell scoring a point whether right or wrong, so an all-zero
table with every expression wrong scored 89% and went to the leaderboard (t6-001); library [12] storing the outputs of
B·D̄ under the key (A·B + C)·D̄, so a correct table was marked 13/16 and "corrected" wrongly (t6-002); library [27]
showing "This expression simplifies to undefined." (t6-003); and the Aa choice never saved (t6-005). The contract
(Jon, 7 Oct 2026): derive the stored outputs from the key expression in code; score correct cells only.

Tables. The page computes every item's table from its key (truthTable()). This script evaluates every expression
  independently (SymPy Boolean algebra, from the same TeX) and requires the page's table to equal it.
Options. The key and each distractor use only the item's inputs; no distractor is equivalent to the key or to another
  distractor; a "simplified" form is equivalent to the key, and an item that links to Boolean Blitz has one.
Chromium (390x844, KaTeX). Every item is played through the game's own handlers: the correct table scores one point a
  cell; an all-zero table scores only the cells whose answer is 0; the key scores 3 and each distractor 0. With
  MaffsLock's real window: a double click on Submit never also clicks Continue; a second option clicked after the
  first is ignored; the results screen submits once. Aa is saved to mfg_accessible and restored on reload.

A self-test plants three of the audit's own faults back (t6-001: a point for every cell; t6-003: [27] without its
simplified form, and [27] written in XOR with no definition); each must FAIL naming its audit item.

[27]'s line after the answer (approved by Project Claude, 7 Oct 2026): XOR is introduced nowhere else in the game, so
the form is "written", not "simplified", with the identity that defines XOR and a gloss: "This expression can be
written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B (XOR: one or the other, but not both). Play Boolean Blitz →".

    python scripts/verify-truth-will-set-you-free.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import itertools
import os
import re
import sys

import sympy as sp
from sympy.logic.boolalg import Equivalent

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import bank_common as bc  # noqa: E402

SLUG = 'truth-will-set-you-free'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')


def to_py(tex):
    """The game's TeX as a Python Boolean expression: \\overline{x} -> ~(x), \\cdot -> &, + -> |, \\oplus -> ^."""
    r = tex
    while '\\overline{' in r:
        a = r.index('\\overline{')
        depth, j = 0, a + len('\\overline')
        while True:
            if r[j] == '{':
                depth += 1
            elif r[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        r = r[:a] + '~(' + r[a + len('\\overline{'):j] + ')' + r[j + 1:]
    r = r.replace('\\cdot', '&').replace('\\oplus', '^').replace('+', '|')
    r = re.sub(r'\s+', '', r)
    # juxtaposition: AB, A(, )A, )(, A~( -> AND
    r = re.sub(r'(?<=[A-Z)])(?=[A-Z(~])', '&', r)
    return r


def parse(tex, inputs):
    syms = {v: sp.Symbol(v) for v in 'ABCDEFGH'}
    e = eval(to_py(tex), {'__builtins__': {}}, syms)  # noqa: S307 (the bank's own expressions)
    extra = {str(z) for z in e.free_symbols} - set(inputs)
    return e, extra


def table(e, inputs):
    syms = [sp.Symbol(v) for v in inputs]
    out = []
    for row in itertools.product([0, 1], repeat=len(inputs)):
        out.append(1 if bool(e.subs(dict(zip(syms, [bool(z) for z in row])))) else 0)
    return out


def equivalent(e1, e2):
    return sp.simplify_logic(Equivalent(e1, e2)) == sp.true


def where(i):
    return 'library[%d]' % i


def check_bank(fails, lib):
    for i, q in enumerate(lib):
        inputs = q['inputs']
        key, extra = parse(q['expr'], inputs)
        if extra:
            fails.append('%s: the key uses %s, not an input' % (where(i), sorted(extra)))
            continue
        want = table(key, inputs)
        if q.get('outputs') != want:
            bad = [k for k, (u, v) in enumerate(zip(q.get('outputs') or [], want)) if u != v]
            fails.append('%s: the table the game marks against is not its key %s (rows %s; '
                         'truth-will-set-you-free-t6-002)' % (where(i), q['expr'], bad[:6]))
        ds = []
        for d in q['distractors']:
            e, extra = parse(d, inputs)
            if extra:
                fails.append('%s: the distractor %s uses %s, not an input' % (where(i), d, sorted(extra)))
            if equivalent(e, key):
                fails.append('%s: the distractor %s is equivalent to the key (SR-4)' % (where(i), d))
            for d0, e0 in ds:
                if equivalent(e, e0):
                    fails.append('%s: the distractors %s and %s are equivalent' % (where(i), d0, d))
            ds.append((d, e))
        if q.get('bbLink') and not q.get('simplified'):
            fails.append('%s: links to Boolean Blitz with no simplified form ("simplifies to undefined"; '
                         'truth-will-set-you-free-t6-003)' % where(i))
        if q.get('simplified'):
            e, extra = parse(q['simplified'], inputs)
            if extra or not equivalent(e, key):
                fails.append('%s: the simplified form %s is not the key %s' % (where(i), q['simplified'], q['expr']))
            # No item's key uses XOR, so a form written with it must define it where it is shown (approved by
            # Project Claude, 7 Oct 2026): an identity whose left side uses XOR, true for every input, and a gloss.
            if '\\oplus' in q['simplified'] and not (q.get('identity') and '\\oplus' in q['identity'][0]):
                fails.append('%s: the form %s uses XOR, which the game never introduces, and does not define it '
                             '(truth-will-set-you-free-t6-003)' % (where(i), q['simplified']))
        if q.get('identity'):
            lhs, x1 = parse(q['identity'][0], inputs)
            rhs, x2 = parse(q['identity'][1], inputs)
            if x1 or x2 or not equivalent(lhs, rhs):
                fails.append('%s: the identity %s = %s is not true' % (where(i), q['identity'][0], q['identity'][1]))
            if not q.get('gloss'):
                fails.append('%s: the identity %s has no gloss in words' % (where(i), q['identity'][0]))


PLAY_JS = r"""() => {
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  QUESTION_LIBRARY.forEach((q, i) => {
    const run = (cells, opt) => {
      QUESTIONS = [q]; qIndex = 0; totalPoints = 0; totalTTCorrect = 0; totalTTCells = 0; exprCorrect = 0;
      document.getElementById('startScreen').style.display = 'none';
      document.getElementById('questionArea').style.display = '';
      loadQuestion();
      cells.forEach((v, k) => { for (let n = 0; n <= v; n++) toggleOutput(k); });
      document.getElementById('submitTT').click();
      const ttPts = totalPoints;
      const line = (document.querySelector('.score-line') || {}).textContent || '';
      document.querySelector('#btnRow button').click();
      const btn = [...document.querySelectorAll('#expressionSection .opt-btn')].find(b => window._exprOpts[+b.dataset.val] === opt);
      btn.click();
      return [ttPts, line, totalPoints - ttPts, document.getElementById('bbLinkSection').textContent,
              document.documentElement.scrollWidth];
    };
    const key = run(q.outputs, q.expr);
    const zeros = run(q.outputs.map(() => 0), q.distractors[0]);
    const others = q.distractors.slice(1).map(d => run(q.outputs, d)[2]);
    out.push([i, key, zeros, others, q.outputs.filter(v => v === 0).length]);
  });
  return out;
}"""

LOCK_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const settle = () => wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 80);
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const q = QUESTION_LIBRARY[0];
  QUESTIONS = [q, q]; qIndex = 0; totalPoints = 0; totalTTCorrect = 0; totalTTCells = 0; exprCorrect = 0;
  document.getElementById('startScreen').style.display = 'none';
  document.getElementById('questionArea').style.display = '';
  loadQuestion();
  await settle();
  q.outputs.forEach((v, k) => { for (let n = 0; n <= v; n++) toggleOutput(k); });
  document.getElementById('submitTT').scrollIntoView({ block: 'center', behavior: 'instant' });
  await wait(100);
  const r = document.getElementById('submitTT').getBoundingClientRect();
  return { x: r.x + r.width / 2, y: r.y + r.height / 2 };
}"""

LOCK2_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const settle = () => wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 80);
  const res = { exprShown: document.getElementById('expressionSection').style.display !== 'none', tt: totalPoints };
  await settle();
  const cont = document.querySelector('#btnRow button');
  if (cont) cont.click();
  await settle();
  const q = QUESTIONS[0];
  const btns = [...document.querySelectorAll('#expressionSection .opt-btn')];
  const wrong = btns.find(b => window._exprOpts[+b.dataset.val] !== q.expr);
  const right = btns.find(b => window._exprOpts[+b.dataset.val] === q.expr);
  if (wrong && right) { wrong.click(); right.click(); }
  res.expr = wrong && right ? [exprCorrect, totalPoints - res.tt] : 'options not on screen';
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  showResults(); showResults();
  res.submits = submits;
  return res;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    lib = None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTION_LIBRARY !== "undefined" && typeof katex !== "undefined"',
                                   timeout=15000)
            # Aa saved and restored (t6-005)
            page.evaluate("localStorage.removeItem('mfg_accessible')")
            page.click('#aaBtn')
            saved = page.evaluate("localStorage.getItem('mfg_accessible')")
            page.reload(wait_until='load')
            page.wait_for_function('typeof QUESTION_LIBRARY !== "undefined" && typeof katex !== "undefined"',
                                   timeout=15000)
            restored = page.evaluate("document.body.classList.contains('accessible-mode')")
            if saved != 'true' or not restored:
                fails.append('Aa is not saved to mfg_accessible and restored (saved %r, restored %s; '
                             'truth-will-set-you-free-t6-005)' % (saved, restored))
            lib = page.evaluate('QUESTION_LIBRARY')
            for i, key, zeros, others, nzero in page.evaluate(PLAY_JS):
                n = len(lib[i]['outputs'])
                w = where(i)
                if key[0] != n or '%d / %d' % (n, n) not in key[1]:
                    fails.append('%s: the correct table scores %d of %d (%r)' % (w, key[0], n, key[1]))
                if zeros[0] != nzero:
                    fails.append('%s: an all-zero table scores %d; only its %d zero cells are right '
                                 '(truth-will-set-you-free-t6-001)' % (w, zeros[0], nzero))
                if key[2] != 3 or zeros[2] != 0 or any(o != 0 for o in others):
                    fails.append('%s: the expression scores key %d, distractors %s (want 3 and 0)' % (
                        w, key[2], [zeros[2]] + others))
                if 'undefined' in key[3]:
                    fails.append('%s: %r (truth-will-set-you-free-t6-003)' % (w, key[3].strip()))
                q = lib[i]
                if q.get('bbLink') and q.get('identity'):
                    want = ('This expression can be written', ', where', '(%s). Play Boolean Blitz →' % q.get('gloss'))
                    if not (key[3].strip().startswith(want[0]) and all(s in key[3] for s in want[1:])):
                        fails.append('%s: the line after the answer reads %r, not the approved "This expression can '
                                     'be written ..., where ... (%s). Play Boolean Blitz →"' % (w, key[3].strip(), q.get('gloss')))
                if key[4] > 390:
                    fails.append('%s at 390px: the page scrolls sideways (%dpx)' % (w, key[4]))
            if page.evaluate('typeof MaffsLock') != 'undefined':
                page.evaluate('MaffsLock.FRESH_MS = 300')
            pt = page.evaluate(LOCK_JS)
            page.mouse.click(pt['x'], pt['y'])
            page.mouse.click(pt['x'], pt['y'])
            lk = page.evaluate(LOCK2_JS)
            if lk['exprShown']:
                fails.append('a double click on Submit also clicked Continue (MaffsLock)')
            if lk['expr'] != [0, 0]:
                fails.append('a wrong option, then the key: exprCorrect, points = %s, not [0, 0] (MaffsLock)' % lk['expr'])
            if lk['submits'] != 1:
                fails.append('the results screen submitted %d scores (MaffsLock.finishOnce)' % lk['submits'])
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return lib


PLANTS = [
    ('library', 't6-001: a point for every cell',
     """      correct++;
      totalPoints++;
    } else {""", """      correct++;
    } else {
      totalPoints++;"""),
    ('library[27]', 't6-003: [27] without its simplified form',
     "bbLink: 'BB Q12', simplified: '(A \\\\oplus B) \\\\cdot C \\\\cdot D \\\\cdot \\\\overline{E}'", "bbLink: 'BB Q12'"),
    ('library[27]', 't6-003: [27] in XOR with no definition',
     ",\n    identity: ['A \\\\oplus B', 'A \\\\cdot \\\\overline{B} + \\\\overline{A} \\\\cdot B'], gloss: 'XOR: one or the other, but not both'",
     ""),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    lib = play(fails, html)
    if lib:
        check_bank(fails, lib)
    print('%s: every table from its key, distractors not equivalent, scoring by correct cells, MaffsLock' % SLUG)
    ok = True
    if not args.no_selftest and not args.against:
        for prefix, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-42s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(prefix)]
            ok = ok and bool(hit)
            print('  self-test %-42s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
