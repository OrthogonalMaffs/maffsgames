# Answer-key audit, tranche 1: 12 games without a verifier (6 Oct 2026)

**Status: report only, as delivered to Jon on 6 Oct 2026.** Read-only audit of main at `3e46400`; no game was
changed by it. Method: `docs/audit-resit-correctness-2026-10-04.md`'s Method section (banks read from the live page on
a scratch copy, every key recomputed exactly, marking code read and reproduced in Chromium). Severity as that audit
defines it. Follow-up: PR #82 unlisted `trig-worms` and `spot-the-error` (relist checklists, todo §1.53 and §1.54);
Jon's rulings of 6 Oct 19:15 are the last section. Fixes are marked against each item as they merge.

---

# Answer-key audit of 12 games that have no verifier — 6 Oct 2026, main at `3e46400`

I changed nothing in the repo: `git status` is clean, and every bank was extracted on a scratch copy. None of the 12 games is on `/resit/`. No STOP IF fired. Bearing Blitz and Trig Worms are generators, not banks, so I ran their own code over every outcome instead.

I went back to the source for every CRITICAL and HIGH below: I read the line and redid the arithmetic. The MEDIUM and LOW faults are the audit agents' evidence; I spot-checked them but did not re-derive each one.

## 1. Summary

The level shown is the one the portal card opens; "ignored" means the game never reads `?level=`.

| Game | Card level → what is served | Items checked | C | H | M | L | Worst fault |
|---|---|---|---|---|---|---|---|
| `trig-worms` | gcse (ignored); one generator | 1,575 outcomes, all of them | **1** | 0 | 3 | 4 | In 333 of 675 angle questions, a wrong option is θ worked out correctly from two sides labelled on the diagram |
| `spot-the-error` | ks3 (ignored; Start stays disabled until a level is picked); ks3 **35**, gcse 45, level4 **30** | 110 | 0* | 10 | 4 | 7 | gcse_044 keys a correct arc-length formula as the error; ks3_019's own explanation gives 120 g of butter (the answer is 150 g) |
| `word-problem-decoder` | ks3 50, gcse 60 (anything else serves gcse) | 110 (114 phrases) | 0 | 5 | 6 | 5 | The same reverse-percentage phrase is "Percentages" at KS3 and wrong at GCSE; a second Enter credits the next phrase unseen |
| `probability-paradox` | bare and core (ignored); **38** across 3 modes | 38 | 0 | 4 | 4 | 6 | Envelope problem keyed £20, but the answer depends on a prior the question never gives |
| `surd-simplifier` | gcse 50, alevel 50 | 100 | 0 | 2 | 0 | 5 | :233 is keyed 137/330, but 0.41616… = 206/495, and no option is right |
| `coordinate-geometry-dash` | gcse **24**, alevel **21** (only `alevel` switches the bank) | 45 | 0 | 1 | 3 | 3 | :287 is keyed "All equivalent", so each correct equation is marked wrong; the circles are drawn as ellipses |
| `scale-factor-scaling` | gcse **38**, alevel 46, level4 **31** (anything else serves level4) | 46 | 0 | 1 | 0 | 3 | :165 paint question cannot be answered, and its key contradicts the stem |
| `prime-or-composite` | ks3 (ignored); 66 | 66 | 0 | 1 | 1 | 2 | Pressing P or C during feedback answers the next question before it is shown |
| `fraction-equivalence` | ks3 (generator; gcse is identical), year6 **20** | 20 + 940 generated | 0 | 0 | 1 | 2 | All keys right; the Year 6 bank has only 20 items |
| `index-laws` | gcse (ignored); 45 | 45 | 0 | 0 | 0 | 7 | All keys right; five distractor pairs equal in value |
| `standard-form-blitz` | gcse 50, alevel 50 | 100 | 0 | 0 | 0 | 4 | All keys right |
| `bearing-blitz` | gcse (ignored); generator | all 360 bearings | 0 | 0 | 0 | 4 | All right: ±5° with wrap-around, and back bearings miss |
| **Total** | | | **1** | **24** | **22** | **52** | |

\* Spot the Error at GCSE sits on the CRITICAL line. 5 of its 45 items (11.1%) mark a correct pick wrong or a wrong one right, and 4 of 45 (8.9%) if gcse_006's rounding slip is left out. I have rated it HIGH; whether the level crosses into CRITICAL is your call.

The figures in bold are banks under the 40 minimum. Six of the HIGHs are judgement calls, marked JC below.

