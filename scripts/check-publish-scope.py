"""What GitHub Pages publishes: every file is SITE or INTERNAL, and no live page uses an INTERNAL one.

Pages builds `main` with Jekyll, which publishes every tracked file except dot-paths, _-prefixed
paths and the `exclude:` list in _config.yml. Jekyll has no allow-list, so a new internal folder
would be published silently. This check closes that gap (canon §7.7):

  1. every tracked file Jekyll would publish must sit under a SITE path below;
  2. no SITE path may be excluded by _config.yml;
  3. no SITE page may reference an excluded file (src/href/url()/fetch strings, resolved the way
     a browser would), because it would 404 on the live site.

A new top-level path fails rule 1 until it is classified: add it to SITE here, or to _config.yml's
exclude list. Stdlib only, about a second. `--selftest` runs the injected faults.

Two listings for the live check after a change to the exclude list (contract FOLD-COMPONENTS item 6, 27 Oct 2026):
`--served [PREFIX ...]` counts what Jekyll publishes under each prefix (default docs/ and scripts/), by folder and file
type; `--live-urls` prints, for every exclude pattern and every folder under docs/, one excluded file as its live URL,
each of which must return 404 (a Markdown file twice: Pages renders a .md without front matter as .html too).
"""
import fnmatch
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Everything a live page needs. Traced from the pages' own references on 2 Oct 2026; docs/art/
# is here because the escape rooms and the portal load their pictures from it.
SITE = [
    "index.html", "CNAME", "robots.txt", "sitemap.xml",
    "6-7/", "about/", "escape-rooms/", "feedback/", "games/", "leaderboards/", "op/",
    "parents/", "privacy/", "essentials/", "resit/", "schools/", "spec-map/", "the-6-ps/", "updates/", "year6/",
    "docs/art/",
]

SCANNED = (".html", ".js", ".css", ".xml", ".json", ".webmanifest", ".mjs")
STRING = re.compile(r"""(?:"([^"\n]{1,300})"|'([^'\n]{1,300})'|url\(\s*([^)'"\s]+)\s*\))""")
SITE_URL = re.compile(r"^https?://(?:www\.)?maffsgames\.co\.uk(/.*)?$")


def read_excludes(text):
    """The `exclude:` list from _config.yml, written as plain '  - path' lines."""
    out, inside = [], False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            inside = line.rstrip() == "exclude:"
            continue
        if inside:
            m = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if not m:
                raise SystemExit(f"_config.yml: cannot read exclude line {line!r}")
            out.append(m.group(1).strip("'\""))
    return out


def excluded(path, patterns):
    """Jekyll 3.10 EntryFilter#glob_include?: fnmatch with no flags (so * crosses /), or prefix."""
    return any(fnmatch.fnmatchcase(path, p) or path.startswith(p) for p in patterns)


def special(path):
    """Jekyll never publishes a path with a component starting . _ # or ~."""
    return any(part[:1] in "._#~" for part in path.split("/"))


def is_site(path):
    return any(path == s or (s.endswith("/") and path.startswith(s)) for s in SITE)


def resolve(ref, page):
    """The repo path a reference on `page` points at, or None if it is not this site's."""
    ref = ref.split("#", 1)[0].split("?", 1)[0].strip()
    if not ref or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//|\$\{|\{)", ref, re.I):
        m = SITE_URL.match(ref)
        if not m:
            return None
        ref = m.group(1) or "/"
    if " " in ref or "<" in ref or "\\" in ref:
        return None
    base = "" if ref.startswith("/") else os.path.dirname(page)
    joined = os.path.normpath(os.path.join(base, ref.lstrip("/"))).replace("\\", "/")
    if joined.startswith("..") or joined == ".":
        return None
    return joined


def check(files, patterns, read):
    failures = []
    for s in SITE:
        if excluded(s.rstrip("/"), patterns) or excluded(s, patterns):
            failures.append(f"SITE path {s} is excluded by _config.yml")
    for f in files:
        if special(f) or excluded(f, patterns):
            continue
        if not is_site(f):
            failures.append(f"unclassified and published: {f} (add it to SITE in this script, "
                            f"or to _config.yml's exclude list)")
    hidden = [f for f in files if excluded(f, patterns) and not special(f)]
    hidden_set = set(hidden)
    for page in files:
        if not is_site(page) or not page.endswith(SCANNED) or excluded(page, patterns):
            continue
        for m in STRING.finditer(read(page)):
            target = resolve(next(g for g in m.groups() if g is not None), page)
            if not target:
                continue
            if target in hidden_set or (target.rstrip("/") + "/index.html") in hidden_set:
                failures.append(f"{page} references {target}, which is not published")
            elif target.endswith("/") or target not in files:
                prefix = target.rstrip("/") + "/"
                under = [f for f in files if f.startswith(prefix)]
                if under and all(f in hidden_set for f in under):
                    failures.append(f"{page} references {prefix}, none of which is published")
    return failures


