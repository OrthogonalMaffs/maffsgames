#!/usr/bin/env python3
# ci-line: Escape-room dial scale (every live room's dials: ticks on their values, labelled majors with min and max, no overlap, drag sets the labelled value, no tick in the dead quarter; every lock's instrument on screen at 390x844; four planted faults caught) |
# ci-deps: escape-rooms/ scripts/check-teacher-invite.py
"""Browser test for the shared escape-room dial (contract DIAL-SCALE, 24 Oct 2026; canon 11.3).

    python scripts/test-escape-dial.py               # every live room, then the four plants
    python scripts/test-escape-dial.py --no-plants   # without the plants

One function in engine.js draws every dial, so this reads the dial each room actually draws, in Chromium, and
holds it to the instrument's own min / max / step / sweep (the angle formula is written out again here, not
read from the engine). For every dial of every live room (a room whose page only redirects is not live):

  ticks     each tick sits on a value of the instrument's grid and at that value's angle (within 0.2 degrees);
            on a 270-degree dial none lies in the dead quarter; there are 8 to 40 of them (unless the range
            has fewer values); a full-circle dial draws its top tick once
  labels    every labelled major carries its value (decimals as the instrument's) at that value's angle; min
            and max are both labelled (a full circle's one top label reads "min/max"); 4 to 11 labels; each is
            at least 11 px as rendered; no two boxes overlap, none touches the pivot or leaves the dial; the
            same at 1280, 390 and 320 px wide
  drag      a pointer press on each labelled major sets exactly that value (a hair inside the scale at either
            end, where the engine's own mapping turns the dead quarter's left half into the maximum)
  phone     at 390x844 picking each lock of each live room leaves its instrument (dial, keypad, slider or pair)
            on screen below the sticky clock with at least 100 px showing; on a fixture lock with art, the art is
            no taller than 30% of the screen at 390x540

  plants    the old 36-tick full-circle scale; a label one step off its tick; labels that overlap; the lock art
            uncapped on a phone: each must FAIL
"""
import argparse
import asyncio
import importlib.util
import math
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
CSS = ROOT / "escape-rooms" / "assets" / "engine.css"
PLANT_ROOMS = ["comic-caper", "big-school-begins", "pe-shed-rebellion", "library-jam"]
FIXTURE_ROOM, ART_KEY = "comic-caper", "comic-caper-scene"
ART_FIXTURE = """(() => {
  let r;
  Object.defineProperty(window, 'ROOM', { configurable: true, get: () => r, set: (v) => {
    v.locks[0].art = '%s'; v.locks[0].artAlt = 'fixture art';
    r = v;
  }});
})()""" % ART_KEY

COUNT = {"dials": 0, "labels": 0, "drags": 0, "locks": 0}

CTL = ".instrument .dial, .instrument .keypad, .instrument input[type=range], .instrument .pair-grid"

DIALS = """() => {
  const out = [];
  document.querySelectorAll('#lockPanel svg.dial').forEach(svg => {
    const b = svg.getBoundingClientRect(), s = b.width / 180, cx = b.left + b.width / 2, cy = b.top + b.height / 2;
    const boss = svg.querySelector('.boss').getBoundingClientRect();
    out.push({
      id: svg.id, size: b.width, scale: s, cx: cx, cy: cy,
      boss: [boss.left, boss.top, boss.right, boss.bottom],
      box: [b.left, b.top, b.right, b.bottom],
      ticks: Array.from(svg.querySelectorAll('line.tick')).map(l => ({
        v: Number(l.dataset.v), major: l.classList.contains('major'),
        x2: Number(l.getAttribute('x2')), y2: Number(l.getAttribute('y2')) })),
      labels: Array.from(svg.querySelectorAll('text.lbl')).map(t => {
        const r = t.getBoundingClientRect();
        return { v: Number(t.dataset.v), text: t.textContent, box: [r.left, r.top, r.right, r.bottom],
                 px: parseFloat(getComputedStyle(t).fontSize) * s };
      })
    });
  });
  return out;
}"""

