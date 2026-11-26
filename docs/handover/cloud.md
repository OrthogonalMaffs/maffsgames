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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (25 Nov):** main run 45574813288 on 8840795 (#906) red only in Content verifiers 26: unit-converter t4-003 (?level=level4, 'e': False); failed jobs rerun once, attempt 2 GREEN. **Flake (14 Nov):** main run 43590939932 on 6f37c69 (#760) red only in Answer lock L7: trig-identity-duel, `Page.goto: Timeout 20000ms exceeded` loading the page from the runner's own server (the merge touched no game, shared asset or checker; the job passed on the PR head); failed jobs rerun once, attempt 2 GREEN. **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk's random phone-fit reds (375x667 Aa, 320x568 normal) are fixed by TAKE-A-WALK-SEED** (no seed reads the clock; the Gate's clock-seed scan); its layout is todo row TAKE-A-WALK-PHONE-LAYOUT. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

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

## 2026-11-26 (cloud): CLASS-NAME-SCRUB (the real class's name, CLASS, and its teacher's surname, TEACHER, taken out of every file on main; invented examples in their place; `docs/handover/contracts/2026-11-26-class-name-scrub.md`)

Claude Code (cloud, lane 3), branch `claude/eager-cerf-10dqly` from main 4b1d749. Medium tier, merge on green. First commit: this contract and SOME-THINGIES-FACTS's close-out (in its entry below). This entry, like the contract, writes CLASS and TEACHER, never the words.
- **The example:** `CLASS_NAME_EXAMPLE` (scripts/check-site.py) is now "Example", an invented name; its comment says so, and that real names come only from MAFFS_CLASS_NAMES, never written in the repo. Every use of the example follows it: 18 files, the capitals form in test-kids-look.py's greeting case included. The apostrophe test case in scripts/test-kids-look.py uses the invented surname "D'Arcy". In docs, "Miss TEACHER" reads "the class teacher".
- **Served files:** class/index.html and schools/assets/kids-look.js change in comments only (two lines each); no behaviour changes.
- **scripts/ci-timings.json:** six keys (the plant name carrying the example) renamed by hand, values untouched: the step 5 search needs it; `ci-groups.py --check` passes.
- **Main merged in (c9acc5c):** the bot's repack on 4b1d749 rewrote ci-timings.json with the old plant keys; main's file taken, the six keys renamed again, both searches run again (empty). A repack from any main run older than this PR's merge would bring the keys back: search main again after the merge's own repack.
- **Searches (step 5):** `git grep -n -w -i CLASS` and `git grep -n -F TEACHER -- ':!docs/audits/served-2026-11.json'`: no output, exit 1, both.
- **Left alone, for Project Claude:** the fictional bank character with TEACHER's surname is also in games/spot-the-muppet/index.html:366 and games/terrible-advice/index.html:326, written with an escaped apostrophe (so the step 5 search does not match it); banks are DO NOT TOUCH. `scripts/check-todo-trim.py` (ci-held, not in CI) reports the two reworded todo rows as lost, as it must: their old words are the names.
- **Not closed out here:** DAILY-POLISH (#924, lane 2) is merged with its contract still in `docs/handover/contracts/`; the contract gave this lane one close-out.
- **Amendment 1 (Jon, 26 Nov 14:59):** the first invented name was itself a real class name at the school (a tree name); the example is now "Example". All three searches (CLASS, TEACHER, the first invented name, case-insensitive) return nothing. This lane stopped: check-site's class-name rule held the example as a whole word on every served page, and "Example" is an ordinary word on 29 of them.
- **Amendment 2 (Jon's ruling (a), 26 Nov):** the rule no longer holds the example. `class_name_names()` returns the MAFFS_CLASS_NAMES names only (the example dropped if listed); a hard-coded class link is refused whatever is held. test-kids-look.py: the string and comment plants use a MAFFS_CLASS_NAMES name, the link plant runs with no name held, and a new case proves the example is not held; PASS, all six page plants behave. canon §7.5's sentence on the rule reworded to match (one parenthesis). The test's earlier invented names are left, as Jon ruled.
- **For Project Claude:** no workflow sets MAFFS_CLASS_NAMES, so in CI the rule now checks hard-coded class links only; a real name in a page is caught only where someone sets the variable locally (true of real names before this change too).
- **Next:** the Gate, merge-pr.py, main's run.

## 2026-11-26 (cloud): SOME-THINGIES-FACTS (Some Thingies' Stage 4 gets a thingy in glasses beside each question and, after marking, the fact as plates; `docs/history/contracts/2026-11-26-some-thingies-facts.md`)

Claude Code (cloud, lane 3), branch `claude/elegant-fermi-a1d1ga` from main f060351, main 3172ba9 merged in. Medium tier, merge on green. No close-out carried (contract). One first name taken out of the saved contract (personal-details scan), marked there.
- **The page (games/some-thingies/index.html):** on `fact` and `missing` items `#sargeMini` holds `thingy(6)` (shown at every width by `.qcard.quiz`), reacting through the classes `settle()` already sets. `factPic()` runs in `settle()` after `fitCrowd()`: `plates(a, b)` (`missing`: answer plates of b) into `#pic`, class `fact`, `--ps` 18 px down a pixel at a time to 10 px, then no picture (`data-fact="off"`). `refit()` (resize, the ResizeObserver, `ST.ui.crowd`) sizes the crowd without the picture, then fits the picture again. `plates()` is unchanged.
- **Decided here (for Project Claude's review):** (1) the crowd: the picture is measured against the crowd as it stands (the contract's second way): past question 10 it shows only if the card, crowd and all, still ends above the fold, so it never changes the crowd's size; (2) the picture sits under the options and the line, above the working (CSS `order`), so the sum and the options do not move at marking; (3) a fifth plant (the picture drawn without looking at the crowd).
- **Measured, question 1, speaker showing, longest right line (items of 192 showing the picture after a right and a wrong answer / dropping it; smallest picture):** 320x568 normal 192/0 (10 px grown, 11 px kids), Aa 184/8 in both looks (m4-10x11, m4-10x12, p4-11x8, p4-8x11, p4-q11x8, p4-12x8, p4-8x12, p4-q12x8); 375x667 normal and Aa 192/0 (15 px grown, 14 px kids); 1280x720 normal and Aa 192/0 (18 px). Next above the fold on every item.
- **Past question 10 (18 sampled plays a unit: 1, 60 and a screen-filling crowd):** 320x568: no picture in any (the crowd leaves no room; normal and Aa, both looks); 375x667: 16 of 18 show in normal, 11 or 12 in Aa; 1280x720: 16 of 18 (not with the screen-filling crowd). For Jon: the first way (the crowd pushed under the fold) would show more pictures on small phones.
- **Verifier:** twelve units `facts <look> <W>x<H> <normal|Aa>` (docstring) and five plants; the plays run in batches, 7 to 12 s a unit in this container.
- **Merged, closed out (26 Nov, CLASS-NAME-SCRUB's first commit):** [#925](https://github.com/OrthogonalMaffs/maffsgames/pull/925) as 4b1d749, route merge-pr.py. The PR head's runs: check-site 45838276118 (Gate) and phone-fit 45838275992, each success. Main's runs on 4b1d749: check-site 45841229218, phone-fit-full 45841229223, pages 45841229064, each success (read from GitHub by this session, 15:00 UTC; the first commit went out while the first two were still running). Contract moved to `docs/history/contracts/`.

## 2026-11-26 (cloud): DAILY-POLISH (a reload of MaffsCards always shows Jon's latest daily result; the daily workflow's form takes 26/11/2026; `docs/handover/contracts/2026-11-26-daily-polish.md`)

Claude Code (cloud, lane 2), branch `claude/inspiring-knuth-b1nns9` from main f060351. Medium tier, merge on green. First commit: this contract and DAILY-FIT's close-out (in its entry below).
- **The page (games/maffscards/index.html):** daily.json is asked for as `daily.json?t=<Date.now()>`, a new address each load, so GitHub Pages' 10-minute browser cache never shows the file from before Jon's result. Nothing else in the load or the panel changed; cards.json's load is as it was.
- **Verifier (scripts/verify-maffscards.py):** in `dailyui`, each of the nine fetched-file loads must ask for daily.json exactly once, as `daily.json?t=<digits>`, and no two loads with the same query string; the requests are read from the browser (`open_page`'s new `seen` list), not from the page. One plant in `dailyplants` (the query string removed): caught. Run here: `--only dailyui` PASS; the seven `dailyplants` all caught.
- **The date (scripts/set-maffscards-daily.py):** `validate()` turns D/M/YYYY or DD/MM/YYYY with slashes (day first) into YYYY-MM-DD before every existing check; the file always holds YYYY-MM-DD; `check_file()` unchanged. Self-test 82 lines, PASS: the contract's good and refused dates, and more refused (a slash date two days old, tomorrow's, text after it, a slash with a dash, a three-digit day, no day; on 6 Jan 2027, 1/6/2027 refused and 6/1/2027 written as 2027-01-06). `--date 26/11/2026` wrote `"date": "2026-11-26"`. The refusal now reads "is not YYYY-MM-DD or D/M/YYYY" and quotes the date as typed.
- **Workflow and doc:** the form's date label names both formats (`.github/workflows/maffscards-daily.yml`); `docs/apps-script-creator.md` section 9 says the same.
- **Decided here (for Project Claude's review):** no /updates/ line (the contract names none; the panel's words and look are unchanged, only how soon a new result shows).
- **Next:** the PR, its Gate, merge-pr.py, main's run.

