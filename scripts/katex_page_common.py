"""The KaTeX rule for a page that renders its maths on load: one definition (contract KATEX-ERRORS, 23 Nov 2026).

Every page renders KaTeX with throwOnError:false, so a LaTeX mistake does not throw: KaTeX shows its source in red, as
a .katex-error span whose title is its message, and the page goes on. An unclosed brace never even reaches KaTeX on a
page that uses auto-render: auto-render matches braces looking for the closing delimiter, so the source stays on the
page as raw text. A rendered page is therefore checked for both, and nothing else here judges it:

  * any .katex-error: a fault naming its source and KaTeX's message;
  * maths left unrendered: the page's text still shows a \\( \\) or $$ delimiter, or its source has maths and the
    page has no .katex at all (KaTeX never ran).

The rule began in check-uses.py (WWIUT-CARD-FORMAT, 22-23 Nov 2026); check-uses.py now imports it from here, with the
same results, and scripts/check-katex-pages.py runs it over every other page outside games/ that loads KaTeX.
Playwright's sync API, as both callers use.
"""
import re

# What the page shows: whether its text still carries a maths delimiter, each .katex-error as [source, message], and
# how many .katex elements it has.
STATE_JS = r"""() => {
  const raw = /\\\(|\\\)|\$\$/.test(document.body.innerText);
  // KaTeX renders with throwOnError:false, so a LaTeX mistake becomes .katex-error (its source, its message as title)
  const kerr = [...document.querySelectorAll('.katex-error')].map(e => [e.textContent, e.getAttribute('title') || '']);
  return {raw, kerr, katex: document.querySelectorAll('.katex').length};
}"""

# Waits until KaTeX has drawn something, or the page shows no delimiter (KaTeX renders on its script's load).
WAIT_JS = r"""() => document.querySelector('.katex') || !/\\\(|\$\$/.test(document.body.innerText)"""


_SCRIPT_BODY = re.compile(r"(<script\b[^>]*>).*?(</script>)", re.S | re.I)


def has_maths(source):
    """True when a page's source carries maths for KaTeX to render on load: a \\( or a $$ delimiter outside a script's
    code. The code is left out (a game-like page builds its maths in script as it is played, the-6-ps among them) but
    a script tag's own attributes are kept: auto-render's onload names its delimiters there, so a page that loads it
    is a page with maths to render."""
    page = _SCRIPT_BODY.sub(r"\1\2", source)
    return "\\(" in page or "$$" in page


def wait_rendered(page, maths, timeout=5000):
    """On a page with maths, wait (up to `timeout` ms) for KaTeX to render; left unrendered, faults() reports it."""
    if not maths:
        return
    try:
        page.wait_for_function(WAIT_JS, timeout=timeout)
    except Exception:
        pass


def state(page):
    """STATE_JS's reading of the page."""
    return page.evaluate(STATE_JS)


def faults(where, st, maths):
    """[fault] for one page reading (`where` names the page, size and mode), in this order: unrendered, each error."""
    out = []
    if st["raw"] or (maths and not st["katex"]):
        out.append("%s: shows KaTeX source it did not render" % where)
    for src, msg in st["kerr"]:
        out.append("%s: KaTeX error on \"%s\": %s" % (where, src, msg))
    return out
