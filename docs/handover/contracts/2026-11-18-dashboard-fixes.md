DASHBOARD-FIXES — home lane (Claude Code, terminal). Tier: Medium (merge on green). Send: now.
Recommended: Opus, high effort — one bug has no known cause and must be found by reasoning about Apps Script/Sheets behaviour before anything is changed.

TASK: Fix two Dashboard bugs (charts drawing their header row as data; two count cells shown as percentages), add standing ruling SR-33 to canon, and close out #827 and #828.

ROOT CAUSE:
(1) Charts: in docs/apps-script-endpoint.js the Top Games bar chart (newChart at :963), the Accuracy bar chart (:996) and the pie (:1047) are built without .setNumHeaders(1); only the Daily Activity line chart (:1093–1096) sets it. Without it Sheets may treat the header row as data, so "Game" is drawn as a category.
(2) Percent cells: on Jon's live Dashboard (18 Nov 2026, after #827) two column-D cells holding counts show percent format: section A's "Different games played" value (90 shows as 9000%) and section C2's Mon-Fri "15:30-18:00" value (245 shows as 24500%). The cause is NOT known. Project Claude read the code and found nothing that formats those cells: rebuildDashboard calls dash.clear() (:883), which should wipe formats; every setNumberFormat('0%') call found (:508, :549, :589, :702, :735, :742, :759, :797, :872, :1023, formatPercentColumn :1119–1121 called from :927, :957, :989) targets a different cell. Finding the real cause is part of this task.
(3) SR-33 approved by Jon on 18 Nov 2026 (about 20:04) and not yet in canon.
(4) #827 (DASHBOARD-GLANCE) and #828 (DD-LINEUP-ORDER) merged without their close-outs.

CLASS CHECK:
(1) Yes, a bug class: the same missing call appears in three charts, and each chart is built by hand. EXACT CHANGE puts every Dashboard chart through one shared builder that always sets the header row, not three separate .setNumHeaders(1) patches.
(2) Unknown until the cause is found. If the cause is a formatting write that can land on the wrong cell, or formats left over that dash.clear() does not remove, it is a class (every cell the Dashboard writes is exposed): the fix goes in the shared writing layer so each written cell gets its number format set explicitly (counts plain, rates '0%'), never left to whatever the cell held before. If it is one specific line's bug, say why it is local and fix that line.
(3), (4) Not bugs: documentation and the standing close-out rule (AGENTS.md :61).

EXACT CHANGE:
A. First commit: close-outs (AGENTS.md :61, :82).
  - #827 DASHBOARD-GLANCE: merge commit bc3d19202d6609bfd11f73bf8d93fd328e52843c; merge-pr.py last line "main bc3d192 run 44370288253: GREEN"; main's runs check-site 44370288253 and phone-fit-full 44370288214 — confirm both from the GitHub API before recording. Replace "- MERGED: pending." in docs/handover/home.md (DASHBOARD-GLANCE entry, currently :29) with the MERGED line in the same form as the DAILY-ANSWERS entry (:43). Move docs/handover/contracts/2026-11-18-dashboard-glance.md to docs/history/contracts/.
  - #828 DD-LINEUP-ORDER: merge commit 5a56852; last line "main 5a56852 run 44376293965: GREEN"; check-site 44376293965, phone-fit-full 44376293770, pages build 44376293960 — confirm from the API. Record it in docs/handover/cloud.md's DD-LINEUP-ORDER entry ONLY if this lane may edit that file; AGENTS/home.md say cloud owns cloud.md, so if it may not, record the close-out in home.md's new entry and leave cloud.md alone. Move docs/handover/contracts/2026-11-18-dd-lineup-order.md to docs/history/contracts/.
  - Save this contract verbatim as docs/handover/contracts/2026-11-18-dashboard-fixes.md in the same commit.
