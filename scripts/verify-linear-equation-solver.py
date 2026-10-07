#!/usr/bin/env python3
# ci-line: B4 | Linear Equation Solver (every move class re-derived with SymPy; every option of every state marked in Chromium at 390px) |
"""Linear Equation Solver: every move option's class re-derived independently; every option played in Chromium.

    python scripts/verify-linear-equation-solver.py              # verify the game (and the self-test)
    python scripts/verify-linear-equation-solver.py --against F  # verify another copy of the page (main's)

The game asks "What is the optimal move here?" (Jon's design, 7 Oct 2026). scripts/gen-linear-moves.py decides
each option's class by a structural search and writes MOVES into the page; this script re-derives every class
from the TeX the student sees, with SymPy, by a different route:

  * Each state line and each option is parsed from its TeX into a SymPy equation.
  * A move is VALID exactly when its equation keeps the state's solution; an ERROR changes it.
  * A linear equation p*x + q = c needs [q != 0] + [p != 1] more moves (one for the constant, one for the
    coefficient; no single move does both), so a valid option's route length is 1 + that count for the line
    it gives. The shortest routes from a two-move line are "remove the constant" and "divide by the
    coefficient"; a route is clean when no line on it has a non-integer number that is not in the starting
    equation. OPTIMAL = shortest, and clean where any shortest route is clean; SLOWER = valid, not optimal.

It then checks, for all 141 questions and every state the game can reach:
  - the generated class of every option equals the re-derived one, and every error has a named reason;
  - four options, at least one optimal, at most one slower, at least one error, no two equal as moves;
  - every valid option's next line is the option's equation simplified (same two sides), and is a state in
    MOVES or x on its own; every state is reachable;
  - on the keyed route, the keyed move is optimal and leads to the bank's own line (the bank is unchanged);
  - the worked solution's "Also optimal" routes are exactly the optimal routes other than the keyed one.

In Chromium at 390x844 it marks every option of every state through the game's own handleAnswer():
optimal green with no cost, slower amber at half a wrong move's cost with the streak kept and "This works, but
it's slower", errors red with their reason; and the contract's four named behaviours (an optimal move scores
full; x2 on x/2 + 5 = 11 scores full; /3 on 3x + 7 = 22 scores amber with the message; a one-side-only error
is red with its reason). Hints render through KaTeX (no raw TeX on screen), options render without a KaTeX
error, and the page never scrolls sideways.

Self-test: plants the old single-key marking (only the keyed move accepted) and a mislabelled error (an error
option labelled optimal); both must be caught.
"""
import argparse, json, os, re, sys, tempfile
from fractions import Fraction as F

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import bank_common as bc  # noqa: E402

SLUG = 'linear-equation-solver'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
X = sp.Symbol('x')
TR = standard_transformations + (implicit_multiplication_application,)


# ------------------------------------------------------------------ TeX -> SymPy
def frac_to_div(t):
    """\\frac{A}{B} -> ((A)/(B)), innermost first, by brace matching."""
    while '\\frac' in t:
        i = t.rindex('\\frac')
        j = i + 5

        def group(j):
            assert t[j] == '{', t
            d, k = 0, j
            while True:
                if t[k] == '{':
                    d += 1
                elif t[k] == '}':
                    d -= 1
                    if d == 0:
                        return t[j + 1:k], k + 1
                k += 1
        a, j = group(j)
        b, j = group(j)
        t = t[:i] + '((%s)/(%s))' % (a, b) + t[j:]
    return t


def tex_expr(t):
    s = frac_to_div(t.replace('\\,', ' ')).replace('\\times', '*').replace('{', '(').replace('}', ')')
    return parse_expr(s, local_dict={'x': X}, transformations=TR, evaluate=True)


def tex_eq(t):
    l, r = t.split('=')
    return tex_expr(l), tex_expr(r)


def solution(eq):
    l, r = eq
    s = sp.solve(sp.Eq(l, r), X)
    return s[0] if len(s) == 1 else None


def lin(eq):
    """(p, q, c): the x-side as p*x + q, the other side's number c."""
    l, r = eq
    xs, other = (l, r) if l.has(X) else (r, l)
    P = sp.Poly(sp.expand(xs), X)
    p, q = P.coeff_monomial(X), P.coeff_monomial(1)
    return sp.Rational(p), sp.Rational(q), sp.Rational(other)


