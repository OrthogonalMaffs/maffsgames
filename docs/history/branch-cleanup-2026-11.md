# BRANCH-CLEANUP: the remote branches, 8 Nov 2026

Contract BRANCH-CLEANUP (Project Claude, 8 Nov 2026). Snapshot: `git ls-remote --heads origin` and `refs/pull/*/head` on 8 Nov 2026, main at 4b57afd0; every PR read by REST (`GET /pulls?state=all`). 156 remote branches: 124 DELETE, 20 KEEP (main among them), 12 NO PR AT TIP; each in exactly one table. `delete_branch_on_merge` (GET /repos/OrthogonalMaffs/maffsgames): **true**, so GitHub already deletes a merged PR's head branch; read only, not changed.

Why NO PR AT TIP is 12, not the 24 expected: 24 branches have no PR at their tip; 12 of them are named in `docs/todo.md`, `docs/handover/contracts/` or a handover, so they are in KEEP (step 2b), and 12 are named nowhere. No branch fits both DELETE and KEEP.

## DELETE (124: 118 merged, 6 closed unmerged)

Each branch's tip is the head of the PR named (its `refs/pull/N/head`), and that PR is merged or closed. Those commits stay reachable through `refs/pull/N/head`, which GitHub keeps after a branch is deleted, so deleting the branch loses nothing. None is named in `docs/todo.md`, `docs/handover/contracts/` or either handover. Deleted only after this file's PR merges (phase 2), one REST call each.

