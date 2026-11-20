=== PART 1 OF 2 ===
LARGE-SCREEN-PILOT, part 1 of 2. Wait for part 2 before starting.
LANE: cloud. Send now. TIER: Medium. MODEL: Claude Code, Opus, medium effort.

TASK: A shared large-screen layer so games fill big screens uniformly: piloted on six games, with a canon rule and a CI check (Jon, 20 Nov 2026).

ROOT CAUSE: On main 2e7c9d2: 76 of 115 games cap their page at 680-760 px (e.g. games/maffscards/index.html:31, card 420 px at :75) and only 17 have any min-width rule, so on a desktop most of the screen is empty. 77% of sessions 20 Sep-19 Nov were desktop. No shared stylesheet reaches every game except site-footer.css (theme.css is on 28).

CLASS CHECK: A bug class: the same shape in 76+ games, and the fix belongs in shared infrastructure. One stylesheet loaded by every game, applied by script and enforced by a check (the site-footer pattern: scripts/apply-footer.py, scripts/check-footer.py). This contract builds the layer and pilots it; rollout to the rest is a later contract after Jon has seen the pilot.

EXACT CHANGE:
1. First commit: (a) close out FORGE-SUBJECT-PROMPT (#854, merge bf019be; main's runs check-site 44807672164, phone-fit-full 44807672235, pages 44807671441 into its cloud.md entry; contract to docs/history/contracts/; its docs/todo.md row moved word for word to docs/history/todo-done.md under TODO-TRIM). (b) docs/handover/cloud.md:5-8, the "Cloud lane owns" paragraph, replaced by exactly: "**Cloud lane scope (Jon, 20 Nov 2026):** the cloud lane edits what its contract names. Without a contract naming them, it never edits `schools/assets/`, the shared modules in `scripts/`, the workflow, canon, the roster's listed section or `docs/todo.md`. AGENTS.md's TODO-TRIM rule applies to every cloud PR." (c) Save this contract (both parts) verbatim as docs/handover/contracts/2026-11-20-large-screen-pilot.md.
2. schools/assets/large-screen.css: scales the whole page with CSS zoom on large viewports only, in steps. Starting values: (min-width:1500px) and (min-height:880px) zoom 1.25; (min-width:2200px) and (min-height:1200px) zoom 1.6. The rule: no zoom below 1500x880, so a 1366x768 screen and every phone are unchanged; after zoom the effective viewport is never smaller than 1200x760 CSS px. Tune the steps to that rule and report the final values. A game opts out with <html data-large-screen="off">.
3. scripts/apply-large-screen.py links it once before </head>; scripts/check-large-screen.py in CI: every page on its MIGRATED list links it exactly once, and no page carries data-large-screen="off" without an entry and reason in the check's OPT_OUT list. MIGRATED for this PR: maffscards, factor-race, surd-simplifier, negative-number-line, bearing-blitz, core-maths-paper1. Plants that must FAIL: a MIGRATED page without the link; an unlisted opt-out.
=== PART 2 OF 2 ===
LARGE-SCREEN-PILOT, part 2 of 2. EXACT CHANGE continued.
4. Pilot: link the six. For each, at viewports 1366x650, 1920x955 and 2560x1310 (real browser viewports of 1366x768, 1080p and 1440p screens), screenshot start, question, wrong answer and results; record whether the answer controls and Next are above the fold, nothing scrolls sideways, and clicks, drags and canvas drawing land where the pointer is (negative-number-line drags, bearing-blitz canvas). A pilot game whose pointer, drag or canvas input lands in the wrong place under zoom goes on OPT_OUT with that reason (don't patch the game); report it. One screenshot grid per game in the PR.
5. docs/canon.md: new §7.5.8 "Large screens" (the layer, the steps, the opt-out) and SR-34: "Every game fills a large screen. Pages scale up uniformly on large viewports through schools/assets/large-screen.css; a game may opt out only with a recorded reason, and must then lay itself out for large screens on its own." (Jon, 20 Nov 2026).
6. docs/todo.md, two rows. LARGE-SCREEN-ROLLOUT: the other 109 games; the 26 pointer, drag or canvas games each checked, or opted out with a reason and a todo row; owner Project Claude (after Jon sees the pilot). START-SIDEWAYS-GATE: start screens stay report-only for the fold, but sideways scroll on a start screen becomes a gate in every mode (Jon, 20 Nov 2026), with a survey first and today's offenders on a known list, each with a row; known case: formula-forge in Aa is 490 px wide at every phone size, its stage-preview grid overflowing; owner Project Claude.
7. cloud.md entry. No /updates/ line.
8. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line.

DO NOT TOUCH: any game's own CSS or layout (the pilot adds only the link); the other 109 games; phone breakpoints and the fold components; theme.css and site-footer.css.

SUCCESS CONDITION: every pilot game not opted out scales up on 1080p and 1440p viewports, is unchanged at 1366x650 and on phones, and takes pointer input correctly; check-large-screen.py in CI with both plants failing; canon §7.5.8 and SR-34 in; LARGE-SCREEN-ROLLOUT row added; FORGE-SUBJECT-PROMPT closed out and its todo row moved; the cloud.md scope paragraph replaced; START-SIDEWAYS-GATE row added; merged GREEN; cloud.md records it.

STOP IF: more than two pilot games need opting out (the approach is wrong; report before going further); zoom pushes Next or the answer controls below the fold at any pilot viewport; a shared check (phone-fit, theme, footer) fails because of the new link; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
