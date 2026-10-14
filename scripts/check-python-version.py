#!/usr/bin/env python3
# ci-line: Python minimum (scripts/ require Python 3.10 or later: CI pins an explicit version, the shared-module guard fires below 3.10) | --selftest && --check
# ci-deps: .github/workflows/ scripts/bank_common.py
"""scripts/ require Python >= 3.10 (write_text newline=); this check keeps that true (contract PYTHON-MIN, 14 Oct 2026).

#390 put newline='' on every text-mode write in scripts/, including Path.write_text, whose newline= argument exists
only from Python 3.10. An older interpreter would fail with an obscure TypeError on a write path CI did not run.

  --check      every actions/setup-python step in .github/workflows/ pins an explicit python-version of 3.10 or
               later (no 3.x, no 3, no unpinned step)
  --selftest   scripts/bank_common.require_python (imported by most scripts) exits with a message naming the
               minimum when sys.version_info is monkeypatched to (3, 9), and stays quiet at 3.10 and at the real
               version; the workflow reader fails an unpinned, a floating and a 3.9 step

The guard lives in bank_common, which 120 of the 181 scripts import; the rest have no shared import and are not
guarded (listed in docs/handover/home.md).
"""
import glob
import os
import re
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
MIN = (3, 10)


def pins(text):
    """[(line, value or None)] for each actions/setup-python step in a workflow's text."""
    out, lines = [], text.split("\n")
    for i, l in enumerate(lines):
        if re.search(r"uses:\s*actions/setup-python@", l):
            indent = len(l) - len(l.lstrip())
            val = None
            for m in lines[i + 1:i + 8]:
                if m.strip() and len(m) - len(m.lstrip()) < indent:
                    break
                g = re.match(r"\s*python-version:\s*[\"']?([^\"'\s#]+)", m)
                if g:
                    val = g.group(1)
                    break
            out.append((i + 1, val))
    return out


def fault_of(val):
    if val is None:
        return "no python-version (an unpinned step takes whatever the runner has)"
    g = re.fullmatch(r"(\d+)\.(\d+)(?:\.\d+)?", val)
    if not g:
        return "python-version %r is floating, not an explicit version" % val
    if (int(g.group(1)), int(g.group(2))) < MIN:
        return "python-version %s is below %d.%d" % (val, MIN[0], MIN[1])
    return None


def check():
    faults, n = [], 0
    for f in sorted(glob.glob(os.path.join(ROOT, ".github", "workflows", "*.y*ml"))):
        with open(f, encoding="utf-8", newline="") as fh:
            for line, val in pins(fh.read()):
                n += 1
                bad = fault_of(val)
                print("  %s:%d  python-version %s" % (os.path.basename(f), line, val))
                if bad:
                    faults.append("%s:%d %s" % (os.path.basename(f), line, bad))
    if n == 0:
        faults.append("no actions/setup-python step found in .github/workflows/")
    return faults


def selftest():
    import bank_common
    fails = []

    def case(name, ok):
        print("  %s  %s" % ("ok    " if ok else "WRONG ", name))
        if not ok:
            fails.append(name)

    with mock.patch.object(sys, "version_info", (3, 9, 18, "final", 0)):
        try:
            bank_common.require_python()
            case("the guard fires under a monkeypatched Python 3.9", False)
        except SystemExit as e:
            msg = str(e)
            case("the guard fires under a monkeypatched Python 3.9", "3.10" in msg and "3.9" in msg)
    with mock.patch.object(sys, "version_info", (3, 10, 0, "final", 0)):
        try:
            bank_common.require_python()
            case("the guard stays quiet under 3.10", True)
        except SystemExit:
            case("the guard stays quiet under 3.10", False)
    try:
        bank_common.require_python()
        case("the guard stays quiet on the running interpreter", True)
    except SystemExit:
        case("the guard stays quiet on the running interpreter", False)
    wf = "jobs:\n  a:\n    steps:\n      - uses: actions/setup-python@v5\n        with:\n          python-version: %s\n"
    case("a 3.12 step passes", fault_of(pins(wf % '"3.12"')[0][1]) is None)
    case("a 3.9 step fails", fault_of(pins(wf % '"3.9"')[0][1]) is not None)
    case("a floating 3.x step fails", fault_of(pins(wf % '"3.x"')[0][1]) is not None)
    case("an unpinned step fails", fault_of(pins("      - uses: actions/setup-python@v5\n      - run: x\n")[0][1]) is not None)
    print("SELFTEST %s" % ("PASS" if not fails else "FAIL: " + ", ".join(fails)))
    return 1 if fails else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    faults = check()
    for f in faults:
        print("FAIL: " + f)
    print("FAILED" if faults else "PASS")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
