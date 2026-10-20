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
- **Done since:** the new-shapes header DONE (#450, e0377e9; main run 39299844863, green); DEPS-SRC-HAZARD DONE (#451, 0dd1b68; main run 39309543642, green, 53 jobs); ANSWER-LOCK-STATE DONE (#452, b23fceb; main run 39315432381, green, 53 jobs); PYTHAG-KEY-COLLIDE DONE (#453, 54e0fe9; main run 39390699573, green, 53 jobs); MONTY-100-RETITLE DONE (#455, ed61533; main run 39398807202, green, 53 jobs).
- **In flight (20 Oct):** nothing. TRIG-WORMS-FILTER DONE (#462, main run 39474891224, green); COLLISION-IDENTITIES DONE (#461). MONTY-CARD-2 DONE (#459, 223d498; main run 39411995366, green, 54 jobs). KEY-COLLISION-SURVEY DONE (#458, a3d431a; **STOPPED for Jon**: wrong methods marked right in seven listed games, see its entry). No game claimed (`scripts/answer-lock-state.json` is empty).
- **Main:** green after every merge on 19 Oct (#445 39233921992, #446 39245413455, #447 39259197128, #448 39273656313, #449 39287568708, #450 39299844863, #451 39309543642, #452 39315432381, #453 39390699573, #454 39393567338, #455 39398807202, #457 39405865621, #458 39409216606 (attempt 1 red: three tier-1 page loads, better-value twice and chart-interrogator, timed out at 20 s in shard 4/4 on a docs-only merge that passed the same shard on its PR; the one rerun of the failed job, attempt 2, green, 53 jobs), #459 39411995366, #460 39414714196 (green, 53 jobs), #461 39472244834 (green, 53 jobs), #462 39474891224 (green, 53 jobs), #463 39478497493 (green, 53 jobs)). **#456's run 39401811389 is red on the timings job alone** ("CI timings and pack (main only)"; 52 of 53 green): the median-of-5 pack failed `ci-groups.py --check` (content groups 1 and 2 at 80% and 82% of 270 s) because this run's setup was 87 s (recorded setups 20, 19, 53, 27, 59: median 27 would become 53); nothing was written, so the committed pack is unchanged and PRs still pass `--check`. Groups 1 and 2 each hold one long line (Just Pythag It, Bruv part 4, median 164 s; Free Daily Pizza 171 s), at 70% and 73% on the committed pack.
- **Ruling (Jon, 20 Oct; expires when the home lane next picks up CI tonight):** main's red from the timings job alone, with every content job green and the committed pack unchanged, does not block merges; any other failure on main still does. No manual run (it skips the timings job, so proves nothing). Do not split Just Pythag It, Bruv part 4: the fix is architectural and the home lane's.
- **With the home lane (Jon, 20 Oct; the cloud lane takes no action):** (a) the roster's "15 triples" for Just Pythag It, Bruv (code: 14), contract ROSTER-PYTHAG-14, in its PR; (b) CI groups 1 and 2 near budget, a timings contract to follow (a per-line limit; splitting Free Daily Pizza and Just Pythag It, Bruv part 4). **If the next cloud work touches `scripts/verify-free-daily-pizza.py` or `scripts/verify-just-pythag-it-bruv.py`, fetch main first and rebase knowingly onto the home lane's split.**
- **Waiting on Jon (no contract yet):** (1) the front page's compact mode hides every fact card's summary on phones (600 px and below, no toggle), so the new MONTY-CARD setup is unseen there: a layout contract; (2) card 2 "The Monty Hall Problem" has the same unstated setup as the 100 Doors card had (full list of cards with unstated setup in the MONTY-CARD entry); (3) PYTHAG-REPORT's findings, for his "Formula only" ruling (the 15-triples roster line is now the home lane's, above); (4) the phone stacking of the two headers was this lane's layout choice (one line overflowed 320 px), to confirm. **Ruled, Jon, 20 Oct:** PYTHAG-KEY-COLLIDE's filter-each-pool-once is correct under §12 and SR-5 (his "reject and redraw" was wrong); the roster's "15 triples" for Just Pythag It, Bruv (the code has 14) is left for the home lane.
- **Container setup (every fresh session):** `pip install playwright==1.56.0 sympy mpmath pyyaml`; `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1 python scripts/check-changed.py`. A run takes about 70 minutes and reports the same 25 KaTeX-CDN/WebKit failures every time (by name: the set in #441's PR); run one at a time, in the background; verifiers in scratch worktrees can run beside it (free ports). Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-20 (cloud): TRIG-WORMS-FILTER (contract and Jon's amendment verbatim: `docs/handover/contracts/2026-10-20-trig-worms-filter.md`). **DONE (#462, c31cbbf; main run 39474891224, green, 53 jobs); claim released.**

- **Root cause:** `questionFrom` drops a named distractor equal to the key, so on a find-the-angle question where a wrong function or the ratio upside down lands on the key's whole degree, the student using that slip picks the key and is marked right.
- **Fix (the game's own pool; no shared module):** `questionFrom` returns `slips`, the three wrong-function and upside-down errors as marked; one pass after the pool is built drops every angle outcome whose slips include the key. Filtered once, never redrawn (canon §12, SR-5). Rounding the ratio first is not filtered (Jon). Count **52 of 588 (8.8%)**, as the merged report says.
- **Lost per (ratio, angle), of 15 hypotenuses:** CAH 75° 8, **CAH 80° 15, CAH 85° 15** (emptied, as ruled: tan⁻¹(H/A) gives the key for every triangle there), SOH 15° 8, TOA 15° 6. Every other pair still served. Both levels share the one pool.
- **Verifier (`verify-trig-worms.py`):** recomputes every slip in mpmath; the pool must be exactly the outcomes no slip gets right; every pair but CAH 80° and 85° must still be served; prints the loss per pair. Plant: the pool without the filter pass, caught ("serves 52 find-the-angle questions where a wrong function or the ratio upside down gives the key").
- **Untouched:** find-a-side questions, distractor choice beyond the filter, scoring, levels, cannon.

## 2026-10-20 (cloud): COLLISION-IDENTITIES (contract and Jon's rulings verbatim: `docs/handover/contracts/2026-10-20-collision-identities.md`). **DONE (#461, 118be76; main run 39472244834, green, 53 jobs).**

- **Done:** `scripts/survey-key-collisions.py`: a coincidence moves to 'agree (identity)' when the error equals the key on EVERY question of its group (two or more), the group named in the row. Groups: modular by b (every a; "applies" = the offerable residues 0..b-1, ruling (1)); split-it by the ratio; QF step 2 by the two coefficients its comparison with ac turns on; FDP of-an-amount by p or a/b. **trig-worms by error type, never grouped (ruling (2)):** rounding first is 'agree (precision)' (all 76); wrong function and upside down stay coincidences. `--selftest`: four modular fixtures, two trig fixtures, the control (0); all PASS. Report `docs/audits/key-collision-survey-2026-10.md` rewritten (main 878d83e).
- **Result:** coincidence 488 -> **185** (227 identities, 76 precision; none rose). modular-battle 231 -> 123, **accepted** (ruling (3), reason recorded; the report adds that guessing among the min(4, b) buttons shown is 29.2%, above every error's full rate); trig-worms 128 -> **52**, to be filtered (TRIG-WORMS-FILTER: CAH 75 8, CAH 80 15, CAH 85 15, SOH 15 8, TOA 15 6); split-it 109 -> 0; QF 15 -> 5; FDP 2, DA 2, six-sevens 1 unchanged.
- **Next:** TRIG-WORMS-FILTER (count 52 from the merged report: matches).

## 2026-10-20 (cloud): MONTY-CARD-2 (contract `docs/history/contracts/2026-10-20-monty-card-2.md`). **DONE (#459, 223d498; main run 39411995366, green).**

- **Done:** card 2 "The Monty Hall Problem": `h` is Jon's wording exactly (one car, two goats; the host knows, always opens a goat door, always offers the switch); `t`, `x`, `g`, `gl` unchanged.
- **verify-facts.py:** three pins on the new summary; `monty(doors)` lists every (car, pick) pair with a knowing host: stay 1/3, switch 2/3, so "doubles" holds exactly. The card's existing `x` pins kept. Fails on the old summary.
- **test-fact-monty.py extended, not a sibling:** it now holds CARDS (both Monty Hall cards; ci-line label renamed to cover both); each card exact, button and Share, no overflow at 320/390/1280; fails on the old summary. The phone compact mode still hides both summaries (known, not touched).
- **Old wording elsewhere:** only the cloud archive's MONTY-CARD step 3 and this contract.

## 2026-10-20 (cloud): KEY-COLLISION-SURVEY (contract `docs/history/contracts/2026-10-20-key-collision-survey.md`; report only). **DONE (#458, a3d431a).**

- **Report:** `docs/audits/key-collision-survey-2026-10.md`; script `scripts/survey-key-collisions.py` (not in CI; every count is its output). Nothing in any game, verifier, findings file, register or workflow changed.
- **Generated games (14, all surveyed):** just-pythag-it-bruv (control), six-sevens-bruv, split-it, free-daily-pizza, trig-worms, distinctly-average, quadratic-factoriser, modular-battle, factor-race and fraction-equivalence (KS3/GCSE), bearing-blitz (8 random bearings), shape-shifter (Rotation), equatle, log-laws (Solve). Found by reading every roster game (three read-only agents, evidence by file:line); simultaneous-solver's bank is generated offline, so a fixed bank at runtime.
- **Control:** just-pythag-it-bruv **0** over 2,041 questions (7 before #453).
- **Headline (error x question pairs):** coincidence **488**, methods agree **6,458**; two-way rules of thumb reported, not counted. Coincidence by game: modular-battle 231, trig-worms 128, split-it 109, quadratic-factoriser 15, free-daily-pizza 2, distinctly-average 2, six-sevens-bruv 1; zero in the rest. Method lesson: a game's own misconception list can hide exactly these cases (log-laws drops a `mis` equal to the answer; trig-worms and free-daily-pizza drop a distractor equal to the key), so every error is recomputed from its definition, never read back.
- **STOP IF (for Jon):** wrong methods marked right in listed games: all seven above (examples in the report's STOP section: 2 x 2 by adding; 2 : 2 shares; 60% of 150 = 150 - 60; trig-worms angles; x^2 + 4x + 4; modular remainders read off a / 9). Not fixed: no standing ruling covers them. The remedy (per-game pool filters as #453, or a shared check in the verifier layer) is Jon's and the home lane's.

## 2026-10-20 (cloud): MONTY-100-RETITLE (#455; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-20 (cloud): PYTHAG-KEY-COLLIDE (#453; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): ANSWER-LOCK-STATE (#452; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): DEPS-SRC-HAZARD (#451; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): HEADER "Q{n} of {N} · {right} right" (#449, #450; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): MONTY-CARD (#448; full entry, with the cards that rely on unstated setup, in `docs/history/handover-cloud-archive.md`)

## 2026-10-19 (cloud): PYTHAG-REPORT (#447; full entry in `docs/history/handover-cloud-archive.md`; report `docs/handover/pythag-report.md`)

## 2026-10-19 (cloud): ROOM-CREDIT v2 (#446; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): ESSENTIALS-SCREEN-TRUTH-2 (#441-#445; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): ESSENTIALS-FALSE-TEXT 3/4 new-shapes (#437; full entry in `docs/history/handover-cloud-archive.md`)

## 2026-10-18 (cloud): RAW-TEX-LAST-2 (#435, #436; full entry in `docs/history/handover-cloud-archive.md`)

Older entries (17 Oct and before): `docs/history/handover-cloud-archive.md`.
