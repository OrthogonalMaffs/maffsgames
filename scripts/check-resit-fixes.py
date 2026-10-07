#!/usr/bin/env python3
# ci-line: B4 | Resit fixes of 4 Oct 2026 (five games' fixed faults, each fails on the old code) |
"""Regression checks for the resit-safety fixes of 4 Oct 2026 (resit correctness audit, PR #35).

    python scripts/check-resit-fixes.py                    # CI
    python scripts/check-resit-fixes.py --root <dir>       # another copy (e.g. the pre-fix commit)
    python scripts/check-resit-fixes.py --no-selftest

Five resit games had live faults and no verifier. Each fix gets a check here that fails on the old
file and passes on the new; the self-test proves it in CI by serving each game with its fix reverted
(the old code, planted as a patch; the file is never touched) and requiring that check to fail.
Full per-game verifiers follow in the audit's fix batches (docs/audit-resit-correctness-2026-10-04.md).

  shape-shifter        every rotation key matches its words, recomputed here on the y-up grid
                       (clockwise (x,y)->(y,-x), anticlockwise (-y,x), 180 (-x,-y)); four distinct
                       options, none the object; the letters at least 0.8 units apart; tapping each
                       option's letter selects that option,
                       for every question in several letter orders (real clicks in Chromium)
  probability-pioneer  "P(letter in MATHS also in GAMES)" keyed 3/5, recomputed from the words
  (estimation-engine's check, sqrt(e x 1000) = 52.137, retired 5 Oct 2026: the whole pool was replaced in its
  SR-12 rebuild, and scripts/verify-estimation-engine.py recomputes every key of the new bank)
  decimal-detective    Place It: the marker never starts on the answer; the reading equal to the
                       value is marked right, the neighbouring ticks and half-way points wrong (since
                       5 Oct 2026 the marker snaps and is marked exactly by MaffsNumberLine; the planted
                       fault is a one-step tolerance)
  negative-number-line Place It: the target is marked right, the snapped half-steps either side wrong
  correlation-or-coincidence  the "suicides by hanging" pair is gone (Jon: safeguarding, 4 Oct 2026)
"""
import argparse, asyncio, json, math, mimetypes, pathlib, re, sys
from fractions import Fraction

import bank_common as bc

BASE = pathlib.Path(__file__).resolve().parent.parent
HOST = "http://resit-fixes.test/"

# The fixes reversed: (game, what the old file had, what the new one has). Each pair restores the
# pre-fix code, so the check for that game must FAIL on the patched page.
REVERT = {
    "shape-shifter": [
        ("games/shape-shifter/index.html",
         "const dirLabel = angle === 90 ? '90\\u00b0 anticlockwise' : angle === -90 ? '90\\u00b0 clockwise' : '180\\u00b0';",
         "const dirLabel = angle === 90 ? '90\\u00b0 clockwise' : angle === -90 ? '90\\u00b0 anticlockwise' : '180\\u00b0';")],
    "shape-shifter tap": [
        ("games/shape-shifter/index.html",
         "    const i = optionAt(...pixelToGridExact(px, py));\n    if (i >= 0) selectRotationOption(i);",
         "    const [sx, sy] = [Math.round(pixelToGridExact(px, py)[0]), Math.round(pixelToGridExact(px, py)[1])];\n"
         "    for (let i = 0; i < rotationOptions.length; i++) {\n"
         "      const sh = rotationOptions[i].shape;\n"
         "      if (insideShape(sx, sy, sh) || sh.some(([vx, vy]) => Math.abs(vx - sx) <= 1 && Math.abs(vy - sy) <= 1)) { selectRotationOption(i); return; }\n"
         "    }")],
    "shape-shifter letters stacked": [
        ("games/shape-shifter/index.html", "    o.at = best;", "    o.at = [cx, cy];")],
    "shape-shifter duplicate options": [
        ("games/shape-shifter/index.html",
         "  const key = sh => sh.map(([x, y]) => x + ',' + y).sort().join(' ');\n  return key(a) === key(b);",
         "  for (let i = 0; i < a.length; i++) {\n    if (a[i][0] !== b[i][0] || a[i][1] !== b[i][1]) return false;\n  }\n  return true;"),
        ("games/shape-shifter/index.html",
         "      const validWrongs = wrongs.filter((w, k) => shapeFits(w) && !shapesEqual(w, correct) &&\n"
         "        !shapesEqual(w, b.shape) && !wrongs.slice(0, k).some(v => shapesEqual(v, w)));",
         "      const validWrongs = wrongs.filter(w => shapeFits(w) && !shapesEqual(w, correct));")],
    "probability-pioneer": [
        ("games/probability-pioneer/index.html",
         '{q:"P(letter in MATHS also in GAMES)", answer:"3/5",', '{q:"P(letter in MATHS also in GAMES)", answer:"2/5",')],
    "decimal-detective start": [
        ("games/decimal-detective/index.html",
         "until 5 Oct 2026.\n  markerPos = null;", "until 5 Oct 2026.\n  markerPos = 0.5;")],
    "decimal-detective tolerance": [
        ("games/decimal-detective/index.html",
         "const isCorrect = MaffsNumberLine.placementCorrect({ placed: placed, target: data.value, mode: 'snapped' });",
         "const isCorrect = Math.abs(placed - data.value) <= (data.max - data.min) / 20 + 1e-9;")],
    "negative-number-line": [
        ("games/negative-number-line/index.html",
         "const correct = MaffsNumberLine.placementCorrect({ placed: placedValue, target: target, mode: 'snapped' });",
         "const correct = Math.abs(placedValue - target) <= 0.5;")],
    "correlation-or-coincidence": [
        ("games/correlation-or-coincidence/index.html", "{id:'C1', cat:'chance',",
         "{id:'C0', cat:'chance', x:['US spending on science (billions $)'], y:['Suicides by hanging per year']},\n"
         "{id:'C1', cat:'chance',")],
}

