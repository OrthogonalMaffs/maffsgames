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
 *   MaffsAnswer.fraction(raw)          the exact reading of a typed fraction a/b (a sign on either
 *                                      part, spaces round the slash) or a whole number: {num, den}
 *                                      in lowest terms with den > 0, or null (a decimal, b = 0,
 *                                      anything else). Exact: no float is formed.
 *   MaffsAnswer.fractionOrDecimal(raw, num, den, dp)  the key is the exact fraction num/den. An
 *                                      answer with a slash is read by fraction(): equal in value
 *                                      (3/7, 6/14, -3/-7) is 'correct', any other fraction 'wrong'.
 *                                      Anything else goes to decimal() against num/den rounded
 *                                      half up, exactly, to dp places: 0.429 'correct', 0.4286
 *                                      'format', 0.43 'wrong' for 3/7 at 3 d.p.
 *   MaffsAnswer.fractionForm(raw, key, opts)  a typed fraction judged by VALUE and by FORM (20 Oct 2026; How
 *                                      Many Parts?). key = {num, den} or {whole, num, den} (a negative whole
 *                                      makes the whole number negative); opts.form = 'simplest' (default) or
 *                                      'mixed'. Reads "a/b", "-a/b", "w a/b" (also "-w a/b") and whole numbers,
 *                                      spaces tolerated; no decimals, no sign on the denominator, no zero
 *                                      denominator (all 'unreadable'). Never reduces what was typed:
 *                                        'correct'  equal in value and in the asked form. 'simplest': lowest
 *                                                   terms, or a whole number when the key is one. 'mixed': a
 *                                                   whole number when the key is one, else a mixed number with
 *                                                   a proper fractional part in lowest terms (a key under 1 in
 *                                                   magnitude has no whole part: a proper fraction in lowest
 *                                                   terms);
 *                                        'format'   equal in value, wrong form: not in lowest terms (2/4, 6/3,
 *                                                   0/5 for 0), improper when mixed is asked (7/4), or mixed
 *                                                   when it is not asked (1 3/4 under 'simplest'). NEVER
 *                                                   MARKED, like every 'format';
 *                                        'wrong'    a different value;
 *                                        'unreadable'.
 *   MaffsAnswer.parse(raw)             the typed value as a Number, or null if unreadable.
 *   MaffsAnswer.message(result, raw, opts)  the words to show for 'format' / 'unreadable';
 *                                      opts.currency ('£' or '€') for money, opts.dp for decimal,
 *                                      opts.sf when the question states significant figures (the
 *                                      marking is still at opts.dp places), opts.fraction when a
 *                                      fraction is accepted too: true (a fraction or a decimal), or, for
 *                                      fractionForm(), 'simplest' / 'mixed' (the form messages).
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

  var FRACTION = /^([+-]?)(\d+)(?:\s*\/\s*([+-]?)(\d+))?$/;
  function gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }

  function fraction(raw) {
    var m = FRACTION.exec(strip(raw, false));
    if (!m) return null;
    var num = Number(m[2]), den = m[4] === undefined ? 1 : Number(m[4]);
    if (!den || !Number.isSafeInteger(num) || !Number.isSafeInteger(den)) return null;
    var g = gcd(num, den);
    num /= g; den /= g;
    return { num: num && (m[1] === '-') !== (m[3] === '-') ? -num : num, den: den };
  }

  // fractionForm(): value and form, never reducing what was typed. Reads whole numbers, a/b and w a/b.
  var FF_INT = /^([+-]?)(\d+)$/, FF_FRAC = /^([+-]?)(\d+)\s*\/\s*(\d+)$/, FF_MIXED = /^([+-]?)(\d+)\s+(\d+)\s*\/\s*(\d+)$/;

  function ffRead(raw) {
    var s = strip(raw, false), m, neg, w, a, b;
    if ((m = FF_INT.exec(s))) { w = Number(m[2]); a = 0; b = 1; neg = m[1] === '-'; m = { shape: 'int' }; }
    else if ((m = FF_FRAC.exec(s))) { w = 0; a = Number(m[2]); b = Number(m[3]); neg = m[1] === '-'; m = { shape: 'frac' }; }
    else if ((m = FF_MIXED.exec(s))) { w = Number(m[2]); a = Number(m[3]); b = Number(m[4]); neg = m[1] === '-'; m = { shape: 'mixed' }; }
    else return null;
    if (!b || !Number.isSafeInteger(w) || !Number.isSafeInteger(a) || !Number.isSafeInteger(b)) return null;
    var n = w * b + a;
    if (!Number.isSafeInteger(n)) return null;
    m.n = neg ? -n : n; m.d = b; m.w = w; m.a = a;
    return m;
  }

  function fractionForm(raw, key, opts) {
    var r = ffRead(raw);
    if (!r) return 'unreadable';
    var kd = key.den, kw = key.whole || 0, kn = Math.abs(kw) * kd + key.num;
    if (kw < 0) kn = -kn;
    if (r.n * kd !== kn * r.d) return 'wrong';
    var kInt = kn % kd === 0, lowest = gcd(Math.abs(r.n), r.d) === 1;
    if (kInt) return r.shape === 'int' ? 'correct' : 'format';
    if (opts && opts.form === 'mixed') {
      if (Math.abs(kn) < kd) return r.shape === 'frac' && r.a < r.d && lowest ? 'correct' : 'format';
      return r.shape === 'mixed' && r.w > 0 && r.a > 0 && r.a < r.d && gcd(r.a, r.d) === 1 ? 'correct' : 'format';
    }
    return r.shape === 'frac' && lowest ? 'correct' : 'format';
  }

  // num/den rounded half up (away from zero on the magnitude) to dp places, as a decimal string,
  // worked in integers.
  function fractionAt(num, den, dp) {
    if (den < 0) { num = -num; den = -den; }
    var p = Math.pow(10, dp), n = Math.abs(num) * p;
    var q = Math.floor((2 * n + den) / (2 * den));
    return (num < 0 && q ? '-' : '') + (q / p).toFixed(dp);
  }

  function fractionOrDecimal(raw, num, den, dp) {
    var s = strip(raw, false);
    if (s.indexOf('/') === -1) return decimal(s, fractionAt(num, den, dp), dp);
    var f = fraction(s);
    if (!f) return 'unreadable';
    return f.num * den === num * f.den ? 'correct' : 'wrong';
  }

  function message(result, raw, opts) {
    opts = opts || {};
    if (result === 'unreadable') {
      if (opts.fraction === 'simplest') return 'Type a fraction or a whole number, e.g. 3/7';
      if (opts.fraction === 'mixed') return 'Type a mixed number, e.g. 1 3/4';
      return opts.fraction ? 'Type a fraction or a decimal, e.g. 3/7 or 0.429' : 'Type just the number, e.g. 12.34';
    }
    if (result !== 'format') return '';
    var fig = strip(raw, !!opts.currency);
    if (opts.fraction === 'simplest') return 'Right value, but simplify it fully. In the exam, ' + fig + ' may lose the mark. Fix it and resubmit.';
    if (opts.fraction === 'mixed') {
      return 'Right value, but write it as a mixed number in its simplest form. In the exam, ' + fig + ' may lose the mark. Fix it and resubmit.';
    }
    if (opts.currency) {
      return 'Right amount, but money always has two decimal places. In the exam, ' + opts.currency +
        fig + ' loses the mark. Fix it and resubmit.';
    }
    var asked = opts.sf ? opts.sf + ' significant figure' + (opts.sf === 1 ? '' : 's')
      : opts.dp + ' decimal place' + (opts.dp === 1 ? '' : 's');
    return 'Right value, but the question asks for ' + asked +
      '. In the exam, ' + fig + ' loses the mark. Fix it and resubmit.';
  }

  window.MaffsAnswer = { money: money, decimal: decimal, exact: exact, fraction: fraction,
    fractionOrDecimal: fractionOrDecimal, fractionForm: fractionForm, parse: parse, message: message };
})();
