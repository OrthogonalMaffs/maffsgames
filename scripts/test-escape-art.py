#!/usr/bin/env python3
# ci-line: Escape-room art (engine.js: a room with no art field requests no picture, in a fixture room; every live room's scene, win and fail pictures load as before; the old always-request engine planted and caught) |
# ci-deps: escape-rooms/assets/engine.js escape-rooms/ scripts/check-teacher-invite.py
"""Browser test for the escape-room engine's room pictures (contract ART-PENDING, 10 Oct 2026).

    python scripts/test-escape-art.py               # every live room, the fixture, then the plant
    python scripts/test-escape-art.py --no-plants   # without the plant

The rule: a room with no `art` field has no pictures yet, so the engine requests none (no scene, fail or win
frame), exactly as a lock with no `art` has no instrument picture (canon §11.3). A room that names its art
behaves as before, data-fallback included.

  live     every live room (one that loads the engine), played in Chromium to a win and to a loss with
           check-teacher-invite.py's ROOM_STEP: the brief shows <art>-scene.webp, the win card <art>-win.webp
           (or -scene without a winAlt), the loss card <art>-fail.webp; each loads (naturalWidth > 0). In a room
           with a missArt lock, that lock's named misconception is entered first: its feedback shows the
           <art>-fail.webp thumbnail
  fixture  the first live room with its top-level `art:` line removed, served by routing (no room file is
           edited): no request to /docs/art/ from the brief, the misconception, the win or the loss; no picture
           or frame on the brief, in the misconception's feedback or on either end card; no response on the page is a 404 (check-site tier 1's rule)
  plant    the fixture against an engine that always has art (HAS_ART forced true, the engine before
           ART-PENDING): it must request the missing pictures, so the fixture check must FAIL
"""
import argparse
import asyncio
import importlib.util
import os
import pathlib
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = pathlib.Path(HERE).parent
_spec = importlib.util.spec_from_file_location("teacher_invite", os.path.join(HERE, "check-teacher-invite.py"))
ti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ti)

ENGINE = ROOT / "escape-rooms" / "assets" / "engine.js"
ROOM_ART = re.compile(r"^  art:\s*'([^']+)',?\r?\n", re.M)
FRAMES = "() => [...document.querySelectorAll('.artframe, .failthumb')].filter(f => f.offsetParent !== null).length"
# The first lock with missArt gets its named misconception (the failure thumbnail's one trigger); returns whether
# a lock was tried. Variant lookup as check-teacher-invite.py's ROOM_STEP.
MISS_STEP = r"""(() => {
  const R = window.ROOM;
  let vars = {};
  try { vars = (JSON.parse(localStorage.getItem('mfg_escape_vars_' + R.slug)) || {}).vars || {}; } catch (e) {}
  const i = R.locks.findIndex(l => l.missArt);
  if (i < 0) return false;
  const l = R.locks[i], v = l.variants ? (l.variants[vars[l.id] || 0] || l.variants[0]) : {};
  const m = v.miss !== undefined ? v.miss : l.miss, ins = l.instrument;
  document.querySelector('[data-lock="' + i + '"]').click();
  const put = (id, val) => { const n = document.getElementById(id); n.value = String(val); n.dispatchEvent(new Event('input', {bubbles: true})); };
  if (ins.kind === 'keypad') put('numK', String(m).padStart(ins.digits, '0'));
  else if (ins.kind === 'pair') { put('numA', m[0]); put('numB', m[1]); }
  else put('num', m);
  document.getElementById('setBtn').click();
  return true;
})()"""
IMGS = """(sel) => [...document.querySelectorAll(sel + ' img')].map(i => ({src: i.getAttribute('src'),
           ok: i.complete && i.naturalWidth > 0}))"""


def no_art(js):
    out, n = ROOM_ART.subn("", js, count=1)
    assert n == 1, "fixture: the room's top-level art line was not found"
    return out


def plant(src):
    """The engine before ART-PENDING: every room is treated as having art."""
    out = src.replace("var HAS_ART = !!R.art;", "var HAS_ART = true;")
    assert out != src, "plant: the HAS_ART line was not found"
    return out


async def play(browser, base, room, win, room_js=None, engine_js=None):
    """Load the room, check the brief, play to the end card; returns (faults-relevant facts)."""
    ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
        if room_js is not None:
            await ctx.route(re.compile(r"/escape-rooms/%s/room\.js(\?.*)?$" % re.escape(room)), lambda r: r.fulfill(
                status=200, content_type="application/javascript; charset=utf-8", body=room_js))
        if engine_js is not None:
            await ctx.route(re.compile(r"/escape-rooms/assets/engine\.js(\?.*)?$"), lambda r: r.fulfill(
                status=200, content_type="application/javascript; charset=utf-8", body=engine_js))
        page = await ctx.new_page()
        art_reqs, not_found = [], []
        page.on("request", lambda q: art_reqs.append(q.url.split("/docs/art/")[1]) if "/docs/art/" in q.url else None)
        page.on("response", lambda r: not_found.append(r.url) if r.status == 404 else None)
        await page.goto(base + "/escape-rooms/%s/" % room, wait_until="load", timeout=20000)
        await page.wait_for_timeout(300)
        brief = {"imgs": await page.evaluate(IMGS, "#scrBrief"), "frames": await page.evaluate(FRAMES)}
        await page.click("#startBtn")
        miss = None
        if await page.evaluate(MISS_STEP):
            await page.wait_for_timeout(600)
            miss = {"near": await page.evaluate("() => !!document.querySelector('#fb.near')"),
                    "imgs": await page.evaluate(IMGS, "#fb")}
        for _ in range(400):
            if await page.evaluate("document.getElementById('scrEnd').classList.contains('active')"):
                break
            await page.evaluate(ti.ROOM_STEP + "(%s)" % ("true" if win else "false"))
            await page.wait_for_timeout(40)
        else:
            return None
        await page.wait_for_timeout(600)
        end = {"imgs": await page.evaluate(IMGS, "#endCard"), "frames": await page.evaluate(FRAMES)}
        return {"brief": brief, "miss": miss, "end": end, "art_reqs": art_reqs, "not_found": not_found}
    finally:
        await ctx.close()


