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
 *     opts.inset  px at the bottom that something fixed covers. Default: the site footer's height while it is pinned
 *                 (position: fixed), 0 once it sits in the flow, which it does on every playable page (site-footer--flow).
 *     opts.clear  px of clearance above the fold that counts as "in view" (default 0); the page is moved so the
 *                 element ends 8px above the fold, as before.
 *     opts.up     also scroll back up when keep has gone above the top of the window (default false).
 *     opts.smooth first pass glides (honours prefers-reduced-motion); later passes are instant.
 *
 * It also watches the element for a few seconds (opts.watch ms, default 4000, 0 = off) and makes the same pass each time
 * it changes size: a font can arrive after fonts.ready (KaTeX's faces are requested as the working is drawn), so the two
 * passes above can both run before the block grows (the 6 P's, main run 40529609805, after #576).
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

  // The px the site footer covers at the bottom: its height while pinned, nothing once it is in the flow (or absent).
  function footerInset() {
    var f = document.querySelector('.site-footer');
    if (!f || getComputedStyle(f).position !== 'fixed') return 0;
    return Math.round(f.getBoundingClientRect().height) || 40;
  }

  function get(x) { return typeof x === 'function' ? x() : x; }

  function reveal(target, opts) {
    opts = opts || {};
    var clear = opts.clear || 0, wanted = opts.inset, up = !!opts.up;
    var mine = ++token, born = Date.now(), watch = null;
    function stop() { if (watch) { watch.disconnect(); watch = null; } }

    function pass(smooth) {
      var el = get(target), keep = get(opts.keep) || el;
      if (!el || !el.getBoundingClientRect || el.isConnected === false) return;
      var dy = delta(el, keep, typeof wanted === 'number' ? wanted : footerInset(), up, clear);
      if (!dy) return;
      var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      try { window.scrollBy({ top: dy, left: 0, behavior: smooth && !still ? 'smooth' : 'instant' }); }
      catch (e) { window.scrollBy(0, dy); }
    }
    function later() { if (mine === token && touched <= born) pass(false); else stop(); }

    pass(!!opts.smooth);
    try {
      requestAnimationFrame(function () {
        later();
        if (document.fonts && document.fonts.ready) document.fonts.ready.then(later);
      });
    } catch (e) { /* ignore */ }
    var ms = typeof opts.watch === 'number' ? opts.watch : 4000, first = get(target);
    if (ms > 0 && first && window.ResizeObserver) {
      try {
        watch = new ResizeObserver(later);
        watch.observe(first);
        setTimeout(stop, ms);
      } catch (e) { /* ignore */ }
    }
  }

  window.MaffsScroll = { reveal: reveal, delta: delta };
})();
