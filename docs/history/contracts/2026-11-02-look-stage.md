CONCURRENCY (Jon, 2 Nov 2026): allowed alongside the cloud lane's PIES-LOOK and ESSENTIALS-ART; neither edits the
roster, canon or CI registration. Do not edit any game folder or scripts/answer-lock-state.json.

CONTRACT: LOOK-STAGE
Tier: Shared · Lane: home · Implementer: Codex (WSL)

ENVIRONMENT
WSL distro "maffs"; primary ~/maffsgames; venv ~/.venvs/maffs; no sandbox; never sudo.
git -C ~/maffsgames fetch origin && git -C ~/maffsgames worktree add -b codex/look-stage ~/mg-look-stage origin/main

TASK
No game is listed until Jon has signed off its look: record the sign-off in the roster and make CI refuse a listed
game without one.

ROOT CAUSE
Six games were built from one shared template on 27 Oct 2026 (lane plan). Who Ate All the Pies? was listed on
30 Oct with the template's placeholder look (an SVG plank and two circles), because the pipeline gates listing on
correctness and play-testing, never on look. As You Can See, Possibly, Maybe, It's on Sale!, Y So Steep? and
The HC Factor are unlisted with the same template look; nothing stops the same thing happening to each.

CLASS CHECK
Yes: a pipeline gap, not one game. Fix at the shared layer: the roster records the sign-off, and one CI check
enforces it for every listed game. Per-game reminders would be the wrong fix.

EXACT CHANGE
1. Roster (.claude/rules/game-roster.md): a documented way to record "Look signed off by Jon, <date>" per game,
   in the roster's existing style (choose the least disruptive form; describe it at the top of the roster).
2. A CI check (new scripts/check-look-signoff.py, or an extension of an existing roster check if one fits better):
   every game in a listed section has a look sign-off. Per canon §7.8.4, warn first: seed a shrink-only warn list
   with every listed game that lacks one today. All games listed before 2 Nov 2026 are signed off retrospectively
   as "pre-2 Nov, grandfathered" (Jon approved by commissioning this check), except who-ate-all-the-pies, which goes
   on the warn list until Jon signs off its new look (PIES-LOOK). A new listing without a sign-off fails.
3. canon: one rule line in the pipeline section ("A game is listed only after Jon signs off its look; the roster
   records it; check-look-signoff.py enforces it"), reason in §12. Game illustrations follow §11.6 and live in
   games/<slug>/assets/ (one line, same place).
4. --selftest with planted faults: a listed game without sign-off fails; a warn-listed one warns; adding to the
   warn list fails.

DO NOT TOUCH
- Any game's files; the listing state of any game; games.json, homepage, Essentials.
- Gate files (workflow, scripts/ci-*, ci_shards.py, merge-pr.py, check-context-size.py, check-changed.py) beyond
  the new check's own ci-line header.
- AGENTS.md, CLAUDE.md, docs/rules/ (just rewritten by RULEBOOK).

SUCCESS CONDITION
Check in CI, warning first per §7.8.4; selftest proves all three plants; canon rule and §12 reason added;
check-changed.py green; Shared-tier review by Project Claude before merge; stop at Gate green for Jon's "merge".
Handover entry in the new "## <date> (home): LOOK-STAGE" form, ending with its Record line.

STOP IF
- The roster format cannot carry the sign-off without changing what other checks parse (report the options).
- Grandfathering any listed game is ambiguous (list them for Jon).
- Registering the check needs a change to a Gate file.