BANNED = re.compile(r"suicid|hanging", re.I)


def read(root, rel, patches):
    text = (root / rel).read_text(encoding="utf-8")
    for path, new, old in patches:
        if path == rel:
            assert text.count(new) == 1, "self-test patch out of date for %s: %r" % (rel, new[:60])
            text = text.replace(new, old)
    return text


# ---------- static checks ----------
def check_probability(root, patches):
    src = read(root, "games/probability-pioneer/index.html", patches)
    m = re.search(r'\{q:"P\(letter in (\w+) also in (\w+)\)", answer:"(\d+)/(\d+)", options:\[([^\]]*)\][^}]*\}', src)
    if not m:
        return ["probability-pioneer: the MATHS/GAMES question is missing"]
    a, b = m.group(1), m.group(2)
    want = Fraction(sum(1 for ch in a if ch in b), len(a))
    got = Fraction(int(m.group(3)), int(m.group(4)))
    opts = re.findall(r'"([^"]+)"', m.group(5))
    errs = []
    if got != want:
        errs.append("probability-pioneer: P(letter in %s also in %s) keyed %s, the answer is %s" % (a, b, got, want))
    if sum(1 for o in opts if Fraction(o) == want) != 1:
        errs.append("probability-pioneer: the answer %s is not among the options exactly once: %s" % (want, opts))
    return errs



def check_correlation(root, patches):
    src = read(root, "games/correlation-or-coincidence/index.html", patches)
    hits = sorted(set(m.group(0).lower() for m in BANNED.finditer(src)))
    return ["correlation-or-coincidence: the removed pair is back (%s)" % ", ".join(hits)] if hits else []


# ---------- browser checks ----------
async def open_game(browser, root, slug, patches, viewport=(1000, 900)):
    ctx = await browser.new_context(viewport={"width": viewport[0], "height": viewport[1]})
    await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)   # MaffsLock's 300 ms window: the checks answer at once

    async def route(r):
        url = r.request.url
        if not url.startswith(HOST):
            return await r.abort()
        rel = url[len(HOST):].split("?")[0].split("#")[0]
        if rel == "" or rel.endswith("/"):
            rel += "index.html"
        f = root / rel
        if not f.is_file():
            return await r.fulfill(status=404, body="")
        ctype = mimetypes.guess_type(str(f))[0] or "application/octet-stream"
        if ctype.startswith("text/") or rel.endswith(".js"):
            await r.fulfill(status=200, content_type=ctype, body=read(root, rel, patches))
        else:
            await r.fulfill(status=200, content_type=ctype, body=f.read_bytes())
    await ctx.route("**/*", route)
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.goto(HOST + "games/%s/" % slug, wait_until="load")
    await page.evaluate("() => { window.mfg = function () {}; }")
    return ctx, page, errors


