#!/usr/bin/env python3
"""Move the GA4 tag out of every page and into schools/assets/analytics.js (GA4-LIVE-ONLY, 12 Oct 2026).

    python scripts/apply-analytics-loader.py            # apply
    python scripts/apply-analytics-loader.py --dry-run  # report only

Each published page carried its own copy of the gtag snippet in <head>, with no hostname check, so any browser
that opened a page (a test run, a local server, a preview) sent a page view to GA4. analytics.js now loads the tag,
on maffsgames.co.uk only. This script, in the pattern of apply-footer.py / apply-meta.py:
  1. removes the snippet's two <script> tags (the async gtag.js loader and the inline config) from every page;
  2. makes sure the page loads analytics.js exactly once: a page that already does is left alone, and the include
     must resolve to schools/assets/analytics.js; a page that does not (about, feedback, leaderboards, privacy,
     spec map) gets one, in the snippet's place, at its own relative path.
Nothing else in a page is touched. Idempotent: a page with no snippet is skipped.
"""
import os, posixpath, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = "G-992JLHLP2D"
ASSET = "schools/assets/analytics.js"
SNIPPET = re.compile(r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=%s"></script>\s*<script>.*?</script>(\r?\n)'
                     % ID, re.S)
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="([^"]*analytics\.js[^"]*)"[^>]*>')


def pages():
    out = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return sorted(out)


def resolves(page, src):
    """True if `src`, written on `page`, points at schools/assets/analytics.js."""
    src = src.split("?", 1)[0].split("#", 1)[0]
    path = src.lstrip("/") if src.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(page), src))
    return path == ASSET


def main(dry):
    changed, added, kept, stray = [], [], [], []
    for page in pages():
        with open(os.path.join(ROOT, page), encoding="utf-8", newline="") as f:
            text = f.read()
        if ID not in text:
            continue
        ms = list(SNIPPET.finditer(text))
        if len(ms) != 1:
            stray.append("%s: %d snippets matched but the ID appears (not the expected shape)" % (page, len(ms)))
            continue
        incs = INCLUDE.findall(SNIPPET.sub("", text))
        if len(incs) > 1:
            stray.append("%s: analytics.js included %d times" % (page, len(incs)))
            continue
        if incs and not resolves(page, incs[0]):
            stray.append("%s: analytics.js include %r does not resolve to %s" % (page, incs[0], ASSET))
            continue
        nl = "\r\n" if "\r\n" in ms[0].group(0) else "\n"
        if incs:
            repl, kept_ = "", True
        else:
            depth = page.count("/")
            repl, kept_ = '<script src="%s%s"></script>%s' % ("../" * depth, ASSET, nl), False
        new = text[:ms[0].start()] + repl + text[ms[0].end():]
        (kept if kept_ else added).append(page)
        changed.append(page)
        if not dry:
            with open(os.path.join(ROOT, page), "w", encoding="utf-8", newline="") as f:
                f.write(new)
    print("pages changed: %d (snippet removed, existing include kept: %d; include added: %d)" % (len(changed), len(kept), len(added)))
    for p in added:
        print("  include added: " + p)
    for s in stray:
        print("  STOP: " + s)
    return 1 if stray else 0


if __name__ == "__main__":
    sys.exit(main("--dry-run" in sys.argv))
