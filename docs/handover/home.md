# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-16 (home): HEATWAVE-PACK (The Heatwave Mutiny print pack, DRAFT; a sixth patrol variant)

Claude Code (home lane), worktree `~/mg-heatwave-pack`, branch `claude/heatwave-pack`; contract `docs/handover/contracts/2026-11-16-heatwave-pack.md` (the reissue; the first HEATWAVE-PACK stopped on 5 patrol variants). The first commit carries PE-SHED-FINAL's close-out (#803, 6e1f4e0; its entry below).

- **Patrol variant:** the reissue's first STOP IF was met too: no sixth patrol-lcm-timer variant passes keep()'s spread at minsep 14 (check() holds answers to 101-192; 112-126-140-154 are 14 apart; the widest gap left is 12). Jon chose in session (16 Nov) to append laps 4, 8, 21 (LCM 168, common wrong answer 33) in an append-only second pass at minsep 12. The five existing variants are unchanged; variants.json and room.js gain that one variant only. check-escape-rooms: heatwave-mutiny VALID 270 of 360, variant 0 VALID. /updates/ line added (the Hamster Heist precedent of the same day).
- **Pack:** `rooms/heatwave-mutiny/config.json` (6 sets, seed 1, DRAFT, certificate "Cold air, already paid for", no answer_units, no readout_voice: the hook is the narrator's) and the eleven WebPs (hw-01-rota ... hw-11-disruptor-dial). Label boxes measured by pixel as in #801 (grown blank rectangle, 26 px inside; the sticky note's blank is its own yellow). Print-only words on all six clues; fan and jacket print no words (the plug's label is 109 x 81 px; the jacket has no blank surface).
- **Generator (general, other packs byte-identical):** split_clue() accepts a clue with no `<b>` part when the image gives both "printed" and "caption" (the clock and sticky note have none); lock_words takes a "label" for the answer box (the keypad's "four digits" breaks Amendment 4 on paper; the slider's label printed "... set off min").
- **lockcheck.py:** LCM by counting up in the longest lap, with the prime-factor lines; cube by face, edge counted up, edge cubed; inequality by trying every dial setting, the one prime, the band's largest. All 22 library variants agree.
- **Checks:** see the PR. Other packs compared with ~/pe-tools/dump.py before (origin/main) and after: 28 files identical once date fields and worktree paths are normalised.
- MERGED: pending.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-16 (home): PE-SHED-FINAL (P.E. Store Rebellion pack approved; readout_voice; teacher page's variant 0)

Claude Code (home lane), worktree `~/mg-pe-shed-final`, branch `claude/pe-shed-final`; contract `docs/handover/contracts/2026-11-16-pe-shed-final.md`. The first commit carries PE-SHED-PACK's close-out (#801, 6f9498b; its entry below).

- **Generator:** `build_pack.py` takes an optional `"readout_voice"` in a room's config: one line, printed in italics as the first line of "Read this at the start", above the hook. readout_voice() (called from load_config()) refuses an empty value, a non-string, a `{{token}}` and an HTML tag, and holds it to the caption sentence rules, figure binding (bound()) and the fixed-penalty rule. Without the key, readouts() prints exactly as before. Documented in the module docstring and the README.
- **Room:** pe-shed-rebellion's config has Jon's readout_voice text, as given (apostrophes as `&rsquo;`, as the room writes them), and `"wording_approved": {"by": "Jon", "date": "2026-11-16"}`. teacher.html's clueMap and notes now quote variant 0 as it is: 27π limit, 9 m reach, 27π over 81π, 84.823... over 254.469... (27π = 84.8230..., 81π = 254.4690...). Nothing in the repo generates those lines (only test-pack-generator.py reads clueMap, for Hamster Heist).
- **Todo:** PE-SHED-PACK-APPROVE closed to todo-done; new row PACK-READOUT-VOICE (the other eight rooms' read-outs, any fix needs Jon's go-ahead, as those packs are on Tes).
- **Checks:** see the PR. Other packs compared with ~/pe-tools/dump.py before (origin/main) and after.
- MERGED 16 Nov as 6e1f4e0 (#803) via merge-pr.py on its second call (the first was refused: no Gate check yet). The second's last line was "main 6e1f4e0: NO RUN FOUND", exit 1: it looked before main's push runs registered; the merge itself succeeded. Main on the merge commit: check-site 43961875130 FAILURE (the Shape Shifter verifier's rotation "moving on" check only, a flake in scripts/verify-shape-shifter.py fixed by SHAPE-SHIFTER-FLAKE; nothing #803 touched), phone-fit-full 43961875121 success (both push runs). Jon ruled "merge at 37 pages" in session (recorded on the PR). Contract moved to `docs/history/contracts/`.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-16 (home): PE-SHED-PACK (The P.E. Store Rebellion print pack, DRAFT; variant 0 fixed)

Claude Code (home lane), worktree `~/mg-pe-shed-pack`, branch `claude/pe-shed-pack`; contract `docs/handover/contracts/2026-11-16-pe-shed-pack.md`. The first commit carries FOOTER-PHONE-FOUR's close-out (#797, cdc38aec; its entry below). #800 had merged (5a82f369) before this branched.

- **Pack:** `rooms/pe-shed-rebellion/config.json` (6 sets, seed 1, DRAFT, certificate "Cross-country cancelled", no `answer_units`: every answer is whole degrees, psi or a dial number) and its eleven WebPs (pe-01-logbook ... pe-11-locker-dial, 1254 px, 44-247 KB). Label boxes measured by pixel: the largest rectangle of near-white (grey 225+) grown from a seed in each blank surface, then 26 px (2%) inside it on every side. The calendar's box sits below the drawn ring. Print-only words on the log, clipboard and laminated card (the clue sentence runs through their bold parts). Bibs and coat have no blank surface: no words printed.
- **lockcheck.py:** sector area (every arc tried against A x r² = 360K; the decimal-circle wrong answer with pi bracketed by Machin), Boyle (every gauge setting tried against P x V2 = P1 x V1; wrong answer P1 x V2 / V1), nth term (step from the first two entries, third checked on the line, rule at day dT; wrong answer c3 + (c2 - c1)). All 27 library variants agree.
- **Variant 0:** sprinkler variant 0 is 9 m / 27π (was 12 m / 48π), same answer 120 and miss 40; check-escape-rooms reports it VALID (273 of 720 draws). Row 47 closed to todo-done.
- **Build:** 36 pages, 6 sets, every check passed first time; no shared-generator change was needed. Other packs: built before and after with a harness that keeps every `build_html()` document and the PDF: HTML and build logs byte-identical, final targets identical, PDFs identical once the two date fields are removed. Roll for Initiative does not build on this machine either way (locks pages 972 > 953 px); its HTML and log are identical. test-pack-generator.py: 67/67, 21 plants caught, 8 controls pass.
- MERGED 16 Nov as 6f9498b (#801) via merge-pr.py, last line "main 6f9498b run 43942870305: GREEN", exit 0. Main on the merge commit: check-site 43942870305 success, phone-fit-full 43942870330 success (both push runs). Contract moved to .

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-16 (home): FOOTER-PHONE-FOUR (four footer links on phones)

Codex (home lane), worktree `~/mg-footer-phone-four`, branch `codex/footer-phone-four`; contract `docs/handover/contracts/2026-11-16-footer-phone-four.md`. First commit 78e43086 closed UNLIST-GRAPH-SKETCHER (#791, 7be6482; check-site 43762342514 and phone-fit-full 43762342465 green; three follow-ups).

- Shared footer: six wide-only links and their preceding separators gain `sf-wide` in CANONICAL; `apply-footer.py` wrote 152 pages. One media query hides them below 810px. In local Chromium with the real fonts, the ten-link row is 784px plus 24px padding and first fits at 808px; 810px is the rounded breakpoint. The four phone links are About, Contact, Privacy and Feedback on the existing 40px bar.
- The browser assertion in `measure-phone-fit.py` passed on the homepage, prime-or-composite and the fractions parent guide at 320, 375, 390, 810 and 1280px. Both plants failed it: missing classes on a homepage copy and the media query removed from a stylesheet copy. `check-footer.py` passed all 152 pages; a diff check found only footer classes in those pages and the dated /updates/ line. `measure-phone-fit.py --selftest`, `check-context-size.py` and `git diff --check` passed; `ci-groups.py --worst-case` said no gate file changed. Next: PR Gate, merge and main-run report.
- Backlog housekeeping: #794, #793, #795 and #796 rows closed or updated as the contract names. The B4 Angle Ace ledger row was not in item 7 and stays for a later contract; its text is stale on main.

- MERGED 16 Nov as cdc38aec (#797), carried by PE-SHED-PACK's first commit. Main on the merge commit: check-site 43927268181 success, phone-fit-full 43927268127 success (both push runs). Contract moved to `docs/history/contracts/`.

Record: agent Codex; wall pending; review cycles 0; amendments 0; usage n/a.

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
- MERGED as 7be6482 (#791); check-site 43762342514 and phone-fit-full 43762342465 green. Three follow-ups above were included.

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

