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

## 2026-11-21 (cloud): ANSWER-LOCK-SELFTEST-SPLIT, STOPPED (`docs/handover/contracts/2026-11-21-answer-lock-selftest-split.md`; Project Claude 20 Nov, 23:33)

Agent Claude Code (cloud), branch `claude/affectionate-carson-k1bg8h` from main 03d1f74. Tier Small (CI). No PR.
**Close-out carried (first commit, 11c7baf):** #857 LARGE-SCREEN-PILOT parked, recorded in its entry below (check-site 44825525834 success on attempt 2, phone-fit-full 44825525844, pages 44825525170). Its contract stays in contracts/ (parked; todo LARGE-SCREEN-LAYER points to it).
**Done on the branch (second commit), not merged:** `scripts/check-answer-lock.py`: the seven self-test plays are work units ("selftest: <plant>", SELFTEST_PLAYS) inside the existing "Answer lock in play" ci-shards header (one header per script is all ci-groups allows, and units and overhead are keyed by script); a --shard part plays its self-test units after its games, each timed at wall time. The static line is `--selftest --static && --static` (no plays); a plain `--selftest` still plays all seven. New assertion `selftest_unit_faults()`: dealt into the pack's parts and 1-12, the self-test units are exactly the plays; dropped, doubled and unknown plants CAUGHT. `layout_errors()` updated. `--selftest --static` PASS. Timings and pack not seeded.
**Measured locally (Chromium 1.63, all seven CAUGHT or clean as before), seconds:** decimal-detective without the lock 193.2; angle-ace bare show() 48.8; binomial-blaster as it is 5.0, wrong path on a timer 5.9, self-advancing Next 5.8; trig-identity-duel dead network 35.5, old KaTeX route 4.6; total 298.7.
**STOP:** the decimal-detective plant cannot fit any part. Part cap with today's 26 s setup is 210 s (SHARD_TARGET x 315 - setup); 186 s with 50 s. Its 193 s plus the script's part overhead (53 s) is 246 s, so `choose_parts()` finds no k and falls back to one part per unit: 117 Answer lock lines. Its time is the driver's tap-through phase: 2,241 answers into a game that never finishes, caught only at the end ("game_completed 0 time(s)"). This is the contract's first STOP IF in substance (the play needs shortening inside itself). Next step waits for Jon.

## 2026-11-20 (cloud): LARGE-SCREEN-PILOT, PARKED (`docs/handover/contracts/2026-11-20-large-screen-pilot.md`, Amendment 1; Project Claude 20 Nov, two parts)

