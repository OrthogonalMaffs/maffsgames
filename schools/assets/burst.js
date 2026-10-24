/* MaffsBurst: run a mapped game as a short "burst" launched from The 6 P's (contract BURST, 24 Oct 2026; canon 7.5.6).
 *
 * The 6 P's sends a student into a real game for a few questions and takes them back. The link names the burst:
 *
 *     /games/<slug>/?burst=5&from=six-ps&topic=<id>[&level=<key>][&mode=<name>]
 *
 *   burst  1 to 10, whole digits: how many answers the burst lasts.
 *   from   exactly "six-ps".
 *   topic  [a-z0-9-], 1 to 40 characters: the topic id The 6 P's will be told about.
 *   level  the game's own ?level= (MaffsLevel reads it; this file does not).
 *   mode   optional: the start screen's [data-mode="<name>"] button is pressed once after load (the stage or mode
 *          a staged game opens at). Nothing else on the page is pressed.
 *
 * Without all three of burst, from and topic, and valid, this file does nothing at all: it wraps nothing, adds
 * nothing to the page and presses nothing. MaffsBurst.active() is then false.
 *
 * When active it wraps the global mfg() (so it must load after analytics.js). Every call still goes through to the
 * original, unchanged and in order; a question_answered is also counted (right when its `correct` is true). After the
 * Nth answer a fixed bar at the foot of the screen says "That's N. Back to The 6 P's (R of N)" and links to
 *
 *     /the-6-ps/?done=<topic>&r=<right>&n=<N>
 *
 * The game is not stopped or changed: the student can read the feedback first, and the page keeps room for the bar.
 * The counts are frozen at the Nth answer.
 *
 * Leaderboards: a burst session never writes a score. firebase-leaderboard.js's submitScore and score-history.js's
 * record() both return at once when MaffsBurst.active(). A game that keeps its own best in localStorage is not
 * reached by that; they are listed in the handover.
 *
 * Privacy: no new data. The return link carries a topic id and a score; nothing is stored or sent here.
 */
(function (global) {
  'use strict';

  var TOPIC = /^[a-z0-9][a-z0-9-]{0,39}$/;
  var MODE = /^[a-z0-9][a-z0-9-]{0,29}$/;

  function read() {
    var q;
    try { q = new URLSearchParams(global.location.search); } catch (e) { return null; }
    var b = q.get('burst'), from = q.get('from'), topic = q.get('topic'), mode = q.get('mode');
    if (b === null || !/^\d{1,2}$/.test(b)) return null;
    var n = parseInt(b, 10);
    if (n < 1 || n > 10) return null;
    if (from !== 'six-ps') return null;
    if (topic === null || !TOPIC.test(topic)) return null;
    return { n: n, topic: topic, mode: (mode !== null && MODE.test(mode)) ? mode : null };
  }

  var cfg = read();
  global.MaffsBurst = { active: function () { return !!cfg; } };
  if (!cfg) return;

  var answered = 0, right = 0, shown = false;

  function bar() {
    var href = '/the-6-ps/?done=' + encodeURIComponent(cfg.topic) + '&r=' + right + '&n=' + cfg.n;
    var css = document.createElement('style');
    css.textContent =
      '#mfg-burst-bar{position:fixed;left:0;right:0;bottom:0;z-index:9000;box-sizing:border-box;display:flex;flex-wrap:wrap;' +
      'align-items:center;justify-content:center;gap:8px 16px;padding:10px 16px calc(10px + env(safe-area-inset-bottom,0px));' +
      'background:#1a2744;color:#fff;font:600 16px/1.3 \'Outfit\',system-ui,sans-serif;border-top:3px solid #f5a524;' +
      'box-shadow:0 -4px 16px rgba(0,0,0,.25)}' +
      '#mfg-burst-bar a{display:inline-flex;align-items:center;justify-content:center;min-height:44px;min-width:44px;padding:0 18px;' +
      'border-radius:10px;background:#fff;color:#1a2744;text-decoration:none;font-weight:700}' +
      '#mfg-burst-bar a:focus-visible{outline:3px solid #f5a524;outline-offset:2px}' +
      '@media print{#mfg-burst-bar{display:none}}';
    document.head.appendChild(css);
    var el = document.createElement('div');
    el.id = 'mfg-burst-bar';
    el.setAttribute('role', 'status');
    var msg = document.createElement('span');
    msg.textContent = "That's " + cfg.n + '.';
    var a = document.createElement('a');
    a.href = href;
    a.textContent = "Back to The 6 P's (" + right + ' of ' + cfg.n + ')';
    el.appendChild(msg);
    el.appendChild(a);
    document.body.appendChild(el);
    // keep the foot of the page clear of the bar, so the game's own feedback and Next can still be reached
    var pad = parseFloat(global.getComputedStyle(document.body).paddingBottom) || 0;
    document.body.style.paddingBottom = (pad + el.offsetHeight) + 'px';
  }

  function count(p) {
    if (shown) return;
    answered++;
    if (p && p.correct === true) right++;
    if (answered >= cfg.n) { shown = true; bar(); }
  }

  function wrap() {
    var orig = global.mfg;
    if (typeof orig !== 'function' || orig.__maffsBurst) return;
    var w = function (name, params) {
      var r = orig.apply(this, arguments);
      try { if (name === 'question_answered') count(params); } catch (e) {}
      return r;
    };
    w.__maffsBurst = true;
    global.mfg = w;
  }
  wrap();

  // The stage or mode a staged game opens at: press the start screen's own button once, and nothing else.
  function openMode() {
    if (!cfg.mode) return;
    var tries = 0;
    (function look() {
      var btns = document.querySelectorAll('[data-mode]');
      for (var i = 0; i < btns.length; i++) {
        var b = btns[i];
        if (b.getAttribute('data-mode') === cfg.mode && !b.disabled && b.offsetParent !== null) {
          global.MaffsBurst.modePressed = true;
          b.click();
          return;
        }
      }
      if (++tries < 30) global.setTimeout(look, 100);
    })();
  }
  if (document.readyState === 'complete') global.setTimeout(openMode, 50);
  else global.addEventListener('load', function () { global.setTimeout(openMode, 50); });
})(window);
