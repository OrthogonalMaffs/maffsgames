#!/usr/bin/env python3
# ci-line: Shared MaffsText (schools/assets/mathtext.js: punctuation next to inline maths never wraps away from it; the old renderer planted and caught) |
# ci-deps: schools/assets/mathtext.js games/core-maths-paper2c/
"""Browser test for the shared MaffsText renderer, schools/assets/mathtext.js (contract MATHTEXT-NOWRAP).

    python scripts/test-mathtext.py
    python scripts/test-mathtext.py --mathtext path/to/mathtext.js   # try another renderer
    python scripts/test-mathtext.py --selftest                       # the same cases against the old renderer: must FAIL

The fault: html() emitted KaTeX's span and the prose after it as separate inline content, so a line could
break between the maths and the punctuation straight after it (a line starting with "." or ")").
The rule now: closing punctuation right after a maths segment, and an opening bracket or quote right before
one, go inside one <span class="maffs-nowrap"> with the maths. Measured in Chromium by line box with KaTeX's
real (pinned) fonts, never by reading the markup alone.

  glued        each planted case (. , ; : ! ? ) closing quotes; an opening bracket or quote) puts the mark
               and the maths in one nowrap span, and prose elsewhere stays outside any span
  line box     the same strings in a narrow column at every width from 120 to 420 px: the mark is never
               on a lower line than the maths it belongs to
  unchanged    a string with no such punctuation renders byte-identical to the old renderer, and the
               prose is escaped as before
  reported     Core Maths Paper 2C Q14 at 390 px, Q9 and Q16 at 375, Q26 at 320 (the cloud lane's report,
               18 Oct 2026), played in the real game: no mark starts a line in the stem, an option or the
               working; and no question of the 36 does at 320, 375 or 390
  overflow     gluing makes no stem, option or working note wider than its container at 320 px

--selftest swaps in the previous html() and expects the line-box, glued and reported cases to fail.
Exits non-zero on any failure.
"""
import argparse
import asyncio
import functools
import http.server
import os
import re
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

DEFAULT_JS = os.path.join(ROOT, "schools", "assets", "mathtext.js")
GAME = "games/core-maths-paper2c/"
REPORTED = [(14, 390), (9, 375), (16, 375), (26, 320)]
SPREAD = 12

# The renderer as it was before the fix: the planted fault for --selftest, and the reference for "unchanged".
OLD_HTML = r"""
(function () {
  function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var D = /\\\(([\s\S]*?)\\\)/g;
  window.oldHtml = function (str) {
    if (typeof str !== 'string') return '';
    var out = '', last = 0, m;
    D.lastIndex = 0;
    while ((m = D.exec(str))) {
      out += esc(str.slice(last, m.index));
      out += (typeof katex !== 'undefined') ? katex.renderToString(m[1], { throwOnError: false }) : esc(m[0]);
      last = m.index + m[0].length;
    }
    return out + esc(str.slice(last));
  };
})();
"""

# In-page measurement. A mark "starts a line" when its first glyph sits below (or above) the maths box it follows.
MEASURE_JS = r"""
(function () {
  var CLOSE = '.,;:!?)]”’"\'', OPEN = '([“‘"\'';
  function mid(node, i) {
    var r = document.createRange();
    r.setStart(node, i); r.setEnd(node, i + 1);
    var rs = r.getClientRects();
    if (!rs.length) return null;
    return (rs[0].top + rs[0].bottom) / 2;
  }
  // Marks that sit on a different line from the maths beside them, in root.
  window.stray = function (root) {
    var bad = [];
    root.querySelectorAll('.katex').forEach(function (K) {
      var rs = K.getClientRects();
      if (!rs.length) return;
      var first = rs[0], last = rs[rs.length - 1];
      var n = K.nextSibling;
      if (n && n.nodeType === 3 && n.data && CLOSE.indexOf(n.data[0]) >= 0) {
        var m = mid(n, 0);
        if (m !== null && (m > last.bottom || m < last.top)) bad.push('after: ' + n.data.slice(0, 8));
      }
      var p = K.previousSibling;
      if (p && p.nodeType === 3 && p.data && OPEN.indexOf(p.data[p.data.length - 1]) >= 0) {
        var m2 = mid(p, p.data.length - 1);
        if (m2 !== null && (m2 > first.bottom || m2 < first.top)) bad.push('before: ' + p.data.slice(-8));
      }
    });
    return bad;
  };
  // The widest thing in root, against root's own width.
  window.overflow = function (root) {
    var box = root.getBoundingClientRect(), worst = 0;
    root.querySelectorAll('.maffs-nowrap, .katex').forEach(function (e) {
      var r = e.getBoundingClientRect();
      worst = Math.max(worst, r.right - box.right);
    });
    return Math.round(worst);
  };
})();
"""

