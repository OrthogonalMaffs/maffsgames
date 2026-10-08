"""Check that nothing on the site links to a /schools/ redirect page.

/feedback/, /privacy/, /about/, /spec-map/ and the portal / are the canonical
pages. /schools/feedback/, /schools/privacy/, /schools/about/, /schools/spec-map/
and /schools/ itself are redirects kept only for links from outside the site.
Linking to a redirect costs visitors a hop, hands search engines the redirect
URL, and drops the referrer the feedback page uses to preselect the game the
visitor came from. The game footers, op/ and the sitemap all did it until
September 2026, because new pages copied the footer of old ones.

Every href and src in .html and .js files, every <loc> in .xml files, and every
content="https://maffsgames.co.uk/..." (og:url and the like) is resolved against
the file's own location before it is compared, so ../about/ inside /schools/
is caught as /schools/about/. The first version matched the link text literally
and missed exactly that. The redirect pages themselves are exempt. Markdown
docs are not scanned: they describe the redirects, they do not link to them.

A second check runs on the pages in RESOLVE_PAGES only (Oct 2026: /updates/, the
"What's changed" record, whose whole job is to send a teacher to the thing it names).
On those pages every internal href and src must resolve to a file in the repo; a page
link must not land on a withdrawn page (one whose index.html carries a robots noindex,
which is how a holding page marks itself); and no link may carry ?level=, because a
level link breaks the day that game's levels are renamed. Pages in LEVEL_LINKS_GUARDED are
exempt from that one rule only, because their own check fails the moment a ?level= key they
link is no longer one the game reads. The first check is unchanged
by this and still runs on every file.

    python scripts/check-canonical-links.py
    python scripts/check-canonical-links.py --root <copy of the repo>   # testing
"""
import argparse, pathlib, posixpath, re, sys
from urllib.parse import urlsplit

BASE = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://maffsgames.co.uk"
REDIRECTS = {
    "/schools/": "/",
    "/schools/feedback/": "/feedback/",
    "/schools/privacy/": "/privacy/",
    "/schools/about/": "/about/",
    "/schools/spec-map/": "/spec-map/",
    # The March 2026 single-mode Sequence Solver, replaced by a stub in Oct 2026 (to-do §1.33).
    "/games/sequence-solver/index-original.html": "/games/sequence-solver/",
}
EXEMPT = {p.strip("/") + "/index.html" for p in REDIRECTS}
RESOLVE_PAGES = {"updates/index.html", "essentials/index.html"}
# Resolve pages whose ?level= links another check guards: page -> that check.
LEVEL_LINKS_GUARDED = {"essentials/index.html": "scripts/check-resit-page.py (every card's ?level= key is read by its game)"}
NOINDEX = re.compile(r'''<meta\s+name\s*=\s*["']robots["'][^>]*noindex''', re.I)
LINK = re.compile(
    r'''(?:href|src)\s*=\s*["']([^"']*)["']'''
    r'''|<loc>\s*([^<\s]+)\s*</loc>'''
    r'''|content\s*=\s*["'](https?://(?:www\.)?maffsgames\.co\.uk[^"']*)["']''',
    re.I,
)


def resolve(link, file_dir):
    """Site path a link points at, or None if it leaves the site."""
    parts = urlsplit(link)
    if parts.scheme or parts.netloc:
        if parts.netloc not in ("maffsgames.co.uk", "www.maffsgames.co.uk"):
            return None
        path = parts.path or "/"
    elif parts.path == "" or link.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    elif parts.path.startswith("/"):
        path = parts.path
    else:
        path = posixpath.join(file_dir, parts.path)
    trailing = path.endswith("/")
    path = posixpath.normpath(path)
    if path.endswith("/index.html"):
        path, trailing = path[: -len("index.html")], True
    if not path.endswith("/") and (trailing or "." not in posixpath.basename(path)):
        path += "/"
    return path


def resolve_problem(link, target, root, self_rel):
    """Why `link` (resolved to `target`) fails the RESOLVE_PAGES check, or None."""
    if self_rel not in LEVEL_LINKS_GUARDED and re.search(r"(^|&)level=", urlsplit(link).query):
        return "carries ?level="
    rel = target.lstrip("/")
    file = root / (rel + "index.html" if target.endswith("/") else rel)
    if not file.is_file():
        return "does not resolve to a file in the repo"
    is_self = file.relative_to(root).as_posix() == self_rel
    if file.name == "index.html" and not is_self \
            and NOINDEX.search(file.read_text(encoding="utf-8", errors="replace")):
        return "points to a withdrawn (noindex) page"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=BASE, type=pathlib.Path)
    root = ap.parse_args().root.resolve()

    hits, broken, scanned = [], [], 0
    for file in sorted(root.rglob("*")):
        if file.suffix not in {".html", ".xml", ".js"} or not file.is_file():
            continue
        rel = file.relative_to(root).as_posix()
        if "node_modules" in rel.split("/") or rel in EXEMPT:
            continue
        scanned += 1
        file_dir = "/" + posixpath.dirname(rel)
        for n, line in enumerate(file.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for m in LINK.finditer(line):
                link = next(g for g in m.groups() if g is not None)
                target = resolve(link, file_dir)
                if target in REDIRECTS:
                    hits.append(f"{rel}:{n}: {link!r} -> {target} (use {REDIRECTS[target]})")
                if rel in RESOLVE_PAGES and target is not None:
                    why = resolve_problem(link, target, root, rel)
                    if why:
                        broken.append(f"{rel}:{n}: {link!r} {why}")

    print(f"scanned {scanned} files")
    if hits:
        print(f"\nFAIL: {len(hits)} link(s) to a /schools/ redirect")
        for h in hits:
            print("  -", h)
    else:
        print("no links to /schools/ redirect pages")

    for p in sorted(RESOLVE_PAGES):
        if not (root / p).is_file():
            broken.append(f"{p}: listed in RESOLVE_PAGES but not found")
    if broken:
        print(f"\nFAIL: {len(broken)} link(s) on {', '.join(sorted(RESOLVE_PAGES))} that must resolve do not")
        for b in broken:
            print("  -", b)
    else:
        print(f"every internal link resolves on {', '.join(sorted(RESOLVE_PAGES))}")

    if hits or broken:
        sys.exit(1)


if __name__ == "__main__":
    main()