| Branch | Tip SHA | PR | State |
|---|---|---|---|
| `claude/answer-fraction` | df7de9425ba7 | #122 | merged |
| `claude/art-pending` | 063f2b8e3347 | #244 | merged |
| `claude/bank-foundation` | 2575272b9bcf | #254 | merged |
| `claude/c-better-value` | aedd36e91b52 | #113 | merged |
| `claude/c-estimation-golf` | 08269ccd3165 | #118 | merged |
| `claude/c-formula-unlocked` | 43dc26155dcd | #116 | merged |
| `claude/c-given-that` | a15f130d0dc0 | #114 | merged |
| `claude/c-proportion-blaster` | aa0b604a816c | #111 | merged |
| `claude/c-sequence-solver` | aa06c2394718 | #117 | merged |
| `claude/canon-r15-timer` | db12f57dfa48 | #121 | merged |
| `claude/car-trap-release` | f77e7c9e3de5 | #252 | merged |
| `claude/car-trap-v2-art` | c3124e233f60 | #246 | merged |
| `claude/changed-utf8` | d505fc2ef746 | #178 | merged |
| `claude/checkpoint-8oct` | 34005043de3f | #169 | merged |
| `claude/checkpoint-8oct-late` | 12f98a306de5 | #186 | merged |
| `claude/checkpoint-9oct` | cb955552a47d | #192 | merged |
| `claude/ci-balance` | 430fc3ac4852 | #220 | merged |
| `claude/ci-lines-v` | 3bc4dc06d26b | #108 | merged |
| `claude/ci-timings-artifacts` | 3ad81ca99d03 | #224 | merged |
| `claude/ci-timings-fix` | e6a688113512 | #222 | merged |
| `claude/claim` | 1702d4937163 | #145 | merged |
| `claude/compassionate-cori-3xi42y` | 4e0411224412 | #263 | merged |
| `claude/contracts-folder` | 7e3390314e69 | #194 | merged |
| `claude/core-maths-paper1-cpi` | d1b082640632 | #93 | merged |
| `claude/ctx` | 460c9d203bfa | #158 | merged |
| `claude/dashboard-charts` | 96b3ed2035e2 | #243 | merged |
| `claude/det` | 5beba36d8e5a | #144 | merged |
| `claude/dnd-live-record` | 345fbc83f20c | #424 | closed-unmerged |
| `claude/docs-9oct` | 670dcfd4a571 | #240 | merged |
| `claude/docs-9oct-b` | 9eb90420d722 | #249 | merged |
| `claude/docs-small` | 9c3e840648eb | #188 | merged |
| `claude/escape-analytics` | 57391f3082bd | #276 | merged |
| `claude/escape-canon-label` | b1cbc6bffe2c | #279 | merged |
| `claude/escape-difficulty` | 6cc6adfa2c59 | #253 | merged |
| `claude/escape-set-checks` | 62ee17f0937f | #278 | merged |
| `claude/essentials` | ec191369a30a | #150 | merged |
| `claude/essentials-wording` | 7ed676dd98f4 | #172 | merged |
| `claude/f1-answer-lock` | d4c1e58251f1 | #125 | merged |
| `claude/f1-batch1` | 384cce4c22b9 | #129 | merged |
| `claude/f1-batch10` | 9db28e48a7c6 | #199 | merged |
| `claude/f1-batch11` | 0d665c31bba2 | #200 | merged |
| `claude/f1-batch2` | 0017cf05543a | #132 | merged |
| `claude/f1-batch3` | 7f9f18f342c1 | #136 | merged |
| `claude/f1-batch4` | 6a4a054c6842 | #140 | merged |
| `claude/f1-batch5` | ead835b78433 | #161 | merged |
| `claude/f1-batch6` | dc53ceb68459 | #165 | merged |
| `claude/f1-batch7` | afa0a31bfd76 | #182 | merged |
| `claude/f1-batch8` | ef28d039cc25 | #190 | merged |
| `claude/f1-batch9` | 10e73ae67fcd | #198 | merged |
| `claude/f1-lock-hints` | 5798fa884348 | #133 | merged |
| `claude/f1-suvat-migrated` | 6fafa03bebfc | #131 | merged |
| `claude/ga4-country-canon` | 725c7f1b6fcd | #179 | merged |
| `claude/gitattributes-bytes` | e389cb39b0fa | #268 | merged |
| `claude/given-that-fractions` | 48c6a80e38d1 | #123 | merged |
| `claude/graph-sketcher-fit` | fd4b261b478b | #218 | merged |
| `claude/handover-dial` | c8fdf8b7ca96 | #518 | closed-unmerged |
| `claude/handover-gate-fix` | ddbb02247dd0 | #636 | closed-unmerged |
| `claude/hook-fix-car-trap` | b3b2a95bf60c | #221 | merged |
| `claude/keen-cray-ypsime` | 1f83f223a5a4 | #130 | merged |
| `claude/keypad-variable` | 5c26ea0d2fb0 | #251 | merged |
| `claude/library-jam-art` | 1d2e7709c0b3 | #270 | merged |
| `claude/lock-bank-ci` | a4d33d2226c8 | #258 | merged |
| `claude/log-notation` | dd74f436c375 | #274 | merged |
| `claude/ltc-flake` | 6bdaf9ed5ea0 | #167 | merged |
| `claude/ltc-focus-race` | 990ddd78315e | #184 | merged |
| `claude/ltc-mark-wait` | 1ac2da97a2d4 | #119 | merged |
| `claude/nice-babbage-4rq1fn` | 85d23f545577 | #191 | merged |
| `claude/overlay-keys` | 6642c820da9f | #232 | merged |
| `claude/overnight-end` | 4eca5d677917 | #201 | merged |
| `claude/play-again-screen` | ce8fbe0c6c66 | #234 | merged |
| `claude/play-again-screen-2` | e3bbedbee77e | #237 | merged |
| `claude/prepush-scope` | c8be687aaf71 | #255 | merged |
| `claude/queue-note-2025` | 7bf8b6c400a6 | #233 | merged |
| `claude/regex-test-fix` | 89073c37f90e | #120 | merged |
| `claude/relist-3` | 4597cb90b916 | #176 | merged |
| `claude/relist-sr` | cdb4e0607f0e | #197 | merged |
| `claude/relist-sr21` | ebac7367d1b6 | #142 | merged |
| `claude/rightful-king-art` | a9d15e22634a | #269 | merged |
| `claude/room-status-single-table` | 4dcb3aa261b8 | #280 | merged |
| `claude/rooms-release-rk-lj` | 2bfa2aaa3fc8 | #271 | merged |
| `claude/rulings-9oct` | d64ff5777e83 | #215 | merged |
| `claude/sci-calc` | ee64b6a5adaf | #239 | merged |
| `claude/sci-core-maths-paper2c` | 558f613bb73e | #267 | merged |
| `claude/sci-force-resolver` | 538ea18af222 | #261 | merged |
| `claude/sci-formula-forge` | 661f906ed434 | #265 | merged |
| `claude/sci-formula-unlocked` | 16f59798505d | #266 | merged |
| `claude/sci-moments-master` | 9cf9827b76b6 | #264 | merged |
| `claude/scores-offline` | 62f37a050b10 | #238 | merged |
| `claude/screening-room-figures` | bf3aa904ec7f | #92 | merged |
| `claude/sharp-lamport-crewyu` | 9382a52d5bc4 | #275 | merged |
| `claude/split-it-katex` | 8c27527ec87c | #281 | merged |
| `claude/star-key` | 3b8506382657 | #260 | merged |
| `claude/tender-dijkstra-oesq52` | 228f8d92dcd9 | #141 | closed-unmerged |
| `claude/todo-slim` | 13956be11c99 | #259 | merged |
| `claude/updates` | b44d638f76ff | #151 | merged |
| `claude/verifier-factor-race` | dd12e16d0a03 | #285 | merged |
| `claude/verifier-fraction-equivalence` | af109897da5f | #283 | merged |
| `claude/verifier-new-shapes` | 05637d80aca4 | #292 | merged |
| `claude/verifier-percentage-flip` | 9b2262d9953b | #284 | merged |
| `claude/verifier-prime-factorisation` | 313a4a0d9866 | #286 | merged |
| `claude/verifier-prime-or-composite` | 422c467a592c | #282 | merged |
| `claude/vocab-idempotent` | b2e3b0c9d4c5 | #193 | merged |
| `claude/vocab-showthat` | 2909e00e7df0 | #180 | merged |
| `claude/worktree-cleanup` | 9cc534bdcb30 | #277 | merged |
| `claude/youthful-bardeen-tu64yp` | e838d95f60bb | #115 | merged |
| `claude/youthful-feynman-anpxuq` | 190463764c9f | #225 | merged |
| `claude/youthful-feynman-anpxuq-boolean-blitz` | b5bfe3bb18dd | #227 | merged |
| `claude/youthful-feynman-anpxuq-build-queue` | e1b6e9ee42cc | #250 | merged |
| `claude/youthful-feynman-anpxuq-car-trap-build` | ffe888d50f0d | #242 | merged |
| `claude/youthful-feynman-anpxuq-car-trap-draft` | 432426997007 | #235 | merged |
| `claude/youthful-feynman-anpxuq-characteristic-quest` | 536a239b5f43 | #228 | merged |
| `claude/youthful-feynman-anpxuq-e2` | ea384d72760d | #213 | merged |
| `claude/youthful-feynman-anpxuq-eigenvalue-extractor` | 192c3c711b98 | #229 | merged |
| `claude/youthful-feynman-anpxuq-font-fit` | 0c7d1484c338 | #256 | merged |
| `claude/youthful-feynman-anpxuq-formula-forge` | 4103982182eb | #231 | merged |
| `claude/youthful-feynman-anpxuq-handover-1010` | 56d72dbbfe18 | #245 | merged |
| `claude/youthful-feynman-anpxuq-handover-235` | 942b6b60735b | #236 | merged |
| `claude/youthful-feynman-anpxuq-library` | 6c46b3f2b2a2 | #248 | merged |
| `claude/youthful-feynman-anpxuq-matrix-crunch` | 5ea41dccfa69 | #230 | merged |
| `claude/youthful-feynman-anpxuq-paper2b` | ff69237df4a0 | #226 | merged |
| `claude/youthful-feynman-anpxuq-pd-close` | 3fff142b74f4 | #241 | merged |
| `claude/youthful-feynman-anpxuq-rightful-king` | 846c13845bb6 | #247 | merged |
| `codex/christmas-pack-current` | 6dc5e2fa9c50 | #690 | closed-unmerged |
| `codex/start-task` | 5248638f325f | #628 | closed-unmerged |

