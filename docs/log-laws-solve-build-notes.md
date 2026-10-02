# Log Laws "Solve": build notes (28 Sep 2026)

These notes are not part of the contract. The contract, with all of Jon's rulings, is
`docs/next-contract-log-laws-solve.md`; read it first. This file hands over what a 28 Sep web
session found and designed before it stopped to free up context. **No game code was written.**
The class is w/c 12 Oct 2026, and the build must be live before then.

## Findings to rely on (re-verify if the code has moved)

**The game** (`games/log-laws/index.html`):
- The Laws drill is 12 questions (`TOTAL = 12`) drawn from 45 with `shuffle` (a sort-based shuffle;
  leave it alone).
- `'alevel'` is hard-coded in six places at `:825`–`:927`: `game_abandoned`, `game_started`,
  `question_answered`, `game_completed`, `submitScore` with `MaffsScoreHistory`, and
  `personal_best_set`.
- The header pill `<span class="header-level">A-Level</span>` is static.
- The personal best is in `ll_best` and local top scores in `ll_scores`.
- KaTeX 0.16.9 loads deferred, and the game waits for it with `waitForKaTeX`.

**Tier 3 and the Laws drill's baseline:**
- In a web session the KaTeX CDN is refused, so tier 3 reports log-laws UNSUPPORTED, which is
  meaningless.
- With KaTeX served from the npm package, and empty stand-ins for Google Fonts and the Firebase SDK,
  the baseline is **3 PASS, 30 questions played**. That is the result the Laws drill must keep. The
  package is `katex-0.16.9.tgz` from registry.npmjs.org, shasum
  `bc62d8f7abfea6e181250f85a56e4ef292dcb1fa`.
- The test-only wrapper that does this, never committed, is below.

**Tier 3 presses the first visible control that looks like a start button.**
- A control qualifies if its text is start / play / begin / go, or its id or class contains "start"
  (`startEls()` in `scripts/check-site.py`, around `:1227`).
- So new mode, stage and length controls must avoid those words. Keep "Start Game" as the first
  match and Laws as the default mode, and the Laws drill's tier 3 path does not change.

**Other checker facts:**
- **Roster levels:** `check-site.py`'s `LEVEL_SLUGS` (around `:574`) has no `l3`, so "L3" in the
  roster would be silently ignored. Add `"l3": "level3"` so tiers 1 and 3 load `?level=level3`.
- **`serve-stubbed.py`** probe-binds its port without `SO_REUSEADDR`. A checker run started within
  about a minute of the last one finds the port in TIME_WAIT, and gets "connection refused". Wait
  for the port to free.
- **Tier 4 locally** needs `pip install --use-pep517 esprima`. SymPy installs from PyPI normally.
- **Leaderboard coverage:** `check-leaderboard-coverage.js` fails a file containing
  `LEADERBOARD_MODE_READY` unless the slug is in `HELD`, and its comment says to keep canon §9 in
  sync. log-laws will have an ungated Laws call and a gated Solve call; the gated one needs the HELD
  entry.

**Shared helpers and labels:**
- **`MaffsSession`** always adds an "All (n)" button when n isn't a preferred length. Solve pools run
  to 40–100+ per family, so pass `poolSize` capped at the longest Solve session. Every button then
  still serves its label, there is no "All (300)", and the helper stays untouched.
- **`LEVEL_LABELS`** has two shared copies, `firebase-leaderboard.js:73` and
  `leaderboards/index.html:168`. The `level3` entry goes in both; see the contract.

The test-only tier 3 wrapper:

```python
import os, runpy, sys
import playwright.async_api as pa
KATEX = '<unpacked package>/dist/'
PREFIX = 'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/'
_orig = pa.Page.route
async def route(self, url, handler, times=None):
    async def wrapped(r):
        u = r.request.url
        if u.startswith(PREFIX):
            p = os.path.join(KATEX, u[len(PREFIX):].split('?')[0])
            if os.path.isfile(p):
                return await r.fulfill(path=p)
        if u.startswith('https://fonts.googleapis.com/'):
            return await r.fulfill(status=200, body='', content_type='text/css')
        if u.startswith('https://www.gstatic.com/firebasejs/'):
            return await r.fulfill(status=200, body='', content_type='application/javascript')
        return await handler(r)
    return await (_orig(self, url, wrapped, times) if times else _orig(self, url, wrapped))
pa.Page.route = route
sys.argv = ['check-site.py'] + sys.argv[1:]
runpy.run_path('scripts/check-site.py', run_name='__main__')   # e.g. --only log-laws --tier 3
```

## Pools, prototyped: counts after the rounding-boundary filter

