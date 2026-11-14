#!/usr/bin/env python3
# ci-line: Start-screen back link (every game page, as loaded at 390x844, shows a visible link back to the games list; planted faults caught: a link only in a hidden header, only on a hidden results screen, invisible, see-through, to another page; four controls pass) | --selftest && --check
# ci-deps: games/ schools/assets/
"""Does every game's start screen show a link back to the games list? (contract BACK-LINK-START, 14 Nov 2026)

    python scripts/check-start-back-link.py --check              # every games/<slug>/index.html, in Chromium
    python scripts/check-start-back-link.py --check --only like-terms-collector
    python scripts/check-start-back-link.py --selftest           # planted faults fail, controls pass (Chromium, no server)

Until 14 Nov 2026 nineteen games kept their only link back inside a game header hidden until Start (or on the results
screen), so a student or teacher who landed on the start screen had no way back but the browser's Back button, and
nothing checked for it. THE RULE: each game page (games/<slug>/index.html, every one, on the roster or not), loaded
at 390x844 in normal mode with nothing pressed, shows at least one visible <a> whose href resolves to the site root
(/ or /index.html) or to /games/. Visible: the link has a size, and neither it nor any ancestor is display:none,
visibility:hidden or opacity 0. It need not be above the fold. A failure lists the slugs and exits 1.

Why its own script and not a second gate in measure-phone-fit.py (which the contract preferred): that script runs
only in .github/workflows/phone-fit-full.yml (nightly, and after a push to main that changes a shared path), never on
a pull request, and it loads the 109 roster games, not all 111 pages. A ci-line here runs in the Gate on every pull
request that changes a game or a shared asset, and on every full run.

The pages are served by serve-stubbed.py behind check-site.py's network guard, with the pinned fonts, so nothing is
sent anywhere.
"""
import argparse
import asyncio
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

ROOT = bc.ROOT
SIZE = (390, 844)
PLANT_ORIGIN = "http://back-link.invalid"

# Every link on the page that leads back to the games list, and whether a student can see it.
PROBE = r"""() => {
  const back = u => /^\/(index\.html)?$/.test(u.pathname) || /^\/games\/?(index\.html)?$/.test(u.pathname);
  const shown = el => {
    const r = el.getBoundingClientRect();
    if (!(r.width > 0 && r.height > 0)) return 'no size';
    for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
      const s = getComputedStyle(e);
      const who = e === el ? 'the link' : (e.id ? '#' + e.id : e.tagName.toLowerCase() + (e.classList[0] ? '.' + e.classList[0] : ''));
      if (s.display === 'none') return who + ' is display:none';
      if (s.visibility === 'hidden' || s.visibility === 'collapse') return who + ' is visibility:hidden';
      if (parseFloat(s.opacity) === 0) return who + ' is opacity 0';
    }
    return '';
  };
  const out = [];
  for (const a of document.querySelectorAll('a[href]')) {
    let u;
    try { u = new URL(a.getAttribute('href'), location.href); } catch (e) { continue; }
    if (u.origin !== location.origin || !back(u)) continue;
    const why = shown(a);
    out.push({ href: a.getAttribute('href'), text: (a.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30),
               visible: !why, why: why, top: Math.round(a.getBoundingClientRect().top + window.scrollY) });
  }
  return out;
}"""


def verdict(links):
    """links: PROBE's rows for one page -> '' when a visible link back is there, or why not."""
    if any(l["visible"] for l in links):
        return ""
    if not links:
        return "no link to the site root or /games/ on the page"
    return "no visible link back; it has %d hidden: %s" % (
        len(links), "; ".join("'%s' (%s)" % (l["text"] or l["href"], l["why"]) for l in links[:3]))


def game_pages():
    g = os.path.join(ROOT, "games")
    return sorted(d for d in os.listdir(g) if os.path.isfile(os.path.join(g, d, "index.html")))


