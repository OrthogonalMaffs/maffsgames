#!/usr/bin/env python3
"""Every game in one adult register: the shared theme, the palette its roster levels give it.

    python scripts/check-theme.py              # CI: fails only on a MIGRATED game, or on the rule itself
    python scripts/check-theme.py --verbose    # every NOT_YET game's findings, and the wording inventory
    python scripts/check-theme.py --root <copy of the repo>   # testing

Until October 2026 every game styled itself from scratch in inline CSS, and canon licensed a
light, playful row (Nunito + Press Start 2P) for any game a Year 6 or KS3 student might play.
Nothing was shared and nothing was checked, so the register drifted game by game: six games
with pixel or rounded fonts, twelve rendering a different row from the one canon gave them,
colour names that differ between games. The fix is the footer's pattern (canon §7.5.2): one
stylesheet (schools/assets/theme.css), one canon rule (§7.5), one check (this file).

The palette is DERIVED, never chosen: palette() below is the only copy of the rule (canon §7.5),
read from the Levels column of .claude/rules/game-roster.md. A level label the rule does not
know is an error, not a default.

Every roster game is in exactly one of two lists:
  MIGRATED  every rule enforced; a breach fails CI.
  NOT_YET   reported, never fails. Migration is per game, in its own contract, never by sweep.

The rules, per game (games/<slug>/index.html):
  - links THEME_LINK exactly once, inside <head>;
  - <html> carries the data-theme that palette() gives;
  - no font-family (in CSS, a style attribute or script) outside the allowed stacks, and no
    font stylesheet but theme.css's (no Google Fonts link of its own);
  - no redefinition of a base token (BASE_TOKENS) in the game's own CSS or script;
  - no hex colour literal outside a :root block (a theme colour belongs in a token);
  - no emoji in <h1>.
Report only, for Jon to rule on: age-specific wording (a year group, a key stage, "primary" or
"secondary school", "your teacher") in each game's static page text, which is its start screen
and anything else written in the HTML. Text a script builds as the game runs is not read.
"""
import argparse, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ".claude/rules/game-roster.md"
THEME_PATH = "schools/assets/theme.css"
THEME_LINK = '<link rel="stylesheet" href="/schools/assets/theme.css">'

# ── The palette rule (canon §7.5, Jon's ruling of 2 Oct 2026). The only copy. ──────────────
LIGHT_LEVELS = {"Year 6", "KS3", "GCSE"}
DARK_LEVELS = {"A-Level", "A-Level Year 2", "Further", "Core", "L3", "L4"}


class UnknownLevel(Exception):
    pass


def palette(levels):
    """A game serving Year 6, KS3 or GCSE is light; one serving only post-16 levels is dark.
    Core Maths is dark (Jon, 2 Oct 2026); GCSE + Core is light because it includes GCSE."""
    unknown = [l for l in levels if l not in LIGHT_LEVELS | DARK_LEVELS]
    if unknown or not levels:
        raise UnknownLevel(", ".join(unknown) or "(no levels)")
    return "light" if any(l in LIGHT_LEVELS for l in levels) else "dark"


