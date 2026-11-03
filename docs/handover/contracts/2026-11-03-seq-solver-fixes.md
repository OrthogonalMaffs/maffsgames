# SEQ-SOLVER-FIXES (received 3 Nov 2026, 16:05, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER). Jon's hand-off ran three contracts strictly in order, each
starting only after the previous one merges: 1 SEQ-SOLVER-FIXES, 2 SEQ-SOLVER-WORKED
(`docs/handover/contracts/2026-11-03-seq-solver-worked.md`), 3 DASHBOARD-METRICS
(`docs/handover/contracts/2026-11-03-dashboard-metrics.md`). Each is Shared tier.

**Earlier wording (superseded):** #650 (main b18b064, 3 Nov) stored an earlier text of this contract from the archived
session. The text below is Jon's 16:05 hand-off, which replaces it; the earlier text stays in git history at b18b064.

In it STOP IF 2 was hit (most Hidden Count-Up games still time the score; new leaderboard key?); Jon's 16:05 text
rules option (a), the policy text, with the same leaderboard key, and asks for the drift table in the PR.

## Hand-off note (verbatim)

FRESH CLOUD SESSION — HANDOVER (Jon, 3 Nov 2026, 16:05)

Read docs/handover/cloud.md first. This replaces an older session that has been archived; it holds no work.

FIRST COMMIT of the first contract: close QUESTION-ID in the cloud handover ("MERGED #649; main green") and move its
contract to docs/history/contracts/.

THEN run these three contracts strictly in order, each starting only after the previous one merges. Each is Shared
tier: stop at a green Gate for Project Claude's review and Jon's "merge"; merge with
python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 and report its last line.
  1. SEQ-SOLVER-FIXES   2. SEQ-SOLVER-WORKED   3. DASHBOARD-METRICS

CONTEXT FROM THE PREVIOUS SESSION'S SURVEY (for SEQ-SOLVER-FIXES): of the other 38 games listed under Hidden Count-Up
in .claude/rules/timer-policy.md, 28 still put answer time into the score and 17 still show a clock, against the
policy text. Jon's ruling below covers Sequence Solver only; report the drift in the PR, change no other game.

## Contract (verbatim)

CONTRACT: SEQ-SOLVER-FIXES
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Apply Jon's three rulings on Sequence Solver: move the five out-of-spec geometric items from GCSE to A-level, make the
clock follow the Hidden Count-Up policy text, and relabel the GCSE level "GCSE Higher".

ROOT CAUSE
SEQ-SOLVER-REREAD (#647): five GCSE geometric items use negative ratios or ratios from non-adjacent terms, beyond DfE
A24 (simple geometric progressions, r a rational number > 0); the game shows a running Time and folds it into the
score (BASE/T_K), although timer-policy.md lists it under Hidden Count-Up ("timer runs silently, no score multiplier,
time shown on results screen only"); the GCSE bank is Higher-weighted, so a lecturer choosing "GCSE" for a grade 1-3
class gets Higher content. Jon's rulings, 3 Nov 2026.

CLASS CHECK
(1) and (3) are local to this game. (2) is one instance of a wider drift (28 of 38 other Hidden Count-Up games keep a
time multiplier, 17 show a clock): Jon has ruled this game only; the class goes to him separately. Leaderboard: per
Jon's October timer ruling, scores before and after a timer change need not compare, so no new leaderboard key.

EXACT CHANGE
1. games/sequence-solver/index.html: move the five geometric items named in the findings register from QUESTIONS.gcse
   to QUESTIONS.alevel, unchanged; update the verifier's COUNTS (gcse 45, alevel 59) and the roster row's counts.
2. Clock (Jon, 3 Nov: option (a), the policy text): remove the visible Time from the HUD; the per-question timer runs
   silently; the score no longer uses time at all; total time appears on the results screen only. Same leaderboard
   key and score history as now.
3. Level label: the GCSE button and its start-screen description read "GCSE Higher"; the level key stays gcse (no
   URL or analytics change). Portal card and Essentials card text, if they name the levels, match.
4. Findings register: close the entries this fixes with this PR's number. PR body: the 28/38 Hidden Count-Up drift
   (game, shows clock y/n, time in score y/n), for Jon.

DO NOT TOUCH
Question wording; the KS3 and A-level banks except receiving the five items; marking; leaderboard keys;
timer-policy.md; other games; Gate files.

SUCCESS CONDITION
GCSE 45 and A-level 59 questions; no visible clock and no time in the score, total time on the results screen;
"GCSE Higher" shown; verify-sequence-solver.py extended (no Time in the HUD, score independent of time; plants caught);
drift table in the PR; Gate green; Shared review by Project Claude; stop for Jon's "merge"; Record line.

STOP IF
"GCSE Higher" needs a change to the shared level system; removing time from the score needs a change to a shared
scoring asset.
