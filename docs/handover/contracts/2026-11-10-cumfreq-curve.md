# CUMFREQ-CURVE — Project Claude, Tue 10 Nov 2026, 06:35. CLOUD lane (listed game). Todo row 1.17. Ruling: Jon, 06:27, option A (smooth monotone curve through the points).

Saved verbatim in the claim commit (cloud lane, 10 Nov 2026). Pasted by Jon, from Project Claude's file `claude/cumfreq-curve-contract-2026-11-10.md`. The preamble (Project Claude, 10 Nov, 13:20) and Project Claude's note answering the cloud lane's first report (10 Nov, 13:40) follow the contract, also verbatim.

Evidence (main c8ac737; line numbers re-checked on f079bf3 by the preamble):
- games/chart-interrogator/index.html:782–792 `cfCurve` (now :788): each class is one cubic Bezier with both control points at the class midpoint, level with its ends (c1 [mid, cf], c2 [mid, cf+f]), so the curve's gradient is 0 at every plotted point: a smoothed staircase.
- :613 sets the axis grey; :621 `ctx.strokeStyle='var(--accent)'`, which canvas ignores, so the curve stays grey. No other game assigns a CSS variable to a canvas colour (searched all games).
- Marking reads the same curve (cfTruth, :846ff. — now :855 — via cfXAt/cfAtX/cfBez) and also accepts the polygon's readings (`alt`, readingOk :841 — now :842). scripts/verify-chart-interrogator.py rebuilds the curve itself (:295) and recomputes every key.
- Exam boards: OCR mark schemes credit "smooth curve or straight line segments" ("condone polygon"); the smooth curve is what is taught.

```text
CUMFREQ-CURVE (Project Claude, 10 Nov 06:35)
LANE: cloud (Claude Code web) · TIER: Small–Medium · branch from current origin/main. Listed game: claim chart-interrogator in scripts/answer-lock-state.json in its own pushed commit first (cloud.md lane rule). No other lane running (check: no open PR from another lane; if one is open, STOP). Stop at a green Gate for Project Claude's review and Jon's look and "merge"; do not merge. Not a draft. Save this contract verbatim in docs/handover/contracts/ in the claim commit or the PR's first commit.

TASK: Chart Interrogator's cumulative frequency curve is one smooth, never-decreasing curve through every plotted point, drawn in the game's accent colour, with every key re-read off the new curve and verified independently.
ROOT CAUSE: cfCurve places both control points of each class's Bezier level with its ends, so the gradient is zero at every plotted point; drawCumFreq assigns 'var(--accent)' to a canvas strokeStyle, which canvas cannot resolve.
CLASS CHECK: Not a class. The curve has one definition (cfCurve), which both drawing and marking already read, so changing it there changes the picture and every key together: that is the architectural layer, and no caller needs a patch. The colour bug is in one game only (no other game assigns a CSS variable to a canvas colour).
EXACT CHANGE:
1. cfCurve: keep one cubic Bezier per class, with control points from a monotone cubic Hermite (Fritsch–Carlson) through the cumulative points (x = class boundaries, y = cumulative frequency): tangents m_i by Fritsch–Carlson, with m = 0 at a point next to a zero-frequency class; for a segment of width h, c1 = (x0 + h/3, y0 + m0·h/3), c2 = (x1 − h/3, y1 − m1·h/3). x(t) is then linear in t; keep cfBez/cfXAt/cfAtX working on the segments as now (adapt the solver only if needed, and say so). Comment the rule where the old comment stands.
2. drawCumFreq: the curve's colour read once from the computed style of --accent (getComputedStyle(document.documentElement).getPropertyValue('--accent')), with the current grey only as the fallback if it is empty.
3. scripts/verify-chart-interrogator.py: rebuild the curve with its own Fritsch–Carlson implementation in Python (never read cfCurve's output), check (a) every segment is non-decreasing in y and passes through its two cumulative points, (b) the curve has no zero gradient at an interior point unless an adjacent class has frequency 0, (c) every cumfreq key and tolerance recomputes from the new curve exactly as cfTruth does, (d) every named wrong answer is still outside its band. Plants: the old level-control-point rule must fail (b); a control point that makes a segment dip must fail (a).
4. Rerun verify-chart-drawings.py and verify-feedback-teaches-charts.py; if either pins the old curve, update the pin to the new rule and say so in the PR body.
5. Proof in the PR body: before/after screenshots of three cumfreq scenarios at 1366×768 and 375×667 (one with a zero-frequency class if any exists); a table of every cumfreq key, old → new (Q1, median, Q3, IQR, benchmark count), with the tolerance; verifier counts.
6. todo row 1.17: append the result; close to docs/history/todo-done.md if wholly fixed. Release the claim; close-out entry in docs/handover/cloud.md; /updates/ line for Jon to confirm.
DO NOT TOUCH: stem-and-leaf, box plot and histogram code and data; the polygon readings (alt) and readingOk; tolerances' rules (capTol, the 2.5% bands); CUM_FREQ data; schools/assets/; any other game; Gate files and workflows; canon; docs/todo.md other than row 1.17; home.md.
SUCCESS CONDITION: the drawn curve passes through every point, never decreases, and has no flat spot at an interior point except beside a zero-frequency class; it is the accent colour; every cumfreq key is re-read off it and matches the verifier's independent rebuild; all named wrong answers stay outside their bands; Gate green; stopped for review and Jon's look.
STOP IF: any named wrong answer falls inside a band under the new curve (report the scenario and values; do not change tolerances); any key moves by more than its own tolerance (report the table first); the curve would dip or overshoot for any scenario (report it); a shared asset would need editing; another lane is running.
```

