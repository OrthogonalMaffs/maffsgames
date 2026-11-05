#!/usr/bin/env python3
# ci-line: Escape-room token minus sign (formatToken in rating.js and format_token in escape_set_checks.py print a fixed table identically, negatives with U+2212; a hyphen-printing JS rule and a hyphen-printing Python rule planted and caught) |
# ci-deps: scripts/fixtures/escape-format.html escape-rooms/assets/rating.js scripts/escape_set_checks.py
"""Parity test for the escape rooms' token rule (contract TRUE-MINUS, Jon, 5 Nov 2026).

    python scripts/test-escape-format.py

A room prints each {{lock.token}} through one rule per language: formatToken() in escape-rooms/assets/rating.js
(engine.js and teacher.js, in the browser) and format_token() in scripts/escape_set_checks.py (the printable pack's
build_pack.py and check-escape-rooms.py). A negative number, or a string starting "-" then a digit, prints with a
true minus sign, U+2212; every other value prints as JavaScript's String() prints it.

  table   the values below, through both functions: each output must equal the expected text written out here (not
          read from either function), so the two can neither drift apart nor agree on a wrong answer. The JS side
          loads scripts/fixtures/escape-format.html, which loads rating.js as every room page does, in Chromium
          through the stub server, and reads String(formatToken(v)), which is what fill() prints.
  plants  rating.js with formatToken reverted to String(v), and a Python rule that is plain str(): each must FAIL.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bank_common as bc  # noqa: E402
from escape_set_checks import format_token  # noqa: E402

from playwright.sync_api import sync_playwright  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
RATING = ROOT / "escape-rooms" / "assets" / "rating.js"
M = "−"

# (value, the text a student must see). Written out by hand: the expectation is not computed by either rule.
TABLE = [
    (-4, M + "4"),
    (-0.5, M + "0.5"),
    ("-4", M + "4"),
    (0, "0"),
    (4, "4"),
    ("4-6", "4-6"),
    (M + "4", M + "4"),
    ("x", "x"),
    (None, "null"),
]

JS_TABLE = """(vals) => vals.map(v => String(window.MaffsEscapeRating.formatToken(v)))"""


def js_outputs(page, base, rating_src=None):
    """The JS outputs: the fixture page with the real rating.js, or with rating_src (a plant) run over it."""
    page.goto(base + "/scripts/fixtures/escape-format.html", wait_until="load")
    if rating_src is not None:
        page.add_script_tag(content=rating_src)
    return page.evaluate(JS_TABLE, [v for v, _ in TABLE])


def judge(js_out, py_rule):
    fails = []
    for (v, want), got_js in zip(TABLE, js_out):
        got_py = py_rule(v)
        if got_js != want:
            fails.append("JS formatToken(%r) printed %s, want %s" % (v, ascii(got_js), ascii(want)))
        if got_py != want:
            fails.append("Python format_token(%r) printed %s, want %s" % (v, ascii(got_py), ascii(want)))
        if got_js != got_py:
            fails.append("%r: JS %s and Python %s differ" % (v, ascii(got_js), ascii(got_py)))
    return fails


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    src = RATING.read_text(encoding="utf-8")
    real = "if (typeof v === 'number') return v < 0 ? '\\u2212' + String(v).slice(1) : String(v);"
    if real not in src:
        print("FAIL  cannot find formatToken's number rule in rating.js to plant against")
        return 1
    planted_js = src.replace(real, "if (typeof v === 'number') return String(v);")

    def planted_py(v):
        return "null" if v is None else str(v)

    ok = True
    proc, base = bc.start_stub_server()
    try:
        ok = run(base, planted_js, planted_py)
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def run(base, planted_js, planted_py):
    ok = True
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        real_js = js_outputs(page, base)
        fails = judge(real_js, format_token)
        print("table: %d values through both rules: %s" % (len(TABLE), "PASS" if not fails else "FAIL"))
        for f in fails:
            print("  " + f)
        ok = ok and not fails

        for name, js_out, py_rule in (("JS formatToken prints String(v) (a hyphen)", js_outputs(page, base, planted_js), format_token),
                                      ("Python format_token prints str(v) (a hyphen)", real_js, planted_py)):
            caught = bool(judge(js_out, py_rule))
            print("  %s  plant: %s" % ("ok  " if caught else "MISS", name))
            ok = ok and caught
        browser.close()
    return ok


if __name__ == "__main__":
    sys.exit(main())
