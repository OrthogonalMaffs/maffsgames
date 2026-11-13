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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk's random phone-fit reds (375x667 Aa, 320x568 normal) are fixed by TAKE-A-WALK-SEED** (no seed reads the clock; the Gate's clock-seed scan); its layout is todo row TAKE-A-WALK-PHONE-LAYOUT. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

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

## 2026-11-13 (cloud): SIX-SEVENS-WEIGHTING (`docs/handover/contracts/2026-11-13-six-sevens-weighting.md`, lane exception, Jon 07:58)

IN PROGRESS. Agent Claude Code (cloud), branch `claude/optimistic-goodall-q87dul` from main 89a5946. First commit: this contract, and WARMUP-PACKS' close-out (below). Core set checked before any edit: 25 products, 42 among them (18 21 24 27 28 30 32 35 36 40 42 45 48 49 54 56 60 63 64 72 81 84 96 108 144); OTHER 15 (9 12 15 16 20 25 33 44 55 66 77 88 99 121 132). Next: six_sevens.py rule and deck_problems, build_deck.py hook, three plants, scripts/test-loop-cards.py, build and proofs.

## 2026-11-12 (cloud): WARMUP-PACKS (`docs/history/contracts/2026-11-12-warmup-packs.md`, lane exception, Jon 17:58; Amendments 1-3)

DONE, merged and live: #744 squash-merged as c0214c8 (12 Nov 19:27 UTC). Route: through the GitHub connection; the merging session recorded no route line, so it is not stated here (gh auth fails in cloud containers, todo CLOUD-MERGE-TOKEN). Main on c0214c8: check-site 43290435666 GREEN, phone-fit-full 43290435842 GREEN (closed out by SIX-SEVENS-WEIGHTING, 13 Nov).
Was: PR OPEN, merging on green. Branch `claude/vibrant-fermi-solu8c` from main 5261dc9: 29699cd contract (no claim: the rooms are not on cloud-remaining, which lists games); f3fac3d #743 close-out; then the work. Stopped three times, each ruled (the contract file has them verbatim): 18:30 (ten shelves, new art, fines-screen one bold part, "all in order."), 18:55 (hook off every cover; a hook or brief with a {{token}} fails the build), 19:12 (the cover picture scales to the space left, floor 60%).
Banks: chokey-factor-count 6 (24, 72, 76, 80, then 36 and 64: squares tried after every non-square so old indices hold; answers 6-10, 12), dewey-sort-arm 10 (the eight, 510, 636; answers 2-7; set codes A-K). variants.json differs from main only there, pure appends. Six RECOMPUTE entries agree on all 205 stored values.
Art: rerolls came as loose PNGs on art/library-jam-pack-1 (9bb2b25) and art/comic-caper-pack-1 (d95bc97), two named *.png.png; saved under their stems. No art branch deleted.
Packs (seed 1, DRAFT): Kiln 35 pages, cover spare 38.0 mm; Christmas 36, 23.0 mm; Comic Caper 36, 33.0 mm; all three pictures full size, 150 x 82 mm. Library Jam 36, picture 119 x 65 mm (79%), spare 0.0 mm. Selftest 38/38. check-escape-rooms, check-lock-bank, check-canon-rooms and all ten test-escape-* PASS.
Known, for Jon's proofread (todo WARMUP-PACKS-APPROVE): captions keep the punctuation round a mid-sentence bold part (Library Jam's trolley, jammed book, reset card). Layout calls (SR-31): Comic Caper's dials 09 and 11 have no write panel, so their answer boxes sit on the wood below.
