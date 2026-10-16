CONTRACT: BSB-ROOM-BUILD (Project Claude for Jon, 16 Oct 2026, 18:35).
CLOUD LANE. Phase 2 of Big School Begins. Fresh session. Save verbatim
under docs/handover/contracts/ in the claim commit.

START CONDITION: met. #422 (the draft) merged as c484459; main green
(run 38910693628). DND-ROOM-RELEASE (home lane, tonight) is a release,
not a build, so this is the one new build in flight (SR-30).

TASK: Build "Big School Begins" from the approved draft
(docs/escape-room-drafts/big-school-begins-draft.md, #422) with Jon's
rulings below, and leave it ready for Jon's play-test behind a holding
page. Do not release it.

ROOT CAUSE: A new ★-level room for Year 6 and new Year 7 (Jon, 16 Oct
2026). The phase 1 draft is approved with the rulings below. Jon's
rulings supersede every item in the draft's "For Jon" section, and his
voice lines (ruling 11) replace the drafted dialogue they name.

CLASS CHECK: Not a bug: a content build under the existing room process
(docs/escape-room-voice-rewrite.md §2 steps 6-7; canon §11). The engine,
checkers and generator are shared and not changed in logic: only new
lock entries, a variant library and the room's own files are added. The
four-lock count and 20-minute timer are room data the engine already
reads (minutes, R.locks.length). The "Starter" label (rating.js, the hub
chip, the checks) and canon's record of this room's exceptions are a
separate home-lane contract, not this one.

JON'S RULINGS ON THE DRAFT (16 Oct 2026):
1. Title "Big School Begins", slug big-school-begins. minutes: 20,
   penalty: 45, four locks: named exceptions for this room.
2. Label: "Starter" on student surfaces (SR-11), applied by the
   home-lane label contract. This build adds no label or star field.
   The derived rating stays ★ Warm-up (every lock grade 1).
3. Theme: same register and palette as every other room. No
   room-specific styling.
4. Bibby is never quoted: she hands over a written card, as drafted.
5. The clock is the hunt's end at the lunch bell; the ending is the win
   as drafted, with ruling 11's William line added. Both [X] marks are
   ruled and removed.
6. The stakes slot (start screen and time-out) is replaced with, word
   for word: "The lunch bell goes with boxes still blank on the card.
   The canteen is heaving, and you end up squeezed onto the end of a
   table of older students, eating in silence. Across the room, William
   is laughing with the group who found him first. Daisy catches your
   eye: 'September, then. You'll get another go.'"
7. Lock C: lesson lengths are 45, 50 or 55 minutes only (no 60). Keep
   the draft's sets 0, 1, 4, 5 and 6. Replace sets 2, 3, 7, 8 and 9
   with new sets meeting every draft constraint: start from 10:00 to
   11:30 in fives, crossing exactly one hour, all ten answers distinct.
   Variant 0 stays 10:35 + 55 -> 1130.
8. William's name: as draft item 17. No line plays on it; none of the
   listed words appear anywhere in the room.
9. Release copy (hub, front page, canon) is NOT changed here. The
   release contract will use "three or four locks, 15 to 20 minutes".
10. Everything else stands as drafted, including the draft's own
    recommendations: eight objects, six clues and two blanks (item 6);
    every lock grade 1 and level 'year6' (item 9); lock B's dial
    sweep: 360, wedge: true, max 360 (item 10); no lock gating (item
    11); the map giving "up" before "along" (item 14); "left on the
    card", "five pounds" in words (item 15); lock D's clue_numbers
    returning every price in pence as well as its printed form (item
    16); the teacher page saying no calculator is needed (item 18);
    lock A marking a point where grid lines cross (item 19).
11. VOICE (Jon's lines, word for word; entities as for every slot):
    a. Hook: Daisy's quoted line ("Everyone gets lost," ... "The
       canteen is one room.") is replaced with: "I'm so glad I'm
       looking after you guys, I'm missing French AND English."
       The rest of the hook stands.
    b. wrongLines: keep the four drafted heads; the bodies become, in
       order:
       1. "One time I got so lost I ended up in the staff room."
       2. "There was the time I accidentally sneezed my pencil at a
          teacher."
       3. "Did you know there's a school cat? His name's Mr
          Furrypants."
       4. "Come on guys, you can do this." (the last line repeats)
    c. missSays (missTitle, hints and solve stay as drafted):
       A: "Ugh, I did that! Along the corridor first, then up the
          stairs."
       B: "Other way! Clockwise, like the hands on a clock. I always
          forget too."
       C: "Hang on, that's not a real time! There's sixty minutes in
          an hour, not a hundred."
       D: "I did exactly that in maths last year. You can't just take
          the small number off the big one."
       Numbers stay in words; no numeral is typed.
    d. Win: before Daisy's "Same table in September?", William says:
       "My big brother said I'd definitely get my head flushed down the
       toilet, but you guys are really nice." The rest of the win
       stands.
    e. SR-14 exception (Jon, 16 Oct 2026): William's line in (d) is
       kept by Jon's ruling. It names the myth a new student fears in
       order to show it is untrue. Record the exception and its date in
       room.js's header and the handover; canon records it via the
       home-lane label contract.

EXACT CHANGE:
0. In the claim commit, record #422's result in docs/handover/cloud.md:
   merged as c484459, main green, run 38910693628. No separate PR.
1. escape-rooms/big-school-begins/room.js: every slot from the draft
   with rulings 1-11 applied: title, hook, brief, stakes, win,
   wrongLines, the eight objects (ids as the draft's table), and the
   four locks (instruments, ids, keys, grades, labels, maxDigits,
   verbs, missTitle, missSays, hints, solve, onOpen). Entities in
   every slot except object and lock name/where (canon §11.3). No
   art field (art pending: Project Claude writes the prompts after
   this build). The header records the four-lock and 20-minute
   exceptions, the SR-14 exception, and Jon's date.
2. index.html as a noindex holding page; play.html as the unlinked
   preview with analytics off, named in check-analytics-loader.py's
   WITHDRAWN registry (data only, as Roll for Initiative's was). The
   home lane's DND-ROOM-RELEASE removes Roll for Initiative's entry
   from the same registry tonight: if main has moved, rebase and keep
   both changes. teacher.html noindex and unlinked, in the existing
   room format.
3. Lock bank: the four locks' entries in the next free
   docs/lock-bank-batch<N>.txt. escape_set_checks.LOCKS: four solvers
   and clue_numbers as the draft's pot sections state, with ruling 7's
   lock C sets and item 16's pence check for lock D.
4. scripts/gen-escape-variants.py: add the four libraries (variant 0
   first in each), then re-run the generator so variants.json and
   room.js's variants: block are written by it. Never hand-edit a
   variants: block. Report the joint-draw VALID count (the draft
   measured 5,710 of 8,000 before ruling 7; the count will move) and
   that variant 0 is VALID.
5. SR-30: check-escape-rooms.py (the rooms' verifier) passes on the
   room in this PR's CI. Create docs/audits/findings/big-school-begins.yml
   (no open findings). Add the room to any shared check's MIGRATED list
   that covers escape rooms; if none applies, say so in the PR.
6. Run check-escape-rooms.py, check-lock-bank.py,
   check-content-safety.py, check-student-labels.py and
   test-escape-rating.py. If check-content-safety flags William's line,
   add one dated allowlist entry for that line only, citing ruling 11e
   (data only; never change the checker). Play the room in Chromium to
   a win and a time-out at 390 and 1280 px, over draws covering every
   set of every lock, with no sideways scroll; attach both end screens
   to the PR. Confirm on screen: lock B's dial needle points the way
   the turn goes, and lock D never shows its answer on the tray.
7. python scripts/check-changed.py before the first push. One PR;
   merge on a green Gate with main green (standing authorisation);
   watch main's run.
8. Handover entry in docs/handover/cloud.md: built and held; the
   preview URL /escape-rooms/big-school-begins/play.html; ★ Warm-up
   derived (grades 1/1/1/1) with "Starter" pending the home-lane label
   contract; the SR-14 exception for canon; the VALID count; art
   pending; "Awaiting Jon's play-test before release".

DO NOT TOUCH: escape-rooms/assets/ (engine.js, rating.js, teacher.js,
engine.css); checker and generator logic; every other room and its
variants (re-running the generator must leave every other room's
variants: block byte-identical); the hub, front page and sitemap;
docs/art/; canon; CLAUDE.md; docs/todo.md; any game.

SUCCESS CONDITION: The room plays to a win and a time-out at both sizes
with all four locks solvable on every variant. Every line in ruling 11
appears word for word in its slot. Every check passes, and
variants.json and every other room's block are unchanged except for the
new room. The room is reachable only at its preview URL, noindex and
unlisted. The findings file exists. #422's result is recorded. Full CI
is green; the PR is merged with the handover entry. Release (label, hub
card, front page, sitemap, copy, noindex off) is a separate instruction.

STOP IF:
- Main's latest full run is red.
- Any check, the engine or the teacher page assumes three locks or
  fifteen minutes (report it; do not change shared code).
- The generator cannot produce ten valid lock C sets under ruling 7, or
  the joint draw falls below 20 VALID, or variant 0 is INVALID.
- Re-running the generator changes any other room's variants.
- Any of Jon's lines would need rewording to fit a slot or pass a check
  other than ruling 11e's allowlist entry (report it; do not reword).
- Any line plays on William's name, or any student-facing text names a
  year group, key stage, primary or secondary (SR-11).
- You would schedule any task that merges, pushes or edits.

END OF CONTRACT
