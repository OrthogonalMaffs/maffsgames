# Audit: answer precision, level routing, bank attribution

Read-only audit, 2 Oct 2026, for to-do §1.35 and §1.36. It measures three bug classes across every game
so that their shared fixes (a precision marker in `schools/assets/`, the leaderboard coverage check and
the bank extractor) can be scoped against the true set. **It fixes nothing.** No game, script, ledger,
allowlist or workflow file was changed.

- **Base.** Measured on `main` at `bc51fef` and published on `65ea1d5`. No file under `games/`,
  `leaderboards/`, `scripts/extract-banks.py` or `scripts/check-leaderboard-coverage.js` changed
  between the two, so every line number below holds on `65ea1d5`.
- **History.** The audit stopped once at the contract's STOP IF ("any game rejects a right answer at the
  asked precision"). Jon waived it for completion only, on 2 Oct 2026.
- **How it was measured.** Keys were checked mechanically with node and Python scripts that load each
  game's own bank and marking code from the file. True values were recomputed from each question's
  own parameters, with SymPy, exact rationals or 50-digit decimals where it mattered. The scripts ran in
  the session scratchpad and are **not** in the repo. Each finding names the lines it depends on, so it
  can be re-run by hand.
- **No page was loaded against the live site, Firebase or the analytics endpoint.** Section 3's
  extraction ran `scripts/extract-banks.py` unchanged against the local stub server, on an exported copy
  of the repo (`git archive`), with KaTeX served locally as in `docs/sandbox-checks.md`. Summary:
  "82 bank (live), 1 bank (static fallback), 13 generator", which is the trusted result.

**Two labels are used on every rejection:**

- **recomputed at source**: re-read and recomputed independently in this session, after the sub-check
  that first found it.
- **reported, not re-checked**: found and computed by a sub-check (a delegated audit of a group of games,
  working from the same rubric), and not independently repeated. Each has its quoted line.

---

## 1. Precision

### 1.0 The set: 26 typed-answer games

**How it was found:** `grep -n "<input"` over every `games/*/index.html`, filtered by hand to answer
inputs. That drops range sliders (`trig-wars`), checkboxes (`equatle`, `log-laws`) and name or initials
boxes (`52dle:656`, `estimation-engine:216`, `prime-or-composite:224`, `six-sevens-bruv:658`,
`equatle:257`). To that were added `createElement('input')` (`given-that:765`, `like-terms-collector:378`)
and on-screen keypads, found by grepping for `keypad`/`numpad` and keyboard digit handlers.

**The 26:** 52dle, chart-interrogator, component-crusher, equatle, estimation-engine, estimation-golf,
factor-theorem, fermi-lab, formula-plug-in, given-that, glorious-gantt, graph-sketcher,
growth-and-decay, like-terms-collector, log-laws, new-shapes, percentage-flip, quadratic-factoriser,
screening-room, six-sevens-bruv, split-it, stat-attack, suvat, tax-theft, test-the-claim,
think-of-a-number.

**Out of scope:** `the-perfect-prank` (unlisted prototype), `regression-rumble` (withdrawn) and the
escape rooms (their locks are integer-exact and checked by `check-escape-rooms.py`).

**Input types.** 15 of the 26 read at least one answer through `type="number"`: 52dle,
chart-interrogator, component-crusher, estimation-engine, estimation-golf, glorious-gantt,
graph-sketcher, growth-and-decay, like-terms-collector, percentage-flip, split-it, stat-attack, suvat,
tax-theft and test-the-claim. There the browser yields an empty value for "£12.30", "1,009" or "2√5",
and most of those games then `return` silently, with no feedback.
- 6 read only text: factor-theorem, fermi-lab, given-that, log-laws, quadratic-factoriser's formula
  level and screening-room.
- 5 are on-screen keypads: equatle, formula-plug-in, new-shapes, six-sevens-bruv and
  think-of-a-number.

**Tolerance as game mechanic.** In three games the band *is* the game, and the screen says so:
estimation-engine ("Within {tol}%", `:307`), estimation-golf (golf-score bands, `:694–702`) and
fermi-lab (factor bands and a final rating, `:444–463`). They are covered below, but their bands are not
precision-marking defects.

### 1.1 Summary per game

**Key:**
- (c) accepts a wrong answer at the asked precision;
- (d) rejects a right answer at the asked precision, or rejects the exact right answer;
- (e) a key disagrees with its own stem;
- (f) a key is computed from values not on screen;
- (g) feedback shows the key at another precision.

| Game | Typed items checked | Precision asked | Marking rule | (c) | (d) | (e) | (f) | (g) |
|---|---|---|---|---|---|---|---|---|
| growth-and-decay | 120 sub-questions | 3 s.f. mostly; 2 s.f., 4 s.f., 1 d.p. | sq1 2% + 0.01, sq3 0.5% (min 0.05) `:754`; sq4 ±0.15 `:793` | yes | **yes, 4** | yes, 14 | yes | yes, 10 |
| stat-attack | 36 scenarios, 181 table rows | mean and SD 3 s.f.; variance unstated | mean ±0.15 `:964`; variance ±max(0.5, 0.5%) `:1152`; SD ±max(0.1, 1%) `:1180`; class string `:1329–1334` | yes | **yes, 19** | yes | yes | yes |
| test-the-claim | 48 items | z and normal CV 2 d.p.; p 4 d.p. | z ±0.02 `:1649`; CV <0.002 `:1679–1689`; corr CV <0.001 `:1669`; p ±0.006 `:1709` | yes | **yes, 12** | no | trivial | yes |
| component-crusher | 92 sub-questions | 2 d.p., 1 d.p., 3-figure bearing, surd | `Math.abs(val-sq.answer)<=tol` `:724`; vectors `:710` | yes | **yes, 2** | yes | **yes, L4** | yes |
| graph-sketcher | 167 cells, 57 interpretation items | unstated | cells `:675–677`; read/extrap `:1024–1027` | yes | **yes, 8 (wrong keys)** | wrong keys only | CM3 | no |
| glorious-gantt | 262 keys | whole days, implied | `parseInt` then `===` `:967–1189` | yes (truncation) | **yes, 6 (wrong keys)** | no | drawn network ≠ table | no |
| tax-theft | 104 steps | unstated; whole pounds keyed | `Math.round(expected)` ±£1/£2 `:1040–1042` | yes | **yes, 6 salaries (wrong key)** | via that defect | yes (NI etc.) | no |
| screening-room | 70 items | unstated; fraction, decimal or % | ±0.005 or 1.5% `:774–782` | yes | **yes, 9 (comma parse)** | no | no | yes |
| factor-theorem | 75 steps, 20 finals, 27 test parts | exact form | exact string `:873–881`, `:981`, `:1090–1092` | yes | **yes (form, order, 1 wrong key)** | 1 wrong key | no | no |
| fermi-lab | 189 steps, 65 ratings | factor bands (mechanic) | `withinFactor` `:444–449`; `getFinalRating` `:457–463` | by design | **yes, 17 (model answer rated Poor)** | yes `:339` | yes | no |
| split-it | full generator ranges | unstated; money implied 2 d.p. | ±0.05 `:543`, `:515`; ±0.15 `:536`, `:538` | yes | U only | no | no | yes |
| given-that | 130 phase answers | unstated | ±0.005 `:842` | yes | U only | no | no | no |
| chart-interrogator | 160 Phase 1 + 10 Phase 2 | unstated | `:864`, `:1092–1093`; stem and leaf exact `:686` | yes | U only (by ruling) | no | by design | yes |
| suvat | 18 + 62 + 8 steps | **never stated** | `:666–667`, `:792`, `:908` | yes | U only (AL34 sign) | yes (L4_8) | harmless | n/a |
| estimation-golf | 56 | 6 stems state one | proximity bands `:808–813` | by design | no | yes `:663`, `:666` | yes `:680` | yes |
| estimation-engine | 49 | "Within n%" | relative band `:386–388` | by design | no | yes `:276` | no | inherits `:276` |
| log-laws | 418 | 3 s.f., on screen | `Number(raw)` vs `r3(answer)` `:1866–1874` | spelling only | no | no | no | no |
| quadratic-factoriser | 1070 formula items + pickers | 2 d.p. (start screen only) | input rounded, then compared `:1034–1038` | yes (over-precise) | no | no | no | no |
| percentage-flip | 32 | unstated; integers | `<0.01` `:262`, `:287` | trivially | no | no | no | no |
| like-terms-collector | 15 | unstated; integers | `parseInt` `:415–424` | yes (truncation) | no | no | no | no |
| formula-plug-in | 50 | unstated; integers | `parseFloat ===` `:512–517` | no | no | no | no | no |
| new-shapes | 50 | unstated; integers | `parseFloat ===` `:832–833` | no | no | no | no | no |
| think-of-a-number | 50 | integer | `parseInt ===` `:588–589` | no | no | no | no | no |
| six-sevens-bruv | 78 facts, 408 forms | integer | `parseInt ===` `:803–804` | no | no | no | no | no |
| 52dle | 20 | integer | `parseInt` then `===` `:899`, `:908` | yes (52.9 wins 52) | no | no | no | no |
| equatle | 23,399 targets | N/A (integer equations) | exact tile match `:658` | no | no | no | no | no |

### 1.2 Every right answer marked wrong

Each item gives the ask, the key, the true value, the rule and why it rejects. The groups are ordered by
severity: a stated precision first, then a wrong key, then a correct value in a form the game cannot
parse, then where no precision is stated.

#### (i) Rejected at a precision the question states

1. **growth-and-decay AL3 sq4** `:368`, "Find T when L = 75. Give your answer to 3 significant figures."
   - Key `25.2`. True ln(180/75)/0.035 = 25.0134, so **25.0**.
   - Rule `Math.abs(val-sq.answer)<=0.15` (`:793`). |25.0 − 25.2| = 0.20, **rejected**.
   - The game's own hint evaluates to 25.01. **recomputed at source.**
2. **growth-and-decay L4_2 sq4** `:482`, "Find t when T = 50. … 3 significant figures."
   - Key `21.2`. True ln(160/30)/0.08 = 20.9247, so **20.9**.
   - Rule ±0.15 (`:793`); diff 0.30, **rejected**. **recomputed at source.**
3. **growth-and-decay L4_14 sq4** `:578`, "Find T when H = 500. … 3 significant figures."
   - Key `211`. True ln(500/k)/0.022 = 210.14 with k = 4.911 (stated, `:574`), 210.15 with the sq3
     answer 4.91, and 210.14 with the exact k. So **210**.
   - Rule ±0.15; diff 1, **rejected** under every k. **recomputed at source.**
4. **growth-and-decay CM2 sq3** `:224`, "Given that L = 100 when T = 24, find the value of k. Give your
   answer to 1 decimal place."
   - Key `161.2`. True 100/0.98²⁴ = 162.3956, so **162.4**.
   - Rule `Math.max(0.005*|key|,0.05)` = ±0.806 (`:754`); diff 1.20, **rejected**.
   - The hard-coded `graphFn` (`:218`) uses 161.2 too, and so the CM2 sq1 key (87.9, true 88.6) is
     built from it. That one is accepted inside the 2% band. **recomputed at source.**
