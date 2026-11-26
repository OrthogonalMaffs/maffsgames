# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-26 (home): BASE-60-LIST (It's Just Base 60, Bruv is listed: portal, /essentials/, sitemap, spec map, hub, /updates/)

Claude Code (home lane), worktree `~/mg-base-60-list`, branch `claude/base-60-list`, PR #930. The contract is at `docs/history/contracts/2026-11-26-base-60-list.md` (verbatim). The first commit closed out CANON-PRIORITY.

- **Approval (Jon, 26 Nov 2026, 13:36):** "Base 60 looks fine, happy to list that, although I will check the lines".
- **Portal:** a card in KS3 and in GCSE, each a copy of Take a Walk's (New badge dated 2026-11-26, levels ks3 gcse, topic number, the keywords of `data/games.json`), placed last in its section: both sections are in listing order, newest last.
- **/essentials/:** one card in Number, after Unit Converter (the same reference, N13), "One level", `data-calc="non-calc"`. `scripts/check-resit-page.py`'s SUITE gains the slug in the same place, as that check's own rule requires (the suite and the page change together).
- **Spec map:** added to the N13 row. N13 is the DfE's "standard units of mass, length, time, money"; the row's own wording, "Unit conversions: length, area, volume", does not name time and is left as it is. For Project Claude: reword the row, or rule otherwise.
- **Hub:** a row with stage-1..stage-4, after How Many Parts?. The NOT_ON_HUB entry is gone; no override entry is needed (the check reads the four keys from the page).
- **Sitemap, /updates/, the roster** (row 116 in Resit Fluency Strand, 8 games; Unlisted, 8; "Look signed off by Jon, 2026-11-26."), and the two notes in `audit-register.py` and `check-theme.py`.
- **`docs/todo.md`:** BASE60-LIST rewritten to Jon's lines, its old row word for word in `docs/history/todo-done.md`; new row BASE60-AA-FOLD, without figures (Project Claude's follow-up of 26 Nov, 17:15: #929 had not merged, so the row points to the verifier's known list).
- **Not touched:** the game page, its verifier, `data/large-screen.json`, `data/games.json`.
- **Gate on the PR head 8cd19935:** check-site 45866316754 and phone-fit-full 45866316762, both green.
- **Merged** on 26 Nov as e367eb4 (#930, squash) via merge-pr.py, which ended "main e367eb4 run 45871430050: GREEN". Main on e367eb4: check-site 45871430050, the pages build 45871429603 and phone-fit-full 45871430115, all green (read back from the API).
- **MERGE TIMING slip (this lane's):** #927 (LARGE-SCREEN-LAYER) merged at 17:35 while merge-pr.py waited, left unattended. The contract said to merge main in and re-run the Gate first; it merged on the Gate from before #927 landed. Main's run on the combined state is green.

Record: agent Claude Code; wall 0:45; review cycles 0; amendments 0 (one follow-up); usage n/a.

## 2026-11-26 (home): CANON-PRIORITY (Jon's new priority order in canon §0.2; SR-35, playability beats personality on a phone; three backlog changes)

Claude Code (home lane), worktree `~/mg-canon-priority`, branch `claude/canon-priority`, PR #928. The contract is at `docs/history/contracts/2026-11-26-canon-priority.md` (verbatim). The first commit closed out DAILY-DEAL. Docs only.

- **Jon's rulings (26 Nov 2026, 13:40-14:14):** his own classes come second, after correctness; resit and grade 1–3 students are the core audience, with primary served through SR-33; on a phone, playability beats personality; Holey Moley folds into I Dropped My Ice Cream; "d by dx? Why?" is wanted for an assessment in about the 3rd week of January.
- **Canon §0.2:** seven priorities in place of six, in the contract's exact words. SR-33 now cites priorities 3 and 7. No other file cites a numbered §0.2 priority (searched canon, AGENTS.md, CLAUDE.md and `.claude/rules/`).
- **Canon §0.3:** SR-35 after SR-33. SR-34 stays reserved (todo LARGE-SCREEN-LAYER).
- **`docs/todo.md` §3:** new rows ICE-CREAM-GCSE and D-BY-DX; ICE-CREAM-LIST now waits for ICE-CREAM-GCSE.
- **Holey Moley:** its line is removed from "Game ideas, not yet built". The list keeps no record of folded ideas, and ICE-CREAM-GCSE names it.
- **First Gate on the PR head 18526de8, a flake:** check-site 45855085400 failed only on the PR budget (`verify-maffscards.py` part 1 at 201 s against 189 s; the close-out's contract move selects that verifier) and passed on Jon's full rerun; phone-fit-full 45855085259 green. merge-pr.py had refused on the first result.
- **Merged** on 26 Nov as a55da6b (#928) via merge-pr.py, which ended "main a55da6b run 45861149266: GREEN". Main on a55da6b: check-site 45861149266, phone-fit-full 45861149106 and the pages build 45861148815, all green (read back from the API).

Record: agent Claude Code; wall 0:25; review cycles 0; amendments 0; usage n/a.

## 2026-11-25 (home): DAILY-DEAL (MaffsCards gets "Today's deal": one deal a UK day, the same for everyone, with Jon's result on it)

Claude Code (home lane), worktree `~/mg-daily-deal`, branch `claude/daily-deal`, PR #919. The contract is at `docs/history/contracts/2026-11-25-daily-deal.md` (verbatim, as reissued by Amendment 1). No close-out rode on the first commit: MAFFSCARDS-CHALLENGE's is in #916, which stays open (Jon's ruling).

- **Jon's rulings (25 Nov 2026, 19:16-20:05):** a daily deal with his own result on it, set from a Google Sheet; a new Creator sheet with its own script; a Sheet line over 240 characters is skipped for a pool line; "Today's deal" at the top of the menu.
- **The deal:** the UK date (Intl, Europe/London) goes through the page's mix32 to a seed; the day's code is that seed at main / ten / hard, played through `deal(ch)` as a challenge. Normal and challenge play are unchanged (the recorded normal games still match).
- **Jon's result:** `games/maffscards/daily.json`, all nulls as committed. It shows only on its own UK date; a missing, unreadable or invalid file reads as not played.
- **The workflow:** `.github/workflows/maffscards-daily.yml`, started by hand only, runs `scripts/set-maffscards-daily.py` and commits the file as answer-counts.yml commits its figures. The four fields reach the script through the environment.
- **The Creator sheet:** `docs/apps-script-creator.js` and its runbook `docs/apps-script-creator.md`. No token, secret or Sheet id is in the repo.
- **Verifier:** units `pool`, `daily`, `dailyui`, `dailyfit` and six planted faults in their own unit, `dailyplants`; twenty-two plants in all, each caught.
- **Decided here (each for Project Claude's review):**
  - The repo has no personal-details check to call (the list is private, outside the repo), so the script drops a line holding an e-mail address, a web address, an @name or seven or more digits.
  - A daily game's detail ends " · challenge · daily" (challenge is still true).
  - A drawn daily game (not reachable in practice) reads "Nobody won this time."
  - The panel's one fixed sentence is a placeholder: "One deal a day, the same for everyone: main deck, first to 10, Marvin on Hard."
  - In Aa on a phone the panel's text is .8rem, so a 240-character line and the button fit one 320 x 568 screen.
  - The script also has `--check` (the committed file is all nulls or a valid result), run in CI beside `--selftest`.
- **The workflow file came from the cloud lane:** the home lane's token has no `workflow` scope and GitHub refused its push (25 Nov, 21:20), so the cloud lane pushed the file as b7b6b47f, from the text in the PR's first comment. It is byte-identical to the home lane's copy (checked with cmp).
- **Amendment 1 (Project Claude, 25 Nov, 22:20):** the first Gate (check-site 45704002404 on 21b142ec) failed on the clock-seed scan alone: today's UK date reaching the day's seed, which is the feature. The lane stopped, since `scripts/check-site.py` was outside the contract. The amendment allows one entry in `CLOCK_SEED_ALLOW` (`dayCode`), as Equatle and Free Daily Pizza have, and accepts the decisions listed below.
- **Not run:** the workflow itself cannot run before it is on main, so the bot's push to main is unproven until Jon's first row (STOP IF 1 would apply then).
- **Waiting on Jon after merge:** the runbook, from step 1; then his rewrite of the placeholder wording (`docs/todo.md` §6).
- **Gate on the PR head cf859e03:** check-site 45711640580 and phone-fit-full 45711640419, both green.
- **Merged** on 25 Nov as 6db4954 (#919) via merge-pr.py, which ended "main 6db4954 run 45715844895: GREEN". Main on 6db4954: check-site 45715844895, phone-fit-full 45715845154 and the pages build 45715843761, all green.

Record: agent Claude Code; wall 1:25 to the first Gate, which stopped it; review cycles 0; amendments 1; usage n/a.

## 2026-11-25 (home): MAFFSCARDS-CHALLENGE (MaffsCards gets "Challenge a friend": a code that gives two students the same deal and the same Marvin)

Claude Code (home lane), worktree `~/mg-maffscards-challenge`, branch `claude/maffscards-challenge`, PR #913. The contract is at `docs/handover/contracts/2026-11-25-maffscards-challenge.md` (verbatim). The first commit closed out THREE-GAMES-LIST.

- **Jon's rulings (25 Nov 2026):** "option 1 please" (a challenge code, not live two-player); challenge games are off the leaderboard; a 6-character code plus a link; both events carry a challenge flag, never the code; placeholder wording, which Jon rewrites after playing.
- **The code:** 5 data characters (settings and a seed, base 31) and a check character. One wrong character, or two neighbours swapped, never reads as a code.
- **Fairness:** a challenge deal has its own generator, and each of Marvin's choices a fresh one keyed by a 32-bit hash of (seed, his card, k). Nothing in a challenge game's play draws from rng; only Marvin's lines do.
- **Menu:** a "Challenge a friend" section under the start button: make a code (with its link, Copy link and Play it), or type one. `?c=CODE` fills the box and sets the options; it never starts a game.
- **Results:** one more line for a challenge game, nothing submitted, and "Play again" is a normal game at the same settings.
- **Analytics:** game_started and game_completed carry `challenge: true` or `false`; game_completed's detail ends " · challenge" when true. No new event.
- **Normal games:** unchanged. The verifier holds three seeded games recorded from main c788f401's page (deal, Marvin's choices, every round and line) and the new page plays them the same.
- **Verifier:** a `challenge` unit (codes, keys, fairness at all 8 settings, leaderboard, menu, the recorded normal games) and a challenge fit check; six new plants, sixteen in all, each caught.
- **Decided here:** in Aa on a phone a challenge game's results are set tighter, with the two buttons side by side, so the extra line keeps both above the fold at 320 x 568. A normal game's Aa results are as they were (its second button already ends 11 px under the fold; not this contract's).
- **Privacy page:** its list of what is collected is by kind ("which game was played", "session completion and score data"), not by parameter, so the flag does not make it untrue. Not edited.
- **Run IDs:** in the close-out, as usual.

Record: agent Claude Code; wall 0:50; review cycles 0; amendments 0; usage n/a.

## 2026-11-24 (home): THREE-GAMES-LIST (MaffsCards, Sums in Disguise and Some Thingies are listed)

Claude Code (home lane), worktree `~/mg-three-games-list`, branch `claude/three-games-list`. The contract is at `docs/history/contracts/2026-11-24-three-games-list.md` (verbatim, with Amendment 1). The first commit closed out TIER3-LOCK-FIX.

- **Approval (verbatim):**
  - Jon, 24 Nov 2026, 21:32: "lets release maffscards and the 2 primary games please."
  - Jon, 24 Nov 2026, ~21:35, answering Project Claude: "No Essentials cards" (portal KS3 section only; the two primary games stay on /class/ as now).
- **Portal:** three cards at the end of the KS3 section, New badges dated 2026-11-24. MaffsCards is `ks3`; the other two are `year6 ks3` and link `?level=year6`.
- **Also listed on:** the sitemap, the leaderboard hub (4, 5 and 8 boards), /updates/, and for MaffsCards the spec map (GCSE N4). MaffsCards' noindex is gone.
- **Roster:** #113, #114 and #115 are in KS3 Games (38), look signed off by Jon, 2026-11-24. Unlisted is 9.
- **Amendment 1 (Jon, in session):** check-spec-mapping.py failed the two primary games, which the contract keeps off the spec map. Jon chose "EXCEPTIONS entry (Recommended)"; both are in that script's EXCEPTIONS.
- **Coverage check:** it needed LEVEL_OVERRIDES entries for the two primary games' stage boards, as the contract allowed.
- **Todo:** MAFFSCARDS-LIST moved whole; the other two rows keep Jon's LINES rewrites and the class teacher's questions.
- **Screenshots:** the three cards at 1366 x 768 and 375 x 667, sent to Jon in session.
- **Merged** on 24 Nov as ee09c84 (#905) via merge-pr.py, which ended "main ee09c84 run 45497440759: GREEN".
- **PR head b8569cd:** check-site 45494570251 and phone-fit-full 45494570226, both success.
- **Main on ee09c84:** check-site 45497440759 success, phone-fit-full 45497440773 success, pages build 45497440296 success.
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/`, closed out by MAFFSCARDS-CHALLENGE's first commit.

Record: agent Claude Code; wall 0:40; review cycles 0; amendments 1; usage n/a.

## 2026-11-24 (home): TIER3-LOCK-FIX (tier 3 plays the games the 300 ms answer lock made it skip)

Claude Code (home lane), worktree `~/mg-tier3-lock-fix`, branch `claude/tier3-lock-fix`. The contract is at `docs/history/contracts/2026-11-24-tier3-lock-fix.md` (verbatim). The first commit closed out TIER3-COVERAGE-REPORT.

- **Fix:** tier3()'s contexts add `bc.NO_LOCK_FRESH_INIT`. quadratic-factoriser left tier3_exceptions.
- **Local, four shards as CI runs them, main 855fce7 then the branch:**
  - runs passing 49 to 188 of 355, questions 556 to 1799, 0 FAIL both times, KaTeX check clean;
  - games passing every run 10 to 52: the report's 39, plus estimation-golf, screening-room and spot-the-muppet;
  - expectation-station is no longer UNSUPPORTED but WARNs once (a repeated tile, which the driver expects there);
  - 64 games still have an UNSUPPORTED run.
- **Wall time:** shards took 8:06 to 9:19 locally (3:22 to 6:35 before). The CI step timeout is 12 minutes: cloud to watch.
- **Self-test:** new `--tier3-lock-selftest`: tier3() plays a planted lock page fully; with the init script emptied it is UNSUPPORTED after 1 question. CI does not run it until cloud adds it to the workflow.
- **Decided for you:** the planted page shows its next question 460 ms after a mark, not at once as the contract says. Shown at once, it is tapped 500 ms later, outside the window, and the plant is not caught (tested).
- **For Project Claude:** the tier3_exceptions entries for spot-the-muppet and expectation-station are now stale; not touched.
- **Merged** on 24 Nov as 590efd7 (#904) via merge-pr.py, which ended "main 590efd7 run 45489207767: GREEN".
- **PR head 87ccba6:** check-site 45486151268 and phone-fit-full 45486151312, both success.
- **Main on 590efd7:** check-site 45489207767 success, phone-fit-full 45489207373 success, pages build 45489206130 success. CI's tier 3 counts match the local ones on all four shards (486 to 557 s a shard).
- **Cleanup:** end-task cleaned up. The contract moved to `docs/history/contracts/`, closed out by THREE-GAMES-LIST's first commit.

Record: agent Claude Code; wall 1:05; review cycles 0; amendments 0; usage n/a.

