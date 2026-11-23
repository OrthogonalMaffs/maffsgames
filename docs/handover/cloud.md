# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane scope (Jon, 20 Nov 2026):** the cloud lane edits what its contract names. Without a contract naming them, it never edits `schools/assets/`, the shared modules in `scripts/`, the workflow, canon, the roster's listed section or `docs/todo.md`. AGENTS.md's TODO-TRIM rule applies to every cloud PR.

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

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/history/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

**Merge route:** merge-pr.py only (the 10 Nov ruling was retired by Jon, 16 Nov 2026; canon MERGE-ROUTE). If it cannot reach GitHub, stop and report; the PR waits.

**Standing rule, close-outs (Jon, 10 Nov 2026, 13:13; recorded verbatim, CUMFREQ-CURVE's preamble):**
> STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
> A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.

## 2026-11-23 (cloud): WWIUT-BATCH-MERGE (`docs/handover/contracts/2026-11-23-wwiut-batch-merge.md`)

Claude Code (cloud), the home lane's branch `claude/wwiut-batch-1-2` taken over at bc1fa32 (its three commits as Project Claude reviewed them), not rebased. Tier: takeover under Jon's one-off lane exception (shared files site-nav.js, index.html, data/games.json; one line in home.md).

- **Done on the branch:** origin/main (ccbcc4b) merged in, clean; `scripts/build-uses.py` re-run after it: "0 of 35 files changed". Close-out commit: #889's (entry below), #887's 616 px record corrected, this contract saved. The takeover line added to the home lane's WWIUT-BATCH-1-2 entry.
- **Decided for you:** the close-out commit comes after the main merge, not before it: #889's entry and contract file exist only on main, so step 2 could not be done on bc1fa32 as written. It is still the task's first own commit.
- **Discoveries:** the corrected SITE-CONTRAST wording names fold.js timing as the cause; #889's entry found that timing for Some Thingies' arrays (601-604 px) and left main's 616 px on Sums in Disguise unreproduced, its cause not shown. The wording is the contract's, applied verbatim.
- **Next:** Gate green, merge with merge-pr.py, report main's run. WWIUT-BATCH-1-2's contract move and this merge's record ride on the cloud lane's next task.

## 2026-11-23 (cloud): PRIMARY-FIT-SWEEP (`docs/history/contracts/2026-11-23-primary-fit-sweep.md`)

Claude Code (cloud), branch `claude/pensive-gates-ktng9n` from main b5123bf. First commit: #887's close-out (entry below), this contract saved.

- **Done on the branch:** `scripts/fit_common.py`, the one fold measurement (MEASURE_JS, fit(), the picture check null-safe), `open_phone()` (360x640, touch, the pinned real fonts, a mocked LOCAL voice so the speaker shows, reduced motion) and `sweep()` (every item, every variant, every step; self-test: Next 20 px below the fold on one item after one variant is caught, a layout moving a frame after measuring is caught; its own ci-line). Both verifiers import it; their FIT_JS/fit() and the k < 2 fits are gone, as are Sums in Disguise's two-item read-aloud fits. Units `fit <look> <stage>` (10 and 16), sharded by ci-shards. A verifier-only line argument on `SID.ui.answer` / `ST.ui.answer` (null for players: the random line). Two plants each (one item, one variant). Coverage: Sums in Disguise 452 item views, 4,760 variants, 19,580 controls; Some Thingies 738 item views (as question 1 and 11, arrays also 5 and 8), 13,400 variants, 30,180 controls. Both PASS locally.
- **Discoveries:** (1) the sweep's first run failed 13 grown and 39 kids Stage 3 arrays (8 or 10 wide) at question 11, Next at 601-604 px: measured in the same task as the tap, before `schools/assets/fold.js` lays the options two to a row (one frame later, 48 to 44 px buttons). Settled, Next is at 593-596 px: no student sees the overflow. Fixed in the measurement (MaffsFold.decide() before measuring; one variant in 20 re-measured after two frames), not the game. (2) Some Thingies' End button grows the HUD 34 to 47 px at question 11: kids Stage 3 arrays keep 7 px under the fold. (3) Main's 616 px (read aloud, kids, s5_005 after a wrong answer, CI run 45126347307 attempt 1) does not reproduce here: 499-503 px with the real fonts, DejaVu, FreeSans/WenQuanYi fallbacks, full or reduced motion, every decoy, the CI block's exact sequence six times. The sweep now measures that item and decoy every run in CI's image; the PR's Gate is the test. No game CSS changed (step 3 found nothing to fix), so no /updates/ line.
- **Next:** Gate green, merge with merge-pr.py, report main's run.
- **MERGED 23 Nov as 765ae37 (#889)**, route merge-pr.py. PR head 597d29c: check-site 45137452185 success, phone-fit-full 45137452271 success. Main on 765ae37: check-site 45139129589 success attempt 1, phone-fit-full 45139129106 success attempt 1, pages build 45139128202 success attempt 1. Contract moved. Closed out by WWIUT-BATCH-MERGE.

## 2026-11-22 (cloud): SITE-CONTRAST (`docs/history/contracts/2026-11-22-site-contrast.md`)

Claude Code (cloud), branch `claude/determined-gauss-3l7zyi` from main f176132. Tier Shared: stops at Gate green for Project Claude's review and Jon's "merge". First commit: #886's close-out (entry below), this contract saved.

- **Done on the branch:** `scripts/contrast_common.py`, the one contrast measurement (check-answer-count.py and check-teacher-invite.py import it); `scripts/check-contrast.py` over every game, start screen, first question and wrong-answer screen through measure-phone-fit.py's own `measure_one()` (a wrapped browser, the driver unedited), normal and Aa, 1366x768 and 390x844, self-test 19 plants; `scripts/contrast-state.json`; two more modes of phone-fit-full.yml's matrix (contrast-normal, contrast-aa); ci-deps.py rule 3 counts the contrast checker's files. 86 games' colour values fixed; 113 of 114 pass, Log Laws' Aa timer listed (STOP IF: a second split token).
- **Measured, not the lead:** 86 of 114 games failed on main (the contract's lead said about 45), 363 colour-on-background pairs; the copied Aa toggle (white on #0d9488, 3.74:1) alone in 77.
- **Decided for you:** the two older checks measure colours alone ({opacity: false}), so their findings equal main's; a literal is changed in its own rule (no game gains a hex outside :root); the Aa toggle's teal darkened, not its text; KaTeX's drawn maths is measured (its aria-hidden is for screen readers); text painted over by an opaque box is not measured; one new token in 6 games for a colour that is text on both a light and a dark surface; three default `.level-btn.active` fills no level shows left with dark text.
- **PR #887: Gate green** on 7429495 (main merged in for #885's /updates/ line): check-site 45085447273, phone-fit-full 45085447375 (contrast-normal 11m16s, contrast-aa 11m10s, every game), both success. **Next:** Project Claude's review and Jon's "merge". Reported, not done: four game verifiers keep their own contrast copies; the footer's links are unmeasurable (its scroll-cue gradients); Log Laws' Aa timer for Jon.
- **MERGED 23 Nov as 661f822 (#887)**, route: cloud (as PRIMARY-FIT-SWEEP's contract records it). Main on 661f822: check-site 45126347307 attempt 1 red (Sums in Disguise Stage 5, kids look: Next at 616 px against a 600 px fold, found by the verifier's sampled fold check; measured before schools/assets/fold.js laid the options two to a row (the old check's timing, not the game): not reproduced locally, and CI's own image passed every Sums in Disguise item and wrong option in #889's sweep), attempt 2 success (other items drawn); phone-fit-full 45126347538 success; pages build 45126346676 success. Contract moved. Closed out by PRIMARY-FIT-SWEEP, which fixes the sampled check and the overflow.

