LANE: cloud (Claude Code on the web), a FRESH session. SEND: now (SUMS-IN-DISGUISE-BRIDGE merged as #826, cb35e08). The home lane is on DASHBOARD-GLANCE (Apps Script files only); the two touch no common file.
RECOMMENDED: Sonnet 5.5, medium effort. One feedback line in one game, with its verifier checks.

TASK: DD-LINEUP-ORDER. In Decimal Detective's Line-Up (games/decimal-detective/), a wrong answer shows the right order of the cards.

ROOT CAUSE: checkLineup (games/decimal-detective/index.html:849-860 on main cb35e08) marks each card green or red and calls recordAnswer('lineup', allCorrect, equalValueNote(data.suspects)). recordAnswer (:925) then writes "Not quite. Check the evidence." (:939), and the only note is the equal-value one, which most items don't have. So after a wrong Line-Up the right order is never shown. That breaks canon §7.6 (a wrong answer shows the right one before Next) on an Essentials game for the priority audience. Found by ESSENTIALS-AUDIT-LEFTOVERS PR 2 (#776, 15 Nov 2026); docs/todo.md row DD-LINEUP-FEEDBACK, part (1).

CLASS CHECK: Local. Round Up already marks the right option and Place It draws the target ring with "You placed x. y is here.". Only Line-Up's wrong path omits the answer, and its fix is one note built in checkLineup from the item's own data.sorted. recordAnswer (shared by the three types in this page) is unchanged: it already shows a note under the message. Part (2) of the same todo row, Next Case below the fold on phones, belongs to a separate class (Next below the fold after a wrong answer in about 21 games), to be fixed in the shared Next control, so it is out of scope here.

EXACT CHANGE:
0. First commit: the close-out of #826 SUMS-IN-DISGUISE-BRIDGE per AGENTS.md's close-out rule: merge commit cb35e08; merge-pr.py's last line "main cb35e08 run 44360424747: GREEN"; main check-site 44360424747 and phone-fit-full 44360424536 (confirm both from the API); its contract to docs/history/contracts/. Then save this contract verbatim as docs/handover/contracts/2026-11-18-dd-lineup-order.md.
1. games/decimal-detective/index.html, checkLineup:
   - on a WRONG answer, the note is "The right order: " followed by data.sorted joined with ", ", as written in the bank (e.g. "The right order: 0.03, 0.3, 0.303, 0.33, 3.0"), then, if there is one, a space and the equal-value note;
   - on a RIGHT answer, the note is unchanged (the equal-value note or nothing), so a right answer with no note still moves on by itself.
   Change nothing else: not recordAnswer, the cards' green and red marks, Round Up or Place It.
2. scripts/verify-decimal-detective.py, in advance_pass (or beside it):
   - for every Line-Up item, a wrong answer's feedback note contains "The right order: " followed by that item's data.sorted, in order, as written;
   - a right answer without an equal pair has no "The right order" text;
   - an item with an equal pair answered wrong shows both the order and the equal-value note.
   New plants (in PATCHES, with the existing self-test) that must fail:
   - the order line removed;
   - the order printed smallest-last (reversed).
   Every existing check and plant passes unchanged.
3. docs/todo.md row DD-LINEUP-FEEDBACK: mark part (1) done (DD-LINEUP-ORDER); part (2) stays open, noted as "to the shared Next fix (NEXT-IN-VIEW, not yet contracted)".
4. docs/handover/cloud.md entry. The file is over its size and main archives it itself (AGENTS.md:70): do not trim by hand.

DO NOT TOUCH:
- recordAnswer, Round Up, Place It, the bank, the cards' marking (lineupMarks).
- The Next Case fold (part 2), schools/assets/, other games, canon (home lane), the Apps Script files.
- No draft PR.

SUCCESS CONDITION:
- A wrong Line-Up shows "Not quite. Check the evidence." and, under it, "The right order: …" from the item.
- A right Line-Up behaves as before.
- verify-decimal-detective.py passes with both new plants failing.
- The Gate and phone-fit (dispatched on the branch) pass.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover and todo committed.

STOP IF:
- Any bank item's data.sorted is not in ascending numeric order (report the item: that would be a wrong key, priority 1).
- The note makes an existing fold check fail that passed before (report the size and figures; do not change layout here).
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
