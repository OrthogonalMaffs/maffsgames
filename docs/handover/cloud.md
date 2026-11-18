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

## 2026-11-18 (cloud): SUMS-IN-DISGUISE-BRIDGE (`docs/handover/contracts/2026-11-18-sums-in-disguise-bridge.md`; Jon 18 Nov, evening; class plays it Thu 19 Nov)

Agent Claude Code (cloud), branch `claude/quirky-hamilton-n94lmq` restarted from main 620594f. Tier Small.
**Close-out carried (first commit):** #824 SUMS-IN-DISGUISE-NO-LABELS, recorded in its entry below; contract moved.
Done on the branch: Stage 5 bridges to the next ten (bridge = 10 - a, rest = a + b - 10, all from the item; bank untouched): take-off as before, the a cubes in a ten outline (a column of ten slots, a real button named by fill_ten), b cubes beside it; "a + ? = 10" on tiles 0 to 10 keyed to bridge; fill the ten by button or outline (bridge cubes slide in, the ten hops into the hat, tag 10t + 10, rest cubes stay); put-back and options unchanged. Working "38 + 2 = 40 / 40 + 4 = 44" (one line when rest = 0); read-aloud to match; ten_in_hat replaced by fill_ten in both looks; Stage 5's about text. The kid hand on the tiles sits over the 0 (never the key) so it never hides the answer (`pointAt` gained optional anchor fractions, defaults unchanged). Verifier: the outline, the key, the fill by both routes, the tag only after fill, the working and speech, the worst items (a = 1, b = 9) above the fold at 360 px; the exchange checks and plants replaced by five new ones. 30/30 plants. todo SUMS-IN-DISGUISE-LIST updated.
Next: PR, Gate and phone-fit-full, merge with merge-pr.py tonight.

## 2026-11-18 (cloud): SUMS-IN-DISGUISE-NO-LABELS (`docs/history/contracts/2026-11-18-sums-in-disguise-no-labels.md`; Jon 18 Nov, 12:21)

Agent Claude Code (cloud), branch `claude/quirky-hamilton-n94lmq` from main 5e53fd4. Tier Small.
**Close-out carried (first commit):** #823 SUMS-IN-DISGUISE-ONE-EQUALS, recorded in its entry below; contract moved.
Done on the branch: put-back draws the blocks with no label on any group (counts unchanged; drawBlocks no longer takes a label, its `.labelled`, `.gb` and `.glabel` CSS removed, nothing else used them); the put-back read-aloud is "Put it back on." alone. The verifier, for every Stage 1, 2 and 5 item in both looks at every step before marking, fails the answer or the regrouped tens (10t, 10c, 10(t + 1)) as a number in the play screen's text outside the tag, the little-sum line, the tiles and the options, or in what the speaker reads; fails any label or value under the blocks after put-back; and requires the put-back read to be the line alone. Plants: an "80" under the sticks of 70 + 10, and "70 and 10. Put it back on." (both caught); ONE-EQUALS' two label plants replaced by one for an empty cubes group. 28/28 plants. **Reading for Jon:** the tiles (0 to 10, 0 to 20) are excluded as an answer control, like the options. The counting note under the cubes (c, as the little-sum line shows it) and Stage 5's exchange note "10 + d" are steps before put-back, cleared at put-back, so they stay (DO NOT TOUCH, the steps); "10 + d" does show the answer's ones digit before the options appear: say if it should go too.
PR #824. PR's final checks on head 5f8037f: Gate 44305303189 and phone-fit-full 44305320869 green. MERGED 18 Nov 12:48:40 UTC as ddc11e6 (squash) via merge-pr.py `--watch --wait 3600`, exit 0, last line "main ddc11e6 run 44307480462: GREEN". Main on ddc11e6: check-site 44307480462, phone-fit-full 44307480521, pages build 44307479714, all success (read back from the API in SUMS-IN-DISGUISE-BRIDGE's first commit, which moved the contract to `docs/history/contracts/`).
Record: agent Claude Code; wall about 0:27 (contract about 12:21, merged 12:48); review cycles 0; amendments 0; usage n/a.

## 2026-11-18 (cloud): SUMS-IN-DISGUISE-ONE-EQUALS (`docs/history/contracts/2026-11-18-sums-in-disguise-one-equals.md`; Jon 18 Nov, 11:34)

