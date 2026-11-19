# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-19 (home): WRONG-PAUSE-NEXT (four games pause on Next after a wrong answer; check-answer-lock fails a game that stops pausing)

Claude Code (home lane), worktree `~/mg-wrong-pause-next`, branch `claude/wrong-pause-next`; contract `docs/handover/contracts/2026-11-19-wrong-pause-next.md`. Tier Medium. The first commit carries the close-outs of #837 NEXT-IN-VIEW and #839 DD-VERIFIER-SHARD (their entries below; both contracts moved to `docs/history/contracts/`).

- In progress: the four games and the check are written; next, the full in-play run, phone-fit, PR.

## 2026-11-19 (home): DD-VERIFIER-SHARD (Decimal Detective's verifier on ci-shards, so #837 fits the per-line limit)

Claude Code (home lane), worktree `~/mg-dd-verifier-shard`, branch `claude/dd-verifier-shard`; contract `docs/handover/contracts/2026-11-19-dd-verifier-shard.md`. Tier Small. Route 1 for #837 NEXT-IN-VIEW, whose Gate (check-site 44573475355) stopped on this verifier: 177s median + 15s setup = 192s, 71% of 270s against the 70% (189s) line limit, selected because next-control.js selects 136 verifiers.

- **`scripts/verify-decimal-detective.py`:** `# ci-shards: <same label> | | 2`; 14 units: desktop, phone 320x568, phone 375x667, phone 390x844, bank (keys plus the four bank plants), and one per page plant (9). Each check and plant runs in exactly one unit; a slice without the desktop pass reads the bank from the page first. `--list-units` works.
- **Checked locally:** full run PASS, identical to main's (45 items, 1307 answers, the same 13 self-test lines caught), 198s against 199s; --shard 1/2 PASS (7 units, 111s), 2/2 PASS (7 units, 84s), together all 14, none twice. ci-groups --selftest and --check PASS (each part 120s default, 50%, until main times its units); ci-deps --selftest PASS.
- **Report only (ci-lines over 60% of their line budget, ci-timings.json from main run 44566476211, setup 15s):** check-answer-lock.py "Answer lock, static rules and self-test" 268s + 15s of 450s (63%); verify-screening-room.py 150s + 15s of 270s (61%).
- MERGED 19 Nov as f2e6d2a (#839) via merge-pr.py, exit 0, last line "main f2e6d2a run 44580613966: GREEN". Main on the merge commit: check-site 44580613966 success, phone-fit-full 44580613885 success (both push runs), pages build 44580613026 success (all confirmed from the API). Cleaned up by end-task. Main then merged into #837 (its entry below). Contract moved to `docs/history/contracts/2026-11-19-dd-verifier-shard.md` (closed out by WRONG-PAUSE-NEXT's first commit).

## 2026-11-19 (home): NEXT-IN-VIEW (MaffsNext.wrong() brings Next into view on a phone, in every game)

Claude Code (home lane), worktree `~/mg-next-in-view`, branch `claude/next-in-view`; contract `docs/handover/contracts/2026-11-19-next-in-view.md`. Tier Medium. The first commit carries PRINTABLES-CORE's close-out (#830, 006d3d8).

- **`schools/assets/next-control.js`:** wrong() calls `MaffsScroll.reveal(wrap, { keep: opts.keep || wrap })` once its timers are set; new option `keep` (the reason element, or a function returning it). A page without scroll.js gets it once, by a tag whose src is resolved from next-control.js's own (`data-maffs-next="scroll"`); the reveal is skipped if the control was cleared or advanced meanwhile, and for a control inside a position:fixed ancestor (scrolling the page cannot move it). Floor, fallback, advance-once and 44px unchanged; scroll.js unchanged.
- **Tests:** `scripts/test-next-control.py` gains six in-view cases at 320x568 on pages served two levels down (Next brought up with the reason's top on screen; no scroll.js: loaded once, same result; already in view: no scroll; keep holds when both cannot fit; a touchstart stops the pending passes; clear() before scroll.js arrives: no scroll). Two plants caught: the reveal call removed, scroll.js not loaded. 23 checks pass. check-scroll-reveal.py unchanged, passes.
- **Re-measure (81 MaffsNext games, 320x568, 375x667, 390x844, main 150bd66 against this branch):** measure-phone-fit.py measures Next from the top of the page after `scrollTo(0, 0)`, so a scroll cannot change it: 0 of 243 rows changed in either mode, known-failures 21 games (normal) and 26 (Aa) before and after, Next below the fold by that measure 55 and 83 rows before and after. **phone-fit-state.json: nothing to take off, nothing added.** The same runs, read in the window after the page settles: Next in view on 95 of 150 wrong screens before, 148 after (normal); 68 before, 147 after (Aa); no screen moved twice or reversed.
- **Decided for you:** screening-room (2 normal rows, 3 Aa) is unchanged: its own `MaffsScroll.reveal(result, { up: true })` right after wrong() holds its explanation's top, which is taller than the screen, so Next stays below (844 / 528 at 320x568, as before). Same task, so no visible jump. Not changed (game files out of scope); a per-game `keep:` or a shorter result is its fix.
- **todo (after Jon's ruling, below):** NNL-PHONE-NEXT, DD-LINEUP-FEEDBACK part 2 and SIX-PS-SHORT-WRONG stay open, each noted that the reveal makes Next reachable but the layout still does not fit (in the window after the reveal, 320x568: NNL Order Them 630 to 518, Calculate 585 to 518, DD Line-Up 799 to 518, Round Up 548 to 517, fold 528). SIX-PS-SHORT-WRONG also lists 5 unlisted sweep failures, on main too. New row PHONE-FIT-PAGE-COORDS. todo.md 151867 bytes (cap 153600).
- **Canon 7.6** sentence under the MaffsNext usage; one /updates/ line.
- **Gate failure 1 (check-site 44572179542, head 735a008):** ci-deps.py --selftest, "always-run verifiers at most ALWAYS_BUDGET (12)": 133. The loader's `tag.src = src` (a computed value) read to ci-deps as an unknown load on every page loading next-control.js. Fixed in 5c09c245 with `setAttribute('src', ...)`; ci-deps still records schools/assets/scroll.js as next-control.js's dependency (the literal 'scroll.js' resolved beside it). ci-deps.py untouched.
- **Gate failure 2 (check-site 44573475355, head 5c09c24): STOPPED.** Plan job: verify-decimal-detective.py's line 177s + 15s setup = 192s, 71% of 270s against the 70% line limit, selected because next-control.js selects 136 verifiers; already over on main's timings (run 44566476211), not slowed by this PR. The fix was outside this contract's files, so it stopped and reported.
- **Route 1 (Project Claude, DD-VERIFIER-SHARD):** #839 put the verifier on ci-shards and merged as f2e6d2a (entry above); main merged into this branch (one conflict, here in home.md), Gate re-run.
- **Gate failure 3 (check-site 44583202526, head d1fe5b9): STOPPED.** Two plants no longer caught, because wrong() now scrolls Next into view: The 6 P's "the feedback not scrolled into view (the helper never called)" and Sequence Solver's "WORKED: the phone rule undone" (its FIT_JS measured Next in the window). Every other selected verifier passed; the Plan job passed.
- **Jon's ruling (option c), 19 Nov 2026:** the 6 P's plant retired (test-next-control.py's plants guard the reveal); Sequence Solver's FIT_JS measures Next in page coordinates (rect + scrollY against innerHeight - 40, as measure-phone-fit.py:207), so its plant is caught again; canon 7.6.1 sentence: fit is measured in page coordinates, the reveal makes Next reachable but does not count as fitting; the three todo rows stay open (above); phone-fit-state.json unchanged. Main merged in again (conflict in updates/index.html only).
- MERGED 19 Nov as 9da4073 (#837) via merge-pr.py, exit 0, last line "main 9da4073 run 44591763818: GREEN". Main on the merge commit: check-site 44591763818 success, phone-fit-full 44591763629 success (both push runs), pages build 44591762538 success (all confirmed from the API). Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-19-next-in-view.md` (closed out by WRONG-PAUSE-NEXT's first commit).

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

