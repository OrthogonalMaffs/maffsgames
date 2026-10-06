/* MaffsCalc — the shared on-screen calculator (canon §4.4), for games whose roster Calculator field
 * is "required". Many resit students do not own a scientific calculator; this gives them the keys a
 * Pythagoras or percentages question needs, and nothing more.
 *
 * Two halves:
 *   MaffsCalc.evaluate(expr)  the engine: a recursive-descent parser over the key symbols, no DOM, no
 *                             eval(). Returns a number, or null for anything a calculator shows as
 *                             "Error" (divide by 0, square root of a negative, unbalanced brackets, a
 *                             trailing operator, 1.2.3).
 *   MaffsCalc.format(x)       the display: 10 significant figures with trailing zeros dropped, so
 *                             0.1 + 0.2 shows 0.3, never 0.30000000000000004.
 *   MaffsCalc.mount(el, {dock: card})
 *                             the UI: a "Calculator" toggle and a panel. On a narrow screen the panel
 *                             opens in the page flow, below whatever comes before el; it never covers
 *                             anything and the page may scroll. Where the space to the right of the
 *                             dock element (the game's question card) holds the panel, it docks there
 *                             instead: beside the card, level with its top, sticky while the page
 *                             scrolls, out of the page flow so the game column never moves (canon §4.4).
 *
 * Grammar (calculator conventions: -3² = -9; √ opens a bracket, like a Casio; missing closing
 * brackets are closed on =, extra ones are an error; a number, bracket or √ straight after a value
 * multiplies, so 2(3) = 6 and 2√(9) = 6):
 *   expr    := term (('+' | '−') term)*
 *   term    := unary (('×' | '÷') unary | <implicit ×> unary)*
 *   unary   := ('−' | '+') unary | power
 *   power   := primary '²'*
 *   primary := number | Ans | '(' expr ')' | '√(' expr ')'
 *
 * On a phone (a touch screen below the dock breakpoint) the panel is compact: its close key sits in the
 * display, keys are 48px. mount(el, {answer: input}) makes the keypad type the game's answer too, so the
 * system keyboard never opens; the student taps a display to choose where the keys go (ANSWER below).
 * Anywhere else nothing about the answer box changes. The answer box is driven by MaffsKeypad
 * (keypad.js, the one phone keypad on the site), which a page with {answer} loads before mounting.
 *
 * The physical keyboard drives the panel only while focus is inside it, so typing in a game's answer
 * box is never taken over. Nothing is sent anywhere: no analytics event, no storage.
 *
 * Self-tests: scripts/test-calculator-js.py (CI). Which games load it: scripts/check-calculator.py.
 */
