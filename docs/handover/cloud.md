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

## 2026-11-19 (cloud): FRACTION-SNAP-START (`docs/history/contracts/2026-11-19-fraction-snap-start.md`; Jon 19 Nov)

Agent Claude Code (cloud), branch `claude/youthful-knuth-uprtv0` restarted from main 1f88f36. Tier Small. Lines 156-159 and the verifier's :368-370 and :415-416 matched the contract.
**Close-outs carried (first commit, 25bd040):** #834 FORMULA-FORGE-40, recorded in its entry below.
Done on the branch: the how-to's lines 157-159 are the contract's three, each with its TeX in `data-mt` and a plain fallback, rendered by `MaffsText.html` at DOMContentLoaded (KaTeX is deferred, so it has run by then); line 156 unchanged. Verifier: the rule check is now the KaTeX line (`\dfrac{a}{b}`, `\dfrac{c}{d}`, `ad = bc`); new checks: no `4/9` or `4}{9}` in the how-to, and in Chromium every how-to line's maths is KaTeX with no plain n/d (or ½-style) text left. New plants, both caught: the old "½ and 4/9 are not equivalent" line restored; the how-to left unrendered. PASS, all 10 plants caught.
**Phone fit (local, main against the branch, same fonts; the footer pre-check skipped in a scratch copy, as it fails locally by 1 px):** the judged rows are identical (normal PASS; Aa WARN at 320, 618/528). Start screen, Start button bottom / fold: normal 418/400/400 on main, 499/463/463 here, all three fit on both; Aa 754/677/599 on main, 823/719/668 here, 320 and 375 below the fold on both, 390 fits on both. No size flips; the screen is 63-81 px taller.
**Report only, plain-text fractions on other games' start screens** (Chromium text at load, plus a static pass over how-to/help/start containers): `possibly-maybe:181` "2/4 counts the same as 1/2"; `shape-shifter:205` "a scale factor of 2, 3 or 1/2". (Score counters such as 0/10 and "2026/27" excluded; `how-many-parts:264`'s 3/4 is a KaTeX fallback and renders.)
**Decided for you:** (1) The \dfrac lines make the start screen taller (above); no fit is lost, so no CSS was added to win it back; Jon may want `\tfrac` or tighter spacing. (2) At 320 px "0.5" wraps onto its own line. (3) The fallback text keeps the contract's wording with a/b-style fractions, so the page still reads if KaTeX never loads. (4) A third plant (the how-to never rendered) proves the Chromium check. (5) An /updates/ line, which the contract did not list but AGENTS.md requires for a change students see.
PR #835. **Merged (closed out by FACTOR-RACE-Y6-40):** merge commit 8bfe33e (14:54:49 UTC 19 Nov), route merge-pr.py `--watch --wait 3600`, exit 0, last line "main 8bfe33e run 44548908435: GREEN"; main's runs on it, read from the API: check-site 44548908435 success, phone-fit-full 44548908467 success, pages build 44548907797 success, all attempt 1. Jon (19 Nov): leave the taller start screen as it is. Contract moved to `docs/history/contracts/`.
Record: agent Claude Code; wall about 0:22 (first commit 14:32, merged 14:55 UTC); review cycles 0; amendments 0; usage n/a.

## 2026-11-19 (cloud): FORMULA-FORGE-40 (`docs/history/contracts/2026-11-19-formula-forge-40.md`; Jon 19 Nov)

Agent Claude Code (cloud), branch `claude/youthful-knuth-uprtv0` from main 346ac4d. Tier Small. Every stage array was where the contract said (s1 closing `],` at :238, s2 :274, s3 :306, s4 :332 on main).
**Close-outs carried (first commit, f9eaf4a):** #833 FRACTION-SNAP-REBUILD, recorded in its entry below, with the check-site attempt-1 flake.
Done on the branch: the 11 items appended verbatim to the end of Q.gcse's four stages (s1 10, s2 10, s3 10, s4 10; Q.level4 4/5/4/3 unchanged; A-Level copies Q.gcse, so 40 too). `verify-formula-forge.py` PASS unchanged (56 items, 203 worked lines). `check-banks.py --ci` (CI's form) failed after extraction on 2 STALE entries, `formula-forge::gcse` and `::alevel` (the fix itself); cleared with `check-banks.py --write-ledger --only formula-forge` (`data/check-ledger.json`, those two entries only; level4 kept), then `--ci` OK. todo row LEDGER-B4-FORMULA-FORGE now names level4 only (150,465 to 150,456 bytes); /updates/ line.
**Decided for you:** (1) the ledger edit above: the contract named only the two scripts as unchanged, and `--ci` cannot pass with the entries left, so the data file was regenerated as FRACTION-SNAP-REBUILD did. (2) The todo row's "Recorded 9 Nov 2026 (DOCS-BUNDLE)" was dropped so todo.md does not grow.
PR #834. **Merged (closed out by FRACTION-SNAP-START):** merge commit d10f9d7 (14:13:57 UTC 19 Nov), route merge-pr.py `--watch --wait 3600`, exit 0, last line "main d10f9d7 run 44541510720: GREEN"; main's runs on it, read from the API: check-site 44541510720 success, phone-fit-full 44541510713 success, pages build 44541509556 success, all attempt 1. Contract moved to `docs/history/contracts/`.
Record: agent Claude Code; wall about 0:19 (first commit 13:55, merged 14:14 UTC); review cycles 0; amendments 0; usage n/a.

