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
`cloud-remaining: wrong-on-the-internet`

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

**Queue:** VERIFIERS-20 (12 Oct, contract `docs/handover/contracts/2026-10-12-verifiers-20.md`): 20 verifiers, one game per PR; 1 prime-or-composite DONE (#282); 2 fraction-equivalence DONE (#283); 3 percentage-flip DONE (#284); 4 factor-race DONE (#285); 5 prime-factorisation DONE (#286); 6 think-of-a-number DONE (#287); 7 formula-plug-in DONE (#290); 8 four-quadrant-explorer DONE (#291); 9 new-shapes DONE (#292); 10 shape-shifter DONE (#293); 11 equatle DONE (#294); 12 standard-form-blitz DONE (#295); 13 index-laws DONE (#296, ruling #297); 14 modular-battle DONE (#298); 15 bearing-blitz DONE (#300); 16 constructions-lab DONE (#301); between games: wrong-on-the-internet t2-006 (Jon's SR-14 ruling) CLAIMED; next formula-forge; next standard-form-blitz ... as in the contract order.
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

## 2026-10-12 (cloud): MAIN RED, verify-modular-battle (run 826, #301's merge); fix is this lane's

- **Were #300 and #301 merged on green? Yes, both.** #300 merged after run 820 (#298) finished green (17:22 UTC); #301 after
  run 825 (#299) finished green (17:53). #300's own run, 822, was green. **Main went red on 826, #301's own merge run:**
  Content verifiers 13, verify-modular-battle (#298's verifier), attempt 1 and the re-run both failed. No cloud merge since.
- **Cause (a flaky verifier, not the game):** after the 408 steered questions, the scaffold and 90-second session drivers
  loaded questions on live `Math.random`. Under the "key offered twice" plant a b = 2 draw can show only the key twice, so
  `find()` returned undefined and the script threw (TypeError at `b.click()`). Measured: the old driver threw 24 of 200.
  It passed #298's PR and runs 820, 822 and 825 by chance.
- **Fix (branch `claude/modular-battle-verifier-steer`):** both drivers load fixed steered questions (`DRIVE_PAIRS`) and
  assert the steering took; a missing button is a `scaffold:`/`session:` FAIL, not an exception. New driver: 0 of 200, one
  outcome. Full verifier three times: PASS, identical output, all 7 plants caught.
- **Class check: local.** Of the 16 VERIFIERS-20 scripts, only this one drives play on live randomness; the other
  find-then-click drivers (four-quadrant-explorer, standard-form-blitz, index-laws) press fixed items, so are deterministic.
- **On hold until main is green:** the woti t2-006 PR (branch `claude/woti-t2-006`, not yet opened).

## 2026-10-12 (cloud): New Shapes diagram findings, Jon's ruling

- **Jon, 12 Oct:** New Shapes' diagram findings (r-001, t3-003, t3-004, t3-005: proportions fixed whatever the numbers, the prism's l arrow on the wrong dimension) **stay open until its SR-26 bank growth, which redraws from each question's parameters.** No cloud-lane redraw before then. The `new-shapes` verifier (#292) checks the numbers on the diagram only and prints that the geometry is not asserted; when the bank is grown and the diagrams are drawn from each item's parameters, extend the verifier to assert the geometry (drawn proportions and the l arrow along the depth edge) and close those four entries in the same PR.

## 2026-10-12 (cloud): Runner cancels at "Initialize containers" (Jon's rule, 12 Oct)

Rule: a job cancelled at Initialize containers is runner infrastructure; re-run only those jobs, up to 3 times per run; a green re-run counts as main green; any other failure or cancel stops the lane. Record per cancelled job, duration against timeout (content groups: 6 min = 360 s), for the home lane:
- Main run 802 (bb79123), attempt 1: 8 jobs cancelled at Initialize containers (Site-wide checks, Content verifiers 3, 9, 12, 25, 14, 32, 24). Durations not captured; one re-run used.
- Main run 802, attempt 2: Content verifiers 33 cancelled at Initialize containers, 10:56:22 to 11:02:41 = 379 s against a 360 s timeout (the whole timeout spent before the first step ran). Second re-run used.
- Earlier, on PR heads: #291 Content verifiers 3; #292 Tiers 1+2 shard 3/4, Content verifiers 4, then 3, 21, 13. Durations not captured.
Reading: 379 s is over the timeout, so the container pull is consuming the timeout, not the checks.

## 2026-10-12 (cloud): CHECKPOINT 2 (Jon asked for one at 66% context)

- **Merged:** VERIFIERS-20 games 1-16 (#282-#287, #290-#298, #300, #301; index-laws ruling #297); main green after each (last checked: 38286441432 on #299, and the #301 merge's run was in progress).
- **IN FLIGHT: wrong-on-the-internet t2-006 (Jon's SR-14 ruling, 12 Oct), branch `claude/woti-t2-006`.** Pushed: claim commit, and the one-line change in woti_core_006's correct stage-2 option
  ("At 100°C humans can't survive, let alone buy ice cream." becomes "At 100°C water boils, so nobody is queuing for ice cream."; key, options, explanation unchanged). The verify-wrong-on-the-internet.py run passed.
  TO DO: let the full `check-changed.py` finish (it touches a game page; the container's esprima/WebKit/KaTeX failures are expected), open the PR, then in a second commit set t2-006 to
  `status: fixed`, `pr: <n>` and `ruling: 'Jon, 12 Oct 2026 (SR-14): ...'`. Take `wrong-on-the-internet` off the remaining line in that PR, merge on a green Gate, then watch main.
- **Next, games 17-20:** drafts that pass are parked on branch `claude/verifiers-17-20-drafts` in `docs/handover/drafts/`, with a README giving each one's follow-ups (formula-forge-v20-001 to file for Jon;
  characteristic-quest's t6-003 SR-6 fix as a patch; a plant label to fix in eigenvalue-extractor; prisoners-dilemma left alone on t4-001). Each game gets its own claim, PR, Gate and main run.
- **Open for Jon:** formula-forge-v20-001 (three items with two wrong options equal in value; replacements suggested in the drafts README). Merged `claude/verifier-*` remote branches need deleting (the proxy refuses).
- **Interim rule:** the re-run rule for "Initialize containers" cancels can be retired once main has had two full runs with no such cancel since #299 (CONTAINER-PULL-TIMEOUT); remove it then.
- **Container setup (each new session):** Playwright 1.63 expects Chromium build 1243; the container has 1194 in another layout. In a scratch dir make `chromium_headless_shell-1243/` (with empty INSTALLATION_COMPLETE and DEPENDENCIES_VALIDATED files)
  holding a symlink `chrome-headless-shell-linux64 -> /opt/pw-browsers/chromium_headless_shell-1194/chrome-linux`, plus `chromium-1243/chrome-linux64` the same way. Add a symlink `chrome-headless-shell -> headless_shell` inside that 1194 dir.
  Set `PLAYWRIGHT_BROWSERS_PATH` to the scratch dir.
- **Recipe that works (games 1-8):** worktree from origin/main; claim commit (the previous game's entry + one `cloud-remaining` line) pushed alone; script; `ci-groups --check`,
  `audit-register --check`, `check-verifier-coverage`, `check-context-size`; PR; merge on green Gate with main's last run green (the "Record CI timings" commit appears only after a
  green main run). KaTeX games: serve it with `bc.is_font_cdn` + `bc.serve_real_font`. Never write the remaining-list token in backticks in an entry; keep this file under 20 KB (move old entries to the archive).
- **TeX readers (Jon, 12 Oct 2026):** per-verifier TeX readers are acceptable (as in verify-formula-unlocked.py, games 12 and 13); games 17-19 carry their own. HOME-LANE ITEM: give `bank_common`
  one exact TeX reader and move these verifiers onto it. Today `parse_value` reads `6x^7 \div 2x^2` as 3x^9 (against Jon's ruling on index-laws-v20-001), reads standard form as a float,
  and returns None for `v = u + at` (multi-letter juxtaposition) and for anything with `\lambda`.
- **Pre-push set for verifier-only PRs (Jon's ruling, 12 Oct 2026; the home lane records it as SR-27):** run the verifier and its self-test, `ci-groups.py --check`,
  `audit-register.py --check`, `check-verifier-coverage.py` and `check-context-size.py`; not `check-changed.py`. A PR that also touches a game page, a shared asset or another script still runs `check-changed.py`.
  Applies from game 12 (standard-form-blitz); games 10 and 11 ran the longer set.

## 2026-10-12 (cloud): VERIFIERS-20 game 16, constructions-lab (#301, merge commit 5b1307a; STOP IF: the game marks nothing)

- **Verifier:** `scripts/verify-constructions-lab.py`: there is no key (t3-001: nothing marks a construction), so per the contract's STOP IF it verifies what the game states and draws. Each task's figure is recorded from
  its own setup (moveTo/lineTo/arc/fillText) and every letter the steps name sits within 25 units of the point it labels; all ten tasks are built by their own steps with the game's compass, Lock Radius and ruler
  (clicks on the real canvas, pinned 1:1), every snapped crossing recomputed in Python (to 1e-6), and each stated result checked: perpendicular bisectors, angle bisectors, perpendiculars from and at P, "Angle BAC = 60°",
  the equilateral triangle, the 120px circle and the two 80px lines (label and steps agreeing), "more than half AB" both ways; the tap mapping at 390 px within one CSS pixel. Eight planted faults fail. About 10 s.
- **Not verifiable, reported:** whether a student's construction is right (t3-001); snapping ignores the given lines and points (t3-002: the verifier draws a ruler line along a given line first); t3-004, t3-005.

## 2026-10-12 (cloud): VERIFIERS-20 game 15, bearing-blitz (#300, merge commit 3575276)

- **Verifier:** `scripts/verify-bearing-blitz.py`: no option list (the key is the target bearing; the mark is the needle's error). All 360 whole-degree bearings pressed on the real compass (whole-pixel points chosen
  here within 0.35 degrees) and read back clockwise from North, with the needle drawn along each; 798 shots through Fire for 38 targets at -10..+10 degrees (every 0/360 wrap): hit within 5, points 150/100/50,
  message figures, lives; sessions (24 bearings, the 16 fixed present); three misses to "Submarine Destroyed!" through the real Next; twenty hits to "All Ships Sunk!" with the score added up. Eight planted faults fail. About 95 s.
- **Main's run:** 38285029221 (the #300 merge) green first time; Gate on #300 51 passed, 2 skipped.
- **Faults fixed:** none; no findings for this game.

## 2026-10-12 (cloud): VERIFIERS-20 game 14, modular-battle (#298, merge commit b220dd4)

- **Verifier:** `scripts/verify-modular-battle.py`: generated game (a 10..60, b 2..9). All 408 questions are driven through the game's own `generateQ()`/`loadQuestion()` by steering the two `Math.random`
  draws; 20,000 free draws land only on those 408 and reach all of them. Each: key = a mod b (Python divmod), min(4, b) different options from 0..b-1 with exactly one the key (SR-4/16), the dot grid
  (floor(a/b) groups of b, then a mod b red) and its label, every option pressed (feedback figures "a÷b=q rR" / "remainder R", score, Next). Scaffold shows, withdraws after 2 right, returns after 2 wrong;
  a session ends at 90 s with the right score. Seven planted faults fail. About 65 s with the self-test.
- **Main's run:** 38282980872 (the #298 merge) green first time; Gate on #298 51 passed, 2 skipped.
- **Faults fixed:** none. **Left open, not asserted:** t4-001 (says 60 s, runs 90; the portal card is outside the folder), t4-002, t4-003 (portal, spec map), t4-004 (the scaffold shows the answer: a design call).

## 2026-10-12 (cloud): VERIFIERS-20 game 13, index-laws (#296, merge commit 7339c3f; ruling #297, 5cdff5c)

- **Verifier:** `scripts/verify-index-laws.py`: all 45 items read from their TeX into exact SymPy expressions (positive symbols), every key worked out and the only right option (SR-4/16; the (5^2)^3 item's `ask` names a form,
  so 25^3 is legitimately wrong); the rule labels (8/8/7/4/8/10) checked against each question; 48 sums and stated roots in the explanations recomputed; KaTeX parses everything; sessions of 12 dealt 5 times; every item shown by
  `nextQ()` and all four options pressed in Chromium. Twelve planted faults fail after the ruling. About 35 s with the self-test.
- **index-laws-v20-001, RULED (Jon, 12 Oct):** the convention stands: a term such as 2x^2 is one object (implied multiplication binds tighter than ÷), so `6x^7 \div 2x^2` = 3x^5; keys and stems unchanged.
  The finding is closed as `ruled`; the verifier now reads a coefficient-and-variable term after ÷ as one term (no expected failures) and fails only a divisor that is not such a term (SR-17), in the follow-up PR.
  The home lane records the convention as a standing ruling.
- **Main's runs:** 38279747529 (#296) and 38281083831 (#297) green first time; both Gates 51 passed, 2 skipped.
- **Faults fixed:** none.

