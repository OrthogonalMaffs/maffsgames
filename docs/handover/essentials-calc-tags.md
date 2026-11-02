# Essentials: proposed Calculator tags for the 28 untagged games (for Jon's ruling)

Build lane, 29 Oct 2026. Contract ESSENTIALS-FILTER, Phase B. **Nothing here is written to `.claude/rules/game-roster.md`.** Jon rules first.

## How these were decided

- None of the 28 has calc-flag data. Calc-flag (#603) only touched the banks behind the new games (pie charts, percentages and money, reading charts, probability). The 28 are older games with no calculator settings in their pages, so every proposal below comes from the game's own questions: the number ranges, what the working looks like, and whether the answer can be reached by a method a student does in their head.
- "Confidence": **High** = the questions are plainly mental or plainly not. **Medium** = judged from a sample of the bank or the generator, not every question. **UNCLEAR** = the questions do not settle it (listed again at the end, with my lean, for Jon rather than guessed).
- "Levels differ" marks a game whose KS3 and GCSE banks differ. The roster has one value per game. `by stage` does not fit these (a level is not a stage: the page's `maffs-calc-stages` map is keyed by stage), so I propose `optional` (shown under both Essentials chips) and say so.

## The table

| # | Game (slug) | Section | Proposed | Confidence | Reason (from its own questions) |
|---|---|---|---|---|---|
| 1 | Six Sevens, Bruv (`six-sevens-bruv`) | Number | not allowed | High | Times-table recall to 12 x 12, typed. A calculator defeats it. |
| 2 | Free Daily Pizza (`free-daily-pizza`) | Number | not allowed | Medium | Fraction, decimal and percentage equivalence from benchmarks; "of an amount" amounts are built as the denominator times a small multiple; thirds shown recurring. Designed for mental work. |
| 3 | Negative Number Line (`negative-number-line`) | Number | not allowed | High | Placing and ordering on a -10 to 10 line. |
| 4 | Decimal Detective (`decimal-detective`) | Number | not allowed | High | Ordering, rounding and placing decimals. |
| 5 | Think of a Number (`think-of-a-number`) | Number | not allowed | High | Undo one to three steps of +, -, x, / with small whole numbers (answers like 24, 12, 5). |
| 6 | Factor Race (`factor-race`) | Number | not allowed | High | Compare two numbers' factor counts. |
| 7 | Prime Sprint (`prime-factorisation`) | Number | not allowed | Medium | Build a number up from primes. |
| 8 | Estimation Golf (`estimation-golf`) | Number | not allowed | High | Estimation by judgement, scored on closeness. |
| 9 | Formula Plug-In (`formula-plug-in`) | Algebra | not allowed | High | Substitute whole numbers into area, perimeter, volume, speed and mean formulae; every answer is at most 200 and no formula has pi. |
| 10 | Like Terms Collector (`like-terms-collector`) | Algebra | not allowed | High | Collecting like terms; exact whole numbers. |
| 11 | Linear Equation Solver (`linear-equation-solver`) | Algebra | not allowed | Medium | Pick the inverse operation at each step; fractional answers are kept as fractions (8x = 12 gives x = 3/2). |
| 12 | Equation Builder (`equation-builder`) | Algebra | not allowed | Medium | Build an equation from slot-and-tile pieces; nothing is evaluated. |
| 13 | Four Quadrant Explorer (`four-quadrant-explorer`) | Algebra (card) | not allowed | High | Plotting and reading coordinates. |
| 14 | Sequence Solver (`sequence-solver`) | Algebra | **UNCLEAR** (lean: optional) | Low | Levels differ: KS3 linear nth term, GCSE linear and quadratic and geometric, A-Level sigma and recurrence. Whole-number terms, but the upper levels are heavier arithmetic. |
| 15 | Split It (`split-it`) | Ratio | optional | Medium | Levels differ: KS3 is whole-number sharing and scale factors; GCSE adds currency (GBP x 1.xx to euros) and speed to one decimal place. |
| 16 | Proportion Blaster (`proportion-blaster`) | Ratio | **UNCLEAR** (lean: optional) | Low | GCSE and A-Level bank: reverse percentages (GBP 170 after a 15% fall), y proportional to 1/x cubed giving 0.625, net percentage change. A mix of mental and calculator items in one bank. |
| 17 | Better Value (`better-value`) | Ratio | required | Medium | Multi-step money across a year: 260 days of coffee, 3% AER, boiler policy with excess and an hourly rate, break-even call minutes. Core Maths applied. |
| 18 | Percentage Flip (`percentage-flip`) | Ratio | not allowed | High | 50%, 25%, 10%, 75%, 15%, 35% of round amounts, each shown with a 10%-and-halves working. |
| 19 | New Shapes (`new-shapes`) | Geometry | not allowed | High | Parallelogram, trapezium and prism with whole-number sides; every answer at most 90. |
| 20 | Angle Ace (`angle-ace`) | Geometry | not allowed | Medium | Find the angle and name the reason; angle facts and sums. (Sampled the Year 6 bank; the GCSE bank not read in full.) |
| 21 | Shape Shifter (`shape-shifter`) | Geometry | not allowed | High | Translation, reflection, rotation: positions on a grid. |
| 22 | Probability Pioneer (`probability-pioneer`) | Probability | not allowed | High | Place events on a 0 to 1 scale; fractions like 3/5 chosen from options. |
| 23 | Expected Damage (`expected-damage`) | Probability | optional | Medium | Levels differ: KS3 starts with certain outcomes; later items weight outcomes by 0.25, 0.35, 0.45 and so on (expected values 2.1, 2.7, 3.3). Worth a calculator, doable without. |
| 24 | Given That (`given-that`) | Probability | **UNCLEAR** (lean: not allowed) | Low | Conditional probability from two-way tables of 80 to 120 people, typed as fractions; fractions are exact but the upper levels (A-Level, Level 4) were not read. |
| 25 | Distinctly Average (`distinctly-average`) | Statistics | optional | Medium | Levels differ: KS3 whole-number sets with a stepped median scaffold; GCSE frequency-table means and missing values shown to 1 d.p. (the working says "=" or "approx"). |
| 26 | Stat Attack (`stat-attack`) | Statistics | scientific | Medium | Estimated mean and standard deviation from grouped tables (for example mean 46.4, SD 11.5): needs the square root and squares. |
| 27 | Chart Interrogator (`chart-interrogator`) | Statistics | not allowed | Medium | Reading and comparing diagrams to a scale band; counts and comparisons, no arithmetic beyond reading. |
| 28 | Correlation or Coincidence? (`correlation-or-coincidence`) | Statistics | not allowed | High | Judging cause, common cause or chance from a described relationship; no numbers to compute. |

## Count if every proposal is accepted

Counting the three UNCLEAR games at their lean (Sequence Solver and Proportion Blaster optional, Given That not allowed):

- not allowed: 21 (20 without Given That)
- optional: 5 (rows 14, 15, 16, 23, 25)
- required: 1 (row 17)
- scientific: 1 (row 26)
- by stage: 0

With the 8 already tagged (2 not allowed, 2 required, 2 scientific, 2 by stage), all 36 Essentials games would be tagged: 23 non-calculator, 6 calculator (required or scientific), 7 under both chips (5 optional and 2 by stage).

## What a tag other than `not allowed` costs (read this before ruling)

`scripts/check-calculator.py` (canon section 4.4) ties each roster value to the game's page, so the roster is not the only edit:

- **not allowed**: no page change. The check only requires that the page carries no calculator and no calculator badge. These 20 (21 with Given That, once ruled) can go straight into the roster.
- **required / scientific / optional**: the game's page must load `schools/assets/calculator.js` and `keypad.js`, show the matching badge on its start screen ("Calculator required", "Scientific calculator required", "Calculator optional"), and (scientific) mount `MaffsCalc` with `keys: 'scientific'`. That is an edit to each game page (7 games: better-value, stat-attack, split-it, expected-damage, distinctly-average, plus the two UNCLEAR optional ones), which this contract is told not to touch, and a roster tag alone would turn CI red on every one of them.

So Phase B can only write the `not allowed` rows on its own. Options for Jon:

1. Write the 20 `not allowed` tags now (rows 1 to 13, 18 to 22, 27, 28), and give the calculator and optional games their own contract (page edit, badge, calculator, the game's verifier). Until then those games stay `untagged` and show under All only.
2. Rule the five optional and two calculator tags now and have the page edits done as a separate contract first, then write all 28 in one step.

## UNCLEAR: for Jon (the contract's STOP IF; not guessed)

1. **Sequence Solver**: no single answer for KS3 / GCSE / A-Level. Lean `optional`.
2. **Proportion Blaster**: GCSE and A-Level proportion items; some are mental (share GBP 150 in 3:2), some want a calculator (0.625, reverse percentage). Lean `optional`.
3. **Given That**: exact fractions from tables, but the A-Level and Level 4 questions were not read in full. Lean `not allowed`.

Also for Jon: where a game has two levels with different needs (split-it, expected-damage, distinctly-average, sequence-solver), `optional` is my stand-in for "KS3 is mental, GCSE is not"; the Essentials card for each opens the Foundation level, where all four are closer to mental than the roster value says. If you would rather tag by the level the Essentials card opens, say so and I will re-read those four at that level only.
