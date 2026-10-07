#!/usr/bin/env python3
# ci-line: B4 | Integration Duel (every key and option checked with SymPy, explanations checked, every option marked in Chromium) |
"""Integration Duel: every key and option checked with SymPy; every explanation's answer checked; every option
marked in Chromium.

The game (90 multiple-choice items: alevel 45, level4 45) asks for an indefinite integral (an antiderivative plus
the constant c) or a definite integral's value. Its bank was keyed by hand; the tranche 5 audit of 6 Oct 2026
found a definite integral keyed 8/3 (it is 16/3), 'ln x + c' offered as a wrong answer to the integral of 1/x
(right for x > 0), pairs of wrong options equal to each other (2e^{2x} and 4e^{2x}/2, ...), a start screen
promising speed bonuses the scoring never gives, and explanations with units the questions never state.

Every question and option is read from its TeX into SymPy (tex() below; one it cannot read FAILS: extend tex(),
never skip). Then:
  indefinite: an option is RIGHT when its derivative is the integrand and it carries the constant c once (its
    derivative with respect to c is 1); the key must be right and no wrong option may be (SR-16). Sample points
    take x, t and omega positive (so ln x + c is right there, which is how the audit's fault shows). A wrong option
    that is the key without its + c is the game's named "missing constant" error, and its feedback must say so;
  definite: the key equals the integral exactly; no wrong option does;
  no two options are equal in value (c held as a symbol);
  the explanation's last statement (after its last '=', ':' or 'so') equals the key; so an explanation that
    never states the answer FAILS, and none may add a unit (m, m/s, J, N·s, kN·m) the question does not state.
In Chromium (390x844) every item is shown through the game's own nextQ() with its options from MaffsOptions,
and every option clicked through guess(): the key marked right, the others wrong; the key without its + c is
told the constant is missing. The start screen must not promise faster answers score higher (t5-009).

A self-test plants three of the audit's own faults back into a copy of the page (t5-001: the impulse integral
keyed 8/3; t5-002: 'ln x + c' as a wrong option; t5-004: 4e^{2x}/2 beside 2e^{2x}); each must FAIL naming its
item.

    python scripts/verify-integration-duel.py [--no-selftest] [--against FILE] [--katex-dir DIR]
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

SLUG = 'integration-duel'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
COUNTS = {'alevel': 45, 'level4': 45}
x, t, w = sp.symbols('x t w', positive=True)
c = sp.Symbol('c')
LOCAL = {'x': x, 't': t, 'w': w, 'c': c, 'e': sp.E, 'E': sp.E, 'pi': sp.pi, 'oo': sp.oo, 'sin': sp.sin,
         'cos': sp.cos, 'tan': sp.tan, 'sec': sp.sec, 'log': sp.log, 'sqrt': sp.sqrt, 'Abs': sp.Abs}
TRANS = standard_transformations + (implicit_multiplication_application, rationalize)
UNITS = re.compile(r'\d\s*(m/s|m\b|J\b|N·s|kN·m)')

# Audit ids by (level, index in the bank), for failure messages.
AUDIT = {('level4', 21): 't5-001', ('alevel', 24): 't5-002', ('alevel', 20): 't5-004', ('level4', 1): 't5-005',
         ('level4', 8): 't5-006', ('level4', 18): 't5-007', ('level4', 41): 't5-008'}


def group(s, i, o, cl):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == o) - (s[j] == cl)
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced %s in %r' % (o, s))


def to_py(s):
    """TeX to a SymPy-parsable string."""
    s = (s.replace('\u2212', '-').replace('\\left', '').replace('\\right', '').replace('\\,', ' ')
         .replace('\\cdot', '*').replace('\\omega', ' w ').replace('\\infty', ' oo ').replace('\\pi', ' pi ').strip())
    s = re.sub(r'\|([^|]+)\|', r'Abs(\1)', s)
    out, i = '', 0
    while i < len(s):
        m = re.match(r'\\[dt]?frac\{', s[i:])
        if m:
            num, j = group(s, i + m.end() - 1, '{', '}')
            den, k = group(s, j, '{', '}')
            out += '((%s)/(%s))' % (to_py(num), to_py(den))
            i = k
            continue
        if s.startswith('\\sqrt{', i):
            inner, j = group(s, i + 5, '{', '}')
            out += 'sqrt(%s)' % to_py(inner)
            i = j
            continue
        m = re.match(r'\\(sin|cos|tan|sec|ln)', s[i:])
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
            elif s.startswith('Abs(', i):
                arg, i = group(s, i + 3, '(', ')')
                arg = 'Abs(%s)' % arg
            else:
                am = re.match(r'(\d*\s*[xtw]|\d+)', s[i:])
                if not am:
                    raise ValueError('no argument after \\%s in %r' % (f, s))
                arg, i = am.group(1).replace(' ', '*') if re.search(r'\d\s*[xtw]', am.group(1)) else am.group(1), i + am.end()
                if re.fullmatch(r'\d+[xtw]', arg):
                    arg = arg[:-1] + '*' + arg[-1]
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
                out += s[i]
                i += 1
            continue
        out += s[i]
        i += 1
    return out


def parse(py, what):
    py = re.sub(r'(?<=[0-9a-z)])\s*(?=(sin|cos|tan|sec|log|sqrt|Abs)\()', '*', py)
    try:
        return parse_expr(py, local_dict=LOCAL, transformations=TRANS)
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (what, py, e))


def tex(s):
    return parse(to_py(s), s)


SUP = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ˣᵗᵘ', '0123456789-+xtu'))
SUB = dict(zip('₀₁₂₃₄₅₆₇₈₉', '0123456789'))


def uni(s):
    """A plain-text (Unicode) expression from an explanation, as SymPy."""
    s0 = s
    s = (s.replace('\u2212', '-').replace('×', '*').replace('·', '*').replace('ω', 'w').replace('½', '(1/2)')
         .replace('^', '**').replace('ln', 'log'))
    s = re.sub(r'\|([^|]+)\|', r'Abs(\1)', s)
    s = re.sub(r'log\s*Abs\(([^)]*)\)', r'log(Abs(\1))', s)
    s = re.sub('[%s]+' % ''.join(SUP), lambda m: '**(%s)' % ''.join(SUP[ch] for ch in m.group(0)), s)
    s = re.sub(r'(sin|cos|tan|sec|log)\s+([a-z0-9]+)', r'\1(\2)', s)
    v = parse(s, s0)
    if not isinstance(v, sp.Expr):
        raise ValueError('not one expression: %r' % s0)
    return v


def final(expl):
    """The explanation's last stated expression, as SymPy (the whole text if it has no '=', ':' or 'so')."""
    cut = max(expl.rfind('='), expl.rfind(': '), expl.rfind(' so '))
    tail = (expl[cut:] if cut >= 0 else expl).lstrip('=: ').strip()
    tail = re.sub(r'^so\s+', '', tail).strip()
    return uni(tail)


