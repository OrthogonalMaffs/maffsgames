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
  Structure (SWEEP-1): a polynomial line of the form lambda^2 - t + d must carry its lambda on the trace term
    (lambda^2 - (t)lambda + (d)), never "lambda^2 - 0 + ...".
  Notes: every prose note and "Diagonal matrix:" / "Upper triangular:" / "Repeated ..." line is checked against its item's matrix
    (diagonal, upper triangular, real symmetric, scalar, singular, the 90 degree rotation, repeated root, complex roots, the sign
    claim "opposite signs" with det < 0, "subtracting (-1)(1) means adding 1"); a prose line with no '=' that none of these
    recognises fails, so a new unchecked claim cannot slip in.
  Start-screen worked example (not in QS): the matrix, A - lambda I, the determinant line, the expansion and lambda^2 - 7 lambda
    + 10 are recomputed, and the quick formula must read lambda^2 - (a+d) lambda + (ad-bc) = 0.
Fixed in SWEEP-1 batch 11: item 13's line "\\lambda^2 - 0 + (0-(-1))" is now "\\lambda^2 - (0)\\lambda + (0-(-1))"; the item 4 note says the
eigenvalues have opposite signs (not "one is negative"); item 17's note says "Real symmetric matrix".
Fixed earlier (SR-6, wording and key agree): item 22's line "\\lambda^2 - (0) - (0 - 4) = \\lambda^2 - 4" read +4, not -4; it now
reads "\\lambda^2 - (0)\\lambda + (0 - 4)" (characteristic-quest-t6-003).
Not asserted (open findings, left open): 15 of 26 served (t6-002), prose lines losing spaces in KaTeX (t6-004), ?level (t6-005),
duplicate keys with identical distractor sets (for Jon), and the worked lines' wording beyond the claims above.

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


def note_checks(fails, where, line, m, cp):
    """Prose claims in a worked line or note, checked against the item's matrix. Returns the number of claims checked."""
    (a, b), (c, d) = m
    det = a * d - b * c
    roots = set(sp.roots(sp.Poly(cp, L)).keys())
    real = all(r.is_real for r in roots)
    t = line.replace('−', '-')
    n = 0

    def need(cond, what):
        nonlocal n
        n += 1
        if not cond:
            fails.append('note: %s: %r claims %s, which the matrix does not bear out' % (where, line, what))
    if t.startswith('Diagonal matrix:') or 'diagonal matrices' in t:
        need(b == 0 and c == 0, 'a diagonal matrix')
    if t.startswith('Upper triangular:'):
        need(c == 0, 'an upper triangular matrix')
    if 'ymmetric matrix' in t:
        need(t.startswith('Real symmetric matrix'), 'real symmetric (the note must say "Real symmetric")')
        need(b == c, 'a symmetric matrix')
    if 'Negative determinant' in t:
        need(det < 0 and real, 'a negative determinant with real roots')
        need('opposite signs' in t and 'one eigenvalue is negative' not in t, 'the eigenvalues have opposite signs')
    if 'scalar matrix' in t and 'NOT' not in t and 'neq' not in t:
        need(b == 0 and c == 0 and a == d, 'a scalar matrix')
    if 'NOT mean scalar matrix' in t:
        need(len(roots) == 1 and not (b == 0 and c == 0), 'a repeated root of a non-scalar matrix')
    if t.startswith('Repeated'):
        need(len(roots) == 1, 'a repeated eigenvalue')
    if 'singular matrix' in t:
        need(det == 0 and 0 in roots, 'a singular matrix with eigenvalue 0')
    if '90° rotation matrix' in t:
        need([[a, b], [c, d]] == [[0, -1], [1, 0]], 'the 90 degree rotation matrix')
    if 'Complex eigenvalues indicate a rotation' in t or 'No real eigenvalues' in t:
        need(not real, 'complex eigenvalues')
    ms = re.search(r'subtracting \((-?\d+)\)\((-?\d+)\) means adding (\d+)', t)
    if ms:
        x, y, z = int(ms.group(1)), int(ms.group(2)), int(ms.group(3))
        need(x * y < 0 and z == -x * y and sorted([x, y]) == sorted([b, c]), 'subtracting a negative product (the matrix has b, c = %d, %d)' % (b, c))
    if '=' not in t and n == 0:
        fails.append('note: %s: the prose line %r makes a claim this verifier does not recognise; add a check for it' % (where, line))
    return n


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
        if re.match(r'\\lambda\^2\s*[+-]\s*(?:\(-?\d+\)|\d+)(?!\s*\\lambda)\s*[+-]', part):
            n += 1
            fails.append('working: %s: in %r, %r has a trace term with no lambda (write lambda^2 - (t)lambda + (d))' % (where, line, part))
        try:
            v = read(part)
        except ValueError as e:
            fails.append('working: %s: the line %r cannot be read here (%s)' % (where, line, e))
            return n
        n += 1
        if sp.expand(v - cp) != 0:
            fails.append('working: %s: in %r, %s is %s, not det(A - lambda I) = %s' % (where, line, part, v, cp))
    return n


