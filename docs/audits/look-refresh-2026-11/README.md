# Look refresh: start screens of the games not yet on the theme (LOOK-REFRESH-1, 4 Nov 2026)

Research only, for Jon to name any game that still looks childish (contract LOOK-REFRESH-1, step 2). No game was changed for it.

**What it shows.** The start screen of every game still on `NOT_YET` in `scripts/check-theme.py` once this contract's three migrations
(Prime Sprint, Percentage Flip, Fraction Snap) are done: 88 games, each loaded at 375x667 from `main` at 6761017 through the stub server,
with its own fonts (pinned copies, or Google Fonts fetched as the live page would), no analytics or leaderboard request, 0.9 s after load.
The sheets number the games in `NOT_YET` order, which is roster order.

**The sheets** (in `docs/screenshots/look-refresh-2026-11/`, which Pages does not publish; `docs/audits/` would publish an image):

- [Sheet 1](../../screenshots/look-refresh-2026-11/contact-sheet-1.webp): games 1 to 24
- [Sheet 2](../../screenshots/look-refresh-2026-11/contact-sheet-2.webp): games 25 to 48
- [Sheet 3](../../screenshots/look-refresh-2026-11/contact-sheet-3.webp): games 49 to 72
- [Sheet 4](../../screenshots/look-refresh-2026-11/contact-sheet-4.webp): games 73 to 88

## Facts beside the pictures

Measured, not judged: which game looks childish is Jon's call.

- **Fonts.** No remaining game loads Press Start 2P or Nunito. 77 already load Outfit and JetBrains Mono from Google Fonts themselves, 9 load Outfit alone.
  Two use other faces: Estimation Golf (Playfair Display, Special Elite, Courier Prime: its golf-scorecard look) and Trig Wars (Bebas Neue, Share Tech Mono).
- **Header emoji.** Two: Trig Wars ("⚔ TRIG WARS ⚔") and Bearing Blitz ("⚓ Bearing Blitz").
- **Palette.** 57 of the 88 render a different palette from the one canon §7.5's rule gives them (read from each screenshot's median brightness: below half is dark).
  53 render dark where the rule gives light (their roster levels include Year 6, KS3 or GCSE); 4 render light where it gives dark. Listed in the table's last two columns.
  The theme moves each of these when it migrates; nothing changes before then.
- `core-maths-paper2b`'s font finding in `check-theme.py --verbose` ("\'jetbrains mono\") is an escaped quote inside a script string, not a different font.

