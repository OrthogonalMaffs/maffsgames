# Test the Claim — every answer key recomputed (30 Sep 2026)

To-do §1.14 (fixed) and §1.26 (the class-check list). The verifier is
`scripts/verify-test-the-claim.py`, and it runs in CI on every push.

## What was wrong

Every probability, critical value, p-value and verdict in the bank was typed by hand, and nothing
recomputed any of them. §1.14 knew of one wrong key (P3). The verifier found **16 of the 48 items
wrong** on numerical grounds. Reading the step code then turned up two marking bugs that affected
many more items:

- **Two decisions were backwards.**
  - **P7** (Po(16), x = 9, 5% lower tail): the true P(X ≤ 9) is 0.0433, not the stated 0.0682. So
    9 is in the critical region and H₀ is **rejected**. The game marked the right answer wrong at
    Steps 3, 4, 5 and 6.
  - **Step 6's "Action" was keyed backwards on every item that rejects H₀** (24 of 48). It marked
    "sufficient evidence … to **reject** the claim that ⟨H₁⟩" correct. That contradicts the model
    answer the game prints straight afterwards.
- **P3's critical region was impossible to enter.** The correct region, X ≥ 8 with no lower
  region, could not be typed in, and the value the game accepted, 0, is wrong maths. B11 and P9
  had the same trap all along.
- **Wrong displayed probabilities, and the boundaries built on them:** B6, B8, B9, B11, P5, P6, P7
  and P11 showed probabilities that were wrong, some by a factor of 2. The critical boundary was
  wrong in B6, B8, P5, P6 and P7.
- **The p-value route disagreed with the critical-region route on two-tailed items.** Step 4
  compared the one-tail probability with the full significance level, so B3 (0.0409 at 5%) and P3
  (0.0335 at 5%) marked a student who followed the instruction wrong.
- **No p-value and no explanation on all 24 Normal and correlation items.** The p-value route
  could never be marked right, and a wrong answer showed "Expected: undefined" or "Incorrect.
  undefined".
- **The correct Step 6 conclusion appeared twice on B8, B10, B12 and P8.** The function that
  builds the wrong conclusions returned the right one unchanged whenever the context had no
  direction word it recognised.
- **The PMCC table disagreed with the exam booklet in five cells** (below), and C5's critical value
  was wrong because of it.
- **Draft prose was shipped** as the hint after a wrong answer: B8 ("Need further: assume CR is …"),
  P9 ("closest tail prob for x=9 region") and P11 ("— nearest tail").

## Rulings applied (Jon, 30 Sep 2026)

1. Correct every numerical failure in one pass. Fill the missing p-values and explanations for the
   Normal and correlation items from the verifier's own computation; they are listed below for
   review.
2. **Two-tailed items:** Step 4 compares **the probability in the tail** with **half** the
   significance level, and is labelled that way. One-tailed items are unchanged.
3. Step 6 duplicates: fix the shared function and assemble the options with `MaffsOptions.build()`.
4. A probability the student needs but is not shown is a **WARN**. Each such item gets one line
   telling the student to use their calculator's distribution functions.
5. The PMCC values must match the exam booklet. They were checked against it before any was changed;
   see the next section.
6. Remove the draft prose.
7. (Asked mid-pass) Step 6: "…support the claim that…" is the correct action for every item.
8. (Asked mid-pass) Step 3: a blank Lower box means "no lower critical region".

## The booklet check (ruling 5)

Source: Pearson Edexcel Level 3 AS and A level Statistics (8ST0/9ST0), *Statistical formulae and
tables*, Issue 1, August 2017, Table 8, the copy Jon supplied. All **260 cells** (n = 4 to 100, five
columns each) were compared with exact computation from the null distribution of r: **0
disagreements** at 4 d.p. The rows for the seven sample sizes the game uses are copied into the
verifier as `BOOKLET`, and a disagreement there fails CI.

The five wrong cells in the game's table, `CORR_CV`, all corrected to the booklet:

