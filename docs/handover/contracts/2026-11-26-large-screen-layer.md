LARGE-SCREEN-LAYER (Project Claude, Thu 26 Nov 2026 14:20; checked against main 6d8b633)
Jon, 26 Nov 2026, 13:44 (Base 60 at a 1905x910 browser, screenshot): "really cramped up to the top." 13:50: "please build the contract for the screen fix, it can go to the lane which becomes free first." Earlier: SR-34's goal, "every game fills a large screen" (Jon, 20 Nov 2026); the CSS-zoom pilot parked 20 Nov 21:34: "can wait a bit, but it is definitely something we need to fix".
RECOMMENDED: Claude Code, Opus 5.5, effort high. Shared infrastructure every game will load; the design must hold for 117 pages.
LANE: cloud, lane 2. SEND: now (DAILY-POLISH merged as 3172ba9). This replaces PINNED-LIVE-DATA as lane 2's next task (Jon, 13:50: the screen fix goes to the first free lane); PINNED-LIVE-DATA waits for a later contract.
CLOSE-OUT (first commit, AGENTS.md:62): DAILY-POLISH, #924 merged as 3172ba9; main's runs check-site 45833870462 success, pages 45833868679 success, phone-fit-full 45833870257: read its result from GitHub before recording it (it was still running at the merge report); if it is not success, stop and report before anything else. Contract to docs/history/contracts/. Jon accepted the ?t= query string and no /updates/ line (recorded as his ruling only if he has given it; otherwise note both as open for Jon).
TIER: Shared (stop at green for Project Claude's review and Jon's "merge").

TASK: Build the shared large-screen layer so that a game fills a large screen, scaled up as far as it can be without any of its own layout rules, folds or pointer input going wrong, and pilot it on seven games.

