/* MaffsNext — self-paced advance after a wrong answer.
 *
 * WHY THIS EXISTS
 * ---------------
 * Games auto-advanced to the next question on a fixed timer: 800ms to 2400ms across
 * 25 games, tuned by guesswork, and none of them distinguished a right answer from a
 * wrong one. A single number cannot fit every reading speed — too short and a slow
 * reader never sees why they were wrong, too long and a fast one is held hostage.
 *
 * So we stop guessing. A correct answer keeps whatever brisk delay the game already
 * had. A wrong answer shows a "Next →" control and waits for the student, with a
 * generous fallback so a walked-away tab still finishes rather than hanging forever.
 *
 * The pause is only worth anything if there is something on screen to read, so a game
 * must show its working/explanation on the wrong path BEFORE calling this. See
 * canon §7.6.
 *
 * WHAT IT GUARANTEES (canon §7.6)
 * -------------------------------
 *   - A floor: for FLOOR_MS (3s, Jon's ruling of 29 Sep 2026) the control is visibly
 *     disabled and nothing a student does can advance, so the explanation is on screen
 *     for at least that long. The floor is separate from the fallback.
 *   - Advance once: onAdvance runs at most once per wrong() call, however it is
 *     triggered — a click, Enter or Space on the focused control, the game's own key
 *     handler calling advance(), or the fallback. A game that also listens for Enter
 *     can no longer skip a question by advancing twice on one key press.
 *   - clear() cancels: removing a control also cancels its timers and listeners, so
 *     nothing it scheduled can fire after the game has moved on.
 *   - A 44px target: the control is at least 44px tall and wide.
 *   - Advancing clears every MaffsLock.timer() (schools/assets/answer-lock.js), so no timer
 *     set for the question just left can fire on the next one.
 *   - In view (NEXT-IN-VIEW, 19 Nov 2026): wrong() brings the control into view itself, through
 *     MaffsScroll.reveal (schools/assets/scroll.js), which settles again as fonts arrive and the
 *     working grows, and stops at the student's own wheel, touch or key. A page that does not
 *     load scroll.js gets it once, from beside this file. Canon §7.6.1: the reason and Next both
 *     on screen on a phone. A control inside something fixed (an overlay) is left alone, since
 *     scrolling the page cannot move it.
 *
 * USAGE
 * -----
 *   var next = MaffsNext.wrong({ mount: someElement, onAdvance: () => loadQuestion() });
 *   next.advance();   // optional: a game's own key handler; honours the floor, runs once
 *
 * Options:
 *   mount       element to append the control to (required)
 *   onAdvance   called once, on click or on fallback (required)
 *   fallbackMs  safety net, default 20000. Deliberately long: it is not the mechanism.
 *               It runs on its own clock and ignores the floor.
 *   label       button text, default 'Next →'
 *   keep        the reason/feedback element (or a function returning it) whose top must stay
 *               on screen while Next is brought into view; default the control itself
 *
 * MaffsNext.FLOOR_MS is read each time a control is made, never captured at load. Its
 * value for students is 3000. Content verifiers set it to 0 through the shared harness
 * helper (scripts/bank_common.py, NO_NEXT_FLOOR_INIT) so they do not wait out the floor
 * on every wrong answer; tier 3 and scripts/test-next-control.py keep the real floor.
 */
