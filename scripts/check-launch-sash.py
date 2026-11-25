#!/usr/bin/env python3
# ci-line: Launch sash (the homepage's #announcements data: every item a valid end, the script hides it after; homepage only; planted faults caught) | --selftest
# ci-deps: schools/assets/launch-sash.js schools/assets/launch-sash.css index.html scripts/check-launch-sash.py
"""The homepage announcement strip is a time-limited claim, so every announcement must end itself (launch contract SIX-PS-LAUNCH,
Jon, 27 Oct 2026; data-driven since ANNOUNCE-STRIP, 25 Nov 2026).

    python scripts/check-launch-sash.py
    python scripts/check-launch-sash.py --selftest     # planted faults are caught
    python scripts/check-launch-sash.py --root <copy>  # testing

A figure on a page is a claim, and a claim with a date in it goes stale (the answer counts follow the same rule). The strip's
announcements are index.html's inline <script type="application/json" id="announcements"> block, {"items": [...]}. This fails when:
  - the homepage loads the strip but has no #announcements block, or the block is not JSON with an "items" list;
  - an item lacks a non-empty id, text or href, its href is not a path on this site ("/..."), its end is missing or not a valid
    ISO 8601 instant with a zone (2026-12-10T00:00:00Z), or it has a start that is not one;
  - schools/assets/launch-sash.js never compares an item's end with the clock before drawing (`Date.now() >= ends`);
  - any page but the homepage (index.html) loads the strip's script or its stylesheet: the strip is homepage only;
  - the script or its stylesheet is missing while the homepage loads it.
The dates themselves are not held to a value: an end is a decision, not a fault. An ended item may stay in the block (it is never
drawn) or be removed; with no item live the strip draws nothing.
"""
import argparse
import datetime
import json
import pathlib
import re
import shutil
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
JS = "schools/assets/launch-sash.js"
CSS = "schools/assets/launch-sash.css"
BLOCK = re.compile(r'<script\s+type="application/json"\s+id="announcements">(.*?)</script>', re.S)
INSTANT = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$")
COMPARE = re.compile(r"Date\.now\(\)\s*>=\s*ends")
USES = re.compile(r"launch-sash\.(js|css)")


