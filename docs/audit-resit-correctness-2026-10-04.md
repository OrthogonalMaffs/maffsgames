# Resit suite correctness audit — 4 Oct 2026

Read-only audit of the `/resit/` suite: every suite game without a CI verifier, every answer key
recomputed independently. **Nothing was fixed** (SR-9); this file is the evidence for the fix batches.

## Handover

- **Scope.** The 32 games in `SUITE` (`scripts/check-resit-page.py`). Six have a verifier run in CI and
  were skipped: `six-sevens-bruv`, `free-daily-pizza`, `split-it`, `distinctly-average`, `stat-attack`,
  `chart-interrogator`. `better-value` was audited even though `verify-better-value-tax.py` is in CI,
  because that verifier checks only the tax/NI question. **26 games audited, every level each offers.**
- **Result: 4 CRITICAL, 29 HIGH, 40 MEDIUM, 83 LOW** across the 26 games (per-game table below).
  Ten games have no HIGH or CRITICAL fault: `think-of-a-number`, `factor-race`, `prime-factorisation`,
  `formula-plug-in`, `like-terms-collector`, `four-quadrant-explorer`, `new-shapes`, `unit-converter`,
  `formula-forge`, `percentage-flip`. `linear-equation-solver`'s one HIGH is a judgement call.
- **STOP IF fired three times** (reported in the session as found; the audit then continued):
  1. **`shape-shifter`**: every rotation question is keyed in the wrong direction (15 of 15), and
     tapping an option often selects a different one (21 of 40 taps in Chromium).
  2. **`correlation-or-coincidence`**: Phase 1 is unanswerable on 13 of 13 questions. The variable
     names are hidden (`color:transparent`) and the charts have no axis text until after the
     student has answered; the guess is scored and sent to the leaderboard.
  3. **`equation-builder`**: marking compares tile slots position by position, so an equally correct
     arrangement (`C = 3 + 2.50m`) is marked wrong on 29 of 120 questions (Foundation, the card's
     level: 9 of 40). One key is also wrong (gcse_013, the vector OM).
- **Wrong keys a student meets at the level the `/resit/` card opens:** `probability-pioneer`
  (MATHS/GAMES keyed 2/5, the answer is 3/5), `angle-ace` Starter diagrams (L293, L437 and three
  co-interior recognition items), `decimal-detective` and `negative-number-line` (number-line
  tolerances that mark a neighbouring tick correct, and a marker that starts on the answer),
  `estimation-engine` (√(e × 1000) keyed 52.07, the answer is 52.137); and `linear-equation-solver`'s
  judgement-call HIGH. Every other HIGH is at a level a student reaches from the card's picker, except
  `expected-damage`'s GCSE ties: its card is a link that opens at Foundation, with no picker.
- **Every HIGH and CRITICAL fault below was re-checked against the source by the reviewing session**
  (the line, the key and the arithmetic), not taken from the auditing agent's word alone. MEDIUM and
  LOW faults carry the agents' evidence and were spot-checked, not all re-derived.