| # | Game | Slug | Its own Google Fonts | Header emoji | Renders | Rule gives |
|---|---|---|---|---|---|---|
| 1 | Sequence Solver | `sequence-solver` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 2 | Estimation Golf | `estimation-golf` | Courier Prime, Playfair Display, Special Elite | - | dark | light (differs) |
| 3 | Prime or Composite | `prime-or-composite` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 4 | Equatle | `equatle` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 5 | 52-dle | `52dle` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 6 | Constructions Lab | `constructions-lab` | JetBrains Mono, Outfit | - | light | light |
| 7 | Word Problem Decoder | `word-problem-decoder` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 8 | Equation Builder | `equation-builder` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 9 | Spot the Error | `spot-the-error` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 10 | Gradient Hunter | `gradient-hunter` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 11 | Truth Buster | `truth-buster` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 12 | Spot the Muppet | `spot-the-muppet` | Outfit | - | light | light |
| 13 | Terrible Advice | `terrible-advice` | Outfit | - | light | light |
| 14 | Wrong on the Internet | `wrong-on-the-internet` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 15 | Maths Court | `maths-court` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 16 | Expected Damage | `expected-damage` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 17 | Negative Number Line | `negative-number-line` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 18 | Think of a Number | `think-of-a-number` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 19 | Formula Plug-In | `formula-plug-in` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 20 | Decimal Detective | `decimal-detective` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 21 | Four Quadrant Explorer | `four-quadrant-explorer` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 22 | Like Terms Collector | `like-terms-collector` | JetBrains Mono, Outfit | - | light | light |
| 23 | Probability Pioneer | `probability-pioneer` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 24 | Shape Shifter | `shape-shifter` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 25 | New Shapes | `new-shapes` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 26 | Higher Power | `higher-power` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 27 | Prisoner's Dilemma | `prisoners-dilemma` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 28 | Seven Bridges | `seven-bridges` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 29 | Index Laws | `index-laws` | Outfit | - | light | light |
| 30 | Quadratic Factoriser | `quadratic-factoriser` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 31 | Trig Wars | `trig-wars` | Bebas Neue, Share Tech Mono | ⚔ TRIG WARS ⚔ | dark | light (differs) |
| 32 | Trig Worms | `trig-worms` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 33 | Modular Battle | `modular-battle` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 34 | Surd Simplifier | `surd-simplifier` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 35 | Proportion Blaster | `proportion-blaster` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 36 | Trig Identity Duel | `trig-identity-duel` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 37 | Standard Form Blitz | `standard-form-blitz` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 38 | Circle Theorem Spotter | `circle-theorem-spotter` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 39 | Probability Paradox | `probability-paradox` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 40 | Angle Ace | `angle-ace` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 41 | Coordinate Geometry Dash | `coordinate-geometry-dash` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 42 | Graph Transformer | `graph-transformer` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 43 | Formula Unlocked | `formula-unlocked` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 44 | Bearing Blitz | `bearing-blitz` | JetBrains Mono, Outfit | ⚓ Bearing Blitz | dark | light (differs) |
| 45 | Scale Factor Scaling | `scale-factor-scaling` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 46 | Unit Converter | `unit-converter` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 47 | Formula Forge | `formula-forge` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 48 | Chart Interrogator | `chart-interrogator` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 49 | Component Crusher | `component-crusher` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 50 | Expectation Station | `expectation-station` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 51 | Better Value | `better-value` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 52 | Given That | `given-that` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 53 | Screening Room | `screening-room` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 54 | Linear Equation Solver | `linear-equation-solver` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 55 | Core Maths Paper 1 Practice | `core-maths-paper1` | JetBrains Mono, Outfit | - | dark | dark |
| 56 | Core Maths Paper 2A Practice | `core-maths-paper2a` | JetBrains Mono, Outfit | - | dark | dark |
| 57 | Core Maths Paper 2B Practice | `core-maths-paper2b` | JetBrains Mono, Outfit | - | dark | dark |
| 58 | Core Maths Paper 2C Practice | `core-maths-paper2c` | JetBrains Mono, Outfit | - | dark | dark |
| 59 | Tax Theft | `tax-theft` | Outfit | - | dark | dark |
| 60 | Stat Attack | `stat-attack` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 61 | Growth and Decay | `growth-and-decay` | JetBrains Mono, Outfit | - | dark | dark |
| 62 | Graph Sketcher | `graph-sketcher` | JetBrains Mono, Outfit | - | dark | dark |
| 63 | Glorious Gantt Game | `glorious-gantt` | JetBrains Mono, Outfit | - | dark | dark |
| 64 | Test the Claim | `test-the-claim` | JetBrains Mono, Outfit | - | dark | dark |
| 65 | Differentiation Duel | `differentiation-duel` | Outfit | - | light | dark (differs) |
| 66 | Integration Duel | `integration-duel` | Outfit | - | light | dark (differs) |
| 67 | SUVAT Selector | `suvat` | JetBrains Mono, Outfit | - | dark | dark |
| 68 | Curling Friction | `curling-friction` | JetBrains Mono, Outfit | - | dark | dark |
| 69 | Force Resolver | `force-resolver` | JetBrains Mono, Outfit | - | dark | dark |
| 70 | Moments Master | `moments-master` | JetBrains Mono, Outfit | - | dark | dark |
| 71 | Log Laws | `log-laws` | Outfit | - | light | dark (differs) |
| 72 | Binomial Blaster | `binomial-blaster` | JetBrains Mono, Outfit | - | dark | dark |
| 73 | Partial Fractions Duel | `partial-fractions-duel` | JetBrains Mono, Outfit | - | dark | dark |
| 74 | Proof Builder | `proof-builder` | JetBrains Mono, Outfit | - | dark | dark |
| 75 | Normal Navigator | `normal-navigator` | JetBrains Mono, Outfit | - | dark | dark |
| 76 | Fermi Lab | `fermi-lab` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 77 | Dimension Checker | `dimension-checker` | JetBrains Mono, Outfit | - | dark | dark |
| 78 | Factor Theorem | `factor-theorem` | JetBrains Mono, Outfit | - | dark | dark |
| 79 | Boolean Blitz | `boolean-blitz` | JetBrains Mono, Outfit | - | dark | dark |
| 80 | The Truth Will Set You Free | `truth-will-set-you-free` | JetBrains Mono, Outfit | - | dark | dark |
| 81 | Complex Converter | `complex-converter` | Outfit | - | dark | dark |
| 82 | Matrix Crunch | `matrix-crunch` | JetBrains Mono, Outfit | - | dark | dark |
| 83 | Characteristic Quest | `characteristic-quest` | JetBrains Mono, Outfit | - | dark | dark |
| 84 | Eigenvalue Extractor | `eigenvalue-extractor` | JetBrains Mono, Outfit | - | dark | dark |
| 85 | Eigenvector Engine | `eigenvector-engine` | JetBrains Mono, Outfit | - | dark | dark |
| 86 | Six Sevens, Bruv | `six-sevens-bruv` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 87 | Free Daily Pizza | `free-daily-pizza` | JetBrains Mono, Outfit | - | dark | light (differs) |
| 88 | Regression Rumble | `regression-rumble` | Outfit | - | light | dark (differs) |

`regression-rumble` is withdrawn: its URL shows the holding page, which is what is pictured.

## Age-specific wording in static page text (`check-theme.py --verbose`)

Report only, for Jon to rule on (SR-11). 12 games; each line is one piece of start-screen text the check matched.

```text
Age-specific wording in static page text, for Jon to rule on: 12 of 90 NOT_YET games.
  word-problem-decoder         KS3
  word-problem-decoder         Year 7-9
  word-problem-decoder         Year 10-11
  spot-the-error               KS3
  spot-the-error               Year 7-9
  spot-the-error               Year 10-11
  gradient-hunter              Year 10-11
  gradient-hunter              Year 12-13
  truth-buster                 KS3 and GCSE level. Calibrates your confidence. 7 questions.
  spot-the-muppet              KS3
  terrible-advice              KS3
  wrong-on-the-internet        KS3
  maths-court                  KS3
  maths-court                  Year 7-9. BIDMAS, fractions, percentages, angles, sequences.
  maths-court                  Year 10-11. Algebra, Pythagoras, probability, circle theorems, indices.
  higher-power                 KS3
  higher-power                 KS3
  prisoners-dilemma            KS3
  seven-bridges                KS3
  seven-bridges                KS3
  binomial-blaster             A-Level Year 1
  binomial-blaster             A-Level Year 2
  binomial-blaster             Year 1:
  binomial-blaster             Year 2:
```

Note: Binomial Blaster's hits are "A-Level Year 1" and "A-Level Year 2", which name parts of a qualification, not a school year; SR-11 keeps "GCSE and every level above it". The check matches "Year 1"/"Year 2" all the same.
