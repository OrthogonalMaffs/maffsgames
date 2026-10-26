/* "N questions answered since September" (contract ANSWER-COUNTS, 23 Oct 2026; canon 7.5.5).

   A figure on a page is a claim, so it is never typed by hand: it comes from /schools/assets/answer-counts.json, written once a
   day by .github/workflows/answer-counts.yml from the counts Apps Script (docs/apps-script-counts.js), and from that
   script's live address. One shared file fills two kinds of mount; no game has code of its own for it:

     [data-maffs-start-note]       a game's start screen (canon 7.5.4): that game's count, from 1,000
     [data-maffs-answer-total]     the homepage: the total across every game and room, from 10,000, refreshed every
                                   minute while the tab is visible

   The daily file's figure shows at once (nothing shifts, nothing waits on a network call to a slow service). A GAME page
   shows that figure and nothing else: it never calls the live address (Jon, 23 Oct 2026: the counts script and the
   analytics script run as Jon and share his concurrent-execution limit, so a class opening games together must not be
   able to crowd out event logging). Only the HOMEPAGE fetches the live address, once on load and then every minute while
   the tab is visible, for 10 minutes at most, and its number counts up to a higher figure (never down; no animation
   under prefers-reduced-motion). The homepage shows the figure as a headline, and "Updated every 5 minutes" (the counts
   script's refresh) under it only while the figure on screen is the live one: never from the daily file, and removed
   again if a later refresh fails. The homepage remembers the last live figure it showed for the rest of the browser session
   (sessionStorage on the viewer's own device, Jon's ruling of 26 Oct 2026): a refresh starts from that figure, not from the
   daily file's, so the count-up no longer replays the whole climb. It starts there only when the stored figure has the same
   "since", is at least the file's figure and no more than the live one; otherwise from the file's figure, as before. A
   source whose as_of (an ISO time with Z or +hh:mm, parsed by Date.parse) is more than 7 days old is ignored, a figure below its threshold
   shows nothing, and so does a page where nothing loads. A page with no mount (52dle, Equatle, Estimation Golf, Factor
   Theorem have no start screen) simply shows nothing: that is correct, not a failure.

   The text inherits the page's colour and font and adds no opacity: scripts/check-answer-count.py measures its contrast
   on every game (4.5:1), and teacher-invite.js found that a faded line falls below it on already-muted pages.
   The live address is fetched on maffsgames.co.uk only, as analytics.js sends events from there only.

   scripts/check-answer-count.py --selftest holds this file to the cases in the contract. */
