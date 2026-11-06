# WHOSE-SIDE-FIT (Jon, via Project Claude, 6 Nov 2026), verbatim

Queued on 6 Nov 2026 by the WHOSE-SIDE-ART session (PR #684) for a fresh cloud session. The contract carried no name; WHOSE-SIDE-BIOS's DO NOT TOUCH calls it "the triangle fit (WHOSE-SIDE-FIT)", so the cloud lane uses that name. Start it only after WHOSE-SIDE-ART (#684) merges, from current main. It names the bios contract WHOSE-SIDE-INTRO (queued as WHOSE-SIDE-BIOS, `2026-11-06-whose-side-bios.md`).

LANE: cloud (fresh session) · TIER: Shared · after WHOSE-SIDE-ART (#684) merges, from current main

COORDINATION: the home lane may have codex/escape-herrings open (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. Record in docs/handover/cloud.md.

TASK: On large screens in "Whose Side Are You On?", make the triangle fill its figure box and stop the question text running under the answer buttons; make the verifier measure both for real.

ROOT CAUSE: Three faults, all from the large-screen layout in #682.
(1) drawFigure() reserves a worst-case margin on all four sides: mx = 2*hw + 10g and my = 2*hh + 10g, where hw is the widest label's half-width and g reaches 2 on large screens. That is about 120 px each side at 1920x1080 whether a label sits there or not, and the triangle is then centred, not the drawing. A long thin triangle (7-24-25, 12-35-37) is width-limited, so the lost width also costs height. Jon's screenshot at about 1890 wide: triangle about 520x155 in a left column of about 800x825.
(2) check_big() in scripts/verify-whose-side-are-you-on.py checks the SVG box height (svgH >= 0.5h). The box always passes, so a small triangle inside it is never caught (its own docstring says so).
(3) In the >=1024px media query, .qcard has grid-template-rows: 1fr auto auto auto auto 1fr, a fixed height (set by bigSize()), and the figure spanning every row. 1fr means minmax(auto, 1fr); with the spanning figure, the row holding #ask is sized to one line (its min-height, 1.4em) however many lines the question wraps to, and the rest overflows under #opts. Reproduced on main, Stage 4 ("You know one side and want the ? side. Which function?"): 1222x688 ask box 29 px, text to 344, buttons from 338; 1920x1080 box 45 px, three lines to 598, buttons from 534; 1024x1366 four lines to 783, buttons from 676. Jon saw it at about 1527 wide. Tested: grid-template-rows: minmax(0,1fr) auto auto auto auto minmax(0,1fr) sizes the row to the text at all three (e.g. 1920x1080: text to 555, buttons from 577), with no page scroll.

CLASS CHECK: Local. drawFigure() is this game's only fitting routine; the grid rule is in this game's own stylesheet (no other game in the repo uses grid-template-rows: 1fr auto); check_big() is this game's verifier. No shared code is involved. (Two patterns noted for Project Claude, not merged here: checkers measuring a stand-in rather than the real thing, as with queue item 1's phone-fit "Submit" control; and no checker anywhere tests text overlapping a control.)

EXACT CHANGE:
1. games/whose-side-are-you-on/index.html, drawFigure(): replace the fixed mx/my reservation with a fit of what is actually drawn. For a candidate scale k, the content box is the union of: the three vertices, each padded by 22 px (half the 44 px tap band, so no band is clipped at the SVG's edge); each label's box at mid + n*clear ± (hw, hh), exactly as placed now; the θ label at labR along the bisector ± its half-size; the right-angle square. Find the largest k with the content box within W x H less a 6g pad (bisection is fine: every extent is monotone in k). Centre the content box, not the triangle. Labels, clear, arcR, labR, S, g and the tap-band width are unchanged.
2. Same routine on phones and large screens. figureSize() and bigSize() are unchanged.
3. Same file, the >=1024px media query: .qcard grid-template-rows becomes minmax(0,1fr) auto auto auto auto minmax(0,1fr). Nothing else in the layout changes.
4. scripts/verify-whose-side-are-you-on.py, check_big():
   a. Measure the drawn triangle's bounding box (from the three side lines' endpoints on screen). On the axis that limits it, it must fill at least 75% of the figure box, for every item of a seeded round in all four stages at 1366x768 and 1920x1080. Also check that no label, θ or tap band is clipped by the SVG's edge, at those sizes and at 320 and 390.
   b. For every stage, asking, wrong and right: the bottom of the question's last line of text (a Range over #ask's contents, not #ask's box) is at or above the top of the first control below it, and no text in the right-hand column overlaps another element there. Sizes: 1024x700, 1222x688, 1366x768, 1920x1080, 1024x1366.
   c. Keep the existing control and scroll checks.
5. Plants: the old margin restored (mx = 2*hw + 10g) is caught; the triangle centred instead of the content box, with a label pushed off the edge, is caught; the grid rows reverted to 1fr auto auto auto auto 1fr is caught.
6. Report the before and after triangle size for the 7-24-25 item and the median across the round at 1920x1080 and 1366x768; the phone figure size at 320 and 390 before and after; the Stage 4 question's text bottom and the buttons' top at the five sizes in 4b, before and after.

DO NOT TOUCH: the triples, turns, tilts and seeds; question wording; label text, sizes, colours and line styles; tap-band width; the two-column layout other than the one grid-rows rule; bigSize(); the feedback panel and Jon's lines (WHOSE-SIDE-INTRO handles those); the start screen and its art; any other game; shared assets and shared checkers; the files under COORDINATION.

SUCCESS CONDITION: On a large screen the triangle fills at least 75% of its figure box on the limiting axis for every item; the question text never runs under a control at any tested size or stage; nothing is clipped; the page never scrolls at the large sizes; the phone checks (Next above the fold, tap bands 44 px, no sideways scroll, Aa) still pass; all three plants are caught; full verifier 0 failures. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: any item cannot reach 75% without shrinking labels or tap bands (report which, with numbers); the fit makes a phone layout fail a check that passes on main; a label would overlap another label or a side at the new fit; with the rows fix the right-hand column no longer fits a screen without scrolling at any tested size (report; do not shrink the text).

## Amendment 1 (Project Claude, 6 Nov 2026, 17:58), verbatim

RULING (Project Claude, 6 Nov 17:58) on WHOSE-SIDE-FIT STOP IF 1: neither A, B nor C.

The 75% figure was an estimate; the property the check must prove is "no wasted space". Replace item 4a's threshold with:
- For every item at 1366x768 and 1920x1080: on the drawing's limiting axis, its content box (triangle, labels, θ, right-angle square, corner pads) reaches the 6g pad on both sides, within 1 px. That is the pass condition.
- Sanity floor: the triangle's own bounding box fills at least 70% of the figure box on that axis.
- Keep the plants; the old-margin plant (mx = 2*hw + 10g) must now be caught by the reach check (it leaves slack), not by the percentage.
- Report the fill distribution as you did (median/minimum per size, the 7-24-25 range), and list the 240 label-limited drawings by triple, as "label-limited, no slack".
Labels, pads, label placement and the two-column layout stay exactly as the contract fixed them. Then do items 4-6, open the PR, stop at a green Gate.

PAGES: after #673 merges on main, re-run the Pages deploy once (two timeouts were GitHub-side; the live site is at run 1346, 79b7bc3). Report the run and its result. Jon checks the live page in a browser.