# ── The two lists. Move a game from NOT_YET to MIGRATED in the PR that migrates it. ─────────
MIGRATED = [
    "split-it",           # the pilot, 2 Oct 2026
    "just-pythag-it-bruv",  # built to the theme, 4 Oct 2026 (unlisted until Jon approves it)
    "correlation-or-coincidence",  # rebuilt to the theme, 4 Oct 2026 (resit audit rebuild)
    "estimation-engine",  # rebuilt to the theme, 5 Oct 2026 (SR-12 rebuild)
    "simultaneous-solver",  # rebuilt to the theme, 6 Oct 2026 (staged elimination; the keypad and the calculator badge live in theme.css)
]
NOT_YET = [
    "sequence-solver", "estimation-golf", "factor-race", "prime-factorisation",
    "prime-or-composite", "percentage-flip", "fraction-equivalence", "equatle", "52dle",
    "constructions-lab", "word-problem-decoder", "equation-builder", "spot-the-error",
    "gradient-hunter", "truth-buster", "spot-the-muppet", "terrible-advice",
    "wrong-on-the-internet", "maths-court", "expected-damage", "negative-number-line",
    "think-of-a-number", "formula-plug-in", "decimal-detective", "four-quadrant-explorer",
    "like-terms-collector", "probability-pioneer", "shape-shifter", "new-shapes", "higher-power",
    "prisoners-dilemma", "seven-bridges", "distinctly-average",
    "index-laws", "quadratic-factoriser", "trig-wars", "trig-worms", "modular-battle",
    "surd-simplifier", "proportion-blaster", "trig-identity-duel", "standard-form-blitz",
    "circle-theorem-spotter", "probability-paradox", "angle-ace",
    "coordinate-geometry-dash", "graph-transformer", "formula-unlocked", "bearing-blitz",
    "scale-factor-scaling", "unit-converter", "formula-forge",
    "chart-interrogator", "component-crusher", "expectation-station", "better-value",
    "given-that", "screening-room", "linear-equation-solver",
    "core-maths-paper1", "core-maths-paper2a", "core-maths-paper2b", "core-maths-paper2c",
    "tax-theft", "stat-attack", "growth-and-decay", "graph-sketcher", "glorious-gantt",
    "test-the-claim",
    "differentiation-duel", "integration-duel", "suvat", "curling-friction", "force-resolver",
    "moments-master", "log-laws", "binomial-blaster", "partial-fractions-duel", "proof-builder",
    "normal-navigator", "fermi-lab", "dimension-checker", "factor-theorem", "boolean-blitz",
    "truth-will-set-you-free",
    "complex-converter", "matrix-crunch", "characteristic-quest", "eigenvalue-extractor",
    "eigenvector-engine",
    "six-sevens-bruv", "free-daily-pizza",
    "regression-rumble",  # withdrawn (holding page); migrated if it returns
]
# Folders under games/ that are not roster games, each with its reason.
NOT_ROSTER = {
    "the-perfect-prank": "the original prototype, unlisted and off the roster (docs/history/claude-md-archive.md, Escape Rooms); "
                         "its own long-form design, like the escape rooms",
}

BASE_TOKENS = ["bg", "surface", "surface-alt", "text", "muted", "border", "correct", "wrong",
               "hint", "font-text", "font-num"]
ALLOWED_FAMILIES = {"outfit", "jetbrains mono", "opendyslexic", "var(--font-text)",
                    "var(--font-num)", "inherit", "sans-serif", "serif", "monospace",
                    "system-ui", "ui-monospace", "ui-sans-serif"}

ROW = re.compile(r"^\|\s*(?:\d+|—)\s*\|[^|]*\|\s*`([^`]+)`\s*\|([^|]*)\|", re.M)
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT = re.compile(r"<script\b[^>]*>.*?</script>", re.S | re.I)
HEAD_END = re.compile(r"</head>", re.I)
HTML_TAG = re.compile(r"<html\b[^>]*>", re.I)
DATA_THEME = re.compile(r"""\bdata-theme\s*=\s*["']([^"']*)["']""", re.I)
ROOT_BLOCK = re.compile(r":root\s*\{[^}]*\}")
# A colour literal: 3, 4, 6 or 8 hex digits, not an HTML entity (&#...;) or a fragment link.
HEX = re.compile(r"(?<![&\w])(?<!href=\")(?<!href=')#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})(?![\w-])")
FONT_DECL = re.compile(r"font-family\s*:\s*([^;{}\n\"`]+)", re.I)
FONT_JS = re.compile(r"""fontFamily\s*=\s*(['"`])(.*?)\1""")
FONT_SHORTHAND = re.compile(r"""\bfont\s*:\s*[^;{}\n]*?\d(?:px|em|rem|pt|%)\S*\s+([^;{}\n"`]+)""", re.I)
GFONTS = re.compile(r"fonts\.googleapis\.com/css2?\?([^\"')\s>]+)", re.I)
H1 = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.S | re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]")
TOKEN_DEF = re.compile(r"(?<![\w-])--(%s)\s*:" % "|".join(sorted((re.escape(t) for t in BASE_TOKENS),
                                                                    key=len, reverse=True)))
