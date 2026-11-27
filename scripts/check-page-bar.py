#!/usr/bin/env python3
# ci-line: Page bar (every non-game site page carries the one canonical top bar, first in <body>, and links the one stylesheet; no hand-copied nav.nav, no bar CSS outside it; planted faults caught) | --selftest
# ci-deps: any-page scripts/apply-page-bar.py scripts/build-uses.py scripts/check-footer.py
"""Every non-game site page carries the one page bar: the canonical markup and the shared stylesheet.

    python scripts/check-page-bar.py              # the check
    python scripts/check-page-bar.py --selftest   # planted faults, each must be caught
    python scripts/check-page-bar.py --root <copy of the repo>

Until November 2026 the top bar was copied into each site page by hand (contract LEADERBOARD-PAGE, Jon 27 Nov 2026,
"there is no back button to get out of the leaderboards page"): eight variants of nav.nav, each styled in its own page
or section stylesheet, and five pages (leaderboards, privacy, spec-map, op, class) with no way home at the top at all.
It is the footer's story again (scripts/check-footer.py), so the bar now lives in one place and this check holds every
page to it. It is the authority on the markup: scripts/apply-page-bar.py and scripts/build-uses.py import bar_for(),
STYLESHEET and OPT_OUT from here.

The bar (schools/assets/page-bar.css for its look): the MaffsGames name linking to "/", then an optional link up to the
page's section (SECTIONS), "← Back to Games" as an a.back-link (schools/assets/site-nav.js turns it into "← Back to
<hub>" when the page was opened from a hub) and, on the pages in SECTIONS that have one, the Aa button.

The pages: every .html page check-footer.py holds to the footer (its pages() less its EXEMPT entries), outside games/
and escape-rooms/ (games have their own bar, the SITE-BAR pilot), less OPT_OUT below.

It fails when:
  - such a page has no bar, or two;
  - a page's bar differs from bar_for(page), byte for byte, or is not the first element in <body>;
  - a page still carries a hand-copied <nav class="nav">;
  - a page with the bar does not link STYLESHEET exactly once, inside <head>;
  - any page's <style> block, or any .css file but the shared one, styles .page-bar or its parts;
  - a site page's <style> block, or a section stylesheet it links (outside schools/assets/), still styles the
    retired .nav or .nav-right;
  - an OPT_OUT entry names nothing that exists, or a page there carries the bar.

To change the bar: edit bar_for() here (and schools/assets/page-bar.css for its look), run scripts/apply-page-bar.py
and scripts/build-uses.py, then this.
"""
import argparse, importlib.util, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_footer", BASE / "scripts" / "check-footer.py")
cf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cf)

STYLESHEET_PATH = "schools/assets/page-bar.css"
STYLESHEET = '<link rel="stylesheet" href="/schools/assets/page-bar.css">'

# Pages under these folders are site pages the footer covers but are not this bar's: each has its own.
NOT_SITE = ("games/", "escape-rooms/")

# Site pages that carry no bar, each with its reason. A key ending in "/" covers a folder.
OPT_OUT = {
    "index.html": "The portal is home: its own header is the way in, and a bar whose every link goes to the page "
                  "itself would be no way out.",
    "scripts/fixtures/": "Test fixtures for scripts' own checks, never published (canon 7.7).",
}

# A section's pages link up to the section's own hub. (href, long label, short label below 480 px.) The hub itself
# has no up link. aa: the section's pages carry the Aa button (parents/guide.js wires #a11yBtn).
SECTIONS = {
    "parents/": {"hub": "parents/index.html", "up": ("/parents/", "All parent guides", "Guides"), "aa": True},
    "when-will-i-use-this/": {"hub": "when-will-i-use-this/index.html",
                              "up": ("/when-will-i-use-this/", "When will I use this?", "Topics"), "aa": True},
}

AA = ('<button class="a11y-btn" id="a11yBtn" type="button" aria-pressed="false" '
      'title="Dyslexia-friendly mode">Aa</button>')


def section_of(rel):
    for prefix, sec in SECTIONS.items():
        if rel.startswith(prefix):
            return sec
    return None


