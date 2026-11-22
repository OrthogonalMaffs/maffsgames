#!/usr/bin/env python3
"""Does every game's text meet WCAG AA contrast as it shows on screen? (contract SITE-CONTRAST, 22 Nov 2026; canon 7.5)

    python scripts/check-contrast.py                       # every roster game, normal and Aa mode
    python scripts/check-contrast.py --mode aa             # one mode (CI runs normal and aa as two jobs)
    python scripts/check-contrast.py --only fermi-lab,bearing-blitz
    python scripts/check-contrast.py --json out.json       # every measured element, for the report
    python scripts/check-contrast.py --selftest            # the planted fixture (Chromium, no server)

THE RULE. Text reads at 4.5:1 against what is behind it, or 3:1 when it is large (24 px, or 18.66 px and bold):
WCAG 2 AA, 1.4.3. The shared theme (schools/assets/theme.css) passes, but most games set their own colours, chosen by
eye and never measured: in November 2026 the muted grey of about 45 games was under 4.5:1 on its own background.

WHAT IS MEASURED. Every game on measure-phone-fit.py's roster, through that file's own driver (imported, never copied:
measure_one() reaches the start screen, the first question and the screen after one wrong answer). Each run is handed a
browser whose contexts carry contrast_common's probe: it scans the page when the driver reads the start screen
(__pfStart) and the asking screen (__pfAsking, its last reading), and once more as the driver closes the context,
which is the wrong-answer screen when the driver produced one. At 1366x768 and 390x844, in normal mode and in Aa mode
(mfg_accessible, set as phone-fit sets it). Every visible element that directly holds text is measured
(contrast_common.CONTRAST_JS, the one copy of the measurement).

  Exempt, counted:      disabled controls, aria-hidden (but not KaTeX's drawn maths, .katex-html, which is on
                        screen: KaTeX hides it from screen readers only), effective opacity <= 0.5 (faded by design).
  Unmeasurable, reported per game, never failed and never passed: text on a background image or gradient, painted
                        with background-clip:text, or with a canvas, video or img behind it.
  A game whose question the driver cannot reach is measured on its start screen only, and reported so.

THE STATE FILE, scripts/contrast-state.json: "known-failures", per mode ("normal", "aa"), each game whose failure is
not a colour value (text on a picture, a canvas), with its reason. A failure not on it fails; an entry that no longer
fails fails as stale (phone-fit's pattern), so the list only shrinks. The network guard is the driver's own.

Run in CI by .github/workflows/phone-fit-full.yml (one job per mode), on the games phone-fit measures there.
"""
import argparse
import asyncio
import importlib.util
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import contrast_common as cc  # noqa: E402

_spec = importlib.util.spec_from_file_location("measure_phone_fit", os.path.join(HERE, "measure-phone-fit.py"))
pf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pf)

SIZES = [(1366, 768), (390, 844)]
MODES = ("normal", "aa")
STATE = os.path.join(HERE, "contrast-state.json")

# Page side: wrap the driver's two readings so each also scans the page, keeping the last scan of each.
HOOK_INIT = r"""(() => {
  window.__mcStates = {};
  const mc = () => { try { return %s; } catch (e) { return null; } };
  const wrap = (name, state) => {
    let fn;
    Object.defineProperty(window, name, {configurable: true,
      get() { return fn; },
      set(f) { fn = function () { const r = f.apply(this, arguments); try { window.__mcStates[state] = mc().scan(); } catch (e) { window.__mcStates[state + '_error'] = String(e); } return r; }; }});
  };
  wrap('__pfStart', 'start');
  wrap('__pfAsking', 'ask');
})();""" % cc.CONTRAST_JS
END_JS = "(() => { try { return (%s).scan(); } catch (e) { return {error: String(e)}; } })()" % cc.CONTRAST_JS
STATES_JS = "window.__mcStates || {}"


class _Ctx:
    """A context the driver uses as its own; before it closes, the page's scans are read."""
    def __init__(self, ctx, sink):
        self._ctx, self._sink, self._pages = ctx, sink, []

    def __getattr__(self, name):
        return getattr(self._ctx, name)

    async def new_page(self):
        page = await self._ctx.new_page()
        self._pages.append(page)
        return page

    async def close(self):
        for page in self._pages:
            try:
                got = await asyncio.wait_for(page.evaluate(STATES_JS), timeout=20)
                got["end"] = await asyncio.wait_for(page.evaluate(END_JS), timeout=20)
                self._sink.update(got)
            except Exception as exc:
                self._sink["error"] = str(exc).split("\n")[0][:120]
        await self._ctx.close()


class _Browser:
    def __init__(self, browser):
        self._b = browser

    async def new_context(self, sink, **kw):
        ctx = await self._b.new_context(**kw)
        await ctx.add_init_script(HOOK_INIT)
        return _Ctx(ctx, sink)


