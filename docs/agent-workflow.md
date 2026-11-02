# Agent workflow — MaffsGames

**Proposed home:** `docs/agent-workflow.md`. Draft, 29 Oct 2026.

This document describes how tasks move between Jon, Project Claude and an implementer. It does not restate
rules that live elsewhere: where a rule already exists it is named, with its file, and that file wins.

| Rule | Lives in |
|---|---|
| Mission, priorities, platform principles | `docs/canon.md` §0, `.claude/rules/project-claude.md` |
| Two lanes, who edits what, the merge guard, the Gate | `docs/canon.md` §7.8.2–§7.8.4, `CLAUDE.md` |
| Start a task in a new worktree; end it with `end-task.py` | `CLAUDE.md` (ESCAPE-SET-CHECKS, WORKTREE-CLEANUP) |
| Background processes via `bg.py` | `CLAUDE.md` |
| Current lane rules (two at a time, freeze, notes file) | `claude/lane-plan-*.md` (Project) and `E:\jon\lanes\notes.md` |
| Findings severities and when a game is held back | `docs/canon.md` SR-20, SR-21 |

---

## 1. Roles

| Who | Does | Does not |
|---|---|---|
| **Jon** | Decides scope and priority; reviews content (maths, wording, feel); plays games on the live site; makes rulings | Review code; approve merges |
| **Project Claude** (architect) | Investigates; writes contracts; answers implementer questions; reviews PRs on GitHub; classifies findings | Edit the repo; merge |
| **Implementer** (Code Claude or Codex) | Checks the contract against the code; implements; runs checks; reports honestly; merges through `merge-pr.py` when its tier allows; cleans up with `end-task.py` | Expand scope; change shared files outside its lane; bypass the Gate or `merge-pr.py`; claim checks it did not run |

**Codex is a lane occupant, not a lane.** The two-lanes-at-a-time rule stands. When Codex works, it takes the
home or build lane's slot for that task, and its contract says which. A third concurrent implementer is out of
scope until Jon rules otherwise.

**Neither agent sees the other's conversation.** Everything that crosses between them is written down: the
contract (in the PR body), the report (in the PR body), the handover file, the notes file, and the diff itself.
Project Claude reviews what is on GitHub, never a summary alone.

---

## 2. Tiers

The tier is set in the contract by Project Claude. It decides the contract form and when review happens. It does
not change the mechanics: every tier uses a worktree, the Gate and `merge-pr.py`.

| Tier | What it covers | Contract | Review | Merge |
|---|---|---|---|---|
| **Small** | One game's files, one bank, docs, a new game in new files | Light (seven fields) | After merge | Implementer, Gate green |
| **Medium** | Several games, a new game touching one shared file, a verifier rework | Full | After merge | Implementer, Gate green |
| **Shared** | Anything more than one game loads, or that CI runs: shared JS/CSS under `schools/assets/`, `bank_common.py`, `MaffsAnswer`, the keypad, the footer, analytics, `firebase/`, the roster format, gate files | Full | **Before merge** | Implementer, after Project Claude's APPROVE |

**Why shared work waits for review.** One fault in a shared file breaks many games at once, and the Gate only
proves the checks that exist. Everything else merges first and is reviewed after, because a follow-up PR is
cheaper than a held queue — the existing practice.

**When unsure, it is Shared.** An implementer who finds that a Small or Medium task needs a shared file stops
(STOP IF) and reports; the task is re-tiered, not quietly widened.

---

## 3. The lifecycle

### 3.1 Small and Medium

1. **Jon** describes the task to Project Claude.
2. **Project Claude** reads the repo (GitHub `main`), checks the handovers and notes, answers CLASS CHECK, and
   writes the contract. Questions only Jon can answer are asked before the contract, not inside it.
3. **Jon** pastes the contract to the implementer. Timing conditions are inside the contract (STOP IF); Jon
   never has to hold a contract back.
4. **Implementer, before editing:** reads the files `AGENTS.md`/`CLAUDE.md` name; `git fetch`; new worktree
   from `origin/main`; reads the code the contract touches; **checks the contract against the code.** If the
   contract is wrong (a file has moved, a function does not do what ROOT CAUSE says, a STOP IF fires), it stops
   and reports — see §5.
5. **Implementer** builds, runs `python scripts/check-changed.py` and any verifier the contract names, pushes,
   opens the PR with the contract and the report (format in §3.4) in the body.
6. Gate green → **implementer** merges with `python scripts/merge-pr.py <n>`, watches main's full run, reports
   it, runs `python scripts/end-task.py <branch>`, updates its lane handover.
7. **Jon** passes the PR number to Project Claude.
8. **Project Claude** reviews the merged diff (§4). APPROVE closes it. Findings become a follow-up contract.
9. **Jon** plays it on the live site where the change is visible.

