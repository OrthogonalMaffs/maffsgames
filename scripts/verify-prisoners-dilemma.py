#!/usr/bin/env python3
# ci-line: Prisoner's Dilemma (no answers to mark: the payoffs, every opponent's play against its stated strategy, every score, count and stated figure recomputed; games and a tournament played in Chromium) |
"""Prisoner's Dilemma: 20 rounds of cooperate or defect against a computer opponent; four levels, each with its own opponents.

The game marks nothing right or wrong (question_answered sends correct: null). What it states, and this verifier checks
independently of the game's code:
  Payoffs: the matrix shown (3,3 / 0,5 / 5,0 / 1,1; "£Nk" at Core) and getPayoffs() for all four pairs; the round reveal ("+N").
  Opponents: each opponent's move, for 3,000 random histories of every length 0 to 19, is the move its own stated strategy
    makes (written here from the stated rule: Always Cooperate, Always Defect, Tit-for-Tat, Grim Trigger / Grudge, Suspicious
    Tit-for-Tat, Pavlov "repeat after 3 or 5, switch after 0 or 1", Tara "retaliates only after two defections in a row", Prober
    "cooperates rounds 1-3, defects in round 4, then always defects if you did not retaliate in round 5, else Tit-for-Tat");
    Random plays only cooperate or defect, each in 40-60% of 4,000 calls.
  Games, in Chromium (390x844) on a controlled clock, through the real Cooperate and Defect buttons: every opponent at every level
    is played for 20 rounds with a fixed pattern of choices; each round the opponent's move is its strategy's (Random's is read
    back), and the running HUD, the end screen's two totals, the four breakdown counts, the title (won / lost / draw) and "If
    you'd both cooperated every round: 60 each" are recomputed here; KS3's round message names the round's own payoffs.
  Statements: GCSE's "E(X) = 0.5 x 3 + 0.5 x 0 = 1.5" and "= 0.5 x 5 + 0.5 x 1 = 3.0", the "3.0 vs 1.5"; A-Level's "5 > 3 if they
    cooperate; 1 > 0 if they defect" and the iteration count; the insight "1 point per round instead of a possible 3".
  Tournament: at each level all opponents in turn; each row's totals and Win/Loss/Draw, the overall total, and "Perfect mutual
    cooperation across all matches" (60 per opponent).
Not asserted (open findings, left open): the leaderboard ranking (prisoners-dilemma-t4-001, contract: waits on Jon), ?level keys
(t4-003), the TF2T name (t4-004), the Discount Store's hint (t4-005), Tara's name (t4-006), small text points (t4-007).

    python scripts/verify-prisoners-dilemma.py [--no-selftest] [--against FILE]
"""
import argparse
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SLUG = 'prisoners-dilemma'
GAME = os.path.join(os.path.dirname(HERE), 'games', SLUG, 'index.html')
LEVELS = ('ks3', 'gcse', 'alevel', 'core')
PAY = {('C', 'C'): (3, 3), ('C', 'D'): (0, 5), ('D', 'C'): (5, 0), ('D', 'D'): (1, 1)}
PATTERN = 'CCDCDDCCCDCDDDCCCCDC'          # the player's 20 choices in each game


def strat_for(stratname):
    s = stratname.lower()
    if 'suspicious' in s:
        return 'stft'
    if 'pavlov' in s:
        return 'pavlov'
    if 'two' in s and 'tat' in s:
        return 'tf2t'
    if 'prober' in s:
        return 'prober'
    if 'grim' in s or 'grudge' in s:
        return 'grim'
    if 'tit-for-tat' in s:
        return 'tft'
    if 'always cooperate' in s:
        return 'allc'
    if 'always defect' in s:
        return 'alld'
    if 'random' in s:
        return 'random'
    return None


def move(kind, h):
    """The opponent's move by its stated rule; h is [(player, opponent)] so far."""
    n = len(h)
    if kind == 'allc':
        return 'C'
    if kind == 'alld':
        return 'D'
    if kind == 'tft':
        return 'C' if n == 0 else h[-1][0]
    if kind == 'stft':
        return 'D' if n == 0 else h[-1][0]
    if kind == 'grim':
        return 'D' if any(p == 'D' for p, _ in h) else 'C'
    if kind == 'pavlov':
        if n == 0:
            return 'C'
        p, o = h[-1]
        mine = PAY[(p, o)][1]
        return o if mine in (3, 5) else ('D' if o == 'C' else 'C')
    if kind == 'tf2t':
        return 'D' if n >= 2 and h[-1][0] == 'D' and h[-2][0] == 'D' else 'C'
    if kind == 'prober':
        if n < 3:
            return 'C'
        if n == 3:
            return 'D'
        if n == 4:
            return 'C'
        return 'D' if h[4][0] == 'C' else h[-1][0]
    raise ValueError(kind)


