# The 6 P's bank inventory (25 Oct 2026)

Contract GEN-SIX-PS, steps (a) and (b) only, done as an inventory before `docs/six-ps-schema.md` has merged. **No bank file is written and no game is touched.** Method: `scripts/extract-banks.py` (list games), then each generator game opened on the stub server at the topic's route level and its own pool or generator called from the page (`page.evaluate`). Counts are what the game itself holds at the route's level and stage or mode; "Foundation-pitched" means the route's level, stage and mode (Jon's routing in `schools/assets/exam-topics-ocr-foundation.json`), because no game marks items by exam tier. A count from a generator is the number of **distinct** items in the draws made (a floor where marked ≥).

## Result in one paragraph

All 32 covered topics route to 29 games. **Every game can be read from outside with no game edit**: 19 games hold question lists the extractor already reads; 10 build their questions in code (Factor Race is counted here: its Foundation level draws from a pair table, not the 20-item list the extractor sees), and all 10 expose their own pool or generator on a global (`window.SQS`, `window.FDP`, `window.HMP`, `window.TAW`, `window.JPIB`, `window.DA_ITEMS`, `window.QF_POOLS`, top-level `POOL` and `questionFrom` in trig-worms, top-level `generators` in split-it, top-level `VALID_PAIRS` in factor-race). So **no topic stops on the unreachable-generator STOP IF**. Four topics are under 30 (shortfall list below). The real risk is conversion: many topics are pictures, drags or tile builds (listed below), so turning them into a written exam form needs the schema's rule for diagrams.

## Per topic (highest marks first)

| # | Topic (marks) | Game, level, scope | Foundation items | Source | Callable from outside | Worked solution in the game |
|---|---|---|---|---|---|---|
| 1 | ratio (13.3) | split-it ks3, modes simplify + divide | simplify ≥296, divide ≥2,342 | generator | yes: top-level `generators.simplify(level)`, `generators.divide(level)` | `working`, `hint` on every item |
| 2 | direct-proportion (11.7) | split-it ks3, modes unitary + scale | unitary ≥3,644, scale 120 | generator | yes: `generators.unitary`, `generators.scale` | `working`, `hint` |
| 3 | powers-roots (9.0) | index-laws gcse | 45 (Multiply 8, Divide 8, Power of a power 7, Zero 4, Negative 8, Fractional 10) | list | yes (extractor) | `exp` |
| 4 | compound-measures (8.2) | squared-squirrel ks3, stages 2 + 3 | 154 + 308 = 462 | generator | yes: `window.SQS.pools()` / `buildPools()` | `SQS.steps(q)`, named slips in `errors` |
| 5 | linear-equations (7.5) | linear-equation-solver gcse | 141 | list | yes | `sol`, `ops` |
| 6 | sequences (7.3) | sequence-solver ks3 | 50 | list | yes | **none** (distractors `d` only) |
| 7 | angles (7.2) | angle-ace gcse | 35 (year6 has 40) | list | yes | `steps`, `reason`, `misconception` |
| 8 | arithmetic-negatives (7.0) | negative-number-line year6 | 30 (order 15, calculate 15) | list | yes | **none** |
| 9 | fdp-convert (6.8) | free-daily-pizza ks3, stages 1 + 2 | 89 + 206 = 295 | generator | yes: `window.FDP.BANK[1]`, `[2]` | `equation`, named slips as `tag` |
| 10 | number-vocabulary (6.7) | factor-race ks3 | 2,694 ordered pairs (1,347 unordered); the list the extractor sees is the 20-item Year 6 bank | generator | yes: top-level `VALID_PAIRS` and `getFactors` | factor counts shown after each answer; no written solution |
| 11 | fraction-operations (6.5) | how-many-parts ks3, Foundation stage 3 | 96 (`HMP.fpool('stage3')`) | generator | yes: `window.HMP.fpool`, `HMP.POOLS` | `HMP.steps(q)`, named errors in `ERR` |
| 12 | fraction-percentage-of-amount (6.3) | free-daily-pizza ks3, stage 3 | 137 (90 fraction of, 47 percentage of) | generator | yes: `FDP.BANK[3]` | `equation`, `tag` |
| 13 | averages (6.3) | distinctly-average ks3 | 259 (mean, median, mode, range) | pool built at load (not read by the extractor: no `correct` field) | yes: `window.DA_ITEMS.ks3` | explanation text built by the game; per-item field to be read at step (d) |
| 14 | area (6.0) | take-a-walk ks3, stages 1-3 | ask A: 81 + 276 + 63 = 420 (plus 17 background-kind items) | generator | yes: `window.TAW.pools()` | `TAW.steps(q)` |
| 15 | inverse-operations (5.3) | think-of-a-number year6 | 50 | list | yes | `steps` / `undoSteps` |
| 16 | trigonometry (5.0) | trig-worms gcse | 1,152 (angle 536, side 412, hypotenuse 204) | pool built at load | yes: top-level `POOL` and `questionFrom(type, angle, hyp, ratio)` | `exp`, `slips` built inside `questionFrom` |
| 17 | simultaneous (4.2) | simultaneous-solver gcse, stage 4 | 48 (stages 1-3 hold 48 each) | list | yes | **none** on stage 4 |
| 18 | transformations (4.0) | shape-shifter year6, random-mix | 81 (translate 15, reflect 35: 15 in the axes and 20 built in y = x, y = -x, x = k, y = k; rotate 15; enlarge 16 built, from 26 Oct) | list | yes | `desc` |
| 19 | simplify-expressions (3.7) | like-terms-collector year6 | 40 (stage 2: 10, stage 3: 30) | list | yes | **none** |
| 20 | basic-probability (3.7) | probability-pioneer year6 | 45 (stage 1: 10, 2: 20, 3: 15) | list | yes | `why` (stage 2), `explanation` (stage 3) |
| 21 | substitution (3.5) | formula-plug-in year6 | 50 | list | yes | `workingSteps` |
| 22 | perimeter (3.3) | take-a-walk ks3, stage 1 | ask P: 81 (plus 10 background-kind) | generator | yes: `TAW.pools()['stage-1']` | `TAW.steps(q)` |
| 23 | standard-form (3.2) | standard-form-blitz gcse | 50 | list | yes | **none** |
| 24 | quadratics-factorise (3.0) | quadratic-factoriser gcse | 174 (both positive 45, one negative 72, both negative 45, difference of squares 12) | pool built at load | yes: `window.QF_POOLS.gcse.stages` | guided steps in the game; per-item field to be read at step (d) |
| 25 | estimation (3.0) | estimation-engine gcse | 45 | list | yes | `show` |
| 26 | metric-units (3.0) | unit-converter gcse | 58 (Length 10, Area 15, Volume 15, Mixed units 8, Engineering 10); 48 without Engineering | list | yes | `s` (steps) |
| 27 | vectors (2.8) | component-crusher gcse | **15** | list | yes | **none** |
| 28 | form-expressions (2.7) | equation-builder ks3 | **40 at ks3 (20 assembly, 20 gap-fill), of which 9 are "Forming Equations"**; the extractor's 120 is the whole file | list | yes | **none** |
| 29 | rounding (2.3) | decimal-detective year6 | **15** rounding items (`ROUNDUP_QUESTIONS`); 45 if all three activities count (order 15, place on a line 15) | list | yes | **none** |
| 30 | pythagoras (2.3) | just-pythag-it-bruv ks3 | ≥252 (round 1), ≥2,314 (round 2), ≥1,294 (round 3), from 1,500 seeds | generator | yes: `window.JPIB.buildSession(seed)` | `JPIB.worked(Q)`, `spot`, `add` slip |
| 31 | change-subject (2.0) | formula-unlocked gcse | **29** (`Q_GCSE`; the game serves exactly this list at gcse) | list | yes | `steps`, `hints`, `misconception` |
| 32 | coordinates (1.8) | four-quadrant-explorer year6 | 45 (plot 20, read 15, shape 10) | list | yes | **none** |

