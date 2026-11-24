#!/usr/bin/env python3
"""Does every calculator game dock its calculator beside the question on a laptop? (canon 4.4, contract CALC-DOCK-COLUMN)

    python scripts/check-calc-dock.py                     # CI: every calculator game at 1366x768 and 1440x900
    python scripts/check-calc-dock.py --only its-a-sine   # one game, or several separated by commas
    python scripts/check-calc-dock.py --selftest          # two planted faults on a copy of the repo must each fail

WHY. On a laptop the shared calculator (schools/assets/calculator.js, MaffsCalc) opens beside the question card, docked
in the room to its right, so the question and the keys are on screen together. Until 24 Nov 2026 it docked only when a
game happened to leave room: three games that widen their column (the ice cream game, It's a SINE!!, CAST Away) never
docked below about 1720px, and six games passed no dock element at all, so their calculator always opened underneath
(Jon, 24 Nov 2026: "why is the calculator below when we have so much real estate on the screen"). MaffsCalc now
narrows the game column just enough to dock (canon 4.4, "The column makes room"), and this check holds every
calculator game to it.

WHICH GAMES. Every roster game whose Calculator field is required, optional, scientific or by stage, read from
.claude/rules/game-roster.md by check-calculator.py's own reader (imported, never a typed list). A by stage game is
started on the first stage its page's stage map (check-calculator.py's STAGE_MAP) does not mark "not allowed".

THE TEST. In Chromium at 1366x768 and at 1440x900: load the page (check-site.py's open_guarded_page), begin play
(check-start-mount.py's START_STEPS for the games that need their own controls, otherwise a level control or Start,
then check-site.py's drive_to_start; all imported, not copied), wait for the visible Calculator toggle, read the
card's box, click the toggle, and require: the calculator is docked (`.maffs-calc.docked`); its panel is inside the
window, right of the card; and the card's box, so the game column, is the same as before opening.
"""
import argparse
import asyncio
import importlib.util
import json
import os
import pathlib
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = pathlib.Path(HERE).parent
SIZES = [(1366, 768), (1440, 900)]
CALC_GAME_VALUES = {"required", "optional", "scientific", "by stage"}


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CC = _load("check_calculator", "check-calculator.py")
SM = _load("check_start_mount", "check-start-mount.py")


def calc_games(root, only=None):
    """{slug: stage key or None} for every roster game with a calculator (in `only`, if given), from the roster."""
    out = {}
    for slug, val in CC.roster(root).items():
        if val not in CALC_GAME_VALUES or (only and slug not in only):
            continue
        stage = None
        if val == "by stage":
            src = (root / "games" / slug / "index.html").read_text(encoding="utf-8")
            m = CC.STAGE_MAP.search(src)
            stages = json.loads(m.group(1)) if m else {}
            stage = next((k for k, v in stages.items() if v != "not allowed"), None)
        out[slug] = stage
    return out


# Staged games open on a worked example, stepped one tap at a time: its buttons are pressed until the question (and its
# calculator) shows. The words are the games' own (take-a-walk, squared-squirrel, its-on-sale, who-ate-all-the-pies).
# A stage button that only selects its stage (take-a-walk, squared-squirrel) is followed by the page's Start.
ADVANCE = ("Show the first step", "Show the next step", "Start the questions")
# A game whose question asks something else before its answer box and calculator show: the step that answers it.
REACH = {
    # Round 1 opens with "Tap the hypotenuse." (no score); the page's own maffs-lock-hint plays it the same way.
    "just-pythag-it-bruv": "window.JPIB && JPIB.ui && JPIB.ui.state() === 'tap' && JPIB.ui.tap('r')",
}

