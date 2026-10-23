"""Is the answer-count line (schools/assets/answer-count.js) on every page that has a mount, shown only as it should be,
and typed by hand nowhere?

Contract ANSWER-COUNTS (23 Oct 2026; canon 7.5.5). The line "N questions answered since September" fills the start
screen's mount (canon 7.5.4, `[data-maffs-start-note]`) from 1,000 and the homepage's (`[data-maffs-answer-total]`) from
10,000, from /schools/assets/answer-counts.json and the counts script's live address. A figure on a page is a claim, so:

  static    every page with a mount loads answer-count.js exactly once, after analytics.js and deferred, and no page
            without one loads it; the homepage has exactly one total mount; the committed data file is valid; the live
            address in the loader is the one the daily job fetches; and NO page carries a hand-typed "N questions
            answered" figure (the only source is the generated file).
            Only the homepage may call the counts script's live address (Jon, 23 Oct 2026: both Apps Scripts run as him and
            share one concurrent-execution limit, so a class opening games together must not be able to crowd out event
            logging): the address appears in no page and no script but the loader.
  browser   with the data file stubbed to a large figure for the page, no game page requests the live address, and every game's line reads "12,345 questions
            answered since September" on its start screen, visible, inside the viewport at 320 px, adding no sideways
            scroll, at 4.5:1 contrast, and not squeezed into a flex row or grid; the homepage line likewise.

    python scripts/check-answer-count.py              # static + Chromium
    python scripts/check-answer-count.py --static     # the static half only (no browser)
    python scripts/check-answer-count.py --selftest   # the loader's cases, and each planted fault must fail
"""
import argparse, asyncio, datetime as dt, importlib.util, json, os, pathlib, re, shutil, socket, subprocess, sys, tempfile, time
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent.parent
HERE = os.path.dirname(os.path.abspath(__file__))
LOADER = "schools/assets/answer-count.js"
INC = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/answer-count\.js"[^>]*>', re.I)
ANALYTICS = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/analytics\.js"', re.I)
GAME_MOUNT = "data-maffs-start-note"
TOTAL_MOUNT = "data-maffs-answer-total"
HAND = re.compile(r"\d[\d,]*\+?\s+(?:maths\s+)?questions\s+(?:have\s+been\s+)?answered", re.I)
SINCE = re.compile(r"questions answered since September", re.I)
# Not scanned for a hand-typed figure: the loader and the generated file themselves, and everything unpublished.
SKIP_DIRS = {"docs", "scripts", ".claude", ".github", ".git", "node_modules", "spec-map-source"}
SKIP_FILES = {LOADER, "schools/assets/answer-counts.json"}


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def games(root):
    return sorted(p.parent.name for p in (root / "games").glob("*/index.html") if not (p.parent / "_withdrawn.html").exists())


def check_static(root, slugs=None):
    fails = []
    for slug in (games(root) if slugs is None else slugs):
        text = (root / "games" / slug / "index.html").read_text(encoding="utf-8")
        has_mount, n = GAME_MOUNT in text, len(INC.findall(text))
        if has_mount and n != 1:
            fails.append("games/%s: has a start-note mount but loads answer-count.js %d times, want exactly once" % (slug, n))
        elif not has_mount and n:
            fails.append("games/%s: loads answer-count.js but has no start-note mount" % slug)
        if has_mount and n == 1:
            tag = INC.search(text)
            a = ANALYTICS.search(text)
            if "defer" not in tag.group(0):
                fails.append("games/%s: answer-count.js must be loaded with defer" % slug)
            if a and a.start() > tag.start():
                fails.append("games/%s: answer-count.js is loaded before analytics.js" % slug)
    home = (root / "index.html").read_text(encoding="utf-8")
    if len(INC.findall(home)) != 1:
        fails.append("index.html: loads answer-count.js %d times, want exactly once" % len(INC.findall(home)))
    if home.count(TOTAL_MOUNT) != 1:
        fails.append("index.html: %d answer-total mounts, want exactly 1" % home.count(TOTAL_MOUNT))
    loader = (root / LOADER).read_text(encoding="utf-8")
    f = _load("fetch_counts", "fetch-answer-counts.py")
    endpoint_id = f.ENDPOINT.split("/macros/s/")[1].split("/")[0][:12]
    if f.ENDPOINT not in loader:
        fails.append("%s: the live address is not the one scripts/fetch-answer-counts.py fetches" % LOADER)
    data = root / "schools" / "assets" / "answer-counts.json"
    if slugs is None:
        try:
            for x in f.validate(json.loads(data.read_text(encoding="utf-8")), f.slugs(root), require_today=False):
                fails.append("schools/assets/answer-counts.json: " + x)
        except Exception as exc:
            fails.append("schools/assets/answer-counts.json: %s" % exc)
    # no figure typed by hand, anywhere a visitor can read it
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if not p.is_file() or p.suffix.lower() not in (".html", ".js", ".json", ".xml", ".md", ".txt", ".css"):
            continue
        if set(rel.split("/")[:-1]) & SKIP_DIRS or rel in SKIP_FILES:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if rel != LOADER and endpoint_id in text:
            fails.append("%s: calls the counts script's live address; only the homepage, through %s, may" % (rel, LOADER))
        for m in HAND.finditer(text):
            fails.append("%s: a hand-typed figure %r (the count comes only from schools/assets/answer-counts.json)" % (rel, m.group(0)))
            break
    return fails


