PHONE-SCROLL (Project Claude, 10 Nov 05:55)
LANE: home · TIER: Small · branch from current origin/main. No other lane running (check: no open PR; if one is open, STOP). Stop at a green Gate for Project Claude's review and Jon's "merge"; do not merge. Not a draft. Save this contract verbatim in docs/handover/contracts/ in the first commit. In the same first commit: home.md Queue line DOCS-BUNDLE → "merged as 10d3167"; todo START block's "Order:" line drops LIVE-BUG-RECHECK and BRANCH-CLEANUP (both done) and reads "by priority (canon §0.2)".

TASK: Wide tables and display maths scroll inside their own box on a 320px phone, instead of scrolling the whole page, on the 14 escape-room teacher pages and the parent guides.
ROOT CAUSE: Wide block content (tables, KaTeX display maths) has no horizontal scroll container in either shared stylesheet: escape-rooms/assets/engine.css:165 (table.tt, width:100%, padding that cannot shrink) and parents/guide.css:334 (table, and no .katex-display rule at all).
CLASS CHECK: Yes, a class. The same shape (a wide block with no scroll container) appears in 20 tier1_phone_overflow entries across two page families: 14 teacher pages (todo 1.37), 4 guides' display maths (1.38), and the tables in fractions and standard-form (1.34). The fix goes in the shared layer of each family, never per page.
EXACT CHANGE:
1. escape-rooms/assets/teacher.js (:147, :168, :217): wrap each table.tt in <div class="tt-scroll">; engine.css: .tt-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:10px 0 16px} and table.tt's margin moves to the wrapper.
2. parents/guide.css: .katex-display{overflow-x:auto;overflow-y:hidden;padding-bottom:2px}.
3. parents/guide.js: on load, wrap every <table> in the guide body in <div class="table-scroll">; guide.css: .table-scroll{overflow-x:auto}. No per-page HTML edits.
4. scripts/checker-allowlist.json: remove every tier1_phone_overflow entry that no longer overflows (expected: 14 teacher pages; the 4 guides of 1.38; fractions; standard-form). spec-map, trig-wars and better-value stay.
5. Update todo rows 1.37, 1.38 and 1.34 with the result (the fixing PR updates its rows, AGENTS.md); close 1.37 and 1.38 to todo-done.md if wholly fixed.
6. Proof in the PR body: 320×568 screenshots of one teacher page and indices-surds, each showing the box scrolling and the page not; the list of entries removed.
7. Close-out entry in docs/handover/home.md; release any claim.
DO NOT TOUCH: any game; schools/assets/; room.js, engine.js or any student-facing room page; per-page guide HTML; spec-map; Gate files and workflows; canon; cloud.md; any todo row not named above.
SUCCESS CONDITION: Tier 1 green with the entries removed; no page wider than its viewport at 320×568 among those listed; tables and display maths unchanged at 1366×768 (before/after screenshot of one of each); Gate green; stopped for review.
STOP IF: an overflow is inline maths rather than display maths (report which page and expression); wrapping tables in guide.js changes any table's look at desktop width; a teacher page still overflows from something other than table.tt; the work will not reach a green Gate in time for Jon to say "merge" before he leaves.

PHONE-SCROLL — Amendment 1 (Project Claude, 10 Nov 06:42; replaces the 06:40 draft)
1. standard-form (parents/standard-form/index.html:120 ONLY), two changes on that line and nothing else on the page:
   a. Insert <wbr> after each comma in "5,970,000,000,000,000,000,000,000" so the number can break only at a comma. This is the only grouped-digit run in parents/ (searched); not a class, so no shared rule.
   b. "The Earth weighs about" → "The Earth has a mass of about" (kg is a mass, not a weight; Jon, 10 Nov).
   Remove its tier1_phone_overflow entry if Tier 1 then passes at 320×568; if it still overflows, STOP and report the element.
2. Remove the 2px padding-bottom from .katex-display in parents/guide.css. Confirm no display maths is clipped on every guide that renders display maths (list them), 320×568 and 1366×768.
3. Deviations accepted as reported: table margins on the scroll box; the in-play row outline drawn inside the row; touch scrolling on the guide box.
4. Lane: record in the close-out that this ran in a cloud container on claude/amazing-goldberg-2eiqbm, committed as Claude, as the only running lane.
5. The /updates/ line, if any, covers the standard-form wording change too.
Then: green Gate, stop for Project Claude's review and Jon's "merge". Do not merge.

PHONE-SCROLL — Amendment 2 (Project Claude, 10 Nov 06:50)
Item 2 of Amendment 1 is reversed: .katex-display gets padding: 2px 0 (top and bottom). Re-run the same 94-block comparison (13 guides × 2 widths); success = 0 blocks losing ink against main. Record Amendment 2 in the close-out. Everything else in Amendment 1 stands. Green Gate, then stop for Project Claude's review and Jon's "merge". Do not merge.

PHONE-SCROLL — Amendment 3 (Project Claude, 10 Nov 06:50)
Permitted: scripts/verify-parent-guides.py:621, the locator regex "weighs about" → "has a mass of about", matching Amendment 1's wording. No other change to the verifier; its ARITH check (the Earth's mass equals 5.97 × 10^24) must still run and pass, not be skipped (confirm in the PR body). Run its selftest, push, record Amendment 3 in the close-out, stop at a green Gate for Project Claude's review and Jon's "merge". Do not merge.
