TIER3-LOCK-FIX (Project Claude, Tue 24 Nov 2026 20:05; checked against main 855fce7)
From TIER3-COVERAGE-REPORT (#895, docs/audits/tier3-coverage-2026-11.md, home lane, 24 Nov 2026): tier 3 fully plays 10 of 116 games; 39 more play fully once MaffsLock's 300 ms fresh window is taken out of the driver's way.
RECOMMENDED: Opus 5.5, effort high. A change to the site's play-through checker that will make it play about four times as many questions in CI.
LANE: home. SEND: now (Jon is at his PC; the cloud lane is on BASE-60-LOOK, which touches only games/its-just-base-60-bruv/ and its verifier, so no shared files). One PR. Branch from current origin/main. No draft PR.

TASK: Tier 3 plays the games it currently skips only because of the answer lock, by running with MaffsLock.FRESH_MS set to 0 as every game verifier already does.

ROOT CAUSE: Shown in docs/audits/tier3-coverage-2026-11.md ("Mechanism, from the code"): after question 1, next_ready() returns as soon as the next question's options appear and the driver taps at once; schools/assets/answer-lock.js drops every click for 300 ms after fresh() (FRESH_MS, answer-lock.js:74), the driver's synthetic click included, so question 2 is never marked and undrivable() records UNSUPPORTED. Tier 3 never reads MaffsLock. Shown by the report's control run: with FRESH_MS set to 0 by an init script, the same 43 games play exactly as when each tap waits the window out (39 fully, 4 at some levels; 132 of 137 runs pass, against 129 with the wait), and 0 runs FAIL.

CLASS CHECK: A bug class in shared infrastructure: one driver (scripts/check-site.py tier3()) used for every game, and the same shape in 43 games. The fix is in the driver, once, not in any game. scripts/bank_common.py's NO_LOCK_FRESH_INIT is already the one way the repo's checkers take the window away (about ten verify-*.py scripts use it, e.g. verify-formula-unlocked.py:352, verify-its-just-base-60-bruv.py:361). The lock itself stays tested where it belongs: scripts/check-answer-lock.py, which this contract does not touch.

EXACT CHANGE:
0. First commit: save this contract verbatim as docs/handover/contracts/2026-11-24-tier3-lock-fix.md, and move docs/handover/contracts/2026-11-24-tier3-coverage-report.md (home's, merged as #895) to docs/history/contracts/ with its close-out in docs/handover/home.md (merge commit and main's run IDs, read back from the API).
1. scripts/check-site.py, tier3() (around line 2870, where each context adds TIER3_INIT and bc.KATEX_HOOK_INIT): add await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT), with a two-line comment naming this contract and the report. Only tier3()'s contexts: not tier 1 (around line 1574), not the phone contexts (around line 1840), not tier3_katex_selftest_async (around line 2967).
2. scripts/checker-allowlist.json: remove quadratic-factoriser from tier3_exceptions (shown in the report: it now passes both runs; the entry describes the game before its rebuild).
3. A regression check in tier 3's existing self-test, or, if tier 3 has no self-test that serves planted pages, in the smallest new --selftest the file's structure allows (say which in the PR): one planted four-option page that loads answer-lock.js and shows question 2 the instant question 1 is marked. Tier 3 must play all its questions. Plant that must fail: the same page with the NO_LOCK_FRESH_INIT line removed comes back UNSUPPORTED (the self-test must detect that the planted page was not played).
4. Run tier 3 locally exactly as CI does (python scripts/check-site.py --tier 3 --workers 4 --shard i/4, i = 1..4) before and after, and put in the PR a table per shard: PASS / UNSUPPORTED / FAIL runs, questions played, wall time. Name every game that moved from UNSUPPORTED to PASS (expected: the report's 39, plus quadratic-factoriser).
5. docs/audits/tier3-coverage-2026-11.md: one dated line at the top: "Fixed by TIER3-LOCK-FIX (24 Nov 2026): tier 3 runs with FRESH_MS 0; N games now play fully" with N from point 4. docs/handover/home.md entry (home.md under its size limit). Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line.

DO NOT TOUCH:
- schools/assets/answer-lock.js and its FRESH_MS value; scripts/check-answer-lock.py.
- Any game page; tier 1, tier 2, the phone contexts and the KaTeX self-test in check-site.py; next_ready(), undrivable() and the rest of the driver.
- Gate files (the workflow and its step and job timeouts, scripts/ci-*, ci_shards.py, merge-pr.py, check-context-size.py, check-changed.py): cloud's. Report any change they need; do not make it.
- tier3_exceptions entries other than quadratic-factoriser.
- games/its-just-base-60-bruv/ and scripts/verify-its-just-base-60-bruv.py (the cloud lane's BASE-60-LOOK).

SUCCESS CONDITION:
- Locally and in CI, tier 3 plays fully at least the report's 39 games plus quadratic-factoriser, with 0 FAIL; the per-shard table is in the PR.
- The regression check passes and its plant is caught.
- The Gate is green; merged through merge-pr.py; its last line reported; home.md records this task and #895's close-out.

STOP IF:
- Any run comes back FAIL, or tier 3's KaTeX check reports an error on a page it now reaches. That is a fault in a live game, newly visible: stop before merging, report the game, level, question and verbatim reason, and do not fix the game or add an exception.
- Any shard's local wall time exceeds 10 minutes (the CI step timeout is 12): stop and report the timings; the workflow is cloud's.
- Fewer than 39 games move to PASS: report which of the report's games did not, and why.
- merge-pr.py cannot reach GitHub, or refuses: report its output, do not merge another way.