# ------------------------------------------------------------------------------------------------ browser
def _serve(root):
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


# The line's state on the page as loaded: its text, whether it can be seen, whether it is inside the viewport, the
# page's sideways overflow, its contrast against the first opaque background behind it, and its parent's layout.
PROBE = r"""(sel) => {
  const p = document.querySelector(sel);
  if (!p) return null;
  const r = p.getBoundingClientRect();
  const rgb = s => { const v = (s.match(/rgba?\(([^)]+)\)/) || [0, ''])[1].split(/[ ,\/]+/).filter(Boolean).map(Number);
    return v.length < 3 ? null : {r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1}; };
  const layers = [];
  for (let e = p; e; e = e.parentElement) {
    const b = rgb(getComputedStyle(e).backgroundColor);
    if (b && b.a > 0) { layers.push(b); if (b.a >= 0.99) break; }
  }
  let bg = {r: 255, g: 255, b: 255};
  for (let i = layers.length - 1; i >= 0; i--) {
    const L = layers[i];
    bg = {r: L.r * L.a + bg.r * (1 - L.a), g: L.g * L.a + bg.g * (1 - L.a), b: L.b * L.a + bg.b * (1 - L.a)};
  }
  const c = rgb(getComputedStyle(p).color);
  const fg = {r: c.r * c.a + bg.r * (1 - c.a), g: c.g * c.a + bg.g * (1 - c.a), b: c.b * c.a + bg.b * (1 - c.a)};
  const lum = x => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(x.r) + 0.7152 * f(x.g) + 0.0722 * f(x.b); };
  const l1 = lum(fg), l2 = lum(bg), q = p.parentElement, pc = getComputedStyle(q);
  return {text: p.textContent, count: p.getAttribute('data-maffs-count'), shown: p.checkVisibility() && r.width > 0 && r.height > 0,
          inside: r.left >= -0.5 && r.right <= document.documentElement.clientWidth + 0.5,
          sw: document.scrollingElement.scrollWidth, vw: document.documentElement.clientWidth,
          ratio: (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05),
          row: (/flex/.test(pc.display) && pc.flexDirection.startsWith('row')) || /grid/.test(pc.display),
          parent: (q.id ? '#' + q.id : '') + (q.className ? '.' + String(q.className).split(' ')[0] : q.id ? '' : q.tagName.toLowerCase())};
}"""


def _fixture(slug, big):
    now = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    return json.dumps({"as_of": now, "since": "2026-09-01", "total": 99999 if big else 0,
                       "games": {slug: 12345} if big and slug else {}})


