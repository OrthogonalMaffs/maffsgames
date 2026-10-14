# Handover: home lane

**FACTS-33-20 (14 Oct, Jon's contract; branch `claude/facts-33-20`).** Closes the two facts FACTS-SIX-FIXES held. `verify-facts.py` passes, zero KNOWN, self-test plants unchanged and all caught. FACTS order, length and `getWeekIndex()` untouched.
- **Fact 33, Regression to the Mean.** Hook, old: "If a student scores 98% on a test, they'll almost certainly score lower next time — not because they got worse, but because of statistics." New: "If a student gets an unusually high score on a test, expect their next one to be lower — not because they got worse, but because of statistics." Body, old: "The instructors' feedback was irrelevant." New: "Regression alone explains the pattern, so the instructors had no evidence that their feedback made any difference." Pins: "Israeli flight instructors" kept; "gets an unusually high score on a test" and "Regression alone explains the pattern" added, sourced to Kahneman, Thinking, Fast and Slow ch. 17.
- **Fact 20, Collatz.** Old: `Paul Erdős said: "Mathematics is not yet ready for such problems."` New: `Paul Erdős is reported to have said: "Mathematics is not yet ready for such problems."` (quoted words untouched). Pin sourced to J. C. Lagarias (1985), The 3x+1 problem and its generalizations, American Mathematical Monthly 92(1), 3-23; its text reads "is not yet ready", so the earlier "may not be ready" claim was the later form.
- **Absolute-language hooks, for Jon's review, none changed** (fact number is 0-indexed; words searched: always, never, almost certainly, guaranteed, impossible, every, no one): **3** Card Shuffles ("almost certainly… never existed… never will again"; a probability claim stated flat); **10** √2 ("every number is a ratio"; the Pythagorean belief, fine); **11** Hairy Ball ("impossible… always at least one cowlick"; true for a sphere, a theorem); **15** Infinitely Many Primes ("always a larger one"; theorem); **20** Collatz ("You will ALWAYS reach 1"; **an unproven conjecture stated as fact in the hook**, worth a look); **26** Infinite Hotel ("can always accommodate one more"; true in the standard setup); **29** Perfect Bracket ("every match… 1 in 9.2 quintillion"; a coin-flip assumption, see its body); **35** Königsberg ("impossible", theorem); **36** Trisect ("impossible", theorem); **39** P vs NP ("may be impossible", hedged); **44** Barcodes ("Every barcode has a check digit"; true of EAN/UPC/ISBN, not of every barcode symbology); **46** Hear a Drum ("not always"; accurate); **49** Matrices ("Every computer graphic, every 3D game, every GPS"; hyperbole). The likeliest to need rewording: 20, 44, 49, 3.

**TEXT-WRITES (14 Oct, Jon's contract; branch `claude/text-writes`).** **Done:** `newline=''` added to all **49** text-mode writes in `scripts/` (29 files; open 'w'/'a' ×30, `Path.write_text` ×15, `NamedTemporaryFile('w')` ×4; the four `Image.open`/`pymupdf.open` hits were false positives and are untouched). No shared helper, per the contract. New `scripts/check-text-writes.py` (CI-wired by header, `ci-deps: scripts/`) reads every `scripts/**/*.py` as a syntax tree and fails on a text-mode `open`/`io.open`/`Path.open`/`write_text`/temp-file write without `newline=`, or an `open()` whose mode is not a literal; it ignores binary modes, reads and non-file `.open`; 181 scripts, 0 violations; the self-test plants 9 offending writes, 6 clean ones and a bad/good file pair in a scratch `scripts/` folder. Newline-only change: no content or encoding argument touched, no byte difference on Linux (`newline=''` is the default there). `verify-test-the-claim.py`, `verify-split-it.py`, `verify-equation-builder.py` (selftest and part 1) and the answer-lock self-test pass on Windows. **The earlier repo-layer ruling (12 Oct: fix CRLF in `.gitattributes`, not in `verify-test-the-claim.py`) is rescinded by Jon, 14 Oct:** `.gitattributes` governs checkouts, not runtime writes, so it could only ever fix the first of the two causes. **Blind spots, not checked and not fixed:** (1) shell redirects (`>`, `>>`) in any command a script runs: `check-changed.py:149` runs CI lines with `shell=True`, and the workflow's own steps are outside `scripts/`; (2) `subprocess` calls given a file as `stdout=` (none found); (3) writes made by embedded Node or JS strings (`fs.writeFileSync` in the verifiers' drivers); (4) `Path.write_text` needs Python 3.10 or later for `newline=` (CI is newer).
**CI TIMINGS DIAGNOSIS (14 Oct, Jon's contract): already fixed at source by the cloud lane's #376; nothing to split.** Cause: #371 added four plants to `verify-probability-paradox.py`'s self-test, and each plant re-ran the whole `run()` including `next_once` (10 s of real MaffsLock timers), taking the verifier from about 161 s to about 203 s locally and 231 s. That was a slow path from added self-test work, not new checks. #376 runs `next_once` only for the real page and the t1-010 plant (all 16 plants still caught, no check dropped). Recorded Probability Paradox time is now 48 to 58 s across the last five main runs, and `CI timings and pack (main only)` has been green on every run since (38581861905 and the one before). I did not touch the budget, the 80% limit, the packer or any pack assignment, and I did not use `--part`.
**FACTS-SIX-FIXES (14 Oct, Jon's contract; branch `claude/facts-six-fixes`). Four of six done; two stopped on the contract's own STOP IF.** Changed in `index.html` (FACTS order and length untouched, `check-content-safety.py` KNOWN still empty), pins updated in `verify-facts.py` (139 pins, **zero KNOWN**, self-test still catches all four plants):
- **Fact 14 (hook):** "can still give wrong results more than 90% of the time" → "…about 80% of the time". Body unchanged (199/248 = 80%). KNOWN pin replaced by a recomputed pin on 80%.
- **Fact 43 (Basel):** "In 1735, a 28-year-old Euler proved this, stunning" → "In December 1735, Euler, then 28, announced a proof of this, stunning". Pin recomputes the age from his birth date (15 Apr 1707) to the 5 Dec 1735 announcement.
- **Fact 51:** "argued about this for 2,500 years" → "…for about 2,500 years".
- **Fact 3 (shuffles):** "that would be about 5 × 10²⁸ shuffles" → "…fewer than 10²⁹ shuffles". Pin is an upper bound checked at both 100 and 117 billion people. **One consequential change beyond the contract:** "around 200,000 times that whole exercise" → "more than 100,000 times…", because the ratio was computed from 5 × 10²⁸ and against a 10²⁹ bound only the lower figure is true (10³⁴ ÷ 10²⁹ ≥ 100,000).
- **STOPPED, fact 33 (Regression to the Mean), unchanged:** its body contains no figure, so there is nothing to support any softened claim (contract STOP IF). Needs a wording from Jon, or permission to add a worked figure.
- **STOPPED, fact 20 (Collatz), unchanged:** the Lagarias source does not confirm the contract's wording. Lagarias's 1985 text, as published on his own page (cecm.sfu.ca/organics/papers/lagarias), reads "Mathematics is not yet ready for such problems", which is what the fact already says bar the capital letters. "May not be ready" is a later form (Guy and later surveys). Per STOP IF I did not reword it. Options: leave as is and cite Lagarias 1985, or attribute it as reported ("Erdős is reported to have said…") with the 1985 words.

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