def bar_for(rel):
    """The canonical bar for a page (its path relative to the site root, e.g. 'parents/angles/index.html')."""
    sec = section_of(rel)
    up = aa = ""
    if sec:
        aa = AA if sec["aa"] else ""
        if rel != sec["hub"]:
            href, long_, short = sec["up"]
            up = ('<a class="page-bar-up" href="%s">&larr; <span class="page-bar-long">%s</span>'
                  '<span class="page-bar-short">%s</span></a>' % (href, long_, short))
    return ('<nav class="page-bar" aria-label="Site"><a class="page-bar-home" href="/">MaffsGames</a>'
            '<span class="page-bar-links">' + up + '<a class="back-link" href="/">&larr; <span class="page-bar-long">Back to </span>'
            'Games</a>' + aa +
            '</span></nav>')


BAR = re.compile(r'<nav\b[^>]*\bclass="page-bar"[^>]*>.*?</nav>', re.S | re.I)
LEGACY = re.compile(r'<nav\b[^>]*\bclass="nav"[^>]*>', re.I)
BODY = re.compile(r'<body\b[^>]*>', re.I)
STYLE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.S | re.I)
CSS_LINK = re.compile(r'<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"', re.I)
BAR_CSS = re.compile(r'\.page-bar\b')
LEGACY_CSS = re.compile(r'(?<![\w-])\.nav(?:-right)?(?![\w-])')


def opt_out(rel):
    for key in OPT_OUT:
        if rel == key or (key.endswith("/") and rel.startswith(key)):
            return key
    return None


def site_pages(root):
    """Every page this check covers, and the opt-out key of each (None for a page that must carry the bar)."""
    for rel in cf.pages(root):
        if cf.exemption(rel)[0] or rel.startswith(NOT_SITE):
            continue
        yield rel, opt_out(rel)


def first_element_after(text, at):
    """The first tag after offset `at`, skipping whitespace and comments."""
    m = re.compile(r'(?:\s|<!--.*?-->)*', re.S).match(text, at)
    return text[m.end():m.end() + 200]


def css_of(root, rel, text):
    """Section stylesheets a page links (local, outside schools/assets/): [(path, text)]."""
    out = []
    for href in CSS_LINK.findall(text):
        if href.startswith(("http:", "https:", "//")):
            continue
        p = (root / href.lstrip("/")) if href.startswith("/") else (root / rel).parent / href
        try:
            r = p.resolve().relative_to(root).as_posix()
        except ValueError:
            continue
        if r.startswith("schools/assets/") or not p.is_file():
            continue
        out.append((r, p.read_text(encoding="utf-8")))
    return out


def problems(root, texts=None, css_files=None):
    """Every fault, as (where, why). `texts` / `css_files` replace files read from `root` (the self-test's plants)."""
    texts = dict(texts or {})
    css_files = dict(css_files or {})
    out, seen_opt = [], set()
    section_css = {}

    def read(rel):
        if rel not in texts:
            texts[rel] = (root / rel).read_text(encoding="utf-8")
        return texts[rel]

    for rel, key in site_pages(root):
        text = read(rel)
        bars = BAR.findall(text)
        if key:
            seen_opt.add(key)
            if bars:
                out.append((rel, "is in OPT_OUT but carries the bar"))
            continue
        if not bars:
            out.append((rel, "no page bar (not in OPT_OUT)"))
        elif len(bars) > 1:
            out.append((rel, "%d page bars" % len(bars)))
        want = bar_for(rel)
        for b in bars:
            if b != want:
                out.append((rel, "page bar differs from the canonical markup: %s" % re.sub(r"\s+", " ", b)[:200]))
        body = BODY.search(text)
        if bars and body and not first_element_after(text, body.end()).startswith('<nav class="page-bar"'):
            out.append((rel, "the page bar is not the first element in <body>"))
        if LEGACY.search(text):
            out.append((rel, 'still carries a hand-copied <nav class="nav">'))
        if bars:
            n = text.count(STYLESHEET)
            head_end = text.lower().find("</head>")
            if n != 1:
                out.append((rel, "links page-bar.css %d times (expected once)" % n))
            elif head_end < 0 or text.find(STYLESHEET) > head_end:
                out.append((rel, "page-bar.css link is not inside <head>"))
        for css in STYLE.findall(text):
            if LEGACY_CSS.search(css):
                out.append((rel, "inline <style> still styles the retired .nav / .nav-right"))
                break
        for path, css in css_of(root, rel, text):
            section_css[path] = css_files.get(path, css)
    for rel in cf.pages(root):
        for css in STYLE.findall(read(rel) if rel in texts else (root / rel).read_text(encoding="utf-8")):
            if BAR_CSS.search(css):
                out.append((rel, "inline <style> styles .page-bar (only %s may)" % STYLESHEET_PATH))
                break
    css_all = {p.relative_to(root).as_posix(): None for p in root.rglob("*.css")
               if not (set(p.relative_to(root).as_posix().split("/")[:-1]) & cf.SKIP_DIRS)}
    css_all.update({k: v for k, v in css_files.items()})
    for rel in sorted(css_all):
        if rel == STYLESHEET_PATH:
            continue
        css = css_all[rel] if css_all[rel] is not None else (root / rel).read_text(encoding="utf-8")
        if BAR_CSS.search(css):
            out.append((rel, "stylesheet styles .page-bar (only %s may)" % STYLESHEET_PATH))
    for path, css in sorted(section_css.items()):
        if LEGACY_CSS.search(css):
            out.append((path, "section stylesheet still styles the retired .nav / .nav-right"))
    if not (root / STYLESHEET_PATH).is_file():
        out.append((STYLESHEET_PATH, "missing"))
    for key in OPT_OUT:
        if key not in seen_opt:
            out.append((key, "OPT_OUT entry matches no page: remove it"))
    return out


