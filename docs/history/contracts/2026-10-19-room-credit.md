CONTRACT: ROOM-CREDIT (Project Claude for Jon, 19 Oct 2026, 10:12). CLOUD LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Credit Mrs Rogers on Big School Begins, with the line "Mrs Rogers'
idea, and she stars in it. Want something built? Let us know.", on every
page where the room is listed or presented.

ROOT CAUSE: Big School Begins was built from a teacher's idea (Mrs
Rogers, who is the room's named character and has agreed to be named),
but carries no credit. The request-built rooms (Comic Caper, Kiln
Disaster) carry "Built from a site user's request. Want something
built? Let us know." on the hub cards only. It is not yet known whether
that line comes from a room data field or is written into each card.

CLASS CHECK: A class. The same credit shape appears on two or more rooms
and is about to appear on a third. The fix is one optional credit field
in the room data, rendered by the shared room templates everywhere a
room is listed or presented. It is not a third hand-written line. If the
existing line is already a field, extend it; if it is hand-written, see
STOP IF.

EXACT CHANGE:
1. Find where the existing request-room line comes from (data field or
   markup) and report it in the PR.
2. If it is a field: set Big School Begins' credit to the text in TASK,
   with "Let us know" linking to /feedback/ exactly as the request rooms
   do. Make every template that presents a room (homepage rooms section,
   /escape-rooms/ hub, the room page, the teacher page) render the field
   when present. Comic Caper and Kiln Disaster therefore gain their
   existing line on their room and teacher pages; their wording is
   unchanged.
3. Verifier: for each credited room, each of the four page types shows
   its credit text exactly once; uncredited rooms show none; at 320, 390
   and 1280 px the credit does not overflow its card or container.
   Main's copy must fail the check for Big School Begins.
4. python scripts/check-changed.py before opening the PR; report
   container-caused failures as before, confirming main fails them
   identically. Merge on green with main green; watch main's run.
5. Handover entry in docs/handover/cloud.md.

DO NOT TOUCH: the request rooms' wording; room content, locks,
characters or teacher-page answers; the Starter label or hub order
(#430, #439); the game count or the "thirteen" room wording (a
separate contract); any game.

SUCCESS CONDITION: Big School Begins shows the credit, linked as the
request rooms are, on the homepage section, /escape-rooms/, its room
page and its teacher page. All credited rooms render from one field. The
verifier passes and main's copy fails it. CI green; merged; main green;
handover recorded.

STOP IF: The existing line is hand-written into cards rather than a
field: report every place it appears and the field shape you would
use, then wait. Any template would need restructuring beyond adding the
credit render. Main's latest full run is red. The credit cannot fit a
card at 320 px without truncating or wrapping the room title.

END OF CONTRACT

---

CONTRACT: ROOM-CREDIT v2 (Project Claude for Jon, 19 Oct 2026, 10:32).
CLOUD LANE. Replaces ROOM-CREDIT (10:12), which stopped correctly on
its first STOP IF. Save both verbatim under docs/handover/contracts/ in
the first commit.

TASK: Give escape rooms one optional credit, held in room data and
shown on the room page, teacher page, hub card and homepage card, and
use it for Big School Begins, Roll for Initiative, Comic Caper and Kiln
Disaster.

ROOT CAUSE: Room credits are typed by hand wherever they appear: the
request line on the hub (escape-rooms/index.html :79-80, :94-95) and
the homepage (index.html :813-814, :825-826), and a different line on
Roll for Initiative's teacher page (teacher.html :24). No room.js has
a credit, so every new credit is another hand-typed copy, and Big
School Begins has none.

CLASS CHECK: A class: the same credit shape is typed by hand on three
rooms across three page types. Fix: one optional `credit` field in
room.js, drawn by the shared code (engine.js, teacher.js). The hub and
homepage are static HTML that load no room data. Their card notes
remain markup, but scripts/check-escape-rooms.py holds each one to its
room's field, as it already does for stars and the Starter label. One
source; checked copies. Lane exception, ruled by Jon: the cloud lane
edits engine.js, teacher.js and check-escape-rooms.py for this
contract only.

EXACT CHANGE:
1. room.js, optional field `credit`: the room's own credit sentence(s)
   only. Values:
   Big School Begins: "Mrs Rogers' idea, and she stars in it."
   Roll for Initiative: "Built from a teacher's idea. Thank you,
     Mrs Rogers."
   Comic Caper and Kiln Disaster: "Built from a site user's request."
   Rooms without a credit carry no field.
2. The invitation is fixed shared text, not room data: "Want something
   built? Let us know.", with "Let us know" linking to /feedback/ as
   the existing notes do. It follows every credit wherever a credit is
   shown. It is defined once for engine.js and teacher.js, and once in
   check-escape-rooms.py as the expected card text.
3. engine.js: show credit + invitation on the room's start screen when
   `credit` is present. teacher.js: show it in the opening text when
   present. Remove the hand-written line at
   roll-for-initiative/teacher.html :24 and the matching comment in
   its room.js.
4. Hub and homepage: add card notes for Big School Begins and Roll for
   Initiative, in the existing markup (print-note on the hub, esc-note
   on the homepage), reading credit + invitation exactly. Comic Caper's
   and Kiln Disaster's notes are unchanged in wording.
5. check-escape-rooms.py: fail if a card note differs from its room's
   credit + invitation, if a card carries a note for a room with no
   credit, or if a credited room's card has no note. Main's copy must
   fail on Big School Begins and Roll for Initiative.
6. Browser verifier: for each credited room, the room start screen and
   the teacher page show credit + invitation exactly once, the link goes
   to /feedback/, and at 320, 390 and 1280 px the note does not
   overflow its container or push the title into truncation. Uncredited
   rooms show none.
7. python scripts/check-changed.py before opening the PR; report
   container-caused failures as before, with main failing them
   identically. Merge on green with main green; watch main's run.
8. Handover entries in docs/handover/cloud.md and docs/handover/home.md.
   The home.md entry names the three shared files edited under this
   exception, so the home lane rebases knowingly.

DO NOT TOUCH: room content, locks, characters, answers, hint ladders;
the Starter label, stars and hub order; the "thirteen" room wording
(separate contract); any game; any other check's rules.

SUCCESS CONDITION: All four credited rooms show credit + invitation,
the same wording on the room page, teacher page, hub card and homepage
card. Every credit comes from room.js, and the check fails any card
copy that disagrees. Both verifiers pass and main's copies fail. CI
green; merged before 17:00 today; main green; both handovers recorded.

STOP IF: Showing the credit needs engine.js or teacher.js restructured
beyond adding the credit display. The check cannot read a room's credit
without executing room.js in a way it does not already do for stars.
The PR cannot merge before 17:00 today (the home lane starts this
evening on shared files): report and hold, do not merge late. Main's
latest full run is red.

END OF CONTRACT

---

Jon's ruling, 19 Oct 2026 (asked during the build): the one shared invitation and the credit render live in
escape-rooms/assets/rating.js (MaffsEscapeRating.credit), the one file both the room page and the teacher page
already load. That is a fourth shared file beyond the exception's three, named in docs/handover/home.md.
