# Contract PHONE-FIT-CHANGED-GAMES (Project Claude; Jon, 21 Nov 2026, 20:47; reissued 22 Nov 2026), verbatim

PHONE-FIT-CHANGED-GAMES. Cloud lane. From Project Claude; Jon approved, 21 Nov 2026, 20:47. Reissued 22 Nov 2026 against main 67ade5e, with the KNOWN_TOP gap #872's lane found.
Recommended: Claude Code, Opus, high effort. CI workflow selection, ci-deps classification and merge-pr's waiting logic; must not slow other PRs much.

TASK: Make phone-fit measure the games a change touches, on the pull request before it merges and on the push to main, not only when a shared path changes or overnight; and stop changes to known non-game folders counting as shared.

ROOT CAUSE: (1) .github/workflows/phone-fit-full.yml runs nightly (cron 23 2 * * *, :21-22), on a manual run (:25), and on a push to main only if the push changes a shared path (job "changed", :35-66, via ci-deps.is_shared; job "measure", :69). Nothing runs it on a pull request. So a change to one game alone (a new game, or a fix like #866, #868 or #870) is measured only by the next night's run, after it has merged: a Next pushed below the fold reaches students and turns main red the next morning. The home lane can't dispatch the workflow on a branch (its token gets 403), so it has been measuring locally by hand (#870). measure-phone-fit.py's --only takes one slug (:1343). (2) scripts/ci-deps.py's KNOWN_TOP (:54-55) is a hand-kept list. On main 67ade5e it lacks six tracked top-level folders: class, printables, ugh-stats, core-maths, tools, firebase. classify() (:389-396) calls a path in any of them "unknown", and is_shared() counts every non-"known" path as shared, so a change to /class/ or /printables/ starts the full phone-fit run. Each new folder (class, #872, 21 Nov) has added to the drift.

CLASS CHECK: Architectural, both. (1) The workflow's selection misses every game-only change the same way: fix the selection (measure the changed games), not by asking each contract to dispatch a run. (2) The same drift recurs with every new top-level folder: fix it at the list, with a self-test that fails when a tracked top-level folder is classified by nobody, not by adding `class` alone.

EXACT CHANGE:
1. First commit: the standing close-out for SIX-PS-BANKS batch 9 (#873, merged as 6310098; its merge-pr route and main's run IDs, check-site 44996163957 and phone-fit-full on 6310098), per AGENTS.md. In the same commit, cloud.md records the failed deletion of claude/ecstatic-thompson-f35dgo (#871, closed unmerged): the command, the exact error, and that the branch stays on origin at a2a254f with no further attempts. If this session holds an unpushed cloud.md note about it, commit that note as it is.
2. measure-phone-fit.py: --only accepts a comma-separated list of slugs (one slug works as now). The known-failures and other list rules apply per game as now; a listed game outside --only is never reported stale because it wasn't measured.
3. scripts/ci-deps.py:
   a. KNOWN_TOP gains class, printables, ugh-stats, core-maths, tools and firebase (each a known area; .github stays under ALL_PREFIXES). For each, say in the PR which verifiers still select on a change there (derivation or a ci-deps header), so nothing loses its check.
   b. --selftest: every top-level folder tracked by git (git ls-files) is in KNOWN_TOP or matched by ALL_PREFIXES, or the self-test fails and names it. Plant: a new tracked top-level folder in neither, caught.
   c. measured_pages(changed_paths) -> the set of phone-fit's measured games whose own files a change touches (games/<slug>/...). Phone-fit measures games only, so non-game pages (/class/, escape rooms, hubs) are out of scope here. Its own --selftest proofs: a game page change gives that slug; a docs change gives none; a /class/ change gives none and is not shared; a shared path is left to is_shared.
4. phone-fit-full.yml:
   - The "changed" job also outputs the changed measured games (via measured_pages).
   - On a push to main: a shared path -> measure everything, as now; otherwise, if games changed -> measure only those (--only with the list), in all three modes; otherwise skip, as now. Nightly and manual runs unchanged.
   - Add a pull_request trigger with the same selection against the PR's base. Its result shows on the PR.
5. merge-pr.py: when a phone-fit run exists for the PR's head, wait for it and refuse to merge if it failed, exactly as it treats check-site. When none ran (no game or shared path changed), it doesn't wait. Its self-test covers both, and the case of a run not yet started.
6. AGENTS.md: replace any instruction to dispatch phone-fit on a branch by hand, or to measure locally because it can't be dispatched, with one line: phone-fit runs on the PR by itself for the games it changes.
7. Test it on this PR: touch one game page in a throwaway commit (then revert it) and show the PR run measuring only that game in all three modes; show a docs-only change skipping it, and a /class/ change skipping it.
8. Merge on green via scripts/merge-pr.py, then the standing close-out (cloud.md short).

DO NOT TOUCH: What phone-fit measures and its pass/fail rules, the known-failures lists, NEXT_WAIT_MS. The nightly full run. check-site.yml and the Gate's budgets. The CI Plan job's selection rules beyond the KNOWN_TOP additions. Any game page (except the reverted test touch). games/complex-converter/, scripts/verify-complex-converter.py, docs/todo.md's WRONG-PAUSE-REASONS row and docs/handover/home.md (the home lane's COMPLEX-CONVERTER-WHY is in flight). The branch claude/ecstatic-thompson-f35dgo.

SUCCESS CONDITION: A PR that changes one game shows a phone-fit run that measures exactly that game in normal, Aa and laptop modes, and merge-pr.py won't merge it red. A push to main that changes one game measures it after merge too. Shared changes still measure everything; docs-only and /class/ changes measure nothing. The ci-deps self-test passes and its new plant is caught. CI is green, the PR is merged, and cloud.md records the #873 close-out and the branch-deletion failure.

STOP IF: A PR-triggered run needs secrets or permissions a pull_request run doesn't have. The changed-games measure would take more than about 10 minutes for a typical one-game PR. merge-pr.py's waiting logic can't tell "no run" from "run not started yet" reliably. Adding a folder to KNOWN_TOP would leave a change there selecting no verifier that reads it. The home lane's open PR would be blocked or re-measured in a way that breaks its merge. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).

## Amendment 1 (Jon, 22 Nov 2026, in this session, answering the step 7 question), verbatim

Neither alone: do options 3 and 2 together. No throwaway branches (we can't delete them; see this morning's failed deletion).
1. Before merging, run the "changed" job's exact Python locally against three diffs (a one-game touch, a docs-only change, a /class/ change) and show each result: the selected games and whether it's shared. Put the output in the PR.
2. Show merge-pr.py's self-test covering: a phone-fit run passed, failed, not yet started, and none expected.
3. Merge #875 on green via merge-pr.py, with step 7 recorded as "simulated locally; live proof pending".
4. The live proof goes in the close-out: the first real one-game PR, docs-only PR and /class/ PR after the merge, with each one's run ID and what it measured. If any selects wrongly, stop and report before the lane takes other work.