5. **test-the-claim, normal critical value**, label "Critical value (2 d.p.)" (`:1603`), placeholder
   `e.g. 1.6449` (`:1604`).
   - Rule `Math.abs(val - cv) < 0.002` against a 4 d.p. table value (`:1679`, `:1688–1689`).
   - The correctly rounded 2 d.p. value is rejected in 9 of 12 items:
     - N1 `:716`, N2 `:736`, N9 `:876`, N11 `:916` and N8 `:856`: **1.64**, since |1.64 − 1.6449| = 0.0049;
     - N4 `:776`, N6 `:816`: **2.33** against 2.3263;
     - N5 `:796`, N12 `:936`: **2.58** against 2.5758.
   - Accepted at 2 d.p.: N3, N7 and N10.
   - Normal items have no `crDirection`, so the two-tailed ones get one positive-only box.
   - **recomputed at source** for the rule and the 1.64/1.6449 case; the per-item list is **reported, not
     re-checked**.
6. **stat-attack, mean**, "Calculate an estimate of the mean. Give your answer to 3 significant figures."
   (`:952`).
   - Rule `Math.abs(val-q.mean)<=0.15` (`:964`), with keys stored to 4–5 s.f., so every mean of 100 or
     more rejects its 3 s.f. value.
   - G10 `:326`: true 106.25, so **106**, key 106.25, diff 0.25. **recomputed at source.**
   - Also, **reported, not re-checked** (true value → 3 s.f. answer, key):
     - G12 `:346`: 108.75 → 109, key 108.75.
     - CM2 `:374`: 190.42 → 190, key 190.4.
     - CM4 `:406`: 258.33 → 258, key 258.3.
     - CM5 `:422`: 223.33 → 223, key 223.3.
     - CM7 `:454`: 1141.67 → 1140, key 1141.7.
     - CM10 `:502`: 231.67 → 232, key 231.7.
     - CM11 `:518`: 2093.33 → 2090, key 2093.3.
     - CM12 `:534`: 169.17 → 169, key 169.2.
     - L4_2 `:568`: 349.2 → 349.
     - L4_5 `:616`: 502.5 → 503.
     - L4_6 `:632`: 222.48 → 222.
     - L4_8 `:664`: 249.2 → 249.
   - 13 scenarios in all.
7. **stat-attack, standard deviation**, "Calculate the standard deviation to 3 significant figures."
   (`:1168`). Rule `Math.abs(val-q.sd)<=Math.max(0.1,q.sd*0.01)` (`:1180`).
   - Each key is √ of a variance key that is not the data's variance (item 22), so the data's true SD is
     rejected:

     | Scenario | True σ | 3 s.f. | Key |
     |---|---|---|---|
     | G2 `:246` | 5.6532 | **5.65** | 5.19 |
     | G7 `:296` | 5.4097 | **5.41** | 5.55 |
     | CM3 `:390` | 9.1758 | **9.18** | 9.04 |
     | CM8 `:470` | 6.1146 | **6.11** | 6.3 |
     | L4_5 `:616` | √27 = 5.1962 | **5.20** | 4.33 |

   - **recomputed at source**, all five, from each scenario's own midpoints and frequencies.
   - In play the student meets step E (variance) first, and a correct variance is rejected there with no
     skip or reveal (item 22), so the student is stuck before reaching this step. Step F then displays
     `σ = √(key variance)` (`:1169`).
8. **stat-attack L4_7, modal and median class** (`:648–652`), key `'3.0 ≤ x < 4.0'`.
   - `parseInterval` (`:1329–1334`) compares digit strings, so the same class typed as `3 ≤ x < 4`
     (`'3_4'` against `'3.0_4.0'`) is rejected. **reported, not re-checked.**
9. **component-crusher AL5.2** `:321`, "Find |AB|. Give as simplified surd or decimal."
   - The asked surd form, **2√5**, cannot be entered: `type="number"` (`:691`), and `checkNum` returns
     silently on NaN (`:721`). The decimal 4.47 passes. **reported, not re-checked.**
10. **component-crusher AL11.2** `:364`, "Find the bearing of motion (3-figure)."
    - Key `143.1`, tol 0.5. v = 4i − 3j (`to:[4,-3]`, `:360`). Bearing 90° + arctan(3/4) = 126.87°, so
      **127**. Rejected (diff 16.1).
    - 143.1 is the bearing of 3i − 4j. **recomputed at source.**
11. **test-the-claim, correlation, lower tail.** C4 `:1009`, C8 `:1077` and C12 `:1145` define the region
    in their own `crExplanation` as `r ≤ −0.4000` / `−0.4409` / `−0.4622`.
    - Rule `Math.abs(val - q.criticalValue) < 0.001` (`:1669`) accepts only the positive value, so the
      boundary as stated is rejected. **reported, not re-checked.**

#### (ii) Wrong key: the exact right answer is rejected

12. **factor-theorem T4(b)** `:551`, p(x) = x³ + ax + b with a = −23, b = 42 (T4(a) `:550`); "Fully
    factorise p(x)."
    - Key `'(x-3)(x+7)(x-2)'` expands to x³ + 2x² − 29x + 42 ≠ p(x).
    - SymPy: p(x) = **(x − 3)(x² + 3x − 14)**. The only accepted answer is false, and the feedback teaches
      it. **recomputed at source.**
13. **graph-sketcher L4_14** `:564`, V = 12 sin(ωt + π/3), ω = 100π.
    - Keys `answers:{0.005:-10.39,0.015:10.39}`. True values **6** and **−6**; tol 0.5, both rejected.
    - A wrong table cell is never revealed and the table must be completed (`:681–693`), so a correct
      student cannot leave the table. **recomputed at source.**
14. **graph-sketcher**, further wrong keys, **reported, not re-checked**:
    - CM6 `:269`: x = 0.5 keyed 35.5, true **31.5**.
    - AL14 `:454`: x = −2 keyed −16, true **0**. Its given −59 at x = −3 is also wrong (true −41).
    - L4_5 `:499`: four cells; true **3.125, 3.375, 0.625, 0.875**.
    - CM1 `:225`: read keyed 40.8, true **38.31**.
    - CM1 `:226`: extrap keyed 8.7, true **7.7**.
    - CM2 `:235`: keyed 1.56, true **0.625**.
    - CM3 `:244`: asks for "the **year**", keys t = 14.2, so the year 2024 is rejected.
15. **glorious-gantt L4_A3** float E, key `floats:{E:15,…}` (`:459`).
    - From the activity table: E has ES 5, and LF = LS(F) = 23 − 3 = 20. So the float is **10**,
      rejected. **recomputed at source.**
16. **glorious-gantt**, further wrong keys, **reported, not re-checked**:
    - CM_A3 `:310`: float C keyed 7, true **4**.
    - L4_B2 `:683`: float E keyed 4, true **1**; float C keyed 5, true **8**.
    - L4_B2 `:664`: node 4 late keyed 12, true **15**.
    - CM_B2 `:552`: node 3 late keyed 6, true **9**.
17. **tax-theft, salaries over £100,000.** The basic band is `basicAmount = TAX_RULES.basicRateLimit -
    (pa > 0 ? pa : 0)` (`:885`). When the allowance tapers, that widens the band beyond HMRC 2025/26's
    £37,700 of taxable income.
    - £105,000: key **£29,932**, HMRC **£30,432** (**recomputed at source**). Rule ±£2 (`:1040–1042`).
    - **reported, not re-checked:** £118,000 (36,432 vs 38,232), £106,000 (30,432 vs 31,032),
      £114,000 (34,432 vs 35,832), £120,000 (37,432 vs 39,432) and £130,000 (42,189 vs 44,703).
    - The error carries into deductions and net. The page's band text (`:890`) teaches the key's method.
18. **fermi-lab**: a student whose every step equals the model value (or who presses "Skip (use model
    value)" on every step) is rated **Poor, 0 points, logged `correct:false`** in 17 of 65 questions.
    - The final rating compares the chain product (`:593–598`) with `acceptedAnswer` (`getFinalRating`,
      `:457–463`, called at `:621`). In these questions the chain is not the calculation behind
      `acceptedAnswer`.
    - **recomputed at source** for all 17, using the game's own chain and rating functions:

      | Question | Line | Factor off | Why |
      |---|---|---|---|
      | tennis-balls-classroom | `:310` | 41 | ball volume multiplied, should divide |
      | footballs-on-pitch | `:315` | 94 | |
      | words-spoken-day | `:329` | 29 | ×60 missing |
      | football-pitches-m25 | `:331` | 49 | |
      | household-electricity-kwh | `:334` | 1001 | Wh vs kWh |
      | molecules-swimming-pool | `:339` | 997 | `acceptedAnswer` itself is wrong |
      | blood-pumped-lifetime | `:346` | 1060 | mL vs L |
      | m25-concrete | `:355` | 1000 | |
      | forth-bridge-steel | `:356` | 1124 | |
      | eiffel-tower-bolts | `:358` | 3154 | |
      | hydro-dam-flow | `:359` | 178,808 | |
      | submarine-welds | `:360` | 97 | |
      | nuclear-cooling-water | `:363` | 5599 | |
      | eq_car_park | `:370` | 1349 | |
      | eq_steps | `:371` | 5000 | |
      | eq_coffee_cups | `:372` | 197,730 | |
      | eq_school_trip | `:377` | 160 | |

    - uk-trees `:327` and books-ever-published `:344` lose only the top band.
    - The results screen shows a "Model" column identical to the student's entries beside "Poor".
19. **suvat AL34** step 1 `:442–446`, "Find v_y (m/s)".
    - Key `0.32` (tol 0.3). True 30 sin 40° − 19.6 = **−0.3164**, and the game's own working says "−0.32".
      The correct answer is rejected.
    - No precision is stated anywhere in suvat, so this is a sign error in the key. **reported, not
      re-checked.**

#### (iii) A correct value in a form the game cannot read

20. **screening-room**, 9 items whose positives total is 1000 or more. The prompt prints the denominator
    with `numFmt` = `toLocaleString('en-GB')` (`:474–476`, `:712`), and the hint invites a fraction.
    - The exact fraction typed as shown, e.g. `10/1,009`, parses as 10/1 (`parseFloat` of "1,009" is 1,
      `:742–745`), so it is rejected.
    - The items: alevel_01 `:361`, alevel_03 `:363`, alevel_07 `:367`, alevel_11 `:371`, alevel_12 `:372`,
      alevel_18 `:378`, alevel_19 `:379`, core_04 `:386` and core_14 `:396`.
    - **recomputed at source** for the parse path; the item list is **reported, not re-checked**.
21. **factor-theorem, exact-string marking** (`:873–881`, `:981`, `:1090–1092`). **reported, not
    re-checked:**
    - `x^2` is rejected against a literal `x²` (`:358`, `:359`, `:380`, `:387`).
    - Factor order: 1 of 6 orderings is accepted, on 13 keys (`:475`–`:523`), e.g. Q21 `(x-2)(x-3)(x+4)`.
    - Root lists need the stored order and the `x=`/`θ=`/`ω=` prefix (Q23, Q29, Q30, Q34, Q37, Q40).
    - Test parts print a label (`x =`, `λ =`, `a, b =`) whose answer must repeat it (T1(c) `:534`, T3(d),
      T4(a), T5, T7(c), T8(c), T9(b), T10(c)).
    - Free text must match exactly: Q33 `:510`, T9(c) `:578`.
    - The scaffold steps also accept wrong answers: order and multiplicity are ignored on 20 two-value
      steps, so `1, 2` passes for `2, 1` at `:365`, and `1, 99` passes for `1, 1` at `:389`.

#### (iv) No precision is stated, and a sensibly rounded or correct answer is rejected

