"""Does every game carry the one standard start-screen mount, in its start screen, and only there?

Canon 7.5.4. Site-wide start-screen notes (the first: the answer counts) mount on `<div class="maffs-start-note"
data-maffs-start-note></div>`, so no feature needs per-game code or a loader that guesses ids. Every live game
(games/<slug>/index.html; a directory holding `_withdrawn.html` is a holding page and is skipped) must be in exactly
one of:

  CONTAINERS   the game has a start screen. The page carries exactly one mount, last inside the recorded container
               (the element shown before play and hidden during play; the container each game uses is recorded
               here). In Chromium, one question deep: the mount is inside that container and visible before Start,
               and not visible once the game has started.
  NO_START     the game opens straight into play (reason recorded); it carries no mount.

    python scripts/check-start-mount.py               # static + Chromium
    python scripts/check-start-mount.py --static      # the static half only (no browser)
    python scripts/check-start-mount.py --selftest    # each planted fault must fail; the clean copy passes
"""
import argparse, asyncio, importlib.util, os, pathlib, re, shutil, socket, subprocess, sys, tempfile, time
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent.parent
HERE = os.path.dirname(os.path.abspath(__file__))
MOUNT = '<div class="maffs-start-note" data-maffs-start-note></div>'
MARK = "data-maffs-start-note"

# slug -> selector of the start container the mount sits last inside. Shown before play, hidden once play begins.
CONTAINERS = {
    "angle-ace": "#menu", "bearing-blitz": "#menu", "better-value": "#startScreen",
    "binomial-blaster": "#menu", "boolean-blitz": "#startScreen", "characteristic-quest": "#menu",
    "chart-interrogator": "#selector", "circle-theorem-spotter": "#menu", "complex-converter": "#menuScreen",
    "component-crusher": "#menuScreen", "constructions-lab": "#menu", "coordinate-geometry-dash": "#menu",
    "core-maths-paper1": "#startScreen", "core-maths-paper2a": "#startScreen",
    "core-maths-paper2b": "#startScreen", "core-maths-paper2c": "#startScreen",
    "correlation-or-coincidence": "#menu", "curling-friction": "#menu", "decimal-detective": "#startScreen",
    "differentiation-duel": "#startScreen", "dimension-checker": "#menu", "distinctly-average": "#startScreen",
    "eigenvalue-extractor": "#menu", "eigenvector-engine": "#menu", "equation-builder": "#startScreen",
    "estimation-engine": "#menu", "expectation-station": "#startScreen", "expected-damage": "#startScreen",
    "factor-race": "#startScreen", "fermi-lab": "#startScreen", "force-resolver": "#menu",
    "formula-forge": "#menu", "formula-plug-in": "#startScreen", "formula-unlocked": "#menu",
    "four-quadrant-explorer": "#startScreen", "fraction-equivalence": "#startScreen",
    "free-daily-pizza": "#menu", "given-that": "#startScreen", "glorious-gantt": "#menuScreen",
    "gradient-hunter": "#menuScreen", "graph-sketcher": "#menuScreen", "graph-transformer": "#menu",
    "growth-and-decay": "#menuScreen", "higher-power": "#menu", "how-many-parts": "#menu",
    "index-laws": "#startScreen", "integration-duel": "#startScreen", "just-pythag-it-bruv": "#menu",
    "like-terms-collector": "#startScreen", "linear-equation-solver": "#menu", "log-laws": "#startScreen",
    "maths-court": "#startScreen", "matrix-crunch": "#menu", "modular-battle": "#startScreen",
    "moments-master": "#menu", "negative-number-line": "#startScreen", "new-shapes": "#startScreen",
    "normal-navigator": "#menu", "partial-fractions-duel": "#menu", "percentage-flip": "#startScreen",
    "prime-factorisation": "#startScreen", "prime-or-composite": "#intro-box", "prisoners-dilemma": "#menu",
    "probability-paradox": "#menu", "probability-pioneer": "#startScreen", "proof-builder": "#menu",
    "proportion-blaster": "#menu", "quadratic-factoriser": "#startScreen", "scale-factor-scaling": "#menu",
    "screening-room": "#startScreen", "sequence-solver": "#menu", "seven-bridges": "#startScreen",
    "shape-shifter": "#startScreen", "simultaneous-solver": "#menu", "six-sevens-bruv": "#menu",
    "split-it": "#menuScreen", "spot-the-error": "#startScreen", "spot-the-muppet": "#startScreen",
    "standard-form-blitz": "#menu", "stat-attack": "#menuScreen", "surd-simplifier": "#menu",
    "suvat": "#startScreen", "take-a-walk": "#menu", "tax-theft": "#diffScreen",
    "terrible-advice": "#startScreen", "test-the-claim": "#menuScreen", "the-perfect-prank": "#scrBrief",
    "think-of-a-number": "#startScreen", "trig-identity-duel": "#menu", "trig-wars": ".briefing",
    "trig-worms": "#startScreen", "truth-buster": "#startScreen", "truth-will-set-you-free": "#startScreen",
    "unit-converter": "#menu", "word-problem-decoder": "#startScreen", "wrong-on-the-internet": "#startScreen",
}

