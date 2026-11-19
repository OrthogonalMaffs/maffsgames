#!/usr/bin/env python3
"""Browser test for the shared Next control, schools/assets/next-control.js (canon §7.6).

    python scripts/test-next-control.py            # the repo's helper
    python scripts/test-next-control.py --helper path/to/next-control.js

Loads the helper into a bare page in headless Chromium and checks what it promises:

  floor        for FLOOR_MS (3s) the control is disabled; Enter, Space and a game's own
               advance() do nothing; after it, Enter advances
  once         one Enter press advances exactly once, even when the game's own keydown
               handler also calls advance() (the batch 1 skip-a-question shape)
  clear        clear() leaves no live timer: neither the floor nor the fallback fires
  fallback     the fallback never fires after a manual advance; on its own it fires
               exactly once, on its own clock, even inside the floor
  size         the control is at least 44px tall and wide
  motion       with prefers-reduced-motion the floor's fill is not drawn
  in view      (NEXT-IN-VIEW) at 320x568, on pages served from games/x/: Next below the fold ends inside
               it with its keep element's top on screen; a page without scroll.js loads it once and does
               the same; Next already in view does not scroll; keep's top holds when both cannot fit; a
               touch during the passes stops them; clear() before scroll.js arrives scrolls nothing
  plants       the in-view cases run again on two planted helpers, each of which must FAIL: the reveal
               call removed, and scroll.js not loaded when the page lacks it

Exits non-zero on any failure. --chromium names a browser binary when Playwright's own
build is not installed (a sandbox).
"""
import argparse
import asyncio
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_HELPER = os.path.join(ROOT, "schools", "assets", "next-control.js")
SCROLL_JS = os.path.join(ROOT, "schools", "assets", "scroll.js")

# NEXT-IN-VIEW: pages served from a routed origin at games/x/, two levels down, so next-control.js finds
# scroll.js beside itself by its own src. %(scroll)s is scroll.js's tag, or nothing for a page without it.
ORIGIN = "http://mfg.test"
VIEW_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;font:16px sans-serif}#top{height:%(top)dpx}#reason{height:%(reason)dpx;background:#fde}
#pad{height:1400px}</style>
%(scroll)s<script src="../../schools/assets/next-control.js"></script></head>
<body><div id="top">question</div><div id="reason">why it was wrong</div><div id="mount"></div><div id="pad"></div>
<script>
  window.reason = document.getElementById('reason');
  window.start = function (opts) {
    window.ctl = MaffsNext.wrong(Object.assign({ mount: document.getElementById('mount'),
      onAdvance: function () {}, keep: window.reason }, opts || {}));
  };
  window.where = function () {
    var b = document.querySelector('.maffs-next');
    return { y: Math.round(window.scrollY), h: window.innerHeight,
             next: b ? Math.round(b.getBoundingClientRect().bottom) : null,
             keep: Math.round(window.reason.getBoundingClientRect().top),
             loads: document.querySelectorAll('script[data-maffs-next]').length };
  };
