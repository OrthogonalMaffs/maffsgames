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
1. **RIGHTFUL-KING-BUILD** (contract `docs/handover/contracts/2026-10-10-rightful-king-build.md`): **IN PROGRESS** on
   `claude/compassionate-cori-3xi42y` (started 10 Oct, 14:45, after FONT-FIT's main run was green). Then
2. **LIBRARY-JAM-BUILD** (contract `docs/handover/contracts/2026-10-10-library-jam-build.md`).
Both shared fixes they waited on are on main: ART-PENDING (#244) and KEYPAD-VARIABLE (#251, `maxDigits`).
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

## 2026-10-10 (cloud): RIGHTFUL-KING-BUILD, The Rightful King built behind its holding page (for Jon's play-test)

- **Jon can play-test it at `/escape-rooms/rightful-king/play.html`** (noindex, linked from nowhere, analytics off).
  `index.html` is a noindex "coming soon" holding page; `teacher.html` is the real teacher page (noindex, unlinked).
  There is no hub card, sitemap entry or count change: the release contract brings those, with the ★★★ chip.
- **Art pending:** no `art` field, so no picture is requested. Jon generates the three pictures after his play-test.
  The alts are the draft's.
- **Locks (bank batch 9, `docs/lock-bank-batch9.txt`; check-lock-bank: unique on all three):**
  - `admin-passcode-product-rule`, grade 6: the product rule with no repeats (Higher). maxDigits 3; k = 5 to 9 with
    L = 3 (60, 120, 210, 336, 504); variant 0 is k = 7.
  - `vote-log-overwrite`, grade 5: building powers of one multiplier, the method #253 graded 5 in Prom (the draft
    said 7). The library is the draft's ten sets, each through the rules, including (1 - f) x 100 not a multiple
    of r. The generator asserts that the 3 d.p. powers keep their comparison with the threshold.
  - `leak-audit-conditional`, grade 7: conditional probability from a Venn diagram (Higher). The library is the
    draft's seven sets, under its story rules.
- **Derived rating, from check-escape-rooms' own `room_rating()`: ★★★ Challenge (grades 6–9).** No grade was fitted.
- **check-escape-rooms:** rightful-king VALID **215 of 350**, variant 0 VALID (the draft measured 183 of 280; the
  fifth passcode set adds draws).
- **The old URL:** `it-vengeance/index.html` is a noindex meta-refresh to `/escape-rooms/rightful-king/` with a
  plain link (ruling 6). `it-vengeance/room.js` and `teacher.html` stay as history. The checker reads every room
  folder; a noindex index makes it not live, so it needs no card or grade.
- **Played headless (scratch script, four draws, all PASS):**
  - Start screen: the brief, ★★★ CHALLENGE · GRADES 6–9, and the stakes after "If you get it wrong."
  - All 8 objects and all 3 lock briefs on screen, every token filled.
  - Four wrong lines in order, then the last repeats. Each misconception gives its own response.
  - All three locks open; k = 5's 60 opens on the up-to-three-digit keypad. Then the win screen ("It was my
    prompt").
  - A time-out ends on the stakes after "And so:".
  - No page errors, no 4xx, nothing sent to analytics.
  - The teacher page shows ★★★, "Suits a top set" and the calculator note. The old URL lands on the holding page.
- **Generator:** run through a scratch wrapper that swaps in this checkout's paths. Before the M block went in, a run
  reproduced every existing library byte for byte.

## 2026-10-10 (cloud): LIBRARY-DRAFT, Library room draft for Jon's review

- **The draft:** `docs/escape-room-drafts/library-draft.md`. It has three title options; **Jon chose The Library Jam
  (10 Oct)**, slug proposed `library-jam`, every slot, three locks with libraries (8, 8 and 10 variants), the alts, hub and meta lines,
  and the checklist. Jon's line is wrong-entry line 3, verbatim. No art prompts.
- **For Jon 1, the big one: lock C needs a keypad that takes "up to four digits", and the engine's keypad takes
  exactly `digits`** (`engine.js:610`, and `:593` drops extra digits). A four-digit keypad shows four slots, which
  steers a student to 5400, the misconception. A two-digit keypad turns a typed 5400 into 54, right by accident.
  Rightful King's lock 1 hit the same limit, so the fix is shared: an opt-in variable-length keypad in `engine.js`
  (home lane), plus the generator's `keep()` edge rule for keypads. Recommended before phase 2.
- **Measured (scratch):** the checker's own `draw_is_valid()` on the draft's clues gives **572 of 640 VALID, variant
  0 VALID**. Fines are multiples of 5p, to stay non-calculator (For Jon 6).

## 2026-10-10 (cloud): RIGHTFUL-KING-DRAFT, Rightful King draft for Jon's review

- **The draft:** `docs/escape-room-drafts/rightful-king-draft.md`. It has every slot `room.js` needs, three new
  locks with proposed libraries, bank entries, the teacher-page line, and the checklist (all pass). No art prompts.
  Its "For Jon" list has 14 items. The ones that change the contract's maths:
  - **Lock 1:** the example sets 60, 24, 42 can't go on a three-digit keypad (the engine wants every digit; no
    leading zero). The only all-three-digit sets with L >= 3 are k = 6 to 9, L = 3, so the library is 4 (120, 210,
    336, 504). Variant 0 is k = 7 (210), because 120 collides with audit set 0's 120 voters.
  - **Lock 2:** where r divides (1 - f) x 100 exactly, a strict linear reader lands one minute later. For 25 with
    a half that is the right answer, so the misconception scores. Proposed: reject those sets. Whole-number r from
    5 to 40 gives 10 variants; the lock needs a calculator.
  - **Lock 3:** the set 150, 70, 50, 60 prints its own answer (60). Proposed story rules: he has 30-60% of the
    vote, P(him | saw it) is at least 20 points above P(him | didn't), and S is not 100. The library is 7.
- **Measured (scratch, nothing committed):** `check-lock-bank.py` says unique on all three bank entries. The
  checker's own `draw_is_valid()` on the draft's clue strings gives **183 of 280 VALID, variant 0 VALID**.
- **STOP IF did not fire:** prom-budget was read in full and never mentions a vote, a king or Narry.
- **Next:** LIBRARY-DRAFT. Phase 2 of The Rightful King is a separate contract after Jon approves.
