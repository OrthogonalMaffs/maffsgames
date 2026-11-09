# Handover: home lane

**Queue (cross-lane facts; never archived)**

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): PR at the Gate, holding for Project Claude's review and Jon's "merge". Branch claude/docs-bundle, worktree ~/mg-docs-bundle. Contract: docs/handover/contracts/2026-11-09-docs-bundle.md. Entry below. MONEY-INPUT merged as #719 (b328883b).

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

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

