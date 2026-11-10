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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk can turn main's phone-fit-full red at random (Aa, 375x667) until its fix merges** (cause in the CAST-AWAY-LIST entry below). **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

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

**Standing ruling, merge route (Jon, 10 Nov 2026, 07:58; recorded verbatim, contract CAST-AWAY-BUILD's first commit):**
> STANDING RULING (Jon, Tue 10 Nov 2026, approved 07:58): merge route when merge-pr.py cannot authenticate.
> Applies to any session, either lane, in which `gh auth status` fails (record its output in the report). It changes the ROUTE only, never the authorisation: a PR still merges only when its contract allows it (Jon's "merge", or a standing authorisation already in force).
> Before merging, the session itself checks and reports what merge-pr.py would: (1) the PR's Gate is green on its current head SHA; (2) the PR is mergeable with no conflicts; (3) main's newest full run is green, and nothing has landed on main since that run other than the bot's own "[skip ci]" record commits (timings, answer counts, REGISTER.md), with no run on main queued or in progress. Any failure: STOP.
> Then squash-merge through the GitHub connection pinned to that head SHA (refuse if it has moved), with the message as merge-pr.py would write it (the PR body, any "[skip ci]" disarmed to "(skip ci)"); watch main's run on the merge commit and report its result, as merge-pr.py --watch would.
> Record each use in the PR's close-out: "Merged via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: <output>)".
> merge-pr.py remains the first route wherever it authenticates. This ruling expires when todo row CLOUD-MERGE-TOKEN closes, or on Tue 24 Nov 2026, whichever is first. Record it verbatim in docs/handover/cloud.md's standing rules in this contract's first commit.

**Standing rule, close-outs (Jon, 10 Nov 2026, 13:13; recorded verbatim, CUMFREQ-CURVE's preamble):**
> STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
> A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.

**Merges by the standing route (Jon's ruling of 10 Nov):** the merge message is the PR body word for word, as merge-pr.py writes it (with its skip markers disarmed). #724's was a condensed form; recorded in its close-out.

## 2026-11-10 (cloud): CUMFREQ-CURVE (`docs/history/contracts/2026-11-10-cumfreq-curve.md`, Small–Medium, Amendment 1, todo row 1.17)

DONE, merged and live: [#725](https://github.com/OrthogonalMaffs/maffsgames/pull/725) merged as 7c34308 on Jon's "merge" (10 Nov; /updates/ line confirmed as written), via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: `github.com` / `X Failed to log in to github.com using token (GH_TOKEN)` / `- Active account: true` / `- The token in GH_TOKEN is invalid.`, exit 1), the message the PR body word for word (checked against it); Gate check-site 42839784197 green on 4efe2d2 (89 jobs: 87 passed, 2 main-only skipped). Main on 7c34308: check-site 42848490044 green (89 of 89 jobs), phone-fit-full 42848490292 green. Close-out carried by CAST-AWAY-DIAGNOSE's first commit after its claim. Branch `claude/zealous-albattani-hmm0un`: claim a21fca2; #723 close-out and the close-out rule d1b2757; STOP report 7a82ff4; origin/main merged in 3bcfd34 (Amendment 1 item 0); #724 close-out eab5d51. Chart Interrogator's cumulative frequency curve is a monotone cubic Hermite (Fritsch–Carlson), one Bezier per class, in the level's accent read from the computed `--accent`; CF5's data changed on Jon's ruling (median band no longer ±0.34). The four keys that moved past their band (CF4 Q3, CF5 median, CF6 Q1, CF10 Q3) were accepted by Jon; no comparator verdict changed. `verify-chart-interrogator.py` rebuilds the curve from its rule and checks (a)–(e); three new planted faults each fail their own check; CF_PIXEL re-measured. verify-chart-drawings and verify-feedback-teaches-charts pass and pin nothing of the curve. Claim released; todo 1.17 closed to todo-done.md; /updates/ line for Jon to confirm. Discovery: at 375 px the game's page is 409 px wide (34 px sideways scroll), on main too; not in this contract.

## 2026-11-10 (cloud): CAST-AWAY-LIST (`docs/history/contracts/2026-11-10-cast-away-list.md`, Small)

DONE, merged and live: [#724](https://github.com/OrthogonalMaffs/maffsgames/pull/724), branch `claude/cast-away-list` from main d0a00f2, Gate check-site 42831239219 green on cce89f3 (89 jobs: 87 passed, 2 main-only skipped). CAST Away listed: noindex and the UNLISTED comment off the page; an A-Level card with the New badge (2026-11-10), last in the section by roster number; sitemap; spec map A-Level E1–E7; hub row with four stage boards, and `cast-away` taken off `NOT_ON_HUB`; roster row #110 moved to A-Level Games with "Look signed off by Jon, 2026-11-10." (its "|k| > 1" rewritten as "k > 1 or k < −1": the pipe split the table into 11 cells, so check-look-signoff could not read the row once it was listed); /updates/ line. CUMFREQ-CURVE stays stopped, branch untouched (a21fca2, d1b2757, 7a82ff4). Under the close-out rule (Jon, 10 Nov, 13:13), this PR's close-out is carried by CUMFREQ-CURVE's first commit after its branch took main.

Approval and exception (Jon, Tue 10 Nov 2026), verbatim:
> - Listing approved: 13:35 "yes I'd like both CAST away and whose side are you on to be listed if possible please"; 13:43 "Cast away now. My students learned this skill today." Whose Side is NOT in this contract (it waits for STAGE-EXIT-LABEL).
> - Look sign-off: Jon played CAST Away on 10 Nov 2026 and approved it.
> - LANE EXCEPTION, granted 13:46 ("yes I do"), for this contract only: AGENTS.md gives listing to the home lane and cloud.md says "Relisting a fixed game is the home lane's docs PR". Jon has no home-lane access today, so the cloud lane lists CAST Away, and may edit ONLY these files, for cast-away only: games/cast-away/index.html (lines 6–7), index.html, sitemap.xml, spec-map/index.html, leaderboards/index.html, scripts/check-leaderboard-coverage.js (the cast-away entry in NOT_ON_HUB only), .claude/rules/game-roster.md (CAST Away's row, the Unlisted note about it, the two section counts), updates/index.html, plus this lane's own docs/handover/cloud.md and the contract file. One lane still: this session, one task at a time. The exception ends when this PR merges.
> - Merge: this PR merges once its Gate is green, under the cloud lane's standing authorisation (10 Oct); Jon's listing approval above is the "merge". Merge route: merge-pr.py, or the standing merge-route ruling of 10 Nov if gh auth fails (record its output).

Merged as 5630720 via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: `github.com` / `X Failed to log in to github.com using token (GH_TOKEN)` / `- Active account: true` / `- The token in GH_TOKEN is invalid.`, exit 1), after checking the Gate green on cce89f3, the PR mergeable (clean), and main green with only bot "[skip ci]" commits since and no run queued or in progress. The commit message was a condensed form of the PR body, not the body word for word as merge-pr.py writes it; both skip markers were disarmed. Main on 5630720: check-site 42833737308 green (89 of 89 jobs); phone-fit-full 42833737342 red on attempt 1, aa mode only: `GATE HARD FAIL: take-a-walk: below the fold, not on the known-failures list: 375x667 (last option 677 / 627)`; #724 did not touch take-a-walk. Failed jobs rerun once (AGENTS.md): attempt 2 green in every mode. Cause: a content-dependent take-a-walk layout fault (Aa, 375x667): a long generated question pushes the last option below the fold. It surfaced at random because `H.newSeed` (`games/take-a-walk/index.html:327`) mixes `Date.now()` into its seed, which escapes PHONE_SEED (canon §7.8.4; todo GATE-STEP-4); the rerun drew shorter questions. Locally take-a-walk read 599 / 627 at 375x667 in Aa three times out of three, while its 320x568 reading varied with the question drawn (726, 694, 668). Discovery for a todo row (home lane): take-a-walk's Aa layout at 375x667.

## 2026-11-10 (cloud): CAST-AWAY-BUILD (`docs/history/contracts/2026-11-09-cast-away-build.md`, Medium, todo row CAST-AWAY)

DONE, merged and live (unlisted): [#723](https://github.com/OrthogonalMaffs/maffsgames/pull/723), branch `claude/relaxed-tesla-8o84r1`, worktree the primary checkout. `gh auth status` failed at the start (GH_TOKEN invalid), so the merge took the standing route above. `games/cast-away/`: sin, cos and tan x = k on 0-360 with CAST and the graph, four stages and boards (pools 70, 244, 258, 290), named feedback, "Show me" after two wrong tries, the three walkthroughs word for word, the band on start and results only. `verify-cast-away.py` PASS: every key by an mpmath root search, every feedback rule fired, seven sizes and modes, 12 of 12 plants. Answer lock PASS; phone-fit PASS (asking only) in normal, Aa and laptop; stage exit OK. Registered unlisted; todo row closed to todo-done.md; no claim taken.

Deviations for review (PR body): level key `level3` (the roster's L3), not `l3`; figures side by side on phones in Stages 3-4 and after answering; Stage 2 asks for the pair of forms; Stage 2 has no axis values; Stage 1 is 25 equations by value. Discoveries: the standing ruling names todo row CLOUD-MERGE-TOKEN, which does not exist; phone-fit's generic driver cannot get a question marked when it resolves only after two tries. Next: Jon lists it after his look (played 10 Nov; listing waits on his word).

Project Claude review (10 Nov 2026): approved. 862 pool questions independently recomputed, 0 mismatches. Stage 1's 25 distinct equations accepted (the full standard exact-value set; the contract's '40+' was impossible); level key 'level3' accepted (matches scripts/roster-levels.json; the contract's 'l3' was wrong); Stage 2's 'which pair solves it?' accepted (works for negative k, where neither solution is α).

Merged as 39df31b via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: `github.com` / `X Failed to log in to github.com using token (GH_TOKEN)` / `- Active account: true` / `- The token in GH_TOKEN is invalid.`, exit 1; output of `gh auth status` re-run 10 Nov before this push); main runs 42809397904 (check-site, 92 of 92 jobs) and 42809397779 (phone-fit-full) green.

Record: agent Claude Code; wall n/a (planner and container clocks differ); review cycles 1; amendments 0; usage n/a.

## 2026-11-10 (cloud): #722 merge route

RULING (Jon, Tue 10 Nov 2026, 07:40): one-off merge route for #722 only (docs-only close-out of #721).
Merge through the GitHub connection after re-checking and reporting: (1) #722's Gate is green on its head b0a7e99, (2) it is mergeable with no conflicts, (3) main's newest full run is green and nothing newer has landed. If any fails, STOP. Squash-merge pinned to b0a7e99, "[skip ci]" disarmed as merge-pr.py does; watch main's run and report it. Record this ruling verbatim (in the next close-out, not a new PR). merge-pr.py remains the only standing route.

#722 merged as 9fdfe7a (squash, pinned to b0a7e99); main's run 42776601366 recorded 07:48.

## 2026-11-09 (cloud): FORGE-HINT-SPACES (`docs/history/contracts/2026-11-09-forge-hint-spaces.md`, Small, todo row FORGE-HINT-SPACES)

Merged as f3d27d3 (main run 42658241563 green): [#718](https://github.com/OrthogonalMaffs/maffsgames/pull/718), branch `claude/festive-cori-ntxpzg`, worktree the primary checkout. formula-forge's 45 hint2 strings mark their maths with `\( \)` and render through `MaffsText.html()` (mathtext.js loaded); token check 45 of 45, no word, number or operation changed. B7 33 -> 0; `--write-ledger` removed exactly the 33 entries (no line field moved). Chromium, the game's own Hint buttons: 74 of 74 Hint 2 renders pass on the branch, main 34 of 45 hints fail. `check-banks.py --ci` OK. Findings r-001 and t4-004 fixed; todo row added and closed to todo-done.md; /updates/ line for Jon to confirm; claim taken (89da753) and released.

Outside EXACT CHANGE, for review: `verify-formula-forge.py` read Hint 2 raw, so with the delimiters its equations failed to parse, the ValueError was swallowed and 32 dropped out unchecked (159 -> 127) under a PASS. It now removes the delimiters first (the same 159, identical digest) and has a planted fault for it (MISSED without the fix). Separate commit 97f5242, to drop if Project Claude prefers. Discoveries: `Substitute: A = ...` (L4 s4) set "Substitute:" in maths italic, which B7 cannot see (one word, no space to lose); fixed by the same convention. Next: review and Jon's "merge"; the contract file moves to `docs/history/contracts/` after merge.

Record: agent Claude Code; wall n/a (planner and container clocks differ); review cycles 0; amendments 0; usage n/a.

## 2026-11-09 (cloud): HEADER-FIT (`docs/history/contracts/2026-11-09-header-fit.md`, Small, Amendment 1, todo row 1.39)

Merged as 3929b1a (main run 42618722393 green): [#717](https://github.com/OrthogonalMaffs/maffsgames/pull/717), branch `claude/festive-lovelace-iukjhc`, worktree the primary checkout. First Gate green on da3d4fe (run 42605952691) with both of equation-builder's Aa buttons kept (STOP IF 1, both wired) and the titles cut short at 320px. Amendment 1 (Jon, 11:34, "yes to both"): equation-builder keeps the standard `a11yToggle`; the second button's cream palette and teal start title moved onto Aa mode, and its larger text too but above 480px only (on a phone, with OpenDyslexic, it put Next at 836 against an 804 fold at 390x844); its tighter letter spacing gave way to the standard's. All three: below 375px, and up to 480px in Aa mode, the back link is its arrow only (aria-label "Back to Games", 44x44), the divider hides, title and Aa share the first row and the pill and score take a row under them; the title shows in full at 320px (168px wide; two lines at a word break in Aa). measure-phone-fit (normal, Aa): no sideways scroll, every figure the same or better than main; tier 1 clean. Todo row 1.39 closed to todo-done.md; /updates/ line; the three claimed together and released.

Discoveries: measure-phone-fit's `--aa` sets `mfg_accessible`, but probability-pioneer and shape-shifter (and like-terms-collector, by the same key) read only `mfg_dyslexia`, so their Aa mode is never measured; in it both headers overflowed at every size (489, 498 px on main). probability-pioneer in its own Aa mode still scrolls sideways (418 px) from `div.scale-label`, question content outside this contract. Next: review, Jon's look and "merge"; the contract file moves to `docs/history/contracts/` after merge.

Record: agent Claude Code; wall n/a (planner and container clocks differ); review cycles 0; amendments 1; usage n/a.