def selftest():
    files = ["index.html", "games/a/index.html", "docs/art/x.webp", "docs/todo.md",
             "scripts/s.py", "_config.yml", ".github/w.yml"]
    pages = {"index.html": '<img src="docs/art/x.webp">', "games/a/index.html": "var ART='../../docs/art/';"}
    pats = ["docs/*.md", "scripts"]
    read = lambda p: pages.get(p, "")
    assert check(files, pats, read) == [], check(files, pats, read)
    faults = {
        "new top-level folder": (files + ["notes/plan.txt"], pats, read),
        "SITE page links an internal file": (files, pats,
            lambda p: pages.get(p, "") + ('<a href="/docs/todo.md">' if p == "index.html" else "")),
        "SITE page fetches an internal folder": (files, pats,
            lambda p: "fetch('../../scripts/')" if p == "games/a/index.html" else pages.get(p, "")),
        "SITE path excluded": (files, pats + ["docs/art"], read),
        "absolute URL to an internal file": (files, pats,
            lambda p: 'content="https://maffsgames.co.uk/docs/todo.md"' if p == "index.html" else ""),
    }
    for name, args in faults.items():
        if not check(*args):
            raise SystemExit(f"selftest: fault not caught: {name}")
    assert excluded("docs/sub/a.md", ["docs/*.md"])  # * crosses / as in Jekyll
    assert served(files, pats, ["docs/", "scripts/"]) == {("docs/art", ".webp"): 1}, served(files, pats, ["docs/", "scripts/"])
    urls = [u for _, u in live_urls(files, pats)]
    assert urls == [LIVE + "docs/todo.md", LIVE + "docs/todo.html", LIVE + "scripts/s.py"], urls
    assert not any(u.endswith("docs/art/x.webp") for u in urls), "a published file listed as one that must 404"
    print(f"selftest: clean case passes, {len(faults)} injected faults each FAIL")


LIVE = "https://maffsgames.co.uk/"


def served(files, patterns, prefixes):
    """{(folder, extension): count} of the published files under the prefixes."""
    out = {}
    for f in files:
        if any(f.startswith(p) for p in prefixes) and not special(f) and not excluded(f, patterns):
            k = (os.path.dirname(f), os.path.splitext(f)[1] or "(none)")
            out[k] = out.get(k, 0) + 1
    return out


def live_urls(files, patterns):
    """[(why, url)]: one excluded file for each exclude pattern and each folder under docs/, as the live URLs that must
    404; a Markdown file also as the .html Pages would render it to."""
    hidden = sorted(f for f in files if excluded(f, patterns) and not special(f))
    picks = []
    for pat in patterns:
        hit = next((f for f in hidden if fnmatch.fnmatchcase(f, pat) or f.startswith(pat)), None)
        if hit:
            picks.append(("exclude %s" % pat, hit))
    for d in sorted({os.path.dirname(f) for f in hidden if f.startswith("docs/") and f.count("/") >= 2}):
        hit = next(f for f in hidden if os.path.dirname(f) == d)
        picks.append(("folder %s/" % d, hit))
    out, seen = [], set()
    for why, f in picks:
        for path in [f] + ([f[:-3] + ".html"] if f.endswith(".md") else []):
            if path not in seen:
                seen.add(path)
                out.append((why, LIVE + path))
    return out


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    selftest()
    files = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True,
                           check=True).stdout.decode("utf-8").split("\0")
    files = [f for f in files if f]
    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as fh:
        patterns = read_excludes(fh.read())
    if not patterns:
        raise SystemExit("_config.yml has no exclude list")
    if "--served" in sys.argv:
        prefixes = [a for a in sys.argv[sys.argv.index("--served") + 1:] if not a.startswith("--")] or ["docs/", "scripts/"]
        got = served(files, patterns, prefixes)
        for (folder, ext), n in sorted(got.items()):
            print("%5d  %s/*%s" % (n, folder, ext))
        print("published under %s: %d file(s)" % (", ".join(prefixes), sum(got.values())))
        return
    if "--live-urls" in sys.argv:
        for why, url in live_urls(files, patterns):
            print("%-44s %s" % (why, url))
        return

    def read(p):
        with open(os.path.join(ROOT, p), encoding="utf-8", errors="replace") as fh:
            return fh.read()

    failures = check(files, patterns, read)
    published = sum(1 for f in files if not special(f) and not excluded(f, patterns))
    print(f"{len(files)} tracked files: {published} published, all under SITE paths; "
          f"{len(patterns)} exclude patterns")
    if failures:
        for f in failures:
            print("FAIL", f)
        sys.exit(1)
    print("OK: every published file is SITE, and no SITE page references an unpublished file")


if __name__ == "__main__":
    main()
