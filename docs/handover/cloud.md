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

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-08 (cloud): CHECKPOINT STOP (Jon): listed-games contract at 2 of 23; nothing claimed

- **Where the contract stands (Jon's listed-games contract, 8 Oct):** both listed CRITICALs are closed.
  trig-wars (#148, merged, main green) and gradient-hunter (#152; its entry below). The `cloud-remaining:` line is
  empty: **no game is claimed.** The session stopped at Jon's checkpoint without claiming the next game.
- **Next game: spot-the-muppet.** Start with a claim PR on main (canon 7.8.2, #145): check the open PRs and the home
  handover first, claim one game at a time, the fix PR takes it off the line.
- **The rest of the order, after spot-the-muppet:** word-problem-decoder, terrible-advice, probability-paradox,
  core-maths-paper2c, core-maths-paper2b, wrong-on-the-internet, 52dle, higher-power, prisoners-dilemma,
  seven-bridges, coordinate-geometry-dash, surd-simplifier, scale-factor-scaling, unit-converter, formula-forge;
  then boolean-blitz, matrix-crunch, complex-converter, eigenvalue-extractor, characteristic-quest.
- **Per game, as done for the first two:** claim PR; read its open register entries and the game; a verifier
  that fails on main naming the entries (group E has room: trig-wars ~45 s, gradient-hunter ~15 s); MaffsLock with
  its lock hint; a scoring change beyond the named fault, or new data, goes to Jon (gradient-hunter t2-003 did);
  `check-changed.py`; PR; fill the register's PR number; merge on green, 10 min clear of a home merge; watch main.
- **Earlier today (all merged, main green):** truth-buster #143; expectation-station #146 (Stage 1 one completion,
  40/40/40; ready to relist under SR-21).

## 2026-10-08 (cloud): gradient-hunter (listed-games contract, 2 of 23; the second CRITICAL); #148 merged

- **#148 (trig-wars) merged** 09:50 UTC; main's full run on b8691f8 green. Claim through main: #149 (merged 09:58).
- **t2-001 (CRITICAL):** MaffsLock locks the options at the first pick (the revealed correct option re-scored without
  limit). A wrong answer now waits for MaffsNext (canon 7.6; it moved on at once before); a right answer keeps its
  own Next, locked at the press; every question opens a fresh window on the game screen (the canvas included);
  `finishOnce`; Play Again opens the menu with `MaffsLock.screen` (the menu has the leaderboard link, as
  partial-fractions-duel's did). The KaTeX wait for the method reference is `// lock-ok:`.
- **t2-002:** the three stated tangents are the DRAWN curve's: a cardinal spline's slope at a plotted point is its
  neighbours' gradient, whatever the tension: 4.5 (was 5), 110 (was "a steeper gradient of 150"; the audit's 98.0 is
  the ideal exponential, not what is drawn, and 110 is LESS steep than the 116.7 chord) and 3.25 (was 4).
- **t2-003, filed and fixed (Jon's ruling, 8 Oct, option A):** a Calculate item scored a point for the gradient
  whatever the student did (the game showed it once the two points were clicked). Now the student types it after
  the two points: `MaffsAnswer.fractionOrDecimal` against the chord through the points clicked (`chordGradient`:
  exact rise/run; "to 2 decimal places" only when it recurs, so -9/80 is asked as -0.1125); that earns the point,
  clicking scores nothing, the working (rise / run) follows, the interpretation is unchanged. One question_answered
  per item, as before (the interpretation's). A text keyboard on phones (`inputmode="text"`: iOS's decimal pad has
  no minus): the shared MaffsKeypad is styled by theme.css, which this game has not migrated to, so it joins the
  todo 3.21 list (home lane: the keypad comes with its theme migration).
- **Verifier** `scripts/verify-gradient-hunter.py` (group E, ~9 s): chords from their points, stated tangents from the
  spline, one true interpretation (an "instantaneous/marginal ... is V" option is keyed right exactly when V is the
  tangent; a plain "is V" claims V to the hundredth, "about V" at V's places), every item played, the typed gradient
  on all 27 Calculate items, answer once and Next once (~15 s). Main's page fails t2-001 on six items, t2-002 on four
  claims and t2-003 on all 27; three plants caught.
  **Gotchas:** read numbers with thousands separators; a fall's interpretation gives its size; MaffsNext takes focus,
  so an Enter after a wrong pick advances (test the option with clicks, not the keyboard). **Never write a shared
  asset's file name (theme.css, keypad.js ...) in a game page, even in a comment:** `ci-deps.py --selftest` (b) reads
  a page that mentions it as one that loads it, and the PR's Plan job fails (#152's first run).
- **For the home lane:** gradient-hunter passes the lock check: add it to MIGRATED.
- **Next:** spot-the-muppet (the first of the audience order): claim PR first (not claimed: checkpoint stop).

## 2026-10-08 (cloud): trig-wars (listed-games contract, 1 of 23; first CRITICAL); #146 merged

- **#146 (expectation-station) merged** 08:56 UTC; main's full run green. **The claim went through main** (#147,
  merged 09:03): under #145 the home lane reads the line on main, so a listed game's claim is its own small PR.
- **Jon's ruling (8 Oct):** 2 PLAYER submits nothing (two people on one device; SR-22). VS CPU scores Player 1 only.
- **Fixed, all six entries (t2-001 CRITICAL, t2-002 HIGH, t2-003..006 MEDIUM):**
  - t2-001: hits and shots per side; VS CPU logs and scores Player 1's shots only, submitted win or lose;
    2 PLAYER logs both sides and submits nothing. Events carry `mode` (analytics rule for multi-mode games).
  - t2-002/005: the panel's Vx, Vy are V cos/sin in V's own units (no "u/s"; 0.28 stays internal).
  - t2-003: one physics (`newShell`/`stepShell`/`simulateShot`) for the flight, the advice and the check's aim; a hit
    is tested along each frame's segment before the ground. The old test missed 3.4% of true hits, half
    ground-first, half a fast shell crossing the circle between frames.
  - t2-004: the quip says only how it missed; `missAdvice()` suggests a change only if the physics says it lands
    at least 1px nearer (a 45-degree rule was wrong on 38% of misses: the hill; a 0-px gain was floating-point
    noise at the field's edge).
  - t2-006: four lines replaced (new wording in the PR for Project Claude).
- **MaffsLock:** FIRE locks per side (the slider rows are `data-maffs-lock-skip`, so a player can aim during the
  other turn); every timer through `MaffsLock.timer`; `finishOnce`; `shotId` stops a flight still animating after a
  reset. Lock hint: i = 0 fires `aimAtEnemy()` (a sure hit), i >= 1 fires 85 deg / 20 (a sure miss).
  `check-answer-lock.py --game trig-wars` passes (judged in full). Its note "no Next after a wrong answer" stands:
  after a miss the turn passes to the opponent (not in the register).
- **Verifier** `scripts/verify-trig-wars.py` (group E, ~45 s with the self-test): its own copy of the physics in
  Python; plays three battles, 252 panel settings, both kinds of missed hit, and near misses either side of 45 deg.
  Main's page fails on all six entries; three plants caught. **Harness gotchas:** run animation frames
  synchronously (a flight is ~150 chained frames; `setTimeout(0)` clamps to 4 ms); read the miss message by
  wrapping the page's `msg()` (the game clears it before a poll sees it); wrap `mfg` once per page.
- **Not changed:** the phone width (711px at load in CI's font, allowlisted, todo §3.9 batch 19).
- **For the home lane:** trig-wars passes the lock check: add it to MIGRATED.
- **Next:** gradient-hunter (the second CRITICAL): claim PR first.

## 2026-10-08 (cloud): expectation-station, Stage 1 one completion and 40/40/40 (Jon's bundle contract); #143 merged

- **#143 (truth-buster) merged** 08:10 UTC on a green Gate, after merging main (#144, contract DET, landed 07:58 while
  #143's CI ran: truth-buster's hint passes DET's lock check, seed 1, twice). #141 closed as superseded.
- **Claimed** in its own commit (58e19a0), off the line in this PR.
- **The bundle** (Project Claude, 7 Oct; Jon's ruling B), applied by script, verbatim: the 33 items get their sentence
  appended to the context and prepended to the explanation; 75 new items (core 021-040, gcse 016-040, alevel 011-040).
  Each level serves min(session length, bank), so 40 each.
- **Verifier:** `COUNTS` 40/40/40; the bundle's CARDS and FIGURES; `FIGURES_ADDED` (the 33 items' new opening claims);
  `CLUES` for all 120; **Stage 1 uniqueness**: every placement of the tiles into the missing cells is tried, and exactly
  one may sum to 1 and satisfy the CLUES entry, the keyed one. A CLUES ratio, difference or E(X) must also be in the
  context's own words (so a CLUES entry cannot claim what the student is not told). Fourth plant: es_core_001 without
  its sentence, CLUES ('none',): caught. Main's page fails 38 items on Stage 1, plus the counts. Runs in about 10 s.
- **Found by the uniqueness check, not in the bundle:** es_gcse_006, es_gcse_014, es_alevel_003, es_alevel_008 and
  es_alevel_010 have equal keyed values, so the bundle gave them ('none',), but a second pair of tiles also summed to
  the gap. **Jon's ruling (8 Oct, approved by Project Claude):** one stray tile changed on each (1/6 -> 1/8,
  0.35 -> 0.40, 0.3 -> 0.4, 0.30 -> 0.35, 0.25 -> 0.30). No new wording.
- **Added here, not in the bundle:** ten definition-only FIGURES entries ("Let P(X = a) = p and P(X = b) = q",
  es_alevel_021-030), like the existing "k + 2k + ... = 1" entries.
- **es_alevel_006** (approved by Project Claude, 8 Oct): its context said only "a batch of 4", so x = 1 and x = 4
  could swap (0.2916 and 0.0001 both fit the sum). It now ends "Each item is defective independently with probability
  0.1."; CONTEXT requires those words and the table to be exactly B(4, 0.1). Cards and explanation unchanged.
- **Phone:** the context is `.context-text` (textContent, no clamp); every one of the 120 measured unclipped at 390x844.
- **Register:** pc-001 fixed; no other entry open. **Ready to relist (SR-21, home lane): no CRITICAL or HIGH open.**
- **Ledger:** 40/40/40 made the three B4 (bank size) entries stale, which failed Tier 4 on the first CI run.
  `extract-banks.py --only <slug>` then `check-banks.py --only <slug> --write-ledger` cleared them (no other rule
  fired on the 75 new items). **Any bank change: run both before the first push** (`check-changed.py` does not run Tier 4).
- **Next:** Jon's listed-games contract (8 Oct): trig-wars first, then gradient-hunter.

## 2026-10-08 (cloud): truth-buster (queue 6 of 6, the last); the remaining list is empty

- **State found:** the previous session's closing note (partial-fractions-duel next) predated #139; #139 and the relist
  (#142) had merged and main's full run on a99efa5 was green. Only truth-buster was left.
  **Missed at the start: #141** (the previous session's truth-buster PR, the same cherry-pick) was already open. #143
  duplicated it; #143 was merged (its lock hint has no fixed wait, the cause contract DET names) with #141's fuller
  t3-016 (375x667 too), and #141 closed as superseded. **Check the open PRs, not only main and this file, at the start.**
- **truth-buster:** the old session's commit (fcc5e4c, `claude/keen-cray-ypsime-truth-buster`) cherry-picked onto main
  cleanly: MaffsLock in full (no `S.answered`; Next locks at its first press; the tier transition and the Next delay
  through MaffsLock.timer; finishOnce), and on a phone the answer buttons fold away during the reveal and the page moves
  Next above the footer. Added here: its maffs-lock-hint. **Two options: it presses the button that differs from the
  key, so every attempt is wrong.** Without it the generic driver came out all right on 8 draws in 1 run of 3 here
  (UNPLAYABLE), the fault contract DET names. Off the remaining list.
- **Proofs:** `verify-truth-buster.py` passes; against main's page it fails 62 times (the double Enter at the tier
  boundary, t3-013; Next under the fold at 390x844 on all 60 items). `check-answer-lock.py --game truth-buster` passes
  four times with the list empty (judged in full; 20 answered, 0 right, the same every run); `--selftest` passes.
- **Register:** t3-013 fixed. t3-015 stays open (the 21 Learn More video IDs: YouTube is refused here); its fold part is
  fixed at 390x844, and 320x568 is filed as **t3-016** (MEDIUM, open: 32 of 60 fit; the reveal is taller than the
  screen, so it needs shorter reveal text or a layout ruling; 375x667: 58 of 60). t3-014 (levels, class 4/5) stays open.
- **For the home lane:** truth-buster passes the lock check: add it to MIGRATED.
- **Next:** Jon's contract of 8 Oct (listed games' CRITICAL/HIGH, trig-wars first) runs after the **Expectation Station
  bundle contract**, whose text this session has not received.

## 2026-10-07 (cloud): partial-fractions-duel (queue 5 of 6); #138 binomial-blaster merged; NEXT = truth-buster

- **#138 merged** at 20:53 on a green Gate; main's full run on b10d3db green.
- **partial-fractions-duel:** the old session's commit (9a19235) cherry-picked onto main (Jon's alevel[22]:
  1/(x(x+1)(x-2)), find C, keyed 1/6; distractors -1/2 = A, 1/3 = B, -1/6 the sign slip; MaffsLock; the B3 duplicate
  cleared), plus its maffs-lock-hint (`{}`) and off the remaining list.
- **The two lock-check reports were one fault, in the game:** Play Again calls `showMenu()`, and at 1280x900 the menu's
  "Global leaderboard" link sits under the button, so the second click of a double click opened /leaderboards/.
  That page then threw "firebase is not defined" (the check blocks the Firebase CDN). `showMenu()` now calls
  `MaffsLock.screen()` on the menu (the shared API's own screen-change call; nothing shared edited). The verifier tests
  a real double click and Play Again then the link and Start; a fourth plant (the old showMenu) is caught.
  `check-answer-lock.py --game partial-fractions-duel` passes, twice. Filed as t5-011 (class 1), fixed.
- **For the home lane, two findings outside this lane:**
  - **The same Play Again shape is in 25 games** (`function showMenu(){show('menu')}` with a `/leaderboards/` link on
    the menu): angle-ace, bearing-blitz, binomial-blaster, characteristic-quest, circle-theorem-spotter,
    coordinate-geometry-dash, curling-friction, dimension-checker, eigenvalue-extractor, eigenvector-engine,
    force-resolver, formula-forge, formula-unlocked, graph-transformer, matrix-crunch, moments-master,
    normal-navigator, probability-paradox, proportion-blaster, scale-factor-scaling, sequence-solver,
    standard-form-blitz, surd-simplifier, trig-identity-duel, unit-converter. The check's Play Again test is a
    double click at one point, so it catches the fault only where a control happens to sit under the button
    (binomial-blaster and trig-identity-duel pass it with the same code). A layout-independent test (Play Again,
    then a click on every menu control within the window) would find all of them.
  - **/leaderboards/ throws when the Firebase SDK does not load** (a school network that blocks gstatic.com):
    `leaderboards/index.html:159` calls `firebase.database()` unguarded, so the whole script stops, including the
    device-local "Your Scores" section. firebase-leaderboard.js guards the same case (`typeof firebase`).

## 2026-10-07 (cloud): binomial-blaster (queue 4 of 6); #137 trig-identity-duel merged; NEXT = partial-fractions-duel

- **#137 merged** at 20:21 on a green Gate. Its first L1 run failed on fraction-equivalence, the second home-lane
  two-option game to do so (prime-or-composite on #134): the shared check's wrong-answer search is not deterministic
  for a two-option game. Passed on the one re-run; commented on #137 with the architectural fix (pick the wrong option
  from the game's data, or seed Math.random as tier 1's PHONE_SEED does). **For the home lane: it will keep failing
  PRs at random until fixed.**
- **binomial-blaster:** the old session's commit (67bf685) cherry-picked onto main, plus its maffs-lock-hint (`{}`), the
  method reference's KaTeX wait (:253) marked `// lock-ok:`, and off the remaining list. Jon's alevel2[36]:
  3/((1+x)(1-2x)) = A/(1+x) + B/(1-2x), find B, keyed 2 (distractors 1, -2, 3); the old item (1/((1+x)(1-x)), B = 1/2)
  was right but duplicated another (B3 ledger entry cleared, no register entry). MaffsLock in full.
- **Register:** t5-017 (class 1) fixed. t5-018 (class 4, shared level resolver) and t5-022 (wording) stay open.

## 2026-10-07 (cloud): trig-identity-duel (queue 3 of 6); #135 truth-will-set-you-free merged; NEXT = binomial-blaster

- **#135 merged** at 19:47 on a green Gate (main green on 571bb60; last home merge 18:44).
- **trig-identity-duel:** the old session's commit (03c34eb) cherry-picked onto main, plus its maffs-lock-hint (`{}`)
  and off the remaining list. Jon's gcse[16]: A = 45°, a = 10 cm, B = 60°, b = 12.2 (the old item, B = 30° keyed 7.1,
  was right but duplicated another question: the B3 ledger entry is cleared, no register entry). Hidden count-up
  (timer-policy, SR-23): no HUD timer, a right answer scores BASE whatever the time, time on the results only.
  MaffsLock in full.
- **Register:** t2-007 (class 1) and t2-010 fixed. Every other entry was already fixed by #102.
- **Not in its register, not fixed here:** a wrong answer still moves on by itself after 1 s (MaffsLock.timer), with
  no Next (canon 7.6). The lock check notes it ("no Next after a wrong answer"); it does not fail.

## 2026-10-07 (cloud): truth-will-set-you-free (queue 2 of 6); #134 eigenvector-engine merged; NEXT = trig-identity-duel

- **#134 merged** at 19:16 on a green Gate. Its first L1 run failed on prime-or-composite, a home-lane game the PR
  did not touch: `answer_wrong()` taps option (k+1) % 2 on 8 unseeded draws, and after a right answer `to_next()`
  waits a fixed 350 ms ('auto'), so a tap can land in the next question's 300 ms fresh window and be dropped. It
  passed 5 of 5 locally and on the one re-run. Commented on #134; the fix is the home lane's (shared check, or an
  `answer` in prime-or-composite's declaration). **For the home lane.**
- **Old branches:** this session's git proxy refuses any push but its own branch, deletes included, so the
  `claude/keen-cray-ypsime-<game>` branches cannot be deleted from here. Jon (or the old session) deletes them.
- **truth-will-set-you-free:** the old session's commit (7b07e09) cherry-picked onto main, plus:
  - [27], approved by Project Claude (7 Oct): "This expression can be written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B
    (XOR: one or the other, but not both). Play Boolean Blitz →", in KaTeX. XOR is introduced nowhere else in the
    game, so a form using it carries `identity` and `gloss`; the verifier checks the identity is true, the gloss, and
    the rendered line (a third plant, XOR with no definition, is caught).
  - Contract LH: its maffs-lock-hint (a wrong table, every cell the opposite of its key, then Submit; on the
    expression step the first option) and off the remaining list. `check-answer-lock.py --game` passes in full, twice.
    Its Next is replaced on each render (btnRow), so the hidden-button double advance eigenvector-engine had is absent.
- **Register:** t6-001, -002, -003, -005 fixed; t6-006 filed and fixed ([6]'s distractors A + B·C and (A + B)·(A + C)
  are equal by the distributive law; class 2, LOW); t6-004 (class 5, bank size) stays open.
- **Queue state (each prepared in a worktree, verifier passing on its branch and failing on main):**
  trig-identity-duel (`/home/user/tid-wt`, hint `{}` committed), binomial-blaster (`bb-wt`, hint `{}` and :253's KaTeX
  wait `// lock-ok:` committed), partial-fractions-duel (`pfd-wt`: needs a hint; the lock check here also reported
  "dblclick on Play again: its second click answered the first question" and "firebase is not defined", neither of
  which reproduces in a direct Chromium probe without the KaTeX shim: settle on CI, where it is judged in full),
  truth-buster (`tb-wt`: needs a hint with an `answer`; the generic driver finds no wrong answer; plus the MEDIUM
  320x568 entry, canon 7.6.1).

## 2026-10-07 (cloud): eigenvector-engine (queue 1 of 6); #130 Factor Theorem merged; NEXT = truth-will-set-you-free

- **#130 merged** at 18:22 on a green Gate (main green on b7e634b; last home merge 17:43). Main's run on d337b0b watched.
- **eigenvector-engine:** the old session's commit (3394734, from `claude/keen-cray-ypsime-eigenvector-engine`)
  cherry-picked onto main. It already adopts MaffsLock in full (newSession, lock, fresh, timer, finishOnce; no local
  flags), so the class-1 entry t6-002 closes. One addition here: `check-answer-lock.py` (on main since #129, after the
  commit was written) found a raw `setTimeout(buildExample, 300)` on load; it draws the start screen's worked example
  and marks nothing, so it carries `// lock-ok:`. Static rules pass.
- **Found here, fixed (class 1, part of t6-002):** `check-answer-lock.py --game eigenvector-engine --not-yet` (KaTeX
  served) reported "question_index jumped" on the old page every run. Instrumented: the worked solution's "Got it —
  next" was a plain onclick, only hidden after use, so a second Enter in the same frame (about 10 ms apart in the
  tap-through) ran closeSol() twice and skipped a question unseen. Now MaffsNext.wrong (canon 7.6; next-control.js
  loads before answer-lock.js), label kept. The verifier checks a real double click and two activations in one task
  (two Enters in one frame); a third plant (the old onclick) is caught. Python's separate key presses never land in
  one frame, so a keyboard test of this needs the in-page double activation.
