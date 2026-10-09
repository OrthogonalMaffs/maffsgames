HOME LANE, TONIGHT (Project Claude for Jon, 9 Oct 2026, 16:10). The full queue, in order.
Items 1, 2, 4, 5 are in claude/home-queue-2026-10-09.md (Jon attaches it). Item 6 is in
claude/home-contract-sci-calc-2026-10-09.md (Jon attaches it). Items 3 and 7 are below.
Save each contract verbatim under docs/handover/contracts/ as it starts. The standing rule
applies. Checkpoint after item 7.

FIRST, before any item: main is red after #211 (CI group E at 9m04s of 9m). Jon has
approved the cloud lane adding a group E2 in scripts/ci-groups.py as a one-off. Wait
for that PR to merge and for main to go green before merging anything. Item 3 then
replaces hand-assigned groups altogether.

QUEUE:
1. RULINGS-9OCT (home-queue-2026-10-09.md, item 1)
2. GRAPH-SKETCHER-FIT (item 2)
3. CI-BALANCE (below)
4. PLAY-AGAIN-SCREEN (item 3 in that file)
5. SCORES-OFFLINE (item 4 in that file)
6. SCI-CALC (home-contract-sci-calc-2026-10-09.md)
7. DOCS-9OCT (below)
CHECKPOINT.

======================================================================
ITEM 3

TASK (home lane, CI-BALANCE): Assign content verifiers to CI groups
automatically from their measured run times, so no group drifts over
its budget and turns main red again.

ROOT CAUSE: Each verifier names its group by hand in its ci-line
header. Groups fill and drift as verifiers are added and pages grow.
On 9 Oct group E reached 9m04s of 9m and turned main red after #211,
though no verifier in E had changed (Screening Room alone drifted from
89 s to 105 s). B4 is at 5m17s of 6m. The fix so far has been to add
a group by hand (B5, E2), which only buys time. ci-groups.py already
records each line's seconds on a main full run
(scripts/ci-timings.json, --record-timings).

CLASS CHECK: A bug class: the same failure in more than one group,
caused by shared CI infrastructure (manual bin-packing). Fix it in
ci-groups.py, not by moving headers or adding groups by hand. Canon
§7.8.1's limits stay: no content job past its timeout, each failing at
75%.

EXACT CHANGE:
1. ci-groups.py builds the content groups from ci-timings.json: pack
   the lines into as many groups as needed so each group's measured
   total is at most 70% of its timeout (headroom for drift and slow
   runners). A line with no recorded time gets a conservative default
   and is flagged until it has one. Keep the pack stable: a line moves
   group only when it must, so the GitHub job names don't churn.
2. Headers: a ci-line keeps its label and args. The group field
   becomes optional (a hint, or a tier such as content or answer-lock
   where the tiers genuinely differ). Keep backwards compatibility
   while the headers migrate, then remove the old field.
3. A check that fails CI (on PRs, not only on main) when any group's
   measured total passes 80% of its timeout, naming the group and its
   largest lines. Timings refresh from each main full run, via the
   existing --record-timings, wired to run automatically on main.
4. Remove E2 and B5-style manual splits once the packer covers them.
5. Canon §7.8.1/§7.8.2: record the rule (groups are packed from
   measured times; 70% target, 80% fails).
6. Handover updated, with the before and after group totals.

DO NOT TOUCH: any verifier's checks or args; the site-wide jobs (tiers
1-2, site-wide checks, tier 4, shared assets), which stay listed in
the workflow; the 4-minute and 75% limits in canon.

SUCCESS CONDITION: every content group's measured total is at most 70%
of its timeout on the next main full run; the 80% check fails on a
plant (one inflated timing) and passes on main; main green; merged on
a green Gate.

STOP IF: the workflow can't take a variable number of content groups
without a change GitHub's matrix doesn't support (describe it); the
total CI time would rise by more than 20% (report the figures).

RULING (Jon, 9 Oct 2026, 17:59): the 70% and 80% are of each group's
BUDGET (75% of its timeout), not of the job timeout. The build on
claude/ci-balance stands as built.

======================================================================
ITEM 7

TASK (home lane, DOCS-9OCT): Record today's rulings and the lane-rule
changes in canon and the docs, and relist Factor Theorem.

ROOT CAUSE: Several rulings and process changes from 8-9 Oct live only
in handovers and contracts. Factor Theorem's fix merged (#207), and its
open findings are MEDIUM only (t5-016, t5-017: the test bank, coming
later), so it meets SR-21. Jon ruled it A-Level only (9 Oct): canon
says a level that serves another level's items is not listed as that
level.

CLASS CHECK: Docs and bookkeeping, plus the SR-21 relist process. No
code.

EXACT CHANGE:
1. Relist factor-theorem under SR-21 (verifier in CI, no open CRITICAL
   or HIGH: confirm both on main). Roster row back at #88, Levels:
   A-Level only (L4 removed). Portal filter, sitemap, spec map (remove
   any L4 mapping), leaderboard hub (A-Level board only). Updates
   page: no entry unless canon §3.4 is met by Practice leaving the
   leaderboard (it isn't: that's scoring, not what students learn).
2. Canon §0.2: record the freeze exception, Simultaneous Solver Stage
   5 only (Jon, 9 Oct; merged #203).
3. Canon §7.8: lane rules from 8-9 Oct. The cloud lane fixes listed
   games by claim; contracts are kept verbatim in
   docs/handover/contracts/; a finished cloud session is closed, not
   left idle (an idle 6 Oct session woke on a GitHub event and re-sent
   its old report on 9 Oct); a one-off exception lets the cloud lane
   edit ci-groups.py (E2, 9 Oct).
4. timer-policy.md: Unit Converter moves to "No timer" (score on
   correct answers only, Jon 8 Oct), if the cloud lane couldn't edit
   it.
5. Rulings recorded in canon where behaviour rules live: Skip shows
   the answer and waits on Next; one log row per answer for multi-part
   items (Screening Room t4-017); display-only number formatting with
   marking on stored values (Unit Converter); "≈" for rounded
   conversion factors.
6. Handover updated.

DO NOT TOUCH: game pages; findings files other than factor-theorem's
relist rows.

SUCCESS CONDITION: Factor Theorem on the portal as A-Level only; canon
and docs carry each item; the roster, coverage, meta and lock checks
pass; merged on a green Gate; main green.

STOP IF: factor-theorem has an open CRITICAL or HIGH by then;
timer-policy.md is already updated (skip that part).
