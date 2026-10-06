# Answer-key audit, tranche 2: 12 more games (6 Oct 2026)

**Status: report only, as delivered to Jon on 6 Oct 2026.** Read-only audit of main at `3e46400`, by the same method
as tranche 1 (`audit-tranche1-2026-10-06.md`). Follow-up: `expectation-station` and `trig-identity-duel` unlisted
(relist checklists, todo §1.55 and §1.56); Core Maths Paper 1's four faults fixed under a new verifier, `scripts/verify-core-maths-paper1.py` (PR #86); Jon's rulings
of 6 Oct 19:15 are the last section. Fixes are marked against each item as they merge.

---

# Tranche 2 audit: 12 more games, answer keys checked — main at `3e46400`, read-only

I changed nothing in the repo (`git status` is clean). The banks were read on a scratch copy. Equatle and Trig Wars are generators, so I ran their own code over every outcome instead; no STOP IF fired. I went back to the source for every CRITICAL and HIGH below: I read the line and redid the arithmetic. The MEDIUM and LOW findings are the audit agents' evidence; I spot-checked them but did not re-derive each one.

**One grading call of mine:** I rated Trig Identity Duel's keyboard re-marking HIGH, not CRITICAL. Tranche 1 rated the same keyboard-only shape HIGH in Prime or Composite, and the two should match. Gradient Hunter's version stays CRITICAL (judgement call) because a plain mouse click reaches it on every question.

**Housekeeping:** PR #82 (unlisting Trig Worms and Spot the Error) merged on a green Gate. Main's full run on the merge, `83098a4`, is **green**.

## 1. Summary

Bold sizes are below the 40-question minimum. The bank size is what each level actually serves, measured in Chromium, not the size of the extracted pool. "JC" marks a judgement call.

| Game | Portal card → what is served | Items checked | C | H | M | L | Worst fault |
|---|---|---|---|---|---|---|---|
| `expectation-station` | core **20** · gcse **15** (alevel **10**) | 45 | 1 JC | 11 | 5 | 6 | A "wrong" stage-3 card is a true statement on 6 of the 10 A-Level items; stage 1 accepts the wrong tile 0.0004 |
| `trig-identity-duel` | gcse 50 (alevel 49; `level4` serves GCSE) | 99 | 0* | 7 | 2 | 5 | Lines 227–229: three wrong keys, and each correct answer is on screen and marked wrong |
| `spot-the-muppet` | bare → gcse **20** · core **12** (ks3 **18**) | 50 | 0 | 5 | 4 | 6 | core_004: "simple interest gives £2,000" is true and marked wrong |
| `terrible-advice` | bare → gcse **20** · core **12** (ks3 **18**) | 50 | 0 | 4 | 4 | 5 | gcse_006: two options both say "correct, 2.45 m"; only one is accepted |
| `core-maths-paper1` | **36** (one level) | 36 | 0 | 4 | 2 | 5 | Q32 is keyed £44.70, the answer is £34.67, and no option is right |
| `gradient-hunter` | gcse **15** (core **20**, alevel **10**) | 45 | 1 JC | 0 | 4 | 5 | Clicking the revealed correct answer re-scores it, unlimited, onto the leaderboard |
| `trig-wars` | gcse (ignored); generator | full grid | 1 JC | 1 JC | 3 | 4 | The computer's hits are logged as the player's correct answers and score |
| `wrong-on-the-internet` | bare → gcse **20** · core **10** (ks3 **15**) | 45 | 0 | 2 JC | 9 | 9 | Roulette keyed 18/38; a UK wheel gives 18/37, so "Depends on wheel" is right |
| `52dle` | daily puzzle, 20 in rotation | 20 | 0 | 1 | 0 | 5 | `parseInt` cuts decimals, so 23.9 wins a puzzle whose answer is 23 |
| `higher-power` | ks3 40 (each level serves its own 40) | 129 | 0 | 1 | 4 | 4 | Pairs mode rejects a match between equal-value cards (2⁸ and 4⁴ both show "256") |
| `core-maths-paper2b` | **36** (one level) | 36 | 0 | 1 JC | 2 | 1 | Q28: option D picks the same policy as the key, for a reason the paper itself teaches |
| `equatle` | daily from a pool of 23,399 | all targets; 114,786 equations | 0 | 0 | 0 | 5 | Keys, validator and colour scoring all correct; an end-screen button is broken |
| **Total** | | | **3** | **37** | **39** | **59** | |