def judge_live(room, art, win_alt, win, got):
    where = "%s (%s)" % (room, "win" if win else "loss")
    if got is None:
        return ["%s: the room never reached its end card" % where]
    faults = []
    want_end = "%s-%s.webp" % (art, ("win" if win_alt else "scene") if win else "fail")
    for name, imgs, want in (("brief", got["brief"]["imgs"], "%s-scene.webp" % art), ("end card", got["end"]["imgs"], want_end)):
        hits = [i for i in imgs if (i["src"] or "").endswith("/docs/art/" + want)]
        if not hits:
            faults.append("%s: the %s shows no %s (has %s)" % (where, name, want, [i["src"] for i in imgs] or "no picture"))
        elif not all(i["ok"] for i in hits):
            faults.append("%s: %s did not load on the %s" % (where, want, name))
    if got["miss"] is not None:
        thumb = [i for i in got["miss"]["imgs"] if (i["src"] or "").endswith("/docs/art/%s-fail.webp" % art)]
        if not got["miss"]["near"]:
            faults.append("%s: the misconception did not raise its feedback" % where)
        elif not thumb or not all(i["ok"] for i in thumb):
            faults.append("%s: the misconception's failure thumbnail is missing or did not load" % where)
    if got["not_found"]:
        faults.append("%s: 404 for %s" % (where, ", ".join(got["not_found"][:3])))
    return faults


def judge_fixture(room, win, got):
    where = "fixture %s, art removed (%s)" % (room, "win" if win else "loss")
    if got is None:
        return ["%s: the room never reached its end card" % where]
    faults = []
    if got["art_reqs"]:
        faults.append("%s: requested /docs/art/%s" % (where, ", ".join(sorted(set(got["art_reqs"])))))
    if got["miss"] is not None:
        if not got["miss"]["near"]:
            faults.append("%s: the misconception did not raise its feedback" % where)
        elif got["miss"]["imgs"]:
            faults.append("%s: the misconception's feedback has %d picture(s), want none" % (where, len(got["miss"]["imgs"])))
    for name in ("brief", "end"):
        if got[name]["imgs"] or got[name]["frames"]:
            faults.append("%s: the %s has %d picture(s) and %d frame(s), want none" % (
                where, "brief" if name == "brief" else "end card", len(got[name]["imgs"]), got[name]["frames"]))
    if got["not_found"]:
        faults.append("%s: 404 for %s" % (where, ", ".join(got["not_found"][:3])))
    return faults


async def run(rooms, fixture_room, engine_js):
    from playwright.async_api import async_playwright
    proc, base = ti._serve(ROOT)
    out = {}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(4)

            async def live(room, win):
                js = (ROOT / "escape-rooms" / room / "room.js").read_text(encoding="utf-8")
                art = ROOM_ART.search(js).group(1)
                win_alt = bool(re.search(r"^  winAlt:", js, re.M))
                async with sem:
                    try:
                        got = await play(browser, base, room, win, engine_js=engine_js)
                    except Exception as e:
                        got, err = None, str(e).splitlines()[0][:120]
                        out[("live", room, win)] = ["%s: could not drive the page: %s" % (room, err)]
                        return
                out[("live", room, win)] = judge_live(room, art, win_alt, win, got)

            async def fixture(win):
                js = no_art((ROOT / "escape-rooms" / fixture_room / "room.js").read_text(encoding="utf-8"))
                async with sem:
                    try:
                        got = await play(browser, base, fixture_room, win, room_js=js, engine_js=engine_js)
                    except Exception as e:
                        out[("fixture", fixture_room, win)] = ["fixture: could not drive the page: %s" % str(e).splitlines()[0][:120]]
                        return
                out[("fixture", fixture_room, win)] = judge_fixture(fixture_room, win, got)

            jobs = [live(r, w) for r in rooms for w in (True, False)] + [fixture(w) for w in (True, False)]
            await asyncio.gather(*jobs)
            await browser.close()
    finally:
        proc.terminate()
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-plants", action="store_true")
    a = ap.parse_args()
    rooms = [r for r in ti.live_rooms(ROOT)
             if ROOM_ART.search((ROOT / "escape-rooms" / r / "room.js").read_text(encoding="utf-8"))]
    fixture_room = rooms[0]
    res = asyncio.run(run(rooms, fixture_room, None))
    print("Escape-room art (ART-PENDING): %d live room(s) with art, each to a win and a loss; fixture: %s, art removed"
          % (len(rooms), fixture_room))
    for key in sorted(res, key=lambda k: (k[0] != "fixture", k[1], not k[2])):
        kind, room, win = key
        print("  %s  %s %s (%s)%s" % ("FAIL" if res[key] else "ok  ", kind, room, "win" if win else "loss",
                                     (": " + "; ".join(res[key])) if res[key] else ""))
    ok = not any(res.values())
    if not a.no_plants:
        pres = asyncio.run(run([], fixture_room, plant(ENGINE.read_text(encoding="utf-8"))))
        caught = all(any("requested /docs/art/" in f for f in pres[k]) for k in pres)
        print("plant (engine always requests the room's pictures), fixture to a win and a loss: %s"
              % ("CAUGHT" if caught else "MISSED: " + "; ".join(f for v in pres.values() for f in v) or "no fault"))
        ok = ok and caught
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
