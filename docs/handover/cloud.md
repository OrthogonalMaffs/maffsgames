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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

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

## 2026-11-09 (cloud): HEADER-FIT (`docs/handover/contracts/2026-11-09-header-fit.md`, Small, Amendment 1, todo row 1.39)

At the Gate, holding for Project Claude's review and Jon's look and "merge" (contract: do not merge): [#717](https://github.com/OrthogonalMaffs/maffsgames/pull/717), branch `claude/festive-lovelace-iukjhc`, worktree the primary checkout. First Gate green on da3d4fe (run 42605952691) with both of equation-builder's Aa buttons kept (STOP IF 1, both wired) and the titles cut short at 320px. Amendment 1 (Jon, 11:34, "yes to both"): equation-builder keeps the standard `a11yToggle`; the second button's cream palette and teal start title moved onto Aa mode, and its larger text too but above 480px only (on a phone, with OpenDyslexic, it put Next at 836 against an 804 fold at 390x844); its tighter letter spacing gave way to the standard's. All three: below 375px, and up to 480px in Aa mode, the back link is its arrow only (aria-label "Back to Games", 44x44), the divider hides, title and Aa share the first row and the pill and score take a row under them; the title shows in full at 320px (168px wide; two lines at a word break in Aa). measure-phone-fit (normal, Aa): no sideways scroll, every figure the same or better than main; tier 1 clean. Todo row 1.39 closed to todo-done.md; /updates/ line; the three claimed together and released.

Discoveries: measure-phone-fit's `--aa` sets `mfg_accessible`, but probability-pioneer and shape-shifter (and like-terms-collector, by the same key) read only `mfg_dyslexia`, so their Aa mode is never measured; in it both headers overflowed at every size (489, 498 px on main). probability-pioneer in its own Aa mode still scrolls sideways (418 px) from `div.scale-label`, question content outside this contract. Next: review, Jon's look and "merge"; the contract file moves to `docs/history/contracts/` after merge.

Record: agent Claude Code; wall n/a (planner and container clocks differ); review cycles 0; amendments 1; usage n/a.

## 2026-11-09 (cloud): SCREENING-ROOM-FIT (`docs/history/contracts/2026-11-09-screening-room-fit.md`, Medium, Amendment 1, todo row SCREENING-ROOM-FOLD)

Merged as 0e27f06 (main run 42597611148 green): [#716](https://github.com/OrthogonalMaffs/maffsgames/pull/716), branch `claude/compassionate-cray-pek7mp` (restarted from main 46fea98 after #715 merged), worktree the primary checkout. First stopped before code: the 6 px floor rested on a wrong premise (the game ships 5 px and 3 px icons; 10,000 icons cannot reach 6 px in any layout). Amendment 1 (Jon, 08:46, "fix it simply"): `ICON_CAP` 10,000 -> 1,000, the largest allowed that fits; the grid class follows the icons drawn (50 / 250). Continue is above the fold on all 70 items at 1366x768 and 1280x720 (worst core_08 649 / 680; main 56 and 38 items over). `verify-screening-room.py` states the cap itself and plays every item at both sizes after a wrong gut check on the page clock (no 5 s race); selftest 23/23. measure-phone-fit, every mode: no size worse, Continue 95-245 px higher everywhere; no state entry stale. Todo row closed to todo-done.md; /updates/ line; claim taken and released.

Discoveries: on the rarest conditions the true positives are now a sliver of one icon (alevel_19: 0.014 of an icon; 0.14 before), flagged for Jon's look. `check-banks.py --ci` cannot pass in this container (CDN unreachable: KaTeX undefined, banks not read). Next: review, Jon's look and "merge"; the contract file moves to `docs/history/contracts/` after merge.

Record: agent Claude Code; wall n/a (planner and container clocks differ); review cycles 0; amendments 1; usage n/a.

## 2026-11-09 (cloud): SCREENING-ROOM-FOLD (`docs/handover/contracts/2026-11-09-screening-room-fold.md`, Small, todo row SCREENING-ROOM-FOLD)

STOPPED (STOP IF: the fix needs a design change), at the Gate for Project Claude's review and Jon's "merge": [#715](https://github.com/OrthogonalMaffs/maffsgames/pull/715), branch `claude/compassionate-cray-pek7mp`, worktree the primary checkout. No game change. The measured "Next" is phase 2's Continue under the icon array after a wrong gut check, at 717/680 at 1280x720 (seeded question gcse_07; local and CI the same). It is real: Continue is below the fold for 17/20 GCSE questions at 1280x720 (up to 1013) and 14/20 at 1366x768, because everything but the grid takes 582 px and the grids are 75-467 px. Spacing would pass the seed only. The CI passes of 7 Nov were false: Continue appears at about 5.0 s and `settle()` stops at 5 s, so a slower page reads opacity 0 as "no Next" (both verdicts reproduced on one commit). That is how #707 took the 27 Oct entry off as STALE. Finding appended to the todo row; claim taken and released; #714's contract to history.

Discoveries: the settle race is a checker defect (shared, home lane), not yet a todo row (outside this contract). `check-site.yml` has no phone-fit shard; only `phone-fit-full.yml` measures laptop mode. CI artifact zips are unreachable from this environment (blob host blocked); logs suffice. Next: Jon's ruling on the design (PR body, options a-e) and Project Claude's review; main's nightly laptop job stays red on screening-room until then.

Record: agent Claude Code; wall 0:30 (contract 07:55 to hand-off); review cycles 0; amendments 0; usage n/a.

## 2026-11-09 (cloud): CLAIM-EXPLAIN-SPACES (`docs/handover/contracts/2026-11-09-claim-explain-spaces.md`, Small, todo §1.32)

Merged as d37644b (main run 42558847352 green): [#714](https://github.com/OrthogonalMaffs/maffsgames/pull/714), branch `claude/amazing-mccarthy-y7q1nh`, worktree the primary checkout. test-the-claim's 15 `crExplanation` strings (B1-B5, B7, B10, B12, P1, P2, P4, P8-P10, P12) wrap their words in `\text{}`; call site unchanged. Played in Chromium through the game's own `checkStep3()`: 21 of 36 with spaces on main, 36 of 36 after. Verifier PASS, output byte-identical; its regexes find the same 57 probability and 57 comparison claims. Ledger: the 15 B7 entries removed, B7 pass. Findings: `test-the-claim-kw-001` (MEDIUM, fixed). §1.32 moved to todo-done.md; /updates/ line; claim taken and released in this PR.

Discoveries: `--write-ledger` also refreshes stale `line` fields (B6 855 → 899 here, the same on untouched main); B6's old value was restored by hand so only the 15 entries change (DO NOT TOUCH). Ledger lines drift whenever a page is edited without a regen; `--ci` matches by id, so nothing fails. Next: review, then Jon's "merge"; the contract file moves to `docs/history/contracts/` after merge.

Record: agent Claude Code; wall 0:25 (claim commit 03:19 UTC to the hand-off push; contract received shortly before); review cycles 0; amendments 0; usage n/a.

## 2026-11-07 (cloud): PHONE-FIT-FULL-WORKFLOW and PHONE-FIT-FULL-SPLIT (`docs/history/contracts/2026-11-07-phone-fit-full-workflow.md`, `...-split.md`, Shared, Amendment 1)

DONE: #702 squash-merged as 023a821 and #707 as 0ec5cd4, both by `merge-pr.py` on Jon's "merge" (7 Nov); main runs 42395102273 and 42403456036 GREEN. `.github/workflows/phone-fit-full.yml` runs `measure-phone-fit.py` over every live game, one parallel job per mode (normal, Aa, laptop) plus a verdict job, nightly at 02:23 UTC, on `workflow_dispatch`, and after a push to main that `scripts/ci-deps.py` `is_shared()` calls shared: `classify()` not "known", a file two or more game pages load, or the checker's own files except `NOT_CHECKER_DEPS` (its output `docs/phone-fit-report.md` and the claim list `scripts/answer-lock-state.json`; Amendment 1). No `paths:` filter, no branch trigger; Plan's selection unchanged (`--explain` byte-identical).

First run (42395102257, modes in series): red as PHONE-FIT-RED expected, about 30m42s, over the contract's 30 minutes: STOP. Jon ruled one job per mode plus a verdict job, and screening-room's stale laptop entry off `phone-fit-state.json` (#707). Run after #707 (42403456019): GREEN, no failing pairs; jobs normal 11m49s, aa 11m51s, laptop 8m26s, verdict 4 s; whole run about 12m13s.

Discovery: run under `scripts/bg.py`, `merge-pr.py --watch` exited both times while main's run was in progress, without its final line; main's runs were read from GitHub instead. Cause not looked into.

Record: agent Claude Code; wall 4:45 (14:26 to 19:10, including both waits for Jon's rulings and merges); review cycles 0; amendments 1; usage n/a.

