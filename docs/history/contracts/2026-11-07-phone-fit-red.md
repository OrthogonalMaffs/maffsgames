# PHONE-FIT-RED (Jon, 7 Nov 2026), verbatim

PHONE-FIT-RED — main's phone-fit run is red, and nothing measures the whole library (7 Nov 2026)
LANE: home (Claude Code) · TIER: Shared · from current main

COORDINATION: Codex owns tools/pack-generator/, docs/screens/christmas-pack/ and may edit escape-rooms/christmas-tree-fiasco/room.js (CHRISTMAS-PACK, #689). The cloud lane may still be closing #693 (data/games.json, room heads, escape-rooms/assets/engine.js). Touch none of those. Do NOT edit docs/handover/home.md or docs/handover/cloud.md: put the close-out entry in the PR body under "Close-out entry (for home.md)". Save this contract word for word in docs/handover/contracts/ per AGENTS.md.

START: claim possibly-maybe, who-ate-all-the-pies, as-you-can-see, distinctly-average, hc-factor, i-found-a-mark and better-value on scripts/answer-lock-state.json in one commit of its own; remove the claims in the fix PR.

TASK: Make a full phone-fit run on main catch new failures automatically, then diagnose and fix the seven games it shows red that are not on known-failures.

ROOT CAUSE: The Gate measures phone fit only for games a PR changes. A change to shared code, or to the checker, can break games that no PR then touches, and nothing measures them again. #687's full run found main red on: possibly-maybe (normal, aa, laptop); aa: who-ate-all-the-pies, as-you-can-see, distinctly-average, hc-factor, i-found-a-mark; laptop: better-value. None is on known-failures, so every one is unexplained.

CLASS CHECK: Part (b) is a bug class by definition: the absence of a check on shared paths, so the fix is a library-wide run, not per-game. Part (a) is unknown until diagnosed: five games failing in the same mode (aa) suggests one shared cause. So: diagnose all seven first and group them by cause. Fix in this PR only causes local to one game's own file. Any cause shared by two or more games, in a shared asset, or in measure-phone-fit.py itself is architectural: STOP and report it (see STOP IF) for Project Claude's ruling; do not patch it per game.

EXACT CHANGE:
1. New workflow .github/workflows/phone-fit-full.yml: runs scripts/measure-phone-fit.py over every live game in every mode (normal, aa, laptop) (a) nightly on main, (b) on push to main when any path that the Gate's Plan job already treats as shared changes. Read that path list from where Plan defines it; do not write a second list. A failure not on phone-fit-state.json's known-failures fails the run (GitHub's failed-scheduled-run email goes to the repo owner). Upload the full report as an artefact. Report the run's wall-clock time.
2. Run it once on main (workflow_dispatch) before any game change, and paste its result: the list of failing game/mode pairs, which must match the seven above. If it doesn't match, report the difference before going on.
3. Diagnosis table in the PR body, one row per game/mode: measured bottom, fold, viewport, the element that sets the bottom (selector + text), and the cause in one line. Then group the rows by cause.
4. For each cause that is local to one game's own index.html: fix it in that file only, keeping the game's look and maths unchanged; re-measure that game in all three modes.
5. phone-fit-state.json: remove entries that now pass (the lists only shrink). Add nothing to known-failures without Project Claude's written ruling in the PR. who-ate-all-the-pies and i-found-a-mark (Essentials games) may NEVER be added.
6. docs/canon.md §7.6.1: two sentences: the full run exists, when it runs, and that a red full run on main is fixed before new game work.
7. No /updates/ line.

DO NOT TOUCH: SUBMIT_RE, CONTINUE_RE, the fold, settle and classify logic, and the data-mfg-aside rule in measure-phone-fit.py; shared assets (schools/assets/**, any file used by more than one game); the existing Gate jobs and their triggers; any game outside the seven; the seven games' questions, answers, generators, text and art; escape-rooms/; tools/pack-generator/; data/games.json; docs/handover/home.md and cloud.md; the files under COORDINATION.

SUCCESS CONDITION: phone-fit-full.yml runs on main nightly and after shared-path changes and fails on any unlisted failure; its first run's result is in the PR; every one of the seven game/mode failures is either fixed in the game's own file (re-measured green in all three modes) or reported under STOP IF with its diagnosis row; no other game's result changes; pies and i-found-a-mark are not on known-failures. Committed, contract saved, PR open, Gate green, close-out entry in the PR body; stop for Project Claude's review and Jon's "merge".

STOP IF: the first full run's failures differ from the seven listed (report the difference); two or more games share a cause, or a cause is in a shared asset or in measure-phone-fit.py (stop after the diagnosis table; fix only the local causes already found, then report); a fix would change a game's maths, question text or answer controls; the full run takes over 30 minutes (report the time and per-mode split; do not shard or cut modes without a ruling); the Plan job's shared-path list cannot be read from one place (report where it lives).
