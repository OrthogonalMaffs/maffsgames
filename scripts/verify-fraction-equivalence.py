#!/usr/bin/env python3
# ci-line: Fraction Snap (every pair's key and cross-multiplication recomputed, the generator drawn 20000 times, every pair marked both ways in Chromium) |
"""Fraction Snap (fraction-equivalence): is each pair of fractions equivalent? Every key recomputed, every
figure in the working recomputed, every pair marked both ways by the game's own guess(). Rewritten for
FRACTION-SNAP-REBUILD (19 Nov 2026).

Three levels, each its own leaderboard, read from the page as served (?level=year6, ks3, gcse):
  Year 6: a static bank, YEAR6_BANK, 15 dealt per session from it.
  KS3 and GCSE: generateQ(), two generators. Half the pairs are equivalent (kind 'yes'); each wrong pair is built from
    one misconception: 'add' (the same number added to top and bottom), 'one' (only the top or only the bottom
    multiplied) or 'near' (cross-products that differ by 1).
The key is whether n1/d1 = n2/d2, recomputed here with fractions.Fraction (the game's own test is never called).

Checks:
  Bank: every key by Fraction; every item's kind holds (yes: equivalent; add: the same k > 0 added to top and
    bottom; one: exactly one of top and bottom multiplied by an integer >= 2; near: |ad - bc| = 1); denominators only
    2, 3, 4, 5, 6, 8, 10 or 12; both fractions proper; no pair repeated in either order; at least 40 items; every
    wrong kind present.
  KS3 and GCSE: 20000 draws each in Chromium. Every key; every rule of the contract's item 3:
    KS3: the first fraction p/q proper and in simplest form, q 2 to 12; yes pm/qm (m 2-6); add (p+k)/(q+k) (k 1-5);
      one p/(qm), or pm/q with pm < q (m 2-6); near a proper c/d with |pd - qc| = 1, d 2 to max(12, 2q).
    GCSE: the first fraction pa/qa (a 2-6) of a base p/q as KS3; yes pb/qb (b 2-9, b != a); add (pa+k)/(qa+k)
      (k 1-9) not in simplest form; one pa/(qa*m), or pa*m/qa when proper (m 2-4); near ce/de (e 2-6) for a
      neighbour c/d of the base (|pd - qc| = 1, d <= 12); every number <= 60; neither fraction in simplest form.
    Each parameter's whole range reached; the YES share 45-55%; each wrong kind 30-37% of the wrong pairs.
  Levels: the page's gameLevel is the level asked for; the personal best is kept under fs_best_<level> and the old
    shared fs_best is never read or written.
  Dealing: startGame() at Year 6, six times: each session's 15 pairs come from the bank, none twice.
  Marking, in Chromium (390x844): every bank pair and 400 draws a level, each answered YES and answered NO through
    guess(): the right answer shows "Correct" and styles the button pressed; the wrong one shows exactly "Not quite:
    they are [not ]equivalent" (recomputed) and styles the key's button correct. Both fractions are drawn by KaTeX
    (\\dfrac{n}{d}), and the working is KaTeX reading "n1xd2=A vs n2xd1=B -> equal/not equal", recomputed.
Nothing leaves the stub server (bank_common.offline: KaTeX comes from the pinned copy, everything else is aborted).

A self-test plants faults in a copy of the page (scripts/plant_common.py: a plant that does not apply is a STALE PLANT
and fails the run) and each must FAIL: a wrong key in the bank, a wrong key in the generator, a wrong answer marked
right, a wrong figure in the working, the cross-multiplication rule with undefined letters, a GCSE draw in simplest
form, the old n1*m / (d1*m + 1..3) wrong pairs restored, and the best back to one shared key.

    python scripts/verify-fraction-equivalence.py [--no-selftest] [--against FILE]
"""
import argparse
import math
import os
import re
import sys
from collections import Counter
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'fraction-equivalence'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
YEAR6_DENOMS = {2, 3, 4, 5, 6, 8, 10, 12}
KINDS = ('yes', 'add', 'one', 'near')
NO_KINDS = ('add', 'one', 'near')
BANK_MIN = 40
DRAWS = 20000
MARKED_DRAWS = 400
DEALS = 6
SESSION = 15