22. **stat-attack, variance** (unstated, `:1136`). Rule ±max(0.5, 0.5%) (`:1152`). In 8 scenarios the key
    is not the variance of the data, so the exact value is rejected. The on-screen formula (`:1139`)
    substitutes the table's own Σfx and Σfx², and following it gives the true value.

    | Scenario | True variance | Key | Note |
    |---|---|---|---|
    | G1 `:236` | 132.24 | 134.9 | key uses the rounded mean |
    | G2 `:246` | 31.96 | 26.98 | |
    | G3 `:256` | 115.56 | 114.11 | |
    | G7 `:296` | 29.27 | 30.78 | |
    | CM3 `:390` | 84.20 | 81.72 | |
    | CM6 `:438` | 631.22 | 628.04 | 3 s.f. 631 passes |
    | CM8 `:470` | 37.39 | 39.74 | |
    | L4_5 `:616` | 27 | 18.75 | its displayed Σfx² 12626661.75 is also wrong; true 12626662.5 |

    There is no skip or reveal, so a correct student cannot proceed. **recomputed at source**, all eight.
23. **split-it**, **reported, not re-checked:**
    - GCSE scale (`:357–364`): 5/3 recipes key 1 d.p. (133.3 ml, 3.3 eggs), so whole units are rejected
      in all 14 recurring rows (rule ±0.15, `:536`, `:538`).
    - Unitary speed (`:392–399`): the key is stored unrounded. 3 s.f. is rejected in 653 of 3528 draws,
      and 1 d.p. in 39 (24.8 for 24.75: diff 0.0500000000000007, rule `<0.05`, `:543`).
24. **given-that** (`:842`, ±0.005). At keys ending in 5 in the third decimal place, both 2 d.p.
    neighbours are rejected by floating point. `Math.abs(0.87-0.865)` = 0.0050000000000000044, so for
    alevel_12 `:350`, 0.86, 0.87, 86% and 87% are all rejected.
    - The same at 0.625 (`:357`, `:380`, `:397`, `:401`), 0.375 `:368` and 0.325 `:373`; half-up only at
      0.175 (`:381`, `:389`) and 0.045 `:358`.
    - Also `104/2,000` parses as 52 (`l4_01`, `:388`). **reported, not re-checked.**
25. **chart-interrogator, stem and leaf** (exact, `slTol` `:686`, by Jon's ruling of 1 Oct 2026; pinned by
    `scripts/verify-chart-interrogator.py`).
    - x.5 medians reject every rounding: S5 `:233` 237.5 → 238; S8 `:245` 222.5 → 223; S9 `:249` 49.65 → 49.7.
    - The stem never says "exactly", and there is no reveal. **reported, not re-checked.**
26. **test-the-claim, correlation critical value** (no d.p. stated; the table shows 4 d.p.). Rule `<0.001`
    (`:1669`) rejects a 2 d.p. reading in 8 of 12: C1, C2, C3, C5, C6, C9, C10 and C12. **reported, not
    re-checked.**

**Not affected (no right answer rejected):** 52dle, equatle, estimation-engine, estimation-golf,
formula-plug-in, like-terms-collector, log-laws, new-shapes, percentage-flip, quadratic-factoriser,
six-sevens-bruv and think-of-a-number.

### 1.3 Wrong answers accepted at the asked precision (c)

These matter for the marker as much as the rejections do: a band wide enough to hide a wrong key also
passes a wrong answer.

- **split-it.** Money ±0.05 (`:543`): wrong pence ±1–4p always pass, and ±5p passes in 3388 of 7700
  cases by float drift.
  - £0.30 accepts 0.25 and 0.35.
  - Currency £35 at €1.05 (key 36.75) accepts 36.70 and 36.80.
  - Fraction numerators use `parseInt`, so 3.9/8 passes for 3/8 (`:521`).
- **tax-theft.** ±£1 on the allowance and taxable steps; ±£2 on tax, NI, deductions and net
  (`:859`–`:961`).
- **growth-and-decay.** sq4 is an absolute ±0.15: L4_1 (`:474`, key 0.0347, 4 s.f. asked) and L4_5
  (`:506`, key 0.0416) accept 0 and 0.1. sq1's 2% band accepts 721–749 for CM1's 735.
- **stat-attack.**
  - The mean ±0.15 accepts neighbouring 3 s.f. values below 100 (G1 46.4 accepts 46.3 and 46.5).
  - SD ±0.1 does the same below 10.
  - Class strings ignore the inequality signs (`40 < x ≤ 50` passes).
- **test-the-claim.**
  - z ±0.02 accepts two wrong 2 d.p. values on each side (N2 2.19 accepts 2.18 and 2.20).
  - The p-value ±0.006 against a 4 d.p. ask accepts P(X = x) for P(X ≥ x) (B2: 0.0148 for 0.0207).
- **component-crusher.**
  - 2 d.p. asks have tol 0.02 (G2 5.83 accepts 5.82, 5.84 and 5.85).
  - 1 d.p. angles have tol 0.3 (AL1.2 116.6 accepts 116.3–116.8).
- **quadratic-factoriser.** The input is rounded to 2 d.p. before comparison (`:1034–1038`), so 9.914
  passes for 9.91.
- **screening-room.** alevel_12 (true 0.05%) accepts 0 and "0.5%".
- **given-that.** l4_13 (true 0.049) accepts 0.0441–0.054.
- **graph-sketcher.**
  - L4_11 cells accept 0 (an absolute 0.15 floor).
  - The roots item tolerates one extra value.
  - AL13's y-band is 1.5 on y = 1.41.
- **chart-interrogator.** Histogram counts ±1 accept 161 and 163 for 162.
- **Truncation by `parseInt`:** glorious-gantt (5.9 for 5), like-terms-collector (5.7 for 5) and 52dle
  (52.9 wins puzzle 52).
- **factor-theorem.** Two-value scaffold steps ignore order and multiplicity (item 21).

### 1.4 Keys that disagree with their own stem (e), every key checked

- **growth-and-decay**, all 120 checked. Keys at the wrong precision, each accepted by the band:
  - CM3 `:229`: 1808 for a 2 s.f. ask (1800).
  - AL5 `:380`: 15530 (15500).
  - AL8 `:404`: 2172 (2170).
  - L4_11 `:550`: 6.17 (6.16).
  - L4_9 `:538`: 4.43 (4.42).
  - L4_1 `:474`: 0.0347 for 4 s.f. (0.03466).
  - L4_5 `:506`: 0.0416 (0.04159).
  - Plus the four wrong values in 1.2(i) and the CM2 sq1 key built from the wrong k.
  - This confirms §1.36's three keys. Correction: `:751` and `:790` are the `parseFloat` lines, not where
    money is keyed.
- **stat-attack**, 36 checked.
  - 17 mean keys are not at 3 s.f.
  - 15 variance keys are not the data's variance (8 rejected, 7 inside the band).
  - CM11's SD key is 437.5 (4 s.f.).
  - L4_5's Σfx² is wrong.
  - The median convention differs between G4 (n/2) and G10 ((n+1)/2).
- **component-crusher**, 92 checked: L2.2 `:409` 79.6 (true 79.7, accepted); AL11.2's bearing (1.2 item 10).
- **suvat**, 70 checked.
  - L4_8 `:259–260` has no real solution: u² = 144 − 400 = −256, yet it is keyed 4 with tol 1.
  - Five A-Level keys differ from the 3 s.f. value inside their bands (AL16, AL18, AL37, AL41, AL48).
  - AL48's key 103.5 contradicts its own working, 103.4.
- **estimation-golf.**
  - `:663` asks for the first-principles gradient with h = 0.001 (27.009) but keys the limit, 27.
  - `:666` prints its own answer in the stem, "(≈ 343 m/s)".
- **estimation-engine.** `:276` √(e × 1000) is keyed 52.07; true 52.137.
- **screening-room.** Three keys are mis-rounded in the 4th d.p. (core_01, core_09, l4_10). None changes
  a mark.
- **fermi-lab.** molecules-swimming-pool `:339` `acceptedAnswer` 8.35e28; its own arithmetic gives 8.3e31.
- **factor-theorem.** T4(b) (1.2 item 12). Practice Q20 `:466` says "Find k", but f(x) has no k.
- **No disagreement in:** test-the-claim (all 48 keys correct; every defect is in the marking),
  log-laws (418), quadratic-factoriser (1070), split-it, percentage-flip, tax-theft (apart from the
  £100k defect), given-that, chart-interrogator and the six integer-keypad games.

### 1.5 Keys computed from values not on screen (f)

- **tax-theft.** NI, deductions and net are keyed from unrounded NI (`:919–923`, `:948`, `:960`), while
  the payslip shows `fmtMoney(Math.round(expected))` (`:1055`).
  - Every route from the on-screen figures stays inside the band; the worst gap is £0.42 over all 20
    salaries.
  - So §1.36's concern does not produce a rejection, but Jon's ruling (key from what is on screen) still
    applies.
- **component-crusher Level 4.** The 3-D vectors are never shown as numbers in L1, L2, L3, L4, L5, L6,
  L8, L11, L12 and L14. Only `q.desc` and an unlabelled isometric projection are drawn (`:562`, `:585–587`,
  `:617–623`). AL12's diagram draws (3, −2), where its prompt says i + 2j.
- **growth-and-decay CM2 sq1.** The key comes from the hard-coded k = 161.2 in `graphFn` (`:218`), which
  is not on screen.
- **glorious-gantt.** `drawNetwork` (`:834ff`) ignores `directTo`/`altTo`, draws self-loops and leaves end
  nodes dangling. The drawn network contradicts the activity table in 10 of 15 scenarios, and the prompts
  tell the student to work from the drawing.
- **graph-sketcher CM3.** Keyed t, where the stem asks for the year.
- **estimation-golf `:680`.** Keyed with π = 3.14, which is not shown.
- **fermi-lab.** 19 questions whose `acceptedAnswer` uses operations the chain does not contain.
- **test-the-claim, normal p-value.** Keyed from the unrounded z while 2 d.p. is shown; always inside
  the band.
- **chart-interrogator.** Cumulative-frequency keys are unrounded readings, by design.

### 1.6 Feedback at a precision other than the one asked (g)

- **growth-and-decay** (`:737`, `:757`, `:795`): 10 keys.
  - "1808" for a 2 s.f. ask; "15530" and "2172" for 3 s.f.
  - "10", "63", "59", "9.9" and "4.6" lose trailing zeros.
  - "0.0347" and "0.0416" are shown for 4 s.f. asks.
- **stat-attack.** The mean and SD feedback (`:967`, `:1183`, `:1260–1261`) shows 4–5 s.f. keys against a
  3 s.f. ask.
- **test-the-claim.** The normal critical value feedback (`:1716–1717`) and placeholder (`:1604`) show
  4 d.p. against "(2 d.p.)".
- **component-crusher.** `:725` prints 6.40 as "6.4" and 8.60 as "8.6", and the bearing as "143.1".
- **split-it.**
  - The speed working prints float noise: "19.799999999999997 miles" (`:397`).
  - Currency drops trailing zeros: "€36.7" (`:390`).
  - Scale prints "5/3 = 1.6666666666666667" (`:363`).
- **chart-interrogator.**
  - Stem-and-leaf feedback prints raw floats: "Correct — 2.3999999999999995" (`:867`, `:820`).
  - The cumulative-frequency IQR shown is the difference of the rounded quartiles: 14, 10 and 2.1 for
    true 13.1, 9.4 and 2.0.
- **screening-room** (`:809`):
  - prints a literal "\approx" outside KaTeX;
  - double-rounds the key, disagreeing with the hand-written explanation in 6 items (alevel_09, alevel_12,
    alevel_20, l4_07, l4_10 and l4_14).
- **estimation-golf.** `:854` shows 2.30 as "2.3", and `:849` shows a 2 s.f. miss as "-0.00".

### 1.7 Input hazards, not marking rules

- **`type="number"` drops non-numeric input.** It empties on a £ sign, a thousands comma or a surd, and
  most games then return silently. That covers 15 of 26 games, including every money input.
