/* Site navigation (contract SITE-NAV, Jon 21 Nov 2026, 11:03-11:04; canon §7.5.8).

   1. The back link goes back to the hub the student came from. Every page's a.back-link is written in its HTML
      (most say "← Back to Games" and go to the front screen), so a student who opened Angle Ace from OP for
      Secondary was sent to the front screen. Now, when this page was opened from a page in HUBS (same origin), every
      a.back-link goes to that hub and reads "← Back to <label>". The hub is remembered for this page in
      sessionStorage, so a reload or a ?level= switch keeps it. Opened directly, from another site or from another
      game, nothing changes: every link stays exactly as written. The referrer is read in the page and never sent.
      window.MaffsNav = { backHref, backLabel, shortLabel } (null without a hub) is what other scripts read
      (schools/assets/stage-exit.js's row link and HUD home link).
   2. A MaffsGames logo, linking to "/", fixed top left in the empty margin beside the page, shown only while the
      measured gap between the viewport's left edge and everything the page paints fits it (no width guess), and only
      on a fine pointer (never phones or tablets). Re-measured on load, on resize and after each click, key or touch. A page that shows
      a logo of its own opts out with <html data-site-logo="off">; scripts/check-site-nav.py lists each with its reason.

   No dependencies. Any failure leaves the page as written. */
