LANE: cloud (Claude Code on the web). Send now; the cloud lane is free.
MODEL: Claude Code, Opus 5.5, medium effort. A one-line fix, plus a test stub that must model real Sheets' behaviour faithfully.

TASK: Stop Dashboard counts showing as percentages by resetting every cell's number format at the start of rebuildDashboard.

ROOT CAUSE: Jon proved it in real Sheets on 19 Nov 2026 at 09:48 (checkPercentCells). Sheet.clear() (docs/apps-script-endpoint.js:883, in rebuildDashboard) does NOT remove number formats. Log, verbatim: `Games started: D7 = 88, format "0%"`; `Mon-Fri: D39 = 244, format "0.###############"`; `Sat-Sun: D40 = 35, format "0%"`; `after Sheet.clear(): format "0%"`. A "0%" left over from an earlier layout or run stays on its cell, and the next count written there shows as a percentage. The affected cells move with the data (18 Nov: Mon–Fri 15:30–18:00; 19 Nov: Sat–Sun D40), so any section can be hit. The test stub hides this: sheetFake's clear() wipes everything and setNumberFormat is a no-op (scripts/test-apps-script-report.py:136, 145).

CLASS CHECK: A bug class. The cause is shared setup in rebuildDashboard that every section depends on, so the fix goes at that single entry point. No per-cell or per-section patches. The only percentages left afterwards are the ones each section sets deliberately on that run.

EXACT CHANGE:
1. First commit (close-outs, before any code):
   a. #830 PRINTABLES-CORE (home lane's PR, recorded in cloud.md because the cloud lane edits only its own handover, as #829 recorded #828 in home.md). Read main's runs on merge commit 006d3d8 from the GitHub API (check-site, phone-fit-full, pages build). Add a dated close-out line to this task's cloud.md entry with those run ids and conclusions. Move docs/handover/contracts/2026-11-19-printables-core.md to docs/history/contracts/.
   b. cloud.md's DD-LINEUP-ORDER (#828) entry still ends "Next: PR, Gate and phone-fit-full, merge with merge-pr.py." Replace that line with the merged facts as home.md:34 records them: MERGED 18 Nov as 5a56852, merge-pr.py last line "main 5a56852 run 44376293965: GREEN", main's check-site 44376293965, phone-fit-full 44376293770 and pages build 44376293960 all success, contract already in docs/history/contracts/.
   c. Save this contract verbatim as docs/handover/contracts/2026-11-19-dashboard-percent-cells.md.
2. docs/apps-script-endpoint.js, rebuildDashboard: straight after `dash.clear();` (line 883, inside the `if (dash)` branch), reset the number format of the whole sheet in one call: `dash.getRange(1, 1, dash.getMaxRows(), dash.getMaxColumns()).setNumberFormat('General');` with a one-line comment: Sheet.clear() leaves number formats in place (proven in real Sheets, 19 Nov 2026), so a stale "0%" would show the next count written to that cell as a percentage. Leave the newly inserted sheet branch alone: it has no stale formats.
3. SCRIPT_VERSION (line 79): '2026-11-18-b' becomes '2026-11-19-a'. docs/apps-script-redeploy.md step 12 (line 171): the version string becomes 2026-11-19-a.
4. scripts/test-apps-script-report.py, sheetFake:
   - Add a per-cell number-format map (e.g. `sh.numFmt`) that clear() does NOT wipe, matching real Sheets. setNumberFormat(f) records f on every cell in the range's dims (r, c, nr, nc). Add getMaxRows() and getMaxColumns(), returning at least the largest row and column ever written or formatted (a fixed generous size such as 1000 × 26 is fine).
   - New check: after a normal rebuild, choose a cell holding a whole-number count ≥ 2 (find it from the output; do not hard-code a row). Plant "0%" on it in numFmt, rebuild with the same data, and assert its format is no longer "0%".
   - New invariant check over the whole rebuilt Dashboard: every cell whose recorded format is a percent ("0%" or containing "%") holds a number from 0 to 1, or is empty. A count under a percent format fails.
   - New plant: rebuildDashboard with the reset line removed (source text substitution, as the existing plants do). Both new checks must catch it. Report the new plant count.
   - Every existing check and plant must still pass unchanged.
