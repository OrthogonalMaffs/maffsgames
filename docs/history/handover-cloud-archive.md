# Cloud lane handover: archive

History only, never loaded by default (contract CTX, 8 Oct 2026). `docs/handover/cloud.md` keeps the current state
and the last three entries; older entries move here, newest first, unchanged.

## 2026-10-09 (cloud): UC-T4-007, unit-converter (claim #204; fix #205 merged 920c5b1)

- **The fix (Jon's answer 3c):** the 60 mph item reads "Convert 60 mph to m/s (1 mile ≈ 1609 m). Give your answer to
  3 significant figures."; key 26.8 m/s unchanged. t4-007 closed with the ruling.
- **Verifier:** the t4-007 NOTE is now a check: "=" before a stated conversion fails unless it is the exact
  definition; "≈" before a rounded one passes. A plant puts "1 mile = 1609 m" back and is caught (11 plants).
- **Main's run on 4081538 (SIM-S5) green**, run 583. #204's PR run: E 36 s, B3 1m32s (the plan ran few verifiers).
- **Moved to the archive:** the entries before SIM-S5's claim. Still live from them: **for the home lane**, a B5
  group before the next verifier lands in B (main's run on c9fbf4b had B4 at 5m17s of its 6m budget); move Unit Converter
  from "Hidden Count-Up" to "No Timer" in `.claude/rules/timer-policy.md` (answers 3b; it shows, logs and scores no
  clock since #196); move unit-converter to check-answer-lock's MIGRATED (it passes seeds 1-3).
  From SIM-S5 (#203): record the build freeze's one named exception (Jon, 9 Oct, 00:25: Simultaneous Solver Stage 5
  only) in canon §0.2 and the todo; the roster row could mention Stage 5.
- **Next: FT-FIX** (`contracts/2026-10-08-ft-fix.md` as amended). From the PP-T1-004 entry: merge main first;
  factor-theorem is in check-answer-lock's MIGRATED, so it must still pass; `wrapExamVocab` is the shared
  `schools/assets/exam-vocab.js:109` (step 3 and t5-008 go to the home lane, per the amendment); both
  `question_index` calls already send `qIdx + 1`; the contract's line numbers are stale (re-find by quoted text).

## 2026-10-09 (cloud): SIM-S5 built (claim #202; fix #203 takes the game off the remaining list)

- **Stage 5** in simultaneous-solver: its own screen and flow (`startForm`, beside the A-Level one); Stages 1-4
  untouched (four existing lines widened: a trailing comma, a third `MaffsNext.clear`, two test hooks). `WORDS`
  bank between markers, worded as the contract (the verifier compares it); 8 a session, 3 W and 3 E at least;
  a mark per line (16); board `foundation-s5` with its label, coverage entry and hub row (Jon's authorisation).
- **EqTiles**, the builder: self-contained (build, read, parse, mark, markAll, tokens, text; `.eqt-*` CSS), exact
  fractions; tiles are whole terms (letters, the keys' numbers, + − =, distractors); Delete and Clear line.
- **Distractors (no invention):** a spare number in the text (not 1) or a pounds amount in pence (SR-4, the
  partly-scaled error). 35 of 40 have fewer than two: for Project Claude to supply if wanted (list in the PR).
- **Feedback notes** (one line each, where the key needs a fact the words leave out): W07, W11, W12, W13, W15,
  E05, E09, E11; listed in the PR for Jon.
- **Verifier** (group E): solutions held only there; every key's forms marked by the page's own EqTiles; tiles
  build every key; 60 draws; sessions tapped at 390x844 and 1280x900; MaffsLock; 3 plants. Stage 5 adds ~30 s.
  check-answer-lock seeds 1-3 PASS. **For the home lane:** the roster row could mention Stage 5 (yours).
- **For the home lane (SIM-S5 item 9): the build freeze has one named exception, Jon, 9 Oct 2026 (00:25): Simultaneous
  Solver Stage 5 only. Record it in canon §0.2 and the todo ("Stage 5 is parked under it" no longer holds).**

## 2026-10-09 (cloud): SIM-S5 claimed (Jon's answers, 08:10)

- **Option A, approved:** a Stage 5 tile builder in simultaneous-solver, marked as a non-zero multiple of a key; the
  builder is a self-contained object (build, read, mark; no reach into Stages 1-4) so it can become a shared module.
- **Jon (9 Oct, in session): the `foundation-s5` board's three shared lines land in the SIM-S5 PR** (as the roster's
  Calculator field did in UC-FIX): its label in `schools/assets/firebase-leaderboard.js`, its entry in
  `scripts/check-leaderboard-coverage.js`'s simultaneous-solver list, its hub row in `leaderboards/index.html`.
  Additive, nothing else in those files.
- **For the home lane (answers 3b):** `.claude/rules/timer-policy.md`: move Unit Converter from "Hidden Count-Up" to
  "No Timer" (since #196 it shows, logs and scores no clock). A shared rules file, so the cloud lane does not edit it.
- **For the home lane:** unit-converter passes check-answer-lock on seeds 1-3: move it to MIGRATED (your question).

## 2026-10-09 (cloud): SIM-S5 stopped before its claim (step 3 STOP IF; answered 08:10, above)

- **simultaneous-solver has no tile UI:** Stages 1-4 are typed boxes on MaffsKeypad (`readInt` whole numbers only;
  keys 0-9, point, minus). Equation Builder's tiles are its own code (fixed slots, arrangement matching), not shared.
  Options put to Jon: **A (recommended)** a Stage 5 free-build tile builder in this game (whole-term tiles incl.
  decimals, Delete/Clear, marked as a non-zero multiple of a key); B a shared tile module first (home lane);
  C typed coefficient boxes (fixes the form; no rearranged answers). Waiting on his choice.
- **The other STOP IFs do not fire:** all 40 bank systems solve uniquely to the stated positive solution (SymPy,
  exact rationals) and each "Let..." line names both letters; a `stage5` STAGES entry, a new step in `askStep()` and
  a problem-text branch in `nextQ()` are additive, so Stages 1-4 and A-Level stay untouched.
- **For the home lane (CI):** main's run on c9fbf4b: B4 5m17s of its 6m budget (Unit Converter 78 s), B3 4m00s; the
  PR runs had B1 4m14s, B2 3m40s. The B tier is close to full: a B5 group (ci-groups.py GROUPS) before the next
  verifier lands in B.

## 2026-10-09 (cloud): UC-FIX, unit-converter (claim #195; fix #196 merged c9fbf4b, main green)

- **The fix:** MaffsLock + MaffsNext ("Got it — next", in the worked solution) with its lock hint; ?level only from
  the game's own LEVELS (hasOwnProperty); 3 s.f. stated on the cylinder, 60 mph and shaft, working as the contract
  quotes (5000π, no 3.14); "1 inch = 2.54 cm"; one `fmt()` for every displayed number (options keep their stored
  `dataset.val`), the start screen's static "1000 cm³" now "1,000"; the calculator (theme.css before the page style,
  which is neutral here; `--surface-alt` and `--hint` added to :root; "Use a calculator." on every question; badge;
  roster field `required`). t4-005: 100 per correct answer, the HUD Time item and its clock removed (nothing logged it).
- **unit-converter has migrated: the home lane can move it from NOT_YET to MIGRATED** (check-answer-lock seeds 1-3 pass).
- **For Jon, the boards (amendment's STOP IF; never delete or move scores):** `unit_converter_gcse`,
  `unit_converter_alevel`, `unit_converter_level4`; the new maximum is **2,000** (20 questions × 100). The old
  speed-weighted score also topped out at 2,000 (100 a question only at 0 s), so honest old scores sit at or below
  what is now possible; scores inflated by the t4-001 re-mark (the audit made 4,399) sit above it. t4-003 may also
  have made junk boards (`unit_converter_nonsense`, `unit_converter___proto__`, `unit_converter_l4`, ...). The
  sandbox cannot reach Firebase: Jon checks in the console.
- **Dock:** docks at 1366 and 1920, not at 1280: this game's column is 760 px (canon's reference is 720), and by
  canon's formula it docks from 1292 px. The column width is design, so left as it is.
- **For Jon and the home lane, the timer list:** `.claude/rules/timer-policy.md` lists Unit Converter under Hidden
  Count-Up ("time shown on results screen only"); the amendment takes time off the results screen too, so it now has
  no timer at all (the No Timer list). Either the list moves it (home lane's file) or Jon wants the time on results.
- **Filed, open, for Jon:** t4-007 (LOW): "1 mile = 1609 m" is not exact (1609.344); the key is 26.8 either way.
  The verifier reports it as a NOTE. The bank is **58** items (I said 59 to Jon in the session; corrected).
- **Verifier** `scripts/verify-unit-converter.py`, group B4 (79 s in CI with its self-test; B3 reached 5m51s of its 6m
  budget with it, so it moved to B4, which ran 3m25s). Reads
  marks from page classes, events through the defineProperty hook (canon §7.9), speed by a skewed Date.now (not
  Playwright's clock: it replays every animation frame, so main's rAF clock took minutes).
- **Sandbox gotchas (this container):** pip's newest Playwright wants a browser build not in /opt/pw-browsers: pin
  `playwright==1.56.0` (matches chromium-1194). `esprima` will not build here: download its sdist and put the source
  on PYTHONPATH for extract-banks/check-banks.
- **Claimed** in its own commit, with three contracts saved verbatim: UC-FIX (21:05), its amendment (23:45: t4-005 joins,
  score on correct answers only, timer hidden; Screening Room t4-017 ruled "one row per answer is correct") and the
  FT-FIX amendment (21:30, Part A). Nothing open held unit-converter (only #193, the home lane's VOCAB-IDEMPOTENT).
- **STOP IF fired, step 5 (separators), and Jon ruled (9 Oct, this session):** marking compares `dataset.val`, which is
  the displayed string itself ('1570 cm³'). Ruling: "One formatter function for all displayed numbers. Verifier proves
  marking unchanged on all 59 items and that every displayed number of 1,000 or more has a comma." Stored strings stay.
- **Keys recomputed: none wrong.** Rounded with nothing stated: cylinder, 60 mph, shaft only. Circle and pipe are exact
  under their stated "π ≈ 3.14".

## 2026-10-08 (cloud, night): probability-paradox t1-004 (contract PP-T1-004)

- **Claim #187** (with both contracts saved, first in this section, then in `docs/handover/contracts/` after Jon's
  20:00 correction). Nothing loads that folder at session start: `check-context-size.py` measures only its three
  files, and CLAUDE.md names `home.md` and `cloud.md`. The home lane was told that the heading reads "read
  `docs/handover/`".
- **The item (#189):** Jon's text exactly, in the same place (fallacy bank, after the horoscope item), with no id.
  Analytics logs only `question_index`, and the B6 ledger keys only the bus item (`ca42ff7e8e2f`), so neither
  STOP IF fired. Tier 4 `--ci` matches the ledger exactly.
- **Verifier:** `PINNED_RTM` (the one item keyed "Regression to the mean": the scenario says "the lowest scores" and "of
  the same difficulty", the four options exactly, the key). `phone()` shows the item at 390x844, asking and after
  its longest wrong option, and measures scrollWidth 390 both times. The old item is planted back whole (nine plants,
  all caught). Main's page fails naming t1-004 (and FALLACY, which no longer reviews it).
- **Next: FT-FIX.** Merge main first. factor-theorem is in check-answer-lock's MIGRATED, so it must still pass.
  **Waiting on Jon before step 3:** `wrapExamVocab` is not the game's helper. It is defined in the shared
  `schools/assets/exam-vocab.js:109` (register t5-008 says so too), which the contract's DO NOT TOUCH and the lane
  rule both exclude. Step 4 to check: on main, both `question_index` calls already send `qIdx + 1` (:1072, :1248).
  The contract's line numbers (177, 625, 780, 1046) are stale (now :817, 958, 1143, 1145); Q33 (:702) and T9 (:766)
  match the quoted text.

## 2026-10-08 (cloud, evening): Jon's rulings on the open items (spot-the-muppet, terrible-advice, word-problem-decoder)

- **Jon's rulings (8 Oct), before probability-paradox:** one PR per game, each claimed first. The loan
  (stm_core_012, ta_core_012): "6% APR"; key about £364.20 a month (total £13,111.19), APR as the effective annual rate,
  interest on what is still owed; the old keys become named distractors (£397 compound, £393.33 simple, both "on the
  whole £12,000 for 3 years, as if none of it were repaid"), "£333.33, Lenny is correct" kept. The "patients" joke becomes
  "I'm telling everyone I know to buy a bigger telly." spot-the-muppet-t2-007 ruled (not in this game). Word Problem
  Decoder: gcse_017 £136, gcse_021 £44 and £48, gcse_059 "about 61 tins", gcse_022 rewritten (3 laps then 4, 33 minutes).
- **spot-the-muppet (claim #166; fix #168):** the key in words ("the twelfth root of 1.06, minus 1", not
  1.06^(1/12): canon 7.1, no ASCII notation; the page shows options as plain text). Each distractor keeps the game's
  "Lenny is wrong — " opening; Jon's em dash after the figure became a colon. Verifier: LOAN check (APR said; the key
  states the rate, the payment and the total to the penny; one distractor per named figure with its method word), the
  joke check, two plants (8 in all). Main's page fails t2-006 and t2-008 by name. Fits 320px (no sideways scroll).
- **spot-the-muppet #168 merged** 14:16 UTC; main's full run on 7252c9d green.
- **terrible-advice (claim #170; fix #171):** "6% per year" -> "6% APR"; the same key working (opening "the 6%
  is interest, not an arrangement fee", which this item's muppet claims) and the same three distractors; the joke as
  spot-the-muppet's. Verifier: `stm.check_loan` (the one copy, in verify-spot-the-muppet.py) on ta_core_012, the joke
  check, three plants (9 in all). Main's page fails t2-005 and t2-007 by name.
- **terrible-advice #171 merged** 14:54 UTC; main's full run on 6386a07 green.
- **word-problem-decoder (claim #173; fix #174):** Jon's numbers and wording, each highlight phrase matching
  its text. gcse_059 keeps "in the box" (Jon's quote left it out; only the number changed). Verifier `check_numbers`:
  gcse_017 and 021 solved from their text (whole and positive), gcse_022 read as 3x + 4y = 33 with y = 2x, gcse_059's
  estimate = round(box / tin volume) and more than the 48 that fit; two plants (5 in all). t1-011, t1-012 (LOW) open.
- **Jon's queue after probability-paradox (8 Oct, two contracts):** screening-room (t4-005 HIGH, 006, 008, 013, 016;
  leave t4-014, 015), then factor-theorem (t5-004, 005 HIGH, 008, 018; leave t5-009, 013-017). Both verbatim in the
  session; each claimed first; relisting is the home lane's.
- **word-problem-decoder #174 merged** 15:29 UTC; main's full run on 7eaff03 green. Jon's three ruling games done.
- **probability-paradox (claim #175; fix #177; listed-games contract 6 of 23).** SR-18 applied: the
  envelope keyed "Cannot determine — it depends on how the amounts were chosen" (t1-001); the bus states random
  (Poisson) arrivals, no timetable (t1-002); Sleeping Beauty accepts 1/3 and 1/2 through an `accept` list and
  `accepted(q)` (t1-003); Two-Child and Tuesday are asked questions with equally likely outcomes (t1-006); Monty's host
  rule and the 95% test's two rates stated (t1-009, re-audit). Simulations (t1-005): Beauty counts wakings (a trial may
  return several outcomes); the bus waits for the next bus of a Poisson stream. Fisher two-sided p 0.58 (t1-007).
  MaffsLock, MaffsNext on a wrong answer, hint (starts Paradox Predictor); t1-010 CRITICAL (score again on the revealed
  key) and t1-011 (mode on every event) filed and fixed. **t1-004 (HIGH, jc: "the test was easier") left open for
  Jon.** Verifier `scripts/verify-probability-paradox.py` (group E, ~1 min; ~8 min with the self-test, 8 plants).
- **Gotcha (again):** editing an item's text changes its content id, so a ledger entry on it (here B6's "wait"
  false positive on the bus item) goes stale and Tier 4 fails; `check-changed.py` does not run Tier 4. After any bank
  edit: `extract-banks.py --only <slug>` then `check-banks.py --only <slug> --write-ledger`.
- **probability-paradox #177 merged** 16:30 UTC; main's full run on dc0f22c green.
- **screening-room (claim #181; fix #183; unlisted, Jon's SR-21 contract + t4-015 ruling + Project
  Claude's note, 8 Oct).** MaffsLock and MaffsNext, hint (plays all three phases). **Gotcha: `fresh(gameScreen)` does
  not undo a lock held by a container inside it** (the gut options, the answer row, Next): fresh each locked container
  when it renders, or the second question's gut check is ignored. t4-006 own levels only (`hasOwnProperty`). t4-008
  (PC's rule): over 10,000, k = gcd(N, condition, TP, FP) if N / k fits 10,000, else the least whole k that fits with
  a group's remainder as one part-icon (`data-part`, CSS gradient); a note gives k in the item's `unit` and every exact
  count. t4-013 phases stack (column). t4-015 phase 3 keeps phase 2 on screen (Continue hidden). t4-016: fixed on main
  by #92 (bf3aa90); pinned with plants; its analytics part filed as t4-017 (LOW, open: own code, one row per answer,
  two answers a question; one row a question is a data change for Jon). t4-014 open (pools).
  **screening-room has migrated: the home lane can take it off NOT_YET** (passes check-answer-lock seeds 1-3; the
  cloud lane does not edit that script). Verifier gains open_page/extra_checks; run it WITHOUT the KaTeX shim (its
  async route handler hangs this verifier's sync page loads). **Without KaTeX the sandbox missed a real phone fault**
  (CI caught it: the A-Level Bayes formula, rendered, is up to 519 px wide); measure phone fit with KaTeX routed by a
  sync handler (`page.route(... lambda r: r.fulfill(path=...))`). Fixed: KaTeX lines scroll inside their box.
- **Main went red at 16:46 (home #180: verify-like-terms-collector, "item 1: typed 8.9/6.5, marked correct=None";
  Check marked nothing within 5 s, so the click itself, not the read); the failed job's re-run passed (17:40). Not
  reproduced with a 200 ms gap after every Playwright action (3 runs). The home lane holds contract MAIN-RED for it.
- **Factor Theorem (Project Claude, 18:35):** go ahead. **The alevel board: checked by Jon, 8 Oct 18:52:
  leaderboards/factor_theorem_alevel is null (nothing ever submitted): record "checked: empty" in the PR; that STOP IF
  cannot trigger.** (The sandbox cannot reach Firebase.) level4: no hub change
  while unlisted (NOT_ON_HUB skips the level check); the home lane's relist adds both levels.
- **#183 merged 18:13; main's run on 8ead626 red on group E's time budget** (10m03s of 12m, budget 9m; every
  verifier passed: today's joiners Probability Paradox 105 s, Screening Room 84 s, Spot the Muppet 69 s, Terrible
  Advice 56 s). Fixed by each verifier's own header: Probability Paradox to B1, Spot the Muppet to B2 (both ran about
  2m50 of 6m). **A new cloud verifier: pick a B group with room, not E.**
- **CHECKPOINT (Jon, 8 Oct ~19:00, context over 60%): STOP once main is green after the group fix.** Nothing claimed
  after it. The next session starts with probability-paradox t1-004.
- **Both contracts are now saved in the repo** (Project Claude, 19:55; queue above): PP-T1-004, then FT-FIX, which
  replaces the two lost Factor Theorem contracts. #180 closed t5-009, so merge main first. The alevel board is
  empty and level4 needs no hub change (both above).

## 2026-10-08 (cloud, afternoon): CHECKPOINT STOP (Jon's queue done): listed-games contract at 5 of 23; nothing claimed

- **Jon's queue for this session is done:** spot-the-muppet (#155), word-problem-decoder (#157), terrible-advice
  (#160), then the Correlation or Coincidence contract (#163, 84 items). All merged on a green Gate, main green after
  each. The remaining list above is empty: **no game is claimed.**
- **Next game: probability-paradox.** Claim it first, in a PR of its own on main (canon 7.8.2). Check the open PRs and
  `docs/handover/home.md` first, and claim one game at a time.
- **The rest of the order:** core-maths-paper2c, core-maths-paper2b, wrong-on-the-internet, higher-power,
  prisoners-dilemma, coordinate-geometry-dash, surd-simplifier, scale-factor-scaling, unit-converter, formula-forge;
  then boolean-blitz, matrix-crunch, complex-converter, eigenvalue-extractor, characteristic-quest. **Skip 52dle and
  seven-bridges:** the home lane's F1 batch 5 (#161) holds them.
- **Per game, as for the first five:** claim PR; read its open register entries and the game; a verifier that fails on
  main naming the entries; MaffsLock with its lock hint; a scoring change beyond the named fault, or new data, goes to
  Jon; `check-changed.py`; PR; fill the register's PR number; merge on green, 10 min clear of a home merge; watch main.
- **Waiting on Jon:** the two loan keys (spot-the-muppet-t2-006, terrible-advice-t2-005: the convention to state);
  spot-the-muppet-t2-007 (the slip is terrible-advice's only; the register has no "not in this game" status); the
  two "patients" jokes (t2-008 / t2-007); word-problem-decoder t1-006..008 (new numbers or wording).
- **This checkpoint trimmed this file** (contract CTX: current state and the last three entries; check-context-size.py
  holds it to 20 KB). The older entries are in `docs/history/handover-cloud-archive.md`. Its DEFERRED entry for this
  file is removed in the same PR, as the entry itself said to do at this checkpoint.
- **Gotchas this session:** `pkill -f` / `pgrep -f` on a pattern that is in your own command line kills your own shell
  (exit 144). Kill a background run by its task id, or match a pattern your command does not contain. In this
  sandbox, `check-changed.py` fails the teacher line (and, when `cloud.md` changes, the answer lock parts) only on
  KaTeX games, because the KaTeX CDN is refused. CI has KaTeX.

## 2026-10-08 (cloud, afternoon): correlation-or-coincidence, 84 items (Jon's contract, 8 Oct)

- **#160 (terrible-advice) merged** 12:46 UTC, after main's red run on #158 (five KaTeX games in answer lock L1; #158's
  own PR run had passed) went green on the home lane's re-run. Claim #162.
- **The 42 items** (A15-A28, B15-B28, C15-C28; Project Claude's and Jon's, the jokes Jon's) appended exactly as
  pasted, each block with its own header comment after A14, B14 and C14; every pasted line is in the page byte for
  byte. 84 items, 28 of each kind. `MIN_BANK = 84` in the verifier, nothing else changed there (a copy with C28
  removed fails "bank has 83 items, the minimum is 84").
- **Every new graph's r inside its band** at its n and whole-number settings (the PR lists all 42). Closest to an
  edge: C27 (strong, n = 8, x whole 0-4) r = 0.928 of [0.80, 0.94]. No STOP IF fired: phone fit at 320/375/390 for
  every item (asking screen and wrong-answer feedback); SR-14 clean; a session of 10 played at 390x844 by real taps,
  the real MaffsNext floor (no sideways scroll, Next above the footer every time, one game_completed).
- **Register:** no bank-size entry exists for this game; nothing to close.
- **For the home lane:** Jon may want an /updates/ line ("Correlation or Coincidence now has 84 questions"): his
  call, not this PR. The home lane's F1 batch 5 (#161) holds 52dle and seven-bridges, both on the listed-games list:
  the cloud lane skips them.

## 2026-10-08 (cloud, afternoon): terrible-advice (listed-games contract, 5 of 23)

- **#157 (word-problem-decoder) merged** 12:18 UTC; main's full run on 2c846ac green. Claim #159 merged 12:26.
- **The same format as spot-the-muppet, its own engine** (a point for a right first pick only; kept). MaffsLock as
  spot-the-muppet: a first wrong pick marks and logs nothing; the question is marked and logged once; finishOnce;
  Play Again a screen change; the same two-wrong-picks hint (seeds 1, 2, 7 pass).
- **Fixed:** t2-001 gcse_006's "Prudence is correct — upper bound is 2.45m" (true, keyed wrong) -> "Prudence is wrong
  — upper bound is 2.49m"; t2-002 core_002 as spot-the-muppet's; t2-003 core_007 (the weighted mean is 70% too): the
  key says she got the right answer this time but her method is wrong, the distractor is "Wendy is correct in both
  method and answer" (the pattern of gcse_008 and gcse_012); t2-006 the key's "£500 × 1.1249 = £562.43" -> "× 1.124864";
  t2-008 the key's "Square roots always have a positive and negative solution" -> "because (−5)² = 25 as well"; filed
  and fixed t2-009 (core_004's working: 1.05 × 20 = 21.05) and t2-010 (HIGH: core_004's simple-interest option true as
  written, as spot-the-muppet-t2-001).
- **Verifier** `scripts/verify-terrible-advice.py` (group E, ~70 s with the self-test) imports spot-the-muppet's
  arithmetic (`# ci-deps: scripts/verify-spot-the-muppet.py`), which this PR extends: every vulgar fraction (⅖ was read
  as a whole number at 0 d.p. and matched ⅚); pounds against pence ("£4.80 ÷ 400 = 1.2p/g"); a rounded intermediate
  ("1,000 × 1.05²⁰ = 1,000 × 2.653") passes only between two expressions and only for a decimal not in the advice, so
  a slip on a given (t2-009) or at the last step (t2-006) still fails. Main's page fails t2-001..004, 006, 008, 009, 010
  by name; six plants.
- **Left open (for Jon):** t2-005 the loan key (simple interest on the whole £12,000 for 3 years, about £393/month; a
  repayment loan is about £364.20/month), with spot-the-muppet-t2-006: both need a stated convention (APR effective
  monthly, or a flat-rate loan). t2-007 the "patients" joke (SR-14 tier (c) vs a joke).
- **spot-the-muppet-t2-007** (562.45 vs 562.43, filed against both games) is terrible-advice's slip only; spot-the-
  muppet's key was always right. The register has no status for "not in this game": Jon's call (ruled, or removed).
- **For the home lane:** terrible-advice passes the lock check: add it to MIGRATED. The two games share one engine
  shape in two copies; a shared module would be the architectural fix (not this lane's).

## 2026-10-08 (cloud, afternoon): word-problem-decoder (listed-games contract, 4 of 23)

- **#155 (spot-the-muppet) merged** 11:51 UTC; main's full run on 6232248 green. Claim #156 merged 12:00.
- **The category scheme (SR-18: one scheme, both accepted where both fit):** `PARENT_TOPIC` in the game: Reverse
  Percentage is a kind of Percentages, Standard Form a kind of Number & Place Value (the KS3 bank, which offers
  neither kind, keys ks3_013, ks3_015 and ks3_023 under the parent), so a phrase keyed the kind is right under the
  parent too (t1-003, t1-004). A phrase's own `also` lists any other topic that genuinely fits: ks3_006 phrase 2
  (t1-001) and gcse_017 (t1-002), plus six found on the re-audit (t1-010: ks3_022, ks3_046, gcse_013, gcse_022,
  gcse_039, gcse_060 phrase 2). `acceptedTopics(hl)` marks; after a pick, every topic that fits and is on the buttons is
  revealed. **The judgement on each `also` is listed in the PR for Project Claude** (it is content).
- **t1-005, MaffsLock:** `lock(optionsGrid)` first in handleAnswer; `fresh(optionsGrid)` per phrase; the advance
  timers through MaffsLock.timer (the ~1 s auto-advance after a wrong answer is kept: the audit's class 7, "not counted
  as a fault"); finishOnce; Play Again a screen change. Hint `{}`: the generic driver plays it (seeds 1, 2, 7).
- **t1-009 (the 3 uncounted MEDIUMs) closed by the re-audit:** every phrase read against the 23 topics; filed t1-010
  (HIGH, fixed), t1-011 (LOW, open: three items refer to a figure the game never shows) and t1-012 (LOW, open: two Aa
  buttons).
- **Verifier** `scripts/verify-word-problem-decoder.py` (group E, ~5 s; ~15 s with the self-test): bank shape; every
  phrase played in Chromium with each topic it accepts and three it does not on the buttons (getDistractors replaced
  for the test), so the marking is tested whatever the page's code; `ACCEPT` holds every second topic with its reason;
  answer once; the session ends once. Main's page fails t1-001..005 and every t1-010 phrase by name; three plants.
  **Gotcha:** the sweep renders each phrase itself, so it drops the game's own setTimeout advances (they would fire
  mid-sweep and move it on).
- **Left open (MEDIUM, wording or numbers: for Jon / Project Claude):** t1-006 gcse_017 and gcse_021 have no
  whole-number answers (c = 71/19; a = 170/19); t1-007 gcse_059 says 48 tins is "too high" but 48 fit exactly
  (6 × 4 × 2), and 72000 ÷ (π × 25 × 15) is 61.1, not 48; t1-008 gcse_022's lap count is ambiguous.
- **For the home lane:** word-problem-decoder passes the lock check: add it to MIGRATED.

## 2026-10-08 (cloud, afternoon): spot-the-muppet (listed-games contract, 3 of 23); session queue

- **Jon's queue for this session (8 Oct):** spot-the-muppet, word-problem-decoder, terrible-advice; then the
  Correlation or Coincidence contract (42 new items, 42 -> 84, MIN_BANK = 84; Jon's text and items arrived 8 Oct, the
  items verbatim in `docs/handover/cloud-coc-items-2026-10-08.js` until that PR appends them and deletes the file);
  then CHECKPOINT: next game probability-paradox, not claimed.
- **Claim #154** (merged 11:3x UTC, main green).
- **spot-the-muppet (this PR):** t2-001 core_004's advice says "compound interest" and the simple-interest option
  claims to be the answer (£1,000 + 20 × £50 = £2,000, false for compound); t2-002 core_008's "£120 − £20 = £100" ->
  "£120 × 1.20 = £144"; t2-003 ks3_005's "(2+10) ÷ 2 = 6" -> "(3+7+8+2+10) ÷ 4 = 7.5"; t2-004 core_002's advice no
  longer makes the valid marginal argument (it compares the extra £1.30 with the whole £3.50, which proves nothing);
  t2-009 (filed here) core_004's working said 1,000 × 1.05 × 20 = 21,050 (it is 21,000).
- **t2-005, MaffsLock:** the two-pick retry is kept (score unchanged: a right second pick still scores 1). A first
  wrong pick marks and logs nothing (the card is disabled, a fresh window opens); the question is marked and logged
  once, when right or at the second wrong pick (spot-the-error's pattern). So question_answered is now one row per
  question (before: a first wrong pick logged its own row). Every timer through MaffsLock.timer; finishOnce; Play
  Again is a screen change. Lock hint: two different wrong picks. `check-answer-lock.py --game spot-the-muppet`
  passes at seeds 1, 2, 7.
- **Verifier** `scripts/verify-spot-the-muppet.py` (group E, ~70 s with the self-test): every equation chain in the
  advice and the keys evaluated (a muppet's deliberate wrong sum is in MUPPET_SUMS); every key recomputed (KEYS) or
  reviewed (CONCEPT), so a new item cannot skip review; no distractor ends on the key's value as the key writes it
  (SR-16); every item played three ways; Next's second click, a real double click, a double click on a first wrong
  pick, the end once. Main's page fails t2-001..005 and t2-009 by name; six plants caught. **Gotchas:** a whole
  number under 10 in a key never stands for a non-whole value ("not 1" is not 0.665); the first piece of an
  equation chain after "of" / "year" or glued to a word ("cos⁻¹(") is a fragment, not a value.
- **Left open (MEDIUM; for Jon):** t2-006 core_012 (the loan key's £14,292.19 total and ≈ £397/month are compound
  growth, not a repayment loan: about £364.20/month at 6% APR; the verifier reports it as KNOWN_OPEN and fails once
  it is fixed and not removed), t2-008 (the "patients" joke, SR-14 tier (c) vs a joke: Jon's call).
- **Seen, not filed (for Project Claude):** gcse_006 Prudence's method "add 5 to the last digit" is keyed correct by
  the key's own reasoning "adding half the degree of accuracy"; the words don't say the same thing.
- **For the home lane:** spot-the-muppet passes the lock check: add it to MIGRATED.
- **check-changed.py:** all green but the teacher line, which fails only on factor-theorem and log-laws (KaTeX CDN
  refused in this sandbox, the known gotcha), not on this game.

## 2026-10-08 (cloud): CHECKPOINT STOP (Jon): listed-games contract at 2 of 23; nothing claimed

- **Where the contract stands (Jon's listed-games contract, 8 Oct):** both listed CRITICALs are closed.
  trig-wars (#148, merged, main green) and gradient-hunter (#152; its entry below). The remaining list above is
  empty: **no game is claimed.** The session stopped at Jon's checkpoint without claiming the next game.
- **Next game: spot-the-muppet.** Start with a claim PR on main (canon 7.8.2, #145): check the open PRs and the home
  handover first, claim one game at a time, the fix PR takes it off the line.
- **The rest of the order, after spot-the-muppet:** word-problem-decoder, terrible-advice, probability-paradox,
  core-maths-paper2c, core-maths-paper2b, wrong-on-the-internet, 52dle, higher-power, prisoners-dilemma,
  seven-bridges, coordinate-geometry-dash, surd-simplifier, scale-factor-scaling, unit-converter, formula-forge;
  then boolean-blitz, matrix-crunch, complex-converter, eigenvalue-extractor, characteristic-quest.
- **Per game, as done for the first two:** claim PR; read its open register entries and the game; a verifier
  that fails on main naming the entries (group E has room: trig-wars ~45 s, gradient-hunter ~15 s); MaffsLock with
  its lock hint; a scoring change beyond the named fault, or new data, goes to Jon (gradient-hunter t2-003 did);
  `check-changed.py`; PR; fill the register's PR number; merge on green, 10 min clear of a home merge; watch main.
- **Earlier today (all merged, main green):** truth-buster #143; expectation-station #146 (Stage 1 one completion,
  40/40/40; ready to relist under SR-21).

## 2026-10-08 (cloud): gradient-hunter (listed-games contract, 2 of 23; the second CRITICAL); #148 merged

- **#148 (trig-wars) merged** 09:50 UTC; main's full run on b8691f8 green. Claim through main: #149 (merged 09:58).
- **t2-001 (CRITICAL):** MaffsLock locks the options at the first pick (the revealed correct option re-scored without
  limit). A wrong answer now waits for MaffsNext (canon 7.6; it moved on at once before); a right answer keeps its
  own Next, locked at the press; every question opens a fresh window on the game screen (the canvas included);
  `finishOnce`; Play Again opens the menu with `MaffsLock.screen` (the menu has the leaderboard link, as
  partial-fractions-duel's did). The KaTeX wait for the method reference is `// lock-ok:`.
- **t2-002:** the three stated tangents are the DRAWN curve's: a cardinal spline's slope at a plotted point is its
  neighbours' gradient, whatever the tension: 4.5 (was 5), 110 (was "a steeper gradient of 150"; the audit's 98.0 is
  the ideal exponential, not what is drawn, and 110 is LESS steep than the 116.7 chord) and 3.25 (was 4).
- **t2-003, filed and fixed (Jon's ruling, 8 Oct, option A):** a Calculate item scored a point for the gradient
  whatever the student did (the game showed it once the two points were clicked). Now the student types it after
  the two points: `MaffsAnswer.fractionOrDecimal` against the chord through the points clicked (`chordGradient`:
  exact rise/run; "to 2 decimal places" only when it recurs, so -9/80 is asked as -0.1125); that earns the point,
  clicking scores nothing, the working (rise / run) follows, the interpretation is unchanged. One question_answered
  per item, as before (the interpretation's). A text keyboard on phones (`inputmode="text"`: iOS's decimal pad has
  no minus): the shared MaffsKeypad is styled by theme.css, which this game has not migrated to, so it joins the
  todo 3.21 list (home lane: the keypad comes with its theme migration).
- **Verifier** `scripts/verify-gradient-hunter.py` (group E, ~9 s): chords from their points, stated tangents from the
  spline, one true interpretation (an "instantaneous/marginal ... is V" option is keyed right exactly when V is the
  tangent; a plain "is V" claims V to the hundredth, "about V" at V's places), every item played, the typed gradient
  on all 27 Calculate items, answer once and Next once (~15 s). Main's page fails t2-001 on six items, t2-002 on four
  claims and t2-003 on all 27; three plants caught.
  **Gotchas:** read numbers with thousands separators; a fall's interpretation gives its size; MaffsNext takes focus,
  so an Enter after a wrong pick advances (test the option with clicks, not the keyboard). **Never write a shared
  asset's file name (theme.css, keypad.js ...) in a game page, even in a comment:** `ci-deps.py --selftest` (b) reads
  a page that mentions it as one that loads it, and the PR's Plan job fails (#152's first run).
- **For the home lane:** gradient-hunter passes the lock check: add it to MIGRATED.
- **Next:** spot-the-muppet (the first of the audience order): claim PR first (not claimed: checkpoint stop).

## 2026-10-08 (cloud): trig-wars (listed-games contract, 1 of 23; first CRITICAL); #146 merged

- **#146 (expectation-station) merged** 08:56 UTC; main's full run green. **The claim went through main** (#147,
  merged 09:03): under #145 the home lane reads the line on main, so a listed game's claim is its own small PR.
- **Jon's ruling (8 Oct):** 2 PLAYER submits nothing (two people on one device; SR-22). VS CPU scores Player 1 only.
- **Fixed, all six entries (t2-001 CRITICAL, t2-002 HIGH, t2-003..006 MEDIUM):**
  - t2-001: hits and shots per side; VS CPU logs and scores Player 1's shots only, submitted win or lose;
    2 PLAYER logs both sides and submits nothing. Events carry `mode` (analytics rule for multi-mode games).
  - t2-002/005: the panel's Vx, Vy are V cos/sin in V's own units (no "u/s"; 0.28 stays internal).
  - t2-003: one physics (`newShell`/`stepShell`/`simulateShot`) for the flight, the advice and the check's aim; a hit
    is tested along each frame's segment before the ground. The old test missed 3.4% of true hits, half
    ground-first, half a fast shell crossing the circle between frames.
  - t2-004: the quip says only how it missed; `missAdvice()` suggests a change only if the physics says it lands
    at least 1px nearer (a 45-degree rule was wrong on 38% of misses: the hill; a 0-px gain was floating-point
    noise at the field's edge).
  - t2-006: four lines replaced (new wording in the PR for Project Claude).
- **MaffsLock:** FIRE locks per side (the slider rows are `data-maffs-lock-skip`, so a player can aim during the
  other turn); every timer through `MaffsLock.timer`; `finishOnce`; `shotId` stops a flight still animating after a
  reset. Lock hint: i = 0 fires `aimAtEnemy()` (a sure hit), i >= 1 fires 85 deg / 20 (a sure miss).
  `check-answer-lock.py --game trig-wars` passes (judged in full). Its note "no Next after a wrong answer" stands:
  after a miss the turn passes to the opponent (not in the register).
- **Verifier** `scripts/verify-trig-wars.py` (group E, ~45 s with the self-test): its own copy of the physics in
  Python; plays three battles, 252 panel settings, both kinds of missed hit, and near misses either side of 45 deg.
  Main's page fails on all six entries; three plants caught. **Harness gotchas:** run animation frames
  synchronously (a flight is ~150 chained frames; `setTimeout(0)` clamps to 4 ms); read the miss message by
  wrapping the page's `msg()` (the game clears it before a poll sees it); wrap `mfg` once per page.
- **Not changed:** the phone width (711px at load in CI's font, allowlisted, todo §3.9 batch 19).
- **For the home lane:** trig-wars passes the lock check: add it to MIGRATED.
- **Next:** gradient-hunter (the second CRITICAL): claim PR first.

## 2026-10-08 (cloud): expectation-station, Stage 1 one completion and 40/40/40 (Jon's bundle contract); #143 merged

- **#143 (truth-buster) merged** 08:10 UTC on a green Gate, after merging main (#144, contract DET, landed 07:58 while
  #143's CI ran: truth-buster's hint passes DET's lock check, seed 1, twice). #141 closed as superseded.
- **Claimed** in its own commit (58e19a0), off the line in this PR.
- **The bundle** (Project Claude, 7 Oct; Jon's ruling B), applied by script, verbatim: the 33 items get their sentence
  appended to the context and prepended to the explanation; 75 new items (core 021-040, gcse 016-040, alevel 011-040).
  Each level serves min(session length, bank), so 40 each.
- **Verifier:** `COUNTS` 40/40/40; the bundle's CARDS and FIGURES; `FIGURES_ADDED` (the 33 items' new opening claims);
  `CLUES` for all 120; **Stage 1 uniqueness**: every placement of the tiles into the missing cells is tried, and exactly
  one may sum to 1 and satisfy the CLUES entry, the keyed one. A CLUES ratio, difference or E(X) must also be in the
  context's own words (so a CLUES entry cannot claim what the student is not told). Fourth plant: es_core_001 without
  its sentence, CLUES ('none',): caught. Main's page fails 38 items on Stage 1, plus the counts. Runs in about 10 s.
- **Found by the uniqueness check, not in the bundle:** es_gcse_006, es_gcse_014, es_alevel_003, es_alevel_008 and
  es_alevel_010 have equal keyed values, so the bundle gave them ('none',), but a second pair of tiles also summed to
  the gap. **Jon's ruling (8 Oct, approved by Project Claude):** one stray tile changed on each (1/6 -> 1/8,
  0.35 -> 0.40, 0.3 -> 0.4, 0.30 -> 0.35, 0.25 -> 0.30). No new wording.
- **Added here, not in the bundle:** ten definition-only FIGURES entries ("Let P(X = a) = p and P(X = b) = q",
  es_alevel_021-030), like the existing "k + 2k + ... = 1" entries.
- **es_alevel_006** (approved by Project Claude, 8 Oct): its context said only "a batch of 4", so x = 1 and x = 4
  could swap (0.2916 and 0.0001 both fit the sum). It now ends "Each item is defective independently with probability
  0.1."; CONTEXT requires those words and the table to be exactly B(4, 0.1). Cards and explanation unchanged.
- **Phone:** the context is `.context-text` (textContent, no clamp); every one of the 120 measured unclipped at 390x844.
- **Register:** pc-001 fixed; no other entry open. **Ready to relist (SR-21, home lane): no CRITICAL or HIGH open.**
- **Ledger:** 40/40/40 made the three B4 (bank size) entries stale, which failed Tier 4 on the first CI run.
  `extract-banks.py --only <slug>` then `check-banks.py --only <slug> --write-ledger` cleared them (no other rule
  fired on the 75 new items). **Any bank change: run both before the first push** (`check-changed.py` does not run Tier 4).
- **Next:** Jon's listed-games contract (8 Oct): trig-wars first, then gradient-hunter.

## 2026-10-08 (cloud): truth-buster (queue 6 of 6, the last); the remaining list is empty

- **State found:** the previous session's closing note (partial-fractions-duel next) predated #139; #139 and the relist
  (#142) had merged and main's full run on a99efa5 was green. Only truth-buster was left.
  **Missed at the start: #141** (the previous session's truth-buster PR, the same cherry-pick) was already open. #143
  duplicated it; #143 was merged (its lock hint has no fixed wait, the cause contract DET names) with #141's fuller
  t3-016 (375x667 too), and #141 closed as superseded. **Check the open PRs, not only main and this file, at the start.**
- **truth-buster:** the old session's commit (fcc5e4c, `claude/keen-cray-ypsime-truth-buster`) cherry-picked onto main
  cleanly: MaffsLock in full (no `S.answered`; Next locks at its first press; the tier transition and the Next delay
  through MaffsLock.timer; finishOnce), and on a phone the answer buttons fold away during the reveal and the page moves
  Next above the footer. Added here: its maffs-lock-hint. **Two options: it presses the button that differs from the
  key, so every attempt is wrong.** Without it the generic driver came out all right on 8 draws in 1 run of 3 here
  (UNPLAYABLE), the fault contract DET names. Off the remaining list.
- **Proofs:** `verify-truth-buster.py` passes; against main's page it fails 62 times (the double Enter at the tier
  boundary, t3-013; Next under the fold at 390x844 on all 60 items). `check-answer-lock.py --game truth-buster` passes
  four times with the list empty (judged in full; 20 answered, 0 right, the same every run); `--selftest` passes.
- **Register:** t3-013 fixed. t3-015 stays open (the 21 Learn More video IDs: YouTube is refused here); its fold part is
  fixed at 390x844, and 320x568 is filed as **t3-016** (MEDIUM, open: 32 of 60 fit; the reveal is taller than the
  screen, so it needs shorter reveal text or a layout ruling; 375x667: 58 of 60). t3-014 (levels, class 4/5) stays open.
- **For the home lane:** truth-buster passes the lock check: add it to MIGRATED.
- **Next:** Jon's contract of 8 Oct (listed games' CRITICAL/HIGH, trig-wars first) runs after the **Expectation Station
  bundle contract**, whose text this session has not received.

## 2026-10-07 (cloud): partial-fractions-duel (queue 5 of 6); #138 binomial-blaster merged; NEXT = truth-buster

- **#138 merged** at 20:53 on a green Gate; main's full run on b10d3db green.
- **partial-fractions-duel:** the old session's commit (9a19235) cherry-picked onto main (Jon's alevel[22]:
  1/(x(x+1)(x-2)), find C, keyed 1/6; distractors -1/2 = A, 1/3 = B, -1/6 the sign slip; MaffsLock; the B3 duplicate
  cleared), plus its maffs-lock-hint (`{}`) and off the remaining list.
- **The two lock-check reports were one fault, in the game:** Play Again calls `showMenu()`, and at 1280x900 the menu's
  "Global leaderboard" link sits under the button, so the second click of a double click opened /leaderboards/.
  That page then threw "firebase is not defined" (the check blocks the Firebase CDN). `showMenu()` now calls
  `MaffsLock.screen()` on the menu (the shared API's own screen-change call; nothing shared edited). The verifier tests
  a real double click and Play Again then the link and Start; a fourth plant (the old showMenu) is caught.
  `check-answer-lock.py --game partial-fractions-duel` passes, twice. Filed as t5-011 (class 1), fixed.
- **For the home lane, two findings outside this lane:**
  - **The same Play Again shape is in 25 games** (`function showMenu(){show('menu')}` with a `/leaderboards/` link on
    the menu): angle-ace, bearing-blitz, binomial-blaster, characteristic-quest, circle-theorem-spotter,
    coordinate-geometry-dash, curling-friction, dimension-checker, eigenvalue-extractor, eigenvector-engine,
    force-resolver, formula-forge, formula-unlocked, graph-transformer, matrix-crunch, moments-master,
    normal-navigator, probability-paradox, proportion-blaster, scale-factor-scaling, sequence-solver,
    standard-form-blitz, surd-simplifier, trig-identity-duel, unit-converter. The check's Play Again test is a
    double click at one point, so it catches the fault only where a control happens to sit under the button
    (binomial-blaster and trig-identity-duel pass it with the same code). A layout-independent test (Play Again,
    then a click on every menu control within the window) would find all of them.
  - **/leaderboards/ throws when the Firebase SDK does not load** (a school network that blocks gstatic.com):
    `leaderboards/index.html:159` calls `firebase.database()` unguarded, so the whole script stops, including the
    device-local "Your Scores" section. firebase-leaderboard.js guards the same case (`typeof firebase`).

## 2026-10-07 (cloud): binomial-blaster (queue 4 of 6); #137 trig-identity-duel merged; NEXT = partial-fractions-duel

- **#137 merged** at 20:21 on a green Gate. Its first L1 run failed on fraction-equivalence, the second home-lane
  two-option game to do so (prime-or-composite on #134): the shared check's wrong-answer search is not deterministic
  for a two-option game. Passed on the one re-run; commented on #137 with the architectural fix (pick the wrong option
  from the game's data, or seed Math.random as tier 1's PHONE_SEED does). **For the home lane: it will keep failing
  PRs at random until fixed.**
- **binomial-blaster:** the old session's commit (67bf685) cherry-picked onto main, plus its maffs-lock-hint (`{}`), the
  method reference's KaTeX wait (:253) marked `// lock-ok:`, and off the remaining list. Jon's alevel2[36]:
  3/((1+x)(1-2x)) = A/(1+x) + B/(1-2x), find B, keyed 2 (distractors 1, -2, 3); the old item (1/((1+x)(1-x)), B = 1/2)
  was right but duplicated another (B3 ledger entry cleared, no register entry). MaffsLock in full.
- **Register:** t5-017 (class 1) fixed. t5-018 (class 4, shared level resolver) and t5-022 (wording) stay open.

## 2026-10-07 (cloud): trig-identity-duel (queue 3 of 6); #135 truth-will-set-you-free merged; NEXT = binomial-blaster

- **#135 merged** at 19:47 on a green Gate (main green on 571bb60; last home merge 18:44).
- **trig-identity-duel:** the old session's commit (03c34eb) cherry-picked onto main, plus its maffs-lock-hint (`{}`)
  and off the remaining list. Jon's gcse[16]: A = 45°, a = 10 cm, B = 60°, b = 12.2 (the old item, B = 30° keyed 7.1,
  was right but duplicated another question: the B3 ledger entry is cleared, no register entry). Hidden count-up
  (timer-policy, SR-23): no HUD timer, a right answer scores BASE whatever the time, time on the results only.
  MaffsLock in full.
- **Register:** t2-007 (class 1) and t2-010 fixed. Every other entry was already fixed by #102.
- **Not in its register, not fixed here:** a wrong answer still moves on by itself after 1 s (MaffsLock.timer), with
  no Next (canon 7.6). The lock check notes it ("no Next after a wrong answer"); it does not fail.

## 2026-10-07 (cloud): truth-will-set-you-free (queue 2 of 6); #134 eigenvector-engine merged; NEXT = trig-identity-duel

- **#134 merged** at 19:16 on a green Gate. Its first L1 run failed on prime-or-composite, a home-lane game the PR
  did not touch: `answer_wrong()` taps option (k+1) % 2 on 8 unseeded draws, and after a right answer `to_next()`
  waits a fixed 350 ms ('auto'), so a tap can land in the next question's 300 ms fresh window and be dropped. It
  passed 5 of 5 locally and on the one re-run. Commented on #134; the fix is the home lane's (shared check, or an
  `answer` in prime-or-composite's declaration). **For the home lane.**
- **Old branches:** this session's git proxy refuses any push but its own branch, deletes included, so the
  `claude/keen-cray-ypsime-<game>` branches cannot be deleted from here. Jon (or the old session) deletes them.
- **truth-will-set-you-free:** the old session's commit (7b07e09) cherry-picked onto main, plus:
  - [27], approved by Project Claude (7 Oct): "This expression can be written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B
    (XOR: one or the other, but not both). Play Boolean Blitz →", in KaTeX. XOR is introduced nowhere else in the
    game, so a form using it carries `identity` and `gloss`; the verifier checks the identity is true, the gloss, and
    the rendered line (a third plant, XOR with no definition, is caught).
  - Contract LH: its maffs-lock-hint (a wrong table, every cell the opposite of its key, then Submit; on the
    expression step the first option) and off the remaining list. `check-answer-lock.py --game` passes in full, twice.
    Its Next is replaced on each render (btnRow), so the hidden-button double advance eigenvector-engine had is absent.
- **Register:** t6-001, -002, -003, -005 fixed; t6-006 filed and fixed ([6]'s distractors A + B·C and (A + B)·(A + C)
  are equal by the distributive law; class 2, LOW); t6-004 (class 5, bank size) stays open.
- **Queue state (each prepared in a worktree, verifier passing on its branch and failing on main):**
  trig-identity-duel (`/home/user/tid-wt`, hint `{}` committed), binomial-blaster (`bb-wt`, hint `{}` and :253's KaTeX
  wait `// lock-ok:` committed), partial-fractions-duel (`pfd-wt`: needs a hint; the lock check here also reported
  "dblclick on Play again: its second click answered the first question" and "firebase is not defined", neither of
  which reproduces in a direct Chromium probe without the KaTeX shim: settle on CI, where it is judged in full),
  truth-buster (`tb-wt`: needs a hint with an `answer`; the generic driver finds no wrong answer; plus the MEDIUM
  320x568 entry, canon 7.6.1).

## 2026-10-07 (cloud): eigenvector-engine (queue 1 of 6); #130 Factor Theorem merged; NEXT = truth-will-set-you-free

- **#130 merged** at 18:22 on a green Gate (main green on b7e634b; last home merge 17:43). Main's run on d337b0b watched.
- **eigenvector-engine:** the old session's commit (3394734, from `claude/keen-cray-ypsime-eigenvector-engine`)
  cherry-picked onto main. It already adopts MaffsLock in full (newSession, lock, fresh, timer, finishOnce; no local
  flags), so the class-1 entry t6-002 closes. One addition here: `check-answer-lock.py` (on main since #129, after the
  commit was written) found a raw `setTimeout(buildExample, 300)` on load; it draws the start screen's worked example
  and marks nothing, so it carries `// lock-ok:`. Static rules pass.
- **Found here, fixed (class 1, part of t6-002):** `check-answer-lock.py --game eigenvector-engine --not-yet` (KaTeX
  served) reported "question_index jumped" on the old page every run. Instrumented: the worked solution's "Got it —
  next" was a plain onclick, only hidden after use, so a second Enter in the same frame (about 10 ms apart in the
  tap-through) ran closeSol() twice and skipped a question unseen. Now MaffsNext.wrong (canon 7.6; next-control.js
  loads before answer-lock.js), label kept. The verifier checks a real double click and two activations in one task
  (two Enters in one frame); a third plant (the old onclick) is caught. Python's separate key presses never land in
  one frame, so a keyboard test of this needs the in-page double activation.
- Verifier passes on the branch, fails on main's page (QS[22], [23], [24]); all three plants caught. The tap-through
  passes on the fixed page.
- **Register:** t6-001, -002, -004, -005, f0-001..007 fixed; t6-003 (class 5) stays open.
- **TWSYF is ready in `/home/user/tw-wt` (branch tw-local):** [27] uses Project Claude's approved wording (7 Oct):
  "This expression can be written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B (XOR: one or the other, but not both). Play
  Boolean Blitz →", in KaTeX. XOR is introduced nowhere else in the game; the verifier checks the identity, the gloss
  and the rendered line, and a third plant (XOR with no definition) is caught.
- **Contract LH (#133, home lane, merged 18:44) landed while this was being prepared:** eigenvector-engine declares
  its maffs-lock-hint (`{}`: the generic driver plays it) and comes off the remaining list above, so CI now judges it
  in full. Each later game does the same in its own PR.
- **Delete each `claude/keen-cray-ypsime-<game>` branch once its game has merged (Jon).**

## 2026-10-07 (cloud): game 18 Factor Theorem (PR #130, merged); NEXT = merge #130, then the six queued games

- **New instance, fresh container (18:00 UTC).** The old worktrees and `/home/user/queue-patches/` were gone. Jon
  approved the old session pushing the six queued games to their own branches; this lane picks each up from its
  branch, one PR per game, under the usual merge rules. Do not rebuild them.
- **Jon's rulings (7 Oct, 18:00):**
  - **The lane question:** #130 does not edit `scripts/check-answer-lock.py`; the home lane moves cloud-lane games to
    MIGRATED. #130's MIGRATED and HINTS edits were dropped when main (#132) was merged in (the file is main's,
    byte for byte). The two in-game fixes stay: suvat loads answer-lock.js after next-control.js, and factor-theorem's
    resize debounce carries `// lock-ok:`. **The home lane will move per-game hints into each game's own file under a
    coming contract: build nothing around the central HINTS.** The two driving hints the old session wrote and
    passed with, as data for the home lane (suvat: Level 4, the equation is picked, then a wrong typed answer;
    factor-theorem: the Practice tab, a wrong answer in every box, Check pressed until the scaffold's three attempts
    are used):

```python
    # suvat (Level 4: pick the equation, then type the answer; question_answered fires on the typed answer).
    # The answer waits out MaffsLock's 300 ms window on the real clock before it presses CHECK.
    'suvat': {
        'level': 'level4',
        'ready': "document.getElementById('mainGame').classList.contains('visible')",
        'answer': ("return (async () => {"
                   "  const vis = id => { const e = document.getElementById(id); return e && e.offsetParent !== null; };"
                   "  const real = ms => new Promise(r => { const t = performance.now(); (function f() {"
                   "    if (performance.now() - t >= ms) r(); else requestAnimationFrame(f); })(); });"
                   "  for (let k = 0; k < 60; k++) {"
                   "    if (vis('phase2') && !document.getElementById('calcInput').disabled) {"
                   "      await real(350); document.getElementById('calcInput').value = '9999';"
                   "      document.querySelector('#phase2 .calc-btn').click(); return; }"
                   "    const b = [...document.querySelectorAll('#eqChoices .eq-btn')].find(e => !e.disabled && e.dataset.val === currentQ.equation);"
                   "    if (vis('phase1') && b) { await real(350); b.click(); }"
                   "    await real(60);"
                   "  }"
                   "})();"),
        'surface': '#phase2',
    },
    # factor-theorem: the Practice tab; a wrong answer in every box, Check pressed until the question is marked
    # (a scaffold has three attempts).
    'factor-theorem': {
        'start': "document.querySelector('[data-section=\"practice\"]').click()",
        'ready': "document.getElementById('sec-practice').classList.contains('active') && !!document.getElementById('checkBtn')",
        'answer': ("return (async () => {"
                   "  const real = ms => new Promise(r => { const t = performance.now(); (function f() {"
                   "    if (performance.now() - t >= ms) r(); else requestAnimationFrame(f); })(); });"
                   "  await real(350);"
                   "  for (let k = 0; k < 3; k++) {"
                   "    const c = document.getElementById('checkBtn');"
                   "    if (!c || c.style.display === 'none') return;"
                   "    document.querySelectorAll('#practice-area input.answer-input:not([disabled])').forEach(e => { e.value = 'zz'; });"
                   "    c.click();"
                   "  }"
                   "})();"),
        'surface': '#practice-area .q-card',
    },
```

  - **Factor Theorem scaffold:** keep "every value of the blanks that makes the line true" (Q6 also takes -2, -3).
  - **Truth Buster:** Next below the fold at 320x568 is filed as an open MEDIUM register entry citing canon 7.6.1;
    it does not block the fix PR.
  - **TWSYF [27]:** keep XOR only if the game introduces it before [27]; otherwise rewrite with AND/OR/NOT and list
    the wording in the PR for Project Claude.
- **The queue after #130, in order (one PR each; register entries to close):**
  1. eigenvector-engine: t6-001, -002, -004, -005, f0-001..007 fixed; t6-003 stays open.
  2. truth-will-set-you-free: t6-001, -002, -003, -005 fixed; file and fix t6-006 ([6]'s duplicate distractor);
     t6-004 stays open.
  3. trig-identity-duel: t2-007, t2-010.
  4. binomial-blaster: t5-017.
  5. partial-fractions-duel: t5-007.
  6. truth-buster: t3-013; file the 320x568 Next entry (above).
- **Each later game loads answer-lock.js:** under #131 it is reported, not failed. Run `check-answer-lock.py --game
  <slug>` (with KaTeX served) before each PR and give the home lane what it finds, in the PR and here.
- **Factor Theorem (unchanged from the PR):** typed answers looked up in ACCEPTED (canon 7.1 pattern, R12), written by
  `scripts/verify-factor-theorem.py --write` (E): one box per blank, matched by position; numbers via MaffsAnswer;
  algebra through canon(). Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5)). Q24/Q38/Q20 asks, Q22 hint,
  Learn ex. 4 candidates, test prompts' raw TeX (t5-019, new). MaffsLock. Open: t5-004/-005 (free text), -008/-009
  (exam-vocab.js), -013 (4), -014/-015 (design), -016/-017 (5), -018 (MaffsNext advance: check-teacher-invite's
  FT_STEP clicks only `.next-q-btn`, home lane).
- **Gotchas:** MaffsLock's 300 ms fresh window drops clicks a sweep makes right after a render: set
  `MaffsLock.FRESH_MS = 0` in sweeps and keep the real window in the lock test. A double click must be tested with
  `page.mouse` at the control (clicking a detached element twice fires its old listener). A fresh container has no
  KaTeX: fetch `registry.npmjs.org/katex/-/katex-0.16.9.tgz` (its `package/dist`). A `sitecustomize.py` on
  PYTHONPATH that adds a KaTeX route to every new context lets the teacher-line and answer-lock checks pass, but it
  makes every verifier that routes for itself (sync API: suvat, factor-theorem, check-resit-page) time out on `load`.
  Run those bare, with `--katex-dir` where the verifier has it.

## 2026-10-07 (cloud): game 17 SUVAT Selector (PR #128); #127 Force Resolver merged; NEXT = factor-theorem

- **Force Resolver (PR #127) merged** at 16:15 on a green Gate; main green after #126 before it.
- **SUVAT Selector:** every typed step marked by MaffsAnswer (`exact`, or `decimal` at the step's stated `dp`; the
  prompt says the precision; phase 0 to 2 d.p.); local parseFloat-and-tolerance gone (t5-006). Keys recomputed both
  ways: from the exact data, and from the values the student is shown (rounded chips, the previous step's key); a
  step's precision is the finest at which both round to the key (al[32] 1 d.p., al[18] 2 d.p., al[41]/[48] whole
  numbers, al[49] 1 d.p.; t5-007). Project Claude's sprinter (u = 8; t5-001) and ALEVEL[39] (2.02 s, 19.8 m/s;
  t5-003). v_y keyed -0.32 (t5-002); ALEVEL[22] says it lands at 3 s (t5-008); a question counts correct only if
  every typed step is (t5-009); wrong answers show the answer and wait for MaffsNext; ALEVEL[3]'s second root
  explained (t5-011). **MaffsLock (#125) adopted (Jon, 7 Oct 17:30):** lock first in every answer handler,
  fresh() on every render, MaffsLock.timer for every delay, endGame through finishOnce, newSession on Start;
  t5-004 closed. `scripts/verify-suvat.py` (E) adds the class-1 test (double click + Enter on CHECK mark once,
  two equation choices count once, one submit). Open: t5-005 (4), t5-010 (5).
- **Standing rule from Jon (7 Oct 17:30): MaffsLock is on main; every game fixed from now on adopts it and closes
  its class-1 entries in the same PR.** `check-answer-lock.py` (F1 part b) is not on main yet, so each verifier
  tests the lock itself.
- **Next: factor-theorem** (worktree `/home/user/ft-work`, branch claude/ft-prep, findings read, no edits):
  ACCEPTED-list typed answers (R12) and Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5) any order);
  t5-004/-005 (free text) and t5-008/-009 (exam-vocab.js, shared) stay open and get listed.

## 2026-10-07 (cloud): game 16 Force Resolver (PR #127); #126 Moments Master merged; NEXT = suvat

- **Moments Master (PR #126) merged** at 16:01 on a green Gate; main green after #124 before it.
- **Force Resolver:** `scripts/verify-force-resolver.py` (E), the Moments Master verifier's shape plus: options written
  as expressions evaluated (25 root 3 N, 10 tan 30 N) and a rounded figure counted equal to the expression it rounds
  from (43.3 N beside 25 root 3 N); figures quoted in text keys recomputed (FIGS) and their verdict required
  (VERDICT: "Yes", it slides). Project Claude's truss for level4[18] (12.8 kN) exactly. From the items' own data:
  level4[8] 1.40 m/s^2 (t5-002), alevel[47] 5 N (t5-004), alevel[32] "Yes" (t5-007), level4[7] worked with the
  stated 9.81 (1224 N; t5-011), alevel[31] "Equilibrium" (t5-012), alevel[35] g stated (t5-013); value-equal
  distractors replaced by named errors (t5-005, t5-006, f0-001, t5-014: 50 root 3, 1 N, "Undefined (tan 90)", 2.5 N,
  4.33 N, 266 N; for review); the given trig values stated where a key used them (alevel[11], level4[1]); 49.8 not
  49.7 (level4[15]). Wrong answers show the answer and working, then MaffsNext. Open: t5-008 (1), t5-009 (4),
  t5-010 (5).
- **Prepared locally, not pushed:** suvat (`/home/user/sv-work`, branch claude/sv-prep): typed steps on MaffsAnswer
  at a stated precision (the finest at which the exact data and the values shown both round to the key: al[32] 1 d.p.,
  al[18] 2 d.p., al[41]/[48] whole numbers), Project Claude's sprinter and ALEVEL[39], wrong answers wait for Next,
  a question correct only if every typed answer is; `scripts/verify-suvat.py` (E).

## 2026-10-07 (cloud): game 15 Moments Master (PR #126); #124 Linear Equation Solver merged; NEXT = Force Resolver

- **Linear Equation Solver (PR #124) merged** at 15:47 on a green Gate, after main's runs following #122 (re-run;
  the first attempt lost its Gate job in GitHub's 15:05-15:17 write errors) and #123 were green.
- **Moments Master:** `scripts/verify-moments-master.py` (E): every numeric key from the item's own data (SymPy;
  KEYS), distractors equal in value to the key (5 kW = 5000 W) or to each other, named-error REASONS for the items
  rewritten, numeric claims in keys and working lines, "Same beam" items quoting their predecessor, text keys pinned
  (REVIEWED, --print-pins); Chromium at 390 and 320: every option clicked, no raw TeX, no sideways scroll. Project
  Claude's data for :128, :134, :147, :172/:173 exactly; :141 rekeyed 75 N; :180's 5 kW replaced by 524 W
  (P = 2 pi N T / 60 with 100 taken as rpm; for review). Filed and fixed: t5-014 (premises: the trapdoor uniform,
  the level4 cable beam light with a vertical cable), t5-015 (R_B, T_A shown raw by textContent: ctx and ask now
  through MaffsText). Wrong answers show the answer and the item's working line, then MaffsNext (no stored
  explanations exist: fuller ones would be Project Claude content). Open: t5-009 (1), t5-010 (4), t5-011 (5),
  t5-012 (the gate premise: Jon).
- **Prepared locally, not pushed:** Force Resolver (`/home/user/fr-work`, branch claude/fr-prep). suvat is planned
  (typed answers onto MaffsAnswer with a stated precision per step; keys from the values the student is shown).

## 2026-10-07 (cloud): Linear Equation Solver, Jon's "optimal move" contract (PR #124); #115 Proof Builder merged; NEXT = moments-master

- **Proof Builder (PR #115) merged**; main's full run after it green (and after #117).
- **Jon's list (7 Oct, this session):** proof-builder (done), linear-equation-solver, then with Project Claude's
  replacement data moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, then
  truth-will-set-you-free; then (Jon, 15:27) follow-ups to merged games, one PR each: trig-identity-duel gcse[16]
  replaced + timer to hidden count-up; binomial-blaster alevel2[36] replaced; partial-fractions-duel alevel[22]
  replaced (each clears its B3 ledger entry); truth-buster Next visible at 390x844 on every item. The replacement
  data is in Jon's 7 Oct paste (the session's first message); if it is not to hand, ask Jon.
- **MaffsLock (`schools/assets/answer-lock.js`) is not on main yet:** class 1 stays open. Once it lands, adopt it in
  each game fixed (lock, fresh, timer, finishOnce) and close that game's class-1 entries.
- **Linear Equation Solver:** `scripts/gen-linear-moves.py` (depth-3 search, iterative deepening, under 1 s) writes
  MOVES between its own GENERATED markers: per line, every optimal move (one per distinct line), one slower move
  where one exists, named errors (one-side, carry, xonly, constnot) to fill four. Options show the move and the line
  it gives with the number side unevaluated (x = 12 - 7), so a one-side error can be shown and the answer phase
  still asks for the value. The trail follows the student's route (295 lines for 141 questions). Amber = 12.5 (half
  the 25 at stake), streak kept; amber and red wait for MaffsNext. Hints and feedback through MaffsText (t4-002).
  `gen-linear-equations.py` no longer writes the superseded per-step `opts`/`hint` (QUESTIONS otherwise identical)
  and uses a repo path. `scripts/verify-linear-equation-solver.py` (group E, ~40 s): its own TeX parser and search,
  SymPy for every value; every option clicked in Chromium; Jon's four cases tapped; page == generator. On main's
  file it fails on exactly r-001 (18 options in the 14 questions), r-002 (49) and t4-002 (11).
  - **Decision to review:** "fractions" in the tie-break means fractional constants, not coefficients (Jon's own x2
    example on x/2 + 5 = 11 needs x/2 = 6 to count as fraction-free). Under that reading every keyed move is
    optimal (STOP IF not triggered).
  - Four lines (-x = c in U1-U4) have 3 options: no fourth honest one exists.
  - Open: t4-003 (class 1).
  - **Gotcha (MOVES size):** the first version stored each option's feedback sentence (MOVES 280 KB, page 348 KB)
    and tier 4's extraction of this one game ran for minutes: the render-site evaluator calls `literal_to_json` on a
    literal every time it resolves an identifier (about 350 calls a second, no cache). Options are now compact arrays
    and the page words the feedback from their fields (MOVES 92 KB, page 159 KB, extraction 8.5 s). A large
    generated literal in any game will hit the same cost.
- **For the home lane:** content group B4 ran 243 s on main's run after #117, over canon's 4-minute cap; this
  verifier went in E (133 s on that run) instead. `bank_common.literal_to_json` is re-run per identifier
  resolution; memoising it by node would make large literals cheap (shared code). SR-13's scoring sentence
  ("scores full marks") needs a note for Jon's 7 Oct amber rule.

## 2026-10-07 (cloud): game 13 Proof Builder (PR #115); #112 Dimension Checker merged; NEXT = Linear Equation Solver (Jon's 7 Oct contract)

- **Dimension Checker (PR #112) merged** on a green Gate; main's full run after it green.
- **Proof Builder (PR #115):** `scripts/verify-proof-builder.py` (B4, declared by its own `# ci-line:` header; no workflow edit): refutation predicates for every counter-example option, SymPy induction stages, sorter orders, rendering at 390px. One renderer `M()` and 79 strings migrated to `\( \)` (132 B7 + 2 B11 ledger entries cleared). The options' TeX test is written as `includes()` at each call site, because tier 4 cannot decide a helper (`isTeX(v)`) and crashes on a regex `.test()` (game 8's note). Open: t5-014, t5-016 (1), t5-021 (5), t5-023 (per-mode boards: Jon), t5-024 in part (4).
- **Main went red once after #109** (13:16): group E, Like Terms Collector item 1, the same failure as on #106 and #88's first run (third time today). One re-run of the failed job was green. It does not reproduce here (0 of 24 runs, 8 at a time; this sandbox has Playwright 1.56 and no gstatic, CI has 1.63 and both). Home lane: the verifier hardening proposed on #106.
- **Original contract list done.** Everything left open is a shared class (1, 4, 5, B11), a decision for Jon (TID timer, Integration Duel + c, Proof Builder per-mode boards, Truth Buster fold), or needs new content (duplicate items in TID, BB and PFD; Truth Buster video IDs to check from home). Skipped until Project Claude supplies data: moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free.
- **Next: Linear Equation Solver** (Jon's contract of 7 Oct, added after Proof Builder): "What is the optimal move here?", every tied optimal move full marks, a valid but slower move amber (half, streak kept), wrong options named real errors; option sets generated by `scripts/gen-linear-moves.py` (depth-3 search) between GENERATED markers; the verifier re-derives every class with SymPy; the SR-13 note in canon.

## 2026-10-07 (cloud): game 12 Dimension Checker (PR #112); #109 Curling Friction merged; NEXT = Proof Builder

- **Curling Friction (PR #109) merged** on a green Gate; main's full run after it green.
- **Dimension Checker (PR #112):** `scripts/verify-dimension-checker.py` (B4, declared by its own `# ci-line:` header; no workflow edit): dimension algebra for keys, options and every worked step; MaffsOptions, MaffsNext. Open: t5-003 (1), t5-005 (5), t5-006 (4).
- **Next:** Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 11 Curling Friction (PR #109); #107 Integration Duel merged; NEXT = Dimension Checker

- **Integration Duel (PR #107) merged** on a green Gate; main's full run after it green.
- **Curling Friction (PR #109):** `scripts/verify-curling-friction.py` (B4): exact targets per item; no negative "speed"; friction only on sliding stones; MaffsNext. t5-008 filed and fixed. Open: t5-003 (1), t5-004 (4), t5-005 (5).
- **CI lines (Jon, 7 Oct):** from when contract V merges (home lane), a cloud-lane verifier declares its CI group
  with a `# ci-line:` header in the verifier file itself, and the PR does not edit `.github/workflows/check-site.yml`
  at all. Until then: one workflow line per PR, and rebase on main before merging.
- **Next:** Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 10 Integration Duel (PR #107); #106 Differentiation Duel merged; NEXT = Curling Friction

- **Differentiation Duel (PR #106) merged** on a green Gate; main's full run after it green.
- **Integration Duel (PR #107):** `scripts/verify-integration-duel.py` (B4): antiderivatives checked by differentiating, c held as a symbol, ln x + c sampled where it is right. Missing + c named in feedback (Jon may rule it right). B11 (5) cleared. Open: t5-010 in part (class 4).
- **Like Terms Collector's verifier flaked once on #106** (group E; item 1 typed 8.9/6.5, `MARK()` null, empty feedback;
  it passed 5 of 5 locally and on the one re-run). Same item and shape as #88's first-run flake. Home lane: after
  `page.fill`, wait for the boxes to read the typed values and for the feedback panel's class before reading the mark.
- **#103 split content group B into B1-B4**; the cloud lane's verifiers go at the end of B4, where #103 put them.
  A branch prepared before a ledger change on main conflicts on `data/check-ledger.json`: take main's ledger and
  replace only that game's record (the scratch helper did this per commit).
- **Next:** Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 9 Differentiation Duel (PR #106); #105 Partial Fractions Duel merged; NEXT = Integration Duel

- **Partial Fractions Duel (PR #105) merged** on a green Gate; main's full run after it green.
- **Differentiation Duel (PR #106):** `scripts/verify-differentiation-duel.py` (B4): implicit items compared on the curve; explanations must state the answer. B11 (9, five of them added by #99) and B7 (1) ledger entries cleared; t5-013/014 filed and fixed. Open: t5-010, t5-011 (class 4).
- **Next:** Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 8 Partial Fractions Duel (PR #105); #104 Binomial Blaster merged; NEXT = Differentiation Duel

- **Binomial Blaster (PR #104) merged** on a green Gate; main's full run after it green.
- **Partial Fractions Duel (PR #105):** `scripts/verify-partial-fractions-duel.py` (B4): every Find solved from its stated form; valid equivalent forms removed. Open: t5-007 (class 1), t5-009 (class 4). New B3 ledger entry: the Find B / Find C pair for 1/(x(x+1)(x-1)) now share stem, options and key (needs a new item).
- **The tier 4 crash recorded under game 6 has a known cause (home lane: shared code).** `_SiteEval.regex()` in
  `bank_common.py` returns `(pattern, glob)`, and the `.test` branch of `_SiteEval.call()` calls `.search` on that
  tuple, so any `/re/.test(x)` the evaluator reaches raises. Taking the pattern from the tuple fixes it. Also: a
  guard written as a page helper (`isTeX(v)`) is never decided, so both branches count; until the evaluator can
  look inside, the cloud lane writes such guards as `includes()` at the call site.
- **Next:** Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 7 Binomial Blaster (PR #104); #102 Trig Identity Duel merged; NEXT = Partial Fractions Duel

- **Trig Identity Duel (PR #102) merged** on a green Gate; main's full run after it green.
- **Binomial Blaster (PR #104):** `scripts/verify-binomial-blaster.py` (B4): three-term estimates as the ask states, rounding-ambiguity check, MaffsOptions. Open: t5-017 (class 1), t5-018 (class 4), t5-022 in part (portal card: home lane). One B3 duplicate (needs a new item).
- **Next:** Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 6 Trig Identity Duel (PR #102); #101 Component Crusher merged; NEXT = Binomial Blaster

- **Component Crusher (PR #101) merged** on a green Gate; main's full run after it green.
- **Trig Identity Duel (PR #102):** `scripts/verify-trig-identity-duel.py` (B2): every option read into SymPy. Compound-angle keys, 85.9°, identical options fixed; t2-011 filed and fixed. Open: t2-007 (class 1), t2-010 (timer: Jon's decision). gcse[16] duplicates gcse[12] (B3; needs a new item).
- **For the home lane (shared code, not edited here):** `bank_common.py`'s render-site analysis crashes
  (`AttributeError: 'tuple' object has no attribute 'search'`, in `call`) on a regex literal's `.test()` in some
  positions: inside a template-literal expression (Component Crusher's first CI run) and `/[\\^_{}]/.test(...)`
  (Proof Builder, found locally). Extraction then fails and every ledger entry reads as stale. The cloud lane works
  round it in each game (a named function, or string methods); the parser fix is the home lane's.
- **Local tier 4 in the cloud sandbox works:** serve KaTeX from the npm tarball (route the jsdelivr KaTeX URLs to
  `package/dist`), run `extract-banks.py`, then `check-banks.py --ci`; about 95 s with 4 workers.
- **Next:** Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 5 Component Crusher (PR #101); #100 Expectation Station merged; NEXT = Trig Identity Duel

- **Expectation Station (PR #100) merged** on a green Gate; main's full run after it green.
- **Component Crusher (PR #101):** `scripts/verify-component-crusher.py` (B2): keys from what is shown, diagrams measured from the canvas, marking through MaffsAnswer. Level 4 data shown; prompts' maths in `\( \)` (31 B7 ledger entries cleared). Open: t4-005 (class 1), t4-011 (class 5), t4-014 in part (class 4).
- **Next:** Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 4 Expectation Station (PR #100); #98 Trig Worms merged; NEXT = Component Crusher

- **Trig Worms (PR #98) merged** on a green Gate; main's full run after it green.
- **Expectation Station (PR #100):** `scripts/verify-expectation-station.py` (B1): all 180 Stage 3 cards reviewed with checks from the distribution ("most" = more than half); Stage 1 marked exactly. t2-001..016 fixed, t2-018/019 filed and fixed; open: t2-017 (class 1).
- **Next:** Component Crusher, Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 3 Trig Worms (PR #98); #97 Truth Buster merged; NEXT = Expectation Station

- **Truth Buster (PR #97) merged** on a green Gate; main's full run after it green.
- **Trig Worms (PR #98):** `scripts/verify-trig-worms.py` (group B2, ~20 s). The generator is rebuilt from a
  `POOL` of servable outcomes (1,204; no retry); every outcome is recomputed with mpmath from the values shown,
  at the stated precision ("to the nearest degree", "to 1 decimal place"); every distractor is a named error and
  the feedback names it; only the two given sides are labelled and the triangle is drawn at one scale.
  t1-001..t1-004 fixed; nothing left open.
- **Next:** Expectation Station, then component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker,
  proof-builder (all prepared on local worktrees /home/user/*-work, not pushed; their PR texts and register
  specs are in this session's scratchpad).

## 2026-10-07 (cloud): game 2 Truth Buster (PR #97); #96 Spot the Error merged; NEXT = Trig Worms

- **Spot the Error (PR #96) merged** on a green Gate; main's full run after it green.
- **Truth Buster (PR #97):** `scripts/verify-truth-buster.py` (group B1). Keys are reviewed judgements, with the
  words a statement must contain for its key to hold (`needs`, SR-18) and SymPy where a key can be computed;
  every reveal figure is in `FIGURES` (an unlisted `=`, `<`, `>` fails); dates and counts in `SOURCED`.
  t3-001..012 fixed. Open: t3-013 (class 1), t3-014 (class 5/4), t3-015 in part: the 21 Learn More video IDs
  (YouTube is refused from the cloud sandbox: check them from home) and Next below the fold (shorter reveal
  text, Project Claude, or a layout ruling).
- **Next:** Trig Worms, then expectation-station, component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker (all
  prepared on local worktrees /home/user/*-work, not pushed), then proof-builder (in progress). A lost container
  loses them: redo from the register.
- **Gotchas:** a PR that clears a fixed B7/B11 finding also clears its entry in `data/check-ledger.json` (dump
  with `indent=1, ensure_ascii=False, sort_keys=True`, as `check-banks.py` does), or CI fails it as stale. With a
  workflow edit, `check-changed.py` selects every check (about 45 minutes here): run it in the background with a
  long timeout, never the default 30 minutes (the Truth Buster run was cut off there).

## 2026-10-07 (cloud): unlisted-games contract, game 1 Spot the Error (PR #96); NEXT = Truth Buster

Jon's contract of 7 Oct (cloud lane): fix the unlisted games one per PR, each under a new verifier, in this order:
spot-the-error, truth-buster, trig-worms, expectation-station, component-crusher, trig-identity-duel,
binomial-blaster, partial-fractions-duel, differentiation-duel, integration-duel, curling-friction,
dimension-checker, proof-builder. Shared classes stay open: 1 (answer lock, F1), 4 (?level resolver, F2),
5 (bank size), B11 parser gaps (F0). Skipped until Project Claude supplies data: moments-master, force-resolver,
suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free. Other owners: linear-equation-solver,
screening-room, glorious-gantt.

- **Spot the Error (PR #96):** `scripts/verify-spot-the-error.py` (group B2, ~9 s). All 19 register entries
  fixed (t1-001..014 plus the re-audit's t1-015..019); nothing left open. 16 items reworded (listed in the PR
  for Project Claude). Model: the key is the first step that departs from correct working; later steps carry it.
- **Prepared on local branches, not pushed** (worktrees under /home/user/*-work, gone with this container): the
  next games are rebuilt from their audit entries in the same order. If this container is lost, redo from the
  register; the PR descriptions list the content choices.
- **Gotchas:**
  - A reviewed verdict (a step judged an error, a statement judged true) reads no text, so each verifier that
    holds verdicts pins each item's content hash (`REVIEWED`, `--print-pins`): any edit fails until re-reviewed.
  - The self-tests count a plant as caught only by a check other than that pin.
  - Locally, the KaTeX CDN is refused: KaTeX games' verifiers take `--katex-dir` (the npm tarball's dist/).
    `check-changed.py` here always fails seven checks for environment reasons (PR #96 lists them).
  - `extract-banks.py` through the sandbox wrapper reports component-crusher's 34 B7 entries stale even on main:
    do not trust a local tier 4 run for B7; read CI's.
  - A shared TeX-to-SymPy reader would serve several of these verifiers (each carries its own small one, since
    the cloud lane does not add shared modules): a home-lane candidate.

## 2026-10-07: the lane starts (written by the home lane, which set up the lanes)

- No cloud session has run since the lanes were split. The last cloud work was 6 Oct 2026 (#85 audit tranches 1-2
  and two games unlisted; #86 Core Maths Paper 1), recorded in CLAUDE.md's history.
- The unlisted games and their open findings: `docs/audits/REGISTER.md` ("By game", Listed = unlisted) and the
  roster's Unlisted section. Each has its relist checklist in `docs/todo.md` §1.53-§1.75.
- **Next:** Jon's first cloud-lane contract names the game.