def valid_instant(v):
    if not isinstance(v, str) or not INSTANT.match(v):
        return False
    try:
        datetime.datetime.fromisoformat(v.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def items_problems(home):
    """The #announcements block's faults, or the parsed items."""
    m = BLOCK.search(home)
    if not m:
        return ["index.html loads the strip but has no <script type=\"application/json\" id=\"announcements\"> block"], []
    try:
        data = json.loads(m.group(1))
    except ValueError as e:
        return ["index.html: #announcements is not valid JSON (%s)" % e], []
    items = data.get("items") if isinstance(data, dict) else None
    if not isinstance(items, list):
        return ['index.html: #announcements has no "items" list'], []
    out = []
    for i, it in enumerate(items):
        where = "index.html: announcement %d (%s)" % (i + 1, it.get("id") if isinstance(it, dict) else it)
        if not isinstance(it, dict):
            out.append("%s is not an object" % where)
            continue
        for k in ("id", "text", "href"):
            if not isinstance(it.get(k), str) or not it[k].strip():
                out.append("%s has no %s" % (where, k))
        href = it.get("href")
        if isinstance(href, str) and href and not (href.startswith("/") and not href.startswith("//")):
            out.append("%s: href %r is not a path on this site" % (where, href))
        if "end" not in it:
            out.append("%s has no end: it would never end itself" % where)
        elif not valid_instant(it["end"]):
            out.append("%s: end %r is not a valid ISO 8601 instant with a zone" % (where, it["end"]))
        if "start" in it and not valid_instant(it["start"]):
            out.append("%s: start %r is not a valid ISO 8601 instant with a zone" % (where, it["start"]))
    return out, items


def problems(root):
    out = []
    js = root / JS
    home = (root / "index.html").read_text(encoding="utf-8", errors="replace") if (root / "index.html").exists() else ""
    if not js.is_file():
        if USES.search(home):
            out.append("index.html loads the sash, but %s is missing" % JS)
    elif not COMPARE.search(js.read_text(encoding="utf-8")):
        out.append("%s never compares an item's end with the clock (Date.now() >= ends): an ended item would still show" % JS)
    if USES.search(home):
        out.extend(items_problems(home)[0])
        if not (root / CSS).is_file():
            out.append("index.html loads the sash stylesheet, but %s is missing" % CSS)
    for page in sorted(root.rglob("*.html")):
        rel = page.relative_to(root).as_posix()
        if rel == "index.html" or rel.startswith((".git/", "node_modules/")):
            continue
        if USES.search(page.read_text(encoding="utf-8", errors="replace")):
            out.append("%s loads the launch sash: it is for the homepage only" % rel)
    return out


def selftest():
    good_js = (BASE / JS).read_text(encoding="utf-8")
    good_home = (BASE / "index.html").read_text(encoding="utf-8")

    def home(d, fn):
        (d / "index.html").write_text(BLOCK.sub(lambda m: m.group(0).replace(m.group(1), fn(m.group(1))), good_home, count=1),
                                      encoding="utf-8", newline="")

    def item(fn):
        def edit(raw):
            data = json.loads(raw)
            fn(data["items"][0])
            return json.dumps(data)
        return edit

    cases = [
        ("the shipped files", lambda d: None, False),
        ("an item without an end", lambda d: home(d, item(lambda it: it.pop("end"))), True),
        ("an item whose end is not a date", lambda d: home(d, item(lambda it: it.update(end="2026-13-45T00:00:00Z"))), True),
        ("an item whose end has no zone", lambda d: home(d, item(lambda it: it.update(end="10 Dec 2026"))), True),
        ("an item whose link leaves the site", lambda d: home(d, item(lambda it: it.update(href="https://example.com/"))), True),
        ("the block missing", lambda d: (d / "index.html").write_text(BLOCK.sub("", good_home), encoding="utf-8", newline=""), True),
        ("the block not JSON", lambda d: home(d, lambda raw: raw[:-2]), True),
        ("the script drawing an item whose end has passed", lambda d: (d / JS).write_text(COMPARE.sub("false", good_js), encoding="utf-8", newline=""), True),
        ("the sash on another page", lambda d: (d / "about").mkdir() or (d / "about" / "index.html").write_text(
            '<script src="/schools/assets/launch-sash.js"></script>', encoding="utf-8", newline=""), True),
        ("the sash stylesheet on another page", lambda d: (d / "essentials").mkdir() or (d / "essentials" / "index.html").write_text(
            '<link rel="stylesheet" href="/schools/assets/launch-sash.css">', encoding="utf-8", newline=""), True),
        ("the homepage loading a sash whose script is gone", lambda d: (d / JS).unlink(), True),
    ]
    bad = []
    for name, plant, should_fail in cases:
        d = pathlib.Path(tempfile.mkdtemp(prefix="sash-check-"))
        try:
            (d / "schools/assets").mkdir(parents=True)
            shutil.copy(BASE / JS, d / JS)
            shutil.copy(BASE / CSS, d / CSS)
            shutil.copy(BASE / "index.html", d / "index.html")
            plant(d)
            got = bool(problems(d))
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if got != should_fail:
            bad.append("self-test: %s: %s" % (name, "failed" if got else "was NOT caught"))
    return bad, len(cases)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    bad, n = selftest()
    if a.selftest:
        print("\n".join(bad) if bad else "self-test: %d cases, each fault caught, the shipped files pass" % n)
        return 1 if bad else 0
    found = bad + problems(pathlib.Path(a.root).resolve())
    for f in found:
        print("FAIL  " + f)
    if found:
        return 1
    items = items_problems((BASE / "index.html").read_text(encoding="utf-8"))[1]
    print("OK  every announcement ends itself (%s), and only the homepage loads the strip; self-test %d cases"
          % (", ".join("%s until %s" % (it["id"], it["end"]) for it in items) or "none", n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
