# LIVE-BUG-RECHECK (Project Claude, 8 Nov 2026 18:55; Amendment 1, 19:08), verbatim

LIVE-BUG-RECHECK (Project Claude, 8 Nov 18:55)
LANE: home (Claude Code) · TIER: Docs · CONTRACT: LIVE-BUG-RECHECK · new worktree from origin/main AFTER #710 has merged (branch claude/live-bug-recheck). No other lane is running. Stop at a green Gate for Project Claude's review and Jon's "merge"; do not merge. Not a draft. Save this contract verbatim in docs/handover/contracts/ in the first commit.

TASK: Re-check every open row in docs/todo.md §1 ("Live bugs and false claims") against current main, record a dated verdict with evidence on each, close the ones that are fixed, and add the rule that stops rows drifting again.
ROOT CAUSE: §1 rows record live bugs, but nothing ties a fixing PR to its row, so fixes merged elsewhere (or partly) left rows open, and rows marked FIXED/DONE in their own text (1.14, 1.26, 1.48, 1.51) still sit in §1 owing a remainder. Nobody can tell from the backlog which live bugs a student can still hit.
CLASS CHECK: Yes, a class: backlog drift across every row, from a missing step in shared process (no PR closes the row it fixes). Fix at the process layer with one AGENTS.md rule (step 4), plus a single sweep to bring the current rows to truth (steps 1–3). Not per-row patches.
EXACT CHANGE:
1. Scope: every row in the §1 table on main: 1.4, 1.8, 1.14, 1.17, 1.23, 1.24, 1.25, 1.26, 1.27, 1.30, 1.32, 1.34, 1.35, 1.36, 1.37, 1.38, 1.39, 1.40, 1.48, 1.51, 1.52, 1.71, FIREBASE-ESCAPING. Not the "Done this session (26 Sep)" narrative below the table. Multi-part rows (1.26, 1.51 …) get a verdict per part.
2. For each row (or part), one verdict, evidence required:
   FIXED: name the merge (PR/commit) AND the proof on main: the verifier/check that now covers it and passes in CI, or file:line on main showing the fix. "Could not reproduce" alone is not FIXED.
   STILL LIVE: file:line on main, or the failing check output, showing it still happens.
   PART: what is fixed (with evidence) and exactly what remains.
   CAN'T TELL: why (e.g. needs Jon's deployed Apps Script, Firebase or Sheet; not covered by any CI check).
   Phone/overflow rows (1.34, 1.37, 1.38, 1.39, 1.40): use main's latest full phone-fit run in CI (AGENTS.md: CI over local runs on maffs). If a page is not in that run, a local measurement is allowed but labelled "local, unconfirmed".
   Run existing verifiers and checks only; write no new check, plant or test.
3. docs/todo.md and docs/history/todo-done.md:
   a. Never rewrite a row's existing text. Append to the row: "Re-checked 2026-11-DD on main <sha>: <VERDICT> — <evidence>." (use the actual date and sha).
   b. A row whose every part is FIXED moves word for word, with its re-check note, to docs/history/todo-done.md under a new heading "Closed by LIVE-BUG-RECHECK (Nov 2026)"; add its number to §1's "numbers still resolve there" list so every number resolves.
   c. STILL LIVE / PART / CAN'T TELL rows stay in §1 with their note.
   d. Close the LIVE-BUG-RECHECK row in §7 the same way. Leave the START block's order as it is.
4. AGENTS.md, Contracts and handovers: add one rule, at most 300 UTF-8 bytes, worded as: "A PR that fixes all or part of a docs/todo.md row updates that row in the same PR, and moves it to docs/history/todo-done.md when nothing is owed. Jon, 8 Nov; LIVE-BUG-RECHECK." Put its reason (this root cause, two sentences) in canon §12 in the same PR, as AGENTS.md's "What may enter an always-loaded file" requires.
5. PR body: a table, one line per row/part: number · game/page · verdict · evidence · canon §0.2 tier. Then a proposed fix order for STILL LIVE and PART rows, tier 1 (wrong answers a student sees) first; Project Claude decides the order. Then "Live wrong answers" at the top if any row shows a student being marked wrong for a right answer (or right for a wrong one) today.
6. Handover: home.md in-flight line and close-out entry under the current AGENTS.md rules.
DO NOT TOUCH: any game, page, script, shared asset, workflow, test or verifier (re-checking only, no fixes, even one-line ones, SR-9 notwithstanding); canon other than the one §12 reason in step 4; the existing text of any row; any other docs/todo.md section except §1 and the §7 LIVE-BUG-RECHECK row; branches; answer-lock-state.json; Jon's Sheet, Apps Script, Firebase or GSC.
SUCCESS CONDITION: every §1 row/part carries a dated verdict with evidence; fully fixed rows are in todo-done.md word for word and their numbers resolve; AGENTS.md has the one rule (≤300 bytes) with its canon §12 reason; PR body carries the verdict table, the proposed fix order and any "Live wrong answers"; check-context-size and the Gate green. Stop for Project Claude's review and Jon's "merge".
STOP IF: #710 has not merged; a verdict needs anything changed outside DO NOT TOUCH's allowance (mark it CAN'T TELL and carry on — stop only if more than 5 rows would be CAN'T TELL, then report the list); the new AGENTS.md rule conflicts with an existing AGENTS.md line (report the line, do not overwrite); a file-size check fails (report file and size).

## Amendment 1 (Project Claude, 8 Nov 19:08), verbatim

LIVE-BUG-RECHECK — Amendment 1 (Project Claude, 8 Nov 19:08). LANE: home.
In the first commit, also git mv docs/handover/contracts/2026-11-07-backlog-one.md to docs/history/contracts/ (BACKLOG-ONE merged as 68ae9e4, #710). DO NOT TOUCH is unchanged otherwise; no other contract file moves.