## 2026-11-19 (cloud): FRACTION-SNAP-REBUILD (`docs/history/contracts/2026-11-19-fraction-snap-rebuild.md`; Jon 19 Nov)

Agent Claude Code (cloud), branch `claude/zealous-dijkstra-12fjsn` restarted from main 4df5235. Tier Medium. Every line reference matched main. Claim commit f99bd58 (`fraction-equivalence` in `scripts/answer-lock-state.json`), taken off in the PR.
**Close-outs carried (first commit after the claim):** #832 TODO-135-CLOSE, recorded in its entry below.
Done on the branch: YEAR6_BANK is the contract's 46 pairs with `kind`; KS3 and GCSE are two generators (half YES, the NOs split between add, one and near); gameLevel is MaffsLevel.resolve's year6, ks3 or gcse with no 'all' board; the hub lists the three; the best is `fs_best_<level>`; both fractions are KaTeX `\dfrac` at 35.1 px (the CSS digits' size at 390 px), the working through MaffsText. `verify-fraction-equivalence.py` rewritten on plant_common: 20000 draws a level, every rule of item 3, each parameter's range reached; 8 plants, all caught; 77 s locally. Ledger: the three B4 entries cleared (`check-banks.py --write-ledger --only fraction-equivalence`). Docs: LEDGER-B4-FRACTION-EQUIVALENCE and 1.48 to todo-done; 1.14 rewritten; BEST-KEY-PER-LEVEL added (§4); todo.md 151,168 to 150,465 bytes; /updates/ line; findings v20-001 and t1-001 fixed.
**Phone fit (local, this game, main against the branch, same fonts):** branch 18-20 px shorter at every size; laptop PASS; Aa at 320x568 WARN on both (Next 638 on main, 618 here). No regression.
**Decided for you:** t1-001 ("The Year 6 bank has only 20 items") closed with v20-001, since the bank now holds 46. Old `fs_best` scores are not carried over (the contract: no longer read), so every player's best starts at 0 per level. The NO-kind label is kept on generated draws, the key computed from the cross-products, never from the kind. The near-pair check accepts KS3 bottoms 2-23 except 22 (22 and 24 cannot occur: 11 or 12 would have to divide 1).
**Reported, not fixed:** (1) the CLASS CHECK's eight: `quadratic-factoriser` already keeps `qf_best_<level>` and `modular-battle` has one level, so six are affected (BEST-KEY-PER-LEVEL). (2) The start screen's how-to still writes ½, 4/8 and 4/9 as text, and "½ and 4/9" is the old +1 rule's example. (3) extract-banks counts the Year 6 bank for ks3 and gcse too (it cannot see the generators). (4) `scripts/survey-key-collisions.py` (not in CI) enumerates this game's old generateQ; not run. (5) Locally, check-start-mount fails 11 other games and the footer check fails by 1 px (container fonts); CI is the authority.
**Merged (closed out by FORMULA-FORGE-40):** #833, merge commit 01c4c3a (13:15:53 UTC 19 Nov), route merge-pr.py (its last line is not in this session); main's runs on it, read from the API: check-site 44531744271 success on attempt 2, phone-fit-full 44531743898 success, pages build 44531742013 success. **Flake:** check-site attempt 1 red only in Content verifiers 68, whose checks passed: the timing artifact's upload failed (`Failed to FinalizeArtifact: Unable to make request: ECONNRESET`); failed jobs rerun once, attempt 2 GREEN. Contract moved to `docs/history/contracts/`.

## 2026-11-19 (cloud): TODO-135-CLOSE (`docs/history/contracts/2026-11-19-todo-135-close.md`; Jon 19 Nov)

Agent Claude Code (cloud), branch `claude/zealous-dijkstra-12fjsn` from main 91d9f0f. Tier Small, docs only. Every line reference in the contract matched main.
**Close-outs carried (first commit):** #831 DASHBOARD-PERCENT-CELLS, recorded in its entry below; cloud.md's STOP IF pointer now names `docs/history/contracts/`.
Done on the branch: row 1.35 moved word for word to todo-done ("Closed by fix PRs") with its done note; LEDGER-B4-FRACTION-EQUIVALENCE rewritten to the generator's real state, owner Project Claude (spec), then cloud lane. todo.md 152,731 to 151,168 bytes.
**Scan (§1, headline live or open, body FIXED or DONE for every part): none.** Of §1's 9 rows, those that say FIXED or DONE (1.14, 1.26, 1.34, 1.36, 1.48) each still name an open part; 1.14 and 1.48 are the reverse case (headline FIXED, a part still open). Changed none.
**Decided for you:** the LEDGER row keeps a bold label without the old counts, and its survey pointer and 9 Nov provenance after the new text.
**Merged (closed out by FRACTION-SNAP-REBUILD):** #832, merge commit 20b30ed, route merge-pr.py, last line "main 20b30ed run 44523951280: GREEN"; main's runs on it, read from the API: check-site 44523951280 success, phone-fit-full 44523951287 success, pages build 44523949894 success. Contract moved to `docs/history/contracts/`.

