#!/usr/bin/env python3
# ci-line: Checks stay offline (bank_common.offline: with the network dead a page still loads, its KaTeX from scripts/fonts/; no script's route leaves KaTeX to the CDN; the old route planted and caught) |
# ci-deps: scripts/ games/trig-identity-duel/
"""No check waits on a third party (contract ANSWER-LOCK-FLAKE, 15 Nov 2026).

    python scripts/test-offline-routes.py

A page's 'load' waits for every stylesheet and script it names. Until 15 Nov 2026, 30 scripts carried one copied route
that aborted everything off the stub server except KaTeX, and in 18 of them KaTeX then went to cdn.jsdelivr.net on
every page load. One response that never came was a failed check on a game with no fault (main run 43590939932,
"Page.goto: Timeout 20000ms exceeded"). bank_common.offline() / offline_async() is the one route they all call now:
everything off the server aborted, KaTeX answered from the pinned copy in scripts/fonts/.

  static   no script under scripts/ registers a route that exempts KaTeX from the abort (the old line, in any
           spelling: "... and '/katex@' not in url", "... 'cdn.jsdelivr.net/npm/katex' not in url"). A self-test that
           plants the old route says so on that line: "# offline-ok: <reason>"
  pinned   a KaTeX CDN file with a pinned copy is answered from it; one without (another version, a file KaTeX does
           not ship) is aborted, never left for the network
  sync     the page of the game that failed, loaded over a DEAD network (a route registered first, so asked last,
           holds every request the routes above it leave for the network and never answers): with offline() the page
           reaches 'load', KaTeX is defined and its stylesheet applied, Google Fonts and the Firebase SDK are aborted,
           and nothing is left waiting on the network
  async    the same with offline_async()
  plant    the old route over the same dead network: the page must NOT reach 'load', and KaTeX's stylesheet and script
           must be what is waiting. If this passes, the dead network is not dead and the checks above prove nothing.
"""
import asyncio
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

GAME = "/games/trig-identity-duel/?level=gcse"
# A route whose predicate lets a KaTeX URL past the abort: ".route(" and, later on the line, "katex ... not in".
HOLE = re.compile(r"\.route\(.*katex[^\n]*?\bnot in\b")
OLD_LINES = ("ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())",
             'await ctx.route(lambda u: not u.startswith(base) and "/katex@" not in u, lambda r: r.abort())',
             "ctx.route(lambda url: not url.startswith(base) and 'cdn.jsdelivr.net/npm/katex' not in url, lambda route: route.abort())")
STATE_JS = """() => {
  const k = document.createElement('span'); k.className = 'katex';
  const m = document.createElement('span'); m.className = 'katex-mathml'; k.appendChild(m); document.body.appendChild(k);
  const styled = getComputedStyle(m).position === 'absolute';      // KaTeX's stylesheet takes .katex-mathml out of the flow
  k.remove();
  return {katex: typeof katex, styled: styled};
}"""


def static(fails):
    n = 0
    for path in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        if os.path.basename(path) == os.path.basename(__file__):
            continue
        for k, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
            if HOLE.search(line) and not line.lstrip().startswith("#") and "# offline-ok:" not in line:
                fails.append("static: scripts/%s:%d registers a route that leaves KaTeX to the network; call "
                             "bc.offline(ctx, base) (or await bc.offline_async(ctx, base)) instead" % (os.path.basename(path), k))
        n += 1
    missed = [line for line in OLD_LINES if not HOLE.search(line)]
    if missed:
        fails.append("static: the rule does not see the old line: %s" % missed[0])
    return n


def pinned(fails):
    for f in ("katex.min.css", "katex.min.js", "fonts/KaTeX_Main-Regular.woff2"):
        got = bc._offline_answer(bc.KATEX_CDN + f)
        if not got or not os.path.isfile(got["path"]):
            fails.append("pinned: %s is not answered from scripts/fonts/" % f)
    for url in (bc.KATEX_CDN + "no-such-file.js", "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js",
                "https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap",
                "https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"):
        if bc._offline_answer(url) is not None:
            fails.append("pinned: %s is answered, not aborted" % url)


