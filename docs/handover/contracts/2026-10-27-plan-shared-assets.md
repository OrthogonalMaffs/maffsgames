# PLAN-SHARED-ASSETS (Jon, 27 Oct 2026), verbatim

TASK: Make Plan pass for PRs that touch shared assets: the per-line 70% limit fails about a dozen verifier lines whenever scripts/bank_common.py changes (home lane #583).
ROOT CAUSE: The per-line limit went into the gate before every long verifier line was moved onto the shard interface. Lines run in the shared Chromium setup (about 107 s each): Answer lock parts 3 and 6, Bearing Blitz, Burst part 1, Equation Builder part 3, Factor Theorem, Squared Squirrel parts 3 and 4, Free Daily Pizza part 1, Growth and Decay, How Many Parts? part 1; Content verifiers 1 at 119% of its budget.
CLASS CHECK: Yes: any PR touching a shared import selects these lines, so it fails every lane's shared-asset PRs. Fix at the shard layer: move each over-limit verifier onto the shared work-unit interface so ci-groups.py splits it from timings. No hand-split --part lines, no raised limit, no per-PR exemption.
EXACT CHANGE: First check whether #578 already covers these. Then migrate each over-limit verifier to the shard interface and rebalance Content verifiers 1. Add a Plan selftest: a no-op change to bank_common.py must select every importer and still pass.
DO NOT TOUCH: The 70% limit and the 189 s per-line limit. Verifier logic and checks. #583's content.
SUCCESS CONDITION: A PR touching bank_common.py passes Plan; main green; the home lane is told to merge main into #583. Handover updated.
STOP IF: A verifier can't be split without changing what it checks: put it on an unmerged branch and report it with its timing. Migrating them all would take more than this session: do the ones #583 selects first, merge, and report what's left.
