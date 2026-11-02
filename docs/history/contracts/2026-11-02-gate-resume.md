CONTRACT: GATE-RESUME (cloud lane, Mon 2 Nov 2026)
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Now that the infrastructure freeze has ended, land the parked gate work in its recorded order (GATE-WARN-THEN-ENFORCE
step 2, then step 5), then add a warning band to check-context-size.py and bring AGENTS.md under it.

ROOT CAUSE
1. Steps 2 and 5 were built and parked on 27 Oct by Jon's freeze (until Mon 2 Nov); until step 2 merges, every
   gate change has to run the worst-case test by hand (canon §7.8.4).
2. check-context-size.py goes straight from silence to failure at 20 KB, so the cap is found mid-task (ENCODING,
   30 Oct) instead of as planned work. Canon §7.8.4 says limits warn first; this one has no warning stage.
3. AGENTS.md is now loaded by every Codex task, and RULEBOOK will make CLAUDE.md import it, but nothing measures it.

CLASS CHECK
Yes: shared gate infrastructure every PR passes through. Step 2 fixes how all gate changes are tested; step 3 fixes
the checker itself, not any one file's size. Both at the shared layer.

EXACT CHANGE
Read first: docs/handover/cloud.md (27 Oct entry) and docs/handover/contracts/2026-10-27-gate-warn-then-enforce.md.
Step 1 (claude/gate-worst-case, 778d926): merge origin/main into it (resolve conflicts without changing step 2's
  behaviour); run its own worst-case test; check-changed.py; PR; stop for review.
Step 2 (claude/gate-handover-archive, e34a15e): drop the checkpoint handover commit noted in the 27 Oct entry;
  merge origin/main (after step 1 is merged); run the worst-case test (now in CI); PR; stop for review.
Step 3 (new branch claude/context-warn, from main after step 2 merges): scripts/check-context-size.py:
  a. WARN = 18 * 1024. A file over WARN and at or under its limit prints a warning (a GitHub ::warning annotation
     in CI) and passes. Over the limit still fails. DEFERRED behaviour unchanged.
  b. Add AGENTS.md to FILES at the 20 KB limit (4,440 bytes on main today, so it passes from day one: this meets
     §7.8.4's warn-first rule with an empty warn list).
  c. --selftest gains: 18.5 KB warns and passes; LIMIT + 1 fails; 17 KB is silent; AGENTS.md over LIMIT fails.
  d. Update the script's docstring and ci-line, and add one sentence to canon §7.8.4 recording the band.
  PR; stop for review.

DO NOT TOUCH
- LIMIT and TODO_LIMIT values; the DEFERRED mechanism.
- CLAUDE.md, AGENTS.md, docs/agent-workflow.md (the home lane's RULEBOOK contract rewrites these next).
- GATE-WARN-THEN-ENFORCE step 4 (separate session) and the FOLD / KEYPAD-FRACTION queue (after this contract).
- Any game, shared asset or bank.

SUCCESS CONDITION
Each of the three PRs: Gate green, worst-case test passed (by hand for step 1, in CI after it), check-changed.py
with no new failures against the known container set, handover current, then STOP for Project Claude's Shared-tier
review and an explicit "merge" from Jon. This contract overrides the cloud lane's standing merge-on-green
authorisation for these three PRs (gate files are Shared tier). After each merge, watch main's full run and report it.
Contract saved verbatim under docs/handover/contracts/ in the first commit, per the cloud lane's rule.

STOP IF
- Merging main into either parked branch changes what it does, or needs edits outside its own files.
- The worst-case test fails on step 1 or 2.
- Main's latest full run is red when a step is due to start.
- Step 3 would need a file to go into DEFERRED, or any limit value to change.
- The cloud handover or the contracts folder say something about steps 2 or 5 that contradicts this contract
  (report both; Jon decides).