# The page side. The card is the calculator's dock element (.maffs-calc-host); the toggle is the first one shown.
PROBE = """(() => {
  const vis = e => !!e && e.checkVisibility && e.checkVisibility();
  const t = [...document.querySelectorAll('.maffs-calc-toggle')].find(vis);
  const calc = t && t.closest('.maffs-calc');
  const host = document.querySelector('.maffs-calc-host');
  const R = e => { if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
  return { toggle: !!t, hosts: document.querySelectorAll('.maffs-calc-host').length, card: R(host),
    docked: !!(calc && calc.classList.contains('docked')), open: !!(t && t.getAttribute('aria-expanded') === 'true'),
    panel: R(calc && calc.querySelector('.maffs-calc-panel')), cw: document.documentElement.clientWidth, vh: innerHeight };
})()"""


async def _begin(cs, page, ev, rec, slug, stage, timeout_ms):
    """Press whatever begins play; True if it began (or the game's own controls were pressed)."""
    err0 = len(rec["errs"])
    steps = []
    if stage is not None:
        n = stage.rsplit("-", 1)[-1]
        btn = page.locator('button[data-mode="%s"]' % stage)
        if not await btn.count() and n.isdigit():
            btn = page.locator('button[data-stage="%s"]' % n)
        if await btn.count():
            await btn.first.click(timeout=timeout_ms)
            await page.wait_for_timeout(300)
            if await ev("window.__mfgHasStart()"):
                await ev("window.__mfgClickStart()")
            return True
    if slug in SM.START_STEPS:
        for step in SM.START_STEPS[slug]:
            if isinstance(step, tuple):
                await page.locator(step[0]).first.fill(step[1], timeout=timeout_ms)
            else:
                await page.locator(step).first.click(timeout=timeout_ms)
        return True
    if await ev("window.__mfgLevelControls().length"):
        steps = await ev("window.__mfgLevelPress(0)")
    else:
        steps = ["start"] if await ev("window.__mfgClickStart()") else []
    return (await ev("window.__mfgStats()"))["started"] or await cs.drive_to_start(page, ev, rec, steps, err0)


async def _game(cs, browser, base, slug, stage, w, h, timeout_ms):
    at = "%s %dx%d" % (slug, w, h)
    ctx = await browser.new_context(viewport={"width": w, "height": h})
    await ctx.add_init_script(cs.TIER3_INIT)
    await ctx.add_init_script(cs.LEVEL_INIT)
    try:
        page, rec = await cs.open_guarded_page(ctx, base, "games/%s/index.html" % slug, timeout_ms, fonts="real")

        async def ev(expr):
            return await asyncio.wait_for(page.evaluate(expr), timeout=timeout_ms / 1000.0)
        if not await _begin(cs, page, ev, rec, slug, stage, timeout_ms):
            return ["%s: could not begin play with check-site.py's drive_to_start" % at]
        m = None
        for _ in range(60):                          # up to 12 s for the question and its Calculator toggle
            await page.wait_for_timeout(200)
            m = await ev(PROBE)
            if m["toggle"] and m["card"] and m["card"][2] > m["card"][0]:
                break
            if slug in REACH:
                await ev(REACH[slug])
            for word in ADVANCE:
                b = page.get_by_role("button", name=word, exact=True)
                if await b.count() and await b.first.is_visible():
                    await page.wait_for_timeout(350)    # past MaffsLock's fresh window (300 ms)
                    await b.first.click(timeout=timeout_ms)
                    break
        if not m["toggle"]:
            return ["%s: no Calculator toggle shown once play began" % at]
        if not m["hosts"]:
            return ["%s: the calculator has no dock element (MaffsCalc.mount without {dock})" % at]
        await page.wait_for_timeout(700)             # past MaffsLock's fresh window and the column's first layout
        before = await ev(PROBE)
        await page.locator(".maffs-calc-toggle >> visible=true").first.click(timeout=timeout_ms)
        await page.wait_for_timeout(300)
        after = await ev(PROBE)
        out = []
        if not after["open"]:
            out.append("%s: the Calculator toggle did not open the panel" % at)
        elif not after["docked"]:
            out.append("%s: the calculator opened in the flow, not docked beside the card (card right %.0f, window %d)"
                       % (at, after["card"][2], after["cw"]))
        else:
            P, C = after["panel"], after["card"]
            if P[0] < C[2] or P[2] > after["cw"] or P[1] < 0 or P[1] >= after["vh"]:
                out.append("%s: the docked panel %r is not inside the window right of the card %r" % (at, P, C))
        if any(abs(a - b) > 0.5 for a, b in zip(before["card"][::2], after["card"][::2])):
            out.append("%s: opening the calculator moved or resized the card: %r -> %r" % (at, before["card"], after["card"]))
        return out
    except Exception as exc:
        return ["%s: %s" % (at, str(exc).splitlines()[0][:160])]
    finally:
        await ctx.close()