def check_example(fails, html):
    """The start-screen worked example (buildExample), which is not in QS."""
    body = html.split('function buildExample(){', 1)[1].split('window.addEventListener', 1)[0]
    tex = [s.replace('\\\\', '\\') for s in re.findall(r"rkI\('((?:[^'\\]|\\.)*)'\)", body)]
    if len(tex) != 7:
        fails.append('example: expected 7 formulas in the worked example, found %d' % len(tex))
        return 0
    nums = [int(x) for x in re.findall(r'-?\d+', tex[0])]
    if len(nums) != 4:
        fails.append('example: cannot read the matrix %r' % tex[0])
        return 0
    m = [nums[:2], nums[2:]]
    cp = charpoly(m)
    (a, b), (c, d) = m
    want1 = 'A - \\lambda I = \\begin{pmatrix} %d-\\lambda & %d \\\\ %d & %d-\\lambda \\end{pmatrix}' % (a, b, c, d)
    if tex[1] != want1:
        fails.append('example: step 1 reads %r, expected %r' % (tex[1], want1))
    for i, what in ((2, 'the determinant line'), (3, 'the expansion'), (4, 'the result')):
        try:
            p = eq_poly(tex[i])
        except ValueError as e:
            fails.append('example: %s cannot be read (%s)' % (what, e))
            continue
        if sp.expand(p - cp) != 0:
            fails.append('example: %s %r is %s, not det(A - lambda I) = %s' % (what, tex[i], p, cp))
    if re.findall(r'\d', tex[5]):
        fails.append('example: the quick-formula matrix %r has numbers' % tex[5])
    if tex[6] != '\\lambda^2 - (a+d)\\lambda + (ad-bc) = 0':
        fails.append('example: the quick formula reads %r' % tex[6])
    if 'λ² − (trace)λ + (determinant) = 0' not in body:
        fails.append('example: the trace/determinant sentence is missing')
    return 7


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
            n += note_checks(fails, where, line, q['m'], cp)
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


def hud_fails(html):
    """SWEEP-1 (R7, characteristic-quest-s1-004): the game is listed under Hidden Count-Up in .claude/rules/timer-policy.md, so the
    HUD shows no running Time."""
    return ['hud: the running Time is on the HUD; Hidden Count-Up means it is never shown (R7, characteristic-quest-s1-004)'] \
        if re.search(r'class="hud-label">Time<', html) or 'id="timer"' in html else []


def play(fails, html):
    fails.extend(hud_fails(html))
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
            n = check_bank(fails, qs) + check_example(fails, html)
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
    ('the HUD Time back', 'hud:', [('<div class="hud-item"><div class="hud-label">Score</div>', '<div class="hud-item"><div class="hud-label">Time</div><div class="hud-val" id="timer">0</div></div><div class="hud-item"><div class="hud-label">Score</div>')]),
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
    ('SWEEP-1: item 13 trace term without its lambda', 'working:', [("'\\\\lambda^2 - (0)\\\\lambda + (0-(-1)) = ", "'\\\\lambda^2 - 0 + (0-(-1)) = ")]),
    ('SWEEP-1: the old item 4 note (one eigenvalue negative)', 'note:', [('means the eigenvalues have opposite signs.', 'means one eigenvalue is negative.')]),
    ('SWEEP-1: the old item 17 note (Symmetric, not Real symmetric)', 'note:', [("mc:'Real symmetric matrix", "mc:'Symmetric matrix")]),
    ('SWEEP-1: a diagonal note on a non-diagonal matrix', 'note:', [("{m:[[5,0],[0,2]],c:", "{m:[[5,1],[0,2]],c:")]),
    ('SWEEP-1: a wrong quick formula on the start screen', 'example:', [("\\\\lambda^2 - (a+d)\\\\lambda + (ad-bc) = 0", "\\\\lambda^2 - (a+d)\\\\lambda + (ad+bc) = 0")]),
    ('SWEEP-1: a wrong expansion on the start screen', 'example:', [("12 - 3\\\\lambda - 4\\\\lambda + \\\\lambda^2 - 2 = 0", "12 - 3\\\\lambda - 4\\\\lambda + \\\\lambda^2 - 3 = 0")]),
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
    print('  not asserted (open): 15 of 26 served (t6-002), prose spacing in KaTeX (t6-004), ?level (t6-005), duplicate option sets')
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