def equivalent(p):
    return Fraction(p['n1'], p['d1']) == Fraction(p['n2'], p['d2'])


def working(p):
    a, b = p['n1'] * p['d2'], p['n2'] * p['d1']
    return '%d×%d=%dvs%d×%d=%d→%s' % (p['n1'], p['d2'], a, p['n2'], p['d1'], b,
                                       'equal' if a == b else 'notequal')


def simplest(n, d):
    return math.gcd(n, d) == 1


def proper(n, d):
    return 0 < n < d


def positive_ints(p):
    return all(isinstance(p.get(k), int) and not isinstance(p.get(k), bool) and p[k] > 0
               for k in ('n1', 'd1', 'n2', 'd2'))


def multiple(big, small):
    """big = small * m with m an integer >= 2: m, else None."""
    return big // small if big % small == 0 and big // small >= 2 else None


def kind_holds(p):
    """The bank's rule for its kind, in either order."""
    n1, d1, n2, d2, kind = p['n1'], p['d1'], p['n2'], p['d2'], p.get('kind')
    if kind == 'yes':
        return equivalent(p)
    if kind == 'add':
        return n2 - n1 == d2 - d1 != 0
    if kind == 'one':
        return ((n1 == n2 and (multiple(d2, d1) or multiple(d1, d2)) is not None)
                or (d1 == d2 and (multiple(n2, n1) or multiple(n1, n2)) is not None))
    if kind == 'near':
        return abs(n1 * d2 - n2 * d1) == 1
    return False


def check_key(fails, where, p):
    if p['equiv'] != equivalent(p):
        fails.append('%s: keyed %s, but %d/%d %s %d/%d' % (
            where, 'equivalent' if p['equiv'] else 'not equivalent', p['n1'], p['d1'],
            '=' if equivalent(p) else '≠', p['n2'], p['d2']))
    if (p.get('kind') == 'yes') != equivalent(p):
        fails.append('%s: kind %r, but %d/%d %s %d/%d' % (
            where, p.get('kind'), p['n1'], p['d1'], '=' if equivalent(p) else '≠', p['n2'], p['d2']))


def check_bank(fails, bank):
    seen = set()
    for i, p in enumerate(bank, 1):
        where = 'bank item %d (%s/%s vs %s/%s)' % (i, p.get('n1'), p.get('d1'), p.get('n2'), p.get('d2'))
        if not positive_ints(p):
            fails.append('%s: a number is not a positive integer' % where)
            continue
        check_key(fails, where, p)
        if p.get('kind') not in KINDS:
            fails.append('%s: kind %r is not yes, add, one or near' % (where, p.get('kind')))
        elif not kind_holds(p):
            fails.append('%s: its kind %r does not hold' % (where, p['kind']))
        if not {p['d1'], p['d2']} <= YEAR6_DENOMS:
            fails.append('%s: a denominator outside 2, 3, 4, 5, 6, 8, 10, 12' % where)
        if not (proper(p['n1'], p['d1']) and proper(p['n2'], p['d2'])):
            fails.append('%s: a fraction is not proper' % where)
        k = frozenset([(p['n1'], p['d1']), (p['n2'], p['d2'])])
        if len(k) == 1:
            fails.append('%s: the two fractions are written identically' % where)
        if k in seen:
            fails.append('%s: the pair is repeated' % where)
        seen.add(k)
    if len(bank) < BANK_MIN:
        fails.append('the bank holds %d pairs, below the %d minimum' % (len(bank), BANK_MIN))
    missing = [k for k in NO_KINDS if not any(p.get('kind') == k for p in bank)]
    if missing or not any(p.get('kind') == 'yes' for p in bank):
        fails.append('the bank is missing a kind: %s' % (missing or ['yes']))
    return Counter(p.get('kind') for p in bank)