- Verifier passes on the branch, fails on main's page (QS[22], [23], [24]); all three plants caught. The tap-through
  passes on the fixed page.
- **Register:** t6-001, -002, -004, -005, f0-001..007 fixed; t6-003 (class 5) stays open.
- **TWSYF is ready in `/home/user/tw-wt` (branch tw-local):** [27] uses Project Claude's approved wording (7 Oct):
  "This expression can be written (A ⊕ B)·C·D·Ē, where A ⊕ B = A·B̄ + Ā·B (XOR: one or the other, but not both). Play
  Boolean Blitz →", in KaTeX. XOR is introduced nowhere else in the game; the verifier checks the identity, the gloss
  and the rendered line, and a third plant (XOR with no definition) is caught.
- **Contract LH (#133, home lane, merged 18:44) landed while this was being prepared:** eigenvector-engine declares
  its maffs-lock-hint (`{}`: the generic driver plays it) and comes off the remaining list above, so CI now judges it
  in full. Each later game does the same in its own PR.
- **Delete each `claude/keen-cray-ypsime-<game>` branch once its game has merged (Jon).**

## 2026-10-07 (cloud): game 18 Factor Theorem (PR #130, merged); NEXT = merge #130, then the six queued games

- **New instance, fresh container (18:00 UTC).** The old worktrees and `/home/user/queue-patches/` were gone. Jon
  approved the old session pushing the six queued games to their own branches; this lane picks each up from its
  branch, one PR per game, under the usual merge rules. Do not rebuild them.
- **Jon's rulings (7 Oct, 18:00):**
  - **The lane question:** #130 does not edit `scripts/check-answer-lock.py`; the home lane moves cloud-lane games to
    MIGRATED. #130's MIGRATED and HINTS edits were dropped when main (#132) was merged in (the file is main's,
    byte for byte). The two in-game fixes stay: suvat loads answer-lock.js after next-control.js, and factor-theorem's
    resize debounce carries `// lock-ok:`. **The home lane will move per-game hints into each game's own file under a
    coming contract: build nothing around the central HINTS.** The two driving hints the old session wrote and
    passed with, as data for the home lane (suvat: Level 4, the equation is picked, then a wrong typed answer;
    factor-theorem: the Practice tab, a wrong answer in every box, Check pressed until the scaffold's three attempts
    are used):

