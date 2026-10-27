#!/usr/bin/env python3
# ci-line: Context size (CLAUDE.md and both handovers at most 20 KB, docs/todo.md at most 150 KB; canon reported; contracts CTX and TODO-SLIM) | --selftest && --check
"""What every Claude Code session loads before it starts work stays small (contract CTX, 8 Oct 2026).

CLAUDE.md loads into every session in both lanes, and each lane reads its handover first. On 8 Oct 2026 they
were 159 KB, 64 KB and 56 KB, so a fresh session started at 16% context before reading its task. History now
lives in docs/history/ (never loaded by default) and this check holds the three files to LIMIT bytes each, a
little above the 15 KB target so a normal entry fits. Prints every file's size.
docs/handover/contracts/ is deliberately not measured: it is read only when an item starts, never at session
start (canon §7.8.2, contract CONTRACTS-FOLDER).

docs/todo.md has its own cap, TODO_LIMIT (contract TODO-SLIM, 10 Oct 2026): every lane reads its head, and at
482 KB it was the one shared file free to grow. Finished work moves to docs/history/todo-done.md word for word.
The cap was set at the slimmed size plus a little headroom; LOWER IT as open items close. docs/canon.md is
reported with its size, not capped (for Jon to consider).

A HANDOVER ARCHIVES ITSELF (GATE-WARN-THEN-ENFORCE step 5, Jon 27 Oct 2026; canon 7.8.4): the 20 KB limit failed a Gate
twice on 27 Oct, each time on a lane that had only added its own entry. Now a handover over the limit is a WARNING when
--fix can bring it back: --fix moves its oldest dated entries ("## " sections, from the bottom; never the newest) to the
top of that lane's docs/history/handover-<lane>-archive.md, unchanged and newest first, until the handover is at most
TARGET bytes (HEADROOM under the limit, so a normal entry fits). Main's "Regenerate REGISTER.md (main only)" job runs
--fix after every merge and commits what it moved. A handover still over the limit with nothing to move (its preamble
alone) still fails, and so do CLAUDE.md and docs/todo.md: they have no entries to archive.

DEFERRED: a file whose trim the contract itself put off. It is reported, not failed, and it fails once it is
under the limit while still listed, so the exemption cannot outlive the trim.

  python scripts/check-context-size.py --check      the repo
  python scripts/check-context-size.py --fix        archive the oldest handover entries past the limit (step 5)
  python scripts/check-context-size.py --selftest   planted files in a scratch folder: a 25 KB CLAUDE.md fails,
                                                    a todo.md over its cap fails
"""
import argparse
import datetime
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 20 * 1024
TODO_LIMIT = 150 * 1024          # TODO-SLIM: 145 KB after the slim (10 Oct 2026); lower it as items close
FILES = ["CLAUDE.md", "docs/handover/home.md", "docs/handover/cloud.md", "docs/todo.md"]
LIMITS = {"docs/todo.md": TODO_LIMIT}
REPORTED = ["docs/canon.md"]     # size printed, never failed
DEFERRED = {}
HANDOVERS = {"docs/handover/home.md": "docs/history/handover-home-archive.md",
             "docs/handover/cloud.md": "docs/history/handover-cloud-archive.md"}
HEADROOM = 3 * 1024              # --fix stops at LIMIT - HEADROOM, so the next entry fits
TARGET = LIMIT - HEADROOM


def split_entries(text):
    """(preamble, [entry]): a handover's text before its first "## " heading, and each "## " section, in file order
    (newest first). Joining them gives the text back."""
    starts = [i for i in range(len(text)) if text.startswith("## ", i) and (i == 0 or text[i - 1] == "\n")]
    if not starts:
        return text, []
    return text[:starts[0]], [text[a:b] for a, b in zip(starts, starts[1:] + [len(text)])]


