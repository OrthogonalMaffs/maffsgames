# Class search: feedback or Next scrolled into view once (27 Oct 2026; Jon's request after #566, report only, nothing fixed)

**The fault (#566):** the page scrolled the feedback into view once, then the maths font arrived and the working grew; nothing scrolled again, so Next ended below a 375 x 667 screen. **Search:** `scrollIntoView`, `scrollBy`, `scrollTo` and `scrollTop` in `games/`, `schools/` and `escape-rooms/` on main (c20374f). This is a read of each call line from the search, not a measurement: whether each one fails needs the font to arrive after the scroll (a first visit with a cold font cache), at 375 x 667 or smaller.

**Scroll to keep feedback, the answer row or Next in view, once, with no second scroll after layout settles (10):**
- `games/decimal-detective/index.html:920` (`scrollBy` so Next clears the fold)
- `games/estimation-engine/index.html:489`
- `games/how-many-parts/index.html:1507`
- `games/just-pythag-it-bruv/index.html:1161` (`scrollTo` by dy)
- `games/squared-squirrel/index.html:1056`
- `games/take-a-walk/index.html:1390`
- `games/truth-buster/index.html:495`
- `games/screening-room/index.html:1017` (`scrollIntoView` nearest on the result)
- `games/simultaneous-solver/index.html:893` (`fitInView`; the file has one `fonts.ready` elsewhere, and I did not check whether the fit is re-run from it)
- `schools/assets/keypad.js:63` (`together()`: the answer row and the keys; shared by every typed game)

**Not this class (a scroll for another reason, or none after a font):** `games/factor-theorem:1027`, `games/the-perfect-prank:586` (next frame, centred), `games/truth-will-set-you-free:843` (the expression section); the `scrollTo(0, 0)` resets in `escape-rooms/assets/engine.js`, `boolean-blitz`, `factor-theorem`, `the-perfect-prank`, `truth-will-set-you-free`; `escape-rooms/assets/engine.js:413` (to a node on a click). `schools/assets/fold.js` re-decides on `fonts.ready` but does not scroll. The `focus({ preventScroll: true })` calls scroll nothing.

**To settle which of the ten fail:** the same 375 x 667 sweep used for #566 (every question, wrong answer, Next on screen) with the font cache cold, per game. The phone-fit gate's fonts-real and fonts-fallback runs compare the two states; the fold contract's `measure-phone-fit.py` is the cloud lane's.

# Item 10 (the 6 P's in the phone-fit gate): not done, and why
The roster is `.claude/rules/game-roster.md` and `measure-phone-fit.py` loads `games/<slug>/index.html` only (lines 320, 327, 372). The 6 P's is at `/the-6-ps/`, so a roster row alone does not work: the driver would need a page path and its own start flow, which is a change to `measure-phone-fit.py` beyond the roster entry (Jon: stop and tell). Branch and worktree for it were removed unused.