async def _page(browser, base, rel, slug, sel, big):
    ctx = await browser.new_context(viewport={"width": 320, "height": 640})
    page = await ctx.new_page()
    live_calls = []

    async def watch(route):
        live_calls.append(route.request.url)
        await route.abort()
    await page.route("**/script.google.com/macros/s/AKfycbxvtM7Y**", watch)

    async def stub(route):
        await route.fulfill(status=200, content_type="application/json", body=_fixture(slug, big))
    await page.route("**/schools/assets/answer-counts.json*", stub)
    try:
        await page.goto(base + rel, wait_until="domcontentloaded")
        for _ in range(40):                         # the loader runs after parse; wait for it, up to 4 s
            got = await page.evaluate(PROBE, sel)
            if got and (got["text"] or not big):
                await page.wait_for_timeout(300)        # a live request, if the page makes one, is made by now
                got["live_calls"] = len(live_calls)
                return got
            await page.wait_for_timeout(100)
        got = await page.evaluate(PROBE, sel)
        if got:
            got["live_calls"] = len(live_calls)
        return got
    finally:
        await ctx.close()


async def _check_one(browser, base, rel, slug, sel, want):
    where = rel
    try:
        got = await _page(browser, base, rel, slug, sel, True)
        if got is None:
            return ["%s: no mount found" % where]
        f = []
        if got.get("live_calls") and "/games/" in rel:
            return ["%s: the page requested the counts script's live address (game pages show the daily file only)" % where]
        if got["text"] != want:
            return ["%s: the line reads %r, want %r" % (where, got["text"], want)]
        if not got["shown"]:
            f.append("%s: the line is not visible on the page as loaded" % where)
        if not got["inside"]:
            f.append("%s: the line runs outside the 320 px viewport" % where)
        if got["ratio"] < 4.5:
            f.append("%s: the line's contrast is %.2f:1 against the background behind it (want 4.5:1)" % (where, got["ratio"]))
        if got["row"]:
            f.append("%s: the line sits inside %s, a flex row or grid, so it is squeezed in beside the controls" % (where, got["parent"]))
        if got["sw"] > got["vw"]:
            base_line = await _page(browser, base, rel, slug, sel, False)
            if base_line and got["sw"] > base_line["sw"]:
                f.append("%s: the line widens the page to %d px (it was %d px without it)" % (where, got["sw"], base_line["sw"]))
        return f
    except Exception as exc:
        return ["%s: %s" % (where, str(exc).splitlines()[0][:160])]


def check_browser(root, slugs=None, home=True, workers=4):
    from playwright.async_api import async_playwright
    slugs = [s for s in (games(root) if slugs is None else slugs)
             if GAME_MOUNT in (root / "games" / s / "index.html").read_text(encoding="utf-8")]
    proc, base = _serve(root)

    async def run():
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)

            async def lim(coro):
                async with sem:
                    return await coro
            jobs = [lim(_check_one(browser, base, "/games/%s/" % s, s, "[%s]" % GAME_MOUNT, "12,345 questions answered since September"))
                    for s in slugs]
            if home:
                jobs.append(lim(_check_one(browser, base, "/", "", "[%s]" % TOTAL_MOUNT, "99,999 questions answered since September")))
            out = await asyncio.gather(*jobs)
            await browser.close()
            return [x for fs in out for x in fs], len(jobs)
    try:
        return asyncio.run(run())
    finally:
        proc.terminate()


