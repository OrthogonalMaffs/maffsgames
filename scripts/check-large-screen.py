#!/usr/bin/env python3
"""The large-screen layer: who links it, who opts out, and its steps (canon §7.5.8, SR-34; contract
LARGE-SCREEN-PILOT, Jon, 20 Nov 2026).

    python -X utf8 scripts/check-large-screen.py              # check the repository
    python -X utf8 scripts/check-large-screen.py --selftest   # plant faults in temporary copies; each must be caught

schools/assets/large-screen.css scales a page up with CSS zoom on large viewports only. A page gets it by linking it
once before </head> (scripts/apply-large-screen.py writes the link, from the lists below). Fails when:

  1. a MIGRATED page does not link the stylesheet, links it more than once, or links it outside <head>;
  2. any .html page carries data-large-screen="off" without an OPT_OUT entry (with its reason), or an OPT_OUT entry's
     page does not carry it, is not MIGRATED, or does not exist;
  3. a step in the stylesheet breaks the rule: zoom at a viewport below 1500 x 880, or a step whose smallest viewport
     leaves less than 1200 x 760 CSS px after zoom (min-width / zoom < 1200 or min-height / zoom < 760), or a step
     not above 1;
  4. a page not on MIGRATED links the stylesheet (the rollout adds pages here, never by hand-linking).

--selftest plants, each of which must fail the check (plant_common: a plant that did not apply is a STALE PLANT and
fails the run): a MIGRATED page without the link; an unlisted opt-out; a MIGRATED page linking it twice; a step that
breaks the rule; an unlisted page linking it.
"""
import argparse
import pathlib
import re
import shutil
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import plant_common as pc  # noqa: E402

STYLESHEET = "/schools/assets/large-screen.css"
LINK = '<link rel="stylesheet" href="%s">' % STYLESHEET
CSS_PATH = "schools/assets/large-screen.css"

# Pages that link the layer. The pilot's six (Jon, 20 Nov 2026); the rest join in the rollout (todo
# LARGE-SCREEN-ROLLOUT), never by hand-linking.
MIGRATED = [
    "games/maffscards/index.html",
    "games/factor-race/index.html",
    "games/surd-simplifier/index.html",
    "games/negative-number-line/index.html",
    "games/bearing-blitz/index.html",
    "games/core-maths-paper1/index.html",
]

# Pages that carry <html data-large-screen="off">, each with its reason. An opted-out game lays itself out for large
# screens on its own (SR-34); each entry has a todo row.
OPT_OUT = {}

STEP = re.compile(r"@media\s*\(\s*min-width:\s*(\d+)px\s*\)\s*and\s*\(\s*min-height:\s*(\d+)px\s*\)\s*\{\s*"
                  r"html:not\(\[data-large-screen=\"off\"\]\)\s*\{\s*--maffs-large-zoom:\s*([0-9.]+)\s*;\s*\}\s*\}")
ZOOM_GATE = re.compile(r"@media\s*\(\s*min-width:\s*(\d+)px\s*\)\s*and\s*\(\s*min-height:\s*(\d+)px\s*\)\s*\{\s*"
                       r"html:not\(\[data-large-screen=\"off\"\]\)\s*\{\s*zoom:\s*var\(--maffs-large-zoom\)")
OFF = re.compile(r"<html\b[^>]*\bdata-large-screen\s*=\s*[\"']off[\"']", re.I)
LINK_RE = re.compile(r"<link\b[^>]*href=[\"']%s[\"'][^>]*>" % re.escape(STYLESHEET), re.I)
SKIP_DIRS = {".git", "node_modules", "_site", "vendor"}

MIN_W, MIN_H, EFF_W, EFF_H = 1500, 880, 1200, 760


def html_pages(root):
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        yield rel.as_posix(), p


