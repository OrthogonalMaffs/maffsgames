# Handover: home lane

**Queue (cross-lane facts; never archived)**

- DONE queue: docs/history/handover-home-archive.md

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

- FRACTION-WHOLE: home/Codex, codex/fraction-whole, /home/maffs/mg-fraction-whole; contract docs/handover/contracts/2026-11-04-fraction-whole.md. STOP on unsupported negative fraction answers; no implementation changes.

## 2026-11-04 (home): FRACTION-WHOLE

Agent: Codex. Worktree: /home/maffs/mg-fraction-whole. Branch: codex/fraction-whole. Base: 67610171. Pre-step and its extension completed: seven queue entries and seven dated entries moved verbatim to docs/history/handover-home-archive.md under "Queue DONE items moved 4 Nov"; CALC-DOCK-WIDE first, then oldest first. GitHub REST confirms all seven PRs merged; each squash commit is an ancestor of origin/main. Cloud ownership line retained. No live or unmerged item moved. Context size passes without warning and with more than 3 KB spare after this entry.

STOP IF hit during contract/code check: shared fraction-input.js digits() strips every non-digit and value() rejects a signed numerator. The 6 P's bank schools/assets/six-ps/linear-equations.json contains linear-equations-375c850e (10x = -4, answer -2/5) and linear-equations-98ad8c09 (9x = -6, answer -2/3). Both require a signed numerator that adding only whole:true cannot represent. Existing player explicitly enables its minus key for fraction answers. No component, player, bank, verifier, warn-list or cloud handover changes. Next: Jon/Project Claude ruling extending the component API for signed fractions while preserving its current default behaviour. No implementation, push or PR yet.

Record: agent Codex; wall n/a; review cycles 0; amendments 1 (pre-step extension); usage n/a.

