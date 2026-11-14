# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-14 (home): UGH-STATS-QUESTIONS

Claude Code (home lane), worktree `~/mg-ugh-q`, branch `claude/ugh-stats-questions`; contract `docs/history/contracts/2026-11-14-ugh-stats-questions.md`. Questions in every case (one widget, `UghStats.quiz()` in `schools/assets/ugh-stats.js`; each page passes its questions as data), Cases 3 (`ugh-stats/one-class/`) and 4 (`ugh-stats/flu-and-answers/`) with their `data.csv`, the foreword and two cards on the landing page, `schools/assets/launch-dates.json` (written once by `scripts/build-launch-dates.py`), B29 in Correlation or Coincidence (`MIN_BANK` 84 to 85 in its verifier), one privacy line.

- Launch dates: 108 of 126 came from the archive's history, read from the local clone `E:\jon\maffsgames` (remote `maffsgames-archive`; `gh` cannot see that repo from WSL) through a saved `git log` (`--archive-log`). None was left at 2026-10-02. A new game adds its own line; `check-ugh-stats.py` LAUNCH fails without it.
- Answers send `stats_question_answered` (level case1 to case4). `doPost` stores any event name and `mfg()` passes it unchanged, so no Apps Script change.
- Case 1 Q2's game 2 is Factor Theorem only when it has 10 or more answers; on 14 Nov it had 9, so the page asks about the lowest-answered game with 10 or more that has a launch date (It's on Sale!), named from its page's `<h1>`.
- Typed answers are worked in whole numbers (`UghStats.divide`); the working shows more decimal places when 1 place would read as a half that rounds the other way, so the working never disagrees with the answer.
- `.btn[hidden]` added: `.btn`'s `display` had overridden `hidden`, so a hidden button still showed.
- todo CONTENT-SAFETY-UGH-STATS: the SR-14 scan does not read `ugh-stats/`.
- MERGED 14 Nov as 8f2b84f (#766), after Project Claude's 21:25 follow-up (game 2 only an A level / Further Maths / Level 4 game, levels read from the home page's cards; Q3 names them) and Jon's ruling on the Case 4 place name ("Generalise it": the south-west of England, CSV column `daylight_hours`). Main on the merge commit: check-site 43644118236 and phone-fit-full 43644118171, RESULTS.

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

## 2026-11-13 (home): MULTI-PRINT

Claude Code (home lane), worktree `~/mg-multi-print`, branch `claude/multi-print`; PR #749; contract `docs/history/contracts/2026-11-13-multi-print.md`. First commit: the contract and two close-outs (LOOP-CARDS below; SIX-SEVENS-WEIGHTING #748 in cloud.md, as the contract told home to carry it). `build_pack.py`: `split_clue()` takes one or more `<b>` parts (none is still a BuildError), prints them joined with " · " for `label_parts()` (unchanged) and joins the caption gap by gap with CAPTION-GAPS's three rules; `caption_problems()` also fails punctuation at a caption's start (opening quotes and brackets excepted). Three plants and two controls; selftest 45/45. README paragraph; todo rows ANSWER-LOGGING-WRONG (§1), CORE-PACKS-ROLL-PROM and CORE-PACKS-CAR-TRAP (§3).

- Proof (scratch `~/mp/mp_check.py`): for all 131 clues of the four packs' sets, main's `split_clue()` and this one give the same printed text and caption; all 143 pages of the four PDFs are pixel-identical to main's build at 150 dpi, with the same page text.
- Dry run (in the PR body): the 18 clue objects of Roll for Initiative, Prom Budget and Car Trap all pass `caption_problems()`, yet 12 captions do not read as sentences (":." and ",." left where a figure came out, or a clause cut short: "The blast is a, centred on the target."), and 5 printed texts need the words between their parts ("80 · 48 · 37 · 12"). Those rooms' contracts need `printed` and `caption` overrides; the check does not see doubled punctuation or a cut clause.
- Merged as a1e4db8 (#749) by merge-pr.py on a green Gate, 13 Nov: main's check-site run 43439246076 success; phone-fit-full 43439246104 failed on its first attempt (the normal-mode job's hosted runner lost communication after 55 minutes, no logs; laptop and aa passed) and succeeded on attempt 2, rerun by Jon, since the home token may not rerun. check-changed.py before the push: 44 checks, all passed. Cleanup: end-task.py removed the branch and worktree.
- Close-out PR, Jon's approvals of 13 Nov: The Library Jam's pack wording (18:12) and The Comic Caper's (18:14) approved; The Christmas Tree Fiasco and The Kiln Disaster re-approved (18:17, key pages checked). All four configs' `wording_approved` is `{"by": "Jon", "date": "2026-11-13"}`, so no pack carries the DRAFT badge and `--final` builds all four; todo rows WARMUP-PACKS-APPROVE and PACKS-REAPPROVE closed (moved to `docs/history/todo-done.md`). (Jon's first message gave the two times the other way round; his second is recorded.)
- Same PR, Jon's approval of 13 Nov (18:32): Six Sevens, Bruv's loop-card wording; `tools/loop-cards/decks/six-sevens-bruv/config.json` records it and todo LOOP-CARDS-APPROVE said so. Jon then approved Like Terms Collector's too (13 Nov): its config records it and LOOP-CARDS-APPROVE is closed (moved to `docs/history/todo-done.md`). No pack of either generator is unapproved.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 0; usage n/a.

## 2026-11-13 (home): CAPTION-GAPS

Claude Code (home lane), worktree `~/mg-caption-gaps`, branch `claude/caption-gaps`; PR #746; contract `docs/history/contracts/2026-11-13-caption-gaps.md`. `tools/pack-generator/build_pack.py`: `split_clue()` tidies the caption left when a clue's `<b>` part is taken out (three rules) and `caption_problems()` fails a broken one, naming room, object and caption; a clue image's config may carry print-only `printed` and `caption` (`check_overrides()` refuses them elsewhere), used once, on Library Jam's reset card (fits at 20 pt, six lines). The key's level line is `MaffsEscapeRating.rating()` from `rating.js`, loaded into `read_room()`'s blank page (`room_rating()`; no other asset); a lock with no grade stops the build. `read_room()`, `prepare()`, `build_html()` and `about_box()` each gained the rating; the four functions `tools/loop-cards` imports are untouched. Kiln's and Comic Caper's teacher notes open "A Warm-up room:". Kiln and Christmas are unapproved again (todo PACKS-REAPPROVE).

- Proof (scratch `~/cg/cg_check.py`, pypdfium2 at 150 dpi against main's build of the same day): Kiln 35, Comic Caper 24 and Christmas 36 clue captions come out word for word as main's; their 14, 12 and 12 evidence pages are pixel-identical; Library Jam's 24 of 36 captions change (trolley, jammed book, reset card, drop counter, in all six sets). The only other pages that differ are each key (page 4) and, for Kiln and Christmas, pages 1 and 2 (the DRAFT badge). Each key prints its derived level and no "Built for" line. Selftest 42/42.
- Deviation: with no room approved, the selftest's DRAFT control and its "DRAFT on an approved room" plant had nothing to run on (the plant went stale), so both now use an approved copy of the config.
- Open: a clue with no left part whose right part starts with a full stop would give a caption that starts with punctuation, which the contract's three checks do not name; no room has one.
- Merged as 1583a51 (#746) by merge-pr.py on a green Gate, 13 Nov: main's check-site run 43350581797 success, phone-fit-full 43350581730 success. check-changed.py before the push: 55 checks, all passed. Done: merged and live; Project Claude's review follows. Cleanup: end-task.py removed the branch and worktree.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 0; usage n/a.