## 2. CRITICAL and HIGH faults

### Trig Worms: CRITICAL
- **Lines 212–228.** Every angle question labels all three sides on the diagram (H=, O= and A=, lines 383–392). The distractors are built from the other valid ratios on the same triangle:
  - SOH questions are offered `atan(O/A)`.
  - TOA questions are offered `asin(O/H)`.
- **Example** (hypotenuse 8, angle 15°): the question says O = 2.1, H = 8. Options are 25°, **15°** (the key), 15.3° and 74.8°.
  - 15.3° is tan⁻¹(2.1/7.7), with 7.7 taken from the diagram, so it is a correct answer.
  - sin⁻¹(2.1/8) = 15.22°, so 15.3° is nearer the true angle than the key.
  - The agent clicked 15.3° in Chromium and got "MISSED!".
- **How often** (my own Python enumeration agreed with the agent's run of the game's code):
  - 333 of 675 angle outcomes (49%) offer a correctly worked θ as a wrong option.
  - 170 of 675 (25.2%) have a wrong option closer to the true value than the key.
  - Angle questions are 4 in every 10, so this is about 20% of all questions.
- **Root cause:** keys are whole degrees, the givens are rounded to 1 d.p., and no precision is stated (SR-1). The fix is at the generator, not per item.

### Spot the Error
- **ks3_019 (:235)**
  - 600 g of oats is 4 parts, so the butter is 600 ÷ 4 = **150 g**. The explanation teaches (1/5) × 600 = 120 g.
  - Step 3, "(4/5) × 600", makes the same error and is marked correct.
- **ks3_024 (:240):** the keyed error step is right, but the Stage 2 key is wrong.
  - The angle actually lost is s + 30 = 67.5°. The game's own explanation says so.
  - Yet the phrase "30° more than s" is marked `isError:false`, so a student who taps the real misreading is marked wrong.
- **ks3_016 (:229), JC:** there is no error in the working.
  - 72 is a valid common denominator.
  - 168/72 + 126/72 + 228/72 = 522/72 = 29/4, which is the true total (7/3 + 7/4 + 19/6 = 29/4).
- **gcse_044 (:301):** the only step, (72/180) × π × 10, is keyed as the error. But θ/180 × πr is identical to θ/360 × 2πr, so the student must click a correct step to be marked right.
- **gcse_020 (:274):** the keyed step, "g(2) = 4", is a true statement.
  - Step 2, "gf(2) = f(4) = 11", is false: gf(2) = g(7) = 49.
  - It is marked correct, so a student who picks the false line is marked wrong.
- **gcse_001 (:255) and gcse_027 (:284), JC:** the same reverse-percentage mistake, keyed at opposite steps.
  - gcse_001 keys the addition, 76.50 + 7.65. gcse_027 keys the "17% of current" step instead.
  - The correct originals are 76.50 ÷ 0.9 = 85 and 292,500 ÷ 1.17 = 250,000.
  - Each item has a second valid step.
- **gcse_006 (:260):** step 3 is marked correct, but 80 × tan 34° = 53.96, not 53.97. The explanation's 80 ÷ tan 34° = 118.6, not 118.5. Low practical risk.
- **l4_002 (:307):** step 2, "log 12 − log 2 = log 10", is marked correct, but it equals log 6. That makes it a second erroneous step.
- **l4_023 (:331), JC:** choosing u = cos x is unhelpful but legitimate, and step 3 is a true identity. So no step contains false maths.

### Surd Simplifier
- **:174.** Question 8/√32, ask "Rationalise and simplify".
  - The key, "√2 · √2", equals 2. The answer is √2.
  - The only option equal to √2 is 8√32/32, and it is marked wrong (the agent reproduced this in Chromium).
  - Line :175, the same stem, is keyed √2.
- **:233.** Question 0.4161616…: 4/10 + 16/990 = 412/990 = **206/495**.
  - The key, 137/330, is 0.41515….
  - None of the four options is correct.

### Coordinate Geometry Dash
- **:287 (A-Level).** Question: x = 3t, y = 4/t; Cartesian equation?
  - xy = 12, y = 12/x and x = 12/y are all correct, and each is marked wrong. Only "All equivalent" is accepted.
  - The game's own working says "xy = 12, or equivalently y = 12/x".

### Scale Factor Scaling
- **:165 (A-Level and Level 4).** "Paint covers 10 m² per litre. If dimensions double, how many litres?"
  - No original area or amount of paint is given, so the question cannot be answered.
  - The key, "4 litres per 10 m²", contradicts the stem's own rate.

