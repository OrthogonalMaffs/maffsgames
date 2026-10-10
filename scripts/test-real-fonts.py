#!/usr/bin/env python3
# ci-line: Real fonts for the phone checks (scripts/fonts/ pinned and complete; the phone pass measures in them, the old font-blocking planted and caught) |
# ci-deps: scripts/fonts/ scripts/bank_common.py
"""The fonts the phone-fit checks draw pages in (contract FONT-FIT, 10 Oct 2026).

    python scripts/test-real-fonts.py

  pinned    every file in scripts/fonts/ matches SHA256SUMS, and SHA256SUMS names no missing file
  complete  every Google Fonts stylesheet a page in the repo asks for (each distinct css2 URL in .html, .js and
            .css) has a pinned copy, and so does every font file those copies name: a page that changed its link
            and was not re-fetched (scripts/fonts/fetch-fonts.py) would quietly be measured in the fallback font
  KaTeX     every KaTeX 0.16.9 file a page loads (katex.min.css, katex.min.js, contrib/auto-render.min.js) and every
            font file katex.min.css names is pinned
  decides   the fonts change a verdict the phone pass gives: distinctly-average at 320x568 is 334px wide in the
            real fonts (its Aa toggle; the page is set in Nunito) and fits with Google Fonts blocked. The plant is the old font-blocking
            (Google Fonts aborted): the width must change, or the check is not measuring in the real fonts.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

FONTS = bc.FONTS_DIR
CSS2 = re.compile(r"https://fonts\.googleapis\.com/css2\?[^\"'\s)<>]+")


def pinned(fails):
    listed = {}
    for line in open(os.path.join(FONTS, "SHA256SUMS"), encoding="utf-8"):
        digest, rel = line.rstrip("\n").split("  ", 1)
        listed[rel] = digest
    for rel, digest in listed.items():
        p = os.path.join(FONTS, rel)
        if not os.path.isfile(p):
            fails.append("pinned: %s is in SHA256SUMS but missing" % rel)
        elif hashlib.sha256(open(p, "rb").read()).hexdigest() != digest:
            fails.append("pinned: %s does not match its checksum" % rel)
    for d, _, files in os.walk(FONTS):
        for f in files:
            rel = os.path.relpath(os.path.join(d, f), FONTS).replace(os.sep, "/")
            if rel not in listed and rel not in ("SHA256SUMS", "README.md", "fetch-fonts.py") and not rel.startswith("licences/"):
                fails.append("pinned: %s is not in SHA256SUMS" % rel)
    return len(listed)


def complete(fails):
    urls = set()
    for d, dirs, files in os.walk(bc.ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules" and os.path.join(d, x) != FONTS]
        for f in files:
            if f.endswith((".html", ".js", ".css")):
                txt = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                urls.update(u.replace("&amp;", "&") for u in CSS2.findall(txt))
    for u in sorted(urls):
        css = bc.real_font_file(u)
        if not css:
            fails.append("complete: no pinned copy of %s (run scripts/fonts/fetch-fonts.py)" % u)
            continue
        for f in re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", open(css, encoding="utf-8").read()):
            if not bc.real_font_file(f):
                fails.append("complete: %s names %s, which is not pinned" % (u, f))
    for f in ("katex.min.css", "katex.min.js", "contrib/auto-render.min.js"):
        if not bc.real_font_file(bc.KATEX_CDN + f):
            fails.append("KaTeX: %s is not pinned" % f)
    css = open(bc.real_font_file(bc.KATEX_CDN + "katex.min.css"), encoding="utf-8").read()
    for f in sorted(set(re.findall(r"url\((fonts/[^)]+\.woff2)\)", css))):
        if not bc.real_font_file(bc.KATEX_CDN + f):
            fails.append("KaTeX: %s is not pinned" % f)
    return len(urls)


WIDTH_JS = "() => document.documentElement.scrollWidth"


def width_at_320(fonts):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={"width": 320, "height": 568})
            ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
            if fonts == "real":
                ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font)
            else:   # the old way: Google Fonts blocked, KaTeX real
                ctx.route(lambda u: u.startswith(bc.KATEX_CDN), bc.serve_real_font)
            page = ctx.new_page()
            page.goto(base + "/games/distinctly-average/?cb=fonts", wait_until="load", timeout=20000)
            page.evaluate("() => document.fonts.ready")
            page.wait_for_timeout(200)
            loaded = page.evaluate("() => [...document.fonts].filter(f => f.status === 'loaded' && !/KaTeX/.test(f.family))"
                                   ".map(f => f.family.replace(/[\"']/g, '')).filter((x, k, a) => a.indexOf(x) === k).join(', ')")
            w = page.evaluate(WIDTH_JS)
            browser.close()
            return w, loaded
    finally:
        proc.terminate()
        proc.wait()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fails = []
    n_files = pinned(fails)
    n_css = complete(fails)
    real_w, real_outfit = width_at_320("real")
    old_w, old_outfit = width_at_320("fallback")
    print("pinned: %d files match SHA256SUMS; complete: %d Google Fonts stylesheets and KaTeX 0.16.9 pinned" % (n_files, n_css))
    print("decides: distinctly-average at 320x568 is %dpx wide in the real fonts (Google faces loaded: %s), %dpx with "
          "Google Fonts blocked (loaded: %s)" % (real_w, real_outfit or "none", old_w, old_outfit or "none"))
    if not real_outfit:
        fails.append("decides: no Google face loaded from the pinned copies")
    if old_outfit:
        fails.append("decides: with Google Fonts blocked, %s still loaded: the plant did not take" % old_outfit)
    if real_w == old_w:
        fails.append("decides: the same width (%dpx) in the real fonts and with them blocked: the phone pass would not "
                     "see the fonts" % real_w)
    print("  self-test the old font-blocking (Google Fonts aborted)  %s" % (
        "caught: the width changes from %dpx to %dpx" % (real_w, old_w) if real_w != old_w else "*** MISSED ***"))
    for f in fails:
        print("FAIL  " + f)
    print("FAILED" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
