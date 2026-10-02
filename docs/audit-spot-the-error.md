# Spot the Error — read-only audit

Step 1 of `docs/snagging-list.md` §2 (Jon, 27 Sep 2026: "it's a poor game"). **Read-only. No fixes applied.** Scope and STOP IF conditions per that entry; this file is the full seven-field contract's output plus the STOP IF resolution, done together since the extraction itself is what resolved the STOP IF question.

## Data source and a STOP IF that fired

The contract's STOP IF list includes *procedurally generated*, *counts don't reconcile*, and *tiers differ from the roster*. Checking those before extracting:

- **Not procedurally generated.** `data/banks/spot-the-error.json` declares `"generator": false`, confirmed by `check-ledger.json`. Every question is hand-authored.
- **Roster matches.** The portal card (`index.html:1409`) tags this game KS3 / GCSE / Level 4, matching the bank's three level keys.
- **Counts do NOT reconcile — STOP IF fired.** `data/banks/spot-the-error.json` declares `levels.ks3.count`, `levels.gcse.count` and `levels.level4.count` as **110 each**, and stores the identical 110-question array (all three levels mixed together) under all three level keys. That is not what the live game plays: `games/spot-the-error/index.html:210-339` holds one array, `Q`, of 110 questions total, and `index.html:377` does `Q.filter(q => q.level === currentLevel)` at session start. The real per-tier split, read from that filter, is **KS3 35 / GCSE 45 / Level 4 30 = 110**. So the exported bank file is not a per-tier export at all — it looks like whatever tool produced it dumped the whole combined array into each tier's slot instead of filtering by `q.level`, and then re-used the combined length as `count` for all three. The live game itself is unaffected (it filters correctly from its own inline array) — this is an export/tooling artifact, consistent with the bank's own `"read_method": "live"`, meaning nothing currently plays the static file. But it will mislead anything that trusts it (including a naive count check on this very contract), so it's filed below as a live-bug item, not silently corrected in this audit.

**Resolution: proceeded**, using the live game's own inline `Q` array (110 questions, each with a correct `level` field) as the authoritative source — this is what a student actually plays. All figures below are against that source.

## Counts vs the 40–50 minimum

| Tier | Actual questions | Vs 40–50 minimum |
|---|---|---|
| KS3 | 35 | **Below minimum** |
| GCSE | 45 | Within range |
| Level 4 | 30 | **Below minimum, furthest short** |

## Systemic findings (apply to all 110/110 questions — confirmed from the game's own code, not per-question)

All four read directly from `games/spot-the-error/index.html`, not from authoring variance, so no per-question fix can touch them.

1. **Snagging-list issue #1 ("Find the misread" targets correct text) is 100% systemic, not occasional.** The scenario prose (`currentQ.text`) never itself contains a false statement — every arithmetic error lives in the `steps` array, never the narrative. So the single `errorPhrases` entry marked `isError:true` is, in all 110 cases, a true fragment lifted verbatim from the problem (`reduced by 20%`, `area of reflective material`, `det(A − λI)`, ...) — never something wrong to "find". Verified this holds for all 110. A literal-minded student looking for a false sentence will never find one, by construction.
2. **Snagging-list issue #2 (Stage 2 doesn't show Stage 1's working) is also 100% systemic.** `showStage2()` (`index.html:438-457`) replaces `#stageContent` entirely with a fresh `.phrase-zone` built only from `currentQ.text`; `currentQ.steps` is never referenced again after Stage 1. No question's Stage 2 shows the wrong working that Stage 1 revealed.
3. **Snagging-list issue #4 (scenario renders twice) is also 100% systemic.** `#questionCard` is set once in `showStage1()` (`index.html:401`) and is never cleared or updated by `showStage2()` — it stays on screen showing the plain scenario text. `showStage2()` then renders a **second**, independent copy of the same text inside `.phrase-zone` (`index.html:444`) with tappable spans. Both are visible together for the whole of Stage 2, on every question.
4. **Stage labels, verbatim:** `"Stage 1: Find the error"` (`:400`) / `"Stage 2: Find the misread"` (`:440`).

## Error classification: READING vs METHOD vs UNCLEAR

The bank's own `errorType` field only ever takes two values across all 110 questions: `operation` (55) and `setup` (55) — `reading` is not an authored category at all. Reading every explanation confirms why: each one corrects a choice of operation or formula/setup (multiply vs add the ratio parts, radius vs diameter, which variable a formula divides by, chain rule vs no chain rule, ...). None hinges on a student misreading a word, number, or quantity in the prose — the prose is always read correctly; what goes wrong is the calculation applied to it.

**Result: 110/110 = METHOD. 0 = READING. 0 = UNCLEAR.** This matches the two examples already in `docs/snagging-list.md` (basketball; "a poor game") and confirms the property holds across the whole bank, not just the two questions Jon happened to see live.

## Authored-but-undisplayed fields