def rotate(shape, desc):
    if "anticlockwise" in desc:
        f = lambda x, y: (-y, x)
    elif "clockwise" in desc:
        f = lambda x, y: (y, -x)
    elif "180" in desc:
        f = lambda x, y: (-x, -y)
    else:
        return None
    return sorted(f(x, y) for x, y in shape)


def as_set(shape):
    return sorted((x, y) for x, y in shape)


async def check_shape_shifter(browser, root, patches, orders=6):
    ctx, page, perr = await open_game(browser, root, "shape-shifter", patches)
    errs = []
    n = await page.evaluate("ROTATION_QUESTIONS.length")
    await page.evaluate("startGame('rotation')")
    for k in range(n):
        q = await page.evaluate("(k) => { questions = [ROTATION_QUESTIONS[k]]; qIndex = 0; loadQuestion(); "
                                "return {desc: currentQ.desc, shape: currentQ.shape, correct: currentQ.correct, "
                                "cx: currentQ.cx, cy: currentQ.cy, wrongs: currentQ.wrongs}; }", k)
        where = "shape-shifter rotation %d (%s, object %s)" % (k + 1, q["desc"], q["shape"])
        if (q["cx"], q["cy"]) != (0, 0) or "about (0,0)" not in q["desc"]:
            errs.append("%s: this check recomputes rotations about (0,0) only" % where)
            continue
        want = rotate(q["shape"], q["desc"])
        if want is None:
            errs.append("%s: no direction in the words" % where)
        elif as_set(q["correct"]) != want:
            errs.append("%s: keyed %s, the image is %s" % (where, as_set(q["correct"]), want))
        sets = [tuple(as_set(s)) for s in [q["correct"]] + q["wrongs"]]
        if len(sets) != 4 or len(set(sets)) != 4:
            errs.append("%s: the four options are not four different shapes" % where)
        if tuple(as_set(q["shape"])) in sets:
            errs.append("%s: an option is the object itself" % where)
        # Tap each option's letter (drawn at its centroid), in several letter orders.
        for _ in range(orders):
            got = await page.evaluate("""async () => {
              buildRotationOptions(); drawGrid();
              const r = canvas.getBoundingClientRect(), out = [];
              for (let i = 0; i < rotationOptions.length; i++) {
                const o = rotationOptions[i], [cx, cy] = o.at || shapeCentroid(o.shape), [px, py] = gridToPixel(cx, cy);
                out.push([r.left + px, r.top + py, cx, cy]);
              }
              return out; }""")
            pts = [(a, b) for _, _, a, b in got]
            close = min(math.hypot(p[0] - q2[0], p[1] - q2[1]) for i, p in enumerate(pts) for q2 in pts[i + 1:])
            if close < 0.8:
                errs.append("%s: two option letters are drawn %.2f grid units apart (one over the other)" % (where, close))
                break
            for i, (x, y, _, _) in enumerate(got):
                await page.evaluate("() => { MaffsLock.fresh(gameEl); selectedOption = -1; }")
                await page.mouse.click(x, y)
                sel = await page.evaluate("selectedOption")
                if sel != i:
                    lab = await page.evaluate("(i) => rotationOptions.map(o => o.label)", i)
                    errs.append("%s: tapping letter %s selected %s" % (where, lab[i], lab[sel] if sel >= 0 else "nothing"))
                    break
            else:
                continue
            break
    errs += ["shape-shifter: page error %s" % e for e in perr]
    await ctx.close()
    return errs


