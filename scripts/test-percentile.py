#!/usr/bin/env python3
# ci-line: Leaderboard percentile ranking rules (submitScore's percentile and tier follow standing()'s rankRules: lower-is-better ranked the right way round, unrankable boards get none, higher-is-better ties as before, tiers exact at the thresholds; planted faults caught) |
# ci-deps: games/estimation-golf/ games/maffscards/ games/higher-power/ schools/assets/firebase-leaderboard.js
"""Tests the percentile and certificate tier that MaffsLeaderboard.submitScore() resolves
(schools/assets/firebase-leaderboard.js; contract PERCENTILE-LOWER-IS-BETTER, 21 Nov 2026). No network and no
browser: the script runs in Node's vm module with no Firebase SDK, as scripts/check-leaderboard-coverage.js loads it.

    python scripts/test-percentile.py

submitScore()'s then-block returns rankScore(gameSlug, score, allScores) once the board is read; this test calls
that same function. What it proves:
  (a) higher-is-better: the best of [10, 20, 30] gets the top percentile of the three, and the best of a board
      big enough for the thresholds (1..21, 1..10) gets gold and silver;
  (b) lower-is-better (estimation-golf and maffscards): the best (lowest) score gets the same;
  (c) the worst score gets the bottom percentile (1) and no tier, both ways round;
  (d) every MIXED_UNRELIABLE game gets percentile null and tier null, with totalPlayers still counted;
  (e) higher-is-better ties are counted exactly as before this change: random boards with many ties give the
      same percentile as the old calculatePercentile, copied here unchanged, and the tier a whole-number
      reference gives;
  (f) the tier is exact at the thresholds (SOME-THINGIES step 1b, 21 Nov 2026): the best of exactly 20 gets
      gold and the second of 20 silver, both ways round (1 - 19/20 is 0.050000000000000044 in floating
      point, which used to miss gold).
Also: rankRules() agrees with LOWER_IS_BETTER and MIXED_UNRELIABLE; standing() takes its direction and rankable
from rankRules() and resolves as before with no Firebase; submitScore() returns rankScore()'s result.

Then four planted faults, each a one-line change to the file, and each must make its check fail: the direction
argument ignored (b), the rankable rule ignored (d), a higher-is-better tie counted as worse (e), and the old
floating-point threshold comparison (f).

Node: the runner's, or the copy the Playwright package ships (as test-ga4-country.py does).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "schools", "assets", "firebase-leaderboard.js")

HARNESS = r"""
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[2], 'utf8');
const sandbox = { window: {}, console: { warn() {}, log() {}, error() {} } };
vm.createContext(sandbox);
vm.runInContext(src, sandbox);
const L = sandbox.window.MaffsLeaderboard;
const fails = [];
function check(tag, ok, msg) { if (!ok) fails.push(tag + ': ' + msg); }
function near(a, b) { return a !== null && b !== null && Math.abs(a - b) < 1e-12; }
function range(n) { const a = []; for (let i = 1; i <= n; i++) a.push(i); return a; }

// The old calculatePercentile, unchanged (main ff244be): the reference for higher-is-better ties.
function oldPercentile(score, allScores) {
  if (!allScores.length) return null;
  let below = 0;
  for (let i = 0; i < allScores.length; i++) if (allScores[i] < score) below++;
  return 1 - below / allScores.length;
}
// The tier in whole numbers: in the top 5% when (n - worse) / n <= 1/20, the top 10% when <= 1/10.
function refTier(n, worse) { return (n - worse) * 20 <= n ? 'gold' : (n - worse) * 10 <= n ? 'silver' : null; }
check('setup', L.GOLD_THRESHOLD === 0.05 && L.SILVER_THRESHOLD === 0.10, 'the thresholds are not 0.05 and 0.10 (refTier assumes them)');

const HIGHER = 'differentiation-duel';
const LOWER = Object.keys(L.LOWER_IS_BETTER);
const UNRANKABLE = Object.keys(L.MIXED_UNRELIABLE);
check('setup', !L.LOWER_IS_BETTER[HIGHER] && !L.MIXED_UNRELIABLE[HIGHER], HIGHER + ' is not a plain higher-is-better game');
check('setup', LOWER.indexOf('estimation-golf') >= 0 && LOWER.indexOf('maffscards') >= 0, 'LOWER_IS_BETTER lacks estimation-golf or maffscards');
check('setup', UNRANKABLE.length > 0, 'MIXED_UNRELIABLE is empty');
check('setup', typeof L.rankScore === 'function' && typeof L.rankRules === 'function', 'rankScore/rankRules not exported');
if (fails.length) { process.stdout.write(JSON.stringify(fails)); process.exit(0); }

