#!/usr/bin/env python3
# ci-line: Game analytics (an escape room won with a search and a tab switch: 3 lock question_answered, 1 game_completed, 0 game_abandoned, to GA4 and the Sheet; a room left mid-game: 1 abandon; an ordinary game with a tab switch: 0 abandons, 1 completion; three old faults planted and caught) |
# ci-deps: schools/assets/analytics.js escape-rooms/assets/engine.js games/prime-or-composite/
"""What one play sends to GA4 and to the Sheet (contract ESCAPE-ANALYTICS, Jon's rulings of 11 Oct 2026).

    python scripts/test-escape-analytics.py

The rules (canon §1.3):
  - an escape room sends question_answered for lock attempts only, numbered 1 to 3; searching the room
    sends nothing (until 11 Oct the first search of each object was a correct answer at index 0);
  - game_abandoned fires only when a started, unfinished game's page is left (pagehide), once; a tab or
    app switch that comes back is not an abandon (until 11 Oct analytics.js sent one on visibilitychange);
  - game_completed reaches each destination once per game.

Scenarios, played in Chromium with the REAL analytics.js (served under https://maffsgames.co.uk by a
Playwright route, as test-section-clicks.py does; nothing leaves the machine):
  room-win    The Rightful King: Start, search every object, a tab switch (hidden, then visible), then
              every lock opened first time. Sheet and GA4 each: exactly 3 question_answered (indices
              1, 2, 3, all correct), 1 game_completed, 0 game_abandoned.
  room-leave  The Rightful King: Start, one lock opened, then the page is left. Sheet: exactly 1
              game_abandoned (the abandon still works).
  game        prime-or-composite, a listed ordinary game with its own visibilitychange abandon handler:
              Start, two answers, a tab switch, then its own endGame(). Sheet and GA4: 0 game_abandoned,
              1 game_completed.

The Sheet is read from the posts to the Apps Script endpoint (beacons included); GA4 from what gtag()
receives (window.dataLayer, which is all gtag.js ever sends; the real gtag.js is not loaded).

Planted faults, each in a copy served by routing (no file is edited), must each be caught:
  search      the engine logging each first search as question_answered at index 0
  hidden      analytics.js sending game_abandoned on visibilitychange (the old listener, no pagehide gate)
  twice       the engine sending game_completed twice
"""
import asyncio
import json
import mimetypes
import os
import re
import sys
from urllib.parse import urlsplit, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGIN = "https://maffsgames.co.uk"
ANALYTICS = "schools/assets/analytics.js"
ENGINE = "escape-rooms/assets/engine.js"
ROOM = "rightful-king"
GAME = "prime-or-composite"

sys.path.insert(0, os.path.join(ROOT, "scripts"))
_spec_src = open(os.path.join(ROOT, "scripts", "check-teacher-invite.py"), encoding="utf-8").read()
ROOM_STEP = re.search(r'ROOM_STEP = r"""(.*?)"""', _spec_src, re.S).group(1)   # the shared room driver

# A tab switch the page can see: document.hidden / visibilityState follow window.__vis.
INIT = """
window.__vis = 'visible';
Object.defineProperty(document, 'visibilityState', {configurable: true, get: function () { return window.__vis; }});
Object.defineProperty(document, 'hidden', {configurable: true, get: function () { return window.__vis === 'hidden'; }});
try { localStorage.clear(); } catch (e) {}
"""
TAB_SWITCH = """async () => {
  window.__vis = 'hidden'; document.dispatchEvent(new Event('visibilitychange'));
  await new Promise(r => setTimeout(r, 400));
  window.__vis = 'visible'; document.dispatchEvent(new Event('visibilitychange'));
  await new Promise(r => setTimeout(r, 200));
}"""
GA4 = "() => (window.dataLayer || []).filter(a => a && a[0] === 'event').map(a => [a[1], a[2] || {}])"


def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def plant_search(engine):
    a = "    st.found[o.id] = true;\n"
    assert engine.count(a) == 1, "plant search: anchor"
    return engine.replace(a, a + "    track('question_answered', { correct: true, question_index: 0, detail: 'searched:' + o.id });\n")


