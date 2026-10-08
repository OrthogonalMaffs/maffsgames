# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**QUEUE (home lane), Jon, 8 Oct 2026 (night)**, replacing the checkpoint's "ask Jon for that queue" note. Run in
order; the standing rule applies (start the next item when one finishes; stop only for a STOP IF, an unruled
decision, or a checkpoint). Each contract's verbatim text is below the list; move it to the archive when it merges.
1. **ESSENTIALS-WORDING: DONE, #172 merged 8 Oct (c1fc37a).** Its verbatim text was in Jon's queue message only.
2. **RELIST-3: DONE, #176 merged 8 Oct (c0c825b).** (Jon, 8 Oct, sent after the queue.) It
   supersedes RELIST-ES-TB, sent minutes earlier: same relists, plus listing Just Pythag It, Bruv (Jon approved it).
3. **CHANGED-UTF8: DONE, #178 merged 8 Oct (d73d3b6).**
4. **GA4-COUNTRY-CANON: DONE, #179 merged 8 Oct (3c3217c).**
4a. **VOCAB-SHOWTHAT: DONE, #180 merged 8 Oct (47ee9b9)** (Jon, 8 Oct, sent later: run after GA4-COUNTRY-CANON, before F1 batch 7). The "show
   that" tooltip in `schools/assets/exam-vocab.js`; closes factor-theorem-t5-009 unless the cloud lane holds that game.
5. **F1 batch 7: DONE, #182 merged 8 Oct (259c143), main green. F1 batch 8: PR #190, branch `claude/f1-batch8`
   (9 Oct; see its entry).** Was: not started (Jon said "checkpoint" at the batch 7 boundary). Then F1 batch 8, exactly as the standing F1 item below states (8 per batch, Year 6/KS3/GCSE/
   Core first; read `cloud-remaining:` in `docs/handover/cloud.md` on main before building each batch and drop
   every game on it).
6. **CHECKPOINT after batch 8 merges with main green:** update this file and stop. Do not start batch 9 in that session.
7. **DOCS-SMALL: DONE, #188 merged 9 Oct (883a638), main green.** Its verbatim text is in the archive.
- **CHECKPOINT STOP (Jon, 8 Oct, late):** batch 7 merged, main green; this session stopped at that boundary.
- **MAIN-RED: DONE, #184 merged 8 Oct (f1a097d), main green** (see its entry).
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item:** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty
  (NOT_YET: 22 once batch 8 merges). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
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
    and waits on Next** (canon 7.6), where it used to move straight on. For Jon: say if Skip should stay instant.
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

## 2026-10-08 (home): F1 batch 7 (#182, merged 259c143, main green)

