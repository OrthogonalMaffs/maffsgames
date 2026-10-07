#!/usr/bin/env python3
# ci-line: E | Eigenvector Engine (every key an eigenvector, no option a multiple of one or of another; working recomputed; every option clicked) |
"""Eigenvector Engine: every key recomputed, every option checked against SR-17, every worked solution recomputed.

The tranche 6 audit (6 Oct 2026) found QS[16] (:122) with a lambda that is not an eigenvalue of its matrix and a
worked solution for another one (t6-001); distractors that are themselves eigenvectors, so a right answer was marked
wrong (t6-001 :117 and :128, t6-005, f0-005: SR-17, "a scalar multiple of an eigenvector is never a wrong option");
wrong options that are sign twins of each other (f0-001..007); "symmetric matrices always have orthogonal
eigenvectors", true only for different eigenvalues (t6-005); worked steps that lose their spaces in KaTeX (t6-004);
and a CSS-only lock, so Enter re-scored an answer (t6-002). Project Claude replaced QS[16] (7 Oct 2026):
A = [[6, 2], [2, 3]], lambda = 7, key (2, 1).

Keys. lambda is an eigenvalue of A (det(A - lambda I) = 0); the key is a nonzero eigenvector for it, in lowest terms.
Options. No distractor is an eigenvector for lambda (SR-17), and no two options are multiples of each other.
Working. The first line's matrix is A - lambda I; every equation in the working holds at the key; the last line is
  the key. A claim that eigenvectors are orthogonal names different eigenvalues.
Chromium (390x844, KaTeX). Every option of every item is clicked through the game's own handler: the key is marked
  right, every other option wrong with the worked solution shown; the solution's words keep their spaces. With
  MaffsLock's real window: the key clicked, then Enter three times on it, scores once; a wrong answer, then Tab and
  Enter, stays wrong; the end screen submits once.

A self-test plants two of the audit's own faults back (t6-001: the old QS[16]; f0-005-style: (-1, 2) offered as
wrong for QS[11], whose key is (1, -2)); each must FAIL naming its item.

    python scripts/verify-eigenvector-engine.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import re
import sys

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import bank_common as bc  # noqa: E402

SLUG = 'eigenvector-engine'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
X, Y = sp.symbols('x y')

VEC = re.compile(r'\\begin\{pmatrix\}\s*(-?\d+)\s*\\\\\s*(-?\d+)\s*\\end\{pmatrix\}')
MAT = re.compile(r'\\begin\{pmatrix\}\s*(-?\d+)\s*&\s*(-?\d+)\s*\\\\\s*(-?\d+)\s*&\s*(-?\d+)\s*\\end\{pmatrix\}')


def vec(tex):
    m = VEC.fullmatch(tex.strip())
    return sp.Matrix([int(m.group(1)), int(m.group(2))]) if m else None


def parallel(u, v):
    return u[0] * v[1] - u[1] * v[0] == 0


def where(i):
    return 'QS[%d]' % i


def maths(step):
    """A worked line without its prose: the maths inside \\( \\) if delimited, else the whole line."""
    segs = re.findall(r'\\\((.*?)\\\)', step)
    return segs if segs else [step]


def equations(seg):
    """'2x + y = 0 \\Rightarrow y = -2x' -> [(lhs, rhs), ...] as SymPy, where every side reads as maths in x, y."""
    out = []
    for part in re.split(r'\\Rightarrow|\\quad|,', seg):
        sides = part.split('=')
        if len(sides) != 2 or '\\begin' in part or 'mathbf' in part or 'I' in part:
            continue
        try:
            lhs, rhs = (sp.sympify(re.sub(r'(\d)([xy])', r'\1*\2', z.strip())) for z in sides)
        except (sp.SympifyError, SyntaxError, TypeError):
            continue
        if (lhs.free_symbols | rhs.free_symbols) <= {X, Y} and (lhs.free_symbols | rhs.free_symbols):
            out.append((lhs, rhs))
    return out


def check_bank(fails, qs):
    for i, q in enumerate(qs):
        A = sp.Matrix(q['m'])
        lam = sp.Integer(q['lam'])
        M = A - lam * sp.eye(2)
        if M.det() != 0:
            fails.append('%s: lambda = %s is not an eigenvalue of A (det(A - lambda I) = %s; eigenvector-engine-t6-001)' % (
                where(i), lam, M.det()))
            continue
        c = vec(q['c'])
        if c is None or c == sp.zeros(2, 1) or M * c != sp.zeros(2, 1):
            fails.append('%s: the key %s is not an eigenvector for lambda = %s (t6-001)' % (where(i), q['c'], lam))
            continue
        if sp.gcd(c[0], c[1]) != 1:
            fails.append('%s: the key %s is not in lowest terms' % (where(i), list(c)))
        opts = [c] + [vec(d) for d in q['d']]
        if any(o is None for o in opts):
            fails.append('%s: an option does not read as a vector' % where(i))
            continue
        for d in opts[1:]:
            if M * d == sp.zeros(2, 1):
                fails.append('%s: %s is an eigenvector for lambda = %s but is offered as wrong (SR-17; '
                             'eigenvector-engine-t6-001/t6-005/f0-005)' % (where(i), list(d), lam))
        for a in range(len(opts)):
            for b in range(a + 1, len(opts)):
                if a and parallel(opts[a], opts[b]):
                    fails.append('%s: %s and %s are multiples of each other, both offered as wrong (f0)' % (
                        where(i), list(opts[a]), list(opts[b])))
        # the working
        steps = q.get('s') or []
        first = MAT.search(steps[0]) if steps else None
        if not first or sp.Matrix(2, 2, [int(z) for z in first.groups()]) != M:
            fails.append('%s: the first worked line is not A - lambda I = %s' % (where(i), M.tolist()))
        last = VEC.search(steps[-1]) if steps else None
        if not last or sp.Matrix([int(last.group(1)), int(last.group(2))]) != c:
            fails.append('%s: the last worked line is not the key %s' % (where(i), list(c)))
        for st in steps[1:-1]:
            for seg in maths(st):
                for lhs, rhs in equations(seg):
                    if sp.simplify((lhs - rhs).subs({X: c[0], Y: c[1]})) != 0:
                        fails.append('%s: the worked line %r does not hold at the key %s' % (where(i), st, list(c)))
        if 'orthogonal' in (q.get('mc') or '') and 'different eigenvalues' not in q['mc']:
            fails.append('%s: %r: orthogonal only for different eigenvalues (eigenvector-engine-t6-005)' % (
                where(i), q['mc']))


SWEEP_JS = r"""() => {
  if (window.MaffsLock) MaffsLock.FRESH_MS = 0;
  const out = [];
  const realTimeout = window.setTimeout; window.setTimeout = () => 0;
  try {
    QS.forEach((q, i) => {
      [q.c].concat(q.d).forEach(v => {
        pool = [q, q]; qIdx = 0; total = 0; score = 0; correctN = 0;
        show('game'); nextQ();
        const btn = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === v);
        if (!btn) { out.push([i, v, 'missing']); return; }
        btn.click();
        const sol = document.getElementById('solution');
        const c = sol.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(e => e.remove());
        out.push([i, v, btn.classList.contains('correct') ? 'right' : btn.classList.contains('wrong') ? 'wrong' : 'none',
                  sol.classList.contains('show'), c.textContent, document.documentElement.scrollWidth]);
      });
    });
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""

LOCK_JS = r"""async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const settle = () => wait((window.MaffsLock ? MaffsLock.FRESH_MS : 0) + 50);
  let submits = 0;
  window.MaffsLeaderboard = { submitScore: () => { submits++; return Promise.resolve(); } };
  const res = {};
  const q = QS[2];
  pool = [q, q, q]; qIdx = 0; total = 0; score = 0; correctN = 0;
  show('game'); nextQ();
  await settle();
  let key = [...document.querySelectorAll('#options .opt-btn')].find(b => b.dataset.val === q.c);
  key.click();
  key.focus();
  ['Enter', 'Enter', 'Enter'].forEach(k => {
    key.dispatchEvent(new KeyboardEvent('keydown', { key: k, bubbles: true }));
    key.click();
  });
  res.once = [score > 0, correctN];
  if (window.MaffsLock) MaffsLock.clearTimers();
  qIdx = 1; nextQ();
  await settle();
  const before = correctN;
  const btns = [...document.querySelectorAll('#options .opt-btn')];
  const wrong = btns.find(b => b.dataset.val !== q.c);
  wrong.click();
  key = btns.find(b => b.dataset.val === q.c);
  key.focus(); key.click();
  res.wrongStays = [correctN - before, wrong.classList.contains('wrong')];
  if (window.MaffsLock) MaffsLock.clearTimers();
  endGame(); endGame();
  res.submits = submits;
  return res;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    qs = None
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
            ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            qs = page.evaluate('QS')
            lost = set()
            for row in page.evaluate(SWEEP_JS):
                i, v = row[0], row[1]
                if row[2] == 'missing':
                    fails.append('%s: the option %s is not on screen' % (where(i), v))
                    continue
                mark, shown, text, sw = row[2:]
                want = 'right' if v == qs[i]['c'] else 'wrong'
                if mark != want:
                    fails.append('%s: %s is marked %s' % (where(i), list(vec(v) or [v]), mark))
                if want == 'wrong':
                    if not shown:
                        fails.append('%s: a wrong answer does not show the worked solution' % where(i))
                    m = re.search(r'Row\d|Let[xy]|Rowone|Takerow', text)
                    if m and i not in lost:
                        lost.add(i)
                        fails.append('%s: the worked solution loses its spaces (%r; eigenvector-engine-t6-004)' % (
                            where(i), text[max(0, m.start() - 10):m.end() + 20]))
                if sw > 390:
                    fails.append('%s at 390px: the page scrolls sideways (%dpx)' % (where(i), sw))
            lk = page.evaluate(LOCK_JS)
            if lk['once'][1] != 1:
                fails.append('the key clicked, then Enter three times on it, counted %d times (eigenvector-engine-t6-002)'
                             % lk['once'][1])
            if lk['wrongStays'] != [0, True]:
                fails.append('a wrong answer, then the key clicked, changed the mark (%s; eigenvector-engine-t6-002)'
                             % (lk['wrongStays'],))
            if lk['submits'] != 1:
                fails.append('the end screen submitted %d scores (MaffsLock.finishOnce)' % lk['submits'])
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            ctx.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return qs


PLANTS = [
    ('QS[16]', 't6-001: the old QS[16]',
     "{m:[[6,2],[2,3]],lam:7,", "{m:[[6,2],[1,3]],lam:7,"),
    ('QS[11]', 'SR-17: (-1, 2) offered as wrong for (1, -2)',
     "d:['\\\\begin{pmatrix} 2 \\\\\\\\ 1 \\\\end{pmatrix}','\\\\begin{pmatrix} 2 \\\\\\\\ -1 \\\\end{pmatrix}'",
     "d:['\\\\begin{pmatrix} -1 \\\\\\\\ 2 \\\\end{pmatrix}','\\\\begin{pmatrix} 2 \\\\\\\\ -1 \\\\end{pmatrix}'"),
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
    qs = play(fails, html)
    if qs:
        check_bank(fails, qs)
    print('%s: every key an eigenvector, no option a multiple of one or of another, working recomputed, every option '
          'clicked' % SLUG)
    ok = True
    if not args.no_selftest and not args.against:
        for prefix, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-44s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(prefix)]
            ok = ok and bool(hit)
            print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:100]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
