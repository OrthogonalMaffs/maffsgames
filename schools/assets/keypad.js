/* MaffsKeypad — the phone keypad for typed answers (canon §4.4). One copy, for every game: a game
 * without a calculator mounts it on its own; MaffsCalc (calculator.js) composes it for its answer mode,
 * so there is one phone keypad on the site.
 *
 * On a touch screen the keypad types the answer, so the system keyboard (about 40% of a phone screen)
 * never opens: every target is read-only with inputmode="none" and is never focused (pointerdown and
 * mousedown are cancelled, focus is dropped, the tap's ghost click is cancelled). Tapping a target makes
 * it the active one, marked by a heavier border and a "typing here" tag, never colour alone; the keys
 * type into the active target only. With a mouse, or no touch, nothing is drawn and the targets are
 * ordinary text inputs (inputmode="decimal" unless the page set its own).
 *
 *   MaffsKeypad.mount(el, {targets, keys, maxLength, keepInView, foldInset})
 *       el          where the keys are drawn (shown on touch screens only)
 *       targets     one or more <input> elements, in order; the first is active to begin with
 *       keys        {minus: true} adds a minus key (off by default): it types "-" into an empty target
 *       maxLength   the most characters a target takes (default 12)
 *       keepInView  an element (say the answer row) to keep in the window with the keys when a target
 *                   is tapped; foldInset is the height of anything fixed at the window's foot (a footer)
 *     Returns a handle: active(), target(), select(i), type(act, val), press(label), apply(), together().
 *     Each typed key fires an "input" event on its target, as typing would.
 *
 * Composition (MaffsCalc only): el is null, so no keys are drawn; the composer presses them through
 * type(), and passes config (its own live switches), enabled (when keypad mode applies), onTap (what a
 * tap on a target does), prefix (its class names) and plain: null (leave inputmode alone with a mouse).
 *
 * MaffsKeypad.CONFIG is read live, so a test can switch each part off. Nothing is sent anywhere: no
 * analytics event, no storage. Self-tests: scripts/check-keypad.py (CI); scripts/test-calculator-js.py
 * covers the composed keypad.
 */