// (a) higher-is-better
let r = L.rankScore(HIGHER, 30, [10, 20, 30]);
const others = [10, 20].map(s => L.rankScore(HIGHER, s, [10, 20, 30]).percentile);
check('a', near(r.percentile, 1 / 3) && others.every(p => p > r.percentile), 'best of [10,20,30] percentile ' + r.percentile + ', others ' + others);
check('a', r.tier === null && r.totalPlayers === 3, 'best of three: tier ' + r.tier + ', totalPlayers ' + r.totalPlayers);
r = L.rankScore(HIGHER, 21, range(21));
check('a', near(r.percentile, 1 / 21) && r.tier === 'gold', 'best of 1..21: ' + JSON.stringify(r));
r = L.rankScore(HIGHER, 10, range(10));
check('a', near(r.percentile, 0.1) && r.tier === 'silver', 'best of 1..10: ' + JSON.stringify(r));

// (b) lower-is-better, every LOWER_IS_BETTER game
for (const g of LOWER) {
  r = L.rankScore(g, 10, [10, 20, 30]);
  const rest = [20, 30].map(s => L.rankScore(g, s, [10, 20, 30]).percentile);
  check('b', near(r.percentile, 1 / 3) && rest.every(p => p > r.percentile), g + ': best (10) of [10,20,30] percentile ' + r.percentile + ', others ' + rest);
  r = L.rankScore(g, 1, range(21));
  check('b', near(r.percentile, 1 / 21) && r.tier === 'gold', g + ': best (1) of 1..21: ' + JSON.stringify(r));
  r = L.rankScore(g, 1, range(10));
  check('b', near(r.percentile, 0.1) && r.tier === 'silver', g + ': best (1) of 1..10: ' + JSON.stringify(r));
}

// (c) the worst gets the bottom, both ways round
r = L.rankScore(HIGHER, 10, [10, 20, 30]);
check('c', r.percentile === 1 && r.tier === null, 'higher worst (10): ' + JSON.stringify(r));
for (const g of LOWER) {
  r = L.rankScore(g, 30, [10, 20, 30]);
  check('c', r.percentile === 1 && r.tier === null, g + ' worst (30): ' + JSON.stringify(r));
  r = L.rankScore(g, 20, range(20));
  check('c', r.percentile === 1 && r.tier === null, g + ' worst (20) of 1..20: ' + JSON.stringify(r));
}

// (d) unrankable boards: no percentile, no tier, players still counted
for (const g of UNRANKABLE) {
  for (const [score, board] of [[30, [10, 20, 30]], [20, range(20)], [1, range(20)]]) {
    r = L.rankScore(g, score, board);
    check('d', r.percentile === null && r.tier === null && r.totalPlayers === board.length, g + ' ' + score + ': ' + JSON.stringify(r));
  }
}

// (e) higher-is-better ties exactly as before
r = L.rankScore(HIGHER, 20, [10, 20, 20, 30]);
check('e', r.percentile === oldPercentile(20, [10, 20, 20, 30]) && near(r.percentile, 0.75), 'tie [10,20,20,30] at 20: ' + r.percentile);
let seed = 12345;
function rnd(n) { seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n; }
for (let t = 0; t < 2000; t++) {
  const n = 1 + rnd(40), board = [];
  for (let i = 0; i < n; i++) board.push(rnd(6));
  const score = board[rnd(n)];
  r = L.rankScore(HIGHER, score, board);
  const p = oldPercentile(score, board);
  const worse = board.filter(x => x < score).length;
  if (r.percentile !== p || r.tier !== refTier(n, worse) || r.totalPlayers !== n) {
    check('e', false, 'board ' + JSON.stringify(board) + ' score ' + score + ': ' + JSON.stringify(r) + ', old ' + p);
    break;
  }
}

// (f) exact at the thresholds, both ways round
r = L.rankScore(HIGHER, 20, range(20));
check('f', r.tier === 'gold', 'higher: best of exactly 20: ' + JSON.stringify(r));
r = L.rankScore(HIGHER, 19, range(20));
check('f', r.tier === 'silver', 'higher: second of 20: ' + JSON.stringify(r));
r = L.rankScore(HIGHER, 18, range(20));
check('f', r.tier === null, 'higher: third of 20: ' + JSON.stringify(r));
r = L.rankScore(HIGHER, 10, range(10));
check('f', r.tier === 'silver', 'higher: best of exactly 10: ' + JSON.stringify(r));
for (const g of LOWER) {
  r = L.rankScore(g, 1, range(20));
  check('f', r.tier === 'gold', g + ': best (1) of exactly 20: ' + JSON.stringify(r));
  r = L.rankScore(g, 2, range(20));
  check('f', r.tier === 'silver', g + ': second (2) of 20: ' + JSON.stringify(r));
}
for (let n = 1; n <= 200; n++) {
  for (let rank = 1; rank <= Math.min(n, 25); rank++) {
    r = L.rankScore(HIGHER, n - rank + 1, range(n));
    if (r.tier !== refTier(n, n - rank)) { check('f', false, 'rank ' + rank + ' of ' + n + ': ' + r.tier + ', want ' + refTier(n, n - rank)); n = 999; break; }
  }
}

