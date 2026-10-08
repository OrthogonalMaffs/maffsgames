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
5. **F1 batch 7: DONE, #182 merged 8 Oct (259c143), main green. F1 batch 8: NOT STARTED** (Jon said "checkpoint" at
   the batch 7 boundary). Then F1 batch 8, exactly as the standing F1 item below states (8 per batch, Year 6/KS3/GCSE/
   Core first; read `cloud-remaining:` in `docs/handover/cloud.md` on main before building each batch and drop
   every game on it).
6. **CHECKPOINT after batch 8 merges with main green:** update this file and stop. Do not start batch 9 in that session.
7. **DOCS-SMALL: IN PROGRESS, branch `claude/docs-small` (9 Oct).** Was: first item next session (Jon, 8 Oct; sent for "after the batch 8 checkpoint", and the checkpoint came
   at batch 7, so it runs first next session, then batch 8). Verbatim below. (a) Roster
   convention: a generated game's row says "N per session, generated", a bank game's gives its bank size;
   just-pythag-it-bruv's row "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3
   generated)"; list other generator rows noticed. (b) /updates/ 8 Oct, Updated badge: "Correlation or Coincidence:
   now 84 questions, twice as many as before." STOP IF its bank on main is not 84, or the roster parser reads the count.
- **CHECKPOINT STOP (Jon, 8 Oct, late):** batch 7 merged, main green; this session stopped at that boundary.
- **MAIN-RED: DONE, #184 merged 8 Oct (f1a097d), main green** (see its entry).
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item:** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty
  (NOT_YET: 31). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
  `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
  line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

<details><summary>Queue item 7 (DOCS-SMALL), verbatim (Jon, 8 Oct)</summary>

> TASK (home lane, DOCS-SMALL; first item next session, after the batch 8 checkpoint): Two docs fixes from 8 Oct 2026,
> in one docs PR.
> ROOT CAUSE: (a) The roster row for just-pythag-it-bruv says "20 questions in three rounds". Project Claude read that
> as a 20-item bank and wrongly told Jon the game was below the 40-50 minimum. The game generates every question each
> session (15 triples with sizes, orientation and side varied in round 1; fresh non-square lengths in round 2; five
> contexts with large number pools in round 3), so 20 is the session length, not the bank. (b) correlation-or-
> coincidence's bank went from 42 to 84 items on 8 Oct (cloud lane, Jon's contract), with no /updates/ entry. Twice
> the questions is a change a returning student notices in what they meet, so it earns the Updated badge under canon
> §3.4.
> CLASS CHECK: (a) is an instance of a pattern: a roster count that does not say whether it is a bank or a session.
> Fix it at the roster's convention. Canon or the roster's header states that a generated game's row says "N per
> session, generated", and a bank game's row gives its bank size. Apply that to just-pythag-it-bruv, and to any other
> generator rows you find while editing. Do not audit every row in this PR; list any you notice. (b) is local: one
> missing entry.
> EXACT CHANGE: 1. .claude/rules/game-roster.md: add the convention line to the roster's header notes.
> just-pythag-it-bruv's row says "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3
> generated)". Keep the rest of the row. 2. /updates/, a new entry dated 8 Oct, Updated badge: "Correlation or
> Coincidence: now 84 questions, twice as many as before." If an 8 Oct entry already exists, add the line to it.
> 3. docs/handover/home.md updated.
> DO NOT TOUCH: any game page; other roster rows' content, beyond rows you confirm are generators (list them in the
> PR; only change those if the change is just the count wording); canon §3.4.
> SUCCESS CONDITION: the roster checks pass; /updates/ shows the line with the badge; merged on a green Gate; main
> green; handover current.
> STOP IF: correlation-or-coincidence's bank on main is not 84 (report the count, and don't write the line); the
> roster parser reads the count field so that new wording breaks it.

</details>

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-09 (home): DOCS-SMALL (branch `claude/docs-small`)

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