FIXTURE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
</head><body style="margin:0;font:16px/1.5 sans-serif"><div id="col" style="width:300px"></div>
<script>%s</script><script>%s</script><script>%s</script></body></html>"""

# Planted strings. {} is where the mark under test goes.
CLOSERS = [".", ",", ";", ":", "!", "?", ")", "”", "’", "...", ".)", "”."]
CLOSING_TEMPLATE = "Work out the value of \\(x^2 + 3x = 28\\){} Then state how many solutions there are."
OPENING_CASES = [
    ("(", "Is the point (\\(3, 4\\)) on the line \\(y = x + 1\\) or not, given the rule?"),
    ("[", "Write the interval [\\(a, b\\)] using the values found earlier in the question."),
    ("“", "Why does the student call it “\\(f(x)\\)” when the graph is a curve?"),
    ("‘", "The label ‘\\(\\frac{3}{4}\\)’ was written on the board by the teacher."),
]
# No mark touches the maths: these must render exactly as before.
UNCHANGED = [
    "plain prose with no maths at all, and a < b & c > d",
    "Find \\(a\\) and \\(b\\) now",
    "Find \\(a\\) , then \\(b\\) .",
    "Between \\(a\\) and \\(b\\) lies <i>nothing</i> & more.",
    "Take \\(x\\) (then \\(y\\) ok) and compare",
    "x < \\(y\\) > z",
]


async def run(js, chromium, selftest):
    from playwright.async_api import async_playwright
    results = []

    def check(name, ok, detail=""):
        results.append((name, ok, detail))
        print("  %s  %-58s %s" % ("PASS" if ok else "FAIL", name, detail))

    handler = functools.partial(_Quiet, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/" % srv.server_address[1]
    swap = "MaffsText.html = oldHtml;" if selftest else ""

    async def route(r):
        url = r.request.url
        if url.startswith(base):
            if url.endswith("/analytics.js"):
                await r.fulfill(body="window.mfg=function(){};", content_type="application/javascript")
            elif url.endswith("/mathtext.js") and js != DEFAULT_JS:
                await r.fulfill(body=open(js, encoding="utf-8").read(), content_type="application/javascript")
            else:
                await r.continue_()
        elif bc.is_font_cdn(url):
            await bc.serve_real_font_async(r)
        else:
            await r.abort()

    async with async_playwright() as p:
        kw = {"executable_path": chromium} if chromium else {}
        browser = await p.chromium.launch(**kw)
        src = open(js, encoding="utf-8").read()

        async def fixture(width=1000):
            ctx = await browser.new_context(viewport={"width": width, "height": 800})
            await ctx.route("**/*", route)
            page = await ctx.new_page()
            await page.set_content(FIXTURE % (OLD_HTML, src, MEASURE_JS + swap))
            await page.wait_for_function("typeof katex !== 'undefined' && typeof MaffsText !== 'undefined'")
            await page.evaluate("document.fonts.ready")
            return ctx, page

        ctx, page = await fixture()

        # glued: the markup, read back through the DOM
        glue_js = """([s, mark, where]) => {
          const d = document.createElement('div'); d.innerHTML = MaffsText.html(s);
          const w = d.querySelectorAll('.maffs-nowrap');
          if (w.length !== 1) return 'spans=' + w.length;
          const e = w[0];
          if (!e.querySelector('.katex')) return 'no maths in the span';
          if (e.querySelectorAll('.katex-mathml').length !== 1) return 'mathml copies=' + e.querySelectorAll('.katex-mathml').length;
          const node = where === 'after' ? e.lastChild : e.firstChild;
          if (!node || node.nodeType !== 3 || node.data !== mark) return 'span edge=' + JSON.stringify(node && node.data);
          const prose = d.textContent.replace(e.textContent, '');
          if (!prose.length) return 'no prose outside the span';
          return '';
        }"""
        bad = []
        for m in CLOSERS:
            r = await page.evaluate(glue_js, [CLOSING_TEMPLATE.format(m), m, "after"])
            if r:
                bad.append("%s -> %s" % (m, r))
        check("closing marks glued to the maths (%d cases)" % len(CLOSERS), not bad, "; ".join(bad[:3]))
        bad = []
        for m, s in OPENING_CASES:
            r = await page.evaluate(glue_js, [s, m, "before"])
            if r:
                bad.append("%s -> %s" % (m, r))
        check("opening marks glued to the maths (%d cases)" % len(OPENING_CASES), not bad, "; ".join(bad[:3]))

        # unchanged: byte-identical to the old renderer when no mark touches the maths
        diff = await page.evaluate("(ss) => ss.filter(s => MaffsText.html(s) !== oldHtml(s))", UNCHANGED)
        check("no adjacent punctuation: byte-identical to before (%d strings)" % len(UNCHANGED), not diff, str(diff[:1]))
        esc = await page.evaluate("MaffsText.html('a <b> & \\\\(x\\\\)). <i>')")
        check("prose still escaped around a glued mark", "&lt;b&gt; &amp; " in esc and esc.endswith("</span> &lt;i&gt;"), esc[-60:])
        check("hasMaths unchanged", await page.evaluate(
            "MaffsText.hasMaths('a \\\\(x\\\\)') === true && MaffsText.hasMaths('a $x$') === false"))

        # line box: every width, every case; the mark never on a different line from its maths
        cases = [CLOSING_TEMPLATE.format(m) for m in CLOSERS] + [s for _, s in OPENING_CASES]
        scan = """async (cases) => {
          const col = document.getElementById('col'); const hits = {}; let tested = 0;
          for (let w = 120; w <= 420; w++) {
            col.style.width = w + 'px';
            for (const s of cases) {
              col.innerHTML = MaffsText.html(s);
              tested++;
              const b = stray(col);
              if (b.length) hits[s.slice(0, 40) + ' @' + w] = b[0];
            }
          }
          return {tested, hits};
        }"""
        res = await page.evaluate(scan, cases)
        keys = sorted(res["hits"])
        check("line box: no mark on another line, 120-420 px (%d renders)" % res["tested"], not keys,
              "%d stray, first: %s" % (len(keys), keys[0] + " " + res["hits"][keys[0]] if keys else ""))
        await ctx.close()

        # the cloud lane's four reported items, in the real game
        async def game(width):
            ctx = await browser.new_context(viewport={"width": width, "height": 800})
            await ctx.route("**/*", route)
            page = await ctx.new_page()
            await page.goto(base + GAME)
            await page.wait_for_function("typeof QUESTIONS !== 'undefined' && typeof MaffsText !== 'undefined' && typeof katex !== 'undefined'")
            await page.add_script_tag(content=OLD_HTML + MEASURE_JS + swap)
            await page.evaluate("document.fonts.ready")
            return ctx, page

        show = """async (n) => {
          showScreen('gameScreen');
          document.getElementById('sectionBanner').style.display = 'none';
          document.getElementById('questionArea').style.display = 'block';
          currentQ = n; showQuestion();
          const note = document.getElementById('workingNote');
          note.innerHTML = MaffsText.html(QUESTIONS[n].working); note.classList.add('visible');
          await document.fonts.ready;   // KaTeX's faces load on first use; measure in them, not the fallback
          await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
          const out = [];
          for (const sel of ['#qStem', '.option-text', '#workingNote']) {
            document.querySelectorAll(sel).forEach(e => { const b = stray(e); if (b.length) out.push(sel + ': ' + b[0]); });
          }
          return out;
        }"""
        for q, width in REPORTED:
            ctx, page = await game(width)
            bad = []
            for w in range(width - SPREAD, width + SPREAD + 1):   # the runner's scrollbar and fallback fonts differ from the report's
                await page.set_viewport_size({"width": w, "height": 800})
                out = await page.evaluate(show, q - 1)
                if out:
                    bad.append("%d px %s" % (w, out[0]))
            check("reported: Paper 2C Q%d at %d px (+/-%d): no mark starts a line" % (q, width, SPREAD), not bad,
                  "%d widths, first: %s" % (len(bad), bad[0]) if bad else "")
            await ctx.close()

        # all 36 at the three phone widths, and nothing wider than its container at 320
        for width in (320, 375, 390):
            ctx, page = await game(width)
            allbad = []
            worst = 0
            for n in range(36):
                out = await page.evaluate(show, n)
                if out:
                    allbad.append("Q%d %s" % (n + 1, out[0]))
                if width == 320:
                    for sel in ('#qStem', '.option-text', '#workingNote'):
                        w = await page.evaluate("(sel) => Math.max(0, ...[...document.querySelectorAll(sel)].map(overflow))", sel)
                        worst = max(worst, w)
            check("all 36 questions at %d px: no mark starts a line" % width, not allbad, "; ".join(allbad[:3]))
            if width == 320:
                check("320 px: nothing wider than its container", worst <= 0, "worst overhang %d px" % worst)
            await ctx.close()

        await browser.close()
    srv.shutdown()
    return results


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--mathtext", default=DEFAULT_JS)
    ap.add_argument("--selftest", action="store_true", help="run against the old html(): the cases must fail")
    ap.add_argument("--chromium", help="launch this Chromium binary instead of Playwright's own")
    args = ap.parse_args()
    print("mathtext.js:", os.path.relpath(args.mathtext, ROOT) if args.mathtext.startswith(ROOT) else args.mathtext,
          "(old html() swapped in)" if args.selftest else "")
    results = asyncio.run(run(args.mathtext, args.chromium, args.selftest))
    bad = [r for r in results if not r[1]]
    print("%d checks, %d failed" % (len(results), len(bad)))
    if args.selftest:
        must_fail = [r for r in results if re.match(r"(closing|opening|line box|reported|all 36 questions at (320|375))", r[0])]
        missed = [r[0] for r in must_fail if r[1]]
        print("self-test: %d of %d fault-sensitive checks failed on the old renderer" % (len(must_fail) - len(missed), len(must_fail)))
        for m in missed:
            print("  MISSED  %s" % m)
        sys.exit(1 if missed else 0)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
