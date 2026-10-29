/* MaffsCardFilter: filters any container of cards by data attributes (contract ESSENTIALS-FILTER, Jon, 29 Oct 2026).
   Essentials is the first consumer; the portal migrates onto it later (after 9 Nov), not before.

   MaffsCardFilter.init({
     page: 'essentials',                      // goes on every event
     mount: '[data-card-filter]',             // where the bar goes
     cards: 'a.card',                         // each filterable card
     sections: 'section.topic',               // each group of cards; hidden when none of its cards shows
     groups: [{ param: 'topic', attr: 'data-topic', label: 'Topic',
                options: [{ key: 'number', label: 'Number' }, ...] }],   // chip rows; 'all' is added first
     search: true                             // a box over the card text
   });

   One reader of filter state: getState(). The bar, the URL (?topic=..&q=..), the count, the analytics and the
   card clicks all read it. The URL is read on load and written with replaceState (no reload, no history entry).
   A card whose attribute is missing is shown under All only. Events (the portal's shapes, mfg() in analytics.js):
   filter_applied, and game_card_clicked carrying the state. The Sheet keeps a fixed column list and drops unknown
   keys, so page and the whole state ride in filter_value ("v1|page=essentials;topic=..;su=..;sl=..;q=..;n=..").
   A second group (for example a calculator row) is one more entry in `groups`. */
