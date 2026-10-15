# Contract BV-CRITERIA (Jon, 15 Oct 2026), verbatim

TASK: Add criterion sentences to every better-value item whose criterion is empty, and make the remaining content changes from the audit, so the claims verifier's KNOWN list reaches zero.

ROOT CAUSE: docs/handover/better-value-audit.md found that most items never state what "better" is measured by, and 23 need content changes. Batch 1 (BV-RULINGS) and the core_047 fix cover core_011, 031, 037, 039, 042, 047, 048 and 050. The rest remain in KNOWN in scripts/verify-better-value-claims.py.

CLASS CHECK: Yes. This completes the redesign (#405) for the remaining items. Content only; the verifier is the architectural layer and already exists.

EXACT CHANGE: games/better-value/index.html, with matching criterion/claim data:
1. Every item with criterion '' gets a plain-words criterion sentence, added to the scenario and the criterion field, stating what the person wants and any quantity the key already relies on, without naming the measure. Use the audit's proposed criterion for each item as the starting draft. Items whose scenario already states one (core_021, 024–030, 033, 038, 041, 046, 049, gcse_019, gcse_020) keep it; core_025 adds "worth it means cheaper, not the same price" as gcse_019 does.
2. Content changes, as the audit flags:
   - core_007 C4: a false conditional, using the audit's suggestion ("fewer than 2,500 copies").
   - core_014: criterion states 2 bottles.
   - core_017, gcse_014, gcse_015, gcse_017: the criterion states how much is used.
   - gcse_018: the criterion states a 6-hour stay.
   - core_020 C4, gcse_003 C1, gcse_011 C1: name the measure so each is false under it, or rewrite it false.
   - core_021 C2: "February had better giving".
   - core_023: add the question "Which builder charges more for each hour of work?".
   - core_044: key rewritten as a verdict under usable value, per the audit's suggestion.
   - gcse_007 C4: rewrite so its figure, not just the word "much", makes it false.
3. Each changed item's explanation agrees with its arithmetic. Distractors that need rewriting keep the same misconception, worded as a false computed claim. Right-verdict, wrong-figure distractors stay where the explanation states the correct figure (Jon's ruling).

DO NOT TOUCH: The items covered by batch 1 and core_047. Verifier logic. The option-parity measure. Any key's verdict, except core_044 and core_023 as specified. Any other game.

SUCCESS CONDITION: KNOWN in verify-better-value-claims.py is empty. Both better-value verifiers and option parity pass (record the new percentages). Full CI is green. Merged, with cloud.md listing every changed item's old and new wording, so Jon can sample them.

STOP IF: A criterion sentence would need a number the key doesn't already rely on (that's a new content choice for Jon). Any rewrite changes a key's verdict other than as specified. Option parity fails for the game. More than about 30 items need wording beyond the criterion sentence; report before continuing.
