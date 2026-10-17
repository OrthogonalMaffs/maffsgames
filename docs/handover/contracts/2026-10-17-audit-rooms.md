CONTRACT: AUDIT-ROOMS (Project Claude for Jon, 17 Oct 2026, 13:35). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Bring escape rooms into the findings register, so every live and
held room has a findings file that audit-register.py --check accepts.

ROOT CAUSE: scripts/audit-register.py (:138) rejects a findings file
whose slug has no games/<slug>/ folder. Rooms live under
escape-rooms/<slug>/, so no room can have a findings file: none of the
13 has one. SR-30 (canon §0.3) requires every new build, rooms
included, to have one; #425 (Big School Begins) could not comply.

CLASS CHECK: Yes, a class: the register's notion of "a thing that can
have findings" is games only, so every room is outside it, not just
the new one. The fix is in the shared checker (accept
escape-rooms/<slug>/ as a valid home) plus a findings file for every
room. Patching one room would leave twelve outside.

EXACT CHANGE:
1. audit-register.py: a findings file is valid if its slug has
   games/<slug>/ OR escape-rooms/<slug>/ (a room folder with room.js).
   Its error message names both. --selftest gains a room case and a
   planted file with neither folder (must fail).
2. REGISTER.md generation: rooms appear in their own section ("Escape
   rooms"), not in the games tables. The "Audit progress" counts for
   games (point 1, verifiers, etc.) are unchanged; rooms are not
   counted as games.
3. A findings file for each of the 13 rooms (the 12 live rooms and
   big-school-begins), in the existing schema, findings: []. Exclude
   it-vengeance (withdrawn; a redirect, no room content) and say so in
   the PR. If the schema's `audited` field needs an audit reference
   rooms do not have, set it the way the schema allows for "not yet
   audited", and state the value used and why in the PR.
4. Canon: SR-30's row (§0.3) gains "(rooms: docs/audits/findings/
   <slug>.yml, accepted by audit-register.py since AUDIT-ROOMS)". The
   §11 room table needs no change.
5. python scripts/check-changed.py before opening the PR. Merge on
   green with main green; watch main's run; check the regenerated
   REGISTER.md shows the rooms section.
6. Handover entry in docs/handover/home.md, including: "Big School
   Begins' release is now unblocked on the register side; the Starter
   label contract is still outstanding."

DO NOT TOUCH: any room's files; any game; the findings of any game; the
games' Audit progress counts or their logic; check-escape-rooms.py;
the cloud lane's handover.

SUCCESS CONDITION: audit-register.py --check passes with 13 room
findings files; --selftest passes, including the room case and the
planted bad file; REGISTER.md lists the rooms in their own section with
the games' counts unchanged; canon SR-30 updated; CI green; merged;
handover recorded.

STOP IF: Main's latest full run is red. Accepting rooms would change
any game count or any existing check's result. The schema cannot
represent a room without inventing a new field (report it; do not add
one). A room folder other than it-vengeance has no room.js.

END OF CONTRACT
