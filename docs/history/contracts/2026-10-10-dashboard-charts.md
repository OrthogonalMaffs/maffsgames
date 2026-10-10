CONTRACT: DASHBOARD-CHARTS (Project Claude for Jon, 10 Oct 2026, 08:35). Either lane. Small.
Save verbatim under docs/handover/contracts/ when it starts.

======================================================================
TASK (DASHBOARD-CHARTS): Make the Sheets dashboard's Accuracy chart
show 0–100% every day without Jon editing it, stop the dashboard's
charts overlapping each other, and keep games with no right answer out
of the accuracy tables.

ROOT CAUSE (read in docs/apps-script-endpoint.js, rebuildDashboard):
1. The axis. Table 3 writes each accuracy as a STRING, pct + '%'
   (e.g. "17%"). Sheets parses that into the NUMBER 0.17 shown as a
   percentage. Chart 3 reads that column, so its data runs 0 to 1, but
   it is built with hAxis {minValue: 0, maxValue: 100}, so the axis runs
   to 10,000% and every bar is a sliver. The dashboard is cleared and
   rebuilt from scratch on every daily run, which is why Jon's manual
   fix is undone each morning.
2. The overlap. Every chart is anchored at its table's first row in
   column F (setPosition(tStart, 6, 0, 0)), but each chart has a FIXED
   pixel height (300 or 280 px) while each table's height depends on how
   many rows it has that day. When a table is short (Level Breakdown is
   about nine rows, roughly 190 px), its chart runs past the next
   table's start and the next chart is drawn on top of it (today: the
   Accuracy chart covers the bottom of the Level Split pie).
3. Prisoners' Dilemma has no right answer, so its 79 answers count as
   0 correct and it tops "Accuracy by Game (sorted lowest first)" every
   week, as it tops "Hardest Questions". This is the open item "exclude
   correct = null" (state-of-play, awaiting Jon), and it is the same
   code.

CLASS CHECK:
1. Yes, a class: three tables (Top Games' Completion %, Accuracy by
   Game, Hardest Questions) all write percentages as strings and rely on
   Sheets' parsing. Fix it once: write the number (a fraction) and set
   the cell format to '0%' for all three; set Chart 3's axis to match
   the data (0 to 1). Do not just change 100 to 1 and leave the string
   parsing in place.
2. Yes, a class: the layout rule (row anchor vs pixel height) applies
   to every chart. Fix it in one place: after each table-and-chart
   section, advance the row counter to at least the chart's bottom row
   (tStart + ceil(chartHeight / rowHeight) + 1, using the sheet's
   default row height), so the next section always starts below the
   previous chart. Each chart stays beside its own table.
3. Yes, a class: both accuracy tables share the "correct" counting. A
   row with a blank `correct` (no right answer) is excluded from both
   totals, through one shared filter.

EXACT CHANGE (docs/apps-script-endpoint.js only):
1. Tables 1, 3 and 4: write the fraction (e.g. 0.17), not pct + '%',
   and apply setNumberFormat('0%') to the percentage column. Values must
   display exactly as today (17%).
2. Chart 3: hAxis {minValue: 0, maxValue: 1, format: 'percent'}.
3. One helper that, given a section's start row and its chart's height
   in px, returns the first free row below the chart; use it after every
   section that has a chart (Charts 1, 2, 3, 5). Remove no chart.
4. One shared filter, used by Accuracy by Game and Hardest Questions:
   count only question_answered rows whose `correct` cell is 'true' or
   'false'. Rows with a blank `correct` are left out of both tables.
5. Bump SCRIPT_VERSION, so Jon's redeploy can be confirmed.
6. In the PR description and the handover, the redeploy steps for Jon:
   paste the new script into the Apps Script editor, Deploy → Manage
   deployments → edit → New version, then run rebuildDashboard (or wait
   for the next daily run) and check the version line. Jon has to do
   this; the repo copy does not deploy itself.

DO NOT TOUCH: doPost and cellValue(); the daily email's content; the
backfill function; analytics.js and every game; any table's columns or
headings; the GA4 side.

SUCCESS CONDITION: after Jon redeploys and the dashboard rebuilds, the
Accuracy chart's axis reads 0% to 100% with no manual edit; no chart
overlaps another or a table at today's row counts, and the helper would
hold for a longer or shorter table; every percentage cell shows as
before; prisoners-dilemma is absent from Accuracy by Game and Hardest
Questions; the version line shows the new SCRIPT_VERSION.

STOP IF: prisoners-dilemma writes `correct` as false rather than blank
(then the filter cannot tell it apart: report, and do not exclude it by
slug — that needs a game-side change and Jon's ruling); any other game
writes blank `correct` on questions that do have a right answer (list
them; excluding them would hide real wrong answers).
