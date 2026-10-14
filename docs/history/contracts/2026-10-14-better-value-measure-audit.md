# BETTER-VALUE MEASURE AUDIT (Jon, 14 Oct 2026), verbatim

TASK: Audit every better-value item and propose, for each, a declared measure and a plain-words decision criterion, as a report only, changing nothing.

ROOT CAUSE: better-value items don't state what "better" is measured by. Distractors that are true under another measure get marked wrong: bv_core_019 (fixed, #392), core_007 (true conditional), core_037 (key = ROI, explanation = net profit). core_044, 047 and 048 are keyed on a judgement, not a computed figure.

CLASS CHECK: Yes. Three instances of the same shape in one game, from shared item design. The proposed architectural fix: each scenario states a decision criterion in plain words ("The owner wants the most profit from her budget") without naming the measure, so the student still chooses the measure. Each item declares its measure in data. The verifier computes that measure for every option and fails any distractor true under it. This phase gathers the evidence to confirm or reject that design before any change.

EXACT CHANGE: No change to games/ or scripts/. Write docs/handover/better-value-audit.md containing, for every item in the bank:
- id, level, type, and current scenario (verbatim).
- The measure the key actually relies on (unit cost, day rate, total cost, net profit, ROI, other).
- A proposed criterion sentence for the scenario.
- Whether each conclusion is TRUE, FALSE or JUDGEMENT under that measure, with the arithmetic.
- A flag where the key, the explanation and the measure disagree (as in core_037).
- A flag where no single measure fits the item.
End with: the count of items per measure, the count needing changes, the list of current item fields, and whether the verifier can compute each measure from existing data or needs new fields.

DO NOT TOUCH: Any game file. Any verifier. The option-parity measure. Any other game.

SUCCESS CONDITION: The audit file covers every item in the bank (state the total), each with its arithmetic shown. It is merged as a docs-only PR. The handover in cloud.md points to it.

STOP IF: The bank contains item types where "better" isn't a value comparison at all (report them and continue the rest). The audit finds a key that is outright wrong, not just ambiguous: report it at once in a message, before finishing the audit, since that is a live correctness issue.
