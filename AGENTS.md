# MaffsGames — agent rulebook

This is the single home for agent-neutral mechanics. Codex loads it directly; Claude Code imports it. Reasons and history: canon §12, RULEBOOK. Roles, tiers and report format: `docs/agent-workflow.md`.

## Before every task

- Read the workflow, canon §0 and contract-named sections, and both lane handovers, including their Queues. Your handover gives current work, the other gives conflicts. Missing access: stop and report.
- Require TASK, ROOT CAUSE, CLASS CHECK, EXACT CHANGE, DO NOT TOUCH, SUCCESS CONDITION, STOP IF, lane and tier. Before editing, state the root cause in one sentence and check the contract against code. Missing fields or a contradiction: stop.
- CLASS CHECK precedes EXACT CHANGE: repeated bug shapes, shared infrastructure or missing safety on multiple call paths require an architectural fix. Otherwise explain why the defect is local. Reference: canon §12, RULEBOOK.
- Apply canon §0.3 standing rulings before asking for decisions; list applied SR numbers in the PR. Contract STOP IF and “Still stops for Jon” remain binding.
- Change only EXACT CHANGE: no unrelated refactoring, renaming, reformatting or tidying. No new collection, dependencies or changes to canon §0 principles. Unsafe work or access: stop and report.
- Codex skips the planner's `.claude/rules/project-claude.md`. Claude Code's role clarification is in CLAUDE.md. Read saved contracts only when starting their item, never the contracts directory at session start.

## Platform principles (bind every task)

- Free forever. No subscription, no freemium, no ads.
- No sign-up required. Zero friction for students.
- **No personal data collected.** Anonymous gameplay events go to GA4 (cookieless) and a Google Sheets backend, all disclosed on the privacy page. No new collection without Jon's approval.
- Curriculum aligned. Every game maps to the AQA, Edexcel, OCR or BTEC spec.
- Single-file HTML games. No build step, no external runtime dependencies beyond KaTeX via CDN.
- Minimum **40–50 questions per game.** Twenty is a starter activity, not a class resource.
- Mathematical notation via **KaTeX** for expressions (scope in canon §7.1.1). No ASCII approximations.
- Answer matching via **`dataset.val`** always. Never compare rendered HTML strings.
- **The maths must be right.** A struggling student is the least able to spot a wrong answer. Correctness outranks new features.

## WSL and git

- Use WSL distro `maffs`, primary `/home/maffs/maffsgames`, venv `/home/maffs/.venvs/maffs`; no sandbox, never sudo. Confirm identity `Vector52F <262527784+Vector52F@users.noreply.github.com>`; report a missing/different identity before committing.
- The identity check is WSL-only; the cloud lane commits as `Claude <noreply@anthropic.com>` (the squash merge lands on main as Vector52F). Reason: canon §12, CLOUD-LEAN.
- The primary checkout is never edited; before starting an agent session, fast-forward it: git -C ~/maffsgames pull --ff-only (stop if it is not a fast-forward). Reason: canon §12, PIES-SIGNOFF-AND-PRIMARY-FF.
- Start each new task with these commands, substituting its task name; use `codex/` for Codex, `claude/` for Claude Code. Work only in that new worktree. Never pull or merge into an existing task branch.

```sh
git -C ~/maffsgames pull --ff-only
git -C ~/maffsgames fetch origin
git -C ~/maffsgames worktree add -b codex/<task> ~/mg-<task> origin/main
```

- Before the first edit, `git status --porcelain` must be empty. Unexpected changes: stop, list paths without contents, leave them alone. Linked worktrees share the primary's git metadata; task file edits stay in their own worktree.
- Never use hard reset, clean, force push or manual branch/worktree deletion; never stash in another task's worktree. Revert merged changes through a fresh branch and PR, preserving main's history. Recovery: the takeover rule below.
- Use `gh api` REST endpoints only, including in scripts; no GraphQL-backed gh commands (pr list/view/checks/status, issue view and similar). Missing tool or write access: stop and report.

## ENCODING and processes

- Edit with your file-edit tool: apply_patch in Codex, Edit in Claude Code. Use `python -X utf8`. After editing non-ASCII text, read the changed lines as UTF-8 in Python and verify their characters, not their console appearance. History: canon §12.
- Start every background server or long loop with `python -X utf8 scripts/bg.py -- <command>`, never raw `&` or nohup. Cleanup uses its registry; stop harness-owned background sessions through that harness's controls. Reference: canon §12, RULEBOOK.
- Never pipe a verifier through tail under a timeout. Preserve output in a log, use the registered launcher for long background checks, and report the command's own exit status. Reason: canon §12, RULEBOOK.

## Checks, merge and cleanup

