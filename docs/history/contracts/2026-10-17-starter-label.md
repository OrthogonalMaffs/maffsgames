CONTRACT: STARTER-LABEL (Project Claude for Jon, 17 Oct 2026, 16:55). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Let a room show an age-neutral label ("Starter") in place of its
stars on student surfaces, apply it to Big School Begins, and record the
room's exceptions in canon. Do not release the room.

ROOT CAUSE: Big School Begins (#425, held) is a Year 6/7 transition room.
Jon ruled (16 Oct) that it shows "Starter" (the SR-11 name for the
Year 6 level) on student surfaces, not stars. Every surface renders the
rating through rating.js html(r) (engine.js :205, teacher.js :57), and
check-escape-rooms.py check_ratings (:313) requires every card chip to
show stars, so no room can carry a label today.

CLASS CHECK: Yes, shared code: rating.js, engine.js, teacher.js and
check-escape-rooms.py are used by every room. The change is an optional
room-level field the shared code honours; a room without it behaves
exactly as now. Not a second rating scheme: rating() is unchanged, and
the derived rating still orders the hub and appears on the teacher page.

JON'S RULINGS (16 Oct 2026): the student-facing label is "Starter"
(SR-11); the teacher page says it is a transition room for Year 6 and
new Year 7 (teacher surface, outside SR-11); four locks, 20 minutes and
the SR-14 exception for William's line are named exceptions for this
room only.

EXACT CHANGE:
1. Room data: big-school-begins/room.js gains two top-level fields:
   label: 'Starter' and labelFor: 'Year 6 and new Year 7'. Nothing else
   in the room changes.
2. rating.js: html(r, room). When room.label is set, it returns the
   label chip instead of the stars:
   <span class="rating" data-label="starter"><span aria-hidden="true">
   Starter</span><span class="sr-only">Level: Starter</span></span>.
   Without room.label, output is byte-identical to today. rating() and
   BANDS unchanged. Update the file's header comment.
3. engine.js ratingLabel(): passes R (M.html(r, R)). The start screen
   shows "Starter", never stars, for a labelled room.
4. teacher.js ratingLabel(): for a labelled room shows the label, then
   "for <labelFor>", then the derived stars chip as today
   (e.g. "Starter, for Year 6 and new Year 7 · ★ Warm-up · grades 1–3").
   Unlabelled rooms unchanged, including "Suits a top set".
5. check-escape-rooms.py: read a room's label from room.js. For a
   labelled room, its card chip must be the label chip (data-label and
   both texts exact) and must not carry data-stars; for an unlabelled
   room, unchanged. Order checks still use the derived rating. Add a
   planted fault that runs every time: a label chip on an unlabelled
   room's card, and a star chip on a labelled room's card (both must
   fail).
6. test-escape-rating.py: a labelled-room case (start screen shows
   Starter and no ★; teacher page shows Starter, labelFor and the
   stars).
7. Canon §11: the room-rules line ("15 minutes, three locks...") notes
   Big School Begins' exceptions (four locks, 20 minutes; Jon, 16 Oct
   2026); §11.3 documents label/labelFor (student surfaces show the
   label; the teacher page shows both; the order still uses the derived
   rating). SR-14's row records the one exception: Big School Begins,
   William's win line, kept by Jon on 16 Oct 2026 because it names a
   new student's fear in order to show it untrue.
8. python scripts/check-changed.py before opening the PR. Merge on
   green with main green; watch main's run. Then remove this task's
   worktree with scripts/end-task.py, and also remove E:/jon/mg-ar
   (AUDIT-ROOMS) the same way.
9. Handover in docs/handover/home.md: "Big School Begins now waits on
   Jon's play-test, its art, and the release contract (hub card,
   front page, sitemap, 'three or four locks, 15 to 20 minutes' copy)."

DO NOT TOUCH: every other room's room.js; the hub, front page and
sitemap (Big School Begins stays unlisted); the stars key line; rating
bands; the room's text, locks and variants; the cloud lane's handover.

SUCCESS CONDITION: Every unlabelled room renders byte-identically on its
start screen, teacher page and cards (show it). Big School Begins'
preview start screen shows "Starter" and no stars; its teacher page
shows Starter, "for Year 6 and new Year 7" and ★ Warm-up. Both planted
faults fail and the real run passes. test-escape-rating passes with the
new case. Canon records the label and all three exceptions. CI green;
merged; both worktrees removed; handover recorded.

STOP IF: Main's latest full run is red. Any unlabelled room's output
changes by a byte. The cards' chip format cannot carry a label without
changing check_ratings for unlabelled rooms. check-student-labels.py
or any other check objects to "Starter" on a student surface (report
it; SR-11 names it, so do not rename it).

END OF CONTRACT
