# SEQ-SOLVER-FIXES (received 3 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER). Order (Jon, 3 Nov): this first, then SEQ-SOLVER-WORKED,
then DASHBOARD-METRICS. STOP IF 2 is hit: see the cloud handover's entry of 3 Nov, "Contracts stored".

## Contract (verbatim)

CONTRACT: SEQ-SOLVER-FIXES
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Apply Jon's three rulings on Sequence Solver: move the five out-of-spec geometric items from GCSE to A-level, make the
clock follow the Hidden Count-Up policy, and relabel the GCSE level "GCSE Higher".

ROOT CAUSE
SEQ-SOLVER-REREAD (#647): five GCSE geometric items use negative ratios or ratios from non-adjacent terms, beyond DfE
A24 (simple geometric progressions, r a rational number > 0); the game shows a running Time and folds it into the
score (BASE/T_K), although .claude/rules/timer-policy.md lists it under Hidden Count-Up (timer silent, no multiplier,
time on the results screen only); the GCSE bank is Higher-weighted, so a lecturer choosing "GCSE" for a grade 1-3
class gets Higher content. Jon's rulings, 3 Nov 2026.

CLASS CHECK
(1) and (3) are local to this game. (2) is an instance of a known class (games out of step with timer-policy.md,
e.g. trig-identity-duel-t2-010): fix this game to the policy as other Hidden Count-Up games do; do not change the
policy or other games. The score change makes old and new scores incomparable: use the repo's established route for
a new leaderboard key (canon's standing rule: separate keys for anything not comparable; every key nameable by
levelLabel()).

EXACT CHANGE
1. games/sequence-solver/index.html: move the five geometric items named in the findings register from QUESTIONS.gcse
   to QUESTIONS.alevel, unchanged; update the verifier's COUNTS (gcse 45, alevel 59) and the roster row's counts.
2. Clock: remove the visible Time from the HUD; the per-question timer runs silently; the score no longer uses time
   (score as the other Hidden Count-Up games score); total time appears on the results screen only. New leaderboard
   key per the established route, with levelLabel() naming it; score history follows.
3. Level label: the GCSE button and its start-screen description read "GCSE Higher"; the level key stays gcse (no
   URL or analytics change). Portal card and Essentials card text, if they name the levels, match.
4. Findings register: close the entries this fixes with this PR's number.

DO NOT TOUCH
Question wording; the KS3 and A-level banks except receiving the five items; marking; timer-policy.md; other games;
Gate files.

SUCCESS CONDITION
GCSE 45 and A-level 59 questions; no visible clock and no time in the score, time on the results screen; new
leaderboard key named by levelLabel(); "GCSE Higher" shown; verify-sequence-solver.py extended (no Time in the HUD,
score independent of time; plants caught); Gate green; Shared review by Project Claude; stop for Jon's "merge";
Record line.

STOP IF
The repo has no established route for a new leaderboard key; another Hidden Count-Up game scores in a way that
conflicts with the policy text (report both); "GCSE Higher" needs a change to the shared level system.