def rule_ks3(p, reach):
    """None if the draw keeps KS3's rule for its kind, else why not."""
    n1, d1, n2, d2, kind = p['n1'], p['d1'], p['n2'], p['d2'], p['kind']
    if not (proper(n1, d1) and simplest(n1, d1) and 2 <= d1 <= 12):
        return 'the first fraction is not proper and in simplest form with a bottom 2 to 12'
    if kind == 'yes':
        m = multiple(d2, d1)
        if m is None or n2 != n1 * m or not 2 <= m <= 6:
            return 'yes is not pm/qm with m 2 to 6'
        reach['yes m'].add(m)
    elif kind == 'add':
        k = n2 - n1
        if not (k == d2 - d1 and 1 <= k <= 5):
            return 'add is not (p+k)/(q+k) with k 1 to 5'
        reach['add k'].add(k)
    elif kind == 'one':
        mb, mt = multiple(d2, d1), multiple(n2, n1)
        if n2 == n1 and mb is not None and 2 <= mb <= 6:
            reach['one m'].add(mb)
            reach['one form'].add('bottom')
        elif d2 == d1 and mt is not None and 2 <= mt <= 6 and n2 < d1:
            reach['one m'].add(mt)
            reach['one form'].add('top')
        else:
            return 'one is neither p/(qm) nor pm/q with pm < q (m 2 to 6)'
    elif kind == 'near':
        if not (proper(n2, d2) and abs(n1 * d2 - n2 * d1) == 1 and 2 <= d2 <= max(12, 2 * d1)):
            return 'near is not a proper c/d with |pd - qc| = 1 and d 2 to max(12, 2q)'
        reach['near d'].add(d2)
    return None


def rule_gcse(p, reach):
    n1, d1, n2, d2, kind = p['n1'], p['d1'], p['n2'], p['d2'], p['kind']
    if max(n1, d1, n2, d2) > 60:
        return 'a number is over 60'
    if simplest(n1, d1) or simplest(n2, d2):
        return 'a fraction is in simplest form'
    a = math.gcd(n1, d1)
    pp, q = n1 // a, d1 // a
    if not (2 <= a <= 6 and proper(pp, q) and 2 <= q <= 12):
        return 'the first fraction is not pa/qa (a 2 to 6) of a proper base with a bottom 2 to 12'
    reach['first a'].add(a)
    if kind == 'yes':
        b = math.gcd(n2, d2)
        if not (n2 == pp * b and d2 == q * b and 2 <= b <= 9 and b != a):
            return 'yes is not pb/qb with b 2 to 9, b != a'
        reach['yes b'].add(b)
    elif kind == 'add':
        k = n2 - n1
        if not (k == d2 - d1 and 1 <= k <= 9):
            return 'add is not (pa+k)/(qa+k) with k 1 to 9'
        reach['add k'].add(k)
    elif kind == 'one':
        mb, mt = multiple(d2, d1), multiple(n2, n1)
        if n2 == n1 and mb is not None and 2 <= mb <= 4:
            reach['one m'].add(mb)
            reach['one form'].add('bottom')
        elif d2 == d1 and mt is not None and 2 <= mt <= 4 and n2 < d2:
            reach['one m'].add(mt)
            reach['one form'].add('top')
        else:
            return 'one is neither pa/(qa*m) nor pa*m/qa when proper (m 2 to 4)'
    elif kind == 'near':
        e = math.gcd(n2, d2)
        c, d = n2 // e, d2 // e
        if not (2 <= e <= 6 and proper(c, d) and d <= 12 and abs(pp * d - q * c) == 1):
            return 'near is not ce/de (e 2 to 6) of a neighbour c/d of the base with d <= 12'
        reach['near e'].add(e)
    return None


def ks3_near_bottoms():
    """Every bottom a KS3 near pair can have: d 2 to max(12, 2q) with a proper c/d next to some base p/q
    (22 and 24 cannot: 11 or 12 would have to divide 1)."""
    out = set()
    for q in range(2, 13):
        for pp in range(1, q):
            if simplest(pp, q):
                out |= {d for d in range(2, max(12, 2 * q) + 1) for c in range(1, d) if abs(pp * d - q * c) == 1}
    return out


