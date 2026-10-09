# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**OVERNIGHT RUN (Project Claude for Jon, 8 Oct 2026, 23:45):** `docs/handover/contracts/2026-10-08-overnight.md`
(verbatim; its rules override the checkpoint rule for this run). Items: 1 VOCAB-IDEMPOTENT (DONE, #193 merged 9 Oct,
fce8721, main green), 2 CONTRACTS-FOLDER (DONE, #194 merged 9 Oct,
7b7b7e2, main green), 3 RELIST-SR (DONE, #197 merged 9 Oct, d1e03ec, main green),
4+ F1 batches 9-11: batch 9 DONE (#198 merged 9 Oct, 2712f54, main green); batch 10 in progress.

**Contracts (canon §7.8.2, contract CONTRACTS-FOLDER):** each is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md`; the queue below holds a one-line pointer; the file moves to
`docs/history/contracts/` when the work merges. Read a contract when its item starts, never at session start.

**QUEUE (home lane):** the overnight run above. The 8 Oct queue (ESSENTIALS-WORDING to DOCS-SMALL, F1 batches 7-8,
the checkpoint) is all merged; its list is in the archive.
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item:** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty
  (NOT_YET: 22). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
  `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
  line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-09 (home): F1 batch 10 (overnight item 4, branch `claude/f1-batch10`)

- **Claims read on main:** `cloud-remaining:` empty (UC-FIX merged). unit-converter dropped anyway (the overnight
  contract: the cloud lane's), factor-theorem already migrated.
- **On MaffsLock, each with its declaration, seeds 1-3 passing:** core-maths-paper2b, core-maths-paper2c,
  growth-and-decay, normal-navigator, log-laws, test-the-claim, characteristic-quest, complex-converter.
  **NOT_YET: 5** (boolean-blitz, eigenvalue-extractor, matrix-crunch; glorious-gantt unlisted; graph-sketcher, below).
- **graph-sketcher taken out of the batch (blocked, not decided):** its known phone overflow (checker-allowlist,
  361-567px, todo §3.9 "in no batch yet") zooms the page out at 390px, and the check's tap on Next lands on the site
  footer ("Parent guides"). A student's would too. The overflow is §3.9's work, not F1's; the migration is easy once
  the page fits. complex-converter took its place.
- **unit-converter (for Jon):** the cloud lane's UC-FIX (#196) put it on MaffsLock and took it off
  `cloud-remaining:`; the check now judges it in full and says the home lane adds it to MIGRATED. The overnight
  contract says leave it to the cloud lane, so it is not added here.
- **Faults fixed beyond the swap:**
  - test-the-claim: no guard anywhere. On main a double-click on Step 6's Check marked the test twice and scored it
    twice (shown: 2 marks, 155 points; now 1 and 85); every step's Check could count twice, Next Question could skip
    a test. Each Check now locks the step panel until the next step renders or the step reopens (Try Again, or at
    once where there is none); a wrong conclusion waits on MaffsNext under the model answer; a right one keeps its
    own Next, which acts once. Functions its verifier runs in node are untouched.
  - growth-and-decay: a double-click on Check with a wrong value marked twice (shown on main); now one mark per
    attempt, the sub-question reopening on Try Again (split-it's pattern); a wrong interpretation option waits on
    MaffsNext (it moved on after 1.5 s); Next Scenario acts once.
  - log-laws: Laws mode's `answered` flag and Solve mode's `busy` flag replaced. Solve is not played by the check:
    double-clicked through a 10-question run in Chromium, 10 marks, one game_completed.
  - normal-navigator, characteristic-quest, core-maths-paper2b/2c: options guarded by a CSS class or a flag only;
    wrong answers now wait on MaffsNext under the worked solution (normal-navigator's right answers keep their own
    "Got it", which acts once). paper2b/2c follow paper1/2a (batch 7).
  - complex-converter: Roulette's wrong answer waits on MaffsNext (it moved on after 1.2 s); Sniper's `sWaiting`
    flag replaced by a lock on the diagram (the SVG gets tabindex="-1" so the lock has a control to hold: locking the
    bare SVG held nothing, a first try marked every double-tap twice); a miss waits on MaffsNext. **Play Again now
    replays the mode just played; it reloaded the page to the menu** (the reload also defeated the check). Sniper (15
    shots, double-tapped: 15 marks, one completion) and Triples (5 rounds, one completion) played in Chromium.
- **Verifier:** normal-navigator adds `NO_LOCK_FRESH_INIT` (it answers at once after each render).

## 2026-10-09 (home): F1 batch 9 (overnight item 4, #198, merged 2712f54, main green)

- **Claims read on main:** `cloud-remaining: unit-converter` (UC-FIX, #196 open); factor-theorem is already migrated.
- **On MaffsLock, each with its declaration, seeds 1-3 passing (KS3, then GCSE):** just-pythag-it-bruv,
  wrong-on-the-internet, higher-power, prisoners-dilemma, surd-simplifier, coordinate-geometry-dash, formula-forge,
  scale-factor-scaling. **NOT_YET: 14** (13 listed, unit-converter claimed; glorious-gantt unlisted, the cloud's).
- **Faults fixed beyond the swap:**
  - surd-simplifier, coordinate-geometry-dash, formula-forge, scale-factor-scaling: options "locked" by a CSS class
    only, so Enter re-marked (shown on main: one wrong answer, then Enter on each option, = 5 marks; now 1). A wrong
    answer now waits on MaffsNext: surd-simplifier's used to move on after 1 s; the other three keep their "Got it"
    label, now MaffsNext under the worked solution. coordinate-geometry-dash's right answer still shows the
    solution and its own button, which now advances only from a shown solution.
  - wrong-on-the-internet (retry until right, kept): **each wrong attempt now waits on Try again (MaffsNext, 3 s
    floor), then the options not yet tried reopen.** It used to reopen at once; the answer-once rule (one mark per
    attempt, canon 7.6/7.6.0) needs the pause, as split-it's Try Again. For Jon: say if the pause is too long here.
  - higher-power: `holAnswered` and `pairsLocked` flags replaced (lock/fresh); Pairs locks the grid while two cards
    are up. Pairs is not played by the check: double-clicked through a whole run in Chromium, one attempt per pair,
    one game_completed, one submit. A wrong call still ends the run after 2 s (a MaffsNext there would make its
    double-click count as a second completion in the check).
  - prisoners-dilemma: `choiceLocked` replaced, C/D keys too; each tournament game is one session. Tournament
    double-clicked through in Chromium: 7 opponents, 140 rounds, 7 game_completed, 7 submits.
  - just-pythag-it-bruv: already guarded by its own state; swap only. Its verifier adds `NO_LOCK_FRESH_INIT`.
- **Answer lock now five CI parts** (L5 added; main's last run had L1 at 254 s with 74 games, budget 360 s).

## 2026-10-09 (home): RELIST-SR (overnight item 3, #197, merged d1e03ec, main green)

- **Step 1 on main, all met:** verify-screening-room.py runs in CI (ci-line, group E); the register has no open
  CRITICAL or HIGH (t4-014 MEDIUM and t4-017 LOW open); `check-answer-lock.py --game screening-room` PASS.
- **NOT_YET:** already done by F1 batch 8 (#190): NOT_YET is NOT_YET_AT_START minus MIGRATED, and batch 8 added
  screening-room to MIGRATED, so the 22 already excluded it. Nothing to edit.
- **Relisted, everything the unlisting commit (e419439) removed:** roster row back at GCSE #62 (GCSE 29, Unlisted
  2); three portal cards verbatim after Given That's (New for 2026/27 with its hand-placed "New", GCSE, Core); the
  weekly fact's game link; sitemap; spec map P6/P9, J1-J3, §3.9 and the coverage row; hub row (out of NOT_ON_HUB);
  canon: 95 live, 2 unlisted, §6.1's §3.9 row (Expectation Station's stale "(unlisted)" dropped too). Not on
  /essentials/ before unlisting, so not added. todo §1.72 closed.
- **/updates/: no entry, no badge.** Phase 3 showing the scenario and array again is the fix for t4-015 (class
  "hidden data": the question needed a count it no longer showed), a correctness fix, which §3.4 excludes.

## 2026-10-09 (home): CONTRACTS-FOLDER (overnight item 2, #194, merged 7b7b7e2, main green)

- **CLAUDE.md** names the two handover files in its heading and says `docs/handover/contracts/` is read only when
  its item starts. **Canon §7.8.2** records the convention (verbatim file on receipt, one-line pointer in the queue,
  moved to `docs/history/contracts/` on merge). **check-context-size.py** never measured the folder (its FILES are
  CLAUDE.md and the two handovers); its docstring now says so. Nothing else at start-up reads the folder (no
  hook; `.claude/rules/` holds no handover pointer to it).
- **home.md** held no live contract text (DOCS-SMALL's was archived in #188); the finished 8 Oct queue list and the
  three oldest entries (F1 batch 7, MAIN-RED, VOCAB-SHOWTHAT) moved to the archive. The overnight contract is the
  first file in `contracts/`; it moves to history when the run ends.
- **STOP IF checked, not met:** start-up load (LF bytes) before 42,222 (CLAUDE.md 12,246, home.md 15,416, cloud.md
  14,560); after 36,287 (12,395, 9,332, 14,560).

## 2026-10-09 (home): VOCAB-IDEMPOTENT (overnight item 1, #193, merged fce8721, main green)

- **Cause, more exactly than the contract's:** the game calls the helper once per text node, and the re-wrapping
  happened inside that one call: wrapExamVocab ran term after term over its own growing output, so a later term
  matched inside markup an earlier one wrote ("verify" in the aria-label "Verify that" wrote, Q10; "hence" after
  "hence find", Q13; "State" inside the "Write down" tooltip, T8(c)). Calling the DOM pass twice was already safe.
- **Fix (exam-vocab.js only):** each term is matched in the original text, never overlapping an earlier term's
  match (list order kept, so "hence find" still beats "hence"); only text outside tags is matched; text inside an
  existing exam-vocab-wrap is left alone. wrap(wrap(x)) == wrap(x).
- **STOP IF checked, not met:** of 509 Factor Theorem strings, 42 hold a term; 7 change on a first application and
  every one of the 7 is the fault (Q10, Q13, Q33, T1b, T8b, T8c, T10b). The other 35 are byte-identical.
  Only factor-theorem loads exam-vocab.js.
- **Test:** `scripts/test-exam-vocab.py` (B3): every CONTENT string wrapped twice, attributes clean, no nested
  wraps, and the game's own render with the tooltips applied twice; the old function planted fails naming Q10.
- **factor-theorem-t5-008 closed** in this PR (factor-theorem was not on `cloud-remaining:` and had no open PR).

## 2026-10-09 (home): F1 batch 8 (branch `claude/f1-batch8`, worktree E:/jon/mg-b8)

- **On MaffsLock, each with its declaration, seeds 1-3 passing:** standard-form-blitz, proportion-blaster,
  formula-unlocked, graph-transformer, simultaneous-solver, tax-theft, stat-attack, quadratic-factoriser. screening-room
  (it already loaded the lock) passes seeds 1-3 and joins MIGRATED. **NOT_YET: 22.** `cloud-remaining:` was empty;
  the only open cloud PR (#187, merged during the batch) claimed probability-paradox, already migrated.
- **Faults fixed beyond the swap:**
  - standard-form-blitz, proportion-blaster: no answer guard at all (a CSS class only); a wrong answer moved on after 1 s.
    Wrong now waits on MaffsNext with the right option shown.
  - formula-unlocked: the wrong path's own "Got it — next question" button ran nextQ twice on a double-click (a
    question skipped); now MaffsNext with the same label, under the worked solution.
  - graph-transformer: after a match the moves were locked by a CSS class only, so moving away and back re-matched and
    scored the puzzle again; Skip after a match marked it wrong as well; a double-click on Skip skipped two puzzles.
    Now a match or Skip locks the moves; **Skip is the puzzle's wrong answer and now names the target transformation
    and waits on Next** (canon 7.6), where it used to move straight on. **Jon's ruling (9 Oct): keep it, "the learning
    needs to be shown not skipped".**
  - tax-theft (retry-until-right kept): a double Enter on a right amount marked it twice **and skipped the next step**
    (two 800 ms timers both advanced; shown on main: step index 2 after one answer). Each readable attempt now locks;
    a wrong one reopens the step after the fresh window.
  - stat-attack: a double-click on the last step's Check (or an interpretation option) ran showCompletion twice: two
    marks, the scenario scored twice; a double-click on a wrong step cost two slips. Each attempt now locks; a wrong
    one reopens the step.
  - simultaneous-solver: the A-Level mode's own flag and raw timer replaced; the Foundation stages (already guarded by
    their state machine) lock each step once its entry is readable.
  - quadratic-factoriser: the GCSE `locked` flag replaced; Higher's step picks and Independent check, and Formula's
    answer, lock their panel; every render opens a fresh window. Higher and Formula (not played by the check, which
    plays GCSE) were double-clicked through a whole session in Chromium: 4 marks, indexes 1-4, one game_completed.
- **Verifiers:** proportion-blaster, formula-unlocked and simultaneous-solver add `bc.NO_LOCK_FRESH_INIT` (as batch 7).
  **simultaneous-solver's phone-fit check was timing-dependent on main too:** KaTeX's fonts (from the CDN) arriving
  after stepInView() has scrolled grow the Stage 4 step by ~25px at 320x568 (shown 4 runs in 8 on main's page). The
  verifier now loads every font face before playing: 6/6. (A first-visit student can meet the same 25px; the page's
  own fix, re-running stepInView when fonts land, is not in this batch.)
- **Answer lock split into four CI parts** (L1-L4, `--part i/4`; ci-groups.py already listed L4).
- **Next:** CHECKPOINT (queue item 6) once this merges with main green. Batch 9 candidates for the next session:
  just-pythag-it-bruv, surd-simplifier, unit-converter, scale-factor-scaling, growth-and-decay, log-laws,
  graph-sketcher, normal-navigator (read `cloud-remaining:` first).

## 2026-10-09 (home): DOCS-SMALL (#188, merged 883a638, main green)

- **STOP IFs clear:** correlation-or-coincidence's `QUESTIONS` on main has 84 items (28 cause, 28 both, 28 chance).
  Every roster parser (bank_common, check-banks, check-leaderboard-coverage, audit-katex/gen_tables, check-calculator)
  reads only the #, slug, levels and calculator cells, never the description, so the count wording is free text.
- **Roster:** the header gains the convention ("N per session, generated" vs bank size); just-pythag-it-bruv's row
  reads "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3 generated)".
- **/updates/:** October, Improved: "Correlation or Coincidence: now 84 questions, twice as many as before." The
  page is monthly, so the line sits in October beside Expectation Station's 8 Oct line. Updated badge: both home
  cards carry `data-badge="updated" data-badge-date="2026-10-08"` (canon §3.4, every occurrence).
- **Generator rows noticed, not changed** (none is just the count wording): split-it ("Procedural generation", no
  count); free-daily-pizza (90/206/138/84 are each stage's generated pool, not a session); simultaneous-solver (48 per
  stage are generated offline by `scripts/gen-simultaneous.py`, so a fixed bank: the size is right as it stands).
- **For Jon:** correlation-or-coincidence's own roster row still says "42 items"; the contract's DO NOT TOUCH covers
  it. The October /updates/ "New" line also says 42; it was true when written.