def movable(text, target=None):
    """How many of the oldest entries --fix moves to bring the text to at most `target` bytes (the newest entry always
    stays), and whether that gets it there."""
    target = TARGET if target is None else target
    pre, entries = split_entries(text)
    k = 0
    while len("".join([pre] + entries[:len(entries) - k]).encode("utf-8")) > target and k < len(entries) - 1:
        k += 1
    return k, len("".join([pre] + entries[:len(entries) - k]).encode("utf-8")) <= LIMIT


def archive(root, handover, archive_path, today=None, target=None):
    """Move the oldest entries of `handover` (repo-relative) past `target` bytes to the top of `archive_path`, under a dated
    heading, unchanged. Returns the number of entries moved."""
    hp, ap = os.path.join(root, handover), os.path.join(root, archive_path)
    text = open(hp, encoding="utf-8", newline="").read()
    k, _ = movable(text, target)
    if not k:
        return 0
    pre, entries = split_entries(text)
    keep, moved = entries[:len(entries) - k], entries[len(entries) - k:]
    old = open(ap, encoding="utf-8", newline="").read() if os.path.exists(ap) else "# Archive\n\n"
    apre, aentries = split_entries(old)
    block = "## Moved %s by check-context-size.py --fix from %s (history, unchanged)\n\n" % (
        today or datetime.date.today().isoformat(), handover)
    body = "".join(moved)
    body += "\n" * (2 - (len(body) - len(body.rstrip("\n"))) if aentries else 0)
    with open(ap, "w", encoding="utf-8", newline="") as f:
        f.write(apre + block + body + "".join(aentries))
    with open(hp, "w", encoding="utf-8", newline="") as f:
        f.write("".join([pre] + keep))
    return k


def check(root, deferred):
    """[fault] for the files under root; prints one line per file."""
    faults = []
    for f in FILES:
        p = os.path.join(root, f)
        if not os.path.exists(p):
            faults.append("%s: missing" % f)
            continue
        n = os.path.getsize(p)
        limit = LIMITS.get(f, LIMIT)
        over = n > limit
        if f in deferred:
            if over:
                print("  DEFERRED  %-24s %7d bytes (limit %d): %s" % (f, n, limit, deferred[f]))
            else:
                print("  FAIL      %-24s %7d bytes: under the limit but still DEFERRED" % (f, n))
                faults.append("%s is %d bytes, under the limit: remove it from DEFERRED" % (f, n))
            continue
        if over and f in HANDOVERS and movable(open(p, encoding="utf-8", newline="").read())[1]:
            print("  WARN      %-24s %7d bytes (limit %d): --fix archives its oldest entries (main does it after the "
                  "merge)" % (f, n, limit))
            continue
        print("  %s  %-24s %7d bytes (limit %d)" % ("FAIL    " if over else "ok      ", f, n, limit))
        if over:
            faults.append("%s is %d bytes, over the %d-byte limit: move history to docs/history/ (contract CTX)"
                          % (f, n, limit))
    for f in REPORTED:
        p = os.path.join(root, f)
        if os.path.exists(p):
            print("  report    %-24s %7d bytes (not capped)" % (f, os.path.getsize(p)))
    return faults


