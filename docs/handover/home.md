# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-20 (home): CALC-IMPLIED-MULT (implied multiplication before × and ÷, as on a current Casio; Enter is equals)

Claude Code (home lane), worktree `~/mg-calc-implied`, branch `claude/calc-implied-mult`; contract `docs/handover/contracts/2026-11-20-calc-implied-mult.md` (Amendments 1-2). Tier Small. The first commit carries TODO-TRIM's close-out (#844, 3d6ce66; its entry below; contract moved to `docs/history/contracts/`).

- **`schools/assets/calculator.js`:** a new grammar level, `implied := unary (<implicit ×> power)*`, under `term := implied (('×' | '÷') implied)*`, so implied multiplication binds tighter than × and ÷ (267÷2π = 42.49436981, 6÷2(1+2) = 1); an implied factor is a power(), never signed, so 2-3 stays a subtraction. Header grammar and prose updated. Keys, layout, CSS, modes and the other rules unchanged.
- **Amendment 1 (Enter is equals):** the panel's keydown handler presses = on Enter (and =) wherever focus is in the panel; Space on a focused key still presses that key. Comment updated.
- **Tests (`scripts/test-calculator-js.py`):** the contract's 11 cases added (76 expressions pass); plants caught: the old flat term(), an implied factor taking a leading minus. Enter cases: click 7 then Enter gives "7 =" / 7 (not 77); Tab to the 8 key then Space types 8; Enter on the panel is =. Plant caught: the old "Enter presses the focused key" branch. One existing case asserted the old Enter behaviour ("Enter on the focused 7 key ... expected the key pressed (7), not =") and is replaced by the new rule; no existing case asserted the old order of operations. Full run PASS.
- **check-calculator.py** PASS; the calculator-driving verifiers (card-filter, estimation-engine, its-on-sale, just-pythag-it-bruv, squared-squirrel, take-a-walk, the-6-ps, unit-converter, who-ate-all-the-pies) PASS. No page outside calculator.js calls MaffsCalc.evaluate or calc, so no answer key or marking depends on the old order.
- **Amendment 2 (a right answer clears the calculator): STOPPED (its STOP IF), nothing changed.** `growth-and-decay` CM2 (`L = k × 0.98^T`, sq_order [3,1,2]) sends `question_answered` correct:true on sub-question 3, "Given that L = 100 when T = 24, find the value of k", then asks sub-question 1, "calculate L when T = 30", which needs that k (not shown in the model). A clear on that correct answer would wipe working still needed. Every other calculator page sends one question_answered per finished question (i-dropped-my-ice-cream and its-a-sine at the last box, stat-attack at the end of the scenario). Question for Jon in todo row CALC-CLEAR-ON-RIGHT.
- Canon §4.4 note (points at SR-28); one /updates/ line, Amendment 1's wording.

## 2026-11-20 (home): TODO-TRIM (todo.md holds only open work; the cap lowered; a row-length warning)

Claude Code (home lane), worktree `~/mg-todo-trim`, branch `claude/todo-trim`; contract `docs/handover/contracts/2026-11-19-todo-trim.md`. Tier Medium. The first commit carries WRONG-PAUSE-NEXT's close-out (#842, 8ab38d1; its entry below; contract moved to `docs/history/contracts/`).

