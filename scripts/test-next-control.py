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