CTL_TOP = """(sel) => {
  const q = s => document.querySelector(s);
  const hud = q('.hud'), c = q(sel), ins = q('.instrument');
  const r = e => e.getBoundingClientRect();
  return { vh: innerHeight, hud: hud ? r(hud).bottom : 0, top: c ? r(c).top : null, bottom: c ? r(c).bottom : null,
           ins: ins ? r(ins).top : null,
           art: q('#lockPanel .artframe') ? r(q('#lockPanel .artframe')).height : null };
}"""


def angle_of(ins, v):
    """The scale's own rule, written out again: a full circle reads its own angle, the rest sweep 270 degrees."""
    f = (v - ins["min"]) / (ins["max"] - ins["min"])
    return f * 360 if ins.get("sweep") == 360 else -135 + f * 270


def signed(a):
    """An angle in -180..180."""
    a = a % 360
    return a - 360 if a > 180 else a


def dp(v, d):
    return ("%.*f" % (d, v)) if d else str(int(round(v)))


def judge_dial(tag, ins, d, narrow=""):
    """d: one DIALS entry. Returns the failures for this dial at this size."""
    f = []
    COUNT["dials"] += 1
    COUNT["labels"] += len(d["labels"])
    dec = ins.get("decimals") or 0
    n = round((ins["max"] - ins["min"]) / ins["step"])
    full = ins.get("sweep") == 360

    def bad(msg):
        f.append("%s%s: %s" % (tag, narrow, msg))
    # ---- ticks
    seen = []
    for t in d["ticks"]:
        if not isinstance(t["v"], (int, float)) or t["v"] != t["v"]:
            bad("a tick carries no value (data-v)")
            continue
        k = (t["v"] - ins["min"]) / ins["step"]
        if abs(k - round(k)) > 1e-6 or round(k) < 0 or round(k) > n:
            bad("a tick at %s is not a value on the grid (min %s, step %s)" % (t["v"], ins["min"], ins["step"]))
            continue
        want = angle_of(ins, t["v"])
        got = math.degrees(math.atan2(t["x2"] - 90, 90 - t["y2"]))
        if abs(signed(got - want)) > 0.2:
            bad("the tick for %s is drawn at %.1f deg, its value's angle is %.1f" % (t["v"], got, want))
        if not full and abs(got) > 135.3:
            bad("the tick for %s lies at %.1f deg, in the dead quarter (+-135 is the live range)" % (t["v"], got))
        seen.append(round(signed(got), 1))
    if len(set(seen)) != len(seen):
        bad("two ticks share a position (a top tick drawn twice?)")
    distinct = len(set(seen))
    if n + 1 >= 8 and not (8 <= distinct <= 40):
        bad("%d ticks, want 8 to 40" % distinct)
    if not d["ticks"]:
        bad("no ticks")
    # ---- labels
    ls = [l for l in d["labels"] if l["v"] == l["v"]]
    if len(ls) != len(d["labels"]):
        bad("a label carries no value (data-v)")
    vals = [l["v"] for l in ls]
    if not (4 <= len(ls) <= 11) and n + 1 >= 4:
        bad("%d labels, want 4 to 11" % len(ls))
    for must, name in ((ins["min"], "min"), (ins["max"] if not full else ins["min"], "max")):
        if must not in vals:
            bad("%s %s is not labelled" % (name, must))
    if full:
        top = [l for l in ls if l["v"] == ins["min"]]
        if top and top[0]["text"] != dp(ins["min"], dec) + "/" + dp(ins["max"], dec):
            bad("the top label reads %r, want '%s/%s'" % (top[0]["text"], dp(ins["min"], dec), dp(ins["max"], dec)))
    tickvals = [t["v"] for t in d["ticks"]]
    for l in ls:
        num = float(l["text"].split("/")[0])
        if abs(num - l["v"]) > 1e-6 or l["text"].split("/")[0] != dp(l["v"], dec):
            bad("a label reads %r on the tick for %s" % (l["text"], l["v"]))
        if l["v"] not in tickvals:
            bad("label %s has no tick" % l["text"])
        want = angle_of(ins, num)
        cx, cy = (l["box"][0] + l["box"][2]) / 2, (l["box"][1] + l["box"][3]) / 2
        got = math.degrees(math.atan2(cx - d["cx"], d["cy"] - cy))
        if abs(signed(got - want)) > 4.0:
            bad("the label %r sits at %.1f deg, its value's angle is %.1f" % (l["text"], got, want))
        if l["px"] < 11 - 1e-6:
            bad("the label %r is %.1f px, want at least 11" % (l["text"], l["px"]))
        b, o, w = l["box"], d["boss"], d["box"]
        if b[0] < o[2] and b[2] > o[0] and b[1] < o[3] and b[3] > o[1]:
            bad("the label %r touches the pivot" % l["text"])
        if b[0] < w[0] - 0.5 or b[2] > w[2] + 0.5 or b[1] < w[1] - 0.5 or b[3] > w[3] + 0.5:
            bad("the label %r leaves the dial" % l["text"])
    for i in range(len(ls)):
        for j in range(i + 1, len(ls)):
            a, b = ls[i]["box"], ls[j]["box"]
            if a[0] < b[2] - 0.5 and a[2] > b[0] + 0.5 and a[1] < b[3] - 0.5 and a[3] > b[1] + 0.5:
                bad("labels %r and %r overlap" % (ls[i]["text"], ls[j]["text"]))
    return f


