#!/usr/bin/env python3
# ci-line: Shared plotter (schools/assets/plot.js, MaffsPlot, in Chromium: axes through 0 or along the edge nearer it, ticks and grid at nice steps or at multiples of pi/2, a curve broken at a value that is not finite, the reveal and the pens, hidden tab and off-screen pauses, reduced motion, every text through KaTeX, colours from the page's variables, each path read back to its function within 1 px; eleven planted faults) |
# ci-deps: schools/assets/plot.js
"""Browser test for the shared plotter, schools/assets/plot.js (contract D-BY-DX-GRAPH, 27 Nov 2026).

    python scripts/test-plot.py            # the repo's plotter
    python scripts/test-plot.py --plot path/to/plot.js

Loads the plotter into a bare page in headless Chromium (a stand-in for KaTeX that records what it is asked to draw;
no network) and checks what its header promises:

  axes         through 0 where 0 is in the window, otherwise along the edge nearer 0, on three windows; 0 is written
               once at most where the axes cross; the axis letters are the caller's
  ticks        at multiples of a step of 1, 2 or 5 times a power of ten, at most five gaps across and six up; one
               grid line and one label a tick, each label at its tick; the window is the caller's, never changed
  pi           ticks "pi": multiples of pi/2 named in pi (pi/2, pi, 3pi/2, 2pi), and of 2 pi on a window of 12 pi
  broken       a function with a gap (not finite on part of the window) and one that throws: two sub-paths, no point
               in the gap, never a line across it
  readback     every point of a path, mapped back through the path's own data attributes, is within 1 px of the
               function; the path spans the window; at 300 px and at 1400 px wide it holds at least one point for
               every 2 px of the plot's width (a box that grows is sampled again)
  reveal       a curve added with reveal is not there at once, draws in left to right and is all there in about
               0.6 s; its label shows only then; a curve added without it is there at once
  pens         two curves drawn together: at every reading the same progress and both tips at the same x, each on
               its own curve; onLand as they finish (the tips go, the labels show), onDone `hold` ms later, once
  pauses       pause() and resume(); a hidden tab; a plot that is not on screen (its box not displayed): the drawing
               stops where it is and carries on after
  still        with prefers-reduced-motion: a reveal is there at once; pens have no tips and are finished at once
  text         every tick label, axis letter and curve label goes through KaTeX; without KaTeX the bare text shows
  look         the two tones take the page's --maffs-plot-1 and --maffs-plot-2 and differ in width; dash is drawn
               dashed; the svg has the documented viewBox and no canvas is made; the file reads no pointer position
  plants       eleven planted plotters, each of which must FAIL at least one of the cases above

Exits non-zero on any failure. --chromium names a browser binary when Playwright's own build is not installed.
"""
import argparse
import asyncio
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_PLOT = os.path.join(ROOT, "schools", "assets", "plot.js")
VW, VH = 480, 340

