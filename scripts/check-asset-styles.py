#!/usr/bin/env python3
"""Does every page that loads a shared script also load the stylesheet that script needs?
(contract HALF-THE-SIZE-LOOK, 24 Nov 2026)

    python scripts/check-asset-styles.py              # CI: every published page
    python scripts/check-asset-styles.py --selftest   # planted faults on a copy of three real pages

WHY. Some shared scripts in schools/assets/ draw markup whose rules live in a stylesheet of their own: the on-screen
calculator and the phone keypad (calculator.css), the fold components (fold.css), the stage exit (stage-exit.css) and
others. The script cannot work without the stylesheet, and nothing made a page load both. #894 (HALF-THE-SIZE, 24 Nov
2026) added calculator.js and keypad.js to But It's Only Half the Size! without calculator.css, a page not on the
theme, so its calculator went live as unstyled browser buttons. This is the check that would have caught it, for every
pair, on every page.

THE RULE. SCRIPT_STYLES maps each shared script with a stylesheet of its own to that stylesheet. A published page that
loads one of those scripts with <script src> must link its stylesheet with <link rel="stylesheet">, either directly or
through schools/assets/theme.css when theme.css @imports it. Which stylesheets theme.css imports is read from theme.css
itself on every run, never typed here, so removing an import there fails every page that relied on it.

"Published page" is check-publish-scope.py's definition (a tracked .html file under a SITE path that _config.yml does not
exclude), imported, never copied, as is its reference resolver. Only static tags are read: HTML comments are removed
first, and a script added at run time by another script is not seen.

Adding a pair: a new schools/assets/*.js whose rules live in a schools/assets/*.css goes into SCRIPT_STYLES in the same
PR. The table is checked too: every script and stylesheet it names must exist.
"""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = "schools/assets/theme.css"

# Each shared script whose markup is styled by a stylesheet of its own -> that stylesheet. Found on 24 Nov 2026 by
# matching the class names each schools/assets/*.js writes against the rules in each schools/assets/*.css.
SCRIPT_STYLES = {
    "schools/assets/calculator.js": "schools/assets/calculator.css",   # MaffsCalc, and the calculator badge
    "schools/assets/keypad.js": "schools/assets/calculator.css",       # MaffsKeypad: its rules share calculator.css
    "schools/assets/fold.js": "schools/assets/fold.css",               # canon 7.5.7: "a page needs both"
    "schools/assets/stage-exit.js": "schools/assets/stage-exit.css",
    "schools/assets/card-filter.js": "schools/assets/card-filter.css",
    "schools/assets/featured.js": "schools/assets/featured.css",
    "schools/assets/launch-sash.js": "schools/assets/launch-sash.css",
}

