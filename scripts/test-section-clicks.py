#!/usr/bin/env python3
"""Portal section clicks: does every labelled element fire exactly one section_clicked?

WHAT IT PROVES
--------------
schools/assets/analytics.js has one delegated listener for portal feature sections
(data-mfg-section / data-mfg-item, added 1 Oct 2026). This test loads the real portal
with the REAL analytics.js -- not serve-stubbed.py's no-op -- and reads what would have
been posted to the Sheet, so it checks the payload as it would land in the columns:

  1. each labelled link fires one section_clicked, action open-link, with the right
     section, item and position, in game_slug / filter_type / filter_value;
  2. each toggle fires one toggle-open when it opens, and nothing when it closes;
  3. no click is held up: the listener never calls preventDefault;
  4. a game card (including one inside the labelled New for 2026/27 section) still
     fires game_card_clicked and never section_clicked;
  5. the Misunderstood Maths card still fires fact_expanded and never section_clicked.

NOTHING LEAVES THE MACHINE
--------------------------
mfg() only sends on maffsgames.co.uk, so the repo is served under that origin by a
Playwright route; the browser never contacts the real site. Every request to the
Apps Script endpoint is answered locally and recorded; every other host is aborted.

    python scripts/test-section-clicks.py
"""
import asyncio, json, mimetypes, os, sys
from urllib.parse import urlsplit, unquote
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = "https://maffsgames.co.uk"

# (section, item, position) in page order: the markup's contract.
EXPECTED_LINKS = [
    ("essentials-link", "open-essentials", 1),
    ("escape-rooms", "summary", 1),
    ("escape-rooms", "hamster-heist", 3),
    ("escape-rooms", "pe-shed-rebellion", 4),
    ("escape-rooms", "heatwave-mutiny", 5),
    ("escape-rooms", "prom-budget", 6),
    ("escape-rooms", "canteen-hack", 7),
    ("escape-rooms", "rugby-mud", 8),
    ("escape-rooms", "comic-caper", 9),
    ("escape-rooms", "kiln-disaster", 10),
    ("escape-rooms", "open-all", 11),
    ("escape-rooms", "start-hamster-heist", 12),
    ("parent-guides", "open-guides", 1),
]
EXPECTED_TOGGLES = [
    ("escape-rooms", "show-all", 2),
    ("new-2026-27", "show-them", 1),
]

# Records whether anything before this point cancelled the click, then stops the
# navigation itself, so one page load serves every click. Bubble phase on window:
# it runs after every listener the page has.
INIT = """
window.__prevented = [];
window.addEventListener('click', function(e) {
  window.__prevented.push(e.defaultPrevented);
  var a = e.target.closest && e.target.closest('a[href]');
  if (a) e.preventDefault();
});
"""


async def main():
    posts = []
    fails = []

    async def route(r):
        url = r.request.url
        if url.startswith(ORIGIN):
            path = unquote(urlsplit(url).path)
            if path.endswith("/"):
                path += "index.html"
            f = os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))
            if os.path.isfile(f):
                ctype = mimetypes.guess_type(f)[0] or "application/octet-stream"
                await r.fulfill(status=200, body=open(f, "rb").read(), content_type=ctype)
            else:
                await r.fulfill(status=404, body=b"")
        elif urlsplit(url).netloc == "script.google.com":
            if r.request.method == "POST":
                posts.append(json.loads(r.request.post_data or "{}"))
            await r.fulfill(status=200, body=b'{"ok":true}', content_type="application/json")
        else:
            await r.abort()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        await ctx.route("**/*", route)
        await ctx.add_init_script(INIT)
        page = await ctx.new_page()
        await page.goto(ORIGIN + "/", wait_until="load")
        await page.wait_for_timeout(500)

        async def click(selector):
            n = len(posts)
            await page.evaluate("s => document.querySelector(s).click()", selector)
            await page.wait_for_timeout(250)
            return posts[n:]

        def check(label, got, want_event, want=None):
            names = [g.get("event") for g in got]
            if names.count(want_event) != 1 or ("section_clicked" in names and want_event != "section_clicked"):
                fails.append("%s: expected one %s, got %s" % (label, want_event, names))
                return
            if want:
                ev = [g for g in got if g["event"] == want_event][0]
                for k, v in want.items():
                    if ev.get(k) != v:
                        fails.append("%s: %s = %r, expected %r" % (label, k, ev.get(k), v))
            print("  ok  %-40s %s" % (label, want_event))

        def fields(sec, item, pos, action):
            return {"section": sec, "item": item, "position": pos, "action": action,
                    "game_slug": item, "filter_type": sec,
                    "filter_value": "v1|pos=%d;action=%s" % (pos, action)}

        print("labelled links")
        for sec, item, pos in EXPECTED_LINKS:
            sel = '[data-mfg-section="%s"] [data-mfg-item="%s"]' % (sec, item)
            check("%s / %s" % (sec, item), await click(sel), "section_clicked",
                  fields(sec, item, pos, "open-link"))

        print("toggles: opening fires, closing does not")
        for sec, item, pos in EXPECTED_TOGGLES:
            sel = '[data-mfg-section="%s"] [data-mfg-item="%s"]' % (sec, item)
            check("%s / %s (open)" % (sec, item), await click(sel), "section_clicked",
                  fields(sec, item, pos, "toggle-open"))
            got = await click(sel)
            if got:
                fails.append("%s / %s (close): expected nothing, got %s" % (sec, item, [g.get("event") for g in got]))
            else:
                print("  ok  %-40s nothing" % ("%s / %s (close)" % (sec, item)))

        print("unchanged events")
        check("game card (in a level section)", await click('.games-grid:not([data-cmp-hide]) a.game-card'),
              "game_card_clicked")
        check("game card (inside new-2026-27)", await click('[data-mfg-section="new-2026-27"] a.game-card'),
              "game_card_clicked", {"section": "New for 2026/27"})
        check("Misunderstood Maths: Read more", await click('#factToggle'), "fact_expanded")

        labelled = await page.evaluate("document.querySelectorAll('[data-mfg-item]').length")
        tested = len(EXPECTED_LINKS) + len(EXPECTED_TOGGLES)
        if labelled != tested:
            fails.append("%d labelled elements on the portal, %d tested" % (labelled, tested))
        if any(await page.evaluate("window.__prevented")):
            fails.append("a click was cancelled before the test's own handler: navigation would be held up")
        await browser.close()

    print()
    if fails:
        print("FAIL")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("OK - %d labelled elements, each one section_clicked; game cards and facts unchanged" % labelled)


if __name__ == "__main__":
    asyncio.run(main())
