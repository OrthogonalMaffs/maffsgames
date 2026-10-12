#!/usr/bin/env python3
# ci-line: Formula Forge (every rearrangement checked in SymPy: the key solves its formula, no wrong option does or equals it, every worked line holds; every option pressed in Chromium) |
"""Formula Forge: "make X the subject" from four options, in four stages, at three levels.

Static bank, read from the page as served: `Q.gcse` and `Q.level4`, each with stages s1-s4 of items `{formula, subject, correct,
distractors[3], hint1, hint2, steps, ctx?, misconception?}`; `Q.alevel` is the GCSE stages (open finding formula-forge-t4-003).
A session deals 6 a stage, stages in order. The mark is `button.dataset.val === q.correct`; a wrong answer shows the worked steps.

Every formula, option and worked line is read into SymPy here (read() below: \\dfrac, \\frac, \\sqrt, \\sqrt[n], Greek letters,
subscripts, letters side by side multiply; every symbol positive, as the quantities are physical; Jon, 12 Oct 2026: a verifier may
carry its own TeX reader until the home lane gives bank_common an exact one). Then:
  - the key is "subject = expression", and put back into the formula it makes it an identity (for a chain such as
    P = I^2 R = V^2/R, one of its equalities);
  - no wrong option does, none equals the key in value, no two are equal in value, and the four are different strings (SR-4,
    SR-16); three items with two wrong options equal in value are the expected failure formula-forge-v20-001 (open for Jon);
  - every worked line that is an equation (after any \\text{...} words) holds when the key is put in for the subject, and the
    last line is the key; a Hint 2 that is an equation is checked the same way;
  - KaTeX (pinned local copy) parses every formula, option and worked line;
  - sessions: startGame() at each level, dealt three times: 6 a stage (or the whole stage when it has fewer), stages in order,
    no item twice;
  - in Chromium (390x844) every option of every item is pressed through the game's own buttons: the key is marked correct and
    scores; any other is marked wrong, the key is shown, the worked solution shows the item's lines, and Next is mounted.
Not asserted (open findings, left open): prose in Hint 2 losing its spaces in KaTeX (r-001, t4-004), Hint 2 alone showing the
previous question's hints (t4-002), pool sizes and A-Level reusing GCSE (t4-003), stage labels (t4-005), the unstated positive
root and the Hint 2s that give the answer (t4-006).

    python scripts/verify-formula-forge.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'formula-forge'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LEVELS = ('gcse', 'level4')
GREEK = {'pi', 'rho', 'sigma', 'epsilon', 'varepsilon', 'theta', 'lambda', 'omega', 'mu', 'alpha', 'beta', 'Delta', 'eta', 'tau', 'phi'}
SYMS = {}
# Two wrong options equal in value to each other (SR-4: four distinct options), every symbol positive. Left open for Jon as
# formula-forge-v20-001 (replacing a distractor is new content); the check fails any other item with such a pair, and fails if
# one of these stops having it.
EQUAL_PAIRS = {('v^2 = u^2 + 2as', 'v'): 'formula-forge-v20-001', ('c^2 = a^2 + b^2', 'a'): 'formula-forge-v20-001',
               ('v^2 = u^2 + 2as', 'u'): 'formula-forge-v20-001'}


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
        if s.startswith('\\cdot', i) or s.startswith('\\times', i):
            out.append(('op', '*'))
            i += 5 if s.startswith('\\cdot', i) else 6
            continue
        if s.startswith('\\,', i) or s.startswith('\\;', i) or s.startswith('\\!', i):
            i += 2
            continue
        m = re.match(r'\\Delta\s*([A-Za-z])(?:_(\{[^}]*\}|[A-Za-z0-9]))?', s[i:])
        if m:                           # \Delta L, \Delta T: one quantity
            out.append(('atom', 'S("Delta_%s%s")' % (m.group(1), ('_' + m.group(2).strip('{}')) if m.group(2) else '')))
            i += m.end()
            continue
        m = re.match(r'\\([A-Za-z]+)', s[i:])
        if m:
            name = m.group(1)
            if name not in GREEK:
                raise ValueError('unknown TeX command \\%s in %r' % (name, s))
            j = i + m.end()
            if j < len(s) and s[j] == '_':
                sub, j = group(s, j + 1) if s[j + 1] == '{' else (s[j + 1], j + 2)
                name += '_' + sub
            out.append(('atom', 'pi' if name == 'pi' else 'S("%s")' % name))
            i = j
            continue
        if ch.isalpha():
            name, j = ch, i + 1
            if j < len(s) and s[j] == '_':
                sub, j = group(s, j + 1) if s[j + 1] == '{' else (s[j + 1], j + 2)
                name += '_' + sub
            out.append(('atom', 'S("%s")' % name))
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
    try:
        return sp.sympify(expr(s), locals={'S': sym, 'Rational': sp.Rational, 'sqrt': sp.sqrt, 'pi': sp.pi})
    except ValueError:
        raise
    except Exception as e:
        raise ValueError('cannot read %r (%s): %s' % (s, expr(s), e))


def zero(e):
    return sp.simplify(e) == 0


def equation(s):
    """The maths of a worked line: drop \\text{...} words and spacing; None when no equation is left."""
    t = re.sub(r'\\text\{[^}]*\}', ' ', s)
    t = re.sub(r'\\quad|\\qquad', ' ', t).strip()
    if ':' in t:                        # "Subtract u: v - u = at": the maths is after the colon
        t = t.rsplit(':', 1)[1].strip()
    return t if t.count('=') >= 1 and re.search(r'[A-Za-z0-9]', t) else None


def holds(eq, subj, value, chain=()):
    """Every '=' in the line is true with the key put in for the subject. For a chain formula (sigma = E eps = F/A) the chain's
    head may also be replaced by each of its equal parts, so a line restating a link of the chain holds."""
    sides = [read(p) for p in eq.split('=')]
    for x in sides[1:]:
        d = (sides[0] - x).subs(subj, value)
        if not (zero(d) or any(zero(d.subs(h, v)) for h, v in chain)):
            return False
    return True


def check_item(fails, where, q):
    opts = [q['correct']] + list(q['distractors'])
    if len(q['distractors']) != 3 or len(set(opts)) != 4:
        fails.append('options: %s: %d distractors, %d different strings with the key' % (where, len(q['distractors']), len(set(opts))))
        return 0
    subj = read(q['subject'])
    if not isinstance(subj, sp.Symbol):
        fails.append('key: %s: the subject %r is not one symbol' % (where, q['subject']))
        return 0
    parts = [read(p) for p in q['formula'].split('=')]
    pairs = [(parts[a], parts[b]) for a in range(len(parts)) for b in range(a + 1, len(parts))]
    # a chain (P = I^2 R = V^2/R) is solved by a key that makes one of its equalities an identity
    solves = lambda v: any(zero((x - y).subs(subj, v)) for x, y in pairs)    # noqa: E731
    vals = []
    for o in opts:
        lhs, rhs = o.split('=', 1)
        if read(lhs) != subj:
            fails.append('options: %s: %r does not make %s the subject' % (where, o, q['subject']))
            return 0
        vals.append(read(rhs))
    key = vals[0]
    if not solves(key):
        fails.append('key: %s: %r does not solve %s for %s' % (where, q['correct'], q['formula'], q['subject']))
    solving = [o for o, v in zip(opts, vals) if solves(v)]
    if solving != [q['correct']]:
        fails.append('options: %s: the options that solve it are %r, the key is %r' % (where, solving, q['correct']))
    for k in range(1, 4):
        if zero(vals[k] - key):
            fails.append('options: %s: %r equals the key in value' % (where, opts[k]))
        for m in range(k + 1, 4):
            if zero(vals[k] - vals[m]):
                if k > 0 and (q['formula'], q['subject']) in EQUAL_PAIRS:
                    SEEN_PAIRS.add((q['formula'], q['subject']))
                else:
                    fails.append('options: %s: %r and %r are equal in value' % (where, opts[k], opts[m]))
    n = 0
    lines = q.get('steps') or []
    chain = [(parts[0], v) for v in parts[1:]] if len(parts) > 2 and isinstance(parts[0], sp.Symbol) else []
    for st in [piece for line in lines for piece in line.split('\\implies')]:
        eq = equation(st)
        if eq is None:
            continue
        try:
            ok = holds(eq, subj, key, chain)
        except ValueError as e:
            fails.append('working: %s: the line %r cannot be read here (%s)' % (where, st, e))
            continue
        n += 1
        if not ok:
            fails.append('working: %s: the worked line %r does not hold for the key' % (where, st))
    if lines:
        last = equation(lines[-1])
        if last is not None:
            ends = [read(p) for p in last.split('=')]
            if not any(e == subj for e in ends) or not any(zero(e - key) for e in ends if e != subj):
                fails.append('working: %s: the last worked line %r is not the key' % (where, lines[-1]))
    h2 = (q.get('hint2') or '').replace('\\implies', '. ')
    for seg in re.split(r'(?<=[.!?])\s+', h2):
        seg = seg.strip().rstrip('.')
        if '=' in seg and not re.search(r'[A-Za-z]{3,}', re.sub(r'\\[A-Za-z]+', '', seg)):
            try:
                if not holds(seg, subj, key, chain):
                    fails.append('working: %s: Hint 2 says %r, which does not hold for the key' % (where, seg))
                n += 1
            except ValueError:
                pass
    return n


SEEN_PAIRS = set()


def check_bank(fails, bank):
    SEEN_PAIRS.clear()
    n_items = n_lines = 0
    for lv in LEVELS:
        for st in ('s1', 's2', 's3', 's4'):
            for i, q in enumerate(bank[lv][st], 1):
                where = '%s %s item %d (%s; %s)' % (lv, st, i, q['formula'], q['subject'])
                try:
                    n_lines += check_item(fails, where, q)
                except ValueError as e:
                    fails.append('key: %s: cannot be read here (%s)' % (where, e))
                n_items += 1
    for k, fid in EQUAL_PAIRS.items():
        if k not in SEEN_PAIRS:
            fails.append('options: the expected equal pair in %s (%s) is gone: close the finding and remove it from EQUAL_PAIRS' % (k, fid))
    return n_items, n_lines


RENDER_JS = r"""(bank) => { const bad = [];
  for (const lv of Object.keys(bank)) for (const st of Object.keys(bank[lv])) for (const q of bank[lv][st])
    for (const t of [q.formula, q.correct].concat(q.distractors, q.steps || []))
      try { katex.renderToString(t, {throwOnError: true}); } catch (e) { bad.push(lv + ' ' + st + ': ' + t + ' -> ' + e.message); }
  return bad; }"""
SESSION_JS = r"""() => { const out = {};
  for (const lv of ['gcse', 'alevel', 'level4']) { out[lv] = [];
    const bank = Q[lv];
    for (let k = 0; k < 3; k++) { level = lv; const p = buildPool();
      out[lv].push(p.map(q => [q.stage, bank['s' + q.stage].findIndex(x => x.formula === q.formula && x.subject === q.subject)])); } }
  return {deals: out, sizes: Object.fromEntries(['gcse', 'alevel', 'level4'].map(lv => [lv, [1, 2, 3, 4].map(s => Q[lv]['s' + s].length)]))}; }"""
MARK_JS = r"""([lv, st, i]) => {
  level = lv; startGame();
  const item = Q[lv][st][i], wanted = [item.correct].concat(item.distractors), out = [];
  for (let k = 0; k < 4; k++) {
    pool = [Object.assign({}, item, {stage: +st.slice(1)})]; qIdx = 0; total = 0; score = 0; nextQ();
    const btns = [...document.querySelectorAll('#options .opt-btn')];
    const target = btns.find(b => b.dataset.val === wanted[k]);
    if (!target) { out.push({k: k, missing: wanted[k], shown: btns.map(b => b.dataset.val)}); continue; }
    target.click();
    const sol = document.getElementById('solution');
    out.push({k: k, n: btns.length, cls: target.className, keycls: btns.find(b => b.dataset.val === item.correct).className,
              score: score, solShown: sol.classList.contains('show'), solSteps: sol.querySelectorAll('.step').length,
              next: sol.querySelectorAll('button').length});
    MaffsLock.clearTimers();
  }
  return out; }"""


def mark_checks(fails, page, bank):
    for lv in LEVELS:
        for st in ('s1', 's2', 's3', 's4'):
            for i, q in enumerate(bank[lv][st]):
                where = '%s %s item %d (%s; %s)' % (lv, st, i + 1, q['formula'], q['subject'])
                for r in page.evaluate(MARK_JS, [lv, st, i]):
                    if r.get('missing'):
                        fails.append('marking: %s: the option %r is not shown (%r)' % (where, r['missing'], r['shown']))
                        break
                    if r['k'] == 0:
                        ok = r['n'] == 4 and 'correct' in r['cls'].split() and r['score'] > 0 and not r['solShown']
                    else:
                        ok = ('wrong' in r['cls'].split() and 'correct' in r['keycls'].split() and r['score'] == 0 and r['solShown']
                              and r['solSteps'] == len(q.get('steps') or []) and r['next'] >= 1)
                    if not ok:
                        fails.append('marking: %s, option %d (%s): %r' % (where, r['k'], 'the key' if r['k'] == 0 else 'a distractor', r))
                        break


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
            page.wait_for_function('typeof Q !== "undefined" && typeof katex !== "undefined"', timeout=15000)
            bank = page.evaluate('() => JSON.parse(JSON.stringify({gcse: Q.gcse, level4: Q.level4}))')
            n_items, n_lines = check_bank(fails, bank)
            for msg in page.evaluate(RENDER_JS, bank):
                fails.append('render: KaTeX cannot parse %s' % msg)
            ses = page.evaluate(SESSION_JS)
            for lv, deals in ses['deals'].items():
                want_stages = [s for s in (1, 2, 3, 4) for _ in range(min(6, ses['sizes'][lv][s - 1]))]
                for d in deals:
                    if [s for s, _ in d] != want_stages or len(set(map(tuple, d))) != len(d) or any(ix < 0 for _, ix in d):
                        fails.append('session: %s dealt %r, expected stages %r with no item twice' % (lv, d, want_stages))
                        break
            mark_checks(fails, page, bank)
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            stats = {'items': n_items, 'lines': n_lines}
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('a wrong key (u = v + at)', 'key:', [("correct:'u = v - at',distractors:['u = v + at','u = at - v','u = \\\\dfrac{v}{at}']",
                                           "correct:'u = v + at',distractors:['u = v - at','u = at - v','u = \\\\dfrac{v}{at}']")]),
    ('SR-4/16: a distractor equal to the key (u = -at + v)', 'options:',
     [("correct:'u = v - at',distractors:['u = v + at','u = at - v','u = \\\\dfrac{v}{at}']",
       "correct:'u = v - at',distractors:['u = -at + v','u = at - v','u = \\\\dfrac{v}{at}']")]),
    ('a wrong worked line (v + at = u)', 'working:', [("'\\\\text{Subtract } at \\\\text{ from both sides}','v - at = u','u = v - at'",
                                                      "'\\\\text{Subtract } at \\\\text{ from both sides}','v + at = u','u = v - at'")]),
    ('SR-4: a new pair of wrong options equal in value (y + 7 and 7 + y)', 'options:',
     [("correct:'x = y - 7',distractors:['x = y + 7','x = 7 - y','x = 7y']", "correct:'x = y - 7',distractors:['x = y + 7','x = 7 + y','x = 7y']")]),
    ('a misspelt TeX command in an option', 'render:', [("'u = at - v','u = \\\\dfrac{v}{at}']", "'u = at - v','u = \\\\dfac{v}{at}']")]),
    ('marking by the first character only', 'marking:', [("const ok=btn.dataset.val===q.correct;", "const ok=btn.dataset.val[0]===q.correct[0];")]),
    ('five a stage dealt, not six', 'session:', [("const s1=shuffle([...bank.s1]).slice(0,6);", "const s1=shuffle([...bank.s1]).slice(0,5);")]),
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
    print('%s: %d items (GCSE and Level 4; A-Level reuses GCSE), every key solved back into its formula in SymPy, every option '
          'classified, %d worked lines and Hint 2 equations checked; every option pressed in Chromium' % (SLUG, st.get('items', 0), st.get('lines', 0)))
    for k, fid in sorted(EQUAL_PAIRS.items()):
        print('  expected failure left open: %s (%s, make %s the subject: two wrong options equal in value)' % (fid, k[0], k[1]))
    print('  not asserted (open): Hint 2 prose spacing (r-001, t4-004), Hint 2 alone (t4-002), pools (t4-003), stage labels (t4-005), '
          'positive root and Hint 2 giving the answer (t4-006)')
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
