# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-18 (home): DASHBOARD-GLANCE (the Dashboard answers Jon's weekly questions; GA4 sources tab; Daily Activity chart fixed)

Claude Code (home lane), worktree `~/mg-dashboard-glance`, branch `claude/dashboard-glance`; contract `docs/handover/contracts/2026-11-18-dashboard-glance.md`. The first commit carries DAILY-ANSWERS' close-out (#825, aba826a). Tier Shared: holds at a green Gate for Project Claude's review and Jon's "merge".

- **Dashboard (`docs/apps-script-endpoint.js`, SCRIPT_VERSION 2026-11-18-a):** sections A (growing: 7 days against the previous 7; % correct in points, always grey), B (check-these questions under 10% right on 10+ marked, on red; where students quit), C (probable classes; when it is used; portal filters), D (GA4 channels and landing pages), E (UK share, top 5 countries, devices), F (games launched in the last 14 days, launch-dates.json read from GitHub), G (Table 4b, hints by lock, time per lock), H (Misunderstood Maths), I (the four older tables, content unchanged, moved), J (Daily Activity last: series named by `setNumHeaders(1)`, curveType removed). sendDailyReport and testDashboard pass prevWeekRows (the 7 days before weekAgo); the existing filters are unchanged. A missing or empty GA4 tab gives "GA4 figures not available yet." in A, D and E. The email's text is unchanged.
- **Time per lock:** included. engine.js `st.openAt[l.id] = st.played` (the room's clock seconds when a lock opened), written by finish() in room.js lock order, "-" if never opened; opened locks sorted by time give the seconds since the previous one opened.
- **GA4 (`docs/apps-script-ga4-country.js`):** a third GA4C_TABLES entry, 'GA4 sources daily' (date, sessionSource, sessionMedium, deviceCategory, landingPage; sessions, engagedSessions, activeUsers; newest date, then most sessions, then the dimensions). The four dimension names are in Google's Data API schema (landingPage is the path, no query string). No city or region.
- **Tests:** test-apps-script-report.py section j (A to H on hand-written rows and GA4 tab rows, through sendDailyReport) plus a chart check; 20 plants caught, 7 of them new. Stubs gained only what the sections call: load() takes GA4 tabs and launch dates, setBackground/setFontColor record their colour, and formatDate honours its zone (it ignored it, so a midnight in BST became the day before) and gains 'HH:mm' and 'u'. Section i's curveType clause removed (contract J). test-ga4-country.py: the mock serves the sources table, a check that it asks for exactly the approved dimensions and nothing finer than country, plant 'city' caught. test-ga4-summary.py unchanged and passes.
- **Docs:** canon §1.2.1 (third tab) and §1.4 (an at-a-glance paragraph); docs/ga4-country-setup.md (the sources tab, re-run ga4CountryBackfill once); docs/apps-script-redeploy.md (no deployment for a Dashboard-only change; step 12's version 2026-11-18-a).
- **Jon's steps after merge (never Deploy):** 1. paste `docs/apps-script-endpoint.js` into Code.gs, keeping your REPORT_EMAIL line; 2. paste `docs/apps-script-ga4-country.js` into ga4-country.gs; 3. Save; 4. run `ga4CountryBackfill` once (fills GA4 sources daily from 1 Sep 2026); 5. run `testDashboard`.
- MERGED: pending.

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

## 2026-11-16 (home): HEATWAVE-PACK (The Heatwave Mutiny print pack, DRAFT; a sixth patrol variant)

Claude Code (home lane), worktree `~/mg-heatwave-pack`, branch `claude/heatwave-pack`; contract `docs/handover/contracts/2026-11-16-heatwave-pack.md` (the reissue; the first HEATWAVE-PACK stopped on 5 patrol variants). The first commit carries PE-SHED-FINAL's close-out (#803, 6e1f4e0; its entry below).

- **Patrol variant:** the reissue's first STOP IF was met too: no sixth patrol-lcm-timer variant passes keep()'s spread at minsep 14 (check() holds answers to 101-192; 112-126-140-154 are 14 apart; the widest gap left is 12). Jon chose in session (16 Nov) to append laps 4, 8, 21 (LCM 168, common wrong answer 33) in an append-only second pass at minsep 12. The five existing variants are unchanged; variants.json and room.js gain that one variant only. check-escape-rooms: heatwave-mutiny VALID 270 of 360, variant 0 VALID. /updates/ line added (the Hamster Heist precedent of the same day).
- **Pack:** `rooms/heatwave-mutiny/config.json` (6 sets, seed 1, DRAFT, certificate "Cold air, already paid for", no answer_units, no readout_voice: the hook is the narrator's) and the eleven WebPs (hw-01-rota ... hw-11-disruptor-dial). Label boxes measured by pixel as in #801 (grown blank rectangle, 26 px inside; the sticky note's blank is its own yellow). Print-only words on all six clues; fan and jacket print no words (the plug's label is 109 x 81 px; the jacket has no blank surface).
- **Generator (general, other packs byte-identical):** split_clue() accepts a clue with no `<b>` part when the image gives both "printed" and "caption" (the clock and sticky note have none); lock_words takes a "label" for the answer box (the keypad's "four digits" breaks Amendment 4 on paper; the slider's label printed "... set off min").
- **lockcheck.py:** LCM by counting up in the longest lap, with the prime-factor lines; cube by face, edge counted up, edge cubed; inequality by trying every dial setting, the one prime, the band's largest. All 22 library variants agree.
- **Checks:** see the PR. Other packs compared with ~/pe-tools/dump.py before (origin/main) and after: 28 files identical once date fields and worktree paths are normalised.
- MERGED 16 Nov as 61b2f9a (#804) via merge-pr.py on its second call; last line "main 61b2f9a: NO RUN FOUND", exit 1, as it looked before main's push runs registered; the merge itself succeeded. Main on the merge commit: check-site 44028365136 success, phone-fit-full 44028365052 success. Contract moved to `docs/history/contracts/` (closed out by FINAL-PADLOCK-FAIR's first commit).

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

