#!/usr/bin/env python3
# ci-line: Index Laws (all 45 keys recomputed symbolically from the question's TeX; every option classified; every explanation's arithmetic recomputed; every option pressed in Chromium) |
"""Index Laws: multiple choice on the laws of indices, 45 items in six rules, 12 a session, four options each.

Static bank, read from the page as served: `QUESTIONS`, each item `{rule, q, correct, wrong[3], exp, ask?}` with `q` and every
option TeX. The game shows `q = ?`, the key and the three `wrong` shuffled, and on an answer the item's `exp`. The mark is
`val === q.correct`.

Checks, independent of the game's code (SymPy, exact rationals, every letter a positive symbol so (x^m)^n = x^(mn) and
x^0 = 1 hold as the lesson teaches; nothing is floated):
  Key: the question's TeX (products, quotients, powers of powers, zero, negative and fractional powers, fractions, roots)
    is read into an expression and the key is equal to it for every positive x or a. An exponent written "4 1/2" is a mixed
    number (4.5), as printed.
  Options: four different strings, none of the three wrong ones the key's string; exactly one is equal to the question
    (SR-4/SR-16), so a distractor equal in value is a second right answer. The one exception is a question whose `ask` names
    a form ("a single power of 5"): there an equal option is wrong when it is not that form (25^3), and exactly one option is
    a power of that base equal to the value.
  Convention (Jon's ruling, 12 Oct 2026, index-laws-v20-001): a coefficient-and-variable term such as 2x^2 is one object;
    implied multiplication binds tighter than ÷, so 6x^7 ÷ 2x^2 divides by the whole term (3x^5). The keys are read that way.
  Ambiguity (SR-17): each stem is also read strictly left to right. Where the two readings differ, every divisor must be a
    coefficient-and-variable term, so the convention gives the stem one reading; a divisor that is anything else (a number
    juxtaposed with a bracket, 2(x^3)) reads two ways under the convention and fails.
  Rule: each item's rule label fits its question (multiply: a product; divide: a quotient; power of a power: a bracket raised
    to a power; zero: an exponent 0; negative: a negative exponent or 1 over a power; fractional: a fractional exponent), and
    the six rules hold 8, 8, 7, 4, 8 and 10 items.
  Explanation: every sum in `exp` ("2×3=6", "6-(-3)=9", "2⁻⁴=1/16", "1/2+1/2=1") and every stated root ("Cube root of 27
    is 3") is recomputed here and must be true; the count checked is printed.
  Render: every question, option and ask is parsed by KaTeX (throwOnError, pinned local copy); the displayed question and each
    option's annotation is the source.
  Sessions: startGame() dealt five times: 12 different questions from the bank, four different buttons each.
  Marking, in Chromium (390x844), through the game's own buttons: every item is shown by nextQ() and each of its four options
    pressed; the key reads CORRECT! (class correct, +10); any other reads WRONG! (class wrong, the key shown, no score, streak
    0, Next mounted); the item's explanation is shown either way.
No analytics or leaderboard request leaves the stub server (every other request is aborted).

    python scripts/verify-index-laws.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy
from sympy import Rational, Symbol, sympify

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'index-laws'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
# A coefficient-and-variable term (Jon's ruling, 12 Oct 2026): an optional number, then letters each with an optional power.
TERM = re.compile(r'\s*\d*(?:\.\d+)?\s*(?:[xa]\s*(?:\^\s*(?:\{(?:[^{}]|\{[^{}]*\})*\}|-?\d+))?\s*)+')
RULES = {'Multiply Rule': 8, 'Divide Rule': 8, 'Power of a Power': 7, 'Zero Power': 4, 'Negative Power': 8, 'Fractional Power': 10}
X, A = Symbol('x', positive=True), Symbol('a', positive=True)
SUPER = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻', '0123456789-')


# ---- TeX to a SymPy expression -----------------------------------------------------------------------------------------
def group(s, i, open_='{', close='}'):
    assert s[i] == open_, (s, i)
    depth, j = 0, i
    while j < len(s):
        if s[j] == open_:
            depth += 1
        elif s[j] == close:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced %r' % s)


def divisor_end(s, i):
    """Where the term after a \\div that starts at s[i] ends: the next \\times, \\div, + or - outside brackets."""
    j, depth = i, 0
    while j < len(s):
        if s[j] in '{(':
            depth += 1
        elif s[j] in '})':
            depth -= 1
        elif depth == 0 and (s.startswith('\\times', j) or s.startswith('\\div', j) or s[j] in '+-'):
            break
        j += 1
    return j


def divisors(s):
    return [s[m.end():divisor_end(s, m.end())] for m in re.finditer(r'\\div', s)]


def conv(s, strict=False):
    s = re.sub(r'(\d+)\\d?frac\{(\d+)\}\{(\d+)\}', r'((\1)+(\2)/(\3))', s)     # 4\frac{1}{2} is the mixed number 4 1/2
    out = ''

    def glue(piece, needs_star=True):
        nonlocal out
        if needs_star and out and (out[-1].isdigit() or out[-1] == ')' or out[-1] in 'xa'):
            out += '*'
        out += piece

    i = 0
    while i < len(s):
        if s.startswith('\\dfrac', i) or s.startswith('\\frac', i):
            a, j = group(s, s.index('{', i))
            b, i = group(s, j)
            glue('((%s)/(%s))' % (conv(a, strict), conv(b, strict)))
        elif s.startswith('\\sqrt[', i):
            n, j = group(s, s.index('[', i), '[', ']')
            a, i = group(s, j)
            glue('((%s)**(1/(%s)))' % (conv(a, strict), conv(n, strict)))
        elif s.startswith('\\sqrt', i):
            a, i = group(s, s.index('{', i))
            glue('sqrt(%s)' % conv(a, strict))
        elif s.startswith('\\times', i):
            out += '*'
            i += 6
        elif s.startswith('\\div', i):
            i += 4
            if strict:
                out += '/'                  # strictly left to right: (6x^7 / 2) * x^2
            else:                           # the convention: a division by a term divides by all of it
                j = divisor_end(s, i)
                out += '/(%s)' % conv(s[i:j])
                i = j
        elif s[i] == '^':
            i += 1
            if s[i] == '{':
                a, i = group(s, i)
                out += '**(%s)' % conv(a, strict)
            else:
                m = re.match(r'-?\d+|[a-z]', s[i:])
                out += '**(%s)' % m.group(0)
                i += len(m.group(0))
        elif s[i] in 'xa':
            glue(s[i])
            i += 1
        elif s[i] == '(':
            glue('(')
            i += 1
        elif s[i] in ' {}':
            i += 1
        elif s[i] == '\\':
            raise ValueError('unknown TeX command in %r' % s)
        else:
            out += s[i]
            i += 1
    return out


def val(tex, strict=False):
    return sympify(conv(tex, strict), rational=True, locals={'x': X, 'a': A})


def same(a, b):
    return sympy.simplify(a - b) == 0


def power_of(tex, base):
    """The exponent k if the option is base^k written as a single power, else None."""
    m = re.fullmatch(r'(\d+)\^\{?(-?\d+)\}?', tex.strip())
    return int(m.group(2)) if m and int(m.group(1)) == base else None


# ---- the explanations' arithmetic ----------------------------------------------------------------------------------------
def norm(c):
    c = c.replace('×', '*').replace('÷', '/').replace('−', '-')
    return re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)', lambda m: '**(%s)' % m.group(1).translate(SUPER), c)


def exp_claims(exp):
    """(true, false) clauses of `exp`: each 'lhs = rhs' with no letters, and each 'X root of N is M'."""
    ok, bad = [], []
    for kind, n, m in re.findall(r'(Square|Cube|Fourth) root of (\d+) is (\d+)', exp):
        r = {'Square': 2, 'Cube': 3, 'Fourth': 4}[kind]
        (ok if int(m) ** r == int(n) else bad).append('%s root of %s is %s' % (kind, n, m))
    for c in re.split(r'[:,;]| so | then | and ', exp):
        c = norm(c.strip())
        if '=' not in c or not re.fullmatch(r'[0-9+\-*/().\s=]+', c):
            continue
        parts = [p.strip() for p in c.split('=')]
        try:
            vals = [sympify(p, rational=True) for p in parts if p]
        except Exception:
            bad.append(c + ' (unreadable)')
            continue
        (ok if all(v == vals[0] for v in vals) else bad).append(c)
    return ok, bad


LABELS = {
    'Multiply Rule': lambda q: '\\times' in q,
    'Divide Rule': lambda q: '\\div' in q or q.startswith('\\dfrac{'),
    'Power of a Power': lambda q: bool(re.match(r'\(.*\)\^', q)),
    'Zero Power': lambda q: '^0' in q,
    'Negative Power': lambda q: '^{-' in q or q.startswith('\\dfrac{1}{x^'),
    'Fractional Power': lambda q: '\\frac' in q,
}


def check_bank(fails, bank):
    counts, seen, nclaims = {}, set(), 0
    for i, q in enumerate(bank, 1):
        where = 'item %d (%s)' % (i, q['q'])
        counts[q['rule']] = counts.get(q['rule'], 0) + 1
        if q['rule'] not in LABELS or not LABELS[q['rule']](q['q']):
            fails.append('rule: %s: labelled %r but the question is not that kind' % (where, q['rule']))
        if q['q'] in seen:
            fails.append('options: %s: question repeated' % where)
        seen.add(q['q'])
        opts = [q['correct']] + list(q['wrong'])
        if len(q['wrong']) != 3 or len(set(opts)) != 4:
            fails.append('options: %s: %d wrong options, %d different strings with the key' % (where, len(q['wrong']), len(set(opts))))
            continue
        try:
            v = val(q['q'])
            ov = [val(o) for o in opts]
        except Exception as e:
            fails.append('key: %s: cannot be read here (%s: %s)' % (where, type(e).__name__, e))
            continue
        if not same(ov[0], v):
            fails.append('key: %s: keyed %s but the question works out to %s' % (where, q['correct'], v))
        strict = val(q['q'], strict=True)
        if not same(strict, v):
            odd = [d for d in divisors(q['q']) if not TERM.fullmatch(d)]
            if odd:
                fails.append('ambiguity: %s: the divisor %r is not a coefficient-and-variable term, so the stem reads two ways (%s or %s; SR-17)' % (
                    where, odd[0].strip(), v, strict))
        ask = q.get('ask')
        if ask:
            m = re.search(r'single power of (\d+)', ask)
            base = int(m.group(1)) if m else None
            right = [o for o, x in zip(opts, ov) if same(x, v) and base is not None and power_of(o, base) is not None]
        else:
            right = [o for o, x in zip(opts, ov) if same(x, v)]
        if right != [q['correct']]:
            fails.append('options: %s: the right option(s) are %r, the key is %r' % (where, right, q['correct']))
        ok, bad = exp_claims(q['exp'])
        nclaims += len(ok)
        for b in bad:
            fails.append('working: %s: the explanation %r says %s, which is false' % (where, q['exp'], b))
    if counts != RULES:
        fails.append('rule: the rules hold %r, expected %r' % (counts, RULES))
    return nclaims


# ---- in the page ----------------------------------------------------------------------------------------------------
RENDER_JS = r"""(bank) => {
  const bad = [];
  for (const q of bank) for (const t of [q.q, q.correct].concat(q.wrong)) {
    try { katex.renderToString(t, {throwOnError: true}); } catch (e) { bad.push(t + ' -> ' + e.message); }
  }
  return bad;
}"""
SESSION_JS = r"""() => { const out = [];
  for (let k = 0; k < 5; k++) { startGame(); const first = questions.map(q => QUESTIONS.indexOf(q));
    out.push({n: questions.length, idx: first}); }
  return out; }"""
SHOWN_JS = r"""() => {
  startGame();
  const out = [];
  for (let k = 0; k < 5; k++) {
    qNum = 0; questions = [QUESTIONS[k]]; nextQ();
    out.push([...document.querySelectorAll('#choices .choice')].map(b => b.dataset.val));
  }
  return out;
}"""
MARK_JS = r"""(i) => {
  startGame();
  const item = QUESTIONS[i], wanted = [item.correct].concat(item.wrong), out = [];
  const ann = (el) => { const a = el.querySelector('annotation'); return a ? a.textContent : el.textContent; };
  for (let k = 0; k < 4; k++) {
    score = 0; streak = 0; qNum = 0; questions = [item]; nextQ();
    const btns = [...document.querySelectorAll('#choices .choice')];
    const shown = btns.map(b => ({val: b.dataset.val, tex: ann(b)}));
    const qtex = ann(document.getElementById('qText'));
    const target = btns.find(b => b.dataset.val === wanted[k]);
    if (!target) { out.push({k: k, missing: wanted[k], shown: shown}); continue; }
    target.click();
    out.push({k: k, shown: shown, qtex: qtex, sub: document.getElementById('qSub').textContent,
              cls: target.className, keycls: btns.find(b => b.dataset.val === item.correct).className,
              others: btns.filter(b => b !== target && b.dataset.val !== item.correct).map(b => b.className),
              fb: document.getElementById('feedback').textContent, exp: document.getElementById('explanation').textContent,
              score: score, streak: streak, next: document.getElementById('explanation').parentNode.querySelectorAll('button:not(.choice)').length});
    MaffsLock.clearTimers();
  }
  return out;
}"""


def mark_checks(fails, page, bank):
    for i, q in enumerate(bank):
        where = 'item %d (%s)' % (i + 1, q['q'])
        res = page.evaluate(MARK_JS, i)
        for r in res:
            if r.get('missing'):
                fails.append('options: %s: the option %r is not on the page (shown: %r)' % (where, r['missing'], [s['val'] for s in r['shown']]))
                break
            right = r['k'] == 0
            cls, key = r['cls'].split(), r['keycls'].split()
            if right:
                ok = 'correct' in cls and 'wrong' not in cls and r['fb'].startswith('CORRECT!') and r['score'] == 10 and r['streak'] == 1
            else:
                ok = ('wrong' in cls and 'correct' in key and r['fb'] == 'WRONG!' and r['score'] == 0 and r['streak'] == 0
                      and r['next'] >= 1 and all('correct' not in c.split() and 'wrong' not in c.split() for c in r['others']))
            if r['exp'] != q['exp']:
                ok = False
            if not ok:
                fails.append('marking: %s, option %d (%s): classes %r / key %r, %r, score %d, streak %d, Next %d, explanation %r' % (
                    where, r['k'], 'the key' if right else 'a distractor', r['cls'], r['keycls'], r['fb'], r['score'], r['streak'],
                    r['next'], r['exp']))
                break
        r0 = res[0]
        if r0.get('missing') or 'qtex' not in r0:
            continue
        if sorted(s['val'] for s in r0['shown']) != sorted([q['correct']] + q['wrong']):
            fails.append('options: %s: the buttons shown are %r, not the item\'s four' % (where, [s['val'] for s in r0['shown']]))
        for s in r0['shown']:
            if s['tex'] != s['val']:
                fails.append('render: %s: option %r shows as %r' % (where, s['val'], s['tex']))
                break
        if r0['qtex'] != q['q'] + ' = \\; ?' or r0['sub'] != (q.get('ask') or 'Select the correct simplified form'):
            fails.append('render: %s: the question shows as %r / %r' % (where, r0['qtex'], r0['sub']))


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
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify(QUESTIONS))')
            nclaims = check_bank(fails, bank)
            for msg in page.evaluate(RENDER_JS, bank):
                fails.append('render: KaTeX cannot parse %s' % msg)
            for d in page.evaluate(SESSION_JS):
                if d['n'] != 12 or len(set(d['idx'])) != 12 or min(d['idx']) < 0:
                    fails.append('session: dealt %d questions (%d different, all from the bank: %s)' % (d['n'], len(set(d['idx'])), min(d['idx']) >= 0))
            for k, shown in enumerate(page.evaluate(SHOWN_JS)):
                if len(shown) != 4 or len(set(shown)) != 4:
                    fails.append('options: item %d shows %d buttons (%d different)' % (k + 1, len(shown), len(set(shown))))
            mark_checks(fails, page, bank)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'items': len(bank), 'claims': nclaims}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong key (x^8 for x^3 times x^4)', 'key:',
     [("{rule:'Multiply Rule', q:'x^3 \\\\times x^4', correct:'x^7',\n    wrong:['x^{12}','2x^7','x^{34}']",
       "{rule:'Multiply Rule', q:'x^3 \\\\times x^4', correct:'x^8',\n    wrong:['x^{12}','2x^7','x^{34}']")]),
    ('SR-4/16: a distractor equal to the key in value (x^{3+4})', 'options:',
     [("wrong:['x^{12}','2x^7','x^{34}'], exp:'Add the powers: 3+4=7'", "wrong:['x^{3+4}','2x^7','x^{34}'], exp:'Add the powers: 3+4=7'")]),
    ('a distractor identical to the key', 'options:',
     [("wrong:['x^{12}','2x^7','x^{34}'], exp:'Add the powers: 3+4=7'", "wrong:['x^7','2x^7','x^{34}'], exp:'Add the powers: 3+4=7'")]),
    ('the asked form met twice ((5^2)^3 with a second 5^6)', 'options:',
     [("wrong:['5^5','5^8','25^3']", "wrong:['5^5','5^{6}','25^3']")]),
    ('a wrong sum in an explanation (3+4=8)', 'working:',
     [("exp:'Add the powers: 3+4=7'", "exp:'Add the powers: 3+4=8'")]),
    ('a wrong stated root in an explanation', 'working:',
     [("Cube root of 27 is 3 (3³=27)", "Cube root of 27 is 9 (3³=27)")]),
    ('the strict reading keyed (3x^9 for 6x^7 ÷ 2x^2; the ruling says 3x^5)', 'key:',
     [("correct:'3x^5',\n    wrong:['4x^5','3x^9','12x^5']", "correct:'3x^9',\n    wrong:['4x^5','3x^5','12x^5']")]),
    ('SR-17: a divisor that is not a term (6x^8 ÷ 2(x^3)) reads two ways', 'ambiguity:',
     [("{rule:'Divide Rule', q:'x^8 \\\\div x^3', correct:'x^5',",
       "{rule:'Divide Rule', q:'6x^8 \\\\div 2(x^3)', correct:'3x^5',")]),
    ('a divide item labelled as multiply', 'rule:',
     [("{rule:'Divide Rule', q:'x^8 \\\\div x^3'", "{rule:'Multiply Rule', q:'x^8 \\\\div x^3'")]),
    ('a misspelt TeX command', 'render:',
     [("q:'x^3 \\\\times x^4'", "q:'x^3 \\\\tims x^4'")]),
    ('marking by the length of the option only', 'marking:',
     [("const correct=val===q.correct;", "const correct=val.length===q.correct.length;")]),
    ('a session one question short', 'session:',
     [("questions=shuffle(QUESTIONS).slice(0,TOTAL);", "questions=shuffle(QUESTIONS).slice(0,TOTAL-1);")]),
    ('only two distractors shown', 'options:',
     [("shuffle(w).slice(0,3)", "shuffle(w).slice(0,2)")]),
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
    print('%s: %d items, every key worked out symbolically from its TeX; every option classified; %d sums and roots in the explanations '
          'recomputed; every option pressed in Chromium' % (SLUG, st.get('items', 0), st.get('claims', 0)))
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
            found = [f for f in rep if tag in f]
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
