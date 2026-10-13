#!/usr/bin/env python3
"""The GA4 tag is loaded by schools/assets/analytics.js only, and only on the live host (GA4-LIVE-ONLY, 12 Oct 2026).

    python scripts/check-analytics-loader.py
    python scripts/check-analytics-loader.py --selftest

Until 12 Oct 2026 every page carried its own copy of the gtag snippet with no hostname check, so any browser that
opened a page sent a page view to GA4 (test runs, local servers, previews). This check holds the fix in place:
  1. no published page contains the tag: not `googletagmanager.com/gtag`, not `gtag('config'`, not the measurement ID inside a script
     (/privacy/ names the ID in plain text, which is wording, not a tag);
  2. every published page loads analytics.js exactly once (redirect stubs and noindex pages are the only exceptions);
  3. analytics.js loads the tag, and only inside the hostname gate (maffsgames.co.uk and www.maffsgames.co.uk).
A "published page" is a tracked .html file under a SITE path that _config.yml does not exclude (check-publish-scope.py).
"""
import importlib.util, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET = "schools/assets/analytics.js"
ID = "G-992JLHLP2D"
SNIPPET_MARKS = ("googletagmanager.com/gtag", "gtag('config'", 'gtag("config"')
SCRIPT = re.compile(r"<script[^>]*>.*?</script>", re.I | re.S)
INCLUDE = re.compile(r'<script\b[^>]*\bsrc="([^"]*analytics\.js[^"]*)"[^>]*>', re.I)
HOSTS = ("maffsgames.co.uk", "www.maffsgames.co.uk")


