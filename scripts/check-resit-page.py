#!/usr/bin/env python3
"""Does /resit/ still tell the truth about every game on it?

    python scripts/check-resit-page.py              # CI
    python scripts/check-resit-page.py --static     # the static half only (no browser)
    python scripts/check-resit-page.py --root <copy of the repo>   # testing

/resit/ (launched Oct 2026) is a hand-curated list of games for GCSE resit classes, with one card
per game naming its spec references and the level to choose. A hand-maintained list drifts, so it is
guarded the way the footer and the spec map are: one source (the page), one check.

SUITE below is Jon's ruling of 3 Oct 2026, by topic and in order. Changing the suite means changing
SUITE and the page in the same PR.

Static half (stdlib), fails on:
  - a topic section missing, renamed or out of order, or a card out of SUITE's order;
  - a game on the page that is not in SUITE, or a SUITE game with no card;
  - an EXCLUDED or WITHDRAWN game linked anywhere on the page, or a WITHDRAWN game the portal
    no longer links (withdrawn from /resit/ only, pending a rebuild);
  - a card whose game the portal (index.html) does not link (not live);
  - a card whose game is not on the spec map, or whose spec line differs from the spec map's
    references for it (GCSE references; a game with none shows the map's other references);
  - a card naming a level (data-label) that is not that key's age-neutral label (canon SR-11),
    or a level key (data-key) the game does not read from ?level= or does not have.
Rendered half (Playwright, the stub server), fails on:
  - a "Choose: X" card whose game, opened from the card's link, shows no X on its start screen;
  - a "One level" card whose game shows a level picker;
  - any year-group or key-stage wording on a suite game's start screen (canon SR-11).
A self-test of the static half runs first on every run.
"""
import argparse, html, importlib.util, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
PAGE = "resit/index.html"

# Jon, 3 Oct 2026: the suite, by topic, in this order. shape-shifter added 4 Oct 2026 (Jon: G7
# transformations banded STRETCH). Three withdrawn 4 Oct 2026 (WITHDRAWN below).
SUITE = [
    ("number", "Number", ["six-sevens-bruv", "free-daily-pizza", "negative-number-line",
        "decimal-detective", "think-of-a-number", "factor-race", "prime-factorisation",
        "estimation-golf", "unit-converter"]),
    ("algebra", "Algebra", ["formula-plug-in", "like-terms-collector", "linear-equation-solver",
        "four-quadrant-explorer", "formula-unlocked", "formula-forge", "sequence-solver"]),
    ("ratio", "Ratio, proportion and percentages", ["split-it", "proportion-blaster",
        "better-value", "percentage-flip"]),
    ("geometry", "Geometry and measures", ["new-shapes", "angle-ace", "shape-shifter"]),
    ("probability", "Probability", ["probability-pioneer", "expected-damage", "given-that"]),
    ("statistics", "Statistics", ["distinctly-average", "stat-attack", "chart-interrogator"]),
]
# Jon, 3 Oct 2026: never on the page. prime-or-composite runs to 9,973 (todo: needs a
# Foundation-range option to join); bearings are out as a topic.
EXCLUDED = {"prime-or-composite": "numbers up to 9,973; needs a Foundation-range option to join",
            "bearing-blitz": "bearings are out as a topic"}
# Jon, 4 Oct 2026: withdrawn from the page pending a rebuild (resit correctness audit, PR #35). Each
# stays live on the portal; it returns by moving it back into SUITE in the rebuild's PR.
WITHDRAWN = {"estimation-engine": "1-5% bands mark the GCSE 1 s.f. method wrong; rebuild under SR-12",
             "equation-builder": "slot-by-slot marking rejects equally correct arrangements",
             "correlation-or-coincidence": "the variables are hidden until after the answer"}
# Canon SR-11: the label a student sees for each level key.
LABEL = {"year6": "Starter", "ks3": "Foundation", "gcse": "GCSE", "alevel": "A-Level",
         "core": "Core Maths", "level4": "Level 4", "l4": "Level 4"}
AGE = re.compile(r"\b(?:Years?\s*\d{1,2}(?!\d)|KS\s*\d|Key\s+Stage|primary\s+school|secondary\s+school|"
                 r"your\s+teacher)\b", re.I)

