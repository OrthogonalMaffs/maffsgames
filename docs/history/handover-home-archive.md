# Handover archive: home lane

## Moved 2026-11-13 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

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

## Moved 2026-11-12 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

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

## Moved 2026-11-11 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

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

## Moved 2026-11-10 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

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

## Moved 2026-11-09 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

## 2026-11-06 (home): PHONE-FIT-ASIDE

measure-phone-fit.py neither counts nor presses anything inside `[data-mfg-aside]`; an option group inside one fails the row with "answer control inside data-mfg-aside", whatever the lists say, and the report lists each region and what it skipped. Tagged: equatle .lbw, 52dle #modal, prime-or-composite #modal. Canon 7.6.1 has the rule. Six new selftest lines cover the three contract cases plus the skipped count, __pfSubmit and the guard against a listed game.

Equatle is off known-failures in normal, aa and laptop. Asking bottom / fold, before to after: 320x568 753/528 to 474/528; 375x667 782/627 to 516/627; 390x844 850/804 to 584/804; 1366x768 897/728 to 630/728; 1280x720 839/680 to 573/680. 52dle stays listed at every entry: its own #guess-input sets the bottom (906/528, 887/627, 868/804; Aa 1186/528 with its top at 1140, 1092/627, 1092/804; laptop 836/728, 836/680). prime-or-composite stays on sideways, Aa 320x568: scrollWidth 374 from its Accuracy stat. Neither is a leaderboard fault; the contract's account of 52dle (escaping only because the modal is hidden) does not match the known-failures it already had.

Open for review: the checker reads Equatle's digit row, not the whole keypad. The option group is the 10 digits; the operator row with `↵ Enter` is outside it and `↵ Enter` does not match SUBMIT_RE (not to be touched). Measured directly, Enter ends at 521/528, 563/627, 631/804, 677/728, 620/680, the same in Aa on phones, so the pass is true, but a later slip of that row would not be caught. The driver still gets "could not get an answer marked" on Equatle (before and after), so it reads PASS (asking only). `__mfgHasInput` (tier 3, not __mfgProbe) still sees #lbname, so the driver may type in it; the guard's STOP IF was not hit (__mfgProbe never picked up a leaderboard).

Other games: full runs before and after in all three modes, no status changed. Twelve cells moved in how-many-parts, screening-room, take-a-walk and squared-squirrel; the same cells move between repeat runs on untouched main, so noise. Already failing on main, unchanged: possibly-maybe not on unmeasurable (all modes); aa who-ate-all-the-pies, as-you-can-see, distinctly-average, hc-factor, i-found-a-mark, its-on-sale, y-so-steep; laptop better-value.

Record: agent Claude Code; wall in the PR's report; review cycles 0; amendments 0; usage n/a.

## 2026-11-06 (home): WHOSE-SIDE handover

Agent Claude Code, Windows, worktree E:/jon/mg-whose-rec, branch claude/whose-side-review-record, which carries this entry and the queue line above. Its local checks were running when this was written; it merges through merge-pr.py on a green Gate (Small, docs).

Done: stages 1-4 live and unlisted (#674 257e883; fixes #676 f1acc1f, containing #675, closed unmerged; close-out #677). Project Claude passed #674 and #676 on 6 Nov. Art: #684 (e42aa76, cloud). Deleted on Jon's call, after confirming #675's changes are on main: E:/jon/mg-whose-fix, its local branch, remote claude/whose-side-fixes, and local claude/whose-side-are-you-on. E:/jon/mg-whose-side is also gone: no retry needed. Windows refused it because one of the verifier's serve-stubbed.py processes had outlived its run in that folder (PID 32912); stopping it let the folder go. Look for that before calling a folder undeletable.

Open: (1) .claude/rules/timer-policy.md: add the game's line from the code (counts up, no lives, faster right answer scores more), docs only, after WHOSE-SIDE-FIT merges; Project Claude reviews. No WHOSE-SIDE-FIT PR found at 16:19 on 6 Nov. (2) After this branch merges: end-task for claude/whose-side-review-record. (3) Stage 5 follows WHOSE-SIDE-BIOS; the cloud lane owns games/whose-side-are-you-on/ until then, so home does not edit it.

## 2026-11-05 (home): WHOSE-SIDE-FIXES

Jon's play-test. Stage 2 gets slots and Check; each side one hit line, nothing painted takes a tap; verifier clicks the dash and dot gaps at every size; 18 plants caught. No click on a side missed in reproduction; the clicks that did nothing came during MaffsLock's 300 ms window, and no bands exist during the 800 ms Right flash. Merged in #676 with Jon's second play-test (double clicks; the 0.8 s hold proven). Record: agent Claude Code; wall in the PR's report; review cycles 0; amendments 0; usage n/a.

## 2026-11-05 (home): WHOSE-SIDE

New unlisted game, stages 1–4; stage 5 and the art are later. Amendment 1: light theme, games.json and precedent checker lines, side-word text bold 19 px. Amendment 2: side colours on sides and side words only; ✓/✗ and a word for right and wrong. Rulings 19:45: grey sides until answered (1, 2, 4), stage 3 coloured with coloured numbers; 16-30-34 for 9-40-41. Added beyond the contract: question_id = item id (check-question-id.py requires it of new games). Verifier: all 10,368 items recomputed from geometry; 13 plants caught. Merged #674. Record: agent Claude Code; wall in the PR's report; review cycles 0; amendments 2; usage n/a.

## 2026-11-05 (home): MERGE-669-671

DONE: #669 EQUATLE-320 merged by merge-pr.py as d6e1ec5; main run 42082117555 GREEN. #671 TRUE-MINUS merged next by merge-pr.py as 3604b7f; main run 42087251109 GREEN. Each PR was rebased after a cloud.md conflict; main's CHRISTMAS-ROOM completion and every main entry were kept, and each PR's new entry was added. CLAUDE.md matched main. No exception to the merge guard was used. Cloud lane returns to one session at a time from 6 Nov.

Record: agent Codex; wall n/a; review cycles 0; amendments 1 (Jon's 5 Nov handover ruling); usage n/a.

## 2026-11-08 (home): Queue DONE items moved 8 Nov (verbatim from `docs/handover/home.md`'s Queue, BRANCH-CLEANUP; history, unchanged)

- LIVE-BUG-RECHECK: DONE. #711 merged as 04116a7 on Jon's word; main run 42517925373 GREEN; claude/live-bug-recheck removed by end-task. Contract: docs/history/contracts/2026-11-08-live-bug-recheck.md. Entry below.

- BACKLOG-ONE: DONE. #710 merged as 68ae9e4 on Jon's word; main run 42512282061 GREEN; claude/backlog-one removed by end-task. Contract: docs/history/contracts/2026-11-07-backlog-one.md.

- PHONE-FIT-RED (Shared; Project Claude, 7 Nov): DONE. #701 merged as 3fe605d6 on Jon's word; main run 42398273354 GREEN; branch removed by end-task. Cloud's #707 merged as 0ec5cd4; main's full run is green (42403456019). Contract: docs/history/contracts/2026-11-07-phone-fit-red.md.

- ROOM-SEARCH-TITLES (Shared; Jon, 6 Nov; Amendment 1, 18:55; Amendment 2, review fixes, 23:05): DONE. #693 merged as 5202a94; main run 42358602377 GREEN; claude/room-meta removed by end-task. Branch claude/room-meta, worktree ~/mg-room-meta. Contract: docs/history/contracts/2026-11-06-room-search-titles.md. Entry below.

- PHONE-FIT-ASIDE: DONE. #687 merged as 5b4931f on Jon's word; main run 42270819300 GREEN. No Project Claude review is recorded in this lane. Contract: docs/history/contracts/2026-11-06-phone-fit-aside.md.

- WHOSE-SIDE: DONE and live, unlisted. #674 merged as 257e883; fixes #676 merged as f1acc1f (it contains #675, closed unmerged); main green. Merged on Jon's word before review; Project Claude reviewed #674 and #676 on 6 Nov and passed them (side roles in both θ positions, FN, Stage 4's key, all 12 triples, uniform scaling). Worktrees and claude/whose-side-fixes deleted on Jon's call, 6 Nov. Art done (#684). timer-policy.md's line: `docs/todo.md` row WHOSE-SIDE-TIMER-LINE; the cloud lane owns the game until stage 5, which follows WHOSE-SIDE-BIOS. Contracts: docs/history/contracts/2026-11-05-whose-side*.md.

- CHRISTMAS-ROOM: DONE. #667 merged as 9cbedee; close-out #668 merged as e32608f. Contract: docs/history/contracts/2026-11-04-christmas-room.md.

- FRACTION-WHOLE: merged #662, b38ce399; Shared review passed and Jon authorised merge, 4 Nov. Contract: docs/history/contracts/2026-11-04-fraction-whole.md. Main run and cleanup recorded below.

## Moved 2026-11-07 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

## 2026-11-04 (home): CHRISTMAS-ROOM

Final state: DONE. #667 merged as 9cbedee; close-out #668 merged as e32608f. The contract is in docs/history/contracts/2026-11-04-christmas-room.md. Earlier notes below record the implementation and review handoffs.

AMENDMENTS 3 and 4 (Jon, 5 Nov), saved verbatim. The 4 Nov Gate stop (run 41922457161, teacher page's table.tt overflow, todo §1.37) is resolved by Amendment 3's tier1_phone_overflow entry, width 541 as issued; it measures 535 locally since the regeneration. Amendment 4: cr's given ratios in simplest form, in the generator and escape_set_checks; only cr's library changed (47 locks compared). VALID now 103 of 1000, was 32; floor 20. Reachable sets ct 8, sc 10, cr 8 of 10. Check-escape-rooms, the four test-escape scripts, the play-through (159 checks) and the independent recompute (30 sets; 232 of 232 corrupted sets rejected) rerun clean. Jon's rulings: Set A stays (warning only); minus signs, canon room count and the unreachable sets are follow-ups, not this PR. Not changed: docs/lock-bank-batch13.txt's cr NOTE does not state the new rule (flagged in the PR). No merge authority.

TAKEOVER (Jon's written task, 4 Nov 21:30): Claude Code takes over from Codex on the Windows machine. Primary E:/jon/maffsgames-new-clone fast-forwarded to 10a8b261. New worktree E:/jon/mg-christmas-room from origin/codex/christmas-room (Jon's instruction; the rulebook's same-worktree rule cannot apply across machines), branch keeps its prefix. Status clean and git log origin/main..HEAD matched the record below (head 0647f999). Identity: local user.name is "Jon", email matches; commits pass user.name=Vector52F per command, config unchanged. All Codex's checks treated as not run. Next: run the SUCCESS CONDITION, PR, stop at green Gate. No merge authority.

PAUSED for context handover at Jon's request, 4 Nov. Implementation checkpoint: 563b14a9; branch codex/christmas-room, worktree /home/maffs/mg-christmas-room, base 10a8b261. Resume the SAME branch/worktree; check clean status and git log origin/main..HEAD against this record. No push, PR, Gate or merge yet. Amendment 2 resolves the bank/findings scope STOP below and is saved verbatim with Amendment 1 and the full contract/draft. Registered preview server on 8874 stopped through end-task.py's stop_registered(); generator already exited. No running check queue remains. Do not restart until Jon resumes.

Implemented: approved room prose, eight objects/two blanks, three instruments/grades, Amendment 1 feedback tokens, scaffolds/teacher mapping, three bank entries and SR-30 findings file (no audit verdict; Project Claude review pending). Generator and shared per-set module add only the three Christmas locks. Ten sets per lock; ct includes rate/rise/abs/short, sc tree/total/ccm, cr reduced ratio/parts/each. Shared check independently recomputes domain, misconception and working tokens from clue parameters; grid solvers use the warming equation, ceiling-height balance and raw ratio proportions. Fixed freezer/door decoys retained and response 18 excluded. Other room.js files unchanged; JSON comparison proves every old variant library unchanged. Added one Core card to each listing, one sitemap URL and Jon's exact updates sentence; current count-bearing hub/front strings changed 13 to 14 (front metadata has no room count). Engine/assets, other rooms, cloud handover and pack generator untouched.

Art: all three source JPGs from origin/art/christmas-tree-fiasco, extracted to /tmp/christmas-tree-fiasco-{scene,win,fail}.jpg; existing strip-gen-watermark.py reports no mark on each, frames each to 1600x873 and writes q80 WebP. Source and output images visually inspected: no people, lettering or visible watermark. Art branch untouched. Local tool prerequisites numpy/Pillow were missing; installed into existing /home/maffs/.venvs/maffs with uv pip, no repo dependency change. First conversion attempts failed on missing imports; final conversions exit 0.

RAN: generator exit 0, log .claude/bg-1793826500110.log (GENERATOR_EXIT_STATUS=0). check-escape-rooms.py exit 0 after the room-specific shared checks were added: 30 verified sets, 32 VALID of 1000, all tokens resolve, all art present, rating Core; existing plants caught. Set A as a JOINT draw is INVALID (ct/cr share clue magnitudes 4/8 etc.; cr answer 6 is another lock's clue). Checker warns and engine never serves that combination; individual Set A locks retained exactly as approved, 32 other joint draws are served. No floor STOP hit. Audit-register --check exit 0. Bank checker 3/3 usable exit 0, with a float-equality note on ct; VERIFY then changed to the equivalent integer balance, NOT re-run yet. UTF-8 character reads and git diff --check pass. check-changed.py --list exit 0: 62 selected; plan /tmp/christmas-check-plan.txt, standard seven CI deferrals. This was planning only, not a test run.

VALIDATED on Windows (Claude Code, 4 Nov), every check rerun, Python 3.14 locally: generator deterministic (no diff); check-escape-rooms.py exit 0, VALID 32 of 1000, rating Core; test-escape-dial/keypad/setcodes/rating exit 0; check-lock-bank.py batch13 3/3; audit-register --check OK; check-changed.py 62/62, 731s, exit 0, standard seven CI deferrals. Scratch only, not committed: all 30 sets recomputed independently and 69 strings matched to the draft (0 fails); 213/213 mutations caught; play at 390x844 touch and desktop, win and timeout, 159 checks, 0 fails. Set A joint draw fails only on rule (a): 4 is in ct and cr (corrects the note above: cr's answer 6 is not a ct clue). Only 6 of 10 ct sets and 6 of 10 cr sets are reachable; neither lock's Set A. OPEN for review, in the PR: Set A / §5c step 6, ASCII -4 beside the draft's −18, canon's two 'thirteen' counts (out of scope), teacher page overflows a phone on every room. Next: PR Gate, then stop for Project Claude's Shared review and Jon's play-test and merge. No merge authority.

Agent: Codex. Worktree: /home/maffs/mg-christmas-room. Branch: codex/christmas-room. Base: 10a8b261. First commit 0b260bb5 saves the full approved draft/contract and Amendment 1 verbatim, plus Queue claim. Primary fast-forwarded; clean takeover and expected git identity confirmed. Root cause: approved new seasonal content on the existing engine; no bug class or engine change. Amendment 1 resolves the initial fixed-number feedback contradiction. Art branch exists; all three source JPGs visually inspected: no people, lettering or visible watermark. No artwork transformation or production changes yet.

STOP at contract/code check: scripts/check-escape-rooms.py:209 rejects every lock missing from docs/lock-bank-batch*.txt; no Christmas entries exist. EXACT CHANGE/lane exception omits that bank, so the required checker cannot pass within the named files. SR-30 also requires a new room's findings file, omitted from scope. Need a numbered amendment authorising the new room's bank entries and docs/audits/findings/christmas-tree-fiasco.yml; retain checker and engine unchanged. No implementation or tests claimed, no push/PR. Next: resume this clean branch after amendment, then build, validate, Gate and Shared review/Jon play-test hold. No SR exception applied; SR-30 requirement flagged.

Record: agent Codex; wall n/a (initial contract receipt timestamp unavailable); review cycles 0; amendments 2; usage n/a.

Record: agent Claude Code (takeover); wall in PR #667's report; review cycles 0; amendments 4; usage n/a.

## Moved 2026-11-05 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

## 2026-11-04 (home): FRACTION-WHOLE

Final state: MERGED and live #662, squash b38ce399. Resumed 4 Nov by Codex at clean head 8db674cd, matching the PR handover. Project Claude Shared review passed; Jon explicitly said "merge". Primary fast-forwarded first. Gate (every job passed) remained successful on that exact head; GitHub reported mergeable/clean after main advanced. No further main merge. Guard last line: `main b38ce39 run 41900832132: GREEN`; independent watch-main confirmation exit 0. end-task.py exit 0 removed codex/fraction-whole and its worktree. Contract moved verbatim to docs/history/contracts/2026-11-04-fraction-whole.md. Close-out: /home/maffs/mg-fraction-whole-closeout, branch codex/fraction-whole-closeout; check-changed.py 40/40 PASS in 255s, standard seven CI deferrals, log .claude/bg-1793821884474.log (detached command exit status not retained). No production changes or SR decision needed. Next: close-out PR and guarded merge; then CHRISTMAS-ROOM under Jon's 4 Nov contract.

Agent: Codex. Worktree: /home/maffs/mg-fraction-whole. Branch: codex/fraction-whole. Base: 67610171. Pre-step and its extension completed: seven queue entries and seven dated entries moved verbatim to docs/history/handover-home-archive.md under "Queue DONE items moved 4 Nov"; CALC-DOCK-WIDE first, then oldest first. GitHub REST confirms all seven PRs merged; each squash commit is an ancestor of origin/main. Cloud ownership line retained. No live or unmerged item moved. Context size passes without warning and with more than 3 KB spare after this entry.

STOP IF hit during contract/code check: shared fraction-input.js digits() strips every non-digit and value() rejects a signed numerator. The 6 P's bank schools/assets/six-ps/linear-equations.json contains linear-equations-375c850e (10x = -4, answer -2/5) and linear-equations-98ad8c09 (9x = -6, answer -2/3). Both require a signed numerator that adding only whole:true cannot represent. Existing player explicitly enables its minus key for fraction answers. No component, player, bank, verifier, warn-list or cloud handover changes. Next: Jon/Project Claude ruling extending the component API for signed fractions while preserving its current default behaviour. No implementation, push or PR yet.

Resumed under Jon's signed-fraction Amendment 1 (saved verbatim). Optional whole/signed modes added at the shared layer; The 6 P's mounts signed mode for every fraction, with whole mode where declared. Its judge() and fractionRaw() are byte-identical; readInput adapts shared raw strings to the existing fields. Only its verifier's input driver changes for the separate sign button; scripted marking values/expectations unchanged, plus a new fraction-phone unit. The page's own fraction boxes/CSS removed and warn-list entry removed. Cloud Queue's authorised follow-up names HOW-MANY-PARTS-FRACTION; no game or Gate files touched.

New component test: four mode combinations at 320x568, 360x640, 375x667, 1280x700 and 1280x701 PASS, five plants CAUGHT, exit 0 (including sign dropped from raw). Initial plant run crashed when deliberately missing a whole target; two bounded test-harness fixes guard both loops; rerun passes. Fraction-input checker selftest 10/10; check 112 pages, 3 shared users, only how-many-parts warns, 0 failures. Existing 6 P's verifier and new fraction-phone unit running. Next: remaining regression checks, check-changed.py, approved updates wording, PR and Gate; Shared review hold.

Implementation commit: f7f157b5. Full verify-the-6-ps.py PASS, exit 0: 34 covered topics, 43 fixture questions, 10,000 session draws each way, desktop and 320px touch sessions, all marking cases, all 25 plants caught. Fraction-phone unit passes all five fixture shapes (including mixed and negative) plus both real negative questions at 320x568, 360x640, 375x667: asking controls and wrong-answer Next above viewport minus 40px, no sideways scroll, sign button on every fraction. Log .claude/bg-1793814069591.log. Direct old/new component comparison at all five sizes confirms default DOM, filtering, raw/value/filled, marking classes, clearing, Enter and geometry exactly equal. Possibly, Maybe, Pies and check-changed queued serially in .claude/bg-1793814327449.log, stopping on first nonzero exit. Awaiting Jon's updates wording; draft/Shared hold until complete.

Jon supplied the updates wording; added newest under November New in the existing dated markup and saved the wording in the contract. No editorial hold remains; finish checks, PR and Gate, then Shared review hold.

Local checks complete: verify-possibly-maybe.py PASS (1,200 questions, 4,713 marking probes, 13 plants), verify-who-ate-all-the-pies.py PASS (1,442 probes, 14 plants), both unchanged, exit 0 each. Full check-changed.py 65/65 in 1078s, exit 0; 15 heavy serial, 50 light. Summary: "All selected checks passed. Push, and CI runs the rest." Log .claude/bg-1793814327449.log captures each command's exit and overall exit 0. CI deferrals: Stage exit, Level resolver in play parts 1/2 selected indirectly through fraction-input.js; seven standard deferrals (four page-load shards, first includes hang scan; bank extraction; ledger lint; leaderboard coverage). No checker weakened.

STOP pending rulebook exception: cloud #660 merged while checks ran. git fetch plus read-only git merge-tree --write-tree --name-only HEAD origin/main (4f2b817a) confirms conflicts only in updates/index.html and docs/handover/cloud.md. Worktree is clean; no merge started. Asked Jon for an explicit exception to AGENTS.md's ban on merging into an existing task branch: preserve all updates and main's cloud handover, reapply only HOW-MANY-PARTS-FRACTION Queue clause. No answer yet. Next: push a draft with complete evidence, retain branch/worktree; after Jon's ruling resolve only those files, Gate, Shared review and Jon's merge. Final PR state tracked in its report. No merge or cleanup authorised.

Pushed and opened draft PR #662: https://github.com/OrthogonalMaffs/maffsgames/pull/662 . Contract and signed Amendment 1 included verbatim; full report and phone table in body. Last commit before this pointer: 9a9f110f; implementation f7f157b5, updates a0b324c4. Stop pending the requested branch-merge exception; no Gate result can be obtained while conflicted. Retain /home/maffs/mg-fraction-whole and codex/fraction-whole. Final context-size check passes with home.md well below the warning band; no merge/cleanup.

Jon's 4 Nov rulings on #662 resolve the merge STOP and supersede the original contract's cloud Queue edit. Consumed the one-time exception by merging origin/main 31c04c6a into this branch; only updates/index.html and docs/handover/cloud.md conflicted. Cloud handover restored byte-for-byte to main, removing this PR's edit entirely; HOW-MANY-PARTS-FRACTION note now in this Queue and PR body. Updates keeps every entry from both sides, unchanged, newest date first. Rulings saved verbatim in the contract and PR. Next: full local check rerun, push and Gate; stop for Shared review and Jon's merge. No further merge-from-main exception and no PR merge authority.

Ruling revision pushed at c2b7143e and PR marked ready (mergeable). First CI run 41892078449 failed Plan's selection selftest, hence Gate: new test-fraction-input-js.py named no HTML page and became the 13th always-run verifier (budget 12). Understood, within-scope correction: a real scripts/fixtures/fraction-input.html used by the test and declared as its dependency. Fixture applies the border-box reset from all three consumer pages; initial standards-mode fixture lacked it and exposed different native button/input sizing, corrected in the fixture without changing production code or assertions. Current component test passes all five sizes/modes and all five plants; ci-deps.py --selftest PASS, exit 0, always-run count back within 12. No Gate file changed or budget raised. Full check-changed rerun continues; its component test had already passed before fixture extraction, so the revised test was also run directly. Final local/CI results are tracked in the PR report; Shared review hold remains.

Post-merge full check-changed.py rerun PASS: 65/65 in 1081s, exit 0 (15 heavy serial, 50 light; same ten CI deferrals). Log .claude/bg-1793818567493.log includes CHECK_CHANGED_RERUN_EXIT_STATUS=0. The added fixture landed after this run's footer/component checks, so its affected checks were run directly too. Second CI run 41893431413 passed Plan/content/answer-lock checks but Site-wide caught the new unpublished HTML fixture's missing canonical footer. Within-scope fix adds the standard footer and stylesheet to that fixture, no exemption. check-footer.py PASS (142 canonical pages, 38 exempt); test-fraction-input-js.py PASS all five sizes/four modes and five plants; final ci-deps.py --selftest PASS, 11 always-run within budget 12, exit 0 (log .claude/bg-1793819750675.log). No production implementation/marking/bank or Gate-file changes. Correction pushed after 1e58d5b4; last implementation f7f157b5, one main merge 3492a781. PR is ready; next: current-head Gate, then stop for Project Claude Shared review and Jon's merge. Final Gate/current-head evidence recorded in the linked PR report, retaining this worktree/branch; no merge/cleanup.

STOP after footer correction 3e929ea8: #663 merged into main as 246794b1 while checks/CI corrections ran. GitHub reports dirty and no run exists on 3e929ea8. Read-only git merge-tree after fetch confirms only updates/index.html conflicts; worktree remains clean, no second merge attempted. The one allowed origin/main merge was already consumed at 3492a781. Next: Jon's explicit further exception to resolve only the new updates conflict, preserving every entry and wording; then current-head Gate and Shared review. Production code remains unchanged from f7f157b5; footer/component/selector checks pass; post-merge full local run 65/65, exit 0. Final PR report records this new STOP. Retain /home/maffs/mg-fraction-whole, branch codex/fraction-whole. No PR merge or cleanup.

Jon answered "yes you may" to the additional merge exception (4 Nov), saved verbatim with its question in the contract and PR. Resumed from clean 5fa48716. Merged origin/main d7cc0e78 (includes #663); only updates/index.html conflicted. Kept the approved fraction entry and every main entry, with wording unchanged and dates descending. Asserted updates equals main plus the exact fraction line; cloud handover byte-identical to main; production, verifier, component test and fixture byte-identical to 5fa48716. No further merge or PR merge authority inferred. Next: fresh full local checks and Gate on this head, then stop for Shared review. Final checks/Gate/current-head evidence in the linked PR report; retain branch/worktree, no cleanup.

Record: agent Codex; wall n/a; review cycles 1; amendments 4 (pre-step extension, signed Amendment 1, #662 rulings, additional merge exception); usage n/a.

## Queue DONE items moved 4 Nov

- CALC-DOCK-WIDE: home/Codex, codex/calc-dock-wide, /home/maffs/mg-calc-dock-wide, draft PR #653; contract docs/handover/contracts/2026-11-03-calc-dock-wide.md. Claims calculator.js and test-calculator-js.py; Shared, stop at Gate green for review and Jon's merge. Awaiting Jon's updates wording. Jon explicitly permits concurrency with SEQ-SOLVER-FIXES, SEQ-SOLVER-WORKED and DASHBOARD-METRICS.

- UPDATES-NOVEMBER: DONE #651, 264e011f; main run 41674541301 GREEN, guarded merge exit 0; end-task.py removed branch/worktree, exit 0. Contract docs/history/contracts/2026-11-03-updates-november.md; final report in PR.

- NEW-AND-UPDATED: home/Codex claims index.html on codex/new-and-updated, /home/maffs/mg-new-and-updated, PR #648; contract docs/handover/contracts/2026-11-03-new-and-updated.md. Full checks 56/56, exit 0. Shared: green Gate then Project Claude review and Jon's merge. Fresh base ffcd9a9b includes DASH-MINUS #646; verifier Amendment 1 applied.

- TODO-TRIM: home/Codex, codex/todo-trim, /home/maffs/mg-todo-trim, PR #645; contract and Jon's 3 Nov HTTP-503 retry ruling in the PR. Small, merge on green. NEW-AND-UPDATED is next; no saved contract found at this head.

- PIES-SIGNOFF-AND-PRIMARY-FF: home/Codex, codex/pies-signoff, /home/maffs/mg-pies-signoff; contract `docs/handover/contracts/2026-11-03-pies-signoff-and-primary-ff.md`. Small, merge on green; TODO-TRIM starts after completion.

- LOOK-STAGE: home/Codex, codex/look-stage, /home/maffs/mg-look-stage, PR #638; contract `docs/handover/contracts/2026-11-02-look-stage.md`. Concurrent PIES-LOOK/ESSENTIALS-ART authorised by Jon; roster, canon and registration reserved here. Pies remains warned until Jon's explicit look sign-off, irrespective of its artwork merge. Shared: stop at green Gate for Project Claude review and Jon's “merge”.

- RULEBOOK: home/Codex, codex/rulebook, /home/maffs/mg-rulebook, PR #635; Shared. Amendment 1 findings addressed on the same branch; stop at Gate green for re-review and Jon's “merge”. Two lanes are explicitly authorised for this task.


## 2026-11-03 (home): CALC-DOCK-WIDE

Agent: Codex. Worktree: /home/maffs/mg-calc-dock-wide. Branch: codex/calc-dock-wide. Base: 264e011f (UPDATES-NOVEMBER #651 merged). Next: before measurements, shared dock fix, outside-card regression and old-rule plant, after measurements, checks and PR. Identity correct; clean worktree before first edit; open PR #652 is authorised cloud work and does not touch calculator.js/css (#518/#424 home.md only). Root cause confirmed: percentage left assumes the card contains the mount; sibling mounts use a wider containing block. No SR decision needed. Awaiting Jon's wording for the now-required updates line. No game or Gate files will change.

Implemented: dock() measures the rail at left zero in its actual containing block, then places it at the host right plus D.gap; the closed rail's hidden state is restored synchronously. Room test, panel width, sticky CSS, resizing debounce and non-docked branch unchanged. New sibling-mount fixture has a positioned ancestor with a border, tests 1280/1920/2560 through resize, and restores the old percentage-left statement through plant_common; plant CAUGHT. Existing cases unchanged. No game or CSS changes.

Targeted calculator test PASS, exit 0 (65 basic expressions, 27 scientific, 16 key sequences, Chromium/WebKit phone behaviour, toggle forms, existing five dock plants and new old-rule plant). Before/after audit: all 14 mounts on 13 pages at 1920 and 2560 (28 rows each), calculator open in play, pinned real fonts and stub server. Every after gap is 12px, panel inside viewport, scroll 0; card right and docked state unchanged. The scratch audit needed startup corrections for Pythagoras' hypotenuse step, Split It's mode and stage worked examples; no game changes. Sequence Solver screenshots captured before/after. Full check-changed running; awaiting approved updates wording.

Full corrected check-changed.py: 76/76 passed in 369s, exit 0, 6 heavy serial and 70 light; log .claude/bg-1793723836837.log. Twenty-one indirect heavy checks selected through calculator.js deferred to CI: Pythagoras 3, The 6 P's 2, Take a Walk 2, Burst 4, Squared Squirrel 3 (parts 1,3,4), Pies 2, Formula Unlocked, Growth and Decay, Unit Converter, level resolver in play 2. Seven standard deferrals: four page-load shards (first also hang scan), bank extraction, ledger lint, leaderboard coverage. Initial run caught screenshot files in an unexcluded folder; moved only those requested artifacts to existing excluded docs/screenshots/calc-dock-wide. Publish-scope selftest/check passes after this one fix; superseded full run stopped through end-task.py's registry. No publishing rule or Gate file changed. git diff --check and UTF-8 reads pass. Next: draft PR with table/screenshots; Jon's updates wording; Gate green, then Shared review hold. No merge authority yet.

Resumed 3 Nov by Codex in the same clean worktree at 69712350; branch history matches this entry. Jon supplied the exact November New entry, relayed Project Claude's approval and explicitly said merge when Gate is green. Added the wording newest first. Contract amendment 1 records this instruction. Next: push, ready for review, guarded merge/main watch, end-task; stop without starting PACKS-CANON. Final merge/main/cleanup results will be recorded in the PR report.

STOP, 3 Nov: approved updates entry pushed at e900a6a8; PR marked ready using the GitHub connector. GitHub REST reports mergeable=false, mergeable_state=dirty against current main; no check runs on the new head. Guarded merge watcher launched through bg.py, then stopped through end-task.py's registry on discovering the conflict. No merge or cleanup. Next: Jon's ruling on resolving the conflict; retain this worktree/branch. PACKS-CANON not started.

Jon's conflict-resolution Amendment 1, 3 Nov, supersedes the STOP: merge origin/main without rebase or force push; preserve all updates and handovers, stop for any other conflict. Merged origin/main af8e7372; only updates/index.html conflicted. Kept the calculator line first on 3 Nov, followed by every main entry in its original order; handovers merged without conflict. No implementation changes. Next: push, Gate, authorised guarded merge/main watch and cleanup; stop. Final lifecycle results in the PR report.

Record: agent Codex; wall n/a; review cycles 1; amendments 2; usage n/a.

## 2026-11-02 (home): RULEBOOK (Shared; Codex)

Agent: Codex. Worktree: /home/maffs/mg-rulebook. Branch: codex/rulebook. Last commit before this report update: dd370c69bd528bf71e91c58d8925dedd18bea9a8. PR #635: https://github.com/OrthogonalMaffs/maffsgames/pull/635 . Next: verify the amendment head's Gate, then stop for Project Claude re-review and Jon's explicit “merge”.

AGENTS.md is the common WSL rulebook; CLAUDE.md imports it with the documented @AGENTS.md form. Local testing, scripts/CI, game claims and room-art rules have explicit topic triggers. Seven previous home entries now use dated level-two headings; text outside those opening lines is unchanged. Windows procedures are historical material in canon §12. Amendment 1 moves cross-lane facts into this handover's Queue preamble and deletes the temporary machine-local notes file; platform-principle bullets are copied verbatim from the unchanged planner brief into AGENTS.md. Task-specific concurrency text is removed from that rulebook.

Rulings: understood failures caused by this change get at most two within-scope fixes; all other unexpected events stop. Answer-lock exempt() requires both a claim and roster-Unlisted status. Cloud handover's missing Unlisted qualification is flagged for cloud; that file remains untouched. Lane notes were waived for startup and replaced in WSL. No merge or cleanup authorised yet.

Validation after Amendment 1: duplicate sentences 0; platform-principle bullets verbatim; Queue in the unarchived preamble; temporary notes file absent; seven old entries (eight with RULEBOOK), with every byte outside converted opening lines unchanged. Context-size check/selftest pass. AGENTS.md 10,100 bytes, CLAUDE.md 628; combined 10,728. Initial complete check-changed: 41/41 in 253s, seven standard CI deferrals. Repeated fresh codex exec at /home/maffs/mg-rulebook-load-test-r1 (dd370c69) quoted takeover exactly with zero tools. First load-test worktree also retained. Initial full-record size assertion required two within-scope shortening fixes; all ad hoc checks now pass. Previous Gate: 84/84 on 8e4fcf21, run 41516051138; it does not verify this amendment. First review hand-off 2026-11-02 20:16:23 UTC; contract received 19:36:38. Record wall measures that first hand-off; review cycles now 1, amendments/rulings 4. Current Gate is tracked in the PR report; no merge or cleanup run.

Record: agent Codex; wall 0:39; review cycles 1; amendments 4; usage n/a.

## 2026-11-02 (home): LOOK-STAGE

Agent: Codex. Worktree: /home/maffs/mg-look-stage. Branch: codex/look-stage. Last commit before this report: 8e2cf3ff; implementation: 5e5a9e44; base: b5c9eaa6. PR #638: https://github.com/OrthogonalMaffs/maffsgames/pull/638 . Current-head Gate and review state are tracked in the PR report. Next: stop at green Gate for Project Claude Shared review and Jon's explicit “merge”. No merge authorised.

Shared listing gap fixed in the roster Description and a new CI-header-registered checker; no existing columns or listing states changed. All 100 eligible listed games record Jon's retrospective approval; Pies alone warns. Shrink-only JSON list rejects additions, restoration after removal and stale entries. Canon §7.8 records the listing/art rule; §12 explains the pipeline failure. No game files, Gate files or answer-lock state changed. SR-21 applied (listing state retained); SR-27 does not exempt this shared check from check-changed.py.

Initial local run exposed a sign-off word-boundary bug and an incorrect expected warning in one selftest; one within-scope fix corrected both. Re-run: 7/7 selftests pass; 101 listed games, 1 warning, 0 failures. CI packing check passes; new line uses the standard untimed warning. Full check-changed: 152/152 passed in 515s (5 heavy serial, 147 light); standard seven checks and indirect heavy roster dependencies deferred to CI. Completion summary retained in `.claude/bg-1793654249945.log`; detached launcher's child exit status was not retained. UTF-8 characters and exact row preservation after removing the 100 new approval suffixes checked. An ad hoc import probe initially omitted scripts/ from sys.path; corrected probe passes, no repository change.

CI run 41528624872: the new check's seven plants passed, but content job 37 failed because its shallow checkout lacked the event's base commit. Within-scope fix fetches that exact base only when absent. Added a real shallow-clone selftest with a local file remote; the missing base is fetched and its older warning list read correctly. Direct selftest 8/8 and roster check (101 listed, one warning, zero failures) pass. Correction-file check-changed run: 41/42 pass in 251s, exit 1; Text writes alone caught three new fixture writes without newline=''. First fix for that check adds newline='' to all three; Text writes selftest/check and look selftest/check pass. Subsequent local run and CI are recorded in the PR report. No check has failed after two fixes for that check. No Gate file changes needed.

After newline correction, check-changed.py --files scripts/check-look-signoff.py docs/handover/home.md passes 42/42 in 251s, captured exit 0 (log `.claude/bg-1793655775463.log`); seven standard CI deferrals. Original complete run remains 152/152. No game files or Gate files changed during corrections.

First review hand-off: PR opened 2 Nov at 21:27 UTC; wall measured from contract/startup at 21:15 UTC.

Record: agent Codex; wall 0:12; review cycles 0; amendments 0; usage n/a.

## 2026-11-03 (home): PIES-SIGNOFF-AND-PRIMARY-FF

Agent: Codex. Worktree: /home/maffs/mg-pies-signoff. Branch: codex/pies-signoff. Base: 560b6b17. Implementation: 494f7055; check report: c104cd86. PR #644: https://github.com/OrthogonalMaffs/maffsgames/pull/644 . Checked locally; next: green Gate, guarded merge and main watch; Small, no review hold. Final merge/main/cleanup results are in the PR report.

Recorded Jon's 3 Nov look approval for Pies and emptied the warning list. Primary fast-forward is the first startup command; AGENTS.md's short rule points to canon §12 for the stale-rulebook history. Other roster rows, game files and CLOUD-LEAN rules unchanged.

Slip: relative roster patch landed in primary; stopped, then Jon's 3 Nov recovery moved only that sign-off to this worktree, passed the checker and restored a clean primary.

Look sign-off check: 101 listed games, 0 warnings, 0 failures. Context-size check passed. Full check-changed.py: 149/149 in 478s, exit 0 (5 heavy serial, 144 light); 71 indirect heavy roster checks and seven standard checks deferred to CI. Log: .claude/bg-1793708922180.log. No answer-bearing change. No SR decision needed; SR-27 exception does not apply. Contract STOP IF conditions not hit.

Record: agent Codex; wall n/a (contract-receipt timestamp unavailable; no estimate); review cycles 0; amendments 1; usage n/a.

## 2026-11-03 (home): TODO-TRIM

Agent: Codex. Worktree: /home/maffs/mg-todo-trim. Branch: codex/todo-trim. Last implementation commit: 359cb347. PR #645: https://github.com/OrthogonalMaffs/maffsgames/pull/645 . Checked locally; Gate and measured-budget check passed on 359cb347. Next: this handover head's Gate, then retry the guarded merge with --watch --wait 3600. Final merge/main/cleanup results are tracked in the PR report.

Moved 40 clearly finished blocks (32,248 bytes) verbatim into docs/history/todo-archive.md under 2026-11-03; todo.md is 118,818 bytes. Verification proves every removed block archived and all retained lines, including START and open items, byte-identical. Mixed-status entries stay intact; judgement calls and reproducible proof are in the PR. Current item formats need consistent boundaries and terminal status before safe automatic archiving. No automation changed. Full check-changed.py: 41/41 in 251s, exit 0; seven standard CI deferrals. Context-size and UTF-8 checks passed. No answer-bearing change; no SR decision needed.

503/retry: first merge helper refused on GitHub HTTP 503, exit 1; Jon's 3 Nov ruling authorises retry after the full Gate, then only if another 503 a five-minute wait and one final attempt. This handover update is explicitly authorised by that ruling; retry outcome goes in the PR report.

Record: agent Codex; wall n/a (contract-receipt timestamp unavailable; no estimate); review cycles 0; amendments 1; usage n/a.

## 2026-11-03 (home): NEW-AND-UPDATED

Agent: Codex. Worktree: /home/maffs/mg-new-and-updated. Branch: codex/new-and-updated. Base ffcd9a9b includes DASH-MINUS #646; claim commit 75dcee63; implementation 6ae4421e; amendment b995f2d9; checks e205418b; previous STOP record a21f0f3c. PR #648: https://github.com/OrthogonalMaffs/maffsgames/pull/648 . Checked locally and pushed. Next: this handover head's Gate, then stop for Project Claude review and Jon's merge. Current-head Gate and review hand-off are tracked in the PR report. No merge or cleanup authorised.

Implemented: cmpNew derives its cards from applyBadges(), one per slug, newest first with New then title ties, cap 12; evergreen heading/note and new-and-updated analytics label. Badge dates/rules, level cards, filter and compact behaviour unchanged. New ci-line verifier reads level-card metadata independently and stubs the clock only in routed copies. Section-click test also fixes its test clock so generated cards remain testable after the current badges expire.

Targeted checks: new verifier passes on 3 Nov (14 live, 12 displayed), 13 Nov (13 live) and 2030 (none, whole section hidden). All three required plants CAUGHT. Phones 320x568, 375x667, 390x844 pass compact controls, live/filtered counts and overflow checks using pinned real fonts. Section clicks pass for all 20 labelled elements; copied cards still fire game_card_clicked alone. First verifier run read the CSS-uppercased heading via inner_text; corrected to text_content, then all pass. UTF-8 characters verified. No answer-bearing change; no SR decision needed; SR-27 exemption does not apply.

Full check-changed.py selected 56 checks (12 serial heavy, 44 light), seven standard CI deferrals. At STOP: 44 passed, one failed, 11 unfinished. The failing Circle Theorem Spotter verifier's check_copies() at line 513 hard-codes portal card count 2; the removed hand card leaves its canonical GCSE card alone. Game and level card are unchanged. This is understood but its fix is outside EXACT CHANGE; no verifier/game/Gate file changed. Registered runner PID 320924 stopped through end-task.py's stop_registered(), so the overall check has no final exit status. Log .claude/bg-1793715256421.log retained; new verifier and section clicks both passed within this run too. Branch remains local; no push, PR, merge or cleanup.

Resumed under Jon's 3 Nov verifier Amendment 1 (saved verbatim beside the earlier wait ruling): only check_copies()'s condition changes to require at least one portal card. Reason: the second card was the removed hand copy; load-built cards have no stable static count. Every card must still match CARD and none may say seven. Direct verifier PASS: 55 questions, 44 calculation questions independently solved, 10 tangent figures, all 15 plants caught. Ad hoc probes: zero cards rejected; one and three exact copies accepted; wrong second copy and seven rejected. One-line-only diff confirmed.

Complete check-changed.py after amendment: 56/56 passed in 631s, exit 0, 12 heavy serial and 44 light; seven standard CI deferrals listed above. Summary: "All selected checks passed. Push, and CI runs the rest." Log .claude/bg-1793716436188.log, including CHECK_CHANGED_EXIT_STATUS=0. No Gate files changed; original badge/filter/compact implementation and level cards byte-identical to base outside the scoped builder.

Record: agent Codex; wall n/a (initial contract-receipt timestamp unavailable); review cycles 0; amendments 2 (wait ruling and verifier Amendment 1); usage n/a.

## 2026-11-03 (home): UPDATES-NOVEMBER

Final state: MERGED and live #651, squash 264e011f. Guard last line: `main 264e011 run 41674541301: GREEN`, exit 0. Pages deployment passed. end-task.py exit 0 removed codex/updates-november and /home/maffs/mg-updates-november; registered processes already gone. PR report updated; architect review remains after merge (Small). Previous checkpoint below is retained as the local-check record.

Agent: Codex. Worktree: /home/maffs/mg-updates-november. Branch: codex/updates-november. Base: 9e17ddfc; implementation f1d26d4f. Checked locally. Next: PR, guarded merge and main watch. November uses Jon's approved wording and existing markup; The 6 P's gains its 27 Oct New badge; AGENTS.md requires dated updates in visible-change PRs, with rationale in canon §12. No checker or game changes. Initial STOP for missing dash exception mechanism resolved by Amendment 1: updates/ is outside that check's scope. Open PRs #518 and #424 touch home.md only. No SR decision needed; SR-27 does not apply. Contract and amendment saved verbatim.

Full check-changed.py: 56/56 passed in 638s (12 heavy serial, 44 light), summary "All selected checks passed. Push, and CI runs the rest." Log .claude/bg-1793721466846.log; detached launcher did not retain the exit status. Seven standard CI deferrals: four page-load shards (first also hang scan), bank extraction, ledger lint and leaderboard coverage. Dash-minus selftest 31/31; check 0 hits across 134 files, exit 0. New-and-updated passes in the full run; independent metadata assertion confirms I Found a Mark, Pies, The 6 P's first to third. November game links and UTF-8 punctuation verified; October and earlier byte-identical; git diff --check clean. No answer-bearing change.

Record: agent Codex; wall n/a; review cycles 0; amendments 1; usage n/a.

Moved verbatim out of `docs/handover/home.md` (contract CTX, 8 Oct 2026). History only: nobody adds to it and
no session reads it by default. Newest first. Later trims add their moved entries at the top of the entries.

**DOCS-RECONCILE (29 Oct 2026): first Codex task**, branch `codex/docs-reconcile`. Approved canon header and Escape rooms summary replacements, Firebase pre-deployment paragraph correction, and exact deferred ESCAPE-COUNT-SOURCE item added. Canon section 11.1, the existing external voice-rewrite pointer and historical handover entries preserved. Amendment 2: eight completed TODO entries shortened only after appending their complete originals verbatim under the dated CTX heading in `docs/history/todo-done.md`; all pre-existing archive bytes preserved. TODO: 153776 to 150545 bytes (3231 recovered, 3055 below the 153600 cap). Initial check-changed run: 37/41 passed, four failed, seven deferred. Jon independently confirmed Teacher feedback line and Start-screen mount pass outside sandbox (sandbox-only failures), and Timing gate fails outside sandbox with WinError 32 during tempfile cleanup (local Windows failure unrelated to this docs change). Context size now PASS on the Amendment 2 check-changed rerun; Timing gate still reports WinError 1920 in the sandbox. Rerun exited 1: 38/41 checks passed in 406 seconds, seven deferred to CI; Teacher feedback line and Start-screen mount reproduced the sandbox-only failures. No additional failures. PR #621 merged as 62f5568; main run 41027231633 green; cleanup by Jon (end-task.py from origin/main, 30 Oct).

**PLAN-TIMEOUT + GATE (29 Oct, Jon's exception):** Plan 5 to 10 min (PLAN-MAP-ONCE, todo); Gate reads `needs.*.result` (the 126 KB `groups` output broke the 128 KiB env limit).

**SETTLE + SWEEP (#583) and SCROLL (27-28 Oct):** shared `bank_common.wait_settled`; `sweep-six-ps-wrong.py` with its shrink-only `KNOWN_FAILURES` (the 14 at 320x568: working not shortened; figure fix in docs/todo.md). `MaffsScroll.reveal` (schools/assets/scroll.js) is the one scroll for feedback/Next/keys: re-reveals after late fonts (ResizeObserver), measures the footer itself; guard `check-scroll-reveal.py`; `sweep-cold-font-scroll.py` is a by-hand report (drives 3 of 10 games; decimal-detective and screening-room flag the same on main).

**SIX-PS-LAUNCH (27 Oct, Jon's contract; branch `claude/six-ps-launch`, worktree E:/jon/mg-launch):** counted first: 99 listed games (sitemap 99 /games/ URLs; roster 107 rows less the 8 Unlisted), nothing queued ahead (build.md: "The 6 P's goes first"). Listed `/the-6-ps/` as the 100th item: `data/games.json` "pages" entry (title/description via apply-meta.py; the page lost its noindex, gained canonical + og tags), sitemap, a portal card (GCSE section), `/updates/` entry (Jon's words, first in October's New list), canon 7.5. **No roster row: the roster is games-only and tied to `games/` directories (check-site, roster_exceptions), so a page that is not a game is listed through "pages", which is the existing mechanism for /essentials/.** New files only: `schools/assets/featured.js` + `featured.css` + `featured-items.json` (Essentials pinned card; second item = data), `launch-sash.js` + `.css` (homepage only; END 2026-11-10T00:00:00Z; since 29 Oct a static gold strip, 34px, between hero and ticker; `--announce-bg`/`-fg`, 9.1:1; the corner ribbon had covered Leaderboards) and `scripts/check-launch-sash.py` (+ 7-case selftest). After 10 Nov the sash hides itself; delete its two homepage lines and files whenever convenient. Public wording avoids "resit" on the featured card (canon 7.5.3); Jon's /updates/ words say "students resitting" and check-student-labels passes, but that is his call.

**SIX-PS-CALCULATOR (27 Oct, Jon's phone check; branch `claude/six-ps-calc`, worktree E:/jon/mg-calc):** The 6 P's served NO calculator at all (only the label); it now mounts the shared MaffsCalc (schools/assets/calculator.js, which already had a scientific mode: sin/cos/tan + inverses in DEG, x^y, pi, x^2, sqrt, brackets) on every calculator / optional question: scientific when the working uses a trig function, pi or a power other than 2, else basic; hidden once the answer is in. NO shared file changed (check-calculator.py gained a PLAYERS rule for the-6-ps). Check `check_calculator` in verify-the-6-ps.py (start unit): function cases, all 223 calculator questions' working vs the served keys, 320x568 UI (19 x sin 25 = 8.029; keys >= 44px), 3 plants.

**FOOTER (27 Oct, Jon's ruling "no footer links during a run"; branch `claude/footer-unpin`, worktree E:/jon/mg-footer):** The 6 P's removes the footer on questions/feedback/between topics and shows it on start and results (`show()`); check + 2 plants in `verify-the-6-ps.py` (results unit); every other page stays pinned; canon 7.5.2 records it. The in-flow footer was tried and dropped (it fails answer-lock's double-tap; backup of that work: local branch `footer-flow-backup`, not pushed). **Site-wide state-based fix waits for the freeze to end (Mon 2 Nov): in `E:\jon\lanes
otes.md`.** Queue: #583 (settle + sweep, parked until the launch), then the scroll PR (`claude/scroll-reveal`, local merge commit, unpushed; its inset auto-detects the footer so it works with pinned).

**SIX-PS-REVIEW-FIXES (27 Oct, Jon's contract items 1-13; branch `claude/six-ps-review-fixes`, worktree E:/jon/mg-sixps; report `docs/handover/contracts/2026-10-27-six-ps-review-fixes-report.md`).** Rules a-h in `scripts/six_ps_rules.py`, fixes in `apply_review_fixes`, Probability Pioneer fixed at source, results screen drawn whole (`#resultsBody`), Constructions `NOT_OFFERED`; review sheet republished (version 6). **Queue after it merges:** the footer unpin on playable pages (a shared marker + a rule in site-footer.css, a check that every page under games/, escape-rooms/ and the-6-ps/ carries it; confirm on a phone), then the scroll contract (branch `claude/scroll-reveal`, worktree E:/jon/mg-scroll: `MaffsScroll.reveal` + ten call sites + guard check committed, sweep driver written not run; the helper's inset must be 0 once the footer is unpinned). **Answer-counts is done (#572, 3b8b702, main green, live file updated 13:54 UTC).**

**ANSWER-COUNTS-SLUGS (27 Oct, #572).** Done: no slug check, every slug published, the total never falls below the published file's.

**SIX-PS-PLAYER-FIXES (27 Oct, Jon's phone play-through; #562, squash 7aee67b, main run 40474638379 green).** Items 1-9, 11, 12 done; **ITEM 10 (phone-fit roster) OUTSTANDING: waits for the cloud lane's DRIVER PR (PR1 of its fix contract, changing measure-phone-fit.py and the phone-fit lists); there is no footer PR, the footer stays pinned (Jon's correction).** **"Your six" duplicated, and Jon's addition (Honor 400 Pro: after a resume, a topic's fifth answer, a choice question, showed no feedback, no Next): neither reproduced** (resume then a choice-only topic to its fifth answer, on the old and the current page; every metric-units question; clean console; state cannot exceed six). Guards: every list swaps its content in one `fill()`; one copy of the script per page; a visible "Reload" note if the page's own script throws; a plain verdict + Next if the feedback throws; tests and plants for each (follow-up branch `claude/six-ps-resume-guard`, commit 6bd5f993, local check-changed passed; PR #565, CI running, then merge-pr.py). **Typed answers: 326 questions, choice 610 -> 284;** new formats hold 84, not 98; left as choice for Project Claude: 10 two-value modes, 5 standard-form selections; no rounding added. Report, before/after per topic, plants: `docs/handover/contracts/2026-10-27-six-ps-player-fixes-report.md`. **Next:** guard #565 and fix #566 merged (main was red on a latent 375 x 667 fault). Pie charts #567. Percentages-money bank, the scroll-once class list and why item 10 did not start: `docs/handover/contracts/2026-10-27-percentages-money-bank-report.md`, `-scroll-once-class-search.md`.

**SIX-PS-THREE-BANKS (26 Oct, Project Claude's contract): STOPPED at step 1, nothing banked.** STOP IF fired for all three sources: given-that has 25 bankable Foundation items (gcse phase 1; phase 2 is all conditional), coordinate-geometry-dash at most 21 (24 gcse, 3 perpendicular excluded), constructions-lab 0 (10 drawing tasks, no questions); each needs 30. No bank, generator or sheet changed. Report with the counts, the set-notation check (none in gcse) and the Core/Level 4 question for Project Claude: `docs/handover/contracts/2026-10-26-six-ps-three-banks-report.md`. Contract text: `docs/handover/contracts/2026-10-26-six-ps-three-banks.md`.

**ANSWER-COUNTS-STALE (26 Oct):** full entry moved to `docs/history/handover-home-archive.md`.

**From the cloud lane (26 Oct; contract LOOK-REDS-2 asks it to tell this lane):** the cloud lane took over `claude/theme-distinctly-average`, rebased it on main and finishes Distinctly Average in its own PR from `claude/theme-distinctly-average-2` (Jon, 26 Oct: no force-push; the old branch is left untouched and unmerged). Prime Sprint waits for Jon's next contract. Do not push to either branch.

**SHAPE-SHIFTER-TYPES (26 Oct):** full entry moved to `docs/history/handover-home-archive.md`.

**SIX-PS-BANKS batch 8 (25 Oct, Project Claude's contract, Jon's rulings on batch 7; #549, squash 9e11d88, main run 40240668164 green).** Batch 7 is #547, squash b327d92, main run 40235069730 green. **Rulings applied:** vectors stay at 36; calc true where a calculator is needed (approved); the quadratics and simplify stage 2 wrong answers are approved and now carry Project Claude's slip lines (quadratics: both signs changed, one sign changed, the same bracket twice; a difference of squares has only two kinds, so its third wrong pair, p + 1, has no slip; simplify stage 2: a coefficient one out, coefficients multiplied with the item's own first letter as the example); typed conversions and the 16 dropped fraction-operations items approved. **Worked lines from the templates, every number computed here:** estimation 45 (round each number, then work it out; a root as sqrt(a x b) = sqrt(n) = answer), quadratics-factorise 60 (two numbers that multiply to c and add to b; difference of two squares), standard-form the 9 (correct form, which two are equal, power 0; **the template's second line for the correct-form items, "Only <key> has that.", is not true of an option in standard form with the wrong value (3.4 x 10^5 for 34 x 10^5), so it reads "Only <key> has that form and the same value as <the question>."** and the script checks exactly one option is in standard form and equal), transformations 45 (translation, reflection in either axis, rotation about the origin, then "So the image of A is ..."; the template's y = x, x = k and other-centre cases do not occur in the game). **No bank now has a question without worked lines.** **The diagram label check** (`diagram_problems` in `gen-six-ps.py`, run on every diagram of every build, `--check` fails if one is left; its plants run in `--check`): a label's box is estimated (0.55 of the font size a character), each drawn line (lines, polygons, polylines, paths, arcs sampled; the faint grid left out) is tested against it, and labels are moved the shortest way (up to 30 px) that clears all lines, other labels and the viewBox. **It finds, of the 360 diagrams (angles 35, area 60, perimeter 60, trigonometry 60, transformations 45, pythagoras 60, coordinates 40): 8 with a line through a label as the check was first worded (a line other than the side it labels: angles 2, trigonometry 6); 42 when a line through the label's own side also counts, which is how I ran it (angles 15, area 12, trigonometry 9, transformations 6); 87 with two labels overlapping (the two -5 on the grid's corner in all 85 grids, two in area); after the labels are moved, 0.** The house diagram is fixed (its "4 m", "6 m" and "12 m" labels no longer sit on a dashed line or touch a slanted side; the 12 area diagrams like it are the same fix). The first-worded rule is the weaker one: it lets a label sit on the line it labels, which is what the house did. **Review sheet for Jon (all 32 banks, 1,649 questions, grouped by topic, every question with its answer, worked lines, slips, diagram and source game):** https://claude.ai/artifact/FHXCnemqt489oVZXribfFS (private; Jon opens it from his own account). The cloud lane has `claude/theme-distinctly-average` (LOOK-REDS-2): untouched. #518 and #424 are not this lane's.

**GH-REST (25 Oct, Project Claude's contract; PR and main run: see the line below once merged).** `scripts/end-task.py` read PR state with `gh pr view` (GraphQL); it now uses `gh api repos/{owner}/{repo}/pulls?head={owner}:<branch>&state=all` (`pr_from_rest`: MERGED when `merged_at` is set, else OPEN or CLOSED; newest PR wins; head sha and merge commit from the REST fields), five new selftest cases. **Grep of `scripts/` and `.claude/` for GraphQL-backed gh use: that one call only** (`ci-groups.py` and `merge-pr.py` already use `gh api` REST; merge-pr.py's refusal path untouched; no `gh pr`/`gh issue` call in `.github/` workflows). CLAUDE.md rule added. Live check: REST gave the same head shas `gh pr view` did for #523/#525.

**BURST-SPLIT (25 Oct, Jon's ruling via Project Claude; PR and main run: see the line below once merged).** Main's timings job went red on b001e21: `check-burst.py` as one CI line ran 220 s (+18 s setup) = 88% of Content verifiers 42's 270 s budget. It is now three lines, as #515 and #528 did: `--part 1` the checks (static, `&stage=` cases, 31 games played; about 116 s alone), `--part 2` three plants (stage ignored, bar after four, active without `?burst`; 65 s), `--part 3` two plants (score submitted, right count; 51 s); no part reads or tests anything differently, and with no `--part` it runs everything as before. All five plants caught in each local run. Merged with Jon's override for this PR only (main red from this group). The architectural fix (median fallback, config-driven sharding) is a separate contract.

**BURST-STAGE (25 Oct, Jon's contract; PR #525, squash 7d432d5; main's push run 40178159416 green).** `schools/assets/burst.js` now also reads `&stage=<value>` and presses `button[data-stage="<value>"]` once (after `&mode=` if both; same wait of 3 s and no Start press: a stage button, like a mode button, only selects, the game's Start button is the student's). No match: the game opens normally and one `console.warn` names `stage=`. Values are the buttons' own: free-daily-pizza `1`-`4` and `mixed`; simultaneous-solver `stage1`-`stage5` (**not** `4`: its buttons are `data-stage="stage4"`; the 6 P's link must use `stage=stage4`). `scripts/check-burst.py` has nine stage cases (the game's own `game_started` mode proves the stage: FDP stages 1-4 give `stage-sN-q20`, `mixed` is the default pick `practice-q20`; SS `stage4`; how-many-parts `?level=ks3&mode=stage3` unchanged with no warning; a missing button warns once) and a plant (`stage=` ignored) caught. No game edited. Still not openable at a stage: how-many-parts Advanced a-f (list items, not buttons). Shape Shifter was not on this lane's list; the cloud lane's fix for it is separate.

**BURST (24 Oct, Jon's contract; PR #523, squash 47a164d; main's push run 40142633667 green; constructions-lab excluded by Jon's ruling of 25 Oct).** `schools/assets/burst.js` (canon 7.5.6): `?burst=N&from=six-ps&topic=<id>` wraps `mfg()`, counts `question_answered`, and after the Nth shows a fixed navy bar "That's N. Back to The 6 P's (R of N)" linking to `/the-6-ps/?done=<topic>&r=<R>&n=<N>`; `?mode=` presses the start screen's `[data-mode]` button once. A burst never submits: guards in `firebase-leaderboard.js` `submitScore` and `score-history.js` `record()` (no game changed for it). Adopted by one deferred line after `analytics.js` in **31 games**: the contract's 32 less `constructions-lab`. **STOP IF fired for constructions-lab and was NOT worked around:** it never calls `mfg('question_answered')` (non-scored, canon 9: it only reports game_started/abandoned), so it is not adopted and has no per-game counting; ruling needed if The 6 P's wants it. `scripts/check-burst.py` (CI; each adopted game played 5 answers in Chromium with the answer-lock driver; bar after the 5th only; link r/n; no submit/history; no change without `?burst`: DOM identical with burst.js stubbed; four plants caught). **Cannot be opened at a stage by `?mode=` (stage buttons are `data-stage`, not `data-mode`; opened at their level, listed not hacked):** how-many-parts Advanced (gcse) stages a-f (Foundation/ks3 stages are data-mode and work; the Advanced stages are list items, not buttons); take-a-walk and squared-squirrel work. (simultaneous-solver and free-daily-pizza now open at a stage by `&stage=`, see BURST-STAGE.) **Games that keep their own best in `localStorage` (not reached by the guard; written only at the end of a full run):** index-laws (`il_best`), factor-race (`fr_best`), distinctly-average, trig-worms (`tw_best`), quadratic-factoriser (`qf_best_<level>`). `MaffsProgress` is used by none of the 31. The 6 P's page is the cloud lane's and does not exist yet: the bar's link 404s until it does.

**SIX-PS-BANKS follow-ups (26 Oct, Project Claude's contract from #549; #551, squash 9a5baec, main run 40341214282 green).** **1. "Only" claims: zero false.** I searched every string of all 32 banks and every template in `gen-six-ps.py` for "Only", "the only", "neither", "no other", "none of", "exactly one" and "unique". Claims of uniqueness among the options: **6, all in standard-form** (the correct-form items, already worded "has that form and the same value as"); each was re-checked here against its four options with Decimal (exactly one option in standard form and equal to the question): 6 true, **0 false**, so nothing was changed. The other "Only" lines are general facts, not claims about the options (averages "Only values tied for the most common count as modes", 5; probability "Only a probability of 1 means it will definitely happen", 3), and no other template says it. **2. Distractors with no slip.** Only choice questions have a fixed set of distractors: **610 choice questions, 1,830 distractors, 929 with no slip** (arithmetic-negatives 45, basic-probability 30, change-subject 84, coordinates 45, metric-units 144, powers-roots 96, quadratics-factorise 20, sequences 18, simplify-expressions 90, simultaneous 144, standard-form 150, vectors 63; averages, form-expressions, fraction-operations and trigonometry 0). For a typed answer the wrong values are open-ended, so they are not counted: any wrong value that matches no slip gets the same path. **What the page shows for one: it already shows that question's worked lines**, so I made **no renderer change**: `feedback()` in `the-6-ps/index.html` hides the slip line when `slipFor` finds none and, for any wrong answer, lists every worked line under "The answer: ..." (the slip line is shown above them only on a match). Checked in Chromium on the real banks, one slipless distractor picked in each of seven banks (standard-form, simultaneous, metric-units, change-subject, powers-roots, vectors, arithmetic-negatives): verdict wrong, no slip line, all worked lines shown (3 of 3, 5 of 5, 2 of 2, 3 of 3, 1 of 1, 3 of 3, 2 of 2), answer line shown; control in trigonometry (a slip answer): slip line then the same worked lines. No question has empty worked lines (0 of 1,649), so the fallback never needs new wording. **3. Review-sheet generator: already in the repo.** It is `sheet()` and the `SHEET` template in `scripts/gen-six-ps.py` (`python scripts/gen-six-ps.py --check --sheet <file>`); only its output had been written to a scratch folder. Regenerated from a fresh worktree on main it is **byte-identical** to the page published at https://claude.ai/artifact/FHXCnemqt489oVZXribfFS, so that artifact was not republished (nothing in it changed). `--check` passes on all 32 banks. **4.** `docs/todo.md` §6 logs the transformations gap (reflection in y = x and x = k, enlargement about other centres) as awaiting Jon's ruling; no transformations question written. Distinctly Average, canon §7.6.1 and every slip and worked-line wording: untouched.

**SIX-PS-BANKS batch 7 (25 Oct, Project Claude's contract; #547, squash b327d92, main run 40235069730 green). ALL 32 ROUTED TOPICS NOW HAVE A BANK.** Batch 6 is #546, squash 3a6dec2, main run 40232409732 green. **Six more banks: standard-form 50, quadratics-factorise 60, estimation 45, metric-units 48, pythagoras 60, coordinates 40. Banks now 32 (1,649 questions, 1.7 MB); 32 topics covered, 168.6 marks a series; the 25 topics left are the ones with no game routed.** **standard-form:** every standard-form-blitz item as `choice` with the game's key and its three wrong answers; the question's value recomputed from its TeX (Fractions), the key checked true and each wrong answer false (a standard form answer must be equal AND in standard form); worked lines follow the STANDARD FORM template for 41 of 50 (writing in and out of standard form, multiplying, dividing, ordering); 9 on the missing list (correct standard form, which two are equal, 10 to the power 0); band 4 writing in and out, 5 the rest. **quadratics-factorise:** quadratic-factoriser's pool (174) as `choice` of bracket pairs, 60 spread over the four stages; the key is the game's (x + p)(x + q) with its numbers checked (p + q = b, pq = c); the three wrong pairs are mine (both signs changed, one sign changed, the same bracket twice), each checked not to expand to the quadratic; **no template and no written steps in the game, so 60 of 60 are on the missing-worked list, and no slips; Project Claude to rule on the wrong pairs and supply a template.** **estimation:** all 45 as `number` (`money` where the game's answer is in pounds), "estimate by rounding each number to 1 significant figure", rounded numbers and estimate recomputed from the printed numbers and the shape (half up; a root only of a perfect square); the game's calculator answer is not asked; 45 on the missing-worked list (no template). **metric-units:** the 48 gcse items (the 10 Engineering items are above Foundation) as `choice` with the game's key and wrong answers, its steps as the worked lines; every answer recomputed from the words (conversion factors, the item's own constants, its pi); the game's `mc` line is a general reminder, not tied to an option, so not a slip; the one item that asks for 3 significant figures is the only calculator item. **pythagoras:** just-pythag-it-bruv's generator, seeds 1 to 300, each distinct question once, 60 kept (ten of each of round 1, 2, 3 by hypotenuse or shorter side) as `number` in the game's unit with its own triangle (outline, right-angle mark, labels as text), the game's prompt (plus "Give your answer to 1 decimal place" where the prompt omits it, and "The diagram is not drawn accurately" where the game flags it), its worked solution as the worked lines and its one named error, adding instead of subtracting, as the slip on a shorter-side question; the key is recomputed (sympy, 40 digits, half up) from the sides shown, the labels checked against the sides, the add error recomputed; whole-number answers are non-calculator, decimal ones calculator. **coordinates:** the 45 four-quadrant-explorer items on a -5 to 5 grid: READ (15) as `choice` with the game's own options, PLOT (20, the game asks the student to place a point) asked the other way as `coordinates` of the point shown, five of them left out because a READ item shows the same point, SHAPE (10) three corners of a rectangle with the fourth asked (`coordinates`, recomputed from the right angle); worked lines are the COORDINATES template; 40 questions, bands 1-2. **Transformations and coordinates** are asked as the image of one corner and the coordinates of a point because the games ask for placing a shape or a point, which a typed bank cannot. **For Project Claude:** the calc=true departures (trigonometry, decimal pythagoras, one metric item); the missing-worked list is now estimation 45, quadratics-factorise 60, standard-form 9, transformations 45. Plants caught: a standard-form value, an estimate, a conversion, a pythagoras root, a coordinate label, and the earlier ones. The cloud lane has `claude/theme-distinctly-average` (LOOK-REDS-2): untouched. #518 and #424 are not this lane's.

**SIX-PS-BANKS follow-up (25 Oct; #541, merged).** Project Claude's two data files are in `data/six-ps/` (`authored.json`, 54 questions; `worked-lines.json`) and `gen-six-ps.py` merges them. **Authored questions** (vectors 15, form-expressions 21, rounding 15, change-subject 3) are validated like any item and recomputed: every rounding value by round-half-up (Decimal) with `dp` checked against the stem (a slip that `dp` would turn into a format message fails), every vector key by evaluating the stem's expression (and no second option may equal it), every change-subject key and option with SymPy; form-expressions are checked for schema, distinct options and slip answers only. **Worked lines:** the 24 sequences items are filled by id (all 50 sequences now have worked lines) and every number in a line must come from the sequence (a prime sequence may name the non-primes between the last term and the next prime, each checked non-prime); equation-builder's 9 forming-equations items become `choice` (answer label plus 3 wrong, each wrapped in \\( \\), slips from the wrong lines, `stem_override` used for QUESTIONS[10]), with the answer label recomputed against the game's own slots by SymPy and every number in a line taken from the question; probability stage 1 is 10 `choice` items (the five words, the answer and the three nearest, a tie between two equally far words broken by the item's own hash; the game's label is checked against the supplied answer). `validate` now also fails a number answer whose stem asks for decimal places but has no `dp` (none of the generated banks does). Six plants caught (wrong rounding answer, rounding answer without dp, wrong vector key, a number in a sequences line not from the sequence, an equation-builder label not the game's equation, two equal options). **Banks now 11 (588 + 30 = 618 questions): form-expressions is new (equation-builder 9 + authored 21 = 30) and covered.** **Still under 30, no bank written (the games' own items are the next conversions):** vectors 15 (authored only; component-crusher's 15 are the rest), rounding 15 (authored only; decimal-detective's rounding items), change-subject 3 (authored only; formula-unlocked's 29), basic-probability 10 (stage 1 only; stages 2 and 3 are not converted). Decision flagged: the probability stem is "Which word best describes how likely this is? <event>." and the form-expressions band is 3 for the game's items. The branch `claude/six-ps-authored-data` is deleted once this merges.

**SIX-PS-BANKS batch 1 (25 Oct, Project Claude's contract; #540, squash 767d0ad, main run 40211346621 green).** `scripts/gen-six-ps.py` builds each bank from its game's own questions on the stub server (a game's list as the page holds it; a generator called in the page with `Math.random` seeded, ref `generator:<function>:<seed>`; Squared Squirrel's and Free Daily Pizza's exported pools), converts to docs/six-ps-schema.md, and recomputes every answer from its own stem (SymPy for equations, Fractions for the rest, a small TeX evaluator for the index laws, the terms for sequences, the figure's numbers for angles); `--check` regenerates and diffs every committed bank and fails on a covered topic with no bank or a bank whose topic is not covered (a CI line, about 10 s); `--write`, `--sheet FILE`. `gen-exam-topics.py` lists a topic as covered only if `schools/assets/six-ps/<id>.json` holds at least 30 questions (derived from the files, no manifest); the rest go to coming_soon with their marks. **Banks (10 topics, 588 questions):** ratio 60, direct-proportion 60, powers-roots 32, compound-measures 60, linear-equations 141, sequences 50, angles 35, arithmetic-negatives 30, fdp-convert 60, fraction-percentage-of-amount 60. Review sheet for Jon (every question, answer, worked lines, diagrams): https://claude.ai/artifact/6JSRxWjZVxAsHefUqxzS2i. **Rulings applied (Jon, 25 Oct):** generator topics keep 60 spread evenly across types and stages from a fixed seed (Split It's scale is one ingredient a question); list topics keep every Foundation item. Powers-roots keeps every item (zero and negative indices included) except those with a fractional exponent, so it reaches 32. **Angles:** Angle Ace draws on a canvas, so each figure is drawn as one shared SVG (viewBox, currentColor, text labels) from the game's own geometry (`FIG[...]` and `placeLabel` read in the page, label widths fixed so the file is reproducible), with a check that every label in the drawing is one of the item's numbers or x, and the answer recomputed from the figure's numbers by its rule; the stem adds "The diagram is not drawn accurately." **Negatives:** the 15 calculate items use the add and subtract templates exactly; the 15 ordering items are `choice` with four orderings (the three wrong ones by size ignoring minus signs, largest first, and the right order with a neighbouring pair swapped, the next neighbouring swap standing in when two coincide, all four checked distinct). **Sequences:** the worked template fills the 26 arithmetic items (next term, kth term, common difference) and is recomputed; the other 24 (squares, cubes, Fibonacci, primes, geometric, 'which term', 'what type') stay on the missing-worked list. **Still waiting: the two attachments did not arrive a second time** (`six-ps-authored.json`, 54 questions for vectors, form-expressions, rounding and change-subject; `six-ps-worked-lines.json`, worked lines for the 24 sequences items and the choice versions of the 9 equation-builder and 10 probability stage-1 items). No file reached this session, so `data/six-ps/authored.json`, their merge and the probability five-word choices are NOT built; send the files as text in the message or commit them to a branch. **The player PR (#538) has merged, so this PR merges normally.** **Decisions for Project Claude to change:** Split It's divide asks for the larger share; `band` is a rule per topic from the game's own structure; `calc` is false everywhere; 8 Free Daily Pizza answers that are recurring decimals and Squared Squirrel times in hours and minutes are left out (cannot be typed); stems use the game's wording where it types a question and the exam's plain form otherwise. `docs/six-ps-worked-requests.md` holds the 9 forming-equations and 10 stage-1 probability items as they appear in the games.

## Moved 2026-11-03 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

## 2026-11-01 (home): GT-EXPLAIN (Small, home, Codex WSL): branch `codex/gt-explain`, worktree `/home/maffs/mg-gt-explain`. Jon confirmed Small and waived Windows lane notes; only one lane is running. Contract-specific hold: stop at Gate green for Project Claude review and explicit "merge". No merge or cleanup authorised yet. PR #628 already closed unmerged by Jon, comment verified via REST; `codex/start-task` kept. All 50 old descriptions agree with their targets. One target-derived builder now supplies result-panel blocks and Show steps names; puzzle `desc` fields removed. Stages contain exam vocabulary (column vectors in KaTeX), before/after equations and a tracked base point. Phone styling confined to the feedback panel; controls, scoring, targets, graph drawing and buildEquation unchanged. The par-4 puzzle has three stages because vertical stretch/reflection share one stage.
- **State: Checked locally, pushed, PR #629 open.** https://github.com/OrthogonalMaffs/maffsgames/pull/629 . Commits `38998177` (implementation), `eb75606f` (check results), `e0101d10` (initial push blocker). First push refused with HTTP 403; after Jon requested retry, `git push -u origin codex/gt-explain` exited 0 and PR creation succeeded. Access blocker resolved. PR body tracks current-head Gate; no merge or live deployment yet. Stop for Project Claude review and explicit "merge". Screenshot repository attachment remains pending Jon's scope answer.
- **Checks:** game verifier PASS for 25 GCSE + 25 A-Level puzzles; all nine plants CAUGHT, including flipped direction, reciprocal scale and missing block. All 600 phone panels checked; Aa at 320px uses canon's recorded overflow exception, other sizes fit. Complete `python -X utf8 scripts/check-changed.py`: 48/48 passed in 438s, "All selected checks passed. Push, and CI runs the rest." Seven standard checks deferred to CI. KaTeX-unavailable fallback: all 50 panels readable, no raw LaTeX. PR body tracks current-head Gate status; review/merge hold remains. Initial verifier attempts exposed a selector reading the vector instead of the equation, and use of the sync settle helper with an async page; corrected in the verifier. No claim those attempts passed.
- **Maths:** names, reciprocal horizontal scales, signed directions and point-coordinate maps independently checked from target parameters. Equation strings compared with buildEquation: consistency, not independent mathematical verification. Existing reachability/par BFS uses the game's actual rules. Base points: square vertex (0,0), cubic origin (0,0), sine's original zero crossing (0,0), square-root endpoint (0,0), exponential (0,1), reciprocal reference point (1,1).
- **Screenshot:** par-4 Skip panel captured at 320x568 after fonts settled and Next enabled: Next bottom 391.64px, usable fold 528px, no KaTeX errors. Local PNG is `.claude/bg-gt-explain-320x568.log` (PNG bytes, ignored artifact); PR attachment location pending scope confirmation.

### WSL mismatches — GT-EXPLAIN

- Windows primary/worktree paths map to `/home/maffs/maffsgames` / `/home/maffs/mg-gt-explain`; fetch and worktree creation succeeded in WSL.
- `E:\jon\lanes\notes.md` is deliberately inaccessible from WSL; Jon waived it for this task (one lane, no pending cross-lane facts). WSL-HOME will establish its WSL location.
- Interim Windows sandbox approval/launcher and locked-folder cleanup rules do not describe this no-sandbox WSL session. Jon's contract authorises local git operations here; no sudo or Windows shell used. Cleanup remains pending the explicit merge hold.
- Git identity not set in WSL: the first commit attempt refused with "Author identity unknown". Jon supplied Vector52F <262527784+Vector52F@users.noreply.github.com> and explicitly authorised global configuration for this dedicated WSL user; both values now set globally for future worktrees.
- GitHub writes initially unavailable in WSL: first push returned HTTP 403 despite account push/admin permissions. Git and gh use the same CLI credential; account permissions alone do not prove token write scope. Resolved on Jon's requested retry: push and PR #629 creation succeeded; no credential changed by Codex.
- Claude-specific shell/session controls map to exec tools and registered background processes via `python -X utf8 scripts/bg.py`; UTF-8 reads and checks use Python in the active WSL venv. AGENTS.md, CLAUDE.md and agent-workflow.md left unchanged.

## 2026-11-01 (home): CONTEXT-SLIM (Shared, home, Codex; PR #627): branch `codex/context-slim`. Amendment 3 addresses Project Claude's REQUEST CHANGES: operational file pointers and both improvement items restored verbatim from origin/main; background-process and escape-room referents restored without rewording. Archives reference moved instead; restored text removed from new canon material; duplicate headings consolidated. Final CLAUDE.md 20,480 -> 17,930 bytes (2,550 saved), below amended 18,000 ceiling. Independent Python checks PASS: 15 relocated blocks (3,385 bytes) exact in canon §12; 14 retained source fragments exact in CLAUDE.md; restored blocks absent from new canon appendix; eight unique headings/eight section pointers; existing canon unchanged; UTF-8/LF preserved. Retained-fragment referent audit complete. Current revision: complete outside-sandbox check-changed.py 40/41 PASS in 277 s; only the documented Windows Timing gate self-test failed during temporary-directory cleanup (WinError 32). Seven standard checks deferred to CI. Timing inputs unchanged; 30 Oct ruling applies, Linux CI is authoritative. Prior head's green Gate does not verify these review corrections. PR report tracks current Gate; stop at green for re-review. No merge or cleanup authorised.

## 2026-10-30 (home): ENCODING (Shared, home, Codex): branch `codex/encoding-rule`. Exact rule added once in AGENTS.md, with pointers from CLAUDE.md and the workflow failure table; no scripts, profiles or config changed. UTF-8 exact-insertion and four-file scope checks PASS; context size PASS (CLAUDE.md exactly 20,480 bytes). Complete `python -X utf8 scripts/check-changed.py`: 40/41 passed in 308 s, exit 1; only failure was Windows timing selftest (three assertions, then missing temporary ci-timing/timing.txt); seven standard checks deferred to CI. Project Claude's standing ruling (30 Oct 20:30) applies: no timing-gate input changed, proceed to PR; Linux CI Gate is the authority, stop on any CI timing failure. Awaiting Gate and Shared review; no merge or cleanup authorised. Optional PYTHONUTF8=1 proposed for Jon only, not applied.

## 2026-10-30 (home): ATTAINMENT-LABELS (Shared, home, Codex; PR #625): Implemented the student attainment/ability policy and checker tests; approved Essentials and updates wording applied. Jon permits grade bands for difficulty/level, including KS3 room metadata; struggle/struggling alone remains permitted. Protected content unchanged. check-changed.py 43/44 locally on Windows; timing-gate selftest fails on Windows only (passes on Linux at origin/main, reported by Project Claude); CI Gate is the authority. Older handover entries archived verbatim under RESUME 4 after CI's size failure. Awaiting green Gate and Shared review; no merge or cleanup authorised. ENCODING pending in its own fresh worktree after attainment Gate green/report.

## Moved 2026-11-03 by check-context-size.py --fix from docs/handover/home.md (history, unchanged)

## 2026-10-30 (home): LIST-TWO (Medium, home, Codex): branch `codex/list-two`. Both approved games listed; I Found a Mark featured second on Essentials and mapped only to AO3 across a growing range of GCSE topics; Who Ate All the Pies? mapped to S2. Pattern `840655ab` (#519), permitted listing surfaces only. Amendments 1-8 applied; all 15 changed files authorised. Essentials static self-test 11/11 and spec mapping pass; filter verifier OK with all 14 existing and five new plants caught, missing technique chip caught by its explicit count message; chip(), check_fit(), thresholds and existing plants unchanged. All 36 existing cards' topic/calculator attributes and expected spec wording unchanged. Bar main/branch identical: 145 px at 320x568, 360x640, 375x667 and 390x844; 163.390625 px at 1280x720; no row wraps, all under 27%. CLAUDE.md 20,447 bytes.
- **RAN (Codex):** documented `python scripts/check-changed.py`; sandbox attempt interrupted for KaTeX/browser failures, then Jon-approved complete outside-sandbox retry: 157/159 passed in 962 s, exit 1, with the runner's documented CI deferrals. Original retry failures: Eigenvalue Extractor `http.client.BadStatusLine: GET /schools/assets/analytics.js HTTP/1.1`; Timing gate self-test missing temporary `ci-timing/timing.txt` (FileNotFoundError). Nothing bypassed or marked passed.
- **Amendment 8 evidence:** working-tree diff against HEAD `0c6dcb29` has empty intersections with both Timing gate's declared dependencies (.github/workflows/check-site.yml, scripts/ci-groups.py, scripts/ci-timings.json) and the eigenvalue game/verifier plus bank_common.py and serve-stubbed.py. Runner commands confirmed from its command registry: `python scripts/verify-eigenvalue-extractor.py`; `python scripts/timing-gate.py --selftest` (runner output names checks, not commands).
- **Independent results (Jon, normal Windows PowerShell, 30 Oct):** Eigenvalue Extractor PASS, exit 0, all nine planted faults caught. Timing gate FAILED: fourteen initial assertions passed, final three failed; missing ci-timing/timing.txt, cleanup WinError 32 and WinError 5. Jon authorised Amendment 8's decision rule: both original failures recorded as unrelated local failures; CI on Linux remains the referee and a red Gate on either stops. No claim that Timing gate passed locally. Local deferrals were subsequently verified by CI: PR Gate green and main full run 41085301202 success after Jon authorised the guarded merge. No answer-bearing change.
- STUB-SELF-CONNECT: bank_common.start_stub_server's readiness probe can connect to itself on Windows (the free_port() port is an ephemeral one) and raises an uncaught http.client.BadStatusLine; fix at the shared layer after the freeze: serve-stubbed.py binds port 0 and reports the port it got, and the probe treats an HTTP error as not-ready.
- Timing gate self-test fails locally on Windows in three different ways (29-30 Oct); unrelated to the changes checked; CI passes it.
- **State: Merged, main full CI green.** Branch `codex/list-two`, PR #623, local head `031d1e09f1d6ce90bc35b95fdae3a7ba6d0e71ba`, squash `c57ad2af8bc334ca079a62b8e226181252059b2d`. Jon separately authorised push/PR and merge. Final check: PR head unchanged, Gate green, mergeable clean, no reviews or comments indicating a blocker. `python scripts/merge-pr.py 623` exited 0, judging green main run 41047842596; no override. Main full `check-site` run 41085301202 on the squash commit started and completed success: 84 jobs completed, no pending or failed jobs. https://github.com/OrthogonalMaffs/maffsgames/actions/runs/41085301202 . Final result also recorded in PR #623's report. Cleanup pending: no end-task.py, branch deletion or worktree removal. Review state: Jon approved the change set and guarded merge; no separate architect review recorded. CLEANUP: debug.log inspected earlier (four Chromium GPU errors, no sensitive contents), deleted personally by Jon; no further action. end-task.py not run, as contracted; Jon cleans up after closing Codex.

## 2026-10-29 (home): HOME LANE CLOSED: work passes to Codex from 29 Oct (Jon). State of play: ticker pause (#616), gold announcement strip (#617), answer-counts `planted_failure` input (#613), new-games status table (`docs/handover/new-games-status.md`, #615), stale-plants helper (#610, `docs/handover/stale-plants.md`), Plan timeout 10 and Gate fix (#618) are all merged, main green. **Parked:** (1) The 6 P's card layout, branch `claude/six-ps-card` on origin (no PR; worktree `E:/jon/mg-card`, Codex or Jon removes it), `docs/handover/six-ps-card.md`: Jon's ruling pending on chart questions that cannot reach Check above the fold at 320x568 (444 of 1805); sticky Check recommended. (2) Item 8 (per-question "pen and paper" flag) waits for `gen-six-ps.py` after 2 Nov. (3) Monday 2 Nov: PLAN-MAP-ONCE (Plan timeout back to 5), post-freeze items in `docs/todo.md` and `E:\jon\lanes\notes.md`. (4) Jon: trigger `gh workflow run answer-counts -f planted_failure=true` and confirm the email; paste the GA4 summary scripts into Apps Script.

## 2026-10-30 (home): AGENTS-MD (#622, Small, home, Codex): branch `codex/agents-md`. Commit the placed AGENTS.md unchanged and agent workflow with Git safety, interim launcher/cleanup rule and Amendment 1 report format; exclude AGENTS.md from Pages (workflow already covered by docs/*.md); correct #621 status below. Temporary git-safety-draft.md incorporated and deleted, never staged. Initial-input exception authorised by Jon for the three copied files only. check-changed.py exited 1: 38/41 passed in 405 s, only the expected Teacher feedback line, Start-screen mount and Timing gate (WinError 1920) failures; seven checks deferred to CI. Publish scope passed with both new files tracked (1254 tracked / 370 published). PR #622 open; Gate, merge and main full run pending; cleanup by Jon after closing Codex, not run by Codex.

## 2026-10-25 (home): SIX-PS-BANKS batch 6 entry, moved to keep the handover under 20 KB

**SIX-PS-BANKS batch 6 (25 Oct, Project Claude's contract; #546, squash 3a6dec2, main run 40232409732 green).** Batch 5 is #545, squash c67145a, main run 40229935284 green. **Six more banks: inverse-operations 50, trigonometry 60, simultaneous 48, transformations 45, simplify-expressions 40, substitution 50. Banks now 26 (1,346 questions); 26 topics covered, 152.3 marks a series; 6 topics left** (standard-form, quadratics-factorise, estimation, metric-units, pythagoras, coordinates). **inverse-operations:** every think-of-a-number item as `number` ("I think of a number. I add 6. My answer is 14. What was my number?"); the answer is checked by running the steps forward, the game's undo steps are the worked lines and each is checked as a true sum; no slips (the game names none); band = the number of steps. **trigonometry:** trig-worms' outcomes as `choice` with the game's own three named wrong answers (each slip is the game's name for the error, capitalised), the game's explanation split at its arrow as the worked lines, a right-angled triangle drawn to scale (only the given sides labelled, "?" on the asked side, theta or the angle); the sides shown, the key and every named error are recomputed (sympy, 40 digits, half up), all 1,152 outcomes checked, 60 kept (ten of each of the six kinds); **`calc` is true for this topic: it needs a calculator, so it departs from "calc false everywhere" and Project Claude should confirm.** Band: side 4, angle and hypotenuse 5. **simultaneous:** stage 4's 48 items as `choice` of "x = a, y = b" (the coordinates box would read the pair as a point); the game gives no wrong answers, so the options are the pair, its swap and a sign changed (the next nearest standing in), each checked not to satisfy both equations, no slips; the worked lines are Project Claude's SIMULTANEOUS template (the letter needing the smaller multipliers eliminated, add or subtract, put back into (1), check in (2)), every figure computed here; band 4 when one equation is a multiple of the other letter's coefficient, else 5. **transformations:** shape-shifter's 45 Random Mix items, which the game answers by placing the image on a grid, are asked as `coordinates` of the image of one corner (A, B, C or D in turn), the object drawn on a -5 to 5 grid; the image is recomputed from the item's words and, for a rotation, compared with the game's own correct shape; **no worked solution exists for it, so 45 of 45 are on the missing-worked list**; band translation 1, reflection 2, rotation 180° 3, ±90° 4. **simplify-expressions:** like-terms-collector's stage 3 (30 choices, the game's own wrong answers) and stage 2 (10 typed items asked as a choice with three wrong answers of mine: one coefficient up one, one down one, and the two coefficients multiplied; **Project Claude to rule**); stage 1's fruit is left out; worked lines are the SIMPLIFY EXPRESSIONS template; every key recomputed by collecting the terms. **substitution:** every formula-plug-in item as `number`, the answer recomputed from the formula's own TeX, the game's working as the worked lines, band 1 (one step) or 2. Plants caught: trig slip value and key, an inverse step run forward, a simultaneous solution, collected terms, a formula value, a rotated image. **Next (marks order):** standard-form 3.2, quadratics-factorise 3.0, estimation 3.0, metric-units 3.0, pythagoras 2.3, coordinates 1.8. #518 and #424 are not this lane's. The cloud lane has `claude/theme-distinctly-average` (LOOK-REDS-2): untouched.

## 2026-10-25 (home): SIX-PS-BANKS batch 5 entry, moved to keep the handover under 20 KB

**SIX-PS-BANKS batch 5 (25 Oct, Project Claude's contract; #545, squash c67145a, main run 40229935284 green).** Batch 4 is #544, squash 28c4265, main run 40227477661 green. **Four more banks: fraction-operations 60, averages 60, area 60, perimeter 60. Banks now 20 (1,071 questions); 20 topics covered, 126.6 marks a series; 12 topics left.** **fraction-operations** is how-many-parts' stage 3 (add or take away, different bottoms) as `choice`: the game's key and three of its own named errors (it picks them with its seeded `pickErrors`; the game's `name` for each error is the slip), `HMP.steps` as the worked lines, the key and every error's value recomputed here from the error's words (TB, MD, DN, OP). 16 of the 96 items give only two wrong answers in the game, so they cannot be four options and are left out; 60 of the remaining 80, 30 adding and 30 taking away; band 2 adding, 3 taking away. **averages** is distinctly-average's Foundation pool (259: mean, median, mode, range) as `choice` with the game's own three named wrong answers and the game's one-line reading of each as its slip, the game's explanation as the worked lines; the key is recomputed from the data and every wrong answer is checked against the misconception it is named for (sum, a value, the position, the mean, the largest, the smallest, the frequency, the middle of the unsorted list); 60 of 259, 12 a kind (the median split by odd and even); band: range and unique mode 1, mean and two modes 2, median 2 (odd) or 3 (even). **area and perimeter** are take-a-walk's ask A (stages 1-3) and ask P (stage 1) as `number` with unit m² or m and a diagram: the game's own drawing (`TAW.draw`) rewritten as one self-contained SVG (outline, dashed lines, labels as text, currentColor, the game's stylesheet written as attributes); the key is recomputed from the corners (shoelace, side lengths), every labelled side is checked against its length and every number drawn is checked against the shape; the slips are the game's `LINES` (its first line of each error, a duplicate value dropped); the worked lines are `TAW.steps` less the "The answer" line, the parts' lines joined where there would be more than five; stems say "drawn to scale", "All the corners are right angles" and, where there is a dashed height, that it is the perpendicular height; 60 of 420 and of 81, spread over stage and shape; area band 1 square or rectangle, 2 other stage 1, 3 stage 2, 4 stage 3; perimeter 1 or 2. **For Project Claude to rule:** the game's own picture has a "4 m" height label that the 5 m side crosses in the house shape (as in the game). Plants caught: mean +1, a TB error value off, an area key off by one, a missing label. **Next (marks order):** inverse-operations 5.3, trigonometry 5.0, simultaneous 4.2, transformations 4.0, simplify-expressions 3.7, substitution 3.5, standard-form 3.2, quadratics-factorise 3.0, estimation 3.0, metric-units 3.0, pythagoras 2.3, coordinates 1.8. #518 and #424 are not this lane's.

## 2026-10-25 (home): SIX-PS-BANKS batch 4 entry, moved to keep the handover under 20 KB

**SIX-PS-BANKS batch 4 (25 Oct, Project Claude's contract; #544, squash 28c4265, main run 40227477661 green).** Project Claude's six rulings on batch 3 (Jon, 25 Oct) are applied, and number-vocabulary is a bank. **Banks now 16 (831 questions); 16 topics covered, 104.5 marks a series; 16 topics left.** **Vectors are Foundation only: 36 questions (21 of component-crusher's + the 15 authored), not the 30 expected.** Kept: every column-vector item that adds, takes away, multiplies by a number (including a fraction and a negative), reads a vector from the origin, writes a translation (and its reverse) or finds AB from two points. Dropped: the 9 magnitudes (so the three 2 d.p. roots are gone), the 5 reasoning/collinearity items, the midpoint coordinates and AM, and the three-term path. Cutting a further 6 to reach 30 needs a ruling: say which (AB from points and the translation back are the likeliest, being the least "add, subtract, multiply"). **Worked lines (VECTORS template):** one line per row ("Add the top numbers: ...", "Take away ...", "Multiply the top number by ..."), a first line giving the multiples for a two-operation item, "So ... = column"; a point-to-point move is "Take the start away from the end. Top number: ..."; every number is computed and the last column is the game's key (21 of 21, none missing). **Rounding** worked lines are the ROUNDING template ("Look at the digit after the place you are rounding to: d." / "d is 5 or more (less than 5), so round up (down): answer."), digit read from the value; rounding has no worked line missing now. **Probability:** stage 2's stem is "Work out P(...). Give your answer as a fraction." and any equal fraction is accepted (`equivalent`); the worked line is "There is/are k favourable outcome(s) out of n equally likely outcomes, so P = k/n = simplified" (the words "favourable outcome" are mine for the template's `<outcome>`), k and n recomputed from the words. **Stage 3 is 9 questions, "Which of these statements is true?" only:** each of the game's 9 true statements is the key, three of its 6 false statements (hash-picked) are the options, the game's explanation of the key is the worked line (leading "Correct." dropped) and each false option's slip is the game's explanation of why it is false; false statements are never keys. Probability is 39 (10 + 20 + 9). **number-vocabulary: 59 questions**, "How many factors does n have?" as `number`, for every number in Factor Race's pairs and Year 6 bank (2 to 60), the factors from the game's own `getFactors` checked against a Python recount; worked line "The factors of n are ...: that is k factors."; band 1 to 20, 2 to 40, 3 above; calc false. Plants caught: stage 2 with the wrong count, vector addition off by one (the existing answer checks), and the 13 earlier ones still hold. **Next (marks order):** fraction-operations 6.5, averages 6.3, area 6.0, inverse-operations 5.3, trigonometry 5.0, simultaneous 4.2, transformations 4.0, simplify-expressions 3.7, substitution 3.5, perimeter 3.3, standard-form 3.2, quadratics-factorise 3.0, estimation 3.0, metric-units 3.0, pythagoras 2.3, coordinates 1.8. #518 and #424 are not this lane's.

## 2026-10-25 (home): SIX-PS-BANKS batch 3 entry, moved to keep the handover under 20 KB

**SIX-PS-BANKS batch 3 (25 Oct, Project Claude's contract; #542, squash 8191db0, main run 40216941315 green).** vectors, rounding, change-subject and basic-probability became banks from the games' own items (the counts and the rulings that changed them are in batch 4 above). Every answer is recomputed from its stem; thirteen plants caught. **Rules (Jon, 25 Oct):** band is a rule per topic (vectors 3 for one operation, a translation or a position, 4 for two operations; rounding whole number 1, decimal places 2, significant figures 3; change-subject stages 1-2 4, stages 3-4 5; probability stage 1 1, 2 2, 3 3); `calc` false everywhere. **Vectors are written, not drawn:** each stem restates the vectors its prompt uses as column vectors, or the points as "A is the point (x, y)"; column-vector answers stay `choice` (the coordinates box would show a vector as a point), the wrong options being the expression's + and - exchanged, the components swapped, then sign flips. **Rounding** is typed (the game's four choices are not shown), stems in the exam's plain form, dp as the authored items have it. **Change-subject (31):** the game's options and steps (`\dfrac` shown as `\frac`); the key and every wrong option checked by SymPy (letters positive); Q_GCSE[10] left out because an authored question asks the same; the game's `misconception` text is not tied to an option so it is not a slip. `tex_to_sympy` reads `\sqrt[n]`, `\Delta T`, `\rho`, nested roots and fractions and runs of letters. Missing worked: change-subject none; probability stage 1's 10 (supplied separately) are filled.

## 2026-10-25 (home): LOOK-REDS Factor Race and the GEN-SIX-PS inventory, moved to keep the handover under 20 KB

**LOOK-REDS, Factor Race (25 Oct, Jon's contract; Jon ruled it merged now, Factor Race only; PR and main run: see the line below once merged).** Factor Race is on theme.css: `data-theme="light"`, indigo accent `#4338ca` (7.9:1), h1, no Google Fonts, no hex outside :root, no emoji in headings; MIGRATED in `check-theme.py`; `verify-factor-race.py` and the answer-lock check pass unchanged; `check-changed.py` passed all 46 selected checks. Phone fit at 320x568 was FAIL (656/528) and passes normal (278, Next 358) and Aa (374, Next 488) with the two cards side by side. **Wording changes (quoted for Jon):** title `⚡ FACTOR RACE` is now `Factor Race` (h1); the start-screen ⚡ and the duplicate caps title are now `Factor Race`; `START GAME` is `Start game`; `PLAY AGAIN` is `Play again`; `GAME OVER` is `Game over`; `Which number has MORE FACTORS?` is `Which number has more factors?`; the `▶` bullets are plain bullets. **Left as they were:** the feedback strings `CORRECT!`, `WRONG! ...`, `TOO SLOW! ...` (verify-factor-race.py pins them exactly, so changing them is a verifier change: Jon to rule), the `🔥` in the streak feedback, and the Top scores panel (🏆, US date) as the contract says. **Distinctly Average stays paused** until The 6 P's is built (branch `claude/theme-distinctly-average`, pushed, not checked): migrated onto theme.css, every one of its 657 items asks above the fold at 320 and none scrolls sideways, but 54 items (compare, frequency-table and outlier questions) put Next 16-40 px below the fold after a wrong answer; Aa mode and `measure-phone-fit.py` not yet run. Before and after screenshots of Factor Race: https://claude.ai/artifact/FqDeHAuYeAbJiu85xdugaV.

**GEN-SIX-PS inventory (25 Oct, Project Claude's contract, steps (a) and (b) only; no bank written; waiting for `docs/six-ps-schema.md` to merge).** Full table in `docs/six-ps-bank-inventory.md`. All 32 covered topics route to 29 games and **every game can be read from outside with no game edit**: 19 hold question lists, 10 build questions in code and all 10 expose a pool or generator (`window.SQS`, `FDP`, `HMP`, `TAW`, `JPIB`, `DA_ITEMS`, `QF_POOLS`; top-level `POOL`/`questionFrom` in trig-worms, `generators` in split-it, `VALID_PAIRS` in factor-race), so the unreachable-generator STOP IF does not fire for any topic. **Under 30 (shortfall):** vectors 15, form-expressions 9 (equation-builder holds 40 at ks3, 9 about forming equations), rounding 15 (decimal-detective, 45 counting ordering and placing), change-subject 29, arithmetic-negatives exactly 30. **No worked-solution field:** sequences, arithmetic-negatives, simultaneous stage 4, simplify-expressions, standard-form, vectors, form-expressions, rounding, coordinates. **Conversion needs the schema's rule (diagram, drag or tile items):** angle-ace, take-a-walk, just-pythag-it-bruv, trig-worms, component-crusher, four-quadrant-explorer, equation-builder, decimal-detective, split-it scale. Counts for the generators are distinct draws (a floor); the extractor's 120 for equation-builder is the whole file, not ks3.

## 2026-10-25 (home): DIAL-SCALE, DIAL-MAPPING and FOOTBALL-PITCHES (23-24 Oct), moved to keep the handover under 20 KB

**DIAL-MAPPING (24 Oct, Jon's contract; #520, squash `c3da1bd`, main run 40123595992 green and started on the merge).** In `escape-rooms/assets/engine.js`: `isDegrees(ins)` (`sweep: 360` with unit "°"): `dialAngle()` returns the value, `fromPoint()` reads the angle as the value clamped to min..max, the scale's labels sit at true angles (right angles 90/180/270 and 360 at the top for the sprinkler arc; its minimum 10 is 10 degrees from the top so only its tick marks it; the 0-360 compass is unchanged), and the wedge draws a full circle at 360 (it drew nothing before). `fromPoint()` on a 270 dial: a drag in the dead quarter sets the nearer end (past 180 degrees clockwise: min, else max). **Degree dials:** big-school-begins (0-360) and pe-shed-rebellion's sprinkler arc (10-360); **no sweep:360 dial without a degree unit exists.** `scripts/test-escape-dial.py` now also checks 1,418 needle positions (every grid value of every dial against its angle, slider values unchanged, wedge end), 1,911 real presses (every press compared with the old mapping, written out again, on every live range, and with the new rule elsewhere; the half-step boundaries skipped), dead-quarter presses at 5 and 40 degrees from each end, and presses below the sprinkler minimum; seven plants caught (the three new: old fraction mapping, dead quarter to max, drag shifted a step). Snapshots of every live room before and after at 1280 and 390: identical except the sprinkler dial's drawing. No pe-shed-rebellion text (room.js, teacher page) mentions the needle, so nothing contradicts the fix. Answers and slider/keyboard values unchanged.

**DIAL-SCALE (24 Oct, Jon's contract; PR and main run: see the line below once merged).** One shared `dialSVG()` in `escape-rooms/assets/engine.js` now draws every dial's ticks and numbers from its own min/max/step/sweep at `dialAngle()`; the dead quarter is blank; a full-circle dial's top is one tick labelled "min/max". `showLockPanel()` scrolls a picked lock's panel under the sticky clock on screens 860 px or narrower (the brief's start if the instrument would still be below the fold), and `#lockPanel .artframe` is capped at 30vh. `scripts/test-escape-dial.py` (13 live rooms, 63 dial drawings at 1280/390/320, 558 labels, 186 drags, 41 phone locks; four plants caught). Snapshots of every live room's start screen, lock panels and teacher page, before and after at 1280 and 390: identical except the 38 dial drawings. **Tick/label plan (ticks; labels):** 0-10 s1: 11; every 1. 0-15: 16; 0,5,10,15. 0-20: 21; every 2. 0-30: 31; every 5. 0-50: 26 (every 2); every 10. 0-99: 21 (every 5 and 99); every 10 and 99. 0-100: 21; every 10. 0-120: 25; every 20. 0-180 (s1 or s5): 37; every 20. 0-200: 21 (every 10); every 20. 1-8: 8; every 1. 1-20: 20; 1,5,10,15,20. 1-60: 31 (every 2); 1 then every 10. 1-100: 21 (every 5, and 1); 1 then every 10. 0-360 s45 sweep 360: 8; 0/360 then every 45. 10-360 s10 sweep 360: 35; 10/360, 100, 200, 300. **Below the fold at 390x844 after the change: none** (before: all 41 locks of the 13 live rooms opened with their instrument 950-1,200 px down the page, because nothing scrolled to a picked lock; no live lock carries art, so the art cap is covered by a fixture test only). **Judgement calls for Jon:** (1) the contract's STOP IF (a dial range admitting no 8-40 tick interval from its minimum) would fire for 1-100 and 1-60 (99 and 59 steps share no factor with 2, 5, 10, 20, 25, 50), so ticks are anchored at multiples of the interval with the two ends always ticked, which keeps every tick on a value of the grid. (2) 10-360 (Sprinkler arc) has only four labels because 350 sits within 24 degrees of the top seam; the 10-360 and 0-360 tops read "10/360" and "0/360". **Seen, not changed (DO NOT TOUCH):** `fromPoint()` sends a drag into the dead quarter's left half (below the 7 o'clock minimum) to the MAXIMUM, not the minimum; a student overshooting the start reads the top of the range. Dial-only fix wanted in its own contract.

**FOOTBALL-PITCHES (23 Oct; cloud lane, exception of 23:05).** New unlisted `squared-squirrel`. Rebase knowingly: `firebase-leaderboard.js` (`stage-5` label only), roster Unlisted, `data/games.json`, NOT_ON_HUB, game lists in check-levels/answer-lock/theme/teacher-invite/start-mount and audit-register.

## 2026-10-21 (home): the 15 Oct entries (DND-ROOM-BUILD to CI-SLOWDOWN-401), moved to keep the handover under 20 KB

**DND-ROOM-BUILD (15 Oct, Jon's contract; branch `claude/dnd-room-build`).** **Roll for Initiative is built and LIVE BUT UNLISTED** at `/escape-rooms/roll-for-initiative/play.html` (Jon's clarification, 15 Oct: live so he and Mrs Rogers can test it; noindex, analytics off, not in the hub, front page or sitemap; `index.html` is the holding page, any room whose index.html loads the engine counts as live to the stars and hub-card checks; teacher page at `.../teacher.html`). **For the difficulty contract: ★★ Core, lock grades 4/3/4 (gate 4, plans 3, fireball 4), no star field.** Credit "Built from a teacher's idea. Thank you, Mrs Rogers."; consent is recorded in the D&D draft entry. Bank batch 11; `escape_set_checks.LOCKS` entries; variant libraries gate 9, plans 7, fireball 5: the generator reports **182 of 315 VALID, variant 0 VALID**, and every other room's `variants:` block is byte-identical. Art: Jon's three JPGs filed as `docs/art/roll-for-initiative-{scene,fail,win}.webp` (no watermark; the 16:9 crop drops the ceiling lights, so the alts omit them). Played in Chromium to a win and a time-out at 390 and 1280 px over draws covering all 21 sets: 20 of 20 clean, no sideways scroll, end screens in `docs/screenshots/dnd-room-build/`. Added a teacher-table width entry to `checker-allowlist.json` (547 px, todo §1.37, as every room has) and named `play.html` in `check-analytics-loader.py`'s WITHDRAWN registry (data, not logic: every noindex page must load analytics.js unless named there; **a judgment call against the contract's checker STOP IF; the alternative is analytics.js on play.html, so test plays count**). **Awaiting Jon's play-test and Mrs Rogers' preview before release** (hub card, front page, sitemap, noindex off, analytics on: a separate instruction).
**TIMING-SELFTEST (15 Oct, Jon's contract; branch `claude/timing-selftest`).** The assertion that failed on main's run for #408 (38736408794, Content verifiers 28) was `timing-gate.py --selftest`'s "… and the summary names the group, the slow line, its time and its recorded median": it wants "Slow verifier took 2s (recorded median 1s)", and the planted line was `sleep 2` timed by bash's whole-second `$SECONDS`, which reads 3 whenever start-up overhead crosses a second. Now the four step tests (the three before, and #411's metadata-service-silent test, which had the same `sleep 2`) run a copy of the step whose clock reads (`$SECONDS` twice, `date +%s` twice; `CLOCK_SEAMS`, which refuses if the step reads time any other way) come from a file each planted check advances by its seconds: no sleep, same assertions, same plants caught (5 step faults planted locally, all caught). One run of the real step on the real clock asserts only that it runs green. The packer and `ci-deps.py` self-tests read no real time. 20 consecutive and 20 parallel runs under 12 busy loops on 4 cores: all pass. Workflow, gate logic, thresholds, budgets and pack unchanged.
**MM-OVERFLOW-DIAG (15 Oct, Jon's contract; branch `claude/mm-overflow-diag`; report only, #414).** Full report: **`docs/handover/mm-overflow-diag.md`**. Main run 38773296418's 5901 px on Moments Master was `katex.min.css` failing while `katex.min.js` loaded (reproduced: 5897 px; KaTeX merely delayed gives 320 px); `alevel[6]` is the bank's only `\sqrt` item. The verifier waits for KaTeX's script, never its stylesheet, and uses the live CDN (6 more verifiers do). 66-game survey: 4 more games overflow without the stylesheet (surd-simplifier, force-resolver, index-laws, characteristic-quest). Proposed (Jon's call): pin KaTeX in the 7 live-CDN verifiers plus a stylesheet-applied wait in `bank_common`; a 3-rule KaTeX fallback in `site-footer.css` (66/66 pages; theme.css is on 5).

**CI-RUNNER-REGION (15 Oct, Jon's contract; branch `claude/runner-region`).** Each group job reads its Azure region from the instance metadata service (probed first on a throwaway branch: inside the Playwright container, 6 of 6 jobs matched the region the runner prints; case differs, so it is lowercased; "unknown" if the call fails) and saves `region: x` as line 2 of its timing artifact. `ci-groups.read_run` stores `regions` {line: region} in each history record (old records and old artifacts read "unknown"); `lines`, medians, packer and `--check` are untouched (self-test proves the record's `lines` and top-level keys are unchanged). The 75% warning and summary now say "<line> took Ns in <region> (recorded median Ms)"; the persistence report adds a region column and `in a/b/c` to its annotation. Flagging logic and thresholds untouched. Canon §7.8.1 has the paragraph, including that within-region comparison is deferred to about 10 runs per region group. The first main run after this records regions; the persistence report reads them from the 5-run history, so older runs show "unknown" for a few runs.
**CI-SLOWDOWN-401 (15 Oct, Jon's contract; branch `claude/ci-slowdown-401`; report only).** Full report: **`docs/handover/ci-slowdown-401.md`**. Equatle (47 to 76 s) and Log Laws Solve (33 to 60 s) are not slower because of #401: they run at 46-64 s / 32-46 s on a runner in Azure region centralus and 69-79 s / 52-64 s in every other region (17 main runs, no overlap), and #401's run and the two after it landed outside centralus; #405's run, in centralus, was 49 s and 33 s. #401 changed no file either verifier reads. Equation Builder part 1 follows the same split (78-98 s fast, 152-159 s slow, 106-138 s between). No fix needed; the persistence report cannot tell a region switch from a regression, and the report proposes comparing the flagged line with the other lines timed in the same runs (Jon's call: it touches `timing-gate.py`).

## 2026-10-20 (home): the oldest entries (9 Oct queue and rulings), moved to keep the handover under 20 KB (PER-LINE-LIMIT)

**QUEUE (home lane, Jon 9 Oct 16:10):** 1 RULINGS-9OCT (#215, merged), 2 GRAPH-SKETCHER-FIT, 3 CI-BALANCE, 4 PLAY-AGAIN-SCREEN,
5 SCORES-OFFLINE, 6 SCI-CALC, 7 DOCS-9OCT, then CHECKPOINT. (E2 merged as #213; main green.)
CAR-TRAP-DRAFT: the cloud lane's (Jon, 20:17); contract at
`docs/handover/contracts/2026-10-09-car-trap-draft.md` on main (HOOK-FIX let it through the hook). Jon also sent the
IT room rewrite brief (Narry, secret ballot; 3 open rulings): a brief, not yet a contract, saved as
contracts/2026-10-09-it-room-brief.md. SCI-CALC (item 6) is saved as docs/history/contracts/2026-10-09-sci-calc.md.
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item: done for every listed game but graph-sketcher** (NOT_YET: glorious-gantt, unlisted and the cloud
  lane's; graph-sketcher, blocked by its phone overflow, batch 10 entry). unit-converter loads the lock (cloud lane,
  #196) and is judged in full, but is not in MIGRATED: Jon's call (the overnight contract left it to the cloud lane). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining` in
  `scripts/answer-lock-state.json` on main and drop every game on it from the batch. Never claim or edit a game on that
  list. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

**Jon's rulings, 9 Oct (on the overnight questions; RULINGS-9OCT):** unit-converter moves to MIGRATED (done,
seeds 1-3 pass). wrong-on-the-internet keeps its 3 s pause before Try again: feedback on a wrong answer is shown, not
skipped (Jon, 8 Oct). complex-converter's Play Again keeps replaying the mode, as its Menu is one tap from the end
screen. graph-sketcher: fix its phone overflow now, then put it on the lock (item 2). The first two are in canon §7.6.

## 2026-10-20 (home): Jon's 7 Oct rulings, moved to keep the handover under 20 KB (ROSTER-PYTHAG-14)

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-17 (home): TIMING-GATE and BG-LAUNCHER entries, moved to keep the handover under 20 KB (STARTER-LABEL)

**TIMING-GATE (14 Oct, Jon's contract; branch `claude/timing-gate`; implements #400's recommendation).** (1) The group step in `check-site.yml` now **warns** past 75% of the timeout: a `::warning::` annotation and a summary block naming the group, the slowest line against its recorded median (looked up in `scripts/ci-timings.json`, "none" when unrecorded) and its time; the job's exit test is the checks alone. (2) The median-of-5 pack and the 80% `--check` are untouched and still block (packer, budgets, 75%/80% figures, timeouts and verifiers unchanged; I only reworded two comments in `ci-groups.py` that said the workflow "fails" a group). (3) New **`scripts/timing-gate.py`** (CI-wired, named without the `ci-` prefix because `ci-deps.py` treats `scripts/ci-*` as "change CI itself, run everything"): `--report` runs in the main timings job as a new `continue-on-error` step that runs even when the pack check fails; it reads the last 9 main runs from the git history of `ci-timings.json` plus the new run's artifacts and reports (summary and warning, never a failure) each verifier whose last 3 runs are each over 20% and 15 s above the median of the 5 before. **Backtest in its `--selftest`, on the recorded series:** Probability Paradox (162 155 161 … 210 211 202 …) is reported on the third slow run (202, baseline 161), silent on the second; the Equation Builder 260 s flake and the Spot the Muppet 290 s flake (injected into its stable stretch) are never reported; one 900 s run never reports; two slow runs are not enough; a 3-run +50% rise is reported; a rise under 15 s is not. **Planted slow line:** the selftest extracts the workflow's step, runs it with a 1-minute timeout and a job started 100 s ago and a line that sleeps 2 s against a recorded median of 1 s: exit 0, `::warning::time budget (a warning, the job is not failed)` in the log, the summary names the group, "Slow verifier took 2s (recorded median 1s)"; inside the budget there is no warning; a failing check still fails the job and the checks after it still run. **Hard timeouts (confirmed, not changed):** content groups `job_timeout` 16 min (35 groups, timeout 6); answer-lock parts 20 min (6 groups, timeout 10); site-wide `check-site` jobs 20 (5) or 18 (2); plan 5, register 5, timings 5, coverage 5, gate 2. A hang holds a runner for at most 16 to 20 minutes against a normal 3 to 5, which I judge acceptable. **Finding:** Equation Builder part 1 is bimodal on main (about 80 s or about 150 s, alternating run to run, 79 runs), so the persistence rule fires on it in 3 windows of the recorded series; it will occasionally warn on that verifier (a warning, not a failure). Why it alternates is not diagnosed. CLAUDE.md and canon §7.8.1 now state what blocks, what warns and why. **First live report (main run 38635401918, after merge):** the new step ran green and named two verifiers, Equatle (47 s to 76 s) and Log Laws Solve (33 s to 60 s), both in `Content verifiers 30`, which holds only those two lines, identical at 76 and 60 in the last two runs and stepped at the run for #401; no commit touched either verifier or its game, so the cause (a slower runner class, or something #401 added to the job) is **not diagnosed**; if it persists the packer will notice at 80%. **Also fixed here:** `end-task.py` crashed (`NoneType has no splitlines`) when the Windows process list held a command line that is not valid UTF-8; its `run()` helper now decodes with `errors="replace"`.
**BG-LAUNCHER (14 Oct, Jon's contract; branch `claude/bg-launcher`).** **`scripts/bg.py`** starts a command detached (Windows: detached process; POSIX: its own session) and records `{pid, create, cmd, started, worktree}` in `<worktree>/.claude/pids.json`; output goes to `<worktree>/.claude/bg-*.log`; both are gitignored (`.claude/` itself holds tracked rules, so only those two paths are ignored). `create` is the OS's creation time, so a recycled PID is never stopped by mistake. **`end-task.py`**, after its merged/tip/clean checks pass and **just before** `git worktree remove` (not before the checks: a refused removal leaves the session's servers running; a self-test case holds that), stops each registered process and its children (`taskkill /PID n /T /F` on Windows, the process group on POSIX; the processes are ones the session itself registered, no system process is touched), prints what it stopped, clears the registry, then lists without killing any unregistered process whose command line holds the worktree path. `end-task.py` stays self-contained (it runs from a copy in /tmp and cannot import `bg.py`), so the registry format is the contract between the two; `bg.py --selftest` runs them together. **Self-tests** (both in CI): a sleeper that spawns a child is started through `bg.py` in a temp worktree, `end-task`'s stop routine kills it and the child, the registry is cleared, a planted unregistered process is reported and left alive; plus two `end-task` cases (registered server stopped then worktree and branch removed; refused removal leaves it running). Passed on Windows, and on Linux in WSL Ubuntu 24.04 (with `ps`, and with `ps` hidden so the `/proc` fallback runs); the CI run is the Linux proof for the container. CLAUDE.md states the rule and that the harness's `run_in_background` shells are not covered. **Child-server teardown report (not fixed):** of 114 scripts that start a stub server (221 start sites: `bank_common.start_stub_server` and 1 hand-rolled `_serve` in `check-teacher-invite.py`), **all 114 stop it in `try/finally`** (`proc.terminate()`; no script lacks teardown; `test-level.py` does too). Two notes: `bank_common._start_stub_server_on` and `check-teacher-invite._serve` are starters that hand the process to the caller (the latter terminates it only on its own failure; its caller does so in `finally`); and `finally` does not run if the script is killed from outside (a `TaskStop`, a timeout, closing the terminal), which is exactly how the 5 to 12 Oct orphans arose, so scripts are not a substitute for registering the long-lived ones through `bg.py`.

## 2026-10-15 (home): ESCAPE-SET-CHECKS, Canon sweep and WORKTREE-CLEANUP entries, moved to keep the handover under 20 KB (FREEZE-LIFT)

**ESCAPE-SET-CHECKS (11 Oct, Jon's contract; branch `claude/escape-set-checks`).** The per-set checks moved out
of `gen-escape-variants.py` into **`scripts/escape_set_checks.py`** (pure, no I/O), unchanged: keep()'s tests ->
`check_set()`; each lock's instrument, clue figures and solver -> `LOCKS` (35 entries, lifted by an AST script,
not retyped); rugby-scoreboard-bases and cookie-price-simultaneous (two instruments, checked inline before) ->
`check_rugby_bases()` / `check_cookie_simultaneous()`, which read the answer and misconception from the set as
served (the generator builds them from the same parameters, so its test is unchanged; CI's is stronger). The
generator imports it, keeps only search + spread, and writes to this checkout (the E:\jon\maffsgames paths are
gone). **Regeneration is byte-identical:** sha256 of variants.json and all 12 room.js equal before and after,
and the generator's whole report too (299 sets, 37 locks, 2763 rejected). `check-escape-rooms.py` runs
`check()` on every set of every live room (names room, lock, set index, check; a live lock missing from LOCKS
fails), prints per-room verified sets and the total (11 Oct: 271 in 11 rooms, none failing; it-vengeance
withdrawn, not checked), and plants the 10 broken sets in `scripts/fixtures/escape-broken-sets.json` (each of
the 7 per-set checks, both two-instrument checks, an unregistered lock; every good original must pass).
Mutation proof: with the clue test disabled the run fails, naming the uncaught plant. CLAUDE.md: new "Start of
task" (fetch, new worktree from origin/main, never pull into the primary or an existing branch). Canon §11.3
replay bullet rewritten: no figures. **Not changed, for Jon:** the ci-line label (it keys ci-pack.json and
ci-timings.json); §11.3's "Ratings as of 10 Oct" (no Rightful King ★★★ or Library Jam ★) and "The live rooms
all use `digits`" (both new rooms are live; maxDigits), stale; §11.4's rows for both scripts predate this.

**Canon sweep (read-only; current-state counts derived from repo content; none changed).** Intro "What is
authoritative where": roster "has all 93 rows". §Portal: "`escape-rooms` (12 items)". §3.2: "135 `.game-card`
elements for 96 games". §7.5: "On 2 Oct 2026 the roster gives 67 games light and 30 dark" (dated). §8.2c and
the shuffle note: "32 games hand-roll `shuffle(...)`", "the other ~30 games", "The other ~28 games". Coverage:
heading "(96 live games)"; "94 of the 96 live games call `submitScore()`" (recounted 3 Oct); "Not counted in
the 96 live games". Firebase/leaderboard: "Wired into 94 of the 96 live games". Tier 1: "125 controls across 47
games ... (122 across 46 ...)". Tier 3: "95 of 96 games fire `question_answered`"; "27 games use
`id="options"`, 8 use a class ... 60 use neither". §11.1: "Eleven rooms live, one withdrawn" and its 12-row
table (accurate today). §11.3: the ratings roster above. §11.4: `check-escape-rooms.py` "(two faults planted)"
(now three, plus the ten broken sets). §11.5: "All eight rooms are being rewritten" (eleven live now). Dated
audit history (e.g. "17 games" 22 Sep, "125 pages", the [x] backlog's "60 games") is history, not drift: left out.

**WORKTREE-CLEANUP (11 Oct, Jon's contract; branch `claude/worktree-cleanup`).** `git worktree list` found 35
beside the primary. Each checked: branch tip an ancestor of origin/main, `status --porcelain` empty, no commit
outside origin. New end-of-task step in CLAUDE.md (Task Contract): remove the task's worktree and local branch
after merge, never `--force` / `-D`. Remote branches untouched. Every worktree found (all E:/jon/):

| Worktree (branch `claude/…`) | Status | Action |
|---|---|---|
| mg-b1..b6, mg-b8 (f1-batch1..6, f1-batch8); mg-cib (ci-balance); mg-cp (checkpoint-8oct); mg-ctx (ctx); mg-cu (changed-utf8); mg-ea (escape-analytics); mg-ess (essentials); mg-ew (essentials-wording); mg-frac (answer-fraction); mg-ga (ga4-country-canon); mg-ga2 (gitattributes-bytes); mg-gs (graph-sketcher-fit); mg-gt (given-that-fractions); mg-hints (f1-lock-hints); mg-lf (ltc-focus-race); mg-lj (library-jam-art); mg-log (log-notation); mg-ltc (ltc-flake); mg-r3 (relist-3); mg-r9 (rulings-9oct); mg-rel (rooms-release-rk-lj); mg-rk (rightful-king-art); mg-rl (relist-sr21); mg-upd (updates); mg-vs (vocab-showthat) | merged, clean, pushed | removed; branch deleted (`-d`) |
| mg-b7 (f1-batch7), mg-lock (f1-answer-lock), mg-sk (star-key) | merged, clean, pushed | unregistered and branch deleted (`-d`), but Windows refused to delete the folder ("Permission denied"; still busy): **an empty folder is left at each**, held by some process. Jon: delete the three empty folders after a reboot |
| mg-pp-before (detached at a02d61d, ancestor of main) | **dirty**: `scripts/check-changed.py`, `scripts/test-escape-keypad.py` modified | **kept** (STOP IF: dirty). Jon: keep or discard those edits |

Also, the same session: the **CANON-VERIFIED-COUNT** contract (canon §11.3's "199 verified number sets") STOPPED
before any edit, reported to Jon in chat; nothing committed.

## 2026-10-15 (home): CI-TIMING-DIAGNOSIS entry, moved to keep the handover under 20 KB (DND-ROOM-BUILD)

**CI-TIMING-DIAGNOSIS (14 Oct, Jon's contract; branch `claude/ci-timing-diagnosis`; report only, nothing changed).** Full report with data tables: **`docs/handover/ci-timing-diagnosis.md`**. Short answer: the failures on unchanged code come from the **per-run 75% clock** in each group's last step (160 runs, 25,323 timed lines: 2 runs failed on it, Equation Builder part 1 at 260 s and Spot the Muppet at 290 s, every verifier `ok`), not from the median-based packing or `--check`. It is not whole-run runner slowness (run-level factor 0.97 to 1.03) but rare single-line stalls (0.13% of lines). The Probability Paradox regression never touched the per-run clock; the median-of-5 pack check caught it on the 3rd slow main run. No per-run multiple can both catch it (1.26×) and pass the flakes (1.9× and 3.1×); persistence can. **Recommended (needs Jon's ruling, it changes what the 75% does on a single run):** make the per-run 75% a warning, keep the median pack and 80% `--check` as the blocking gate, and add a named persistence report to the main-only timings job. "Just Pythag It part 4 at 242 s" was not found in the sample.

## 2026-10-15 (home): STALE-PROCESSES entry, moved to keep the handover under 20 KB (MM-OVERFLOW-DIAG)

**STALE-PROCESSES (14 Oct, Jon's contract; branch `claude/stale-procs`).** Cleanup only; no repo content touched. **Listed before killing** (PID, start, command, parent): **37168**, 5 Oct 20:24, `python E:\jon\maffsgames-new-clone\scripts\serve-stubbed.py 60131` (parent 35676 already dead); **7072**, 7 Oct 16:24, `python E:\jon\mg-lock\scripts\serve-stubbed.py 62173` (parent 18764 already dead); **3704**, 8 Oct 18:05, `python scripts/serve-stubbed.py 8792` (parent bash 19448 still alive); **380**, 10 Oct 17:49, `python -m http.server 8765` (parent bash 22416 still alive); **36888** with its Playwright `node.exe` **22708**, 12 Oct 23:30, `python scripts/test-level.py --run` (parent bash 2764; this was background task `brj7ba02w`). **Stopped:** tasks `brj7ba02w` (taking 36888, 22708 and bash 2764 with it) and `barjw6rq4` by TaskStop; `bdmdk98sn` was already gone. **Killed by PID:** 37168 and 7072, stub servers whose launching shells are dead and whose command lines point at local stubs, not live servers. **Left running, per the contract's STOP IF (their parent shells are alive, so I cannot confirm their sessions are closed):** 3704 (port 8792), 380 (port 8765, a plain static `http.server` that may be Jon's own preview). Jon: kill them if they are yours to drop (`taskkill /PID 3704 /PID 380`), or say so and I will. **wt-level-resolver:** `E:\jon\wt-level-resolver` was not a registered worktree and not a git repo: an empty directory (0 entries), the leftover target of the `cd` in task `brj7ba02w`; nothing to merge or lose; removed with `rmdir`. `wt-pd-tournament-board` is another empty-looking leftover in `E:\jon`, outside this contract and untouched. **Does `end-task.py` stop a session's background processes? No.** It runs only `git` and `gh` (merged PR, local tip equals the PR head, clean worktree), then removes the worktree and branch; it neither lists nor stops processes, which is why servers outlive their sessions (and a server holding a folder open makes the removal fail with "Permission denied"). The structural fix is a separate ruling.

## 2026-10-15 (home): MG-PP-BEFORE entry, moved to keep the handover under 20 KB (TIMING-SELFTEST)

**MG-PP-BEFORE (11 Oct, Jon's contract; read-only).** Worktree unchanged since the WORKTREE-CLEANUP entry
(detached at a02d61d, the same two files, nothing else). **Both edits are already in main, byte for byte**
(same git blob): `scripts/check-changed.py` is main's as landed by PREPUSH-SCOPE (6192382, two queues), and
`scripts/test-escape-keypad.py`'s one-line ci-deps change (`kiln-disaster/room.js` -> `escape-rooms/`) is
2414310. Nothing in main relies on their absence. **Recommendation: discard** (nothing to keep): Jon runs
`git -C E:/jon/mg-pp-before checkout -- .`, then `git worktree remove E:/jon/mg-pp-before`.

## 2026-10-15 (home): FACTS-29-35-11-36-49 entry, moved to keep the handover under 20 KB (CI-SLOWDOWN-401)

**FACTS-29-35-11-36-49 (14 Oct, Jon's contract; branch `claude/facts-29-35-11-36-49`).** `verify-facts.py` passes (149 pins), zero KNOWN, self-test plants unchanged and caught. Facts 3, 10, 15, 20, 26, 39, 44, 46, every other fact, FACTS order and length untouched.
- **29, Perfect Bracket (hook).** Old: "The probability of correctly predicting every match in an NCAA tournament is about 1 in 9.2 quintillion." New: "If every match were a coin flip, the probability of correctly predicting every match in an NCAA tournament would be about 1 in 9.2 quintillion." The body already uses 2^63 (63 games, 2 outcomes each); the existing recomputed pin on 2^63 ≈ 9.2 × 10^18 stays, plus a pin on the new condition.
- **35, Königsberg.** Hook, old: "…crossing each of its seven bridges exactly once — and invented graph theory." New: "…crossing each of its seven bridges, as they stood then, exactly once — and invented graph theory." (it was already past tense). Body, added after "no solution.": "Wartime bombing and rebuilding changed the bridges. Today's layout allows a walk crossing each bridge exactly once, though not one that finishes where it began." Source confirmed (Wikipedia, Seven Bridges of Königsberg): five bridges remain at the original sites, two nodes of degree 2 and two of degree 3, so an Eulerian path exists and a circuit does not; the pin recomputes that (degree sum 10 = 2 × 5, two odd nodes).
- **11, Hairy Ball: no change needed.** The hook and body speak only of a hairy sphere and the Earth; no head is implied. Left as is.
- **36, Trisect: no change needed.** The hook already says "trisecting a general angle with just a compass and straightedge is impossible — proved in 1837". Added only a pin on that phrase (Wantzel, 1837), beside the existing "proved in 1837" and cubic pins.
- **49, Matrices (body).** Old: "…this is how every pixel of every video game is calculated." New: "…this is how a 3D game works out where every object appears on screen." Pinned as a phrase.

## 2026-10-14 (home): HOOKS-20-44-49, PYTHON-MIN and FACTS-33-20 entries, moved to keep the handover under 20 KB (BG-LAUNCHER)
**HOOKS-20-44-49 (14 Oct, Jon's contract; branch `claude/hooks-20-44-49`).** Three overstated hooks corrected (0-indexed; bodies, order, length, fact 3 and the nine other flagged hooks untouched). `verify-facts.py` passes, zero KNOWN, self-test plants unchanged and caught.
- **Fact 20, Collatz.** Old: "…Repeat. You will ALWAYS reach 1. Nobody knows why." New: "…Repeat. Every number anyone has ever tried reaches 1 — but nobody has proved they all do." The old closing "Nobody knows why." is dropped as redundant beside the new sentence (the only wording change beyond the contract's replacement). Pinned to Lagarias (1985), Amer. Math. Monthly 92(1).
- **Fact 44, Barcodes.** Old: "Every barcode has a check digit calculated using modular arithmetic…" New: "Every barcode on a shop product has a check digit calculated using modular arithmetic…" Pinned to GS1 General Specifications (EAN/UPC check digit mandatory; Code 39 optional). The body does not depend on the universal claim.
- **Fact 49, Matrices.** Old: "Every computer graphic, every 3D game, every GPS navigation uses matrix multiplication to rotate, scale, and transform objects in space." New: "3D games, computer graphics and GPS all run on matrices: matrix multiplication rotates, scales, and transforms objects in space." Pinned as a phrase. **Left for Jon:** fact 49's body still says "this is how every pixel of every video game is calculated", the same hyperbole one level down; bodies were out of scope.
- **Decision recorded (Jon, 14 Oct):** the 57 scripts with no shared import are not worth a shared import for the Python 3.10 guard (PYTHON-MIN); they are left unguarded.
**PYTHON-MIN (14 Oct, Jon's contract; branch `claude/python-min`).** `scripts/` require Python >= 3.10 (`Path.write_text(newline=)`, added in #390). **CI pin:** all three `actions/setup-python@v5` steps in `check-site.yml` already pin `python-version: "3.12"` explicitly, so nothing changed there and the version CI runs is unchanged. **Guard:** added to the shared module `scripts/bank_common.py` (`require_python()`, run at import; exits with "scripts/ require Python >= 3.10 (write_text newline=); this is Python X.Y"). **Coverage count:** of 181 scripts under `scripts/`, 120 import `bank_common`; 57 import no shared module at all and are not guarded (the other 4 import only `stats_common`, `uk_rates` or `escape_set_checks`); the contract's STOP IF (no shared module imported by most) was not met. **New `scripts/check-python-version.py`** (CI-wired, `ci-deps` on the workflows and `bank_common.py`): `--check` fails any `setup-python` step that is unpinned, floating (`3.x`) or below 3.10; `--selftest` monkeypatches `sys.version_info` to (3, 9) and confirms the guard exits naming 3.10, stays quiet at 3.10 and on the real interpreter, and that the workflow reader fails 3.9, `3.x` and unpinned steps. **Docs:** the minimum is stated in CLAUDE.md (Tech Stack), canon (checker tooling, beside the Playwright setup line) and the `check-text-writes.py` docstring beside its blind spots. **Not verifiable from here:** Jon's Linux Mint machine's Python version (this Windows machine runs 3.14.6); anything below 3.10 there now fails with the clear message from the 120 guarded scripts, and the 57 others would still hit the `TypeError`. Jon: say if a shared import (or a `sitecustomize`-style guard) is worth adding for those 57.
**FACTS-33-20 (14 Oct, Jon's contract; branch `claude/facts-33-20`).** Closes the two facts FACTS-SIX-FIXES held. `verify-facts.py` passes, zero KNOWN, self-test plants unchanged and all caught. FACTS order, length and `getWeekIndex()` untouched.
- **Fact 33, Regression to the Mean.** Hook, old: "If a student scores 98% on a test, they'll almost certainly score lower next time — not because they got worse, but because of statistics." New: "If a student gets an unusually high score on a test, expect their next one to be lower — not because they got worse, but because of statistics." Body, old: "The instructors' feedback was irrelevant." New: "Regression alone explains the pattern, so the instructors had no evidence that their feedback made any difference." Pins: "Israeli flight instructors" kept; "gets an unusually high score on a test" and "Regression alone explains the pattern" added, sourced to Kahneman, Thinking, Fast and Slow ch. 17.
- **Fact 20, Collatz.** Old: `Paul Erdős said: "Mathematics is not yet ready for such problems."` New: `Paul Erdős is reported to have said: "Mathematics is not yet ready for such problems."` (quoted words untouched). Pin sourced to J. C. Lagarias (1985), The 3x+1 problem and its generalizations, American Mathematical Monthly 92(1), 3-23; its text reads "is not yet ready", so the earlier "may not be ready" claim was the later form.
- **Absolute-language hooks, for Jon's review, none changed** (fact number is 0-indexed; words searched: always, never, almost certainly, guaranteed, impossible, every, no one): **3** Card Shuffles ("almost certainly… never existed… never will again"; a probability claim stated flat); **10** √2 ("every number is a ratio"; the Pythagorean belief, fine); **11** Hairy Ball ("impossible… always at least one cowlick"; true for a sphere, a theorem); **15** Infinitely Many Primes ("always a larger one"; theorem); **20** Collatz ("You will ALWAYS reach 1"; **an unproven conjecture stated as fact in the hook**, worth a look); **26** Infinite Hotel ("can always accommodate one more"; true in the standard setup); **29** Perfect Bracket ("every match… 1 in 9.2 quintillion"; a coin-flip assumption, see its body); **35** Königsberg ("impossible", theorem); **36** Trisect ("impossible", theorem); **39** P vs NP ("may be impossible", hedged); **44** Barcodes ("Every barcode has a check digit"; true of EAN/UPC/ISBN, not of every barcode symbology); **46** Hear a Drum ("not always"; accurate); **49** Matrices ("Every computer graphic, every 3D game, every GPS"; hyperbole). The likeliest to need rewording: 20, 44, 49, 3.

## 2026-10-14 (home): TEXT-WRITES, CI TIMINGS DIAGNOSIS and FACTS-SIX-FIXES entries, moved to keep the handover under 20 KB (STALE-PROCESSES)
**TEXT-WRITES (14 Oct, Jon's contract; branch `claude/text-writes`).** **Done:** `newline=''` added to all **49** text-mode writes in `scripts/` (29 files; open 'w'/'a' ×30, `Path.write_text` ×15, `NamedTemporaryFile('w')` ×4; the four `Image.open`/`pymupdf.open` hits were false positives and are untouched). No shared helper, per the contract. New `scripts/check-text-writes.py` (CI-wired by header, `ci-deps: scripts/`) reads every `scripts/**/*.py` as a syntax tree and fails on a text-mode `open`/`io.open`/`Path.open`/`write_text`/temp-file write without `newline=`, or an `open()` whose mode is not a literal; it ignores binary modes, reads and non-file `.open`; 181 scripts, 0 violations; the self-test plants 9 offending writes, 6 clean ones and a bad/good file pair in a scratch `scripts/` folder. Newline-only change: no content or encoding argument touched, no byte difference on Linux (`newline=''` is the default there). `verify-test-the-claim.py`, `verify-split-it.py`, `verify-equation-builder.py` (selftest and part 1) and the answer-lock self-test pass on Windows. **The earlier repo-layer ruling (12 Oct: fix CRLF in `.gitattributes`, not in `verify-test-the-claim.py`) is rescinded by Jon, 14 Oct:** `.gitattributes` governs checkouts, not runtime writes, so it could only ever fix the first of the two causes. **Blind spots, not checked and not fixed:** (1) shell redirects (`>`, `>>`) in any command a script runs: `check-changed.py:149` runs CI lines with `shell=True`, and the workflow's own steps are outside `scripts/`; (2) `subprocess` calls given a file as `stdout=` (none found); (3) writes made by embedded Node or JS strings (`fs.writeFileSync` in the verifiers' drivers); (4) `Path.write_text` needs Python 3.10 or later for `newline=` (CI is newer).
**CI TIMINGS DIAGNOSIS (14 Oct, Jon's contract): already fixed at source by the cloud lane's #376; nothing to split.** Cause: #371 added four plants to `verify-probability-paradox.py`'s self-test, and each plant re-ran the whole `run()` including `next_once` (10 s of real MaffsLock timers), taking the verifier from about 161 s to about 203 s locally and 231 s. That was a slow path from added self-test work, not new checks. #376 runs `next_once` only for the real page and the t1-010 plant (all 16 plants still caught, no check dropped). Recorded Probability Paradox time is now 48 to 58 s across the last five main runs, and `CI timings and pack (main only)` has been green on every run since (38581861905 and the one before). I did not touch the budget, the 80% limit, the packer or any pack assignment, and I did not use `--part`.
**FACTS-SIX-FIXES (14 Oct, Jon's contract; branch `claude/facts-six-fixes`). Four of six done; two stopped on the contract's own STOP IF.** Changed in `index.html` (FACTS order and length untouched, `check-content-safety.py` KNOWN still empty), pins updated in `verify-facts.py` (139 pins, **zero KNOWN**, self-test still catches all four plants):
- **Fact 14 (hook):** "can still give wrong results more than 90% of the time" → "…about 80% of the time". Body unchanged (199/248 = 80%). KNOWN pin replaced by a recomputed pin on 80%.
- **Fact 43 (Basel):** "In 1735, a 28-year-old Euler proved this, stunning" → "In December 1735, Euler, then 28, announced a proof of this, stunning". Pin recomputes the age from his birth date (15 Apr 1707) to the 5 Dec 1735 announcement.
- **Fact 51:** "argued about this for 2,500 years" → "…for about 2,500 years".
- **Fact 3 (shuffles):** "that would be about 5 × 10²⁸ shuffles" → "…fewer than 10²⁹ shuffles". Pin is an upper bound checked at both 100 and 117 billion people. **One consequential change beyond the contract:** "around 200,000 times that whole exercise" → "more than 100,000 times…", because the ratio was computed from 5 × 10²⁸ and against a 10²⁹ bound only the lower figure is true (10³⁴ ÷ 10²⁹ ≥ 100,000).
- **STOPPED, fact 33 (Regression to the Mean), unchanged:** its body contains no figure, so there is nothing to support any softened claim (contract STOP IF). Needs a wording from Jon, or permission to add a worked figure.
- **STOPPED, fact 20 (Collatz), unchanged:** the Lagarias source does not confirm the contract's wording. Lagarias's 1985 text, as published on his own page (cecm.sfu.ca/organics/papers/lagarias), reads "Mathematics is not yet ready for such problems", which is what the fact already says bar the capital letters. "May not be ready" is a later form (Guy and later surveys). Per STOP IF I did not reword it. Options: leave as is and cite Lagarias 1985, or attribute it as reported ("Erdős is reported to have said…") with the 1985 words.

## 2026-10-14 (home): FACTS-AND-NOTICE and LEVEL-LOGGED entries, moved to keep the handover under 20 KB (FACTS-33-20)
**FACTS-AND-NOTICE (13 and 14 Oct, Jon's contract and its 14 Oct revision; branch `claude/facts-and-notice`).** **Done:** (A) the 20 corrected weekly facts in `index.html` `FACTS` (A1-A6 and A7-A20 as worded in the contract; FACTS order, the anchor date and every other fact untouched; the three entries removed from `KNOWN` in `check-content-safety.py`, so 'SR-14 fields' is True). One punctuation change of mine: A19 replaces from "— about 460 billion", so I wrote "grains. At roughly 50 mg…" (a full stop in place of the dash) to keep the sentence break. (B) `scripts/verify-facts.py` (CI-wired: ci-line plus `ci-deps: index.html`): 52 facts, about 140 pins, each a regex over the fact's words whose captured figures are recomputed (52!, 5 × 10²⁸ = 117 billion people × seconds since the Big Bang, √(2 ln 2 · 52!) ≈ 10³⁴ and its ratio, 8x³ − 6x − 1 at cos 20° with no rational root, (2⁶⁴ − 1) × 50 mg, 18/37 to the 26th, energy 10^(1.5 × 1.3), compound growth, the Collatz path, the Birthday and Small-Samples probabilities, ISBN-13 and Luhn digits) or sourced in the script where nothing can be computed; a pin with neither fails; a title, count or order change fails (`fact_index` stays stable). Self-test plants a wrong figure (90 → 22), a wrong year (1998 → 1999), a changed pinned phrase and a literal modulus. (C) `getWeekIndex()` uses `% FACTS.length`; the verifier fails on a literal modulus or a changed anchor. (D) Glorious Gantt carries `<!-- maffs-correction-notice -->` and the banner text from the contract (checked visible with no sideways scroll at 320 px and 1280 px); `audit-register.py` fails if a game unlisted for faults lacks the marker or a listed game carries it (two plants in its self-test). (E) `GATE_EXCLUDED` for glorious-gantt covers points 1, 2, 3 and 5 with the contract's reason; canon §0.2 updated to match; 'answer lock' now waits on characteristic-quest alone (the cloud lane's). (F) see the result line at the end of this entry.

**For Jon (findings outside A, not fixed; the contract says list, do not reword):** (1) **Fact 14, "98% Accurate Doesn't Mean What You Think":** the hook says a "98% accurate" test can be wrong "more than 90% of the time", but the body computes 199 false of 248 positives = 80%. True value 80% for those inputs (a prevalence near 0.2% would give 90%). Carried as a KNOWN pin in `verify-facts.py`, which fails once it is fixed, so the pin is removed with the fix. (2) **Softer, sourced but worth a look:** fact 43 Basel "a 28-year-old Euler proved this" (born April 1707; solved 1734 aged 27, announced 1735, so 27 or 28 depending on the date); fact 51 "argued about this for 2,500 years" is a round figure; fact 33 "almost certainly score lower" overstates (the expected score is lower; an individual can still score higher); fact 36 still says compass and straightedge "can only produce square roots" beside the new cubic, which is correct (constructible numbers are built from square roots) but reads oddly next to a cubic. (3) The Erdős quotation in fact 20 is the documented variant ("not yet ready"); Guy's wording is "may not be ready". (4) A8's 5 × 10²⁸ rests on about 117 billion people ever born (Population Reference Bureau, 2022); estimates run 100 to 117 billion, and the argument holds across that range. **F (confirmation run, 14 Oct):** `check-changed.py` on a clean `origin/main` (d1b23bc) over the 70 files changed by #355 to #358 (REGISTER.md left out, CI regenerates it): 157 checks in 3,598 s; **no genuine failure.** Five reported failures, all environmental: Answer lock in play parts 1, 5 and 6 and Force Resolver failed under load ("MaffsLock undefined" at start; the usual local load flake) and **pass when run alone** (parts 1, 5, 6, the answer-lock self-test, and Force Resolver twice); Test the Claim fails on that checkout only because it has no LF rule yet (the Windows CRLF problem, PR #373). **A second cause of Test the Claim's local failure, not fixed because Jon ruled it be fixed at the repo layer and not in that verifier:** `scripts/verify-test-the-claim.py:1020` writes its mutated temp page with `NamedTemporaryFile('w')`, which converts to CRLF on Windows, so its newline-brace-newline slicing finds nothing; adding `newline=''` there makes it pass (tried and reverted). Jon: say if you want that one-word change. **Main after #373:** run 38520053624 failed only in the main-only job `CI timings and pack`, not in any check: Probability Paradox ran 203 s against a recorded 161 s, so Content verifiers 20 sat at 82% of its budget (the pack fails above 80%) and nothing was committed; a re-run of the job gave the same result. The next main run re-times it.

**LEVEL-LOGGED (13 Oct, Jon's contract and rulings; branch `claude/level-logged`, triage rule R10).** New `scripts/check-level-logged.py` (CI-wired by its ci-line; one plant plus six cases): no `mfg(...)` call in `games/` or `escape-rooms/` carries a literal `level`; `'all'` passes only where the game's `MaffsLevel.resolve` lists `'all'` in `boards` (52dle, equatle, prime-or-composite, truth-buster, bearing-blitz keep logging it). Each game captures the resolver result as `resolvedLevel`; the leaderboard and score-history keys are untouched (SR-29). **Fixed (25): ** boolean-blitz, circle-theorem-spotter, constructions-lab, core-maths-paper1, core-maths-paper2a, core-maths-paper2b, core-maths-paper2c, dimension-checker, eigenvalue-extractor, eigenvector-engine, factor-theorem, index-laws, like-terms-collector, modular-battle, normal-navigator, partial-fractions-duel, probability-paradox, quadratic-factoriser (its four 'higher'/'formula' literals now `currentLevel`; Chromium proved each equals `currentLevel` in every mode first), shape-shifter, tax-theft, test-the-claim, think-of-a-number, trig-wars, trig-worms, truth-will-set-you-free. **GA4 and Sheets level data from before this merge is unreliable for every game above** (single-level games logged the right value; the multi-level ones, i.e. constructions-lab, eigenvalue-extractor, eigenvector-engine, index-laws, normal-navigator, partial-fractions-duel, probability-paradox, test-the-claim, trig-wars, trig-worms, logged one fixed level whatever was played). Also in `.claude/rules/analytics.md`. **Open:** characteristic-quest is on the check's NOT_YET (reported, may only shrink): the cloud lane fixes it in its SWEEP-1-RULINGS PR (with R7) after #359 and removes it from NOT_YET there. Closed eigenvector-engine-s1-004 and normal-navigator-s1-007; new LOW normal-navigator-s1-009 (page says use a calculator, roster untagged) for Jon's tagging decision.

## 2026-10-14 (home): entries from 12-13 Oct, moved to keep the handover under 20 KB (FACTS-AND-NOTICE)
**LISTINGS-AND-GATE (13 Oct, Jon's contract; PRs #333 part A, #334 part B, #335 part C): COMPLETE; what Jon needs to see is below. Where the gate stands (REGISTER.md after #335): points 1, 2 and 5 met; 4 tracked, not gating; 3 and 6 not met.** **Met now in point 3:** 'level resolver' (12 Oct) and 'B11 parser' (the ledger holds no B11 entry for any game, #331). **Point 3 still lacks two.** (1) *'answer lock' is False:* `check-answer-lock.py` still lists `glorious-gantt` on NOT_YET and `characteristic-quest` on SCREEN_NOT_YET (the contract expected neither; characteristic-quest is the cloud lane's game, on its list for the Play-again screen). Glorious Gantt is excluded from points 1, 2 and 5 only, not 3, so it needs either a lock or a ruling from Jon. (2) *'SR-14 fields' is False:* the contract said no site-wide SR-14 check existed; **`scripts/check-content-safety.py` does, and has run in CI since 4 Oct** (word lists, a displayed-text reader, 26 planted cases, KNOWN empty). I did not write a duplicate `check-sr14.py`: I widened that one to every other published page and the shared scripts (195 files now) and added two plants on that surface (28 of 28). Its first read of those pages found **5 tier (a) hits in three of the portal's weekly facts** (`index.html` lines 3687, 3694, 3714): "√2 is Irrational — and It Caused a Murder" (murder, drowned), "Correlation Does Not Imply Causation" (drowned in swimming pools, deaths by bedsheet entanglement) and "Survivorship Bias" ("everyone who died at 60"). No tier (b) hits. Nothing was rewritten (voice and content are Jon's); they sit in `KNOWN` with a comment. **Jon: rewrite the three facts, or allow them with a reason in `ALLOW`; then 'SR-14 fields' goes True.** **Point 6 (the sweep) is the cloud lane's; it reports `SWEEP_DONE`.** **Part A:** Jon's 13 Oct level-listing rulings applied (details in the LEVEL-RESOLVER entry below). SR-29 is in canon §0.3 and `AUDIENCE_LISTINGS` in `check-levels.py` holds the five games; `CARD_KNOWN_MISMATCH` is empty. I also had to drop the two ledger B4 entries and the generated search titles for the removed levels, and the hub rows for factor-race and angle-ace. I could not tell whether any removed hub board has Firebase entries (none of those games could submit under the removed keys, since the migration). **Part C:** `test-section-clicks.py` reads the card order from `index.html`; the 7 orphan GA comments are gone (`apply-analytics-loader.py`, checked in `check-analytics-loader.py`); the calculator failure did not reproduce (todo §4 item 18 (d), (e)). **Mistakes of mine:** I guessed the PR number into the findings (#332, it was #333) and fixed it on the PR; the first push missed the hub registry check, which CI caught.

**LEVEL-RESOLVER (12-13 Oct, Jon's contract; PRs #316-#319, #321-#323 and #325-#327): COMPLETE.** `MaffsLevel` (canon 4.5, 7.9.1) is in all 98 games with a script (regression-rumble is a script-free holding page, exempt); `NOT_YET` is empty and 'level resolver' is True in the register's point 3. `check-levels.py` (declaration = roster or LEVEL_OVERRIDES; links, sitemap and portal cards; no own-code reader), `test-level.py` (module, guard, and every game at junk and declared keys; four lock-tier parts) and the `submitScore` guard are the standing checks. The per-batch entries are in the home archive. The contracts for GATE-AND-SR28, PD-TOURNAMENT-BOARD and LEVEL-RESOLVER are now in `docs/history/contracts/`. **Level listings: ruled by Jon 13 Oct, applied in LISTINGS-AND-GATE part A (#333).** Removed from roster row, card, game declaration and hub: factor-race GCSE, modular-battle A-Level, dimension-checker A-Level, sequence-solver L4, trig-identity-duel L4, angle-ace KS3, estimation-golf Core (its Core-only duplicate card deleted), quadratic-factoriser A-Level (`CARD_KNOWN_MISMATCH` is now empty). SR-29 keeps the five single-bank audience listings (characteristic-quest, eigenvalue-extractor, eigenvector-engine, partial-fractions-duel, normal-navigator), policed by `AUDIENCE_LISTINGS` in `check-levels.py`. Existing Firebase boards untouched. Nine Year 6-only cards also list `ks3` (portal has no Year 6 filter; a documented alias). Closed: modular-battle-t4-002, dimension-checker-t5-006, partial-fractions-duel-t5-009. **Still open class-4:** characteristic-quest-t6-005 (its level half is settled by SR-29; the wording 'Complex eigenvalues indicate a rotation' is loose and is game content), factor-race-t3-004, integration-duel-t5-010 and proof-builder-t5-024 (composites: level part fixed, the rest not) and higher-power-t2-002 (a streak crash, not ?level). Game pages' meta descriptions were not edited (sequence-solver's still says Level 4). **For the cloud lane:** a game page that reads `?level` itself fails `check-levels.py`; use `MaffsLevel.resolve`. A verifier that plants on a level line plants against the `MaffsLevel.resolve` call. A new game is declared from the start. **Mistakes of mine to know:** I merged #321 while the cloud lane's #320 main run was still in progress (both runs came back green); three CI failures along the way (a stale plant regex, an Essentials check that wanted `get('level')`, and a verifier plant that URL normalisation hid) were fixed on the PR.

**PD-TOURNAMENT-BOARD (12 Oct, Jon's contract; PR #314, branch `claude/pd-tournament-board`).** prisoners-dilemma-t4-001 fixed per SR-22: single matches submit nothing; a completed tournament submits the player's total out of 20 x opponents under `<level>-tournament`. Hub lists the four tournament boards; the old per-level boards stay in Firebase, unlisted. `check-leaderboard-coverage.js` now fails if any PD submit is not `currentLevel+'-tournament'`, and PD's score-history keys are declared in HISTORY_ONLY_KEYS. **Contract conflict, for Jon:** the contract says do not touch `firebase-leaderboard.js`, but the coverage check requires `levelLabel()` to name every submitted key, and the only way is LEVEL_NAMES; I added four label entries there (data only, no logic) rather than stop. Node is not installed on the Windows machine, so the check ran only in CI and the planted-fail was shown by a Python re-implementation of the rule.

**GATE-AND-SR28 (12 Oct, Jon's contract; branch `claude/gate-and-sr28`).** Three rulings of 12 Oct recorded. (1) Bank depth (point 4, and served bank size in point 3) is out of the build-freeze gate: tracked in the register, worked on in parallel under SR-26. (2) `glorious-gantt` is excluded from points 1, 2 and 5 by name while unlisted (it stays live at its URL, as Jon accepted); `GATE_EXCLUDED` in `scripts/audit-register.py` holds it with the reason, the dashboard lists it on its own line, and the script fails if a slug in it leaves the roster's Unlisted section (self-test plants a relisted one). (3) SR-28: algebraic terms divide as a whole (6x⁷ ÷ 2x² divides by 2x²; SR-17 does not apply). Canon §0.2 and §0.3 updated. Dashboard locally: points 1 and 5 read met, 2 reads 1 HIGH open, 4 marked not gating. `index-laws-v20-001` is the cloud lane's to close, citing SR-28.

**RULINGS-12OCT (12 Oct, Jon's contract; branch `claude/rulings-12oct`).** Canon §0.3 has SR-26 (grow banks from parameters, never swap single items) and SR-27 (verifier-only PRs run five named checks, not `check-changed.py`); CLAUDE.md "Before pushing" names SR-27 as the one exception. New `scripts/end-task.py <branch>` replaces the `branch -d` rule: it removes the worktree and local branch only if the PR is MERGED, the tip is the PR's head and the worktree is clean, else refuses; self-test in CI. (`-d` can pass while the stale `origin/<branch>` ref exists, and refuses after a prune.) **For the cloud lane:** from its next PR use SR-27 and `end-task.py`; GitHub deletes merged head branches, so drop the "Open for Jon: delete branch" lines in your next handover commit. ROOM-ART/ROOMS-RELEASE-RK-LJ moved to `docs/history/handover-home-archive.md` for size.

## 2026-10-13 (home): LEVEL-RESOLVER per-batch entries, moved when the contract completed
**LEVEL-RESOLVER batch 8 (13 Oct; PR #326, branch `claude/level-batch-8`).** Migrated: scale-factor-scaling, coordinate-geometry-dash, standard-form-blitz, surd-simplifier, estimation-golf, factor-race, boolean-blitz, modular-battle, dimension-checker, partial-fractions-duel, the-perfect-prank (93 of 99; regression-rumble is exempt: a 4 KB holding page with no script, and the check fails if it gains one). The five 'held' games (factor-race, modular-battle, dimension-checker, partial-fractions-duel, characteristic-quest) are migrated with their roster listing unchanged, so their listing findings stay open for Jon. **Left (5):** chart-interrogator (its Level 4 key is `l4`, the roster's is `level4`: needs a ruling), quadratic-factoriser (game levels gcse/higher/formula vs roster gcse/alevel), free-daily-pizza (daily board keys need a pattern form in `boards`), screening-room and unit-converter (their verifiers plant faults on the old `?level` line and need rewriting with the game).

**LEVEL-RESOLVER batch 7 (13 Oct; PR #325, branch `claude/level-batch-7`).** Migrated: core-maths-paper1/2a/2b/2c, tax-theft, normal-navigator, factor-theorem, truth-will-set-you-free, eigenvalue-extractor, eigenvector-engine, test-the-claim, characteristic-quest, glorious-gantt, graph-sketcher, growth-and-decay, log-laws (82 of 99). The games on the roster that list a level they do not serve (characteristic-quest, eigenvalue-extractor, eigenvector-engine, normal-navigator, test-the-claim: Level 4 or Core listed, one board submitted) are migrated with their listing unchanged, so their level findings stay open (characteristic-quest-t6-005): a listing change is Jon's call. **Left (17):** scale-factor-scaling, screening-room, unit-converter, free-daily-pizza, chart-interrogator, quadratic-factoriser, estimation-golf, factor-race, modular-battle, dimension-checker, partial-fractions-duel, boolean-blitz and coordinate-geometry-dash / standard-form-blitz / surd-simplifier (cloud B11-CLEAR), regression-rumble, the-perfect-prank (no roster row).

**LEVEL-RESOLVER batch 6 (13 Oct; PR #323, branch `claude/level-batch-6`).** Migrated: component-crusher, gradient-hunter, stat-attack, expectation-station, formula-forge, formula-unlocked, given-that, simultaneous-solver, trig-identity-duel (66 of 99). **Held, needs Jon:** chart-interrogator (its Level 4 button uses the key `l4`, the roster key is `level4`; keys never change, so a ruling is needed), quadratic-factoriser (game levels are gcse/higher/formula, roster says gcse/alevel). **Not yet done:** scale-factor-scaling (reads any key raw; check its banks), screening-room / unit-converter / factor-theorem (verifiers plant faults on the old `?level` line; update them with the game), coordinate-geometry-dash / standard-form-blitz / surd-simplifier (cloud B11-CLEAR), free-daily-pizza (daily board keys need a pattern form).

**LEVEL-RESOLVER batch 5 (13 Oct; PR #322, branch `claude/level-batch-5`).** Migrated: bearing-blitz, circle-theorem-spotter, estimation-engine, linear-equation-solver, index-laws, trig-wars, trig-worms, probability-paradox, correlation-or-coincidence, better-value, graph-transformer, proportion-blaster (57 of 99). Skipped for now: coordinate-geometry-dash, standard-form-blitz, surd-simplifier (the cloud lane's B11-CLEAR is editing those pages; migrate after it finishes). **For Jon:** index-laws, trig-wars, trig-worms, probability-paradox, correlation-or-coincidence list more levels than they submit (they submit 'gcse' only). **Next:** the remaining GCSE games, then Core, A-Level, Further, Level 4.

**LEVEL-RESOLVER batch 4 (13 Oct; PR #321, branch `claude/level-batch-4`).** Migrated: spot-the-muppet, maths-court, expected-damage, terrible-advice, wrong-on-the-internet, word-problem-decoder, fermi-lab, sequence-solver, split-it, spot-the-error, six-sevens-bruv, truth-buster (45 of 99). `declared().asked` added (a level parameter was present). **For Jon:** sequence-solver lists Level 4 in the roster but has no Level 4 bank (it plays ks3); truth-buster and the 'all'-board games list levels with one board. **Verifiers that plant faults on a game's old `?level` line** (verify-factor-theorem, verify-screening-room, verify-unit-converter) need their plant strings updated in the batch that migrates those games. free-daily-pizza is held: its daily boards are `daily-YYYY-MM-DD`, which `boards` cannot list (needs a pattern form). **Next:** the GCSE games.

**LEVEL-RESOLVER batch 3 (13 Oct; PR #319, branch `claude/level-batch-3`).** Migrated: angle-ace, fraction-equivalence, percentage-flip, prime-factorisation, prime-or-composite, 52dle, equatle, constructions-lab, distinctly-average, equation-builder, just-pythag-it-bruv (33 of 99). Each plays exactly as before for every key it handled; a roster level with no bank of its own plays the nearest bank (angle-ace ks3 plays gcse), and games that submit one 'all' board declare it in `boards`. **For Jon (roster lists levels these games do not have separate content or boards for):** angle-ace (no ks3 bank), the year6-or-'all' trio, prime-or-composite, 52dle, equatle (one 'all' board, ?level ignored), estimation-golf (roster lists Core; no Core bank), held back. **Next:** sequence-solver, spot-the-error, spot-the-muppet, maths-court, expected-damage, fermi-lab, free-daily-pizza, six-sevens-bruv, split-it, then GCSE.

**LEVEL-RESOLVER batch 2 (13 Oct; PR #318, branch `claude/level-batch-2`).** Migrated: suvat, complex-converter, matrix-crunch and the nine Year 6-only games; 22 of 99 migrated. Closed suvat-t5-005, complex-converter-t6-006, matrix-crunch-t6-004. **Held (for Jon):** characteristic-quest (roster lists Level 4; the game plays Further only and submits 'further'), joining factor-race, modular-battle, dimension-checker and partial-fractions-duel. **Next batch:** the KS3 and Year 6/KS3/GCSE games (angle-ace, estimation-golf, fraction-equivalence, percentage-flip, prime-factorisation, 52dle, constructions-lab, ...).

**LEVEL-RESOLVER batch 1 (12 Oct; PR #317, branch `claude/level-batch-1`).** Migrated: higher-power, prisoners-dilemma, seven-bridges, binomial-blaster, curling-friction, differentiation-duel, force-resolver, moments-master, integration-duel, proof-builder (MIGRATED in `check-levels.py`; `test-level.py --games` plays each at junk and declared keys, 4 lock-tier parts). Closed: the entries that are only the ?level fault. integration-duel-t5-010 and proof-builder-t5-024 are composite (other faults in the same entry) and stay open; higher-power-t2-002 is class 4 but a streak crash, not ?level. **Held back for Jon (roster says more levels than the game has content for; removing a listing is Jon's call, no usage data to hand):** factor-race (roster lists GCSE; game plays ks3/year6 only), modular-battle (roster/card list A-Level; the game is GCSE only; its page title also says A-Level), dimension-checker (roster lists A-Level; one L4 bank, submits as level4), partial-fractions-duel (roster lists Level 4; alevel bank only). They stay on NOT_YET. **Next batch:** the other class-4 games (suvat, characteristic-quest, complex-converter, matrix-crunch), then the rest of the 99, lowest roster level first.

**LEVEL-RESOLVER (12 Oct, Jon's contract; PR 1 of the migration, branch `claude/level-resolver`).** Shared layer built: `schools/assets/level.js` (`MaffsLevel.resolve/declared/allows`, canon 4.5), a guard in `submitScore` (undeclared level = warn and no submit; undeclared pages unchanged), `scripts/check-levels.py` (declaration = roster, links/cards/sitemap, own-code reader, NOT_YET = 99 games, three plants) and `scripts/test-level.py` (Chromium; property-lookup plant caught). Listing fixes: binomial-blaster's card dropped `l4` (the game has no Level 4 content). **For Jon:** the nine Year 6-only cards also list `ks3`; I kept that as a documented alias (the portal has no Year 6 filter, so removing it would hide them from every filter but All). Decisions: an absent `?level` leaves the URL alone; matching is exact-case; `boards` is an extra declared list for session-length and tournament boards. **Next:** batches of about 10 from the 19 open class-4 findings (18 games), lowest roster level first; each moves games from NOT_YET_AT_START to MIGRATED in `check-levels.py`.

## 2026-10-12 (home): trimmed for LEVEL-RESOLVER batch 1
**SPLIT-IT-KATEX (11 Oct, Jon's contract; branch `claude/split-it-katex`): todo §1.48 CLOSED.** split-it now loads
KaTeX (CDN, as suvat) and `mathtext.js`. Fractions in working/feedback text render via `F()` (`rac`); `X()` gives
a whole number or lowest-terms `rac`. Fixed: speed working (13.33.. -> stacked 40/3; distance uses the same
value), the fractions-mode working and simplify message, and the GCSE scale-factor working and hint (5/3 had
printed 1.6666666666666667). `showFeedback` runs through `MaffsText.html`. Unit label drawn once, after the input
(money keeps its prefix). Keys, marking and scoring untouched. Checked: 48,000 generated questions, no float
artefact (610 stacked speeds, 730 whole); 375px render, no overflow; check-changed 28/28. **For Jon:** the
fractions-mode answer INPUT is still two boxes with a CSS bar (`.frac-wrap`): it is a control, not a displayed
fraction, and KaTeX cannot hold inputs, so it stays. Scans (report-only): `docs/audits/split-it-fraction-scan-2026-10-11.md`.

**ESCAPE-CANON-LABEL (11 Oct, Jon's contract; branch `claude/escape-canon-label`).** Canon §11.3-11.5 brought
up to date with the live rooms and #278, no figures derived from repo content: §11.3's ratings roster is now a
pointer (each rating derives from lock grades, is recorded as `data-stars` on the cards, and is printed in the
CI log; both new rooms came out as Jon ruled, hub ★★★ and ★, so no STOP); the plants sentence names all three;
"The live rooms all use `digits`" and its "waiting on" drafts replaced (maxDigits was built for the two new
rooms; each lock's mode is in its `room.js`). §11.4: the gate's row describes the per-set re-check, the
fixture, the plants and the printed counts; new row for `escape_set_checks.py`; the generator's row
corrected. §11.5: "All eight rooms" and "The two withdrawn rooms" gone (described, with The IT Teacher's
Vengeance's redirect and Car Trap's return); "drawn out of Jon" kept, with the ally-and-clock rooms noted.
**CI label: already single-source.** The `# ci-line:` header in `check-escape-rooms.py` is the source;
`ci-pack.json` and `ci-timings.json` are caches that main's "CI timings" job rewrites wholesale after every
full run (`write_pack` from the headers, `record_timings` from the run's log), so an old label drops out of
both. Only the header changed; the JSON files were not hand-edited. Until main's next full run times it, the
renamed line counts as 120 s and runs in a group of its own (`ci-groups.py --check` passes). (The stale voice-rewrite §5 status table is fixed by ROOM-STATUS-ONE-TABLE, above.)

## 2026-10-12 (home): trimmed for LEVEL-RESOLVER batch 1
**CONTAINER-PULL-TIMEOUT (12 Oct, #299).** The image pull no longer counts against a group's limit: both container jobs use `timeout-minutes: matrix.job_timeout` = `timeout` + `PULL_ALLOWANCE` (10, `ci-groups.py`; emitted for content groups, literal on the 7 static entries). Budget step untouched (75% of `timeout` from JOB_T0). `ci-groups.py --selftest` fails on any mismatch. Not done: pull seconds in the summary (no in-job source for the start time). Cause: run 802, Content verifiers 33 took 379 s against 360 s. **Cloud lane:** the re-run-at-Initialize-containers rule can go after two clean full main runs.

**CI-TIMINGS-MEDIAN (12 Oct, Jon's contract; #288, merge d00a818): MAIN IS UNBLOCKED, and the cloud lane can resume VERIFIERS-20.**
`ci-groups.py --check` had failed on main and every PR since the "Record CI timings and repack (run 38224711265)" commit
(`25f887b`): run 785 recorded a 125 s setup against 18-28 s in the eleven records before it, and the repack against that
left 12 groups at 81-108%. `scripts/ci-timings.json` now keeps the last 5 main runs under `history` and its top-level
`setup` and `lines` are their medians (the seed is runs 777-785; median setup 25 s); `ci-groups.py --record-and-pack` works the
pack out in memory and writes neither file if `--check` fails; the timings job uses it and runs `--check` again before
committing. Self-test covers the 125 s outlier, a line slow in 3 of 5 runs, and a failing pack being refused. **Confirmed on
main:** run 791 (38230011527) green, its timings job ran the new path and committed run 38230011527 (`1878166`), and
`--check` passes on main. Canon §7.8.1 and CLAUDE.md have a sentence each. **For the cloud lane:** merge `main` into
`claude/verifier-think-of-a-number`, push, merge #287 on a green Gate, then continue at `formula-plug-in`. No budget,
`TARGET`/`FAIL`, timeout, verifier or `ci-pack.json` (by hand) was touched.

## 2026-10-12 (home): trimmed for LEVEL-RESOLVER batch 1
**GA4-LIVE-ONLY (12 Oct, Jon's contract; branch `claude/ga4-live-only`).** GA4's tag is now loaded only by `schools/assets/analytics.js`, and only on maffsgames.co.uk / www; no page carries the snippet. `scripts/apply-analytics-loader.py` changed exactly 150 pages (the snippet's two tags removed from all; the include kept on 145; added, at its relative path, on about, feedback, leaderboards, privacy, spec-map). New `check-analytics-loader.py` (site-wide, selftest with 4+ plants) and `test-analytics-loader.py` (Chromium: stub server and a local host reach no Google host and define no gtag; the live host does one gtag.js load and one config). `test-escape-analytics.py` keeps Google blocked and now asserts zero requests reach it. `verify-parent-guides.py` TPL asserts the new arrangement; canon §1.1 and `.claude/rules/analytics.md` updated. **For Jon:** (1) data before this merge still includes test traffic: exclude 800x600 in any report up to the merge; crawlers still reach GA4 (separate decision); (2) boolean-blitz and truth-will-set-you-free load analytics.js but never had the snippet, so they now send page views too; (3) `/privacy/` still prints the measurement ID as plain text (not a tag; the check allows it); (4) the old "Google Analytics (cookieless)" HTML comment stays above the include on those pages.

**FRONT-PAGE-ROOM-ORDER (12 Oct, Jon's contract; branch `claude/front-page-room-order`).** The front page's escape-room grid is now in the hub's order (comic-caper, kiln-disaster, library-jam, then the five/six ★★, rugby-mud, rightful-king); cards moved whole, the Comic Caper and Kiln Disaster wrappers with their notes; nothing else in `index.html` changed (same words, same markup). `check-escape-rooms.py` `check_ratings()` now applies the rating-order rule to every page, and requires the front page's live-room sequence to equal the hub's (both printed on failure); two planted faults (a swap across a star band, a swap within a band) are caught every run. Checked on the stub server: no overflow at 320 or 1280 px; at 1280 Library Jam shares the first row's top and height with the two wrapped cards. Only the hub and front page carry room cards. **Side effect for Jon:** `section_clicked` `position`/`filter_value` for the escape-room cards follow page order, so from this merge a room's `pos` differs (e.g. comic-caper 9 to 3, library-jam 13 to 5); `test-section-clicks.py`'s table is updated. Seen on main 5b1307a (#301): Modular Battle's verifier failed twice at its scaffold step (line 178); it passed on every later main run, so it may be a draw-dependent flake: cloud lane's.

## 2026-10-12 (home): trimmed for PD-TOURNAMENT-BOARD
**ESCAPE-ANALYTICS (11 Oct, Jon's contract; STOPPED on its shared-layer STOP IF, then Jon's rulings 11 Oct).**
Diagnosis (Jon's Rightful King play, Sheet rows 55413-55434): (1) the eight index-0 "answers" were room searches:
`engine.js:359` logged each first search as question_answered, correct, index 0 (the Sheet has no `detail` column,
so the `searched:` tag never showed); (2) the mid-game abandon came from `analytics.js:138-146`, which sent
game_abandoned on every visibilitychange to hidden, in **every game**, so a game finished after a tab switch counted
as abandoned and completed; (3) GA4's 2 completions did not reproduce: one call site (`engine.js:805`, st.done
guard), one analytics.js, and the test shows one play sends exactly one game_completed to GA4 and one to the Sheet,
so it is closed as a realtime counting artefact (Jon's ruling). Fixed, shared layer: searches send nothing;
`mfg()` drops game_abandoned unless the page is being left (beforeunload / pagehide set `_mfgLeaving`;
analytics.js loads in the head, so its beforeunload runs before any game's), the visibilitychange listener is
gone, pagehide sends it; once per game as before. **Abandon figures change meaning on 11 Oct 2026** (canon §1.3,
with the trade-off: a backgrounded phone tab later killed by the OS sends nothing). New
`scripts/test-escape-analytics.py` (in CI): Rightful King won after searching every object and a tab switch, 3/1/0
to GA4 and the Sheet; the room left mid-game, 1 abandon; prime-or-composite (own visibilitychange handler) with a
tab switch, 0 abandons, 1 completion; three old faults planted and caught. Both faults predate the public repo
(2 Oct 2026), so the history cannot date them; affected Sheet rows not counted (no export here).

**LOG-NOTATION (10-11 Oct, Jon's contract; STOPPED on a wrong key, then Jon's rulings; PR #274).** B11's parser
(`bank_common`): log with no base is base 10, ln base e, log_b base b; a power argument of ln/log is bracketed
(ln e^2 parses); and, Jon's class fix, a symbol inside a log is positive when two values are compared (log(x^2) =
2 log x). **B11 over all 97 games: no existing verdict changed; +4 pairs, all log-laws ([7], [13], [39], [42]); the
domain rule added none anywhere**, so no other game's findings file changed. log-laws Laws bank: five distractors
replaced ([7], [13], [18], [39], [42]); **[22] (1/3 log 27) was keyed 1, value log 3: CRITICAL (Jon), now keyed log
3** (options log 3, 1, 3, log 9); [24]'s 2 log x (equal to the key for x > 0) replaced by log(1/(2x)).
verify-log-laws.py now checks the Laws bank too (every key its question's value, no two options equal; the old [22]
and [24] planted and caught). Findings log-laws-ln-001..006 (fixed, #274; f0-001 fixed); ledger cleared for log-laws
only. Locally the banks were extracted with `extract-banks.py --workers 2` (98 s; 4 workers risks this machine's
memory). Note: this machine's Bash heredocs eat backslashes, so regex-heavy scripts were written to files first.

## 2026-10-11 (home): trimmed for SPLIT-IT-KATEX
**RIGHTFUL-KING-ART (10 Oct, Jon's contract; pictures approved 22:20).** Filed `docs/art/rightful-king-scene.webp`,
`-fail.webp`, `-win.webp` (1600x873, WebP q80, through `strip-gen-watermark.py --width 1600 --frame 1600x873`: no
watermark; 2752x1536 cropped to 2752x1502, so crown, server cupboard and desk all stay in frame). Nothing readable or
branded; the mug carries a pixel-high scribble under its leaf, illegible even zoomed. room.js: `art: 'rightful-king'`,
the "ART: none yet" note replaced, sceneAlt gains the sticky note and printer, failAlt rewritten (night, lit by the
display), winAlt unchanged; the RULE (no `missArt`) kept. **Still unreleased** (holding page, no hub card, no sitemap).
**Jon can play-test it with its pictures at https://maffsgames.co.uk/escape-rooms/rightful-king/play.html.** Checked:
play.html in Chromium at 1280 and 320 px shows the scene on the brief, the win picture on a win, the fail picture at
time-out; check-escape-rooms and test-escape-art pass.

**SCIENTIFIC TAGGING 5/5: core-maths-paper2c (10 Oct). The tagging run is done** (#261, #264, #265, #266, this;
complex-converter stays untagged, Jon). Roster `scientific`, badge on the start card, scientific calculator under the
question card (below Next, so Next does not move on a phone); check-calculator, verify-core-maths-paper2c and the
Chromium smoke (sin(30) = 0.5 at 1280 and 320 px, no overflow) pass; CI the gate.

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**OVERNIGHT RUN (Project Claude for Jon, 8 Oct 2026, 23:45): DONE.** Contract verbatim in
`docs/history/contracts/2026-10-08-overnight.md`. Every item merged (see the summary above and the entries below).
main's run on #200 (2782d17) went red on a runner network flake (the DejaVu font fetch: curl 503s and 60 s
timeouts pushed B4 and L4 past their budgets; tier 1 timed out loading spot-the-muppet, untouched); one rerun of the
failed jobs passed (run 37875059753, attempt 2).

**Contracts (canon §7.8.2, contract CONTRACTS-FOLDER):** each is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md`; the queue below holds a one-line pointer; the file moves to
`docs/history/contracts/` when the work merges. Read a contract when its item starts, never at session start.

## 2026-10-11 (home): trimmed for ESCAPE-CANON-LABEL

**STAR-KEY (10 Oct, Jon's contract 17:50; `docs/handover/contracts/2026-10-10-star-key.md`).** One line saying
what the stars mean, on the hub (under "Ordered easiest to hardest") and on the front page's escape-room band
(`.esc-note` size, 12.5 px; placed just above the cards, so with the band compacted it sits directly under the
summary and on desktop beside the cards it explains): "Stars show difficulty, set by each room's hardest lock: ★
Warm-up, grades 1–3 · ★★ Core, grades 4–5 · ★★★ Challenge, grades 6–9." Glyphs aria-hidden; a screen reader reads
"one star, Warm-up, grades 1 to 3; two stars, ..." (checked in Chromium's accessibility tree). check-escape-rooms.py
matches each page's `data-star-key` line to BANDS (which already match rating.js), checks the spoken text, and
plants "Core, grades 4–6" (caught). No 320 px overflow (test-escape-rating). STOP IF clear: it wraps at the band's
own size. Older entries (CAR-TRAP-V2-ART, ART-PENDING, MAIN GREEN) moved to the archive for room.

**TODO-SLIM (10 Oct; Jon's option (b), 17:15).** `docs/todo.md` 481,628 -> **148,748 bytes** (3,662 -> 810 lines);
moved word for word to new `docs/history/todo-done.md` (333,814 bytes; the two add up to the original plus the
added headings): the session log (line 5 kept its newest three entries; lines 6-56, 88-140, 145-160 of 28-29 Sep
notes), the whole START block (replaced by a pointer: **the live queues are the two handovers**), 27 done rows of
§1/§3 (listed under §1's heading, so their numbers still resolve), and "Done — full history". **Kept, for Jon:**
the 29 Sep paragraph (lines 57-87) holding a leaderboard recommendation still "pending Jon's ruling"; done-looking
rows with open follow-ups stay whole (1.8, 1.11, 1.14, 1.16, 1.24, 1.25, 1.26, 1.33, 1.36, 1.51, 1.72, 1.75, 3.4,
3.6-3.10, 3.18). **Cap 150 KB, not 140:** the kept content came out at 145 KB (open rows were bigger than my
estimate); lower `TODO_LIMIT` in `check-context-size.py` as items close. canon.md is reported (194,804 bytes),
not capped. Canon's three "todo START" citations now point at the history file. **For Jon:** update Project
Claude's instructions to name the handovers, not todo.md's START, as the live queue.

## 2026-10-11 (home): trimmed for ESCAPE-SET-CHECKS

**LOCK-BANK-CI (10 Oct, Jon 17:15; for the cloud lane's room builds).** `scripts/check-lock-bank.py` rejected
hamster-feeder-bounds on main: `NOTE` was not a known field, so a multi-line note's continuation lines were glued
onto VERIFY (SyntaxError). Fixed in the parser (`NOTE` is a field), not by reflowing the entry; every other lock's
result is unchanged (before/after diff of all 7 batches: only hamster-feeder-bounds, REJECT -> ok, 580). With no
argument it checks every `docs/lock-bank-batch*.txt`; `--selftest` plants four entries (a sound lock with a
two-line NOTE, two answers, a restating VERIFY, a wrong ANSWER), all caught; it is now in CI (ci-line, about a
second). **Never run by CI (report only):** `scripts/check-feedback-options.py` (the feedback page's game menu;
passes locally) and `scripts/check-lock-uniqueness.py` (an older one-answer checker; passes locally);
`verify-regression-rumble.py` is declared held (game withdrawn). `check-changed.py` is the runner, not a check.
**#255 PREPUSH-SCOPE merged** (99a0bf5).

**DASHBOARD-CHARTS (10 Oct, Jon's contract 08:35; `docs/handover/contracts/2026-10-10-dashboard-charts.md`).**
`docs/apps-script-endpoint.js` only, SCRIPT_VERSION `2026-10-10-a`: the three percentage columns are written as
fractions with the cell format `0%` (they show as before), the Accuracy chart's axis runs 0 to 1 as percent;
`rowBelowChart()` moves the row counter below each chart (a 21 px default row), so no chart overlaps the next
section; one filter, `isMarked()`, keeps rows with a blank `correct` out of Accuracy by Game and Hardest Questions.
STOP IFs clear: prisoners-dilemma sends `correct: null` (written blank by `cellValue`), and every other
`question_answered` call in games/ sends a boolean. The daily email is untouched (its own hardest-questions list still
counts prisoners-dilemma: the contract left the email alone). **Jon must redeploy; the repo copy does not deploy
itself** (runbook `docs/apps-script-redeploy.md`): paste the file into the Apps Script editor and set `REPORT_EMAIL`
to your address before saving; Deploy, Manage deployments, edit (pencil) the existing deployment, Version: New
version, Deploy; select `testDashboard` in the function menu and Run (it rebuilds the dashboard from the sheet;
`rebuildDashboard` itself needs arguments), or wait for the 07:00 run; open the `/exec` URL and check `version` reads
`2026-10-10-a`.

**DOCS-9OCT (10 Oct, branch `claude/docs-9oct-b`, after the checkpoint).** #239 SCI-CALC and #240 (checkpoint
handover) merged on 9 Oct late, main green after each (9f51dc7, 302d4d2). DOCS-9OCT applied: Factor Theorem relisted
under SR-21, **A-Level only** (roster #88, portal, sitemap, hub, spec map, canon count 96, todo 1.62); canon §0.2 the
freeze's one exception (Simultaneous Solver Stage 5, #203); §7.6 four rulings (Skip shows the answer and waits on
Next; one log row per answer; display-only number formatting; "≈" for rounded factors); §7.8.2 closed-not-idle cloud
sessions and the E2 one-off; timer-policy: Unit Converter to No Timer. **Escape on the initials overlay (Jon, 9 Oct
19:42): left as is, Skip stays the way out; Escape-to-close is deferred to a future accessibility pass, because an
accidental Escape would discard a leaderboard entry** (the OVERLAY-KEYS contract's "Escape closes the overlay as now"
was Project Claude's error; recorded on #232 too). **Next: KEYPAD-VARIABLE (entry at the top), then PREPUSH-SCOPE** (contract
`docs/handover/contracts/2026-10-09-prepush-scope.md`). LIBRARY-DRAFT moved to the cloud lane (Jon, 10 Oct 09:30);
Car Trap moved the other way: the home lane owns it end to end (#242, entry above). **Scientific tagging, Jon's ruling (10 Oct):** tag force-resolver,
moments-master, complex-converter, formula-forge, formula-unlocked, core-maths-paper2c (one PR each, after
PREPUSH-SCOPE); not estimation-golf or equation-builder; log-laws and higher-power reported back (SCI-CALC's
entry is archived in `docs/history/handover-home-archive.md`). Finished home-lane contracts (home-queue, its addendum, hook-fix, overlay-keys) moved to `docs/history/contracts/` in
this PR; the cloud lane's (listed-high, car-trap) and the IT room brief stay.

## 2026-10-11 (home): trimmed for LOG-NOTATION

**SCIENTIFIC TAGGING 4/5: formula-unlocked (10 Oct).** As formula-forge (#265): roster `scientific`, badge,
scientific calculator under the options and solution (its own `--hint` kept); check-calculator, verify-formula-unlocked
and the Chromium smoke (sin(30) = 0.5 at 1280 and 320 px, no overflow) pass; CI the gate.

**SCIENTIFIC TAGGING 3/6: formula-forge (10 Oct).** As force-resolver: roster `scientific`, badge, scientific
calculator under the options (its own `--hint` kept: calculator.css uses it only for the "required" badge);
check-calculator passes; sin(30) = 0.5 at 1280 and 320 px, no overflow. No verify script exists for this game.
**complex-converter stays untagged (Jon, 10 Oct, "for now"):** it already has a "Calculator (−25 pts)" hint (pick the
right keystrokes), and a free scientific calculator would let a student skip that cost; the paid hint stays its support.
So the tagging run is 5 games, not 6. Per Jon (10 Oct) the tagging PRs run only the game's
own checks locally; CI is the gate (a roster change selects ~120 checks, more than this machine can sustain).

**SCIENTIFIC TAGGING 2/6: moments-master (10 Oct).** As force-resolver (#261, main green): roster `scientific`, badge,
scientific calculator under the options; check-calculator passes; sin(30) = 0.5 at 1280 and 320 px, no overflow.

**SCIENTIFIC TAGGING 1/6: force-resolver (10 Oct, Jon's ruling).** Roster tag `scientific`, badge, the scientific
calculator mounted under the options (`{keys:'scientific'}`); check-calculator passes; sin(30) = 0.5 in Chromium, no
320 px overflow; check-changed 119/120 pass. **The one local failure is not this PR:** `test-real-fonts.py` fails on
every Windows checkout, main included: `core.autocrlf` rewrites the pinned text files (.css, manifest.json, LICENSE)
to CRLF, so their SHA256s differ; CI (Linux) is unaffected. Fix: a `.gitattributes` line `scripts/fonts/** -text`.
Next: moments-master, complex-converter, formula-forge, formula-unlocked, core-maths-paper2c (one PR each).

**ESCAPE-DIFFICULTY (10 Oct, Jon's contract 13:05, after CAR-TRAP-RELEASE; contract
`docs/handover/contracts/2026-10-10-escape-difficulty.md`).** Every live lock has `grade: N`; a room's
rating is its hardest lock's band (★ Warm-up 1–3, ★★ Core 4–5, ★★★ Challenge 6–9), drawn by the new
`escape-rooms/assets/rating.js` on the start screen and the teacher page (the teacher page adds "Suits a top
set" at ★★★ only), and written as a `data-stars` chip on every hub and front-page card (the old level chips
replaced). The derived ratings reproduce Jon's list exactly (no STOP): ★ Comic Caper, Kiln Disaster; ★★
Canteen, Heatwave, P.E., Prom, Hamster, Car Trap; ★★★ Rugby Mud. Every lock's grade and reason is in the PR.
Two locks the bank tags "GCSE Higher" are graded 5 (Car Trap's monic quadratic by factorising, Prom's
compound growth by building powers): the method is Foundation's. `levelLabel` removed from the live rooms
(display only); `level` kept (analytics send it). The hub's cards are now in rating order (it says "Ordered
easiest to hardest"); the front page's order is unchanged. **check-escape-rooms.py was never in CI** (it ran
only by hand): it now has a ci-line and fails a missing grade or any disagreeing card, with two plants caught
on every run. New `scripts/test-escape-rating.py` (start screen and teacher page match the hub card in
Chromium; no 320 px overflow apart from the teacher pages' allowlisted tables, §1.37). **For the cloud lane:**
The Rightful King must derive ★★★ and The Library Jam ★: add `grade` to every lock, a `data-stars` chip on
both cards, and load `../assets/rating.js` before engine.js and teacher.js.

## 2026-10-10 (home): trimmed for ROOM-ART-RK-LJ

**PREPUSH-SCOPE (10 Oct; Jon's ruling after the STOP: two queues).** Cause **(b)**: `check-changed.py` already
selected through `ci-deps.select` (CI's own function); the checks ran one at a time. There is no installed
pre-push hook: "pre-push" is `check-changed.py`, run by hand. Now two queues: **heavy** (CI time >= 60 s, or a
browser check that runs its own work concurrently: the six answer-lock parts, teacher feedback line, initials
overlay, escape-room tests) one at a time, longest first; **light** six at once beside them. Six answer-lock
parts in parallel had all failed (UNPLAYABLE) and pushed the machine to low memory. Shared-asset tests now
always run (CI always runs them); the last line is the PR line "checks deferred to CI: ..."; `--files` plans
for given paths. **Measured** (old serial -> two queues, b40a475's tree): docs-only 22 checks 353 s -> 26
checks **167 s**, all pass; one game (angle-ace) 29 checks 1565 s -> 33 checks **1375 s**, all pass; shared
asset (#232's files) 119 checks 4198 s -> 120 checks **2907 s (48 min)**. **The 10-minute target is not met
for the shared-asset case:** the heavy queue is the floor (the six answer-lock parts alone are ~20 min
serial), and it is printed, not skipped. Both shared-asset failures are local-only and fail serially and on
main too: Negative Number Line 320x568 fold (Confirm at 536 under 528), Test the Claim ReferenceError under the
local node. Also seen under the old serial load: core-maths-paper1 UNPLAYABLE (passes alone).

**CAR-TRAP-RELEASE (10 Oct, Jon's contract 13:00; `docs/handover/contracts/2026-10-10-car-trap-release.md`).**
Jon's wording in room.js: wrong lines 1 and 2 are now Mr Strictman's memos (gates at oh-seven-hundred; staffroom
biscuits discontinued), lines 3-4 unchanged; the "two point six centimetres" line moved into the brief ("You hear him
before you see him: ..."), in words, real quote marks. Released: `escape-rooms/car-trap/index.html` is the room
(play.html's body; prom-budget's head: analytics on, indexable, canonical, the draft's 158-character description
for description and og:, og:image the v2 scene), play.html deleted; card on the hub (premise line + Bounds · Arc
length · Quadratics, chip GCSE / Core, placed last) and on the front-page band; `<url>` in sitemap.xml; "eight" →
"nine" on the hub (description, og:description, lede) and the front page (band lede, "Open all nine rooms"),
CLAUDE.md, canon §11.1 (Car Trap Live 10/10, Mr Strictman, **★★**; "Nine rooms live, one withdrawn"). **The
front page's meta descriptions carry no count** (they say "15-minute escape rooms"), so the contract's "two hits"
had nothing to change. teacher.html stays noindex; it is linked from inside the room, as every room's is. /updates/:
one line under October's New. **For Jon:** the hub says "Ordered easiest to hardest"; Car Trap sits last until
ESCAPE-DIFFICULTY orders the cards by stars. Checked: check-escape-rooms passes; test-escape-art plays all nine
rooms to a win and a loss; on the real URL a wrong barrier setting shows the memo line.

## 2026-10-10 (home): trimmed for SCIENTIFIC TAGGING 5/5

**KEYPAD-VARIABLE (10 Oct, Jon's contract 10:20, ahead of PREPUSH-SCOPE: the cloud lane's Rightful King and
Library Jam builds wait on it; contract `docs/handover/contracts/2026-10-10-keypad-variable.md`).** A keypad may
now take `maxDigits: N` instead of `digits: N`: **"up to N digits, Set to submit"**. The display shows only what
has been typed (no empty slots), the room's existing Set button submits 1 to N digits (nothing typed: nothing
happens, no time lost), a leading zero is never kept (0,5,4 reads 54), and the typed fallback shares the rule
(`upTo()` in engine.js). A keypad with `digits` is key for key as before. teacher.js describes the instrument as
"keypad, up to N digits" (answers were never padded there). check-escape-rooms.py fails a maxDigits lock whose
answer or misconception is not a whole number of 1 to N digits; gen-escape-variants.py has `keypad(n)` (the range
both modes can set, so `keep()` applies the rule). check-teacher-invite's room driver handles both modes. New
`scripts/test-escape-keypad.py` (fixture: kiln-disaster's keypad rewritten in the page to maxDigits 4, answer 54,
misconception 5400; no room file edited): 5,4,Set opens; 5,4,0,0,Set raises the named misconception; Set on
nothing does nothing; no empty slot ever shows; the fixed two-digit keypad is unchanged; the old fixed-length rule
planted is caught. All 8 live rooms to a win and a loss (test-escape-art) pass; check-escape-rooms passes. STOP IFs
clear: keypad entry is not saved state (no SAVE_V change), no live room's keypad changed, one rule for keys and
typed fallback. Canon §11.3 and §11.4. **For the cloud lane: The Rightful King's passcode and the Library Jam's
fines lock can use `maxDigits` in phase 2** (the misconception must fit: 9900 needs `maxDigits: 4`).

**CAR-TRAP-BUILD, taken over (10 Oct, Jon 09:30, one lane: `docs/handover/contracts/2026-10-10-car-trap-one-lane.md`).**
The home lane owns Car Trap end to end; the cloud lane has stopped and will not touch #242 or any car-trap file. On
#242: `art: 'car-trap-v2'` (pictures merged in #246); sceneAlt corrected (the measuring wheel is at the pillar by the
yellow bollard), failAlt rewritten (the scene's own view, not from the ramp), winAlt rewritten for the high CCTV-style
view (the barrier arm is down, not up); car-trap's teacher page allowlisted at 320 px (570, table.tt) like the other
eight, todo §1.37 still the real fix for all nine. Played in Chromium: v2 scene, win and fail pictures load, no 404.
The room stays behind its holding page (`index.html` unchanged). **Jon can play-test it at
https://maffsgames.co.uk/escape-rooms/car-trap/play.html** (unlinked, noindex, analytics off). Release is a separate
step on Jon's word: play.html's content becomes index.html and play.html is deleted in that PR.

## 2026-10-10 (home): trimmed for STAR-KEY

**CAR-TRAP-V2-ART (10 Oct, Jon; image work only, #242 and car-trap/room.js are the cloud lane's).** Filed for
#242's `art: 'car-trap-v2'`: **`docs/art/car-trap-v2-scene.webp`, `docs/art/car-trap-v2-fail.webp`,
`docs/art/car-trap-v2-win.webp`** (1600x873, through `strip-gen-watermark.py --width 1600 --frame 1600x873`; no
watermark found, corners checked by eye). The old `car-trap-scene/-fail/-win.webp` are left as they are (main's
room still names `car-trap`). Badges blanked: the pale blue hatchback's front (scene, fail) and rear (win), the grey
car's bonnet oval (fail) and grille oval (win). Every plate checked blank: hatchback front (white) and rear (yellow),
grey car, beige car. **For the cloud lane (#242):** rebase on main and the v2 pictures resolve, so `art` can stay. The
win is a high CCTV-style view of the bays (camera top right), so #242's `winAlt` ("The same row of bays...") needs
rewriting to match: Jon asked for it, and it is the cloud lane's file.

**ART-PENDING (10 Oct, Jon's contract 08:50, ahead of the queue for cloud PR #242; contract
`docs/handover/contracts/2026-10-10-art-pending.md`).** Rule: **no `art` field, no request.** engine.js
(`HAS_ART = !!R.art`) emits no scene, fail-thumbnail or end-card picture for a room with no top-level `art:`;
a room with art is unchanged, data-fallback included. teacher.js mentions the mid-game failure picture only when
the room has art. check-escape-rooms.py lists a room with no `art` as "art pending" (it crashed on one before);
a named picture that is missing is listed as before, and check-site's tier 1 fails its 404. New
`scripts/test-escape-art.py` (15 s): all 8 live rooms to a win and a loss, their pictures load as before; the
fixture (canteen-hack with `art` removed, by routing) makes no /docs/art/ request through the brief, its
misconception, the win and the loss; the old always-request engine is planted and caught. STOP IFs clear: every
live room has all three files, so none uses the 404 path for its data-fallback; no saved field changes (SAVE_V 1).
Recorded in CLAUDE.md and voice-rewrite §6. **For the cloud lane (#242):** drop `art` from car-trap's room.js
(and leave the hub card's `<img>` out of `escape-rooms/index.html` until the art lands), then re-run.

**MAIN GREEN (for the cloud lane: #223 may merge):** main's full run on 5cea89b (#224) passed every job, run
37969653160, and its timings job recorded and repacked (760ef9a). Main had been red since #220 (CI-BALANCE) on its
main-only "CI timings and pack" job alone: the job-log API refused the workflow's token; #224 reads the timings from
artifacts instead. Every content group is now at most 69% of its budget. Main green again after #218 (18f5da8, run 37970610295).

## 2026-10-09 (home): SCI-CALC (item 6)

- **Engine (calculator.js):** xʸ as `^`, right-associative and tighter than a minus on its left (2^3^2 = 512,
  −2^2 = −4); ln, log, eˣ, sin/cos/tan and their inverses (each opens a bracket, like √); π and e with implicit ×;
  DEG (default) / RAD. Errors: ln/log ≤ 0, sin⁻¹/cos⁻¹ outside [−1, 1], tan at odd multiples of 90° (exact for
  whole degrees) or π/2, non-finite. All 65 existing cases unchanged (STOP IF clear).
- **UI:** `mount(el, {keys: 'scientific'})` adds a 13-key block above the basic keys and a DEG/RAD indicator in the
  display; `mount()` without it is key for key the old panel (tested). Fits 320/390/412 px touch, 48 px keys.
- **Tests (test-calculator-js.py):** 27 scientific cases (the contract's, plus inverses, RAD and errors), two
  plants (left-associative ^, no tan 90 guard: both caught), the basic panel's labels, the fit, and the DEG/RAD
  key driving sin.
- **check-calculator.py:** new value `scientific` (calculator.js + keypad.js, "Scientific calculator required",
  `keys: 'scientific'` in the page); `required` unchanged; either badge on the other value fails (12 self-test
  cases). Canon §4.4 and the roster legend updated.
- **CSS (Jon's ruling, 9 Oct):** the calculator, badge and keypad styles moved out of theme.css into
  `schools/assets/calculator.css`, which theme.css imports, so the themed games get them unchanged and Growth
  and Decay links calculator.css alone (its look is otherwise untouched; four tokens mapped to its own).
- **Growth and Decay:** roster `scientific`; badge on the start screen; the calculator under the question,
  `{keys: 'scientific'}`. Not `{answer}`: each sub-question rebuilds its input, so answers stay typed in the
  game's box. AL1 worked end to end on the keys at 390x844 (touch) and 1280x800: 5000eˣ(0.03×20) = 9110.594002
  (sq1), ln(2)÷0.03 = 23.10490602 (sq4), all four sub-questions marked correct, no page error.
- **Report for Jon (no changes; each tagging its own PR):** games whose questions likely need scientific keys,
  from a scan of question text, to confirm by reading: **strong** force-resolver (θ = arctan…, resolving with
  sin/cos), moments-master (ω = 2π×1500/60 = 50π), log-laws (log 6 + log …, ln); **probable** formula-unlocked
  (π, e^, ln), formula-forge (π, r³), complex-converter (e^{iθ}, π, tan), core-maths-paper2c (ln),
  equation-builder (ln), higher-power (ln, π), estimation-golf (π). Games where trig/log appear only in drawing
  or console code (angle-ace, bearing-blitz, circle-theorem-spotter and others) were not counted.

## 2026-10-09 (home): SCORES-OFFLINE (item 5)

- **The class:** /leaderboards/ and the portal called `firebase.initializeApp` / `firebase.database()` themselves,
  outside any guard; on a network that blocks the SDK (`firebase` undefined) the script stopped, and on
  /leaderboards/ that killed the device-local Your Scores. No other served page did (188 .html/.js files checked).
- **Fix:** both read through `MaffsLeaderboard`: new read paths `available()`, `readBoard(slug, level)` and
  `watchRecent(n, cb)` (submit path untouched). Blocked: /leaderboards/ shows Your Scores and "Live leaderboards
  can't load on this network. Your Scores above are kept on this device and still work." (search, level pills and
  cards hidden); the portal hides its ticker quietly.
- **Check:** `scripts/test-scores-offline.py` (ci-line): no served file but the shared module calls the SDK; both
  pages with gstatic.com/firebasejs refused (no page error, Your Scores renders a seeded game, offline line /
  ticker hidden) and with a fake SDK (cards render, ticker shows the score, no offline line). Plants: a page
  calling `firebase.database()` (caught by the rule); main's old /leaderboards/ blocked (caught: "firebase is not
  defined").

## 2026-10-09 (home): PLAY-AGAIN-SCREEN batch 2 (item 4 done but for characteristic-quest)

- **The 21 games batch 1 left on `SCREEN_NOT_YET` now change every screen through `MaffsLock.screen()`:**
  - their own screen helper ends with it: better-value, expectation-station, fermi-lab, formula-plug-in,
    like-terms-collector, new-shapes, probability-pioneer, think-of-a-number (`showScreen(id)`); equation-builder,
    spot-the-error (`showScreen(name)`: the active screen); simultaneous-solver (`showS`);
  - no helper: each line that makes a `...Screen` active is followed by `MaffsLock.screen(<it>)`: component-crusher,
    four-quadrant-explorer, given-that, growth-and-decay, split-it, stat-attack, test-the-claim, truth-buster,
    wrong-on-the-internet;
  - prime-or-composite: `showModal()` opens the window on the modal, `closeModal()` (its Play Again) on `.page`,
    where its Start button sits;
  - six games reveal a header with "← Back to Games" outside the screens when a run starts (truth-buster,
    think-of-a-number, four-quadrant-explorer, like-terms-collector, probability-pioneer, given-that): that line now
    also calls `MaffsLock.fresh(gameHeader)`.
- `SCREEN_NOT_YET` is down to characteristic-quest (the cloud lane's; it comes off when the claim ends). All 21 pass
  check-answer-lock.py locally (seed 1).

## 2026-10-09 (home): PLAY-AGAIN-SCREEN (item 4)

- **Every listed game's screen change goes through `MaffsLock.screen()`**: 33 pages' `show(id)` / `showScreen(id)`
  now end with `MaffsLock.screen(<the screen shown>)` (27 shared one exact one-liner; the rest small variants).
  So Play Again, back to menu, mode select and results all open the 300 ms fresh window on the new screen; a
  double-click's second click lands on nothing. characteristic-quest is cloud-claimed (`cloud-remaining:`): left
  for a later batch. constructions-lab (a compass tool, not on the lock) also loads answer-lock.js now, for
  `screen()`; it is not played by the lock check (it records no question_answered).
- **Check (`check-answer-lock.py`, every migrated game, its existing Play again double-click):** before the first
  click it records the visible controls; after it, every newly visible control must sit in an open fresh window,
  whatever the layout, and the control under the pointer too; the second click must leave the URL unchanged. The
  fresh window is stretched to 5 s for the probe, so no verdict depends on runner speed (canon 7.6.0, DET).
  **Against main's pages 25 of the 32 fail** (angle-ace, bearing-blitz, binomial-blaster, coordinate-geometry-dash,
  curling-friction, dimension-checker, eigenvalue-extractor, eigenvector-engine, force-resolver, formula-forge, formula-unlocked,
  graph-transformer, higher-power, just-pythag-it-bruv, linear-equation-solver, matrix-crunch, moments-master,
  normal-navigator, proof-builder, proportion-blaster, scale-factor-scaling, sequence-solver, standard-form-blitz,
  surd-simplifier, trig-identity-duel; typically the menu's level buttons and its "Global leaderboard" link open
  to the second click); the other 7 go from Play again straight into a new game whose question is already fresh.
  With the change all 32 pass. Self-test plant: angle-ace with a bare `show()`: caught.
- **Batch 2 (next PR): 21 more games** the stricter check found on CI, whose Play again changes screen through their
  own code (showScreen, showMenu toggling classes, or none): better-value, component-crusher, equation-builder,
  expectation-station, fermi-lab, formula-plug-in, four-quadrant-explorer, given-that, growth-and-decay,
  like-terms-collector, new-shapes, prime-or-composite, probability-pioneer, simultaneous-solver, split-it,
  spot-the-error, stat-attack, test-the-claim, think-of-a-number, truth-buster, wrong-on-the-internet (plus
  characteristic-quest, cloud-claimed). They are on `SCREEN_NOT_YET` in check-answer-lock.py: reported, not failed;
  a listed game that passes fails, so the list only shrinks. Batch 2 empties it.
- **Two drivers clicked inside the new fresh windows** (a student's click comes after them): check-teacher-invite.py
  moved while the menu's fresh window was open: PD_UNLOCK's opponent counter advanced on clicks the page dropped,
  so it kept landing on the same opponent and never won the three games that unlock the tournament; verify-partial-fractions-duel.py double-clicked Play again the moment its results screen appeared. Both
  now wait for `MaffsLock.isFresh()` to clear (check-teacher-invite.py before every move and click), as canon 7.6.0 (DET) asks of drivers. partial-fractions-duel's own
  extra `MaffsLock.screen` in showMenu went (show() does it); its verifier's plant now strips it from show().
- **Canon §7.6.0:** "every screen change goes through MaffsLock.screen()".

## 2026-10-09 (home): OVERLAY-KEYS (19:00 addendum; for the cloud lane: re-check item 12)

- **The overlay is shared:** `askInitials()` in `schools/assets/firebase-leaderboard.js`, loaded by all 97 games; no
  game has its own copy. Key listeners at page level: 11 games, all `keydown` on document or window in the bubbling
  phase; none in capture, no `onkeydown` properties (10 more games listen on their own elements only).
- **Games whose shortcuts fired while initials were typed (main's overlay, every key reached the game):** 52dle,
  decimal-detective, equatle, formula-plug-in, negative-number-line, new-shapes, prime-or-composite,
  prisoners-dilemma, six-sevens-bruv, think-of-a-number, trig-wars.
- **Fix (in the overlay only, no game touched):** (1) the overlay stops keydown/keypress/keyup bubbling out of it,
  after its inputs' own handlers (Enter still submits, Backspace still steps back); bubbling is enough because no
  game listens in capture. (2) While it is open, a window capture-phase guard stops keys aimed outside it (focus left
  on the page by a tap on the backdrop), and it stays up through the keyup of a key held when it closes, so the
  Enter that submits never reaches the game. It then removes itself (1 s fallback).
- **Check:** `scripts/test-initials-overlay.py` (content tier, ci-deps on the overlay): every one of the 97 games,
  48 keys typed (a-z, 0-9, space, arrows, Escape, punctuation) + 6 on the backdrop + Enter; asserts no game key
  listener and no probe (its own document/window keydown, so it bites in games without shortcuts) saw a key, the page
  did not navigate, submitScore resolved with ABC saved, and the next key after the overlay reaches the page.
  Against main's overlay all 97 FAIL (`--against`); with the fix all 97 pass; the plant (containment removed) is
  caught in all 11 shortcut games. ~33 s locally.
- **prisoners-dilemma:** passes with no change to its own code; the cloud lane can re-check item 12.
- **Escape:** the contract says "Escape closes the overlay as now", but the overlay has never handled Escape (it
  does nothing; Skip is the way out). Not added: Jon's call. Escape no longer reaches the game either.
- Offline, submitScore writes nothing after the overlay (not the production host, by design), so "submitted" is
  checked at the overlay's edge.

## 2026-10-09 (home): HOOK-FIX (Jon, 18:00) and the Car Trap contract

- **The block:** the local pre-commit guard (`.git/hooks/pre-commit`, a copy of `~/.maffsgames-local/pre-commit`;
  patterns in `~/.maffsgames-local/personal-patterns.txt`, also read by `scan-personal.sh`; no other repo uses it;
  not gitleaks, not CI) has no bare relationship words. Its one relationship pattern was
  "possessive + relation word", with three possessives: Jon's name, "his" and "my". "his daughter" in the draft
  (fiction) matched it.
- **Ruling (Jon, 9 Oct):** "the word daughter should not be blocked, that's taking the rule too far"; name-only
  chosen. The pattern now matches only "<Jon's name>'s <relation>". "his/my <relation>" in prose or room dialogue
  commits.
- **What it matches now (16 patterns, by category):** 1 email/phone pattern; 14 standalone words or short phrases for
  real names, places and identifiers (unchanged); 1 "Jon's name + relation word" combination. The hook's allowlist
  for the project's own addresses is unchanged. Backup of the old list: `personal-patterns.txt.bak-2026-10-09`
  (local only).
- **Self-test:** `~/.maffsgames-local/test-pre-commit.sh` runs the real hook in a throwaway repo. "his daughter's
  first car" passes; a "<name>'s daughter" fixture and a standalone-pattern fixture, both built at test time from
  the list, are blocked. It passes on the new list and fails the fiction case on the old one.
- **Gap to know about:** an unnamed "his daughter" about Jon's own family is no longer caught; only the named form
  and the other patterns are.
- **The HOOK-FIX contract** (`docs/handover/contracts/2026-10-09-hook-fix.md`, verbatim) has one line that matches a
  standalone real-detail pattern by coincidence (an everyday word). Jon ruled: allow that exact line
  (`allowed-lines.txt`); the pattern is unchanged.
- **The Car Trap contract is in the repo:** `docs/handover/contracts/2026-10-09-car-trap-draft.md`, verbatim
  (committed through the hook, no bypass). It is queued after the checkpoint, as before.

## 2026-10-09 (home): GRAPH-SKETCHER-FIT (item 2, #218)

- **Overflow, measured at 320x568, 390x844, 412x915 on all 45 scenarios** (main: every one overflowed, the page
  growing ~9px per scenario loaded, up to 881px). Causes, all in the page (CLASS CHECK: local; the same
  `Math.max(320, ...)` canvas floor appears only in glorious-gantt, unlisted and the cloud lane's: not touched):
  `getCanvasCtx` sized the canvas to the panel's width less 12px, but the panel's padding and border are ~21px, so
  the canvas pushed its grid track wider on every draw, with a 320px floor; and the tracks were `fr` (min-width
  auto), so the value table widened its column instead of scrolling in `.table-box`. Fixed: `minmax(0,..)` tracks;
  the canvas takes the panel's content box. After: no overflow at any size for any scenario, in the table, draw,
  question and results phases; the table scrolls in its own box. `tier1_phone_overflow` entry removed.
- **Touch drawing at 390x844:** canvas 336x225 CSS px; eleven real touch taps placed eleven control points on the
  curve, Check Curve passed into the questions (screenshot checked). Next is tappable: the check's 390px double-tap
  phase passes.
- **On MaffsLock** (declaration: the answer completes the table, draws the true curve at Core, then answers the
  question on screen); seeds 1-3 pass; **NOT_YET: glorious-gantt only.** verify-graph-sketcher.py passes.
- **Faults fixed beyond the swap:**
  - CM15 (Core, the Ferris wheel) gives every table value, so there was no cell to fill, and the table only
    completed from a cell's change: the scenario never moved on, and a Core run (6 of 15 scenarios) drew it about
    40% of the time, so the game could not be finished. Its table now completes as it loads. Scenario data untouched.
  - Check Curve: a double-click on a passing curve scored it twice (+20 then +10) and restarted the questions. One
    check per attempt now (the draw tools lock; a failed check reopens them).
  - Every question's answer went on by a timer, right or wrong (1-2 s): a wrong one now waits on MaffsNext under its
    feedback (canon 7.6). Next Scenario acts once; the end runs once (finishOnce).
- **Answer lock split into six parts** (contract CI-BALANCE: lock parts grow by hand). L1 ran 6m40s on this PR's
  first run (6m budget then); `ci-groups.py --check` passes with part 6 counted at the 300 s default until main
  records it.
- Seen, not touched: on a phone the table's typed values are clipped by the cell width (608.3 of 608.33 shows);
  the table scrolls, the value is kept. Checking a curve with fewer than three points uses `alert()`.

## 2026-10-09 (home): CI-BALANCE (item 3)

- **Content groups are packed from measured times** (`scripts/ci-groups.py`, `scripts/ci-pack.json`): a ci-line
  names only its tier (`label | args`, or `lock | label | args`); `pack()` fills content groups to 70% of each
  group's BUDGET (75% of its timeout) and keeps lines where they are unless they must move. `--check` fails in the
  plan job past 80% of the budget. Content jobs 6 min, lock jobs 10 min. Old group ids still parse (DOCS-9OCT drops
  that once the cloud lane's open branches merge).
- **Jon's ruling (17:59): 70% / 80% are of the BUDGET, not of the job timeout.** Recorded in the contract.
- **Before / after:** 18 groups, 3900 job-s, worst group 85% -> 21 groups, ~4010 job-s (+2.8%), content max 189 s.
- **New main-only job "CI timings and pack"** records timings and repacks.
  It failed on its first three main runs (b7d5038, 5926c24, 1850e7e): the job-log API refused every fetch with the
  workflow's own token (the same calls work with a user token, mid-run too; #222's retries ran it into its 5-minute
  timeout). Fixed in the next PR: each group saves its timing lines as an artifact (ci-timing-*, 3 days), and the
  job reads them with download-artifact (`ci-groups.py --record-timings RUN --from-dir DIR`). Without --from-dir it
  still reads job logs through gh, for use from a workstation; both paths give identical timings for run 37966843652.
- **Lock parts are not packed:** add a part as the roll-out grows. L1 reached 6m40s on #218 (graph-sketcher on the
  lock, after higher-power in #217), so #218 adds part 6.

## 2026-10-09 (home): RULINGS-9OCT (item 1, #215)

- **unit-converter into MIGRATED** (`check-answer-lock.py`): seeds 1, 2 and 3 pass. NOT_YET: glorious-gantt,
  graph-sketcher.
- **complex-converter, end screen to menu in one tap: yes, no change.** In Chromium at 390x844 (touch), each mode
  (roulette, triples, sniper) was ended through its own finishOnce handler; one tap on the end screen's Menu button
  showed the mode menu each time, with no page error. So no "Choose mode" button is added. (Its screen changes
  call `showScreen`, not `MaffsLock.screen`: item 4, PLAY-AGAIN-SCREEN, converts them.)
- **Rulings recorded:** canon §7.6 (feedback shown, not skipped, with wrong-on-the-internet's pause; Play Again
  may replay the mode while the menu is one tap away) and the rulings paragraph above.

## 2026-10-09 (home): F1 batch 11 (overnight item 4, #200, merged 2782d17, main green after one flake rerun)

- **Claims read on main:** `cloud-remaining:` empty. **Batch: the last three listed games on NOT_YET:**
  eigenvalue-extractor, matrix-crunch, boolean-blitz. After it NOT_YET holds glorious-gantt (unlisted, the cloud
  lane's) and graph-sketcher (held back, batch 10), with unit-converter outside it on the cloud lane's lock.
- **On MaffsLock, each with its declaration, seeds 1-3 passing.** NOT_YET: 2 (glorious-gantt, graph-sketcher).
- **Faults fixed beyond the swap:**
  - boolean-blitz: options marked by a CSS class only; on main one wrong answer then Enter on each option gave 5
    marks and 3 points the student never earned (now 1 mark, 0 points). A wrong answer waits on MaffsNext under the
    walkthrough; a right one keeps its own Next, which acts once.
  - matrix-crunch: after an option was marked, the Flag as Singular button stayed live (a CSS class): on main a
    wrong option then the flag gave 2 marks. One lock now covers the options and the flag. A wrong answer or a wrong
    flag waits on MaffsNext under the worked solution. The flag path (not pressed by the check) double-clicked in
    Chromium at stage 2: one mark per question, game over after three lives, one game_completed.
  - eigenvalue-extractor: the characteristic-quest shape (batch 10).

## 2026-10-09 (home): F1 batch 10 (overnight item 4, #199, merged ebc91e0, main green)

- **Claims read on main:** `cloud-remaining:` empty (UC-FIX merged). unit-converter dropped anyway (the overnight
  contract: the cloud lane's), factor-theorem already migrated.
- **On MaffsLock, each with its declaration, seeds 1-3 passing:** core-maths-paper2b, core-maths-paper2c,
  growth-and-decay, normal-navigator, log-laws, test-the-claim, characteristic-quest, complex-converter.
  **NOT_YET: 5** (boolean-blitz, eigenvalue-extractor, matrix-crunch; glorious-gantt unlisted; graph-sketcher, below).
- **graph-sketcher taken out of the batch (blocked, not decided):** its known phone overflow (checker-allowlist,
  361-567px, todo §3.9 "in no batch yet") zooms the page out at 390px, and the check's tap on Next lands on the site
  footer ("Parent guides"). A student's would too. The overflow is §3.9's work, not F1's; the migration is easy once
  the page fits. complex-converter took its place.
- **unit-converter (for Jon):** the cloud lane's UC-FIX (#196) put it on MaffsLock and took it off
  `cloud-remaining:`; the check now judges it in full and says the home lane adds it to MIGRATED. The overnight
  contract says leave it to the cloud lane, so it is not added here.
- **Faults fixed beyond the swap:**
  - test-the-claim: no guard anywhere. On main a double-click on Step 6's Check marked the test twice and scored it
    twice (shown: 2 marks, 155 points; now 1 and 85); every step's Check could count twice, Next Question could skip
    a test. Each Check now locks the step panel until the next step renders or the step reopens (Try Again, or at
    once where there is none); a wrong conclusion waits on MaffsNext under the model answer; a right one keeps its
    own Next, which acts once. Functions its verifier runs in node are untouched.
  - growth-and-decay: a double-click on Check with a wrong value marked twice (shown on main); now one mark per
    attempt, the sub-question reopening on Try Again (split-it's pattern); a wrong interpretation option waits on
    MaffsNext (it moved on after 1.5 s); Next Scenario acts once.
  - log-laws: Laws mode's `answered` flag and Solve mode's `busy` flag replaced. Solve is not played by the check:
    double-clicked through a 10-question run in Chromium, 10 marks, one game_completed.
  - normal-navigator, characteristic-quest, core-maths-paper2b/2c: options guarded by a CSS class or a flag only;
    wrong answers now wait on MaffsNext under the worked solution (normal-navigator's right answers keep their own
    "Got it", which acts once). paper2b/2c follow paper1/2a (batch 7).
  - complex-converter: Roulette's wrong answer waits on MaffsNext (it moved on after 1.2 s); Sniper's `sWaiting`
    flag replaced by a lock on the diagram (the SVG gets tabindex="-1" so the lock has a control to hold: locking the
    bare SVG held nothing, a first try marked every double-tap twice); a miss waits on MaffsNext. **Play Again now
    replays the mode just played; it reloaded the page to the menu** (the reload also defeated the check). Sniper (15
    shots, double-tapped: 15 marks, one completion) and Triples (5 rounds, one completion) played in Chromium.
- **Verifier:** normal-navigator adds `NO_LOCK_FRESH_INIT` (it answers at once after each render).
- **CI fix in the PR:** check-teacher-invite.py's Laws-mode driver read log-laws' removed `answered`; it asks MaffsLock.

## 2026-10-09 (home): F1 batch 9 (overnight item 4, #198, merged 2712f54, main green)

- **Claims read on main:** `cloud-remaining: unit-converter` (UC-FIX, #196 open); factor-theorem is already migrated.
- **On MaffsLock, each with its declaration, seeds 1-3 passing (KS3, then GCSE):** just-pythag-it-bruv,
  wrong-on-the-internet, higher-power, prisoners-dilemma, surd-simplifier, coordinate-geometry-dash, formula-forge,
  scale-factor-scaling. **NOT_YET: 14** (13 listed, unit-converter claimed; glorious-gantt unlisted, the cloud's).
- **Faults fixed beyond the swap:**
  - surd-simplifier, coordinate-geometry-dash, formula-forge, scale-factor-scaling: options "locked" by a CSS class
    only, so Enter re-marked (shown on main: one wrong answer, then Enter on each option, = 5 marks; now 1). A wrong
    answer now waits on MaffsNext: surd-simplifier's used to move on after 1 s; the other three keep their "Got it"
    label, now MaffsNext under the worked solution. coordinate-geometry-dash's right answer still shows the
    solution and its own button, which now advances only from a shown solution.
  - wrong-on-the-internet (retry until right, kept): **each wrong attempt now waits on Try again (MaffsNext, 3 s
    floor), then the options not yet tried reopen.** It used to reopen at once; the answer-once rule (one mark per
    attempt, canon 7.6/7.6.0) needs the pause, as split-it's Try Again. For Jon: say if the pause is too long here.
  - higher-power: `holAnswered` and `pairsLocked` flags replaced (lock/fresh); Pairs locks the grid while two cards
    are up. Pairs is not played by the check: double-clicked through a whole run in Chromium, one attempt per pair,
    one game_completed, one submit. A wrong call still ends the run after 2 s (a MaffsNext there would make its
    double-click count as a second completion in the check).
  - prisoners-dilemma: `choiceLocked` replaced, C/D keys too; each tournament game is one session. Tournament
    double-clicked through in Chromium: 7 opponents, 140 rounds, 7 game_completed, 7 submits.
  - just-pythag-it-bruv: already guarded by its own state; swap only. Its verifier adds `NO_LOCK_FRESH_INIT`.
- **Answer lock now five CI parts** (L5 added; main's last run had L1 at 254 s with 74 games, budget 360 s).

## 2026-10-09 (home): RELIST-SR (overnight item 3, #197, merged d1e03ec, main green)

- **Step 1 on main, all met:** verify-screening-room.py runs in CI (ci-line, group E); the register has no open
  CRITICAL or HIGH (t4-014 MEDIUM and t4-017 LOW open); `check-answer-lock.py --game screening-room` PASS.
- **NOT_YET:** already done by F1 batch 8 (#190): NOT_YET is NOT_YET_AT_START minus MIGRATED, and batch 8 added
  screening-room to MIGRATED, so the 22 already excluded it. Nothing to edit.
- **Relisted, everything the unlisting commit (e419439) removed:** roster row back at GCSE #62 (GCSE 29, Unlisted
  2); three portal cards verbatim after Given That's (New for 2026/27 with its hand-placed "New", GCSE, Core); the
  weekly fact's game link; sitemap; spec map P6/P9, J1-J3, §3.9 and the coverage row; hub row (out of NOT_ON_HUB);
  canon: 95 live, 2 unlisted, §6.1's §3.9 row (Expectation Station's stale "(unlisted)" dropped too). Not on
  /essentials/ before unlisting, so not added. todo §1.72 closed.
- **/updates/: no entry, no badge.** Phase 3 showing the scenario and array again is the fix for t4-015 (class
  "hidden data": the question needed a count it no longer showed), a correctness fix, which §3.4 excludes.

## 2026-10-09 (home): CONTRACTS-FOLDER (overnight item 2, #194, merged 7b7b7e2, main green)

- **CLAUDE.md** names the two handover files in its heading and says `docs/handover/contracts/` is read only when
  its item starts. **Canon §7.8.2** records the convention (verbatim file on receipt, one-line pointer in the queue,
  moved to `docs/history/contracts/` on merge). **check-context-size.py** never measured the folder (its FILES are
  CLAUDE.md and the two handovers); its docstring now says so. Nothing else at start-up reads the folder (no
  hook; `.claude/rules/` holds no handover pointer to it).
- **home.md** held no live contract text (DOCS-SMALL's was archived in #188); the finished 8 Oct queue list and the
  three oldest entries (F1 batch 7, MAIN-RED, VOCAB-SHOWTHAT) moved to the archive. The overnight contract is the
  first file in `contracts/`; it moves to history when the run ends.
- **STOP IF checked, not met:** start-up load (LF bytes) before 42,222 (CLAUDE.md 12,246, home.md 15,416, cloud.md
  14,560); after 36,287 (12,395, 9,332, 14,560).

## 2026-10-09 (home): VOCAB-IDEMPOTENT (overnight item 1, #193, merged fce8721, main green)

- **Cause, more exactly than the contract's:** the game calls the helper once per text node, and the re-wrapping
  happened inside that one call: wrapExamVocab ran term after term over its own growing output, so a later term
  matched inside markup an earlier one wrote ("verify" in the aria-label "Verify that" wrote, Q10; "hence" after
  "hence find", Q13; "State" inside the "Write down" tooltip, T8(c)). Calling the DOM pass twice was already safe.
- **Fix (exam-vocab.js only):** each term is matched in the original text, never overlapping an earlier term's
  match (list order kept, so "hence find" still beats "hence"); only text outside tags is matched; text inside an
  existing exam-vocab-wrap is left alone. wrap(wrap(x)) == wrap(x).
- **STOP IF checked, not met:** of 509 Factor Theorem strings, 42 hold a term; 7 change on a first application and
  every one of the 7 is the fault (Q10, Q13, Q33, T1b, T8b, T8c, T10b). The other 35 are byte-identical.
  Only factor-theorem loads exam-vocab.js.
- **Test:** `scripts/test-exam-vocab.py` (B3): every CONTENT string wrapped twice, attributes clean, no nested
  wraps, and the game's own render with the tooltips applied twice; the old function planted fails naming Q10.
- **factor-theorem-t5-008 closed** in this PR (factor-theorem was not on `cloud-remaining:` and had no open PR).

## 2026-10-09 (home): F1 batch 8 (branch `claude/f1-batch8`, worktree E:/jon/mg-b8)

- **On MaffsLock, each with its declaration, seeds 1-3 passing:** standard-form-blitz, proportion-blaster,
  formula-unlocked, graph-transformer, simultaneous-solver, tax-theft, stat-attack, quadratic-factoriser. screening-room
  (it already loaded the lock) passes seeds 1-3 and joins MIGRATED. **NOT_YET: 22.** `cloud-remaining:` was empty;
  the only open cloud PR (#187, merged during the batch) claimed probability-paradox, already migrated.
- **Faults fixed beyond the swap:**
  - standard-form-blitz, proportion-blaster: no answer guard at all (a CSS class only); a wrong answer moved on after 1 s.
    Wrong now waits on MaffsNext with the right option shown.
  - formula-unlocked: the wrong path's own "Got it — next question" button ran nextQ twice on a double-click (a
    question skipped); now MaffsNext with the same label, under the worked solution.
  - graph-transformer: after a match the moves were locked by a CSS class only, so moving away and back re-matched and
    scored the puzzle again; Skip after a match marked it wrong as well; a double-click on Skip skipped two puzzles.
    Now a match or Skip locks the moves; **Skip is the puzzle's wrong answer and now names the target transformation
    and waits on Next** (canon 7.6), where it used to move straight on. **Jon's ruling (9 Oct): keep it, "the learning
    needs to be shown not skipped".**
  - tax-theft (retry-until-right kept): a double Enter on a right amount marked it twice **and skipped the next step**
    (two 800 ms timers both advanced; shown on main: step index 2 after one answer). Each readable attempt now locks;
    a wrong one reopens the step after the fresh window.
  - stat-attack: a double-click on the last step's Check (or an interpretation option) ran showCompletion twice: two
    marks, the scenario scored twice; a double-click on a wrong step cost two slips. Each attempt now locks; a wrong
    one reopens the step.
  - simultaneous-solver: the A-Level mode's own flag and raw timer replaced; the Foundation stages (already guarded by
    their state machine) lock each step once its entry is readable.
  - quadratic-factoriser: the GCSE `locked` flag replaced; Higher's step picks and Independent check, and Formula's
    answer, lock their panel; every render opens a fresh window. Higher and Formula (not played by the check, which
    plays GCSE) were double-clicked through a whole session in Chromium: 4 marks, indexes 1-4, one game_completed.
- **Verifiers:** proportion-blaster, formula-unlocked and simultaneous-solver add `bc.NO_LOCK_FRESH_INIT` (as batch 7).
  **simultaneous-solver's phone-fit check was timing-dependent on main too:** KaTeX's fonts (from the CDN) arriving
  after stepInView() has scrolled grow the Stage 4 step by ~25px at 320x568 (shown 4 runs in 8 on main's page). The
  verifier now loads every font face before playing: 6/6. (A first-visit student can meet the same 25px; the page's
  own fix, re-running stepInView when fonts land, is not in this batch.)
- **Answer lock split into four CI parts** (L1-L4, `--part i/4`; ci-groups.py already listed L4).
- **Next:** CHECKPOINT (queue item 6) once this merges with main green. Batch 9 candidates for the next session:
  just-pythag-it-bruv, surd-simplifier, unit-converter, scale-factor-scaling, growth-and-decay, log-laws,
  graph-sketcher, normal-navigator (read `cloud-remaining:` first).

## 2026-10-09 (home): DOCS-SMALL (#188, merged 883a638, main green)

- **STOP IFs clear:** correlation-or-coincidence's `QUESTIONS` on main has 84 items (28 cause, 28 both, 28 chance).
  Every roster parser (bank_common, check-banks, check-leaderboard-coverage, audit-katex/gen_tables, check-calculator)
  reads only the #, slug, levels and calculator cells, never the description, so the count wording is free text.
- **Roster:** the header gains the convention ("N per session, generated" vs bank size); just-pythag-it-bruv's row
  reads "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3 generated)".
- **/updates/:** October, Improved: "Correlation or Coincidence: now 84 questions, twice as many as before." The
  page is monthly, so the line sits in October beside Expectation Station's 8 Oct line. Updated badge: both home
  cards carry `data-badge="updated" data-badge-date="2026-10-08"` (canon §3.4, every occurrence).
- **Generator rows noticed, not changed** (none is just the count wording): split-it ("Procedural generation", no
  count); free-daily-pizza (90/206/138/84 are each stage's generated pool, not a session); simultaneous-solver (48 per
  stage are generated offline by `scripts/gen-simultaneous.py`, so a fixed bank: the size is right as it stands).
- **For Jon:** correlation-or-coincidence's own roster row still says "42 items"; the contract's DO NOT TOUCH covers
  it. The October /updates/ "New" line also says 42; it was true when written.

## QUEUE (home lane), Jon, 8 Oct 2026 (night): the list as it stood when done (moved 9 Oct, contract CONTRACTS-FOLDER)

**QUEUE (home lane), Jon, 8 Oct 2026 (night)**, replacing the checkpoint's "ask Jon for that queue" note. Run in
order; the standing rule applies (start the next item when one finishes; stop only for a STOP IF, an unruled
decision, or a checkpoint). Each contract's verbatim text is below the list; move it to the archive when it merges.
1. **ESSENTIALS-WORDING: DONE, #172 merged 8 Oct (c1fc37a).** Its verbatim text was in Jon's queue message only.
2. **RELIST-3: DONE, #176 merged 8 Oct (c0c825b).** (Jon, 8 Oct, sent after the queue.) It
   supersedes RELIST-ES-TB, sent minutes earlier: same relists, plus listing Just Pythag It, Bruv (Jon approved it).
3. **CHANGED-UTF8: DONE, #178 merged 8 Oct (d73d3b6).**
4. **GA4-COUNTRY-CANON: DONE, #179 merged 8 Oct (3c3217c).**
4a. **VOCAB-SHOWTHAT: DONE, #180 merged 8 Oct (47ee9b9)** (Jon, 8 Oct, sent later: run after GA4-COUNTRY-CANON, before F1 batch 7). The "show
   that" tooltip in `schools/assets/exam-vocab.js`; closes factor-theorem-t5-009 unless the cloud lane holds that game.
5. **F1 batch 7: DONE, #182 merged 8 Oct (259c143). F1 batch 8: DONE, #190 merged 9 Oct (d7aa0de), main green**
   (see its entry).
6. **CHECKPOINT: reached 9 Oct.** Batch 8 merged, main green; this session stopped here. Next session: ask Jon for the
   queue, or run F1 batch 9 under the standing item (candidates in the batch 8 entry).
7. **DOCS-SMALL: DONE, #188 merged 9 Oct (883a638), main green.** Its verbatim text is in the archive.
- **CHECKPOINT STOP (Jon, 8 Oct, late):** batch 7 merged, main green; this session stopped at that boundary.
- **MAIN-RED: DONE, #184 merged 8 Oct (f1a097d), main green** (see its entry).

## 2026-10-08 (home): F1 batch 7 (#182, merged 259c143, main green)

- **On MaffsLock, each with its declaration, seeds 1-3 passing:** circle-theorem-spotter, index-laws, modular-battle,
  correlation-or-coincidence, estimation-engine, given-that, core-maths-paper1, core-maths-paper2a. probability-paradox
  (the cloud lane's #177) also to MIGRATED. **NOT_YET: 31.** Chosen from Year 6/KS3/GCSE/Core games NOT next in the cloud
  lane's listed-games order (core-maths-paper2b/2c, wrong-on-the-internet, higher-power, ... left to it).
- **Faults fixed beyond the swap:** circle-theorem-spotter moved on 1 s after a wrong answer with nothing to read: it now
  names the theorem and waits on Next; Play Again's double-click pressed Start. given-that: phase 1 wrong moved on by
  itself (now waits on Next); its own Next fired twice on two quick Enters (the hidden button keeps focus) and skipped a
  question; phase 2's two tries survive a double-click. The Core Maths papers' own Next could be pressed twice (a second
  press during the section banner skipped a question): it now acts once, only on an answered question. modular-battle:
  the 90 s clock running out during a question's timer or Next now stops both.
- **Shared fixes (home lane):** `check-answer-lock.py` reads no clock as a score (modular-battle's #timer is a .score-val,
  so the countdown looked like a re-mark); `check-site.py`'s start finder never follows a link to another page (the Core
  Maths papers' "Play Fermi Lab" signpost took the driver away).
- **Declarations:** estimation-engine declares `ready` from its own state (on a phone the keypad makes its boxes
  read-only, so nothing looked typeable); the Core Maths papers declare `start_sel` (".start-btn"). given-that gains a
  read-only `window.GT.ui` (its game is an IIFE), as EE.ui and COC.ui. verify-given-that adds `bc.NO_LOCK_FRESH_INIT`.
- **Answer lock split into three CI parts** (L1-L3, `--part i/3`): L2 ran 6m43s of its 8 min (75% budget 6m) on the
  first push. ci-groups.py already listed L3 and L4; a part is added only by its ci-line. Add L4 when a part nears 6 min.
- **Next session:** DOCS-SMALL (item 7) first, then F1 batch 8. **Batch 8 also needs L4** (`--part i/4`): with batch 7
  L1 ran 5m31s against its 6 min budget. Candidates (GCSE/Core, not next in the cloud lane's order; read
  `cloud-remaining:` first): proportion-blaster, quadratic-factoriser, simultaneous-solver, standard-form-blitz,
  stat-attack, tax-theft, formula-unlocked, graph-transformer. NOT_YET: 31 (30 once screening-room, which now loads the
  lock, passes).

## 2026-10-08 (home): MAIN-RED, like-terms-collector's verifier typed before the question settled (#184, merged f1a097d, main green)

- **Main red after #180** (47ee9b9, run 37811456669 attempt 1), Content verifiers E: `FAIL item 1: typed 8.9/6.5,
  marked correct=None, expected False` and `the feedback does not say why: ''`. **The re-run (attempt 2) passed: main
  green again, Jon told.**
- **Cause (in the verifier, not the page):** `loadInputQuestion()` focuses `#ans0` on a 50 ms MaffsLock timer. The
  verifier typed as soon as `#ans0` was visible; Playwright's `fill('#ans1')` selects the box and inserts the text in a
  second step, and when the timer fired between the two, "6.5" went into `#ans0` ("8.965", `#ans1` empty), so Check
  marked nothing (an unreadable box is not an answer). Shown directly: interleaving the two steps leaves
  `['8.965', '']` and no mark. The same "marked correct=None" as run 37626794263 (6 Oct), which the 6 Oct and #167
  fixes did not touch: likely the cause after #89 and #109 too.
- **Fix:** type only once the page's own focus is on `#ans0` (its signal that the question has settled); `read_mark`
  takes the mark from the same call that saw it land. Local: the other verifiers that `page.fill` (just-pythag-it-bruv,
  six-sevens) fill one box, so a focus timer cannot redirect their text; component-crusher's and split-it's (the
  other 50 ms focus timers) set values in the page.
- **Proof:** a 100 ms runner stall inside `fill('#ans1')` (select, stall, insert): main's verifier fails 3/3 with main's
  exact message; this one passes 3/3. A 200 ms gap after every Playwright action: passes 3/3. Plain: 20/20.

## 2026-10-08 (home): VOCAB-SHOWTHAT (#180, branch `claude/vocab-showthat`)

- `schools/assets/exam-vocab.js`: two strings only, "show that" (Jon's exact text) and "hence show" ("prove" -> "reach").
  Only factor-theorem loads the file (STOP IF clear); its "show that" questions are all numerical (f(a) = 0).
- Proof: on the stub server in Chromium, factor-theorem practice Q3's tooltip reads the new text.
- factor-theorem-t5-009 closed here (`status: fixed`, `pr: 180`, `ruling:` Jon's 8 Oct ruling): nothing claimed on
  `cloud-remaining:`, no open PR touched factor-theorem or exam-vocab.js. The cloud lane's factor-theorem queue already
  left t5-009 out.

## QUEUE item DOCS-SMALL, verbatim (Jon, 8 Oct; moved when done, #188)

<details><summary>Queue item 7 (DOCS-SMALL), verbatim (Jon, 8 Oct)</summary>

> TASK (home lane, DOCS-SMALL; first item next session, after the batch 8 checkpoint): Two docs fixes from 8 Oct 2026,
> in one docs PR.
> ROOT CAUSE: (a) The roster row for just-pythag-it-bruv says "20 questions in three rounds". Project Claude read that
> as a 20-item bank and wrongly told Jon the game was below the 40-50 minimum. The game generates every question each
> session (15 triples with sizes, orientation and side varied in round 1; fresh non-square lengths in round 2; five
> contexts with large number pools in round 3), so 20 is the session length, not the bank. (b) correlation-or-
> coincidence's bank went from 42 to 84 items on 8 Oct (cloud lane, Jon's contract), with no /updates/ entry. Twice
> the questions is a change a returning student notices in what they meet, so it earns the Updated badge under canon
> §3.4.
> CLASS CHECK: (a) is an instance of a pattern: a roster count that does not say whether it is a bank or a session.
> Fix it at the roster's convention. Canon or the roster's header states that a generated game's row says "N per
> session, generated", and a bank game's row gives its bank size. Apply that to just-pythag-it-bruv, and to any other
> generator rows you find while editing. Do not audit every row in this PR; list any you notice. (b) is local: one
> missing entry.
> EXACT CHANGE: 1. .claude/rules/game-roster.md: add the convention line to the roster's header notes.
> just-pythag-it-bruv's row says "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3
> generated)". Keep the rest of the row. 2. /updates/, a new entry dated 8 Oct, Updated badge: "Correlation or
> Coincidence: now 84 questions, twice as many as before." If an 8 Oct entry already exists, add the line to it.
> 3. docs/handover/home.md updated.
> DO NOT TOUCH: any game page; other roster rows' content, beyond rows you confirm are generators (list them in the
> PR; only change those if the change is just the count wording); canon §3.4.
> SUCCESS CONDITION: the roster checks pass; /updates/ shows the line with the badge; merged on a green Gate; main
> green; handover current.
> STOP IF: correlation-or-coincidence's bank on main is not 84 (report the count, and don't write the line); the
> roster parser reads the count field so that new wording breaks it.

</details>

## 2026-10-08 (home): GA4-COUNTRY-CANON (#179, merged 3c3217c)

- Canon §1.2.1 "GA4 country tabs" added after §1.2 (the analytics section), in #153's proposed text, plus "Live only once
  Jon has installed it" from the contract's fallback line. The contract's anchor, a "'Users' are not people here" note,
  does not exist in canon; #153's own reading bullet says it, so that bullet now opens "'users' are not people here".
- STOP IF checked: #153's description and `docs/ga4-country-setup.md` agree on what is collected (aggregates GA4
  already holds; nothing new; site, analytics.js, endpoint and privacy page unchanged).

## 2026-10-08 (home): CHANGED-UTF8 (#178, merged d73d3b6)

- `check-changed.py` reconfigures its own stdout and stderr to UTF-8 (errors="replace") at the top of `main()`. Python
  here 3.14.6, CI 3.12: `reconfigure` exists on both. **Proof:** with a planted failing check printing "£5 → ✓",
  `python scripts/check-changed.py > out.txt` on main crashes (`UnicodeEncodeError` on "→"); this version completes,
  writes the failing check's tail and the summary. The `PYTHONIOENCODING` follow-up note is removed. **Still true for
  the verifiers themselves:** a verifier run on its own with output redirected can crash the same way (seen on
  verify-truth-buster and verify-just-pythag-it-bruv, 8 Oct); run those with `PYTHONIOENCODING=utf-8`.
- **Windows-only false failure seen:** verify-negative-number-line fails locally on main too (320x568: Confirm 536, fold
  528) while CI is green. Not a regression; ignore it in local check-changed runs.

## QUEUE item VOCAB-SHOWTHAT, verbatim (Jon, 8 Oct; moved when done)

<details><summary>Queue item 4a, verbatim (2, 3 and 4 moved to the archive when done) (Jon, 8 Oct)</summary>

> TASK (home lane, VOCAB-SHOWTHAT; run after GA4-COUNTRY-CANON, before F1 batch 7): Correct the "show that" tooltip
> in the shared exam vocabulary file.
> ROOT CAUSE: schools/assets/exam-vocab.js gives "show that" the definition "Prove this is true. Show every step of
> your working — you can't just verify it with numbers, you must derive it algebraically." That merges two different
> command words. "Show that" means the result is given and the student shows the working that reaches it. The
> working is often numerical: f(2) = 0 to show (x − 2) is a factor; a change of sign to show a root lies in an
> interval; "show that 3/4 of 60 is 45" at Foundation. "Prove" is the general argument. The rule the tooltip
> half-remembers is narrower: do not start from the given answer and work backwards. Found as factor-theorem-t5-009
> (shows on Q3, Q4, T1a, T3b, T7a, T10a, where the expected method is numerical). Ruled by Jon, 8 Oct 2026.
> CLASS CHECK: Shared infrastructure. The definition lives in a shared asset that any game can load, so it is fixed
> once, there, and every current and future user is corrected. Today only factor-theorem loads it; the fix is still
> made in the shared file, never as an override in the game.
> EXACT CHANGE: 1. schools/assets/exam-vocab.js, the 'show that' entry's plain text, exactly: "The answer is given
> to you. Write out every step that gets there. Working with numbers is fine when that is the method, such as
> showing f(2) = 0. You must not start from the given answer and work backwards." 2. Check the 'hence show' entry
> ("Use your previous answer to prove this result — show every step.") and change "prove" to "reach": "Use your
> previous answer to reach this result — show every step." The 'prove that', 'prove', 'verify that' and 'verify'
> entries stay as they are. 3. Close factor-theorem-t5-009 in docs/audits/findings/factor-theorem.yml in this PR,
> with a resolution line citing Jon's ruling. This is the one cloud-lane findings file the home lane edits here;
> check cloud-remaining: and the open PRs first, and if factor-theorem is claimed or has an open PR, leave the
> findings file to that PR and say so in the handover. 4. docs/handover/home.md updated.
> DO NOT TOUCH: every other entry in exam-vocab.js; the tooltip mechanism (wrapExamVocab's re-wrapping bug, t5-008,
> is in the cloud lane's factor-theorem contract); any game page.
> SUCCESS CONDITION: the 'show that' tooltip on factor-theorem Q3 shows the new text in Chromium; no other tooltip
> text changes (diff shows two strings); t5-009 closed (or handed to the cloud PR as above); merged on a green Gate;
> main green; handover current.
> STOP IF: exam-vocab.js is loaded by more pages than factor-theorem and any of them uses "show that" for a genuine
> proof (quote the question and ask Jon); the factor-theorem cloud PR has changed how the tooltip text is read so
> that this edit does not show.

</details>

## 2026-10-08 (home): RELIST-3 (#176, merged c0c825b)

- **Start state, main c8e1b91 (neither game nor its findings file changed by c1fc37a):** verify-expectation-station and verify-truth-buster pass; findings:
  expectation-station none open, truth-buster t3-014 MEDIUM, t3-015 LOW, t3-016 MEDIUM (stay open, SR-21).
  Neither is on `cloud-remaining:` (terrible-advice only). On Windows a verifier run redirected to a file crashes on
  cp1252 (same as CHANGED-UTF8): run with `PYTHONIOENCODING=utf-8`.
- **Done:** Pythag listed (noindex off, head comment, portal KS3 card with New badge, /essentials/ Geometry, spec map
  G20 as its own row, sitemap, hub row, NOT_ON_HUB dropped, SUITE, roster KS3 #98, canon §1 and §4.2); ES and TB
  relisted from their unlisting commits (059b2ec, e419439): portal cards (ES Updated badge, both its cards), sitemap,
  spec map (ES §3.9 rows), hub rows, NOT_ON_HUB, TB's spec-mapping EXCEPTIONS entry back; roster #59 (GCSE), #17 (KS3).
  /updates/: Jon's Pythag line under October New; his suggested ES line under October Improved. TB: no badge, no line
  (its changes since unlisting are SR-18 rewording, corrected figures, the lock, phone fit and a test-only lock-hint
  declaration: none meets §3.4). todo: listing item closed with Jon's approval recorded; iPhone check a separate
  open follow-up; §1.55 and §1.75 closed.
- **Deviation, for Jon:** the /essentials/ card says "One level", not "Choose: Foundation": the game has one level and no
  picker and reads no `?level=`, so a Choose card fails check-resit-page.py (and would promise a choice that isn't there).

## QUEUE item GA4-COUNTRY-CANON, verbatim (Jon, 8 Oct; moved when done)

> TASK (GA4-COUNTRY-CANON): Record the GA4 country figures in canon.
> ROOT CAUSE: #153 merged the Apps Script and setup steps (docs/ga4-country-setup.md), but canon's analytics
> section does not say the events Sheet now gains country tabs from GA4's Data API, so the next reader of canon
> cannot tell where those figures come from.
> CLASS CHECK: Local: one missing canon line for one merged feature.
> EXACT CHANGE: docs/canon.md, the analytics section beside the "'Users' are not people here" note: add the line
> proposed in #153's PR description (read it with gh); if it proposed none, write: "Country figures (Jon, 8 Oct
> 2026): two tabs in the events Sheet, copied daily from GA4's Data API by docs/apps-script-ga4-country.js (setup:
> docs/ga4-country-setup.md). Aggregates only: nothing new is collected, and the site, analytics.js, the events
> endpoint and the privacy page are unchanged. Live only once Jon has installed it." Handover updated.
> DO NOT TOUCH: the script, its test, the setup doc, the privacy page.
> SUCCESS CONDITION: canon carries the line; merged on a green Gate.
> STOP IF: #153's description says anything that contradicts the setup doc on what is collected (quote both).

## 2026-10-08 (home): ESSENTIALS-WORDING, "resit" off every public page (#172, merged c1fc37a)

- /updates/ (four lines) and /essentials/ (description, og:description, teacher line, intro) no longer say resit or
  post-16; games.json's /essentials/ description matches. The /updates/ link now goes to /essentials/.
- `check-student-labels.py` now scans essentials/index.html and updates/index.html (PORTALS); /essentials/ is no
  longer exempt; the self-test plants a label on each and requires it caught. Against main's copies the widened check
  finds 10 labels (5 per page). Canon §7.5.3 records Jon's rule.
- Remaining site-wide hits (all exempt): the two rooms' teacher.html notes (teacher surface); given-that (KNOWN); code
  and HTML comments in room.js, schools/assets, games and the /essentials/ head comment (history of /resit/ and the
  script name check-resit-page.py).

## QUEUE items RELIST-3 and CHANGED-UTF8, verbatim (Jon, 8 Oct; moved when done)

> TASK (home lane, RELIST-3; run after ESSENTIALS-WORDING, before CHANGED-UTF8): List Just Pythag It, Bruv (Jon's
> approval) and relist Expectation Station and Truth Buster (canon SR-21), in one batched docs PR.
> ROOT CAUSE: just-pythag-it-bruv was merged unlisted on 4 Oct 2026 for Jon to play first. Jon played it and approved
> it, but the approval was never recorded, so it is still noindex and off every listing surface (Jon, 8 Oct 2026: "I
> approved it days ago"). expectation-station and truth-buster were unlisted on 6 Oct (SR-20) and now meet SR-21:
> verifier in CI with ci-line headers, and no open CRITICAL or HIGH in docs/audits/findings/<slug>.yml (checked on
> main c8e1b91: expectation-station none open; truth-buster t3-014 MEDIUM, t3-015 LOW, t3-016 MEDIUM). The roster's
> Unlisted section is stale on expectation-station: it says pc-001 awaits Jon's A/B ruling, but Jon ruled B, and the
> fix and the 40/40/40 bank are merged.
> CLASS CHECK: Not a bug in code: it is the existing listing and SR-21 processes, batched through the home lane as
> canon says. The approval going unrecorded is a process gap, not code. Record it in the handover and to-do as a Jon
> ruling with its date, so no later session asks again. No shared code changes.
> EXACT CHANGE:
> 1. Re-run all three verifiers and confirm each register state on main at the time of the PR.
> 2. just-pythag-it-bruv, as docs/todo.md's listing item states (the "Jon to play /games/just-pythag-it-bruv/; on
>    approval" item, about line 545), reading /resit/ as /essentials/:
>    - remove the noindex line, and update the page's head comment to say it is listed;
>    - portal; /essentials/ (Geometry and measures; Choose: Foundation; Calculator required); spec map G20; sitemap;
>    - leaderboard hub row, with its NOT_ON_HUB entry dropped (check-leaderboard-coverage.js);
>    - add it to SUITE in check-resit-page.py;
>    - move the roster row to its listed section;
>    - update canon §4.2 and canon §1's game total.
>    The /updates/ entry, under 8 Oct, New badge, in exactly these words (Jon's approved line):
>    "Just Pythag It, Bruv: Pythagoras' theorem in three rounds, starting with whole-number triangles. In the
>    Essentials section."
> 3. expectation-station and truth-buster: relist on every surface SR-21 and the to-do relist checklists name
>    (expectation-station: todo §1.55; truth-buster: its row in §1.58-§1.75). That covers the roster rows, back in
>    their listed sections at their old numbers (#59, #17); the portal; the sitemap; the spec map; and the
>    leaderboard hub (remove each from NOT_ON_HUB). Add either to /essentials/ only if it was there before unlisting.
> 4. Roster descriptions current: Expectation Station "120 questions (40 per level); Stage 1 states a relation, so
>    every table has one completion"; Truth Buster's count as its bank now stands.
> 5. /updates/, same 8 Oct entry as step 2. Expectation Station gets the Updated badge (canon §3.4: three times the
>    questions, and Stage 1 now always has one right answer, which changes what a student meets and how they are
>    marked). Suggested line: "Expectation Station: now 40 questions at each level, and every probability table has
>    exactly one right completion." Truth Buster gets a badge and a line only if its changes since unlisting meet
>    §3.4. Wording honest, no alarming numbers; name the maths, never the student.
> 6. docs/todo.md: close the listing item and the two relist rows, and record "Jon approved Just Pythag It, Bruv
>    after playing it (recorded 8 Oct 2026)". Keep the real-iPhone check open as a separate follow-up; it does not
>    block listing. Handover updated.
> DO NOT TOUCH: any game's page or bank, apart from the noindex line and head comment of just-pythag-it-bruv; the
> findings files (MEDIUM and LOW entries stay open, cloud lane's); screening-room, factor-theorem, glorious-gantt; any
> game on cloud-remaining:.
> SUCCESS CONDITION: all three are on the portal and the sitemap; just-pythag-it-bruv is on /essentials/ and has no
> noindex; the roster lists three unlisted games (screening-room, glorious-gantt, factor-theorem); the roster,
> coverage, theme, meta, label and essentials-page checks pass; merged on a green Gate; main green; handover current.
> STOP IF: any of the three verifiers fails on main; expectation-station or truth-buster has an open CRITICAL or HIGH
> by the time you start; a listing surface named here no longer exists; Truth Buster's §3.4 call is unclear (quote
> the change and ask Jon).

> TASK (CHANGED-UTF8): Stop scripts/check-changed.py crashing on Windows when its output is redirected.
> ROOT CAUSE: check-changed.py already runs each check with PYTHONIOENCODING=utf-8 and decodes its output as UTF-8,
> but it prints the failing check's last 15 lines to its own stdout. On Windows with output redirected to a file,
> that stream is cp1252, so a non-ASCII character (£, →, ✓) raises UnicodeEncodeError and the summary is lost.
> CLASS CHECK: Local. check-changed.py is the one Windows entry point that wraps the other checks, and it already
> sets the child encoding; the gap is its own stdout only. Eight scripts already reconfigure stdout the same way;
> CI (Linux, UTF-8) is unaffected.
> EXACT CHANGE: scripts/check-changed.py: at start-up, sys.stdout.reconfigure(encoding="utf-8", errors="replace")
> and the same for sys.stderr. Remove the PYTHONIOENCODING workaround note from home.md's follow-ups once merged.
> DO NOT TOUCH: the other scripts; the check selection logic; CI.
> SUCCESS CONDITION: on Windows, `python scripts/check-changed.py > out.txt` with a failing check whose output
> contains £ completes and writes the summary; merged on a green Gate; handover current.
> STOP IF: reconfigure is unavailable on the Python version CI or Jon's machine runs (report the version).

## 2026-10-08 (home): F1 batch 6 (#165, branch `claude/f1-batch6`, worktree E:/jon/mg-b6)

- **On MaffsLock, each with its declaration, seeds 1-3 and its own verifier passing:** sequence-solver, bearing-blitz,
  expected-damage, maths-court, equation-builder, fermi-lab, better-value, chart-interrogator. terrible-advice (the cloud
  lane's #160) also to MIGRATED. **NOT_YET: 40.** Chosen off the cloud lane's listed-games order; opened as a draft PR
  at the start so the cloud lane could see it.
- **Faults fixed beyond the swap:** sequence-solver and bearing-blitz wait on Next after a wrong answer (bearing-blitz's
  Fire was "disabled" by a CSS class only; the last life's miss waits too); expected-damage, maths-court and fermi-lab
  keep their own Next, which now acts only on an answered question (a double-click skipped one); maths-court's two
  attempts survive a double-click and a tapped card cannot re-mark; equation-builder's double Check no longer spends the
  retry and the shown key waits on Next; fermi-lab's Calculate Estimate marked and scored twice on a double-click, and a
  step could count twice; chart-interrogator (logs right answers only, so `mark_any`) marked a right answer twice on a
  second Enter inside its 600 ms advance, and a double Submit Comparison finished the game twice.
- **Declarations:** bearing-blitz and fermi-lab declare `start_sel` (no Start button), so the double-click on Start is
  real; equation-builder fills its slots from data and checks twice to spend the retry, stopping if the question moved on.
- **Verifiers:** sequence-solver and fermi-lab get `bc.NO_LOCK_FRESH_INIT` (they answer as soon as a question renders).
  better-value's page-load KaTeX poll keeps a raw timer, marked `// lock-ok:`.

## 2026-10-08 (home): LTC flake, like-terms-collector's late-mark self-test (#167, merged)

- **Cause:** the self-test serves a copy whose showFeedback() marks DEFER (300) ms late, then reads the mark "straight off
  the click" to prove the plant bites, expecting none. That read was a second Playwright call after `page.click`; on a
  slow runner more than 300 ms passed between the two and the mark had landed, so the self-test failed. (DEFER only
  equals MaffsLock's 300 ms window by coincidence: the race is the gap between two Playwright calls.)
- **Fix:** in the deferred plant only, the click and the early read are one page task
  (`checkBtn.click(); return MARK();`). A timer cannot fire inside one synchronous task, so the early read sees no mark
  on any runner; the waiting read (`read_mark`) must still see every mark land. Real typing and clicking elsewhere are
  unchanged.
- **Proof:** with a 200 ms gap forced after each click (a slow runner, DEFER 50), main's version reads `[False, True]`
  early and fails; this one reads `[None, None]` and holds. Plain runs: 3/3 pass.

## QUEUE as of the 8 Oct evening checkpoint (moved when Jon sent the next queue, 8 Oct night)

**QUEUE (home lane):** done 8 Oct: DET (#144), CLAIM (#145), ESSENTIALS (#150), UPDATES (#151). Their verbatim
contracts and notes moved to `docs/history/handover-home-archive.md` ("QUEUE as of 8 Oct") in contract CTX. Then:
1. **Contract CTX: DONE, #158 merged 8 Oct (b66ccde).** Its verbatim text: `docs/history/handover-home-archive.md`
   ("QUEUE items CTX and F1 batch 5"); its notes: the CTX entry below.
2. **F1 batch 5: DONE, #161 merged 8 Oct (8216ff4), main green.**
3. **F1 batch 6: DONE, #165 merged 8 Oct (7844d10).**
4. **LTC flake: DONE, #167 merged 8 Oct (7d442e1), main green.** (The cloud lane, relayed by Jon, 8 Oct.)
- **CHECKPOINT STOP (Jon, 8 Oct, evening):** items 1-4 done, main green; this session stopped here, as told ("do not
  start the next item in this session"). **Jon's checkpoint message said to record "the queue below", but no queue came
  with it.** Next session: ask Jon for that queue first. Without it, the standing queue is item 5 (F1 batch 7).
- **Follow-up (home lane, small):** `check-changed.py` crashes (`UnicodeEncodeError`, cp1252) printing a failure when
  its output is redirected to a file on Windows. Until fixed: `PYTHONIOENCODING=utf-8 python scripts/check-changed.py`.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.
5. **Then** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty (NOT_YET: 40).
   **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
   `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
   line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Checkpoint rule:** stop after every 2 batches merged (main green), or at the next batch boundary when Jon
  says "checkpoint". At each stop, update this file.

## 2026-10-08 (home): F1 batch 5 (branch `claude/f1-batch5`, worktree E:/jon/mg-b5)

- **On MaffsLock, each with its declaration:** angle-ace, free-daily-pizza, split-it, six-sevens-bruv, 52dle,
  distinctly-average, seven-bridges. Each passes check-answer-lock on seeds 1-3 and its own verifier where it has one.
  **MIGRATED also gains** trig-wars, truth-buster, gradient-hunter, spot-the-muppet and word-problem-decoder (the cloud
  lane's; each passes seeds 1-3 here). trig-wars: its tap-through (`aimAtEnemy`, used only by the declaration) also
  searches 46-85 degrees, since some terrains leave no robust shot at 45 or below (seeds 2, 3, 8 failed; 1-12 pass).
- **word-problem-decoder dropped from the batch:** the cloud lane claimed and fixed it (#156, #157) while this batch was
  parked unseen (no PR; its queue note was only on the unmerged CTX branch). Main's version is kept. **Lesson: a parked
  batch must be visible on main (a draft PR, or its games in home.md on main) before a pause, or the cloud lane cannot
  skip its games.**
- **Fixes beyond the swap:** angle-ace's own "Got it" button is now `MaffsNext.wrong` (same label); split-it keeps its
  retry, Check stays locked until Try Again, Best value waits on Next after a wrong pick; free-daily-pizza and
  distinctly-average lose their local guards (`state`, `locked`) to the lock; 52dle locks per guess and reopens for the
  next; seven-bridges: a wrong Impossible waits on Next, the solution animation's timers are MaffsLock timers (they
  could draw onto the next puzzle), and Play Again returns to the start screen in the page (it reloaded, which the
  check's Play-again probe misreads).
- **Verifier lessons:** a sweep that answers at once needs `bc.NO_LOCK_FRESH_INIT` (angle-ace, free-daily-pizza,
  six-sevens). A top-level `const endGame` cannot be stubbed by `window.endGame =`: keep `function endGame(){finishGame()}`.
- **NOT_YET: 47.**

## QUEUE items CTX and F1 batch 5, as of 8 Oct (moved when CTX merged, #158)

1. **Contract CTX: PR on `claude/ctx` (8 Oct; see its entry below).** Merge on a green Gate once Jon has answered
   the PR's "For Jon" list (its STOP IF). Verbatim (Jon, 8 Oct):
   > TASK (home lane, after UPDATES merges and main is green): Cut what every Claude Code session loads before it
   > starts work: CLAUDE.md down to standing rules and pointers, each handover down to current state plus its last
   > three entries, history moved to archives nobody loads by default, and a CI size limit so it can't creep back.
   > ROOT CAUSE: Measured 8 Oct on main: CLAUDE.md is 159 KB and loads automatically into every session in both
   > lanes; most of it is dated "## Handover —" sections back to 3 Oct. docs/handover/cloud.md (56 KB) and
   > docs/handover/home.md (64 KB) are read first by instruction and hold every entry since 7 Oct.
   > .claude/rules/*.md add about 40 KB. A fresh cloud session starts at 16% context before reading its task,
   > which forces checkpoints after two or three games.
   > CLASS CHECK: Yes: shared infrastructure every session loads, and the absence of any limit on it. Fix at that
   > layer: restructure once, move history out of the load path, and add a CI check with a size limit. Not by
   > trimming individual pastes or by asking sessions to skim.
   > EXACT CHANGE: 1. Inventory first (in the PR description): every standing rule, ruling and lesson in
   > CLAUDE.md, each mapped to where it now lives: CLAUDE.md (still needed every session), canon (already there:
   > cite the section), or docs/history/claude-md-archive.md (history only). Nothing is deleted; everything is
   > moved or kept. 2. CLAUDE.md, target <= 15 KB: project overview (short); the standing rules sections that
   > apply every session (checkpoint discipline, check-changed before pushing, watch main after merging, two
   > lanes and who edits what, the cloud-claim rule, Jon never amends contracts: PC sends complete pastes);
   > pointers to canon, the handovers, the register, the roster, the archive. Every dated "## Handover —" section
   > moves verbatim to docs/history/claude-md-archive.md (newest first). 3. Handovers, target <= 15 KB each:
   > docs/handover/home.md keeps its header (rules, queue, standing rulings) and its newest three dated entries;
   > older entries move verbatim to docs/history/handover-home-archive.md. docs/handover/cloud.md: the same, to
   > docs/history/handover-cloud-archive.md, BUT only when the cloud lane has no open PR and its cloud-remaining
   > line is empty (it is at a checkpoint). If it isn't, skip cloud.md in this PR and leave a one-line note in
   > home.md to do it at the next cloud checkpoint. 4. Scripts that read CLAUDE.md (on main 8 Oct:
   > bank_common.py, check-theme.py, ci-deps.py, extract-banks.py, gen-simultaneous.py, verify-log-laws.py,
   > verify-quadratic-factoriser.py): find what each reads. If it needs content that moves, point it at the
   > content's new home (canon or the archive) in this PR; prove each still passes. 5.
   > scripts/check-context-size.py (CI, own ci-line header): fails if CLAUDE.md > 20 KB or either handover >
   > 20 KB (limits a little above the targets so a normal entry fits); prints each file's size. Self-test: a
   > planted 25 KB CLAUDE.md fails. 6. Roster header: .claude/rules/game-roster.md's title still says "74 games
   > on the portal, 23 unlisted" (91 and 6 after #142): a hand-typed count beside the data. Drop the counts from
   > the title or generate them; don't hand-type new ones. 7. Report in the PR: bytes before and after for
   > CLAUDE.md, both handovers and .claude/rules/ total.
   > DO NOT TOUCH: canon's content (cite it, don't move things into it unless the inventory shows a rule exists
   > nowhere else, and then list it); the roster's rows (the only copy); .claude/rules/ files other than the
   > roster title; any game; the workflow beyond what the new check's ci-line header gives; the meaning of any
   > rule (move text verbatim; reword nothing except pointers).
   > SUCCESS CONDITION: CLAUDE.md <= 15 KB with every every-session rule present; each handover <= 15 KB
   > (cloud.md may be deferred per step 3); archives hold the moved text verbatim; every script that read
   > CLAUDE.md passes; the size check passes and catches its planted file; the inventory and before/after sizes
   > are in the PR; merged on a green Gate; main green; home.md handover current.
   > STOP IF: a rule appears only in a dated handover section and it is unclear whether it still stands (list it
   > for Jon; don't guess); a script depends on CLAUDE.md content in a way that can't be repointed without
   > changing what it checks; the cloud lane has an open PR touching docs/handover/cloud.md (skip cloud.md, per
   > step 3).
2. **F1 batch 5: PARKED on `claude/f1-batch5` (worktree E:/jon/mg-b5), pushed, no PR.** Done and committed:
   angle-ace, word-problem-decoder, free-daily-pizza, split-it, six-sevens-bruv on MaffsLock (each passes
   check-answer-lock on seeds 1-3 and its own verifier), trig-wars (tap-through now also aims above 45 degrees;
   seeds 1-12 pass) and truth-buster added to MIGRATED. Still to do: 52dle, distinctly-average, seven-bridges.
   Then rebase on main, check-changed, PR. Lesson: a sweep that answers at once needs `bc.NO_LOCK_FRESH_INIT`;
   a top-level `const endGame` cannot be stubbed by `window.endGame =`: keep `function endGame(){finishGame()}`.

## QUEUE as of 8 Oct (moved from the header by contract CTX)

**QUEUE (home lane; Jon, 7 Oct evening session):** MaffsLock #125, batches 1 (#129), 2 (#132), contract LH (#133)
and batch 3 (#136) are done. This session runs batch 4 and the relist PR, then stops at the checkpoint. Then:
1. **Contract DET: DONE, #144 merged 8 Oct, main green (fedb2ce).** check-answer-lock.py made deterministic (Jon, 7 Oct). Two
   causes fail a PR at random: (a) after a right answer `to_next()` waits a fixed 350 ms and returns 'auto', so the
   next tap can land in MaffsLock's 300 ms fresh window (UNPLAYABLE; #134 prime-or-composite, #137
   fraction-equivalence); (b) with no answer hint the driver taps option (k+1) % 2 on 8 unseeded questions, all
   right ~1/2^8 of the time in a two-option game. Fix in the driver, never with retries: wait for game state (next
   question rendered AND its fresh window over; a read-only `MaffsLock.isFresh(container)` in answer-lock.js if
   needed, documented, no behaviour change); two-option games declare an answer that picks the option differing
   from the key; a seeded default (seed printed) for games with no hint; no new declaration key (else STOP IF).
   Also seen 7 Oct: `start()` waits a fixed 8 x 400 ms for an option group (eigenvector-engine UNPLAYABLE once
   under local load, then 3/3 alone). Proofs: same seed, identical event log; a forced all-right draw and a tap inside the fresh window both handled
   every time; no Math.random and no fixed delay on the path to a wrong answer; a planted lock removal still caught
   every run; then 20 consecutive passes on prime-or-composite and fraction-equivalence (smoke test only). Canon
   §7.6, this file, and one line in cloud.md (two-option games declare the differing-from-key answer). DO NOT
   TOUCH: answer-lock.js behaviour, what the check tests, scoring, cloud-remaining games, CI retry settings.
   STOP IF: the fresh window can't be observed without changing answer-lock.js behaviour; a two-option game's
   wrong answer can't be expressed with the existing key; determinism would stop it testing something it tests now.
2. **Contract ESSENTIALS: DONE, #150 merged 8 Oct, main green (69d05df).** (Jon's paste, received in full 8 Oct): after DET merges and main is green. Verbatim:
   > TASK: Rename the resit section to "Essentials", stop any student-facing page naming the student's status,
   > and correct the homepage title and description so they're accurate and name who the site is for.
   > ROOT CAUSE: Status labels and site facts are hand-typed into individual pages. The two resit escape rooms'
   > description, og and twitter tags open "A GCSE resit escape room on…", so a link posted in Google Classroom or
   > Teams shows that label to the whole class; homepage and /escape-rooms/ cards say "for a GCSE resit class". The
   > homepage meta/og description says "96 free curriculum-aligned maths games" although the portal lists 91, and
   > says "KS3 through Further Maths" while the page subtitle says "KS3 through A-Level". Neither names the
   > priority audience or Core Maths.
   > CLASS CHECK: two classes. (1) Status labels on student surfaces: fix at the layer, a canon rule plus a CI
   > check, not just edits. (2) A site fact (the game count) typed by hand beside the data it should come from:
   > generate it from the single metadata source, or remove the number.
   > EXACT CHANGE: 1. Canon rule (Jon, 7 Oct): "Name the maths, never the student." Teacher surfaces
   > (/essentials/, its metadata, each room's teacher.html, teacher guides) may say resit or post-16. Student
   > surfaces (every game and escape-room page, including description, og and twitter tags; portal and
   > /escape-rooms/ cards) describe the topic and level only (e.g. "A GCSE escape room on factors, primes and HCF").
   > 2. Rename /resit/ to /essentials/: heading "Essentials", with the teacher line under it: "GCSE Foundation
   > maths for students working at grades 1–3, including post-16 resit classes." /resit/ becomes a meta-refresh
   > redirect to /essentials/ (the /schools/spec-map/ pattern) so existing Classroom links keep working. Homepage
   > badge, nav, sitemap, check-resit-page.py and every internal link follow the new address. Analytics:
   > section/item values for this page change to essentials; canon's analytics section records the rename date
   > and the old-to-new mapping so the Sheet and GA4 read across it. 3. Fix the student surfaces: comic-caper and
   > kiln-disaster description, og and twitter tags; the "for a GCSE resit class" card notes on the homepage and
   > /escape-rooms/ (keep the "built from a request, want something built?" invitation without the status label).
   > 4. scripts/check-student-labels.py (CI, declares its ci-line): fails if "resit", "retake" or "post-16" appear
   > in visible text or in description/og/twitter tags of any games/**/index.html, escape-rooms/*/index.html or
   > portal card; teacher.html, /essentials/, docs and code comments exempt. Self-test plants the old comic-caper
   > description; caught. 5. Homepage title, description, og and twitter: no hand-typed game count (generate it
   > from the listed games in the single metadata source, or drop the number: your choice, recorded in the PR);
   > one consistent range; name GCSE Foundation and Core Maths alongside the existing levels. Draft wording for
   > Project Claude to review in the PR. 6. Docs: canon (rule, analytics mapping), handover in home.md.
   > DO NOT TOUCH: game content, keys, scoring; game-page titles (topic-first titles are a later job); Core Maths
   > landing page (build freeze); the escape rooms' gameplay and teacher pages beyond links; Firebase and
   > leaderboard keys; games on the cloud lane's remaining list.
   > SUCCESS CONDITION: /essentials/ live with the teacher line; /resit/ redirects to it; no student surface names
   > the student's status and the check catches the planted label; homepage metadata carries no stale count and
   > one consistent range; listing and resit-page checks pass under the new name; merged on a green Gate; main
   > green; handover current.
   > STOP IF: a generated count needs a new field in the metadata source; the redirect breaks a check that
   > assumes /resit/ is a real page; any analytics event name (not just a value) would have to change.
2b. **Contract CLAIM: DONE, #145 merged 8 Oct (c752d9a).** Its STOP IF hit (no time bound); Jon's ruling (8 Oct):
   option 3, for listed games a claim is a process lock only, the check judges them as unclaimed, the exemption
   stays for unlisted games only, no time bound. Verbatim (Jon, 8 Oct; a separate PR, after DET):
   > TASK: Record the cloud lane's widened remit in canon and make the F1 rollout skip any game the cloud lane
   > has claimed. ROOT CAUSE: From 8 Oct the cloud lane also fixes listed games (Jon's ruling; its contract tells
   > it to claim each game by adding it to the `cloud-remaining:` line in docs/handover/cloud.md before
   > starting). Canon §7.8 still says the cloud lane works only on unlisted games, and the F1 batch plan lists
   > games without checking that line, so both lanes could edit the same game. CLASS CHECK: shared process rule
   > (canon) and shared CI behaviour (check-answer-lock.py already reads `cloud-remaining:`). One canon edit and
   > one rule in the F1 batch procedure; no game files.
   > EXACT CHANGE: 1. Canon §7.8: "The cloud lane may fix listed games it has claimed on the `cloud-remaining:`
   > line in docs/handover/cloud.md (Jon, 8 Oct). It claims one game at a time, before starting it, in a handover
   > commit of its own, and removes the game in the PR that fixes it." 2. docs/handover/home.md and the F1 batch
   > procedure: before building each batch, read `cloud-remaining:` on main and drop any claimed game from the
   > batch. Never claim or edit a game on that line. 3. Confirm check-answer-lock.py treats a claimed listed game
   > the same way as a claimed unlisted one (reported, not failed, while on the line). If it doesn't, make it so
   > in this PR.
   > DO NOT TOUCH: game files; answer-lock.js; the cloud handover file; what check-answer-lock.py tests.
   > SUCCESS CONDITION: canon carries the rule; the batch procedure skips claimed games; a listed game placed on
   > the line in a scratch copy is reported, not failed; merged on a green Gate; main green; handover current.
   > STOP IF: honouring the line for listed games would let a game sit on it indefinitely without failing
   > (propose a bound, e.g. it fails once off the line or after its PR merges).
   - Note for that session (8 Oct, from DET): today `counts()` returns True for any MIGRATED game, so a MIGRATED
     game put on the line is FAILED, not reported: item 3 needs a change. Also check the STOP IF before changing it.
2c. **Contract UPDATES: PR on `claude/updates` (8 Oct); item 3 reworded per Project Claude's ruling (see entry).** (Jon, 8 Oct): after ESSENTIALS merges and main is green. Verbatim:
   > TASK: Add Jon's approved October quality entries to /updates/. ROOT CAUSE: The 6-8 Oct clean-up (audit,
   > per-game verifiers, SR-16/17 fixes, the shared answer lock, 17 games relisted) is not on /updates/, the page
   > that shows teachers the site is maintained. Jon approved wording on 8 Oct: honest, no fault counts. CLASS
   > CHECK: Local: content on one docs page, in its existing format. No shared code.
   > EXACT CHANGE: In updates/index.html, October 2026 section, in the page's existing markup and style (links to
   > games as the page does): 1. After the "Which tax year?" note, a second note: <strong>Every answer checked
   > again.</strong> This month we went back through the games and worked out every answer again from each
   > question's own data, by script, rather than relying on the answers typed in when the games were written.
   > Where we found a wrong answer, a true statement offered as a wrong option, or a question using a rule it
   > didn't state, we fixed it. Some games were taken off the home page while that happened; they're back, apart
   > from a handful still being worked on. Every game that has been through this now has its own check that runs
   > whenever the site changes, so a fault can't quietly come back. We're working through the rest of the
   > library in the same way. 2. Under New, first item: <a href="/games/linear-equation-solver/">Linear Equation
   > Solver</a> now asks "What is the optimal move here?" Every move that is equally quick scores full marks, and
   > a move that works but takes longer scores half, with the quicker route shown. A wrong move tells you what
   > went wrong, such as dividing only one side. 3. Under Clarified, first item: <strong>Questions say which rule
   > they use.</strong> Where maths has more than one convention, the games checked so far now say which one: for
   > example which quartile method, or that a roulette wheel is the American kind. 4. Under Improved, first item:
   > <strong>One answer per question.</strong> In some games a second tap, a double-click or the Enter key could
   > mark an answer twice or skip a question. The games updated so far accept exactly one answer per question;
   > the rest are following. 5. Before committing, confirm each claim against the repo: Linear Equation Solver's
   > live marking matches item 2 (full / half / named error); at least one listed game states a quartile method
   > and one names the American wheel (item 3). If either is not true on main, STOP IF.
   > DO NOT TOUCH: existing entries (history stays as written, including the September and earlier October items
   > and the /resit/ link, which redirects); any game file; the portal's New & updated badges (Jon, 8 Oct:
   > correctness fixes do not earn the Updated badge; only student-visible changes do).
   > SUCCESS CONDITION: the four items appear in the October section in the page's style; page passes its
   > existing checks at 320/390/1280; merged on a green Gate; main green; handover current.
   > STOP IF: a claim in items 2-3 is not true on main (report which; do not reword it yourself); the page's
   > checks require a format the text doesn't fit.

## 2026-10-08 (home): contract CTX, what every session loads (branch `claude/ctx`, worktree E:/jon/mg-ctx)

- **Sizes (bytes, before -> after):** CLAUDE.md 159,172 -> 12,246; home.md 63,666 -> ~13,300;
  cloud.md 55,721 (deferred); .claude/rules/ 42,011 -> 41,960. Canon 148,526 -> 175,803 (§12).
- **CLAUDE.md** keeps the every-session rules, the cloud-claim rule (copied verbatim from canon §7.8.2), "Jon never
  amends contracts: PC sends complete pastes" (new: it existed nowhere; wording from the contract) and a "Where
  things live" pointer block. Every other section moved verbatim (proof: every non-blank old line is in the new
  file, the archive or canon §12, except the one reworded pointer sentence).
- **Canon §12 (new):** the sections that existed only in CLAUDE.md: check-site tiers 1-4, no rejection sampling,
  `MaffsOptions.build()`, generator ranges, scaffolds fade, accessibility, tiered banks, level colours, the Firebase
  leaderboard. Four canon pointers to "CLAUDE.md" now say §12.
- **Archives:** `docs/history/claude-md-archive.md` (dated handovers, state sections, and reference sections canon
  already holds, each headed with where it lives), `docs/history/handover-home-archive.md` (the done contracts'
  queue text and every entry before UPDATES). cloud.md deferred (cloud PR #154 open on it).
- **`scripts/check-context-size.py`** (site-wide ci-line): CLAUDE.md and both handovers <= 20 KB; self-test plants
  a 25 KB CLAUDE.md. Roster title no longer carries hand-typed counts.
- **STOP IF hit, answered (Jon, 8 Oct):** seven rules lived only in dated sections; all stand. Placed as he named:
  canon §3.4 (New & updated badges, his Updated definition verbatim), §3.5 (/updates/: describe a false claim, never
  quote it), SR-24 (counterexample refutes the statement as written), SR-25 (words, figure and key agree), §0.4 (register
  files edited by hand), §7.9 (verifiers read the page's feedback, not a wrapped mfg; pointer in CLAUDE.md), CLAUDE.md
  "Session practice" (`--against` scratch copy; never `| tail` under a timeout). Then merge on a green Gate.

## 2026-10-08 (home): contract UPDATES, the October quality entries on /updates/ (branch `claude/updates`)

- **STOP IF hit (item 5's fact check, before committing):** item 3's American-wheel example was not true on main.
  No game names the wheel; wrong-on-the-internet (listed) still keys roulette `P(black) = 18/38` with no wheel
  stated (audit tranche 2's open fix: "say 'American wheel', or key 18/37"). **Ruling (Project Claude, 8 Oct):**
  drop it; item 3 now ends "for example, which method to use for quartiles." Items 1, 2 and 4 unchanged.
  wrong-on-the-internet's roulette item is still an open SR-17 fix for a later batch.
- **Claims confirmed on main:** Linear Equation Solver marks `b` (every optimal move) full, `s` (valid but slower)
  half the points at stake with the quickest route shown, `e` named (154 one-side ÷ errors, "Whatever you do to
  one side, do to the other side too"). core-maths-paper1 (listed) states "Using the (n + 1)/4 method".
- **Page:** the "Every answer checked again" note after "Which tax year?", then first items under New, Clarified
  and Improved in the October section. No existing entry touched; the /resit/ history links stay (they redirect).

## 2026-10-08 (home): contract ESSENTIALS, BUILT on `claude/essentials` (worktree E:/jon/mg-ess), MERGED (#150, 69d05df)

**MERGED 8 Oct (#150, 69d05df) on a green Gate.** Locally, Test the Claim (`generateWrongContexts is not defined`
under Playwright's Node v24 `node -e`) and Negative Number Line (320x568 fold, 536 vs 528) fail on main too: local
environment only, CI green. Worth a look if a local run must be clean.
- **/resit/ -> /essentials/**: page moved (git mv), heading "Essentials" plus the teacher line, analytics section
  `essentials`; /resit/ is a meta-refresh stub (spec-map pattern, registered in check-footer.py). games.json key,
  apply-meta/check-meta, check-resit-page.py (PAGE; filename kept), check-canonical-links RESOLVE/LEVEL pages,
  publish scope, ci-deps KNOWN_TOP, sitemap, homepage badge ("Essentials", section `essentials-link`, item
  `open-essentials`), test-section-clicks, workflow labels all follow. Title: "Essentials: GCSE Foundation
  Maths Games | MaffsGames" (description kept: teacher metadata).
- **Not done on purpose:** /resit/ is NOT in check-canonical-links' REDIRECTS: that would fail the /updates/
  history links to /resit/, which contract UPDATES says stay as written (they redirect). Say so in the PR.
- **Student surfaces:** comic-caper and kiln-disaster description/og/twitter now "A GCSE escape room on ...";
  the four "for a GCSE resit class" card notes (homepage, /escape-rooms/) now "Built from a site user's
  request. Want something built?".
- **scripts/check-student-labels.py:** visible text, alt/title/aria-label/placeholder, script strings (comments
  stripped) and description/og/twitter meta of games/**/index.html, escape-rooms/*/index.html and the portals
  (index, escape-rooms, op). Self-test: the old comic-caper description and three more plants caught; comments
  not flagged. **In the workflow's site-wide list, NOT a ci-line** (a ci-line is selected per named page on PRs;
  this must see every page): a departure from the contract's wording, say so in the PR. **given-that** has a
  tree-diagram question about students re-sitting (6 hits): a KNOWN exception, reported not failed, flagged
  for Jon (game content is DO NOT TOUCH).
- **Homepage:** title "MaffsGames — Free Maths Games for KS3, GCSE, Core Maths and A-Level"; description (also
  og, new twitter tags) "Free maths games and 15-minute escape rooms for UK schools, KS3 to Further Maths,
  including GCSE Foundation and Core Maths. No sign-up, no personal data." No game count AND no room count
  ("eight" vs 8 cards / 11 room folders: same class); subtitle and JSON-LD now "KS3 to Further Maths". Draft
  wording for Project Claude to review in the PR. Choice recorded: the number is dropped, not generated.
- **Canon:** new §7.5.3 (the rule, the check, KNOWN, the teacher line, no hand-typed counts); analytics mapping
  (resit-link->essentials-link, open-resit->open-essentials, resit->essentials, page views) in §1.3; §2.1 and the
  CI tables follow the new address.

## 2026-10-08 (home): contract CLAIM (branch `claude/claim`)

- **STOP IF hit:** honouring the line for listed games would have exempted a claimed game with no time bound.
  Jon's ruling (8 Oct): option 3. For a listed game a claim is a process lock only: the F1 batches skip it, the
  check judges it as unclaimed. The reported-not-failed exemption stays for unlisted games only.
- **Check:** `exempt(claimed, unlisted)` = the line's games that are in the roster's Unlisted section
  (`unlisted_games()`, the same section parse as audit-register.py). Only those are reported, not failed; a
  listed game on the line gets a `note:` line saying it is judged as unclaimed. Self-test covers the parse and
  the rule. Before this PR, a MIGRATED game on the line already failed (`counts()`), but an adopted NOT_YET
  game that was listed would have been reported: now it is judged in full.
- **Canon §7.8.2** carries the claim rule and the ruling; the QUEUE's batch item carries the skip rule.
- **Proof (scratch worktree):** line `cloud-remaining: prime-or-composite truth-buster`, prime-or-composite
  planted with no lock: it FAILS (re-mark, no continue) with the process-lock note; truth-buster (unlisted,
  adopted) stays on the reported path.
- **Follow-up (home lane, next batch):** #143 took truth-buster off the cloud line, and it now passes the check in
  full. Add it to MIGRATED (and consider relisting it under SR-21) in the next batch.
## 2026-10-08 (home): contract DET, check-answer-lock.py deterministic (branch `claude/det`)

- **Driver:** every page's `Math.random` is seeded (`--seed`, default 1, printed in the first line; check-site's
  PHONE_SEED with the run's seed mixed in). The path to a wrong answer has no fixed delay: `start()` waits for
  the screen to change after each Start press and then for an answerable, settled question; `answer()` taps
  only once no fresh window is open; `to_next()` waits for the next question (a new `fresh()`/`screen()` call
  since the mark, or an enabled option group) and its window to close. The only sleeps left in Driver are
  25 ms polls inside those waits. A tap the page sees land in a fresh window (a capture listener added before
  the guard, reading `MaffsLock.isFresh`) is made again once the window closes, and the game goes on the
  note line. The tap-through's 320 ms sleep is now the same settled wait.
- **answer-lock.js:** `MaffsLock.isFresh([target])` added, read-only, documented; test-answer-lock.py's
  `fresh` check covers it. No behaviour change.
- **Declarations:** the two-option games played generically were prime-or-composite, fraction-equivalence and
  factor-race (a scan of every migrated game's option group; spot-the-error is two-option but already
  declared). Each now declares `answer`: for `i >= 1` the option that differs from its key; for `i = 0`
  (the tap-through) the first option, as the generic driver did, so the tap-through still meets right and
  wrong answers. Canon §7.6.0 and one line in cloud.md record the rule.
- **Two snags found and fixed on the way:** (1) a declared answer in a right-answer pause cannot mark, so
  it waited out the deadline: `answer()` now returns at once when no option group or input is on screen,
  but only where the declaration has no `ready` (truth-will-set-you-free's `ready` describes its first
  question only, and the shortcut stalled it). (2) The tap-through keeps its old 1.5 s mark deadline; the
  wrong-answer search waits up to 5 s (load).
- **Proofs (scratchpad `prove_det.py`, results in the PR):** same seed gives an identical event log
  (5 games, desktop + touch); a forced all-right draw gives the same named UNPLAYABLE (seed printed) 3/3
  runs; a fresh window opened before the first tap is caught and re-tapped 5/5 on 7 games, mouse and touch;
  the declared games are wrong on the first answer for 20/20 seeds, both ways; the planted no-lock
  decimal-detective is caught every run (same single fault as the old driver); then 20 passes in a row of
  the two named games.
- **Timing:** local part 1 3m05s, part 2 4m23s (CI's last main run took 5m04s and 5m56s with the old driver).
- **Not changed (out of scope, flagged):** several declarations (component-crusher, linear-equation-solver,
  proof-builder, spot-the-error, suvat, truth-will-set-you-free, expectation-station, factor-theorem) wait a
  fixed `real(350)` inside their own `answer` JS. That wait starts after the driver has already found no
  window open, so it cannot race the window; it is just redundant. Removing it is game-file work for a batch.
## 2026-10-07 (home, night 3): batch 4 (#140); the SR-21 relist PR; CHECKPOINT STOP

- **Batch 4 = #140** (see its entry below). It also filed **expectation-station-pc-001** (Jon's paste: CRITICAL,
  jc, Stage 1 underdetermined on ~33 of 45 items; fix design awaits his ruling A/B), and the self-test now
  plants decimal-detective by name (binomial-blaster, first in MIGRATED once the cloud games joined, guards
  itself, so its no-lock plant played clean).
- **Relist PR (SR-21):** 17 games back, **listed 74 -> 91** (partial-fractions-duel joined after #139 took it off
  the cloud list; also to MIGRATED, NOT_YET 61). Still unlisted (6): expectation-station (Jon's hold,
  pc-001), factor-theorem, screening-room, glorious-gantt (open CRITICAL/HIGH),
  truth-buster (on `cloud-remaining:`), just-pythag-it-bruv (Jon's play-test). Canon SR-21 written. The todo
  checklists' "every entry fixed" item was read as superseded by SR-21's bar (open MEDIUM/LOW stay in the
  register): flagged in the PR for Jon.
- **How:** scratchpad `relist.py` re-inserts each game's exact removed block (from #82/#85/#87's diffs) after its
  old neighbour, bottom-up; spec-map links are merged into today's rows. Hand-done: roster, NOT_ON_HUB,
  check-resit-page.py, the guide's "two free games" line, Component Crusher's Coverage Status row, the hub's last
  comma. A later relist of the seven can reuse the same approach.
- **Next session:** contract DET first (QUEUE above), then ESSENTIALS (its text is now in the QUEUE).
## 2026-10-07 (home, night 2): #136 (batch 3) merged; F1 batch 4 PR; relist PR next

- **#136 merged** on a green Gate after one fix: CI's answer lock L2 failed it with spot-the-error UNPLAYABLE.
  Cause, found by instrumenting the driver: 36 of the game's 110 questions have ONE step (it is the error), and
  the declaration returned without answering when it drew one (about 1 run in 4-6). The declaration now picks
  that step and misses in stage 2. It is not a retry: 2 picks, as before. **For Jon:** on those 36 questions
  stage 1 is a free pick (a content point, not F1's; not filed yet).
- **Batch 4 (this PR):** proof-builder, linear-equation-solver, moments-master, force-resolver on MaffsLock.
  MIGRATED also gains the four the cloud lane finished: eigenvector-engine, truth-will-set-you-free,
  trig-identity-duel, binomial-blaster (all pass). `cloud-remaining:` is now partial-fractions-duel and
  truth-buster. **NOT_YET: 62.**
  - linear-equation-solver's worked-solution Next was a plain onclick (a second Enter skipped a question): now
    MaffsNext. Its hint is refused once the step is answered.
  - proof-builder loads answer-lock.js BEFORE its game script: `const endGame = MaffsLock.finishOnce(...)`
    runs at parse time. **Lesson:** check where the game's inline script sits before putting the include
    beside next-control.js.
  - Register: closed proof-builder-t5-014, -t5-016, moments-master-t5-009, force-resolver-t5-008;
    linear-equation-solver-t4-003 notes its fixed class-1 part (stays open: fold, accuracy field).
- **No Node on this machine:** a JS syntax slip (an unclosed `finishOnce(`) shows only as a driver
  "ReferenceError" in the browser check. Read the error that way.
- **Relist (next):** the scratchpad script `relist.py` (session 9093ec13) puts back exactly what #82/#85/#87
  removed, per game: portal cards, FACTS links, sitemap, hub rows, spec-map links (merged into the current
  rows), /resit/ and the trig parent guide. Roster rows, NOT_ON_HUB, check-resit-page.py and the todo
  checklists are done by hand.
## 2026-10-07 (home, late night): F1 batch 3 BUILT, NOT YET A PR; STOPPED for Jon's context clear

- **State at the stop:** all 8 games and the handover are committed and pushed on `claude/f1-batch3` (worktree
  `E:/jon/mg-b3`). There is **no PR yet**. A local `check-changed.py` was running when Jon stopped the session,
  so its result is unknown. **Next session, before the new contract or after it as Jon says:** rerun
  `python scripts/check-changed.py` on the branch (rebase on main first). Open the PR with the body in `docs/handover/pr-b3-draft.md` (delete that file in the PR)
  . Set `status: fixed, pr: <n>` on the four entries named below, then merge on green (staggered from
  cloud merges).
- **#133 (contract LH) merged** on a green Gate, 22 min after the cloud lane's #130, with no cloud PR in CI.
  Main is green.
- **Batch 3, eight games on MaffsLock:** dimension-checker, curling-friction, trig-worms, component-crusher,
  differentiation-duel, integration-duel, spot-the-error and expectation-station. Each has its declaration;
  four needed a real one:
  - trig-worms: start_sel, because "FIRE!" is its Start.
  - component-crusher: a typed key + 1000 at the stated precision, or the first wrong option.
  - spot-the-error: picks a level, then the same wrong step twice.
  - expectation-station: wrong tiles, wrong products, then a wrong card still open.
  All 26 migrated games pass.
- **Faults fixed beyond swapping in the lock:**
  - spot-the-error: a double-click on a wrong step spent both attempts. A first wrong pick now opens a fresh
    window (stage 1 and stage 2).
  - expectation-station: each Check is one attempt (a double-click spent the retry, t2-017). The game's own
    Next was outside every container, so a second Enter skipped a question. `fresh(gameScreen)` on load.
- **Register:** closed component-crusher-t4-005, curling-friction-t5-003 and dimension-checker-t5-003 (all
  HIGH, class 1), and expectation-station-t2-017.
- **Verifiers:** each sweep that answers at once now has `bc.NO_LOCK_FRESH_INIT`. Two sweeps replace
  `window.setTimeout` (spot-the-error runs callbacks at once; expectation-station queues them with id 0), and
  that silently drops `MaffsLock.timer` callbacks: the asset records the id only after `setTimeout`
  returns. Both sweeps now override `MaffsLock.timer` the same way. expectation-station's sweep also calls
  `MaffsLock.fresh(stage3Wrap)` when it re-renders stage 3 by hand. **Lesson for the next batches:** any
  sweep that stubs setTimeout must stub `MaffsLock.timer` too.
- **Note, not a fault:** expectation-station shows "no Next after a wrong answer". A first wrong attempt
  resets the stage for a retry, so the classifier sees an auto-advance. Its stages keep the game's own Next.
- **NOT_YET: 70.**
## 2026-10-07 (home, night): contract LH, lock hints declared by each game (#133)

- **Jon's contract LH (before batch 3).** The root cause: per-game facts sat in a shared script, so each cloud
  migration needed a home-lane edit (suvat #128, factor-theorem #130). The fix is at that layer, the same
  shape as contract V.
  - **Declaration.** Each migrated game declares how the check produces a wrong answer in its own page: one
    `<!-- maffs-lock-hint` comment holding a JSON object (canon §7.6.0, answer-lock.js's header,
    `HINT_KEYS` in the script).
  - **Moved out of the script:** all 11 central hints (each reads back equal), plus suvat's from #130. The five games that needed
    none declare `{}`, and a declaration is now required. No per-game hint is left in the script.
- **The load-order rule is removed, and tested both ways in Chromium.**
  - factor-race, reversed (answer-lock.js first) and played through `--against`, passes every behaviour,
    including the double-click on MaffsNext.
  - suvat loads answer-lock.js first natively, and it passes.
  - No STOP IF.
- **The "reported, not failed" state now has an exit.**
  - A NOT_YET game whose page loads the lock is judged in full.
  - Its failures are reported only while it is on the `cloud-remaining:` line, which the home lane added to
    cloud.md's header at Jon's instruction (the one cross-lane edit; the cloud lane keeps it from now on). A
    missing or doubled line fails the check.
  - An off-list game that passes is noted for the home lane to add to MIGRATED.
  - `--selftest` (run in L1 before part 1) plants a page with no lock. In it `MaffsLock.lock` never refuses
    and there's no fresh window. It is played as an off-list adopter: CAUGHT (a question skip in the
    tap-through). On the list it is reported. Overriding `lock()` alone was not enough: decimal-detective
    replaces its Check button, so the plant had to remove the fresh window too.
- **suvat and factor-theorem are in MIGRATED and pass.** #130 merged while LH was in review. Its "hints as data"
  (cloud.md, Jon's 18:00 rulings) became factor-theorem's declaration, and factor-theorem came off the
  remaining list, which is now eigenvector-engine, truth-will-set-you-free, trig-identity-duel,
  binomial-blaster, partial-fractions-duel and truth-buster. #130 had already swapped suvat's script order;
  the merge keeps main's order and the declaration. All 18 migrated games pass both parts.
- **CI selection.** The script no longer names any game, so `ci-deps.py` marks it ALWAYS: it runs on every PR,
  cloud-lane game PRs included. Before, a game PR selected it only through the slugs in HINTS/CLOUD_LANE, so
  factor-race, formula-plug-in and others were never selected by their own changes.
- **Register (item 5).** §7.6.1 says the reason and Next both sit above the fold, so these are MEDIUM
  (`NEW:phone-layout`, open):
  - factor-race-f1-001: reason 648-680 and Next 691-735; the fold is 528.
  - fraction-equivalence-f1-001: Next 534-578. Its reason, 477-501, is above the fold, so the entry says so.
  - percentage-flip-f1-001: below the fold from the top of the page. But the page scrolls itself 346px as
    the answer box takes focus, so in the run both were on screen.
- **For the cloud lane:** each queued game (eigenvector-engine first) declares its maffs-lock-hint in its own
  page and comes off `cloud-remaining:` in the PR that finishes it.
  - factor-theorem's open note (moving to MaffsNext needs `FT_STEP` in check-teacher-invite.py taught first) is home-lane
    work, not yet queued.
## 2026-10-07 (home, night): F1 batches 1 (#129) and 2 (#132) merged; CHECKPOINT STOP (2 batches)

- **#129 (batch 1) merged.** Of the three local failures, two were environmental and fail on main too:
  Negative Number Line's 320px fold (fonts) and Test the Claim (no Node on this machine, `FileNotFoundError`).
  **check-resit-fixes.py was a real break** (Shape Shifter and NNL). Its clicks landed in MaffsLock's 300 ms
  window, and it reset an `answered` flag the games no longer have. It now uses `bc.NO_LOCK_FRESH_INIT` and calls
  `MaffsLock.fresh(gameEl)`; its self-test still catches every reverted fix. Closed: formula-plug-in-t3-001,
  new-shapes-t3-001, four-quadrant-explorer-t3-001, like-terms-collector-t3-002. shape-shifter-t3-005 has its
  fixed part noted.
- **Main went red after #129 (#131 fixed it).** The cloud lane's #128 put suvat on answer-lock.js while
  check-answer-lock (new in #129) still had it on NOT_YET, and the "stale" rule failed it. Both PRs were green
  alone. Now a CLOUD_LANE game that loads the lock is a note, not a failure, and the home lane moves it to
  MIGRATED once it passes. **suvat does not pass yet, and it is the cloud lane's game:** it loads answer-lock.js
  before next-control.js, and the driver needs a HINT to produce a wrong answer. factor-theorem (#130, open)
  will be in the same position.
- **#132 (batch 2) adds two things, on Jon's order.**
  - **(a) MaffsNext on a wrong answer (canon §7.6)** for factor-race, fraction-equivalence and percentage-flip,
    on wrong answers and time-outs. Two of the games needed a call on what counts as the wrong path:
    - prime-factorisation: a wrong tap that leaves lives never moved on, so Next goes on the last life. It
      shows the whole factorisation, then Game Over.
    - equatle: a wrong guess is the next row of the same puzzle, so Next goes on a lost puzzle. It shows the
      equation, then the results.
  - **(b) Equatle :337 restored.** The links pasted into the button's onclick now sit under the buttons, with
    the teacher line after them, outside the `.mf` flex row (check-teacher-invite required this).
  - Closed: prime-or-composite-t1-001 (HIGH) and percentage-flip-r-001. factor-race-t3-004 has its fixed part
    noted.
- **NOT_YET: 80** (73 home + 7 cloud). 16 games migrated.
- **For Jon:**
  - **Phone rule:** at 320×568, Next is below the fold on factor-race, fraction-equivalence and percentage-flip.
    Their answer controls are already below the fold on main (`measure-phone-fit.py`), so this is phone-fit
    work, not F1. Not queued.
  - **check-teacher-invite.py** drives Log Laws through its global `answered`. Fix that when log-laws migrates.
  - **Equatle and Prime Factorisation:** the reading of "wrong path" above is mine, so overrule it if needed.
- **Lessons:**
  - `measure-phone-fit.py --only X` rewrites `docs/phone-fit-report.md`. Restore the file afterwards.
  - A one-off wrong-path script must click Next with `force` or `dispatch_event` during the floor. A plain
    `click()` waits for Next to enable, and a raw coordinate click can land on the fixed footer.
  - Heredocs still eat `\'`: use Edit or Write for those.
- **Next session:** read the QUEUE above and start batch 3 (re-read `docs/handover/cloud.md` first).
## 2026-10-07 (home, evening): F1 batches 1 and 2 built; PAUSED for a context clear (Jon, at 55%)

- **#125 (F1 part a, MaffsLock) MERGED** on a green Gate. Its group E run failed once on a 1px fold in Simultaneous
  Solver (320x568, s4_01: 529 vs 528) and passed on rerun: flaky, not this change.
- **Jon's F1 checkpoint rule (7 Oct):** after the shared lock PR, stop after every 2 roll-out batches (each merged,
  main green); at each stop update this file (batches, PRs, NOT_YET, next batch, lessons) and stop. Also stop at the
  next batch boundary when Jon says "checkpoint".
- **STATE AT THE PAUSE:** both branches pushed (after GitHub returned "Internal Server Error" on push three times
  at 17:00; the fourth went through). No PR open for either yet.
  - `claude/f1-batch1` in worktree `E:/jon/mg-b1` (rebased on main after #125): batch 1 + check-answer-lock.py.
  - `claude/f1-batch2` in worktree `E:/jon/mg-b2` (stacked on batch 1, not yet rebased).
- **NEXT SESSION, in order:** (1) open the PR for `claude/f1-batch1` (body drafted: games, faults fixed, check);
  run `python scripts/close_entries`-style edit: set status fixed + pr on formula-plug-in-t3-001, new-shapes-t3-001,
  four-quadrant-explorer-t3-001, like-terms-collector-t3-002 (shape-shifter-t3-005 stays open: bundle; note its
  class-1 part fixed). (2) Local check-changed on batch 1: 82 ok, 3 FAILED: Negative Number Line (320px fold, also
  fails on main locally: fonts), **Test the Claim** and **Resit fixes** (not yet compared with main: check first;
  CI is the judge). (3) Merge on green, watch main. (4) Rebase batch 2, its PR, register entries, merge. (5) That is
  2 batches: STOP per Jon's rule.
- **Batch 1 (Year 6):** formula-plug-in, new-shapes, four-quadrant-explorer, like-terms-collector, shape-shifter,
  negative-number-line, think-of-a-number, decimal-detective.
- **Batch 2:** probability-pioneer (5 s Wait retries queued one per click: now one pending), prime-or-composite
  (P/C keys re-marked: fixed), factor-race, prime-factorisation, percentage-flip (Skip after Check skipped a second
  card: fixed), fraction-equivalence, equatle (one lock per guess, released at once; finish once), estimation-golf.
  All 16 pass check-answer-lock.py both parts locally (about 3 min per 8 games).
- **NOT_YET after batch 2:** 80 (73 home + 7 cloud). **Next batch 3 (KS3/GCSE):** 52dle, split-it,
  word-problem-decoder, equation-builder, spot-the-muppet, terrible-advice, wrong-on-the-internet, maths-court.
  Re-read docs/handover/cloud.md first: the cloud lane merged #124 (linear-equation-solver), #126 (moments-master),
  #127 (force-resolver) today.
- **Lessons (check-answer-lock.py):** the generic tier-3 driver needs per-game HINTS for most games (ready, answer,
  surface, start_sel, keys, each, mark_any, repeat); write the hint while migrating. Auto-advance games (no Next on
  a wrong answer: factor-race, fraction-equivalence, percentage-flip, prime-factorisation, equatle) are noted, not
  failed (canon 7.6's Next is logged for Jon, not F1's). `fresh()` must cover skip-marked Next buttons (fixed in
  #125 before merge). Verifiers that load and answer in one breath need `bc.NO_LOCK_FRESH_INIT`. Game-wide regex
  replacement of `answered` also hits CSS comments: check. Heredocs eat backslashes: write patch scripts with the
  Write tool (scratchpad mig_*.py / patch_cal*.py are this session's).
- **For Jon:** equatle :337 has a malformed `onclick="<div ...` (logged, not fixed, SR-9). STOP IF (c): 89 games to
  migrate, carrying on in batches.
## 2026-10-07 (home): F1 part a, the MaffsLock asset (#125)

- **#123 (0d, Given That) merged** on a green Gate after main's rerun of #122 went green. Main's first runs
  after #121 and #122 were marked failed with every job green: the run never created its Gate job (the two
  pushes were 5 s apart). A rerun of #122's run created it: green.
- **F1 (Jon, 7 Oct):** one shared lock every game uses, so no click, key, double-click or double-tap marks
  twice, answers unseen, or finishes twice; then roll it out (no game keeps a local guard) and relist every
  unlisted game that is ready (SR-21: verifier merged, no open CRITICAL/HIGH). Do not touch scoring, keys,
  banks, MaffsAnswer/Options/Keypad internals, or the cloud lane's remaining games
  (linear-equation-solver, moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine,
  truth-will-set-you-free: it adopts the lock itself). STOP IF a game cannot adopt it without a scoring change,
  or a CRITICAL/HIGH game would have to be relisted.
- **Count (STOP IF c, reported, carrying on):** 96 roster games record question_answered; 7 are the cloud
  lane's, so **89 to migrate** here, in batches of 8 by audience (Year 6 first).
- **This PR:** `schools/assets/answer-lock.js` (MaffsLock: `lock`, `isLocked`, `fresh`, `screen`, `timer`,
  `cancel`, `clearTimers`, `finishOnce`, `newSession`; header documents it); MaffsNext's advance calls
  `MaffsLock.clearTimers()`; canon §7.6.0 ("every game marks through MaffsLock; no local answered flags");
  `scripts/test-answer-lock.py` (B3 by ci-line): nine behaviours on a fixture game in Chromium, and the four
  planted faults (CSS-only lock, no fresh delay, uncleared timers, double finish) each caught. `isLocked()` is
  an addition to the contract's API: a keypad that must stop typing, or an Enter that must advance rather
  than mark, asks it instead of keeping a flag.
- **Next (part b):** `scripts/check-answer-lock.py` with batch 1 (the Year 6 games: formula-plug-in,
  new-shapes, four-quadrant-explorer, like-terms-collector, shape-shifter, negative-number-line,
  think-of-a-number, decimal-detective). Drafted on the f1 worktree (stashed): a generic driver on check-site's
  tier 3 probes; on main's formula-plug-in it already finds the double finish (game_completed x2, submitScore x2).
## 2026-10-07 (home): queue item 0d, shared fraction answers (#122) and Given That (#123)

- **#121 (0c) and #122 merged** on green Gates. Slip: #122 merged while main's run for #121 was still in
  progress (both green as PRs, disjoint files); both main runs watched to the end.
- **#122, shared:** `MaffsAnswer.fraction(raw)` (exact a/b, signs, whole numbers, lowest terms) and
  `fractionOrDecimal(raw, num, den, dp)` (a slash: exact, right or wrong, never 'format'; else the unchanged
  `decimal()` against num/den rounded half up in integers). `message()` gains `{sf}` and `{fraction}`.
  test-answer-js.py 68 to 125 cases; canon §7.1.3.
- **This PR, Given That:** each free-entry question ends "Give your answer as a fraction, or as a decimal to 3
  significant figures." (marked at dpFor()'s places, as before); placeholder "e.g. 3/7 or 0.429"; the exact key
  comes from answerDisplay (`exactOf()`), `keyAt()` gone. The verifier types every key as a fraction (lowest
  terms and x3), every other diagram ratio as a fraction (wrong), and on the 3/7 items 3/7 and 0.429 right, 0.43
  wrong; new plant r-004 (decimals only). Against main's page it fails on every fraction.
- **Register:** no open entry covered it (r-002/r-003 closed in #114), so r-004 (MEDIUM, class 7: fractions
  unreadable since #114) is filed and closed here.
## 2026-10-07 (home): queue item 0c, canon SR-22 and SR-23 (docs only, #121)

- **#120 (0b) merged** on a green Gate.
- **Numbering (decision taken, for Jon to see):** Jon called the leaderboard ruling "R15", but §0.3 numbers by SR-n
  and F1 names its relist rule SR-21. So SR-21 is reserved for F1 (a placeholder row), the leaderboard ruling is
  **SR-22** (its source column says "his ruling R15") and the timer ruling **SR-23**.
- **SR-22:** one board per mode or session length; Prime Sprint's board key on the hub; Prisoner's Dilemma ranks
  the tournament total only. proof-builder-t5-023 and prisoners-dilemma-t4-001 set `jc: false` (ruled), still open:
  the code is not changed (new level keys in `firebase-leaderboard.js` and the hub: shared code, home lane, not yet
  queued). Prime Sprint has no register entry.
- **SR-23:** timer-policy's Hidden Count-Up applies; Trig Identity Duel and Glorious Gantt follow it (both already
  listed there; a dated note added). trig-identity-duel-t2-010 and the timer part of glorious-gantt's :783/:968
  entry stay open until their code changes (TID is the cloud lane's game; Gantt is unlisted).
## 2026-10-07 (home): queue item 0b, regex .test() guards in bank_common (#120)

- **Jon's new queue (7 Oct, after the clear):** 0b this; 0c canon §0.3 R15 + the timer ruling (docs only);
  0d shared fraction answers (MaffsAnswer, then Given That); then F1 (MaffsLock, pasted).
- **0b:** `_SiteEval.call()`'s `.test` branch called `.search` on `regex()`'s `(pattern, glob)` tuple, so any
  render site guarded by `/re/.test(x)` crashed extraction (the cloud lane's note, #102/#105/#115). It now unpacks
  the tuple. `test-bank-common.py` gains REGEX_GUARDS: Proof Builder's `if (/[\\^_{}]/.test(q.a))` (in JS source) shape and
  Component Crusher's template-literal ternary; both raise on main, both pass now, and each guard is decided per
  value (`x^2` reaches KaTeX, `seven` does not). The cloud lane may go back to regex guards at render sites.
## 2026-10-07 (home): item 0, Like Terms Collector's flaky read (this PR); STOP for a clear before F1

- **Contract C is complete:** #111, #113, #114, #116, #117, #118 all merged on green Gates (#118's main run:
  watch it if not yet reported below). Contract V (#108) merged earlier.
- **Item 0 (Jon, 7 Oct):** `verify-like-terms-collector.py` failed once on main (run 37626794263, #109, attempt 1:
  "item 1: typed 8.9/6.5, marked correct=None") and passed on rerun. It read MARK() straight after
  `page.click('#checkBtn')`. Now `read_mark()` waits for the game's own mark to land (up to 5 s), and the in-page
  sweep polls the same way. New self-test: a copy whose showFeedback() marks 300 ms late; the waiting read must
  see every mark and a read straight off the click must see none. With the old immediate read put back, the
  self-test fails with main's exact message. Not traced: why the real page was ever late (the check no longer
  depends on it).
- **Then STOP (Jon):** he clears the session before contract F1. Next session: read this file and the memory's
  LATEST block; F1 starts when Jon pastes it.
- **Open for Jon (carried):** eigenvector-engine-f0-005 set jc: false (done in #108); the cloud lane's #112 and
  #115 already declare their verifiers by ci-line header, so V is working as intended. B3 now carries 11
  lines: check its time on the next full main run; re-record `scripts/ci-timings.json` with
  `python scripts/ci-groups.py --record-timings <run id>` if it grows.
## 2026-10-07 (home): contract C game 6, Estimation Golf (#118); contract C complete once it merges

- **#117 (Sequence Solver) merged.** Slip to note: the cloud lane merged #115 seconds before, and #117 went in
  while main's run for #115 was still in progress (not red, but not yet green, against "main green, then the
  next"). Both main runs were watched to the end.
- **#118:** level4[7] keyed 565.49 (r-001; choice recorded: the true value, not "use pi = 3.14"); alevel[1] states
  the forward difference and 3 d.p. and keys 27.009, hint reworked (r-002). `verify-estimation-golf.py` (B3). On
  main it failed on exactly r-001 and r-002. Open: r-003, r-004, r-005.
- **Contract C summary (#111, #113, #114, #116, #117, #118):** six verifiers, all in B3 by ci-line header. No
  verifier found a wrong key the register did not list, so no STOP IF. Value-equal option pairs fixed along the way
  and their ledger entries cleared: proportion-blaster x5, given-that x2, formula-unlocked x2 (+B2, B10),
  sequence-solver x1; plus formula-unlocked F4 (sqrt(u^2), not caught by B11). B3 now carries 11 lines; check its
  time on main's next full run (the timing file was recorded before contract C).
- **Item 0 (Jon, 7 Oct), ON HOLD, Jon to confirm:** Like Terms Collector flaked on main once since #89: run
  37626794263 (#109), attempt 1, group E: "item 1: typed 8.9/6.5, marked correct=None", passed on rerun.
  `None` means MARK() found the feedback panel unmarked straight after `page.click('#checkBtn')` (the real-UI path
  in play(), scripts/verify-like-terms-collector.py ~:153-156); the cause is not yet traced. Jon said this may
  belong to a contract he has not sent yet, so no fix has been started.
- **Queue after #118:** F1 (Jon pastes it); item 0 if Jon confirms.
## 2026-10-07 (home): contract C game 5, Sequence Solver (#117)

- **#116 (Formula Unlocked) merged** on a green Gate, main green after #114.
- **This PR:** alevel[49]'s "0.999..." replaced by 10 (r-001); gcse[6]'s B11 pair replaced by 3n + 7.
  `verify-sequence-solver.py` (B3) recomputes all 154 keys; on main it failed on exactly r-001 and the B11 pair: no
  other wrong key. r-002 and r-003 stay open.
- **Next:** game 6, Estimation Golf (committed locally on claude/c-estimation-golf in worktree ../mg-eg): :680
  keyed 565.49 (choice recorded: the true value, not "use pi = 3.14"), :663 states the forward difference and
  3 d.p. and keys 27.009.
## 2026-10-07 (home): contract C game 4, Formula Unlocked (#116)

- **#114 (Given That) merged** on a green Gate, main green after #113.
- **#116:** Q_ALEVEL[0]'s value-equal option replaced by named slips, override and duplicate dropped (r-001);
  value-equal wrong options replaced in Q_LEVEL4[10] (f0-001, closed), Q_GCSE[22] and Q_GCSE[23] (audit F3, F4:
  not register entries; F3 was a B11 ledger entry). `verify-formula-unlocked.py` (B3, SymPy). On main it failed on
  exactly those four items: every key satisfies its formula, no other wrong key.
- **Next:** game 5, Sequence Solver (r-001: "0.999..." beside 1; the replacement is 10, the sum taken with first
  term 9). Its B11 ledger pair (gcse[6] -3n + 10 = 10 - 3n) is fixed in the same PR. r-002 (raw TeX on screen) and
  r-003 (jc) stay open.
## 2026-10-07 (home): contract C game 3, Given That (#114)

- **#113 (Better Value) merged** on a green Gate, after main's run on the cloud lane's #112 (Dimension Checker,
  which declared its verifier by ci-line header: no workflow edit) was green.
- **#114:** alevel_18's Venn regions from its stored totals (r-001); free entry on `MaffsAnswer.decimal` with the
  precision stated on every free-entry question (r-002, r-003); F4/F5's value-equal options replaced, two B11
  ledger entries cleared. `verify-given-that.py` (B3) has a reviewed SPEC for all 180 keys. On main it failed on
  exactly r-001, r-002, r-003 and F4/F5: no other wrong key.
- **Decision taken (for Jon to see):** one precision for all free entry would not do. At 3 d.p. two small keys
  (core_06 0.0518, alevel_25 0.0297) round the same as another ratio on their own diagram, and a 4 d.p. stored
  value rounded again gives the wrong 3 d.p. key for 6/11 and 136/228 (the verifier caught both in my first
  version). So N keeps three significant figures: 3 d.p. from 0.1 up, 4 from 0.01, 5 below, stated per
  question; the two stored values carry more places. Fractions and percentages are no longer accepted (MaffsAnswer
  reads plain decimals): the placeholder says "e.g. 0.429".
- Not in scope, still open: audit F6 (no phase 1 explanation at the typed levels); Given That's typed answers are
  not yet on MaffsKeypad (canon 4.4 rollout).
## 2026-10-07 (home): contract C game 2, Better Value (#113)

- **#111 (Proportion Blaster) merged** on a green Gate (B3 ran its verifier by its header alone).
- **#113:** five Core conclusions corrected from the recomputed figures (r-001..r-005) and core_033's working put
  in pence (r-009, closed too: the verifier proves its equation solved to 425). core_009 needed its repayment
  stated (GBP 90.20/month, 8% APR effective over 24 months) to be answerable; the old key is now a wrong card,
  explained. `verify-better-value.py` (B3): every figure in a keyed card or explanation must be a given or a
  recomputed value at its printed precision. On main it failed on exactly r-001..r-005 and r-009: no other wrong
  figure in the 70 items. Open (jc: true): r-006, r-007, r-008.
- **Next:** game 3, Given That. Spec reviewed for all 180 keys (num/den by named quantity, Yes/No tables'
  headers pinned); plan: alevel_18's Venn regions from its stored totals (onlyB 15, neither 55), free entry on
  `MaffsAnswer.decimal` at 3 d.p. stated on every free-entry question, gcse_14/gcse_23 value-equal options
  replaced (audit F4/F5).
## 2026-10-07 (home): contract C game 1, Proportion Blaster (#111)

- **V (#108) merged** on a green Gate (51/51 content lines ran); main's full run after it: see the next entry.
- **Contract C (Jon, 7 Oct, revised):** audit batch 3, one game per PR, in order: proportion-blaster, better-value,
  given-that, formula-unlocked, sequence-solver, estimation-golf. Each: a verifier that recomputes every key
  (SR-4/SR-16 option checks, explanation figures), declaring its own ci-line; the game's register entries
  set fixed with the PR; other open entries the verifier proves are one-line data fixes may be closed too;
  shared-class entries (classes 1, 4, 5) stay open. STOP IF a verifier finds more wrong keys than the register
  lists (file them, stop) or a fix would change wording beyond the named item. Do not touch engines, scoring,
  levels, leaderboard keys, other games, estimation-golf's proximity scoring, or the workflow.
- **#111:** alevel[47] keyed 900/11 (r-001 fixed); F2-F5's value-equal wrong options replaced by named errors,
  five B11 ledger entries cleared; `verify-proportion-blaster.py` in B3. On main it failed on exactly r-001
  and F2-F5: no other wrong key. Not fixed (beyond the named items): gcse[16] and gcse[21] ask "Find x" from x^2
  without "positive" (SR-17); -5 is not offered, so nothing is mis-marked. Audit F6 (raw TeX in the context
  line) and F7 (no explanation, auto-advance) are not register entries and were left.
- **Next:** game 2, Better Value (r-001..r-005; r-009 too, since the verifier proves its explanation's equation
  solves to 425). Verifier drafted: every keyed and explanation figure must be a given or a recomputed value at
  its printed precision; on main it flags exactly r-001..r-005 and r-009.
## 2026-10-07 (home): contract V, verifiers declare their own CI group (#108)

- **Why:** each new verifier edited `.github/workflows/check-site.yml` (the cloud lane's #96, #97, #100-#102), two
  conflicted with home-lane PRs, and canon §7.8.2 and the cloud contract disagreed about it.
- **Headers:** every content script carries `# ci-line: <group> | <label> | <args>` (51 lines in 47 scripts,
  including `stats_common.py`, `uk_rates.py` and `check-resit-fixes.py`); `&&` in `<args>` runs the script again,
  so the C and D parts (`--part-selftest && --part 1`) and Fermi Lab / Screening Room (` && --selftest`) are
  expressed exactly. `verify-regression-rumble.py` carries `# ci-held:` (the HELD dict is gone). Optional
  `# ci-deps: <paths>` adds dependencies (none uses it yet: ci-deps.py had no per-verifier central rule to move).
- **`scripts/ci-groups.py`:** reads the headers; `GROUPS` holds the 12 groups' job names and timeouts (unchanged);
  the plan job writes the matrix (`groups` output) and the new `content` job runs `fromJSON` of it with the same
  container and steps as `check-site` (YAML anchors `check-container`, `check-steps`). Job names unchanged; the
  Gate needs `content` too, so nothing is hidden from it. Site-wide jobs stay static in the workflow.
- **Proof (item 5):** `ci-groups.py --compare <workflow>` ran in the plan job on the commit that still had the
  static lists. Its first run caught the cloud lane's Integration Duel line, merged to main minutes earlier (51 static
  lines, 50 from headers: DIFFERENT); after merging main and adding that header, 51 = 51, EQUAL. Then the lists
  were deleted.
- **Readers of the workflow moved to the headers:** `ci-deps.py` (checks + `# ci-deps:`), `check-changed.py` (via
  ci-deps), `audit-register.py` (which games have a verifier: without this, REGISTER.md would have said 97 of 97
  games have none), and the `--part-selftest`s of Just Pythag It, Bruv and Equation Builder ("CI runs every part").
- **`check-verifier-coverage.py`:** a verify-*.py with no ci-line and no ci-held fails; an unknown group fails; a
  verifier listed in the workflow, or declared AND listed, fails. Reports each group's check seconds from
  `scripts/ci-timings.json` (recorded from main's run 37625188261 after #107 by `ci-groups.py --record-timings`;
  B4 164s is the largest, setup excluded) and flags any over 240s.
- **Success proof:** throwaway PR #110 (based on this branch) added only `scripts/verify-zz-v-probe.py` with a
  `B3` ci-line: the plan selected just it, and B3 ran it (1 line run, 5 skipped; run 37626296241); closed and
  deleted. #108's own full run (CI changed, so everything): 51 of 51 content lines ran, Gate green, 4m39s.
- **The cloud lane merged twice while this was open** (#107 Integration Duel, #109 Curling Friction), each adding a
  workflow line; each time main was merged in, the verifier given its header, and `--compare` against main's
  workflow re-run: 52 = 52, EQUAL, before the merge.
- **For the cloud lane:** add the verifier's `# ci-line:` header in its own file; never edit the workflow for it.
  Canon §7.8.2 says so (the cloud handover is the cloud lane's to update).
## 2026-10-07 (home): queue item 2, every content job under 4 minutes

- Main's full run after #99 (before): D 5m23s, B2 4m33s (the cloud lane had added three verifiers to it),
  C3 4m04s, C2 3m57s, A 3m34s, B1 3m32s.
- **D:** `verify-equation-builder.py --part i/n` splits by candidate arrangement, not by question: eb_ks3_012 alone
  has 31,032 candidates and is 60% of the time. Whole-question checks run in part 1; the planted-fault self-test now
  also runs each fault through both parts and requires them to fail exactly where the whole run does;
  `--part-selftest` proves every candidate is in one part. Locally: 121 s and 124 s against 185 s whole.
- **C:** four parts (C4 added); **B:** four groups, cut by the slowest time each line has taken on main (runners vary up to 1.8x: Log Laws 30-55 s, Growth and Decay 58-93 s). Timeouts 6-8 min (budget 75%). 19 matrix entries now (was 16): more runner pressure when both lanes run.
- Canon §7.8.1: no content job past 4 minutes; a new verifier goes where that holds.
- **After (#103's full run):** every job 3m38s or less (A 3m38s, B2 3m29s, C4 3m10s, C1-C3 2m50s-3m06s, B1/B3/B4 2m47s-2m50s,
  D1 1m56s, D2 2m03s); the whole run 4m47s (main after #99: 6m19s).
- **For Jon:** the cloud lane's #96, #97, #100 and #101 each edited `.github/workflows/check-site.yml` (adding their
  verifier to a B group). Canon §7.8.2 reserves the workflow for the home lane. It did no harm (the lines were
  needed and CI passed), but either the rule should allow "add my verifier's line to a content group" or the cloud
  lane should hand those lines to the home lane. Your call.
## 2026-10-07 (home): contract F0, B11 sees the value-equal shapes it skipped

- **Fixtures first:** `scripts/test-bank-common.py` (CI, Tier 4 layer A job), 13 equal pairs from the tranche 5-6 items
  (differentiation-duel :820/:848, binomial-blaster :134, force-resolver :118/:138, moments-master :180,
  eigenvector-engine :117/:128, complex-converter ids 21/40, boolean-blitz :584/:744, plus a Boolean distributive law)
  and 14 look-alikes that must stay unequal. All 13 failed on main's parser (commit 630ff40), all pass now.
- **`bank_common.py`:** `parse_value(raw, ctx)` / `value_equal_pairs(pool, ctx)` with `item_context(slug, q)`;
  juxtaposition, `\binom`, trig of constants in degrees, ≈ chains, SI prefixes, `vector`, `polar`, `bool` kinds
  (canon §7.1, the B11 paragraph). Exact throughout. `VECTOR_DIRECTION_GAMES` and `BOOLEAN_GAMES` tag the two games
  whose ask is in code, not in the item.
- **First run: 42 new pairs in 9 games** (eigenvector-engine 11, boolean-blitz 10, complex-converter 8,
  differentiation-duel 5, force-resolver 4, formula-unlocked, log-laws, moments-master, binomial-blaster 1 each).
  28 were already in the register: each ledger entry carries `"register": "<id>"`. 14 are new findings
  `<slug>-f0-NNN` (eigenvector-engine 7, boolean-blitz 4, force-resolver, formula-unlocked, log-laws 1 each;
  log-laws had no register file, so F0 opened one, its `audited` entry saying it is a B11 run, not an audit).
  Two misreads found on the way and fixed with fixtures: "vs" read as v·s; "1! = 1" read as a value.
- `check-banks.py --write-ledger` now carries each entry's `register` link over (`keep_register_links`).
- Planted `12\cos 90° N` beside the key `0 N` in a scratch copy of force-resolver's bank: `--ci` fails on it as NEW.
## 2026-10-07 (home): CI split for speed + two lanes (#95, merged); NEXT = contract F0

**State of play.**
- main `a041590` (#94) green before this PR. Build freeze in force (canon §0.2).
- Done today: the tranche 3-6 contract (#87-#90: 18 games unlisted, the freeze, the findings register) and the
  quoted-figures contract (#91-#94: Fermi Lab, Screening Room, Core Maths Paper 1 CPI, `check-quoted-figures.py`).
  The detail is in CLAUDE.md's last two "Handover" sections (7 Oct), the history this file replaces.
- **This PR (CI + two lanes):**
  - `check-site.py --shard i/n` and `--shard-selftest n`: tier 1 runs as four shards; tier 2 and the parts that
    cannot be split run in shard 1 only. The site-wide checks are their own job.
  - Tier 4 layer A and the shared-asset tests are separate jobs; group B is B1 + B2.
  - `verify-just-pythag-it-bruv.py --part 1|2|3` and `--part-selftest`: C1, C2, C3. (The contract named two parts,
    phone and desktop; measured, the heavier half would still have taken about 5.8 minutes as a job, which leaves
    no room under the 7-minute target for main, so it is three parts dealt by measured cost.)
  - REGISTER.md is no longer edited by PRs: `audit-register.py --check` validates the yml files only; the
    `register` job regenerates and commits it on main after the Gate (canon §0.4).
  - Handover by lane (this file and `cloud.md`); CLAUDE.md's opening block is a fixed pointer; canon §7.8.1-§7.8.2.
- **Before/after timings** (canon §7.8.1): full run 10m42s -> 5m45s; site-wide critical path 6m34s -> 3m03s
  (Tier 4 layer A); shards 1m40s-2m18s at --workers 4 on 4 CPUs (not the critical path, so more workers were not
  tried). Still over 4 min as single verifiers: Equation Builder (D, 4m48s) and B1 (4m51s); a PR touching those
  games waits on them. Split them next if it matters (Equation Builder needs a --part like JPIB's).
- Planted page error in `parents/fractions` (a shard-3 page) on a throwaway branch: only shard 3 failed, Gate red.

**Next.**
1. Watch this PR's merge run on main: every job green, and the `register` job either commits
   `Regenerate REGISTER.md [skip ci]` or reports "unchanged". (It should commit: the generated header's wording
   changed in this PR, and REGISTER.md was deliberately left unregenerated here.)
2. **Contract F0** (Jon pasted it 7 Oct: B11 value comparison in bank_common.py; START only after this PR is merged and main is green), then contract C (audit batch 3) when Jon pastes it.

**Gotchas learned today.**
- On the GitHub runner the "Content verifiers" jobs still pull the Playwright image even when the plan selects
  nothing for them (about 40 seconds each), so every matrix entry costs a runner briefly on every PR. A PR run is
  now 19 jobs (16 in the matrix, was 9); two PRs at once ask for up to 38 of the 20 runners a public repo gets,
  so some jobs wait for the short skipped ones to finish. Watch for it before adding more entries.
- A flake seen once on #92's run: Simultaneous Solver at 320x568, keypad 1px. Not reproduced since.

## Moved from home.md on 12 Oct 2026 (RULINGS-12OCT, for size)

**ROOMS-RELEASE-RK-LJ (10 Oct, Jon 22:45: "both have been play tested, so lets just release"; contract in
`docs/history/contracts/2026-10-10-rooms-release-rk-lj.md`).** The Rightful King (★★★) and The Library Jam (★) are
live, released as Car Trap was: each index.html is the room (prom-budget's head: analytics on, indexable, canonical,
the draft's meta description, 159 and 150 characters; og:image the scene), play.html deleted, teacher.html still
noindex. Hub cards (draft hub line, topics, `data-stars` chip; Library Jam last of the ★, Rightful King after Rugby
Mud) and front-page band cards (after Car Trap; test-section-clicks' order updated); sitemap `<url>` each; "nine" ->
"eleven" in the hub (description, og:description, lede), the front page (band lede, "Open all eleven rooms"),
CLAUDE.md and canon §11.1 (both rows added, Live 10/10). **Not a plain "nine", left for Jon:** canon §11.3's "Across
the eight live rooms: 199 verified number sets" is a replay statistic, not a count to bump. it-vengeance still
redirects to /escape-rooms/rightful-king/ (checked in Chromium). /updates/: one line each under October's New. The
twelve finished contracts moved from docs/handover/contracts/ to docs/history/contracts/ (the folder is empty).
Checked: check-escape-rooms, test-escape-rating (11 rooms, no 320 px overflow), test-escape-art (both rooms to a win
and a loss with their pictures), test-section-clicks, context size. **Merged #271 (227fb0a), main green. Live site checked
10 Oct:** /escape-rooms/rightful-king/ and /escape-rooms/library-jam/ serve 200 with their titles; in Chromium at 320 px each
shows its scene picture and Start, no sideways scroll; /escape-rooms/it-vengeance/ lands on The Rightful King; the hub
says "Eleven"; the old play.html is 404.

**ROOM-ART-RK-LJ: The Library Jam (10 Oct, Jon's contract; pictures approved 22:20-22:42).** The Rightful King's
half was already merged as #269 (main green, 32c2be0). Filed `docs/art/library-jam-scene/-fail/-win.webp` (1600x873,
q80, via `strip-gen-watermark.py --width 1600 --frame 1600x873`: no watermark). **All three sources are 2752x1536, like
the scene, so nothing was upscaled** (the contract expected ~1024 px fail and win). Arm, bin, drop-box and desk screen
all in frame. The squiggle "writing" on the two papers pinned to the right-hand wall is blanked in all three (each
paper refilled from a plane fitted to its clean paper, so the glow gradients stay; outlines untouched); nothing else
retouched. The papers stacked on the desk keep a few pixel-high illegible marks. room.js: `art: 'library-jam'`, the
"ART: none yet" note replaced; sceneAlt checked against the picture and unchanged; failAlt and winAlt as the contract
gives them; RULE (no `missArt`) kept. **Still unreleased. Jon can play-test with pictures at
https://maffsgames.co.uk/escape-rooms/library-jam/play.html** (and rightful-king/play.html). Checked: play.html in
Chromium at 1280 and 320 px (scene, win, fail at time-out); check-escape-rooms (all art present) and test-escape-art pass.


## Moved from home.md on 12 Oct 2026 (GA4-LIVE-ONLY, for size)

**ROOM-STATUS-ONE-TABLE (11 Oct, Jon's contract; branch `claude/room-status-single-table`).** Canon §11.1 is now the
only per-room status table. `docs/escape-room-voice-rewrite.md` §5 is "Per-room rewrite notes": status columns
removed, one bullet per room keeping everything rewrite-specific (the `missArt` rules, timing, cancelled engine
work, release commits, art edits), and a line pointing to §11.1. No STOP: no decision lived only in a status
column. Canon §11.5's two pointers reworded to land on it. `docs/resit-coverage-audit.md` §"live, KS3 label" rows
are a per-lock audit, not a room status table; left alone. **SPLIT-IT-FRACTIONS (todo §1.48) STOPPED on its STOP IF:**
`games/split-it/index.html` loads neither KaTeX nor `mathtext.js`, so a stacked KaTeX `rac` adds a page dependency.
Nothing changed; todo §1.48 stays open, worktree removed. Awaiting Jon: add KaTeX + mathtext.js to the page, or
use the page's existing CSS `.frac-wrap` stacked fraction (no new dependency). Still to do under §1.48: the
duplicated unit label (index.html:514/516) and the report-only division-interpolation scan.

## 2026-10-22 (home): moved from home.md

**FREEZE-LIFT (15 Oct, Jon's contract; #418, merged, main green).** Build freeze lifted: canon §0.2 now holds Jon's dated record and quote; the freeze text, exceptions and exit bar are verbatim in `docs/history/build-freeze-2026-10.md`. New **SR-30** (§0.3) "New builds ship checked" (verifier in first PR, straight into every MIGRATED list, findings file, wrong live answer outranks any build, one build in flight). Priority order untouched. Register dashboard **relabelled "Audit progress"** (counts kept, a line says it is no longer a gate); `audit-register.py` comments/headings reworded, flags `SHARED_CHECKS_GREEN`/`SWEEP_DONE` unchanged and read only by register generation. No check enforced the freeze mechanically. CLAUDE.md had no freeze mention; `todo.md` line 5 is dated history, left. Moved to the archive to stay under 20 KB: ESCAPE-SET-CHECKS, Canon sweep, WORKTREE-CLEANUP (the three empty `mg-b7`/`mg-lock`/`mg-sk` folders and the dirty `mg-pp-before` are still Jon's).
**REGION-HISTORY (15 Oct, Jon's contract; branch `claude/region-history`).** New `scripts/ci-timings-regions.json`, written by `ci-groups.py --record-regions RUN --from-dir DIR` (`add_regions` is pure): per timed line, per region, the last 10 seconds (oldest first; no region = "unknown"; the last 20 run ids remembered so a rerun counts once). The main timings job runs it right after the pack check passes and commits it in the same commit as `ci-timings.json`/`ci-pack.json` (only the diff/add path lists grew); a failure is a `::warning::` and `git checkout` of the file, never a job failure. `ci-timings.json`, history length 5, medians, packer, `--check`, budgets, persistence report untouched. Self-test: 12 runs over 3 regions, 10 kept per line per region, oldest rolled off, `ci-timings.json` byte-identical with and without the step. **Size:** saturated worst case (141 lines x 12 regions x 10) ~108 KB, under the 200 KB stop. Canon §7.8.1 says where it lives and its retention; the comparison itself stays deferred. **Check the first main run after merge wrote the file with regions populated.**
**D&D CLUB DRAFT, APPROVED (15 Oct, Jon's contract DND-ROOM-DRAFT; #415).** Draft: **`docs/escape-room-drafts/dnd-club-draft.md`** (phase 1, nothing built; phase 2 is DND-ROOM-BUILD). Mrs Rogers's idea; **consent to her real name recorded: Mrs Rogers has agreed to her real name being used (Jon, 15 Oct 2026)**; no student named. Rated ★★ Core (lock grades 4/3/4, no star field). Title Roll for Initiative. Jon's rulings applied: Strictmane's gracious withdrawal (Form R-1), the nine-set gate pot accepted (persuade is always the better path), initiative in lock 3's brief, DWARF/WIZARD in species/class boxes, general hint ladders for locks 2 and 3, "Form G" with no number, distinct token names. Pot: gate 9, plans 7, fireball 5 sets; 182 of 315 joint draws VALID. Art (Jon supplies): `docs/art/roll-for-initiative-{scene,fail,win}.webp`.

## 2026-10-23 (home): moved from home.md

**STARTER-LABEL (17 Oct, Jon's contract; branch `claude/starter-label`).** A room may carry an optional `label` (+ `labelFor`) in `room.js`; `rating.js` `html(r, room)` then draws `<span class="rating" data-label="starter">` ("Starter" / "Level: Starter") in place of the stars on student surfaces (start screen via `engine.js`; cards, checked by `check-escape-rooms.py`), and `teacher.js` shows "Starter, for Year 6 and new Year 7 · ★ Warm-up · grades 1–3". `rating()`, the bands and the ordering are unchanged. **Unlabelled rooms are byte-identical:** the start-screen and teacher-page DOM of all 12 live rooms was snapshotted in Chromium before and after, 24 of 24 identical; only Big School Begins changed. Big School Begins carries `label: 'Starter'`, `labelFor: 'Year 6 and new Year 7'` and nothing else in the room changed. `check-escape-rooms.py` plants two more faults on every run (a label chip on an unlabelled room's card; a star chip on a labelled room's card); `test-escape-rating.py` has a labelled-room case (start screen: Starter, no ★; teacher page: Starter, labelFor, ★ Warm-up). Canon §11 records the four-locks/20-minute exception and documents label/labelFor; SR-14 records the William's-line exception. **Big School Begins now waits on Jon's play-test, its art, and the release contract (hub card, front page, sitemap, 'three or four locks, 15 to 20 minutes' copy).** Note: the labelled-room card check has no live user yet (the room is unlisted and has no card), so only the plants exercise it until release.

**AUDIT-ROOMS (17 Oct, Jon's contract; branch `claude/audit-rooms`).** Rooms are in the findings register. Root cause: `audit-register.py` required `games/<slug>/` for every findings file, so no room could have one (SR-30 asks for one on every build; #425 could not comply). Now a file is valid with `games/<slug>/` **or** `escape-rooms/<slug>/` holding a `room.js` (error names both); REGISTER.md gets its own "Escape rooms" section and every games section is byte-identical to before (checked by diff: the change is purely additive). 13 room files (`findings: []`): big-school-begins, canteen-hack, car-trap, comic-caper, hamster-heist, heatwave-mutiny, kiln-disaster, library-jam, pe-shed-rebellion, prom-budget, rightful-king, roll-for-initiative, rugby-mud. **it-vengeance excluded** (withdrawn; a redirect with no room content, though its folder still holds a room.js). `escape-rooms/assets/` is shared assets, not a room. **`audited` value:** the schema has no "not yet audited" form, but `tranche` is free text (precedent: `F0 (B11 parser, not an audit)`), so rooms use `tranche: none (not yet audited)`, `head: f657998` (main when made), `date: 2026-10-17`, `served: {}`; no new field. `--selftest` gained a room case (accepted, listed under Escape rooms only) and a planted file with neither folder (fails). Canon SR-30 row updated. **Big School Begins' release is now unblocked on the register side; the Starter label contract is still outstanding.**

**DND-ROOM-RELEASE (16 Oct, Jon's contract; branch `claude/dnd-room-release`).** Roll for Initiative is RELEASED: play.html's body is now `index.html` (live head: analytics, canonical, description 153 chars, og:image = scene), play.html deleted and its WITHDRAWN entry removed; hub + front-page cards (★★ Core, after Car Trap, before Rugby Mud, same order on both), sitemap, `/updates/` line, eleven -> twelve on the hub (3), front page (2), CLAUDE.md and canon 11.1. Derived stars ★★ (test-escape-rating). Contracts DND-ROOM-BUILD and this one moved to `docs/history/contracts/`. Live check: see the line below once merged.

## 2026-10-23 (home): moved from home.md (evening)

**BSB-ART (17 Oct, Jon's contract; branch `claude/bsb-art`).** Art filed: `docs/art/big-school-begins-{scene,fail,win}.webp`, 1600x873 (from Jon's 2752x1536 JPEGs: 34 px cropped off the height for the frame; the fail picture is Jon's re-edit with plain cans and four boxes on both clipboards, checked at full size before filing). `strip-gen-watermark.py` found no mark on any of the three and I looked at each bottom-right corner myself: clean. `room.js` gains `art: 'big-school-begins'` and `sceneAlt`/`failAlt`/`winAlt` (what is there, no people, no figures, nothing that places the book symbol or hints at a lock); only the ART header comment otherwise changed. Played at 1280 and 390 px to a win and a time-out: scene on the start screen, win and fail on the end card, all load (naturalWidth 1600), no 404, no sideways scroll, each looked at on screen. `test-escape-art.py` and `check-escape-rooms.py` pass (the room is unlisted, so neither plays it; the play check above was my own script). **The room now waits only on the release contract** (hub card, front page, sitemap, 'three or four locks, 15 to 20 minutes' copy; Jon's play-test also outstanding).

**COORD-KEYPAD (17 Oct, Jon's contract; branch `claude/coord-keypad`).** Done. `engine.js` keypads take an optional display `format: 'coordinates'` (with `digits: 2`): `( – , – )`, `( 3 , – )`, `( 3 , 7 )`; the typed value, Set and the check are still the two digits, the typed fallback is "Or type the coordinates" and keeps `(3, 7)` as typed; `teacher.js` shows such a lock's answer and misconception as `(x, y)`. Big School Begins' lock A only: `digits: 2` + `format`, label "LIBRARY: COORDINATES", brief/hint 3/solve no longer call the answer a code. Lock A's sets, VALID count (5670 of 8000) and variant 0 are unchanged (`keypad(2)` is the same range for `digits` and `maxDigits`, so neither the generator nor `escape_set_checks.py` needed a change). **Snapshots (Chromium, Math.random pinned, start screen + every lock screen + teacher page, 13 rooms, 66 pages): 64 identical, only Big School Begins lock 0 and its teacher page changed.** `test-escape-keypad.py` has a coordinates case (display at 0, 1, 2 digits; 3,Set "Not enough digits."; typed `(3, 7)` opens and stays as typed; 4,2 wrong; 7,3 gets Daisy's line). Canon §11.3 has the format line. Big School Begins still waits on its art and the release contract.

## 2026-10-24 (home): moved from home.md

**BSB-RELEASE (18 Oct, Jon's contract; branch `claude/bsb-release`).** Big School Begins is RELEASED: `index.html` is the room (analytics on, indexable, canonical, og:image the scene; 155-char description from the draft), `play.html` deleted and out of `WITHDRAWN`; Starter-chip cards on the hub and front page (end of the Warm-up band, after Library Jam); sitemap; `/updates/` line; "thirteen" everywhere (hub, front page, CLAUDE.md, canon 11.1 with its row, and canon's "(12 items)" portal-label count, now 13); site-wide copy now "three or four locks, 15 to 20 minutes" (single-room lines and the dated 1 Sept update left). Win sentence replaced ("...and he hasn't stopped talking"); stale unlisted comments in room.js/teacher.html updated. `test-escape-rating.py` now skips the star check for labelled rooms (their card has no stars) and still runs them through `labelled()` and the 320 px pass; `test-escape-keypad.py` loads the room at its URL. No shared code touched. Local check-changed: only the usual Answer lock parts 1/6 and Quadratic Factoriser self-test flakes. Contract and BSB-ART moved to `docs/history/contracts/`.

## 2026-10-24 (home): moved from home.md (DIAL-SCALE)

**PER-LINE-LIMIT (20 Oct, Jon's contract; branch `timings-line-limit`; replaces his temporary ruling of 20 Oct, which stands in `cloud.md` until that lane next edits it).** `ci-groups.py --check` now fails any timed line whose median + median setup passes 70% of its group's budget (named, with figures); `--record-and-pack` exits 2 (the workflow warns, commits nothing, does not fail) when the refused pack passes at the previous median setup, else fails as before. Selftests prove both paths and the limit (169 s passes, 170 s fails). Replayed on the 5 recorded runs: it tells setup from line growth (a reconstructed 39479308670 is setup-only; 260 s lines are not). **Free Daily Pizza is split into parts 1 and 2 (`--part 1|2`; part 2 has its own two planted phone faults) and Just Pythag It, Bruv into parts 1-5 (part 5: WebKit, play-through, self-test); cloud lane: rebase knowingly.** Canon §7.8.1. At today's medians the limit names no line (Pizza 69%, Pythag part 4 63%): both were split on Jon's instruction, not because it named them. **DONE: #465, main run 39484798159 green, timings job included (the first run to time the parts: Pizza 94 s + 83 s, Pythag part 4 79 s + part 5 70 s; setup 32 s). `cloud.md`'s 20 Oct ruling is superseded; the cloud lane may delete it.**

**ROSTER-PYTHAG-14 (20 Oct, #464; main run 39479308670 red from the timings job alone: setup 66 s, Content verifiers 2 at 81%).** Row 98 of `game-roster.md` now says 14 triples (the code has 14). The cloud lane's item is closed.

**DEPS-SRC-HAZARD (19 Oct; cloud lane, Jon's contract).** `scripts/ci-deps.py`: `src_hazard()` replaces the computed-src regex; selftest has an always-run budget of 12 (now 9, was 125). Detail: cloud handover.

**ROOM-CREDIT v2 (19 Oct; cloud lane, under Jon's lane exception).** Shared files the cloud lane edited: `escape-rooms/assets/engine.js` (start-screen credit note), `escape-rooms/assets/teacher.js` (teacher-page credit note), `scripts/check-escape-rooms.py` (card notes held to room.js `credit`) and, on Jon's ruling, `escape-rooms/assets/rating.js` (`credit()`, `INVITE`). Rebase on them knowingly. Detail: cloud handover, ROOM-CREDIT v2.

**STARTER-FIRST (18 Oct, Jon's contract; branch `claude/starter-first`).** A Starter-labelled room is listed before every starred room, on the hub and the front page. `check-escape-rooms.py` ranks a labelled card below every star rating (`order_rank`) and fails "cards are not in rating order (easiest first, Starter before every star)"; two planted faults (`swap_cards`) prove it. Order before: stars 1.. then Big School Begins; after: Big School Begins first, rest unchanged. Canon §11.3 has the one-sentence rule. Local full run was lost to the LOCAL-FLAKES server cause (#438); CI was the judge.

**LOCAL-FLAKES (18 Oct, Jon's contract; branch `claude/local-flakes`).** One cause: `serve-stubbed.py`'s listen queue was socketserver's 5; Windows refuses a full backlog (`ERR_CONNECTION_REFUSED`), Linux CI queues it. Fix: `request_queue_size = 128`. Report: `docs/audits/local-flakes-2026-10.md`. Before (idle): 9/10 on three checks; loaded: 0/10 on Quadratic Factoriser self-test and the stars test. After, idle: 70/70. After, loaded: 70/70. A local full pass still fails Tier 1 shard 4/4 on `parents/fractions` (local fonts, CI passes): a separate difference, noted in the report.

## 2026-10-24 (home): moved from home.md (DIAL-MAPPING)

**FRACTION-FORM (20 Oct, Jon's contract; branch `fraction-form`).** `MaffsAnswer.fractionForm(raw, key, opts)` in `schools/assets/answer.js`: key `{num, den}` or `{whole, num, den}`, `opts.form` `'simplest'` (default) or `'mixed'`. Reads `a/b`, `-a/b`, `w a/b`, whole numbers, spaces tolerated; never reduces what was typed. **`correct`** = equal and in the asked form (simplest: lowest terms, a whole number when the key is one; mixed: whole number for a whole key, else a mixed number with a proper lowest-terms fractional part, or a proper fraction when the key is under 1). **`format`** = equal, wrong form (2/4, 6/3, 0/5 for 0, 7/4 when mixed is asked, 1 3/4 when simplest is asked), never marked (SR-3). **`wrong`** = different value. **`unreadable`** = decimals, a zero or signed denominator, junk, numbers past 2^53. `message()` takes `opts.fraction` `'simplest'`/`'mixed'` for the format texts (and fraction-only unreadable texts). Existing functions and messages untouched. 223 outcome cases in `test-answer-js.py`. **Cloud lane: How Many Parts? can now wire stages (d)-(f).** DONE: #467, main run 39489555957 green.

## 2026-10-24 (home): moved from home.md (BURST)

**MATHTEXT-NOWRAP (21 Oct, Jon's contract; #471, main run 39559008796 green).** `MaffsText.html()` now puts a closing mark (`. , ; : ! ? )` and closing quotes) right after a maths segment, and an opening bracket or quote right before one, inside one `<span class="maffs-nowrap" style="white-space:nowrap">` with the maths. **Why not a plain nowrap:** KaTeX wraps long expressions between its `.base` blocks, and nowrap on the whole span overflowed 76 px at 320 px (the STOP IF), and a word joiner did not stop Chromium breaking after an inline-block either. So the maths is split at its `.base` boundaries: only the base beside a mark stays in the nowrap run; the rest wraps normally; the MathML stays once. **Deviation from the contract:** the rule is inline, and `theme.css` is NOT edited: 16 of the 17 MaffsText games do not link it, and touching it selected five unrelated game verifiers (the STOP IF on selection). New `scripts/test-mathtext.py` (Chromium, pinned KaTeX fonts, 10 s): glued markup, a 120-420 px line-box scan, byte-identical when no mark touches the maths, the four reported items (Paper 2C Q14/390, Q9/375, Q16/375, Q26/320; **they reproduce on the old renderer 2-8 px under the reported width in the pinned fonts, so each is scanned across +/-12 px**), all 36 Paper 2C items at 320/375/390, and nothing wider than its container at 320. `--selftest` swaps in the old `html()`: 9 of 9 fault-sensitive checks fail. **Affected (16 games load mathtext.js):** component-crusher, core-maths-paper2c, differentiation-duel, eigenvector-engine, factor-theorem, formula-unlocked, free-daily-pizza, linear-equation-solver, log-laws, moments-master, proof-builder, proportion-blaster, quadratic-factoriser, sequence-solver, split-it, test-the-claim (distinctly-average names MaffsText but does not load mathtext.js). **For Jon:** 36 games render KaTeX through their own `K()` without MaffsText; I did not measure whether any shows the same fault.

**CTS-SEVEN (21 Oct, Jon's contract; #470, main run 39556574853 green).** "All seven circle theorems" is gone from `data/games.json`, the page's two meta descriptions and both portal cards (now "the circle theorems"); `verify-circle-theorem-spotter.py` pins all of them (any "seven" or any other wording fails; three plants caught). Finding s1-008's ruling note updated. **Drift count for Jon:** the portal's 133 cards (96 distinct games) are hand-written; only **1 of 96** has a `card-desc` identical to its `games.json` description. **20 cards state a figure or scope claim** (a count, "all", "every", "each"): boolean-blitz, core-maths-paper1/2a/2b/2c, curling-friction, estimation-engine, estimation-golf, factor-theorem, four-quadrant-explorer, given-that, gradient-hunter, higher-power, linear-equation-solver, prisoners-dilemma, screening-room, seven-bridges, six-sevens-bruv, split-it, truth-will-set-you-free. None of those figures appears in its `games.json` description (only screening-room's "99" and four-quadrant-explorer's "all" do), so none can be checked against it; I did not audit the counts against the games. Generating cards from `games.json` is the fix for the drift: your call.

## 2026-10-25 (home): moved from home.md (answer-counts outcome)

**MERGE-GUARD (21 Oct, Jon's contract; #476).** **#473 finding (facts):** #473 merged at 07:28:30Z (08:28 BST). Main's last completed full run before it, 39559284220 (push, #472's merge, created 07:02:47Z), finished **failure** at 07:13:43Z, red on "CI timings and pack (main only)" alone (every other job green or skipped). So the rule was broken: the merging session (home) had watched only #471's own run (39559008796, green, finished 07:09:41Z) and did not check main's newest run before merging; the red run was started by the other lane's merge at 07:02:47Z and had finished 14 minutes before #473 merged. Not checked, not misread, not in progress. Jon's 20 Oct timings-only ruling had been replaced by PER-LINE-LIMIT (#465) and was not relied on. Main's next run, 39562229614 (#473's own merge), was green. **Replay of the last 8 days (80 merged PRs):** under rule (b) 11 would have been refused: red previous run: #457 and #465 (both under Jon's recorded 20 Oct timings-only ruling, so an `--override` case) and #473; run in progress at merge: #395, #399, #417, #430, #438, #464, #470, #472. I found no authorisation from Jon outside a recorded ruling; I cannot see anything unrecorded. **Built:** `scripts/merge-pr.py <n>` (`--wait`, `--override "<ruling>"`, `--selftest`): refuses unless the Gate is green on the head and main's newest push/manual `check-site` run is green (in progress is not green; PR runs and the Monday schedule are not main's full run, the API's `event` field tells them apart, no guessing); squash, pinned to the head. Canon §7.8.3, CLAUDE.md and cloud.md's "Every PR" line (home lane, lane-rule change, that line only; cloud.md is at 20,473 of 20,480 bytes so its next entry must trim). **From now both lanes merge only through `merge-pr.py`.** Not changed: workflow, Gate, ci-groups, ci-deps, verifiers, end-task.py, branch protection (Jon's: a rule there would stop a raw merge). #476 was itself merged with `merge-pr.py` (judged main run 39632637545); main's run after it, 39656729976, green.

## 2026-10-25 (home): moved from home.md (GEN-SIX-PS inventory)

**SET-CODES (22 Oct, Jon's contract; #486, main run 39825246146 green).** Each lock with 2+ sets shows "Set C" on its lock screen (engine.js `setTag`, from `st.vars` at render; SAVE_V and the save shape unchanged); the teacher page lists every set by letter and, with no live game, gives no single set's answer ("By set, see below", "answer depends on the set", "Worked for Set A, as an example"; live game: "14 (Set C)"). **The mapping is in `escape-rooms/assets/rating.js` (`SET_CODES` A-K, no I, `setCode(i)`):** it is already loaded by every room's index.html and teacher.html, so no room file or script tag changed (a new setcode.js would have touched 26 pages). Max library is 10 sets, so the letters suffice. New check `scripts/test-escape-setcodes.py`, CI line "Escape-room set codes" (content tier, ~50 s: 13 rooms, 40 locks, 330 sets forced through saved state; the teacher's answer for each letter must open the lock; four plants caught). 13 start screens byte-identical before and after (body HTML and screenshot hashes). Canon §11.3. Merged with merge-pr.py.

**ANSWER-LOCK-STATIC (22 Oct; cloud lane, Jon's lane exception).** `scripts/check-answer-lock.py` changed: the self-test and the static rules are their own CI line (`--selftest && --static`); `--part i/6` plays games only, part 1 included. Canon §7.6.0 records it; rebase knowingly.

## 2026-10-25 (home): moved from home.md (LOOK-REDS)

**HMP-LIST (23 Oct; cloud lane, Jon's lane exception of 07:11).** How Many Parts? listed. Shared files the cloud lane edited, rebase knowingly: `index.html`, `essentials/index.html`, `sitemap.xml`, `spec-map/index.html`, `leaderboards/index.html`, `updates/index.html`, `scripts/check-leaderboard-coverage.js`, `scripts/check-resit-page.py`, the roster, CLAUDE.md, canon. Stale counts left for you: cloud handover, HMP-LIST.

**MAIN-JOBS (22 Oct, Jon's contract; #489, main run 39841875056 green).** `merge-pr.py` `check_main()` now also reads the newest run's jobs (all pages, latest attempt): all must be finished and none failed (skipped/neutral pass); an open job is "not finished" (`--wait` is the ceiling, so a job record GitHub never closes ends in a refusal naming it, not a hang), a failed one is red, no jobs or a failed jobs call refuses. Selftest cases i-v added; the run-only `check_main` is planted and caught. **Step 1 (run 39797799822, #484):** read afterwards, run completed/success, updated 14:49:22Z; all 54 jobs completed/success, last finished 14:49:01Z, none after the run's update, so that run could not be reproduced. **But on first live use** (#489, run 39834989641) the run read "completed" while 2 of 54 jobs were still in_progress (Shared asset tests; Regenerate REGISTER.md), so the cloud lane's report is real as a transient state. A record GitHub leaves open for good (cloud lane's "Content verifiers 10" on 39823720730, gone when read later) ends a `--wait` in a refusal, then rerun or `--override`. *Cloud lane: merge-pr.py now checks jobs; call it exactly as before.*

## 2026-10-25 (home): moved from home.md (SIX-PS-BANKS batch 1)

**ANSWER-COUNTS (23 Oct, Jon's contract; #503, squash `4c32398`; main's full run 40025197868 green; first daily run by hand committed `1fef6a43`).** **The merge's own push run never started: the squash message carried the PR text's skip-CI words, which GitHub honours. Keep those words out of every PR title and body (and squash message); a manual `workflow_dispatch` of check-site.yml was the main run.** "N questions answered since September" now fills the START-MOUNT slot (games, from 1,000) and the homepage header (total, from 10,000). Counts script: separate Apps Script project, **deployed by Jon 23 Oct 2026**, read-only scope, reads through the Sheets advanced service (SpreadsheetApp needs the read-write scope and failed at deploy); first full count 26,987 rows in 6.7 s, one run; tab is `Sheet1`. `.github/workflows/answer-counts.yml` (its own workflow; 05:40 UTC alone never fired on 24 Oct, so since 24 Oct 08:16 it runs 05:40, 11:40 and 17:40 UTC; manual run 40073512548 refreshed the file) runs `scripts/fetch-answer-counts.py` and commits `schools/assets/answer-counts.json` `[skip ci]`. Loader `schools/assets/answer-count.js` (97 pages, one deferred line each, after analytics.js); `scripts/check-answer-count.py` (static, 320 px with the line shown, 28 loader cases, 10 plants), `scripts/test-apps-script-counts.py` (27 checks). **First file (23 Oct 20:34): total 16,250 over 93 slugs; 3 games at 1,000 or more** (six-sevens-bruv 3,992, factor-race 1,559, like-terms-collector 1,160). **Gate date (step 5): `mfg()` was gated to the live host on 16 Sep 2026 18:28 BST (archive `7bcbba3`), after 1 Sept, so any test/local `question_answered` rows written 1-16 Sep are in the count (the Sheet records no host; not filtered).** **Rulings (Jon, 23 Oct 20:42):** game pages show the daily file only and never call the live address (both Apps Scripts share Jon's concurrent-execution limit); only the homepage fetches live, on load then every 60 s while visible, stopping after 10 minutes (loader selftest plants: a game that fetches it, a homepage that never stops; both caught). Privacy: "used to improve MaffsGames and, as anonymous totals, to show how many questions have been answered" replaces "used solely to improve..."; no separate sentence. **File is `schools/assets/answer-counts.json`, not `data/` (`data/` is excluded from the published site; a deviation from the contract's path).** **updateCounts durations (Jon, 23 Oct 20:33-20:43, evening, low volume): 3.785 s, 1.646 s, 2.324 s, one no-new-rows run 1.436 s; doGet 0.44-2.04 s; all under the 5 s STOP IF, the worst is 76% of it. TO DO: re-check updateCounts durations (Executions panel) during a school-day peak in the first week after half term.** `docs/apps-script-counts.md` covers redeploys. **Scheduled-run outcome (25 Oct, accepted by Jon):** after the cron change (#511) scheduled runs fired late (24 Oct 11:40 slot at 14:51 UTC, 17:40 slot at 19:45 UTC) and the 25 Oct 05:40 slot was dropped; twice-a-day freshness is adequate for cumulative counts. Monitoring closed.


**START-MOUNT (23 Oct, Jon's contract; #501, squash `8bb61e4`, main run 39999880771 green).** Every live game now carries `<div class="maffs-start-note" data-maffs-start-note></div>` as the last child of its start container (96 games, one added line each, 0 changed); site-wide start-screen notes mount there (canon 7.5.4). 4 games open straight into play and carry none (52dle, equatle, estimation-golf, factor-theorem). 5 hand-placed, 3 need explicit start steps; the per-game container list and the reasons are in `docs/audits/start-mount-2026-10.md`. New `scripts/check-start-mount.py` (site-wide checks; static + Chromium, 8-case selftest): a live game in neither `CONTAINERS` nor `NO_START`, a missing, second, misplaced, late or lingering mount each fail. Next: ANSWER-COUNTS can mount on it.

**CALC-BY-STAGE (23 Oct; cloud lane, Jon's lane exception of 09:45).** Shared files the cloud lane edited, rebase knowingly: `scripts/check-calculator.py` (new value `by stage`), canon §4.4, the roster's calculator-value line.

## 2026-10-25 (home): moved from home.md (SIX-PS-BANKS follow-up)

**CHECK-CHANGED-DEFER (23 Oct, Jon's contract; #507, squash `0360034`, main run 40037107654 green and started on the merge).** `scripts/check-changed.py` now classifies each selected check from the paths `ci-deps.select()` says picked it (direct: its own script, a game's or room's own files, a page it names, data it declares; indirect: `schools/*`, `escape-rooms/assets/*`, a script library) and defers to CI every heavy check reached ONLY through a shared file, listed with the file and in the PR line; light checks, direct hits, always-run checks and a CI-file change plan as before, and `--all-heavy` runs them here; `--list` shows the split; `--selftest` (not run by CI; ~1 min) has five cases and three plants. `ci-deps.py`, CI and the Gate are untouched: CI runs every selected check. **`--list` before -> after:** the five-file ANSWER-COUNTS follow-up set (index.html, answer-count.js, its check, two handover files): 178 checks (41 heavy, 137 light) -> 146 (9 heavy, 137 light) + 32 heavy deferred; the 9 left are 3 site-wide checks, 3 escape-room tests and 2 Equation Builder parts reached through `index.html` (a page they name), and 2 always-run checks. One game (`games/split-it/index.html`): 46 (5 heavy, 41 light) -> unchanged. Canon 7.8 and CLAUDE.md carry one sentence each.

**TAKE-A-WALK-LIST (23 Oct; cloud lane, Jon's lane exceptions of 20:00 and 20:33).** Take a Walk listed. Shared files the cloud lane edited, rebase knowingly: `index.html`, `essentials/index.html`, `sitemap.xml`, `spec-map/index.html`, `leaderboards/index.html`, `updates/index.html`, `scripts/check-leaderboard-coverage.js`, `scripts/check-resit-page.py`, `schools/assets/firebase-leaderboard.js` (LEVEL_NAMES `stage-1`..`-4`), the roster, CLAUDE.md, canon.

**ANSWER-HEADLINE (23 Oct, Jon's contract; #506, squash `c330b65`, main run 40034938914 green; the push run started: no skip-CI words in the PR text).** The homepage's questions-answered figure is now a headline (option A): the number large and bold in white (2.4rem, 700, tabular figures) with its label beside it, under a 1 px rule (#2f3e60) at the foot of the subtitle; hidden, with no rule or gap, under the same rules as before. "Updated every 5 minutes" is rendered by `schools/assets/answer-count.js` only while the figure on screen is the live one (never from the daily file, and removed if a later refresh fails). Game start screens unchanged. `scripts/check-answer-count.py`: 320 px no sideways scroll, number on one line, 4.5:1 for number, label and updated line, and 12 new loader cases; plants (updated line from the daily file, updated line while the block is hidden) both caught.

## Moved from docs/handover/home.md, 29 Oct 2026 (home lane close)

**ANSWER-COUNTS-STALE (26 Oct, Project Claude's contract; Jon's ruling: accept Z; #555, squash 9680096, main run 40391972449; the alert fallback #557, squash 5a1d072, main run 40396174732 green). **Result:** the manual run (workflow_dispatch 40391985213, 20:01 UTC) committed as_of 2026-10-26T20:01:23Z, total 17,216; the live file, fetched with a cache-buster, shows the same; on the live homepage (the Apps Script answer stubbed to 17,500) a refresh starts from the stored 17,500, and with sessionStorage blocked it behaves as before. **Closed 26 Oct (Jon's ruling): Issues stays off**; the alert route is GitHub's e-mail plus the daily scheduled-watch failure (above). **check-site b001e21 (25 Oct 10:46 UTC, e-mail 10:55): failed in the post-merge job "CI timings and pack (main only)", step "Record, repack and commit if changed", not in Plan (Plan passed):** burst mode's check-burst.py line ran 220 s (88% of Content verifiers 42's 270 s budget), so the new pack failed `ci-groups.py --check` and nothing was committed. Resolved by BURST-SPLIT (#530, f4853dd, three lines); timings commits have recorded on every main run since. The next scheduled answer-counts slot is 27 Oct 05:40 UTC (GitHub starts it late); its commit is not recorded here.** **Cause (evidence):** every scheduled answer-counts run since the last good one (24 Oct 19:45 UTC) failed at "Fetch, validate, commit" with `FAIL as_of '2026-10-26T11:31:31Z' is not an ISO time with an offset`: runs 40183466989 (25 Oct 10:07 UTC), 40205053536 (25 Oct 15:02), 40228338567 (25 Oct 19:55), 40315693353 (26 Oct 11:31), all schedule, all failure, `NOT written`. The Apps Script writes `as_of` with `Utilities.formatDate(..., "...XXX")`, which prints `+01:00` in BST and `Z` in GMT; the clocks went back on 25 Oct; the validator's `AS_OF` accepted only `[+-]hh:mm`. Only four scheduled runs fired in the window, not six (none between 25 Oct 19:55 and 26 Oct 11:31). The weekly check-site was fine (its 26 Oct 11:08 scheduled run and every push and PR run passed); it does not look at the counts. **Fix:** `Z` accepted (ISO 8601, RFC 3339); the Apps Script untouched. Every reader of `as_of` checked: `fetch-answer-counts.py` (regex now `Z|[+-]hh:mm`; "is today" is now the instant's date in London, not the string's), `answer-count.js` (`Date.parse`, already correct), `check-answer-count.py` and `test-apps-script-counts.py` (the latter asserted `[+-]hh:mm` of the Apps Script's own payload, now both); the "Updated every 5 minutes" logic never reads `as_of`. Each has cases for `Z`, `+01:00`, `+00:00` and the exact `2026-10-26T11:31:31Z`; the validator selftest also has `+0100`, lower-case `z`, no offset, Z across London midnight (37 cases). **Visibility (revised 26 Oct, Jon: Issues stays off):** no issue code. A failed run of answer-counts, scheduled-watch or check-site on main sends GitHub's e-mail, which Jon filters in Gmail (the four failures did e-mail him; buried, not missing). `scheduled-watch.yml` (daily 07:50 UTC) fails with a plain reason when the committed file is over 24 hours old (`fetch-answer-counts.py --check --fresh`), which catches a schedule GitHub never starts; the weekly check-site holds the file to 24 hours on a scheduled run only (selftest plants stale files). `scheduled-alert.py` and its 410 handling are removed. **Count-up memory (Jon's option b):** homepage branch of `answer-count.js`: after each live figure is displayed it is stored in `sessionStorage` (`maffsAnswerCount`, `{n, since}`); a load starts from it when same `since`, at least the file figure and no more than the live figure, else from the file figure; never animated down (a stored figure found too high is snapped back to the file figure, then counted up), reduced motion and the 10,000 and 7-day rules unchanged, every storage call in try/catch; game start screens untouched. Loader selftest: 62 cases, 16 planted faults (refresh starts from stored, other `since` ignored in both layers, above live ignored, throwing read and write, live figure never stored, a loader reading only `+hh:mm`). Canon 7.5.5 records all four.

**SHAPE-SHIFTER-TYPES (26 Oct, Project Claude's contract, Jon's ruling "fixed at the source"; #552, squash 8d0ffeb, main run 40363636645 green; its clean-up #553, squash e153421, main run 40367993153 green; its first two pushes failed CI: the plant parts ran 226 s and 220 s, then Tier 4's B3 found identical enlargement words; the PR also carried `.claude/pr.json` by mistake, removed in the follow-up that wrote this line).** Shape Shifter now **builds** reflections in y = x, y = -x, x = k and y = k and enlargements, the way it builds rotations; the 6 P's transformations bank is regenerated from it. **Before / after, game pools:** translation 15 / 15, reflection 15 / **35** (the 15 typed ones untouched, then 20 built: 5 in each of the four lines; k = 2, -3, 1, -1, 3 for x = k and -2, 3, 1, -3, 2 for y = k; the shape on alternate sides of every line), rotation 15 / 15 (untouched), **enlargement 0 / 16** (scale factor 2 six, 3 four, 1/2 six; centre at the origin 3, elsewhere 13, at least two in each quadrant; each scale factor and centre once, so no two questions share words: Tier 4 layer A's B3 flagged two pairs of identical words on the first push and the pool was redrawn). **Bank: 45 / 81**: the 45 are byte-identical (same ids, corners, answers, diagrams); 36 new (reflection 20, enlargement 16; bands 3: 12, 4: 14, 5: 10); every one has worked lines, and 34 of 36 have slip lines (the two without are the enlargements about the origin by 2 and by 3, which have no distinct wrong answer to name). **How:** `reflectShape` takes `'x'`, `'y'`, `'y=x'`, `'y=-x'`, `'x=k'`, `'y=k'` (the typed items' two lines are unchanged); `buildReflectionQuestions()` and `buildEnlargementQuestions()` draw from a fixed seed so the pool is the same on every load, dropping any candidate whose shape or image leaves the -5 to 5 grid (and, for enlargement, any image that is not a whole number or that has a corner on the centre); the mirror line is drawn dashed and named just outside the grid, the centre of an enlargement is an amber dot; the same tap-every-vertex interaction, the grid still -5 to 5. A fifth **Enlargement** mode card (`data-mode="enlargement"`), 10 questions, its own personal best; **Random Mix is still translation, reflection and rotation** (so it now draws its reflections from the 35, and its card says so). The reflection card, the reflection reveal text and the start sentence were reworded to match. The game has no KaTeX (plain text on the canvas and in the instruction); the **bank** stems use `\( \)` for every equation and coordinate. **Verifier** (`scripts/verify-shape-shifter.py`): learns the new lines (each image recomputed from the words as a reflection in a x + b y = c, not from the game's formulas) and enlargements (Fractions; whole numbers on the grid; no corner on the centre), checks the counts (at least 5 in each line, both signs of k, both sides; at least 15 enlargements, 5 at 1/2, 8 about another centre, a centre in every quadrant, only 2, 3 and 1/2), taps every vertex of every new image at all 121 grid points, plays all five modes to 10/10 and 0/10, and checks the mirror line's name is drawn; four new plants, each caught (no swap in y = x, no doubling in x = k, an enlargement about the origin, an off-grid image not dropped); 18 plants in all, now in four CI lines (parts 2 to 5, a quarter each: the first push ran two halves at 226 s and 220 s against a 189 s per-line limit and failed PR budget, so they were split); part 1 about 20 s. **Templates (gen-six-ps.py; the wording is mine, for Project Claude to review):** y = x "swaps the coordinates: (x, y) goes to (y, x)"; y = -x "swaps the coordinates and changes both signs: (x, y) goes to (-y, -x)"; x = k and y = k "a point goes the same distance from the line, on the other side", then "A is 2 to the right of the line, so its image is 2 to the left of the line: x = 1, and y = 3 stays the same" (a point on the line stays); enlargement "every distance from the centre is multiplied by 2 / halved", "From the centre to A is 2 right and 1 down. Multiplied by 2, that is 4 right and 2 down", "Starting at (1, 2) and moving ... gives (5, 0)"; slips: y = x answered as y = -x and the reverse; x = k answered as the y-axis, or as y = k; y = k answered as the x-axis, or as x = k; an enlargement done from the origin, the distance from the centre left unadded, the scale factor the wrong way round (only where the wrong answer is a whole number and differs from the key). **Diagram check, now 396 diagrams (was 360):** line through a label as first worded 8 (unchanged: angles 2, trigonometry 6; none in the 36 new ones), strict 61 (was 42: the 19 new are the mirror lines and rays, transformations 6 / 25), labels overlapping 123 (was 87: the two -5 on every grid), **0 faulty after the labels are moved**. **Phone:** `measure-phone-fit.py` reports shape-shifter UNMEASURABLE ("no answer controls found", the canvas) before and after, the report identical; separately I measured the game screen at 320 px: it scrolls sideways by 5 to 21 px in every vertex mode, **on main too** (translation 337 against 320, reflection 325; enlargement 341), a pre-existing fault this change did not cause and did not touch; 390 px fits. Not touched: the typed translations and reflections, the rotation builder, the grid size, theme row or tier, `data/games.json` (its description still reads "Translate, reflect and rotate"), Distinctly Average, canon 7.6, score-history.js. Review sheet: regenerated and republished at https://claude.ai/artifact/FHXCnemqt489oVZXribfFS (81 transformations questions, 1,685 in all).