(function () {
  'use strict';

  var CONFIG = { query: '(pointer: coarse)', readOnly: true, inputmode: true, blur: true, cue: true };
  var MAX = 12;
  // Five columns, the calculator's, so a key is the same size as MaffsCalc's on a phone. The point
  // spans two columns when there is no minus key.
  var KEYS = [
    ['7', 'in', '7'], ['8', 'in', '8'], ['9', 'in', '9'], ['DEL', 'del', '', 'Delete', 'op'], ['C', 'clear', '', 'Clear', 'op'],
    ['4', 'in', '4'], ['5', 'in', '5'], ['6', 'in', '6'], ['.', 'in', '.', 'Decimal point'], ['−', 'minus', '-', 'Minus', 'op'],
    ['1', 'in', '1'], ['2', 'in', '2'], ['3', 'in', '3'], ['0', 'in', '0', null, 'wide']
  ];

  // Type one key into an input: digits and the point up to the length limit, DEL, C, and a minus into
  // an empty box. Returns whether anything changed.
  function typeInto(t, act, val, max) {
    var v = t.value;
    if (act === 'clear') v = '';
    else if (act === 'del') v = v.slice(0, -1);
    else if (act === 'minus') { if (v !== '') return false; v = '-'; }
    else if (act === 'in' && /^[0-9.]$/.test(val) && v.length < max) v += val;
    else return false;
    t.value = v;
    t.dispatchEvent(new Event('input', { bubbles: true }));
    return true;
  }

  // Scroll so that keep (the answer row) and the keys are in the window together, keep's top first.
  function together(keep, keys, foldInset) {
    if (!keep || !keys) return;
    var r1 = keep.getBoundingClientRect(), r2 = keys.getBoundingClientRect();
    var fold = window.innerHeight - (foldInset || 0);
    var dy = Math.min(r2.bottom - fold + 8, r1.top - 8);
    if (r2.bottom > fold && dy > 0) window.scrollBy(0, dy);
  }

  function mount(el, opts) {
    opts = opts || {};
    var targets = [].concat(opts.targets || []).filter(Boolean);
    var cfg = typeof opts.config === 'function' ? opts.config : function () { return window.MaffsKeypad.CONFIG; };
    var enabled = typeof opts.enabled === 'function' ? opts.enabled : function () {
      return !!(window.matchMedia && window.matchMedia(cfg().query).matches);
    };
    var prefix = opts.prefix || 'maffs-keypad';
    var max = opts.maxLength || MAX;
    var plain = 'plain' in opts ? opts.plain : 'decimal';
    var initial = 'initial' in opts ? opts.initial : (el ? 0 : -1);
    var active = -1;
    var orig = targets.map(function (t) { return { readOnly: t.readOnly, inputmode: t.getAttribute('inputmode') }; });
    var cues = targets.map(function (t) {
      var c = document.createElement('span');
      c.className = prefix + '-cue ' + prefix + '-cue-answer';
      c.setAttribute('aria-hidden', 'true');
      c.textContent = 'typing here';
      t.insertAdjacentElement('afterend', c);
      t.parentElement.classList.add(prefix + '-answer-host');
      return c;
    });

    var panel = null;
    if (el) {
      var minus = !!(opts.keys && opts.keys.minus);
      var h = '<div class="maffs-keypad-panel" role="group" aria-label="Keypad"><div class="maffs-keypad-keys">';
      KEYS.forEach(function (k) {
        if (k[1] === 'minus' && !minus) return;
        var cls = (k[4] ? ' ' + k[4] : '') + (k[0] === '.' && !minus ? ' wide' : '');
        h += '<button type="button" class="maffs-keypad-key' + cls + '" data-act="' + k[1] + '" data-val="' + k[2] + '"' +
          (k[3] ? ' aria-label="' + k[3] + '"' : '') + '>' + k[0] + '</button>';
      });
      el.classList.add('maffs-keypad');
      el.innerHTML = h + '</div></div>';
      panel = el.querySelector('.maffs-keypad-panel');
      el.addEventListener('click', function (e) {
        var b = e.target.closest ? e.target.closest('.maffs-keypad-key') : null;
        if (b && !b.disabled) type(b.getAttribute('data-act'), b.getAttribute('data-val'));
      });
    }

    function type(act, val) {
      return active >= 0 ? typeInto(targets[active], act, val, max) : false;
    }
    // The targets' attributes, and whether the keys show: keypad mode on a touch screen, plain inputs otherwise.
    function attrs() {
      var C = cfg(), on = enabled();
      targets.forEach(function (t, i) {
        t.readOnly = on && C.readOnly ? true : orig[i].readOnly;
        var im = orig[i].inputmode !== null ? orig[i].inputmode : plain;
        if (on && C.inputmode) t.setAttribute('inputmode', 'none');
        else if (im === null) t.removeAttribute('inputmode');
        else t.setAttribute('inputmode', im);
      });
      if (el) el.hidden = !on;
      return on;
    }
    // Which target the keys type into (-1: none). The active one has a heavier border and a "typing here" tag.
    function select(i) {
      var C = cfg(), on = enabled();
      active = on && i >= 0 && i < targets.length ? i : -1;
      var cue = on && C.cue;
      targets.forEach(function (t, k) {
        t.classList.toggle(prefix + '-selected', cue && k === active);
        cues[k].hidden = !(cue && k === active);
        // On the box's top edge, 6px in. A narrow box (one of several in a row on a phone) gets the tag
        // centred on it, its text shrunk to at most 6px wider than the box each side, so it never lies over
        // the next box, in any font (OpenDyslexic included).
        var c = cues[k], tw = t.offsetWidth;
        if (c.style.fontSize) c.style.fontSize = '';
        var w = c.offsetWidth;
        if (w > tw + 12) {
          c.style.fontSize = Math.max(8, parseFloat(getComputedStyle(c).fontSize) * (tw + 12) / w) + 'px';
          w = c.offsetWidth;
        }
        c.style.left = (w && w > tw - 12 ? t.offsetLeft + (tw - w) / 2 : t.offsetLeft + 6) + 'px';
        c.style.top = (t.offsetTop - 7) + 'px';
      });
    }
    function apply() {
      var on = attrs();
      select(on ? (active >= 0 ? active : initial) : -1);
    }
    function keepTogether() { together(opts.keepInView || targets[active] || targets[0], panel, opts.foldInset); }

    targets.forEach(function (t, i) {
      // A tap makes the target active; the box itself is never focused (no system keyboard).
      var noFocus = function (e) { if (enabled() && cfg().blur) e.preventDefault(); };
      t.addEventListener('pointerdown', noFocus);
      t.addEventListener('mousedown', noFocus);
      t.addEventListener('focus', function () { if (enabled() && cfg().blur) t.blur(); });
      // Activate on pointerup: WebKit sends no click after a touch whose pointerdown was cancelled (which is
      // what keeps focus, and so the keyboard, away). click stays for anything without pointer events.
      var lastUp = 0;
      var activate = function () {
        if (opts.onTap) { opts.onTap(i); return; }
        select(i);
        keepTogether();
      };
      t.addEventListener('pointerup', function () { if (!enabled()) return; lastUp = Date.now(); activate(); });
      // Activating may move the page, so the tap's own click could land on whatever is now under the
      // finger, a key: cancel it.
      t.addEventListener('touchend', function (e) { if (enabled() && cfg().blur) e.preventDefault(); }, { passive: false });
      t.addEventListener('click', function () { if (enabled() && Date.now() - lastUp > 600) activate(); });
    });

    if (el) {
      apply();
      if (!opts.enabled && window.matchMedia) {
        var mq = window.matchMedia(cfg().query);
        if (mq.addEventListener) mq.addEventListener('change', apply);
      }
    }

    return {
      el: el,
      targets: targets,
      active: function () { return active; },
      target: function () { return active >= 0 ? targets[active] : null; },
      enabled: enabled,
      select: select,
      type: type,
      attrs: attrs,
      apply: apply,
      together: keepTogether,
      // For tests: press a key by its label ('7', '.', 'DEL', 'C', '−').
      press: function (label) {
        var k = KEYS.filter(function (x) { return x[0] === label; })[0];
        return k ? type(k[1], k[2]) : false;
      }
    };
  }

  window.MaffsKeypad = { mount: mount, together: together, CONFIG: CONFIG, KEYS: KEYS, MAX: MAX };
})();
