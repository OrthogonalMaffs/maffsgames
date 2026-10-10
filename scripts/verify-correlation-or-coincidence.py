#!/usr/bin/env python3
# ci-line: Correlation or Coincidence (bank, graphs' r, labels before the answer, phone fit) |
"""Correlation or Coincidence: the bank, the graphs, the labels before the answer, and the phone fit.

    python scripts/verify-correlation-or-coincidence.py
    python scripts/verify-correlation-or-coincidence.py --no-selftest

Rebuilt 4 Oct 2026 (Jon's contract, from the resit correctness audit, PR #35): the old game hid both
variable names until after the student had answered, yet scored and ranked the guess (audit F1), and
held an unsafe pair. This verifier holds the rebuild to its contract:

  Bank        at least 40 items; every item's category is one of the three (cause / both / chance);
              the three roughly a third each (each within 2 of a third of the bank); a non-empty
              explanation for every item; the lurking variable named on every "both" item; a joke
              theory on every coincidence (and none elsewhere); unique ids; ranges the right way round.
  SR-14       no tier (a) word anywhere in an item and no tier (b) word (illness, injury) in its joke,
              by scripts/check-content-safety.py's word lists (canon §0.3).
  Graphs      every item's points recomputed into Pearson's r here (not by the page): the sign is the
              item's direction and |r| is inside the band its stated strength names; every point is
              inside the axis range; whole-number variables are whole.
  Sessions    300 seeded deals of 10: ten distinct items, at least 3 of each kind; a deal of the whole
              bank is the whole bank.
  Play        a full session of every item, played with real clicks (Firebase blocked): BEFORE each
              answer both variable names are on screen in the axis titles (visible, in the viewport,
              not transparent); exactly three answer buttons; after the answer, the
              explanation, the lurking variable ("both") or the joke (coincidence) and the Next control.
  Phone fit   every item at 320x568, 375x667 and 390x844 (canon §7.6.1): no sideways scroll; the three
              buttons above the fixed footer while asking; the feedback's Next above it after a wrong
              answer.

FAULT-INJECTION SELF-TEST (runs every time; --no-selftest skips it): each fault is patched into a fresh
page at run time (the file is never touched) and must make the checks above fail.
"""
import argparse, asyncio, importlib.util, math, os, sys
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402

SLUG = "correlation-or-coincidence"
PAGE = "/games/%s/" % SLUG
CATS = ("cause", "both", "chance")
BUTTONS = {"cause": "One causes the other", "both": "Something else causes both", "chance": "Coincidence"}
# The strength bands, stated here independently of the page.
BANDS = {"very strong": (0.94, 1.0), "strong": (0.80, 0.94), "moderate": (0.50, 0.80)}
MIN_BANK = 84
PHONES = [(320, 568), (375, 667), (390, 844)]
PORT = None
_FAILURES = []


def fail(msg):
    _FAILURES.append(msg)
    print("FAIL " + msg)


