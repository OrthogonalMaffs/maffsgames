#!/usr/bin/env python3
# ci-line: Launch sash (schools/assets/launch-sash.js carries an end date and hides itself after it; homepage only; planted faults caught) | --selftest
# ci-deps: schools/assets/launch-sash.js schools/assets/launch-sash.css index.html scripts/check-launch-sash.py
"""The "100 games" sash is a time-limited claim, so it must end itself (launch contract SIX-PS-LAUNCH, Jon, 27 Oct 2026).

    python scripts/check-launch-sash.py
    python scripts/check-launch-sash.py --selftest     # planted faults are caught
    python scripts/check-launch-sash.py --root <copy>  # testing

A figure on a page is a claim, and a claim with a date in it goes stale (the answer counts follow the same rule). This fails when:
  - schools/assets/launch-sash.js has no END date (a quoted ISO 8601 instant, `var END = '2026-11-10T00:00:00Z'`), or the date is
    not valid, or the script never compares it with the clock and returns before drawing anything (`Date.now() >= ends`);
  - any page but the homepage (index.html) loads the sash script or its stylesheet: the sash is homepage only;
  - the script or its stylesheet is missing while the homepage loads it.
The date itself is not held to a value: Jon's 10 Nov 2026 is the shipped one, and a later one is a decision, not a fault.
After the end date the files may be deleted with the homepage's two lines.
"""
import argparse
import datetime
import pathlib
import re
import shutil
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
JS = "schools/assets/launch-sash.js"
CSS = "schools/assets/launch-sash.css"
END = re.compile(r"""var\s+END\s*=\s*['"]([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+(?:Z|[+-][0-9]{2}:[0-9]{2}))['"]""")
COMPARE = re.compile(r"Date\.now\(\)\s*>=\s*ends")
USES = re.compile(r"launch-sash\.(js|css)")


def problems(root):
    out = []
    js = root / JS
    home = (root / "index.html").read_text(encoding="utf-8", errors="replace") if (root / "index.html").exists() else ""
    if not js.is_file():
        if USES.search(home):
            out.append("index.html loads the sash, but %s is missing" % JS)
    else:
        src = js.read_text(encoding="utf-8")
        m = END.search(src)
        if not m:
            out.append("%s has no END date (var END = '2026-11-10T00:00:00Z'): the sash would never end itself" % JS)
        else:
            try:
                datetime.datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
            except ValueError:
                out.append("%s: END %r is not a valid ISO 8601 instant" % (JS, m.group(1)))
        if not COMPARE.search(src):
            out.append("%s never compares END with the clock (Date.now() >= ends): it would show for ever" % JS)
    if USES.search(home) and not (root / CSS).is_file():
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
    cases = [
        ("the shipped files", lambda d: None, False),
        ("a sash with no end date", lambda d: (d / JS).write_text(END.sub("var END_GONE = 0", good_js), encoding="utf-8", newline=""), True),
        ("an end date that is not a date", lambda d: (d / JS).write_text(good_js.replace("2026-11-10T00:00:00Z", "2026-13-45T00:00:00Z"), encoding="utf-8", newline=""), True),
        ("a sash that never compares the clock", lambda d: (d / JS).write_text(COMPARE.sub("false", good_js), encoding="utf-8", newline=""), True),
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
    print("OK  the sash ends itself (%s), and only the homepage loads it; self-test %d cases" % (END.search((BASE / JS).read_text(encoding="utf-8")).group(1), n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
