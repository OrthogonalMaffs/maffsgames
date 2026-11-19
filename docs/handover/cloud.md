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

## 2026-11-19 (cloud): CORE-PAPERS-NO-LETTERS (`docs/handover/contracts/2026-11-19-core-papers-no-letters.md`; Jon 19 Nov)

Agent Claude Code (cloud), branch `claude/nifty-faraday-13526r` from main eb89b6f. Tier Small.
**Close-outs carried (first commit, b235476):** #841 WORKING-CARD, recorded in its entry below (check-site 44616595773, phone-fit-full 44616595499, pages 44616593785, all success).
**STOP IF sweep:** nothing reads the letters. The only reader of `.option-letter` text is `scripts/core_paper_deal.py`; no keyboard handler, analytics field, lock hint (each says "the first option shown") or "press A" text in the four pages, scripts, `schools/assets/` or firebase/.
Done on the branch: each paper's builder (paper1 :760-767, 2a :585-592, 2b :539-546, 2c :558-565) drops `letters` and writes `<span class="option-letter" aria-hidden="true"></span>`; marking's ✓/✗ untouched. `core_paper_deal.py`: the A-D check replaced by every badge empty and aria-hidden before marking, and, after each option is pressed, the pressed badge ✗ (or ✓ if accepted), every accepted option ✓, every other badge empty; the key-position message now names positions 1-4; new plant "the position letters put back".
**Checked locally:** verify-core-maths-paper1, -2a, -2b, -2c, -paper1-tax all exit 0; the deal PASS on each paper, 20 sessions; all five plants caught on each (the new one: "a button shows ['A', 'B', 'C', 'D'] before marking"). measure-phone-fit `--only` each paper in normal, `--aa` and `--laptop` (fallback fonts: this container's footer pre-check fails on real fonts, main too), main eb89b6f against the branch: all 12 reports byte-identical.
**Decided for you:** (1) aria-hidden stays on the badge after marking too (the contract's attribute; ✓/✗ was the badge's text before and the button's state is in its class), so a screen reader reads the option text alone throughout; (2) the deal check's position wording ("position 1-4", not "A-D").

## 2026-11-19 (cloud): WORKING-CARD (`docs/history/contracts/2026-11-19-working-card.md`; Jon 19 Nov)

Agent Claude Code (cloud), branch `claude/epic-curie-1vh9wl` restarted from main ed8590b. Tier Small. Root cause matched (#working at :137, below #nextMount at :136).
**Close-outs carried (first commit, 2717b47):** #840 CORE-PAPERS-SHUFFLE, recorded in its entry below.
Done on the branch: Surd Simplifier loads `/schools/assets/fold.css`; `#working` replaced by `.maffs-ref-row.work-row` with `.maffs-ref-phone` (collapsed) and `.maffs-ref-fits` (open), summary "How to get there", then `#nextMount`; `showWorking()` fills both, `clearWorking()` resets them; tint `--ref-bg`/`--ref-edge` only, line styles kept under `.work-row`; `MaffsNext.wrong(..., keep: shownCard)`. Collapsed by default; open by the page's media query `(320-759 wide and >= 980 tall), (>= 760 wide and >= 860 tall)`. Measured over all 100 items answered wrong, each in its worst pairing of options to a row (the 2x2 grid's rows take the taller option, so one random order understates it), normal and Aa, real fonts, fold = viewport less the 40 px fixed footer (measure-phone-fit's): open, Next needs 950 px at 320 wide (Aa), 912 at 375-412, 830 from 760; +30 px. Canon 7.6.2: theme.css to fold.css (twice: the definition and "everything else is in"), and Jon's sentence. `verify-surd-simplifier.py`: the card before Next in document order, both copies the same lines, a collapsed card opened shows every line; at 12 sizes x normal/Aa, every item, worst pairing, Next within the fold, never past it with the card open, past it collapsed only where KNOWN_PAST_FOLD lists; plants (card below Next; the open band loosened to 700 px) both caught. SymPy checks unchanged. PASS, 75 s locally (was 45).
**Phone fit (measure-phone-fit, --only):** normal (fallback fonts: this container's footer pre-check fails on main too, 811 vs 810 px) and laptop identical to main; Aa same verdict (WARN Aa at 320), the sampled Next 57 px lower on phones. check-answer-lock, check-scroll-reveal (--selftest, --check), ci-groups --check PASS.
**STOP IF hit (reported; merge held for Jon):** with the card collapsed, in Aa at 375x667 (627 px fold) 25 items' Next ends past the fold that fits on main (worst alevel[16]: 680 px, main 623): gcse[20-32], alevel[10-19, 41, 42]. Cause: in Aa the collapsed pill (239 px, OpenDyslexic spacing) and Next (135 px) do not fit one 343 px row, so `.maffs-ref-row` wraps (+57 px). Not fixable inside the contract: shrinking the pill is a fold.css change (home lane) and "tint only"; removing Aa's letter-spacing undoes the mode. Also worse but in canon's scroll exception: Aa 320x568, 100 items past (main 69). Normal mode: no item worse anywhere (320x568's 53 past the fold are main's 53). Screenshots: Aa 375x667 alevel[16], main and branch, sent to Jon.
**Decided for you:** (1) the fold is the viewport less the fixed footer, as measure-phone-fit reads it (innerHeight alone would pass 25 items that the footer covers); (2) each item measured in its worst option pairing; (3) collapsed by default, open only in measured bands (log-laws' pattern inverted: a band too generous shows the open card where it does not fit); (4) "1280 x 720" kept as Jon wrote it in the canon sentence.
PR #841. **Jon's first ruling on the stop (19 Nov):** the collapsed label (`.maffs-ref-show`) becomes "Show working" in every mode, the open title stays "How to get there"; "Working" instead only if "Show working" and Next still wrap in Aa at 375x667; the 25 exceptions must clear and the exception list goes; Aa 320x568 no worse than main (69 past the fold), else report and stop; then the Gate and merge-pr.py.
**Done, and a second stop (reported, merge held):** "Show working" in both copies (pushed). Aa 375x667: pill 187 px + Next 135 + 10 gap = 332 of 343, one line; all 25 clear (0 past the fold, main 0). Re-measured all 100, worst pairing, footer-adjusted fold, at the verifier's 12 sizes: normal no worse than main anywhere (320x568: the same 53); Aa no worse anywhere except **Aa 320x568: 100 past the fold, main 69** (31 more, from alevel[0]): the 288 px row still wraps ("Show working" 187 + 135 + 10 = 332). Measured on a scratch copy, not committed: "Working" (121 px) fits one line at 320 and 375 in Aa, and gives figures identical to main at both phone sizes, normal and Aa (320x568: 53 and 69; worst 576 and 629 px). **Jon's second ruling (19 Nov):** "Working" in every mode (open title still "How to get there"); the exception list replaced by the no-height rule: with the card collapsed, Next ends where it would with no card, at every verifier size in normal and Aa; the open card keeps the strict check (Next above the fold); a plant restoring "Show working" must FAIL.
**Done:** label "Working" (121 px in Aa: one line with Next at 320 and 375). `KNOWN_PAST_FOLD` removed; `LAYOUT_JS` measures each pairing with the card and with the row's cards hidden, and fails a collapsed card that costs over 0.5 px. Plants: the card below Next, the open band loosened to 700 px, "Show working" restored (caught: Aa 320x568 gcse[0] costs 57 px). Verifier PASS (79 s). Phone fit identical to main in normal (fallback fonts), Aa and laptop. Figures with "Working" (worst pairing, footer-adjusted fold): every size, both modes, the same items past the fold as main (normal 320x568: 53; Aa 320x568: 69; elsewhere none).
**MERGED 19 Nov as dc7885b (#841)** via merge-pr.py (closed out by CORE-PAPERS-NO-LETTERS's first commit). Main on the merge commit, read from the API: check-site 44616595773 success, phone-fit-full 44616595499 success (both push, attempt 1), pages build and deployment 44616593785 success. Contract moved to `docs/history/contracts/`.
Record: agent Claude Code; wall n/a (spans two rulings, not timed in this session); review cycles 0; amendments 2 (Jon's rulings); usage n/a.

