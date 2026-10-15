CONTRACT: PHRASING-FIX-2 (Project Claude for Jon, 15 Oct 2026, 13:40).
CLOUD LANE. Save verbatim under docs/handover/contracts/.

AUTHORISED BY JON, 15 Oct 13:38: merge #408 (PHRASING-SWEEP report)
before starting. Then this contract.

TASK: Reword the two AMBIGUOUS items from #408 so each has exactly one
reading, and that reading matches its key.

ROOT CAUSE: #408 found two live items whose wording supports two
readings that give different answers:
- probability-pioneer (Year 6): "If two outcomes are equally likely,
  each has probability 0.5" is keyed false. It is true for an
  experiment with only two outcomes.
- wrong-on-the-internet woti_core_007 (Core): asks for the "break-even
  point" (exact crossover 5,000 ÷ 15 = 333.3) but keys 334, the fewest
  whole units sold to stop making a loss. On the exact reading, the
  stage 2 distractor "should not have rounded 333.3 up to 334" is true.

CLASS CHECK: Not a new class. #408 measured the phrasing class and
found it confined to these two items outside Better Value. woti_core_007
is an instance of the existing rounding rule R2 (a minimum rounds up,
stated in the stem). Local fixes, to existing rules.

JON'S RULINGS (15 Oct):
R1 probability-pioneer: the statement becomes "On a fair dice, rolling
   a 1 and rolling a 2 are equally likely, so each has probability
   0.5." Keyed false. Rewrite its explanation to match: equally likely
   outcomes share the probability equally among ALL the outcomes; a
   dice has six, so each is 1/6.
R2 woti_core_007: the ask becomes "What is the fewest units the company
   must sell to stop making a loss?" Key stays 334. The stage 2
   distractor "should not have rounded 333.3 up to 334" stays, and is
   now plainly wrong. Adjust any reply or explanation text that still
   says "break-even point" so it agrees with the new ask.

EXACT CHANGE:
1. Merge #408 on its green Gate, with main green.
2. Apply R1 and R2 to the two items named in #408's report (take the
   exact item ids and line references from that report).
3. Recompute both keys and confirm against the rulings.
4. Reworded items move content ids in data/check-ledger.json: update
   the ledger as CI's Tier 4 layer A directs. Do not hand-edit ids.
5. Run scripts/check-changed.py BEFORE the first push.
6. One PR. Merge on a green Gate with main green (standing rule).
   Watch main's full run on the merge.
7. Handover entry in docs/handover/cloud.md: both items fixed, PR
   number, main's run result.

DO NOT TOUCH:
- Any other item in either game.
- docs/canon.md, CLAUDE.md, docs/todo.md.
- better-value.
- gcse_014, 015, 017, 018 (held for batch 2).
- Shared code (schools/assets/), scripts/, the workflow.

SUCCESS CONDITION:
- Both items read as ruled; each has one reading, matching its key.
- #408 and the fix PR merged; main's full run green after each.
- Handover recorded.

STOP IF:
- Main's latest full run is red.
- Either ruling's wording proves wrong on checking (report it; do not
  reword).
- The probability-pioneer item's id or slot is shared with a
  leaderboard key or GA4 parameter.
- You would need to schedule any task that merges, edits or pushes.
  Self-scheduled tasks may only read CI status and report.

END OF CONTRACT

Jon, 15 Oct 2026 (in session): scripts/verify-probability-pioneer.py's STAGE3_KEYS entry for the R1 statement
may be updated (the one entry only; no logic change).
