# SWEEP-1 rulings, 13 Oct 2026 (contract SWEEP-1-RULINGS): the two documents Jon pasted

Saved verbatim in the claim commit (cloud handover, "Contracts"). Part A is Project Claude's pre-triage, approved in
full by Jon on 13 Oct 2026 at 20:35 (Parts 1, 2 and 3). Part B is the wording Project Claude drafted for the items it
undertook to draft. Nothing below is edited.

---

## Part A: the triage

SWEEP-1: pre-triage of the 181 findings for Jon's rulings (13 Oct 2026)
Source: closing section of `docs/audits/sweep-1-2026-10.md` (main, 13 Oct). Prepared by Project Claude; nothing here is ruled until Jon says so. Each game was tagged with its lowest roster level and whether it sits in the Essentials section.
Shape of the 181:

* Severity: 5 HIGH, 56 MEDIUM, 120 LOW.
* Lowest level served: Year 6 15, KS3 53, GCSE 63, Core 13, A-Level 21, Level 4 16.
* Essentials: 52 of the 181 are in Essentials games.

How to rule:

* Part 1, standing rules: ten rules. Approving a rule lets the cloud lane apply it without coming back. They cover about 160 findings.
* Part 2, individual rulings: 18 items that change a key, a context or a convention, ordered by audience then severity. Each has my proposal.
* Part 3, deferred: items that wait.

Part 1: proposed standing rules
R1. Wording. The cloud lane fixes wording, plurals, British usage and notation without asking, provided the fix changes no key, no context and no convention.

* Covers about 50 of the 60 "wording" findings.
* Examples: "1 lives", "1 full groups", cosec for csc, "picture card" for "face card", italic "cm" inside a root, Unicode and ASCII fractions mixed in one option set, "What is Mean?".
* The exceptions are in Part 2.

R2. State the convention (SR-17 applied library-wide). Where a key rests on an assumption the student is never told, the stem or the start screen states it. The key does not change.

* Covers the 27 "convention-unstated" and 5 "unstated-convention" findings, apart from three in Part 2.
* Examples: fair six-sided dice and fair coins (probability-pioneer, terrible-advice), + and − worked left to right (equatle), which number in a payoff cell is yours (prisoners-dilemma), the chessboard doubling rule (higher-power), the definition of a hectare (unit-converter), divisors that must be non-zero (formula-forge).

R3. Make on-screen text true. A statement on screen that is false or contradicts the game is corrected to the nearest true wording. This rule never changes a key: if the true wording would change one, the item comes to Jon.

* Covers most of the 38 "text-contradicts-content" findings.
* Examples: "eight reasons" where the game has nine, "all seven circle theorems", "20,000 alarm events", "It comes back in a few questions", the topic label taken from the hole number.

R4. Money is shown to the penny, from unrounded values.

* Covers split-it-002 and stat-attack-004, both in Essentials.
* Wrong pence on screen are wrong maths to a resit student.
* Class check: two games already show the same shape. The fix should be one rule that every money string uses `toFixed(2)` on the exact value, with a check over the extracted banks. Patching the two games alone would leave the class open.

R5. True distractors are replaced by named errors (SR-4). A wrong option that is true as written is replaced by one that names a real error.

* Covers wrong-on-the-internet-004, factor-theorem-003, gradient-hunter-003 and spot-the-error-003.
* word-problem-decoder-003 and modular-battle-002 also fall here; see the note in Part 3.

R6. SR-14 content is removed.

* bearing-blitz-001: "Fire or die" becomes "Fire before they do".
* spot-the-muppet-002: the "No Relation to the Clown" title is retitled.
* expected-damage-003: the "welcome the trolley" people are reworded.
* probability-paradox-005: the fatal-outcome item is replaced by a non-fatal one.
* maths-court-006: the "planet will end" joke is removed.

R7. Games follow the timer policy. A game listed under Hidden Count-Up hides its running Time from the HUD.

