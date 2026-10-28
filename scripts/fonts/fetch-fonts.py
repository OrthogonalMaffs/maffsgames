#!/usr/bin/env python3
"""Fetch the web fonts students see, pinned for the phone-fit checks (contract FONT-FIT, 10 Oct 2026).

Test-only: no page loads these. The checks serve them in place of the CDNs (bank_common.real_fonts_route), so
every phone-fit measurement is taken in the fonts a phone draws, not in the runner's fallback font.

    python scripts/fonts/fetch-fonts.py          # (re)writes scripts/fonts/katex/, google/, dejavu/ and SHA256SUMS

  katex/   KaTeX 0.16.9 (the version every page loads from cdn.jsdelivr.net), from the npm registry's tarball:
           dist/katex.min.css, katex.min.js, contrib/auto-render.min.js, every fonts/*.woff2, and its LICENSE.
  google/  every Google Fonts stylesheet the site's pages request (each distinct css2 URL, found by scanning the
           repo's .html, .js and .css), fetched with headless Chromium's user agent so Google returns exactly the
           woff2 @font-face rules Chromium gets; and every font file those stylesheets name, by its fonts.gstatic.com
           path. google/manifest.json maps each css2 query string to its stylesheet file.
  dejavu/  Ubuntu 24.04's DejaVu fallback faces, fonts-dejavu-core and fonts-dejavu-mono 2.37-8 (the packages the bare
           runner has), checksum-pinned. Not a web font: CI's container jobs unpack them to pin the generic families
           (the workflow's "Pin fallback fonts" step), from here, so no job fetches them from Launchpad (contract SHARD,
           27 Oct 2026: that fetch, on every job, was what made job setup slow).
"""
import hashlib, io, json, os, re, tarfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KATEX_TGZ = "https://registry.npmjs.org/katex/-/katex-0.16.9.tgz"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "HeadlessChrome/141.0.7390.37 Safari/537.36")
CSS2 = re.compile(r"https://fonts\.googleapis\.com/css2\?[^\"'\s)<>]+")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def write(rel, data):
    p = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data)


def katex():
    tar = tarfile.open(fileobj=io.BytesIO(get(KATEX_TGZ)), mode="r:gz")
    want = re.compile(r"^package/(LICENSE|dist/katex\.min\.(css|js)|dist/contrib/auto-render\.min\.js|dist/fonts/[^/]+\.woff2)$")
    n = 0
    for m in tar.getmembers():
        if m.isfile() and want.match(m.name):
            write(os.path.join("katex", m.name[len("package/"):]), tar.extractfile(m).read())
            n += 1
    return n


# The two packages the workflow's "Pin fallback fonts" step unpacks, with their pinned SHA256 (Ubuntu 24.04, 2.37-8).
DEJAVU = (("fonts-dejavu-core_2.37-8_all.deb", "40049660c194f3b8a2541fc7369efebb10e9f94bdac836a2f38fafedd10fa73a"),
          ("fonts-dejavu-mono_2.37-8_all.deb", "8a599d6553307db7ecb795d2f0e5a301e03234afc75c7358b0ba43466454c89a"))
DEJAVU_FROM = ("https://launchpad.net/ubuntu/+archive/primary/+files/",
               "http://archive.ubuntu.com/ubuntu/pool/main/f/fonts-dejavu/")


def dejavu():
    """The DejaVu packages, each from the first source whose bytes match its pinned SHA256, and their copyright file."""
    for name, sha in DEJAVU:
        for base in DEJAVU_FROM:
            try:
                data = get(base + name)
            except OSError:
                continue
            if hashlib.sha256(data).hexdigest() == sha:
                write(os.path.join("dejavu", name), data)
                break
        else:
            raise SystemExit("dejavu: no source gave %s with SHA256 %s" % (name, sha))
    import subprocess, tempfile
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(["dpkg-deb", "-x", os.path.join(HERE, "dejavu", DEJAVU[0][0]), t], check=True)
        write(os.path.join("licences", "dejavu-copyright.txt"),
              open(os.path.join(t, "usr", "share", "doc", "fonts-dejavu-core", "copyright"), "rb").read())
    return len(DEJAVU)


def site_css2_urls():
    urls = set()
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules" and
                   os.path.join(d, x) != os.path.join(ROOT, "scripts", "fonts")]
        for f in files:
            if f.endswith((".html", ".js", ".css")):
                txt = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                urls.update(u.replace("&amp;", "&") for u in CSS2.findall(txt))
    return sorted(urls)


def google():
    manifest, files = {}, set()
    for url in site_css2_urls():
        query = url.split("?", 1)[1]
        css = get(url).decode("utf-8")
        name = "css/%s.css" % hashlib.sha1(query.encode()).hexdigest()[:16]
        write(os.path.join("google", name), css.encode("utf-8"))
        manifest[query] = name
        files.update(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css))
    for u in sorted(files):
        write(os.path.join("google", "gstatic", u.split("fonts.gstatic.com/", 1)[1]), get(u))
    write(os.path.join("google", "manifest.json"),
          (json.dumps(manifest, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    return len(manifest), len(files)


# Each Google family's licence, from Google's own fonts repository (the file a family ships with). Every family the
# site loads is SIL OFL 1.1 except Special Elite (Apache 2.0); confirmed from the fonts' own name table (ID 14).
LICENCES = {f: "https://raw.githubusercontent.com/google/fonts/main/ofl/%s/OFL.txt" % f for f in (
    "outfit", "jetbrainsmono", "nunito", "pressstart2p", "sharetechmono", "bebasneue", "playfairdisplay",
    "courierprime")}


def licences():
    for fam, url in LICENCES.items():
        write(os.path.join("licences", fam + "-OFL.txt"), get(url))
    write(os.path.join("licences", "specialelite-LICENSE.txt"),
          get("https://raw.githubusercontent.com/google/fonts/main/apache/specialelite/LICENSE.txt"))
    # KaTeX's fonts carry the SIL OFL (their name table, ID 14; MathJax-derived), its code the MIT LICENSE in katex/.
    ofl = open(os.path.join(HERE, "licences", "outfit-OFL.txt"), encoding="utf-8").read()
    body = ofl[ofl.index("This Font Software is licensed"):]
    # The copyright notice exactly as KaTeX_Main-Regular carries it (name table, ID 0).
    from fontTools.ttLib import TTFont
    notice = TTFont(os.path.join(HERE, "katex", "dist", "fonts", "KaTeX_Main-Regular.woff2"))["name"].getDebugName(0)
    write(os.path.join("licences", "katex-fonts-OFL.txt"),
          (notice + "\n\n" + body).encode("utf-8"))
    return len(LICENCES) + 2


def sums():
    lines = []
    for d, _, files in os.walk(HERE):
        for f in files:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, HERE).replace(os.sep, "/")
            if rel in ("SHA256SUMS", "fetch-fonts.py", "README.md") or rel.startswith("licences/"):
                continue
            lines.append("%s  %s" % (hashlib.sha256(open(p, "rb").read()).hexdigest(), rel))
    write("SHA256SUMS", ("\n".join(sorted(lines, key=lambda l: l.split("  ", 1)[1])) + "\n").encode())
    return len(lines)


if __name__ == "__main__":
    print("katex: %d files" % katex())
    print("google: %d stylesheets, %d font files" % google())
    print("dejavu: %d packages" % dejavu())
    print("licences: %d files" % licences())
    print("SHA256SUMS: %d files" % sums())