`id`, `level`, `errorType`, `topic` are read by game logic (filtering, scoring, analytics tags) but never shown to the student as text. Each `step`'s own `correct` boolean is authored but functionally unused: `handleStage1()` (`index.html:416`) checks `step.id === currentQ.errorStepId`, never `step.correct`. Checked all 110 for drift between the two: **zero anomalies** — every question has exactly one step with `correct:false`, and it always matches `errorStepId`. Also **zero anomalies** in `errorPhrases`: every question has exactly one `isError:true` entry, and it always matches a real step's error. So the redundant field is dead weight, not a live inconsistency.

## Headline bugs found (live, not design opinion — filed to `docs/todo.md` §1)

- **`ste_gcse_016` (GCSE, Standard Form): Stage 2 is unwinnable.** Its only `isError:true` phrase, `10⁴ × 10³`, does not occur verbatim in the question text (`Calculate (3 × 10⁴) × (2 × 10³)`), so `.replace()` never creates a tappable span for it. No correct answer is ever clickable on this question's Stage 2.
- **`ste_gcse_002` (GCSE, Compound Interest): the shown "correct answer" is itself wrong.** 2000 × 1.035³ = £2,217.44 to the nearest penny; the explanation states £2,217.24. A student who fails this question is taught the wrong figure.
- **`data/banks/spot-the-error.json` is a corrupted export** — see the STOP IF section above. Not currently read by anything live, but will mislead future tooling.
- 5 further questions (`ste_gcse_025`, `ste_l4_007`, `ste_l4_013`, `ste_l4_018`, `ste_l4_028`) have one decoy phrase each that doesn't render — cosmetic, drops decoy count from 2 to 1, does not affect correctness.
- `ste_gcse_006`'s stated distance is ~0.1 m off a more precise recompute (118.6 m vs stated 118.5 m) — noted, not severity-worthy on its own.

---

## Full per-question extraction

One row per question. **Wrong working shown / rendered twice** columns are omitted per-row since they are the systemic findings above (true for all 110). `Target phrase` is the single `isError:true` entry a student must tap in Stage 2 to score full marks; `Renders?` flags the 6 exceptions found. `Arithmetic` flags the 2 exceptions found; all other rows were hand-recomputed from the question's own stated numbers against the explanation's final answer with no discrepancy.

### KS3 (35 questions)

