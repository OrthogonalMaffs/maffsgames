# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**QUEUE (home lane; Jon, 7 Oct evening session):** MaffsLock #125, batches 1 (#129), 2 (#132), contract LH (#133)
and batch 3 (#136) are done. This session runs batch 4 and the relist PR, then stops at the checkpoint. Then:
1. **Contract DET: DONE, #144 merged 8 Oct, main green (fedb2ce).** check-answer-lock.py made deterministic (Jon, 7 Oct). Two
   causes fail a PR at random: (a) after a right answer `to_next()` waits a fixed 350 ms and returns 'auto', so the
   next tap can land in MaffsLock's 300 ms fresh window (UNPLAYABLE; #134 prime-or-composite, #137
   fraction-equivalence); (b) with no answer hint the driver taps option (k+1) % 2 on 8 unseeded questions, all
   right ~1/2^8 of the time in a two-option game. Fix in the driver, never with retries: wait for game state (next
   question rendered AND its fresh window over; a read-only `MaffsLock.isFresh(container)` in answer-lock.js if
   needed, documented, no behaviour change); two-option games declare an answer that picks the option differing
   from the key; a seeded default (seed printed) for games with no hint; no new declaration key (else STOP IF).
   Also seen 7 Oct: `start()` waits a fixed 8 x 400 ms for an option group (eigenvector-engine UNPLAYABLE once
   under local load, then 3/3 alone). Proofs: same seed, identical event log; a forced all-right draw and a tap inside the fresh window both handled
   every time; no Math.random and no fixed delay on the path to a wrong answer; a planted lock removal still caught
   every run; then 20 consecutive passes on prime-or-composite and fraction-equivalence (smoke test only). Canon
   §7.6, this file, and one line in cloud.md (two-option games declare the differing-from-key answer). DO NOT
   TOUCH: answer-lock.js behaviour, what the check tests, scoring, cloud-remaining games, CI retry settings.
   STOP IF: the fresh window can't be observed without changing answer-lock.js behaviour; a two-option game's
   wrong answer can't be expressed with the existing key; determinism would stop it testing something it tests now.