NO_START = {
    "52dle": "one puzzle, open at load: the first guess starts the game",
    "equatle": "one puzzle, open at load: the first guess starts the game",
    "estimation-golf": "calls startGame() at load; the level bar stays on screen during play",
    "factor-theorem": "opens on a Learn / Practice / Test Yourself tab bar, with no start control",
}

# Games whose Start control the shared driver does not find (or whose game_started the page's mfg shim never sees):
# the controls a student presses to begin play, first match of each CSS selector in turn; (selector, text) types text.
START_STEPS = {
    "six-sevens-bruv": ["#newGridBtn", ("#iniInput", "ABC"), "#iniCreate", "#startBtn"],
    "test-the-claim": [".mode-btn", "#tailPills .pill", "#sigPills .pill", "#startBtn"],
    "trig-worms": ["#startScreen .btn-primary"],
}


def live_games(root):
    return sorted(p.parent.name for p in (root / "games").glob("*/index.html") if not (p.parent / "_withdrawn.html").exists())


def check_static(root, games=None):
    fails = []
    every = games is None
    games = live_games(root) if every else games
    for slug in games:
        text = (root / "games" / slug / "index.html").read_text(encoding="utf-8")
        n = text.count(MARK)
        if slug in CONTAINERS and slug in NO_START:
            fails.append("%s: in both CONTAINERS and NO_START" % slug)
        elif slug in CONTAINERS:
            if n != 1:
                fails.append("%s: %d start-note mounts, want exactly 1" % (slug, n))
            elif MOUNT not in text:
                fails.append("%s: the mount is not exactly %s" % (slug, MOUNT))
        elif slug in NO_START:
            if n:
                fails.append("%s: recorded as having no start screen but carries %d mount(s)" % (slug, n))
        else:
            fails.append("%s: a live game in neither CONTAINERS nor NO_START (add the mount to its start screen)" % slug)
    for slug in sorted(set(CONTAINERS) | set(NO_START)) if every else ():
        if slug not in games:
            fails.append("%s: recorded here but is not a live game" % slug)
    return fails