\* Trig Identity Duel at A-Level is on the CRITICAL line. 3 of its 49 items (6.1%) mark the correct answer wrong. If the two value-equal items at lines 243–244 count too, it is 5 of 49 (10.2%).

## 2. CRITICAL and HIGH faults

### Expectation Station
- **CRITICAL (JC): the stage-3 "wrong" cards are true statements.** The screen shows only E(X) and four cards, with no question. These distractors are true from the table:
  - **es_alevel_001 (:369):** "The median of X is 3". Cumulative probabilities run 0.1, 0.3, 0.6, so it is true.
  - **es_alevel_002 (:370):** P(X = 1) = 0.4 is the largest probability, so "X = 1 occurs more than any other value" is true.
  - **es_alevel_003 (:371):** two true cards. "X = 3 is the most probable outcome" (0.4 > 0.2) and "60% exceed the mean" (P(X > 2.6) = 0.6).
  - **es_alevel_004 (:372):** P(X ≥ 1) = 0.55, so "more likely to break down than not" is true. The game's own explanation says so.
  - **es_alevel_007 (:375):** the median is 5, as the card says.
  - **es_alevel_010 (:378):** P(profit) = 0.5, as the card says.
  - **es_gcse_001 (:352):** P(3 or 4) = 0.5, so "Half the scores are above 2.5" is true.
  - **es_gcse_005 (:356):** P(heads) = 0.5, which the explanation itself states.
  - **es_core_005 (:334):** P(X = 0) = 0.72, so "Most transactions need no assistance" is true.
  - **es_core_017 (:346):** the 74% conversion rate is the explanation's own figure.
  - **Share of each level:** A-Level 6 of 10, GCSE 2 of 15, Core 2 of 20.
- **HIGH, es_alevel_006 (:374):** stage 1 marks a tile with `Math.abs(x − p) < 0.001` (:674). The wrong tile 0.0004 is 0.0003 from the true 0.0001, so it is accepted and the table shows "complete". This is the 21 Sep tolerance class, still live in stage 1.

### Trig Identity Duel
- **:172:** largest angle of the triangle 7, 9, 11. cos C = 9/126 gives C = 85.904°, so the answer is 85.9°. The key is 86.2°, and 85.9° is not offered.
- **:227, :228, :229:** sin A = 3/5 and cos B = 5/13, so cos A = 4/5 and sin B = 12/13.
  - sin(A+B) = 15/65 + 48/65 = **63/65**. The key is 56/65.
  - cos(A+B) = 20/65 − 36/65 = **−16/65**. The key is −33/65.
  - cos(A−B) = 20/65 + 36/65 = **56/65**. The key is 63/65.
  - Each correct value is offered as a distractor and marked wrong. The keys look as if sin B and cos B were swapped.
- **:243 and :244:** "Expand and simplify" keys 1 ± sin 2x. The distractor 1 ± 2 sin x cos x is identical in value. JC on whether "simplify" names the form.
- **Keyboard re-marking (handle(), :285):** buttons are disabled only by CSS class and have no answered guard.
  - Pressing Enter on the revealed correct option re-scores it.
  - Repeated presses during the 1 s pause queue extra advances, and questions are skipped unseen.

### Spot the Muppet
- **core_004 (:317):** the stem never says compound; the topic field is never displayed. So "simple interest gives £2,000" (1000 + 1000 × 0.05 × 20) is true and marked wrong.
- **core_008 (:325) and ks3_005 (:241), JC:** distractors with the right value by an invalid method.
  - core_008: "£120 − £20 = £100" (the key is £120 ÷ 1.2 = £100).
  - ks3_005: "mean = (2 + 10) ÷ 2 = 6" (the true mean is 30 ÷ 5 = 6).
