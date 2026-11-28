TODO-AUDIT — home lane — Small tier (docs only): merges on green
Recommended: Claude Code, Opus, high effort. Every verdict is a judgement against main and needs evidence.
Send when: now (the home lane is free; TODO-SEARCH-DEMAND merged as a0c6f53).

TASK: Audit every item in docs/todo.md against main, move out everything finished or duplicated with evidence, reduce each still-owed row to what is owed, and list the items that look stale or superseded for Jon to rule on, so the backlog is what is genuinely outstanding.

ROOT CAUSE: The backlog is never checked against reality as a whole, so it grows until the cap stops each new row, and each contract then trims whatever is easiest (TODO-SEARCH-DEMAND, 27-28 Nov: 1,155 bytes short of finished parts, made up from history notes). Shown, main abb9b605: docs/todo.md is 106,470 bytes against TODO_LIMIT 107,520 (scripts/check-context-size.py:59), 132 table rows. By section: §3 rows 45.7 KB; §4 "Prevention and quality" 20.2 KB, all prose, never audited; "Check-ledger debt (DOCS-BUNDLE, 9 Nov 2026)" 9.2 KB; §7 Housekeeping 7.2 KB; §1 7.8 KB; "3.9 — Phone fit order (Jon, 1 Oct 2026)" 4.5 KB; §2 Leaderboard integrity 3.2 KB. Ten rows carry no date after October; ten are parked. Jon, 28 Nov 2026: "why trim and not a proper audit and cut?"

CLASS CHECK: The repeated cap hits are one class (the backlog drifting from main), so the fix is the whole-file audit, not another trim. The rule it applies already exists: AGENTS.md:84, a row records only what is still owed and a finished part moves word for word to docs/history/todo-done.md. This contract adds no new rule and changes no checker.

EXACT CHANGE:
1. First commit:
   a. The close-out of TODO-SEARCH-DEMAND (#942, merge commit a0c6f53) in your new entry in docs/handover/home.md: merge-pr.py's last line "main a0c6f53 run 46095376807: GREEN"; PR head 59cd56a2 check-site 46093722219 and phone-fit-full 46093722236; main on a0c6f53 check-site 46095376807, phone-fit-full 46095376824, pages 46095376554. Confirm each from GitHub Actions. Then git mv docs/handover/contracts/2026-11-27-todo-search-demand.md docs/history/contracts/.
   b. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-28-todo-audit.md.

2. Audit every item: each table row in every section, and each bullet or paragraph of the prose sections (§2, §4, §5, §6, §7, "Check-ledger debt", "3.9 — Phone fit order", "Game ideas, not yet built", "Parked, low priority", "Post-freeze"). Give each exactly one verdict, with evidence from main:
   - DONE: the work is on main. Evidence: the merged PR number or commit, and the file:line, check or CI step that shows it. A §4 prevention item is DONE when a check enforces it: name the check, its CI step, and its self-test plant if it has one.
   - PART DONE: some of it is on main. Evidence as DONE for the finished part.
   - DUPLICATE: the same owed work is in another item. Name that item.
   - OWED: nothing of it is on main, or you cannot show that it is.
   - STALE?: owed on paper, but main suggests it may no longer matter (the code it names is gone or rebuilt, a later ruling covers it, or it was parked and nothing has changed since). Evidence: what you found.
   Anything you cannot evidence is OWED or STALE?, never DONE.

3. Act on the verdicts in docs/todo.md:
   - DONE: the whole item moves, word for word, to docs/history/todo-done.md under a new heading "## Closed by TODO-AUDIT (28 Nov 2026)", each followed by one line of evidence.
   - PART DONE: the finished part moves the same way; the row keeps what is owed.
   - DUPLICATE: the duplicate's owed text, if anything in it is not already in the item it repeats, is added to that item word for word; then the duplicate moves to todo-done with a line naming the item it was merged into.
   - OWED and STALE?: stay. In every row that stays, move any history clause (who moved it where, when it was renamed, past states) out word for word as above. Never reword or shorten owed text.
   - Rows referred to by name elsewhere (a "blocked by" cell, START OF NEXT SESSION, another row) keep their IDs; if a referenced item moves, update the reference to "(closed, TODO-AUDIT)".

4. The report: docs/audits/todo-audit-2026-11-28.md, one table, an item per line: section, row ID or first words, verdict, evidence, bytes moved. Then a separate section "For Jon: STALE? items", one line each: what it is, why it may no longer matter, and the plain choice (keep, or close). Nothing in that section is moved by this contract; Jon's rulings come back as a follow-up contract.

5. Totals in the PR body and the home.md entry: bytes before and after, items by verdict, bytes moved by verdict, and the STALE? count.

DO NOT TOUCH: any game, page, asset, script or checker (TODO_LIMIT and ROW_WARN included); canon; AGENTS.md; CLAUDE.md; the roster; docs/handover/cloud.md. The START OF NEXT SESSION block's wording, except a reference to a moved item. Never move a STALE? item, and never move or reword owed text. Rows the cloud lane's in-flight 3-GON-LINE-UP-BUILD may touch: it does not edit docs/todo.md, but leave row 3-GON-LINE-UP as it is.

SUCCESS CONDITION: Every item in docs/todo.md has a verdict in docs/audits/todo-audit-2026-11-28.md. Every DONE and PART DONE has evidence that resolves on main. Everything moved is in docs/history/todo-done.md word for word under "## Closed by TODO-AUDIT (28 Nov 2026)" with its evidence line. No owed text is reworded. The STALE? section lists each candidate with a keep-or-close choice. check-context-size.py passes. Gate green; merged with merge-pr.py --watch; main's runs green; the totals are in the PR body and home.md.

STOP IF: (1) You find owed work with no row (a live fault, a ruling not recorded): add nothing; report it under "Found, not recorded" in the report and the PR. (2) An item's verdict would decide something only Jon can (a design or priority choice): mark it STALE? with the question. (3) Evidence for a DONE points to a PR that merged but whose change is no longer on main (reverted or overwritten): mark it OWED and report it. (4) A check still fails after your second fix (standing rule). (5) merge-pr.py can't reach GitHub, or a push is refused (never force). (6) Anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies: report it under "Decided for you", and never use it to override a STOP IF.
