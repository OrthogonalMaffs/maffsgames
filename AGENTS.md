# AGENTS.md — Codex entry point for MaffsGames

This file is an index, not a rulebook. The rules live in the files below; open them and read them as files.
If this file and any of them disagree, they win and this file is wrong: say so in your report. **The only
exceptions are the Codex-specific rules listed under "Codex overrides" below.** For those, this file wins.

## Codex overrides (Jon, 29 Oct 2026)
- Branch prefix `codex/<task>`, where `CLAUDE.md` says `claude/<task>`. The scripts accept either.
- How you are launched and where your git metadata lives: as `docs/agent-workflow.md` (git safety section)
  specifies for Codex, where that differs from `CLAUDE.md`'s worktree commands.

## Before any task
1. Read `CLAUDE.md` in full. It is written for Claude Code. Where it names Claude tools or session controls
   (the Bash tool, `run_in_background`, `/tasks`), apply the intent with your own tools; do not claim the Claude
   mechanisms exist for you. Where it says "Code Claude" or "the session", it means you.
2. Read `docs/agent-workflow.md`: roles, tiers, the report format, failure handling.
3. Read `docs/canon.md` §0 and every section your contract names.
4. Read both handovers, `docs/handover/home.md` and `docs/handover/cloud.md`: yours for current work, the other
   for conflicts. Read `E:\jon\lanes\notes.md`; if you cannot, say so before starting, and do not start a
   Shared-tier task without it. Your contract names your lane and tier; if either is missing, stop and ask.
5. Read the `.claude/rules/` files your task touches (`game-roster.md`, `analytics.md`, `timer-policy.md`,
   `help-audit.md`). Skip `project-claude.md`: it is the planner's brief, not yours.
6. Before touching a file, state the root cause in one sentence, and check the contract against the code.

## Non-negotiable mechanics (`CLAUDE.md` has the reasons)
- Start: `git fetch`, then `git worktree add -b codex/<task> <path> origin/main`. Work only there.
  Never pull or merge into the primary checkout or an existing branch.
- Before the first edit, `git status --porcelain` in your worktree is empty. If not, stop.
- Before the first push: `python scripts/check-changed.py`.
- Merge only with `python scripts/merge-pr.py <number>`. Never `gh pr merge`, the button or a raw API call.
  **Shared tier: stop at Gate green and wait for "merge"; do not run `merge-pr.py` until told.**
- After merging, wait for main's full `check-site` run and report it. A red or cancelled run is dealt with,
  under `CLAUDE.md`'s rules, before new work starts.
- Finish with `end-task.py`, run as `CLAUDE.md` currently specifies. If it refuses, report the reason.
  Never remove a worktree or delete a branch by hand.
- Background processes only via `python scripts/bg.py -- <command>`.
- GitHub through `gh api` REST endpoints only. GraphQL-backed `gh` subcommands (`gh pr list`, `gh pr view`,
  `gh pr checks`, `gh pr status`, `gh issue view`) are not used here.
- Gate files belong to the cloud lane. Report proposed changes; do not edit unless your contract puts you in
  that lane for that work.

## Working rules
- The task arrives as a seven-field contract: TASK, ROOT CAUSE, CLASS CHECK, EXACT CHANGE, DO NOT TOUCH,
  SUCCESS CONDITION, STOP IF. DO NOT TOUCH and STOP IF are binding. If a field is missing, or the code
  contradicts the contract, stop and report before editing.
- Change nothing outside EXACT CHANGE: no refactoring, renaming, reformatting or tidying. Do not invent a
  parallel workflow.
- Put the contract and your report in the PR body. The report format is in `docs/agent-workflow.md`.
- Report what you ran and what it returned. Never claim a check passed that you did not run; "not run" is an
  acceptable line.
- A green verifier proves the maths only if it computes the answer independently of the game's own code. Say
  which kind of check it was.
- No new data collection, no new external dependencies, no change to the platform principles in canon §0.
- If a task or the access it needs cannot be completed safely, stop and report. Never skip an instruction
  silently.
