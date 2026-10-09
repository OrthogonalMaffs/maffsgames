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

**Queue:** UC-FIX: DONE, #196 merged 9 Oct (c9fbf4b), main green.
SIM-S5: DONE, #203 merged 9 Oct (4081538). UC-T4-007: DONE, #205 merged 9 Oct (920c5b1; the answers' item 3c, in
`docs/history/contracts/2026-10-09-sim-s5-answers.md`; claim #204). FT-FIX: DONE, #207 merged 9 Oct (cf96929; contract, amendment and Jon's answers
of 9 Oct, 11:00, in `docs/history/contracts/2026-10-0[89]-ft-fix*.md`).
LISTED-HIGH (in progress, `contracts/2026-10-09-listed-high.md`): 13 items, one game per PR, in the contract's order;
each next game is claimed in a commit of its own, riding the previous game's PR. Progress in the LISTED-HIGH entry below.
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-09 (cloud): LISTED-HIGH (in progress; contract in `contracts/2026-10-09-listed-high.md`)

One PR per game, in the contract's order; each next game's claim is a commit of its own at the end of the previous
game's PR (so it reaches main before that game starts). New verifiers go in **B2** (main run 595: 249 s of its 360 s
budget; E is at 491 s and takes nothing new).
- **1 surd-simplifier: #210** (claim #209). t1-001 keyed sqrt2 (sqrt2.sqrt2 kept as the value-2 distractor;
  8sqrt32/32 removed, so no B11 allowlist entry was needed), t1-002 keyed 206/495. New `verify-surd-simplifier.py`
  (B2, ~15 s): every stem read as TeX and compared with its key in SymPy, keys in simplest form, every option
  clicked; fails main's page on both. No other key differed.
