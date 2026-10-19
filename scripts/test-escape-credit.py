#!/usr/bin/env python3
# ci-line: Escape-room credits (every credited room's start screen and teacher page show its room.js credit and the one invitation exactly once, linked to /feedback/; uncredited rooms show none; at 320, 390 and 1280 px no note leaves its container or truncates a title, on the room pages, the hub and the front page) |
# ci-deps: escape-rooms/ index.html scripts/check-teacher-invite.py
"""Browser test for escape-room credits (contract ROOM-CREDIT v2, 19 Oct 2026).

    python scripts/test-escape-credit.py

A room's optional `credit` in room.js is its credit sentence(s). rating.js credit(room) draws it with the one
shared invitation, "Want something built? Let us know." ("Let us know." linking to /feedback/), on the start
screen (engine.js) and the teacher page (teacher.js). check-escape-rooms.py holds the hub and front-page card
notes, which are static copies, to the same field. This test plays the drawn pages in Chromium:

  text    every live room's start screen (#scrBrief) and teacher page: a credited room shows one .credit note
          reading credit + invitation exactly, its credit sentence once on the page, and one link in the note,
          to /feedback/, reading "Let us know."; an uncredited room shows no .credit note and no invitation
  fit     at 320x568, 390x844 and 1280x900, on each credited room's start screen and teacher page and on the
          hub and front page: every credit note lies inside its container (the card, or the card's cell on the
          hub and front page) and scrolls nothing sideways itself, and every room title (h1 on the room pages,
          h3 on the cards) is not cut off (its scrollWidth fits its box)
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

INVITE = "Want something built? Let us know."
WIDTHS = ((320, 568), (390, 844), (1280, 900))

NOTES = """(sel) => { const root = document.querySelector(sel) || document.body;
  return { notes: [...root.querySelectorAll('.credit')].map(n => ({
             text: n.textContent.replace(/\\s+/g, ' ').trim(),
             links: [...n.querySelectorAll('a')].map(a => [a.getAttribute('href'), a.textContent.trim()]) })),
           body: root.textContent.replace(/\\s+/g, ' '),
           invites: (root.textContent.match(/Want something built\\?/g) || []).length }; }"""
# Every credit note against its container, and every title against its own box.
FIT = """(args) => { const [noteSel, boxSel, titleSel] = args, out = [];
  document.querySelectorAll(noteSel).forEach(n => {
    const box = n.closest(boxSel) || n.parentElement, a = n.getBoundingClientRect(), b = box.getBoundingClientRect();
    if (a.left < b.left - 0.5 || a.right > b.right + 0.5) out.push('the note "' + n.textContent.trim().slice(0, 40) +
      '" spans ' + Math.round(a.left) + '-' + Math.round(a.right) + ' px, its container ' + Math.round(b.left) + '-' + Math.round(b.right));
    if (n.scrollWidth > n.clientWidth + 1) out.push('the note "' + n.textContent.trim().slice(0, 40) + '" scrolls sideways');
  });
  document.querySelectorAll(titleSel).forEach(t => {
    if (t.scrollWidth > t.clientWidth + 1) out.push('the title "' + t.textContent.trim().slice(0, 40) + '" is cut off');
  });
  return out; }"""


def credits():
    """{slug: credit} for every room.js with a credit (the same reading as check-escape-rooms.py)."""
    out = {}
    for d in sorted((ROOT / "escape-rooms").iterdir()):
        js = (d / "room.js").read_text(encoding="utf-8").replace("\r\n", "\n") if (d / "room.js").exists() else ""
        m = re.search(r'\n  credit: "([^"\\]+)",', js)
        if m:
            out[d.name] = m.group(1)
    return out


async def run(rooms, credit):
    from playwright.async_api import async_playwright
    proc, base = ti._serve(ROOT)
    faults = []
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(3)

            async def open_at(path, w, h):
                ctx = await browser.new_context(viewport={"width": w, "height": h})
                await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
                page = await ctx.new_page()
                await page.goto(base + path, wait_until="load", timeout=20000)
                await page.wait_for_timeout(200)
                return ctx, page

            async def text(slug):
                want = credit.get(slug)
                for where, path, sel in (("start screen", "/escape-rooms/%s/" % slug, "#scrBrief"),
                                         ("teacher page", "/escape-rooms/%s/teacher.html" % slug, "body")):
                    async with sem:
                        ctx, page = await open_at(path, 1280, 900)
                        try:
                            got = await page.evaluate(NOTES, sel)
                        finally:
                            await ctx.close()
                    if want is None:
                        if got["notes"] or got["invites"]:
                            faults.append("%s: the %s shows a credit (%s), but the room has none" % (
                                slug, where, [n["text"] for n in got["notes"]] or "the invitation"))
                        continue
                    full = "%s %s" % (want, INVITE)
                    if [n["text"] for n in got["notes"]] != [full]:
                        faults.append("%s: the %s's credit notes are %s, want exactly one reading %r" % (
                            slug, where, [n["text"] for n in got["notes"]], full))
                        continue
                    if got["notes"][0]["links"] != [["/feedback/", "Let us know."]]:
                        faults.append("%s: the %s's credit links are %s, want one to /feedback/ reading 'Let us know.'" % (
                            slug, where, got["notes"][0]["links"]))
                    if got["body"].count(want) != 1 or got["invites"] != 1:
                        faults.append("%s: the %s shows the credit %d time(s) and the invitation %d time(s), want once each" % (
                            slug, where, got["body"].count(want), got["invites"]))

            async def fit(path, note_sel, box_sel, title_sel, w, h):
                async with sem:
                    ctx, page = await open_at(path, w, h)
                    try:
                        got = await page.evaluate(FIT, [note_sel, box_sel, title_sel])
                        notes = await page.evaluate("(s) => document.querySelectorAll(s).length", note_sel)
                    finally:
                        await ctx.close()
                if not notes:
                    faults.append("%s at %d px: no credit note to measure" % (path, w))
                for g in got:
                    faults.append("%s at %d px: %s" % (path, w, g))

            jobs = [text(r) for r in rooms]
            for w, h in WIDTHS:
                for slug in sorted(credit):
                    if slug not in rooms:
                        continue
                    jobs.append(fit("/escape-rooms/%s/" % slug, "#scrBrief .credit", ".card", "#scrBrief h1", w, h))
                    jobs.append(fit("/escape-rooms/%s/teacher.html" % slug, ".credit", ".card", "h1", w, h))
                # On the hub and front page the note sits under its card in the card's cell (the cell is the
                # card link's parent; a card is one link, so the note cannot sit inside it).
                jobs.append(fit("/escape-rooms/", "p.print-note", "div", ".room-card h3", w, h))
                jobs.append(fit("/", "span.esc-note:not(.esc-key)", "div", ".esc-card h3", w, h))
            await asyncio.gather(*jobs)
            await browser.close()
    finally:
        proc.terminate()
    return faults


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rooms = ti.live_rooms(ROOT)
    credit = credits()
    faults = asyncio.run(run(rooms, credit))
    print("Escape-room credits (ROOM-CREDIT v2): %d live room(s), %d credited: %s" % (
        len(rooms), len(credit), "; ".join("%s %r" % kv for kv in sorted(credit.items()))))
    for f in faults:
        print("  FAIL  " + f)
    print("PASS" if not faults else "FAIL")
    return 0 if not faults else 1


if __name__ == "__main__":
    sys.exit(main())
