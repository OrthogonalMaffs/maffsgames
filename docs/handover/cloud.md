# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Remaining list (contract LH, 7 Oct 2026; added by the home lane, kept by the cloud lane):** take a game off
this line in the PR that finishes it. `scripts/check-answer-lock.py` reads it. While a game is on it, a
failure of that game in the check is reported, not failed; off it, a failure fails CI.
`cloud-remaining: unit-converter`

**Lane rule, listed games (Jon, 8 Oct 2026; contract "listed-game CRITICAL/HIGH"; the home lane records it in
canon §7.8 in its next docs PR):** the cloud lane now also fixes listed games. Before starting one, add it to the
remaining list above and push that handover commit on its own, so the home lane's F1 batches skip it; take it off
in the PR that fixes it. One game claimed at a time; never claim a game already in an open home-lane F1 batch branch
(check `docs/handover/home.md` and the open PRs first; if it is, skip to the next and note it).

**Resume rule, MaffsLock (Jon, contract LH):** adopting MaffsLock includes the game's lock-hint declaration
(`<!-- maffs-lock-hint ... -->`, canon §7.6.0), and the game passes `check-answer-lock.py`. Hints live in the
game's page, never in the shared script.
A two-option game declares an `answer` that picks the option differing from its key for `i >= 1` (canon
§7.6.0, contract DET, 8 Oct; prime-or-composite is the pattern).

**Contracts (Jon, 8 Oct 2026, corrected 20:00):** each contract is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md` in its claim commit (or the PR's first commit), with one line
in the queue below pointing to it. Read it when the item starts, not at session start (the folder stays out of the
start-up load). When the work merges, move the file to `docs/history/`.

**Queue:** UC-FIX: contracts/2026-10-08-uc-fix.md and its amendment -uc-fix-amend.md (in progress, claimed 9 Oct).
Then FT-FIX: contracts/2026-10-08-ft-fix.md as amended by -ft-fix-amend.md (step 3 and t5-008 go to the home lane).
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-09 (cloud): UC-FIX, unit-converter (claimed; listed game)

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