- **Next:** Jon ruled on all eight decision items on 4 Oct 2026 (recorded under each in "Decisions
  for Jon"; canon SR-13). The fix batches, with the rulings applied, are in `docs/todo.md` START,
  in the order proposed below, one game per contract, each with its own verifier added to CI (the class
  this audit measures is "games without verifiers"; fixing keys without adding the verifier leaves
  the class open).

## Method

- **Banks read from the live page.** `scripts/extract-banks.py` was run unchanged, on a disposable
  copy of the repo in the session scratchpad (`docs/sandbox-checks.md` recipe, KaTeX served locally),
  so each bank is what a student is served after any runtime patching. The extract captures only
  arrays of objects carrying `correct`, so every game's source was also read in full; several banks
  are larger than the extract (e.g. `negative-number-line`'s 15 Place It targets are a plain array).
- **Every key recomputed independently**, in exact arithmetic (Python `Fraction`/`Decimal`, SymPy),
  never by trusting the game's own explanation or computed key. Generators (Prime Sprint's tap logic,
  Shape Shifter's rotations, Factor Race's pairs) were enumerated in full or run in node on the
  game's own code.
- **Every check in the contract**, per item: key correct; options (four distinct, key once, none equal
  in value to the key, none a second valid answer); stated precision (SR-1); money form (canon §7.1.3);
  words, picture and key agree (SR-6). Pictures were checked by recording the canvas/SVG drawing calls
  and, where it mattered, rendering in Chromium (`angle-ace`: all 75 diagrams rendered and every label
  measured against the angle it sits in).
- **Marking code read for every game**, and reproduced in Chromium where a fault depends on it
  (tap tolerances, the rotation keys, tile marking, Prime Sprint's acceptance).
- **Levels.** Every level the game offers was audited, because a picker card lets a resit student
  reach any of them. The card's own level is the priority, and each fault names its level. Four cards
  are `link` cards (no picker; the link sets `?level=`): `factor-race`, `prime-factorisation`,
  `percentage-flip` (Starter) and `expected-damage` (Foundation). Their other levels are not reachable
  from `/resit/`.
- **Line numbers.** Every HIGH/CRITICAL line reference, and a sample of the rest, was checked against
  the source at `6ee0bd6`. One auditing agent's references for `decimal-detective`, `negative-number-line` and `think-of-a-number` had
  drifted by up to 34 lines and were corrected by the reviewing session.
- **Script names** in the per-game sections refer to the auditing session's scratchpad (not
  committed). Every fault states its evidence inline, so it can be reproduced from the source alone.

**Severity.** CRITICAL: a correct answer marked wrong (or a wrong one right) on 10% or more of a level's
questions, or the game unplayable. HIGH: a wrong key, an unanswerable question, a second valid answer
or a value-equal option (a student marked wrong for being right, or right for being wrong). MEDIUM:
picture/words disagree with the key, unstated precision, money form, a wrong explanation. LOW:
cosmetic or teaching-quality notes. "Judgement call" marks a finding whose severity depends on a
ruling, not on arithmetic.

## Summary

| Game | Card opens at | Levels audited | C | H | M | L | Headline |
|---|---|---|---|---|---|---|---|
| `shape-shifter` | single level | 4 modes, 45 items | 2 | 1 | 1 | 1 | Every rotation keyed the wrong direction; taps select the wrong option |
| `correlation-or-coincidence` | single level | 13 questions (no real levels) | 1 | 0 | 2 | 5 | Phase 1 unanswerable: labels hidden until after the answer |
| `equation-builder` | Foundation (picker) | ks3, gcse, level4 (40 each) | 1 | 1 | 3 | 3 | Slot-order marking rejects equal arrangements (29/120); gcse_013 key wrong |
| `angle-ace` | Starter (picker) | year6 40, gcse 35 | 0 | 6 | 7 | 1 | Keys right, diagrams contradict them (20/40 Starter, 22/35 GCSE have a picture fault) |
| `better-value` | GCSE (picker) | gcse 20, core 50 | 0 | 5 | 4 | 3 | Five Core conclusions wrong (009, 031, 036, 037, 049); GCSE keys all right |
| `given-that` | GCSE (picker) | gcse 25, alevel 25, core 20, level4 20 | 0 | 3 | 0 | 3 | alevel_18 Venn/key disagree; free entry ±0.005 with no precision stated |
| `probability-pioneer` | single level | year6 45 | 0 | 2 | 2 | 4 | MATHS/GAMES keyed 2/5 (answer 3/5); "equally likely ⇒ 0.5" keyed True |
| `decimal-detective` | single level | year6 45 | 0 | 2 | 2 | 2 | Marker starts on the answer (2 items); ±0.05 accepts the next tick |
| `estimation-golf` | Starter (picker) | year6, ks3, gcse, alevel, level4 | 0 | 2 | 3 | 5 | Cylinder keyed with π = 3.14 (L4); first-principles estimate keyed as the limit (A-Level) |
| `negative-number-line` | single level | year6 45 | 0 | 1 | 1 | 0 | Place It ±0.5 marks 0 and 1 correct for 0.5 |
| `estimation-engine` | single level | one pool of 49 | 0 | 1 | 3 | 3 | √(e × 1000) keyed 52.07 (52.137); 1-s.f. estimates marked wrong (decision) |
| `expected-damage` | Foundation (link) | ks3 15, gcse 20, core 15 | 0 | 1 | 1 | 5 | Two GCSE ties keyed to A only; outcome draw ignores shown probabilities when they sum < 1 |
| `formula-unlocked` | GCSE (picker) | gcse 29, alevel 25, level4 14 | 0 | 1 | 0 | 7 | alevel :297 distractor equal to the key, marked wrong |
| `sequence-solver` | Foundation (picker) | ks3 50, gcse 50, alevel 54 | 0 | 1 | 2 | 5 | alevel :291 "0.999..." marked wrong against 1; 15 GCSE questions show raw LaTeX |
| `proportion-blaster` | GCSE (picker) | gcse 50, alevel 50 | 0 | 1 | 0 | 6 | alevel :242 keyed 450/11 (900/11); no correct option |
| `linear-equation-solver` | GCSE (picker) | gcse 141 | 0 | 1 | 1 | 0 | All keys right; valid alternative first moves marked wrong (judgement call) |
| `unit-converter` | GCSE (picker) | gcse 48, alevel 38, level4 42 (one pool of 58) | 0 | 0 | 2 | 3 | π = 3.14 and 3 s.f. used without being stated |
| `like-terms-collector` | single level | year6 45 | 0 | 0 | 2 | 3 | Two emoji show a different fruit from the label |
| `formula-forge` | GCSE (picker) | gcse 29, alevel (= gcse), level4 16 | 0 | 0 | 1 | 6 | Keys right; hint prose loses spaces (known, B7) |
| `percentage-flip` | Starter (link) | year6 20, default 12 | 0 | 0 | 1 | 3 | Keys right; SKIP during feedback marks the next question wrong unseen |
| `four-quadrant-explorer` | single level | year6 45 | 0 | 0 | 1 | 1 | Keys right; "(0,0)" overprints the −1 labels on phones |
| `new-shapes` | single level | year6 50 | 0 | 0 | 1 | 4 | Keys right; prism "l" arrow on the wrong edge |
| `factor-race` | Starter (link) | year6 20, ks3 2,694 pairs | 0 | 0 | 0 | 3 | Keys right; no ties possible |
| `formula-plug-in` | single level | year6 50 | 0 | 0 | 0 | 3 | Keys right |
| `think-of-a-number` | single level | year6 50 | 0 | 0 | 0 | 2 | Keys right |
| `prime-factorisation` | Starter (link) | year6 20, ks3/gcse 28 | 0 | 0 | 0 | 2 | Every correct factorisation accepted, every wrong tap rejected |
| **Total** | | | **4** | **29** | **40** | **83** | |

## Bug classes seen across games (CLASS CHECK input for the fix contracts)

Each of these shapes appears in two or more games, so by the contract's own test each is a class,
and the fix contracts should address the shared layer rather than the call sites.

1. **Games without verifiers ship wrong keys.** 16 of the 26 games had a HIGH or CRITICAL fault. Every
   fix batch should add the game's `scripts/verify-<slug>.py` to CI in the same PR, as earlier
   batches did (`check-verifier-coverage.py` then holds it there).
2. **Typed answers marked by game-local code, not `MaffsAnswer`** (canon §7.1.3, SR-1): `given-that`
   (±0.005, no precision stated), `percentage-flip` (±0.01), `formula-plug-in` (`parseFloat ===`),
   `like-terms-collector` (`parseInt`, so 5.9 passes for 5), `new-shapes`. The shared answer checker
   exists; these games are not on it.
3. **Position tolerance on a number line** wider than half the tick gap: `negative-number-line`,
   `decimal-detective`. This is canon §7.1.2's rule ("never wide enough to accept a named wrong
   answer") applied to a tap instead of a typed value; it has no shared implementation.
4. **Marking by structure, not value:** `equation-builder` (slot by slot), `linear-equation-solver`
   (one valid move), `angle-ace` phase 2 (one reason; `multiReason` is never read). A correct answer
   in another valid form is marked wrong.
5. **Value-equal options that B11 cannot see:** `sequence-solver:291` ("0.999..." against 1),
   `formula-unlocked:297` (s/t − ½at against (2s − at²)/(2t)). Both are outside what
   `bank_common.parse_value()` reads. Distractor-against-distractor pairs: `proportion-blaster` (4),
   `formula-forge` (3), `formula-unlocked` (3), `probability-pioneer` (2), `given-that` (2).
6. **Pictures drawn by hand per question, not from the question's data:** `angle-ace`, `new-shapes`
   (prism), `correlation-or-coincidence` (r stated ≠ r of the plotted data on 11 of 13),
   `given-that` alevel_18 (Venn regions ≠ stored totals). SR-6 failures are invisible to every
   checker that reads only the key.
7. **Unstated π ≈ 3.14 and unstated rounding:** `unit-converter` (:166, :183, :178),
   `estimation-golf` (:680), `given-that` (whole free-entry mode).
8. **An unknown `?level=` silently serves another bank:** `unit-converter`, `factor-race` (gcse plays
   ks3), `sequence-solver` (level4 plays ks3), `estimation-golf` (core plays ks3), `angle-ace` (ks3
   plays gcse), `percentage-flip` (ks3/gcse play a shared default bank). The roster lists levels that
   do not exist; tier 1 loads them without error, so nothing has caught it.
9. **Wrong-answer advance not on `MaffsNext`** (canon §7.6): noted in most of the 26 games; not
   counted as a fault here.

## Proposed fix batches, in order

Ordered by harm to a resit student: first what breaks marking at the card's own level game-wide, then
wrong keys at the card's level, then wrong keys a student reaches from the picker, then the rest.

1. **Batch 1: marking broken game-wide at the resit level.**
   - `shape-shifter`: rotation direction (`rotatePoint` or the labels), tap selection (choose the
     option whose own label/interior was tapped, never "first match"), duplicate-shape options
     (`shapesEqual` on vertex sets).
   - `equation-builder`: mark by value (SymPy-equivalent forms are equal), not slot by slot; fix
     gcse_013's key. Class 4.
   - `correlation-or-coincidence`: needs Jon's ruling first (below), then show the variables before
     the choice.
2. **Batch 2: wrong keys at the card's level.** `probability-pioneer` (Q20 and the 0.5 statement),
   `angle-ace` Starter diagrams (L293, L437, L423/444/465), `decimal-detective` and
   `negative-number-line` together (class 3: one rule for a tap tolerance), `estimation-engine` :276.
3. **Batch 3: wrong keys reached from the picker.** `better-value` Core (five), `given-that`
   (alevel_18, and free entry onto `MaffsAnswer.decimal` with a stated precision: class 2),
   `proportion-blaster` :242, `formula-unlocked` :297, `sequence-solver` :291, `estimation-golf`
   :663/:680, `expected-damage` ties, `angle-ace` GCSE diagrams.
4. **Batch 4: MEDIUM.** Raw LaTeX in `sequence-solver` GCSE (15 questions), `unit-converter` precision
   and π, `correlation-or-coincidence` r values, `percentage-flip` SKIP race, `expected-damage` outcome
   draw, `like-terms-collector` emoji, the remaining `angle-ace` picture faults.
5. **Batch 5: LOW**, and the `?level=` fallbacks (class 8) as one roster-and-checker change.

## Decisions for Jon

These are judgement calls the audit cannot settle; each blocks or shapes a fix. **Jon ruled on all
eight on 4 Oct 2026**; each ruling is recorded under its item, and the fix batches in `docs/todo.md`
START apply them. Decisions 3 and 5 are canon SR-13 (§0.3).

1. **`correlation-or-coincidence`:** are the hidden labels meant as a "guess first" mechanic? If so,
   it should not be scored or ranked. If not, show the variable names before the choice. Also: the
   "suicides by hanging" pair is played for laughs in its Phase 2 jokes (L138–140); a safeguarding
   question for a resit audience.
   - **Jon's ruling (4 Oct 2026):** show the variable names before the choice. The "suicides by
     hanging" pair is removed (done, PR #36). Withdrawn from `/resit/` pending the rebuild.
2. **`estimation-engine`:** the `/resit/` card advertises GCSE estimation (N14: round each number to
   1 s.f.). The game's 1–5% bands mark that method wrong on 21 of the 27 KS3, GCSE and π items, and 10
   of 49 items need e, φ, ln or log (φ never defined). Keep it on `/resit/`, re-band it, or move it?
   - **Jon's ruling (4 Oct 2026):** withdrawn from `/resit/` pending rebuild (done, PR #36), under
     SR-12, marked by an exact match to the method's answer(s).
3. **`linear-equation-solver`:** is "×2 first" for x/2 + 5 = 11, or ÷(−1) for −x + 6 = 10, a correct
   move? Today it is marked wrong (14 questions; 63 of 141 if "divide first" on 3x + 7 = 22 is also
   ruled correct).
   - **Jon's ruling (4 Oct 2026): SR-13.** Any operation applied to both sides is valid and accepted,
     except × 0 and ÷ 0 (blocked, with an explanation); a valid move that makes the problem harder
     scores full marks and is followed by a nudge towards a neater move. So "×2 first", ÷(−1) and
     "divide first" are all correct moves.
4. **`probability-pioneer` Stage 3:** "If two outcomes are equally likely, each has probability 0.5"
   is keyed True. True only if there are exactly two outcomes; as worded it teaches the 50-50
   misconception. Reword or rekey?
   - **Jon's ruling (4 Oct 2026):** rekey as False, with an explanation: the probability is 0.5 only
     when there are exactly two outcomes; each face of a dice is equally likely, at 1/6. **Done, PR #45.**
5. **`equation-builder`:** when a question says "write the equation", is an equivalent rearrangement
   (`d = 80 ÷ tan 34°`) correct, and may the sides be swapped?
   - **Jon's ruling (4 Oct 2026): SR-13.** Equivalent rearrangements and swapped sides are accepted
     unless the question specifies the form. Withdrawn from `/resit/` pending the rebuild (done, PR #36).
6. **`decimal-detective` (todo §1.49):** the marking risk does not occur (equal cards are accepted in
   either order). What remains is content: identical cards at :256 (1.9), :261 (0.6), :263 (0.11) and
   equal-value pairs 0.77/0.770 (:267), 0.44/0.440 (:269). Intended?
   - **Jon's ruling (4 Oct 2026):** remove the identical cards; keep the equal-value pairs (0.77/0.770),
     with feedback that trailing zeros don't change the value.
7. **`expected-damage`:** two GCSE questions have equal expected values; rekey as "either" or change
   the numbers (SR-5 says comparisons never tie)?
   - **Jon's ruling (4 Oct 2026):** change the numbers so no comparison ties (SR-5).
8. **`estimation-golf` Starter:** 8 of 20 items are general knowledge with no maths (continents 7,
   class size 30). Is that the level a resit card should open at?
   - **Jon's ruling (4 Oct 2026):** the `/resit/` card opens at Foundation (done, PR #42;
     `check-resit-page.py` pins it in `RULED_LEVEL`). The general-knowledge Starter items are to be
     replaced in a later batch.

---

# Per-game findings

In `/resit/` page order. Line numbers are `games/<slug>/index.html` unless stated.


### Negative Number Line (`negative-number-line`)
Resit card level: year6 (single level). Levels audited: year6 (the only level): 15 Place It + 15 Order Them + 15 Calculate = 45 items. Bank type: static (three arrays, `games/negative-number-line/index.html:281-319`); sessions of 10/20/30 cycle place, order, calc (`buildQuestions`, :361), so a 30-question session uses 10 of each with no repeats.
Marking:
- Place It: tap snapped to the nearest 0.5 (`Math.round(val*2)/2`, :550), correct if `|placed - target| <= 0.5` (`confirmPlace`, :583).
- Order Them: each tile's `parseFloat(dataset.value)` compared with `answer[i]` by position (`checkOrder`, :774-801).
- Calculate: four buttons, the clicked number `=== data.answer` (`selectCalcOption`, :859). Distractors are built at run time (:806-853) from start+val, start-val, -answer and answer±1, ±2.
Items checked: all 45, recomputed with exact integer arithmetic (`scratchpad/work/extract.js`; output in `scratchpad/work/negative-number-line/check.txt`). Order: each `answer` equals `nums` sorted, and no duplicates. Calc: start ± val equals the answer, and the start and answer are both on the -10..10 line. Place: targets distinct and in range. Every calc item's distractor candidate set has at least 3 distinct values other than the key, so the random pad loop (:837) never runs. The Place It tolerance was enumerated for every target (`scratchpad/work/negative-number-line/place-tolerance.txt`) and reproduced in Chromium (`scratchpad/work/repro.py`, `scratchpad/work/repro-out.json`).

#### Faults
- **F1 [HIGH]** year6 / Place It, :282 (targets `0.5` and `-0.5`); marking at :550 and :583
  - Question: "Place 0.5 on the number line" (and "Place -0.5 …"). The line has a labelled tick at every integer from -10 to 10.
  - Keyed answer: 0.5. But the game also marks the whole-number ticks 0 and 1 correct (for -0.5, it marks -1 and 0 correct).
  - Evidence: a placement snaps to a multiple of 0.5, and the game accepts a placement within 0.5 of the target. For 0.5 that accepts {0, 0.5, 1}. Reproduced in Chromium: tapping 1 shows the marker label "1" and the feedback "Correct!", and the score goes up. The same happens at 0 for 0.5, and at -1 and at 0 for -0.5. So putting -0.5 at -1 or at 0, the misconception this item tests, is marked right.
  - Share affected: 2 of 15 Place It items (2 of 45 items).
- **F2 [MEDIUM]** year6 / Place It, all integer targets (:282), same marking (:550, :583)
  - Question: e.g. "Place -3 on the number line".
  - Keyed answer: -3. Also accepted: -3.5 and -2.5. The marker's own label shows "-2.5" when the game says "Correct!".
  - Evidence: `|−2.5 − (−3)| = 0.5 <= 0.5`. Reproduced: tapping -2.5 shows the label "-2.5" and "Correct!"; tapping -2 is rejected. The half-unit band is probably meant to forgive a slightly-off tap. But the placement is snapped and labelled, so the student sees a wrong value accepted. Judgement call: a tolerance of 0.25 would still forgive the tap and reject the half-way points.
  - Share affected: 13 of 15 Place It items, whenever the student places on a half-way point.

#### Clean
- Order Them: 15/15 answers equal `nums` sorted ascending. No equal values in any set. Positional numeric compare is sound.
- Calculate: 15/15 keys correct (start + or - val). Start and answer are both on the -10..10 line, so the start marker and the post-answer arrow are drawn on the line.
- Calc options: the key appears once, there are 4 distinct integers on every item, and no distractor equals the key. The click compares numbers (`selected === correct`), not rendered strings.
- Feedback text: "Correct position was X", "Correct order: …" and "start ± val = answer" all state the right answer. After answering, the picture's arrow runs from the start to the key.
- Numbers display through `formatNum`: integers bare, halves to 1 d.p. (0.5, -0.5). No display/key mismatch.

#### Not checked / limits
- Touch drag on a real device was not exercised; the tap/click path was (Chromium, desktop viewport).
- LOW notes, not faults:
  - Some Calculate distractors lie off the drawn line (11, -11, 12, -12; 5 of the 15 Calculate items, :303-319). They are plausible wrong answers, but cannot be placed on the picture.
  - The pad loop at :837 is rejection sampling (CLAUDE.md), but it is unreachable with this bank.
  - The wrong-answer Next is a plain button, not `MaffsNext` (no 3s floor, canon §7.6).

**Reviewing session re-check:** F1 re-checked: taps snap to the nearest 0.5 (:550) and are accepted within ≤ 0.5 (:583); for the target 0.5 the snapped values 0 and 1 pass.


### Decimal Detective (`decimal-detective`)
Resit card level: year6 (single level). Levels audited: year6 (the only level): 15 Line-Up + 15 Round Up + 15 Place It = 45 items. Bank type: static (`games/decimal-detective/index.html:254-306`); sessions of 10/20/30 cycle the three types (`buildSession`, :343).
Marking:
- Line-Up: the card at each position is compared numerically with `sorted[i]` (`Math.abs(user - sorted) < 1e-9`, `checkLineup` :762-780).
- Round Up: string compare, `selectedOption === data.answer` (`checkRoundup` :782-797; the option string goes through `data-option`).
- Place It: `|min + markerPos*range - value| <= 0.05`, absolute, the same for every line (`checkPlaceit` :799-827). The marker is continuous, with a live 2 d.p. readout (`setMarkerPosition` :738-748).
Items checked: all 45 (`scratchpad/work/decimal-detective/check.py`, output in `check.txt`). Line-Up was re-sorted with `Decimal`. Every rounding was recomputed with `Decimal` half up (tenths, whole numbers, 2 d.p., 1 s.f.); the options were checked for presence and for equal values. For Place It: the range, tick size, tolerance in ticks, and whether the starting marker already sits on the answer. Reproduced in Chromium: `scratchpad/work/repro.py`, `scratchpad/work/repro2.py` (outputs `repro-out.json`, `repro2-out.json`).

#### Faults
- **F1 [HIGH]** year6 / Place It, :301 (`{value:4.5,min:4,max:5}`) and :305 (`{value:5.5,min:5,max:6}`); start state :630-641, Check enabled :425
  - Question: "Place 4.5 on the number line from 4 to 5" (and 5.5, from 5 to 6).
  - Keyed answer: 4.5 / 5.5. The marker starts at 50% of the line, which is exactly the answer, already labelled "4.5" / "5.5". The Check button is enabled on load (:425; `renderPlaceit` never disables it).
  - Evidence: pressing Check with no input gives "Correct! Case solved." in Chromium for both items. So a free mark, and the starting picture pre-announces the answer.
  - Share affected: 2 of 15 Place It items.
- **F2 [HIGH]** year6 / Place It on the 0 to 0.5 line, :299 (`0.15`) and :300 (`0.45`); tolerance :803
  - Question: "Place 0.15 on the number line from 0 to 0.5" (and 0.45).
  - Keyed answer: 0.15 / 0.45. The fixed ±0.05 tolerance is a whole tick on this line (ticks every 0.05), so the neighbouring ticks are accepted as well.
  - Evidence (Chromium, `repro2-out.json`): for 0.15, the marker reading "0.10" and the marker reading "0.20" are both "Correct! Case solved.". For 0.45, "0.40" and "0.50" are both correct. 0.4 and 0.5 are exactly the truncate/round-up confusions the item tests.
  - Share affected: 2 of 15 Place It items.
- **F3 [MEDIUM]** year6 / Place It, hundredths targets on a 0.1-tick line: :293 (`0.25`), :294 (`0.75`), :302 (`1.25`), :303 (`2.75`); also every other 0-1 item
  - Question: e.g. "Place 0.25 on the number line from 0 to 1".
  - Keyed answer: 0.25. The ±0.05 band reaches both neighbouring tenths ticks, so a marker reading "0.20" or "0.30" is accepted. For 0.3, the band accepts the reading "0.25".
  - Evidence: reproduced in Chromium (`repro2-out.json`): 0.25 with the marker at "0.20" and at "0.30" are correct; 0.3 at "0.25" is correct.
  - Share affected: 4 of 15 Place It items at the tick boundaries (the half-tick band on the other 0.1-tick items is a judgement call).
- **F4 [MEDIUM, judgement call]** year6 / Place It, all 15; `setMarkerPosition` :738-748
  - The marker shows its exact value to 2 d.p. as it moves. Only 3 ticks are labelled (min, middle, max). So any item can be solved by dragging until the label reads the target, without reading the scale. That breaks "a visual aid must never give the answer away" (CLAUDE.md, Scaffolds).
- **F5 [LOW]** year6 / Round Up, :283 (7.895 to 2 d.p.)
  - Options: 7.89 / 7.90 / 7.895 / 7.9. Key "7.90".
  - "7.9" is equal in value to the key and is marked wrong. The ask names the form ("Round to 2 decimal places"), so this is allowed by the audit's form rule (SR-4). Listed so Jon can confirm it is intended.
- **F6 [LOW]** year6 / Round Up, :280 (9.50 to the nearest whole number)
  - Options: 9 / 10 / 9.5 / 9.50. Key "10" is correct, but two distractors (9.5 and 9.50) are the same value, so the student effectively has 3 distinct choices.
- **F7 [LOW] (todo §1.49)** year6 / Line-Up: :256 (`1.9` twice), :261 (`0.6` twice), :263 (`0.11` twice); also :267 (`0.77` and `0.770`) and :269 (`0.44` and `0.440`), which are equal in value
  - **The marking risk §1.49 feared does not occur.** `checkLineup` compares values by position (:769-777), so either order of two equal cards is accepted. Reproduced: `1.09, 1.099, 1.9, 1.9, 1.99` gives "Correct! Case solved.". No student is marked wrong.
  - What remains is content. Two identical cards in a five-card line-up look like a typo, and the wording "smallest to largest" with a tie may unsettle a weak student. The pattern of the other rows (x, x.0y, x.yy, x.y0y, x.0yy) suggests 1.909, 0.66/0.606-style and 0.101-style values were intended; for example, :256 probably meant `1.909`. The two trailing-zero pairs (0.77/0.770, 0.44/0.440) may be deliberate teaching that a trailing zero does not change the value. Jon to rule; replacement values are content.
  - Share affected: 5 of 15 Line-Up items (3 identical strings, 2 equal values).

#### Clean
- Line-Up: 15/15 `sorted` arrays are the correct ascending order (`Decimal` compare), and each is a permutation of its suspects.
- Round Up: 15/15 keys correct under half-up rounding, including the exact-half cases: 4.95 to 5.0, 9.50 to 10, 3.145 to 3.15, 7.895 to 7.90, and 12.8 to 10 at 1 s.f. The key appears exactly once in every option list. Marking compares raw strings: the button's `data-option` and the key are the same literal, so no rendering mismatch.
- Place It: 15/15 targets lie within their line. Tick labels from `formatPlaceit` are correct (0, 0.25, 0.5 / 2, 2.5, 3 …). After answering, the target ring and tolerance zone are drawn at the key.

#### Not checked / limits
- Touch drag on a real device was not exercised; click, and `setMarkerPosition` driven directly, were.
- LOW notes, not faults:
  - Wrong-answer feedback is only "Not quite. Check the evidence." On Line-Up the correct order is never shown (only per-position green/red), so the pause has nothing worth reading (canon §7.6).
  - Line-Up's Check is enabled on load, so a shuffle that happens to come out sorted (1/120, or more with duplicates) scores with no move.

**Reviewing session re-check:** F1 re-checked: the marker starts at 50% (:630-631) with Check enabled (:425); the targets 4.5 on 4–5 (:301) and 5.5 on 5–6 (:305) are the midpoints. F2 re-checked: fixed tolerance 0.05 (:803) on the 0–0.5 line (:299-300).


### Think of a Number (`think-of-a-number`)
Resit card level: year6 (single level). Levels audited: year6 (the only level): 50 puzzles (10 one-step, 20 two-step, 20 three-step). Bank type: static (`games/think-of-a-number/index.html:257-414`). Sessions of 10/20/30 draw 2/4/4, 4/8/8 and 6/12/12 (`buildQuestionSet` :464).
Marking: typed on a digits-only numpad (max 4 digits, no minus sign or decimal point). `parseInt(input) === q.answer` (`submitAnswer` :588-589). Game-local exact integer compare; not `MaffsAnswer`, but every key is a positive whole number, so no precision or format question arises.
Items checked: all 50 (`scratchpad/work/think-of-a-number/check.py`, output in `check.txt`), each with exact `Fraction` arithmetic:
- (a) the steps run forward from the key reach the stated result;
- (b) an independent backward solve from the result reaches the key;
- (c) every intermediate value is a whole, non-negative number;
- (d) the key can be typed on the pad;
- (e) the displayed wording matches the stored operation and value;
- (f) every worked "Undo:" line is true arithmetic, chains from the result, inverts the right step in reverse order and ends at the key;
- (g) no duplicate puzzles or ids.
Every operation is a bijection, so each puzzle has exactly one answer.

#### Faults
- **F1 [LOW]** All levels, keyboard handler :558-577 with `showResults` :685-734. Not a maths fault.
  - On the results screen, `answered` is still true, so pressing Enter calls `nextQuestion()`, which returns to the reveal screen. "Continue to Results" then runs `showResults()` again, which re-fires `game_completed` and calls `MaffsLeaderboard.submitScore` a second time for the same run.
  - Evidence: reproduced in Chromium (`scratchpad/work/think-of-a-number/repro.py`). After one 10/10 run, Enter then Continue gives 2 `submitScore` calls and 2 `game_completed` events.
- **F2 [LOW]** :404 (ton_047, "×2, +8, ÷3 = 8", key 8)
  - The key equals the stated result, so a student who types the result back (a common non-attempt) is marked correct. The key itself is correct (8×2=16, 16+8=24, 24÷3=8). Teaching note only.

#### Clean
- 50/50 keys correct (forward and backward). All intermediates are whole and non-negative, and all keys are positive integers of at most 2 digits.
- 50/50 worked "Working backwards" explanations are arithmetically true, chain correctly from the result, and end at the key.
- 50/50 displayed steps match the stored operation and value.
- No duplicate puzzles; 50 unique ids.

#### Not checked / limits
- The on-screen numpad Enter does not advance after an answer (it calls `submitAnswer`, which returns); the Next button and the physical Enter key do. The wrong-answer Next is a plain button with no 3s floor (canon §7.6) and the physical Enter skips it. Not a correctness fault.


### Factor Race (`factor-race`)
Resit card level: year6 (Starter). Levels audited: year6 (static bank, 20 pairs, 10 drawn per session); ks3 (generator, table of 2,694 ordered pairs from 2..60); gcse (the page has no gcse branch: `?level=gcse` and any value other than `year6` runs the ks3 generator and submits as `ks3`, index.html:204). Bank type: mixed (static year6 + exhaustive-table generator).
Marking: `guess(choice)` at index.html:319-325 compares `getFactors(a).length > getFactors(b).length` (computed at run time from the shown numbers, not from the bank comments); B is treated as correct whenever A does not have strictly more factors, so a tie would mark B right and A wrong.
Items checked: all 20 year6 pairs (both numbers' divisor counts recomputed with sympy `divisor_count`, winner, tie, and the inline comment's claim); all 2,694 ks3 ordered pairs (sympy recompute, ties counted); the game's own `VALID_PAIRS` re-run in node (same 2,694, 0 ties). Scripts: scratchpad/work/factor-race/check.py, scratchpad/work/factor-race/g.js.

#### Faults
- **F1 [LOW]** all levels, index.html:131 vs :176
  - Start screen says "You have 5 seconds per question — don't overthink it!"; `TIME_PER_Q = 30000` (30 s; also the roster/timer policy's 30 s). Words disagree with behaviour. Not a key fault.
  - Share affected: every session (instructions only).
- **F2 [LOW]** all levels, index.html:307-316, :339-348
  - On a time-out the game shows "TOO SLOW!" and both factor counts, but never marks which card was the right one (`revealCards(-1)` adds no class). On a wrong tap the right card is highlighted but only the counts ("6 factors") are shown, not the factors themselves, and the game advances on a fixed 1.6 s timer (canon §7.6 `MaffsNext.wrong` not applied). Teaching-quality/policy note, not a key fault.
- **F3 [LOW]** gcse, index.html:204
  - `?level=gcse` (a roster level) silently runs the ks3 game and submits/logs as level `ks3`. No GCSE content exists. Not a key fault; noted because the roster lists GCSE.

#### Clean
- year6: 20 of 20 pairs keyed correctly; 0 ties; the winner in every inline comment and both counts match sympy (including the pairs where B wins: 15/16, 16/12, 45/36, 26/24).
- ks3/gcse: 2,694 of 2,694 possible pairs have different divisor counts, so no tie can ever be shown; the tie behaviour (B wins) is unreachable. Margin between counts: 1 in 358 pairs (13%), 2 or more otherwise.
- No 1 or 0 can be drawn (PAIR_MIN = 2); `getFactors` includes 1 and n, matching the start screen's definition and examples (12 -> 6 factors, 7 -> 2).
- Double tap guarded by `answered` (index.html:320).
- No rejection sampling (table built once, uniform pick).

#### Not checked / limits
- Layout/phone fit not measured (out of scope). Level label on the start screen vs the /resit/ card ("Starter") not checked here.


### Prime Sprint (`prime-factorisation`)
Resit card level: year6 (Starter). Levels audited: year6 (`NUMBERS_YEAR6`, 20 targets, index.html:212); ks3 and gcse (both resolve to level `all` and `NUMBERS_DEFAULT`, 28 targets, index.html:211, :215-217). 8 targets drawn per session. Bank type: static target lists (not a generator: extract found no bank because the lists are plain numbers, not objects with `correct`).
Marking: `pressPrime(p)` at index.html:268-325. A tap is accepted iff `(currentTarget / product) % p === 0`, i.e. p divides what is left; the target is complete when `product === currentTarget`. Order-free, no overshoot possible, a non-dividing tap costs a life and is not multiplied in.
Items checked: all 48 targets (20 + 28) factorised with sympy: every prime factor is on a button (2, 3, 5, 7, 11, 13), none is prime or below 4, no duplicates. Acceptance: (a) python model, every ordering of every target's prime multiset (301 orders) completes with no rejection; (b) the game's own `pressPrime` run in node with DOM stubs, depth-first over every reachable tap state x every button, under `?level=year6`, `ks3`, `gcse` (786 + 2,964 + 2,964 taps): every tap accepted iff p divides the remainder, 0 mismarks. Scripts: scratchpad/work/prime-factorisation/check.py, scratchpad/work/prime-factorisation/g.js.

#### Faults
- **F1 [LOW, judgement call]** all levels, index.html:276
  - When a student taps a prime that divides the target but is already used up (e.g. target 12, taps 2, 2, then 2 again), the message is "2 is not a factor here!". 2 is a factor of 12; what is meant is "of what is left (3)". After question 3 the running product is hidden (index.html:249-257), so the student cannot see "what is left" either. Wording, not a key fault; reachable on every target with a repeated or used-up prime.
- **F2 [LOW]** all levels, index.html:283-287, :345-349
  - On running out of lives the game ends with "Out of lives!" and never shows the target's factorisation. Teaching-quality note.

#### Clean
- 48 of 48 targets are composite and fully buildable from the six prime buttons (largest: 210 = 2x3x5x7, 132 = 2x2x3x11; year6 includes 22 = 2x11 and 26 = 2x13).
- Every correct factorisation is accepted in any order (301 of 301 orders); repeated factors handled (product tracks multiplicity); every wrong tap rejected (0 mismarks in 6,714 tap states across the three level URLs).
- The completion line `n = p x q x ...` (index.html:309) lists exactly the taps made, which multiply to n.
- Example on the start screen (60 -> 2, 2, 3, 5) is correct.
- Integer arithmetic only: `currentTarget / product` is always exact because `product` divides the target by construction.

#### Not checked / limits
- Layout and phone fit not measured. Level label on the start screen vs the /resit/ card not checked.


### Estimation Engine (`estimation-engine`)
Resit card level: none (card says "One level", links to `/games/estimation-engine/`, spec N14–N16). Levels audited: the one pool of 49 items (index.html:226-279; source comments group them 12 "KS3", 20 "GCSE", 17 "A-Level / Core Maths"), 10 drawn at random per game, every event logged as level `all`. The page has no level picker and ignores `?level=` (roster lists KS3, GCSE, Core). Bank type: static.
Marking: typed, `parseFloat(input.value)` (index.html:360, `type="number"` input), `err = |val - ans| / ans * 100`, hit iff `err <= q.tol` (index.html:388-389). Band is relative to the stored key `ans`, not to the true value. A miss shows "x% off. Answer: <ans>" (index.html:401) and advances on a fixed 2 s timer (index.html:409).
Items checked: 49 of 49 keys recomputed with sympy to 15 s.f. (exact rationals/roots/powers; e, π, φ, ln, log10 symbolic); every band printed; the meter's labels re-derived; GCSE N14 1-s.f. estimates tested against the 27 KS3/GCSE/π items; float behaviour at the band edges run in node. Scripts: scratchpad/work/estimation-engine/check.py, scratchpad/work/estimation-engine/est.py.

#### Faults
- **F1 [HIGH]** A-Level/Core block, index.html:276
  - Question: "√(e × 1000)", "Within 4%". Typed.
  - Keyed answer: 52.07   Correct answer: 52.137 (52.14 to 2 d.p.)
  - Evidence: e × 1000 = 2718.2818…, √2718.2818 = 52.1371. Key is 0.13% low. The miss/timeout message prints "Answer: 52.07" (wrong). Marking effect is small: the band is [49.99, 54.15] instead of [50.05, 54.22], so 54.16–54.22 (within 4% of the truth) is marked wrong and 49.99–50.05 marked right.
  - Share affected: 1 of 49 items (drawn in about 20% of games).
- **F2 [MEDIUM]** all items, index.html:377 then :343
  - The tolerance meter's centre label is set to "Correct" and then overwritten by `updateMeter` with `Math.round(ans)`, so the label under the answer marker shows the key rounded to a whole number. For six items that rounded value is itself outside the band, i.e. the picture shows as "the answer" a value the game marks wrong: log₁₀(500) shows 3 (key 2.699, 11.2% off, tol 3%); e² shows 7 (key 7.389, 5.3%); e × π shows 9 (key 8.54, 5.4%); ln(100) shows 5 (key 4.605, 8.6%); φ² shows 3 (key 2.618, 14.6%); log₁₀(π × 100) shows 2 (key 2.497, 19.9%). (The text flash above it does give the right key.) The min/max labels are likewise whole-number rounded (e.g. φ²: "1 … 3 … 4").
  - Share affected: 6 of 49 items show a centre label outside the band; 16 of 49 show a label different from the key.
- **F3 [MEDIUM, judgement call]** whole pool, index.html:226-279, :291
  - A-Level content is served to everyone, with no level choice. 10 items need e, φ, ln or log₁₀ (e × 100, φ × 1000, ln(1000), log₁₀(500), e², e × π, ln(100), φ², √(e × 1000), log₁₀(π × 100)); φ is never defined on screen and is on no GCSE/Core spec. A 10-question game contains at least one of these with probability 0.92 (expected 2.0 per game); at least one item from the 17-item A-Level block with probability 0.99 (expected 3.5). For the resit audience these are effectively unanswerable. Not a wrong key.
- **F4 [MEDIUM, judgement call]** KS3/GCSE items, tolerances at index.html:228-260
  - The resit card describes "Quick estimates of calculations" and maps the game to GCSE N14 (estimate by rounding to 1 significant figure). With tolerances of 1–5%, the N14 estimate is rejected on 21 of 27 KS3/GCSE/π items (e.g. 847 × 23 ≈ 800 × 20 = 16,000, 17.9% off, tol 5%; 314 × 159 ≈ 300 × 200 = 60,000, 20.2% off; 12 × 15 ≈ 10 × 20 = 200, 11.1% off; π × 100 ≈ 3 × 100 = 300, 4.5% off, tol 3%; 2¹⁰ ≈ 1000, 2.3% off, tol 1%). The game rewards near-exact mental calculation, not N14 estimation; a resit student doing the taught technique is marked wrong almost every time. Design/spec-fit issue for Jon, not a key error. Table in est.py output.
- **F5 [LOW]** index.html:388
  - Float edge: an entry exactly on the stated band edge is rejected for 9 of the 16 integer keys tested (e.g. 12, tol 2%: 11.76 gives err 2.0000000000000018 > 2). Only an exact-edge entry is affected.
- **F6 [LOW]** index.html:357-361
  - `submitAnswer` cancels the question timer before checking the input; an empty or unparseable entry (e.g. "19,481" in a number field reads as empty) returns silently with no message, and the question then never times out. No mark is given either way.
- **F7 [LOW]** index.html:409
  - Wrong answers advance on a fixed 2 s timer with only "x% off. Answer: …" (canon §7.6 `MaffsNext.wrong` not applied). The start screen has no instructions beyond "Press Start" and the "Within n%" tag.

#### Clean
- 48 of 49 keys are correct to the precision stored (all integer keys exact; 1234/17 = 72.588 -> 72.6, 1000/7 -> 142.86, e×100 -> 271.83, φ×1000 -> 1618, π² -> 9.87, ln 1000 -> 6.908, log₁₀500 -> 2.699, e² -> 7.389, √(1000π) -> 56.05, 2500π -> 7854, eπ -> 8.54, ln 100 -> 4.605, φ² -> 2.618, π³ -> 31.006, log₁₀(100π) -> 2.497, 100π -> 314.16); key rounding error ≤ 0.02% on all of them, far inside every band.
- No band accepts an order-of-magnitude slip (×10 or ÷10 is ≥ 90% off) or the obvious wrong-operation slips checked (18 × 20 = 360 and 18 × 18 = 324 for 18 × 19 are both rejected at 5%; 144 − 12, 3 × 4 for 3⁴, 2 × 10 for 2¹⁰ all far outside).
- Meter geometry: zone width 2×tol % on a track spanning ans ± 50% is correct; marker position matches the computed error.
- Expressions are unambiguous as written (no operator-precedence traps; √(144 × 25) bracketed).

#### Not checked / limits
- No rounding instruction exists or is needed (tolerance-marked), so SR-1 does not apply.
- Whether Chrome lets a student type a comma into the `type="number"` field depends on locale; F6 is from the code path, not a device test.

**Reviewing session re-check:** F1 re-checked: :276 `ans:52.07`; √(1000e) = 52.1371.


### Estimation Golf (`estimation-golf`)
Resit card level: year6 ("Choose: Starter"; the picker's Starter button). Levels audited: year6 (20 items, 9 drawn per round, index.html:617-637); ks3 shown as "Foundation" (9, :639-648); gcse (9, :650-659); alevel (9, :661-670); level4 (9, :672-682). `core` (on the roster) does not exist: `?level=core` falls back to ks3 (index.html:716) and the picker has no Core button. Bank type: static. The 9-item banks are played in the same fixed order every round.
Marking: proximity, not right/wrong. `pct = |guess - answer| / answer * 100` (index.html:778), first band with `pct <= b.pct` (BANDS, :689-697): exact = Hole in One (1 stroke), ≤1% Eagle (2), ≤5% Birdie (3), ≤10% Par (4), ≤20% Bogey (5), ≤35% Double (6), else Triple (7); +1 for a hint. Analytics logs `correct = strokes ≤ 3`, i.e. within 5% (:788). The result panel shows "Actual answer: <answer>" (:818).
Items checked: 56 of 56 keys (36 non-year6 recomputed with sympy exact arithmetic; 20 year6 facts checked by hand); named wrong answers run through the game's own BANDS code in node. Scripts: scratchpad/work/estimation-golf/check.py, scratchpad/work/estimation-golf/bands.js.

#### Faults
- **F1 [HIGH]** level4, index.html:680
  - Question: "A cylinder has diameter 60 mm and length 200 mm. Estimate its volume in cm³." Hint: "V = π × r² × h. r = 3 cm, h = 20 cm".
  - Keyed answer: 565.2   Correct answer: 565.49 (180π = 565.4867…)
  - Evidence: the key uses π = 3.14, which neither the question nor the hint states. A student using π (calculator) gets Eagle (2 strokes) not Hole in One, and is told "Actual answer: 565.2 cm³", which is wrong.
  - Share affected: 1 of 9 level4 items (every level4 round).
- **F2 [HIGH]** alevel, index.html:663
  - Question: "Estimate the gradient of y = x³ at x = 3 using first principles with h = 0.001."
  - Keyed answer: 27   Correct answer: 27.009001 (the estimate asked for)
  - Evidence: ((3.001)³ − 27) / 0.001 = 27.009001. 27 is the exact derivative (the limit), not the h = 0.001 estimate; the student who does what is asked gets Eagle and is shown "Actual answer: 27". (A central difference would give 27.000001, but "first principles with h" normally means the forward difference.) Judgement on the method wording; the key is the limit either way.
  - Share affected: 1 of 9 alevel items (every alevel round).
- **F3 [MEDIUM]** ks3, gcse, alevel; index.html:640, :643, :651, :662, :665, :669
  - Questions that ask for a specific rounding are scored by proximity, so wrong roundings score under par and are logged as correct. Through the game's own code: "Round 3,847 to the nearest hundred" (key 3800): 3900 (rounded the wrong way), 3840, 3850 and the unrounded 3847 all score Birdie (1.0–2.6%); "Estimate √50 to 1 decimal place" (7.1): 7 and 7.2 Birdie; "Round 0.004857 to 2 significant figures" (0.0049): 0.0048 (truncated) and 0.005 Birdie, 0.00486 (3 s.f.) Eagle; "e to 4 s.f." (2.718): 2.719, 2.72, 2.7 all Eagle; "ln(10) to 2 d.p." (2.30): 2.31 Eagle; sphere "to the nearest whole number" (268): 269 Eagle. Only the exact key earns Hole in One, so a correct answer is still distinguished, but the named rounding errors are rewarded as under-par (canon 7.1.2: a band must not accept a named wrong answer). Judgement call on game design.
  - Share affected: ks3 2 of 9, gcse 1 of 9, alevel 3 of 9.
- **F4 [MEDIUM]** level4, index.html:673, :677, :681 (and :680)
  - No precision is stated, yet only the stored rounding earns Hole in One: RMS 325/√2 = 229.8097 keyed 229.8; Xc = 1/(2π·50·100µF) = 31.831 keyed 31.8; R = 0.1/(0.6×2) = 0.08333… keyed 0.0833. A more precise correct answer (229.81, 31.83, 0.08333) scores Eagle. SR-1 (state the precision) not met. Keys are correct to their stored rounding.
- **F5 [MEDIUM, judgement call]** year6 (the resit card's level), index.html:617-637
  - The Starter bank is mostly general-knowledge recall, not estimation (the card maps the game to GCSE N14–N16): football team 11, adult teeth 32, spider legs 8, bones 206, pizza slices 8, letters in the alphabet 26, continents 7, pupils in a class 30 (8 of 20 have no maths content); most of the rest are unit facts (60, 100, 1000, 24). Factual keys needing Jon's check (convention-dependent, not wrong as such): continents 7 (5 or 6 under other conventions; the hint lists 7), class size 30 (the hint says 25–35; England averages are in the mid-20s), adult teeth 32 (full set including wisdom teeth), door 200 cm (UK standard internal door is 1,981 mm, 1% off). Proximity scoring blunts the effect (28 for class size is Par).
- **F6 [LOW]** year6, index.html:603-613, :756
  - Hole topics come from `HOLES_META` by hole number, but the year6 bank is shuffled, so labels are arbitrary (e.g. "How many legs does a spider have?" under "Rounding" or "Percentages"). alevel and level4 are also mismatched in fixed order (alevel hole 2 "Percentages" = first-principles gradient; hole 3 "Large Numbers" = trapezium rule; hole 4 "Powers & Roots" = ln 10; hole 7 "Time & Rates" = sin 30°; level4 hole 1 "Rounding" = RMS voltage). ks3 and gcse match.
- **F7 [LOW]** all levels, index.html:811
  - The error line formats the difference with `toFixed(2)`, so small answers show "(-0.00)" or "(+0.00)": e.g. 0.0048 for 0.0049, 2.719 for 2.718, 0.08 for 0.0833. The percentage alongside is right.
- **F8 [LOW]** alevel, index.html:666
  - "Estimate the speed (m/s) of sound in air at 20°C (≈ 343 m/s)." gives the answer in the question.
- **F9 [LOW]** alevel, index.html:665: key 2.30 displays as "Actual answer: 2.3" (JS number), losing the 2 d.p. the question asks for.
- **F10 [LOW]** core / bank size: `?level=core` silently plays ks3 (labelled "Foundation"); ks3, gcse, alevel and level4 have 9 items each, so every round at those levels is the same 9 questions in the same order.

#### Clean
- ks3: 9 of 9 keys correct (3,847 -> 3,800; 15% of 200 = 30; 86,400 s; √50 = 7.071 -> 7.1; 3,500 mm; 96p ÷ 8 = 12p; 30 miles; 63 cm²; 1,800 g ÷ 12 = 150 g).
- gcse: 9 of 9 correct (0.0049; 193.2; 36,792,000; 5; 120 km/h; 560 g; 15 min; 3.14 × 49 = 153.86 with π ≈ 3.14 stated; 6,300).
- alevel: 8 of 9 correct (e 2.718; trapezium 0.375; ln 10 2.30; 343; S∞ = 6; sin 30° = 0.5; sphere 268.08 -> 268; 8^(2/3) = 4).
- level4: 8 of 9 correct to their stored rounding (229.8; 12 ×10⁻⁶/°C; 680 Hz; wL²/8 = 10 kNm; 31.8 Ω; 29.43 m/s; 75%; 0.0833 K/W).
- year6: 20 of 20 keys are the standard answers (365, 60, 100, 11, 32, 8, 24, 52, 206, 60, 6, 200, 4, 1000, 1000, 8, 26, 7, 30, 21); the 30-day-months (4) and die-dots (21) items checked arithmetically.
- No answer is 0, so the percentage error is always defined; exact entry of every key gives pct = 0 (Hole in One).
- Hints checked: all state correct facts or methods (e.g. ln 10 = ln 2 + ln 5; trapezium values 0, 0.25, 1).

#### Not checked / limits
- Year6 real-world figures were reasoned from general knowledge, not a cited source; F5's factual notes are for Jon.
- Leaderboard is held (lower-is-better), so scoring direction on the boards was not examined.

**Reviewing session re-check:** F1 re-checked: :680 keys 565.2; π × 3² × 20 = 565.487. F2 re-checked: :663 keys 27; ((3.001)³ − 27)/0.001 = 27.009001. The reviewing session rates F2 as a key/wording disagreement with a small marking effect (proximity scoring) rather than a wrong answer as such.


### Unit Converter (`unit-converter`)
Resit card level: gcse (`/resit/` card `?level=gcse`, picker). Levels audited: gcse 48 questions (L+A+V+T), alevel 38 (A+V+T), level4 42 (L[0..3]+A[0..4]+V+T+E). Bank type: static. The 5 arrays (L 10, A 15, V 15, T 8, E 10 = 58 distinct questions, `index.html:110-185`) are shared; the levels are slices of one pool (`startGame`, `:188-191`), 20 drawn per session. The extract's "58 per level" is the whole pool, not what each level serves.
Marking: multiple choice, `btn.dataset.val===q.c` (`:210`). Options are `shuffle([q.c,...q.d])` (`:205`) and set as both `dataset.val` and `textContent` from the same string, so a key click always matches.
Items checked: all 58 questions. Each key was recomputed from my own conversion table in exact `Fraction` arithmetic (π taken as 3.14 only where the question says so), and every option was parsed to (value, unit) to check four distinct strings, four distinct values, a unit that matches the ask, and thousands-comma grouping. Script: `scratchpad/work/unit-converter/check.py` (bank dumped by node from `:110-185` into `bank.json`).

#### Faults
- **F1 [MEDIUM]** gcse and alevel and level4 (T bank), `:166`
  - Question: "Cylinder: radius 10 cm, height 0.5 m. Volume in cm³?" Options 15,700 cm³ / 1570 cm³ / 157,000 cm³ / 157 cm³
  - Keyed answer: 15,700 cm³. Correct answer: π·10²·50 = 15,707.96… cm³ (15,708 to the nearest cm³). 15,700 is only exact with π ≈ 3.14.
  - Evidence: the worked solution uses 3.14, but the question does not say so. Its two neighbours (`:165`, `:168`) do say "(π ≈ 3.14)". A student using the π key gets 15,708, which is not offered. 15,700 is still clearly the closest option, so they are not marked wrong, but words and key disagree.
  - Share affected: 1 of 48 (gcse), 1 of 38 (alevel), 1 of 42 (level4).
- **F2 [MEDIUM]** level4 only (E bank), `:183`
  - Question: "A shaft has diameter 25 mm. Cross-sectional area in m²?" Options 0.000491 / 0.491 / 0.00491 / 4.91 m²
  - Keyed answer: 0.000491 m². Exact: π·0.0125² = 0.00049087… m². The key is right to 3 s.f., but neither the precision nor π is stated.
  - Share affected: 1 of 42 (level4).
- **F3 [LOW]** level4 only, `:178`
  - Question: "Convert 60 mph to m/s (1 mile = 1609 m)". Keyed 26.8 m/s; exact 96,540/3600 = 26.8166… m/s. No precision is stated. As multiple choice it cannot mislead (the distractors are 60, 16.1 and 96.5), so it is LOW.
  - Share affected: 1 of 42.
- **F4 [LOW, cosmetic]** thousands separators are inconsistent inside one question, `:166`: "15,700" and "157,000" have commas but "1570" does not. Every comma that is present is grouped correctly (checked on all 232 option strings).
- **F5 [LOW, not a key fault]** `:107` takes any `?level=` value. An unknown key (for example `?level=ks3`) falls into the `else` branch and serves the level4 bank, and `endGame` then prints "undefined" for the level name (`:214`, `lvl[level]`). The /resit/ card uses `gcse`, so it is unaffected.

#### Clean
- Keys: 57 of 58 equal the exact conversion. The 58th, `:178`, is a rounded value with the precision not stated (F3). The other two rounded keys (`:166`, `:183`) are correct under π ≈ 3.14 or to 3 s.f. (F1, F2). Every area factor (10², 100², 1000²) and volume factor (10³, 100³, litre = 1000 cm³, m³ = 1000 litres) is right.
- Options: 58 of 58 questions have 4 distinct strings and 4 distinct values. No distractor equals the key in value, and none is a second valid answer.
- Units: every option carries the unit the question asks for. The only variation is "1 litre" singular at `:152`, which is fine.
- Marking: the string compare cannot fail on a correct click, because the key and the button come from the same string.
- Worked solutions (`s`) and misconception notes (`mc`): all 58 read. Each states the keyed answer with correct working. The `:183` and `:178` steps round as noted above.

#### Not checked / limits
- Nothing is drawn (no figures), so there are no picture-versus-words checks.
- Wrong-answer flow: the game uses its own "Got it — next" button (`:211`), not `MaffsNext` (canon §7.6). That is outside a key audit and is noted only.


### Formula Plug-In (`formula-plug-in`)
Resit card level: year6 (single level, shown as "Starter"; `LEVEL='year6'`, `index.html:358`). Levels audited: year6, 50 questions. Bank type: static (`QUESTIONS`, `:282-352`). Sessions of 10, 20 or 30 are drawn by shuffle and slice (`:430-431`).
Marking: a typed answer on an on-screen keypad (digits and `.` only, at most 8 characters, `:491-499`), marked by `parseFloat(inputValue) === q.answer` (`:516-517`). Game-local code, not `MaffsAnswer`. Every key is a whole number, so "24", "24.", "24.0" and "024" are all accepted.
Items checked: all 50 questions. Each `formulaKatex` was parsed to SymPy, the stated variable values were substituted exactly, and the result was compared with `answer`. I also checked that the formula's letters are exactly the given variables, that every worked step after the first evaluates to the key, that the substitution step uses the given values in order, and that the last step states the key. No two questions are duplicates (same formula and values). Script: `scratchpad/work/formula-plug-in/check.py` (bank dumped by node into `bank.json`). The checker flagged 10 lines (fpi_006-010, fpi_026-030) on its "values in order" test. All 10 are false positives from the formula's own constant (`2(5 + 3)`, `4 \times 5`), and I checked each by eye: they are correct.

#### Faults
None at HIGH or CRITICAL.
- **F1 [LOW]** year6, `:513-517` (marking): an input of "." alone is submitted, `parseFloat('.')` is `NaN`, and it is marked wrong. It counts as an attempt, sends `question_answered correct:false` and shows "Not quite". Canon §7.1.3 never marks an unreadable answer. This is the only unreadable input the keypad allows.
- **F2 [LOW, teaching quality, judgement call]** the bank has no negatives, decimals, fractions, squares of negatives or order-of-operations traps. Every value is a positive whole number and every answer is a positive whole number (largest 200). There is no minus key on the keypad (`:229-241`), so a negative answer could not be typed at all if one were added. The audit watched for negatives and order of operations: none occur. Area of a square is the only power (s², s = 5 to 9), and P = 2(l + w) is the only bracket.
- **F3 [LOW, judgement call]** answers repeat inside a formula: 4 of the 5 perimeter-of-a-rectangle questions answer 28 (`:292-295`), and the speed questions answer 20, 20, 8, 9, 9 (`:305-309`). Not wrong, but a student can learn the answer rather than substitute.

#### Clean
- Keys: 50 of 50 equal the exact substitution (SymPy).
- Formula letters match the given variables in 50 of 50 questions. No question is unanswerable.
- Worked steps (shown on a wrong answer, KaTeX, `:551-553`): in 50 of 50, every step after the first evaluates to the key, and the last step states it. The triangle steps "A = ½ × 24" and so on are correct.
- Wrong-answer flow: `MaffsNext.wrong` (`:569`). Enter goes through `nextCtl.advance()` (`:665`).
- Marking: a whole-number key cannot be rejected when typed correctly. Leading zeros and a trailing "." are tolerated, which is harmless.

#### Not checked / limits
- No pictures in the game.
- Only one level exists, so there is nothing else to audit.


### Like Terms Collector (`like-terms-collector`)
Resit card level: year6 (single level; all events use `'year6'`, `index.html:343`). Levels audited: year6, 45 questions: Stage 1 Fruit 5 (`:250-254`), Stage 2 Letters 10 (`:258-267`), Stage 3 Full 30 (`:271-300`). Bank type: static. Questions are served in the fixed bank order, never shuffled. Stage 3 options are shuffled (`:397`), and Stage 3 has checkpoints after 10 and 20 questions.
Marking:
- Stages 1-2: two `<input type="number">` boxes (`:378`). Each is read with `parseInt(value,10)` (`:415`). An empty or unreadable box makes the check return silently, so nothing is marked (`:417`). The answer is correct only if both match `answers` (`:424`).
- Stage 3: multiple choice, `chosen===answer` on the same string the button was built from (`:442`), so a correct click always matches.
Items checked: all 45 questions.
- Stage 1: each emoji group was summed and its Unicode name read, then compared with the labels and keys.
- Stage 2: each expression was parsed to SymPy, and the coefficient of each labelled letter was compared with the key.
- Stage 3: each expression and every option were parsed to SymPy. I checked that the key equals `expand(expr)`, that the key is fully simplified (each letter once, no zero term, no `1x`), that there are 4 distinct strings and 4 distinct values, and that no distractor is algebraically equal to the expression.
- Script: `scratchpad/work/like-terms-collector/check.py` (bank dumped by node into `bank.json`).

#### Faults
None at HIGH or CRITICAL.
- **F1 [MEDIUM]** Stage 1, `:253` (picture and words disagree, SR-6)
  - Question: "8 🍒 + 1 🍒 + 6 🪣 + 4 🪣", input boxes labelled "cherries" and "plums".
  - The second emoji is `🪣` = U+1FAA3 **BUCKET**, not a plum (Unicode has no plum emoji). Students see buckets under a box labelled "plums". The keys (9, 10) are right for the counts shown. U+1FAA3 is Unicode 13 (2020), so older school devices may show an empty box instead.
  - Share affected: 1 of 5 Stage 1 questions.
- **F2 [MEDIUM]** Stage 1, `:252` (picture and words disagree, SR-6)
  - Question: "4 🍋 + 3 🍋 + 5 🥝 + 2 🥝", boxes labelled "lemons" and "limes".
  - The second emoji is U+1F95D **KIWIFRUIT**, not a lime. The keys (7, 7) are right for the counts shown.
  - Share affected: 1 of 5 Stage 1 questions.
- **F3 [LOW]** Stages 1-2, `:415` (marking): `parseInt` truncates a decimal, so typing "5.5" or "5.9" where the key is 5 is marked correct. The keys are whole counts, so the risk is small, but it is a wrong answer marked right.
- **F4 [LOW, judgement call]** wrong-answer feedback is only "The correct answer is X" (`:432`, `:451`), with no working shown. The Next button appears at once (`:469-471`), without `MaffsNext` or its 3s floor (canon §7.6). Not a key fault.
- **F5 [LOW]** Stage 2 and 3 expressions are plain text, not KaTeX (`:371`, `:393`). Canon §7.1.1 asks for KaTeX on expressions. This is display only; the keys are not affected.

#### Clean
- Stage 1: 5 of 5 keys equal the summed counts. The 🍊 TANGERINE labelled "oranges" is acceptable.
- Stage 2: 10 of 10 keys equal the SymPy coefficients. A bare letter (`y`, `m`, `q`) is correctly read as coefficient 1.
- Stage 3:
  - 30 of 30 keys equal the expanded expression (SymPy).
  - 30 of 30 keys are fully simplified, including `5m` (`:297`) and `8a` (`:300`), where one letter cancels to zero.
  - 30 of 30 have 4 distinct option strings and 4 distinct values. No distractor is algebraically equal to the key, and none is a reordering of it.
- Marking: Stage 3's string compare cannot fail on a correct click. In Stages 1-2 an empty box is never marked.

#### Not checked / limits
- Emoji rendering was not checked on real devices; the Unicode names come from Python's `unicodedata`.
- There is no other level.


### Linear Equation Solver (`linear-equation-solver`)
Resit card level: GCSE (the only level; picker has one button, `gcse`, line 112). Levels audited: gcse, 141 questions
(55 one-step, 86 two-step; ids A1-Y6, 25 id-families in 10 tags). Bank type: static (generated offline by
`scripts/gen-linear-equations.py`, pasted between the GENERATED BANK markers, lines 157-303).
Marking: each phase renders the question's own `opts` with `dataset.val = o`; `btn.dataset.val === correctVal`
(lines 360-389). Key and options come from the same array, so no string-form mismatch is possible. Wrong pick:
penalty, the keyed move is written into the working trail anyway, worked solution at the end (lines 395-451).
Items checked (script `scratchpad/work/linear-equation-solver/check.py`, bank dumped by `dump.js` straight from the
source with node): every equation solved with SymPy (141); every move phase (227) with all 908 offered moves
applied to both whole sides of the current equation; every intermediate `line` (86) compared side-by-side with the
result of applying the keyed move; that the equation is x = solution after the last move (141); every final
`ans` key and its 4 options (141 x 4, compared by value); every non-text line of every worked solution solved
again; the verb and number of every `\text{...}` step and of every hint against its keyed move; duplicate equations.

#### Faults
- **F1 [HIGH, judgement call]** gcse, two-step shapes M, U, V and Y1 (lines 227-232, 274-280, 295): a second valid
  first move is offered and marked wrong, and it gives a clean integer equation.
  - Example (M1, line 227): `x/2 + 5 = 11`, "What do you do to both sides?" Options `-5`, `+5`, `×2`, `÷2`.
    Keyed: `-5`. Also correct: `×2` (multiply both whole sides by 2) gives `x + 10 = 22`, then `-10` gives x = 12.
  - U1 (line 274): `-x + 6 = 10`, options `-6`, `+6`, `×(-1)`, `÷(-1)`. Keyed `-6`. Both `×(-1)` and `÷(-1)` give
    `x - 6 = -10`, a standard valid move: two valid moves marked wrong in each of U1-U4.
  - V1 (line 278): `x/4 + 9 = 5`, `×4` gives `x + 36 = 20`. Y1 (line 295): `(2/3)x + 4 = 10`, `×3/2` gives `x + 6 = 15`.
  - Evidence: check.py applies each offered move to both sides and finds the equation one step from solved
    (structure a·x+b=c with a=1) with integer coefficients.
  - Share affected: 14 of 141 questions (M1-M6, V1-V3, U1-U4, Y1), ~10% of the level. The hint ("Clear the 5 first")
    shows the convention is intended (the generator offers the swapped order as the "wrong order" misconception,
    `gen-linear-equations.py:187-204`), but the ask does not say "first step in the usual order", and a student
    who multiplies through first is doing correct algebra and is penalised 25 points and loses the clean streak.
- **F2 [MEDIUM, judgement call]** gcse, two-step shapes L, P, Q, R, T, X, Y2-Y6 (lines 215-226, 247-265,
  271-273, 285-300): the same "other order" move is offered and marked wrong; it is valid algebra but gives
  fractions. Example L1 (line 215): `3x + 7 = 22`, options `-7`, `+7`, `÷3`, `×3`; keyed `-7`; `÷3` (every term)
  gives `x + 7/3 = 22/3`, which still solves to x = 5. Share: 49 of 141 questions. Whether "divide first" counts as
  a correct move is Jon's ruling; if it is ruled correct, F1+F2 together are 63 of 141 questions (45%, 63 of the 86
  two-step questions), which is over the CRITICAL threshold. A fix that keeps the misconception would be an ask
  that names the convention, or replacing that distractor with an invalid move (e.g. `÷3` applied to the
  x-term only is the real misconception, but the button cannot show that).

#### Clean
- Keys: 141/141 equations have the keyed final answer equal to the SymPy solution.
- Keyed moves: 227/227 keyed moves are valid and make progress; after the last move every equation is x = solution.
- Intermediate lines: 86/86 `line` equations equal the keyed move applied to the previous line (both sides).
- Options: every move phase has 4 distinct options with the key present once (227); every answer phase has 4
  options, key once, no two equal in value (141).
- No offered move in the brackets shapes (N, O, W) or the one-step shapes is a second valid move.
- Worked solutions: every equation line in every `sol` solves to the key; every `\text{Subtract/Add/Multiply/
  Divide ... n}` step matches its keyed move in verb and number (227); every hint names the keyed operation.
- No duplicate equations in the bank.

#### Not checked / limits
- Visual rendering (KaTeX) not rendered in a browser; strings were parsed as LaTeX by the script only.
- "Progress" for F1/F2 is defined as reducing the a·x+b=c structure count; a move such as `÷2` on `-2x = 8`
  (giving `-x = 4`) is counted as no progress, so it is not reported.

**Reviewing session re-check:** F1 is a judgement call (Decisions for Jon, item 3); the algebra in the evidence was not disputed.


### Equation Builder (`equation-builder`)
Resit card level: ks3 (shown as "Foundation"; `?level=ks3` auto-clicks the button, line 382). Levels audited: ks3 40
(20 assembly, 20 gap-fill), gcse 40 (24 + 16), level4 40 (24 + 16); 120 questions. Bank type: static (lines 215-343).
Marking: `checkAnswer` (lines 505-554) compares each non-prefilled slot to the key by string, position by position:
`slotValues[i] === currentQ.slots[i]`. Any other arrangement of the same tiles is marked wrong, however correct.
First wrong attempt: the wrong slots are cleared for one retry (0.5 point); second wrong: key revealed, scored wrong.
Items checked: every key read and modelled against its word problem by hand (120). `scratchpad/work/equation-builder/eb_enum.py`
(SymPy) placed every possible choice of tiles into the empty slots (every permutation, ~13.4M before a grammar
filter), parsed each well-formed result and compared it with the key at 3 random exact points: same value on each
side (reorder or value-equal form), sides swapped, or an equivalent equation (same solution set). Output
`enum.out`, `hits.json`. 110 questions ran automatically; 10 (ks3_014, gcse_031, gcse_039, l4_008, l4_014, l4_021,
l4_023, l4_024, l4_033, l4_034: integrals, sigma, matrices, LCM, two `=` signs) were enumerated by hand.

#### Faults
- **F1 [CRITICAL]** all levels, assembly questions: an equally correct arrangement of the same tiles is marked
  wrong, because marking is slot-by-slot string equality (line 513). Each question below has a correct answer the
  student can build that is not the keyed one (evidence: `hits.json`, class REORDER = both sides equal in value to
  the key's for all inputs):
  - ks3 (9 of 40, 22%): ks3_001 l.217 key `C = 2.50m + 3`, also `C = 3 + 2.50m`; ks3_003 l.219 `T = 45h + 60` /
    `T = 60 + 45h`; ks3_004 l.220 `S = e + (e−4) + 3e` / 5 other orders; ks3_005 l.221 `P = 2(2w + 15) + 2w` /
    `P = 2w + 2(2w + 15)`; ks3_006 l.222 `S = 2n + 18` / `S = 18 + 2n`; **ks3_007 l.223 `A = P ÷ 5` / `A = 2P ÷ 10`**
    (Amy's 2 shares of 10, the more natural form, both tiles on offer); ks3_012 l.228 `s + 2s + (s+30) = 180` /
    5 other orders; **ks3_013 l.229 `M = 48 − ¾×48` / `M = 48 − 36`** (36 is a tile and is ¾ of 48);
    ks3_016 l.232 `F = 4.50 × 2(l+w)` / `F = 2(l+w) × 4.50`.
  - gcse (12 of 40, 30%): gcse_002 l.260 `A = 1.035ⁿ × P`; gcse_003 l.261 `4t + 5p = 167`; gcse_004 l.262
    `t + p = 33.75`; gcse_006 l.264 `1.8² + h² = 6²`; gcse_009 l.267 `(5x−18) + (3x+10) = 180`; gcse_010 l.268
    `P = 4/9 × 5/10`; gcse_012 l.270 `T = 40/32 + 1.5/2`; **gcse_014 l.272 `V = 50 ÷ (8/12)³`** (equal value) and
    `V = (12/8)³ × 50`; gcse_015 l.273 `(2m+3) + m = 39`; gcse_017 l.275 `A = 3.65 × 4.85`; **gcse_018 l.276
    `m = (85−40) ÷ (5−20)`** (= −3, both tiles offered); **gcse_024 l.282 `P = 2×0.3 − 0.3²`** (= 0.51, P(A or B)).
  - level4 (8 of 40, 20%): l4_001 l.301 e.g. `dy/dx = 2 − 10x + 12x²`; l4_002 l.302 `s = c + t² + t³` (5 orders);
    l4_005 l.305 `kt = ln(P₀) − ln(P₀/2)` (= ln 2); l4_006 l.306 `dy/dx = 6x × 5(3x²+1)⁴`; l4_007 l.307
    `dy/dx = 2x·sin(x) + x²cos(x)` (the usual order); l4_010 l.310 `B/(x−2) + A/(x+1)`; l4_016 l.316
    `10x² + 5x + 1` (5 orders); l4_017 l.317 `x + x⁵/5! − x³/3!` (3 orders).
  - Share affected: 29 of 120 questions (ks3 22%, gcse 30%, level4 20%); in each, only the students who choose
    another order are hit. A student marked wrong is shown the key's order on retry, so the game teaches that
    `3 + 2.50m` is wrong.
- **F2 [HIGH]** gcse, line 271 (gcse_013): wrong key.
  - Question: "OABC is a parallelogram where OA = a and OC = c. M is the midpoint of BC. Write the expression for
    the vector OM." Tiles: OM, =, a, +, ½c, −, ×, a+c, ÷, 2c (5 slots).
  - Keyed answer: `OM = a + ½c`. Correct answer: `OM = c + ½a` (½a + c).
  - Evidence: OABC in order, so OB = a + c and CB = OA = a; M is the midpoint of BC, so OM = OC + ½CB = c + ½a.
    `a + ½c` is the midpoint of AB. The correct answer cannot be built from the tiles (no ½a tile).
  - Share affected: 1 of 40 gcse questions.
- **F3 [MEDIUM, judgement call]** questions that say "Write the equation (to find ...)" rather than "a formula for
  X": an equivalent rearranged equation is marked wrong. Examples: ks3_020 l.236 key `3V ÷ 8 = 360`, also
  `3V = 360 × 8`; gcse_006 l.264 `h² = 6² − 1.8²`; gcse_007 l.265 key `tan34° = 80 ÷ d`, also `d = 80 ÷ tan34°`
  (literally "the equation to find d"); gcse_008 l.266 `T × 3×10⁸ = 4.013×10¹⁶`; gcse_016 l.274 `2x² = 15 + 3`;
  gcse_021/022 l.279-280 `40²+55² − 70² = 2×40×55×cosC`; l4_005 l.305 `kt + ln(P₀) = ln(2P₀)`. Side swaps
  (`360 = 3V ÷ 8`, `76.50 = 0.9P`, `0 = (3−λ)(4−λ) − 2`) are also marked wrong (58 of the 110 machine-checked questions offer one). Counts per
  question are in `enum.out` (EQUIV / SWAP lines).
- **F4 [MEDIUM, judgement call]** level4, line 324 (l4_023): "Write the sum 1 + 4 + 9 + 16 + 25 in sigma notation."
  Key `Σ r² r=1 to 5`; the tiles also build `Σ r² r=0 to 5`, whose value is the same 55 (the r = 0 term is 0),
  marked wrong. Whether the extra zero term counts as wrong is a ruling.
- **F5 [MEDIUM, judgement call]** gcse, line 268 (gcse_010): the distractor tiles 5/9 and 4/10 build
  `P = 5/9 × 4/10`, which equals the key 5/10 × 4/9 = 2/9 in value but is the wrong method; marked wrong. A
  value-equal distractor arrangement (canon 7.1 sense). Similar LOW cases: l4_004 l.304 `det(A) = 3×1 + 2×1` (= 5,
  equal to 2×4 − 3×1 by coincidence); l4_012 l.312 `|z| = √18 + √(−9+9)`.
- **F6 [LOW]** gcse, line 266 (gcse_008): key `T = 4.013×10¹⁶ ÷ 3×10⁸`. Read with the usual order of operations
  this is (4.013×10¹⁶ ÷ 3) × 10⁸; it is right only if each standard-form tile is read as one number. No brackets
  shown. Judgement call.
- **F7 [LOW]** the simplest correct answer cannot be built because the slot count is fixed (no Check button until
  every slot is filled): ks3_016 `F = 9(l+w)` (the 9(l+w) tile is a distractor), ks3_018 `O = 0.8T`, l4_005
  `kt = ln(2)`, l4_012 `|z| = √18`. Not marked wrong, but the correct simplified tile is presented as a distractor.
- **F8 [LOW, judgement call]** l4_026 l.328 and l4_034 l.336 (gap-fill operators): `... − c` is as valid a constant
  of integration as `+ c` and is marked wrong.

#### Clean
- Keys model their word problems in 119 of 120 questions (all except F2), checked by hand; numeric values
  re-derived where present (e.g. ks3_006 2n + 18, ks3_019 4n − 3, gcse_022 angle 160° − 40° = 120°, gcse_031
  discriminant 25 + 24, l4_009 (3−λ)(4−λ) − 1×2, l4_020 36x² − 12x, l4_036 6 × 4 = 24).
- Gap-fill questions (52): no alternative tile placement is equivalent except F8 (two machine hits on gcse_034, `−` and `×` in place of `+`, are float-precision artefacts and wrong);
  every gap-fill key is unique among its tiles.
- `?level=ks3` opens the ks3 bank; each level has exactly 40 questions.

#### Not checked / limits
- The enumerator's "zero set" test produced spurious hits where a tile gave a division by zero (e.g. `÷ 0` in
  l4_009, `√(−9+9)` as divisor in l4_012) and in l4_006 / gcse_034 (numeric tolerance); those were read by hand
  and discarded. F1 counts use only the exact same-value test.
- KaTeX rendering of tiles not inspected (tiles are plain Unicode text unless they contain LaTeX patterns).

**Reviewing session re-check:** F1 re-checked: `checkAnswer` compares `slotValues[i]===currentQ.slots[i]` slot by slot (:511-517); ks3_001's key is `C = 2.50m + 3` (:217), so `C = 3 + 2.50m` is marked wrong. F2 re-checked: OM = OC + CM = c + ½a; the key at :271 is `a + ½c`.


**Resolved, PR #49 (5 Oct 2026), Jon's rulings of 4 Oct 21:04:** F1-F8 all fixed at the root. Marking is now a
lookup in each question's ACCEPTED list, which `scripts/verify-equation-builder.py` computes with SymPy from the
tiles (every well-formed arrangement, any length up to the slot count, unused tiles allowed) and CI holds the page
to. F1 and F3: equal-value and equivalent forms and swapped sides accepted (SR-13). F2: gcse_013 now says "midpoint
of AB", so the key a + ½c is right (the verifier checks the geometry). F4: sigma from r = 0 accepted. F5: gcse_010's
5/9 and 4/10, l4_004's 2×1 and l4_012's √(−9+9) replaced; the verifier fails any accepted build that uses a
distractor tile. F6: standard-form tiles display in brackets. F7: Check appears as soon as the built answer is
well formed, leftover tiles allowed. F8: + c and − c both accepted (l4_002, l4_026, l4_034). Also found and fixed:
ks3_029 and l4_026 keys could not be built at all (one + tile for two + slots); l4_034 likewise needed a second −
for − c. Back on /resit/ at Foundation.

### Four Quadrant Explorer (`four-quadrant-explorer`)
Resit card level: year6 (single level; `LEVEL = 'year6'`, line 241). Levels audited: year6 only, 45 items: Plot It 20
(lines 199-204), Read It 15 (lines 206-222), Complete the Shape 10 (lines 224-235). Bank type: static.
Marking: Plot It and Complete the Shape snap the tap to the nearest grid point, clamped to -5..5 (`snapToGrid`,
lines 339-343), then compare integers with tolerance 0.4, i.e. exact (lines 556-559, 632-635). Read It shuffles
the 4 option indices and marks `i === q.correct` (lines 486-496); every `correct` is 0. Shape gives a second try,
no point (lines 641-676).
Items checked: `scratchpad/work/four-quadrant-explorer/check.js` (node, banks read from the source): every plot point is
an integer in -5..5 and distinct (20); every Read It key `opts[correct]` equals "(x,y)" of the drawn point, 4
distinct well-formed options, key once (15); every shape has its right angle at the middle vertex, is
axis-aligned, its answer equals v0 + v2 - v1, no other vertex has a right angle (so the fourth corner is unique),
all in range (10). `play.py` (Playwright, Chromium) played 30-question sessions (all 20 plots, all 15 reads, all
10 shapes, at least once) at 320x568, 390x844 and 1280x800: tapped each keyed point at its computed screen position
and clicked each keyed option; all 150 answers were marked correct; for every Read It the canvas pixel at the keyed
point is the point colour #6366f1. `zoom.py` took 3x close-ups of the origin.

#### Faults
- **F1 [MEDIUM]** year6, all three modes, `drawGrid` lines 389-392: on phone widths the origin label "(0,0)" is
  printed over the -1 tick labels of both axes, so the -1 on the x-axis and the -1 on the y-axis cannot be read.
  - Evidence: "(0,0)" is drawn right-aligned 6px left of the origin and 6px below the x-axis, 12px font, about 26px
    wide; the grid spacing is 20px at 320 wide and 27px at 390 wide, so the -1 labels (centred 20-27px left of the
    origin, and right-aligned 6px left of the y-axis 20-27px below it) sit under it. Close-up `origin_320.png`: the x-axis
    "-1" is printed inside "(0,0)" and the y-axis "-1" overlaps its lower edge; at 1280 (`origin_1280.png`, spacing 48px) the
    labels are clear.
  - Share affected: every question on screens up to roughly 430px wide; the scale is what the student counts from.
- **F2 [LOW, judgement call]** year6, Complete the Shape, `showQuestion` line 506 calls `drawRectOutline` on the
  three given corners: it closes the path, so the student sees a dashed right-angled triangle, diagonal included
  (`shot_390_shape.png`), under "Tap where the fourth corner of the rectangle goes". The geometry is right; the
  drawn diagonal is a line that is not a side of the rectangle. Share: 10 of 45.

#### Clean
- Plot It: 20/20 targets in range and distinct; the tap at each target is marked correct at all three sizes.
- Read It: 15/15 keys equal the plotted point; 4 distinct options each, key once; the point is drawn where the key says.
- Complete the Shape: 10/10 answers complete an axis-aligned rectangle and are the only possible fourth corner; all
  marked correct when tapped; the finished rectangle is drawn in the right vertex order (sorted by angle).
- Quadrant labels Q1-Q4 are in the standard positions; axis numbers -5..5 match the grid lines (1280 close-up).
- Feedback text after a wrong answer states the right coordinate (plot and shape) or option (read).

#### Not checked / limits
- Rendered with CDN fonts blocked (fallback font); in Outfit the "(0,0)" label is of similar width, so F1 should
  still apply, not measured.
- Wrong-answer paths were read in the code, not played.


### Formula Unlocked (`formula-unlocked`)
Resit card level: gcse. Levels audited: gcse (Q_GCSE, 29 questions; 20 drawn per session), alevel (Q_GCSE stages 2-4 = 19 + Q_ALEVEL 6 = 25 distinct; 20 per session), level4 (Q_LEVEL4, 14; all 14 per session). Bank type: static.
Marking: options built by `MaffsOptions.build(correct_override||correct, d)` (index.html:448-449), `dataset.val = v` (:452), click marked by string compare `btn.dataset.val === (q.correct_override||q.correct)` (:475-476). Option strings and key strings are the same literals, so no rendering/format mismatch is possible; a correct-in-value option with a different string is marked wrong.
Items checked: all 49 questions (29 + 6 + 14). For each, with SymPy (`parse_latex`, symbols positive): the keyed rearrangement substituted back into the formula must give an identity; every distractor compared in value with the key and checked against the formula (second valid answer); distractors compared pairwise; every `steps` line (and the bank's own `correct` where `correct_override` is set) checked to hold when the key is substituted. Hints (plain text) read by hand. Mutation self-test: swapping each key for each distractor is caught as a wrong key 145/146 times; the one not caught is the value-equal option in F1. Session pools simulated (20,000 per level) from the `startGame()` logic (:391-413). Scripts: `scratchpad/work/formula_check.py`, `scratchpad/work/formula-unlocked/{check.py,selftest.py,pool_sim.js}`, outputs `check.out`; render check `scratchpad/work/render_check.py` -> `render_out.json`.

#### Faults
- **F1 [HIGH]** alevel, games/formula-unlocked/index.html:297 (Q_ALEVEL[0])
  - Question: s = ut + ½at², "Make u the subject". Options as rendered (confirmed in Chromium): `u = (2s − at²)/(2t)`, `u = s/t − ½at`, `u = st − ½at²` (three options: the bank's `d[2]` is string-identical to `correct_override` and `MaffsOptions.build` drops it, known todo §1.4).
  - Keyed answer: `u = \dfrac{2s - at^2}{2t}` (the `correct_override`). Correct answer: both `u = (2s − at²)/(2t)` AND `u = s/t − ½at`.
  - Evidence: s/t − ½at = (2s − at²)/(2t) identically (SymPy simplify of the difference = 0). Clicking `u = s/t − ½at` in the live page (render check) gives class `opt-btn disabled wrong`, correctN stays 0 and the worked solution is shown. So a student who divides each term by t (a correct method) is marked wrong. Two of the three options are correct in value. Not caught by B11 (its ledger entry for this game is only Q_GCSE[22]); todo §1.4/§1.12 record only the missing fourth distractor and the override, not this.
  - Share affected: 1 of 25 A-level questions, but it is drawn twice over: it sits in the stage-2 pool (5 of 10 drawn) and in the extra `shuffle(Q_ALEVEL).slice(0,5)` (:409), so it appears in about 92% of A-level sessions (1 − 0.5 × 1/6) and twice in about 42%.
- **F2 [LOW]** alevel, index.html:396 and :409 — A-level sessions repeat questions. `bank` already contains all of Q_ALEVEL, and the pool then adds 5 more drawn from Q_ALEVEL, so the same question appears twice in 99.8% of simulated A-level sessions (19,955 of 20,000). gcse and level4: 0 repeats.
- **F3 [LOW]** gcse, index.html:265 (Q_GCSE[22], V = 4/3 πr³, make r the subject): two wrong options equal in value, `r = 3V/(4π)` and `r = V/(4/3 π)` (already in the B11 ledger). Not a wrong mark, but one option is wasted.
- **F4 [LOW]** gcse, index.html:269 (Q_GCSE[23], v² = u² + 2as, make v the subject): wrong options `v = u + √(2as)` and `v = √(u²) + √(2as)` are equal in value for u ≥ 0. Not a wrong mark.
- **F5 [LOW]** level4, index.html:368 (Q_LEVEL4[10], T = 2π√(L/g), make L the subject): wrong options `L = gT/(2π)` and `L = g(T/2π)` are identical in value. Not a wrong mark.
- **F6 [LOW]** gcse, index.html:226 misconception text says "The last distractor is a common error — dividing only the first term by m", but options are shuffled (:449), so "the last distractor" points at nothing the student can see.
- **F7 [LOW]** hints render as plain text (`div.innerHTML = 'Step n: ' + hint`, :467) but some contain raw LaTeX: index.html:302 shows "ln(e^{bx}) = ln(ae^{bx})" with braces; :379 "1/R_T"; :384 is fine. Cosmetic.
- **F8 [LOW]** bank sizes below the platform's 40-50 minimum: gcse 29, alevel 25 distinct, level4 14 (a level4 session is 14 questions, not 20).

#### Clean
- Every keyed rearrangement is correct: 49/49 satisfy their formula exactly (SymPy, positive symbols), including all stage-4 "variable appears twice" items (:278, :282, :286, :290, :315, :319, :377, :382).
- No distractor satisfies the formula (no second valid answer) apart from F1: 0 of 146 other distractors.
- No other distractor equal in value to its key (48/49 questions clean).
- Worked-solution steps: every step line in all 49 questions holds when the key is substituted (consistent working); the bank's `correct` at :297 equals its override.
- Plain-text hints read for all 49: the mathematics in each is right.
- Marking path: no string/format mismatch possible (options and key are the same literals; `correct_override` is used both to build and to mark).

#### Not checked / limits
- Square-root rearrangements key the positive root only (v, r, I, a, T); taken as the intended physical/length reading, not flagged.
- Visual layout of options at phone widths not checked (out of scope).

**Reviewing session re-check:** F1 re-checked: :297, s/t − ½at = (s − ½at²)/t = (2s − at²)/(2t); the question's own `correct_note` lists two of the three equal forms but not this distractor. The checker ledger has B2 and B10 for this line, not this pair.


### Formula Forge (`formula-forge`)
Resit card level: gcse. Levels audited: gcse (Q.gcse, 29: s1 8, s2 8, s3 7, s4 6; session = 6 per stage, so 6+6+6+6 capped by stage size = 24), alevel (identical copy of the GCSE bank, index.html:352), level4 (Q.level4, 16: 4/5/4/3; 16 per session). Bank type: static.
Marking: hand-rolled `shuffle([correct, ...distractors])` (index.html:402), `dataset.val = v` (:405), marked by `btn.dataset.val === q.correct` (:441). No string duplicates in any question (B2 clean), so every question shows four options and the key literal is the option literal.
Items checked: all 45 distinct questions (29 GCSE/A-level + 16 Level 4). Same SymPy method as formula-unlocked: key substituted into the formula gives an identity (for the two chain formulas at :341 and :344 the key was checked against the equation that does not contain the eliminated variable); every distractor compared in value with the key, checked against the formula, and compared pairwise; every `steps` line and every LaTeX `hint2` checked by substituting the key (parse failures were prose prefixes such as "Subtract u:" and were read by hand). Plain-text `hint1`s read by hand. Mutation self-test: 222/222 key-for-distractor swaps caught. Scripts: `scratchpad/work/formula_check.py`, `scratchpad/work/formula-forge/check.py` (output `check.out`), `scratchpad/work/formula-unlocked/selftest.py` run on this bank.

#### Faults
No HIGH or CRITICAL fault.
- **F1 [MEDIUM, known]** all levels, index.html:433: `hint2` is rendered with `rkStr()` (KaTeX maths mode), so prose hints lose their spaces, e.g. "Divide both sides by 4" shows as "Dividebothsidesby4", "y − c = mx. Now divide by m." as "y − c = mx.Nowdividebym." 33 hint2 strings affected; already in the B7 ledger and todo §1.31 counts. Listed because the hint is the scaffold a resit student relies on.
- **F2 [LOW]** gcse/alevel, index.html:246 (v² = u² + 2as, make v the subject): wrong options `v = u + √(2as)` and `v = √(u²) + √(2as)` are equal in value for u ≥ 0. Not a wrong mark.
- **F3 [LOW]** gcse/alevel, index.html:264 (c² = a² + b², make a the subject): wrong options `a = c − b` and `a = √(c²) − √(b²)` are equal in value (c, b > 0). Not a wrong mark.
- **F4 [LOW]** level4, index.html:332 (v² = u² + 2as, make u the subject): wrong options `u = v − √(2as)` and `u = √(v²) − √(2as)` equal for v ≥ 0. Not a wrong mark.
- **F5 [LOW]** alevel, index.html:352: the A-Level button serves the GCSE bank unchanged (comment says "shares GCSE bank and adds more"; nothing is added). Not a correctness fault.
- **F6 [LOW]** level4, index.html:325: `hint1` is plain text and shows raw "P_in". Cosmetic.
- **F7 [LOW, known]** bank sizes below the 40 minimum: gcse 29, alevel 29 (copy), level4 16 (B4 ledger).

#### Clean
- Every keyed rearrangement is correct: 45/45 (SymPy), including stage-4 items :278, :283, :287 (x = (a − yb)/(y − 1)), :295, :299 (compound interest r = 100(ⁿ√(A/P) − 1)) and the Level 4 chains :341, :344.
- No distractor equal in value to its key: 0 of 135. No distractor satisfies the formula (no second valid answer): 0 of 135.
- Worked-solution steps and LaTeX hint2s: all consistent with the key (every equation holds with the key substituted; prose-prefixed lines read by hand).
- Plain-text hint1s: the mathematics in all 45 is right.
- Marking: four distinct options on every question; key compared as the same literal it was built from.

#### Not checked / limits
- Square-root keys take the positive root; accepted as the intended reading.
- Phone layout not checked.


### Sequence Solver (`sequence-solver`)
Resit card level: ks3 (picker label "Foundation"). Levels audited: ks3 50, gcse 50, alevel 54 (154 in all). There is no level4 bank: `QUESTIONS` has only ks3/gcse/alevel (index.html:121-297), and `?level=level4` fails the `QUESTIONS[level]` test at :305, so it silently opens Foundation (confirmed in Chromium: `level` = 'ks3'). The extract's "level4 154" is all three banks merged, not a level. Bank type: static; 20 questions drawn per session (:307).
Marking: `shuffle([q.correct, ...q.d])` (:320), `dataset.val = v` (:322), marked by `btn.dataset.val === q.correct` (:337). Options containing `\`, `^` or `{` are rendered by KaTeX, others as text (:323); the key literal is always the option literal, so no format mismatch. No explanation is shown; the right option is highlighted and the game moves on after 1 s (:342).
Items checked: all 154. Every key recomputed independently in `scratchpad/work/sequence-solver/check.py` (output `check.out`): next term by fitting every simple rule to the shown terms (arithmetic, geometric, constant second difference, Fibonacci-type, primes) and flagging any second rule with a different next term; common difference/ratio and second differences from the terms; kth term and "which term" from a + (n−1)d; type by testing each named family (arithmetic, geometric, quadratic, Fibonacci, square, triangular, cube, powers of 2) against the terms, and checking no distractor family also fits; nth-term keys and distractors parsed with SymPy and tested against the shown terms, plus pairwise value equality; T_n questions evaluated; every A-level AP/GP/sum-to-infinity/sigma/recurrence item hand-encoded with exact Fractions (S_n formulas, first-term-exceeding loops, recurrences iterated, S10/S20 system solved). 9 items whose answer is a formula or a sentence (:248, :249, :262, :271-273, :281, :290, :293) read by hand. Mutation self-test: swapping each key for its first distractor is flagged on 145/145 computed items. Rendering of every question captured in Chromium (`scratchpad/work/render_check.py` -> `render_out.json`).

#### Faults
- **F1 [HIGH]** alevel, games/sequence-solver/index.html:291
  - Question: `0.\dot{9} = \sum_{r=1}^{\infty} 9 \times 10^{-r}` "What does this sum equal?" Options: 1, 0.999..., 9/10, ∞.
  - Keyed answer: 1. Correct answer: 1, and 0.999... is the same number.
  - Evidence: Σ 9×10^(−r) = 0.9/(1 − 0.1) = 1 exactly, and 0.999... is 0.9̇ = 1. Marking "0.999..." wrong is a value-equal distractor, and it tells the student that 0.999... ≠ 1, the opposite of the point the question makes. (0.999... is also the left-hand side of the question as written.)
  - Share affected: 1 of 54 A-level questions (drawn in about 37% of A-level sessions: 20 of 54).
- **F2 [MEDIUM]** gcse, index.html:314 (`seqEl.textContent = q.seq`): the sequence line is written as plain text, so LaTeX in `seq` reaches the student raw (confirmed in Chromium). Worst cases: :219 shows `T_n = 3 \times 2^{n-1}`, :220 `T_n = 5 \times 3^{n-1}`, :229 `T_n = 3 \times 2^n`, :232 `T_n = (-1)^n \times n` (4 questions whose rule is unreadable to a grade 1-3 student). Milder: `n^2` and `T_n` shown raw at :193-196, :209-212, :227-228, :230 (11 more). 15 of 50 GCSE questions in all; canon §7.1.1 requires KaTeX for expressions.
- **F3 [MEDIUM, judgement call]** alevel, index.html:262: "Sum of GP — Which formula when |r| < 1?" Key `S_n = a(1−r^n)/(1−r)`; distractor `S_n = a/(1−r)`. |r| < 1 is precisely the condition for the sum to infinity a/(1−r), so the wording steers a student who knows S∞ to a distractor. The key is defensible only because the distractor is labelled S_n; and a(1−r^n)/(1−r) is valid for every r ≠ 1, so "when |r| < 1" does not single it out. (todo §1.29 fixed this question's earlier value-equal distractor; the wording remains.)
- **F4 [LOW]** alevel, index.html:290: the prompt is set with `textContent` (:318) and contains LaTeX, so it shows "Prove S_n for a = 1, d = 1 gives \dfrac{n(n+1)}{2}" raw (confirmed in Chromium).
- **F5 [LOW, judgement call]** gcse, index.html:233: "3, __, 12, __, 21 — Fill in the gaps", key 3, 7.5, 12, 16.5, 21. Arithmetic is assumed but not stated (the next question, :234, does say "If geometric"). The key is the only linear completion; flagged as wording only.
- **F6 [LOW, known]** gcse, index.html:188 (10, 7, 4, 1 nth term; key 13 − 3n): wrong options `-3n + 10` and `10 - 3n` are equal in value (B11 ledger). Not a wrong mark.
- **F7 [LOW]** level picker vs roster: the roster lists L4 for this game, but there is no Level 4 bank and `?level=level4` opens Foundation (see header). Roster description says A-Level 55q; the bank has 54.
- **F8 [LOW]** wrong answers auto-advance after 1000 ms with no explanation (:342); canon §7.6 asks for a Next control and something worth reading. Not a correctness fault.

#### Clean
- Keys: 153/154 correct with no value-equal alternative (all 50 ks3, all 50 gcse, 53/54 alevel; F1 is the exception).
- Next-term questions (ks3 28, gcse 1): each set of shown terms fits exactly one simple rule family (or several giving the same next term); no question has a second simple rule with a different next term; no distractor equals a next term given by any fitting rule.
- nth-term questions (gcse 19): every key reproduces all shown terms; no distractor reproduces them; only value-equal pair is F6.
- Type questions (ks3 6): key family fits the terms; no offered distractor family fits.
- A-level AP/GP/S∞/sigma/recurrence (45 numeric): all keys match exact recomputation; :253 S8 = 199.21875 -> 199.22 (2 d.p., half up) correct.
- Numeric options: no other pair of options equal in value at any level (checked as exact Fractions, `\dfrac{}{}` parsed).
- Marking: 4 distinct option strings on all 154; key compared as the same literal it was built from.

#### Not checked / limits
- "Second valid answer" for next-term questions was tested against simple rule families only (arithmetic, geometric, quadratic, Fibonacci, primes, pronic); exotic rules were not considered, by design.

**Reviewing session re-check:** F1 re-checked: :291 `correct:'1'`, distractor `'0.999...'`.


### Proportion Blaster (`proportion-blaster`)
Resit card level: gcse (`/games/proportion-blaster/?level=gcse`, picker). Levels audited: gcse (50), alevel (50). Bank type: static (`QUESTIONS` at games/proportion-blaster/index.html:141-246; 20 drawn per session, `startGame()` :257).
Marking: pick-one; `btn.dataset.val === q.correct` (index.html:286). Options are `shuffle([q.correct, ...q.d])` (:272), so the button value is the same string as the key; strings containing `\`, `^` or `{` are rendered with KaTeX, others with textContent (:275). No typed answers. No explanation is shown after a wrong answer; the game moves on after a fixed 1000 ms (:291).
Items checked: 100 of 100. Each key was recomputed by hand from the question's own data and checked by script with exact Rational/SymPy arithmetic. Every option was parsed and compared in value: fractions, surds, money and the percentages; ratios were reduced by their gcd. Scripts: `scratchpad/work/proportion-blaster/bank.js` (pulls the bank from the source, with line numbers), `check.py` (expected keys by source line, key-once, distinct strings, value-equal pairs).

#### Faults
- **F1 [HIGH]** alevel, index.html:242
  - Question: "a : b = 1 : 4. b : c = 2 : 3. a + b + c = 150." / "Find c". Options: 450/11, 50, 60, 150/3
  - Keyed answer: 450/11   Correct answer: 900/11 (≈ 81.8)
  - Evidence: b : c = 2 : 3 = 4 : 6, so a : b : c = 1 : 4 : 6. That is 11 parts, so c = 150 × 6/11 = 900/11. The key 450/11 is 150 × 3/11: it uses c's unscaled 3 over the scaled total of 11. **No option is correct**, so every student is marked wrong on this question. Also, two distractors are equal in value: 50 and 150/3.
  - Share affected: 1 of 50 alevel questions. It appears in 40% of alevel sessions (20 drawn from 50).
- **F2 [LOW]** gcse, index.html:159. Two distractors are equal in value, so the student sees only three distinct values: `10` and `\sqrt{100}` (key 5). Neither is the key.
- **F3 [LOW]** gcse, index.html:187. The distractors `3 : 4 : 5` and `6 : 8 : 10` are the same ratio (key 3 : 4 : 10).
- **F4 [LOW]** gcse, index.html:188. The distractors `5 : 4 : 3` and `10 : 8 : 6` are the same ratio (key 5 : 8 : 6).
- **F5 [LOW]** alevel, index.html:225. The distractors `2 : 5 : 7` and `6 : 15 : 21` are the same ratio (key 6 : 15 : 35).
- **F6 [LOW]** alevel. The context line is written with `textContent` (:268), so raw LaTeX is visible to the student: "y ∝ x^{3/2}" (:201). Bare carets show in "x^n" (:209, :218, :219, :223, :224), "x^2 ... a/2" (:239) and "Q^a" (:244). This is cosmetic, and canon §7.1.1 (KaTeX scope) applies.
- **F7 [LOW]** both levels. A wrong answer gets no working or explanation. It auto-advances after 1000 ms (:291), with no Next control (canon §7.6). This is teaching quality, not a key fault.

#### Clean
- Keys: 99 of 100 match an independent exact recomputation. The one that does not is F1. :229 £5627.54 = 5000 × 1.03⁴ = 5627.544…, and the ask states 2 d.p. :192 9261 and :237 £4913 are exact.
- Key present exactly once, 4 distinct option strings: 100 of 100.
- No distractor is equal in value to its key: 100 of 100.
- No distractor is a second valid answer. In :159 and :164, x = −5 is not offered.
- Marking cannot reject a correct click: the button value is the key string itself (:274, :286).
- Money: every pence amount is shown to 2 d.p. (£195.50 at :190, £5627.54 and £5636.36 at :229). Whole pounds have no .00, which is allowed.

#### Not checked / limits
- KaTeX rendering of options was not inspected visually; I checked the strings only.
- The game has no drawn figures, so there was no picture to check.

**Reviewing session re-check:** F1 re-checked: :242, a:b:c = 2:8:12 = 1:4:6, c = 6/11 × 150 = 900/11; keyed 450/11; no option equals 900/11.


### Better Value (`better-value`)
Resit card level: gcse (`/games/better-value/?level=gcse`, picker; the default without `?level` is core). Levels audited: gcse (20), core (50). Bank type: static (`QUESTIONS` at games/better-value/index.html:258-1112). Sessions are 10, 20 or 30 questions, capped at the pool size (:1146, :1191).
Marking: pick one of 4 conclusion cards. `el.dataset.correct === 'true'` (:1258), set from each conclusion's `correct` boolean (:1230); the order is shuffled per question. A wrong pick shows `q.explanation` and `MaffsNext.wrong` (:1307-1310). A right pick moves on after 1200 ms and never shows the explanation. No typed answers.
Items checked: all 70 questions (gcse 20, core 50). Every one has exactly 1 correct conclusion out of 4. I recomputed every figure in every keyed conclusion and every explanation with exact Fractions: totals, unit rates, break-evens and paybacks. I checked each distractor for being false, or for being a second true statement, and scanned the money format. core_046 (tax) is also covered by verify-better-value-tax.py; I rechecked it here (£1,294.44 and £1,161.11, which match). Scripts: `scratchpad/work/better-value/bank.js` → `bank.json`, `dump.txt` (every question as the student sees it), `recompute.py` (all the figures, plus the core_009 loan amortisation).

#### Faults
- **F1 [HIGH]** core, bv_core_009, index.html:358 (keyed line :364, explanation :368)
  - Question: "Tom wants to borrow £2,000 for 2 years." The bank loan is £2,000 at 8% APR over 2 years; the credit union is £95/month for 24 months. Options: "The bank loan is cheaper — 8% APR sounds low" / "The credit union is cheaper — total repayment £2,280 vs approximately £2,332 for the bank loan" / "They cost the same — both around £2,300" / "The bank loan is better because it has a fixed rate".
  - Keyed answer: the credit union is cheaper (£2,280 vs about £2,332).   Correct answer: the bank loan is cheaper, at about £2,165 in total.
  - Evidence: £2,332 is 2000 × 1.08² = £2,332.80, which is the debt with **no repayments at all for 2 years** (and £2,332.80 rounds to £2,333 anyway). A 2-year loan at 8% APR repaid monthly costs £90.20/month, £2,164.80 in total (`recompute.py`). The credit union's £95 × 24 on £2,000 works out at an APR of about 13.7%. Under the usual monthly-repayment reading the key is reversed. The scenario never states how the bank loan is repaid, so the question is at best unanswerable as worded. The explanation teaches the wrong model.
  - Share affected: 1 of 50 core questions.
- **F2 [HIGH]** core, bv_core_031, index.html:626 (keyed line :633)
  - Question: the advertised deal is £18/month + £10/month line rental + £60 installation over 18 months; the rival is £32/month all-in over 12 months. Keyed conclusion: "The advertised deal costs £564 over 18 months; the rival costs £384 over 12 months. Per month, the rival is cheaper at £32 vs £31.33 — but the advertised deal locks you in for 6 extra months".
  - Keyed answer states "the rival is cheaper at £32 vs £31.33".   Correct: £31.33 < £32, so the **advertised** deal is cheaper per month. The game's own explanation (:636) says "Per month the advertised deal is marginally cheaper".
  - Evidence: (28 × 18 + 60)/18 = 564/18 = £31.33 < £32. The keyed text is false as written, and no other option is correct: one claims £18 beats £32, and another compares totals over different terms.
  - Share affected: 1 of 50 core.
- **F3 [HIGH]** core, bv_core_036, index.html:686 (keyed line :691, explanation :696)
  - Question: 20 return trips; Anytime £48; Advance £22, with 3 missed trains replaced at £48. Keyed: "Advance tickets are better value — total £518 vs £960 for Anytime, even with 3 missed trains".
  - Keyed answer: £518.   Correct: £584 (20 × £22 + 3 × £48). The explanation's own sum, £440 + £66 + £144, is £650, not £518.
  - Evidence: 440 + 66 + 144 = 650, and the key printed 518. The verdict (Advance is cheaper) holds, but the keyed figure and the "saves £442" in the explanation are wrong arithmetic.
  - Share affected: 1 of 50 core.
- **F4 [HIGH]** core, bv_core_037, index.html:698 (keyed line :704)
  - Question: standard flyers cost £180 and bring £800 of sales; premium flyers cost £260 and bring £1,120. Keyed: "Premium flyers give better return on investment — net profit £860 vs £620 for standard".
  - Keyed answer: premium has the better ROI.   Correct: standard has the better ROI, 344% against 331%. Premium has the higher net **profit**.
  - Evidence: 620/180 = 344.4% and 860/260 = 330.8%. The game's own explanation says "Although premium has slightly lower ROI…". The keyed claim is false as worded. A student who computes ROI finds no true option.
  - Share affected: 1 of 50 core.
- **F5 [HIGH]** core, bv_core_049, index.html:842 (keyed line :847, explanation :852)
  - Question: an employee costs £15/h × 20 h/week plus £180/month employer costs; outsourcing costs £40/h. "At what weekly outsourcing hours does hiring become cheaper?" Keyed: "Hiring becomes cheaper above approximately 8.8 hours per week".
  - Keyed answer: 8.8 hours.   Correct answer: about 8.5 hours. The explanation itself computes "h = 8.54 hours", then says "Above about 8.8 hours".
  - Evidence: (300 + 180 × 12/52)/40 = 8.538. With the game's ÷4.33 it is 8.539.
  - Share affected: 1 of 50 core.
- **F6 [MEDIUM, judgement call]** gcse, bv_gcse_020, index.html:1100 (distractor :1105)
  - Question: a £15 reusable bottle against £1 bottled water. The distractor "The reusable bottle saves money after 15 bottles" is marked wrong. The keyed answer is "…saves money after more than 15 bottles — from bottle 16 onwards".
  - Evidence: "after 15 bottles" naturally means once 15 have been bought, which is the same as "from bottle 16". The game itself keys exactly this "after N = break-even N" wording as correct in bv_core_024 (:545, "After 34 coffees the machine becomes better value — break-even at 34 cups", where 85/2.50 = 34 exactly). A student can be marked wrong for the game's own accepted phrasing. This is in the resit card's level.
  - Share affected: 1 of 20 gcse.
- **F7 [MEDIUM, judgement call]** core, bv_core_007, index.html:333 (distractor :341)
  - The distractor "Lease B is better if the business makes fewer than 1,000 copies" is marked wrong, but it is **true**. Lease B costs £85 + 0.02n per month, which is below £120 whenever n < 1,750. It is irrelevant to this business (2,000 copies), but as a statement it is correct.
- **F8 [MEDIUM, judgement call]** core, bv_core_019, index.html:479 (distractor :484)
  - The distractor "Contract B pays more in total — £18,000 vs £11,520" is marked wrong. It is true if Contract A also runs 12 weeks (320 × 3 × 12 = 11,520). The scenario gives no length for Contract A and never says whether "pays better" means the day rate or the total.
- **F9 [MEDIUM]** core, bv_core_033, index.html:650 (explanation :660). The keyed 4.25 kWh/day is right (28d + 25 = 24d + 42 in pence). The explanation mixes pounds and pence, writing "0.28d + 25 = 0.24d + 42 → 0.04d = 17 → d = 4.25". In that form 0.04d = 17 gives d = 425.
- **F10 [LOW]** gcse, bv_gcse_019, index.html:1088 (keyed :1093). "The pass is worth it if you eat 12 or more lunches". At 12, the pass and pay-per-lunch cost exactly the same (£30), so the pass only saves from 13. This is inconsistent with gcse_020's strict "more than 15". No option is affected, because 13 is not offered.
- **F11 [LOW]** core, bv_core_018 (:477) and bv_core_020 (:501). The explanations show money to 3 d.p. ("£1.503/litre", "£2.392/litre"). The conclusions round correctly (£1.50 vs £1.52, £2.39 vs £2.52), and the gaps clear SR-5.
- **F12 [LOW, judgement]** core, bv_core_047 (:818). The keyed answer, "Cleaner B is better value overall — £135/year vs £130/year", rests on a qualitative preference ("values the longer-lasting clean"), not on the numbers: B costs more. bv_core_044 (:782) and bv_core_048 (:830) are similar opinion-keyed items. Their keyed text is defensible, but a student cannot reach the answer by calculation.

#### Clean
- Exactly one correct conclusion out of 4 per question: 70 of 70.
- GCSE (the resit level): all 20 keyed totals, unit rates and break-evens recompute exactly (gcse_001-020; see `recompute.py`). The only issues are F6 and F10.
- Core: 45 of 50 keyed conclusions are numerically right. F1-F5 are the exceptions.
- SR-5, no ties: in every comparison the two figures differ by at least 1p or 0.01 as shown. The closest are bv_core_018 (£1.50 vs £1.52), bv_core_023 (£30 vs £29.17), bv_gcse_007 (£22.49 vs £23.00), bv_gcse_009 (£45 vs £45.99) and bv_gcse_016 (£9 vs £8.89). Every "they cost the same" distractor is false.
- Money format: every pence amount in the conclusions is shown to 2 d.p.; the only 3 d.p. values are in explanations (F11).
- Worked example (method overlay, :1389-1407): £144/156 = £0.92, 156 × £4.50 = £702, saving £558. All correct.
- Marking cannot mis-mark a click: it reads the boolean stored on the card itself.

#### Not checked / limits
- Opinion-keyed items (bv_core_044, 047, 048 and parts of 050) cannot be verified by calculation. I flagged them as judgement only.
- The core_009 verdict depends on the repayment model, which the scenario leaves unstated. I give both readings above.

**Reviewing session re-check:** F1–F5 re-checked against the source lines: 009 (:364, 2000 × 1.08² ignores repayments; amortised monthly at 8% APR the total is about £2,165), 031 (:633, "the rival is cheaper at £32 vs £31.33" is false), 036 (:691, 20 × £22 + 3 × £48 = £584, not £518), 037 (:704, ROI 620/180 = 344% > 860/260 = 331%), 049 (:847, 341.57/40 = 8.54, not 8.8).


### Percentage Flip (`percentage-flip`)
Resit card level: year6 ("Starter", link `/games/percentage-flip/?level=year6`). Levels audited: year6 → `QUESTIONS_YEAR6` (20 questions, index.html:191-212); every other URL, including `?level=ks3` and `?level=gcse` → `QUESTIONS_DEFAULT` (12 questions, :173-189), with level reported as `'all'` (:215-217). The extractor's "32 each" is the two arrays added together. In fact year6 draws from 20, and ks3/gcse/bare draw from 12, with no separate ks3 or gcse bank. Bank type: static. 10 questions are drawn per session (:225).
Marking: typed, `<input type="number">` (:148). `parseFloat(value)` with `Math.abs(user − key) < 0.01` (:262, :287), which is a game-local tolerance, not MaffsAnswer. It is answered either by CHECK (:280) or by tapping the card, which reveals the answer and marks whatever is typed (:254). There are no multiple-choice options and no drawn grids or bars: the "card" is only text, the answer and a working line.
Items checked: 32 of 32 keys recomputed exactly (p/100 × x with Fraction; `scratchpad/work/percentage-flip/check_keys.py`). All 32 working lines read by hand. Duplicates: none within either bank. The SKIP race was reproduced in Chromium with `scratchpad/work/percentage-flip/skip_race.py`.

#### Faults
- **F1 [MEDIUM]** all levels, index.html:299-303 (`checkAnswer` timers and `skipQ`)
  - What happens: after CHECK, the game schedules an auto-flip at 1.5 s and an advance at 3 s (:299-300). SKIP stays live during that feedback window, and `skipQ()` (:303) does not check `answered`. If the student presses SKIP while the feedback shows, the next question loads at once. 1.5 s later the old auto-flip fires on the **new** question's card: it reveals the answer and marks it wrong with nothing typed, logging `question_answered correct:false`. The two pending advances then skip one more question unseen.
  - Evidence (skip_race.py, year6): Q1 "What is 50% of 80?" was answered 40 → correct. Pressing SKIP 0.3 s later showed "What is 25% of 120?", and 1.4 s after that its feedback read "Answer was 30". Events: [{q1 correct:true}, {q2 correct:false}]. qNum went 0 → 3 in 4.2 s, so Q2 was marked wrong unanswered and Q3 was never shown. The same double advance (without the auto-mark) follows SKIP after a card-tap answer (:276).
  - Share affected: any question where the student presses SKIP during feedback. This needs a student action; it is not tied to particular questions.
- **F2 [LOW]** the ks3 and gcse levels do not exist as banks. `?level=ks3` (the portal card, index.html:1374 of the portal) and `?level=gcse` both serve the 12-question `QUESTIONS_DEFAULT` with level `'all'`, so a 10-question session sees 10 of the same 12 questions every time. The roster lists Year 6, KS3, GCSE. This is already in the check ledger as B4 (below the 40 minimum), but the ledger entry says 32 per level, which overstates ks3/gcse.
- **F3 [LOW]** a wrong answer auto-advances after a fixed 2 s or 3 s (:276, :300), with no Next control (canon §7.6). The working is visible only on the flipped card during that time.
- **F4 [LOW]** the start screen says "Questions get harder as you go" (:124), but the questions are shuffled (`sort(() => Math.random() − 0.5)`, :221, a biased but bounded shuffle), so the order is random.

#### Clean
- Keys: 32 of 32 correct (default 12: 50%·80=40, 25%·200=50, 10%·350=35, 100%·47=47, 20%·150=30, 75%·80=60, 15%·200=30, 40%·250=100, 35%·120=42, 12.5%·160=20, 60%·85=51, 5%·340=17; year6 20, all of them 10%, 25%, 50% or 75% of a multiple of 4 or 10, all whole numbers).
- Working lines: 32 of 32 arithmetically correct. For example, "10% = 8.5, × 6 = 51" and "10% = 12, 30% = 36, 5% = 6 → 42".
- Typed marking: every key is a whole number. A correct entry (e.g. "40" or "40.0") is accepted, and the 0.01 tolerance admits no named wrong answer. A `type=number` input cannot take "%" or "£", and none is needed.
- Value-equal forms and option distinctness: not applicable (typed answers, no options).
- Drawn representations: none exist (no grids or bars), so there is nothing that could disagree with the key.

#### Not checked / limits
- The other timing paths were not exhaustively fuzzed, for example rapid double taps on the card. I read the logic only, and found no mis-marking apart from F1.


### New Shapes (`new-shapes`)
Resit card level: year6 (single level, shown as "Starter"). Levels audited: year6 only (the game has one hard-coded level, `LEVEL = 'year6'`, index.html:421): 50 questions = 15 parallelogram + 20 trapezium + 15 prism. Bank type: static. (The extract's "100 items" is `ALL_QUESTIONS` (50) counted again alongside its three section arrays (50); there are 50 distinct questions.)
Marking: typed on an on-screen keypad (digits and `.` only, max 8 chars); `parseFloat(inputValue) === q.answer` (index.html:832-833). Not MaffsAnswer. All 50 keys are positive whole numbers, so "24", "24.", "24.0", "024" are all accepted; no sign key is needed.
Items checked: all 50 questions (index.html:355-412). Each key recomputed in exact integer arithmetic (b*h; (a+b)*h/2 with the parity checked; A*l), every working-step line recomputed and matched, trapezium a < b checked, duplicate ids/questions checked: `scratchpad/work/new-shapes/check.js`. One question of each shape rendered under Playwright at 900x900 and 375x667 (`scratchpad/work/new-shapes/render.py`, screenshots `ns_p12_*`, `ns_t16_*`, `ns_v13_*.png`), and the drawing code read (renderParallelogram 468-504, renderTrapezium 506-583, renderPrism 585-684).

#### Faults
- **F1 [MEDIUM]** year6 / prism, all 15 prism questions (index.html:398-412; drawing index.html:653-681)
  - Question (e.g. ns_v13): "VOLUME OF A PRISM", diagram, "V = A × l", "A = 30, l = 2", "What is V?"
  - Keyed answer: 60. Correct answer: 60 (key is right).
  - Evidence (picture vs words, SR-6): the prism's length l is the distance between the two cross-section faces, i.e. along the receding edges (drawn from (20,130) to (60,100) etc.). The `l` dimension arrow is instead drawn horizontally under the drawing from x=22 to x=148 (index.html:655-658), spanning the front face's width (x 20-110) plus the depth offset. On screen it reads as the width of the front (cross-section) face, which is a dimension of A, not of the prism's length. The cross-section is also always drawn as a square, so the solid is a cube whatever A and l are (A = 30, l = 2 is drawn as a cube). The key is unaffected; the picture labels the wrong dimension for the formula it teaches.
  - Share affected: 15 of 50 questions (30%), every prism question.

- **F2 [LOW]** year6 / parallelogram and trapezium, all 35 (drawings index.html:468-583)
  - The parallelogram and trapezium are fixed drawings whatever the numbers (parallelogram 180x100 skewed box; trapezium top:bottom always 1:2), with no "not drawn to scale" note. e.g. ns_p12 (b = 3, h = 10) draws a wide, short parallelogram whose labelled height is drawn at about a third of its labelled base; ns_t16 (a = 1, b = 7) draws a top half the bottom. The labels are right and are on the right parts (b on the base, h on a perpendicular dashed line between the parallel sides, a on the shorter parallel side). Judgement call: diagrams are not claimed to scale, but a Starter-level student may read the picture.

- **F3 [LOW]** year6 / trapezium, cosmetic (index.html:574-580)
  - The `h = …` label (right: 20px, opaque background) is drawn over the slanted right-hand side of the trapezium, hiding part of that edge (visible in `ns_t16_900.png`). The label is still next to the dashed height line, so it is not misleading.

- **F4 [LOW]** year6, marking edge (index.html:828-833)
  - Entering only "." and pressing Enter submits `parseFloat('.')` = NaN and is marked wrong (counts against the score, shows the answer). An unreadable entry should not be marked (canon 7.1.3 treats unreadable input as unmarked). Minor, needs a deliberate mis-key.

- **F5 [LOW]** wording, reveal screen (index.html:326)
  - "You now know five area formulae and one volume formula." The game teaches two area formulae (parallelogram, trapezium) and one volume formula; with rectangle and triangle (start screen, index.html:258) that is four area formulae, five only if the circle is assumed. Judgement call.

#### Clean
- Keys: 50/50 correct (15 parallelogram b×h, 20 trapezium ½(a+b)h all integer, 15 prism A×l).
- Working steps: 50/50 lines arithmetically correct and end on the key; "Not quite — the answer is N" states the key.
- Diagram labels: on every question the drawn labels are built from the same `variables` the key uses (loadQuestion 761-775), so label values always equal the question's numbers; the vars line repeats them.
- Diagram shape: parallelogram is a true parallelogram (skewX), height dashed line vertical (perpendicular to the base) and inside the shape; trapezium's labelled a and b are the two parallel sides (top shorter, a < b in all 20), the height is a vertical dashed line between them, not the slant edge.
- Typed marking accepts the key in every natural form available on the keypad; no tolerance, so no named wrong answer is accepted.
- No duplicate ids; no two questions identical.

#### Not checked / limits
- No units are given anywhere (questions, keys, labels); not a fault for a pure formula drill, noted only.
- Personal best is stored as a raw count across 10/20/30-question sessions (index.html:943) and shown as "/sessionLength"; not a maths-key issue, not pursued.
- Phone layout at 320x568 not measured (CI tier 1 covers horizontal overflow).


### Angle Ace (`angle-ace`)
Resit card level: year6 ("Starter", card opens `?level=year6`, picker). Levels audited: year6 (40: 10 straight line, 10 at a point, 10 vertically opposite, 10 parallel-line recognition) and gcse (35). The extract's "ks3 75" is not a real level: `QUESTIONS_BY_LEVEL` has only `year6` and `gcse` (index.html:200, 483); `?level=ks3` falls back to gcse (index.html:724-729) and the picker shows only Starter and GCSE. Bank type: static, every diagram hand-drawn on a canvas per question.
Marking: phase 1 angle, `parseInt(btn.dataset.val)===currentQ.answer` (index.html:795); recognition, `btn.dataset.val===currentQ.answer` (780); phase 2 reason, `btn.dataset.val===currentQ.reason` (818), options = the key plus 3 reasons drawn at random from the other 8 (806-809). `multiReason` (628, 644) is never read.
Items checked: all 75 questions. Keys recomputed from the numbers printed on each diagram and the relationship (`scratchpad/work/angle-ace/analyse.js`); options checked for count, distinctness and key-once. Every diagram's canvas calls recorded in node (`harness.js` -> `measured.json`/`measured.txt`): for each printed label and each arc, the vertex, the drawn rays, the region the label actually sits in and that region's true drawn size. All 75 diagrams rendered under Playwright and inspected (`render.py`, contact sheets `sheet_year6_*.png`, `sheet_gcse_*.png`).

Summary: every numeric key equals what the printed numbers and the keyed relationship give (75/75), and all option sets are sound. The fault is the pictures: 20 of 40 year6 and 22 of 35 gcse diagrams have at least one picture fault, several of which make the drawn figure give a different answer or name a different relationship from the key.

#### Faults
- **F1 [HIGH]** gcse, index.html:563 and index.html:665 (2 questions)
  - Question: "Find angle x" (two crossing lines). Options 65, 115, 75, 105 (L563); 43, 137, 47, 133 (L665).
  - Keyed: 65 (reason: angles on a straight line), 43. Picture: the "115°" (resp. "137°") label and the x arc are drawn in the same region, the top angle between the two lines (rays at 17.65° and 153.43° from the vertex; label direction 40°, x arc 55°-155°; for L665 rays 16.7°/163.3°, label 32.5°, arc 55°-170°). Read from the picture, x is the 115° (137°) angle, which is an offered option; nothing drawn shows x adjacent to it on a straight line, although the step text (and L568's misconception note) says so. Words and key disagree with the picture.
  - Share: 2 of 35 gcse.
- **F2 [HIGH]** gcse, index.html:630
  - Question: "Find angle x", options 73, 107, 83, 97; keyed 73, reason "Alternate angles are equal"; steps "73° and x are alternate angles".
  - Evidence: x's arc is at (320,240) between the lower parallel line and a third line drawn from (320,240) to (240,100), not the transversal (the transversal runs (200,40)-(380,300)). The 73° label is at the transversal's crossing of the upper line, above the line. The third line is not parallel to the transversal (drawn angles 60.3° for x against 55.3° for the 73° region), so no angle fact links x to 73°: the question is unanswerable from the figure and the stated alternate pair is not drawn.
- **F3 [HIGH]** gcse, index.html:638
  - Question: "Find angle x in the triangle", options 105, 75, 115, 85; keyed 105 (45° + 30° + x = 180°; reasons alternate then triangle).
  - Evidence: the "45°" is printed at (260,100) above the upper parallel line where the only rays are the line itself (0°, 180°) and the third line going down (299.4°): it labels a straight angle, not an angle of any triangle. The x arc is centred at (310,180), 34.5px from the nearest line intersection (323,212), so x marks no vertex. No triangle with angles 45°, 30°, x is drawn. Unanswerable from the figure.
- **F4 [HIGH]** year6 (resit level), index.html:293
  - Question: "One angle is 270°. Find angle x." Options 90, 180, 270, 45; keyed 90.
  - Evidence: rays at 0° and 270°. The "270°" is printed twice (drawAngleValue span 270-360, plus a second fillText at (360,250)), both inside the lower-right quarter, which is drawn as 90°. The x arc is drawn 0°-270°, the reflex angle. The picture labels the right angle 270° and draws x as the reflex angle, so a student reading the picture picks 270 (offered). Key and picture contradict.
- **F5 [HIGH]** "co-interior" pairs that are not co-interior: gcse index.html:517, 522, 527, 655, 688; year6 recognition index.html:423, 444, 465 (8 questions)
  - Questions: gcse "Find angle x" keyed 120/105/132/70/55, reason "Co-interior angles sum to 180°"; year6 "These angles form a C-shape / U-shape. What type of angle pair is this?" keyed "Co-interior angles (sum to 180°)".
  - Evidence: in every one the given angle's label is printed above the upper parallel line, right of the transversal (an exterior angle, drawn 127.6°), and the other angle (x, or the 120°/110°/100° arc) is between the lines, left of the transversal (drawn 52.4°). The two angles are on opposite sides of the transversal and one is outside the parallel lines: not co-interior, not a C or U shape (getting from one to the other needs vertically opposite + co-interior, or corresponding + straight line). The numbers are consistent with the drawing (the drawn pair does sum to 180°), but the keyed reason is not the relationship drawn, and in 6 of the 8 the acute/obtuse sizes are swapped (e.g. L517: "60°" on a 127.6° angle, x = 120 drawn 52.4°). Year6's caption text "C-shape"/"U-shape" names a shape the angles do not form.
  - Share: 5 of 35 gcse, 3 of 40 year6.
- **F6 [HIGH]** year6 recognition, index.html:437
  - Question: "These angles form a reverse Z-shape. What type of angle pair is this?" keyed "Alternate angles (equal)"; both angles labelled 48°.
  - Evidence: transversal (400,40)-(200,300). The upper "48°" is above the upper line, left of the transversal (drawn 127.6°); the lower 48° arc is between the lines, right of the transversal (drawn 52.4°). Opposite sides, one exterior and one interior: not alternate, not corresponding, not co-interior; the drawn pair sums to 180° yet both are labelled 48°.
- **F7 [MEDIUM]** "alternate" pairs drawn as alternate EXTERIOR angles: gcse index.html:485, 495, 647, 683; year6 recognition index.html:416, 458 (6 questions)
  - Keyed "Alternate angles are equal" / "Z-shape". Evidence: the given label is above the upper line right of the transversal and x (or the second angle) is below the lower line left of it: both outside the parallel lines. They are equal (key values hold), but they are not the Z pair GCSE means by alternate angles, and the drawn angles are obtuse (124.7°-137.1°) while labelled 40°-68°.
- **F8 [MEDIUM]** label printed on the transversal: gcse index.html:490, 506
  - L490 "Find angle x", options 70, 110, 180, 60, keyed 70 (alternate): the "70°" sits across the transversal at the upper line (label direction 133.8°, boundary 124.7°: just inside the acute upper-left angle). Read as the upper-left angle, x (below the lower line, left) is supplementary to it, giving 110 (offered). L506 keyed 65 (corresponding): the "65°" sits exactly on the transversal (direction 127.6° = the ray); read as the upper-right angle, x is supplementary, giving 115 (offered). Ambiguous picture, one reading gives an offered distractor.
- **F9 [MEDIUM]** label value contradicts the drawn size (acute labelled on an obtuse angle, or the reverse); key unaffected. year6: index.html:216 ("120°" on a 47.3° angle, x = 60 drawn 132.7°), 245 ("115°" on 49.8°, x = 65 drawn 130.2°), 338/345/359/380/394 (vertically opposite: 50°, 73°, 45°, 67°, 28° printed on angles drawn 136°-147°), 409/430/451/472 (corresponding: 50°, 65°, 45°, 55° on angles drawn 124.7°-127.6°). gcse: index.html:501, 511, 651 (corresponding 50°, 35°, 42° on 121.6°-127.6°), 556, 671 (vertically opposite 48°, 63° on 136.4°, 126.9°), 590 ("90°" printed in the 35.5° corner of the triangle, with no right-angle mark), 625 ("62°" on 132.7°). No diagram says "not drawn accurately"; a student checking "is x acute or obtuse?" is misled.
- **F10 [MEDIUM]** year6, index.html:259: "Two angles on a straight line: one is 60°. Find x." The drawing has a second ray (to (220,50)), so three angles meet on the line and the x arc (60°-180°) spans two of them. Key 120 holds if x is the whole arc; words and picture disagree.
- **F11 [MEDIUM]** year6, index.html:312: "One angle is 200°. Find angle x." A second "200°" is printed at (250,230), inside x's region (200°-360°), right beside the x label.
- **F12 [MEDIUM]** gcse, index.html:625: "Find angle x (two steps needed)". The y arc (0°-62°) and x arc (62°-180°) meet at 62°, where no line is drawn; the transversal is at 132.7°, and the "x" letter falls on the same side of it as y. The figure does not show x and y as two angles separated by the transversal.
- **F13 [MEDIUM]** phase 2 marks a valid reason wrong (handlePhase2, index.html:818; reasons drawn at random, 806-809)
  - year6 index.html:281 (x = 180, rays at 0°, 100°, 180°): x is the angle on the straight line formed by the 0° and 180° rays, so "Angles on a straight line sum to 180°" is also a valid reason; it is offered with probability 3/8 and marked wrong. year6 index.html:331 (four right angles on two perpendicular lines, x = 90): "Vertically opposite angles are equal" and "Angles on a straight line" are both valid; at least one is offered with probability 36/56 = 64%, marked wrong. gcse index.html:625 and 638 carry `multiReason` (corresponding + straight line; alternate + triangle) but only the single keyed reason is accepted, so the other needed reason, when offered (3/8), is marked wrong. Judgement call for the multi-step pair.
- **F14 [LOW]** gcse has 35 questions (comment at index.html:481 says 55; below the 40-50 minimum). Roster lists KS3 but there is no ks3 bank (falls back to gcse). Year6 recognition captions ("F-shape", "Z-shape"...) print the answer's shape on the diagram. Isosceles tick on the right side (index.html:603) is drawn almost parallel to that side, so it barely shows.

#### Clean
- Numeric keys: 75/75 equal the value from the printed numbers and the keyed relationship (64 numeric, 10 recognition, 2 multi-step checked by hand: 180 - 62 = 118; 180 - 45 - 30 = 105).
- Options: 65 angle sets have 4 distinct values with the key exactly once; 10 recognition sets have the 3 pair names with the key exactly once; every keyed reason string is one of the 9 REASONS.
- Marking: integer `dataset.val` compare and exact string compare, with keys and option strings from the same source; no correct click can be marked wrong by formatting.
- Diagrams correct and consistent with key: year6 at-a-point 10 (except L293, L312), straight line 6 of 10; gcse triangles L584, L596, L677, L693, exterior L608, L616, point L571, L577, straight L533, L540, L548, L659, L701.

#### Not checked / limits
- Analytic region measurement assumes the reader takes the region the label text sits in; for labels within a few degrees of a line (F8) the reading is genuinely ambiguous and is reported as such.
- Fonts were the fallback font (Google Fonts blocked); label positions do not depend on the font.

**Reviewing session re-check:** F1 re-checked by rendering (gcse L563: the x arc and the 115° label sit in the same angle) and in the recorded drawing calls; F4 (L293) re-checked in the recorded calls. F2, F3, F5 and F6 rest on the same measurement method and were spot-checked on the rendered sheets.


### Shape Shifter (`shape-shifter`)
Resit card level: year6 (single level; `level: 'year6'` hard-coded, index.html:473). Modes audited: Translation (15 items, 10 per session), Reflection (15, 10 per session), Rotation (15, built at load by `buildRotationQuestions`, index.html:335-376; 10 per session), Random Mix (3 of each + 1 extra, index.html:442-465). Bank type: static lists for translation/reflection; rotation is generated deterministically once at load (no randomness), so its full space is the 15 items.
Marking: Translation/Reflection: the student taps lattice points (`pixelToGrid` rounds to the nearest integer point, index.html:241-247); after as many taps as vertices, an order-independent exact match against `expectedVertices` (index.html:812-828). Rotation: four shapes drawn on the grid, labelled A-D at their centroids; a tap selects the FIRST option (in A-D order) whose polygon contains the snapped point or has a vertex within 1 unit of it (`pointInShape`, index.html:779-798; loop 740-745); marked by `rotationOptions[i].correct` (859).
Items checked: all 45 items. Each image recomputed independently (translation from the words of `desc`, reflection from the words, rotation with the clockwise map (x,y)->(y,-x) and anticlockwise (x,y)->(-y,x) about (0,0) on the y-up grid) and compared with the game's key; desc vs dx/dy/axis; every image inside the -5..5 grid; option sets compared as vertex SETS; click selection simulated for every lattice point and every one of the 24 option orders (`scratchpad/work/shape-shifter/check.js`). Browser play under Playwright: 60 translation/reflection questions answered by tapping the true image (`tapplay.py`, 60/60 marked Correct); 10 rotation questions answered by tapping the true image (`play.py`, every tap that selected it marked "Not quite"); 40 rotation taps on option labels (`labelclick.py`). Screenshot `rot_after.png`.

#### Faults
- **F1 [CRITICAL]** Rotation mode (and the rotation third of Random Mix): every rotation key is the wrong direction. index.html:290-296 (`rotatePoint`), 361 (labels), 337-349 (bases).
  - `rotatePoint` applies [cos -sin; sin cos], which on this y-up grid is an ANTICLOCKWISE turn for a positive angle; the question text labels angle 90 as "90° clockwise" and -90 as "90° anticlockwise" (index.html:361). So the keyed shape is always the image for the opposite direction, and the true image is the "wrong direction" distractor (`generateWrongRotations`, index.html:311).
  - Example (first base, index.html:337): "Rotate 90° clockwise about (0,0)", object (1,1),(3,1),(2,3). Keyed: (-1,1),(-1,3),(-3,2) (that is 90° anticlockwise). Correct: (1,-1),(1,-3),(3,-2). Check: 90° clockwise about the origin sends (1,1) to (1,-1); `rotatePoint(1,1,0,0,90)` returns (-1,1).
  - Share: 15 of 15 rotation items (8 "clockwise", 7 "anticlockwise"; the 15-item cap is reached before any 180° item is built, so no 180° question exists). In play, every tap on the true image was marked "Not quite — correct answer was X" and the opposite-direction image marked "Correct!". 100% of Rotation mode; about a third of Random Mix (3 or 4 of 10).
- **F2 [CRITICAL]** Rotation mode: a tap on a shape often selects a different shape. index.html:740-745, 779-798.
  - A tap snaps to the nearest lattice point and selects the first option (A, then B...) whose polygon contains it OR has any vertex within 1 grid unit of it. The four options and the object overlap (18-39 lattice points per question hit two or more options), so earlier-lettered options capture taps meant for later ones.
  - Evidence: simulated tap on each option's own label (its centroid, snapped as the game snaps), over all 15 items x 4 options x 24 orders: 730 of 1440 (50.7%) select a differently shaped option. In the browser, 21 of 40 taps on a label selected another option, e.g. tapping label C gave "Not quite — correct answer was C" (the student pressed the right letter and was marked wrong). Independent of F1: this would remain after the direction is fixed.
- **F3 [HIGH]** Rotation, duplicate options: index.html:313 (reflection distractor), 338, 343
  - "Rotate 90° clockwise/anticlockwise about (0,0)" for the squares (1,1),(3,1),(3,3),(1,3) and (0,0),(2,0),(2,2),(0,2): the "reflection instead" distractor (reflect in the x-axis) is the same square as the 90° clockwise image. Clockwise items (rot #2, #11): two of the four options are the identical shape (both the true answer, both marked wrong). Anticlockwise items (rot #3, #12): the keyed option and the reflection distractor are the identical shape drawn on top of each other; which one a tap selects depends on letter order, so in 12 of 24 orders the keyed option cannot be selected at all. `shapesEqual` (index.html:321-327) compares vertex lists in order, so it never sees these as equal.
  - Share: 4 of 15 rotation items.
- **F4 [MEDIUM]** Rotation, distractor identical to the object: for the square (0,0),(2,0),(2,2),(0,2) (index.html:343), the "wrong centre" distractor (rotation about (1,1)) is the object itself, drawn exactly over the teal original. 2 of 15 rotation items.
- **F5 [LOW]** Bank sizes 15/15/15 (below the 40-50 minimum); rotation never asks 180° although the code lists it; all rotations are about (0,0). Reflection items with a vertex on the mirror line (index.html:279, 283, 284) require tapping that vertex in place; correct and accepted, noted only.

#### Clean
- Translation: 15/15 keys match the words (direction and size), all images inside the grid, no duplicate items; 30 browser questions answered by tapping the true image, 30/30 Correct.
- Reflection: 15/15 keys match the words (x-axis: (x,y)->(x,-y); y-axis: (x,y)->(-x,y)), mirror line drawn on the named axis (index.html:586-597), images inside the grid, no duplicates; 30 browser questions, 30/30 Correct.
- Vertex marking is exact and order-independent; a wrong vertex or a missing vertex is marked wrong; no tolerance.

#### Not checked / limits
- Touch input (touchstart) not exercised; it uses the same handler as click.
- Rotation centre is drawn as an orange dot at (0,0) as stated; grid drawing matches gridToPixel (checked in screenshot).

**Reviewing session re-check:** F1 re-checked: `rotatePoint` (:290-296) is [cos −sin; sin cos], anticlockwise for a positive angle on this y-up grid (`gy = GRID_MAX − …`, :245); angle 90 is labelled "90° clockwise" (:361). F2 re-checked in the code (:739-745, :779-797: the first option containing the snapped point, or with a vertex within 1 unit); the 21 of 40 figure is the agent's Chromium run.


### Probability Pioneer (`probability-pioneer`)
Resit card level: year6 (single level, `const LEVEL = 'year6'`, index.html:358). Levels audited: year6, 45 items (Stage 1 scale 10, Stage 2 MCQ 20, Stage 3 true/false 15). Bank type: static. Every session plays all 45 in fixed order (only Stage 2 option order is shuffled), so every fault below is met by every student.
Marking: Stage 1 `confirmScale()` compares the clicked float literal to `q.answer` or `q.accept` (index.html:474); Stage 2 `pickMCQ()` compares the option string to `q.answer` with `===` (index.html:561); Stage 3 `answerTF()` compares booleans (index.html:635). No string/format mismatch possible: every Stage 2 key string appears verbatim in its own options (checked).
Items checked: all 45. Stage 2 keys recomputed exactly with Fraction from the question wording, options checked for key-once and value-equal pairs (scratchpad/work/probability-pioneer/check.py, output out.txt). Stage 1 and Stage 3 read and judged by hand.

#### Faults
- **F1 [HIGH]** **RESOLVED** (key PR #36; reason line PR #45) year6 / Stage 2 Q20, index.html:333
  - Question: "P(letter in MATHS also in GAMES)"   Options: 2/5, 3/5, 1/5, 4/5
  - Keyed answer: 2/5   Correct answer: 3/5
  - Evidence: MATHS = {M, A, T, H, S}; GAMES = {G, A, M, E, S}; common letters M, A, S = 3 of 5. 3/5 is offered and marked wrong; feedback says "The correct answer is 2/5".
  - Share affected: 1 of 20 Stage 2 questions; every session (fixed order).
- **F2 [HIGH, wording-dependent]** **RESOLVED PR #45** (rekeyed False, decision 4) year6 / Stage 3 Q7, index.html:343
  - Statement: "If two outcomes are equally likely, each has probability 0.5"   Keyed: True
  - As worded this is false in general: rolling a 1 and rolling a 2 on a die are two equally likely outcomes, each 1/6. It is only true if the experiment has exactly two outcomes, a condition the explanation adds ("If there are exactly two equally likely outcomes...") but the statement does not. A student who answers False for the right reason is marked wrong, and the True key reinforces the "it either happens or it doesn't, so 50-50" equiprobability misconception that probability teaching targets. Fix is a wording change ("If an experiment has exactly two outcomes and they are equally likely...").
  - Share affected: 1 of 15 Stage 3 statements.
- **F3 [MEDIUM]** **RESOLVED PR #45** (Unlikely only) year6 / Stage 1 Q8, index.html:308
  - Event: "You win the lottery with one ticket"   Keyed: Impossible (0), Unlikely (0.25) also accepted.
  - Marking is safe (Unlikely is accepted), but the feedback states a false fact: on any answer the text reads '"You win the lottery with one ticket" is Impossible.' (index.html:500/505), and the Impossible label is the one highlighted as correct (index.html:484). Winning with one ticket is possible (about 1 in 45 million for UK Lotto), so the right label is Unlikely; Impossible should not be the headline key, and the scale has no "very unlikely" point so 0.25 Unlikely is the best fit. Wrong explanation.
- **F4 [MEDIUM, judgement call]** **RESOLVED PR #45** (Likely only) year6 / Stage 1 Q3, index.html:303
  - Event: "It will rain somewhere in Britain this week"   Keyed: Certain (1) only.
  - Not certain in the probability sense (P = 1); it is very likely. A student who picks Likely (0.75), arguably the more defensible answer, is marked wrong. Either accept Likely or reword (e.g. something genuinely certain).
- **F5 [LOW]** **RESOLVED PR #45** (4/6 → 1/2; "on a dice") year6 / Stage 2 Q9, index.html:322: "P(rolling greater than 4)", options 1/3, 2/3, 4/6, 1/6. Key 1/3 correct (5, 6 of 6), but two distractors, 2/3 and 4/6, are equal in value, so the question has only three distinct values. Also the stem does not say "on a die" (context implies it).
- **F6 [LOW]** **RESOLVED PR #45** (2/4 → 1/3) year6 / Stage 2 Q13, index.html:326: "P(heads twice in a row)", options 1/4, 1/2, 1/8, 2/4. Key 1/4 correct, but distractors 1/2 and 2/4 are equal in value (three distinct values).
- **F7 [LOW, judgement call]** **open, judgement call (unchanged in PR #45)** year6 / Stage 1 Q9, index.html:309: "A baby born today is a boy" keyed Even Chance. Conventional, though the real figure is about 0.51; acceptable at this level.
- **F8 [LOW]** **RESOLVED PR #45** ("tend to get closer") year6 / Stage 3 Q10, index.html:346: "The more times you repeat an experiment, the closer results get to theoretical probability" keyed True. Standard GCSE answer, but "tend to get closer" is the accurate form (it is not guaranteed to get closer with every extra trial).

#### Clean
- Stage 2: 19 of 20 keys recomputed exactly and correct; every key appears exactly once in its options; no distractor equal in value to the key (20/20).
- Stage 1: 8 of 10 keys clearly correct (breathe, roll a 7, fair coin, month starting with J = 3/12 = 0.25, red card, even on a die, baby, sun); scale labels' values (0, 0.25, 0.5, 0.75, 1) match the floats compared.
- Stage 3: 13 of 15 statements keyed correctly with correct explanations (all but F2 and the LOW note F8).
- No drawn spinners/bags/figures in this game (text only), so no picture/words check applies.

#### Not checked / limits
- Not run in a browser; marking paths read from source. Bank in data/banks matches source literals (45 items).

**Reviewing session re-check:** F1 re-checked: :333 keyed "2/5"; the letters of MATHS also in GAMES are M, A, S, so 3/5. F2 re-checked: :343 keyed `true`.

**Resolved, PR #45 (4 Oct 2026):** F1 to F6 and F8 fixed (F1's key was already fixed in PR #36; #45 adds its reason line); F7 left as a judgement call. The whole bank is now held in CI by `scripts/verify-probability-pioneer.py`: Stage 2 keys recomputed exactly from each stem, four options with none equal in value, Stage 1 and 3 keys pinned to a reviewed table with reasons, and every answer to all 45 items clicked in Chromium. It failed on the pre-fix bank (9 FAILs).


### Expected Damage (`expected-damage`)
Resit card level: ks3 (opens `?level=ks3`, shown as "Foundation"). Levels audited: ks3 15, gcse 20, core 15 (50 questions). Bank type: static (`QUESTIONS`, index.html:484-542); outcomes are drawn at random at play time.
Marking: a two-way choice (Track A / Track B). `choseHigherEV = choice === q.higherEVOption` (index.html:823) feeds `optimalChoices`, which drives the end-of-session "Optimal Choices %", the stars and `questions_correct` (index.html:930-946). There is no per-question right/wrong message: after a choice the student sees only the random number of Muppets hit (or an escape event). The leaderboard score is `totalScore`, the random Muppets hit (index.html:949), not the number of correct choices.
Items checked: all 50. For each: both options' probabilities summed exactly (Fraction; source literals like `1/3` read as exact thirds), each track's E(X) recomputed, the higher track recomputed and compared with `higherEVOption`, stored `ev`/`evDifference`, `escapeEventPossible` vs sums below 1, every displayed probability passed through a copy of `formatProb()` (index.html:709) to confirm the shown % or fraction equals the stored value; all 14 word problems read against their outcome lists. The game's outcome draw (`resolveOutcome`, index.html:774) was modelled exactly and confirmed by a 2-million-draw Monte Carlo of the copied code. Scripts: scratchpad/work/expected-damage/check.py (out.txt), sim.py (sim_out.txt), mc.js (mc_out.txt).

#### Faults
- **F1 [HIGH]** gcse, index.html:514 (`ed_gcse_011`) and index.html:521 (`ed_gcse_018`): equal expected values, but one track is keyed as the only correct choice.
  - ed_gcse_011: Track A "½ chance of 7, ½ chance of 3"; Track B "40% chance of 11, 60% chance of 1". E(A) = 3.5 + 1.5 = 5; E(B) = 4.4 + 0.6 = 5. Keyed: A only (the bank even stores `evDifference: 0.0`). Correct: either.
  - ed_gcse_018: Track A "¾ chance of 5, ¼ chance of 1"; Track B "⅓ chance of 12, ⅔ chance of 0". E(A) = 3.75 + 0.25 = 4; E(B) = 4 + 0 = 4. Keyed: A only (`evDifference: 0.0`). Correct: either.
  - A student who calculates correctly and picks B is counted as a non-optimal choice (lower Optimal Choices %, fewer stars, `correct:false` in analytics).
  - Share affected: 2 of 20 GCSE questions (10%, which meets the audit's share threshold for CRITICAL; graded HIGH because the miscount shows only in the end-of-session percentage and stars, not as a per-question "wrong"). Caller to rule.
- **F2 [MEDIUM]** all levels, index.html:789 (and the "optimal" replay at index.html:812): the outcome draw does not follow the probabilities shown on screen whenever a track's probabilities total less than 1.
  - Code: escape if `roll > pSum`; otherwise `adjustedRoll = roll * Math.min(pSum, 1)` and the first outcome whose running total reaches `adjustedRoll` is hit. Given no escape, `roll` is already uniform on [0, pSum], so multiplying by pSum again squeezes it into [0, pSum²] and over-weights the first listed outcome. (Using `roll` itself would give exactly the stated probabilities.)
  - Example ed_ks3_014 (index.html:499), Track B shown "50% chance of 8, 30% chance of 2": the game actually hits 8 with probability 5/8 and 2 with 7/40 (escape 1/5 is right). Its E(B) as played is 5.35, not the stated 4.6, so the keyed track A (E = 5) yields fewer Muppets on average than B. Same flip on ed_gcse_016 (index.html:519): B played 5.44 vs keyed A 5. Monte Carlo of the copied code: ks3_014 B mean 5.349, gcse_016 B mean 5.443.
  - Share affected: 20 of 50 questions play outcomes at probabilities other than those displayed (ks3 3/15, gcse 9/20, core 8/15); on 2 of them (ks3_014, gcse_016) the track keyed as higher-EV is the lower-scoring one in play. Marking (`higherEVOption`) is unaffected, but the leaderboard score, the "Optimal play would have hit N" figure and the closing claim "The students who scored closest to optimal were not luckier. They calculated." rest on this draw.
- **F3 [LOW]** all levels: no per-question feedback. The trolley shows "E(X)=?" and then only the random hit count; the game never says which track had the higher E(X) or what the two values were, so a student cannot find out whether a choice was right (results show only an overall %).
- **F4 [LOW]** all levels, index.html:665: when both tracks total less than 1 with different totals, the hint shows only the smaller total ("⚠️ probability: 85%"), e.g. ed_gcse_020, ed_core_003, ed_core_010, ed_core_014 (A 90%/B 85% or reverse). The per-outcome percentages are still shown, so E(X) can be computed; the hint text itself is unclear.
- **F5 [LOW, judgement call]** word problems: several describe one person but count several Muppets on the track, e.g. ed_ks3_008 B "a man walking while watching a football match... There are 5 people on this track"; ed_ks3_009 B "a woman walking her dog... There are 9 people"; ed_ks3_015 B, ed_gcse_005 B, ed_gcse_016 B ("someone... N people"); ed_core_012 A ("a man... 6 people") and B ("a pair of people... There are 5 people"). Only ed_gcse_007 states the rule that the others follow the one person. The outcome lines with explicit numbers are shown under each story, so keys are unaffected.
- **F6 [LOW]** core start-screen text "Gaps under 0.2" (index.html:332) is false for most core questions (gaps 0.12 to 4.6; only ed_core_003, 011 under 0.2). Cosmetic.
- **F7 [LOW]** `renderMuppets` draws at most 8 figures (index.html:726-730); 26 tracks hold 9 to 16 Muppets (e.g. ed_ks3_011 B, 16). Decorative, the numbers are in text.

#### Clean
- Probabilities: no track sums above 1 (50/50); `escapeEventPossible` agrees with "some track sums below 1" on all 50; stored `ev` and `evDifference` exact on all 50.
- Keys: 48 of 50 `higherEVOption` keys are the strictly higher E(X) (all except the two ties in F1); ks3 15/15, core 15/15, gcse 18/20.
- Display: every probability shown on screen (% via `Math.round`, or ⅓ ⅔ ¼ ¾ ½ 3/5 2/5) equals the stored value exactly; no rounding hides a value (50/50).
- Word problems: all 14 outcome lists match the numbers in their stories (people counts, percentages; ed_core_014's "twice... sum to 0.9" gives 0.6 and 0.3 as stored).
- Money/units: not applicable (counts of Muppets only).

#### Not checked / limits
- Not played in a browser; marking and draw paths read from source and the draw modelled exactly + Monte Carlo of the copied code.

**Reviewing session re-check:** F1 re-checked: :514 (EV 5.0 and 5.0) and :521 (EV 4.0 and 4.0), `higherEVOption:'A'` in both; the choice is scored by `choice === q.higherEVOption` (:823).


### Given That (`given-that`)
Resit card level: gcse (opens `?level=gcse`, picker). Levels audited: gcse 25, alevel 25, core 20, level4 20 (90 questions, each with two phases = 180 marked items). Bank type: static (`QUESTIONS` inside a module IIFE, index.html:310-409); a session draws 10 questions at random.
Marking:
- gcse: multiple choice, both phases. The correct option is `phaseData.options[0]` and the click is compared by LaTeX string (`chosen===correctLatex`, index.html:782); phase 2 allows a second try.
- alevel, core, level4: typed answer, one attempt. `parseAnswer()` (index.html:879) reads a fraction, a decimal or a percentage, and the answer is marked `Math.abs(userVal - phaseData.answer) <= 0.005` (index.html:842). This is game-local, not `MaffsAnswer`; no question states a precision.
Items checked: all 180.
- Every table, Venn and tree was checked for internal consistency: rows and columns add to their totals; Venn regions add to the total and to each set total; tree children add to their branch and branches to the total; tree "(x%)" labels match the counts; titles match the totals.
- Every key was recomputed exactly (Fraction) from the data the student sees. Each key was matched to the named probability it equals, and that name was read against the question wording.
- gcse options: key at options[0], four distinct strings, no option equal in value to the key, and pairs of distractors equal in value to each other.
- The free-entry rule was replayed with JS float semantics on correctly rounded typed answers (1 d.p., 2 d.p. half up, 3 d.p., %, fraction), and on every other natural probability from the same data, to see what the tolerance accepts.
- Grey-out inference (`inferGreyOut`) was run on all 90 questions. Explanation arithmetic was checked.
- Scripts in scratchpad/work/given-that/: check.py (out.txt), tol.js (tol_out.txt), near.py, labels.py, grey.js (grey_out.txt); compact.txt is a readable dump of the bank.

#### Faults
- **F1 [HIGH]** alevel, index.html:356 (`alevel_18`): the Venn diagram contradicts the key.
  - Data drawn: M only 35, M∩P 45, P only 20, neither 50, Total 150 (the set totals are not drawn). Stored `setB.total: 60`, but 20 + 45 = 65.
  - Phase 2 question: "Find P(takes Maths | takes Physics)."   Keyed: 45/60 = 0.75.   Correct from the diagram: 45/65 = 9/13 ≈ 0.692.
  - A student who reads the diagram correctly (0.692) is marked wrong (|0.692 − 0.75| = 0.058 > 0.005), and the worked answer says "60 students take Physics". Phase 1 (45/150) is unaffected.
  - Share affected: 1 of 25 A-level questions (phase 2).
- **F2 [HIGH]** alevel/core/level4, index.html:842 (the free-entry rule): no precision is stated, and a correctly rounded answer is rejected.
  - The rule accepts within ±0.005 of a value that is itself stored rounded. No question or screen states a precision (the placeholder only shows "e.g. 3/7 or 0.429 or 42.9%"), against SR-1.
  - Two decimal places, rounded half up, is rejected wherever the exact answer ends in 5 in the third decimal place. Both neighbours sit exactly 0.005 away, and the float difference exceeds 0.005:
    - alevel_12 phase 1 (346/400 = 0.865): 0.87 and 0.86 both rejected, also "87%".
    - alevel_19 phase 2 (0.625): 0.63 rejected.
    - alevel_20 phase 1 (45/1000 = 0.045): 0.05 and "5%" rejected.
    - core_03 phase 1 (0.375): 0.38 rejected.
    - core_08 phase 1 (0.325): 0.33 rejected.
    - core_15 phase 2 (0.625): 0.63 rejected.
    - core_16 phase 1 (0.175): 0.18 rejected.
    - l4_02 phase 2 (0.175): 0.18 rejected.
    - l4_10 phase 2 (0.625): 0.63 rejected.
    - l4_14 phase 2 (0.625): 0.63 rejected.
  - Any 1 d.p. answer is rejected on 89 of the 130 free-entry items (e.g. 3/7 typed as 0.4).
  - Share affected (2 d.p.): alevel 3 of 50 items, core 4 of 40, level4 3 of 40. Fix: state the precision on each question (or accept exact fractions only) and mark through `MaffsAnswer.decimal`.
- **F3 [HIGH]** core/alevel/level4, index.html:842: the absolute ±0.005 tolerance accepts named wrong answers on small probabilities (canon 7.1.2).
  - core_04 phase 1 (index.html:369), "What proportion of people test positive?" Key 448/10000 = 0.0448. Accepts 0.04 = 400/10000, the true positives only (forgetting the 48 false positives): the classic screening error.
  - core_06 phase 1 (index.html:371), "What proportion of bags trigger an alert?" Key 2590/50000 = 0.0518. Accepts 0.0499 = 2495/50000 (false alerts only) and 0.05 (the 5% false-alert rate).
  - core_12 phase 1 (index.html:377), "What proportion of the time does the alarm go off?" Key 2088/20000 = 0.1044. Accepts 0.0995 = 1990/20000 (false alarms only). It also accepts 0.1, which is both the false-alarm rate and a 1 d.p. rounding of the key.
  - alevel_22 phase 2 (index.html:360), "Using P(A ∩ B) = 0.3 and P(A) = 0.55, find P(B|A)." Key 6/11 ≈ 0.5455. Accepts 0.55, i.e. typing P(A) from the question.
  - l4_04 phase 1 (index.html:391), "Find P(major defect)." Key 380/3000 = 0.1267. Accepts P(minor defect) = 370/3000 = 0.1233, the adjacent row.
  - Share affected: core 3 of 40 items, alevel 1 of 50, level4 1 of 40.
  - The tolerance also accepts contrived combinations elsewhere, not named errors and not counted here (core_03 phase 1, l4_02 phases 1 and 2, l4_04 phase 2, l4_08 phase 2; see near.py output).
- **F4 [LOW]** gcse, index.html:325 (`gcse_14` phase 2): "What is P(red | even)?", options 60/90 (key), 60/180, 30/90, 90/180. The key is correct, but distractors 60/180 and 30/90 are both 1/3, so there are only three distinct values.
- **F5 [LOW]** gcse, index.html:334 (`gcse_23` phase 2): "What is P(has Disney+ | has Netflix)?", options 20/50 (key), 20/75, 20/30, 50/75. The key is correct, but distractors 20/30 and 50/75 are both 2/3. (Independent data here: the key 0.4 also equals phase 1's P(Disney+) = 30/75, which is not offered, so there is no marking issue.)
- **F6 [LOW]** alevel/core/level4: the explanation for phase 1 is never shown (only phase 2 has `explanation`). After a wrong phase 1 the student sees only "The answer was …".

#### Clean
- Data consistency: 89 of 90 diagrams internally consistent (all tables' rows, columns and grand totals; all tree sums and every "(x%)" label; all titles). The one failure is alevel_18 (F1). Zero-count leaves "(n/a)" in core_20, l4_03 and l4_17 are hidden by `renderTree` and change no answer.
- Keys: 179 of 180 keys equal the exact probability the question asks for, read from the data shown. The exception is alevel_18 phase 2. These include all Bayes reversals in trees (P(branch | leaf)) and the A-level joint tables (alevel_11, 16, 24) and formula questions (alevel_06, 22).
- Stored `answer` decimals agree with `answerDisplay` to 4 d.p. on all 180.
- gcse MCQ: 50 of 50 have four options, key = options[0] = answerDisplay, the key appears once, and no distractor is equal in value to the key.
- Explanations: every "a/b = c/d" and "≈" value in the explanations is correct; the 11 Bayes explanations give correctly rounded decimals.
- Grey-out (the visual "given that" highlight): every explicit and inferred grey-out greys the non-condition columns, regions or branches. Where inference finds no match (conditions on a leaf or a row), nothing is greyed, which is safe.

#### Not checked / limits
- Not played in a browser; MCQ and free-entry marking replayed from copied source. The KaTeX rendering of options was not inspected visually.

**Reviewing session re-check:** F1 re-checked: :356, `onlyB:20, intersection:45` but `setB.total:60`, and P(M|P) keyed 45/60. F2/F3 re-checked: :842, `Math.abs(userVal - phaseData.answer) <= 0.005`, with no precision stated in any free-entry ask.


### Correlation or Coincidence (`correlation-or-coincidence`)
Resit card level: single level shown. The game has no levels: `?level=` is ignored and every event and score uses the hard-coded level `'gcse'` (index.html:266, 314, 362). The roster's "GCSE, A-Level, Core" and the extract's "gcse/alevel/core, 13 each" are the same 13-question bank, loaded three times. Levels audited: the one bank, 13 questions (8 spurious, 5 real); a session plays 12 (`MAX_Q`, index.html:254). Bank type: static (`QUESTIONS`, index.html:128-205).
Marking: a two-button choice, "Yes — real causal relationship" or "No — just a coincidence". `btn.dataset.val === correctAnswer`, where `correctAnswer` comes from `q.type` (index.html:298-300; key at 299). +100 per correct answer, and the score is submitted to the leaderboard (index.html:363).
Items checked: all 13.
- Pearson r recomputed exactly (Fraction sums) from each question's plotted `data1`/`data2` and compared with the stated `r` shown after answering: scratchpad/work/correlation-or-coincidence/r.py, output r_out.txt; bank.json is the extracted bank.
- Each real/spurious classification judged.
- The display code read to see what the student has when answering.

#### Faults
- **F1 [CRITICAL]** every question, index.html:114 (markup) and index.html:46, 280-281 (CSS and reset): Phase 1 cannot be answered from what is on screen.
  - When the student must choose real or coincidence, the two chart labels are present but painted invisible (`.chart-label.hidden{color:transparent}`). The canvases draw no axis titles, tick values or units (`drawChart`, index.html:210-251). The dataset names (`reveal`) and `r` appear only after the click (`handlePhase1`, index.html:305-321).
  - The prompt asks "These two datasets appear to correlate. Is there a real causal relationship?" (index.html:287) about two unlabelled, auto-scaled line shapes, so whether a causal mechanism exists cannot be judged. Every pair is drawn rising (or falling) together, so the shapes carry no cue, and the answer is a coin toss.
  - The marking is consistent with `type`, but the student is scored, and ranked on the leaderboard, on a guess. The game's stated lesson ("Always ask: what is the causal mechanism?", index.html:360) cannot be applied, because the variables are hidden.
  - Share affected: 13 of 13 questions (100%). Fix: show the two variable names (and axes) before the choice; reveal `r` and the explanation after.
- **F2 [MEDIUM]** 11 of 13 questions: the stated correlation coefficient disagrees with the data plotted. "Correlation coefficient: r = …" is shown after each answer (index.html:312); computed values to 2 d.p. (label lines):
  - L132 Nicolas Cage films vs pool drownings: stated 0.87, data 0.99.
  - L138 US science spending vs suicides by hanging: stated 0.92, data 1.00 (0.9987).
  - L144 Cheese vs bedsheet deaths: stated 0.95, data 0.98.
  - L150 Robot films vs ski revenue: stated 0.91, data 1.00 (0.9967).
  - L156 Organic food vs autism diagnoses: stated 0.88, data 0.95.
  - L164 Height vs weight: stated 0.94, data 1.00 (0.9977).
  - L169 Study hours vs exam score: stated 0.97, data 1.00 (0.9967).
  - L184 Cigarettes vs lung capacity: stated −0.98, data −1.00 (−0.9976).
  - L190 Devon maths teachers vs shark attacks: stated 0.89, data 1.00 (0.9960).
  - L196 UK butter vs Maine divorce: stated 0.99, data exactly 1. The plotted series is perfectly linear: divorce = butter/5 − 12.
  - L202 Renewables vs pirates: stated 0.85, data 0.88.
  - Only L174 (ice cream, 0.92) and L179 (house price, −0.96) agree.
- **F3 [MEDIUM, content judgement, not maths]** L138: "Suicides by hanging per year" is played for laughs. The Phase 2 "conspiracies" include "The peer review process is so brutal it drives people to desperate measures" and "Government science labs are secretly powered by the souls of the despondent" (index.html:140). For a resit audience this is a safeguarding risk worth Jon's review; the other death-themed pairs (drownings, bedsheet deaths) are milder.
- **F4 [LOW]** spurious questions (7 of 8, all but the `serious` one): `q.explain` is never shown. `handlePhase1` routes them to `showPhase2`, which shows only a joke mechanism (index.html:326-327, 340-349). The real explanation ("Both happened to trend upward over the same decade…") is authored but unreachable.
- **F5 [LOW, judgement call]** L156 explanation: "This is one of the most harmful spurious correlations in history". The well-known harmful claim is vaccines and autism; the organic-food chart is a satirical example. Overstated. The classification (spurious) is right.
- **F6 [LOW, judgement call]** L169 "Hours of study per week vs Exam score" keyed real causal. Defensible at this level (the explanation names the mechanism). The real/spurious split is otherwise sound: height/weight, temperature/ice cream, distance/house price and smoking/lung capacity are causal; the eight spurious pairs have no plausible mechanism.
- **F7 [LOW]** real, cross-sectional pairs (height/weight, distance/price, cigarettes/lung capacity) are drawn as two line charts against row order, a time-series display for data with no time order. The "real" pairs are also sorted so the lines rise together, which a scatter graph would show properly.
- **F8 [LOW]** the hidden label elements keep the previous question's text (`textContent` is not reset in `nextQ`, index.html:279-281), so a screen reader or a text selection reads the last question's variable names on the new charts.

#### Clean
- Marking: the button value is compared to the key string built from `type`; both strings are identical literals, so no mismatch is possible (13/13).
- Classifications: 13 of 13 keyed defensibly (5 real, 8 spurious), with the judgement notes F5 and F6.
- Data arrays: all 13 pairs have equal length (10 and 10), so the plots are well formed.

#### Not checked / limits
- Not rendered in a browser; display behaviour read from source (CSS `color:transparent` on the labels, no axis text in `drawChart`). The real-world figures behind the spurious pairs (e.g. 12-18 Nicolas Cage films a year) are implausible, but no values are displayed, so they were not treated as faults.

**Reviewing session re-check:** F1 re-checked: `.chart-label.hidden{color:transparent}` (:46), set on every new question (:280-281); `drawChart` draws no text; the labels and r are revealed in `handlePhase1` (:305-312), in the same handler that scores the answer.
