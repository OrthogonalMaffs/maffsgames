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

## 2026-11-25 (cloud): MARVIN-LOG (MaffsCards' game_completed carries the winner and the tally in the Sheet's existing columns; `docs/handover/contracts/2026-11-25-marvin-log.md`)

Claude Code (cloud, lane 1), branch `claude/stoic-wright-o60xub` from main c7805e6. Merges on green with merge-pr.py (point 5). First commit: #909's close-out (in the TIER3-GUARD entry below) and this contract.

- **Done on the branch:** `games/maffscards/index.html`, game_completed keeps game_slug, level, mode, score, won and adds correct (the player won; false on a loss or a draw), questions_answered (G.round), questions_correct (G.wins.you) and detail `you N · Marvin N · ties N · win|loss|draw · <why>` (why is G.result.why: `ten`, `out` or `cap`). **Ties are counted, not subtracted:** the page had no tie count (G.mid empties when a round is won, so it cannot give the total), so a counter G.ties is added, incremented in the tie branch where the cards go to the middle pile; MC.ui.game() exposes it and the test hook MC.ui.rig takes it as an optional fifth argument. No new event, storage or look.
- **Verifier:** `scripts/verify-maffscards.py` gains check_completed: a won and a lost first-to-10 game, a first-to-10 game ended by cards running out, and entire-deck games drawn and won at the cap, each against the tally the test set up; the two played-by-clicks games against the script's own count of each reveal; won + lost + tied = rounds played. Three plants (correct true on a loss; questions_correct counting Marvin's wins; ties not counted, so the detail does not add up), ten in all. Docstring and ci-line say what game_completed carries.
- **Not changed:** privacy page (line 159, "Session completion and score data", already covers it); canon (it has no MaffsCards analytics text, so nothing added, per point 4); the endpoint, analytics.js, GA4. doPost writes correct, questions_answered, questions_correct and detail (docs/apps-script-endpoint.js 62-72); the live deployment was not inspectable from here.
- **Ran here:** Python playwright 1.63.0 installed (pip; requirements-ci.txt's esprima will not build here). verify-maffscards.py full run PASS in 2m17s, all ten plants caught (played: easy, you won 10-5, 5 tied; hard, Marvin won 10-6, 3 tied; balance easy 68.4%, hard 48.5%, unchanged by this work). check-level-logged and the personal-details and skip-CI word checks by hand: clean.
- **Next:** Gate and phone fit green, merge main in if it has moved (keep both lanes' entries), merge with merge-pr.py.

## 2026-11-25 (cloud): TIER3-GUARD (tier 3's answer-lock self-test in CI; two stale tier3_exceptions out; `docs/handover/contracts/2026-11-25-tier3-guard.md`)

Claude Code (cloud, lane 1), branch `claude/gracious-cori-62jzp2` from main d3a27af. Merges on green with merge-pr.py (point 4). Lane 2 runs BANKS-40 at the same time (#908); the only shared file is this one, so main is merged in before the merge. First commit: #907's close-out (in the MARVIN-BALANCE entry below) and this contract.

- **Done on the branch:** `.github/workflows/check-site.yml`, shard 1/4: "Tier 3 answer-lock self-test|python scripts/check-site.py --tier3-lock-selftest" after the KaTeX self-test (no timeout changed). `scripts/checker-allowlist.json`: the spot-the-muppet and expectation-station entries removed (7 left).
- **Checks run here:** the self-test on main as it stood: OK in 10 s (4 of 4 played; the plant caught). Guard proof on a local scratch branch, never pushed (`scratch/tier3-guard-proof`): with tier3()'s NO_LOCK_FRESH_INIT line deleted, the command exits 1, "FAILED: as tier 3 runs (the planted page was not played through)"; the edit reverted there after. Tier 3 without the entries: spot-the-muppet 4 PASS of 4 (40 questions); expectation-station 3 PASS, 1 WARN, 0 FAIL (the same WARN as #904: 0.8 twice on question 4), so step 2's exception does not apply.
- **How tier 3 ran here:** this container's network blocks cdn.jsdelivr.net and www.gstatic.com (Chromium got ERR_TUNNEL_CONNECTION_FAILED and tier 3 counted the console error as FAIL). A throwaway wrapper, never committed, ran check-site.py unchanged and answered locally any request its routes continued to an outside host: KaTeX 0.16.9 from scripts/fonts/ (bank_common._offline_answer), the two Firebase SDK files as an empty script (the leaderboard off), Google Fonts aborted. CI, with the network, is the authority.
- **Shard 1/4 time:** main 2b78900 (run 45581276557): the group 9m13s (KaTeX self-test 30 s, tier 3 513 s; 43 PASS, 0 FAIL, 51 UNSUPPORTED). The PR's figure is in the PR.
- **For Project Claude:** better-value's tier3_exceptions reason begins "Same shape as spot-the-muppet", whose entry is now gone; not touched (DO NOT TOUCH). Expectation-station's removed reason also said why its repeated tiles are legitimate; tier 3's WARN line says the same ("expected in a tile bank"), so nothing is lost from the output.
- **Merged main in (af77bc4, #908 BANKS-40 A) before the merge:** cloud.md conflicted (both lanes' entries), resolved by keeping both. #908 rebuilt Spot the Muppet's banks, so tier 3 ran again on the new page without its entry: 4 PASS of 4, 40 questions. The first Gate (head 5ad2666, before the merge, run 45590981250): green; shard 1/4 9m25s (answer-lock self-test 7 s; tier 3 517 s), tier 3 0 FAIL on all four shards (43, 54, 35 and 56 PASS).
- **Closed out (MARVIN-LOG's first commit):** #909 squash-merged as 419c531 through merge-pr.py; its last line `main 419c531 run 45597594977: GREEN`. Main's runs on 419c531, read back from the API: check-site 45597594977 success, phone-fit-full 45597595086 success, pages 45597594816 success. Contract moved to `docs/history/contracts/`.

