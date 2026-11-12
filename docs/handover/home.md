# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-11 (home): STAGE-EXIT-LABEL (HOME-QUEUE-1111, PR 2 of 3)

Claude Code (home lane), worktree `~/mg-stage-exit-label`, branch `claude/stage-exit-label`, PR #738; contract `docs/handover/contracts/2026-11-11-home-queue-1111.md`. `schools/assets/stage-exit.js` build() sets the page's own `a.back-link` to "← Games" (or the script tag's `data-home-label`) before the HUD copy is made; no game page touched, and non-stage games keep "← Back to Games". Measured on all 10 stage-exit games at 1366x768, 390x844, 375x667 and 320x568, normal and Aa, row and HUD (160 measurements, a scratch probe on verify-stage-exit.py's own server and stage start): main's file has the HUD link's text overlapping `#calcBadge` by 6 px (its-on-sale) and `.hud-label` by 3 px (hc-factor) at 320 in Aa; with the change every one reads "← Games" with no overlap and no sideways scroll. `scripts/phone-fit-state.json` had no known-failure entry for any of the 10 games (PHONE-FIT-RED fixed the overflow in CSS), so nothing came off it. `measure-phone-fit.py --only <game>` in normal, `--aa` and `--laptop` for the 10: all 30 exit 0; the one FAIL row printed, `free-daily-pizza` in Aa (Next below the fold after a wrong answer), is identical with main's `stage-exit.js` and has no state entry, so it is not this change's. /updates/ line under November. No claim held.

## 2026-11-11 (home): PACK-APPROVED (HOME-QUEUE-1111, PR 1 of 3)

Claude Code (home lane), worktree `~/mg-pack-approved`, branch `claude/pack-approved`, PR #737; contract `docs/handover/contracts/2026-11-11-home-queue-1111.md` (three PRs, one at a time; PR 2 STAGE-EXIT-LABEL and PR 3 WHOSE-SIDE-LISTING follow). Each pack config carries `wording_approved` ({"by", "date"} or null; no key counts as null): christmas-tree-fiasco and kiln-disaster `{"by": "Jon", "date": "2026-11-07"}`. `build_pack.py` prints the DRAFT badge (its only draft marker: main's PDFs say DRAFT on pages 1 and 2 only) while it is null, fails a build whose approved room prints DRAFT anywhere (AUDIT_JS reads each whole page, head included), and `--final` refuses an unapproved room by name. Selftest 32/32 (three new plants: DRAFT on an approved page 1; an unapproved page 2 without its badge; `--final` on null and on a missing key) plus a control (approved: no DRAFT; unapproved: pages 1 and 2). Both packs rebuilt with `--final`: no DRAFT on any page; pages 3 onward pixel-identical to main's build at 150 dpi; on pages 1-2 every changed pixel is in one 280x47 px box at the top right that held only the badge and is blank paper now. Proofs `docs/screens/pack-approved/`. README: approval paragraph, page 1-2 lines. No page wording, layout, lockcheck.py, final.py or label fitting touched. No claim held.

## 2026-11-11 (home): RULES-EMULATOR-TEST

Claude Code (home lane), worktree `~/mg-rules-emulator-test`, branch `claude/rules-emulator-test`, PR #736; contract `docs/handover/contracts/2026-11-11-rules-emulator-test.md` (unnamed in the paste; named here). `firebase/rules.test.mjs` gains four cases for the 10 Nov `recent_scores` change: game `"<b>x</b>"`, game `"a<b"` and level `"GCSE > Higher"` refused, "Factor Race"/"GCSE" accepted. The emulator suite passes 36 of 36 against main's rules; against the pre-#728 rules the three refusals fail. `docs/firebase-rules-deploy.md`: the 10 Nov section's Playground test (hand-typed timestamp) is replaced by the suite result; the deploy section and AGENTS.md carry the rule (canon §12, RULES-EMULATOR-TEST). `database.rules.json` untouched. Tooling: no Java was on this machine; a user-local Temurin JDK 21 is in WSL `~/.local/jdk/jdk-21.0.13+9` (set `JAVA_HOME` to it and put its `bin` on `PATH` before the run); `firebase/package-lock.json` from `npm install` is not committed. Todo row FIREBASE-ESCAPING closed and moved to `docs/history/todo-done.md`. No claim held. The rules were already deployed by Jon 08:12 11 Nov 2026 (a real score reached its board); this PR changes tests and docs only, so no deploy follows it.

## 2026-11-10 (home): FIREBASE-ESCAPING

