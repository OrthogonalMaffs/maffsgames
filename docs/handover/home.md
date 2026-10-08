# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**QUEUE (home lane):** done 8 Oct: DET (#144), CLAIM (#145), ESSENTIALS (#150), UPDATES (#151). Their verbatim
contracts and notes moved to `docs/history/handover-home-archive.md` ("QUEUE as of 8 Oct") in contract CTX. Then:
1. **Contract CTX: DONE, #158 merged 8 Oct (b66ccde).** Its verbatim text: `docs/history/handover-home-archive.md`
   ("QUEUE items CTX and F1 batch 5"); its notes: the CTX entry below.
2. **F1 batch 5: DONE, #161 merged 8 Oct (8216ff4), main green.**
3. **F1 batch 6: PR #165 on `claude/f1-batch6` (8 Oct; see its entry below).** Merge on a green Gate, watch main, then
   **CHECKPOINT STOP** (2 batches merged since the last stop: 5 and 6). Next batch: re-read `cloud-remaining:` and the
   cloud lane's order in cloud.md first; NOT_YET is 40.
- **cloud.md not trimmed (contract CTX step 3):** the cloud lane had PR #154 open on it. Trim it to its header and
  newest three entries (to `docs/history/handover-cloud-archive.md`) at the next cloud checkpoint.
- **Follow-up (home lane, small):** `check-changed.py` crashes (`UnicodeEncodeError`, cp1252) printing a failure when
  its output is redirected to a file on Windows. Until fixed: `PYTHONIOENCODING=utf-8 python scripts/check-changed.py`.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.
3. **Then** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty.
   **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
   `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
   line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Checkpoint rule:** stop after every 2 batches merged (main green), or at the next batch boundary when Jon
  says "checkpoint". At each stop, update this file.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-08 (home): F1 batch 6 (#165, branch `claude/f1-batch6`, worktree E:/jon/mg-b6)

- **On MaffsLock, each with its declaration, seeds 1-3 and its own verifier passing:** sequence-solver, bearing-blitz,
  expected-damage, maths-court, equation-builder, fermi-lab, better-value, chart-interrogator. terrible-advice (the cloud
  lane's #160) also to MIGRATED. **NOT_YET: 40.** Chosen off the cloud lane's listed-games order; opened as a draft PR
  at the start so the cloud lane could see it.
- **Faults fixed beyond the swap:** sequence-solver and bearing-blitz wait on Next after a wrong answer (bearing-blitz's
  Fire was "disabled" by a CSS class only; the last life's miss waits too); expected-damage, maths-court and fermi-lab
  keep their own Next, which now acts only on an answered question (a double-click skipped one); maths-court's two
  attempts survive a double-click and a tapped card cannot re-mark; equation-builder's double Check no longer spends the
  retry and the shown key waits on Next; fermi-lab's Calculate Estimate marked and scored twice on a double-click, and a
  step could count twice; chart-interrogator (logs right answers only, so `mark_any`) marked a right answer twice on a
  second Enter inside its 600 ms advance, and a double Submit Comparison finished the game twice.
- **Declarations:** bearing-blitz and fermi-lab declare `start_sel` (no Start button), so the double-click on Start is
  real; equation-builder fills its slots from data and checks twice to spend the retry, stopping if the question moved on.
- **Verifiers:** sequence-solver and fermi-lab get `bc.NO_LOCK_FRESH_INIT` (they answer as soon as a question renders).
  better-value's page-load KaTeX poll keeps a raw timer, marked `// lock-ok:`.

## 2026-10-08 (home): F1 batch 5 (branch `claude/f1-batch5`, worktree E:/jon/mg-b5)

