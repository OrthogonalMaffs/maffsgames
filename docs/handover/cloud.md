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

## 2026-11-11 (cloud): CLOUD-QUEUE-1111 PR 3, PP-AA-OVERFLOW (`docs/handover/contracts/2026-11-11-cloud-queue-1111.md`, Small): STOPPED for Jon

STOP IF hit: "the fix needs the label wording shortened (report the labels; Jon writes words)". Nothing changed, no claim pushed; the queue is not finished. Measured with `mfg_dyslexia` set and the pinned fonts (bank_common.real_font_response): stage 1 is 418 px wide at 320, 375 and 390 (1366 fits). The labels are the only source: stages 2-3 fit on all 15 questions each, and the footer's links scroll in their own box. In Aa mode each label's name needs 93 (Impossible), 73 (Unlikely), 61 (Even / Chance), 55 (Likely) and 66 px (Certain) at 10px OpenDyslexic with the inherited 1.8px letter-spacing. That is 388 px of label in a 260 px row at 320 (52 px a label); the "1 Certain" option sits off the right edge at 375. Prototyped in the game's own Aa CSS: (A) the contract's `min-width:0` plus wrapping `.label-name` fits the row but breaks every word mid-word ("Impo/ssibl/e", "Chan/ce"); (B) wrapping whole labels makes three rows, "1" alone and the scale out of order. Neither is fit for a dyslexia mode. Even shorter words do not fit one row at 320 above about 4 letters, so wording plus wrapping at spaces, a stacked layout, or a legend is Jon's call. Still owed when it resumes: the fix, todo PP-AA-OVERFLOW closed, AA-KEY-MISMATCH (§4) added, /updates/ line, and #735's close-out (this entry records it, on this branch only until then).

## 2026-11-11 (cloud): CLOUD-QUEUE-1111 PR 2, MONEY-ANSWERS (`docs/handover/contracts/2026-11-11-cloud-queue-1111.md`, Medium; lane exception for answer.js, check-banks.py, test-answer-js.py)

DONE, merged and live: [#735](https://github.com/OrthogonalMaffs/maffsgames/pull/735) merged as 0b61732 on a green Gate under the standing authorisation, via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: `X Failed to log in to github.com using token (GH_TOKEN)` / `The token in GH_TOKEN is invalid.`), the message the PR title and body word for word (checked). The first Gate (43020902589, on 5c92ade) was red in Answer lock L7: graph-sketcher's `checkCell` took `input.parentElement` as the cell, which `moneyInput` wraps in a span, so CM5/CM11's tables never completed. Fixed with `closest('td')` (71c4320); `verify-graph-sketcher.py` read the same parent and missed it, fixed in 379b195. Gate check-site 43024047117 green on 379b195. Main on 0b61732: check-site 43026110129 green (89 of 89), phone-fit-full 43026110113 green (5 of 5). Branch from main 3a49f48: claim b26f889; #734 close-out 2061ea6. Audit (table in the PR body): 8 pages changed: growth-and-decay, stat-attack, chart-interrogator, graph-sketcher, fermi-lab, as-you-can-see, squared-squirrel (stages 2-3, not boxed by #720) and the-6-ps (£ compound measures). `MaffsAnswer.decimal()`/`exact()` take `opts.currency`; readers of their own read money through `MaffsAnswer.parse()` (fermi-lab strips the sign before its own parser). check-banks' money rule sees `money(`, a currency passed to `decimal(`/`exact(`, and `unit:'£'`; plants caught (and a no-money page not). Unboxed, for Jon (todo MONEY-THOUSANDS): £k, £100s, pence and the escape rooms (shared engine.js, home lane). All 8 verifiers PASS except as-you-can-see, which fails here only on chart-label overlaps, the same on main in this sandbox (fonts stubbed). Main's CI is green on it.

## 2026-11-11 (cloud): CLOUD-QUEUE-1111 PR 1, MATRIX-CRUNCH-1.4 (`docs/handover/contracts/2026-11-11-cloud-queue-1111.md`, Small)

DONE, merged and live: [#734](https://github.com/OrthogonalMaffs/maffsgames/pull/734) merged as 3a49f48 on a green Gate under the standing authorisation, via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: `X Failed to log in to github.com using token (GH_TOKEN)` / `The token in GH_TOKEN is invalid.`), the message the PR title and body word for word (checked); Gate check-site 43015319467 green on 90db100. Main on 3a49f48: check-site 43017088862 green (89 of 89 jobs), phone-fit-full 43017088839 green (its "shared path changed?" job passed: no shared path, so the per-mode jobs were skipped). The queue contract stays in `docs/handover/contracts/` until PR 3 merges. Close-out carried by PR 2's first commit after its claim (b26f889). Branch `claude/compassionate-sagan-9myj6x` from main 9dba297: contract and claim 777e245; #732/#733 close-out 9d4dbb5. `games/matrix-crunch/index.html:186` det [[6,2],[3,1]] distractors `['12','9','6']` (Jon, 10 Nov: '0' → '9'): four distinct options in Chromium. `--write-ledger` removed exactly the B2 entry `matrix-crunch::0a3572e58f4d#1::B2` and changed no entry set; it also rewrote 54 `line`/`detail` fields in 8 untouched games (LEDGER-LINE-DRIFT, todo §4 item 39), so only the B2 change is committed. `verify-matrix-crunch.py` PASS; check-banks --ci OK. Todo 1.4 and LEDGER-B2-MATRIX-CRUNCH closed; claim released.

## 2026-11-11 (cloud): BANKS-40 PR 2, spot-the-error (`docs/history/contracts/2026-11-11-banks-40.md`, Small)

DONE, merged and live: [#732](https://github.com/OrthogonalMaffs/maffsgames/pull/732) merged as d4cacdb on a green Gate under the standing authorisation, via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: `X Failed to log in to github.com using token (GH_TOKEN)` / `The token in GH_TOKEN is invalid.`), the message the PR title and body word for word; Gate check-site 43002485996 green on c765c27. Main on d4cacdb: check-site 43004531103 green; phone-fit-full 43004531224 red in all three modes, only on spot-the-error stale on the unmeasurable list, fixed by #733. [#733](https://github.com/OrthogonalMaffs/maffsgames/pull/733) (Jon's GO of 11 Nov: two files only, `scripts/phone-fit-state.json` and the verifier's ci-line) merged as e309e9c by the same route; Gate check-site 43009597897 green on c7ce6a6; main on e309e9c: check-site 43011407222 green (90 of 90 jobs), phone-fit-full 43011407164 green (5 of 5). spot-the-error became measurable because the phone check's address-seeded shuffle now deals ste_ks3_010, a two-step item, first. Close-outs carried by CLOUD-QUEUE-1111 PR 1's first commit after its claim; the contract moved to docs/history/contracts/. Branch `claude/practical-archimedes-3k6s2p` from main 2924e0b: #731 close-out c62fc09. Spot the Error ks3 40, gcse 45, level4 40 (15 items); `verify-spot-the-error.py` PASS on 125 with each new item's ITEMS entry and pin; check-banks --ci OK; claim released (cloud-remaining empty). The contract moves to docs/history/contracts/ in the lane's next close-out.

