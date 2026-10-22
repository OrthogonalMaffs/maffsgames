#!/usr/bin/env python3
# ci-line: The Comic Caper (lock 1 and lock 3 briefs rendered exactly, inside their panel at 320, 390 and 1280 px; the old wording and an overflow planted and caught) |
# ci-deps: escape-rooms/comic-caper/ escape-rooms/assets/ scripts/check-teacher-invite.py
"""Verifier for The Comic Caper's lock briefs (contract COMIC-CAPER-BRIEFS, 22 Oct 2026).

    python scripts/verify-comic-caper.py

docs/audits/comic-caper-locks-2026-10-22.md found every lock opening on its worked answer, and two briefs that
did not say what to find: lock 3's "Every bundle has the same number of grammar books and dictionaries" reads as
"as many grammar books as dictionaries" (no set works that way) and never asked for the largest number of
bundles; lock 1's said the dial was "numbered all the way round" (it shows no numbers). Jon's wording replaced
both. This verifier plays the page in Chromium (analytics stubbed) and checks:

  text    each brief, as the panel renders it (#lockPanel .lock-brief, innerText), is exactly the wording below
  fit     at 320x568, 390x844 and 1280x900 each brief lies inside its panel, scrolls nothing sideways itself,
          and the page scrolls nothing sideways
  plants  the same checks run against room.js served with each old brief, and with the panel's text forced onto
          one line, and must fail each time
"""
import importlib.util
import os
import pathlib
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = pathlib.Path(HERE).parent
_spec = importlib.util.spec_from_file_location("teacher_invite", os.path.join(HERE, "check-teacher-invite.py"))
ti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ti)

ROOM = "/escape-rooms/comic-caper/"
WIDTHS = ((320, 568), (390, 844), (1280, 900))
# Lock index on the page -> the brief it must render (Jon's wording, 22 Oct 2026).
BRIEFS = {
    0: "A dial on the hinge side. It opens at the number of factors of the cupboard’s asset number.",
    2: "A brass slider across the handle. It opens at the largest number of identical bundles you can make from "
       "the grammar books and the dictionaries, using every book. Identical means every bundle has the same "
       "number of grammar books as the others, and the same number of dictionaries.",
}
# The briefs these replaced, as room.js held them: each must fail the text check when served.
OLD = {
    0: ("'A dial on the hinge side. It opens at the number of factors of the cupboard&rsquo;s asset number.'",
        "'A dial on the hinge side, numbered all the way round. It opens at the number of factors of the ' +\n"
        "             'cupboard&rsquo;s asset number.'"),
    2: ("'A brass slider across the handle. It opens at the largest number of identical bundles you can make ' +\n"
        "             'from the grammar books and the dictionaries, using every book. Identical means every bundle has the ' +\n"
        "             'same number of grammar books as the others, and the same number of dictionaries.'",
        "'A brass slider across the handle. Every bundle has the same number of grammar books and ' +\n"
        "             'dictionaries, and every book is used.'"),
}
NOWRAP = "#lockPanel .lock-brief { white-space: nowrap !important; }"

FIT = """() => { const out = [], b = document.querySelector('#lockPanel .lock-brief'),
    panel = b.closest('.panel'), r = b.getBoundingClientRect(), p = panel.getBoundingClientRect();
  if (r.left < p.left - 0.5 || r.right > p.right + 0.5)
    out.push('the brief spans ' + Math.round(r.left) + '-' + Math.round(r.right) + ' px, its panel ' +
             Math.round(p.left) + '-' + Math.round(p.right));
  if (b.scrollWidth > b.clientWidth + 1) out.push('the brief scrolls sideways (' + b.scrollWidth + ' > ' + b.clientWidth + ')');
  const d = document.documentElement;
  if (d.scrollWidth > window.innerWidth + 1) out.push('the page scrolls sideways (' + d.scrollWidth + ' > ' + window.innerWidth + ')');
  return out; }"""


def check(browser, base, room_js=None, css=None):
    """Every fault on the page, for each brief at each width. room_js / css replace or add to what is served."""
    faults = []
    for w, h in WIDTHS:
        ctx = browser.new_context(viewport={"width": w, "height": h})
        ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
        if room_js is not None:
            ctx.route(base + ROOM + "room.js", lambda r: r.fulfill(
                status=200, content_type="application/javascript", body=room_js))
        page = ctx.new_page()
        try:
            page.goto(base + ROOM, wait_until="load", timeout=20000)
            if css:
                page.add_style_tag(content=css)
            page.evaluate("() => localStorage.clear()")
            page.click("#startBtn")
            for i, want in BRIEFS.items():
                page.click('#lockBtns [data-lock="%d"]' % i)
                got = page.inner_text("#lockPanel .lock-brief").replace("\n", " ").strip()
                if got != want:
                    faults.append("lock %d at %d px: the brief reads %r, want %r" % (i + 1, w, got, want))
                for f in page.evaluate(FIT):
                    faults.append("lock %d at %d px: %s" % (i + 1, w, f))
        finally:
            ctx.close()
    return faults


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    from playwright.sync_api import sync_playwright
    room_js = (ROOT / "escape-rooms" / "comic-caper" / "room.js").read_text(encoding="utf-8")
    problems = []
    proc, base = ti._serve(ROOT)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for f in check(browser, base):
                problems.append(f)
            plants = [("lock %d's old brief" % (i + 1), dict(room_js=room_js.replace(new, old)))
                      for i, (new, old) in OLD.items()]
            plants.append(("each brief forced onto one line", dict(css=NOWRAP)))
            for name, kw in plants:
                if "room_js" in kw and kw["room_js"] == room_js:
                    problems.append("plant %r changed nothing: room.js no longer holds the brief it replaces" % name)
                    continue
                caught = check(browser, base, **kw)
                print("  plant %-34s %s" % (name, "caught (%s)" % caught[0][:90] if caught else "NOT CAUGHT"))
                if not caught:
                    problems.append("plant %r was not caught" % name)
            browser.close()
    finally:
        proc.terminate()
    print("The Comic Caper: lock 1 and lock 3 briefs at %s px" % ", ".join(str(w) for w, _ in WIDTHS))
    for f in problems:
        print("  FAIL  " + f)
    print("PASS" if not problems else "FAIL")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