* Covers 6 findings: circle-theorem-spotter, dimension-checker, growth-and-decay, matrix-crunch, scale-factor-scaling, surd-simplifier.
* characteristic-quest-004 is added to the policy's Hidden Count-Up list and hidden the same way.
* Why the game changes, not the policy: a visible clock is exactly what a maths-anxious student does not need, so the policy is right and the games are wrong.

R8. Rendering bugs are fixed without asking. Raw TeX on screen, maths rendered in prose mode, and drawings off the canvas.

* Covers sequence-solver-002 and -003, formula-unlocked-002, proportion-blaster-002 and trig-wars-002.

R9. Marking follows canon.

* chart-interrogator-001: tolerance becomes a band read from the scale (canon §7.1.2).
* chart-interrogator-005: a reading from either a polygon or a curve is accepted within the band.
* proof-builder-002: every valid order is accepted (SR-24).
* proof-builder-005 and -010: the "actually TRUE" option appears on every counter-example item, and distractors show their results like the key does.

R10. The logged level is the resolved level (home lane; architectural).

* eigenvector-engine-004 hard-codes `level: 'further'` and normal-navigator-007 hard-codes `'alevel'` in every event.
* Class check: same shape in two games, and it corrupts every level-based analytics report. The fix is that every `mfg` event takes its level from `MaffsLevel.resolve`, with a check that fails on a literal level string anywhere in a game.
* normal-navigator's untagged calculator is a separate tagging decision for Jon.

Part 2: individual rulings, resit-facing first
Each item has my proposal. If you agree with all of them, "approve Part 2" will do; otherwise strike or amend by number.
Year 6, KS3 and Essentials

1. new-shapes-001 (M, Year 6, Essentials). On every parallelogram the h label sits on the slanted side, not the dashed height. That teaches the exact misconception, slant side for perpendicular height, that costs resit marks.
   * Proposal: draw h on the dashed perpendicular. Raise it to HIGH.
2. prime-factorisation-001 (L, Essentials). The feedback says "p is not a factor of N" when p is a factor of N but not of what is left. That is a false mathematical statement to a KS3 student.
   * Proposal: "p doesn't go into what's left (r)". Raise it to MEDIUM.
3. maths-court-004 (H, KS3). Brenda reaches 54 by "division before multiplication", a false rule, and is keyed correct.
   * Proposal: key her wrong, since the right answer comes from a wrong reason, consistent with mc_ks3_002.
   * Class: the court never says what it judges. Add to the start screen: "The court judges the reasoning, not just the answer." That also settles maths-court-006's "one correct answer" line: the GCSE cases with two or three right arguments then say so.
4. spot-the-error-001 (H, KS3). The explanation names the 80 trials as the missed fact, but "replaces it 80 times" is keyed wrong, and the "+ 4" is never explained.
   * Proposal: move the Stage 2 key to "replaces it 80 times", and rewrite step 2 so that the stray 4 is the visible error.
5. fermi-lab-001 (H, KS3). The question asks for distance travelled by buses, but the chain computes distance travelled by students.
   * Proposal: reword the stem to "the total distance travelled by students on school buses". The key is unchanged and no new number is needed.
6. fermi-lab-003 (filed L; really a wrong key). piano-tuners-london is keyed 140, but its own chain gives 82.
   * Proposal: the key follows the chain (82). The verifier pins chain and key together.
7. 52dle-001 (M, KS3). "My divisors (1,2,4,7,14) sum to me" is false.
   * Proposal: "My proper divisors (1, 2, 4, 7, 14) sum to me", which is the definition of a perfect number.
8. 52dle-002 (M, KS3). The clue states a curiosity that doesn't exist.
   * Proposal: replace it with a true clue. I'll draft it from the puzzle's number on your yes.
9. wrong-on-the-internet-003 (M, KS3). 1000 × 1.05 × 20 is 21,000, not 21,050.
   * Proposal: use £21,000 throughout. The poster's error, multiplying by 20 instead of compounding, stays intact.
10. expected-damage-002 (M, Essentials). "Optimal play would have hit N" comes from a random roll, so a student who chose correctly can be told they did worse than optimal.
   * Proposal: compare the student's expected values with the optimum, not with a roll.
