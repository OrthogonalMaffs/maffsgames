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
LISTED-HIGH: COMPLETE but item 12 (`contracts/2026-10-09-listed-high.md`): #210-#212, #214, #216, #217, #219, #223,
#225-#231 merged; main green (run 654, 37978742832). **Item 12 (PD-CHECK) STOPPED, 9 Oct 20:40: Jon's call, see the
PD-CHECK entry below.** CAR-TRAP-DRAFT (moved from the home lane, Jon 20:17; contract on main,
`contracts/2026-10-09-car-trap-draft.md`): **Car Trap draft for Jon's review**, #235 merged (ba5b6b2); main green
(run 661). Phase 2 waits on Jon's review. **Nothing else is queued for the cloud lane.**
Done: PP-T1-004 (#189; its contract is now in `docs/history/contracts/`).

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-09 (cloud): CAR-TRAP-DRAFT, Car Trap draft for Jon's review (#235 merged ba5b6b2; main run 661 green)

- **Contract:** the repo copy on main, `contracts/2026-10-09-car-trap-draft.md` (Jon's amended text of 16:45, saved
  verbatim by the home lane in dc43926 and merged in #221). It is left where it is, because the home lane's handover
  points to that path; it moves to `docs/history/contracts/` with phase 2.
- **The draft:** `docs/escape-room-drafts/car-trap-draft.md`. It has every slot `room.js` needs, the three art
  prompts, lock 1's variant proposal and bank entry, and the checklist (all pass; two figure exceptions in words,
  both flagged). Its "For Jon" list has 11 decisions, including:
  - **There is no `fail` slot.** The engine shows `stakes` after "If you get it wrong." (`engine.js:238`) and after
    "And so:" on time-out (`:791`), so the Fail is written into `stakes`.
  - **`hook`, `brief` and `stakes` are written raw**, so they can't hold tokens.
- **Lock 1 (`head-bay-lower-bound`, proposed):**
  - W 2.2 to 2.9 m to the nearest ten centimetres; slider 2.00 to 3.00 m, step 0.01; answer W - 0.05; miss the
    stated W.
  - Scratch checks, not committed: `check-lock-bank.py` "unique (2.35)", and all 8 variants pass the generator's
    `keep()` rules.
  - Joint draws by the checker's collision rules: 352 of 512 VALID with the precision in words, 184 with a numeral
    10.
- **Next (phase 2, a separate contract after Jon approves):** the generator block, a lock-bank batch entry,
  `room.js`, `teacher.html`, the art and the release. STOP IF did not fire: no brief/rule clash the draft couldn't
  resolve, and lock 1 has exactly one settable answer in every variant.

## 2026-10-09 (cloud): PD-CHECK (LISTED-HIGH item 12) STOPPED for Jon: #232 fixes t4-002; the saved check is wrong

- **#232 (OVERLAY-KEYS) is on main** (9a0830f, merged 18:46 UTC, before #229; main green, run 654). The pd-check
  branch already contained it: no rebase needed.
- **The saved check FAILS on main** (both cases): STOP IF fired. **But the cause is the check, not the game:** it builds
  its own `<div id="mfg-initials-overlay">`, which #232's listeners (bound to the overlay that `askInitials()` creates)
  never touch; and its "dd typed into a text field" case has no counterpart in this game (prisoners-dilemma has no
  input, textarea or contenteditable; the overlay's inputs are the only text fields it ever shows). Both were written
  for the discarded in-game guard.
- **Measured, real path (scratch probe, not committed; no game code changed):** a tournament in Chromium, match 1
  played to its end with C, the real overlay opened by `submitScore`, match 2 ready, "CDC" typed into the overlay.
  Main's overlay: round 0 -> 0, nothing played, the overlay holds "CDC"; C plays a move after Skip. The pre-#232 overlay
  (`6642c82~1`): round 0 -> 1, a move played, the overlay holds "DC" (the first initial went to the game).
- **Already in CI:** #232's `scripts/test-initials-overlay.py` opens the real overlay in prisoners-dilemma, types a-z
  (so C and D), and fails if any game key listener sees a key: stronger than "no move played". It names
  prisoners-dilemma among the 11 games whose shortcuts fired before the fix.
- **For Jon (recommendation A):** close t4-002 citing #232 and `test-initials-overlay.py`; retire the saved check (no
  PR, no new CI line). The bug was a shared-layer bug, fixed and tested there across 97 games; a per-game copy would test
  a weaker property of the same code. **B:** rewrite the check on the real path above (the probe, as a verifier;
  self-test serves the pre-#232 overlay and must FAIL), drop the text-field case, wire it in, close t4-002. Either way
  the text-field case goes: no such field exists in this game. **t4-001** stays open (SR-22, Jon's leaderboard).
- Branch `claude/youthful-feynman-anpxuq-pd-check` left as it was (its check unchanged, no PR).

## 2026-10-09 (cloud): LISTED-HIGH (complete but item 12; contract in `contracts/2026-10-09-listed-high.md`)

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
- **13a characteristic-quest t6-001: #228** (stacked on #227): closed with measurements, no code change.
- **13b eigenvalue-extractor t6-001: #229** (stacked on #228): closed with measurements, no code change.
- **13c matrix-crunch t6-001, t6-002: #230** (stacked on #229): new `verify-matrix-crunch.py` (~40 s, both levels,
  the flag path check-answer-lock never presses); fails the pre-batch page with the audit's numbers.
- **13d formula-forge t4-001: #231** (stacked on #230): closed with measurements, no code change. **LISTED-HIGH is done
  but item 12** (held for OVERLAY-KEYS); the remaining list is empty.
- **CI (CI-BALANCE, #220):** groups are packed now. A new verifier's header is `# ci-line: <label> | <args>` (no
  group id); untimed lines get a group each until main's timings job records them. `ci-groups.py --check` locally.
- **Local checks used for each PR** (the sandbox cannot reach the KaTeX CDN): check-changed's plan, the answer lock for
  the changed game with KaTeX served locally, and `extract-banks.py --only <slug>` + `check-banks.py --ci --only
  <slug>` (stale B11 ledger entries must leave `data/check-ledger.json` with the fix). esprima: unpack its sdist on
  PYTHONPATH. Teacher-line fails locally on factor-theorem and log-laws only (KaTeX CDN): not a change's fault.
- **Item 12, prisoners-dilemma t4-002: waiting on the home lane's OVERLAY-KEYS (#232)** (Jon, 18:56; note in
  `contracts/2026-10-09-listed-high-note-1900.md`). The drafted in-game keydown guard was **discarded**, in no PR: it
  was the defensive-patch shape (the shared initials overlay lets typed keys reach page shortcuts in every game with a
  document keydown handler; the overlay is the fix). **The check is saved on branch
  `claude/youthful-feynman-anpxuq-pd-check`** (`scripts/verify-prisoners-dilemma.py`, verbatim from the scratchpad;
  no PR, not in CI: it fails main until #232 is on main). It asserts, on a tournament's first match in Chromium: C
  pressed on the game screen plays a move; "CDC" typed into the initials overlay (`#mfg-initials-overlay`, an input
  focused in it) plays nothing; "dd" typed into any other text field plays nothing. **When #232 is on main:** run it
  against prisoners-dilemma with no change to the game's code; it must pass. Its self-test plants the discarded
  in-game guard, so it reports CANNOT PLANT: rewrite the plant to serve main's pre-#232 overlay module (the shared
  file's old content) and confirm it FAILs, update the `ci-line` header to the packed form (`# ci-line: <label> |`),
  then open the PR (claim prisoners-dilemma first), closing t4-002. **t4-001** (the board ranks whichever opponent is
  chosen) stays open: Jon's leaderboard design, not this lane's.
- **Stacked PRs (Jon's ruling, 9 Oct 20:20): one branch per PR, stacked, is fine.** #226-#231 were each on
  `claude/youthful-feynman-anpxuq-<game>`, opened together so CI ran in parallel, merged strictly in order, each on a
  green Gate with main green on the previous merge.
