CONTRACT: ESCAPE-DIFFICULTY (Project Claude for Jon, 10 Oct 2026, 13:05). HOME LANE, straight after
CAR-TRAP-RELEASE (both touch the hub; doing it after means Car Trap joins the scheme in this
PR). Save verbatim under docs/handover/contracts/.

======================================================================
TASK (ESCAPE-DIFFICULTY): Show a 1–3 star difficulty rating on every
escape room — hub card, front-page card, start screen and teacher page —
derived from the room's hardest lock, enforced in CI, replacing the
"KS3 / GCSE" style level labels.

ROOT CAUSE: rooms carry only a loose level label, so a class can walk
into a room that frustrates it. Evidence: Rugby Mud's analytics show a
lock dialled 37 times with 1 correct, a stuck group on a Higher-tier
lock in a room labelled "GCSE". Jon ruled the scheme on 9 Oct 2026; the
contract was owed and never written (Project Claude's miss).

CLASS CHECK: Yes, a class: every room's label, on four surfaces, set by
hand. Fix it once: the rating is DERIVED from per-lock grades in room.js
(one source of truth), computed by shared code, and checked in CI so no
surface can disagree. Do not type stars into each page by hand without
a check.

JON'S SCHEME (9 Oct 2026):
- ★ Warm-up — grades 1–3. ★★ Core — grades 4–5. ★★★ Challenge — grades
  6–9. A room's rating = its HARDEST lock.
- "Suits a top set" appears on ★★★ teacher pages ONLY, never on a card
  or a student-facing screen.
- Jon's room ratings, which the derivation must reproduce: ★ Comic
  Caper, Kiln Disaster; ★★ Canteen Hack, Heatwave Mutiny, P.E. Shed
  Rebellion, Prom Budget, Hamster Heist (Jon ruled ★★ for its
  lower-bound lock), Car Trap; ★★★ Rugby Mud.
  (In build, not yet live: The Rightful King ★★★, The Library Jam ★.)

EXACT CHANGE:
1. room.js, every live room: each lock gets `grade: N` (GCSE grade 1–9,
   the grade at which the lock's skill is typically secure; use the
   lock bank's LEVEL/TOPIC and the AQA/Edexcel grade descriptors). List
   every lock's grade and a one-line reason in the PR description.
2. escape-rooms/assets/engine.js and teacher.js: one shared function,
   rating(room) = band(max lock grade) → {stars: 1|2|3, name:
   'Warm-up'|'Core'|'Challenge', grades: '1–3'|'4–5'|'6–9'}. The start
   screen shows the stars, name and grade range; the teacher page shows
   the same plus "Suits a top set" for ★★★ only.
3. Hub cards (escape-rooms/index.html) and front-page cards (index.html):
   replace the level label with the stars and name (e.g. "★★ Core ·
   grades 4–5"). These are static HTML, so each card carries
   data-stars; check-escape-rooms.py derives each room's rating from
   room.js and FAILS if any card, on either page, disagrees, or if any
   lock lacks a grade.
4. Remove `level`/`levelLabel` from display wherever the stars replace
   them; keep the fields in room.js only if analytics or the checker use
   them (say which).
5. Accessibility: the stars have a text equivalent ("Difficulty: 2 of
   3, Core, grades 4–5"); colour is not the only signal.
6. Canon §11: the scheme, the derivation, and the CI rule. Handover
   updated, including the ratings The Rightful King and The Library Jam
   must reproduce when they release (the cloud lane's builds add lock
   grades).

DO NOT TOUCH: any lock's maths, variants or instrument; the wrong lines
and prose; the art; analytics fields (no new data collected); rooms in
build (rightful-king, library-jam — the cloud lane's).

SUCCESS CONDITION: every live room shows the same rating on hub card,
front-page card, start screen and teacher page; the derived ratings
match Jon's list exactly; "Suits a top set" appears only on Rugby Mud's
teacher page; the checker fails a planted mismatch (a card saying ★ for
Rugby Mud) and a planted missing grade; main green after merge.

STOP IF: grading the locks honestly gives any room a rating different
from Jon's list (report the lock and its grade; do not fudge a grade to
fit); a surface cannot show stars without breaking the 320 px phone
check; analytics depend on levelLabel in a way that would change
collected data.