def selftest(root):
    """The plants. Each must be caught on the real pages, and the real pages must pass untouched."""
    base = problems(root)
    if base:
        print("SELFTEST: the unplanted site already fails (%d problem(s)); fix those first" % len(base))
        for where, why in base[:10]:
            print("  %s: %s" % (where, why))
        return 1
    page = "leaderboards/index.html"
    text = (root / page).read_text(encoding="utf-8")
    bar = bar_for(page)
    guide = "parents/angles/index.html"
    gtext = (root / guide).read_text(encoding="utf-8")
    plants = [
        ("a page with the bar removed", {page: text.replace(bar, "")}, {}, page, "no page bar"),
        ("a hand-edited bar", {page: text.replace(bar, bar.replace("MaffsGames", "Maffs Games"))}, {}, page,
         "differs from the canonical markup"),
        ("a bar CSS rule in a page", {page: text.replace("</style>", ".page-bar{height:60px}\n</style>", 1)}, {},
         page, "inline <style> styles .page-bar"),
        ("a bar CSS rule in a section stylesheet", {}, {"parents/guide.css":
         (root / "parents/guide.css").read_text(encoding="utf-8") + "\n.page-bar a{color:red}\n"},
         "parents/guide.css", "styles .page-bar"),
        ("a guide given the generic bar (its up link and Aa lost)", {guide: gtext.replace(bar_for(guide), bar)}, {},
         guide, "differs from the canonical markup"),
        ("the bar moved below the header", {page: text.replace(bar + "\n", "").replace("</div>\n\n<div class=\"content\">",
         "</div>\n" + bar + "\n\n<div class=\"content\">", 1)}, {}, page, "not the first element"),
        ("a hand-copied nav.nav put back", {page: text.replace(bar, bar + '\n<nav class="nav"><a href="/">MaffsGames</a></nav>')},
         {}, page, 'hand-copied <nav class="nav">'),
        ("the stylesheet link dropped", {page: text.replace(STYLESHEET + "\n", "")}, {}, page, "links page-bar.css 0 times"),
    ]
    failed = 0
    for name, texts, css, where, expect in plants:
        got = problems(root, texts, css)
        hit = [w for w in got if w[0] == where and expect in w[1]]
        print("%s  plant: %s" % ("caught" if hit else "MISSED", name))
        if not hit:
            failed += 1
            for w in got[:5]:
                print("    got %s: %s" % w)
    if failed:
        print("SELFTEST FAILED: %d plant(s) missed" % failed)
        return 1
    print("SELFTEST OK: %d plants caught; the real pages pass" % len(plants))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    if args.selftest:
        return selftest(root)
    found = problems(root)
    for where, why in found:
        print("FAIL  %s: %s" % (where, why))
    if found:
        print("\n%d problem(s). Fix with: python scripts/apply-page-bar.py (and scripts/build-uses.py)" % len(found))
        return 1
    pages = list(site_pages(root))
    print("OK  %d site pages carry the canonical page bar and link %s; %d opted out (%s)."
          % (sum(1 for _, k in pages if not k), STYLESHEET_PATH, sum(1 for _, k in pages if k),
             ", ".join(sorted(OPT_OUT))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
