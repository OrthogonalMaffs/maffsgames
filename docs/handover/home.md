# Handover: home lane

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
**LOCK-BANK-CI (10 Oct, Jon 17:15; for the cloud lane's room builds).** `scripts/check-lock-bank.py` rejected
hamster-feeder-bounds on main: `NOTE` was not a known field, so a multi-line note's continuation lines were glued
onto VERIFY (SyntaxError). Fixed in the parser (`NOTE` is a field), not by reflowing the entry; every other lock's
result is unchanged (before/after diff of all 7 batches: only hamster-feeder-bounds, REJECT -> ok, 580). With no
argument it checks every `docs/lock-bank-batch*.txt`; `--selftest` plants four entries (a sound lock with a
two-line NOTE, two answers, a restating VERIFY, a wrong ANSWER), all caught; it is now in CI (ci-line, about a
second). **Never run by CI (report only):** `scripts/check-feedback-options.py` (the feedback page's game menu;
passes locally) and `scripts/check-lock-uniqueness.py` (an older one-answer checker; passes locally);
`verify-regression-rumble.py` is declared held (game withdrawn). `check-changed.py` is the runner, not a check.
**#255 PREPUSH-SCOPE merged** (99a0bf5).

**DASHBOARD-CHARTS (10 Oct, Jon's contract 08:35; `docs/handover/contracts/2026-10-10-dashboard-charts.md`).**
`docs/apps-script-endpoint.js` only, SCRIPT_VERSION `2026-10-10-a`: the three percentage columns are written as
fractions with the cell format `0%` (they show as before), the Accuracy chart's axis runs 0 to 1 as percent;
`rowBelowChart()` moves the row counter below each chart (a 21 px default row), so no chart overlaps the next
section; one filter, `isMarked()`, keeps rows with a blank `correct` out of Accuracy by Game and Hardest Questions.
STOP IFs clear: prisoners-dilemma sends `correct: null` (written blank by `cellValue`), and every other
`question_answered` call in games/ sends a boolean. The daily email is untouched (its own hardest-questions list still
counts prisoners-dilemma: the contract left the email alone). **Jon must redeploy; the repo copy does not deploy
itself** (runbook `docs/apps-script-redeploy.md`): paste the file into the Apps Script editor and set `REPORT_EMAIL`
to your address before saving; Deploy, Manage deployments, edit (pencil) the existing deployment, Version: New
version, Deploy; select `testDashboard` in the function menu and Run (it rebuilds the dashboard from the sheet;
`rebuildDashboard` itself needs arguments), or wait for the 07:00 run; open the `/exec` URL and check `version` reads
`2026-10-10-a`.

**DOCS-9OCT (10 Oct, branch `claude/docs-9oct-b`, after the checkpoint).** #239 SCI-CALC and #240 (checkpoint
handover) merged on 9 Oct late, main green after each (9f51dc7, 302d4d2). DOCS-9OCT applied: Factor Theorem relisted
under SR-21, **A-Level only** (roster #88, portal, sitemap, hub, spec map, canon count 96, todo 1.62); canon §0.2 the
freeze's one exception (Simultaneous Solver Stage 5, #203); §7.6 four rulings (Skip shows the answer and waits on
Next; one log row per answer; display-only number formatting; "≈" for rounded factors); §7.8.2 closed-not-idle cloud
sessions and the E2 one-off; timer-policy: Unit Converter to No Timer. **Escape on the initials overlay (Jon, 9 Oct
19:42): left as is, Skip stays the way out; Escape-to-close is deferred to a future accessibility pass, because an
accidental Escape would discard a leaderboard entry** (the OVERLAY-KEYS contract's "Escape closes the overlay as now"
was Project Claude's error; recorded on #232 too). **Next: KEYPAD-VARIABLE (entry at the top), then PREPUSH-SCOPE** (contract
`docs/handover/contracts/2026-10-09-prepush-scope.md`). LIBRARY-DRAFT moved to the cloud lane (Jon, 10 Oct 09:30);
Car Trap moved the other way: the home lane owns it end to end (#242, entry above). **Scientific tagging, Jon's ruling (10 Oct):** tag force-resolver,
moments-master, complex-converter, formula-forge, formula-unlocked, core-maths-paper2c (one PR each, after
PREPUSH-SCOPE); not estimation-golf or equation-builder; log-laws and higher-power reported back (SCI-CALC's
entry is archived in `docs/history/handover-home-archive.md`). Finished home-lane contracts (home-queue, its addendum, hook-fix, overlay-keys) moved to `docs/history/contracts/` in
this PR; the cloud lane's (listed-high, car-trap) and the IT room brief stay.

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
