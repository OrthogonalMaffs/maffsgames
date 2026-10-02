# Chart Interrogator, cumulative frequency: Contract B record

**Built 28 Sep 2026** in a web session, as commit `d8b244e` on branch `claude/cool-hawking-f88bj7`. The contract, with Jon's
rulings, is `docs/next-contract-chart-interrogator-cumfreq.md`. This file is its step 6 report, its
step 2 report on the other three chart types, and the verification record. Only
`games/chart-interrogator/index.html` changed.

**What a student sees now.** Every cumulative-frequency answer is marked against the curve on the
screen, to a tolerance that scales with the axis. Phase 2 asks a benchmark question and a comparator
question instead of the spread sentence, whose key could never change. The 25% dropdown has one true
option instead of two.

## What changed

1. **One curve.** `cfCurve(s)` defines the curve: each class is one cubic Bezier between its two
   cumulative points, with both control points at the class midpoint, level with each end. That is
   the same construction `drawCumFreq` always drew. `drawCumFreq` now draws its curve and its points
   from `cfCurve`, and every key reads the same curve through `cfXAt` / `cfAtX`. These bisect on the
   Bezier parameter with 50 fixed halvings: no retry loop, exact to machine precision because both
   coordinates rise monotonically along every segment.
   - The straight-line `interpolateCF` and `buildCumFreqLookup` had no other caller anywhere in the
     repo, so they are removed.
   - No straight-line version of the curve is left for anything to reach for again.
2. **Tolerance and rounding** (`cfTruth`):
   - A reading off the x axis is marked to ±2.5% of the axis span. An IQR is marked to ±5%, because it
     is the difference of two readings. A count is marked to ±2.5% of n.
   - Keys are never rounded.
   - Display rounds to whole numbers, or to 1 dp where the span is 20 or less (CF9, CF10).
   - The IQR *shown* is the difference of the quartiles *shown*, so the screen never reads "between 21
     and 35 (an IQR of 13)".
     - Otherwise that would happen in CF4, CF8 and CF9, where the true IQR rounds one unit away from
       the difference of the rounded quartiles.
     - Both values are well inside the IQR tolerance.
3. **Phase 2** (`cfParts`, one definition feeding both the scaffold and the model answer). Every key
   in it comes from `cfTruth`, never from `sessionAnswers`.
   - **Benchmark:** the scenario's own benchmark line, then the contract's question, with a typed
     answer marked on the count tolerance.
     - The benchmark line (e.g. "Pass mark = 40") was always in the data but never on screen, and the
       question cannot be answered without it.
     - The model answer gives the count as "About N."
   - **Comparator:** Jon's accepted wording, e.g. "The IQR of 21 mm compared with a second greenhouse
     (12 mm) shows this group is less consistent." CF1 reads "compared with last year's IQR (32)".
     - The student's IQR sits in a filled chip, like every other value they worked out.
     - The comparator's IQR is plain text, because it is given, not derived.
   - **25%:** "below Q1 (v)", "below the median (v)", "below Q3 (v)", with only Q1 correct, as the
     contract lists them.
4. **Lines shared with the other chart types**, whose behaviour for those types is byte-identical
   (proved below):
   - Phase 1's "Correct — …" line and the completed-question list show a question's `shown` value when
     it has one. Only cumulative-frequency questions have one.
   - `submitPhase2` also marks a typed answer in the scaffold (only cumulative frequency has one), and
     only then says "check the highlighted answers" instead of "dropdowns".

## Step 6: true values from the drawn curve

| Scenario | Level | x span | Q1 | Median | Q3 | IQR | Reading tol | IQR tol | Old key, all ±3 (Q1 / med / Q3 / IQR) | Old key failed an accurate reader on |
|---|---|---|---|---|---|---|---|---|---|---|
| CF1 | gcse | 80 | 33.86 | 44.77 | 54.72 | 20.86 | ±2 | ±4 | 33 / 45 / 54 / 22 | — |
| CF2 | gcse | 70 | 105.42 | 115.86 | 126.14 | 20.71 | ±1.75 | ±3.5 | 106 / 117 / 127 / 21 | — |
| CF3 | alevel | 80 | 34.14 | 43.95 | 53.31 | 19.17 | ±2 | ±4 | 33 / 43 / 52 / 19 | — |
| CF4 | alevel | 60 | 21.47 | 26.93 | 34.58 | 13.11 | ±1.5 | ±3 | 21 / 26 / 34 / 13 | — |
| CF5 | alevel | 60 | 33.41 | 37.91 | 45.08 | 11.68 | ±1.5 | ±3 | 32 / 39 / 46 / 14 | — |
| CF6 | core | 300 | 185.42 | 231.25 | 280.50 | 95.08 | ±7.5 | ±15 | 193 / 237 / 285 / 93 | Q1, median, Q3 |
| CF7 | core | 1600 | 1,120.38 | 1,330.07 | 1,546.18 | 425.80 | ±40 | ±80 | 1139 / 1355 / 1575 / 436 | Q1, median, Q3, IQR |
| CF8 | core | 40 | 33.26 | 37.90 | 42.63 | 9.38 | ±1 | ±2 | 34 / 38 / 43 / 9 | — |
| CF9 | l4 | 10 | 1.528 | 2.523 | 3.564 | 2.036 | ±0.25 | ±0.5 | 2 / 3 / 4 / 2 | — |
| CF10 | l4 | 12 | 48.699 | 50.773 | 52.729 | 4.030 | ±0.3 | ±0.6 | 48 / 51 / 53 / 4 | — |