FIXTURE = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;background:rgb(24,32,51);color:rgb(232,236,244);font:16px sans-serif}
:root{--maffs-plot-1:rgb(196, 181, 253);--maffs-plot-2:rgb(251, 191, 36)}
#mount{width:%(width)dpx}</style>
%(katex)s<script>%(plot)s</script></head>
<body><div id="mount"></div><script>
  window.FN = {
    cubic: function (x) { return x * x * x - 3 * x; }, slope: function (x) { return 3 * x * x - 3; },
    sin3: function (x) { return Math.sin(3 * x); },
    gap: function (x) { return Math.sqrt(x * x - 0.25); },                 // not finite for -0.5 < x < 0.5
    thrower: function (x) { if (Math.abs(x) < 0.5) throw new Error('no value here'); return x; }
  };
  window.log = [];
  window.make = function (o) { window.log.length = 0; if (window.plot) window.plot.destroy(); window.plot = MaffsPlot.create(document.getElementById('mount'), o); return !!window.plot; };
  window.read = function () {
    var root = document.querySelector('.maffs-plot'), svg = root && root.querySelector('svg');
    if (!svg) return null;
    var num = function (el, k) { return parseFloat(el.getAttribute(k)); };
    var text = function (n) { var a = n.querySelector('annotation'); return a ? a.textContent : n.textContent; };
    var r = svg.getBoundingClientRect();
    return {
      width: r.width, viewBox: svg.getAttribute('viewBox'), canvases: document.querySelectorAll('canvas').length,
      aria: root.getAttribute('aria-label'), role: root.getAttribute('role'),
      axes: [].map.call(svg.querySelectorAll('[data-axis]'), function (l) { return { axis: l.dataset.axis, at: +l.dataset.at, x1: num(l, 'x1'), y1: num(l, 'y1'), x2: num(l, 'x2'), y2: num(l, 'y2') }; }),
      ticks: [].map.call(svg.querySelectorAll('[data-tick]'), function (l) { return { axis: l.dataset.tick, v: +l.dataset.v, x: (num(l, 'x1') + num(l, 'x2')) / 2, y: (num(l, 'y1') + num(l, 'y2')) / 2 }; }),
      grid: [].map.call(svg.querySelectorAll('[data-grid]'), function (l) { return l.dataset.grid; }),
      labels: [].map.call(root.querySelectorAll('.maffs-plot-tick'), function (n) { return { axis: n.classList.contains('maffs-plot-tick-x') ? 'x' : 'y', v: +n.dataset.v, tex: text(n), left: parseFloat(n.style.left), top: parseFloat(n.style.top), katex: !!n.querySelector('.katex') }; }),
      letters: [].map.call(root.querySelectorAll('.maffs-plot-letter'), function (n) { return { axis: n.dataset.axis, tex: text(n), katex: !!n.querySelector('.katex') }; }),
      paths: [].map.call(svg.querySelectorAll('path.maffs-plot-curve'), function (p) { var cs = getComputedStyle(p); return { id: p.dataset.curve, tone: p.dataset.tone, d: p.getAttribute('d') || '',
        x0: +p.dataset.x0, x1: +p.dataset.x1, y0: +p.dataset.y0, y1: +p.dataset.y1, box: p.dataset.box.split(' ').map(Number), progress: +p.dataset.progress,
        stroke: cs.stroke, wide: parseFloat(cs.strokeWidth), dash: cs.strokeDasharray }; }),
      tips: [].map.call(svg.querySelectorAll('.maffs-plot-tip'), function (c) { return { id: c.dataset.curve, x: +c.dataset.x, cx: num(c, 'cx'), cy: num(c, 'cy'), shown: c.getAttribute('display') !== 'none' }; }),
      names: [].map.call(root.querySelectorAll('.maffs-plot-name'), function (n) { return { id: n.dataset.curve, tex: text(n), on: n.classList.contains('is-on'), katex: !!n.querySelector('.katex') }; }),
      state: window.plot.state(), log: window.log.slice()
    };
  };
