# Handover: home lane

**Queue (cross-lane facts; never archived)**

- DONE queue: docs/history/handover-home-archive.md

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

- FRACTION-WHOLE: home/Codex, codex/fraction-whole, /home/maffs/mg-fraction-whole; contract docs/handover/contracts/2026-11-04-fraction-whole.md. Amendment 1 resolves signed-fraction STOP. Shared: checks in progress; stop at green Gate for Project Claude and Jon's merge.

## 2026-11-04 (home): FRACTION-WHOLE

Agent: Codex. Worktree: /home/maffs/mg-fraction-whole. Branch: codex/fraction-whole. Base: 67610171. Pre-step and its extension completed: seven queue entries and seven dated entries moved verbatim to docs/history/handover-home-archive.md under "Queue DONE items moved 4 Nov"; CALC-DOCK-WIDE first, then oldest first. GitHub REST confirms all seven PRs merged; each squash commit is an ancestor of origin/main. Cloud ownership line retained. No live or unmerged item moved. Context size passes without warning and with more than 3 KB spare after this entry.

STOP IF hit during contract/code check: shared fraction-input.js digits() strips every non-digit and value() rejects a signed numerator. The 6 P's bank schools/assets/six-ps/linear-equations.json contains linear-equations-375c850e (10x = -4, answer -2/5) and linear-equations-98ad8c09 (9x = -6, answer -2/3). Both require a signed numerator that adding only whole:true cannot represent. Existing player explicitly enables its minus key for fraction answers. No component, player, bank, verifier, warn-list or cloud handover changes. Next: Jon/Project Claude ruling extending the component API for signed fractions while preserving its current default behaviour. No implementation, push or PR yet.

Resumed under Jon's signed-fraction Amendment 1 (saved verbatim). Optional whole/signed modes added at the shared layer; The 6 P's mounts signed mode for every fraction, with whole mode where declared. Its judge() and fractionRaw() are byte-identical; readInput adapts shared raw strings to the existing fields. Only its verifier's input driver changes for the separate sign button; scripted marking values/expectations unchanged, plus a new fraction-phone unit. The page's own fraction boxes/CSS removed and warn-list entry removed. Cloud Queue's authorised follow-up names HOW-MANY-PARTS-FRACTION; no game or Gate files touched.

New component test: four mode combinations at 320x568, 360x640, 375x667, 1280x700 and 1280x701 PASS, five plants CAUGHT, exit 0 (including sign dropped from raw). Initial plant run crashed when deliberately missing a whole target; two bounded test-harness fixes guard both loops; rerun passes. Fraction-input checker selftest 10/10; check 112 pages, 3 shared users, only how-many-parts warns, 0 failures. Existing 6 P's verifier and new fraction-phone unit running. Next: remaining regression checks, check-changed.py, approved updates wording, PR and Gate; Shared review hold.

Record: agent Codex; wall n/a; review cycles 0; amendments 2 (pre-step extension and signed Amendment 1); usage n/a.

