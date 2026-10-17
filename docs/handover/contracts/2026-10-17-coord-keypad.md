CONTRACT: COORD-KEYPAD (Project Claude for Jon, 17 Oct 2026, 19:30). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Make Big School Begins' lock A show its answer as coordinates,
(x, y), on screen, through a display-only keypad option, and make the
lock's text teach the notation rather than drop it. Do not release the
room.

ROOT CAUSE: Lock A (big-school-begins/room.js :158-161, :229-232) asks
for the library's coordinates but takes them as a two-digit "code":
the keypad shows "37", the label says "COORDINATES AS A CODE", and hint
3 says "no brackets and no comma". Writing coordinates as (x, y) is the
skill the lock teaches, so the screen teaches the wrong habit (Jon's
play-test, 17 Oct 2026). engine.js wireKeypad (~:598-606) prints the
typed digits as they are; no keypad can show a format.

CLASS CHECK: Shared code: the keypad belongs to the engine every room
uses. The fix is an optional display format on the keypad that any
room can use; a keypad without it is unchanged. Only lock A uses it
today: every other keypad enters a plain number, and Jon ruled (17 Oct)
that lock C's 24-hour time stays without a colon.

EXACT CHANGE:
1. engine.js, keypad: an optional instrument field format:
   'coordinates', valid only with digits: 2. The display shows
   "( – , – )" when empty, then "( 3 , – )", then "( 3 , 7 )". Typed
   value, stored value, Set and checking are unchanged (still the two
   digits). The typed fallback's label becomes "Or type the
   coordinates", and its input accepts "(3, 7)", "3,7" or "37" (the
   existing non-digit stripping already does this; raise maxlength so
   the brackets and comma fit). Without format, output is byte-identical
   to today.
2. teacher.js: where a lock's answer or misconception is shown, a
   format: 'coordinates' lock shows it as (x, y).
3. big-school-begins/room.js, lock A only:
   - instrument: digits: 2 (fixed: both coordinates are required)
     replaces maxDigits: 2; format: 'coordinates'; label
     "LIBRARY: COORDINATES".
   - brief: "...WRITE ITS COORDINATES." (drop "AS A CODE" and anything
     after it that describes a code).
   - hint 3: "Write the coordinates as (across, up)."
   - solve: "...so its coordinates are ({{map.x}}, {{map.y}}): across
     first, then up." (drop "The code is ...").
   - missSays, missTitle, hints 1-2, onOpen unchanged.
   If escape_set_checks.LOCKS or the generator records lock A's
   instrument, update it to match and re-run the generator; every other
   room's variants block stays byte-identical, and lock A's sets and
   VALID count must not change.
4. test-escape-keypad.py: a coordinates case (empty, one digit, two
   digits, the typed fallback "(3, 7)", a wrong answer still marked
   wrong, the misconception y-then-x still getting Daisy's line).
5. Canon §11.3: document format: 'coordinates' in one line.
6. Show every other room unchanged: before-and-after DOM snapshots of
   every room's start screen, lock screens and teacher page in
   Chromium, identical except Big School Begins' lock A and teacher
   page.
7. python scripts/check-changed.py before opening the PR. Merge on
   green with main green; watch main's run; remove the worktree with
   scripts/end-task.py.
8. Handover in docs/handover/home.md: done; Big School Begins still
   waits on its art and the release contract.

DO NOT TOUCH: lock C (Jon: 24-hour time needs no colon), locks B and D;
every other room; the dial and slider instruments; rating.js; the hub,
front page and sitemap (the room stays unlisted); the cloud lane's
handover.

SUCCESS CONDITION: Lock A shows ( – , – ) and fills to ( x , y ) as the
student types; a correct answer opens the lock; y-then-x still gets
Daisy's misconception line; the teacher page shows (x, y). No text in
lock A calls the answer a code. Every other room's snapshots are
identical. Checks, test-escape-keypad and CI green; merged; worktree
removed; handover recorded.

STOP IF: Main's latest full run is red. Any other room's output changes
by a byte. Switching lock A to digits: 2 changes its sets, its VALID
count or variant 0. The typed fallback can't accept "(3, 7)" without
changing how other keypads read input.

END OF CONTRACT
