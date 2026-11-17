# In-play exit gap, November 2026

Survey for contract CORE-PAPER-EXIT (Jon, 17 Nov 2026; 14:55: "listed only", no game changed), read on main fee6ad3, 17 Nov 2026. Todo row: `IN-PLAY-EXIT-GAP`.

**89 games have no in-play control back to the game's own start.** During play the only ways out are the portal link and the browser's Back button. The Core Maths papers had the same gap; they now carry the shared stage-exit shell's options (`data-game`, `data-leave`, `data-confirm="second-tap"`, `schools/assets/stage-exit.js`), which any game below can adopt.

## Method

Each page played in Chromium to its first question by `scripts/check-answer-lock.py`'s driver, every visible control listed, each exit-like control clicked in a fresh page to see whether it returned to the game's own start without leaving its URL; the nine the driver could not start, and every borderline result, checked by hand.

## The 89 games

- `angle-ace`
- `bearing-blitz`
- `better-value`
- `binomial-blaster`
- `boolean-blitz`
- `characteristic-quest`
- `chart-interrogator`
- `circle-theorem-spotter`
- `complex-converter`
- `component-crusher`
- `coordinate-geometry-dash`
- `correlation-or-coincidence`
- `curling-friction`
- `decimal-detective`
- `differentiation-duel`
- `dimension-checker`
- `distinctly-average`
- `eigenvalue-extractor`
- `eigenvector-engine`
- `equation-builder`
- `estimation-engine`
- `expectation-station`
- `expected-damage`
- `factor-race`
- `fermi-lab`
- `force-resolver`
- `formula-forge`
- `formula-plug-in`
- `formula-unlocked`
- `four-quadrant-explorer`
- `fraction-equivalence`
- `given-that`
- `glorious-gantt`
- `gradient-hunter`
- `graph-sketcher`
- `graph-transformer`
- `growth-and-decay`
- `higher-power`
- `how-many-parts`
- `index-laws`
- `integration-duel`
- `just-pythag-it-bruv`
- `like-terms-collector`
- `linear-equation-solver`
- `log-laws`
- `maths-court`
- `matrix-crunch`
- `modular-battle`
- `moments-master`
- `negative-number-line`
- `new-shapes`
- `normal-navigator`
- `partial-fractions-duel`
- `percentage-flip`
- `prime-factorisation`
- `prime-or-composite`
- `prisoners-dilemma`
- `probability-paradox`
- `probability-pioneer`
- `proof-builder`
- `proportion-blaster`
- `quadratic-factoriser`
- `scale-factor-scaling`
- `screening-room`
- `sequence-solver`
- `seven-bridges`
- `shape-shifter`
- `simultaneous-solver`
- `six-sevens-bruv`
- `split-it`
- `spot-the-error`
- `spot-the-muppet`
- `squared-squirrel`
- `standard-form-blitz`
- `stat-attack`
- `surd-simplifier`
- `suvat`
- `take-a-walk`
- `tax-theft`
- `terrible-advice`
- `test-the-claim`
- `think-of-a-number`
- `trig-identity-duel`
- `trig-worms`
- `truth-buster`
- `truth-will-set-you-free`
- `unit-converter`
- `word-problem-decoder`
- `wrong-on-the-internet`

## Notes

`how-many-parts`, `take-a-walk` and `squared-squirrel` are staged games without the shell; `graph-transformer`'s and `seven-bridges`' Reset restarts only the current puzzle; `word-problem-decoder`'s Topics is a filter overlay; `graph-sketcher` is unlisted.

## Not in the list, with reasons

`equatle`, `52dle` (one daily puzzle, not a run); `estimation-golf` (its level buttons stay on screen in play and restart the round); `factor-theorem` (Learn/Practice/Test tabs restart a run); `constructions-lab` ("← Back to Tasks"); `trig-wars` (VS CPU, 2 PLAYER and RESET in play; a battle, not a question run); `the-perfect-prank` (an escape room, not on the roster); `regression-rumble` (withdrawn holding page); the 11 stage-exit games and the 4 papers (they have the control).