async def drive_room(browser, base, slug, engine_js, css, only_dials=False):
    """Returns (failures, {lock id: instrument}) for one room: dial geometry at three widths, and every labelled major dragged."""
    f = []
    ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
        if engine_js is not None:
            await ctx.route(re.compile(r"/escape-rooms/assets/engine\.js(\?.*)?$"), lambda r: r.fulfill(
                status=200, content_type="application/javascript; charset=utf-8", body=engine_js))
        if css is not None:
            await ctx.route(re.compile(r"/escape-rooms/assets/engine\.css(\?.*)?$"), lambda r: r.fulfill(
                status=200, content_type="text/css; charset=utf-8", body=css))
        page = await ctx.new_page()
        await page.goto(base + "/escape-rooms/%s/" % slug, wait_until="load", timeout=20000)
        await page.click("#startBtn")
        locks = await page.evaluate("() => window.ROOM.locks.map(l => ({id: l.id, ins: l.instrument}))")
        for i, lk in enumerate(locks):
            ins = lk["ins"]
            parts = [("", ins)] if ins["kind"] == "dial" else (
                [("A", ins["a"]), ("B", ins["b"])] if ins["kind"] == "pair" and ins["a"]["kind"] == "dial" else [])
            if not parts:
                continue
            await page.click('[data-lock="%d"]' % i)
            await page.wait_for_timeout(120)
            for width in (1280, 390, 320):
                await page.set_viewport_size({"width": width, "height": 900})
                await page.wait_for_timeout(80)
                dials = await page.evaluate(DIALS)
                if len(dials) != len(parts):
                    f.append("%s/%s: %d dials drawn, want %d" % (slug, lk["id"], len(dials), len(parts)))
                    continue
                for (suffix, pins), d in zip(parts, dials):
                    f += judge_dial("%s/%s%s" % (slug, lk["id"], (" " + suffix) if suffix else ""), pins, d,
                                    "" if width == 1280 else " at %d px" % width)
                    if d["size"] < 190 - 1:
                        f.append("%s/%s: the dial renders %.0f px wide at %d px, want 190" % (slug, lk["id"], d["size"], width))
            await page.set_viewport_size({"width": 1280, "height": 900})
            await page.wait_for_timeout(80)
            # drag to every labelled major
            for k, (suffix, pins) in enumerate(parts):
                sid = "ctl" + suffix
                for lab in await page.evaluate(
                        "(id) => Array.from(document.querySelectorAll('#dial_' + id + ' text.lbl')).map(t => Number(t.dataset.v))", sid):
                    d = (await page.evaluate(DIALS))[k]
                    a = angle_of(pins, lab)
                    stepdeg = abs(angle_of(pins, pins["min"] + pins["step"]) - angle_of(pins, pins["min"]))
                    nudge = min(0.3, stepdeg / 4)
                    if pins.get("sweep") == 360 and lab == pins["min"]:
                        a += nudge
                    elif pins.get("sweep") != 360 and lab == pins["min"]:
                        a += nudge
                    elif lab == pins["max"]:
                        a -= nudge
                    r = 60 * d["scale"]
                    x, y = d["cx"] + r * math.sin(math.radians(a)), d["cy"] - r * math.cos(math.radians(a))
                    await page.mouse.click(x, y)
                    COUNT["drags"] += 1
                    got = await page.evaluate("(id) => Number(document.getElementById(id).value)", sid)
                    if abs(got - lab) > 1e-9:
                        f.append("%s/%s%s: a press on the label %s set %s" % (slug, lk["id"], (" " + suffix) if suffix else "", lab, got))
    finally:
        await ctx.close()
    return f


