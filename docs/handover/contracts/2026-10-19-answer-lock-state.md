CONTRACT: ANSWER-LOCK-STATE (Jon, 19 Oct 2026). CLOUD LANE. Saved verbatim.

TASK: Move the answer-lock "cloud-remaining" state out of docs/handover/cloud.md into a data file, so handover edits stop selecting all six answer-lock parts.

ROOT CAUSE: scripts/check-answer-lock.py reads a `cloud-remaining:` line from docs/handover/cloud.md (lines 17, 93), so the dependency map correctly lists that file as a dependency. Every cloud-lane PR edits its handover, so every cloud-lane PR runs answer-lock parts 1–6 (~20 min, the heaviest lines in the suite).

CLASS CHECK: Local: one script stores machine state in a prose document. The mapper is behaving correctly here. Fix the script. Also grep scripts/ for any other verifier reading docs/handover/ or docs/todo.md; if one exists, apply the same fix to it in this PR.

EXACT CHANGE: Create scripts/answer-lock-state.json holding the current cloud-remaining value. check-answer-lock.py reads that file instead, with the same "exactly one value" validation. Remove the machine-read line from cloud.md, leaving a one-line prose pointer to the JSON.

DO NOT TOUCH: answer-lock logic, its parts split, its report-not-fail behaviour, scripts/ci-deps.py, any other handover content.

SUCCESS CONDITION: `check-changed.py --list --files docs/handover/cloud.md` selects no answer-lock part; answer-lock passes in CI with identical results to the last main run; handover updated.

STOP IF: the cloud-remaining value is written by another script or process that would need changing too; answer-lock results differ from the last main run.

---

RULING (Jon, 19 Oct 2026, on the STOP IF report: the claim process writes and reads the line, and CLAUDE.md and canon §7.6 and §7.8.2 name it; options A, B, C):

A, please. Add canon SR-21 (line 83) to the rewrites; it also names the cloud-remaining: line in cloud.md. Before pushing, grep the repo for cloud-remaining and make sure nothing outside the JSON and its reader still describes it as a line in the handover. Agreed that claim commits should still select answer-lock: they change its result. Put run 39309543642 in this PR’s handover commit. Thank you.
