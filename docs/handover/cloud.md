# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Remaining list (contract LH, 7 Oct 2026; added by the home lane, kept by the cloud lane):** it lives in
`scripts/answer-lock-state.json`, not in this file (contract ANSWER-LOCK-STATE, 19 Oct 2026); `scripts/check-answer-lock.py`
reads it. Take a game off it in the PR that finishes it. While a game is on it **and unlisted**, a failure of that game
in the check is reported, not failed; a listed game on it is judged as if unclaimed (`exempt()`: claimed AND unlisted;
corrected 2 Nov, Codex's catch). Off it, a failure fails CI.

**Lane rule, listed games (Jon, 8 Oct 2026; contract "listed-game CRITICAL/HIGH"; the home lane records it in
canon §7.8 in its next docs PR):** the cloud lane now also fixes listed games. Before starting one, add it to the
remaining list (`scripts/answer-lock-state.json`) and push that commit on its own, so the home lane's F1 batches skip it; take it off
in the PR that fixes it. One game claimed at a time; never claim a game already in an open home-lane F1 batch branch
(check `docs/handover/home.md` and the open PRs first; if it is, skip to the next and note it).

**Resume rule, MaffsLock (Jon, contract LH):** adopting MaffsLock includes the game's lock-hint declaration
(`<!-- maffs-lock-hint ... -->`, canon §7.6.0), and the game passes `check-answer-lock.py`. Hints live in the
game's page, never in the shared script.
A two-option game declares an `answer` that picks the option differing from its key for `i >= 1` (canon
§7.6.0, contract DET, 8 Oct; prime-or-composite is the pattern).

**Contracts (Jon, 8 Oct 2026, corrected 20:00):** each contract is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md` in its claim commit (or the PR's first commit), pointed to by a `docs/todo.md`
row, not a Queue line (AGENTS.md). Read it when the item starts, not at session start (the folder stays out of the
start-up load). When the work merges, move the file to `docs/history/contracts/`.

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (14 Nov):** main run 43590939932 on 6f37c69 (#760) red only in Answer lock L7: trig-identity-duel, `Page.goto: Timeout 20000ms exceeded` loading the page from the runner's own server (the merge touched no game, shared asset or checker; the job passed on the PR head); failed jobs rerun once, attempt 2 GREEN. **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk's random phone-fit reds (375x667 Aa, 320x568 normal) are fixed by TAKE-A-WALK-SEED** (no seed reads the clock; the Gate's clock-seed scan); its layout is todo row TAKE-A-WALK-PHONE-LAYOUT. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

**Live pointers (kept out of dated entries, Jon 2 Nov; the first four from the 27 Oct entry):**
- **Step 4:** `docs/todo.md` row GATE-STEP-4 (§4).
- **Step 6:** `docs/todo.md` row GATE-STEP-6 (§4).
- **Queue after the freeze:** `docs/todo.md` rows FOLD-COMPONENTS and KEYPAD-FRACTION (§3); measure-phone-fit on `wait_settled` is in GATE-STEP-4 (§4).
- **Old worktrees and their branches:** `docs/todo.md` row BRANCH-CLEANUP (§7).
- **merge-pr.py grace period:** `docs/todo.md` row MERGE-PR-GRACE (§4).
- **check-banks.py escape:** `docs/todo.md` row CHECK-BANKS-ESCAPE (§4).
- **Flake (4 Nov):** main run 41811116888 red only in the timings job (GitHub push: Internal Server Error x3); one rerun GREEN.
- **LOOK-REFRESH-1 palette triage:** `docs/todo.md` row LOOK-REFRESH-PALETTE (§3).
- **ci-deps.py and tools/:** `docs/todo.md` row CI-DEPS-TOOLS (§4).
- **SEARCH-KEYWORDS triage:** `docs/todo.md` row SPEC-MAP-SHORT-BANKS (§3).
- **Search rule in canon:** `docs/todo.md` row CANON-SEARCH-RULE (§7).
- **Room escapes in canon:** `docs/todo.md` row CANON-ROOM-ESCAPED (§7). Jon redeployed the endpoint at 09:02 on 4 Nov; /exec reports `2026-11-04-a`: done.
- **For the rulebook queue (Jon, 3 Nov; no change now):** end-task.py always refuses in cloud sessions, which work in the primary checkout ("is checked out in the primary checkout", after #643); cloud cleanup is nothing to do (the container ends, GitHub deletes the merged branch).

**START HERE (next session; written 19 Oct, 18:10 BST).**
- **Done lists and main-run history to 24 Oct:** moved to `docs/history/handover-cloud-archive.md` (27 Oct, size limit).
- **Waiting on Jon, the list of 20 Oct (fact cards, Monty Hall card, PYTHAG-REPORT, phone header stacking):** in `docs/history/handover-cloud-archive.md`, moved 27 Oct.
- **Container setup (every fresh session):** `pip install playwright==<the version in /opt/node-tools/node_modules/playwright-core/package.json> sympy mpmath pyyaml` (1.63.0, browser revision 1243, on 25 Oct; a pinned 1.56.0 looks for a browser the container does not have and fails every Chromium check); `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1` for what imports it (`bank_common.py` and some verifiers). **No check-changed.py before a push (AGENTS.md, CLOUD-LEAN):** before the first push only the worst-case test where canon §7.8.4 requires it by hand, and the selftest of any script changed; the PR's Gate is the check. Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/handover/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

**Merge route:** merge-pr.py only (the 10 Nov ruling was retired by Jon, 16 Nov 2026; canon MERGE-ROUTE). If it cannot reach GitHub, stop and report; the PR waits.

**Standing rule, close-outs (Jon, 10 Nov 2026, 13:13; recorded verbatim, CUMFREQ-CURVE's preamble):**
> STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
> A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.

## 2026-11-17 (cloud): ITS-A-SINE-LIST (`docs/handover/contracts/2026-11-17-its-a-sine-list.md`; Jon 17 Nov)

Agent Claude Code (cloud), branch `claude/fervent-feynman-25e9sg` restarted from main 6d8cc0e (after #816). Tier Medium: merge on green, Project Claude reviews after. **Lane exception (Jon, 17 Nov 2026, verbatim):** "one-off LANE EXCEPTION (listing is normally home-lane work; Jon, 17 Nov 2026, chose "Cloud, before ice cream")".
**Approval (verbatim):** Jon, 17 Nov 2026, 14:58: "also the students have tried the it's a sign game, it's ready to get listed now please". Jon, ~15:03, to Project Claude: levels "All three" (GCSE, Level 3, Level 4); placement "GCSE section" (roster GCSE Games, a portal GCSE card, no /essentials/ card); lane "Cloud, before ice cream".
**Close-out carried (first commit):** #816 CORE-PAPER-EXIT, recorded in its entry below; contract moved.
Done on the branch: portal GCSE card (after whose-side-are-you-on: the section's listed games run in go-live order; `data-levels="gcse l4"`, the filter has no Level 3 value; keywords from data/games.json; New badge 2026-11-17); sitemap (alphabetical, after integration-duel); spec map G22–G23 (`?level=gcse`) and Level 4 LO2 (`?level=level4`), no Level 3 row for the rules (the map's only Level 3 is Core Maths); hub row after screening-room with the 12 boards `<level>-<mode>`; check-leaderboard-coverage.js: NOT_ON_HUB entry removed, LEVEL_OVERRIDES entry added (the check required it); notes in audit-register.py and check-theme.py; roster row #111 to GCSE Games (31), "Unlisted (contract ...)" dropped from its description, look signed off 2026-11-17, Unlisted (7), the listing note; /updates/ line; todo ITS-A-SINE-LIST closed to todo-done.
Next: PR, Gate, merge with merge-pr.py (after CANTEEN-PACK #817 if it is merging).

## 2026-11-17 (cloud): CORE-PAPER-EXIT (`docs/history/contracts/2026-11-17-core-paper-exit.md`; Jon 17 Nov)

Agent Claude Code (cloud), branch `claude/fervent-feynman-25e9sg` from main 359a368 (after #815; step W met 16:47 UTC). Tier Shared (Amendment 1): stops at "Ready for architect review", merges only on Jon's "merge".
**Close-out carried (first commit):** #815 ANSWER-BOX-TEXT PR 2, recorded in its entry below; contract moved. #814 was already recorded.
File:lines re-checked on 359a368: the papers, stage-exit.js/.css and verify-stage-exit.py are unchanged since fee6ad3.
Done on the branch: `schools/assets/stage-exit.js`/`.css` take `data-game`, `data-leave` and `data-confirm="second-tap"` (3 s "Tap again to exit", the shell's own timer), each default today's behaviour; with no `.hud` in the in-play screen the header row holds the button while that screen is active, in the back link's 15 px (44 px targets overflow it). The four papers load it with `data-game="#gameScreen" data-leave="exitPaper" data-label="← Exit paper"`; `exitPaper()` is `MaffsLock.clearTimers(); showScreen('startScreen')` (clearTimers: found by me, approved in Amendment 1; the section banner's 2 s timer otherwise fires after leaving). `scripts/verify-stage-exit.py`: the papers in ci-deps; per paper the button off on start and results, on during the banner and a question, one tap arms and reverts after 3 s, two taps reach the start, nothing recorded, the banner timer cleared, a fresh run after; the papers at all five sizes; the stage games' header row must stay hidden on a question. 13 of 13 plants caught (4 new). Fold at 375 x 667, before and after: screen top 47 px on all four; first option above the fold 36/36, 35/36, 36/36, 36/36, every option at the same y. todo IN-PLAY-EXIT-GAP (89 games, listed only): the list, method and exclusions in `docs/audits/in-play-exit-gap-2026-11.md`, the row a pointer (Jon, 17 Nov, in session: main's todo.md had 389 bytes left under its cap, the full row was 3,408); /updates/ line.
PR #816. First Gate 44154190683 red only in Answer lock L1/L3/L5/L6, one fault on each paper: Play again showed "← Exit paper" open to a double-click's second click (not MaffsLock.screen): the row sits outside #gameScreen, so the page's fresh window never covered it. Fixed in the shell: when the in-play screen becomes active the row gets `MaffsLock.fresh(row)` (a MutationObserver; leaving the screen also disarms); the verifier checks it, a new plant catches its removal (14 of 14), and check-answer-lock passes on the four papers locally. phone-fit-full 44154267653 was green on the first head.
Jon said "merge" (17 Nov, after the PR opened), then "merge when green". PR's final checks on head 4dfe3ff: Gate 44158222817 and phone-fit-full 44158207479 green. MERGED 17 Nov 19:39:03 UTC as 7d8ff64 (squash) via merge-pr.py `--watch --wait 3600`, exit 0, last line "main 7d8ff64 run 44160860707: GREEN". Main on 7d8ff64: check-site 44160860707, phone-fit-full 44160860832, pages build 44160860492, all success (recorded in ITS-A-SINE-LIST's first commit, which moved the contract to `docs/history/contracts/`). Branch removed by end-task.py.
Record: agent Claude Code; wall about 4:41 (contract 14:58, merged 19:39, mostly the step-W wait for #815 and runner queues); review cycles 1 (first Gate red on Answer lock: the exit row was open to a double-click's second click after Play again; fixed in stage-exit.js); amendments 1; usage n/a.

