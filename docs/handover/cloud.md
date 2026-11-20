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

## 2026-11-20 (cloud): CIRCLE-WORKING (`docs/handover/contracts/2026-11-19-circle-working.md`; Project Claude 19 Nov, three parts)

Agent Claude Code (cloud), branch `claude/modest-lamport-bgup39` from main d41f900. Tier Small. Root cause matched (handle() showed only "The answer: X."); QUESTIONS.gcse has 55 items in the order the working quotes.
**Close-outs carried (first commit, 337b23d):** #847 PACK-WORDING-VERSIONS, recorded in its entry below (check-site 44701989506, phone-fit-full 44701989671, pages 44701989105, all success).
Done on the branch: `games/circle-theorem-spotter/index.html` gains `WORKING` (keys 1-55, verbatim from the contract) and a "Why" reference card built as Surd Simplifier's: loads `fold.css`; `.maffs-ref-row.work-row` holds `.maffs-ref-phone` (collapsed), `.maffs-ref-fits` (open) and `#nextMount`, under the "The answer: X." line; `showWorking()` on a wrong answer, `clearWorking()` in `showQ()`; `MaffsNext.wrong(..., keep: shownCard)`. Collapsed by default; open by the media query `(320-429 wide and >= 1430 tall), (430-759 and >= 1300), (>= 760 and >= 1170)`. Measured over all 55 items answered wrong, each in its worst option pairing, normal and Aa, real fonts, every width 320-760 in 10 px steps, fold = viewport less the 40 px footer: open, Next needs 1392 px at 320 (Aa), at most 1268 from 430 to 759 (Aa), 1133 from 760 (Aa; normal 1050); +30 px. So every canon phone and both laptops get the collapsed card. With the card collapsed, Next ends exactly where it does on main at every size, both modes (the row wrapper measured against main's page: identical).
`verify-circle-theorem-spotter.py`: every item has an entry; every "=" chain outside `\text{}` true in SymPy (degrees stripped; the contract's unknowns x, y, OP, AB, d replaced by the key; 50 chains); in Chromium every wrong option of every item shows its lines in "Why" before Next, both copies alike, and a right answer shows none; at 15 sizes x normal/Aa, open card: Next within the fold; collapsed: no height (0.5 px). Plants caught: item 12's line made 118; no card on a wrong answer; the card below Next. Every existing check and plant passes. PASS, 21 s locally (was 6).
**Phone fit (measure-phone-fit --only, fallback fonts):** normal, Aa and laptop identical to main. check-answer-lock (--game), check-scroll-reveal --check, check-context-size PASS.
Todo §3 row WRONG-PAUSE-REASONS (one row); /updates/ line.
**Decided for you:** (1) each line is rendered as Surd's `workLine()` does: `\text{}` runs as plain words so a long sentence wraps on a 320 px phone (KaTeX's `\text` never wraps), the maths between rendered with `rk()`; (2) the collapsed label is "Why" too (short enough to sit beside Next in Aa at 320); (3) a lone capital letter in a chain (item 34's C and D) names the angle found and is not checked as a value; (4) the bands take the worst width's need in either mode, as Surd's do, so the open card shows only on tall desktop screens; (5) the /updates/ line is dated 20 Nov, the day it ships.

## 2026-11-20 (cloud): PACK-WORDING-VERSIONS (`docs/history/contracts/2026-11-20-pack-wording-versions.md`; Jon 20 Nov)

Agent Claude Code (cloud), branch `claude/nifty-faraday-13526r` restarted from main cbad9b0. Tier Small.
**Close-outs carried (first commit, 1f7cbe3):** #845 ESCAPE-WORDING, recorded in its entry below (check-site 44690793429, phone-fit-full 44690793221, pages 44690792634, all success).
Done on the branch: `tools/pack-generator/rooms/christmas-tree-fiasco/config.json` pack_version 3 -> 4, wording_approved 2026-11-13 -> 2026-11-20; `heatwave-mutiny/config.json` pack_version 2 -> 3, wording_approved 2026-11-17 -> 2026-11-20. Todo PACKS-V2-UPLOAD (the repo's record of the Tes versions; README :73 points to it) now names christmas-tree-fiasco v4 replacing v3 (Tes 13656567) and heatwave-mutiny v3 replacing v2 (Tes 13669810), for Jon to upload; no PACK-RELIST row (the record exists). New §4 row ESCAPE-KEYPAD-FLAKY.
**Built here with --final (not committed, uploaded or attached; dist-packs/ is gitignored):** christmas-tree-fiasco-pack-v4.pdf, 36 pages, 21060 KB, no DRAFT, eric-clipboard 15.0 pt (up to 10 lines), prize-leaflet 19.0 pt (up to 7 lines); heatwave-mutiny-pack-v3.pdf, 36 pages, 17764 KB, no DRAFT; the Patrol window brief prints no fit line, and the build fails a locks page whose briefs leave too little working space (its plant), so exit 0 is the proof. Both exit 0.
**Decided for you:** the replacement note went into the existing PACKS-V2-UPLOAD row rather than a new one, as the contract allows.
**MERGED 20 Nov as 504bae6 (#847)** at 08:22:14 UTC (head 86e3d37), route merge-pr.py. Main on the merge commit, read from the API by CIRCLE-WORKING: check-site 44701989506 success, phone-fit-full 44701989671 success (both push, attempt 1), pages build and deployment 44701989105 success. Closed out by CIRCLE-WORKING's first commit; contract moved to `docs/history/contracts/`.

## 2026-11-20 (cloud): ESCAPE-WORDING (`docs/history/contracts/2026-11-20-escape-wording.md`; Jon 20 Nov)

Agent Claude Code (cloud), branch `claude/nifty-faraday-13526r` restarted from main 3d6ce66. Tier Small.
**Close-outs carried (first commit, e7fdf69):** #843 CORE-PAPERS-NO-LETTERS, recorded in its entry below (check-site 44686407010, phone-fit-full 44686407025, pages 44686406533, all success).
Done on the branch, Jon's wording verbatim: christmas-tree-fiasco/room.js:46 "WARMS AT A CONSTANT RATE: {{ct.g}} °C EVERY {{ct.h}} HOURS ONCE UNLOADED"; :48 "THE REAL STAND ADDS {{sc.s}} cm"; heatwave-mutiny/room.js:127-129 "...set off until the first time it is safe to cross: the first time all three are back together, and it will let you through at that moment and no other." (the lock is the LCM of three patrol loops, so "all three" matches it). No variant, answer, hint, solve, missSays or wrongLine touched. No teacher page, alt text, pack config or verifier quotes the old strings (only docs/lock-bank-batch13.txt and docs/heatwave-mutiny-sanity-check.md, records of the authoring, left as history).
**Checked locally:** check-escape-rooms, check-canon-rooms, check-lock-bank, test-escape-{analytics, art, credit, dial, format, keypad, order, rating, setcodes, times}, test-pack-generator, build_pack.py --selftest (67/67): all exit 0. test-escape-keypad failed once in the 15-way parallel run (kiln-disaster fixture: "Set with nothing typed ... clock 15:00 -> 14:59", a room this PR does not touch); alone it passes twice on the branch and twice on main: load, not this change. Both packs built locally (dist-packs/, gitignored, not uploaded, pack_version unchanged) to prove the longer labels fit: christmas-tree-fiasco v3, 36 pages, eric-clipboard 15 pt, prize-leaflet 19 pt; heatwave-mutiny v2, 36 pages; both exit 0.
**STOP IF hit (reported; nothing rebuilt):** the listed packs on Tes carry the old wording (the pack prints each clue's `<b>` part on the art and each lock's brief on the locks page): Christmas Tree Fiasco pack v3 (Tes 13656567, printables/index.html:122): the clipboard and the leaflet; Heatwave Mutiny pack v2 (Tes 13669810, :197): the Patrol window brief. Decision for Jon: rebuild both with pack_version raised (v4 and v3) and replace the Tes files (the PACKS-V2-UPLOAD route), or leave them.
**Decided for you:** (1) the room edits went ahead (the STOP IF says report and don't rebuild, not change nothing); (2) the brief's line broken at "and it ' +" to keep the source's line length.
**MERGED 20 Nov as e769730 (#845)** via `merge-pr.py 845 --watch --wait 3600`, exit 0, last line "main e769730 run 44690793429: GREEN" (Gate 44689057748 and the branch's dispatched phone-fit-full 44689054796 green on aee250a first). Main on the merge commit, read from the API: check-site 44690793429 success, phone-fit-full 44690793221 success, pages build and deployment 44690792634 success. Jon's answer on the packs: new versions (PACK-WORDING-VERSIONS). Closed out by PACK-WORDING-VERSIONS's first commit; contract moved to `docs/history/contracts/`.
Record: agent Claude Code; wall n/a (not timed); review cycles 0; amendments 0; usage n/a.

