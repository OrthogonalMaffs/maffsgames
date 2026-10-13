#!/usr/bin/env python3
# ci-line: B2 | Higher Power Pairs (two cards match exactly when they are worth the same; played in Chromium) |
"""Higher Power, Pairs mode: two cards match exactly when they are worth the same.

Pairs deals 10 cards from the level's pool as 20 face-down cards: each card's expression and its value. The
tranche 2 audit of 6 Oct 2026 found the match decided by the deal's pairId, not by value: 2^8 turned over with
the 256 belonging to 4^4 was rejected, though the two 256 cards look identical (also the two golden-ratio
cards, the two zeros and the two pi^2/6 cards; higher-power-t2-001, HIGH; contract LISTED-HIGH, 9 Oct 2026:
match by value, so 2^8 with any card worth 256 is a match).

What each card is worth, independently of the game's rule: its stored value when finite; the two cards stored as
Infinity are told apart by what they are (WORTH): a googolplex is finite, the harmonic series diverges.
Checks, every level, in Chromium (390x844), each pair turned over through pairsFlip() and the match read from
the cards' state: every card's expression with its own value card matches; every card with every other card
worth the same (its value card and its expression card) matches; every card with the card nearest to it in
value but worth something else does not, nor a googolplex with infinity. Cards that look the same must be
worth the same. A perfect number's fact lists exactly its proper divisors (SWEEP-1, 13 Oct 2026). A self-test
plants main's pairId rule back, and ks3_35's old fact; each must FAIL.

    python scripts/verify-higher-power.py [--no-selftest] [--against FILE] [--katex-dir DIR]
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'higher-power'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LEVELS = ('ks3', 'gcse', 'alevel')
# Cards stored as Infinity, by id: what each is really worth (a finite number too big to store, or infinity).
WORTH = {'al_32': ('googolplex', 10.0 ** 300), 'al_38': ('infinity', math.inf)}


def worth(card):
    if card['id'] in WORTH:
        return WORTH[card['id']]
    if card['value'] is None or not math.isfinite(card['value']):
        raise ValueError('%s is stored as %r: say in WORTH what it is worth' % (card['id'], card['value']))
    return ('number', card['value'])


def same_worth(a, b):
    wa, wb = worth(a), worth(b)
    if wa[0] != 'number' or wb[0] != 'number':
        return wa[0] == wb[0]
    return math.isclose(wa[1], wb[1], rel_tol=1e-9, abs_tol=1e-12)


def cases(pool):
    """[(i, type_i, j, type_j, should match, why)] for one level's pool."""
    out = []
    for i, a in enumerate(pool):
        out.append((i, 'expr', i, 'val', True, 'its own value card'))
        others = [j for j in range(len(pool)) if j != i]
        for j in others:
            if same_worth(a, pool[j]):
                out.append((i, 'expr', j, 'val', True, 'worth the same'))
                out.append((i, 'expr', j, 'expr', True, 'worth the same'))
        diff = [j for j in others if not same_worth(a, pool[j])]
        if diff and worth(a)[0] == 'number':
            near = min(diff, key=lambda j: abs(worth(pool[j])[1] - worth(a)[1]))
            out.append((i, 'expr', near, 'val', False, 'the nearest card worth something else'))
    ids = {c['id']: k for k, c in enumerate(pool)}
    if 'al_32' in ids and 'al_38' in ids:
        out.append((ids['al_32'], 'expr', ids['al_38'], 'val', False, 'a googolplex is not infinity'))
    return out


def check_perfect(fails, pools):
    """SWEEP-1 (13 Oct 2026, higher-power-s1-001): a perfect number's fact lists exactly its proper divisors, which
    sum to it, and never says its factors (which include itself) add up to it."""
    for lv in LEVELS:
        for c in pools[lv]:
            if 'perfect number' not in c['display']:
                continue
            n, fact = int(c['value']), c.get('fact', '')
            proper = [d for d in range(1, n) if n % d == 0]
            m = re.match(r'(\d+) = ([\d+ ]+)\.', fact)
            terms = [int(t) for t in m.group(2).replace(' ', '').split('+')] if m else None
            if not m or int(m.group(1)) != n or terms != proper or sum(proper) != n:
                fails.append('%s %s: the fact %r does not list %d\'s proper divisors, summing to it' % (lv, c['id'], fact, n))
            if re.search(r'factors add up', fact) and 'other than itself' not in fact:
                fails.append('%s %s: "%s": its factors include %d itself; only those other than itself add up to it'
                             % (lv, c['id'], fact, n))


