#!/usr/bin/env python3
"""Is every live game on the spec map against at least one spec reference?

    python scripts/check-spec-mapping.py              # CI
    python scripts/check-spec-mapping.py --verbose    # every game's references
    python scripts/check-spec-mapping.py --root <copy of the repo>   # testing

The About page said "every game maps to a spec reference" and nothing ever checked it. On
3 Oct 2026 the audit found 68 of the 96 portal games on the spec map and 28 not. A public claim
about the platform needs a check, not a one-off edit, so this is the footer/theme pattern
(canon §7.5.2): one source, one list of known gaps, one check.

Live games are the game cards the portal (index.html) links: every distinct games/<slug>/.
The spec map (spec-map/index.html) is static HTML: one <tr> per spec reference, with
<td class="ref"> (the reference) and <td class="games"> (links to ../games/<slug>/). A game is
mapped when a row with a non-empty reference links it.

Every live game is either mapped or in UNMAPPED. Fails on:
  - a live game that is not mapped and not in UNMAPPED (a new game ships mapped);
  - an UNMAPPED entry that is now mapped (stale: remove it in the PR that maps it);
  - an UNMAPPED entry the portal no longer links (remove it);
  - a spec map with no reference rows at all (the page changed shape; this check is blind).
Reported, never fails: the UNMAPPED games, and spec-map links to games the portal does not list.
Mapping a game is a curriculum judgement (Jon's); this check never decides one.

Stdlib only; about a second. A self-test runs first on every run.
"""
import argparse, html, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
PORTAL = "index.html"
SPEC_MAP = "spec-map/index.html"

# Live games not yet on the spec map (audit of 3 Oct 2026, docs/todo.md). Remove an entry in
# the PR that maps the game; a stale entry fails.
UNMAPPED = [
    "boolean-blitz", "core-maths-paper1", "core-maths-paper2a", "core-maths-paper2b",
    "core-maths-paper2c", "decimal-detective", "equation-builder", "formula-plug-in",
    "four-quadrant-explorer", "free-daily-pizza", "higher-power", "like-terms-collector",
    "linear-equation-solver", "maths-court", "negative-number-line", "new-shapes",
    "probability-pioneer", "seven-bridges", "shape-shifter", "six-sevens-bruv", "spot-the-error",
    "spot-the-muppet", "terrible-advice", "think-of-a-number", "truth-buster",
    "truth-will-set-you-free", "word-problem-decoder", "wrong-on-the-internet",
]

PORTAL_GAME = re.compile(r"""href\s*=\s*["'](?:\./|/)?games/([a-z0-9-]+)/?""", re.I)
SECTION = re.compile(r'<span class="spec-label">(.*?)</span>|<tr\b[^>]*>(.*?)</tr>', re.S | re.I)
REF = re.compile(r'<td class="ref">(.*?)</td>', re.S | re.I)
MAP_GAME = re.compile(r"""href\s*=\s*["'](?:\.\./|/)games/([a-z0-9-]+)/?""", re.I)


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def live_games(portal_html):
    return sorted(set(m.lower() for m in PORTAL_GAME.findall(portal_html)))


def spec_refs(map_html):
    """{slug: ["Section: ref", ...]} for every game a reference row links."""
    out, section = {}, "?"
    for m in SECTION.finditer(map_html):
        if m.group(1) is not None:
            section = text(m.group(1))
            continue
        ref = REF.search(m.group(2))
        if not ref or not text(ref.group(1)):
            continue
        for slug in MAP_GAME.findall(m.group(2)):
            out.setdefault(slug.lower(), []).append("%s: %s" % (section, text(ref.group(1))))
    return out


def check(games, refs, unmapped):
    """(errors, reported) for one portal + spec map + UNMAPPED list."""
    errors = []
    if not refs:
        errors.append("the spec map has no reference rows this check can read "
                      "(<td class=\"ref\"> + a games link): the page changed shape")
    for s in sorted({s for s in unmapped if unmapped.count(s) > 1}):
        errors.append("%s: listed more than once in UNMAPPED" % s)
    for s in games:
        if s not in refs and s not in unmapped:
            errors.append("%s: live on the portal but not on the spec map, and not in UNMAPPED "
                          "(map it on spec-map/index.html; the mapping is Jon's call)" % s)
    for s in sorted(set(unmapped)):
        if s in refs and s in games:
            errors.append("%s: in UNMAPPED but now mapped (%s): remove it from UNMAPPED"
                          % (s, "; ".join(refs[s])))
        elif s not in games:
            errors.append("%s: in UNMAPPED but the portal does not list it: remove it" % s)
    reported = sorted(set(refs) - set(games))
    return errors, reported


def selftest():
    portal = '<a href="games/alpha/">A</a><a href="./games/beta/?level=gcse">B</a><a href="/games/gamma/">G</a>'
    smap = ('<span class="spec-label">GCSE</span><table><tr><th>Ref</th></tr>'
            '<tr><td class="ref">N1</td><td class="topic">x</td><td class="games">'
            '<a class="game-link" href="../games/alpha/?level=gcse">A</a></td></tr>'
            '<tr><td class="ref"></td><td class="games"><a href="../games/beta/">B</a></td></tr>'
            '<tr><td class="ref">N2</td><td class="games"><a href="../games/old/">O</a></td></tr></table>')
    g, r = live_games(portal), spec_refs(smap)
    assert g == ["alpha", "beta", "gamma"], g
    assert r == {"alpha": ["GCSE: N1"], "old": ["GCSE: N2"]}, r     # an empty ref maps nothing
    cases = [
        (["beta", "gamma"], 0),               # all known: passes
        (["beta"], 1),                        # gamma new and unmapped: fails
        (["alpha", "beta", "gamma"], 1),      # alpha mapped but listed: stale, fails
        (["beta", "gamma", "delta"], 1),      # delta not on the portal: fails
        (["beta", "beta", "gamma"], 1),       # duplicate: fails
    ]
    for unmapped, want in cases:
        errors, reported = check(g, r, unmapped)
        assert len(errors) == want, (unmapped, errors)
        assert reported == ["old"], reported
    assert check(g, {}, ["alpha", "beta", "gamma"])[0], "an unreadable map must fail"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--verbose", action="store_true", help="list every mapped game's references")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # a Windows console is cp1252
    selftest()
    root = pathlib.Path(args.root).resolve()
    games = live_games((root / PORTAL).read_text(encoding="utf-8"))
    refs = spec_refs((root / SPEC_MAP).read_text(encoding="utf-8"))
    errors, reported = check(games, refs, UNMAPPED)

    mapped = [s for s in games if s in refs]
    print("Live games on the portal: %d. On the spec map: %d. UNMAPPED (reported, never fails): %d."
          % (len(games), len(mapped), len([s for s in games if s in UNMAPPED and s not in refs])))
    if args.verbose:
        for s in mapped:
            print("  mapped    %-28s %s" % (s, "; ".join(refs[s])))
    for s in UNMAPPED:
        if s in games and s not in refs:
            print("  UNMAPPED  %s" % s)
    for s in reported:
        print("  NOTE      the spec map links %s, which the portal does not list (%s)"
              % (s, "; ".join(refs[s])))
    for e in errors:
        print("FAIL  %s" % e)
    if errors:
        print("\n%d problem(s)." % len(errors))
        return 1
    print("\nOK  every live game is on the spec map or in UNMAPPED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
