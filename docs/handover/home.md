# Handover: home lane

**Queue (cross-lane facts; never archived)**

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts to move next (cloud lane, HOW-MANY-PARTS-FRACTION)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

- FRACTION-WHOLE: home/Codex, codex/fraction-whole, /home/maffs/mg-fraction-whole, draft PR #662; contract docs/handover/contracts/2026-11-04-fraction-whole.md. Claims fraction-input.js and the-6-ps; checked locally. #660 created updates/cloud.md conflicts; awaiting Jon's branch-merge exception. Shared review hold.

## 2026-11-04 (home): FRACTION-WHOLE

Agent: Codex. Worktree: /home/maffs/mg-fraction-whole. Branch: codex/fraction-whole. Base: 67610171. Pre-step and its extension completed: seven queue entries and seven dated entries moved verbatim to docs/history/handover-home-archive.md under "Queue DONE items moved 4 Nov"; CALC-DOCK-WIDE first, then oldest first. GitHub REST confirms all seven PRs merged; each squash commit is an ancestor of origin/main. Cloud ownership line retained. No live or unmerged item moved. Context size passes without warning and with more than 3 KB spare after this entry.

STOP IF hit during contract/code check: shared fraction-input.js digits() strips every non-digit and value() rejects a signed numerator. The 6 P's bank schools/assets/six-ps/linear-equations.json contains linear-equations-375c850e (10x = -4, answer -2/5) and linear-equations-98ad8c09 (9x = -6, answer -2/3). Both require a signed numerator that adding only whole:true cannot represent. Existing player explicitly enables its minus key for fraction answers. No component, player, bank, verifier, warn-list or cloud handover changes. Next: Jon/Project Claude ruling extending the component API for signed fractions while preserving its current default behaviour. No implementation, push or PR yet.

Resumed under Jon's signed-fraction Amendment 1 (saved verbatim). Optional whole/signed modes added at the shared layer; The 6 P's mounts signed mode for every fraction, with whole mode where declared. Its judge() and fractionRaw() are byte-identical; readInput adapts shared raw strings to the existing fields. Only its verifier's input driver changes for the separate sign button; scripted marking values/expectations unchanged, plus a new fraction-phone unit. The page's own fraction boxes/CSS removed and warn-list entry removed. Cloud Queue's authorised follow-up names HOW-MANY-PARTS-FRACTION; no game or Gate files touched.

New component test: four mode combinations at 320x568, 360x640, 375x667, 1280x700 and 1280x701 PASS, five plants CAUGHT, exit 0 (including sign dropped from raw). Initial plant run crashed when deliberately missing a whole target; two bounded test-harness fixes guard both loops; rerun passes. Fraction-input checker selftest 10/10; check 112 pages, 3 shared users, only how-many-parts warns, 0 failures. Existing 6 P's verifier and new fraction-phone unit running. Next: remaining regression checks, check-changed.py, approved updates wording, PR and Gate; Shared review hold.

Implementation commit: f7f157b5. Full verify-the-6-ps.py PASS, exit 0: 34 covered topics, 43 fixture questions, 10,000 session draws each way, desktop and 320px touch sessions, all marking cases, all 25 plants caught. Fraction-phone unit passes all five fixture shapes (including mixed and negative) plus both real negative questions at 320x568, 360x640, 375x667: asking controls and wrong-answer Next above viewport minus 40px, no sideways scroll, sign button on every fraction. Log .claude/bg-1793814069591.log. Direct old/new component comparison at all five sizes confirms default DOM, filtering, raw/value/filled, marking classes, clearing, Enter and geometry exactly equal. Possibly, Maybe, Pies and check-changed queued serially in .claude/bg-1793814327449.log, stopping on first nonzero exit. Awaiting Jon's updates wording; draft/Shared hold until complete.

Jon supplied the updates wording; added newest under November New in the existing dated markup and saved the wording in the contract. No editorial hold remains; finish checks, PR and Gate, then Shared review hold.

Local checks complete: verify-possibly-maybe.py PASS (1,200 questions, 4,713 marking probes, 13 plants), verify-who-ate-all-the-pies.py PASS (1,442 probes, 14 plants), both unchanged, exit 0 each. Full check-changed.py 65/65 in 1078s, exit 0; 15 heavy serial, 50 light. Summary: "All selected checks passed. Push, and CI runs the rest." Log .claude/bg-1793814327449.log captures each command's exit and overall exit 0. CI deferrals: Stage exit, Level resolver in play parts 1/2 selected indirectly through fraction-input.js; seven standard deferrals (four page-load shards, first includes hang scan; bank extraction; ledger lint; leaderboard coverage). No checker weakened.

STOP pending rulebook exception: cloud #660 merged while checks ran. git fetch plus read-only git merge-tree --write-tree --name-only HEAD origin/main (4f2b817a) confirms conflicts only in updates/index.html and docs/handover/cloud.md. Worktree is clean; no merge started. Asked Jon for an explicit exception to AGENTS.md's ban on merging into an existing task branch: preserve all updates and main's cloud handover, reapply only HOW-MANY-PARTS-FRACTION Queue clause. No answer yet. Next: push a draft with complete evidence, retain branch/worktree; after Jon's ruling resolve only those files, Gate, Shared review and Jon's merge. Final PR state tracked in its report. No merge or cleanup authorised.

Pushed and opened draft PR #662: https://github.com/OrthogonalMaffs/maffsgames/pull/662 . Contract and signed Amendment 1 included verbatim; full report and phone table in body. Last commit before this pointer: 9a9f110f; implementation f7f157b5, updates a0b324c4. Stop pending the requested branch-merge exception; no Gate result can be obtained while conflicted. Retain /home/maffs/mg-fraction-whole and codex/fraction-whole. Final context-size check passes with home.md well below the warning band; no merge/cleanup.

Jon's 4 Nov rulings on #662 resolve the merge STOP and supersede the original contract's cloud Queue edit. Consumed the one-time exception by merging origin/main 31c04c6a into this branch; only updates/index.html and docs/handover/cloud.md conflicted. Cloud handover restored byte-for-byte to main, removing this PR's edit entirely; HOW-MANY-PARTS-FRACTION note now in this Queue and PR body. Updates keeps every entry from both sides, unchanged, newest date first. Rulings saved verbatim in the contract and PR. Next: full local check rerun, push and Gate; stop for Shared review and Jon's merge. No further merge-from-main exception and no PR merge authority.

Record: agent Codex; wall n/a; review cycles 0; amendments 3 (pre-step extension, signed Amendment 1, #662 rulings); usage n/a.

