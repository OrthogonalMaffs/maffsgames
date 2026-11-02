# Handover: the portal score ticker can be paused (TICKER-PAUSE, Jon, 29 Oct 2026; home lane)

**Why.** WCAG 2.2.2 (Pause, Stop, Hide): the ticker moved for ever with no way to stop it; it also made the scores hard to read and Jon wants it still for screenshots.

**Class check.** Local. The ticker (markup, CSS, JS) exists only in the portal's `index.html` (`scoreTicker`); nothing shared was touched. `schools/assets/launch-sash.js` only inserts the announcement strip before it.

**What it does now.**
- A real `<button id="tickerToggle">` at the ticker's left edge (36 x 36 px, inside the 36 px ticker, so the ticker's height is unchanged at 360, 768 and 1440): `aria-label` "Pause scores" / "Play scores", `aria-pressed`. It takes keyboard focus; Enter and Space press it; it works on touch.
- The scores sit in `#scoreTickerTrack`, beside the button, so the button is not destroyed when `buildTicker()` rebuilds the scores on each update.
- Paused while the pointer is over the scores (CSS), and while a keyboard-focused element inside the scores has focus (JS, `.tp-focus`; the scores have no focusable item today). **Hovering or focusing the button itself does not hold the scores still**, or pressing Play could never be seen working (Jon's item 2 read literally would pause on the button's own focus; this is the reading that works).
- A pause set by the button (`.tp-user`) survives hover and focus changes until the button is pressed again.
- `prefers-reduced-motion: reduce`: no animation, one set of scores (the repeats that make the loop seamless are `.ticker-dup`, hidden), every score still there, the track scrolls sideways by hand, and the button is hidden (nothing to pause). The ticker had no reduced-motion handling before (the only other use in the file is the answers counter), so nothing was changed that existed.

**A fault found on the way.** On main, hover never paused the ticker: `.score-ticker:hover .score-ticker-inner{animation-play-state:paused}` lost to the inline `animation` shorthand that `buildTicker()` sets (it resets the play state to running). The pause rules now carry `!important` for that reason. Measured on main with the same fake scores: moving with the pointer over it.

**Verifier.** `scripts/check-ticker-pause.py` (CI line; deps `index.html`): at 1440, 768 and 360 it checks running, hover, focus, the button (labels, `aria-pressed`, persistence through hover and focus, Play with the pointer still over the button, Enter and Space), reduced motion (nothing moves, 12 scores once each, no button, scrollable) and the height (36); plus five planted faults through `plant_common.py`: no hover pause, a button that sets no state, a button that never changes its name, no focus pause, no reduced-motion rule.

**Not touched.** The score data, its source and refresh logic, the announcement strip, the hero, the grid and filters, analytics events, any game page. `test-scores-offline.py` (the ticker's data) is unchanged and still passes.
