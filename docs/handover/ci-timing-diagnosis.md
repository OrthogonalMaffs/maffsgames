# CI timing gate: diagnosis and proposed design (14 Oct 2026, home lane, report only)

Nothing in CI, the budgets, the 75% and 80% figures, the packer or any verifier was changed. Every number below was read
from the job logs of real runs (`gh api repos/OrthogonalMaffs/maffsgames/actions/runs/<id>/logs`, no extra credentials
needed): the per-verifier line `ok <label> (Ns; group at MmSSs of Tm)` that `check-site.yml` prints.

**Sample.** The last 80 `push` (main) runs and 80 `pull_request` runs that ended in success or failure: 160 runs,
12 Oct 23:36 to 14 Oct 18:53 UTC (about 43 hours), 25,323 timed verifier lines. Cancelled runs are left out. That is
all the history the retention and the page size gave; it is well past the ~15 runs the contract asked for, but it is
two days, not weeks, and the verifiers themselves changed during it (see "Honest limits").

## 1. How the gate decides today

| Where | What fails | Against what number |
|---|---|---|
| **Every run (PR and main), per content or lock group** | The step *Content verifiers N* (or *Answer lock*), then *Gate (every job passed)* | **That run's own clock**: elapsed seconds since the group's first step, checked after each verifier line. Fails once `elapsed > 75% of the group's timeout` (content: 270 s of a 6-minute timeout; lock: 450 s of 10). The error reads `time budget: Content verifiers 19 at 4m50s of 6m (budget 4m30s, 75%): split it`. |
| Every run, hang guard | GitHub cancels the job | `timeout-minutes` = the group's timeout + 10 minutes of image-pull allowance (`PULL_ALLOWANCE`). Nothing in the 160 runs came near it. |
| **Every PR**, job *Plan* | `ci-groups.py --check` | A group's *estimated* time (setup + the lines' recorded **medians**) past **80%** of its budget. This is a number from `ci-timings.json`, not from the run. Only a single line too big for any group can trip it. |
| **Main only**, job *CI timings and pack* | `ci-groups.py --record-and-pack` | Records the run, takes the **median of the last 5 main runs** per line, repacks to 70% of budget, applies the same 80% `--check` to the result and writes nothing if it fails. This is what failed on 14 Oct (Content verifiers 20 estimated at 82%). |

So there are two different kinds of number. The packer and the `--check` already judge **medians of five main runs**
and ignore one slow run. The failure that hits single PR or main runs on unchanged code is the first row: the
**per-run clock**, which has no memory and no tolerance.

Both failures reported as flaky were exactly that row, confirmed from their logs:

| Run | Group | What happened | Verdict |
|---|---|---|---|
| 38600298822 (main, 14 Oct 16:42) | Content verifiers 19 | Equation Builder part 1 took **260 s** (its median 136 s). Every verifier printed `ok`. `time budget: Content verifiers 19 at 4m50s of 6m (budget 4m30s, 75%)` | Failed on the clock alone. Green on re-run. |
| 38556658031 (PR, 14 Oct 11:27) | Content verifiers 28 | Spot the Muppet took **290 s** (neighbouring runs 94 s). `time budget: Content verifiers 28 at 5m05s of 6m` | Same. |

I could not find "Just Pythag It part 4 at 242 s" in the 160 runs: its longest line is 184 s and its longest group clock
211 s. The 242 s figure is not in this window (it may be from an earlier run, or a group clock rather than the line).
I am not counting it.

## 2. What the data says

**Per verifier** (all 160 runs; the heaviest by median; the Answer lock parts are the steadiest lines in CI):

| Verifier | runs | median s | p90 s | max s | max / median |
|---|---|---|---|---|---|
| Answer lock in play, part 1 | 155 | 263 | 264 | 267 | 1.02 |
| Answer lock in play, part 6 | 155 | 234 | 236 | 237 | 1.01 |
| Answer lock in play, part 5 | 155 | 204 | 205 | 210 | 1.03 |
| Answer lock in play, part 2 | 155 | 176 | 178 | 179 | 1.02 |
| Free Daily Pizza | 155 | 165 | 173 | 213 | 1.29 |
| Answer lock in play, part 3 | 155 | 165 | 166 | 167 | 1.01 |
| Just Pythag It, Bruv, part 4 | 156 | 154 | 162 | 184 | 1.19 |
| Answer lock in play, part 4 | 155 | 147 | 148 | 150 | 1.02 |
| Just Pythag It, Bruv, part 2 | 155 | 145 | 146 | 148 | 1.02 |
| **Equation Builder, part 1** | 156 | 136 | 155 | **260** | **1.90** |
| Equation Builder, part 2 | 155 | 132 | 144 | 150 | 1.14 |
| Probability Paradox | 155 | 124 | 162 | 211 | 1.70 (a regime change, see 14 Oct below) |