class _OneRun:
    """What measure_one() is handed as its browser: one run's contexts report into one sink."""
    def __init__(self, wrapped, sink):
        self._w, self._sink = wrapped, sink

    async def new_context(self, **kw):
        return await self._w.new_context(self._sink, **kw)


async def measure(wrapped, base, slug, size, mode, opts):
    sink = {}
    args = argparse.Namespace(aa=(mode == "aa"), proxy_from_env=opts.proxy_from_env, fonts="real",
                              katex_dir=opts.katex_dir)
    out = await pf.measure_one(_OneRun(wrapped, sink), base, slug, size, args)
    states = {}
    if isinstance(sink.get("start"), list):
        states["start"] = sink["start"]
    if out.get("ask") and isinstance(sink.get("ask"), list):
        states["question"] = sink["ask"]
    if out.get("wrong") and isinstance(sink.get("end"), list):
        states["after a wrong answer"] = sink["end"]
    if not states and isinstance(sink.get("end"), list):
        states["as loaded"] = sink["end"]       # the driver reached nothing it reads: the page as it stood
    return {"slug": slug, "mode": mode, "w": size[0], "h": size[1], "states": states,
            "note": out.get("note", ""), "escaped": out.get("escaped", []), "error": sink.get("error")}


def summarise(rows):
    """{(slug, mode): {...}} from the raw runs: failures deduplicated by element and colours."""
    games = {}
    for r in rows:
        g = games.setdefault((r["slug"], r["mode"]), {"fails": {}, "unmeasurable": {}, "measured": 0, "exempt": {},
                                                       "states": set(), "notes": set(), "elements": 0})
        g["states"] |= {"%s@%dx%d" % (s, r["w"], r["h"]) for s in r["states"]}
        if r["note"]:
            g["notes"].add(r["note"])
        if r["error"]:
            g["notes"].add("probe: " + r["error"])
        for state, recs in r["states"].items():
            for e in recs:
                g["elements"] += 1
                key = (e["el"], e.get("fg"), e.get("bg"))
                if e["kind"] == "exempt":
                    g["exempt"][e["exempt"].split(" ")[0]] = g["exempt"].get(e["exempt"].split(" ")[0], 0) + 1
                elif e["kind"] == "unmeasurable":
                    g["unmeasurable"].setdefault(e["unmeasurable"], set()).add(e["el"])
                else:
                    g["measured"] += 1
                    if e["kind"] == "fail":
                        f = g["fails"].setdefault(key, dict(e, where=set()))
                        f["where"].add("%s@%dx%d" % (state, r["w"], r["h"]))
    return games


def load_state(path=STATE):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {m: data.get("known-failures", {}).get(m, {}) for m in MODES}


def judge(games, known):
    """[(verdict, slug, mode, detail)] and whether the run fails. A failure on the list is KNOWN FAIL; a listed
    entry that passes is STALE; a failure not on it FAILS."""
    out, bad = [], False
    for (slug, mode), g in sorted(games.items()):
        listed = known.get(mode, {}).get(slug)
        if g["fails"]:
            worst = min(f["ratio"] for f in g["fails"].values())
            detail = "%d failing element(s), worst %.2f:1" % (len(g["fails"]), worst)
            if listed:
                out.append(("KNOWN FAIL", slug, mode, detail + " (listed: %s)" % listed))
            else:
                out.append(("FAIL", slug, mode, detail))
                bad = True
        elif listed:
            out.append(("STALE (take it off the list)", slug, mode, "listed (%s) but nothing fails" % listed))
            bad = True
        else:
            reach = "" if any(s.startswith(("question", "after")) for s in g["states"]) else \
                " (start screen only: the driver reached no question)"
            out.append(("PASS", slug, mode, "%d measured%s" % (g["measured"], reach)))
    for mode, entries in known.items():
        for slug in entries:
            if (slug, mode) not in games:
                pass    # not measured in this run (--only, or the other mode's job): not judged
    return out, bad


def fail_lines(g):
    lines = []
    for (el, fg, bg), f in sorted(g["fails"].items(), key=lambda kv: kv[1]["ratio"]):
        lines.append("      %.2f:1 (needs %.1f) %s on %s, %s in %s, %.1fpx/%d, %r [%s]" % (
            f["ratio"], f["need"], fg, bg, el, f["parent"], f["size"], f["weight"], f["text"][:40],
            ", ".join(sorted(f["where"]))))
    return lines


