VERIFIER-SPLIT, AMENDMENT 1 (Project Claude, Wed 25 Nov 2026 19:20; the whole contract, reissued; checked against main d4050ed and #917)
AMENDMENT 1 (Jon's ruling on lane 2's stop of 19:09: option 1): the narrowed # ci-deps lines had no effect because the planner also reads each verifier's own string literals and turns any literal naming an existing folder into a dependency on the whole folder (scripts/ci-deps.py literal_paths, :192-225), except folders on its WIDE list (:63). All four verifiers spell 'docs/handover/contracts' and 'docs/history/contracts' as the folders they search. Fix at the planner: add both folders to WIDE (step 2b), so a literal naming them never becomes a dependency and the declared contract files are the trigger. Checked by Project Claude: the only other scripts naming those folders do so in docstrings (skipped by the planner: they contain spaces), or by a join down to the file (verify-simultaneous-solver.py:621, a file dependency, unaffected); check-context-size.py declares docs/handover/ in its own # ci-deps (declared, not inferred, so WIDE does not touch it). Merge #917 first as it is (its split already ends #915's Plan failure), then the WIDE change as its own PR. Accepted: its-a-sine's # ci-deps names both contracts it reads (sine-not-sine and its-a-sine-polish). Option 2 (spelling the paths so the planner cannot see them) is ruled out: it hides a real dependency.
Jon, 25 Nov 2026, 18:25: "happy for lane 2 to do it" (after ANNOUNCE-STRIP stopped on STOP IF 3: #915's Plan job failed, check-site run 45672202038, because verify-maffscards.py's median, 231 s, is over the per-line limit, 189 s, and #915's close-out commit selects it). Lane 1 is closed (Jon: no third lane).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. CI plumbing; nothing a student sees.
LANE: cloud, lane 2. SEND: now (lane 2 is stopped on #917, waiting). ANNOUNCE-STRIP resumes after this, unchanged. The home lane is on SITE-BAR-PILOT (#916): no shared files beyond docs/handover; merge main in before each merge.
TIER: Medium (merge on green). Two PRs: #917 (open), then PR 2 (WIDE).

TASK: Run verify-maffscards.py as several CI parts, and make the four verifiers that read their own contract trigger only on that contract's file, so close-outs and MaffsCards PRs pass Plan.

ROOT CAUSE: Shown. (1) scripts/ci-timings.json:157: the MaffsCards game line's median is 231 s since #913 (76 s before), over the 189 s per-line limit; a line over the limit fails Plan on any PR that selects it (canon §7.8.1, LINE-LIMIT-SCOPE). (2) Four verifiers read their own contract for verbatim text and depend on both whole contract folders, twice over: in # ci-deps, and through their own literals 'docs/handover/contracts' and 'docs/history/contracts', which ci-deps.py's literal_paths (:192-225) makes into folder dependencies because those folders are not in WIDE (:63). So every close-out runs all four.

CLASS CHECK: Both are classes. (1) Splitting a long verifier is what the shared SHARD mechanism is for (scripts/ci_shards.py, # ci-shards, bc.Shard). (2) The over-wide trigger is the same in four verifiers and comes from the shared planner's rule, so it is fixed in the planner (WIDE), plus correct declarations in the four; any future verifier that reads a contract then declares its file and nothing more. Out of scope, recorded only: a verifier can grow past the limit in its own PR and fail only the next (VERIFIER-GROWTH, step 4).

EXACT CHANGE:
0. First commit (done on #917): this contract's first version saved as docs/handover/contracts/2026-11-25-verifier-split.md. Now replace that file with this Amendment 1 verbatim, on #917.
1. Done on #917: scripts/verify-maffscards.py on SHARD (3 parts of 3 units each, every unit once, 16 plants caught; the plants' part about 160 s with setup). Keep as is.
2. Done on #917: # ci-deps in the four verifiers name their own contract file(s) in both folders (its-a-sine both of its contracts). Keep as is.
2a. Merge #917: merge main in, Gate green, python -X utf8 scripts/merge-pr.py 917 --watch --wait 3600; report its last line and main's runs.
2b. PR 2 (from main after #917): scripts/ci-deps.py: add "docs/handover/contracts" and "docs/history/contracts" to WIDE (:63), with a one-line comment: "contract folders: a verifier that reads a contract declares that file in # ci-deps (VERIFIER-SPLIT)". Nothing else in ci-deps.py. If ci-deps.py has a self-test or a test file, add one case: a verifier whose literal is 'docs/history/contracts' and whose # ci-deps names one contract file is selected by a change to that file and not by a change to another contract.
3. Prove it on PR 2: a dry selection shows that a change touching only docs/history/contracts/<another contract>.md (use like-terms-plus's) selects none of the four verifiers; a change to each verifier's own contract file selects that verifier; a change to games/maffscards/index.html selects the MaffsCards parts; verify-simultaneous-solver.py is still selected by a change to docs/history/contracts/2026-10-09-sim-s5.md; check-context-size.py is still selected by a change under docs/handover/. Report each selection.
4. Done on #917: the VERIFIER-GROWTH row in docs/todo.md. Keep as is.
5. docs/handover/cloud.md entries for both PRs. Merge PR 2 as 2a; report its last line.
6. Then resume ANNOUNCE-STRIP on its branch: merge main into #915, re-run its Gate, and continue that contract unchanged (PR A, then PR B).

DO NOT TOUCH:
- What any verifier checks (no check, threshold or plant changed).
- scripts/ci-deps.py beyond the WIDE entries, its comment and its test case; scripts/ci_shards.py, scripts/ci-groups.py, scripts/ci-timings.json, scripts/ci-pack.json (main's timings job writes these), .github/workflows/.
- The four verifiers' code (their literals stay as they are; option 2 is ruled out).
- Every game page, schools/assets/, canon, the roster; ANNOUNCE-STRIP's branch until step 6.

SUCCESS CONDITION:
- verify-maffscards.py runs as SHARD parts, each under the per-line limit, every unit once, sixteen plants caught.
- After PR 2: a close-out of another contract selects none of the four verifiers; each still runs on its own contract, its game and its own files; Simultaneous Solver and the context-size check select as before.
- Both PRs merged through merge-pr.py, last lines reported; #915 re-run green and ANNOUNCE-STRIP continuing.

STOP IF:
- Adding the folders to WIDE changes the selection of any script other than the four verifiers (step 3's dry runs, or a wider comparison of the full selection map before and after): report which and why; do not merge PR 2.
- A MaffsCards unit alone is over the per-line limit: report the unit and its time.
- Any existing check fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