(function () {
  'use strict';

  var DATA_URL = '/schools/assets/answer-counts.json';
  var LIVE_URL = 'https://script.google.com/macros/s/AKfycbxvtM7Y5jtL7flZozfFUEoZZalNHieP44vK6rB4juUG5yPgQf5hfb8tOlgetoEtogZl8w/exec';
  var GAME_MIN = 1000;
  var TOTAL_MIN = 10000;
  var STALE_MS = 7 * 24 * 3600 * 1000;
  var POLL_MS = 60000;
  var POLL_MAX_MS = 10 * 60 * 1000;   // a homepage left open in a classroom must not poll all day
  var ANIMATE_MS = 900;
  var MEMORY_KEY = 'maffsAnswerCount';   // sessionStorage: {n, since}, the last live figure the homepage showed

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
  // Put the figure on screen at once, with no animation and without counting from the previous one.
  Mount.prototype.reset = function (n) { this.job++; this.shown = n; this.set(n); };
  Mount.prototype.set = function (n) {
    this.display = n;
    if (this.el.hasAttribute('data-maffs-answer-total')) {
      // the homepage headline: the number and its label are separate spans (the page styles them); textContent still
      // reads "N questions answered since September"
      var num = this.el.querySelector('.ac-num');
      if (!num) {
        this.el.innerHTML = '<span class="ac-num"></span> <span class="ac-label">questions answered since September</span>';
        num = this.el.querySelector('.ac-num');
      }
      num.textContent = format(n);
    } else {
      this.el.textContent = line(n);
    }
    this.el.setAttribute('data-maffs-count', String(n));
    this.el.hidden = false;
  };
  // "Updated every 5 minutes" (the counts script refreshes every 5 minutes): present only while the figure on screen is
  // the live one. A sibling of the block, so a hidden block never has it and the block's text is unchanged.
  Mount.prototype.updated = function (on) {
    var cur = this.el.nextElementSibling;
    cur = cur && cur.hasAttribute('data-maffs-answer-updated') ? cur : null;
    if (on && !cur) {
      var d = this.el.ownerDocument.createElement('div');
      d.className = 'answer-updated';
      d.setAttribute('data-maffs-answer-updated', '');
      d.textContent = 'Updated every 5 minutes';
      this.el.parentNode.insertBefore(d, this.el.nextSibling);
    } else if (!on && cur) {
      cur.parentNode.removeChild(cur);
    }
  };
  // Called with each live response: the line stays only when the live figure is valid, over the threshold and the
  // one on screen (a lower live figure leaves the file's higher one showing, which is not the live figure).
  Mount.prototype.live = function (v) {
    var ok = v !== null && v >= this.min && v >= this.shown;
    this.updated(ok);
  };
  // `done(v)` is called once v is on screen (the end of the count-up, or at once when there is none).
  Mount.prototype.offer = function (v, done) {
    if (v === null || v < this.min || v <= this.shown) return;     // below threshold, or not higher: ignored
    var from = this.display, self = this, job = ++this.job;
    this.shown = v;
    if (!from || this.o.reduced || !this.o.raf) { this.set(v); if (done) done(v); return; }
    var t0 = null;
    var step = function (ts) {
      if (job !== self.job) return;                                  // a newer figure took over
      if (t0 === null) t0 = ts;
      var k = Math.min(1, (ts - t0) / ANIMATE_MS);
      var e = 1 - Math.pow(1 - k, 3);
      self.set(k >= 1 ? v : Math.round(from + (v - from) * e));
      if (k < 1) self.o.raf(step); else if (done) done(v);
    };
    self.o.raf(step);
  };

  // run(opts): everything the page does, with its dependencies injectable so the selftest needs no network.
  //   doc, slug, get(url) -> Promise of a parsed object, now() -> ms, live (bool), reduced (bool), raf(fn),
  //   visible() -> bool, setInterval(fn, ms) -> id, clearInterval(id),
  //   memory {read() -> {n, since} or null, write(n, since)}: the homepage's session memory (absent: none)
  function run(opts) {
    var doc = opts.doc, now = opts.now || Date.now;
    var mounts = [];
    var starts = doc.querySelectorAll('[data-maffs-start-note]');
    for (var i = 0; i < starts.length; i++) mounts.push({ m: new Mount(starts[i], GAME_MIN, opts), total: false });
    var totals = doc.querySelectorAll('[data-maffs-answer-total]');
    for (var j = 0; j < totals.length; j++) mounts.push({ m: new Mount(totals[j], TOTAL_MIN, opts), total: true });
    if (!mounts.length) return Promise.resolve();                  // no mount: nothing to show, and no error
    if (starts.length) style(doc);

    // The homepage's memory of the last live figure it showed. Every read and write is guarded: where storage is blocked or
    // throws, the page behaves exactly as it did without a memory.
    var memory = opts.memory || null;
    function recall() {
      try {
        var m = memory ? memory.read() : null;
        return m && typeof m === 'object' && whole(m.n) && typeof m.since === 'string' ? m : null;
      } catch (e) { return null; }
    }
    function remember(n, since) {
      try { if (memory) memory.write(n, since); } catch (e) { /* storage unavailable: nothing to remember with */ }
    }

    function apply(src, isLive) {
      var t = now();
      mounts.forEach(function (x) {
        var v = figure(src, opts.slug, x.total, t);
        if (x.total && memory) {
          if (!isLive) {
            // The daily file: start from the last live figure shown this session when it is the same school year's ("since") and
            // at least the file's figure; the live figure (next) decides whether it was not too high.
            x.file = v;
            var m = v !== null ? recall() : null;
            if (m && typeof src.since === 'string' && m.since === src.since && m.n >= v && m.n >= x.m.min) { x.stored = m; x.m.offer(m.n); }
            else x.m.offer(v);
            return;
          }
          if (x.stored && v !== null && (x.stored.n > v || x.stored.since !== src.since)) {
            x.stored = null;               // above the live figure, or from another year: not a starting point after all
            x.m.reset(x.file);             // back to the file's figure, then up to the live one as before
          }
          x.m.offer(v, function (n) { if (typeof src.since === 'string') remember(n, src.since); });
          x.m.live(v);
          return;
        }
        x.m.offer(v);
        if (isLive && x.total) x.m.live(v);
      });
    }
    function safe(url) {
      try { return Promise.resolve(opts.get(url)).catch(function () { return null; }); } catch (e) { return Promise.resolve(null); }
    }
    // Only the homepage (a total mount) ever calls the live address.
    var useLive = opts.live && totals.length > 0;
    function live() { return useLive ? safe(LIVE_URL).then(function (src) { apply(src, true); }) : Promise.resolve(); }

    return safe(DATA_URL).then(function (src) { apply(src, false); }).then(live).then(function () {
      if (useLive && opts.setInterval) {
        var t0 = now();
        var id = opts.setInterval(function () {
          if (now() - t0 >= POLL_MAX_MS) { if (opts.clearInterval) opts.clearInterval(id); return; }   // stop after 10 minutes
          if (!opts.visible || opts.visible()) live();
        }, POLL_MS);
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

  window.MaffsAnswerCount = { run: run, figure: figure, format: format, GAME_MIN: GAME_MIN, TOTAL_MIN: TOTAL_MIN, STALE_MS: STALE_MS, POLL_MAX_MS: POLL_MAX_MS, MEMORY_KEY: MEMORY_KEY };

  // The session memory on this device: sessionStorage, nothing else, never sent anywhere. Reading or writing it can throw
  // (blocked storage, a private window, a full quota); every failure is swallowed.
  var sessionMemory = {
    read: function () {
      try { var raw = window.sessionStorage.getItem(MEMORY_KEY); return raw ? JSON.parse(raw) : null; } catch (e) { return null; }
    },
    write: function (n, since) {
      try { window.sessionStorage.setItem(MEMORY_KEY, JSON.stringify({ n: n, since: since })); } catch (e) { /* blocked */ }
    }
  };

  function go() {
    var m = location.pathname.match(/\/games\/([a-z0-9-]+)\//);
    var host = location.hostname;
    var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    try {
      run({
        doc: document, slug: m ? m[1] : '', get: xhr, now: Date.now, reduced: reduced, memory: sessionMemory,
        live: host === 'maffsgames.co.uk' || host === 'www.maffsgames.co.uk',
        raf: function (f) { window.requestAnimationFrame(f); },
        visible: function () { return document.visibilityState !== 'hidden'; },
        setInterval: function (f, ms) { return window.setInterval(f, ms); },
        clearInterval: function (id) { window.clearInterval(id); }
      });
    } catch (e) { /* a figure is decoration: never let it break a page */ }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