```python
    # suvat (Level 4: pick the equation, then type the answer; question_answered fires on the typed answer).
    # The answer waits out MaffsLock's 300 ms window on the real clock before it presses CHECK.
    'suvat': {
        'level': 'level4',
        'ready': "document.getElementById('mainGame').classList.contains('visible')",
        'answer': ("return (async () => {"
                   "  const vis = id => { const e = document.getElementById(id); return e && e.offsetParent !== null; };"
                   "  const real = ms => new Promise(r => { const t = performance.now(); (function f() {"
                   "    if (performance.now() - t >= ms) r(); else requestAnimationFrame(f); })(); });"
                   "  for (let k = 0; k < 60; k++) {"
                   "    if (vis('phase2') && !document.getElementById('calcInput').disabled) {"
                   "      await real(350); document.getElementById('calcInput').value = '9999';"
                   "      document.querySelector('#phase2 .calc-btn').click(); return; }"
                   "    const b = [...document.querySelectorAll('#eqChoices .eq-btn')].find(e => !e.disabled && e.dataset.val === currentQ.equation);"
                   "    if (vis('phase1') && b) { await real(350); b.click(); }"
                   "    await real(60);"
                   "  }"
                   "})();"),
        'surface': '#phase2',
    },
    # factor-theorem: the Practice tab; a wrong answer in every box, Check pressed until the question is marked
    # (a scaffold has three attempts).
    'factor-theorem': {
        'start': "document.querySelector('[data-section=\"practice\"]').click()",
        'ready': "document.getElementById('sec-practice').classList.contains('active') && !!document.getElementById('checkBtn')",
        'answer': ("return (async () => {"
                   "  const real = ms => new Promise(r => { const t = performance.now(); (function f() {"
                   "    if (performance.now() - t >= ms) r(); else requestAnimationFrame(f); })(); });"
                   "  await real(350);"
                   "  for (let k = 0; k < 3; k++) {"
                   "    const c = document.getElementById('checkBtn');"
                   "    if (!c || c.style.display === 'none') return;"
                   "    document.querySelectorAll('#practice-area input.answer-input:not([disabled])').forEach(e => { e.value = 'zz'; });"
                   "    c.click();"
                   "  }"
                   "})();"),
        'surface': '#practice-area .q-card',
    },
```

  - **Factor Theorem scaffold:** keep "every value of the blanks that makes the line true" (Q6 also takes -2, -3).
  - **Truth Buster:** Next below the fold at 320x568 is filed as an open MEDIUM register entry citing canon 7.6.1;
    it does not block the fix PR.
  - **TWSYF [27]:** keep XOR only if the game introduces it before [27]; otherwise rewrite with AND/OR/NOT and list
    the wording in the PR for Project Claude.