- **2 52dle: #211** (claim rode #210). Guesses marked by the shared `MaffsAnswer.exact` on the raw text (answer.js
  loaded), never `parseInt`. The pi hint "100 × π rounded to 2dp" read as 314.16; it now says "100 × (π to 2 d.p.)"
  (an unambiguous key/word clash in the finding's own puzzle: fixed here, per the STOP IF). New `verify-52dle.py`
  (B2, ~4 s): every number recomputed from its clue and hints (FACTS), 7 guesses per puzzle typed in Chromium.
- **3 scale-factor-scaling: #212.** The paint item states the original surface (10 m², 1 litre); key 4 litres (its
  text "4 litres per 10 m²" contradicted the stem's rate; the value is kept). New `verify-scale-factor-scaling.py`
  (B2, ~2 s): every key from the quantities its prompt states. Seen, not touched (B11's domain, not this finding):
  T1[8] offers 2:5 and 4:10, T1[9] 1:3 and 3:9, wrong options equal to each other.
- **Main went red after #211 (run 601): group E at 9m04s of its 9m budget**, none of this lane's verifiers in it.
  Jon (9 Oct): the cloud lane adds E2 now, on a branch of its own: **#213** (`claude/youthful-feynman-anpxuq-e2`,
  merged 63ad521) moved Screening Room, Simultaneous Solver and Terrible Advice into E2; E 4m31s, E2 4m22s on its
  run; main green again (run 37950120068). E's job name still lists two moved verifiers (names kept stable): the
  home lane's call.
- **Jon's rulings of 9 Oct, 16:21** saved beside the contract (`contracts/2026-10-09-listed-high-rulings.md`):
  item 9 t4-003 is NOT rewritten: "Yes - but only when k > 0" is accepted alongside the key (an accepted set, in
  the game), the explanation says why both are right; the rest as written.
- **4 coordinate-geometry-dash: #214.** x = 3t, y = 4/t: options xy = 12 (key), xy = 7, y = 12x, x = 3y/4. New
  `verify-coordinate-geometry-dash.py` (B2, ~4 s): all 45 keys recomputed, equations compared as curves.
- **5 complex-converter: #216** (#215 was the home lane's RULINGS-9OCT). The contract's "apply it to every item" taken literally: the target line states
  the range on every polar and exponential question; ids 20, 28, 30, 38, 53 keyed principal (same numbers; ids 20,
  28 and 53 said "positive angle", which went); a second form of the key removed from ids 20, 21, 28, 40, 48 (40
  and 48 had a negative-modulus twin); argDeg/argRad principal everywhere (Triples' cards). New
  `verify-complex-converter.py` (B2, ~5 s, KaTeX from the CDN): every option read as a complex number. Also closes
  t6-002 and t6-003 (the ids 40/48 twins, MEDIUM jc). **Lesson (CI red once on #216): a fixed B11 pair must leave
  `data/check-ledger.json` in the same PR** (tier 4 fails a stale entry); run `extract-banks.py --only <slug>` then
  `check-banks.py --ci --only <slug>` before pushing (esprima: pip build fails here; unpack its sdist on PYTHONPATH).
- **6 higher-power: #217.** Pairs matches by value (`sameValue`). New `verify-higher-power.py` (B2, ~2 s).
- **Jon, 9 Oct (answer to a question, item 11): Boolean Blitz marks an option right when it has the key's truth
  table AND no more literals than the key** (AB + BC, AB + AC accepted; the t6-004 unsimplified forms such as
  A·B + A for A stay wrong; t6-004 untouched). Boolean-blitz has B11 ledger entries for t6-002/003: clear them.
- **7 seven-bridges: #219, merged 5926c24.** al_15's E to (300,150); t4-001 fixed by F1 batch 9 (closed with
  measurements). **Jon's rulings, 9 Oct 18:03 (addendum, folded into #219):** al_10, al_18, al_21's grazing edges
  fixed (each layout mirrors its own other half; edges unchanged); `CLEAR` 28 px (current vertex r 24 + 2 px stroke
  + half a 4 px edge; grazes were 19.8-21.1 px, next edge 28.1 px), no exemptions. **complex-converter ids 20, 28, 53
  stay on the principal range (-pi < arg z <= pi), as merged in #216: no change.** Main's #217 run went over budget
  in B4 and L2 (no test failed); one re-run passed.
- **8 wrong-on-the-internet: #223, merged 4094b01** after main went green on #224 (run 37969653160). The wheel is
  stated (European, single zero; key 18/37) and A and B are said to be independent in their post.
- **9 core-maths-paper2c: #225.** Q12 stem opens "f is a quadratic."; Q35 `accept: [1, 3]` (Jon 16:21): selectAnswer
  marks against `q.accept || [q.correct]`, the lock hint picks outside it, the working says why both "Yes" are right;
  t4-001 fixed by F1 batch 10. New `verify-core-maths-paper2c.py` (~25 s).
- **10 core-maths-paper2b: #226** (stacked on #225, on its own branch so CI runs while #225 waits; Jon, 18:56: one
  PR each). Q28 option D is "Neither — both premiums cost more than the expected loss" (false: the data breach
  premium, £900, is below its expected loss, £1,000). New `verify-core-maths-paper2b.py` (~5 s).
- **11 boolean-blitz: #227** (stacked on #226). Marked in the game (boolParse, minSopLiterals, sameAnswer): right =
  the key's truth table AND literals <= max(the key's, the minimal SOP's) (Jon's two answers of 9 Oct). Only Q24's
  AB + BC and Q41's AB + AC are accepted beside a key; the verifier fails any other (Jon, 18:56). t6-001 fixed by F1
  batch 11. The B11 ledger entries stay (options unchanged; Jon agrees). Locally the bank lint cannot extract this
  bank (KaTeX CDN; main's page fails the same way): CI judges it.
- **CI (CI-BALANCE, #220):** groups are packed now. A new verifier's header is `# ci-line: <label> | <args>` (no
  group id); untimed lines get a group each until main's timings job records them. `ci-groups.py --check` locally.
- **Local checks used for each PR** (the sandbox cannot reach the KaTeX CDN): check-changed's plan, the answer lock for
  the changed game with KaTeX served locally, and `extract-banks.py --only <slug>` + `check-banks.py --ci --only
  <slug>` (stale B11 ledger entries must leave `data/check-ledger.json` with the fix). esprima: unpack its sdist on
  PYTHONPATH. Teacher-line fails locally on factor-theorem and log-laws only (KaTeX CDN): not a change's fault.
- **Remaining, in order.** Drafts (page edits, verifiers, item-13 evidence) survive a clear in the session scratchpads
  under `/tmp/claude-0/-home-user-maffsgames/` (5dd7a927.../scratchpad and 8451d901.../scratchpad); each was checked
  9 Oct: passes the fixed page, fails main's (or the pre-batch) page.
  - 12 prisoners-dilemma t4-002: **HOLD (Jon, 18:56; note saved as `contracts/2026-10-09-listed-high-note-1900.md`).**
    The drafted in-game keydown guard is **discarded**, in no PR: it was the defensive-patch shape (a guard in one
    caller round a fault in the shared initials overlay, which lets typed keys reach page shortcuts in every game with
    a document keydown handler). The home lane fixes the overlay (contract OVERLAY-KEYS). When its handover records
    that fix, re-run item 12's check (drafted `verify-prisoners-dilemma.py`: C plays; "CDC" typed in the overlay and
    "dd" in a field play nothing) against prisoners-dilemma with no change to the game's code. t4-001 stays open
    (Jon's design).
  - **Merging (Jon, 18:56):** #223 and every later PR wait for a green main run; the workflow and `ci-groups.py` are
    the home lane's. With no green main this session, the PRs stay open, green on their own checks.
  - 13 stale locks: characteristic-quest t6-001, eigenvalue-extractor t6-001, matrix-crunch t6-001 and t6-002,
    formula-forge t4-001: all fixed on main (measured 9 Oct: key + Enter x3 = one mark, wrong + Tab+Enter = no change;
    the pre-batch pages give the audits' numbers, e.g. 93 -> 369; matrix-crunch flag 25 -> 100, lives 3 -> 0) and
    check-answer-lock passes on main, fails each pre-batch page. matrix-crunch's flag path is not played by
    check-answer-lock: give it a small verifier.

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