def check(root):
    """Every failure as a line of text; empty when the tree passes."""
    fails = []
    css_file = root / CSS_PATH
    if not css_file.is_file():
        return ["%s does not exist" % CSS_PATH]
    css = css_file.read_text(encoding="utf-8")
    steps = [(int(w), int(h), float(z)) for w, h, z in STEP.findall(css)]
    if not steps:
        fails.append("%s: no zoom steps found" % CSS_PATH)
    for w, h, z in steps:
        if z <= 1:
            fails.append("%s: step %.2f at %dx%d is not above 1" % (CSS_PATH, z, w, h))
        if w < MIN_W or h < MIN_H:
            fails.append("%s: step %.2f starts at %dx%d, below %dx%d" % (CSS_PATH, z, w, h, MIN_W, MIN_H))
        if w / z < EFF_W - 1e-9 or h / z < EFF_H - 1e-9:
            fails.append("%s: step %.2f at %dx%d leaves %.0fx%.0f CSS px, under %dx%d"
                         % (CSS_PATH, z, w, h, w / z, h / z, EFF_W, EFF_H))
    gates = [(int(w), int(h)) for w, h in ZOOM_GATE.findall(css)]
    if len(gates) != 1:
        fails.append("%s: expected one rule applying zoom, found %d" % (CSS_PATH, len(gates)))
    elif steps and gates[0] != (min(w for w, _, _ in steps), min(h for _, h, _ in steps)):
        fails.append("%s: the zoom rule's gate %dx%d is not the smallest step's viewport" % ((CSS_PATH,) + gates[0]))
    elif gates[0][0] < MIN_W or gates[0][1] < MIN_H:
        fails.append("%s: zoom applies from %dx%d, below %dx%d" % (CSS_PATH, gates[0][0], gates[0][1], MIN_W, MIN_H))

    pages = dict(html_pages(root))
    for rel in MIGRATED:
        p = pages.get(rel)
        if p is None:
            fails.append("%s: on MIGRATED but does not exist" % rel)
            continue
        src = p.read_text(encoding="utf-8")
        links = LINK_RE.findall(src)
        if len(links) != 1:
            fails.append("%s: links %s %d times (expected once)" % (rel, STYLESHEET, len(links)))
            continue
        head_end = src.lower().find("</head>")
        if head_end < 0 or LINK_RE.search(src).start() > head_end:
            fails.append("%s: the %s link is not inside <head>" % (rel, STYLESHEET))
    for rel, p in pages.items():
        src = p.read_text(encoding="utf-8")
        if rel not in MIGRATED and LINK_RE.search(src):
            fails.append("%s: links %s but is not on MIGRATED (run apply-large-screen.py from the lists)"
                         % (rel, STYLESHEET))
        if OFF.search(src) and rel not in OPT_OUT:
            fails.append('%s: carries data-large-screen="off" with no OPT_OUT entry and reason' % rel)
    for rel, reason in OPT_OUT.items():
        if not reason.strip():
            fails.append("%s: OPT_OUT entry has no reason" % rel)
        p = pages.get(rel)
        if p is None:
            fails.append("%s: on OPT_OUT but does not exist" % rel)
            continue
        if rel not in MIGRATED:
            fails.append("%s: on OPT_OUT but not MIGRATED" % rel)
        if not OFF.search(p.read_text(encoding="utf-8")):
            fails.append('%s: on OPT_OUT but its <html> does not carry data-large-screen="off"' % rel)
    return fails


def selftest():
    """Each plant, in a temporary copy of the pages the check reads, must produce a failure; the clean copy none."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="large-screen-selftest-"))
    try:
        def fresh():
            dst = tmp / "tree"
            if dst.exists():
                shutil.rmtree(dst)
            (dst / "schools/assets").mkdir(parents=True)
            shutil.copy(BASE / CSS_PATH, dst / CSS_PATH)
            for rel in MIGRATED + ["games/formula-forge/index.html"]:
                (dst / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(BASE / rel, dst / rel)
            return dst

        def edit(root, rel, old, new, name, regex=False):
            f = root / rel
            src = f.read_text(encoding="utf-8")
            out = pc.apply_re_plant(src, old, new, name=name) if regex else pc.apply_plant(src, old, new, name=name)
            f.write_text(out, encoding="utf-8", newline="")

        plain = [p for p in MIGRATED if p not in OPT_OUT]
        plants = [
            ("a MIGRATED page without the link",
             lambda r: edit(r, plain[0], LINK, "", "the link removed")),
            ("an unlisted opt-out",
             lambda r: edit(r, plain[1], r"<html\b", '<html data-large-screen="off"', "an unlisted opt-out",
                            regex=True)),
            ("a MIGRATED page linking it twice",
             lambda r: edit(r, plain[2], LINK, LINK + "\n" + LINK, "the link doubled")),
            ("a step that breaks the rule (1.6 at 2200x1200 leaves 1375x750)",
             lambda r: edit(r, CSS_PATH, "(min-width: 1920px) and (min-height: 1216px)",
                            "(min-width: 2200px) and (min-height: 1200px)", "the contract's starting 1.6 step")),
            ("an unlisted page linking it",
             lambda r: edit(r, "games/formula-forge/index.html", "</head>", LINK + "\n</head>",
                            "a hand-linked page")),
        ]
        bad = []
        clean = check(fresh())
        if clean:
            bad.append("the clean copy fails: %s" % clean)
        for name, plant in plants:
            root = fresh()
            try:
                plant(root)
            except pc.StalePlant as e:
                bad.append(str(e))
                continue
            found = check(root)
            print("  %-62s %s" % (name, "CAUGHT" if found else "MISSED"))
            if not found:
                bad.append("plant not caught: " + name)
        return bad
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        bad = selftest()
        for b in bad:
            print("FAIL:", b)
        print("check-large-screen selftest: %s" % ("FAIL" if bad else "PASS, all plants caught"))
        return 1 if bad else 0
    fails = check(BASE)
    for f in fails:
        print("FAIL:", f)
    print("check-large-screen: %s (%d MIGRATED, %d OPT_OUT)"
          % ("FAIL" if fails else "PASS", len(MIGRATED), len(OPT_OUT)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
