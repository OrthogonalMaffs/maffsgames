/* MaffsAnswer — marking a typed numeric answer (canon §7.1.3). One copy, for every game.
 *
 * Every function reads the RAW typed string, never a number parsed by the game: 114.4 and 114.40
 * are the same number but not the same answer. Each returns one of
 *   'correct'    the answer, in an accepted form;
 *   'wrong'      a different value;
 *   'format'     the right value in the wrong form (money not at 2 d.p.; a rounded answer given
 *                unrounded). NEVER MARKED: no score change, no penalty, no analytics event. The
 *                game shows MaffsAnswer.message('format', ...) and the student resubmits;
 *   'unreadable' not a number at all (empty, "12abc", "1,250"). NEVER MARKED: the game shows
 *                MaffsAnswer.message('unreadable').
 *
 *   MaffsAnswer.money(raw, key)        key in pounds (or euros) at the penny. An optional leading
 *                                      £ or € is accepted. Pence answers need exactly 2 d.p.; a
 *                                      whole-pound key also accepts an integer. 1250.7, 3050.0 and
 *                                      1250.700 are 'format'.
 *   MaffsAnswer.decimal(raw, key, dp)  the question states dp decimal places and key is already
 *                                      rounded to them. Any form equal in value is 'correct'
 *                                      (2.5, 2.50); a value that rounds (half up) to the key but
 *                                      is not equal to it is 'format' (333.33 when 333.3 is asked).
 *   MaffsAnswer.exact(raw, key)        an answer that needs no rounding (whole-number ratios, an
 *                                      integer scale factor): equal in value or 'wrong'. Nothing is
 *                                      'format', since no precision was asked for.
 *   MaffsAnswer.parse(raw)             the typed value as a Number, or null if unreadable.
 *   MaffsAnswer.message(result, raw, opts)  the words to show for 'format' / 'unreadable';
 *                                      opts.currency ('£' or '€') for money, opts.dp for decimal.
 *
 * scripts/test-answer-js.py runs every outcome in a browser, in CI.
 */
(function () {
  'use strict';
  // A plain decimal number, optionally signed, with an optional exponent (a type="number" input
  // can hand a game "1e3" or ".5"). Nothing else: no thousands commas, no units.
  var NUM = /^([+-]?)(\d*)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/;
  var CURRENCY = /^[£€]\s*/;

  function strip(raw, allowCurrency) {
    var s = String(raw == null ? '' : raw).trim();
    return allowCurrency ? s.replace(CURRENCY, '') : s;
  }

  // Exact decimal: {neg, digits, scale} with value = (neg ? -1 : 1) * digits / 10^scale.
  function read(s) {
    var m = NUM.exec(s);
    if (!m || (m[2] === '' && (m[3] === undefined || m[3] === ''))) return null;
    var intPart = m[2], frac = m[3] || '', exp = m[4] ? parseInt(m[4], 10) : 0;
    var digits = (intPart + frac).replace(/^0+(?=\d)/, '') || '0';
    var scale = frac.length - exp;
    if (scale < 0) { digits += new Array(-scale + 1).join('0'); scale = 0; }
    return { neg: m[1] === '-' && /[1-9]/.test(digits), digits: digits, scale: scale, text: s };
  }

  // The value times 10^dp as an integer, worked on the digit string so no float rounding creeps in
  // (answers are a dozen digits at most, well inside Number's exact-integer range).
  function scaledExact(d, dp) {
    // null if d has non-zero digits beyond dp places
    if (d.scale <= dp) return sign(d) * Number(d.digits) * Math.pow(10, dp - d.scale);
    var cut = d.digits.length - (d.scale - dp);
    var head = cut > 0 ? d.digits.slice(0, cut) : '0', tail = cut > 0 ? d.digits.slice(cut) : pad(d.digits, d.scale - dp);
    return /^0*$/.test(tail) ? sign(d) * Number(head) : null;
  }
  function scaledHalfUp(d, dp) {
    // rounded half up (away from zero on the magnitude) to dp places
    if (d.scale <= dp) return scaledExact(d, dp);
    var cut = d.digits.length - (d.scale - dp);
    var head = cut > 0 ? Number(d.digits.slice(0, cut)) : 0;
    var next = cut >= 0 ? d.digits.charAt(cut) : '0';
    return sign(d) * (head + (Number(next) >= 5 ? 1 : 0));
  }
  function pad(digits, len) { while (digits.length < len) digits = '0' + digits; return digits; }
  function sign(d) { return d.neg ? -1 : 1; }
  function keyScaled(key, dp) { return Math.round(Number(key) * Math.pow(10, dp)); }

  function parse(raw) {
    var d = read(strip(raw, true));
    return d ? Number(d.text) : null;
  }

  function money(raw, key) {
    var s = strip(raw, true), d = read(s);
    if (!d) return 'unreadable';
    var keyP = keyScaled(key, 2);
    // Compared as a number first (canon §7.1.3), exactly as tax-theft always has.
    if (Math.abs(Number(s) * 100 - keyP) > 1e-6) return 'wrong';
    var written = keyP % 100 === 0 ? /^\d+(\.\d\d)?$/ : /^\d+\.\d\d$/;
    return written.test(s) ? 'correct' : 'format';
  }

  function decimal(raw, key, dp) {
    var d = read(strip(raw, false));
    if (!d) return 'unreadable';
    var k = keyScaled(key, dp), v = scaledExact(d, dp);
    if (v === k) return 'correct';
    return scaledHalfUp(d, dp) === k ? 'format' : 'wrong';
  }

  function exact(raw, key) {
    var d = read(strip(raw, false));
    if (!d) return 'unreadable';
    var dp = Math.max(d.scale, 0), k = Number(key) * Math.pow(10, dp);
    return scaledExact(d, dp) === Math.round(k) && Math.abs(k - Math.round(k)) < 1e-6 ? 'correct' : 'wrong';
  }

  function message(result, raw, opts) {
    opts = opts || {};
    if (result === 'unreadable') return 'Type just the number, e.g. 12.34';
    if (result !== 'format') return '';
    var fig = strip(raw, !!opts.currency);
    if (opts.currency) {
      return 'Right amount, but money always has two decimal places. In the exam, ' + opts.currency +
        fig + ' loses the mark. Fix it and resubmit.';
    }
    var dp = opts.dp;
    return 'Right value, but the question asks for ' + dp + ' decimal place' + (dp === 1 ? '' : 's') +
      '. In the exam, ' + fig + ' loses the mark. Fix it and resubmit.';
  }

  window.MaffsAnswer = { money: money, decimal: decimal, exact: exact, parse: parse, message: message };
})();
