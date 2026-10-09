# Handover: home lane

**MAIN GREEN (for the cloud lane: #223 may merge):** main's full run on 5cea89b (#224) passed every job, run
37969653160, and its timings job recorded and repacked (760ef9a). Main had been red since #220 (CI-BALANCE) on its
main-only "CI timings and pack" job alone: the job-log API refused the workflow's token; #224 reads the timings from
artifacts instead. Every content group is now at most 69% of its budget. Main green again after #218 (18f5da8, run 37970610295).

**HOME LANE, 9 OCT EVENING (Jon's 16:10 queue, reordered 18:00 and 19:00): IN PROGRESS.** Done: RULINGS-9OCT (#215),
CI-BALANCE (#220, then #222 and #224 to fix its timings job; merged ahead of #218 because #218's L1 went over
budget), GRAPH-SKETCHER-FIT (#218, with the answer lock in six parts). HOOK-FIX (#221), OVERLAY-KEYS (#232).
PLAY-AGAIN-SCREEN (#234 + batch 2). Next: SCORES-OFFLINE, SCI-CALC, DOCS-9OCT, checkpoint, PREPUSH-SCOPE,
LIBRARY-DRAFT. **CAR-TRAP-DRAFT moved to the CLOUD LANE (Jon, 20:17); the home lane does not start it.** Its
contract is on main, verbatim: `docs/handover/contracts/2026-10-09-car-trap-draft.md` (committed dc43926, merged in
#221). LIBRARY-DRAFT (Jon, 19:35; new ★ room, Mrs Barb Phile's library) starts after The Rightful King and Car
Trap drafts; its contract is saved verbatim under contracts/ when it starts.

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**OVERNIGHT RUN (Project Claude for Jon, 8 Oct 2026, 23:45): DONE.** Contract verbatim in
`docs/history/contracts/2026-10-08-overnight.md`. Every item merged (see the summary above and the entries below).
main's run on #200 (2782d17) went red on a runner network flake (the DejaVu font fetch: curl 503s and 60 s
timeouts pushed B4 and L4 past their budgets; tier 1 timed out loading spot-the-muppet, untouched); one rerun of the
failed jobs passed (run 37875059753, attempt 2).

**Contracts (canon §7.8.2, contract CONTRACTS-FOLDER):** each is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md`; the queue below holds a one-line pointer; the file moves to
`docs/history/contracts/` when the work merges. Read a contract when its item starts, never at session start.

**QUEUE (home lane, Jon 9 Oct 16:10):** 1 RULINGS-9OCT (#215, merged), 2 GRAPH-SKETCHER-FIT, 3 CI-BALANCE, 4 PLAY-AGAIN-SCREEN,
5 SCORES-OFFLINE, 6 SCI-CALC, 7 DOCS-9OCT, then CHECKPOINT. (E2 merged as #213; main green.)
CAR-TRAP-DRAFT: the cloud lane's (Jon, 20:17); contract at
`docs/handover/contracts/2026-10-09-car-trap-draft.md` on main (HOOK-FIX let it through the hook). Jon also sent the
IT room rewrite brief (Narry, secret ballot; 3 open rulings): a brief, not yet a contract, saved as
contracts/2026-10-09-it-room-brief.md. SCI-CALC (item 6) is saved as contracts/2026-10-09-sci-calc.md.
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item: done for every listed game but graph-sketcher** (NOT_YET: glorious-gantt, unlisted and the cloud
  lane's; graph-sketcher, blocked by its phone overflow, batch 10 entry). unit-converter loads the lock (cloud lane,
  #196) and is judged in full, but is not in MIGRATED: Jon's call (the overnight contract left it to the cloud lane). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
  `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
  line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

**Jon's rulings, 9 Oct (on the overnight questions; RULINGS-9OCT):** unit-converter moves to MIGRATED (done,
seeds 1-3 pass). wrong-on-the-internet keeps its 3 s pause before Try again: feedback on a wrong answer is shown, not
skipped (Jon, 8 Oct). complex-converter's Play Again keeps replaying the mode, as its Menu is one tap from the end
screen. graph-sketcher: fix its phone overflow now, then put it on the lock (item 2). The first two are in canon §7.6.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-09 (home): PLAY-AGAIN-SCREEN batch 2 (item 4 done but for characteristic-quest)

- **The 21 games batch 1 left on `SCREEN_NOT_YET` now change every screen through `MaffsLock.screen()`:**
  - their own screen helper ends with it: better-value, expectation-station, fermi-lab, formula-plug-in,
    like-terms-collector, new-shapes, probability-pioneer, think-of-a-number (`showScreen(id)`); equation-builder,
    spot-the-error (`showScreen(name)`: the active screen); simultaneous-solver (`showS`);
  - no helper: each line that makes a `...Screen` active is followed by `MaffsLock.screen(<it>)`: component-crusher,
    four-quadrant-explorer, given-that, growth-and-decay, split-it, stat-attack, test-the-claim, truth-buster,
    wrong-on-the-internet;
  - prime-or-composite: `showModal()` opens the window on the modal, `closeModal()` (its Play Again) on `.page`,
    where its Start button sits;
  - six games reveal a header with "← Back to Games" outside the screens when a run starts (truth-buster,
    think-of-a-number, four-quadrant-explorer, like-terms-collector, probability-pioneer, given-that): that line now
    also calls `MaffsLock.fresh(gameHeader)`.
- `SCREEN_NOT_YET` is down to characteristic-quest (the cloud lane's; it comes off when the claim ends). All 21 pass
  check-answer-lock.py locally (seed 1).

## 2026-10-09 (home): PLAY-AGAIN-SCREEN (item 4)

- **Every listed game's screen change goes through `MaffsLock.screen()`**: 33 pages' `show(id)` / `showScreen(id)`
  now end with `MaffsLock.screen(<the screen shown>)` (27 shared one exact one-liner; the rest small variants).
  So Play Again, back to menu, mode select and results all open the 300 ms fresh window on the new screen; a
  double-click's second click lands on nothing. characteristic-quest is cloud-claimed (`cloud-remaining:`): left
  for a later batch. constructions-lab (a compass tool, not on the lock) also loads answer-lock.js now, for
  `screen()`; it is not played by the lock check (it records no question_answered).
- **Check (`check-answer-lock.py`, every migrated game, its existing Play again double-click):** before the first
  click it records the visible controls; after it, every newly visible control must sit in an open fresh window,
  whatever the layout, and the control under the pointer too; the second click must leave the URL unchanged. The
  fresh window is stretched to 5 s for the probe, so no verdict depends on runner speed (canon 7.6.0, DET).
  **Against main's pages 25 of the 32 fail** (angle-ace, bearing-blitz, binomial-blaster, coordinate-geometry-dash,
  curling-friction, dimension-checker, eigenvalue-extractor, eigenvector-engine, force-resolver, formula-forge, formula-unlocked,
  graph-transformer, higher-power, just-pythag-it-bruv, linear-equation-solver, matrix-crunch, moments-master,
  normal-navigator, proof-builder, proportion-blaster, scale-factor-scaling, sequence-solver, standard-form-blitz,
  surd-simplifier, trig-identity-duel; typically the menu's level buttons and its "Global leaderboard" link open
  to the second click); the other 7 go from Play again straight into a new game whose question is already fresh.
  With the change all 32 pass. Self-test plant: angle-ace with a bare `show()`: caught.
- **Batch 2 (next PR): 21 more games** the stricter check found on CI, whose Play again changes screen through their
  own code (showScreen, showMenu toggling classes, or none): better-value, component-crusher, equation-builder,
  expectation-station, fermi-lab, formula-plug-in, four-quadrant-explorer, given-that, growth-and-decay,
  like-terms-collector, new-shapes, prime-or-composite, probability-pioneer, simultaneous-solver, split-it,
  spot-the-error, stat-attack, test-the-claim, think-of-a-number, truth-buster, wrong-on-the-internet (plus
  characteristic-quest, cloud-claimed). They are on `SCREEN_NOT_YET` in check-answer-lock.py: reported, not failed;
  a listed game that passes fails, so the list only shrinks. Batch 2 empties it.
- **Two drivers clicked inside the new fresh windows** (a student's click comes after them): check-teacher-invite.py
  moved while the menu's fresh window was open: PD_UNLOCK's opponent counter advanced on clicks the page dropped,
  so it kept landing on the same opponent and never won the three games that unlock the tournament; verify-partial-fractions-duel.py double-clicked Play again the moment its results screen appeared. Both
  now wait for `MaffsLock.isFresh()` to clear (check-teacher-invite.py before every move and click), as canon 7.6.0 (DET) asks of drivers. partial-fractions-duel's own
  extra `MaffsLock.screen` in showMenu went (show() does it); its verifier's plant now strips it from show().
- **Canon §7.6.0:** "every screen change goes through MaffsLock.screen()".

## 2026-10-09 (home): OVERLAY-KEYS (19:00 addendum; for the cloud lane: re-check item 12)

- **The overlay is shared:** `askInitials()` in `schools/assets/firebase-leaderboard.js`, loaded by all 97 games; no
  game has its own copy. Key listeners at page level: 11 games, all `keydown` on document or window in the bubbling
  phase; none in capture, no `onkeydown` properties (10 more games listen on their own elements only).
- **Games whose shortcuts fired while initials were typed (main's overlay, every key reached the game):** 52dle,
  decimal-detective, equatle, formula-plug-in, negative-number-line, new-shapes, prime-or-composite,
  prisoners-dilemma, six-sevens-bruv, think-of-a-number, trig-wars.
- **Fix (in the overlay only, no game touched):** (1) the overlay stops keydown/keypress/keyup bubbling out of it,
  after its inputs' own handlers (Enter still submits, Backspace still steps back); bubbling is enough because no
  game listens in capture. (2) While it is open, a window capture-phase guard stops keys aimed outside it (focus left
  on the page by a tap on the backdrop), and it stays up through the keyup of a key held when it closes, so the
  Enter that submits never reaches the game. It then removes itself (1 s fallback).
- **Check:** `scripts/test-initials-overlay.py` (content tier, ci-deps on the overlay): every one of the 97 games,
  48 keys typed (a-z, 0-9, space, arrows, Escape, punctuation) + 6 on the backdrop + Enter; asserts no game key
  listener and no probe (its own document/window keydown, so it bites in games without shortcuts) saw a key, the page
  did not navigate, submitScore resolved with ABC saved, and the next key after the overlay reaches the page.
  Against main's overlay all 97 FAIL (`--against`); with the fix all 97 pass; the plant (containment removed) is
  caught in all 11 shortcut games. ~33 s locally.
- **prisoners-dilemma:** passes with no change to its own code; the cloud lane can re-check item 12.
- **Escape:** the contract says "Escape closes the overlay as now", but the overlay has never handled Escape (it
  does nothing; Skip is the way out). Not added: Jon's call. Escape no longer reaches the game either.
- Offline, submitScore writes nothing after the overlay (not the production host, by design), so "submitted" is
  checked at the overlay's edge.

## 2026-10-09 (home): HOOK-FIX (Jon, 18:00) and the Car Trap contract

- **The block:** the local pre-commit guard (`.git/hooks/pre-commit`, a copy of `~/.maffsgames-local/pre-commit`;
  patterns in `~/.maffsgames-local/personal-patterns.txt`, also read by `scan-personal.sh`; no other repo uses it;
  not gitleaks, not CI) has no bare relationship words. Its one relationship pattern was
  "possessive + relation word", with three possessives: Jon's name, "his" and "my". "his daughter" in the draft
  (fiction) matched it.
- **Ruling (Jon, 9 Oct):** "the word daughter should not be blocked, that's taking the rule too far"; name-only
  chosen. The pattern now matches only "<Jon's name>'s <relation>". "his/my <relation>" in prose or room dialogue
  commits.
- **What it matches now (16 patterns, by category):** 1 email/phone pattern; 14 standalone words or short phrases for
  real names, places and identifiers (unchanged); 1 "Jon's name + relation word" combination. The hook's allowlist
  for the project's own addresses is unchanged. Backup of the old list: `personal-patterns.txt.bak-2026-10-09`
  (local only).
- **Self-test:** `~/.maffsgames-local/test-pre-commit.sh` runs the real hook in a throwaway repo. "his daughter's
  first car" passes; a "<name>'s daughter" fixture and a standalone-pattern fixture, both built at test time from
  the list, are blocked. It passes on the new list and fails the fiction case on the old one.
- **Gap to know about:** an unnamed "his daughter" about Jon's own family is no longer caught; only the named form
  and the other patterns are.
- **The HOOK-FIX contract** (`docs/handover/contracts/2026-10-09-hook-fix.md`, verbatim) has one line that matches a
  standalone real-detail pattern by coincidence (an everyday word). Jon ruled: allow that exact line
  (`allowed-lines.txt`); the pattern is unchanged.
- **The Car Trap contract is in the repo:** `docs/handover/contracts/2026-10-09-car-trap-draft.md`, verbatim
  (committed through the hook, no bypass). It is queued after the checkpoint, as before.

## 2026-10-09 (home): GRAPH-SKETCHER-FIT (item 2, #218)

- **Overflow, measured at 320x568, 390x844, 412x915 on all 45 scenarios** (main: every one overflowed, the page
  growing ~9px per scenario loaded, up to 881px). Causes, all in the page (CLASS CHECK: local; the same
  `Math.max(320, ...)` canvas floor appears only in glorious-gantt, unlisted and the cloud lane's: not touched):
  `getCanvasCtx` sized the canvas to the panel's width less 12px, but the panel's padding and border are ~21px, so
  the canvas pushed its grid track wider on every draw, with a 320px floor; and the tracks were `fr` (min-width
  auto), so the value table widened its column instead of scrolling in `.table-box`. Fixed: `minmax(0,..)` tracks;
  the canvas takes the panel's content box. After: no overflow at any size for any scenario, in the table, draw,
  question and results phases; the table scrolls in its own box. `tier1_phone_overflow` entry removed.
- **Touch drawing at 390x844:** canvas 336x225 CSS px; eleven real touch taps placed eleven control points on the
  curve, Check Curve passed into the questions (screenshot checked). Next is tappable: the check's 390px double-tap
  phase passes.
- **On MaffsLock** (declaration: the answer completes the table, draws the true curve at Core, then answers the
  question on screen); seeds 1-3 pass; **NOT_YET: glorious-gantt only.** verify-graph-sketcher.py passes.
- **Faults fixed beyond the swap:**
  - CM15 (Core, the Ferris wheel) gives every table value, so there was no cell to fill, and the table only
    completed from a cell's change: the scenario never moved on, and a Core run (6 of 15 scenarios) drew it about
    40% of the time, so the game could not be finished. Its table now completes as it loads. Scenario data untouched.
  - Check Curve: a double-click on a passing curve scored it twice (+20 then +10) and restarted the questions. One
    check per attempt now (the draw tools lock; a failed check reopens them).
  - Every question's answer went on by a timer, right or wrong (1-2 s): a wrong one now waits on MaffsNext under its
    feedback (canon 7.6). Next Scenario acts once; the end runs once (finishOnce).
- **Answer lock split into six parts** (contract CI-BALANCE: lock parts grow by hand). L1 ran 6m40s on this PR's
  first run (6m budget then); `ci-groups.py --check` passes with part 6 counted at the 300 s default until main
  records it.
- Seen, not touched: on a phone the table's typed values are clipped by the cell width (608.3 of 608.33 shows);
  the table scrolls, the value is kept. Checking a curve with fewer than three points uses `alert()`.

