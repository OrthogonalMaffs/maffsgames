# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-15 (home): MONOTONIC-CLOCK (the shared input windows on a clock that never jumps)

Claude Code (home lane), worktree `~/mg-monotonic-clock`, branch `claude/monotonic-clock`; contract `docs/handover/contracts/2026-11-15-monotonic-clock.md`. Jon's ruling (15 Nov 11:07): option 1 of todo row ANSWER-LOCK-WALL-CLOCK, now closed in `docs/history/todo-done.md`.

- **Changed:** answer-lock.js `now()`, keypad.js's ghost-click window and scroll.js's touch cancel read `performance.now()`, with `Date` only where `performance.now` is missing. Each window's two sides read the same clock. The window lengths and MaffsLock's API are unchanged. No game file changed, and none of the timestamp uses named in the contract changed.
- **Starting values:** keypad's `lastUp` and scroll's `touched` start at `-Infinity`, not 0. `performance.now()` counts from page load, so a 0 would have ignored a box's click in the page's first 600 ms. check-keypad plants the 0 and catches it.
- **Tests:** `test-answer-lock.py` "clock-step" steps `Date.now()` 10 s back, then 10 s forward, inside the fresh window. Its plant "the wall clock" fails it twice. `check-keypad.py` "Clock" does the same to the 600 ms window, at 100 ms and 700 ms, and with no step. It has two plants: both readings back on `Date.now()`, and `lastUp` starting at 0. Both are caught.
- **Load:** `test-answer-lock.py --no-plants`, six at a time for 20 rounds (120 runs), with six wall-clock steps of about -2.9 s during the rounds: 0 failed. Before this change, 18 of 120 failed.
- **The four Date.now() stubs were left as they are:** sequence-solver (the game's hidden timer; its sweep sets `NO_LOCK_FRESH_INIT`), trig-identity-duel (the game's time line; it waits FRESH_MS first), unit-converter (it already skews `performance.now()` with `Date.now()`) and test-top-scores (stored dates). Each still passes.
- MERGED: pending.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-15 (home): ANSWER-LOCK-FLAKE PR 2 (checks offline; the local flake parked)

Claude Code (home lane), worktree `~/mg-answer-lock-flake`, branch `claude/answer-lock-flake`; contract `docs/history/contracts/2026-11-15-answer-lock-flake.md`. The cloud session's draft (735f405, branch `claude/laughing-einstein-3hckbl`) is applied unchanged as this PR's second commit, and every claim in it was checked here.

- **Cause (a), CI (main run 43590939932, L7, trig-identity-duel):** `check-answer-lock.py`'s route aborted everything off the stub server except KaTeX, which went to cdn.jsdelivr.net. A page's 'load' waits for KaTeX's stylesheet and script.
  - Reproduced on unmodified main: KaTeX held 25 s gives "Page.goto: Timeout 20000ms exceeded" at 20.1 s, CI's error. Served from the pinned copy, the page loads in 0.1 s.
  - It is a class: 30 scripts carried the copied route, and 18 of them left KaTeX on the CDN (both counts re-counted here).
  - Fixed in `bank_common.offline()` / `offline_async()`, called by all 30, verify-cast-away and verify-log-laws. Guarded by `scripts/test-offline-routes.py` and check-answer-lock's self-test over a dead network.
  - The remainder (20 no-route scripts) is todo row CHECKS-OFFLINE-REST.