# Each parameter's whole range must be reached in 20000 draws.
REACH = {
    'ks3': {'yes m': set(range(2, 7)), 'add k': set(range(1, 6)), 'one m': set(range(2, 7)),
            'one form': {'top', 'bottom'}, 'near d': ks3_near_bottoms()},
    'gcse': {'first a': set(range(2, 7)), 'yes b': set(range(2, 10)), 'add k': set(range(1, 10)),
             'one m': set(range(2, 5)), 'one form': {'top', 'bottom'}, 'near e': set(range(2, 7))},
}


def check_draws(fails, draws, level):
    rule = rule_ks3 if level == 'ks3' else rule_gcse
    reach = {k: set() for k in REACH[level]}
    kinds = Counter()
    bad = 0
    for i, p in enumerate(draws):
        where = '%s draw %d (%s/%s vs %s/%s, %s)' % (level, i, p.get('n1'), p.get('d1'), p.get('n2'), p.get('d2'),
                                                     p.get('kind'))
        if not positive_ints(p) or p.get('kind') not in KINDS:
            fails.append('%s: a number is not a positive integer, or the kind is not yes, add, one or near' % where)
            bad += 1
        else:
            kinds[p['kind']] += 1
            n = len(fails)
            check_key(fails, where, p)
            if not proper(p['n2'], p['d2']):
                fails.append('%s: the second fraction is not proper' % where)
            why = rule(p, reach)
            if why:
                fails.append('%s: %s' % (where, why))
            bad += len(fails) > n
        if bad > 20:
            break
    for k, want in REACH[level].items():
        if reach[k] != want:
            fails.append('%s generator: %s reached %s, not %s' % (level, k, sorted(reach[k]), sorted(want)))
    total = sum(kinds.values())
    nos = total - kinds['yes']
    if total and not 0.45 <= kinds['yes'] / total <= 0.55:
        fails.append('%s generator: YES share %.1f%%, not 45-55%%' % (level, 100.0 * kinds['yes'] / total))
    for k in NO_KINDS:
        if nos and not 0.30 <= kinds[k] / nos <= 0.37:
            fails.append('%s generator: %s is %.1f%% of the wrong pairs, not 30-37%%' % (level, k, 100.0 * kinds[k] / nos))
    return kinds


GEN_JS = "(n) => { const out = []; for (let i = 0; i < n; i++) out.push(generateQ()); return out; }"
# What the student sees in an element: its text without KaTeX's MathML copy, whitespace removed.
SEEN_JS = r"""(el) => { const c = el.cloneNode(true); c.querySelectorAll('.katex-mathml').forEach(m => m.remove());
  return c.textContent.replace(/\s+/g, ''); }"""
MARK_JS = r"""(args) => {
  const [p, val] = args;
  const seen = %s;
  const tex = (el) => Array.from(el.querySelectorAll('annotation')).map(a => a.textContent);
  generateQ = () => p;
  score = 0; streak = 0; qNum = 0;
  nextQ();
  guess(val);
  MaffsLock.clearTimers();
  const fb = document.getElementById('feedback'), hint = document.getElementById('hint');
  const f1 = document.getElementById('frac1'), f2 = document.getElementById('frac2');
  return {fb: fb.textContent, cls: fb.className, hint: seen(hint), hintKatex: hint.querySelectorAll('.katex').length,
          f1: tex(f1), f2: tex(f2),
          yes: document.getElementById('btnYes').className, no: document.getElementById('btnNo').className};
}""" % SEEN_JS
DEAL_JS = r"""() => { const out = [];
  for (let k = 0; k < %d; k++) { startGame(); const d = [cur];
    for (let i = 1; i < %d; i++) d.push(generateQ());
    out.push(d); MaffsLock.clearTimers(); }
  return out; }""" % (DEALS, SESSION)
