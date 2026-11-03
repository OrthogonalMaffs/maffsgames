#!/usr/bin/env python3
# ci-line: Dash before a number (no em dash or spaced en dash directly before a number, a variable or a minus sign in student-facing text; planted faults) | --selftest && --check
# ci-deps: games/ the-6-ps/ escape-rooms/ schools/assets/
"""DASH-MINUS (contract, Jon, 3 Nov 2026; canon §7.1): a dash directly before a number, a variable or a minus sign reads
as a minus. "Victor is wrong — x = 625" (Terrible Advice) reads as "−x = 625". Jon's rule: never put a dash directly
before a number, a variable or a minus sign in text students read; use a colon or rephrase.

The check reads the source of every student-facing file (no browser), with code comments blanked (HTML comments, CSS in
<style>, and // and /* */ comments in scripts; a URL's // inside a string is not a comment), and fails:

  - an em dash (—), or an en dash with a space before it (" – "), then optional spaces, then optional markup (HTML tags, a
    KaTeX opener \\( \\[ or $), then a digit, "£", a minus sign (− or -), an opening bracket, or a single-letter variable
    (one letter not followed by another letter or digit).

Each dash, space and minus is read in every spelling the source uses: the character, an HTML entity (&mdash; &ndash;
&minus; &nbsp; &pound; and their numeric forms) or a JavaScript escape (\\u2014 \\u2013 \\u2212 \\u00a0 \\u00a3).
An unspaced en dash between two numbers (a range, "1–3") is allowed.

Student-facing files: games/*/index.html, the-6-ps/ (its pages), escape-rooms/**/room.js, and the files under
schools/assets/ that produce question, option or feedback text (SHARED below: the banks, generators and templates, and
the three shared game engines that write a stage's text).

  python scripts/check-dash-minus.py --check      every student-facing file; exit 1 on any hit
  python scripts/check-dash-minus.py --selftest   planted faults, one per pattern, and the cases that must pass
"""
import argparse
from pathlib import Path
import re
import sys

import plant_common as pc

ROOT = Path(__file__).resolve().parent.parent
SHARED = ('found-a-mark-templates.js', 'hc-factor-gen.js', 'percentages-money-generator.js', 'pie-chart-generator.js',
          'probability-generator.js', 'reading-charts-generator.js', 'y-so-steep-gen.js',
          'pie-game.js', 'probability-game.js', 'reading-charts-game.js')

EM = r"(?:—|&mdash;|&#8212;|&#x2014;|\\u2014)"
EN = r"(?:–|&ndash;|&#8211;|&#x2013;|\\u2013)"
SP = r"(?:[ \t ]|&nbsp;|&#160;|&#xa0;|\\u00a0)"
MARKUP = r"(?:<[^<>\n]{1,200}>|\\\\?\\\(|\\\\?\\\[|\$)"
# A single-letter variable is one letter not followed by another letter or digit. Three English words are not variables:
# "a", "A" and "I" followed by a space and a lower-case word, or (for I) an apostrophe ("— a stratified sample", "— I am",
# "— I'll"); a letter joined to a word by a hyphen ("– A-Level") is a word too. "— a·b", "— A, B and C", "— I²" are variables.
WORD_NOT_VAR = r"(?![aAI](?:(?:[ \t ]|&nbsp;)+[a-z]|['’]|&rsquo;|\\u2019))"
TARGET = (r"(?:\d|£|&pound;|&#163;|\\u00a3|−|&minus;|&#8722;|&#x2212;|\\u2212|-|[(\[{]"
          r"|%s[A-Za-z](?![A-Za-z0-9]|-[A-Za-z]))" % WORD_NOT_VAR)
HIT = re.compile(r"(?:%s|%s+%s)%s*(?:%s%s*)*%s" % (EM, SP, EN, SP, MARKUP, SP, TARGET))


def _blank(s):
    """s with every character but a newline turned into a space, so line numbers and offsets survive."""
    return re.sub(r"[^\n]", " ", s)


REGEX_BEFORE = set("(,=:[!&|?{};+-*%<>~^")


