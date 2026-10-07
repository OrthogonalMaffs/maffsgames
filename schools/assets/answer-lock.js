/* MaffsLock — answer once (canon §7.6). One copy, for every game; used with MaffsNext.
 *
 * WHY THIS EXISTS
 * ---------------
 * Every game guarded its own input, or didn't. The audits found the same faults in 30+ games
 * (register class 1): an answered option "locked" only by a CSS class (pointer-events:none), so
 * Enter or Space on it still fired and re-marked it; a double-click on Next landed its second
 * click on the next question's option; Check stayed live during the pause; a timer set for one
 * question fired after the student had moved on (a game that finished twice and submitted its
 * score twice; a solution animation drawn onto the next puzzle). MaffsNext handled only the
 * wrong-answer pause. This is the rest, fixed once.
 *
 * THE API
 * -------
 *   MaffsLock.lock(container)    Call it FIRST in every answer handler, and stop if it says no:
 *                                  if (!MaffsLock.lock(answerArea)) return;
 *                                The first call for a question sets the disabled attribute (and
 *                                aria-disabled="true") on every answer control in the container
 *                                and drops any further click, key or touch on them in a capture
 *                                listener, before the game's own listeners see it. A second call
 *                                for the same question returns false. A question is "the same"
 *                                until fresh() is called on the container, or until every control
 *                                it locked has left the page (the game rendered new ones).
 *                                Answer controls: buttons, inputs, selects, textareas, anything
 *                                with role="button"/"option"/"radio", a tabindex, an onclick, or a
 *                                pointer cursor. A MaffsNext control, and anything inside an
 *                                element marked data-maffs-lock-skip (a game's own Next button
 *                                inside the container), is never locked; fresh() still covers it,
 *                                so a second Enter on Next cannot skip the question it loaded.
 *   MaffsLock.isLocked(container)  true from lock() until the next question (fresh(), or its
 *                                controls gone): what a game asks instead of keeping an "answered"
 *                                flag (a keypad that must stop typing, an Enter that must advance).
 *   MaffsLock.fresh(container[, ms])  Call it when a new question or screen renders into the
 *                                container. It undoes the lock on the container (re-enabling what
 *                                lock() disabled, for a game that reuses its buttons) and ignores
 *                                ALL input on it for FRESH_MS (300 ms): the second click of a
 *                                double-click, a second Enter, a double-tap. A key press with no
 *                                focused control (document.body) counts as input on it.
 *   MaffsLock.screen(container)  A screen change: clearTimers(), then fresh(container).
 *   MaffsLock.timer(fn, ms)      setTimeout for every per-question and per-screen timer. Returns
 *                                an id for MaffsLock.cancel(id).
 *   MaffsLock.clearTimers()      Cancels every timer made by timer(). MaffsNext's advance calls
 *                                it, and so does screen(), so a stale timer can never fire.
 *   MaffsLock.finishOnce(fn)     Returns fn wrapped so it runs at most once per session: the
 *                                end-of-game handler (game_completed and submitScore).
 *                                  const endGame = MaffsLock.finishOnce(function () { ... });
 *   MaffsLock.newSession()       A new run (Start, Play again): clearTimers(), and every
 *                                finishOnce() handler may run once more.
 *   MaffsLock.FRESH_MS           300. Read at each fresh() call, never captured at load.
 *
 * RULE (canon §7.6): every game marks through MaffsLock; no game keeps a local "answered" flag.
 * scripts/test-answer-lock.py tests this file in Chromium (every behaviour above, and planted
 * faults); scripts/check-answer-lock.py plays every migrated game against it.
 *
 * THE GAME'S DECLARATION (contract LH, canon §7.6.0)
 * --------------------------------------------------
 * Adopting MaffsLock includes declaring, in the game's own page, how check-answer-lock.py produces
 * a wrong answer there: one HTML comment, "<!-- maffs-lock-hint" then a JSON object then "-->", e.g.
 *   {"ready": "document.getElementById('gameScreen').classList.contains('active')",
 *    "answer": "document.querySelector('#numpad [data-val=\"enter\"]').click();"}
 * {} when the check's generic driver plays the game unaided. Keys and meanings: HINT_KEYS in
 * scripts/check-answer-lock.py. Nothing here reads it; it is for the check only. The script order of
 * this file and next-control.js is free: neither reads the other at load.
 */
