#!/usr/bin/env python3
# ci-line: Characteristic Quest (every 2x2 characteristic equation recomputed from its matrix in SymPy; every option classified; every worked line, trace, determinant and eigenvalue claim checked; every option pressed in Chromium) |
"""Characteristic Quest: given a 2x2 matrix A, pick its characteristic equation from four options.

Static bank, read from the page as served: `QS`, 26 items `{m: [[a, b], [c, d]], c: key, d: [3 distractors], s: worked lines,
mc?: a note}`, 15 a session. The mark is `button.dataset.val === q.c`; a wrong answer shows the worked lines.

Checks, independent of the game's code (SymPy; the TeX is read by a small reader here, Jon's ruling of 12 Oct 2026 allowing a
verifier its own reader until bank_common has an exact one; \\lambda is the unknown):
  Key: the key equation, moved to one side, is det(A - lambda I) = lambda^2 - (a + d) lambda + (ad - bc), worked out here from
    the matrix.
  Options: four different strings; no distractor is the characteristic equation (no option is a multiple of it, SR-4/SR-16).
  Worked lines: every expression in a line, between '=' signs (after any lead-in such as "Upper triangular:"), equals
    det(A - lambda I) or is 0; "Trace = t" and "Det = ... = d" are the matrix's; every eigenvalue a line or note names
    ("lambda = 3", "lambda = \\pm i", "Repeated lambda = 4") is a root, and "A \\neq 4I" is true; a note's own sum ("(4−6 = −2)")
    is true.
  Render: KaTeX (pinned local copy) parses every option and worked line, and the matrix shown is the item's.
  Sessions: startGame() dealt five times: 15 different items from the bank.
  Marking, in Chromium (390x844), through the game's own buttons: every item, every option pressed: the key is marked correct and
    scores; any other is marked wrong, the key shown, the worked solution shows the item's lines, Next mounted.
Fixed in this PR (SR-6, wording and key agree): item 22's line "\\lambda^2 - (0) - (0 - 4) = \\lambda^2 - 4" read +4, not -4; it now
reads "\\lambda^2 - (0)\\lambda + (0 - 4)" (characteristic-quest-t6-003).
Not asserted (open findings, left open): 15 of 26 served (t6-002), prose lines losing spaces in KaTeX (t6-004), ?level and the
rotation note (t6-005).

    python scripts/verify-characteristic-quest.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'characteristic-quest'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
L = sp.Symbol('L')


def read(tex):
    """A TeX polynomial in lambda as SymPy: \\lambda, numbers, + - ( ), ^, juxtaposition multiplies."""
    t = tex.replace('\\lambda', ' L ').replace('−', '-').replace('\\left', '').replace('\\right', '')
    t = re.sub(r'\^\{([^}]*)\}', r'**(\1)', t).replace('^', '**')
    if re.search(r'[^0-9L+\-*/() .]', t):
        raise ValueError('cannot read %r' % tex)
    t = re.sub(r'(\d|\))\s*(L|\()', r'\1*\2', t)
    t = re.sub(r'(L)\s*(\(|\d)', r'\1*\2', t)
    t = re.sub(r'\)\s*\(', ')*(', t)
    return sp.expand(sp.sympify(t, locals={'L': L}))


def charpoly(m):
    (a, b), (c, d) = m
    return sp.expand(L ** 2 - (a + d) * L + (a * d - b * c))


def eq_poly(tex):
    lhs, rhs = tex.split('=')
    return sp.expand(read(lhs) - read(rhs))


def proportional(p, q):
    if p == 0 or q == 0:
        return p == q
    r = sp.simplify(p / q)
    return r.is_number and r != 0


def line_checks(fails, where, line, m, cp):
    n = 0
    (a, b), (c, d) = m
    tr, det = a + d, a * d - b * c
    roots = set(sp.roots(sp.Poly(cp, L)).keys())
    t = line.replace('−', '-')
    if '=' not in t:
        return 0                        # prose with no claim ("Watch the sign: ...")
    for mt in re.finditer(r'Trace = (-?\d+)', t):
        n += 1
        if int(mt.group(1)) != tr:
            fails.append('working: %s: %r says trace %s, the matrix has %d' % (where, line, mt.group(1), tr))
    for md in re.finditer(r'Det(?:\(A\))? = ([-\d\s+−]+?)(?: = (-?\d+))?(?:[,.)]|$)', t):
        parts = [md.group(1).strip()] + ([md.group(2)] if md.group(2) else [])
        n += 1
        vals = [sp.sympify(p) for p in parts if p]
        if any(v != det for v in vals):
            fails.append('working: %s: %r says the determinant is %s, the matrix has %d' % (where, line, parts, det))
    for mr in re.finditer(r'\((\d+)\s*-\s*(\d+)\s*=\s*(-?\d+)\)', t):
        n += 1
        if int(mr.group(1)) - int(mr.group(2)) != int(mr.group(3)):
            fails.append('working: %s: %r says %s' % (where, line, mr.group(0)))
    for me in re.finditer(r'\\lambda = (\\pm )?(\d+|i)\b', t):
        n += 1
        v = sp.I if me.group(2) == 'i' else sp.Integer(me.group(2))
        claimed = {v, -v} if me.group(1) else {v}
        if not claimed <= roots:
            fails.append('working: %s: %r names %s, the eigenvalues are %s' % (where, line, sorted(map(str, claimed)), sorted(map(str, roots))))
    mi = re.search(r'A \\neq (\d+)I', t)
    if mi:
        n += 1
        k = int(mi.group(1))
        if [[a, b], [c, d]] == [[k, 0], [0, k]]:
            fails.append('working: %s: %r, but A is %dI' % (where, line, k))
    if re.search(r'\\lambda = |\\neq|Trace|Det|rotation|eigenvalue', t):
        return n
    body = t.split(':', 1)[1] if re.match(r'^[A-Za-z][A-Za-z ]+:', t) else t
    for part in body.split('='):
        part = part.strip()
        if not part or part == '0':
            continue
        try:
            v = read(part)
        except ValueError as e:
            fails.append('working: %s: the line %r cannot be read here (%s)' % (where, line, e))
            return n
        n += 1
        if sp.expand(v - cp) != 0:
            fails.append('working: %s: in %r, %s is %s, not det(A - lambda I) = %s' % (where, line, part, v, cp))
    return n


def check_bank(fails, qs):
    n = 0
    seen = set()
    for i, q in enumerate(qs, 1):
        where = 'item %d (A = %s)' % (i, q['m'])
        cp = charpoly(q['m'])
        opts = [q['c']] + list(q['d'])
        if len(q['d']) != 3 or len(set(opts)) != 4:
            fails.append('options: %s: %d distractors, %d different strings' % (where, len(q['d']), len(set(opts))))
            continue
        try:
            polys = [eq_poly(o) for o in opts]
        except ValueError as e:
            fails.append('key: %s: an option cannot be read (%s)' % (where, e))
            continue
        if sp.expand(polys[0] - cp) != 0:
            fails.append('key: %s: keyed %r, det(A - lambda I) = %s' % (where, q['c'], cp))
        right = [o for o, p in zip(opts, polys) if proportional(p, cp)]
        if right != [q['c']]:
            fails.append('options: %s: the options that are the characteristic equation are %r, the key is %r' % (where, right, q['c']))
        for line in (q.get('s') or []) + ([q['mc']] if q.get('mc') else []):
            n += line_checks(fails, where, line, q['m'], cp)
        k = str(q['m'])
        if k in seen:
            fails.append('options: %s: matrix repeated' % where)
        seen.add(k)
    return n


RENDER_JS = r"""(qs) => { const bad = [];
  for (const q of qs) for (const t of [q.c].concat(q.d, q.s || []))
    try { katex.renderToString(t, {throwOnError: true}); } catch (e) { bad.push(t + ' -> ' + e.message); }
  return bad; }"""
SESSION_JS = r"""() => { const out = [];
  for (let k = 0; k < 5; k++) { startGame(); out.push(pool.map(q => QS.indexOf(q))); }
  return out; }"""
MARK_JS = r"""(i) => {
  startGame();
  const item = QS[i], wanted = [item.c].concat(item.d), out = [];
  const ann = (el) => { const a = el.querySelector('annotation'); return a ? a.textContent : el.textContent; };
  for (let k = 0; k < 4; k++) {
    pool = [item]; qIdx = 0; total = 0; score = 0; nextQ();
    const btns = [...document.querySelectorAll('#options .opt-btn')];
    const target = btns.find(b => b.dataset.val === wanted[k]);
    if (!target) { out.push({k: k, missing: wanted[k]}); continue; }
    const shown = ann(document.getElementById('matrixDisplay'));
    target.click();
    const sol = document.getElementById('solution');
    out.push({k: k, n: btns.length, shown: shown, cls: target.className, keycls: btns.find(b => b.dataset.val === item.c).className,
              score: score, sol: sol.classList.contains('show'), steps: sol.querySelectorAll('.step').length, next: sol.querySelectorAll('button').length});
    MaffsLock.clearTimers();
  }
  return out; }"""


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
            ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)     # KaTeX from the pinned local copy
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.clock.install()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            qs = page.evaluate('() => JSON.parse(JSON.stringify(QS))')
            n = check_bank(fails, qs)
            for msg in page.evaluate(RENDER_JS, qs):
                fails.append('render: KaTeX cannot parse %s' % msg)
            for d in page.evaluate(SESSION_JS):
                if len(d) != 15 or len(set(d)) != 15 or min(d) < 0:
                    fails.append('session: dealt %r, expected 15 different items from the bank' % d)
                    break
            for i, q in enumerate(qs):
                where = 'item %d (A = %s)' % (i + 1, q['m'])
                (a, b), (c, d) = q['m']
                want_m = 'A = \\begin{pmatrix} %d & %d \\\\ %d & %d \\end{pmatrix}' % (a, b, c, d)
                for r in page.evaluate(MARK_JS, i):
                    if r.get('missing'):
                        fails.append('marking: %s: option %r not shown' % (where, r['missing']))
                        break
                    if r['shown'] != want_m:
                        fails.append('render: %s: the matrix shows as %r' % (where, r['shown']))
                        break
                    if r['k'] == 0:
                        ok = r['n'] == 4 and 'correct' in r['cls'].split() and r['score'] > 0 and not r['sol']
                    else:
                        ok = ('wrong' in r['cls'].split() and 'correct' in r['keycls'].split() and r['score'] == 0 and r['sol']
                              and r['steps'] == len(q.get('s') or []) and r['next'] >= 1)
                    if not ok:
                        fails.append('marking: %s, option %d: %r' % (where, r['k'], r))
                        break
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'items': len(qs), 'claims': n}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong key (trace sign flipped)', 'key:', [("{m:[[2,1],[0,3]],c:'\\\\lambda^2 - 5\\\\lambda + 6 = 0',d:['\\\\lambda^2 - 5\\\\lambda + 3 = 0','\\\\lambda^2 + 5\\\\lambda + 6 = 0'",
                                                     "{m:[[2,1],[0,3]],c:'\\\\lambda^2 + 5\\\\lambda + 6 = 0',d:['\\\\lambda^2 - 5\\\\lambda + 3 = 0','\\\\lambda^2 - 5\\\\lambda + 6 = 0'")]),
    ('SR-4/16: a distractor that is the key doubled', 'options:', [("d:['\\\\lambda^2 - 5\\\\lambda + 3 = 0','\\\\lambda^2 + 5\\\\lambda + 6 = 0','\\\\lambda^2 - 6\\\\lambda + 5 = 0'],s:['(2-",
                                                                   "d:['2\\\\lambda^2 - 10\\\\lambda + 12 = 0','\\\\lambda^2 + 5\\\\lambda + 6 = 0','\\\\lambda^2 - 6\\\\lambda + 5 = 0'],s:['(2-")]),
    ('a wrong expansion in a worked line', 'working:', [("'(4-\\\\lambda)(3-\\\\lambda) - (2)(1) = 12 - 7\\\\lambda + \\\\lambda^2 - 2'",
                                                        "'(4-\\\\lambda)(3-\\\\lambda) - (2)(1) = 12 - 7\\\\lambda + \\\\lambda^2 - 3'")]),
    ('a wrong trace stated', 'working:', [("'Trace = -5, Det = 4 - 6 = -2'", "'Trace = 5, Det = 4 - 6 = -2'")]),
    ('a wrong eigenvalue named', 'working:', [("'Repeated eigenvalue \\\\lambda = 3 (scalar matrix)'", "'Repeated eigenvalue \\\\lambda = 9 (scalar matrix)'")]),
    ('marking by the first five characters', 'marking:', [("ok=btn.dataset.val===q.c;", "ok=btn.dataset.val.slice(0,5)===q.c.slice(0,5);")]),
    ('the t6-003 step restored (the -4 sign lost)', 'working:', [("'\\\\lambda^2 - (0)\\\\lambda + (0 - 4) = ", "'\\\\lambda^2 - (0) - (0 - 4) = ")]),
    ('the matrix shown transposed', 'render:', [("' & '+m[0][1]+' \\\\\\\\ '+m[1][0]+' & '", "' & '+m[1][0]+' \\\\\\\\ '+m[0][1]+' & '")]),
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
    print('%s: %d items, every characteristic equation recomputed from its matrix; every option classified; %d worked expressions and '
          'claims checked; every option pressed in Chromium' % (SLUG, st.get('items', 0), st.get('claims', 0)))
    print('  not asserted (open): 15 of 26 served (t6-002), prose spacing in KaTeX (t6-004), ?level and the rotation note (t6-005)')
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
            found = [f for f in rep if f.startswith(tag)]
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