def plant_hidden(analytics):
    a = "if (!window._mfgLeaving || !window._mfgActive"
    assert analytics.count(a) == 1, "plant hidden: gate"
    out = analytics.replace(a, "if (!window._mfgActive")
    b = "  window.addEventListener('beforeunload', function() { window._mfgLeaving = true; });\n"
    assert out.count(b) == 1, "plant hidden: listener"
    return out.replace(b, b + """  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') mfg('game_abandoned', {});
  });
""")


def plant_twice(engine):
    a = "    track('game_completed', {"
    assert engine.count(a) == 1, "plant twice: anchor"
    return engine.replace(a, "    track('game_completed', {});\n" + a)


async def run(served):
    """served: {repo path: replacement text}. -> {scenario: {"sheet": [...], "ga4": [...]} or an error string}"""
    from playwright.async_api import async_playwright
    out = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        async def scenario(name, body):
            posts = []
            ctx = await browser.new_context(viewport={"width": 1280, "height": 900})

            async def route(r):
                url = r.request.url
                if url.startswith(ORIGIN):
                    path = unquote(urlsplit(url).path).lstrip("/")
                    if path.endswith("/") or path == "":
                        path += "index.html"
                    if path in served:
                        await r.fulfill(status=200, body=served[path].encode("utf-8"),
                                        content_type="application/javascript; charset=utf-8")
                        return
                    f = os.path.join(ROOT, path.replace("/", os.sep))
                    if os.path.isfile(f):
                        ctype = mimetypes.guess_type(f)[0] or "application/octet-stream"
                        await r.fulfill(status=200, body=open(f, "rb").read(), content_type=ctype)
                    else:
                        await r.fulfill(status=404, body=b"")
                elif urlsplit(url).netloc == "script.google.com":
                    if r.request.method == "POST":
                        try:
                            posts.append(json.loads(r.request.post_data or "{}"))
                        except ValueError:
                            pass
                    await r.fulfill(status=200, body=b'{"ok":true}', content_type="application/json")
                else:
                    await r.abort()

            await ctx.route("**/*", route)
            await ctx.add_init_script(INIT)
            page = await ctx.new_page()
            try:
                ga4 = await body(page)
                await page.wait_for_timeout(400)
                out[name] = {"sheet": posts, "ga4": ga4}
            except Exception as exc:
                out[name] = "%s: %s" % (name, str(exc).splitlines()[0][:200])
            finally:
                await ctx.close()

        async def room_win(page):
            await page.goto(ORIGIN + "/escape-rooms/%s/" % ROOM, wait_until="load")
            await page.wait_for_selector("#startBtn", state="visible", timeout=15000)
            await page.click("#startBtn")
            await page.wait_for_timeout(300)
            n = await page.evaluate("""() => { const bs = [...document.querySelectorAll('#objects [data-obj]')];
                                              bs.forEach(b => b.click()); return bs.length; }""")
            if not n:
                raise RuntimeError("no room objects to search")
            await page.evaluate(TAB_SWITCH)
            for _ in range(400):
                if await page.evaluate("document.getElementById('scrEnd').classList.contains('active')"):
                    break
                await page.evaluate(ROOM_STEP + "(true)")
                await page.wait_for_timeout(40)
            else:
                raise RuntimeError("the room never reached its end card")
            await page.wait_for_timeout(500)
            return await page.evaluate(GA4)

        async def room_leave(page):
            await page.goto(ORIGIN + "/escape-rooms/%s/" % ROOM, wait_until="load")
            await page.wait_for_selector("#startBtn", state="visible", timeout=15000)
            await page.click("#startBtn")
            await page.wait_for_timeout(300)
            await page.evaluate(ROOM_STEP + "(true)")
            await page.wait_for_timeout(300)
            await page.goto(ORIGIN + "/about/", wait_until="load")
            return None

        async def game(page):
            await page.goto(ORIGIN + "/games/%s/" % GAME, wait_until="load")
            await page.wait_for_timeout(300)
            await page.click("#start-btn")
            for _ in range(2):
                await page.wait_for_function("!document.getElementById('btn-prime').disabled", timeout=10000)
                await page.click("#btn-prime")
                await page.wait_for_timeout(300)
            await page.evaluate(TAB_SWITCH)
            await page.evaluate("endGame()")
            await page.wait_for_timeout(500)
            return await page.evaluate(GA4)

        await scenario("room-win", room_win)
        await scenario("room-leave", room_leave)
        await scenario("game", game)
        await browser.close()
    return out