Push and pull-request runs have the same medians to within a few seconds (for example Free Daily Pizza 162 s on main,
166 s on PRs): the verifiers do not run differently on PRs.

**Per group** (the content groups, by worst single run; budget 270 s):

| Group | runs | median s | p90 s | max s |
|---|---|---|---|---|
| Content verifiers 28 | 155 | 87 | 124 | **305** |
| Content verifiers 19 | 156 | 155 | 174 | **290** |
| Content verifiers 25 | 155 | 98 | 114 | 255 |
| Content verifiers 7 | 155 | 154 | 200 | 253 |
| Content verifiers 14 | 155 | 120 | 156 | 246 |
| Content verifiers 5 | 156 | 142 | 174 | 245 |
| Content verifiers 11 | 155 | 128 | 152 | 242 |
| Content verifiers 2 | 155 | 182 | 191 | 239 |

Across 5,448 content group-runs, **2 went past the 270 s budget** (the two above), which is 1 run in 80. Every other
group's worst run in the sample was at or under 255 s, including the ones with median over 150 s.

**Is it runner variance?** Mostly not, in the sense the question assumed:

* **Not whole-run slowness.** For each run, the median of (each line's time ÷ that line's median) is 1.00 across the
  runs (p10 0.97, p90 1.03, one run at 1.47). A slow runner would lift every line in a run; it did not. The two failing
  runs were normal everywhere except one line.
* **A rare single-line stall.** Comparing each line with the median of its eight neighbouring runs, **33 of 25,323 timed
  lines (0.13%)** are isolated outliers (more than 1.5× and at least 15 s over), spread across **25 of the 160 runs**
  (6 runs have two or more). Examples: Spot the Muppet 290 s against 94 s, Equation Builder part 1 260 s against 117 s,
  Decimal Detective 200 s against 74 s, Index Laws 109 s against 47 s. That is a stall inside one verifier, which is
  consistent with a cold SymPy or Chromium start or a retry; the logs show no more than the `ok` line, so **the cause
  inside the verifier is not confirmed**.
* **Clustering.** By verifier type: the labels do not say which verifiers drive a browser (only 1.2% mention
  Chromium), so I cannot split browser from pure compute reliably; the 33 outliers are all in lines whose labels do not
  mention Chromium, which tells nothing either way. By time of day: the flagged lines follow where the runs are (busy
  12:00 to 17:00 UTC), with no hour standing out per run. By concurrency: runs started within 10 minutes of a run with
  an outlier is a median of 3, the same as for all runs. One bunching: three of the six runs with two or more outliers fall in one
  55-minute window on 14 Oct (38599217245 at 16:34, 38605874736 at 17:20, 38607039775 at 17:29 UTC, the last with four),
  which could be a slow spell on the runner pool, but three runs are too few to call it a pattern.
* **Most "slow" lines are not stalls, they are growth.** Lines flagged by a plain 1.5× test (166 of them) are mostly a
  verifier whose time *changed* during the window: Spot the Muppet went from about 70 s to about 123 s as the
  option-parity PRs landed, so its single 290 s stall is one real outlier on top of a slower regime. Thirteen more
  verifiers show the same persistent step over the 31 main runs (Formula Forge, Formula Unlocked, Factor Theorem, Bearing
  Blitz, Growth and Decay, Decimal Detective, Given That and others, up 25 to 50%). **No current gate notices these; they only show up
  as a pack that creeps towards 80%.**

**14 Oct, Probability Paradox (the real catch).** Push runs in time order, seconds:
`161 155 160 161 161 | 210 211 (missing) 202 | 51 57 57 47 51 58 …`. It rose from 161 to about 210 on the first main run
after #371 and stayed there for three main runs; #376 took it to about 50. The per-run clock **never fired** for it (its
group reached at most 230 s, under 270). It was caught by the main-only job when the median of five reached 202 s,
which is the **third slow main run** (08:35), and that is by design: one or two slow runs do not move a median of five.