The old key joined the points with straight lines, rounded, and allowed a fixed ±3. It failed an
accurate reader on 7 of the 40 questions, all at Core level, where the axes run to £300k and £1,600.
Where the axis is short, the same ±3 accepted almost anything: in CF9 (a 10-day axis) any Q1 from −1
to 5 was marked correct.

**The key is the drawing.** The quartiles below were measured from the pixels of the original,
unedited canvas: the alpha-weighted centre of the curve's own pixels on the two rows either side of
each quartile's line. That is independent of any key code. The new key matches all 30 readings to
at most 0.05% of the axis, which is a quarter of a pixel. The same values were also computed a third
way, in closed form in Python. They agree with the game's own to floating-point precision: every
difference is under 1e-9 of the axis span.

| Scenario | Pixel-measured Q1 / median / Q3 (original drawing) | Largest gap to the new key |
|---|---|---|
| CF1 | 33.846 / 44.779 / 54.737 | 0.019 (0.024% of the axis) |
| CF2 | 105.432 / 115.897 / 126.147 | 0.035 (0.050% of the axis) |
| CF3 | 34.118 / 43.935 / 53.281 | 0.027 (0.033% of the axis) |
| CF4 | 21.468 / 26.907 / 34.563 | 0.025 (0.042% of the axis) |
| CF5 | 33.392 / 37.904 / 45.097 | 0.016 (0.027% of the axis) |
| CF6 | 185.552 / 231.326 / 280.604 | 0.132 (0.044% of the axis) |
| CF7 | 1120.876 / 1330.478 / 1546.757 | 0.576 (0.036% of the axis) |
| CF8 | 33.267 / 37.913 / 42.639 | 0.008 (0.019% of the axis) |
| CF9 | 1.525 / 2.525 / 3.565 | 0.002 (0.024% of the axis) |
| CF10 | 48.696 / 50.768 / 52.724 | 0.005 (0.042% of the axis) |

**Phase 2 keys.** Verdicts split 5 more consistent / 5 less, and every compIQR / IQR ratio lies
outside 0.7–1.4.
- CF7's comparator is **£280, by Jon's ruling of 28 Sep**. At £300 the drawn-curve IQR (£425.80) gave
  0.7046, inside the band, which fired the contract's STOP IF.
- £300 had been chosen against the straight-line IQR (£436.11, ratio 0.688), the very value this
  contract replaces.

| Scenario | Benchmark shown | Question | Answer (drawn curve) | Count tol | Comparator | Verdict | compIQR / IQR |
|---|---|---|---|---|---|---|---|
| CF1 | Pass mark = 40 | How many students passed? (above 40) | 50.00 | ±2 | last year's IQR (32) | more consistent | 1.534 |
| CF2 | Target height = 120 mm | How many plants reached the target? (above 120) | 25.00 | ±1.5 | a second greenhouse (12 mm) | less consistent | 0.579 |
| CF3 | Timetabled time = 45 min | How many journeys were late? (above 45) | 44.00 | ±2.5 | the old timetable (28 min) | more consistent | 1.461 |
| CF4 | National median = £28k | How many employees earn below the national median? (below 28) | 71.35 | ±3 | a competitor firm (£8k) | less consistent | 0.610 |
| CF5 | Legal maximum = 48 hrs | How many work over the legal maximum? (above 48) | 14.00 | ±2 | last year (20 hrs) | more consistent | 1.713 |
| CF6 | Regional average = £220k | How many properties are below the regional average? (below 220) | 37.27 | ±2.5 | a neighbouring town (£60k) | less consistent | 0.631 |
| CF7 | Average bill = £1,400 | How many households pay above the average bill? (above 1400) | 40.00 | ±2.25 | last year (£280) | less consistent | 0.658 |
| CF8 | Contract hours = 37.5 | How many work over contract hours? (above 37.5) | 60.50 | ±2.75 | another department (14 hrs) | more consistent | 1.493 |
| CF9 | SLA target = 3 days | How many deliveries missed the SLA? (above 3) | 30.00 | ±2 | the previous courier (3.5 days) | more consistent | 1.719 |
| CF10 | Tolerance limit = 52 mm | How many components exceed the tolerance limit? (above 52) | 30.00 | ±2.5 | Machine B (2 mm) | less consistent | 0.496 |