async def phone_room(browser, base, slug, engine_js, css, fixture=False):
    f = []
    h = 540 if fixture else 844
    ctx = await browser.new_context(viewport={"width": 390, "height": h}, has_touch=True, is_mobile=True)
    try:
        await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
        if engine_js is not None:
            await ctx.route(re.compile(r"/escape-rooms/assets/engine\.js(\?.*)?$"), lambda r: r.fulfill(
                status=200, content_type="application/javascript; charset=utf-8", body=engine_js))
        if css is not None:
            await ctx.route(re.compile(r"/escape-rooms/assets/engine\.css(\?.*)?$"), lambda r: r.fulfill(
                status=200, content_type="text/css; charset=utf-8", body=css))
        if fixture:
            await ctx.add_init_script(ART_FIXTURE)
        page = await ctx.new_page()
        await page.goto(base + "/escape-rooms/%s/" % slug, wait_until="load", timeout=20000)
        await page.click("#startBtn")
        ids = await page.evaluate("() => window.ROOM.locks.map(l => l.id)")
        for i, lid in enumerate(ids):
            if fixture and i:
                break
            await page.evaluate("window.scrollTo(0, 0)")
            await page.tap('[data-lock="%d"]' % i)
            await page.wait_for_timeout(150)
            m = await page.evaluate(CTL_TOP, CTL)
            COUNT["locks"] += 1
            if m["top"] is None:
                f.append("%s/%s: no instrument after picking the lock" % (slug, lid))
                continue
            if m["top"] < m["hud"] - 1 or m["top"] > m["vh"] - 100:
                f.append("%s/%s: at 390x%d the instrument's top is at y=%d (clock ends %d, screen %d): not on screen"
                         % (slug, lid, h, m["top"], m["hud"], m["vh"]))
            if fixture:
                if m["art"] is None:
                    f.append("%s/%s: the fixture lock shows no art" % (slug, lid))
                elif m["art"] > 0.3 * m["vh"] + 1:
                    f.append("%s/%s: the lock art is %d px tall on a %d px screen, over 30%%" % (slug, lid, m["art"], m["vh"]))
    finally:
        await ctx.close()
    return f


def live_rooms():
    out = []
    for p in sorted((ROOT / "escape-rooms").glob("*/room.js")):
        idx = p.parent / "index.html"
        if idx.exists() and 'http-equiv="refresh"' not in idx.read_text(encoding="utf-8", errors="replace"):
            out.append(p.parent.name)
    return out


async def run(rooms, engine_js, css, phone=True, art=True):
    from playwright.async_api import async_playwright
    proc, base = ti._serve(ROOT)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(3)

            async def lim(coro):
                async with sem:
                    return await coro
            jobs = [lim(drive_room(browser, base, s, engine_js, css)) for s in rooms]
            if phone:
                jobs += [lim(phone_room(browser, base, s, engine_js, css)) for s in rooms]
            if art:
                jobs.append(lim(phone_room(browser, base, FIXTURE_ROOM, engine_js, css, fixture=True)))
            res = await asyncio.gather(*jobs, return_exceptions=True)
            await browser.close()
    finally:
        proc.terminate()
    f = []
    for r in res:
        if isinstance(r, Exception):
            f.append("could not drive the page: " + str(r).splitlines()[0][:140])
        else:
            f += r
    return f