def strip_js(src):
    """JavaScript with its comments blanked. Strings, template literals and regex literals are kept as they are."""
    out, i, n = [], 0, len(src)
    last = ""   # the last significant character of code, to tell a regex literal from a division
    while i < n:
        c = src[i]
        if c in "'\"`":
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == "\\":
                    j += 1
                elif c != "`" and src[j] == "\n":
                    break
                j += 1
            out.append(src[i:j + 1])
            i, last = j + 1, c
        elif src.startswith("//", i):
            j = src.find("\n", i)
            j = n if j < 0 else j
            out.append(_blank(src[i:j]))
            i = j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(_blank(src[i:j]))
            i = j
        elif c == "/" and (last == "" or last in REGEX_BEFORE):
            j, cls = i + 1, False
            while j < n and src[j] != "\n" and (src[j] != "/" or cls):
                if src[j] == "\\":
                    j += 1
                elif src[j] == "[":
                    cls = True
                elif src[j] == "]":
                    cls = False
                j += 1
            out.append(src[i:j + 1])
            i, last = j + 1, "/"
        else:
            out.append(c)
            if not c.isspace():
                last = c
            i += 1
    return "".join(out)


SCRIPT = re.compile(r"(<script\b[^>]*>)(.*?)(</script\s*>)", re.S | re.I)
STYLE = re.compile(r"(<style\b[^>]*>)(.*?)(</style\s*>)", re.S | re.I)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


def strip_html(src):
    """An HTML page with its comments, its CSS and its scripts' comments blanked."""
    src = HTML_COMMENT.sub(lambda m: _blank(m.group(0)), src)
    src = STYLE.sub(lambda m: m.group(1) + _blank(m.group(2)) + m.group(3), src)
    return SCRIPT.sub(lambda m: m.group(1) + strip_js(m.group(2)) + m.group(3), src)


def hits(src, kind):
    """[(line, column, the text around the hit)] for one file's source; kind is 'html' or 'js'."""
    text = strip_html(src) if kind == "html" else strip_js(src)
    found = []
    for m in HIT.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        col = m.start() - (text.rfind("\n", 0, m.start()) + 1)
        ctx = src.splitlines()[line - 1]
        found.append((line, col + 1, ctx[max(0, col - 50):col + 40].strip()))
    return found


def files(root=ROOT):
    """{relative path: kind} of every student-facing file."""
    out = {}
    for p in sorted((root / "games").glob("*/index.html")):
        out[p.relative_to(root).as_posix()] = "html"
    for p in sorted((root / "the-6-ps").rglob("*")):
        if p.suffix in (".html", ".js"):
            out[p.relative_to(root).as_posix()] = "html" if p.suffix == ".html" else "js"
    for p in sorted((root / "escape-rooms").rglob("room.js")):
        out[p.relative_to(root).as_posix()] = "js"
    for name in SHARED:
        out["schools/assets/" + name] = "js"
    return out


def check(root=ROOT):
    bad = 0
    per_file = {}
    for rel, kind in files(root).items():
        p = root / rel
        if not p.exists():
            print("FAIL  %s: listed as student-facing but missing" % rel)
            bad += 1
            continue
        for line, col, ctx in hits(p.read_text(encoding="utf-8"), kind):
            print("FAIL  %s:%d:%d  %s" % (rel, line, col, ctx))
            per_file[rel] = per_file.get(rel, 0) + 1
            bad += 1
    if per_file:
        print("\nBy file:")
        for rel, k in sorted(per_file.items(), key=lambda kv: (-kv[1], kv[0])):
            print("  %4d  %s" % (k, rel))
    print("%d hit(s) in %d file(s) of %d checked" % (sum(per_file.values()), len(per_file), len(files(root))))
    return 1 if bad else 0


# A clean page: every pattern below is planted into it in turn.
CLEAN = """<!doctype html><html><head><style>.a{} /* — 5 in CSS */</style></head><body>
<!-- a comment — 5 is not read -->
<p id="opt">Victor is wrong: x = 625</p>
<p>Pages 1–3 are a range.</p>
<p>It costs money — and time.</p>
<script>
// a comment: Victor is wrong — x = 625
/* also a comment — 12 */
const url = "https://example.com/a"; const r = /a\\/b/; const half = 6 / 2;
const opt = 'Victor is wrong: x = 625';
</script></body></html>"""

