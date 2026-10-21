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
 * Punctuation touching a maths segment never wraps away from it: a closing mark right
 * after (. , ; : ! ? ) and closing quotes) or an opening bracket/quote right before goes
 * inside one <span class="maffs-nowrap"> with the maths (scripts/test-mathtext.py).
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

  // Punctuation that must stay on the line of the maths beside it: closing marks after
  // a maths segment, opening marks before one. Without this the browser may break the
  // line between the maths and the mark ("... = 12" / ".").
  var CLOSING = /^[.,;:!?)\]”’"']+/;
  var OPENING = /[(\[“‘"']+$/;
  var HEAD = '<span class="katex-html" aria-hidden="true">';
  var BASE = '<span class="base">';
  var TAIL = '</span></span>';

  // The rendered maths with the marks fixed to it, in one nowrap span. The inline style is the
  // rule itself, because most MaffsText games do not link theme.css (the class carries no
  // other rule). A long expression must still wrap between its own pieces (KaTeX's
  // .base blocks), so the maths is split there: only the base beside a mark stays in the nowrap
  // run (Chromium breaks after an inline-block unless the block's parent forbids it), and the
  // rest keeps normal wrapping. The accessible MathML stays in the first piece only.
  function glue(rendered, open, close) {
    var h = rendered.indexOf(HEAD);
    var inner = h < 0 || rendered.slice(-TAIL.length) !== TAIL ? '' : rendered.slice(h + HEAD.length, -TAIL.length);
    var bases = inner.indexOf(BASE) === 0 ? inner.split(BASE).slice(1) : [];
    var body = rendered;
    if (bases.length > 1) {
      bases = bases.map(function (b) { return BASE + b; });
      var parts = [];
      if (open) parts.push({ b: bases.shift(), wrap: true });
      var tail = close ? bases.pop() : null;
      if (bases.length) parts.push({ b: bases.join(''), wrap: true });
      if (tail) parts.push({ b: tail, wrap: false });
      var pre = rendered.slice(0, h);
      body = parts.map(function (p, k) {
        return (k === 0 ? pre : '<span class="katex">') +
          HEAD.replace('">', '"' + (p.wrap ? ' style="white-space:normal"' : '') + '>') + p.b + TAIL;
      }).join('');
    }
    return '<span class="maffs-nowrap" style="white-space:nowrap">' + escapeHtml(open) + body + escapeHtml(close) + '</span>';
  }

  function html(str) {
    if (typeof str !== 'string') return '';
    var out = '';
    var last = 0;
    var m;
    DELIM.lastIndex = 0;
    while ((m = DELIM.exec(str))) {
      var prose = str.slice(last, m.index);
      var open = (OPENING.exec(prose) || [''])[0];
      out += escapeHtml(prose.slice(0, prose.length - open.length));
      var rendered = (typeof katex !== 'undefined')
        ? katex.renderToString(m[1], { throwOnError: false })
        : escapeHtml(m[0]);
      last = m.index + m[0].length;
      var close = (CLOSING.exec(str.slice(last)) || [''])[0];
      last += close.length;
      out += (open || close) ? glue(rendered, open, close) : rendered;
    }
    out += escapeHtml(str.slice(last));
    return out;
  }

  window.MaffsText = { html: html, hasMaths: hasMaths };
})();