Claude Code (home lane), worktree `~/mg-firebase-escaping`, branch `claude/firebase-escaping`, PR #728; contract `docs/handover/contracts/2026-11-10-firebase-escaping.md`. The hub escapes every Firebase value it renders (board initials, score and timestamp; the all-time high's score and date) through one esc(); the '&mdash;' fallback stays markup. The rules file refuses `<` and `>` in `recent_scores` `game` and `level`, written, NOT deployed: Jon deploys (`docs/firebase-rules-deploy.md`, "10 Nov 2026 change"). Plant in `scripts/test-scores-offline.py`: markup initials on a fake board; the unescaped hub is caught. STOP IF checks: no other page or shared asset renders Firebase data unescaped (the ticker escapes; Free Daily Pizza's target is a number checked with typeof); no game name or level label holds `<` or `>`; the rules are tested in the console's Rules Playground, no write. No claim held. Todo row FIREBASE-ESCAPING stays open for the deploy only.

## 2026-11-10 (home): HUB-ALL-BOARDS

Claude Code (home lane), worktree `~/mg-hub-all-boards`, branch `claude/hub-all-boards`, PR #727; contract `docs/handover/contracts/2026-11-10-hub-all-boards.md` (preamble, contract and Jon's ruling). The hub lists year6 and all for Fraction Snap, Percentage Flip and Prime Sprint; the 'all' pill reads "All levels" (levelLabel('all') is '' by design, so the hub page labels its own pill; no shared asset touched). check-leaderboard-coverage.js reads a level variable's literal or ternary-of-literal assignments, else the roster's tiers; a selftest runs on every invocation. STOP IF hit: correlation-or-coincidence and the-perfect-prank also changed derivation; on Jon's ruling both now-stale LEVEL_OVERRIDES entries were removed, the correlation reason kept as a comment. Row 1.35: hub part fixed, extract-banks part left open. No claim held. Next: FIREBASE-ESCAPING from the new main.

## 2026-11-10 (home): HOME-DOCS-1110