11. correlation-or-coincidence-003 and -004 (Essentials). Both keys are arguable because a confounder is plausible.
   * Proposal: change the contexts rather than the keys. Revision becomes one student across several tests. The fridge magnets are replaced by a pair with no shared driver.
   * I'll draft both on your yes.
12. better-value-002 (M, Essentials). Break-even is keyed one way in gcse_019 and the other way in gcse_020.
   * Proposal: one convention, "worth it" means strictly cheaper, stated in the stem (R2), with gcse_019 re-keyed to match.
13. word-problem-decoder-004 (M, KS3). KS3 has no Probability topic, so a probability question is keyed "Statistics & Averages".
   * Proposal: add Probability to KS3's topic list.

GCSE, Core and above

14. graph-sketcher-006 (H). This entry bundles four items:
   * L4_5 has two maxima on the closed interval. Proposal: ask for "the turning point".
   * CM2's key is false and no option is true. Proposal: replace the key with a true limitation; I'll draft it.
   * CM11. Proposal: accept "Reliable" as well as the current key.
   * CM4. Proposal: correct the key text.
15. test-the-claim-007 (M). 14/22 is already more than half of the whole class.
   * Proposal: new context: "A head teacher believes more than half of the county's Year 11 will pass. In a sample of 22, 14 pass."
16. growth-and-decay-003, -004 and -007 (M).
   * Pressure "decreasing" with depth is false. Proposal: use light intensity falling with depth, which is genuinely exponential.
   * A hardness of 3,610 HV is not physical. Proposal: new context, which I'll draft.
   * Fractional device counts. Proposal: key "the least n" as the integer.
17. suvat-005 (L). "A table 5 m high". Proposal: "a wall 5 m high".
18. normal-navigator-002 (M). A minimum or pass mark is rounded to nearest.
   * Proposal: a minimum always rounds up, stated in the stem (R2), re-keyed where needed.

Part 3: deferred, with reasons

* Degenerate and duplicate items (8): characteristic-quest-003, circle-theorem-spotter-004, correlation-or-coincidence-002, differentiation-duel-001, eigenvalue-extractor-002, factor-theorem-005, split-it-004, truth-will-set-you-free-007.
   * These need new items. That is bank-depth work, priority 4, and I'd draft them in a later content pass.
   * Exception: split-it-004 is a generator fault in an Essentials game, where it asks for the amount it has just given. Fix it under R3 now.
* modular-battle-002 and word-problem-decoder-003: the distractors are not named errors, by design of the game.
   * Proposal: accept them as they are, with a reason recorded. SR-4 fits multiple-choice items with authored distractors, not a remainder drill or topic overlaps.
* standard-form-blitz-004 and normal-navigator's calculator tag: these are calculator tags (canon §4.4). Tagging is its own decision, best taken game by game.
* linear-equation-solver-001: on 227 of 295 lines the ask doesn't match the options. That is a redesign of the ask, not wording. It sits in an Essentials game, so I'd draft the new ask for your review as a next step.
* proportion-blaster-003: a wrong answer shows no working.
   * Class: this is probably not one game. I'd ask the cloud lane to count how many games show only the key after a wrong answer before we rule. For a struggling student, the working is the whole point.

Process points

1. Bundled entries hide severity. Several entries carry a wrong key inside a LOW "wording" finding: fermi-lab-003's key is 140 where the chain gives 82, and maths-court-006 has wrong arithmetic in gcse_015's summary.
   * Severity was set by the entry's first item, so wrong maths can sit at LOW. Proposal: amend the reviewer brief to one defect per entry, each with its own severity, and split the bundled entries before rulings are applied.
2. The class labels need tidying. "convention-unstated" and "unstated-convention" are the same class, and one class is labelled "5".
3. core-maths-paper1-006 is part-stale. #357 fixed its histogram half, but the entry is still open for Q19's £318.55.

---

## Part B: the content document

