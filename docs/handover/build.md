# Build lane handover

Lane rules: new, fully specified games only; new files only; games stay unlisted; branches `claude/build-<slug>`; worktrees `E:/jon/mg-build-<slug>`.
Contracts are saved verbatim in `docs/handover/contracts/<date>-build-<slug>.md`.

## Queue
1. **found-a-mark** ("I Found a Mark") — contract `contracts/2026-10-27-build-found-a-mark.md`. IN PROGRESS. Worktree `E:/jon/mg-build-found-a-mark`, branch `claude/build-found-a-mark`.

2. **hc-factor** ("The HC Factor") — contract `contracts/2026-10-27-build-hc-factor.md`. QUEUED (received 27 Oct, mid-build of #1). Branch `claude/build-hc-factor`, worktree `E:/jon/mg-build-hc-factor` (create from origin/main when starting). Not started.

## found-a-mark: state (27 Oct 2026)
Milestones: module pushed (fbbd7e6e); game page `games/i-found-a-mark/index.html` written and plays end to end at 375x667; fold fix for the garden question (last option 654px vs 627px fold) in progress; then verifier, shared-file lines, CI, merge.
Done: read CLAUDE.md, canon §0/§7/§8.2.1; surveyed the last unlisted-game PR (#509) for the minimum shared-file lines a new game folder needs.

Design (so a fresh session can carry on):
- Module `schools/assets/found-a-mark-templates.js` (`MaffsFoundAMark`, pure data, seedable rng). Each calculation is an `expr` string of space-separated tokens (numbers, `+ - * / ^ ( )`, `@stepId` refs); tex is derived from the expr; the verifier re-evaluates the same strings with Fractions in Python and re-derives each question from its `params`.
- Marks are slots; a step carries a `slot`; a slot completes when `need` of its steps are found. A step may have several `forms` (alternative expressions, each with its own deps). Distractors carry `deps` (their refs), a `for` step and a `why`.
- Wrong tap shows the one-line `why` plus MaffsNext (3 s floor), then the options come back with that one struck out. Hinted steps never score.

Shared-file lines a new game needs (the #509 pattern; each marked unlisted, to be reported): `.claude/rules/game-roster.md` (Unlisted + row), `data/games.json`? (only at listing, #509 added it; check), `scripts/audit-register.py` UNLISTED_NOT_BY_AUDIT, `scripts/check-answer-lock.py` MIGRATED, `scripts/check-leaderboard-coverage.js` NOT_ON_HUB, `scripts/check-levels.py`, `scripts/check-start-mount.py` CONTAINERS, `scripts/check-teacher-invite.py` RESULTS, `scripts/check-theme.py` MIGRATED, plus `docs/audits/findings/<slug>.yml`.
Leaderboard: a new board key needs a label in `schools/assets/firebase-leaderboard.js` (shared). If that can't be avoided, leave the board off and report.

## Decided for you
(filled in at the report)
