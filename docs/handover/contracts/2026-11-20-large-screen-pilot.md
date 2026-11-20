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

=== AMENDMENT 1 (Project Claude, 20 Nov 2026; Jon's ruling 21:34) ===
LARGE-SCREEN-PILOT — follow-up from Project Claude. Jon's ruling, 20 Nov 21:34: option 2, PARK.
None of (a), (b) or (c).
Recommended: Claude Code, low effort. Docs-only cherry-pick and backlog rows.

Thank you for stopping cleanly at STOP IF. Your measurements are what showed the real cause.

TASK: Land only the FORGE-SUBJECT-PROMPT close-out commit (4e90390) on main. Park the large-screen layer on its branch, and record the finding and the required fix as a todo row.

ROOT CAUSE: Under CSS zoom, media queries and window.innerHeight read the real viewport, but layout is drawn in zoomed px. The site's fold handling assumes those are one unit:
- fold.css:26-31 gives each game its own viewport-height media query for the working card; about 41 game pages carry height queries.
- scroll.js:42 computes the fold from innerHeight against getBoundingClientRect.
- Drag code positions things from clientX (negative-number-line Order Them; 13 game pages use clientX).
surd-simplifier and the drag offset are instances of this, not exceptions.

CLASS CHECK: A bug class. It is shared infrastructure (the zoom layer breaks an invariant fold.css, scroll.js and per-game fold queries rely on), and it appears in two or more components. So per-game zoom caps (option b) are the call-site patch shape and are rejected. The fix belongs in the layer (fold decisions read the effective height) and is a separate, larger piece of work. Jon: it "can wait a bit, but it is definitely something we need to fix". Nothing in this follow-up fixes it; this only parks the work and records it.

EXACT CHANGE:
1. Make a new branch from current origin/main. Cherry-pick 4e90390 only: the #854 close-out, the moved todo row, the cloud.md:5-8 scope paragraph replaced with Jon's text, and the saved contract.
2. In the same PR, add to docs/todo.md (format and entry sizes per AGENTS.md):
   - LARGE-SCREEN-LAYER. Large screens (SR-34 goal; not yet in canon). The CSS-zoom pilot is parked at claude/youthful-fermi-ujam6l @ 63b758c (large-screen.css, apply/check scripts, tuned steps 1.15/1.25/1.4/1.6, the vh divide-back). Root cause and class: as above. Required fix: make the site's fold decisions read the effective (zoomed) height at the shared layer, e.g. container queries on a full-height root in place of per-game viewport-height media queries, and scroll.js and drag code in the same unit. Then re-pilot the same six games. Not per-game zoom caps. Covers MaffsCards list item (1), large screens.
   - START-SIDEWAYS-GATE. Jon's ruling (b) from the pilot contract, unchanged: sideways scroll on start screens becomes a CI gate; fold stays report-only; known case formula-forge Aa at 490 px. Independent of zoom.
   - PERCENTILE-LOWER-IS-BETTER. calculatePercentile (schools/assets/firebase-leaderboard.js:531) ignores LOWER_IS_BETTER. Latent: no page displays a percentile or tier. Fix before any page does.
3. Carry the measured STOP findings (your results table and the step-tuning figures) from 63b758c's docs/handover/cloud.md into main's cloud.md, within AGENTS.md entry sizes, so they survive the branch. The LARGE-SCREEN-LAYER row points to them.
4. Merge on green via scripts/merge-pr.py, then the standing close-out.

DO NOT TOUCH: Don't merge, rebase or delete claude/youthful-fermi-ujam6l. Leave 9413388 and 63b758c on it; don't bring them to main. No game page, no schools/assets file, no scripts/ file, no CI wiring. Don't write canon §7.5.8 or SR-34. No LARGE-SCREEN-ROLLOUT row; LARGE-SCREEN-LAYER replaces it.

SUCCESS CONDITION: main has 4e90390's changes, the three new todo rows and the carried findings. main has no large-screen.css, apply/check script or game-page link. The pilot branch still exists at 63b758c. CI is green, the PR is merged, and cloud.md shows the pilot parked, with the branch and SHA, the reason, and Jon's ruling.

STOP IF: The cherry-pick conflicts outside docs/. A CI failure is caused by anything other than these docs changes. Any todo row would break AGENTS.md entry-size rules in a way you can't fix by shortening the row.