- **On MaffsLock, each with its declaration:** angle-ace, free-daily-pizza, split-it, six-sevens-bruv, 52dle,
  distinctly-average, seven-bridges. Each passes check-answer-lock on seeds 1-3 and its own verifier where it has one.
  **MIGRATED also gains** trig-wars, truth-buster, gradient-hunter, spot-the-muppet and word-problem-decoder (the cloud
  lane's; each passes seeds 1-3 here). trig-wars: its tap-through (`aimAtEnemy`, used only by the declaration) also
  searches 46-85 degrees, since some terrains leave no robust shot at 45 or below (seeds 2, 3, 8 failed; 1-12 pass).
- **word-problem-decoder dropped from the batch:** the cloud lane claimed and fixed it (#156, #157) while this batch was
  parked unseen (no PR; its queue note was only on the unmerged CTX branch). Main's version is kept. **Lesson: a parked
  batch must be visible on main (a draft PR, or its games in home.md on main) before a pause, or the cloud lane cannot
  skip its games.**
- **Fixes beyond the swap:** angle-ace's own "Got it" button is now `MaffsNext.wrong` (same label); split-it keeps its
  retry, Check stays locked until Try Again, Best value waits on Next after a wrong pick; free-daily-pizza and
  distinctly-average lose their local guards (`state`, `locked`) to the lock; 52dle locks per guess and reopens for the
  next; seven-bridges: a wrong Impossible waits on Next, the solution animation's timers are MaffsLock timers (they
  could draw onto the next puzzle), and Play Again returns to the start screen in the page (it reloaded, which the
  check's Play-again probe misreads).
- **Verifier lessons:** a sweep that answers at once needs `bc.NO_LOCK_FRESH_INIT` (angle-ace, free-daily-pizza,
  six-sevens). A top-level `const endGame` cannot be stubbed by `window.endGame =`: keep `function endGame(){finishGame()}`.
- **NOT_YET: 47.**

## 2026-10-08 (home): contract CTX, what every session loads (branch `claude/ctx`, worktree E:/jon/mg-ctx)

- **Sizes (bytes, before -> after):** CLAUDE.md 159,172 -> 12,246; home.md 63,666 -> ~13,300;
  cloud.md 55,721 (deferred); .claude/rules/ 42,011 -> 41,960. Canon 148,526 -> 175,803 (§12).
- **CLAUDE.md** keeps the every-session rules, the cloud-claim rule (copied verbatim from canon §7.8.2), "Jon never
  amends contracts: PC sends complete pastes" (new: it existed nowhere; wording from the contract) and a "Where
  things live" pointer block. Every other section moved verbatim (proof: every non-blank old line is in the new
  file, the archive or canon §12, except the one reworded pointer sentence).
- **Canon §12 (new):** the sections that existed only in CLAUDE.md: check-site tiers 1-4, no rejection sampling,
  `MaffsOptions.build()`, generator ranges, scaffolds fade, accessibility, tiered banks, level colours, the Firebase
  leaderboard. Four canon pointers to "CLAUDE.md" now say §12.
- **Archives:** `docs/history/claude-md-archive.md` (dated handovers, state sections, and reference sections canon
  already holds, each headed with where it lives), `docs/history/handover-home-archive.md` (the done contracts'
  queue text and every entry before UPDATES). cloud.md deferred (cloud PR #154 open on it).
- **`scripts/check-context-size.py`** (site-wide ci-line): CLAUDE.md and both handovers <= 20 KB; self-test plants
  a 25 KB CLAUDE.md. Roster title no longer carries hand-typed counts.
- **STOP IF hit, answered (Jon, 8 Oct):** seven rules lived only in dated sections; all stand. Placed as he named:
  canon §3.4 (New & updated badges, his Updated definition verbatim), §3.5 (/updates/: describe a false claim, never
  quote it), SR-24 (counterexample refutes the statement as written), SR-25 (words, figure and key agree), §0.4 (register
  files edited by hand), §7.9 (verifiers read the page's feedback, not a wrapped mfg; pointer in CLAUDE.md), CLAUDE.md
  "Session practice" (`--against` scratch copy; never `| tail` under a timeout). Then merge on a green Gate.