def _check_site():
    spec = importlib.util.spec_from_file_location("check_site", os.path.join(HERE, "check-site.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


async def _one(cs, ctx, base, slug, timeout_ms):
    page = None
    try:
        page, rec = await cs.open_guarded_page(ctx, base, "games/%s/index.html" % slug, timeout_ms, settle_ms=0, fonts="real")
        await asyncio.wait_for(page.evaluate(bc.settle_js()), timeout=timeout_ms / 1000.0)
        links = await asyncio.wait_for(page.evaluate(PROBE), timeout=timeout_ms / 1000.0)
        if rec["escaped"]:
            return slug, "NETWORK GUARD BREACHED: %s" % rec["escaped"][0], links
        return slug, verdict(links), links
    except Exception as exc:
        return slug, "could not be loaded: %s" % (str(exc).splitlines() or ["?"])[0][:160], []
    finally:
        if page is not None:
            try:
                await page.close()
            except Exception:
                pass


def check(slugs, workers=4, timeout_ms=20000):
    """[(slug, '' or why it fails, links)] for each page, loaded once at SIZE."""
    from playwright.async_api import async_playwright
    cs = _check_site()
    proc, base = bc.start_stub_server()

    async def run():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            pool = asyncio.Queue()
            for _ in range(workers):
                pool.put_nowait(await browser.new_context(viewport={"width": SIZE[0], "height": SIZE[1]}))

            async def one(slug):
                ctx = await pool.get()
                try:
                    return await _one(cs, ctx, base, slug, timeout_ms)
                finally:
                    pool.put_nowait(ctx)
            out = await asyncio.gather(*[one(s) for s in slugs])
            await browser.close()
            return out
    try:
        return asyncio.run(run())
    finally:
        proc.terminate()


# ------------------------------------------------------------------------------------------------ self-test
def _plant(body, css=""):
    return ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>plant</title><style>"
            ".back-link{display:inline-block;margin-bottom:12px}.screen{display:none}.screen.active{display:block}"
            "#gameHeader{display:none}%s</style></head><body>%s</body></html>" % (css, body))


LINK = '<a href="../../" class="back-link">← Back to Games</a>'
START = '<div id="startScreen" class="screen active">%s<h1>A game</h1><button>Start</button>%s</div>'
# (name, page, must it fail?)
CASES = [
    ("plant: the only link is in a display:none header",
     _plant('<div id="gameHeader">' + LINK + '</div>' + START % ("", "")), True),
    ("plant: the only link is on a hidden results screen",
     _plant(START % ("", "") + '<div id="resultsScreen" class="screen">' + LINK + '</div>'), True),
    ("plant: the link is visibility:hidden",
     _plant(START % ('<div style="visibility:hidden">' + LINK + '</div>', "")), True),
    ("plant: the link's start screen is opacity 0",
     _plant(START % (LINK, ""), "#startScreen{opacity:0}"), True),
    ("plant: the link has no size",
     _plant(START % ('<a href="../../" class="back-link"></a>', "")), True),
    ("plant: the only visible link goes to another game",
     _plant(START % ('<a href="../another-game/" class="back-link">Another game</a>', "")), True),
    ("plant: no link at all", _plant(START % ("", "")), True),
    ("control: the standard back link, first in the start screen", _plant(START % (LINK, "")), False),
    ("control: a link at the bottom of a visible start screen",
     _plant(START % ("", '<div style="height:1600px"></div><a href="/">All games</a>')), False),
    ("control: a link to /games/", _plant(START % ('<a href="/games/">Games</a>', "")), False),
    ("control: a hidden header link beside a visible start-screen link",
     _plant('<div id="gameHeader">' + LINK + '</div>' + START % (LINK, "")), False),
]


def selftest():
    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": SIZE[0], "height": SIZE[1]})
        for i, (name, html, must_fail) in enumerate(CASES):
            page = ctx.new_page()
            url = "%s/games/plant-%d/index.html" % (PLANT_ORIGIN, i)
            # Served from memory: the plant itself and nothing else, so no server and no network.
            def serve(route, html=html, url=url):
                if route.request.url == url:
                    route.fulfill(status=200, content_type="text/html; charset=utf-8", body=html)
                else:
                    route.abort()
            page.route("**/*", lambda route: serve(route))
            page.goto(url, wait_until="domcontentloaded")
            why = verdict(page.evaluate(PROBE))
            page.close()
            ok = bool(why) == must_fail
            print("  %s  %-62s %s" % ("ok  " if ok else "FAIL", name, why or "passes"))
            if not ok:
                bad.append(name)
        browser.close()
    print("selftest: %s (%d cases)" % ("FAILED: " + "; ".join(bad) if bad else "PASS", len(CASES)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="every game page (the default)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--only", action="append", help="one game slug (repeatable)")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--list", action="store_true", help="print each page's links back, visible or not")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    slugs = game_pages()
    if a.only:
        missing = [s for s in a.only if s not in slugs]
        if missing:
            sys.exit("no game page named %s" % ", ".join(missing))
        slugs = [s for s in slugs if s in a.only]
    results = check(slugs, a.workers)
    failed = [(s, why) for s, why, _ in results if why]
    if a.list:
        for s, why, links in results:
            for l in links:
                print("  %-28s %-7s %-14s %-24s top %-5d %s" % (s, "visible" if l["visible"] else "hidden", l["href"], l["text"], l["top"], l["why"]))
    for s, why in failed:
        print("FAIL  %s: %s" % (s, why))
    if failed:
        print("start-screen back link: FAIL, %d of %d game pages show no link back to the games list at %dx%d: %s"
              % (len(failed), len(results), SIZE[0], SIZE[1], ", ".join(s for s, _ in failed)))
        return 1
    print("start-screen back link: PASS (%d game pages, each shows a link back to the games list at %dx%d)"
          % (len(results), SIZE[0], SIZE[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
