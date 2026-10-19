CONTRACT: PYTHAG-REPORT (Project Claude for Jon, 19 Oct 2026, 10:24). CLOUD LANE.
Save verbatim under docs/handover/contracts/ in the first commit.
RESEARCH ONLY. No code changes, no PR to main beyond the contract
and handover commits.

TASK: Report how Just Pythag It, Bruv handles the hypotenuse step,
scoring and its questions, and measure whether misconception feedback
computed from each question's sides is feasible, so Jon can rule on a
"Formula only" mode.

ROOT CAUSE: The game makes every student click the hypotenuse before
each calculation. Students who can already identify it have no way to
go straight to using the formula. A "Formula only" mode is wanted, with
feedback that names the common Pythagoras errors. The design depends on
facts not yet known: where the click happens, whether it scores, how
questions are stored and checked, and how often the wrong answers
collide.

CLASS CHECK: Not yet determinable; this contract finds out. Report
whether the game's stage/step flow and answer checking are its own
code or shared with other games (e.g. Matrix Crunch's stage
unlocking). If they are shared, the later build contract changes the
shared layer, not this game alone.

EXACT CHANGE:
1. Report where the hypotenuse click occurs: before every question,
   in which rounds, and whether a wrong click blocks the calculation.
2. Report scoring: whether the click earns points, what reaches the
   leaderboard and the on-device score history, and the session
   length.
3. Report how questions are stored or generated (fixed bank or
   generated; count per round), what each question gives and asks for
   (hypotenuse or a shorter side), and how answers are checked
   (rounding rule, tolerance).
4. Report whether any wrong-answer diagnosis exists now.
5. Feasibility measurement, in a scratch script not committed to the
   game: for every question, compute the correct answer and these
   candidate errors, rounded as the game rounds:
   finding hypotenuse c from a, b: sqrt(|b^2 - a^2|), a^2 + b^2,
   a + b, sqrt(2a + 2b);
   finding a shorter side from c, a: sqrt(c^2 + a^2), c^2 - a^2,
   c - a, sqrt(2c - 2a) where defined.
   Report the count of questions where any candidate equals the
   correct answer, or where two candidates are equal, within the
   game's tolerance; list up to ten examples. Put the script's output
   in the handover entry.
6. Report whether the start screen can take a mode choice and where
   other games keep theirs.
7. Handover entry in docs/handover/cloud.md with all of the above.

DO NOT TOUCH: the game's code, questions, scoring, leaderboard or
verifiers; any other game; canon.

SUCCESS CONDITION: Jon has answers to items 1-6, including the
collision count, in one report, and nothing in the game has changed.

STOP IF: Answering needs a code change or a deploy. The question bank
cannot be enumerated without running the game in a way the container
does not support: report what you could measure and wait. Main's
latest full run is red.

END OF CONTRACT
