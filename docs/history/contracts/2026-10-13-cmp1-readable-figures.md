CONTRACT FOR THE CLOUD LANE: CMP1-READABLE-FIGURES (Project Claude for Jon, 13 Oct 2026, 14:40). Recommended: Sonnet, medium effort (one game's chart drawing and its verifier).
Save this verbatim as docs/handover/contracts/2026-10-13-cmp1-readable-figures.md in the first claim commit.
======================================================================
TASK (cloud lane, CMP1-READABLE-FIGURES): Make every value a student must read from a figure in Core Maths Paper 1 sit on a labelled tick or a gridline (SR-32, Jon 13 Oct 2026), starting with the Q4 histogram, and make the game's verifier enforce it.

ROOT CAUSE: Jon play-tested the live game on 13 Oct. Q4 ("A histogram shows the distribution of waiting times at a clinic. How many patients waited between 10 and 40 minutes?") draws frequency-density bars at 2.4, 3.6 and 1.2, but the y-axis has gridlines only at 0, 1, 2 and 3. A student cannot read 3.6 from the scale. Reading 3.5 gives 59, which is not an option, so the student only reaches the key (60) by picking the nearest option. The item tests estimation, not the AO1 skill it is tagged with (§3.1). The key and distractors are right: 48 is the wrong bars, 72 the wrong width, 84 the total. The fault is in the figure.

CLASS CHECK: Yes, a bug class. Figure readability applies to every game that draws a chart. No rule or check covers it: SR-25 checks that the words, the figure and the key agree, not that a value can be read. The architectural layer has two parts. The ruling is SR-32, which the home lane records in canon. Enforcement is each game's verifier reading the drawn figure, as SR-25 established with verify-angle-ace.py. In this game the fix goes in the game's chart-drawing code, so every figure it draws is fixed, never item by item. Other games are the home lane's work. If the chart is drawn by a file in schools/assets/, STOP.

EXACT CHANGE (one PR, branch claude/cmp1-readable-figures, from origin/main):
1. Claim core-maths-paper-1 on `cloud-remaining:` in its own pushed commit. If the home lane or an in-flight SWEEP-1 batch has it, skip and report.
2. In games/core-maths-paper-1/index.html, the chart-drawing code: set the gridline step from the data. Use the largest step from {1, 0.5, 0.2, 0.1} × a power of 10 at which every plotted value the key depends on lies on a gridline. Draw faint minor gridlines at that step, and keep labels at the existing major steps, exam style (AQA prints 2 mm graph paper). Apply this to every chart type the game draws. For Q4 the result is minor gridlines every 0.2, with labels unchanged at 0, 1, 2 and 3.
3. Gridlines stay at least 4 px apart at 320 px width, and the labels stay legible. Check with screenshots at 320 px, 390 px and desktop width.
4. scripts/verify-core-maths-paper-1.py: in Chromium, for every item with a figure, read each plotted value the key depends on and assert that it lies on a drawn gridline or a labelled tick (within 0.5 px). Planted fault: a bar at 3.6 with gridlines only at whole numbers fails the run.
5. docs/audits/findings/core-maths-paper-1.yml: add an entry for Q4, marked fixed in this PR, citing SR-32 (Jon, 13 Oct 2026; canon entry pending in the home lane).
6. `python scripts/check-changed.py` before the first push. Merge on a green Gate with main's last run green. Watch main's run. Use scripts/end-task.py. Add a dated cloud.md entry and take the slug off `cloud-remaining:`.

DO NOT TOUCH: any item's stem, values, key or options; the scoring, timers and theme; schools/assets/; any other game; docs/canon.md (the home lane records SR-32); docs/handover/home.md.

SUCCESS CONDITION: On main, Q4 shows gridlines every 0.2 and each of the bars at 2.4, 3.6 and 1.2 meets a gridline. Every figure in the game passes the verifier's new check, and the planted fault fails it. Screenshots at 320 px show gridlines at least 4 px apart and legible labels. Main's full run is green.

STOP IF: the chart is drawn by a shared asset; a value lies on no gridline down to a 0.1 step of the axis's labelled unit (for example 3.65), because changing it is new content and Jon's call (quote the item); gridlines cannot stay 4 px apart at 320 px (report the item and the spacing); the game is claimed elsewhere.

(Slug note, added in the claim commit: the contract writes "core-maths-paper-1"; the game's directory, verifier and findings file are core-maths-paper1, so that is the slug claimed below.)