def selftest():
    fails = []
    tmp = tempfile.mkdtemp(prefix="ctxsize-")
    try:
        def plant(sizes):
            for f in FILES:
                p = os.path.join(tmp, f)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w", encoding="utf-8", newline='') as fh:
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
        case("files at the limit pass", {f: LIMITS.get(f, LIMIT) for f in FILES}, {}, False)
        case("a planted todo.md 1 KB over its cap fails", {"docs/todo.md": TODO_LIMIT + 1024}, {}, True)
        case("a 25 KB todo.md passes (its cap is its own, not 20 KB)", {"docs/todo.md": 25 * 1024}, {}, False)
        case("a deferred file over the limit is reported, not failed", {"docs/handover/cloud.md": 60 * 1024},
             {"docs/handover/cloud.md": "test"}, False)
        case("a deferred file under the limit fails (the exemption is stale)", {"docs/handover/cloud.md": 9000},
             {"docs/handover/cloud.md": "test"}, True)
        # Step 5: a handover with entries archives itself; one with nothing to move still fails.
        entry = lambda d, n: "## %s (cloud): entry\n\n%s\n\n" % (d, "y" * n)
        text = "# Handover: cloud lane\n\npreamble\n\n" + "".join(entry("2026-10-%02d" % d, 4000) for d in range(27, 20, -1))
        plant({})
        hp = os.path.join(tmp, "docs/handover/cloud.md")
        with open(hp, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        warned = not check(tmp, {})
        print("  %s  a 28 KB handover of dated entries is a warning, not a failure" % ("passed" if warned else "WRONG "))
        ap = os.path.join(tmp, "docs/history/handover-cloud-archive.md")
        os.makedirs(os.path.dirname(ap), exist_ok=True)
        with open(ap, "w", encoding="utf-8", newline="") as fh:
            fh.write("# Cloud lane handover: archive\n\nintro\n\n## 2026-10-01 (cloud): oldest\n\nold\n")
        k = archive(tmp, "docs/handover/cloud.md", "docs/history/handover-cloud-archive.md", today="2026-10-28")
        after, arch = open(hp, encoding="utf-8").read(), open(ap, encoding="utf-8").read()
        kept = [e.split("\n", 1)[0] for e in split_entries(after)[1]]
        moved_ok = (len(after.encode()) <= TARGET and kept[0].startswith("## 2026-10-27") and k == 7 - len(kept)
                    and arch.index("## Moved 2026-10-28") < arch.index("## 2026-10-%02d" % (27 - len(kept)))
                    < arch.index("## 2026-10-21") < arch.index("## 2026-10-01")
                    and after + "".join(e for e in split_entries(arch)[1] if e.startswith("## 2026-10-2")) != "")
        same = (sorted(e.rstrip() for e in split_entries(text)[1])
                == sorted(e.rstrip() for e in split_entries(after)[1] + [e for e in split_entries(arch)[1]
                                                                        if e.startswith("## 2026-10-2")]))
        print("  %s  --fix moved %d oldest entries, newest first, to the archive's top; the handover is %d bytes; every "
              "entry kept word for word" % ("passed" if moved_ok and same else "WRONG ", k, len(after.encode())))
        with open(hp, "w", encoding="utf-8", newline="") as fh:
            fh.write("# Handover\n\n" + "z" * (LIMIT + 10) + "\n" + entry("2026-10-27", 10))
        stuck = bool(check(tmp, {}))
        print("  %s  a handover over the limit with only its newest entry to spare still fails" % ("caught" if stuck else "WRONG "))
        for name, ok in (("handover warning", warned), ("--fix", moved_ok and same), ("nothing to move", stuck)):
            if not ok:
                fails.append(name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST %s" % ("PASS" if not fails else "FAIL: " + ", ".join(fails)))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="check the repo (the default)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fix", action="store_true", help="archive the oldest entries of a handover past the limit")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.fix:
        for h, arc in HANDOVERS.items():
            n = os.path.getsize(os.path.join(ROOT, h))
            if n > LIMIT:
                k = archive(ROOT, h, arc)
                print("%s: %d bytes; moved its %d oldest entr%s to %s; now %d bytes"
                      % (h, n, k, "y" if k == 1 else "ies", arc, os.path.getsize(os.path.join(ROOT, h))))
            else:
                print("%s: %d bytes, within the limit; nothing moved" % (h, n))
        return 0
    print("Context size (contracts CTX, TODO-SLIM): at most %d bytes each, docs/todo.md at most %d" % (LIMIT, TODO_LIMIT))
    faults = check(ROOT, DEFERRED)
    for f in faults:
        print("FAIL: " + f)
    print("FAILED" if faults else "PASS")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
