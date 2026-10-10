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
1. **RIGHTFUL-KING-BUILD** (contract `docs/handover/contracts/2026-10-10-rightful-king-build.md`), then
2. **LIBRARY-JAM-BUILD** (contract `docs/handover/contracts/2026-10-10-library-jam-build.md`).
**BOTH WAIT on BOTH home-lane fixes, ART-PENDING and KEYPAD-VARIABLE (Jon, 10 Oct), not KEYPAD-VARIABLE alone.**
ART-PENDING is on main (#244: `HAS_ART` in engine.js). KEYPAD-VARIABLE was not on main when checked (10 Oct): no
`maxDigits` in `escape-rooms/assets/engine.js` or the scripts, and no branch for it. Before starting, check main for
both and read `docs/handover/home.md`.
**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's
last full run is green, without asking each time; it still watches main's run after each merge. Ratings for the handover when built: The Rightful
King ★★★ Challenge, The Library Jam ★ Warm-up (no star field; the difficulty contract owns it).
**FONT-FIT (Jon, 10 Oct 11:05; contract `docs/handover/contracts/2026-10-10-font-fit.md`): IN PROGRESS on branch
`claude/youthful-feynman-anpxuq-font-fit`, no PR yet. CHECKPOINT 10 Oct.** Findings: `docs/audits/font-fit-2026-10-10.md`.
- **Jon's answers (10 Oct):**
  - Stage 5's how-to line shows on the first problem only, and a game opens on one of the 25 problems that fit
    with it (`FORM_OPENERS`).
  - The self-test is planted on pages where the fonts decide the verdict.
- **Done, all on the branch:**
  - `scripts/fonts/`: KaTeX 0.16.9 and every Google Fonts file the site requests, with SHA256SUMS, licences
    (MIT and OFL; Special Elite Apache 2.0) and `fetch-fonts.py`.
  - `bank_common`: `real_font_response` and `serve_real_font(_async)`.
  - Measured in the real fonts: check-site's phone pass, `measure-phone-fit.py` (now seeded; `--fonts fallback`
    compares) and nine fold verifiers. `check-keypad` aborts everything on a fixture with no web fonts, so it is
    unchanged.
  - `checker-allowlist.json`: 12 entries that fit in the real fonts removed; distinctly-average added as known.
  - `test-real-fonts.py` (new ci-line): the pin is complete and checksummed; plant: the old blocking changes
    distinctly-average's width from 334 to 320 px.
  - **Simultaneous Solver:**
    - `fitInView` gives an 8 px margin, re-fitted when the fonts arrive; Stage 5 keeps its form in view;
      `formHow` shows on the first problem only; `FORM_OPENERS`.
    - Its verifier: real fonts, `MARGIN = 8`, `fit_check` over Stages 1-5 at three sizes (the opener list proved
      exact), and the plant: with Google Fonts blocked, W01 needs 533 of 512 px. PASS.
- **Open, decide next:** two fold verifiers newly FAIL in the real fonts at 320x568, so CI would be red:
  - free-daily-pizza: Next at 533 against a 528 fold (Stage 4, 9 of 30);
  - negative-number-line: Confirm at 536 against 528, with a marker placed.
  - Newly over in all: 9 pages (6 fold from measure-phone-fit, 1 width, these 2), under the 15 limit.
  - **Ask Jon how these two go green** (fix the pages, or record them as known) before opening the PR.
- **Then:** `check-changed.py`, open the PR, merge on green, watch main.
- **For the home lane:** CI's DejaVu pin step can be retired for the phone checks once this merges (not removed).
- Local runs used `FONTCONFIG_FILE` pinning DejaVu, as CI does (scratch `fonts.conf`).
**Open for Jon:** delete branch `claude/youthful-feynman-anpxuq-pd-check` in GitHub (the proxy refused the remote
delete, HTTP 403).
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

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

## 2026-10-10 (cloud): CAR-TRAP-BUILD, the rewritten Car Trap built behind its holding page (awaiting Jon's play-test)

