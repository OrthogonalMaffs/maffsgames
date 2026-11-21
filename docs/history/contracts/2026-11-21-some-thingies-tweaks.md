# Contract SOME-THINGIES-TWEAKS (Project Claude; Jon ruled, 21 Nov 2026), verbatim

SOME-THINGIES-TWEAKS. Home lane. From Project Claude; Jon ruled, 21 Nov 2026, 17:40-18:07, after play-testing Pro Stage 3 on a big screen.
Recommended: Claude Code, Opus, medium effort. One game's drawing, stage 3 flow and run length; verifier extended.

TASK: In games/some-thingies/ only: (1) draw stage 3 arrays as thingies, not dots, in Jon's chosen style (bigger, a colour per column, a gap after every 5th row and column); (2) add a stage 3 scaffold that fades over the first 10 questions; (3) add "winner stays on": every run has AT LEAST 10 questions, then carries on until the first wrong answer or until the student presses End, so scores go above 10.

ROOT CAUSE: (1) drawArray() (index.html:747-752) draws plain 13 px dots, all one colour (.arr i, :92-93). Jon, on a big screen: "I'm struggling to see what times table that is"; an 8 rows of 6 array has to be counted one by one, which tests counting, not multiplication. And the game's theme is thingies: "when we have dots, they're not dots, they're thingies". (2) Nothing helps a child read the array as rows and columns. (3) A run is fixed at PER = 10 (:301, run() :774, finish at qi >= qs.length :802), so the boards fill with 10s and 10 questions is too little practice.

CLASS CHECK: Local. Each change is to this game's own drawing, stage 3 flow and run length. No shared asset changes. Other games' run lengths are untouched.

EXACT CHANGE:
1. First commit: the standing close-out for #865 (merge commit a579740, merge-pr.py, its main runs: check-site 44930388215, phone-fit-full 44930388209 green, with some-thingies PASS in normal, aa and laptop modes and nothing below the fold at any size (dispatching on the branch first wasn't possible: it merged before the run, and the branch was deleted), pages), per AGENTS.md.
2. Stage 3 picture (Jon chose option C from Project Claude's mock-up):
   - Each cell is the game's THINGY (index.html:734), not a dot, sized about 22 px on a laptop and as large as fits on a phone.
   - Each column gets its own colour from one fixed set of 10 distinct colours, the same set and order every time (column 1 always the first colour). Text never relies on colour alone.
   - A gap of about 0.7 of a thingy's width after the 5th and 10th column and after the 5th row, so 6 reads as 5 and 1, and 10 as 5 and 5. Rows are spaced slightly more than now.
   - The turn after marking stays (columns become rows), and the colours follow their thingies.
   - It fits 360 px at 10 across (the 5 rows of 10 array) and at 10 rows (10 rows of 5); verify both.
3. Stage 3 scaffold, fading over each run (only the total ever scores; the steps never cost a mark):
   - Questions 1-4: three steps. "How many rows?" (3 options: rows and two neighbours), then "How many in each row?" (3 options), then the total (4 options, as now). Each answered step labels the array: "R rows" down the side, "C in each row" along the top, whether the step was right or wrong (on a wrong step, show the right number).
   - Questions 5-7: the rows label is shown from the start; the student answers "How many in each row?", then the total.
   - Question 8 onwards (including every question after 10): the total only.
   - The step options are generated in the page from rows and cols (not added to the bank), with dataset.val marking.
4. Winner stays on (every mode and stage, both looks):
   - A run is AT LEAST 10 questions. In questions 1-10, a wrong answer works as now (feedback, MaffsNext) and the run goes on.
   - After question 10, the run carries on with more questions until the first wrong answer. That wrong answer shows its feedback and worked maths as normal, then "See results →" ends the run.
   - From question 11, an End button (in the HUD, next to the question counter) ends the run at once, with no penalty. Questions 1-10 have no End button; the existing back links stay.
   - Supply: draw from the stage's items with no repeat until all are used, then reshuffle, never repeating the item just answered. (Stage 1 main has 22 items, so long runs repeat; that's fine.)
   - Score = questions answered right in the whole run. The HUD shows "Q n" (no "/10" after question 10) and the score. Results show the score and "n answered". game_completed sends the real questions_answered and questions_correct. submitScore at the run's end, once (MaffsLock.finishOnce, as now), with the real score.
   - The Stage 2 adding item still scores only when both parts are right; after question 10, a wrong part ends the run.
   - Leaderboard keys unchanged.
5. LINES: add placeholders for "winner stays on" in both looks, at most 6 words each in the kid look: on reaching question 11 (e.g. "Keep going! One slip ends it."), and on the end-of-run screen after an overtime wrong. Same comment as the existing placeholders, for Jon to rewrite.
6. scripts/verify-some-thingies.py: extend it. Stage 3 draws thingies, not dots; 10 column colours in a fixed order; the gaps after the 5th column and row; fits 360 px at 5 × 10 and 10 × 5. The scaffold: questions 1-4 ask three steps, 5-7 two, 8+ one; the steps never change the score. Winner stays on: a run of 10 right answers then one wrong ends at 11 answered with score 10; a wrong answer at question 3 does not end the run; End at question 12 ends it with the score so far; no End button before question 11; no immediate repeats. New plants: a run that ends at the first wrong before question 10; an End button visible at question 5; a step answer that changes the score; a dot drawn instead of a thingy. Each must be caught.
7. Update the roster row's note ("at least 10 questions, then winner stays on"), and the todo row SOME-THINGIES-LIST: add "Jon checks the new stage 3 picture, the scaffold and winner stays on".
8. Merge on green via scripts/merge-pr.py, then the standing close-out.

DO NOT TOUCH: The bank (its 369 items and hash), tools/some-thingies/bank.py, stages 1, 2 and 4's pictures and questions, the looks and the #kids fragment rules, analytics event names and fields other than the real counts, shared assets, other games, CI budgets.

SUCCESS CONDITION: phone-fit (some-thingies) still passes in all three modes on the merge commit. Stage 3 shows coloured thingies in option C's layout and fits 360 px at 10 across and 10 down. The scaffold fades 3 → 2 → 1 steps over questions 1-4, 5-7, 8+, and never changes a score. Every run is at least 10 questions, continues until the first wrong after 10 or End, scores above 10 are submitted once, and the verifier passes with all old and new plants caught. #865's close-out is on main. CI is green and the PR is merged.

STOP IF: The 5 × 10 or 10 × 5 array can't fit 360 px with the thingies readable (report the size you reached). Any change outside games/some-thingies/, its verifier, the roster note and the todo row is needed. The bank's hash changes. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).