- **core_002 (:313), JC:** the key condemns a valid marginal-cost argument. £1.30 for 250 ml is 0.52 p/ml, below 0.70 p/ml.
- **Input after marking:** `nextQuestion()` has no guard. A double-click on Next lands on the new question's options, and that question is answered unseen; reproduced in Chromium.

### Terrible Advice
- **gcse_006 (:293):** "Prudence is correct — upper bound is 2.45m" is marked wrong. The key is "Prudence is correct this time — … 2.45m".
- **core_002 and core_007, JC:**
  - core_002 is the same valid marginal-cost argument as in Spot the Muppet.
  - core_007: Wendy's unweighted mean, 70%, equals the weighted mean (600 + 2100 + 800) ÷ 50 = 70%. So "Wendy is correct — the overall average is 70%" is a true statement, marked wrong.
- **Double-click on Next answers the next question unseen**, the same mechanism as Spot the Muppet.

### Core Maths Paper 1
**All four FIXED, PR #86**, under `scripts/verify-core-maths-paper1.py` (CI group B), which fails on the old file at each.
- **Q32 (:462–465):** simple interest A = 5000 × 0.035 × 3 = £525.00. Compound B = 5000 × 1.036³ − 5000 = £559.67. B wins by **£34.67**. **FIXED, PR #86:** keyed £34.67; the other options are named errors (rates on the wrong account types, both simple, one year only).
  - The key is "B by £44.70", from the working's false £569.70. No option is correct.
- **Q9 (:296–300):** keyed "Yes" to "more than half the class scored above 51" (the median). At most half the values are strictly above the median, so the answer is No. The working concedes it ("slightly imprecise"). **FIXED, PR #86:** keyed "No — at most half the values can be above the median"; the old "No" with a wrong reason removed (Jon's ruling).
- **Q7 (:282–284):** option C, "Discrete, qualitative, continuous, discrete", is the same classification as the key, because discrete and continuous imply quantitative. **FIXED, PR #86:** option C now treats shoe size as continuous.
- **Q1 (:238), JC:** the IQR of 9 values is keyed 12, which needs the inclusive-median convention. **FIXED, PR #86:** the stem names the (n + 1)/4 method, keyed 14; 12 (inclusive), 32 (range) and 5 (positions) are the distractors.
  - The (n+1)/4 rule gives 29 − 15 = 14, and so does a calculator's exclusive method.
  - 14 is not offered, and the question names no method.

### Gradient Hunter: CRITICAL (JC)
- **renderInterpretations (:1046–1062):** buttons get only a `locked` class, and `onclick` stays live.
- After a wrong pick, clicking the green-revealed correct option runs the callback again. Each click adds the score again, logs another correct answer and appends another Next button, with no limit.
- Reproduced in Chromium: 38/16 over 10 questions, with 30 `question_answered` events. The total goes to the leaderboard.
- This is reachable on every question by the natural action of clicking the right answer once it is shown.

### Trig Wars
- **CRITICAL (JC), :888–903:** every hit, by either side, runs `_twHits++`, logs `correct:true` and feeds `submitScore`. Reproduced: a player who never hit lost 3–0 and submitted a score of 3.
- **HIGH (JC), :968:** the trig panel shows Vx = power·cos θ·**0.28**, while it labels V as the power.
  - At V = 60, θ = 45° it shows Vx = 11.9 beside cos 45° = Vx/V = 0.707.
  - But 11.9/60 = 0.198, so the panel contradicts its own formula on every screen.

### Wrong on the Internet (both JC)
- **gcse_004 (:458–461):** keyed 18/38, the American wheel. A UK or European wheel gives 18/37, so the distractor "Depends on wheel" is correct.
- **gcse_011 (:537):** keyed "0.12 (if independent)". The post never says A and B are independent, so "Need more information" is correct.
  - The stage-2 key's "Addition gives P(A OR B)" is false unless the events are mutually exclusive.

### 52-dle, line 900
- `parseInt(input.value)` cuts a decimal to a whole number before the exact-match check, on all 20 puzzles. Reproduced: 23.9 is accepted as 23 and wins.
- 314.16 wins the π puzzle, and the π hint "100 × π rounded to 2dp" invites exactly that entry.

