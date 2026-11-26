#!/usr/bin/env python3
"""Write the large-screen layer's tag into every page on check-large-screen.py's MIGRATED list. Idempotent: a second
run changes nothing (SR-34's goal; contract LARGE-SCREEN-LAYER, 26 Nov 2026; from the parked pilot's script).

    python -X utf8 scripts/apply-large-screen.py            # write
    python -X utf8 scripts/apply-large-screen.py --dry-run  # report what would change

The lists come from scripts/check-large-screen.py, which holds every page to them in CI; each page's measured height
need comes from data/large-screen.json (scripts/measure-large-screen.py writes it). For each MIGRATED page this:

  1. writes <script src="/schools/assets/large-screen.js" data-need="N" data-pointer="P"></script> once, on its own
     line just before </head>, or brings an existing tag's two values up to date: N is the data's need, P is "none",
     "verified" or "held" as the check works it out from the page's scripts and its POINTER_VERIFIED list;
  2. OPT_OUT: adds data-large-screen="off" to the page's <html> tag if it is not there.

It refuses (exit 1, nothing written) on a page with no </head> or no <html> tag, one carrying the tag more than once,
or one with no entry in data/large-screen.json: those need a person, or a measurement. It never removes a tag: taking
a page off MIGRATED is a hand edit, reviewed. It touches nothing else in a page.
"""
import argparse
import importlib.util
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_large_screen", BASE / "scripts" / "check-large-screen.py")
cl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cl)

HTML_TAG = re.compile(r"<html\b", re.I)


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def plan(rel, src, data):
    """The page's new text, or src unchanged. Raises ValueError where a person is needed."""
    entry = data.get(rel)
    if entry is None or type(entry.get("need")) is not int:
        raise ValueError("%s has no measured need in %s (run scripts/measure-large-screen.py)" % (rel, cl.DATA))
    tag = cl.tag_for(entry["need"], cl.pointer_status(rel, cl.page_facts(BASE, rel)))
    out = src
    found = cl.TAG_RE.findall(out)
    if len(found) > 1:
        raise ValueError("%s carries the %s tag %d times" % (rel, cl.LAYER_URL, len(found)))
    if len(found) == 1:
        out = out.replace(found[0], tag)
    else:
        i = out.lower().find("</head>")
        if i < 0:
            raise ValueError("%s has no </head>" % rel)
        nl = "\r\n" if "\r\n" in out else "\n"
        out = out[:i] + tag + nl + out[i:]
    if rel in cl.OPT_OUT and not cl.OFF.search(out):
        if not HTML_TAG.search(out):
            raise ValueError("%s has no <html> tag" % rel)
        out = HTML_TAG.sub('<html data-large-screen="off"', out, count=1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    data = cl.load_data(BASE)
    changes = {}
    try:
        for rel in cl.MIGRATED:
            path = BASE / rel
            src = cl.read(path)
            out = plan(rel, src, data)
            if out != src:
                changes[path] = out
    except (OSError, ValueError) as e:
        print("REFUSED (nothing written):", e)
        return 1
    for path, out in changes.items():
        print("%s %s" % ("would change" if args.dry_run else "changed", path.relative_to(BASE).as_posix()))
        if not args.dry_run:
            write(path, out)
    print("apply-large-screen: %d page(s) %s" % (len(changes), "to change" if args.dry_run else "changed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