async def check_decimal_detective(browser, root, patches):
    ctx, page, perr = await open_game(browser, root, "decimal-detective", patches)
    errs = []
    items = await page.evaluate("PLACEIT_QUESTIONS")

    async def mark(data, reading=None):
        """Load the question; optionally move the marker to a reading; press Check. -> (start, correct)"""
        return await page.evaluate("""([data, reading]) => {
          questions = [{type: 'placeit', data: data}]; currentQ = 0; loadQuestion();
          const start = document.getElementById('markerValue').textContent;
          if (reading !== null) setMarkerPosition((reading - data.min) / (data.max - data.min));
          checkAnswer();
          return [start, document.getElementById('lineMarker').classList.contains('correct')]; }""", [data, reading])

    await page.evaluate("startGame()")
    for d in items:
        v, lo, hi = Fraction(str(d["value"])), Fraction(str(d["min"])), Fraction(str(d["max"]))
        tick = (hi - lo) / 10
        where = "decimal-detective Place It %s on %s to %s" % (d["value"], d["min"], d["max"])
        start, ok = await mark(d)
        if start and Fraction(start) == v:
            errs.append("%s: the marker starts on the answer (reads %s)" % (where, start))
        if ok:
            errs.append("%s: Check with the marker untouched is marked right" % where)
        _, ok = await mark(d, float(v))
        if not ok:
            errs.append("%s: the marker on the value is marked wrong" % where)
        for off, name in ((tick, "one tick gap"), (tick / 2, "half a tick gap")):
            for w in (v - off, v + off):
                if lo <= w <= hi and (w * 100).denominator == 1:
                    _, ok = await mark(d, float(w))
                    if ok:
                        errs.append("%s: %s, %s away, is marked right" % (where, float(w), name))
    errs += ["decimal-detective: page error %s" % e for e in perr]
    await ctx.close()
    return errs


async def check_negative_number_line(browser, root, patches):
    ctx, page, perr = await open_game(browser, root, "negative-number-line", patches)
    errs = []
    targets = await page.evaluate("PLACE_QUESTIONS")
    await page.evaluate("startGame()")

    async def place(t, v):
        await page.evaluate("(t) => { questions = [{type: 'place', data: t}]; qIndex = 0; showQuestion(); }", t)
        x, y = await page.evaluate("""(v) => { const s = document.getElementById('placeNL').getBoundingClientRect();
          return [s.left + valueToX(v) / 680 * s.width, s.top + s.height / 2]; }""", v)
        await page.mouse.click(x, y)
        shown = await page.evaluate("placedValue")
        await page.evaluate("confirmPlace()")
        return shown, await page.evaluate("document.getElementById('feedbackBar').textContent.trim() === 'Correct!'")

    for t in targets:
        where = "negative-number-line Place It %s" % t
        shown, ok = await place(t, t)
        if shown != t or not ok:
            errs.append("%s: placing it on %s (marker reads %s) is not marked right" % (where, t, shown))
        for w in (t - 0.5, t + 0.5):
            if -10 <= w <= 10:
                shown, ok = await place(t, w)
                if shown == w and ok:
                    errs.append("%s: the marker on %s is marked right" % (where, w))
    errs += ["negative-number-line: page error %s" % e for e in perr]
    await ctx.close()
    return errs


async def run_checks(browser, root, which=None, patches=()):
    """{check name: [errors]}; which limits to some checks (the self-test)."""
    static = {"probability-pioneer": check_probability, "correlation-or-coincidence": check_correlation}
    live = {"shape-shifter": check_shape_shifter, "decimal-detective": check_decimal_detective,
            "negative-number-line": check_negative_number_line}
    out = {}
    for name, fn in static.items():
        if which is None or name in which:
            out[name] = fn(root, patches)
    for name, fn in live.items():
        if which is None or name in which:
            out[name] = await fn(browser, root, patches)
    return out


async def main_async(args):
    from playwright.async_api import async_playwright
    root = pathlib.Path(args.root)
    failed = False
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        results = await run_checks(browser, root)
        for name, errs in results.items():
            print("  %-28s %s" % (name, "PASS" if not errs else "FAIL (%d)" % len(errs)))
            for e in errs[:8]:
                print("      " + e)
            failed |= bool(errs)
        if not args.no_selftest and not failed:
            print("Self-test (each fix reverted on a served copy; the file is never touched):")
            for fault, patches in REVERT.items():
                game = fault.split(" ")[0]
                errs = (await run_checks(browser, root, {game}, patches))[game]
                print("  %-34s %s" % (fault, ("CAUGHT (%d, e.g. %s)" % (len(errs), errs[0][:90])) if errs else "*** MISSED ***"))
                failed |= not errs
        await browser.close()
    print("FAILED" if failed else "PASS")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--no-selftest", action="store_true")
    return asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
