/* "N questions answered since September" (contract ANSWER-COUNTS, 23 Oct 2026; canon 7.5.5).

   A figure on a page is a claim, so it is never typed by hand: it comes from /data/answer-counts.json, written once a
   day by .github/workflows/answer-counts.yml from the counts Apps Script (docs/apps-script-counts.js), and from that
   script's live address. One shared file fills two kinds of mount; no game has code of its own for it:

     [data-maffs-start-note]       a game's start screen (canon 7.5.4): that game's count, from 1,000
     [data-maffs-answer-total]     the homepage: the total across every game and room, from 10,000, refreshed every
                                   minute while the tab is visible

   The daily file's figure shows at once (nothing shifts, nothing waits on a network call to a slow service); the live
   address is then fetched and, if its figure is higher, the number counts up to it (never down; no animation under
   prefers-reduced-motion). A source whose as_of is more than 7 days old is ignored, a figure below its threshold shows
   nothing, and so does a page where nothing loads. A page with no mount (52dle, Equatle, Estimation Golf, Factor
   Theorem have no start screen) simply shows nothing: that is correct, not a failure.

   The text inherits the page's colour and font and adds no opacity: scripts/check-answer-count.py measures its contrast
   on every game (4.5:1), and teacher-invite.js found that a faded line falls below it on already-muted pages.
   The live address is fetched on maffsgames.co.uk only, as analytics.js sends events from there only.

   scripts/check-answer-count.py --selftest holds this file to the cases in the contract. */
(function () {
  'use strict';

  var DATA_URL = '/data/answer-counts.json';
  var LIVE_URL = 'https://script.google.com/macros/s/AKfycbxvtM7Y5jtL7flZozfFUEoZZalNHieP44vK6rB4juUG5yPgQf5hfb8tOlgetoEtogZl8w/exec';
  var GAME_MIN = 1000;
  var TOTAL_MIN = 10000;
  var STALE_MS = 7 * 24 * 3600 * 1000;
  var POLL_MS = 60000;
  var ANIMATE_MS = 900;

  function format(n) {
    return String(Math.floor(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  function line(n) { return format(n) + ' questions answered since September'; }

  function whole(v) { return typeof v === 'number' && isFinite(v) && v >= 0 && Math.floor(v) === v; }

  // The figure a source holds for this page, or null when the source cannot be trusted: not an object of the right
  // shape, as_of missing, unreadable or more than 7 days old, or no whole number for this page.
  function figure(src, slug, total, now) {
    if (!src || typeof src !== 'object' || typeof src.as_of !== 'string') return null;
    var t = Date.parse(src.as_of);
    if (!isFinite(t) || now - t > STALE_MS) return null;
    var v = total ? src.total : (src.games && typeof src.games === 'object' ? src.games[slug] : undefined);
    if (v === undefined && !total) v = 0;
    return whole(v) ? v : null;
  }

  function style(doc) {
    if (doc.getElementById('maffsAnswerCountStyle')) return;
    var s = doc.createElement('style');
    s.id = 'maffsAnswerCountStyle';
    s.textContent = '.maffs-start-note:not(:empty){margin:.8rem 0 0;font-size:.82rem;line-height:1.4;' +
      'text-align:center;font-family:inherit;color:inherit}';
    (doc.head || doc.documentElement).appendChild(s);
  }

  // One mount: what it shows, what it may show, and how it moves to a higher figure.
  function Mount(el, min, o) {
    this.el = el; this.min = min; this.o = o;
    this.shown = 0;          // the figure on screen (or being counted up to)
    this.display = 0;
    this.job = 0;
  }
  Mount.prototype.set = function (n) {
    this.display = n;
    this.el.textContent = line(n);
    this.el.hidden = false;
    this.el.setAttribute('data-maffs-count', String(n));
  };
  Mount.prototype.offer = function (v) {
    if (v === null || v < this.min || v <= this.shown) return;     // below threshold, or not higher: ignored
    var from = this.display, self = this, job = ++this.job;
    this.shown = v;
    if (!from || this.o.reduced || !this.o.raf) { this.set(v); return; }
    var t0 = null;
    var step = function (ts) {
      if (job !== self.job) return;                                  // a newer figure took over
      if (t0 === null) t0 = ts;
      var k = Math.min(1, (ts - t0) / ANIMATE_MS);
      var e = 1 - Math.pow(1 - k, 3);
      self.set(k >= 1 ? v : Math.round(from + (v - from) * e));
      if (k < 1) self.o.raf(step);
    };
    self.o.raf(step);
  };

  // run(opts): everything the page does, with its dependencies injectable so the selftest needs no network.
  //   doc, slug, get(url) -> Promise of a parsed object, now() -> ms, live (bool), reduced (bool), raf(fn),
  //   visible() -> bool, setInterval/clearInterval
  function run(opts) {
    var doc = opts.doc, now = opts.now || Date.now;
    var mounts = [];
    var starts = doc.querySelectorAll('[data-maffs-start-note]');
    for (var i = 0; i < starts.length; i++) mounts.push({ m: new Mount(starts[i], GAME_MIN, opts), total: false });
    var totals = doc.querySelectorAll('[data-maffs-answer-total]');
    for (var j = 0; j < totals.length; j++) mounts.push({ m: new Mount(totals[j], TOTAL_MIN, opts), total: true });
    if (!mounts.length) return Promise.resolve();                  // no mount: nothing to show, and no error
    if (starts.length) style(doc);

    function apply(src) {
      var t = now();
      mounts.forEach(function (x) { x.m.offer(figure(src, opts.slug, x.total, t)); });
    }
    function safe(url) {
      try { return Promise.resolve(opts.get(url)).catch(function () { return null; }); } catch (e) { return Promise.resolve(null); }
    }
    function live() { return opts.live ? safe(LIVE_URL).then(apply) : Promise.resolve(); }

    return safe(DATA_URL).then(apply).then(live).then(function () {
      if (totals.length && opts.live && opts.setInterval) {
        opts.setInterval(function () { if (!opts.visible || opts.visible()) live(); }, POLL_MS);
      }
    });
  }

  function xhr(url) {
    return new Promise(function (resolve, reject) {
      var x = new XMLHttpRequest();
      x.open('GET', url);
      x.timeout = 8000;
      x.onload = function () {
        if (x.status !== 200) { reject(new Error('status ' + x.status)); return; }
        try { resolve(JSON.parse(x.responseText)); } catch (e) { reject(e); }
      };
      x.onerror = x.ontimeout = function () { reject(new Error('network')); };
      x.send();
    });
  }

  window.MaffsAnswerCount = { run: run, figure: figure, format: format, GAME_MIN: GAME_MIN, TOTAL_MIN: TOTAL_MIN, STALE_MS: STALE_MS };

  function go() {
    var m = location.pathname.match(/\/games\/([a-z0-9-]+)\//);
    var host = location.hostname;
    var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    try {
      run({
        doc: document, slug: m ? m[1] : '', get: xhr, now: Date.now, reduced: reduced,
        live: host === 'maffsgames.co.uk' || host === 'www.maffsgames.co.uk',
        raf: function (f) { window.requestAnimationFrame(f); },
        visible: function () { return document.visibilityState !== 'hidden'; },
        setInterval: function (f, ms) { window.setInterval(f, ms); }
      });
    } catch (e) { /* a figure is decoration: never let it break a page */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