| Family | Enumeration | Items |
|---|---|---|
| F1 `aˣ = b` | a 2–9 × b {5,7,10,12,15,20,30,45,50,60,80,100}, b not a power of a | 94 |
| F2 | `a^{kx} = b`: a {2,3,5,7} × k {2,3,4} × b {10,20,50,100}; `a^{x+k} = b`: a {2–6} × k {±1,±2} × b {10,30,100} | 108 |
| F3 | `e^{kx} = b`: k {2–5} × b {3,5,7,10,20,50}, plus k {−1,−2} × b {0.2,0.5}; `V = V₀e^{−t/RC}`: (V₀,V) (12,6),(12,3.5),(12,2),(9,3),(9,4.5),(5,1.5),(5,2),(24,6) × (R kΩ, C μF) (1,100),(2.2,100),(4.7,100),(10,100),(2.2,1000),(4.7,1000); RC = R·C/1000 s | 76 |
| F4 | base {log₁₀, ln} × a {1,2,3,4,5,6,8,10} × b {2–6}; x = a/(b−1); domain x > 0 | 80 |
| F5 | "= 1": (r,k) (1,9),(2,3),(5,−3),(10,−9); "= log m": r 1–9, k −(r−1)…9, k ≠ 0, 2 ≤ m = r(r+k) ≤ 60, m ≠ 10; the invalid root is −(r+k); domain x > max(0,−k) | 83 |
| F6 `aˣ = b^{x−k}` | a, b ∈ {2,3,5,6,7}, a ≠ b, k {1,2,3} | 60 |

## Design, proposed within the contract (flag the starred items to Jon in the report)

- **One expression tree per line.** Each line of working is built once as a small tree, which
  renders to TeX for KaTeX and to SymPy text for the verifier. The key's numeric value comes from
  the same tree, so what is verified is exactly what is shown.
- **Each item is a small state graph:**
  - `states` (TeX, SymPy text, kind);
  - `go`, the valid moves and where each leads;
  - `why`, a reason id for every other move, so each non-final state covers all nine moves;
  - F5's "which solution is valid?" step, with options x = s, x = r, Both.

  The whole config is exported as `window.LL_SOLVE`.
- **Honest branching.**
  - F1, F2 and F6 accept either log₁₀ or ln at the take-logs step, and the chain continues in the
    chosen base.
  - F3 accepts only ln. log₁₀ gets "works, but leaves log₁₀ e".
  - Valid alternative routes are accepted: F3's power law before ln e = 1, F6's quotient law on
    x(log a − log b), and F5 "= 1" writing 1 as log 10.
  - Any other valid-but-not-this-route move gets a "That works, but…" reason, never "wrong".
- **\* The move label** is "log 10 = 1 / ln e = 1", not the contract's "log_a a = 1". Rule 3 says no
  other base appears anywhere in Solve mode. For the same reason the Solve start screen and quick
  reference drop change of base.
- **Named reasons.** One catalogue keyed by state kind (exp, expCoef, logPow, lnE, eCoef, lin, diff,
  sum, single, alg), with per-family overrides. It includes the contract's wording: "the power law
  moves an index to the front — there is no index here".
- **\* Stages.** The start screen picks stage 1–6, with no locks.
  - A stage-s session is the focus family, with every third question from an earlier family,
    round-robin.
  - Lengths are [5, 10, 15] via `MaffsSession`, with `poolSize` capped at 15.
  - The game-over screen offers the next stage.
- **\* Scoring.**
  - A correct final answer scores max(4, 10 − 2 × wrong moves) + streak × 3; a wrong one scores 0.
  - Solve's personal best is `ll_best_solve` and its local scores `ll_scores_solve`.
  - Solve is held off the leaderboard *and* out of score history, because modes would mix, behind
    `LEADERBOARD_MODE_READY`, with a HELD entry and a canon §9 line.
- **The final answer is typed**, and correct iff it equals the root rounded to 3 s.f. The
  misconceptions:
  - `misDivide` (F1, F2);
  - `misK` (F2, and F3, including "forgot RC");
  - `misRoot` (F5).

  Each is kept only where its 3 s.f. value differs from the answer. On a wrong answer: an
  evaluation line is added to the chain, then the misconception message if it matched, then
  `MaffsNext`.
- **Levels:** `?level=` `alevel` (default) / `level3` / `level4`, with the header pill showing the
  label. `mode: 'laws' | 'solve'` goes on every event. The Laws drill's only other change is the
  "Skip change of base" checkbox, unticked by default. In Solve it shows ticked and disabled.

## `scripts/verify-log-laws.py`: the approach, prototyped and working

- **Parsing.** Parse each line's SymPy text with plain `Symbol`s. With `real=True`, SymPy expands
  `log(3**x)` on its own and the power-law check can no longer tell the lines apart.
- **Solution sets.** For every line, find the solution set on the item's domain:
  - `solveset(expand_log(lhs − rhs, force=True))`;
  - failing that, `sympy.solve` plus a residual check and the domain filter (lines with x inside a
    log need this).

  Compare sets **numerically**. SymPy returns equal roots in different forms.
- **Law checks per move:**
  - take logs: the log of each side;
  - power: `log(b**e)` becomes `e·log b`;
  - product / quotient: equal under `expand_log`, with fewer log atoms on the changed side;
  - log 10 = 1 / ln e = 1: equal after evaluation, with `log(E)` or `log(10, 10)` present;
  - undo: the arguments of the single logs;
  - rearrange: equivalent, with an identical set of log atoms.
- **Other checks:**
  - every root matches SymPy's own solve of the first line, to 1e-9;
  - no root is within 1e-6 of a 3 s.f. rounding boundary;
  - every pool is ≥ 40;
  - every non-final state covers all 9 moves;
  - every misconception value differs from the answer;
  - F5's rejected root makes an argument ≤ 0 and the kept root does not;
  - no `\log_` except `\log_{10}` in any Solve string;
  - every line parses in KaTeX (in CI, where KaTeX loads).
- **CI:** add `pip install sympy` and a step to `.github/workflows/check-site.yml`.