PLANTS = [  # (name, old, new): each must be caught
    ("em dash before a variable (the Terrible Advice option)", "Victor is wrong: x = 625</p>", "Victor is wrong — x = 625</p>"),
    ("em dash before a digit", "Victor is wrong: x = 625</p>", "Victor is wrong —625</p>"),
    ("em dash before £", "It costs money — and time.", "It costs money — £5."),
    ("em dash before a minus sign (U+2212)", "Victor is wrong: x = 625</p>", "Victor is wrong — −3</p>"),
    ("em dash before a hyphen-minus", "Victor is wrong: x = 625</p>", "Victor is wrong — -3</p>"),
    ("em dash before an opening bracket", "Victor is wrong: x = 625</p>", "Victor is wrong — (x + 1)</p>"),
    ("spaced en dash before a digit", "Pages 1–3 are a range.", "Pages 1 – 3 are a range."),
    ("spaced en dash before a variable", "It costs money — and time.", "It costs money – y more."),
    ("em dash as an HTML entity", "Victor is wrong: x = 625</p>", "Victor is wrong &mdash; x = 625</p>"),
    ("em dash as a JS escape in a string", "const opt = 'Victor is wrong: x = 625';", "const opt = 'Victor is wrong \\u2014 x = 625';"),
    ("em dash in a JS string", "const opt = 'Victor is wrong: x = 625';", "const opt = 'Victor is wrong — x = 625';"),
    ("em dash, then a tag, then a digit", "Victor is wrong: x = 625</p>", "Victor is wrong — <b>625</b></p>"),
    ("em dash, then a KaTeX opener", "const opt = 'Victor is wrong: x = 625';", "const opt = 'Victor is wrong — \\\\(x = 625\\\\)';"),
    ("em dash before &nbsp; and a digit", "Victor is wrong: x = 625</p>", "Victor is wrong —&nbsp;625</p>"),
    ("em dash before a template value (a number at run time)", "const opt = 'Victor is wrong: x = 625';",
     "const opt = `Correct — ${score}/3`;"),
    ("em dash before a room placeholder", "Victor is wrong: x = 625</p>", "Victor is wrong — {{grad.t1}} minutes</p>"),
    ("em dash before the variable a (a·b)", "Victor is wrong: x = 625</p>", "No — a·b = 1</p>"),
    ("em dash before the variable I (I²)", "Victor is wrong: x = 625</p>", "No — I² has wrong dimensions</p>"),
    ("em dash before the point A (A, B and C)", "Victor is wrong: x = 625</p>", "No — A, B and C form a triangle</p>"),
    ("spaced en dash between two amounts (a spaced range)", "Pages 1–3 are a range.", "£12,571 &ndash; &pound;50,270"),
]
PASSES = [  # (name, old, new): each must NOT be caught
    ("an unspaced en dash between two numbers (a range)", "Pages 1–3 are a range.", "Pages 10–20 are a range."),
    ("an em dash before a word", "It costs money — and time.", "It costs money — every penny."),
    ("an em dash before a number, inside a // comment", "// a comment: Victor is wrong — x = 625", "// a comment — 625"),
    ("an em dash before a number, inside an HTML comment", "<!-- a comment — 5 is not read -->", "<!-- a comment — 7 -->"),
    ("a URL's // inside a string is not a comment start", 'const url = "https://example.com/a";', 'const url = "https://e.com/a — page";'),
    ("the article a is a word, not a variable", "It costs money — and time.", "Too small — a census would be better."),
    ("the pronoun I is a word, not a variable", "It costs money — and time.", "6 is the first — I am the second."),
    ("I with an apostrophe is a word", "It costs money — and time.", "and &mdash; I&rsquo;ll be honest &mdash; it works."),
    ("a letter hyphened into a word (A-Level) is a word", "It costs money — and time.", "Binomial Game – A-Level Maths"),
]


def selftest():
    cases, failed = [], 0
    base = hits(CLEAN, "html")
    cases.append(("the clean page has no hit", not base, repr(base)))
    for name, old, new in PLANTS:
        try:
            found, err = hits(pc.apply_plant(CLEAN, old, new, name=name), "html"), None
        except pc.StalePlant as e:
            found, err = [], str(e)
        cases.append(("PLANT %s: caught" % name, pc.is_caught(found, err), err or "not caught"))
    for name, old, new in PASSES:
        try:
            found, err = hits(pc.apply_plant(CLEAN, old, new, name=name), "html"), None
        except pc.StalePlant as e:
            found, err = [], str(e)
        cases.append(("%s: passes" % name, err is None and not found, err or repr(found)))
    js = "const a = 'ok'; // — 5\nconst b = 'Victor is wrong — x';\n"
    found = hits(js, "js")
    cases.append(("a .js file: the string is read, the comment is not (one hit, line 2)",
                  len(found) == 1 and found[0][0] == 2, repr(found)))
    for name, ok, detail in cases:
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "   -> " + detail))
        failed += not ok
    print("Dash-minus selftest: %d/%d passed" % (len(cases) - failed, len(cases)))
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not (a.selftest or a.check):
        ap.error("give --selftest and/or --check")
    rc = 0
    if a.selftest:
        rc |= selftest()
    if a.check:
        rc |= check()
    return rc


if __name__ == "__main__":
    sys.exit(main())
