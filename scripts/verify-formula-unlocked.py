#!/usr/bin/env python3
# ci-line: B3 | Formula Unlocked (every rearrangement checked in SymPy: the key satisfies its formula, no wrong option equals it or another; every option marked in Chromium) |
"""Formula Unlocked: every rearrangement checked with SymPy; every option clicked in Chromium.

The game (49 questions: Q_GCSE 29, Q_ALEVEL 6, Q_LEVEL4 14) shows a formula and asks to make one variable the
subject, from four options. Its bank was keyed by hand with no verifier; the resit audit of 4 Oct 2026 found
Q_ALEVEL[0] (s = ut + at^2/2, make u the subject) offering u = s/t - at/2, equal to the key (2s - at^2)/(2t),
and marking it wrong (formula-unlocked-r-001), with a third option string-identical to the key (dropped, so three
options showed). Three more items offered two wrong options equal in value: Q_GCSE[22] 3V/(4 pi) and
V/(4/3 pi) (audit F3, B11), Q_GCSE[23] u + sqrt(2as) and sqrt(u^2) + sqrt(2as) for u >= 0 (audit F4), and
Q_LEVEL4[10] gT/(2 pi) and g(T/(2 pi)) (formula-unlocked-f0-001, B11).

Every formula, option and worked step is read into SymPy (read() below: \\dfrac, \\frac, \\sqrt, \\sqrt[n],
\\left( \\right), Greek letters, \\Delta X as one symbol, subscripts, \\ln, e^{...}; every symbol positive, as
the quantities are physical lengths, masses and rates; an option read() cannot read FAILS: extend it). Then:
  - the key, put back into the formula, makes it an identity (the target's own value);
  - no wrong option does (SR-16), and no wrong option equals the key in value;
  - the four options are distinct strings and distinct in value (SR-4);
  - every line of the worked solution holds when the key is put in for the target;
  - in Chromium (390x844), every option of every question shown through nextQ() and clicked through
    handleAnswer(): the key marked right, the others wrong, four options on screen.
A self-test plants the audit's faults back into a copy of the page (r-001's value-equal option; f0-001's
g(T/(2 pi))); each must FAIL naming its item.

    python scripts/verify-formula-unlocked.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'formula-unlocked'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
BANKS = {'Q_GCSE': 29, 'Q_ALEVEL': 6, 'Q_LEVEL4': 14}
AUDIT = {('Q_ALEVEL', 0): 'formula-unlocked-r-001', ('Q_GCSE', 22): 'audit F3, B11', ('Q_GCSE', 23): 'audit F4',
         ('Q_LEVEL4', 10): 'formula-unlocked-f0-001, B11'}
GREEK = {'pi': 'PI', 'rho': 'rho', 'sigma': 'sigma', 'epsilon': 'epsilon'}
SYMS = {}


def sym(name):
    if name not in SYMS:
        SYMS[name] = sp.Symbol(name, positive=True)
    return SYMS[name]


def group(s, i, o='{', c='}'):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == o) - (s[j] == c)
        if d == 0:
            return s[i + 1:j], j + 1
    raise ValueError('unbalanced %s%s in %r' % (o, c, s))


def tokens(s):
    """[('atom', python text) | ('op', + - * / ^ ( ))] for one TeX expression."""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch.isspace():
            i += 1
            continue
        m = re.match(r'\\[dt]?frac(?=\{)', s[i:])
        if m:
            a, j = group(s, i + m.end())
            b, k = group(s, j)
            out.append(('atom', '((%s)/(%s))' % (expr(a), expr(b))))
            i = k
            continue
        if s.startswith('\\sqrt[', i):
            n, j = group(s, i + 5, '[', ']')
            a, k = group(s, j)
            out.append(('atom', '((%s)**(1/(%s)))' % (expr(a), expr(n))))
            i = k
            continue
        if s.startswith('\\sqrt{', i):
            a, j = group(s, i + 5)
            out.append(('atom', 'sqrt(%s)' % expr(a)))
            i = j
            continue
        if s.startswith('\\left', i):
            i += 5
            continue
        if s.startswith('\\right', i):
            i += 6
            continue
        if s.startswith('\\ln', i):
            j = i + 3
            while s[j].isspace():
                j += 1
            if s[j] == '{':
                a, k = group(s, j)
            elif s[j] == '(':
                a, k = group(s, j, '(', ')')
            else:
                a, k = s[j], j + 1
            out.append(('atom', 'log(%s)' % expr(a)))
            i = k
            continue
        m = re.match(r'\\Delta\s*([A-Za-z])', s[i:])
        if m:
            out.append(('atom', 'S("Delta_%s")' % m.group(1)))
            i += m.end()
            continue
        m = re.match(r'\\([A-Za-z]+)', s[i:])
        if m:
            name = m.group(1)
            if name not in GREEK:
                raise ValueError('unknown TeX command \\%s in %r' % (name, s))
            out.append(('atom', 'pi' if name == 'pi' else 'S("%s")' % name))
            i += m.end()
            continue
        if ch.isalpha():
            name, j = ch, i + 1
            if j < len(s) and s[j] == '_':
                if s[j + 1] == '{':
                    sub, j = group(s, j + 1)
                else:
                    sub, j = s[j + 1], j + 2
                name += '_' + sub
            out.append(('atom', 'E' if name == 'e' else 'S("%s")' % name))
            i = j
            continue
        if ch.isdigit() or ch == '.':
            m = re.match(r'\d+(\.\d+)?', s[i:])
            out.append(('atom', 'Rational("%s")' % m.group(0)))
            i += m.end()
            continue
        if ch == '{':
            a, j = group(s, i)
            out.append(('atom', '(%s)' % expr(a)))
            i = j
            continue
        if ch in '+-*/()^':
            out.append(('op', ch))
            i += 1
            continue
        raise ValueError('cannot read %r at %r' % (s, s[i:]))
    return out


def expr(s):
    """TeX to Python text: atoms side by side multiply; ^ is a power."""
    parts, prev = [], None
    for kind, t in tokens(s):
        if kind == 'atom' and prev in ('atom', ')'):
            parts.append('*')
        if kind == 'op' and t == '(' and prev in ('atom', ')'):
            parts.append('*')
        parts.append('**' if t == '^' else t)
        prev = ')' if t == ')' else kind if kind == 'atom' else 'op'
    return ''.join(parts)


def read(s):
    """A TeX expression as SymPy; ValueError when it cannot be read."""
    try:
        return sp.sympify(expr(s), locals={'S': sym, 'Rational': sp.Rational, 'sqrt': sp.sqrt, 'log': sp.log,
                                           'E': sp.E, 'pi': sp.pi})
    except ValueError:
        raise
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (s, expr(s), e))


def sides(eq):
    return [read(p) for p in eq.split('=')]


def zero(e):
    e = sp.expand_log(sp.simplify(e), force=True)
    return sp.simplify(e) == 0


def same(a, b):
    return zero(a - b)


def target_symbol(q):
    lhs = read(q['target'])
    if not isinstance(lhs, sp.Symbol):
        raise ValueError('target %r is not one symbol' % q['target'])
    return lhs


def option(q, s):
    """An option 'X = expr' as (lhs symbol, SymPy rhs)."""
    lhs, rhs = s.split('=', 1)
    return read(lhs), read(rhs)


def satisfies(q, t, value):
    """Does target := value make the formula an identity?"""
    fl, fr = sides(q['formula'])
    return zero((fl - fr).subs(t, value))


def check_bank(fails, banks):
    for name, want in BANKS.items():
        if len(banks.get(name) or []) != want:
            fails.append('%s: %d questions, expected %d (a change needs this script reviewed)' % (name, len(banks.get(name) or []), want))
            return
    for name in BANKS:
        for i, q in enumerate(banks[name]):
            w = '%s[%d] (%s, make %s the subject)%s' % (name, i, q['formula'], q['target'],
                                                         ' (%s)' % AUDIT[(name, i)] if (name, i) in AUDIT else '')
            key = q.get('correct_override') or q['correct']
            opts = [key] + [o for o in q['d'] if o != key]
            if len(q['d']) != 3 or len(set([key] + q['d'])) != 4:
                fails.append('%s: the options %s are not four distinct strings' % (w, [key] + q['d']))
            try:
                t = target_symbol(q)
                vals = [option(q, o) for o in opts]
            except ValueError as e:
                fails.append('%s: %s (extend read())' % (w, e))
                continue
            if any(lhs != t for lhs, _ in vals):
                fails.append('%s: an option does not have %s as its subject: %s' % (w, q['target'], opts))
                continue
            k = vals[0][1]
            if t in k.free_symbols:
                fails.append('%s: the key %s still has %s on the right' % (w, key, q['target']))
            elif not satisfies(q, t, k):
                fails.append('%s: the key %s does not satisfy %s' % (w, key, q['formula']))
            for o, (_, v) in zip(opts[1:], vals[1:]):
                if same(v.subs(t, k), k):
                    fails.append('%s: the wrong option %s equals the key in value (SR-16)' % (w, o))
            for a in range(1, len(opts)):
                for b in range(a + 1, len(opts)):
                    if same(vals[a][1].subs(t, k), vals[b][1].subs(t, k)):
                        fails.append('%s: the wrong options %s and %s are equal in value (SR-4)' % (w, opts[a], opts[b]))
            for line in q.get('steps', []):
                try:
                    ss = [e.subs(t, k) for e in sides(line)]
                except ValueError as e:
                    fails.append('%s: step %r: %s' % (w, line, e))
                    continue
                fl, fr = sides(q['formula'])
                if not all(same(ss[0], x) for x in ss[1:]):
                    fails.append('%s: the step %r does not hold for the key' % (w, line))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.setInterval = () => 0;
  const out = [], banks = {Q_GCSE, Q_ALEVEL, Q_LEVEL4};
  for (const [name, bank] of Object.entries(banks)) bank.forEach((q, i) => {
    const key = q.correct_override || q.correct;
    for (const pick of [key, ...q.d]) {
      pool = [q]; qIdx = 0; total = 0; score = 0; correctN = 0;
      nextQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')];
      if (shown.length !== 4) out.push([name, i, pick, shown.length + ' options on screen']);
      const btn = shown.find(b => b.dataset.val === pick);
      if (!btn) { out.push([name, i, pick, 'not on screen']); continue; }
      btn.click();
      const right = btn.classList.contains('correct');
      if (right !== (pick === key)) out.push([name, i, pick, right ? 'marked right' : 'marked wrong']);
    }
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof Q_GCSE !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            for name, i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('%s[%d]%s in Chromium: option %s %s' % (name, i, ' (%s)' % AUDIT[(name, i)] if (name, i) in AUDIT else '', pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()


def load(html):
    tree, _ = bc.parse_game_source(html)
    if tree is None:
        return {}
    return {name: bc.literal_to_json(init) for name, init, _ in bc.top_level_declarations(tree) if name in BANKS}


def run(html):
    fails = []
    banks = load(html)
    check_bank(fails, banks)
    play(fails, html)
    return fails, sum(len(v or []) for v in banks.values())


PLANTS = [
    ('Q_ALEVEL[0]', 'r-001: s/t - at/2 offered beside the key',
     "d:['u = \\\\dfrac{s}{t} - \\\\dfrac{1}{2}at^2',", "d:['u = \\\\dfrac{s}{t} - \\\\dfrac{1}{2}at',"),
    ('Q_LEVEL4[10]', 'f0-001: g(T/(2 pi)) beside gT/(2 pi)',
     "'L = \\\\dfrac{gT^2}{2\\\\pi}']", "'L = g\\\\left(\\\\dfrac{T}{2\\\\pi}\\\\right)']"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='check this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails, n = run(html)
    print('%s: %d questions, every option read into SymPy and clicked in Chromium' % (SLUG, n))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-42s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep, _ = run(html.replace(old, new))
            hit = [f for f in rep if f.startswith(tag)]
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