def true_values():
    """The exact value (30 digits) of every card whose valueDisplay is a decimal expansion, by id."""
    from mpmath import mp, mpf, pi, e, sqrt, log, euler, catalan, zeta, sin, cos, quad, cbrt, phi
    mp.dps = 30
    return {'ks3_16': pi, 'ks3_17': sqrt(2), 'ks3_18': sqrt(3), 'ks3_19': sqrt(5), 'ks3_20': sqrt(10), 'ks3_40': pi ** 2,
            'gcse_10': sqrt(200), 'gcse_11': e, 'gcse_12': phi, 'gcse_13': (1 + sqrt(5)) / 2, 'gcse_14': log(2), 'gcse_15': log(10),
            'gcse_16': mpf('1.05') ** 10, 'gcse_17': mpf('1.1') ** 10, 'gcse_18': mpf('0.95') ** 20, 'gcse_19': mpf('1.02') ** 35,
            'gcse_20': pi ** 2, 'gcse_21': e ** 2, 'gcse_22': 3 * pi, 'gcse_23': phi ** 2, 'gcse_24': e + 1, 'gcse_25': sqrt(2) + sqrt(3),
            'gcse_26': sqrt(7), 'gcse_27': 3 * sqrt(2), 'gcse_28': sqrt(50), 'gcse_36': (mpf(3) / 2) ** 12,
            'al_01': e ** pi, 'al_02': pi ** e, 'al_03': e ** e, 'al_04': pi ** pi, 'al_05': log(pi), 'al_11': mp.log10(2),
            'al_12': log(10, 2), 'al_13': mp.log10(7), 'al_14': euler, 'al_15': catalan, 'al_16': zeta(3), 'al_17': pi ** 3,
            'al_18': e ** 3, 'al_19': cbrt(12), 'al_20': sqrt(e), 'al_22': sin(1), 'al_23': cos(1), 'al_34': quad(lambda x: x ** x, [0, 1]),
            'al_36': 1 - 1 / e, 'al_37': 1 / e, 'razor_04': sqrt(3) / 2, 'razor_05': mpf(23) / 6}


CARD_RE = re.compile(r'\{id:"(\w+)",display:"((?:[^"\\]|\\.)*)",displayType:"\w+",valueDisplay:"((?:[^"\\]|\\.)*)"(?:.*?fact:"((?:[^"\\]|\\.)*)")?')


def check_text(fails, html):
    """R1, R2, R3 (SWEEP-1 higher-power-s1-002 to -009): a decimal ending "..." is the truncated expansion; a rounded one
    is written with the approximately-equals sign; labels and facts say what is true."""
    from mpmath import mp, mpf, floor
    tv = true_values()
    cards = {m.group(1): m for m in CARD_RE.finditer(html)}
    for i, m in cards.items():
        shown = m.group(3)
        d = re.fullmatch(r'([\d.]+)\.\.\.', shown)
        r = re.fullmatch(r'\\\\approx ([\d.]+)', shown)
        if not (d or r) or i not in tv:
            if (d or r):
                fails.append('%s: %r is a decimal expansion with no true value in true_values()' % (i, shown))
            continue
        digits = (d or r).group(1)
        dp = len(digits.split('.')[1])
        trunc = floor(tv[i] * 10 ** dp) / mpf(10) ** dp
        rounded = floor(tv[i] * 10 ** dp + mpf(1) / 2) / mpf(10) ** dp
        want = mpf(digits)
        if d and abs(trunc - want) > mpf(10) ** (-dp - 3):
            fails.append('%s: %r ends "..." but the digits are rounded (true %s): write "\\approx" instead (R3)' % (i, shown, mp.nstr(tv[i], 12)))
        if r and abs(rounded - want) > mpf(10) ** (-dp - 3):
            fails.append('%s: %r is not the value rounded to %d places (true %s)' % (i, shown, dp, mp.nstr(tv[i], 12)))
    need = (('ks3_31', 'display', 'doubling'), ('gcse_34', 'display', 'known'), ('ks3_04', 'fact', 'mebibyte'),
            ('al_40', 'fact', 'fourth roots'), ('al_36', 'fact', 'large'))
    for i, field, word in need:
        m = cards.get(i)
        if not m or word not in m.group(2 if field == 'display' else 4):
            fails.append('%s: its %s must say %r (R1, R2, R3)' % (i, field, word))
    if cards.get('al_30') and 'Total chessboard grains.' in cards['al_30'].group(4):
        fails.append('al_30: 2^64 is not the board\'s total; the total is 2^64 \u2212 1 (R3)')
    if html.count('If the two are equal, either answer is right.') < 2:
        fails.append('start screen: it must say a tie accepts either answer (R2)')