ROOT CAUSE: Shown. Most games lay out in a 680-900 px column at the top of the page (Base 60: .container max-width 720px, widened to at most 900px at 1024px or wider, games/its-just-base-60-bruv/index.html:35 and :130-133), so on a 1920-wide screen two thirds is empty and the text is small. The parked pilot (branch claude/youthful-fermi-ujam6l @ 63b758c: schools/assets/large-screen.css with fixed CSS-zoom steps 1.15/1.25/1.4/1.6, scripts/apply-large-screen.py, scripts/check-large-screen.py, and the STOP findings in that branch's docs/handover/cloud.md) stopped on two failures of one kind:
(1) Under CSS zoom, media queries read the real viewport while the page is laid out in zoomed px. A page's own breakpoints then fire on the wrong side: surd-simplifier's working card opens by (min-width:760px) and (min-height:860px) on a real 955 px viewport while zoom 1.25 leaves 764, so Next fell 12-60 px under the fold on 25 of 100 items. On main 6d8b633, 45 game pages carry height media queries (mostly max-height 580-800, a few min-height 860-960), and width breakpoints (e.g. Base 60's min-width:1024px) have the same exposure.
(2) A fixed zoom ignores how tall a game's tallest screen is: core-maths-paper1's chart questions need about 1,050 px; zoom left 764, so Next fell below the fold.
(3) Separately, negative-number-line's touch drag sets style.left/top from clientX/clientY (:764-765), read in zoomed px: the ghost tile drew 233-746 px from the finger. 13 game pages use clientX.
scroll.js:42 (fold from innerHeight against getBoundingClientRect) was measured consistent under zoom in the pilot: both visual px.

CLASS CHECK: A class, in shared infrastructure: every game that will load the layer is exposed to (1), (2) and (3) in the same way. So the fix is in the layer's rule for choosing the zoom, never in any game's CSS or a per-game hand-set cap. The layer chooses each page's zoom at run time from facts it can read or that are measured and checked, so a page's own layout rules always agree with what it is drawn at.

EXACT CHANGE:
0. First commit: the close-out above. Save this contract verbatim as docs/handover/contracts/2026-11-26-large-screen-layer.md. Start from main, not the pilot branch; reuse the pilot's apply and check scripts and measurements where they fit (cherry-pick or copy, your choice, named in the report). Leave the pilot branch as it is.
1. schools/assets/large-screen.js (and large-screen.css if needed), loaded once by each migrated page, sets the page's zoom on <html> on load and on resize, to the largest value z, rounded down to a step of 0.05, that meets every rule below; z below 1.1 means no zoom (z = 1):
   a. Only on big screens: no zoom when the viewport is under 1500 px wide (a 1366x768 laptop and every phone and tablet unchanged).
   b. Effective width: viewport width / z >= 1200.
   c. Never across the page's own breakpoints: for every min-width, max-width, min-height and max-height threshold T in the page's same-origin stylesheets (its <style> and linked site CSS, read through the CSSOM at run time; cross-origin sheets such as KaTeX and Google Fonts skipped), the effective size (viewport / z) is on the same side of T as the real viewport. So every media query gives the same answer as it would unzoomed at that effective size. This is what fixes (1) for every page at once.
   d. Height budget: viewport height / z >= the page's measured need (rule 3), so every screen's answer controls and Next stay above the fold. This fixes (2).
   e. Pointer safety: a page that positions elements from clientX/clientY (or pageX/pageY) gets z = 1 unless it is on the check's POINTER_VERIFIED list after a measured drag test under zoom. This guards (3) without patching any game; the pages left at 1 are listed in the report with a todo row (LARGE-SCREEN-POINTER) for a shared drag helper later.
   f. Upper limit 1.6. vh correction as the pilot found: the body's min-height divided back by z, so 100vh still ends at the bottom of the screen.
   An opt-out stays: <html data-large-screen="off">, only with a reason in the check's OPT_OUT list.
2. data/large-screen.json: per migrated page, its measured height need in CSS px (the tallest bottom edge of the answer controls and of Next after a wrong answer, over every screen the measurement reaches, at effective width 1200 so it is the most conservative) and how it was measured. Written by a script (scripts/measure-large-screen.py, or a mode of measure-phone-fit.py, your choice), never by hand.
3. scripts/check-large-screen.py in CI: every MIGRATED page loads the layer exactly once; every MIGRATED page has a current entry in data/large-screen.json; no unlisted opt-out; and a browser check at viewports 1920x955 and 2560x1310 (real 1080p and 1440p browser viewports) plus 1366x650 and 390x844 (both must stay at z = 1), on the start, question, wrong-answer and results screens: answer controls and Next above the fold, no sideways scroll, z as rule 1 gives it. Plants (each must FAIL): a page whose zoom would cross one of its own height breakpoints (rule c removed); a page whose zoom ignores its height need (rule d removed); a clientX page zoomed without being on POINTER_VERIFIED; a MIGRATED page without the layer.
4. Pilot: link the layer on seven games: the pilot's six (maffscards, factor-race, surd-simplifier, negative-number-line, bearing-blitz, core-maths-paper1) and its-just-base-60-bruv (Jon's case). For each, record in the PR the zoom at 1920x955 and 2560x1310, which rule limited it, and one screenshot per screen at 1920x955 and 1366x650. Expected, to confirm or explain: surd-simplifier limited by its 860 px breakpoint, core-maths-paper1 by its height need, negative-number-line at 1 by the pointer rule unless its drag test passes, Base 60 visibly larger at 1920x955.
5. docs/todo.md: LARGE-SCREEN-LAYER row updated to the merged layer and the pilot's results; new rows LARGE-SCREEN-ROLLOUT (the other 110 games, owner Project Claude after Jon has seen the pilot) and LARGE-SCREEN-POINTER (the pages held at 1 by rule e). docs/handover/cloud.md entry. No canon change and no /updates/ line in this PR (both come with the rollout).

DO NOT TOUCH:
- Any game's own CSS, layout, breakpoints or script (the pilot pages get only the layer's link or script tag).
- The other 110 games; scroll.js, fold.css, fold.js, theme.css, site-footer.css, site-nav.js, calculator.css (read them; a change to any of them is a STOP).
- phone-fit's own sizes, lists and gates (scripts/phone-fit-state.json); scripts/merge-pr.py; every workflow other than adding the new check to check-site's plan the way the repo adds checks (ci-line / ci-deps).
- The pilot branch claude/youthful-fermi-ujam6l.

SUCCESS CONDITION:
- On the seven pilot pages: zoom 1 at 1366x650, 390x844 and every phone; at 1920x955 and 2560x1310 each zooms to the largest value rules a-f allow, and on every measured screen the answer controls and Next are above the fold, nothing scrolls sideways, and no media query in the page gives a different answer from the unzoomed page at the effective size.
- Base 60 at a 1920x955 viewport visibly fills more of the screen (its zoom and screenshot in the PR).
- check-large-screen.py and its four plants run in CI; data/large-screen.json written by the measuring script.
- At green: stop and report to Project Claude for review; merge only on Jon's "merge", through merge-pr.py; main green after; cloud.md records it.

STOP IF:
- DAILY-POLISH's phone-fit-full run on 3172ba9 is not success.
- Rule c or d holds a pilot page at zoom 1 at 1920x955 for a reason other than its own measured breakpoints, height need or pointer use: report the page and the reason.
- Reading thresholds through the CSSOM cannot see a stylesheet that holds a page's breakpoints (for example a same-origin sheet the browser blocks): report which, before working around it.
- Zoom behaves differently in WebKit or Firefox (Playwright's engines) in a way that breaks a rule above: report the engine, page and measurement; Chromium results alone are not enough to merge.
- Any change to a shared file in DO NOT TOUCH turns out to be needed.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