- **Thousands commas in the stems.** estimation-engine ("1,000 ÷ 8") and estimation-golf ("3,847") print
  them, so a student who copies the format gets no response. Browser-dependent; not run in a browser.
- **fermi-lab `parseInput` (`:426–442`).**
  - It reads "3/4" as 3 and "75%" as 75.
  - "0.22m" is read as 220,000 on a step whose unit is metres.
  - "6×10^23" is read as 6.
- **iOS keypad with no minus key.** log-laws and quadratic-factoriser use `inputmode="decimal"`, which
  on iOS is widely reported to give no minus key. 34 log-laws answers and 940 quadratic-factoriser items
  are negative. **Unverified:** no device was available.

---

## 2. Level routing

**How the set was found:** `grep -noE "MaffsLeaderboard\.submitScore\(\s*[^,]+,\s*[^,]+," games/*/index.html`.

- That finds 98 calls in 95 files: the 94 roster games that submit, plus the unlisted `the-perfect-prank`.
  factor-theorem, higher-power and log-laws each make two calls.
- No game submits through a wrapper (grep for `submitScore` without the prefix finds only a comment,
  `quadratic-factoriser:1757`).
- Of the calls, 32 in 31 games pass a string literal, and 66 in 64 games pass a variable.
- Each variable was read back to every assignment: defaults, `?level=` handling and its validation,
  level-button `data-level` values, ternaries and resume state.
- The site's own links to each game (portal, `/op/`, `/parents/`, spec-map) were collected.

**What the result is compared with:** the hub registry, `leaderboards/index.html` `var GAMES = [`
(`:183`). The hub fetches only `leaderboards/<slug>_<level>` for the levels a row lists (`:456–460`).
So a submitted level that is not listed never shows on the hub, and a listed level that is never
submitted is a dead row.

**Firebase accepts any lowercase key** matching `/^[a-z0-9_]{1,80}$/` (`firebase/database.rules.json:10`).

**Verification.** The table comes from the routing sub-check. These mismatch rows were **recomputed at
source**, by re-reading the quoted lines:
- percentage-flip `:216`, fraction-equivalence `:208`, prime-factorisation `:212`, factor-race `:204`;
- angle-ace `:727`, sequence-solver `:305`, trig-identity-duel `:253`, estimation-golf `:716`;
- fermi-lab `:403–406`, expected-damage `:560`, log-laws `:740`;
- complex-converter `:299`, differentiation-duel `:626`, suvat `:575`.

The other rows are **reported, not re-checked**: group D's scale-factor-scaling, unit-converter and
split-it, all of group E and the "none" rows. `node scripts/check-leaderboard-coverage.js` passes on
this base: "95 games listed, each with exactly the levels it submits."

**Mismatch codes:**
- **SNL**: submitted, not listed.
- **LNS**: listed, never submitted.
- **typed-only**: a listed level reached only by hand-typing the URL.
- **SNL-typed**: any hand-typed `?level=` is submitted unvalidated.
- **collapsed**: the row matches, but tiers the game serves share one board.

**Source abbreviations:** `idx` = portal `index.html`; `sm` = `spec-map/`; `op` = `op/`;
`par/x` = `parents/x/`; `upd` = `updates/`.

