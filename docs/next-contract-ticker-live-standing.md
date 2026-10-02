Status: READY, not started. Issued by Jon 28 Sep 2026, verbatim below. Filed as `docs/todo.md` 1.19,
a live false claim, and queued after Log Laws "Solve" only because Log Laws has a class date. Its
success condition reads the live site and the live database, so build it from home: web sessions
cannot reach maffsgames.co.uk or www.gstatic.com.

TASK: Make the portal ticker's HIGH SCORE, WEEKLY BEST and "best:" reflect the leaderboard as it is now, not as it was when each score was submitted.

ROOT CAUSE: submitScore() (schools/assets/firebase-leaderboard.js:336–363) computes highScore, weeklyBest and best against the leaderboard at the moment of submission and stores them in the recent_scores entry. The ticker (index.html:3575–3585) prints those stored flags indefinitely, so they go stale: a weekly best is guaranteed stale within 7 days, and any later higher score makes an older entry's badge and "best" wrong. Seen live 28 Sep: RAQ, Negative Number Line (Year 6), "WEEKLY BEST 10 · best: 28" scrolling beside RAQ's newer "HIGH SCORE 30". The leaderboards hub (leaderboards/index.html:336–389) already computes the same quantities live, correctly, with LOWER_IS_BETTER and MIXED_UNRELIABLE handling — so the logic exists twice, once frozen and once live.

CLASS CHECK: Yes, a bug class. (a) Derived state stored at write time and displayed later — the same shape as the hand-kept New/Updated badges rebuilt on 27 Sep. (b) "Best / weekly best for a game+level" is computed in two components by two different methods. Fix at the shared layer: one live function in firebase-leaderboard.js, used by both pages; the stored flags stop being written or read. Not a patch to the ticker alone.

EXACT CHANGE:
1. schools/assets/firebase-leaderboard.js: add MaffsLeaderboard.standing(slug, levelKey) → Promise<{allTimeBest, weekBest, direction, rankable}>, computed from leaderboards/<key> at call time, with a 7-day window from Date.now(). Move LOWER_IS_BETTER and MIXED_UNRELIABLE here from leaderboards/index.html, unchanged in content, as the single copy. For a MIXED_UNRELIABLE game, rankable is false. Cache per key for the page's lifetime.
2. submitScore(): stop writing highScore, weeklyBest and best into recent_scores. Add levelKey (the raw level, e.g. 'year6') to each new entry alongside the existing level label. Everything else in the entry, the leaderboard push and the pruning is unchanged.
3. index.html ticker: load firebase-leaderboard.js, or share its db instance — whichever keeps a single Firebase initialisation on the page; state which in the report. For each of the ≤ 20 entries, call standing() and derive at render time: HIGH SCORE if the entry equals allTimeBest (lower-is-better aware); else WEEKLY BEST if it is within the last 7 days and equals weekBest; "best: N" = allTimeBest when not HIGH SCORE. rankable false → no badge and no "best". Ignore any stored highScore/weeklyBest/best on old entries. For old entries without levelKey, map the label back through an inverted LEVEL_LABELS.
4. leaderboards/index.html: replace its own all-time and 7-day computation with standing() and the moved constants. Rendered output must be identical for every game.
5. docs/canon.md §9: record the rule — a status that depends on other records is computed at display time, never stored. CLAUDE.md Firebase section: one line pointing to it.

DO NOT TOUCH: The leaderboards/<key> data and its write path. Profanity filter, initials overlay, askInitials(). score-history.js. The LEADERBOARD_MODE_READY gates on estimation-golf and equatle. Any game file. Firebase security rules. Existing recent_scores entries in the database — no migration, no rewrite.

SUCCESS CONDITION: The live ticker shows no badge that contradicts another entry: scripted check against the live recent_scores snapshot (read-only) lists every entry with its recomputed badge and best, and the RAQ Negative Number Line 10 shows no badge and "best: 30" (or higher if beaten since). The leaderboards hub's rendered text is byte-identical before and after for every game (scripted diff, stub server with a fixed snapshot of leaderboards/). A lower-is-better fixture and a MIXED_UNRELIABLE fixture render correctly in both pages. Tiers 1+2 green; check-leaderboard-coverage.js green; network guard confirms no write to Firebase during any check. Merged and live; report states the Firebase-initialisation choice from step 3.

STOP IF: Any LEVEL_LABELS value maps to more than one level key, so old entries cannot be resolved unambiguously. The ticker cannot share or reuse one Firebase initialisation without changing firebase-leaderboard.js's init() contract for games. The hub's output changes for any game. Firebase security rules turn out to block the ticker's reads of leaderboards/. Any checker FAIL.

---

Context found 28 Sep 2026. This is not part of the contract; re-verify it before relying on it.

- **STOP IF 1 looks clear, but step 3's inversion needs a fallback.**
  - `LEVEL_LABELS` (`firebase-leaderboard.js:73`–`76`) has eight distinct values, so no label maps to
    two keys.
  - But `submitScore()` stores `LEVEL_LABELS[level] || level` as the label (`:297`). A level key
    missing from `LEVEL_LABELS` is therefore stored as its own label. Chart Interrogator, for
    example, submits `l4` (see `docs/todo.md` §2).
  - So an old entry whose label is not in the inverted map must be read as its own key. That keeps
    the mapping unambiguous unless some game submits a raw key equal to another key's label, such as
    a literal `'GCSE'`. Check that before building.
- **Overlap with §2 of `docs/todo.md`** (the held leaderboard-modes contract).
  - §2's first bullet records that the ticker's HIGH SCORE and "best:" use `score >= maxScore`, which
    crowns the worst round in a lower-is-better game.
  - A direction-aware `standing()` removes that from the ticker. The rest of §2 (lifting the
    `LEADERBOARD_MODE_READY` holds, scores that are not scores) stays with that contract.
