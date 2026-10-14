# Handover: home lane

**FACTS-29-35-11-36-49 (14 Oct, Jon's contract; branch `claude/facts-29-35-11-36-49`).** `verify-facts.py` passes (149 pins), zero KNOWN, self-test plants unchanged and caught. Facts 3, 10, 15, 20, 26, 39, 44, 46, every other fact, FACTS order and length untouched.
- **29, Perfect Bracket (hook).** Old: "The probability of correctly predicting every match in an NCAA tournament is about 1 in 9.2 quintillion." New: "If every match were a coin flip, the probability of correctly predicting every match in an NCAA tournament would be about 1 in 9.2 quintillion." The body already uses 2^63 (63 games, 2 outcomes each); the existing recomputed pin on 2^63 ≈ 9.2 × 10^18 stays, plus a pin on the new condition.
- **35, Königsberg.** Hook, old: "…crossing each of its seven bridges exactly once — and invented graph theory." New: "…crossing each of its seven bridges, as they stood then, exactly once — and invented graph theory." (it was already past tense). Body, added after "no solution.": "Wartime bombing and rebuilding changed the bridges. Today's layout allows a walk crossing each bridge exactly once, though not one that finishes where it began." Source confirmed (Wikipedia, Seven Bridges of Königsberg): five bridges remain at the original sites, two nodes of degree 2 and two of degree 3, so an Eulerian path exists and a circuit does not; the pin recomputes that (degree sum 10 = 2 × 5, two odd nodes).
- **11, Hairy Ball: no change needed.** The hook and body speak only of a hairy sphere and the Earth; no head is implied. Left as is.
- **36, Trisect: no change needed.** The hook already says "trisecting a general angle with just a compass and straightedge is impossible — proved in 1837". Added only a pin on that phrase (Wantzel, 1837), beside the existing "proved in 1837" and cubic pins.
- **49, Matrices (body).** Old: "…this is how every pixel of every video game is calculated." New: "…this is how a 3D game works out where every object appears on screen." Pinned as a phrase.
**STALE-PROCESSES (14 Oct, Jon's contract; branch `claude/stale-procs`).** Cleanup only; no repo content touched. **Listed before killing** (PID, start, command, parent): **37168**, 5 Oct 20:24, `python E:\jon\maffsgames-new-clone\scripts\serve-stubbed.py 60131` (parent 35676 already dead); **7072**, 7 Oct 16:24, `python E:\jon\mg-lock\scripts\serve-stubbed.py 62173` (parent 18764 already dead); **3704**, 8 Oct 18:05, `python scripts/serve-stubbed.py 8792` (parent bash 19448 still alive); **380**, 10 Oct 17:49, `python -m http.server 8765` (parent bash 22416 still alive); **36888** with its Playwright `node.exe` **22708**, 12 Oct 23:30, `python scripts/test-level.py --run` (parent bash 2764; this was background task `brj7ba02w`). **Stopped:** tasks `brj7ba02w` (taking 36888, 22708 and bash 2764 with it) and `barjw6rq4` by TaskStop; `bdmdk98sn` was already gone. **Killed by PID:** 37168 and 7072, stub servers whose launching shells are dead and whose command lines point at local stubs, not live servers. **Left running, per the contract's STOP IF (their parent shells are alive, so I cannot confirm their sessions are closed):** 3704 (port 8792), 380 (port 8765, a plain static `http.server` that may be Jon's own preview). Jon: kill them if they are yours to drop (`taskkill /PID 3704 /PID 380`), or say so and I will. **wt-level-resolver:** `E:\jon\wt-level-resolver` was not a registered worktree and not a git repo: an empty directory (0 entries), the leftover target of the `cd` in task `brj7ba02w`; nothing to merge or lose; removed with `rmdir`. `wt-pd-tournament-board` is another empty-looking leftover in `E:\jon`, outside this contract and untouched. **Does `end-task.py` stop a session's background processes? No.** It runs only `git` and `gh` (merged PR, local tip equals the PR head, clean worktree), then removes the worktree and branch; it neither lists nor stops processes, which is why servers outlive their sessions (and a server holding a folder open makes the removal fail with "Permission denied"). The structural fix is a separate ruling.
**HOOKS-20-44-49 (14 Oct, Jon's contract; branch `claude/hooks-20-44-49`).** Three overstated hooks corrected (0-indexed; bodies, order, length, fact 3 and the nine other flagged hooks untouched). `verify-facts.py` passes, zero KNOWN, self-test plants unchanged and caught.
- **Fact 20, Collatz.** Old: "…Repeat. You will ALWAYS reach 1. Nobody knows why." New: "…Repeat. Every number anyone has ever tried reaches 1 — but nobody has proved they all do." The old closing "Nobody knows why." is dropped as redundant beside the new sentence (the only wording change beyond the contract's replacement). Pinned to Lagarias (1985), Amer. Math. Monthly 92(1).
- **Fact 44, Barcodes.** Old: "Every barcode has a check digit calculated using modular arithmetic…" New: "Every barcode on a shop product has a check digit calculated using modular arithmetic…" Pinned to GS1 General Specifications (EAN/UPC check digit mandatory; Code 39 optional). The body does not depend on the universal claim.
- **Fact 49, Matrices.** Old: "Every computer graphic, every 3D game, every GPS navigation uses matrix multiplication to rotate, scale, and transform objects in space." New: "3D games, computer graphics and GPS all run on matrices: matrix multiplication rotates, scales, and transforms objects in space." Pinned as a phrase. **Left for Jon:** fact 49's body still says "this is how every pixel of every video game is calculated", the same hyperbole one level down; bodies were out of scope.
- **Decision recorded (Jon, 14 Oct):** the 57 scripts with no shared import are not worth a shared import for the Python 3.10 guard (PYTHON-MIN); they are left unguarded.
**PYTHON-MIN (14 Oct, Jon's contract; branch `claude/python-min`).** `scripts/` require Python >= 3.10 (`Path.write_text(newline=)`, added in #390). **CI pin:** all three `actions/setup-python@v5` steps in `check-site.yml` already pin `python-version: "3.12"` explicitly, so nothing changed there and the version CI runs is unchanged. **Guard:** added to the shared module `scripts/bank_common.py` (`require_python()`, run at import; exits with "scripts/ require Python >= 3.10 (write_text newline=); this is Python X.Y"). **Coverage count:** of 181 scripts under `scripts/`, 120 import `bank_common`; 57 import no shared module at all and are not guarded (the other 4 import only `stats_common`, `uk_rates` or `escape_set_checks`); the contract's STOP IF (no shared module imported by most) was not met. **New `scripts/check-python-version.py`** (CI-wired, `ci-deps` on the workflows and `bank_common.py`): `--check` fails any `setup-python` step that is unpinned, floating (`3.x`) or below 3.10; `--selftest` monkeypatches `sys.version_info` to (3, 9) and confirms the guard exits naming 3.10, stays quiet at 3.10 and on the real interpreter, and that the workflow reader fails 3.9, `3.x` and unpinned steps. **Docs:** the minimum is stated in CLAUDE.md (Tech Stack), canon (checker tooling, beside the Playwright setup line) and the `check-text-writes.py` docstring beside its blind spots. **Not verifiable from here:** Jon's Linux Mint machine's Python version (this Windows machine runs 3.14.6); anything below 3.10 there now fails with the clear message from the 120 guarded scripts, and the 57 others would still hit the `TypeError`. Jon: say if a shared import (or a `sitecustomize`-style guard) is worth adding for those 57.
**FACTS-33-20 (14 Oct, Jon's contract; branch `claude/facts-33-20`).** Closes the two facts FACTS-SIX-FIXES held. `verify-facts.py` passes, zero KNOWN, self-test plants unchanged and all caught. FACTS order, length and `getWeekIndex()` untouched.
- **Fact 33, Regression to the Mean.** Hook, old: "If a student scores 98% on a test, they'll almost certainly score lower next time — not because they got worse, but because of statistics." New: "If a student gets an unusually high score on a test, expect their next one to be lower — not because they got worse, but because of statistics." Body, old: "The instructors' feedback was irrelevant." New: "Regression alone explains the pattern, so the instructors had no evidence that their feedback made any difference." Pins: "Israeli flight instructors" kept; "gets an unusually high score on a test" and "Regression alone explains the pattern" added, sourced to Kahneman, Thinking, Fast and Slow ch. 17.
- **Fact 20, Collatz.** Old: `Paul Erdős said: "Mathematics is not yet ready for such problems."` New: `Paul Erdős is reported to have said: "Mathematics is not yet ready for such problems."` (quoted words untouched). Pin sourced to J. C. Lagarias (1985), The 3x+1 problem and its generalizations, American Mathematical Monthly 92(1), 3-23; its text reads "is not yet ready", so the earlier "may not be ready" claim was the later form.
- **Absolute-language hooks, for Jon's review, none changed** (fact number is 0-indexed; words searched: always, never, almost certainly, guaranteed, impossible, every, no one): **3** Card Shuffles ("almost certainly… never existed… never will again"; a probability claim stated flat); **10** √2 ("every number is a ratio"; the Pythagorean belief, fine); **11** Hairy Ball ("impossible… always at least one cowlick"; true for a sphere, a theorem); **15** Infinitely Many Primes ("always a larger one"; theorem); **20** Collatz ("You will ALWAYS reach 1"; **an unproven conjecture stated as fact in the hook**, worth a look); **26** Infinite Hotel ("can always accommodate one more"; true in the standard setup); **29** Perfect Bracket ("every match… 1 in 9.2 quintillion"; a coin-flip assumption, see its body); **35** Königsberg ("impossible", theorem); **36** Trisect ("impossible", theorem); **39** P vs NP ("may be impossible", hedged); **44** Barcodes ("Every barcode has a check digit"; true of EAN/UPC/ISBN, not of every barcode symbology); **46** Hear a Drum ("not always"; accurate); **49** Matrices ("Every computer graphic, every 3D game, every GPS"; hyperbole). The likeliest to need rewording: 20, 44, 49, 3.

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
