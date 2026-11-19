DD-VERIFIER-SHARD, one part.
LANE: home. Send now, to the same home session that holds #837 (it stopped correctly; this is route 1). TIER: Small. MODEL: Claude Code, Opus 5.5, medium effort.

TASK: Split scripts/verify-decimal-detective.py into work units (# ci-shards) in its own small PR, so it fits the per-line CI limit; then bring main into #837 and let its merge finish.

ROOT CAUSE: #837's Gate (check-site 44573475355, Plan job) fails on a time budget, not on #837's code: Decimal Detective's verifier is 177s median + 15s setup = 192s, 71% of its 270s budget against a 70% (189s) per-line limit, already over on main's timings (run 44566476211). It only fails when a change selects it, and next-control.js selects 136 verifiers. ci-shards is the mechanism the error message names (scripts/ci_shards.py, contract SHARD, canon 7.8.1).

CLASS CHECK: A class: any verifier still on fixed # ci-lines can grow past the per-line limit and turn the next PR that selects it red. Fix it at the existing architectural layer: move this verifier onto ci-shards (ci-groups.py then chooses its part count from timings on every repack). The rest of the class is reported, not fixed, in item 4.

EXACT CHANGE:
1. New branch and worktree from main (not #837's). Save this contract verbatim as docs/handover/contracts/2026-11-19-dd-verifier-shard.md.
2. scripts/verify-decimal-detective.py: replace its # ci-lines header with a "# ci-shards: <label> | <args> | 2" header and divide its work into named units with bc.shard_args / bc.Shard / shard.pick / shard.unit, exactly as the docstring of scripts/ci_shards.py shows and as the sharded verifiers already do (e.g. scripts/verify-bearing-blitz.py, verify-cast-away.py). Every check and plant it runs today still runs, each in exactly one unit; a full local run (no --shard) does everything it does now. --list-units works.
3. Check: python scripts/verify-decimal-detective.py (full) passes with its self-test; each of --shard 1/2 and 2/2 passes; their units together are the full set, none twice. ci-groups.py and the ci-deps selftest pass.
4. Report only: list verifiers still on # ci-lines whose median + setup is over 60% of their line budget in scripts/ci-timings.json (they are next to fail this way). In the PR body and home.md.
5. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, report its last line.
6. Then in #837's worktree: merge main into #837's branch (no rebase, no force-push), push, and run merge-pr.py on #837 as before. In #837's home.md entry, record both Gate failures (the ci-deps one, fixed by setAttribute in 5c09c245, and this budget stop) and this route.

DO NOT TOUCH: Decimal Detective's game page; what the verifier checks or how (units only regroup existing work); scripts/ci_shards.py, ci-groups.py, ci-deps.py and the workflow; scripts/ci-timings.json by hand (main's repack updates it); docs/handover/cloud.md; the cloud lane's open PR and its files.

SUCCESS CONDITION: the verifier runs as shards, full and sliced runs pass, nothing checked is lost; its PR merged GREEN; main merged into #837 and #837 merged GREEN by merge-pr.py; home.md records both PRs and both Gate failures; the report-only list given.

STOP IF: a check can't be placed in a unit without changing what it checks; the sharded verifier still breaks the per-line limit with 2 parts before timings exist (report the figures); merging main into #837 conflicts outside home.md, todo.md or updates/index.html; any other verifier selected by #837 also breaks a budget (report it; don't shard it here); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
