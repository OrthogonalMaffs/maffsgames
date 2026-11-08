TASK: Build Who Ate All the Pies?, the pie-chart game, on the existing pie-charts bank (#567), unlisted.

ROOT CAUSE: No game covers pie charts (24 OCR Foundation marks). The bank is merged; under the bank-first rule (canon §8.2.1) the game imports the bank's generator and never copies its questions. Spec: Project Claude's pie-chart spec, summarised below.

CLASS CHECK: Local: a new game. One shared need is a class issue and is NOT solved here: the stage-5 board label is missing from the shared map, the same gap as stage 6 of Y So Steep? and The HC Factor. Ship stage 5 without a leaderboard; the shared label fix is queued for the home lane.

EXACT CHANGE:
1. games/<slug>/ using the bank's slug (suggested who-ate-all-the-pies). Five stages, each its own board/analytics mode, played one at a time: a stepped worked example, then 10 questions easiest first, then "Next: Stage N+1" (the Take a Walk pattern).
   1 Read it: the fraction of the whole a slice is. 2 Find the amount: angle ÷ 360 × total. 3 Draw it: the student types each angle from a frequency table, and the chart builds itself from their angles, so a wrong angle visibly fails to close the circle; the stage's results screen says in one line that drawing with a protractor is practised on paper. 4 Can you tell?: "Yes, it's …" or "You can't tell", with the reason. 5 Work backwards: one slice's angle and frequency given, find the total.
2. "You can't tell" appears as a genuine option in stages 2 and 5 where the bank provides such items; do not write new ones.
3. Charts in SVG. Labels at least 12 px. Slices told apart by label as well as colour, never colour alone.
4. Setting: a football ground's pie stall on matchday (default; Jon may change it). Plain wording; jokes are Jon's.
5. Marking by value through MaffsAnswer; the bank's named slips as feedback. Calculator per the bank's calc field (by stage if it varies).
6. Theme from the roster levels (lowest tier served decides).
7. Phone fit with the keypad open at 320×568, 360×640, 375×667, 390×844. Verifier through a separate code path, with planted faults.

DO NOT TOUCH: The bank's questions and answers. Shared files, the lists (games.json, sitemap, homepage, Essentials). Any other game.

SUCCESS CONDITION: Merged once CI is green, unlisted, main green. build.md records the state, a "Decided for you" list, and one screenshot per stage at 375×667 in your scratchpad.

STOP IF: A bank answer is wrong: leave that question out of the game, report it with the correct answer, and carry on (don't edit the bank). The bank lacks items a stage needs (e.g. no "can't tell" items for stage 4): build the stages it supports, show "Coming soon" on the rest, report the gap. A stage can't fit at 320×568: park it on the known-failures list and report.
