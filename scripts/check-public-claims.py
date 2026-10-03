#!/usr/bin/env python3
"""Does any live page claim that no data is collected?

    python scripts/check-public-claims.py               # CI
    python scripts/check-public-claims.py --root <copy of the repo>   # testing

Until 3 Oct 2026 the About page said "No data collected — GDPR compliant", and the portal's
header badge and both pages' meta and og: descriptions said "no data collected". It was never
true: the site records anonymous gameplay statistics (GA4, cookieless, and the Events sheet),
as the privacy page says. Nothing tied the public wording to the privacy page, so it drifted.
The approved wording is "No sign-up, no personal data. We record anonymous gameplay statistics
to improve the games. See our privacy page for exactly what." (or "No sign-up, no personal
data" where space is tight). "No personal data" is true and is not caught.

Live pages are the files GitHub Pages publishes, decided exactly as check-publish-scope.py
decides it (canon §7.7: tracked, no ./_ path component, not in _config.yml's exclude list),
read if their extension is one of TEXT. Each file is read twice: as raw text with entities
decoded (so meta/og: attributes and script strings are read) and with tags removed (so a claim
split by markup, "No data <b>collected</b>", is read too). Case-insensitive, whitespace
collapsed. The patterns are in PATTERNS below.

Fails on a match not in KNOWN, and on a KNOWN entry that no longer matches (stale). KNOWN
entries are reported, never fail: each is a live claim awaiting Jon's ruling.

Stdlib only; about a second. A self-test runs first on every run.
"""
import argparse, fnmatch, html, pathlib, re, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
TEXT = (".html", ".js", ".mjs", ".json", ".xml", ".webmanifest", ".txt", ".css")

_SUBJ = r"(?:(?:student|pupil|user|player)s?'?\s+)?"
PATTERNS = [
    # "no data collected", "no data is stored", "no data are recorded"
    r"\bno\s+" + _SUBJ + r"data\s+(?:is\s+|are\s+|gets\s+|will\s+be\s+)?(?:collected|recorded|stored|tracked|gathered|kept|logged)\b",
    # "no data collection"
    r"\bno\s+" + _SUBJ + r"data\s+collection\b",
    # "collects no data", "records zero student data", "collect nothing"
    r"\b(?:collect|record|store|track|gather|log)(?:s|ing)?\s+(?:no|zero)\s+" + _SUBJ + r"data\b",
    r"\b(?:collect|record|store|track|gather|log)(?:s|ing)?\s+nothing\b",
    # "zero data", "zero student data"
    r"\bzero\s+" + _SUBJ + r"data\b",
    # "we don't collect any data", "never records data"
    r"\b(?:don'?t|doesn'?t|do\s+not|does\s+not|never)\s+(?:collect|record|store|track|gather|log)s?\s+(?:any\s+)?(?:data|anything)\b",
    # "nothing is collected", "nothing tracked"
    r"\bnothing\s+(?:is\s+)?(?:collected|recorded|stored|tracked|logged)\b",
    # "data-free", "no tracking"
    r"\bdata[\s-]free\b",
    r"\bno\s+tracking\b",
]
COMPILED = [re.compile(p, re.I) for p in PATTERNS]

# Live claims awaiting Jon's ruling: (path, exact matched text, lower case). Reported, never fail;
# a stale entry fails. Remove the entry in the PR that rewords the claim.
KNOWN = {
    ("about/index.html", "collects zero student data"):
        "the bio's fourth paragraph, which the 3 Oct 2026 contract put out of scope; Jon to rule",
}

TAG = re.compile(r"<[^>]+>")
COMMENT = re.compile(r"<!--.*?-->", re.S)
# Code comments are not public text: /* block */ anywhere, and // line comments that start a line
# or follow whitespace or ; { } (so "https://" in a string is kept).
CODE_COMMENT = re.compile(r"/\*.*?\*/|(?:^|(?<=[\s;{}]))//[^\n]*", re.S | re.M)


def read_excludes(text):
    """The `exclude:` list from _config.yml (the same reader as check-publish-scope.py)."""
    out, inside = [], False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            inside = line.rstrip() == "exclude:"
            continue
        if inside:
            m = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if m:
                out.append(m.group(1).strip("'\""))
    return out


def published(path, patterns):
    if any(part[:1] in "._#~" for part in path.split("/")):
        return False
    return not any(fnmatch.fnmatchcase(path, p) or path.startswith(p) for p in patterns)


