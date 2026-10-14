#!/usr/bin/env python3
# ci-line: Text writes (every text-mode write in scripts/ passes newline='', so Windows cannot turn LF into CRLF) | --selftest && --check
# ci-deps: scripts/
"""A script that writes a page or content file in text mode must say newline='' (contract TEXT-WRITES, 14 Oct 2026).

Python's text mode translates LF to the platform newline on write: on Windows every LF becomes CRLF. .gitattributes
(eol=lf) governs what git checks out, not what a script writes at runtime, so a mutated page written by
verify-test-the-claim.py came out CRLF and its newline-sensitive slicing found nothing. This check reads every .py
under scripts/ as a syntax tree and fails on a text-mode write without newline=:

  open(p, 'w' | 'a' | 'x' | 'r+' ...)           (also io.open and pathlib's Path.open)
  Path.write_text(...)
  NamedTemporaryFile / TemporaryFile / SpooledTemporaryFile with a text mode

Binary modes ('wb') and reads are ignored, and so are .open calls that are not file opens (Image.open, pymupdf.open:
their first argument is not a mode string). An open() whose mode is a variable cannot be judged and fails too: write
the mode as a literal.

BLIND SPOTS (listed in docs/handover/home.md, not checked): shell redirects (> and >>) in commands the scripts run,
and subprocess calls given a file as stdout=. Neither goes through Python's text layer here.

scripts/ require Python >= 3.10 (write_text newline=): Path.write_text has no newline= argument before 3.10 (held by
scripts/check-python-version.py).

  python scripts/check-text-writes.py --check      the repo's scripts/
  python scripts/check-text-writes.py --selftest   planted offending writes must be caught, clean ones passed
"""
import argparse
import ast
import os
import re
import shutil
import sys
import tempfile
import warnings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODE_RX = re.compile(r"^[rwaxbt+U]+$")
TEMPS = ("NamedTemporaryFile", "TemporaryFile", "SpooledTemporaryFile")


def _mode(call, pos):
    """('lit', mode) | ('var', None) | (None, None) when the call has no mode argument at that position."""
    node = call.args[pos] if len(call.args) > pos else None
    for k in call.keywords:
        if k.arg == "mode":
            node = k.value
    if node is None:
        return None, None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return "lit", node.value
    return "var", None


def _writes(mode):
    return any(c in mode for c in "wax+")


def scan_source(src, name="<src>"):
    """['name:line what'] for each text-mode write in src that lacks newline=."""
    out = []
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")      # a SyntaxWarning in the scanned file is its own business
            tree = ast.parse(src)
    except SyntaxError as e:
        return ["%s: cannot parse (%s)" % (name, e.msg)]
    for c in ast.walk(tree):
        if not isinstance(c, ast.Call):
            continue
        fn = c.func
        attr = fn.attr if isinstance(fn, ast.Attribute) else None
        ident = fn.id if isinstance(fn, ast.Name) else attr
        has_nl = any(k.arg == "newline" for k in c.keywords)
        what = None
        if ident == "open":
            recv = fn.value.id if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name) else None
            if attr is None or recv == "io":
                kind, mode = _mode(c, 1)           # open(file, mode) / io.open(file, mode)
                if kind == "var":
                    what = "open() with a non-literal mode"
                elif kind == "lit" and _writes(mode) and "b" not in mode:
                    what = "open(..., %r)" % mode
            else:
                kind, mode = _mode(c, 0)           # Path.open(mode); Image.open(path) etc. have no mode string
                if kind == "lit" and MODE_RX.match(mode) and _writes(mode) and "b" not in mode:
                    what = ".open(%r)" % mode
        elif ident == "write_text":
            what = ".write_text()"
        elif ident in TEMPS:
            kind, mode = _mode(c, 0)
            if kind == "var":
                what = ident + "() with a non-literal mode"
            elif kind == "lit" and "b" not in mode:
                what = "%s(%r)" % (ident, mode)
        if what and not has_nl:
            out.append("%s:%d %s" % (name, c.lineno, what))
    return sorted(out)


def check(root):
    faults, n = [], 0
    for d, dirs, files in os.walk(os.path.join(root, "scripts")):
        dirs[:] = [x for x in dirs if x not in ("__pycache__", "node_modules", ".git")]
        for f in sorted(files):
            if f.endswith(".py"):
                p = os.path.join(d, f)
                n += 1
                with open(p, encoding="utf-8", newline="") as fh:
                    faults += scan_source(fh.read(), os.path.relpath(p, root).replace(os.sep, "/"))
    return faults, n


def selftest():
    fails = []
    cases = [
        ("open(p, 'w') fails", "open(p, 'w', encoding='utf-8').write(s)", 1),
        ("open(p, mode='a') fails", "open(p, mode='a')", 1),
        ("open(p, 'r+') fails", "open(p, 'r+')", 1),
        ("io.open(p, 'w') fails", "import io\nio.open(p, 'w')", 1),
        ("Path.open('w') fails", "Path(p).open('w')", 1),
        ("Path.write_text fails", "Path(p).write_text(s, encoding='utf-8')", 1),
        ("NamedTemporaryFile('w') fails", "import tempfile\ntempfile.NamedTemporaryFile('w', suffix='.html')", 1),
        ("NamedTemporaryFile(mode='w') fails", "NamedTemporaryFile(mode='w')", 1),
        ("a variable mode fails", "open(p, m)", 1),
        ("open(p, 'w', newline='') passes", "open(p, 'w', newline='')", 0),
        ("write_text(newline='') passes", "Path(p).write_text(s, newline='')", 0),
        ("NamedTemporaryFile('w', newline='') passes", "NamedTemporaryFile('w', newline='')", 0),
        ("a read passes", "open(p)\nopen(p, 'r', encoding='utf-8')", 0),
        ("a binary write passes", "open(p, 'wb')\nNamedTemporaryFile('wb')\nNamedTemporaryFile()", 0),
        ("Image.open / pymupdf.open pass", "Image.open(path)\npymupdf.open(PDF)\nImage.open(f).convert('RGB')", 0),
    ]
    for name, src, want in cases:
        got = len(scan_source(src))
        ok = got == want
        print("  %s  %s" % (("caught" if want else "passed") if ok else "WRONG ", name))
        if not ok:
            fails.append(name)
    # the directory walk: a planted offending file under scripts/ is found, its clean twin is not
    tmp = tempfile.mkdtemp(prefix="textwrites-")
    try:
        os.makedirs(os.path.join(tmp, "scripts"))
        with open(os.path.join(tmp, "scripts", "bad.py"), "w", encoding="utf-8", newline="") as fh:
            fh.write("open('x', 'w').write('a')\n")
        with open(os.path.join(tmp, "scripts", "good.py"), "w", encoding="utf-8", newline="") as fh:
            fh.write("open('x', 'w', newline='').write('a')\n")
        faults, n = check(tmp)
        ok = n == 2 and len(faults) == 1 and faults[0].startswith("scripts/bad.py:1")
        print("  %s  a planted scripts/bad.py is the only fault found (%d files read)" % ("caught" if ok else "WRONG ", n))
        if not ok:
            fails.append("directory walk")
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
    faults, n = check(ROOT)
    for f in faults:
        print("FAIL: " + f)
    print("text writes: %d scripts read, %d without newline=''" % (n, len(faults)))
    print("FAILED" if faults else "PASS")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main())