def judge(name, loaded, state, waiting, aborted, fails):
    """One dead-network load with the helper: what must hold."""
    if not loaded:
        fails.append("%s: the page did not reach 'load' over a dead network (waiting on it: %s)"
                     % (name, ", ".join(sorted(set(waiting))) or "nothing"))
        return
    if waiting:
        fails.append("%s: %d request(s) left for the network, e.g. %s" % (name, len(waiting), waiting[0]))
    if state["katex"] != "object":
        fails.append("%s: KaTeX is %s on the page (the pinned script was not served)" % (name, state["katex"]))
    if not state["styled"]:
        fails.append("%s: KaTeX's stylesheet is not applied (.katex-mathml is in the flow)" % name)
    for host in ("fonts.googleapis.com", "www.gstatic.com"):
        if not any(host in u for u in aborted):
            fails.append("%s: the page's request to %s was not aborted" % (name, host))


def old_route(target, base):        # the line 30 scripts carried until 15 Nov 2026
    target.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())


def load_sync(base, routes, timeout):
    """(loaded, state, waiting, aborted) for the game's page over a dead network, with `routes` registered above it."""
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
    waiting, aborted = [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        held = []       # the dead network: each request held, and aborted only when the load is over
        ctx.route(lambda u: not u.startswith(base), lambda r: (waiting.append(r.request.url), held.append(r)))
        routes(ctx, base)
        page = ctx.new_page()
        page.on("requestfailed", lambda r: aborted.append(r.url))
        try:
            page.goto(base + GAME, wait_until="load", timeout=timeout)
            loaded, state = True, page.evaluate(STATE_JS)
        except PwTimeout:
            loaded, state = False, None
        for r in held:
            r.abort()
        browser.close()
    return loaded, state, list(waiting), aborted


async def load_async(base, timeout):
    from playwright.async_api import async_playwright, TimeoutError as PwTimeout
    waiting, aborted = [], []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 390, "height": 844})
        held = []
        await ctx.route(lambda u: not u.startswith(base), lambda r: (waiting.append(r.request.url), held.append(r)))
        await bc.offline_async(ctx, base)
        page = await ctx.new_page()
        page.on("requestfailed", lambda r: aborted.append(r.url))
        try:
            await page.goto(base + GAME, wait_until="load", timeout=timeout)
            loaded, state = True, await page.evaluate(STATE_JS)
        except PwTimeout:
            loaded, state = False, None
        for r in held:
            await r.abort()
        await browser.close()
    return loaded, state, list(waiting), aborted


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fails = []
    n = static(fails)
    pinned(fails)
    proc, base = bc.start_stub_server()
    try:
        s = load_sync(base, bc.offline, 20000)
        judge("sync", *s, fails)
        a = asyncio.run(load_async(base, 20000))
        judge("async", *a, fails)
        p_loaded, _, p_waiting, _ = load_sync(base, old_route, 4000)     # (a short wait: the answer never comes)
    finally:
        proc.terminate()
        proc.wait()
    held = sorted(set(u.rsplit("/", 1)[-1] for u in p_waiting if "/katex@" in u))
    print("static: %d scripts, none registers a route that leaves KaTeX to the network" % n)
    print("dead network, offline(): loaded %s, KaTeX %s, stylesheet applied %s, %d request(s) left waiting; offline_async(): "
          "loaded %s, %d left waiting" % (s[0], s[1] and s[1]["katex"], s[1] and s[1]["styled"], len(s[2]), a[0], len(a[2])))
    caught = (not p_loaded) and "katex.min.css" in held and "katex.min.js" in held
    if not caught:
        fails.append("plant: the old route over a dead network %s, with %s waiting on it: the dead network is not dead"
                     % ("reached 'load'" if p_loaded else "did not load", ", ".join(held) or "nothing"))
    print("  self-test the old route (KaTeX left to the CDN) over a dead network  %s" % (
        "caught: the page never reaches 'load'; waiting on the network: %s" % ", ".join(held) if caught else "*** MISSED ***"))
    for f in fails:
        print("FAIL  " + f)
    print("FAILED" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
