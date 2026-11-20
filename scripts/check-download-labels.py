#!/usr/bin/env python3
# ci-line: Download links labelled (every <a download> on a served page has data-mfg-item inside a data-mfg-section, so analytics.js counts it as section_clicked action download; planted faults caught) |
"""Every download link on the site is labelled, so the Events sheet counts it (contract DOWNLOAD-COUNTS, 20 Nov 2026).

    python -X utf8 scripts/check-download-labels.py

The shared analytics script has one click listener for labelled sections: an element with data-mfg-item inside a
data-mfg-section fires section_clicked, and an <a> with a download attribute is sent with action "download". A
download link with no label is seen only by GA4's automatic file_download, which ad-blockers and many school
networks block, so the Sheet never learns of it. Until 20 Nov the five downloads on the Counting Players page and
the CSV buttons on two Ugh, stats pages were unlabelled.

Fails when any <a> with a download attribute, in any served .html (a tracked file GitHub Pages publishes, by
check-publish-scope's own rules), either has no data-mfg-item or has no ancestor with data-mfg-section.
Then it plants two faults in a copy of the first served page that has download links, each of which must be caught
(plant_common: a plant that did not apply is a STALE PLANT and fails the run): one link's data-mfg-item removed;
the page's data-mfg-section labels removed. Stdlib only, about a second.

No page path is written here on purpose: scripts/ci-deps.py maps a verifier to the pages its strings name, and this
check must run on every change (a new page with an unlabelled download is exactly what it is for), which it does
only while it names no page.
"""
import html.parser
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import plant_common as pc  # noqa: E402

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
ITEM_ON_DOWNLOAD = re.compile(r'(<a\b[^>]*\sdownload\b[^>]*?)\sdata-mfg-item="[^"]+"')
SECTION = re.compile(r'\sdata-mfg-section="[^"]+"')


def load_scope():
    spec = importlib.util.spec_from_file_location("publish_scope", os.path.join(ROOT, "scripts", "check-publish-scope.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def served_html():
    """Tracked .html files GitHub Pages publishes (check-publish-scope.py's SITE, excludes and special paths)."""
    scope = load_scope()
    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as f:
        excludes = scope.read_excludes(f.read())
    files = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    return sorted(p for p in files
                  if scope.is_site(p) and not scope.special(p) and not scope.excluded(p, excludes))


class Finder(html.parser.HTMLParser):
    """Each <a download>: (line, has data-mfg-item, inside a data-mfg-section)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # [(tag, opens a section)]
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "download" in a:
            inside = "data-mfg-section" in a or any(s for _, s in self.stack)
            self.links.append((self.getpos()[0], bool(a.get("data-mfg-item")), inside, a.get("href", "")))
        if tag not in VOID:
            self.stack.append((tag, "data-mfg-section" in a))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


def faults(path, text):
    """[(message)] for each unlabelled download link in one page's text; also the number of download links."""
    f = Finder()
    f.feed(text)
    f.close()
    out = []
    for line, has_item, inside, href in f.links:
        if not has_item:
            out.append("%s:%d: download link %r has no data-mfg-item" % (path, line, href))
        if not inside:
            out.append("%s:%d: download link %r is not inside a data-mfg-section" % (path, line, href))
    return out, len(f.links)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def main():
    found, total, pages, plant_page = [], 0, 0, None
    for p in served_html():
        got, n = faults(p, read(p))
        found += got
        total += n
        pages += 1 if n else 0
        if n and not got and plant_page is None:
            plant_page = p
    print("download links on served pages: %d, on %d page(s)" % (total, pages))
    ok = True
    if found:
        ok = False
        print("FAIL: unlabelled download links (label each: data-mfg-item on the link, data-mfg-section on a container)")
        for m in found:
            print("  -", m)

    print("planted faults (in a copy of %s)" % plant_page)
    if plant_page is None:
        print("  STALE PLANT: no served page has a labelled download link to plant in")
        sys.exit(1)
    src = read(plant_page)
    plants = [
        ("one download link's data-mfg-item removed", ITEM_ON_DOWNLOAD, r"\1", 1),
        ("the page's data-mfg-section labels removed", SECTION, "", 0),
    ]
    for name, pattern, repl, count in plants:
        try:
            planted = pc.apply_re_plant(src, pattern.pattern, repl, name=name, count=count)
            got, err = faults(plant_page, planted)[0], None
        except pc.StalePlant as e:
            print("  " + str(e))
            ok = False
            continue
        except Exception as e:  # an error is never a catch
            got, err = [], e
        if pc.is_caught(got, err):
            print("  caught: %s (%s)" % (name, got[0]))
        else:
            print("  NOT CAUGHT: %s%s" % (name, " (error: %r)" % err if err else ""))
            ok = False

    if not ok:
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
