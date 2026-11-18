LANE: home (Claude Code in the terminal on Jon's PC). SEND: now. The home lane is free (DAILY-ANSWERS merged as #825, aba826a). The cloud lane is on SUMS-IN-DISGUISE-BRIDGE; the two touch no common file.
TIER: Shared (analytics, docs/agent-workflow.md §2). STOP at a green Gate with "Ready for architect review". Project Claude reviews the diff; merge only on Jon's "merge".
RECOMMENDED: Opus 5.5, high effort. A Dashboard reorganised around Jon's weekly questions, one new GA4 aggregate tab, and two chart fixes, each tested on hand-written rows.

TASK: DASHBOARD-GLANCE. Rebuild the analytics Dashboard tab so it answers, at a glance, the six questions Jon asks most weeks:
- Is the site growing?
- Is anything broken?
- Are teachers using it in class?
- Did my posts bring visitors?
- Who uses it?
- Is my newest game landing?
Use data already in the Sheet and in GA4's aggregates. Add one GA4 tab, "GA4 sources daily" (traffic source, device, landing page; no city). Fix the Daily Activity chart's empty key and overshooting curves.

ROOT CAUSE:
- The Dashboard (docs/apps-script-endpoint.js rebuildDashboard, :353 on main aba826a) lists top games, levels, accuracy, hardest questions, escape rooms and daily activity, but answers none of those questions directly.
- Collected but never reported:
  - the GA4 country tabs (canon §1.2.1: filled daily at 06:00, read by nothing; they hold engagedSessions, which the Sheet lacks);
  - game_abandoned's question_index;
  - the portal's filter_applied (filter_type, filter_value), game_card_clicked, section_clicked, ticker_clicked;
  - Misunderstood Maths' fact_viewed, fact_expanded, fact_game_clicked, fact_shared;
  - escape-room hint_used detail (lock:step);
  - launch dates (schools/assets/launch-dates.json).
- Traffic source is not pulled at all, so whether a LinkedIn, Facebook or Tes post brought visitors cannot be seen.
- Daily Activity chart (:543-560): its legend shows colours with no names (Jon's screenshot, 18 Nov 2026, 17:40). curveType 'function' (:556) bows the lines past the real points, so near a trough they dip towards or below zero.

CLASS CHECK: Local to the two report scripts and their tests. Every Sheet row is classed by kind through the existing rptKind, exactly as rptBuild does. The new GA4 tab is one more entry in the existing GA4C_TABLES (docs/apps-script-ga4-country.js:44), so the existing fetch, merge, 3-day settle window, backfill and trigger serve it with no new mechanism. No game page, no analytics.js, and no event, column or endpoint change.

JON'S DECISIONS (18 Nov 2026, verbatim in the PR body):
- 17:40: "can you think of anything else useful we can put onto the dashboard ? we might as well make it all singing and all dancing it we're going to mess about with it. what data do we want to have 'at a glance' ?"
- 17:44: "we currently do nothing useful with the GA4 country daily and events ... think about what information is genuinely helpful that we collect but is not being outputted in a way that I can understand without giving you the entire spreadsheet."
- 17:49: "I ask pretty much all of those most weeks. so lets build, traffic sources without city is still useful ?" Project Claude answered yes. Approved: GA4 traffic source, medium, landing page and device category, as aggregates; NO city or region.

EXACT CHANGE:
0. First commit: DAILY-ANSWERS' close-out per AGENTS.md:
   - #825 merged as aba826a; merge-pr.py last line "main aba826a run 44351676786: GREEN";
   - main check-site 44351676786 success, phone-fit-full 44351676633 success (confirm from the API);
   - its contract to docs/history/contracts/; its home.md "MERGED: pending" filled in;
   - also record in its entry: Jon pasted the file into Code.gs and ran testDashboard, 18 Nov 2026, 17:35; the table showed three columns; no redeploy was needed.
   Then save this contract verbatim as docs/handover/contracts/2026-11-18-dashboard-glance.md.

1. docs/apps-script-ga4-country.js: a third GA4C_TABLES entry:
     tab 'GA4 sources daily'; dimensions ['date', 'sessionSource', 'sessionMedium', 'deviceCategory', 'landingPage'];
     metrics ['sessions', 'engagedSessions', 'activeUsers']; eventFilter false;
     order newest date first, then sessions descending.
   - Keep the GA4C_/ga4c/ga4Country prefix on every new name.
   - Never request city, region or any location dimension other than country, which the existing tabs already hold.
   - Update the header comment, canon §1.2.1's table and docs/ga4-country-setup.md: one extra step, "re-run ga4CountryBackfill once", which fills the new tab from 1 Sep 2026.
   - scripts/test-ga4-country.py: the new table's request asks for exactly these dimensions and metrics. Plant that must fail: 'city' added to its dimensions.

2. docs/apps-script-endpoint.js:
   - SCRIPT_VERSION (:79) → '2026-11-18-a'.
   - The Dashboard reads the three GA4 tabs by name (read-only, never written).
   - A missing or empty GA4 tab gives one line, "GA4 figures not available yet.", in each section that uses it. It never stops the Dashboard.
   - The Dashboard is built in this order, each section with a bold size-11 title. Every cell is written through cellValue. "7 days" means weekRows' boundaries in TIMEZONE; "previous 7 days" is the 7 days before weekAgo (add a prevWeekRows filter in sendDailyReport and pass it in; don't change the existing filters). GA4 figures run to the last complete day.
   A. IS IT GROWING? A headline row: last 7 days against the previous 7, each figure with ▲, ▼ or ▬ and the % change ("new" when the earlier figure is 0):
      - games started;
      - questions answered (rptKind 'question' rows);
      - % correct (marked question rows, rptMarked), shown in neutral grey whichever way it moves;
      - different games played;
      - engaged sessions (GA4 country daily, summed).
      Up is green and down is red, except % correct.
   B. IS ANYTHING BROKEN?
      B1. "Check these questions — possible wrong answer key", last 30 days:
          - which questions: question_ids in rptKind 'question' games with at least RPT_CHECK_MIN = 10 marked answers and under RPT_CHECK_PCT = 0.10 right;
          - columns: game, level, question id, marked answers, % right;
          - lowest first, each row on a red background, and the existing decode line under it;
          - when there are none: "None: every question answered 10+ times has at least 10% right."
      B2. "Where students quit", last 7 days, games with at least 10 game_abandoned rows:
          - columns: game, starts, abandoned, % abandoned, the question position most quit at, how many quit there;
          - highest % first, top 10;
          - a note line: "Position in the run, not which question: game_abandoned carries question_index only."
   C. ARE TEACHERS USING IT?
      C1. "Probably a class (estimate: RPT_CLASS_STARTS = 10 or more starts of one game, each within RPT_CLASS_GAP_MIN = 30 minutes of the one before)", last 7 days:
          - columns: game, date, first start, last start, starts, questions answered from the first start to 30 minutes after the last;
          - newest first; "None this week." when empty.
      C2. "When it is used", last 30 days of game_started:
          - rows: Mon-Fri, Sat-Sun;
          - columns: before 09:00, 09:00-15:30, 15:30-18:00, 18:00-22:00, after 22:00;
          - footnote: "School day = 09:00-15:30, Mon-Fri. Term dates not applied."
      C3. "What people look for on the portal", last 7 days: filter_applied counted by filter_type and filter_value, top 10.
   D. DID MY POSTS BRING VISITORS? (GA4 sources daily)
      D1. "Visitors by channel", last 7 days against the previous 7: sessions, engaged sessions, % engaged and the change in engaged sessions. Channels, matched in this order, case-insensitive:
          - Google search (source contains google, medium organic);
          - Other search (medium organic);
          - LinkedIn (source contains linkedin or lnkd);
          - Facebook (source contains facebook or fb);
          - Tes (source contains tes.com);
          - Direct (source "(direct)");
          - Other (everything else).
          Constants for the matching lists.
      D2. "Top landing pages", last 7 days, by engaged sessions, top 10.
   E. WHO USES IT?
      - "UK share": the United Kingdom's engaged sessions as % of all, 7 days;
      - top 5 countries by engaged sessions;
      - device split (mobile, desktop, tablet) of engaged sessions, 7 days.
   F. IS MY NEWEST GAME LANDING? "New games (launched in the last 14 days)":
      - fetch https://raw.githubusercontent.com/OrthogonalMaffs/maffsgames/main/schools/assets/launch-dates.json the way rptLoadKinds fetches games.json (cached, muteHttpExceptions); on failure, one line "Launch dates could not be read today." and carry on;
      - columns: game, launched, starts, questions answered, % correct (question games; rooms show escapes as Table 4b does; shot games "–"), completed, all since launch;
      - newest first.
   G. ESCAPE ROOMS. Table 4b as now, then "Hints by lock", last 30 days: hint_used rows counted by room and lock (the lock id before ":" in detail), most first.
      Time per lock from game_completed's detail (locks:...) ONLY if the engine's meaning of those numbers can be confirmed from escape-rooms/assets/engine.js; otherwise leave it out and say so in the PR (see STOP IF).
   H. MISUNDERSTOOD MATHS, last 7 days, one row: facts viewed, expanded, game links clicked, shared, and game clicks as % of views.
   I. The existing tables, unchanged in content, in this order: Top games, Accuracy by game, Hardest questions, Levels.
   J. Daily Activity (Table 5) with its chart, LAST. The chart's series take their names from the header row (legend "Games Started", "Questions Answered"). curveType is removed, so the lines are straight. Nothing else changes.

3. scripts/test-apps-script-report.py: a test per section on hand-written rows (including hand-written GA4 tab rows), every figure worked out by hand. Include:
   - headline "new" when the earlier week is 0, and % correct neutral;
   - check-these: 9% on 11 answers listed, 10% on 10 not listed, 0% on 9 not listed, a room's lock never listed;
   - quit points: a game with 9 abandons left out;
   - class: 10 starts 29 minutes apart counted, a 31-minute gap splitting it, 9 starts not counted;
   - when-used: a 15:29 Tuesday start in the school day, 15:30 in 15:30-18:00, a Saturday 10:00 in Sat-Sun;
   - channels: lnkd.in to LinkedIn, m.facebook.com to Facebook, google / organic to Google search, bing / organic to Other search, (direct) to Direct;
   - a missing GA4 tab giving the line, not an error;
   - new games: launched 13 days ago in, 15 days ago out; a failed launch-dates fetch giving the line;
   - hints by lock from "lock:step" detail;
   - the chart: named series and no curveType.
   Plants that must fail:
   - the 10% threshold made ≤;
   - the class gap made 60 minutes;
   - % correct coloured green or red;
   - lnkd.in falling into Other;
   - a missing GA4 tab throwing;
   - a room counted in check-these;
   - curveType back.
   Every existing test passes unchanged.

4. docs/apps-script-redeploy.md: a note under the deploy steps: "A change only to the Dashboard, the daily email or the GA4 file (not doPost) needs no deployment: paste, save, run testDashboard. Timers run the latest saved code (Jon, 18 Nov 2026: DAILY-ANSWERS went live this way)." Step 12's expected version becomes '2026-11-18-a'.

5. docs/handover/home.md entry, ending with Jon's steps after merge: paste docs/apps-script-endpoint.js into Code.gs (keeping his REPORT_EMAIL line) and docs/apps-script-ga4-country.js into ga4-country.gs; save; run ga4CountryBackfill once; run testDashboard. Never Deploy.

6. When the Gate is green, STOP with "Ready for architect review". After Project Claude's review and Jon's "merge", merge with scripts/merge-pr.py.

DO NOT TOUCH:
- doPost, doGet, EXPECTED_HEADERS and every column; analytics.js and every game page (no new event or parameter).
- The daily email's text.
- rptBuild, rptKind, rptMarked and the existing tables' contents (they only move).
- The existing two GA4 tabs' columns, and the trigger times.
- data/games.json and schools/assets/launch-dates.json (read only).
- REPORT_EMAIL stays the placeholder (canon §7.7).
- No city, region or other location dimension.
- No draft PR.

SUCCESS CONDITION:
- Every section's test figures match the hand-written ones; every plant fails; every existing test (both scripts) passes.
- The new GA4 table requests exactly the approved dimensions.
- The chart has named series and straight lines.
- SCRIPT_VERSION is '2026-11-18-a'.
- The runbook, setup doc and canon §1.2.1 are updated.
- After "merge": merged by merge-pr.py, reported with its last line, the merge commit and main's check-site and phone-fit-full run IDs; handover committed with Jon's steps.

STOP IF:
- The meaning of game_completed's "locks:" times cannot be confirmed from engine.js (leave time per lock out and report what the numbers appear to be).
- GA4's Data API names differ from those given (sessionSource, sessionMedium, deviceCategory, landingPage); report the right names before using any.
- The test harness cannot exercise a section without changing its stubs beyond adding what that section calls; report what it needs.
- Any figure would need a new event, column or a location dimension finer than country.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
