# BV-RULINGS (Jon, 15 Oct 2026), verbatim

TASK: Rewrite the ruled better-value items to Jon's rulings of 15 Oct, with criterion sentences, so their KNOWN entries clear.

ROOT CAUSE: These items have two defensible measures, opposite rulings, no computable measure, a stepped reading, or ambiguous "becomes" wording (docs/handover/better-value-decisions.md).

CLASS CHECK: Yes. This applies the schema/verifier redesign (#405) to its ruled items. Content changes only; the verifier is the architectural layer and already exists.

EXACT CHANGE: games/better-value/index.html, with matching claim data. Each item's explanation is updated to its arithmetic.
- core_031: measure average monthly cost. Criterion "She'll stay for the whole contract and wants the lowest cost per month." C2 rewritten false.
- core_037: measure net profit. Criterion "She wants the most profit from this one print run." Key → "Premium flyers are better value — £860 vs £620 profit". C1 rewritten false.
- core_050: measure including time. Criterion "She would work those 45 minutes at her part-time job if she didn't cook." Key → verdict for buying (£825 vs £1,047.40). C4 → a computed false claim, without "always".
- core_011: add a 3% AER on money kept, with a criterion to count interest. Key unchanged (cash, £549 vs £582.53 net). Explanation states the 9.1% break-even rate.
- core_042: criterion to count interest earned. Key unchanged.
- core_047: add clean duration (windows stay clean 3 of A's 4 weeks, all 6 of B's). Measure cost per clean week (A £3.33, B £2.50). Key B with that figure.
- core_048: add "This year she has a minor accident: £1,200 to repair her own car." Measure total cost this year. Key → "Policy A is better value this year — £730 vs £1,540".
- core_030: ink stated as "works out at 9p a page". Key unchanged.
- core_024 C2, core_026 C4, core_027 C4, core_029 C4: add "only" so each claims the switch point. Remove from KNOWN once reworded.
Add the "becomes/only after = switch point; if/worth it when = sufficient" rule to canon §7.x (better-value content rules).
Distractors that must be rewritten false keep the same misconception, worded as a false computed claim.

DO NOT TOUCH: Any item not listed. The verifier's logic. Option parity measure. gcse_014/015/017/018 (batch 2).

SUCCESS CONDITION: Every listed item's KNOWN entries are removed, and the claims verifier passes. The existing better-value verifier passes and option parity still passes (record the new percentages). Full CI is green. Merged, with cloud.md listing old and new wording per item, and the core_022 audit note corrected.

STOP IF: Any rewritten item's arithmetic disagrees with the figures above. A rewrite pushes option parity past threshold. Any added figure needs to differ from those Jon approved.