STRAT_JS = r"""([lv, cases]) => {
  const out = {};
  for (const opp of OPPONENTS[lv]) {
    out[opp.id] = {stratName: opp.stratName, moves: cases.map(h => opp.play(h.map(([p, o]) => {
      const pay = getPayoffs(p === 'C' ? 'cooperate' : 'defect', o === 'C' ? 'cooperate' : 'defect');
      return {player: p === 'C' ? 'cooperate' : 'defect', opponent: o === 'C' ? 'cooperate' : 'defect', pPts: pay.p, oPts: pay.o};
    })))};
    if (opp.stratName.toLowerCase().includes('random')) {
      let c = 0; for (let k = 0; k < 4000; k++) { const m = opp.play([]); if (m === 'cooperate') c++; else if (m !== 'defect') c = -1e9; }
      out[opp.id].coopRate = c / 4000;
    }
  }
  return out;
}"""
PAY_JS = r"""() => { const o = {};
  for (const p of ['cooperate', 'defect']) for (const q of ['cooperate', 'defect']) { const r = getPayoffs(p, q); o[p[0] + q[0]] = [r.p, r.o]; }
  return o; }"""


# The game's own MaffsLock.timer callbacks are queued and run in order (CLAUDE.md: drain the game's timers rather than wait on
# them), so a 20-round game is one call. Every callback still runs; the buttons are the page's own.
DRAIN_INIT = """(() => { if (window.__drain) return; window.__q = []; const t = MaffsLock.timer;
  MaffsLock.timer = function (fn, ms) { window.__q.push(fn); return 0; };
  window.__drain = () => { let n = 0; while (window.__q.length && n++ < 1000) window.__q.shift()(); }; })()"""
GAME_JS = r"""(pattern) => { const out = [];
  for (const ch of pattern) {
    document.getElementById(ch === 'C' ? 'btnCoop' : 'btnDefect').click();
    const fn = window.__q.shift(); if (fn) fn();          // the reveal
    out.push({you: document.getElementById('revealYouPts').textContent, them: document.getElementById('revealOppPts').textContent,
              hy: document.getElementById('hudYou').textContent, ht: document.getElementById('hudThem').textContent,
              tip: document.getElementById('roundTooltip').textContent, opp: history[history.length - 1].opponent[0].toUpperCase()});
    window.__drain();                                      // the advance (and, after round 20, the end)
  }
  return out; }"""


def play_game(page, lv, opp_id, pattern, tournament=False):
    """Play 20 rounds through the real buttons; return what the page showed each round."""
    page.evaluate(DRAIN_INIT)
    return page.evaluate(GAME_JS, pattern)


def fmt(lv, n):
    return '£%dk' % n if lv == 'core' else str(n)


