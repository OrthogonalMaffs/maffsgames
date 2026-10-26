# Contract PHONE-FIT-DRIVER (Jon, 26 Oct 2026), verbatim, with Jon's correction to item 1

TASK: Make the phone-fit measurement see what students see (the question screen as well as the start screen, after any timed banner), re-measure, and give Jon the facts he needs to rule on the question-taller-than-the-screen group: report and measurement only, no game fixes.

ROOT CAUSE: The below-fold audit (#556, docs/audits/below-fold-2026-10-26.md) found two measurement gaps. (1) For 9 games, the driver measured the start screen and never reached a question; of the 4 where a question was reached, 3 also fail there, so the true state of these games is unknown. (2) The Core Maths papers read as unmeasurable until their two-second banner was waited out, so any timed element can hide a failure. Separately, the 11 "question taller than the screen" games need Jon's ruling on canon §7.6.1's 1 Oct exception, and he needs its wording and the game list.

CLASS CHECK: Yes. Both gaps are in the shared driver (measure-phone-fit.py), so they affect every game it measures. Fix the driver generally: no per-game special cases, except where a game's start can't be driven generically (record those on the unmeasurable list with the reason).

EXACT CHANGE:
1. measure-phone-fit.py: for every game, measure the start screen AND the first question screen (driving the start screen generically: the first level or option, then Start). Both screens are judged: on the start screen, the level picker and Start button must sit above the fold; on the question screen, the existing rule applies.
2. Wait out timed elements generally: after each navigation, wait until the layout has been stable for 500 ms (up to a ceiling of 5 s) before measuring. Remove any Core Maths-specific wait if one was added.
3. Re-run the whole roster at the three phone sizes in both modes, and at 1366 × 768 and 1280 × 720 in report mode. Update the known-failures and unmeasurable lists so they match exactly (they may grow; that is expected and is the point).
4. Add to docs/audits/below-fold-2026-10-26.md:
   - the corrected per-game results for the 9 start-screen games and the Core Maths papers;
   - canon §7.6.1's 1 Oct exception, quoted word for word;
   - for each of the 11 question-taller-than-the-screen games: lowest tier served, the question types involved, how far over, and whether the question would fit with the options alongside at 375 × 667.
   Order everything with the resit-suite games first.
5. Selftest: add planted cases for a game whose start screen passes but whose question screen fails, and for a game with a 2 s banner.
6. Fill in the #556 handover entry (PR #556, squash 469d78d, main run 40394376362). Merge once CI is green, and write the handover. Then stop.

DO NOT TOUCH: Any game file, theme.css, or the .maffs-ref component. The phone-fit rules themselves (only what is measured, and when). Canon. The old claude/theme-distinctly-average branch.

SUCCESS CONDITION: Every measurable game is judged on both its start screen and its first question screen, after its layout settles. The lists match the new measurements exactly. The audit has the corrected results, the exception quoted, and the 11-game table. Both new selftest plants are caught. The gate exits 0 on main, the #556 entry is complete, and main is green.

STOP IF: More than 10 games can't be driven from the start screen to a question generically (report the list). Waiting for the layout to settle pushes a full roster run past 30 minutes. The new measurements change which group a game falls into for more than 5 games (report before updating the lists).

## Jon's correction to item 1 (26 Oct 2026), verbatim

The contradiction: item 1 adds a new rule (the level picker and Start must sit above the fold), but DO NOT TOUCH forbids changing the phone-fit rules. The lane would either break DO NOT TOUCH or stop on it. A rule is yours to rule on, not something to slip in through a measurement contract. So the start screen should be measured and reported, not judged by the gate yet.
Replace item 1 with:

1. measure-phone-fit.py: for every game, measure the start screen AND the first question screen (driving the start screen generically: the first level or option, then Start). The question screen is judged by the existing rule. The start screen is measured in report mode only (where the level picker and Start button end against the fold), with no pass or fail, until Jon rules on a start-screen rule.

Everything else stands as written. If you've already sent the original to the cloud lane, send it this instead:
Correction to item 1: measure the start screen in report mode only (where the level picker and Start end against the fold, with no pass or fail). Only the question screen is judged by the gate. A start-screen rule is Jon's to rule on, after the audit.
