# Handover: home lane

**FACTS-AND-NOTICE (13 and 14 Oct, Jon's contract and its 14 Oct revision; branch `claude/facts-and-notice`).** **Done:** (A) the 20 corrected weekly facts in `index.html` `FACTS` (A1-A6 and A7-A20 as worded in the contract; FACTS order, the anchor date and every other fact untouched; the three entries removed from `KNOWN` in `check-content-safety.py`, so 'SR-14 fields' is True). One punctuation change of mine: A19 replaces from "— about 460 billion", so I wrote "grains. At roughly 50 mg…" (a full stop in place of the dash) to keep the sentence break. (B) `scripts/verify-facts.py` (CI-wired: ci-line plus `ci-deps: index.html`): 52 facts, about 140 pins, each a regex over the fact's words whose captured figures are recomputed (52!, 5 × 10²⁸ = 117 billion people × seconds since the Big Bang, √(2 ln 2 · 52!) ≈ 10³⁴ and its ratio, 8x³ − 6x − 1 at cos 20° with no rational root, (2⁶⁴ − 1) × 50 mg, 18/37 to the 26th, energy 10^(1.5 × 1.3), compound growth, the Collatz path, the Birthday and Small-Samples probabilities, ISBN-13 and Luhn digits) or sourced in the script where nothing can be computed; a pin with neither fails; a title, count or order change fails (`fact_index` stays stable). Self-test plants a wrong figure (90 → 22), a wrong year (1998 → 1999), a changed pinned phrase and a literal modulus. (C) `getWeekIndex()` uses `% FACTS.length`; the verifier fails on a literal modulus or a changed anchor. (D) Glorious Gantt carries `<!-- maffs-correction-notice -->` and the banner text from the contract (checked visible with no sideways scroll at 320 px and 1280 px); `audit-register.py` fails if a game unlisted for faults lacks the marker or a listed game carries it (two plants in its self-test). (E) `GATE_EXCLUDED` for glorious-gantt covers points 1, 2, 3 and 5 with the contract's reason; canon §0.2 updated to match; 'answer lock' now waits on characteristic-quest alone (the cloud lane's). (F) see the result line at the end of this entry.
**For Jon (findings outside A, not fixed; the contract says list, do not reword):** (1) **Fact 14, "98% Accurate Doesn't Mean What You Think":** the hook says a "98% accurate" test can be wrong "more than 90% of the time", but the body computes 199 false of 248 positives = 80%. True value 80% for those inputs (a prevalence near 0.2% would give 90%). Carried as a KNOWN pin in `verify-facts.py`, which fails once it is fixed, so the pin is removed with the fix. (2) **Softer, sourced but worth a look:** fact 43 Basel "a 28-year-old Euler proved this" (born April 1707; solved 1734 aged 27, announced 1735, so 27 or 28 depending on the date); fact 51 "argued about this for 2,500 years" is a round figure; fact 33 "almost certainly score lower" overstates (the expected score is lower; an individual can still score higher); fact 36 still says compass and straightedge "can only produce square roots" beside the new cubic, which is correct (constructible numbers are built from square roots) but reads oddly next to a cubic. (3) The Erdős quotation in fact 20 is the documented variant ("not yet ready"); Guy's wording is "may not be ready". (4) A8's 5 × 10²⁸ rests on about 117 billion people ever born (Population Reference Bureau, 2022); estimates run 100 to 117 billion, and the argument holds across that range. **F (confirmation run, 14 Oct):** `check-changed.py` on a clean `origin/main` (d1b23bc) over the 70 files changed by #355 to #358 (REGISTER.md left out, CI regenerates it): 157 checks in 3,598 s; **no genuine failure.** Five reported failures, all environmental: Answer lock in play parts 1, 5 and 6 and Force Resolver failed under load ("MaffsLock undefined" at start; the usual local load flake) and **pass when run alone** (parts 1, 5, 6, the answer-lock self-test, and Force Resolver twice); Test the Claim fails on that checkout only because it has no LF rule yet (the Windows CRLF problem, PR #373). **A second cause of Test the Claim's local failure, not fixed because Jon ruled it be fixed at the repo layer and not in that verifier:** `scripts/verify-test-the-claim.py:1020` writes its mutated temp page with `NamedTemporaryFile('w')`, which converts to CRLF on Windows, so its newline-brace-newline slicing finds nothing; adding `newline=''` there makes it pass (tried and reverted). Jon: say if you want that one-word change. **Main after #373:** run 38520053624 failed only in the main-only job `CI timings and pack`, not in any check: Probability Paradox ran 203 s against a recorded 161 s, so Content verifiers 20 sat at 82% of its budget (the pack fails above 80%) and nothing was committed; a re-run of the job gave the same result. The next main run re-times it.

