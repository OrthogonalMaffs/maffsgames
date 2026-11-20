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

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/history/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

**Merge route:** merge-pr.py only (the 10 Nov ruling was retired by Jon, 16 Nov 2026; canon MERGE-ROUTE). If it cannot reach GitHub, stop and report; the PR waits.

**Standing rule, close-outs (Jon, 10 Nov 2026, 13:13; recorded verbatim, CUMFREQ-CURVE's preamble):**
> STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
> A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.

## 2026-11-20 (cloud): 52DLE-REBUILD (`docs/handover/contracts/2026-11-19-52dle-rebuild.md`; Project Claude 19 Nov, two parts)

Agent Claude Code (cloud), branch `claude/admiring-lovelace-71xc46` from main d659bd7. Tier Medium-Large. Root cause matched on d659bd7 (the 20 puzzles, the score and the fixed warmth bands, level 'all', the dark page).
**Close-outs carried (first commit, 061887d):** #849 SFB-WORKING-GCSE, recorded in its entry below.
Done on the branch: `scripts/gen-52dle.py` (new; seed 52) searches every 3-5 clue set per number exhaustively under item 3 and writes compact codes into the page (3 ladders a number where they exist, shortest length kept; 2771 ladders, 95 KB page). KS3: all 100 numbers (96 with 3-clue ladders, 4 with 5). GCSE: 928, the 72 left out the contract's count. `games/52dle/index.html` rebuilt on the light theme: level picker (Foundation `ks3` 1-100, GCSE 1-1000), "Start: five numbers" (Firebase board per level, PB, history) and "Today's number" (UK date + level through FNV-1a, no generator and no seed; the result shown again on return; local list and share grid). Guess any time or take the next clue; a wrong guess shows Higher/Lower, a closeness word as a share of the range (1/5/15/40% bands) and each revealed clue it breaks. A found number waits on its own Next, a missed one on `MaffsNext.wrong` (no fallback); "Did you know?" for the 17 numbers. One `question_answered` per number (question_id `52dle-<level>-<n>`, attempts, correct). `scripts/verify-52dle.py` rewritten (see its docstring); 5 plants caught, PASS, about 2 min locally.
Other files: 52dle off WRONG_PAUSE_KNOWN_FAIL (both sets) and in check-theme MIGRATED; check-start-mount (now a start screen, `#menu`, START_STEPS), check-teacher-invite (`results`), question-id-warn.json, phone-fit-state.json (the 3 modes' entries: it now passes at every size), `data/check-ledger.json` (52dle is a generator now: its entry and both B4 entries removed), leaderboards hub `['ks3','gcse']`; roster row #10; todo LEDGER-B4-52DLE moved to todo-done; /updates/ line.
**Phone fit (measure-phone-fit --only 52dle, fallback fonts):** main failed every size (last option 887-906 px on phones, 836 on laptops); the branch passes the asking screen at every size in normal, Aa and laptop. The driver cannot reach a marked answer (six wrong guesses make one mark), so Next is measured by hand at 320x568: bottom 517 px normal, 519 Aa, fold 528. Start screen (report only): Start 393 px normal, 473 Aa at 320x568.
**Decided for you:** (1) "I have 1 digit" for N = 1; (2) bands are inclusive and the start screen says so; a band ending at the number counts as naming it, used only where no other ladder exists (KS3 41, 61; GCSE 201, 251, 401, 501, 601, 751, 801, 951; pinned in the verifier); any other clue whose own number is the hidden number is never used; (3) a ladder's order is its clues by how many numbers each fits alone, most first; (4) a guess that is not a whole number from 1 to the top (23.9, 0, 1,000) is refused with a message, costs no guess and is never marked; (5) numbers written without commas (1000), as they are typed; (6) warmth bands 1%, 5%, 15%, 40% of the range; (7) the daily's own list stays on the device; (8) the start screen's order: level, play, then how it works.
**Gate red on b7630b6 (Site-wide checks, job 136289802146), fixed:** Search titles (`check-meta.py`) failed because the rebuild had rewritten the page's meta and og descriptions, which `data/games.json` generates; restored to the generated text (not in EXACT CHANGE). Every other job passed on b7630b6.
**OPEN for Jon:** the new look needs his sign-off (the roster keeps the old page's grandfathered line with a note); 521's fact never shows (521 is not in the GCSE pool), and 13, 23, 31, 37, 53, 97 show at Foundation only; timer-policy.md does not list 52-dle (it has no clock).

## 2026-11-20 (cloud): SFB-WORKING-GCSE (`docs/history/contracts/2026-11-19-sfb-working-gcse.md`; Project Claude 19 Nov, two parts)

Agent Claude Code (cloud), branch `claude/modest-lamport-bgup39` restarted from main b7ba480. Tier Medium. Root cause matched (handle() :245: marks and Next only). Every GCSE item fits a kind: a 1-10, b 11-18 and 44, c 45-50, d 19-28, e 29-38, f 39-43.
**Close-outs carried (first commit, 0045d45):** #848 CIRCLE-WORKING, recorded in its entry below (check-site 44712504443, phone-fit-full 44712504425, pages 44712504265, all success).
Done on the branch: `games/standard-form-blitz/index.html` gains `working(q)` (GCSE only; [] for A-Level), built by the contract's rules a-f from the item's own digits with exact decimals (BigInt mantissa and power of ten; division by scaling until it divides, never a float); the contract's examples for items 22, 32 and 48 come out character for character. The card is Surd Simplifier's: `fold.css`, `.maffs-ref-row.work-row` with `.maffs-ref-phone` / `.maffs-ref-fits` ("Working" / "How to get there") then `#nextMount`; `showWorking()` on a wrong answer, `clearWorking()` in `showQ()`, `keep: shownCard`. Open by the media query `(320-359 wide, >= 1050 tall), (360-439, >= 980), (440-759, >= 940), (>= 760, >= 870)`: measured over all 50 GCSE items answered wrong, worst option pairing, normal and Aa, real fonts, every width 320-760 in 10 px steps, fold less the 40 px footer: open, Next needs 1013 px (320-359, Aa), 943 (360-439), 902 (440-759), 833 from 760; +30 px. Canon phones and both laptops get the collapsed card; 1440x900 and 1920x1080 the open one. Collapsed, the card costs 0 px at every size in both modes ("Working" sits beside Next in Aa at 320 and 375), and Next ends where it does on main (measured against main's page: identical).
`verify-standard-form-blitz.py`: every GCSE item has working, no A-Level item does; every "=" chain exact in SymPy (76 chains); kind a names the key's coefficient and places moved in the right direction; kinds a-e end on the key as written, f on "So <key>"; in Chromium every wrong option of every GCSE item shows the lines in the card before Next, both copies alike, and a right answer or any A-Level answer shows none; at 16 sizes x normal/Aa, open: Next within the fold, collapsed: no height. New plants caught: rule d adding the coefficients, rule e subtracting the powers the wrong way round, no card, the card below Next (Next moved above the row). All 20 plants caught; PASS, 82 s locally.
**Phone fit (measure-phone-fit --only, fallback fonts):** normal, Aa and laptop identical to main. check-answer-lock (--game), check-scroll-reveal --check PASS.
Todo WRONG-PAUSE-REASONS: standard-form-blitz now "A-Level; GCSE has its working"; the GCSE half recorded in `docs/history/todo-done.md`. /updates/ line.
**Decided for you:** (1) lines rendered as Surd's `workLine()` (words as plain text that wraps, the maths by `rk()`); (2) in rule d a negative second power is bracketed too (`10^{3 + (-2)}`), as rule e asks; (3) in rule f a number already ordinary (item 42's 0.006) is shown as itself, not "0.006 = 0.006"; (4) four bands, not Surd's two, each its measured need, so a tall phone wider than 360 gets the open card sooner; (5) the "Which two are equal" endings read "So 4.5 × 10⁶ and 45 × 10⁵", the key as written.
**Gate red on 2d23dca (check-site 44716988585), fixed:** Tier 4 layer A's lint failed (0 new, 77 unused allowlist) because esprima (ES2017, `bank_common.py`) could not parse the page at all: the working's BigInt literals (`10n`) and `**`. The bank was unread, so every standard-form-blitz allowlist entry looked unused. Fix inside EXACT CHANGE's file: `BigInt()` constants, no literals, no `**`. The page parses; extract-banks and check-banks give main's totals in this container (whose KaTeX-offline noise both share); the verifier PASS again, 20 plants caught. phone-fit-full 44716986352 was green on 2d23dca.

**MERGED 20 Nov as 5b7d0cf (#849)** at 10:51:28 UTC (head 8dc8cdd), route merge-pr.py. Main on the merge commit, read from the API by 52DLE-REBUILD: check-site 44722741034 success, phone-fit-full 44722741254 success (both push, attempt 1), pages build and deployment 44722740832 success. Closed out by 52DLE-REBUILD's first commit; contract moved to `docs/history/contracts/`.
