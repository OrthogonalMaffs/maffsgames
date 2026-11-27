# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane scope (Jon, 20 Nov 2026):** the cloud lane edits what its contract names. Without a contract naming them, it never edits `schools/assets/`, the shared modules in `scripts/`, the workflow, canon, the roster's listed section or `docs/todo.md`. AGENTS.md's TODO-TRIM rule applies to every cloud PR.

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
`docs/handover/contracts/<yyyy-mm-dd>-<name>.md` in its claim commit (or the PR's first commit), pointed to by a `docs/todo.md`
row, not a Queue line (AGENTS.md). Read it when the item starts, not at session start (the folder stays out of the
start-up load). When the work merges, move the file to `docs/history/contracts/`.

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (25 Nov):** main run 45574813288 on 8840795 (#906) red only in Content verifiers 26: unit-converter t4-003 (?level=level4, 'e': False); failed jobs rerun once, attempt 2 GREEN. **Flake (14 Nov):** main run 43590939932 on 6f37c69 (#760) red only in Answer lock L7: trig-identity-duel, `Page.goto: Timeout 20000ms exceeded` loading the page from the runner's own server (the merge touched no game, shared asset or checker; the job passed on the PR head); failed jobs rerun once, attempt 2 GREEN. **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk's random phone-fit reds (375x667 Aa, 320x568 normal) are fixed by TAKE-A-WALK-SEED** (no seed reads the clock; the Gate's clock-seed scan); its layout is todo row TAKE-A-WALK-PHONE-LAYOUT. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

**Live pointers (kept out of dated entries, Jon 2 Nov; the first four from the 27 Oct entry):**
- **Step 4:** `docs/todo.md` row GATE-STEP-4 (§4).
- **Step 6:** `docs/todo.md` row GATE-STEP-6 (§4).
- **Queue after the freeze:** `docs/todo.md` rows FOLD-COMPONENTS and KEYPAD-FRACTION (§3); measure-phone-fit on `wait_settled` is in GATE-STEP-4 (§4).
- **Old worktrees and their branches:** `docs/todo.md` row BRANCH-CLEANUP (§7).
- **merge-pr.py grace period:** `docs/todo.md` row MERGE-PR-GRACE (§4).
- **check-banks.py escape:** `docs/todo.md` row CHECK-BANKS-ESCAPE (§4).
- **Flake (4 Nov):** main run 41811116888 red only in the timings job (GitHub push: Internal Server Error x3); one rerun GREEN.
- **LOOK-REFRESH-1 palette triage:** `docs/todo.md` row LOOK-REFRESH-PALETTE (§3).
- **ci-deps.py and tools/:** `docs/todo.md` row CI-DEPS-TOOLS (§4).
- **SEARCH-KEYWORDS triage:** `docs/todo.md` row SPEC-MAP-SHORT-BANKS (§3).
- **Search rule in canon:** `docs/todo.md` row CANON-SEARCH-RULE (§7).
- **Room escapes in canon:** `docs/todo.md` row CANON-ROOM-ESCAPED (§7). Jon redeployed the endpoint at 09:02 on 4 Nov; /exec reports `2026-11-04-a`: done.
- **For the rulebook queue (Jon, 3 Nov; no change now):** end-task.py always refuses in cloud sessions, which work in the primary checkout ("is checked out in the primary checkout", after #643); cloud cleanup is nothing to do (the container ends, GitHub deletes the merged branch).

**START HERE (next session; written 19 Oct, 18:10 BST).**
- **Done lists and main-run history to 24 Oct:** moved to `docs/history/handover-cloud-archive.md` (27 Oct, size limit).
- **Waiting on Jon, the list of 20 Oct (fact cards, Monty Hall card, PYTHAG-REPORT, phone header stacking):** in `docs/history/handover-cloud-archive.md`, moved 27 Oct.
- **Container setup (every fresh session):** `pip install playwright==<the version in /opt/node-tools/node_modules/playwright-core/package.json> sympy mpmath pyyaml` (1.63.0, browser revision 1243, on 25 Oct; a pinned 1.56.0 looks for a browser the container does not have and fails every Chromium check); `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1` for what imports it (`bank_common.py` and some verifiers). **No check-changed.py before a push (AGENTS.md, CLOUD-LEAN):** before the first push only the worst-case test where canon §7.8.4 requires it by hand, and the selftest of any script changed; the PR's Gate is the check. Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/history/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

**Merge route:** merge-pr.py only (the 10 Nov ruling was retired by Jon, 16 Nov 2026; canon MERGE-ROUTE). If it cannot reach GitHub, stop and report; the PR waits.

**Standing rule, close-outs (Jon, 10 Nov 2026, 13:13; recorded verbatim, CUMFREQ-CURVE's preamble):**
> STANDING RULE (Jon, Tue 10 Nov 2026, 13:13): cloud close-outs ride on the lane's next task.
> A PR cannot record its own merge, because main's run on the merge commit exists only after the merge, so there is no separate close-out PR. The first commit of each cloud task (straight after the claim commit, where the task claims a listed game) closes out every cloud PR merged since the last close-out: (1) its contract file moves from docs/handover/contracts/ to docs/history/contracts/; (2) its handover entry records the merge commit, the merge route (merge-pr.py, or the standing merge-route ruling with the gh auth output), and main's run IDs on the merge commit with their results. If main's run on any of those merge commits is red, or neither the session nor the contract can confirm it, STOP and report before the task's own work. The task's PR body lists the close-outs it carries. Close-outs left when the lane has no next task go in the home lane's next docs PR. The home lane records this rule in AGENTS.md in its next docs PR.

## 2026-11-27 (cloud): TICKER-LISTED (the front page's score ticker shows only scores from games with a portal card; `docs/handover/contracts/2026-11-27-ticker-listed.md`)

Claude Code (cloud), branch `claude/funny-fermat-12gj5x` from main b5a7a8f. Medium tier (merge on green).
- **Close-out, LEADERBOARD-PAGE:** [#939](https://github.com/OrthogonalMaffs/maffsgames/pull/939) squash-merged as 083faa3 by merge-pr.py, its last line "main 083faa3 run 46072970885: GREEN" (exit 0). Main's runs on 083faa3: check-site 46072970885, phone-fit-full 46072970949, pages 46072970255, each success. Contract file moved to `docs/history/contracts/`.
- **Next:** the ticker change and its check.

## 2026-11-27 (cloud): LEADERBOARD-PAGE (the hub lists exactly the listed scoring games with a computed count; one shared top bar on every non-game site page; true wording on the hub and the privacy page; `docs/handover/contracts/2026-11-27-leaderboard-page.md`)

Claude Code (cloud), branch `claude/fervent-johnson-6mjf5x` from main 314e9ed. Medium tier (merge on green).
- **Close-out, PINNED-LIVE-DATA:** [#936](https://github.com/OrthogonalMaffs/maffsgames/pull/936) squash-merged as 447b22b by merge-pr.py (main merged in twice, for #935 and #937, both clean; one allowed rerun of a Plan timeout on ca88d71); its last line "main 447b22b run 46063470902: GREEN". Main's runs on 447b22b, read from GitHub Actions in this session: check-site 46063470902 success, pages 46063470524 success, phone-fit-full 46063470889 success (each attempt 1). Both contract files moved to `docs/history/contracts/`.
- **The hub (`leaderboards/index.html`, held by `scripts/check-leaderboard-coverage.js`, the hub's existing check, extended rather than a second copy in check-levels.py):** its rows are exactly the roster's listed games that call `submitScore()`, each with exactly the boards it submits (105 rows); `NOT_ON_HUB` is now derived from the roster's Unlisted and Withdrawn sections (10 games: the 9 unlisted and the off-roster the-perfect-prank), never hand-kept. regression-rumble's row is off. The count badge is `GAMES.length` at run time ("105 scoring games"); a typed count fails. Badge "Your score history stays on this device"; both trophy emoji gone. Five plants in the script's own run, each caught: a listed game dropped, a withdrawn game added, an unlisted game added, a typed count, a row whose boards differ. main's hub page fails the new check in four places.
- **STOP IF 1 (a listed game loads firebase-leaderboard.js but never submits):** given-that and constructions-lab. Not added to the hub (they are the check's `EXCLUDED`, "no numeric score", canon §9). The contract's root cause counted them as games with leaderboards; they have none. Also never submitting today, and on the hub since before this task: the three HELD games, estimation-golf, equatle, distinctly-average (their call is gated off; log-laws submits its Laws drill). Left on, as main had them: for Project Claude.
- **The page bar:** one canonical bar, markup in `scripts/check-page-bar.py` (`bar_for()`; SECTIONS gives the parents' guides and "When will I use this?" pages an up link and the Aa button), CSS only in `schools/assets/page-bar.css`, written by `scripts/apply-page-bar.py` (39 pages) and by `scripts/build-uses.py` (its 33 generated pages; it now emits the bar, the stylesheet and the site-nav.js tag). 72 pages carry it; opt-outs: `index.html` (the portal is home) and `scripts/fixtures/` (never published). site-nav.js now loads on the 36 pages that had no a.back-link before (`apply-site-nav.py`). The hand-copied nav.nav and its CSS are gone from 9 files (7 pages, `parents/guide.css`, `ugh-stats/ugh-stats.css`); the foot back links and their CSS on leaderboards and privacy are gone. The check runs from its own `# ci-line` (`--selftest`: the real pages pass, then 8 plants, each caught: bar removed, hand-edited bar, bar CSS in a page, bar CSS in a section stylesheet, a guide given the generic bar, the bar moved below the header, nav.nav put back, the stylesheet link dropped); `# ci-deps: any-page`.
- **Measured, main 314e9ed against this branch, 72 pages at 375x667 and 1280x720 (first content's top):** no page moved more than the bar's 48 px. 108 of 144 page-views moved up 12 px, the rest of the hand-copied-bar pages up 2 to 11 px; the five pages that had no bar (class, leaderboards, op, privacy, spec-map) moved down exactly 48 at both sizes. The bar never overflows and is 48 px everywhere, Aa mode included; no page newly scrolls sideways (spec-map's 375 px sideways scroll is on main too, todo 1.34). site-nav.js's margin logo shows on none of them at 1920x1080: the full-width bar fills the margin it needs, so no clash (it showed on none before either).
- **Decided for you (wording/layout):** the bar is 48 px navy, in the flow, Outfit at its own sizes (a page's Aa mode does not resize it); the section links read "← All parent guides" / "← When will I use this?", "← Guides" / "← Topics" below 480 px, and beside them "← Back to Games" reads "← Games" below 400 px; the bar replaces about's and feedback's relative "../" links with "/"; the class page (Year 6 look) gets the adult bar, as the contract lists it; spec-map's own two "← Back to Games" links (header and content) were left, the contract naming only leaderboards' and privacy's; the leaderboard hub's bar sits on its navy header.
- **STOP IF 2 (privacy wording parked, nothing changed on /privacy/ but the bar):** three games store a name a student types, up to 20 characters, in localStorage for a device-only list: equatle (`games/equatle/index.html:920`, its local "leaderboard"), 52-dle (`games/52dle/index.html:1635`, "Your name for today's list"), prime-or-composite (`games/prime-or-composite/index.html:539`). None is sent anywhere (no mfg or Firebase call carries it). A name can be personal data, so the page cannot say "none of it personal data" as the contract words it. Question for Jon: reword to name these lists (stored only on the device, never sent), or remove the name boxes first?
- **For the home lane:** canon SR-21 says relisting takes a hub row "out of `NOT_ON_HUB`"; that step is now automatic (the roster row's move does it), and the roster's Unlisted preamble still names `NOT_ON_HUB`, which still exists, derived. A `docs/todo.md` row for the privacy question (the cloud lane does not edit todo.md without a contract naming it).
- **Next:** the Gate; merge on green.

