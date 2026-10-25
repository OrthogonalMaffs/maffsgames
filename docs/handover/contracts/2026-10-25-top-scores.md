# Contract TOP-SCORES (Project Claude, 25 Oct 2026, Jon's rulings), verbatim

FROM PROJECT CLAUDE, 25 Oct 2026 (Jon's rulings). Two contracts, in this order. The other cloud session is finishing MAIN-WARN (ci-groups.py, the workflow): do not touch those files.

=== CONTRACT 1: TOP-SCORES ===
TASK: Replace the hand-rolled local "Top scores" panel in 11 games with one shared renderer, so every panel shows British dates and never lists a score of 0.

ROOT CAUSE: 11 games (differentiation-duel, percentage-flip, trig-worms, suvat, fraction-equivalence, modular-battle, prime-factorisation, integration-duel, quadratic-factoriser, factor-race, index-laws) each keep their own top-5 list in localStorage, stamped with new Date().toLocaleDateString() (no locale, so a US-set browser shows 10/25/2026) and saved after every game, including a score of 0. The shared schools/assets/score-history.js already records every game's scores with timestamps in 98 games; these panels duplicate it.

CLASS CHECK: Yes: the same copied snippet in 11 games. Fix the class once: a shared renderer in score-history.js, called by each game, and a CI check so no game hand-rolls the panel or formats a date without the British locale again.

EXACT CHANGE:
(a) schools/assets/score-history.js: add a renderer for a game's top scores (e.g. top(slug, level, n) and renderTop(el, slug, level, n)): reads the existing history, drops scores of 0 or less, sorts highest first, takes n (5), and shows each date as toLocaleDateString('en-GB') from the stored timestamp. "No scores yet" when the list is empty. Burst behaviour unchanged.
(b) Each of the 11 games: remove its own top-scores list (its *_scores localStorage write and render) and call the shared renderer in the same place, with the game's slug and level. Make sure each game records its score through score-history.js (most already do; add the call where missing). The game's own single personal-best key is unchanged.
(c) A check in CI: no page under games/ calls toLocaleDateString() or toLocaleString() without 'en-GB', and none writes its own *_scores top-scores list. Planted faults, each caught: a bare toLocaleDateString(); a zero score shown; a game's own scores list restored.
(d) Old per-game lists in students' browsers are simply no longer read (no migration, no deletion needed).

DO NOT TOUCH: Question data, marking, scoring, timers, levels and analytics in every game. Firebase leaderboards (firebase-leaderboard.js). The personal-best keys. theme.css. burst.js. Anything under the-6-ps/, schools/assets/six-ps/, data/six-ps/ or scripts/gen-six-ps.py.

SUCCESS CONDITION: All 11 games show the shared panel: British dates, no zero, highest five, at 1280 and 320 px. Each game's own verifier passes unchanged in what it checks. The new check passes with its plants caught. python scripts/gen-six-ps.py --check still passes (several of these games feed The 6 P's). Main green after merge. Work committed and handover written.

STOP IF: A game's panel shows something score-history.js does not record (a time, a per-level split it lacks) and the shared renderer would lose it. gen-six-ps.py --check changes. A verifier needs a change to what it checks, not just a selector. Any change reaches marking or scoring.

(Contract 2, LOOK-REDS-2, follows after TOP-SCORES merges: `docs/handover/contracts/2026-10-25-look-reds-2.md` once started.)

## Jon's ruling after the STOP (via Project Claude, 25 Oct 2026), verbatim

FROM PROJECT CLAUDE, 25 Oct 2026 (Jon's ruling):
0. First finish MAIN-WARN (the earlier session was closed): its commit b398457 is on claude/intelligent-bohr-mqmov7 with no PR. Run the pre-push check, open the PR, merge through merge-pr.py when its CI and the Gate are green, and confirm main's run and that ci-pack.json now carries "over-budget". Contract text: the commit message and the docstring paragraph it added; ask if anything is unclear.
1. TOP-SCORES: option 1. score-history.js record() also maintains a separate key, mfg_top_v1::<slug>::<level>, holding the best five scores with their timestamps, never a score of 0 or less (ties: keep the earlier one). renderTop reads that key; the last-10 history and the hub are unchanged. Students' existing all-time bests in the old per-game lists are not migrated.
2. Under (b): move every MaffsScoreHistory.record call outside the if (window.MaffsLeaderboard) check, so a device records its own scores whether or not Firebase loads (as Quadratic Factoriser already does).
3. Per-level panels for Percentage Flip, Fraction Snap, Prime Sprint and Factor Race: accepted.
4. Add plants for the new rules: a sixth-best score does not displace the top five; a 0 is never stored; a game records with Firebase blocked.
Carry on in your claude/top-scores worktree. LOOK-REDS-2 still waits until TOP-SCORES merges.
