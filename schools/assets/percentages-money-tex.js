/* MaffsPercentagesMoneyTex: the percentages-and-money bank's plain-text working as KaTeX (contract FEEDBACK-TEACHES part 3, build lane, 28 Oct 2026).
 *
 * The bank (percentages-money-generator.js) writes its working in plain text: "New price = £400 − £40 = £360.", "2 × £2 = £4",
 * "500 × 1.08^2 = 583.2". Canon 7.1.1 wants expressions like these through KaTeX. The bank's strings are NOT rewritten (The 6 P's copies them);
 * a page converts as it renders:
 *
 *   MaffsPercentagesMoneyTex.texify('New price = £400 − £40 = £360.')
 *     -> 'New price = \\(\\pounds 400 - \\pounds 40 = \\pounds 360\\).'
 *
 * Only a RUN of terms joined by x, /, minus, plus or equals is converted: a term is a number, with an optional pound sign before it, a percent
 * sign after it and a whole-number power (1.08^2). A lone number, a lone price ("£24"), "10% of £240" and a sign with nothing either side
 * ("(÷ 10)") are left as written. Pure data, no DOM; the page renders what is between \\( and \\) with KaTeX.
 */
(function (root) {
  'use strict';

  var TERM = '\\u00a3?\\d+(?:\\.\\d+)?%?(?:\\^\\d+)?';
  var RUN = new RegExp(TERM + '(?:\\s*[\\u00d7\\u00f7\\u2212+=]\\s*' + TERM + ')+', 'g');

  function texify(text) {
    return String(text == null ? '' : text).replace(RUN, function (m) {
      return '\\(' + m.replace(/£/g, '\\pounds ').replace(/%/g, '\\%').replace(/×/g, '\\times ').replace(/÷/g, '\\div ').replace(/−/g, '-') + '\\)';
    });
  }

  root.MaffsPercentagesMoneyTex = { texify: texify };
})(typeof window !== 'undefined' ? window : globalThis);