SECTION = re.compile(r'<section class="topic" id="([a-z]+)">\s*<h2>(.*?)</h2>(.*?)</section>', re.S)
CARD = re.compile(r'<a class="card" href="([^"]+)"([^>]*)>(.*?)</a>', re.S)
ATTR = re.compile(r'data-([a-z]+)="([^"]*)"')
SPAN = re.compile(r'<span class="card-([a-z]+)">(.*?)</span>', re.S)
ANY_GAME = re.compile(r"""href\s*=\s*["'](?:\.\./|/)?games/([a-z0-9-]+)/?""", re.I)


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def spec_module(root):
    spec = importlib.util.spec_from_file_location("csm", root / "scripts" / "check-spec-mapping.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def expected_spec(refs):
    gcse = [r.split(": ", 1)[1] for r in refs if r.startswith("GCSE Mathematics: ")]
    if gcse:
        return "GCSE spec: " + ", ".join(gcse)
    return "Spec map: " + "; ".join(r.replace(": ", " ") for r in refs) + " (no GCSE reference on the map)"


def parse(page):
    """[(id, heading, [card dict, ...]), ...] in page order."""
    out = []
    for sid, head, body in SECTION.findall(page):
        cards = []
        for href, attrs, inner in CARD.findall(body):
            c = dict(ATTR.findall(attrs))
            c["href"] = href
            c.update({k: text(v) for k, v in SPAN.findall(inner)})
            cards.append(c)
        out.append((sid, text(head), cards))
    return out


def static_check(page, portal, refs, game_src):
    """Errors from the page alone, given the portal, the spec map's refs and each game's source."""
    errors = []
    live = set(m.lower() for m in ANY_GAME.findall(portal))
    for slug, why in EXCLUDED.items():
        if re.search(r"games/%s/" % re.escape(slug), page):
            errors.append("%s is on the page but EXCLUDED (%s)" % (slug, why))
    for slug, why in WITHDRAWN.items():
        if re.search(r"games/%s/" % re.escape(slug), page):
            errors.append("%s is on the page but WITHDRAWN pending rebuild (%s)" % (slug, why))
        if slug not in live:
            errors.append("%s: WITHDRAWN from /resit/ only, but the portal no longer links it" % slug)
    sections = parse(page)
    got = [(s, h) for s, h, _ in sections]
    want = [(s, h) for s, h, _ in SUITE]
    if got != want:
        errors.append("topic sections are %s, expected %s" % (got, want))
    want_games = {s: g for s, _, g in SUITE}
    for sid, head, cards in sections:
        slugs = [c.get("slug") for c in cards]
        if sid in want_games and slugs != want_games[sid]:
            errors.append("section %s has %s, expected %s" % (sid, slugs, want_games[sid]))
        for c in cards:
            slug = c.get("slug", "?")
            if not c["href"].startswith("/games/%s/" % slug):
                errors.append("%s: card links %s" % (slug, c["href"]))
            if slug not in live:
                errors.append("%s: not live (the portal does not link it)" % slug)
            if slug not in refs:
                errors.append("%s: not on the spec map" % slug)
            elif c.get("spec") != expected_spec(refs[slug]):
                errors.append("%s: card says %r, the spec map gives %r" % (slug, c.get("spec"), expected_spec(refs[slug])))
            kind, label, key = c.get("kind"), c.get("label"), c.get("key")
            want_level = {"choose": "Choose: %s" % label, "link": "Opens at: %s" % label, "one": "One level"}.get(kind)
            if want_level is None or c.get("level") != want_level:
                errors.append("%s: level line %r does not match data-kind=%r data-label=%r" % (slug, c.get("level"), kind, label))
            if kind == "link" and not key:
                errors.append("%s: an 'Opens at' card must carry the level key in its link" % slug)
            if key:
                if c["href"] != "/games/%s/?level=%s" % (slug, key):
                    errors.append("%s: link %s does not open level %s" % (slug, c["href"], key))
                if LABEL.get(key) != label:
                    errors.append("%s: level key %s is labelled %r, SR-11 says %r" % (slug, key, label, LABEL.get(key)))
                src = game_src(slug)
                if "get('level')" not in src or not re.search(r"""['"]%s['"]""" % re.escape(key), src):
                    errors.append("%s: the game does not read level %r from ?level=" % (slug, key))
    on_page = set(m.lower() for m in ANY_GAME.findall(page))
    suite = {g for _, _, gs in SUITE for g in gs}
    for slug in sorted(on_page - suite):
        errors.append("%s: on the page but not in SUITE" % slug)
    for slug in sorted(suite - on_page):
        errors.append("%s: in SUITE but has no card" % slug)
    return errors, sections


PICKER = ".level-btn, .lvl-btn, .level-select, .level-grid, #levelSelect, #levelGrid, [data-level]"


def rendered_check(root, sections):
    sys.path.insert(0, str(root / "scripts"))
    from bank_common import start_stub_server
    from playwright.sync_api import sync_playwright
    errors = []
    proc, base = start_stub_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for _, _, cards in sections:
                for c in cards:
                    pg = browser.new_page(viewport={"width": 1280, "height": 900})
                    pg.goto(base + c["href"], wait_until="load")
                    pg.wait_for_timeout(300)
                    body = pg.locator("body").inner_text()
                    slug, kind, label = c.get("slug"), c.get("kind"), c.get("label")
                    if kind == "choose":
                        # Page text outside scripts, hidden or not: Split It shows its level
                        # picker only after a mode is picked.
                        shown = pg.evaluate("""() => { const out = [];
                            const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                            while (w.nextNode()) {
                              const p = w.currentNode.parentElement;
                              if (p && !p.closest('script,style,noscript')) out.push(w.currentNode.textContent.trim());
                            }
                            return out; }""")
                        if not any(re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(label), t, re.I) for t in shown):
                            errors.append("%s: card says Choose: %s, the start screen shows no %s" % (slug, label, label))
                    if kind == "one":
                        n = pg.locator(PICKER).evaluate_all("els => els.filter(e => e.offsetParent !== null).length")
                        if n:
                            errors.append("%s: card says One level, the start screen shows %d level control(s)" % (slug, n))
                    for m in AGE.finditer(body):
                        errors.append("%s: start screen says %r (canon SR-11)" % (slug, m.group(0)))
                    pg.close()
            browser.close()
    finally:
        proc.terminate()
    return errors


