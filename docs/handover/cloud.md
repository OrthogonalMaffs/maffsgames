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
`cloud-remaining: equatle`

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

**Queue:** VERIFIERS-20 (12 Oct, contract `docs/handover/contracts/2026-10-12-verifiers-20.md`): 20 verifiers, one game per PR; 1 prime-or-composite DONE (#282); 2 fraction-equivalence DONE (#283); 3 percentage-flip DONE (#284); 4 factor-race DONE (#285); 5 prime-factorisation DONE (#286); 6 think-of-a-number DONE (#287); 7 formula-plug-in DONE (#290); 8 four-quadrant-explorer DONE (#291); 9 new-shapes DONE (#292); 10 shape-shifter DONE (#293); 11 equatle CLAIMED; next standard-form-blitz ... as in the contract order.
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

## 2026-10-12 (cloud): New Shapes diagram findings, Jon's ruling

- **Jon, 12 Oct:** New Shapes' diagram findings (r-001, t3-003, t3-004, t3-005: proportions fixed whatever the numbers, the prism's l arrow on the wrong dimension) **stay open until its SR-26 bank growth, which redraws from each question's parameters.** No cloud-lane redraw before then. The `new-shapes` verifier (#292) checks the numbers on the diagram only and prints that the geometry is not asserted; when the bank is grown and the diagrams are drawn from each item's parameters, extend the verifier to assert the geometry (drawn proportions and the l arrow along the depth edge) and close those four entries in the same PR.

## 2026-10-12 (cloud): Runner cancels at "Initialize containers" (Jon's rule, 12 Oct)

Rule: a job cancelled at Initialize containers is runner infrastructure; re-run only those jobs, up to 3 times per run; a green re-run counts as main green; any other failure or cancel stops the lane. Record per cancelled job, duration against timeout (content groups: 6 min = 360 s), for the home lane:
- Main run 802 (bb79123), attempt 1: 8 jobs cancelled at Initialize containers (Site-wide checks, Content verifiers 3, 9, 12, 25, 14, 32, 24). Durations not captured; one re-run used.
- Main run 802, attempt 2: Content verifiers 33 cancelled at Initialize containers, 10:56:22 to 11:02:41 = 379 s against a 360 s timeout (the whole timeout spent before the first step ran). Second re-run used.
- Earlier, on PR heads: #291 Content verifiers 3; #292 Tiers 1+2 shard 3/4, Content verifiers 4, then 3, 21, 13. Durations not captured.
Reading: 379 s is over the timeout, so the container pull is consuming the timeout, not the checks.

## 2026-10-12 (cloud): VERIFIERS-20 game 10, shape-shifter (#293, merge commit 8e52e94)

- **Verifier:** `scripts/verify-shape-shifter.py`: 15 translation, 15 reflection and 15 rotation items recomputed from their words (SR-25: dx/dy, axis, turn
  direction; rotation turned here, clockwise (x,y)->(y,-x)); four rotation options, one true, each other a named slip; letters inside their shapes; sessions of all four
  modes dealt 5 times; every vertex of every answer tapped at all 121 grid points and every rotation letter tapped over 8 deals on the real canvas; whole sessions played to 10/10 and 0/10.
  Seven planted faults fail (wrong dx, wrong axis, reversed turn = old r-001, second correct option, wrong feedback letter, y ignored, wrong reflection). About 2 min a run.
- **Main's run:** 38266515892 (the #293 merge) green first time; Gate on #293 had 50 passed, 2 skipped. Local `check-changed.py` fails site-wide checks only because this container lacks `esprima`, WebKit and the KaTeX CDN.
- **Faults fixed:** none. **Expected failure left open:** t3-003 (reflection item 15 is its own image; a replacement is content, SR-26). Not asserted: t3-001, t3-002, t3-004, t3-005.

## 2026-10-12 (cloud): VERIFIERS-20 game 9, new-shapes (#292, merge commit 12c5018)

- **Verifier:** `scripts/verify-new-shapes.py`: all 50 items (15 parallelogram, 20 trapezium, 15 prism) against three formulas held in the verifier; key by `Fraction` from the item's values;
  working steps checked; sessions of 10/20/30 dealt 3 times; the diagram's numbers and accessible description checked in Chromium (SR-25); every item answered on the numpad. Five planted faults fail.
