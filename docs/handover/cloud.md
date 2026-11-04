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
reads it. Take a game off it in the PR that finishes it. While a game is on it **and unlisted**, a failure of that game
in the check is reported, not failed; a listed game on it is judged as if unclaimed (`exempt()`: claimed AND unlisted;
corrected 2 Nov, Codex's catch). Off it, a failure fails CI.

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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026): **IN PROGRESS: SEARCH-KEYWORDS** (Shared, lane exception in the contract, `docs/handover/contracts/2026-11-04-search-keywords.md`; stops at a green Gate for Project Claude's review and Jon's "merge"). **ROOM-ESCAPED: DONE** (#656, a7b476c, main run 41800889964 GREEN; `docs/history/contracts/2026-11-04-room-escaped.md`). **In this order (Jon, 3 Nov; each starts after the one before merges): 1 SEQ-SOLVER-FIXES: DONE** (#652; `docs/history/contracts/2026-11-03-seq-solver-fixes.md`); **2 SEQ-SOLVER-WORKED: DONE** (#654; `docs/history/contracts/2026-11-03-seq-solver-worked.md`); **3 DASHBOARD-METRICS: DONE** (#655, ba104dc; Shared, `docs/handover/contracts/2026-11-03-dashboard-metrics.md`; Amendments 1 and 2: games.json read from raw.githubusercontent.com; stops at a green Gate for Project Claude's review and Jon's "merge"; STOP IF 1 listed for Jon: Prisoner's Dilemma, entry below). **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **QUESTION-ID**: DONE (#649; `docs/history/contracts/2026-11-03-question-id.md`); Jon redeployed the endpoint, 3 Nov. **SEQ-SOLVER-REREAD**: DONE (#647; `docs/history/contracts/2026-11-03-seq-solver-reread.md`). **DASH-MINUS**: DONE (#646; `docs/history/contracts/2026-11-03-dash-minus.md`, its table beside it). **CLOUD-LEAN**: DONE (#643; `docs/history/contracts/2026-11-03-cloud-lean.md`). **PIES-EXIT**: DONE (#642; `docs/history/contracts/2026-11-03-pies-exit.md`). **FRACTION-STACK follow-up:** give MaffsFractionInput an optional whole-number box for mixed numbers, then move the-6-ps and how-many-parts (`scripts/fraction-input-warn.json`) onto it. **Estimation Golf art parked: the game has no start screen; placement to be decided** (Jon, 2 Nov; branch `art/estimation-golf`, 028cf683, the PNG unchanged, no PR). **GATE-RESUME** and **GATE-FIX** (2 Nov, `docs/history/contracts/`): DONE (#630, #631, #632, #634), entry below. **GATE-WARN-THEN-ENFORCE** (27 Oct): steps 1-3, 5 DONE (#590, #630, #592, #631); steps 4, 6 and the post-freeze queue: live pointers below. **SHARD** (27 Oct): DONE (#578, 39b7c99; its entry archived). **Session queue (Jon, 27 Oct afternoon):** 1 SHARD; 2 FOLD PR 3-6 (PR 6 stops before merge: Project Claude's live 404 check); then, after the home lane's 6 P's launch PR merges (do not edit games.json, the homepage, /essentials/ or /updates/ before it), **KEYPAD-FRACTION** (Jon: review `claude/keypad-fraction-key` 799dbfd9, the / key on the shared keypad; every keypad game through the phone-fit gate; PR, merge on green; then tell the build lane to set `FRACTIONS = true` in `games/y-so-steep/` (Stage 3); if any existing game changes behaviour, leave it unmerged and report); 3 The 6 P's in the phone-fit gate (driver change); 4 Higher Power's card values spilling on phones; 5 Screening Room panels + the hardened top-scores check (item E); 6 the mode dimension (item D); 7 the answer-control (8) and tall-input (6) games; 8 the start-screen rule only once a shared compact start screen exists, else write up what it needs and stop. Items D and E: no contract text found in the repo; ask Jon. **FOLD-COMPONENTS** (27 Oct, `docs/handover/contracts/2026-10-27-fold-components.md`; **lane exception, this contract only (Jon, 27 Oct):** theme.css, canon §7.5/§7.6.1, `_config.yml`, the shared scripts, and per-game edits to listed games in the three groups, each claimed first; canon outside those sections stops and asks; `site-footer.css` and `the-6-ps/` are not ours): IN PROGRESS, entry below. **THE-6-PS v2** (Jon's ruling, 25 Oct, via Project Claude): The 6 P's is rebuilt self-contained (its own banks, one stylesheet, no hand-off into games; spec `claude/six-ps-v2-spec-2026-10-25.md` in the project). **Waiting for its build contracts.** STOPPED: all burst work for The 6 P's and contract SIX-PS-SOON. Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). Kept: PR-MEASURED (CI); LOOK-REDS second, after this build (home lane, see home.md). v1 (#531, `docs/history/contracts/2026-10-24-the-6-ps.md`) is what is live at /the-6-ps/, unlisted, until v2 replaces it. **MAIN-WARN** (25 Oct, `docs/handover/contracts/2026-10-25-main-warn.md`): DONE (#548), entry below. **TOP-SCORES**: DONE (#550). **LOOK-REDS-2** (Distinctly Average): DONE (#554), entry below; Prime Sprint waits for Jon's next contract. **BELOW-FOLD-AUDIT** DONE (#556), entry below. **PHONE-FIT-DRIVER** (26 Oct, `docs/history/contracts/2026-10-26-phone-fit-driver.md`, Jon's correction to item 1 appended): DONE (#560), entry below; two rulings now Jon's (the 11-game exception, a start-screen rule). **PR-MEASURED** DONE (#543; `docs/history/contracts/2026-10-25-pr-measured.md`). **SIX-PS-PLAYER** (25 Oct, the first v2 build contract; contract, Project Claude's schema and Jon's three rulings `docs/history/contracts/2026-10-25-six-ps-player.md`): DONE (#535, #536, #538), entry below. **SHAPE-SHIFTER-DATA-MODE** (25 Oct, `docs/history/contracts/2026-10-25-shape-shifter-data-mode.md`): DONE (#526); SHAPE-SHIFTER-SPLIT DONE (#528); their worktrees left for the home lane (end-task.py's `gh pr view` was GraphQL, refused from Claude Code sessions; GH-REST #529). **SWEEP-1** (12 Oct, contract `docs/handover/contracts/2026-10-12-sweep-1.md`): one reading sweep of 96 live games (glorious-gantt skipped), 12 batches of 8 in lowest-level order; findings in each game's file, report `docs/audits/sweep-1-2026-10.md`. **Jon's rulings, 13 Oct** (verbatim: `docs/handover/contracts/2026-10-13-sweep-1-rulings.md`): word-problem-decoder and equation-builder fixed, not unlisted; **equation-builder must merge today, or say so and the home lane unlists it.** quadratic-factoriser DONE (#342, 3ab8cd5; Jon, 13 Oct: fixed, not unlisted). **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). Batches 1-5 DONE (#332, #336, #339, #340, #341); equation-builder DONE (#338). Batch 6 DONE (#343). **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** circle-theorem-spotter DONE (#344, 091b4f0; batch 7's SR-20 hit, fixed under SR-30). Batch 7 DONE (#345). growth-and-decay DONE (#346, 3b2eb76). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h). correlation-or-coincidence DONE (#347, f283457; batch 8's SR-20 hit, B22, B25, B27 replaced on Jon's ruling). Batch 8 DONE (#348, 186aa27). **Batch 9 (all eight reviewed) found two SR-20 levels, each fixed first under SR-30: core-maths-paper2a DONE (#349, 3989aed); stat-attack DONE (#350, 856aa7c). Batch 9 DONE (#351, 6c7c53e; Jon's rulings of 13 Oct and SR-31).** **Batch 10 (all eight reviewed; scratchpad `batch10-notes.txt`) found three SR-20 levels: growth-and-decay (PR open), test-the-claim (wt-tc), graph-sketcher; each its own PR under SR-30, then batch 10 (tax-theft on Jon's ruling).** Then batch 11 (curling-friction, force-resolver, moments-master, log-laws, binomial-blaster, partial-fractions-duel, proof-builder, dimension-checker). Reviewer brief: `docs/handover/contracts/2026-10-12-sweep-1-reviewer-brief.md`.

**Live pointers (kept out of dated entries, Jon 2 Nov; the first four from the 27 Oct entry):**
- **Step 4 from Mon 2 Nov: spec `docs/handover/contracts/2026-10-27-gate-step4-spec.md`** (Jon's ruling verbatim, the approved approach: stub-server default seed, per-verifier seed lists, a nightly non-gating random sweep that adds failing seeds, Take a Walk's `Date.now` seed, `bc.wait_settled` after #583; the audit list of ~45 sites).
- **Step 6:** nothing to clear (the warn list is empty); migrating Factor Theorem (88 s), Growth and Decay (123 s) and Screening Room (94 s) to work units is insurance against the setup median rising again (they passed the limit at 107 s); Jon to say.
- **Queue after the freeze (each needs main merged in):** FOLD PR 3 `claude/fold-options-v2` (`/home/user/wt-fo`, 44a4ef8) -> PR 4 `claude/fold-figures-v2` (`/home/user/wt-lf`, 227c3d6) -> PR 5 `claude/fold-canon` (`/home/user/wt-fc`, 4a526a6) -> PR 6 `claude/fold-publish` (`/home/user/wt-fp`, ed00d80; NOT merged: Project Claude's live 404 check). KEYPAD-FRACTION `claude/keypad-fraction` (`/home/user/wt-kp`, fbf6c36: 799dbfd9 cherry-picked + 4 plants; phone-fit on the 19 keypad games identical to main in all three modes; check-changed: no new failure). Then measure-phone-fit on `wait_settled` (after #583), queue item 6. FOLD-COMPONENTS' and SHARD's entries are in the archive (moved 27 Oct).
- **Worktrees to clear by end-task.py once their PRs merge:** wt-sh (#578), wt-jsn (#588), wt-mp (#582); scratch: wt-kpm, wt-seed, wt-ref, wt-main-da.
- (2 Nov: each branch above is on origin at its commit; the `wt-*` worktrees went with an earlier container.)
- **Queued, Low (Jon, 2 Nov, after GATE-FIX):** merge-pr.py counts "the newest merge has no run of its own" as red even under `--wait`, so in the seconds before GitHub registers a new merge's run it refuses ("start one by hand") instead of waiting. Fix: count it as unfinished for a short grace period (about 5 minutes after the commit), with a plant.
- **Home-lane queue (Jon, 2 Nov):** `scripts/check-banks.py:25` has an invalid escape `\(` (ci-deps.py's `ast.parse` warns on Python 3.12+). Harmless.
- **For Project Claude to triage (4 Nov, SEARCH-KEYWORDS ruling 6):** spec-map rows the banks do not teach (57 games) and possibly short banks: listed in the entry "SEARCH-KEYWORDS triage lists" (archived unchanged when it moves) and `docs/search-keywords-review.md`.
- **For the home lane, canon §7 (SEARCH-KEYWORDS, 4 Nov):** card search has one rule, `MaffsSearch.match` (`schools/assets/search.js`): card text plus `data-keywords`, every word, a trailing s dropped past 3 letters; the portal and card-filter.js call it. Keywords live in games.json (`keywords`; The 6 P's on its `pages` record), written by apply-meta.py, held by check-meta.py. The portal's `#noResults` now sits outside the grids (it was hidden with them).
- **For the home lane (ROOM-ESCAPED, 4 Nov):** canon §1.4 item 5 says rooms "escaped (`game_completed`)"; from endpoint `2026-11-04-a` an escape is a `game_completed` with `questions_correct` = `questions_answered` > 0, any other is "timed out" (its own column).
- **For the rulebook queue (Jon, 3 Nov; no change now):** end-task.py always refuses in cloud sessions, which work in the primary checkout ("is checked out in the primary checkout", after #643); cloud cleanup is nothing to do (the container ends, GitHub deletes the merged branch).

SWEEP-1-RULINGS (13 Oct, contract and Jon's two documents verbatim in `docs/handover/contracts/2026-10-13-sweep-1-rulings-2.md`): Jon approved the triage in full (20:35): standing rules R1-R9 (SR-33, below), 18 Part 2 rulings, Part 3 deferrals; R10 is the home lane's (contract LEVEL-LOGGED). Order: step 0 record, step 1 split bundled entries, step 2 R4 money check, step 3 per-game fixes (Year 6, KS3, Essentials at GCSE, other GCSE, Core, A-Level, L4), step 4 proportion-blaster-003 class count.
ESSENTIALS-SCREEN-TRUTH-2 (18 Oct, contract `docs/history/contracts/2026-10-18-essentials-screen-truth-2.md`): four listed Essentials games whose screens show something untrue or unreadable, one game per PR, each claimed on the remaining list first: 1 formula-plug-in DONE (#441); 2 new-shapes DONE (#442); 3 four-quadrant-explorer DONE (#443); 4 shape-shifter DONE (#445; Jon's ruling (a), 19 Oct); then (Jon, 19 Oct) 5 formula-plug-in and 6 new-shapes: header "Q{n} of {N} · {right} right". Rulings verbatim at the end of the contract file.
ROOM-CREDIT v2 (19 Oct, contract and v1 verbatim `docs/history/contracts/2026-10-19-room-credit.md`; Jon's lane exception plus his rating.js ruling): one optional room.js `credit`, drawn on the room and teacher pages, checked on the hub and front-page cards; four rooms credited. **DONE (#446, 9a94e78, merged 12:33 BST).**
PYTHAG-REPORT (19 Oct, contract `docs/history/contracts/2026-10-19-pythag-report.md`, research only): **DONE (#447)**; report `docs/handover/pythag-report.md`, for Jon's ruling on a "Formula only" mode. Then ruling (2) of 19 Oct: formula-plug-in DONE (#449, 531c988); new-shapes DONE (#450, e0377e9).
MONTY-CARD (19 Oct, contract `docs/history/contracts/2026-10-19-monty-card.md`; Jon's ruling on the phone gap at its end): the "100 Doors" card states its setup and condition; step 3 list in the entry below. **DONE (#448, b973e23).**
**START HERE (next session; written 19 Oct, 18:10 BST).**
- **Done lists and main-run history to 24 Oct:** moved to `docs/history/handover-cloud-archive.md` (27 Oct, size limit).
- **Waiting on Jon, the list of 20 Oct (fact cards, Monty Hall card, PYTHAG-REPORT, phone header stacking):** in `docs/history/handover-cloud-archive.md`, moved 27 Oct.
- **Container setup (every fresh session):** `pip install playwright==<the version in /opt/node-tools/node_modules/playwright-core/package.json> sympy mpmath pyyaml` (1.63.0, browser revision 1243, on 25 Oct; a pinned 1.56.0 looks for a browser the container does not have and fails every Chromium check); `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1` for what imports it (`bank_common.py` and some verifiers). **No check-changed.py before a push (AGENTS.md, CLOUD-LEAN):** before the first push only the worst-case test where canon §7.8.4 requires it by hand, and the selftest of any script changed; the PR's Gate is the check. Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/handover/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

## 2026-11-04 (cloud): SEARCH-KEYWORDS (`docs/handover/contracts/2026-11-04-search-keywords.md`, Shared, lane exception; stops at a green Gate for Project Claude's review and Jon's "merge")

- Agent: Claude Code. Primary checkout `/home/user/maffsgames`, branch `claude/sleepy-shannon-itnz0v` (restarted from main a7b476c after #656; claim 7e2bb09).
- Built: keywords on all 107 games (drafted from each bank, spot-checked; `docs/search-keywords-review.md`), The 6 P's on its `pages` record (Decided for you: STOP IF 1, it is a page with a record, not a game); check-meta.py keyword and card rules, 20/20 selftest plants; apply-meta.py writes data-keywords (124 portal, 38 Essentials cards; idempotent); `schools/assets/search.js` the one matcher; `scripts/verify-search.py` (19 queries, 3 plants). The portal's no-results message was inside a grid applyFilters hides, so it never showed: moved out (own commit 2fe55bb). /updates/ line.
- For Project Claude: 57 games' spec-map rows claim topics their banks do not teach, and a few banks look small (Estimation Golf ~9 a level, Percentage Flip 12, 52-dle ~20): listed in the review doc, not edited.
- **STOP (resolved by Amendment 1):** `scripts/verify-new-and-updated.py:123` derives the portal's search results with the old rule (`search in c['text']`), so under the shared matcher it fails on "pies" (How Many Parts? now matches: "pie" is in its "pieces"). Outside the lane exception, so asked.
- Local: check-meta OK + selftest 20/20; verify-search OK (3/3 plants); verify-card-filter OK after its search check reads data-keywords too; verify-circle-theorem-spotter PASS.
- **Amendment 1 (Project Claude for Jon, 4 Nov, verbatim in the contract):** verify-new-and-updated.py and verify-card-filter.py now ask the page's MaffsSearch.match (no second copy of the rule; both pass, new-and-updated --selftest 3/3); keyword review approved; resit on Linear Equation Solver kept; decisions accepted; triage lists in the next entry.
- **State:** PR #657, Gate pending; then Jon's "merge".

Record: agent Claude Code; wall pending; review cycles 0; amendments 1; usage n/a.

## 2026-11-04 (cloud): SEARCH-KEYWORDS triage lists (Amendment 1, ruling 6: for Project Claude to triage; not in #657)

*Spec-map rows the banks do not teach* (found while drafting keywords; `spec-map/` not edited; "not taught" is the drafting read of each game's bank):

- `sequence-solver`: Spec row 'LO1: Arithmetic and geometric progressions, series' (BTEC/HNC) is listed, but the game has no L4 level (levels KS3, GCSE, A-Level only).
- `estimation-golf`: Mixed bank: Year 6 is general-knowledge facts (days in a year, legs on a spider), not estimation maths; A-Level and L4 are assorted calculations (trapezium rule, RMS voltage). Spec '§3.3 Fermi estimation' is only touched by one or two items (heartbeats in a year, seconds in a day); 'LO1 number theory, fractions' is not taught. Banks are 9 per level (20 for Year 6).
- `factor-race`: Spec N4 also names primes, HCF, LCM and prime factorisation, none of which this game asks.
- `prime-factorisation`: Spec N4 also names HCF and LCM; the game does not ask for them.
- `prime-or-composite`: Spec N4 also names HCF, LCM and prime factorisation; not asked.
- `percentage-flip`: Spec N12 'percentage change' and N10-N11 'interconversion' are not taught: the game only finds a percentage of an amount. Banks are small (12 default, 20 Year 6).
- `fraction-equivalence`: Spec N2 'four operations with fractions' is not taught (no fraction arithmetic); N10-N11 interconversion only via one example (1/2 = 0.5).
- `52dle`: Only about 20 puzzles in the list, one per day.
- `constructions-lab`: Spec G9 also names bearings; the game has no bearings task.
- `split-it`: Spec R9 also names percentage increase/decrease; not in this game.
- `word-problem-decoder`: Keywords deliberately avoid the individual topic names: the game asks students to name the topic, not to do it.
- `equation-builder`: 'btec' used because the Level 4 tier is HNC/BTEC Level 4 (canon level table).
- `truth-buster`: No spec rows in the input for this game.
- `terrible-advice`: The input search_phrase 'Financial Maths Mistakes' overstates the money content: the advisers are money-themed characters, but most questions are general misconceptions (fractions, angles, sequences, area); only a handful are financial (compound interest, loan repayment, best value, break-even). No 'financial maths' keyword proposed.
- `negative-number-line`: Spec N2 names decimals, fractions and mixed numbers and N1 names ordering decimals and fractions: the game uses integers only (plus 0.5 and -0.5 to place). It never adds or subtracts a negative number, so no 'subtracting negatives' keyword.
- `formula-plug-in`: Spec G16 names parallelograms, trapezia and prisms: the game has only triangles, rectangles, squares and cuboids.
- `decimal-detective`: Spec N14-N16 names estimation and error intervals; the game has no estimation or error intervals, only rounding.
- `like-terms-collector`: Spec row A4 wording 'laws of indices in algebra' is not taught: the bank has no powers at all (collecting like terms only).
- `shape-shifter`: Roster says 4 modes; the page also has an Enlargement mode (5 cards). Spec G7 row omits enlargement, which the game does teach.
- `new-shapes`: Spec row G16 also lists area of triangles; the bank has no triangle questions.
- `higher-power`: Spec row N14-N16 (rounding, error intervals) is not taught: the game compares magnitudes, no rounding or error intervals. N6 fits.
- `prisoners-dilemma`: Spec row §3.10 cost-benefit analysis is tenuous: Core level reframes the payoff matrix as competitor pricing, but there are no cost-benefit questions; not used for keywords.
- `seven-bridges`: Spec row DA1-DA2 also lists Hamiltonian graphs; the game has no Hamiltonian content.
- `index-laws`: Spec row LO1 also names logarithms; this game has no logarithm questions.
- `quadratic-factoriser`: Spec row B3 lists completing the square; the game does not teach it.
- `trig-wars`: Spec rows G20-G21 (Pythagoras, exact values) and E1-E7 (radians, identities, compound angles, equations) are not taught; only sin/cos components of a velocity. Q5 projectiles fits.
- `trig-worms`: Spec rows E1-E7 (radians, identities, compound angles) and the Pythagoras/exact values part of G20-G21 are not taught; also LO2's sine/cosine rules and radians.
- `modular-battle`: Spec ref looks mislabelled: DfE GCSE N5 is systematic listing/product rule, not remainders; modular arithmetic is not named in the GCSE content.
- `proportion-blaster`: Spec row R9 (percentage increase/decrease) is barely taught: one item asks the percentage change in y when x rises 50%; the bank is direct/inverse proportion (DfE R10, R13) and ratio sharing (R5).
- `circle-theorem-spotter`: Spec ref looks mislabelled: in the DfE GCSE content circle theorems are G10; G17 is circumference/area of circles and volumes.
- `probability-paradox`: Spec rows S1-S4 (averages, data representation), I1-I3 (sampling, data presentation, measures of location/spread) and LO4's distributions/hypothesis testing are not taught; §3.9 Expectation is tenuous (only the envelope paradox). J1-J3 fits.
- `graph-transformer`: Spec ref looks mislabelled: DfE GCSE A13 is translations/reflections of graphs; A14 is graphs in real contexts, which this game does not teach.
- `bearing-blitz`: Spec row G9 (constructions, loci) is not taught; only bearings. The DfE ref for bearings is G15, not G9.
- `scale-factor-scaling`: Spec ref looks mislabelled: in the DfE GCSE content this is R12/G19; R6 is expressing a multiplicative relationship as a ratio or fraction.
- `correlation-or-coincidence`: Spec rows M1–M3 (PMCC) and §3.7 (PMCC, regression lines) are not taught: the bank has no PMCC, regression or line of best fit, only correlation vs causation. Not used for keywords.
- `chart-interrogator`: Spec row S1–S4 mentions probability; the game teaches no probability (diagrams and averages/spread only).
- `given-that`: Spec row §3.9 (Expectation) is not taught: the bank has no expected value questions.
- `screening-room`: Spec row §3.9 (Expectation) is not taught, and J1–J3's Venn and tree diagrams are not used (icon arrays and Bayes only); only the conditional-probability part fits.
- `linear-equation-solver`: 'resit' included because the content is GCSE Foundation equation-solving fluency; the game is not in the Resit Fluency Strand, so drop it if the reviewer reads the rule narrowly. Unknowns on both sides are not in the bank ('unknown either side' means 19 = 2x + 9).
- `stat-attack`: Spec row LO4 (probability, distributions, hypothesis testing) is not taught; only grouped-data summary statistics are.
- `graph-sketcher`: Spec row A14 mentions graph transformations; the bank has none (the only 'transform' hits are CSS). 'Graphs in real contexts' fits.
- `glorious-gantt`: Page shows a 'We're correcting this game' notice (some critical-path answers wrong); keywords describe the topic regardless. No spec rows in input.
- `differentiation-duel`: Spec rows G5–G6 (differential equations part) and Q4 (calculus in kinematics) are not taught: no differential equations or velocity/acceleration items in the bank.
- `suvat`: Spec rows Q4 (calculus in kinematics, v = dr/dt) and LO2's 'calculus in mechanics' are not taught: the bank has no calculus.
- `binomial-blaster`: Roster topics include Statistics, but the bank has no binomial distribution; all questions are the binomial expansion (pure).
- `partial-fractions-duel`: Spec row H1-H8 (integration by parts, substitution, partial fractions) does not fit: the bank only decomposes into partial fractions and never integrates.
- `proof-builder`: Spec row A1-A5 lists proof by exhaustion; no exhaustion proof is in the bank.
- `normal-navigator`: Spec row L1-L3 (statistical hypothesis testing) does not fit: no hypothesis testing in the bank. LO4 fits only for its distributions part.
- `truth-will-set-you-free`: Spec row LO1 includes logic simplification; this game builds and matches truth tables but does not simplify expressions (Boolean Blitz does).
- `complex-converter`: Spec rows B1-B3 (conjugates, arithmetic), B4-B7 loci and B8-B11 (de Moivre, nth roots of unity) are not in the bank; it only converts forms and plots on the Argand diagram.
- `matrix-crunch`: Spec row C1-C4 (matrix arithmetic, transformations, invariant points) is not taught; C5-C6 fits only for 2x2 (no 3x3 in the bank).
- `characteristic-quest`: Spec row C10-C11 includes diagonalisation, which none of the eigen trilogy teaches.
- `eigenvalue-extractor`: Spec row C10-C11 includes diagonalisation, not taught.
- `eigenvector-engine`: Spec row C10-C11 includes diagonalisation, not taught.
- `free-daily-pizza`: Spec rows N12 (percentage change) and R9 (percentage increase/decrease) do not fit: no increase, decrease or percentage change in the bank.
- `y-so-steep`: Stage 3 (rearranging) is off until fractions are enabled, so no rearranging keyword is given.
- `take-a-walk`: Spec row G16 mentions trapezia and volume of prisms; neither is in the bank (circles, G17, would fit and is not listed).
- Reference numbers that look wrong against the DfE GCSE subject content (the drafting note for batch 2): circle theorems are G10, not G17 (G17 is circle area and circumference); graph transformations A13, not A14; bearings G15, not G9; area and volume scale factors R12/G19, not R6; proportion R10/R13, not R9; modular arithmetic is listed under N5 (systematic listing).

*Possibly short banks* (from the drafting notes; not counted further, may be under the 40-question minimum): Estimation Golf about 9 a level (20 for Year 6); Percentage Flip 12 (20 for Year 6); 52-dle about 20 puzzles, one a day.


## 2026-11-04 (cloud): ROOM-ESCAPED (`docs/history/contracts/2026-11-04-room-escaped.md`, Shared; stopped at a green Gate for Project Claude's review and Jon's "merge")

- Agent: Claude Code. Primary checkout `/home/user/maffsgames`, branch `claude/sleepy-shannon-itnz0v` (from main 921f7fb; claim ee2c446).
- Built: `rptEscaped()` in the endpoint: a room `game_completed` is an escape only when `questions_correct` = `questions_answered` > 0 (both numbers); any other is "timed out", counted per room and shown in the email line and a Dashboard column. `SCRIPT_VERSION` `2026-11-04-a`; redeploy note (no new permission). Test: a 3/3 win, a 1/3 and a 0/3 timeout give 1 escaped, 2 timed out; new plant (every completion an escape) CAUGHT; 29 checks, 5 plants.
- STOP IF 1 checked from code, not the Sheet (the Drive connector cannot return a 1.1 MB sheet into a session): the engine has sent both fields as numbers since at least 15 Oct and is unchanged since 24 Oct. STOP IF 2 clear. Details in the contract file.
- **Jon's redeploy step after the merge:** new version of the existing deployment; `/exec` reports `2026-11-04-a`.
- **State:** DONE. MERGED #656 (a7b476c) on Jon's Amendment 1; merge-pr.py exit 0, last line `main a7b476c run 41800889964: GREEN`. Jon's redeploy to `2026-11-04-a` is his step. Amendment 1 ("merge on green please"); Project Claude's review after the merge. Jon checked the Sheet (4 Nov): no blank J/K in the 7 days; blanks from ~29 Sep back, outside every window the rule reads.

Record: agent Claude Code; wall pending; review cycles 0; amendments 1; usage n/a.

## 2026-11-03 (cloud): DASHBOARD-METRICS (`docs/handover/contracts/2026-11-03-dashboard-metrics.md`, Shared, Amendments 1 and 2; stops at a green Gate for Project Claude's review and Jon's "merge")

- Agent: Claude Code. Primary checkout `/home/user/maffsgames`, branch `claude/stoic-galileo-xvzt45` (from main af8e737).
- First stopped at STOP IF 2 (`data/` is not published, so maffsgames.co.uk/data/games.json 404s); Jon's Amendment 2 (3 Nov): read it from raw.githubusercontent.com, publish nothing.
- Built: `answer_kind: "shot"` on trig-wars and bearing-blitz (survey of every question_answered call); endpoint `2026-11-03-b`: one model (`rptBuild`) feeds the email and the Dashboard: question-game accuracy (min 30), hardest by game + level + question_id (min 10), Escape Rooms table, shot games on one line, a one-line games.json-failure fallback, pre-29-Sep blanks wrong; `isMarked` replaced. `scripts/test-apps-script-report.py` (ci-line): 28 checks and 4 plants. Canon §1.2, §1.4, §12; redeploy notes.
- **STOP IF 1, for Jon:** Prisoner's Dilemma's question_answered is neither an answer nor a shot (`correct: null`, one row a round); the report leaves it unmarked, as before. Bearing Blitz set as shot is a borderline call (a hit is within 5° of the bearing).
- **Jon's redeploy step after the merge:** new version of the existing deployment (`docs/apps-script-redeploy.md`), accept "Connect to an external service"; `/exec` reports `2026-11-03-b`.
- **State:** PR pending, Gate pending.

Record: agent Claude Code; wall pending; review cycles 0; amendments 2; usage n/a.

## 2026-11-03 (cloud): SEQ-SOLVER-WORKED (`docs/history/contracts/2026-11-03-seq-solver-worked.md`, Shared)

- Agent: Claude Code. Primary checkout `/home/user/maffsgames`, branch `claude/stoic-galileo-xvzt45` (from main 03acf76; first commits ff2c555 DASHBOARD Amendment 1, 0e2b471 closes SEQ-SOLVER-FIXES).
- Built: a `worked` field (1 to 3 steps) on all 154 items, question text untouched (ids unchanged); shown under the options on a wrong answer, before Next, in the house "How it goes" list. Phone rule during that feedback: calculator and the two unpicked distractors hidden, HUD and card compacted. Verifier: every worked line checked against its own item (251 equalities, 81 difference and ratio claims, every key), the panel order in Chromium, Next above the fold on all 462 wrong answers at 320, 375, 390 (and Aa 375, 390); 15/15 plants.
- **State:** MERGED #654 (af8e737) on Jon's "merge" (Gate green on 097b053, run 41716406405); main green: `main af8e737 run 41722042176: GREEN`. Contract moved to `docs/history/contracts/`. Survey for Jon (PR body): of 100 other listed games, 63 explain a wrong answer, 24 do not, 11 partly, 2 n/a.

Record: agent Claude Code; wall 4:58 (received 16:05; queued behind SEQ-SOLVER-FIXES until 20:05; handed off 21:03); review cycles 0; amendments 0; usage n/a.