def selftest(page, portal, refs, game_src):
    """Each injected breach must fail the static check; the page as it is must pass."""
    base_errors, _ = static_check(page, portal, refs, game_src)
    if base_errors:
        return []   # the real run reports them
    first = re.search(r'<a class="card" href="/games/([a-z0-9-]+)/', page).group(1)
    faults = {
        "a withdrawn game added back": page.replace("</main>", '<a href="/games/equation-builder/">x</a></main>'),
        "an excluded game added": page.replace("</main>", '<a href="/games/prime-or-composite/">x</a></main>'),
        "a card removed": re.sub(r'<a class="card" href="/games/%s/.*?</a>' % first, "", page, count=1, flags=re.S),
        "a Starter card relabelled": page.replace('data-label="Starter" data-key="year6"', 'data-label="Year 6" data-key="year6"', 1),
        "a spec line edited": page.replace("GCSE spec: N4", "GCSE spec: N5", 1),
        "a section renamed": page.replace("<h2>Probability</h2>", "<h2>Chance</h2>"),
    }
    missed = [name for name, bad in faults.items() if not static_check(bad, portal, refs, game_src)[0]]
    print("self-test: %d of %d injected faults caught" % (len(faults) - len(missed), len(faults)))
    return ["self-test: injected fault not caught: " + n for n in missed]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--static", action="store_true", help="skip the rendered half")
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    page = (root / PAGE).read_text(encoding="utf-8")
    portal = (root / "index.html").read_text(encoding="utf-8")
    refs = spec_module(root).spec_refs((root / "spec-map" / "index.html").read_text(encoding="utf-8"))
    src_cache = {}

    def game_src(slug):
        if slug not in src_cache:
            f = root / "games" / slug / "index.html"
            src_cache[slug] = f.read_text(encoding="utf-8") if f.is_file() else ""
        return src_cache[slug]

    errors = selftest(page, portal, refs, game_src)
    found, sections = static_check(page, portal, refs, game_src)
    errors += found
    n = sum(len(c) for _, _, c in sections)
    if not args.static and not found:
        errors += rendered_check(root, sections)
    for e in errors:
        print("FAIL  " + e)
    print("/resit/: %d sections, %d cards; EXCLUDED checked: %s" % (len(sections), n, ", ".join(EXCLUDED)))
    print("WITHDRAWN pending rebuild (checked off the page, still live): %s" % ", ".join(WITHDRAWN))
    print("FAILED" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
