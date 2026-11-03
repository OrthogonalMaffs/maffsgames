# CLOUD-LEAN (received 3 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER). Jon's covering note came with it in the same message.

## Covering note (Jon, 3 Nov 2026, verbatim)

Stop. Do not run check-changed.py: Jon ruled on 2 Nov that the cloud lane does not run it (CLOUD-LEAN writes
that into the rulebook). Commit under this container's identity: cloud PRs always have, and the squash merge lands
on main as Vector52F. Do not push the RULE-QUOTE entry on its own. Keep it uncommitted until the contract below
says to commit it. Then work to this contract.

## Contract (verbatim)

CONTRACT: CLOUD-LEAN (amended 3 Nov 2026)
Tier: Shared · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Write the cloud lane's rules into the rulebook (no local suite, what "a fresh context" means, the cloud commit
identity), and give every lane a one-line, script-produced report of main's run after a merge.

ROOT CAUSE
1. "Run check-changed.py before pushing" was set for the home machine (canon §7.8, 4 Oct 2026). In the cloud
   container it takes about 70 minutes (two hours and unfinished when all 229 checks are selected, 2 Nov) and always
   reports the same 25 known failures (KaTeX CDN, WebKit) before CI runs the same checks without them. CI minutes
   are free. Jon ruled it out for the cloud lane on 2 Nov; the rulebook does not say so.
2. A /clear inside a cloud session keeps that session's original clone: on 3 Nov a /clear'd session reloaded
   Sunday 1 Nov's pre-RULEBOOK rules (checkout 0925c2fb) and failed the load test; a new session passed it.
3. AGENTS.md's identity check (Vector52F) sits in the WSL start-up rules but is read by cloud sessions, which commit
   as Claude <noreply@anthropic.com>; the squash merge lands as Vector52F.
4. After a merge nothing scripted watches main's run: each agent polls GitHub and reads job results itself.

CLASS CHECK
Yes, all shared: (1)-(3) rules every cloud task follows; (4) every merge in every lane. Fix (1)-(3) in the rulebook,
per lane; fix (4) in merge-pr.py, which already has the run-and-job reader (do not write a second copy).

EXACT CHANGE
0. First commit: the RULE-QUOTE entry already in your working tree (load test passed, 3 Nov), after the old
   session's open handover PR has merged and you have pulled main.
1. Rulebook (AGENTS.md, one line each, 300-byte entry rule; reasons to canon §12):
   a. The cloud lane does not run check-changed.py before pushing. Before the first push it runs only the
      worst-case test where canon §7.8.4 requires it by hand, and the selftest of any script it changed; the PR's
      Gate is the check. The home lane keeps check-changed.py.
   b. "A fresh context is a new cloud session, never /clear: /clear keeps the session's original clone, so it
      reloads the rules of the day it started."
   c. The identity check is WSL-only; the cloud lane commits as Claude <noreply@anthropic.com>.
   docs/handover/cloud.md: replace the container-setup note's check-changed run with rule (a).
2. scripts/merge-pr.py:
   a. New mode --watch-main [<sha>] (default origin/main's head after fetch): waits up to --wait seconds for
      main's check-site run for that commit to finish, using the existing reader and definitions of finished and
      green; prints ONE line and exits 0 (green) or 1 (red, unfinished, or no run):
      "main <sha7> run <id>: GREEN" | "main <sha7> run <id>: RED: <failed job names>" |
      "main <sha7>: NOT FINISHED after <n>s" | "main <sha7>: NO RUN FOUND".
   b. A successful merge given --watch runs the same watch on the squash commit.
   c. --selftest: fixtures for all four outcomes; a planted fault reporting green while a job still runs is CAUGHT.
3. Rulebook: the after-merge rule becomes "merge with python scripts/merge-pr.py <n> --watch --wait 3600 and
   report its last line". One line.
4. docs/handover/cloud.md: correct PIES-EXIT's state line to "MERGED #642 (2a635bd); main green (41615387944,
   84/84)" and move its contract to docs/history/contracts/.

DO NOT TOUCH
merge-pr.py's merge guard (a) and (b), --override and their selftest cases (the watch is additive); the Gate, the
workflow, check-changed.py's selection logic, every check; the home lane's before-pushing rule; review tiers and
Jon's "merge" authority; AGENTS.md rules other than those named.

SUCCESS CONDITION
Rules (a)-(c) and the after-merge rule in AGENTS.md, reasons in canon §12; --watch-main and --watch work, selftest
proves all four outcomes and the plant is CAUGHT; worst-case test passes in CI (merge-pr.py is a Gate file); Gate
green; Shared review by Project Claude; stop for Jon's "merge"; handover ends with its Record line.

STOP IF
The old session's handover PR is not merged when you are ready for the first push (wait, then report); the watch
cannot reuse merge-pr.py's reader without changing guard behaviour; any Gate or workflow file other than
merge-pr.py needs changing; a rulebook line cannot fit the 300-byte entry rule.

## Amendment 1 (Jon, 3 Nov 2026, chat, verbatim)

Option 1, please: commit RULE-QUOTE, then the CLOUD-LEAN work, and push now. STOP IF 1 referred to the old
session's note from this morning, not #636.
#636 (2 Nov, GATE-RESUME/GATE-FIX handover) is stale and conflicts with main. In your handover commit, carry over
what main still lacks from it (GATE-FIX done, #634; GATE-RESUME steps 1-3 done; its contracts moved to
docs/history/), word for word where it still holds, then close #636 unmerged with a comment naming your PR.
The old session's 3 Nov note (0909d491) is superseded by your RULE-QUOTE entry: do not wait for it.