def integral(q):
    m = re.match(r'^\\int(?:_(\{[^}]*\}|\S)\^(\{[^}]*\}|\S))?\s*(.*?)\\,d([xt])$', q.strip())
    if not m:
        raise ValueError('not an integral: %r' % q)
    lo, hi, body, var = m.group(1), m.group(2), m.group(3), m.group(4)
    f = tex(body)
    v = x if var == 'x' else t
    if lo is None:
        return 'indefinite', f, v, None
    a, b = tex(lo.strip('{}')), tex(hi.strip('{}'))
    return 'definite', f, v, sp.integrate(f, (v, a, b))


def points():
    rng = random.Random(11)
    return [{x: sp.Rational(rng.randint(5, 140), 100), t: sp.Rational(rng.randint(5, 140), 100),
             w: sp.Rational(rng.randint(50, 300), 100), c: sp.Rational(rng.randint(-200, 200), 100)}
            for _ in range(12)]


PTS = points()


def same(a, b):
    a, b = sp.sympify(a), sp.sympify(b)
    if not (a.free_symbols or b.free_symbols):
        return sp.simplify(a - b) == 0
    hits = 0
    for pt in PTS:
        try:
            av, bv = complex(sp.N(a.subs(pt), 30)), complex(sp.N(b.subs(pt), 30))
        except (TypeError, ZeroDivisionError):
            continue
        if abs(av - bv) > 1e-9 * max(1, abs(av)):
            return False
        hits += 1
    return hits >= 8


def right(kind, f, v, val, opt):
    if kind == 'definite':
        return same(opt, val)
    return same(sp.diff(opt, v), f) and sp.diff(opt, c) == 1


