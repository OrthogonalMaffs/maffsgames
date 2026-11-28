3-GON-LINE-UP-BUILD AMENDMENT 1 (Project Claude, 28 Nov 2026, ruling on the getBBox STOP).

Ruling: getBBox() measures Outfit's full font box (1.21-1.28 em tall), not the visible text; your figures show the ink (0.72 em) inside every bank box with about 0.13 em to spare at top and bottom and at least 0.137 units at the sides. Jon's rule is that labels never visibly clash, so the check tests ink. The bank, both hashes and every position stay exactly as the contract states.

Changes to the contract:
1. Step 5c, the containment check, now reads: "every rendered label's ink box lies within its bank box, converted to the SVG's coordinates, at every size". The ink box is the glyphs' measured extents (the browser's own text measurement, e.g. canvas measureText actualBoundingBoxLeft/Right/Ascent/Descent, with the label's exact font, weight 600, size, text-anchor middle and dominant-baseline central, placed at the label's rendered position). Do not use getBBox for this check. Put a comment above the check giving your figures (getBBox 1.21-1.28 em tall against the bank's 1.1 em; ink 0.72 em, 0.13 em inside) and this amendment's name.
2. Step 5e gains a ninth plant: one label's bank y moved by 0.2 units, so its ink leaves its box; it must be caught.
3. Third STOP IF now reads "A rendered label's ink box falls outside its bank box at any size".
4. Your three "Decided for you" items are accepted: "Confirm accusation"; feedback first on one column; on small phones the Stage 2-4 line-up may need a scroll before answering, provided "Confirm accusation" sits directly under the line-up and the selected suspects stay marked. Report the scroll needed at 375x667 for each of Stages 2-4 in the PR body.
5. Save this amendment verbatim as docs/handover/contracts/2026-11-28-3-gon-line-up-build-amendment-1.md and include it in the PR.

Then carry on with step 4 (integration), step 6 (phone fit, contrast) and step 7. The tier is unchanged: Medium, merge on green with merge-pr.py. No hold.