def scope_module():
    spec = importlib.util.spec_from_file_location("check_publish_scope", os.path.join(ROOT, "scripts", "check-publish-scope.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def published_pages():
    """{path: text} for every published .html page."""
    ps = scope_module()
    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as f:
        excl = ps.read_excludes(f.read())
    out = {}
    tracked = subprocess.run(["git", "ls-files", "*.html"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    for p in sorted(tracked):
        if ps.is_site(p) and not ps.excluded(p, excl) and not ps.special(p):
            with open(os.path.join(ROOT, p), encoding="utf-8") as f:
                out[p] = f.read()
    return out


# Withdrawn pages: a holding page with no tracking of its own. Naming them keeps every other noindex page (the
# unlisted games, the teacher pages) held to the rule.
WITHDRAWN = {"escape-rooms/it-vengeance/teacher.html", "games/regression-rumble/index.html"}


def exempt(path, text):
    """A redirect stub or a withdrawn holding page: it sends nothing to GA4 and has no <head> to load analytics.js in."""
    return path in WITHDRAWN or bool(re.search(r'http-equiv="refresh"', text, re.I)
                                     or (len(text) < 600 and "location.replace(" in text))


def resolves(page, src):
    src = src.split("?", 1)[0].split("#", 1)[0]
    if src.startswith("/"):
        path = src.lstrip("/")
    else:
        parts = page.split("/")[:-1]
        for seg in src.split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg not in ("", "."):
                parts.append(seg)
        path = "/".join(parts)
    return path == ASSET


def loader_problems(js):
    """Problems with analytics.js: the loader must exist and sit inside the hostname gate."""
    out = []
    i = js.find("googletagmanager.com/gtag/js")
    if i < 0:
        return ["analytics.js does not load the GA4 tag (no googletagmanager.com/gtag/js)"]
    if ID not in js:
        out.append("analytics.js does not carry the measurement ID")
    gate = re.search(r"var LIVE = ([^;]+);", js)
    if not gate or not all(("'%s'" % h) in gate.group(1) and "location.hostname" in gate.group(1) for h in HOSTS):
        out.append("analytics.js: LIVE is not the maffsgames.co.uk / www.maffsgames.co.uk hostname test")
    # the nearest `if (` before the loader must be `if (LIVE)`
    ifs = list(re.finditer(r"\bif \(([^)]*)\)", js[:i]))
    if not ifs or ifs[-1].group(1).strip() != "LIVE":
        out.append("analytics.js: the GA4 loader is not inside `if (LIVE)`, the hostname gate")
    if "mfg" in js and "var host = location.hostname;" not in js:
        out.append("analytics.js: mfg()'s own hostname gate is missing")
    return out


def problems(pages, js):
    out = []
    for p, t in pages.items():
        # The measurement ID is flagged inside a <script> element only: /privacy/ names it in plain text, which is
        # public wording (canon §1), not a tag.
        marks = [m for m in SNIPPET_MARKS if m in t] + ([ID] if any(ID in s.group(0) for s in SCRIPT.finditer(t)) else [])
        if marks:
            out.append("%s: carries its own copy of the GA4 tag (%s); it belongs in analytics.js only" % (p, marks[0]))
        if "Google Analytics (cookieless)" in t:
            out.append("%s: keeps the orphan 'Google Analytics (cookieless)' comment; scripts/apply-analytics-loader.py removes it" % p)
        incs = INCLUDE.findall(t)
        if exempt(p, t):
            continue
        if len(incs) != 1:
            out.append("%s: loads analytics.js %d times (want exactly once)" % (p, len(incs)))
        elif not resolves(p, incs[0]):
            out.append("%s: its analytics.js include %r does not resolve to %s" % (p, incs[0], ASSET))
    return out + loader_problems(js)


def selftest(pages, js):
    fails = []

    def check(name, ok):
        print("  %s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails.append(name)

    page = next(p for p, t in pages.items() if not exempt(p, t) and "/" in p)
    base = dict(pages)
    check("the real files are clean", not problems(base, js))
    snip = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
            "<script>gtag('config','%s',{});</script>" % (ID, ID))
    p = problems(dict(base, **{page: base[page].replace("</head>", snip + "</head>", 1)}), js)
    check("PLANT: a page with the snippet back is caught", any("carries its own copy" in x for x in p))
    p = problems(dict(base, **{page: base[page].replace("</head>", "<script>var id='%s';</script></head>" % ID, 1)}), js)
    check("PLANT: the measurement ID inside a script is caught", any("carries its own copy" in x for x in p))
    p = problems(dict(base, **{page: base[page].replace("</head>", "<!-- Google Analytics (cookieless) -->\n</head>", 1)}), js)
    check("PLANT: the orphan comment back is caught", any("orphan" in x for x in p))
    check("the ID as plain text (as on /privacy/) is not flagged",
          not problems(dict(base, **{page: base[page].replace("</body>", "<p><code>%s</code></p></body>" % ID, 1)}), js))
    inc = INCLUDE.search(base[page]).group(0)
    p = problems(dict(base, **{page: base[page].replace(inc, inc + inc, 1)}), js)
    check("PLANT: a page with analytics.js twice is caught", any("2 times" in x for x in p))
    p = problems(dict(base, **{page: base[page].replace(inc, "", 1)}), js)
    check("PLANT: a page with no analytics.js is caught", any("0 times" in x for x in p))
    p = problems(dict(base, **{page: base[page].replace(inc, '<script src="analytics.js"></script>', 1)}), js)
    check("PLANT: an include that points elsewhere is caught", any("does not resolve" in x for x in p))
    check("PLANT: analytics.js with the gate removed is caught",
          any("not inside" in x for x in loader_problems(js.replace("if (LIVE) {", "if (true) {", 1))))
    check("PLANT: analytics.js with no loader is caught", bool(loader_problems(js.replace("googletagmanager.com/gtag/js", "x"))))
    check("a redirect stub with no analytics.js is not flagged",
          not problems({"year6/index.html": "<html><head></head><body><script>window.location.replace('/op/');</script></body></html>"},
                       js))
    check("a noindex page that is not withdrawn is still held to the rule",
          any("0 times" in x for x in problems({"games/x/index.html": '<meta name="robots" content="noindex"><p>game</p>'}, js)))
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main(argv):
    pages = published_pages()
    with open(os.path.join(ROOT, ASSET), encoding="utf-8") as f:
        js = f.read()
    if argv == ["--selftest"]:
        return selftest(pages, js)
    found = problems(pages, js)
    for x in found:
        print("FAIL  " + x)
    n = sum(1 for p, t in pages.items() if not exempt(p, t))
    print("%s: %d published pages, %d load analytics.js once and carry no tag of their own; analytics.js loads the tag on the live host only"
          % ("FAILED" if found else "PASS", len(pages), n))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