**LEVEL-LOGGED (13 Oct, Jon's contract and rulings; branch `claude/level-logged`, triage rule R10).** New `scripts/check-level-logged.py` (CI-wired by its ci-line; one plant plus six cases): no `mfg(...)` call in `games/` or `escape-rooms/` carries a literal `level`; `'all'` passes only where the game's `MaffsLevel.resolve` lists `'all'` in `boards` (52dle, equatle, prime-or-composite, truth-buster, bearing-blitz keep logging it). Each game captures the resolver result as `resolvedLevel`; the leaderboard and score-history keys are untouched (SR-29). **Fixed (25): ** boolean-blitz, circle-theorem-spotter, constructions-lab, core-maths-paper1, core-maths-paper2a, core-maths-paper2b, core-maths-paper2c, dimension-checker, eigenvalue-extractor, eigenvector-engine, factor-theorem, index-laws, like-terms-collector, modular-battle, normal-navigator, partial-fractions-duel, probability-paradox, quadratic-factoriser (its four 'higher'/'formula' literals now `currentLevel`; Chromium proved each equals `currentLevel` in every mode first), shape-shifter, tax-theft, test-the-claim, think-of-a-number, trig-wars, trig-worms, truth-will-set-you-free. **GA4 and Sheets level data from before this merge is unreliable for every game above** (single-level games logged the right value; the multi-level ones, i.e. constructions-lab, eigenvalue-extractor, eigenvector-engine, index-laws, normal-navigator, partial-fractions-duel, probability-paradox, test-the-claim, trig-wars, trig-worms, logged one fixed level whatever was played). Also in `.claude/rules/analytics.md`. **Open:** characteristic-quest is on the check's NOT_YET (reported, may only shrink): the cloud lane fixes it in its SWEEP-1-RULINGS PR (with R7) after #359 and removes it from NOT_YET there. Closed eigenvector-engine-s1-004 and normal-navigator-s1-007; new LOW normal-navigator-s1-009 (page says use a calculator, roster untagged) for Jon's tagging decision.

**ESCAPE-SET-CHECKS (11 Oct, Jon's contract; branch `claude/escape-set-checks`).** The per-set checks moved out
of `gen-escape-variants.py` into **`scripts/escape_set_checks.py`** (pure, no I/O), unchanged: keep()'s tests ->
`check_set()`; each lock's instrument, clue figures and solver -> `LOCKS` (35 entries, lifted by an AST script,
not retyped); rugby-scoreboard-bases and cookie-price-simultaneous (two instruments, checked inline before) ->
`check_rugby_bases()` / `check_cookie_simultaneous()`, which read the answer and misconception from the set as
served (the generator builds them from the same parameters, so its test is unchanged; CI's is stronger). The
generator imports it, keeps only search + spread, and writes to this checkout (the E:\jon\maffsgames paths are
gone). **Regeneration is byte-identical:** sha256 of variants.json and all 12 room.js equal before and after,
and the generator's whole report too (299 sets, 37 locks, 2763 rejected). `check-escape-rooms.py` runs
`check()` on every set of every live room (names room, lock, set index, check; a live lock missing from LOCKS
fails), prints per-room verified sets and the total (11 Oct: 271 in 11 rooms, none failing; it-vengeance
withdrawn, not checked), and plants the 10 broken sets in `scripts/fixtures/escape-broken-sets.json` (each of
the 7 per-set checks, both two-instrument checks, an unregistered lock; every good original must pass).
Mutation proof: with the clue test disabled the run fails, naming the uncaught plant. CLAUDE.md: new "Start of
task" (fetch, new worktree from origin/main, never pull into the primary or an existing branch). Canon §11.3
replay bullet rewritten: no figures. **Not changed, for Jon:** the ci-line label (it keys ci-pack.json and
ci-timings.json); §11.3's "Ratings as of 10 Oct" (no Rightful King ★★★ or Library Jam ★) and "The live rooms
all use `digits`" (both new rooms are live; maxDigits), stale; §11.4's rows for both scripts predate this.

**Canon sweep (read-only; current-state counts derived from repo content; none changed).** Intro "What is
authoritative where": roster "has all 93 rows". §Portal: "`escape-rooms` (12 items)". §3.2: "135 `.game-card`
elements for 96 games". §7.5: "On 2 Oct 2026 the roster gives 67 games light and 30 dark" (dated). §8.2c and
the shuffle note: "32 games hand-roll `shuffle(...)`", "the other ~30 games", "The other ~28 games". Coverage:
heading "(96 live games)"; "94 of the 96 live games call `submitScore()`" (recounted 3 Oct); "Not counted in
the 96 live games". Firebase/leaderboard: "Wired into 94 of the 96 live games". Tier 1: "125 controls across 47
games ... (122 across 46 ...)". Tier 3: "95 of 96 games fire `question_answered`"; "27 games use
`id="options"`, 8 use a class ... 60 use neither". §11.1: "Eleven rooms live, one withdrawn" and its 12-row
table (accurate today). §11.3: the ratings roster above. §11.4: `check-escape-rooms.py` "(two faults planted)"
(now three, plus the ten broken sets). §11.5: "All eight rooms are being rewritten" (eleven live now). Dated
audit history (e.g. "17 games" 22 Sep, "125 pages", the [x] backlog's "60 games") is history, not drift: left out.

**MG-PP-BEFORE (11 Oct, Jon's contract; read-only).** Worktree unchanged since the WORKTREE-CLEANUP entry
(detached at a02d61d, the same two files, nothing else). **Both edits are already in main, byte for byte**
(same git blob): `scripts/check-changed.py` is main's as landed by PREPUSH-SCOPE (6192382, two queues), and
`scripts/test-escape-keypad.py`'s one-line ci-deps change (`kiln-disaster/room.js` -> `escape-rooms/`) is
2414310. Nothing in main relies on their absence. **Recommendation: discard** (nothing to keep): Jon runs
`git -C E:/jon/mg-pp-before checkout -- .`, then `git worktree remove E:/jon/mg-pp-before`.

**WORKTREE-CLEANUP (11 Oct, Jon's contract; branch `claude/worktree-cleanup`).** `git worktree list` found 35
beside the primary. Each checked: branch tip an ancestor of origin/main, `status --porcelain` empty, no commit
outside origin. New end-of-task step in CLAUDE.md (Task Contract): remove the task's worktree and local branch
after merge, never `--force` / `-D`. Remote branches untouched. Every worktree found (all E:/jon/):

| Worktree (branch `claude/…`) | Status | Action |
|---|---|---|
| mg-b1..b6, mg-b8 (f1-batch1..6, f1-batch8); mg-cib (ci-balance); mg-cp (checkpoint-8oct); mg-ctx (ctx); mg-cu (changed-utf8); mg-ea (escape-analytics); mg-ess (essentials); mg-ew (essentials-wording); mg-frac (answer-fraction); mg-ga (ga4-country-canon); mg-ga2 (gitattributes-bytes); mg-gs (graph-sketcher-fit); mg-gt (given-that-fractions); mg-hints (f1-lock-hints); mg-lf (ltc-focus-race); mg-lj (library-jam-art); mg-log (log-notation); mg-ltc (ltc-flake); mg-r3 (relist-3); mg-r9 (rulings-9oct); mg-rel (rooms-release-rk-lj); mg-rk (rightful-king-art); mg-rl (relist-sr21); mg-upd (updates); mg-vs (vocab-showthat) | merged, clean, pushed | removed; branch deleted (`-d`) |
| mg-b7 (f1-batch7), mg-lock (f1-answer-lock), mg-sk (star-key) | merged, clean, pushed | unregistered and branch deleted (`-d`), but Windows refused to delete the folder ("Permission denied"; still busy): **an empty folder is left at each**, held by some process. Jon: delete the three empty folders after a reboot |
| mg-pp-before (detached at a02d61d, ancestor of main) | **dirty**: `scripts/check-changed.py`, `scripts/test-escape-keypad.py` modified | **kept** (STOP IF: dirty). Jon: keep or discard those edits |

Also, the same session: the **CANON-VERIFIED-COUNT** contract (canon §11.3's "199 verified number sets") STOPPED
before any edit, reported to Jon in chat; nothing committed.


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
