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
SIM-S5: DONE, #203 merged 9 Oct (4081538). UC-T4-007: DONE, #205 merged 9 Oct (920c5b1; the answers' item 3c, in
`docs/history/contracts/2026-10-09-sim-s5-answers.md`; claim #204). FT-FIX: DONE, #207 merged 9 Oct (cf96929; contract, amendment and Jon's answers
of 9 Oct, 11:00, in `docs/history/contracts/2026-10-0[89]-ft-fix*.md`). The queue is empty: stopped for Jon.
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-09 (cloud): FT-FIX, factor-theorem (fix #207 merged cf96929; main run 593 green)

- **For the home lane, CI, before the next E verifier lands:** main's run 593 put group E at **8m39s of its 9m00s
  budget** (12 min timeout). Factor Theorem now takes 69 s there (its option, level and Next checks and 8 plants);
  Screening Room 89 s, Simultaneous Solver 73 s, Terrible Advice 57 s, Linear Equation Solver 52 s. The B1, B3 and B4 jobs
  took 5m00s to 5m23s (setup included; their budget is 6 min), so moving one verifier only moves the pressure: a new group (E2 or B5) in
  `scripts/ci-groups.py`. The cloud lane left E as it is.
- **Answer buttons (answers 1):** Q33 ("Which line proves it?") and T9(c) are four shuffled buttons each, the
  contract's lines, marked by `dataset.val` on Check or Submit (with T9's other parts); the explanation shows after
  marking. All in the game (`fillOptions`, `chosenValue`, `markOptions`, `.opt-*` CSS); the lock hint picks a button.
- **A-Level only (answers 2):** the page never reads `?level` (a comment says so); every URL logs and submits
  `alevel`. No start screen, no level4 board. **For the home lane, at relisting: remove L4 from Factor Theorem's
  roster row, the portal filter and the spec map.** With no open CRITICAL or HIGH after this PR, it is ready (SR-21).
- **Practice submits nothing** (t5-014, t5-015); its device-local score-history record went with it (nothing reads
  `MaffsScoreHistory.get`). The Test alone submits, once, to `factor_theorem_alevel`.
- **A wrong answer waits on `MaffsNext`** (t5-018's note; next-control.js loaded); a right one keeps Next Question.
  t5-018's other parts were already fixed on main: closed with the measurements.
- **`scripts/check-teacher-invite.py` (answers 3):** one line added to FT_STEP (choose a button in any unanswered
  `.opt-group`); nothing else changed. Its factor-theorem routes reach both end screens at 390 and 1280 (KaTeX served
  locally: the sandbox cannot reach the CDN). check-answer-lock seeds 1-3 PASS the same way.
- **Verifier** (group E): the option checks (Q33's working for every n; T9(c) from s, v and a), prose keys, the five
  ?level URLs, no Practice submit, MaffsNext on a wrong answer; 8 plants, all caught. About 80 s with its self-test.
- **Still open, not this lane's:** t5-008 (home lane, VOCAB-IDEMPOTENT), t5-016 and t5-017 (a Test bank of 40 from
  Project Claude, a separate contract).

## 2026-10-09 (cloud): FT-FIX stopped before building (contract STOP IF; answered 11:00, above)

- **STOP IF fired: "the game's selection pattern can't serve a 4-option item inside a multi-part test question
  without engine changes".** factor-theorem has no selection pattern at all: every Practice item and every Test part
  is a typed box (no options, no `dataset.val` anywhere). Engine changes needed, all in the game: an item or part
  with `options` renders four buttons (shuffled, `data-val` the option's text) in place of its box; choosing one
  marks it chosen; Check (Practice) or Submit Answer (Test, with the other parts) marks `dataset.val` against the
  key; one attempt, as the typed tier-5 items. Self-contained, about 40 lines. Recommended.
- **Also unexpected, for Jon:** the game has **no start screen**. It opens on Learn, with Practice and Test as
  tabs. Step 5's "an absent or unknown key shows the start screen (level choice)" needs a new one. Proposal: a
  level choice (A-Level, Level 4) shown instead of the tabs until a level is chosen; a valid `?level` skips it;
  the top bar's badge shows the chosen level. Design addition (canon §0.3 "still stops").
- **Both changes break a shared check the cloud lane may not edit:** `scripts/check-teacher-invite.py` (site-wide,
  every PR) plays factor-theorem with no `?level`, clicks the Practice tab and fills `input.answer-input` boxes
  (FUNCTION_ROUTE, FT_STEP). Additive fix: a `("click", '[data-level="alevel"]')` step first in both routes, and
  FT_STEP choosing the first option in any unanswered option group. Jon authorises it in the FT-FIX PR (as the
  foundation-s5 lines), or the home lane lands it first. check-answer-lock needs nothing shared: the game's own
  lock hint can name `"level": "alevel"`.
- **t5-018 is fixed on main already** (Chromium, 390x844, this session): T5 and every Test question 390 px wide;
  Learn at 390 and 320 px; no literal `___` and no `<span` in any attribute; `question_index` is `qIdx + 1` in
  both modes; hint button off after marking; Enter checks. Left: its "wrong-answer advance not MaffsNext" note.
- **For Jon (the rule recorded with SR-16 to SR-20):** "a level that serves another level's items is not listed as
  that level". Step 5 has Level 4 serve A-Level's content (the page has no separate Level 4 content); relisting it
  at L4 would fall under that rule. The home lane's relisting decides.
- **Did not fire:** Q33 and T9(c) match the quoted text; `question_index` needs no change; a `level4` board needs
  no hub or coverage change (factor-theorem is in NOT_ON_HUB; the module labels `level4` "Level 4").

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
