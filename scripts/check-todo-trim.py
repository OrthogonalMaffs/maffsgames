#!/usr/bin/env python3
# ci-held: a one-off proof for contract TODO-TRIM's PR (20 Nov 2026); its output goes in that PR's body
"""Proves a trim of docs/todo.md lost nothing (contract TODO-TRIM, Jon 19 Nov 2026).

Compares the base's docs/todo.md (git show <base>:docs/todo.md, default origin/main) with the working tree's
docs/todo.md and docs/history/todo-done.md:

  - every row ID on the base's todo.md (a table row's first cell, and each numbered §4 item) is still in todo.md
    or was moved: the base's row line, or the §4 item's first line, is in todo-done.md word for word;
  - every sentence and table cell of the base's todo.md (whitespace collapsed; fragments under 25 characters are
    skipped) is still in todo.md or appears verbatim in todo-done.md;
  - it prints the bytes before and after, and the IDs moved and rewritten.

  python -X utf8 scripts/check-todo-trim.py [--base REF]      exit 1 on a lost ID or sentence
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROW = re.compile(r"^\| *([^|]+?) *\|")
ITEM = re.compile(r"^(\d+)\. ")
MIN_FRAGMENT = 25


def norm(s):
    return re.sub(r"\s+", " ", s)


def ids(text):
    """{id: the line that carries it}: table rows (not headers, separators or §3.9's batch tables) and §4 items."""
    out, sec = {}, ""
    for line in text.split("\n"):
        if line.startswith("## "):
            sec = line
        m = ROW.match(line)
        if m:
            k = m.group(1)
            if k not in ("#", "Batch") and not set(k) <= set("-: ") and not k.isdigit():
                out[k] = line
            continue
        m = ITEM.match(line)
        if m and sec.startswith("## 4."):
            out["§4 item " + m.group(1)] = line
    return out


def fragments(text):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+|\s*\|\s*", norm(text)) if len(f.strip()) >= MIN_FRAGMENT]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    a = ap.parse_args()
    old = subprocess.run(["git", "show", a.base + ":docs/todo.md"], cwd=ROOT, capture_output=True, text=True,
                         encoding="utf-8", check=True).stdout
    new = open(os.path.join(ROOT, "docs/todo.md"), encoding="utf-8").read()
    done = open(os.path.join(ROOT, "docs/history/todo-done.md"), encoding="utf-8").read()
    n_new, n_done = norm(new), norm(done)
    old_ids, new_ids = ids(old), ids(new)
    moved, rewritten, lost = [], [], []
    for k, line in old_ids.items():
        in_done = line in done
        if k in new_ids:
            if new_ids[k] != line:
                (rewritten if in_done else lost).append(k)
        elif in_done:
            moved.append(k)
        else:
            lost.append(k)
    gone = [f for f in fragments(old) if f not in n_new]
    lost_s = [f for f in gone if f not in n_done]
    print("docs/todo.md: %d bytes on %s, %d bytes now (%d fewer)"
          % (len(old.encode()), a.base, len(new.encode()), len(old.encode()) - len(new.encode())))
    print("Row IDs on %s: %d; still in todo.md: %d (%d rewritten, the old row word for word in todo-done.md); "
          "moved whole: %d" % (a.base, len(old_ids), len([k for k in old_ids if k in new_ids]), len(rewritten),
                               len(moved)))
    print("Moved: " + (", ".join(moved) or "none"))
    print("Rewritten: " + (", ".join(rewritten) or "none"))
    print("Sentences and cells removed from todo.md: %d; each found verbatim in todo-done.md: %d"
          % (len(gone), len(gone) - len(lost_s)))
    for k in lost:
        print("LOST ID: " + k)
    for f in lost_s:
        print("LOST SENTENCE: " + f[:200])
    print("FAILED" if lost or lost_s else "PASS: no ID or sentence lost")
    return 1 if lost or lost_s else 0


if __name__ == "__main__":
    sys.exit(main())