## Preamble (Project Claude, Tue 10 Nov 2026, 13:20)

```text
CUMFREQ-CURVE PREAMBLE (Project Claude, Tue 10 Nov 2026, 13:20) — do this first, then the CUMFREQ-CURVE contract below it.

TASK: Before CUMFREQ-CURVE's own work, close out #723 (CAST Away) and record Jon's standing rule on close-outs, so the cloud handover shows main's true state.
ROOT CAUSE: A PR cannot record its own merge: main's run on the merge commit exists only after the merge. #723's entry in docs/handover/cloud.md still says it is at the Gate and "to be merged", and its contract file is still in docs/handover/contracts/.
CLASS CHECK: A class. Every cloud merge has this gap (#721 needed #722 to close it). The fix is at the process layer: a standing rule that each cloud task's first commit closes out the lane's merged PRs, instead of one close-out PR per merge. This preamble is the rule's first use.
EXACT CHANGE:
1. Check first: origin/main has 39df31b with only the bot's "[skip ci]" record commits after it (2a9d4bb, ca33d62, f079bf3 when this was written), and main's runs on 39df31b are green: check-site 42809397904 (92 of 92 jobs) and phone-fit-full 42809397779. Report what you checked and how; if you cannot read the runs yourself, say so and rely on the IDs and results given here.
2. In docs/handover/cloud.md's standing rules, straight after the merge-route ruling, record verbatim:
   > STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
   > A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.
3. Close out #723 in the same commit as step 2. Order: the chart-interrogator claim commit stays its own pushed commit first (lane rule); this commit comes straight after it.
   a. git mv docs/handover/contracts/2026-11-09-cast-away-build.md docs/history/contracts/
   b. In the CAST-AWAY-BUILD entry of docs/handover/cloud.md: the heading's contract path becomes docs/history/contracts/2026-11-09-cast-away-build.md; "At the Gate, approved by Project Claude, holding for Jon's look and "merge" (contract: do not merge):" becomes "DONE, merged and live (unlisted):"; "Merge route: to be merged via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: …)" becomes "Merged as 39df31b via the GitHub connection under the standing ruling of 10 Nov 2026 (gh auth failed: …, the output as already recorded); main runs 42809397904 (check-site, 92 of 92 jobs) and 42809397779 (phone-fit-full) green."; the sentence beginning "Next: the Gate, review, Jon's look" becomes "Next: Jon lists it after his look (played 10 Nov; listing waits on his word)."
   c. List this close-out in the CUMFREQ-CURVE PR body.
4. Then CUMFREQ-CURVE as written. Its evidence was taken on c8ac737; re-find the line numbers on current main (on f079bf3: strokeStyle :621, cfCurve :788, readingOk :842, cfTruth :855) and report any difference beyond the line numbers.
DO NOT TOUCH: games/cast-away/ and its registry/listing (Jon lists it after his look); docs/todo.md (CLOUD-MERGE-TOKEN and the other new rows come in the home lane's docs PR); AGENTS.md (the home lane records the rule); the merge-route ruling's text; archived handover bodies; everything the CUMFREQ-CURVE contract excludes.
SUCCESS CONDITION: the CAST Away contract is in docs/history/contracts/; its cloud.md entry says merged as 39df31b with both runs green and listing waiting on Jon; the close-out rule stands verbatim in cloud.md's standing rules; CUMFREQ-CURVE then proceeds and its PR body lists the close-out.
STOP IF: main's runs on 39df31b are not green; anything other than the bot's "[skip ci]" record commits has landed on main since 39df31b; another lane has an open PR; the CAST Away contract file is not at docs/handover/contracts/2026-11-09-cast-away-build.md; cloud.md would exceed its size limit with nothing archivable.
```

## Note from Project Claude (10 Nov, 13:40), answering the cloud lane's report

```text
- Todo row 1.17 is "waiting on Jon" for the ruling below: Jon ruled at 06:27 on 10 Nov, option A (smooth monotone curve through the points). Step 6 updates the row.
- docs/next-contract-chart-interrogator-cumfreq.md (DONE 28 Sep) is earlier work; this contract supersedes nothing in it except the curve rule and the colour. Read it for context only.
- The claim lists one game: chart-interrogator. The contract names no other.
- Your step-1 checks are accepted as reported (92 jobs counted from the run total, not job by job: fine).
```