BEST_JS = r"""() => {
  localStorage.clear();
  localStorage.setItem('fs_best', '999');
  const before = getBest();
  saveBest(37);
  const keys = {};
  for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); keys[k] = localStorage.getItem(k); }
  const after = getBest();
  localStorage.clear();
  return {level: gameLevel, before, after, keys};
}"""


def mark_all(fails, page, items, tag):
    for p in items:
        key = equivalent(p)
        for val in (True, False):
            got = page.evaluate(MARK_JS, [p, val])
            where = '%s %d/%d vs %d/%d, %s' % (tag, p['n1'], p['d1'], p['n2'], p['d2'], 'YES' if val else 'NO')
            btn = got['yes'] if val else got['no']
            keybtn = got['yes'] if key else got['no']
            if val == key:
                if not (got['fb'].startswith('Correct') and 'correct' in got['cls'] and 'correct' in btn):
                    fails.append('%s: the right answer was not marked right (%r)' % (where, got))
            else:
                want = 'Not quite: they are %sequivalent' % ('' if key else 'not ')
                if not (got['fb'] == want and 'wrong' in got['cls'] and 'correct' in keybtn):
                    fails.append('%s: the wrong answer was not marked wrong as %r (%r)' % (where, want, got))
            if got['hint'] != working(p) or got['hintKatex'] != 2:
                fails.append('%s: working %r in %d KaTeX pieces, recomputed %r in 2' % (
                    where, got['hint'], got['hintKatex'], working(p)))
            for f, n, d in (('f1', p['n1'], p['d1']), ('f2', p['n2'], p['d2'])):
                if got[f] != ['\\dfrac{%d}{%d}' % (n, d)]:
                    fails.append('%s: a fraction is not drawn by KaTeX as \\dfrac{%d}{%d}: %r' % (where, n, d, got[f]))
            if len(fails) > 30:
                return


def check_best(fails, page, level):
    got = page.evaluate(BEST_JS)
    want = 'fs_best_' + level
    if got['level'] != level:
        fails.append('level: asked for %s, the page plays %r' % (level, got['level']))
    if got['before'] != 0 or got['after'] != 37 or got['keys'] != {'fs_best': '999', want: '37'}:
        fails.append('best: at %s it must be kept under %s only and the old fs_best never read (%r)' % (level, want, got))


def open_page(pw, base, html, level):
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={'width': 390, 'height': 844})
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify&level=%s' % (SLUG, level), wait_until='load', timeout=20000)
    page.wait_for_function('typeof YEAR6_BANK !== "undefined" && typeof guess === "function" '
                           '&& typeof katex !== "undefined"', timeout=15000)
    return browser, page, errors


def play(fails, html):
    from playwright.sync_api import sync_playwright
    # R2 (SWEEP-1 fraction-equivalence-s1-001): the cross-multiplication rule says which fractions a, b, c and d belong to
    if "Cross multiply to check: for a/b and c/d, they're equivalent if a×d = b×c" not in html:
        fails.append("how-to: the cross-multiplication rule must name its fractions: 'for a/b and c/d, they're equivalent if a×d = b×c'")
    proc, base = bc.start_stub_server()
    stats = {}
    try:
        with sync_playwright() as pw:
            browser, page, errors = open_page(pw, base, html, 'year6')
            check_best(fails, page, 'year6')
            bank = page.evaluate('() => JSON.parse(JSON.stringify(YEAR6_BANK))')
            stats['bank'] = check_bank(fails, bank)
            inbank = {(p['n1'], p['d1'], p['n2'], p['d2']) for p in bank}
            for d in page.evaluate(DEAL_JS):
                keys = [(p['n1'], p['d1'], p['n2'], p['d2']) for p in d]
                if len(set(keys)) != len(keys) or not set(keys) <= inbank or len(keys) != SESSION:
                    fails.append('a Year 6 session is not %d different pairs from the bank' % SESSION)
            mark_all(fails, page, bank, 'Year 6')   # last: marking replaces generateQ in the page
            if errors:
                fails.append('year6 page errors: %s' % '; '.join(errors[:3]))
            browser.close()
            for level in ('ks3', 'gcse'):
                browser, page, errors = open_page(pw, base, html, level)
                check_best(fails, page, level)
                draws = page.evaluate(GEN_JS, DRAWS)
                stats[level] = check_draws(fails, draws, level)
                mark_all(fails, page, draws[:MARKED_DRAWS], level)
                if errors:
                    fails.append('%s page errors: %s' % (level, '; '.join(errors[:3])))
                browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return stats


