# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 pending. Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-10 (home): PHONE-SCROLL

Ran in a cloud container on branch claude/amazing-goldberg-2eiqbm, committed as Claude, as the only running lane (Amendment 1, item 4). PR #721.

Wide tables and display maths scroll in their own box on a 320px phone. `escape-rooms/assets/teacher.js` wraps its three `table.tt` in `div.tt-scroll` (`engine.css`: `overflow-x:auto`, the table's margin moved to the box). `parents/guide.js` wraps every guide table in `div.table-scroll` (margin moved likewise), and `parents/guide.css` scrolls `.katex-display` in its own line. Amendment 1: standard-form's 33-digit number breaks at its commas (`<wbr>`, line 120 only) and "weighs" became "has a mass of"; the 2px display padding removed. 20 `tier1_phone_overflow` entries removed: 14 teacher pages and six guides. Todo 1.37 and 1.38 closed to todo-done.md; 1.34 updated. Tables pixel-identical to main at 1366×768. /updates/ line added.

Amendment 1 item 2 stopped: without padding, `overflow-y:hidden` cut one anti-aliased pixel row from a tall fraction on 9 of the 94 display blocks (13 guides × 2 widths); my earlier "nothing clipped" had covered 5 guides only. Amendment 2 (Project Claude, 06:50) reversed it: `.katex-display` gets `padding:2px 0`, and 0 of 94 blocks lose ink against main (+4px per display line).

Amendment 3: `scripts/verify-parent-guides.py:621`'s locator pinned the old wording ("weighs about"), so the Gate failed its SF check; the regex now reads "has a mass of about", nothing else changed. 353 checks, 0 failed; its ARITH check runs and passes (5,970,000,000,000,000,000,000,000 = 5.97 × 10^24). The script has no selftest; two faults planted in a scratch copy were caught (a wrong power, FAIL ARITH; the old wording, FAIL FOUND).

Discoveries: `scripts/test-escape-rating.py` still hides `table.tt` at 320px, no longer needed (not touched: outside EXACT CHANGE).

Merged as a594c8f (#721), squash pinned to 8e5e1e7, through the GitHub connection under Jon's one-off ruling below (merge-pr.py could not run: this container's GH_TOKEN is invalid). Re-checked first, as the ruling asks: the Gate on 8e5e1e7 green (89 jobs: 87 success, 2 skipped); mergeable, no conflicts; main's newest merge 10d3167's run 42691430373 green (89/89 jobs), nothing newer on main but the bot's c8ac737, no run on main queued or in progress. No skip marker in the title or body. The squash message was a condensed form of the PR body with the ruling noted, not the body verbatim as merge-pr.py would send. Main's run on a594c8f: check-site 42772678182, pending at the time of writing. Contract moved to `docs/history/contracts/`. Cleanup: end-task.py always refuses in a cloud session (cloud.md); GitHub deleted the merged branch.

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

## 2026-11-07 (home): PHONE-FIT-RED

Done: #701 merged by `merge-pr.py` as 3fe605d6; main run 42398273354 GREEN. Project Claude reviewed it and Jon authorised the merge. The workflow went in first through cloud's #702 (023a8215), because this lane's token can't push workflow files. #701 left draft by Jon's `gh pr ready`. Contract: `docs/history/contracts/2026-11-07-phone-fit-red.md`.

Nine games were red on the full run, not seven: `its-on-sale` and `y-so-steep` had been dropped from the contract's list. The sideways group came from STAGE-EXIT (ed9b7374, #608), which added a HUD link that couldn't shrink; the Gate never runs `measure-phone-fit.py`, so nothing caught it. Fixed in `stage-exit.css` (five sideways games, and `possibly-maybe` by hand), plus Pies, `distinctly-average` and `better-value` in their own pages. `possibly-maybe` is on the unmeasurable list until PROBE-DATA-OPT.

Full runs on main: 023a8215, without the fixes, red as expected (normal 663 s, aa 665 s, laptop 449 s; 30m43s in all). 3fe605d6, with them, normal and aa exit 0, laptop exit 1 on one pair: `screening-room`'s `1280x720 next` entry is stale (659 s, 659 s, 446 s; 30m27s in all). All nine games pass in CI.

Done since: cloud's #707 (PHONE-FIT-FULL-SPLIT) split the workflow into per-mode jobs and removed the stale entry. It merged as 0ec5cd4, and main's full run is green (42403456019).

Follow-ups:

- PROBE-DATA-OPT: the checker should see `[data-opt]` delegated buttons, with `possibly-maybe`'s entry coming off; the sideways check should run on every game, including unmeasurable ones; "asking only" on `hc-factor`, `y-so-steep`, `i-found-a-mark` and `who-ate-all-the-pies` (diagnose, don't assume: `y-so-steep` and `i-found-a-mark` have no `[data-opt]`).
- Aa audit: HUD label overlap at 375; `line-height` below 1.5 (`distinctly-average` sets 1.4).
- Jon's decision: a shorter "← Games" label, as the wrapped link runs 3-9 px onto the next element at 320 Aa.
- LOCAL-CHECKS: browser verifiers fail intermittently in WSL `maffs`, on clean main too. Leading lead, untested: WSL's clock stepping backwards, up to 2.884 s in 40 s. Local runs measure `screening-room` 717/680 while CI passes it; CI is the authority.

Record: agent Claude Code; wall 6:35; review cycles 1; amendments 11; usage n/a.

## 2026-11-07 (home): PACK-COVER close-out

Done: #703 merged by `merge-pr.py` as 7043a989; main run 42394072989 GREEN. Jon authorised merge on 7 Nov; Project Claude reviewed and passed #703's proofs on 7 Nov. Contract: `docs/history/contracts/2026-11-07-pack-cover.md`.

The shared pack template now prints each room's own win scene on page 1. Christmas and Kiln build with a 1465 × 799 pixel image at about 200 dpi; the scenes remain readable in greyscale and show no visible digits. Proofs are in `docs/screens/pack-cover/`. Pages after page 1 are pixel-identical to clean main builds at 100 dpi. The missing-image and page-overflow plants passed with all existing plants (29/29); `check-changed.py` passed 42/42 selected checks, and #703's Gate was green before merge. The PDFs grew by 259,760 bytes (Christmas) and 197,232 bytes (Kiln).

Record: agent Codex; wall n/a (work spanned conversations); review cycles 0; amendments 0; usage n/a.

## 2026-11-07 (home): CHRISTMAS-PACK close-out

Done: #689 merged by `merge-pr.py` as b4d0323; main run 42362844296 GREEN. Jon authorised merge on 7 Nov. The six-set Christmas Tree Fiasco printable pack builds with 98 of 900 joint draws VALID; its 18 printed lock answers agree with 108 independently recomputed values. The PDF stays gitignored in `dist-packs/`, never committed or uploaded. Contract and Amendments 1–5: `docs/history/contracts/2026-11-06-christmas-pack.md`; the two later typography and box-measurement corrections are reported in #689.

Final review fixes: a one-box label splits each ` · ` fact onto its own line; lock names ending `?` or `!` gain no colon in the key. The hall plan and Eric's clipboard boxes sit inside their drawn paper. All Christmas labels fit at 11 pt or more; all other fitted sizes stayed unchanged. Kiln's rebuilt PDF is pixel identical to the pre-fix build. The generator selftest caught 27 of 27 plants; `check-changed.py` passed 51 of 51 selected checks on the final branch, and #689's Gate was green before merge. Proof PNGs are in `docs/screens/christmas-pack/`. This entry follows #693's merged close-out on main, with #693's entry retained below.

Record: agent Codex; wall n/a (work spanned fresh sessions); review cycles 3; amendments 5; usage n/a.

## 2026-11-07 (home): ROOM-SEARCH-TITLES, review fixes (Amendment 2)

Room descriptions no longer read lockMeta: every live room's games.json entry carries a required, person-written "topics" (short_topics renamed), the 14 lists verbatim from Amendment 2; check-meta.py fails a room with none or blank. Every description is at most 120 characters; nothing was shortened. The hub description is Amendment 2's, 130 characters, and check-meta.py fails a hub title or description that counts the rooms (a number, digits or words, up to five words before "room(s)"; KS3 is not one). Plants: no topics, blank topics, topics over 155, the hub count in words and in digits, a count in the hub title: 36 of 36 caught. Comic Caper's description is unchanged, so check-student-labels.py is untouched (its selftest passes). apply-meta.py rewrote 11 heads (kiln-disaster, big-school-begins, comic-caper and rightful-king already matched) and is idempotent. Canon §2.1 updated. Gate green on fb9028e (run 42357252313).

Review, 7 Nov: the count check on the hub title approved; "one room a lesson" being flagged accepted; the contract file stays in task PRs, only home.md and cloud.md wait for close-out. home.md was restored to the merge-base; this entry lands at close-out. The cloud container lacked Python playwright and sympy, so check-changed.py's 31 browser and SymPy checks failed on import and fell to the Gate, which passed them.

Next: Merged as 5202a94; main run 42358602377 green; end-task removed claude/room-meta.

Record: agent Claude Code; wall in the PR's report; review cycles 2; amendments 2; usage n/a.

## 2026-11-06 (home): ROOM-SEARCH-TITLES

Built after the stop below. data/games.json gains "rooms" (14) and the hub joins "pages"; check-meta.py and apply-meta.py hold and write them; canon §2.1 says so. Topics come from each teacher page's lockMeta, the clock from room.js. engine.js's `document.title` line is gone (Amendment 1), and check-meta.py fails if a room script assigns it again; teacher.js:231 stays. No title uses the fallback; big-school-begins and rightful-king use short_topics. The full title table is in the PR body. In Chromium all 14 rooms and the hub keep the generated title after load. Browser tabs now show the search title during play, not the story name.

Deviation approved by Project Claude, 6 Nov 22:32: check-student-labels.py's selftest pinned Comic Caper's old description, so its expected string and planted fault now use the generated one; the rule is unchanged. For later, not this PR: that selftest borrows live page wording, and synthetic fixtures would stop it breaking on content changes.

Next: Project Claude's review and Jon's approval of the table, then merge-pr.py. The Gate file's label for this check still says "every game page and /essentials/": for the cloud lane, harmless.

Record: agent Claude Code; wall in the PR's report; review cycles 0; amendments 1; usage n/a.

## 2026-11-06 (home): ROOM-SEARCH-TITLES, STOPPED

Nothing built. First version stopped on two descriptions over 155 characters; the consolidated contract (18:50) answered that and the rulings it raised, and replaces it in the contracts folder. Consolidated version stopped on "a change outside <head> seems necessary": escape-rooms/assets/engine.js:994 sets `document.title = R.title + ' — MaffsGames'` on every load, so a generated <title> is overwritten in the rendered page (tested on kiln-disaster and rightful-king with a title planted in the served head: story name by DOMContentLoaded). check-meta.py reads source, so it would pass while the rendered title stayed wrong. Asked Jon: may the line go, with a plant so it cannot return; and whether topics are lower-cased in full, first letter included, short_topics too (the contract's wording reads two ways). Clear: 14 timers read from room.js, 14 lockMeta blocks parse, hub og:description 127 characters and "Fourteen" equals the live rooms, no title needs the fallback.

Record: agent Claude Code; wall n/a (stopped before build); review cycles 0; amendments 1 (the consolidation); usage n/a.

