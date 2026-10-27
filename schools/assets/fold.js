/* MaffsFold: answer options two to a row, decided by measuring them (canon §7.5.7; Jon's ruling R3, 26 Oct 2026).

   Two options to a row only when EVERY option fits on one line, without wrapping, at the width it would have, with tap
   targets at least 44px tall; otherwise one to a row. A character count cannot tell (a KaTeX fraction is short in
   characters and wide on screen, a word is the reverse), so this measures the rendered options:

     <div class="choices maffs-options"> <button>…</button> <button>…</button> … </div>

   Each .maffs-options box is laid out two to a row with every option held to one line (.maffs-measuring, nowrap); an
   option whose content is wider than its box would have wrapped, so the box goes back to one to a row. Decided again
   when the box's options are replaced (a new question: its direct children change), when the fonts finish loading and
   when the box's width changes (a resize, or the box first shown), never when something inside an option changes (a
   tick added after answering), so the layout never jumps while a student reads the feedback. A box that is not shown
   is not decided until it is. The styles are in fold.css; a page needs both. */
(function () {
  'use strict';
  if (window.MaffsFold) return;
  var MIN_TAP = 44;

  function shown(el) {
    return getComputedStyle(el).display !== 'none';
  }

  // One box: two to a row when every shown option fits on one line at half width and is at least 44px tall.
  function decide(box) {
    if (!box.offsetWidth) return false;                 // not shown yet: decided when its width appears
    var opts = Array.prototype.filter.call(box.children, shown);
    if (opts.length < 2) { box.classList.remove('maffs-two-up'); return false; }
    box.classList.add('maffs-two-up', 'maffs-measuring');
    var fits = opts.every(function (el) {
      return el.scrollWidth <= el.clientWidth + 1 && el.getBoundingClientRect().height >= MIN_TAP - 0.5;
    });
    box.classList.remove('maffs-measuring');
    if (!fits) box.classList.remove('maffs-two-up');
    return fits;
  }

  var pending = new Set(), frame = 0;
  function later(box) {
    pending.add(box);
    if (frame) return;
    frame = requestAnimationFrame(function () {
      frame = 0;
      var boxes = Array.from(pending); pending.clear();
      boxes.forEach(function (b) { if (b.isConnected) decide(b); });
    });
  }

  var watched = new WeakSet(), widths = new WeakMap();
  var kids = new MutationObserver(function (records) {
    records.forEach(function (r) { later(r.target); });
  });
  // Width only: two to a row changes the box's height, which must not decide it again.
  var sized = new ResizeObserver(function (entries) {
    entries.forEach(function (e) {
      var w = Math.round(e.contentRect.width);
      if (widths.get(e.target) !== w) { widths.set(e.target, w); later(e.target); }
    });
  });
  function watch(box) {
    if (watched.has(box)) return;
    watched.add(box);
    kids.observe(box, { childList: true });
    sized.observe(box);
    later(box);
  }
  var scanning = 0;
  function scan() {
    if (scanning) return;
    scanning = requestAnimationFrame(function () {
      scanning = 0;
      document.querySelectorAll('.maffs-options').forEach(watch);
    });
  }
  function all() {
    document.querySelectorAll('.maffs-options').forEach(later);
  }

  // A box added later (a game that builds its question area on Start) is found by watching the page.
  new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true });
  scan();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(all);

  window.MaffsFold = { decide: decide, refresh: all };
})();