## Shortfall list (under 30, for Project Claude)

| Topic | Items | Note |
|---|---|---|
| vectors | 15 | component-crusher gcse, all it has |
| form-expressions | 9 (or 40) | equation-builder ks3: 9 are about forming equations; the other 31 at ks3 are ratio, area, angles and so on |
| rounding | 15 (or 45) | decimal-detective: 15 are rounding; 30 are ordering decimals and placing them on a line |
| change-subject | 29 | one short; `Q_GCSE` is the whole gcse set |
| arithmetic-negatives | 30 | exactly at the line |

## Items that need a ruling on conversion (not yet a STOP IF: the schema is not merged)

These are picture, drag, tap or tile items. Turning them into a written exam question from the same numbers is mechanical for some and a wording judgement for others; the schema's rule decides which.

- **Diagram needed to ask the question:** angle-ace (angle figures), take-a-walk (compound shapes, areas and perimeters), just-pythag-it-bruv (triangles), trig-worms (the labelled triangle), component-crusher (grid and arrows), four-quadrant-explorer (plot a point, read a point, shape vertices).
- **Tap or drag, with a clear written form:** shape-shifter (the contract's own example, "Write down the coordinates of A'"), factor-race ("which of 24 and 18 has more factors"), probability-pioneer stage 1 (place an event on a 0 to 1 scale), like-terms-collector (drag the terms).
- **Multi-answer or build items:** split-it scale (one answer per ingredient), equation-builder (tiles and gap-fill), decimal-detective (order and place-on-a-line).

## Missing worked solutions so far (step (d) will confirm per item)

sequences (sequence-solver), arithmetic-negatives, simultaneous (stage 4), simplify-expressions, standard-form, vectors, form-expressions, rounding and coordinates have no worked-solution field at all. Probability has one for stages 2 and 3 only (stage 1 has none). Not invented; they go on the list.

## What this does not cover

Items' answers have not been recomputed (that is step (d) onward). Generator counts for split-it, factor-race and JPIB are floors from random draws, not exact spaces. The generator games' item shape (`question`, `options`, per-item worked field) is read at step (e) once the schema says what is carried.
