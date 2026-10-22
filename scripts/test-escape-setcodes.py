#!/usr/bin/env python3
# ci-line: Escape-room set codes (every live room, every lock, every set forced through a saved state in Chromium: the lock screen shows its letter, and a fresh teacher page with no game gives, under that letter, the answer that opens the lock; no bare single-set answer without a live game; four faults planted and caught) |
# ci-deps: escape-rooms/ scripts/check-teacher-invite.py
"""Browser test for the escape-room set codes (contract SET-CODES, 22 Oct 2026; canon 11.3).

    python scripts/test-escape-setcodes.py               # every live room, then the four plants
    python scripts/test-escape-setcodes.py --no-plants   # without the plants

Each lock draws one set from its library per play. The lock screen shows that set as a letter ("Set C"), and the
teacher page lists every set under the same letter, so a teacher on another device reads the right answer.
The letters live once, in escape-rooms/assets/rating.js (SET_CODES): A B C D E F G H J K, no I.

  student  for every live room, every lock, every set: a saved state (the shape engine.js saves, vars forced) is
           put in localStorage, the page reloaded and Resume pressed, and the lock opened. A lock with two or
           more sets shows exactly one "Set X" tag, X the letter expected for that index (written out here, not
           read from rating.js), before and after it opens; a lock with one set shows none
  teacher  one fresh browser context per room, with no localStorage (no game on the device). For every lock with
           two or more sets: the "The locks" row reads "By set, see below" in the Answer and Wrong-answer
           cells, the lock's heading reads "answer depends on the set" and shows no number, and the library table
           has one row per set, lettered A, B, C ... in order
  opens    the answer read from the teacher page's row for that letter is set on the forced lock (typed into its
           own fallback box) and the lock must open ("Open.")
  live     with a game started in the same context, the teacher page follows it: the answer reads "(Set X)" with
           the letter the lock screen shows, and nothing says "By set"
  plants   engines served by routing (no file is edited), each of which must FAIL the check above, on one room:
             the lock-screen letter off by one; the teacher's rows lettered from 1; the teacher summary giving
             set A's answer with no live game; a code containing a digit
"""
import argparse
import asyncio
import importlib.util
import json
import os
import pathlib
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = pathlib.Path(HERE).parent
_spec = importlib.util.spec_from_file_location("teacher_invite", os.path.join(HERE, "check-teacher-invite.py"))
ti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ti)

ASSETS = ROOT / "escape-rooms" / "assets"
EXPECTED = "ABCDEFGHJK"          # written out here on purpose: the test must not read the answer from the code under test
PLANT_ROOM = "comic-caper"

LOCKS = """() => window.ROOM.locks.map(l => ({
  id: l.id, n: (l.variants || []).length, ins: l.instrument,
  digits: l.instrument.digits || 0, kind: l.instrument.kind }))"""
SEEN = """() => ({
  tags: [...document.querySelectorAll('#lockPanel .set-code')].map(e => e.textContent.trim()),
  open: !document.getElementById('setBtn') && !!document.querySelector('#lockPanel .feedback.good.show'),
  openText: (document.querySelector('#lockPanel .feedback.good.show') || {}).textContent || ''
})"""
TEACHER = """() => {
  const out = {};
  for (const panel of document.querySelectorAll('div.panel[data-lock]')) {
    const id = panel.getAttribute('data-lock');
    const row = document.querySelector('tr[data-lock="' + id + '"]');
    out[id] = {
      head: panel.querySelector('h3').textContent.trim(),
      summaryAns: row ? row.querySelector('td.ans').textContent.trim() : null,
      summaryMiss: row ? row.querySelector('td.wrongans').textContent.trim() : null,
      rows: [...panel.querySelectorAll('tr[data-set]')].map(r => ({
        code: r.getAttribute('data-set'),
        first: r.children[0].textContent.replace('in play', '').replace(/[^A-Za-z0-9]/g, ''),
        ans: r.querySelector('td.ans').textContent.trim()
      }))
    };
  }
  return out;
}"""


def live_rooms():
    rooms = []
    for d in sorted((ROOT / "escape-rooms").iterdir()):
        idx = d / "index.html"
        if idx.is_file() and (d / "room.js").is_file() and "noindex" not in idx.read_text(encoding="utf-8"):
            rooms.append(d.name)
    return rooms


def save_for(room_slug, total, vars_):
    return json.dumps({"v": 1, "found": {}, "open": {}, "hints": {}, "wrongs": 0, "left": total, "done": None,
                       "vars": vars_})