def steps(eq):
    p, q, _c = lin(eq)
    return int(q != 0) + int(p != 1)


def nums(eq):
    p, q, c = lin(eq)
    return {abs(p), abs(q), abs(c)}


def new_fraction(eq, start):
    return any(v.q != 1 and v not in start for v in nums(eq))


def shortest_routes(eq):
    """The two first moves that start a shortest route from a two-move line, as the equations they give."""
    p, q, c = lin(eq)
    return [(p, 0, c - q), (1, q / p, c / p)]


def optimal_set(eq, start):
    """{(p, q, c)} of the lines an optimal move gives, re-derived."""
    n = steps(eq)
    if n == 1:
        p, q, c = lin(eq)
        return {(sp.Integer(1), sp.Integer(0), (c - q) / p)}, n
    cands = shortest_routes(eq)
    clean = [r for r in cands if not any(sp.Rational(v).q != 1 and abs(sp.Rational(v)) not in start for v in r)]
    return set(tuple(sp.Rational(v) for v in r) for r in (clean or cands)), n


def same_sides(a, b):
    return sp.expand(a[0] - b[0]) == 0 and sp.expand(a[1] - b[1]) == 0


# ------------------------------------------------------------------ the page's data
READ_JS = '() => ({Q: QUESTIONS.gcse, M: MOVES})'


def load(page_html, fails):
    """Read QUESTIONS and MOVES from the running page (Chromium); None if the page has no MOVES."""
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            route_page(ctx, page_html)
            page = ctx.new_page()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            if not page.evaluate('() => typeof MOVES !== "undefined"'):
                fails.append('the page has no MOVES table: every move is marked against one keyed option '
                             '(linear-equation-solver-t4-001, -r-001, -r-002)')
                return None
            return page.evaluate(READ_JS)
    finally:
        proc.terminate()


def route_page(ctx, html):
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))