def check(root, only=None, workers=4, timeout_ms=20000):
    from playwright.async_api import async_playwright
    cs = SM._check_site()
    games = calc_games(root, only)
    if not games:
        return ["no calculator games found in the roster: the table changed shape, so this check is blind"], 0
    proc, base = SM._serve(root)

    async def run():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)

            async def one(slug, stage, w, h):
                async with sem:
                    return await _game(cs, browser, base, slug, stage, w, h, timeout_ms)
            out = await asyncio.gather(*[one(g, s, w, h) for g, s in sorted(games.items()) for w, h in SIZES])
            await browser.close()
            return [f for fs in out for f in fs], len(games)
    try:
        return asyncio.run(run())
    finally:
        proc.terminate()


# ------------------------------------------------------------------------------------------------ self-test
# Two games: one that docks only because its column makes room (its 1000px column), and one 720px game.
WIDE, NARROW = "i-dropped-my-ice-cream", "scale-factor-scaling"


def selftest():
    def scratch():
        d = pathlib.Path(tempfile.mkdtemp(prefix="calc-dock-"))
        shutil.copytree(BASE / "schools", d / "schools")
        (d / "scripts").mkdir()
        shutil.copy(BASE / "scripts" / "serve-stubbed.py", d / "scripts" / "serve-stubbed.py")
        (d / ".claude" / "rules").mkdir(parents=True)
        shutil.copy(BASE / CC.ROSTER, d / CC.ROSTER)
        for slug in (WIDE, NARROW):
            (d / "games" / slug).mkdir(parents=True)
            shutil.copy(BASE / "games" / slug / "index.html", d / "games" / slug / "index.html")
        return d

    def edit(path, old, new):
        s = path.read_bytes().decode("utf-8")
        assert s.count(old) == 1, "planted fault: %r is not in %s exactly once" % (old, path.name)
        path.write_bytes(s.replace(old, new).encode("utf-8"))

    cases = [
        ("clean copy passes", None, None),
        ("a dock element removed (%s)" % NARROW,
         lambda d: edit(d / "games" / NARROW / "index.html", "{dock:document.getElementById('qcard')}", "{}"),
         NARROW + " "),
        ("DOCK.colMin raised above %s's column" % WIDE,
         lambda d: edit(d / "schools" / "assets" / "calculator.js", "colMin: 640 }", "colMin: 5000 }"),
         WIDE + " "),
    ]
    bad = []
    for name, plant, want in cases:
        d = scratch()
        try:
            if plant:
                plant(d)
            got, _ = check(d, only={WIDE, NARROW}, workers=2)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = (not got) if want is None else bool(got) and all(f.startswith(want) for f in got)
        print("  %s  %-48s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(no failures)"))
        if not ok:
            bad.append(name)
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(cases)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--only", help="game slugs, comma separated")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    only = set(args.only.split(",")) if args.only else None
    fails, n = check(BASE, only=only, workers=args.workers)
    for f in fails:
        print("FAIL  " + f)
    if fails:
        print("\n%d problem(s) in %d calculator games at %s." % (len(fails), n, ", ".join("%dx%d" % s for s in SIZES)))
        return 1
    print("OK  %d calculator games dock beside their card at %s; opening never moves the card."
          % (n, ", ".join("%dx%d" % s for s in SIZES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
