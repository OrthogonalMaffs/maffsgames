#!/usr/bin/env python3
# ci-line: Download links labelled (every <a download> and every data-mfg-download button on a served page has data-mfg-item inside a data-mfg-section, so analytics.js counts it as section_clicked action download; a page that builds a download in script has a labelled button; planted faults caught) |
# ci-deps: any-page _config.yml scripts/check-publish-scope.py
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

Button downloads (contract UGH-STATS-BUTTON-DOWNLOADS, 21 Nov 2026). A page can also build a file in the browser and
hand it over from a button: its handler calls a helper's download() (the Ugh, stats helper, the only one), which clicks
a temporary unlabelled <a download> outside every section, so the listener counts the button instead, when it carries
data-mfg-download (any element but an <a>, whose download attribute already says it). Also fails when (a) an element
with data-mfg-download has no data-mfg-item or no data-mfg-section ancestor, or (b) a served page's own script calls
<name>.download( but the page has no data-mfg-download element. Two more plants, in a copy of the first served page
with a labelled download button: the button's data-mfg-item removed; its data-mfg-download removed.

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
# A script call that builds a download in the browser: <helper>.download( (a page's own script; the attribute
# download="..." or a.download = name is not a call).
SCRIPT_DOWNLOAD = re.compile(r'\b[A-Za-z_$][\w$]*\.download\s*\(')
ITEM_ON_BUTTON = re.compile(r'(<(?!a\b)[a-z]+\b[^>]*?)\sdata-mfg-item="[^"]+"(?=[^>]*\sdata-mfg-download\b)')
BUTTON_FLAG = re.compile(r'\sdata-mfg-download\b(?!-)(?:="[^"]*")?')


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
    """Each <a download>: (line, has data-mfg-item, inside a data-mfg-section, href); each other element with
    data-mfg-download: (line, has data-mfg-item, inside a data-mfg-section, tag); and the page's script text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []      # [(tag, opens a section)]
        self.links = []
        self.buttons = []
        self.script = []

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] == "script":
            self.script.append(data)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        inside = "data-mfg-section" in a or any(s for _, s in self.stack)
        if tag == "a" and "download" in a:
            self.links.append((self.getpos()[0], bool(a.get("data-mfg-item")), inside, a.get("href", "")))
        elif "data-mfg-download" in a:
            self.buttons.append((self.getpos()[0], bool(a.get("data-mfg-item")), inside, tag))
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
    for line, has_item, inside, tag in f.buttons:
        if not has_item:
            out.append("%s:%d: download button <%s data-mfg-download> has no data-mfg-item" % (path, line, tag))
        if not inside:
            out.append("%s:%d: download button <%s data-mfg-download> is not inside a data-mfg-section" % (path, line, tag))
    calls = SCRIPT_DOWNLOAD.findall("".join(f.script))
    if calls and not f.buttons:
        out.append("%s: its script calls %s but no element has data-mfg-download, so that download is never counted"
                   % (path, calls[0].strip()))
    return out, len(f.links) + len(f.buttons)


def buttons(text):
    f = Finder()
    f.feed(text)
    f.close()
    return len(f.buttons)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def main():
    found, total, pages, plant_page, button_page = [], 0, 0, None, None
    for p in served_html():
        text = read(p)
        got, n = faults(p, text)
        found += got
        total += n
        pages += 1 if n else 0
        nb = buttons(text) if n else 0
        if n and not got and nb == 0 and plant_page is None:
            plant_page = p
        if nb and not got and button_page is None:
            button_page = p
    print("downloads on served pages (links and data-mfg-download buttons): %d, on %d page(s)" % (total, pages))
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
    print("button plants (in a copy of %s)" % button_page)
    if button_page is None:
        print("  STALE PLANT: no served page has a labelled download button to plant in")
        sys.exit(1)
    plants = [
        (plant_page, "one download link's data-mfg-item removed", ITEM_ON_DOWNLOAD, r"\1", 1),
        (plant_page, "the page's data-mfg-section labels removed", SECTION, "", 0),
        (button_page, "a download button's data-mfg-item removed", ITEM_ON_BUTTON, r"\1", 1),
        (button_page, "the page's data-mfg-download removed (its script still calls download)", BUTTON_FLAG, "", 0),
    ]
    for page, name, pattern, repl, count in plants:
        try:
            planted = pc.apply_re_plant(read(page), pattern.pattern, repl, name=name, count=count)
            got, err = faults(page, planted)[0], None
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
