#!/usr/bin/env python3
"""Write schools/assets/launch-dates.json: each game's and room's launch date (contract UGH-STATS-QUESTIONS, 14 Nov 2026).

One-off, kept for audit. Every games/<slug>/ and escape-rooms/<slug>/ directory with an index.html gets
{"<slug>": "YYYY-MM-DD"}: the UK date of the commit that first added that index.html in this repository.
This repository starts on 2 October 2026 with a fresh tree, so a page first added that day was older: for those
the date is the first commit adding the same path in OrthogonalMaffs/maffsgames-archive, read from a local
clone (--archive DIR) or from a saved log of one (--archive-log FILE, made with
  git log --diff-filter=A --format='@%aI' --name-only -- 'games/*/index.html' 'escape-rooms/*/index.html'
). A page found in neither keeps 2026-10-02 and is listed on stderr.

From now on a new game adds its own line at launch; scripts/check-ugh-stats.py fails a directory with no entry.

    python3 scripts/build-launch-dates.py --archive ../maffsgames-archive
    python3 scripts/build-launch-dates.py --archive-log adds.txt
"""
import argparse
import datetime
import glob
import json
import os
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "schools", "assets", "launch-dates.json")
FRESH = "2026-10-02"
UK = ZoneInfo("Europe/London")
PATTERNS = ["games/*/index.html", "escape-rooms/*/index.html"]


def uk_date(iso):
    return datetime.datetime.fromisoformat(iso).astimezone(UK).date().isoformat()


def first_adds(lines):
    """Parse `git log --format=@<iso> --name-only` (newest first) into {path: earliest UK date}."""
    out, when = {}, None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("@"):
            when = uk_date(line[1:])
        elif when:
            out[line] = when      # newest first, so the last write is the earliest add
    return out


def git_adds(repo):
    cmd = ["git", "-C", repo, "log", "--diff-filter=A", "--format=@%aI", "--name-only", "--"] + PATTERNS
    return first_adds(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.splitlines())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--archive", help="a local clone of OrthogonalMaffs/maffsgames-archive")
    src.add_argument("--archive-log", help="a saved git log of that clone (see the docstring)")
    args = ap.parse_args()

    here = git_adds(ROOT)
    if args.archive:
        old = git_adds(args.archive)
    else:
        with open(args.archive_log, encoding="utf-8") as f:
            old = first_adds(f.read().splitlines())

    dates, missing, from_archive = {}, [], 0
    for pattern in PATTERNS:
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            slug = rel.split("/")[1]
            d = here.get(rel)
            if d is None:
                print("not committed yet: " + rel, file=sys.stderr)
                continue
            if d == FRESH:
                if rel in old:
                    d = old[rel]
                    from_archive += 1
                else:
                    missing.append(rel)
            dates[slug] = d

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(dates.items())), f, indent=1)
        f.write("\n")
    print("wrote %s: %d entries, %d dated from the archive, %d kept at %s"
          % (os.path.relpath(OUT, ROOT), len(dates), from_archive, len(missing), FRESH))
    for rel in missing:
        print("  in neither history, kept at %s: %s" % (FRESH, rel))


if __name__ == "__main__":
    main()
