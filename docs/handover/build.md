# Build lane handover

Lane rules: new, fully specified games only; new files only; games stay unlisted; branches `claude/build-<slug>`; worktrees `E:/jon/mg-build-<slug>`.
Contracts are saved verbatim in `docs/handover/contracts/<date>-build-<slug>.md`.

## Standing rules (Jon, 27 Oct 2026; apply to every contract unless it says otherwise)
1. **Never sit idle.** Several contracts: save each verbatim to `docs/handover/contracts/<date>-build-<slug>.md`, work in order. A real STOP IF parks the contract: commit and push the branch, record the stop here with the exact question for Jon, start the next. While CI runs on one job, start the next in its own worktree. Main red from another lane: keep building, only the merge waits.
2. **Decide the small things and say so** (wording and copy: plain, adult, listed for Jon; layout inside theme.css and shared components; names and structure; example numbers; counts above the minimum), each as one line under "Decided for you" in the report. Real stops: a mathematically wrong answer that can't be resolved; a shared-file change; a design question with no reasonable default; any new data collection.
3. **Worktree `E:/jon/mg-build-<slug>`** (cloud: any worktree), never the main checkout.
4. **Context loss:** commit and push at each milestone; keep this file current enough for a fresh session. At about 60% context, checkpoint and say so.
5. **One short report per job:** what merged (PR, commit, main run); "Decided for you"; screenshots; anything parked with its question. End with "Ready for /clear".
6. Queue finished: write "Build queue empty" here and stop. Start nothing uncontracted.
7. **Subagents for large reads** (CI logs, full measurement runs, long files): only conclusions enter the main context.
8. **Done marker:** when a contract's job is merged (or parked with its question recorded), add a line `DONE: <contract file name>` under "Done" below; `E:/jon/tools/run-build-queue.ps1` skips contracts with such a line.

## Done
DONE: 2026-10-27-build-found-a-mark.md   (merged: PR #569, squash 6c5cc59, 27 Oct 2026; held up by CI timing blocks, fixed by #570, then one real 320 x 568 fault on CI's real fonts, fixed)

DONE: 2026-10-27-build-hc-factor.md   (merged: PR #571, squash f6eecad; main run 40510992524 green)
DONE: 2026-10-27-build-y-so-steep.md   (merged: PR #574, squash f8083cc, 27 Oct 2026; main run 40518636405 green)

## Queue
1. **found-a-mark**: MERGED (#569) + art swap MERGED (#573, aaef265, main run 40514401072 green). Report still owed to Jon: its "Decided for you" list and screenshots.
2. **hc-factor**: MERGED (#571).
3. **y-so-steep**: MERGED (#574). Unmerged side branch: the "/" key for MaffsKeypad on `claude/keypad-fraction-key` (799dbfd9, worktree `E:/jon/mg-keypad-slash`), NOT a PR. Home lane/Jon to rule on merging it; then set `FRACTIONS = true` in `games/y-so-steep/index.html` to bring in Stage 3 and the fractional items.
Build queue empty (27 Oct 2026, after #574). Nothing uncontracted is started.

## Standing notes (Jon, 27 Oct 2026)
- Roster numbers stay as they are (#102 found-a-mark, #103 hc-factor; next is #104). "The 100th" is the count of LISTED items on the portal, not a roster number. NEVER list anything: listing is the home lane's job and The 6 P's goes first.
- Roster rows for unlisted games go in the Unlisted section, numbered above #101.

## hc-factor: state (27 Oct 2026)
Design: `schools/assets/hc-factor-gen.js` (`MaffsHCFactor`: bank(stage) 40 a stage, session(stage, seed), mark(step, vals)); polynomial [c2,c1,c0]; box answers marked by value; Stage 3 `canon` vector gives the 'format' (not fully factorised) verdict; sign grid is its own step (marks: S1-S5 one a question, S6 two).
Verifier `scripts/verify-hc-factor.py` parses the printed stem with its own polynomial parser; part 2 plays all six stages at 375, 360, 320, 1280, 1366.
Lessons that cost a round each (new-game checklist): the Theme check bans hex colours outside :root (use tokens); Search titles needs the page meta description = data/games.json text; the lock check finds Next by its text ("See results →", not "See the result →"); check-start-mount needs a START_STEPS entry when the menu has no Start button; CI has real fonts so options wrap more than locally: test short phones with a wide font (inject `body{font-family:Verdana,"DejaVu Sans"}`); a PR that edits the site-wide check lists selects ~136 verifiers, so ANY near-limit verifier line (70% of 270 s) blocks it: check `PR budget` job text.

## Decided for you (hc-factor; found-a-mark's list is in its PR #569)
- Palette: LIGHT row, not dark: check-theme derives it from the roster levels (GCSE = light). The stage is dark panels inside it.
- "Round" in the UI for the contract's "stage"; "You're through to the next round!" when at least half the marks, never a block.
- Round 6 has no leaderboard (stage-6 needs a label in firebase-leaderboard.js, shared); rounds 1-5 use stage-1..stage-5.
- Round 6: 2 marks a question (signs, then numbers).
- Extra named slips: S3 divided the x term but not the number; S6 add to b but multiply to -c; S2 kx(x+a) lost the k on the second term.
- Unsigned boxes (no toggle) take 0 or more; a missing term is typed as 0.
- Short phones (height under 620 px): Next sits under the one-line reason, the worked answer after it.
- Rows: #103, Unlisted (3).

## y-so-steep: state (27 Oct 2026)
S1, S2, S4, S5, S6 shipped with whole-number items; S3 ("Rearrange it") and fractional items OFF. Generator `schools/assets/y-so-steep-gen.js` (whole-number and with-fractions banks, 48 items a stage; the 6 P's imports it later); verifier `scripts/verify-y-so-steep.py` (3 parts, about 22,000 probe answers marked both ways against an independent marker). Roster #104, Unlisted (4). Keypad: `MaffsKeypad.mount(..., {keys: {fraction: true}})` on the unmerged branch above; `MaffsAnswer.fraction()` already exists, so test-answer-js.py needed no new cases.
Decided for you: light palette; fractions off until the keypad branch merges; Stage 6 has no board (stage-6 needs a label in firebase-leaderboard.js, shared; stages 1-5 use stage-1..stage-5, stage-3's declared but unused); Stage 5 has two steps (the gradient is given) and about 92% of its given points are off the y-intercept (minimum 75%); Stage 2's line comes from the figure data (no equation in its stem); marking by value through MaffsAnswer.fraction(), no game parser; extra slips on Stage 1 (m and c swapped; sign of c); a slip equal to the right answer is dropped; "run over rise" only fires once fractions are on; marks a question 1/1/1/3/2/3 (S1..S6).
Lessons: merge-pr.py refuses while main's run is queued (other lanes push often): use `--wait 540`; end-task.py must be run from a CURRENT worktree (the primary checkout's scripts/ is stale), e.g. `python scripts/end-task.py <branch>` from any worktree.