</script></body></html>"""
SCROLL_TAG = '<script src="../../schools/assets/scroll.js"></script>'

# Plants for the in-view cases: (name, old text, new text). Each planted helper must fail them.
VIEW_PLANTS = [
    ("the reveal call removed", "    reveal(wrap, opts.keep, state);\n", "\n"),
    ("scroll.js not loaded when missing", "    if (scrollWaiting === 'failed') return;\n", "    return;\n"),
]


async def in_view(browser, helper_js, scroll_js, check):
    """The NEXT-IN-VIEW cases at 320x568. `check(name, ok, detail)` records each; returns nothing."""
    async def page_for(top, reason, with_scroll):
        ctx = await browser.new_context(viewport={"width": 320, "height": 568})
        page = await ctx.new_page()
        fetched = {"scroll": 0}
        html = VIEW_PAGE % {"top": top, "reason": reason, "scroll": SCROLL_TAG if with_scroll else ""}

        async def route(r):
            u = r.request.url
            if u.endswith("/schools/assets/next-control.js"):
                return await r.fulfill(body=helper_js, content_type="application/javascript")
            if u.endswith("/schools/assets/scroll.js"):
                fetched["scroll"] += 1
                return await r.fulfill(body=scroll_js, content_type="application/javascript")
            if u.startswith(ORIGIN + "/games/x/"):
                return await r.fulfill(body=html, content_type="text/html")
            return await r.abort()
        await page.route("**/*", route)
        await page.goto(ORIGIN + "/games/x/index.html")
        return ctx, page, fetched

    # Next below the fold, scroll.js on the page: Next ends inside the fold, the reason's top on screen.
    ctx, page, _ = await page_for(480, 120, True)
    before = await page.evaluate("where()")
    await page.evaluate("start()")
    await page.wait_for_timeout(700)
    w = await page.evaluate("where()")
    check("in view: Next below the fold is brought up", before["y"] == 0 and w["next"] is not None and
          0 < w["next"] <= w["h"] and w["keep"] >= 0 and w["y"] > 0,
          "Next %s / %d, reason top %d, scrolled %d" % (w["next"], w["h"], w["keep"], w["y"]))
    await ctx.close()

    # A page without scroll.js: it is fetched once, beside next-control.js, and does the same; a second
    # wrong() does not fetch it again.
    ctx, page, fetched = await page_for(480, 120, False)
    await page.evaluate("start()")
    await page.wait_for_timeout(900)
    w = await page.evaluate("where()")
    await page.evaluate("window.scrollTo(0, 0); start()")
    await page.wait_for_timeout(700)
    w2 = await page.evaluate("where()")
    check("no scroll.js: loaded once, Next brought up", fetched["scroll"] == 1 and w2["loads"] == 1 and
          w["next"] is not None and 0 < w["next"] <= w["h"] and w["keep"] >= 0 and
          0 < w2["next"] <= w2["h"],
          "fetched %d, tags %d, Next %s / %d, reason top %d; again: Next %s" %
          (fetched["scroll"], w2["loads"], w["next"], w["h"], w["keep"], w2["next"]))
    await ctx.close()

    # Next already in view: nothing moves.
    ctx, page, _ = await page_for(100, 100, True)
    await page.evaluate("start()")
    await page.wait_for_timeout(700)
    w = await page.evaluate("where()")
    check("in view: Next already in view, no scroll", w["y"] == 0 and w["next"] <= w["h"],
          "scrolled %d, Next %s / %d" % (w["y"], w["next"], w["h"]))
    await ctx.close()

    # Both cannot fit: the reason's top stays on screen (scroll.js's keep), Next as near as that allows.
    ctx, page, _ = await page_for(400, 700, True)
    await page.evaluate("start()")
    await page.wait_for_timeout(700)
    w = await page.evaluate("where()")
    check("in view: keep's top holds when both cannot fit", w["y"] > 0 and 0 <= w["keep"] <= 16,
          "reason top %d, scrolled %d" % (w["keep"], w["y"]))
    await ctx.close()

    # A touch during the passes stops them: the control's box grows after the first pass (a pass would follow,
    # as the untouched run shows), but after a touchstart nothing moves.
    async def grown(touch):
        ctx, page, _ = await page_for(480, 60, True)
        await page.evaluate("start()")
        await page.wait_for_timeout(300)
        y0 = (await page.evaluate("where()"))["y"]
        if touch:
            await page.evaluate("window.dispatchEvent(new Event('touchstart'))")
        await page.evaluate("document.querySelector('.maffs-next-wrap').style.height = '200px'")
        await page.wait_for_timeout(500)
        y1 = (await page.evaluate("where()"))["y"]
        await ctx.close()
        return y0, y1
    a0, a1 = await grown(False)
    t0, t1 = await grown(True)
    check("a touch stops the pending passes", a0 > 0 and a1 > a0 and t0 > 0 and t1 == t0,
          "untouched %d -> %d; touched %d -> %d" % (a0, a1, t0, t1))

    # clear() before scroll.js arrives: the late reveal finds the control gone and scrolls nothing.
    ctx, page, _ = await page_for(480, 120, False)
    await page.evaluate("start(); MaffsNext.clear(document.getElementById('mount'))")
    await page.wait_for_timeout(700)
    w = await page.evaluate("where()")
    check("clear() before scroll.js arrives: no scroll", w["y"] == 0 and w["next"] is None,
          "scrolled %d" % w["y"])
    await ctx.close()

FIXTURE = """<!doctype html><html><head><meta charset="utf-8"></head>
<body style="font:16px sans-serif"><div id="mount"></div><script>%s</script>
<script>
  window.count = 0;
  window.mount = document.getElementById('mount');
  window.ctl = null;
  window.gameKeys = false;   // a game that also advances on Enter, as formula-plug-in does
  document.addEventListener('keydown', function (e) {
    if (window.gameKeys && e.key === 'Enter' && window.ctl) window.ctl.advance();
  });
  window.start = function (opts) {
    window.count = 0;
    window.ctl = MaffsNext.wrong(Object.assign({ mount: window.mount,
      onAdvance: function () { window.count++; } }, opts || {}));
  };