Agent Claude Code (cloud), branch `claude/youthful-fermi-ujam6l` from main 2e7c9d2; this PR from `claude/large-screen-park`. Tier Medium.
**Close-outs carried (first commit, cherry-picked from 4e90390):** #854 FORGE-SUBJECT-PROMPT, recorded in its entry below (check-site 44807672164, phone-fit-full 44807672235, pages 44807671441, all success); its todo row moved word for word to `docs/history/todo-done.md`. The "Cloud lane owns" paragraph replaced by Jon's scope paragraph of 20 Nov.
**Stopped at STOP IF, then parked (Jon, 20 Nov, 21:34: "option 2, PARK"; none of (a), (b), (c)).** The layer stays on `claude/youthful-fermi-ujam6l` @ 63b758c, unmerged: `schools/assets/large-screen.css`, `scripts/apply-large-screen.py`, `scripts/check-large-screen.py` (PASS, five plants caught), the six pilot games linked. Nothing of it is on main. The fix and re-pilot: todo LARGE-SCREEN-LAYER.
**Steps, tuned to the rule (min-width / zoom >= 1200, min-height / zoom >= 760, nothing below 1500x880):** 1.15 from 1500x880, 1.25 from 1500x950 (1920x955 gets 1536x764), 1.4 from 1680x1064, 1.6 from 1920x1216 (2560x1310 gets 1600x819). The starting values broke it: 1.25 at 1500x880 leaves 704 px; 1.6 at 2200x1200 leaves 750. vh is zoomed too (100vh measured 1193.75 px on a 955 px viewport at 1.25), so the layer divides the body's min-height back by the step.
**Measured** (Chromium 157, real fonts; layer on against off at the same viewport):
| Game | Result |
|---|---|
| core-maths-paper1 | Next below the fold because of zoom on Q2, 4, 15, 26, 36 at 1920x955 (82-215 px; Q4's options too) and those and Q12 at 2560x1310 (17-450 px). Its chart questions need about 1,050 px. At 1366x650 (no zoom) already over on 15 questions. |
| surd-simplifier | Next 12-60 px below the fold on 25 of 100 items at 1920x955, all fitting with the layer off; none at 2560x1310. Its working card opens by `(min-width:760px) and (min-height:860px)` (:80), which reads 955 while layout has 764. |
| negative-number-line | Order Them's touch ghost tile 233 px off the finger at 1920x955, 746 px at 2560x1310, 0 at 1366x650 (`style.left/top = clientX/clientY`, :764-765); the drop lands right. Mouse input exact. |
| maffscards, factor-race, bearing-blitz | Next above the fold at every size (maffscards over 17-24 rounds); canvas clicks and drag 0 degrees out. factor-race's Start is 167 px below the fold with the layer at 1920x955 (60 px above without). |
No page scrolls sideways at any size; zoom is 1 at 1366x650 and at 320x568, 375x667, 390x844.
**Todo rows added:** LARGE-SCREEN-LAYER, START-SIDEWAYS-GATE, PERCENTILE-LOWER-IS-BETTER. No canon §7.5.8 or SR-34 (parked); no LARGE-SCREEN-ROLLOUT row (LARGE-SCREEN-LAYER replaces it). No /updates/ line.
**Correction to Amendment 1's root cause, measured:** scroll.js:42 compares `innerHeight` with `getBoundingClientRect`, and in the pilot's probe both were visual px under zoom (innerHeight 955, rects scaled 1.25), so that comparison is consistent; its scroll units were not measured. The row says so.

**MERGED 20 Nov as ce6308c (#857)** at 22:02:21 UTC (head 7c4d555), route merge-pr.py. Main on the merge commit, read from the API by ANSWER-LOCK-SELFTEST-SPLIT: check-site 44825525834 success on attempt 2 (attempt 1 failed at checkout in Content verifiers 60 and Answer lock L1, the network to github.com: a flake, one rerun), phone-fit-full 44825525844 success, pages build and deployment 44825525170 success. Closed out by ANSWER-LOCK-SELFTEST-SPLIT's first commit. The contract stays in `docs/handover/contracts/`: the pilot is parked, not done, and todo row LARGE-SCREEN-LAYER points to it (AGENTS.md: stopped work is pointed to by a row).

## 2026-11-20 (cloud): FORGE-SUBJECT-PROMPT (`docs/handover/contracts/2026-11-20-forge-subject-prompt.md`; Project Claude 20 Nov, one part)

Agent Claude Code (cloud), branch `claude/dreamy-knuth-e94w15` from main c46eb14. Tier Small. Root cause matched on c46eb14 (:64-65 the target's style, :475-477 the dead `<strong>` line, :478-480 the three spans, :141-148 no paper line).
**Close-outs carried (first commit, 750aa98):** #852 52DLE-TIDY, recorded in its entry below (check-site 44759669255, phone-fit-full 44759669240, pages 44759668147, all success).
Done on the branch: `games/formula-forge/index.html`: the dead innerHTML line and its comment deleted (`tEl` kept, the clear kept); the subject span has class `subject-chip`, styled exactly as the contract gives it; "Powers and Multi: have paper handy." as a `menu-info` after the stage previews. `verify-formula-forge.py`: the first question at gcse, alevel and level4 has one `.subject-chip` whose KaTeX annotation is the subject; the start screen shows the line. PASS, all 12 plants caught (new: class removed, line removed). No /updates/ line.
**Measured (all 56 items, branch against main, Chromium):** the chip never leaves "Make" and nothing overflows sideways. **At 375x667 Aa (6 items) and 390x844 Aa (2), the target line now wraps "Make [chip] the / subject"; on main every item fits on one line there.** At 320x568 Aa every item already wrapped on main the same way, so the 320 STOP IF cannot see the case it guards; I read it as applying at 375 and 390 too, and **the merge is held for Jon**. The items: gcse s1 #10 (M); level4 s1 #3 (ΔL), #4 (W), s2 #4 (ΔT), #5 (P_in), s4 #1 (R₁); at 390 only ΔL and ΔT. Normal mode: one line at every size.
**Amendment 1 (Jon, 20 Nov, ruling (b)):** the end span is " the" + U+00A0 + "subject" (written `\u00a0` in the JS, so the source stays ASCII); the chip's styling unchanged. Verifier: the end span's text exactly that at each level; new plant (an ordinary space back) caught; PASS, all 13 plants caught. Re-measured all 56 items at 320x568, 375x667 and 390x844, normal and Aa: "the" and "subject" always share a line, the chip never leaves "Make", no sideways overflow; "Make [chip]" / "the subject" on 56 items at 320 Aa, 6 at 375 Aa, 2 at 390 Aa (accepted by the ruling); normal mode one line. Merge released.
The start screen is 490 px wide in Aa at every phone size on main and the branch alike (the stage-preview grid): pre-existing, not touched.

**MERGED 20 Nov as bf019be (#854)** at 20:02:12 UTC (head a68f4f7), route merge-pr.py. Main on the merge commit, read from the API by LARGE-SCREEN-PILOT: check-site 44807672164 success, phone-fit-full 44807672235 success (both push), pages build and deployment 44807671441 success. Closed out by LARGE-SCREEN-PILOT's first commit; contract moved to `docs/history/contracts/`; todo row FORGE-SUBJECT-PROMPT moved word for word to `docs/history/todo-done.md`.

