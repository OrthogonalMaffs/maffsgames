#!/usr/bin/env python3
# ci-line: E2 | Seven Bridges (every puzzle's answer recomputed from its edges, no edge drawn through a vertex it does not join, the solution animation stops at Next; Chromium) |
"""Seven Bridges: every puzzle's answer follows from its edges, its drawing shows those edges, and nothing
from one puzzle reaches the next.

The game deals 10 graphs a session from three banks (ks3, gcse, alevel). The student traces an Eulerian path
or declares the graph impossible; a wrong "Impossible" shows the solution, animated, under the Next control.
The tranche 4 audit of 6 Oct 2026 found (contract LISTED-HIGH, 9 Oct 2026):
  seven-bridges-t4-001  the solution animation was never cancelled and traced onto the next puzzle, which then
                        opened part-drawn and unsolvable. Fixed on main by F1 batch 9 (its timers are MaffsLock
                        timers, and the Next control's advance cancels them); this verifier keeps it fixed.
  seven-bridges-t4-002  al_15's E sat at the midpoint of AC and BD, so edges A-C and B-D were drawn through E:
                        the screen showed four odd vertices where the data has none.

Checks:
  every puzzle: degrees from its edges give its oddVertices, hasEulerianPath (connected, 0 or 2 odd) and
  hasEulerianCircuit; its sampleSolution uses every edge exactly once (an Euler circuit when it says so);
  every edge, drawn as the page draws it (a line, or a curve for parallel edges), passes no vertex it does not
  join by less than CLEAR px (a vertex is drawn with radius 22);
  in Chromium (390x844, the real timers), on one level (the animation is one function for all three): a wrong
  "Impossible" on a possible puzzle, Next pressed while its solution is still being drawn, and the next puzzle
  must open with nothing traced, and stay so.
A self-test plants al_15's old E and a raw setTimeout in the animation (main before F1 batch 9); each must FAIL.

    python scripts/verify-seven-bridges.py [--no-selftest] [--against FILE]
"""
import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'seven-bridges'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
BANKS = {'ks3': 'KS3_PUZZLES', 'gcse': 'GCSE_PUZZLES', 'alevel': 'ALEVEL_PUZZLES'}
CLEAR = 24          # px between an edge and a vertex it does not join: a vertex is drawn with radius 22 (24 current)
# Edges that graze a vertex's disc (20-21 px) in puzzles t4-002 does not name. Reported to Jon with contract
# LISTED-HIGH (9 Oct 2026); its DO NOT TOUCH keeps them as they are until he rules. (puzzle, edge, vertex).
KNOWN_GRAZES = {('al_10', 'A-C', 'B'), ('al_10', 'B-D', 'C'), ('al_18', 'E-G', 'F'), ('al_21', 'K-O', 'B'), ('al_21', 'B-W', 'O')}


def banks(html):
    out = {}
    for lv, name in BANKS.items():
        m = re.search(r'const %s = (\[.*?\]);\n' % name, html)
        out[lv] = json.loads(m.group(1)) if m else None
    return out


