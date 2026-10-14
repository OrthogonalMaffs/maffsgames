# TRUE-DISTRACTORS (Jon, 14 Oct 2026), verbatim

TASK: Correct the true distractors in better-value bv_core_019 and graph-sketcher CM8, and report any reuse of the same wording elsewhere.

ROOT CAUSE: bv_core_019: the key says "pays better" without naming the measure, so distractor 1 ("Contract B pays more in total — £18,000 vs £11,520") is a true statement a student can reasonably choose. Distractor 4 is a judgement that can't be checked. CM8: for h = 15t − 5t² on [0,3], speed is greatest at the roots (15 m/s at t = 0 and t = 3), so the roots distractor "Times of maximum speed" is true.

CLASS CHECK: Partly. The two corrections are local content errors. Two possible classes exist: (a) better-value conclusions that say "better" without naming the measure, and (b) "Times of maximum speed", or wording close to it, reused as a roots distractor on symmetric projectile items. This task fixes these two items only and reports (a) and (b). The architectural fix is the separate distractor-falsity verifier audit.

EXACT CHANGE: games/better-value/index.html, bv_core_019:
- Key text → 'Contract A has the better day rate — £320/day vs £300/day for Contract B' (correct:true unchanged).
- Conclusion 1 → 'Contract B has the better day rate — £18,000 ÷ 12 = £1,500/day' (correct:false).
- Conclusion 3 unchanged ('They pay the same daily rate').
- Conclusion 4 → 'Contract B has the better day rate — £18,000 ÷ 36 = £500/day' (correct:false).
- Explanation → append: ' Contract B does pay more in total (£18,000 vs £11,520 over 12 weeks), but only because it is 60 days of work against 36. The day rate tells you which pays better for your time.'
games/graph-sketcher/index.html, CM8, roots mcq: replace wrong option 'Times of maximum speed' with 'The time taken to reach maximum height'. Nothing else in CM8 changes.
Then grep both games for (a) and (b), and all games for (b). List the hits in the handover. Do not fix them.

DO NOT TOUCH: Scenario, optionA/optionB details, id, level and type of bv_core_019. CM8's eqLatex, fn, ranges, table, answers, the read question and the limitation question. Any other item. The option-parity measure.

SUCCESS CONDITION: Both games' verifiers pass. The option-parity measure for better-value and graph-sketcher still passes; record the new percentages. Full CI is green. The commit is merged, and the handover lists the grep hits for (a) and (b) for my review.

STOP IF: Either game's verifier pins the old text so it can't simply be updated. Either change pushes a game past the option-parity threshold. The better-value item format can't hold ÷ or the appended explanation without a rendering change. The grep finds the CM8 distractor wording on a projectile item that also starts and ends at ground level; list those, don't fix them.