(function () {
  'use strict';

  var FRESH_MS = 300;
  var CONTROLS = 'button, input, select, textarea, [role="button"], [role="option"], [role="radio"], ' +
    '[tabindex], [onclick]';
  var EVENTS = ['click', 'dblclick', 'auxclick', 'contextmenu', 'mousedown', 'mouseup', 'pointerdown',
    'pointerup', 'touchstart', 'touchend', 'keydown', 'keypress', 'keyup', 'input', 'change', 'submit'];
  var KEYS = { keydown: 1, keypress: 1, keyup: 1 };

  var api;
  var states = [];          // one per container lock() or fresh() has seen
  var timers = {};          // id -> true, for every live timer()
  var session = 0;

  function now() { return Date.now(); }
  function freshMs() {
    var v = api && api.FRESH_MS;
    return (typeof v === 'number' && v >= 0) ? v : FRESH_MS;
  }

  function stateOf(container) {
    for (var i = 0; i < states.length; i++) if (states[i].c === container) return states[i];
    var st = { c: container, locked: false, els: [], undo: [], until: 0 };
    states.push(st);
    return st;
  }

  function skipped(el) {
    return !!(el.closest && el.closest('.maffs-next-wrap, [data-maffs-lock-skip]'));
  }

  function isControl(el) {
    if (el.matches && el.matches(CONTROLS)) return true;
    try { return getComputedStyle(el).cursor === 'pointer'; } catch (e) { return false; }
  }

  // The controls a lock covers: every answer control in the container at the time of the lock.
  function controlsIn(container) {
    var out = [], all = container.querySelectorAll('*');
    for (var i = 0; i < all.length; i++) {
      if (!skipped(all[i]) && isControl(all[i])) out.push(all[i]);
    }
    return out;
  }

  // A lock belongs to the question whose controls it locked: once all of them have left the
  // page (the game rendered the next question's), the container is unlocked for the next one.
  function stale(st) {
    if (!st.locked) return false;
    for (var i = 0; i < st.els.length; i++) if (st.c.contains(st.els[i])) return false;
    return true;
  }

  function undo(st) {
    for (var i = 0; i < st.undo.length; i++) {
      var u = st.undo[i];
      if (u[1] === 'disabled') u[0].disabled = false;
      else u[0].removeAttribute('aria-disabled');
    }
    st.undo = [];
    st.els = [];
    st.locked = false;
  }

  function lock(container) {
    if (!container) return true;
    var st = stateOf(container);
    if (stale(st)) undo(st);
    if (st.locked) return false;
    st.locked = true;
    st.els = controlsIn(container);
    for (var i = 0; i < st.els.length; i++) {
      var el = st.els[i];
      if ('disabled' in el && !el.disabled) { el.disabled = true; st.undo.push([el, 'disabled']); }
      if (el.getAttribute('aria-disabled') !== 'true') {
        el.setAttribute('aria-disabled', 'true');
        st.undo.push([el, 'aria']);
      }
    }
    return true;
  }

  function isLocked(container) {
    if (!container) return false;
    var st = stateOf(container);
    if (stale(st)) undo(st);
    return st.locked;
  }

  function fresh(container, ms) {
    if (!container) return;
    var st = stateOf(container);
    undo(st);
    st.until = now() + (typeof ms === 'number' && ms >= 0 ? ms : freshMs());
  }

  // Does this event land on something the locks or fresh windows cover?
  function blocked(e) {
    var t = e.target, t0 = now();
    if (!t || t.nodeType !== 1) t = document.body;
    var bare = !!KEYS[e.type] && (t === document.body || t === document.documentElement);
    for (var i = states.length - 1; i >= 0; i--) {
      var st = states[i];
      if (!st.c.isConnected) { states.splice(i, 1); continue; }
      var inside = st.c.contains(t);
      if (st.until > t0 && (inside || bare)) return true;
      if (st.locked && inside && !stale(st)) {
        for (var n = t; n && n !== st.c; n = n.parentNode) {
          if (st.els.indexOf(n) !== -1) return true;
        }
      }
    }
    return false;
  }

  function guard(e) {
    if (!states.length || !blocked(e)) return;
    e.stopImmediatePropagation();
    if (e.cancelable) e.preventDefault();
  }

  for (var i = 0; i < EVENTS.length; i++) {
    window.addEventListener(EVENTS[i], guard, { capture: true, passive: false });
  }

  function timer(fn, ms) {
    var id = setTimeout(function () {
      if (!timers[id]) return;
      delete timers[id];
      fn();
    }, ms);
    timers[id] = true;
    return id;
  }

  function cancel(id) {
    if (timers[id]) { clearTimeout(id); delete timers[id]; }
  }

  function clearTimers() {
    for (var id in timers) {
      if (Object.prototype.hasOwnProperty.call(timers, id)) clearTimeout(Number(id));
    }
    timers = {};
  }

  function screen(container) {
    clearTimers();
    fresh(container);
  }

  function finishOnce(fn) {
    var ran = -1;
    return function () {
      if (ran === session) return undefined;
      ran = session;
      return fn.apply(this, arguments);
    };
  }

  function newSession() {
    clearTimers();
    session++;
  }

  api = {
    lock: lock, isLocked: isLocked, fresh: fresh, screen: screen, timer: timer, cancel: cancel, clearTimers: clearTimers,
    finishOnce: finishOnce, newSession: newSession, FRESH_MS: FRESH_MS
  };
  window.MaffsLock = api;
})();
