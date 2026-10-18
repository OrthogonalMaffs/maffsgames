CONTRACT: STARTER-FIRST (Project Claude for Jon, 18 Oct 2026, 16:20). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: List a Starter room before every starred room, wherever rooms are
listed easiest to hardest, and make the checks enforce that order.

ROOT CAUSE: The hub ("Ordered easiest to hardest") and the front-page
band order rooms by their derived rating, and check-escape-rooms.py
enforces that order. A labelled room keeps its derived rating for
ordering (#430), so Big School Begins (every lock grade 1, derived
★ Warm-up) sits at the end of the ★ band, after The Library Jam. Its
content is KS2, easier than any ★ room's grade 1-3 GCSE content (Jon,
18 Oct 2026).

CLASS CHECK: Shared: the order rule lives in check-escape-rooms.py
(and any order logic in test-escape-rating.py) and decides every
room's place on both pages. The fix is in the rule: a room labelled
Starter sorts before every starred room. Unlabelled rooms keep their
current order exactly.

EXACT CHANGE:
1. check-escape-rooms.py: in the easiest-first order check, a room with
   label 'Starter' ranks below ★ (sorts first). Any other future label
   is not given a rank here; if one appears, the check fails and says
   it needs a ruling. Add a planted fault: a Starter card placed after
   a ★ card must fail.
2. test-escape-rating.py: if it asserts order, the same rule.
3. Move Big School Begins' card to first place on the hub and in the
   front-page band. No other card moves.
4. Canon §11.3 (the label paragraph from #430): one sentence: "A Starter
   room is listed before every starred room."
5. python scripts/check-changed.py before opening the PR. Merge on
   green with main green; watch main's run; check the live hub shows
   Big School Begins first. Remove the worktree with
   scripts/end-task.py.
6. Handover entry in docs/handover/home.md.

DO NOT TOUCH: rating.js, engine.js, teacher.js (display is unchanged);
any room's room.js; the stars key line; every other card's position and
wording; the cloud lane's handover.

SUCCESS CONDITION: Big School Begins is the first card on the hub and
in the front-page band; every other card is in the same order as
before (show the before and after order). The planted fault fails and
the real run passes. Canon records the rule. CI green; merged; live
hub checked; worktree removed; handover recorded.

STOP IF: Main's latest full run is red. Any unlabelled room's position
would change. The order rule is implemented somewhere other than the
two scripts named (report where; do not change shared runtime code).

END OF CONTRACT
