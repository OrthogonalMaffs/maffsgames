#!/usr/bin/env python3
"""Every page carries the one site footer: the canonical markup and the shared stylesheet.

    python scripts/check-footer.py
    python scripts/check-footer.py --root <copy of the repo>   # testing

Until October 2026 the footer was copied into each page by hand: 125 pages, four link
sets, two dozen private CSS copies, and one defect shared by every copy (links lost off
both edges of a phone, to-do §1.28). A fix by hand drifts again, so the footer now lives
in one place and this check holds every page to it. It is the authority on the markup:
scripts/apply-footer.py imports CANONICAL, STYLESHEET and EXEMPT from here.

It fails when:
  - a page that needs a footer has none (every .html page not listed in EXEMPT);
  - any page's <footer> differs from CANONICAL, byte for byte, or a page has two;
  - a page with a footer does not link STYLESHEET exactly once, inside <head>;
  - any page's <style> block, or any .css file but the shared one, still styles
    .site-footer (a private copy is how the drift started);
  - an EXEMPT entry names nothing that exists, or a redirect stub stops redirecting.

To change the footer: edit CANONICAL here (and schools/assets/site-footer.css for its
look), run scripts/apply-footer.py, then this. A new page needs only
<footer class="site-footer"></footer> before </body>; apply-footer.py fills it in.
"""
import argparse, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent

STYLESHEET_PATH = "schools/assets/site-footer.css"
STYLESHEET = '<link rel="stylesheet" href="/schools/assets/site-footer.css">'

# Root-absolute links, so one string is right on every page at any depth.
_LINKS = [
    ('/about/', 'About'),
    ('/leaderboards/', 'Leaderboards'),
    ('/spec-map/', 'Spec Map'),
    ('/parents/', 'Parent guides'),
    ('/updates/', "What's changed"),
    ('mailto:contact@maffsgames.co.uk', 'Contact'),
    ('/privacy/', 'Privacy'),
    ('/feedback/', 'Feedback'),
]
_SEP = '<span class="sep">&middot;</span>'
_SUPPORT = ('<a href="https://buymeacoffee.com/maffsgames" target="_blank" rel="noopener">'
            '&#9749; Support<span class="sf-long"> MaffsGames</span></a>')
CANONICAL = ('<footer class="site-footer">'
             + _SEP.join(['<a href="%s">%s</a>' % l for l in _LINKS] + [_SUPPORT])
             + '</footer>')

# Pages that carry no footer, each with its reason. A key ending in "/" covers a folder.
# kind "redirect": the page must still redirect, or the exemption no longer holds.
EXEMPT = {
    "escape-rooms/": ("room",
        "Escape rooms and their teacher pages: a fixed bar over the room engine needs its own "
        "layout check. The 29 Sep ruling (a feedback link in the rooms) is open in to-do §6."),
    "schools/index.html": ("redirect", "Redirect stub to / (kept for links from outside the site)."),
    "schools/about/index.html": ("redirect", "Redirect stub to /about/."),
    "schools/feedback/index.html": ("redirect", "Redirect stub to /feedback/."),
    "schools/privacy/index.html": ("redirect", "Redirect stub to /privacy/."),
    "schools/spec-map/index.html": ("redirect", "Redirect stub to /spec-map/."),
    "year6/index.html": ("redirect", "Redirect stub to /op/."),
    "6-7/index.html": ("redirect", "Redirect stub to /games/prime-or-composite/."),
    "games/sequence-solver/index-original.html": ("redirect",
        "Redirect stub to /games/sequence-solver/: the March 2026 single-mode game it replaced "
        "is in git history at 757837d (to-do §1.33)."),
}

FOOTER = re.compile(r'<footer\b[^>]*>.*?</footer>', re.S | re.I)
STYLE = re.compile(r'<style\b[^>]*>(.*?)</style>', re.S | re.I)
REDIRECT = re.compile(r'http-equiv\s*=\s*["\']refresh|location\.replace\(', re.I)
SKIP_DIRS = {".git", "node_modules"}


def pages(root):
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root).as_posix()
        if not (set(rel.split("/")[:-1]) & SKIP_DIRS):
            yield rel


def exemption(rel):
    for key, val in EXEMPT.items():
        if rel == key or (key.endswith("/") and rel.startswith(key)):
            return key, val
    return None, None


def problems(root):
    out = []
    seen_keys = set()
    for rel in pages(root):
        text = (root / rel).read_text(encoding="utf-8")
        key, ex = exemption(rel)
        if key:
            seen_keys.add(key)
        footers = FOOTER.findall(text)
        if not footers and not ex:
            out.append((rel, "no footer (not in EXEMPT)"))
        if ex and ex[0] == "redirect" and not REDIRECT.search(text):
            out.append((rel, "listed in EXEMPT as a redirect stub but no longer redirects"))
        if len(footers) > 1:
            out.append((rel, "%d <footer> elements" % len(footers)))
        for f in footers:
            if f != CANONICAL:
                out.append((rel, "footer differs from the canonical markup: %s"
                            % re.sub(r"\s+", " ", f)[:160]))
        if footers:
            n = text.count(STYLESHEET)
            head_end = text.lower().find("</head>")
            if n != 1:
                out.append((rel, "links site-footer.css %d times (expected once)" % n))
            elif head_end < 0 or text.find(STYLESHEET) > head_end:
                out.append((rel, "site-footer.css link is not inside <head>"))
        for css in STYLE.findall(text):
            if ".site-footer" in css:
                out.append((rel, "inline <style> still styles .site-footer"))
                break
    for p in sorted(root.rglob("*.css")):
        rel = p.relative_to(root).as_posix()
        if set(rel.split("/")[:-1]) & SKIP_DIRS or rel == STYLESHEET_PATH:
            continue
        if ".site-footer" in p.read_text(encoding="utf-8"):
            out.append((rel, "stylesheet styles .site-footer (only %s may)" % STYLESHEET_PATH))
    if not (root / STYLESHEET_PATH).is_file():
        out.append((STYLESHEET_PATH, "missing"))
    for key in EXEMPT:
        if key not in seen_keys:
            out.append((key, "EXEMPT entry matches no page: remove it"))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    found = problems(root)
    n_pages = sum(1 for _ in pages(root))
    n_exempt = sum(1 for r in pages(root) if exemption(r)[0])
    for rel, why in found:
        print("FAIL  %s: %s" % (rel, why))
    if found:
        print("\n%d problem(s). Fix with: python scripts/apply-footer.py" % len(found))
        return 1
    print("OK  %d pages carry the canonical footer and link %s; %d exempt."
          % (n_pages - n_exempt, STYLESHEET_PATH, n_exempt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