// rankRules agrees with the two maps
for (const g of [HIGHER].concat(LOWER, UNRANKABLE)) {
  const x = L.rankRules(g);
  check('rules', x.direction === (L.LOWER_IS_BETTER[g] ? 'lower' : 'higher') && x.rankable === !L.MIXED_UNRELIABLE[g], g + ': ' + JSON.stringify(x));
}

// standing() as before, with no Firebase (it never reaches the database)
const st = {};
Promise.all([HIGHER].concat(LOWER, UNRANKABLE).map(g => L.standing(g, 'gcse').then(v => { st[g] = v; }))).then(() => {
  for (const g of Object.keys(st)) {
    const v = st[g], want = { allTimeBest: null, weekBest: null, direction: L.LOWER_IS_BETTER[g] ? 'lower' : 'higher', rankable: !L.MIXED_UNRELIABLE[g] };
    check('standing', JSON.stringify(v) === JSON.stringify(want), g + ': ' + JSON.stringify(v));
  }
  process.stdout.write(JSON.stringify(fails));
});
"""

# (name, the one-line change, the check that must fail)
PLANTS = [
    ("direction ignored",
     "if (direction === 'lower' ? allScores[i] > score : allScores[i] < score) scoresWorse++;",
     "if (allScores[i] < score) scoresWorse++;", "b"),
    ("rankable ignored",
     "var percentile = rules.rankable ? calculatePercentile(score, allScores, rules.direction) : null;",
     "var percentile = calculatePercentile(score, allScores, rules.direction);", "d"),
    ("the old floating-point threshold comparison",
     "return (n - worse) * 100 <= Math.round(t * 100) * n;",
     "return 1 - worse / n <= t;", "f"),
    ("higher-is-better tie counted as worse",
     "if (direction === 'lower' ? allScores[i] > score : allScores[i] < score) scoresWorse++;",
     "if (direction === 'lower' ? allScores[i] > score : allScores[i] <= score) scoresWorse++;", "e"),
]


def find_node():
    node = shutil.which("node")
    if node:
        return node
    try:
        import playwright
        cand = os.path.join(os.path.dirname(playwright.__file__), "driver", "node")
        if os.path.exists(cand) or os.path.exists(cand + ".exe"):
            return cand
    except ImportError:
        pass
    sys.exit("FAIL  no node on PATH and no Playwright driver node")


def run(node, source, work, tag):
    path = os.path.join(work, "lb-%s.js" % tag)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(source)
    p = subprocess.run([node, os.path.join(work, "harness.js"), path], capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout), None


def static_checks(src):
    """The wiring the harness cannot see without Firebase: submitScore and standing use the shared rules."""
    bad = []
    if src.count("return rankScore(gameSlug, score, allScores);") != 1:
        bad.append("submitScore() does not return rankScore(gameSlug, score, allScores) once")
    if src.count("calculatePercentile(") != 2:  # its definition and rankScore's one call
        bad.append("calculatePercentile() is called somewhere other than rankScore()")
    body = src[src.index("function standing("):]
    body = body[:body.index("standingCache[cacheKey] = promise;")]
    if "rankRules(gameSlug)" not in body or "LOWER_IS_BETTER[" in body or "MIXED_UNRELIABLE[" in body:
        bad.append("standing() does not take its rules from rankRules()")
    return bad


def main():
    src = open(SRC, encoding="utf-8").read()
    node = find_node()
    failed = static_checks(src)
    for b in failed:
        print("FAIL  " + b)
    work = tempfile.mkdtemp(prefix="test-percentile-")
    try:
        with open(os.path.join(work, "harness.js"), "w", encoding="utf-8", newline="") as f:
            f.write(HARNESS)
        fails, err = run(node, src, work, "real")
        if fails is None:
            print("FAIL  the harness did not run on the real file: " + err)
            return 1
        for x in fails:
            print("FAIL  " + x)
        failed += fails
        if not fails:
            print("PASS  (a)-(f), rankRules and standing() on the real file")
        for name, old, new, tag in PLANTS:
            if src.count(old) != 1:
                print("FAIL  plant %r: its line is not in the file once (update the plant)" % name)
                failed.append(name)
                continue
            got, err = run(node, src.replace(old, new), work, "plant")
            caught = got is not None and any(x.startswith(tag + ":") for x in got)
            print("%s  plant %r %s check (%s)" % ("PASS" if caught else "FAIL", name, "fails" if caught else "does NOT fail", tag))
            if not caught:
                failed.append(name)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("OK" if not failed else "FAILED (%d)" % len(failed))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
