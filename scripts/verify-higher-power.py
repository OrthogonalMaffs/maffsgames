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
worth the same. A self-test plants main's pairId rule back; it must FAIL.

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


def check_pools(fails, pools):
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
            planted = play(rep, html.replace(new, old))
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