2. **Contract ESSENTIALS** (Jon's paste, received in full 8 Oct): after DET merges and main is green. Verbatim:
   > TASK: Rename the resit section to "Essentials", stop any student-facing page naming the student's status,
   > and correct the homepage title and description so they're accurate and name who the site is for.
   > ROOT CAUSE: Status labels and site facts are hand-typed into individual pages. The two resit escape rooms'
   > description, og and twitter tags open "A GCSE resit escape room on…", so a link posted in Google Classroom or
   > Teams shows that label to the whole class; homepage and /escape-rooms/ cards say "for a GCSE resit class". The
   > homepage meta/og description says "96 free curriculum-aligned maths games" although the portal lists 91, and
   > says "KS3 through Further Maths" while the page subtitle says "KS3 through A-Level". Neither names the
   > priority audience or Core Maths.
   > CLASS CHECK: two classes. (1) Status labels on student surfaces: fix at the layer, a canon rule plus a CI
   > check, not just edits. (2) A site fact (the game count) typed by hand beside the data it should come from:
   > generate it from the single metadata source, or remove the number.
   > EXACT CHANGE: 1. Canon rule (Jon, 7 Oct): "Name the maths, never the student." Teacher surfaces
   > (/essentials/, its metadata, each room's teacher.html, teacher guides) may say resit or post-16. Student
   > surfaces (every game and escape-room page, including description, og and twitter tags; portal and
   > /escape-rooms/ cards) describe the topic and level only (e.g. "A GCSE escape room on factors, primes and HCF").
   > 2. Rename /resit/ to /essentials/: heading "Essentials", with the teacher line under it: "GCSE Foundation
   > maths for students working at grades 1–3, including post-16 resit classes." /resit/ becomes a meta-refresh
   > redirect to /essentials/ (the /schools/spec-map/ pattern) so existing Classroom links keep working. Homepage
   > badge, nav, sitemap, check-resit-page.py and every internal link follow the new address. Analytics:
   > section/item values for this page change to essentials; canon's analytics section records the rename date
   > and the old-to-new mapping so the Sheet and GA4 read across it. 3. Fix the student surfaces: comic-caper and
   > kiln-disaster description, og and twitter tags; the "for a GCSE resit class" card notes on the homepage and
   > /escape-rooms/ (keep the "built from a request, want something built?" invitation without the status label).
   > 4. scripts/check-student-labels.py (CI, declares its ci-line): fails if "resit", "retake" or "post-16" appear
   > in visible text or in description/og/twitter tags of any games/**/index.html, escape-rooms/*/index.html or
   > portal card; teacher.html, /essentials/, docs and code comments exempt. Self-test plants the old comic-caper
   > description; caught. 5. Homepage title, description, og and twitter: no hand-typed game count (generate it
   > from the listed games in the single metadata source, or drop the number: your choice, recorded in the PR);
   > one consistent range; name GCSE Foundation and Core Maths alongside the existing levels. Draft wording for
   > Project Claude to review in the PR. 6. Docs: canon (rule, analytics mapping), handover in home.md.
   > DO NOT TOUCH: game content, keys, scoring; game-page titles (topic-first titles are a later job); Core Maths
   > landing page (build freeze); the escape rooms' gameplay and teacher pages beyond links; Firebase and
   > leaderboard keys; games on the cloud lane's remaining list.
   > SUCCESS CONDITION: /essentials/ live with the teacher line; /resit/ redirects to it; no student surface names
   > the student's status and the check catches the planted label; homepage metadata carries no stale count and
   > one consistent range; listing and resit-page checks pass under the new name; merged on a green Gate; main
   > green; handover current.
   > STOP IF: a generated count needs a new field in the metadata source; the redirect breaks a check that
   > assumes /resit/ is a real page; any analytics event name (not just a value) would have to change.
2b. **Contract CLAIM: BUILT, PR on `claude/claim` (8 Oct).** Its STOP IF hit (no time bound); Jon's ruling (8 Oct):
   option 3, for listed games a claim is a process lock only, the check judges them as unclaimed, the exemption
   stays for unlisted games only, no time bound. Verbatim (Jon, 8 Oct; a separate PR, after DET):
   > TASK: Record the cloud lane's widened remit in canon and make the F1 rollout skip any game the cloud lane
   > has claimed. ROOT CAUSE: From 8 Oct the cloud lane also fixes listed games (Jon's ruling; its contract tells
   > it to claim each game by adding it to the `cloud-remaining:` line in docs/handover/cloud.md before
   > starting). Canon §7.8 still says the cloud lane works only on unlisted games, and the F1 batch plan lists
   > games without checking that line, so both lanes could edit the same game. CLASS CHECK: shared process rule
   > (canon) and shared CI behaviour (check-answer-lock.py already reads `cloud-remaining:`). One canon edit and
   > one rule in the F1 batch procedure; no game files.
   > EXACT CHANGE: 1. Canon §7.8: "The cloud lane may fix listed games it has claimed on the `cloud-remaining:`
   > line in docs/handover/cloud.md (Jon, 8 Oct). It claims one game at a time, before starting it, in a handover
   > commit of its own, and removes the game in the PR that fixes it." 2. docs/handover/home.md and the F1 batch
   > procedure: before building each batch, read `cloud-remaining:` on main and drop any claimed game from the
   > batch. Never claim or edit a game on that line. 3. Confirm check-answer-lock.py treats a claimed listed game
   > the same way as a claimed unlisted one (reported, not failed, while on the line). If it doesn't, make it so
   > in this PR.
   > DO NOT TOUCH: game files; answer-lock.js; the cloud handover file; what check-answer-lock.py tests.
   > SUCCESS CONDITION: canon carries the rule; the batch procedure skips claimed games; a listed game placed on
   > the line in a scratch copy is reported, not failed; merged on a green Gate; main green; handover current.
   > STOP IF: honouring the line for listed games would let a game sit on it indefinitely without failing
   > (propose a bound, e.g. it fails once off the line or after its PR merges).
   - Note for that session (8 Oct, from DET): today `counts()` returns True for any MIGRATED game, so a MIGRATED
     game put on the line is FAILED, not reported: item 3 needs a change. Also check the STOP IF before changing it.
2c. **Contract UPDATES** (Jon, 8 Oct): after ESSENTIALS merges and main is green. Verbatim:
   > TASK: Add Jon's approved October quality entries to /updates/. ROOT CAUSE: The 6-8 Oct clean-up (audit,
   > per-game verifiers, SR-16/17 fixes, the shared answer lock, 17 games relisted) is not on /updates/, the page
   > that shows teachers the site is maintained. Jon approved wording on 8 Oct: honest, no fault counts. CLASS
   > CHECK: Local: content on one docs page, in its existing format. No shared code.
   > EXACT CHANGE: In updates/index.html, October 2026 section, in the page's existing markup and style (links to
   > games as the page does): 1. After the "Which tax year?" note, a second note: <strong>Every answer checked
   > again.</strong> This month we went back through the games and worked out every answer again from each
   > question's own data, by script, rather than relying on the answers typed in when the games were written.
   > Where we found a wrong answer, a true statement offered as a wrong option, or a question using a rule it
   > didn't state, we fixed it. Some games were taken off the home page while that happened; they're back, apart
   > from a handful still being worked on. Every game that has been through this now has its own check that runs
   > whenever the site changes, so a fault can't quietly come back. We're working through the rest of the
   > library in the same way. 2. Under New, first item: <a href="/games/linear-equation-solver/">Linear Equation
   > Solver</a> now asks "What is the optimal move here?" Every move that is equally quick scores full marks, and
   > a move that works but takes longer scores half, with the quicker route shown. A wrong move tells you what
   > went wrong, such as dividing only one side. 3. Under Clarified, first item: <strong>Questions say which rule
   > they use.</strong> Where maths has more than one convention, the games checked so far now say which one: for
   > example which quartile method, or that a roulette wheel is the American kind. 4. Under Improved, first item:
   > <strong>One answer per question.</strong> In some games a second tap, a double-click or the Enter key could
   > mark an answer twice or skip a question. The games updated so far accept exactly one answer per question;
   > the rest are following. 5. Before committing, confirm each claim against the repo: Linear Equation Solver's
   > live marking matches item 2 (full / half / named error); at least one listed game states a quartile method
   > and one names the American wheel (item 3). If either is not true on main, STOP IF.
   > DO NOT TOUCH: existing entries (history stays as written, including the September and earlier October items
   > and the /resit/ link, which redirects); any game file; the portal's New & updated badges (Jon, 8 Oct:
   > correctness fixes do not earn the Updated badge; only student-visible changes do).
   > SUCCESS CONDITION: the four items appear in the October section in the page's style; page passes its
   > existing checks at 320/390/1280; merged on a green Gate; main green; handover current.
   > STOP IF: a claim in items 2-3 is not true on main (report which; do not reword it yourself); the page's
   > checks require a format the text doesn't fit.
3. **Then** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty.
   **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
   `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
   line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Checkpoint rule:** stop after every 2 batches merged (main green), or at the next batch boundary when Jon
  says "checkpoint". At each stop, update this file.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-08 (home): contract ESSENTIALS, BUILT on `claude/essentials` (worktree E:/jon/mg-ess), rebased, PR next

**State (8 Oct, next session):** rebased onto main after CLAIM #145 and #147 (home.md conflict only: CLAIM's
entry kept below). Re-run `python scripts/check-changed.py`, open the PR, merge on a green Gate, then UPDATES (QUEUE 2c).
- **/resit/ -> /essentials/**: page moved (git mv), heading "Essentials" plus the teacher line, analytics section
  `essentials`; /resit/ is a meta-refresh stub (spec-map pattern, registered in check-footer.py). games.json key,
  apply-meta/check-meta, check-resit-page.py (PAGE; filename kept), check-canonical-links RESOLVE/LEVEL pages,
  publish scope, ci-deps KNOWN_TOP, sitemap, homepage badge ("Essentials", section `essentials-link`, item
  `open-essentials`), test-section-clicks, workflow labels all follow. Title: "Essentials: GCSE Foundation
  Maths Games | MaffsGames" (description kept: teacher metadata).
- **Not done on purpose:** /resit/ is NOT in check-canonical-links' REDIRECTS: that would fail the /updates/
  history links to /resit/, which contract UPDATES says stay as written (they redirect). Say so in the PR.
- **Student surfaces:** comic-caper and kiln-disaster description/og/twitter now "A GCSE escape room on ...";
  the four "for a GCSE resit class" card notes (homepage, /escape-rooms/) now "Built from a site user's
  request. Want something built?".
- **scripts/check-student-labels.py:** visible text, alt/title/aria-label/placeholder, script strings (comments
  stripped) and description/og/twitter meta of games/**/index.html, escape-rooms/*/index.html and the portals
  (index, escape-rooms, op). Self-test: the old comic-caper description and three more plants caught; comments
  not flagged. **In the workflow's site-wide list, NOT a ci-line** (a ci-line is selected per named page on PRs;
  this must see every page): a departure from the contract's wording, say so in the PR. **given-that** has a
  tree-diagram question about students re-sitting (6 hits): a KNOWN exception, reported not failed, flagged
  for Jon (game content is DO NOT TOUCH).
- **Homepage:** title "MaffsGames — Free Maths Games for KS3, GCSE, Core Maths and A-Level"; description (also
  og, new twitter tags) "Free maths games and 15-minute escape rooms for UK schools, KS3 to Further Maths,
  including GCSE Foundation and Core Maths. No sign-up, no personal data." No game count AND no room count
  ("eight" vs 8 cards / 11 room folders: same class); subtitle and JSON-LD now "KS3 to Further Maths". Draft
  wording for Project Claude to review in the PR. Choice recorded: the number is dropped, not generated.
- **Canon:** new §7.5.3 (the rule, the check, KNOWN, the teacher line, no hand-typed counts); analytics mapping
  (resit-link->essentials-link, open-resit->open-essentials, resit->essentials, page views) in §1.3; §2.1 and the
  CI tables follow the new address.

## 2026-10-08 (home): contract CLAIM (branch `claude/claim`)

- **STOP IF hit:** honouring the line for listed games would have exempted a claimed game with no time bound.
  Jon's ruling (8 Oct): option 3. For a listed game a claim is a process lock only: the F1 batches skip it, the
  check judges it as unclaimed. The reported-not-failed exemption stays for unlisted games only.
- **Check:** `exempt(claimed, unlisted)` = the line's games that are in the roster's Unlisted section
  (`unlisted_games()`, the same section parse as audit-register.py). Only those are reported, not failed; a
  listed game on the line gets a `note:` line saying it is judged as unclaimed. Self-test covers the parse and
  the rule. Before this PR, a MIGRATED game on the line already failed (`counts()`), but an adopted NOT_YET
  game that was listed would have been reported: now it is judged in full.
- **Canon §7.8.2** carries the claim rule and the ruling; the QUEUE's batch item carries the skip rule.
- **Proof (scratch worktree):** line `cloud-remaining: prime-or-composite truth-buster`, prime-or-composite
  planted with no lock: it FAILS (re-mark, no continue) with the process-lock note; truth-buster (unlisted,
  adopted) stays on the reported path.
- **Follow-up (home lane, next batch):** #143 took truth-buster off the cloud line, and it now passes the check in
  full. Add it to MIGRATED (and consider relisting it under SR-21) in the next batch.

## 2026-10-08 (home): contract DET, check-answer-lock.py deterministic (branch `claude/det`)

- **Driver:** every page's `Math.random` is seeded (`--seed`, default 1, printed in the first line; check-site's
  PHONE_SEED with the run's seed mixed in). The path to a wrong answer has no fixed delay: `start()` waits for
  the screen to change after each Start press and then for an answerable, settled question; `answer()` taps
  only once no fresh window is open; `to_next()` waits for the next question (a new `fresh()`/`screen()` call
  since the mark, or an enabled option group) and its window to close. The only sleeps left in Driver are
  25 ms polls inside those waits. A tap the page sees land in a fresh window (a capture listener added before
  the guard, reading `MaffsLock.isFresh`) is made again once the window closes, and the game goes on the
  note line. The tap-through's 320 ms sleep is now the same settled wait.
- **answer-lock.js:** `MaffsLock.isFresh([target])` added, read-only, documented; test-answer-lock.py's
  `fresh` check covers it. No behaviour change.
- **Declarations:** the two-option games played generically were prime-or-composite, fraction-equivalence and
  factor-race (a scan of every migrated game's option group; spot-the-error is two-option but already
  declared). Each now declares `answer`: for `i >= 1` the option that differs from its key; for `i = 0`
  (the tap-through) the first option, as the generic driver did, so the tap-through still meets right and
  wrong answers. Canon §7.6.0 and one line in cloud.md record the rule.
- **Two snags found and fixed on the way:** (1) a declared answer in a right-answer pause cannot mark, so
  it waited out the deadline: `answer()` now returns at once when no option group or input is on screen,
  but only where the declaration has no `ready` (truth-will-set-you-free's `ready` describes its first
  question only, and the shortcut stalled it). (2) The tap-through keeps its old 1.5 s mark deadline; the
  wrong-answer search waits up to 5 s (load).
- **Proofs (scratchpad `prove_det.py`, results in the PR):** same seed gives an identical event log
  (5 games, desktop + touch); a forced all-right draw gives the same named UNPLAYABLE (seed printed) 3/3
  runs; a fresh window opened before the first tap is caught and re-tapped 5/5 on 7 games, mouse and touch;
  the declared games are wrong on the first answer for 20/20 seeds, both ways; the planted no-lock
  decimal-detective is caught every run (same single fault as the old driver); then 20 passes in a row of
  the two named games.
- **Timing:** local part 1 3m05s, part 2 4m23s (CI's last main run took 5m04s and 5m56s with the old driver).
- **Not changed (out of scope, flagged):** several declarations (component-crusher, linear-equation-solver,
  proof-builder, spot-the-error, suvat, truth-will-set-you-free, expectation-station, factor-theorem) wait a
  fixed `real(350)` inside their own `answer` JS. That wait starts after the driver has already found no
  window open, so it cannot race the window; it is just redundant. Removing it is game-file work for a batch.

## 2026-10-07 (home, night 3): batch 4 (#140); the SR-21 relist PR; CHECKPOINT STOP

- **Batch 4 = #140** (see its entry below). It also filed **expectation-station-pc-001** (Jon's paste: CRITICAL,
  jc, Stage 1 underdetermined on ~33 of 45 items; fix design awaits his ruling A/B), and the self-test now
  plants decimal-detective by name (binomial-blaster, first in MIGRATED once the cloud games joined, guards
  itself, so its no-lock plant played clean).
- **Relist PR (SR-21):** 17 games back, **listed 74 -> 91** (partial-fractions-duel joined after #139 took it off
  the cloud list; also to MIGRATED, NOT_YET 61). Still unlisted (6): expectation-station (Jon's hold,
  pc-001), factor-theorem, screening-room, glorious-gantt (open CRITICAL/HIGH),
  truth-buster (on `cloud-remaining:`), just-pythag-it-bruv (Jon's play-test). Canon SR-21 written. The todo
  checklists' "every entry fixed" item was read as superseded by SR-21's bar (open MEDIUM/LOW stay in the
  register): flagged in the PR for Jon.
- **How:** scratchpad `relist.py` re-inserts each game's exact removed block (from #82/#85/#87's diffs) after its
  old neighbour, bottom-up; spec-map links are merged into today's rows. Hand-done: roster, NOT_ON_HUB,
  check-resit-page.py, the guide's "two free games" line, Component Crusher's Coverage Status row, the hub's last
  comma. A later relist of the seven can reuse the same approach.
- **Next session:** contract DET first (QUEUE above), then ESSENTIALS (its text is now in the QUEUE).

## 2026-10-07 (home, night 2): #136 (batch 3) merged; F1 batch 4 PR; relist PR next

- **#136 merged** on a green Gate after one fix: CI's answer lock L2 failed it with spot-the-error UNPLAYABLE.
  Cause, found by instrumenting the driver: 36 of the game's 110 questions have ONE step (it is the error), and
  the declaration returned without answering when it drew one (about 1 run in 4-6). The declaration now picks
  that step and misses in stage 2. It is not a retry: 2 picks, as before. **For Jon:** on those 36 questions
  stage 1 is a free pick (a content point, not F1's; not filed yet).
- **Batch 4 (this PR):** proof-builder, linear-equation-solver, moments-master, force-resolver on MaffsLock.
  MIGRATED also gains the four the cloud lane finished: eigenvector-engine, truth-will-set-you-free,
  trig-identity-duel, binomial-blaster (all pass). `cloud-remaining:` is now partial-fractions-duel and
  truth-buster. **NOT_YET: 62.**
  - linear-equation-solver's worked-solution Next was a plain onclick (a second Enter skipped a question): now
    MaffsNext. Its hint is refused once the step is answered.
  - proof-builder loads answer-lock.js BEFORE its game script: `const endGame = MaffsLock.finishOnce(...)`
    runs at parse time. **Lesson:** check where the game's inline script sits before putting the include
    beside next-control.js.
  - Register: closed proof-builder-t5-014, -t5-016, moments-master-t5-009, force-resolver-t5-008;
    linear-equation-solver-t4-003 notes its fixed class-1 part (stays open: fold, accuracy field).
- **No Node on this machine:** a JS syntax slip (an unclosed `finishOnce(`) shows only as a driver
  "ReferenceError" in the browser check. Read the error that way.
- **Relist (next):** the scratchpad script `relist.py` (session 9093ec13) puts back exactly what #82/#85/#87
  removed, per game: portal cards, FACTS links, sitemap, hub rows, spec-map links (merged into the current
  rows), /resit/ and the trig parent guide. Roster rows, NOT_ON_HUB, check-resit-page.py and the todo
  checklists are done by hand.

## 2026-10-07 (home, late night): F1 batch 3 BUILT, NOT YET A PR; STOPPED for Jon's context clear

- **State at the stop:** all 8 games and the handover are committed and pushed on `claude/f1-batch3` (worktree
  `E:/jon/mg-b3`). There is **no PR yet**. A local `check-changed.py` was running when Jon stopped the session,
  so its result is unknown. **Next session, before the new contract or after it as Jon says:** rerun
  `python scripts/check-changed.py` on the branch (rebase on main first). Open the PR with the body in `docs/handover/pr-b3-draft.md` (delete that file in the PR)
  . Set `status: fixed, pr: <n>` on the four entries named below, then merge on green (staggered from
  cloud merges).
- **#133 (contract LH) merged** on a green Gate, 22 min after the cloud lane's #130, with no cloud PR in CI.
  Main is green.
- **Batch 3, eight games on MaffsLock:** dimension-checker, curling-friction, trig-worms, component-crusher,
  differentiation-duel, integration-duel, spot-the-error and expectation-station. Each has its declaration;
  four needed a real one:
  - trig-worms: start_sel, because "FIRE!" is its Start.
  - component-crusher: a typed key + 1000 at the stated precision, or the first wrong option.
  - spot-the-error: picks a level, then the same wrong step twice.
  - expectation-station: wrong tiles, wrong products, then a wrong card still open.
  All 26 migrated games pass.
- **Faults fixed beyond swapping in the lock:**
  - spot-the-error: a double-click on a wrong step spent both attempts. A first wrong pick now opens a fresh
    window (stage 1 and stage 2).
  - expectation-station: each Check is one attempt (a double-click spent the retry, t2-017). The game's own
    Next was outside every container, so a second Enter skipped a question. `fresh(gameScreen)` on load.
- **Register:** closed component-crusher-t4-005, curling-friction-t5-003 and dimension-checker-t5-003 (all
  HIGH, class 1), and expectation-station-t2-017.
- **Verifiers:** each sweep that answers at once now has `bc.NO_LOCK_FRESH_INIT`. Two sweeps replace
  `window.setTimeout` (spot-the-error runs callbacks at once; expectation-station queues them with id 0), and
  that silently drops `MaffsLock.timer` callbacks: the asset records the id only after `setTimeout`
  returns. Both sweeps now override `MaffsLock.timer` the same way. expectation-station's sweep also calls
  `MaffsLock.fresh(stage3Wrap)` when it re-renders stage 3 by hand. **Lesson for the next batches:** any
  sweep that stubs setTimeout must stub `MaffsLock.timer` too.
- **Note, not a fault:** expectation-station shows "no Next after a wrong answer". A first wrong attempt
  resets the stage for a retry, so the classifier sees an auto-advance. Its stages keep the game's own Next.
- **NOT_YET: 70.**

## 2026-10-07 (home, night): contract LH, lock hints declared by each game (#133)

- **Jon's contract LH (before batch 3).** The root cause: per-game facts sat in a shared script, so each cloud
  migration needed a home-lane edit (suvat #128, factor-theorem #130). The fix is at that layer, the same
  shape as contract V.
  - **Declaration.** Each migrated game declares how the check produces a wrong answer in its own page: one
    `<!-- maffs-lock-hint` comment holding a JSON object (canon §7.6.0, answer-lock.js's header,
    `HINT_KEYS` in the script).
  - **Moved out of the script:** all 11 central hints (each reads back equal), plus suvat's from #130. The five games that needed
    none declare `{}`, and a declaration is now required. No per-game hint is left in the script.
- **The load-order rule is removed, and tested both ways in Chromium.**
  - factor-race, reversed (answer-lock.js first) and played through `--against`, passes every behaviour,
    including the double-click on MaffsNext.
  - suvat loads answer-lock.js first natively, and it passes.
  - No STOP IF.
- **The "reported, not failed" state now has an exit.**
  - A NOT_YET game whose page loads the lock is judged in full.
  - Its failures are reported only while it is on the `cloud-remaining:` line, which the home lane added to
    cloud.md's header at Jon's instruction (the one cross-lane edit; the cloud lane keeps it from now on). A
    missing or doubled line fails the check.
  - An off-list game that passes is noted for the home lane to add to MIGRATED.
  - `--selftest` (run in L1 before part 1) plants a page with no lock. In it `MaffsLock.lock` never refuses
    and there's no fresh window. It is played as an off-list adopter: CAUGHT (a question skip in the
    tap-through). On the list it is reported. Overriding `lock()` alone was not enough: decimal-detective
    replaces its Check button, so the plant had to remove the fresh window too.
- **suvat and factor-theorem are in MIGRATED and pass.** #130 merged while LH was in review. Its "hints as data"
  (cloud.md, Jon's 18:00 rulings) became factor-theorem's declaration, and factor-theorem came off the
  remaining list, which is now eigenvector-engine, truth-will-set-you-free, trig-identity-duel,
  binomial-blaster, partial-fractions-duel and truth-buster. #130 had already swapped suvat's script order;
  the merge keeps main's order and the declaration. All 18 migrated games pass both parts.
- **CI selection.** The script no longer names any game, so `ci-deps.py` marks it ALWAYS: it runs on every PR,
  cloud-lane game PRs included. Before, a game PR selected it only through the slugs in HINTS/CLOUD_LANE, so
  factor-race, formula-plug-in and others were never selected by their own changes.
- **Register (item 5).** §7.6.1 says the reason and Next both sit above the fold, so these are MEDIUM
  (`NEW:phone-layout`, open):
  - factor-race-f1-001: reason 648-680 and Next 691-735; the fold is 528.
  - fraction-equivalence-f1-001: Next 534-578. Its reason, 477-501, is above the fold, so the entry says so.
  - percentage-flip-f1-001: below the fold from the top of the page. But the page scrolls itself 346px as
    the answer box takes focus, so in the run both were on screen.
- **For the cloud lane:** each queued game (eigenvector-engine first) declares its maffs-lock-hint in its own
  page and comes off `cloud-remaining:` in the PR that finishes it.
  - factor-theorem's open note (moving to MaffsNext needs `FT_STEP` in check-teacher-invite.py taught first) is home-lane
    work, not yet queued.

## 2026-10-07 (home, night): F1 batches 1 (#129) and 2 (#132) merged; CHECKPOINT STOP (2 batches)

- **#129 (batch 1) merged.** Of the three local failures, two were environmental and fail on main too:
  Negative Number Line's 320px fold (fonts) and Test the Claim (no Node on this machine, `FileNotFoundError`).
  **check-resit-fixes.py was a real break** (Shape Shifter and NNL). Its clicks landed in MaffsLock's 300 ms
  window, and it reset an `answered` flag the games no longer have. It now uses `bc.NO_LOCK_FRESH_INIT` and calls
  `MaffsLock.fresh(gameEl)`; its self-test still catches every reverted fix. Closed: formula-plug-in-t3-001,
  new-shapes-t3-001, four-quadrant-explorer-t3-001, like-terms-collector-t3-002. shape-shifter-t3-005 has its
  fixed part noted.
- **Main went red after #129 (#131 fixed it).** The cloud lane's #128 put suvat on answer-lock.js while
  check-answer-lock (new in #129) still had it on NOT_YET, and the "stale" rule failed it. Both PRs were green
  alone. Now a CLOUD_LANE game that loads the lock is a note, not a failure, and the home lane moves it to
  MIGRATED once it passes. **suvat does not pass yet, and it is the cloud lane's game:** it loads answer-lock.js
  before next-control.js, and the driver needs a HINT to produce a wrong answer. factor-theorem (#130, open)
  will be in the same position.
- **#132 (batch 2) adds two things, on Jon's order.**
  - **(a) MaffsNext on a wrong answer (canon §7.6)** for factor-race, fraction-equivalence and percentage-flip,
    on wrong answers and time-outs. Two of the games needed a call on what counts as the wrong path:
    - prime-factorisation: a wrong tap that leaves lives never moved on, so Next goes on the last life. It
      shows the whole factorisation, then Game Over.
    - equatle: a wrong guess is the next row of the same puzzle, so Next goes on a lost puzzle. It shows the
      equation, then the results.
  - **(b) Equatle :337 restored.** The links pasted into the button's onclick now sit under the buttons, with
    the teacher line after them, outside the `.mf` flex row (check-teacher-invite required this).
  - Closed: prime-or-composite-t1-001 (HIGH) and percentage-flip-r-001. factor-race-t3-004 has its fixed part
    noted.
- **NOT_YET: 80** (73 home + 7 cloud). 16 games migrated.
- **For Jon:**
  - **Phone rule:** at 320×568, Next is below the fold on factor-race, fraction-equivalence and percentage-flip.
    Their answer controls are already below the fold on main (`measure-phone-fit.py`), so this is phone-fit
    work, not F1. Not queued.
  - **check-teacher-invite.py** drives Log Laws through its global `answered`. Fix that when log-laws migrates.
  - **Equatle and Prime Factorisation:** the reading of "wrong path" above is mine, so overrule it if needed.
- **Lessons:**
  - `measure-phone-fit.py --only X` rewrites `docs/phone-fit-report.md`. Restore the file afterwards.
  - A one-off wrong-path script must click Next with `force` or `dispatch_event` during the floor. A plain
    `click()` waits for Next to enable, and a raw coordinate click can land on the fixed footer.
  - Heredocs still eat `\'`: use Edit or Write for those.
- **Next session:** read the QUEUE above and start batch 3 (re-read `docs/handover/cloud.md` first).

## 2026-10-07 (home, evening): F1 batches 1 and 2 built; PAUSED for a context clear (Jon, at 55%)

- **#125 (F1 part a, MaffsLock) MERGED** on a green Gate. Its group E run failed once on a 1px fold in Simultaneous
  Solver (320x568, s4_01: 529 vs 528) and passed on rerun: flaky, not this change.
- **Jon's F1 checkpoint rule (7 Oct):** after the shared lock PR, stop after every 2 roll-out batches (each merged,
  main green); at each stop update this file (batches, PRs, NOT_YET, next batch, lessons) and stop. Also stop at the
  next batch boundary when Jon says "checkpoint".
- **STATE AT THE PAUSE:** both branches pushed (after GitHub returned "Internal Server Error" on push three times
  at 17:00; the fourth went through). No PR open for either yet.
  - `claude/f1-batch1` in worktree `E:/jon/mg-b1` (rebased on main after #125): batch 1 + check-answer-lock.py.
  - `claude/f1-batch2` in worktree `E:/jon/mg-b2` (stacked on batch 1, not yet rebased).
- **NEXT SESSION, in order:** (1) open the PR for `claude/f1-batch1` (body drafted: games, faults fixed, check);
  run `python scripts/close_entries`-style edit: set status fixed + pr on formula-plug-in-t3-001, new-shapes-t3-001,
  four-quadrant-explorer-t3-001, like-terms-collector-t3-002 (shape-shifter-t3-005 stays open: bundle; note its
  class-1 part fixed). (2) Local check-changed on batch 1: 82 ok, 3 FAILED: Negative Number Line (320px fold, also
  fails on main locally: fonts), **Test the Claim** and **Resit fixes** (not yet compared with main: check first;
  CI is the judge). (3) Merge on green, watch main. (4) Rebase batch 2, its PR, register entries, merge. (5) That is
  2 batches: STOP per Jon's rule.
- **Batch 1 (Year 6):** formula-plug-in, new-shapes, four-quadrant-explorer, like-terms-collector, shape-shifter,
  negative-number-line, think-of-a-number, decimal-detective.
- **Batch 2:** probability-pioneer (5 s Wait retries queued one per click: now one pending), prime-or-composite
  (P/C keys re-marked: fixed), factor-race, prime-factorisation, percentage-flip (Skip after Check skipped a second
  card: fixed), fraction-equivalence, equatle (one lock per guess, released at once; finish once), estimation-golf.
  All 16 pass check-answer-lock.py both parts locally (about 3 min per 8 games).
- **NOT_YET after batch 2:** 80 (73 home + 7 cloud). **Next batch 3 (KS3/GCSE):** 52dle, split-it,
  word-problem-decoder, equation-builder, spot-the-muppet, terrible-advice, wrong-on-the-internet, maths-court.
  Re-read docs/handover/cloud.md first: the cloud lane merged #124 (linear-equation-solver), #126 (moments-master),
  #127 (force-resolver) today.
- **Lessons (check-answer-lock.py):** the generic tier-3 driver needs per-game HINTS for most games (ready, answer,
  surface, start_sel, keys, each, mark_any, repeat); write the hint while migrating. Auto-advance games (no Next on
  a wrong answer: factor-race, fraction-equivalence, percentage-flip, prime-factorisation, equatle) are noted, not
  failed (canon 7.6's Next is logged for Jon, not F1's). `fresh()` must cover skip-marked Next buttons (fixed in
  #125 before merge). Verifiers that load and answer in one breath need `bc.NO_LOCK_FRESH_INIT`. Game-wide regex
  replacement of `answered` also hits CSS comments: check. Heredocs eat backslashes: write patch scripts with the
  Write tool (scratchpad mig_*.py / patch_cal*.py are this session's).
- **For Jon:** equatle :337 has a malformed `onclick="<div ...` (logged, not fixed, SR-9). STOP IF (c): 89 games to
  migrate, carrying on in batches.

## 2026-10-07 (home): F1 part a, the MaffsLock asset (#125)

- **#123 (0d, Given That) merged** on a green Gate after main's rerun of #122 went green. Main's first runs
  after #121 and #122 were marked failed with every job green: the run never created its Gate job (the two
  pushes were 5 s apart). A rerun of #122's run created it: green.
- **F1 (Jon, 7 Oct):** one shared lock every game uses, so no click, key, double-click or double-tap marks
  twice, answers unseen, or finishes twice; then roll it out (no game keeps a local guard) and relist every
  unlisted game that is ready (SR-21: verifier merged, no open CRITICAL/HIGH). Do not touch scoring, keys,
  banks, MaffsAnswer/Options/Keypad internals, or the cloud lane's remaining games
  (linear-equation-solver, moments-master, force-resolver, suvat, factor-theorem, eigenvector-engine,
  truth-will-set-you-free: it adopts the lock itself). STOP IF a game cannot adopt it without a scoring change,
  or a CRITICAL/HIGH game would have to be relisted.
- **Count (STOP IF c, reported, carrying on):** 96 roster games record question_answered; 7 are the cloud
  lane's, so **89 to migrate** here, in batches of 8 by audience (Year 6 first).
- **This PR:** `schools/assets/answer-lock.js` (MaffsLock: `lock`, `isLocked`, `fresh`, `screen`, `timer`,
  `cancel`, `clearTimers`, `finishOnce`, `newSession`; header documents it); MaffsNext's advance calls
  `MaffsLock.clearTimers()`; canon §7.6.0 ("every game marks through MaffsLock; no local answered flags");
  `scripts/test-answer-lock.py` (B3 by ci-line): nine behaviours on a fixture game in Chromium, and the four
  planted faults (CSS-only lock, no fresh delay, uncleared timers, double finish) each caught. `isLocked()` is
  an addition to the contract's API: a keypad that must stop typing, or an Enter that must advance rather
  than mark, asks it instead of keeping a flag.
- **Next (part b):** `scripts/check-answer-lock.py` with batch 1 (the Year 6 games: formula-plug-in,
  new-shapes, four-quadrant-explorer, like-terms-collector, shape-shifter, negative-number-line,
  think-of-a-number, decimal-detective). Drafted on the f1 worktree (stashed): a generic driver on check-site's
  tier 3 probes; on main's formula-plug-in it already finds the double finish (game_completed x2, submitScore x2).

## 2026-10-07 (home): queue item 0d, shared fraction answers (#122) and Given That (#123)

- **#121 (0c) and #122 merged** on green Gates. Slip: #122 merged while main's run for #121 was still in
  progress (both green as PRs, disjoint files); both main runs watched to the end.
- **#122, shared:** `MaffsAnswer.fraction(raw)` (exact a/b, signs, whole numbers, lowest terms) and
  `fractionOrDecimal(raw, num, den, dp)` (a slash: exact, right or wrong, never 'format'; else the unchanged
  `decimal()` against num/den rounded half up in integers). `message()` gains `{sf}` and `{fraction}`.
  test-answer-js.py 68 to 125 cases; canon §7.1.3.
- **This PR, Given That:** each free-entry question ends "Give your answer as a fraction, or as a decimal to 3
  significant figures." (marked at dpFor()'s places, as before); placeholder "e.g. 3/7 or 0.429"; the exact key
  comes from answerDisplay (`exactOf()`), `keyAt()` gone. The verifier types every key as a fraction (lowest
  terms and x3), every other diagram ratio as a fraction (wrong), and on the 3/7 items 3/7 and 0.429 right, 0.43
  wrong; new plant r-004 (decimals only). Against main's page it fails on every fraction.
- **Register:** no open entry covered it (r-002/r-003 closed in #114), so r-004 (MEDIUM, class 7: fractions
  unreadable since #114) is filed and closed here.

## 2026-10-07 (home): queue item 0c, canon SR-22 and SR-23 (docs only, #121)

- **#120 (0b) merged** on a green Gate.
- **Numbering (decision taken, for Jon to see):** Jon called the leaderboard ruling "R15", but §0.3 numbers by SR-n
  and F1 names its relist rule SR-21. So SR-21 is reserved for F1 (a placeholder row), the leaderboard ruling is
  **SR-22** (its source column says "his ruling R15") and the timer ruling **SR-23**.
- **SR-22:** one board per mode or session length; Prime Sprint's board key on the hub; Prisoner's Dilemma ranks
  the tournament total only. proof-builder-t5-023 and prisoners-dilemma-t4-001 set `jc: false` (ruled), still open:
  the code is not changed (new level keys in `firebase-leaderboard.js` and the hub: shared code, home lane, not yet
  queued). Prime Sprint has no register entry.
- **SR-23:** timer-policy's Hidden Count-Up applies; Trig Identity Duel and Glorious Gantt follow it (both already
  listed there; a dated note added). trig-identity-duel-t2-010 and the timer part of glorious-gantt's :783/:968
  entry stay open until their code changes (TID is the cloud lane's game; Gantt is unlisted).

## 2026-10-07 (home): queue item 0b, regex .test() guards in bank_common (#120)

- **Jon's new queue (7 Oct, after the clear):** 0b this; 0c canon §0.3 R15 + the timer ruling (docs only);
  0d shared fraction answers (MaffsAnswer, then Given That); then F1 (MaffsLock, pasted).
- **0b:** `_SiteEval.call()`'s `.test` branch called `.search` on `regex()`'s `(pattern, glob)` tuple, so any
  render site guarded by `/re/.test(x)` crashed extraction (the cloud lane's note, #102/#105/#115). It now unpacks
  the tuple. `test-bank-common.py` gains REGEX_GUARDS: Proof Builder's `if (/[\\^_{}]/.test(q.a))` (in JS source) shape and
  Component Crusher's template-literal ternary; both raise on main, both pass now, and each guard is decided per
  value (`x^2` reaches KaTeX, `seven` does not). The cloud lane may go back to regex guards at render sites.

## 2026-10-07 (home): item 0, Like Terms Collector's flaky read (this PR); STOP for a clear before F1

- **Contract C is complete:** #111, #113, #114, #116, #117, #118 all merged on green Gates (#118's main run:
  watch it if not yet reported below). Contract V (#108) merged earlier.
- **Item 0 (Jon, 7 Oct):** `verify-like-terms-collector.py` failed once on main (run 37626794263, #109, attempt 1:
  "item 1: typed 8.9/6.5, marked correct=None") and passed on rerun. It read MARK() straight after
  `page.click('#checkBtn')`. Now `read_mark()` waits for the game's own mark to land (up to 5 s), and the in-page
  sweep polls the same way. New self-test: a copy whose showFeedback() marks 300 ms late; the waiting read must
  see every mark and a read straight off the click must see none. With the old immediate read put back, the
  self-test fails with main's exact message. Not traced: why the real page was ever late (the check no longer
  depends on it).
- **Then STOP (Jon):** he clears the session before contract F1. Next session: read this file and the memory's
  LATEST block; F1 starts when Jon pastes it.
- **Open for Jon (carried):** eigenvector-engine-f0-005 set jc: false (done in #108); the cloud lane's #112 and
  #115 already declare their verifiers by ci-line header, so V is working as intended. B3 now carries 11
  lines: check its time on the next full main run; re-record `scripts/ci-timings.json` with
  `python scripts/ci-groups.py --record-timings <run id>` if it grows.

## 2026-10-07 (home): contract C game 6, Estimation Golf (#118); contract C complete once it merges

- **#117 (Sequence Solver) merged.** Slip to note: the cloud lane merged #115 seconds before, and #117 went in
  while main's run for #115 was still in progress (not red, but not yet green, against "main green, then the
  next"). Both main runs were watched to the end.
- **#118:** level4[7] keyed 565.49 (r-001; choice recorded: the true value, not "use pi = 3.14"); alevel[1] states
  the forward difference and 3 d.p. and keys 27.009, hint reworked (r-002). `verify-estimation-golf.py` (B3). On
  main it failed on exactly r-001 and r-002. Open: r-003, r-004, r-005.
- **Contract C summary (#111, #113, #114, #116, #117, #118):** six verifiers, all in B3 by ci-line header. No
  verifier found a wrong key the register did not list, so no STOP IF. Value-equal option pairs fixed along the way
  and their ledger entries cleared: proportion-blaster x5, given-that x2, formula-unlocked x2 (+B2, B10),
  sequence-solver x1; plus formula-unlocked F4 (sqrt(u^2), not caught by B11). B3 now carries 11 lines; check its
  time on main's next full run (the timing file was recorded before contract C).
- **Item 0 (Jon, 7 Oct), ON HOLD, Jon to confirm:** Like Terms Collector flaked on main once since #89: run
  37626794263 (#109), attempt 1, group E: "item 1: typed 8.9/6.5, marked correct=None", passed on rerun.
  `None` means MARK() found the feedback panel unmarked straight after `page.click('#checkBtn')` (the real-UI path
  in play(), scripts/verify-like-terms-collector.py ~:153-156); the cause is not yet traced. Jon said this may
  belong to a contract he has not sent yet, so no fix has been started.
- **Queue after #118:** F1 (Jon pastes it); item 0 if Jon confirms.

## 2026-10-07 (home): contract C game 5, Sequence Solver (#117)

- **#116 (Formula Unlocked) merged** on a green Gate, main green after #114.
- **This PR:** alevel[49]'s "0.999..." replaced by 10 (r-001); gcse[6]'s B11 pair replaced by 3n + 7.
  `verify-sequence-solver.py` (B3) recomputes all 154 keys; on main it failed on exactly r-001 and the B11 pair: no
  other wrong key. r-002 and r-003 stay open.
- **Next:** game 6, Estimation Golf (committed locally on claude/c-estimation-golf in worktree ../mg-eg): :680
  keyed 565.49 (choice recorded: the true value, not "use pi = 3.14"), :663 states the forward difference and
  3 d.p. and keys 27.009.

## 2026-10-07 (home): contract C game 4, Formula Unlocked (#116)

- **#114 (Given That) merged** on a green Gate, main green after #113.
- **#116:** Q_ALEVEL[0]'s value-equal option replaced by named slips, override and duplicate dropped (r-001);
  value-equal wrong options replaced in Q_LEVEL4[10] (f0-001, closed), Q_GCSE[22] and Q_GCSE[23] (audit F3, F4:
  not register entries; F3 was a B11 ledger entry). `verify-formula-unlocked.py` (B3, SymPy). On main it failed on
  exactly those four items: every key satisfies its formula, no other wrong key.
- **Next:** game 5, Sequence Solver (r-001: "0.999..." beside 1; the replacement is 10, the sum taken with first
  term 9). Its B11 ledger pair (gcse[6] -3n + 10 = 10 - 3n) is fixed in the same PR. r-002 (raw TeX on screen) and
  r-003 (jc) stay open.

## 2026-10-07 (home): contract C game 3, Given That (#114)

- **#113 (Better Value) merged** on a green Gate, after main's run on the cloud lane's #112 (Dimension Checker,
  which declared its verifier by ci-line header: no workflow edit) was green.
- **#114:** alevel_18's Venn regions from its stored totals (r-001); free entry on `MaffsAnswer.decimal` with the
  precision stated on every free-entry question (r-002, r-003); F4/F5's value-equal options replaced, two B11
  ledger entries cleared. `verify-given-that.py` (B3) has a reviewed SPEC for all 180 keys. On main it failed on
  exactly r-001, r-002, r-003 and F4/F5: no other wrong key.
- **Decision taken (for Jon to see):** one precision for all free entry would not do. At 3 d.p. two small keys
  (core_06 0.0518, alevel_25 0.0297) round the same as another ratio on their own diagram, and a 4 d.p. stored
  value rounded again gives the wrong 3 d.p. key for 6/11 and 136/228 (the verifier caught both in my first
  version). So N keeps three significant figures: 3 d.p. from 0.1 up, 4 from 0.01, 5 below, stated per
  question; the two stored values carry more places. Fractions and percentages are no longer accepted (MaffsAnswer
  reads plain decimals): the placeholder says "e.g. 0.429".
- Not in scope, still open: audit F6 (no phase 1 explanation at the typed levels); Given That's typed answers are
  not yet on MaffsKeypad (canon 4.4 rollout).

## 2026-10-07 (home): contract C game 2, Better Value (#113)

- **#111 (Proportion Blaster) merged** on a green Gate (B3 ran its verifier by its header alone).
- **#113:** five Core conclusions corrected from the recomputed figures (r-001..r-005) and core_033's working put
  in pence (r-009, closed too: the verifier proves its equation solved to 425). core_009 needed its repayment
  stated (GBP 90.20/month, 8% APR effective over 24 months) to be answerable; the old key is now a wrong card,
  explained. `verify-better-value.py` (B3): every figure in a keyed card or explanation must be a given or a
  recomputed value at its printed precision. On main it failed on exactly r-001..r-005 and r-009: no other wrong
  figure in the 70 items. Open (jc: true): r-006, r-007, r-008.
- **Next:** game 3, Given That. Spec reviewed for all 180 keys (num/den by named quantity, Yes/No tables'
  headers pinned); plan: alevel_18's Venn regions from its stored totals (onlyB 15, neither 55), free entry on
  `MaffsAnswer.decimal` at 3 d.p. stated on every free-entry question, gcse_14/gcse_23 value-equal options
  replaced (audit F4/F5).

## 2026-10-07 (home): contract C game 1, Proportion Blaster (#111)

- **V (#108) merged** on a green Gate (51/51 content lines ran); main's full run after it: see the next entry.
- **Contract C (Jon, 7 Oct, revised):** audit batch 3, one game per PR, in order: proportion-blaster, better-value,
  given-that, formula-unlocked, sequence-solver, estimation-golf. Each: a verifier that recomputes every key
  (SR-4/SR-16 option checks, explanation figures), declaring its own ci-line; the game's register entries
  set fixed with the PR; other open entries the verifier proves are one-line data fixes may be closed too;
  shared-class entries (classes 1, 4, 5) stay open. STOP IF a verifier finds more wrong keys than the register
  lists (file them, stop) or a fix would change wording beyond the named item. Do not touch engines, scoring,
  levels, leaderboard keys, other games, estimation-golf's proximity scoring, or the workflow.
- **#111:** alevel[47] keyed 900/11 (r-001 fixed); F2-F5's value-equal wrong options replaced by named errors,
  five B11 ledger entries cleared; `verify-proportion-blaster.py` in B3. On main it failed on exactly r-001
  and F2-F5: no other wrong key. Not fixed (beyond the named items): gcse[16] and gcse[21] ask "Find x" from x^2
  without "positive" (SR-17); -5 is not offered, so nothing is mis-marked. Audit F6 (raw TeX in the context
  line) and F7 (no explanation, auto-advance) are not register entries and were left.
- **Next:** game 2, Better Value (r-001..r-005; r-009 too, since the verifier proves its explanation's equation
  solves to 425). Verifier drafted: every keyed and explanation figure must be a given or a recomputed value at
  its printed precision; on main it flags exactly r-001..r-005 and r-009.

## 2026-10-07 (home): contract V, verifiers declare their own CI group (#108)

- **Why:** each new verifier edited `.github/workflows/check-site.yml` (the cloud lane's #96, #97, #100-#102), two
  conflicted with home-lane PRs, and canon §7.8.2 and the cloud contract disagreed about it.
- **Headers:** every content script carries `# ci-line: <group> | <label> | <args>` (51 lines in 47 scripts,
  including `stats_common.py`, `uk_rates.py` and `check-resit-fixes.py`); `&&` in `<args>` runs the script again,
  so the C and D parts (`--part-selftest && --part 1`) and Fermi Lab / Screening Room (` && --selftest`) are
  expressed exactly. `verify-regression-rumble.py` carries `# ci-held:` (the HELD dict is gone). Optional
  `# ci-deps: <paths>` adds dependencies (none uses it yet: ci-deps.py had no per-verifier central rule to move).
- **`scripts/ci-groups.py`:** reads the headers; `GROUPS` holds the 12 groups' job names and timeouts (unchanged);
  the plan job writes the matrix (`groups` output) and the new `content` job runs `fromJSON` of it with the same
  container and steps as `check-site` (YAML anchors `check-container`, `check-steps`). Job names unchanged; the
  Gate needs `content` too, so nothing is hidden from it. Site-wide jobs stay static in the workflow.
- **Proof (item 5):** `ci-groups.py --compare <workflow>` ran in the plan job on the commit that still had the
  static lists. Its first run caught the cloud lane's Integration Duel line, merged to main minutes earlier (51 static
  lines, 50 from headers: DIFFERENT); after merging main and adding that header, 51 = 51, EQUAL. Then the lists
  were deleted.
- **Readers of the workflow moved to the headers:** `ci-deps.py` (checks + `# ci-deps:`), `check-changed.py` (via
  ci-deps), `audit-register.py` (which games have a verifier: without this, REGISTER.md would have said 97 of 97
  games have none), and the `--part-selftest`s of Just Pythag It, Bruv and Equation Builder ("CI runs every part").
- **`check-verifier-coverage.py`:** a verify-*.py with no ci-line and no ci-held fails; an unknown group fails; a
  verifier listed in the workflow, or declared AND listed, fails. Reports each group's check seconds from
  `scripts/ci-timings.json` (recorded from main's run 37625188261 after #107 by `ci-groups.py --record-timings`;
  B4 164s is the largest, setup excluded) and flags any over 240s.
- **Success proof:** throwaway PR #110 (based on this branch) added only `scripts/verify-zz-v-probe.py` with a
  `B3` ci-line: the plan selected just it, and B3 ran it (1 line run, 5 skipped; run 37626296241); closed and
  deleted. #108's own full run (CI changed, so everything): 51 of 51 content lines ran, Gate green, 4m39s.
- **The cloud lane merged twice while this was open** (#107 Integration Duel, #109 Curling Friction), each adding a
  workflow line; each time main was merged in, the verifier given its header, and `--compare` against main's
  workflow re-run: 52 = 52, EQUAL, before the merge.
- **For the cloud lane:** add the verifier's `# ci-line:` header in its own file; never edit the workflow for it.
  Canon §7.8.2 says so (the cloud handover is the cloud lane's to update).

## 2026-10-07 (home): queue item 2, every content job under 4 minutes

- Main's full run after #99 (before): D 5m23s, B2 4m33s (the cloud lane had added three verifiers to it),
  C3 4m04s, C2 3m57s, A 3m34s, B1 3m32s.
- **D:** `verify-equation-builder.py --part i/n` splits by candidate arrangement, not by question: eb_ks3_012 alone
  has 31,032 candidates and is 60% of the time. Whole-question checks run in part 1; the planted-fault self-test now
  also runs each fault through both parts and requires them to fail exactly where the whole run does;
  `--part-selftest` proves every candidate is in one part. Locally: 121 s and 124 s against 185 s whole.
- **C:** four parts (C4 added); **B:** four groups, cut by the slowest time each line has taken on main (runners vary up to 1.8x: Log Laws 30-55 s, Growth and Decay 58-93 s). Timeouts 6-8 min (budget 75%). 19 matrix entries now (was 16): more runner pressure when both lanes run.
- Canon §7.8.1: no content job past 4 minutes; a new verifier goes where that holds.
- **After (#103's full run):** every job 3m38s or less (A 3m38s, B2 3m29s, C4 3m10s, C1-C3 2m50s-3m06s, B1/B3/B4 2m47s-2m50s,
  D1 1m56s, D2 2m03s); the whole run 4m47s (main after #99: 6m19s).
- **For Jon:** the cloud lane's #96, #97, #100 and #101 each edited `.github/workflows/check-site.yml` (adding their
  verifier to a B group). Canon §7.8.2 reserves the workflow for the home lane. It did no harm (the lines were
  needed and CI passed), but either the rule should allow "add my verifier's line to a content group" or the cloud
  lane should hand those lines to the home lane. Your call.

## 2026-10-07 (home): contract F0, B11 sees the value-equal shapes it skipped

- **Fixtures first:** `scripts/test-bank-common.py` (CI, Tier 4 layer A job), 13 equal pairs from the tranche 5-6 items
  (differentiation-duel :820/:848, binomial-blaster :134, force-resolver :118/:138, moments-master :180,
  eigenvector-engine :117/:128, complex-converter ids 21/40, boolean-blitz :584/:744, plus a Boolean distributive law)
  and 14 look-alikes that must stay unequal. All 13 failed on main's parser (commit 630ff40), all pass now.
- **`bank_common.py`:** `parse_value(raw, ctx)` / `value_equal_pairs(pool, ctx)` with `item_context(slug, q)`;
  juxtaposition, `\binom`, trig of constants in degrees, ≈ chains, SI prefixes, `vector`, `polar`, `bool` kinds
  (canon §7.1, the B11 paragraph). Exact throughout. `VECTOR_DIRECTION_GAMES` and `BOOLEAN_GAMES` tag the two games
  whose ask is in code, not in the item.
- **First run: 42 new pairs in 9 games** (eigenvector-engine 11, boolean-blitz 10, complex-converter 8,
  differentiation-duel 5, force-resolver 4, formula-unlocked, log-laws, moments-master, binomial-blaster 1 each).
  28 were already in the register: each ledger entry carries `"register": "<id>"`. 14 are new findings
  `<slug>-f0-NNN` (eigenvector-engine 7, boolean-blitz 4, force-resolver, formula-unlocked, log-laws 1 each;
  log-laws had no register file, so F0 opened one, its `audited` entry saying it is a B11 run, not an audit).
  Two misreads found on the way and fixed with fixtures: "vs" read as v·s; "1! = 1" read as a value.
- `check-banks.py --write-ledger` now carries each entry's `register` link over (`keep_register_links`).
- Planted `12\cos 90° N` beside the key `0 N` in a scratch copy of force-resolver's bank: `--ci` fails on it as NEW.

## 2026-10-07 (home): CI split for speed + two lanes (#95, merged); NEXT = contract F0

**State of play.**
- main `a041590` (#94) green before this PR. Build freeze in force (canon §0.2).
- Done today: the tranche 3-6 contract (#87-#90: 18 games unlisted, the freeze, the findings register) and the
  quoted-figures contract (#91-#94: Fermi Lab, Screening Room, Core Maths Paper 1 CPI, `check-quoted-figures.py`).
  The detail is in CLAUDE.md's last two "Handover" sections (7 Oct), the history this file replaces.
- **This PR (CI + two lanes):**
  - `check-site.py --shard i/n` and `--shard-selftest n`: tier 1 runs as four shards; tier 2 and the parts that
    cannot be split run in shard 1 only. The site-wide checks are their own job.
  - Tier 4 layer A and the shared-asset tests are separate jobs; group B is B1 + B2.
  - `verify-just-pythag-it-bruv.py --part 1|2|3` and `--part-selftest`: C1, C2, C3. (The contract named two parts,
    phone and desktop; measured, the heavier half would still have taken about 5.8 minutes as a job, which leaves
    no room under the 7-minute target for main, so it is three parts dealt by measured cost.)
  - REGISTER.md is no longer edited by PRs: `audit-register.py --check` validates the yml files only; the
    `register` job regenerates and commits it on main after the Gate (canon §0.4).
  - Handover by lane (this file and `cloud.md`); CLAUDE.md's opening block is a fixed pointer; canon §7.8.1-§7.8.2.
- **Before/after timings** (canon §7.8.1): full run 10m42s -> 5m45s; site-wide critical path 6m34s -> 3m03s
  (Tier 4 layer A); shards 1m40s-2m18s at --workers 4 on 4 CPUs (not the critical path, so more workers were not
  tried). Still over 4 min as single verifiers: Equation Builder (D, 4m48s) and B1 (4m51s); a PR touching those
  games waits on them. Split them next if it matters (Equation Builder needs a --part like JPIB's).
- Planted page error in `parents/fractions` (a shard-3 page) on a throwaway branch: only shard 3 failed, Gate red.

**Next.**
1. Watch this PR's merge run on main: every job green, and the `register` job either commits
   `Regenerate REGISTER.md [skip ci]` or reports "unchanged". (It should commit: the generated header's wording
   changed in this PR, and REGISTER.md was deliberately left unregenerated here.)
2. **Contract F0** (Jon pasted it 7 Oct: B11 value comparison in bank_common.py; START only after this PR is merged and main is green), then contract C (audit batch 3) when Jon pastes it.

**Gotchas learned today.**
- On the GitHub runner the "Content verifiers" jobs still pull the Playwright image even when the plan selects
  nothing for them (about 40 seconds each), so every matrix entry costs a runner briefly on every PR. A PR run is
  now 19 jobs (16 in the matrix, was 9); two PRs at once ask for up to 38 of the 20 runners a public repo gets,
  so some jobs wait for the short skipped ones to finish. Watch for it before adding more entries.
- A flake seen once on #92's run: Simultaneous Solver at 320x568, keypad 1px. Not reproduced since.
