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

## 2026-11-22 (cloud): GIVEN-THAT-FIT-WHY (`docs/handover/contracts/2026-11-22-given-that-fit-why.md`)

Claude Code (cloud), branch `ccr-bcba17c0-u8yhyf` from main e12f99a. First commit: the close-outs of #876 (CC-TRIG-SLIP, entry below) and #875's live proof so far (PHONE-FIT-CHANGED-GAMES, entry below), the contract saved, given-that claimed in `scripts/answer-lock-state.json` (the contract's step 1: claim in the same commit). No other merged contract was left in `docs/handover/contracts/` (the other five are unstarted or parked work, each with a todo row).

- Baseline (local, this sandbox, the driver without its footer pre-check, which reads 811/810 at 810px here only): normal 320x568 last option 743/528, 375x667 777/627; Aa 320x568 options start 637/528, 375x667 last option 867/627, 390x844 876/804; laptop last option 746 and Next 851, against folds 728 and 680. The nine listed entries, exactly.
- Next: the layout and the Why card.

## 2026-11-22 (cloud): CC-TRIG-SLIP and PHONE-FIT-DOCS (`docs/history/contracts/2026-11-22-cc-trig-slip.md`)

Claude Code (cloud), branch `claude/funny-keller-2thbao` restarted from main 1ecc4d2. **Lane: the contract says home; Jon's one-off exception (22 Nov 2026, in this session): the cloud lane does it, its entry here, both close-outs in its first commit.** First commit closes out #875 (entry below) and the home lane's #874.