- **todo.md 152,931 → 96,712 bytes** (todo-done.md 443,563 → 528,066). Moved whole: 3.4, 3.6, 3.7, 3.10, SIX-PS-LOOK-REDS, §4 items 6, 7 and 16, and finished prose (§1's 26 Sep blocks, §2's "Still unverified", §4's layer A and Group C sub-items, §5's calculator bullet). Rewritten to what is owed, each old text word for word in todo-done.md under its ID ("Moved by TODO-TRIM, 19 Nov 2026"): 1.14, 1.26, 1.34, 1.36, 3.1, 3.5, 3.8, 3.9, 3.12, 3.21, PRIME-SPRINT-LOOK-REDS, TAKE-A-WALK-PHONE-LAYOUT, DD-LINEUP-FEEDBACK, PACKS-V2-UPLOAD, §4 items 12, 18, 23, 27, 28, §3.9's order (12.3 KB to 4 KB) and the 45 LEDGER rows (their shared survey/recorded tail said once in the section's intro; every group is still in data/check-ledger.json, so none closed).
- **`scripts/check-todo-trim.py`** (ci-held, one-off): PASS: 164 IDs, 8 moved, 62 rewritten, none lost; 413 removed sentences and cells, each verbatim in todo-done.md. Plants caught: a moved row deleted from todo-done.md; one sentence altered.
- **`scripts/check-context-size.py`:** TODO_LIMIT 150 → 105 KiB (96,712 + 10 KiB, rounded up); a todo.md table row over ROW_WARN (1,200) characters is a warning, never a failure; self-tests: 1,201 warns, 1,200 silent; SELFTEST PASS. Five rows warn, all open work: 3.12, 3.20, MONEY-THOUSANDS, GRAPH-SKETCHER-REDESIGN, PACK-ART-EXTRAS. The ci-line label states the new cap (ci-groups --check PASS, warns until main times the new label). AGENTS.md:70 states 105 KiB.
- **Rule:** AGENTS.md:83 is Jon's sentence of 19 Nov; canon's LIVE-BUG-RECHECK section mirrors it, with the reason. No /updates/ line.
- **Decided for you:** (1) check-context-size.py is a Gate file (cloud's, AGENTS.md); edited because the contract names it. (2) PRIME-SPRINT-LOOK-REDS: #660 (LOOK-REFRESH-1) put Prime Sprint on theme.css with no pixel font, so the row now asks Jon to close it or contract its one leftover (Aa Start button 657 / 627 at 375x667, "not a gate"). (3) SIX-PS-LOOK-REDS moved as done: factor-race and distinctly-average load theme.css and use no pixel font (main 527f8b8). (4) 3.6 and 3.10 moved whole as the contract lists them, so their blocked-on cells went too: 3.6 "Jon: eyeball pass and the ten points in START"; 3.10 "Jon: 320 is 173px over 1.5 screens". (5) §4 items 6 and 7 judged done: CLAUDE.md is 15 lines with `docs/history/claude-md-archive.md`; `schools/assets/calculator.js` is the shared calculator. (6) Where a row named no owner (3.8, §4 item 12's `--live` confirmation), it now says so. (7) 3.5's blocked-on cell restated: canon has carried ruling (1) since 2 Oct. (8) The heading date is the contract's (19 Nov).