# ------------------------------------------------------------------ the classes, re-derived
def check_data(data, fails):
    Q, M = data['Q'], data['M']
    if len(Q) != 141:
        fails.append('expected 141 questions, read %d' % len(Q))
    n_states = n_opts = 0
    for q in Q:
        qid = q['id']
        mv = M.get(qid)
        if not mv:
            fails.append('%s: no MOVES entry' % qid)
            continue
        start = tex_eq(q['eq'])
        start_nums = nums(start)
        x0 = solution(start)
        if mv['start'] != q['eq']:
            fails.append('%s: MOVES starts at %r, the question at %r' % (qid, mv['start'], q['eq']))
        reached = {mv['start']}
        keyed_lines = {}
        for k, st in mv['states'].items():
            n_states += 1
            eq = tex_eq(k)
            if solution(eq) != x0:
                fails.append('%s: state %s does not have the solution x = %s' % (qid, k, x0))
            opt_set, need = optimal_set(eq, start_nums)
            opts = st['opts']
            n_opts += len(opts)
            where = '%s at %s' % (qid, k)
            cls = [o['c'] for o in opts]
            if len(opts) != 4:
                fails.append('%s: %d options, not 4' % (where, len(opts)))
            if cls.count('opt') < 1 or cls.count('slow') > 1 or cls.count('err') < 1:
                fails.append('%s: classes %s (need >=1 optimal, <=1 slower, >=1 error)' % (where, cls))
            seen_eq = []
            for o in opts:
                oe = tex_eq(o['t'])
                sol = solution(oe)
                valid = (sol == x0)
                if valid:
                    # the next line is this option's equation simplified, side for side
                    if 'n' not in o:
                        fails.append('%s: valid option %s has no next line' % (where, o['t']))
                        continue
                    ne = tex_eq(o['n'])
                    if not same_sides(oe, ne):
                        fails.append('%s: %s does not simplify to %s' % (where, o['t'], o['n']))
                    if o['n'] in mv['states']:
                        reached.add(o['n'])
                    elif steps(ne) != 0:
                        fails.append('%s: %s leads to %s, which is neither a state nor solved' % (where, o['t'], o['n']))
                    p, qq, c = lin(ne)
                    total = 1 + steps(ne)
                    if total == need and (p, qq, c) in opt_set:
                        want = 'opt'
                    else:
                        want = 'slow'
                    if o['c'] != want:
                        fails.append('%s: %s is labelled %s, re-derived %s (%d steps, optimal %d)' % (
                            where, o['t'], o['c'], want, total, need))
                    if want == 'slow' and not o.get('why'):
                        fails.append('%s: slower option %s gives no reason' % (where, o['t']))
                    key_eq = ('v', p, qq, c)
                else:
                    if o['c'] != 'err':
                        fails.append('%s: %s is labelled %s but changes the solution (%s, not %s)' % (
                            where, o['t'], o['c'], sol, x0))
                    if not o.get('why'):
                        fails.append('%s: error %s has no named reason' % (where, o['t']))
                    key_eq = ('e', sp.expand(oe[0] - oe[1]))
                if key_eq in seen_eq:
                    fails.append('%s: two options are the same move (%s)' % (where, o['t']))
                seen_eq.append(key_eq)
            if 'keyed' in st:
                i = st['keyed']
                kop = q['ops'][i]['correct']
                ko = [o for o in opts if o.get('op') == kop and o['c'] == 'opt']
                if not ko:
                    fails.append('%s: the keyed move %s is not offered as optimal' % (where, kop))
                elif 'line' in q['ops'][i] and ko[0]['n'] != q['ops'][i]['line']:
                    fails.append('%s: the keyed move leads to %s, the bank says %s' % (where, ko[0]['n'], q['ops'][i]['line']))
                keyed_lines[i] = k
        # every keyed phase is a state; every state is reachable; after an error the game goes along best[0]
        for i in range(len(q['ops'])):
            if i not in keyed_lines:
                fails.append('%s: keyed phase %d has no state' % (qid, i + 1))
        for k, st in mv['states'].items():
            best = [o for o in st['opts'] if o['c'] == 'opt']
            if best and best[0]['n'] in mv['states']:
                reached.add(best[0]['n'])
        for k in mv['states']:
            if k not in reached:
                fails.append('%s: state %s cannot be reached' % (qid, k))
        check_alt(q, mv, start, start_nums, fails)
    return n_states, n_opts


def routes(eq, start_nums):
    """Every optimal route from eq, as lists of (p, q, c) lines, re-derived."""
    if steps(eq) == 0:
        return [[]]
    out = []
    opt_set, _n = optimal_set(eq, start_nums)
    for p, q, c in opt_set:
        nxt = (p * X + q, c)
        for r in routes(nxt, start_nums):
            out.append([(p, q, c)] + r)
    return out


def check_alt(q, mv, start, start_nums, fails):
    """The worked solution's other optimal routes: exactly the optimal routes other than the keyed one."""
    all_r = routes(start, start_nums)
    shown = []
    for r in mv.get('alt', []):
        if r[0] != q['eq']:
            fails.append('%s: an "Also optimal" route does not start at the question' % q['id'])
            continue
        lines = [tex_eq(t if '=' in t else t) for t in r[2::2]]
        shown.append([lin(e) for e in lines])
    keyed = []
    eq = start
    for i, op in enumerate(q['ops']):
        nxt = op.get('line')
        if nxt:
            keyed.append(lin(tex_eq(nxt)))
    keyed.append(lin(tex_eq(q['ans']['correct'])))
    want = [r for r in all_r if r != keyed]
    if sorted(map(str, want)) != sorted(map(str, shown)):
        fails.append('%s: "Also optimal" shows %d route(s); %d optimal route(s) besides the keyed one' % (
            q['id'], len(shown), len(want)))


# ------------------------------------------------------------------ Chromium
PLAY_JS = r"""async ([qid, key, val]) => {
  if (window.MaffsNext) MaffsNext.clear(document.getElementById('feedback'));
  pool = QUESTIONS.gcse.filter(q => q.id === qid); qIdx = 0; streak = 3;
  loadQuestion();
  state = key; renderPhase();
  const btn = [...document.querySelectorAll('.opt-btn')].find(b => b.dataset.val === val);
  if (!btn) return {missing: true};
  handleAnswer(btn);
  const fb = document.getElementById('feedback');
  const r = {cls: btn.className, penalty: qPenalty, missed: qMissed,
             fb: fb.textContent, fbShown: fb.classList.contains('show'),
             trail: [...document.querySelectorAll('#workCard .work-line, #workCard .work-op')].map(e => e.textContent).join(' | '),
             err: document.querySelectorAll('.opt-btn .katex-error').length};
  if (window.MaffsNext) MaffsNext.clear(fb);
  return r;
}"""