async def run(opts):
    from playwright.async_api import async_playwright
    slugs = pf.roster_slugs()
    if opts.only:
        wanted = [w.strip() for w in opts.only.split(",") if w.strip()]
        missing = sorted(set(wanted) - set(slugs))
        if missing or not wanted:
            sys.exit("no roster game named %s" % ", ".join(repr(m) for m in missing or [opts.only]))
        slugs = [s for s in slugs if s in wanted]
    modes = MODES if opts.mode == "both" else (opts.mode,)
    proc, base = bc.start_stub_server()
    t0 = time.time()
    try:
        async with async_playwright() as p:
            launch = {}
            if opts.proxy_from_env:
                launch["proxy"] = {"server": os.environ["HTTPS_PROXY"], "bypass": "127.0.0.1,localhost"}
            browser = await p.chromium.launch(**launch)
            wrapped = _Browser(browser)
            sem = asyncio.Semaphore(opts.workers)
            jobs = [(s, sz, m) for m in modes for s in slugs for sz in SIZES]
            done = [0]

            async def job(s, sz, m):
                async with sem:
                    r = await measure(wrapped, base, s, sz, m, opts)
                    done[0] += 1
                    if done[0] % 20 == 0:
                        print("  %d/%d measured (%d s)" % (done[0], len(jobs), time.time() - t0), flush=True)
                    return r
            rows = await asyncio.gather(*(job(*j) for j in jobs))
            await browser.close()
    finally:
        proc.terminate()

    escaped = sorted({u for r in rows for u in r["escaped"]})
    if escaped:
        print("NETWORK GUARD BREACHED -- a write request completed:", escaped[:5])
        sys.exit(2)
    if opts.json:
        with open(opts.json, "w", encoding="utf-8", newline="") as fh:
            json.dump(rows, fh)
    games = summarise(rows)
    known = load_state(opts.state)
    verdicts, bad = judge(games, known)
    tot = {"games": len({s for s, _ in games}), "runs": len(rows),
           "states": sum(len(r["states"]) for r in rows), "elements": sum(g["elements"] for g in games.values()),
           "measured": sum(g["measured"] for g in games.values()),
           "exempt": sum(sum(g["exempt"].values()) for g in games.values()),
           "unmeasurable": sum(1 for r in rows for recs in r["states"].values() for e in recs if e["kind"] == "unmeasurable")}
    for v, slug, mode, detail in verdicts:
        g = games[(slug, mode)]
        print("  %-28s %-6s %-28s %s" % (v, mode, slug, detail))
        if v != "PASS":
            for line in fail_lines(g):
                print(line)
        if g["unmeasurable"]:
            print("      unmeasurable (reported): " + "; ".join(
                "%s (%d)" % (k, len(v)) for k, v in sorted(g["unmeasurable"].items())))
        if g["exempt"]:
            print("      exempt: " + ", ".join("%s %d" % kv for kv in sorted(g["exempt"].items())))
        for n in sorted(g["notes"]):
            print("      driver: " + n)
    print("TOTALS games %(games)d, runs %(runs)d, screens %(states)d, text elements %(elements)d: measured "
          "%(measured)d, exempt %(exempt)d, unmeasurable %(unmeasurable)d" % tot)
    print("modes %s at %s in %d s" % (", ".join(modes), ", ".join("%dx%d" % s for s in SIZES), time.time() - t0))
    if bad:
        for v, slug, mode, detail in verdicts:
            if v not in ("PASS", "KNOWN FAIL"):
                print("GATE %s: %s (%s): %s" % (v, slug, mode, detail))
        return 1
    print("OK  every measured game passes or is on %s" % os.path.relpath(opts.state, bc.ROOT))
    return 0


# ── self-test: planted elements on one fixture page, measured by the same probe ─────────────────────────────────
FIXTURE = """<!doctype html><html><head><meta charset="utf-8"><style>
body { background: #ffffff; margin: 0; font: 16px/1.4 sans-serif; }
p { margin: 4px; }
#grey3 { color: #949494; }                       /* 3.03:1 on white */
#large32 { color: #8a8a8a; font-size: 24px; }    /* 3.45:1 at 24px: large */
#small32 { color: #8a8a8a; font-size: 16px; }    /* the same at 16px: caught */
#faded { color: #000; opacity: 0.4; }
#layer { background: rgba(0, 0, 0, 0.2); }       /* over white: #cccccc */
#layer span { color: #ffffff; }
#grad { background: linear-gradient(#000, #333); color: #fff; }
#ok { color: #333; }
#gone { display: none; color: #eee; }
</style></head><body>
<p id="grey3">grey at 3:1</p>
<p id="large32">large text at 3.45:1</p>
<p id="small32">the same grey at 16px</p>
<p id="faded">faded by design</p>
<div id="layer"><span>white on a translucent layer</span></div>
<p id="grad">text on a gradient</p>
<p id="ok">clean text</p>
<p id="gone">hidden</p>
<svg width="200" height="40"><rect width="200" height="40" fill="#1a2744"/><text x="4" y="24" fill="#3a4a6a" id="svgt">svg label</text></svg>
<button disabled style="color:#ddd">disabled</button>
<span class="katex"><span class="katex-html" aria-hidden="true"><span id="kx" style="color:#aaaaaa">x</span></span></span>
<span aria-hidden="true"><span id="deco" style="color:#eeeeee">decoration</span></span>
<div style="position:relative;height:40px"><p id="under" style="color:#eeeeee">painted over</p><div style="position:absolute;inset:0;background:#ffffff"></div></div>
<div style="background:#1a2744;pointer-events:none;padding:4px"><span id="nohit" style="color:#ffffff;pointer-events:auto">white on navy, its box not hit-tested</span></div>
</body></html>"""


