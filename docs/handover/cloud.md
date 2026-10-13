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
`cloud-remaining: standard-form-blitz`

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

**Queue:** VERIFIERS-20 (12 Oct, contract `docs/handover/contracts/2026-10-12-verifiers-20.md`): 20 verifiers, one game per PR; 1 prime-or-composite DONE (#282); 2 fraction-equivalence DONE (#283); 3 percentage-flip DONE (#284); 4 factor-race DONE (#285); 5 prime-factorisation DONE (#286); 6 think-of-a-number DONE (#287); 7 formula-plug-in DONE (#290); 8 four-quadrant-explorer DONE (#291); 9 new-shapes DONE (#292); 10 shape-shifter DONE (#293); 11 equatle DONE (#294); 12 standard-form-blitz DONE (#295); 13 index-laws DONE (#296, ruling #297); 14 modular-battle DONE (#298); 15 bearing-blitz DONE (#300); 16 constructions-lab DONE (#301); between games: wrong-on-the-internet t2-006 (Jon's SR-14 ruling) DONE (#304, 73478d6), closes t2-006; modular-battle verifier flake fixed (#303); 17 formula-forge DONE (#305); 18 characteristic-quest DONE (#306); 19 eigenvalue-extractor DONE (#307); 20 prisoners-dilemma DONE (#309). **VERIFIERS-20 COMPLETE.** Then: formula-forge-v20-001 (Jon's ruling, 12 Oct) DONE (#310, 8d36ca2).
B11-CLEAR (12 Oct, contract `docs/handover/contracts/2026-10-12-b11-clear.md`): clear B11 from the ledger, one game per PR: 1 scale-factor-scaling DONE (#312, 031d8ed); 2 coordinate-geometry-dash DONE (#315); 3 index-laws DONE (#320, 588a903); 4 standard-form-blitz claimed; then surd-simplifier, boolean-blitz, complex-converter.
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

## 2026-10-12 (cloud): B11-CLEAR game 3, index-laws (#320)

- **Replacements (kind a, keys unchanged):** [6] 3^{12} -> 3^2 (subtracted the powers; 9^6 kept); [27] 1/x^{-3} -> −1/x^3 (negative as well; x^3 kept); [38] 27/3 -> 1/3, [39] 100/2 -> 1/10, [40] 25/2 -> 1/5 (reciprocal as for a negative power; 9, 50, 12.5 kept).
- **Verifier** fails on any equal pair except the key beside another form where `ask` names it ((5^2)^3); plant puts 3^{12} back.
- **Games 4-7 are built and committed locally** (worktrees /home/user/wt/sfb, ss, bb, cc; branches claude/b11-<slug>), each verifier PASS with its plant, each ledger clean for its game only. Each needs: rebase on main, claim commit pushed alone, fix pushed, PR, findings + release commit. Recipe: KaTeX via `npm pack katex@0.16.9` in the scratchpad; extraction through `docs/sandbox-checks.md`'s `run_extract_offline.py`; verifiers take `--katex-dir`.
- **Surd Simplifier note for Jon:** six of its eight pairs (27/99 and 9/33 for 3/11, and so on) are both the KEY's value unsimplified, under "simplest form": SR-4's form exception, so they are listed in the allowlist (as alevel[6]/[7] already were), not replaced. gcse[38] and [43] are replaced. Jon can reverse this.

## 2026-10-12 (cloud): B11-CLEAR game 2, coordinate-geometry-dash (#315)

- **Replacement (kind a, key unchanged):** alevel[15] (x = 2t + 1, y = t^2 - 3, dy/dx at t = 1; key 1): 1/2 -> −2 (gave y at t = 1, not the gradient); ½ kept.
- **Verifier** fails on any equal pair (EQUAL_PAIRS empty; plant puts 1/2 back). Ledger: this game only.
- **Container (new session after a clear):** cdn.jsdelivr.net is refused by the proxy (403), so every browser check of a page loading KaTeX from the CDN fails locally (about 30, incl. answer-lock parts); the changed game's own verifier and B11 passed. CI is the measure. Playwright needs `PLAYWRIGHT_BROWSERS_PATH` pointing at a dir with `chromium-1243 -> /opt/pw-browsers/chromium-1194` (and the headless shell likewise); esprima as in game 1. A full check-changed run takes over 35 min here: give the background run the 2 h timeout. Never run two at once (they share the stub server's port: "QUESTIONS is not defined").
- **Next:** index-laws (replacements drafted: [6] 3^{12} -> 3^2, subtracted the powers; [27] 1/x^{-3} -> −1/x^3, made the answer negative as well; [38] 27/3 -> 1/3, [39] 100/2 -> 1/10, [40] 25/2 -> 1/5, each took the reciprocal as for a negative power; the kept twin of each is the student's own form). Then standard-form-blitz ([35] 25x10^2 -> 2.5x10^{-3}, squared and ignored the minus); surd-simplifier (its pairs also equal the key: 27/99 = 9/33 = 3/11; ask "simplest form"); boolean-blitz (every question shows "Simplify fully.", so the six kind-b items are allowlisted, #227 accepts AB + BC for B(A + C)); complex-converter ([14] context "Express in polar form (degrees).": allowlist; [42] 0 + 7j -> 0, took e^{j0} as 0).

## 2026-10-12 (cloud): B11-CLEAR game 1, scale-factor-scaling (#312, merge commit 031d8ed)

- **Replacements (kind a, keys unchanged):** T1[8] 4:10 -> 4:5 (squared only the first number; 2:5 kept); T1[9] 3:9 -> 1:6 (doubled the scale factor instead of squaring it; 1:3 kept).
- **Verifier** fails on any equal pair (EQUAL_PAIRS empty; plant puts 4:10 back). **Ledger:** `extract-banks.py --only` then `check-banks.py --only <slug> --write-ledger`; only this game changed.
- **Container:** extraction needs esprima, which will not build here; the CI pin (4.0.1) is pure Python: `pip download --no-binary :all: esprima==4.0.1`, untar into the scratchpad, put it on PYTHONPATH.
