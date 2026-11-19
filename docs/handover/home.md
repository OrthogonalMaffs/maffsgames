# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-19 (home): NEXT-IN-VIEW (MaffsNext.wrong() brings Next into view on a phone, in every game)

Claude Code (home lane), worktree `~/mg-next-in-view`, branch `claude/next-in-view`; contract `docs/handover/contracts/2026-11-19-next-in-view.md`. Tier Medium. The first commit carries PRINTABLES-CORE's close-out (#830, 006d3d8).

- **`schools/assets/next-control.js`:** wrong() calls `MaffsScroll.reveal(wrap, { keep: opts.keep || wrap })` once its timers are set; new option `keep` (the reason element, or a function returning it). A page without scroll.js gets it once, by a tag whose src is resolved from next-control.js's own (`data-maffs-next="scroll"`); the reveal is skipped if the control was cleared or advanced meanwhile, and for a control inside a position:fixed ancestor (scrolling the page cannot move it). Floor, fallback, advance-once and 44px unchanged; scroll.js unchanged.
- **Tests:** `scripts/test-next-control.py` gains six in-view cases at 320x568 on pages served two levels down (Next brought up with the reason's top on screen; no scroll.js: loaded once, same result; already in view: no scroll; keep holds when both cannot fit; a touchstart stops the pending passes; clear() before scroll.js arrives: no scroll). Two plants caught: the reveal call removed, scroll.js not loaded. 23 checks pass. check-scroll-reveal.py unchanged, passes.
- **Re-measure (81 MaffsNext games, 320x568, 375x667, 390x844, main 150bd66 against this branch):** measure-phone-fit.py measures Next from the top of the page after `scrollTo(0, 0)`, so a scroll cannot change it: 0 of 243 rows changed in either mode, known-failures 21 games (normal) and 26 (Aa) before and after, Next below the fold by that measure 55 and 83 rows before and after. **phone-fit-state.json: nothing to take off, nothing added.** The same runs, read in the window after the page settles: Next in view on 95 of 150 wrong screens before, 148 after (normal); 68 before, 147 after (Aa); no screen moved twice or reversed.
- **Decided for you:** screening-room (2 normal rows, 3 Aa) is unchanged: its own `MaffsScroll.reveal(result, { up: true })` right after wrong() holds its explanation's top, which is taller than the screen, so Next stays below (844 / 528 at 320x568, as before). Same task, so no visible jump. Not changed (game files out of scope); a per-game `keep:` or a shorter result is its fix.
- **todo:** NNL-PHONE-NEXT and DD-LINEUP-FEEDBACK closed with figures in `docs/history/todo-done.md` (NNL Order Them 630 to 518, Calculate 585 to 518, DD Line-Up 799 to 518, Round Up 548 to 517, at 320x568, fold 528; Aa too). SIX-PS-SHORT-WRONG: all 14 unchanged (the 6 P's own reveal decides); 5 more found unlisted, on main too (row updated). todo.md 150456 to 149425 bytes.
- **Canon 7.6** sentence under the MaffsNext usage; one /updates/ line.
- MERGED: pending. The next home contract's first commit records the merge and moves this contract to history.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-19 (home): PRINTABLES-CORE (the seven Core rooms and three Core bundles on /printables/)

Claude Code (home lane), worktree `~/mg-printables-core`, branch `claude/printables-core`; contract `docs/handover/contracts/2026-11-19-printables-core.md`. Tier Medium. The first commit carries DASHBOARD-FIXES' close-out (#829, e4ac609).

- **/printables/ (`printables/index.html`):** ten `<article class="pack">` cards after the Warm-up bundle, inside the escape-room packs' div, built as the page's other cards with the ★★ Core chip copied from The Christmas Tree Fiasco's. Seven rooms in /escape-rooms/'s order (Hamster Heist, P.E. Store, Heatwave, Prom Budget, Canteen, Car Trap, Roll for Initiative), each £3 with topics, a Tes link (`tes-<slug>`) and a play link (`play-<slug>`); then Core bundle (£5), Core bundle 2 (£6.50) and the complete Core collection (£10), Tes link only. Every h3 matches the hub's card and every topics line matches the room's meta description word for word; each /escape-rooms/<slug>/ exists. Existing cards unchanged.
- **/updates/:** one 19 Nov 2026 line.
- **todo:** PRINTABLES-CORE and CORE-BUNDLES-2 moved word for word to `docs/history/todo-done.md` with a done note; todo.md 153572 to 152846 bytes.
- MERGED 19 Nov as 006d3d8 (#830) via merge-pr.py, exit 0, last line "main 006d3d8 run 44477099151: GREEN". Main on the merge commit: check-site 44477099151 success, phone-fit-full 44477099247 success (both push runs), pages build 44477099011 success (all confirmed from the API). Contract already in `docs/history/contracts/2026-11-19-printables-core.md` (moved by #831); closed out by NEXT-IN-VIEW's first commit.

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-18 (home): DASHBOARD-FIXES (every Dashboard chart names its series from its header row; SR-33; two close-outs)

Claude Code (home lane), worktree `~/mg-dashboard-fixes`, branch `claude/dashboard-fixes`; contract `docs/handover/contracts/2026-11-18-dashboard-fixes.md`. Tier Medium. The first commit carries two close-outs:
- **#827 DASHBOARD-GLANCE:** recorded in its entry below; contract moved.
- **#828 DD-LINEUP-ORDER (cloud's task; recorded here because the cloud lane owns `docs/handover/cloud.md`):** MERGED 18 Nov as 5a56852 (#828), merge-pr.py last line "main 5a56852 run 44376293965: GREEN". Main on the merge commit: check-site 44376293965 success, phone-fit-full 44376293770 success, pages build 44376293960 success (confirmed from the API). Contract moved to `docs/history/contracts/2026-11-18-dd-lineup-order.md`. Cloud's own DD-LINEUP-ORDER entry still ends "Next: PR, Gate and phone-fit-full, merge"; its next first commit can mark it merged.
- **Charts (`docs/apps-script-endpoint.js`, SCRIPT_VERSION 2026-11-18-b):** one helper, `dashChart(dash, spec)`, builds all four Dashboard charts (Top Games, Accuracy, the level pie, Daily Activity) and always calls `setNumHeaders(1)`, the pattern of `docs/apps-script-ga4-summary.js`'s chart loop; `newChart(` appears once. Each range still starts at its header row. Look unchanged: in the stubs every chart's type, ranges, position and options match main's call for call; only setNumHeaders(1) is added (it was missing on three).
- **Percent cells: PARKED (STOP IF), cause not shown.** Ruled out, in a traced run of the stubs (every write and format recorded per cell): each of the two cells is written once per run, as a number (a count; cellValue passes numbers through), and no setNumberFormat touches it; no cell is written twice; no string such as "12%" is written. The only mechanism that fits: a number format left over from an earlier build that `dash.clear()` (:883) did not remove. The pre-#827 layout's Top Games "Completion %" (formatPercentColumn, column D, first data row) sits exactly on A's "Different games played" cell whatever the data, because both layouts start at the same row; C2's cell depends on the day's data. But Google documents Sheet.clear() as "Clears the sheet of content and formatting information", so this is unproven, and no guessed fix ships. The test function `checkPercentCells` is in the PR body: it logs the two cells' formats and whether a scratch sheet keeps "0%" through clear(). Pointer row DASHBOARD-PERCENT-CELLS in `docs/todo.md` (todo.md is 28 bytes under its 150 KiB cap).
- **Tests:** `scripts/test-apps-script-report.py` section i: all four charts are built, each with setNumHeaders(1); newChart( appears once. New plant: the pie built without setNumHeaders(1), caught. The curveType plant now targets the spec. 21 plants caught.
- **Canon:** SR-33 (foundational skills are priority-audience work, Jon 18 Nov 2026) after SR-32; §0.2 point 2 names it. `docs/apps-script-redeploy.md` step 12: 2026-11-18-b. No /updates/ line (internal).
- **Jon's steps after merge (never Deploy):** 1. paste `docs/apps-script-endpoint.js` into Code.gs, keeping your REPORT_EMAIL line; 2. Save; 3. run `testDashboard`. Then the percent check in the PR body, once.
- MERGED 18 Nov as e4ac609 (#829) via merge-pr.py, exit 0, last line "main e4ac609 run 44397107631: GREEN". Main on the merge commit: check-site 44397107631 success, phone-fit-full 44397107629 success (both push runs), pages build 44397106626 success (all confirmed from the API). Contract moved to `docs/history/contracts/2026-11-18-dashboard-fixes.md` (closed out by PRINTABLES-CORE's first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-18 (home): DASHBOARD-GLANCE (the Dashboard answers Jon's weekly questions; GA4 sources tab; Daily Activity chart fixed)

Claude Code (home lane), worktree `~/mg-dashboard-glance`, branch `claude/dashboard-glance`; contract `docs/handover/contracts/2026-11-18-dashboard-glance.md`. The first commit carries DAILY-ANSWERS' close-out (#825, aba826a). Tier Shared: holds at a green Gate for Project Claude's review and Jon's "merge".

- **Dashboard (`docs/apps-script-endpoint.js`, SCRIPT_VERSION 2026-11-18-a):** sections A (growing: 7 days against the previous 7; % correct in points, always grey), B (check-these questions under 10% right on 10+ marked, on red; where students quit), C (probable classes; when it is used; portal filters), D (GA4 channels and landing pages), E (UK share, top 5 countries, devices), F (games launched in the last 14 days, launch-dates.json read from GitHub), G (Table 4b, hints by lock, time per lock), H (Misunderstood Maths), I (the four older tables, content unchanged, moved), J (Daily Activity last: series named by `setNumHeaders(1)`, curveType removed). sendDailyReport and testDashboard pass prevWeekRows (the 7 days before weekAgo); the existing filters are unchanged. A missing or empty GA4 tab gives "GA4 figures not available yet." in A, D and E. The email's text is unchanged.
- **Time per lock:** included. engine.js `st.openAt[l.id] = st.played` (the room's clock seconds when a lock opened), written by finish() in room.js lock order, "-" if never opened; opened locks sorted by time give the seconds since the previous one opened.
- **GA4 (`docs/apps-script-ga4-country.js`):** a third GA4C_TABLES entry, 'GA4 sources daily' (date, sessionSource, sessionMedium, deviceCategory, landingPage; sessions, engagedSessions, activeUsers; newest date, then most sessions, then the dimensions). The four dimension names are in Google's Data API schema (landingPage is the path, no query string). No city or region.
- **Tests:** test-apps-script-report.py section j (A to H on hand-written rows and GA4 tab rows, through sendDailyReport) plus a chart check; 20 plants caught, 7 of them new. Stubs gained only what the sections call: load() takes GA4 tabs and launch dates, setBackground/setFontColor record their colour, and formatDate honours its zone (it ignored it, so a midnight in BST became the day before) and gains 'HH:mm' and 'u'. Section i's curveType clause removed (contract J). test-ga4-country.py: the mock serves the sources table, a check that it asks for exactly the approved dimensions and nothing finer than country, plant 'city' caught. test-ga4-summary.py unchanged and passes.
- **Docs:** canon §1.2.1 (third tab) and §1.4 (an at-a-glance paragraph); docs/ga4-country-setup.md (the sources tab, re-run ga4CountryBackfill once); docs/apps-script-redeploy.md (no deployment for a Dashboard-only change; step 12's version 2026-11-18-a).
- **Jon's steps after merge (never Deploy):** 1. paste `docs/apps-script-endpoint.js` into Code.gs, keeping your REPORT_EMAIL line; 2. paste `docs/apps-script-ga4-country.js` into ga4-country.gs; 3. Save; 4. run `ga4CountryBackfill` once (fills GA4 sources daily from 1 Sep 2026); 5. run `testDashboard`.
- MERGED 18 Nov as bc3d192 (#827) via merge-pr.py, exit 0, last line "main bc3d192 run 44370288253: GREEN". Main on the merge commit: check-site 44370288253 success, phone-fit-full 44370288214 success (both push runs, confirmed from the API). Contract moved to `docs/history/contracts/2026-11-18-dashboard-glance.md` (closed out by DASHBOARD-FIXES' first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-18 (home): DAILY-ANSWERS (the Dashboard's Daily Activity shows games started and questions answered)

Claude Code (home lane), worktree `~/mg-daily-answers`, branch `claude/daily-answers`; contract `docs/handover/contracts/2026-11-18-daily-answers.md`. The first commit carries CANTEEN-APPROVE's close-out (#819, 6f2d29c). Tier Shared: holds at a green Gate for Project Claude's review and Jon's "merge".

- **Table 5 (`docs/apps-script-endpoint.js`, rebuildDashboard):** one pass over monthRows tallies, by day (`Utilities.formatDate(..., TIMEZONE, 'yyyy-MM-dd')` as before), game_started rows and question_answered rows whose `rptKind(String(slug), kinds)` is 'question' (marked or not; rooms and shot games left out). Both are rptMap tallies. Days are the sorted union of both; a missing count is 0. Header `Date | Games Started | Questions Answered` (bold, #f0f0f0, 3 columns); every row through cellValue. Section title unchanged.
- **Chart 5:** LINE over 3 columns, same position and 500 × 280, curveType kept; colours #0ea5e9 (starts) and #0d9488 (answers); series 0 on axis 0, series 1 on axis 1; vAxes 'Games started' / 'Questions answered'; legend bottom; title 'Daily Games Started and Questions Answered — Last 30 Days'. Column 3 width stays 80 (its header overflows into the empty column 4 cell).
- **rptKind vs rptBuild:** the same call on the same String(game_slug), so no slug is classed differently. rptBuild drops unmarked rows for accuracy; this count keeps them, by Jon's decision.
- **Test (`scripts/test-apps-script-report.py`, section i):** five days of hand-written rows (a day with answers and no starts, a day of room answers only that must have no row, room and shot answers, one row with correct null); expected table and chart options written by hand. The chart stub now records its calls per newChart and a range keeps its size, so the chart can be read; nothing else in the stubs changed. Three new plants caught: room answers counted, shot answers counted, a day with no starts dropped. Every earlier check passes unchanged; test-apps-script-counts.py PASS (38).
- **Gate flake (for the cloud lane):** the first Gate, check-site 44342334459 on 4e3413d1, went red only because "PR budget (measured times)" was cancelled at its 5-minute timeout: its timing-files step took 3 minutes while GitHub returned 502s (that job usually takes about 2 minutes); the other 89 jobs passed. The token cannot rerun jobs (403), so an empty commit started a fresh run. Project Claude approved the diff, 18 Nov.
- **For Jon, before the Dashboard changes:** paste the updated `docs/apps-script-endpoint.js` into Apps Script per `docs/apps-script-redeploy.md`, with your own address in REPORT_EMAIL (the repo keeps the placeholder), as a new version of the existing deployment. Done: Jon pasted the file into Code.gs and ran testDashboard, 18 Nov 2026, 17:35; the table showed three columns; no redeploy was needed.
- MERGED 18 Nov as aba826a (#825) via merge-pr.py, exit 0, last line "main aba826a run 44351676786: GREEN". Main on the merge commit: check-site 44351676786 success, phone-fit-full 44351676633 success (both push runs, confirmed from the API). Contract moved to `docs/history/contracts/2026-11-18-daily-answers.md` (closed out by DASHBOARD-GLANCE's first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-18 (home): CANTEEN-APPROVE (The Canteen Hack's opening names the Healthy Week price; pack approved, v2)

Claude Code (home lane), worktree `~/mg-canteen-approve`, branch `claude/canteen-approve`; contract `docs/handover/contracts/2026-11-18-canteen-approve.md`. The first commit carries CANTEEN-PACK's close-out (#817, 236e9ae).

- **Room:** `escape-rooms/canteen-hack/room.js` hook gains Jon's sentence "Last term it cost a fraction of that." straight after the £8.40 one (Jon 18 Nov 03:43). Nothing else in the room changed. The pack reads the hook, so its start read-out has it too.
- **Pack:** config `"wording_approved": {"by": "Jon", "date": "2026-11-18"}`, `"pack_version": "2"` (a string, as every other pack's). `build_pack.py canteen-hack --final` exit 0: `dist-packs/canteen-hack-pack-v2.pdf`, 36 pages, no DRAFT on any page, the sentence on page 2 (the start read-out), which still fits. Finals unchanged: A 1928, B 2340, C 2960, D 2000, E 1510, F 3508.
- **Checks:** check-escape-rooms exit 0; test-pack-generator exit 0 (self-test 67/67 on 11 rooms; 56 plants caught, 23 controls pass). No generator or other config changed, so the other ten packs are unchanged.
- **Docs:** /updates/ line (18 Nov); CANTEEN-PACK-APPROVE closed to todo-done; CORE-BUNDLES-2 stays open.
- MERGED 18 Nov as 6f2d29c (#819) via merge-pr.py, exit 0, last line "main 6f2d29c run 44235030804: GREEN". Main on the merge commit: check-site 44235030804 success, phone-fit-full 44235030742 success (both push runs, confirmed from the API). Contract moved to `docs/history/contracts/2026-11-18-canteen-approve.md` (closed out by DAILY-ANSWERS' first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-17 (home): CANTEEN-PACK (The Canteen Hack print pack, DRAFT; the generator prints a "pair" lock)

Claude Code (home lane), worktree `~/mg-canteen-pack`, branch `claude/canteen-pack`; contract `docs/handover/contracts/2026-11-17-canteen-pack.md`. The first commit carries FINAL-PADLOCK-FAIR's close-out (#807, 65c7ebd).

- **Pair locks (build_pack.py, general; Jon 17 Nov 19:25, "I agree that you add the 2 numbers for cookie."):** an instrument of kind "pair" is an ORDERED pair: answer_atoms() (distinctness), miss_is_answer() and lockcheck compare (a, b); answers_of() gives a + b; two labelled boxes on the cover (`label_boxes` + `part_label_boxes`; labels from lock_words "parts"); key and solutions give both labels; the locks page and key say a + b. New checks pair_final_problems() and pair_key_problems(). Single-value and multi-accepted locks untouched.
- **Clipped cards (general):** AUDIT_JS stops a build when an evidence card's words run past its foot (the card hid it; the page did not overflow). Found on Canteen's kale (32 px); no other pack had one. The kale picture is cropped 100 px top and bottom.
- **Pack:** 6 sets, seed 1, DRAFT, 36 pages, class 2-digit x 3-digit (default shape; easier classes reach 5), certificate "Nothing left to sign off", no readout_voice (the hook is the narrator's), herrings print no words; all six clues have printed/caption overrides. lockcheck: 3 recomputes, all 30 variants agree.
- **Checks:** the other ten packs byte-identical (31 files: HTML, logs, PDFs less dates; Roll for Initiative fails locally before and after). check-escape-rooms exit 0 (600 of 1000 VALID). test-pack-generator exit 0: self-test 67/67 on 11 rooms (its wrong-answer plant now bumps a pair's first value, Canteen sorting first), 56 plants caught, 23 controls pass.
- **Todo:** CANTEEN-PACK-APPROVE, CORE-BUNDLES-2; COMIC-CAPER-REUPLOAD and CHRISTMAS-LIBRARY-KILN-REUPLOAD closed as superseded by PACKS-V2-UPLOAD (todo-done).
- MERGED 17 Nov as 236e9ae (#817) via merge-pr.py, exit 0, last line "main 236e9ae run 44165899116: GREEN". Main on the merge commit: check-site 44165899116 success, phone-fit-full 44165898866 success (both push runs). Contract moved to  (closed out by CANTEEN-APPROVE's first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

