# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

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