def to_input(lock, text):
    """The value(s) to type for a teacher-page answer string: [(selector, value)]."""
    nums = re.findall(r"-?\d+(?:\.\d+)?", re.sub(r"\(Set [A-Z]\)", "", text))
    kind = lock["kind"]
    if kind == "keypad":
        digits = "".join(re.findall(r"\d", re.sub(r"\(Set [A-Z]\)", "", text)))
        return [("#numK", digits.zfill(lock["digits"]) if lock["digits"] else digits)]
    if kind == "pair":
        return [("#numA", nums[0]), ("#numB", nums[1])] if len(nums) >= 2 else []
    return [("#num", nums[0])] if nums else []


async def new_ctx(browser, base, subs):
    ctx = await browser.new_context(viewport={"width": 1100, "height": 900})
    await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
    def handler_for(fn):
        async def handler(route):
            resp = await route.fetch()
            body = fn((await resp.body()).decode("utf-8"))
            await route.fulfill(response=resp, body=body)
        return handler
    for pat, fn in subs:
        await ctx.route(re.compile(pat), handler_for(fn))
    return ctx


async def check_room(browser, base, slug, subs):
    fails = []

    def want(cond, msg):
        if not cond:
            fails.append("%s: %s" % (slug, msg))
    stats = {"locks": 0, "sets": 0}

    # ---- the teacher page, fresh: no localStorage, so no game on the device ----
    tctx = await new_ctx(browser, base, subs)
    tpage = await tctx.new_page()
    await tpage.goto(base + "/escape-rooms/%s/teacher.html" % slug, wait_until="load", timeout=20000)
    await tpage.wait_for_selector("div.panel[data-lock]")
    teacher = await tpage.evaluate(TEACHER)
    banner = await tpage.evaluate("() => (document.getElementById('liveBox') || {}).textContent || ''")
    want("No game running on this device" in banner and "set letter" in banner, "the no-game banner does not tell the teacher to ask for the set letter (%r)" % banner[:80])
    await tctx.close()

    # ---- the student page ----
    ctx = await new_ctx(browser, base, subs)
    page = await ctx.new_page()
    await page.goto(base + "/escape-rooms/%s/" % slug, wait_until="load", timeout=20000)
    locks = await page.evaluate(LOCKS)
    total = await page.evaluate("() => (window.ROOM.minutes || 15) * 60")
    key = "mfg_escape_" + await page.evaluate("() => window.ROOM.slug")
    for lk in locks:
        t = teacher.get(lk["id"])
        want(t is not None, "%s: the teacher page has no panel for this lock" % lk["id"])
        if t is None:
            continue
        stats["locks"] += 1
        if lk["n"] >= 2:
            want(t["summaryAns"] == "By set, see below" and t["summaryMiss"] == "By set, see below",
                 "%s: with no game the locks table gives %r / %r, want 'By set, see below'" % (lk["id"], t["summaryAns"], t["summaryMiss"]))
            want(t["head"].endswith("answer depends on the set") and not re.search(r"answer\s*[-\d]", t["head"]),
                 "%s: with no game the heading reads %r" % (lk["id"], t["head"]))
            want([r["code"] for r in t["rows"]] == list(EXPECTED[:lk["n"]]),
                 "%s: the teacher's set rows are %r, want %s" % (lk["id"], [r["code"] for r in t["rows"]], list(EXPECTED[:lk["n"]])))
            want([r["first"] for r in t["rows"]] == list(EXPECTED[:lk["n"]]),
                 "%s: the first column reads %r, want the letters" % (lk["id"], [r["first"] for r in t["rows"]]))
        else:
            want(not t["rows"], "%s: a single-set lock has a set table" % lk["id"])

    vars_all = {lk["id"]: 0 for lk in locks}
    for lk in locks:
        t = teacher.get(lk["id"])
        sets = max(lk["n"], 1)
        for k in range(sets):
            stats["sets"] += 1
            v = dict(vars_all)
            v[lk["id"]] = k
            await page.evaluate("([key, val]) => localStorage.setItem(key, val)",
                                [key, save_for(slug, total, v)])
            await page.reload(wait_until="load")
            await page.click("#resumeBtn")
            idx = [x["id"] for x in locks].index(lk["id"])
            await page.click('[data-lock="%d"]' % idx)
            seen = await page.evaluate(SEEN)
            if lk["n"] < 2:
                want(not seen["tags"], "%s: a single-set lock shows %r" % (lk["id"], seen["tags"]))
                continue
            want(seen["tags"] == ["Set " + EXPECTED[k]],
                 "%s set %d: the lock screen shows %r, want 'Set %s'" % (lk["id"], k, seen["tags"], EXPECTED[k]))
            row = next((r for r in (t or {"rows": []})["rows"] if r["code"] == EXPECTED[k]), None)
            want(row is not None, "%s: no teacher row for Set %s" % (lk["id"], EXPECTED[k]))
            if row is None:
                continue
            fill = to_input(lk, row["ans"])
            want(bool(fill), "%s Set %s: cannot read an answer from the teacher row %r" % (lk["id"], EXPECTED[k], row["ans"]))
            if not fill:
                continue
            for sel, val in fill:
                await page.fill(sel, val)
            await page.click("#setBtn")
            await page.wait_for_timeout(40)
            seen = await page.evaluate(SEEN)
            want(seen["open"] and "Open." in seen["openText"],
                 "%s Set %s: the teacher's answer %r did not open the lock" % (lk["id"], EXPECTED[k], row["ans"]))
            want(seen["tags"] == ["Set " + EXPECTED[k]],
                 "%s Set %s: after opening, the lock screen shows %r" % (lk["id"], EXPECTED[k], seen["tags"]))
            await page.evaluate("() => localStorage.clear()")
    await ctx.close()

    # ---- a live game on the same device: the teacher page follows it ----
    multi = [lk for lk in locks if lk["n"] >= 2]
    if multi:
        lk = multi[-1]
        k = lk["n"] - 1
        ctx = await new_ctx(browser, base, subs)
        page = await ctx.new_page()
        await page.goto(base + "/escape-rooms/%s/" % slug, wait_until="load", timeout=20000)
        key = "mfg_escape_" + await page.evaluate("() => window.ROOM.slug")
        v = {x["id"]: 0 for x in locks}
        v[lk["id"]] = k
        await page.evaluate("([key, val]) => localStorage.setItem(key, val)", [key, save_for(slug, total, v)])
        await page.reload(wait_until="load")
        await page.click("#resumeBtn")
        tp = await ctx.new_page()
        await tp.goto(base + "/escape-rooms/%s/teacher.html" % slug, wait_until="load", timeout=20000)
        await tp.wait_for_selector("div.panel[data-lock]")
        cell = await tp.evaluate("(id) => document.querySelector('tr[data-lock=\"' + id + '\"] td.ans').textContent.trim()", lk["id"])
        body = await tp.evaluate("() => document.body.textContent")
        want(cell.endswith("(Set %s)" % EXPECTED[k]), "%s: with a live game the answer reads %r, want '(Set %s)'" % (lk["id"], cell, EXPECTED[k]))
        want("By set, see below" not in body, "the teacher page says 'By set' while a game is live")
        await ctx.close()
    return fails, stats


