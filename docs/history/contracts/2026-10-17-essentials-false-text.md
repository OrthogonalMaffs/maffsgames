CONTRACT: ESSENTIALS-FALSE-TEXT (Project Claude for Jon, 17 Oct 2026, 13:35).
CLOUD LANE. Fresh session. Save verbatim under docs/handover/contracts/
in the first claim commit.

TASK: Fix four Essentials games whose screens state or show something
false, one game per PR in this order: like-terms-collector,
factor-race, new-shapes, shape-shifter.

ROOT CAUSE (each confirmed in the code on main, 17 Oct):
1. like-terms-collector (:269-270; findings r-001, r-002, t3-003): a
   question labels U+1FAA3 BUCKET as "plums" and U+1F95D KIWIFRUIT as
   "limes". The keys are right; the pictures are wrong.
2. factor-race (:137 against :182; t3-001): the start screen says "You
   have 5 seconds per question"; TIME_PER_Q is 30000 (30 seconds).
3. new-shapes (:329; t3-007): "You now know five area formulae and one
   volume formula." The finding records four area formulae taught
   (rectangle, triangle, parallelogram, trapezium).
4. shape-shifter (:672, :725, :885; t3-001): after a wrong answer the
   correct shape is drawn in navy #1a2744 on the #0a0c12 canvas, and
   the feedback says "correct shape shown in navy". It is effectively
   invisible.

CLASS CHECK: Partly. (1) is a class within the game: every emoji and
label pair in the bank is checked, not just the two reported. (2)-(4)
are local text or colour faults in one game each, each the canon rule
that a screen states what the code does. No shared code changes.

EXACT CHANGE (one PR per game, claimed per the listed-game lane rule
in docs/handover/cloud.md: add to the remaining list in its own
handover commit; skip a game in an open home-lane batch and note it):
1. like-terms-collector: every label matches its emoji. Replace 🪣 with
   a fruit emoji whose standard name matches a label (e.g. 🍐 "pears"
   or 🍇 "grapes"), and relabel "limes" to "kiwis" (keep 🥝). Check
   every emoji and label pair in the bank against its Unicode name and
   list them in the PR; fix any other mismatch the same way. Keys
   unchanged. Close r-001, r-002 and t3-003.
2. factor-race: the start screen states the real time: "You have 30
   seconds per question" (keep "don't overthink it!"). The timer is
   unchanged. Close t3-001.
3. new-shapes: count the area formulae the game teaches; the line
   states that number in words. Close t3-007.
4. shape-shifter: the correct shape after a wrong answer is drawn in
   the game's own --green (#22c55e) at the same stroke width, and the
   feedback says "correct shape shown in green". Check contrast of at
   least 3:1 against #0a0c12 (WCAG 1.4.11) and state the ratio. Close
   t3-001.
5. Reworded items move content ids in data/check-ledger.json: update it
   as CI's Tier 4 layer A directs; never hand-edit ids.
6. Per PR: python scripts/check-changed.py before opening the PR; merge
   on a green Gate with main green (standing authorisation); watch
   main's run; take the game off the remaining list in the PR that
   fixes it.
7. Handover entry in docs/handover/cloud.md per game.

DO NOT TOUCH: any other finding in these games (each stays open);
answer keys; timers, scoring or leaderboard logic; shared code
(schools/assets/), shared scripts/, the workflow, canon, CLAUDE.md,
docs/todo.md; any other game.

SUCCESS CONDITION: Each game's screen matches its code: every
like-terms label names its picture; factor-race states 30 seconds;
new-shapes states the counted number; shape-shifter's correct shape is
visible and the feedback names its colour. Six findings closed, citing
their PRs. Four PRs merged; main green after each; handover recorded.

STOP IF:
- Main's latest full run is red.
- A game is in an open home-lane batch branch (skip it, note it, carry
  on with the next).
- A fix would change an answer key, a timer or a leaderboard key.
- new-shapes' count of area formulae is not four (report what it
  teaches; do not reword until checked).
- --green fails 3:1 against the canvas (report; do not pick another
  colour unasked).
- You would schedule any task that merges, pushes or edits.

END OF CONTRACT
