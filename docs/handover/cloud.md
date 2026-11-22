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

## 2026-11-22 (cloud): PHONE-FIT-CHANGED-GAMES (`docs/handover/contracts/2026-11-22-phone-fit-changed-games.md`)

Claude Code (cloud), branch `claude/funny-keller-2thbao` from main 67ade5e. First commit closes out #873 (SIX-PS-BANKS-9, entry below).

- **#871's branch (closed unmerged, duplicate of #872):** a deletion of `claude/ecstatic-thompson-f35dgo` failed in an earlier session. That session's command and its exact error reached neither this session nor any file (no unpushed note here), so neither is recorded. The branch stays on origin at a2a254f; no further attempts.
- Implemented (commit 2): measure-phone-fit `--only a,b`; ci-deps KNOWN_TOP + the tracked-folder self-test (planted) + `measured_pages()`; phone-fit-full on pull requests (shared: all; else the changed games; else nothing; per-PR concurrency); merge-pr (a'), the PR head's phone-fit run, waited for and never waived; AGENTS.md line; todo CI-DEPS-TOOLS and CI-DEPS-UGH-STATS to todo-done. Local: all three self-tests PASS, ci-groups --check and --worst-case PASS.
- Next: the PR's own phone-fit run (it changes .github/, so it measures every game), then step 7's one-game, docs-only and /class/ runs.

## 2026-11-21 (cloud): SIX-PS-BANKS-9 (`docs/history/contracts/2026-11-21-six-ps-banks-9.md`)

Claude Code (cloud), branch `claude/six-ps-banks-9` from main 90db64e. First commit closes out #869.

- **hcf-lcm: covered.** `schools/assets/hcf-lcm-gen.js` (MaffsHcfLcm: STAGES, makeRng, bank) builds 5 stages of 12 by enumerating every candidate, then a seeded shuffle; `topic_hcf_lcm` recomputes every answer from the stem with math.gcd/lcm (`check_hcf_lcm`) and every slip by its line (`six_ps_rules.hcf_slips`, rule c). Plant: the module's lcm() returning a x b, caught on every LCM item with HCF > 1. Topic band (2, 4) and the S3 cap LCM <= 2000 are my calls, for Jon.
- **expand-factorise: PARKED, STOP IF hit (SR-31).** MaffsHCFactor's named slips per item, stages 1-4 (bank of 40 each): stage 1 one slip (40/40); stage 2 one (40/40); stage 3 one (36), none (4); stage 4 two (38), one (2). No item has the 3 a four-option choice needs. **Question for Jon / Project Claude:** which of these? (a) allow a 3-option choice for this topic (validate() and the page take exactly 4 today: a page change, also a STOP); (b) add named slips to hc-factor-gen.js in its own contract (it is DO NOT TOUCH here); (c) leave expand-factorise coming soon. It stays in coming_soon meanwhile: todo row SIX-PS-EXPAND-FACTORISE.
- **Jon's ruling (22 Nov 2026, 06:45):** ship hcf-lcm on its own; expand-factorise stays coming soon (todo SIX-PS-EXPAND-FACTORISE) and will get its own bank-first generator with named slips, specced by Project Claude.
- Review sheet for Jon: https://claude.ai/artifact/8fRwR8zvx5MY52HGUiTYki (private to Jon), built by `gen-six-ps.py --only hcf-lcm --sheet`.
- **MERGED 22 Nov as 6310098 (#873)**, route merge-pr.py; main on the merge commit: check-site 44996163957 success, phone-fit-full 44996163909 success (its matrix skipped: no shared path), pages 44996163862 success. Contract moved to `docs/history/contracts/`. Closed out by PHONE-FIT-CHANGED-GAMES.

## 2026-11-21 (cloud): CI-DEPS-ANY-PAGE (`docs/history/contracts/2026-11-21-ci-deps-any-page.md`)

Claude Code (cloud), branch `claude/wonderful-knuth-jzdjsx` restarted from main edf8fb5. First commit closes out #867. **1b:** check-site-nav.py `--check` run 10 times in full: 10 of 10 PASS (15-17 s each), 0 failures; not reproduced, left. **1c:** canon §7.5 sentence. `scripts/ci-deps.py`: `always_reason()` (a declared header makes a page-less verifier selective; hazards still always); `any-page` token (served .html, schools/assets/, escape-rooms/assets/, data/, or any file a served page loads); a header pattern with `*` is a glob. Always-set 12 -> 2: merge-pr.py (no header, unchanged), test-escape-credit.py (hazard: feedback/index.html fetch(form.action), fetch(path)). any-page: check-download-labels.py, test-initials-overlay.py. Headers added: test-wait-settled, test-ga4-country, test-ga4-summary, check-context-size; check-lock-bank's list (batches 3-9, missing 10-13) is now `docs/lock-bank-batch*.txt`. Plants all caught. **MERGED 21 Nov as e291c9c (#869)**, route merge-pr.py; main check-site 44944770214 GREEN, phone-fit-full 44944770080 success (normal, aa, laptop), pages 44944770079 success. **Jon's ruling (21 Nov 2026, 20:03):** test-escape-credit.py stays always-run; the hazard rule is not changed for form posts; revisit only if the always-set fills again. Todo row CI-DEPS-ANY-PAGE moved to `docs/history/todo-done.md`. Closed out by SIX-PS-BANKS-9.

## 2026-11-21 (cloud): SITE-NAV-GUIDE-LABEL (`docs/history/contracts/2026-11-21-site-nav-guide-label.md`; Jon 14:55, "back to guide is fine")

Claude Code (cloud), branch `claude/wonderful-knuth-jzdjsx` restarted from main 528e4de. First commit closes out #864 (step 1's #862 close-out rode on #864, its red stop resolved there). **MERGED 21 Nov as 35cffc8 (#867)**, route merge-pr.py; main check-site 44939367340 GREEN, phone-fit-full 44939367354 success (normal, aa, laptop), pages 44939367009 success. Closed out by CI-DEPS-ANY-PAGE. site-nav.js HUBS: the 20 /parents/ labels are "the guide" ("← Back to the guide", stage-exit "← the guide"). check-site-nav.py: every distinct label opened as referrer on Angle Ace and Free Daily Pizza's stage-exit row at 360x640, one line by Range rects; all 10 fit, the 9 kept included. Plant: a 60-character label, caught. /updates/ line. Local note: the existing "stage" check failed once in a full local --check (row links []), passed 3 of 3 alone; untouched, CI decides.

## 2026-11-21 (cloud): PHONE-FIT-WAIT-NEXT (`docs/history/contracts/2026-11-21-phone-fit-wait-next.md`; Jon 16:24, "we fix them gradually, or nothing gets built")

Claude Code (cloud), branch `claude/wonderful-knuth-jzdjsx` from main 308dcf4. First commit closes out #862 (and notes #863). **MERGED 21 Nov as ffe56df (#864)**, route merge-pr.py; main check-site 44928833095 GREEN, phone-fit-full 44928833092 success, pages 44928832583 success. Closed out by SITE-NAV-GUIDE-LABEL. Then for the home lane: #865 had merged (a579740) before its branch run could be dispatched (422, branch deleted); main phone-fit-full 44930388209 on a579740: some-thingies PASS in normal, aa and laptop. `scripts/measure-phone-fit.py`: after a wrong answer and settle(), `wait_next()` samples every 100 ms; pure `next_point()` decides: a Next still for 500 ms (measured there), the option group changed (auto-advance, no Next), or NEXT_WAIT_MS = 6000. Self-test: pure plants and two Chromium pages (a Next 1.5 s late, 900 px down at 1280x720: one look misses it, the wait catches it; an auto-advance: no Next). **Branch run 44925427874 (all three modes) against main 44920568988:** normal trig-worms PASS (no Next) -> FAIL (Next below fold); aa trig-worms WARN (Aa at 320) -> FAIL; laptop trig-worms KNOWN FAIL -> HARD FAIL (Next 888), spot-the-error PASS (no Next) -> PASS; probability-paradox laptop HARD FAIL on both (Next 853). No game changed for any other reason; times 864->920, 863->905, 583->614 s (timeout 60 min). Both Nexts come after an animation, never an auto-advance. Listed: laptop probability-paradox and trig-worms "next" entries (state note); todo PHONE-FIT-NEXT-FOLD. docs/phone-fit-report.md not regenerated: the workflow does not write it.

