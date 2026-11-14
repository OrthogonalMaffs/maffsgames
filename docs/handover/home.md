# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-14 (home): BACK-LINK-START

Claude Code (home lane), worktree `~/mg-back-link-start`, branch `claude/back-link-start`; contract `docs/handover/contracts/2026-11-14-back-link-start.md`. Nineteen games showed no link back to the games list on their start screen (the only ones were in a header hidden until Start, or on the results screen). Each now has `<a href="../../" class="back-link">← Back to Games</a>` as the first element of `#startScreen`, on the page's own `.back-link` rule; nothing else on any page changed. New gate `scripts/check-start-back-link.py` (ci-line, `--selftest && --check`): every `games/<slug>/index.html`, loaded at 390 × 844, must show a visible link to the site root or `/games/`; 7 plants fail, 4 controls pass.

- A standalone script, not a second gate in `measure-phone-fit.py` (the contract allowed either): that script runs only in `phone-fit-full.yml` (nightly, and after a push to main that changes a shared path), never on a pull request, and loads the 109 roster games, not all 111 pages. The ci-line runs in the Gate whenever a game or a shared asset changes.
- On main before the edits the gate failed exactly the contract's 19 and passed the other 92; after, 111 pass.
- On four pages (better-value, expected-damage, formula-plug-in, new-shapes) the page's own phone rule for `.back-link` draws the new link 20 px and 44 px tall, centred; on the other 15 it is 13 px, left. Style is todo 3.20's.

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

## 2026-11-12 (home): LOOP-CARDS

Claude Code (home lane), worktree `~/mg-loop-cards`, branch `claude/loop-cards`; PR #745; contract `docs/history/contracts/2026-11-12-loop-cards.md`. New `tools/loop-cards/`: `build_deck.py` (layout, loop, checks), adapters `six_sevens.py` and `like_terms.py`, configs in `decks/<slug>/`, README. Both packs build (40 pages each: page 1, three answer sheets, double-sided pages 5–22, fold-over pages 23–40), DRAFT badge on until Jon approves (todo §6 LOOP-CARDS-APPROVE); `--selftest` passes both packs and catches all 15 plants. Six Sevens page 1 is exactly 120 words. Shout card: 42 at 23 pt under the shout line at 27 pt (shout = answer + 4 pt). Like Terms backs fit at 24 pt.