- **The queue after #130, in order (one PR each; register entries to close):**
  1. eigenvector-engine: t6-001, -002, -004, -005, f0-001..007 fixed; t6-003 stays open.
  2. truth-will-set-you-free: t6-001, -002, -003, -005 fixed; file and fix t6-006 ([6]'s duplicate distractor);
     t6-004 stays open.
  3. trig-identity-duel: t2-007, t2-010.
  4. binomial-blaster: t5-017.
  5. partial-fractions-duel: t5-007.
  6. truth-buster: t3-013; file the 320x568 Next entry (above).
- **Each later game loads answer-lock.js:** under #131 it is reported, not failed. Run `check-answer-lock.py --game
  <slug>` (with KaTeX served) before each PR and give the home lane what it finds, in the PR and here.
- **Factor Theorem (unchanged from the PR):** typed answers looked up in ACCEPTED (canon 7.1 pattern, R12), written by
  `scripts/verify-factor-theorem.py --write` (E): one box per blank, matched by position; numbers via MaffsAnswer;
  algebra through canon(). Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5)). Q24/Q38/Q20 asks, Q22 hint,
  Learn ex. 4 candidates, test prompts' raw TeX (t5-019, new). MaffsLock. Open: t5-004/-005 (free text), -008/-009
  (exam-vocab.js), -013 (4), -014/-015 (design), -016/-017 (5), -018 (MaffsNext advance: check-teacher-invite's
  FT_STEP clicks only `.next-q-btn`, home lane).
- **Gotchas:** MaffsLock's 300 ms fresh window drops clicks a sweep makes right after a render: set
  `MaffsLock.FRESH_MS = 0` in sweeps and keep the real window in the lock test. A double click must be tested with
  `page.mouse` at the control (clicking a detached element twice fires its old listener). A fresh container has no
  KaTeX: fetch `registry.npmjs.org/katex/-/katex-0.16.9.tgz` (its `package/dist`). A `sitecustomize.py` on
  PYTHONPATH that adds a KaTeX route to every new context lets the teacher-line and answer-lock checks pass, but it
  makes every verifier that routes for itself (sync API: suvat, factor-theorem, check-resit-page) time out on `load`.
  Run those bare, with `--katex-dir` where the verifier has it.

## 2026-10-07 (cloud): game 17 SUVAT Selector (PR #128); #127 Force Resolver merged; NEXT = factor-theorem

- **Force Resolver (PR #127) merged** at 16:15 on a green Gate; main green after #126 before it.
- **SUVAT Selector:** every typed step marked by MaffsAnswer (`exact`, or `decimal` at the step's stated `dp`; the
  prompt says the precision; phase 0 to 2 d.p.); local parseFloat-and-tolerance gone (t5-006). Keys recomputed both
  ways: from the exact data, and from the values the student is shown (rounded chips, the previous step's key); a
  step's precision is the finest at which both round to the key (al[32] 1 d.p., al[18] 2 d.p., al[41]/[48] whole
  numbers, al[49] 1 d.p.; t5-007). Project Claude's sprinter (u = 8; t5-001) and ALEVEL[39] (2.02 s, 19.8 m/s;
  t5-003). v_y keyed -0.32 (t5-002); ALEVEL[22] says it lands at 3 s (t5-008); a question counts correct only if
  every typed step is (t5-009); wrong answers show the answer and wait for MaffsNext; ALEVEL[3]'s second root
  explained (t5-011). **MaffsLock (#125) adopted (Jon, 7 Oct 17:30):** lock first in every answer handler,
  fresh() on every render, MaffsLock.timer for every delay, endGame through finishOnce, newSession on Start;
  t5-004 closed. `scripts/verify-suvat.py` (E) adds the class-1 test (double click + Enter on CHECK mark once,
  two equation choices count once, one submit). Open: t5-005 (4), t5-010 (5).
- **Standing rule from Jon (7 Oct 17:30): MaffsLock is on main; every game fixed from now on adopts it and closes
  its class-1 entries in the same PR.** `check-answer-lock.py` (F1 part b) is not on main yet, so each verifier
  tests the lock itself.
- **Next: factor-theorem** (worktree `/home/user/ft-work`, branch claude/ft-prep, findings read, no edits):
  ACCEPTED-list typed answers (R12) and Project Claude's T4 (a = -19, b = 30; (x - 3)(x - 2)(x + 5) any order);
  t5-004/-005 (free text) and t5-008/-009 (exam-vocab.js, shared) stay open and get listed.

## 2026-10-07 (cloud): game 16 Force Resolver (PR #127); #126 Moments Master merged; NEXT = suvat

- **Moments Master (PR #126) merged** at 16:01 on a green Gate; main green after #124 before it.
- **Force Resolver:** `scripts/verify-force-resolver.py` (E), the Moments Master verifier's shape plus: options written
  as expressions evaluated (25 root 3 N, 10 tan 30 N) and a rounded figure counted equal to the expression it rounds
  from (43.3 N beside 25 root 3 N); figures quoted in text keys recomputed (FIGS) and their verdict required
  (VERDICT: "Yes", it slides). Project Claude's truss for level4[18] (12.8 kN) exactly. From the items' own data:
  level4[8] 1.40 m/s^2 (t5-002), alevel[47] 5 N (t5-004), alevel[32] "Yes" (t5-007), level4[7] worked with the
  stated 9.81 (1224 N; t5-011), alevel[31] "Equilibrium" (t5-012), alevel[35] g stated (t5-013); value-equal
  distractors replaced by named errors (t5-005, t5-006, f0-001, t5-014: 50 root 3, 1 N, "Undefined (tan 90)", 2.5 N,
  4.33 N, 266 N; for review); the given trig values stated where a key used them (alevel[11], level4[1]); 49.8 not
  49.7 (level4[15]). Wrong answers show the answer and working, then MaffsNext. Open: t5-008 (1), t5-009 (4),
  t5-010 (5).
- **Prepared locally, not pushed:** suvat (`/home/user/sv-work`, branch claude/sv-prep): typed steps on MaffsAnswer
  at a stated precision (the finest at which the exact data and the values shown both round to the key: al[32] 1 d.p.,
  al[18] 2 d.p., al[41]/[48] whole numbers), Project Claude's sprinter and ALEVEL[39], wrong answers wait for Next,
  a question correct only if every typed answer is; `scripts/verify-suvat.py` (E).

## 2026-10-07 (cloud): game 15 Moments Master (PR #126); #124 Linear Equation Solver merged; NEXT = Force Resolver

- **Linear Equation Solver (PR #124) merged** at 15:47 on a green Gate, after main's runs following #122 (re-run;
  the first attempt lost its Gate job in GitHub's 15:05-15:17 write errors) and #123 were green.
- **Moments Master:** `scripts/verify-moments-master.py` (E): every numeric key from the item's own data (SymPy;
  KEYS), distractors equal in value to the key (5 kW = 5000 W) or to each other, named-error REASONS for the items
  rewritten, numeric claims in keys and working lines, "Same beam" items quoting their predecessor, text keys pinned
  (REVIEWED, --print-pins); Chromium at 390 and 320: every option clicked, no raw TeX, no sideways scroll. Project
  Claude's data for :128, :134, :147, :172/:173 exactly; :141 rekeyed 75 N; :180's 5 kW replaced by 524 W
  (P = 2 pi N T / 60 with 100 taken as rpm; for review). Filed and fixed: t5-014 (premises: the trapdoor uniform,
  the level4 cable beam light with a vertical cable), t5-015 (R_B, T_A shown raw by textContent: ctx and ask now
  through MaffsText). Wrong answers show the answer and the item's working line, then MaffsNext (no stored
  explanations exist: fuller ones would be Project Claude content). Open: t5-009 (1), t5-010 (4), t5-011 (5),
  t5-012 (the gate premise: Jon).
- **Prepared locally, not pushed:** Force Resolver (`/home/user/fr-work`, branch claude/fr-prep). suvat is planned
  (typed answers onto MaffsAnswer with a stated precision per step; keys from the values the student is shown).

## 2026-10-07 (cloud): Linear Equation Solver, Jon's "optimal move" contract (PR #124); #115 Proof Builder merged; NEXT = moments-master

- **Proof Builder (PR #115) merged**; main's full run after it green (and after #117).
- **Jon's list (7 Oct, this session):** proof-builder (done), linear-equation-solver, then with Project Claude's
  replacement data moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, then
  truth-will-set-you-free; then (Jon, 15:27) follow-ups to merged games, one PR each: trig-identity-duel gcse[16]
  replaced + timer to hidden count-up; binomial-blaster alevel2[36] replaced; partial-fractions-duel alevel[22]
  replaced (each clears its B3 ledger entry); truth-buster Next visible at 390x844 on every item. The replacement
  data is in Jon's 7 Oct paste (the session's first message); if it is not to hand, ask Jon.
- **MaffsLock (`schools/assets/answer-lock.js`) is not on main yet:** class 1 stays open. Once it lands, adopt it in
  each game fixed (lock, fresh, timer, finishOnce) and close that game's class-1 entries.
- **Linear Equation Solver:** `scripts/gen-linear-moves.py` (depth-3 search, iterative deepening, under 1 s) writes
  MOVES between its own GENERATED markers: per line, every optimal move (one per distinct line), one slower move
  where one exists, named errors (one-side, carry, xonly, constnot) to fill four. Options show the move and the line
  it gives with the number side unevaluated (x = 12 - 7), so a one-side error can be shown and the answer phase
  still asks for the value. The trail follows the student's route (295 lines for 141 questions). Amber = 12.5 (half
  the 25 at stake), streak kept; amber and red wait for MaffsNext. Hints and feedback through MaffsText (t4-002).
  `gen-linear-equations.py` no longer writes the superseded per-step `opts`/`hint` (QUESTIONS otherwise identical)
  and uses a repo path. `scripts/verify-linear-equation-solver.py` (group E, ~40 s): its own TeX parser and search,
  SymPy for every value; every option clicked in Chromium; Jon's four cases tapped; page == generator. On main's
  file it fails on exactly r-001 (18 options in the 14 questions), r-002 (49) and t4-002 (11).
  - **Decision to review:** "fractions" in the tie-break means fractional constants, not coefficients (Jon's own x2
    example on x/2 + 5 = 11 needs x/2 = 6 to count as fraction-free). Under that reading every keyed move is
    optimal (STOP IF not triggered).
  - Four lines (-x = c in U1-U4) have 3 options: no fourth honest one exists.
  - Open: t4-003 (class 1).
  - **Gotcha (MOVES size):** the first version stored each option's feedback sentence (MOVES 280 KB, page 348 KB)
    and tier 4's extraction of this one game ran for minutes: the render-site evaluator calls `literal_to_json` on a
    literal every time it resolves an identifier (about 350 calls a second, no cache). Options are now compact arrays
    and the page words the feedback from their fields (MOVES 92 KB, page 159 KB, extraction 8.5 s). A large
    generated literal in any game will hit the same cost.
- **For the home lane:** content group B4 ran 243 s on main's run after #117, over canon's 4-minute cap; this
  verifier went in E (133 s on that run) instead. `bank_common.literal_to_json` is re-run per identifier
  resolution; memoising it by node would make large literals cheap (shared code). SR-13's scoring sentence
  ("scores full marks") needs a note for Jon's 7 Oct amber rule.

## 2026-10-07 (cloud): game 13 Proof Builder (PR #115); #112 Dimension Checker merged; NEXT = Linear Equation Solver (Jon's 7 Oct contract)

- **Dimension Checker (PR #112) merged** on a green Gate; main's full run after it green.
- **Proof Builder (PR #115):** `scripts/verify-proof-builder.py` (B4, declared by its own `# ci-line:` header; no workflow edit): refutation predicates for every counter-example option, SymPy induction stages, sorter orders, rendering at 390px. One renderer `M()` and 79 strings migrated to `\( \)` (132 B7 + 2 B11 ledger entries cleared). The options' TeX test is written as `includes()` at each call site, because tier 4 cannot decide a helper (`isTeX(v)`) and crashes on a regex `.test()` (game 8's note). Open: t5-014, t5-016 (1), t5-021 (5), t5-023 (per-mode boards: Jon), t5-024 in part (4).
- **Main went red once after #109** (13:16): group E, Like Terms Collector item 1, the same failure as on #106 and #88's first run (third time today). One re-run of the failed job was green. It does not reproduce here (0 of 24 runs, 8 at a time; this sandbox has Playwright 1.56 and no gstatic, CI has 1.63 and both). Home lane: the verifier hardening proposed on #106.
- **Original contract list done.** Everything left open is a shared class (1, 4, 5, B11), a decision for Jon (TID timer, Integration Duel + c, Proof Builder per-mode boards, Truth Buster fold), or needs new content (duplicate items in TID, BB and PFD; Truth Buster video IDs to check from home). Skipped until Project Claude supplies data: moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free.
- **Next: Linear Equation Solver** (Jon's contract of 7 Oct, added after Proof Builder): "What is the optimal move here?", every tied optimal move full marks, a valid but slower move amber (half, streak kept), wrong options named real errors; option sets generated by `scripts/gen-linear-moves.py` (depth-3 search) between GENERATED markers; the verifier re-derives every class with SymPy; the SR-13 note in canon.

## 2026-10-07 (cloud): game 12 Dimension Checker (PR #112); #109 Curling Friction merged; NEXT = Proof Builder

- **Curling Friction (PR #109) merged** on a green Gate; main's full run after it green.
- **Dimension Checker (PR #112):** `scripts/verify-dimension-checker.py` (B4, declared by its own `# ci-line:` header; no workflow edit): dimension algebra for keys, options and every worked step; MaffsOptions, MaffsNext. Open: t5-003 (1), t5-005 (5), t5-006 (4).
- **Next:** Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 11 Curling Friction (PR #109); #107 Integration Duel merged; NEXT = Dimension Checker

- **Integration Duel (PR #107) merged** on a green Gate; main's full run after it green.
- **Curling Friction (PR #109):** `scripts/verify-curling-friction.py` (B4): exact targets per item; no negative "speed"; friction only on sliding stones; MaffsNext. t5-008 filed and fixed. Open: t5-003 (1), t5-004 (4), t5-005 (5).
- **CI lines (Jon, 7 Oct):** from when contract V merges (home lane), a cloud-lane verifier declares its CI group
  with a `# ci-line:` header in the verifier file itself, and the PR does not edit `.github/workflows/check-site.yml`
  at all. Until then: one workflow line per PR, and rebase on main before merging.
- **Next:** Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 10 Integration Duel (PR #107); #106 Differentiation Duel merged; NEXT = Curling Friction

- **Differentiation Duel (PR #106) merged** on a green Gate; main's full run after it green.
- **Integration Duel (PR #107):** `scripts/verify-integration-duel.py` (B4): antiderivatives checked by differentiating, c held as a symbol, ln x + c sampled where it is right. Missing + c named in feedback (Jon may rule it right). B11 (5) cleared. Open: t5-010 in part (class 4).
- **Like Terms Collector's verifier flaked once on #106** (group E; item 1 typed 8.9/6.5, `MARK()` null, empty feedback;
  it passed 5 of 5 locally and on the one re-run). Same item and shape as #88's first-run flake. Home lane: after
  `page.fill`, wait for the boxes to read the typed values and for the feedback panel's class before reading the mark.
- **#103 split content group B into B1-B4**; the cloud lane's verifiers go at the end of B4, where #103 put them.
  A branch prepared before a ledger change on main conflicts on `data/check-ledger.json`: take main's ledger and
  replace only that game's record (the scratch helper did this per commit).
- **Next:** Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 9 Differentiation Duel (PR #106); #105 Partial Fractions Duel merged; NEXT = Integration Duel

- **Partial Fractions Duel (PR #105) merged** on a green Gate; main's full run after it green.
- **Differentiation Duel (PR #106):** `scripts/verify-differentiation-duel.py` (B4): implicit items compared on the curve; explanations must state the answer. B11 (9, five of them added by #99) and B7 (1) ledger entries cleared; t5-013/014 filed and fixed. Open: t5-010, t5-011 (class 4).
- **Next:** Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 8 Partial Fractions Duel (PR #105); #104 Binomial Blaster merged; NEXT = Differentiation Duel

- **Binomial Blaster (PR #104) merged** on a green Gate; main's full run after it green.
- **Partial Fractions Duel (PR #105):** `scripts/verify-partial-fractions-duel.py` (B4): every Find solved from its stated form; valid equivalent forms removed. Open: t5-007 (class 1), t5-009 (class 4). New B3 ledger entry: the Find B / Find C pair for 1/(x(x+1)(x-1)) now share stem, options and key (needs a new item).
- **The tier 4 crash recorded under game 6 has a known cause (home lane: shared code).** `_SiteEval.regex()` in
  `bank_common.py` returns `(pattern, glob)`, and the `.test` branch of `_SiteEval.call()` calls `.search` on that
  tuple, so any `/re/.test(x)` the evaluator reaches raises. Taking the pattern from the tuple fixes it. Also: a
  guard written as a page helper (`isTeX(v)`) is never decided, so both branches count; until the evaluator can
  look inside, the cloud lane writes such guards as `includes()` at the call site.
- **Next:** Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 7 Binomial Blaster (PR #104); #102 Trig Identity Duel merged; NEXT = Partial Fractions Duel

- **Trig Identity Duel (PR #102) merged** on a green Gate; main's full run after it green.
- **Binomial Blaster (PR #104):** `scripts/verify-binomial-blaster.py` (B4): three-term estimates as the ask states, rounding-ambiguity check, MaffsOptions. Open: t5-017 (class 1), t5-018 (class 4), t5-022 in part (portal card: home lane). One B3 duplicate (needs a new item).
- **Next:** Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 6 Trig Identity Duel (PR #102); #101 Component Crusher merged; NEXT = Binomial Blaster

- **Component Crusher (PR #101) merged** on a green Gate; main's full run after it green.
- **Trig Identity Duel (PR #102):** `scripts/verify-trig-identity-duel.py` (B2): every option read into SymPy. Compound-angle keys, 85.9°, identical options fixed; t2-011 filed and fixed. Open: t2-007 (class 1), t2-010 (timer: Jon's decision). gcse[16] duplicates gcse[12] (B3; needs a new item).
- **For the home lane (shared code, not edited here):** `bank_common.py`'s render-site analysis crashes
  (`AttributeError: 'tuple' object has no attribute 'search'`, in `call`) on a regex literal's `.test()` in some
  positions: inside a template-literal expression (Component Crusher's first CI run) and `/[\\^_{}]/.test(...)`
  (Proof Builder, found locally). Extraction then fails and every ledger entry reads as stale. The cloud lane works
  round it in each game (a named function, or string methods); the parser fix is the home lane's.
- **Local tier 4 in the cloud sandbox works:** serve KaTeX from the npm tarball (route the jsdelivr KaTeX URLs to
  `package/dist`), run `extract-banks.py`, then `check-banks.py --ci`; about 95 s with 4 workers.
- **Next:** Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 5 Component Crusher (PR #101); #100 Expectation Station merged; NEXT = Trig Identity Duel

- **Expectation Station (PR #100) merged** on a green Gate; main's full run after it green.
- **Component Crusher (PR #101):** `scripts/verify-component-crusher.py` (B2): keys from what is shown, diagrams measured from the canvas, marking through MaffsAnswer. Level 4 data shown; prompts' maths in `\( \)` (31 B7 ledger entries cleared). Open: t4-005 (class 1), t4-011 (class 5), t4-014 in part (class 4).
- **Next:** Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 4 Expectation Station (PR #100); #98 Trig Worms merged; NEXT = Component Crusher

- **Trig Worms (PR #98) merged** on a green Gate; main's full run after it green.
- **Expectation Station (PR #100):** `scripts/verify-expectation-station.py` (B1): all 180 Stage 3 cards reviewed with checks from the distribution ("most" = more than half); Stage 1 marked exactly. t2-001..016 fixed, t2-018/019 filed and fixed; open: t2-017 (class 1).
- **Next:** Component Crusher, Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 3 Trig Worms (PR #98); #97 Truth Buster merged; NEXT = Expectation Station

- **Truth Buster (PR #97) merged** on a green Gate; main's full run after it green.
- **Trig Worms (PR #98):** `scripts/verify-trig-worms.py` (group B2, ~20 s). The generator is rebuilt from a
  `POOL` of servable outcomes (1,204; no retry); every outcome is recomputed with mpmath from the values shown,
  at the stated precision ("to the nearest degree", "to 1 decimal place"); every distractor is a named error and
  the feedback names it; only the two given sides are labelled and the triangle is drawn at one scale.
  t1-001..t1-004 fixed; nothing left open.
- **Next:** Expectation Station, then component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker,
  proof-builder (all prepared on local worktrees /home/user/*-work, not pushed; their PR texts and register
  specs are in this session's scratchpad).

## 2026-10-07 (cloud): game 2 Truth Buster (PR #97); #96 Spot the Error merged; NEXT = Trig Worms

- **Spot the Error (PR #96) merged** on a green Gate; main's full run after it green.
- **Truth Buster (PR #97):** `scripts/verify-truth-buster.py` (group B1). Keys are reviewed judgements, with the
  words a statement must contain for its key to hold (`needs`, SR-18) and SymPy where a key can be computed;
  every reveal figure is in `FIGURES` (an unlisted `=`, `<`, `>` fails); dates and counts in `SOURCED`.
  t3-001..012 fixed. Open: t3-013 (class 1), t3-014 (class 5/4), t3-015 in part: the 21 Learn More video IDs
  (YouTube is refused from the cloud sandbox: check them from home) and Next below the fold (shorter reveal
  text, Project Claude, or a layout ruling).
- **Next:** Trig Worms, then expectation-station, component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker (all
  prepared on local worktrees /home/user/*-work, not pushed), then proof-builder (in progress). A lost container
  loses them: redo from the register.
- **Gotchas:** a PR that clears a fixed B7/B11 finding also clears its entry in `data/check-ledger.json` (dump
  with `indent=1, ensure_ascii=False, sort_keys=True`, as `check-banks.py` does), or CI fails it as stale. With a
  workflow edit, `check-changed.py` selects every check (about 45 minutes here): run it in the background with a
  long timeout, never the default 30 minutes (the Truth Buster run was cut off there).

## 2026-10-07 (cloud): unlisted-games contract, game 1 Spot the Error (PR #96); NEXT = Truth Buster

Jon's contract of 7 Oct (cloud lane): fix the unlisted games one per PR, each under a new verifier, in this order:
spot-the-error, truth-buster, trig-worms, expectation-station, component-crusher, trig-identity-duel,
binomial-blaster, partial-fractions-duel, differentiation-duel, integration-duel, curling-friction,
dimension-checker, proof-builder. Shared classes stay open: 1 (answer lock, F1), 4 (?level resolver, F2),
5 (bank size), B11 parser gaps (F0). Skipped until Project Claude supplies data: moments-master, force-resolver,
suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free. Other owners: linear-equation-solver,
screening-room, glorious-gantt.

- **Spot the Error (PR #96):** `scripts/verify-spot-the-error.py` (group B2, ~9 s). All 19 register entries
  fixed (t1-001..014 plus the re-audit's t1-015..019); nothing left open. 16 items reworded (listed in the PR
  for Project Claude). Model: the key is the first step that departs from correct working; later steps carry it.
- **Prepared on local branches, not pushed** (worktrees under /home/user/*-work, gone with this container): the
  next games are rebuilt from their audit entries in the same order. If this container is lost, redo from the
  register; the PR descriptions list the content choices.
- **Gotchas:**
  - A reviewed verdict (a step judged an error, a statement judged true) reads no text, so each verifier that
    holds verdicts pins each item's content hash (`REVIEWED`, `--print-pins`): any edit fails until re-reviewed.
  - The self-tests count a plant as caught only by a check other than that pin.
  - Locally, the KaTeX CDN is refused: KaTeX games' verifiers take `--katex-dir` (the npm tarball's dist/).
    `check-changed.py` here always fails seven checks for environment reasons (PR #96 lists them).
  - `extract-banks.py` through the sandbox wrapper reports component-crusher's 34 B7 entries stale even on main:
    do not trust a local tier 4 run for B7; read CI's.
  - A shared TeX-to-SymPy reader would serve several of these verifiers (each carries its own small one, since
    the cloud lane does not add shared modules): a home-lane candidate.

## 2026-10-07: the lane starts (written by the home lane, which set up the lanes)

- No cloud session has run since the lanes were split. The last cloud work was 6 Oct 2026 (#85 audit tranches 1-2
  and two games unlisted; #86 Core Maths Paper 1), recorded in CLAUDE.md's history.
- The unlisted games and their open findings: `docs/audits/REGISTER.md` ("By game", Listed = unlisted) and the
  roster's Unlisted section. Each has its relist checklist in `docs/todo.md` §1.53-§1.75.
- **Next:** Jon's first cloud-lane contract names the game.
