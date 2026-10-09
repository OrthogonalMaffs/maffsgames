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

**Contracts (Jon, 8 Oct 2026, corrected 20:00):** each contract is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md` in its claim commit (or the PR's first commit), with one line
in the queue below pointing to it. Read it when the item starts, not at session start (the folder stays out of the
start-up load). When the work merges, move the file to `docs/history/`.

**Queue:** UC-FIX: DONE, #196 merged 9 Oct (c9fbf4b), main green.
SIM-S5: done by its PR (claim #202 merged 7de7e73; its contract and the answers move to `docs/history/contracts/`
in it). Then UC-T4-007 (a small PR, the answers' item 3c), then FT-FIX without asking. Then FT-FIX: contracts/2026-10-08-ft-fix.md as amended by -ft-fix-amend.md (step 3 and t5-008 go to the home lane).
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

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
