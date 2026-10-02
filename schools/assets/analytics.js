// ============================================================
//  MaffsGames Dual Analytics — GA4 + Google Sheets
// ============================================================
//  Include in every game via:
//    <script src="../../schools/assets/analytics.js"></script>
//
//  Usage:
//    mfg('game_started', { game_slug: 'fermi-lab', level: 'gcse' });
//    mfg('question_answered', { game_slug: 'fermi-lab', level: 'gcse', correct: true, question_index: 3 });
//
//  Sends to both GA4 (gtag) and Google Sheets (fetch POST).
//  Sheets endpoint URL set below — update after deploying Apps Script.

(function() {
  'use strict';

  // ── CONFIGURE ──
  // Replace with your deployed Apps Script Web App URL
  var ANALYTICS_ENDPOINT = 'https://script.google.com/macros/s/AKfycbzKUxT4TpL2kgFNFBzVEw0ALv3A7qHndNjgIdBoSedtl8T17O2KV7TLrtuVCrYmAkVR/exec';
  var SHEETS_ENABLED = true;

  // ── STATE ──
  window._mfgCompleted = false;   // set by game_completed, guards abandon
  window._mfgActive = false;      // true only between game_started and game_completed
  window._mfgAbandonSent = false; // abandon is once-per-session, not once-per-tab-away
  window._mfgQuestionIndex = 0;
  var _seq = 0;                   // monotonic, breaks ties when events race

  // ── MAIN FUNCTION ──
  window.mfg = function(eventName, params) {
    params = params || {};

    // ── Production only ──────────────────────────────────────────────
    // Local test runs (python -m http.server on 127.0.0.1) load this same
    // file and wrote straight into the production GA4 property and Events
    // sheet. serve-stubbed.py was the only defence and has been missed twice,
    // so the gate lives here, where every event already passes.
    var host = location.hostname;
    if (host !== 'maffsgames.co.uk' && host !== 'www.maffsgames.co.uk') return;

    // ── Abandon hygiene ──────────────────────────────────────────────
    // Games register their own visibilitychange/beforeunload handlers on top
    // of the one below, so a single tab-away can fire this two or three times.
    // mfg() is the only shared choke point, so the rules live here rather than
    // in 94 game files. Drop the event outright when it is not real:
    //   - no game ever started (portal page, or player left before pressing Start)
    //   - the game was already completed
    //   - an abandon was already recorded for this session
    if (eventName === 'game_abandoned') {
      if (!window._mfgActive || window._mfgCompleted || window._mfgAbandonSent) return;
      window._mfgAbandonSent = true;
      window._mfgActive = false;
      // Backfill context if the caller omitted it
      if (!params.game_slug) params.game_slug = window._mfgSlug || '';
      if (!params.level) params.level = window._mfgLevel || '';
      if (!params.question_index) params.question_index = window._mfgQuestionIndex || 0;
    }

    // ── Browsing is not starting ─────────────────────────────────────
    // Some games (e.g. estimation-golf) call startGame() straight from their
    // level buttons, so clicking through tiers logs a start per click and
    // craters the completion rate. Re-starting the SAME game with nothing
    // played in between is a switch or a restart, not a new session.
    // The slug check matters: a start for a different game is always real.
    if (eventName === 'game_started' && window._mfgActive &&
        !window._mfgQuestionIndex &&
        (params.game_slug || '') === (window._mfgSlug || '')) {
      eventName = (params.level || '') !== (window._mfgLevel || '')
        ? 'level_selected'
        : 'game_restarted';
    }

    // Send to GA4 (if gtag exists)
    if (typeof gtag === 'function') {
      gtag('event', eventName, params);
    }

    // Send to Google Sheets
    if (SHEETS_ENABLED && ANALYTICS_ENDPOINT) {
      // Events are fire-and-forget over the network and regularly arrive out of
      // order, but the sheet timestamps on arrival — so a completion can land
      // before the answer that caused it. Stamp the event client-side and carry
      // a sequence number so true order is always recoverable by sorting.
      var payload = Object.assign({
        event: eventName,
        client_ts: new Date().toISOString(),
        seq: ++_seq
      }, params);
      try {
        // Use sendBeacon for abandon events (more reliable on page close)
        if (eventName === 'game_abandoned' && navigator.sendBeacon) {
          navigator.sendBeacon(ANALYTICS_ENDPOINT, JSON.stringify(payload));
        } else {
          fetch(ANALYTICS_ENDPOINT, {
            method: 'POST',
            mode: 'no-cors',
            body: JSON.stringify(payload),
            keepalive: true  // survives page navigation
          }).catch(function() {}); // silent fail — analytics should never break the game
        }
      } catch (e) {
        // Silent fail
      }
    }

    // Auto-capture slug/level from game_started for abandon tracking
    if (eventName === 'game_started') {
      window._mfgSlug = params.game_slug || '';
      window._mfgLevel = params.level || '';
      window._mfgCompleted = false;
      window._mfgActive = true;
      window._mfgAbandonSent = false;
      window._mfgQuestionIndex = 0;
    }

    // Track level on a switch too, so a later abandon reports the right tier
    if (eventName === 'level_selected' && params.level) {
      window._mfgLevel = params.level;
    }

    // Track question index for abandon context
    if (eventName === 'question_answered' && params.question_index) {
      window._mfgQuestionIndex = params.question_index;
    }

    // Track completion state for abandon guard
    if (eventName === 'game_completed') {
      window._mfgCompleted = true;
      window._mfgActive = false;
    }
  };

  // ── ABANDON TRACKING ──
  // Uses visibilitychange (reliable on mobile) with sendBeacon fallback.
  // Each game sets window._mfgSlug and window._mfgLevel on start.
  // The guards in mfg() decide whether this is a real abandon — do not
  // duplicate those checks here, or the two will drift apart.
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
      mfg('game_abandoned', {
        game_slug: window._mfgSlug || '',
        level: window._mfgLevel || '',
        question_index: window._mfgQuestionIndex || 0
      });
    }
  });

  // ── SECTION CLICKS (1 Oct 2026) ──
  // One listener for every labelled feature section, on any page that loads this file.
  // To track a section, label it in the markup; there is no per-section code:
  //   <div data-mfg-section="escape-rooms">                   the section
  //     <a data-mfg-item="hamster-heist" href="...">            each element to count
  //     <button data-mfg-item="show-all" aria-expanded="false">  a show/hide toggle
  // A click on a labelled item fires section_clicked: section, item, position (1-based
  // among the section's labelled items) and action. A link is "open-link"; a toggle
  // (aria-expanded) is "toggle-open" and fires only when opening, as fact_expanded does.
  // Capture phase, so the toggle is read before the page's own handler flips it.
  // Never preventDefault or delay: mfg() posts with keepalive, so the event survives
  // the navigation. The Sheet keeps a fixed column list, so the fields ride in columns
  // it already has: item -> game_slug, section -> filter_type, and
  // "v1|pos=N;action=X" -> filter_value (the portal's existing v1| format).
  // game_card_clicked and the fact_* events are separate and unchanged.
  document.addEventListener('click', function(e) {
    var el = e.target && e.target.closest ? e.target.closest('[data-mfg-item]') : null;
    if (!el) return;
    var sec = el.closest('[data-mfg-section]');
    if (!sec) return;
    var action;
    if (el.hasAttribute('aria-expanded')) {
      if (el.getAttribute('aria-expanded') === 'true') return;   // closing: not counted
      action = 'toggle-open';
    } else if (el.tagName === 'A' && el.getAttribute('href')) {
      action = 'open-link';
    } else {
      return;
    }
    var items = sec.querySelectorAll('[data-mfg-item]');
    var position = Array.prototype.indexOf.call(items, el) + 1;
    var section = sec.getAttribute('data-mfg-section');
    var item = el.getAttribute('data-mfg-item');
    mfg('section_clicked', {
      section: section,
      item: item,
      position: position,
      action: action,
      game_slug: item,
      filter_type: section,
      filter_value: 'v1|pos=' + position + ';action=' + action
    });
  }, true);

})();
