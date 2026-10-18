CONTRACT: LOCAL-FLAKES (Project Claude for Jon, 18 Oct 2026, 13:30). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Find out why some checks fail on Jon's Windows machine but pass in
CI, prove the cause, and fix it at the cause, so check-changed.py is
trustworthy locally again.

ROOT CAUSE (to be proven; hypothesis below): Since 15 Oct, these have
failed in local check-changed.py runs on PRs that did not touch them,
and passed in CI every time: Answer lock part 1 (most runs), part 5
(once), part 6 (most runs); Quadratic Factoriser self-test (twice);
Level resolver part 1 (once); Estimation Engine (once);
test-escape-rating ("0 ratings" on two rooms, once). Each recent PR has
been pushed on CI's word over a red local run, which wears down the
pre-push rule. Hypothesis: scripts/check-answer-lock.py (and possibly
others) synchronise by fixed sleeps (page.wait_for_timeout(25), (300),
(500), int(1000 * TIME_SCALE), :519-749) instead of waiting for a page
state, and a loaded Windows machine runs slower than those sleeps allow.

CLASS CHECK: Probably a class: the same failure shape across several
browser checks points to how the checks wait, not to any one game. If
proven, the fix is in the test harnesses (how they wait), applied to
every check that waits the same way, not a longer sleep in one place.
If the cause is something else (a Windows path, encoding or port issue,
a shared fixture), the fix goes wherever that cause is.

EXACT CHANGE:
1. Reproduce: on this machine, run each check named above 10 times on
   unchanged main (sequentially, and once under the parallel load
   check-changed.py creates). Record pass/fail counts and the exact
   failure output for each.
2. Diagnose: for each failing check, find the line that fails and why,
   with evidence (the state the page was in, the timing, the error).
   Test the hypothesis directly: does the failure disappear when the
   machine is idle, or when the specific sleep is lengthened in a
   scratch copy? Write the findings to
   docs/audits/local-flakes-2026-10.md, one section per check.
3. Fix at the cause, only where the cause is in a test harness:
   replace a fixed sleep with a wait for the condition it was waiting
   for (an element, a state, a MaffsLock event), across every check
   that uses the same pattern. Never fix by lengthening a sleep.
4. Prove it: rerun the same 10x set locally, sequential and under
   load; every check named above passes 10/10. CI green.
5. If any cause is NOT in a test harness (game code, a shared runtime
   module, a real race in the product): do not fix it here. Report it
   in the findings doc with evidence; it gets its own contract.
6. python scripts/check-changed.py before opening the PR (it should now
   pass locally; say if it does not). Merge on green with main green;
   watch main's run; remove the worktree with scripts/end-task.py.
7. Handover in docs/handover/home.md: the causes found, what was fixed,
   the before and after pass rates, anything handed on.

DO NOT TOUCH: any game file; schools/assets/ (shared runtime); what
any check tests (its assertions stay the same; only how it waits may
change); CI workflow timeouts; the cloud lane's handover.

SUCCESS CONDITION: The findings doc names a proven cause for every
check listed, with evidence. Every harness-side cause is fixed by
waiting for a condition, not for a time. All listed checks pass 10/10
locally, sequential and under load. A full local check-changed.py run
on main passes. CI green; merged; worktree removed; handover recorded.

STOP IF: Main's latest full run is red. A cause is in game code or
schools/assets/ (report it; do not fix). A fix would change what a
check asserts. A check can't be made reliable without lengthening a
sleep (report why). The failures can't be reproduced in 10 runs
(report the counts; do not change anything).

END OF CONTRACT
