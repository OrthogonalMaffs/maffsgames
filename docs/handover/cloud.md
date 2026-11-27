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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (25 Nov):** main run 45574813288 on 8840795 (#906) red only in Content verifiers 26: unit-converter t4-003 (?level=level4, 'e': False); failed jobs rerun once, attempt 2 GREEN. **Flake (14 Nov):** main run 43590939932 on 6f37c69 (#760) red only in Answer lock L7: trig-identity-duel, `Page.goto: Timeout 20000ms exceeded` loading the page from the runner's own server (the merge touched no game, shared asset or checker; the job passed on the PR head); failed jobs rerun once, attempt 2 GREEN. **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk's random phone-fit reds (375x667 Aa, 320x568 normal) are fixed by TAKE-A-WALK-SEED** (no seed reads the clock; the Gate's clock-seed scan); its layout is todo row TAKE-A-WALK-PHONE-LAYOUT. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

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

## 2026-11-27 (cloud): PINNED-LIVE-DATA (the stub server answers the files bots rewrite on main with fixed bodies, so no check's colour moves with Jon's play or the nightly counts; `docs/handover/contracts/2026-11-27-pinned-live-data.md`)

Claude Code (cloud), branch `claude/admiring-faraday-c7alrl` from main b8ab511. Shared tier (stop at green for Project Claude's review and Jon's "merge").
- **Close-out, D-BY-DX-SIGN-LINE:** [#934](https://github.com/OrthogonalMaffs/maffsgames/pull/934) squash-merged as f6c0809 by merge-pr.py on a green Gate at 4730844 (check-site 46007737308, phone-fit-full 46007737275); merge-pr.py's last line "main f6c0809 run 46010247971: GREEN". Main's runs on f6c0809: check-site 46010247971, phone-fit-full 46010247561, pages 46010246665, each success (read back from GitHub Actions in this session). Contract moved to `docs/history/contracts/`.
- **The pin (`scripts/serve-stubbed.py` BOT_WRITTEN, Amendment 1):** all 12 workflow-staged paths listed. Pinned, with or without a query string: `daily.json` (not played; owner verify-maffscards.py), `answer-counts.json` (as_of now, total 0, no games; owners check-answer-count.py, check-ugh-stats.py), `ugh-stats.json` (one day, every count 0: an all-zero chart, Project Claude's ruling; owner check-ugh-stats.py). The other nine: never read by a page.
- **Opt-out:** `--committed` / `MAFFS_STUB_COMMITTED=1` via `start_stub_server(committed=True)`; check-ugh-stats.py's one server takes it (its QUIZ unit too, accepted).
- **Guard:** `serve-stubbed.py --selftest` (its own `# ci-line`), five plants caught.
- **ci-deps (Amendment 1 step 4):** a module whose header holds `# ci-deps-literals: none` gives its file, never its literals; serve-stubbed.py declares it, so no table path is a phone-fit input. The stop report said ten paths newly shared: it was seven (daily.json, ugh-stats.json, REGISTER.md, both handovers and archives); answer-counts.json and the ci-*.json were already shared.
- **Next:** the PR and the Gate; at green stop for Project Claude's review and Jon's "merge".

## 2026-11-27 (cloud): D-BY-DX-SIGN-LINE (d by dx? Why?'s placeholder sign_lost line reworded so it holds on s2-06, where the number in front is negative; `docs/handover/contracts/2026-11-27-d-by-dx-sign-line.md`)

Claude Code (cloud), branch `claude/funny-hamilton-900869` restarted from main 99a8e30. Medium tier (merge on green). One commit: the close-out below, the contract verbatim and the line.
- **Close-out, D-BY-DX-BUILD:** [#933](https://github.com/OrthogonalMaffs/maffsgames/pull/933) squash-merged as 024e9ae by merge-pr.py on a green Gate at 41029c4 (check-site 45909502642, phone-fit-full 45909502704). Main's runs on 024e9ae: check-site 45911763308, phone-fit-full 45911763285, pages 45911762690, each success. merge-pr.py's last line: not captured; main's result read from GitHub Actions (that session's first watch hit a 10-minute limit and the script refuses to re-watch a merged PR). Contract moved to `docs/history/contracts/`. end-task.py not run (it refuses in cloud sessions).
- **The line:** `LINES.sign_lost` in `games/d-by-dx-why/index.html` is now "The power is negative, so its minus comes down with it: 3 × -2 = -6, but -2 × -3 = +6." (× is U+00D7, the minuses ASCII hyphens). Nothing else in the page, the bank or the verifier changed; the bank's SHA-256 is a8ecdc05...428a14e.
- **For Jon:** every sign_lost line you write must hold for a negative number in front too: on s2-06 (-2/t^3) the answer is +6t^-4 and the wrong option is the one with the minus.
- **Next:** the Gate; merge on green; main's runs recorded by the next cloud task's close-out.

Record: agent Claude Code; wall n/a until hand-off; review cycles 0; amendments 0; usage n/a.

## 2026-11-26 (cloud): D-BY-DX-BUILD ("d by dx? Why?", Jon's Level 3 differentiation game, five stages from a fixed 60-item bank, a Pro switch that hides the derivative table; merges unlisted; `docs/handover/contracts/2026-11-26-d-by-dx-build.md`)

Claude Code (cloud), branch `claude/funny-hamilton-900869` from main 60fb649. Medium tier (merge on green). The first commit is the two close-outs below and the contract, verbatim.
- **Close-out, BASE-60-CUCKOO:** [#929](https://github.com/OrthogonalMaffs/maffsgames/pull/929) merged as 54d13e6, route merge-pr.py. Main's runs on 54d13e6, read from GitHub Actions by this session: check-site 45875526978, phone-fit-full 45875526946, pages 45875526100, each success (attempt 1). merge-pr.py's last line is its report of that check-site run (`main 54d13e6 run 45875526978: GREEN`, rebuilt here from the run: this session did not see the command's output). Contract moved to `docs/history/contracts/`.
- **Close-out, SOME-THINGIES-HOST:** [#931](https://github.com/OrthogonalMaffs/maffsgames/pull/931) merged as 9f51bb8, route merge-pr.py. Main's runs on 9f51bb8, read the same way: check-site 45888635200, phone-fit-full 45888635189, pages 45888634578, each success (attempt 1); last line `main 9f51bb8 run 45888635200: GREEN`, rebuilt the same way. Contract moved to `docs/history/contracts/`.
- **Bank:** `tools/d-by-dx-why/bank.py` saved verbatim; it prints total 60 and sha256 a8ecdc05...428a14e, the contract's. Embedded one item a line.
- **Page (`games/d-by-dx-why/`):** Base 60's structure on CAST Away's dark theme, a violet accent (a placeholder: the look is Jon's). The Pro switch is a button above the stages, in memory only. The table is the shared reference card: its own column beside the question from 1024 px (open), the closed "Derivative table" button under the options on anything narrower (canon §7.6.2); in Pro the element is not in the page. A wrong answer's rows are pairs of cells on one line under "From the table:", and lit in the open table until Next.
- **Decided here (for Jon):** (1) while a wrong answer shows, the two spare options go on any screen narrower than 1024 px or 660 px tall or less; a laptop keeps all four. (2) An option's tick or cross sits in its corner and an expression never breaks across lines: `3+14t-8` wrapped inside its option at 320 px. (3) Aa on a phone and any screen 640 px tall or less get closer line spacing in the feedback, same text, same size. (4) The stage cards' one-line descriptions and the line under the Pro switch are mine, placeholders. (5) games.json: search phrase "Differentiation" (the title rule adds "Game" and the level), description cut to fit 155 characters.
- **For Project Claude:** `sign_lost`'s line ("...bringing it down gives a minus") is shown on s2-06, where the question is -2/t^3 and the answer is +6t^-4: the decoy is -6t^-4, so the line reads backwards for that one item. The bank and line are as the contract gives them; not changed.
- **Verifier:** bank (sympy differentiates every question; every decoy from its err key; TeX, prompt, rows and working rebuilt), KaTeX (527 strings), play at 375x667 and 1280x720 (ten runs each), fit at the four sizes in normal and Aa plus 320x568 normal (canon §7.6.1; beyond the contract), with the table and in Pro: 18 units, 3,240 screens. Eight plants caught. Local figures (CI's are the record): least room under Next 21 px (375x667 Aa, s5-08), 18 px (320x568), 63 px (1280x720 Aa).
- **Not measured by the shared driver:** `measure-phone-fit.py` cannot press the Pro switch; Pro is covered by the verifier's fit units, every item.
- **Gate, first two runs (PR #933):** check-site 45903464919 on 0092bf2 red only in Content verifiers 113: the 320x568 units 1 px over on s5-08 and s5-12 (CI's text font runs about 18 px taller there than the container's; the contract's sizes passed, least room 21 px at 375x667 Aa), and the verifier took 6m21s of a 6m line (now three parts). Fix 1 (f5b07f8) squeezed short screens and made the HUD shorter than its 44 px exit controls: check-site 45906689551 red only in Content verifiers 25, Stage exit, the controls 10 px above the viewport at 320x568 (my regression; the verifier's own units passed, 20 px at 320x568). Fix 2: the HUD stays 44 px tall, and on a screen 600 px tall or less the table rows sit below Next (canon §7.6.1's fixed rule; visual order only), so 320x568 has 67 px locally. The contract's four sizes are unchanged.
- **Next:** the Gate; merge on green; main's runs recorded here.