(function () {
  'use strict';
  var HUBS = {
    '/': 'Games',
    '/op/': 'OP for Secondary',
    '/essentials/': 'Essentials',
    '/spec-map/': 'Specification map',
    '/updates/': 'What’s changed',
    '/6-7/': '6 or 7',
    '/printables/': 'Printable packs',
    '/escape-rooms/': 'Escape rooms',
    '/leaderboards/': 'Leaderboards',
    '/parents/algebra-basics/': 'Algebra Basics guide',
    '/parents/angles/': 'Angles guide',
    '/parents/area-perimeter/': 'Area & Perimeter guide',
    '/parents/averages/': 'Mean, Median & Mode guide',
    '/parents/circle-theorems/': 'Circle Theorems guide',
    '/parents/coordinates/': 'Coordinates & Quadrants guide',
    '/parents/expanding-factorising/': 'Expanding & Factorising guide',
    '/parents/fractions/': 'Fractions, Decimals & Percentages guide',
    '/parents/graphs-transformations/': 'Graphs & Transformations guide',
    '/parents/indices-surds/': 'Indices & Surds guide',
    '/parents/negative-numbers/': 'Negative Numbers guide',
    '/parents/probability-trees/': 'Probability Trees guide',
    '/parents/probability/': 'Probability guide',
    '/parents/pythagoras/': 'Pythagoras’ Theorem guide',
    '/parents/ratio-proportion/': 'Ratio & Proportion guide',
    '/parents/sequences/': 'Sequences & Patterns guide',
    '/parents/simultaneous-equations/': 'Simultaneous Equations guide',
    '/parents/standard-form/': 'Standard Form guide',
    '/parents/statistics-data/': 'Statistics & Data guide',
    '/parents/trigonometry/': 'Trigonometry guide'
  };
  var KEY = 'maffs-nav:';
  var LOGO = { left: 16, top: 16, size: 40, clear: 16 };   // px: where the logo sits, and the space it keeps clear

  function norm(path) { return path.replace(/index\.html$/, ''); }

  var nav = { backHref: null, backLabel: null, shortLabel: null, hubs: HUBS };
  try {
    var here = norm(location.pathname), hub = null;
    if (document.referrer) {
      var ref = new URL(document.referrer);
      var rp = norm(ref.pathname);
      if (ref.origin === location.origin && rp !== here && Object.prototype.hasOwnProperty.call(HUBS, rp)) hub = rp;
    }
    try {
      if (hub) sessionStorage.setItem(KEY + here, hub);
      else {
        var kept = sessionStorage.getItem(KEY + here);
        if (kept && Object.prototype.hasOwnProperty.call(HUBS, kept)) hub = kept;
      }
    } catch (e) { /* storage blocked: this load's referrer only */ }
    if (hub) {
      nav.backHref = hub;
      nav.backLabel = '← Back to ' + HUBS[hub];
      nav.shortLabel = '← ' + HUBS[hub];      // stage-exit's row keeps its short form (STAGE-EXIT-LABEL)
    }
  } catch (e) { nav.backHref = nav.backLabel = nav.shortLabel = null; }
  window.MaffsNav = nav;

  function relink() {
    if (!nav.backHref) return;
    var links = document.querySelectorAll('a.back-link');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      a.setAttribute('href', nav.backHref);
      var span = a.querySelector('.back-text');       // "←<span class=back-text> Back to Games</span>": the span hides in some modes
      if (span) span.textContent = ' Back to ' + HUBS[nav.backHref];
      else a.textContent = nav.backLabel;
      if (a.hasAttribute('aria-label')) a.setAttribute('aria-label', 'Back to ' + HUBS[nav.backHref]);
    }
  }

  // ---- the logo ----
  var logo = null, src = null;
  try {
    var me = document.currentScript && document.currentScript.src;
    if (me) src = me.replace(/site-nav\.js(\?.*)?$/, 'logo.svg');
  } catch (e) { src = null; }

  function painted(el, cs) {
    var tag = el.tagName;
    if (/^(IMG|SVG|CANVAS|VIDEO|INPUT|BUTTON|SELECT|TEXTAREA|IFRAME|PICTURE|OBJECT|EMBED)$/i.test(tag)) return true;
    var bg = cs.backgroundColor;
    if (bg && bg !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(bg)) return true;
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return true;
    if (cs.boxShadow && cs.boxShadow !== 'none') return true;
    var sides = ['Top', 'Right', 'Bottom', 'Left'];
    for (var i = 0; i < 4; i++) {
      if (parseFloat(cs['border' + sides[i] + 'Width']) > 0 && cs['border' + sides[i] + 'Style'] !== 'none'
          && !/rgba\([^)]*,\s*0\)$/.test(cs['border' + sides[i] + 'Color'])) return true;
    }
    return false;
  }

  function fixedish(el) {
    for (var e = el; e && e !== document.body; e = e.parentElement) {
      if (getComputedStyle(e).position === 'fixed') return true;
    }
    return false;
  }

  // Does anything the page paints come within the logo's clear space? A fixed box is judged where it is on screen; a
  // box in the page's flow is judged by its left edge alone, at any height, since scrolling can bring it under the logo.
  function conflict() {
    var right = LOGO.left + LOGO.size + LOGO.clear, bottom = LOGO.top + LOGO.size + LOGO.clear;
    function hits(r, fixed) {
      if (r.width <= 0 || r.height <= 0 || r.left >= right) return false;
      return fixed ? r.top < bottom && r.bottom > 0 : r.right > 0;
    }
    var all = document.body.getElementsByTagName('*');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el === logo || (logo && logo.contains(el))) continue;
      var cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') continue;
      if (painted(el, cs)) {
        var r = el.getBoundingClientRect();
        if (r.left < right && hits(r, fixedish(el))) return el;
      }
    }
    var walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var range = document.createRange(), t;
    while ((t = walk.nextNode())) {
      if (!/\S/.test(t.nodeValue) || (logo && logo.contains(t))) continue;
      var p = t.parentElement, cp = p && getComputedStyle(p);
      if (!cp || cp.visibility === 'hidden' || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName)) continue;
      range.selectNodeContents(t);
      var rs = range.getClientRects();
      for (var j = 0; j < rs.length; j++) if (hits(rs[j], fixedish(p))) return p;
    }
    return null;
  }

  function place() {
    if (!logo) return;
    var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
    var block = fine ? conflict() : 'coarse pointer';
    logo.style.display = block ? 'none' : 'block';
    logo.setAttribute('data-blocked-by', block ? (block.nodeType ? (block.tagName.toLowerCase() + (block.id ? '#' + block.id : '')
      + (block.className && typeof block.className === 'string' ? '.' + block.className.trim().split(/\s+/).join('.') : '')) : block) : '');
  }

  var pending = 0;
  function later(ms) {
    if (pending) return;
    pending = setTimeout(function () { pending = 0; try { place(); } catch (e) { if (logo) logo.style.display = 'none'; } }, ms);  // lock-ok: layout only, marks nothing
  }

  function addLogo() {
    if (!src || document.documentElement.getAttribute('data-site-logo') === 'off' || document.querySelector('.maffs-site-logo')) return;
    logo = document.createElement('a');
    logo.className = 'maffs-site-logo';
    logo.href = '/';
    logo.setAttribute('aria-label', 'MaffsGames home');
    logo.style.cssText = 'position:fixed;left:' + LOGO.left + 'px;top:' + LOGO.top + 'px;width:' + LOGO.size + 'px;height:'
      + LOGO.size + 'px;z-index:1001;display:none;border-radius:8px;line-height:0';
    var img = document.createElement('img');
    img.src = src;
    img.alt = '';
    img.width = img.height = LOGO.size;
    img.style.cssText = 'width:100%;height:100%;display:block';
    logo.appendChild(img);
    document.body.appendChild(logo);
    place();
    window.addEventListener('resize', function () { later(150); });
    window.addEventListener('load', function () { later(0); });
    // A screen changes after the student does something, so the logo is re-measured after each click, key or touch
    // (once the screen has changed, and again once any short transition has run), never on a timer or every DOM
    // change: a page's own ticking clock would otherwise re-measure the whole page every second for the whole session
    // (it doubled test-escape-times.py's run, 119 s to 246 s, on this contract's first Gate).
    var afterInput = function () {
      later(300);
      setTimeout(function () { later(0); }, 1500);   // lock-ok: layout only, marks nothing
    };
    ['click', 'keyup', 'touchend'].forEach(function (ev) { document.addEventListener(ev, afterInput, true); });
  }

  function ready() {
    try { relink(); } catch (e) { /* leave the links as written */ }
    try { addLogo(); } catch (e) { if (logo) logo.style.display = 'none'; }
  }
  nav.place = function () { place(); return logo ? logo.getAttribute('data-blocked-by') : 'no logo'; };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
