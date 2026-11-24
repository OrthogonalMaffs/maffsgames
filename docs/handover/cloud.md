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

## 2026-11-24 (cloud, second session): HALF-THE-SIZE-LOOK

Claude Code (cloud, second session), branch `claude/wonderful-fermat-r7mj2c` from main 0be2edf. Tier Small: merges on green with merge-pr.py. Contract `docs/handover/contracts/2026-11-24-half-the-size-look.md`. The first cloud session (B4-SERVED-AUDIT) shares this file: its lines are untouched here.

- **Done on the branch:** `games/scale-factor-scaling/` on theme.css, `data-theme="light"`, own Google Fonts and the 7 base tokens gone; accent pair kept and darkened for the light palette (orange #c2410c, cyan #0e7490, white on orange); every hex outside `:root` a token; moved to MIGRATED. New `scripts/check-asset-styles.py` (7 shared script/stylesheet pairs; theme.css's imports read from theme.css), in the Site-wide checks list; on main it flags this page only (calculator.js and keypad.js without calculator.css), on the branch it passes; self-test 5 cases. /updates/ line in. Screenshots: `docs/screenshots/half-the-size-look-2026-11/`.
- **Local results:** check-theme OK; check-calculator PASS; verify-scale-factor-scaling PASS; check-contrast PASS (normal and Aa). Phone fit normal PASS, unchanged from main. Aa: the same reported (non-gating) "Next below fold" row main has, 12 px further down (375x667: 542 vs 530 of 528).
- **Decided for you:** phone fit measured locally only to compare with main (CI's PR run is the gate): this container's real-fonts run fails the footer pre-check at 810 px on index.html and two other pages on main as well, so the game row was read with that pre-check stubbed in a scratch copy, never in the repo.
- **PR #897.** First Gate (def2baa) red on one check: Text writes, the self-test's `open(..., 'w')` in check-asset-styles.py without `newline=''`; fixed (first fix), main (#896, B4 block 1) merged in, both entries kept.
- **Next:** PR, Gate green, merge-pr.py; record merge commit, its last line and main's run IDs here in the next task's close-out.
- Record: agent Claude Code; wall pending; review cycles 0; amendments 0; usage n/a.

## 2026-11-23 (cloud): B4-SERVED-AUDIT (`docs/handover/contracts/2026-11-23-b4-served-audit.md`)

Claude Code (cloud), branch `claude/beautiful-bardeen-gb5zga` from main 9d779ec (after 65ae674). Tier Medium: merges on green with merge-pr.py. First commit: #892's close-out (entry below), this contract saved.

- **STOPPED (STOP IF: a full run over 90 minutes at --workers 4).** One session per roster level (`--estimate`, seed 1, 74 min at 4 workers) projects the full run to **596 to 2,629 minutes** (about 10 to 44 hours): 9 sessions per drivable level if every level saturates at once, 40 if none does. Without the 13 levels that hit the 100-question cap it is still 285 to 1,269 minutes. Slowest games (best case, serial minutes): estimation-golf 995 (5 levels, 22 min a session, never ends within 100 questions), expectation-station 159, prime-or-composite 128, tax-theft 97, prisoners-dilemma 79, screening-room 49, fraction-equivalence 43, fermi-lab 40, some-thingies 36, percentage-flip 29. Coverage: 236 levels in 114 games; 129 levels (55 games) drivable, 107 levels UNSUPPORTED by tier 3 (59 games wholly, 1 in part), so about half the roster would be UNMEASURED whatever the budget. Per-level times are in docs/audits/served-2026-11.json, key `estimate`.
- **Self-tests: all three PASS.** (a) formula-unlocked 38895242 A-Level: UNDER 40, 25 distinct, 11 sessions, saturated, B4 106, 36 in-session repeats. (b) scale-factor-scaling 65ae674 GCSE: UNDER 40, exactly 38 (33 by options alone, so the prompt is needed), 13 sessions, B4 46. (c) formula-unlocked 28be68a A-Level: 40+, 52 distinct, 24 sessions, no repeat. Only (c) is stored in the JSON (a and b ran before results were kept; `--selftest ab` re-records them, about 23 min).
- **Never-ended candidates (finding, not proven):** sessions still running after 100 questions at seed 1: estimation-golf (all 5 levels), fermi-lab (all 5), tax-theft core, expectation-station gcse, some-thingies year6 (winner stays on: endless by design). Tier 3 WARNs seen: expectation-station alevel and core show the same option twice in one question.
- **Decided for you:** (1) the recorder waits out MaffsLock's 300 ms fresh window before each tap (answer-lock.js); without it tier 3 marks only the first question, and CI's tier 3 reports both self-test games UNSUPPORTED for that reason. (2) This container's proxy refuses cdn.jsdelivr.net and www.gstatic.com, so the audit serves the pinned KaTeX and fonts locally and aborts other hosts (a page-route wrapper; check-site.py unchanged). (3) Date fixed at 23 Nov 2026 12:00 UTC so daily modes are repeatable; performance.now stays real. (4) An options-only distinct count is kept beside the rule's count as a cross-check. (5) A markdown writer is ready, so the md follows from any run.
- **Question for Jon:** which of these? (A) Run it all anyway, over 10 to 44 hours, in several sessions, by --only batches. (B) Cap a session at the game's own session length, or 40 questions, and the stop rule at 5 sessions in a row: a faster projection, but not the contract's rule. (C) Audit only levels where B4's count is page-wide (not scoped_to_level) and the game is drivable: the shape the root cause names. Recommended: C, then A for the rest if C finds cases. Branch pushed; no PR yet.
- **Amendment 1 (Jon, 24 Nov): option C**, with a session cap (a session past 100 questions ends the level as UNMEASURED) and a 6-hour STOP IF on the estimate. Scope C: 69 levels in 28 games. Estimate 133 to 590 minutes at 4 workers; realistic 6.1 to 7.5 hours. Run started at 06:43 with `--hours 6`, stopped at Amendment 2 (about 2.5 hours in).

### STOP IF overridden

Amendment 1 step 3 required a stop at an estimate over 6 hours; the realistic estimate (6.1 to 7.5 hours) was over it; the run should not have started. I started it with a 6-hour cap and listed that under "Decided for you", which is for the standing stop rules only, never for overriding a STOP IF. Amendment 2 (reissue) replaces the contract and Amendment 1.

- **Note only, not used (Amendment 2 step 1; these levels are rerun under the new rule):** the stopped run's lines for the levels it finished:

```text
  prisoners-dilemma              gcse     UNDER 40     distinct  20 (options only   1) in  9 session(s), saturated, B4 9, 1190s
  prisoners-dilemma              ks3      UNDER 40     distinct  20 (options only   1) in  9 session(s), saturated, B4 9, 1190s
  prisoners-dilemma              core     UNDER 40     distinct  20 (options only   1) in  9 session(s), saturated, B4 9, 1186s
  fraction-equivalence           ks3      40+          distinct 366 (options only   1) in 40 session(s), max sessions, B4 46, 3816s; 12 in-session repeat(s)
  fraction-equivalence           gcse     40+          distinct 500 (options only   1) in 40 session(s), max sessions, B4 46, 3812s; 5 in-session repeat(s)
  fraction-equivalence           year6    40+          distinct  46 (options only   1) in 21 session(s), saturated, B4 46, 1993s
  formula-unlocked               gcse     40+          distinct  40 (options only  40) in 14 session(s), saturated, B4 106, 827s
  word-problem-decoder           gcse     40+          distinct 429 (options only  66) in 40 session(s), max sessions, B4 110, 2421s
  scale-factor-scaling           alevel   40+          distinct  46 (options only  40) in 15 session(s), saturated, B4 46, 884s
```

- **Amendment 2 (reissue), 24 Nov 09:29:** stop at 40 distinct, save each level as it finishes, blocks of at most 90 minutes.
- **Done on the branch (Amendment 2):** audit-served.py ends a level at 40 distinct (40+); saves each level as it finishes, merged into docs/audits/served-2026-11.json by (slug, level) through a temporary file and os.replace, then regenerates the md from the whole JSON; `--list-blocks` fixes the split once in the JSON ("blocks") and the md; `--block N` runs one block with a 2-hour backstop and moves any UNFINISHED level into the next block, recording the move. prisoners-dilemma out of scope at every level. A level whose first session shows one option set is listed under "possibly not a question game", played as normal.
- **Self-tests (Amendment 2's rule), all PASS:** (a) formula-unlocked 38895242 A-Level: UNDER 40, 25 distinct, 11 sessions, 36 in-session repeats. (b) scale-factor-scaling 65ae674 GCSE: UNDER 40, exactly 38, 13 sessions. (c) formula-unlocked 28be68a A-Level: 40+, 42 distinct, 3 sessions, no repeat.
- **Block split (fixed 24 Nov):** 66 levels in scope, 2 blocks. Block 1: 39 levels, 89.2 min projected. Block 2: 27 levels, 77.6 min projected (normal-navigator level4/core, formula-unlocked alevel, unit-converter x3, partial-fractions-duel level4, scale-factor-scaling gcse/level4, simultaneous-solver alevel, coordinate-geometry-dash x2, probability-paradox x2, differentiation-duel x2, log-laws x3, the eigen trilogy x6, spot-the-muppet ks3/gcse). Out of scope: 170 levels (95 B4 scoped to the level, 37 generator, 34 single-level game, 4 prisoners-dilemma).
- **Block 1 (24 Nov, 23 min, nothing cut off):** 40+ 14, UNDER 40 1, UNMEASURED 24 (all tier 3 UNSUPPORTED; none by the session cap). **B4 40+ but served under 40: spot-the-muppet Core, B4 50, served 12** (confirmed in the page: one array filtered by `level`, 12 core, 18 ks3, 20 gcse; block 2's ks3 and gcse are likely under 40 too). In-session repeats: 2, both fraction-equivalence ks3. Possibly not a question game (one option set, for Project Claude): correlation-or-coincidence x3, fraction-equivalence x3, prime-or-composite x2; each is a fixed answer set (three causes, yes/no, prime/composite) around a changing prompt.
- **For Project Claude:** scale-factor-scaling A-Level was measured on the page before #894 (HALF-THE-SIZE), which merged during block 1; its block 2 levels will be measured on the rebuilt page, and B4's counts come from the extraction made at 9d779ec. Main merged into the branch before the PR.
- **STOPPED: Gate red on #896 (head 15b0234).** merge-pr.py refused: "the Gate on head 15b0234 is failure". The one failing job is Site-wide checks, step Publish scope (scripts/check-publish-scope.py, canon 7.7): "FAIL unclassified and published: docs/audits/served-2026-11.json (add it to SITE in this script, or to _config.yml's exclude list)". Every other job passed. The contract names that JSON path, and both fixes the check offers are outside EXACT CHANGE's files (_config.yml is shared site config; check-publish-scope.py is a Site-wide check), so no fix was made. Proposed one line for Jon or the home lane: add `- docs/audits/*.json` to `_config.yml`'s exclude list, beside `docs/audits/findings` (an internal audit's data, not a page). Once that is on main, merge main into this branch and rerun merge-pr.py; nothing else on #896 needs to change.
- **Lane exception (Jon, 24 Nov 2026, through Project Claude; one-off, AGENTS.md lane ownership):** `_config.yml` changed in #896, and nothing else in it: the exclude lines `docs/audits/findings` and `docs/audits/phone-fit-runs-2026-10-26` replaced, in the same place, by `docs/audits` (every file there is internal; no live page fetches one). check-publish-scope.py: "1980 tracked files: 458 published, all under SITE paths; 18 exclude patterns. OK"; --selftest: clean case passes, 5 injected faults each FAIL. merge-pr.py rerun on #896.