## 3. Candidate designs, backtested

| Design | Catches Probability Paradox (161 → 203) | Passes the Equation Builder flake (260 s) | Passes the Spot the Muppet flake (290 s) |
|---|---|---|---|
| **Today**: fail a run past 75% of timeout on that run's clock; medians for packing | Not by the clock. Yes by the median, on the 3rd slow main run | **No** (failed) | **No** (failed) |
| **A. Judge on recorded medians**: the per-run 75% check becomes a warning (annotation plus summary line naming the slowest verifier); compliance stays with the median-of-5 packing and the 80% `--check`; the 10-minute-plus hang guard stays as the only per-run failure | Yes, on the 3rd slow main run (unchanged) | **Yes** | **Yes** |
| **B. Per-run hard timeout at a multiple of median** | A multiple that catches it must be at most 1.26× (203 ÷ 161). The flakes were 1.9× and 3.1×, so that threshold fails both flakes and, over the first 64-run sample, fires on 222 of 2,201 baseline-checked lines at 1.3× and 100 at 1.5×. To pass the flakes it must be above 3.1×, which misses Probability Paradox. **No multiple does both** | Only if above 1.9× | Only if above 3.1× |
| **C. Persistence rule**: a verifier whose last 3 main runs are each more than 20% and at least 15 s over the median of the 5 runs before them is reported by name | Yes, on the 3rd slow main run (run 8 of 31), now naming the verifier | Yes (a single run never fires) | Yes |

The separating fact is **persistence**: the regression stayed for every run after it, the flakes lasted one run. A
threshold on a single run's number cannot tell them apart (B); anything that looks across runs can (A, C).

Over the 31 main runs in the sample, rule C fires on 14 verifiers; the ones I looked at are real, lasting increases
(Probability Paradox 161 → 210; Bearing Blitz 85 → 125; Factor Theorem 79 → 107; Formula Unlocked 50 → 84; Growth and
Decay 106 → 131). That is why C is a **report**, not a second failing gate: failing main on all of them would turn ordinary
content growth into red builds.

## 4. Recommendation (one design: A plus the C report)

1. **Make the per-run 75% check a warning, not a failure.** The group still prints its budget line and the step summary
   names the slowest verifier and its median, but the run passes unless the existing hang guard (timeout plus pull
   allowance) cancels it. This removes the only gate that fired on unchanged code (2 of the 160 runs, 1 in 80), and it
   changes no budget and no figure: 75% and 80% keep their meaning, applied to medians, which is what the packer
   already does.
2. **Keep the blocking size gate where it is**: the median-of-5 pack and the 80% `--check` (PR) and
   `--record-and-pack` (main). Backtest: it caught Probability Paradox on the 3rd slow main run, and the two flakes
   never reach it.
3. **Add rule C to the main-only timings job as a named report** (job summary and an annotation, not a failure), so a
   verifier that has grown persistently is named at the third run rather than appearing only as a group at 82%.
   Backtest: names Probability Paradox on run 8 of 31, the same run the pack check failed, plus the other lasting
   increases above.

Backtested against the three cases: Probability Paradox **caught** (median pack check, unchanged, plus rule C naming it);
Equation Builder 260 s **passes**; Spot the Muppet 290 s **passes**. Not recovered: a regression of about 1.26× is still
only seen after three main runs, never on the PR that caused it. Seeing it on the PR would need a per-line comparison
with the median, and the measured single-line noise (about 0.13% of lines are isolated outliers, up to 3×) means that
comparison would have to retry the line before judging; I did not design that here.

## 5. Honest limits

* Two days of history (43 hours) across 160 runs. The verifiers changed during it, which is why a plain "1.5× the
  median" flags many lines that are really a new regime; the neighbour-median method above separates them, but a longer
  window would give firmer p90 and max figures.
* No log line says *why* a verifier stalled, so "cold SymPy or Chromium start, or a retry" is an inference. A one-line
  `time` print around the slowest steps of Equation Builder and Spot the Muppet would settle it.
* The "Just Pythag It part 4 at 242 s" case was not in the sample and is not backtested.
* Nothing here has been run as a change. Option 1 touches the shared workflow and changes what a ruled figure (the
  75% budget, Jon, 5 Oct 2026) does on a single run, so it needs Jon's ruling before anyone implements it.