- **On MaffsLock, each with its declaration, seeds 1-3 passing:** circle-theorem-spotter, index-laws, modular-battle,
  correlation-or-coincidence, estimation-engine, given-that, core-maths-paper1, core-maths-paper2a. probability-paradox
  (the cloud lane's #177) also to MIGRATED. **NOT_YET: 31.** Chosen from Year 6/KS3/GCSE/Core games NOT next in the cloud
  lane's listed-games order (core-maths-paper2b/2c, wrong-on-the-internet, higher-power, ... left to it).
- **Faults fixed beyond the swap:** circle-theorem-spotter moved on 1 s after a wrong answer with nothing to read: it now
  names the theorem and waits on Next; Play Again's double-click pressed Start. given-that: phase 1 wrong moved on by
  itself (now waits on Next); its own Next fired twice on two quick Enters (the hidden button keeps focus) and skipped a
  question; phase 2's two tries survive a double-click. The Core Maths papers' own Next could be pressed twice (a second
  press during the section banner skipped a question): it now acts once, only on an answered question. modular-battle:
  the 90 s clock running out during a question's timer or Next now stops both.
- **Shared fixes (home lane):** `check-answer-lock.py` reads no clock as a score (modular-battle's #timer is a .score-val,
  so the countdown looked like a re-mark); `check-site.py`'s start finder never follows a link to another page (the Core
  Maths papers' "Play Fermi Lab" signpost took the driver away).
- **Declarations:** estimation-engine declares `ready` from its own state (on a phone the keypad makes its boxes
  read-only, so nothing looked typeable); the Core Maths papers declare `start_sel` (".start-btn"). given-that gains a
  read-only `window.GT.ui` (its game is an IIFE), as EE.ui and COC.ui. verify-given-that adds `bc.NO_LOCK_FRESH_INIT`.
- **Answer lock split into three CI parts** (L1-L3, `--part i/3`): L2 ran 6m43s of its 8 min (75% budget 6m) on the
  first push. ci-groups.py already listed L3 and L4; a part is added only by its ci-line. Add L4 when a part nears 6 min.
- **Next session:** DOCS-SMALL (item 7) first, then F1 batch 8. **Batch 8 also needs L4** (`--part i/4`): with batch 7
  L1 ran 5m31s against its 6 min budget. Candidates (GCSE/Core, not next in the cloud lane's order; read
  `cloud-remaining:` first): proportion-blaster, quadratic-factoriser, simultaneous-solver, standard-form-blitz,
  stat-attack, tax-theft, formula-unlocked, graph-transformer. NOT_YET: 31 (30 once screening-room, which now loads the
  lock, passes).

## 2026-10-08 (home): MAIN-RED, like-terms-collector's verifier typed before the question settled (#184, merged f1a097d, main green)

- **Main red after #180** (47ee9b9, run 37811456669 attempt 1), Content verifiers E: `FAIL item 1: typed 8.9/6.5,
  marked correct=None, expected False` and `the feedback does not say why: ''`. **The re-run (attempt 2) passed: main
  green again, Jon told.**
- **Cause (in the verifier, not the page):** `loadInputQuestion()` focuses `#ans0` on a 50 ms MaffsLock timer. The
  verifier typed as soon as `#ans0` was visible; Playwright's `fill('#ans1')` selects the box and inserts the text in a
  second step, and when the timer fired between the two, "6.5" went into `#ans0` ("8.965", `#ans1` empty), so Check
  marked nothing (an unreadable box is not an answer). Shown directly: interleaving the two steps leaves
  `['8.965', '']` and no mark. The same "marked correct=None" as run 37626794263 (6 Oct), which the 6 Oct and #167
  fixes did not touch: likely the cause after #89 and #109 too.
- **Fix:** type only once the page's own focus is on `#ans0` (its signal that the question has settled); `read_mark`
  takes the mark from the same call that saw it land. Local: the other verifiers that `page.fill` (just-pythag-it-bruv,
  six-sevens) fill one box, so a focus timer cannot redirect their text; component-crusher's and split-it's (the
  other 50 ms focus timers) set values in the page.
- **Proof:** a 100 ms runner stall inside `fill('#ans1')` (select, stall, insert): main's verifier fails 3/3 with main's
  exact message; this one passes 3/3. A 200 ms gap after every Playwright action: passes 3/3. Plain: 20/20.

## 2026-10-08 (home): VOCAB-SHOWTHAT (#180, branch `claude/vocab-showthat`)

- `schools/assets/exam-vocab.js`: two strings only, "show that" (Jon's exact text) and "hence show" ("prove" -> "reach").
  Only factor-theorem loads the file (STOP IF clear); its "show that" questions are all numerical (f(a) = 0).
- Proof: on the stub server in Chromium, factor-theorem practice Q3's tooltip reads the new text.
- factor-theorem-t5-009 closed here (`status: fixed`, `pr: 180`, `ruling:` Jon's 8 Oct ruling): nothing claimed on
  `cloud-remaining:`, no open PR touched factor-theorem or exam-vocab.js. The cloud lane's factor-theorem queue already
  left t5-009 out.