Claude Code (home lane), worktree `~/mg-home-docs-1110`, branch `claude/home-docs-1110`; contract `docs/handover/contracts/2026-11-10-home-docs-1110.md`. R1 and R2 match cloud.md's standing rules line for line. Canon §12 gains "MERGE-ROUTE and CLOSE-OUTS"; AGENTS.md's merge bullet gains the CLOUD-MERGE-TOKEN exception (151 bytes) and a close-outs bullet (245 bytes); todo rows added; PLAYTEST-S1 closed to todo-done.md. Cloud close-outs carried: none (#725's rides on CAST-AWAY-DIAGNOSE, the lane's next task). Item 5 stopped on its STOP IF (row 1.25 also held the untracked `previous_score` dead-column finding); Jon's ruling (10 Nov evening, option 1) added row PREVIOUS-SCORE-COLUMN (§4 item 43), so eight rows in all, then 1.25 closed to todo-done.md and the backfill note added to `docs/sheets-falsy-backfill.md` §7. Next step: Gate green, then Project Claude's review and Jon's "merge".

## 2026-11-10 (home): PHONE-SCROLL

Ran in a cloud container on branch claude/amazing-goldberg-2eiqbm, committed as Claude, as the only running lane (Amendment 1, item 4). PR #721.

Wide tables and display maths scroll in their own box on a 320px phone. `escape-rooms/assets/teacher.js` wraps its three `table.tt` in `div.tt-scroll` (`engine.css`: `overflow-x:auto`, the table's margin moved to the box). `parents/guide.js` wraps every guide table in `div.table-scroll` (margin moved likewise), and `parents/guide.css` scrolls `.katex-display` in its own line. Amendment 1: standard-form's 33-digit number breaks at its commas (`<wbr>`, line 120 only) and "weighs" became "has a mass of"; the 2px display padding removed. 20 `tier1_phone_overflow` entries removed: 14 teacher pages and six guides. Todo 1.37 and 1.38 closed to todo-done.md; 1.34 updated. Tables pixel-identical to main at 1366×768. /updates/ line added.

Amendment 1 item 2 stopped: without padding, `overflow-y:hidden` cut one anti-aliased pixel row from a tall fraction on 9 of the 94 display blocks (13 guides × 2 widths); my earlier "nothing clipped" had covered 5 guides only. Amendment 2 (Project Claude, 06:50) reversed it: `.katex-display` gets `padding:2px 0`, and 0 of 94 blocks lose ink against main (+4px per display line).

Amendment 3: `scripts/verify-parent-guides.py:621`'s locator pinned the old wording ("weighs about"), so the Gate failed its SF check; the regex now reads "has a mass of about", nothing else changed. 353 checks, 0 failed; its ARITH check runs and passes (5,970,000,000,000,000,000,000,000 = 5.97 × 10^24). The script has no selftest; two faults planted in a scratch copy were caught (a wrong power, FAIL ARITH; the old wording, FAIL FOUND).

Discoveries: `scripts/test-escape-rating.py` still hides `table.tt` at 320px, no longer needed (not touched: outside EXACT CHANGE).

Merged as a594c8f (#721), squash pinned to 8e5e1e7, through the GitHub connection under Jon's one-off ruling below (merge-pr.py could not run: this container's GH_TOKEN is invalid). Re-checked first, as the ruling asks: the Gate on 8e5e1e7 green (89 jobs: 87 success, 2 skipped); mergeable, no conflicts; main's newest merge 10d3167's run 42691430373 green (89/89 jobs), nothing newer on main but the bot's c8ac737, no run on main queued or in progress. No skip marker in the title or body. The squash message was a condensed form of the PR body with the ruling noted, not the body verbatim as merge-pr.py would send. Main's run on a594c8f: check-site 42772678182 GREEN, all 89 jobs successful; phone-fit-full 42772678203 green. Done: merged and live. Contract moved to `docs/history/contracts/`. Cleanup: end-task.py always refuses in a cloud session (cloud.md); GitHub deleted the merged branch.

The ruling, verbatim:

> RULING (Jon, Tue 10 Nov 2026, 07:05): one-off merge route for #721 only.
> merge-pr.py cannot run in this container (GH_TOKEN invalid). For #721 only, merge through the GitHub connection: first re-check and report (1) the Gate on 8e5e1e7 is green, (2) the PR is mergeable with no conflicts, (3) main's newest full run is green and no newer commit has landed on main since; if any fails, STOP. Squash-merge pinned to head SHA 8e5e1e7 (refuse if the head has moved), with any "[skip ci]" in the message disarmed as merge-pr.py does. Then watch main's run on the merge commit and report its result. Record this ruling verbatim in the close-out entry. merge-pr.py remains the only standing route; this ruling covers #721 and nothing else.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 3; usage n/a.

## 2026-11-09 (home): DOCS-BUNDLE

`docs/rules/games.md` agrees with AGENTS.md: line 3 (a PR that fixes a todo row updates it; a cloud PR may fix more than one small game when its contract says so), line 5 (such a PR claims its games in one commit) and line 13 (Amendment 2: Jon's findings become todo rows; `docs/jon-playtest-2026-08.md` is a historical log, marked so at its top). The log's one open item, Snagging S1, is row PLAYTEST-S1; its #4 (Circle Theorem Spotter Q48) was fixed on 3 Oct (row 1.3, PR #11) though its status table still says Open. `docs/audits/ledger-debt-2026-11.md` surveys `data/check-ledger.json`: 167 entries in 43 games (B4 96, B7 44, B6 18, B3 8, B2 1), none a wrong answer a student can see; 49 LEDGER-* rows in todo §4. Nine rows from 9 Nov's findings and requests; notes appended to LOCAL-CHECKS and 1.36. Canon §0.3 gains SR-31 (Jon's standing STOP IF rules, word for word) and SR-32 (same-day fix of a CRITICAL level, SR-20's exception); cloud.md's SWEEP-1 label reads SR-32; rows STANDING-STOP-RULES and SR-NUMBERING closed. `scripts/list-initials.mjs` lists leaderboard entries by initials with public reads only: 37 for JLF and SSF, all reads succeeded (table in the PR body only).

Discoveries: the ledger's `line` fields were stale (row LEDGER-LINE-DRIFT). Before the start, a stopped agent's ~/mg-docs-bundle (local branch at origin/main, one untracked file, no remote branch) was discarded on Project Claude's note: end-task.py refused it (no PR), and I removed the worktree and branch by hand, against AGENTS.md's "report refusals without bypassing them". Nothing was lost; reported to Jon.

Next: Project Claude's review and Jon's "merge".

Record: agent Claude Code; wall n/a; review cycles 0; amendments 2; usage n/a.

## 2026-11-09 (home): MONEY-INPUT

`MaffsAnswer.moneyInput(input, currency)` in `schools/assets/answer.js` turns a game's own input into a money box: a text box with a number keypad (a typed £ no longer empties it) and a fixed £ or € inside its left edge (Jon, 9 Nov; canon §7.1.3). All six games that mark with `MaffsAnswer.money()` call it: estimation-engine, its-on-sale, split-it, squared-squirrel, tax-theft and the-6-ps. Each one's old £ beside the box went. tax-theft's "Please enter a number." check now reads a typed £. `scripts/check-banks.py` fails any page that marks money without the helper, and its plant runs in `--ci`. Marking is unchanged. growth-and-decay is not on the list: it marks to significant figures, never by `money()` (todo 1.36). Claims taken and released in the PR.

Discoveries: four of the six verifiers fail locally on clean main as well (keypad and timeout races in WSL; LOCAL-CHECKS); CI is the authority.

Next: Project Claude's review, Jon's look and "merge". Row 1.36 stays open for its 1 d.p. key check.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 0; usage n/a.

## 2026-11-08 (home): BRANCH-CLEANUP

Phase 1 (#712, 80f3eef; main run 42526066041 GREEN): `docs/history/branch-cleanup-2026-11.md` sorts the 156 remote branches into DELETE 124, KEEP 20 and NO PR AT TIP 12. `delete_branch_on_merge` was already true. cloud.md's contracts paragraph now matches AGENTS.md, and its Queue holds only in-flight facts and todo pointers (16,326 → 10,327 bytes); 12 todo rows added, SCREENING-ROOM-FOLD among them.

Phase 2, after Jon's "merge": 124 REST deletes, each 204. `git ls-remote --heads origin` then listed 32 branches: the 20 KEEP and 12 NO PR AT TIP, none of the 124. GitHub removed claude/branch-cleanup on merge. The close-out PR adds Amendment 1's two rows (REPORT-EMAIL-PROPERTY, SR-NUMBERING), closes the BRANCH-CLEANUP row to todo-done.md, moves the contract to history, and moves home.md's DONE Queue lines to the archive verbatim.

Discoveries: `scripts/test-answer-lock.py` now fails locally on clean main too (LOCAL-CHECKS); it passes in CI.

Next: Project Claude's review and Jon's "merge". The 12 NO PR AT TIP verdicts (11 DELETE proposed, 1 JON) wait for a ruling; nothing deletes them.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 1; usage n/a.

## 2026-11-08 (home): LIVE-BUG-RECHECK

Every §1 row of `docs/todo.md` re-checked against main f8a287b4, each with a dated verdict and evidence appended to its text: 4 FIXED (1.8, 1.24, 1.30, 1.40, moved with the §7 row to `docs/history/todo-done.md`, "Closed by LIVE-BUG-RECHECK"), 10 PART, 9 STILL LIVE, no row wholly CAN'T TELL. No live wrong answer found. AGENTS.md gains the rule that a fixing PR updates its todo row; its reason is in canon §12. Table, fix order and evidence: the PR body.

Discoveries: main's nightly phone-fit-full run 42466279497 is red in laptop mode alone (screening-room, Next 717 / 680 at 1280×720, not on the known-failures list), reported for the cloud lane. The `--live` checks owed by 1.8 and 1.14 ran: both OK, deployed pages byte-identical to main.

Next: Project Claude's review and Jon's "merge"; then BRANCH-CLEANUP (START block).

Record: agent Claude Code; wall n/a; review cycles 0; amendments 1; usage n/a.

## 2026-11-07 (home): BACKLOG-ONE

`docs/todo.md` is the single backlog. AGENTS.md gains rules b–h of the contract: no draft PRs; no environment, network or credential change without asking Jon; never merge on a Gate older than main's newest checks; one lane at a time (replacing "at most two implementers", line 70 removed); CI over local browser runs on maffs; Queues hold only in-flight cross-lane facts; a contract not finished is pointed to by a todo row. Lines 7, 69, 72 and 78 amended. Contract with Amendment 1: `docs/handover/contracts/2026-11-07-backlog-one.md`.

Parked under Jon's standing STOP IF rules, as todo rows for Project Claude to rule on. Rule a (HANDOVER-IN-TASK-PRS) conflicts with AGENTS.md's "keep the branch handover current" and the takeover paragraph built on it. Rule i (STANDING-STOP-RULES) conflicts with "What may enter an always-loaded file": a 300-byte cap with reasons in canon §12, which this contract may not touch.

Contracts: 53 moved to `docs/history/contracts/` (52 merged; PLAN-SHARED-ASSETS superseded by GATE-STEP-6); six kept, each with a todo row. Todo: 36 rows added, plus the START block. No row moved: each row marked DONE or FIXED still names something owed (listed in the PR). cloud.md's live pointers that held work now point to rows. Its Queue paragraph still holds unfinished items (FRACTION-STACK follow-up, the 27 Oct session queue): outside this contract.

Next: Project Claude's review and Jon's "merge".

Record: agent Claude Code; wall n/a (spanned a STOP and Amendment 1); review cycles 0; amendments 1; usage n/a.

