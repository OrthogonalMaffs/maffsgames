#!/usr/bin/env python3
# ci-line: Escape-room difficulty stars (every live room's start screen and teacher page show its hub card's rating, with the text equivalent; "Suits a top set" on 3-star teacher pages only; no sideways scroll at 320 px on the rooms, teacher pages, hub and front page) |
# ci-deps: escape-rooms/ index.html scripts/check-teacher-invite.py
"""Browser test for the escape-room difficulty rating (contract ESCAPE-DIFFICULTY, 10 Oct 2026).

    python scripts/test-escape-rating.py

check-escape-rooms.py derives each room's rating from its locks' grades and fails a hub or front-page card
that disagrees. The start screen and the teacher page are drawn at run time by rating.js, so this test
plays them in Chromium and holds them to the hub card:

  start    every live room's start screen (#scrBrief) shows one .rating with the hub card's data-stars, the
           same visible label ("★★ Core · grades 4–5") and the text equivalent ("Difficulty: 2 of 3, Core,
           grades 4–5"); "Suits a top set" appears nowhere on it
  teacher  the room's teacher.html shows the same rating, and "Suits a top set" exactly when it is ★★★
  phone    at 320x568, no sideways scroll on each room's start screen, each teacher page, the hub and the
           front page (the longest label is "★★★ Challenge · grades 6–9"). On a teacher page the answer
           tables (table.tt) are hidden first: they are its known overflow, allowlisted in check-site
           (todo §1.37), and this test is about everything else, the rating included
"""
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

RATING = """(sel) => [...document.querySelectorAll(sel + ' .rating')].map(r => ({
  stars: r.getAttribute('data-stars'),
  label: (r.querySelector('[aria-hidden="true"]') || {}).textContent,
  sr: (r.querySelector('.sr-only') || {}).textContent }))"""
TOPSET = "(sel) => (document.querySelector(sel) || document.body).textContent.includes('Suits a top set')"
WIDE = "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"


def hub_cards():
    html = (ROOT / "escape-rooms" / "index.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<a class="room-card" href="([a-z0-9-]+)/".*?</a>', html, re.S):
        c = re.search(r'data-stars="(\d)"><span aria-hidden="true">([^<]*)</span><span class="sr-only">([^<]*)</span>', m.group(0))
        if c:
            out[m.group(1)] = {"stars": c.group(1), "label": c.group(2).replace("&middot;", "·"), "sr": c.group(3)}
    return out


async def run(rooms, cards):
    from playwright.async_api import async_playwright
    proc, base = ti._serve(ROOT)
    faults = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(3)

            async def page_at(w, h):
                ctx = await browser.new_context(viewport={"width": w, "height": h})
                await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
                return ctx, await ctx.new_page()

            async def room(slug):
                want = cards.get(slug)
                async with sem:
                    ctx, page = await page_at(1280, 900)
                    try:
                        await page.goto(base + "/escape-rooms/%s/" % slug, wait_until="load", timeout=20000)
                        start = await page.evaluate(RATING, "#scrBrief")
                        start_top = await page.evaluate(TOPSET, "#app")
                        await page.goto(base + "/escape-rooms/%s/teacher.html" % slug, wait_until="load", timeout=20000)
                        await page.wait_for_timeout(200)
                        teach = await page.evaluate(RATING, "body")
                        teach_top = await page.evaluate(TOPSET, "body")
                    finally:
                        await ctx.close()
                if not want:
                    faults.append("%s: no rating on its hub card" % slug)
                    return
                for where, got in (("start screen", start), ("teacher page", teach)):
                    if len(got) != 1:
                        faults.append("%s: the %s shows %d ratings, want 1" % (slug, where, len(got)))
                    elif got[0] != want:
                        faults.append("%s: the %s shows %s, the hub card %s" % (slug, where, got[0], want))
                if start_top:
                    faults.append("%s: the start screen says \"Suits a top set\" (teacher pages only)" % slug)
                if teach_top != (want["stars"] == "3"):
                    faults.append("%s: the teacher page %s \"Suits a top set\" at %s star(s)"
                                  % (slug, "says" if teach_top else "does not say", want["stars"]))

            async def narrow(path):
                async with sem:
                    ctx, page = await page_at(320, 568)
                    try:
                        await page.goto(base + path, wait_until="load", timeout=20000)
                        await page.wait_for_timeout(200)
                        if path.endswith("teacher.html"):
                            # The answer tables are the teacher pages' known 320 px overflow, allowlisted in
                            # check-site (scripts/checker-allowlist.json, todo §1.37). Hide them, so this
                            # measures everything else on the page, the rating included.
                            await page.add_style_tag(content="table.tt{display:none!important}")
                            await page.wait_for_timeout(100)
                        over = await page.evaluate(WIDE)
                    finally:
                        await ctx.close()
                if over > 0:
                    faults.append("%s: scrolls sideways by %d px at 320x568" % (path, over))

            paths = ["/", "/escape-rooms/"] + ["/escape-rooms/%s/%s" % (r, t) for r in rooms for t in ("", "teacher.html")]
            await asyncio.gather(*([room(r) for r in rooms] + [narrow(x) for x in paths]))
            await browser.close()
    finally:
        proc.terminate()
    return faults


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rooms = ti.live_rooms(ROOT)
    cards = hub_cards()
    faults = asyncio.run(run(rooms, cards))
    print("Escape-room difficulty (ESCAPE-DIFFICULTY): %d live room(s): %s" % (
        len(rooms), ", ".join("%s %s" % (r, "★" * int(cards[r]["stars"])) for r in rooms if r in cards)))
    for f in faults:
        print("  FAIL  " + f)
    print("PASS" if not faults else "FAIL")
    return 0 if not faults else 1


if __name__ == "__main__":
    sys.exit(main())