SWEEP-1 rulings, 13 Oct 2026: wording drafted by Project Claude for items Jon approved
Jon approved the whole triage (`claude/sweep-1-triage-2026-10-13.md`: Parts 1, 2 and 3) on 13 Oct 2026 at 20:35. The items below are the ones I undertook to draft. Every key value is unchanged unless stated, and every figure was checked against the game's own code on main.
52dle-s1-002 (puzzle 18, a = 23, `games/52dle/index.html` ~701)

* clue: "I am the 9th prime. I am also the smallest number of people needed for a better than even chance that two of them share a birthday."
* Hints are unchanged.
* [check: P(shared birthday, 23 people) = 0.507 > 0.5; for 22 people it is 0.476 < 0.5]

correlation-or-coincidence-s1-003 (A19)

* x: "Hours one student revised for each of 12 tests". y: "Their score on that test (out of 50)". cat 'cause', ranges, direction, strength and n are unchanged.
* explain: "For one student, more revision means a better score. Other things change from test to test, such as the topic and how hard it is, which is why the pattern is only moderate."
* Using one student removes prior attainment as a confounder.

correlation-or-coincidence-s1-004 (C26)

* x: "House number (8 families)", range 1 to 120, integers. y is unchanged.
* joke: "Families at the far end of the street live further from the cinema, so naturally they stay in and rewatch the same film. Obviously."
* explain: "With only 8 families, a pattern can appear by chance. A house number can't press play."

graph-sketcher-s1-006

* L4_5: the ask becomes "the turning point" in place of "maximum deflection". The key is unchanged.
* CM2 limitation MCQ:
   * correct: "The model predicts profit keeps rising without limit as x increases"
   * wrong: "The model predicts a loss when x = 3", "The model is linear", "x cannot be a whole number"
   * [check: P = x(x − 3)² ≥ 0, with P = 0 at x = 3 (zero profit, not a loss), and P → ∞ as x → ∞]
* CM11: "Reliable" is accepted as well as the current key.
* CM4: the key text names a limitation of the braking-distance model itself, not reaction time. The cloud lane writes this under R3 from the item's own context and reports the wording in its PR.

growth-and-decay-s1-004 (L4_14). Change the context and variable names only. Every number and key stays.

* modelLatex: "N = ke^{0.022t}"
* context: "The number of bacteria N (thousands) in a culture grows with time t (minutes). Model valid for early growth."
* Graph labels "N (thousands)" and "t (min)". Units "thousand" in place of "HV".
* sq2 correct: "The number of bacteria grows continuously at 2.2% per minute". Wrong options get the same substitution.
* sq1 "when t = 300", key 3610. sq3 "Given N = 400 when t = 200", key 4.91. sq4 "Find t when N = 500", key 210.
* [check: 4.911e^{6.6} = 3,610; doubling time ln2/0.022 = 31.5 min, plausible for bacteria]

growth-and-decay-s1-003 (AL12). Change the context and variable names only. Every number and key stays.

* modelLatex: "I = ke^{-0.046d}"
* context: "In clear sea water, light intensity I (as a fraction of the light at the surface) decreases with depth d (m)."
* Graph labels "I" and "d (m)". No unit in place of "atm".
* sq1 "when d = 30", key 0.252. sq2 correct: "Light intensity decreases continuously at 4.6% per metre of depth", with wrong options substituted the same way. sq3 "Given I = 1 when d = 0", key 1. sq4 "Find d when I = 0.1", key 50.1.
* [check: e^{-1.38} = 0.252; an attenuation coefficient of 0.046 per metre is within the range for clear ocean water]

probability-paradox-s1-005 (Fallacy item)

* scenario: "'Every famous band I know of kept going when things got hard. So if a band never gives up, it will become famous.'"
* The question, options and key (Survivorship bias) are unchanged.
* explain: "We only hear about the bands that made it. Thousands of bands never gave up and still weren't famous, and you never hear about them. The sample is biased."

bearing-blitz-s1-001

* "Fire or die." becomes "Fire first."
* "💀 DESTROYED! Surface ships locked onto your position." becomes "HIT! Surface ships locked onto your position."

spot-the-muppet-s1-002

* Delete "(No Relation to the Clown)".
* Apply the same deletion to the same joke in terrible-advice core_004.
