# MERGE-PR-ROBUST (Jon, 17 Nov 2026), saved verbatim

TOOL: Claude Code (cloud lane). SIZE: medium (one shared Gate script and its self-test; no site pages). Recommended: Opus, high effort.
MERGE TIMING: one merge heading for main at a time. HEATWAVE-PACK (#804, home lane) is due to merge this morning; if it is in its Gate or merge when yours is green, wait for it to merge, rebase, then merge.

TASK: Make scripts/merge-pr.py survive GitHub's timing and transient errors, so a lane is never stopped by a 5xx, a PR head that has not caught up with a push, or a main run that has not registered yet.

ROOT CAUSE: Four refusals in 24 hours (16-17 Nov), none caused by a red Gate or red main:
1. gh_api() (scripts/merge-pr.py:86-93) raises Refused on ANY non-zero gh exit, including HTTP 5xx, and guard() (:196) lets that propagate, so one 502 ends the run even with --wait 3600. Seen on #797 (Gate wait) and three times on #805, each on run_jobs()'s GET actions/runs/43961875130/jobs?per_page=50&page=1 (a re-run main run of 92 jobs), while the identical request by hand succeeded 8/8. JOBS_PER_PAGE (:120) was already lowered from 100 to 50 on 27 Oct 2026 for the same symptom on a 71-job re-run.
2. Stale head: guard() reads the PR's head from GitHub; straight after a push GitHub still reports the old head, whose Gate had failed, so guard() judged it red and refused at once (#802: "the Gate on head c08a613 is failure", with the fixed commit already pushed).
3. NO RUN FOUND: merge_and_report() runs watch_main() with the same `wait` as the guard; with --watch and wait 0 (or a short wait), a fresh merge whose push runs have not registered returns "main 6e1f4e0: NO RUN FOUND", exit 1, although the merge succeeded and its runs appeared seconds later (#803).

CLASS CHECK: Architectural. gh_api() is the single function every path calls (guard, check_gate, main_runs, run_jobs, newest_merge, watch); the missing safety is there, so retries go there, not at call sites. The stale-head and registration gaps are in guard() and merge_and_report(), shared by both lanes and every merge. No call-site patches, no per-lane flags.

EXACT CHANGE:
First commit: the cloud close-outs owed (AGENTS.md rule): ANSWER-AUDIT-PILOT (#802, bbbab73; check-site 43950743520 success, phone-fit-full 43950743561 success) and SHAPE-SHIFTER-FLAKE (#805, e91dd5e via merge-pr.py, last line "main e91dd5e run 44025444710: GREEN", exit 0; check-site 44025444710 success, phone-fit-full 44025444701 success; three earlier refusals on the 502 above); note that main run 43961875130 was red only on the Shape Shifter flake and its one rerun passed. Move both contracts to docs/history/contracts/ if not already moved. Save this contract verbatim at docs/handover/contracts/2026-11-17-merge-pr-robust.md.
1. gh_api(): for GET only (idempotent), retry on HTTP 5xx (and gh's "Server Error"/connection-reset text) up to 4 attempts with backoff 5, 15, 45 s (sleep injectable for tests); PUT/POST are never retried. After the last attempt, raise a distinct Transient(Refused) subclass whose message names the status. 4xx is never retried.
2. run_jobs(): if a page still fails with Transient after gh_api's retries, retry that page at half the page size (50 → 25 → 13), then continue paging at the smaller size; only then propagate. Keep JOBS_PER_PAGE's comment, adding the 16-17 Nov evidence.
3. guard(): treat Transient from any read as "not finished" (waitable within --wait, logged as "waiting: GitHub <status> reading <what>"), never as red. With wait 0 it still refuses, naming the transient.
4. Stale head: new optional --head SHA. When given, guard() waits (within --wait) while the PR's head sha differs from it ("waiting: PR head <old7> has not caught up with <new7>"), and refuses if wait runs out. When omitted and the local checkout's current branch equals the PR's head ref, use `git rev-parse HEAD` as the expected head and say so in the first log line; otherwise behave as today. A red Gate on a head that is NOT the expected head is never judged; only the expected head's Gate counts.
5. merge_and_report(): after a successful merge with --watch, the post-merge watch waits at least REGISTER_GRACE_S = 180 s for main's run on the squash commit to appear, whatever --wait is (a fresh merge's runs always register within seconds to a minute); NO RUN FOUND only after both the grace and --wait have passed. The guard's own wait is unchanged.
6. Self-test (the script's existing Fake and cases()/watch_cases()): plants that must be caught, each with the old behaviour shown failing: a single 502 on run_jobs page 1 then success (merges); 502 on every attempt at 50 a page but success at 25 (merges); 502 forever (refuses with Transient named, after retries, nothing merged); a 502 on a PUT (never retried, refused); a 404 (never retried); PR head stale for two polls then caught up with --head (waits, then merges on the new head's green Gate); stale head with a red Gate on the OLD head (not refused for red; waits); stale head never catching up (refuses at deadline); post-merge run registering after 60 s with --wait 0 (GREEN, not NO RUN FOUND); no run after the grace (NO RUN FOUND). All existing cases still pass.
7. Docstring and AGENTS.md's merge-pr.py usage line: document --head, the retry policy, the registration grace. Lanes' usage: `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600` (unchanged; --head optional).
8. docs/todo.md: close any rows for MERGE-PR-5XX-RETRY / merge-pr timing if present. Cloud handover.

Merge this PR with THIS branch's scripts/merge-pr.py (the fixed one), as `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600`; that is the live test.

Run only the checks this contract names and the Gate: merge-pr.py --selftest. No optional all-game local runs.

DO NOT TOUCH: the Gate's rules (what counts as green: GATE name, JOB_OK, MAIN_EVENTS, the main-is-green rule, --override's requirements); the merge method (squash) and commit-title cleaning; CI workflow files; any game, pack or script other than merge-pr.py (and AGENTS.md's usage line); the home handover; HEATWAVE-PACK's branch.

SUCCESS CONDITION:
- merge-pr.py --selftest passes, every new plant caught and every old case unchanged.
- No path judges a red Gate or red main as green, and PUT/POST are never retried (state how checked).
- This PR merged on green by its own fixed script; report its last line and exit status, and main's check-site and phone-fit-full run IDs and results on the merge commit. Cloud handover documented.

STOP IF:
- A retry would re-send a PUT or POST.
- Any existing self-test case has to change its expected result.
- The 502 on run 43961875130's jobs reproduces at 13 a page (report it; do not lower further).
- The fixed script refuses its own merge for a reason this contract does not cover (report the line).
