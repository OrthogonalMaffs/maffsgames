CONTRACT: LIBRARY-JAM-BUILD (Project Claude for Jon, 10 Oct 2026, 10:35). CLOUD LANE (it
drafted the room; one task, one lane). After RIGHTFUL-KING-BUILD. Save verbatim under
docs/handover/contracts/.

WAITS ON: the home lane's ART-PENDING and KEYPAD-VARIABLE, both merged to main, and #248
(the draft) merged.

======================================================================
TASK (LIBRARY-JAM-BUILD): Build The Library Jam from the approved draft
(docs/escape-room-drafts/library-draft.md, #248) and leave it ready for
Jon to play-test behind a holding page. Do not release it.

ROOT CAUSE: a new ★ Warm-up room for the priority audience (grade 1–3).
Jon approved the draft in full on 10 Oct ("spot on"): every "For Jon"
recommendation and every [X] stands, with the rulings below.

CLASS CHECK: Not a bug: a content build under the existing room process.
The shared keypad fix it needs (KEYPAD-VARIABLE) is the home lane's and
lands first. No shared code changes here.

JON'S RULINGS (10 Oct):
1. Title "The Library Jam", slug `library-jam`. ★ Warm-up, grades 1–3;
   levelLabel "GCSE" (Kiln and Comic precedent). Record ★ in the
   handover; no star field (the difficulty contract owns it).
2. Lock C (fines): the keypad's `maxDigits` mode, maxDigits 4, so £54
   is typed as 54 and the misconception 5400 is settable and gets its own
   response. Fines in multiples of 5p. No calculator: grade 1–2 arithmetic
   (Kiln standard); the teacher page says so.
3. Lock A (drop order): dial 1 to 8; a drop order already sorted either
   way is rejected; the answer may be the last book on the trolley, never
   slot 1. Variant 0 as the draft (five books, answer 3rd, misconception
   slot 1st).
4. Lock B (deflector): five-degree spread (eight variants).
5. Bibby never overturns anything: the system cancels the fines once the
   books reach the cleared bin, as drafted.

EXACT CHANGE:
1. New folder escape-rooms/library-jam/ with room.js (every slot from
   the draft; Jon's "Pride and Prejudice" line verbatim as wrong line 3;
   entities except object/lock name and where), index.html as a holding
   page (noindex), play.html as the unlinked preview with analytics off,
   teacher.html (noindex, unlinked). No `art` field (art pending).
2. New bank batch file with the three locks; libraries in
   scripts/gen-escape-variants.py per the rulings (lock C uses the
   maxDigits settable rule KEYPAD-VARIABLE adds to the generator); re-run
   the generator. Never hand-edit a variants: block.
3. check-escape-rooms.py and check-lock-bank.py pass; report the VALID
   count (draft measured 572 of 640).
4. Play it through headless, as for every room: objects, all three lock
   briefs, the wrong lines in order, each misconception's own response
   (including 5400 on lock C), all locks opening, the win, the time-out.
5. PR; merge on green. Handover: built, behind its holding page, Jon can
   play-test at /escape-rooms/library-jam/play.html; art pending.

DO NOT TOUCH: engine.js, teacher.js, engine.css, the checkers' rules;
every other room; the hub, front page and sitemap; docs/art/.

SUCCESS CONDITION: both checkers pass with VALID ≥ 20 and variant 0
VALID; typing 54 on lock C opens it and 5400 triggers the named
misconception; the room plays end to end on play.html; nothing public
lists the room; handover current.

STOP IF: KEYPAD-VARIABLE or ART-PENDING is not on main; any lock needs a
grade above 3; any lock has other than exactly one settable answer;
VALID falls below 20; anything needs an engine change.