Agent Claude Code (cloud), branch `claude/beautiful-goldberg-dh2a9w` restarted from main 33db4a1. Tier Small.
**Close-out carried (first commit):** #822 SUMS-IN-DISGUISE-ART, recorded in its entry below; contract moved.
Done on the branch: the rule, every rendered KaTeX string a line with at most one "=", a sum on its left and a single number or "?" on its right. The put-back question is the plain big sum; the blocks carry each group's value (tens, then ones; a tens item has no ones label). The exchange label is "10 + d". The working is one "=" a line ("40 + 20 = 60" replaces "6 tens = 60"; "7 + 5 = 12" and "20 + 10 + 2 = 32"). Read-aloud follows. The blocks clear once the answer is marked (the working repeats them), so Next stays above the fold at 360 px with the speaker showing (603 and 612 px before). The verifier collects every KaTeX string at every step of every item in both looks.
**Amendment 1 (Jon, 18 Nov):** a group with no blocks is not drawn and gets no label (81 + 9 shows only "90"); the verifier fails a label under a group with zero blocks (plant: a "0" under an empty cubes group). 27/27 plants.
**Jon, 18 Nov, about 11:55:** no further PRs in this session (context at 70%); every new job goes to a fresh cloud session.
PR #823. PR's final checks on head 51aa557: Gate 44298415647 and phone-fit-full 44298444369 green. MERGED 18 Nov 12:10:52 UTC as 5e53fd4 (squash), merged by Vector52F (merge-pr.py, the only route; its last line was not carried into the next session). Main on 5e53fd4: check-site 44301469818, phone-fit-full 44301469719, pages build 44301468786, all success (read back from the API in SUMS-IN-DISGUISE-NO-LABELS's session and recorded in its first commit, which moved the contract to `docs/history/contracts/`).
Record: agent Claude Code; wall about 0:36 (contract 11:34, merged 12:10); review cycles 0; amendments 1; usage n/a.

## 2026-11-18 (cloud): SUMS-IN-DISGUISE-ART (`docs/history/contracts/2026-11-18-sums-in-disguise-art.md`; Jon 18 Nov)