# ------------------------------------------------------------------------------------------------ loader self-test
LOADER_CASES = r"""
async ([src]) => {
  const out = [];
  const ok = (name, cond, detail) => out.push([name, !!cond, cond ? '' : String(detail === undefined ? '' : detail)]);
  const NOW = Date.parse('2026-10-23T12:00:00+01:00');
  const day = 24 * 3600 * 1000;
  const iso = ms => new Date(ms).toISOString();
  const file = (asOfMs, total, games) => ({ as_of: iso(asOfMs), since: '2026-09-01', total, games });

  // The loader file, run on a page of its own with no mount (its own start-up finds nothing and does nothing).
  const holder = document.createElement('iframe');
  document.body.appendChild(holder);
  const win = holder.contentWindow;
  win.eval(src);
  const A = win.MaffsAnswerCount;

  async function page(mountHtml, o) {
    const doc = holder.contentDocument;
    const old = doc.getElementById('maffsAnswerCountStyle'); if (old) old.remove();
    doc.body.innerHTML = mountHtml;
    const frames = [];
    const calls = [];
    const opts = Object.assign({
      doc, slug: 'x', now: () => NOW, live: true, reduced: false,
      raf: f => frames.push(f), visible: () => true, setInterval: (f, ms) => { opts.timer = f; opts.every = ms; },
      get: url => { calls.push(url); return Promise.reject(new Error('not served')); },
    }, o);
    if (o && o.sources) {
      opts.get = url => { calls.push(url); const s = url.indexOf('/exec') >= 0 ? o.sources.live : o.sources.file;
        return s === undefined ? Promise.reject(new Error('down')) : Promise.resolve(s); };
    }
    await A.run(opts);
    const m = doc.querySelector('[data-maffs-start-note],[data-maffs-answer-total]');
    return { doc, m, frames, calls, opts, text: () => (m ? m.textContent : null) };
  }
  const G = '<div data-maffs-start-note></div>';
  const T = '<div data-maffs-answer-total hidden></div>';
  const fresh = (n, slug = 'x') => file(NOW - 3600000, n, { [slug]: n });

  let r = await page(G, { sources: { file: fresh(999) } });
  ok('below the threshold: 999 shows nothing', r.text() === '', r.text());
  r = await page(G, { sources: { file: fresh(1000) } });
  ok('at the threshold: 1,000 shows the line', r.text() === '1,000 questions answered since September', r.text());
  r = await page(G, { sources: { file: fresh(4312) } });
  ok('thousands separators: 4,312', r.text() === '4,312 questions answered since September', r.text());
  r = await page(G, { sources: { file: file(NOW - 8 * day, 5000, { x: 5000 }) } });
  ok('stale (8 days): hidden', r.text() === '', r.text());
  r = await page(G, { sources: { file: file(NOW - 6 * day, 5000, { x: 5000 }) } });
  ok('not yet stale (6 days): shown', r.text() === '5,000 questions answered since September', r.text());
  r = await page(G, { sources: { file: file(NOW - 8 * day, 5000, { x: 5000 }), live: file(NOW - 8 * day, 6000, { x: 6000 }) } });
  ok('both sources stale: hidden', r.text() === '', r.text());
  // a GAME page shows the daily file only: a fresh live figure is never asked for (cases for the live address are the homepage's)
  r = await page(G, { sources: { file: file(NOW - 8 * day, 5000, { x: 5000 }), live: fresh(6000) } });
  ok('game page, stale file: hidden (the live address is not consulted)', r.text() === '' && r.calls.length === 1, r.text() + ' calls=' + r.calls.length);
  r = await page(G, { sources: { file: fresh(2000), live: fresh(2600) } });
  ok('game page: the live figure is ignored, the file figure stays', r.text() === '2,000 questions answered since September' && r.frames.length === 0, r.text());

  // homepage: live higher counts up from the file's figure, never down, ends exactly on the live figure
  const fileT = (n, asOf = NOW - 3600000) => file(asOf, n, {});
  r = await page(T, { sources: { file: fileT(20000), live: fileT(26000, NOW - 1000) } });
  ok('homepage, live higher: starts the animation from the file figure', r.text() === '20,000 questions answered since September' && r.frames.length === 1, r.text() + ' frames=' + r.frames.length);
  const seen = [];
  let guard = 0, t = 0;
  while (r.frames.length && guard++ < 50) { const f = r.frames.shift(); f(t); seen.push(Number(r.m.getAttribute('data-maffs-count'))); t += 150; }
  ok('homepage, live higher: it counts up, in order, and ends on the live figure',
     seen[seen.length - 1] === 26000 && seen.every((v, i) => i === 0 || v >= seen[i - 1]) && seen.some(v => v > 20000 && v < 26000), seen.join(','));
  r = await page(T, { sources: { file: fileT(20000), live: fileT(26000, NOW - 1000) }, reduced: true });
  ok('homepage, reduced motion: jumps straight to the live figure, no animation frames', r.text() === '26,000 questions answered since September' && r.frames.length === 0, r.text() + ' frames=' + r.frames.length);
  r = await page(T, { sources: { file: fileT(20000), live: fileT(15000, NOW - 1000) } });
  ok('homepage, live lower: ignored (never counts down)', r.text() === '20,000 questions answered since September' && r.frames.length === 0, r.text());
  r = await page(T, { sources: { file: fileT(20000), live: fileT(20000, NOW - 1000) } });
  ok('homepage, live equal: nothing changes', r.text() === '20,000 questions answered since September' && r.frames.length === 0);
  r = await page(T, { sources: { file: fileT(5000), live: fileT(12000, NOW - 1000) } });
  ok('homepage, file below / live over the threshold: shows (no animation from nothing)', r.text() === '12,000 questions answered since September' && r.frames.length === 0, r.text());
  r = await page(T, { sources: { file: fileT(30000, NOW - 8 * day), live: fileT(31000, NOW - 1000) } });
  ok('homepage, stale file / fresh live: the live figure shows', r.text() === '31,000 questions answered since September', r.text());
  r = await page(T, { sources: { file: fileT(30000, NOW - 8 * day), live: fileT(31000, NOW - 8 * day) } });
  ok('homepage, both sources stale: hidden', r.text() === '', r.text());

  // missing / broken sources
  r = await page(G, { sources: {} });
  ok('missing: neither source loads, nothing shown', r.text() === '', r.text());
  r = await page(G, { sources: { file: fresh(3000) } });
  ok('live down: the file figure stays', r.text() === '3,000 questions answered since September');
  r = await page(G, { sources: { file: { as_of: 'soon', total: 5, games: {} } } });
  ok('as_of unreadable: hidden', r.text() === '');
  r = await page(G, { sources: { file: { as_of: iso(NOW), total: 5, games: { x: '3000' } } } });
  ok('count not a number: hidden', r.text() === '');
  r = await page(G, { sources: { file: { as_of: null, total: 5000, games: { x: 5000 } } } });
  ok('as_of null (the first count unfinished): hidden', r.text() === '');
  r = await page(G, { sources: { file: fresh(5000, 'y') } });
  ok("another game's count is not this game's: hidden", r.text() === '', r.text());
  r = await page(G, { sources: { file: fresh(5000) }, live: false });
  ok('off the live host: the live address is never called', r.calls.length === 1 && r.calls[0].indexOf('/schools/assets/answer-counts.json') === 0, r.calls.join(' '));
  r = await page(G, { get: () => { throw new Error('boom'); } });
  ok('a get that throws: hidden, no error escapes', r.text() === '');

  // no mount
  r = await page('<p>no start screen here</p>', { sources: { file: fresh(5000) } });
  ok('no mount: nothing shown and no error', r.calls.length === 0 && !r.doc.getElementById('maffsAnswerCountStyle') && r.doc.body.textContent.indexOf('questions answered') < 0, r.calls.join(' '));

  // a game page never calls the live address (both Apps Scripts share Jon's concurrent-execution limit)
  r = await page(G, { sources: { file: fresh(2000), live: fresh(2600) } });
  ok('game page: no request to the live address, even on the live host', r.calls.length === 1 && r.calls[0].indexOf('/exec') < 0 && r.text() === '2,000 questions answered since September', r.calls.join(' '));

  // the homepage total
  r = await page(T, { sources: { file: file(NOW - 3600000, 9999, {}) } });
  ok('homepage: 9,999 shows nothing and stays hidden', r.text() === '' && r.m.hidden === true, r.text());
  r = await page(T, { sources: { file: file(NOW - 3600000, 10000, {}) } });
  ok('homepage: 10,000 shows the total, unhidden', r.text() === '10,000 questions answered since September' && r.m.hidden === false, r.text());
  r = await page(T, { sources: { file: file(NOW - 3600000, 68412, {}) } });
  ok('homepage: 68,412', r.text() === '68,412 questions answered since September', r.text());
  let liveTotal = file(NOW - 1000, 70000, {});
  const sources = { file: file(NOW - 3600000, 68412, {}), live: liveTotal };
  r = await page(T, { sources });
  const before = r.calls.length;
  ok('homepage: refetches every 60 s', r.opts.every === 60000 && typeof r.opts.timer === 'function', r.opts.every);
  sources.live = file(NOW - 500, 70500, {});
  r.opts.timer();
  await new Promise(res => setTimeout(res, 20));
  ok('homepage: a tick fetches the live figure again', r.calls.length === before + 1, r.calls.length);
  r.opts.visible = () => false;
  r.opts.timer();
  await new Promise(res => setTimeout(res, 20));
  ok('homepage: a hidden tab does not fetch', r.calls.length === before + 1, r.calls.length);

  // one live fetch on load, then at most 10 minutes of refreshing
  let clock = NOW, cleared = 0;
  const src3 = { file: file(NOW - 3600000, 68412, {}), live: file(NOW - 500, 70000, {}) };
  r = await page(T, { sources: src3, now: () => clock, clearInterval: () => { cleared++; } });
  const lives = () => r.calls.filter(u => u.indexOf('/exec') >= 0).length;
  ok('homepage: one live fetch on load', lives() === 1, lives());
  for (let i = 0; i < 9; i++) { clock += 60000; r.opts.timer(); await new Promise(res => setTimeout(res, 5)); }
  ok('homepage: refreshes every minute for the first 9 minutes', lives() === 10 && cleared === 0, lives() + ' cleared=' + cleared);
  for (let i = 0; i < 5; i++) { clock += 60000; r.opts.timer(); await new Promise(res => setTimeout(res, 5)); }
  ok('homepage: stops refreshing after 10 minutes on the page', lives() === 10 && cleared >= 1, lives() + ' cleared=' + cleared);
  return out;
}
"""