def live_files(root):
    try:
        out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True)
        files = [f for f in out.stdout.decode("utf-8").split("\0") if f]
    except (OSError, subprocess.CalledProcessError):      # a plain copy (testing): walk it
        files = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    patterns = read_excludes((root / "_config.yml").read_text(encoding="utf-8"))
    if not patterns:
        raise SystemExit("_config.yml has no exclude list")
    return sorted(f for f in files if f.lower().endswith(TEXT) and published(f, patterns))


def normalise(s):
    return re.sub(r"\s+", " ", html.unescape(s).replace("’", "'"))


def claims(text):
    """Every distinct matched phrase (lower case) in one file's text. A phrase inside a longer
    match is the same claim ("zero student data" in "collects zero student data"): kept once."""
    text = CODE_COMMENT.sub(" ", text)
    views = [normalise(text), normalise(TAG.sub(" ", COMMENT.sub(" ", text)))]
    found = set()
    for v in views:
        for rx in COMPILED:
            found.update(re.sub(r"\s+", " ", m.group(0)).lower() for m in rx.finditer(v))
    return {p for p in found if not any(p != q and p in q for q in found)}


def check(found_by_file, known):
    errors, reported = [], []
    for path, phrases in sorted(found_by_file.items()):
        for p in sorted(phrases):
            if (path, p) in known:
                reported.append((path, p, known[(path, p)]))
            else:
                errors.append('%s: says "%s", a no-data claim the site cannot make (it records '
                              'anonymous gameplay statistics; see the privacy page). Use "No sign-up, '
                              'no personal data" or the full approved wording.' % (path, p))
    for (path, p) in sorted(known):
        if p not in found_by_file.get(path, set()):
            errors.append('%s: KNOWN entry "%s" no longer matches: remove it from KNOWN' % (path, p))
    return errors, reported


def selftest():
    must = [
        '<meta name="description" content="No sign-up, no data collected.">',
        "<li>No data collected &mdash; GDPR compliant</li>",
        "No data <b>collected</b>",
        "and collects zero student data.",
        "Zero data, ever",
        "We don&rsquo;t collect any data",
        "it collects nothing",
        "nothing is tracked",
        "A data-free site",
        "no tracking",
        "No user data is stored",
        "<span>No\n  Data\n  Collected</span>",
        "no data collection",
        "<script>var s = 'No data is stored';</script>",
        '<a href="https://example.com/">No data collected</a>',
    ]
    mustnot = [
        "No sign-up, no personal data. We record anonymous gameplay statistics to improve the games.",
        "Playing MaffsGames collects no personal data.",
        "No personal data is collected",
        "no admin panel, no class codes, no data dashboard.",
        "They are not used for tracking.",
        "Gameplay data can't be linked to an individual.",
        "} catch (e) { /* private mode, or nothing stored yet */ }",
        "x = 1; // nothing is tracked here",
    ]
    assert claims("and collects zero student data.") == {"collects zero student data"}
    for s in must:
        assert claims(s), "should match: %r" % s
    for s in mustnot:
        assert not claims(s), "should not match: %r -> %s" % (s, claims(s))
    k = {("a.html", "zero data"): "why"}
    assert check({"a.html": {"zero data"}}, k) == ([], [("a.html", "zero data", "why")])
    assert len(check({"a.html": {"zero data", "no tracking"}}, k)[0]) == 1    # new claim fails
    assert len(check({}, k)[0]) == 1                                          # stale entry fails
    pats = ["scripts", "docs/*.md"]
    assert published("about/index.html", pats) and not published("docs/x.md", pats)
    assert not published(".claude/rules/x.md", pats) and not published("scripts/a.py", pats)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # a Windows console is cp1252
    selftest()
    root = pathlib.Path(args.root).resolve()
    files = live_files(root)
    found = {}
    for f in files:
        hits = claims((root / f).read_text(encoding="utf-8", errors="replace"))
        if hits:
            found[f] = hits
    errors, reported = check(found, KNOWN)

    print("Live text files read: %d. Patterns: %d (case-insensitive)." % (len(files), len(PATTERNS)))
    for path, p, why in reported:
        print('  KNOWN (reported, never fails)  %s: "%s" -- %s' % (path, p, why))
    for e in errors:
        print("FAIL  %s" % e)
    if errors:
        print("\n%d problem(s)." % len(errors))
        return 1
    print("\nOK  no live page claims that no data is collected%s."
          % (" (beyond the %d KNOWN above)" % len(reported) if reported else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
