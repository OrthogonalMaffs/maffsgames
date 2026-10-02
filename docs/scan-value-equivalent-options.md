# Scan: options that are different strings but equal in value

28 Sep 2026. Step 1 of the `coordinate-geometry-dash:233` contract, run read-only against `main` at
`7f0d3e5`. Reproduce it with `python scripts/scan-value-equivalent-options.py` (its `--selftest` runs
the 32 fixtures). Committed at Jon's instruction as the evidence for
`docs/next-contract-value-equivalent-options.md` (DRAFT).

**Re-run, 1 Oct 2026 (end of this file):** the scan is now deterministic and every pair is classified. Group A is **39 questions in 12 games**; read that section first.

**Since the scan:** `coordinate-geometry-dash:233` is fixed on the same branch (√50 replaced by 50,
Jon's ruling), so group A now stands at **32 pairs in 10 games**. A rescan after the fix finds 229
pairs, exactly one fewer.

## Scope and method

- **Banks:** `data/banks/*.json`, freshly extracted from `main`. 81 of 94 games have a bank (80 live, 1 static fallback). The 13 generators build options at runtime and are **not covered**. In this environment that includes `boolean-blitz`, whose real bank CI can extract but this container cannot (it finds only `LAWS`).
- **Options:** walked with the same `bank_common` helpers as `check-banks.py` B2. Distinct strings only, since B2 already catches identical ones.
- **Coverage:** 10646 options, 6989 parsed, **3657 unparsed and not examined** (prose, units in words, inequalities, intervals).
- **Equality:** SymPy `simplify` of the difference, with a relative numeric fallback. Also handled: ratios reduced by their HCF, coordinates compared element-wise, and equations compared up to a constant multiple.
- **Scanner proof:** 32 fixtures, 17 equal pairs and 15 look-alike unequal pairs. They caught two scanner bugs, both fixed before the final run. `50%` had parsed as 0, and an absolute tolerance made every number below 10⁻¹² "equal".

## Result: 230 pairs in 21 games

| Category | Pairs | Games |
|---|---|---|
| A. The marked answer is offered twice, and the question does not ask for a form (must fix) | 33 | `binomial-blaster` 5, `circle-theorem-spotter` 1, `coordinate-geometry-dash` 1, `curling-friction` 1, `force-resolver` 2, `probability-paradox` 2, `probability-pioneer` 8, `proportion-blaster` 2, `sequence-solver` 5, `simultaneous-solver` 4, `trig-identity-duel` 2 |
| B. The marked answer is offered twice; the game is about form, but this question does not say which form (teaching call) | 53 | `standard-form-blitz` 30, `surd-simplifier` 23 |
| C. The form is what the question asks for (deliberate; keep) | 103 | `decimal-detective` 1, `proof-builder` 2, `sequence-solver` 1, `standard-form-blitz` 47, `surd-simplifier` 52 |
| D. Two wrong options are equal in value (no right answer is marked wrong, but one option is wasted) | 31 | `complex-converter` 2, `coordinate-geometry-dash` 1, `decimal-detective` 1, `formula-unlocked` 1, `given-that` 2, `probability-paradox` 1, `probability-pioneer` 4, `proportion-blaster` 5, `scale-factor-scaling` 2, `sequence-solver` 1, `simultaneous-solver` 2, `standard-form-blitz` 1, `surd-simplifier` 8 |
| E. Scanner false positives (discarded) | 10 | `complex-converter` 6, `core-maths-paper1` 3, `moments-master` 1 |

## A. The marked answer is offered twice, and the question does not ask for a form (must fix)

| Game | Where | The pair | Marked answer | Question / ask |
|---|---|---|---|---|
| `binomial-blaster` | `QUESTIONS.alevel2[26]` | `0.97090` · `0.9709` | `0.97090` | Estimate using first 3 terms \dfrac{1}{1.03} \approx (1+0.03)^{-1} |
| `binomial-blaster` | `QUESTIONS.alevel2[27]` | `1.02040` · `1.0204` | `1.02040` | Estimate using first 3 terms \dfrac{1}{0.98} \approx (1-0.02)^{-1} |
| `binomial-blaster` | `QUESTIONS.alevel2[29]` | `1.06270` · `1.0627` | `1.06270` | Estimate using first 3 terms (0.97)^{-2} \approx (1-0.03)^{-2} |
| `binomial-blaster` | `QUESTIONS.alevel2[49]` | `1` · `1 + 0x + 0x^2` | `1` | Expansion (1+x)^0 |
| `binomial-blaster` | `QUESTIONS.alevel[10]` | `1 + 3x + 3x^2 + x^3` · `1 + 3x^2 + 3x + x^3` | `1 + 3x + 3x^2 + x^3` | Expand fully (1+x)^3 |
| `circle-theorem-spotter` | `QUESTIONS.gcse[53]` | `8` · `\sqrt{64}` | `8` | Find AB |
| `coordinate-geometry-dash` | `Q_GCSE[16]` | `5√2` · `√50` | `5√2` | Distance AB? |
| `curling-friction` | `QUESTIONS.alevel[47]` | `3 \text{ m/s}` · `\sqrt{9} \text{ m/s}` | `3 \text{ m/s}` | Speed of A when it reaches B |
| `force-resolver` | `QUESTIONS.alevel[7]` | `10 \text{ N}` · `\sqrt{100} \text{ N}` | `10 \text{ N}` | Find the magnitude of the force R = \sqrt{F_x^2 + F_y^2} |
| `force-resolver` | `QUESTIONS.alevel[9]` | `13 \text{ N}` · `\sqrt{169} \text{ N}` | `13 \text{ N}` | Resultant magnitude |
| `probability-paradox` | `CONDITIONAL_QUESTIONS[10]` | `9/19` · `18/38` | `9/19` | An item is defective. P(made by X)? |
| `probability-paradox` | `CONDITIONAL_QUESTIONS[12]` | `1/3` · `4/12` | `1/3` | P(King \| Face card)? |
| `probability-pioneer` | `STAGE2[13]` | `1/3` · `2/6` | `1/3` | P(rolling 1 or 2) |
| `probability-pioneer` | `STAGE2[14]` | `3/13` · `12/52` | `3/13` | P(face card from 52) |
| `probability-pioneer` | `STAGE2[15]` | `1/2` · `3/6` | `1/2` | P(prime on a die) |
| `probability-pioneer` | `STAGE2[16]` | `1/5` · `2/10` | `1/5` | P(yellow from 8R, 2Y) |
| `probability-pioneer` | `STAGE2[17]` | `1/3` · `2/6` | `1/3` | P(square number on a die) |
| `probability-pioneer` | `STAGE2[18]` | `1/2` · `4/8` | `1/2` | P(even from 1–8) |
| `probability-pioneer` | `STAGE2[5]` | `3/5` · `6/10` | `3/5` | P(blue from 4 red, 6 blue) |
| `probability-pioneer` | `STAGE2[7]` | `1/4` · `13/52` | `1/4` | P(heart from 52 cards) |
| `proportion-blaster` | `QUESTIONS.alevel[18]` | `2` · `\dfrac{10}{5}` | `2` | Find y when x = 6 y = \dfrac{k}{x-1} |
| `proportion-blaster` | `QUESTIONS.gcse[33]` | `\dfrac{4}{3}` · `\dfrac{12}{9}` | `\dfrac{4}{3}` | Find y when x = 3 y = \dfrac{k}{x^2} |
| `sequence-solver` | `QUESTIONS.alevel[4]` | `4` · `\dfrac{36}{9}` | `4` | Find d S_{10} = 200, a = 2 |
| `sequence-solver` | `QUESTIONS.gcse[23]` | `n^2 + n` · `n(n+1)` | `n^2 + n` | Find the nth term |
| `sequence-solver` | `QUESTIONS.gcse[24]` | `n^2 + 2n` · `n(n+2)` | `n^2 + 2n` | Find the nth term |
| `sequence-solver` | `QUESTIONS.gcse[7]` | `22 - 2n` · `-2n + 22` | `22 - 2n` | Find the nth term |
| `sequence-solver` | `QUESTIONS.gcse[8]` | `3n - 3` · `3(n-1)` | `3n - 3` | Find the nth term |
| `simultaneous-solver` | `QUESTIONS.alevel[0]` | `2` · `\tfrac{34}{17}` | `2` | Find x |
| `simultaneous-solver` | `QUESTIONS.alevel[35]` | `5` · `\sqrt{25}` | `5` | Find the positive x value |
| `simultaneous-solver` | `QUESTIONS.alevel[42]` | `5` · `\sqrt{25}` | `5` | Find the positive x value |
| `simultaneous-solver` | `QUESTIONS.alevel[45]` | `3` · `\sqrt{9}` | `3` | Find the positive y value |
| `trig-identity-duel` | `QUESTIONS.gcse[25]` | `10` · `\sqrt{100}` | `10` | Find c c^2 = a^2 + b^2 - 2ab\cos C |
| `trig-identity-duel` | `QUESTIONS.gcse[2]` | `\dfrac{1}{\sqrt{3}}` · `\dfrac{\sqrt{3}}{3}` | `\dfrac{1}{\sqrt{3}}` | Exact value \tan 30° |

## B. The marked answer is offered twice; the game is about form, but this question does not say which form (teaching call)

| Game | Where | The pair | Marked answer | Question / ask |
|---|---|---|---|---|
| `standard-form-blitz` | `QUESTIONS.alevel[0]` | `1.44 \times 10^3` · `14.4 \times 10^2` | `1.44 \times 10^3` | Calculate (3.2 \times 10^5) \times (4.5 \times 10^{-3}) |
| `standard-form-blitz` | `QUESTIONS.alevel[11]` | `8 \times 10^5` · `80 \times 10^4` | `8 \times 10^5` | Calculate (4.2 \times 10^5) + (3.8 \times 10^5) |
| `standard-form-blitz` | `QUESTIONS.alevel[13]` | `6.8 \times 10^5` · `68 \times 10^4` | `6.8 \times 10^5` | Calculate (6 \times 10^5) + (8 \times 10^4) |
| `standard-form-blitz` | `QUESTIONS.alevel[15]` | `3.5 \times 10^6` · `35 \times 10^5` | `3.5 \times 10^6` | Calculate (5.2 \times 10^6) - (1.7 \times 10^6) |
| `standard-form-blitz` | `QUESTIONS.alevel[16]` | `2.5 \times 10^4` · `25 \times 10^3` | `2.5 \times 10^4` | Calculate (3 \times 10^4) - (5 \times 10^3) |
| `standard-form-blitz` | `QUESTIONS.alevel[17]` | `1.3 \times 10^{-2}` · `13 \times 10^{-3}` | `1.3 \times 10^{-2}` | Calculate (1 \times 10^{-2}) + (3 \times 10^{-3}) |
| `standard-form-blitz` | `QUESTIONS.alevel[18]` | `4.8 \times 10^{-4}` · `48 \times 10^{-5}` | `4.8 \times 10^{-4}` | Calculate (5 \times 10^{-4}) - (2 \times 10^{-5}) |
| `standard-form-blitz` | `QUESTIONS.alevel[19]` | `3.25 \times 10^7` · `32.5 \times 10^6` | `3.25 \times 10^7` | Calculate (2.5 \times 10^7) + (7.5 \times 10^6) |
| `standard-form-blitz` | `QUESTIONS.alevel[1]` | `2.52 \times 10^{-6}` · `25.2 \times 10^{-7}` | `2.52 \times 10^{-6}` | Calculate (8.4 \times 10^{-2}) \times (3 \times 10^{-5}) |
| `standard-form-blitz` | `QUESTIONS.alevel[20]` | `9.9 \times 10^7` · `99 \times 10^6` | `9.9 \times 10^7` | Calculate (1 \times 10^8) - (1 \times 10^6) |
| `standard-form-blitz` | `QUESTIONS.alevel[21]` | `1 \times 10^6` · `10 \times 10^5` | `1 \times 10^6` | Calculate (4 \times 10^5) + (6 \times 10^5) |
| `standard-form-blitz` | `QUESTIONS.alevel[22]` | `1 \times 10^4` · `10 \times 10^3` | `1 \times 10^4` | Calculate (9.9 \times 10^3) + (1 \times 10^2) |
| `standard-form-blitz` | `QUESTIONS.alevel[23]` | `1 \times 10^{-2}` · `10 \times 10^{-3}` | `1 \times 10^{-2}` | Calculate (8 \times 10^{-3}) + (2 \times 10^{-3}) |
| `standard-form-blitz` | `QUESTIONS.alevel[24]` | `1 \times 10^7` · `0.01 \times 10^9` | `1 \times 10^7` | Calculate (3 \times 10^9) - (2.99 \times 10^9) |
| `standard-form-blitz` | `QUESTIONS.alevel[2]` | `3.90625 \times 10^9` · `39.0625 \times 10^8` | `3.90625 \times 10^9` | Calculate (6.25 \times 10^4)^2 |
| `standard-form-blitz` | `QUESTIONS.alevel[34]` | `5 \times 10^{-4}` · `0.5 \times 10^{-3}` | `5 \times 10^{-4}` | Calculate (2 \times 10^3)^{-1} |
| `standard-form-blitz` | `QUESTIONS.alevel[36]` | `2 \times 10^3` · `20 \times 10^2` | `2 \times 10^3` | Calculate (4 \times 10^6)^{0.5} |
| `standard-form-blitz` | `QUESTIONS.alevel[5]` | `6.4 \times 10^{10}` · `64 \times 10^9` | `6.4 \times 10^{10}` | Calculate (4 \times 10^3)^3 |
| `standard-form-blitz` | `QUESTIONS.alevel[7]` | `4 \times 10^7` · `0.4 \times 10^8` | `4 \times 10^7` | Calculate \dfrac{2 \times 10^6}{5 \times 10^{-2}} |
| `standard-form-blitz` | `QUESTIONS.gcse[20]` | `3 \times 10^7` · `30 \times 10^6` | `3 \times 10^7` | Calculate (5 \times 10^2) \times (6 \times 10^4) |
| `standard-form-blitz` | `QUESTIONS.gcse[21]` | `1.2 \times 10^4` · `12 \times 10^3` | `1.2 \times 10^4` | Calculate (3 \times 10^{-2}) \times (4 \times 10^5) |
| `standard-form-blitz` | `QUESTIONS.gcse[22]` | `4 \times 10^2` · `40 \times 10^1` | `4 \times 10^2` | Calculate (8 \times 10^3) \times (5 \times 10^{-2}) |
| `standard-form-blitz` | `QUESTIONS.gcse[23]` | `1.4 \times 10^{-6}` · `14 \times 10^{-7}` | `1.4 \times 10^{-6}` | Calculate (7 \times 10^{-3}) \times (2 \times 10^{-4}) |
| `standard-form-blitz` | `QUESTIONS.gcse[24]` | `1 \times 10^7` · `10 \times 10^6` | `1 \times 10^7` | Calculate (2.5 \times 10^4) \times (4 \times 10^2) |
| `standard-form-blitz` | `QUESTIONS.gcse[25]` | `3.6 \times 10^5` · `36 \times 10^4` | `3.6 \times 10^5` | Calculate (6 \times 10^2) \times (6 \times 10^2) |
| `standard-form-blitz` | `QUESTIONS.gcse[26]` | `3 \times 10^2` · `30 \times 10^1` | `3 \times 10^2` | Calculate (1.5 \times 10^3) \times (2 \times 10^{-1}) |
| `standard-form-blitz` | `QUESTIONS.gcse[27]` | `2.7 \times 10^4` · `27 \times 10^3` | `2.7 \times 10^4` | Calculate (9 \times 10^8) \times (3 \times 10^{-5}) |
| `standard-form-blitz` | `QUESTIONS.gcse[31]` | `5 \times 10^2` · `0.5 \times 10^3` | `5 \times 10^2` | Calculate (3 \times 10^{-2}) \div (6 \times 10^{-5}) |
| `standard-form-blitz` | `QUESTIONS.gcse[36]` | `8 \times 10^2` · `0.8 \times 10^3` | `8 \times 10^2` | Calculate (7.2 \times 10^{-1}) \div (9 \times 10^{-4}) |
| `standard-form-blitz` | `QUESTIONS.gcse[37]` | `3 \times 10^4` · `0.3 \times 10^5` | `3 \times 10^4` | Calculate (1.8 \times 10^{12}) \div (6 \times 10^7) |
| `surd-simplifier` | `QUESTIONS.alevel[30]` | `\dfrac{1}{3}` · `\dfrac{3}{9}` | `\dfrac{1}{3}` | Convert to a fraction 0.\dot{3} |
| `surd-simplifier` | `QUESTIONS.alevel[31]` | `\dfrac{2}{11}` · `\dfrac{18}{99}` | `\dfrac{2}{11}` | Convert to a fraction 0.\dot{1}\dot{8} |
| `surd-simplifier` | `QUESTIONS.alevel[31]` | `\dfrac{2}{11}` · `\dfrac{6}{33}` | `\dfrac{2}{11}` | Convert to a fraction 0.\dot{1}\dot{8} |
| `surd-simplifier` | `QUESTIONS.alevel[32]` | `\dfrac{6}{11}` · `\dfrac{54}{99}` | `\dfrac{6}{11}` | Convert to a fraction 0.\dot{5}\dot{4} |
| `surd-simplifier` | `QUESTIONS.alevel[32]` | `\dfrac{6}{11}` · `\dfrac{18}{33}` | `\dfrac{6}{11}` | Convert to a fraction 0.\dot{5}\dot{4} |
| `surd-simplifier` | `QUESTIONS.alevel[36]` | `1` · `\dfrac{9}{9}` | `1` | Convert to a fraction 0.\dot{9} |
| `surd-simplifier` | `QUESTIONS.alevel[38]` | `\dfrac{1}{7}` · `\dfrac{142857}{999999}` | `\dfrac{1}{7}` | Convert to a fraction 0.\dot{1}4285\dot{7} |
| `surd-simplifier` | `QUESTIONS.alevel[39]` | `\dfrac{8}{11}` · `\dfrac{72}{99}` | `\dfrac{8}{11}` | Convert to a fraction 0.\dot{7}\dot{2} |
| `surd-simplifier` | `QUESTIONS.alevel[39]` | `\dfrac{8}{11}` · `\dfrac{24}{33}` | `\dfrac{8}{11}` | Convert to a fraction 0.\dot{7}\dot{2} |
| `surd-simplifier` | `QUESTIONS.alevel[45]` | `4` · `9-5` | `4` | Expand (3+\sqrt{5})(3-\sqrt{5}) |
| `surd-simplifier` | `QUESTIONS.gcse[35]` | `\dfrac{1}{3}` · `\dfrac{3}{9}` | `\dfrac{1}{3}` | Convert to a fraction 0.\dot{3} |
| `surd-simplifier` | `QUESTIONS.gcse[36]` | `\dfrac{2}{3}` · `\dfrac{6}{9}` | `\dfrac{2}{3}` | Convert to a fraction 0.\dot{6} |
| `surd-simplifier` | `QUESTIONS.gcse[40]` | `\dfrac{1}{11}` · `\dfrac{9}{99}` | `\dfrac{1}{11}` | Convert to a fraction 0.\dot{0}\dot{9} |
| `surd-simplifier` | `QUESTIONS.gcse[41]` | `\dfrac{4}{33}` · `\dfrac{12}{99}` | `\dfrac{4}{33}` | Convert to a fraction 0.\dot{1}\dot{2} |
| `surd-simplifier` | `QUESTIONS.gcse[42]` | `\dfrac{3}{11}` · `\dfrac{27}{99}` | `\dfrac{3}{11}` | Convert to a fraction 0.\dot{2}\dot{7} |
| `surd-simplifier` | `QUESTIONS.gcse[42]` | `\dfrac{3}{11}` · `\dfrac{9}{33}` | `\dfrac{3}{11}` | Convert to a fraction 0.\dot{2}\dot{7} |
| `surd-simplifier` | `QUESTIONS.gcse[43]` | `\dfrac{5}{11}` · `\dfrac{45}{99}` | `\dfrac{5}{11}` | Convert to a fraction 0.\dot{4}\dot{5} |
| `surd-simplifier` | `QUESTIONS.gcse[44]` | `\dfrac{9}{11}` · `\dfrac{81}{99}` | `\dfrac{9}{11}` | Convert to a fraction 0.\dot{8}\dot{1} |
| `surd-simplifier` | `QUESTIONS.gcse[44]` | `\dfrac{9}{11}` · `\dfrac{27}{33}` | `\dfrac{9}{11}` | Convert to a fraction 0.\dot{8}\dot{1} |
| `surd-simplifier` | `QUESTIONS.gcse[47]` | `\dfrac{1}{7}` · `\dfrac{142857}{999999}` | `\dfrac{1}{7}` | Convert to a fraction 0.\dot{1}4285\dot{7} |
| `surd-simplifier` | `QUESTIONS.gcse[48]` | `1` · `\dfrac{9}{9}` | `1` | Convert to a fraction 0.\dot{9} |
| `surd-simplifier` | `QUESTIONS.gcse[49]` | `\dfrac{4}{11}` · `\dfrac{36}{99}` | `\dfrac{4}{11}` | Convert to a fraction 0.\dot{3}\dot{6} |
| `surd-simplifier` | `QUESTIONS.gcse[49]` | `\dfrac{4}{11}` · `\dfrac{12}{33}` | `\dfrac{4}{11}` | Convert to a fraction 0.\dot{3}\dot{6} |

## D. Two wrong options are equal in value (no right answer is marked wrong, but one option is wasted)

| Game | Where | The pair | Marked answer | Question / ask |
|---|---|---|---|---|
| `complex-converter` | `QUESTIONS.further[42]` | `7j` · `0 + 7j` | `7` | This phasor has zero phase angle. What is its rectangular form? |
| `complex-converter` | `QUESTIONS.level4[42]` | `7j` · `0 + 7j` | `7` | This phasor has zero phase angle. What is its rectangular form? |
| `coordinate-geometry-dash` | `Q_ALEVEL[15]` | `½` · `1/2` | `1` | Find dy/dx at t = 1 |
| `decimal-detective` | `ROUNDUP_QUESTIONS[7]` | `9.5` · `9.50` | `10` |  |
| `formula-unlocked` | `Q_GCSE[22]` | `r = \dfrac{3V}{4\pi}` · `r = \dfrac{V}{\frac{4}{3}\pi}` | `r = \sqrt[3]{\dfrac{3V}{4\pi}}` |  |
| `given-that` | `QUESTIONS.gcse[13].phase2` | `\tfrac{60}{180}` · `\tfrac{30}{90}` | `0.6667` | 180 trials, even/odd dice, then red/blue spinner |
| `given-that` | `QUESTIONS.gcse[22].phase2` | `\tfrac{20}{30}` · `\tfrac{50}{75}` | `0.4` | Households, Netflix, Disney+ |
| `probability-paradox` | `CONDITIONAL_QUESTIONS[12]` | `4/52` · `1/13` | `1/3` | P(King \| Face card)? |
| `probability-pioneer` | `STAGE2[12]` | `1/2` · `2/4` | `1/4` | P(heads twice in a row) |
| `probability-pioneer` | `STAGE2[5]` | `2/5` · `4/10` | `3/5` | P(blue from 4 red, 6 blue) |
| `probability-pioneer` | `STAGE2[7]` | `1/13` · `4/52` | `1/4` | P(heart from 52 cards) |
| `probability-pioneer` | `STAGE2[8]` | `2/3` · `4/6` | `1/3` | P(rolling greater than 4) |
| `proportion-blaster` | `QUESTIONS.alevel[30]` | `2 : 5 : 7` · `6 : 15 : 21` | `6 : 15 : 35` | Find a : b : c |
| `proportion-blaster` | `QUESTIONS.alevel[47]` | `50` · `\dfrac{150}{3}` | `\dfrac{450}{11}` | Find c |
| `proportion-blaster` | `QUESTIONS.gcse[16]` | `10` · `\sqrt{100}` | `5` | Find x when y = 100 y = kx^2 |
| `proportion-blaster` | `QUESTIONS.gcse[44]` | `3 : 4 : 5` · `6 : 8 : 10` | `3 : 4 : 10` | Find a : b : c |
| `proportion-blaster` | `QUESTIONS.gcse[45]` | `5 : 4 : 3` · `10 : 8 : 6` | `5 : 8 : 6` | Find x : y : z |
| `scale-factor-scaling` | `T1[8]` | `2:5` · `4:10` | `4:25` | Similar shapes. Lengths in ratio 2:5. Area ratio = ? |
| `scale-factor-scaling` | `T1[9]` | `1:3` · `3:9` | `1:9` | Similar triangles. Sides 3 cm and 9 cm. Area ratio = ? |
| `sequence-solver` | `QUESTIONS.gcse[6]` | `-3n + 10` · `10 - 3n` | `13 - 3n` | Find the nth term |
| `simultaneous-solver` | `QUESTIONS.alevel[46]` | `5` · `\sqrt{25}` | `4` | Find the larger x value |
| `simultaneous-solver` | `QUESTIONS.alevel[48]` | `2` · `\sqrt{4}` | `\sqrt{2}` | Find the positive x value |
| `standard-form-blitz` | `QUESTIONS.alevel[35]` | `2.5 \times 10^{3}` · `25 \times 10^{2}` | `4 \times 10^2` | Calculate (5 \times 10^{-2})^{-2} |
| `surd-simplifier` | `QUESTIONS.alevel[31]` | `\dfrac{18}{99}` · `\dfrac{6}{33}` | `\dfrac{2}{11}` | Convert to a fraction 0.\dot{1}\dot{8} |
| `surd-simplifier` | `QUESTIONS.alevel[32]` | `\dfrac{54}{99}` · `\dfrac{18}{33}` | `\dfrac{6}{11}` | Convert to a fraction 0.\dot{5}\dot{4} |
| `surd-simplifier` | `QUESTIONS.alevel[39]` | `\dfrac{72}{99}` · `\dfrac{24}{33}` | `\dfrac{8}{11}` | Convert to a fraction 0.\dot{7}\dot{2} |
| `surd-simplifier` | `QUESTIONS.gcse[38]` | `\dfrac{1}{5}` · `\dfrac{2}{10}` | `\dfrac{2}{9}` | Convert to a fraction 0.\dot{2} |
| `surd-simplifier` | `QUESTIONS.gcse[42]` | `\dfrac{27}{99}` · `\dfrac{9}{33}` | `\dfrac{3}{11}` | Convert to a fraction 0.\dot{2}\dot{7} |
| `surd-simplifier` | `QUESTIONS.gcse[43]` | `\dfrac{45}{100}` · `\dfrac{9}{20}` | `\dfrac{5}{11}` | Convert to a fraction 0.\dot{4}\dot{5} |
| `surd-simplifier` | `QUESTIONS.gcse[44]` | `\dfrac{81}{99}` · `\dfrac{27}{33}` | `\dfrac{9}{11}` | Convert to a fraction 0.\dot{8}\dot{1} |
| `surd-simplifier` | `QUESTIONS.gcse[49]` | `\dfrac{36}{99}` · `\dfrac{12}{33}` | `\dfrac{4}{11}` | Convert to a fraction 0.\dot{3}\dot{6} |

## E. Scanner false positives (discarded)

| Game | Where | The pair | Marked answer | Question / ask |
|---|---|---|---|---|
| `complex-converter` | `QUESTIONS.further[15]` | `10e^{j0.927}` · `10e^{j0.644}` | `10e^{j0.927}` | Convert this voltage to exponential form. |
| `complex-converter` | `QUESTIONS.further[1]` | `5e^{j0.927}` · `5e^{j0.644}` | `5e^{j0.927}` | Write this phasor in exponential form. |
| `complex-converter` | `QUESTIONS.further[3]` | `5e^{j0.927}` · `5e^{j0.644}` | `5e^{j0.927}` | Express in exponential form. |
| `complex-converter` | `QUESTIONS.level4[15]` | `10e^{j0.927}` · `10e^{j0.644}` | `10e^{j0.927}` | Convert this voltage to exponential form. |
| `complex-converter` | `QUESTIONS.level4[1]` | `5e^{j0.927}` · `5e^{j0.644}` | `5e^{j0.927}` | Write this phasor in exponential form. |
| `complex-converter` | `QUESTIONS.level4[3]` | `5e^{j0.927}` · `5e^{j0.644}` | `5e^{j0.927}` | Express in exponential form. |
| `core-maths-paper1` | `QUESTIONS[11]` | `20–40` · `40–60` | `1` |  |
| `core-maths-paper1` | `QUESTIONS[11]` | `20–40` · `60–80` | `1` |  |
| `core-maths-paper1` | `QUESTIONS[11]` | `40–60` · `60–80` | `1` |  |
| `moments-master` | `QUESTIONS.alevel[10]` | `1 \text{ Nm anticlockwise}` · `1 \text{ Nm clockwise}` | `1 \text{ Nm anticlockwise}` | Net moment about the pivot |

## C. The form is what the question asks for (deliberate; keep)

Not listed row by row. 103 pairs: `standard-form-blitz` 47 (asks "Write in standard form"), `surd-simplifier` 52 (asks "Simplify" or "Rationalise"), `decimal-detective` 1 ("Round to 2 decimal places": 7.90 against 7.9), `proof-builder` 2 (an induction step whose factorised form is the target), and `sequence-solver` `alevel[23]` 1 ("Which formula when |r| < 1?", which asks for the conventional form of the geometric-series sum). A future check needs a way to declare these deliberate; see the recommendation.

## What this means for the contract

**STOP IF fired.** The scan found value-equal pairs in games other than `coordinate-geometry-dash`.
`:233` is one of 33 must-fix pairs in 11 games, so this is a class, and the contract says to report
rather than patch.

**Recommended architectural fix**, drafted as `docs/next-contract-value-equivalent-options.md`:

1. **A `check-banks.py` rule, "options equal in value"**, using this scan's normaliser and its
   fixture set as `--selftest` cases. SymPy is already a CI dependency
   (`.github/workflows/check-site.yml:49`), so it adds nothing to install.
2. **Record the current hits in `data/check-ledger.json`.** Existing ones are tracked, and any new one
   fails CI, the same as B1–B10.
3. **Keep category C with a written reason.** A reviewed list of deliberate form questions, keyed on
   game plus question content rather than line number: the `checker-allowlist.json` rule, and to-do
   item 7's point about ledger identity.

**The content fixes then go in batches, and each one is a teaching call:**

- **Category A:** a replacement distractor per item, drawn from a real misconception, as `:233`'s
  "50" is.
- **Category B has a cheap class fix:** put the required form in the ask. For example,
  `standard-form-blitz` "Calculate. Give your answer in standard form." and `surd-simplifier`
  "Convert to a fraction in its simplest form." That resolves 53 pairs with no new distractors.
- **Category D** wastes an option but marks no right answer wrong. It is the lowest priority.

**Not covered:** the 13 generator games, where options are built at runtime (Trig Worms shipped a
duplicate that way), and the 3,657 unparsed options. This is a floor, not a census.

---

## Re-run, 1 Oct 2026: the scan made deterministic, every pair classified

A re-run on 1 Oct found more pairs than this report, all of them in six games unchanged since 28 Sep.
Neither count could be trusted until the cause was found, so the scan was fixed before any
classification. **No question is fixed here, and B11 is not built.**

### Why the two runs differed: two environment dependencies

1. **Extraction needs the KaTeX CDN.** `differentiation-duel`, `index-laws` and `integration-duel` do
   not load without KaTeX. The 28 Sep run was made in a cloud sandbox that refuses `cdn.jsdelivr.net`
   (`docs/sandbox-checks.md`), so `extract-banks.py` marked all three `unreadable` and the scan saw no
   options from them. Evidence: re-extracting the three here with only `cdn.jsdelivr.net` blocked turns
   each from `read_method: live` into `unreadable` with an empty bank, while `core-maths-paper1`,
   `core-maths-paper2b` and `binomial-blaster` extract byte-identically even with every external host
   blocked. **23 pairs** were missing for this reason.
2. **SymPy's `parse_expr` goes through Python's tokenizer, which changed in Python 3.12.** The same
   scanner code and SymPy 1.14.0 give different values by Python version:

   | Option text | Python 3.11.9 | Python 3.12.3 / 3.14.6 |
   |---|---|---|
   | `£0.33`, `−£0.33`, `£6,480.00` | unparsed | **0** (so every pair of money options was "equal") |
   | `1 + 0x + 0x^2` | 1 | unparsed (`0x` reads as a broken hex literal) |

   SymPy's version is not a factor: 1.12, 1.13.3 and 1.14.0 behave identically on Python 3.12. CI runs
   Python 3.12 (`check-site.yml`), so a B11 built on the old scanner would have reported 33 false money
   pairs in `core-maths-paper1` and `core-maths-paper2b`, and lost a genuine pair in `binomial-blaster`.

### The fix (`scripts/scan-value-equivalent-options.py`; B1–B10 untouched, as they do not use this parser)

- **Implicit multiplication after a number is written in explicitly** (`0x` → `0*x`, `2(x+1)` →
  `2*(x+1)`), with scientific notation left alone, instead of being left to the tokenizer.
- **Text holding a character Python cannot read as a name, operator or digit (such as `£`) is
  unparsed**, on every Python, before it reaches the tokenizer. That is what Python 3.11 did, and what
  this report recorded.
- **The scan refuses to report** (exit 2, naming the games) when a non-generator bank was not read live,
  so an environment that cannot reach KaTeX can no longer produce a quietly partial list.
  `given-that`'s deliberate static fallback is accepted.
- **The environment is recorded** in the JSON output (`env`: Python and SymPy versions). Packages are pinned
  in `scripts/scan-requirements.txt` (SymPy 1.14.0, mpmath 1.3.0, esprima 4.0.1, the versions CI installs).
- **Six new self-test fixtures** cover both faults (`£0.33` ≠ `£0.67`, `−£0.33` ≠ `£0.33`,
  `1 + 0x + 0x^2` = `1`, …): 38 fixtures, all pass on Python 3.11 and 3.14.

**Proof of determinism.** On the same freshly extracted banks (`main` at `1d8220f`), the full scan gives
an **identical pair list, 252 pairs**, on Python 3.11.9 (Windows), Python 3.12.3 with CI's pinned
packages (Ubuntu 24.04 under WSL, as CI) and Python 3.14.6 (Windows). Options 11,746; parsed 7,755;
unparsed 3,991.

**It reconciles with this report pair by pair.** Every pair the report lists is still found except
`coordinate-geometry-dash:233`, fixed in PR 8. The other 23 are the three KaTeX games. The report's 103
group C pairs were counted per game, not listed; the per-game counts match.

### Every pair, by game and group

| Game | A | B | C | D | E | Total |
|---|---|---|---|---|---|---|
| `binomial-blaster` | 5 |  |  |  |  | 5 |
| `circle-theorem-spotter` | 1 |  |  |  |  | 1 |
| `complex-converter` |  |  |  | 2 | 6 | 8 |
| `coordinate-geometry-dash` |  |  |  | 1 |  | 1 |
| `core-maths-paper1` |  |  |  |  | 3 | 3 |
| `curling-friction` | 1 |  |  |  |  | 1 |
| `decimal-detective` |  |  | 1 | 1 |  | 2 |
| `differentiation-duel` | 6 |  |  | 4 |  | 10 |
| `force-resolver` | 2 |  |  |  |  | 2 |
| `formula-unlocked` |  |  |  | 1 |  | 1 |
| `given-that` |  |  |  | 2 |  | 2 |
| `index-laws` | 1 | 1 |  | 5 | 1 | 8 |
| `integration-duel` |  |  |  | 5 |  | 5 |
| `moments-master` |  |  |  |  | 1 | 1 |
| `probability-paradox` | 2 |  |  | 1 |  | 3 |
| `probability-pioneer` | 8 |  |  | 4 |  | 12 |
| `proof-builder` |  |  | 2 |  |  | 2 |
| `proportion-blaster` | 2 |  |  | 5 |  | 7 |
| `scale-factor-scaling` |  |  |  | 2 |  | 2 |
| `sequence-solver` | 5 |  | 1 | 1 |  | 7 |
| `simultaneous-solver` | 4 |  |  | 2 |  | 6 |
| `standard-form-blitz` |  | 30 | 47 | 1 |  | 78 |
| `surd-simplifier` |  | 23 | 52 | 8 |  | 83 |
| `trig-identity-duel` | 2 |  |  |  |  | 2 |
| **Total** | **39** | **54** | **103** | **45** | **11** | **252** |

The 229 pairs already in this report keep the groups it gave them. The 23 new ones were classified by
the same definitions:

- **A (7):** `differentiation-duel` level4 [35], [39], [42], [46], [50], [51]: each offers the marked
  derivative again, unsimplified or rearranged (`-\dfrac{6x}{4y}` beside `-\dfrac{3x}{2y}`), in a game
  that is not about form and a question that asks for none. `index-laws` [42]: `\dfrac{27}{3}` beside the
  key `9` for `27^{\frac{2}{3}}`.
- **B (1): Jon to rule.** `index-laws` [22], `(5^2)^3`: the key `5^6` and the distractor `25^3` are equal.
  Index Laws is about the form the laws produce, so this is a teaching call, like the 53 above it.
- **D (14):** two wrong options equal in value. `differentiation-duel` level4 [2], [4], [38], [49];
  `index-laws` [6], [27], [38], [39], [40]; `integration-duel` alevel [20], level4 [1], [8], [18], [41]
  (for example `2e^{2x}` and `\frac{4e^{2x}}{2}`, both missing `+ c`).
- **E (1), a scanner false positive:** `index-laws` [21], `x^{4\frac{1}{2}}`. The distractor is the
  mixed number 4½ as an index; the scanner read `4\frac{1}{2}` as 4 × ½ = 2, equal to the key `x^2`.
  The existing E pairs keep their named faults: the en-dash class interval read as a subtraction
  (`20–40` = −20 = `40–60`, `core-maths-paper1`), `\text{}` units that carry meaning, and e^{jθ} phasors
  (`complex-converter`, `moments-master`).

**Group A is 39 questions in 12 games**, not 32 in 10.

### Group A in full: every question where the marked answer is offered twice

For each: the question as the live bank holds it, every option a student sees, the marked answer, and
the option equal to it. Enough to draft a replacement distractor without opening the repo.

#### A1. `binomial-blaster` `QUESTIONS.alevel[10]`

- **Question:** q: `(1+x)^3`; ask: `Expand fully`; correct: `1 + 3x + 3x^2 + x^3`
- **Options shown:** `1 + 3x + 3x^2 + x^3` · `1 + 3x + x^3` · `1 + x + x^2 + x^3` · `1 + 3x^2 + 3x + x^3`
- **Marked answer:** `1 + 3x + 3x^2 + x^3`
- **Equal in value to it:** `1 + 3x^2 + 3x + x^3`

#### A2. `binomial-blaster` `QUESTIONS.alevel2[26]`

- **Question:** q: `\dfrac{1}{1.03} \approx (1+0.03)^{-1}`; ask: `Estimate using first 3 terms`; correct: `0.97090`
- **Options shown:** `0.97090` · `0.971` · `0.97` · `0.9709`
- **Marked answer:** `0.97090`
- **Equal in value to it:** `0.9709`

#### A3. `binomial-blaster` `QUESTIONS.alevel2[27]`

- **Question:** q: `\dfrac{1}{0.98} \approx (1-0.02)^{-1}`; ask: `Estimate using first 3 terms`; correct: `1.02040`
- **Options shown:** `1.02040` · `1.02` · `1.0204` · `1.021`
- **Marked answer:** `1.02040`
- **Equal in value to it:** `1.0204`

#### A4. `binomial-blaster` `QUESTIONS.alevel2[29]`

- **Question:** q: `(0.97)^{-2} \approx (1-0.03)^{-2}`; ask: `Estimate using first 3 terms`; correct: `1.06270`
- **Options shown:** `1.06270` · `1.063` · `1.06` · `1.0627`
- **Marked answer:** `1.06270`
- **Equal in value to it:** `1.0627`

#### A5. `binomial-blaster` `QUESTIONS.alevel2[49]`

- **Question:** q: `(1+x)^0`; ask: `Expansion`; correct: `1`
- **Options shown:** `1` · `1 + x` · `0` · `1 + 0x + 0x^2`
- **Marked answer:** `1`
- **Equal in value to it:** `1 + 0x + 0x^2`

#### A6. `circle-theorem-spotter` `QUESTIONS.gcse[53]`

- **Question:** fig: `{"t": "semicircle", "C": 65, "cLab": "90&deg;", "names": ["A", "C", "B"]}`; ctx: `In a circle, angle ABC = 90°. BC = 6, AC = 10.`; ask: `Find AB`; correct: `8`
- **Options shown:** `8` · `4` · `\sqrt{64}` · `\sqrt{136}`
- **Marked answer:** `8`
- **Equal in value to it:** `\sqrt{64}`

#### A7. `curling-friction` `QUESTIONS.alevel[47]`

- **Question:** ctx: `Stone A (20 kg) launched at 5 m/s. μ = 0.04, g = 10. Target stone B (20 kg) is 20 m away.`; ask: `Speed of A when it reaches B`; correct: `3 \text{ m/s}`; cat: `suvat`
- **Options shown:** `3 \text{ m/s}` · `4 \text{ m/s}` · `1 \text{ m/s}` · `\sqrt{9} \text{ m/s}`
- **Marked answer:** `3 \text{ m/s}`
- **Equal in value to it:** `\sqrt{9} \text{ m/s}`

#### A8. `differentiation-duel` `QUESTIONS.level4[35]`

- **Question:** rule: `Quotient Rule`; q: `\dfrac{x^3}{2x + 1}`; correct: `\dfrac{3x^2(2x+1) - 2x^3}{(2x+1)^2}`; difficulty: `3`; exp: `(3x²(2x+1) - x³·2) / (2x+1)²`
- **Options shown:** `\dfrac{3x^2(2x+1) - 2x^3}{(2x+1)^2}` · `\dfrac{3x^2}{2x+1}` · `\dfrac{6x^3 + 3x^2 - 2x^3}{(2x+1)^2}` · `\dfrac{2x^3 - 3x^2(2x+1)}{(2x+1)^2}`
- **Marked answer:** `\dfrac{3x^2(2x+1) - 2x^3}{(2x+1)^2}`
- **Equal in value to it:** `\dfrac{6x^3 + 3x^2 - 2x^3}{(2x+1)^2}`

#### A9. `differentiation-duel` `QUESTIONS.level4[39]`

- **Question:** rule: `Implicit`; q: `3x^2 + 2y^2 = 14`; prompt: `Find \dfrac{dy}{dx}`; correct: `-\dfrac{3x}{2y}`; difficulty: `2`; exp: `6x + 4y(dy/dx) = 0 → dy/dx = -3x/(2y)`
- **Options shown:** `-\dfrac{3x}{2y}` · `\dfrac{3x}{2y}` · `-\dfrac{6x}{4y}` · `-\dfrac{2y}{3x}`
- **Marked answer:** `-\dfrac{3x}{2y}`
- **Equal in value to it:** `-\dfrac{6x}{4y}`

#### A10. `differentiation-duel` `QUESTIONS.level4[42]`

- **Question:** rule: `Implicit`; q: `x^3 + y^3 = 9`; prompt: `Find \dfrac{dy}{dx}`; correct: `-\dfrac{x^2}{y^2}`; difficulty: `2`; exp: `3x² + 3y²(dy/dx) = 0 → dy/dx = -x²/y²`
- **Options shown:** `-\dfrac{x^2}{y^2}` · `\dfrac{x^2}{y^2}` · `-\dfrac{3x^2}{3y^2}` · `-\dfrac{y^2}{x^2}`
- **Marked answer:** `-\dfrac{x^2}{y^2}`
- **Equal in value to it:** `-\dfrac{3x^2}{3y^2}`

#### A11. `differentiation-duel` `QUESTIONS.level4[46]`

- **Question:** rule: `Parametric`; q: `x = t^2, \quad y = t^3`; prompt: `Find \dfrac{dy}{dx}`; correct: `\dfrac{3t}{2}`; difficulty: `2`; exp: `dy/dt = 3t², dx/dt = 2t → (3t²)/(2t) = 3t/2`
- **Options shown:** `\dfrac{3t}{2}` · `\dfrac{2t}{3}` · `\dfrac{3t^2}{2t}` · `6t`
- **Marked answer:** `\dfrac{3t}{2}`
- **Equal in value to it:** `\dfrac{3t^2}{2t}`

#### A12. `differentiation-duel` `QUESTIONS.level4[50]`

- **Question:** rule: `Parametric`; q: `x = 3t^2, \quad y = 2t^3 - t`; prompt: `Find \dfrac{dy}{dx}`; correct: `\dfrac{6t^2 - 1}{6t}`; difficulty: `3`; exp: `dy/dt = 6t²-1, dx/dt = 6t → (6t²-1)/(6t)`
- **Options shown:** `\dfrac{6t^2 - 1}{6t}` · `\dfrac{6t^2 - 1}{3t^2}` · `t - \dfrac{1}{6t}` · `\dfrac{6t^2}{6t}`
- **Marked answer:** `\dfrac{6t^2 - 1}{6t}`
- **Equal in value to it:** `t - \dfrac{1}{6t}`

#### A13. `differentiation-duel` `QUESTIONS.level4[51]`

- **Question:** rule: `Parametric`; q: `x = t + \dfrac{1}{t}, \quad y = t - \dfrac{1}{t}`; prompt: `Find \dfrac{dy}{dx}`; correct: `\dfrac{t^2 + 1}{t^2 - 1}`; difficulty: `3`; exp: `dy/dt = 1+t⁻², dx/dt = 1-t⁻² → (t²+1)/(t²-1)`
- **Options shown:** `\dfrac{t^2 + 1}{t^2 - 1}` · `\dfrac{t^2 - 1}{t^2 + 1}` · `1` · `\dfrac{1 + t^{-2}}{1 - t^{-2}}`
- **Marked answer:** `\dfrac{t^2 + 1}{t^2 - 1}`
- **Equal in value to it:** `\dfrac{1 + t^{-2}}{1 - t^{-2}}`

#### A14. `force-resolver` `QUESTIONS.alevel[7]`

- **Question:** ctx: `A force has horizontal component 8 N and vertical component 6 N.`; q: `R = \sqrt{F_x^2 + F_y^2}`; ask: `Find the magnitude of the force`; correct: `10 \text{ N}`
- **Options shown:** `10 \text{ N}` · `14 \text{ N}` · `7 \text{ N}` · `\sqrt{100} \text{ N}`
- **Marked answer:** `10 \text{ N}`
- **Equal in value to it:** `\sqrt{100} \text{ N}`

#### A15. `force-resolver` `QUESTIONS.alevel[9]`

- **Question:** ctx: `Components: Fx = 5 N, Fy = 12 N.`; ask: `Resultant magnitude`; correct: `13 \text{ N}`
- **Options shown:** `13 \text{ N}` · `17 \text{ N}` · `7 \text{ N}` · `\sqrt{169} \text{ N}`
- **Marked answer:** `13 \text{ N}`
- **Equal in value to it:** `\sqrt{169} \text{ N}`

#### A16. `index-laws` `QUESTIONS[42]`

- **Question:** rule: `Fractional Power`; q: `27^{\frac{2}{3}}`; correct: `9`; exp: `Cube root of 27 is 3, then 3²=9`
- **Options shown:** `9` · `18` · `3` · `\dfrac{27}{3}`
- **Marked answer:** `9`
- **Equal in value to it:** `\dfrac{27}{3}`

#### A17. `probability-paradox` `CONDITIONAL_QUESTIONS[10]`

- **Question:** scenario: `A factory has machines X and Y. X produces 60% of items, Y produces 40%. X has a 3% defect rate, Y has 5%.`; q: `An item is defective. P(made by X)?`; correct: `9/19`; steps: `["P(D) = 0.03×0.6 + 0.05×0.4 = 0.018 + 0.02 = 0.038", "P(X|D) = 0.018/0.038 = 18/38 = 9/19 ≈ 0.474"]`; misconception: `Even though X produces most items, its lower defect rate means a defective item is almost equally likely to come from either machine.`
- **Options shown:** `9/19` · `3/20` · `18/38` · `0.60`
- **Marked answer:** `9/19`
- **Equal in value to it:** `18/38`

#### A18. `probability-paradox` `CONDITIONAL_QUESTIONS[12]`

- **Question:** scenario: `A card is drawn from a standard 52-card deck.`; q: `P(King | Face card)?`; correct: `1/3`; steps: `["Face cards: J, Q, K in each suit = 12 cards", "Kings = 4", "P(King | Face) = 4/12 = 1/3"]`
- **Options shown:** `1/3` · `4/52` · `1/13` · `4/12`
- **Marked answer:** `1/3`
- **Equal in value to it:** `4/12`

#### A19. `probability-pioneer` `STAGE2[5]`

- **Question:** q: `P(blue from 4 red, 6 blue)`; answer: `3/5`
- **Options shown:** `3/5` · `2/5` · `6/10` · `4/10`
- **Marked answer:** `3/5`
- **Equal in value to it:** `6/10`

#### A20. `probability-pioneer` `STAGE2[7]`

- **Question:** q: `P(heart from 52 cards)`; answer: `1/4`
- **Options shown:** `1/4` · `13/52` · `1/13` · `4/52`
- **Marked answer:** `1/4`
- **Equal in value to it:** `13/52`

#### A21. `probability-pioneer` `STAGE2[13]`

- **Question:** q: `P(rolling 1 or 2)`; answer: `1/3`
- **Options shown:** `1/3` · `2/6` · `1/6` · `2/3`
- **Marked answer:** `1/3`
- **Equal in value to it:** `2/6`

#### A22. `probability-pioneer` `STAGE2[14]`

- **Question:** q: `P(face card from 52)`; answer: `3/13`
- **Options shown:** `3/13` · `12/52` · `1/4` · `4/52`
- **Marked answer:** `3/13`
- **Equal in value to it:** `12/52`

#### A23. `probability-pioneer` `STAGE2[15]`

- **Question:** q: `P(prime on a die)`; answer: `1/2`
- **Options shown:** `1/2` · `1/3` · `2/3` · `3/6`
- **Marked answer:** `1/2`
- **Equal in value to it:** `3/6`

#### A24. `probability-pioneer` `STAGE2[16]`

- **Question:** q: `P(yellow from 8R, 2Y)`; answer: `1/5`
- **Options shown:** `1/5` · `2/10` · `8/10` · `2/8`
- **Marked answer:** `1/5`
- **Equal in value to it:** `2/10`

#### A25. `probability-pioneer` `STAGE2[17]`

- **Question:** q: `P(square number on a die)`; answer: `1/3`
- **Options shown:** `1/3` · `2/6` · `1/6` · `1/2`
- **Marked answer:** `1/3`
- **Equal in value to it:** `2/6`

#### A26. `probability-pioneer` `STAGE2[18]`

- **Question:** q: `P(even from 1–8)`; answer: `1/2`
- **Options shown:** `1/2` · `4/8` · `3/8` · `5/8`
- **Marked answer:** `1/2`
- **Equal in value to it:** `4/8`

#### A27. `proportion-blaster` `QUESTIONS.gcse[33]`

- **Question:** ctx: `y ∝ 1/x². When x = 1, y = 12.`; q: `y = \dfrac{k}{x^2}`; ask: `Find y when x = 3`; correct: `\dfrac{4}{3}`
- **Options shown:** `\dfrac{4}{3}` · `4` · `36` · `\dfrac{12}{9}`
- **Marked answer:** `\dfrac{4}{3}`
- **Equal in value to it:** `\dfrac{12}{9}`

#### A28. `proportion-blaster` `QUESTIONS.alevel[18]`

- **Question:** ctx: `y is inversely proportional to (x − 1). When x = 3, y = 5.`; q: `y = \dfrac{k}{x-1}`; ask: `Find y when x = 6`; correct: `2`
- **Options shown:** `2` · `\dfrac{10}{5}` · `\dfrac{5}{3}` · `1`
- **Marked answer:** `2`
- **Equal in value to it:** `\dfrac{10}{5}`

#### A29. `sequence-solver` `QUESTIONS.gcse[7]`

- **Question:** seq: `20, 18, 16, 14, ...`; ask: `Find the nth term`; correct: `22 - 2n`
- **Options shown:** `22 - 2n` · `20 - 2n` · `-2n + 22` · `2n + 20`
- **Marked answer:** `22 - 2n`
- **Equal in value to it:** `-2n + 22`

#### A30. `sequence-solver` `QUESTIONS.gcse[8]`

- **Question:** seq: `0, 3, 6, 9, ...`; ask: `Find the nth term`; correct: `3n - 3`
- **Options shown:** `3n - 3` · `3n` · `3(n-1)` · `n + 3`
- **Marked answer:** `3n - 3`
- **Equal in value to it:** `3(n-1)`

#### A31. `sequence-solver` `QUESTIONS.gcse[23]`

- **Question:** seq: `2, 6, 12, 20, 30`; ask: `Find the nth term`; correct: `n^2 + n`
- **Options shown:** `n^2 + n` · `n(n+1)` · `2n^2` · `n^2 + 2n`
- **Marked answer:** `n^2 + n`
- **Equal in value to it:** `n(n+1)`

#### A32. `sequence-solver` `QUESTIONS.gcse[24]`

- **Question:** seq: `3, 8, 15, 24, 35`; ask: `Find the nth term`; correct: `n^2 + 2n`
- **Options shown:** `n^2 + 2n` · `n^2 + n + 1` · `n(n+2)` · `2n^2 + 1`
- **Marked answer:** `n^2 + 2n`
- **Equal in value to it:** `n(n+2)`

#### A33. `sequence-solver` `QUESTIONS.alevel[4]`

- **Question:** q: `S_{10} = 200, a = 2`; ask: `Find d`; correct: `4`
- **Options shown:** `4` · `3` · `5` · `\dfrac{36}{9}`
- **Marked answer:** `4`
- **Equal in value to it:** `\dfrac{36}{9}`

#### A34. `simultaneous-solver` `QUESTIONS.alevel[0]`

- **Question:** sys: `["2x + 3y = 7", "5x - y = 9"]`; ask: `Find x`; correct: `2`
- **Options shown:** `2` · `1` · `3` · `\tfrac{34}{17}`
- **Marked answer:** `2`
- **Equal in value to it:** `\tfrac{34}{17}`

#### A35. `simultaneous-solver` `QUESTIONS.alevel[35]`

- **Question:** sys: `["x^2 + y^2 = 25", "y = 0"]`; ask: `Find the positive x value`; correct: `5`
- **Options shown:** `5` · `4` · `3` · `\sqrt{25}`
- **Marked answer:** `5`
- **Equal in value to it:** `\sqrt{25}`

#### A36. `simultaneous-solver` `QUESTIONS.alevel[42]`

- **Question:** sys: `["x^2 + y^2 = 50", "y = x"]`; ask: `Find the positive x value`; correct: `5`
- **Options shown:** `5` · `\sqrt{50}` · `25` · `\sqrt{25}`
- **Marked answer:** `5`
- **Equal in value to it:** `\sqrt{25}`

#### A37. `simultaneous-solver` `QUESTIONS.alevel[45]`

- **Question:** sys: `["x^2 + y^2 = 45", "x = 2y"]`; ask: `Find the positive y value`; correct: `3`
- **Options shown:** `3` · `\sqrt{45}` · `9` · `\sqrt{9}`
- **Marked answer:** `3`
- **Equal in value to it:** `\sqrt{9}`

#### A38. `trig-identity-duel` `QUESTIONS.gcse[2]`

- **Question:** q: `\tan 30°`; ask: `Exact value`; correct: `\dfrac{1}{\sqrt{3}}`
- **Options shown:** `\dfrac{1}{\sqrt{3}}` · `\sqrt{3}` · `\dfrac{\sqrt{3}}{3}` · `1`
- **Marked answer:** `\dfrac{1}{\sqrt{3}}`
- **Equal in value to it:** `\dfrac{\sqrt{3}}{3}`

#### A39. `trig-identity-duel` `QUESTIONS.gcse[25]`

- **Question:** ctx: `Triangle: a = 8, b = 6, C = 90°.`; q: `c^2 = a^2 + b^2 - 2ab\cos C`; ask: `Find c`; correct: `10`
- **Options shown:** `10` · `14` · `\sqrt{100}` · `48`
- **Marked answer:** `10`
- **Equal in value to it:** `\sqrt{100}`


## Fixed, 1 Oct 2026: group A applied (Jon's approved replacements and rulings)

Contract: `E:\jon\contracts\2026-10-01-groupA-distractors.md` (Project Claude, approved by Jon 1 Oct).

- **All 39 group A questions now offer a named-misconception distractor in place of the equal form**,
  plus the three group D pairs inside questions already being edited (A18, A19, A20). Each edit was
  located by its whole option literal and had to match exactly once in its file; none was located by
  index. 41 edits in 12 game files.
- **Ruling 1, `index-laws` [22] `(5^2)^3`:** `25^3` stays. The question now carries
  `ask:'Write (5²)³ as a single power of 5'`, shown in the game's existing sub-line under the
  question (`#qSub`, which every other question still fills with "Select the correct simplified
  form"). The game had no per-question ask, so `nextQ()` gained one line to show it. **Reclassified C**:
  the form is now what the question asks for.
- **Ruling 2, `binomial-blaster` alevel2 [26], [27], [29]:** keys now `0.9709`, `1.0204`, `1.0627` (same
  values). The game has no explanation text that quoted them.
- **Explanations:** none referred to a removed option as a choice. `probability-paradox` A17 and A18
  keep `18/38 = 9/19` and `4/12 = 1/3` in their worked steps; that is working, not an option.

**Re-run on freshly extracted banks** (Python 3.14.6, SymPy 1.14.0, Windows): **252 → 210 pairs.** Exactly
the 39 group A pairs and the 3 named D pairs are gone; no pair was added; none of the 39 touched questions
has any value-equal pair left. `check-banks.py --ci` still matches the ledger exactly.

| Group | Before | After |
|---|---|---|
| A | 39 | **0** |
| B | 54 | 53 (`index-laws` [22] moved to C) |
| C | 103 | 104 |
| D | 45 | 42 |
| E | 11 | 11 |
| **Total** | **252** | **210** |

Next: B11 (Contract 1 in `docs/next-contract-value-equivalent-options.md`), so no new case can land.

---

## B11 built, 2 Oct 2026 (PR 51)

`check-banks.py` rule B11, "options equal in value", now runs in CI inside the existing
`check-banks.py --ci` step. It uses this scan's parser, moved into `scripts/bank_common.py` (one copy;
the scan imports it). Moving it changed nothing: the same 210 pairs and stats, and `check-banks.py --ci`
output for B1–B10 is byte-identical to `main`.

**Parser fixes (section E, 11 pairs, now all unequal; no other pair changed):** en-dash class intervals
are intervals (`core-maths-paper1` [11], 3 pairs); j in a phasor's exponent is the imaginary unit
(`complex-converter`, 6); an integer written straight before `\frac{p}{q}` is a mixed number (`index-laws`
[21], 1); and `\text{}` parts are compared as words, the rest by value, so `1 \text{ Nm clockwise}` ≠
`1 \text{ Nm anticlockwise}` (`moments-master` alevel[10], 1) while `\sqrt{50}\text{ cm}` =
`5\sqrt{2}\text{ cm}`. A first version left every `\text{}` option unparsed, which hid 585 options;
with the final rule, 3,991 of 11,746 options are unparsed, the same as before any `\text{}` rule.

**B11 finds 199 pairs on freshly extracted `main`,** pair for pair with the 1 Oct re-run less section E;
none is new.

**Reclassified on reading, Jon's rulings of 2 Oct.** Twelve group C questions turned out not to ask
for the form they test:

| Question | Pairs | The ask, and why it does not name the form | Ruling |
|---|---|---|---|
| `surd-simplifier` `QUESTIONS.gcse[28]` | 1 | "Rationalise": `\dfrac{5\sqrt{5}}{5}` is rationalised, only unsimplified; the game says "Rationalise and simplify" when it wants that | B |
| `surd-simplifier` `QUESTIONS.gcse[31]` | 3 | "Simplify": the key `\dfrac{\sqrt{3}}{3}` beside `\dfrac{1}{\sqrt{3}}`; "Simplify" does not say rationalise | B |
| `surd-simplifier` `QUESTIONS.alevel[12]` | 2 | "Rationalise": `\dfrac{\sqrt{2}-1}{1}` beside the key `\sqrt{2}-1` | B |
| `surd-simplifier` `QUESTIONS.alevel[14]` | 1 | "Rationalise": `\dfrac{2(\sqrt{3}-1)}{2}` is rationalised, only unsimplified | B |
| `surd-simplifier` `QUESTIONS.alevel[16]` | 2 | "Rationalise": the key `4(2-\sqrt{3})` beside `8-4\sqrt{3}`; both rationalised and simplified, factorised against expanded (a possible key flip) | B |
| `surd-simplifier` `QUESTIONS.alevel[17]` | 1 | "Rationalise": `\dfrac{2+\sqrt{2}}{1}` beside the key `2+\sqrt{2}` | B |
| `surd-simplifier` `QUESTIONS.alevel[18]` | 1 | "Rationalise": `\dfrac{5(\sqrt{6}-1)}{5}` is rationalised, only unsimplified | B |
| `surd-simplifier` `QUESTIONS.alevel[42]` | 1 | "Rationalise": `\dfrac{\sqrt{3}-\sqrt{2}}{1}` beside the key `\sqrt{3}-\sqrt{2}` | B |
| `standard-form-blitz` `QUESTIONS.alevel[47]` | 1 | "Estimate to 1 s.f.": `10 \times 10^8` beside the key `1 \times 10^9`; the ask names 1 s.f., not standard form | B |
| `proof-builder` `INDUCTION[0]` stage 4 | 1 | "This simplifies to:": the key `\frac{(k+1)(k+2)}{2}` beside `\frac{k^2+3k+2}{2}`; both simplified, the factorised target not named | B |
| `proof-builder` `INDUCTION[3]` stage 2 | 1 | "Factor:": factoring (k+1)! out gives the distractor `(k+1)! \cdot (k+2) - 1`; the key `(k+2)! - 1` needs a further step the prompt does not ask for | B |
| `sequence-solver` `QUESTIONS.alevel[23]` | 1 | "Which formula when \|r\| < 1?": the two S_n forms are identical for every r ≠ 1, so a correct formula is marked wrong | **A** (live bug, to-do §1.29) |

**Final split: A 1 / B 68 / C 88 / D 42 = 199.**

| Group | Pairs | Where it lives |
|---|---|---|
| A | 1 | `data/check-ledger.json` (tracked; to-do §1.29) |
| B | 68 (53 + 15 on the 11 questions above) | the ledger; their wording is Contract 2, which needs a redraft |
| C | 88 | `scripts/checker-allowlist.json`, `b11_form_questions`: one entry per pair, each with a reason quoting the ask |
| D | 42 | the ledger |

The ledger holds 111 B11 entries (A + B + D). CI fails on any new pair, on a ledgered pair that no
longer reproduces, and on an allowlist entry that matches nothing.

## Contract 2 applied, 2 Oct 2026 (PR 54)

Contract 2, as redrafted by Project Claude on 2 Oct (afternoon), with Jon's rulings of the same day.
Every edit was located by its whole question literal, never by index. **100 asks rewritten in two
games, plus one distractor.**

**Changed asks, before and after** (questions are bank positions on 2 Oct, for a reader; the edits
were made by literal):

**standard-form-blitz: 54 asks**

| Before | After | n | Questions |
|---|---|---|---|
| Calculate | Calculate. Give your answer in standard form. | 49 | gcse[18], gcse[19], gcse[20], gcse[21], gcse[22], gcse[23], gcse[24], gcse[25], gcse[26], gcse[27], gcse[28], gcse[29], gcse[30], gcse[31], gcse[32], gcse[33], gcse[34], gcse[35], gcse[36], gcse[37], alevel[0], alevel[1], alevel[2], alevel[3], alevel[5], alevel[6], alevel[7], alevel[8], alevel[10], alevel[11], alevel[12], alevel[13], alevel[14], alevel[15], alevel[16], alevel[17], alevel[18], alevel[19], alevel[20], alevel[21], alevel[22], alevel[23], alevel[24], alevel[32], alevel[34], alevel[35], alevel[36], alevel[38], alevel[39] |
| Calculate (3 s.f.) | Calculate. Give your answer in standard form to 3 s.f. | 4 | alevel[4], alevel[9], alevel[26], alevel[37] |
| Estimate to 1 s.f. | Estimate to 1 s.f., in standard form. | 1 | alevel[47] |

**surd-simplifier: 46 asks**

| Before | After | n | Questions |
|---|---|---|---|
| Rationalise | Rationalise and simplify | 18 | gcse[20], gcse[21], gcse[22], gcse[23], gcse[24], gcse[28], gcse[29], gcse[30], alevel[10], alevel[11], alevel[12], alevel[13], alevel[14], alevel[15], alevel[17], alevel[18], alevel[19], alevel[42] |
| Simplify | Simplify, rationalising the denominator | 1 | gcse[31] |
| Convert to a fraction | Convert to a fraction in its simplest form | 23 | gcse[35], gcse[36], gcse[37], gcse[38], gcse[39], gcse[40], gcse[41], gcse[42], gcse[43], gcse[44], gcse[45], gcse[46], gcse[47], gcse[49], alevel[30], alevel[31], alevel[32], alevel[33], alevel[34], alevel[35], alevel[37], alevel[38], alevel[39] |
| Convert to a fraction | Write in its simplest form | 2 | gcse[48], alevel[36] |
| Rationalise | Rationalise, giving your answer in the form a + b√3 | 1 | alevel[16] |
| Expand | Expand and simplify | 1 | alevel[45] |

standard-form-blitz alevel[43] (key 1), alevel[44] (key 10^9) and alevel[46] (key 3.16) keep their asks:
their keys are not in standard form. Three surd-simplifier literals are byte-identical copies in the
gcse and alevel banks (0.3̇, 0.1̇42857̇, 0.9̇); each **matched x2 by design (cross-level copy)**, one copy in
each array, asserted. Cross-level reuse itself is a separate item for Jon.

**Two content fixes:**

- **`surd-simplifier` alevel[16]** (4/(2+√3)), Jon's ruling: ask "Rationalise, giving your answer in the
  form a + b√3"; the key is now `8-4\sqrt{3}`, and the old key `4(2-\sqrt{3})` is a form distractor. Rendered
  and marked: 8 − 4√3 correct, 4(2 − √3) wrong.
- **`sequence-solver` alevel[23]** (to-do §1.29, group A): the distractor `S_n = \dfrac{a(r^n-1)}{r-1}`,
  identical in value to the key for every r ≠ 1, is now `S_n = \dfrac{a(1-r^{n-1})}{1-r}` (carrying the n − 1
  from the nth term ar^{n−1} into the sum).

**The two 0.9̇ questions** (gcse[48], alevel[36]; key 1) ask "Write in its simplest form", by Jon's ruling:
"Convert to a fraction" would leave 9/9 as the only option that looks like a fraction and equals the
value, and "or a whole number" would give the answer away.

**Split out: proof-builder (the contract's step 3).** Its induction stage prompts render through
`rkStr()`, KaTeX maths mode, so prose loses its spaces (to-do §1.30); new wording there would render as
`Writethisintheformtheformulagivesforn=k+1:`. Its 2 group B pairs stay in the ledger until that is fixed.

**Bookkeeping.** 80 B11 ids changed, all on edited questions, one to one:

| Group | Pairs | Now |
|---|---|---|
| B | 66 (standard-form-blitz 31, surd-simplifier 35) | `b11_form_questions`, each reason quoting the new ask |
| C | 5 (surd-simplifier gcse[20], [21], [22], alevel[10], [11]) | re-keyed in place, reasons re-quoted ("Rationalise and simplify") |
| D | 9 (standard-form-blitz alevel[35]; surd-simplifier gcse[38], [42], [43], [44], [49], alevel[31], [32], [39]) | re-keyed in the ledger by `--write-ledger` |

The sequence-solver A pair is gone. Identical cross-level copies keep their ordinals (#1 in gcse, #2 in
alevel, before and after). The old id → new id table is in the PR description. B1–B10 re-keys: 0.

**Final B11 counts:** 198 pairs platform-wide (199 less the A pair; none new) = 154 allowlisted + 44 ledgered.
**Group A 0; group B 2** (proof-builder, waiting on §1.30); **allowlisted 154** (88 C + 66 former B);
**group D 42**, ledgered. The ledger holds 44 B11 entries.

**Checks:** tier 1 PASS on all three games and tier 3 identical to `main` (standard-form-blitz and
surd-simplifier 3/3, sequence-solver 5/5). At 320×568 and 375×667, every question in both games was
rendered through its own `showQ()`, before and after: no question that had its options above the fold
lost them (the longest new ask adds at most 20px). Each of the 100 changed questions was rendered and
answered with its key: all marked correct, with the new ask on screen.
