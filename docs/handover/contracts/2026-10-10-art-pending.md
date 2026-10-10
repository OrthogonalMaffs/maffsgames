CONTRACT: ART-PENDING (Project Claude for Jon, 10 Oct 2026, 08:50). HOME LANE (engine.js is
home-lane only). Do it before anything else in the home queue except a red main: cloud PR
#242 (Car Trap build) is waiting on it. Save verbatim under docs/handover/contracts/.

======================================================================
TASK (ART-PENDING): Stop the escape-room engine requesting a room's
scene, fail and win pictures when the room has none yet, so a room built
before its art loads with no 404.

ROOT CAUSE: engine.js always requests docs/art/<art>-scene/-fail/-win.webp
and relies on the 404 to drop the frame (or swap in data-fallback). The
page therefore makes a request it knows will fail. Since check-site's
Tier 1 fails any page that logs a 404, a room built before its art
cannot go green. Found on #242 (car-trap, art pending by design: the
house rule is art after the room is settled).

CLASS CHECK: Yes, a class. The fault is in shared code (engine.js), and
it hits every room built before its art: Car Trap now, The Rightful
King and the Library next, every future room after. The engine already
has the right rule for instruments — a lock with no `art` field emits no
<img> and makes no request (canon §11.3). Extend that same rule to the
room's three pictures. Do NOT relax check-site's 404 rule or allowlist
the missing pictures: that bends the test around the fault.

EXACT CHANGE:
1. escape-rooms/assets/engine.js: if window.ROOM has no `art` field
   (absent or empty), emit no <img> for the scene, the fail screen or
   the win screen and make no request for them; their frames are left
   out, exactly as a lock with no `art` is handled. A room WITH `art`
   behaves exactly as now, data-fallback included.
2. escape-rooms/assets/teacher.js: the same rule for any picture the
   teacher page shows.
3. scripts/check-escape-rooms.py: a room with no `art` field is
   reported as "art pending" (as it already lists pending pictures), not
   failed. A room that HAS `art` but whose files are missing still
   fails, as now.
4. A browser test: load one room with `art` removed (a fixture copy,
   not a live room) and assert no request is made to docs/art/ for its
   scene, fail or win, the start, time-out and win screens render
   without an empty frame, and check-site logs no 404. Plant: restore
   the old always-request behaviour; the test must fail.
5. Handover: record the rule ("no art field, no request") in CLAUDE.md
   and voice-rewrite §6, and tell the cloud lane #242 can drop `art`
   from car-trap's room.js and re-run.

DO NOT TOUCH: check-site.py's 404 rule and checker-allowlist.json (for
this); every live room's room.js; data-fallback behaviour for rooms
that have art; the collision rules; engine save state (no SAVE_V bump —
this changes no saved field).

SUCCESS CONDITION: the fixture room makes no docs/art/ request and
logs no 404; every live room renders its three pictures exactly as
before (check against all eight); check-escape-rooms passes and lists
pending-art rooms; the plant fails the test; merged on a green Gate;
#242 can go green with `art` omitted.

STOP IF: any live room relies on the 404 path to show a data-fallback
picture (list it — then "no art field" must not be confused with
"art file missing"); the change needs a SAVE_V bump; teacher.js shares
the picture code with engine.js in a way that makes the two changes
inseparable from other behaviour.