def safety_module():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check-content-safety.py")
    spec = importlib.util.spec_from_file_location("check_content_safety", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SAFETY = safety_module()


def pearson(pts):
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    syy = sum((p[1] - my) ** 2 for p in pts)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


# ---------------------------------------------------------------- the bank and its graphs
def check_bank(bank, points):
    out = []
    n = len(bank)
    if n < MIN_BANK:
        out.append("bank has %d items, the minimum is %d" % (n, MIN_BANK))
    ids = [q.get("id") for q in bank]
    if len(set(ids)) != n:
        out.append("item ids are not unique")
    counts = {c: 0 for c in CATS}
    for q in bank:
        qid = q.get("id", "?")
        cat = q.get("cat")
        if cat not in CATS:
            out.append("%s: category %r is not one of %s" % (qid, cat, ", ".join(CATS)))
        else:
            counts[cat] += 1
        if not str(q.get("explain") or "").strip():
            out.append("%s: no explanation" % qid)
        lurk, joke = str(q.get("lurk") or "").strip(), str(q.get("joke") or "").strip()
        if cat == "both" and not lurk:
            out.append("%s: a 'both' item with no lurking variable named" % qid)
        if cat == "chance" and not joke:
            out.append("%s: a coincidence with no joke theory" % qid)
        if cat != "chance" and joke:
            out.append("%s: a joke theory on a %r item (only coincidences get one)" % (qid, cat))
        for axis in ("x", "y"):
            a = q.get(axis) or []
            if len(a) != 4 or not str(a[0]).strip() or not a[1] < a[2]:
                out.append("%s: %s axis %r is not [name, low, high, whole]" % (qid, axis, a))
        if q.get("dir") not in (1, -1):
            out.append("%s: direction %r is not +1 or -1" % (qid, q.get("dir")))
        if q.get("str") not in BANDS:
            out.append("%s: strength %r is not one of %s" % (qid, q.get("str"), ", ".join(BANDS)))
        # SR-14: tier (a) anywhere in the item; tier (b) (illness, injury) also in its joke.
        text = " ".join(str(v) for v in (q.get("x", [""])[0], q.get("y", [""])[0], q.get("explain"), lurk))
        words = SAFETY.terms(text) + SAFETY.terms(joke, humour=True)
        if words:
            out.append("%s: SR-14 word(s) %s" % (qid, ", ".join(sorted(set(words)))))
        # The graph, recomputed here.
        pts = points.get(qid) or []
        if len(pts) != q.get("n") or len(pts) < 5:
            out.append("%s: %d points drawn, the item says %s" % (qid, len(pts), q.get("n")))
            continue
        if q.get("str") in BANDS and q.get("dir") in (1, -1):
            r = pearson(pts)
            lo, hi = BANDS[q["str"]]
            if (r > 0) != (q["dir"] > 0):
                out.append("%s: the graph's r is %.3f, the item says %s" % (qid, r, "positive" if q["dir"] > 0 else "negative"))
            elif not lo <= abs(r) <= hi:
                out.append("%s: |r| = %.3f is outside the %s band [%.2f, %.2f]" % (qid, abs(r), q["str"], lo, hi))
        for axis, k in (("x", 0), ("y", 1)):
            a = q.get(axis) or [None, 0, 0, 0]
            for p in pts:
                v = p[k]
                if not a[1] - 1e-9 <= v <= a[2] + 1e-9:
                    out.append("%s: a point's %s = %s is outside %s..%s" % (qid, axis, v, a[1], a[2]))
                    break
                if a[3] and v != round(v):
                    out.append("%s: %s is whole numbers, a point has %s" % (qid, axis, v))
                    break
    third = n / 3.0
    for c in CATS:
        if not math.floor(third) - 2 <= counts[c] <= math.ceil(third) + 2:
            out.append("category %r has %d of %d items; the plan is a third each (within 2)" % (c, counts[c], n))
    return out, counts


DEALS_JS = """() => {
  var out = [];
  for (var s = 1; s <= 300; s++) {
    var seed = s * 7919;
    var rand = function () { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
    out.push(COC.deal(10, rand).map(function (q) { return q.id + ':' + q.cat; }));
  }
  var all = COC.deal(COC.BANK.length).map(function (q) { return q.id; });
  return { deals: out, all: all };
}"""


def check_deals(data, bank):
    out = []
    for d in data["deals"]:
        ids = [x.split(":")[0] for x in d]
        cats = [x.split(":")[1] for x in d]
        if len(d) != 10 or len(set(ids)) != 10:
            out.append("a deal of 10 gave %d items, %d distinct" % (len(d), len(set(ids))))
            break
        if min(cats.count(c) for c in CATS) < 3:
            out.append("a deal of 10 has fewer than 3 of one kind: %s" % ", ".join(cats))
            break
    if sorted(data["all"]) != sorted(q["id"] for q in bank):
        out.append("a deal of the whole bank is not the whole bank")
    return out


# ---------------------------------------------------------------- the browser
async def new_page(browser, viewport=(1200, 900)):
    ctx = await browser.new_context(viewport={"width": viewport[0], "height": viewport[1]},
                                    has_touch=viewport[0] < 500)
    await bc.no_next_floor(ctx)
    await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)  # MaffsLock's 300 ms window: the sweep answers at once (F1 batch 7)

    async def route(r):
        if r.request.url.startswith("http://127.0.0.1:%d/" % PORT):
            await r.continue_()
        else:
            await r.abort()          # GA, Firebase SDK, fonts: nothing leaves the runner
    await ctx.route("**/*", route)
    await ctx.route(lambda u: bc.is_font_cdn(u), bc.serve_real_font_async)  # FONT-FIT: KaTeX and the text faces from scripts/fonts/, the fonts students see
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    await page.goto("http://127.0.0.1:%d%s" % (PORT, PAGE))
    await page.wait_for_function("window.COC && COC.BANK && COC.ui")
    return ctx, page, errors


