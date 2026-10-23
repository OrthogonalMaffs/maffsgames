#!/usr/bin/env python3
"""Does every game load the on-screen calculator exactly when its roster says "required"?

    python scripts/check-calculator.py                  # CI
    python scripts/check-calculator.py --root <copy of the repo>   # testing

The calculator tag (canon §4.4) is the last column of .claude/rules/game-roster.md. A game whose
field is `required` shows the "Calculator required" badge on its start screen and loads the shared
on-screen calculator, schools/assets/calculator.js (MaffsCalc), because many resit students do not
own a scientific calculator. The roster is not served, so a page cannot read it at run time: each
game includes the script itself, and this check keeps the three in step, either way.

A `scientific` game (contract SCI-CALC, 9 Oct 2026) needs the scientific keys (xʸ, ln, log, eˣ, trig,
π): it loads the same two scripts, shows "Scientific calculator required" and mounts the calculator with
{keys: 'scientific'}.

Fails on:
  - a `required` game whose page does not include calculator.js, or does not show
    <span class="calc-badge" data-calc="required">Calculator required</span>;
  - a `scientific` game whose page does not include calculator.js, does not show
    <span class="calc-badge" data-calc="scientific">Scientific calculator required</span>, or never mounts
    MaffsCalc with keys: 'scientific'; either badge on a game whose value is the other one;
  - a game that includes calculator.js, or shows a "required" badge, when its roster field is
    anything else (the calculator never appears on a game that does not need it);
  - any other published page (not a roster game) that includes calculator.js;
  - a page that includes calculator.js without schools/assets/keypad.js (MaffsKeypad, the phone
    keypad its answer mode composes). keypad.js itself may load on any page, whatever the roster says:
    it is the keypad for typed answers, with no calculator in it;
  - a roster value outside required / scientific / not allowed / optional / untagged / by stage; a roster with no
    rows at all (the table changed shape; this check is blind).
A `by stage` game (contract CALC-BY-STAGE, Jon, 23 Oct 2026) is a staged game whose stages differ: it declares
<script type="application/json" id="maffs-calc-stages">{"stage-1": "not allowed", ..., "stage-4": "scientific"}</script>
once in its page, keyed by its stage (mode) keys, each value required / scientific / not allowed / optional. Each
stage's choice on the start screen carries that stage's badge, the usual markup with data-stage="<key>" added
(an `optional` stage shows none: its wording is decided when the first game is tagged optional). Fails on:
  - `by stage` with no map, a map that is not a JSON object of strings, or a value outside those four;
  - a map on a game whose roster value is not `by stage`;
  - a badged stage without exactly one badge of its value's markup and wording, a badge naming no stage in the
    map, an `optional` stage with a badge, or a full badge with no data-stage (the header's badge, of the
    stage being played, is filled in at run time and is empty in the source);
  - a map with a required or scientific stage on a page without calculator.js (and keypad.js, as above); a map
    with a scientific stage that never mounts MaffsCalc with keys: 'scientific'; calculator.js on a map with
    no calculator stage.
That the calculator is mounted in the calculator stages only, and the header shows the stage's badge, is the
game's own verifier's job (it plays every stage), not this static check's.

Stdlib only; about a second. A self-test runs first on every run.
"""
import json, argparse, pathlib, re, shutil, sys, tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ".claude/rules/game-roster.md"
VALUES = {"required", "scientific", "not allowed", "optional", "untagged", "by stage"}
STAGE_VALUES = {"required", "scientific", "not allowed", "optional"}   # a `by stage` map's values
CALC_VALUES = {"required", "scientific"}            # the two values that load the on-screen calculator
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/calculator\.js"', re.I)
# The phone keypad (MaffsKeypad) may load on any page; the calculator composes it, so every page that
# loads calculator.js loads keypad.js too.
KEYPAD = re.compile(r'<script\b[^>]*\bsrc="[^"]*schools/assets/keypad\.js"', re.I)
BADGE = re.compile(r'<span class="calc-badge" data-calc="required"[^>]*>Calculator required</span>')
SCI_BADGE = re.compile(r'<span class="calc-badge" data-calc="scientific"[^>]*>Scientific calculator required</span>')
SCI_MOUNT = re.compile(r"""keys\s*:\s*['"]scientific['"]""")
STAGE_MAP = re.compile(r'<script type="application/json" id="maffs-calc-stages">(.*?)</script>', re.S)
# Any full badge (markup and wording); its data-stage, if any, is read separately.
ANY_BADGE = re.compile(r'<span class="calc-badge"([^>]*)>([^<]+)</span>')
# The markup and wording of each value that shows a badge (canon §4.4).
BADGE_FOR = {"required": ("required", "Calculator required"),
             "scientific": ("scientific", "Scientific calculator required"),
             "not allowed": ("not-allowed", "Non-calculator")}
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
        m = STAGE_MAP.search(src)
        if val == "by stage" or m:
            fails.extend(by_stage(slug, val, src, m))
            continue
        inc, badge, sbadge = bool(INCLUDE.search(src)), bool(BADGE.search(src)), bool(SCI_BADGE.search(src))
        if inc and not KEYPAD.search(src):
            fails.append("%s: loads the on-screen calculator without schools/assets/keypad.js, which its answer "
                         "mode needs" % slug)
        if val in CALC_VALUES and not inc:
            fails.append("%s: roster says %s, but the page does not load schools/assets/calculator.js" % (slug, val))
        if val == "required":
            if not badge:
                fails.append("%s: roster says required, but the start screen has no 'Calculator required' badge" % slug)
            if sbadge:
                fails.append("%s: shows 'Scientific calculator required', but its roster field is 'required'" % slug)
        elif val == "scientific":
            if not sbadge:
                fails.append("%s: roster says scientific, but the start screen has no 'Scientific calculator required' "
                             "badge" % slug)
            if badge:
                fails.append("%s: shows 'Calculator required', but its roster field is 'scientific'" % slug)
            if not SCI_MOUNT.search(src):
                fails.append("%s: roster says scientific, but the page never mounts MaffsCalc with keys: 'scientific'" % slug)
        else:
            if inc:
                fails.append("%s: loads the on-screen calculator, but its roster field is %r" % (slug, val))
            if badge or sbadge:
                fails.append("%s: shows a calculator badge, but its roster field is %r" % (slug, val))
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


