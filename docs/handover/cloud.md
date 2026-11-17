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

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/handover/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

**Merge route:** merge-pr.py only (the 10 Nov ruling was retired by Jon, 16 Nov 2026; canon MERGE-ROUTE). If it cannot reach GitHub, stop and report; the PR waits.

**Standing rule, close-outs (Jon, 10 Nov 2026, 13:13; recorded verbatim, CUMFREQ-CURVE's preamble):**
> STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
> A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.

## 2026-11-17 (cloud): SINE-NOT-SINE (`docs/handover/contracts/2026-11-17-sine-not-sine.md`; Jon 17 Nov)

Agent Claude Code (cloud), branch `claude/blissful-heisenberg-lzfkax` from main 3349092 (after #809). Size: a new game in new files, unlisted.
**Close-out carried (first commit):** HEATWAVE-APPROVE (#809, 862f7a6), recorded below; contract moved.
Bank: all 120 answers recomputed independently by coordinates and vector addition before any build (scratch script): 120/120 agree, none within 0.005 of a 1 d.p. boundary, the eight ambiguous items each have two triangles and every other sine-angle item one.
Done on the branch: `games/its-a-sine/index.html` (the bank verbatim; level picker gcse/level3/level4; modes stage-1, stage-2, stage-3, all-three, 10 items a run; true-shape SVG diagrams with a label-spacing pass; calculator by stage; boards `<level>-<mode>`); `scripts/verify-its-a-sine.py` (bank, marking, diagrams 360x640, play 360x640; the five plants caught; PASS); the 12 board labels in `schools/assets/firebase-leaderboard.js` (Jon's lane exception, 17 Nov, additive only); roster row #111 (Unlisted); `data/games.json` and apply-meta; the findings file; check-answer-lock, check-levels, check-theme, check-teacher-invite, check-start-mount, audit-register, verify-stage-exit and the coverage check's NOT_ON_HUB; `schools/assets/launch-dates.json` (one line; check-ugh-stats needs every game page dated); todo ITS-A-SINE-LIST.
Decided against the contract, with evidence: the palette is light, not dark (canon §7.5: a game whose levels include GCSE is light; check-theme fails dark, and an exemption is a STOP IF); so the teal is `#0f766e` and the coral `#b8432c` (each over 4.5:1 on every light surface). The stage buttons carry `data-stage="1"`..`"4"` and `data-mode`, the shared stage-exit verifier's convention.
Local: measure-phone-fit cannot run in this sandbox (its footer pre-check fails on untouched main too, 1 px at 810 px, fonts); CI's phone-fit is the evidence.
PR #810. Gate red only on Tier 4 layer A: `its-a-sine::B3`, a false duplicate (level3_014 and level3_015: same prompt, both 117.7, different triangles). Jon ruled (17 Nov): change the bank, Project Claude's Amendment 1 (level3_015 now a 7.5, b 10, A 37°, answer 126.6; recomputed here independently, 126.638°, two triangles); no ledger entry; todo BANK-LINT-GIVEN for the lint itself. The amendment is appended to the saved contract, and the verifier takes an amendment's line in place of the original's.
Next: Gate; merge with merge-pr.py.

## 2026-11-17 (cloud): HEATWAVE-APPROVE (`docs/history/contracts/2026-11-17-heatwave-approve.md`; Jon 17 Nov)

Agent Claude Code (cloud), branch `claude/youthful-newton-86oz7b` restarted from main d23fe46 (after #808).
**Close-out carried (first commit):** PADLOCK-EASIEST-HINT (#808), recorded below; contract moved.
Done on the branch: `rooms/heatwave-mutiny/config.json` `"wording_approved": {"by": "Jon", "date": "2026-11-17"}` (Jon proofread the v2 PDF from main 58e4ea7: "approved, please remove the draft markings"); no other key changed. `build_pack.py heatwave-mutiny --final`: exit 0, "no page says DRAFT (--final)", page 1 178 words, `dist-packs/heatwave-mutiny-pack-v2.pdf` 36 pages (pypdf: no "DRAFT" on any page; title "The Heatwave Mutiny pack v2"); targets as #808 (A 1605, B 2587, C 3450, D 5949, E 6696, F 9380). Todo: HEATWAVE-PACK-APPROVE moved to `docs/history/todo-done.md`; PACKS-V2-UPLOAD no longer waits on #808 and lists heatwave-mutiny (v2) at £3. This file archived to under 16 KiB with check-context-size.py's own `archive()`.
MERGED 17 Nov as 862f7a6 (#809; merged_by Vector52F; route merge-pr.py as this entry planned; this session cannot see that call's output). Main on the merge commit: check-site 44057701420 success, phone-fit-full 44057701474 success. Contract moved to `docs/history/contracts/`. Closed out by SINE-NOT-SINE's first commit.

## 2026-11-17 (cloud): PADLOCK-EASIEST-HINT (`docs/history/contracts/2026-11-17-padlock-easiest-hint.md`; Jon 17 Nov)

Agent Claude Code (cloud), branch `claude/youthful-newton-86oz7b` from main a017ee9 (after #807). Lane exception: Jon, 17 Nov (started while the home lane's merge-pr.py waited on #807).
**Close-outs carried (first commit):**
- FINAL-PADLOCK-FAIR (#807, home lane's PR, run from a cloud session): MERGED 17 Nov as 65c7ebd via merge-pr.py (the home lane's call, named in this contract's LANE line). Main on the merge commit: check-site 44044387029 success, phone-fit-full 44044386836 success. Contract moved to `docs/history/contracts/`. Its entry in `docs/handover/home.md` still reads "MERGED: pending": home's file, not edited by this lane.
- MERGE-PR-ROBUST (#806, below): MERGED 17 Nov as 3797bf8 (merged_by Vector52F; route merge-pr.py as its entry planned; this session cannot see that call's output). Main on the merge commit: check-site 44030827845 success, phone-fit-full 44030827838 success. Contract moved to `docs/history/contracts/`.
Done on the branch: `final.py` `ease()` (x: the hardest product's (smaller, larger) digits, then the count; +-: the largest term's digits); `SHAPES` entries carry their student hint and key line (x text unchanged; plus-and-minus new), `shape_wording()` refuses a missing one by name, `shape_wording_problems()` fails a no-x shape that says multiply/product. `build_pack.py`: `class_order()` = easiest first (was the seeded shuffle), `choose(only=)`, `grader()`, `easiest_class_problems()` (every easier class re-searched on its own must stay below N), `final_hint()`/`final_key_line()` from the shape, `final_wording_problems()` on the printed hint card and key (in the build and the self-test). Tests: self-test 67/67, every room's easier classes below N; test-pack-generator 48 plants caught, 21 controls (new: seeded order, no hint, no key line, multiply in a shape, four Heatwave wording plants; ease order, Car Trap as built, both packs' wording as built). check-escape-rooms exit 0. All ten built (nine --final, Heatwave DRAFT); page 1 178 words (Kiln 175).
Changed classes: car-trap 1x3 (645-1935) -> 1x2 (120-360); library-jam 1x3 (268-804) -> 1x2 (72-216); pe-shed-rebellion 2x3 (1800-5400) -> 2x2 (690-2070); the other seven unchanged (each with its easier classes' best below N, in the self-test log). Canon has no #807 ruling to update (#807 did not touch canon): for the home lane's next docs PR, "easiest class first (Jon, 17 Nov 2026)" beside the final-padlock rules.
MERGED 17 Nov as 58e4ea7 (#808) via merge-pr.py `--watch --wait 3600`, exit 0, last line "main 58e4ea7 run 44052013877: GREEN". Main on the merge commit: check-site 44052013877 success, phone-fit-full 44052013837 success. Closed out by HEATWAVE-APPROVE's first commit.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-17 (cloud): MERGE-PR-ROBUST (`docs/history/contracts/2026-11-17-merge-pr-robust.md`; Jon 17 Nov)

Agent Claude Code (cloud), branch `claude/gallant-allen-2f8ehb` from main cf4687e. Size medium; gate file (merge-pr.py).
**Close-out carried (first commit):** SHAPE-SHIFTER-FLAKE (#805, e91dd5e), recorded below; contract moved. ANSWER-AUDIT-PILOT's had already ridden on #805.
Done on the branch: `scripts/merge-pr.py`: `gh_raw()` + `classify()` (5xx, "Server Error", connection reset are `Transient(Refused)`; a 4xx never is) and `with_retry()` (GET only, 4 tries, 5/15/45 s; a Transient on PUT/POST becomes a plain Refused, never re-sent); `run_jobs()` steps 50 → 25 → 13 a page on a Transient; `guard()` waits on a Transient within --wait, never judging it; `--head` (default: this checkout's HEAD when on the PR's branch) skips judging until GitHub reports it; the post-merge watch has a 180 s registration grace; a failed read of main's head after the merge no longer hides the report. `--selftest`: 97 PASS, all 66 of main's lines unchanged, five plants caught (gh_api before, 50 a page only, a naive retry of PUT/POST/4xx, no expected head, no grace). Todo rows MERGE-PR-VERDICT and MERGE-PR-GRACE updated, both still open (the guard's (b') refusal is unchanged by contract).
MERGED 17 Nov as 3797bf8 (#806); main green on it (check-site 44030827845, phone-fit-full 44030827838); closed out by PADLOCK-EASIEST-HINT's first commit.