async def run(subs, rooms):
    from playwright.async_api import async_playwright
    proc, base = ti._serve(ROOT)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(3)

            async def lim(slug):
                async with sem:
                    return await check_room(browser, base, slug, subs)
            res = await asyncio.gather(*[lim(r) for r in rooms], return_exceptions=True)
            await browser.close()
    finally:
        proc.terminate()
    fails, locks, sets = [], 0, 0
    for r, slug in zip(res, rooms):
        if isinstance(r, Exception):
            fails.append("%s: could not drive the page: %s" % (slug, str(r).splitlines()[0][:120]))
        else:
            fails += r[0]
            locks += r[1]["locks"]
            sets += r[1]["sets"]
    return fails, locks, sets


def sub_in(path_name, old, new):
    src = (ASSETS / path_name).read_text(encoding="utf-8")
    assert old in src, "plant: %r not found in %s" % (old[:50], path_name)
    return (r"/escape-rooms/assets/%s(\?.*)?$" % re.escape(path_name), lambda s: s.replace(old, new, 1))


PLANTS = [
    ("lock-screen letter off by one", sub_in("engine.js", "M.setCode(Math.min(", "M.setCode(1 + Math.min(")),
    ("teacher rows lettered from 1", sub_in("teacher.js", "return M && M.setCode ? M.setCode(i) : '';", "return String(i + 1);")),
    ("teacher summary gives set A's answer with no live game", sub_in("teacher.js", "return !live && multi(l);", "return false;")),
    ("a code containing a digit", sub_in("rating.js", "'ABCDEFGHJK'", "'ABCDEFGH12'")),
]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-plants", action="store_true")
    a = ap.parse_args()
    rooms = live_rooms()
    fails, locks, sets = asyncio.run(run([], rooms))
    print("Escape-room set codes (SET-CODES): %d live rooms, %d locks, %d sets forced" % (len(rooms), locks, sets))
    for f in fails[:20]:
        print("  FAIL  " + f)
    print("  %s  every lock shows its letter, the teacher page gives that letter's answer, and it opens the lock"
          % ("FAIL" if fails else "ok  "))
    ok = not fails
    if not a.no_plants:
        for name, sub in PLANTS:
            pf, _, _ = asyncio.run(run([sub], [PLANT_ROOM]))
            print("  %s  plant: %s%s" % ("ok  " if pf else "FAIL", name, " (caught: %s)" % pf[0][:90] if pf else " (NOT caught)"))
            ok = ok and bool(pf)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