- Layout calls (SR-31), approved by Jon 12 Nov: "Which deck?" gained Double-sided and Fold-over page columns, so step 1's "Print it" can be followed; all fold-over pages come after all double-sided ones, so "(p. N)" is one range (p. 23–40); curly quotes.
- Imports from build_pack.py: offline_context, wording_approved, draft_badge, check_final, page, CSS, LOGO, esc, ignored_by_git, pdf_page_count. The footer string follows its build_html() (no public function); check_final's message names the pack-generator path, so build_deck.py re-raises it with its own.
- Found by the proofs, not the first check: the cut lines had zero length (a `height: 0` beat `top/bottom: 0`); the check now measures each line's drawn length.
- Merged as 74444a9 (#745), 12 Nov: main's check-site run 43295807424 success, phone-fit-full 43295807406 success. Done: merged and live (closed out by MULTI-PRINT, 13 Nov).

## 2026-11-12 (home): HOME-QUEUE-1111 close-out

Claude Code (home lane), worktree `~/mg-home-queue-closeout`, branch `claude/home-queue-closeout`, PR #742; stand-down and close-out from Project Claude, 12 Nov 2026, 16:22. The queue is finished; its contract moves to `docs/history/contracts/2026-11-11-home-queue-1111.md` (the entries below name its old path).

- PR 1 PACK-APPROVED #737, merge 7c73372: main's check-site run 43090717833 success, phone-fit-full 43090717891 success.
- PR 2 STAGE-EXIT-LABEL #738, merge 84e8bc0: main's check-site run 43172855407 success, phone-fit-full 43172855534 success. Its PR runs sat queued for about 10 hours after the 11 Nov GitHub Actions outage; the token cannot cancel runs (HTTP 403), so the PR was closed and reopened at 06:52 on 12 Nov, which started a fresh run and superseded the stuck ones (one concurrency group per PR).
- PR 3 WHOSE-SIDE-LISTING: stood down. The cloud lane did it as #740 (merged cddcdef, 12 Nov, a one-off lane exception, Jon 09:53). The home lane's prepared listing was never pushed; its local branch `claude/whose-side-listing` (commits 4777543a, 3402902e) and worktree were removed by hand, because end-task refused a branch with no PR.
- Remote branch `claude/compassionate-sagan-9myj6x` deleted: its one commit c31f4ac was on main by content (cherry-picked in #739, now in `docs/history/handover-cloud-archive.md`); `git ls-remote` no longer lists it.

## 2026-11-11 (home): STAGE-EXIT-LABEL (HOME-QUEUE-1111, PR 2 of 3)

Claude Code (home lane), worktree `~/mg-stage-exit-label`, branch `claude/stage-exit-label`, PR #738; contract `docs/handover/contracts/2026-11-11-home-queue-1111.md`. `schools/assets/stage-exit.js` build() sets the page's own `a.back-link` to "← Games" (or the script tag's `data-home-label`) before the HUD copy is made; no game page touched, and non-stage games keep "← Back to Games". Measured on all 10 stage-exit games at 1366x768, 390x844, 375x667 and 320x568, normal and Aa, row and HUD (160 measurements, a scratch probe on verify-stage-exit.py's own server and stage start): main's file has the HUD link's text overlapping `#calcBadge` by 6 px (its-on-sale) and `.hud-label` by 3 px (hc-factor) at 320 in Aa; with the change every one reads "← Games" with no overlap and no sideways scroll. `scripts/phone-fit-state.json` had no known-failure entry for any of the 10 games (PHONE-FIT-RED fixed the overflow in CSS), so nothing came off it. `measure-phone-fit.py --only <game>` in normal, `--aa` and `--laptop` for the 10: all 30 exit 0; the one FAIL row printed, `free-daily-pizza` in Aa (Next below the fold after a wrong answer), is identical with main's `stage-exit.js` and has no state entry, so it is not this change's. /updates/ line under November. No claim held.

## 2026-11-11 (home): PACK-APPROVED (HOME-QUEUE-1111, PR 1 of 3)

Claude Code (home lane), worktree `~/mg-pack-approved`, branch `claude/pack-approved`, PR #737; contract `docs/handover/contracts/2026-11-11-home-queue-1111.md` (three PRs, one at a time; PR 2 STAGE-EXIT-LABEL and PR 3 WHOSE-SIDE-LISTING follow). Each pack config carries `wording_approved` ({"by", "date"} or null; no key counts as null): christmas-tree-fiasco and kiln-disaster `{"by": "Jon", "date": "2026-11-07"}`. `build_pack.py` prints the DRAFT badge (its only draft marker: main's PDFs say DRAFT on pages 1 and 2 only) while it is null, fails a build whose approved room prints DRAFT anywhere (AUDIT_JS reads each whole page, head included), and `--final` refuses an unapproved room by name. Selftest 32/32 (three new plants: DRAFT on an approved page 1; an unapproved page 2 without its badge; `--final` on null and on a missing key) plus a control (approved: no DRAFT; unapproved: pages 1 and 2). Both packs rebuilt with `--final`: no DRAFT on any page; pages 3 onward pixel-identical to main's build at 150 dpi; on pages 1-2 every changed pixel is in one 280x47 px box at the top right that held only the badge and is blank paper now. Proofs `docs/screens/pack-approved/`. README: approval paragraph, page 1-2 lines. No page wording, layout, lockcheck.py, final.py or label fitting touched. No claim held.

