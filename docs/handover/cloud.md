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
`cloud-remaining: `

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

**Queue:** VERIFIERS-20 (12 Oct, contract `docs/handover/contracts/2026-10-12-verifiers-20.md`): 20 verifiers, one game per PR; 1 prime-or-composite DONE (#282); 2 fraction-equivalence DONE (#283); 3 percentage-flip DONE (#284); 4 factor-race DONE (#285); 5 prime-factorisation DONE (#286); 6 think-of-a-number DONE (#287); 7 formula-plug-in DONE (#290); 8 four-quadrant-explorer in PR; next 9 new-shapes.
UC-FIX: DONE, #196 merged 9 Oct (c9fbf4b), main green.
SIM-S5: DONE, #203 merged 9 Oct (4081538). UC-T4-007: DONE, #205 merged 9 Oct (920c5b1; the answers' item 3c, in
`docs/history/contracts/2026-10-09-sim-s5-answers.md`; claim #204). FT-FIX: DONE, #207 merged 9 Oct (cf96929; contract, amendment and Jon's answers
of 9 Oct, 11:00, in `docs/history/contracts/2026-10-0[89]-ft-fix*.md`).
LISTED-HIGH: COMPLETE (contract, rulings and notes now in `docs/history/contracts/2026-10-09-listed-high*.md`):
#210-#212, #214, #216, #217, #219, #223, #225-#231 merged; main green (run 654, 37978742832). Item 12 closed on
Jon's ruling of 22:45 (option A): see the PD-CLOSE entry below. CAR-TRAP-DRAFT (moved from the home lane, Jon 20:17; contract on main,
`contracts/2026-10-09-car-trap-draft.md`): **Car Trap draft for Jon's review**, #235 merged (ba5b6b2); main green
(run 661). **CAR TRAP HAS MOVED ENTIRELY TO THE HOME LANE (Jon, 10 Oct), including #242 (CAR-TRAP-BUILD): the cloud
lane does not push to #242 or touch any car-trap file.** #242's state at hand-over is in its branch's
`docs/handover/cloud.md` (the CAR-TRAP-BUILD entry). It is red only on the teacher page at 320 px (§1.37). The new
art was not on main when Jon said it was: the only `car-trap-*.webp` there are the old pictures.
**QUEUE (Jon, 10 Oct), in order. Keep the handover current after each:**
Done 10 Oct: RIGHTFUL-KING-DRAFT (#247, aa660f7) and LIBRARY-DRAFT (#248, 8302ba8). Jon approved both drafts in
full ("spot on"); the Library room's title is The Library Jam.
1. **RIGHTFUL-KING-BUILD: DONE.** #257 merged 10 Oct (79165de); main's run 723 is green. The contract is now in
   `docs/history/contracts/`. Jon can play-test the room at `/escape-rooms/rightful-king/play.html`.
2. **LIBRARY-JAM-BUILD: DONE.** #262 merged 10 Oct (5f4f656); main's run 736 is green. The contract is now in
   `docs/history/contracts/`. Jon can play-test the room at `/escape-rooms/library-jam/play.html`. CI passed its
   teacher page under the §1.37 entry (recorded at 538 px, measured in the cloud container).
**THE CLOUD QUEUE IS EMPTY (11 Oct).** RK-STICKY-NOTE done (this PR). Ask Jon for the next item.
**Jon's ruling for both builds (10 Oct, after 13:45):**
- **The hub is left alone.** A built room sits behind its noindex holding page, and the checker counts a room as
  live only without `noindex`, so no card is needed. The star chip comes with the release contract.
- **Every lock gets a `grade` in room.js**, with a one-line reason in the PR, as #253 did.
- **The derived rating must be ★★★ (Rightful King) and ★ (Library Jam).** If honest grading gives anything else,
  STOP and report; never adjust a grade to fit.
- **Calibration from #253:** building powers to find the years (Prom's compound growth) is 5; a Venn overlap from
  totals is 4.
**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's
last full run is green, without asking each time. It still watches main's run after each merge.
**FONT-FIT: DONE.** #256 merged 10 Oct (a2dbdeb); main's run 720 is green. The contract is now
`docs/history/contracts/2026-10-10-font-fit.md`; the findings are in `docs/audits/font-fit-2026-10-10.md`.
- Free Daily Pizza and Negative Number Line both fit at 320x568 with **14 px** to spare (Next and Confirm at 514
  against 528), by layout only. Their verifiers assert `MARGIN = 8`.
- **Known problems, for Jon to order** (in the findings file; not fixed, not allowlisted):
  - Over the fold: standard-form-blitz +10, surd-simplifier +9, coordinate-geometry-dash +7, sequence-solver +4 and
    modular-battle +2 (320x568); estimation-golf +12 (390x844).
  - Too wide: distinctly-average, +14 px (its Aa toggle).
  - Within 5 px of the fold: proportion-blaster, prime-or-composite, higher-power, matrix-crunch, trig-worms and
    wrong-on-the-internet.
- **Lesson:** the cloud container's Chromium (1194) lays out 1 px differently from CI's (1243). parents/fractions
  measured 320 here and 321 in CI, so the allowlist keeps it at 321. **CI is the measure for a 1 px verdict.**
  Locally, Playwright 1.63 runs through scratch symlinks to build 1194 (`/opt/pw-browsers/*-1243`), with
  `FONTCONFIG_FILE` pinning DejaVu.
- **For the home lane:** CI's DejaVu pin step can now be retired for the phone checks (not removed: the workflow is
  home-lane).