</script></body></html>"""


async def run(helper_js, chromium):
    from playwright.async_api import async_playwright
    results = []

    def check(name, ok, detail=""):
        results.append((name, ok, detail))
        print("  %s  %-34s %s" % ("PASS" if ok else "FAIL", name, detail))

    async with async_playwright() as p:
        kw = {"executable_path": chromium} if chromium else {}
        browser = await p.chromium.launch(**kw)

        async def fresh(reduced=False):
            ctx = await browser.new_context(viewport={"width": 380, "height": 700},
                                            reduced_motion="reduce" if reduced else "no-preference")
            page = await ctx.new_page()
            await page.set_content(FIXTURE % helper_js)
            return ctx, page

        ctx, page = await fresh()
        floor = await page.evaluate("MaffsNext.FLOOR_MS")
        check("FLOOR_MS is 3000", floor == 3000, "FLOOR_MS=%s" % floor)
        floor = 3000   # Jon's ruling (29 Sep 2026); time against it whatever the helper says

        # floor: nothing advances for 3s, then Enter does
        await page.evaluate("start()")
        st = await page.evaluate("() => ({d: !!(document.querySelector('.maffs-next') || {}).disabled})")
        check("disabled during the floor", st["d"])
        await page.wait_for_timeout(1000)
        await page.keyboard.press("Enter")
        await page.keyboard.press(" ")
        await page.evaluate("ctl.advance()")
        await page.evaluate("() => { const b = document.querySelector('.maffs-next'); if (b) b.click(); }")
        check("floor blocks Enter/Space/advance/click", await page.evaluate("count") == 0,
              "count=%d at 1s" % await page.evaluate("count"))
        await page.wait_for_timeout(floor - 1000 + 250)
        st = await page.evaluate("() => { const b = document.querySelector('.maffs-next'); "
                                 "return {d: b ? b.disabled : null, f: !!b && document.activeElement === b}; }")
        check("enabled and focused after the floor", st["d"] is False and st["f"], str(st))
        await page.keyboard.press("Enter")
        check("Enter advances after the floor", await page.evaluate("count") == 1,
              "count=%d" % await page.evaluate("count"))
        await ctx.close()

        # once: the game's own Enter handler and the focused control on one key press
        ctx, page = await fresh()
        await page.evaluate("gameKeys = true; start()")
        await page.wait_for_timeout(floor + 250)
        await page.keyboard.press("Enter")
        await page.keyboard.press("Enter")
        await page.evaluate("ctl.advance()")
        check("one Enter advances exactly once", await page.evaluate("count") == 1,
              "count=%d after Enter, Enter, advance()" % await page.evaluate("count"))
        await ctx.close()

        # The shape found in phone-fit batch 1, before the in-game guards: the game's own
        # Enter handler advances directly, and loading the next question calls clear().
        # The old clear() left the fallback timer running, so it advanced a second time.
        ctx, page = await fresh()
        await page.evaluate("""() => {
          document.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && window.direct) { window.direct = false; count++; MaffsNext.clear(mount); }
          });
          start({fallbackMs: %d}); window.direct = true;
        }""" % (floor + 800))
        await page.wait_for_timeout(floor + 250)
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(1200)
        check("game's own Enter + clear(): once", await page.evaluate("count") == 1,
              "count=%d after the fallback's time" % await page.evaluate("count"))
        await ctx.close()

        # Space advances, once
        ctx, page = await fresh()
        await page.evaluate("start()")
        await page.wait_for_timeout(floor + 250)
        await page.keyboard.press(" ")
        await page.keyboard.press(" ")
        check("Space advances once", await page.evaluate("count") == 1,
              "count=%d" % await page.evaluate("count"))
        await ctx.close()

        # clear: no live timer afterwards, neither the fallback nor the floor
        ctx, page = await fresh()
        await page.evaluate("start({fallbackMs: 500}); MaffsNext.clear(mount)")
        await page.wait_for_timeout(floor + 500)
        left = await page.evaluate("document.querySelectorAll('.maffs-next').length")
        check("clear() leaves no live timer", await page.evaluate("count") == 0 and left == 0,
              "count=%d, controls left=%d after %dms" % (await page.evaluate("count"), left, floor + 500))
        # a second wrong() on the same mount clears the first one's timers too
        await page.evaluate("start({fallbackMs: 400}); start({fallbackMs: 60000})")
        await page.wait_for_timeout(700)
        check("a new wrong() cancels the old one", await page.evaluate("count") == 0,
              "count=%d" % await page.evaluate("count"))
        await ctx.close()

        # fallback never fires after a manual advance
        ctx, page = await fresh()
        await page.evaluate("start({fallbackMs: %d})" % (floor + 600))
        await page.wait_for_timeout(floor + 200)
        await page.evaluate("() => { const b = document.querySelector('.maffs-next'); if (b) b.click(); }")
        await page.wait_for_timeout(1200)
        check("no fallback after a manual advance", await page.evaluate("count") == 1,
              "count=%d" % await page.evaluate("count"))
        await ctx.close()

        # fallback alone: once, on its own clock, even inside the floor
        ctx, page = await fresh()
        await page.evaluate("start({fallbackMs: 600})")
        await page.wait_for_timeout(900)
        c1 = await page.evaluate("count")
        await page.wait_for_timeout(floor)
        c2 = await page.evaluate("count")
        check("fallback fires once, inside the floor", c1 == 1 and c2 == 1, "count=%d at 0.9s, %d at %.1fs" % (c1, c2, 0.9 + floor / 1000))
        await ctx.close()

        # size
        ctx, page = await fresh()
        await page.evaluate("start()")
        r = await page.evaluate("() => { const b = document.querySelector('.maffs-next').getBoundingClientRect(); return [b.width, b.height]; }")
        check("at least 44px tall and wide", r[0] >= 44 and r[1] >= 44, "%.0f x %.0f" % (r[0], r[1]))
        fill = await page.evaluate("getComputedStyle(document.querySelector('.maffs-next'), '::before').display")
        check("floor fill drawn", fill != "none", "::before display=%s" % fill)
        await ctx.close()

        # reduced motion: dimmed only
        ctx, page = await fresh(reduced=True)
        await page.evaluate("start()")
        fill = await page.evaluate("getComputedStyle(document.querySelector('.maffs-next'), '::before').display")
        check("reduced motion: no fill animation", fill == "none", "::before display=%s" % fill)
        await ctx.close()

        # NEXT-IN-VIEW
        with open(SCROLL_JS, encoding="utf-8") as f:
            scroll_js = f.read()
        await in_view(browser, helper_js, scroll_js, check)

        # Plants: each planted helper must fail at least one in-view case.
        for name, old, new in VIEW_PLANTS:
            if helper_js.count(old) != 1:
                check("plant: " + name, False, "its text is not in the helper once")
                continue
            got = []
            await in_view(browser, helper_js.replace(old, new), scroll_js,
                          lambda n, ok, d="": got.append((n, ok)))
            failed = [n for n, ok in got if not ok]
            check("plant caught: " + name, bool(failed), "fails: " + "; ".join(failed) if failed else "nothing failed")

        await browser.close()
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--helper", default=DEFAULT_HELPER)
    ap.add_argument("--chromium", help="launch this Chromium binary instead of Playwright's own")
    args = ap.parse_args()
    with open(args.helper, encoding="utf-8") as f:
        helper_js = f.read()
    print("next-control.js:", os.path.relpath(args.helper, ROOT) if args.helper.startswith(ROOT) else args.helper)
    results = asyncio.run(run(helper_js, args.chromium))
    bad = [r for r in results if not r[1]]
    print("%d checks, %d failed" % (len(results), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