### 3.2 Shared

As above, except at step 6 the implementer **stops at Gate green**, writes "Ready for architect review" in the
PR body, and does not merge. Jon passes the PR number; Project Claude reviews the unmerged diff; on APPROVE, Jon
tells the implementer "merge" and it continues from `merge-pr.py`. On findings, §4.3.

### 3.3 States

These are distinct and a report names which one a task is in:

| State | Means | Evidence |
|---|---|---|
| Implemented | Code written in the worktree | Commits on the branch |
| Checked locally | `check-changed.py` and named verifiers passed | Command output in the report |
| Gate green | CI passed on the PR head | The Gate check on GitHub |
| Reviewed | Project Claude returned APPROVE | Review in chat; noted in the handover |
| Merged | Squash-merged via `merge-pr.py` | Merge commit on `main` |
| Live | Main's full run green; GitHub Pages deployed | Main run; the page loads |
| Accepted | Jon has played it | Jon says so |

"Done" in a handover means **Merged and Live**, with the review state stated separately.

### 3.4 The report

The implementer's report goes in the PR body, under the contract:

```
## Report
CONTRACT: <TASK line>   TIER: <...>   LANE: <...>   IMPLEMENTER: <Code Claude|Codex>
BRANCH: <the actual branch name>
STATE: <Implemented | Checked locally | Gate green | Merged | Live>   (see §3.3)

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

Every RAN line is backed by output from this task. "Not run" and "failed" are acceptable; an unbacked "passed" is a HIGH finding. The lane handover entry is updated after the merge to the final state.


---

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

---

## 5. Failure handling

| Situation | Who acts | Response | Resumes when |
|---|---|---|---|
| Contract contradicts the code | Implementer | Stop before editing; report what the code does, with file and line | Project Claude issues a corrected contract |
| Requirement ambiguous | Implementer | Stop; one question, with the options it sees | Jon or Project Claude answers in writing |
| A check fails **before** any change | Implementer | Stop; report it as pre-existing (main's run state, the failing check) | Main is green, or Jon's ruling with `--override` |
| A check fails **after** the change | Implementer | Fix within scope; if the fix needs a file outside EXACT CHANGE, stop | Fixed, or contract widened |
| Non-ASCII becomes `?` after an edit (PowerShell's legacy code page) | Implementer | Stop; follow AGENTS.md's ENCODING rule: apply_patch edits, `python -X utf8`, verify UTF-8 file bytes | Original text restored and UTF-8 verification passes |
| Main's last full run is red | Implementer | Do not merge (`merge-pr.py` refuses anyway); one re-run of failed jobs is allowed (lane plan rule 4) | Main green |
| Tool or access missing (`gh`, network, notes file) | Implementer | Stop; say exactly what failed | Jon fixes access |
| Unexpected changes in the worktree | Implementer | Stop; list them (`git status --porcelain`, no contents); touch nothing | Owner identified |
| Scope grows | Implementer | Stop at the boundary; report what more is needed | New contract or re-tier |
| Project Claude finds a CRITICAL | Project Claude | Tell Jon at once; contract for the fix, and SR-20 if a live game is wrong | Fix merged |
| Agents disagree | Project Claude | Both positions, evidence, recommendation | Jon rules |
| Terminal closed or task interrupted | Next session | Read the handover; `git -C <worktree> status`, `log origin/main..HEAD`, PR state via `gh api` | State reconstructed and written in the handover |
| Task cannot be done safely | Implementer | Stop; say why; leave the worktree as it is and name it in the handover | Jon decides |
| Report and diff disagree | Project Claude | HIGH finding; the diff is the truth | Corrected report and, if needed, a fix |

Honest reporting is the rule under all of these: "not run", "failed" and "not verified" are acceptable report
lines. A claim that cannot be backed by output is not.

---

## 6. Worked example (Small tier, Codex)

**Task.** Jon: "The canon §0 escape-room row is stale."

**Project Claude** checks `main`: §0 says 8 live; §11.1 says thirteen with a table; the escape-rooms page lists 13.
CLASS CHECK: one fact in four places, so the fix removes the duplicate from §0 rather than updating it; the CI
check for the pages is Shared-tier work, deferred. It writes the light contract (the docs reconciliation contract
of 29 Oct), Tier: Small, Lane: home.

**Jon** pastes it into Codex, started in the home lane's slot.

**Codex** reads `AGENTS.md`, then `CLAUDE.md`, canon §0 and §11.1, `docs/handover/home.md`, the notes file.
`git fetch`; `git worktree add -b codex/docs-reconcile ..\mg-docs-reconcile origin/main`. It checks the contract:
§11.1 agrees with the page's 13 cards (STOP IF does not fire). It edits the two canon places, the Firebase
paragraph with the exact text given, adds the deferred item, runs `python scripts/check-changed.py` (docs-only:
no verifiers selected; site-wide fast checks pass), pushes, opens PR #6xx with the contract and report.

Gate green; `python scripts/merge-pr.py 6xx`; main's full run green; `python scripts/end-task.py
codex/docs-reconcile` removes the worktree; handover updated.

**Report (excerpt):** "State: Merged, Live. Ran: check-changed.py (output attached). Not run: none needed for docs.
Deviations: none. Open: none."

**Jon** passes "#6xx" to Project Claude.

**Project Claude** reads the diff: four files, as contracted; §0 row names no count; the Firebase paragraph matches
the given text exactly; no other canon section changed. Report matches diff. **APPROVE.** Notes for the handover:
"ESCAPE-COUNT-SOURCE deferred to after 2 Nov."

**Jon** has nothing to play; done.

## Git safety

**Interim, until the launcher and git wrapper exist (Jon, 30 Oct 2026):** Jon creates each Codex worktree from a normal terminal; Codex's git add, commit and push run on approval prompts that Jon checks name the task's worktree; Jon runs end-task.py outside Codex (from a temporary copy of origin/main's script) after closing Codex, because the sandbox cannot write git metadata and a running Codex session locks its folder.

The rules here already exist in `CLAUDE.md`; this section explains how they fit together and what changes for
Codex. Where `CLAUDE.md` and this section differ, `CLAUDE.md` wins and this section is fixed.

## 1. The layout (from the checkout audit, 29 Oct 2026)

- **One primary checkout:** `E:\jon\maffsgames-new-clone`. Every lane uses it. Nobody works in it directly.
- **One worktree per task**, a sibling folder (`E:\jon\mg-<task>`), on a branch made from `origin/main`.
- **Not part of the layout:** `E:\jon\maffsgames` (clone of the archived private repo) and `E:\jon\maffsgames-c1`
  (not a repo: runbook, patches, `old-pages.json`). No agent works in either. Jon decides their fate once they are
  confirmed to hold nothing unique.

## 2. Start of task

From the primary (shell-neutral; these work in PowerShell, Git Bash and WSL):

```
git -C E:\jon\maffsgames-new-clone fetch
git -C E:\jon\maffsgames-new-clone worktree add -b codex/<task> E:\jon\mg-<task> origin/main
```

Then work only inside `E:\jon\mg-<task>`. Never `pull` or `merge` into the primary or an existing branch: on
11 Oct 2026 that fast-forwarded the wrong branch (`CLAUDE.md`, ESCAPE-SET-CHECKS).

**The tree is not yours.** Before the first edit, `git status --porcelain` in the worktree must be empty. If it
is not, something else wrote there: stop.

## 3. During the task

- Edit only files EXACT CHANGE names. A file outside it is a STOP IF, even if the change looks harmless.
- Background processes only through `python scripts/bg.py -- <command>`. Orphaned servers have blocked worktree
  removal before (`CLAUDE.md`, 14 Oct).
- Before pushing: `python scripts/check-changed.py`.
- Never: `git reset --hard`, `git clean`, `git stash` in a worktree you did not create, `git push --force`,
  `git branch -D`, `gh pr merge`, the merge button, a raw API merge, `--override` without Jon's ruling in writing.

## 4. End of task

```
python scripts/merge-pr.py <pr-number>        # from the worktree; refuses unless Gate and main are green
python scripts/end-task.py <branch>            # from the primary; removes worktree and local branch only if safe
```

`end-task.py` refuses (and deletes nothing) if the PR is not merged, the local tip is not the PR's head, or the
worktree is dirty. **A refusal is reported in the handover with its reason, never worked around by hand.**

## 5. Known gaps (to fix after the freeze, Mon 2 Nov)

The 29 Oct audit found 20 worktrees: 10 idle on merged branches, 5 detached, plus 5 empty folders that are no
longer repos. That is one shared step failing, not twenty separate mistakes.

**Root cause found (cleanup run, 29 Oct):** `CLAUDE.md` says to run `end-task.py` "from the primary checkout", but
the primary is never updated (by rule: no pulls into it) and sits on `main` at `a5ee5c2f`, 11 Oct — the day
before `end-task.py` was written. The documented command has never existed where the rule says to run it. Proposed
fix: run the current script from `origin/main` without touching the primary, e.g.
`git -C E:\jon\maffsgames-new-clone show origin/main:scripts/end-task.py > %TEMP%\end-task.py`, then
`python %TEMP%\end-task.py <branch>` with the primary as working directory (the script is already designed to run
from a temporary copy). Same pattern for any script "run from the primary".

| Gap | Evidence | Fix at |
|---|---|---|
| `end-task.py` absent from the primary | Primary at `a5ee5c2f` (11 Oct); script dates from 12 Oct | `CLAUDE.md` rule: run from `origin/main` via a temporary copy |
| Orphan processes lock worktree folders | 29 Oct, Resource Monitor: a bash + python pair held each of mg-footer, mg-launch, mg-scroll and mg-tall. All came from one Claude Code session (27 Oct 19:27 to 28 Oct 00:24), started with a raw `&` or `nohup`, not through `bg.py`. The build lane's live worktree had `nohup.exe` running on 29 Oct. | Enforce at the tool level: block a raw `&` or `nohup` in agent shell commands unless the command goes through `bg.py`. A written rule alone has demonstrably failed. |
| `end-task.py` cannot see those processes | The server's command line was `scripts/serve-stubbed.py 8772`, with no worktree path in it. Only its working folder pointed at the worktree. | `end-task.py`: find processes by their working folder, not just their command line |
| Local servers that bypass the stubs | Two of the orphans were plain `python -m http.server`, not `serve-stubbed.py` | Check whether local plays from a plain server reach the real Sheets or Firebase backends. If they do, block it and assess the data. |
| Branch left behind when the folder cannot be deleted | mg-footer, mg-launch, mg-scroll: git emptied and unregistered the worktree, then "Permission denied" on the folder; branch not deleted | `end-task.py`: once git has unregistered the worktree, still delete the branch; report the folder as held |
| Worktrees left after merge | 10 idle on merged branches | Cause from the "Cleanup run 29 Oct" refusal reasons, then the shared layer: `end-task.py` or where it is called |
| Detached worktrees cannot be removed by `end-task.py` (it works by branch name) | 5 detached | `end-task.py`: a mode for a detached worktree whose HEAD is on `origin/main` or on a merged PR's head |
| Empty folders after removal | 5 empty, unregistered | Likely Windows file locks (`CLAUDE.md` line 158); `end-task.py` to report a folder it could not delete |

**This is a prerequisite for Codex.** A third agent on a broken cleanup step multiplies the folders.

## 6. Parallel work

- **Two lanes at a time** (lane plan rule 1). Codex takes a lane's slot; it does not add one.
- **Shared files: one lane, nothing else running** (the deferred shared-file list). A Shared-tier contract says so
  in its STOP IF.
- **Cross-lane facts go in `E:\jon\lanes\notes.md`** — "fetch main", merges others need, flakes. Read before each
  item.
- **What worktrees do not isolate:** the Firebase database, the Google Sheets endpoint, GA4, local ports used by
  stub servers, and GitHub Actions minutes. CI stubs the first three; local test servers must use the stubs
  (`serve-stubbed.py`). Two lanes starting stub servers on the same port collide: use `bg.py`, which records the
  PID, and let the server pick a free port where the script supports it.

## 7. Recovery

**Interrupted task** (terminal closed, session lost):

```
git -C E:\jon\mg-<task> status --porcelain
git -C E:\jon\mg-<task> log --oneline origin/main..HEAD
gh api "repos/OrthogonalMaffs/maffsgames/pulls?state=all&head=OrthogonalMaffs:<branch>"
```

Write what these show into the lane handover before doing anything else. Then: if the PR merged, finish with
`end-task.py`; if open and green, resume at merge; if no PR, resume at check-changed and push; if the worktree
is dirty with changes nobody can explain, stop and ask.

**Reverting a merged change:** a new branch from `origin/main`, `git revert <merge-sha>`, a PR, the Gate,
`merge-pr.py`. Never rewrite `main`.

## 8. What changes for Codex (pilot check 3)

Codex's `workspace-write` sandbox limits writes to the folder it starts in. Two consequences, **both untested**:

- **Creating a worktree** writes a sibling folder and the primary's `.git\worktrees\` — both outside a worktree.
- **Committing from a linked worktree** writes objects and refs into the primary's `.git` — outside the worktree.

Options, to choose from the pilot's evidence:

1. Jon (or the implementer's first approved command) creates the worktree; Codex starts **inside** it; commits and
   pushes run with approval (`--ask-for-approval on-request`). Most contained; more prompts.
2. Codex starts in `E:\jon` with `workspace-write`, so every worktree and the primary are inside its workspace.
   Fewer prompts; the sandbox no longer protects other lanes' worktrees — the instructions do.
3. Add the primary's `.git` as an extra writable root, if the installed Codex supports it. To be verified in the
   docs for the installed version before relying on it.

**Not an option:** `danger-full-access` as routine.
