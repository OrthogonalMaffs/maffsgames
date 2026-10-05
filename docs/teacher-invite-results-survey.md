# Teacher feedback line to the results screen: survey and STOP (5 Oct 2026)

Jon's contract of 5 Oct 2026 (move `MaffsInvite`'s line from the start screen to the results screen). **Halted
before any edit:** two games have no results screen (STOP IF 1), and one of them (`trig-wars`) cannot get a results
container without changing how the game ends (STOP IF 2). Nothing in any game, the engine, `teacher-invite.js`,
`check-teacher-invite.py` or canon has changed.

## Counts

- 97 roster games surveyed (the numbered rows of `.claude/rules/game-roster.md`).
- **91 static:** a results container in the page's own markup, its end controls static; the mount point moves into
  it, directly after the last control row. The static check can hold these.
- **4 function route** (under the contract's limit of 10): `chart-interrogator`, `factor-theorem`,
  `prisoners-dilemma`, `log-laws`. Three of the four are there because they have **two end states**, and
  the contract's "one mount per page" plus "the line on every end state" means one mount point that the game moves
  into whichever results container it shows.
- **2 STOP:** `constructions-lab` (an open task menu, no end of game, no `game_completed`) and `trig-wars` (the game
  ends with "PLAYER n WINS" written into the play screen's turn bar; there is no results screen or container).
- Escape-room engine: `finish(win)` rebuilds `#endCard` by `innerHTML` for both victory and failure, so the engine
  mounts after its button row there: one function-route site, in `engine.js` only.

## Method

`BeautifulSoup` over each game's `index.html`: the current mount point's ancestors; every element whose id names a
results screen (`results`, `resultsScreen`, `gameOver`, `endScreen`, `summaryCard`, the result modals, ...); whether
JS assigns that container's `innerHTML` (directly, or via a variable bound to `getElementById`); and the static
buttons and links inside it. Then each special case was read by hand (the table's notes).

## Per game

| Game | Results container | Route |
|---|---|---|
| `sequence-solver` | `#results` | static |
| `estimation-golf` | `#summaryCard` (`#resultPanel` is per hole) | static |
| `estimation-engine` | the modal holding `#modal-result` | static, after `.modal-acts` |
| `factor-race` | `#gameOver` | static |
| `prime-factorisation` | `#gameOver` | static |
| `prime-or-composite` | the modal holding `#modal-result` | static, after `.modal-acts` |
| `percentage-flip` | `#gameOver` | static |
| `fraction-equivalence` | `#gameOver` | static |
| `equatle` | `#m-end` | static |
| `52dle` | the modal holding `#modal-result` | static, after `.modal-acts` |
| `constructions-lab` | **none** | STOP: no results screen (open task menu) |
| `split-it` | `#resultsScreen` | static |
| `word-problem-decoder` | `#resultsScreen` | static |
| `equation-builder` | `#resultsScreen` | static |
| `spot-the-error` | `#resultsScreen` | static |
| `gradient-hunter` | `#resultsScreen` | static |
| `truth-buster` | `#resultsScreen` | static |
| `spot-the-muppet` | `#resultsScreen` | static |
| `terrible-advice` | `#resultsScreen` | static |
| `wrong-on-the-internet` | `#resultsScreen` | static |
| `maths-court` | `#resultsScreen` | static |
| `expected-damage` | `#resultsScreen` | static |
| `negative-number-line` | `#resultsScreen` | static |
| `think-of-a-number` | `#resultsScreen` | static |
| `formula-plug-in` | `#resultsScreen` | static |
| `decimal-detective` | `#resultsScreen` | static |
| `four-quadrant-explorer` | `#resultsScreen` | static |
| `like-terms-collector` | `#resultsScreen` | static |
| `probability-pioneer` | `#resultsScreen` | static |
| `shape-shifter` | `#resultsScreen` | static |
| `new-shapes` | `#resultsScreen` | static |
| `higher-power` | `#results` | static |
| `prisoners-dilemma` | `#results`, `#tournamentResults` (controls inside rebuilt content) | function route (one point, moved), two end states |
| `seven-bridges` | `#resultsScreen` | static |
| `distinctly-average` | `#gameOver` | static |
| `index-laws` | `#gameOver` | static |
| `quadratic-factoriser` | `#gameOver` | static |
| `trig-wars` | **none** | STOP: game ends with "PLAYER n WINS" on the play screen's turn bar |
| `trig-worms` | `#gameOver` | static |
| `modular-battle` | `#gameOver` | static |
| `surd-simplifier` | `#results` | static |
| `proportion-blaster` | `#results` | static |
| `trig-identity-duel` | `#results` | static |
| `standard-form-blitz` | `#results` | static |
| `simultaneous-solver` | `#results` | static |
| `circle-theorem-spotter` | `#results` | static |
| `probability-paradox` | `#results` | static |
| `angle-ace` | `#results` | static |
| `coordinate-geometry-dash` | `#results` | static |
| `graph-transformer` | `#results` | static |
| `formula-unlocked` | `#results` | static |
| `bearing-blitz` | `#results` | static |
| `scale-factor-scaling` | `#results` | static |
| `unit-converter` | `#results` | static |
| `formula-forge` | `#results` | static |
| `correlation-or-coincidence` | `#results` | static |
| `chart-interrogator` | score bar built by `showScore()` in `#activeQuestion` | function route |
| `component-crusher` | `#resultsScreen` | static |
| `expectation-station` | `#resultsScreen` | static |
| `better-value` | `#resultsScreen` | static |
| `given-that` | `#resultsScreen` | static |
| `screening-room` | `#endScreen` | static |
| `linear-equation-solver` | `#results` | static |
| `core-maths-paper1` | `#resultsScreen` | static |
| `core-maths-paper2a` | `#resultsScreen` | static |
| `core-maths-paper2b` | `#resultsScreen` | static |
| `core-maths-paper2c` | `#resultsScreen` | static |
| `tax-theft` | `#completionScreen` | static, after `.completion-buttons` |
| `stat-attack` | `#resultsScreen` | static |
| `growth-and-decay` | `#resultsScreen` | static |
| `graph-sketcher` | `#resultsScreen` | static |
| `glorious-gantt` | `#resultsScreen` | static |
| `test-the-claim` | `#resultsScreen` | static |
| `differentiation-duel` | `#gameOver` | static |
| `integration-duel` | `#gameOver` | static |
| `suvat` | `#gameOver` | static |
| `curling-friction` | `#results` | static |
| `force-resolver` | `#results` | static |
| `moments-master` | `#results` | static |
| `log-laws` | `#gameOver`, `#solveOver` | function route (one point, moved), two end states |
| `binomial-blaster` | `#results` | static |
| `partial-fractions-duel` | `#results` | static |
| `proof-builder` | `#results` | static |
| `normal-navigator` | `#results` | static |
| `fermi-lab` | `#endScreen` (`#resultsScreen` is per question) | static |
| `dimension-checker` | `#results` | static |
| `factor-theorem` | `#practice-results`, `#test-results` (both rebuilt by innerHTML) | function route, two end states |
| `boolean-blitz` | `#resultsScreen` | static |
| `truth-will-set-you-free` | `#resultsScreen` | static |
| `complex-converter` | `#endScreen` | static |
| `matrix-crunch` | `#results` | static |
| `characteristic-quest` | `#results` | static |
| `eigenvalue-extractor` | `#results` | static |
| `eigenvector-engine` | `#results` | static |
| `six-sevens-bruv` | `#results` | static |
| `free-daily-pizza` | `#results` | static |
| `just-pythag-it-bruv` | `#results` | static |
