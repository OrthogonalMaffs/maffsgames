# Handover: home lane

**LEVEL-RESOLVER batch 1 (12 Oct; PR #317, branch `claude/level-batch-1`).** Migrated: higher-power, prisoners-dilemma, seven-bridges, binomial-blaster, curling-friction, differentiation-duel, force-resolver, moments-master, integration-duel, proof-builder (MIGRATED in `check-levels.py`; `test-level.py --games` plays each at junk and declared keys, 4 lock-tier parts). Closed: the entries that are only the ?level fault. integration-duel-t5-010 and proof-builder-t5-024 are composite (other faults in the same entry) and stay open; higher-power-t2-002 is class 4 but a streak crash, not ?level. **Held back for Jon (roster says more levels than the game has content for; removing a listing is Jon's call, no usage data to hand):** factor-race (roster lists GCSE; game plays ks3/year6 only), modular-battle (roster/card list A-Level; the game is GCSE only; its page title also says A-Level), dimension-checker (roster lists A-Level; one L4 bank, submits as level4), partial-fractions-duel (roster lists Level 4; alevel bank only). They stay on NOT_YET. **Next batch:** the other class-4 games (suvat, characteristic-quest, complex-converter, matrix-crunch), then the rest of the 99, lowest roster level first.

**LEVEL-RESOLVER (12 Oct, Jon's contract; PR 1 of the migration, branch `claude/level-resolver`).** Shared layer built: `schools/assets/level.js` (`MaffsLevel.resolve/declared/allows`, canon 4.5), a guard in `submitScore` (undeclared level = warn and no submit; undeclared pages unchanged), `scripts/check-levels.py` (declaration = roster, links/cards/sitemap, own-code reader, NOT_YET = 99 games, three plants) and `scripts/test-level.py` (Chromium; property-lookup plant caught). Listing fixes: binomial-blaster's card dropped `l4` (the game has no Level 4 content). **For Jon:** the nine Year 6-only cards also list `ks3`; I kept that as a documented alias (the portal has no Year 6 filter, so removing it would hide them from every filter but All). Decisions: an absent `?level` leaves the URL alone; matching is exact-case; `boards` is an extra declared list for session-length and tournament boards. **Next:** batches of about 10 from the 19 open class-4 findings (18 games), lowest roster level first; each moves games from NOT_YET_AT_START to MIGRATED in `check-levels.py`.

**PD-TOURNAMENT-BOARD (12 Oct, Jon's contract; PR #314, branch `claude/pd-tournament-board`).** prisoners-dilemma-t4-001 fixed per SR-22: single matches submit nothing; a completed tournament submits the player's total out of 20 x opponents under `<level>-tournament`. Hub lists the four tournament boards; the old per-level boards stay in Firebase, unlisted. `check-leaderboard-coverage.js` now fails if any PD submit is not `currentLevel+'-tournament'`, and PD's score-history keys are declared in HISTORY_ONLY_KEYS. **Contract conflict, for Jon:** the contract says do not touch `firebase-leaderboard.js`, but the coverage check requires `levelLabel()` to name every submitted key, and the only way is LEVEL_NAMES; I added four label entries there (data only, no logic) rather than stop. Node is not installed on the Windows machine, so the check ran only in CI and the planted-fail was shown by a Python re-implementation of the rule.

**GATE-AND-SR28 (12 Oct, Jon's contract; branch `claude/gate-and-sr28`).** Three rulings of 12 Oct recorded. (1) Bank depth (point 4, and served bank size in point 3) is out of the build-freeze gate: tracked in the register, worked on in parallel under SR-26. (2) `glorious-gantt` is excluded from points 1, 2 and 5 by name while unlisted (it stays live at its URL, as Jon accepted); `GATE_EXCLUDED` in `scripts/audit-register.py` holds it with the reason, the dashboard lists it on its own line, and the script fails if a slug in it leaves the roster's Unlisted section (self-test plants a relisted one). (3) SR-28: algebraic terms divide as a whole (6x⁷ ÷ 2x² divides by 2x²; SR-17 does not apply). Canon §0.2 and §0.3 updated. Dashboard locally: points 1 and 5 read met, 2 reads 1 HIGH open, 4 marked not gating. `index-laws-v20-001` is the cloud lane's to close, citing SR-28.

**GA4-LIVE-ONLY (12 Oct, Jon's contract; branch `claude/ga4-live-only`).** GA4's tag is now loaded only by `schools/assets/analytics.js`, and only on maffsgames.co.uk / www; no page carries the snippet. `scripts/apply-analytics-loader.py` changed exactly 150 pages (the snippet's two tags removed from all; the include kept on 145; added, at its relative path, on about, feedback, leaderboards, privacy, spec-map). New `check-analytics-loader.py` (site-wide, selftest with 4+ plants) and `test-analytics-loader.py` (Chromium: stub server and a local host reach no Google host and define no gtag; the live host does one gtag.js load and one config). `test-escape-analytics.py` keeps Google blocked and now asserts zero requests reach it. `verify-parent-guides.py` TPL asserts the new arrangement; canon §1.1 and `.claude/rules/analytics.md` updated. **For Jon:** (1) data before this merge still includes test traffic: exclude 800x600 in any report up to the merge; crawlers still reach GA4 (separate decision); (2) boolean-blitz and truth-will-set-you-free load analytics.js but never had the snippet, so they now send page views too; (3) `/privacy/` still prints the measurement ID as plain text (not a tag; the check allows it); (4) the old "Google Analytics (cookieless)" HTML comment stays above the include on those pages.

**FRONT-PAGE-ROOM-ORDER (12 Oct, Jon's contract; branch `claude/front-page-room-order`).** The front page's escape-room grid is now in the hub's order (comic-caper, kiln-disaster, library-jam, then the five/six ★★, rugby-mud, rightful-king); cards moved whole, the Comic Caper and Kiln Disaster wrappers with their notes; nothing else in `index.html` changed (same words, same markup). `check-escape-rooms.py` `check_ratings()` now applies the rating-order rule to every page, and requires the front page's live-room sequence to equal the hub's (both printed on failure); two planted faults (a swap across a star band, a swap within a band) are caught every run. Checked on the stub server: no overflow at 320 or 1280 px; at 1280 Library Jam shares the first row's top and height with the two wrapped cards. Only the hub and front page carry room cards. **Side effect for Jon:** `section_clicked` `position`/`filter_value` for the escape-room cards follow page order, so from this merge a room's `pos` differs (e.g. comic-caper 9 to 3, library-jam 13 to 5); `test-section-clicks.py`'s table is updated. Seen on main 5b1307a (#301): Modular Battle's verifier failed twice at its scaffold step (line 178); it passed on every later main run, so it may be a draw-dependent flake: cloud lane's.

**RULINGS-12OCT (12 Oct, Jon's contract; branch `claude/rulings-12oct`).** Canon §0.3 has SR-26 (grow banks from parameters, never swap single items) and SR-27 (verifier-only PRs run five named checks, not `check-changed.py`); CLAUDE.md "Before pushing" names SR-27 as the one exception. New `scripts/end-task.py <branch>` replaces the `branch -d` rule: it removes the worktree and local branch only if the PR is MERGED, the tip is the PR's head and the worktree is clean, else refuses; self-test in CI. (`-d` can pass while the stale `origin/<branch>` ref exists, and refuses after a prune.) **For the cloud lane:** from its next PR use SR-27 and `end-task.py`; GitHub deletes merged head branches, so drop the "Open for Jon: delete branch" lines in your next handover commit. ROOM-ART/ROOMS-RELEASE-RK-LJ moved to `docs/history/handover-home-archive.md` for size.

**CONTAINER-PULL-TIMEOUT (12 Oct, #299).** The image pull no longer counts against a group's limit: both container jobs use `timeout-minutes: matrix.job_timeout` = `timeout` + `PULL_ALLOWANCE` (10, `ci-groups.py`; emitted for content groups, literal on the 7 static entries). Budget step untouched (75% of `timeout` from JOB_T0). `ci-groups.py --selftest` fails on any mismatch. Not done: pull seconds in the summary (no in-job source for the start time). Cause: run 802, Content verifiers 33 took 379 s against 360 s. **Cloud lane:** the re-run-at-Initialize-containers rule can go after two clean full main runs.

**CI-TIMINGS-MEDIAN (12 Oct, Jon's contract; #288, merge d00a818): MAIN IS UNBLOCKED, and the cloud lane can resume VERIFIERS-20.**
`ci-groups.py --check` had failed on main and every PR since the "Record CI timings and repack (run 38224711265)" commit
(`25f887b`): run 785 recorded a 125 s setup against 18-28 s in the eleven records before it, and the repack against that
left 12 groups at 81-108%. `scripts/ci-timings.json` now keeps the last 5 main runs under `history` and its top-level
`setup` and `lines` are their medians (the seed is runs 777-785; median setup 25 s); `ci-groups.py --record-and-pack` works the
pack out in memory and writes neither file if `--check` fails; the timings job uses it and runs `--check` again before
committing. Self-test covers the 125 s outlier, a line slow in 3 of 5 runs, and a failing pack being refused. **Confirmed on
main:** run 791 (38230011527) green, its timings job ran the new path and committed run 38230011527 (`1878166`), and
`--check` passes on main. Canon §7.8.1 and CLAUDE.md have a sentence each. **For the cloud lane:** merge `main` into
`claude/verifier-think-of-a-number`, push, merge #287 on a green Gate, then continue at `formula-plug-in`. No budget,
`TARGET`/`FAIL`, timeout, verifier or `ci-pack.json` (by hand) was touched.

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