</script></body></html>"""
KATEX_STUB = ("<script>window.katex = { asked: [], render: function (s, el) { this.asked.push(s); "
              "el.innerHTML = '<span class=\"katex\"><annotation></annotation></span>'; el.querySelector('annotation').textContent = s; } };</script>")

# Plants: (name, old text, new text). Each planted plotter must fail at least one case.
PLANTS = [
    ("the x-axis always along the edge", "var ax = win.y0 <= 0 && 0 <= win.y1 ? 0 : ", "var ax = false ? 0 : "),
    ("ticks at steps that are not nice", "return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p;", "return raw;"),
    ("pi ticks ignored", "var xt = win.ticks === 'pi' ? piTicks(win.x0, win.x1) : numTicks(win.x0, win.x1, 5);", "var xt = numTicks(win.x0, win.x1, 5);"),
    ("a line joined across a value that is not finite", "{ open = false; continue; }", "{ continue; }"),
    ("a curve drawn 3 units off", "d += (open ? 'L' : 'M') + num(X(x)) + ' ' + num(py);", "d += (open ? 'L' : 'M') + num(X(x)) + ' ' + num(py + 3);"),
    ("sixty samples whatever the width", "return Math.max(480, Math.ceil(w / 2));", "return 60;"),
    ("a reveal that is there at once", "if (o.reveal) start(", "if (false) start("),
    ("pens at different x", "var x = win.x0 + (win.x1 - win.x0) * p, y;", "var x = win.x0 + (win.x1 - win.x0) * p * (c.tone === 2 ? 0.9 : 1), y;"),
    ("a hidden tab or an off-screen plot keeps drawing", "function paused() { return held || !seen || document.hidden; }", "function paused() { return held; }"),
    ("reduced motion ignored", "var still = reducedMotion();", "var still = false;"),
    ("text not sent through KaTeX", "if (window.katex && typeof window.katex.render === 'function') {", "if (false) {"),
]


def points(d):
    return [(float(a), float(b)) for a, b in re.findall(r"[ML]\s*(-?\d+(?:\.\d+)?)[ ,](-?\d+(?:\.\d+)?)", d)]


def nice(step):
    m = step / 10 ** math.floor(math.log10(step) + 1e-9)
    return any(abs(m - k) < 1e-6 for k in (1, 2, 5, 10))


async def cases(browser, plot_js, check):
    """Every case, on this plotter's text. check(name, ok, detail) records each."""
    async def page_for(width=480, katex=True, reduced=False, height=700):
        ctx = await browser.new_context(viewport={"width": max(width + 40, 400), "height": height},
                                        reduced_motion="reduce" if reduced else "no-preference")
        page = await ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.set_content(FIXTURE % {"width": width, "katex": KATEX_STUB if katex else "", "plot": plot_js})
        return ctx, page, errors

    async def settle(page, ms=120):
        await page.wait_for_timeout(ms)

    def X(r, x, p=None):
        b = (p or r["paths"][0])["box"] if (p or r["paths"]) else [46, 28, 364, 280]
        w = r["state"]["window"]
        return b[0] + (x - w["x"][0]) / (w["x"][1] - w["x"][0]) * b[2]

    def Y(r, y):
        b, w = r["state"]["box"], r["state"]["window"]
        return b[1] + (w["y"][1] - y) / (w["y"][1] - w["y"][0]) * b[3]

    # ---- axes and ticks, on three windows
    ctx, page, errors = await page_for()
    wins = [("both through 0", [-2, 2], [-200, 200], 0, 0, [-2, -1, 0, 1, 2], [-200, -100, 0, 100, 200]),
            ("the y-axis along the left edge", [0.5, 3], [-55, 20], 0, 0.5, [0.5, 1, 1.5, 2, 2.5, 3], [-40, -20, 0, 20]),
            ("both along the edges nearer 0", [-3, -1], [2, 6], 2, -1, [-3, -2.5, -2, -1.5, -1], [2, 3, 4, 5, 6])]
    for name, wx, wy, ax, ay, xt, yt in wins:
        await page.evaluate("(o) => make(o)", {"x": wx, "y": wy, "xLabel": "t", "yLabel": "s", "aria": "A test graph"})
        r = await page.evaluate("read()")
        box = r["state"]["box"]
        axes = {a["axis"]: a for a in r["axes"]}
        ok = (set(axes) == {"x", "y"} and axes["x"]["at"] == ax and axes["y"]["at"] == ay
              and abs(axes["x"]["y1"] - Y(r, ax)) < 0.02 and abs(axes["x"]["y2"] - Y(r, ax)) < 0.02
              and abs(axes["y"]["x1"] - (box[0] + (ay - wx[0]) / (wx[1] - wx[0]) * box[2])) < 0.02)
        check("axes: " + name, ok, "x-axis at y = %s, y-axis at x = %s" % (axes.get("x", {}).get("at"), axes.get("y", {}).get("at")))
        got_x = sorted(t["v"] for t in r["ticks"] if t["axis"] == "x")
        got_y = sorted(t["v"] for t in r["ticks"] if t["axis"] == "y")
        near = lambda a, b: len(a) == len(b) and all(abs(p - q) < 1e-9 for p, q in zip(a, b))   # noqa: E731
        steps = [b - a for g in (got_x, got_y) for a, b in zip(g, g[1:])]
        check("ticks: " + name, near(got_x, xt) and near(got_y, yt) and all(nice(s) for s in steps),
              "x %s, y %s" % (got_x, got_y))
        check("grid: one line a tick (%s)" % name, sorted(r["grid"]) == ["x"] * len(got_x) + ["y"] * len(got_y),
              "%d grid lines for %d ticks" % (len(r["grid"]), len(got_x) + len(got_y)))
        both = ax == 0 and ay == 0
        want_x = [v for v in xt if not (both and v == 0)]
        want_y = [v for v in yt if not (both and wx[0] < 0 and v == 0)]
        lx = sorted(lb["v"] for lb in r["labels"] if lb["axis"] == "x")
        ly = sorted(lb["v"] for lb in r["labels"] if lb["axis"] == "y")
        placed = all(abs(lb["left"] / 100 * VW - (box[0] + (lb["v"] - wx[0]) / (wx[1] - wx[0]) * box[2])) < 0.05 for lb in r["labels"] if lb["axis"] == "x") and \
            all(abs(lb["top"] / 100 * VH - Y(r, lb["v"])) < 0.05 for lb in r["labels"] if lb["axis"] == "y")
        texts = all(abs(float(lb["tex"]) - lb["v"]) < 1e-9 for lb in r["labels"])
        check("labels: one a tick, at its tick, 0 once at most (%s)" % name, near(lx, want_x) and near(ly, want_y) and placed and texts,
              "x %s, y %s" % (lx, ly))
        w = r["state"]["window"]
        check("the window is the caller's (%s)" % name, w["x"] == wx and w["y"] == wy, str(w))
        check("the axis letters are the caller's (%s)" % name, sorted((x["axis"], x["tex"]) for x in r["letters"]) == [("x", "t"), ("y", "s")], str(r["letters"]))
    check("the picture is one image to a screen reader", r["role"] == "img" and r["aria"] == "A test graph", "%s, %r" % (r["role"], r["aria"]))
    check("the documented viewBox, and no canvas", r["viewBox"] == "0 0 %d %d" % (VW, VH) and r["canvases"] == 0, "%s, %d canvas" % (r["viewBox"], r["canvases"]))

    # ---- pi ticks
    await page.evaluate("(o) => make(o)", {"x": [0, 2 * math.pi], "y": [-1.5, 1.5], "ticks": "pi"})
    r = await page.evaluate("read()")
    got = [(round(lb["v"] / (math.pi / 2), 6), lb["tex"]) for lb in sorted((x for x in r["labels"] if x["axis"] == "x"), key=lambda x: x["v"])]
    check("pi ticks: multiples of pi/2, named in pi", got == [(1.0, "\\frac{\\pi}{2}"), (2.0, "\\pi"), (3.0, "\\frac{3\\pi}{2}"), (4.0, "2\\pi")], str(got))
    await page.evaluate("(o) => make(o)", {"x": [0, 12 * math.pi], "y": [-1.5, 1.5], "ticks": "pi"})
    r = await page.evaluate("read()")
    got = [lb["tex"] for lb in sorted((x for x in r["labels"] if x["axis"] == "x"), key=lambda x: x["v"])]
    check("pi ticks: no more than eight gaps on a long window", got == ["2\\pi", "4\\pi", "6\\pi", "8\\pi", "10\\pi", "12\\pi"], str(got))

    # ---- a curve broken where it has no value
    for fn in ("gap", "thrower"):
        await page.evaluate("(o) => make(o)", {"x": [-2, 2], "y": [-2.5, 2.5]})
        await page.evaluate("(f) => { plot.add('f', FN[f], { tone: 1 }); }", fn)
        r = await page.evaluate("read()")
        p = r["paths"][0]
        pts = points(p["d"])
        lo, hi = X(r, -0.5, p), X(r, 0.5, p)
        pieces = p["d"].count("M")
        inside = [a for a in pts if lo + 0.02 < a[0] < hi - 0.02]
        subs = [points(s) for s in p["d"].split("M") if s]
        across = any(s[0][0] < lo and s[-1][0] > hi for s in subs if s)
        check("broken: a function with a gap (%s)" % fn, pieces == 2 and not inside and not across and len(pts) > 100,
              "%d pieces, %d points in the gap, %s" % (pieces, len(inside), "a line across it" if across else "no line across it"))

    # ---- readback, and the sampling
    for width in (300, 1400):
        c2, p2, e2 = await page_for(width=width)
        await p2.evaluate("(o) => make(o)", {"x": [0, 2 * math.pi], "y": [-1.5, 1.5], "ticks": "pi"})
        await p2.evaluate("plot.add('f', FN.sin3, { tone: 1, label: 'y' })")
        await settle(p2, 200)
        r = await p2.evaluate("read()")
        p = r["paths"][0]
        pts = points(p["d"])
        left, top, w, h = p["box"]
        scale = r["width"] / VW
        worst = max(abs(py - (top + (p["y1"] - math.sin(3 * (p["x0"] + (px - left) / w * (p["x1"] - p["x0"])))) / (p["y1"] - p["y0"]) * h)) * scale for px, py in pts) if pts else 99
        spans = bool(pts) and abs(pts[0][0] - left) < 0.02 and abs(pts[-1][0] - (left + w)) < 0.02
        check("readback at %d px: every point within 1 px of the function" % width, worst <= 1.0 and spans and p["d"].count("M") == 1,
              "worst %.3f px over %d points" % (worst, len(pts)))
        need = math.ceil(w * scale / 2)
        check("sampling at %d px: one point for every 2 px" % width, len(pts) >= need, "%d points, %d needed" % (len(pts), need))
        check("no page error at %d px" % width, not e2, "; ".join(e2)[:160])
        await c2.close()

    # ---- look: tones, dash, labels through KaTeX
    await page.evaluate("(o) => make(o)", {"x": [-2.2, 2.2], "y": [-5, 15], "xLabel": "x", "yLabel": "y"})
    await page.evaluate("plot.add('f', FN.cubic, { tone: 1, label: 'y' }); plot.add('d', FN.slope, { tone: 2, label: \"y'\", dash: true });")
    await settle(page)
    r = await page.evaluate("read()")
    f, d = r["paths"]
    check("tones: the page's two colours, the second the wider line", f["stroke"] == "rgb(196, 181, 253)" and d["stroke"] == "rgb(251, 191, 36)" and d["wide"] > f["wide"],
          "%s %s px, %s %s px" % (f["stroke"], f["wide"], d["stroke"], d["wide"]))
    check("dash: drawn dashed only where asked", d["dash"] not in ("none", "") and f["dash"] == "none", "%s / %s" % (f["dash"], d["dash"]))
    check("a curve added without reveal is there at once, with its label", f["progress"] == 1 and all(n["on"] for n in r["names"]) and [n["tex"] for n in r["names"]] == ["y", "y'"],
          "progress %s, labels %s" % (f["progress"], r["names"]))
    texts = r["labels"] + r["letters"] + r["names"]
    check("text: every label through KaTeX", bool(texts) and all(t["katex"] for t in texts), "%d of %d" % (sum(1 for t in texts if t["katex"]), len(texts)))

    # ---- reveal
    await page.evaluate("(o) => make(o)", {"x": [-2.2, 2.2], "y": [-5, 15]})
    await page.evaluate("plot.add('f', FN.cubic, { tone: 1 }); plot.add('d', FN.slope, { tone: 2, label: 'd', reveal: true, onDone: function () { log.push('revealed'); } });")
    seen = []
    for _ in range(40):                                  # about 0.6 s; a slow machine draws fewer frames and takes longer
        await page.wait_for_timeout(100)
        r = await page.evaluate("read()")
        seen.append((r["paths"][1]["progress"], r["names"][0]["on"]))
        if seen[-1][0] == 1 and len(seen) >= 2 and seen[-2][0] == 1:
            break
    prog = [s[0] for s in seen]
    mid = [s for s in seen if 0 < s[0] < 1]
    done_at = next((i for i, v in enumerate(prog) if v == 1), None)
    check("reveal: draws in left to right, all there in about 0.6 s", len(mid) >= 2 and prog == sorted(prog) and done_at is not None and done_at >= 3,
          "progress each 0.1 s: %s" % prog)
    check("reveal: its label shows only when it is all there", all(not on for v, on in seen if v < 1) and seen[-1][1] and r["log"] == ["revealed"], str(seen[-1]) + " " + str(r["log"]))

    # ---- pens
    await page.evaluate("(o) => make(o)", {"x": [-2.2, 2.2], "y": [-5, 15]})
    await page.evaluate("""plot.pens([{ id: 'f', fn: FN.cubic, tone: 1, label: 'y' }, { id: 'd', fn: FN.slope, tone: 2, label: 'dy' }],
        { duration: 1200, hold: 500, onLand: function () { log.push('land'); }, onDone: function () { log.push('done'); } });""")
    same_x = on_curve = together = unlabelled = True
    count, landed = 0, None
    for i in range(120):
        await page.wait_for_timeout(70)
        r = await page.evaluate("read()")
        if len(r["tips"]) == 2 and not r["log"]:
            a, b = r["tips"]
            p = [x["progress"] for x in r["paths"]]
            if 0 < p[0] < 1:
                count += 1
            same_x = same_x and a["x"] == b["x"] and abs(a["cx"] - b["cx"]) < 0.011
            together = together and p[0] == p[1]
            for tip, fn in ((a, lambda x: x ** 3 - 3 * x), (b, lambda x: 3 * x * x - 3)):
                y = fn(tip["x"])
                inside = -5 <= y <= 15
                on_curve = on_curve and tip["shown"] == inside and (not inside or abs(tip["cy"] - Y(r, y)) * r["width"] / VW <= 1.0)
            unlabelled = unlabelled and not any(n["on"] for n in r["names"])
        if landed is None and "land" in r["log"]:
            landed = (i, len(r["tips"]), [n["on"] for n in r["names"]], [x["progress"] for x in r["paths"]], list(r["log"]))
        if "done" in r["log"]:
            break
    check("pens: the same x at every reading", same_x and together and count >= 5, "%d readings while drawing" % count)
    check("pens: each tip on its own curve", on_curve and count >= 5, "")
    check("pens: onLand as they finish (tips gone, labels shown)", landed is not None and landed[1] == 0 and landed[2] == [True, True] and landed[3] == [1, 1] and unlabelled, str(landed))
    for _ in range(40):
        if "done" in (await page.evaluate("read()"))["log"]:
            break
        await page.wait_for_timeout(100)
    r = await page.evaluate("read()")
    check("pens: onDone once, after the hold", r["log"] == ["land", "done"] and landed is not None and landed[4] == ["land"], str(r["log"]))

    # ---- pauses: pause()/resume(), a hidden tab, a plot that is not on screen
    async def progress():
        return (await page.evaluate("read()"))["paths"][0]["progress"]

    async def stops(name, stop, start):
        await page.evaluate("(o) => make(o)", {"x": [-2.2, 2.2], "y": [-5, 15]})
        await page.evaluate("plot.pens([{ id: 'f', fn: FN.cubic, tone: 1 }], { duration: 3000 });")
        await page.wait_for_timeout(350)
        await page.evaluate(stop)
        await page.wait_for_timeout(200)
        p1 = await progress()
        await page.wait_for_timeout(450)
        p2 = await progress()
        await page.evaluate(start)
        await page.wait_for_timeout(450)
        p3 = await progress()
        check("pauses: " + name, 0 < p1 < 1 and p2 == p1 and p3 > p2, "progress %s, %s while stopped, %s after" % (p1, p2, p3))
    await stops("pause() and resume()", "plot.pause()", "plot.resume()")
    await stops("a hidden tab", "(() => { Object.defineProperty(document, 'hidden', { configurable: true, get: () => true }); document.dispatchEvent(new Event('visibilitychange')); })()",
                "(() => { delete document.hidden; document.dispatchEvent(new Event('visibilitychange')); })()")
    await stops("a plot that is not on screen", "document.getElementById('mount').style.display = 'none'", "document.getElementById('mount').style.display = ''")
    check("no page error", not errors, "; ".join(errors)[:160])
    await ctx.close()

    # ---- reduced motion
    ctx, page, errors = await page_for(reduced=True)
    await page.evaluate("(o) => make(o)", {"x": [-2.2, 2.2], "y": [-5, 15]})
    await page.evaluate("plot.add('d', FN.slope, { tone: 2, label: 'd', reveal: true, onDone: function () { log.push('revealed'); } });")
    r = await page.evaluate("read()")
    check("still: a reveal is there at once", r["paths"][0]["progress"] == 1 and r["names"][0]["on"] and r["log"] == ["revealed"], "progress %s, %s" % (r["paths"][0]["progress"], r["log"]))
    await page.evaluate("(o) => { log.length = 0; make(o); }", {"x": [-2.2, 2.2], "y": [-5, 15]})
    await page.evaluate("""plot.pens([{ id: 'f', fn: FN.cubic, tone: 1, label: 'y' }, { id: 'd', fn: FN.slope, tone: 2, label: 'dy' }],
        { duration: 1200, hold: 300, onLand: function () { log.push('land'); }, onDone: function () { log.push('done'); } });""")
    r = await page.evaluate("read()")
    check("still: pens are finished at once, with no tips", not r["tips"] and [p["progress"] for p in r["paths"]] == [1, 1] and r["log"] == ["land"] and r["state"]["still"],
          "tips %d, progress %s, %s" % (len(r["tips"]), [p["progress"] for p in r["paths"]], r["log"]))
    for _ in range(40):
        if "done" in (await page.evaluate("read()"))["log"]:
            break
        await page.wait_for_timeout(100)
    r = await page.evaluate("read()")
    check("still: onDone after the hold", r["log"] == ["land", "done"], str(r["log"]))
    check("no page error (reduced motion)", not errors, "; ".join(errors)[:160])
    await ctx.close()

    # ---- without KaTeX: the bare text
    ctx, page, errors = await page_for(katex=False)
    await page.evaluate("(o) => make(o)", {"x": [-2, 2], "y": [-200, 200], "xLabel": "t", "yLabel": "s"})
    r = await page.evaluate("read()")
    check("text: without KaTeX the bare text shows", sorted(x["tex"] for x in r["letters"]) == ["s", "t"] and len(r["labels"]) == 8 and not errors, str(r["letters"]))
    await ctx.close()