# ---- the planted faults (each is the engine or its stylesheet with one thing wrong)
OLD_DIALSVG = """  function dialSVG(id, ins) {
    var ticks = '';
    for (var i = 0; i <= 36; i++) {
      var a = (i / 36) * 360 - 90;
      var rad = a * Math.PI / 180;
      var major = i % 3 === 0;
      var r1 = major ? 66 : 71, r2 = 78;
      ticks += '<line class="tick' + (major ? ' major' : '') + '" x1="' + (90 + r1 * Math.cos(rad)).toFixed(1) +
        '" y1="' + (90 + r1 * Math.sin(rad)).toFixed(1) + '" x2="' + (90 + r2 * Math.cos(rad)).toFixed(1) +
        '" y2="' + (90 + r2 * Math.sin(rad)).toFixed(1) + '"/>';
    }
    return '<svg class="dial" id="dial_' + id + '" viewBox="0 0 180 180" aria-hidden="true">' +
      '<circle class="face" cx="90" cy="90" r="84"/>' + ticks +
      '<path id="wedge_' + id + '" fill="rgba(245,165,36,0.18)" stroke="none"></path>' +
      '<line class="needle" id="needle_' + id + '" x1="90" y1="90" x2="90" y2="22"/>' +
      '<circle class="boss" cx="90" cy="90" r="7"/>' +
      '</svg>';
  }
"""


def plant_old_scale(src):
    """The engine before DIAL-SCALE: 36 ticks evenly round the full circle, no numbers."""
    a = src.index("  function dialSVG(id, ins) {")
    b = src.index("  function wireInstrument(l) {")
    return src[:a] + OLD_DIALSVG + "\n" + src[b:]


def plant_off_by_one(src):
    old = "var text = (P.seam && i === 0) ? dp(v, d) + '/' + dp(ins.max, d) : dp(v, d);"
    assert old in src, "plant: the label text line was not found"
    return src.replace(old, old + " text = (P.seam && i === 0) ? text : dp(v + ins.step, d);", 1)


def plant_overlap(src):
    old = "var idx = pick(cands[ci]);"
    assert old in src, "plant: the label candidate line was not found"
    src = src.replace(old, "var idx = pick(t);", 1)
    old2 = "var ok = idx.length <= 11 && idx.length >= 4;"
    assert old2 in src, "plant: the label count line was not found"
    src = src.replace(old2, "var ok = true;", 1)
    old3 = "for (var j = 1; ok && j < idx.length; j++) if (ang(idx[j]) - ang(idx[j - 1]) < 24) ok = false;"
    assert old3 in src, "plant: the label gap line was not found"
    return src.replace(old3, "", 1)


def plant_art_uncapped(css):
    old = "max-height:30vh"
    assert old in css, "plant: the art cap was not found"
    return css.replace(old, "max-height:none", 1)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-plants", action="store_true")
    ap.add_argument("--rooms", nargs="*")
    a = ap.parse_args()
    rooms = a.rooms or live_rooms()
    fails = asyncio.run(run(rooms, None, None))
    print("Escape-room dial scale (DIAL-SCALE): %d live rooms, every dial, every lock on a 390x844 phone" % len(rooms))
    print("  checked: %(dials)d dial drawings (3 widths each), %(labels)d labels, %(drags)d drags, %(locks)d phone locks" % COUNT)
    print("  %s  the scales, the drag and the phone layout%s" % ("FAIL" if fails else "ok  ", (":\n    " + "\n    ".join(fails[:40])) if fails else ""))
    ok = not fails
    if not a.no_plants:
        src = ENGINE.read_text(encoding="utf-8")
        css = CSS.read_text(encoding="utf-8")
        plants = [
            ("the old 36-tick full-circle scale", plant_old_scale(src), None, False),
            ("a label one step off its tick", plant_off_by_one(src), None, False),
            ("labels that overlap", plant_overlap(src), None, False),
            ("the lock art uncapped on a phone", None, plant_art_uncapped(css), True),
        ]
        for name, js, css_, art_only in plants:
            if art_only:
                pf = asyncio.run(run([FIXTURE_ROOM], js, css_, phone=False, art=True))
            else:
                pf = asyncio.run(run(PLANT_ROOMS, js, css_, phone=False, art=False))
            print("plant (%s): %s" % (name, ("CAUGHT: " + "; ".join(pf[:2])) if pf else "MISSED"))
            ok = ok and bool(pf)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