def check_pools(fails, pools):
    check_perfect(fails, pools)
    for lv in LEVELS:
        pool = pools[lv]
        for a in pool:
            for b in pool:
                if a['id'] < b['id'] and a['valueDisplay'] == b['valueDisplay']:
                    try:
                        if not same_worth(a, b):
                            fails.append('%s: %s and %s show the same value card %r but are not worth the same'
                                         % (lv, a['id'], b['id'], a['valueDisplay']))
                    except ValueError as e:
                        fails.append('%s: %s' % (lv, e))


SWEEP_JS = r"""(all) => {
  window.setTimeout = () => 0;
  const out = [];
  for (const [lv, cs] of Object.entries(all)) {
    currentLevel = lv;
    const pool = getCardPool();
    for (const [i, ti, j, tj, want, why] of cs) {
      const a = pool[i], b = pool[j];
      // pairId is the card's place in the pool, as startPairs() deals it.
      pairsCards = [{pairId: i, type: ti, card: a, content: ti === 'expr' ? a.display : a.valueDisplay},
                    {pairId: j, type: tj, card: b, content: tj === 'expr' ? b.display : b.valueDisplay}];
      pairsState = pairsCards.map(() => ({flipped: false, matched: false}));
      pairsFirst = null; pairsAttempts = 0; pairsMatched = 0;
      renderPairsGrid();
      pairsFlip(0); pairsFlip(1);
      const got = pairsState[0].matched && pairsState[1].matched;
      if (got !== want) out.push([lv, a.id + ' (' + ti + ') with ' + b.id + ' (' + tj + ')',
                                  (got ? 'matched' : 'not matched') + ': ' + why]);
    }
  }
  return out;
}"""
KATEX_DIR = None


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            if KATEX_DIR:
                ctx.route(lambda url: '/katex@' in url and '/dist/' in url, lambda route: route.fulfill(
                    path=os.path.join(KATEX_DIR, route.request.url.split('/dist/', 1)[1].split('?')[0])))
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof ALL_BANKS !== "undefined"', timeout=15000)
            # Infinity does not survive JSON: read it as null, then WORTH names those cards.
            pools = page.evaluate('() => JSON.parse(JSON.stringify(ALL_BANKS))')
            try:
                all_cases = {lv: [list(c) for c in cases(pools[lv])] for lv in LEVELS}
            except ValueError as e:
                fails.append(str(e))
                browser.close()
                return pools
            page.evaluate("() => show('pairsGame')")
            for lv, what, why in page.evaluate(SWEEP_JS, all_cases):
                fails.append('%s Pairs in Chromium: %s %s' % (lv, what, why))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            return pools
    finally:
        proc.terminate()
        proc.wait()


PLANTS = [
    ('ks3_19', 's1-009: 2.23607 rounded but shown with "..."', '"\\\\approx 2.23607"', '"2.23607..."'),
    ('ks3_31', 's1-002: the chessboard rule unstated', '(1, then doubling)', '(first half)'),
    ('al_30', 's1-005: 2^64 called the board total', 'One less than this is the total number of grains on the whole chessboard.', 'Total chessboard grains.'),
    ('al_36', 's1-004: 1 - 1/e for every n', 'As n gets large, ', ''),
    ('start screen', 's1-008: a tie never mentioned', 'If the two are equal, either answer is right. Build your streak!\n', 'Build your streak!\n'),
    ('ks3 ks3_35', "s1-001: 6's factors 'add up to itself'",
     'Its factors other than itself add up to 6.', 'Its factors add up to itself.'),
    ('ks3 Pairs in Chromium: ks3_02', "t2-001: the deal's pairId decides the match",
     'if(first!==second&&sameValue(pairsCards[first].card,pairsCards[second].card)){',
     'if(pairsCards[first].pairId===pairsCards[second].pairId&&first!==second){'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    ap.add_argument('--katex-dir', help='serve KaTeX from this local dist/ folder')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    global KATEX_DIR
    KATEX_DIR = args.katex_dir
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    check_text(fails, html)
    pools = play(fails, html)
    if pools is not None:
        check_pools(fails, pools)
    n = sum(len(cases(pools[lv])) for lv in LEVELS) if pools and not fails else 0
    print('%s: Pairs, %d pairs of cards turned over in Chromium' % (SLUG, n))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            rep = []
            bad_html = html.replace(new, old)
            check_text(rep, bad_html)
            planted = play(rep, bad_html) if tag.startswith(('ks3 ', 'gcse ', 'alevel ')) else None
            if planted is not None:
                check_pools(rep, planted)
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
