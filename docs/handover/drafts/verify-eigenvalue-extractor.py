#!/usr/bin/env python3
# ci-line: Eigenvalue Extractor (every characteristic equation solved in SymPy; every option read as its list of eigenvalues and classified; every worked line and check sum recomputed; every option pressed in Chromium) |
"""Eigenvalue Extractor: given a characteristic equation in lambda, pick its eigenvalues from four options.

Static bank, read from the page as served: `QS`, 25 items `{eq, c: key, d: [3 distractors], s: worked lines, mc?: a note}`, 15 a
session. The mark is `button.dataset.val === q.c`; a wrong answer shows the worked lines.

Checks, independent of the game's code (SymPy; a small TeX reader here, as Jon allowed on 12 Oct 2026):
  Key: every option is read as a list of eigenvalues with repeats ("lambda = 2, lambda = 3"; "lambda = 3 (repeated)" is 3 twice;
    "lambda = (-5 \\pm \\sqrt{33})/2" and "\\pm i" are two; "No eigenvalues exist" is none), and the key is exactly the roots of
    the equation, counted with multiplicity, complex roots included.
  Options: four different strings; exactly one is the roots (SR-4/SR-16).
  Worked lines: an equation ("(lambda - 2)(lambda - 3) = 0", "lambda^2 = -1") has exactly the equation's roots; a list of
    eigenvalues ("lambda = 2 or lambda = 3", "Repeated eigenvalue lambda = 4", "lambda = \\pm i") names only roots; a quadratic
    formula line's expressions are equal in value and are the roots; "Discriminant = 81 - 64 = 17" and "Check: 2 + 3 = 5, 2 × 3 = 6"
    are true sums; "Both eigenvalues are negative" is true.
  Render: KaTeX (pinned local copy) parses every equation, option and worked line, and the equation shown is the item's.
  Sessions: startGame() dealt five times: 15 different items from the bank.
  Marking, in Chromium (390x844), through the game's own buttons: every option of every item pressed: the key is marked correct
    and scores; any other is marked wrong, the key shown, the worked solution shows the item's lines, Next mounted.
Not asserted (open findings, left open): 15 of 25 served (t6-002), the repeated-eigenvalue note (t6-003), prose losing its
spaces in KaTeX (t6-004), the rotation wording (t6-005).

    python scripts/verify-eigenvalue-extractor.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'eigenvalue-extractor'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
L = sp.Symbol('L')


def group(s, i):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '{') - (s[j] == '}')
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in %r' % s)


def to_py(tex, pm='+'):
    """TeX (lambda, numbers, \\dfrac, \\sqrt, i, \\pm as the sign pm) to Python text for SymPy."""
    s, out, i = tex.replace('−', '-'), '', 0
    while i < len(s):
        if s.startswith('\\dfrac', i) or s.startswith('\\frac', i):
            a, j = group(s, s.index('{', i))
            b, i = group(s, j)
            out += '((%s)/(%s))' % (to_py(a, pm), to_py(b, pm))
        elif s.startswith('\\sqrt', i):
            a, i = group(s, s.index('{', i))
            out += 'sqrt(%s)' % to_py(a, pm)
        elif s.startswith('\\pm', i):
            out += pm
            i += 3
        elif s.startswith('\\lambda', i):
            out += ' L '
            i += 7
        elif s.startswith('\\left', i) or s.startswith('\\right', i):
            i += 5 if s.startswith('\\left', i) else 6
        elif s[i] == '^':
            i += 1
            if s[i] == '{':
                a, i = group(s, i)
                out += '**(%s)' % to_py(a, pm)
            else:
                out += '**' + s[i]
                i += 1
        elif s[i] == 'i' and not s[i - 1:i].isalpha() and not s[i + 1:i + 2].isalpha():
            out += ' I '
            i += 1
        elif s[i] in '0123456789+-*/(). ':
            out += s[i]
            i += 1
        elif s[i] in '{}':
            i += 1
        else:
            raise ValueError('cannot read %r at %r' % (tex, s[i:]))
    out = re.sub(r'(\d|\))\s*(L|I|\(|sqrt)', r'\1*\2', out)
    out = re.sub(r'(L|I)\s*(\(|\d)', r'\1*\2', out)
    return out


def val(tex, pm='+'):
    return sp.sympify(to_py(tex, pm), locals={'L': L, 'I': sp.I})


def poly_of(eq):
    lhs, rhs = eq.split('=')
    return sp.expand(val(lhs) - val(rhs))


def roots_of(p):
    r = sp.roots(sp.Poly(p, L))
    return sorted([sp.nsimplify(k) for k, m in r.items() for _ in range(m)], key=sp.default_sort_key)


def same_multiset(a, b):
    a, b = list(a), list(b)
    if len(a) != len(b):
        return False
    for x in a:
        hit = next((k for k, y in enumerate(b) if sp.simplify(x - y) == 0), None)
        if hit is None:
            return False
        b.pop(hit)
    return True


def option_roots(opt):
    """The eigenvalues an option names, with repeats; None if it names none ("No eigenvalues exist")."""
    if re.search(r'No eigenvalues', opt):
        return []
    out = []
    for part in re.split(r',|\\text\{ or \}', opt):
        part = part.strip()
        if not part:
            continue
        rep = '\\text{ (repeated)}' in part
        part = part.replace('\\text{ (repeated)}', '').strip()
        m = re.fullmatch(r'\\lambda\s*=\s*(.+)', part)
        if not m:
            raise ValueError('cannot read the option %r' % opt)
        rhs = m.group(1)
        vs = [val(rhs, '+'), val(rhs, '-')] if '\\pm' in rhs else [val(rhs)]
        out += vs * (2 if rep else 1)
    return out


def line_checks(fails, where, line, p, roots):
    n = 0
    t = line.replace('−', '-').replace('×', '*')
    for a, op, b, c in re.findall(r'(-?\d+)\s*([+*])\s*(-?\d+)\s*=\s*(-?\d+)', t if 'Check' in t else ''):
        n += 1
        if (int(a) + int(b) if op == '+' else int(a) * int(b)) != int(c):
            fails.append('working: %s: the check %s %s %s = %s is false' % (where, a, op, b, c))
    md = re.search(r'Discriminant = (\d+) - (\d+) = (-?\d+)', t)
    if md:
        n += 1
        a2, c4, dd = map(int, md.groups())
        poly = sp.Poly(p, L)
        A, B, C = [int(x) for x in poly.all_coeffs()]
        if a2 - c4 != dd or B * B != a2 or 4 * A * C != c4:
            fails.append('working: %s: %r; b^2 - 4ac = %d - %d = %d' % (where, line, B * B, 4 * A * C, B * B - 4 * A * C))
    if 'Both eigenvalues are negative' in t:
        n += 1
        if not all(r.is_real and r < 0 for r in roots):
            fails.append('working: %s: %r but the eigenvalues are %s' % (where, line, roots))
    if 'Check' in t or 'Discriminant' in t or '=' not in t:
        return n
    body = re.sub(r'^[A-Za-z][A-Za-z :]*?:\s*', '', t).replace('Repeated eigenvalue', '').strip()
    if re.match(r'^\\lambda\s*=', body) and body.count('=') == 1 or '\\text{ or }' in body:
        try:
            named = option_roots(body)
        except ValueError as e:
            fails.append('working: %s: %r cannot be read here (%s)' % (where, line, e))
            return n
        n += 1
        if not all(any(sp.simplify(x - r) == 0 for r in roots) for x in named):
            fails.append('working: %s: %r names %s, the roots are %s' % (where, line, named, roots))
        return n
    if body.startswith('\\lambda = \\dfrac') or body.startswith('\\lambda = \\frac'):
        rhs = [q.strip() for q in body.split('=')[1:]]
        n += 1
        for sign in '+-':
            vs = [val(r, sign) for r in rhs]
            if not all(sp.simplify(v - vs[0]) == 0 for v in vs) or not any(sp.simplify(vs[0] - r) == 0 for r in roots):
                fails.append('working: %s: %r does not give the roots %s' % (where, line, roots))
                break
        return n
    try:
        q = poly_of(body)
    except Exception as e:
        fails.append('working: %s: %r cannot be read here (%s)' % (where, line, e))
        return n
    n += 1
    if not same_multiset(roots_of(q), roots):
        fails.append('working: %s: %r has roots %s, the equation %s' % (where, line, roots_of(q), roots))
    return n


def check_bank(fails, qs):
    n = 0
    seen = set()
    for i, q in enumerate(qs, 1):
        where = 'item %d (%s)' % (i, q['eq'])
        p = poly_of(q['eq'])
        roots = roots_of(p)
        opts = [q['c']] + list(q['d'])
        if len(q['d']) != 3 or len(set(opts)) != 4:
            fails.append('options: %s: %d distractors, %d different strings' % (where, len(q['d']), len(set(opts))))
            continue
        try:
            named = [option_roots(o) for o in opts]
        except ValueError as e:
            fails.append('key: %s: %s' % (where, e))
            continue
        if not same_multiset(named[0], roots):
            fails.append('key: %s: keyed %r, the roots are %s' % (where, q['c'], roots))
        right = [o for o, r in zip(opts, named) if same_multiset(r, roots)]
        if right != [q['c']]:
            fails.append('options: %s: the options that are the roots are %r, the key is %r' % (where, right, q['c']))
        for line in q.get('s') or []:
            n += line_checks(fails, where, line, p, roots)
        if q['eq'] in seen:
            fails.append('options: %s: equation repeated' % where)
        seen.add(q['eq'])
    return n


RENDER_JS = r"""(qs) => { const bad = [];
  for (const q of qs) for (const t of [q.eq, q.c].concat(q.d, q.s || []))
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
    const shown = ann(document.getElementById('eqDisplay'));
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
                where = 'item %d (%s)' % (i + 1, q['eq'])
                for r in page.evaluate(MARK_JS, i):
                    if r.get('missing'):
                        fails.append('marking: %s: option %r not shown' % (where, r['missing']))
                        break
                    if r['shown'] != q['eq']:
                        fails.append('render: %s: the equation shows as %r' % (where, r['shown']))
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
    ('a wrong key (2 and 4 for roots 2 and 3)', 'key:', [("c:'\\\\lambda = 2, \\\\lambda = 3',d:['\\\\lambda = 1, \\\\lambda = 6'",
                                                           "c:'\\\\lambda = 2, \\\\lambda = 4',d:['\\\\lambda = 1, \\\\lambda = 6'")]),
    ('SR-4/16: a distractor naming the roots in the other order', 'options:', [("d:['\\\\lambda = 1, \\\\lambda = 6','\\\\lambda = -2, \\\\lambda = -3','\\\\lambda = 2, \\\\lambda = -3'],s:['(\\\\lambda - 2)",
                                                                              "d:['\\\\lambda = 3, \\\\lambda = 2','\\\\lambda = -2, \\\\lambda = -3','\\\\lambda = 2, \\\\lambda = -3'],s:['(\\\\lambda - 2)")]),
    ('a repeated root keyed once only (3 for (lambda - 3)^2)', 'key:', [("c:'\\\\lambda = 3 \\\\text{ (repeated)}',d:['\\\\lambda = 3, \\\\lambda = 6'",
                                                                       "c:'\\\\lambda = 3, \\\\lambda = -3',d:['\\\\lambda = 3, \\\\lambda = 6'")]),
    ('a wrong factorisation in a worked line', 'working:', [("s:['(\\\\lambda - 2)(\\\\lambda - 5) = 0']", "s:['(\\\\lambda - 2)(\\\\lambda + 5) = 0']")]),
    ('a wrong discriminant', 'working:', [("'Discriminant = 81 - 64 = 17'", "'Discriminant = 81 - 64 = 19'")]),
    ('a wrong check sum', 'working:', [("'Check: 2 + 3 = 5 ✓, 2 × 3 = 6 ✓'", "'Check: 2 + 3 = 6 ✓, 2 × 3 = 6 ✓'")]),
    ('marking by the first nine characters', 'marking:', [("ok=btn.dataset.val===q.c", "ok=btn.dataset.val.slice(0,9)===q.c.slice(0,9)")]),
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
    print('%s: %d items, every equation solved and every option read as its eigenvalues; %d worked lines and sums checked; every option '
          'pressed in Chromium' % (SLUG, st.get('items', 0), st.get('claims', 0)))
    print('  not asserted (open): 15 of 25 served (t6-002), the repeated-eigenvalue note (t6-003), prose spacing (t6-004), rotation wording (t6-005)')
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
