HOME LANE — ADDENDUM (9 Oct 2026, 19:45). Jon's rulings (19:42).

1. OVERLAY-KEYS (#232) — ESCAPE: leave as is. Do not add Escape handling; Skip stays the way out. The "Escape closes the overlay as now" line in the contract was Project Claude's error (the overlay never handled Escape). Record in the PR description and the handover that Escape-to-close is deferred to a future accessibility pass, because an accidental Escape would discard a leaderboard entry.
2. New item PREPUSH-SCOPE — after the checkpoint, before CAR-TRAP-DRAFT and LIBRARY-DRAFT. Contract below.

---

TASK: Make the local pre-push check fast enough that a lane can run it before every push, without running less than CI would catch for that change.

ROOT CAUSE: Not yet established. On #232 the pre-push script wanted 113 checks and ran past 25 minutes, so the lane skipped most of it and left the per-game verifiers to CI. A safeguard that is too slow to run gets skipped, and then it protects nothing. Two possible causes, which need different fixes: (a) pre-push runs every check regardless of what changed; (b) it already selects by changed files, and a change to a shared asset (the overlay) correctly selects every game, so the cost is in how the checks run (one browser per check, serial execution).

CLASS CHECK: Yes, a class. Pre-push is shared infrastructure that every push from every lane goes through, and its cost affects every future change, not one PR. So the fix belongs in the pre-push script and its runner, not in a per-PR habit of skipping it.

EXACT CHANGE:
1. Measure first. Time pre-push on three cases: a one-game change, a shared-asset change (re-run #232's diff), and a docs-only change. Report the number of checks selected and wall time for each, and which of causes (a) and (b) applies.
2. If (a): make pre-push select checks by the changed files, using the SAME selection logic CI uses (import or call it; do not write a second copy). A shared-asset change must still select every game that loads the asset.
3. If (b), or after (a) still leaves the shared-asset case slow: make the checks cheaper to run without dropping any — run them in parallel workers, and reuse one browser instance across checks where the harness allows. Target: the shared-asset case under 10 minutes locally; state the measured figure.
4. Whatever remains too slow, do not silently skip it: print exactly which checks were deferred to CI and why, and make the lane's PR template line ("checks deferred to CI: …") come from that output.
5. Record the before/after timings in docs/handover/home.md and in CLAUDE.md's CI notes.

DO NOT TOUCH: the CI workflow's own selection or grouping (CI-BALANCE owns it; reuse its logic, don't change it); any check's assertions; the answer-lock parts' content; the pre-commit personal-details hook.

SUCCESS CONDITION: the three measured cases are reported before and after; a one-game change and a docs-only change finish pre-push in a few minutes; the shared-asset case meets the target or prints a clear list of what it deferred to CI; no check that CI would run for a change is dropped without being named.

STOP IF: the only way to hit the target is to run fewer checks than CI selects for the same change; CI's selection logic cannot be reused from the pre-push script without changing it; parallel runs make any check flaky (report which).