def static(plot_js, check):
    hits = re.findall(r"\b(?:client|page|offset|screen)[XY]\b", plot_js)
    check("the plotter reads no pointer position", not hits, ", ".join(sorted(set(hits))))
    made = re.findall(r"createElement(?:NS)?\([^)]*canvas", plot_js)
    check("the plotter makes no canvas", not made, "")
    check("the plotter sets no timer of its own", not re.search(r"\bset(?:Timeout|Interval)\s*\(", plot_js), "animation frames only")


async def run(plot_js, chromium):
    from playwright.async_api import async_playwright
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))
        print("  %s  %-64s %s" % ("PASS" if ok else "FAIL", name, detail))

    static(plot_js, check)
    async with async_playwright() as p:
        kw = {"executable_path": chromium} if chromium else {}
        browser = await p.chromium.launch(**kw)
        await cases(browser, plot_js, check)
        for name, old, new in PLANTS:
            if plot_js.count(old) != 1:
                check("plant: " + name, False, "STALE PLANT: its text is in the plotter %d times, not once" % plot_js.count(old))
                continue
            got, err = [], None
            try:
                await cases(browser, plot_js.replace(old, new), lambda n, ok, d="": got.append((n, ok)))
            except Exception as e:  # noqa: BLE001
                err = e                                   # an error is never a catch (plant_common's rule)
            failed = [n for n, ok in got if not ok]
            check("plant caught: " + name, bool(failed) and err is None,
                  ("fails: " + "; ".join(failed[:3])) if failed else ("nothing failed" + (" (error: %s)" % str(err).splitlines()[0][:80] if err else "")))
        await browser.close()
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--plot", default=DEFAULT_PLOT)
    ap.add_argument("--chromium", help="launch this Chromium binary instead of Playwright's own")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    with open(args.plot, encoding="utf-8") as f:
        plot_js = f.read()
    print("plot.js:", os.path.relpath(args.plot, ROOT) if args.plot.startswith(ROOT) else args.plot)
    results = asyncio.run(run(plot_js, args.chromium))
    bad = [r for r in results if not r[1]]
    print("%d checks, %d failed" % (len(results), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
