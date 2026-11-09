HEADER-FIT (Project Claude, 9 Nov 10:45)
LANE: cloud (Claude Code web) · TIER: Small · CONTRACT: HEADER-FIT (docs/todo.md §1.39) · branch from origin/main 0e27f06 or later. No other lane is running. Stop at a green Gate for Project Claude's review and Jon's "merge"; do not merge. Not a draft. Save this contract verbatim in docs/handover/contracts/ in the first commit.
FIRST COMMIT ALSO (#716 leftovers): git mv docs/handover/contracts/2026-11-09-screening-room-fit.md to docs/history/contracts/; cloud.md's SCREENING-ROOM-FIT entry → "merged as 0e27f06 (main run 42597611148 green)".
CONTRACT EXCEPTIONS (explicit): (1) docs/rules/games.md says cloud fixes one game per PR and claims one game at a time: this PR fixes three small games, so claim all three in one commit first and release them in the PR (one lane runs, so no claim can clash). (2) As in #714–#716, this PR updates its todo row. Edit no rule file.

TASK: Stop the header overflowing sideways on a phone in equation-builder, probability-pioneer and shape-shifter, and close §1.39.
ROOT CAUSE: After the start screen, each game's header holds more than fits at 320 px (div.header-right 329, 355, 375 px wide in the nightly run). The .header-right rule is identical in 24 games and 21 fit, so the rule is not the fault; the contents are: equation-builder carries two "Aa" buttons (a11yToggle and a11yBtn, index.html:185, :187); probability-pioneer and shape-shifter carry the Aa button, a pill and a score next to the title.
CLASS CHECK: Not a class: the shared rule is innocent (21 of 24 fit) and each overflow comes from that game's own header contents. Fix per game, in one PR.
EXACT CHANGE:
1. equation-builder: if one of the two Aa buttons is a dead duplicate (not the one the shared a11y code wires), remove it; report which and why. If both are wired, STOP.
2. All three: at narrow widths, make the header fit at 320 px by the smallest change: let the title shrink with an ellipsis (min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap) and, if still needed, slightly smaller pill/score text. Keep the title and the Aa toggle on one line (canon §7.6.1); no tap target under 44 px; nothing removed except a dead duplicate.
3. Measure with scripts/measure-phone-fit.py for these three games, normal and Aa modes: no sideways scroll at 320×568, 375×667, 390×844 after start; no other size or mode worse. Remove known-failures entries only where the checker reports them stale.
4. docs/todo.md §1.39: append the dated outcome; move the row word for word to docs/history/todo-done.md under "Closed by fix PRs (Nov 2026)" (the other seven games were already fixed by #256).
5. /updates/: one dated line in plain words for Jon to confirm, e.g. "Equation Builder, Probability Pioneer and Shape Shifter: the top bar now fits on small phones."
6. Release the claims; close-out entry in docs/handover/cloud.md.
DO NOT TOUCH: the other 21 games that carry .header-right; schools/assets/; questions, marking, wording; Gate files; scripts/measure-phone-fit.py; canon; AGENTS.md and docs/rules/; any other todo row; home.md.
SUCCESS CONDITION: no sideways scroll in the three games at the three phone sizes in normal and Aa; nothing else worse; §1.39 closed; /updates/ line drafted; claims released; Gate green; stopped for review.
STOP IF: both Aa buttons in equation-builder are wired; the fit needs removing a working control or shrinking a tap target under 44 px; another game's measurement changes; another lane or claim holds any of the three.

HEADER-FIT — Amendment 1 (Project Claude, 9 Nov 11:36). LANE: cloud. Same branch, PR #717, claims held. Jon, 11:34: yes to both.
1. equation-builder: one Aa button, the platform-standard a11yToggle (mfg_accessible). Move anything the game's own "dyslexia" class does that the standard accessible mode does not onto the accessible mode, then remove a11yBtn, its CSS and its mfg_dyslexia handler. Report what moved (or "nothing: accessible already covers it").
2. All three games: on small phones (the widths where the title would otherwise truncate; at least ≤ 360 px), the back link shows "←" only, as Expected Damage does, with aria-label "Back to Games" kept and its tap target ≥ 44 px. The title then shows in full at 320 px in normal and Aa modes; report its width. Ellipsis stays only as a last resort, never down to one letter.
3. Re-measure as before (normal and Aa, three phone sizes): no sideways scroll, nothing worse. Update the PR body's proofs and the /updates/ line if it changes.
STOP IF: the dyslexia styling cannot move onto the standard mode without changing other games or schools/assets/ (report it); the title still truncates at 320 px with the arrow-only link.
Nothing else changes.