def check_game(fails, page, lv, opp, kind, rounds, pattern):
    where = '%s vs %s' % (lv, opp['id'])
    h, ys, ts = [], 0, 0
    for i, (ch, r) in enumerate(zip(pattern, rounds)):
        want_o = move(kind, h) if kind != 'random' else r['opp']
        if r['opp'] != want_o:
            fails.append('opponent: %s round %d: played %s, its stated rule plays %s after %r' % (where, i + 1, r['opp'], want_o, ''.join(p + o for p, o in h)))
            return
        py, pt = PAY[(ch, want_o)]
        ys += py
        ts += pt
        if r['you'] != '+' + fmt(lv, py) or r['them'] != '+' + fmt(lv, pt) or r['hy'] != fmt(lv, ys) or r['ht'] != fmt(lv, ts):
            fails.append('scores: %s round %d (%s v %s): shown +%r/+%r, totals %r/%r; expected +%s/+%s, %s/%s' % (
                where, i + 1, ch, want_o, r['you'], r['them'], r['hy'], r['ht'], fmt(lv, py), fmt(lv, pt), fmt(lv, ys), fmt(lv, ts)))
            return
        if lv == 'ks3':
            nums = [int(x) for x in re.findall(r'(\d+)', r['tip'])]
            want = sorted({py, pt}) if py != pt else [py]
            if sorted(set(nums)) != want:
                fails.append('statement: %s round %d: the round message %r names %r, the payoffs are %d and %d' % (where, i + 1, r['tip'], nums, py, pt))
                return
        h.append((ch, want_o))
    end = page.evaluate('''() => { const c = document.getElementById("resultsContent");
        return {title: (c.querySelector("h2") || {}).textContent, vals: [...c.querySelectorAll(".sb-val")].map(e => e.textContent),
                bd: [...c.querySelectorAll(".bd-val")].map(e => e.textContent), ideal: (c.querySelector(".ideal-note") || {}).textContent,
                text: c.textContent}; }''')
    mc = sum(1 for p, o in h if p == o == 'C')
    md = sum(1 for p, o in h if p == o == 'D')
    yb = sum(1 for p, o in h if p == 'D' and o == 'C')
    tb = sum(1 for p, o in h if p == 'C' and o == 'D')
    title = 'You Won!' if ys > ts else 'They Won!' if ys < ts else "It's a Draw!"
    if end['title'] != title or end['vals'] != [fmt(lv, ys), fmt(lv, ts)] or end['bd'] != [str(mc), str(md), str(yb), str(tb)]:
        fails.append('scores: %s end screen %r, expected %r, totals %r, counts %r' % (where, end, title, [ys, ts], [mc, md, yb, tb]))
    if end['ideal'] != "If you'd both cooperated every round: %s each" % fmt(lv, 20 * 3):
        fails.append('statement: %s: %r, 20 rounds of 3 is %d' % (where, end['ideal'], 60))
    t = end['text']
    if lv == 'gcse':
        for a, b, c, d, v in re.findall(r'E\(X\) = ([\d.]+) x (\d+) \+ ([\d.]+) x (\d+) = ([\d.]+)', t):
            if abs(float(a) * int(b) + float(c) * int(d) - float(v)) > 1e-9:
                fails.append('statement: %s: E(X) = %s x %s + %s x %s = %s is false' % (where, a, b, c, d, v))
        if 'E(X) = 0.5 x 3 + 0.5 x 0' not in t or 'E(X) = 0.5 x 5 + 0.5 x 1' not in t or '(3.0 vs 1.5)' not in t:
            fails.append('statement: %s: the expected values are not the payoffs against a 50/50 opponent: %r' % (where, t[-600:]))
    if lv == 'alevel':
        if '5 > 3 if they cooperate; 1 > 0 if they defect' not in t or '20 iterations' not in t:
            fails.append('statement: %s: the dominance figures or iteration count do not match the payoffs: %r' % (where, t[-700:]))
    if 'instead of a possible' in t and 'got 1 point per round instead of a possible 3' not in t:
        fails.append('statement: %s: the mutual-defection insight misstates the payoffs' % where)


S1 = (('matrix', "<h3 id=\"matrixTitle\">Payoff Matrix (you, them)</h3>", 'the matrix does not say which number in a cell is yours (R2)'),
      ('matrix', "'Profit Matrix (you, them)'", 'the Core matrix does not say which number in a cell is yours (R2)'),
      ('pavlov', 'after a good result (\u00a33k or \u00a35k) and changes it after a poor one (\u00a30k or \u00a31k)',
       'the Adaptive Firm\'s description does not match its rule (R3)'),
      ('adapts', 'an opponent may adapt', 'GCSE says the opponent adapts after any opponent (R3)'),
      ('random', 'is random, so there is no pattern to find', 'the halfway prompt asks for Random Rita\'s pattern (R3)'),
      ('prober', 'Prober (a simplified version of Axelrod', 'Prober Pat\'s rule is not Axelrod\'s Prober (R1)'),
      ('tournament', 'Tournament Mode unlocks once you have beaten 3 different opponents', 'the tournament unlock is never said (R2)'))


def check_text(fails, html):
    """SWEEP-1 prisoners-dilemma-s1-001 to -006."""
    for tag, need, why in S1:
        if need not in html:
            fails.append('%s: %s' % (tag, why))
    if 'sticks with a pricing strategy while it' in html:
        fails.append('pavlov: the Adaptive Firm still "changes when it\'s not" profitable, but changes after \u00a31k, a profit (R3)')