def check_bank(fails, bank):
    counts = {lv: len(bank.get(lv, [])) for lv in COUNTS}
    if counts != COUNTS:
        fails.append('bank: %s items by level, expected %s (update COUNTS and AUDIT together)' % (counts, COUNTS))
    for lv in COUNTS:
        for i, q in enumerate(bank.get(lv, [])):
            w_ = '%s[%d] (%s: %s)%s' % (lv, i, q['rule'], q['q'],
                                       ' (integration-duel-%s)' % AUDIT[(lv, i)] if (lv, i) in AUDIT else '')
            opts = [q['correct']] + q['wrong']
            try:
                kind, f, v, val = integral(q['q'])
                vals = [tex(o) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend tex())' % (w_, e))
                continue
            if not right(kind, f, v, val, vals[0]):
                fails.append('%s: keyed %s, the answer is %s' % (w_, q['correct'],
                             val if kind == 'definite' else '%s + c' % sp.integrate(f, v)))
            for o, ov in zip(opts[1:], vals[1:]):
                if right(kind, f, v, val, ov):
                    fails.append('%s: the wrong option %s is also right (SR-16)' % (w_, o))
            for a in range(1, len(vals)):
                for b in range(a + 1, len(vals)):
                    if same(vals[a], vals[b]):
                        fails.append('%s: wrong options %s and %s are equal in value' % (w_, opts[a], opts[b]))
            if len(set(opts)) != 4:
                fails.append('%s: %d options, not 4 distinct' % (w_, len(set(opts))))
            if UNITS.search(q['exp']):
                fails.append('%s: the explanation adds a unit the question does not state: %r' % (w_, q['exp']))
            try:
                fv = final(q['exp'])
            except ValueError as e:
                fails.append('%s: the explanation\'s answer cannot be read: %s' % (w_, e))
                continue
            if not same(fv, vals[0]):
                fails.append('%s: the explanation ends at %s, the key is %s' % (w_, fv, q['correct']))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [];
  if (/faster answers score higher/i.test(document.body.textContent)) out.push(['page', -1, '', 'the start screen promises faster answers score higher (integration-duel-t5-009)']);
  const lv = currentLevel;
  QUESTIONS[lv].forEach((q, i) => {
    for (const pick of [q.correct, ...q.wrong]) {
      questions = [q]; qNum = 0; score = 0; streak = 0;
      nextQ();
      const shown = [...document.querySelectorAll('#choices .choice')].map(b => b.dataset.val);
      const want = [q.correct, ...q.wrong];
      if (shown.length !== 4 || want.some(v => !shown.includes(v))) out.push([lv, i, pick, 'options shown ' + JSON.stringify(shown)]);
      const b = [...document.querySelectorAll('#choices .choice')].find(x => x.dataset.val === pick);
      if (!b) { out.push([lv, i, pick, 'not on screen']); continue; }
      b.click();
      const right = b.classList.contains('correct');
      if (right !== (pick === q.correct)) out.push([lv, i, pick, right ? 'marked right' : 'marked wrong']);
      const fb = document.getElementById('feedback').textContent;
      if (/ \+ c$/.test(q.correct) && pick === q.correct.replace(/ \+ c$/, '') && !/\+ c is missing/.test(fb))
        out.push([lv, i, pick, 'the missing constant is not named: ' + JSON.stringify(fb)]);
      if (window.MaffsNext) MaffsNext.clear(document.getElementById('explanation').parentNode);
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
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the sweep answers at once
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
                    fails.append(('%s[%d] in Chromium: option %s %s' % (lvl, i, pick, what)) if i >= 0 else what)
                if errors:
                    fails.append('page errors (%s): %s' % (lv, '; '.join(errors[:3])))
                page.close()
            browser.close()
            return banks
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('level4[21]', 't5-001: the impulse integral keyed 8/3',
     "correct:'\\\\frac{16}{3}',\n      wrong:['-\\\\frac{16}{3}'", "correct:'\\\\frac{8}{3}',\n      wrong:['-\\\\frac{16}{3}'"),
    ('alevel[24]', "t5-002: 'ln x + c' as a wrong option", "'-x^{-2} + c','x^{-1} + c']", "'\\\\ln x + c','x^{-1} + c']"),
    ('alevel[20]', 't5-004: 4e^{2x}/2 beside 2e^{2x}', "'8e^{2x} + c'", "'\\\\frac{4e^{2x}}{2}'"),
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
    print('%s: %d items, every key and option checked (SymPy), every option clicked in Chromium'
          % (SLUG, sum(len(bank.get(k, [])) for k in COUNTS) if bank else 0))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-42s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-42s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
