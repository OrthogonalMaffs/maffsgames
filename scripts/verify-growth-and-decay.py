#!/usr/bin/env python3
# ci-line: Growth and Decay (keys recomputed from each printed model) |
"""Independent verification of growth-and-decay's keys (todo §1.36; audit §1.2 items 1-4).

Each scenario prints its model (modelLatex). That equation, not the game's graphFn, is
the source of truth. It is parsed into SymPy; a constant the model leaves as k (or N₀) is
solved from the condition the scenario's own prompt states ("Given that L = 100 when
T = 24, find the value of k"), or taken from the prompt where the prompt gives it
("… and k = 800"). Then every typed sub-question is recomputed from its own prompt:

  - "… when X = v"                 the model's value at v;
  - "Find X when Y = c"            the X where the model equals c;
  - "Given Y = a when X = b, find k" (or "confirm N₀"): the constant;
  - a value at t = 0 ("Confirm the initial value", "Find P₀ when t = 0").

Where the prompt states a precision (n significant figures, n decimal places) the key
must be the true value rounded to it (§1.36: the three keys at :229, :380 and :404 were
not); where none is stated the key must be the true value at the precision it is stored
to. A stored sf field must agree with the s.f. the prompt asks. The game's graphFn, which
draws the curve, must agree with the model to 0.01% across the graph's range (CM2's drew
k = 161.2 for a stated condition that gives 162.4).

The marking is then played in the page through the game's own loadSQ / checkNumSQ /
checkSQ4: the true value, rounded as the prompt asks, must be marked correct. The bands
themselves are the shared precision marker's business (§1.36), not checked here.

A fault-injection self-test (a wrong key, a key at the wrong precision, a graph that
disagrees with its model, a reworded prompt) must FAIL each time; it runs unless
--no-selftest.

    python scripts/verify-growth-and-decay.py [--verbose] [--no-selftest]
"""
import argparse
import copy
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication,
                                        parse_expr, standard_transformations)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'growth-and-decay'
TRANSFORMS = standard_transformations + (implicit_multiplication, convert_xor)
K = sp.Symbol('K')          # the model's unknown constant (k, or N₀)

# Prompts whose model differs from the printed one, stated in the prompt itself.
MODEL_OVERRIDES = {
    ('L4_2', 'sq3'): ('where model is T = 20 + ke^(−0.08t)', '20 + K*exp(-0.08*t)'),
}


class Report:
    def __init__(self):
        self.fails = []

    def fail(self, sid, what, detail):
        self.fails.append('%s %s: %s' % (sid, what, detail))


def _braces(s, i):
    depth = 0
    for j in range(i, len(s)):
        depth += {'{': 1, '}': -1}.get(s[j], 0)
        if depth == 0:
            return j + 1
    raise ValueError('unbalanced braces in %r' % s)


def parse_model(tex):
    """'L = k \\times 0.98^T' -> (left name, SymPy expression in K and one variable)."""
    left, right = [p.strip() for p in tex.split('=', 1)]
    right = right.replace(r'\times', '*').replace('N_0', 'K').replace('−', '-')
    right = re.sub(r'(?<![A-Za-z])k(?=e\^)', 'K*', right)        # ke^{...}  -> K*exp(...)
    right = re.sub(r'(?<![A-Za-z])k(?![A-Za-z])', 'K', right)     # k \times …
    right = re.sub(r'(?<![A-Za-z])e\^([A-Za-z])', r'exp(\1)', right)  # e^y      -> exp(y)
    out, i = '', 0
    while i < len(right):
        if right.startswith('e^{', i) and (i == 0 or not right[i - 1].isalpha()):
            j = _braces(right, i + 2)
            out += 'exp(%s)' % right[i + 3:j - 1]
            i = j
        elif right.startswith('^{', i):
            j = _braces(right, i + 1)
            out += '^(%s)' % right[i + 2:j - 1]
            i = j
        else:
            out += right[i]
            i += 1
    names = {c: sp.Symbol(c) for c in set(re.findall(r'[A-Za-z]', out)) - set('expE') - {'K'}}
    names.update(K=K, exp=sp.exp, E=sp.E)
    return left, parse_expr(out, local_dict=names, transformations=TRANSFORMS)