### Probability Paradox
- **Envelope problem (:194–200).**
  - Given £20, E(switch) = 40·P(£40 | £20) + 10·P(£10 | £20). That needs a prior, which the scenario does not give, and the game's own text (:200) says so.
  - "Cannot determine" is marked wrong.
  - Under the game's own simulation prior (:449), E(switch) = £24.91.
- **Inspection paradox (:210–216).**
  - "Every 10 minutes on average" does not say the arrivals are random (Poisson).
  - E(wait) = E[G²]/2E[G], where G is the gap between buses, so "Depends on the schedule" is literally correct. It is marked wrong.
- **Sleeping Beauty (:226), JC:** keyed 1/3, while the game's own text calls the question "genuinely debated".
- **Fallacy, "95% after 60%" (:354), JC:** "The test was easier" is also an alternative explanation that should be considered.
- These faults fall in the 12-item Paradox mode: 2 of 12 are arithmetic faults (16.7%), and 3 of 12 counting Sleeping Beauty. If a mode counts as a level, that is over the CRITICAL line.

### Word Problem Decoder
- **H1, ks3_006 (:262):** "£2.50 per 100g" is keyed Number & Place Value. Ratio & Proportion, a unit rate, is always on screen and is defensible.
- **H2, gcse_017 (:347):** the problem has two unknowns and two conditions, keyed Equations. gcse_021 (:353), which has the same shape, is keyed Simultaneous Equations, and that option is shown 58% of the time.
- **H3 and H4, JC:**
  - gcse_001–005 key "10% off" as Reverse Percentage, but ks3_013 (:271) keys the same shape as Percentages. Percentages is offered about 50% of the time.
  - gcse_006–009 key Standard Form, but ks3_023 (:285) keys the phrase "standard form" itself as Number & Place Value.
- **H5:** answered buttons are disabled only by CSS (`pointer-events:none`, :115), so a second Enter credits the next phrase unseen. Reproduced: 2/2 phrases credited with only one shown.

### Prime or Composite
- **:529–533.** The keyboard handler checks only `gameActive`, and `qIdx++` runs before the feedback pause.
  - Pressing P or C during feedback answers the next question unseen. Reproduced: question 2 (7) was marked wrong without ever being shown.
  - A key press after the last question throws an error.

## 3. MEDIUM and LOW, briefly

- **Trig Worms**
  - M (arguably HIGH): "Find the adjacent side" sets `findSide='opposite'` (:247). The diagram shows "O=?" and prints **A=<the answer>**. This affects 450 of 1,575 outcomes.
  - M: in 48 of 675 angle outcomes, the stated method rounds to a different whole degree from the key.
  - M: the explanation "= 15°" is false at 1 d.p. in 517 of 675.
  - L: distractors of 90° or more; the drawn triangle is distorted by up to 6.8°.
- **Coordinate Geometry Dash**
  - M: `drawCircle` scales the radius by x only, so every circle is 1.25–1.5 times too tall. At :273 the point "on" the circle is drawn inside it.
  - M: the point at :210 is drawn off the canvas.
  - M: at :224 the perpendicular lines are drawn meeting at 72°.
- **Spot the Error**
  - M: gcse_028 rounds money without saying so (c = 69/19).
  - M: gcse_031's explanation is false.
  - M: ks3_025 uses "of 400", a number not in the question.
  - L: 34 of 110 items have one step, so Stage 1 cannot be failed on them.
- **Word Problem Decoder**
  - M: gcse_017 has no whole-number answer (c = 71/19), and neither does gcse_021.
  - M: the tins in gcse_059 are 72000 ÷ (π·25·15) = 61.1 by volume, not 48. And 48 is exactly how many physically fit, so it is not "too high".
  - M: gcse_022's lap count is ambiguous.
  - L: questions refer to diagrams that do not exist; there are two Aa buttons.
- **Probability Paradox**
  - M: the simulations contradict the keys: Sleeping Beauty's bars show 50/50, and the bus simulation shows a 5-minute mean wait.
  - M (JC): Two-Child and Tuesday hold only under the "asked" reading.
  - M: the p-value given is one-sided (0.29); the usual two-sided value is 0.58.
- **Prime or Composite**
  - M (JC): every hint gives the answer away. A rule that reads only the hint classifies all 66 items correctly.