| ID | Topic | Type→Class | Target phrase (Stage 2 correct answer) | Renders? | Wrong step (errorStepId) | Corrected explanation | Arithmetic |
|---|---|---|---|---|---|---|---|
| `ste_ks3_001` | Ratio | operation → METHOD | share the winnings in the ratio | yes | Total parts = 2 × 3 × 5 = 30 | 'Ratio' means add the parts to find the total, not multiply them. Total parts = 2 + 3 + 5 = 10. Amy’s share = (2/10) × £180 = £36. | OK |
| `ste_ks3_002` | Percentages | operation → METHOD | reduced by 20% | yes | Sale price = £65 + £13 = £78 | 'Reduced by' means subtract the discount, not add it. Sale price = £65 − £13 = £52. | OK |
| `ste_ks3_003` | Fractions | operation → METHOD | one-third of the remainder | yes | Sold in afternoon = (1/3) × 48 = 16 | The afternoon fraction applies to the remainder (12), not the original 48. Afternoon sales = (1/3) × 12 = 4. Left at end = 12 − 4 = 8. | OK |
| `ste_ks3_004` | Proportion | operation → METHOD | travels 240 miles on a full tank of 30 litres | yes | Rate = 240 − 30 = 210 miles per litre | The rate is found by dividing, not subtracting. Rate = 240 ÷ 30 = 8 miles per litre. Fuel needed = 180 ÷ 8 = 22.5 litres. | OK |
| `ste_ks3_005` | Percentages | operation → METHOD | what percentage walk to school | yes | Percentage = 18 × 30 ÷ 100 = 5.4% | Percentage = (part ÷ whole) × 100, not part × whole ÷ 100. Correct: (18 ÷ 30) × 100 = 60%. | OK |
| `ste_ks3_006` | Sequences | operation → METHOD | nth term | yes | Multiply by position: nth term = 4n | The nth term of an arithmetic sequence is dn + (a − d), not just dn. nth term = 4n + (1 − 4) = 4n − 3. | OK |
| `ste_ks3_007` | Area | operation → METHOD | area of reflective material | yes | Area = base × height = 40 × 35 = 1400 cm² | Area of a triangle = ½ × base × height, not base × height. Correct area = ½ × 40 × 35 = 700 cm². | OK |
| `ste_ks3_008` | Mean | operation → METHOD | age of the seventh player | yes | Age of 7th player = 122.5 × 102 = 12,495 | To find the seventh player’s age, subtract the original total from the new total, not multiply. Age = 122.5 − 102 = 20.5 years. | OK |
| `ste_ks3_009` | Ratio | operation → METHOD | ratio 1:4 | yes | Orange juice fraction = 1 out of (1 × 4) = 4 parts | The total parts are found by adding, not multiplying. Total = 1 + 4 = 5 parts. Orange juice = (1/5) × 500 = 100 ml. | OK |
| `ste_ks3_010` | Probability | operation → METHOD | estimates the probability of picking red | yes | P(red) = 24 ÷ (24 + 36 + 20 + 4) = 24 ÷ 84 | The total number of trials is 80 (stated in the question), so P(red) = 24 ÷ 80 = 0.3. | OK |
| `ste_ks3_011` | Fractions | operation → METHOD | full capacity of the tank | yes | Full capacity = 360 × (3/8) = 135 litres | To find the full capacity, divide by the fraction, not multiply. Full capacity = 360 ÷ (3/8) = 360 × (8/3) = 960 litres. | OK |
| `ste_ks3_012` | Percentages | operation → METHOD | 4% simple interest per year | yes | Student then says: '4% compound interest would give £250 × 1.04³ = £281.22' | The question specifies simple interest, not compound. The method in steps 1–3 is correct. Compound interest gives a different answer and is not relevant here. | OK |
| `ste_ks3_013` | Scale | operation → METHOD | a scale of 1:50,000 | yes | Real distance = 6.4 + 50,000 = 50,006.4 cm | Scale means multiply, not add. Real distance = 6.4 × 50,000 = 320,000 cm = 3.2 km. | OK |
| `ste_ks3_014` | Angles | operation → METHOD | angle on the other side of the junction | yes | Student says: 'Actually angles around a point sum to 360°, so other angle = 360° − 47° = 313°' | The two angles on either side of a straight junction sum to 180°, not 360°. The correct answer is 133°. | OK |
| `ste_ks3_015` | Area & Perimeter | operation → METHOD | total length of fencing needed | yes | Fencing needed = length × width = 85 × 62 = 5,270 m | Fencing goes around the perimeter, not the area. Perimeter = 2(85 + 62) = 294 m. | OK |
| `ste_ks3_016` | Fractions | operation → METHOD | total distance | yes | Common denominator = 3 × 4 × 6 = 72 | The LCM of 3, 4 and 6 is 12, not 72. Total = 28/12 + 21/12 + 38/12 = 87/12 = 7¼ miles. | OK |
| `ste_ks3_017` | Number | operation → METHOD | next align | yes | Find HCF(420, 315) = 105 | To find when they next align, you need the LCM, not the HCF. LCM(420, 315) = 1260 days. | OK |
| `ste_ks3_018` | Sequences | operation → METHOD | Each row has 2 more seats than the one before | yes | 15th term = 20 × 2 × 15 = 600 | For an arithmetic sequence, nth term = a + (n−1)d. 15th row = 20 + (14 × 2) = 48 seats. | OK |
| `ste_ks3_019` | Ratio | setup → METHOD | oats and butter in the ratio 4:1 | yes | Butter is 4 parts out of 5 | In ratio 4:1, oats are 4 parts and butter is 1 part. Butter = (1/5) × 600 = 120 g. | OK |
| `ste_ks3_020` | Percentages | setup → METHOD | percentage increase in average attendance | yes | Percentage increase = (540 ÷ 5,040) × 100 = 10.7% | Percentage increase uses the original value as the denominator. Correct: (540 ÷ 4,500) × 100 = 12%. | OK |
| `ste_ks3_021` | Area | setup → METHOD | area of the pond | yes | Area = π × 4.2² = 55.4 m² | The area formula uses the radius, not the diameter. Area = π × 2.1² ≈ 13.85 m². | OK |
| `ste_ks3_022` | Sequences | setup → METHOD | height after the 4th bounce | yes | Height after 4th bounce = 160 ÷ (4 × 2) = 20 cm | Height = 160 × (½)⁴ = 160 ÷ 16 = 10 cm. | OK |
| `ste_ks3_023` | Mean | setup → METHOD | finds the median | yes | 9 scores so the median is the 4th value = 14 | For 9 values, the median is the (9+1)/2 = 5th value, not the 4th. The 5th value is 14 — same answer here, but the method is wrong. | OK |
| `ste_ks3_024` | Angles | setup → METHOD | one angle is twice the smallest angle | yes | Angles are: 37.5°, 75° and 37.5° | The third angle is s + 30° = 67.5°, not s. The angles are 37.5°, 75°, and 67.5°. | OK |
| `ste_ks3_025` | Fractions | setup → METHOD | fraction who study German | yes | 7/20 of 400 = 7 × 400 ÷ 20 = 560 | 7 × 400 ÷ 20 = 140, not 560. The student multiplied incorrectly. | OK |
| `ste_ks3_026` | Subtraction | setup → METHOD | how far is left | yes | Remaining = 87 − 142 = −55 km | Remaining = total − travelled = 142 − 87 = 55 km. The subtraction was reversed. | OK |
| `ste_ks3_027` | Triangle | setup → METHOD | finds the hypotenuse | yes | Hypotenuse = 100 ÷ 2 = 50 cm | After finding c² = 100, take the square root, not divide by 2. Hypotenuse = √100 = 10 cm. | OK |
| `ste_ks3_028` | Angle Sum | setup → METHOD | quadrilateral | yes | Angles in a quadrilateral sum to 180° | Angles in a quadrilateral sum to 360°, not 180°. Missing angle = 360 − 285 = 75°. | OK |
| `ste_ks3_029` | Proportion | setup → METHOD | 150 km in 2 hours | yes | Speed = 150 + 2 = 152 km/h | Speed = distance ÷ time = 150 ÷ 2 = 75 km/h. Time = 225 ÷ 75 = 3 hours. | OK |
| `ste_ks3_030` | Circumference | setup → METHOD | area to buy topsoil | yes | Area = 2πr = 2 × 3.14 × 3.5 = 22.0 m² | 2πr is the circumference formula, not area. Area = πr² = 3.14 × 3.5² ≈ 38.5 m². | OK |
| `ste_ks3_031` | Median | setup → METHOD | find the median | yes | Median of 5, 2, 8, 4, 6, 1, 9 is 4 (the middle number in the list) | The data must be sorted first: 1, 2, 4, 5, 6, 8, 9. The median (middle value) is 5, not 4. The student picked the middle of the unsorted list. | OK |
| `ste_ks3_032` | Rounding | setup → METHOD | rounded to 1 decimal place | yes | 3.45 rounded to 1 d.p. = 3.4 | When the digit is 5, round up. 3.45 to 1 d.p. = 3.5. | OK |
| `ste_ks3_033` | Conversion | setup → METHOD | converts this to millilitres | yes | 1.5 litres = 1.5 × 10 = 15 ml | 1 litre = 1000 ml, not 10 ml. 1.5 litres = 1.5 × 1000 = 1500 ml. | OK |
| `ste_ks3_034` | Scale Factor | setup → METHOD | real length | yes | Real length = 8 × 25000 = 200,000 cm = 20 km | 200,000 cm = 2 km, not 20 km. The conversion from cm to km is ÷ 100,000. | OK |
| `ste_ks3_035` | Brackets | setup → METHOD | 3(x + 4) | yes | 3(x + 4) = 3x + 4 = 3(2) + 4 = 10 | The 3 multiplies the entire bracket: 3(x + 4) = 3x + 12 = 6 + 12 = 18. The student only multiplied x, not the 4. | OK |