LABELS_SHOWN_JS = """(names) => {
  function shown(el) {
    if (!el) return 'missing';
    var cs = getComputedStyle(el), r = el.getBoundingClientRect();
    if (cs.visibility !== 'visible' || cs.display === 'none' || parseFloat(cs.opacity) === 0) return 'hidden';
    var m = cs.color.match(/rgba?\\(([^)]+)\\)/), parts = m ? m[1].split(',') : [];
    if (parts.length === 4 && parseFloat(parts[3]) === 0) return 'transparent';
    if (cs.color === 'transparent') return 'transparent';
    if (r.width < 1 || r.height < 1) return 'zero-size';
    if (r.top < 0 || r.bottom > innerHeight) return 'out of view (' + Math.round(r.top) + '..' + Math.round(r.bottom) + ')';
    return 'ok';
  }
  var x = document.getElementById('labelX'), y = document.getElementById('labelY'), p = document.getElementById('prompt');
  var res = [];
  [['x-axis title', x, names[0]], ['y-axis title', y, names[1]]].forEach(function (t) {
    var s = shown(t[1]);
    if (s !== 'ok') res.push(t[0] + ' ' + s);
    else if (t[1].innerText.indexOf(t[2]) < 0) res.push(t[0] + ' does not name ' + JSON.stringify(t[2]));
  });
  var btns = Array.prototype.map.call(document.querySelectorAll('#choices .choice'), function (b) { return b.innerText.trim(); });
  return { problems: res, buttons: btns, answered: COC.ui.answered() };
}"""


async def play_all(page, by_id, policy="alternate"):
    """Play a session of every item with real clicks. Returns (problems, played)."""
    out = []
    await page.evaluate("() => { var all = COC.BANK.slice(); COC.deal = function () { return all.slice(); }; }")
    await page.click("#startBtn")
    played = 0
    for i in range(len(by_id) + 1):
        if await page.is_visible("#results"):
            break
        qid = await page.evaluate("COC.ui.current()")
        q = by_id.get(qid)
        if q is None:
            out.append("question %d: unknown item %r" % (i + 1, qid))
            break
        seen = await page.evaluate(LABELS_SHOWN_JS, [q["x"][0], q["y"][0]])
        if seen["answered"]:
            out.append("%s: already answered before any click" % qid)
        for p in seen["problems"]:
            out.append("%s: before the answer, %s" % (qid, p))
        if sorted(seen["buttons"]) != sorted(BUTTONS.values()):
            out.append("%s: answer buttons are %s, not the three" % (qid, seen["buttons"]))
            break
        pick = q["cat"] if (policy == "right" or (policy == "alternate" and i % 2 == 0)) else \
            CATS[(CATS.index(q["cat"]) + 1) % 3]
        await page.click("#choices .choice[data-cat='%s']" % pick)
        fb = await page.inner_text("#feedback")
        must = [q["explain"]]
        if q["cat"] == "both":
            must.append(q["lurk"][:1].upper() + q["lurk"][1:])
        if q["cat"] == "chance":
            must.append(q["joke"])
        for m in must:
            if m not in fb:
                out.append("%s: the feedback does not show %r" % (qid, m[:60]))
        if await page.locator("#feedback .maffs-next").count() != 1:
            out.append("%s: no Next control after the answer" % qid)
            break
        await page.click("#feedback .maffs-next")
        played += 1
    score = await page.evaluate("COC.ui.score()")
    want = 100 * sum(1 for i, _ in enumerate(by_id) if policy == "right" or (policy == "alternate" and i % 2 == 0))
    if played == len(by_id) and score != want:
        out.append("score %d after the session, expected %d" % (score, want))
    return out, played


