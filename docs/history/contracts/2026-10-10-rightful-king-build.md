CONTRACT: RIGHTFUL-KING-BUILD (Project Claude for Jon, 10 Oct 2026, 10:35). CLOUD LANE (it
drafted the room; one task, one lane). Save verbatim under docs/handover/contracts/.

WAITS ON: the home lane's ART-PENDING and KEYPAD-VARIABLE, both merged to main. Do not start
until both are on main; check docs/handover/home.md.

======================================================================
TASK (RIGHTFUL-KING-BUILD): Build The Rightful King from the approved
draft (docs/escape-room-drafts/rightful-king-draft.md, merged #247),
replacing the withdrawn it-vengeance room, and leave it ready for Jon
to play-test behind a holding page. Do not release it.

ROOT CAUSE: it-vengeance was withdrawn on 8 Sep 2026. Jon approved the
draft in full on 10 Oct ("spot on"): every "For Jon" recommendation and
every [X] stands, with the rulings below.

CLASS CHECK: Not a bug: a content build under the existing room process.
The engine and checker are shared and are NOT changed here (the two
shared fixes it needs, ART-PENDING and KEYPAD-VARIABLE, are the home
lane's and land first).

JON'S RULINGS (10 Oct):
1. Slug `rightful-king`. Title "The Rightful King". ★★★ Challenge
   (record in the handover; no star field, the difficulty contract owns
   it).
2. Lock 1 (passcode): use the keypad's `maxDigits` mode (KEYPAD-
   VARIABLE). Library: k = 6, 7, 8, 9 with L = 3, plus k = 5, L = 3 (60,
   miss 125), which maxDigits makes settable. Variant 0 = k 7, L 3 → 210
   (miss 343), as the draft set it.
3. Lock 2 (overwrite): whole-number rates 5% to 40% (draft's ten-set
   library), with the rule "(1 − f) × 100 is not a multiple of r".
   Teacher page states that a calculator is needed (repeated × works on
   a basic one).
4. Lock 3 (audit): the draft's story rules (leader 30–60%, 20–60% saw
   the page, a gap of at least twenty points, four distinct clue figures,
   S ≠ 100). Variant 0 = 120, 50, 40, 60.
5. All three old locks leave the room; their bank entries and libraries
   stay as history.
6. The old URL /escape-rooms/it-vengeance/ redirects to
   /escape-rooms/rightful-king/ (a minimal noindex page with a meta
   refresh and a plain link), so no old share breaks.

EXACT CHANGE:
1. New folder escape-rooms/rightful-king/ with room.js (every slot from
   the draft; entities except object/lock name and where), index.html as
   a holding page (noindex), play.html as the unlinked preview with
   analytics off, teacher.html (noindex, unlinked). No `art` field (art
   pending; ART-PENDING makes that load cleanly).
2. New bank batch file with the three new locks; their libraries in
   scripts/gen-escape-variants.py per the rulings; re-run the generator.
   Never hand-edit a variants: block.
3. it-vengeance/index.html becomes the redirect in ruling 6;
   it-vengeance/room.js and teacher.html are left in place unserved
   (history), or removed if the checker requires one folder per room —
   say which.
4. check-escape-rooms.py and check-lock-bank.py pass; report the VALID
   count (the draft measured 183 of 280; the extra passcode set may
   change it).
5. Play it through headless: all objects and all three lock briefs on
   screen, the four wrong lines in order, each misconception's own
   response, all three locks opening, the win, and a time-out ending on
   the stakes.
6. PR; merge on green. Handover: built, behind its holding page, Jon can
   play-test at /escape-rooms/rightful-king/play.html; art pending (Jon
   generates the three pictures after his play-test).

DO NOT TOUCH: engine.js, teacher.js, engine.css, the checkers' rules;
every other room; the hub, front page and sitemap; docs/art/; prom-
budget (nothing here may contradict it).

SUCCESS CONDITION: both checkers pass with VALID ≥ 20 and variant 0
VALID; the room plays end to end on play.html; the old URL redirects;
nothing public lists the room; handover current.

STOP IF: ART-PENDING or KEYPAD-VARIABLE is not on main; any lock has
other than exactly one settable answer; VALID falls below 20; anything
needs an engine change.