def _serve(root):
    """serve-stubbed.py from `root` (analytics stubbed, so nothing is sent); returns (proc, base)."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    proc = subprocess.Popen([sys.executable, str(root / "scripts" / "serve-stubbed.py"), str(port)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=str(root))
    base = "http://127.0.0.1:%d" % port
    for _ in range(150):
        try:
            urllib.request.urlopen(base + "/schools/assets/analytics.js", timeout=2).read()
            return proc, base
        except OSError:
            time.sleep(0.1)
    proc.terminate()
    raise RuntimeError("serve-stubbed.py did not answer on port %d" % port)


def _check_site():
    spec = importlib.util.spec_from_file_location("check_site", os.path.join(HERE, "check-site.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# One look at the mount: how many there are, whether the recorded container holds the one there is, and whether it
# is shown. checkVisibility() is false for display:none and visibility:hidden on the element or any ancestor; an
# empty block takes no height, so the test cannot depend on it having any.
PROBE = """((sel) => {
  const m = document.querySelectorAll('[data-maffs-start-note]');
  const e = m[0];
  return { n: m.length, inside: !!(e && e.closest(sel)), shown: !!(e && e.checkVisibility()),
           container: document.querySelectorAll(sel).length };
})"""


async def _game(cs, ctx, base, slug, timeout_ms):
    sel = CONTAINERS[slug]
    page = None
    try:
        page, rec = await cs.open_guarded_page(ctx, base, "games/%s/index.html" % slug, timeout_ms)

        async def ev(expr):
            return await asyncio.wait_for(page.evaluate(expr), timeout=timeout_ms / 1000.0)
        before = await ev(PROBE + "(%r)" % sel)
        if before["n"] != 1:
            return ["%s: %d mounts in the loaded page, want exactly 1" % (slug, before["n"])]
        if not before["container"]:
            return ["%s: the recorded container %s is not on the page" % (slug, sel)]
        if not before["inside"]:
            return ["%s: the mount is outside its start screen %s" % (slug, sel)]
        if not before["shown"]:
            return ["%s: the mount is not visible before Start" % slug]
        steps = []
        err0 = len(rec["errs"])
        if slug in START_STEPS:
            for step in START_STEPS[slug]:
                if isinstance(step, tuple):
                    await page.locator(step[0]).first.fill(step[1], timeout=timeout_ms)
                else:
                    await page.locator(step).first.click(timeout=timeout_ms)
        elif await ev("window.__mfgLevelControls().length"):
            steps = await ev("window.__mfgLevelPress(0)")
        else:
            steps = ["start"] if await ev("window.__mfgClickStart()") else []
        started = slug in START_STEPS or (await ev("window.__mfgStats()"))["started"]             or await cs.drive_to_start(page, ev, rec, steps, err0)
        if not started:
            return ["%s: could not begin play (steps %s) to see the mount hidden" % (slug, steps)]
        await page.wait_for_timeout(300)
        during = await ev(PROBE + "(%r)" % sel)
        if during["n"] == 1 and during["shown"]:
            return ["%s: the mount is still visible once play has begun" % slug]
        return []
    except Exception as exc:
        return ["%s: %s" % (slug, str(exc).splitlines()[0][:160])]
    finally:
        if page is not None:
            try:
                await page.close()
            except Exception:
                pass


def check_browser(root, games=None, workers=4, timeout_ms=20000):
    """Load each game, find the mount shown on its start screen, press Start, find it gone."""
    from playwright.async_api import async_playwright
    cs = _check_site()
    games = sorted(CONTAINERS) if games is None else games
    proc, base = _serve(root)

    async def run():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            ctxs = []
            for _ in range(workers):
                ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
                await ctx.add_init_script(cs.TIER3_INIT)
                await ctx.add_init_script(cs.LEVEL_INIT)
                ctxs.append(ctx)
            pool = asyncio.Queue()
            for c in ctxs:
                pool.put_nowait(c)

            async def one(slug):
                ctx = await pool.get()
                try:
                    return await _game(cs, ctx, base, slug, timeout_ms)
                finally:
                    pool.put_nowait(ctx)
            out = await asyncio.gather(*[one(g) for g in games])
            await browser.close()
            return [f for fs in out for f in fs]
    try:
        return asyncio.run(run())
    finally:
        proc.terminate()


# ------------------------------------------------------------------------------------------------ self-test
def selftest():
    g = "better-value"            # a #startScreen game with a plain Start button
    line = re.compile(r"^[ \t]*" + re.escape(MOUNT) + r"\n", re.M)

    def scratch():
        d = pathlib.Path(tempfile.mkdtemp(prefix="start-mount-"))
        shutil.copytree(BASE / "schools", d / "schools")
        (d / "scripts").mkdir()
        shutil.copy(BASE / "scripts" / "serve-stubbed.py", d / "scripts" / "serve-stubbed.py")
        for slug in (g,) + tuple(NO_START)[:1]:
            (d / "games" / slug).mkdir(parents=True)
            shutil.copy(BASE / "games" / slug / "index.html", d / "games" / slug / "index.html")
        return d

    def edit(d, fn, slug=g):
        p = d / "games" / slug / "index.html"
        s = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        t = fn(s)
        assert t != s, "planted fault changed nothing"
        p.write_bytes(t.encode("utf-8"))

    def drop(s):
        return line.sub("", s, count=1)

    def static(d):
        return check_static(d, games=[g, tuple(NO_START)[0]])

    def browser(d):
        return check_browser(d, games=[g], workers=1)

    def move_outside(s):
        return drop(s).replace("</body>", MOUNT + "\n</body>", 1)

    def keep_start_up(s):
        return s.replace("</head>", "<style>#startScreen{display:block !important}</style>\n</head>", 1)

    both = lambda d: static(d) + browser(d)
    cases = [
        ("clean copy passes", None, both, None),
        ("mount missing", lambda d: edit(d, drop), both, "0 start-note mounts"),
        ("second mount", lambda d: edit(d, lambda s: line.sub(lambda m: m.group(0) * 2, s, count=1)), both, "2 start-note mounts"),
        ("mount outside the start screen", lambda d: edit(d, move_outside), browser, "outside its start screen"),
        ("mount visible during play", lambda d: edit(d, keep_start_up), browser, "still visible once play has begun"),
        ("mount hidden before Start", lambda d: edit(d, lambda s: s.replace(MOUNT, MOUNT.replace(">", ' hidden>', 1), 1)),
         browser, "not visible before Start"),
        ("mount on a no-start game", lambda d: edit(d, lambda s: s.replace("</body>", MOUNT + "\n</body>", 1),
                                                    tuple(NO_START)[0]), static, "no start screen"),
        ("mount altered", lambda d: edit(d, lambda s: s.replace(MOUNT, MOUNT.replace('class="maffs-start-note"', 'class="start-note"'), 1)),
         static, "not exactly"),
    ]
    bad = []
    for name, plant, run, want in cases:
        d = scratch()
        try:
            if plant:
                plant(d)
            got = run(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = (not got) if want is None else any(want in f for f in got)
        print("  %s  %-34s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(no failures)"))
        if not ok:
            bad.append(name)
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(cases)))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--static", action="store_true", help="skip the Chromium half")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    fails = check_static(BASE)
    if not a.static:
        fails += check_browser(BASE)
    for f in fails:
        print("FAIL", f)
    print("start-note mount: %s (%d games with the mount, %d with no start screen%s)"
          % ("FAIL" if fails else "PASS", len(CONTAINERS), len(NO_START),
             "" if a.static else "; each played to its first question in Chromium"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
