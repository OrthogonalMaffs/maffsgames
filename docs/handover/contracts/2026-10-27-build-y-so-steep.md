TASK: Build "Y So Steep?" (slug y-so-steep): the equation of a straight line, in Foundation and Higher modes, with staged practice, typed answers, a generator module the game imports, and a verifier. Unlisted.

ROOT CAUSE: Straight-line graphs carry 28 of 1,800 OCR Foundation marks over 18 papers, and GCSE A9/A10 (equation of a line, gradients and intercepts) have no game. Coordinate Geometry Dash's GCSE level has 24 mixed multiple-choice items, few on equations. Jon (7 Oct) chose a new game; (27 Oct) it becomes the 6 P's source for straight lines.

CLASS CHECK: Not a bug. Bank-first (canon §8.2.1): the generator lives in its own module that the game imports and the 6 P's will later import; never copied. Built on existing shared patterns only: MaffsKeypad/MaffsAnswer for typed answers, step marking as Simultaneous Solver does it (any valid step scores, the neatest shown as feedback), pictures drawn from the item's data, the shared answer lock, level resolver and MaffsNext, theme.css.

EXACT CHANGE:
1. Modes: Foundation (Stages 1–2) and Higher (Stages 1–6). Each stage carries its mode on every analytics event (existing events only).
   S1 Read it (Foundation): y = mx + c in varied orders (y = 3 − 2x, y = 5x, y = −4, y = x + 7); type m and c in two boxes. Integers.
   S2 Spot it (Foundation): a line on a labelled grid through lattice points; type m and c. A wrong answer draws the rise/run triangle and marks the intercept.
   S3 Rearrange it (Higher): 2y = 4x + 6, 3x + y = 7, 2x + 3y = 12; type m and c (fractions allowed).
   S4 Two points (Higher): steps: gradient (rise over run), then c (substituting either point scores), then the equation.
   S5 Point and gradient (Higher): the given point is not the y-intercept in at least 75% of items; steps as S4.
   S6 Parallel and perpendicular (Higher).
   Answers are always m and c in two typed boxes; feedback writes y = mx + c in full. Named wrong answers: run over rise; wrong sign on a falling line; the x-intercept read as c; c from a wrong substitution; perpendicular gradient not negated or not reciprocated. No timer.
2. Generator module (new file): at least 45 items per stage; at least 40% negative gradients; S2 lines pass through at least two lattice points in view; Higher gradients include fractions with denominators 2–5; no repeats within a stage.
3. Game page games/y-so-steep/ (new folder): theme.css as it is (lowest tier GCSE, dark row); KaTeX; matching by value; the phone-fit rules in canon §7.6 at 320 × 568, 375 × 667, 390 × 844 with the keypad open, and at 1366 × 768 / 1280 × 720; grid labels and any figure text at least 12 px. Unlisted.
4. Fraction entry: if MaffsAnswer can't accept a/b exactly, that is a shared-asset change: write it (MaffsAnswer.fraction(), a "/" key on MaffsKeypad's fraction variant, test-answer-js.py cases) on its own branch, do NOT merge it, report it, and ship S1, S2, S4–S6 items with integer gradients meanwhile, with S3 and fractional items enabled once that branch merges. Never a game-local parser.
5. Verifier (new file, declares its CI line): recompute every m, c and step exactly (Fraction); check every drawn line from its data; check the bank rules; play one item of every stage in Chromium at 390 px. Plants, each caught: a wrong c; a line drawn off its data; a positive-only bank.
6. Merge once CI and main are green; docs/handover/build.md; report with screenshots (one per stage, 375 × 667) for Jon. Then start the next queued contract.

DO NOT TOUCH: Coordinate Geometry Dash. Other games. Shared files (lane rules), except the minimum a site-wide check demands for a new game folder, marked unlisted and reported, and item 4's separate unmerged branch. The 6 P's (it imports the generator later, in its own contract).

SUCCESS CONDITION: Every stage plays start to finish on the keypad at all phone sizes and on a laptop; the verifier passes and catches its plants; named-error feedback appears for each listed error; unlisted; merged; main green; screenshots reported.

STOP IF (each with its default; record in "Decided for you"):
- A stage can't fit a phone with its keypad without scrolling between question and answer: park that stage with screenshots, ship the others, report.
- A stage falls short of 45 items: widen ranges within the tier, list what was widened; if still short, ship it and report the count.
- Fraction entry needs more than item 4: leave fractional items off, ship the rest, report.