def play(fails, html):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    stats = {'games': 0, 'cases': 0}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
            ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
            page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
            ctx.route(lambda url: not url.startswith(base), lambda route: route.abort())
            ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
                status=200, content_type='text/html; charset=utf-8', body=html))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.clock.install()
            page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof OPPONENTS !== "undefined" && typeof makeChoice === "function"', timeout=15000)
            pay = page.evaluate(PAY_JS)
            want = {'cc': [3, 3], 'cd': [0, 5], 'dc': [5, 0], 'dd': [1, 1]}
            if pay != want:
                fails.append('payoffs: getPayoffs gives %r, the matrix is %r' % (pay, want))
            rng = random.Random(42)
            cases = [[(rng.choice('CD'), rng.choice('CD')) for _ in range(rng.randint(0, 19))] for _ in range(3000)]
            for n in range(20):
                cases.append([('D', 'C')] * n)
                cases.append([('C', 'C')] * n)
            stats['cases'] = len(cases)
            kinds = {}
            for lv in LEVELS:
                res = page.evaluate(STRAT_JS, [lv, [[list(x) for x in h] for h in cases]])
                for oid, r in res.items():
                    kind = strat_for(r['stratName'])
                    kinds[(lv, oid)] = kind
                    if kind is None:
                        fails.append('opponent: %s %s: no rule known here for the stated strategy %r' % (lv, oid, r['stratName']))
                        continue
                    if kind == 'random':
                        if not 0.4 <= r.get('coopRate', -1) <= 0.6:
                            fails.append('opponent: %s %s: Random cooperated in %r of 4,000 calls' % (lv, oid, r.get('coopRate')))
                        continue
                    for h, m in zip(cases, r['moves']):
                        if m[0].upper() != move(kind, h):
                            fails.append('opponent: %s %s (%s): after %r plays %s, the stated rule plays %s' % (lv, oid, r['stratName'], ''.join(p + o for p, o in h), m, move(kind, h)))
                            break
            for lv in LEVELS:
                opps = page.evaluate('(lv) => OPPONENTS[lv].map(o => ({id: o.id, stratName: o.stratName}))', lv)
                for opp in opps:
                    page.evaluate('([lv, id]) => { localStorage.clear(); currentLevel = lv; selectOpponent(id); }', [lv, opp['id']])
                    cells = page.evaluate('() => ["mc_cc", "mc_cd", "mc_dc", "mc_dd"].map(i => document.getElementById(i).textContent)')
                    want_cells = ['%s, %s' % (fmt(lv, a), fmt(lv, b)) for a, b in (PAY[('C', 'C')], PAY[('C', 'D')], PAY[('D', 'C')], PAY[('D', 'D')])]
                    if cells != want_cells:
                        fails.append('payoffs: %s: the matrix shows %r, expected %r' % (lv, cells, want_cells))
                    rounds = play_game(page, lv, opp['id'], PATTERN)
                    check_game(fails, page, lv, opp, kinds.get((lv, opp['id'])), rounds, PATTERN)
                    stats['games'] += 1
                # a tournament at this level, all-cooperate
                page.evaluate('(lv) => { localStorage.clear(); currentLevel = lv; startTournament(); }', lv)
                totals = {}
                for opp in opps:
                    totals[opp['id']] = play_game(page, lv, opp['id'], 'C' * 20)
                tr = page.evaluate('''() => { const c = document.getElementById("tournamentResultsContent");
                    return {rows: [...c.querySelectorAll("tr")].slice(1).map(r => [...r.children].map(td => td.textContent)),
                            total: (c.querySelector(".sb-val") || {}).textContent, ideal: (c.querySelector(".ideal-note") || {}).textContent}; }''')
                tot_y = 0
                for opp, row in zip(opps, tr['rows']):
                    kind = kinds.get((lv, opp['id']))
                    h, ys, ts = [], 0, 0
                    for r in totals[opp['id']]:
                        o = r['opp'] if kind == 'random' else move(kind, h)
                        a, b = PAY[('C', o)]
                        ys, ts = ys + a, ts + b
                        h.append(('C', o))
                    tot_y += ys
                    res = 'Win' if ys > ts else 'Loss' if ys < ts else 'Draw'
                    want_row = [row[0], fmt(lv, ys), fmt(lv, ts), res]
                    if row != want_row:
                        fails.append('tournament: %s %s: row %r, expected %r' % (lv, opp['id'], row, want_row))
                if len(tr['rows']) != len(opps) or tr['total'] != fmt(lv, tot_y) or \
                        tr['ideal'] != 'Perfect mutual cooperation across all matches: %s' % fmt(lv, 60 * len(opps)):
                    fails.append('tournament: %s: %d rows, total %r (expected %s), %r' % (lv, len(tr['rows']), tr['total'], fmt(lv, tot_y), tr['ideal']))
            if errors:
                fails.append('page errors: %s' % '; '.join(errors[:3]))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return stats


