# Contract PHONE-FIT-STATE-SELECTIVE (Project Claude; Jon, 22 Nov 2026, 14:12), verbatim

PHONE-FIT-STATE-SELECTIVE. Cloud lane. Tier: Shared (ci-deps.py and the phone-fit workflow are Gate files): stop at Gate green, report, and wait for Project Claude's review and Jon's "merge" (AGENTS.md:60). From Project Claude; Jon, 22 Nov 2026, 14:12 ("yes please"), from #877's report.
Recommended: Claude Code, Opus, high effort. A change to the one definition of "shared", with the base-to-head diff of a JSON file as its input.

TASK: Make a change to scripts/phone-fit-state.json measure only the games whose entries changed, not every game; carry #877's close-out.

ROOT CAUSE: is_shared() (scripts/ci-deps.py:424-440) counts a path as shared under rule 3 if it is one of the phone-fit checker's own files; scripts/phone-fit-state.json is one (measure-phone-fit.py reads it). So any PR that edits it starts a full measure of every game in all three modes. #877 (GIVEN-THAT-FIT-WHY, c6d51b4) took given-that off the lists, as AGENTS.md requires of the PR that fixes a game. That one edit turned a one-game PR run (about 2 minutes, proven by #876's run 45008584432: 1m38s) into a full run of about 16 minutes. Every game fix that leaves the known-failures lists will do the same. The file is per-game data: every entry under known-failures, sideways and unmeasurable is keyed by mode and then by game slug, so which games a change affects can be read from the diff.

CLASS CHECK: Architectural. The rule sits in the one definition of "shared" and hits every PR that edits the state file, i.e. every phone-fit fix. Fix it there (ci-deps.py, with the workflow passing the base), not by a special case in one PR or by asking contracts to split the state-file edit out.

EXACT CHANGE:
1. First commit: the standing close-out for GIVEN-THAT-FIT-WHY (#877, merged as c6d51b4 via merge-pr.py; main runs check-site 45028817739, Pages 45028817113 and phone-fit-full 45028817763, with its result), per AGENTS.md. Take given-that off cloud.md's claim list and move its contract to docs/history/contracts/. Keep #875's owed live proof (docs-only and /class/ PRs) listed as owed. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-22-phone-fit-state-selective.md.
2. scripts/ci-deps.py:
   a. state_games(base_text, head_text) -> a sorted list of slugs, or None. Parse both versions. The games are the slugs whose entries differ, in any list (known-failures, sideways, unmeasurable), in any mode: added, removed or changed. It returns None ("treat as shared") if either side doesn't parse, or if anything other than per-game entries changed: a mode or list added or removed, the note, the file's shape.
   b. is_shared(): scripts/phone-fit-state.json is no longer shared by rule 3. Shared or not is decided by state_games: None means shared; a list means those games join the measure. Document this in is_shared's docstring next to NOT_CHECKER_DEPS. Nothing else changes in rules 1-3.
   c. measured_pages() (or the workflow's "changed" step, whichever keeps one definition) adds state_games' slugs to the games it returns.
   d. --selftest proofs:
      - #877's real diff of the state file (2107eef -> c6d51b4) gives ["given-that"].
      - A note-only change gives None.
      - A new mode key gives None.
      - Unparseable JSON gives None.
      - A change to two games' entries gives both.
      - A slug that appears in the state file but not in phone_fit_games() is reported, not silently dropped (STOP IF).
3. .github/workflows/phone-fit-full.yml: the "changed" step gives state_games the state file's text at the base (the PR's base, or the push's before-commit) and at the head. Nightly and manual runs unchanged.
4. Prove it before asking for "merge":
   - The selftest, with output in the PR.
   - A local run of the "changed" step's exact Python against #877's full diff (2107eef..c6d51b4: a game page, its verifier, the state file, docs). It should select given-that only and not be shared.
   - This PR's own run is a full measure (it changes Gate files), as expected: say so.
5. Stop at Gate green. Report: the selftest and simulation output, the run IDs, and the full measure's result. Wait for Project Claude's review and Jon's "merge"; then merge via scripts/merge-pr.py and do the standing close-out (cloud.md short). The live proof (the next PR that takes a game off the state file measures that game only) is owed to a later close-out.

DO NOT TOUCH: What phone-fit measures and its pass/fail rules; the contents of scripts/phone-fit-state.json; measure-phone-fit.py's --only and stale rules; rules 1 and 2 of is_shared(); NOT_CHECKER_DEPS's two entries; the Plan job's selection (select()); merge-pr.py; check-site.yml and the Gate's budgets; games/given-that/, scripts/verify-given-that.py, docs/canon.md, docs/snagging-list.md and docs/handover/home.md (the home lane's GIVEN-THAT-VENN-FADE is in flight); every game page.

SUCCESS CONDITION: A PR that changes a game and its entry in the state file measures that game only, in all three modes; a change to the state file's note or shape still measures everything. The selftest passes with #877's real diff giving ["given-that"]. The simulation of #877 selects given-that only. CI is green; Project Claude has reviewed and Jon has said "merge"; the PR is merged; cloud.md records #877's close-out with Given That unclaimed.

STOP IF: The state file has a structure that isn't per-mode, per-list, per-slug: report it, don't guess. A state-file slug isn't in the phone-fit roster (report, don't drop). The workflow can't read the base version of the file on a push or PR run. Selecting by the state file would let a game's entry be removed without that game being measured. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).
