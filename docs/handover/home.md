# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-15 (home): ANSWER-LOCK-FLAKE (PR 1 of 2: the header badge and the leftover branch)

Claude Code, in a cloud session (the contract's lane is home; no WSL worktree), branch `claude/laughing-einstein-3hckbl`; contract `docs/handover/contracts/2026-11-15-answer-lock-flake.md`. PR 1 removes the "Built to be safe for school networks" badge from the homepage header (`index.html`, Jon 15 Nov 08:51); no other badge, style or order changed. PR 2, the answer-lock flake's cause, follows on the same branch name once PR 1 is merged.

- Header, measured in Chromium with the pinned Outfit (`scripts/fonts/`), the answers total showing: before #771 240 px, one row, at 1280, 1366 and 1440 px; on main 282 px at 1280 (the "Ugh, stats" badge alone on a second row) and 240 px at 1366 and 1440; after, 240 px and one row at all three, and at 1263, 1349 and 1423 px (the same screens with a 17 px scrollbar).
- Main's 282 px at 1366 (Project Claude's figure) appears only when Outfit does not load: in the fallback font the row needs 1,318 px and has 1,302. With Outfit it needs 1,253. After the change the row needs 1,013 px (1,060 in the fallback font) and has 1,199 at its narrowest laptop width, so it is one row either way.
- `art/answer-box-redraws`: nothing to delete. On 15 Nov the remote had no such branch (`git ls-remote --heads origin`, and GitHub's list of 42 branches). This session's copy of the ref still read 799748c, one commit on da84b07 adding only `art-incoming/prom-11-router-dial.png` and `art-incoming/rfi-10-plans-keypad.png`, so the content check the contract asked for was made. Todo row ANSWER-BOX-REDRAWS-BRANCH is closed (moved to `docs/history/todo-done.md`).
- Checks: this container cannot run the home lane's `check-changed.py` usefully (the KaTeX CDN is refused by its proxy); the Gate is the check, as for the cloud lane. Run by hand: see the PR body.

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

## 2026-11-13 (home): LOOP-PAGE1 (Amendment 1)

Claude Code (home lane), worktree `~/mg-loop-page1`, branch `claude/loop-page1`; PR #754; contract `docs/history/contracts/2026-11-13-loop-page1.md`. Start art for Six Sevens, Bruv and Like Terms Collector (`games/<slug>/assets/start.webp`, 1600 × 873, 91,232 and 176,708 bytes; the ESSENTIALS-ART pattern in both pages). `build_deck.py` `run_page()`: every pack's page 1 opens with the game's art (`game_art()`, read from the game folder) beside `loop_diagram()`, one loop step drawn from the first deck; the check fails a missing diagram, a diagram whose back its front does not answer, and art that exists but is not printed. `free_pizza.py`: a recurring decimal carries "(recurring)" under it and a dot 0.28em across (was 0.13em); the parser requires the label. Two plants, two controls: selftest 3 packs, 25 plants.

- Stopped once, ruled by Jon (13 Nov): the art moves the first control below the fold on phones (Six Sevens at 320 × 568 and 375 × 667; Like Terms at 375 × 667 and 390 × 844); accepted as it is, start screens being report-only for phone fit. The table is in the PR.
- Also ruled: the sources were two files in Jon's Downloads, not in a checkout (he confirmed which); PNG proofs are allowed (the ban is for art sources); the diagram's caption is outside page 1's 120-word count; ANSWER-LOGGING-WRONG's contract file is left for the cloud lane.
- Against main's `--final` builds: Six Sevens and Like Terms differ on page 1 only (pages 2 to 40 pixel-identical); Free Daily Pizza's six recurring cards and its answer sheets gain the label; all three still 40 pages. Todo LOOP-PAGE1-CHECK is Jon's look before Tes.
- Merged as 816679e (#754) by merge-pr.py on a green Gate, 13 Nov: main's check-site run 43517360052 success, phone-fit-full 43517359973 success (all three modes, both changed start screens among them). check-changed.py before the push: 58 checks, all passed. Done: merged and live; Project Claude's review and Jon's LOOP-PAGE1-CHECK follow. Cleanup: end-task.py removed the branch and worktree.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 1; usage n/a.

## 2026-11-13 (home): FDP-LOOP-CARDS (Amendment 1)

Claude Code (home lane), worktree `~/mg-fdp-loop-cards`, branch `claude/fdp-loop-cards`; PR #752; contract `docs/history/contracts/2026-11-13-fdp-loop-cards.md` (Amendment 1's text; the 19:10 contract was stopped before any code, on its own STOP IF: `build_deck.py` had to change). New `tools/loop-cards/free_pizza.py` and `decks/free-daily-pizza/config.json`: the third pack, FP-16, FP-24 and FP-32. The values and every printed form come from the game page's own FDP code, run each build in a node subprocess (`vm`, no browser; node on PATH or Playwright's, as `scripts/test-ga4-country.py` finds it and as check-site.yml puts it on PATH for `verify-test-the-claim.py`). `build_deck.py`: `free_pizza` in `ADAPTERS`, five plants, the pack count computed, the third slug in `--help`; nothing else. First commit also moved four merged home contracts (#726, #727, #728, #736) to history.

- Built (DRAFT, 40 pages): each deck one closed loop, every value once, all 15 S1 values in, pairs 2-2-3-3-3-3 (16), 4 each (24), 6-5-5-6-5-5 (32); fronts 57 pt, backs 30.5 pt with the value at 1.4 times that. The "/" of a stacked fraction is in the page's text and not in the PDF's (checked by extraction and by eye). Selftest: 3 packs, 23 plants. Six Sevens and Like Terms: all 80 pages pixel-identical to main's build, same page text.
- Deviation: page 1's extra line is "0.25 and 25% never both appear." The contract's sentence made page 1 126 words; the limit is 120 and was not loosened (todo FDP-LOOP-CARDS-APPROVE said so).
- Merged as 69a2a1a (#752) by merge-pr.py on a green Gate, 13 Nov: main's check-site run 43497247741 success, phone-fit-full 43497247777 success. check-changed.py before the push: 43 checks, all passed. Cleanup: end-task.py removed the branch and worktree.
- Close-out PR, Jon's instruction of 13 Nov: he approved Free Daily Pizza's loop-card wording, so its config's `wording_approved` is `{"by": "Jon", "date": "2026-11-13"}` and FDP-LOOP-CARDS-APPROVE is closed (moved to `docs/history/todo-done.md`). All three loop-card packs are approved; the `--final` PDF was built for him.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 1; usage n/a.

