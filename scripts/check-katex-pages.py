#!/usr/bin/env python3
"""KaTeX on the pages that render it on load (contract KATEX-ERRORS, 23 Nov 2026): no .katex-error, no maths left as
raw source, on every page outside games/ that loads KaTeX.

    python -X utf8 scripts/check-katex-pages.py             # CI: every such page, in Chromium
    python -X utf8 scripts/check-katex-pages.py --selftest  # the plants must be caught, an untouched page must pass

The rule is scripts/katex_page_common.py's, the one check-uses.py uses for "When will I use this?" (whose pages it
checks itself, at two sizes and in Aa, so they are left to it here). Games are not pages that render on load: what
they hand KaTeX is checked as they are played (check-site.py tier 3) and from their banks (check-banks.py B12).

The pages are found, not listed: every tracked .html file outside games/ and when-will-i-use-this/ that loads
KaTeX's script. Today that is the 20 parent guides (parents/*/index.html, auto-render), the portal (index.html, which
loads KaTeX and renders nothing on load) and the-6-ps/index.html (which renders as it is played: on load it shows no
maths, so this check reaches only what it draws before play). Each page is served from the checkout and loaded once at
390x844; KaTeX comes from the pinned copy in scripts/fonts/ (bank_common.real_font_response), nothing from the network.
"""
import argparse
import mimetypes
import os
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402
import katex_page_common as kp  # noqa: E402

ROOT = bc.ROOT
ORIGIN = "http://katex-pages.test"
LEFT_TO_OTHERS = ("games/", "when-will-i-use-this/")
LOADS_KATEX = re.compile(r"""<script[^>]+src=["'][^"']*katex(?:\.min)?\.js""", re.I)


def pages():
    """Every tracked .html page outside games/ and when-will-i-use-this/ that loads KaTeX's script, sorted."""
    tracked = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    out = []
    for rel in sorted(tracked):
        if rel.startswith(LEFT_TO_OTHERS):
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            if LOADS_KATEX.search(fh.read()):
                out.append(rel)
    return out


def url_for(rel):
    return ORIGIN + "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel) + "?cb=katex-pages"


def browse(rels, planted=None):
    """{rel: [fault]} for each page. `planted` maps a rel to the page text to serve in place of the checkout's."""
    from playwright.sync_api import sync_playwright
    planted = planted or {}
    out = {}

    def route(r):
        u = r.request.url
        got = bc.real_font_response(u)
        if got:
            return r.fulfill(**got)
        if u.startswith(ORIGIN):
            path = unquote(urlsplit(u).path).lstrip("/")
            if path == "" or path.endswith("/"):
                path += "index.html"
            if path in planted:
                return r.fulfill(status=200, body=planted[path].encode("utf-8"), content_type="text/html")
            f = os.path.join(ROOT, path)
            if os.path.isfile(f):
                with open(f, "rb") as fh:
                    body = fh.read()
                return r.fulfill(status=200, body=body,
                                 content_type=mimetypes.guess_type(f)[0] or "application/octet-stream")
            return r.fulfill(status=404, body=b"")
        return r.abort()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for rel in rels:
                if rel in planted:
                    src = planted[rel]
                else:
                    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                        src = fh.read()
                maths = kp.has_maths(src)
                ctx = browser.new_context(viewport={"width": 390, "height": 844})
                ctx.add_init_script("try { localStorage.clear(); } catch (e) {}")
                ctx.route("**/*", route)
                page = ctx.new_page()
                try:
                    page.goto(url_for(rel), wait_until="load")
                    kp.wait_rendered(page, maths)
                    page.wait_for_timeout(150)
                    st = kp.state(page)
                    out[rel] = kp.faults(rel, st, maths)
                    out[rel + "#katex"] = st["katex"]
                except Exception as e:   # a page that cannot be checked is a fault, never a pass
                    out[rel] = ["%s: could not be checked: %s" % (rel, str(e).splitlines()[0])]
                    out[rel + "#katex"] = 0
                ctx.close()
        finally:
            browser.close()
    return out


def selftest():
    """[failure]: two plants on a parent guide (one LaTeX mistake each) must be caught, the guide untouched must pass."""
    base = "parents/fractions/index.html"
    with open(os.path.join(ROOT, base), encoding="utf-8") as fh:
        src = fh.read()
    # Planted as a new paragraph at the end of the guide's <body>, so the rest of the page is as it is.
    para = "<p>Plant: \\(%s\\)</p>\n</body>"
    if src.count("</body>") != 1:
        return ["cannot plant: %s has %d </body>" % (base, src.count("</body>"))]
    plants = {
        "plant/brace-balanced/index.html": (src.replace("</body>", para % "\\dfrac{1}"),
                                            'KaTeX error on "\\dfrac{1}"',
                                            "\\dfrac{1} (balanced, a missing argument): auto-render hands it to KaTeX, a .katex-error"),
        "plant/unclosed/index.html": (src.replace("</body>", para % "\\dfrac{1}{"),
                                      "shows KaTeX source it did not render",
                                      "\\dfrac{1}{ (an unclosed brace): auto-render never finds its end, raw source"),
    }
    found = browse([base] + sorted(plants), {p: t for p, (t, _n, _w) in plants.items()})
    failures = []
    ok_base = not found[base] and found[base + "#katex"] > 0
    print("  %-6s %-34s %s" % ("OK" if ok_base else "FAILED", base + " untouched", found[base] or "no fault"))
    if not ok_base:
        failures.append("the untouched guide did not pass: %s" % found[base])
    for p, (_t, needle, why) in sorted(plants.items()):
        caught = any(needle in f for f in found[p])
        print("  %-6s %-34s %s" % ("caught" if caught else "MISSED", p, why))
        if not caught:
            failures.append("planted %s not caught (got %s)" % (p, found[p]))
    print("self-test: %d of %d plants caught, the untouched page %s"
          % (sum(1 for p in plants if any(plants[p][1] in f for f in found[p])), len(plants),
             "passes" if ok_base else "FAILS"))
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        failures = selftest()
        for f in failures:
            print("SELF-TEST FAIL: " + f)
        return 1 if failures else 0
    rels = pages()
    found = browse(rels)
    faults = [f for rel in rels for f in found[rel]]
    print("KaTeX on load: %d page(s) outside games/ and when-will-i-use-this/ load KaTeX:" % len(rels))
    for rel in rels:
        print("  %-44s %3d .katex  %s" % (rel, found[rel + "#katex"], "FAIL" if found[rel] else "ok"))
    for f in faults:
        print("FAIL: " + f)
    print("FAILED: %d" % len(faults) if faults else "OK")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
