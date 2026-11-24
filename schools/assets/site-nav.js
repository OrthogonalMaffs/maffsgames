/* Site navigation (contract SITE-NAV, Jon 21 Nov 2026, 11:03-11:04; canon §7.5.8).

   1. The back link goes back to the hub the student came from. Every page's a.back-link is written in its HTML
      (most say "← Back to Games" and go to the front screen), so a student who opened Angle Ace from OP for
      Secondary was sent to the front screen. Now, when this page was opened from a page in HUBS (same origin), every
      a.back-link goes to that hub and reads "← Back to <label>". The hub is remembered for this page in
      sessionStorage, so a reload or a ?level= switch keeps it. Opened directly, from another site or from another
      game, nothing changes: every link stays exactly as written. The referrer is read in the page and never sent.
      window.MaffsNav = { backHref, backLabel, shortLabel } (null without a hub) is what other scripts read
      (schools/assets/stage-exit.js's row link and HUD home link).
      The class page (contract CLASS-PAGE, Jon 21 Nov 2026): a game opened from /class/ whose own address carries
      "#kids/<name>" goes back to /class/#<name>. The name is read from this page's own location.hash through MaffsKids
      (schools/assets/kids-look.js, the one copy of the name rule), on pages that load it; only the hub's path is kept
      in sessionStorage, never the name or the fragment.
   2. A MaffsGames logo, linking to "/", fixed top left in the empty margin beside the page, shown only while the
      measured gap between the viewport's left edge and everything the page paints fits it (no width guess), and only
      on a fine pointer (never phones or tablets). Re-measured on load, on resize and after each click, key or touch. A page that shows
      a logo of its own opts out with <html data-site-logo="off">; scripts/check-site-nav.py lists each with its reason.
   3. The game's name during play (contract GAME-TITLE-IN-PLAY, Jon 24 Nov 2026). Most games write their title inside
      the start screen, so it goes when Start is pressed. On a game page this file's tag carries
      data-game-name="<the roster's name>" (scripts/apply-site-nav.py writes it from .claude/rules/game-roster.md;
      scripts/check-site-nav.py holds it equal). The name is shown as plain text beside the logo, top aligned with it,
      only while the logo shows and only while the page's own title is not showing: hidden when the page's first <h1>
      is rendered, or when any rendered text on the page equals the name. Its width is the measured free margin (from
      its left edge to the nearest thing the page paints, by the logo's own measure, less the logo's clear space); it
      wraps to at most three lines and does not show where the name needs more, or the free width is under 120 px.
      Re-measured exactly when the logo is. window.MaffsNav.gameName is the name (null without one), and
      MaffsNav.nameHiddenBy why the label is hidden ('' while it shows). Not a link, aria-hidden (the page's <title>
      names the game), and it takes no clicks.

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
    '/class/': 'the class page',
    // Every parents' guide reads "← Back to the guide": a guide's full name wrapped on a phone (SITE-NAV-GUIDE-LABEL,
    // Jon 21 Nov 2026, "back to guide is fine"). scripts/check-site-nav.py proves each label fits one line at 360 px.
    '/parents/algebra-basics/': 'the guide',
    '/parents/angles/': 'the guide',
    '/parents/area-perimeter/': 'the guide',
    '/parents/averages/': 'the guide',
    '/parents/circle-theorems/': 'the guide',
    '/parents/coordinates/': 'the guide',
    '/parents/expanding-factorising/': 'the guide',
    '/parents/fractions/': 'the guide',
    '/parents/graphs-transformations/': 'the guide',
    '/parents/indices-surds/': 'the guide',
    '/parents/negative-numbers/': 'the guide',
    '/parents/probability-trees/': 'the guide',
    '/parents/probability/': 'the guide',
    '/parents/pythagoras/': 'the guide',
    '/parents/ratio-proportion/': 'the guide',
    '/parents/sequences/': 'the guide',
    '/parents/simultaneous-equations/': 'the guide',
    '/parents/standard-form/': 'the guide',
    '/parents/statistics-data/': 'the guide',
    '/parents/trigonometry/': 'the guide',
    // The "When will I use this?" topic pages link their games under "Practise it" (WHEN-WILL-I-USE-THIS, Jon 22 Nov 2026).
    '/when-will-i-use-this/ratio/': 'the topic page',
    '/when-will-i-use-this/percentages/': 'the topic page',
    '/when-will-i-use-this/area-perimeter/': 'the topic page',
    '/when-will-i-use-this/averages/': 'the topic page',
    '/when-will-i-use-this/speed-distance-time/': 'the topic page',
    '/when-will-i-use-this/formulae/': 'the topic page',
    '/when-will-i-use-this/angles/': 'the topic page',
    '/when-will-i-use-this/negative-numbers/': 'the topic page',
    '/when-will-i-use-this/estimation/': 'the topic page',
    '/when-will-i-use-this/decimals-measurement/': 'the topic page',
    '/when-will-i-use-this/pythagoras/': 'the topic page',
    '/when-will-i-use-this/trigonometry/': 'the topic page',
    '/when-will-i-use-this/probability/': 'the topic page',
    '/when-will-i-use-this/exponential-change/': 'the topic page',
    '/when-will-i-use-this/gradients/': 'the topic page',
    '/when-will-i-use-this/transformations/': 'the topic page',
    '/when-will-i-use-this/hypothesis-testing/': 'the topic page'
  };
  var KEY = 'maffs-nav:';
  var LOGO = { left: 16, top: 16, size: 40, clear: 16 };   // px: where the logo sits, and the space it keeps clear
  var NAME = { size: 15, weight: 600, line: 1.25, lines: 3, min: 120 };   // the game's name beside the logo (point 3)

  function norm(path) { return path.replace(/index\.html$/, ''); }

  var nav = { backHref: null, backLabel: null, shortLabel: null, hubs: HUBS, gameName: null, nameHiddenBy: 'no name' }, hubPath = null;
  try {
    var named = document.currentScript && document.currentScript.getAttribute('data-game-name');
    if (named && /\S/.test(named)) { nav.gameName = named; nav.nameHiddenBy = 'no logo on this page'; }
  } catch (e) { nav.gameName = null; }

  // The way back to the class page carries the class name from this page's own fragment, never from storage.
  function classFragment(hub) {
    if (hub !== '/class/' || !window.MaffsKids) return '';
    return window.MaffsKids.classLink(window.MaffsKids.read(location.hash).name);
  }
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
      hubPath = hub;
      nav.backHref = hub + classFragment(hub);
      nav.backLabel = '← Back to ' + HUBS[hub];
      nav.shortLabel = '← ' + HUBS[hub];      // stage-exit's row keeps its short form (STAGE-EXIT-LABEL)
    }
  } catch (e) { nav.backHref = nav.backLabel = nav.shortLabel = hubPath = null; }
  window.MaffsNav = nav;

  function relink() {
    if (!nav.backHref) return;
    var links = document.querySelectorAll('a.back-link');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      a.setAttribute('href', nav.backHref);
      var span = a.querySelector('.back-text');       // "←<span class=back-text> Back to Games</span>": the span hides in some modes
      if (span) span.textContent = ' Back to ' + HUBS[hubPath];
      else a.textContent = nav.backLabel;
      if (a.hasAttribute('aria-label')) a.setAttribute('aria-label', 'Back to ' + HUBS[hubPath]);
    }
  }

  // ---- the logo ----
  var logo = null, src = null, label = null;
  try {
    var me = document.currentScript && document.currentScript.src;
    if (me) src = me.replace(/site-nav\.js(\?.*)?$/, 'favicon.svg');
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
      if (el === logo || (logo && logo.contains(el)) || el === label) continue;
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
      if (!/\S/.test(t.nodeValue) || (logo && logo.contains(t)) || (label && label.contains(t))) continue;
      var p = t.parentElement, cp = p && getComputedStyle(p);
      if (!cp || cp.visibility === 'hidden' || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName)) continue;
      range.selectNodeContents(t);
      var rs = range.getClientRects();
      for (var j = 0; j < rs.length; j++) if (hits(rs[j], fixedish(p))) return p;
    }
    return null;
  }

  // ---- the game's name beside the logo (point 3) ----
  function fold(s) { return String(s).replace(/[\u2018\u2019]/g, "'").replace(/\s+/g, ' ').trim().toLowerCase(); }

  function rendered(el) {
    if (!el || !el.getClientRects().length) return false;          // no box: display:none on it or an ancestor
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden';
  }

  // Is the page's own title showing? Its first <h1> rendered, or any rendered text equal to the name: a text node's
  // parent, or one of the three elements above it (a title written across a span or two).
  function titleShowing() {
    if (rendered(document.querySelector('h1'))) return 'the page\'s h1 shows';
    var want = fold(nav.gameName), walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false), t;
    while ((t = walk.nextNode())) {
      if (!/\S/.test(t.nodeValue) || (label && label.contains(t))) continue;
      var e = t.parentElement;
      if (!e || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE|TITLE)$/.test(e.tagName)) continue;
      for (var up = 0; e && e !== document.body && up < 4; up++, e = e.parentElement) {
        var text = e.textContent;
        if (text.length > nav.gameName.length + 24) break;
        if (fold(text) === want && rendered(e)) return 'the name is on the page';
      }
    }
    return '';
  }

  // The free margin right of the label's left edge: the smallest left edge of anything the page paints, by conflict()'s
  // own measure (a fixed box only where it is on screen, within the label's tallest band; anything in the flow at any
  // height), less the label's left edge and the logo's clear space.
  function freeWidth(left) {
    var bandBottom = LOGO.top + NAME.lines * NAME.size * NAME.line + LOGO.clear, nearest = window.innerWidth;
    function see(r, fixed) {
      if (r.width <= 0 || r.height <= 0 || r.right <= 0) return;
      if (fixed && !(r.top < bandBottom && r.bottom > 0)) return;
      if (r.left < nearest) nearest = r.left;
    }
    var all = document.body.getElementsByTagName('*');
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el === label || el === logo || (logo && logo.contains(el))) continue;
      var cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') continue;
      if (painted(el, cs)) see(el.getBoundingClientRect(), fixedish(el));
    }
    var walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var range = document.createRange(), t;
    while ((t = walk.nextNode())) {
      if (!/\S/.test(t.nodeValue) || (logo && logo.contains(t)) || (label && label.contains(t))) continue;
      var p = t.parentElement, cp = p && getComputedStyle(p);
      if (!cp || cp.visibility === 'hidden' || /^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(p.tagName)) continue;
      range.selectNodeContents(t);
      var rs = range.getClientRects(), fx = fixedish(p);
      for (var j = 0; j < rs.length; j++) see(rs[j], fx);
    }
    return Math.floor(nearest - left - LOGO.clear);
  }

  // Show the name, or hide it and say why. Called only from place(), after the logo is judged.
  function placeName(logoShown) {
    if (!label) return;
    var why = '';
    label.style.display = 'none';
    if (!logoShown) why = 'the logo is hidden';
    else if ((why = titleShowing())) { /* the page names itself */ }
    else {
      var left = LOGO.left + LOGO.size + LOGO.clear, free = freeWidth(left);
      label.setAttribute('data-room-px', String(free));
      if (free < NAME.min) why = 'no room (' + free + ' px free)';
      else {
        var body = getComputedStyle(document.body);
        label.style.fontFamily = body.fontFamily;
        label.style.color = body.color;
        label.style.maxWidth = free + 'px';
        label.style.visibility = 'hidden';
        label.style.display = 'block';
        var lines = Math.round(label.getBoundingClientRect().height / (NAME.size * NAME.line));
        if (lines > NAME.lines || label.scrollWidth > label.clientWidth + 1) {
          label.style.display = 'none';
          why = 'no room (' + free + ' px free: the name needs more than ' + NAME.lines + ' lines)';
        }
        label.style.visibility = '';
      }
    }
    nav.nameHiddenBy = why;
    label.setAttribute('data-hidden-by', why);
  }

  function place() {
    if (!logo) return;
    var fine = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
    var block = fine ? conflict() : 'coarse pointer';
    logo.style.display = block ? 'none' : 'block';
    logo.setAttribute('data-blocked-by', block ? (block.nodeType ? (block.tagName.toLowerCase() + (block.id ? '#' + block.id : '')
      + (block.className && typeof block.className === 'string' ? '.' + block.className.trim().split(/\s+/).join('.') : '')) : block) : '');
    try { placeName(!block); } catch (e) { if (label) { label.style.display = 'none'; nav.nameHiddenBy = 'error'; } }
  }

  var pending = 0;
  function later(ms) {
    if (pending) return;
    pending = setTimeout(function () { pending = 0; try { place(); } catch (e) { if (logo) logo.style.display = 'none'; if (label) label.style.display = 'none'; } }, ms);  // lock-ok: layout only, marks nothing
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
    if (nav.gameName) {
      // The name: plain text in the body's own font and colour, no background, never a link and never in the way of a click.
      label = document.createElement('div');
      label.className = 'maffs-site-name';
      label.setAttribute('aria-hidden', 'true');
      label.textContent = nav.gameName;
      label.style.cssText = 'position:fixed;left:' + (LOGO.left + LOGO.size + LOGO.clear) + 'px;top:' + LOGO.top + 'px;width:max-content;'
        + 'z-index:1001;display:none;margin:0;padding:0;background:none;pointer-events:none;overflow-wrap:normal;text-align:left;'
        + 'font-size:' + NAME.size + 'px;font-weight:' + NAME.weight + ';line-height:' + NAME.line + ';letter-spacing:normal';
      document.body.appendChild(label);
    }
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
    try { addLogo(); } catch (e) { if (logo) logo.style.display = 'none'; if (label) label.style.display = 'none'; }
  }
  nav.place = function () { place(); return logo ? logo.getAttribute('data-blocked-by') : 'no logo'; };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