- MERGED 20 Nov as 3d6ce66 (#844) via merge-pr.py, exit 0, last line "main 3d6ce66 run 44688020212: GREEN". Main on the merge commit: check-site 44688020212 success, phone-fit-full 44688020167 success (both push runs), pages build 44688019690 success (all confirmed from the API). Contract moved to `docs/history/contracts/2026-11-19-todo-trim.md` (closed out by CALC-IMPLIED-MULT's first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-19 (home): WRONG-PAUSE-NEXT (four games pause on Next after a wrong answer; check-answer-lock fails a game that stops pausing)

Claude Code (home lane), worktree `~/mg-wrong-pause-next`, branch `claude/wrong-pause-next`; contract `docs/handover/contracts/2026-11-19-wrong-pause-next.md`. Tier Medium. The first commit carries the close-outs of #837 NEXT-IN-VIEW and #839 DD-VERIFIER-SHARD (their entries below; both contracts moved to `docs/history/contracts/`).

- **Games:** binomial-blaster, partial-fractions-duel, trig-identity-duel load next-control.js; a wrong answer shows "The answer:" and the key (KaTeX by the option's own rule) in a new line beside Next (`#after`, a wrapping flex row), then MaffsNext.wrong (keep: that line); right answers still advance at 1000 ms; MaffsNext.clear at the top of showQ. word-problem-decoder: a wrong answer outlines the phrase's own highlight in the text and shows "The answer:" (every accepted topic) and "The clue:" above Next; the fade runs when Next is pressed. Their verifiers pass.
- **check-answer-lock.py:** the 390px touch play first watches the wrong answer for PAUSE_S (3 s): FAIL if the game draws something new through MaffsLock (fresh/screen) with no pause control on screen, or no pause control (MaffsNext's, a `.dismiss-btn`, or a game's own on OWN_NEXT) is on screen by the end. Four lists, documented at the top: OWN_NEXT (17), WRONG_PAUSE_UNCHECKED (6, shrink-only), WRONG_PAUSE_EXEMPT (2, changes need Jon), WRONG_PAUSE_KNOWN_FAIL (52dle, shrink-only); each with its reason. Self-test PASS: both plants CAUGHT. On main's pages the check fails binomial-blaster and word-problem-decoder. The first draft's `up` test (an enabled option group read as a new question) gave 9 false failures; replaced.
- **STOP (19 Nov):** the first full run failed 22 other games (17 own Next; 52dle, higher-power, trig-wars, split-it, growth-and-decay with no pause). **Jon's ruling, 19 Nov:** 1 the 17 into OWN_NEXT; 2 `.dismiss-btn` (_addDismiss "Try Again", 8 games) counts as a pause control while the question holds, window 3 s (split-it and growth-and-decay then pass, no game edit); 3 WRONG_PAUSE_EXEMPT higher-power, trig-wars; 4 WRONG_PAUSE_KNOWN_FAIL 52dle (52DLE-REBUILD); 5 UNCHECKED keeps the 6; 6 phone-fit, PR, merge.
- **Full local in-play run after the ruling (seed 1):** PASS, 110 judged games pass; 9 reported (6 unchecked, 2 exempt, 1 known fail).
- **Phone fit (measure-phone-fit.py --only, normal and Aa, main 233ce57 against this branch):** the gate (last option) is unchanged at every size for all four; phone-fit-state.json unchanged. Next (reported, not a gate on a phone): binomial-blaster and trig-identity-duel fit at 320/375/390 (first draft: 554 and 562 / 528 at 320, fixed by the beside-Next row); partial-fractions-duel Next 733 / 528 and 627 (its options already fail there), Aa 390 797 / 804 fits; word-problem-decoder Next 1022 / 528, 934 / 627, 905 / 804 (its options already fail at 320 and 375; at 390 Next is reachable by the reveal, not fitting): **reported, not fixed** (about 100 px).
- todo WRONG-PAUSE-UNCHECKED (covers UNCHECKED and KNOWN_FAIL); one /updates/ line.
- **Gate:** the first merge-pr.py run refused after 3600 s, "no Gate check": the PR conflicted with main (todo.md and updates/index.html, after #840 and #841), so GitHub started no PR runs (`mergeable_state` dirty). Main merged in, both sides kept (head e653f620); Gate green.
- MERGED 19 Nov as 8ab38d1 (#842) via merge-pr.py, last line "main 8ab38d1 run 44627354287: GREEN". Main on the merge commit (from the API): check-site 44627354287 success, pages build 44627353664 success, **phone-fit-full 44627354371 failure**, on the Core Maths papers only (paper1 HARD FAIL at 320 in Aa; stale entries on paper2a, 2b and 2c). **Jon, 20 Nov:** from #840's shuffle on the Core papers, not #842: the measurement is deterministic, and #840's shuffle changed Paper 1's first question; the cloud lane fixes it in #843; the home lane touches nothing on the Core papers. Cleaned up 20 Nov by end-task (run from a copy of origin/main's script). Contract moved to `docs/history/contracts/2026-11-19-wrong-pause-next.md` (closed out by TODO-TRIM's first commit).

Record: agent Claude Code; review cycles 0; amendments 0; usage n/a.

## 2026-11-19 (home): DD-VERIFIER-SHARD (Decimal Detective's verifier on ci-shards, so #837 fits the per-line limit)

Claude Code (home lane), worktree `~/mg-dd-verifier-shard`, branch `claude/dd-verifier-shard`; contract `docs/handover/contracts/2026-11-19-dd-verifier-shard.md`. Tier Small. Route 1 for #837 NEXT-IN-VIEW, whose Gate (check-site 44573475355) stopped on this verifier: 177s median + 15s setup = 192s, 71% of 270s against the 70% (189s) line limit, selected because next-control.js selects 136 verifiers.

- **`scripts/verify-decimal-detective.py`:** `# ci-shards: <same label> | | 2`; 14 units: desktop, phone 320x568, phone 375x667, phone 390x844, bank (keys plus the four bank plants), and one per page plant (9). Each check and plant runs in exactly one unit; a slice without the desktop pass reads the bank from the page first. `--list-units` works.
- **Checked locally:** full run PASS, identical to main's (45 items, 1307 answers, the same 13 self-test lines caught), 198s against 199s; --shard 1/2 PASS (7 units, 111s), 2/2 PASS (7 units, 84s), together all 14, none twice. ci-groups --selftest and --check PASS (each part 120s default, 50%, until main times its units); ci-deps --selftest PASS.
- **Report only (ci-lines over 60% of their line budget, ci-timings.json from main run 44566476211, setup 15s):** check-answer-lock.py "Answer lock, static rules and self-test" 268s + 15s of 450s (63%); verify-screening-room.py 150s + 15s of 270s (61%).
- MERGED 19 Nov as f2e6d2a (#839) via merge-pr.py, exit 0, last line "main f2e6d2a run 44580613966: GREEN". Main on the merge commit: check-site 44580613966 success, phone-fit-full 44580613885 success (both push runs), pages build 44580613026 success (all confirmed from the API). Cleaned up by end-task. Main then merged into #837 (its entry below). Contract moved to `docs/history/contracts/2026-11-19-dd-verifier-shard.md` (closed out by WRONG-PAUSE-NEXT's first commit).

