# Contract SIX-PS-THREE-BANKS (Project Claude, 26 Oct 2026), verbatim; stored by the home lane, not yet started

TASK: Add three 6 P's topic banks drawn from existing live games (given-that, coordinate-geometry-dash, constructions-lab), then measure the 6 P's page for phone and classroom fit before Jon lists it.

ROOT CAUSE: The 6 P's banks cover topics worth 1,060 of 1,800 marks (59%) in the OCR Foundation audit (project doc claude/ocr-foundation-topic-audit-2026-10-23.md). Three topics already have live games but no 6 P's bank: Venn diagrams (25 marks) with frequency trees and two-way tables (21), straight-line graphs (28), and constructions and loci (24), a total of 98 marks. Separately, the phone-fit gate measures games, not the 6 P's page, so nothing has measured it. Jon ruled on 26 Oct 2026 that these three topics come first, alongside the pie-chart bank.

CLASS CHECK: Not a bug. This follows the existing pattern: banks are generated from their source games by gen-six-ps.py, never hand-copied. The measurement uses the shared measure-phone-fit.py driver: if it can't drive the 6 P's page generically, extend the driver rather than writing a one-off script.

EXACT CHANGE:
1. For each source game, report its question types and counts, and which are Foundation content. Exclude Higher-only content (conditional probability; perpendicular lines). List any item using set notation (∩, ∪, ′) separately for Project Claude to check, rather than deciding.
2. Bank only items whose answer fits the 6 P's existing answer formats. For constructions, report which items can't be banked (for example, drawing tasks) and why. Don't add a new answer format.
3. Topic slugs: venn-two-way, straight-line-graphs, constructions-loci. At least 30 questions each, with worked lines and slip lines following the existing templates, and every diagram through the diagram check.
4. Regenerate. gen-six-ps.py --check passes on all 35 banks. Republish the review sheet to the same artifact URL.
5. Only after the cloud lane's measure-phone-fit.py change has merged: add the 6 P's page to the gate's roster. Measure the topic picker, a question screen of each answer format, and the feedback screen with worked lines, at the three phone sizes in both modes, and at 1366 × 768 and 1280 × 720 in report mode. If the page fails, record it on the known-failures list and report.
6. Merge once CI is green, and write the handover. Then stop: Jon will send the next contract.

DO NOT TOUCH: The three source games. The questions in the existing 32 banks. Distinctly Average, theme.css and the .maffs-ref component. measure-phone-fit.py's rules (driver changes to reach the 6 P's page are allowed). Canon.

SUCCESS CONDITION: 35 banks, the three new ones with at least 30 Foundation questions each. The diagram check reports 0 faults, gen-six-ps.py --check passes, and the review sheet is republished. The 6 P's page is on the gate's roster and measured, with results in the handover. Main is green.

STOP IF: Any source yields fewer than 30 bankable Foundation questions (report the counts; Project Claude writes the rest). A new answer format would be needed. The cloud lane's measure-phone-fit.py change hasn't merged when you reach step 5: finish steps 1–4, merge, and stop with step 5 outstanding.

## Notes from the home lane (26 Oct)
- Start from a new worktree off origin/main; gen-six-ps.py, scripts/check-changed.py (a workflow-file change selects everything, about 80 minutes), merge with merge-pr.py, never `git add -A` with .claude/pr.json in the tree (write PR JSON to the scratchpad).
- Banks are 32 now; the pie-chart bank is a separate contract, so "35 banks" assumes it lands first or the count is 35 including pie-chart: check the count before claiming it.