## Step 2: the other three chart types (report only, nothing changed)

**The 2.5% rule would change all 110 of their numeric tolerances. It would not make an accurate
reading fail its current key anywhere, so that STOP IF is clear.**
- Their keys are exact, except the histograms' `Math.round`, which is never more than 0.5 from the true
  value, well inside the rule's tolerance.
- The worst cases are logged in `docs/todo.md` §1: 1.15 (H4) and 1.16 (B7, B10, S3, S9).

**Stem and leaf** — every Phase 1 key is an exact value read from a table: median ±1, range ±1, no rounding. The rule is written for graph readings, so the 'axis' here is the data range across both groups, with a range taking the spread tolerance (×2).

| Scenario | Data range | Now: median / range | Under the rule: median / range | Would an accurate reading fail its current key? |
|---|---|---|---|---|
| S1 | 46 | ±1 / ±1 | ±1.15 / ±2.3 | no — keys are exact |
| S2 | 36 | ±1 / ±1 | ±0.9 / ±1.8 | no — keys are exact |
| S3 | 2.5 | ±1 / ±1 | ±0.0625 / ±0.125 | no — keys are exact |
| S4 | 52 | ±1 / ±1 | ±1.3 / ±2.6 | no — keys are exact |
| S5 | 150 | ±1 / ±1 | ±3.75 / ±7.5 | no — keys are exact |
| S6 | 63 | ±1 / ±1 | ±1.575 / ±3.15 | no — keys are exact |
| S7 | 50 | ±1 / ±1 | ±1.25 / ±2.5 | no — keys are exact |
| S8 | 270 | ±1 / ±1 | ±6.75 / ±13.5 | no — keys are exact |
| S9 | 3.5 | ±1 / ±1 | ±0.0875 / ±0.175 | no — keys are exact |
| S10 | 30 | ±1 / ±1 | ±0.75 / ±1.5 | no — keys are exact |

**Box plots** — median ±2 and IQR ±2, exact keys, no rounding. The drawn axis runs 10% beyond the data at each end (1.2 × the data range) across 500 px.

| Scenario | Drawn axis | ±2 is | Under the rule: median / IQR | Would an accurate reading fail its current key? |
|---|---|---|---|---|
| B1 | 52.8 | 18.94 px | ±1.32 / ±2.64 | no — keys are exact |
| B2 | 210 | 4.76 px | ±5.25 / ±10.5 | no — keys are exact |
| B3 | 43.2 | 23.15 px | ±1.08 / ±2.16 | no — keys are exact |
| B4 | 80.4 | 12.44 px | ±2.01 / ±4.02 | no — keys are exact |
| B5 | 390 | 2.56 px | ±9.75 / ±19.5 | no — keys are exact |
| B6 | 216 | 4.63 px | ±5.4 / ±10.8 | no — keys are exact |
| B7 | 2880 | 0.35 px | ±72 / ±144 | no — keys are exact |
| B8 | 38.4 | 26.04 px | ±0.96 / ±1.92 | no — keys are exact |
| B9 | 270 | 3.70 px | ±6.75 / ±13.5 | no — keys are exact |
| B10 | 2640 | 0.38 px | ±66 / ±132 | no — keys are exact |

**Histograms** — class frequency ±1 and sample total ±1 (both `Math.round`ed), proportion ±2 percentage points (`Math.round`ed); the first question is multiple choice. Under the rule a count takes 2.5% of n and a percentage 2.5 points.