- **10 Oct, after ART-PENDING (#244): rebased on main; `art` dropped.** The room requests no picture.
  check-escape-rooms lists it as art pending (VALID 352 of 512). Tier 1 passes the play page, and
  `test-escape-art.py` passes.
  - **Still red, one failure:** the teacher page is 545 px wide at 320 px. This is the shared `table.tt` overflow
    (todo §1.37). **Jon (10 Oct): the home lane fixes §1.37 first; no allowlist entry.** #242 waits for that.
  - **Jon's message of 10 Oct ("the Car Trap art is now on main; set art to those pictures; rewrite winAlt for the
    win picture's high CCTV-style view") did not match main.** The only `car-trap-*.webp` on main are the OLD
    pictures: an orange sports car reversing into a VISITOR bay before a crowd of staff, an eye-level view. Main is
    unchanged in `docs/art/` since before #242, and home.md names no new files.
    - So `art` was NOT set and winAlt was NOT rewritten: pointing at those would show the wrong premise, and an alt
      cannot be written for a picture not seen.
    - When the new files are on main: add `art:` naming them, check all three alts against them, and rewrite winAlt
      for the win picture's view.

- **Built from the approved draft with Jon's changes (9 Oct, 22:53).**
  - "The dullest car in the county" appears once, in the hook (scripted count: 1).
  - The stakes and lock 3's onOpen are as ruled.
  - Wrong-entry line 1 carries the figure in words.
  - The only figures in the prose outside tokens are the draft's flagged words and locks 2 and 3's unchanged method
    constants. Mr Strictman is invented, Jon confirmed.
- **For the difficulty contract: the room is ★★ Core** (Jon's ruling 3). No star field or label was added anywhere.
- **Lock 1, `head-bay-lower-bound`, is bank batch 8** (`docs/lock-bank-batch8.txt`; check-lock-bank `unique (2.35)`).
  - Its library is in `gen-escape-variants.py`: the draft's eight widths, variant 0 = 2.4, the draft's solver, all
    eight kept.
  - The generator also writes the room's `variants:` blocks.
  - `visitor-space-bounds` leaves the room; its bank entry and library stay as history.
  - Locks 2 and 3: a scripted diff shows id, key, instrument, variants, missTitle, hints and solve unchanged. Only
    framing and missSays' last clause changed, per the draft.
  - **check-escape-rooms: car-trap VALID 352 of 512, variant 0 VALID**, as the draft measured.
- **The generator's paths are Jon's machine's** (`E:\jon\maffsgames\...`). The cloud lane runs it through a scratch
  wrapper that swaps in this checkout's paths at run time; the script's paths are unchanged.
  - Before the new library went in, a run reproduced every existing library byte for byte.
  - Only car-trap's room.js and variants.json changed.
- **Art pending.** `art: 'car-trap-v2'` has no files yet, so the engine drops the frame and none of the six old pictures
  shows (they stay in docs/art/ untouched). No lock has art or missArt (the rule is in room.js's header).
  - **Filing Jon's three pictures is a separate step:** file them as `car-trap-v2-scene`, `-fail` and `-win.webp`, or
    file over the old names and set `art` back to `car-trap`.
  - The three alts are the draft's, to be checked against the pictures before release.
- **Pages (Jon's answers, 10 Oct):**
  - `teacher.html` is the real teacher page (noindex, unlinked).
  - `play.html` is the play-test page: noindex, linked from nowhere, analytics off (no gtag, no analytics.js, so the
    engine sends no events).
  - `index.html` stays the holding page.
  - **At release, in one PR:** play.html's content becomes index.html, with prom-budget's head lines (analytics, meta,
    og:) put back; play.html is deleted; then the §5c release steps.
- **Played through in Chromium** on serve-stubbed, with no page errors and nothing sent off-origin.
  - It shows every object and all three lock briefs on screen.
  - The four wrong-entry lines arrive in order, then the last repeats.
  - Each lock's misconception gives its own response.
  - All three locks open on their answers; lock 1 is set by the slider's arrow keys.
  - Then the win screen; a second play times out to the stakes after "And so:".
  - The teacher page follows the draw. The cloud session cannot open Jon's Chrome: that is what play.html is for.

## 2026-10-09 (cloud): PD-CLOSE, LISTED-HIGH item 12 closed (Jon's ruling, 22:45, option A)

- **t4-002 closed by #232 (shared-overlay fix); covered by the OVERLAY-KEYS CI check; per-game check not added
  because the fault was in shared code.** The check is `scripts/test-initials-overlay.py` (in CI). Measured 9 Oct, with
  `--games prisoners-dilemma`: main passes, and its plant is caught. Run `--against` the pre-#232 overlay, it fails
  with 55 keys reaching the game's document keydown. That confirms the check covers this game, so the STOP IF did not fire.
- `verify-prisoners-dilemma.py` is **not** in CI. Its branch, `claude/youthful-feynman-anpxuq-pd-check`, had nothing in
  its handover that main lacks. It was deleted locally, but the remote delete was refused (the sandbox proxy, HTTP
  403), so **Jon deletes it in GitHub's branch list**.
- **prisoners-dilemma-t4-001** (the leaderboard ranks the chosen opponent) stays open for Jon's design decision.
- Jon's note is saved verbatim as `docs/history/contracts/2026-10-09-listed-high-note-2245.md`.