B. Charts (docs/apps-script-endpoint.js): add one helper that builds a Dashboard chart from a spec (type, ranges, position, options) and always calls .setNumHeaders(1); build all four charts (Top Games, Accuracy, pie, Daily Activity) through it. Each chart's ranges must still start at its header row (they do: t1Start+1, t3Start+1, etc.), so the header supplies series/category names. Keep each chart's look (colours, sizes, positions, titles) unchanged.
C. Percent cells — in this order:
  1. Find the cause. Trace every write and format call that can touch those two cells (row positions from r, rowBelowChart, every setNumberFormat, the string parsing Range.setValues applies to strings such as "12%", and what Sheet.clear() does and does not clear per Google's Apps Script documentation). Reproduce it in scripts/test-apps-script-report.py's stubs if the stubs can model it. Report the cause with file:line, and how you know, in the PR and in home.md.
  2. Fix per CLASS CHECK (2).
  3. Add a test to scripts/test-apps-script-report.py that fails on the old code (or, if the cause cannot be modelled in the stubs, a test that every count cell in sections A and C2 ends with a non-percent format and every rate cell with '0%'), with a plant that it catches.
  4. Bump SCRIPT_VERSION (currently '2026-11-18-a') and step 12 of docs/apps-script-redeploy.md to match.
D. Chart test: extend section i's chart check in scripts/test-apps-script-report.py so every chart built must call setNumHeaders(1); plant one chart without it and show the test catches it.
E. SR-33 in docs/canon.md:
  - §0.3: add after the SR-32 row (currently :94), as its own row:
| SR-33 | **Foundational skills are priority-audience work.** Primary-level skills (place value, number bonds, times tables, crossing the tens, the four operations, first fractions) count as §0.2 priority 2 when built for teenagers and adults: resit students' gaps often go back to primary school, which is why Functional Skills Entry Levels exist. A game made only for young children (a child-only look and wording) stays priority 6. Where a game also serves a primary class, build one bank with two looks, as Sums in Disguise does: the adult version on the main site under SR-11's age-neutral labels, the child version a separate unlisted page. | 18 Nov 2026 | Jon, 18 Nov 2026 (chat) |
  - §0.2 point 2 (currently :46): change
"**Work for the priority audience.** Grade 1–3 and resit content, and making it findable by the people who teach it."
to
"**Work for the priority audience.** Grade 1–3 and resit content, including the foundational skills behind it (SR-33), and making it findable by the people who teach it."
F. docs/handover/home.md: a new entry for this task (done, cause found, Jon's steps after merge). Jon's steps after merge, never Deploy: 1. paste docs/apps-script-endpoint.js into Code.gs, keeping his REPORT_EMAIL line; 2. Save; 3. run testDashboard. Keep home.md within its archiving limit.
G. No /updates/ line: the Dashboard is internal, not seen by students or teachers (AGENTS.md :80).

DO NOT TOUCH:
- Any game, the portal, schools/assets/, or anything students or teachers see.
- docs/apps-script-ga4-country.js and docs/apps-script-ga4-summary.js (read ga4-summary.js :192–194 as the pattern for a header-setting chart loop; do not edit it).
- The daily email's text, the Dashboard's sections, their order, wording, filters and figures (only the chart builder and number formats change).
- Gate files (workflow, scripts/ci-*, ci_shards.py, merge-pr.py, check-context-size.py, check-changed.py).
- docs/handover/cloud.md, if this lane does not own it.
- Anything that calls for a new Apps Script deployment: no change to doPost/doGet or the web app.
- Personal or identifying details beyond "Jon".

SUCCESS CONDITION:
- First commit holds both close-outs and this contract, with run IDs confirmed from the API.
- All four charts are built by the one helper; no newChart() call elsewhere in endpoint.js; the chart test fails on a planted chart without setNumHeaders(1) and passes on the fix.
- The percent-cell cause is stated with file:line and evidence; the new test fails on the old code (or its plant) and passes on the fix.
- SR-33 row and the §0.2 wording are in canon exactly as above.
- scripts/test-apps-script-report.py, test-ga4-country.py and test-ga4-summary.py pass; Gate green; merged with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, last line reported.
- home.md entry written, including Jon's three steps.

STOP IF:
- The percent-cell cause cannot be found or demonstrated: do not ship a guessed fix for it. Report what you ruled out and ask Jon (he can send a screenshot of the cells' Format > Number setting or of the sheet). Bugs B, D, E and the close-outs may still merge.
- The fix needs a new Apps Script deployment, a new trigger, or any change to what data is collected.
- A run ID in section A does not match the API, or main is red.
- Building the charts through one helper would change any chart's look or position.
- Canon §0.2 point 2 or the SR-32 row no longer reads as quoted above.