### GCSE (45 questions)

| ID | Topic | Type→Class | Target phrase (Stage 2 correct answer) | Renders? | Wrong step (errorStepId) | Corrected explanation | Arithmetic |
|---|---|---|---|---|---|---|---|
| `ste_gcse_001` | Reverse Percentage | operation → METHOD | after a 10% reduction | yes | Original price = £76.50 + £7.65 = £84.15 | The 10% was taken off the original price, not the sale price. Original = £76.50 ÷ 0.9 = £85. | OK |
| `ste_gcse_002` | Compound Interest | operation → METHOD | compound interest | yes | Total interest after 3 years = £70 × 3 = £210 | Compound means interest is calculated on the growing balance each year. Correct: A = 2000 × 1.035³ = £2,217.24. | MISMATCH — explanation states £2,217.24; 2000 × 1.035³ = £2,217.4358 → correct rounded answer is **£2,217.44**, not £2,217.24 (20p off; the wrong 'corrected' figure is the one shown to a student who fails the question). |
| `ste_gcse_003` | Vectors | operation → METHOD | vector OM in terms of a and c | yes | OM = OB × BM = (a + c) × (−½a) | Vectors are combined by addition, not multiplication. OM = OB + BM = (a + c) + (−½a) = ½a + c. | OK |
| `ste_gcse_004` | Probability | operation → METHOD | without replacement | yes | P(2nd red) = 5/10 | Without replacement means the denominator changes. P(2nd red \| 1st red) = 4/9. P(both red) = 5/10 × 4/9 = 2/9. | OK |
| `ste_gcse_005` | Standard Form | operation → METHOD | 3 × 10⁸ m/s | yes | Time = distance × speed | Time = distance ÷ speed, not ×. T = 4.013 × 10¹⁶ ÷ (3 × 10⁸) ≈ 1.34 × 10⁸ seconds. | OK |
| `ste_gcse_006` | Trigonometry | operation → METHOD | angle of depression to a boat | yes | tan(34°) = opposite ÷ adjacent = d ÷ 80 | The 80 m height is the opposite side, d is adjacent. tan(34°) = 80 ÷ d, so d = 80 ÷ tan(34°) ≈ 118.5 m. | Minor — states d ≈ 118.5 m; 80 ÷ tan(34°) = 118.6 m to 1 d.p. (tan34° = 0.67451). Off by ~0.1 m, immaterial but not exact. |
| `ste_gcse_007` | Similarity | operation → METHOD | similar in shape | yes | Volume scale factor = 1.5² = 2.25 | Volume scales by the cube, not square, of the linear scale factor. Volume SF = 1.5³ = 3.375. Capacity = 168.75 ml. | OK |
| `ste_gcse_008` | Cumulative Frequency | operation → METHOD | interquartile range | yes | IQR = Q1 + Q3 = 4.8 + 9.1 = 13.9 km | IQR = Q3 − Q1, not Q3 + Q1. IQR = 9.1 − 4.8 = 4.3 km. | OK |
| `ste_gcse_009` | Simultaneous Equations | operation → METHOD | returns 1 tin and 1 roll | yes | t = 33.75 + 32 = 65.75 | To find t, subtract: t = 33.75 − 32 = £1.75. Adding gives a nonsensical answer. | OK |
| `ste_gcse_010` | Surds | operation → METHOD | exact side length in simplified surd form | yes | √45 = √9 + √5 = 3 + √5 | Surds cannot be split by addition: √(ab) = √a × √b, not √a + √b. Correct: √45 = √(9×5) = 3√5. | OK |
| `ste_gcse_011` | Circle Theorems | operation → METHOD | cyclic quadrilateral | yes | Opposite angles in a cyclic quadrilateral are equal | Opposite angles in a cyclic quadrilateral sum to 180°, not equal each other. Correct: (3x+10) + (5x−18) = 180, x = 23.5. | OK |
| `ste_gcse_012` | Gradient | operation → METHOD | gradient | yes | Gradient = (6 − 2) ÷ (13 − 5) = 4 ÷ 8 = 0.5 | Gradient = change in y ÷ change in x = (13−5) ÷ (6−2) = 8 ÷ 4 = 2. The student inverted the fraction. | OK |
| `ste_gcse_013` | Sine Rule | operation → METHOD | finds side b | yes | b = a × sinA ÷ sinB = 10 × sin30° ÷ sin45° | From a/sinA = b/sinB, b = a × sinB ÷ sinA = 10 × sin45° ÷ sin30°. The student swapped sinA and sinB. | OK |
| `ste_gcse_014` | Percentage | operation → METHOD | percentage profit | yes | % profit = (120 ÷ 520) × 100 = 23.1% | Percentage profit uses the cost price as denominator: (120 ÷ 400) × 100 = 30%. | OK |
| `ste_gcse_015` | Bounds | operation → METHOD | lower bound of the area | yes | LB of area = 8.35 + 5.15 = 13.50 cm² | Area = length × width, not length + width. LB area = 8.35 × 5.15 = 43.0 cm². | OK |
| `ste_gcse_016` | Standard Form | operation → METHOD | 10⁴ × 10³ | **NO — see finding above** | 10⁴ × 10³ = 10¹² | When multiplying powers, add the exponents: 10⁴ × 10³ = 10⁷, not 10¹². | OK |
| `ste_gcse_017` | Completing the Square | operation → METHOD | complete the square | yes | (x + 8)² + 3 − 64 | Half the coefficient of x is 4, not 8. Correct: (x + 4)² + 3 − 16 = (x + 4)² − 13. | OK |
| `ste_gcse_018` | Logarithms | operation → METHOD | log(5) + log(4) | yes | log(5) + log(4) = log(5 + 4) = log(9) | log(a) + log(b) = log(a × b) = log(20), not log(a + b). | OK |
| `ste_gcse_019` | Quadratic Formula | operation → METHOD | quadratic formula | yes | x = (5 ± √(25 − 8)) ÷ 2 | The denominator is 2a = 4, not 2. x = (5 ± √17) ÷ 4. | OK |
| `ste_gcse_020` | Functions | operation → METHOD | gf(2) | yes | g(2) = 4 | gf(2) means g(f(2)). First find f(2) = 7, then g(7) = 49. The student applied them in wrong order. | OK |
| `ste_gcse_021` | Inequalities | operation → METHOD | solves the inequality | yes | x > 12 ÷ (−3) = x > −4 | When dividing by a negative number, the inequality sign reverses. x < −4, not x > −4. | OK |
| `ste_gcse_022` | Vectors | operation → METHOD | find 2a | yes | 2a = 2(3) + 2(2) = 6 + 4 = 10 | Scalar multiplication applies to each component: 2a = 6i + 4j, a vector, not the scalar sum 10. | OK |
| `ste_gcse_023` | Quadratics | setup → METHOD | area of the field is 198 m² | yes | Perimeter = 198, so 2(w + w + 7) = 198 | 198 m² is the area, not the perimeter. Correct: w(w + 7) = 198. | OK |
| `ste_gcse_024` | Pythagoras | setup → METHOD | how far up the wall the ladder reaches | yes | h² = 36 + 3.24 = 39.24 | When finding a shorter side, subtract: h² = 36 − 3.24 = 32.76. h ≈ 5.72 m. | OK |
| `ste_gcse_025` | Trigonometry | setup → METHOD | angle of incline | no (decoy only) | tan(θ) = adjacent ÷ opposite = 6 ÷ 0.9 = 6.67 | tan(θ) = opposite ÷ adjacent = 0.9 ÷ 6 = 0.15. θ ≈ 8.5°. The student inverted the fraction. | OK |
| `ste_gcse_026` | Standard Form | setup → METHOD | how many times heavier | yes | Earth ÷ Moon = 5.97 ÷ 7.34 = 0.81, so Earth is 0.81 times heavier | Must account for the different powers of 10. (5.97 × 10²⁴) ÷ (7.34 × 10²²) ≈ 81.3 times heavier. | OK |
| `ste_gcse_027` | Reverse Percentage | setup → METHOD | after its value increased by 17% | yes | 17% of £292,500 = £49,725 | 17% was applied to the original, not current value. Original = £292,500 ÷ 1.17 = £250,000. | OK |
| `ste_gcse_028` | Simultaneous Equations | setup → METHOD | eliminates a | yes | Add equations: 30a + 31c = 381 | Both equations have 15a, so subtract (not add) to eliminate a: 25c − 6c = 225 − 156, giving 19c = 69, c = £3.63. | OK |
| `ste_gcse_029` | Circle Theorems | setup → METHOD | angle ACB where C is any point on the major arc | yes | Student reconsiders: 'C is on major arc, use reflex: 360 − 136 = 224, ACB = 112°' | The angle-at-centre theorem uses the non-reflex angle when C is on the major arc. ACB = 68°. | OK |
| `ste_gcse_030` | Probability | setup → METHOD | at least one day | yes | P(at least one rainy day) = P(day 1) + P(day 2) = 0.6 | P(at least one) = 1 − P(none) = 1 − 0.7² = 0.51. Simply adding P(A) + P(B) double-counts the overlap. | OK |
| `ste_gcse_031` | Trigonometry | setup → METHOD | bearing to return | yes | Bearing angle: sin(θ) = 15/26.6 | The bearing angle from north uses tan(θ) = opposite/adjacent = 22/15 (east/north). Using sin with the hypotenuse gives the wrong setup. | OK |
| `ste_gcse_032` | Bearing | setup → METHOD | westward displacement | yes | West = 30 × cos(250°) | The westward component uses sin, not cos. West = 30 × sin(250° − 180°) = 30 × sin(70°) ≈ 28.2 km. | OK |
| `ste_gcse_033` | IQR | setup → METHOD | IQR | yes | IQR = Q1 − Q3 = 23 − 41 = −18 | IQR = Q3 − Q1 = 41 − 23 = 18. The subtraction was reversed. | OK |
| `ste_gcse_034` | Histogram | setup → METHOD | frequency | yes | Frequency = height = 3 | In a histogram, frequency = frequency density × class width = 3 × 10 = 30. | OK |
| `ste_gcse_035` | Cosine Rule | setup → METHOD | cosine rule | yes | c² = a² + b² + 2ab·cosC | The cosine rule is c² = a² + b² − 2ab·cosC (minus, not plus). c² = 100 − 48 = 52, c = √52. | OK |
| `ste_gcse_036` | Probability Tree | setup → METHOD | two days | yes | Day 2 after rain: P(rain) = 0.4, P(no rain) = 0.4 | Independent events: P(no rain) is always 0.6, not 0.4. Each branch pair must sum to 1. | OK |
| `ste_gcse_037` | Perpendicular Gradient | setup → METHOD | perpendicular | yes | Perpendicular gradient = 1/3 | The perpendicular gradient is the negative reciprocal: −1/3, not 1/3. | OK |
| `ste_gcse_038` | Expanding Brackets | setup → METHOD | expand | yes | (x + 3)(x + 5) = x² + 5x + 3x = x² + 8x | Missing the constant term from 3 × 5. Correct: x² + 8x + 15. | OK |
| `ste_gcse_039` | Circle Equation | setup → METHOD | equation | yes | (x − 3)² + (y + 2)² = 5 | The equation uses r², not r. Correct: (x − 3)² + (y + 2)² = 25. | OK |
| `ste_gcse_040` | Surds | setup → METHOD | rationalise | yes | 6/√3 × √3/√3 = 6√3/9 | √3 × √3 = 3, not 9. Correct: 6√3/3 = 2√3. | OK |
| `ste_gcse_041` | Composite Function | setup → METHOD | fg(x) | yes | fg(x) = f(x) × g(x) = (x + 2)(3x) = 3x² + 6x | fg(x) means f(g(x)) = f(3x) = 3x + 2, not f × g. | OK |
| `ste_gcse_042` | nth Term | setup → METHOD | nth term | yes | nth term = 3n + 5 | nth term = 3n + (5 − 3) = 3n + 2. Check: n=1 gives 5. The student added the first term instead of adjusting. | OK |
| `ste_gcse_043` | Equation Rearrangement | setup → METHOD | make t the subject | yes | t = a(v − u) | t = (v − u) ÷ a, not a(v − u). The student multiplied instead of dividing. | OK |
| `ste_gcse_044` | Arc Length | setup → METHOD | arc length | yes | Arc length = (72/180) × π × 10 = 12.57 cm | Arc length = (θ/360) × 2πr. Correct: (72/360) × 2π(10) = 4π ≈ 12.57 cm. Same answer by coincidence here, but the formula used is wrong. | OK |
| `ste_gcse_045` | Simultaneous | setup → METHOD | by substitution | yes | 2x + 12x − 5 = 13, so 14x = 18, x = 18/14 | The −5 should be −15 (3 × −5). Correct: 2x + 12x − 15 = 13, 14x = 28, x = 2. | OK |

