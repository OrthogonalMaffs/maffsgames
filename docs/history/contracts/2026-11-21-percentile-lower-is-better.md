# Contract PERCENTILE-LOWER-IS-BETTER (Project Claude, 21 Nov 2026), verbatim, with its follow-up

PERCENTILE-LOWER-IS-BETTER. Home lane. From Project Claude, 21 Nov 2026 (todo row PERCENTILE-LOWER-IS-BETTER; Jon asked for home-lane work, 14:56).
Recommended: Claude Code, Sonnet, low-medium effort. One shared function and its one caller, with a Node test.

TASK: Make the percentile and certificate tier that submitScore() returns follow the same ranking rules as standing(): lower-is-better games ranked the right way round, and unrankable games given no percentile or tier.

ROOT CAUSE: schools/assets/firebase-leaderboard.js calculatePercentile(score, allScores) (:533-540) always counts scores below as worse (allScores[i] < score). For LOWER_IS_BETTER games (:203: estimation-golf, maffscards), the best score gets the worst percentile and no tier. Its one caller, submitScore()'s then-block (:498-499), also ignores MIXED_UNRELIABLE, which standing() (:575-576) honours with rankable:false. Latent: no page displays percentile or tier yet (searched main), but submitScore resolves them, so the first page to show one would show a wrong one.

CLASS CHECK: Architectural. The same ranking rules (direction, rankable) are applied in standing() and ignored in calculatePercentile(), the missing safety in shared code that two paths need. Put them in one helper both use, not a flag at the call site.

EXACT CHANGE:
1. First commit: the standing close-out for #861 (merge commit 84424d3, merge-pr.py, its main runs), per AGENTS.md.
2. firebase-leaderboard.js: add one helper, e.g. rankRules(gameSlug) -> { direction: 'higher'|'lower', rankable: bool }, from LOWER_IS_BETTER and MIXED_UNRELIABLE. standing() uses it instead of its own two lines (:575-576), with its behaviour unchanged. calculatePercentile(score, allScores, direction) counts worse scores the right way round: for 'lower', scores above are worse. submitScore() passes the direction, and returns percentile:null, tier:null (totalPlayers as now) when rankable is false.
3. Node test (new, e.g. scripts/test-percentile.js, wired into CI as the repo's other Node tests are): (a) higher-is-better: the best of [10, 20, 30] gets the top percentile and gold where the threshold allows; (b) lower-is-better: the best of [10, 20, 30] (10) gets the same; (c) the worst gets the bottom in both; (d) an unrankable slug gets null and null; (e) ties are counted exactly as now for higher-is-better. A planted fault (the direction argument ignored) must fail (b).
4. Merge on green via scripts/merge-pr.py, then the standing close-out.

DO NOT TOUCH: LOWER_IS_BETTER, MIXED_UNRELIABLE, GOLD_THRESHOLD and SILVER_THRESHOLD values. What is written to Firebase (leaderboard entries, recent_scores). standing()'s results. Any game page. site-nav.js and any back-link code (the cloud lane has a label fix in flight).

SUCCESS CONDITION: For estimation-golf and maffscards, the lowest score gets the top percentile. For an unrankable game, percentile and tier are null. standing() is unchanged in behaviour and both use the one helper. The Node test passes, and the planted fault fails. #861's close-out is on main. CI is green and the PR is merged.

STOP IF: Any page or script outside firebase-leaderboard.js reads percentile or tier (list it and stop). Tie handling would change for higher-is-better games. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).

## Follow-up (Project Claude, 21 Nov 2026), after the home lane stopped on the first STOP IF (scripts/check-burst.py:293)

PERCENTILE-LOWER-IS-BETTER, follow-up from Project Claude. Cleared: carry on from step 1 in ~/mg-percentile.

Thank you for stopping and for the thorough search. Verified on main ff244be: scripts/check-burst.py:293 reads res.get("percentile") only as a sentinel that submitScore() returned at once via reject() (firebase-leaderboard.js:224, percentile:null, fixed). The burst early-return (:436-437) precedes the then-block at :498-499 that this contract changes. So it isn't a reader of a calculated percentile, and this STOP IF doesn't apply to it.

Add one line to the PR body recording this. Don't change reject(), the burst early-return or check-burst.py. check-burst must pass unchanged. All other STOP IFs stand.