TOKEN_JS = re.compile(r"""setProperty\(\s*['"]--(%s)['"]""" % "|".join(re.escape(t) for t in BASE_TOKENS))
AGE_WORDING = re.compile(r"\b(?:Years?\s*\d{1,2}(?:\s*[–-]\s*\d{1,2})?(?!\d)|KS\s*\d|Key\s+Stage\s*\d?|primary\s+school|"
                         r"secondary\s+school|your\s+teacher)\b", re.I)


def roster(root):
    text = (root / ROSTER).read_text(encoding="utf-8")
    return {m.group(1): [l.strip() for l in m.group(2).split(",") if l.strip()]
            for m in ROW.finditer(text)}


def families(value):
    value = re.sub(r"!\s*important", "", value)
    out = []
    for part in value.split(","):
        name = part.strip().strip("'\"").strip().lower()
        if name:
            out.append(name)
    return out


def static_text(html):
    body = re.split(r"<body\b[^>]*>", html, maxsplit=1, flags=re.I)[-1]
    body = SCRIPT.sub(" ", body)
    body = STYLE.sub(" ", body)
    body = re.sub(r"<footer\b.*?</footer>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", "\n", body)
    return [re.sub(r"\s+", " ", l).strip() for l in body.split("\n") if l.strip()]


