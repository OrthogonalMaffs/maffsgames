#!/usr/bin/env python3
"""Link the large-screen layer into every page on check-large-screen.py's lists. Idempotent: a second run changes
nothing (canon §7.5.8, SR-34; contract LARGE-SCREEN-PILOT, Jon, 20 Nov 2026).

    python -X utf8 scripts/apply-large-screen.py            # write
    python -X utf8 scripts/apply-large-screen.py --dry-run  # report what would change

The lists come from scripts/check-large-screen.py, which holds every page to them in CI. For each page this:

  1. MIGRATED: links /schools/assets/large-screen.css once, on its own line just before </head> (a page that
     already links it once is left alone);
  2. OPT_OUT: adds data-large-screen="off" to the page's <html> tag if it is not there.

It refuses (exit 1, nothing written) on a page with no </head> or no <html> tag, or one linking the stylesheet more
than once: those need a person. It never removes a link: taking a page off MIGRATED is a hand edit, reviewed.
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


def read(path):
    with open(path, encoding="utf-8", newline="") as f:   # keep line endings as they are
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def plan(rel, src):
    """The page's new text, or src unchanged. Raises ValueError where a person is needed."""
    out = src
    n = len(cl.LINK_RE.findall(out))
    if n > 1:
        raise ValueError("%s links %s %d times" % (rel, cl.STYLESHEET, n))
    if n == 0:
        i = out.lower().find("</head>")
        if i < 0:
            raise ValueError("%s has no </head>" % rel)
        nl = "\r\n" if "\r\n" in out else "\n"
        out = out[:i] + cl.LINK + nl + out[i:]
    if rel in cl.OPT_OUT and not cl.OFF.search(out):
        if not HTML_TAG.search(out):
            raise ValueError("%s has no <html> tag" % rel)
        out = HTML_TAG.sub('<html data-large-screen="off"', out, count=1)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    changes = {}
    try:
        for rel in cl.MIGRATED:
            path = BASE / rel
            src = read(path)
            out = plan(rel, src)
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