| slug | call line | level expr | values via UI / site links (sources) | values only via hand-typed URL | hub levels | mismatch |
|---|---|---|---|---|---|---|
| 52dle | :945 | `'all'` | all | none | all | collapsed ('all'; roster KS3, GCSE; one untiered daily puzzle; idx:1422 bare) |
| angle-ace | :871 | currentLevel | gcse (default :716; bare idx:2117 GCSE; button :108); year6 (button :107; op:446, par/angles:131) | none. `:727 if(lvl && QUESTIONS_BY_LEVEL[lvl])`, and the bank holds only year6 (:200) and gcse (:483), so `?level=ks3` gives gcse | year6, ks3, gcse | **LNS ks3**; KS3 (roster, card data-levels "ks3 gcse") collapsed into gcse |
| bearing-blitz | :294 | `'all'` | all (idx:2188 `?level=gcse` is ignored) | none | all | none (roster GCSE only) |
| better-value | :1357 | currentLevel | core (default :1118; idx:2838, sm:294/313); gcse (button :202; idx:2355) | none (validated :1119) | gcse, core | none |
| binomial-blaster | :243 | level | alevel (default :229; idx:3099, sm:188); alevel2 (button :87) | none (validated :235) | alevel, alevel2 | none |
| boolean-blitz | :875 | `'level4'` | level4 | none | level4 | none |
| characteristic-quest | :145 | `'further'` | further | none | further | collapsed (roster Further, L4; card "further l4" idx:3302) |
| chart-interrogator | :1148 | selectedLevel | gcse, alevel, core, l4 (buttons :183-186; idx:2281 gcse, idx:2786 core). Start is disabled until a type and a level are chosen (:379) | none. The URL must match a `[data-level]` element (:387); `?level=level4` matches nothing | gcse, alevel, core, l4 | none (`l4` is declared in LEVEL_OVERRIDES :172) |
| circle-theorem-spotter | :449 | `'gcse'` | gcse | none | gcse | none |
| complex-converter | :625 (Rounds mode only) | LEVEL | further (idx:3271, sm:239-241/266); level4 (bare default :299, via sitemap/canonical; no site link carries it) | **any string**: `:299 const LEVEL = params.get('level') \|\| 'level4';` is unvalidated, and `:396 QUESTIONS[LEVEL] \|\| QUESTIONS.level4` lets the game run | further, level4 | **SNL-typed** |
| component-crusher | :769 | G.level | gcse, alevel, level4 (buttons :122-124; idx:2300, sm:310 gcse; sm:192 alevel); start returns early with no level (:537) | none (URL must match a button, :534) | gcse, alevel, level4 | none |
| coordinate-geometry-dash | :380 | level | gcse (default :122, button :92); alevel (button :93; sm:190) | none (only `'alevel'` is honoured, :130) | gcse, alevel | none |
| core-maths-paper1 / 2a / 2b / 2c | :785 / :604 / :557 / :560 | `'core'` | core | none | core | none |
| correlation-or-coincidence | :363 | `'gcse'` | gcse (idx:2262 bare; idx:2769 `?level=core` is ignored) | none | gcse | collapsed (roster GCSE, A-Level, Core; Core runs from the Core section rank on GCSE) |
| curling-friction | :317 | level | alevel (default :232; idx:3009); level4 (button :105) | none (validated :239) | alevel, level4 | none |
| decimal-detective | :935 | LEVEL | year6 (`const LEVEL = 'year6'` :322) | none | year6 | none |
| differentiation-duel | :996 | LEVEL | alevel (default :626; idx:2955, sm); level4 (sm:186) | **any string**: `:626 ... .get('level') \|\| 'alevel'` is unvalidated; `:869 QUESTIONS[LEVEL] \|\| QUESTIONS.alevel` runs | alevel, level4 | **SNL-typed** |
| dimension-checker | :154 | `'level4'` | level4 (idx:3192, A-Level section) | none | level4 | collapsed (roster A-Level, L4) |
| distinctly-average | :1461 (gated) | currentLevel | ks3 (default `IMPLEMENTED_LEVELS[0]` :1103; bare idx:1824; par/averages:140); gcse (idx:2411; buttons built from IMPLEMENTED_LEVELS :1109) | none (validated :1103) | ks3, gcse | none. `LEADERBOARD_MODE_READY=false` (:1458), so it submits nothing today |
| eigenvalue-extractor | :144 | `'further'` | further | none | further | collapsed (roster Further, L4) |
| eigenvector-engine | :158 | `'further'` | further | none | further | collapsed (roster Further, L4) |
| equation-builder | :578 | currentLevel | ks3, gcse, level4 (buttons :177-179; Start is `disabled` until one is clicked, :187/:366; idx:1476 `?level=ks3` clicks the button, :383) | none | ks3, gcse, level4 | none |
| equatle | :666 (gated) | `'all'` | all | none | all | collapsed ('all'; roster KS3, GCSE; untiered); gate is closed (:665) |
| estimation-engine | :437 | `'all'` | all (idx:1298 `?level=ks3` and idx:2648 `?level=core` are ignored) | none | all | collapsed ('all'; roster KS3, GCSE, Core) |
| estimation-golf | :912 (gated) | level | ks3 (default :716; idx:1278, sm); year6 (op:483); gcse, alevel, level4 (buttons :507-511). **`?level=core` (idx:2629, Core section) has no bank and gives ks3** | none (validated :716) | year6, ks3, gcse, alevel, level4, core | **LNS core**; Core collapsed into ks3. Moot today: `LEADERBOARD_MODE_READY=false` (:911) |
| expectation-station | :1080 | currentLevel | core (default :384; idx:2821); gcse (idx:2337); alevel (button :235) | none (validated :412) | gcse, core, alevel | none |
| expected-damage | :949 | currentLevel | gcse (default :546; **KS3 card idx:1604 is bare**); core (idx:2736, sm). The game has no level selector | ks3 (`:560 if (lvl && QUESTIONS[lvl]) currentLevel = lvl;`) | ks3, gcse, core | **typed-only ks3**; KS3 portal runs collapse into gcse |
| factor-race | :375 | gameLevel | ks3 (default; idx:1316, sm:141); year6 (op:468) | none: `:204 const gameLevel = urlLevel === 'year6' ? 'year6' : 'ks3';` | year6, ks3, gcse | **LNS gcse**; GCSE (card data-levels "ks3 gcse") collapsed into ks3 |
| factor-theorem | :779, :1044 | `'alevel'` ×2 | alevel | none | alevel | collapsed (roster A-Level, L4) |
| fermi-lab | :718 | currentTier | gcse (bare default :406; sm:287); core (idx:2872); ks3 (**idx:3171, the A-Level section card**). No selector in the game | alevel, level4 (whitelisted :403-404, but nothing links to them) | ks3, gcse, alevel, level4, core | **typed-only alevel, level4**; the A-Level portal card ranks on ks3 |
| force-resolver | :222 | level | alevel (default :193; idx:3028); level4 (button :82) | none | alevel, level4 | none |
| formula-forge | :483 | level | gcse, alevel, level4 (buttons :110-112; idx:2243) | none (whitelist :169) | gcse, alevel, level4 | none |
| formula-plug-in | :659 | LEVEL | year6 (const :358) | none | year6 | none |
| formula-unlocked | :516 | level | gcse, alevel, level4 (buttons :113-115) | none (whitelist :168) | gcse, alevel, level4 | none |
| four-quadrant-explorer | :747 | LEVEL | year6 (const :241) | none | year6 | none |
| fraction-equivalence | :334 | gameLevel | **all** (every non-year6 run: idx:1387 `?level=ks3`, par/fractions:120, sm:142/145); year6 (op:463) | none: `:208 const gameLevel = urlLevel === 'year6' ? 'year6' : 'all';` | year6, ks3, gcse | **SNL all; LNS ks3, gcse** |
| free-daily-pizza | :1066 | board | practice-q20, practice-q40 (`FDP.boardFor` :798-801, mixed stage only; lengths `[20, 40]` :269, menu pool capped at 40 :936); daily-YYYY-MM-DD (:800). Single-stage runs give null and submit nothing | none (no `?level` read) | practice-q20, practice-q40 | none (daily-* is off the hub by design, OFF_HUB_LEVEL_PATTERNS :180) |
| glorious-gantt | :1235 | G.level | core, level4 (pills :150-151; idx:2611 `?mode=a&level=core`; sm:272 level4); start needs a mode and a level (:789) | none (URL must match a pill, :785) | core, level4 | none |
| gradient-hunter | :1127 | G.level | gcse, core, alevel (buttons :138-140; idx:2592 gcse; sm core); start returns early with no level (:679) | none (URL must match a button, :670) | gcse, core, alevel | none |
| graph-sketcher | :1128 | G.level | core, alevel, level4 (buttons :158-160; idx:2573) | none (:596) | core, alevel, level4 | none |
| graph-transformer | :772 | level | gcse (default :172); alevel (button :122). `gtBfsCheck` swaps `level` (:600) and restores it synchronously (:631) | none (only `'alevel'`, :781) | gcse, alevel | none |
| growth-and-decay | :858 | G.level | core, alevel, level4 (buttons :156-158; idx:2554) | none (:609) | core, alevel, level4 | none |
| higher-power | :624, :775 | currentLevel ×2 | ks3 (default :378; idx:1130/1766); gcse, alevel (buttons :159-160) | none (validated :403) | ks3, gcse, alevel | none (see aside 1) |
| index-laws | :801 | `'gcse'` | gcse | none | gcse | collapsed (roster GCSE, A-Level; card "gcse alevel" idx:1884) |
| integration-duel | :1019 | currentLevel | alevel (default :902; idx:2973); level4 (button :608) | none (:902) | alevel, level4 | none |
| like-terms-collector | :580 | `'year6'` | year6 | none | year6 | none |
| linear-equation-solver | :476 | level | gcse (default :308, the only button :112) | none (no `?level` read) | gcse | none |
| log-laws | :1086 (Laws drill); :1925 (Solve mode, gated) | LEVEL | alevel (bare default and `?level=alevel`: idx:3064, sm) | level3, level4 (`:740 return Object.prototype.hasOwnProperty.call(levelNames, p) ? p : 'alevel';`; no button or link) | alevel, level3, level4 | **typed-only level3, level4**; the L4 portal filter shows the alevel link |
| maths-court | :842 | currentLevel | ks3 (default :621; bare KS3 idx:1586); gcse, core (cards :199/:203; idx:2719 core) | none (:620) | ks3, gcse, core | none |
| matrix-crunch | :422 | level | further (default :234; idx:3288); level4 (button :111; sm:267) | none (:244) | further, level4 | none |
| modular-battle | :349 | `'gcse'` | gcse | none | gcse | collapsed (roster GCSE, A-Level) |
| moments-master | :202 | level | alevel (default :188); level4 (button :80) | none (:194) | alevel, level4 | none |
| negative-number-line | :937 | LEVEL | year6 (const :325) | none | year6 | none |
| new-shapes | :972 | LEVEL | year6 (const :421) | none | year6 | none |
| normal-navigator | :376 | `'alevel'` | alevel (idx:2855 `?level=core` is ignored) | none | alevel | collapsed (roster A-Level, L4, Core) |
| partial-fractions-duel | :162 | `'alevel'` | alevel | none | alevel | collapsed (roster A-Level, L4) |
| percentage-flip | :313 | gameLevel | **all** (every non-year6 run: idx:1369 `?level=ks3`, par/fractions:121, sm:145-146); year6 (op:478) | none: `:216 const gameLevel = _pfUrlLevel === 'year6' ? 'year6' : 'all';` | year6, ks3, gcse | **SNL all; LNS ks3, gcse** |
| prime-factorisation | :407 | gameLevel | **all** (idx:1334 `?level=ks3`, sm:141); year6 (op:473) | none: `:212 var gameLevel = _urlLevel === 'year6' ? 'year6' : 'all';` | year6, ks3, gcse | **SNL all; LNS ks3, gcse** |
| prime-or-composite | :467 | `'all'` | all (idx `?level=ks3` is ignored; 6-7/index.html bare) | none | all | collapsed ('all'; roster KS3, GCSE) |
| prisoners-dilemma | :781 | currentLevel | ks3 (default :298; idx:1150/1785); gcse, alevel, core (buttons :199-202; idx:2927 core) | none (:1016) | ks3, gcse, alevel, core | none |
| probability-paradox | :573 | `'gcse'` | gcse (idx:2753 `?level=core` is ignored) | none | gcse | collapsed (roster GCSE, Core) |
| probability-pioneer | :808 | LEVEL | year6 (const :358) | none | year6 | none |
| proof-builder | :621 | level | alevel (default :203; idx:3135); further (button :132; sm:246; Induction mode forces further, :327) | none (:209) | alevel, further | none |
| proportion-blaster | :296 | level | gcse (default :248; idx:2009); alevel (button :104) | none (:254) | gcse, alevel | none |
| quadratic-factoriser | :1743 | currentLevel | gcse (default :1084; idx:1919); higher, formula (buttons from IMPLEMENTED_LEVELS :1090) | none (:1084) | gcse, higher, formula | none (LEVEL_OVERRIDES :171) |
| scale-factor-scaling | :190 | level | gcse (default :99; idx:2205); alevel, level4 (buttons :78-79) | **any string**: `:105 if(pa.get('level')){level=pa.get('level');...` is unvalidated; `:174 else bank=[...T2,...T3,...T4];` runs | gcse, alevel, level4 | **SNL-typed** |
| screening-room | :894 | currentLevel | gcse (default :419; idx:1211/2392); alevel, core, level4 (buttons :234-236; idx:2909 core) | none (:431) | gcse, alevel, core, level4 | none |
| sequence-solver | :347 | level | ks3 (default :299; idx:1259, par/sequences, sm); gcse, alevel (buttons :92-93) | none. Validated at :305, and QUESTIONS has only ks3 (:122), gcse (:180) and alevel (:236), so `?level=level4` gives ks3 | ks3, gcse, alevel, level4 | **LNS level4**; L4 (roster, card data-levels "l4") collapsed into ks3 |
| seven-bridges | :842 | S.level | ks3, gcse, alevel (cards :176-184; idx `?level=ks3`); start returns early with no level (:317) | none (:864) | ks3, gcse, alevel | none |
| shape-shifter | :922 | `'year6'` | year6 | none | year6 | none |
| simultaneous-solver | :412 | level | gcse (default :247; idx:2064); alevel (button :104) | none (:286) | gcse, alevel | none |
| six-sevens-bruv | :862 | board | q20, q40 (`SSB.boardFor` :472-474 is `'q' + cap`; lengths `[20, 40]` filtered below the pool size :709; `MaffsSession.render` re-syncs the length on every menu render). `'clear'` is never submitted (:862) | none (no `?level` read) | q20, q40 | none |
| split-it | :635 | S.level | ks3, gcse (buttons :148-149 `startGame('ks3')` and `startGame('gcse')`). Site `?level=` links (idx:1241, par/ratio-proportion, sm:148) are ignored because they carry no `?mode=` (:206) | **any string** when a valid `?mode=` is present: `:205 if(p.get('mode'))S.mode=p.get('mode');` then `:206 if(p.get('level')&&S.mode)startGame(p.get('level'));`. The generators branch on `level==='ks3'` and otherwise give gcse (:263), so the game runs | ks3, gcse | **SNL-typed** |
| spot-the-error | :516 | currentLevel | ks3, gcse, level4 (buttons :170-172; Start is `disabled` until one is clicked, :180). The game reads no `?level` (idx:1495 is ignored) | none | ks3, gcse, level4 | none |
| spot-the-muppet | :622 | currentLevel | gcse (default :336; bare KS3 idx:1532); ks3, core (buttons :174/:176; idx:2665 core) | none (whitelist :348) | ks3, gcse, core | none |
| standard-form-blitz | :237 | level | gcse (default :223; idx:2046); alevel (button :92) | none (:229) | gcse, alevel | none |
| stat-attack | :1317 | G.level | gcse, core, level4 (buttons :179-185; idx:2319/2804); start returns early with no level (:789) | none (:780) | gcse, core, level4 | none |
| surd-simplifier | :299 | level | gcse (default :251; idx:1991); alevel (button :104) | none (:259) | gcse, alevel | none |
| suvat | :937 | level | alevel (idx:2991, sm:205-207/265); level4 (bare default :575; upd:190) | **any string**: `:575 const level = params.get('level') \|\| 'level4';` is unvalidated; `:577 const POOL = isALevel ? QUESTIONS_ALEVEL : QUESTIONS_LEVEL4;` runs | alevel, level4 | **SNL-typed** |
| tax-theft | :1123 | `'core'` | core | none | core | none |
| terrible-advice | :653 | currentLevel | gcse (default :328; bare KS3 idx:972/1550); ks3, core (buttons :208/:210; idx:2683 core) | none (:371) | ks3, gcse, core | none |
| test-the-claim | :2078 | `'alevel'` | alevel | none | alevel | collapsed (roster A-Level, L4) |
| the-perfect-prank | :639 | LEVEL | ks3 (`const SLUG='the-perfect-prank', LEVEL='ks3';` :301; escape-rooms/index.html:179) | none | not on the hub (NOT_ON_HUB :158-160) | none (declared off-hub) |
| think-of-a-number | :732 | `'year6'` | year6 | none | year6 | none |
| trig-identity-duel | :295 | level | gcse (default :247; idx:2027); alevel (button :104; sm:183) | none. Validated at :253, and QUESTIONS has only gcse (:142) and alevel (:194) | gcse, alevel, level4 | **LNS level4**; L4 (roster, card data-levels "l4") collapsed into gcse |
| trig-wars | :902 | `'gcse'` | gcse | none | gcse | collapsed (roster GCSE, A-Level) |
| trig-worms | :560 | `'gcse'` | gcse | none | gcse | collapsed (roster GCSE, A-Level) |
| truth-buster | :523 | `'all'` | all | none | all | collapsed ('all'; roster KS3, GCSE, A-Level; the three "tiers" are rounds within one run) |
| truth-will-set-you-free | :900 | `'level4'` | level4 | none | level4 | none |
| unit-converter | :215 | level | gcse (default :101; idx:2224); alevel, level4 (buttons :81-82) | **any string**: `:107 if(pa.get('level')){level=pa.get('level');...` is unvalidated; `:191 else{bank=[...]}` runs | gcse, alevel, level4 | **SNL-typed** |
| word-problem-decoder | :825 | currentLevel | gcse (default; the button is clicked at :500-501); ks3 (:500; idx:1457) | none (:500) | ks3, gcse | none |
| wrong-on-the-internet | :1145 | S.level | gcse (default :770); ks3, core (buttons :201/:203; idx:2701 core) | none (:790) | ks3, gcse, core | none |

### 2.1 Mismatches

**A. Submitted under a level the hub does not list, through the site's own links (live): 3 games.**
- **percentage-flip** `:216` `const gameLevel = _pfUrlLevel === 'year6' ? 'year6' : 'all';`, submitted at
  `:313`.
- **fraction-equivalence** `:208` `const gameLevel = urlLevel === 'year6' ? 'year6' : 'all';`, submitted
  at `:334`.
- **prime-factorisation** `:212` `var gameLevel = _urlLevel === 'year6' ? 'year6' : 'all';`, submitted at
  `:407`.

Each sends every KS3 and GCSE run, including the portal's `?level=ks3` links, to `<slug>_all`. The hub
lists `year6, ks3, gcse`, so the `all` board is invisible and the ks3 and gcse rows are dead.
**Confirmed as §1.35 states.**

**B. A listed level that is never submitted (dead hub rows): 5 games, none of them in §1.35.**
- **factor-race, gcse.** `:204` `const gameLevel = urlLevel === 'year6' ? 'year6' : 'ks3';`, and there
  are no level buttons. GCSE runs rank on the KS3 board.
- **angle-ace, ks3.** `:727` `if(lvl && QUESTIONS_BY_LEVEL[lvl]){selectLevel(lvl)}`, but only `year6` and
  `gcse` keys exist, so `?level=ks3` plays and ranks as GCSE.
