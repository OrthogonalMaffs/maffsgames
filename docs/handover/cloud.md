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

**Queue** (finished contracts moved to `docs/history/handover-cloud-archive.md`, 19 Oct 2026; on 8 Nov, BRANCH-CLEANUP, every DONE item with an entry below or a history file was taken out and unfinished work became `docs/todo.md` rows, listed in that PR): **Flake (14 Nov):** main run 43590939932 on 6f37c69 (#760) red only in Answer lock L7: trig-identity-duel, `Page.goto: Timeout 20000ms exceeded` loading the page from the runner's own server (the merge touched no game, shared asset or checker; the job passed on the PR head); failed jobs rerun once, attempt 2 GREEN. **Flake (5 Nov):** main run 42049027958 on e32608f (#668) red only in Content verifiers 53: the Playwright image pull from mcr.microsoft.com timed out three times, no test ran; failed jobs rerun once (attempt 2). **take-a-walk's random phone-fit reds (375x667 Aa, 320x568 normal) are fixed by TAKE-A-WALK-SEED** (no seed reads the clock; the Gate's clock-seed scan); its layout is todo row TAKE-A-WALK-PHONE-LAYOUT. **Parked (Jon, 3 Nov, Amendment 1 above): every older item in this queue; start none of them.** **Unfinished work, as `docs/todo.md` rows:** WHOSE-SIDE-LISTING (the subtitle, Jon 6 Nov), FOLD-COMPONENTS, KEYPAD-FRACTION, HOW-MANY-PARTS-FRACTION (the FRACTION-STACK follow-up), SIX-PS-LOOK-REDS, PRIME-SPRINT-LOOK-REDS, ESTIMATION-GOLF-ART, HIGHER-POWER-PHONE, SCREENING-ROOM-PANELS and ANSWER-CONTROL-TALL-INPUT (§3); GATE-STEP-4, GATE-STEP-6, PHONE-FIT-DRIVER-RULINGS, SIX-PS-PHONE-FIT, MODE-DIMENSION and START-SCREEN-RULE (§4); BURST-CLEANUP (§7). **burst.js (Jon, 25 Oct):** Do NOT remove `burst.js` or its hooks (a cleanup contract after launch). **Standing rulings from SWEEP-1 (Jon, 13 Oct; the block moved to the archive 4 Nov, copied here unchanged):** **SR-32 (recorded in canon §0.3, 9 Nov) (Jon, 13 Oct; the home lane records it in canon): a CRITICAL level whose fix a standing ruling decides is fixed the same day in its own PR, no unlist, reported to Jon after; stop and ask only for a new stem, context or convention, or if it cannot merge the same day.** **From now on (Jon, 13 Oct):** a verifier that does not check worked steps or hints is a finding; report every typed answer that can be negative behind inputmode="decimal" (so far: log-laws, suvat; listed in the report's batch 6). **Jon, 13 Oct, from now:** an 'Estimate' stem states a method (SR-12) or says 'use the model to estimate' (brief checks g, h).

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

## 2026-11-23 (cloud): B4-SERVED-AUDIT (`docs/handover/contracts/2026-11-23-b4-served-audit.md`)

Claude Code (cloud), branch `claude/beautiful-bardeen-gb5zga` from main 9d779ec (after 65ae674). Tier Medium: merges on green with merge-pr.py. First commit: #892's close-out (entry below), this contract saved.

- **Next:** scripts/audit-served.py, its three self-tests, the full run, docs/audits/served-2026-11.{md,json}.

## 2026-11-23 (cloud): KATEX-ERRORS (`docs/history/contracts/2026-11-23-katex-errors.md`)

Claude Code (cloud), branch `claude/cool-franklin-htrt70` from main dbd2395. Tier Shared: stops at Gate green for Project Claude's review and Jon's "merge". First commit: #890's close-out (entry below), this contract saved.

- **Done on the branch:** one parse function, `bank_common.KATEX_PARSE_JS` (the string again, the page's own options, throwOnError:true; a ParseError is the finding), used by MATHTEXT_THROW_JS, extract-banks.py's SITE_RENDER_JS (B12) and `KATEX_HOOK_INIT` (tier 3's trap). B12 in check-banks.py: 0 findings over 13,500 strings at 278 sites in 52 games. Tier 3 fails a game that hands KaTeX a string it cannot parse (known list: checker-allowlist.json `tier3_katex_known`, empty), with `--tier3-katex-selftest`. `scripts/katex_page_common.py` holds the page rule; check-uses.py imports it (self-test 98 of 98, --check OK, as on main); `scripts/check-katex-pages.py` runs it over 22 pages (20 parent guides, the portal, the-6-ps): 0 faults. CI: B12 self-tests in Tier 4, the page check in Site-wide, tier 3 as four new shard jobs. One /updates/ line.
- **Decided for you:** (1) tier 3 was in no CI job, so the contract's "run in CI" and its timing STOP IF had nothing to compare against: tier 3 joined CI in four shards, failing on every tier 3 FAIL, as tier 3 always has (main had 0 FAIL in 352 runs). (2) Canon 7.8.4 forbids random sampling in a gate, so tier 3 now seeds Math.random with tier 1's PHONE_SEED (`--tier3-random` for local sweeps). (3) B12's first run found 77 "failures", all sequence-solver options authored with \( \): the game sends those to MaffsText, never `rk` (:369), but the site evaluator could not decide `MaffsText.hasMaths` and counted both branches. A checker bug, not a game bug: the evaluator now decides it, with a self-test fixture that fails without the fix. No game needed a LaTeX fix. (4) `has_maths` ignores script code (the-6-ps's `\(` is code), so the page check does not false-fail it; check-uses.py's pages read exactly as before.
- **PR #892.** #891 merged first: main merged into the branch, both /updates/ lines kept. Gate green on 152a6d6 (check-site 45230974807, phone-fit-full 45230974749, both success). CI tier 3 (seeded): 49 PASS, 0 FAIL, 303 UNSUPPORTED of 352 runs, 556 questions, 0 KaTeX failures; shards 4m17s to 7m53s against a 12-minute limit. Local seeded runs: 49/0/303 with 558 and 556 questions (22m34s, 22m30s); main unseeded 22m05s.
- **Merged (closed out by B4-SERVED-AUDIT's first commit):** #892 merged as 65ae674, route merge-pr.py, on Jon's "merge". Main's runs on 65ae674: check-site 45245221265 success, phone-fit-full 45245221320 success, pages 45245220384 success. Contract moved to `docs/history/contracts/2026-11-23-katex-errors.md`.

## 2026-11-23 (cloud): WWIUT-CARD-FORMAT (`docs/history/contracts/2026-11-23-wwiut-card-format.md`)

Claude Code (cloud), branch `claude/relaxed-albattani-2zeun8` from main 5adf87a. Lane exception (Jon): build-uses.py and check-uses.py. First commit: #888's close-out (entry below), SITE-CONTRAST's two phrases corrected, this contract saved.

- **Done on the branch:** data/uses.json: formula (39, health-visitor null), question, inside, formulaNote (9) on every scenario, verbatim from the contract, inserted by text so no existing line changed; _comment describes them. build-uses.py: a hub card shows the formula (display style), note, question and "Inside: ...", never the worked sum; a job section shows formula, note and question after its chips, then the wording and steps, then "The answer:" with the headline sum. check-uses.py: the four fields checked (null count reported), any .katex-error fails naming page, source and KaTeX's message; self-test 98 of 98 (4 new plants). --check: 32 pages x 320x568 and 390x844 x normal and Aa, no sideways scroll, no .katex-error. Build idempotent; only when-will-i-use-this/ changed. Screenshots in docs/screens/wwiut-card-format/. One /updates/ line.
- **Decided for you:** (1) the formula's class is `job-formula`, not `formula`: parents/guide.css:292 already styles `.formula` as a padded box with `overflow-x: auto`, which would have scrolled an overlong formula inside its box where the page check cannot see it. (2) Formula size 1.3rem (KaTeX glyphs about 25 px, body 16 px): at 1.45rem three desktop cards wrapped mid-formula; at 1.3rem none wraps at 390, one at 1366 (payroll-administrator), three at 320 (hospital-nurse, payroll-administrator, bookkeeper), each breaking after = or ×, none past its card's edge (measured, every page, every size, both modes). Lowest contrast of the new text 4.76:1. (3) The contract's plant "\dfrac{1}{" never reaches KaTeX: auto-render matches braces looking for the closing delimiter, so it stays as raw source, caught by the existing unrendered-source rule. Both are planted: "\dfrac{1}" (balanced, a missing argument) for .katex-error, and "\dfrac{1}{" for the raw-source rule.
- **Discoveries (step 6, report only):** KaTeX with throwOnError:false in 90 files outside this section, 126 occurrences: the 20 parent guides through auto-render (one each); 68 games, schools/assets/mathtext.js (2) and scripts/audit-katex/rerender.js through katex.render. Seven game verifiers already check .katex-error (graph-transformer, circle-theorem-spotter, complex-converter, percentage-flip, its-a-sine, standard-form-blitz, surd-simplifier); the parent guides and the other games have none found. The list is in the PR body.
- MERGED 23 Nov as 936188a (#890) via merge-pr.py. Main on the merge commit: check-site 45158418307, phone-fit-full 45158418369, pages build 45158417639, all success, attempt 1; PR head 7d9e8b0: check-site 45156559796, phone-fit-full 45156559603. Contract moved to `docs/history/contracts/2026-11-23-wwiut-card-format.md` (closed out by KATEX-ERRORS's first commit).