- **#874 (COMPLEX-CONVERTER-WHY), closed out here:** MERGED 22 Nov as 842aa2e, route merge-pr.py (the contract's statement; home.md's entry has no MERGED line). Main on 842aa2e: check-site 45002104858 success, phone-fit-full 45002104942 success (the old workflow: no shared path, matrix skipped), pages 45002104429 success. Contract moved to `docs/history/contracts/2026-11-22-complex-converter-why.md`. Its home.md entry is left as it is (cloud does not edit home.md).
- **r slip (`r_part`):** `slip()` names it only where no other family fits (so no option #874 named changes), when each part of a Cartesian pick is right or equals ±r or ±r/2 with the right part's sign, one at least wrong. The line repeats the card's own Re and Im working lines: "Re and Im aren't r: Re = r cos θ = 6cos(45°) = 3√2, Im = r sin θ = 6sin(45°) = 3√2." (my call from step 3's template; Jon may reword). The verifier's `slip_of()` mirrors it independently: 15 named (q3, q9, q10, q12 x2, q17 x3, q18 x3, q22, q32, q33, q41, the contract's list exactly), every #874 count unchanged, unnamed 61 -> 46. New plant (q5's 3.5 + 3.5j named) caught, 12 of 12; a live q17 6 + 6j check at level4 (j) and further (i); against main's page all 15 and both live checks fail.
- **Docs:** canon.md "The full run" (§7.6.1) rewritten for #875's three triggers; one more stale trigger line found and fixed, canon.md:1333 ("not yet in CI"); check-start-back-link.py's docstring. Seen, not changed (not a trigger): canon.md:1330-1331 says Next below the fold and sideways scroll are "reported, not gated", against measure-phone-fit.py's "two gates".
- Next: the PR's own phone-fit run (predicted complex-converter only) as #875's first live one-game proof (PHONE-FIT-CHANGED-GAMES Amendment 1.4).
- **MERGED 22 Nov as 2107eef (#876)**, route merge-pr.py. Main on 2107eef: check-site 45009566057 success, phone-fit-full 45009566045 success (complex-converter only: normal, aa, laptop), pages 45009565576 success. The PR's own phone-fit run 45008584432 (head 4b87bf7) measured complex-converter only in normal, Aa and laptop, 1m38s (09:39:15 to 09:40:51), success. Contract moved to `docs/history/contracts/`. Closed out by GIVEN-THAT-FIT-WHY.

## 2026-11-22 (cloud): PHONE-FIT-CHANGED-GAMES (`docs/history/contracts/2026-11-22-phone-fit-changed-games.md`)

Claude Code (cloud), branch `claude/funny-keller-2thbao` from main 67ade5e. First commit closes out #873 (SIX-PS-BANKS-9, entry below).

- **#871's branch (closed unmerged, duplicate of #872):** a deletion of `claude/ecstatic-thompson-f35dgo` failed in an earlier session. That session's command and its exact error reached neither this session nor any file (no unpushed note here), so neither is recorded. The branch stays on origin at a2a254f; no further attempts.
- Implemented (commit 2): measure-phone-fit `--only a,b`; ci-deps KNOWN_TOP + the tracked-folder self-test (planted) + `measured_pages()`; phone-fit-full on pull requests (shared: all; else the changed games; else nothing; per-PR concurrency); merge-pr (a'), the PR head's phone-fit run, waited for and never waived; AGENTS.md line; todo CI-DEPS-TOOLS and CI-DEPS-UGH-STATS to todo-done. Local: all three self-tests PASS, ci-groups --check and --worst-case PASS.
- PR #875. Its own phone-fit run (45001991098) diffed exactly its own files and chose every game (shared paths: the workflow, ci-deps.py, measure-phone-fit.py), so step 7 cannot be shown on it. **Amendment 1 (Jon, 22 Nov):** no throwaway branches; step 7 simulated locally (the changed job's Python, extracted from the yml, against local commits in a scratch clone: one game -> split-it; docs-only and /class/ -> nothing, not shared; output in the PR) and merge-pr's self-test; merge on green; step 7 recorded as "simulated locally; live proof pending".
- **Owed in the close-out (Amendment 1.4):** the first real one-game PR, docs-only PR and /class/ PR after the merge, each one's phone-fit run ID and what it measured. If any selects wrongly, STOP and report before other work.
- **Live proof so far (closed out by GIVEN-THAT-FIT-WHY):** one-game, from #876: PR run 45008584432 measured complex-converter only in normal, Aa and laptop (1m38s), success; push run 45009566045 on 2107eef the same, success. Selected correctly. **Still owed to a later close-out:** a docs-only PR and a /class/ PR.
- **MERGED 22 Nov as e5aa98a (#875)**, route merge-pr.py (its new phone-fit check judged run 45002445020 on head 3d64abd, green), exit 0, last line "main e5aa98a run 45004673420: GREEN". Main on e5aa98a: check-site 45004673420 success, phone-fit-full 45004673440 success (shared paths, so every game: normal, aa, laptop), pages 45004673258 success. Contract moved to `docs/history/contracts/`. Closed out by CC-TRIG-SLIP.
Record: agent Claude Code; wall about 1:20 (start not timed exactly); review cycles 0; amendments 1; usage n/a.

## 2026-11-21 (cloud): SIX-PS-BANKS-9 (`docs/history/contracts/2026-11-21-six-ps-banks-9.md`)

Claude Code (cloud), branch `claude/six-ps-banks-9` from main 90db64e. First commit closes out #869.

- **hcf-lcm: covered.** `schools/assets/hcf-lcm-gen.js` (MaffsHcfLcm: STAGES, makeRng, bank) builds 5 stages of 12 by enumerating every candidate, then a seeded shuffle; `topic_hcf_lcm` recomputes every answer from the stem with math.gcd/lcm (`check_hcf_lcm`) and every slip by its line (`six_ps_rules.hcf_slips`, rule c). Plant: the module's lcm() returning a x b, caught on every LCM item with HCF > 1. Topic band (2, 4) and the S3 cap LCM <= 2000 are my calls, for Jon.
- **expand-factorise: PARKED, STOP IF hit (SR-31).** MaffsHCFactor's named slips per item, stages 1-4 (bank of 40 each): stage 1 one slip (40/40); stage 2 one (40/40); stage 3 one (36), none (4); stage 4 two (38), one (2). No item has the 3 a four-option choice needs. **Question for Jon / Project Claude:** which of these? (a) allow a 3-option choice for this topic (validate() and the page take exactly 4 today: a page change, also a STOP); (b) add named slips to hc-factor-gen.js in its own contract (it is DO NOT TOUCH here); (c) leave expand-factorise coming soon. It stays in coming_soon meanwhile: todo row SIX-PS-EXPAND-FACTORISE.
- **Jon's ruling (22 Nov 2026, 06:45):** ship hcf-lcm on its own; expand-factorise stays coming soon (todo SIX-PS-EXPAND-FACTORISE) and will get its own bank-first generator with named slips, specced by Project Claude.
- Review sheet for Jon: https://claude.ai/artifact/8fRwR8zvx5MY52HGUiTYki (private to Jon), built by `gen-six-ps.py --only hcf-lcm --sheet`.
- **MERGED 22 Nov as 6310098 (#873)**, route merge-pr.py; main on the merge commit: check-site 44996163957 success, phone-fit-full 44996163909 success (its matrix skipped: no shared path), pages 44996163862 success. Contract moved to `docs/history/contracts/`. Closed out by PHONE-FIT-CHANGED-GAMES.

