VERIFIER-SPLIT (Project Claude, Wed 25 Nov 2026 18:35; checked against main d4050ed)
Jon, 25 Nov 2026, 18:25: "happy for lane 2 to do it" (after ANNOUNCE-STRIP stopped on STOP IF 3: #915's Plan job failed, check-site run 45672202038, because verify-maffscards.py's median, 231 s, is over the per-line limit, 189 s, and #915's close-out commit selects it). Lane 1 is closed (Jon: no third lane).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. CI plumbing on four verifiers; nothing a student sees.
LANE: cloud, lane 2. SEND: now (lane 2 is stopped on ANNOUNCE-STRIP, waiting). This is a new task that comes first; ANNOUNCE-STRIP resumes after it, unchanged. The home lane is on SITE-BAR-PILOT (site-nav.js, site-bar.css, stage-exit.js, calculator.css, three game pages, check-site-nav.py, verify-stage-exit.py, docs/todo.md, canon §7.5.8): no shared files beyond docs/handover; merge main in before merging.
TIER: Medium (merge on green).

TASK: Run verify-maffscards.py as several CI parts, and make the four verifiers that read their own contract trigger only on that contract's file, so close-outs and MaffsCards PRs pass Plan.

ROOT CAUSE: Shown. (1) scripts/ci-timings.json:157: the MaffsCards game line's median is 231 s since #913 (76 s before), over the 189 s per-line limit; a line over the limit fails Plan on any PR that selects it (canon §7.8.1, LINE-LIMIT-SCOPE). It is one line (# ci-line, verify-maffscards.py:2), though the script already runs in named units (--only data balance rules marvin sim play challenge fit, :1335-1347, and the plants via --selftest). (2) Four verifiers list both whole contract folders in # ci-deps because each reads its own contract for verbatim text: verify-maffscards.py:3 (CONTRACT '2026-11-20-maffscards-game.md', :107), verify-i-dropped-my-ice-cream.py ('i-dropped-my-ice-cream.md', :76), verify-its-a-sine.py ('sine-not-sine.md', :79), verify-sums-in-disguise.py ('sums-in-disguise.md', :104). So every close-out (a contract file moving into docs/history/contracts/) runs all four, and any of them over the limit blocks every cloud close-out.

CLASS CHECK: Both are classes. (1) Splitting a long verifier is what the shared SHARD mechanism is for (scripts/ci_shards.py, # ci-shards, bc.Shard; e.g. verify-cast-away.py:2), so MaffsCards moves onto it rather than gaining a hand-made --part. (2) The over-wide trigger is the same in four verifiers, so all four are narrowed, not only MaffsCards. Out of scope, recorded only: a verifier can grow past the limit in its own PR and fail only the next PR (#913 passed at its old 76 s median); step 4 makes that a todo row for Project Claude to scope.

EXACT CHANGE:
0. First commit: save this contract verbatim as docs/handover/contracts/2026-11-25-verifier-split.md. (ANNOUNCE-STRIP's branch keeps its own close-out of LIKE-TERMS-PLUS; do not repeat it here.)
1. scripts/verify-maffscards.py onto SHARD: replace the # ci-line with a # ci-shards line (same label text, args, parts until timed 3), and in main() take the units from bc.Shard (bc.shard_args on the parser; shard.pick([...]) over the existing units, in run order: data, balance, rules, marvin, sim, play, challenge, fit, and the plants as a unit "selftest"; each unit run inside shard.unit(uid)). Without --shard a local run still runs every unit and the plants, as now; --only stays for local use. No check is changed, removed or weakened; every plant is still caught.
2. # ci-deps in the four verifiers: replace "docs/handover/contracts/ docs/history/contracts/" with that verifier's own contract file in both folders (e.g. "docs/handover/contracts/2026-11-20-maffscards-game.md docs/history/contracts/2026-11-20-maffscards-game.md"), using the CONTRACT names above. Confirm the planner accepts a ci-deps path that does not exist in one of the two folders; if it does not, STOP IF.
3. Prove it on the PR: the Plan job passes; the MaffsCards parts each run under the per-line limit; every unit runs in exactly one part (the shard log); verify-maffscards.py --selftest catches all sixteen plants. A dry selection (scripts/ci-groups.py's PR selection, or the planner's own dry mode) shows that a change touching only docs/history/contracts/<another contract>.md selects none of the four verifiers, and a change to games/maffscards/index.html selects the MaffsCards parts.
4. docs/todo.md: one new row VERIFIER-GROWTH: "A verifier that grows past the per-line limit passes its own PR (judged on its old median) and fails the next PR that selects it: #913 took verify-maffscards.py from 76 s to 231 s; #915 failed Plan (run 45672202038). Fixed for MaffsCards by VERIFIER-SPLIT; the gap remains. Owner: Project Claude (scope)." Nothing else in docs/todo.md.
5. docs/handover/cloud.md entry. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line and main's runs.
6. Then resume ANNOUNCE-STRIP on its branch: merge main into #915, re-run its Gate, and continue that contract unchanged (PR A, then PR B).

DO NOT TOUCH:
- What any of the four verifiers checks (no check, threshold or plant changed); their ci-line labels beyond MaffsCards' line becoming its ci-shards line.
- scripts/ci_shards.py, scripts/ci-groups.py, scripts/ci-timings.json, scripts/ci-pack.json (main's timings job writes these), .github/workflows/.
- Every game page, schools/assets/, canon, the roster; ANNOUNCE-STRIP's branch until step 6.

SUCCESS CONDITION:
- verify-maffscards.py runs as SHARD parts, each under the per-line limit, every unit once, sixteen plants caught; a local run without --shard is the full run.
- The four verifiers trigger on their own contract file only; a close-out of another contract selects none of them.
- Merged through merge-pr.py, last line reported; VERIFIER-GROWTH row added; #915 re-run green and ANNOUNCE-STRIP continuing.

STOP IF:
- The planner cannot take a ci-deps path that is missing in one folder: report how it reads ci-deps; do not change the planner.
- A MaffsCards unit alone is over the per-line limit (no split of whole units can fit): report the unit and its time.
- Any existing check fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
