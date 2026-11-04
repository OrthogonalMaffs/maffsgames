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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026): **IN PROGRESS: LOOK-REFRESH-1** (Small per game, `docs/handover/contracts/2026-11-04-look-refresh-1.md`: prime-factorisation, percentage-flip, fraction-equivalence, one PR each, then the NOT_YET contact sheet). **PACK-GENERATOR: DONE** (#659, 713a178, main run 41859685493 GREEN; `docs/history/contracts/2026-11-04-pack-generator.md`). **DONE items** (moved 4 Nov, verbatim, to `docs/history/handover-cloud-archive.md`, entries "Queue DONE items moved 4 Nov" and "... second batch": SWEEP-1, SWEEP-1-RULINGS, ESSENTIALS-SCREEN-TRUTH-2). Live tails inside them: Prime Sprint (LOOK-REDS) waits for Jon's next contract; PHONE-FIT-DRIVER's two rulings (the 11-game exception, a start-screen rule) are Jon's. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **FRACTION-STACK follow-up:** give MaffsFractionInput an optional whole-number box for mixed numbers, then move the-6-ps and how-many-parts (`scripts/fraction-input-warn.json`) onto it. **Estimation Golf art parked: the game has no start screen; placement to be decided** (Jon, 2 Nov; branch `art/estimation-golf`, 028cf683, the PNG unchanged, no PR). **GATE-WARN-THEN-ENFORCE** (27 Oct): steps 1-3, 5 DONE (#590, #630, #592, #631); steps 4, 6 and the post-freeze queue: live pointers below. **Session queue (Jon, 27 Oct afternoon):** 1 SHARD; 2 FOLD PR 3-6 (PR 6 stops before merge: Project Claude's live 404 check); then, after the home lane's 6 P's launch PR merges (do not edit games.json, the homepage, /essentials/ or /updates/ before it), **KEYPAD-FRACTION** (Jon: review `claude/keypad-fraction-key` 799dbfd9, the / key on the shared keypad; every keypad game through the phone-fit gate; PR, merge on green; then tell the build lane to set `FRACTIONS = true` in `games/y-so-steep/` (Stage 3); if any existing game changes behaviour, leave it unmerged and report); 3 The 6 P's in the phone-fit gate (driver change); 4 Higher Power's card values spilling on phones; 5 Screening Room panels + the hardened top-scores check (item E); 6 the mode dimension (item D); 7 the answer-control (8) and tall-input (6) games; 8 the start-screen rule only once a shared compact start screen exists, else write up what it needs and stop. Items D and E: no contract text found in the repo; ask Jon. **FOLD-COMPONENTS** (27 Oct, `docs/handover/contracts/2026-10-27-fold-components.md`; **lane exception, this contract only (Jon, 27 Oct):** theme.css, canon §7.5/§7.6.1, `_config.yml`, the shared scripts, and per-game edits to listed games in the three groups, each claimed first; canon outside those sections stops and asks; `site-footer.css` and `the-6-ps/` are not ours): IN PROGRESS, entry below. **THE-6-PS v2** (Jon's ruling, 25 Oct, via Project Claude): The 6 P's is rebuilt self-contained (its own banks, one stylesheet, no hand-off into games; spec `claude/six-ps-v2-spec-2026-10-25.md` in the project). **Waiting for its build contracts.** STOPPED: all burst work for The 6 P's and contract SIX-PS-SOON. Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). Kept: PR-MEASURED (CI); LOOK-REDS second, after this build (home lane, see home.md). v1 (#531, `docs/history/contracts/2026-10-24-the-6-ps.md`) is what is live at /the-6-ps/, unlisted, until v2 replaces it. **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-30 (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

**Live pointers (kept out of dated entries, Jon 2 Nov; the first four from the 27 Oct entry):**
- **Step 4 from Mon 2 Nov: spec `docs/handover/contracts/2026-10-27-gate-step4-spec.md`** (Jon's ruling verbatim, the approved approach: stub-server default seed, per-verifier seed lists, a nightly non-gating random sweep that adds failing seeds, Take a Walk's `Date.now` seed, `bc.wait_settled` after #583; the audit list of ~45 sites).
- **Step 6:** nothing to clear (the warn list is empty); migrating Factor Theorem (88 s), Growth and Decay (123 s) and Screening Room (94 s) to work units is insurance against the setup median rising again (they passed the limit at 107 s); Jon to say.
- **Queue after the freeze (each needs main merged in):** FOLD PR 3 `claude/fold-options-v2` (`/home/user/wt-fo`, 44a4ef8) -> PR 4 `claude/fold-figures-v2` (`/home/user/wt-lf`, 227c3d6) -> PR 5 `claude/fold-canon` (`/home/user/wt-fc`, 4a526a6) -> PR 6 `claude/fold-publish` (`/home/user/wt-fp`, ed00d80; NOT merged: Project Claude's live 404 check). KEYPAD-FRACTION `claude/keypad-fraction` (`/home/user/wt-kp`, fbf6c36: 799dbfd9 cherry-picked + 4 plants; phone-fit on the 19 keypad games identical to main in all three modes; check-changed: no new failure). Then measure-phone-fit on `wait_settled` (after #583), queue item 6. FOLD-COMPONENTS' and SHARD's entries are in the archive (moved 27 Oct).
- **Worktrees to clear by end-task.py once their PRs merge:** wt-sh (#578), wt-jsn (#588), wt-mp (#582); scratch: wt-kpm, wt-seed, wt-ref, wt-main-da.
- (2 Nov: each branch above is on origin at its commit; the `wt-*` worktrees went with an earlier container.)
- **Queued, Low (Jon, 2 Nov, after GATE-FIX):** merge-pr.py counts "the newest merge has no run of its own" as red even under `--wait`, so in the seconds before GitHub registers a new merge's run it refuses ("start one by hand") instead of waiting. Fix: count it as unfinished for a short grace period (about 5 minutes after the commit), with a plant.
- **Home-lane queue (Jon, 2 Nov):** `scripts/check-banks.py:25` has an invalid escape `\(` (ci-deps.py's `ast.parse` warns on Python 3.12+). Harmless.
- **Flake (4 Nov):** main run 41811116888 red only in the timings job (GitHub push: Internal Server Error x3); one rerun GREEN.
- **For Project Claude to triage (PACK-GENERATOR, Amendment 2):** `tools` is not in `scripts/ci-deps.py` KNOWN_TOP, so a tools/ change selects every verifier.
- **For Project Claude to triage (SEARCH-KEYWORDS ruling 6):** spec-map rows banks do not teach, possibly short banks: archive entry "SEARCH-KEYWORDS triage lists".
- **For the home lane, canon §7 (SEARCH-KEYWORDS, 4 Nov):** one search rule, `MaffsSearch.match` (`schools/assets/search.js`: text plus `data-keywords`, every word, trailing s), called by the portal and card-filter.js; keywords in games.json via apply-meta.py, held by check-meta.py.
- **For the home lane (ROOM-ESCAPED, 4 Nov):** canon §1.4 item 5 says rooms "escaped (`game_completed`)"; from endpoint `2026-11-04-a` an escape is a `game_completed` with `questions_correct` = `questions_answered` > 0, any other is "timed out" (its own column). Jon redeployed the endpoint at 09:02 on 4 Nov; /exec reports `2026-11-04-a`: done.
- **For the rulebook queue (Jon, 3 Nov; no change now):** end-task.py always refuses in cloud sessions, which work in the primary checkout ("is checked out in the primary checkout", after #643); cloud cleanup is nothing to do (the container ends, GitHub deletes the merged branch).

**START HERE (next session; written 19 Oct, 18:10 BST).**
- **Done lists and main-run history to 24 Oct:** moved to `docs/history/handover-cloud-archive.md` (27 Oct, size limit).
- **Waiting on Jon, the list of 20 Oct (fact cards, Monty Hall card, PYTHAG-REPORT, phone header stacking):** in `docs/history/handover-cloud-archive.md`, moved 27 Oct.
- **Container setup (every fresh session):** `pip install playwright==<the version in /opt/node-tools/node_modules/playwright-core/package.json> sympy mpmath pyyaml` (1.63.0, browser revision 1243, on 25 Oct; a pinned 1.56.0 looks for a browser the container does not have and fails every Chromium check); `pip download --no-deps esprima==4.0.1`, untar into the scratchpad, `PYTHONPATH=<that>/esprima-4.0.1` for what imports it (`bank_common.py` and some verifiers). **No check-changed.py before a push (AGENTS.md, CLOUD-LEAN):** before the first push only the worst-case test where canon §7.8.4 requires it by hand, and the selftest of any script changed; the PR's Gate is the check. Remote branches are deleted on merge: after a squash merge, `git checkout -B claude/brave-allen-reghhq origin/main` and push without `--force-with-lease`.

**Standing authorisation (Jon, 10 Oct):** the cloud lane merges any PR of its own once its Gate is green and main's last full run is green, without asking each time; it still watches main's run after each merge. The 10 Oct queue (RIGHTFUL-KING, LIBRARY-JAM, FONT-FIT) is DONE and moved to `docs/history/handover-cloud-archive.md`, with Jon's rulings for the two room builds and FONT-FIT's known problems.
**Holds and self-scheduled tasks (Jon, 16 Oct 2026):** a hold the cloud lane states on a PR is released only by Jon. Stating a hold cancels, or rewrites to report-only, any pending task this lane scheduled for that PR. A task this lane schedules for itself carries no authority beyond the standing rules at the time it fires, and its report names it as the lane's own follow-up, not a request. Self-scheduled tasks may read CI status and report; they never merge, push or edit while a hold stands. (Contract GS-L4-5-ENDPOINT; canon §7.8 records it via the home lane.)

**STOP IF defaults (Jon, 27 Oct, every contract):** `docs/handover/contracts/2026-10-27-standing-stop-rules.md`; report each under "Decided for you".
**Every PR:** no `check-changed.py` in the cloud (AGENTS.md, CLOUD-LEAN); merge only via `python scripts/merge-pr.py <n>
--watch --wait 3600` (needs a green Gate and main, §7.8.3) and report its last line.

## 2026-11-04 (cloud): PACK-GENERATOR (`docs/history/contracts/2026-11-04-pack-generator.md`, Shared, Amendments 1-11; stops at a green Gate for Project Claude's review and Jon's "merge")

- Agent: Claude Code; primary checkout, branch `claude/great-feynman-vs4fpp`. Pre-step a9e175f; generator 562c5a2; PR #659.
- Built: `tools/pack-generator/` (build_pack.py, lockcheck.py, README, Kiln config and 11 webp, two fonts); `dist-packs/` gitignored. Kiln: 320/700 VALID draws, 7 sets, 70 values (21 answers) recomputed independently, labels at least 11.5 pt, 35 pages. Amendment 3: per-lock checking, landscape score sheet (page 2). Final padlock: one x and one + or - in every set, calculator allowed (Amendments 5, 7). Penalties left blank for the teacher (6). Answer boxes give nothing away (4). Page 1 "Run it" (150 words) and read-outs; stakes only as the timeout read-out (8, 9). Final padlock: students told only + - x /, no calculator; friendly products (11). Selftest 17/17.
- **Jon builds and proofreads the PDF at home:** `python -X utf8 tools/pack-generator/build_pack.py kiln-disaster` (README: what to proofread). Run it and read-outs are DRAFT for his wording.
- Amendment 2 accepted `scripts/test-pack-generator.py`, `_config.yml` `- tools`, two evidence pages and the fonts.
- **State:** DONE. Gate green on acdf9fb (run 41850766841); merged #659 (713a178); main run 41859685493 GREEN (checked 4 Nov via the Actions API).

Record: agent Claude Code; wall n/a; review cycles 0; amendments 11; usage n/a.

## 2026-11-04 (cloud): PACKS-CANON (`docs/handover/contracts/2026-11-04-packs-canon.md`, Small, lane exception: canon §7.1, §8, §12)

- Agent: Claude Code; branch `claude/sleepy-shannon-itnz0v` (claim 86a2667). Pre-step 953a0ca. Done: §7.1 line replaced verbatim; §8.2 backlog line; §12 reason.
- Occurrences, reported not edited: AGENTS.md:16 and .claude/rules/project-claude.md:72 "Free forever. No subscription, no freemium, no ads."; index.html:760 "Free forever"; about/index.html:161 "Free forever &mdash; no subscriptions, no freemium, no ads"; about/index.html:193 "will always be free"; parents/index.html:204 "free to use". None in CLAUDE.md, privacy or canon §0.
- **STOP IF 1 resolved (Amendment 1, Jon):** §7.1 keeps "no freemium" (nothing on the site held back for payers); about, AGENTS.md, project-claude.md unchanged and now agree.
- **State:** DONE. Merged #658 (c693a17) on Amendment 1; merge-pr.py's watch: `main c693a17 run 41816602804: GREEN`.

Record: agent Claude Code; wall n/a; review cycles 0; amendments 1; usage n/a.