def judge(res):
    """-> list of faults."""
    faults = []
    for name, r in res.items():
        if isinstance(r, str):
            faults.append(r)
    if any(isinstance(r, str) for r in res.values()):
        return faults

    def names(evs):
        return [e[0] for e in evs]

    win = res["room-win"]
    sheet = [(p.get("event"), p) for p in win["sheet"]]
    ga4 = [(e[0], e[1]) for e in win["ga4"]]
    for dest, evs in (("Sheet", sheet), ("GA4", ga4)):
        qa = [p for n, p in evs if n == "question_answered"]
        idx = sorted(p.get("question_index") for p in qa)
        if idx != [1, 2, 3] or not all(p.get("correct") is True for p in qa):
            faults.append("room-win, %s: question_answered %s (want indices [1, 2, 3], all correct)"
                          % (dest, [(p.get("question_index"), p.get("correct"), p.get("detail")) for p in qa]))
        nc = names(evs).count("game_completed")
        if nc != 1:
            faults.append("room-win, %s: %d game_completed (want 1)" % (dest, nc))
        na = names(evs).count("game_abandoned")
        if na:
            faults.append("room-win, %s: %d game_abandoned after a tab switch that came back (want 0)" % (dest, na))
    leave = [p.get("event") for p in res["room-leave"]["sheet"]]
    if leave.count("game_abandoned") != 1:
        faults.append("room-leave, Sheet: %d game_abandoned when the page was left mid-game (want 1)"
                      % leave.count("game_abandoned"))
    g = res["game"]
    for dest, evs in (("Sheet", [p.get("event") for p in g["sheet"]]), ("GA4", [e[0] for e in g["ga4"]])):
        if evs.count("game_abandoned"):
            faults.append("game (%s), %s: %d game_abandoned after a tab switch that came back (want 0)"
                          % (GAME, dest, evs.count("game_abandoned")))
        if evs.count("game_completed") != 1:
            faults.append("game (%s), %s: %d game_completed (want 1)" % (GAME, dest, evs.count("game_completed")))
    return faults


def summary(res):
    def count(evs, n):
        return sum(1 for e in evs if e == n)
    lines = []
    for name, r in res.items():
        if isinstance(r, str):
            continue
        s = [p.get("event") for p in r["sheet"]]
        g = [e[0] for e in r["ga4"]] if r["ga4"] is not None else None
        lines.append("  %-10s Sheet: %d question_answered, %d game_completed, %d game_abandoned%s" % (
            name, count(s, "question_answered"), count(s, "game_completed"), count(s, "game_abandoned"),
            "" if g is None else "; GA4: %d, %d, %d" % (count(g, "question_answered"), count(g, "game_completed"),
                                                         count(g, "game_abandoned"))))
    return lines


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    res = asyncio.run(run({}))
    faults = judge(res)
    print("Game analytics (ESCAPE-ANALYTICS): %s and %s, real analytics.js" % (ROOM, GAME))
    print("\n".join(summary(res)))
    for f in faults:
        print("  FAIL " + f)
    engine, analytics = read(ENGINE), read(ANALYTICS)
    plants = [("the engine logs each first search as an answer", {ENGINE: plant_search(engine)}, "room-win"),
              ("analytics.js sends game_abandoned on a hidden tab", {ANALYTICS: plant_hidden(analytics)}, "abandoned"),
              ("the engine sends game_completed twice", {ENGINE: plant_twice(engine)}, "game_completed")]
    caught = True
    for what, served, expect in plants:
        got = judge(asyncio.run(run(served)))
        ok = any(expect in g for g in got)
        caught = caught and ok
        print("plant (%s): %s" % (what, "CAUGHT" if ok else "MISSED: " + ("; ".join(got) or "no fault")))
    ok = not faults and caught
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
