# Contract GS-L4-5-ENDPOINT (Project Claude for Jon, 16 Oct 2026, 07:50), verbatim

CONTRACT: GS-L4-5-ENDPOINT (Project Claude for Jon, 16 Oct 2026, 07:50).
CLOUD LANE. Fresh session. Save verbatim under docs/handover/contracts/
in the claim commit.

TASK: Make graph-sketcher L4_5's turning-point question have exactly one
correct answer, and make the game's verifier fail on any extremum
question whose keyed point is tied or beaten by an endpoint of its range.

ROOT CAUSE: L4_5 (games/graph-sketcher/index.html :534-540) asks "Write
down the coordinates of maximum deflection." for y = x^3 - 6x^2 + 9x,
xRange [0, 4]. The key is (1, 4), the local maximum, but y(4) = 4, so
the endpoint (4, 4) is an equal maximum and a correct answer marked
wrong (finding graph-sketcher-s1-006, HIGH). The Part 2 #14 wording
("the turning point") was rightly not applied: there are two turning
points, (1, 4) and (3, 0).

CLASS CHECK: Yes, within this game. Every 'tp' question that asks for a
maximum or minimum on a closed range can tie with or lose to an
endpoint, and nothing checks for it. The fix is the verifier
(scripts/verify-graph-sketcher.py or the game's existing verifier),
which must evaluate fn at both ends of xRange for every 'tp' question
and fail if an endpoint equals or beats the key in the direction the
prompt asks, unless the prompt says "local". Then fix L4_5. Not shared
code: the check sits in this game's own verifier.

JON'S RULING (16 Oct): L4_5's tp prompt becomes "Write down the
coordinates of the local maximum." Key unchanged, (1, 4).

EXACT CHANGE:
0. STANDING RULE (Jon, 16 Oct): add to docs/handover/cloud.md, beside
   the Standing authorisation, verbatim:
   "Holds and self-scheduled tasks (Jon, 16 Oct 2026): a hold the cloud
   lane states on a PR is released only by Jon. Stating a hold cancels,
   or rewrites to report-only, any pending task this lane scheduled for
   that PR. A task this lane schedules for itself carries no authority
   beyond the standing rules at the time it fires, and its report names
   it as the lane's own follow-up, not a request. Self-scheduled tasks
   may read CI status and report; they never merge, push or edit while
   a hold stands."
   Note in the entry that canon §7.8 records it via the home lane.
1. Add the endpoint check to graph-sketcher's verifier, as in CLASS
   CHECK. Prove it: plant a tie (scratch copy) and see it fail; revert.
2. Run the new check over every 'tp' question in the game BEFORE fixing
   L4_5. List each hit in the PR description: id, prompt, key, the
   endpoint values.
3. Apply Jon's ruling to L4_5. Close graph-sketcher-s1-006 citing this
   PR.
4. Any OTHER hit from step 2: do not fix. Report it to Jon in the
   session with the numbers and a proposed wording, and record it in
   the handover. (L4_5 is the only ruled one.)
5. Reworded item moves its content id: update data/check-ledger.json as
   CI's Tier 4 layer A directs. Never hand-edit ids.
6. python scripts/check-changed.py BEFORE the first push.
7. One PR; merge on a green Gate with main green (standing
   authorisation). Watch main's full run on the merge.
8. Handover entry in docs/handover/cloud.md: the rule from step 0, the
   check, the step 2 list, PR number, main's run.

DO NOT TOUCH:
- Any item in graph-sketcher other than L4_5's tp prompt.
- graph-sketcher-s1-009, -010, -011 (open, separate).
- L4_5's function, range, table, given values or key.
- Shared code (schools/assets/), shared scripts/, the workflow, canon,
  CLAUDE.md, docs/todo.md.
- glorious-gantt.

SUCCESS CONDITION:
- L4_5 has exactly one correct answer: (1, 4).
- The verifier fails on a planted endpoint tie and passes on main after
  the fix.
- Every 'tp' question in the game has been checked and listed; any other
  hit has been reported to Jon, not fixed.
- The step 0 rule is in cloud.md.
- PR merged; main's full run green; handover recorded.

STOP IF:
- Main's latest full run is red.
- The endpoint check needs a change to a shared module or the workflow.
- Step 2 finds a hit on a Year 6, KS3, Essentials or GCSE item: report
  it at once before anything else.
- The ruled wording proves wrong on checking (report it; do not
  reword).
- You would schedule any task that merges, pushes or edits.

END OF CONTRACT