### Higher Power, line 724
- Pairs mode matches by `pairId`, not by value. Matching 2⁸ to the "256" card that belongs to 4⁴ is rejected (reproduced), and the two "256" cards look identical.
- The same applies to φ/φ (GCSE), 0/0 and π²/6 twice (A-Level).
- About 6% of KS3 and GCSE Pairs games and about 11% of A-Level Pairs games deal such a pair.

### Core Maths Paper 2B, Q28 (:383–387), JC
- Option D, "Data breach — larger potential loss", picks the same policy as the key, for the risk-aversion reason that Q27 and Q34 teach.

## 3. MEDIUM and LOW, briefly

- **Expectation Station**
  - es_gcse_005 says "biased coin", but its table is exactly Bin(3, ½).
  - es_alevel_005 keys E(X) = £2.50 where X is the die score (E = 3.5).
  - es_alevel_009 calls a left-skewed distribution "right-skewed".
  - Several "true within the model" cards (JC).
  - LOW: a double-click on Check spends the retry.
- **Wrong on the Internet**
  - The banner always says "they're wrong", including on 4 items where the poster is right.
  - gcse_009, ks3_012 and ks3_010 have wrong or contradictory reasoning text.
  - gcse_001 keys 6÷2(1+2) = 9 (JC).
  - core_006: "humans can't survive" in a jokey key (SR-14, JC).
  - Stage 2 has 3 options.
- **Gradient Hunter:** alevel_009, 010 and 007 state tangent gradients (150, 4, 5) that disagree with the model or the drawn curve (98.0, 3.25, 4.5).
- **Trig Wars**
  - Shells that land on a tank miss 9–12% of the time, because the ground check runs before the hit check.
  - The miss advice is backwards above 45°.
  - Vx and Vy are labelled "u/s" but are pixels per frame.
  - **SR-14 (JC):** "Are you… shooting yourself?" (:791), "nearly did themselves in" (:804), "☠ WE LOST ONE" and "💀 DOWN!" (:893).
- **Trig Identity Duel**
  - :188 is keyed 30°; 150° is also valid, but not offered.
  - :193's kite is under-specified.
  - The "hidden" timer is visible and feeds the score, against timer-policy.md.
- **Spot the Muppet and Terrible Advice**
  - The loan item's figures are wrong (the real repayment is about £364/month).
  - TA's "square roots always have ± solutions" is false.
  - The 562.45 vs 562.43 slip.
  - SR-14: the "patients" joke, which the scanner cannot see (class 9 below).
- **Core Maths papers**
  - Paper 1 Q9's box-plot whiskers are drawn in the background colour, so they are invisible. **FIXED, PR #86** (the chart's axis grey, 5.7:1).
  - Paper 1 Q27's CPI pair is already in the quoted-statistics audit.
  - Paper 2B Q23's Monty Hall never says the host knows where the car is.
  - Options are never shuffled, and B is the key on 26 of 36 in 2B.
- **Higher Power**
  - KS3 Higher or Lower crashes at streak 11+ (1 in 40 per question); see class 4.
  - Razor pairs from A-Level are served at KS3.
  - gcse_19 shows "2.0000…" for 1.99989.
  - "2³² is the max 32-bit value" is false (2³² − 1).
- **Equatle**
  - :337: the leaderboard-teaser sweep was pasted into an `onclick` attribute, so the button throws.
  - Result 0 is refused without saying so.
  - UTC/BST off-by-one in the puzzle number. 52-dle has the same.
- **52-dle:** "emirp twins/cousins" misuse those terms; "100 is the basis of our decimal system" is wrong (the base is 10).

## 4. Bug classes in two or more games

Each class is counted once, with tranche 1's games included where tranche 1 already found it.

1. **Input accepted after marking** (tranche 1: Prime or Composite, Word Problem Decoder). Tranche 2 adds Gradient Hunter, Trig Identity Duel, Spot the Muppet, Terrible Advice and Expectation Station (LOW). That is **7 games**.
   - `MaffsNext` locks only the wrong-answer pause. Nothing shared locks an answer once it is marked.
   - This is now clearly a shared-layer fix: one "answer once" lock owned by the shared assets, not seven local guards.
