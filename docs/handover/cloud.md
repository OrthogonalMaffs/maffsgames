# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Remaining list (contract LH, 7 Oct 2026; added by the home lane, kept by the cloud lane):** it lives in
`scripts/answer-lock-state.json`, not in this file (contract ANSWER-LOCK-STATE, 19 Oct 2026); `scripts/check-answer-lock.py`
reads it. Take a game off it in the PR that finishes it. While a game is on it, a failure of that game in the check
is reported, not failed; off it, a failure fails CI.

**Lane rule, listed games (Jon, 8 Oct 2026; contract "listed-game CRITICAL/HIGH"; the home lane records it in
canon §7.8 in its next docs PR):** the cloud lane now also fixes listed games. Before starting one, add it to the
remaining list (`scripts/answer-lock-state.json`) and push that commit on its own, so the home lane's F1 batches skip it; take it off
in the PR that fixes it. One game claimed at a time; never claim a game already in an open home-lane F1 batch branch
(check `docs/handover/home.md` and the open PRs first; if it is, skip to the next and note it).

**Resume rule, MaffsLock (Jon, contract LH):** adopting MaffsLock includes the game's lock-hint declaration
(`<!-- maffs-lock-hint ... -->`, canon §7.6.0), and the game passes `check-answer-lock.py`. Hints live in the
game's page, never in the shared script.
A two-option game declares an `answer` that picks the option differing from its key for `i >= 1` (canon
§7.6.0, contract DET, 8 Oct; prime-or-composite is the pattern).

