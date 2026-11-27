# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-27 (home): NEXT-NO-FALLBACK (the shared Next control no longer advances by itself; canon §7.6 says so, and that a revealing right answer waits too)

Claude Code (home lane), worktree `~/mg-next-no-fallback`, branch `claude/next-no-fallback`. The contract is at `docs/handover/contracts/2026-11-27-next-no-fallback.md` (verbatim). The first commit closed out MERGE-GUARD.

- **Jon (27 Nov 2026, 18:27):** "I'd remove the auto advance … the student needs to press continue, it gives them a chance to check where they went wrong, and write down the correct method before moving on".
- **The helper (`schools/assets/next-control.js`):** no timer unless `fallbackMs` is passed; the 20 s default and the exported `FALLBACK_MS` are gone (nothing read the constant but canon). `fallbackMs` stays for test harnesses. The floor, the in-view scroll, advance-once, clear(), the 44 px target and the MaffsLock clearing are untouched.
- **The seven pages:** the-6-ps, take-a-walk, squared-squirrel, just-pythag-it-bruv, how-many-parts, 52dle and distinctly-average no longer pass `fallbackMs` (the NO_FALLBACK constants and the day-long literal are gone). Nothing else in them changed.
- **The guard, in `scripts/test-next-control.py` (the "Shared asset tests" job, which runs on every PR):** a static scan fails on any `.html` or `.js` under games/, escape-rooms/, the-6-ps/ or any page in the site root that names `fallbackMs` (plant: a page passing `fallbackMs: 20000`, caught); with no `fallbackMs` the control does not advance in 90 s on a fast clock (the page's setTimeout at 1/100) and Enter still advances once (plant: the 20 s default restored, caught). The existing fallback cases already passed `fallbackMs` themselves.
- **One verifier changed, because it held a page's workaround:** `verify-just-pythag-it-bruv.py` required the worked example's Next to be given the day-long delay; it now requires that the page passes none.
- **One check relied on the 20 s default, and now advances for itself:** `check-teacher-invite.py` plays factor-theorem to its results screen, and its step never pressed the shared Next (its harness cut every timer to 25 ms, so the fallback moved it on). The first Gate (check-site 46053172613) failed there. The step now presses Next; what the check tests, the teacher line on the results screen, is unchanged. The same Gate also failed Text writes (the new test's two planted files were written without newline=''; fixed) and one job on a Docker pull.
- **Canon §7.6:** a wrong answer waits with no timer (Jon's reason); the new line on a right answer that reveals something new, in the contract's words; the three other mentions of the fallback in the section now say "a test's `fallbackMs`".
- **Stale words fixed:** `check-answer-lock.py`'s docstring and `docs/sandbox-checks.md` spoke of the 20 s fallback. `scripts/check-site.py:2680` still does, in a comment; that file is the cloud lane's.
- **A wrong answer advanced by a page's own timer (the contract's STOP IF list; none changed here):** trig-wars (a miss shows its tip for 2.8 s and passes the turn; exempt by Jon's ruling of 19 Nov) and higher-power (a wrong guess ends the run). correlation-or-coincidence falls back to 4 s only if next-control.js did not load. CI's pause check (WRONG-PAUSE-NEXT) holds every other judged game for 3 s; a scan of the pages for timers of 3 s or more found no other. Six games that check cannot judge are on its own list (WRONG_PAUSE_UNCHECKED).
- **/updates/:** one line, 27 Nov.
- **Run IDs and the merge:** in the close-out, as usual.

Record: agent Claude Code; wall 0:45; review cycles 0; amendments 0; usage n/a.

## 2026-11-27 (home): MERGE-GUARD (merge-pr.py refuses a PR whose Gate or phone-fit run started before main's newest merge)

Claude Code (home lane), worktree `~/mg-merge-guard`, branch `claude/merge-guard`, PR #935. The contract is at `docs/history/contracts/2026-11-27-merge-guard.md` (verbatim). Shared tier: it stops at Gate green for Project Claude's review and Jon's "merge". The first commit closed out BASE-60-TIDY.

- **Jon (27 Nov 2026, 17:57):** "merge script please".
- **(a''), new, in `scripts/merge-pr.py`:** M is main's newest merge as (b') picks it (bot skip-marker commits passed over). If M is the PR's head or an ancestor of it (compare M...head reads "ahead" or "identical"), it passes. Otherwise the Gate's run and the phone-fit run must each have been created after M's committer date, or the merge is refused, naming M and the run. The Gate's time is its workflow run's created_at, found by check suite; the Gate check's own started_at (the end of the run) is never read.
- **Red, never waited on:** judged every poll with (a) and (a'), also while a run is still going; --wait does not wait on it and --override does not waive it.
- **The record behind the fixtures:** #930's runs were created at 17:16:26Z on 26 Nov, #927 landed on main at 17:35:08Z, the Gate check started at 17:37:25Z and #930 merged at 17:52:57Z. Ids, shas and those times in the selftest are GitHub's.
- **Selftest:** 17 new cases and 4 plants (the check removed; the Gate's started_at for its run's created_at; bot skip-marker commits counted as M; the ancestor test inverted), each caught. The 108 lines the selftest printed before are printed unchanged.
- **Decided here, for review:** (1) a run created in the same second as M is refused (not after it); (2) under --override, which waives (b'), an unreadable M is refused by (a'') itself, so the override cannot pass an unjudged PR; (3) a Gate check that cannot be tied to a run, or an unreadable compare or commit, is refused, never guessed; (4) the selftest's fake API moves a phone-fit script on once per poll, not once per read, since two checks now read those runs in a poll.
- **Not touched:** (a), (a'), (b), (b'), (c), the watch, --head, the retries, the merge PUT; every workflow; `serve-stubbed.py`, `bank_common.py`.
- **AGENTS.md:** the stale-Gate rule gains "merge-pr.py enforces this (MERGE-GUARD, 27 Nov 2026)".
- **Gate on the PR head f038472f:** check-site 46046955243 and phone-fit-full 46046955221, both green.
- **Merged** on Jon's "merge", 27 Nov at 18:30 UTC, as b6c0119 (#935, squash) via merge-pr.py, which ended "main b6c0119 run 46049988829: GREEN". Main on b6c0119: check-site 46049988829, phone-fit-full 46049988775 and the pages build 46049988366, each success.
- **Departure, as the lane reported it:** the contract said main's current script judges this merge. merge-pr.py was run from the PR's worktree, so the new version judged its own merge; the new check passed (main's newest merge, #934, was in the branch) and every existing condition was applied unchanged.

Record: agent Claude Code; wall 0:50; review cycles 0; amendments 0; usage n/a.

## 2026-11-26 (home): BASE-60-TIDY (Base 60's cuckoo rides out on a perch joined to its clock; the page's stale comment; spec-map row N13 names time)

Claude Code (home lane), worktree `~/mg-base-60-tidy`, branch `claude/base-60-tidy`, PR #932. The contract is at `docs/history/contracts/2026-11-26-base-60-tidy.md` (verbatim). The first commit closed out BASE-60-LIST.

- **Jon (26 Nov 2026, 19:51):** "the cuckoo clock looks much better alhough the cuckoo is not attached to the clock when it pays a visit".
- **The perch:** a thin level arm (`.ck-perch`, cream with a dark edge, as the bird is drawn) from inside the doorway (x 36 of the drawing) to under the bird's body (x 7). It grows out of the doorway and back with the bird, on the same times and easing, and is hidden at no length when the bird is in. The bird's own movement, timings and shape are unchanged; it bows and droops on the arm, which stays level.
- **Decided here:** the arm extends from the doorway; it does not slide as a fixed-length piece. A fixed-length arm sliding with the bird would stick out of the far side of the house while the bird is in, and past the drawing's edge. Measured every 20 ms of a right answer and through a wrong answer's transition at 1366x768, 320x568 and 1920x955: the bird is on the arm whenever it shows.
- **The drawing's box does not grow** (the arm lies inside the bird's reach), so the clock's size, the fold figures and `data/large-screen.json` are untouched.
- **Verifier:** the bird units also hold the perch showing and within 1 drawing unit of the door's box and the bird's at each sampled moment of the hold, after a wrong answer and in both reduced-motion states. Two plants: the perch removed, and the perch left behind at the door. Run locally: both bird units pass, both plants and the two older bird plants caught.
- **Page comment and spec map:** the UNLISTED comment is now "Listed 26 Nov 2026 (contract BASE-60-LIST, PR 930)." ("PR 930", not "#930": the first Gate, check-site 45887805820, failed only on the Theme check, which read "#930" in the page as a hex colour outside :root); row N13 reads "Standard units and conversions: length, area, volume, mass, time", its games unchanged.
- **Screenshot** (the bird out on its perch at 1366x768): in the report to Jon; no image is committed.
- **Gate on the PR head d5417e8f:** check-site 45892119116 and phone-fit-full 45892119126, both green. Main was merged in twice while the PR waited (9f51bb8d, then eaf158af), and the Gate re-ran each time, as the contract's step 6 asked.
- **Merged** on 26 Nov as 60fb649 (#932, squash) via merge-pr.py, which ended "main 60fb649 run 45894195608: GREEN" (the line as the lane reported it to Jon on 26 Nov; this file did not hold it). Main on 60fb649, read from GitHub Actions on 27 Nov: check-site 45894195608, phone-fit-full 45894195615 and the pages build 45894194832, all success.

Record: agent Claude Code; wall 0:40; review cycles 0; amendments 0; usage n/a.

## 2026-11-26 (home): BASE-60-LIST (It's Just Base 60, Bruv is listed: portal, /essentials/, sitemap, spec map, hub, /updates/)

Claude Code (home lane), worktree `~/mg-base-60-list`, branch `claude/base-60-list`, PR #930. The contract is at `docs/history/contracts/2026-11-26-base-60-list.md` (verbatim). The first commit closed out CANON-PRIORITY.

- **Approval (Jon, 26 Nov 2026, 13:36):** "Base 60 looks fine, happy to list that, although I will check the lines".
- **Portal:** a card in KS3 and in GCSE, each a copy of Take a Walk's (New badge dated 2026-11-26, levels ks3 gcse, topic number, the keywords of `data/games.json`), placed last in its section: both sections are in listing order, newest last.
- **/essentials/:** one card in Number, after Unit Converter (the same reference, N13), "One level", `data-calc="non-calc"`. `scripts/check-resit-page.py`'s SUITE gains the slug in the same place, as that check's own rule requires (the suite and the page change together).
- **Spec map:** added to the N13 row. N13 is the DfE's "standard units of mass, length, time, money"; the row's own wording, "Unit conversions: length, area, volume", does not name time and is left as it is. For Project Claude: reword the row, or rule otherwise.
- **Hub:** a row with stage-1..stage-4, after How Many Parts?. The NOT_ON_HUB entry is gone; no override entry is needed (the check reads the four keys from the page).
- **Sitemap, /updates/, the roster** (row 116 in Resit Fluency Strand, 8 games; Unlisted, 8; "Look signed off by Jon, 2026-11-26."), and the two notes in `audit-register.py` and `check-theme.py`.
- **`docs/todo.md`:** BASE60-LIST rewritten to Jon's lines, its old row word for word in `docs/history/todo-done.md`; new row BASE60-AA-FOLD, without figures (Project Claude's follow-up of 26 Nov, 17:15: #929 had not merged, so the row points to the verifier's known list).
- **Not touched:** the game page, its verifier, `data/large-screen.json`, `data/games.json`.
- **Gate on the PR head 8cd19935:** check-site 45866316754 and phone-fit-full 45866316762, both green.
- **Merged** on 26 Nov as e367eb4 (#930, squash) via merge-pr.py, which ended "main e367eb4 run 45871430050: GREEN". Main on e367eb4: check-site 45871430050, the pages build 45871429603 and phone-fit-full 45871430115, all green (read back from the API).
- **MERGE TIMING slip (this lane's):** #927 (LARGE-SCREEN-LAYER) merged at 17:35 while merge-pr.py waited, left unattended. The contract said to merge main in and re-run the Gate first; it merged on the Gate from before #927 landed. Main's run on the combined state is green.

Record: agent Claude Code; wall 0:45; review cycles 0; amendments 0 (one follow-up); usage n/a.

## 2026-11-26 (home): CANON-PRIORITY (Jon's new priority order in canon §0.2; SR-35, playability beats personality on a phone; three backlog changes)

Claude Code (home lane), worktree `~/mg-canon-priority`, branch `claude/canon-priority`, PR #928. The contract is at `docs/history/contracts/2026-11-26-canon-priority.md` (verbatim). The first commit closed out DAILY-DEAL. Docs only.

- **Jon's rulings (26 Nov 2026, 13:40-14:14):** his own classes come second, after correctness; resit and grade 1–3 students are the core audience, with primary served through SR-33; on a phone, playability beats personality; Holey Moley folds into I Dropped My Ice Cream; "d by dx? Why?" is wanted for an assessment in about the 3rd week of January.
- **Canon §0.2:** seven priorities in place of six, in the contract's exact words. SR-33 now cites priorities 3 and 7. No other file cites a numbered §0.2 priority (searched canon, AGENTS.md, CLAUDE.md and `.claude/rules/`).
- **Canon §0.3:** SR-35 after SR-33. SR-34 stays reserved (todo LARGE-SCREEN-LAYER).
- **`docs/todo.md` §3:** new rows ICE-CREAM-GCSE and D-BY-DX; ICE-CREAM-LIST now waits for ICE-CREAM-GCSE.
- **Holey Moley:** its line is removed from "Game ideas, not yet built". The list keeps no record of folded ideas, and ICE-CREAM-GCSE names it.
- **First Gate on the PR head 18526de8, a flake:** check-site 45855085400 failed only on the PR budget (`verify-maffscards.py` part 1 at 201 s against 189 s; the close-out's contract move selects that verifier) and passed on Jon's full rerun; phone-fit-full 45855085259 green. merge-pr.py had refused on the first result.
- **Merged** on 26 Nov as a55da6b (#928) via merge-pr.py, which ended "main a55da6b run 45861149266: GREEN". Main on a55da6b: check-site 45861149266, phone-fit-full 45861149106 and the pages build 45861148815, all green (read back from the API).

Record: agent Claude Code; wall 0:25; review cycles 0; amendments 0; usage n/a.

## 2026-11-25 (home): DAILY-DEAL (MaffsCards gets "Today's deal": one deal a UK day, the same for everyone, with Jon's result on it)

Claude Code (home lane), worktree `~/mg-daily-deal`, branch `claude/daily-deal`, PR #919. The contract is at `docs/history/contracts/2026-11-25-daily-deal.md` (verbatim, as reissued by Amendment 1). No close-out rode on the first commit: MAFFSCARDS-CHALLENGE's is in #916, which stays open (Jon's ruling).

- **Jon's rulings (25 Nov 2026, 19:16-20:05):** a daily deal with his own result on it, set from a Google Sheet; a new Creator sheet with its own script; a Sheet line over 240 characters is skipped for a pool line; "Today's deal" at the top of the menu.
- **The deal:** the UK date (Intl, Europe/London) goes through the page's mix32 to a seed; the day's code is that seed at main / ten / hard, played through `deal(ch)` as a challenge. Normal and challenge play are unchanged (the recorded normal games still match).
- **Jon's result:** `games/maffscards/daily.json`, all nulls as committed. It shows only on its own UK date; a missing, unreadable or invalid file reads as not played.
- **The workflow:** `.github/workflows/maffscards-daily.yml`, started by hand only, runs `scripts/set-maffscards-daily.py` and commits the file as answer-counts.yml commits its figures. The four fields reach the script through the environment.
- **The Creator sheet:** `docs/apps-script-creator.js` and its runbook `docs/apps-script-creator.md`. No token, secret or Sheet id is in the repo.
- **Verifier:** units `pool`, `daily`, `dailyui`, `dailyfit` and six planted faults in their own unit, `dailyplants`; twenty-two plants in all, each caught.
- **Decided here (each for Project Claude's review):**
  - The repo has no personal-details check to call (the list is private, outside the repo), so the script drops a line holding an e-mail address, a web address, an @name or seven or more digits.
  - A daily game's detail ends " · challenge · daily" (challenge is still true).
  - A drawn daily game (not reachable in practice) reads "Nobody won this time."
  - The panel's one fixed sentence is a placeholder: "One deal a day, the same for everyone: main deck, first to 10, Marvin on Hard."
  - In Aa on a phone the panel's text is .8rem, so a 240-character line and the button fit one 320 x 568 screen.
  - The script also has `--check` (the committed file is all nulls or a valid result), run in CI beside `--selftest`.
- **The workflow file came from the cloud lane:** the home lane's token has no `workflow` scope and GitHub refused its push (25 Nov, 21:20), so the cloud lane pushed the file as b7b6b47f, from the text in the PR's first comment. It is byte-identical to the home lane's copy (checked with cmp).
- **Amendment 1 (Project Claude, 25 Nov, 22:20):** the first Gate (check-site 45704002404 on 21b142ec) failed on the clock-seed scan alone: today's UK date reaching the day's seed, which is the feature. The lane stopped, since `scripts/check-site.py` was outside the contract. The amendment allows one entry in `CLOCK_SEED_ALLOW` (`dayCode`), as Equatle and Free Daily Pizza have, and accepts the decisions listed below.
- **Not run:** the workflow itself cannot run before it is on main, so the bot's push to main is unproven until Jon's first row (STOP IF 1 would apply then).
- **Waiting on Jon after merge:** the runbook, from step 1; then his rewrite of the placeholder wording (`docs/todo.md` §6).
- **Gate on the PR head cf859e03:** check-site 45711640580 and phone-fit-full 45711640419, both green.
- **Merged** on 25 Nov as 6db4954 (#919) via merge-pr.py, which ended "main 6db4954 run 45715844895: GREEN". Main on 6db4954: check-site 45715844895, phone-fit-full 45715845154 and the pages build 45715843761, all green.

Record: agent Claude Code; wall 1:25 to the first Gate, which stopped it; review cycles 0; amendments 1; usage n/a.

