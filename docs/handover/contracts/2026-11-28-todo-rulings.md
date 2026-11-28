TODO-RULINGS — home lane — Small tier (docs only): merges on green
Recommended: Claude Code, Sonnet, effort medium. Every action is listed by the audit's own numbering; no judgement beyond finding the text.
Send when: TODO-AUDIT (#944) has merged.

TASK: Apply Jon's rulings on the 35 STALE? items of docs/audits/todo-audit-2026-11-28.md, and correct three rows Project Claude found wrong or out of date.

ROOT CAUSE: TODO-AUDIT (#944) listed 35 items it could not close without Jon. Jon, 28 Nov 2026, 08:23, Project Claude chat: "all other decisions are fine", accepting Project Claude's recommendation on every one (close 32, keep 3 with a change). Separately, three rows that stay are wrong on main (shown, main after #944):
- GRAPH-SKETCHER-REDESIGN points (2) and (10) say the shared calculator has no x^y, e, sin or cos. schools/assets/calculator.js:38-40 has all of them in scientific mode (contract SCI-CALC, 9 Oct 2026; mount(el, {keys: 'scientific'})).
- CGD-PHONE-LONG waits for "PHONE-FIT-ALL-ITEMS", which is no row; the work it means is §4 item 37(b) (the Gate measures one seeded question per game).
- Row 3.21's list of 22 games is the 4 Oct survey; 11 now load schools/assets/keypad.js (component-crusher, estimation-engine, graph-sketcher, growth-and-decay, just-pythag-it-bruv, log-laws, quadratic-factoriser, split-it, stat-attack, suvat, test-the-claim; counted by Project Claude on main, 28 Nov).

CLASS CHECK: Not a bug class: backlog text only, by Jon's rulings and the evidence above.

EXACT CHANGE:
1. First commit: TODO-AUDIT's close-out (#944) in your new docs/handover/home.md entry (merge-pr.py's last line and main's run IDs, confirmed from GitHub Actions), git mv its contract docs/handover/contracts/2026-11-28-todo-audit.md to docs/history/contracts/; save this contract verbatim as docs/handover/contracts/2026-11-28-todo-rulings.md.

2. Close. Numbers are the "For Jon: STALE? items" list in docs/audits/todo-audit-2026-11-28.md. Each item named below moves word for word from docs/todo.md to docs/history/todo-done.md under a new heading "## Closed by Jon's rulings on TODO-AUDIT (28 Nov 2026)", each followed by "Closed by Jon, 28 Nov 2026 (TODO-AUDIT item N): <the reason given in the audit's line for it>."
   - Close outright: 2, 4, 5, 7, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 30, 31, 32, 33, 34, 35.
   - Item 1: close only the "chart-interrogator submits a constant 100" part (the page now multiplies its score, games/chart-interrogator/index.html:1277); any wording about its `l4` key stays.
   - Item 3, FOLD-COMPONENTS: close the row; before deleting, record each of its four branches' names and last commit SHAs (44a4ef8, 227c3d6, 4a526a6, ed00d80, as the audit found) in the todo-done entry; then delete the four remote branches (git push origin --delete <branch>). Nothing else is deleted.
   - Items 24 and 27: close into row START-SIDEWAYS-GATE. Any owed text in them not already in that row is added to it word for word; then they move.
   - Item 28 (§4 item 50, AA-KEY-MISMATCH): close into §4 item 37(c); add to item 37(c) "Owner: home lane (a shared-asset fault; Jon, 28 Nov 2026)." if it names no owner.
   - Item 29 (Matrix Crunch 50+50): close into its ledger row, which asks for 40 per level.

3. Keep, with Jon's change:
   - Item 6, PRIME-SPRINT-LOOK-REDS: replace "Close the row, or contract that fix." with "Jon, 28 Nov 2026: contract that fix." and the owner cell "**Jon** — close it, or the contract" with "Project Claude (contract)".
   - Item 8, HIGHER-POWER-PHONE: replace "Parked (Jon, 3 Nov)." with "Unparked (Jon, 28 Nov 2026): Higher Power still fails the phone-fit Gate in normal and Aa (`scripts/phone-fit-state.json`)." The owner cell stays.
   - Item 15: in row NUMBER-BONDS, after "needs building soon" (Jon, 18 Nov 2026)." add: "One game, not two (Jon, 28 Nov 2026): stages for bonds to 10, 20, 100 and 1000, and decimals to 1 (from the idea \"Bond. Number Bond.\")." Then the idea line "- **Bond. Number Bond.** [PROPOSED]: number bonds to 10/100/1000, and decimals to 1." moves to todo-done with "Folded into NUMBER-BONDS (Jon, 28 Nov 2026)."

4. Corrections (Project Claude, evidence in ROOT CAUSE):
   - GRAPH-SKETCHER-REDESIGN: replace "the site calculator (`schools/assets/calculator.js`) has none of x^y, e, sin, cos" with "the site calculator (`schools/assets/calculator.js`) has them all in scientific mode (SCI-CALC, 9 Oct 2026; mount(el, {keys: 'scientific'})), but this game does not mount it"; replace "(10) depends on the shared calculator gaining x^y, e, sin and cos (a later contract)" with "(10) mounts the shared calculator in scientific mode".
   - CGD-PHONE-LONG: replace "(PHONE-FIT-ALL-ITEMS)" with "(§4 item 37(b))" and, in the owner cell, "after PHONE-FIT-ALL-ITEMS" with "after §4 item 37(b)".
   - Row 3.21: replace the sentence beginning "**Games with a typed answer box (22, survey 4 Oct 2026):**" through "Which of the rest are done is not recounted here;" with "**Still to move onto the keypad (11 of the 22 in the 4 Oct 2026 survey; recounted 28 Nov 2026):** `52dle`, `chart-interrogator`, `estimation-golf`, `factor-theorem`, `fermi-lab`, `given-that`, `glorious-gantt`, `like-terms-collector`, `percentage-flip`, `screening-room`, `tax-theft`." and move the removed sentence, word for word, to todo-done under the same heading with "Done by 28 Nov 2026: component-crusher, estimation-engine, graph-sketcher, growth-and-decay, just-pythag-it-bruv, log-laws, quadratic-factoriser, split-it, stat-attack, suvat, test-the-claim (each loads schools/assets/keypad.js)." Keep "history in `docs/history/todo-done.md` under 3.21." Before writing, confirm on main that exactly those 11 load keypad.js and the other 11 do not.

5. docs/audits/todo-audit-2026-11-28.md: under its "For Jon" heading add one line: "Ruled by Jon, 28 Nov 2026; applied by TODO-RULINGS." Nothing else in the report changes.

6. Totals in the PR body and home.md: bytes before and after, items closed, kept and corrected.

DO NOT TOUCH: any game, page, asset, script or checker; canon; AGENTS.md; CLAUDE.md; the roster; any row or item not named above; any remote branch except the four FOLD-COMPONENTS branches; docs/handover/cloud.md.

SUCCESS CONDITION: Every item in steps 2-4 is done exactly as written; everything moved is word for word in docs/history/todo-done.md under the new heading with its line; the four FOLD-COMPONENTS branches are deleted and recorded; check-todo-trim.py and check-context-size.py pass; Gate green; merged with merge-pr.py --watch; main green.

STOP IF: (1) An item's text is not on main where the audit's line says (it moved or changed after #944): report it; do not guess. (2) The keypad recount differs from the 11 and 11 above. (3) A FOLD-COMPONENTS branch has a commit after 27 Oct 2026, or a SHA differs: do not delete it; report. (4) A check still fails after your second fix (standing rule). (5) merge-pr.py can't reach GitHub, or a push is refused (never force). (6) Anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies: report it under "Decided for you", and never use it to override a STOP IF.
