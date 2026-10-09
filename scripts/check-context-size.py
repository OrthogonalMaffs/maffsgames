#!/usr/bin/env python3
# ci-line: Context size (CLAUDE.md and both handovers at most 20 KB; contract CTX) | --selftest && --check
"""What every Claude Code session loads before it starts work stays small (contract CTX, 8 Oct 2026).

CLAUDE.md loads into every session in both lanes, and each lane reads its handover first. On 8 Oct 2026 they
were 159 KB, 64 KB and 56 KB, so a fresh session started at 16% context before reading its task. History now
lives in docs/history/ (never loaded by default) and this check holds the three files to LIMIT bytes each, a
little above the 15 KB target so a normal entry fits. Prints every file's size.
docs/handover/contracts/ is deliberately not measured: it is read only when an item starts, never at session
start (canon §7.8.2, contract CONTRACTS-FOLDER).

DEFERRED: a file whose trim the contract itself put off. It is reported, not failed, and it fails once it is
under the limit while still listed, so the exemption cannot outlive the trim.

  python scripts/check-context-size.py --check      the repo
  python scripts/check-context-size.py --selftest   planted files in a scratch folder: a 25 KB CLAUDE.md fails
"""
import argparse
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 20 * 1024
FILES = ["CLAUDE.md", "docs/handover/home.md", "docs/handover/cloud.md"]
DEFERRED = {}


def check(root, deferred):
    """[fault] for the files under root; prints one line per file."""
    faults = []
    for f in FILES:
        p = os.path.join(root, f)
        if not os.path.exists(p):
            faults.append("%s: missing" % f)
            continue
        n = os.path.getsize(p)
        over = n > LIMIT
        if f in deferred:
            if over:
                print("  DEFERRED  %-24s %7d bytes (limit %d): %s" % (f, n, LIMIT, deferred[f]))
            else:
                print("  FAIL      %-24s %7d bytes: under the limit but still DEFERRED" % (f, n))
                faults.append("%s is %d bytes, under the limit: remove it from DEFERRED" % (f, n))
            continue
        print("  %s  %-24s %7d bytes (limit %d)" % ("FAIL    " if over else "ok      ", f, n, LIMIT))
        if over:
            faults.append("%s is %d bytes, over the %d-byte limit: move history to docs/history/ (contract CTX)"
                          % (f, n, LIMIT))
    return faults


def selftest():
    fails = []
    tmp = tempfile.mkdtemp(prefix="ctxsize-")
    try:
        def plant(sizes):
            for f in FILES:
                p = os.path.join(tmp, f)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write("x" * sizes.get(f, 1000))

        def case(name, sizes, deferred, want_fail):
            plant(sizes)
            print(" %s:" % name)
            got = bool(check(tmp, deferred))
            ok = got == want_fail
            print("  %s  %s" % ("caught" if want_fail and ok else "passed" if ok else "WRONG ", name))
            if not ok:
                fails.append(name)

        case("a planted 25 KB CLAUDE.md fails", {"CLAUDE.md": 25 * 1024}, {}, True)
        case("a planted 25 KB home.md fails", {"docs/handover/home.md": 25 * 1024}, {}, True)
        case("files at the limit pass", {f: LIMIT for f in FILES}, {}, False)
        case("a deferred file over the limit is reported, not failed", {"docs/handover/cloud.md": 60 * 1024},
             {"docs/handover/cloud.md": "test"}, False)
        case("a deferred file under the limit fails (the exemption is stale)", {"docs/handover/cloud.md": 9000},
             {"docs/handover/cloud.md": "test"}, True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST %s" % ("PASS" if not fails else "FAIL: " + ", ".join(fails)))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="check the repo (the default)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print("Context size (contract CTX): every file at most %d bytes" % LIMIT)
    faults = check(ROOT, DEFERRED)
    for f in faults:
        print("FAIL: " + f)
    print("FAILED" if faults else "PASS")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
