# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Remaining list (contract LH, 7 Oct 2026; added by the home lane, kept by the cloud lane):** take a game off
this line in the PR that finishes it. `scripts/check-answer-lock.py` reads it. While a game is on it, a
failure of that game in the check is reported, not failed; off it, a failure fails CI.
`cloud-remaining: `

**Lane rule, listed games (Jon, 8 Oct 2026; contract "listed-game CRITICAL/HIGH"; the home lane records it in
canon §7.8 in its next docs PR):** the cloud lane now also fixes listed games. Before starting one, add it to the
remaining list above and push that handover commit on its own, so the home lane's F1 batches skip it; take it off
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
ESSENTIALS-SCREEN-TRUTH-2 (18 Oct, contract `docs/handover/contracts/2026-10-18-essentials-screen-truth-2.md`): four listed Essentials games whose screens show something untrue or unreadable, one game per PR, each claimed on the remaining line first: 1 formula-plug-in DONE (#441); 2 new-shapes DONE (#442); 3 four-quadrant-explorer DONE (#443); 4 shape-shifter DONE (#445; Jon's ruling (a), 19 Oct); then (Jon, 19 Oct) 5 formula-plug-in and 6 new-shapes: header "Q{n} of {N} · {right} right". Rulings verbatim at the end of the contract file.
ROOM-CREDIT v2 (19 Oct, contract and v1 verbatim `docs/handover/contracts/2026-10-19-room-credit.md`; Jon's lane exception plus his rating.js ruling): one optional room.js `credit`, drawn on the room and teacher pages, checked on the hub and front-page cards; four rooms credited. **DONE (#446, 9a94e78, merged 12:33 BST).**
PYTHAG-REPORT (19 Oct, contract `docs/handover/contracts/2026-10-19-pythag-report.md`, research only): **DONE (#447)**; report `docs/handover/pythag-report.md`, for Jon's ruling on a "Formula only" mode. Then ruling (2) of 19 Oct: formula-plug-in and new-shapes headers, one PR each.
MONTY-CARD (19 Oct, contract `docs/handover/contracts/2026-10-19-monty-card.md`; Jon's ruling on the phone gap at its end): the "100 Doors" card states its setup and condition; step 3 list in the entry below. In progress (this PR).
**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-19 (cloud): MONTY-CARD (contract `docs/handover/contracts/2026-10-19-monty-card.md`)

- **Source:** one entry, `FACTS[41]` in `index.html` (`t`/`h`/`x`/`g`/`gl`), drawn by `loadFact()`. Share copies `h` at run time; no other page, share image or metadata carries the text. `scripts/verify-facts.py` pinned the old words, so its pins for this card now hold the new claims, each recomputed (50/50 for a random host by exact fractions).
- **Done:** summary and expanded text exactly as the contract; title, label, button, link and Share unchanged. New `scripts/test-fact-monty.py` (CI): both texts exact, button and Share shown, no overflow, at 320/390/1280; main fails on the text.
- **Phone gap (Jon's ruling, 19 Oct: ship, test truthfully):** at 600 px and below the compact mode hides every fact card's summary with no toggle, so phone readers never see the setup sentence; the test records it. A later layout contract.
- **Step 3: other cards that rely on setup, terms or conditions they never state** (changed: none):
  - **2 The Monty Hall Problem** (strongest, the same gap): "He opens another to reveal a goat. Should you switch?" never says one car and two goats, nor that the host knows where the car is and always opens a goat door and always offers the switch; the body then uses "the car" unintroduced.
  - **27 The Prisoner's Dilemma:** "If both stay silent: 1 year each" never sets up two suspects questioned separately who cannot confer; "tit-for-tat won both" names two tournaments never introduced.
  - **31 The Unexpected Hanging Paradox:** "can't be Friday" assumes a Monday-to-Friday week, and never says what "a surprise" means (he cannot work out the day the night before).
  - **33 Regression to the Mean:** "Israeli flight instructors concluded criticism worked and praise didn't" omits the story: praise came after unusually good landings, criticism after unusually bad ones.
  - **21 Small Samples Vary More:** the hospital figures assume each birth is a boy or a girl with equal chance, independently; never stated.
  - **8 Benford's Law:** "In most real-world datasets" omits the condition (data spanning several orders of magnitude); the "11% you'd expect" assumes each first digit 1-9 equally likely, unstated.
  - **47 Why Sample Size Matters:** "±3% margin of error" assumes a 95% confidence level and a proportion near 50%; unstated.
  - **29 The Perfect Bracket Is Impossible:** "NCAA tournament", "bracket" and "higher seeds" assume US college basketball's 64-team knockout.
  - **Terms used but never explained:** 14 "P(disease|positive)" (conditional-probability notation); 17 "r ≈ 0.96" (the correlation coefficient); 19 "e" (only i is defined); 43 "the Taylor series for sin(x)"; 50 "a random arrangement has no fixed point".

## 2026-10-19 (cloud): PYTHAG-REPORT (contract `docs/handover/contracts/2026-10-19-pythag-report.md`; full report `docs/handover/pythag-report.md`)

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

## 2026-10-19 (cloud): ROOM-CREDIT v2 (contract `docs/handover/contracts/2026-10-19-room-credit.md`)

- **v1 stopped (10:12)** on its first STOP IF: the request line was hand-written in four places (hub :79-80, :94-95; front page :813-814, :825-826), plus Roll for Initiative's teacher.html :24. v2 (10:32) rules the shape.
- **Done:** `credit: "..."` in room.js (Big School Begins, Roll for Initiative, Comic Caper, Kiln Disaster); `rating.js` `credit(room)` + the one `INVITE` (Jon's ruling, 19 Oct: rating.js is the one file both pages load); engine.js draws it under the start screen's buttons, teacher.js after the brief; RfI's hand-written line and its room.js comment removed; hub and front-page notes added for BSB and RfI in the existing wrapper markup. `check-escape-rooms.py` reads the credit by regex (as it reads `label`) and fails a differing note, a note on an uncredited room and a credited room with no note (three plants); main's pages fail exactly on BSB and RfI, both pages. New `scripts/test-escape-credit.py` (CI): text once, link to /feedback/, no overflow or cut title at 320/390/1280; main's assets fail on all four rooms.

## 2026-10-18 (cloud): ESSENTIALS-SCREEN-TRUTH-2 (contract `docs/handover/contracts/2026-10-18-essentials-screen-truth-2.md`)

- **#437's main run (the contract asks it be recorded):** 39157734021 on 32ac21b, green. Main's latest full run at the start of this contract: 39159103668 on 925738e (#439), green. Open home-lane PR #440 (LOCAL-FLAKES follow-up) touches no game.
- **Local setup, every fresh container, before `check-changed.py`:** esprima 4.0.1 will not pip-install here, so `pip download --no-deps esprima==4.0.1`, untar the sdist into the scratchpad and put the unpacked `esprima-4.0.1` directory on `PYTHONPATH` (`PYTHONPATH=<scratchpad>/esprima/esprima-4.0.1 python scripts/check-changed.py`); without it tier 4 layer A and every bank extraction fail. Also `pip install playwright==1.56.0 sympy mpmath pyyaml` (1.56.0 matches `/opt/pw-browsers` Chromium 1194).
- **1 formula-plug-in (#441):** the header slot read questions done over session length (`currentIndex`/length); now `showScore(answered)` writes `correctCount` over answers given (0/0, 1/1, 1/2, 2/3), from `loadQuestion` and straight after marking. Display only: no leaderboard, PB, history or event value changes (nothing reads the slot). Verifier plays right, wrong, right and checks the slot against its own count; plant of the old count caught; main fails on exactly that check. t3-005 fixed; off the remaining line. **For Jon:** the page now has no "how far through" count (the slot was the only one); not changed, a design call.
- **#441's main run:** 39174478559 on 2f1b1cb, green.
- **2 new-shapes (#442):** the same slot fault and fix as formula-plug-in; same verifier check, plant caught, main fails on it. t3-008 split as SWEEP-1-RULINGS step 1 did (52dle pattern): t3-008 keeps the score slot (fixed); t3-009 (no units) and t3-010 (events lack mode) new and open, parent's fields kept. Prepared in a scratch worktree while #441's checks ran, claimed before any of it was pushed. check-changed: 25 failures, the same set by name as #441's.
- **#442's main run:** 39180198115 on 5576582, green.
- **3 four-quadrant-explorer (#443):** "(0,0)" moves from below-left of the origin (over both -1s at 320 px, the x -1 at 390) to above-right, the one quadrant with no tick label; kept at every width. Verifier measures every drawGrid label (measureText box at its alignment, pinned Outfit) at 320/390/1280 px: all ticks present, "(0,0)" once, no overlap; old position planted and caught; main fails on exactly the three overlaps. Screenshots `docs/screenshots/four-quadrant-explorer-origin-{320,390}.webp` (main | branch). check-changed: the same 25 by name.
- **#443's main run:** 39186222986 on 1e7e532, green.
- **4 shape-shifter, 18-19 Oct: STOPPED** on the STOP IF (the contract's square shares area with reflection items index 3 and 6; no duplicate, on the grid); full record in #444 (597a8b3). Jon ruled (a), 19 Oct: go as written.
- **Jon's rulings, 19 Oct (verbatim at the end of the contract):** (1) shape-shifter goes as written, "overlaps" meant a duplicate item; (2) formula-plug-in and new-shapes get "Q{n} of {N} · {right} right", one PR each after shape-shifter, a follow-up to t3-005/t3-008, nothing new closed; both games have a fixed session length (10/20/30 chosen before Start, ends after that many), so its STOP IF does not fire; (3) #437 did apply the new-shapes reveal line (main :329, squash 32ac21b); not touched here.
- **4 shape-shifter (#445):** REFLECTION_QUESTIONS[14] is now the contract's square (-4,1)..(-4,3); `verify-shape-shifter.py` has `EXPECTED = {}`, so its self-image check fails any such item (Reflection and Random Mix share the bank); plant of the old square caught; main fails only on reflection 15. Ledger: no shape-shifter content ids. check-changed: the same 25 by name. t3-003 fixed.
- **check-changed here:** 73 min, 25 failures, all the KaTeX-CDN/WebKit set (formula-plug-in appears only as `katex is not defined` in answer-lock part 6, identical on main's copy). Run one at a time; free ports mean verifiers in scratch worktrees can run beside it.

## 2026-10-18 (cloud): ESSENTIALS-FALSE-TEXT 3/4 new-shapes (#437; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): RAW-TEX-LAST-2 (#435, #436; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-17 (cloud): ESSENTIALS-FALSE-TEXT (#426, #428, #431; new-shapes awaits Jon; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-16 (cloud): BSB-ROOM-BUILD (finished 17 Oct, #425 and #429; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-16 (cloud): BSB-ROOM-DRAFT (finished 16 Oct, #422; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-16 (cloud): GS-L4-5-ENDPOINT (finished 16 Oct, #420; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-15 (cloud): BV-CRITERIA (finished 15 Oct, #416; full entry, with every old and new wording, in `docs/history/handover-cloud-archive.md`)

## 2026-10-15 (cloud): BV-RULINGS (finished 15 Oct, #407; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-14 (cloud): TRUE-DISTRACTORS and MAIN-GREEN-AND-OPTION-PARITY (finished 14 Oct; full entries in `docs/history/handover-cloud-archive.md`)
