/* MaffsFractionFeedback: what a typed fraction answer says back to the student (contract FEEDBACK-TEACHES, build lane, 28 Oct 2026).
 *
 * A right answer is often a different form from the one the bank stores (the student types 1/3, the bank holds 5/15). Feedback that only
 * shows the stored form ("P = 5/15") does not connect to what was typed. echo() returns the equation that does:
 *
 *   MaffsFractionFeedback.echo('1/3', { num: 5, den: 15 })  ->  { same: false, tex: '\\frac{1}{3} = \\frac{5}{15}', plain: '1/3 = 5/15' }
 *   MaffsFractionFeedback.echo('5/15', { num: 5, den: 15 }) ->  { same: true,  tex: '', plain: '' }      (nothing to add)
 *
 * The student's fraction is first, the stored form second ("1/3 = 4/12"). `same` is true when the two are written alike, and then there is
 * no equation to show. A wrong or unreadable raw gives { same: true, tex: '' } too: the echo is only for an answer that is equal in value.
 *
 * Pure data, no DOM: a page renders `tex` with KaTeX (canon 7.1.1, no plain-text fractions). This is a NEW shared file beside
 * fraction-input.js (which the Possibly, Maybe page uses for the two boxes); folding it into MaffsFractionInput is a job for after the
 * 2 Nov freeze (lanes notes file).
 */
(function (root) {
  'use strict';

  var RAW = /^\s*(\d+)\s*\/\s*(\d+)\s*$/;

  // "n/d" as typed, or null.
  function parse(raw) {
    var m = RAW.exec(String(raw == null ? '' : raw));
    if (!m) return null;
    var n = parseInt(m[1], 10), d = parseInt(m[2], 10);
    return d === 0 ? null : { num: n, den: d };
  }

  function frac(n, d) { return '\\frac{' + n + '}{' + d + '}'; }

  function echo(raw, key) {
    var f = parse(raw), none = { same: true, tex: '', plain: '' };
    if (!f || !key || !(key.den > 0)) return none;
    if (f.num * key.den !== key.num * f.den) return none;              // not equal in value: nothing to say here
    if (f.num === key.num && f.den === key.den) return none;           // written the same way
    return { same: false, tex: frac(f.num, f.den) + ' = ' + frac(key.num, key.den), plain: f.num + '/' + f.den + ' = ' + key.num + '/' + key.den };
  }

  root.MaffsFractionFeedback = { echo: echo, parse: parse };
})(typeof window !== 'undefined' ? window : globalThis);