2. **True or second-valid distractors that B11 cannot see** (tranche 1 class 1). Expectation Station stage 3, Wrong on the Internet, Spot the Muppet and Terrible Advice (right value by a wrong method), Core Maths Paper 1 Q7 and Q1, Paper 2B Q28, Trig Identity Duel 243–244, and Higher Power's equal cards.
3. **Hand-written wrong keys in games without a verifier** (tranche 1 class 2): Trig Identity Duel ×4 and Core Maths Paper 1 Q32 and Q9.
4. **`?level=` silently served or crashing** (tranche 1 class 4): Trig Identity Duel, Wrong on the Internet, Expectation Station, Terrible Advice and Higher Power crash on `?level=constructor`; `level4` serves GCSE in Trig Identity Duel; Trig Wars, both Core Maths papers and Higher Power's unknown keys fall back silently. Higher Power's KS3 crash at streak 11 is the same unguarded-pool shape.
5. **Banks under 40, sometimes invisible to B4** (tranche 1 class 3). Nine of the 12 games have a level under 40.
   - Spot the Muppet extracts as 50 per level but serves 18, 20 and 12. That is the same extractor gap as in tranche 1.
6. **Pictures or words not drawn from the data** (tranche 1 class 6): Gradient Hunter's tangent claims, Paper 1 Q9's whiskers, Trig Wars' panel.
7. **Game-local marking instead of `MaffsAnswer`**, the resit audit's class 2. New instances: 52-dle (`parseInt`) and Expectation Station (`< 0.001`).
8. **New: scores that don't measure the student's first answers.** Trig Wars (the computer's hits), Gradient Hunter (re-marks), Wrong on the Internet, Expectation Station and Terrible Advice (raw points shared across session lengths), and Higher Power's Pairs board (known).
9. **New: SR-14 scanner coverage gap.** `check-content-safety.py`'s humour fields miss `huffyResponse`, `advice` and `title` (Spot the Muppet, Terrible Advice) and Trig Wars' quip arrays.
   - This is shared infrastructure: fix the field list once rather than reword games one by one.
10. **Sweep markup pasted into an attribute:** Equatle now, Chart Interrogator in March. Tier 1 doesn't fail it, because the throw happens only on click.

## 5. Rulings needed from you, with my recommendation

1. **Expectation Station stage 3: may a true statement be a "wrong" option?**
   - I recommend no: a distractor must be false as a statement. That makes A-Level CRITICAL at 6 of 10.
   - I'd unlist it now, using PR #82's mechanism.
2. **Unlisting the others.**
   - Trig Identity Duel: I'd unlist it, since 4 wrong keys means a correctly worked answer is marked wrong.
   - Gradient Hunter and Trig Wars: I would **not** unlist them. Their CRITICALs inflate scores but never mark a first answer wrong. Fix them in a batch.
3. **Re-answer faults: one shared answer lock (recommended) or a fix per game?** Seven games now share the shape, which meets your own CLASS CHECK test.
4. **Contested conventions.** I recommend the question states the convention, as SR-1 already does for precision.
   - Roulette: say "American wheel", or key 18/37.
   - Quartiles: name the method.
   - Monty Hall: add the host-knows sentence.
   - 6÷2(1+2): remove it. It tests notation ambiguity, not maths.
5. **"Right answer, wrong method" distractors** (Spot the Muppet and Terrible Advice).
   - I recommend: if an option's statement is true, it is not wrong. Either the option names the method's fault explicitly, or it goes.
6. **"Expand and simplify" (Trig Identity Duel :243–244):** name the form ("in terms of sin 2x"), or accept both. I recommend naming it.
7. **SR-14:**
   - Trig Wars' "shooting yourself" and "did themselves in" are self-harm and suicide idioms played for laughs. I recommend removing them.
   - Extend the scanner's humour fields (class 9) in the same PR, so it fails before and passes after.
8. **Banks under 40 in 9 games:** I recommend no unlisting for size alone. Order the expansions by resit relevance: Expectation Station and Gradient Hunter first.

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
