CONTRACT: PIES-SIGNOFF-AND-PRIMARY-FF
Tier: Small · Lane: home · Implementer: Codex (WSL)

START
git -C ~/maffsgames pull --ff-only, then: git -C ~/maffsgames worktree add -b codex/pies-signoff ~/mg-pies-signoff origin/main

TASK
Record Jon's look sign-off for Who Ate All the Pies?, and make the primary checkout fast-forward before every agent
session so agents never load a stale rulebook.

ROOT CAUSE
1. LOOK-STAGE (#638) left who-ate-all-the-pies on scripts/look-signoff-warn.json until Jon signed off its new look;
   Jon played it after PIES-LOOK (#637) and FRACTION-STACK (#640) and approved it on 3 Nov 2026.
2. Agents load AGENTS.md from the primary checkout's working tree. The rule "never pull or merge into the primary
   checkout" froze it at its clone date, so Codex loaded Saturday's rules on 1 and 2 Nov (two stops on a retired
   lane-notes file). The cloud lane hit the same class on 3 Nov (a /clear'd session on its original clone; CLOUD-LEAN).

CLASS CHECK
(1) Local: one roster line. (2) Shared: every session starts from the primary; fix the rule itself.

EXACT CHANGE
1. .claude/rules/game-roster.md: append "Look signed off by Jon, 2026-11-03." to who-ate-all-the-pies' Description, in
   the roster's documented form; remove who-ate-all-the-pies from scripts/look-signoff-warn.json (leaving it empty).
2. AGENTS.md: replace the rule forbidding pulls into the primary with: "The primary checkout is never edited; before
   starting an agent session, fast-forward it: git -C ~/maffsgames pull --ff-only (stop if it is not a fast-forward)."
   Within the 300-byte entry rule; reason to canon §12. Add the same command as the first line of the start-up steps.

DO NOT TOUCH
Any game file; other roster rows; scripts/check-look-signoff.py; other AGENTS.md rules (including CLOUD-LEAN's lines).

SUCCESS CONDITION
check-look-signoff.py passes with an empty warn list; AGENTS.md carries the fast-forward rule; check-changed.py green;
merge on green (Small) with merge-pr.py <n> --watch --wait 3600, reporting its last line; handover entry with its
Record line.

STOP IF
The roster's documented form differs from the text above; the warn list holds any other game.

## Recovery ruling (Jon, 3 Nov)

Recovery, then carry on (Jon, 3 Nov). Move the roster edit from the primary to the task worktree, in this order:
1. git -C ~/maffsgames diff -- .claude/rules/game-roster.md > /tmp/pies-roster.patch
   (check it holds only the Pies sign-off line)
2. git -C ~/mg-pies-signoff apply /tmp/pies-roster.patch
   and confirm check-look-signoff.py passes in the worktree.
3. Only then: git -C ~/maffsgames checkout -- .claude/rules/game-roster.md
   and confirm git -C ~/maffsgames status --porcelain is empty.
Report each step's result. If step 1 shows anything other than the sign-off, or step 2 does not apply cleanly, stop.
Then continue the contract from where you stopped (check-changed.py, PR, merge on green), and record this slip in the
handover entry in one line.
