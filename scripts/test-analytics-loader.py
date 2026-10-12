#!/usr/bin/env python3
# ci-line: GA4 loads on the live host only (analytics.js in Chromium: on the stub server and on a local host no request reaches Google's analytics hosts and no gtag is defined; on the live host one gtag.js load and one page_view with the old config; two faults planted) |
"""GA4-LIVE-ONLY (12 Oct 2026): the tag is loaded by schools/assets/analytics.js, on maffsgames.co.uk only.

    python scripts/test-analytics-loader.py

Played in Chromium with the REAL analytics.js. Every request to a Google analytics host is recorded and aborted, so
nothing leaves the machine; the page is served from the repo by a Playwright route (as test-section-clicks.py does).
  A. The stub server (scripts/serve-stubbed.py): a game page and the front page make no request to Google.
  B. A local host (http://127.0.0.1, the real analytics.js, no stub): game, front page, escape room and /about/ make no
     request to Google, and define neither gtag nor dataLayer, so nothing can send.
  C. The live host (https://maffsgames.co.uk, emulated): each page attempts exactly one gtag.js load and queues exactly
     one config with the old parameters (send_page_view true, storage none, anonymize_ip true), i.e. one page_view.
Planted faults, each of which must fail the run: analytics.js with its hostname gate removed (B must catch it), and
analytics.js with no loader (C must catch it).
"""
import asyncio, mimetypes, os, sys
from urllib.parse import urlsplit, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from bank_common import start_stub_server

ANALYTICS = "schools/assets/analytics.js"
GA_HOSTS = ("googletagmanager.com", "google-analytics.com", "analytics.google.com")
GTAG_URL = "https://www.googletagmanager.com/gtag/js?id=G-992JLHLP2D"
GA_CONFIG = ["G-992JLHLP2D", {"send_page_view": True, "storage": "none", "anonymize_ip": True}]
PAGES = ["/games/prime-or-composite/", "/", "/escape-rooms/rightful-king/", "/about/"]
LOCAL = "http://127.0.0.1:8765"
LIVE = "https://maffsgames.co.uk"
STATE = """() => ({ gtag: typeof window.gtag, dataLayer: typeof window.dataLayer,
  config: (window.dataLayer || []).filter(a => a && a[0] === 'config').map(a => [a[1], a[2] || {}]) })"""


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


async def visit(browser, base, path, served=None, from_files=True):
    """Load `path` on `base`; -> (Google requests attempted, state). from_files: serve the repo by route (else the
    base is a real server, the stub one, and only Google and other hosts are intercepted)."""
    ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
    google = []

    async def route(r):
        url = r.request.url
        host = urlsplit(url).hostname or ""
        if host.endswith(GA_HOSTS):
            google.append(url)
            await r.abort()
        elif url.startswith(base):
            rel = unquote(urlsplit(url).path).lstrip("/")
            if from_files:
                if rel.endswith("/") or rel == "":
                    rel += "index.html"
                if served and rel in served:
                    await r.fulfill(status=200, body=served[rel].encode("utf-8"), content_type="application/javascript; charset=utf-8")
                    return
                f = os.path.join(ROOT, rel.replace("/", os.sep))
                if os.path.isfile(f):
                    await r.fulfill(status=200, body=open(f, "rb").read(), content_type=mimetypes.guess_type(f)[0] or "application/octet-stream")
                else:
                    await r.fulfill(status=404, body=b"")
            else:
                await r.continue_()
        else:
            await r.abort()

    await ctx.route("**/*", route)
    page = await ctx.new_page()
    try:
        await page.goto(base + path, wait_until="load")
        await page.wait_for_timeout(500)
        return google, await page.evaluate(STATE)
    finally:
        await ctx.close()


async def run(served=None):
    """-> {scenario: [faults]}"""
    from playwright.async_api import async_playwright
    out = {"A stub server": [], "B local host": [], "C live host": []}
    proc, stub = start_stub_server()
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for path in PAGES[:2]:
                g, s = await visit(browser, stub, path, from_files=False)
                if g:
                    out["A stub server"].append("%s: %d request(s) to Google: %s" % (path, len(g), g[:2]))
            for path in PAGES:
                g, s = await visit(browser, LOCAL, path, served)
                if g:
                    out["B local host"].append("%s: %d request(s) to Google: %s" % (path, len(g), g[:2]))
                if s["gtag"] != "undefined" or s["dataLayer"] != "undefined":
                    out["B local host"].append("%s: gtag is %s and dataLayer is %s (want both undefined off the live host)"
                                               % (path, s["gtag"], s["dataLayer"]))
                g, s = await visit(browser, LIVE, path, served)
                if g != [GTAG_URL]:
                    out["C live host"].append("%s: gtag.js attempted as %s (want exactly one %s)" % (path, g, GTAG_URL))
                if s["config"] != [GA_CONFIG]:
                    out["C live host"].append("%s: config %s (want one %s, i.e. one page_view)" % (path, s["config"], GA_CONFIG))
            await browser.close()
    finally:
        proc.terminate()
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    res = asyncio.run(run())
    bad = False
    for name, faults in res.items():
        print("  %s  %s  (%s)" % ("FAIL" if faults else "PASS", name, ", ".join(PAGES) if not name.startswith("A") else ", ".join(PAGES[:2])))
        for f in faults:
            print("        " + f)
        bad = bad or bool(faults)
    js = read(ANALYTICS)
    plants = [("analytics.js with its hostname gate removed", js.replace("if (LIVE) {", "if (true) {", 1), "B local host"),
              ("analytics.js with no loader", js.replace("googletagmanager.com/gtag/js", "example.invalid/x", 1), "C live host")]
    for what, text, scenario in plants:
        assert text != js
        got = asyncio.run(run({ANALYTICS: text}))[scenario]
        ok = bool(got)
        bad = bad or not ok
        print("  plant (%s): %s" % (what, "CAUGHT in " + scenario if ok else "MISSED"))
    print("FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
