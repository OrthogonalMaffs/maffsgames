CONTRACT: PHRASING-SWEEP (Project Claude for Jon, 15 Oct 2026, 13:20).
CLOUD LANE. Read-only audit. Save verbatim under docs/handover/contracts/.

TASK: Find every live question outside Better Value whose wording uses
the switch-point / sufficient-condition phrasing that #407 ruled on, and
report each one against the new canon rule, without changing any game.

ROOT CAUSE: #407 added a canon rule: "becomes / only after N" names the
switch point; "if / worth it when" is a sufficient condition. Better
Value's items were rewritten to it. Nothing has checked whether other
banks use the same phrasing with the same ambiguity, so the defect may
still be live elsewhere.

CLASS CHECK: Yes, a class. It is a wording rule that applies to every
bank, and only one game has been checked against it. This contract
measures the class; the fixes follow under a separate contract once Jon
has ruled. Read-only now, because a wording change needs Jon's rulings
(batch 1 did).

EXACT CHANGE:
1. Read the new rule in docs/canon.md as merged by #407 (83f9a7a).
   Quote it verbatim at the top of the report.
2. Search every live game's bank (data/banks/ and the game files,
   excluding better-value) for: "becomes", "only after", "only when",
   "worth it when", "worth it if", "break-even", "cheaper when",
   "better value when", "after how many", "from how many", and "if"
   inside a question asking for a threshold or count.
3. For each hit, state: game, item id, tier/level, the stem verbatim,
   the key, and one of:
   CLEAR (wording and key agree under the rule),
   AMBIGUOUS (two readings give different keys; give both keys),
   WRONG (the key contradicts the rule).
   Recompute every key you classify. Do not judge from wording alone.
4. Order the report: Essentials and GCSE first, then Core, A-Level,
   L4. Give totals per class.
5. Write the report to docs/audits/phrasing-sweep-2026-10-15.md.
   One PR containing only that file and the cloud.md handover entry.

DO NOT TOUCH:
- Any game file, bank, verifier, ledger or findings file.
- docs/canon.md, CLAUDE.md, docs/todo.md.
- better-value (already done in #407).
- gcse_014, 015, 017, 018 (held for batch 2).

SUCCESS CONDITION:
- The report lists every hit with a recomputed key and a class.
- The PR's Gate is green. Do NOT merge it. Leave it open for Jon.
- docs/handover/cloud.md records: the PR number, the totals, and
  "awaiting Jon's review; not merged".
- Claim released with scripts/end-task.py.

STOP IF:
- Main's latest full run is red.
- A hit is a wrong key on a live Essentials or GCSE game: report it
  to Jon at once, in the session, before continuing.
- More than 40 hits: stop at 40, report the count so far, and ask
  whether to continue.
- You would need to schedule any task that merges, edits or pushes.
  Self-scheduled tasks are allowed only to read CI status and report.

END OF CONTRACT
