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

## 2026-11-16 (cloud): ANGLE-ACE-GCSE-45 (`docs/handover/contracts/2026-11-16-angle-ace-gcse-45.md`; Jon 11:15)

Agent Claude Code (cloud), branch `ccr-bd20fca4-euxido` from main 4c13e95. Small; merges on green, by merge-pr.py only.
**Close-out carried (first commit):** MERGE-ROUTE-RETIRE merged #794 by merge-pr.py (last line "main 4e7a25d run 43847525596: GREEN", exit 0) as 4e7a25d; main check-site 43847525596 success (10:31:06 UTC), phone-fit-full 43847525561 success (10:17:52 UTC), both push-triggered. Contract moved to docs/history/contracts/.
Done on the branch: the ten items appended verbatim (checked as an exact substring of the contract file; non-ASCII only U+00B0 and U+2212); headers :301 and :499 say 45; verifier COUNTS gcse 45; ledger B4 `angle-ace::gcse` gone (`extract-banks.py --only angle-ace`, then `check-banks.py --write-ledger --only angle-ace`; diff is that entry only, year6 B3 untouched); check-banks --only angle-ace exit 0, B4 0; /updates/ line.
Main checks: verify-angle-ace.py reports no FAIL on 85 items.
**STOPPED 11:59 (STOP IF: the self-test; DO NOT TOUCH: the verifier beyond COUNTS).** The self-test crashed before planting anything: `IndexError: list index out of range` at `scripts/verify-angle-ace.py:914`. The filter on the patched page's renders, keyed `(level, index, width)`, looked every key up in `banks['year6']` by index without checking the level, so a gcse key with index 40-44 (new with this bank) was out of range. Latent before: at 35 it silently let gcse renders with a matching index into `extra`.
**Amendment 1 (Project Claude, 12:10), done in the third commit:** `k[0] == 'year6' and` at the front of the :914 filter; the contract file replaced with the amended text. Full verifier, self-test included, from the repo copy: exit 0, all 8 planted faults caught, "PASS: 0 FAIL(s); 85 items (year6, gcse) measured at 320/390/1280 px".
**STOPPED 12:20, PR #795 not merged (closed by Amendment 2 below).** merge-pr.py: "REFUSED #795: the Gate on head ca3c956 is failure", exit 1. The only failed job is Content verifiers 85 (run 43863264772, job 133286571338), in "The 6 P's banks": "FAIL  angles.json is not what the game's questions generate; run gen-six-ps.py --write". `scripts/gen-six-ps.py` `topic_angles` builds `schools/assets/six-ps/angles.json` from Angle Ace's `QUESTIONS_BY_LEVEL.gcse`, so the ten new items change it. That file is under `schools/assets/` (DO NOT TOUCH). Locally, `gen-six-ps.py --check --only angles` reads 45 questions with no assertion (every answer recomputed from its fig, every label matched) and fails only on the committed file.
**Amendment 2 (Project Claude, 13:40), done in one commit:** `gen-six-ps.py --write --only angles` changed only angles.json (+228 lines; 35 to 45 questions, the first 35 unchanged); `--check --only angles` PASS ("1 banks match their games"; labels: 0 still faulty after moving); `gen-exam-topics.py --check` PASS; /updates/ line widened to the 6 P's; contract file replaced with the Amendment 2 text.
Next: Gate, merge by merge-pr.py, main's two runs.
**For the home lane, docs/todo.md:** close row 1.52 (GCSE now 45; the KS3 part already fixed by #333).

## 2026-11-16 (cloud): MERGE-ROUTE-RETIRE (`docs/handover/contracts/2026-11-16-merge-route-retire.md`; Jon's ruling 16 Nov 09:41)

Agent Claude Code (cloud), branch `claude/great-hypatia-7d9ksh` from main c73ea61. Small; merges on green, by merge-pr.py only.
**Close-out carried (first commit):** PERCENTAGE-FLIP-BANKS merged #793 as c73ea61, via the GitHub connection under the (now retired) merge-route ruling of 10 Nov. The merge message carried a literal skip marker in a closing line the merging session wrote itself, so no run started on main; check-site and phone-fit-full were started by hand (workflow_dispatch) on c73ea61 at 09:30 UTC, Jon's go-ahead: check-site 43840393393 success (09:43:31 UTC), phone-fit-full 43840399609 success (09:42:40 UTC). Contract moved to docs/history/contracts/.
Done on the branch: AGENTS.md's merge line (merge-pr.py only, either lane; if it cannot reach GitHub, stop, the PR waits; `gh auth status` is not the test); canon MERGE-ROUTE R1 replaced by its dated retirement note (R2 unchanged); this file's merge-route block and "Merges by the standing route" line replaced by one line.
**For the home lane, docs/todo.md:** close row 40 CLOUD-MERGE-TOKEN (cause found: `gh auth status` is a false test in cloud sessions, where the proxy authenticates `gh api`; route retired; merge-pr.py proved by this PR's merge); and the Percentage Flip rows listed under #793 below (3.11, LEDGER-B4-PERCENTAGE-FLIP, the percentage-flip parts of 1.35 and 1.36, proposed PERCENT-SUFFIX).

## 2026-11-16 (cloud): PERCENTAGE-FLIP-BANKS (`docs/handover/contracts/2026-11-16-percentage-flip-banks.md`; Jon's rulings 15 Nov 22:52)

Agent Claude Code (cloud), branch `claude/pensive-fermat-j6m1x8` from main 14b8711. Medium; merges on green.
**Close-out carried (first commit):** CONTENT-SAFETY-COVERAGE merged as d64b788 (#792); main check-site 43764352225 and phone-fit-full 43764352219, both success (read through the GitHub connection). Route: the PR does not record it; gh auth fails in cloud sessions ("Failed to log in to github.com using token (GH_TOKEN)", checked again here), so it was the GitHub connection under the standing ruling of 10 Nov 2026. Contract moved to docs/history/contracts/.
Bank checked first, from each question's own words: 120 keys and every equation in every working line, 0 disagreements (no STOP).
Done on the branch (PR #793): one level-keyed `QUESTIONS` (verbatim); `gameLevel` is `MaffsLevel.resolve` (year6 | ks3 | gcse, fallback ks3, no 'all'); deals 3/3/2/2 by band, Fisher-Yates; one `markAnswer()` (money() for £ with moneyInput on/off, else exact()) behind both Check and the card; format/unreadable never marked; KaTeX working, one line each; the card sized to its taller face (`fitCard()`); after a wrong answer the box, Check and Skip fold away. Portal card, Essentials (now GCSE: its data-key and label follow the link, check-resit-page requires it), spec-map N12, hub row, /updates/. extract-banks 40/40/40 scoped; ledger B4 entries gone (`check-banks.py --write-ledger --only percentage-flip`). f1-001 fixed. verify-percentage-flip.py rewritten: PASS, 6/6 plants, 59 s locally.
Fold, after a wrong answer, worst Next bottom (fold = height less 40): normal 389 at 320x568, 383 at 375x667. Aa mode (not in this contract): fits at 375x667 (550 of 627) but not at 320x568 on 44 of 120 questions (Next to 605 of 528): canon 7.6.1's known Aa gap.
**For the home lane, docs/todo.md:** close 3.11 and LEDGER-B4-PERCENTAGE-FLIP; mark the percentage-flip parts of 1.36 (MaffsAnswer, money to the penny) and 1.35 (extract-banks now counts 40 a level) done. **Proposed row PERCENT-SUFFIX:** a typed "35%" is 'unreadable' in MaffsAnswer (answer.js NUM takes no unit). Listed games that mark a typed percentage: chart-interrogator (:783, `suffix:'%'`), screening-room (:343, :935); percentage-flip (this PR); unlisted its-on-sale.

## 2026-11-15 (cloud): CONTENT-SAFETY-COVERAGE (`docs/handover/contracts/2026-11-15-content-safety-coverage.md`; Jon's ruling 14 Nov 22:46, item 3 of 3)

Agent Claude Code (cloud), branch `claude/nice-davinci-26hl5y` from main 7b00e6c. Close-out of ESSENTIALS-PHONE-FIT-PAIR (#788 6065fb6, #790 984851c) in the first commit. One PR, Medium, merging on green.
Done on the branch: `scripts/check-content-safety.py` no longer reads a hand list (GLOBS); it reads every `.html` and `.js` (git's tracked and untracked-not-ignored files, or a walk for a `--root` copy) outside a named `EXCLUDE` (.git, .github, .claude, docs, scripts, data, tools, firebase, node_modules, each with its reason), games and escape rooms first, each once. `guard()` fails a top-level folder holding an `.html` that is neither a published section (`SITE`, read from `scripts/check-publish-scope.py`, not copied) nor in `EXCLUDE`, and a published page or script that `EXCLUDE` would hide (docs/art/ is SITE inside docs). Selftest: 28 to 33 cases (a tier (a) word on an Ugh, stats page; a planted `newsection/`; a planted `docs/art/page.html`; the tree passes the guard; ugh-stats read). Files read 241 to 248: new, the six `/ugh-stats/` pages and `parents/guide.js`; 0 hits. Run time 7.3 s to 6.8 s locally. Todo row 52 moved to todo-done.
Decided for you: the contract's guard ("neither read nor in EXCLUDE") cannot fire when everything outside EXCLUDE is read, so its other side is the site's own publish classification; no second list of sections.
STOP (Plan red on ac9aa7a): `ci-deps.py --selftest` "docs-only change runs no verifier" -> 12, since verify-correlation-or-coincidence.py loads check-content-safety.py, which now loads check-publish-scope.py, whose literals (docs/todo.md fixtures) became its dependencies. Amendment 1 (Jon, via Project Claude, 15 Nov 20:45): route 1, the class fix in `scripts/ci-deps.py` (Gate-file STOP IF lifted for that file only).
**Rule, beside LINE-LIMIT-SCOPE (21 Oct 2026; #792, 15 Nov 2026):** when ci-deps.py follows a verifier's local imports, a site-wide check (a `scripts/check-*.py` not itself in a "Content verifiers" group) gives its own file and the files of the modules it loads, never their literals (paths, game slugs, self-test fixtures). `site_check()` reads the groups from checks(); no list of names.
Amendment 1 done: selftest PASS (docs-only -> the 11 always-run; a docs/art/ picture no page loads selects only the verifiers that read docs/art/ themselves; check-content-safety.py, check-publish-scope.py and games/correlation-or-coincidence/index.html each select verify-correlation-or-coincidence.py). Planted fault (`site_check()` returns False): docs-only -> 12, verify-correlation-or-coincidence.py, FAIL. `--explain` main vs after: verify-correlation-or-coincidence.py gains only scripts/check-publish-scope.py; 16 verifiers lose only an imported site-wide check's literals (check-site.py: .github/workflows/check-site.yml, scripts/checker-allowlist.json; check-banks.py: data/check-ledger.json, scripts/checker-allowlist.json; check-teacher-invite.py: .claude/rules/game-roster.md); none loses its game, a page it tests or a shared asset. Selftest 1 m 49 s locally, before and after.
Next: Gate, merge, main's two runs; the contract moves to history in the next cloud task's first commit.