async def _loader_cases(src=None):
    from playwright.async_api import async_playwright
    src = (BASE / LOADER).read_text(encoding="utf-8") if src is None else src
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.set_content("<!doctype html><body></body>")
        got = await page.evaluate(LOADER_CASES, [src])
        await browser.close()
    return [tuple(g) for g in got]


def selftest():
    bad = []
    results = asyncio.run(_loader_cases())
    for name, ok, detail in results:
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  <- " + detail))
        if not ok:
            bad.append(name)
    # planted faults in the loader itself: each must be caught by a named case
    loader = (BASE / LOADER).read_text(encoding="utf-8")
    for name, a, b, want in (
            ("a homepage that refreshes for ever", "if (now() - t0 >= POLL_MAX_MS) {", "if (false) {", "stops refreshing after 10 minutes"),
            ("a game page that calls the live address", "var useLive = opts.live && totals.length > 0;", "var useLive = opts.live;", "no request to the live address")):
        assert a in loader, a
        got = [r for r in asyncio.run(_loader_cases(loader.replace(a, b, 1))) if not r[1]]
        ok = any(want in r[0] for r in got)
        print("  %s  planted: %-40s %s" % ("PASS" if ok else "FAIL", name, got[0][0] if got else "(no case failed)"))
        if not ok:
            bad.append(name)
    # planted faults in the static half
    slug, other = "better-value", "angle-ace"

    def scratch():
        d = pathlib.Path(tempfile.mkdtemp(prefix="answer-count-"))
        for rel in ("schools",):
            shutil.copytree(BASE / rel, d / rel)
        (d / "scripts").mkdir()
        for f in ("fetch-answer-counts.py", "serve-stubbed.py"):
            shutil.copy(BASE / "scripts" / f, d / "scripts" / f)
        for s in (slug, other):
            (d / "games" / s).mkdir(parents=True)
            shutil.copy(BASE / "games" / s / "index.html", d / "games" / s / "index.html")
        for s in sorted(p.name for p in (BASE / "games").iterdir() if p.is_dir()):   # the roster the data file is judged against
            (d / "games" / s).mkdir(exist_ok=True)
        for r in sorted(p.name for p in (BASE / "escape-rooms").iterdir() if p.is_dir() and (p / "room.js").exists()):
            (d / "escape-rooms" / r).mkdir(parents=True, exist_ok=True)
            (d / "escape-rooms" / r / "room.js").write_text("", encoding="utf-8", newline="")
        shutil.copy(BASE / "index.html", d / "index.html")
        return d

    def edit(d, rel, fn):
        p = d / rel
        s = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
        t = fn(s)
        assert t != s, "planted fault changed nothing in " + rel
        p.write_bytes(t.encode("utf-8"))

    inc = lambda s: INC.search(s).group(0)
    cases = [
        ("clean copy passes", None, None),
        ("a page with a mount but no include", lambda d: edit(d, "games/%s/index.html" % slug, lambda s: s.replace(inc(s), "")), "loads answer-count.js 0 times"),
        ("a page loading it twice", lambda d: edit(d, "games/%s/index.html" % slug, lambda s: s.replace(inc(s), inc(s) + "\n" + inc(s))), "2 times"),
        ("a page loading it without a mount", lambda d: edit(d, "games/%s/index.html" % slug,
            lambda s: s.replace('<div class="maffs-start-note" data-maffs-start-note></div>', "")), "no start-note mount"),
        ("include not deferred", lambda d: edit(d, "games/%s/index.html" % slug, lambda s: s.replace(" defer></script>", "></script>", 1) if "answer-count.js\" defer" in s else s), "defer"),
        ("a hand-typed figure on a game page", lambda d: edit(d, "games/%s/index.html" % slug,
            lambda s: s.replace("</body>", "<p>12,000 questions answered</p></body>", 1)), "hand-typed figure"),
        ("a hand-typed figure on the homepage", lambda d: edit(d, "index.html",
            lambda s: s.replace("</body>", "<p>Over 50,000 questions answered so far</p></body>", 1)), "hand-typed figure"),
        ("the homepage mount removed", lambda d: edit(d, "index.html", lambda s: s.replace(" data-maffs-answer-total", "", 1)), "answer-total mounts"),
        ("a data file with a total that is not the sum", lambda d: edit(d, "schools/assets/answer-counts.json",
            lambda s: re.sub(r'"total": \d+', '"total": 1', s, count=1)), "not the sum"),
        ("a game page that names the live address", lambda d: edit(d, "games/%s/index.html" % slug, lambda s: s.replace(
            "</body>", "<script>var u='%s'</script></body>" % _load("fetch_counts", "fetch-answer-counts.py").ENDPOINT, 1)),
         "live address; only the homepage"),
        ("the loader's live address changed", lambda d: edit(d, LOADER, lambda s: s.replace("AKfycbxvtM7Y", "AKfycbxXXXXX", 1)), "live address"),
    ]
    # a game page that calls the live address by its own code: caught in Chromium, not only in the source scan
    d = scratch()
    try:
        f = _load("fetch_counts", "fetch-answer-counts.py")
        edit(d, "games/%s/index.html" % slug, lambda s: s.replace(
            "</body>", "<script>var q=new XMLHttpRequest();q.open('GET','%s');q.send()</script></body>" % f.ENDPOINT, 1))
        got, _ = check_browser(d, slugs=[slug], home=False)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    ok = any("live address" in g for g in got)
    print("  %s  planted: %-40s %s" % ("PASS" if ok else "FAIL", "a game page that fetches the live address",
                                       got[0][:110] if got else "(no failures)"))
    if not ok:
        bad.append("game page fetches live address (browser)")
    for name, plant, want in cases:
        d = scratch()
        try:
            if plant:
                plant(d)
            got = check_static(d, slugs=[slug, other]) + (
                check_static_data(d) if name.startswith("a data file") else [])
        finally:
            shutil.rmtree(d, ignore_errors=True)
        ok = (not got) if want is None else any(want in g for g in got)
        print("  %s  %-48s %s" % ("PASS" if ok else "FAIL", name, got[0][:110] if got else "(no failures)"))
        if not ok:
            bad.append(name)
    print("selftest: %s (%d loader cases, %d planted faults)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(results), len(cases) + 3))
    return 1 if bad else 0


def check_static_data(root):
    f = _load("fetch_counts", "fetch-answer-counts.py")
    try:
        return ["schools/assets/answer-counts.json: " + x for x in f.validate(json.loads((root / "schools" / "assets" / "answer-counts.json").read_text(encoding="utf-8")),
                                                                    f.slugs(root), require_today=False)]
    except Exception as exc:
        return ["schools/assets/answer-counts.json: %s" % exc]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--static", action="store_true", help="skip the Chromium half")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    fails = check_static(BASE)
    played = 0
    if not a.static:
        bf, played = check_browser(BASE)
        fails += bf
    for f in fails:
        print("FAIL", f)
    print("answer count: %s (%d pages with a mount%s)" % (
        "FAIL" if fails else "PASS", played or sum(1 for g in games(BASE) if GAME_MOUNT in (BASE / "games" / g / "index.html").read_text(encoding="utf-8")) + 1,
        "; each loaded at 320 px with the line shown" if played else "; Chromium half skipped"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