Agent Claude Code (cloud), branch `claude/beautiful-goldberg-dh2a9w` restarted from main 3eb2069. Tier Small.
**Close-out carried (first commit):** #821 SUMS-IN-DISGUISE, recorded in its entry below; contract moved.
Done on the branch: Jon's picture, byte for byte from `art/sums-in-disguise` ("start (1).webp", SHA-256 bfdd4ecd…4645, 54,110 bytes, 1600 x 873), as `games/sums-in-disguise/assets/start.webp`, under the title in both looks with Ice Cream's `.start-art` CSS; verifier checks the tag, size and SHA-256 (plant: no alt). **STOP IF hit and ruled (Jon, in session):** at 360 x 640 the picture moves stages 2-3 below the fold (stage 1 stays above); "Accept as is". **Amendment 1 (Jon, 10:38, "find 5 factorial"):** LINES.kids.find is now "Find {little} in disguise!"; the verifier fails any LINES string with "{little}" or "{big}" followed by "!" or "?" (plant: "Find {little}!"); Stage 4's read-aloud now reads the find line. Todo SUMS-IN-DISGUISE-LIST notes the picture.
**Amendment 3 (Jon, 10:45-10:53, tens on show; it replaces Amendment 2, the Stage 5 split, which was built but never committed):** Stages 1, 2 and 5 show the big sum as base-10 blocks; take off sends the t sticks into the disguise, parked in view beside the sum (tag 10t, or "0" on a tens item); the ones on tiles, then counted; in Stage 5 ten cubes become a stick into the hat (tag 10t + 10, "c = 10 + d", the Stage 5 reveal only now); put back (LINES' put_back) shows the regrouped question ("64 + 3 = 60 + 7 = ?") and only then the options; working and read-aloud to match; the kid hand on each step's button. Verifier checks every Stage 1, 2 and 5 item in both looks (7 new plants). Stage 5's method provisional (todo row).
PR #822. PR's final checks on head 36018fd: Gate 44291169060 and phone-fit-full 44291711282 green. MERGED 18 Nov 11:20 UTC as fca96ed (squash) via merge-pr.py `--watch --wait 3600`, exit 0, last line "main fca96ed run 44293850170: GREEN". Main on fca96ed: check-site 44293850170, phone-fit-full 44293849978, pages build 44293849198, all success (recorded in SUMS-IN-DISGUISE-ONE-EQUALS's first commit, which moved the contract to `docs/history/contracts/`).
Record: agent Claude Code; wall about 1:20 (contract about 10:00, merged 11:20); review cycles 0; amendments 3 (and one STOP ruled in session); usage n/a.

## 2026-11-18 (cloud): SUMS-IN-DISGUISE (`docs/history/contracts/2026-11-18-sums-in-disguise.md`; Jon 18 Nov)

Agent Claude Code (cloud), branch `claude/beautiful-goldberg-dh2a9w` from main 5e1c236. Tier Medium: merge on green.
**Close-out carried (first commit):** #820 I-DROPPED-MY-ICE-CREAM, recorded in its entry below; contract moved.
Bank: the generator reproduces SHA-256 19e41556…068a8; recomputed independently before building: 0 disagreements.
Done on the branch: the page (five stages, two looks from the fragment, LINES verbatim, the 67 after marking, boards `stage-1`..`stage-5`); `scripts/verify-sums-in-disguise.py` (PASS, 14/14 plants); roster row #113 in Unlisted (9); games.json and apply-meta; findings file; every list #820 touched; NOT_ON_HUB; launch date; todo SUMS-IN-DISGUISE-LIST and NUMBER-BONDS.
**Amendment 1 (Jon, 18 Nov, 09:19, "all 4 please"), in the saved contract:** questions as maths ("64 + 3 = ?"), the working stacked in KaTeX with the tens highlighted, one LINES string in feedback, the new kid set (6 words or fewer), take_off/find from LINES, the disguise a button, the kid hand on question 1, Read aloud on on-device voices only (hidden without one; tested against a mocked speechSynthesis). Built into #821.
PR #821. PR's final checks on head 8bb2d65: Gate 44277968798 and phone-fit-full 44278017720 green (the first head's Gate run was cancelled by the amendment's push). MERGED 18 Nov 09:56 UTC as e9f236e (squash) via merge-pr.py `--watch --wait 3600`, exit 0, last line "main e9f236e run 44280602409: GREEN". Main on e9f236e: check-site 44280602409, phone-fit-full 44280602129, pages build 44280601436, all success (recorded in SUMS-IN-DISGUISE-ART's first commit, which moved the contract to `docs/history/contracts/`).
Record: agent Claude Code; wall about 1:47 (contract about 08:50, merged 09:56, with Amendment 1 received 09:19); review cycles 0; amendments 1; usage n/a.

## 2026-11-18 (cloud): I-DROPPED-MY-ICE-CREAM (`docs/history/contracts/2026-11-18-i-dropped-my-ice-cream.md`; Jon 17-18 Nov)

Agent Claude Code (cloud), branch `claude/fervent-mccarthy-3l9b5u` from main bb46787. Tier Medium: merge on green, Project Claude reviews after. Jon teaches it Tue 24 Nov.
**Close-out carried (first commit):** #818 ITS-A-SINE-LIST, recorded in its entry below; contract moved.
**Amendments (Jon, 18 Nov, in session):** 1, lane exception: `gcse-stage-4` and `level3-stage-4` labels in firebase-leaderboard.js, and one launch-dates.json line (both under DO NOT TOUCH `schools/assets/`, which the per-level boards and check-ugh-stats need). 2: "no duplicate given" reads the given with its unit (gcse_005 61 cm and gcse_020 61 m).
Bank recomputed independently before building: 96/96 answers and traps agree, none within 0.005 of a boundary. PNG 1672 x 941 on the art branch; start.webp 1600 x 873.
Done on the branch: the page (two levels, four stages, 8 a run, boxes (a) then (b), Jon's lines, working cut to 4 d.p., formulas by level and stage, scientific calculator, cones drawn to proportion with the height label clear of the slant edges); `scripts/verify-i-dropped-my-ice-cream.py` (PASS, 6/6 plants caught); roster row #112 in Unlisted (8); games.json and apply-meta; findings file; every MIGRATED list; NOT_ON_HUB; todo ICE-CREAM-LIST.
PR #820. PR's final checks on head 7edee19: Gate 44268072982 and phone-fit-full 44268068543 green. MERGED 18 Nov 08:50:07 UTC as 5e1c236 (squash), merged by Vector52F (merge-pr.py, the only route; its last line was not carried into the next session). Main on 5e1c236: check-site 44270404391, phone-fit-full 44270405049, pages build 44270404235, all success (read back from the API in SUMS-IN-DISGUISE's session and recorded in its first commit, which moved the contract to `docs/history/contracts/`).