## KEEP (20)

| Branch | Tip SHA | Tip date | Reason |
|---|---|---|---|
| `art/christmas-pack` | 74bcc1bbdd6b | 2026-11-06 | prefix art/ |
| `art/christmas-tree-fiasco` | efd31d53f5be | 2026-11-04 | prefix art/ |
| `art/estimation-golf` | 028cf6839587 | 2026-11-02 | prefix art/ |
| `art/kiln-pack` | b06e450642f7 | 2026-11-04 | prefix art/ |
| `claude/fold-canon` | 4a526a631b95 | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/fold-*); docs/todo.md |
| `claude/fold-figures` | 4bdcb2104250 | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/fold-*) |
| `claude/fold-figures-v2` | 227c3d6da205 | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/fold-*); docs/todo.md |
| `claude/fold-options` | c18738c9ae1c | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/fold-*); docs/todo.md; docs/todo.md (claude/fold-options*) |
| `claude/fold-options-v2` | 44a4ef8effec | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/fold-*); docs/todo.md; docs/todo.md (claude/fold-options*) |
| `claude/fold-publish` | ed00d80f965e | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/fold-*); docs/todo.md |
| `claude/jpib-split` | c8ed288f4ffb | 2026-10-27 | named in docs/handover/contracts/2026-10-27-fold-components.md |
| `claude/keypad-fraction` | fbf6c3620f34 | 2026-10-27 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md; docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/keypad-fraction*); docs/todo.md; docs/todo.md (claude/keypad-fraction*) |
| `claude/keypad-fraction-key` | 799dbfd94640 | 2026-10-27 | named in docs/handover/cloud.md; docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/keypad-fraction*); docs/todo.md (claude/keypad-fraction*) |
| `claude/six-ps-banks-1` | 7f8142a7b288 | 2026-10-25 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/six-ps-*) |
| `claude/six-ps-card` | 7646c5461fb6 | 2026-10-29 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/six-ps-*) |
| `claude/six-ps-handover-541` | 5dd6d69dd7fc | 2026-10-25 | named in docs/handover/contracts/2026-11-08-branch-cleanup.md (claude/six-ps-*) |
| `main` | 4b57afd015b1 | 2026-11-08 | the default branch |
| `pr-assets/christmas-room` | b43dfee9b426 | 2026-11-05 | prefix pr-assets/ |
| `pr-assets/teacher-invite` | 47beb080a293 | 2026-10-04 | prefix pr-assets/ |
| `wip/linear-equation-solver` | a2083e21f783 | 2026-10-07 | prefix wip/ |