def selftest():
    from playwright.async_api import async_playwright
    want = {"grey3": "fail", "large32": "pass", "small32": "fail", "faded": "exempt", "layer-span": "fail",
            "grad": "unmeasurable", "ok": "pass", "svgt": "fail", "disabled": "exempt",
            "kx": "fail", "deco": "exempt", "nohit": "pass"}

    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page(viewport={"width": 800, "height": 600})
            await page.set_content(FIXTURE)
            recs = await page.evaluate("(%s).scan()" % cc.CONTRAST_JS)
            await b.close()
            return recs
    recs = asyncio.run(go())
    got = {}
    for e in recs:
        k = e["el"].split("#")[1].split(".")[0] if "#" in e["el"] else e["el"]
        if e["el"] == "span" and "layer" in e["parent"]:
            k = "layer-span"
        if e["el"] == "button":
            k = "disabled"
        got[k] = e
    bad = []
    for k, kind in want.items():
        e = got.get(k)
        ok = e is not None and e["kind"] == kind
        print("  %s  %-12s want %-12s got %s" % ("PASS" if ok else "FAIL", k, kind,
                                               e and "%s %.2f:1 (%s on %s)" % (e["kind"], e["ratio"] or 0, e.get("fg"), e.get("bg"))))
        if not ok:
            bad.append(k)
    for k in ("gone", "under"):
        if k in got:
            print("  FAIL  %s: a hidden or painted-over element was measured" % k)
            bad.append(k)
    # the composited layer: white on rgba(0,0,0,.2) over white is #cccccc, not black
    lay = got.get("layer-span")
    if lay and lay["bg"] != "#cccccc":
        print("  FAIL  the translucent layer was not composited (bg %s, want #cccccc)" % lay["bg"])
        bad.append("composite")
    # the state file's two rules, on summaries built from the fixture
    fake = [{"slug": "plant", "mode": "normal", "w": 800, "h": 600, "states": {"question": recs}, "note": "",
             "escaped": [], "error": None},
            {"slug": "clean", "mode": "normal", "w": 800, "h": 600,
             "states": {"question": [e for e in recs if e["kind"] != "fail"]}, "note": "", "escaped": [], "error": None}]
    games = summarise(fake)
    for name, known, verdict in (("a failure not listed fails", {}, ("plant", "FAIL")),
                                 ("a listed failure is known", {"normal": {"plant": "planted"}}, ("plant", "KNOWN FAIL")),
                                 ("a stale entry fails", {"normal": {"clean": "planted"}}, ("clean", "STALE (take it off the list)"))):
        v, failed = judge(games, known)
        hit = [x for x in v if x[1] == verdict[0] and x[0] == verdict[1]]
        ok = bool(hit) and failed == (verdict[1] != "KNOWN FAIL" or any(x[0] == "FAIL" for x in v))
        print("  %s  %s" % ("PASS" if hit else "FAIL", name))
        if not hit:
            bad.append(name)
    # lightness_fix, used to choose the new values: same hue, reaches the target, and None when none can
    fx = cc.lightness_fix("#94a3b8", ["#ffffff"])
    if not (fx and cc.ratio(fx, "#ffffff") >= 4.6):
        bad.append("lightness_fix")
    if cc.lightness_fix("#808080", ["#000000", "#ffffff"], target=10) is not None:
        bad.append("lightness_fix impossible")
    print("selftest: %s (%d plants)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(want) + 7))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--only", help="one game slug, or several separated by commas")
    ap.add_argument("--mode", choices=("normal", "aa", "both"), default="both")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--json", help="write every raw measurement to this file")
    ap.add_argument("--state", default=STATE)
    ap.add_argument("--katex-dir", help="serve KaTeX 0.16.9 from this local dist/ (sandbox only)")
    ap.add_argument("--proxy-from-env", action="store_true", help="route Chromium through $HTTPS_PROXY (sandbox only)")
    opts = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if opts.selftest:
        return selftest()
    return asyncio.run(run(opts))


if __name__ == "__main__":
    sys.exit(main())
