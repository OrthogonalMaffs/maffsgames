#!/usr/bin/env python3
"""Write the one page bar into every non-game site page. Idempotent: a second run changes nothing.

    python scripts/apply-page-bar.py            # write
    python scripts/apply-page-bar.py --dry-run  # report what would change

The canonical markup (bar_for()), the stylesheet link, the pages and the opt-outs all come from
scripts/check-page-bar.py, which holds every page to them in CI. For each page this:

  1. replaces a hand-copied <nav class="nav">...</nav> with the canonical bar, where the page has one;
  2. replaces any <nav class="page-bar">...</nav> with the canonical bar, or, on a page with neither, inserts it as
     the first element in <body>;
  3. links /schools/assets/page-bar.css once, just before </head>.

The pages under when-will-i-use-this/ are scripts/build-uses.py's output and are left to it (it writes the same bar
from the same bar_for()). The retired .nav CSS was removed by hand once (LEADERBOARD-PAGE); this script never edits
CSS. Then run scripts/apply-site-nav.py: every page with an a.back-link loads site-nav.js.

It refuses (exit 1, nothing written) on a page with more than one nav.nav or page bar: that needs a person.
"""
import argparse, importlib.util, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_page_bar", BASE / "scripts" / "check-page-bar.py")
cpb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cpb)

GENERATED = ("when-will-i-use-this/",)
NAV_BLOCK = re.compile(r'<nav\b[^>]*\bclass="(?:nav|page-bar)"[^>]*>.*?</nav>', re.S | re.I)


class Refuse(Exception):
    pass


def fix(rel, text):
    bar = cpb.bar_for(rel)
    blocks = NAV_BLOCK.findall(text)
    if len(blocks) > 1:
        raise Refuse("%s: %d nav.nav / page bars" % (rel, len(blocks)))
    if blocks:
        text = NAV_BLOCK.sub(lambda m: bar, text, count=1)
    else:
        body = cpb.BODY.search(text)
        if not body:
            raise Refuse("%s: no <body>" % rel)
        text = text[:body.end()] + "\n" + bar + "\n" + text[body.end():]
    if cpb.STYLESHEET not in text:
        at = text.lower().find("</head>")
        if at < 0:
            raise Refuse("%s: no </head>" % rel)
        text = text[:at] + cpb.STYLESHEET + "\n" + text[at:]
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    out = {}
    try:
        for rel, key in cpb.site_pages(BASE):
            if key or rel.startswith(GENERATED):
                continue
            path = BASE / rel
            with open(path, encoding="utf-8", newline="") as f:
                text = f.read()
            new = fix(rel, text)
            if new != text:
                out[path] = new
    except Refuse as e:
        print("REFUSED: %s (nothing written)" % e)
        return 1
    for path, new in out.items():
        print(("would write " if args.dry_run else "write ") + path.relative_to(BASE).as_posix())
        if not args.dry_run:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(new)
    print("%d page(s) %s." % (len(out), "would change" if args.dry_run else "changed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
