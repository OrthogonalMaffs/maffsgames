#!/usr/bin/env python3
"""Differentiation Duel: every key and option differentiated again with SymPy; every explanation checked; every
option marked in Chromium.

The game (98 multiple-choice items: alevel 45, level4 53) asks for dy/dx of an explicit function, an implicit
relation or a parametric pair. Its bank was keyed by hand; the tranche 5 audit of 6 Oct 2026 found wrong options
equal to the key (e^x(x - 2)/x^3 for e^x/x^2; 2xe^{-y} and, on the curve, 2x/(x^2 + 1) for e^y = x^2 + 1) and
pairs of wrong options equal to each other (2x^{-3} and 2/x^3, x/y and 2x/2y, ...), plus explanations in caret
notation and ones that never state the answer.

Every item's question and options are read from their TeX into SymPy (tex() below; one it cannot read FAILS:
extend tex(), never skip). The target is
  explicit:   d/dx of the function (the part before any '=', which restates it);
  implicit:   -F_x / F_y for F = left - right, compared ON THE CURVE: at sample points (x, y) that satisfy the
              relation, since an option written in x alone can equal the key there (SR-16);
  parametric: (dy/dt) / (dx/dt).
Then: the key equals the target; no wrong option equals it (SR-4, SR-16); no two options are equal in value;
the explanation's last statement (after its last '=', ':', 'so' or 'to') equals the target, read from Unicode
or from \\( \\) TeX, so an explanation that never states the answer FAILS; no explanation uses caret notation
(x^(...)) outside \\( \\). In Chromium (390x844) every item is shown through the game's own nextQ() with its
options from MaffsOptions, and every option clicked through guess(): the key marked right, the others wrong;
the prompt renders with its spaces ("Find dy/dx").

A self-test plants three of the audit's own faults back into a copy of the page (t5-001: e^x(x - 2)/x^3 as a
wrong option; t5-002: 2xe^{-y}; t5-006: 2/x^3 beside 2x^{-3}); each must FAIL naming its item.

    python scripts/verify-differentiation-duel.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import os
import random
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr, rationalize,
                                        standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'differentiation-duel'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'alevel': 45, 'level4': 53}
x, y, t = sp.symbols('x y t')
LOCAL = {'x': x, 'y': y, 't': t, 'e': sp.E, 'E': sp.E, 'pi': sp.pi, 'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
         'sec': sp.sec, 'csc': sp.csc, 'cot': sp.cot, 'log': sp.log, 'ln': sp.log, 'sqrt': sp.sqrt}
TRANS = standard_transformations + (implicit_multiplication_application, rationalize)
FUNCS = ('sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'ln')

# Audit ids by (level, index in the bank), for failure messages.
AUDIT = {('level4', 32): 't5-001', ('level4', 45): 't5-002', ('level4', 26): 't5-003', ('level4', 31): 't5-004',
         ('level4', 44): 't5-005', ('level4', 2): 't5-006', ('level4', 4): 't5-007', ('level4', 38): 't5-008',
         ('level4', 49): 't5-009'}


def group(s, i, o, c):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == o) - (s[j] == c)
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced %s in %r' % (o, s))


def to_py(s):
    """TeX to a SymPy-parsable string."""
    s = (s.replace('\u2212', '-').replace('\\left', '').replace('\\right', '').replace('\\,', ' ')
         .replace('\\quad', ' ').replace('\\times', '*').replace('\\cdot', '*').strip())
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            num, j = group(s, i + m.end() - 1, '{', '}')
            den, k = group(s, j, '{', '}')
            out += '((%s)/(%s))' % (to_py(num), to_py(den))
            i = k
            continue
        m = re.match(r'\\sqrt\[(\d+)\]\{', s[i:])
        if m:
            inner, j = group(s, i + m.end() - 1, '{', '}')
            out += '((%s)**(1/%s))' % (to_py(inner), m.group(1))
            i = j
            continue
        if s.startswith('\\sqrt{', i):
            inner, j = group(s, i + 5, '{', '}')
            out += 'sqrt(%s)' % to_py(inner)
            i = j
            continue
        m = re.match(r'\\(sin|cos|tan|sec|csc|cot|ln)', s[i:])
        if m:
            f, i = m.group(1), i + m.end()
            f = 'log' if f == 'ln' else f
            power = None
            if s.startswith('^', i):
                pm = re.match(r'\^(\{[^}]*\}|\d)', s[i:])
                power, i = pm.group(1).strip('{}'), i + pm.end()
            while i < len(s) and s[i] == ' ':
                i += 1
            if s.startswith('(', i):
                arg, i = group(s, i, '(', ')')
                arg = to_py(arg)
            else:
                am = re.match(r'(\d*)\s*([xyt])', s[i:])
                if not am:
                    raise ValueError('no argument after \\%s in %r' % (f, s))
                arg, i = (am.group(1) + '*' if am.group(1) else '') + am.group(2), i + am.end()
            call = ' %s(%s)' % (f, arg)
            out += '(%s)**(%s)' % (call, power) if power else call
            continue
        if s[i] == '{':
            inner, j = group(s, i, '{', '}')
            out, i = out + '(%s)' % to_py(inner), j
            continue
        if s[i] == '\\':
            raise ValueError('unknown TeX command in %r' % s)
        if s[i] == '^':
            out += '**'
            i += 1
            if i < len(s) and s[i] not in '{(':
                out += s[i]          # a single-character exponent: e^x, x^3
                i += 1
            continue
        out += s[i]
        i += 1
    return out


def parse(py, what):
    py = re.sub(r'(?<=[0-9a-z)])\s*(?=(sin|cos|tan|sec|log|sqrt)\()', '*', py)
    try:
        return parse_expr(py, local_dict=LOCAL, transformations=TRANS)
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (what, py, e))


def tex(s):
    return parse(to_py(s), s)


SUP = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ˣʸᵗ', '0123456789-+xyt'))
VULGAR = {'½': '(1/2)', '⅓': '(1/3)', '⅔': '(2/3)', '¼': '(1/4)', '¾': '(3/4)', '³⁄₂': '(3/2)'}


def uni(s):
    """A plain-text (Unicode) expression from an explanation, as SymPy."""
    s0 = s
    s = s.replace('\u2212', '-').replace('×', '*').replace('·', '*').replace('d/dx', '')
    for k, v in VULGAR.items():
        s = s.replace(k, v)
    s = re.sub(r'√\(', 'sqrt(', s)
    s = re.sub(r'√([a-z0-9])', r'sqrt(\1)', s)
    # trig powers written sec²x, sin²x
    s = re.sub(r'(sin|cos|tan|sec)([²³])\s*([a-z])', lambda m: '(%s(%s))**%s' % (m.group(1), m.group(3), SUP[m.group(2)]), s)
    s = re.sub('[%s]+' % ''.join(SUP), lambda m: '**(%s)' % ''.join(SUP[c] for c in m.group(0)), s)
    s = re.sub(r'\bln\b', 'log', s)
    s = re.sub(r'(sin|cos|tan|sec|log)\s+([a-z])\b', r'\1(\2)', s)
    return parse(s, s0)


def final(expl):
    """The explanation's last stated expression, as SymPy (None if it states none)."""
    segs = re.split(r'\\\(|\\\)', expl)
    # rebuild with markers so a TeX segment is read as TeX
    parts = [(seg, k % 2 == 1) for k, seg in enumerate(segs)]
    text = ''.join(('\x01%s\x02' % seg) if is_tex else seg for seg, is_tex in parts)
    cut = max(text.rfind('='), text.rfind(': '), text.rfind(' so '), text.rfind(' to '))
    tail = (text[cut:] if cut >= 0 else text).lstrip('=: ').strip()   # no marker: the whole text is the answer
    tail = re.sub(r'^(so|to)\s+', '', tail).strip()
    tail = re.sub(r'^dy/dx\s*=\s*', '', tail)
    if '\x01' in tail or '\x02' in tail:
        tex_part = tail.replace('\x01', '').replace('\x02', '')
        tex_part = re.sub(r'^\\dfrac\{dy\}\{dx\}\s*=\s*', '', tex_part)
        return tex(tex_part)
    tail = re.sub(r'\s+to the nearest.*$', '', tail).rstrip('.')
    return uni(tail)


