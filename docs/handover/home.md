# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-18 (home): DASHBOARD-FIXES (every Dashboard chart names its series from its header row; SR-33; two close-outs)

Claude Code (home lane), worktree `~/mg-dashboard-fixes`, branch `claude/dashboard-fixes`; contract `docs/handover/contracts/2026-11-18-dashboard-fixes.md`. Tier Medium. The first commit carries two close-outs:
- **#827 DASHBOARD-GLANCE:** recorded in its entry below; contract moved.
- **#828 DD-LINEUP-ORDER (cloud's task; recorded here because the cloud lane owns `docs/handover/cloud.md`):** MERGED 18 Nov as 5a56852 (#828), merge-pr.py last line "main 5a56852 run 44376293965: GREEN". Main on the merge commit: check-site 44376293965 success, phone-fit-full 44376293770 success, pages build 44376293960 success (confirmed from the API). Contract moved to `docs/history/contracts/2026-11-18-dd-lineup-order.md`. Cloud's own DD-LINEUP-ORDER entry still ends "Next: PR, Gate and phone-fit-full, merge"; its next first commit can mark it merged.
- **Charts (`docs/apps-script-endpoint.js`, SCRIPT_VERSION 2026-11-18-b):** one helper, `dashChart(dash, spec)`, builds all four Dashboard charts (Top Games, Accuracy, the level pie, Daily Activity) and always calls `setNumHeaders(1)`, the pattern of `docs/apps-script-ga4-summary.js`'s chart loop; `newChart(` appears once. Each range still starts at its header row. Look unchanged: in the stubs every chart's type, ranges, position and options match main's call for call; only setNumHeaders(1) is added (it was missing on three).
- **Percent cells: PARKED (STOP IF), cause not shown.** Ruled out, in a traced run of the stubs (every write and format recorded per cell): each of the two cells is written once per run, as a number (a count; cellValue passes numbers through), and no setNumberFormat touches it; no cell is written twice; no string such as "12%" is written. The only mechanism that fits: a number format left over from an earlier build that `dash.clear()` (:883) did not remove. The pre-#827 layout's Top Games "Completion %" (formatPercentColumn, column D, first data row) sits exactly on A's "Different games played" cell whatever the data, because both layouts start at the same row; C2's cell depends on the day's data. But Google documents Sheet.clear() as "Clears the sheet of content and formatting information", so this is unproven, and no guessed fix ships. The test function `checkPercentCells` is in the PR body: it logs the two cells' formats and whether a scratch sheet keeps "0%" through clear(). Pointer row DASHBOARD-PERCENT-CELLS in `docs/todo.md` (todo.md is 28 bytes under its 150 KiB cap).
- **Tests:** `scripts/test-apps-script-report.py` section i: all four charts are built, each with setNumHeaders(1); newChart( appears once. New plant: the pie built without setNumHeaders(1), caught. The curveType plant now targets the spec. 21 plants caught.
- **Canon:** SR-33 (foundational skills are priority-audience work, Jon 18 Nov 2026) after SR-32; §0.2 point 2 names it. `docs/apps-script-redeploy.md` step 12: 2026-11-18-b. No /updates/ line (internal).
- **Jon's steps after merge (never Deploy):** 1. paste `docs/apps-script-endpoint.js` into Code.gs, keeping your REPORT_EMAIL line; 2. Save; 3. run `testDashboard`. Then the percent check in the PR body, once.
- MERGED: pending.

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

## 2026-11-17 (home): FINAL-PADLOCK-FAIR (fair final padlocks, the optional final padlock, versioned PDF names; all ten packs rebuilt)

Claude Code (home lane, cloud session), branch `claude/inspiring-einstein-jylil1`; contract `docs/handover/contracts/2026-11-17-final-padlock-fair.md` with Amendment 1 (the final padlock optional for the teacher) and Amendment 2 (Jon: page 1's cap 150 to 180). The first commit carries HEATWAVE-PACK's close-out (#804, 61b2f9a). MERGE-PR-ROBUST (#806) had merged (3797bf8) before this branched.

- **Rules (final.py, lockcheck.py, build_pack.py; every pack):** friendly() refuses a product above PRODUCT_MAX = 10,000; lockcheck refuses it independently. One difficulty class a pack: with a multiplication, one digit signature and every product in [lo, 3 lo]; in plus-and-minus, the largest term's digits. choose() tries classes in a seeded order, each class's windows smallest first, and raises naming the best class found; each set's target is drawn by the existing seeded choice from its in-class, in-window candidates. lockcheck.pack_problems() re-reads the printed expressions (called from verify_finals, so the build and the self-test check every room).
- **Optional final padlock (Amendment 1):** run sheet step 5's second line, the score sheet's "Finished (final padlock, or Lock 3 if skipped)", the locks page's "The final padlock (if your teacher says so)". The lock number comes from the room's lock count. RUN_IT_WORDS 180 (Amendment 2); page 1 is now 178 words in nine packs, 175 in Kiln: little headroom.
- **Names:** `dist-packs/<slug>-pack-v<N>.pdf`; the PDF title and footer carry the same version (pack_version(), a whole number from 1; the configs keep it as a string). Every room's pack_version up by one (Amendment 1 changed every pack): car-trap 2, christmas-tree-fiasco 3, comic-caper 2, hamster-heist 2, heatwave-mutiny 2, kiln-disaster 3, library-jam 2, pe-shed-rebellion 2, prom-budget 2, roll-for-initiative 2.
- **Heatwave:** `"final_shape": "plus-and-minus"` (with a multiplication the best class reached 3 sets). Found: the generator's shared wording speaks of multiplying (teacher key "two answers whose product is close"; student hint card "Which two of your answers multiply to about that?"), wrong for this shape. Not changed (outside the contract); added to HEATWAVE-PACK-APPROVE.
- **Builds (this machine, all ten, Roll for Initiative included):** nine `--final`, Heatwave DRAFT; every PDF's title, every footer and every name checked with pypdf. Targets in the PR.
- **Tests:** a plant that tested the old factor rule found a ceiling case first; its search now asks for the factor rule. test-pack-generator.py: self-test 67/67; its own 40 plants caught, 17 controls pass (new: 10,001; mixed signatures; ratio over 3; plus-and-minus digits; unversioned name; controls 10,000, two packs as built, the versioned name). check-escape-rooms.py exit 0.
- **Todo:** PACKS-V2-UPLOAD added; HEATWAVE-PACK-APPROVE updated (v2 name, the shape, the wording question).
- MERGED 17 Nov as 65c7ebd (#807). Main on the merge commit: check-site 44044387029 success, phone-fit-full 44044386836 success (both push runs). Contract already in `docs/history/contracts/` (closed out by CANTEEN-PACK's first commit).

Record: agent Claude Code; review cycles 0; amendments 2; usage n/a.