- Before the first push, run `python -X utf8 scripts/check-changed.py`; SR-27's verifier-only exception applies. Report selected checks and CI deferrals. The cloud lane's rule is the next line. Queue details: `docs/rules/scripts.md`.
- The cloud lane does not run check-changed.py. Before its first push it runs only the worst-case test where canon §7.8.4 requires it by hand, and the selftest of any script it changed; the PR's Gate is the check. The home lane keeps check-changed.py. Reason: canon §12, CLOUD-LEAN.
- A check failing after your change may be fixed when its cause is understood and the fix stays in EXACT CHANGE's files. Stop if the same check still fails after your second fix, or its cause is unclear. Any other unexpected event: stop and report. Jon, 2 Nov; canon §12.
- Merge only with `python -X utf8 scripts/merge-pr.py <number>`, unpiped; check its exit status before proceeding. No other merge route. It requires green Gate on the PR head and green main; an override needs Jon's written dated ruling. Detail: canon §7.8.3.
- Shared tier stops at Gate green for Project Claude review and waits for Jon's “merge”. Small/Medium merge on green unless a contract or hold says otherwise. Definitions and review handling: `docs/agent-workflow.md`.
- The merging agent merges with `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600` and reports its last line. Resolve red/cancelled main before new work. Either lane may rerun failed jobs once; report a rerun pass to cloud as a flake. Reference: canon §12.
- After merge and the main-run report, cleanup is authorised: run a temporary copy of origin/main's end-task script from the primary with the branch argument. It requires a merged PR, matching local/PR tips and a clean worktree. Report refusals without bypassing them. See canon §12.

```sh
git -C ~/maffsgames show origin/main:scripts/end-task.py > /tmp/maffs-end-task.py
cd ~/maffsgames
python -X utf8 /tmp/maffs-end-task.py <branch>
```

- Size limit: check-context-size.py warns past 18 KiB and fails past 20 KiB for AGENTS.md, CLAUDE.md and both handovers. Archivable handovers warn; main archives to 17 KiB; unarchivable excess fails. Todo's cap is 150 KiB without the band; canon is reported only. See canon §12.

## Lane ownership

- At most two implementers run, one per lane; an agent occupies a slot. Home owns shared code/assets, canon and docs, including batched relisting; cloud owns per-game fixes and their findings. Edit only your lane's handover. Contract exceptions must be explicit. See canon §7.8.2.
- Shared-file work requires one lane with nothing else running unless Jon explicitly allows concurrency in the contract or its amendments. History: canon §12, RULEBOOK.
- Gate files belong to cloud: workflow, `scripts/ci-*`, ci_shards.py, merge-pr.py, check-context-size.py and check-changed.py. Other lanes report proposed changes and wait. Before game/listing work read `docs/rules/games.md` for claims and register restrictions.
- Put cross-lane facts (merge dependencies, files in use, flakes) in the writing lane's handover Queue, before its first `## ` entry; the archive never moves that preamble. Both handovers are read before every task. Rationale: canon §12, RULEBOOK.

## Contracts and handovers

- Corrections arrive as numbered amendments to the in-flight contract (Jon, 30 Oct 2026). Save contracts verbatim in `docs/handover/contracts/` with a queue pointer; move to `docs/history/contracts/` on completion. Include contract, amendments and report in the PR. See workflow §3.4.
- Commit and push at milestones; keep the branch handover current with done, next and discoveries. Context percentage never stops a task: only Jon can measure it and clear the session. Archives are history, not startup reading. Rationale: canon §12, RULEBOOK.
- A fresh context is a new cloud session, never /clear: /clear keeps the session's original clone, so it reloads the rules of the day it started. Reason: canon §12, CLOUD-LEAN.
- Handover entry format: every entry starts `## <yyyy-mm-dd> (<lane>): <TASK> ...`, newest first, so check-context-size.py can archive it. “Done” means merged and live, with review state separate. Archived bodies stay unchanged. Reason: canon §12, RULEBOOK.

### Changing agent mid-task

The handover entry names the agent, worktree path, branch, last commit and next step. The taking-over agent checks `git status --porcelain` and `git log origin/main..HEAD` against the handover, then uses the same worktree and branch, retaining its original prefix. See canon §12.

### Task record

End each finished entry:

```text
Record: agent <Codex|Claude Code>; wall <h:mm from contract received to hand-off for review, or to a STOP>; review cycles <n>; amendments <n>; usage <figure as the agent reports it, or "n/a">.
```

Gate green/STOP; no usage estimates. Canon §12.

### What may enter an always-loaded file

A new entry is its rule plus a pointer, at most 300 UTF-8 bytes; put reason and history in canon §12 in the same PR. Only rules every task needs stay loaded. Move area rules only on unambiguous triggers and list every move. See the trigger table.

## Read on the matching trigger

Before working in an area below, read its file. If a trigger is ambiguous, retain that rule here and list it for review.

| Area / trigger | File |
|---|---|
| Scripts, verifiers, CI or local-check planning | `docs/rules/scripts.md` |
| Local rendering, previewing or browser tests | `docs/rules/local-testing.md` |
| Games, banks, findings, claims or listing/relisting | `docs/rules/games.md` and `.claude/rules/game-roster.md` |
| Escape-room code or artwork | `docs/rules/escape-rooms.md` |
| Analytics or event logging | `.claude/rules/analytics.md` |
| Timers or scoring clocks | `.claude/rules/timer-policy.md` |
| Help or instructions | `.claude/rules/help-audit.md` |

Current-state pointers: both handovers; `docs/todo.md`; canon §0 (principles), §7 (technical), §11 (rooms), §12 (engineering); findings in `docs/audits/findings/`. Tech Stack: canon §12, “Tech Stack”.
