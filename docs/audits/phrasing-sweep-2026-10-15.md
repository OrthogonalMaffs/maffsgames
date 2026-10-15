# Phrasing sweep: switch point or sufficient condition, outside Better Value (15 Oct 2026)

Contract PHRASING-SWEEP (Project Claude for Jon, 15 Oct 2026, 13:20; verbatim in
`docs/handover/contracts/2026-10-15-phrasing-sweep.md`). Read-only: no game, bank, verifier, ledger or findings file
changes. Cloud lane; every classification is mine, from the arithmetic shown, and Jon may overrule any of it.

## The rule (docs/canon.md §7.1.5, as merged by #407, 83f9a7a), verbatim

> ### 7.1.5 Better Value content rules: reading a threshold claim
>
> Ruled by Jon, 15 Oct 2026 (contract BV-RULINGS).
>
> **"Becomes … after N" and "only after N" name the switch point. "If" and "worth it when" state a
> sufficient condition.**
>
> - **Switch point** ("X becomes better value after N", "X is better value only above N"): true only
>   when N is the break-even itself: "after N" or "above N" means X is first strictly cheaper at N + 1, "from
>   N" means at N, and "approximately N" means N is within ±0.1 of the crossover. A threshold past the
>   break-even makes the claim false. A wrong threshold option in this form needs no other wording, though "only" may be added
>   to make the claim plain.
> - **Sufficient condition** ("X is better value if you buy N or more", "X is worth it when you use it at
>   least N times"): true whenever every count it covers is past the break-even, so a threshold past the
>   break-even is **true**. A wrong option in this form must either reach below the break-even or say
>   "only" (better-value-s1-001).
> - **Checked in CI:** `verify-better-value-claims.py` reads every crossover claim as a switch point;
>   `verify-better-value.py`'s BREAK_EVEN check fails a sufficient-condition option that is true as written.

## Method

- **What was searched:** every live game's extracted bank (`data/banks/*.json`, 96 games, made from main at 83f9a7a by
  `scripts/extract-banks.py`), and the source of every game with no extracted bank (the generator games), excluding
  better-value. The terms: "becomes", "only after", "only when", "worth it when", "worth it if", "break-even",
  "cheaper when", "better value when", "after how many" and "from how many". Separately, every question string
  containing both "if" and a count or threshold word ("how many", "at least", "or more", "minimum", "least number",
  "smallest number", "fewest", "worth").
- **Raw matches:** 98 term matches. Each item appears once per level that serves it, so this is fewer unique items
  than matches; the generator sources added none. There were also 7 "if" + count questions.
- **A hit** is a question whose wording states a condition, a switch point or a threshold in this phrasing. Matches
  that use the words in another sense ("the equation becomes", "if you counted …, how many years") are listed under
  **Screened out**, with the reason, and not classified.
- **Each hit's key is recomputed**, and the hit is classed as:
  - **CLEAR:** the wording and the key agree under the rule;
  - **AMBIGUOUS:** two readings give different keys (both given);
  - **WRONG:** the key contradicts the rule.

## Totals

| Group | Hits | CLEAR | AMBIGUOUS | WRONG |
|---|---|---|---|---|
| Year 6, KS3 and GCSE (Essentials: no hit) | 6 | 5 | 1 | 0 |
| Core | 6 | 5 | 1 | 0 |
| A-Level | 1 | 1 | 0 | 0 |
| L4 | 1 | 1 | 0 | 0 |
| **All** | **14** | **12** | **2** | **0** |

No WRONG key anywhere, so the contract's STOP IF (a wrong key on a live Essentials or GCSE game) did not fire.
14 hits is under the 40 stop. Year 6 and KS3 items are grouped with GCSE, before Core.

## Year 6, KS3 and GCSE

### 1. probability-pioneer, Year 6: "If two outcomes are equally likely, each has probability 0.5" — **AMBIGUOUS**

- **Item:** the true-or-false stage. The statement is verbatim as above. Key: **false**. Explanation: "Only when there are
  exactly two outcomes. Each face of a dice is equally likely, and each has probability 1/6."