**Open for Jon:** delete branch `claude/youthful-feynman-anpxuq-pd-check` in GitHub (the proxy refused the remote
delete, HTTP 403).
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-12 (cloud): VERIFIERS-20 game 7, formula-plug-in (#290, merge commit d31a12a)

- **Verifier:** `scripts/verify-formula-plug-in.py`: all 50 items against ten formulas held in the verifier (variables, result variable, rule):
  key from the item's own values with Fraction (whole numbers); `formulaKatex` read as maths and worked with the values; every working step has the
  formula's left-hand side and is worth exactly the key; the substitution step uses the formula's numbers plus the values only; last step is
  "LHS = key"; sessions of 10/20/30 dealt 3 times; every item shown by `loadQuestion()` (formula TeX read from KaTeX's annotation, variables line,
  prompt) and answered on the numpad in Chromium (key right; key +-1 and the usual slips wrong, with "the answer is K" and the item's working). KaTeX is
  served from the pinned local copy (`bank_common.serve_real_font`), so it runs offline. Four planted faults all fail the run.
- **Faults fixed:** none. **Expected failures left open:** none (t3-002..006 stay open as before).
- **Main's run:** 38232674780 (the #287 merge) green.

## 2026-10-12 (cloud): VERIFIERS-20 game 6, think-of-a-number (#287, merge commit 25a73bc)

- **Verifier:** `scripts/verify-think-of-a-number.py`: all 50 items (10 one-step, 20 two-step, 20 three-step): each key run forwards with
  Fraction must give the result (every intermediate a whole number from 0 up, key 1-9999) and run backwards must return the key; step
  displays and every `undoSteps` line recomputed; sessions of 10, 20 and 30 (2/4/4, 4/8/8, 6/12/12, no repeats); every item shown and answered on the
  numpad in Chromium (key right; result, key +-1, steps run forwards again, steps undone in the order told: wrong with the recomputed working).
  Four planted faults all fail the run.
- **Faults fixed:** none. **Expected failures left open:** none.
- **Lessons:** (1) #287 was held up by CI-TIMINGS-MEDIAN (home lane #288: timings are now the median of 5 main runs and the timings job
  commits only a pack that passes `--check`; main unblocked, run 791 green). (2) `cloud.md` must stay under 20 KB (context-size check):
  older entries move to `docs/history/handover-cloud-archive.md`. (3) The answer-lock self-test counts the backticked remaining-list line in this
  file: exactly one, so never write that token in backticks in an entry.
- **Main's run:** 38231678130 (the #289 merge) green; game 6's own main run is checked in the game 7 entry.

## 2026-10-12 (cloud): VERIFIERS-20 STOPPED after game 5: main's CI is red from the generated timings pack (home-lane item) - RESOLVED

- **RESOLVED 12 Oct:** the home lane's CI-TIMINGS-MEDIAN (#288, d00a818) made the timings a median of the last 5 runs; main's run 791 is green and `ci-groups.py --check` passes. This branch has main merged in; VERIFIERS-20 resumes with #287, then `formula-plug-in`.
- **STOP IF reached:** "main's full run is red after a merge and the fault is not in this lane's files". Main's run 787 (38225600227, the
  merge of #286) failed in 1 minute: the Plan job's `python scripts/ci-groups.py --check` fails with 12 group-budget FAILs
  (Content verifiers 1-4, 19-24, 34, 35 and Answer lock L1, each 81-108% of its budget). The same check fails on plain `main` at
  `ef82d88`, so every open PR is red too (#287's Plan and Gate are red for this alone).
- **Cause:** the automatic "Record CI timings and repack (run 38224711265)" commit `25f887b` (run 785) recorded inflated timings
  (e.g. Growth and Decay 55 s to 94 s, Formula Unlocked 17 s to 28 s, while PR #286's CI ran beside it) and repacked, leaving
  about a dozen groups above 80%. The check passed on main at `0f2f398` (before the repack) and failed from `25f887b`. The timings job
  only runs after a green full run, so main cannot repack itself out: it needs a home-lane commit. `scripts/ci-timings.json`
  and `scripts/ci-pack.json` are generated files outside this lane, so none was edited.
- **For the home lane:** restore the pack (for example revert `25f887b`, or re-record the timings from a quiet run and run
  `python scripts/ci-groups.py --write-pack`), and consider recording the median of several runs so one slow run cannot break the
  check. Note also that each new verifier line counts as 120 s until a main run times it.
- **State of play:** games 1-5 done and merged (#282-#286; main runs 779, 781, 783, 785 green, 787 red for the reason above). Game 6
  `think-of-a-number` is built and passing (`scripts/verify-think-of-a-number.py`, 50 items, four planted faults caught) in PR #287,
  which is merged-ready except for the red Plan/Gate. Games 7-20 not started. Game 6 is off the remaining list in this PR;
  nothing is claimed.
- **To resume:** once main's `ci-groups.py --check` passes again, merge `main` into `claude/verifier-think-of-a-number`, push, merge #287 on
  a green Gate, then continue with `formula-plug-in`.
- **Open for Jon:** delete branches `claude/verifier-prime-or-composite` and the other merged `claude/verifier-*` branches on GitHub (the
  proxy refuses remote deletes).

## 2026-10-12 (cloud): VERIFIERS-20 game 5, prime-factorisation (#286, merge commit ef82d88)

- **Verifier:** `scripts/verify-prime-factorisation.py`: both target banks (28 + 20) factorised by trial division, every prime factor
  on a button (buttons checked to be 2, 3, 5, 7, 11, 13), sessions of 8 different targets, and 4273 taps (ascending, descending,
  one too many, every button, non-dividing taps, seeded random) replayed against a model of the rule in Chromium: lives, product,
  hearts, product line, "T = p x q (+200)", "p is not a factor here!" and the out-of-lives factorisation. Four planted faults all fail.
- **Faults fixed:** none. **Expected failures left open:** none (t3-001..004 stay open as before).
- **Main's run:** 785 (game 4's merge) green.

## 2026-10-12 (cloud): VERIFIERS-20 game 4, factor-race (#285, merge commit 0f2f398)

- **Verifier:** `scripts/verify-factor-race.py`: the 20 Year 6 pairs (numbers 1-50, counts differ, no repeat, sessions of 10) and the
  KS3 table (`VALID_PAIRS`, 2694 pairs) rebuilt independently and compared as a set; 20,000 draws all inside it; every Year 6 pair and
  539 KS3 pairs answered by both cards and by time-out in Chromium (mark, card styles, "a has X factors; b has Y.", labels). Four
  planted faults all fail the run. Divisors are counted by the verifier's own loop, never the game's `getFactors()`.
- **Faults fixed:** none. **Expected failures left open:** none (t3-001..004 and f1-001 stay open as before).
- **Main's run:** 783 (game 3's merge) green.

## 2026-10-12 (cloud): VERIFIERS-20 game 3, percentage-flip (#284, merge commit c2f9d86)

- **Verifier:** `scripts/verify-percentage-flip.py`: both static banks (12 default + 20 Year 6): every key from the question's own
  P and N, every figure in every working line (seven shapes; an unknown shape fails), five deals per level, and each item
  answered right and wrong (key, key +-1, +-0.5, a tenth, ten times, the complement) through `checkAnswer()` and `flipCard()`
  in Chromium. Four planted faults all fail the run.
- **Faults fixed:** none. **Expected failures left open:** none (f1-001 phone fold stays open as before).
- **Main's run:** 781 (game 2's merge) green. Game 3's own main run is checked in the game 4 entry.

## 2026-10-12 (cloud): VERIFIERS-20 game 2, fraction-equivalence (#283, merge commit 69a2003)

- **Verifier:** `scripts/verify-fraction-equivalence.py`: the Year 6 bank (20 pairs) and the generator (20,000 draws in
  Chromium, every multiplier 2-6 and offset 1-3 reached); every key and cross-multiplication line recomputed with Fraction;
  every bank pair and 400 draws answered YES and NO through `guess()`; Year 6 sessions checked. Four planted faults all fail.
- **Faults fixed:** none. **Expected failure left open (for Jon):** `fraction-equivalence-v20-001` (LOW): Year 6 bank items
  12 and 18 are one question written both ways round, so 19 different pairs; replacing one is new content (SR-19). The
  verifier names it and fails on any other repeat. t1-001 (20 items) and f1-001 (phone fold) stay open as before.
- **Main's run:** see the next entry.
- Branch `claude/verifier-fraction-equivalence` deleted locally; GitHub branch `claude/verifier-prime-or-composite` is still
  on the remote (proxy refuses deletes): listed under Open for Jon. Squash merges mean `git branch -d` refuses, so the
  local branch was removed with `-D` after confirming the PR was merged.

## 2026-10-12 (cloud): VERIFIERS-20 game 1, prime-or-composite (#282, merge commit cdd29ff)

- **Verifier:** `scripts/verify-prime-or-composite.py`, all 66 numbers: key by trial division (SymPy cross-check), every hint
  claim, every explanation (first three divisors, ellipsis rule), each number marked both ways through the game's buttons in
  Chromium, five deals checked (whole bank once, 6 then 7 first). Five planted faults all fail the run.
- **Faults fixed:** none found. **Expected failures left open:** none (t1-002, hints give the answer away, MEDIUM, is not a
  key fault and stays open as before).
- **Main's run:** 779 (38218891574) green.
- **Container note for the next session:** the cloud container has no `esprima`, no WebKit and no KaTeX CDN, so
  `check-changed.py` shows environment failures (B11, calculator, answer-lock parts, teacher feedback) that CI does not.
  Python needs `pip install playwright==1.63.0 sympy mpmath`, and Chromium 1194 through scratch symlinks named 1243.
- **Open for Jon:** delete branch `claude/verifier-prime-or-composite` in GitHub (the proxy refused the remote delete).