| n | column | stated | booklet |
|---|---|---|---|
| 12 | 1% one-tail (2% two-tail) | 0.6614 | 0.6581 |
| 15 | 1% one-tail | 0.5974 | 0.5923 |
| 18 | 1% one-tail | 0.5480 | 0.5425 |
| 20 | 1% one-tail | 0.5202 | 0.5155 |
| 25 | 1% two-tail | 0.5029 | 0.5052 (so also C5's `criticalValue`) |

0.6614 is the booklet's value for **n = 14** at 0.5%, which looks like a slip onto the wrong row.
C5's decision (r = 0.48, do not reject) is unchanged.

## Before: the verifier on the unchanged bank

It was run before anything was fixed, as the contract required. On the first pass (the data checks
only), 16 of 48 items failed (33%). That tripped the 10% STOP IF, and Jon ruled to proceed. The
final verifier also checks what Steps 4 and 6 mark correct. On the unchanged bank it reports 42
items with at least one FAIL, 203 FAILs in all. Every FAIL is in the list above or is covered by a
ruling:

| Check | Items |
|---|---|
| Step 4 (p-value route) marks a false statement | all 19 two-tailed items (ruling 2), and P7 |
| Step 6 "Action" marks "reject the claim that ⟨H₁⟩" | 24 items that reject H₀ |
| pValue / pValueExpr wrong or missing | B6, B8, B9, P5, P7, P9, P11, and all 24 Normal and correlation items |
| crExplanation missing or draft | B8, and all 24 Normal and correlation items |
| a displayed probability wrong | B6, B8, B9, B11, P5, P6, P7, P11 |
| critical boundary wrong | B6, B8, P3, P5, P6, P7 |
| verdict (inCR / reject) wrong | P7 |
| Step 6 shows the correct conclusion twice | B8, B10, B12, P8 |
| PMCC value wrong (booklet and exact computation agree) | C5, and `CORR_CV` rows 12, 15, 18, 20, 25 |
| z stored wrongly (harmless at 2 d.p.) | N3 (1.8788, should be 1.8783) |
| needed probability not displayed | B3, B6, B8, P5, P6, P9, P11 (now WARN, ruling 4) |

## Corrections — binomial and Poisson: stated → corrected

Generated from a field-by-field comparison of the old and new banks, not typed by hand. Also
changed but not listed: P3's dead first `crBoundaryUpper: 7` key was deleted, because the second
key, 8, was the live and correct one. And the calculator line was added to the scenario of
B3, B6, B8, P5, P6, P9 and P11: *"Any probability not listed can be found with your calculator's
binomial / Poisson distribution functions."*

| Item | Field | Stated | Corrected |
|---|---|---|---|
| B6 | given P(X ≤ 7) | `0.0289` | `0.0576` |
| B6 | given P(X ≤ 8) | `0.0771` | `0.1347` |
| B6 | given P(X ≥ 15) | `0.0154` | `0.0328` |
| B6 | given P(X ≥ 14) | `0.0481` | `0.0942` |
| B6 | crBoundary | `7 or 15` | `6 or 15` |
| B6 | crBoundaryLower | `7` | `6` |
| B6 | pValue | `0.0771` | `0.1347` |
| B6 | pValueExpr | `P(X \leq 8) = 0.0771` | `P(X \leq 8) = 0.1347` |
| B8 | given P(X ≥ 12) | `0.0660` | `0.1254` |
| B8 | given P(X ≥ 13) | `0.0334` | `0.0604` |
| B8 | given P(X ≥ 14) | `0.0149` | `0.0255` |
| B8 | crBoundary | `14` | `15` |
| B8 | pValue | `0.066` | `0.1254` |
| B8 | pValueExpr | `P(X \geq 12) = 0.0660` | `P(X \geq 12) = 0.1254` |
| B9 | given P(X ≥ 14) | `0.0189` | `0.0214` |
| B9 | given P(X ≥ 13) | `0.0532` | `0.0580` |
| B9 | pValue | `0.0189` | `0.0214` |
| B9 | pValueExpr | `P(X \geq 14) = 0.0189` | `P(X \geq 14) = 0.0214` |
| B11 | given P(X ≥ 5) | `0.0072` | `0.0156` |
| B11 | given P(X ≥ 6) | `0.0019` | `0.0033` |
| P3 | crBoundary | `0 or 7` | `none feasible lower; 8 upper` |
| P3 | crBoundaryLower | `0` | `-1` |
| P5 | given P(X ≥ 20) | `0.0161` | `0.0213` |
| P5 | given P(X ≥ 21) | `0.0077` | `0.0116` |
| P5 | given P(X ≥ 19) | `0.0316` | `0.0374` |
| P5 | crBoundary | `21` | `22` |
| P5 | pValue | `0.0161` | `0.0213` |
| P5 | pValueExpr | `P(X \geq 20) = 0.0161` | `P(X \geq 20) = 0.0213` |
| P6 | given P(X ≥ 17) | `0.0261` | `0.0270` |
| P6 | crBoundary | `4 or 17` | `4 or 16` |
| P6 | crBoundaryUpper | `17` | `16` |
| P7 | given P(X ≤ 8) | `0.0341` | `0.0220` |
| P7 | given P(X ≤ 9) | `0.0682` | `0.0433` |
| P7 | given P(X ≤ 10) | `0.1170` | `0.0774` |
| P7 | crBoundary | `8` | `9` |
| P7 | pValue | `0.0682` | `0.0433` |
| P7 | pValueExpr | `P(X \leq 9) = 0.0682` | `P(X \leq 9) = 0.0433` |
| P7 | inCR | `False` | `True` |
| P7 | reject | `False` | `True` |
| P9 | pValue | `0.0081` | `0.0214` |
| P9 | pValueExpr | `P(X \geq 10) closest tail prob for x=9 region` | `P(X \geq 9) = 0.0214` |
| P11 | given P(X ≥ 20) | `0.0211` | `0.0213` |
| P11 | pValue | `0.0374` | `0.063` |
| P11 | pValueExpr | `P(X \geq 19) — nearest tail` | `P(X \geq 18) = 0.0630` |

The explanations rewritten on the discrete items above now wrap their prose in `\text{}`. KaTeX
renders these strings in maths mode, where a bare "and" loses its spaces:

| Item | Rewritten explanation (shown after a wrong critical-region answer) |
|---|---|
| B6 | `\text{Lower: } P(X \leq 6) = 0.0203 < 0.05 \text{ and } P(X \leq 7) = 0.0576 > 0.05 \text{. Upper: } P(X \geq 15) = 0.0328 < 0.05 \text{ and } P(X \geq 14) = 0.0942 > 0.05` |
| B8 | `P(X \geq 15) = 0.0093 < 0.01 \text{ and } P(X \geq 14) = 0.0255 > 0.01` |
| B9 | `\text{Lower: } P(X \leq 4) = 0.0189 < 0.025 \text{ and } P(X \leq 5) = 0.0553 > 0.025 \text{. Upper: } P(X \geq 14) = 0.0214 < 0.025 \text{ and } P(X \geq 13) = 0.0580 > 0.025` |
| B11 | `\text{Lower: } P(X \leq 0) = 0.2146 > 0.005 \text{, so there is no lower critical region. Upper: } P(X \geq 6) = 0.0033 < 0.005 \text{ and } P(X \geq 5) = 0.0156 > 0.005` |
| P3 | `\text{Lower: } P(X \leq 0) = 0.0498 > 0.025 \text{, so there is no lower critical region. Upper: } P(X \geq 8) = 0.0119 < 0.025 \text{ and } P(X \geq 7) = 0.0335 > 0.025` |
| P5 | `P(X \geq 22) = 0.0061 < 0.01 \text{ and } P(X \geq 21) = 0.0116 > 0.01` |
| P6 | `\text{Lower: } P(X \leq 4) = 0.0293 < 0.05 \text{ and } P(X \leq 5) = 0.0671 > 0.05 \text{. Upper: } P(X \geq 16) = 0.0487 < 0.05 \text{ and } P(X \geq 15) = 0.0835 > 0.05` |
| P7 | `P(X \leq 9) = 0.0433 < 0.05 \text{ and } P(X \leq 10) = 0.0774 > 0.05` |
| P11 | `\text{Lower: } P(X \leq 5) = 0.0203 < 0.025 \text{ and } P(X \leq 6) = 0.0458 > 0.025 \text{. Upper: } P(X \geq 20) = 0.0213 < 0.025 \text{ and } P(X \geq 19) = 0.0374 > 0.025` |

Also corrected: **N3** `zStat` 1.8788 → 1.8783 (`zStatExact` stays '1.88'); **C5** `criticalValue`
0.5029 → 0.5052; and the five `CORR_CV` cells in the booklet table above.

## For Jon's review — the 24 generated p-values and explanations (ruling 1)

*The six two-tailed correlation rows show the two-sided p-value, per the wording ruling at the end of this doc.*

Every one of these comes from `normal_fields()` / `corr_fields()` in the verifier, and the verifier
now requires the game's text to match exactly. So if you reword one, change the template there too.

- **pValue** is what the student types in the p-value route. It is marked within ±0.006, which
  is the existing tolerance, unchanged.
- **Normal:** the tail probability comes from the exact z (not z rounded to 2 d.p.) and is written
  as P(X̄ ≤ x̄) so that it is exact.
- **Correlation:** P(R ≥ r) under ρ = 0, from the exact distribution of r (checked against a
  separate mpmath integration: they agree to 8 significant figures).
- **On two-tailed items** the value is the probability in the tail on the observed side, and Step
  4 compares it with half the level (ruling 2).
- **crExplanation** is the hint shown after a wrong critical-region answer.

| Item | pValue | pValueExpr | crExplanation (generated) |
|---|---|---|---|
| N1 | 0.0228 | `P(\bar{X} \leq 496) = 0.0228` | `P(Z \leq -1.6449) = 0.05 \text{, so the critical region is } Z \leq -1.6449` |
| N2 | 0.0144 | `P(\bar{X} \geq 65.5) = 0.0144` | `P(Z \geq 1.6449) = 0.05 \text{, so the critical region is } Z \geq 1.6449` |
| N3 | 0.0302 | `P(\bar{X} \geq 332.1) = 0.0302` | `P(Z \geq 1.9600) = 0.025 \text{ in each tail, so the critical region is } \|Z\| \geq 1.9600` |
| N4 | 0.0013 | `P(\bar{X} \leq 49.4) = 0.0013` | `P(Z \leq -2.3263) = 0.01 \text{, so the critical region is } Z \leq -2.3263` |
| N5 | 0.0112 | `P(\bar{X} \geq 3.45) = 0.0112` | `P(Z \geq 2.5758) = 0.005 \text{ in each tail, so the critical region is } \|Z\| \geq 2.5758` |
| N6 | 0.0098 | `P(\bar{X} \geq 207) = 0.0098` | `P(Z \geq 2.3263) = 0.01 \text{, so the critical region is } Z \geq 2.3263` |
| N7 | 0.0569 | `P(\bar{X} \leq 747.5) = 0.0569` | `P(Z \leq -1.2816) = 0.10 \text{, so the critical region is } Z \leq -1.2816` |
| N8 | 0.0401 | `P(\bar{X} \geq 48.5) = 0.0401` | `P(Z \geq 1.6449) = 0.05 \text{ in each tail, so the critical region is } \|Z\| \geq 1.6449` |
| N9 | 0.0359 | `P(\bar{X} \leq 271) = 0.0359` | `P(Z \leq -1.6449) = 0.05 \text{, so the critical region is } Z \leq -1.6449` |
| N10 | 0.0228 | `P(\bar{X} \geq 100.2) = 0.0228` | `P(Z \geq 1.9600) = 0.025 \text{ in each tail, so the critical region is } \|Z\| \geq 1.9600` |
| N11 | 0.0221 | `P(\bar{X} \leq 43.2) = 0.0221` | `P(Z \leq -1.6449) = 0.05 \text{, so the critical region is } Z \leq -1.6449` |
| N12 | 0.0082 | `P(\bar{X} \leq 26800) = 0.0082` | `P(Z \geq 2.5758) = 0.005 \text{ in each tail, so the critical region is } \|Z\| \geq 2.5758` |
| C1 | 0.0234 | `P(\|R\| \geq 0.58) = 0.0234` | `n = 15,\ 5\% \text{ two-tailed: critical value } 0.5140 \text{, so the critical region is } \|r\| \geq 0.5140` |
| C2 | 0.0363 | `P(R \geq 0.41) = 0.0363` | `n = 20,\ 5\% \text{ one-tailed: critical value } 0.3783 \text{, so the critical region is } r \geq 0.3783` |
| C3 | 0.0831 | `P(\|R\| \geq 0.52) = 0.0831` | `n = 12,\ 5\% \text{ two-tailed: critical value } 0.5760 \text{, so the critical region is } \|r\| \geq 0.5760` |
| C4 | 0.0173 | `P(R \leq -0.5) = 0.0173` | `n = 18,\ 5\% \text{ one-tailed: critical value } 0.4000 \text{, so the critical region is } r \leq -0.4000` |
| C5 | 0.0152 | `P(\|R\| \geq 0.48) = 0.0152` | `n = 25,\ 1\% \text{ two-tailed: critical value } 0.5052 \text{, so the critical region is } \|r\| \geq 0.5052` |
| C6 | 0.0053 | `P(R \geq 0.46) = 0.0053` | `n = 30,\ 1\% \text{ one-tailed: critical value } 0.4226 \text{, so the critical region is } r \geq 0.4226` |
| C7 | 0.0667 | `P(\|R\| \geq 0.6) = 0.0667` | `n = 10,\ 10\% \text{ two-tailed: critical value } 0.5494 \text{, so the critical region is } \|r\| \geq 0.5494` |
| C8 | 0.0753 | `P(R \leq -0.39) = 0.0753` | `n = 15,\ 5\% \text{ one-tailed: critical value } 0.4409 \text{, so the critical region is } r \leq -0.4409` |
| C9 | 0.0413 | `P(\|R\| \geq 0.46) = 0.0413` | `n = 20,\ 5\% \text{ two-tailed: critical value } 0.4438 \text{, so the critical region is } \|r\| \geq 0.4438` |
| C10 | 0.0320 | `P(R \geq 0.55) = 0.0320` | `n = 12,\ 5\% \text{ one-tailed: critical value } 0.4973 \text{, so the critical region is } r \geq 0.4973` |
| C11 | 0.0061 | `P(\|R\| \geq 0.62) = 0.0061` | `n = 18,\ 1\% \text{ two-tailed: critical value } 0.5897 \text{, so the critical region is } \|r\| \geq 0.5897` |
| C12 | 0.0160 | `P(R \leq -0.43) = 0.0160` | `n = 25,\ 1\% \text{ one-tailed: critical value } 0.4622 \text{, so the critical region is } r \leq -0.4622` |

**RESOLVED in the follow-up below: the question now gives the value.** **One thing to challenge in ruling 1: correlation p-values.** A student has no way to reach these 12
numbers with what the game gives them. The PMCC table gives critical values, not tail
probabilities, and neither AQA/Edexcel booklets nor a standard scientific calculator will give
P(R ≥ r). In the exam a PMCC p-value is always *given in the question*. As built, the p-value route
on a correlation item asks for a number the student can only find with software. The two
alternatives are to show the p-value in the scenario (as the exam does) and ask only for the
comparison, or to hide the p-value route on correlation items. Either is a change to the flow, so
it is not done here.

## Code changes (all in `games/test-the-claim/index.html`)

| Step | Change | Ruling |
|---|---|---|
| 3 | **Discrete two-tailed:** a blank Lower box counts as "no lower critical region" (the bank's `-1`), and the label reads "Lower boundary (leave blank if there is none)" on *every* discrete two-tailed item, so it never hints at the answer | 8 |
| 3 | **p-value route, two-tailed items:** the instruction and label say "probability in the tail" instead of "p-value". **This is a judgement call, flagged for review:** ruling 2 named Step 4, but Step 3 is where the number is asked for, and leaving it labelled "p-value" would make the label wrong one step earlier. Text only; the input and its marking are unchanged | 2 |
| 4 | **p-value route, two-tailed items:** "The probability in the tail is (not) less than half the significance level (2.5% / 0.5% / 5%)". One-tailed items are unchanged | 2 |
| 6 | "Action": `q._compBCorrect = 1` (…support the claim that…) for every item | 7 |
| 6 | "Conclusion in context" is assembled with `MaffsOptions.build()` (`options.js` is now loaded) | 3 |
| 6 | `generateWrongContexts()`: when the direction-word swap leaves the context unchanged, it falls back to the misconception "the claimed proportion / rate / mean has been proved correct" (failing to reject H₀ proves nothing) | 3 |

Nothing else in the flow, scoring, levels or analytics was touched.

## Verification

| Check | Result |
|---|---|
| `verify-test-the-claim.py` on the corrected bank | **PASS**: 0 FAIL, 7 WARN (the seven calculator-line items). Self-test: 18/18 injected faults caught |
| Contract fault injection, on copies of the corrected page | a critical value (P1 3 → 4): `FAIL [KEY] P1 crBoundary: stated 4, computed 3`. A probability (B1 P(X≤0) 0.0352 → 0.0353): `FAIL [PROBABILITY] B1 givenCDF P(X \leq 0): stated '0.0353', computed '0.0352'`. A verdict (P2 inCR/reject → false): caught six ways — inCR, reject, the p-value comparison, Step 4 in both routes, and Step 6 evidence. The page itself was never modified |
| Booklet Table 8 vs exact computation | 260 / 260 cells agree |
| KaTeX 0.16.9 (the game's version), `throwOnError: true` | all 185 explanation, hint, probability and critical-region strings render |
| `check-site.py` tiers 1 + 2 | **348 PASS, 0 FAIL, 0 WARN**. No unlisted loops in 139 files. 0 escaped writes |
| `check-site.py --tier 3 --only test-the-claim` | 3 UNSUPPORTED, 0 FAIL (tier 3 cannot drive this game's dropdowns; acceptable per the contract) |
| Hand-driven play in headless Chromium, because tier 3 cannot drive the game | 31 / 31: P3 blank-lower accepted and the old (0, 8) rejected; B6 corrected region accepted and a blank lower rejected; B3 Step 3 and 4 wording, its tail probability 0.0409 accepted, the Step 4 key "not less than"; B1 still says p-value; N1, N3, C1 and C12 p-values accepted and their explanations shown (no "undefined"); B2, P7, B8, B10, B12 and P8 at Step 6: the correct conclusion shown exactly once in 4, and the right sentence scores "Perfect conclusion!"; no page errors |
| `extract-banks.py` + `check-banks.py --ci` | the P3 duplicate-key entry (B8, `test-the-claim::line526`) is fixed. The ledger's test-the-claim entry was rewritten; that was its only change. After it: "OK - matches the ledger exactly" |
| `check-leaderboard-coverage.js` | OK |

**How the local runs were done.** The sandbox's egress policy blocks `cdn.jsdelivr.net`,
`www.gstatic.com` and the exam-board sites. Tiers 1–3, extraction and the play-through were therefore
run through a scratch wrapper, never committed, that served npm copies of the same versions
(`katex@0.16.9`, `firebase@10.8.0`) and an empty Google Fonts stylesheet. CI reaches the real CDNs,
so it is the authoritative run.

## Class check — other games with hard-coded distribution values (report only)

No other game shares data or code with Test the Claim, so the STOP IF did not fire. The list is
to-do §1.26:

| Game | What is hard-coded | Items |
|---|---|---|
| `normal-navigator` | Normal probabilities and z-scores from μ, σ | 46 items, 29 of them with a probability to 3–4 d.p. |
| `regression-rumble` | PMCC critical values (`cv`, all 5% two-tailed), and r stated alongside Σx, Σy, Σx², Σy², Σxy | 28 scenarios with `cv`; 14 of them also state r next to its sums |
| `core-maths-paper2a` | Normal probabilities and z critical values (§3.5 Normal, §3.6 confidence intervals) | 7 of the 18 items in §3.5–3.6 |
| `maths-court` | one binomial hypothesis test, B(20, 0.5), P(X ≥ 15) = 0.0207 (`:575`) | 1 item. Spot-checked correct: it is the same value B2 verifies |

Searched and excluded on reading, because the matches are coincidences:
- `higher-power`: π²/6 ≈ 1.6449;
- `curling-friction`: a 1.96 N force;
- `core-maths-paper2c`: ln 1.4 ≈ 0.3365.

Also excluded, because they hold discrete or conditional probabilities with no named distribution:
`expectation-station`, `core-maths-paper2b`, `given-that` and `probability-paradox`. And
`terrible-advice`, `spot-the-muppet` and `wrong-on-the-internet` state the 68–95 rule in prose only.

## Found but not fixed (outside this contract)

- **FIXED in the follow-up below.** **Step 6's "Action" is now always the second option.** Neither the "Evidence" nor the "Action"
  dropdown is shuffled, so a student can learn the position. Before this fix it was just as learnable,
  because it copied the Evidence answer. Shuffling both is a small change to step 6.
- **The explanations on the 15 discrete items that were not rewritten** still use bare words in maths
  mode, which KaTeX runs together: B1 renders "…< 0.05andP(X≤1)…" and B3 "Lower:P(X≤10)=0.0139<0.025.Upper:…".
  B7 misses this because it looks for two or more adjacent words, and these are single words.
  Items: B1–B5, B7, B10, B12, P1, P2, P4, P8–P10, P12 (the explanations only; their numbers verify).
- **The first wrong conclusion is often ungrammatical**, for example "the defect rate has changed
  significantly below 20%" and "the mean fill weight has equals the claimed value below 500g". The
  direction-word swap is text surgery. It is now safe, because it can no longer echo the answer,
  but it is not good English.
- **Step 4's wrong-answer hint** talks about "the critical region" even on the p-value route.
- **The p-value tolerance** is ±0.006 while the label asks for 4 d.p.
- **Correlation, lower-tail items:** Step 3 accepts only the positive critical value, so a student who
  types −0.4000 for C4 is marked wrong.
- **`serve-stubbed.py`** checks its port with a plain `bind` (no `SO_REUSEADDR`). Within about 60 s of
  a previous run, while the port is still in `TIME_WAIT`, it reports "already in use" and exits. It
  only bites back-to-back local runs; CI runs once.
- **`check-banks.py --write-ledger`** records `line` numbers one off from the committed ledger in five
  games this change never touched. The field is not part of the comparison key, so CI is unaffected.
  Those entries were left as they were.

## Follow-up, 30 Sep 2026 (later): Step 6 shuffled, correlation p-value given

**Step 6.** Class check: all three Step 6 lists are built in one place, `buildStep6`. Ruling 3's
`MaffsOptions.build()` did not shuffle Evidence or Action because it was applied to the context list
only. Those two were passed to `buildRenderedSelect` as fixed literal arrays with a fixed key
index. Now all three lists go through `MaffsOptions.build()`, and each key is the correct option's
index in the built list.

**Correlation p-value.** Ruling 1 asked students to produce P(R ≥ r), which they cannot find. The
scenario template (`buildScenario`) now adds one sentence on every correlation item, built from the
item's verified `pValue` at 4 d.p.:
- one-tailed items: "The p-value for this test is 0.0363.";
- two-tailed items: "The probability in the tail for this test is 0.0117.".

That wording followed ruling 2. **Superseded the same day by the wording ruling below:** two-tailed
correlation items now give the two-sided p-value.

Step 3's p-value route on correlation items now shows the given value and a **Continue** button in
place of an input: there is nothing to calculate, and Step 4 is the comparison. The other three modes
are unchanged.

**The verifier now also asserts:**
- every Step 6 list, loaded 20 times per item with a seeded random, shows its correct option exactly
  once, keyed consistently, in more than one position;
- every correlation scenario contains its sentence, with the p-value recomputed from the exact
  distribution of r;
- Step 3's p-value route shows the given p-value and has no input.

**Evidence:**
- **Verifier:** PASS. The self-test catches 20/20 faults, including a code-level injection of an
  unshuffled options builder (144 position FAILs, 48 items × 3 lists) and a wrong scenario p-value.
- **The previous build fails the new checks exactly where expected:** Evidence and Action positions
  are constant on all 48 items; the scenario p-value and the Step 3 route fail on all 12 correlation
  items.
- **Site checks:** tiers 1 + 2 give 348/348 PASS. Tier 3 `--only test-the-claim` gives 3
  UNSUPPORTED, 0 FAIL.
- **Headless play-through:** 18/18, twice.
  - All 12 correlation items: the scenario sentence is present, Step 3 continues without an input,
    and Step 4's correct comparison scores "Correct comparison.".
  - A wrong comparison is marked wrong.
  - B2, P1, N3 and C8 over 20 loads each: Evidence and Action in positions 0 and 1, context in 0–3;
    the right sentence scores "Perfect conclusion!".

**The `--live` check could not be run from the cloud sandbox:** its egress policy denies
`maffsgames.co.uk`. See to-do §1.14.

## Wording ruling, 30 Sep 2026 (Jon): "p-value" is two-sided, "probability in the tail" is one tail

**The ruling.** A "p-value" is always two-sided on a two-tailed test and is compared with the FULL
significance level. A "probability in the tail" is always one tail and is compared with HALF of it.
- **Correlation, two-tailed items:** the scenario now states the two-sided p-value, as an exam would:
  "The p-value for this test is 0.0234". It is compared with the full level.
- **Correlation, one-tailed items:** unchanged.
- **Binomial, Poisson and Normal:** unchanged. Two-tailed items keep "probability in the tail",
  compared with half the level.

**How it is built.** One function, `pRoute(q)` in the game, decides both the name and the comparison
level. The scenario sentence, Step 3 and Step 4 all read it, so they cannot drift apart. The
verifier's `tail_only(q)` states the same rule, and `corr_tail(q)` now returns the two-sided
P(|R| ≥ |r|) on two-tailed items.

**The six values changed.** Each is recomputed exactly from the null distribution of r, not by
doubling the rounded tail value. The difference shows on C9: 2 × 0.0206 would be 0.0412, but the
exact two-sided value is 0.0413.

| Item | level | before (one tail) | now (two-sided p-value) | decision |
|---|---|---|---|---|
| C1 | 5% | 0.0117 | 0.0234 | reject (unchanged) |
| C3 | 5% | 0.0416 | 0.0831 | do not reject (unchanged) |
| C5 | 1% | 0.0076 | 0.0152 | do not reject (unchanged) |
| C7 | 10% | 0.0333 | 0.0667 | reject (unchanged) |
| C9 | 5% | 0.0206 | 0.0413 | reject (unchanged) |
| C11 | 1% | 0.0030 | 0.0061 | reject (unchanged) |

**STOP IF not triggered: no decision changed.** Doubling p and doubling the comparison level are
equivalent, and the verifier confirms it on the exact values. Its p-value comparison check and every
Step 4 key pass, and no `inCR` or `reject` field changed.

**Evidence:**
- **Verifier:** PASS; the self-test catches 20/20 faults.
- **Site checks:** tiers 1 + 2 give 348/348 PASS.
- **`check-banks --ci`:** matches the ledger.
- **Headless play-through:** 18/18. All 12 correlation items say "The p-value for this test is …".
  Each Step 4 marks "The p-value is (not) less than the significance level (α%)" right against the full
  level; a wrong comparison is marked wrong; Step 6 positions vary.
- **The Continue button is kept.**
