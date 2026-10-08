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
`cloud-remaining:`

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

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

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
- **word-problem-decoder (claim #173; fix PR this branch):** Jon's numbers and wording, each highlight phrase matching
  its text. gcse_059 keeps "in the box" (Jon's quote left it out; only the number changed). Verifier `check_numbers`:
  gcse_017 and 021 solved from their text (whole and positive), gcse_022 read as 3x + 4y = 33 with y = 2x, gcse_059's
  estimate = round(box / tin volume) and more than the 48 that fit; two plants (5 in all). t1-011, t1-012 (LOW) open.
- **Jon's queue after probability-paradox (8 Oct, two contracts):** screening-room (t4-005 HIGH, 006, 008, 013, 016;
  leave t4-014, 015), then factor-theorem (t5-004, 005 HIGH, 008, 018; leave t5-009, 013-017). Both verbatim in the
  session; each claimed first; relisting is the home lane's.
- **Next:** probability-paradox. Its two non-jc HIGHs (t1-001 the £20 envelope, t1-002 the bus wait) are SR-16 cases
  where the fix is a wording or key choice; t1-003, t1-004 are jc.

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
