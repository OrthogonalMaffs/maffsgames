MERGE-GUARD (Project Claude, Fri 27 Nov 2026 18:10; checked against main b8ab511)
Jon, 27 Nov 2026, 17:57: "merge script please" (the guard owed since #930 merged on a Gate from before #927 landed, 26 Nov).
RECOMMENDED: Claude Code, Opus 5.5, effort high. The one merge route both lanes use; a wrong refusal or a wrong pass affects every PR.
LANE: home. SEND: now. First commit carries BASE-60-TIDY's close-out (AGENTS.md:62): #932 squash-merged as 60fb649. Record merge-pr.py's last line as the lane reported it if docs/handover/home.md holds it, else "not captured"; read main's check-site, phone-fit-full and pages runs on 60fb649 from GitHub Actions and record their IDs and results; move docs/handover/contracts/2026-11-26-base-60-tidy.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-merge-guard.md in the same commit.
TIER: Shared (stop at green for Project Claude's review and Jon's "merge").

TASK: Make scripts/merge-pr.py refuse a PR whose Gate or phone-fit run started before main's newest real merge, unless that merge is already in the PR's branch.

ROOT CAUSE (shown, file:line on b8ab511):
- AGENTS.md:58 says never merge on a Gate result older than main's newest checks: merge main into the branch and re-run the Gate. The tool does not enforce it.
- check_gate (scripts/merge-pr.py:181-193) asks only that the newest Gate check on the PR's head commit is a completed success; check_phone_fit (:196-211) the same for the phone-fit run. Neither asks what main held when the run started.
- A pull_request run tests the PR merged onto main as main stood when the run was triggered. A real PR merged to main after that is untested in combination. #930 merged this way on 26 Nov, on a Gate from before #927 (the large-screen layer) landed.
- GitHub's "require branches to be up to date" setting is the wrong tool: bots commit to main with [skip ci] several times a day (daily.json, answer counts, CI timings, REGISTER, handover archives), and it would force a re-run after each. merge-pr.py already tells those apart: newest_merge (:258-273) skips github-actions[bot] commits whose message has a skip marker.

CLASS CHECK: A class: both PR-side checks the guard trusts, (a) the Gate and (a') phone-fit, share the same missing safety, in the one shared merge route both lanes use. The fix goes in the guard, once, for both checks. Not in each lane's instructions.

EXACT CHANGE:
1. scripts/merge-pr.py, a new guard condition (a''), judged inside guard() (:333-388) with (a) and (a'), every poll:
   - M = newest_merge(api) (the newest commit on main that is not a bot skip-marker commit). If M cannot be read, (b') already refuses; (a'') adds nothing then.
   - If M is the PR's head or an ancestor of it (GET compare/M...<head sha>: status "ahead" or "identical"), (a'') passes: main's newest real merge is in the branch, so the runs tested it.
   - Otherwise, take the trigger time of each judged run: for the Gate, the check-site.yml pull_request workflow run on the head commit whose check_suite_id is the judged Gate check's check_suite id (its created_at; the Gate check's own started_at is the end of the run, never use it); for phone-fit, the judged run's created_at. M's time is its committer date (GitHub's squash merge writes the merge time there). If either run was created before M's time, (a'') fails: "main gained <M7> (<M's title, first 60 characters>) at <time> after this PR's <Gate|phone-fit run> started at <time>: merge main into the branch and let the checks re-run (AGENTS.md:58)".
   - (a'') is red, never "not finished": --wait does not wait on it (a stale run never freshens). --override never waives it, as (a) and (a') are not waived.
   - Bot skip-marker commits never trigger it, because M skips them.
2. The docstring's guard list (:15-38): add (a'') in the same register, with the #930 case as its reason, and say why GitHub's up-to-date setting is not used.
3. --selftest (:1229 onwards): fixture cases, each by the existing fixture style (:503-630):
   - pass: M an ancestor of head (main merged in);
   - pass: M not an ancestor, both runs created after M (the merge ref held it);
   - pass: only bot skip-marker commits on main since the runs started;
   - refuse: M not an ancestor and the Gate's run created before M, phone-fit after;
   - refuse: the same with phone-fit before and the Gate after;
   - refuse under --override and under --wait, immediately, with the message above.
   Plants, each must FAIL the selftest: the check removed; the Gate's started_at used in place of its run's created_at; bot skip-marker commits counted as M; the ancestor test inverted. All existing cases and plants unchanged and passing.
4. AGENTS.md:58: add one clause: "merge-pr.py enforces this (MERGE-GUARD, 27 Nov 2026)." docs/handover/home.md entry.

DO NOT TOUCH:
- (a), (a'), (b), (b'), (c), --watch, --watch-main, --head, the retry and Transient handling, the squash pinned to the judged head; the merge PUT itself.
- serve-stubbed.py and bank_common.py (the cloud lane's PINNED-LIVE-DATA is working there); docs/handover/cloud.md; every workflow; canon; the roster; docs/todo.md; every game.
- No force-push.

SUCCESS CONDITION:
- The selftest's new cases pass and its four plants are caught; every existing case passes; the Gate green on the PR.
- Against the live API, read only (no merge): run the guard's judgement on this PR itself and report (a'')'s verdict and the M it chose; if main gained a real merge after this PR's runs started, it must refuse, and you merge main in and re-run before stopping at green.
- At green: stop and report to Project Claude for review; merge only on Jon's "merge", through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 (main's current script judges this merge); report its last line; home.md records it.

STOP IF:
- GitHub's API gives no way to tie the Gate check to its workflow run (no check_suite id on either), or the compare API cannot answer for a squash-merged main: report what it does give; do not fall back to the Gate's started_at.
- Any existing selftest case changes result.
- An open PR in either lane would be refused by (a'') when you finish: list it in the report (that lane merges main in; not yours to fix).
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