def play(html, data, fails, quick=False):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    played = 0
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            route_page(ctx, html)
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof MOVES !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            page.evaluate("() => { window.setTimeout = (f) => 0; }")   # no auto-advance while each option is marked
            page.click('.start-btn')
            M = data['M']

            def mark(qid, key, opt):
                return page.evaluate(PLAY_JS, [qid, key, opt['t']])

            # the contract's four behaviours
            named = [
                ('L1', '3x + 7 = 22', '3x + 7 - 7 = 22 - 7', 'opt', 'an optimal move scores full'),
                ('M1', r'\frac{x}{2} + 5 = 11', r'2 \times \frac{x}{2} + 2 \times 5 = 2 \times 11', 'opt',
                 'x2 on x/2 + 5 = 11 scores full (tie)'),
                ('L1', '3x + 7 = 22', r'\frac{3x}{3} + \frac{7}{3} = \frac{22}{3}', 'slow',
                 '/3 on 3x + 7 = 22 scores amber with the message'),
                ('L1', '3x + 7 = 22', None, 'err-one-side', 'a one-side-only error is red with its reason'),
            ]
            for qid, key, t, want, label in named:
                st = M.get(qid, {}).get('states', {}).get(key)
                if not st:
                    fails.append('%s: no state %s' % (label, key))
                    continue
                if t is None:
                    o = next((o for o in st['opts'] if o.get('kind') in ('one-side', 'other-side')), None)
                    if o is None:
                        # the start state may not offer one: L1's offers carry-across and a constant-kept slip
                        o = next((o for o in st['opts'] if o['c'] == 'err'), None)
                else:
                    o = next((o for o in st['opts'] if o['t'] == t), None)
                if o is None:
                    fails.append('%s: the option is not offered' % label)
                    continue
                r = mark(qid, key, o)
                check_mark(r, o, '%s (%s)' % (label, qid), fails)
            # a one-side-only error, wherever the bank offers one (A1: x + 7 - 7 = 12)
            o = next(o for o in M['A1']['states']['x + 7 = 12']['opts'] if o.get('kind') == 'one-side')
            r = mark('A1', 'x + 7 = 12', o)
            check_mark(r, o, 'a one-side-only error is red with its reason (A1)', fails)
            if 'one side only' not in r.get('fb', ''):
                fails.append('A1: the one-side-only error does not say "one side only": %r' % r.get('fb'))

            # every option of every state
            if not quick:
                for qid, mv in M.items():
                    for key, st in mv['states'].items():
                        for o in st['opts']:
                            r = mark(qid, key, o)
                            check_mark(r, o, '%s at %s, %s' % (qid, key, o['t']), fails)
                            played += 1

            # hints: no raw TeX on screen (J1 and Y1 carry \frac)
            for qid in ('J1', 'Y1'):
                txt = page.evaluate("""(qid) => { pool = QUESTIONS.gcse.filter(q => q.id === qid); qIdx = 0;
                    loadQuestion(); useHint(); const p = document.getElementById('hintPanel');
                    return {text: p.textContent, katex: p.querySelectorAll('.katex').length}; }""", qid)
                if '\\frac' in txt['text'] or not txt['katex']:
                    fails.append('%s: the hint shows raw TeX (linear-equation-solver-t4-002): %r' % (qid, txt['text'][:80]))
            # the worked solution names the other optimal route (M1)
            sol = page.evaluate("""() => { pool = QUESTIONS.gcse.filter(q => q.id === 'M1'); qIdx = 0; loadQuestion();
                qMissed = true; showSolution(); return document.getElementById('solution').textContent; }""")
            if 'Also optimal' not in sol:
                fails.append('M1: the worked solution does not show the other optimal route')
            # no sideways scroll at 390px with the longest options on screen
            for qid, key in (('Y1', r'\frac{2}{3}x + 4 = 10'), ('U1', '-x + 6 = 10'), ('S1', '5 - 2x = 13')):
                w = page.evaluate("""([qid, key]) => { pool = QUESTIONS.gcse.filter(q => q.id === qid); qIdx = 0;
                    loadQuestion(); state = key; renderPhase(); return document.documentElement.scrollWidth; }""", [qid, key])
                if w > 390:
                    fails.append('%s: the page is %dpx wide at 390px (scrolls sideways)' % (qid, w))
            for e in errors:
                fails.append('page error: %s' % e)
    finally:
        proc.terminate()
    return played