(function () {
  'use strict';

  var MUL = '×', DIV = '÷', MINUS = '−', SQ = '²', ROOT = '√', ANS = 'A';
  var MAX_LEN = 80;

  /* ---------- engine ---------- */
  // Accepts the key symbols and their ASCII forms (* / - ^2 sqrt), so tests can be written plainly.
  function normalise(s) {
    return String(s).replace(/\s+/g, '').replace(/\*/g, MUL).replace(/\//g, DIV).replace(/-/g, MINUS)
      .replace(/\^2/g, SQ).replace(/sqrt\(/g, ROOT + '(').replace(/Ans/g, ANS);
  }

  function evaluate(expr, ans) {
    var s = normalise(expr), i = 0;
    if (!s) return null;
    // Close any brackets left open (as a calculator does on =); more ')' than '(' is an error.
    var depth = 0;
    for (var k = 0; k < s.length; k++) {
      if (s[k] === '(') depth++;
      else if (s[k] === ')' && --depth < 0) return null;
    }
    while (depth-- > 0) s += ')';

    function fail() { throw new Error('calc'); }
    function peek() { return s[i]; }
    function startsValue(c) { return c !== undefined && (/[0-9.(]/.test(c) || c === ROOT || c === ANS); }

    function number() {
      var m = /^(\d+\.?\d*|\.\d+)/.exec(s.slice(i));
      if (!m) fail();
      i += m[0].length;
      if (peek() === '.') fail();                       // 1.2.3
      return parseFloat(m[0]);
    }
    function primary() {
      var c = peek();
      if (c === '(') { i++; var v = expr0(); if (peek() !== ')') fail(); i++; return v; }
      if (c === ROOT) {
        i++; if (peek() !== '(') fail(); i++;
        var r = expr0(); if (peek() !== ')') fail(); i++;
        if (r < 0) fail();
        return Math.sqrt(r);
      }
      if (c === ANS) { i++; if (typeof ans !== 'number' || !isFinite(ans)) fail(); return ans; }
      if (c !== undefined && /[0-9.]/.test(c)) return number();
      return fail();
    }
    function power() {
      var v = primary();
      while (peek() === SQ) { i++; v = v * v; }
      return v;
    }
    function unary() {
      var c = peek();
      if (c === MINUS) { i++; return -unary(); }
      if (c === '+') { i++; return unary(); }
      return power();
    }
    function term() {
      var v = unary();
      for (;;) {
        var c = peek();
        if (c === MUL) { i++; v = v * unary(); }
        else if (c === DIV) { i++; var d = unary(); if (d === 0) fail(); v = v / d; }
        else if (startsValue(c)) { v = v * unary(); }
        else return v;
      }
    }
    function expr0() {
      var v = term();
      for (;;) {
        var c = peek();
        if (c === '+') { i++; v = v + term(); }
        else if (c === MINUS) { i++; v = v - term(); }
        else return v;
      }
    }
    try {
      var v = expr0();
      if (i !== s.length || !isFinite(v)) return null;
      return v;
    } catch (e) {
      return null;
    }
  }

  // 10 significant figures, trailing zeros dropped; 10^10 and over, or under 10^-6, as a × 10^n.
  function format(x) {
    if (x === null || typeof x !== 'number' || !isFinite(x)) return 'Error';
    var v = Number(x.toPrecision(10));
    if (v === 0) return '0';                             // also -0
    var a = Math.abs(v);
    var t = a >= 1e10 || a < 1e-6 ? v.toExponential() : String(v);   // a calculator's 10-digit screen
    var m = /^(-?[\d.]+)e([+-]\d+)$/.exec(t);
    if (m) return (m[1] + MUL + '10^' + String(parseInt(m[2], 10))).replace('-', MINUS);
    return t.replace('-', MINUS);
  }

  function calc(expr, ans) { return format(evaluate(expr, ans)); }

  /* ---------- UI ---------- */
  // Five columns, so every key is at least 44px wide in a 278px card (a 320px phone).
  var KEYS = [
    ['C', 'clear', 'C', 'Clear'], ['DEL', 'del', 'DEL', 'Delete'], ['(', 'in', '(', 'Open bracket'],
    [')', 'in', ')', 'Close bracket'], [DIV, 'in', DIV, 'Divide'],
    ['7', 'in', '7'], ['8', 'in', '8'], ['9', 'in', '9'], [ROOT, 'in', ROOT + '(', 'Square root'], [MUL, 'in', MUL, 'Times'],
    ['4', 'in', '4'], ['5', 'in', '5'], ['6', 'in', '6'], ['x' + SQ, 'in', SQ, 'Squared'], [MINUS, 'in', MINUS, 'Minus'],
    ['1', 'in', '1'], ['2', 'in', '2'], ['3', 'in', '3'], ['.', 'in', '.', 'Decimal point'], ['+', 'in', '+', 'Plus'],
    ['0', 'in', '0', null, 'wide'], ['=', 'eq', '=', 'Equals', 'eq']
  ];
  var KEYBOARD = {
    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    '.': '.', ',': '.', '+': '+', '-': MINUS, '*': MUL, 'x': MUL, 'X': MUL, '/': DIV, '(': '(', ')': ')',
    '^': SQ, 'r': ROOT + '(', 'R': ROOT + '('
  };
  var OPERATORS = ['+', MINUS, MUL, DIV, SQ];
  var uid = 0;
  // The wide-screen dock. min is the narrowest panel whose five columns of keys stay 44px
  // (5 x 44 + 4 gaps of 6 + 2 x 8 padding + 2 x 1 border); the panel docks only when the room right of
  // the card, less the gap and an edge margin, is at least that. The breakpoint follows from the
  // game's own column, so it is measured, never a fixed media query.
  var DOCK = { gap: 12, edge: 8, min: 262, max: 340 };

  // Phones (canon §4.4, Jon 4 Oct 2026). "Compact" is a touch screen below the dock breakpoint: the
  // Calculator button moves into the panel (a close key in its display), keys grow to 48px and the display
  // slims. With {answer: input} the keypad also types the game's answer, so the system keyboard never
  // opens: the answer box is read-only with inputmode="none" and is never focused, and the student picks
  // which display the keys go to. Read live, so a test can switch each part off.
  var ANSWER = { query: '(pointer: coarse)', readOnly: true, inputmode: true, blur: true, disableOps: true,
    route: true, cue: true };
  var ANSWER_MAX = 12;

  function mount(el, opts) {
    opts = opts || {};
    var id = 'maffsCalc' + (++uid);
    el.classList.add('maffs-calc');
    var h = '<button type="button" class="maffs-calc-toggle" aria-expanded="false" aria-controls="' + id + '">' +
      'Calculator</button><div class="maffs-calc-rail" hidden>' +
      '<div class="maffs-calc-panel" id="' + id + '" role="group" aria-label="Calculator" tabindex="-1" hidden>' +
      '<div class="maffs-calc-screen"><button type="button" class="maffs-calc-close" aria-label="Close the calculator">' +
      '\u00d7</button><div class="maffs-calc-lines"><div class="maffs-calc-expr" aria-hidden="true">&nbsp;</div>' +
      '<div class="maffs-calc-result" aria-live="polite">0</div></div>' +
      '<span class="maffs-calc-cue" aria-hidden="true">typing here</span></div><div class="maffs-calc-keys">';
    KEYS.forEach(function (k) {
      h += '<button type="button" class="maffs-calc-key' + (k[4] ? ' ' + k[4] : '') + (k[1] !== 'in' || /[^0-9.]/.test(k[0]) ? ' op' : '') +
        '" data-act="' + k[1] + '" data-val="' + k[2] + '"' + (k[3] ? ' aria-label="' + k[3] + '"' : '') + '>' + k[0] + '</button>';
    });
    el.innerHTML = h + '</div></div></div>';

    var toggle = el.querySelector('.maffs-calc-toggle'), panel = el.querySelector('.maffs-calc-panel');
    var rail = el.querySelector('.maffs-calc-rail'), host = opts.dock || null;
    var screen = el.querySelector('.maffs-calc-screen'), closeBtn = el.querySelector('.maffs-calc-close');
    var keys = [].slice.call(el.querySelectorAll('.maffs-calc-key'));
    if (host) host.classList.add('maffs-calc-host');
    var exprEl = el.querySelector('.maffs-calc-expr'), resEl = el.querySelector('.maffs-calc-result');
    var expr = '', ans = null, done = false, ok = false;   // done: the last key was =; ok: and it gave a number
    var input = opts.answer || null, target = 'calc', kp = null;
    if ((input || opts.keepInView) && !window.MaffsKeypad) {
      throw new Error('MaffsCalc: {answer} and {keepInView} need schools/assets/keypad.js (MaffsKeypad) on the page');
    }
    if (input) {
      // The answer box is MaffsKeypad's target: read-only, never focused, marked when selected. This panel's
      // keys type into it through kp.type(); MaffsCalc.ANSWER stays the live switches, under its class names.
      kp = window.MaffsKeypad.mount(null, { targets: [input], prefix: 'maffs-calc', plain: null, initial: -1,
        maxLength: ANSWER_MAX, config: function () { return window.MaffsCalc.ANSWER; }, enabled: answerMode,
        onTap: function () { if (panel.hidden) setOpen(true); select('answer'); } });
    }

    function shown(e) { return e.split(ANS).join('Ans'); }
    function render(result) {
      exprEl.textContent = (done ? shown(expr) + ' =' : shown(expr)) || ' ';
      resEl.textContent = result;
    }
    function press(act, val) {
      // Typing the answer: MaffsKeypad takes digits, the point, DEL and C only.
      if (target === 'answer' && answerMode() && window.MaffsCalc.ANSWER.route) { kp.type(act, val); return; }
      if (act === 'clear') { expr = ''; done = false; ok = false; render('0'); return; }
      if (act === 'del') {
        if (done) { done = false; render(''); return; }
        expr = expr.slice(-2) === ROOT + '(' ? expr.slice(0, -2) : expr.slice(0, -1);
        render(''); return;
      }
      if (act === 'eq') {
        if (!expr) return;
        var v = evaluate(expr, ans);
        done = true;
        ok = v !== null;
        if (ok) ans = v;
        render(format(v));
        return;
      }
      if (done) {
        // After =, an operator carries the answer on (as "Ans"); anything else starts afresh.
        expr = OPERATORS.indexOf(val) !== -1 && ok ? ANS : '';
        done = false;
      }
      if (expr.length + val.length > MAX_LEN) return;
      expr += val;
      render('');
    }
    // Dock beside the card when the room to its right holds the panel; otherwise stay in the flow.
    function dock() {
      var D = window.MaffsCalc.DOCK;     // read live, so a test can move the threshold
      if (host && !host.getBoundingClientRect().width) return el.classList.contains('docked');   // not laid out yet
      var room = host ? document.documentElement.clientWidth - host.getBoundingClientRect().right - D.gap - D.edge : 0;
      var on = !!host && room >= D.min;
      el.classList.toggle('docked', on);
      rail.style.width = on ? Math.min(D.max, Math.floor(room)) + 'px' : '';
      rail.style.left = on ? 'calc(100% + ' + D.gap + 'px)' : '';
      return on;
    }
    function compact() {
      var q = window.MaffsCalc.ANSWER.query;
      return !el.classList.contains('docked') && !!(window.matchMedia && window.matchMedia(q).matches);
    }
    function answerMode() { return !!input && compact(); }
    // Compact or not, answer target or not: set the classes and the answer box's attributes to match.
    function applyMode() {
      var c = compact(), am = !!input && c;
      el.classList.toggle('compact', c);
      el.classList.toggle('answer-mode', am);
      if (kp) kp.attrs();
      select(am ? target : 'calc');
    }
    // Which display the keypad types into. The selected one has a heavier border and a "typing here" tag.
    function select(t) {
      var A = window.MaffsCalc.ANSWER, am = answerMode();
      target = am && t === 'answer' ? 'answer' : 'calc';
      var cue = am && A.cue;
      el.classList.toggle('target-answer', am && target === 'answer');
      el.classList.toggle('target-calc', am && target === 'calc');
      screen.classList.toggle('maffs-calc-selected', cue && target === 'calc');
      if (kp) kp.select(target === 'answer' ? 0 : -1);
      var off = am && target === 'answer' && A.disableOps;
      keys.forEach(function (b) {
        var act = b.getAttribute('data-act'), val = b.getAttribute('data-val');
        var dis = off && !(act === 'clear' || act === 'del' || (act === 'in' && /^[0-9.]$/.test(val)));
        b.disabled = dis;
        b.setAttribute('aria-disabled', String(dis));
      });
    }
    function setOpen(on) {
      dock();
      applyMode();
      rail.hidden = !on;
      panel.hidden = !on;
      el.classList.toggle('open', on);
      toggle.setAttribute('aria-expanded', String(on));
      toggle.classList.toggle('open', on);
      if (!on) select('calc');
      if (opts.onToggle) opts.onToggle(on);
      if (on && !compact()) { try { panel.focus({ preventScroll: true }); } catch (e) {} }
      if (on && compact()) together();
    }
    // Compact and open: the answer row (opts.keepInView), Check and the keypad in the window together.
    function together() { if (opts.keepInView) window.MaffsKeypad.together(opts.keepInView, panel, opts.foldInset); }

    if (host) {
      var t = null;
      window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { dock(); applyMode(); }, 100); });
    }
    dock();
    applyMode();

    toggle.addEventListener('click', function () { setOpen(panel.hidden); });
    closeBtn.addEventListener('click', function () { setOpen(false); });
    panel.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('.maffs-calc-key') : null;
      if (b && !b.disabled) press(b.getAttribute('data-act'), b.getAttribute('data-val'));
    });
    screen.addEventListener('click', function (e) {
      if (e.target !== closeBtn && answerMode()) select('calc');
    });
    // Keyboard: only while focus is inside the panel. Enter or Space on a focused key presses that key.
    panel.addEventListener('keydown', function (e) {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      var onKey = e.target !== panel;
      if ((e.key === 'Enter' || e.key === ' ') && onKey) return;
      var k = e.key;
      if (k === 'Enter' || k === '=') press('eq', '=');
      else if (k === 'Backspace') press('del', '');
      else if (k === 'Delete') press('clear', '');
      else if (k === 'Escape') { setOpen(false); toggle.focus(); }
      else if (KEYBOARD[k]) press('in', KEYBOARD[k]);
      else return;
      e.preventDefault();
    });

    return {
      el: el,
      open: function () { setOpen(true); },
      close: function () { setOpen(false); },
      isOpen: function () { return !panel.hidden; },
      isDocked: function () { return el.classList.contains('docked'); },
      isCompact: compact,
      answerMode: answerMode,
      target: function () { return target; },
      select: select,
      redock: function () { var d = dock(); applyMode(); return d; },
      // A new question: the calculator display clears and is selected again.
      clear: function () { select('calc'); press('clear', ''); },
      // For tests: press keys by their labels ('7', '×', 'x²', '√', 'DEL', 'C', '=').
      press: function (label) {
        var k = KEYS.filter(function (x) { return x[0] === label; })[0];
        if (k) press(k[1], k[2]);
      },
      display: function () { return { expr: exprEl.textContent, result: resEl.textContent }; }
    };
  }

  window.MaffsCalc = { evaluate: evaluate, format: format, calc: calc, mount: mount, KEYS: KEYS, DOCK: DOCK, ANSWER: ANSWER };
})();