(function () {
  'use strict';

  var FALLBACK_MS = 20000;
  var FLOOR_MS = 3000;
  var api;   // window.MaffsNext, assigned below

  // This file's own address, read while it runs, so scroll.js is found beside it at any page depth.
  var SELF_SRC = (function () {
    var s = document.currentScript;
    if (s && s.src) return s.src;
    var all = document.getElementsByTagName('script');
    for (var i = all.length - 1; i >= 0; i--) {
      if (/(^|\/)next-control\.js([?#]|$)/.test(all[i].src || '')) return all[i].src;
    }
    return '';
  })();
  var scrollWaiting = null;   // callbacks waiting for scroll.js, once its tag is added; 'failed' if it could not load

  /* Run fn once MaffsScroll exists: now if the page loaded scroll.js, otherwise after one tag fetches it. */
  function withScroll(fn) {
    if (window.MaffsScroll && typeof window.MaffsScroll.reveal === 'function') { fn(); return; }
    if (scrollWaiting === 'failed') return;
    if (scrollWaiting) { scrollWaiting.push(fn); return; }
    var src;
    try { src = new URL('scroll.js', SELF_SRC || document.baseURI).href; } catch (e) { return; }
    scrollWaiting = [fn];
    var tag = document.createElement('script');
    tag.src = src;
    tag.setAttribute('data-maffs-next', 'scroll');
    tag.onload = function () {
      var q = scrollWaiting;
      scrollWaiting = null;
      if (!(window.MaffsScroll && typeof window.MaffsScroll.reveal === 'function')) { scrollWaiting = 'failed'; return; }
      for (var i = 0; i < q.length; i++) { try { q[i](); } catch (e) { /* one page's fault stays its own */ } }
    };
    tag.onerror = function () { scrollWaiting = 'failed'; };
    (document.head || document.documentElement).appendChild(tag);
  }

  // Inside something fixed (an overlay), scrolling the page cannot move the control: leave it.
  function inFixed(el) {
    for (var n = el; n && n.nodeType === 1; n = n.parentElement) {
      if (getComputedStyle(n).position === 'fixed') return true;
    }
    return false;
  }

  /* Bring the control into view, with keep's top held on screen. Nothing once the control has gone. */
  function reveal(wrap, keep, state) {
    withScroll(function () {
      if (state.cancelled || state.done || !wrap.isConnected || inFixed(wrap)) return;
      window.MaffsScroll.reveal(wrap, { keep: keep || wrap });
    });
  }

  // The floor in force for a new control: the public constant, read at use.
  function floorMs() {
    var v = api && api.FLOOR_MS;
    return (typeof v === 'number' && v >= 0) ? v : FLOOR_MS;
  }

  function injectStyleOnce() {
    if (document.getElementById('maffs-next-style')) return;
    var st = document.createElement('style');
    st.id = 'maffs-next-style';
    /* Inherits the host game's palette: games set --red/--primary/--accent differently,
       so this leans on currentColor and a neutral surface rather than naming a colour.
       During the floor the control is dimmed and a faint fill crosses it once, so the
       wait is visible without being loud; with reduced motion it is dimmed only.
       The 44px minimum is 3px taller than the old control, so the top margin gives the 3px
       back (11px, was 14px): the control's footprint is unchanged and no game fitted to the
       phone rule moves (free-daily-pizza's tightest screens had less than 3px to spare). */
    st.textContent =
      '.maffs-next{position:relative;overflow:hidden;display:inline-flex;align-items:center;justify-content:center;' +
      'gap:8px;margin:11px auto 2px;padding:11px 26px;min-height:44px;min-width:44px;box-sizing:border-box;' +
      'font-family:inherit;font-size:15px;font-weight:700;line-height:1;cursor:pointer;' +
      'border:2px solid currentColor;border-radius:10px;background:transparent;color:inherit;' +
      'opacity:0.95;transition:background .15s,transform .15s,opacity .2s;}' +
      '.maffs-next:hover:not([disabled]){background:rgba(127,127,127,0.18);transform:translateY(-1px);}' +
      '.maffs-next:focus-visible{outline:3px solid currentColor;outline-offset:3px;}' +
      '.maffs-next[disabled]{cursor:default;opacity:0.55;}' +
      '.maffs-next[disabled]::before{content:"";position:absolute;inset:0;background:currentColor;opacity:0.14;' +
      'transform-origin:left center;transform:scaleX(0);animation:maffs-next-floor var(--maffs-next-floor,3000ms) linear forwards;}' +
      '@keyframes maffs-next-floor{to{transform:scaleX(1);}}' +
      '@media (prefers-reduced-motion: reduce){.maffs-next[disabled]::before{display:none;}.maffs-next{transition:none;}}' +
      '.maffs-next-wrap{display:flex;justify-content:center;width:100%;}';
    document.head.appendChild(st);
  }

  /* Stop everything one control scheduled or listened for. Idempotent. */
  function cancel(state) {
    if (!state || state.cancelled) return;
    state.cancelled = true;
    if (state.fallback) { clearTimeout(state.fallback); state.fallback = null; }
    if (state.floor) { clearTimeout(state.floor); state.floor = null; }
    state.btn.removeEventListener('click', state.onClick);
  }

  function wrong(opts) {
    opts = opts || {};
    var mount = opts.mount;
    var onAdvance = opts.onAdvance;
    if (!mount || typeof onAdvance !== 'function') return null;

    injectStyleOnce();
    clear(mount);

    var wrap = document.createElement('div');
    wrap.className = 'maffs-next-wrap';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'maffs-next';
    btn.textContent = opts.label || 'Next →';
    btn.disabled = true;                 // the floor: no click, Enter or Space can land
    wrap.appendChild(btn);
    mount.appendChild(wrap);

    var floor = floorMs();
    btn.style.setProperty('--maffs-next-floor', floor + 'ms');   // the fill crosses in the floor's time
    var state = { btn: btn, ready: false, done: false, cancelled: false, fallback: null, floor: null, onClick: null };

    // The single way out. `force` is the fallback, which runs on its own clock and
    // ignores the floor; everything a student or a game does waits for the floor.
    function go(force) {
      if (state.done || state.cancelled) return;
      if (!state.ready && !force) return;
      state.done = true;
      cancel(state);
      if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
      // Advancing ends the question: no timer it set (MaffsLock.timer) may fire after this.
      if (window.MaffsLock) window.MaffsLock.clearTimers();
      onAdvance();
    }

    state.onClick = function () { go(false); };
    btn.addEventListener('click', state.onClick);
    wrap.__maffsNext = state;

    state.floor = setTimeout(function () {
      state.floor = null;
      if (state.cancelled) return;
      state.ready = true;
      btn.disabled = false;
      // Focus so Enter/Space advances without reaching for the mouse, but do not scroll
      // the page out from under the explanation the student is reading.
      try { btn.focus({ preventScroll: true }); } catch (e) { /* older browsers */ }
    }, floor);

    // Safety net only. If the student walks away the run still completes.
    state.fallback = setTimeout(function () { state.fallback = null; go(true); },
      typeof opts.fallbackMs === 'number' ? opts.fallbackMs : FALLBACK_MS);

    // The reason and Next on screen (canon §7.6.1), settling as the page does.
    reveal(wrap, opts.keep, state);

    return { advance: function () { go(false); }, button: btn };
  }

  /* Remove any control left over from a previous question, and cancel its timers. */
  function clear(mount) {
    if (!mount) return;
    var old = mount.querySelectorAll('.maffs-next-wrap');
    for (var i = 0; i < old.length; i++) {
      cancel(old[i].__maffsNext);
      if (old[i].parentNode) old[i].parentNode.removeChild(old[i]);
    }
  }

  api ={ wrong: wrong, clear: clear, FALLBACK_MS: FALLBACK_MS, FLOOR_MS: FLOOR_MS };
  window.MaffsNext = api;
})();