def number(text):
    """'10,000' -> 10000; '1×10⁶' -> 1000000; '0.1s' -> 0.1."""
    text = text.strip().rstrip('.s').replace(',', '')
    m = re.match(r'^([\d.]+)\s*×\s*10([⁰¹²³⁴⁵⁶⁷⁸⁹]+)$', text)
    if m:
        exp = int(m.group(2).translate(str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹', '0123456789')))
        return sp.nsimplify(m.group(1)) * 10 ** exp
    return sp.nsimplify(text)


NUM = r'([\d.,]+(?:\s*×\s*10[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?s?)'


def asked(prompt):
    m = re.search(r'(\d) significant figures?', prompt)
    if m:
        return ('sf', int(m.group(1)))
    m = re.search(r'(\d) decimal places?', prompt)
    if m:
        return ('dp', int(m.group(1)))
    return None


def to_decimal(x):
    return Decimal(str(sp.N(x, 30)))


def round_as(x, how):
    d = to_decimal(x)
    if how[0] == 'dp':
        return d.quantize(Decimal(1).scaleb(-how[1]), rounding=ROUND_HALF_UP)
    if d == 0:
        return d
    return d.quantize(Decimal(1).scaleb(d.adjusted() - how[1] + 1), rounding=ROUND_HALF_UP)


def stored_dp(v):
    s = repr(float(v))
    if 'e' in s:
        s = format(Decimal(s), 'f')
    return 0 if s.endswith('.0') else len(s.split('.')[1]) if '.' in s else 0


def recompute(s, key):
    """(true value, how it is asked) for sub-question `key`, from its prompt alone."""
    sq = s[key]
    prompt = sq['prompt']
    left, model = parse_model(s['modelLatex'])
    over = MODEL_OVERRIDES.get((s['id'], key))
    if over:
        if over[0] not in prompt:
            raise ValueError('override no longer matches the prompt')
        model = parse_expr(over[1], local_dict={'K': K, 't': sp.Symbol('t'), 'exp': sp.exp},
                           transformations=TRANSFORMS)
    var = [v for v in model.free_symbols if v != K]
    if len(var) != 1:
        raise ValueError('model %r: expected one variable' % s['modelLatex'])
    var = var[0]
    # the constant: stated in this prompt, else solved from the condition in sq3's prompt
    kval = None
    m = re.search(r'and k = ' + NUM, prompt)
    if m:
        kval = number(m.group(1))
    elif K in model.free_symbols:
        cond = re.search(r'Given (?:that )?(\w+) = ' + NUM + r' when (\w) = ' + NUM, s['sq3']['prompt'])
        if not cond:
            raise ValueError('the model has a constant and sq3 states no condition')
        kval = sp.solve(sp.Eq(model.subs(var, number(cond.group(4))), number(cond.group(2))), K)[0]
    find_k = re.search(r'find (?:the value of )?k\b|confirm N₀', prompt)
    if find_k:
        if K not in model.free_symbols:
            raise ValueError('asks for k but the model has none')
        return kval, asked(prompt)
    f = model.subs(K, kval) if kval is not None else model
    # "Find A when B = c": B the model's variable -> the value there ("Find L when T = 24",
    # "Find P₀ when t = 0"); B the modelled quantity -> solve for the variable ("Find t
    # when P = 10,000", "Find the half-life — when R = 40").
    m = re.match(r'Find (.+?) when (\w) = ' + NUM, prompt)
    if m and sp.Symbol(m.group(2)) != var:
        roots = [r for r in sp.solve(sp.Eq(f, number(m.group(3))), var) if r.is_real]
        if len(roots) != 1:
            raise ValueError('%d real solutions' % len(roots))
        return roots[0], asked(prompt)
    at = re.search(r'(?:when|after) (\w) = ' + NUM, prompt)
    if at and sp.Symbol(at.group(1)) == var:
        return f.subs(var, number(at.group(2))), asked(prompt)
    raise ValueError('prompt not understood: %r' % prompt)


def check_scenario(rep, s, graph_vals, verbose=False):
    sid = s['id']
    for key in ('sq1', 'sq3', 'sq4'):
        sq = s.get(key)
        if not sq:
            continue
        try:
            true, how = recompute(s, key)
        except Exception as e:  # noqa: BLE001  (an unreadable prompt is a finding)
            rep.fail(sid, key, 'cannot recompute %r: %s' % (sq['prompt'], e))
            continue
        if how:
            want = round_as(true, how)
            if Decimal(repr(float(sq['answer']))) != want:
                rep.fail(sid, key, '%r keyed %s; the model gives %s, %s to %d %s'
                         % (sq['prompt'], sq['answer'], sp.N(true, 8), want, how[1], how[0]))
        else:
            want = round_as(true, ('dp', stored_dp(sq['answer'])))
            if Decimal(repr(float(sq['answer']))).quantize(Decimal(1).scaleb(-stored_dp(sq['answer']))) != want:
                rep.fail(sid, key, '%r keyed %s; the model gives %s' % (sq['prompt'], sq['answer'], sp.N(true, 8)))
        if 'sf' in sq and how and how[0] == 'sf' and sq['sf'] != how[1]:
            rep.fail(sid, key, 'sf field %s, but the prompt asks %d s.f.' % (sq['sf'], how[1]))
    # the graph must draw the model (with the constant the stated condition gives)
    try:
        _, model = parse_model(s['modelLatex'])
        var = [v for v in model.free_symbols if v != K][0]
        if K in model.free_symbols:
            m = re.search(r'Given (?:that )?(\w+) = ' + NUM + r' when (\w) = ' + NUM, s['sq3']['prompt'])
            kval = sp.solve(sp.Eq(model.subs(var, number(m.group(4))), number(m.group(2))), K)[0]
            model = model.subs(K, kval)
        g = sp.lambdify(var, model, 'math')
        for x, y in graph_vals:
            want = g(x)
            if abs(y - want) > 1e-4 * max(abs(want), 1e-12):
                rep.fail(sid, 'graph', 'graphFn(%s) = %.6g but the model gives %.6g' % (x, y, want))
                break
    except Exception as e:  # noqa: BLE001
        rep.fail(sid, 'graph', 'cannot check: %s' % e)
    if verbose:
        print('  %-5s %s' % (sid, s['modelLatex']))


def check_bank(rep, bank, graphs, verbose=False):
    scenarios = [s for lvl in bank.values() for s in lvl]
    for s in scenarios:
        check_scenario(rep, s, graphs.get(s['id'], []), verbose)
    return scenarios


GRAPH_JS = """(id) => {
  const s = Object.values(Q).flat().find(q => q.id === id);
  const lo = s.graphXMin || 0, hi = s.graphXMax;
  const out = [];
  for (let k = 0; k <= 20; k++) { const x = lo + (hi - lo) * k / 20; out.push([x, s.graphFn(x)]); }
  return out;
}"""

PLAY_JS = """async (a) => {
  const q = Object.values(Q).flat().find(s => s.id === a.id);
  const realTimeout = window.setTimeout;
  window.setTimeout = () => 0;
  const out = {};
  try {
    G.questions = [q]; G.qIdx = 0; G.level = a.level;
    const order = q.sq_order.filter(n => n <= 3 || (n === 4 && G.level !== 'core'));
    for (const [n, v] of Object.entries(a.values)) {
      G.sqIdx = order.indexOf(Number(n));
      if (G.sqIdx < 0) continue;
      loadSQ(q);
      document.getElementById('sqInput').value = v;
      if (Number(n) === 4) checkSQ4(); else checkNumSQ(Number(n));
      out[n] = document.getElementById('sqFb').textContent;
    }
  } finally { window.setTimeout = realTimeout; }
  return out;
}"""


def typed_values(s):
    vals = {}
    for n in (1, 3, 4):
        sq = s.get('sq%d' % n)
        if not sq:
            continue
        try:
            true, how = recompute(s, 'sq%d' % n)
        except Exception:  # noqa: BLE001  (reported by check_scenario)
            continue
        vals[str(n)] = format(round_as(true, how), 'f') if how else format(to_decimal(true).normalize(), 'f')
    return vals


def check_played(rep, scenarios, played):
    for s in scenarios:
        for n, text in (played.get(s['id']) or {}).items():
            if 'Correct' not in text:
                rep.fail(s['id'], 'marking (sq%s)' % n, 'typed the true value as asked; the game said %r' % text.strip()[:100])


def load(patch_js=None):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/' + SLUG + '/?cb=verify', wait_until='load', timeout=20000)
            page.wait_for_function('typeof Q !== "undefined" && typeof checkSQ4 === "function"', timeout=8000)
            if patch_js:
                page.evaluate(patch_js)
            bank = page.evaluate('JSON.parse(JSON.stringify(Q))')
            graphs, played = {}, {}
            for lvl, items in bank.items():
                for s in items:
                    graphs[s['id']] = page.evaluate(GRAPH_JS, s['id'])
                    played[s['id']] = page.evaluate(PLAY_JS, dict(id=s['id'], level=lvl, values=typed_values(s)))
            browser.close()
            if errors:
                sys.exit('page errors: %s' % '; '.join(errors[:5]))
            return bank, graphs, played
    finally:
        proc.terminate()
        proc.wait()


def selftest(bank, graphs, played):
    lines, ok = [], True
    base = Report()
    check_played(base, check_bank(base, bank, graphs), played)
    clean = [s for lvl in bank.values() for s in lvl
             if s.get('sq4') and not any(f.startswith(s['id'] + ' ') for f in base.fails)]
    if not clean:
        return False, ['  self-test skipped: no clean scenario with an sq4']
    target = clean[0]['id']

    def expect(name, fn):
        nonlocal ok
        rep = Report()
        fn(rep)
        rep.fails = [f for f in rep.fails if f not in base.fails]
        caught = bool(rep.fails)
        ok = ok and caught
        lines.append('  self-test %-34s %s' % (name, ('caught: ' + rep.fails[0][:110]) if caught else '*** MISSED ***'))

    def mutated(fn):
        b = copy.deepcopy(bank)
        fn(next(s for lvl in b.values() for s in lvl if s['id'] == target))
        return b

    expect('wrong sq4 key (+0.3)', lambda rep: check_bank(rep, mutated(lambda s: s['sq4'].__setitem__('answer', round(s['sq4']['answer'] + 0.3, 4))), graphs))
    expect('sq1 key at 4 s.f. for a 3 s.f. ask', lambda rep: check_bank(rep, mutated(
        lambda s: s['sq1'].__setitem__('answer', float(round_as(recompute(s, 'sq1')[0], ('sf', 4))))), graphs))
    bad = dict(graphs)
    bad[target] = [(x, y * 1.01) for x, y in graphs[target]]
    expect('graph disagrees with its model', lambda rep: check_bank(rep, bank, bad))
    expect('reworded prompt', lambda rep: check_bank(rep, mutated(lambda s: s['sq4'].__setitem__('prompt', 'Describe the curve.')), graphs))
    _, _, lie = load("""(() => { const s = Object.values(Q).flat().find(q => q.id === %r);
        s.sq4.answer = s.sq4.answer + 1; })()""" % target)
    expect('sq4 marked against a wrong key', lambda rep: check_played(rep, clean[:1], lie))
    return ok, lines


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    bank, graphs, played = load()
    rep = Report()
    scenarios = check_bank(rep, bank, graphs, args.verbose)
    check_played(rep, scenarios, played)
    for f in rep.fails:
        print('FAIL ' + f)
    ok = not rep.fails
    if not args.no_selftest:
        s_ok, lines = selftest(bank, graphs, played)
        print('\nFault-injection self-test (patched copies; the file is never touched):')
        for ln in lines:
            print(ln)
        ok = ok and s_ok
    bad = {f.split(' ', 1)[0] for f in rep.fails}
    print('\n%s: %d FAIL(s) across %d of %d scenarios' % ('PASS' if ok else 'FAILED', len(rep.fails), len(bad), len(scenarios)))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