(function () {
  'use strict';

  var API = {};

  API.init = function (cfg) {
    var mount = document.querySelector(cfg.mount);
    var cards = Array.prototype.slice.call(document.querySelectorAll(cfg.cards));
    var sections = Array.prototype.slice.call(document.querySelectorAll(cfg.sections || ''));
    if (!mount || !cards.length) return null;

    var state = { q: '' };
    cfg.groups.forEach(function (g) { state[g.param] = 'all'; });
    var ready = false;                       // load-time setup is not a user action: no event
    var els = { chips: {}, input: null, count: null, empty: null };

    function validKey(g, v) {
      return v === 'all' || g.options.some(function (o) { return o.key === v; });
    }

    // ── URL ──
    function readUrl() {
      var p = new URLSearchParams(location.search);
      cfg.groups.forEach(function (g) {
        var v = (p.get(g.param) || '').toLowerCase();
        state[g.param] = validKey(g, v) ? v : 'all';
      });
      state.q = (p.get('q') || '').slice(0, 80);
    }
    function writeUrl() {
      var p = new URLSearchParams(location.search);
      cfg.groups.forEach(function (g) {
        if (state[g.param] === 'all') p.delete(g.param); else p.set(g.param, state[g.param]);
      });
      var q = state.q.trim();
      if (q) p.set('q', q); else p.delete('q');
      var s = p.toString();
      try { history.replaceState(null, '', location.pathname + (s ? '?' + s : '') + location.hash); } catch (e) { /* sandbox */ }
    }

    // ── filtering ──
    function textOf(card) { return (card.textContent || '').replace(/\s+/g, ' ').toLowerCase(); }
    function matches(card) {
      for (var i = 0; i < cfg.groups.length; i++) {
        var g = cfg.groups[i];
        if (state[g.param] === 'all') continue;
        if (card.getAttribute(g.attr) !== state[g.param]) return false;
      }
      var q = state.q.trim().toLowerCase();
      return !q || q.split(/\s+/).every(function (w) { return textOf(card).indexOf(w) !== -1; });
    }
    function apply() {
      var n = 0;
      cards.forEach(function (c) {
        var show = matches(c);
        c.classList.toggle('cf-hidden', !show);
        if (show) n++;
      });
      sections.forEach(function (s) {
        s.classList.toggle('cf-hidden', !s.querySelector(cfg.cards + ':not(.cf-hidden)'));
      });
      els.count.textContent = n + (n === 1 ? ' game' : ' games');
      els.empty.hidden = n !== 0;
      cfg.groups.forEach(function (g) {
        Object.keys(els.chips[g.param]).forEach(function (k) {
          var on = k === state[g.param];
          els.chips[g.param][k].setAttribute('aria-pressed', on ? 'true' : 'false');
          els.chips[g.param][k].classList.toggle('cf-on', on);
        });
      });
      if (els.input.value !== state.q) els.input.value = state.q;
      writeUrl();
      return n;
    }

    // ── the only reader of filter state ──
    function getState() {
      var q = state.q.trim().toLowerCase();
      var out = { search_used: q.length > 0, search_length: q.length, search_query: q.slice(0, 40),
                  result_count: parseInt(els.count.textContent, 10) || 0 };
      cfg.groups.forEach(function (g) { out[g.param] = state[g.param]; });
      return out;
    }
    function filterValue(st) {
      var v = 'v1|page=' + cfg.page;
      cfg.groups.forEach(function (g) { v += ';' + g.param + '=' + st[g.param]; });
      return v + ';su=' + (st.search_used ? 1 : 0) + ';sl=' + st.search_length +
             ';q=' + String(st.search_query).replace(/[;=|]/g, '') + ';n=' + st.result_count;
    }
    function report(trigger) {
      if (!ready || typeof window.mfg !== 'function') return;
      var st = getState();
      var p = { page: cfg.page, trigger: trigger, filter_type: trigger, filter_value: filterValue(st) };
      Object.keys(st).forEach(function (k) { p[k] = st[k]; });
      window.mfg('filter_applied', p);
    }

    // ── bar ──
    function el(tag, cls, text) {
      var e = document.createElement(tag);
      if (cls) e.className = cls;
      if (text) e.textContent = text;
      return e;
    }
    var bar = el('div', 'cf-bar');
    bar.setAttribute('role', 'search');
    cfg.groups.forEach(function (g) {
      var row = el('div', 'cf-chips');
      row.setAttribute('role', 'group');
      row.setAttribute('aria-label', g.label);
      els.chips[g.param] = {};
      [{ key: 'all', label: 'All' }].concat(g.options).forEach(function (o) {
        var b = el('button', 'cf-chip', o.label);
        b.type = 'button';
        b.setAttribute('data-cf-group', g.param);
        b.setAttribute('data-cf-key', o.key);
        els.chips[g.param][o.key] = b;
        row.appendChild(b);
      });
      bar.appendChild(row);
    });
    var line = el('div', 'cf-searchline');
    var input = el('input', 'cf-search');
    input.type = 'search';
    input.setAttribute('aria-label', 'Search games');
    input.placeholder = 'Search games';
    input.autocomplete = 'off';
    input.maxLength = 80;
    els.input = input;
    els.count = el('span', 'cf-count');
    els.count.setAttribute('aria-live', 'polite');
    line.appendChild(input);
    line.appendChild(els.count);
    bar.appendChild(line);
    var empty = el('div', 'cf-empty');
    empty.hidden = true;
    var msg = el('p', 'cf-empty-msg', 'No games match. Try fewer words, or clear the filters.');
    var clear = el('button', 'cf-clear', 'Clear filters');
    clear.type = 'button';
    empty.appendChild(msg);
    empty.appendChild(clear);
    els.empty = empty;
    mount.appendChild(bar);
    mount.appendChild(empty);

    // After a change the results start just under the sticky bar (the page may have got shorter under the reader).
    function sizeBar() { document.documentElement.style.setProperty('--cf-bar-h', bar.offsetHeight + 'px'); }
    function showResults() {
      sizeBar();
      var first = null;
      for (var i = 0; i < sections.length; i++) if (!sections[i].classList.contains('cf-hidden')) { first = sections[i]; break; }
      var target = first || empty;
      var y = target.getBoundingClientRect().top + window.pageYOffset - bar.offsetHeight - 8;
      if (Math.abs(window.pageYOffset - y) > 4) window.scrollTo(0, Math.max(0, y));
    }

    // ── events ──
    bar.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.cf-chip') : null;
      if (!b) return;
      state[b.getAttribute('data-cf-group')] = b.getAttribute('data-cf-key');
      apply();
      report(b.getAttribute('data-cf-group'));
      showResults();
    });
    clear.addEventListener('click', function () {
      cfg.groups.forEach(function (g) { state[g.param] = 'all'; });
      state.q = '';
      apply();
      report('clear');
      showResults();
    });
    var timer = null, lastSent = '';
    els.input.addEventListener('input', function () {
      state.q = els.input.value;
      apply();
      clearTimeout(timer);
      timer = setTimeout(function () {                 // once typing stops, and only when the query moved
        var q = state.q.trim().toLowerCase();
        if (q === lastSent) return;
        lastSent = q;
        report('search');
        showResults();
      }, 1000);
    });
    // Card clicks carry the state (one delegated listener, as on the portal). Never preventDefault or delay.
    document.addEventListener('click', function (e) {
      var card = e.target && e.target.closest ? e.target.closest(cfg.cards) : null;
      if (!card || cards.indexOf(card) === -1 || typeof window.mfg !== 'function') return;
      var st = getState();
      var topic = card.getAttribute('data-topic') || '';
      var p = { page: cfg.page, game_slug: card.getAttribute('data-slug') || '', section: topic,
                filter_type: topic, filter_value: filterValue(st) };
      Object.keys(st).forEach(function (k) { p[k] = st[k]; });
      window.mfg('game_card_clicked', p);
    }, true);
    window.addEventListener('resize', sizeBar);

    readUrl();
    apply();
    sizeBar();
    var filtered = cfg.groups.some(function (g) { return state[g.param] !== 'all'; }) || state.q.trim();
    ready = true;
    // A link that opens the page pre-filtered lands on the bar, so the results are what the reader sees.
    if (filtered) setTimeout(function () { bar.scrollIntoView(); }, 0);
    API.getState = getState;
    return API;
  };

  window.MaffsCardFilter = API;
})();