- **sequence-solver, level4.** `:305` accepts a level only if `QUESTIONS[level]` exists, and there is no
  `level4` key. L4 runs rank on KS3.
- **trig-identity-duel, level4.** `:253` has the same check and no `level4` key. L4 runs rank on GCSE.
- **estimation-golf, core.** `:716` falls back to `'ks3'`, and the portal's Core link (`idx:2629`) plays
  KS3. Moot while `LEADERBOARD_MODE_READY=false` (`:911`).

**C. A listed level reachable only by hand-typing the URL: 3 games, 5 levels.**
- **expected-damage, ks3.** `:560`, and the game has no selector. The portal's KS3 card (`idx:1604`) is
  a bare link, so KS3 players rank on GCSE.
- **fermi-lab, alevel and level4.** `:403–404`, but no link sends them. The A-Level card links
  `?level=ks3` (`idx:3171`).
- **log-laws, level3 and level4.** `:740`; no button or link reaches them.

**D. Any hand-typed `?level=` is submitted unvalidated, creating a board the hub never reads: 6 games.**
- complex-converter `:299` `params.get('level') || 'level4'`, with the bank falling back at `:396`;
- differentiation-duel `:626`, falling back at `:869`;
- scale-factor-scaling `:105`, bank else-branch `:174`;
- unit-converter `:107`, else-branch `:191`;
- suvat `:575`, pool chosen at `:577`;
- split-it `:205–206`, but only when a valid `?mode=` is also present.

**E. Several served tiers merged on one board ("collapsed"): 19 literal-level games.**
- Named after one tier:
  - index-laws, modular-battle, trig-wars and trig-worms submit `gcse`, but also serve A-Level;
  - correlation-or-coincidence `gcse` also serves A-Level and Core;
  - probability-paradox `gcse` also serves Core;
  - normal-navigator `alevel` also serves L4 and Core;
  - partial-fractions-duel, factor-theorem and test-the-claim `alevel` also serve L4;
  - dimension-checker `level4` also serves A-Level;
  - characteristic-quest, eigenvalue-extractor and eigenvector-engine `further` also serve L4.
- `all` on an untiered game: 52dle, equatle, estimation-engine, prime-or-composite and truth-buster.

Whether each is a defect depends on whether the tiers should rank separately. That is Jon's call; the
data only shows that they do not.

**Counts:**

| Group | Games | Detail |
|---|---|---|
| A + B | 8 | 3 invisible boards, 11 dead rows |
| C | 3 | 5 levels |
| D | 6 | |
| E | 19 | |
| Any finding | 36 of 95 | |

**Why the coverage check passes all of them.**
- `scripts/check-leaderboard-coverage.js:246`, inside `submittedLevels()`, assumes the roster's tiers
  for a variable level instead of tracing it:
  `return [...new Set((roster[slug] || []).concat(literals))].sort();`
  For every game in A–D, the roster row equals the hub row, so the comparison never fires.
- For E, `:245` `if (literals.length === calls.length) return [...new Set(literals)].sort();` returns the
  literal, and nothing compares it with the tiers the game is served at.

---

## 3. Bank attribution

**How the set was found:** `scripts/extract-banks.py` was run unchanged over all 96 games (see the
preamble), giving per-level counts and whether each count was scoped to its level. Every game with more
than one roster level, every game the extractor calls a GENERATOR, and the single-level games were then
read by hand. "Served" means the distinct questions a student can draw from at
`/games/<slug>/?level=<key>`, or from the matching level button where the game ignores the URL. Every
fallback was followed, and arrays were evaluated in node.

**Verification.** Recomputed at source by evaluating the arrays:
- percentage-flip `:173`/`:191`, coordinate-geometry-dash `:194`/`:254`;
- equation-builder, spot-the-error, spot-the-muppet and word-problem-decoder (per-item `level` counts);
- prime-factorisation `:207–208`, fraction-equivalence and factor-race `YEAR6_BANK`;
- formula-unlocked `:395–397`, scale-factor-scaling `:172–174`, unit-converter `:189–191`;
- chart-interrogator's level tags, and the `:400` filter.

The other rows are **reported, not re-checked**.

**Key:** E = extractor count; L = ledger B4 entry ("–" for none).