- **Causes (b)/(c), local (`test-answer-lock.py`): STOPPED** on the STOP IF "the cause is in a shared site asset". answer-lock.js times its window with `Date.now()`, and WSL steps the wall clock back about 2.5 s every 30 s. 18 of 120 load runs failed, every failing round held a clock step, and no round without one failed. Not fixed; the question for Jon is in todo row ANSWER-LOCK-WALL-CLOCK. LOCAL-CHECKS updated.
- MERGED 15 Nov as 5446ace (#777). Main on the merge commit: check-site 43709064790 success, phone-fit-full 43709064695 success. Local check-changed: 174 checks. Seven failed in the parallel run: test-top-scores was a real bug in the draft (`bc` out of scope), fixed. Four passed alone. HC Factor and Negative Number Line failed on unmodified main too (table in #777).
- The remote branch `claude/laughing-einstein-3hckbl` was deleted after the merge (Jon, 15 Nov). Its tip, 735f405, had landed byte for byte as #777's second commit, and the two #774 commits under it duplicated PR 1.

Record: agent Claude Code; wall about 2:30 (contract to PR 2 merge, both PRs); review cycles 0; amendments 1 (Jon's follow-up of about 10:00); usage n/a.

## 2026-11-15 (home): ANSWER-LOCK-FLAKE PR 1 (header badge, leftover branch)

Claude Code (home lane), worktree `~/mg-header-badge-trim`, branch `claude/header-badge-trim`; contract `docs/history/contracts/2026-11-15-answer-lock-flake.md`. PR 2 (the answer-lock flake) follows on a new branch once this PR merges.

- Jon ruled on 15 Nov at 08:51 ("remove the badge entirely please"), and the "Built to be safe for school networks" header badge is removed from `index.html`. No other badge changes. The wording stays on /op/ and /privacy/.
- Measured locally in Chromium (stub server, Outfit loaded). Header heights before, then after, the removal:
  - 1280 × 800: 282 px on two rows, then 240 px on one row.
  - 1366 × 768: 240 px on one row, then 240 px on one row.
  - 1440 × 900: 240 px on one row, then 240 px on one row.
  - Before #771 (4114eeac) it was 240 px on one row at all three widths.
  - The badge row now needs 1,012 px, against 1,257 px before.
  - Locally the row already fitted at 1366. Project Claude measured 282 px there, so the two renderers differ by a few pixels; after the removal there is about 245 px to spare at 1280.
- `art/answer-box-redraws` deleted from the remote after Jon's ruling of 15 Nov at 08:37. Before deleting, its only commit was confirmed as 799748c, adding only the two `art-incoming/` PNGs. Todo row ANSWER-BOX-REDRAWS-BRANCH moved to `docs/history/todo-done.md`. No cloud close-out should carry the branch.
- MERGED 15 Nov as dd03c87 (#773). Main on the merge commit: check-site 43699387814 success, phone-fit-full 43699387701 success (push run). Local check-changed: 63 of 63 passed.

## 2026-11-14 (home): UGH-STATS-HOME

Claude Code (home lane), worktree `~/mg-ugh-stats-home`, branch `claude/ugh-stats-home`; contract `docs/history/contracts/2026-11-14-ugh-stats-home.md`. The homepage gets three ways into /ugh-stats/: an "Ugh, stats" badge, last in the header row and styled like the white trust badges; the questions-answered total as a link; and a card at the top of the game list, shown only with the Statistics topic. All three are in `index.html`. `answer-count.js` and the other shared files are unchanged.

- The total link: `.answer-total-link:has(> .answer-total[hidden])` is `display:none`, so while the total is hidden the link takes no space and is never focused. answer-count.js puts "Updated every 5 minutes" inside the link, so it is linked too.
- Each link has its own `data-mfg-section` (`answer-total`, `ugh-stats-link`, `ugh-stats-topic`). analytics.js counts an item only inside a section, and test-section-clicks.py reads the sections from the page.
- On a phone, choosing a topic scrolls to the first result; with Statistics chosen, that is the card. The card ignores the level, search and New filters.
- Laptop: at 1280 px the new badge wraps onto a second row and the header grows from 240 to 282 px. It fits on one row at 1440 px. From 600 px down the badge row scrolls sideways inside itself, as before, so the header height on phones is unchanged and the row never wraps.
- **Not done: the art/answer-box-redraws branch is NOT deleted.** The STOP IF fired, so the branch is parked. It holds one commit, 799748c "Add files via upload", made against merge base da84b07. That commit adds `art-incoming/prom-11-router-dial.png` and `art-incoming/rfi-10-plans-keypad.png`, and `git diff 799748c c0cec86 --` on those two files is not empty: neither file is on main. #769 landed only WebP conversions, under `tools/pack-generator/rooms/*/art/`. The original PNGs exist only on that branch, so the next cloud close-out must not record the branch as deleted. Jon's question is in `docs/todo.md` row ANSWER-BOX-REDRAWS-BRANCH (§7).
- MERGED 14 Nov, 23:53 UTC, as 14f0a3c (#771), live on the homepage. Main on the merge commit: check-site 43655483437 success, phone-fit-full 43655483470 success. Local check-changed: 63 of 63 passed. The PR's first Gate failed only in Content verifiers 47, where the Playwright image pull from mcr.microsoft.com timed out and no test ran. This token cannot rerun jobs (rerun-failed-jobs returned 403), so an empty commit re-ran the Gate, and it passed: a flake.

Record: agent Claude Code; wall about 0:55 (contract to merge); review cycles 0; amendments 0; usage n/a.

## 2026-11-14 (home): UGH-STATS-CASE1-1DP

Claude Code (home lane), worktree `~/mg-ugh-1dp`, branch `claude/ugh-stats-case1-1dp`; contract `docs/history/contracts/2026-11-14-ugh-stats-case1-1dp.md`. Case 1 Q1 and Q2 ask answers per day to 1 decimal place (working to 3), and Q3 quotes those values. A typed question may set `dp: 1` in `UghStats.quiz`: the decimal keypad, and only the 1 dp value accepted ("90.9" or "90.90", never "91" or "90.8"). Cases 2 and 3 keep dp 0 and their unchanged code path. Game 2 must also show at least 0.1 a day.

- The 0.1 rule cannot bite before about 20 March 2027: 10 or more answers in at most 200 days is always 0.05 a day or more. Its plant therefore lets a game with 1 answer through.
- MERGED 14 Nov as 51bc881 (#768). Main on the merge commit: check-site 43646870538 success, phone-fit-full 43646870632 success. The local run's one failure, Shared answer lock in the parallel run, passed when rerun alone.

## 2026-11-14 (home): UGH-STATS-QUESTIONS

Claude Code (home lane), worktree `~/mg-ugh-q`, branch `claude/ugh-stats-questions`; contract `docs/history/contracts/2026-11-14-ugh-stats-questions.md`. Questions in every case (one widget, `UghStats.quiz()` in `schools/assets/ugh-stats.js`; each page passes its questions as data), Cases 3 (`ugh-stats/one-class/`) and 4 (`ugh-stats/flu-and-answers/`) with their `data.csv`, the foreword and two cards on the landing page, `schools/assets/launch-dates.json` (written once by `scripts/build-launch-dates.py`), B29 in Correlation or Coincidence (`MIN_BANK` 84 to 85 in its verifier), one privacy line.

- Launch dates: 108 of 126 came from the archive's history, read from the local clone `E:\jon\maffsgames` (remote `maffsgames-archive`; `gh` cannot see that repo from WSL) through a saved `git log` (`--archive-log`). None was left at 2026-10-02. A new game adds its own line; `check-ugh-stats.py` LAUNCH fails without it.
- Answers send `stats_question_answered` (level case1 to case4). `doPost` stores any event name and `mfg()` passes it unchanged, so no Apps Script change.
- Case 1 Q2's game 2 is Factor Theorem only when it has 10 or more answers; on 14 Nov it had 9, so the page asks about the lowest-answered game with 10 or more that has a launch date (It's on Sale!), named from its page's `<h1>`.
- Typed answers are worked in whole numbers (`UghStats.divide`); the working shows more decimal places when 1 place would read as a half that rounds the other way, so the working never disagrees with the answer.
- `.btn[hidden]` added: `.btn`'s `display` had overridden `hidden`, so a hidden button still showed.
- todo CONTENT-SAFETY-UGH-STATS: the SR-14 scan does not read `ugh-stats/`.
- MERGED 14 Nov as 8f2b84f (#766), after Project Claude's 21:25 follow-up (game 2 only an A level / Further Maths / Level 4 game, levels read from the home page's cards; Q3 names them) and Jon's ruling on the Case 4 place name ("Generalise it": the south-west of England, CSV column `daylight_hours`). Main on the merge commit: check-site 43644118236 and phone-fit-full 43644118171, both success.

## 2026-11-14 (home): UGH-STATS-PAGES

Claude Code (home lane), worktree `~/mg-ugh-stats`, branch `claude/ugh-stats-pages`; contract `docs/history/contracts/2026-11-14-ugh-stats-pages.md`. Four new pages under `/ugh-stats/` (landing, `half-our-games/`, `charts/`, `whos-playing/`), one loader and chart drawer `schools/assets/ugh-stats.js`, shared look `ugh-stats/ugh-stats.css`, gate `scripts/check-ugh-stats.py` (ci-line), sitemap, /updates/ entry, one canon line (section 3).

- Case 1's ten groups cut at floor(n i / 10): that, not "remainder from the top", reproduces the 12 November figures from that day's file (commit 0e426612). Quartiles are the exclusive method.
- The loader uses XMLHttpRequest: `serve-stubbed.py` replaces `window.fetch` with a stub that refuses.
- Jon's rulings, 14 Nov: "Ugh, stats" joins the one canonical footer on every page (`check-footer.py` `_LINKS`, `apply-footer.py`), overriding the contract; the landing page's "Figures below 10 are hidden" sentence is deleted and Case 2's can't-tell box gains "Figures below 10 are shown as <10: too small to mean anything."; the deviations are accepted; `ci-deps.py` is todo CI-DEPS-UGH-STATS, not changed.
- MERGED 14 Nov as 84848b8 (#763). Main on the merge commit: check-site run 43605958933 success, phone-fit-full 43605959013 success. The local check-changed run (248 checks, 6,522 s) failed 37: Publish scope was real (`ugh-stats/` added to SITE in `check-publish-scope.py`); the other 36 were browser verifiers timing out on a loaded machine, not rerun locally, and the Gate passed them. Phone screenshots: `docs/screens/ugh-stats/`. Open: Jon edits the /updates/ entry; todo CI-DEPS-UGH-STATS.

## 2026-11-14 (home): BACK-LINK-START

Claude Code (home lane), worktree `~/mg-back-link-start`, branch `claude/back-link-start`; PR #757; contract `docs/history/contracts/2026-11-14-back-link-start.md`. Nineteen games showed no link back to the games list on their start screen (the only ones were in a header hidden until Start, or on the results screen). Each now has `<a href="../../" class="back-link">← Back to Games</a>` as the first element of `#startScreen`, on the page's own `.back-link` rule; nothing else on any page changed. New gate `scripts/check-start-back-link.py` (ci-line, `--selftest && --check`): every `games/<slug>/index.html`, loaded at 390 × 844, must show a visible link to the site root or `/games/`; 7 plants fail, 4 controls pass.

- A standalone script, not a second gate in `measure-phone-fit.py` (the contract allowed either): that script runs only in `phone-fit-full.yml` (nightly, and after a push to main that changes a shared path), never on a pull request, and loads the 109 roster games, not all 111 pages. The ci-line runs in the Gate whenever a game or a shared asset changes.
- On main before the edits the gate failed exactly the contract's 19 and passed the other 92; after, 111 pass.
- On four pages (better-value, expected-damage, formula-plug-in, new-shapes) the page's own phone rule for `.back-link` draws the new link 20 px and 44 px tall, centred; on the other 15 it is 13 px, left. Style is todo 3.20's.
- Phone fit for the 19, main against the branch, three modes: every asking screen identical; Next after a wrong answer matched on quiet reruns (the driver's reading moves between runs of one tree). Start screens (report only): two first controls moved below the fold (expectation-station at 390 × 844, spot-the-muppet at 375 × 667); the table is in the PR.
- Merged as c6c9385 (#757) by merge-pr.py on a green Gate, 14 Nov: main's check-site run 43575260622 success; phone-fit-full 43575260595 success, its measure jobs skipped because no shared path changed (the nightly run measures every game). check-changed.py before the push: 90 checks, 88 passed; verify-negative-number-line.py and verify-decimal-detective.py failed locally and fail the same way on clean main (todo LOCAL-CHECKS); the Gate passed both. Done: merged and live; Project Claude's review and Jon's sample play follow. Cleanup: end-task.py removed the branch and worktree.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 0; usage n/a.

