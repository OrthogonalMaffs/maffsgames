/* MaffsScroll: bring feedback, Next or an answer row into view, and keep it there while the page settles.
 *
 * The fault this closes (the 6 P's, #566; class search 27 Oct 2026): a page scrolled its feedback into view once,
 * then the maths font arrived, the working grew, and Next ended under the fold. reveal() scrolls now, again on the
 * next animation frame, and again when the fonts are ready, and each pass does nothing if the element is already
 * in view. Every game and keypad.js calls this; none keeps a scrollIntoView / scrollBy of its own for feedback or Next
 * (scripts/check-scroll-reveal.py).
 *
 *   MaffsScroll.reveal(el, opts)     (el and opts.keep may each be a function returning the element, looked up at
 *                                    every pass, for a control that is drawn after the call)
 *     el          the element whose bottom must clear the fold (Next, the feedback, the keys).
 *     opts.keep   the element whose top must stay in the window (default el): the page never moves up past it,
 *                 so the question the student is reading is not scrolled off the top.
 *     opts.inset  px at the bottom the page's fixed footer covers (default 40).
 *     opts.clear  px of clearance above the fold that counts as "in view" (default 0); the page is moved so the
 *                 element ends 8px above the fold, as before.
 *     opts.up     also scroll back up when keep has gone above the top of the window (default false).
 *     opts.smooth first pass glides (honours prefers-reduced-motion); later passes are instant.
 *
 * A second reveal() call replaces the first one's pending passes. A wheel, touch or key from the student cancels
 * the passes still pending, so the page never fights their own scrolling.
 */
(function () {
  'use strict';
  var MARGIN = 8, token = 0, touched = 0;

  function mark() { touched = Date.now(); }
  ['wheel', 'touchstart', 'keydown'].forEach(function (t) {
    try { window.addEventListener(t, mark, { passive: true, capture: true }); } catch (e) { /* ignore */ }
  });

  // The scroll, in px, that one pass makes: 0 when el is already in view. Positive is down the page.
  function delta(el, keep, inset, up, clear) {
    var fold = window.innerHeight - inset, r = el.getBoundingClientRect(), k = keep.getBoundingClientRect();
    if (!r.height && !r.width) return 0;                       // not laid out: nothing to place
    var dy = 0;
    if (r.bottom > fold - clear) dy = Math.min(r.bottom - fold + MARGIN, k.top - MARGIN);
    else if (up && k.top < 0) dy = k.top - MARGIN;
    return dy > 0 ? Math.ceil(dy) : (up && dy < 0 ? Math.floor(dy) : 0);   // whole pixels: a fraction scrolls short
  }

  function get(x) { return typeof x === 'function' ? x() : x; }

  function reveal(target, opts) {
    opts = opts || {};
    var clear = opts.clear || 0, inset = typeof opts.inset === 'number' ? opts.inset : 40, up = !!opts.up;
    var mine = ++token, born = Date.now();

    function pass(smooth) {
      var el = get(target), keep = get(opts.keep) || el;
      if (!el || !el.getBoundingClientRect || el.isConnected === false) return;
      var dy = delta(el, keep, inset, up, clear);
      if (!dy) return;
      var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      try { window.scrollBy({ top: dy, left: 0, behavior: smooth && !still ? 'smooth' : 'instant' }); }
      catch (e) { window.scrollBy(0, dy); }
    }
    function later() { if (mine === token && touched <= born) pass(false); }

    pass(!!opts.smooth);
    try {
      requestAnimationFrame(function () {
        later();
        if (document.fonts && document.fonts.ready) document.fonts.ready.then(later);
      });
    } catch (e) { /* ignore */ }
  }

  window.MaffsScroll = { reveal: reveal, delta: delta };
})();