## NO PR AT TIP (12; proposed verdicts, none deleted by this contract)

"Files equal to main" compares each file the branch changed with main's copy today. PRs were squash-merged, so a differing file can still be work main already has; the verdict names where main has it.

| Branch | Tip SHA | Tip date | Ahead of main | Files equal to main | Proposed verdict | Why |
|---|---|---|---|---|---|---|
| `claude/determined-galileo-8fb399` | 0da25e4d0e54 | 2026-10-06 | 1: Just Pythag It, Bruv: listed; triangle fitted to the keypad (60% floor); Round 1 'Spot the shortcut?' | 0 of 14 | DELETE | superseded: Just Pythag It, Bruv listed by RELIST-3 (#176, addb51ee, 8 Oct) |
| `claude/keen-cray-ypsime-binomial-blaster` | 67bf685cf5ee | 2026-10-07 | 1: Binomial Blaster: Jon's alevel2[36] (B = 2); MaffsLock; the B3 duplicate cleared | 0 of 3 | DELETE | the same commit merged as eab7330e (#138) |
| `claude/keen-cray-ypsime-eigenvector-engine` | 3394734fb59c | 2026-10-07 | 1: Eigenvector Engine: Project Claude's QS[16]; no option a multiple of an eigenvector or of another option (SR-17); working through MaffsText; MaffsLock; verifier | 0 of 3 | DELETE | the same commit merged as 8c2f23ec (#134) |
| `claude/keen-cray-ypsime-partial-fractions-duel` | 9a19235d1a6d | 2026-10-07 | 1: Partial Fractions Duel: Jon's alevel[22] (C = 1/6); MaffsLock; the B3 duplicate cleared | 0 of 3 | DELETE | the same commit merged as c59bcfb4 (#139) |
| `claude/keen-cray-ypsime-trig-identity-duel` | 03c34eb4e226 | 2026-10-07 | 1: Trig Identity Duel: Jon's gcse[16] (12.2); a hidden count-up, no marks for speed (SR-23); MaffsLock; the B3 duplicate cleared | 0 of 3 | DELETE | the same commit merged as abc5fdab (#137) |
| `claude/keen-cray-ypsime-truth-buster` | fcc5e4c4053d | 2026-10-07 | 1: Truth Buster: the reason and Next above the fold at 390x844 on every item (canon 7.6.1); MaffsLock (t3-013); verifier measures both | 0 of 2 | DELETE | the same commit merged as bd5bb7a6 (#143) |
| `claude/keen-cray-ypsime-truth-will-set-you-free` | 7b07e09a5691 | 2026-10-07 | 1: The Truth Will Set You Free: tables computed from each key; only correct cells score; [27]'s simplified form; [6]'s duplicate distractor; Aa saved; MaffsLock; verifier | 0 of 2 | DELETE | the same commit merged as 71fd49c8 (#135) |
| `claude/stoic-galileo-xvzt45` | 3c20c14a411f | 2026-11-04 | 4: Cloud handover: main green after #655; the report's placeholder address found live (4 Nov); Cloud handover: /exec reports 2026-11-03-b (Jon, 4 Nov); Cloud handover: Jon reports the 2026-11-03-b endpoint redeployed and working; Close DASHBOARD-METRICS in the cloud handover (MERGED #655); Jon's redeploy step outstanding | 1 of 2 | JON | cloud handover notes for DASHBOARD-METRICS; the contract move is on main, but its 4 Nov finding is recorded nowhere on main: a manual `sendDailyReport` failed with "Invalid email: OWNER_EMAIL_HERE" (the pasted endpoint kept the placeholder), with the proposal to read the address from Script Properties |
| `claude/theme-distinctly-average` | dacb7c3aabe9 | 2026-10-26 | 7: LOOK-REDS-2 checkpoint: the phone-fit gate's first runs, games flagged (normal 20, Aa 35, Aa-320 warnings 14); LOOK-REDS-2 checkpoint: measure-phone-fit gates options that start below the fold; Jon's Aa ruling saved; two STOPs recorded; Handover: LOOK-REDS-2 (Distinctly Average) built, waiting on Jon's Aa ruling; TOP-SCORES archived as done; LOOK-REDS-2 (Distinctly Average): Aa on a phone; the median card below Next; the x-bar drawn; LOOK-REDS-2 (Distinctly Average): the wrong-answer screen fits a phone; LOOK-REDS-2: claim distinctly-average; the contract saved verbatim; THEME-DA (work in progress, paused): Distinctly Average onto theme.css; phone fit not finished | 0 of 9 | DELETE | superseded by LOOK-REDS-2 (#554, 27f56a0d): Distinctly Average onto theme.css and the phone gate |
| `claude/verifiers-17-20-drafts` | a5d39dff0bbc | 2026-10-12 | 1: Park VERIFIERS-20 drafts for games 17-20 (checkpoint; not live) | 0 of 6 | DELETE | superseded: all four drafted verifiers are on main (formula-forge #305, characteristic-quest #306, eigenvalue-extractor #307, prisoners-dilemma #309) |
| `claude/wonderful-hamilton-ovf7vf` | 884ec8bc5eaf | 2026-10-08 | 1: Cloud handover: FT-FIX amendment saved verbatim (Jon, 21:30: step 3 to the home lane, t5-008 stays open); queue UC-FIX first, then FT-FIX | 0 of 2 | DELETE | superseded: the FT-FIX amendment is on main, fuller and later, as `docs/history/contracts/2026-10-08-ft-fix-amend.md` |
| `claude/youthful-feynman-anpxuq-pd-check` | 1cf970fea672 | 2026-10-09 | 3: Cloud handover: PD-CHECK stopped for Jon (#232 fixes t4-002; the saved check tests a fake overlay); CAR-TRAP-DRAFT next; Cloud handover: LISTED-HIGH complete but item 12; main green on #231 (run 37978742832); the check's branch; stacked PRs ruled fine; Prisoner's Dilemma check saved for item 12 (not in CI: it fails main until OVERLAY-KEYS, #232) | 0 of 3 | DELETE | superseded: `scripts/verify-prisoners-dilemma.py` is on main (#309); its handover lines were rewritten since |
