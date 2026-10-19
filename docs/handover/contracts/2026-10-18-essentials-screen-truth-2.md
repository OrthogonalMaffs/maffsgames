CONTRACT: ESSENTIALS-SCREEN-TRUTH-2 (Project Claude for Jon, 18 Oct 2026, 22:35).
CLOUD LANE. Fresh session. Save verbatim under docs/handover/contracts/
in the first claim commit.

FIRST, in the claim commit's handover entry: record #437's main run
(39157734021, green), and the local setup step "put the unpacked esprima
on PYTHONPATH before check-changed.py", so local runs here don't trip
on it again.

TASK: Fix four Essentials games whose screens show a student something
untrue or unreadable, one game per PR, in this order: formula-plug-in,
new-shapes, four-quadrant-explorer, shape-shifter.

ROOT CAUSE (each confirmed on main, 18 Oct):
1. formula-plug-in (t3-005, open): the header score slot (:192,
   scoreNum/scoreTotal) shows questions done (currentIndex), not
   correct answers, so a student with 2 right out of 5 sees "5/5".
2. new-shapes (t3-008, open, bundled): the header score slot shows
   questions done, the same fault (:751, :967). The same entry also
   holds two unrelated points: no units on any answer, and
   game_completed/personal_best_set lacking mode.
3. four-quadrant-explorer (r-001, open): drawGrid prints "(0,0)" at
   toCanvasX(0) - 6, toCanvasY(0) + 6 (:411). On phone widths it
   covers the -1 tick labels on both axes, so a Year 6 student cannot
   read -1 in a coordinates game.
4. shape-shifter (t3-003, open): REFLECTION_QUESTIONS[14] (:292) is the
   square (-4,-1), (-2,-1), (-2,1), (-4,1), which is its own reflection
   in the x-axis, so tapping the original's corners scores correct.

CLASS CHECK: (1) and (2) are the same fault in two games: each fixed in
its own game, and each game's verifier gains a check that the score
slot equals correct answers. (3) is local to one drawing. (4) is a
class within the game: any reflection item whose image equals the
original. The fix replaces this item and makes the verifier fail on
any such item in the bank. No shared code changes.

EXACT CHANGE (one PR per game, claimed per the listed-game lane rule):
1. formula-plug-in: the score slot shows correct answers over questions
   answered so far. Verifier: after a planted wrong answer, the slot
   shows one fewer correct than answered. Close t3-005.
2. new-shapes: split t3-008 into three entries (score slot; units;
   event mode), as SWEEP-1-RULINGS step 1 split bundles. Fix the score
   slot only, as in 1, with the same verifier check, and close that
   entry. The units and event-mode entries stay open.
3. four-quadrant-explorer: "(0,0)" no longer covers any tick label at
   320, 390 or 1280 px. Place it in the quadrant away from both -1
   labels, or drop it below a width where it cannot fit; every tick
   label from -N to N is readable. Screenshots at 320 and 390 px in the
   PR. Close r-001.
4. shape-shifter: REFLECTION_QUESTIONS[14] becomes the same 2 by 2
   square moved up clear of the axis: (-4,1), (-2,1), (-2,3), (-4,3).
   Its key is recomputed as its reflection in the x-axis. The verifier
   fails any reflection item whose image equals the original (as a set
   of vertices), in every mode. Close t3-003.
5. Reworded or changed items move content ids in data/check-ledger.json:
   update as CI's Tier 4 layer A directs; never hand-edit ids.
6. Per PR: python scripts/check-changed.py before opening the PR (CI
   judges the checks this container can't run, as recorded); look at
   the changed screen in Chromium at 390 px; merge on a green Gate with
   main green; watch main's run.
7. Handover entry per game in docs/handover/cloud.md.

DO NOT TOUCH: every other finding in these games, including
shape-shifter t3-002 (no 180° rotation is ever served; a design fix,
for Jon) and the two new-shapes entries split off in step 2; answer
keys other than step 4's item; scoring logic, leaderboard keys and
analytics events; shared code (schools/assets/), shared scripts/, the
workflow, canon, CLAUDE.md, docs/todo.md; any other game.

SUCCESS CONDITION: Both score slots show correct answers; four-quadrant
-explorer's -1 labels are readable at every width; no shape-shifter
reflection item is its own image, and the verifier enforces it. Four
findings closed (t3-005; the score-slot part of t3-008; r-001; t3-003),
two new open entries from the split. Four PRs merged; main green after
each; handover recorded, including #437's run and the esprima step.

STOP IF:
- Main's latest full run is red.
- A game is in an open home-lane batch branch (skip it, note it).
- The score slot feeds a leaderboard, personal best or analytics value
  that would change (report; do not change it).
- shape-shifter's replacement square overlaps another item in its mode
  or falls outside the grid (report; do not pick other coordinates).
- You would schedule any task that merges, pushes or edits.

END OF CONTRACT

---

Rulings, Jon, 19 Oct 2026 (verbatim; on the 18 Oct STOP at item 4 and the report after items 1-3).

(1) shape-shifter: option (a). "Overlaps" meant a duplicate item. Go as
written: rerun python scripts/check-changed.py, then PR, and merge on
green with main green.

(2) formula-plug-in and new-shapes: restore a progress count beside the
score. The header reads "Q{n} of {N} · {right} right" (n = the question
on screen, N = the session length). Display only. Each verifier checks
both numbers through right, wrong, right. One PR per game, after
shape-shifter. Close nothing new; note it in each game's handover entry
as a follow-up to t3-005 and t3-008.
STOP IF either game has no fixed session length: report how its
session ends, and wait.

(3) Before starting new-shapes, report whether #437 applied the reveal
line "You now know two new area formulae and the volume of a prism."
Do not apply it in this work either way.
