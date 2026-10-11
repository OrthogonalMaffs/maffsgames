# Handover: home lane

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


**ESCAPE-ANALYTICS (11 Oct, Jon's contract; STOPPED on its shared-layer STOP IF, then Jon's rulings 11 Oct).**
Diagnosis (Jon's Rightful King play, Sheet rows 55413-55434): (1) the eight index-0 "answers" were room searches:
`engine.js:359` logged each first search as question_answered, correct, index 0 (the Sheet has no `detail` column,
so the `searched:` tag never showed); (2) the mid-game abandon came from `analytics.js:138-146`, which sent
game_abandoned on every visibilitychange to hidden, in **every game**, so a game finished after a tab switch counted
as abandoned and completed; (3) GA4's 2 completions did not reproduce: one call site (`engine.js:805`, st.done
guard), one analytics.js, and the test shows one play sends exactly one game_completed to GA4 and one to the Sheet,
so it is closed as a realtime counting artefact (Jon's ruling). Fixed, shared layer: searches send nothing;
`mfg()` drops game_abandoned unless the page is being left (beforeunload / pagehide set `_mfgLeaving`;
analytics.js loads in the head, so its beforeunload runs before any game's), the visibilitychange listener is
gone, pagehide sends it; once per game as before. **Abandon figures change meaning on 11 Oct 2026** (canon §1.3,
with the trade-off: a backgrounded phone tab later killed by the OS sends nothing). New
`scripts/test-escape-analytics.py` (in CI): Rightful King won after searching every object and a tab switch, 3/1/0
to GA4 and the Sheet; the room left mid-game, 1 abandon; prime-or-composite (own visibilitychange handler) with a
tab switch, 0 abandons, 1 completion; three old faults planted and caught. Both faults predate the public repo
(2 Oct 2026), so the history cannot date them; affected Sheet rows not counted (no export here).

**LOG-NOTATION (10-11 Oct, Jon's contract; STOPPED on a wrong key, then Jon's rulings; PR #274).** B11's parser
(`bank_common`): log with no base is base 10, ln base e, log_b base b; a power argument of ln/log is bracketed
(ln e^2 parses); and, Jon's class fix, a symbol inside a log is positive when two values are compared (log(x^2) =
2 log x). **B11 over all 97 games: no existing verdict changed; +4 pairs, all log-laws ([7], [13], [39], [42]); the
domain rule added none anywhere**, so no other game's findings file changed. log-laws Laws bank: five distractors
replaced ([7], [13], [18], [39], [42]); **[22] (1/3 log 27) was keyed 1, value log 3: CRITICAL (Jon), now keyed log
3** (options log 3, 1, 3, log 9); [24]'s 2 log x (equal to the key for x > 0) replaced by log(1/(2x)).
verify-log-laws.py now checks the Laws bank too (every key its question's value, no two options equal; the old [22]
and [24] planted and caught). Findings log-laws-ln-001..006 (fixed, #274; f0-001 fixed); ledger cleared for log-laws
only. Locally the banks were extracted with `extract-banks.py --workers 2` (98 s; 4 workers risks this machine's
memory). Note: this machine's Bash heredocs eat backslashes, so regex-heavy scripts were written to files first.


**ROOMS-RELEASE-RK-LJ (10 Oct, Jon 22:45: "both have been play tested, so lets just release"; contract in
`docs/history/contracts/2026-10-10-rooms-release-rk-lj.md`).** The Rightful King (★★★) and The Library Jam (★) are
live, released as Car Trap was: each index.html is the room (prom-budget's head: analytics on, indexable, canonical,
the draft's meta description, 159 and 150 characters; og:image the scene), play.html deleted, teacher.html still
noindex. Hub cards (draft hub line, topics, `data-stars` chip; Library Jam last of the ★, Rightful King after Rugby
Mud) and front-page band cards (after Car Trap; test-section-clicks' order updated); sitemap `<url>` each; "nine" ->
"eleven" in the hub (description, og:description, lede), the front page (band lede, "Open all eleven rooms"),
CLAUDE.md and canon §11.1 (both rows added, Live 10/10). **Not a plain "nine", left for Jon:** canon §11.3's "Across
the eight live rooms: 199 verified number sets" is a replay statistic, not a count to bump. it-vengeance still
redirects to /escape-rooms/rightful-king/ (checked in Chromium). /updates/: one line each under October's New. The
twelve finished contracts moved from docs/handover/contracts/ to docs/history/contracts/ (the folder is empty).
Checked: check-escape-rooms, test-escape-rating (11 rooms, no 320 px overflow), test-escape-art (both rooms to a win
and a loss with their pictures), test-section-clicks, context size. **Merged #271 (227fb0a), main green. Live site checked
10 Oct:** /escape-rooms/rightful-king/ and /escape-rooms/library-jam/ serve 200 with their titles; in Chromium at 320 px each
shows its scene picture and Start, no sideways scroll; /escape-rooms/it-vengeance/ lands on The Rightful King; the hub
says "Eleven"; the old play.html is 404.

**ROOM-ART-RK-LJ: The Library Jam (10 Oct, Jon's contract; pictures approved 22:20-22:42).** The Rightful King's
half was already merged as #269 (main green, 32c2be0). Filed `docs/art/library-jam-scene/-fail/-win.webp` (1600x873,
q80, via `strip-gen-watermark.py --width 1600 --frame 1600x873`: no watermark). **All three sources are 2752x1536, like
the scene, so nothing was upscaled** (the contract expected ~1024 px fail and win). Arm, bin, drop-box and desk screen
all in frame. The squiggle "writing" on the two papers pinned to the right-hand wall is blanked in all three (each
paper refilled from a plane fitted to its clean paper, so the glow gradients stay; outlines untouched); nothing else
retouched. The papers stacked on the desk keep a few pixel-high illegible marks. room.js: `art: 'library-jam'`, the
"ART: none yet" note replaced; sceneAlt checked against the picture and unchanged; failAlt and winAlt as the contract
gives them; RULE (no `missArt`) kept. **Still unreleased. Jon can play-test with pictures at
https://maffsgames.co.uk/escape-rooms/library-jam/play.html** (and rightful-king/play.html). Checked: play.html in
Chromium at 1280 and 320 px (scene, win, fail at time-out); check-escape-rooms (all art present) and test-escape-art pass.

**RIGHTFUL-KING-ART (10 Oct, Jon's contract; pictures approved 22:20).** Filed `docs/art/rightful-king-scene.webp`,
`-fail.webp`, `-win.webp` (1600x873, WebP q80, through `strip-gen-watermark.py --width 1600 --frame 1600x873`: no
watermark; 2752x1536 cropped to 2752x1502, so crown, server cupboard and desk all stay in frame). Nothing readable or
branded; the mug carries a pixel-high scribble under its leaf, illegible even zoomed. room.js: `art: 'rightful-king'`,
the "ART: none yet" note replaced, sceneAlt gains the sticky note and printer, failAlt rewritten (night, lit by the
display), winAlt unchanged; the RULE (no `missArt`) kept. **Still unreleased** (holding page, no hub card, no sitemap).
**Jon can play-test it with its pictures at https://maffsgames.co.uk/escape-rooms/rightful-king/play.html.** Checked:
play.html in Chromium at 1280 and 320 px shows the scene on the brief, the win picture on a win, the fail picture at
time-out; check-escape-rooms and test-escape-art pass.

**SCIENTIFIC TAGGING 5/5: core-maths-paper2c (10 Oct). The tagging run is done** (#261, #264, #265, #266, this;
complex-converter stays untagged, Jon). Roster `scientific`, badge on the start card, scientific calculator under the
question card (below Next, so Next does not move on a phone); check-calculator, verify-core-maths-paper2c and the
Chromium smoke (sin(30) = 0.5 at 1280 and 320 px, no overflow) pass; CI the gate.

**STAR-KEY (10 Oct, Jon's contract 17:50; `docs/handover/contracts/2026-10-10-star-key.md`).** One line saying
what the stars mean, on the hub (under "Ordered easiest to hardest") and on the front page's escape-room band
(`.esc-note` size, 12.5 px; placed just above the cards, so with the band compacted it sits directly under the
summary and on desktop beside the cards it explains): "Stars show difficulty, set by each room's hardest lock: ★
Warm-up, grades 1–3 · ★★ Core, grades 4–5 · ★★★ Challenge, grades 6–9." Glyphs aria-hidden; a screen reader reads
"one star, Warm-up, grades 1 to 3; two stars, ..." (checked in Chromium's accessibility tree). check-escape-rooms.py
matches each page's `data-star-key` line to BANDS (which already match rating.js), checks the spoken text, and
plants "Core, grades 4–6" (caught). No 320 px overflow (test-escape-rating). STOP IF clear: it wraps at the band's
own size. Older entries (CAR-TRAP-V2-ART, ART-PENDING, MAIN GREEN) moved to the archive for room.

**TODO-SLIM (10 Oct; Jon's option (b), 17:15).** `docs/todo.md` 481,628 -> **148,748 bytes** (3,662 -> 810 lines);
moved word for word to new `docs/history/todo-done.md` (333,814 bytes; the two add up to the original plus the
added headings): the session log (line 5 kept its newest three entries; lines 6-56, 88-140, 145-160 of 28-29 Sep
notes), the whole START block (replaced by a pointer: **the live queues are the two handovers**), 27 done rows of
§1/§3 (listed under §1's heading, so their numbers still resolve), and "Done — full history". **Kept, for Jon:**
the 29 Sep paragraph (lines 57-87) holding a leaderboard recommendation still "pending Jon's ruling"; done-looking
rows with open follow-ups stay whole (1.8, 1.11, 1.14, 1.16, 1.24, 1.25, 1.26, 1.33, 1.36, 1.51, 1.72, 1.75, 3.4,
3.6-3.10, 3.18). **Cap 150 KB, not 140:** the kept content came out at 145 KB (open rows were bigger than my
estimate); lower `TODO_LIMIT` in `check-context-size.py` as items close. canon.md is reported (194,804 bytes),
not capped. Canon's three "todo START" citations now point at the history file. **For Jon:** update Project
Claude's instructions to name the handovers, not todo.md's START, as the live queue.
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