COMMENT = re.compile(r"<!--.*?-->", re.S)
SCRIPT_SRC = re.compile(r"<script\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
LINK = re.compile(r"<link\b[^>]*>", re.I)
HREF = re.compile(r"\bhref\s*=\s*[\"']([^\"']+)[\"']", re.I)
STYLESHEET = re.compile(r"\brel\s*=\s*[\"']?[^\"'>]*\bstylesheet\b", re.I)
IMPORT = re.compile(r"@import\s+(?:url\(\s*)?[\"']?([^\"')\s;]+)", re.I)
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def scope_module():
    spec = importlib.util.spec_from_file_location("check_publish_scope",
                                                  os.path.join(ROOT, "scripts", "check-publish-scope.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PS = scope_module()


def published(root, candidates):
    """The published .html pages among `candidates` (repo-relative paths), by check-publish-scope.py's rule."""
    with open(os.path.join(root, "_config.yml"), encoding="utf-8") as f:
        excl = PS.read_excludes(f.read())
    return [p for p in sorted(candidates)
            if p.endswith(".html") and PS.is_site(p) and not PS.excluded(p, excl) and not PS.special(p)]


def tracked_pages(root):
    out = subprocess.run(["git", "ls-files", "*.html"], cwd=root, capture_output=True, text=True, check=True).stdout
    return published(root, out.split())


def theme_imports(root):
    """The repo paths of the stylesheets theme.css @imports, read from theme.css itself (local files only)."""
    with open(os.path.join(root, THEME), encoding="utf-8") as f:
        css = CSS_COMMENT.sub("", f.read())
    out = set()
    for ref in IMPORT.findall(css):
        path = PS.resolve(ref, THEME)
        if path:
            out.add(path)
    return out


def page_refs(page, html):
    """(scripts, stylesheets): the repo paths this page loads with <script src> and <link rel=stylesheet>."""
    html = COMMENT.sub("", html)
    scripts = {PS.resolve(s, page) for s in SCRIPT_SRC.findall(html)}
    sheets = set()
    for tag in LINK.findall(html):
        h = HREF.search(tag)
        if h and STYLESHEET.search(tag):
            sheets.add(PS.resolve(h.group(1), page))
    return scripts - {None}, sheets - {None}


def problems(root, pages):
    out = []
    for script, sheet in SCRIPT_STYLES.items():
        for path in (script, sheet):
            if not os.path.isfile(os.path.join(root, path)):
                out.append(f"SCRIPT_STYLES names {path}, which does not exist (renamed or removed? update the table)")
    via_theme = theme_imports(root)
    for page in pages:
        with open(os.path.join(root, page), encoding="utf-8") as f:
            scripts, sheets = page_refs(page, f.read())
        for script in sorted(scripts & SCRIPT_STYLES.keys()):
            need = SCRIPT_STYLES[script]
            if need in sheets or (THEME in sheets and need in via_theme):
                continue
            how = ("it links theme.css, which does not import it" if THEME in sheets
                   else "link it, or link theme.css, which imports it" if need in via_theme
                   else "link it")
            out.append(f"{page}: loads {script} but not {need} ({how})")
    return out


def main():
    found = problems(ROOT, tracked_pages(ROOT))
    for line in found:
        print("FAIL  " + line)
    if found:
        print(f"\n{len(found)} problem(s). A shared script without its stylesheet renders as bare browser controls.")
        return 1
    n = len(tracked_pages(ROOT))
    print(f"OK  {n} published pages: every page that loads one of {len(SCRIPT_STYLES)} shared scripts links its "
          f"stylesheet, directly or through theme.css (which imports {', '.join(sorted(os.path.basename(p) for p in theme_imports(ROOT)))}).")
    return 0


# Two real pages for the self-test: one off the theme that links calculator.css itself, one on the theme that gets it
# through theme.css's import. Each must load calculator.js; the self-test refuses to run if either stops fitting.
DIRECT = "games/better-value/index.html"
VIA_THEME = "games/scale-factor-scaling/index.html"


def selftest():
    calc, css = "schools/assets/calculator.js", "schools/assets/calculator.css"
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        files = ["_config.yml", DIRECT, VIA_THEME, THEME] + sorted(set(SCRIPT_STYLES) | set(SCRIPT_STYLES.values()))
        for rel in files:
            os.makedirs(os.path.dirname(os.path.join(tmp, rel)) or tmp, exist_ok=True)
            shutil.copyfile(os.path.join(ROOT, rel), os.path.join(tmp, rel))
        pages = published(tmp, [DIRECT, VIA_THEME])

        def read(rel):
            with open(os.path.join(tmp, rel), encoding="utf-8") as f:
                return f.read()

        def write(rel, text):
            with open(os.path.join(tmp, rel), "w", encoding="utf-8") as f:
                f.write(text)

        # Each plant must fail only that page, only for calculator.css (keypad.js shares it, so it may be named twice).
        # The fixture still fits: both pages published and loading calculator.js, one linking calculator.css directly
        # and not theme.css, the other through theme.css only.
        d_scripts, d_sheets = page_refs(DIRECT, read(DIRECT))
        t_scripts, t_sheets = page_refs(VIA_THEME, read(VIA_THEME))
        if not (pages == sorted([DIRECT, VIA_THEME]) and calc in d_scripts and css in d_sheets
                and THEME not in d_sheets and calc in t_scripts and THEME in t_sheets and css not in t_sheets
                and css in theme_imports(tmp)):
            print("SELFTEST FIXTURE STALE: the two pages no longer fit the cases; pick two that do")
            return 1

        got = problems(tmp, pages)
        print(("ok    " if not got else "MISS  ") + "clean copy passes")
        if got:
            failures.append(("clean copy", got))

        orig = read(DIRECT)
        planted = re.sub(r"<link\b[^>]*calculator\.css[^>]*>\n?", "", orig)
        assert planted != orig
        write(DIRECT, planted)
        got = problems(tmp, pages)
        hit = (any(g.startswith(DIRECT + ": loads " + calc + " but not " + css) for g in got)
               and all(g.startswith(DIRECT + ": ") and " but not " + css + " " in g for g in got))
        print(("ok    " if hit else "MISS  ") + "calculator.css removed from a page not on the theme: caught")
        if not hit:
            failures.append(("direct link removed", got))
        write(DIRECT, orig)

        orig = read(THEME)
        planted = re.sub(r"@import url\('calculator\.css'\);\n?", "", orig)
        assert planted != orig
        write(THEME, planted)
        got = problems(tmp, pages)
        hit = (any(g.startswith(VIA_THEME + ": loads " + calc + " but not " + css) for g in got)
               and all(g.startswith(VIA_THEME + ": ") and " but not " + css + " " in g for g in got))
        print(("ok    " if hit else "MISS  ") + "theme.css's calculator import removed: the page relying on it caught")
        if not hit:
            failures.append(("theme import removed", got))
        write(THEME, orig)

        write(THEME, orig.replace("@import url('calculator.css');", "/* @import url('calculator.css'); */"))
        got = problems(tmp, pages)
        hit = any(g.startswith(VIA_THEME) for g in got)
        print(("ok    " if hit else "MISS  ") + "an import commented out in theme.css does not count")
        if not hit:
            failures.append(("commented import", got))
        write(THEME, orig)

        page = read(VIA_THEME)
        write(VIA_THEME, page.replace('<link rel="stylesheet" href="/schools/assets/theme.css">',
                                      '<!-- <link rel="stylesheet" href="/schools/assets/theme.css"> -->'))
        got = problems(tmp, pages)
        hit = any(g.startswith(VIA_THEME) for g in got)
        print(("ok    " if hit else "MISS  ") + "a theme.css link inside an HTML comment does not count")
        if not hit:
            failures.append(("commented link", got))
        write(VIA_THEME, page)

    if failures:
        for name, got in failures:
            print(f"SELFTEST FAIL {name}: {got}")
        return 1
    print("SELFTEST PASS")
    return 0


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else main())