def check_mark(r, o, where, fails):
    if r.get('missing'):
        fails.append('%s: no button for this option' % where)
        return
    if r['err']:
        fails.append('%s: an option renders as a KaTeX error' % where)
    c = o['c']
    if c == 'opt':
        if 'correct' not in r['cls'] or r['penalty'] != 0 or r['missed'] or r['fbShown']:
            fails.append('%s: optimal, but marked %s, cost %s, missed %s' % (where, r['cls'], r['penalty'], r['missed']))
    elif c == 'slow':
        if 'slower' not in r['cls'] or r['penalty'] != 12.5 or r['missed'] or 'This works, but it’s slower' not in r['fb']:
            fails.append('%s: slower, but marked %s, cost %s, missed %s, feedback %r' % (
                where, r['cls'], r['penalty'], r['missed'], r['fb'][:60]))
    else:
        if 'wrong' not in r['cls'] or r['penalty'] != 25 or not r['missed'] or o['why'] not in r['fb']:
            fails.append('%s: an error, but marked %s, cost %s, missed %s, feedback %r' % (
                where, r['cls'], r['penalty'], r['missed'], r['fb'][:60]))


# ------------------------------------------------------------------ self-test
OLD_MARK = "  const o = st.opts.find(x=>x.t === btn.dataset.val);\n"
PLANT_MARK = ("  const o0 = st.opts.find(x=>x.t === btn.dataset.val);\n"
              "  const kk = ('keyed' in st) ? currentQ.ops[st.keyed].correct : null;\n"
              "  const o = (kk && o0.op !== kk) ? Object.assign({}, o0, {c: 'err', why: 'Wrong move.'}) : o0;\n")


def run(html, quick=False):
    fails = []
    data = load(html, fails)
    if data is None:
        return fails, 0, 0, 0
    n_states, n_opts = check_data(data, fails)
    played = play(html, data, fails, quick=quick)
    return fails, n_states, n_opts, played


def selftest(html):
    out = []
    # 1. the old single-key marking: only the keyed move accepted
    assert OLD_MARK in html, 'the marking line the self-test plants against is not in the page'
    f, *_ = run(html.replace(OLD_MARK, PLANT_MARK, 1), quick=True)
    out.append(('the old single-key marking', any('x2 on x/2' in x or 'slower, but marked' in x for x in f), f))
    # 2. a mislabelled error: L1's carry-across slip labelled optimal
    bad = '"t":"3x = 22 + 7","c":"err"'
    assert bad in html, 'the error the self-test relabels is not in the page'
    f, *_ = run(html.replace(bad, '"t":"3x = 22 + 7","c":"opt"', 1), quick=True)
    out.append(('a mislabelled error (L1 carry-across as optimal)', any('changes the solution' in x for x in f), f))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--against', help='verify another copy of the page')
    ap.add_argument('--no-selftest', action='store_true')
    a = ap.parse_args()
    html = open(a.against or GAME, encoding='utf-8').read()
    fails, n_states, n_opts, played = run(html)
    if not a.against and not a.no_selftest:
        for name, caught, f in selftest(html):
            print('  self-test %-48s %s' % (name, 'caught: ' + (f[0] if f else '') [:110] if caught else 'NOT CAUGHT'))
            if not caught:
                fails.append('self-test: %s was not caught' % name)
    print('linear-equation-solver: %d states, %d options re-derived; %d marked in Chromium at 390px' % (n_states, n_opts, played))
    for x in fails:
        print('FAIL  ' + x)
    print('FAILED' if fails else 'PASS')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
