/* MaffsText — inline maths inside ordinary prose, without KaTeX eating the spaces.
 *
 * WHY THIS EXISTS
 * ---------------
 * component-crusher, factor-theorem and test-the-claim all pass a whole mixed
 * string -- prose AND maths together -- to K()/katex.renderToString() as one
 * math-mode expression. Math mode has no concept of a word boundary, so every
 * space between English words vanishes and letters run together and
 * italicise: "Find the angle between a and b to 1 d.p." becomes
 * "Findtheanglebetweenaandbto1d.p." (checker tier 4 layer A, rule B7). This
 * is a rendering-layer bug, not a content bug -- the fix is a renderer that
 * knows which parts of a string are prose and which are maths, not a rewrite
 * of every prompt into pure LaTeX (most of them are genuinely English
 * sentences with a symbol or two embedded, e.g. "d.p." or "\mathbf{a}").
 *
 * THE CONVENTION
 * ---------------
 * Wrap only the maths in `\( ... \)`; leave the prose around it as plain
 * text: 'Find the angle between \(\mathbf{a}\) and \(\mathbf{b}\) to 1 d.p.'
 * MaffsText.html() splits on that delimiter, HTML-escapes the prose
 * segments, and renders each maths segment through KaTeX on its own (inline,
 * not display mode) -- so the prose keeps its spaces and the maths still
 * renders as maths.
 *
 * A string with NO `\( ... \)` in it is treated as plain text and returned
 * HTML-escaped, not rendered as KaTeX. This is deliberate: a game's older,
 * pure-maths fields (`'Find \mathbf{a} + \mathbf{b}.'`, authored with no
 * delimiters, meant to go through K() as a whole expression) must keep doing
 * exactly that -- MaffsText is for MIXED strings only, not a drop-in
 * replacement for K(). `MaffsText.hasMaths(str)` is how a caller tells the
 * two apart: true means "this was authored with \( \) and belongs in
 * MaffsText.html", false means "this is a whole-expression string, keep
 * sending it to K() unchanged".
 *
 * Never `$...$` -- this platform's word-problem and money games use a literal
 * `$` for currency in ordinary prose ("costs $12"), so `$` cannot be
 * repurposed as a maths delimiter without colliding with real content.
 *
 * USAGE
 * -----
 *   MaffsText.hasMaths(sq.prompt)
 *     ? MaffsText.html(sq.prompt)   // authored with \( \), mixed prose+maths
 *     : K(sq.prompt)                // no delimiters, whole-expression string
 *
 * Rendering never throws: each maths segment is rendered with
 * `{throwOnError: false}`, so a malformed segment shows KaTeX's own inline
 * error styling instead of breaking the page. Authoring mistakes (unbalanced
 * delimiters, a segment KaTeX can't parse at all) are caught ahead of time by
 * checker tier 4 layer A's B7 rule, not silently shipped.
 */
(function () {
  'use strict';

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  var DELIM = /\\\(([\s\S]*?)\\\)/g;

  function hasMaths(str) {
    if (typeof str !== 'string') return false;
    DELIM.lastIndex = 0;
    return DELIM.test(str);
  }

  function html(str) {
    if (typeof str !== 'string') return '';
    var out = '';
    var last = 0;
    var m;
    DELIM.lastIndex = 0;
    while ((m = DELIM.exec(str))) {
      out += escapeHtml(str.slice(last, m.index));
      out += (typeof katex !== 'undefined')
        ? katex.renderToString(m[1], { throwOnError: false })
        : escapeHtml(m[0]);
      last = m.index + m[0].length;
    }
    out += escapeHtml(str.slice(last));
    return out;
  }

  window.MaffsText = { html: html, hasMaths: hasMaths };
})();