def by_stage(slug, val, src, m):
    """The failures of a game tagged `by stage`, or of a stage map on a game tagged anything else."""
    if val != "by stage":
        return ["%s: declares a per-stage calculator map, but its roster field is %r, not 'by stage'" % (slug, val)]
    if not m:
        return ["%s: roster says by stage, but the page has no <script type=\"application/json\" "
                "id=\"maffs-calc-stages\"> map" % slug]
    try:
        stages = json.loads(m.group(1))
    except ValueError as e:
        return ["%s: the calculator stage map is not valid JSON (%s)" % (slug, e)]
    if not isinstance(stages, dict) or not stages or not all(isinstance(v, str) for v in stages.values()):
        return ["%s: the calculator stage map must be a non-empty object of stage key -> value" % slug]
    fails = []
    for k, v in stages.items():
        if v not in STAGE_VALUES:
            fails.append("%s: stage %r has calculator value %r, not one of %s" % (slug, k, v, sorted(STAGE_VALUES)))
    if fails:
        return fails
    found = {}
    for attrs, text in ANY_BADGE.findall(src):
        st = re.search(r'\bdata-stage="([^"]*)"', attrs)
        calc = re.search(r'\bdata-calc="([^"]*)"', attrs)
        if not st:
            fails.append("%s: a by-stage game shows a badge with no data-stage (%r)" % (slug, text.strip()))
            continue
        found.setdefault(st.group(1), []).append(((calc.group(1) if calc else None), text.strip()))
    for k in sorted(set(found) - set(stages)):
        fails.append("%s: a badge names stage %r, which is not in the stage map" % (slug, k))
    for k, v in sorted(stages.items()):
        got = found.get(k, [])
        if v == "optional":
            if got:
                fails.append("%s: stage %r is optional, which shows no badge, but has %s" % (slug, k, got))
        elif got != [BADGE_FOR[v]]:
            fails.append("%s: stage %r is %r, so it needs one badge data-calc=%r reading %r; it has %s"
                         % (slug, k, v, BADGE_FOR[v][0], BADGE_FOR[v][1], got or "none"))
    values = set(stages.values())
    inc = bool(INCLUDE.search(src))
    if values & CALC_VALUES:
        if not inc:
            fails.append("%s: a stage needs a calculator (%s), but the page does not load "
                         "schools/assets/calculator.js" % (slug, ", ".join(sorted(values & CALC_VALUES))))
        if not KEYPAD.search(src):
            fails.append("%s: a stage needs a calculator, but the page does not load schools/assets/keypad.js" % slug)
        if "scientific" in values and not SCI_MOUNT.search(src):
            fails.append("%s: a stage is scientific, but the page never mounts MaffsCalc with keys: 'scientific'" % slug)
    elif inc:
        fails.append("%s: loads the on-screen calculator, but no stage in its map needs one" % slug)
    return fails


