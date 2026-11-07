# Handover: home lane

**Queue (cross-lane facts; never archived)**

- ROOM-SEARCH-TITLES (Shared; Jon, 6 Nov; Amendment 1, 18:55; Amendment 2, review fixes, 23:05): DONE. #693 merged as 5202a94; main run 42358602377 GREEN; claude/room-meta removed by end-task. Branch claude/room-meta, worktree ~/mg-room-meta. Contract: docs/history/contracts/2026-11-06-room-search-titles.md. Entry below.

- PHONE-FIT-ASIDE: DONE. #687 merged as 5b4931f on Jon's word; main run 42270819300 GREEN. No Project Claude review is recorded in this lane. Contract: docs/history/contracts/2026-11-06-phone-fit-aside.md.

- WHOSE-SIDE: DONE and live, unlisted. #674 merged as 257e883; fixes #676 merged as f1acc1f (it contains #675, closed unmerged); main green. Merged on Jon's word before review; Project Claude reviewed #674 and #676 on 6 Nov and passed them (side roles in both θ positions, FN, Stage 4's key, all 12 triples, uniform scaling). Worktrees and claude/whose-side-fixes deleted on Jon's call, 6 Nov. Art done (#684). timer-policy.md's line waits for WHOSE-SIDE-FIT to merge; the cloud lane owns the game until stage 5, which follows WHOSE-SIDE-BIOS. Contracts: docs/history/contracts/2026-11-05-whose-side*.md.

- CHRISTMAS-ROOM: DONE. #667 merged as 9cbedee; close-out #668 merged as e32608f. Contract: docs/history/contracts/2026-11-04-christmas-room.md.

- Cloud lane: one session at a time from 6 Nov (Jon, 5 Nov). #669 and #671 are merged; no overlapping cloud sessions remain authorised.

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts to move next (cloud lane, HOW-MANY-PARTS-FRACTION)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

- FRACTION-WHOLE: merged #662, b38ce399; Shared review passed and Jon authorised merge, 4 Nov. Contract: docs/history/contracts/2026-11-04-fraction-whole.md. Main run and cleanup recorded below.

## 2026-11-07 (home): CHRISTMAS-PACK close-out

Done: #689 merged by `merge-pr.py` as b4d0323; main run 42362844296 GREEN. Jon authorised merge on 7 Nov. The six-set Christmas Tree Fiasco printable pack builds with 98 of 900 joint draws VALID; its 18 printed lock answers agree with 108 independently recomputed values. The PDF stays gitignored in `dist-packs/`, never committed or uploaded. Contract and Amendments 1–5: `docs/handover/contracts/2026-11-06-christmas-pack.md`; the two later typography and box-measurement corrections are reported in #689.

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