def target_of(q):
    if q['rule'] == 'Implicit':
        lhs, rhs = q['q'].split('=')
        F = tex(lhs) - tex(rhs)
        return 'implicit', -sp.diff(F, x) / sp.diff(F, y), F
    if q['rule'] == 'Parametric':
        xs, ys = [p.split('=', 1)[1] for p in q['q'].split('\\quad')]
        xs = xs.strip().rstrip(',')
        X, Y = tex(xs), tex(ys)
        return 'parametric', sp.diff(Y, t) / sp.diff(X, t), None
    f = tex(q['q'].split('=')[0])
    return 'explicit', sp.diff(f, x), None


def points(kind, F):
    rng = random.Random(11)
    if kind == 'implicit':
        pts = []
        for _ in range(40):
            xv = sp.Rational(rng.randint(5, 95), 100)
            for yv in sp.solve(F.subs(x, xv), y):
                yn = complex(sp.N(yv, 30))
                if abs(yn.imag) < 1e-20:
                    pts.append({x: xv, y: sp.Float(yn.real, 30)})
            if len(pts) >= 12:
                break
        return pts
    sym = t if kind == 'parametric' else x
    return [{sym: sp.Rational(rng.randint(5, 140), 100)} for _ in range(12)]


def same(a, b, pts):
    hits = 0
    for pt in pts:
        try:
            av, bv = complex(sp.N(sp.sympify(a).subs(pt), 30)), complex(sp.N(sp.sympify(b).subs(pt), 30))
        except (TypeError, ZeroDivisionError):
            continue
        if abs(av - bv) > 1e-9 * max(1, abs(av)):
            return False
        hits += 1
    return hits >= 8


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (update COUNTS and AUDIT together)' % (counts, COUNTS))
    for lv in COUNTS:
        for i, q in enumerate(bank.get(lv, [])):
            w = '%s[%d] (%s: %s)%s' % (lv, i, q['rule'], q['q'],
                                      ' (differentiation-duel-%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            opts = [q['correct']] + q['wrong']
            try:
                kind, target, F = target_of(q)
                vals = [tex(o) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend tex())' % (w, e))
                continue
            pts = points(kind, F)
            if len(pts) < 8:
                fails.append('%s: too few sample points on the curve (%d)' % (w, len(pts)))
                continue
            if not same(vals[0], target, pts):
                fails.append('%s: keyed %s, the derivative is %s' % (w, q['correct'], sp.simplify(target)))
            for o, v in zip(opts[1:], vals[1:]):
                if same(v, target, pts):
                    fails.append('%s: the wrong option %s equals the derivative%s (SR-16)'
                                 % (w, o, ' on the curve' if kind == 'implicit' else ''))
            for a in range(1, len(vals)):
                for b in range(a + 1, len(vals)):
                    if same(vals[a], vals[b], pts):
                        fails.append('%s: wrong options %s and %s are equal in value' % (w, opts[a], opts[b]))
            if len(set(opts)) != 4:
                fails.append('%s: %d options, not 4 distinct' % (w, len(set(opts))))
            plain = re.sub(r'\\\(.*?\\\)', '', q['exp'])
            if re.search(r'\^\(', plain):
                fails.append('%s: the explanation uses caret notation outside \\( \\): %r' % (w, q['exp']))
            try:
                fv = final(q['exp'])
            except ValueError as e:
                fails.append('%s: the explanation\'s answer cannot be read: %s' % (w, e))
                continue
            if fv is None:
                fails.append('%s: the explanation states no answer: %r' % (w, q['exp']))
            elif not same(fv, target, pts):
                fails.append('%s: the explanation ends at %s, the derivative is %s' % (w, fv, sp.simplify(target)))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  const lv = LEVEL;
  QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.wrong]) {
      questions = [q]; qNum = 0; score = 0; streak = 0; window._ddCorrect = 0;
      nextQ();
      const shown = [...document.querySelectorAll('#choices .choice')].map(b => b.dataset.val);
      const want = [q.correct, ...q.wrong];
      if (shown.length !== 4 || want.some(v => !shown.includes(v))) out.push([lv, i, pick, 'options shown ' + JSON.stringify(shown)]);
      const label = document.getElementById('qLabel');
      if (q.prompt && !/Find\s/.test(label.textContent.replace(/\u00a0/g, ' '))) out.push([lv, i, pick, 'prompt reads ' + JSON.stringify(label.textContent)]);
      const b = [...document.querySelectorAll('#choices .choice')].find(x => x.dataset.val === pick);
      if (!b) { out.push([lv, i, pick, 'not on screen']); continue; }
      b.click();
      const right = b.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
      const ex = document.getElementById('explanation');
      if (/\\\(|\\\)/.test(ex.textContent)) out.push([lv, i, pick, 'explanation shows raw delimiters']);
      if (window.MaffsNext) MaffsNext.clear(ex.parentNode);
    }
  });
  return out;
}"""

KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    banks = {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@0.16.9/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            for lv in COUNTS:
                page = ctx.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.goto(base + '/games/%s/?level=%s&cb=verify' % (SLUG, lv), wait_until='load', timeout=20000)
                page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
                banks = page.evaluate('() => QUESTIONS')
                for lvl, i, pick, what in page.evaluate(SWEEP_JS):
                    fails.append('%s[%d] in Chromium: option %s %s' % (lvl, i, pick, what))
                if errors:
                    fails.append('page errors (%s): %s' % (lv, '; '.join(errors[:3])))
                page.close()
            browser.close()
            return banks
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('level4[32]', 't5-001: e^x(x - 2)/x^3 as a wrong option',
     "'\\\\dfrac{x^2 e^x + 2xe^x}{x^4}'", "'\\\\dfrac{e^x(x - 2)}{x^3}'"),
    ('level4[45]', 't5-002: 2xe^{-y} as a wrong option', "'2xe^y']", "'2xe^{-y}']"),
    ('level4[2]', 't5-006: 2/x^3 beside 2x^{-3}', "'-2x^{-1}','x^{-3}']", "'-2x^{-1}','\\\\tfrac{2}{x^3}']"),
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
    bank = play(fails, html)
    if bank:
        check_bank(fails, bank)
    print('%s: %d items, every key and option differentiated again (SymPy), every option clicked in Chromium'
          % (SLUG, sum(len(bank.get(k, [])) for k in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-46s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
