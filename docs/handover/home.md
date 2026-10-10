# Handover: home lane

**ART-PENDING (10 Oct, Jon's contract 08:50, ahead of the queue for cloud PR #242; contract
`docs/handover/contracts/2026-10-10-art-pending.md`).** Rule: **no `art` field, no request.** engine.js
(`HAS_ART = !!R.art`) emits no scene, fail-thumbnail or end-card picture for a room with no top-level `art:`;
a room with art is unchanged, data-fallback included. teacher.js mentions the mid-game failure picture only when
the room has art. check-escape-rooms.py lists a room with no `art` as "art pending" (it crashed on one before);
a named picture that is missing is listed as before, and check-site's tier 1 fails its 404. New
`scripts/test-escape-art.py` (15 s): all 8 live rooms to a win and a loss, their pictures load as before; the
fixture (canteen-hack with `art` removed, by routing) makes no /docs/art/ request through the brief, its
misconception, the win and the loss; the old always-request engine is planted and caught. STOP IFs clear: every
live room has all three files, so none uses the 404 path for its data-fallback; no saved field changes (SAVE_V 1).
Recorded in CLAUDE.md and voice-rewrite §6. **For the cloud lane (#242):** drop `art` from car-trap's room.js
(and leave the hub card's `<img>` out of `escape-rooms/index.html` until the art lands), then re-run.

**DASHBOARD-CHARTS (10 Oct, Jon's contract 08:35; `docs/handover/contracts/2026-10-10-dashboard-charts.md`).**
`docs/apps-script-endpoint.js` only, SCRIPT_VERSION `2026-10-10-a`: the three percentage columns are written as
fractions with the cell format `0%` (they show as before), the Accuracy chart's axis runs 0 to 1 as percent;
`rowBelowChart()` moves the row counter below each chart (a 21 px default row), so no chart overlaps the next
section; one filter, `isMarked()`, keeps rows with a blank `correct` out of Accuracy by Game and Hardest Questions.
STOP IFs clear: prisoners-dilemma sends `correct: null` (written blank by `cellValue`), and every other
`question_answered` call in games/ sends a boolean. The daily email is untouched (its own hardest-questions list still
counts prisoners-dilemma: the contract left the email alone). **Jon must redeploy; the repo copy does not deploy
itself** (runbook `docs/apps-script-redeploy.md`): paste the file into the Apps Script editor and set `REPORT_EMAIL`
to your address before saving; Deploy, Manage deployments, edit (pencil) the existing deployment, Version: New
version, Deploy; select `testDashboard` in the function menu and Run (it rebuilds the dashboard from the sheet;
`rebuildDashboard` itself needs arguments), or wait for the 07:00 run; open the `/exec` URL and check `version` reads
`2026-10-10-a`.

**MAIN GREEN (for the cloud lane: #223 may merge):** main's full run on 5cea89b (#224) passed every job, run
37969653160, and its timings job recorded and repacked (760ef9a). Main had been red since #220 (CI-BALANCE) on its
main-only "CI timings and pack" job alone: the job-log API refused the workflow's token; #224 reads the timings from
artifacts instead. Every content group is now at most 69% of its budget. Main green again after #218 (18f5da8, run 37970610295).

**CHECKPOINT (Jon asked, 9 Oct late).** Main green at cfe0861. Merged tonight: #215, #220/#222/#224 (CI-BALANCE),
#218, #221 (HOOK-FIX), #232 (OVERLAY-KEYS), #233, #234/#237 (PLAY-AGAIN-SCREEN), #238 (SCORES-OFFLINE).
**#239 SCI-CALC merged after the checkpoint (9f51dc7, Jon: "merge in whatever order makes the most sense"); its
contract moved to `docs/history/contracts/`. This handover (#240) merged after it.** **DOCS-9OCT: started, nothing
applied**: its two STOP IFs are clear (factor-theorem has no open CRITICAL or HIGH;
timer-policy.md still lists Unit Converter under the silent timer). The relist is scripted from the unlisting
commit e419439 (roster #88 A-Level only, both portal cards, sitemap, hub row + NOT_ON_HUB, spec-map B6 rows, canon
96, todo 1.62), kept at `~/.maffsgames-local/docs-9oct-relist-factor-theorem.py` on the home machine; then canon §0.2,
§7.8 lane rules, timer-policy, the rulings in §7.6. **After it:** PREPUSH-SCOPE (no contract yet: Jon to paste),
then LIBRARY-DRAFT (Jon, 19:35; new ★ room, Mrs Barb Phile's library; parked: after The Rightful King and Car Trap
drafts; its contract is saved verbatim under contracts/ when it starts). CAR-TRAP-DRAFT is the cloud lane's
(merged #235); its contract is `docs/handover/contracts/2026-10-09-car-trap-draft.md`.
**Open for Jon:** Escape on the initials overlay (never handled; like Skip?); further scientific tagging (candidates
in the SCI-CALC entry).

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
contracts/2026-10-09-it-room-brief.md. SCI-CALC (item 6) is saved as docs/history/contracts/2026-10-09-sci-calc.md.
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

## 2026-10-09 (home): SCI-CALC (item 6)

- **Engine (calculator.js):** xʸ as `^`, right-associative and tighter than a minus on its left (2^3^2 = 512,
  −2^2 = −4); ln, log, eˣ, sin/cos/tan and their inverses (each opens a bracket, like √); π and e with implicit ×;
  DEG (default) / RAD. Errors: ln/log ≤ 0, sin⁻¹/cos⁻¹ outside [−1, 1], tan at odd multiples of 90° (exact for
  whole degrees) or π/2, non-finite. All 65 existing cases unchanged (STOP IF clear).
- **UI:** `mount(el, {keys: 'scientific'})` adds a 13-key block above the basic keys and a DEG/RAD indicator in the
  display; `mount()` without it is key for key the old panel (tested). Fits 320/390/412 px touch, 48 px keys.
- **Tests (test-calculator-js.py):** 27 scientific cases (the contract's, plus inverses, RAD and errors), two
  plants (left-associative ^, no tan 90 guard: both caught), the basic panel's labels, the fit, and the DEG/RAD
  key driving sin.
- **check-calculator.py:** new value `scientific` (calculator.js + keypad.js, "Scientific calculator required",
  `keys: 'scientific'` in the page); `required` unchanged; either badge on the other value fails (12 self-test
  cases). Canon §4.4 and the roster legend updated.
- **CSS (Jon's ruling, 9 Oct):** the calculator, badge and keypad styles moved out of theme.css into
  `schools/assets/calculator.css`, which theme.css imports, so the themed games get them unchanged and Growth
  and Decay links calculator.css alone (its look is otherwise untouched; four tokens mapped to its own).
- **Growth and Decay:** roster `scientific`; badge on the start screen; the calculator under the question,
  `{keys: 'scientific'}`. Not `{answer}`: each sub-question rebuilds its input, so answers stay typed in the
  game's box. AL1 worked end to end on the keys at 390x844 (touch) and 1280x800: 5000eˣ(0.03×20) = 9110.594002
  (sq1), ln(2)÷0.03 = 23.10490602 (sq4), all four sub-questions marked correct, no page error.
- **Report for Jon (no changes; each tagging its own PR):** games whose questions likely need scientific keys,
  from a scan of question text, to confirm by reading: **strong** force-resolver (θ = arctan…, resolving with
  sin/cos), moments-master (ω = 2π×1500/60 = 50π), log-laws (log 6 + log …, ln); **probable** formula-unlocked
  (π, e^, ln), formula-forge (π, r³), complex-converter (e^{iθ}, π, tan), core-maths-paper2c (ln),
  equation-builder (ln), higher-power (ln, π), estimation-golf (π). Games where trig/log appear only in drawing
  or console code (angle-ace, bearing-blitz, circle-theorem-spotter and others) were not counted.

## 2026-10-09 (home): SCORES-OFFLINE (item 5)

- **The class:** /leaderboards/ and the portal called `firebase.initializeApp` / `firebase.database()` themselves,
  outside any guard; on a network that blocks the SDK (`firebase` undefined) the script stopped, and on
  /leaderboards/ that killed the device-local Your Scores. No other served page did (188 .html/.js files checked).
- **Fix:** both read through `MaffsLeaderboard`: new read paths `available()`, `readBoard(slug, level)` and
  `watchRecent(n, cb)` (submit path untouched). Blocked: /leaderboards/ shows Your Scores and "Live leaderboards
  can't load on this network. Your Scores above are kept on this device and still work." (search, level pills and
  cards hidden); the portal hides its ticker quietly.
- **Check:** `scripts/test-scores-offline.py` (ci-line): no served file but the shared module calls the SDK; both
  pages with gstatic.com/firebasejs refused (no page error, Your Scores renders a seeded game, offline line /
  ticker hidden) and with a fake SDK (cards render, ticker shows the score, no offline line). Plants: a page
  calling `firebase.database()` (caught by the rule); main's old /leaderboards/ blocked (caught: "firebase is not
  defined").

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