def findings(html, expected):
    """Every breach of the register in one game's page, as (rule, detail) pairs."""
    out = []
    head_end = HEAD_END.search(html)
    n = html.count(THEME_LINK)
    if n != 1:
        out.append(("theme.css", "links theme.css %d times (expected once)" % n))
    elif not head_end or html.find(THEME_LINK) > head_end.start():
        out.append(("theme.css", "theme.css link is not inside <head>"))

    tag = HTML_TAG.search(html)
    got = DATA_THEME.search(tag.group(0)) if tag else None
    if not got:
        out.append(("data-theme", '<html> has no data-theme (the rule gives "%s")' % expected))
    elif got.group(1) != expected:
        out.append(("data-theme", '<html data-theme="%s"> but the rule gives "%s"' % (got.group(1), expected)))

    styles = STYLE.findall(html)
    rest = STYLE.sub(" ", html)
    bad_fonts = set()
    for css in styles:
        for m in FONT_DECL.finditer(css):
            bad_fonts.update(f for f in families(m.group(1)) if f not in ALLOWED_FAMILIES)
        for m in FONT_SHORTHAND.finditer(css):
            bad_fonts.update(f for f in families(m.group(1)) if f not in ALLOWED_FAMILIES)
    for m in FONT_DECL.finditer(rest):
        bad_fonts.update(f for f in families(m.group(1)) if f not in ALLOWED_FAMILIES)
    for m in FONT_JS.finditer(html):
        bad_fonts.update(f for f in families(m.group(2)) if f not in ALLOWED_FAMILIES)
    for f in sorted(bad_fonts):
        out.append(("font", "font-family outside the allowed stacks: %s" % f))
    for m in GFONTS.finditer(html):
        out.append(("font", "loads its own Google Fonts (%s); theme.css loads the stacks"
                    % re.sub(r"&display=\w+", "", m.group(1))[:80]))

    redefined = set()
    for css in styles:
        redefined.update(TOKEN_DEF.findall(css))
    redefined.update(TOKEN_DEF.findall(rest))
    redefined.update(TOKEN_JS.findall(html))
    for t in sorted(redefined):
        out.append(("token", "redefines the base token --%s (it belongs to theme.css)" % t))

    hexes = []
    for css in styles:
        hexes += HEX.findall(ROOT_BLOCK.sub(" ", css))
    hexes += HEX.findall(rest)
    if hexes:
        out.append(("hex", "%d hex colour literal(s) outside :root, e.g. %s"
                    % (len(hexes), ", ".join(sorted(set(hexes))[:4]))))

    for h in H1.findall(html):
        if EMOJI.search(h):
            out.append(("emoji", "emoji in <h1>: %s" % re.sub(r"<[^>]+>|\s+", " ", h).strip()[:60]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--verbose", action="store_true",
                    help="list every NOT_YET finding and the age-wording inventory")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # a Windows console is cp1252

    errors = []          # fail CI
    if not (root / THEME_PATH).is_file():
        errors.append((THEME_PATH, "missing"))
    games = roster(root)
    expected = {}
    for slug, levels in games.items():
        try:
            expected[slug] = palette(levels)
        except UnknownLevel as e:
            errors.append((slug, "roster level the palette rule cannot place: %s "
                           "(add it to canon §7.5 and palette(), never default it)" % e))

    listed = MIGRATED + NOT_YET
    for slug in sorted({s for s in listed if listed.count(s) > 1}):
        errors.append((slug, "listed more than once in MIGRATED/NOT_YET"))
    for slug in sorted(set(listed) - set(games)):
        errors.append((slug, "in MIGRATED/NOT_YET but not on the roster: remove it"))
    for slug in sorted(set(games) - set(listed)):
        errors.append((slug, "on the roster but in neither MIGRATED nor NOT_YET "
                       "(a new game is built to the theme and goes in MIGRATED)"))
    games_dir = root / "games"
    for d in sorted(p.name for p in games_dir.iterdir() if p.is_dir()):
        if d not in games and d not in NOT_ROSTER:
            errors.append(("games/" + d, "folder is neither a roster game nor in NOT_ROSTER"))
    for d in NOT_ROSTER:
        if not (games_dir / d).is_dir():
            errors.append(("games/" + d, "NOT_ROSTER entry matches no folder: remove it"))

    report = []
    for slug in listed:
        if slug not in expected:
            continue
        page = games_dir / slug / "index.html"
        if not page.is_file():
            errors.append((slug, "games/%s/index.html missing" % slug))
            continue
        html = page.read_text(encoding="utf-8")
        found = findings(html, expected[slug])
        if slug in MIGRATED:
            errors += [(slug, d) for _, d in found]
        else:
            ages = [l for l in static_text(html) if AGE_WORDING.search(l)]
            report.append((slug, expected[slug], found, ages))

    for slug, why in errors:
        print("FAIL  %s: %s" % (slug, why))

    light = sum(1 for p in expected.values() if p == "light")
    print("Palette from the roster: %d light, %d dark (of %d roster games)."
          % (light, len(expected) - light, len(expected)))
    print("NOT_YET (reported, never fails): %d games." % len(report))
    for slug, pal, found, ages in report:
        rules = {}
        for r, _ in found:
            rules[r] = rules.get(r, 0) + 1
        summary = ", ".join("%s %d" % kv for kv in sorted(rules.items())) or "clean"
        print("  %-28s %-5s  %s%s" % (slug, pal, summary, "  | age wording %d" % len(ages) if ages else ""))
        if args.verbose:
            for _, d in found:
                print("      - %s" % d)
    with_ages = [(s, a) for s, _, _, a in report if a]
    print("\nAge-specific wording in static page text, for Jon to rule on: %d of %d NOT_YET games."
          % (len(with_ages), len(report)))
    if args.verbose:
        for slug, ages in with_ages:
            for line in ages:
                print("  %-28s %s" % (slug, line[:110]))

    if errors:
        print("\n%d problem(s)." % len(errors))
        return 1
    print("\nOK  MIGRATED: %s; every rule holds." % ", ".join(MIGRATED))
    return 0


if __name__ == "__main__":
    sys.exit(main())