FIT_JS = """() => {
  var foot = document.querySelector('.site-footer'), fold = foot ? foot.getBoundingClientRect().top : innerHeight;
  var btns = document.querySelectorAll('#choices .choice'), last = btns[btns.length - 1];
  return { fold: fold, wide: document.documentElement.scrollWidth - innerWidth,
           ask: last ? last.getBoundingClientRect().bottom : null };
}"""
FIT_FB_JS = """() => {
  var foot = document.querySelector('.site-footer'), fold = foot ? foot.getBoundingClientRect().top : innerHeight;
  var n = document.querySelector('#feedback .maffs-next');
  return { fold: fold, wide: document.documentElement.scrollWidth - innerWidth, next: n ? n.getBoundingClientRect().bottom : null };
}"""


async def phone_fit(browser, by_id):
    out, worst = [], {}
    for w, h in PHONES:
        ctx, page, errors = await new_page(browser, (w, h))
        try:
            await page.evaluate("() => { var all = COC.BANK.slice(); COC.deal = function () { return all.slice(); }; }")
            await page.evaluate("document.getElementById('startBtn').click()")
            for _ in range(len(by_id)):
                qid = await page.evaluate("COC.ui.current()")
                q = by_id[qid]
                a = await page.evaluate(FIT_JS)
                if a["wide"] > 0:
                    out.append("%dx%d %s: the page scrolls sideways by %dpx" % (w, h, qid, a["wide"]))
                if a["ask"] is None or a["ask"] > a["fold"]:
                    out.append("%dx%d %s: the answer buttons end at %s, below the footer at %d" % (w, h, qid, a["ask"], a["fold"]))
                wrong = CATS[(CATS.index(q["cat"]) + 1) % 3]
                await page.evaluate("document.querySelector(\"#choices .choice[data-cat='%s']\").click()" % wrong)
                f = await page.evaluate(FIT_FB_JS)
                if f["next"] is None or f["next"] > f["fold"]:
                    out.append("%dx%d %s: after a wrong answer Next ends at %s, below the footer at %d" % (w, h, qid, f["next"], f["fold"]))
                key = "%dx%d" % (w, h)
                worst[key] = max(worst.get(key, (-1e9, ""))[0], (f["next"] or 0) - f["fold"]), qid
                await page.evaluate("document.querySelector('#feedback .maffs-next').click()")
            for e in errors:
                out.append("%dx%d page error: %s" % (w, h, e))
        finally:
            await ctx.close()
    return out


async def collect(page):
    bank = await page.evaluate("JSON.parse(JSON.stringify(COC.BANK))")
    points = await page.evaluate("() => { var o = {}; COC.BANK.forEach(function (q) { o[q.id] = COC.points(q); }); return o; }")
    found, counts = check_bank(bank, points)
    found += check_deals(await page.evaluate(DEALS_JS), bank)
    return found, bank, counts


