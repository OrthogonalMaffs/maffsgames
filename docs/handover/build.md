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
DONE: 2026-10-27-build-found-a-mark.md   (PARKED at the merge, see "Parked" below; everything else is built)

## Queue
1. **found-a-mark** ("I Found a Mark") — contract `contracts/2026-10-27-build-found-a-mark.md`. IN PROGRESS. Worktree `E:/jon/mg-build-found-a-mark`, branch `claude/build-found-a-mark`.

2. **hc-factor** ("The HC Factor") — contract `contracts/2026-10-27-build-hc-factor.md`. QUEUED (received 27 Oct, mid-build of #1). Branch `claude/build-hc-factor`, worktree `E:/jon/mg-build-hc-factor` (create from origin/main when starting). Not started.
3. **y-so-steep** ("Y So Steep?") — contract `contracts/2026-10-27-build-y-so-steep.md`. QUEUED. Branch `claude/build-y-so-steep`, worktree `E:/jon/mg-build-y-so-steep`. Item 4 (fraction entry) may need an UNMERGED shared-asset branch; see the contract.

## Parked
**found-a-mark, PR #569 (head 32af744d): the CI Plan job fails, so the Gate is red; not merged.**
The change edits the site-wide check lists a new game folder needs, so it "selects 136 verifiers (CI itself)", and the Plan job's per-line rule then fails on a line that is not mine: `Content verifiers 19: Equation Builder, part 1: 137s (median) + 56s setup = 193s, 71% of its 270s budget; the limit is 70% (189s)` (timings from main run 40494866923). Every other check in the PR passed locally (check-changed.py: only three failures, all mine, all fixed: burst.js not adopted, meta description length, the last button's wording).
**Question for Jon / home lane:** split or speed up Equation Builder part 1 (home lane's CI), or tell me to wait for the next main timings pack and re-run the PR; I will not touch ci-groups or the Equation Builder verifier (shared). To resume: re-run the PR's CI, then `python scripts/merge-pr.py 569` (unpiped), watch main, run `python scripts/end-task.py claude/build-found-a-mark`, then report with the screenshots.
Screenshots (375x667 and 1366x768, every question type) are in the session scratchpad `shots/` folder: garden_*, interest_*, ratio_*, enough_*; re-make with the play script if lost.

## found-a-mark: state (27 Oct 2026)
Milestones: module, game page (fits 320x568, 375x667, 1280x720) and verifier (3 parts, 6 plants, all caught) pushed. Shared-file registrations (roster, games.json, 7 check lists, findings yml) added; `check-changed.py` run in background; next: push, PR, `merge-pr.py`, watch main, screenshots 375x667 + 1366x768.
Done: read CLAUDE.md, canon §0/§7/§8.2.1; surveyed the last unlisted-game PR (#509) for the minimum shared-file lines a new game folder needs.

Design (so a fresh session can carry on):
- Module `schools/assets/found-a-mark-templates.js` (`MaffsFoundAMark`, pure data, seedable rng). Each calculation is an `expr` string of space-separated tokens (numbers, `+ - * / ^ ( )`, `@stepId` refs); tex is derived from the expr; the verifier re-evaluates the same strings with Fractions in Python and re-derives each question from its `params`.
- Marks are slots; a step carries a `slot`; a slot completes when `need` of its steps are found. A step may have several `forms` (alternative expressions, each with its own deps). Distractors carry `deps` (their refs), a `for` step and a `why`.
- Wrong tap shows the one-line `why` plus MaffsNext (3 s floor), then the options come back with that one struck out. Hinted steps never score.

Shared-file lines a new game needs (the #509 pattern; each marked unlisted, to be reported): `.claude/rules/game-roster.md` (Unlisted + row), `data/games.json`? (only at listing, #509 added it; check), `scripts/audit-register.py` UNLISTED_NOT_BY_AUDIT, `scripts/check-answer-lock.py` MIGRATED, `scripts/check-leaderboard-coverage.js` NOT_ON_HUB, `scripts/check-levels.py`, `scripts/check-start-mount.py` CONTAINERS, `scripts/check-teacher-invite.py` RESULTS, `scripts/check-theme.py` MIGRATED, plus `docs/audits/findings/<slug>.yml`.
Leaderboard: a new board key needs a label in `schools/assets/firebase-leaderboard.js` (shared). If that can't be avoided, leave the board off and report.

## Decided for you
(filled in at the report)