| Scenario | n | Frequency: true / key / rule | Total: true / key / rule | Proportion: true / key / rule | Fails? |
|---|---|---|---|---|---|
| H1 | 162 | 30 / 30 / ±4.05 | 162 / 162 / ±4.05 | 30.86 / 31 / ±2.5 | no |
| H2 | 143 | 35 / 35 / ±3.575 | 143 / 143 / ±3.575 | 27.97 / 28 / ±2.5 | no |
| H3 | 114 | 25 / 25 / ±2.85 | 114 / 114 / ±2.85 | 21.93 / 22 / ±2.5 | no |
| H4 | 132.5 | 30 / 30 / ±3.3125 | 132.5 / 133 / ±3.3125 | 16.98 / 17 / ±2.5 | no |
| H5 | 162 | 30 / 30 / ±4.05 | 162 / 162 / ±4.05 | 21.60 / 22 / ±2.5 | no |
| H6 | 375 | 90 / 90 / ±9.375 | 375 / 375 / ±9.375 | 21.33 / 21 / ±2.5 | no |
| H7 | 310 | 70 / 70 / ±7.75 | 310 / 310 / ±7.75 | 19.35 / 19 / ±2.5 | no |
| H8 | 126 | 20 / 20 / ±3.15 | 126 / 126 / ±3.15 | 15.87 / 16 / ±2.5 | no |
| H9 | 1310 | 300 / 300 / ±32.75 | 1310 / 1310 / ±32.75 | 26.72 / 27 / ±2.5 | no |
| H10 | 101 | 25 / 25 / ±2.525 | 101 / 101 / ±2.525 | 19.80 / 20 / ±2.5 | no |

## Verification

- **Scripted check, stub server: 285 assertions, 0 failures.** Driven through the game's own
  functions and inputs, with every request that is not the local stub aborted. For each of CF1–CF10:
  - **Drawing:** pixel-identical to the original (canvas data URL compared).
  - **Game vs closed form:** the game's curve values equal the independent closed form.
  - **Phase 1:** for Q1, median, Q3 and IQR, the pixel-measured drawn value is marked correct, and
    that value ± 2 × tolerance is marked wrong, both sides.
  - **Phase 2 keys:** the comparator and 25% keys and options are right.
  - **Benchmark:** keyed to the independent value; its value + 2 × tolerance is marked wrong; a wrong
    verdict or "below Q3" is marked wrong.
  - **`sessionAnswers`:** Phase 2 re-renders byte-identically after every `sessionAnswers` value is
    set to −999.
  - **Model answer:** built after that corruption, it equals a sentence built independently in Python.

  Then, for all 10 stem-and-leaf, 10 box-plot and 10 histogram scenarios, the original file
  (`origin/main`, served by route interception) and the new one, both with the same seeded random,
  gave identical results for:
  - keys and drawing;
  - Phase 2 HTML;
  - wrong and right feedback;
  - the model answer.

  There were no page or console errors.
- **`check-site.py --only chart-interrogator`:** tier 2 PASS.
  - Tier 1 cannot load external resources from a web session: fonts and the Firebase SDK fail at the
    gateway. Every page load therefore records the same kind of failure, 5 before the change and 5
    after, and nothing else. CI's tier 1 is the authority.
  - The network guard: 0 escaped.
- **Tier 3, `--only chart-interrogator`:** 5 UNSUPPORTED, identical to before the change. The game
  opens on its menu, so tier 3 finds no option group; UNSUPPORTED is never a failure.
- **Tier 4 layer A:** `extract-banks.py --only chart-interrogator` then `check-banks.py --ci`: OK,
  matches the ledger exactly.
  - In a web session `esprima` only installs with `pip install --use-pep517 esprima`.
- **`check-leaderboard-coverage.js`:** OK.
- **Still owed:** `check-site.py --live` after deployment. A web session cannot reach
  maffsgames.co.uk.

## Found while building: logged in `docs/todo.md` §1, not fixed

- **1.15** Histogram H4: class 35–40 is frequency density 4.5 × width 5 = 22.5 employees, so the sample
  total is 132.5, keyed as 133.
- **1.16** Fixed tolerances that do not fit their scale:
  - box plots B7 and B10, where ±2 is a third of a pixel;
  - stem and leaf S3 and S9, where ±1 on decimal data accepts most of the data range.
- **1.17** `drawCumFreq`:
  - The curve is horizontal at every plotted point: each class is an S-bend, so the whole reads as a
    smoothed staircase, not the one smooth curve students are taught to draw.
  - It is drawn in the axis grey (`#5a5e6a`), measured in all four levels' colours. Canvas cannot
    resolve `strokeStyle='var(--accent)'`, so that assignment is ignored.
  - The keys now follow the drawn shape exactly, so neither issue affects marking.
- **1.18** CF5 and CF8 read "The median hours is approximately…" and "have a hours below…". The
  sentence frame assumes a singular noun, and both scenarios' `contextNoun` is "hours". The frame is
  unchanged from the old sentence, and the scenario data was outside this contract.