FAULTS = [
    ("labels hidden until the answer (the audit's F1)",
     "(function(){ var o = COC.renderLabels; COC.renderLabels = function (q) { o(q);"
     " document.getElementById('labelX').style.color = 'transparent';"
     " document.getElementById('labelY').style.visibility = 'hidden'; }; })();"),
    ("a 'both' item with no lurking variable", "COC.BANK.filter(function(q){return q.cat==='both';})[3].lurk = '';"),
    ("a coincidence with no joke theory", "COC.BANK.filter(function(q){return q.cat==='chance';})[5].joke = '';"),
    ("an item outside the three categories", "COC.BANK[7].cat = 'maybe';"),
    ("an empty explanation", "COC.BANK[11].explain = ' ';"),
    ("a lopsided split (six coincidences relabelled)",
     "COC.BANK.filter(function(q){return q.cat==='chance';}).slice(0,6).forEach(function(q){ q.cat='cause'; delete q.joke; });"),
    ("a graph drawn the wrong way (A3 flipped)",
     "(function(){ var o = COC.points; COC.points = function (q) { var p = o(q);"
     " return q.id === 'A3' ? p.map(function (a) { return [a[0], q.y[1] + q.y[2] - a[1]]; }) : p; }; })();"),
    ("a graph weaker than its stated strength",
     "(function(){ var o = COC.points; COC.points = function (q) { var p = o(q); if (q.str !== 'very strong') return p;"
     " return p.map(function (a, i) { return [a[0], i % 2 ? q.y[1] : q.y[2]]; }); }; })();"),
    ("only two answer buttons",
     "new MutationObserver(function () { var b = document.querySelectorAll('#choices .choice');"
     " if (b.length === 3) b[2].remove(); }).observe(document.getElementById('choices'), { childList: true });"),
    ("the lurking variable left out of the feedback",
     "(function(){ var o = COC.feedbackHtml; COC.feedbackHtml = function (q, ok) {"
     " return o(q, ok).replace(/<div class=\"fb-lurk\">.*?<\\/div>/, ''); }; })();"),
    ("a SR-14 tier (a) word in an explanation", "COC.BANK[1].explain = 'Nobody drowned.';"),
    ("a SR-14 tier (b) word in a joke", "COC.BANK.filter(function(q){return q.cat==='chance';})[2].joke = 'Cheese cures flu.';"),
    ("a deal that leaves out a kind",
     "(function(){ COC.deal = function (n) { return COC.BANK.filter(function(q){return q.cat!=='chance';}).slice(0, n); }; })();"),
]


async def selftest(browser, by_id):
    lines, ok = [], True
    for name, patch in FAULTS:
        ctx, page, _ = await new_page(browser)
        try:
            try:
                await page.evaluate(patch)
                found, bank, _ = await collect(page)
                if not found:
                    play, _ = await play_all(page, {q["id"]: q for q in bank})
                    found = play
            except Exception as exc:          # a fault that breaks the page is reported, so caught
                found = ["the page broke: %s" % str(exc).splitlines()[0]]
        finally:
            await ctx.close()
        caught = bool(found)
        ok = ok and caught
        lines.append("  %-52s %s" % (name, ("CAUGHT (%d, e.g. %s)" % (len(found), found[0][:80])) if caught else "*** MISSED ***"))
    return ok, lines


async def run_all(args):
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx, page, errors = await new_page(browser)
        found, bank, counts = await collect(page)
        by_id = {q["id"]: q for q in bank}
        for f in found:
            fail(f)
        print("Bank: %d items (cause %d, both %d, chance %d); every graph's r recomputed; 300 deals checked"
              % (len(bank), counts["cause"], counts["both"], counts["chance"]))
        # The session-length buttons offer the whole bank.
        if not await page.locator("#sessionSelect button", has_text="All").count():
            fail("the session-length buttons offer no way to play the whole bank")
        play, played = await play_all(page, by_id)
        for f in play:
            fail("play: " + f)
        for e in errors:
            fail("page error: " + e)
        await ctx.close()
        print("Play (real clicks, Firebase blocked): %d of %d items; labels on screen before every answer" % (played, len(bank)))
        fit = await phone_fit(browser, by_id)
        for f in fit:
            fail("phone fit: " + f)
        print("Phone fit: %d items x %d sizes, asking screen and wrong-answer feedback" % (len(bank), len(PHONES)))
        if not args.no_selftest:
            ok, lines = await selftest(browser, by_id)
            print()
            print("Fault-injection self-test (patched into a fresh page; the file is never touched):")
            for ln in lines:
                print(ln)
            if not ok:
                fail("fault-injection self-test: at least one fault was not caught")
        await browser.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-selftest", action="store_true", help="skip the fault-injection self-test")
    args = ap.parse_args()
    global PORT
    try:
        server, base = bc.start_stub_server()
    except bc.StubServerError as exc:
        fail("stub server did not start: %s" % exc)
    else:
        PORT = urlsplit(base).port
        try:
            asyncio.run(run_all(args))
        finally:
            server.terminate()
    print()
    if _FAILURES:
        print("%d FAILURE(S)" % len(_FAILURES))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
