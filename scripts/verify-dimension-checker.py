#!/usr/bin/env python3
# ci-line: B4 | Dimension Checker (every key and option checked by dimension algebra, worked steps recomputed, every item marked in Chromium) |
"""Dimension Checker: every key and option checked by dimension algebra; every worked step recomputed; every item
marked in Chromium.

The game (28 multiple-choice items, 20 a session) asks whether equations are dimensionally homogeneous and what
dimensions a quantity has. Its bank was keyed by hand; the tranche 5 audit of 6 Oct 2026 found s = ut + at^2
keyed "No" with the true "Yes - all terms are [L]" marked wrong, and two items (Stokes' law, P = I^2 R) that need
dimensions the page never gives, so "Cannot check" was a true answer.

Dimensions are vectors of powers of M, L, T and A (current). TARGETS below gives each item's answer as dimension
algebra on the quantities in its prompt (DIM) or, for a verdict, the computed truth (homogeneous or not) and the
reviewed key. Then:
  the key's dimensions (an option "[M L T^-2]", or the bracket in "Yes - both sides are [...]") equal the target;
  every wrong option's dimensions differ from it; a "Yes"/"No" key agrees with the computed homogeneity and
  every wrong option that agrees with it differs in its reason;
  an item whose answer needs a quantity's dimensions not in M, L, T (current; viscosity; resistance) states them
  in its prompt or context (t5-002, t5-004), and no option says it "cannot" be checked when the item gives all
  it needs;
  every worked step's chain ("ut: [L T^-1][T] = [L]", "[A] = [B] / [C]") is evaluated: each side of every '='
  equal, each side of every '≠' different;
  in Chromium (390x844) every item is shown through the game's own nextQ() with its options from MaffsOptions,
  every option clicked through handleAnswer(): the key marked right, the others wrong; a wrong answer shows the
  worked solution and the shared Next control (MaffsNext, canon 7.6), not a hand-rolled button.
A self-test plants three of the audit's own faults back into a copy of the page (t5-001: s = ut + at^2 keyed No;
t5-002: Stokes' law without mu's dimensions; t5-004: P = I^2 R without R's); each must FAIL naming its item.

    python scripts/verify-dimension-checker.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'dimension-checker'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
SUPS = {'⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-'}


def D(M=0, L=0, T=0, A=0):
    return (M, L, T, A)


def mul(*ds):
    return tuple(sum(c) for c in zip(*ds)) if ds else D()


def pw(d, n):
    return tuple(c * n for c in d)


def inv(d):
    return pw(d, -1)


ONE = D()
M_, L_, T_, A_ = D(M=1), D(L=1), D(T=1), D(A=1)
VEL, ACC = D(L=1, T=-1), D(L=1, T=-2)
FORCE = mul(M_, ACC)
ENERGY = mul(FORCE, L_)
POWER = mul(ENERGY, inv(T_))
PRESS = mul(FORCE, pw(L_, -2))
VISC = D(M=1, L=-1, T=-1)
RES = D(M=1, L=2, T=-3, A=-2)

# Each item: ('dims', target) for "what are the dimensions"; ('homog', lhs, [terms], key) for yes/no items,
# where key is the reviewed key text; ('pick', key, why) for a reviewed key with its dimension check done by hand.
TARGETS = [
    ('homog', VEL, [VEL, mul(ACC, T_)]),                                        # v = u + at
    ('homog', FORCE, [mul(M_, VEL)]),                                           # F = mv
    ('homog', ENERGY, [mul(M_, pw(VEL, 2))]),                                   # E = 1/2 m v^2
    ('homog', POWER, [mul(FORCE, VEL)]),                                        # P = Fv
    ('homog', L_, [mul(VEL, T_), mul(ACC, pw(T_, 2))]),                         # s = ut + at^2 (t5-001)
    ('homog', POWER, [mul(pw(A_, 2), RES)]),                                    # P = I^2 R (t5-004)
    ('homog', PRESS, [mul(FORCE, pw(L_, 2))]),                                  # pressure = force x area
    ('homog', pw(VEL, 2), [pw(VEL, 2), mul(ACC, L_)]),                          # v^2 = u^2 + 2as
    ('dims', FORCE), ('dims', ENERGY), ('dims', PRESS), ('dims', mul(M_, VEL)), ('dims', POWER),
    ('dims', mul(M_, pw(L_, -3))), ('dims', ENERGY), ('dims', PRESS),
    ('homog', ENERGY, [mul(M_, ACC, L_), mul(M_, pw(VEL, 3))]),                 # E = mgh + 1/2 m v^3
    ('homog', FORCE, [mul(M_, pw(VEL, 2), inv(L_)), mul(M_, ACC)]),             # F = mv^2/r + ma
    ('homog', POWER, [mul(pw(FORCE, 2), VEL)]),                                 # P = F^2 v
    ('dims', mul(FORCE, pw(L_, 3), inv(L_))),                                   # EI = F L^3 / y
    ('dims', VISC),                                                             # Reynolds
    ('dims', mul(FORCE, inv(L_))),                                              # spring constant
    ('dims', ONE), ('dims', PRESS), ('dims', inv(T_)),
    ('homog', FORCE, [mul(VISC, L_, VEL)]),                                     # Stokes (t5-002)
    ('dims', ACC), ('dims', mul(pw(L_, 3), inv(T_))),
]
AUDIT = {4: 't5-001', 25: 't5-002', 5: 't5-004'}
# Quantities outside M, L, T that an item must state when it needs them: (pattern in the prompt, text to state).
NEEDS = [(r'I²R', r'\[M L² T⁻³ A⁻²\]'), (r'6πμrv', r'\[M L⁻¹ T⁻¹\]')]


def parse_dim(b):
    """'[M L⁻¹ T⁻²]' (inside of one bracket) as a vector; '1' is dimensionless."""
    d = {'M': 0, 'L': 0, 'T': 0, 'A': 0}
    b = b.strip()
    if b in ('1', ''):
        return ONE
    for m in re.finditer(r'([MLTA])([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]*)', b):
        e = ''.join(SUPS[ch] for ch in m.group(2))
        d[m.group(1)] += int(e) if e else 1
    if re.sub(r'[MLTA⁻⁰¹²³⁴⁵⁶⁷⁸⁹\s]', '', b):
        raise ValueError('cannot read dimensions [%s]' % b)
    return D(d['M'], d['L'], d['T'], d['A'])


def bracket_expr(s):
    """A product/quotient of bracket groups ('[M][L T⁻¹]²', '[M L² T⁻²]/([M][L])'); None if it has no bracket."""
    if '[' not in s or re.search(r'\[[^\]]*[a-z][^\]]*\]', s):
        return None          # no bracket, or a symbol such as [g] still to be found
    s = re.sub(r'[½]|\d+π|2π|6π|\b\d+\b', '', s)
    num, _, den = s.partition('/')
    def prod(part):
        out = ONE
        for m in re.finditer(r'\[([^\]]*)\]([⁰¹²³⁴⁵⁶⁷⁸⁹]*)', part):
            e = ''.join(SUPS[ch] for ch in m.group(2))
            out = mul(out, pw(parse_dim(m.group(1)), int(e) if e else 1))
        return out
    return mul(prod(num), inv(prod(den))) if den else prod(num)


def check_steps(fails, w, steps):
    for st in steps:
        body = re.split(r' — |✓|✗|, not ', re.sub(r'\((?:[a-z ]+)\)', '', st))[0]
        body = body.split(':', 1)[1] if re.match(r'^[^\[]*:', body) else body
        if '≠' in body:
            l, r = body.split('≠', 1)
            try:
                a, b = bracket_expr(l), bracket_expr(r)
            except ValueError as e:
                fails.append('%s: worked step %r: %s' % (w, st, e))
                continue
            if a is not None and b is not None and a == b:
                fails.append('%s: worked step %r says ≠ but both sides are %s' % (w, st, a))
            body = l
        sides = [p for p in body.split('=')]
        try:
            vals = [bracket_expr(p) for p in sides]
        except ValueError as e:
            fails.append('%s: worked step %r: %s' % (w, st, e))
            continue
        vals = [v for v in vals if v is not None]
        for a, b in zip(vals, vals[1:]):
            if a != b:
                fails.append('%s: worked step %r: %s ≠ %s' % (w, st, a, b))


def opt_dims(o):
    m = re.search(r'\[([^\]]*)\]', o)
    if 'Dimensionless' in o and not m:
        return ONE
    return parse_dim(m.group(1)) if m else None


def check_bank(fails, bank):
    if len(bank) != len(TARGETS):
        fails.append('bank: %d items, TARGETS has %d (review the new items and extend TARGETS)' % (len(bank), len(TARGETS)))
        return
    for i, (q, tg) in enumerate(zip(bank, TARGETS)):
        w = 'item %d (%s)%s' % (i, q['p'], ' (dimension-checker-%s)' % AUDIT[i] if i in AUDIT else '')
        opts = [q['c']] + q['d']
        if len(set(opts)) != 4:
            fails.append('%s: %d options, not 4 distinct' % (w, len(set(opts))))
        text = q['p'] + ' ' + (q.get('ctx') or '')
        for pat, need in NEEDS:
            if re.search(pat, q['p']) and not re.search(need, text):
                fails.append('%s: the answer needs dimensions the item never gives (%s)' % (w, need.replace('\\', '')))
        try:
            check_steps(fails, w, q.get('s') or [])
            dims = [opt_dims(o) for o in opts]
        except ValueError as e:
            fails.append('%s: %s' % (w, e))
            continue
        if tg[0] == 'dims':
            if dims[0] != tg[1]:
                fails.append('%s: keyed %s, the dimensions are %s' % (w, q['c'], tg[1]))
            for o, d in zip(opts[1:], dims[1:]):
                if d == tg[1]:
                    fails.append('%s: the wrong option %s has the right dimensions (SR-16)' % (w, o))
            continue
        _, lhs, terms = tg
        homog = all(t == lhs for t in terms)
        key_yes = q['c'].startswith('Yes') or q['c'].startswith('Neither')
        if key_yes != homog:
            fails.append('%s: keyed %r, but the equation %s homogeneous' % (w, q['c'], 'is' if homog else 'is not'))
        if dims[0] is not None and homog and dims[0] != lhs:
            fails.append('%s: the key quotes %s, the terms are %s' % (w, dims[0], lhs))
        for o, d in zip(opts[1:], dims[1:]):
            says_yes = o.startswith('Yes') or o.startswith('Neither')
            if says_yes and homog and (d is None or d == lhs):
                fails.append('%s: the wrong option %r is also right (SR-16)' % (w, o))


SWEEP_JS = r"""() => {
  window.setTimeout = () => 0; window.requestAnimationFrame = () => 0;
  const out = [];
  QS.forEach((q, i) => {
    for (const pick of [q.c, ...q.d]) {
      pool = [q]; qIdx = 0; total = 0; score = 0; correctN = 0;
      nextQ();
      const shown = [...document.querySelectorAll('#options .opt-btn')].map(b => b.dataset.val);
      if (shown.length !== 4 || [q.c, ...q.d].some(v => !shown.includes(v))) out.push([i, pick, 'options shown ' + JSON.stringify(shown)]);
      if ((q.ctx || '') !== document.getElementById('context').textContent) out.push([i, pick, 'context not shown']);
      const b = [...document.querySelectorAll('#options .opt-btn')].find(x => x.dataset.val === pick);
      if (!b) { out.push([i, pick, 'not on screen']); continue; }
      b.click();
      const right = b.classList.contains('correct');
      if (right !== (pick === q.c)) out.push([i, pick, right ? 'marked right' : 'marked wrong']);
      if (pick !== q.c) {
        const sol = document.getElementById('solution');
        if (!sol.classList.contains('show')) out.push([i, pick, 'no worked solution shown']);
        if (sol.querySelector('.next-btn')) out.push([i, pick, 'a hand-rolled Next button (canon 7.6: MaffsNext)']);
        if (window.MaffsNext) MaffsNext.clear(sol);
        sol.className = 'solution';
      }
    }
  });
  return out;
}"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw_:
            browser = pw_.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof QS !== "undefined"', timeout=15000)
            bank = page.evaluate('() => QS')
            page.evaluate("() => { document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));"
                          " document.getElementById('game').classList.add('active'); }")
            for i, pick, what in page.evaluate(SWEEP_JS):
                fails.append('item %d in Chromium: option %r %s' % (i, pick, what))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return bank
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('item 4 ', 't5-001: s = ut + at² keyed No', "c:'Yes — all terms are [L]',d:['No — it should be ½at², so the dimensions do not match'",
     "c:'No — it should be ½at², so the dimensions do not match',d:['Yes — all terms are [L]'"),
    ('item 25 ', "t5-002: Stokes' law without mu's dimensions", "ctx:'Viscosity μ has dimensions [M L⁻¹ T⁻¹].',", ''),
    ('item 5 ', "t5-004: P = I²R without R's dimensions",
     "ctx:'Current I has dimensions [A] (amperes); resistance R has dimensions [M L² T⁻³ A⁻²].',", ''),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bank = play(fails, html)
    if bank:
        check_bank(fails, bank)
    print('%s: %d items, every key, option and worked step checked by dimension algebra, every option clicked in'
          ' Chromium' % (SLUG, len(bank or [])))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, old, new in PLANTS:
            if html.count(old) != 1:
                print('  self-test %-44s *** CANNOT PLANT (%d) ***' % (what, html.count(old)))
                ok = False
                continue
            rep = []
            planted = play(rep, html.replace(old, new))
            if planted:
                check_bank(rep, planted)
            hit = [f for f in rep if f.startswith(tag)]
            ok = ok and bool(hit)
            print('  self-test %-44s %s' % (what, ('caught: ' + hit[0][:110]) if hit else '*** MISSED ***'))
    for f in fails:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