| slug | selection code | served per level (true) | E per level | L per level | mismatch |
|---|---|---|---|---|---|
| 52dle | `PUZZLES[dayIdx()]` :995, `% PUZZLES.length` :710 (no level branch, one puzzle a day) | ks3 20, gcse 20 | 20, 20 | 20, 20 | none |
| angle-ace | `if(lvl && QUESTIONS_BY_LEVEL[lvl])…else selectLevel('gcse')` :727-728; `QUESTIONS_BY_LEVEL[currentLevel]\|\|QUESTIONS_BY_LEVEL.gcse` :735 | year6 40, **ks3 35 (gcse fallback, no ks3 key or button)**, gcse 35 | 40, **75**, 35 | –, **–**, 35 | **hidden-B4 (ks3)** |
| better-value | `if (!QUESTIONS[currentLevel]) currentLevel='core'` :1119; `QUESTIONS[currentLevel]` :1190 | gcse 20, core 50 | 20, 50 | 20, – | none |
| binomial-blaster | `QUESTIONS[pa.get('level')]` :235; `QUESTIONS[level]` :236 | alevel 50, alevel2 50 | 50, 50 | –, – | none |
| characteristic-quest | `shuffle([...QS])` :137 (no level read) | further 26, level4 26 | 26, 26 | 26, 26 | none |
| chart-interrogator | `[data-level="'+l+'"]` :387; `getScenarios().filter(s=>s.level===selectedLevel)` :400, per type :392-395; buttons `gcse/alevel/core/l4` :183-186 | **gcse 10, alevel 10, core 12, level4 8** (key `l4`; `?level=level4` matches no button, so nothing is selected). Per type 2-3 | **40, 40, 40, 40** | **–, –, –, –** | **hidden-B4 ×4** |
| circle-theorem-spotter | `QUESTIONS.gcse` :442 | gcse 55 | 55 | – | none |
| complex-converter | `QUESTIONS.further = QUESTIONS.level4` :366; `QUESTIONS[LEVEL]\|\|QUESTIONS.level4` :396; all 3 modes draw from `bank` :491,:673,:890 | further 55, level4 55 (same array) | 55, 55 | –, – | none |
| component-crusher | `.level-btn[data-level="${l}"]` :534; `SCENARIOS[G.level]` :538 | gcse 15, alevel 15, level4 15 | 15, 15, 15 | 15, 15, 15 | none |
| constructions-lab | `TASKS[idx]` :447 (no level read) | ks3 10, gcse 10 | 10, 10 | 10, 10 | none |
| coordinate-geometry-dash | `if(pa.get('level')==='alevel')` :130; `level==='gcse'?Q_GCSE:Q_ALEVEL` :311 | **gcse 24, alevel 21** | **45, 45** | **–, –** | **hidden-B4 ×2** |
| correlation-or-coincidence | `shuffle([...QUESTIONS])` :260 | 13 at gcse, alevel, core | 13 ×3 | 13 ×3 | none |
| curling-friction | `QUESTIONS[pa.get('level')]` :239; `QUESTIONS[level]` :241 | alevel 56, level4 20 | 56, 20 | –, 20 | none |
| differentiation-duel | `QUESTIONS[LEVEL]\|\|QUESTIONS.alevel` :869; level4 `selectWeighted(pool,…)` :906 (same pool) | alevel 45, level4 53 | 45, 53 | –, – | none |
| dimension-checker | `shuffle([...QS])` :146 | alevel 28, level4 28 | 28, 28 | 28, 28 | none |
| eigenvalue-extractor | `shuffle([...QS])` :136 | further 25, level4 25 | 25, 25 | 25, 25 | none |
| eigenvector-engine | `shuffle([...QS])` :137 | further 25, level4 25 | 25, 25 | 25, 25 | none |
| equation-builder | `.level-btn[data-level="'+urlLevel+'"]` :383; `QUESTIONS.filter(q=>q.level===currentLevel)` :400 | **ks3 40, gcse 40, level4 40** | **120 ×3** | –, –, – | count-wrong |
| estimation-engine | `[...QUESTIONS].sort(...).slice(0,ROUNDS)` :291 | ks3, gcse, core 49 each | 49 ×3 | – ×3 | none |
| estimation-golf | `_egUrlLevel && QUESTIONS[_egUrlLevel] ? _egUrlLevel : 'ks3'` :716; `QUESTIONS[level]` :736; buttons have no core :507-511 | year6 20, ks3 9, gcse 9, alevel 9, level4 9, **core 9 (ks3 fallback)**. `HOLES_META` :603 is hole metadata, not questions | 20, 9, 9, 9, 9, **65** | 20, 9, 9, 9, 9, **–** | **hidden-B4 (core)** |
| expectation-station | `if (lvl && QUESTIONS[lvl])` :412; `QUESTIONS[currentLevel]` :462 | gcse 15, core 20, alevel 10 | 15, 20, 10 | 15, 20, 10 | none |
| expected-damage | :560, `QUESTIONS[currentLevel]` :601 | ks3 15, gcse 20, core 15 | same | same | none |
| factor-race | `urlLevel==='year6' ? 'year6' : 'ks3'` :204; year6 `shuffle(YEAR6_BANK)` :246; else `VALID_PAIRS[randInt(...)]` :255, built by enumeration :230-240 | year6 20 (bank); **ks3, gcse generated: 2,694 ordered pairs (1,347 unordered)** | 20, **20, 20** | 20, **20, 20** | **false-B4 (ks3, gcse) + misclassified** |
| factor-theorem | Practice `CONTENT.practice.questions` :763, Test `CONTENT.test.questions` :1024 (separate tabs, no level read) | alevel 50, level4 50 (union; Practice 40, Test 10) | 50, 50 | –, – | none |
| fermi-lab | `if (level==='ks3')…else currentTier='gcse'` :401-406; `QUESTIONS[currentTier]` :467 | ks3 12, gcse 15, alevel 13, level4 10, core 15 | same | same | none |
| force-resolver | :199-200 `QUESTIONS[level]` | alevel 52, level4 20 | 52, 20 | –, 20 | none |
| formula-forge | `Q.alevel={s1:[...Q.gcse.s1],…}` :352; `Q[level]\|\|Q.gcse` :358; 4 stages in one session :359-364 | gcse 29, alevel 29 (copy of gcse), level4 16 | 29, 29, 16 | 29, 29, 16 | none |
| formula-unlocked | :168; `if(level==='gcse')bank=[...Q_GCSE]; else if(level==='alevel')bank=[...Q_GCSE.filter(q=>q.stage>=2),...Q_ALEVEL]; else bank=[...Q_LEVEL4]` :395-397 | **gcse 29, alevel 25 (19+6), level4 14** | **49 ×3** | **–, –, –** | **hidden-B4 ×3** |
| given-that | `urlLevel&&QUESTIONS[urlLevel]` :456; `QUESTIONS[currentLevel]` :464 | gcse 25, alevel 25, core 20, level4 20 | 25, 25, 20, 20 | same | none |
| glorious-gantt | `.pill[data-level=…]` :785; `key=G.level+'_'+G.mode; SCENARIOS[key]` :790-791 | **core 7 (mode a 4 + mode b 3), level4 8 (4+4)**; pool is per mode | **15, 15** | **15, 15** | **false-B4 (wrong number) ×2** |
| gradient-hunter | :668-670; `QUESTIONS[G.level]` :680 | gcse 15, core 20, alevel 10 | same | same | none |
| graph-sketcher | :596; `SCENARIOS[G.level]` :603 | core 15, alevel 15, level4 15 | same | same | none |
| growth-and-decay | :609; `Q[G.level]` :617 | core 15, alevel 15, level4 15 | same | same | none |
| higher-power | `ALL_BANKS[urlParams.get('level')]` :403; `ALL_BANKS[currentLevel]` :457 | ks3 40, gcse 40, alevel 40 cards (both modes) | 40 ×3 | – ×3 | none |
| index-laws | `shuffle(QUESTIONS)` :722 | gcse 45, alevel 45 | 45, 45 | –, – | none |
| integration-duel | `(urlLevel==='level4')?'level4':'alevel'` :902; `QUESTIONS[currentLevel]` :927 | alevel 45, level4 45 | 45, 45 | –, – | none |
| log-laws | `LEVEL` IIFE :738-741 (label only); Laws mode `QUESTIONS` :988 (38 if "skip Change of Base" is ticked); Solve mode is generated. `LAWS` :745 is a reference list | alevel, level3, level4 45 each (Laws) | 45 ×3 | – ×3 | none |
| maths-court | :620; `QUESTIONS[currentLevel]` :631 | ks3 15, gcse 20, core 10 | same | same | none |
| matrix-crunch | :244; `QUESTIONS[level]` :247, stages det/inv/cramer added in one session :249-251 | further 35 (15/10/10), level4 18 (8/4/6) | 35, 18 | 35, 18 | none |
| moments-master | :194-195 `QUESTIONS[level]` | alevel 49, level4 20 | 49, 20 | –, 20 | none |
| normal-navigator | `shuffle([...QUESTIONS])` :297 | alevel, level4, core 47 each | 47 ×3 | – ×3 | none |
| partial-fractions-duel | `QUESTIONS.alevel` :155 (no level read) | alevel 50, level4 50 (same array) | 50, 50 | –, – | none |
| percentage-flip | `gameLevel==='year6' ? QUESTIONS_YEAR6 : QUESTIONS_DEFAULT` :216-217 | **year6 20, ks3 12, gcse 12** | **32 ×3** | **32 ×3** | **false-B4 (wrong number) ×3** |
| prime-or-composite | opener 6,7, then `QUESTIONS.filter(...)` :325-327 | ks3 66, gcse 66 | 66, 66 | –, – | none |
| prisoners-dilemma | `if (lvl && OPPONENTS[lvl])` :1016; `[...OPPONENTS[currentLevel]]` :926. These are strategy bots (`{id:"nora",…stratName:"Always Cooperate (ALLC)"}`), not questions | **no question bank**; opponents ks3 5, gcse 7, alevel 9, core 7 | 9 ×4 (`OPPONENTS.alevel` only) | **9 ×4** | **false-B4 ×4 + misclassified** |
| probability-paradox | `if(mode==='paradox')…PARADOX_QUESTIONS / CONDITIONAL / FALLACY` :489-491 (no level read) | gcse 38, core 38 (union; per mode 12/14/12) | 38, 38 | 38, 38 | none |
| proof-builder | `['alevel','further'].includes(...)` :209; induction forces further :327; counter `COUNTER.alevel (+COUNTER.further if further)` :342-343; sorter same :346-347; `INDUCTION` :350 | alevel 33 (counter 25 + sorter 8); **further 50 (counter 35 + sorter 11 + induction 4)** | 33, **10** | 33, **10** | **false-B4 (further)** |
| proportion-blaster | :254; `QUESTIONS[level]` :257 | gcse 50, alevel 50 | 50, 50 | –, – | none |
| scale-factor-scaling | :105; `gcse:[...T1,...T2,...T3]; alevel:[...T1..T4]; else [...T2,...T3,...T4]` :172-174 | **gcse 38**, alevel 46, **level4 31** | **46** ×3 | **–, –, –** | **hidden-B4 (gcse, level4)** |
| screening-room | :431; `QUESTIONS[currentLevel]` :480 | gcse 20, alevel 20, core 15, level4 15 | same | same | none |
| sequence-solver | `pa.get('level')&&QUESTIONS[pa.get('level')]` :305 (no level4 key, so level stays `'ks3'` :299); `QUESTIONS[level]` :307 | ks3 50, gcse 50, alevel 54, **level4 50 (ks3 fallback)** | 50, 50, 54, **154** | – ×4 | count-wrong (level4) |
| seven-bridges | :863; `PUZZLE_BANKS[S.level]` :318 | ks3 25, gcse 25, alevel 25 | same | same | none |
| simultaneous-solver | :286; `[...QUESTIONS[level]]` :294 | gcse 50, alevel 50 | 50, 50 | –, – | none |
| spot-the-error | **no URL read anywhere** (only buttons :170-172); `Q.filter(q=>q.level===currentLevel)` :376 | **ks3 35, gcse 45, level4 30** | **110 ×3** | **–, –, –** | **hidden-B4 (ks3, level4)** |
| spot-the-muppet | `['ks3','gcse','core'].includes(lvl)` :348; `QUESTIONS.filter(q => q.level === currentLevel)` :401 | **ks3 18, gcse 20, core 12** | **50 ×3** | **–, –, –** | **hidden-B4 ×3** |
| standard-form-blitz | :229-230 `QUESTIONS[level]` | gcse 50, alevel 50 | 50, 50 | –, – | none |
| stat-attack | :776-780; `SCENARIOS[G.level]` :790 | gcse 12, core 12, level4 12 | same | same | none |
| surd-simplifier | :259; `QUESTIONS[level]` :262 | gcse 50, alevel 50 | 50, 50 | –, – | none |
| suvat | `params.get('level') \|\| 'level4'` :575; `isALevel ? QUESTIONS_ALEVEL : QUESTIONS_LEVEL4` :577 | **alevel 50, level4 8** | **58, 58** | –, **–** | **hidden-B4 (level4)**; count-wrong (alevel) |
| terrible-advice | :371; `QUESTIONS[currentLevel]` :442 | ks3 18, gcse 20, core 12 | same | same | none |
| test-the-claim | `QUESTIONS[state.mode].filter(q=>q.tail===tailType&&q.sig===state.sig)` :1269 (no level read) | alevel 48, level4 48 (union; per distribution 12, narrowed further by tail and sig) | 48, 48 | –, – | none |
| trig-identity-duel | :253 (no level4 key, so stays `'gcse'` :247); `QUESTIONS[level]` :256 | gcse 50, alevel 49, **level4 50 (gcse fallback)** | 50, 49, **99** | – ×3 | count-wrong (level4) |
| truth-buster | tiers 7+7+6 from `QUESTIONS.tier1/2/3` :333-335, all in one session | ks3, gcse, alevel 60 each | 60 ×3 | – ×3 | none |
| unit-converter | :107; `gcse:[...L,...A,...V,...T]; alevel:[...A,...V,...T]; else [...L.slice(0,4),...A.slice(0,5),...V,...T,...E]` :189-191 | **gcse 48, alevel 38, level4 42** | **58 ×3** | **–, –, –** | **hidden-B4 (alevel)**; count-wrong (gcse, level4) |
| word-problem-decoder | `(urlLevel==='ks3'\|\|urlLevel==='gcse') ? urlLevel : 'gcse'` :501; `QUESTIONS.filter(q=>q.level!==currentLevel…)` :607-613 (topic toggles narrow it further) | **ks3 50, gcse 60** | **110, 110** | –, – | count-wrong |
| wrong-on-the-internet | :790; `QUESTIONS[S.level]` :907 | ks3 15, gcse 20, core 10 | same | same | none |
| **Generators (table: GENERATOR)** | | | | | |
| prime-factorisation | `gameLevel==='year6'?'year6':'all'` :212; `NUMBERS = gameLevel==='year6' ? NUMBERS_YEAR6 : NUMBERS_DEFAULT` :213; `shuffle(NUMBERS).slice(0,TOTAL_QS)` :229 | **year6 20, ks3 28, gcse 28** (static literals :207-208, all distinct) | GENERATOR | **–, –, –** | **misclassified + hidden-B4 ×3** |
| graph-transformer | `generatePuzzles(){ if(level==='gcse'){ p.push({...literal}) ×25 } else { ×25 } }` :201-258; `shuffle(generatePuzzles()).slice(0,12)` :670; URL :781 | **gcse 25, alevel 25** (fixed literals, all distinct, no randomness) | GENERATOR | **–, –** | **misclassified + hidden-B4 ×2** |
| tax-theft | `SALARIES={easy:[8],medium:[8],hard:[4]}` :794-798; `shuffle(SALARIES[diff])` :824 | **core 20 salary scenarios** (8/8/4, per difficulty) | GENERATOR | **–** | **misclassified + hidden-B4** (scenario unit) |
| bearing-blitz | 16 fixed bearings + 8 × `Math.floor(Math.random()*360)` per session :116-121 | gcse: generated (0-359) | GENERATOR | – | none (mixed, but generated) |
| distinctly-average | `KS3_POOL = noCollisions([].concat(build…()))` :1083; `GCSE_POOL = KS3_POOL.concat(...)` :1086; `poolFor` :1096 | enumerated per level | GENERATOR | – | none |
| quadratic-factoriser | `window.QF_POOLS[level]` :862 (enumerated) | enumerated per level | GENERATOR | – | none |
| equatle | `getBank()` enumerates equations :365ff; daily or free target :557-567 | generated | GENERATOR | – | none |
| modular-battle, trig-worms, trig-wars, split-it | random parameters (`randInt`/`Math.random`), no static question list | generated | GENERATOR | – | none |
| six-sevens-bruv, free-daily-pizza | enumerated (78 facts; 518 items on `window.FDP` :880), level-invariant | generated | GENERATOR | – | none |
| **Single-level games** | | | | | |
| negative-number-line | `buildQuestions`: cycles place/order/calc from `PLACE_QUESTIONS`, `ORDER_QUESTIONS`, `CALC_QUESTIONS` :363-372. `PLACE_QUESTIONS` is plain numbers, so the extractor misses it | **year6 45 (15+15+15)** | **30** | **30** | **false-B4** |
| new-shapes | `ALL_QUESTIONS = [...PARALLELOGRAM, ...TRAPEZIUM, ...PRISM]` :415; session draws the three parts :724-726 | **year6 50** (15+20+15) | **100** (double count) | – | count-wrong |
| boolean-blitz | `QUESTIONS` :363, :762; `LAWS` :329 is the cheat sheet (`buildCheatSheet` :345-354) | **level4 42** | **56** | – | count-wrong |
| like-terms-collector | stages `STAGE1` (5) → `STAGE2` (10) → `STAGE3` (30) :363-365 | **year6 45** | **40** (STAGE1 missed) | – | count-wrong |
| circle-theorem-spotter, core-maths-paper1/2a/2b/2c, decimal-detective, formula-plug-in, four-quadrant-explorer, linear-equation-solver, probability-pioneer, shape-shifter, think-of-a-number, truth-will-set-you-free | flat or all-stages-in-one-session | 55; 36 ×4; 45; 50; 45; 141; 45; 45; 50; 32 | same | core-maths 36 ×4, twsyf 32; others – | none |

### 3.1 Mismatches

**Hidden B4: the true pool is under 40, with no ledger entry. 26 level entries in 13 games.**