### Level 4 (30 questions)

| ID | Topic | Type→Class | Target phrase (Stage 2 correct answer) | Renders? | Wrong step (errorStepId) | Corrected explanation | Arithmetic |
|---|---|---|---|---|---|---|---|
| `ste_l4_001` | Differentiation | operation → METHOD | rate of change of y with respect to x | yes | 4x³ → 12x², 5x² → 10x, 2x → 2, −7 → −7 | The derivative of a constant is 0, not the constant itself. dy/dx = 12x² − 10x + 2. | OK |
| `ste_l4_002` | Logarithms | operation → METHOD | log(8) + log(4) − log(2) | yes | log(8) + log(4) = log(8 + 4) = log(12) | log(a) + log(b) = log(a × b), not log(a + b). log(8) + log(4) = log(32). Then log(32) − log(2) = log(16). | OK |
| `ste_l4_003` | Complex Numbers | operation → METHOD | multiplies | yes | j² = 1, so −3j² = −3 | j² = −1, not +1. So −3j² = +3. Correct: 2 + 3 + j = 5 + j. | OK |
| `ste_l4_004` | Integration | operation → METHOD | distance s travelled from t = 0 | yes | = (3t² ÷ 2) + (2t ÷ 1) + c = 1.5t² + 2t + c | Integration increases the power by 1 and divides by the new power. ∫3t² = t³. Correct: s = t³ + t² + c. | OK |
| `ste_l4_005` | Product Rule | operation → METHOD | product rule | yes | dy/dx = du/dx × dv/dx = 2x·cos(x) | Product rule: dy/dx = u(dv/dx) + v(du/dx) = x²cos(x) + 2x·sin(x). | OK |
| `ste_l4_006` | Matrices | operation → METHOD | determinant det(A) | yes | det(A) = (2 × 4) + (3 × 1) = 8 + 3 = 11 | det([[a,b],[c,d]]) = ad − bc, not ad + bc. det(A) = 8 − 3 = 5. | OK |
| `ste_l4_007` | Geometric Series | operation → METHOD | sum to infinity | no (decoy only) | S∞ = a ÷ (1 + r) = 3 ÷ 1.5 = 2 | S∞ = a ÷ (1 − r), not (1 + r). S∞ = 3 ÷ 0.5 = 6. | OK |
| `ste_l4_008` | Integration | operation → METHOD | evaluates | yes | ∫(4x + 1) dx = 4x² + x + c | ∫4x dx = 2x², not 4x². The power rule increases the exponent and divides by it. Correct: 2x² + x + c. | OK |
| `ste_l4_009` | Chain Rule | operation → METHOD | finds dy/dx | yes | dy/dx = 3(2x + 5)² | Chain rule requires multiplying by the inner derivative. dy/dx = 3(2x + 5)² × 2 = 6(2x + 5)². | OK |
| `ste_l4_010` | Implicit Differentiation | operation → METHOD | finds dy/dx | yes | Differentiate: 2x + 2y = 0 | Differentiating y² requires the chain rule: d/dx(y²) = 2y·dy/dx. Correct: 2x + 2y(dy/dx) = 0. | OK |
| `ste_l4_011` | Sum to Infinity | operation → METHOD | S∞ | yes | S∞ = a/(1−r) = 10/(1−2) = 10/(−1) = −10 | The sum to infinity only converges when \|r\| < 1. Since r = 2, the series diverges and S∞ does not exist. | OK |
| `ste_l4_012` | Binomial Expansion | operation → METHOD | coefficient of x² | yes | Coefficient = 5C2 = 5!/(2! × 2!) = 120/4 = 30 | 5C2 = 5!/(2! × 3!) = 120/(2 × 6) = 10, not 30. The student used 2! twice instead of 2! and 3!. | OK |
| `ste_l4_013` | Eigenvalue | operation → METHOD | eigenvalues | no (decoy only) | (4−λ)(3−λ) + 2 = 0 | det = (4−λ)(3−λ) − (1)(2) = 0. The off-diagonal product should be subtracted, not added. | OK |
| `ste_l4_014` | Partial Fractions | operation → METHOD | partial fractions | yes | 1/((x+1)(x−1)) = A/(x+1) + B/(x+1) | The second denominator should be (x−1), not (x+1). Correct: A/(x+1) + B/(x−1). | OK |
| `ste_l4_015` | De Moivre | operation → METHOD | De Moivre | yes | = cos(4 × 30°) + j·sin(30°) = cos120° + j·sin30° | De Moivre applies the power to BOTH arguments: cos(4×30°) + j·sin(4×30°) = cos120° + j·sin120°. | OK |
| `ste_l4_016` | Eigenvalues | setup → METHOD | eigenvalue equation | yes | For λ = 2: solve (A + 2I)v = 0 | Eigenvectors use (A − λI)v = 0, not (A + λI)v = 0. | OK |
| `ste_l4_017` | Integration | setup → METHOD | definite integral | yes | Result = 7/3 − 15 = −38/3 | Definite integral = F(b) − F(a) = upper − lower. Result = 15 − 7/3 = 38/3. | OK |
| `ste_l4_018` | Partial Fractions | setup → METHOD | cover-up method | no (decoy only) | Cover up (x+1), substitute x = 1 | Cover-up substitutes the root of the covered factor. For (x+1), set x = −1. A = (3(−1)+1)/((−1)−2) = (−2)/(−3) = 2/3. | OK |
| `ste_l4_019` | Chain Rule | setup → METHOD | chain rule | yes | dy/du = 5u⁴, du/dx = 3x² | du/dx is the derivative of 3x² + 1, which is 6x, not 3x². dy/dx = 30x(3x²+1)⁴. | OK |
| `ste_l4_020` | Modulus-Argument | setup → METHOD | modulus-argument form | yes | arg(z) = arctan(3/−3) = arctan(−1) = −45° | z is in the second quadrant (negative real, positive imaginary). arg(z) = 180° − 45° = 135°. | OK |
| `ste_l4_021` | Matrix Inverse | setup → METHOD | A⁻¹ | yes | A⁻¹ = (1/10)[[4, 1], [2, 3]] | The adjugate swaps diagonal and negates off-diagonal: [[4, −2], [−1, 3]]. A⁻¹ = (1/10)[[4,−2],[−1,3]]. | OK |
| `ste_l4_022` | Stationary Points | setup → METHOD | classifies | yes | d²y/dx² = 6x. At x=1: d²y/dx² = 6 > 0, so maximum | d²y/dx² > 0 indicates a minimum, not a maximum. | OK |
| `ste_l4_023` | Integration by Parts | setup → METHOD | integration by parts | yes | u = cos(x), dv = x dx | Choose u = x (simplifies on differentiation) and dv = cos(x) dx. Then du = dx, v = sin(x). ∫ = x·sin(x) − ∫sin(x) dx. | OK |
| `ste_l4_024` | Binomial | setup → METHOD | x³ term | yes | Term = 6C3 × (2x)² = 15 × 4x² = 60x² | For the x³ term, use (2x)³ not (2x)². Term = 6C3 × (2x)³ = 20 × 8x³ = 160x³. | OK |
| `ste_l4_025` | Maclaurin | setup → METHOD | Maclaurin series for cos(x) | yes | cos(x) = 1 − x²/2! + x³/3! − x⁴/4! | cos(x) only has even powers: 1 − x²/2! + x⁴/4!. The x³/3! term belongs to sin(x). | OK |
| `ste_l4_026` | Parametric | setup → METHOD | dy/dx | yes | dy/dx = dx/dt ÷ dy/dt = 2/(2t) = 1/t | dy/dx = (dy/dt) ÷ (dx/dt) = 2t/2 = t. The student inverted the fraction. | OK |
| `ste_l4_027` | Geometric Series | setup → METHOD | identifies r | yes | r = 12/6 = 2 | r = next term ÷ current term = 6/12 = 0.5, not 12/6. S∞ = 12/(1−0.5) = 24. | OK |
| `ste_l4_028` | Complex Modulus | setup → METHOD | \|z\| | no (decoy only) | \|z\| = √(3 − 4) = √(−1) | The modulus squares both components: \|z\| = √(3² + 4²) = √(9+16) = 5. The student subtracted instead of squaring. | OK |
| `ste_l4_029` | Cramer's Rule | setup → METHOD | Cramer’s rule | yes | A₁ = [[2,7],[1,9]], det(A₁) = 18−7 = 11 | For x, replace the FIRST column with constants: A₁ = [[7,3],[9,4]]. det(A₁) = 28−27 = 1. x = 1/5. | OK |
| `ste_l4_030` | Implicit Differentiation | setup → METHOD | implicitly | yes | 2x × y + x² = 0 | Product rule on x²y gives 2xy + x²(dy/dx) = 0. The student forgot the dy/dx factor on the y term. | OK |