OLD_NO_RULE = ("const q = (kind === 'yes') ? (gameLevel === 'gcse' ? genGCSE(kind) : genKS3(kind)) : (() => {"
               " const [p,b] = baseFraction(), m = randInt(2,6); return {n1:p, d1:b, n2:p*m, d2:b*m+randInt(1,3)}; })();")
# (name, tag a catch must contain, [(old, new, allow_multiple)])
PLANTS = [
    ('a wrong key in the bank (1/2 = 2/4 flagged no)', 'keyed',
     [("{ n1:1, d1:2, n2:2, d2:4, equiv:true, kind:'yes' }", "{ n1:1, d1:2, n2:2, d2:4, equiv:false, kind:'yes' }", False)]),
    ('a wrong key in the generator (add keyed yes)', 'keyed',
     [("q.equiv = q.n1*q.d2 === q.n2*q.d1;", "q.equiv = kind === 'yes' || kind === 'add';", False)]),
    ('a wrong answer marked right (any answer)', 'was not marked wrong',
     [('const correct=val===cur.equiv;', 'const correct=true;', False)]),
    ('a wrong figure in the working (n1 x d1)', 'working',
     [('const cross=cur.n1*cur.d2;', 'const cross=cur.n1*cur.d1;', False)]),
    ('the cross-multiplication rule with undefined letters', 'how-to',
     [("for a/b and c/d, they're equivalent if a×d = b×c", "if a×d = b×c, they're equivalent", False)]),
    ('a GCSE draw in simplest form (a = 1 allowed)', 'simplest form',
     [('const a = randInt(2,6), n1 = p*a', 'const a = randInt(1,6), n1 = p*a', False)]),
    ('the old n1*m / (d1*m + 1..3) wrong pairs restored', 'draw',
     [("const q = gameLevel === 'gcse' ? genGCSE(kind) : genKS3(kind);", OLD_NO_RULE, False)]),
    ('the best back to one shared key', 'best',
     [("'fs_best_'+gameLevel", "'fs_best'", True)]),
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
    fmt = lambda c: ', '.join('%s %d' % (k, c.get(k, 0)) for k in KINDS) if c else 'not read'
    print('%s: Year 6 bank %d pairs (%s); KS3 %d draws (%s); GCSE %d draws (%s); every key and working recomputed; '
          'the bank and %d draws a level marked both ways in Chromium' % (
              SLUG, sum(st.get('bank', {}).values()), fmt(st.get('bank')), DRAWS, fmt(st.get('ks3')), DRAWS,
              fmt(st.get('gcse')), MARKED_DRAWS))
    ok = True
    if not args.no_selftest and not args.against:
        for what, tag, edits in PLANTS:
            try:
                planted = html
                for old, new, many in edits:
                    planted = pc.apply_plant(planted, old, new, name=what, allow_multiple=many)
            except pc.StalePlant as e:
                print('  self-test %-52s *** %s ***' % (what, e))
                ok = False
                continue
            rep = []
            try:
                play(rep, planted)
                err = None
            except Exception as e:  # an error is never a catch
                err = e
            hit = [f for f in rep if tag in f]
            caught = pc.is_caught(hit, err)
            ok = ok and caught
            print('  self-test %-52s %s' % (what, ('caught: ' + hit[0][:110]) if caught else
                                            '*** MISSED ***' + (' (error: %s)' % err if err else '')))
    for f in fails[:40]:
        print('FAIL  ' + f)
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if fails or not ok else 'PASS')
    return 1 if fails or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