| Game | True pool under 40 | Cause |
|---|---|---|
| angle-ace | ks3 35 | gcse fallback, `:727`/`:735` |
| chart-interrogator | gcse 10, alevel 10, core 12, level4 8 | `:400` filter. Its L4 button key is `l4`, so `?level=level4` selects nothing |
| coordinate-geometry-dash | gcse 24, alevel 21 | `:311` |
| estimation-golf | core 9 | ks3 fallback, `:716` |
| formula-unlocked | gcse 29, alevel 25, level4 14 | `:395–397` |
| scale-factor-scaling | gcse 38, level4 31 | `:172–174` |
| spot-the-error | ks3 35, level4 30 | `:376` |
| spot-the-muppet | ks3 18, gcse 20, core 12 | `:401` |
| suvat | level4 8 | `:577` |
| unit-converter | alevel 38 | `:190` |
| prime-factorisation | year6 20, ks3 28, gcse 28 | static lists `:207–208` chosen at `:213`; extractor says GENERATOR |
| graph-transformer | gcse 25, alevel 25 | fixed `p.push` literals in `generatePuzzles()` `:201–258`; extractor says GENERATOR |
| tax-theft | core 20 salary scenarios | `SALARIES` `:794–798`; extractor says GENERATOR |

**False B4: a ledger entry at a level that never uses that bank, or for an array that is not questions,
or for a true pool of 40 or more. 10 entries in 5 games.**

| Game | Ledger says | True |
|---|---|---|
| factor-race ks3, gcse | 20 | generated from `VALID_PAIRS` (`:230–240`, `:255`); `YEAR6_BANK` is year6 only (`:204`) |
| fraction-equivalence ks3, gcse | 20 | generated by `generateQ()` (`:229–247`) |
| prisoners-dilemma, all four levels | 9 | `OPPONENTS` (`:926`) are strategy bots, not questions |
| proof-builder further | 10 | 50 (`:342–350`) |
| negative-number-line year6 | 30 | 45 (`:363–365`); `PLACE_QUESTIONS` is plain numbers, which the extractor does not see |

**False B4 with the wrong number: the level really is under 40, but the count is wrong. 5 entries in 2
games.**
- **percentage-flip.** The ledger says 32 at all three levels. The truth is **year6 20, ks3 12, gcse 12**
  (`:217`). **Correction to the contract and §1.35**, which say 12/12/20: the 12-question
  `QUESTIONS_DEFAULT` (`:173`) serves KS3 and GCSE, and the 20-question `QUESTIONS_YEAR6` (`:191`)
  serves Year 6.
- **glorious-gantt.** The ledger says 15 at both levels. The truth is core 7 and level4 8: the pool key is
  level plus mode (`:790–791`).

**Misclassified: 6 games.**
- prime-factorisation, graph-transformer and tax-theft serve static lists, but the extractor calls them
  generators.
- factor-race and fraction-equivalence generate at KS3 and GCSE, but the extractor calls them banks there.
- prisoners-dilemma has no question bank at all.

**Count wrong, with no effect on B4:**
- equation-builder 40/40/40 (E 120);
- word-problem-decoder 50/60 (E 110);
- sequence-solver level4 50 (E 154, ks3 fallback);
- trig-identity-duel level4 50 (E 99, gcse fallback);
- suvat alevel 50 (E 58);
- unit-converter gcse 48 and level4 42 (E 58);
- new-shapes 50 (E 100, counted twice through `ALL_QUESTIONS`);
- boolean-blitz 42 (E 56, `LAWS` is the cheat sheet);
- like-terms-collector 45 (E 40, `STAGE1` missed).

**Four games quietly serve another level's bank:** angle-ace (KS3 gets GCSE), estimation-golf (Core gets
KS3), sequence-solver (L4 gets KS3) and trig-identity-duel (L4 gets GCSE). This is the same defect as
section 2, group B, seen from the bank's side.

**Where the extractor misses it:**
- `scripts/extract-banks.py:448–449` sums every array on the page when no group's top path names the
  level:
  `scoped = [g for g in groups if lv and g["path"] and g["path"][0] == lv]`
  `pool_groups = scoped if scoped else groups`
- The misclassifications have two further causes:
  - candidates are only top-level SCREAMING_CASE declarations (`candidate_names`, `:104–113`), so
    graph-transformer's in-function literals are invisible;
  - `bank_common.find_question_groups` (`:328`) recognises only question-shaped objects, so plain number
    lists (prime-factorisation, tax-theft, negative-number-line's `PLACE_QUESTIONS`) are not counted.

---

## 4. Summary

### Class A: precision

**Affected (a right answer marked wrong), 14 games:**
- **At a stated precision:** growth-and-decay, stat-attack, test-the-claim and component-crusher.
- **Wrong key:** factor-theorem, graph-sketcher, glorious-gantt, tax-theft, fermi-lab and suvat.
- **Correct value in a form the game cannot read:** screening-room, factor-theorem and component-crusher.
- **No precision stated:** stat-attack (variance), split-it, given-that, chart-interrogator and
  test-the-claim (correlation).

**Wrong answers accepted at the asked precision:** 16 of 26 games (1.3). That excludes the three
band-mechanic games, percentage-flip's ±0.01 and log-laws' trailing-zero spelling.

**The shared code that misses it.** There is none, which is the finding: `schools/assets/` has no answer
marker, and every game rolls its own band. Nor does the bank checker test a key against its stem.
`scripts/check-banks.py:10–30` lists rules B1–B11, and none compares a key with its stem's stated
precision or with its own marking band. The one verifier that tests marking at all,
`scripts/verify-chart-interrogator.py`, deliberately pins exact stem-and-leaf marking.

**Most of the worst cases are wrong keys, not bands.**
- **The shared marker alone will not fix:** factor-theorem T4(b), graph-sketcher's eight keys,
  glorious-gantt's six, tax-theft over £100k, component-crusher's bearing, growth-and-decay's four,
  stat-attack's eight variances, fermi-lab's 17 chains and suvat AL34. Each needs its key corrected.
- **What would have caught them is layer C**, which recomputes each key from its own parameters
  (`docs/checker-tier4-design.md`).
- **The marker fixes:** the stated-precision rejections in test-the-claim, stat-attack's means and
  growth-and-decay's absolute sq4 band, and every wrong-answer acceptance in 1.3.

**Proposed precision kinds for `schools/assets/answer.js`**, each drawn from what a game actually asks:

| Kind | Asked by | Notes |
|---|---|---|
| `dp(n)`, n = 1, 2, 4 | growth-and-decay CM2 (1); test-the-claim z and CV, component-crusher, quadratic-factoriser, estimation-golf `:665` (2); test-the-claim p-value (4) | Accept exactly the correctly rounded value; reject other values at that precision. Decide whether a shorter spelling of a trailing zero (2.1 for 2.10) is accepted, as log-laws does today on 102 items |
| `sf(n)`, n = 2, 3, 4 | growth-and-decay (all three); stat-attack mean and SD (3); log-laws (3); estimation-golf `:651`, `:662` | Keys must be stored unrounded or as the true value, never pre-rounded to another precision. Mark from the `sf` field growth-and-decay already carries (Jon's ruling, 2 Oct 2026) |
| `integer` | glorious-gantt, think-of-a-number, six-sevens-bruv, 52dle, like-terms-collector, split-it ratio parts, test-the-claim boundaries | Reject decimals, never truncate with `parseInt` |
| `money` | split-it £/€; tax-theft | Jon's rule: whole pounds may be an integer; with pence, exactly 2 d.p. Three outcomes: correct, wrong, right value in the wrong form. A leading £ and thousands commas are readable |
| `nearest(k)` | estimation-golf `:640` (hundred), `:669` (whole number) | Rounding to a stated unit |
| `bearing` | component-crusher AL11.2 | Integer degrees 000–359; leading zeros readable |
| `rational` (fraction, decimal or %) | given-that, screening-room | Exact fraction compared exactly; decimal and % at a stated precision; thousands separators readable |
| `interval` | stat-attack modal and median class | Compare bounds numerically (3.0 = 3) and respect the inequality signs |
| `exact-algebra` | factor-theorem, quadratic-factoriser (pickers already do this) | Equivalence by expansion, order-free factors and root sets, `^2` = ², an optional `x =` prefix. Free-text proofs cannot be string-matched |
| `surd` | component-crusher AL5.2 | Or drop the surd option from the ask |

**Input layer, common to every kind:** read the raw string from a `type="text" inputmode="decimal"`
input, never `type="number"`. Accept a Unicode minus, and say why an unreadable entry was not marked,
rather than doing nothing.

**Not for the marker:** the three games whose band is the mechanic (estimation-engine, estimation-golf
and fermi-lab, section 1.0). The marker should not absorb them. Their defects are keys (1.4) and parsing
(1.7).

### Class B: level routing

**Affected:**
- **8 games live:** percentage-flip, fraction-equivalence, prime-factorisation, factor-race, angle-ace,
  sequence-solver, trig-identity-duel and estimation-golf (gated).
- **3 more with levels reachable only by a typed URL:** expected-damage, fermi-lab and log-laws.
- **6 that accept any typed level:** complex-converter, differentiation-duel, scale-factor-scaling,
  unit-converter, suvat and split-it.
- **19 with tiers merged on one board.** 36 of 95 in all.

**The shared code that misses it:** `scripts/check-leaderboard-coverage.js:246`,
`return [...new Set((roster[slug] || []).concat(literals))].sort();`. A variable level is assumed to take
the roster's tiers instead of being traced. For literal levels (`:245`), nothing compares the literal
with the tiers served.

### Class C: bank attribution

**Affected (27 of 96 examined):**
- **13 with hidden B4 shortfalls:** angle-ace, chart-interrogator, coordinate-geometry-dash,
  estimation-golf, formula-unlocked, scale-factor-scaling, spot-the-error, spot-the-muppet, suvat,
  unit-converter, prime-factorisation, graph-transformer and tax-theft.
- **7 with false or wrong-number B4 entries:** factor-race, fraction-equivalence, prisoners-dilemma,
  proof-builder, negative-number-line, percentage-flip and glorious-gantt.
- **Misclassified:** 6 games, all already named above.
- **9 more with wrong counts that do not change a B4 outcome:** equation-builder, word-problem-decoder,
  sequence-solver, trig-identity-duel, suvat, unit-converter, new-shapes, boolean-blitz and
  like-terms-collector.

**The shared code that misses it:** `scripts/extract-banks.py:449`, `pool_groups = scoped if scoped else
groups`. With no level-named key, every array on the page is summed into every level. It is compounded by
`candidate_names` (`:104–113`, top-level declarations only) and `bank_common.find_question_groups`
(`:328`, question-shaped objects only).

---

## 5. Side findings

Outside the three classes; recorded so they are not lost.

1. **52dle `:681` states a false fact.** "52! arrangements — more than atoms in the observable universe."
   - 52! ≈ 8.07 × 10⁶⁷, while the observable universe holds roughly 10⁷⁸ to 10⁸² atoms (about 10⁸⁰), so
     52! is about 10¹² times too small.
   - The claim would be true of the atoms in the Earth, about 10⁵⁰.
   - It is in a daily puzzle clue, which every player of that puzzle reads.
2. **higher-power's Pairs and Hi-Lo modes share one board in opposite directions.**
   - Hi-Lo submits a streak, where higher is better (`:624`). Pairs submits its attempt count, where
     lower is better and 10 is a perfect game (`:753`, `:775`). Both use `currentLevel`, so both write
     `higher_power_<level>`.
   - **This is already known and contained:**
     - `schools/assets/firebase-leaderboard.js:189` declares `MIXED_UNRELIABLE = { 'higher-power': true }`
       ("flagged to Jon, not fixed here");
     - the hub replaces the board with a "Flagged, not yet fixed" note (`leaderboards/index.html:359–363`);
     - the in-game standing is marked not rankable (`firebase-leaderboard.js:517`);
     - `docs/todo.md:430` lists the per-mode sort-direction fix.
   - The scores still mix in the database.