PLANTS = [
    ('the matrix title without (you, them)', 'matrix:', [("<h3 id=\"matrixTitle\">Payoff Matrix (you, them)</h3>", "<h3 id=\"matrixTitle\">Payoff Matrix</h3>")]),
    ('the Adaptive Firm described as profit-driven', 'pavlov:',
     [("repeats its pricing strategy after a good result (\u00a33k or \u00a35k) and changes it after a poor one (\u00a30k or \u00a31k)", "sticks with a pricing strategy while it\\'s profitable and changes when it\\'s not")]),
    ('the halfway prompt for Random Rita', 'random:',
     [("' is random, so there is no pattern to find.'", "' has a pattern.'")]),
    ('the tournament unlock unsaid', 'tournament:',
     [(" Tournament Mode unlocks once you have beaten 3 different opponents at this level (more points than them in a match).", "")]),
    ('the sucker payoff 1, not 0', 'payoffs:', [("if (playerChoice === 'cooperate' && opponentChoice === 'defect') return { p: 0, o: 5 };",
                                                  "if (playerChoice === 'cooperate' && opponentChoice === 'defect') return { p: 1, o: 5 };")]),
    ('Grudge Gary forgives after 3 rounds (KS3)', 'opponent:',
     [("      play: function(h) { for (let i = 0; i < h.length; i++) { if (h[i].player === 'defect') return 'defect'; } return 'cooperate'; }\n    }\n  ],\n  gcse:",
       "      play: function(h) { for (let i = Math.max(0, h.length - 3); i < h.length; i++) { if (h[i].player === 'defect') return 'defect'; } return 'cooperate'; }\n    }\n  ],\n  gcse:")]),
    ('Pavlov Pete switching after a win (GCSE)', 'opponent:',
     [("        const myLastPts = last.oPts; // opponent's points from history (Pete is the opponent)\n        if (myLastPts === 3 || myLastPts === 5) return last.opponent; // repeat",
       "        const myLastPts = last.oPts; // opponent's points from history (Pete is the opponent)\n        if (myLastPts === 1 || myLastPts === 5) return last.opponent; // repeat")]),
    ('a wrong figure in the GCSE expected value', 'statement:', [("E(X) = 0.5 x 5 + 0.5 x 1 = 3.0", "E(X) = 0.5 x 5 + 0.5 x 1 = 3.5")]),
    ('the end screen counting mutual defection as cooperation', 'scores:',
     [("    if (h.player === 'cooperate' && h.opponent === 'cooperate') mutualCoop++;\n    else if (h.player === 'defect' && h.opponent === 'defect') mutualDef++;",
       "    if (h.player === h.opponent) mutualCoop++;\n    else if (h.player === 'defect' && h.opponent === 'defect') mutualDef++;")]),
    ('the tournament total missing the last match', 'tournament:',
     [("  tournamentOpponents.forEach(function(opp) {\n    const s = tournamentScores[opp.id];\n    totalPlayer += s.player;",
       "  tournamentOpponents.slice(0, -1).forEach(function(opp) {\n    const s = tournamentScores[opp.id];\n    totalPlayer += s.player;")]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-selftest', action='store_true')
    ap.add_argument('--against', help='serve this file as the game page')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    html = open(args.against or GAME, encoding='utf-8').read()
    fails = []
    check_text(fails, html)
    st = play(fails, html)
    print('%s: payoffs checked; every opponent at every level against its stated rule over %d histories; %d games of 20 rounds and a '
          'tournament per level played in Chromium, every score, count and stated figure recomputed' % (SLUG, st.get('cases', 0), st.get('games', 0)))
    print('  not asserted (open): leaderboard ranking (t4-001, waits on Jon), ?level keys (t4-003), TF2T name (t4-004), the Discount '
          "Store's hint (t4-005), Tara's name (t4-006), small text points (t4-007)")
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
            check_text(rep, planted)
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