def drawn(p):
    """Each edge as the page draws it (renderGraph): [(edge, [points])]."""
    V = {v['id']: (v['x'], v['y']) for v in p['vertices']}
    count, index = Counter(), []
    for e in p['edges']:
        k = '-'.join(sorted(e))
        index.append(count[k])
        count[k] += 1
    out = []
    for i, e in enumerate(p['edges']):
        (x1, y1), (x2, y2) = V[e[0]], V[e[1]]
        total = count['-'.join(sorted(e))]
        if total > 1:
            dx, dy = x2 - x1, y2 - y1
            dist = math.hypot(dx, dy)
            c = (index[i] - (total - 1) / 2) * min(60, dist * 0.4)
            cx, cy = (x1 + x2) / 2 - dy / dist * c, (y1 + y2) / 2 + dx / dist * c
            pts = [((1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2,
                    (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2) for t in (k / 200 for k in range(201))]
        else:
            pts = [(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t) for t in (k / 200 for k in range(201))]
        out.append((e, pts))
    return out


def connected(p):
    used = {v for e in p['edges'] for v in e}
    if not used:
        return True
    seen, todo = set(), [next(iter(used))]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo += [b if a == v else a for a, b in p['edges'] if v in (a, b)]
    return seen == used


def check_bank(fails, bk):
    for lv in BANKS:
        if not bk.get(lv):
            fails.append('%s: bank not found' % lv)
            continue
        for p in bk[lv]:
            w = '%s %s' % (lv, p['id'])
            V = {v['id']: (v['x'], v['y']) for v in p['vertices']}
            deg = Counter(v for e in p['edges'] for v in e)
            odd = sorted(v for v in V if deg[v] % 2)
            path = connected(p) and len(odd) in (0, 2)
            if sorted(p['oddVertices']) != odd:
                fails.append('%s: oddVertices %s, the edges give %s' % (w, p['oddVertices'], odd))
            if p['hasEulerianPath'] != path or p['hasEulerianCircuit'] != (path and not odd):
                fails.append('%s: hasEulerianPath %s / Circuit %s, the edges give %s / %s'
                             % (w, p['hasEulerianPath'], p['hasEulerianCircuit'], path, path and not odd))
            sol = p.get('sampleSolution')
            if path:
                left = Counter(tuple(sorted(e)) for e in p['edges'])
                ok = bool(sol) and len(sol) == len(p['edges']) + 1
                for a, b in zip(sol or [], (sol or [])[1:]):
                    k = tuple(sorted((a, b)))
                    ok = ok and left[k] > 0
                    left[k] -= 1
                if not ok or (p['hasEulerianCircuit'] and sol[0] != sol[-1]):
                    fails.append('%s: sampleSolution %s does not use every edge exactly once' % (w, sol))
            for e, pts in drawn(p):
                for vid, (x, y) in V.items():
                    if vid in e:
                        continue
                    d = min(math.hypot(x - px, y - py) for px, py in pts)
                    if d < CLEAR and (p['id'], '%s-%s' % tuple(e), vid) not in KNOWN_GRAZES:
                        fails.append('%s: edge %s-%s is drawn %.0f px from %s, a vertex it does not join (t4-002)'
                                     % (w, e[0], e[1], d, vid))


STALE_JS = """(lv) => { S.level = lv; startGame();
  const bank = PUZZLE_BANKS[lv];
  const poss = bank.find(q => q.hasEulerianPath && q.sampleSolution && q.sampleSolution.length > 6);
  S.session[0] = poss; S.session[1] = bank.find(q => q !== poss); S.puzzleIdx = 0; loadPuzzle();
  return [poss.id, S.session[1].id]; }"""


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)       # Next at once; the animation keeps its real timing
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof PUZZLE_BANKS !== "undefined"', timeout=15000)
            for lv in ('ks3',):
                first, second = page.evaluate(STALE_JS, lv)
                time.sleep(0.4)                              # MaffsLock's fresh window on a new puzzle
                page.evaluate('() => declareImpossible()')
                time.sleep(1.8)                              # the animation starts after 1 s, a step every 300 ms
                mid = page.evaluate('() => S.path.length')
                # Count every redraw of the graph from here: a stale animation step redraws it with no input.
                page.evaluate('() => { const f = renderGraph; window.__draws = 0;'
                              ' renderGraph = function () { window.__draws++; return f.apply(this, arguments); }; }')
                page.locator('#nextMount button').first.click()
                time.sleep(0.2)
                opened = page.evaluate('() => window.__draws')
                time.sleep(2.5)                              # long enough for several more animation steps
                now, traced, edges, draws = page.evaluate(
                    '() => [S.puzzle.id, S.path.length, S.traversedEdges.length, window.__draws]')
                if mid == 0:
                    fails.append('%s (t4-001): %s\'s solution was not being drawn when Next was pressed' % (lv, first))
                if now != second or traced or edges or draws != opened:
                    fails.append('%s (t4-001): after Next on %s, %s opened with %d vertices and %d edges traced, and '
                                 'was redrawn %d times with no input' % (lv, first, now, traced, edges, draws - opened))
            browser.close()
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
    finally:
        proc.terminate()
        proc.wait()


# (the text the failure must start with, what is planted, today's text, main's text before the fix).
PLANTS = [
    ('alevel al_15', "t4-002: al_15's E at the midpoint of AC and BD",
     '{"id":"E","x":300,"y":150}],"edges":[["A","B"],["B","C"],["C","D"],["D","A"],["A","E"]',
     '{"id":"E","x":300,"y":200}],"edges":[["A","B"],["B","C"],["C","D"],["D","A"],["A","E"]'),
    ('ks3 (t4-001)', 't4-001: the animation on a raw setTimeout (before F1 batch 9)',
     '      MaffsLock.timer(nextStep, delay);\n    }\n  }\n\n  nextStep();',
     '      setTimeout(nextStep, delay);\n    }\n  }\n\n  nextStep();'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    bk = banks(html)
    check_bank(fails, bk)
    play(fails, html)
    print('%s: %d puzzles, every answer recomputed and every edge measured; Next during a solution, in Chromium'
          % (SLUG, sum(len(v or []) for v in bk.values())))
    ok = True
    if not args.no_selftest and not args.against:
        for tag, what, new, old in PLANTS:
            if html.count(new) != 1:
                print('  self-test %-46s *** CANNOT PLANT (%d) ***' % (what, html.count(new)))
                ok = False
                continue
            planted = html.replace(new, old)
            rep = []
            check_bank(rep, banks(planted))
            if not any(f.startswith(tag) for f in rep):
                play(rep, planted)
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