- **Reading A** ("if" as a sufficient condition over *any* two equally likely outcomes, which is the rule's reading of "if"):
  two faces of a die are equally likely at 1/6 each, not 0.5, so the statement is **false**, as keyed.
- **Reading B** ("two outcomes" as the experiment's *only* two outcomes, the reading the explanation itself
  names): two equally likely outcomes that make up the whole sample space have 1 ÷ 2 = 0.5 each, so the
  statement is **true**.
- **Why it matters:** the rule settles what "if" does, but not what "two outcomes" refers to, and a Year 6 student
  can take either. The explanation's "only when there are exactly two outcomes" is Reading B's condition.

### 2. wrong-on-the-internet, GCSE, woti_gcse_013 (circle theorems) — **CLEAR**

- **The post:** "Angle at centre = angle at circumference. So if the centre angle is 80°, the circumference
  angle is 80°." Stage 1 key: "Circumference angle = 40°".
- **The hit:** a stage 2 distractor, "The two angles are equal, but only when the arc is minor".
- **Recomputed:** angle at circumference = 80° ÷ 2 = 40°. The angle at the centre is twice the angle at the
  circumference for any arc (a major arc's reflex centre angle too), so "equal, but only when the arc is minor"
  is false under any reading. The key stands.

### 3. truth-buster, Tier 1, tb_t1_017 — **CLEAR**

- **Statement:** "A number is always bigger than its reciprocal." Key: **false** (counterexample 0.2, whose reciprocal is 5).
- **The hit:** the reveal, "A number beats its reciprocal only when it is greater than 1 or between −1 and 0".
- **Recomputed:**
  - For x > 0, x > 1/x ⇔ x² > 1 ⇔ x > 1.
  - For x < 0, multiplying by x reverses the inequality: x² < 1 ⇔ −1 < x < 0.
  - So "only when" is exact (if and only if). The key and the reveal agree.

### 4. probability-paradox, GCSE/Core, bias round: "So if a band never gives up, it will become famous" — **CLEAR**

- **Scenario:** "'Every famous band I know of kept going when things got hard. So if a band never gives up, it will
  become famous.'" Question: "What bias is this?" Key: **Survivorship bias**.
- **The hit:** the sufficient-condition claim is the faulty inference the item tests. "Never gives up" is
  observed only among the famous bands that survived, so it cannot be shown sufficient. Survivorship bias is right,
  and the other options (confirmation bias, availability, anchoring) do not describe the sampling fault.

### 5. probability-paradox, GCSE/Core, the envelope problem — **CLEAR**

- **Question:** "What's the expected value if you switch?" Key: **"Cannot determine — it depends on how the amounts
  were chosen"**.
- **The hit:** a step reads "if the pairs (£10, £20) and (£20, £40) were equally likely to be used, switching is
  worth £25; if the larger amount is never more than £30, the other envelope holds £10".
- **Recomputed:**
  - The first conditional gives 0.5 × £10 + 0.5 × £40 = **£25**.
  - In the second, a larger amount of at most £30 rules out (£20, £40), so the other envelope holds **£10**.
  - The two sufficient conditions give different values, which is exactly why the key is "cannot determine".

### 6. word-problem-decoder, KS3, wpd_ks3_026: "After how many Earth days …" — **CLEAR**

- **Stem:** "Planet A takes 420 Earth days to complete one orbit. Planet B takes 315 Earth days. … After how many
  Earth days will they next both be back at the starting position at the same time?"
- **Key** (the topic): **Number & Place Value**, from the highlight "how many Earth days will they next both be back".
- **Recomputed:** 420 = 2² × 3 × 5 × 7 and 315 = 3² × 5 × 7, so LCM = 2² × 3² × 5 × 7 = **1,260 days**. "After how
  many" asks for the next coincidence, a single number, not a switch point. Nothing in the rule bears on it.

## Core

### 7. spot-the-muppet, Core, stm_core_009 (break-even) — **CLEAR**

- **Advice:** "Fixed costs £2,000. Each unit costs £5 to make and sells for £15. Break-even = £2,000 ÷ £15 = 133.3,
  so 134 units. Just divide by selling price." Key: **"Benny is wrong — it's 200 units"**.
- **Recomputed:** contribution £15 − £5 = £10, and break-even £2,000 ÷ £10 = **200**. That is a whole number, so the
  crossover and the first whole count agree: profit is £0 at 200 and positive from 201. The distractors (134, 400,
  100) are all false.

### 8. terrible-advice, Core, ta_core_009 (break-even) — **CLEAR**

- The same figures as 7, with key **"Brenda is wrong — it's 200 units"**: £2,000 ÷ (£15 − £5) = **200**. The
  distractors are 134, 400 and 20,000.

### 9. wrong-on-the-internet, Core, woti_core_007: "Break-even point?" — **AMBIGUOUS**

- **Post:** "My fixed costs are £5,000. Each unit costs £10 to make and sells for £25. Break-even point?"
- **Keys:** stage 1 **"334 units"** (the options are 334, 200, 500 and 167); stage 2 "QuickBusiness ignored the £10 cost:
  divide by £25 − £10". A stage 2 distractor reads "CarefulCalc should not have rounded 333.3 up to 334".
- **Recomputed:** the crossover is £5,000 ÷ (£25 − £10) = **333.3** units. At 333 units contribution is
  333 × £15 = £4,995, a £5 loss. At 334 it is £5,010, a £10 profit.
- **Reading A** ("break-even point" as the crossover, the sense the rule gives "break-even"): the answer is
  **333.3**, which is not among the stage 1 options. The stage 2 distractor "should not have rounded 333.3 up to 334"
  becomes true.
- **Reading B** ("break-even point" as the whole number of units needed to stop making a loss): the answer is
  **334**, as keyed, and the distractor is false.
- **Why it matters:** the crossover is not a whole number here, so the two readings differ. The items above (200)
  do not have this problem.

### 10. maths-court, Core, mc_core_001: "it's worth it if you're lucky" — **CLEAR**

- **Problem:** "A game: P(win £5) = 0.3, P(win £0) = 0.7. Game costs £2. Is it worth playing?" Key: Monte Expect,
  **"Not worth playing"**.
- **The hit:** the phrase is in a wrong argument's working (Optimist Owen).
- **Recomputed:** E(X) = £5 × 0.3 + £0 × 0.7 = **£1.50** < £2, so the game makes an expected loss of **£0.50** a
  game. "Worth it if you're lucky" is a sufficient condition about one outcome, not the expected value, and the
  item marks it wrong. The key stands.

### 11. core-maths-paper2c, Core, Q34 (§3.13): "Yes — but only when k > 0" — **CLEAR**

- **Stem:** "A population is modelled by P = 1200e^(0.04t). A student claims: 'The doubling time is constant
  regardless of the starting population.' Is the student correct?"
- **Keys:** the page keys option 2, "Yes — for exponential models, doubling time is constant", and accepts
  options 2 and 4 (accept [1, 3], 0-based). Option 4 is "Yes — but only when k > 0".
- **Recomputed:** the doubling time is T = ln 2 ÷ k = 0.6931 ÷ 0.04 = **17.3**, independent of the 1,200, so the claim
  holds. A doubling time exists only for growth, k > 0, and here k = 0.04. So "only when k > 0" states a true
  necessary condition, and accepting both "Yes" options is consistent with the rule.

### 12. graph-sketcher, Core (also A-Level and L4 listings), CM13: "(break-even)" — **CLEAR**

- **Stem:** "What does x = 4 represent in context?" for P = 0.5x³ − 4x² + 8x (profit, £000, against price, £). Key:
  **"The price at which profit is zero (break-even)"**.
- **Recomputed:** P(4) = 0.5 × 64 − 4 × 16 + 8 × 4 = 32 − 64 + 32 = **0**. The key is right.
- **Note, for Jon:** P = 0.5x(x − 4)², so x = 4 is a double root. Profit touches zero there and stays positive on
  both sides (P(3) = 1.5, P(5) = 2.5). "Break-even" is still correct as "profit is zero". The distractors (maximum
  profit, minimum cost, the optimal price) are false: P rises from x = 4 to 12 at x = 6.

## A-Level

### 13. proof-builder, A-Level, counterexample round: "equality only when …" — **CLEAR**

- **Statement:** "If z₁ and z₂ are complex, then |z₁ + z₂| = |z₁| + |z₂|". Key counterexample: **z₁ = 1, z₂ = i**.
  The misconception text says "equality only when one is a non-negative real multiple of the other (or either is 0)".
- **Recomputed:** |1 + i| = √2 ≈ 1.414, but |1| + |i| = 2, so the key refutes the statement. The distractors
  z₁ = z₂ = 1 (2 = 2) and z₁ = 2, z₂ = 3 (5 = 5) satisfy it, and "This statement is actually TRUE" is false. The
  equality case of the triangle inequality is exactly as stated (an "only when" that is if and only if).

## L4

### 14. truth-will-set-you-free, L4, Tier 1, the extraction fan — **CLEAR**

- **Scenario:** "The fan motor (output F) runs only when the power switch is on AND the safety guard is in place."
  C (dust sensor) is "not used in output logic". Key: **A · B**, outputs 0 0 0 0 0 0 1 1 over ABC = 000 … 111.
- **Recomputed:** A · B is 1 only at 110 and 111, matching the outputs.
- **Note:** read strictly, "only when" is a necessary condition (F ⇒ A · B). That alone would also admit A · B · C,
  but C is stated as unused, and F = 0 is not offered. Among the options (A + B, A · B̄, A · B · C, A · B), only
  A · B fits the scenario, and the item's "logic" line ("runs when … AND …") supplies the sufficient half.

## Screened out (matched a term, not this phrasing)

| Game | Item | Match | Why not a hit |
|---|---|---|---|
| fermi-lab | data-centre-heat, nuclear-cooling-water (all levels) | "becomes heat", "If 33% becomes electricity, 67% …" | Energy conversion; 1 − 0.33 = 0.67 is right |
| fermi-lab | count-to-billion, drive-to-sun, eq_packed_lunch, eq_markers | "If you counted …, how many years" | A hypothetical premise, not a threshold |
| word-problem-decoder | wpd_ks3_019, wpd_ks3_032 | "If there are 400 students …, how many …" | Premise-if (substitution) |
| expectation-station | es_core_040 | "beds that become free" | Context noun phrase |
| graph-sketcher | CM7 | "Mass becomes negative" (a limitation distractor) | Not a threshold; false for exponential decay |
| higher-power | gcse_16 | "1 pound becomes 1.63 pounds" | A fact: 1.05¹⁰ = 1.629 |
| matrix-crunch | 4 | "subtracting a negative becomes addition" | Misconception text |
| proof-builder | 2, 3 (induction) | "this becomes:", "RHS becomes …" | Algebra step |
| proportion-blaster | 32 | "a value becomes 200" | Percentage-change context |
| scale-factor-scaling | 10 | "area becomes a QUARTER" | Scale-factor fact: (½)² = ¼ |
| simultaneous-solver | E15 | "the series total becomes 21 Ω" | Equation context |
| truth-buster | tb_t3_019 | "spheres become vanishingly small" | Reveal title |

## For Jon

- **The two AMBIGUOUS items are wording problems, not arithmetic ones.** Each item's current key is right under
  one reading:
  - **probability-pioneer:** "If two outcomes …". A candidate wording is "If an experiment has exactly two
    outcomes and they are equally likely …" (true), or keep false and say "any two outcomes".
  - **woti_core_007:** "Break-even point?" with a non-whole crossover. A candidate wording is "How many units must be
    sold to break even?" (334), or key 333.3.
- **The rule names Better Value; no other bank uses "becomes … after N" or "worth it when" for a threshold.** The
  only break-even items outside Better Value are 7, 8, 9 and 12, all stated as the level point, and only 9's crossover
  is not whole.
