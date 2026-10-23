# Start-screen mount survey, 23 Oct 2026 (contract START-MOUNT)

Every live game directory on main (100, Regression Rumble's holding page excluded) was re-surveyed. The cloud lane's
22 Oct survey found `id="startScreen"` 43, `id="menu"` 38, `id="menuScreen"` 9, `class="screen"` 2 and 7 with nothing
recognisable; Take a Walk and How Many Parts? bring `menu` to 39 (the recount: 43 + 39 + 9 = 91 by id, 9 without).

`<div class="maffs-start-note" data-maffs-start-note></div>` was inserted by script as the last child of the container
below, one new line per game (96 lines added, 0 changed). `scripts/check-start-mount.py` holds the same table
(`CONTAINERS`) and plays each game to its first question in Chromium.

**Hand placement (5, under the contract's limit of 9):** `chart-interrogator` (`#selector`, after the Start button),
`the-perfect-prank` (`#scrBrief`, after the details block), `tax-theft` (`#diffScreen`, after the difficulty buttons),
`trig-wars` (`.briefing`, the mission-briefing overlay that opens the game; after its BEGIN button and the teacher line),
`prime-or-composite` (`#intro-box`: the game has no separate start screen, but the intro box is the one element that is
hidden when play begins; the mount sits at its foot, above the Start button, and `#intro-box` is itself marked for
removal in that page's comment).

**No start screen, left without a mount (4):** `52dle` and `equatle` (one puzzle open at load), `estimation-golf`
(calls `startGame()` at load; its level bar stays during play), `factor-theorem` (opens on a Learn / Practice / Test tab bar).

**Start controls the shared driver does not find** (explicit steps in `START_STEPS`): `six-sevens-bruv` (needs a grid
made first), `test-the-claim` (needs a mode and both pills chosen), `trig-worms` (the FIRE! button).

| Game | Start container |
| --- | --- |
| `angle-ace` | `#menu` |
| `bearing-blitz` | `#menu` |
| `better-value` | `#startScreen` |
| `binomial-blaster` | `#menu` |
| `boolean-blitz` | `#startScreen` |
| `characteristic-quest` | `#menu` |
| `chart-interrogator` | `#selector` |
| `circle-theorem-spotter` | `#menu` |
| `complex-converter` | `#menuScreen` |
| `component-crusher` | `#menuScreen` |
| `constructions-lab` | `#menu` |
| `coordinate-geometry-dash` | `#menu` |
| `core-maths-paper1` | `#startScreen` |
| `core-maths-paper2a` | `#startScreen` |
| `core-maths-paper2b` | `#startScreen` |
| `core-maths-paper2c` | `#startScreen` |
| `correlation-or-coincidence` | `#menu` |
| `curling-friction` | `#menu` |
| `decimal-detective` | `#startScreen` |
| `differentiation-duel` | `#startScreen` |
| `dimension-checker` | `#menu` |
| `distinctly-average` | `#startScreen` |
| `eigenvalue-extractor` | `#menu` |
| `eigenvector-engine` | `#menu` |
| `equation-builder` | `#startScreen` |
| `estimation-engine` | `#menu` |
| `expectation-station` | `#startScreen` |
| `expected-damage` | `#startScreen` |
| `factor-race` | `#startScreen` |
| `fermi-lab` | `#startScreen` |
| `force-resolver` | `#menu` |
| `formula-forge` | `#menu` |
| `formula-plug-in` | `#startScreen` |
| `formula-unlocked` | `#menu` |
| `four-quadrant-explorer` | `#startScreen` |
| `fraction-equivalence` | `#startScreen` |
| `free-daily-pizza` | `#menu` |
| `given-that` | `#startScreen` |
| `glorious-gantt` | `#menuScreen` |
| `gradient-hunter` | `#menuScreen` |
| `graph-sketcher` | `#menuScreen` |
| `graph-transformer` | `#menu` |
| `growth-and-decay` | `#menuScreen` |
| `higher-power` | `#menu` |
| `how-many-parts` | `#menu` |
| `index-laws` | `#startScreen` |
| `integration-duel` | `#startScreen` |
| `just-pythag-it-bruv` | `#menu` |
| `like-terms-collector` | `#startScreen` |
| `linear-equation-solver` | `#menu` |
| `log-laws` | `#startScreen` |
| `maths-court` | `#startScreen` |
| `matrix-crunch` | `#menu` |
| `modular-battle` | `#startScreen` |
| `moments-master` | `#menu` |
| `negative-number-line` | `#startScreen` |
| `new-shapes` | `#startScreen` |
| `normal-navigator` | `#menu` |
| `partial-fractions-duel` | `#menu` |
| `percentage-flip` | `#startScreen` |
| `prime-factorisation` | `#startScreen` |
| `prime-or-composite` | `#intro-box` |
| `prisoners-dilemma` | `#menu` |
| `probability-paradox` | `#menu` |
| `probability-pioneer` | `#startScreen` |
| `proof-builder` | `#menu` |
| `proportion-blaster` | `#menu` |
| `quadratic-factoriser` | `#startScreen` |
| `scale-factor-scaling` | `#menu` |
| `screening-room` | `#startScreen` |
| `sequence-solver` | `#menu` |
| `seven-bridges` | `#startScreen` |
| `shape-shifter` | `#startScreen` |
| `simultaneous-solver` | `#menu` |
| `six-sevens-bruv` | `#menu` |
| `split-it` | `#menuScreen` |
| `spot-the-error` | `#startScreen` |
| `spot-the-muppet` | `#startScreen` |
| `standard-form-blitz` | `#menu` |
| `stat-attack` | `#menuScreen` |
| `surd-simplifier` | `#menu` |
| `suvat` | `#startScreen` |
| `take-a-walk` | `#menu` |
| `tax-theft` | `#diffScreen` |
| `terrible-advice` | `#startScreen` |
| `test-the-claim` | `#menuScreen` |
| `the-perfect-prank` | `#scrBrief` |
| `think-of-a-number` | `#startScreen` |
| `trig-identity-duel` | `#menu` |
| `trig-wars` | `.briefing` |
| `trig-worms` | `#startScreen` |
| `truth-buster` | `#startScreen` |
| `truth-will-set-you-free` | `#startScreen` |
| `unit-converter` | `#menu` |
| `word-problem-decoder` | `#startScreen` |
| `wrong-on-the-internet` | `#startScreen` |
