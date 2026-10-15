# CI slowdown at #401: Equatle and Log Laws Solve (diagnosis, report only)

Contract CI-SLOWDOWN-401, 15 Oct 2026. Nothing but this file and the handover pointer changed.

## Answer

**#401 did not cause it, and nothing in the repo did.** Equatle and Log Laws Solve (the only two lines in
`Content verifiers 30`) run fast on a runner in Azure region **centralus** and about 1.5x slower in every other
region. The run for #401 happened to land in eastus, and the next two runs in westus and westus2, so three slow
runs in a row looked like a step. Run 38640496977 landed in centralus and both lines were back to 49 s and 33 s.
This is the contract's "runner change outside the repo" STOP IF: **no fix is needed.** One change to the
persistence report is worth considering (last section).

## 1. What was measured

The recorded times in `scripts/ci-timings.json` (history of the last 5 main runs, read from every commit of that
file, 64 runs) and, for the 17 main runs from 38555231031 to 38640496977, each run's `Content verifiers 30` job log
(Azure region, runner agent and image versions, the two lines' own `(NNs; ...)` times).

| Run | Commit | Region | Agent / image | Equatle | Log Laws Solve |
|---|---|---|---|---|---|
| 38627468056 | #400 (before #401) | centralus | 20261002 / 20261004 | 47 | 33 |
| 38629139453 | **#401** | **eastus** | 20261012 / 20261012 | 76 | 60 |
| 38631269829 | #402 | westus | 20261002 / 20261004 | 76 | 60 |
| 38635401918 | #403 | westus2 | 20261002 / 20261004 | 76 | 60 |
| 38638149544 | #404 | eastus2 | 20261012 / 20261012 | 75 | 58 |
| 38640496977 | #405 | **centralus** | 20261012 / 20261012 | 49 | 33 |

All 17 runs, split by region:

| Region | Runs | Equatle | Log Laws Solve |
|---|---|---|---|
| centralus | 6 | 46, 47, 49, 50, 56, 64 | 32, 33, 33, 35, 39, 46 |
| any other (eastus, eastus2, westus, westus2, westus3, southcentralus) | 10 | 69, 73, 75, 75, 76, 76, 76, 76, 76, 79 | 52, 53, 55, 58, 60, 60, 60, 60, 60, 64 |

The two groups do not overlap (centralus at most 64 s, elsewhere at least 69 s; Log Laws 46 against 52). Equatle
and Log Laws Solve rise and fall together (correlation 0.68 over the 64 recorded runs, their difference between
-3 and 21 s). Nothing else in the job differs: the same container image
(`mcr.microsoft.com/playwright/python:v1.63.0-noble`), the same pinned packages, the same two lines.

The "76 and 60 three times running" in the first live persistence report was three runs on three non-centralus
runners, not a stuck value. The same pair appeared earlier the same day (76 and 60 in run 38555231031, eastus;
79 and 64 in 38560892125, southcentralus), before #401 existed: 19% of the 59 runs before #401 had Equatle at 70 s
or more.

## 2. Why #401 is cleared

* **The diff reaches neither line.** #401 changed `.gitignore`, `CLAUDE.md`, two handover docs, a new
  `scripts/bg.py` and `scripts/end-task.py` (`git show --stat fa7ccd1`). No verifier, workflow, game or shared
  module changed. `verify-equatle.py` and `verify-log-laws.py` import neither `bg.py` nor `end-task.py` (the one
  match in `verify-log-laws.py` is a docstring quoting CLAUDE.md).
* **Neither new script runs in the job.** `bg.py` and `end-task.py` are a launcher and a worktree-removal tool for
  local sessions. CI calls them only through their own self-test lines, which run in other groups.
* **The same commit is fast or slow with the region.** Group 30 on #405's tree (which contains #401) was 49 s and
  33 s in centralus. That is, with #401 in, the lines are as fast as before it.
* **No local reproduction was needed.** The two trees are byte-identical for every file these lines read, so a
  local before and after comparison could only measure the laptop. I did not run one.

## 3. Equation Builder part 1

The same mechanism, with more noise. It lives in `Content verifiers 19` with other lines, and the group lands on a
different runner in each run, so the regions differ from group 30's in the same run.

| Region | Runs | Equation Builder part 1 |
|---|---|---|
| centralus, southcentralus | 3 | 98, 78, 97 |
| eastus, eastus2, westus | 9 | 152 to 159 |
| northcentralus, westus3, westcentralus | 4 | 106, 135, 136, 138 |

(16 runs, 38555231031 to 38640496977.) The "80 s or 150 s" alternation is the same fast-region and slow-region
split; the intermediate regions give the intermediate values. This is one fast and one slow hardware class, with
centralus and southcentralus in the fast class for this load. I have not shown it is CPU class rather than
something else about the region (disk, network, noisy neighbours); the logs do not say. Chromium start-up and
SymPy are CPU-bound, which fits.

## 4. What this means for the gate

* The 75% warning and the 80% pack check are unaffected: the slow figure (76 s) is the real cost on most
  runners, and the median of 5 already tracks it. The pack for group 30 is fine at either speed.
* The **persistence report** (last 3 runs each more than 20% and 15 s above the earlier median) cannot tell a
  region switch from a code regression. Three runs on non-centralus runners after a spell of centralus ones
  reports a line that has not changed, as it did here. It is a warning only, so this one cost a diagnosis, not a
  red build.

## 5. Proposed fix (not made; the contract forbids touching the workflow and the gate)

Have the persistence report require that the verifier rose **alone**. A real regression moves one verifier; a
region class moves everything CPU-bound at once. In the recorded history Equatle's time correlates 0.5 to 0.7 with
Log Laws Solve, Truth Buster, Prisoner's Dilemma, Bearing Blitz, Matrix Crunch and others, which is the runner's
signature. The report would then compare the flagged line's rise with the median rise of the other lines timed in
the same runs, and warn only on the excess. That needs no new data.

The exact fix would record each job's region next to its times, but the region is in the runner provisioner log,
not an environment variable, and I have not checked that the job can read it, so I do not propose it.

Either change touches `timing-gate.py` or `check-site.yml`, which this contract excludes, so it is Jon's call.

## 6. Not shown

* Which hardware centralus has. GitHub does not publish the CPU class per region, and the logs do not print it.
* Whether a future centralus slowdown would have to be detected differently. The persistence report would see it
  as a regression, which is right.
