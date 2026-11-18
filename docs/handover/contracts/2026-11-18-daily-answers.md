LANE: home (Claude Code in the terminal on Jon's PC). SEND: now. The home lane is free (CANTEEN-APPROVE merged as #819, 6f2d29c) and the cloud lane is idle after #824. Jon moved this from cloud to home, 18 Nov 2026, 15:54.
TIER: Shared (analytics, docs/agent-workflow.md §2). STOP at a green Gate with "Ready for architect review". Project Claude reviews; merge only on Jon's "merge".
RECOMMENDED: Sonnet 5.5, medium effort. One function in one Apps Script file, plus its existing CI test.

TASK: DAILY-ANSWERS. Add a "Questions Answered" column to the Dashboard's Daily Activity table and a second line on its chart, so each day shows games started and questions answered together.

ROOT CAUSE: docs/apps-script-endpoint.js, rebuildDashboard, TABLE 5 (from :515 on main ddc11e6):
- It counts only game_started rows by day (:517-522).
- It writes a two-column table (Date, Games Started; header :528, rows :530-533).
- It draws a one-series line chart (:535-549).
A day's games started does not show how much work was done, because some games have many more questions than others. The same monthRows already hold every question_answered row.

CLASS CHECK: Local. One table in one report function; no other table or caller is affected. The kind of game comes from the existing shared helper rptKind (:139), not a new rule.

JON'S DECISIONS (17 Nov 2026, verbatim in the PR body):
- 13:52: "can we add questions answered to it ? games started is an important stats, but some games have many more questions than others, these 2 numbers together give us a better image of the entire picture".
- One chart with two axes: games started on the left, questions answered on the right, with a legend.
- Questions only: count question_answered rows whose rptKind is 'question'. Escape rooms ('room') and shot games such as Trig Wars ('shot') are left out. Every such row counts, whether or not it is marked (this is a count of answers, not accuracy).
- 18 Nov 15:54: home lane, now.

EXACT CHANGE:
0. First commit: CANTEEN-APPROVE's close-out per AGENTS.md: #819 merged as 6f2d29c; merge-pr.py last line "main 6f2d29c run 44235030804: GREEN"; main check-site 44235030804 success, phone-fit-full 44235030742 success (confirm both from the API); its contract docs/handover/contracts/2026-11-18-canteen-approve.md to docs/history/contracts/; its home.md entry's "MERGED: pending" filled in. Then save this contract verbatim as docs/handover/contracts/2026-11-18-daily-answers.md.
1. docs/apps-script-endpoint.js, TABLE 5:
   - Count by day, using Utilities.formatDate(..., TIMEZONE, 'yyyy-MM-dd') as now:
     - game_started rows;
     - question_answered rows with rptKind(slug, kinds) === 'question'.
     Both tallies are rptMap maps (COUNTS-SAFE-TALLY).
   - Days = the sorted union of both maps' keys; a missing count is written as 0.
   - Header row: ['Date', 'Games Started', 'Questions Answered'], in the same bold, #f0f0f0 style, over 3 columns. Every row is written through cellValue.
   - Chart (still only when days.length > 1):
     - the range is 3 columns (Date plus two series);
     - keep the LINE type, the position, the size 500 × 280, curveType and the starts colour #0ea5e9; questions answered are #0d9488;
     - series 0 on axis 0 and series 1 on axis 1 (series: {1: {targetAxisIndex: 1}});
     - vAxes titled 'Games started' and 'Questions answered';
     - legend {position: 'bottom'};
     - title 'Daily Games Started and Questions Answered — Last 30 Days'.
   - The section title stays 'Daily Activity — Last 30 Days'. Column 3's width stays 80 unless the header is cut off; if it is, widen column 3 only.
2. scripts/test-apps-script-report.py: a test with hand-written rows over at least three days, including:
   - one day with answers but no starts;
   - one 'room' slug and one 'shot' slug;
   - one question row with correct null.
   Expected figures written by hand. Plants that must fail:
   - room answers counted;
   - shot answers counted;
   - a day with no starts dropped.
3. docs/handover/home.md entry. Note in it: Jon must paste the updated file into Apps Script per docs/apps-script-redeploy.md (with his address in REPORT_EMAIL) before the Dashboard changes.
4. When the Gate is green, STOP with "Ready for architect review" (Shared tier). After Project Claude's review and Jon's "merge", merge with scripts/merge-pr.py.

DO NOT TOUCH:
- The daily email (sendDailyReport's text), every other Dashboard table and chart, rptBuild, rptKind, rptMarked, doPost, doGet, the headers, the trigger.
- REPORT_EMAIL stays the placeholder (canon §7.7: no owner address in the repo).
- data/games.json; any game page; analytics.js.
- docs/handover/cloud.md (the cloud lane owns it; its trim and #824's close-out go with the next cloud contract).
- No draft PR.

SUCCESS CONDITION:
- The test passes with the hand-written figures, and its three plants fail; every existing test in the file passes unchanged.
- Table 5 has three columns, with one row for every day that has either count.
- The chart has two series on two axes, with a legend.
- After "merge": merged by merge-pr.py, reported with its last line, the merge commit and main's check-site and phone-fit-full run IDs. Handover committed, including the paste step for Jon.

STOP IF:
- The test harness cannot run rebuildDashboard's chart builder (a stub is missing) without a change to the stubs beyond adding the two chart options; report what it needs.
- Counting by rptKind would count a slug differently from rptBuild for the same row.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
