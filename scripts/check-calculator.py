#!/usr/bin/env python3
"""Does every game load the on-screen calculator exactly when its roster says "required"?

    python scripts/check-calculator.py                  # CI
    python scripts/check-calculator.py --root <copy of the repo>   # testing

The calculator tag (canon §4.4) is the last column of .claude/rules/game-roster.md. A game whose
field is `required` shows the "Calculator required" badge on its start screen and loads the shared
on-screen calculator, schools/assets/calculator.js (MaffsCalc), because many resit students do not
own a scientific calculator. The roster is not served, so a page cannot read it at run time: each
game includes the script itself, and this check keeps the three in step, either way.

Fails on:
  - a `required` game whose page does not include calculator.js, or does not show
    <span class="calc-badge" data-calc="required">Calculator required</span>;
  - a game that includes calculator.js, or shows a "required" badge, when its roster field is
    anything else (the calculator never appears on a game that does not need it);
  - any other published page (not a roster game) that includes calculator.js;
  - a page that includes calculator.js without schools/assets/keypad.js (MaffsKeypad, the phone
    keypad its answer mode composes). keypad.js itself may load on any page, whatever the roster says:
    it is the keypad for typed answers, with no calculator in it;
  - a roster value outside required / not allowed / optional / untagged; a roster with no rows at
    all (the table changed shape; this check is blind).

Stdlib only; about a second. A self-test runs first on every run.
"""
import argparse, pathlib, re, shutil, sys, tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ".claude/rules/game-roster.md"
VALUES = {"required", "not allowed", "optional", "untagged"}
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/calculator\.js"', re.I)
# The phone keypad (MaffsKeypad) may load on any page; the calculator composes it, so every page that
# loads calculator.js loads keypad.js too.
KEYPAD = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/keypad\.js"', re.I)
BADGE = re.compile(r'<span class="calc-badge" data-calc="required"[^>]*>Calculator required</span>')
# A game row: | 12 | Name | `slug` | ... | calculator |   (a withdrawn game is numbered "—")
ROW = re.compile("^\\|\\s*(?:\\d+|—)\\s*\\|[^|]*\\|\\s*`([a-z0-9-]+)`\\s*\\|.*\\|\\s*([^|]*?)\\s*\\|\\s*$")
SKIP_DIRS = {".git", ".github", ".claude", "node_modules", "scripts", "docs", "tools"}


def roster(root):
    """{slug: calculator value} from the roster's game rows."""
    out = {}
    for line in (root / ROSTER).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def check(root):
    fails = []
    tags = roster(root)
    if not tags:
        return ["no game rows found in %s: the table changed shape, so this check is blind" % ROSTER]
    for slug, val in sorted(tags.items()):
        if val not in VALUES:
            fails.append("%s: roster Calculator field %r is not one of %s" % (slug, val, sorted(VALUES)))
    for slug, val in sorted(tags.items()):
        page = root / "games" / slug / "index.html"
        if not page.exists():
            continue
        src = page.read_text(encoding="utf-8")
        inc, badge = bool(INCLUDE.search(src)), bool(BADGE.search(src))
        if inc and not KEYPAD.search(src):
            fails.append("%s: loads the on-screen calculator without schools/assets/keypad.js, which its answer "
                         "mode needs" % slug)
        if val == "required":
            if not inc:
                fails.append("%s: roster says required, but the page does not load schools/assets/calculator.js" % slug)
            if not badge:
                fails.append("%s: roster says required, but the start screen has no 'Calculator required' badge" % slug)
        else:
            if inc:
                fails.append("%s: loads the on-screen calculator, but its roster field is %r" % (slug, val))
            if badge:
                fails.append("%s: shows 'Calculator required', but its roster field is %r" % (slug, val))
    games = {(root / "games" / s / "index.html").resolve() for s in tags}
    for page in root.rglob("*.html"):
        rel = page.relative_to(root)
        if rel.parts and rel.parts[0] in SKIP_DIRS:
            continue
        if page.resolve() in games:
            continue
        if INCLUDE.search(page.read_text(encoding="utf-8", errors="replace")):
            fails.append("%s: loads the on-screen calculator but is not a roster game" % rel.as_posix())
    return fails


def selftest():
    """Each breach planted in a scratch copy of the relevant files must fail; the clean copy must pass."""
    tags = roster(BASE)
    req = [s for s, v in tags.items() if v == "required"]
    other = [s for s, v in tags.items() if v != "required" and (BASE / "games" / s / "index.html").exists()]
    if not req or not other:
        return ["self-test: needs one required and one other game in the roster"], 0
    r, o = req[0], other[0]

    def scratch():
        d = pathlib.Path(tempfile.mkdtemp(prefix="calc-check-"))
        (d / ".claude/rules").mkdir(parents=True)
        shutil.copy(BASE / ROSTER, d / ROSTER)
        for s in (r, o):
            (d / "games" / s).mkdir(parents=True)
            shutil.copy(BASE / "games" / s / "index.html", d / "games" / s / "index.html")
        return d

    def edit(path, fn):
        path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8")

    def retag(slug, old, new):
        return lambda s: re.sub(r"(`%s`.*\|\s*)%s(\s*\|\s*)$" % (re.escape(slug), old), r"\g<1>%s\g<2>" % new, s, flags=re.M)

    cases = [
        ("clean copy passes", lambda d: None, False),
        ("required game without the include",
         lambda d: edit(d / "games" / r / "index.html", lambda s: INCLUDE.sub("<script data-x", s)), True),
        ("required game without the badge",
         lambda d: edit(d / "games" / r / "index.html", lambda s: BADGE.sub("", s)), True),
        ("other game loads the calculator",
         lambda d: edit(d / "games" / o / "index.html",
                        lambda s: s.replace("</head>", '<script src="../../schools/assets/calculator.js"></script></head>', 1)), True),
        ("required tag dropped from the roster", lambda d: edit(d / ROSTER, retag(r, "required", "untagged")), True),
        ("a value outside the four", lambda d: edit(d / ROSTER, retag(o, "untagged", "maybe")), True),
        ("other game loads the keypad only (allowed on any roster value)",
         lambda d: edit(d / "games" / o / "index.html",
                        lambda s: s.replace("</head>", '<script src="../../schools/assets/keypad.js"></script></head>', 1)), False),
        ("required game without the keypad",
         lambda d: edit(d / "games" / r / "index.html", lambda s: KEYPAD.sub("<script data-x", s)), True),
        ("a non-game page loads it",
         lambda d: (d / "about").mkdir() or (d / "about" / "index.html").write_text(
             '<script src="/schools/assets/calculator.js"></script>', encoding="utf-8"), True),
    ]
    out = []
    for name, plant, should_fail in cases:
        d = scratch()
        try:
            plant(d)
            got = bool(check(d))
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if got != should_fail:
            out.append("self-test: %s: %s" % (name, "failed" if got else "was NOT caught"))
    return out, len(cases)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(BASE))
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    st, ncases = selftest()
    for f in st:
        print("FAIL    " + f)
    root = pathlib.Path(args.root)
    fails = check(root)
    for f in fails:
        print("FAIL    " + f)
    if st or fails:
        print("\nFAILED: %d problem(s)" % (len(st) + len(fails)))
        return 1
    tags = roster(root)
    req = sorted(s for s, v in tags.items() if v == "required")
    print("PASS: %d roster games; the on-screen calculator loads on exactly the 'required' ones (%s); "
          "self-test %d cases" % (len(tags), ", ".join(req) or "none", ncases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