- **Fraction Snap:** M: Year 6 bank is 20; L: "max streak" prints the current streak.
- **Surd Simplifier:** the :246 √(a²)/a pair is not in the allowlist; the menu promises "nested surds" and the bank has none.
- **Standard Form Blitz:** two blank prompts (:212, :213).
- **Index Laws:** five distractor pairs equal in value (already in the ledger).
- **Scale Factor Scaling:** an unknown level shows "undefined" on the results screen.
- **Bearing Blitz:** a miss repeats the same bearing straight after its answer line was drawn.

## 4. Bug classes seen in two or more games

1. **Second valid answers that B11 cannot see.** Five games: Trig Worms (a distractor worked by a valid route), Coordinate Geometry Dash (:287), Spot the Error (a second false step in 4 items), Probability Paradox (keys that depend on an unstated assumption), and Word Problem Decoder (topic categories that overlap).
   - None of these is a string-equal or value-equal pair, so B2, B11 and `MaffsOptions.build()` all pass them.
   - The only thing that catches this class is a per-game verifier that recomputes from the question data. That is the resit audit's class 1 again.
2. **Wrong keys written by hand into the bank.** Surd Simplifier ×2, Spot the Error, Scale Factor Scaling and Probability Paradox. Same class as above: there is no verifier.
3. **The B4 bank-size check misses banks under 40.** Coordinate Geometry Dash serves 24 and 21 but is extracted as 45. Scale Factor Scaling serves 38 and 31 but is extracted as 46. Spot the Error serves 35 and 30 but is extracted as 110.
   - `extract-banks.py` records `scoped_to_level: false` and counts the whole unfiltered pool, so B4 passes them.
   - This is in shared tooling, so it should be fixed in the extractor or in B4, not game by game.
4. **`?level=` ignored, or quietly serving another bank.** Ten of the 12 games (all but Word Problem Decoder and Probability Paradox). Index Laws, Trig Worms, Bearing Blitz and Prime or Composite log every run under one fixed level.
   - `?level=constructor` (an Object prototype key) passes the `QUESTIONS[level]` test in Surd Simplifier and Standard Form Blitz, and Start then throws, so the game cannot be played.
   - This is the resit audit's class 8. It belongs in one roster-and-checker change.
5. **Input accepted after an answer is marked.** Prime or Composite and Word Problem Decoder. `MaffsNext` handles the wrong-answer pause, but no shared layer locks input once an answer is marked, so each game guards it locally, or not at all.
6. **Pictures not drawn from the question's data (SR-6).** Trig Worms (labels, triangle cap), Coordinate Geometry Dash (non-uniform scale) and Probability Paradox (the simulations). Same class as the resit audit's class 6.
7. **Wrong-answer advance not on `MaffsNext` (canon §7.6).** Surd Simplifier and Standard Form Blitz (1 s), Fraction Snap (1.8 s), Word Problem Decoder (about 1 s), Spot the Error (2 s) and Scale Factor Scaling (its own Next button, no 3 s floor). Not counted as a fault.

**Rulings this needs from you:** whether a contested convention may be the only accepted key (Sleeping Beauty, Two-Child, the inspection paradox); whether the topic categories may overlap in Word Problem Decoder (Reverse Percentage vs Percentages, Standard Form vs Number & Place Value); whether a "strategy error" counts as an error in Spot the Error (l4_023, ks3_016); and whether 11.1% at Spot the Error GCSE makes it CRITICAL.

---

## Rulings, Jon 6 Oct 19:15

- A true statement is never a wrong option. An option with the right
  value by a wrong method names the fault in its own text, or goes.
- A contested convention is stated in the question: roulette "American
  wheel"; quartiles name the method; Monty Hall says the host knows and
  always opens a goat door; 6÷2(1+2) removed; "expand and simplify"
  names the form.
- Probability Paradox states its assumptions; Sleeping Beauty accepts
  1/2 and 1/3; the envelope item keyed "can't tell". Word Problem Decoder
  uses one category scheme, accepting both where both genuinely fit. In
  Spot the Error a choice of strategy is not an error; the GCSE set is
  critical.
- Trig Wars' self-harm and suicide idioms removed; the SR-14 scanner's
  humour fields extended.
- One shared "answer once" lock for the 7 games; one shared level
  resolver.
- Unlist Expectation Station and Trig Identity Duel; not Gradient Hunter
  or Trig Wars. Bank size alone is never a reason to unlist; expansions
  Expectation Station first, then Gradient Hunter.