**Contracts (Jon, 8 Oct 2026, corrected 20:00):** each contract is saved verbatim as
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md` in its claim commit (or the PR's first commit), with one line
in the queue below pointing to it. Read it when the item starts, not at session start (the folder stays out of the
start-up load). When the work merges, move the file to `docs/history/`.

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026): **SWEEP-1** (12 Oct, contract `docs/handover/contracts/2026-10-12-sweep-1.md`): one reading sweep of 96 live games (glorious-gantt skipped), 12 batches of 8 in lowest-level order; findings in each game's file, report `docs/audits/sweep-1-2026-10.md`. **Jon's rulings, 13 Oct** (verbatim: `docs/handover/contracts/2026-10-13-sweep-1-rulings.md`): word-problem-decoder and equation-builder fixed, not unlisted; **equation-builder must merge today, or say so and the home lane unlists it.** quadratic-factoriser DONE (#342, 3ab8cd5; Jon, 13 Oct: fixed, not unlisted). **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). Batches 1-5 DONE (#332, #336, #339, #340, #341); equation-builder DONE (#338). Batch 6 DONE (#343). **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** circle-theorem-spotter DONE (#344, 091b4f0; batch 7's SR-20 hit, fixed under SR-30). Batch 7 DONE (#345). growth-and-decay DONE (#346, 3b2eb76). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h). correlation-or-coincidence DONE (#347, f283457; batch 8's SR-20 hit, B22, B25, B27 replaced on Jon's ruling). Batch 8 DONE (#348, 186aa27). **Batch 9 (all eight reviewed) found two SR-20 levels, each fixed first under SR-30: core-maths-paper2a DONE (#349, 3989aed); stat-attack DONE (#350, 856aa7c). Batch 9 DONE (#351, 6c7c53e; Jon's rulings of 13 Oct and SR-31).** **Batch 10 (all eight reviewed; scratchpad `batch10-notes.txt`) found three SR-20 levels: growth-and-decay (PR open), test-the-claim (wt-tc), graph-sketcher; each its own PR under SR-30, then batch 10 (tax-theft on Jon's ruling).** Then batch 11 (curling-friction, force-resolver, moments-master, log-laws, binomial-blaster, partial-fractions-duel, proof-builder, dimension-checker). Reviewer brief: `docs/handover/contracts/2026-10-12-sweep-1-reviewer-brief.md`.
SWEEP-1-RULINGS (13 Oct, contract and Jon's two documents verbatim in `docs/handover/contracts/2026-10-13-sweep-1-rulings-2.md`): Jon approved the triage in full (20:35): standing rules R1-R9 (SR-33, below), 18 Part 2 rulings, Part 3 deferrals; R10 is the home lane's (contract LEVEL-LOGGED). Order: step 0 record, step 1 split bundled entries, step 2 R4 money check, step 3 per-game fixes (Year 6, KS3, Essentials at GCSE, other GCSE, Core, A-Level, L4), step 4 proportion-blaster-003 class count.
ESSENTIALS-SCREEN-TRUTH-2 (18 Oct, contract `docs/history/contracts/2026-10-18-essentials-screen-truth-2.md`): four listed Essentials games whose screens show something untrue or unreadable, one game per PR, each claimed on the remaining list first: 1 formula-plug-in DONE (#441); 2 new-shapes DONE (#442); 3 four-quadrant-explorer DONE (#443); 4 shape-shifter DONE (#445; Jon's ruling (a), 19 Oct); then (Jon, 19 Oct) 5 formula-plug-in and 6 new-shapes: header "Q{n} of {N} · {right} right". Rulings verbatim at the end of the contract file.
ROOM-CREDIT v2 (19 Oct, contract and v1 verbatim `docs/history/contracts/2026-10-19-room-credit.md`; Jon's lane exception plus his rating.js ruling): one optional room.js `credit`, drawn on the room and teacher pages, checked on the hub and front-page cards; four rooms credited. **DONE (#446, 9a94e78, merged 12:33 BST).**
PYTHAG-REPORT (19 Oct, contract `docs/history/contracts/2026-10-19-pythag-report.md`, research only): **DONE (#447)**; report `docs/handover/pythag-report.md`, for Jon's ruling on a "Formula only" mode. Then ruling (2) of 19 Oct: formula-plug-in DONE (#449, 531c988); new-shapes DONE (#450, e0377e9).
MONTY-CARD (19 Oct, contract `docs/history/contracts/2026-10-19-monty-card.md`; Jon's ruling on the phone gap at its end): the "100 Doors" card states its setup and condition; step 3 list in the entry below. **DONE (#448, b973e23).**
**START HERE (next session; written 19 Oct, 18:10 BST).**
- **Done since:** the new-shapes header DONE (#450, e0377e9; main run 39299844863, green); DEPS-SRC-HAZARD DONE (#451, 0dd1b68; main run 39309543642, green, 53 jobs); ANSWER-LOCK-STATE DONE (#452, b23fceb; main run 39315432381, green, 53 jobs); PYTHAG-KEY-COLLIDE DONE (#453, 54e0fe9; main run 39390699573, green, 53 jobs).
- **In flight (20 Oct):** MONTY-100-RETITLE (this PR; entry below). No game claimed (`scripts/answer-lock-state.json` is empty).
- **Main:** green after every merge on 19 Oct (#445 39233921992, #446 39245413455, #447 39259197128, #448 39273656313, #449 39287568708, #450 39299844863, #451 39309543642, #452 39315432381, #453 39390699573, #454 39393567338).
- **Waiting on Jon (no contract yet):** (1) the front page's compact mode hides every fact card's summary on phones (600 px and below, no toggle), so the new MONTY-CARD setup is unseen there: a layout contract; (2) card 2 "The Monty Hall Problem" has the same unstated setup as the 100 Doors card had (full list of cards with unstated setup in the MONTY-CARD entry); (3) PYTHAG-REPORT's findings, for his "Formula only" ruling (the roster says 15 triples, the code has 14); (4) the phone stacking of the two headers was this lane's layout choice (one line overflowed 320 px), to confirm. **Ruled, Jon, 20 Oct:** PYTHAG-KEY-COLLIDE's filter-each-pool-once is correct under §12 and SR-5 (his "reject and redraw" was wrong); the roster's "15 triples" for Just Pythag It, Bruv (the code has 14) is left for the home lane.
- **Container setup (every fresh session):** `pip install playwright==1.56.0 sympy mpmath pyyaml`; `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1 python scripts/check-changed.py`. A run takes about 70 minutes and reports the same 25 KaTeX-CDN/WebKit failures every time (by name: the set in #441's PR); run one at a time, in the background; verifiers in scratch worktrees can run beside it (free ports). Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-20 (cloud): MONTY-100-RETITLE (contract `docs/handover/contracts/2026-10-20-monty-100-retitle.md`)

- **Root cause:** the title called the 100-door version "Obvious" while its expanded text repeated the probability argument and never gave the picture that makes it persuasive. Jon's ruling, 20 Oct: drop "obvious", use his wording.
- **Done:** `FACTS[41]` `t` is now "Monty Hall, With 100 Doors" and `x` is Jon's text exactly; `h`, `g`, `gl` unchanged. No card 2 PR was open (STOP IF clear).
- **verify-facts.py:** re-keyed; the summary's three pins kept; the new text's pins recompute 1 in 100 stay and 99 in 100 switch (with the skipped door the same in all three places and not yours), 99 others, 50/50 for a random host (exact fractions) and 2 in 3 for three doors. Fails on main's page (old title), on the new title with the old text, and on a mismatched door.
- **test-fact-monty.py:** TITLE, EXPANDED and docstring; passes at 320/390/1280 with no overflow; fails on both plants. Its ci-line label ("Weekly fact \"100 Doors\"") still fits the new title, so it is unchanged (CI timings key on it).
- **Old title elsewhere:** only `docs/history/contracts/2026-10-19-monty-card.md` and this contract's verbatim copy; `og:` metadata and the share image are site-wide, not per fact.

## 2026-10-20 (cloud): PYTHAG-KEY-COLLIDE (contract `docs/history/contracts/2026-10-20-pythag-key-collide.md`). **DONE (#453, 54e0fe9; main run 39390699573, green); claim (620aa2a) released.**

- **Root cause:** round 3's ladder pools held small lengths where a named error rounds to the key at 1 d.p., and the game marks by value, so that wrong method was marked right. PYTHAG-REPORT §5's seven, exactly: hyp [8,24] [9,24] [11,24] [8,25] [11,25] (sqrt(2a+2b), e.g. 0.8 and 2.4 m: 2a+2b = a²+b² = 6.4); short [45,44] [50,49] (c²−a² = 0.89 and 0.99, rounding as their roots do).
- **Fix (the game's own generator; no shared module):** `J.errors`/`J.errorIsKey` compute the eight named errors in the numbers' own units, rounded as the key is (exact integers: `J.roundSqrt`, new `J.roundRat`). One pass after every pool is built keeps only entries no named error gets right: triples (all three questions a triple can ask), round 2, all five situations. Draws come from what is left. **Not "reject and redraw", as the contract worded it:** canon §12 and SR-5 forbid a redraw loop ("draw from the values that qualify"); the filter meets the contract's aim, computed in code at generation, so a later pool change is filtered too. Ladder hyp 292 → 287, ladder short 92 → 90, nothing else changed; smallest situation pool TV hyp 21 (TV 59 in all), so the under-20 STOP IF does not fire; type sequence untouched.
- **Verifier (part 4, task "named errors"):** reads every pool from the page, recomputes keys and the eight errors in exact fractions: 2,041 questions, none at the key; each situation at least 20; the plant (the page with the filter cut out, the old generator) shows 2,048 and the seven, CAUGHT; the filter drops exactly those entries. Main's page served as the real one fails on all seven.
- **Untouched:** the 95 two-error ties (they wait for the Formula-only ruling), the tap step, scoring, leaderboard, session length, the add-instead-of-subtract diagnosis.
- **For the home lane (roster):** the row says round 1 draws "from 15 triples"; the code has 14 (3-4-5 ×1-8 and ×10, 5-12-13 ×1-3, 8-15-17, 7-24-25), and the filter drops none.

## 2026-10-19 (cloud): ANSWER-LOCK-STATE (contract and Jon's ruling A verbatim: `docs/history/contracts/2026-10-19-answer-lock-state.md`). **DONE (#452, b23fceb; main run 39315432381, green).**

- **Root cause:** `check-answer-lock.py` read the cloud lane's remaining list from this file, so every handover edit selected all six answer-lock parts. The list is state, not prose.
- **Fix:** the list is now `scripts/answer-lock-state.json` (`{"cloud-remaining": [...]}`, empty). `cloud_remaining()` reads it and fails unless it holds exactly that one key, once, with a list of slugs (selftest: missing, repeated, string, extra key, non-object, old line format, each rejected). Answer-lock logic, parts and report-not-fail unchanged.
- **STOP IF fired, then ruled (Jon, A):** the claim process wrote and read the line, so CLAUDE.md, canon SR-21, §7.6 and §7.8.2, `docs/handover/home.md` (its batch rule) and this file's lane rules now name the JSON. A claim or unclaim commit edits the JSON and so still selects answer-lock (it changes its result; Jon agreed). Verbatim contracts and archives keep their wording.
- **Other scripts reading `docs/handover/` or `docs/todo.md` as state:** none. `check-context-size.py` measures the handover's size (its job; it always runs anyway); `verify-simultaneous-solver.py` reads a contract file under `contracts/`, not a handover; every other match is a comment.

## 2026-10-19 (cloud): DEPS-SRC-HAZARD (contract `docs/history/contracts/2026-10-19-deps-src-hazard.md`; Jon gave this shared-script fix to the cloud lane). **DONE (#451, 0dd1b68; main run 39309543642, green).**

- **Root cause:** `ci-deps.py`'s computed-src test `\.src\s*=\s*(?!quote)` backtracked `\s*` to zero and fired on every literal, so `analytics.js`'s `.src = 'https://...' + GA_ID` made every page that loads it a hazard: 125 of 129 selective verifiers always ran. Only `analytics.js` creates a script element on the site, and its one src is a literal https prefix plus the constant `GA_ID`: no real hidden hazard.
- **Fix:** `src_hazard(text)`: `\.src\s*=(?!\s*quote)` (the contract's regex), plus a literal joined to anything is computed unless it is an https prefix joined only to constants (names assigned a literal in the file). Selftest gains fixture lines, `analytics.js` has no hazard, and `ALWAYS_BUDGET = 12` (now 9). Check (a) now also expects the verifiers that read every game (a `games/` directory dependency: check-levels, check-level-logged, test-level), which the always-set had hidden.

## 2026-10-19 (cloud): HEADER "Q{n} of {N} · {right} right" (#449, #450; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): MONTY-CARD (#448; full entry, with the cards that rely on unstated setup, in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): PYTHAG-REPORT (contract `docs/history/contracts/2026-10-19-pythag-report.md`; full report `docs/handover/pythag-report.md`)

- Research only; nothing in the game changed. The flow, tap, diagnosis and scoring are the game's own code (`window.JPIB`); only marking (`MaffsAnswer`), session buttons, lock, Next, calculator, leaderboard and history are shared. No shared stage layer exists.
- **1** The tap is round 1 only (7 of 20), and a wrong tap blocks until the hypotenuse is tapped. **2** The tap scores nothing and costs nothing (score is timed from the answer box opening); leaderboard `ks3` takes the summed time-weighted score over 20, plus score history and `jpib_best_ks3`; the session is always 20. **3** Generated from pools: round 1 from **14** triples (the roster says 15), round 2 from 164 hyp / 236 short pairs, round 3 from five situations (1,083 hyp / 523 short); keys are sqrt(S)/D half up, round 1 exact; marking is exact at 1 d.p. with no tolerance (an unrounded answer gets a "round" message). **4** One diagnosis now: added instead of subtracting (worked example x3, then a nudge). **6** The start screen's Questions panel can take a mode row; modes elsewhere are cards (Shape Shifter) or boards per mode (Simultaneous Solver `foundation-s1..4`).
- **5** Script output (scratch `measure.py`, every question rounded as the game rounds):

```
Questions the game can ask: 2048 (round 1: 42; round 2: 400; round 3: 1606)
round  type   questions  candidate=key  two candidates equal  either
1      hyp           14              0                     1       1
1      short         28              0                     7       7
2      hyp          164              0                    15      15
2      short        236              0                    18      18
3      hyp         1083              5                    43      48
3      short        523              2                    11      13
total              2048              7                    95     102
```

  The 7 key collisions are all round-3 ladders, in metres below about 3 (sqrt(2a+2b) or c^2-a^2 rounds to the key). 87 of the 95 pair collisions are two identities: c-a = sqrt(2c-2a) when c-a = 2, and sqrt(|b^2-a^2|) = sqrt(2a+2b) when b-a = 2. Examples and the full list are in the report.

## 2026-10-19 (cloud): ROOM-CREDIT v2 (#446; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): ESSENTIALS-SCREEN-TRUTH-2 (#441-#445; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): ESSENTIALS-FALSE-TEXT 3/4 new-shapes (#437; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): RAW-TEX-LAST-2 (#435, #436; full entry in `docs/history/handover-cloud-archive.md`)

Older entries (17 Oct and before): `docs/history/handover-cloud-archive.md`.
