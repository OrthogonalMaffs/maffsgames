# Handover: home lane

**OVERNIGHT RUN ENDED (9 Oct 2026), for Jon:** merged, main green: #193 VOCAB-IDEMPOTENT, #194 CONTRACTS-FOLDER,
#197 RELIST-SR (Screening Room listed), #198/#199/#200 F1 batches 9-11 (19 games on MaffsLock). Open: none.
Stopped because no F1 game is left to build: NOT_YET is glorious-gantt (unlisted, the cloud lane's) and graph-sketcher
(blocked by its known phone overflow, todo §3.9). Questions: add unit-converter (on MaffsLock since #196) to MIGRATED?
Keep wrong-on-the-internet's Try again pause and complex-converter's Play Again replaying the mode? Schedule §3.9 for graph-sketcher?

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

**QUEUE (home lane):** empty: ask Jon. The 8 Oct queue and the overnight run are merged.
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

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-09 (home): F1 batch 11 (overnight item 4, #200, merged 2782d17, main green after one flake rerun)

- **Claims read on main:** `cloud-remaining:` empty. **Batch: the last three listed games on NOT_YET:**
  eigenvalue-extractor, matrix-crunch, boolean-blitz. After it NOT_YET holds glorious-gantt (unlisted, the cloud
  lane's) and graph-sketcher (held back, batch 10), with unit-converter outside it on the cloud lane's lock.
- **On MaffsLock, each with its declaration, seeds 1-3 passing.** NOT_YET: 2 (glorious-gantt, graph-sketcher).
- **Faults fixed beyond the swap:**
  - boolean-blitz: options marked by a CSS class only; on main one wrong answer then Enter on each option gave 5
    marks and 3 points the student never earned (now 1 mark, 0 points). A wrong answer waits on MaffsNext under the
    walkthrough; a right one keeps its own Next, which acts once.
  - matrix-crunch: after an option was marked, the Flag as Singular button stayed live (a CSS class): on main a
    wrong option then the flag gave 2 marks. One lock now covers the options and the flag. A wrong answer or a wrong
    flag waits on MaffsNext under the worked solution. The flag path (not pressed by the check) double-clicked in
    Chromium at stage 2: one mark per question, game over after three lives, one game_completed.
  - eigenvalue-extractor: the characteristic-quest shape (batch 10).

## 2026-10-09 (home): F1 batch 10 (overnight item 4, #199, merged ebc91e0, main green)

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
- **CI fix in the PR:** check-teacher-invite.py's Laws-mode driver read log-laws' removed `answered`; it asks MaffsLock.

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
