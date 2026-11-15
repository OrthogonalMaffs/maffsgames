# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-15 (home): UNLIST-GRAPH-SKETCHER (Graph Sketcher off every list, page live; two todo rows)

Claude Code (home lane), worktree `~/mg-unlist-gs`, branch `claude/unlist-graph-sketcher`; contract `docs/handover/contracts/2026-11-15-unlist-graph-sketcher.md`. The first commit carries FOOTER-NO-SUPPORT's close-out (merge line below, contract to history).

- **Off every list (SR-21's list in reverse):** the roster row goes to Unlisted (#71, with its note and a dated bullet; Core 9 to 8, Unlisted 6 to 7); the portal card (index.html); sitemap.xml; the spec map's three rows (now "Graph Sketcher (being rebuilt)", as glorious-gantt's are); the hub row (leaderboards/index.html) and a NOT_ON_HUB entry (check-leaderboard-coverage.js). There was no weekly-fact, /resit/ or parent-guide link.
- **Kept:** data/games.json (check-meta needs one entry per roster row, unlisted rows too), launch-dates.json, firebase-leaderboard.js's names, check-ledger.json and the scripts' slug lists. The game page stays indexed and gains only the correction notice (follow-ups below).
- **/updates/:** Jon's line is verbatim at the top of November's list. The October "Wrong answer keys" line keeps its link (it lost it only while the page had noindex).
- **todo:** new rows GRAPH-SKETCHER-REDESIGN (11 points) and PACK-ART-EXTRAS ((a)-(d)), beside the print-pack rows in §3. todo-done's PACK-WORDING-1511 close note gains the re-tracked sentence.
- **Local checks (quick, not a merge condition):** check-meta, check-spec-mapping, check-canonical-links, check-look-signoff, check-levels, check-theme, check-analytics-loader, check-publish-scope, check-context-size and check-leaderboard-coverage all pass.
- **STOPPED 15 Nov, about 20:25, PR #791 not merged (STOP IF: a check would need loosening).** The Gate failed only in check-site's "Findings register" (audit-register.py:206-214, FACTS-AND-NOTICE, 14 Oct): "graph-sketcher is unlisted for faults but its page lacks <!-- maffs-correction-notice -->: add the correction notice". Passing needs either the notice banner on the game page, which is visible to students and outside DO NOT TOUCH ("beyond the noindex line"), or graph-sketcher in UNLISTED_NOT_BY_AUDIT, which loosens the check. Waiting on Jon and Project Claude.
- **Follow-up 20:35 (Jon 20:33), saved under the contract:** the noindex line is out, the October /updates/ link is restored, the notice (verbatim) and its CSS are on the start screen, and SR-20 has its sentence. **STOPPED again (its STOP IF: the notice changes the phone fit).** Start button bottom on main is 526 at 320x568, 469 at 375x667, 469 at 390x844 and 434 at 1280x720. With the notice at the top of the start screen (154 px tall at 320) it is 696 at 320x568 (fold 568: BELOW), 618 at 375x667 and 390x844, and 518 at 1280x720 (all above). Measured alternatives at 320x568: notice just above Start, 692 (BELOW); notice just after Start, 526 (above, the notice at 545-699, partly below the fold). Committed on the branch, not pushed (the Gate has not run on it).
- **Second follow-up 20:50 (Jon: option 1), saved under the contract; the stop is closed.** The marker and notice moved to just after Start, unchanged. audit-register checks only that the marker is on the page (:211), not where. Start's bottom edge, the same as on main: 526 at 320x568, 469 at 375x667, 469 at 390x844, 434 at 1280x720. The notice's top and bottom: 545-699, 489-621, 489-621, 453-521. audit-register --check, check-canonical-links, check-theme, check-content-safety and check-meta pass locally.
- **Third follow-up 20:55, saved under the contract (Jon, 20:50: "with the escape room section reduced, the "start with the hamster heist" is redundant, particularly as that is one of the 3 games currently showing. we need to remove it"):** the homepage band's last esc-note now reads exactly "Free, in a browser, nothing to install." (the " &mdash;" and the start-hamster-heist link are gone). `start-hamster-heist` was only in index.html: no check or analytics config held it. check-escape-rooms reads only an esc-note straight after a card, and test-escape-credit's fit is unaffected. Band layout: at 320 px the note goes from two lines to one (38 to 19 px), so the band is 19 px shorter (1554 to 1535); the cards, the button and the printables link do not move. At 1280 px the note is narrower (420 to 203 px) and the band is unchanged at 444 px. The merge watch on 9c5792ad was stopped before its Gate finished, so this could join the PR.
- MERGED: pending.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-15 (home): FOOTER-NO-SUPPORT (the Support MaffsGames link out of the site footer)

Claude Code (home lane), worktree `~/mg-footer-no-support`, branch `claude/footer-no-support`; contract `docs/handover/contracts/2026-11-15-footer-no-support.md`. The first commit carries HOME-LEAN's close-out (merge line below, contract to history).

- **check-footer.py:** `_SUPPORT` is gone, so CANONICAL is the ten `_LINKS` joined by `_SEP`, unchanged in order. apply-footer.py rewrote 152 pages, including the two test fixtures (check-footer scans them). Every page's diff was checked to be the footer's Support link and its separator only; a second run changes nothing.
- **site-footer.css:** the `.sf-long` media rule and the header comment's two lines about it are removed; nothing else changes.
- **Kept:** About's coffee button and the privacy page's Buy Me a Coffee section are unchanged.
- **Fit (local Chromium, / and /about/):** the footer is still 40 px. Its row is 808 px wide (it was 885 px), so at 320, 375 and 390 px it still scrolls inside itself, as it did before. No page scrolls sideways. At 1280 px it fits in one row.
- **check-footer has no self-test.** Plants were run by hand on a copy instead: a page still carrying the Support link FAILS ("footer differs from the canonical markup"), and a page with its footer removed FAILS ("no footer").
- No other check needs the link: check-site's 'buy me a coffee' is a skip-list entry, and verify-the-6-ps strips the footer before its emoji check.
- /updates/: no line (a footer tidy). todo: none.
- MERGED 15 Nov as 8791910 (#789). Main on the merge commit: check-site 43753882335 success, phone-fit-full 43753882351 success; the live footer ends at Feedback and About keeps its coffee button. end-task removed claude/footer-no-support.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-15 (home): HOME-LEAN (neither lane runs check-changed.py before pushing)

Claude Code (home lane), worktree `~/mg-home-lean`, branch `claude/home-lean`; contract `docs/handover/contracts/2026-11-15-home-lean.md`. The first commit carries ESC-BAND-SLIM's close-out (merge line below, contract to history).

- **AGENTS.md:** the two pre-push lines (home runs check-changed.py; cloud does not) are one rule for both lanes: the PR's Gate is the check, local runs are optional and never a merge condition, and the by-hand list is the personal-details scan, the skip-CI word check, the selftest of touched scripts and the §7.8.4 worst-case test. 299 bytes.
- **Canon:** §7.8's pre-push and "which lane" lines carry the new rule, with the 7 Oct note kept as history (CI minutes are free). §12 has a HOME-LEAN section after CLOUD-LEAN (Jon's two rulings, the measured cost, the by-hand list); CLOUD-LEAN's home-lane line now points to it. SR-27 is marked superseded, its text kept.
- **docs/rules/scripts.md:** its SR-27 pointer now says check-changed.py is optional and SR-27 is history. CLAUDE.md has no such line.
- Not run: check-changed.py (this ruling). By hand: the personal-details scan, the skip-CI word check, check-context-size.py.
- todo: none.
- MERGED 15 Nov as 4809d1a (#787). Main on the merge commit: check-site 43749922722 success, phone-fit-full 43749922791 success. end-task removed claude/home-lean.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-15 (home): ESC-BAND-SLIM (the homepage escape-rooms band down to three rooms; loop cards on /printables/)

Claude Code (home lane), worktree `~/mg-esc-band-slim`, branch `claude/esc-band-slim`; contract `docs/handover/contracts/2026-11-15-esc-band-slim.md`, with Jon's 17:03 follow-up (the loop bundle) in the PR body. The first commit carries PRINTABLES-PAGE's close-out: the merge line above, and the contract moved to history.

- **The band** (index.html) now shows three rooms, one per star band, in hub order and with today's markup: Library Jam, The Great Hamster Heist, The Rugby Mud Bath. The other eleven cards are gone, and so is the "New this term" flag with its CSS. The heading, lede, facts and star key are unchanged.
  - Above 768 px the three cards sit in one row, each with its picture beside its text (CSS only). At 1280 px the band is 487 px tall; it was 1520 px, so it is now 32%. Phones stack the cards as before.
  - "Printable class packs →" (to /printables/, `data-mfg-item="printables"`) now sits after "Open all fourteen rooms →".
  - The band carries `data-room-count="14"`, and the phone summary reads that, not the number of cards: it still says "14 rooms". The toggle reads "Show rooms" / "Hide rooms".
- **check-escape-rooms.py, front page:** "a card for every live room, in the hub's order" is replaced. The band must now show exactly one card per star band, each live and carrying the right chip, in hub order (a subsequence of the hub's). data-room-count must equal the number of live rooms, and the lede's "Fourteen" and the button's "fourteen" must be that number as a word.
  - Seven plants are caught: a fourth card, two cards in one band, a band missing, cards out of hub order, a wrong data-room-count, and a wrong number word in the lede and in the button.
  - The hub's rules and plants are unchanged.
- **Other checks:** test-escape-credit still passes on the three cards without loosening. No other check asserts a card per room.
- **/printables/:** "Printable games" now has the loop-cards line, two cards and "More decks coming soon.":
  - Six Sevens, Bruv (Free; Tes and play links);
  - the £5 loop-card bundle (Tes link only).
  - Both Tes links returned 200 with their own listing titles.
- todo: PRINTABLES-PAGE is closed to todo-done; ESC-BAND-ROTATION is added (later, research first).
- MERGED 15 Nov, 18:28 UTC, as d5381e8 (#786). Main on the merge commit: check-site 43746949609 success, phone-fit-full 43746949659 success; live checked. end-task removed claude/esc-band-slim. Local check-changed was stopped at 203 of 260 (none failed) on Jon's 18:15 ruling (HOME-LEAN).

Record: agent Claude Code; review cycles 0; amendments 1 (Jon 17:03, the loop bundle card); usage n/a.

## 2026-11-15 (home): PRINTABLES-PAGE (/printables/, the escape-room packs on Tes)

Claude Code (home lane), worktree `~/mg-printables-page`, branch `claude/printables-page`; contract `docs/handover/contracts/2026-11-15-printables-page.md`. The first commit carries MONOTONIC-CLOCK's close-out (merge line above, contract and Amendment 1 to history).

- **The page.** `printables/index.html` shows Jon's approved wording (13:23) word for word. It is styled as `/updates/` is: Outfit, navy and teal, the nav bar with its back link, and the site footer.
  - **Cards, in the contract's order:** Christmas Tree Fiasco, Kiln Disaster, Comic Caper, Library Jam, then the Warm-up bundle.
  - **Each room card:** its chip copied from /escape-rooms/ (data-stars and the sr-only text), three topics from the room page's meta description, the price, "View on Tes →" (new tab, rel="noopener") and "Play it free online".
  - The bundle card has the Warm-up chip (all three rooms are ★) and no topics line.
  - The links carry `data-mfg-section="printables"` and `data-mfg-item`, so they count as section_clicked. No new event.
- **Tes links:** all five returned 200 on 15 Nov, each with its own listing title.
- **Footer.** `('/printables/', 'Printable packs')` was added to `_LINKS`, and `apply-footer.py` changed 152 pages. check-footer passes.
  - At 320, 375 and 390 px the footer is one 40 px row that scrolls inside itself, exactly as on main, and no page scrolls sideways. site-footer.css is not changed.
- **Also changed:**
  - /escape-rooms/ has one line under its first lede.
  - /updates/ has the approved line.
  - `printables/` is in the sitemap.
  - `printables/` is in check-publish-scope's SITE and in check-content-safety's GLOBS. Both add coverage, as for `ugh-stats/`, and neither is an exception.
  - data/games.json is not touched. check-meta needs no record, because no portal card links to the page.
- todo: the PRINTABLES-PAGE row is updated (loop cards still to come), and a new row PRINTABLES-CORE is added.
- MERGED 15 Nov, 16:41 UTC, as a892547 (#784). Main on the merge commit: check-site 43736934812 success, phone-fit-full 43736934783 success. Local check-changed: 260 checks passed. The branch was rebased onto QF-HCF-FIRST (#783) before the push; the only conflict was the /updates/ November list. Leftover worktree ~/mg-monotonic-closeout and branch claude/monotonic-clock-closeout (1435f511, never pushed) removed by hand on Jon's ruling, after its diff was shown to reverse-apply cleanly on main; end-task removed claude/printables-page.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-15 (home): MONOTONIC-CLOCK (the shared input windows on a clock that never jumps)

Claude Code (home lane), worktree `~/mg-monotonic-clock`, branch `claude/monotonic-clock`; contract `docs/history/contracts/2026-11-15-monotonic-clock.md`. Jon's ruling (15 Nov 11:07): option 1 of todo row ANSWER-LOCK-WALL-CLOCK, now closed in `docs/history/todo-done.md`.

- **Changed:** answer-lock.js `now()`, keypad.js's ghost-click window and scroll.js's touch cancel read `performance.now()`, with `Date` only where `performance.now` is missing. Each window's two sides read the same clock. The window lengths and MaffsLock's API are unchanged. No game file changed, and none of the timestamp uses named in the contract changed.
- **Starting values:** keypad's `lastUp` and scroll's `touched` start at `-Infinity`, not 0. `performance.now()` counts from page load, so a 0 would have ignored a box's click in the page's first 600 ms. check-keypad plants the 0 and catches it.
- **Tests:** `test-answer-lock.py` "clock-step" steps `Date.now()` 10 s back, then 10 s forward, inside the fresh window. Its plant "the wall clock" fails it twice. `check-keypad.py` "Clock" does the same to the 600 ms window, at 100 ms and 700 ms, and with no step. It has two plants: both readings back on `Date.now()`, and `lastUp` starting at 0. Both are caught.
- **Load:** `test-answer-lock.py --no-plants`, six at a time for 20 rounds (120 runs), with six wall-clock steps of about -2.9 s during the rounds: 0 failed. Before this change, 18 of 120 failed.
- **The four Date.now() stubs were left as they are:** sequence-solver (the game's hidden timer; its sweep sets `NO_LOCK_FRESH_INIT`), trig-identity-duel (the game's time line; it waits FRESH_MS first), unit-converter (it already skews `performance.now()` with `Date.now()`) and test-top-scores (stored dates). Each still passes.
- MERGED 15 Nov as d59aeca (#781), after #780 (8e8f3d6) made check-ugh-stats round halves up. The first Gate on #781 failed only on "Ugh, stats pages", which main failed too from the bot's data commit 54e4a99 (Jon: wait for #780, do not change the check). Branch then brought up to date with main (278e168), and the Gate went green. Main on the merge commit: check-site 43722528620 success, phone-fit-full 43722528614 success. Contract moved to `docs/history/contracts/` by the close-out.

Record: agent Claude Code; review cycles 0; amendments 1 (Jon's follow-up: wait for #780); usage n/a.