def selftest():
    """Each breach planted in a scratch copy of the relevant files must fail; the clean copy must pass."""
    tags = roster(BASE)
    req = [s for s, v in tags.items() if v == "required"]
    other = [s for s, v in tags.items() if v != "required" and (BASE / "games" / s / "index.html").exists()]
    if not req or not other:
        return ["self-test: needs one required and one other game in the roster"], 0
    r, o = req[0], other[0]
    # A `by stage` game that exists only in the scratch copy (CALC-BY-STAGE): three non-calculator stages and a
    # scientific fourth, each stage's choice with its badge, the header's badge empty until play.
    f = "calc-stage-fixture"
    fixture = ('<html><head><script src="../../schools/assets/keypad.js"></script>'
               '<script src="../../schools/assets/calculator.js"></script></head><body>'
               '<script type="application/json" id="maffs-calc-stages">{"stage-1": "not allowed", '
               '"stage-2": "not allowed", "stage-3": "not allowed", "stage-4": "scientific"}</script>'
               '<header><span class="calc-badge" id="calcBadge" hidden></span></header>' +
               ''.join('<button data-mode="stage-%d">Stage %d <span class="calc-badge" data-calc="not-allowed" '
                       'data-stage="stage-%d">Non-calculator</span></button>' % (i, i, i) for i in (1, 2, 3)) +
               '<button data-mode="stage-4">Stage 4 <span class="calc-badge" data-calc="scientific" '
               'data-stage="stage-4">Scientific calculator required</span></button>'
               "<script>function go(){ MaffsCalc.mount(el, {keys: 'scientific'}); }</script></body></html>")

    def scratch():
        d = pathlib.Path(tempfile.mkdtemp(prefix="calc-check-"))
        (d / ".claude/rules").mkdir(parents=True)
        shutil.copy(BASE / ROSTER, d / ROSTER)
        for s in (r, o):
            (d / "games" / s).mkdir(parents=True)
            shutil.copy(BASE / "games" / s / "index.html", d / "games" / s / "index.html")
        (d / "games" / f).mkdir(parents=True)
        (d / "games" / f / "index.html").write_text(fixture, encoding="utf-8", newline='')
        with open(d / ROSTER, "a", encoding="utf-8", newline='') as fh:
            fh.write("\n| 999 | Fixture | `%s` | KS3 | Number | scratch only | by stage |\n" % f)
        return d

    fpage = lambda d: d / "games" / f / "index.html"

    def edit(path, fn):
        path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8", newline='')

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
        ("required game shows the scientific badge",
         lambda d: edit(d / "games" / r / "index.html", lambda s: BADGE.sub(
             '<span class="calc-badge" data-calc="scientific">Scientific calculator required</span>', s)), True),
        ("required game retagged scientific without its badge or keys",
         lambda d: edit(d / ROSTER, retag(r, "required", "scientific")), True),
        ("required game retagged scientific with its badge and keys",
         lambda d: (edit(d / ROSTER, retag(r, "required", "scientific")),
                    edit(d / "games" / r / "index.html", lambda s: BADGE.sub(
                        '<span class="calc-badge" data-calc="scientific">Scientific calculator required</span>', s)
                        .replace("</body>", "<script>/* keys: 'scientific' */</script></body>", 1))), False),
        # CALC-BY-STAGE: the clean fixture passes in "clean copy passes"; each breach below must fail.
        ("by stage with no map",
         lambda d: edit(fpage(d), lambda s: STAGE_MAP.sub("", s)), True),
        ("a stage map value outside the list",
         lambda d: edit(fpage(d), lambda s: s.replace('"stage-2": "not allowed"', '"stage-2": "maybe"', 1)), True),
        ("a stage badge disagreeing with its map value",
         lambda d: edit(fpage(d), lambda s: s.replace(
             'data-calc="not-allowed" data-stage="stage-3">Non-calculator',
             'data-calc="scientific" data-stage="stage-3">Scientific calculator required', 1)), True),
        ("a scientific stage with no scientific mount",
         lambda d: edit(fpage(d), lambda s: SCI_MOUNT.sub("keys: 'basic'", s)), True),
        ("a map that needs a calculator, but no calculator.js",
         lambda d: edit(fpage(d), lambda s: INCLUDE.sub("<script data-x", s)), True),
        ("calculator.js on a map with no calculator stage",
         lambda d: edit(fpage(d), lambda s: s.replace('"stage-4": "scientific"', '"stage-4": "not allowed"', 1)
                        .replace('data-calc="scientific" data-stage="stage-4">Scientific calculator required',
                                 'data-calc="not-allowed" data-stage="stage-4">Non-calculator', 1)), True),
        ("a stage map on a whole-game-tagged page",
         lambda d: edit(d / "games" / r / "index.html", lambda s: s.replace(
             "</body>", '<script type="application/json" id="maffs-calc-stages">{"stage-1": "required"}</script></body>', 1)), True),
        ("a non-game page loads it",
         lambda d: (d / "about").mkdir() or (d / "about" / "index.html").write_text(
             '<script src="/schools/assets/calculator.js"></script>', encoding="utf-8", newline=''), True),
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
    sci = sorted(s for s, v in tags.items() if v == "scientific")
    staged = sorted(s for s, v in tags.items() if v == "by stage")
    print("PASS: %d roster games; the on-screen calculator loads on exactly the 'required' ones (%s), the "
          "'scientific' ones (%s) and the 'by stage' ones whose map needs it (%s); self-test %d cases"
          % (len(tags), ", ".join(req) or "none", ", ".join(sci) or "none", ", ".join(staged) or "none", ncases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
