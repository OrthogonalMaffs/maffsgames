# Agent workflow — MaffsGames

Task mechanics, WSL setup and recovery have one home: AGENTS.md. This document covers the people, review tiers and evidence passed between them. Canon §0 supplies platform principles and findings severities.

## 1. Roles

| Who | Does | Does not |
|---|---|---|
| **Jon** | Decides scope and priority; reviews content (maths, wording, feel); plays games on the live site; makes rulings | Review code; approve merges |
| **Project Claude** (architect) | Investigates; writes contracts; answers implementer questions; reviews PRs on GitHub; classifies findings | Edit the repo; merge |
| **Implementer** (Code Claude or Codex) | Checks the contract against the code; implements; runs checks; reports honestly; finishes the lifecycle under AGENTS.md | Expand scope; change shared files outside its lane; bypass safeguards; claim checks it did not run |

Lane slots and ownership are defined in AGENTS.md.

**Neither agent sees the other's conversation.** Everything that crosses between them is written down: the
contract (in the PR body), the report (in the PR body), the handover file, the notes file, and the diff itself.
Project Claude reviews what is on GitHub, never a summary alone.


## 2. Tiers

Project Claude sets the tier in the contract; when unsure, classify it Shared. Scope growth into a shared file stops a Small/Medium task for re-tiering.

| Tier | Scope | Contract | Review |
|---|---|---|---|
| Small | One game's files, one bank, docs, a game in new files | Light, seven fields | After merge |
| Medium | Several games, one shared file for a new game, verifier rework | Full | After merge |
| Shared | Infrastructure multiple games load or CI runs, shared assets, analytics, Firebase, roster format or gate files | Full | Before merge |

Shared work waits because one fault can affect many games and existing checks cannot prove every behaviour. Merge authority and holds are specified in the rulebook.

## 3. Lifecycle and evidence

Jon sets priorities through Project Claude, who investigates main, handovers and lane notes, answers CLASS CHECK and supplies the contract. The implementer follows AGENTS.md, produces the scoped change and opens a PR containing the contract and report below.

For Shared work, write “Ready for architect review” when the Gate is green. Jon relays the PR for Project Claude to review the actual GitHub diff. Findings follow §4; approval is recorded in the handover. Visible work is accepted after Jon plays it.

| State | Evidence |
|---|---|
| Implemented | Commits on the task branch |
| Checked locally | Output for the selected local checks |
| Gate green | Successful Gate on the PR head |
| Reviewed | Project Claude's APPROVE, noted in handover |
| Merged | Squash commit on main |
| Live | Successful full main run and deployed page |
| Accepted | Jon has played it |

### 3.4 The report

The implementer's report goes in the PR body, under the contract:

```
## Report
CONTRACT: <TASK line>   TIER: <...>   LANE: <...>   IMPLEMENTER: <Claude Code|Codex>
BRANCH: <the actual branch name>
STATE: <Implemented | Checked locally | Gate green | Merged | Live>   (see §3's state table)

CHANGED: <file — one line on what changed; one line per file>

RAN:
- <command> → <result; pass/fail counts; paste the summary line>

NOT RUN: <each check the contract or check-changed.py named that did not run, and why; or "none">

MATHS: <for any answer-bearing change: how each answer is computed, and whether the check is independent of
the game's own code; or "no answer-bearing change">

DEVIATIONS: <anything done differently from EXACT CHANGE, and why; or "none">

STOP IF HIT: <which, and what was reported; or "none">

OPEN: <anything left for Project Claude or Jon; or "none">

CLEANUP: <end-task.py result, or its refusal reason; or "pending">
```

Every RAN line is backed by output from this task. "Not run" and "failed" are acceptable; an unbacked "passed" is a HIGH finding. Final-state handover maintenance follows AGENTS.md.


## 4. Review

### 4.1 What Project Claude reads

From GitHub, in this order: the PR body (contract and report), the diff, the surrounding code the diff calls or is
called by, the Gate's job list and results, and any verifier the change should have run.

### 4.2 What it checks

1. **Contract fit.** Did the diff do EXACT CHANGE, and only that? Anything in DO NOT TOUCH touched?
2. **Correctness of the maths.** Is each answer computed, and is the check that confirms it independent of the
   code that generated it? A verifier that recomputes with the game's own formula is not independent.
3. **Report vs diff.** Does the report claim anything the diff or the Gate does not show?
4. **The class.** Did the fix land at the layer CLASS CHECK named, or at one call site?
5. **Regressions.** Who else loads the changed file? Did their checks run (the Gate's selection) or were they deferred?
6. **Platform principles.** KaTeX, `dataset.val`, no new data collection, question counts, adult register.
7. **Simplicity.** Is anything added that the contract did not ask for?

Style preferences are not findings. If it would not change what a student sees, what a teacher trusts, or what
breaks next, it is a note at most.

### 4.3 Findings

Format: Project Claude's review template, kept with Project Claude's project documents, not in this repo. Severities are the repo's own (canon SR-20/21):

| Severity | Meaning | Action |
|---|---|---|
| CRITICAL | Wrong maths or a broken game reachable by a student | Fix now; the game may be unlisted under SR-20 |
| HIGH | Wrong behaviour likely to be hit; a contract violation; a false claim in the report | Fix before the next task in that lane |
| MEDIUM | Real defect, unlikely to be hit or cosmetic-with-consequence | Queue |
| LOW | Minor | Queue or note |

Findings go back as a **new seven-field contract**, never as loose notes. For Shared-tier PRs not yet merged, the
same branch is fixed and re-reviewed.

### 4.4 Stopping the loop

- Round 2 is the last automatic round. If a third round would be needed, Project Claude sets out the
  disagreement and Jon rules.
- A finding the implementer disputes with evidence (a command and its output) goes to Jon with both sides, not
  round again.
- MEDIUM and LOW never hold a merge (SR-21).


## 5. Failure handling

Consult AGENTS.md for unexpected events, bounded check fixes, missing access, worktree safety and interrupted-task recovery. The contract's boundaries remain the stop conditions.

| Situation | Review response |
|---|---|
| A contract contradicts code | Project Claude supplies a corrected contract after the implementer's report |
| A requirement is ambiguous | Jon or Project Claude answers in writing |
| A pre-existing check fails | Record baseline evidence; Jon decides any exception |
| A finding is disputed with evidence | Jon receives both positions, the command and its output |
| A CRITICAL is found | Project Claude tells Jon at once; a fix contract and SR-20 where applicable |
| Report and diff disagree | HIGH finding; correct the report and any required implementation |

The PR is the reviewable record: statements of success need output from this task. Maths claims distinguish independent recomputation from consistency with a game's own code.