- **Faults fixed:** none. **Left open:** diagram proportions and the prism l arrow (r-001, t3-003/004/005), Jon's call.
- **Main's run:** 38236088363 (the #291 merge) green on its third attempt after two "Initialize containers" cancels (container pull used the 360 s timeout; two of three re-runs used).
  Run 38260101808 (the #292 merge) green first time. Gate on #292: 51 jobs passed, 2 main-only skipped.

## 2026-10-12 (cloud): VERIFIERS-20 game 8, four-quadrant-explorer (#291, merge commit bb79123)

- **Verifier:** `scripts/verify-four-quadrant-explorer.py`: Plot (20), Read (15) and Shape (10) banks recomputed (grid points; read options four distinct, one equal, every
  distractor a sign or order slip; the point drawn at exactly one of 121 grid points; shape key = the missing fourth corner), queues cycle plot/read/shape at 10/20/30, and
  every plot and shape question tapped at all 121 grid points on the real canvas (plus 0.45/0.55-cell edge taps), every read option pressed, in Chromium. Five planted faults fail.
- **Faults fixed:** none. **Expected failures left open:** none (r-001, t3-002, t3-003 stay open).
- **Main's run:** 38233755799 (the #290 merge) green. A runner cancelled one job once ("Initialize containers"); one re-run of the failed job passed.

## 2026-10-12 (cloud): CHECKPOINT (Jon asked for one: context very high)

- **Done and merged:** games 1-7 (#282-#287, #290); the CI-TIMINGS-MEDIAN home-lane fix (#288, #289). **In flight:** game 8 four-quadrant-explorer, PR #291
  (verifier passes locally, 5 planted faults caught; waiting on its Gate; merge on green with main's run green, then record it in the next entry).
- **Game 9 draft:** `scripts/verify-new-shapes.py` is on branch `claude/verifier-new-shapes` (passes; 50 items; diagram numbers checked; 5 planted faults caught).
  To resume: after #291 merges, make a fresh worktree from origin/main, claim `new-shapes` in a handover commit, bring the script over from that branch
  (`git checkout claude/verifier-new-shapes -- scripts/verify-new-shapes.py`), run `ci-groups --check`, open the PR. The diagram's PROPORTIONS and the prism l arrow
  are deliberately not asserted (open findings r-001, t3-003/004/005: a redraw is Jon's call); the verifier prints that.
- **SR-26 (Jon, 12 Oct): growing banks.** A bank too small or with duplicates is fixed by growing it from parameters, never by swapping single items; new
  real-world contexts stop for Jon; a bank is grown only after its verifier runs in CI. This now decides `fraction-equivalence-v20-001` (the repeated Year 6 pair) and
  t1-001 (20 items): fix = a parameter-generated Year 6 pair bank. NOT started: the contract still says not to add questions, and the size and the named
  misconceptions for the non-equivalent pairs need Jon (a contract).
- **Recipe that works (games 1-8):** worktree from origin/main; claim commit (the previous game's entry + one `cloud-remaining` line) pushed alone; script; `ci-groups --check`,
  `audit-register --check`, `check-verifier-coverage`, `check-context-size`; PR; merge on green Gate with main's last run green (the "Record CI timings" commit appears only after a
  green main run). KaTeX games: serve it with `bc.is_font_cdn` + `bc.serve_real_font`. Never write the remaining-list token in backticks in an entry; keep this file under 20 KB (move old entries to the archive).
- **Container setup (each new session):** `pip install playwright==1.63.0 sympy mpmath`; Chromium 1194 via a scratch dir of symlinks named 1243 (see the container note in the game 1 entry); `PLAYWRIGHT_BROWSERS_PATH` pointing at it.
- **Remaining after 9:** shape-shifter, equatle, standard-form-blitz, index-laws, modular-battle, bearing-blitz, constructions-lab, formula-forge, characteristic-quest, eigenvalue-extractor, prisoners-dilemma (contract order).
- **Open for Jon:** delete the merged `claude/verifier-*` branches on GitHub (the proxy refuses remote deletes); `fraction-equivalence-v20-001` and SR-26 scope (above).

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

(Entries for VERIFIERS-20 games 1-5 and the CI stop of 12 Oct are in `docs/history/handover-cloud-archive.md`: #282-#286, all green; the stop was resolved by #288.)