5. docs/todo.md: move row DASHBOARD-PERCENT-CELLS (§1) word for word to docs/history/todo-done.md with a done note: cause proven (Sheet.clear() keeps number formats), fixed by this PR; Jon's eye check after paste. todo.md must end smaller than it started (152,846 bytes on main at 1aebc5b; cap 153,600).
6. cloud.md entry for this task: what changed, plants, PR, merge facts, and Jon's steps after merge (below). No /updates/ line (internal).
7. PR, Gate and phone-fit-full green, then merge with `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600` and report its last line. No draft PR.

Jon's steps after merge, for the PR body and cloud.md, one at a time; never Deploy (doPost and doGet are unchanged):
   1. Paste docs/apps-script-endpoint.js into Code.gs, keeping your REPORT_EMAIL line.
   2. Save.
   3. Run testDashboard.
   4. Look at "Different games played" and the When-used rows (Mon–Fri, Sat–Sun): counts must show as whole numbers, not percentages.
   5. Delete the temporary `check` script file if it is still there.

DO NOT TOUCH: doPost, doGet or anything that would need a new Deploy; any section's deliberate setNumberFormat('0%') calls (lines 508, 549, 589, 702, 735, 742, 759, 797, 872, 1007, 1101); dashChart and the chart specs from #829; docs/apps-script-ga4-summary.js and ga4-country.gs; REPORT_EMAIL; docs/handover/home.md; schools/assets/; the workflow; canon; any game.

SUCCESS CONDITION: rebuildDashboard resets number formats straight after clear(); the stub

---

Amendment 1 (Jon, 19 Nov 2026). Your copy of the contract was cut off in transit. It goes on from "the stub" in SUCCESS CONDITION exactly as below. Save the contract verbatim as the text you received, followed by this amendment, in docs/handover/contracts/2026-11-19-dashboard-percent-cells.md.

TIER: Small (one Apps Script file, its test and docs). Model: Claude Code, Opus 5.5, medium effort.

Your numFmt plan is right: number formats go in a separate numFmt map that clear() leaves alone; fmt (backgrounds, font colours) and its clear() behaviour stay as they are.

SUCCESS CONDITION (complete): rebuildDashboard resets number formats straight after clear(); the stub keeps formats through clear(), as real Sheets does; the two new checks pass; the reset-removed plant is caught by both; all existing checks and plants pass; SCRIPT_VERSION is 2026-11-19-a in the script and redeploy.md; the todo row is moved and todo.md is smaller; #830 and #828 are closed out in cloud.md and #830's contract is moved; the PR is merged via merge-pr.py with a GREEN last line; cloud.md records it all, including Jon's five steps.

STOP IF: merge-pr.py cannot reach GitHub (report its output; the PR waits); the GitHub API cannot give main's runs on 006d3d8 (record "not confirmed" and carry on, do not guess); modelling formats that survive clear() changes the result of any existing check or plant (report which, and why); a deliberate percent cell fails the new invariant (that would be a second bug: report it, do not fix it here); any file would pass its size cap; anything in docs/handover/contracts/2026-10-27-standing-stop-rules.md applies (report each under "Decided for you").

Jon's steps after merge, for the PR body and cloud.md, one at a time; never Deploy (doPost and doGet are unchanged):
   1. Paste docs/apps-script-endpoint.js into Code.gs, keeping your REPORT_EMAIL line.
   2. Save.
   3. Run testDashboard.
   4. Look at "Different games played" and the When-used rows (Mon–Fri, Sat–Sun): counts must show as whole numbers, not percentages.
   5. Delete the temporary `check` script file if it is still there.

Everything you received before the cut stands unchanged. Start with the close-out commit.
