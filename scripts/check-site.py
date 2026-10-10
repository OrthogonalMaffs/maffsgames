#!/usr/bin/env python3
"""Whole-site checker: does every page actually RUN?

WHY THIS EXISTS
---------------
`check-leaderboard-coverage.js` verifies that code *exists*. It cannot tell you
whether that code *runs*. Two site-wide sweeps (96381d74 and 76514c70, both
2026-03-22) left `chart-interrogator` and `modular-battle` unable to start at
all, and both games passed the coverage check every time it ran for the six
months they were dead. `modular-battle` additionally shipped a rejection-sampling
loop that froze the tab outright on ~25% of questions (1a407fe); expectation-station
had a latent one of the same shape.

So this script adds the missing layer, in two tiers:

  Tier 1 (browser)  Load every page in headless Chromium and fail on anything
                    that proves the page is broken: an uncaught exception, a
                    console.error, a 404 on a local asset, or a main thread that
                    stops answering (an infinite loop). Then press every game's
                    every level button in a fresh page and fail unless the game
                    starts (see "Tier 1, level controls" below).

  Tier 2 (static)   Read every inline <script> and every room.js and flag the
                    rejection-sampling shape that caused the freeze: a loop whose
                    exit depends on a collection growing, whose body draws random
                    values, and which has no counter that advances regardless of
                    the draw. Such a loop terminates only by luck.

THE NETWORK GUARD
-----------------
Mandatory in every mode, including --live. Every request to the Apps Script
endpoint, to Google Analytics/gtag collect, and to Firebase is aborted before it
leaves the machine, over HTTP and WebSocket alike. Checking a page must never
write a row into the production Events sheet or a score into the live
leaderboard. Every blocked request is logged, and the run FAILS if even one
request to a write host completes.

USAGE
-----
    python scripts/check-site.py                 # tiers 1 + 2 against a local stub server
    python scripts/check-site.py --tier 2        # static scan only, no browser
    python scripts/check-site.py --live          # tier 1 against the deployed site
    python scripts/check-site.py --only modular-battle
    python scripts/check-site.py --workers 8

Exit code 0 = no FAILs. Exit code 1 = at least one FAIL. WARNs never fail a run.

Node is not installed on the Windows machine, so this is Python + Playwright.
Install once with:  pip install playwright && python -m playwright install chromium
"""
import argparse
import asyncio
import json
import os
import random
import re
import sys
import time
from urllib.parse import urlparse, urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402  (roster level table; no esprima needed to import it)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWLIST_PATH = os.path.join(ROOT, "scripts", "checker-allowlist.json")
LIVE_ORIGIN = "https://maffsgames.co.uk"

# ---------------------------------------------------------------------------
# Network guard
# ---------------------------------------------------------------------------

# Read-only CDNs the pages legitimately need. Checked BEFORE the block list, so
# www.gstatic.com (the Firebase SDK bundle) loads while the database hosts below
# stay blocked -- we want the real SDK to run and then find the door shut, which
# is a truer test than never loading it.
ALLOW_HOST_SUFFIXES = (
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "www.gstatic.com",
    "unpkg.com",
)

# Anything that could write. Host suffix match.
BLOCK_HOST_SUFFIXES = (
    "script.google.com",              # the Apps Script endpoint in analytics.js
    "script.googleusercontent.com",
    "google-analytics.com",
    "analytics.google.com",
    "googletagmanager.com",
    "doubleclick.net",
    "firebaseio.com",
    "firebasedatabase.app",
    "firebaseapp.com",
    "firebasestorage.app",
    "firebaseinstallations.googleapis.com",
    "firebaseremoteconfig.googleapis.com",
    "identitytoolkit.googleapis.com",
    "securetoken.googleapis.com",
)

# Collect endpoints that live on otherwise-innocent hosts.
BLOCK_PATH_SUBSTRINGS = ("/ccm/collect", "/g/collect", "/gtag/js", "/gtm.js")

LOCAL_HOSTS = ("127.0.0.1", "localhost")


def host_of(url):
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def suffix_match(host, suffixes):
    return any(host == s or host.endswith("." + s) for s in suffixes)


def block_reason(url):
    """Return a reason string if this URL must not leave the machine, else None."""
    scheme = urlsplit(url).scheme.lower()
    if scheme in ("data", "blob", "about", "chrome-extension"):
        return None
    host = host_of(url)
    if not host or host in LOCAL_HOSTS:
        return None
    if suffix_match(host, ALLOW_HOST_SUFFIXES):
        return None
    if suffix_match(host, BLOCK_HOST_SUFFIXES):
        return "write host " + host
    path = urlsplit(url).path or ""
    for frag in BLOCK_PATH_SUBSTRINGS:
        if frag in path:
            return "telemetry path " + frag
    return None


def is_write_host(url):
    """Used to prove nothing escaped: did a request to a write host COMPLETE?"""
    host = host_of(url)
    if suffix_match(host, ALLOW_HOST_SUFFIXES):
        return False
    if suffix_match(host, BLOCK_HOST_SUFFIXES):
        return True
    path = urlsplit(url).path or ""
    return any(frag in path for frag in BLOCK_PATH_SUBSTRINGS)


# ---------------------------------------------------------------------------
# JavaScript source hygiene -- strip comments and string bodies
# ---------------------------------------------------------------------------

def strip_js_noise(src):
    """Blank out comments, string and template bodies, and regex literals.

    Replaces them with spaces rather than deleting them, so every byte offset --
    and therefore every line number -- in the result still matches the original.

    This matters more than it looks. expectation-station carries a comment that
    quotes the very loop this scanner hunts ("while (distractors.length < target)")
    as a note explaining why it was removed. Scanning raw text flags the comment
    and calls a fixed file broken.
    """
    out = list(src)
    i, n = 0, len(src)
    # Tracks whether a '/' starts a regex literal or is a division sign.
    prev_significant = ""

    def blank(start, end):
        for k in range(start, min(end, n)):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""

        if c == "/" and nxt == "/":
            j = src.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
            continue

        if c == "/" and nxt == "*":
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            blank(i, j)
            i = j
            continue

        if c in ("'", '"'):
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == c or src[j] == "\n":
                    break
                j += 1
            blank(i + 1, j)
            i = min(j + 1, n)
            prev_significant = "x"
            continue

        if c == "`":
            # Template literal. Keep ${...} expressions -- they are real code and
            # can hold real loops -- but blank the literal text around them.
            j = i + 1
            seg = j
            depth = 0
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if depth == 0 and src[j] == "$" and j + 1 < n and src[j + 1] == "{":
                    blank(seg, j)
                    depth = 1
                    j += 2
                    continue
                if depth > 0:
                    if src[j] == "{":
                        depth += 1
                    elif src[j] == "}":
                        depth -= 1
                        if depth == 0:
                            seg = j + 1
                    j += 1
                    continue
                if src[j] == "`":
                    break
                j += 1
            if depth == 0:
                blank(seg, j)
            i = min(j + 1, n)
            prev_significant = "x"
            continue

        if c == "/" and prev_significant in ("", "=", "(", ",", ":", "[", "!", "&",
                                             "|", "?", "{", "}", ";", "+", "-",
                                             "*", "%", "~", "^", "<", ">", "\n"):
            # Regex literal.
            j = i + 1
            in_class = False
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == "[":
                    in_class = True
                elif src[j] == "]":
                    in_class = False
                elif src[j] == "/" and not in_class:
                    break
                elif src[j] == "\n":
                    break
                j += 1
            blank(i, min(j + 1, n))
            i = min(j + 1, n)
            prev_significant = "x"
            continue

        if not c.isspace():
            prev_significant = c
        i += 1

    return "".join(out)


def extract_inline_scripts(html):
    """Yield (js_source_padded, ) for each inline <script> block.

    The source is returned padded with spaces to the full length of the document
    so that offsets -- and line numbers -- stay true to the original file.
    """
    padded = [" " if ch != "\n" else "\n" for ch in html]
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script\s*>", html,
                         re.IGNORECASE | re.DOTALL):
        attrs = m.group(1)
        if re.search(r'\bsrc\s*=', attrs, re.IGNORECASE):
            continue  # external file, not inline
        t = re.search(r'\btype\s*=\s*["\']?([^"\'\s>]+)', attrs, re.IGNORECASE)
        if t and t.group(1).lower() not in ("text/javascript", "module",
                                            "application/javascript"):
            continue  # a data block or template, not code
        body = m.group(2)
        start = m.start(2)
        for k, ch in enumerate(body):
            padded[start + k] = ch
    return "".join(padded)


# ---------------------------------------------------------------------------
# Function-scope resolution -- so the allowlist can key on a name, not a line
# ---------------------------------------------------------------------------

FUNC_PATTERNS = (
    re.compile(r"\bfunction\s*\*?\s*([A-Za-z_$][\w$]*)\s*\("),
    re.compile(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?function\b"),
    re.compile(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^()]*\)\s*=>"),
    re.compile(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?[A-Za-z_$][\w$]*\s*=>"),
    re.compile(r"\b([A-Za-z_$][\w$]*)\s*:\s*(?:async\s*)?function\b"),
    re.compile(r"^\s{2,}(?:async\s+)?([A-Za-z_$][\w$]*)\s*\([^()]*\)\s*\{", re.MULTILINE),
)


def match_brace(src, open_idx):
    depth = 0
    for k in range(open_idx, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return k
    return len(src)


def build_scopes(src):
    """Return [(start, end, name)] for every function-ish body found in src."""
    scopes = []
    for pat in FUNC_PATTERNS:
        for m in pat.finditer(src):
            name = m.group(1)
            brace = src.find("{", m.end() - 1)
            if brace == -1 or brace - m.end() > 200:
                continue
            end = match_brace(src, brace)
            scopes.append((brace, end, name))
    return scopes


def enclosing_function(scopes, pos):
    """Innermost named function containing pos, or '(top level)'."""
    best = None
    for start, end, name in scopes:
        if start <= pos <= end:
            if best is None or (end - start) < (best[1] - best[0]):
                best = (start, end, name)
    return best[2] if best else "(top level)"


# ---------------------------------------------------------------------------
# Tier 2 -- the rejection-sampling scan
# ---------------------------------------------------------------------------

RANDOM_CALL = re.compile(r"\bMath\s*\.\s*random\s*\(")
SIZE_IN_COND = re.compile(r"\.\s*(?:length|size)\b")
UPDATE_VARS = re.compile(r"([A-Za-z_$][\w$]*)\s*(?:\+\+|--)|(?:\+\+|--)\s*([A-Za-z_$][\w$]*)"
                         r"|([A-Za-z_$][\w$]*)\s*(?:\+=|-=|\*=|/=)")


def random_helpers(src):
    """Names of functions in this file whose own body reaches Math.random.

    Resolved transitively, because modular-battle's loop drew through randInt
    rather than calling Math.random directly -- a scanner that only looks for
    the literal call misses the exact bug it was written to catch.
    """
    scopes = build_scopes(src)
    bodies = {}
    for start, end, name in scopes:
        body = src[start:end]
        # Keep the smallest body for a given name (innermost definition).
        if name not in bodies or len(body) < len(bodies[name]):
            bodies[name] = body
    direct = {n for n, b in bodies.items() if RANDOM_CALL.search(b)}
    changed = True
    while changed:
        changed = False
        for name, body in bodies.items():
            if name in direct:
                continue
            for cand in direct:
                if re.search(r"\b" + re.escape(cand) + r"\s*\(", body):
                    direct.add(name)
                    changed = True
                    break
    return direct


def body_draws_random(body, helpers):
    if RANDOM_CALL.search(body):
        return "Math.random"
    for h in helpers:
        if re.search(r"\b" + re.escape(h) + r"\s*\(", body):
            return h + "() -> Math.random"
    return None


def split_for_header(header):
    """Split a for(...) header on top-level semicolons."""
    parts, depth, cur = [], 0, []
    for ch in header:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == ";" and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def paren_span(src, open_idx):
    depth = 0
    for k in range(open_idx, len(src)):
        if src[k] == "(":
            depth += 1
        elif src[k] == ")":
            depth -= 1
            if depth == 0:
                return k
    return -1


def body_span(src, after_idx):
    """Extent of a loop body starting at/after after_idx."""
    k = after_idx
    while k < len(src) and src[k].isspace():
        k += 1
    if k < len(src) and src[k] == "{":
        return k, match_brace(src, k)
    end = src.find(";", k)
    return k, (len(src) if end == -1 else end)


def has_fixed_bound(cond, update):
    """True if a counter advances every iteration regardless of the random draw.

    This is the whole discriminator, and getting it wrong in either direction
    defeats the check. A Fisher-Yates shuffle reads `arr.length` in its condition
    and calls Math.random in its body -- identical on the surface to the loop that
    froze modular-battle. What separates them is that the shuffle's `i--` runs on
    every pass, so the loop is bounded no matter what the draw returns, whereas
    `while (choices.size < 4)` advances only when the draw happens to be new.
    """
    if not update.strip():
        return False
    names = set()
    for m in UPDATE_VARS.finditer(update):
        names.update(g for g in m.groups() if g)
    return any(re.search(r"\b" + re.escape(nm) + r"\b", cond) for nm in names)


def scan_source(src, relpath):
    """Find rejection-sampling loops. src must already be comment/string-stripped."""
    helpers = random_helpers(src)
    scopes = build_scopes(src)
    hits = []

    for m in re.finditer(r"\b(while|for|do)\b", src):
        kw = m.group(1)
        if kw == "do":
            bstart, bend = body_span(src, m.end())
            wm = re.compile(r"\s*while\s*\(").match(src, bend + 1)
            if not wm:
                continue
            popen = src.find("(", bend)
            pclose = paren_span(src, popen)
            if pclose == -1:
                continue
            cond, update = src[popen + 1:pclose], ""
        else:
            popen = src.find("(", m.end())
            if popen == -1 or src[m.end():popen].strip():
                continue
            pclose = paren_span(src, popen)
            if pclose == -1:
                continue
            header = src[popen + 1:pclose]
            if kw == "for":
                parts = split_for_header(header)
                if len(parts) != 3:
                    continue  # for..of / for..in: bounded by the collection itself
                cond, update = parts[1], parts[2]
            else:
                cond, update = header, ""
            bstart, bend = body_span(src, pclose + 1)

        if not SIZE_IN_COND.search(cond):
            continue
        body = src[bstart:bend]
        draw = body_draws_random(body, helpers)
        if not draw:
            continue
        if has_fixed_bound(cond, update):
            continue  # a counter advances every pass -- bounded, e.g. Fisher-Yates

        hits.append({
            "file": relpath,
            "function": enclosing_function(scopes, m.start()),
            "line": src.count("\n", 0, m.start()) + 1,
            "loop": kw,
            "condition": " ".join(cond.split())[:90],
            "draws": draw,
        })
    return hits


def load_config():
    if not os.path.exists(ALLOWLIST_PATH):
        return {}
    with open(ALLOWLIST_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_allowlist():
    data = load_config()
    return {(e["file"], e["function"]): e.get("reason", "") for e in data.get("allow", [])}


def roster_gaps():
    """Games the roster does not list, split by whether that absence is known.

    The roster is where tier 1 reads each game's levels, so a game missing from it is
    only ever loaded bare. For a deliberately unlisted game that is full coverage; for
    one somebody forgot to add, it is a silent hole in the check. Reporting both keeps
    the difference visible and stops the exceptions list quietly becoming a lie about
    what is actually covered.
    """
    levels = roster_levels()
    known = {e["path"]: e.get("reason", "")
             for e in load_config().get("roster_exceptions", [])}
    expected, unexpected = [], []
    for rel in rel_glob("games", "index.html"):
        slug = rel.split("/")[1]
        if slug in levels:
            continue
        path = "games/" + slug
        (expected if path in known else unexpected).append(path)
    return expected, unexpected, known


def tier2(targets, verbose=True):
    allow = load_allowlist()
    flagged, allowed = [], []
    for relpath in targets:
        path = os.path.join(ROOT, relpath.replace("/", os.sep))
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        js = extract_inline_scripts(raw) if relpath.endswith(".html") else raw
        for hit in scan_source(strip_js_noise(js), relpath):
            key = (hit["file"], hit["function"])
            if key in allow:
                hit["reason"] = allow[key]
                allowed.append(hit)
            else:
                flagged.append(hit)

    if verbose:
        print("\n" + "=" * 78)
        print("TIER 2 - rejection-sampling scan")
        print("=" * 78)
        for h in allowed:
            print("  ALLOWED  %s :: %s  (line %d)" % (h["file"], h["function"], h["line"]))
            print("           reason: %s" % h["reason"])
        if not flagged:
            print("  PASS - no unlisted rejection-sampling loops in %d files." % len(targets))
        for h in flagged:
            print("  FAIL     %s :: %s  (line %d)" % (h["file"], h["function"], h["line"]))
            print("           %s (%s) draws %s, no counter advances per pass"
                  % (h["loop"], h["condition"], h["draws"]))
    return flagged, allowed


# ---------------------------------------------------------------------------
# Page inventory
# ---------------------------------------------------------------------------

def roster_levels():
    """slug -> [level query values]. The table and the parser are bank_common's:
    scripts/roster-levels.json is the one place a roster label becomes a key."""
    if not os.path.exists(bc.ROSTER_PATH):
        return {}
    return bc.roster_levels()[0]


def rel_glob(subdir, name):
    base = os.path.join(ROOT, subdir)
    if not os.path.isdir(base):
        return []
    found = []
    for entry in sorted(os.listdir(base)):
        p = os.path.join(base, entry, name)
        if os.path.isfile(p):
            found.append("%s/%s/%s" % (subdir, entry, name))
    return found


# What GitHub Pages serves, as one rule. This repo is published by Pages' Jekyll build
# (there is no .nojekyll), and Jekyll leaves out of the site any file or folder whose
# name starts with "_", ".", "#" or "~" or ends in "~", anything in its default exclude
# list, and symlinks (Pages builds in safe mode); a folder left out takes everything in
# it. Everything else is published as it stands, so docs/, scripts/ and data/ are served
# too: an .html file there would be a live page. Until Oct 2026 tier 1 loaded only files
# named index.html, which is how games/sequence-solver/index-original.html, a served
# page, went unloaded (todo §4 item 12), while games/regression-rumble/_withdrawn.html is
# rightly never loaded: Jekyll does not publish it.
JEKYLL_SPECIAL_LEAD = ("_", ".", "#", "~")
JEKYLL_DEFAULT_EXCLUDE = ("Gemfile", "Gemfile.lock", "node_modules", "gemfiles",
                          ".sass-cache", ".jekyll-cache", "vendor/bundle", "vendor/cache",
                          "vendor/gems", "vendor/ruby")


def jekyll_serves(rel):
    """True if GitHub Pages publishes the repo path `rel` (file or folder, '/'-separated)."""
    if os.path.exists(os.path.join(ROOT, ".nojekyll")):
        return rel.split("/")[0] != ".git"   # no Jekyll build: every file is served
    parts = rel.split("/")
    for i, name in enumerate(parts):
        if name.startswith(JEKYLL_SPECIAL_LEAD) or name.endswith("~"):
            return False
        if "/".join(parts[:i + 1]) in JEKYLL_DEFAULT_EXCLUDE:
            return False
    return not os.path.islink(os.path.join(ROOT, rel.replace("/", os.sep)))


def discover_pages(skip=()):
    """Every .html file GitHub Pages serves (jekyll_serves), minus the paths in `skip`
    (games and rooms, already listed with their own labels)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        reldir = os.path.relpath(dirpath, ROOT).replace(os.sep, "/")
        reldir = "" if reldir == "." else reldir + "/"
        dirnames[:] = sorted(d for d in dirnames if jekyll_serves(reldir + d))
        for name in filenames:
            rel = reldir + name
            if name.endswith(".html") and rel not in skip and jekyll_serves(rel):
                found.append(rel)
    return sorted(found)


def page_label(rel):
    """'page:' plus the folder of an index.html ('root' at the top), else the path
    without .html, so games/sequence-solver/index-original.html is not mistaken for
    the folder's own page."""
    if rel == "index.html":
        return "page:root"
    if rel.endswith("/index.html"):
        return "page:" + rel[:-len("/index.html")]
    return "page:" + rel[:-len(".html")]


def build_page_list(only=None):
    """[(label, path, [query strings])] covering every page that must run."""
    levels = roster_levels()
    pages = []

    for rel in rel_glob("games", "index.html"):
        slug = rel.split("/")[1]
        queries = [""] + ["?level=%s" % lv for lv in levels.get(slug, [])]
        pages.append(("game:" + slug, rel, queries))

    for rel in rel_glob("escape-rooms", "index.html"):
        pages.append(("room:" + rel.split("/")[1], rel, [""]))
    for rel in rel_glob("escape-rooms", "teacher.html"):
        pages.append(("room-teacher:" + rel.split("/")[1], rel, [""]))

    # Every other page the site serves, discovered rather than listed. Until Oct 2026
    # this was a hard-coded list of 13, so a new page was never loaded unless someone
    # remembered to add it here: the 21 parent guides went unchecked that way. Until
    # 2 Oct 2026 it found index.html files only (see jekyll_serves).
    for rel in discover_pages(skip={p[1] for p in pages}):
        pages.append((page_label(rel), rel, [""]))

    if only:
        pages = [p for p in pages if only in p[0] or only in p[1]]
    return pages


def tier2_targets():
    targets = [rel for _, rel, _ in build_page_list() if rel.endswith(".html")]
    targets += rel_glob("escape-rooms", "room.js")
    return sorted(set(targets))


# ---------------------------------------------------------------------------
# Shards (canon §7.8, 7 Oct 2026)
# ---------------------------------------------------------------------------
#
# CI runs tier 1 as four parallel jobs, `--shard 1/4` .. `--shard 4/4`. Each page (with all its
# ?level= loads, its level controls and its phone-width measurements) goes to exactly one shard:
# page k of build_page_list()'s order to shard (k mod n) + 1. That order is stable (games sorted by
# folder, then rooms, then every other served page, sorted), so dealing round-robin spreads the
# games, which cost the most, evenly. Whatever cannot be split runs once, in shard 1 only: tier 2
# (a static scan of every page), the roster-gap notes, and the tier1_phone_overflow entries that
# name no page at all. Every other verdict belongs to one page, so it fails in that page's shard
# exactly as it failed in the unsharded run. One message moves: a redirect stub whose target is in
# another shard is not re-checked from the stub's shard; the target is measured in its own shard,
# and fails there if it does not load.

def parse_shard(text):
    """'i/n' -> (i, n) with 1 <= i <= n."""
    m = re.match(r"^\s*(\d+)\s*/\s*(\d+)\s*$", text or "")
    if not m or not 1 <= int(m.group(1)) <= int(m.group(2)):
        raise ValueError("--shard wants i/n with 1 <= i <= n, got %r" % text)
    return int(m.group(1)), int(m.group(2))


def shard_pages(pages, shard):
    """The pages one shard loads. shard None (unsharded) keeps them all."""
    if shard is None:
        return list(pages)
    i, n = shard
    return [p for k, p in enumerate(pages) if k % n == i - 1]


def site_wide_here(shard):
    """True where the parts that cannot be split run: unsharded, or shard 1."""
    return shard is None or shard[0] == 1


def shard_union_faults(full, parts):
    """What is wrong with `parts` (one page list per shard) as a split of `full`: [] if nothing."""
    fails, seen = [], {}
    want = {(label, rel): q for label, rel, q in full}
    for i, part in enumerate(parts, 1):
        if not part:
            fails.append("shard %d loads no page" % i)
        for label, rel, queries in part:
            if (label, rel) in seen:
                fails.append("%s is in shard %d and shard %d" % (label, seen[(label, rel)], i))
            seen[(label, rel)] = i
            if want.get((label, rel)) != queries:
                fails.append("%s: shard %d's level loads differ from the unsharded run's" % (label, i))
    dropped = [label for label, rel, _ in full if (label, rel) not in seen]
    if dropped:
        fails.append("%d page(s) in no shard: %s" % (len(dropped), ", ".join(dropped[:8])))
    return fails


def shard_selftest(n, workflow=os.path.join(ROOT, ".github", "workflows", "check-site.yml")):
    """The n shards together load every page exactly once, and the workflow runs all n of them."""
    full = build_page_list()
    parts = [shard_pages(full, (i, n)) for i in range(1, n + 1)]
    fails = shard_union_faults(full, parts)
    print("  shard self-test: %d pages (%d loads) in %d shards: %s"
          % (len(full), sum(len(q) for _, _, q in full), n,
             ", ".join("%d/%d: %d pages, %d loads" % (i, n, len(p), sum(len(q) for _, _, q in p))
                       for i, p in enumerate(parts, 1))))
    # The workflow must run every shard once, and no unsharded copy alongside them.
    if os.path.exists(workflow):
        with open(workflow, encoding="utf-8") as fh:
            runs = re.findall(r"python scripts/check-site\.py\b([^\n|&]*)", fh.read())
        shards = sorted(m.group(1) for m in (re.search(r"--shard (\d+/\d+)", r) for r in runs) if m)
        unsharded = [r.strip() for r in runs if "--shard" not in r]
        want = sorted("%d/%d" % (i, n) for i in range(1, n + 1))
        if shards != want:
            fails.append("the workflow runs shards %s, not %s" % (shards, want))
        if unsharded:
            fails.append("the workflow also runs check-site.py unsharded: %s" % unsharded)
        print("  workflow runs shards: %s" % (", ".join(shards) or "none"))
    # Planted faults, each must be caught: a page dropped, a page in two shards.
    caught_drop = bool(shard_union_faults(full, [parts[0][1:]] + parts[1:]))
    caught_dup = bool(shard_union_faults(full, [parts[0] + parts[-1][:1]] + parts[1:]))
    for name, caught in (("a page dropped from shard 1", caught_drop),
                         ("a page in two shards", caught_dup)):
        print("  planted: %-30s %s" % (name, "caught" if caught else "*** MISSED ***"))
        if not caught:
            fails.append("self-test: %s was not caught" % name)
    for f in fails:
        print("  FAIL  " + f)
    print("  shard self-test: %s" % ("FAILED" if fails else "PASS"))
    return 1 if fails else 0


# ---------------------------------------------------------------------------
# Tier 1 -- load every page in a real browser
# ---------------------------------------------------------------------------

GUARD_NOISE = (
    "stubbed",                 # serve-stubbed.py's window.fetch replacement
    "net::err_failed",
    "net::err_blocked",
    "failed to fetch",
    "err_aborted",
    "load failed",
)


def is_guard_noise(text, blocked_urls):
    """True if this console error is our own network guard, not a page defect."""
    low = text.lower()
    if any(is_write_host(u) and host_of(u) and host_of(u) in low for u in blocked_urls):
        return True
    for suffix in BLOCK_HOST_SUFFIXES:
        if suffix in low:
            return True
    return any(tok in low for tok in GUARD_NOISE)


async def check_one(context, base, label, rel, query, live, timeout_ms):
    blocked, escaped, console_errs, page_errs, missing, ext_fail = [], [], [], [], [], []

    page = await context.new_page()

    def on_response(resp):
        try:
            if resp.status in (404, 403, 500) and resp.request.resource_type != "document":
                if host_of(resp.url) in LOCAL_HOSTS or (live and LIVE_ORIGIN in resp.url):
                    missing.append("%d %s" % (resp.status, resp.url))
                else:
                    ext_fail.append("%d %s" % (resp.status, resp.url))
        except Exception:
            pass

    def on_requestfinished(req):
        if is_write_host(req.url):
            escaped.append(req.url)

    page.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errs.append(str(e)))
    page.on("response", on_response)
    page.on("requestfinished", on_requestfinished)
    page.on("requestfailed", lambda r: ext_fail.append("failed %s" % r.url)
            if not is_write_host(r.url) and host_of(r.url) not in LOCAL_HOSTS else None)

    async def route_handler(route):
        url = route.request.url
        reason = block_reason(url)
        if reason:
            blocked.append(url)
            try:
                await route.abort()
            except Exception:
                pass
        else:
            try:
                await route.continue_()
            except Exception:
                pass

    await page.route("**/*", route_handler)

    sep = "&" if "?" in query else "?"
    cb = "%scb=%d%d" % (sep, int(time.time() * 1000), random.randint(1000, 9999))
    url = base + "/" + rel + query + cb

    status, detail = "PASS", ""
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await page.wait_for_timeout(900)
        # If the main thread is stuck in an infinite loop, this never returns.
        await asyncio.wait_for(page.evaluate("1 + 1"), timeout=timeout_ms / 1000.0)
    except asyncio.TimeoutError:
        status, detail = "FAIL", "main thread unresponsive (probable infinite loop)"
    except Exception as exc:
        msg = str(exc).split("\n")[0]
        if "Timeout" in msg:
            status, detail = "FAIL", "page load timed out: " + msg[:120]
        else:
            status, detail = "FAIL", "navigation error: " + msg[:120]

    real_console = [t for t in console_errs if not is_guard_noise(t, blocked)]
    real_pageerr = [t for t in page_errs if not is_guard_noise(t, blocked)]

    if status == "PASS":
        if real_pageerr:
            status, detail = "FAIL", "uncaught exception: " + real_pageerr[0][:160]
        elif real_console:
            status, detail = "FAIL", "console.error: " + real_console[0][:160]
        elif missing:
            status, detail = "FAIL", "missing local asset: " + missing[0][:160]
        elif ext_fail:
            status, detail = "WARN", "external resource: " + ext_fail[0][:120]

    try:
        await page.close()
    except Exception:
        pass

    return {
        "label": label, "url": rel + query, "status": status, "detail": detail,
        "blocked": blocked, "escaped": escaped,
    }


async def tier1(pages, live, workers, timeout_ms, site_wide=True):
    from playwright.async_api import async_playwright

    base = LIVE_ORIGIN if live else None
    server = None
    if not live:
        # A free port chosen per run; raises bc.StubServerError if the server cannot start.
        server, base = bc.start_stub_server()

    jobs = [(label, rel, q) for label, rel, queries in pages for q in queries]
    results, all_blocked, all_escaped = [], [], []
    done = 0

    print("\n" + "=" * 78)
    print("TIER 1 - page load (%s) - %d page loads across %d targets"
          % ("LIVE " + LIVE_ORIGIN if live else "local stub server", len(jobs), len(pages)))
    print("=" * 78)

    expected, unexpected, known = roster_gaps() if site_wide else ([], [], {})
    for path in expected:
        print("  bare-load only  %s  (declared roster exception)" % path)
        print("                  %s" % known[path])
    for path in unexpected:
        print("  NOTE            %s is not in game-roster.md, so it is only loaded bare."
              % path)
        print("                  Add it to the roster, or record it under roster_exceptions")
        print("                  in scripts/checker-allowlist.json if that is deliberate.")

    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)
            contexts = [await browser.new_context() for _ in range(workers)]
            for ctx in contexts:
                # Firebase RTDB talks over WebSocket, which HTTP routing does not
                # touch. Without this the guard has a hole exactly where the
                # leaderboard writes go -- and the first full run proved it, with
                # a wss:// connection to the live database on every page carrying
                # the ticker.
                #
                # The predicate intercepts ONLY blocked hosts, so any other
                # WebSocket is left alone rather than needing to be proxied back
                # to its server. Reaching this handler means Playwright took the
                # socket over before it was opened: that is a block, not an escape.
                async def ws_handler(ws):
                    all_blocked.append(ws.url)
                    await ws.close()
                await ctx.route_web_socket(
                    lambda url: block_reason(url) is not None, ws_handler)
            pool = asyncio.Queue()
            for ctx in contexts:
                pool.put_nowait(ctx)

            async def run(label, rel, q):
                nonlocal done
                async with sem:
                    ctx = await pool.get()
                    try:
                        res = await check_one(ctx, base, label, rel, q, live, timeout_ms)
                    finally:
                        pool.put_nowait(ctx)
                results.append(res)
                all_blocked.extend(res["blocked"])
                all_escaped.extend(res["escaped"])
                done += 1
                if res["status"] != "PASS":
                    print("  %-5s %-34s %s" % (res["status"], label, res["detail"]))
                if done % 50 == 0:
                    print("  ... %d/%d" % (done, len(jobs)))

            await asyncio.gather(*(run(*j) for j in jobs))

            lc = await level_controls(browser, base, pages, live, workers, timeout_ms)
            results.extend(lc)
            for res in lc:
                all_blocked.extend(res["blocked"])
                all_escaped.extend(res["escaped"])

            pw_res = await phone_width(browser, base, pages, workers, timeout_ms, site_wide)
            results.extend(pw_res)
            for res in pw_res:
                all_blocked.extend(res["blocked"])
                all_escaped.extend(res["escaped"])
            await browser.close()
    finally:
        if server:
            server.terminate()

    return results, all_blocked, all_escaped


# ---------------------------------------------------------------------------
# Tier 1, level controls -- press every level button
# ---------------------------------------------------------------------------
#
# Tier 1 loads every game bare and once per ?level= in the roster, and tier 3
# plays from the same URLs. Neither ever presses a level button, so a button
# whose key the game's banks do not have was invisible to both.
# regression-rumble's Level 4 button set 'l4', beginGame() read SCENARIOS['l4'],
# which does not exist, and threw on Start -- while ?level=l4 and ?level=level4
# were both mapped to 'level4' and passed every run.
#
# So for every game, every level control is pressed in a fresh page, the rest of
# the setup screen is filled in with its first choice, Start is pressed, and the
# game has to say it began: `game_started`, read through TIER3_INIT's mfg
# accessor, as tier 3 does.
#
#   FAIL  an uncaught exception after the press   (the dead-key signature)
#   FAIL  the main thread stops answering
#   FAIL  neither: the game never said it started
#   PASS  game_started fired
#
# "Options on screen" is deliberately NOT a start. The level picker is itself a
# group of options, so the first draft of this check read regression-rumble's
# crash as a pass.
#
# WHAT COUNTS AS A LEVEL CONTROL (outside header/footer/nav)
#   1. any [data-level]
#   2. an onclick calling a function with a level-key literal, as split-it's
#      startGame('ks3') does. 'higher' is NOT in that list: higher-power's
#      in-game guess('higher') would match it. quadratic-factoriser's 'higher'
#      level is reached by rule 3 instead.
#   3. a <button> inside a level container -- the rule that reaches pickers built
#      in JavaScript with no key in the markup (quadratic-factoriser,
#      distinctly-average).
# Controls are indexed in document order, including hidden ones, so a fresh page
# can press the same one.
#
# GETTING PAST THE REST OF THE SETUP SCREEN
#   * A control hidden on load is revealed by choosing the first mode: split-it
#     asks for a mode before it shows its level buttons.
#   * After the level, the first visible element of every other picker attribute
#     is pressed (glorious-gantt wants a data-mode before Start will go).
#   * Then up to three passes of: Start if there is one, else the first entry of
#     the largest clickable group -- prisoners-dilemma shows opponents after the
#     level, proof-builder shows modes. That group is never clicked if it holds a
#     level control, because choosing a DIFFERENT level would start the game and
#     read a dead button as a pass.
# Measured 30 Sep 2026: 125 controls across 47 games, and every one reached a
# started game except regression-rumble's Level 4, before its fix.

LEVEL_INIT = r"""
(() => {
  const KEY_RE = /\(\s*['"](ks3|gcse|alevel|alevel2|further|level3|level4|l3|l4|core|year6|formula|foundation)['"]/i;
  const CONTAINER = '[id*=level i], [class*=level-select i], [class*=level-row i], ' +
                    '[class*=levelselect i], [class*=level-grid i], [id*=lvl i]';
  const OTHER = ['data-type', 'data-mode', 'data-stage', 'data-topic', 'data-count',
                 'data-length', 'data-tier'];
  const REVEAL = '[data-mode], [class*=mode-card i], [class*=mode-btn i]';

  function vis(el) {
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return false;
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
  }

  function controls() {
    const out = [];
    document.querySelectorAll('body *').forEach(function (el) {
      if (el.closest('header, footer, nav')) return;
      const oc = el.getAttribute('onclick') || '';
      if (el.hasAttribute('data-level')) {
        out.push({ el: el, key: el.getAttribute('data-level') });
      } else if (KEY_RE.test(oc)) {
        out.push({ el: el, key: oc.match(KEY_RE)[1] });
      } else if (el.tagName === 'BUTTON' && el.parentElement &&
                 el.parentElement.closest(CONTAINER)) {
        out.push({ el: el, key: '' });
      }
    });
    return out;
  }

  window.__mfgLevelControls = function () {
    return controls().map(function (c, i) {
      return { i: i, key: c.key,
               text: (c.el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 30) };
    });
  };

  window.__mfgLevelPress = function (i) {
    const steps = [];
    const c = controls()[i];
    if (!c) return ['no control ' + i];
    if (!vis(c.el)) {
      const r = Array.prototype.find.call(document.querySelectorAll(REVEAL), vis);
      if (r) { r.click(); steps.push('reveal'); }
      if (!vis(c.el)) { steps.push('unreached'); return steps; }
    }
    c.el.click(); steps.push('level');
    const levelEls = new Set(controls().map(function (x) { return x.el; }));
    OTHER.forEach(function (a) {
      const el = Array.prototype.find.call(document.querySelectorAll('[' + a + ']'),
        function (e) { return vis(e) && !levelEls.has(e); });
      if (el) { el.click(); steps.push(a); }
    });
    if (window.__mfgClickStart()) steps.push('start');
    return steps;
  };

  window.__mfgLevelMenuStep = function () {
    window.__mfgProbe();
    const g = window.__mfgGroup || [];
    if (!g.length) return false;
    const levelEls = new Set(controls().map(function (x) { return x.el; }));
    if (g.some(function (e) { return levelEls.has(e); })) return false;
    g[0].click();
    return true;
  };
})();
"""


async def open_guarded_page(ctx, base, rel, timeout_ms, settle_ms=800, fonts=None):
    """A fresh page in `ctx` behind the network guard, loaded cache-busted and given
    `settle_ms` to settle. Returns (page, rec): rec collects blocked and escaped
    requests and uncaught exceptions. fonts="real" serves KaTeX and Google Fonts from
    their pinned copies in scripts/fonts/ (bank_common.real_font_response; a font URL
    with no pinned copy is aborted), so the page is drawn in the faces students see
    with no network; fonts="fallback" is the old way: the Google Fonts hosts
    (PHONE_FONT_HOSTS) aborted, KaTeX still real (from its pinned copy, the same bytes
    the CDN served). Neither is recorded in rec: font hosts are not write hosts."""
    page = await ctx.new_page()
    rec = {"blocked": [], "escaped": [], "errs": []}
    page.on("pageerror", lambda e: rec["errs"].append(str(e)))
    page.on("requestfinished",
            lambda r: rec["escaped"].append(r.url) if is_write_host(r.url) else None)

    async def route_handler(route):
        if block_reason(route.request.url):
            rec["blocked"].append(route.request.url)
            try:
                await route.abort()
            except Exception:
                pass
        elif fonts and bc.is_font_cdn(route.request.url) and not (
                fonts == "fallback" and suffix_match(host_of(route.request.url), PHONE_FONT_HOSTS)):
            got = bc.real_font_response(route.request.url)
            try:
                await (route.fulfill(**got) if got else route.abort())
            except Exception:
                pass
        elif fonts == "fallback" and suffix_match(host_of(route.request.url), PHONE_FONT_HOSTS):
            try:
                await route.abort()
            except Exception:
                pass
        else:
            try:
                await route.continue_()
            except Exception:
                pass
    await page.route("**/*", route_handler)
    cb = "?cb=%d%d" % (int(time.time() * 1000), random.randint(1000, 9999))
    await page.goto(base + "/" + rel + cb, wait_until="domcontentloaded",
                    timeout=timeout_ms)
    if settle_ms:
        await page.wait_for_timeout(settle_ms)
    return page, rec


async def drive_to_start(page, ev, rec, steps, before):
    """After a level control (or nothing) has been pressed: up to three rounds of
    waiting 2s for game_started, then pressing Start, else the first entry of the
    menu group (LEVEL_INIT's __mfgLevelMenuStep). Stops early on a new uncaught
    exception or an unreached control. True if the game said it started."""
    started = False
    for _ in range(3):
        for _ in range(10):
            await page.wait_for_timeout(200)
            if (await ev("window.__mfgStats()"))["started"]:
                started = True
                break
        if started or len(rec["errs"]) > before or "unreached" in steps:
            break
        if await ev("window.__mfgHasStart()"):
            await ev("window.__mfgClickStart()")
            steps.append("start")
        elif await ev("window.__mfgLevelMenuStep()"):
            steps.append("menu")
        else:
            break
    return started


async def level_controls(browser, base, pages, live, workers, timeout_ms):
    """Press every level control of every game; one result per control."""
    games = [(lbl, rel) for lbl, rel, _ in pages if lbl.startswith("game:")]
    if not games:
        return []

    contexts = []
    for _ in range(workers):
        ctx = await browser.new_context()
        await ctx.add_init_script(TIER3_INIT)
        await ctx.add_init_script(LEVEL_INIT)

        async def ws_handler(ws):
            await ws.close()
        await ctx.route_web_socket(lambda url: block_reason(url) is not None, ws_handler)
        contexts.append(ctx)
    pool = asyncio.Queue()
    for ctx in contexts:
        pool.put_nowait(ctx)

    async def open_page(ctx, rel):
        return await open_guarded_page(ctx, base, rel, timeout_ms)

    async def discover(label, rel):
        ctx = await pool.get()
        try:
            page, _ = await open_page(ctx, rel)
            try:
                return [(label, rel, c)
                        for c in await page.evaluate("window.__mfgLevelControls()")]
            finally:
                await page.close()
        except Exception:
            return []   # a page that will not load is already a tier 1 FAIL
        finally:
            pool.put_nowait(ctx)

    async def press(label, rel, c):
        name = c["key"] or c["text"]
        res = {"label": "level:" + label.split(":", 1)[1],
               "url": "%s [%s]" % (rel, name), "status": "PASS", "detail": ""}
        ctx = await pool.get()
        page, rec = None, {"blocked": [], "escaped": [], "errs": []}
        try:
            page, rec = await open_page(ctx, rel)

            async def ev(expr):
                # Bounded, so a click that loops forever FAILs this control
                # instead of hanging the whole run.
                return await asyncio.wait_for(page.evaluate(expr),
                                              timeout=timeout_ms / 1000.0)

            before = len(rec["errs"])
            steps = await ev("window.__mfgLevelPress(%d)" % c["i"])
            started = await drive_to_start(page, ev, rec, steps, before)
            errs = rec["errs"][before:]
            if errs:
                res["status"] = "FAIL"
                res["detail"] = ascii_safe("level button '%s' throws: %s"
                                           % (name, errs[0][:140]))
            elif not started:
                res["status"] = "FAIL"
                res["detail"] = ascii_safe(
                    "level button '%s' never reached a started game (%s)"
                    % (name, " > ".join(steps)))
        except asyncio.TimeoutError:
            res["status"] = "FAIL"
            res["detail"] = ascii_safe("level button '%s': main thread unresponsive" % name)
        except Exception as exc:
            res["status"] = "FAIL"
            res["detail"] = ascii_safe("level button '%s': %s"
                                       % (name, str(exc).split("\n")[0][:140]))
        finally:
            if page is not None:
                try:
                    await page.close()
                except Exception:
                    pass
            pool.put_nowait(ctx)
        res["blocked"], res["escaped"] = rec["blocked"], rec["escaped"]
        return res

    found = await asyncio.gather(*(discover(l, r) for l, r in games))
    jobs = [j for per_game in found for j in per_game]
    results = await asyncio.gather(*(press(*j) for j in jobs))
    for ctx in contexts:
        await ctx.close()

    n_games = len({lbl for lbl, _, _ in jobs})
    print("\n  level controls: %d pressed across %d games" % (len(jobs), n_games))
    for res in results:
        if res["status"] != "PASS":
            print("  %-5s %-34s %s" % (res["status"], res["label"], res["detail"]))
    return list(results)


# ---------------------------------------------------------------------------
# Tier 1, phone width -- does any page scroll sideways on a 320px phone?
# ---------------------------------------------------------------------------
#
# Nothing checked page width on a phone, so sideways scrolling was found only by
# accident: 15 pages on 2 Oct 2026, while measuring the footer (todo §1.34), and
# measure-phone-fit.py is a report, not a gate. So every page tier 1 loads is
# loaded once more at 320x568, bare URL, and every game is then started through
# its first level control (tier 1's own method, LEVEL_INIT, the same as
# level_controls) or its Start button, and measured again: a game's start screen
# can fit while its first question does not.
#
#   width    document.documentElement.scrollWidth against window.innerWidth, as
#            measure-phone-fit.py reads it. 1px over is a FAIL.
#   fonts    the faces students see (FONT-FIT, 10 Oct 2026): KaTeX 0.16.9 and every
#            Google Fonts stylesheet and file the pages ask for are served from their
#            pinned copies in scripts/fonts/ (bank_common.real_font_response), never
#            the network, so the verdict is the same every run and is taken in Outfit,
#            not the runner's fallback (DejaVu, pinned in CI). Until 10 Oct Google
#            Fonts were blocked here, because loading Outfit live made the verdict
#            depend on a third-party fetch (Jon, 2 Oct 2026: 12 of the 44 overflows
#            found in fallback fitted in Outfit). --phone-fonts fallback still runs
#            the old measure, for comparison.
#   settle   no fixed pause: the page is measured once its load event has fired,
#            KaTeX has arrived where the page asks for it, document.fonts.ready
#            has resolved and two animation frames have passed (PHONE_SETTLE); the
#            same after a game starts.
#   known    scripts/checker-allowlist.json "tier1_phone_overflow", one entry per
#            path and "at" ("load" or "start"), with the width measured when it
#            was recorded and the to-do item that owns its fix. A known overflow
#            passes; a known entry that no longer overflows FAILs as stale, so the
#            fixing PR removes it -- the same two ways check-banks.py's ledger fails.
#   start    a game that will not start at 320x568 is tried again at desktop
#            size. Starting there and not on a phone FAILs as "phone start
#            unreachable" (itself a phone defect) unless recorded with reason
#            "unreachable"; starting at neither size is not a phone fact, and is
#            noted, not failed.
#   seed     Math.random is replaced, before any page script runs, by a seeded
#            generator (PHONE_SEED: mulberry32, seeded with the FNV-1a hash of
#            the page's own location.pathname, e.g. /games/moments-master/). So
#            every run draws the same first question, the same option order and
#            the same everything else, and the verdict cannot flip between runs
#            of one commit (todo §4 item 16: moments-master's start passed one CI
#            run and failed the next, §1.40). Only this pass is seeded; the other
#            tier 1 passes keep the real Math.random. A seed shows one draw, not
#            a game's worst question: a game whose width depends on the draw is
#            swept on its own (moments-master: §1.40).
#
# The outermost elements past the right edge are named in a FAIL, skipping any
# inside a fixed-position or overflow-clipped ancestor: those cannot scroll the
# page (the footer's links overrun a 320px phone inside a fixed bar).

PHONE_SIZE = (320, 568)
PHONE_FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")
# "real" (FONT-FIT, 10 Oct 2026): the phone pass draws every page in KaTeX and the Google faces it asks for, served
# from scripts/fonts/. "fallback" is the old measure (Google Fonts blocked), kept for comparison: --phone-fonts.
PHONE_FONTS = "real"

# Resolves when the page has settled enough to measure; bounded at 8s inside the
# page so a font that never arrives cannot hold the run.
PHONE_SETTLE = r"""
async () => {
  const settle = (async () => {
    if (document.readyState !== 'complete') {
      await new Promise(function (r) { window.addEventListener('load', r, { once: true }); });
    }
    const wantsKatex = Array.prototype.some.call(document.scripts,
      function (s) { return /katex/i.test(s.src || ''); });
    while (wantsKatex && typeof window.katex === 'undefined') {
      await new Promise(function (r) { setTimeout(r, 25); });
    }
    await document.fonts.ready;
    await new Promise(function (r) {
      requestAnimationFrame(function () { requestAnimationFrame(r); });
    });
    return true;
  })();
  return Promise.race([settle, new Promise(function (r) { setTimeout(function () { r(false); }, 8000); })]);
}
"""

# Added to the phone pass's contexts before any other init script, so it runs before
# every page script, in every frame. See "seed" above.
PHONE_SEED = r"""
(() => {
  let h = 0x811c9dc5;
  const p = location.pathname;
  for (let i = 0; i < p.length; i++) {
    h ^= p.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  let s = h;
  Math.random = function () {
    s = (s + 0x6D2B79F5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
})();
"""

PHONE_INIT = r"""
(() => {
  window.__mfgWidth = function () {
    const vw = window.innerWidth;
    const sw = document.documentElement.scrollWidth;
    const out = [];
    if (sw > vw) {
      const over = function (el) { return el.getBoundingClientRect().right > vw + 0.5; };
      const contained = function (el) {
        for (let a = el; a && a !== document.documentElement; a = a.parentElement) {
          const cs = getComputedStyle(a);
          if (cs.position === 'fixed') return true;
          if (a !== el && cs.overflowX !== 'visible' && !over(a)) return true;
        }
        return false;
      };
      document.querySelectorAll('body *').forEach(function (el) {
        if (out.length >= 3 || !over(el) || !el.getBoundingClientRect().width) return;
        const p = el.parentElement;
        if (p && p !== document.body && over(p)) return;      // outermost only
        if (contained(el)) return;
        const cls = String(el.className && el.className.baseVal !== undefined
                           ? el.className.baseVal : el.className || '').trim().split(/\s+/)[0];
        out.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
                 (cls ? '.' + cls : '') + ' to ' + Math.round(el.getBoundingClientRect().right) + 'px');
      });
    }
    return { sw: sw, vw: vw, culprits: out };
  };
})();
"""


async def phone_settle(page, timeout_ms):
    """Wait for PHONE_SETTLE, following a redirect stub to its target first: a meta
    refresh fires only after load, and location.replace() destroys the context
    PHONE_SETTLE is running in, so both are waited out rather than raced."""
    for _ in range(4):
        try:
            if await page.locator('meta[http-equiv="refresh" i]').count():
                was = urlsplit(page.url).path
                await page.wait_for_url(lambda u: urlsplit(u).path != was, timeout=timeout_ms)
                await page.wait_for_load_state("domcontentloaded")
                continue
            await asyncio.wait_for(page.evaluate(PHONE_SETTLE), timeout=timeout_ms / 1000.0)
            return
        except asyncio.TimeoutError:
            raise
        except Exception as exc:
            if "destroyed" not in str(exc) and "navigat" not in str(exc).lower():
                raise
            await page.wait_for_load_state("domcontentloaded")


def landed_rel(url):
    """The repo path a served URL comes from: /spec-map/ -> spec-map/index.html."""
    path = urlsplit(url).path.lstrip("/")
    return path + "index.html" if path == "" or path.endswith("/") else path


def phone_known():
    """(path, at) -> its tier1_phone_overflow entry."""
    return {(e["path"], e.get("at", "load")): e
            for e in load_config().get("tier1_phone_overflow", [])}


async def phone_width(browser, base, pages, workers, timeout_ms, site_wide=True):
    """One result per page at load and one per game start, at PHONE_SIZE."""
    t_start = time.time()
    known = phone_known()
    w, h = PHONE_SIZE
    size = "%dx%d" % PHONE_SIZE

    async def new_ctx(viewport):
        ctx = await browser.new_context(viewport=viewport) if viewport \
            else await browser.new_context()
        await ctx.add_init_script(PHONE_SEED)
        await ctx.add_init_script(TIER3_INIT)
        await ctx.add_init_script(LEVEL_INIT)
        await ctx.add_init_script(PHONE_INIT)

        async def ws_handler(ws):
            await ws.close()
        await ctx.route_web_socket(lambda url: block_reason(url) is not None, ws_handler)
        return ctx

    contexts = [await new_ctx({"width": w, "height": h}) for _ in range(workers)]
    desktop = await new_ctx(None)
    pool = asyncio.Queue()
    for ctx in contexts:
        pool.put_nowait(ctx)

    judged, loaded, known_hits, notes, redirects = set(), set(), [], [], []

    def judge(label, rel, at, m):
        key = (rel, at)
        judged.add(key)
        entry = known.get(key)
        res = {"label": ("phone:" + label) if at == "load"
               else "phone-start:" + label.split(":", 1)[1],
               "url": "%s [%s%s]" % (rel, size, ", after start" if at == "start" else ""),
               "status": "PASS", "detail": "", "blocked": [], "escaped": [],
               "width": m["sw"]}
        excess = m["sw"] - m["vw"]
        if entry and entry.get("reason") == "unreachable":
            res["status"] = "FAIL"
            res["detail"] = ("stale: recorded as phone start unreachable, but it started "
                             "at %s; remove its tier1_phone_overflow entry" % size)
        elif excess >= 1 and entry:
            known_hits.append((rel, at, m["sw"], entry))
        elif excess >= 1:
            res["status"] = "FAIL"
            res["detail"] = ascii_safe(
                "scrolls sideways at %s%s: %dpx wide (+%d); %s"
                % (size, " after start" if at == "start" else "", m["sw"], excess,
                   "; ".join(m["culprits"]) or "no single element found"))
        elif entry:
            res["status"] = "FAIL"
            res["detail"] = ("stale: recorded at %spx in tier1_phone_overflow (%s), now fits "
                             "at %s; remove the entry" % (entry.get("width"),
                                                          entry.get("todo", ""), size))
        return res

    async def start(page, rec):
        async def ev(expr):
            return await asyncio.wait_for(page.evaluate(expr), timeout=timeout_ms / 1000.0)
        before = len(rec["errs"])
        if (await ev("window.__mfgStats()"))["started"]:
            return True, ["at load"]
        if await ev("window.__mfgLevelControls().length"):
            steps = await ev("window.__mfgLevelPress(0)")
        else:
            steps = ["start"] if await ev("window.__mfgClickStart()") else []
        return await drive_to_start(page, ev, rec, steps, before), steps

    async def starts_on_desktop(rel):
        page = None
        try:
            page, rec = await open_guarded_page(desktop, base, rel, timeout_ms)
            return (await start(page, rec))[0]
        except Exception:
            return False
        finally:
            if page is not None:
                try:
                    await page.close()
                except Exception:
                    pass

    async def one(label, rel):
        """Load, settle and measure one page; start and measure it again if a game."""
        out = []
        ctx = await pool.get()
        page, rec = None, {"blocked": [], "escaped": [], "errs": []}
        try:
            page, rec = await open_guarded_page(ctx, base, rel, timeout_ms,
                                                settle_ms=0, fonts=PHONE_FONTS)

            async def ev(expr):
                return await asyncio.wait_for(page.evaluate(expr), timeout=timeout_ms / 1000.0)
            await phone_settle(page, timeout_ms)
            # A redirect stub (the /schools/ pages, index-original.html) has no layout
            # of its own: what loads is its target, which must be measured as its own
            # page -- asserted after the run.
            landed = landed_rel(page.url)
            if landed != rel:
                redirects.append((rel, landed))
            else:
                out.append(judge(label, rel, "load", await ev("window.__mfgWidth()")))
                loaded.add(rel)
            if label.startswith("game:") and rel in loaded:
                started, steps = await start(page, rec)
                if started:
                    await phone_settle(page, timeout_ms)
                    out.append(judge(label, rel, "start", await ev("window.__mfgWidth()")))
                else:
                    out.append((label, rel, steps))     # settled below, off the pool
        except asyncio.TimeoutError:
            out.append({"label": "phone:" + label, "url": rel, "status": "FAIL",
                        "detail": "main thread unresponsive at %s" % size,
                        "blocked": [], "escaped": []})
        except Exception as exc:
            out.append({"label": "phone:" + label, "url": rel, "status": "FAIL",
                        "detail": ascii_safe("did not load at %s: %s"
                                             % (size, str(exc).split("\n")[0][:140])),
                        "blocked": [], "escaped": []})
        finally:
            if page is not None:
                try:
                    await page.close()
                except Exception:
                    pass
            pool.put_nowait(ctx)

        for i, r in enumerate(out):
            if isinstance(r, tuple):
                lbl, rl, steps = r
                slug = lbl.split(":", 1)[1]
                key = (rl, "start")
                entry = known.get(key)
                res = {"label": "phone-start:" + slug, "url": "%s [%s, after start]" % (rl, size),
                       "status": "PASS", "detail": "", "blocked": [], "escaped": []}
                if await starts_on_desktop(rl):
                    judged.add(key)
                    if entry and entry.get("reason") == "unreachable":
                        known_hits.append((rl, "start", None, entry))
                    else:
                        res["status"] = "FAIL"
                        res["detail"] = ascii_safe("phone start unreachable: %s (%s)"
                                                   % (slug, " > ".join(steps) or "no control"))
                else:
                    notes.append("%s: starts at neither %s nor desktop size by this method; "
                                 "start not measured" % (slug, size))
                out[i] = res
        if not out:
            out.append({"label": "phone:" + label, "url": rel, "status": "PASS",
                        "detail": "redirect stub", "blocked": [], "escaped": []})
        out[0]["blocked"], out[0]["escaped"] = rec["blocked"], rec["escaped"]
        return out

    found = await asyncio.gather(*(one(label, rel) for label, rel, _ in pages))
    results = [r for per_page in found for r in per_page]
    for ctx in contexts + [desktop]:
        await ctx.close()

    # Recorded entries this run should have measured and did not: the page is gone,
    # it is not a game (so has no start), or its start was not reached at any size.
    in_run = {rel for _, rel, _ in pages}
    for (rel, at), entry in sorted(known.items()):
        if (rel, at) in judged:
            continue
        gone = not os.path.isfile(os.path.join(ROOT, rel.replace("/", os.sep)))
        # An entry naming no page belongs to no shard: reported once, where site-wide parts run.
        if (gone and site_wide) or (rel in in_run and rel in loaded):
            results.append({"label": "phone-known:" + rel, "url": "%s [%s]" % (rel, at),
                            "status": "FAIL", "blocked": [], "escaped": [],
                            "detail": "stale: tier1_phone_overflow entry (%s) %s; remove it"
                                      % (at, "names no page" if gone else "was not measured")})

    # Every redirect stub's target must itself be measured, or the stub hides a page
    # from this check. A target outside an --only run is only noted.
    every = {rel for _, rel, _ in build_page_list()}
    for rel, landed in sorted(redirects):
        problem = ("lands on /%s, which is not a page tier 1 loads" % landed
                   if landed not in every
                   else "lands on /%s, which was not measured" % landed
                   if landed in in_run and landed not in loaded else "")
        if problem:
            results.append({"label": "phone-redirect:" + rel, "url": rel, "status": "FAIL",
                            "detail": "redirect stub " + problem,
                            "blocked": [], "escaped": []})

    n_start = sum(1 for r in results if r["label"].startswith("phone-start:"))
    n_measured = sum(1 for _, landed in redirects if landed in loaded)
    print("\n  phone width (%s, %s): %d pages, %d game starts, %.0fs; "
          "%d redirect stubs, %d with their target measured; %d known overflow(s)"
          % (size, "real fonts, pinned" if PHONE_FONTS == "real" else "web fonts blocked", len(pages), n_start,
             time.time() - t_start, len(redirects), n_measured, len(known_hits)))
    for res in results:
        if res["status"] != "PASS":
            print("  %-5s %-34s %s" % (res["status"], res["label"], res["detail"]))
    for rel, at, sw, entry in sorted(known_hits, key=lambda k: (k[0], k[1])):
        print("  known %-44s %-5s %s  (recorded %s; %s)"
              % (rel, at, "unreachable" if sw is None else "%dpx" % sw,
                 entry.get("reason") if entry.get("reason") == "unreachable"
                 else "%spx" % entry.get("width"), entry.get("todo", "")))
    for n in notes:
        print("  note  " + n)
    for rel, landed in sorted(redirects):
        print("  note  %s redirects to /%s; not measured itself%s"
              % (rel, landed, "" if landed in loaded else " (target outside this run)"
                 if landed not in in_run else ""))
    return results


# ---------------------------------------------------------------------------
# Tier 3 -- play every game
# ---------------------------------------------------------------------------
#
# Tier 1 proves a page loads. It says nothing about what happens on the second
# question, which is exactly where modular-battle froze: its parse error was
# fixed, and behind it sat a rejection-sampling loop that hung the tab on ~25%
# of questions. A page-load check can never see that, because question 1 was
# usually fine.
#
# So tier 3 plays. For each game it finds the answer options, clicks one,
# waits for the question to change, and repeats. It asserts the things that are
# true of every multiple-choice question regardless of topic:
#
#   * options are actually rendered            (a dead bank renders none)
#   * there are at least two of them           (nothing to choose is not a question)
#   * no two options are the same              (Trig Worms shipped -5.1 twice)
#   * the click is accepted and the game moves (a stuck question is unplayable)
#   * the main thread still answers            (the hang class)
#   * nothing new appears in the console       (a mid-play throw)
#
# What it deliberately does NOT do is check whether the maths is right. Clicking
# an option and seeing the game move on proves the machinery runs, not that the
# marked answer is true. That is tier 4, it needs a per-game answer key, and it
# is the tier that would have caught es_gcse_005.
#
# UNSUPPORTED IS NOT A FAILURE
# ----------------------------
# Tier 3 drives multiple-choice games. A drag game, a keypad, a canvas or a
# free-text entry has no option group to click, and reporting those as broken
# would be a lie that costs the checker its credibility -- and a checker nobody
# trusts is worse than no checker. Those games come back UNSUPPORTED, are
# listed by name at the end of the run, and never fail it. Recording one in
# scripts/checker-allowlist.json under "tier3_exceptions" is how you say the
# classification has been read and is correct.
#
# HOW AN OPTION IS RECOGNISED
# ---------------------------
# Not by class name or id -- the 94 games do not agree on either. 27 use
# id="options", 8 use a class containing "option", and 60 use neither. It is
# done by behaviour instead: an element is a candidate if it is visible and has
# a click handler, found either as an `onclick` property (which is how
# index-laws, modular-battle, trig-worms and suvat bind) or through
# addEventListener (angle-ace, matrix-crunch), which the init script wraps
# before any page script runs. Candidates are then grouped by their parent
# element, and the largest same-tag group of two or more is the option group.
#
# Grouping is by parent alone, never by parent+class: prime-or-composite's two
# buttons are `ans-prime` and `ans-composite` and a class-aware key splits the
# pair into two groups of one, which then reads as "only one option".
#
# HOW AN OPTION IS IDENTIFIED (for the duplicate check)
# ----------------------------------------------------
# In the site's own order of preference, which is canon: `dataset.val` first,
# because that is where tile identity belongs and suvat moved its matching there
# when KaTeX started rewriting textContent underneath it; then the KaTeX
# `<annotation encoding="application/x-tex">`, which is the source TeX; and only
# then the rendered text, with the duplicated `.katex-mathml` subtree stripped
# so a KaTeX option does not read as its own content twice over.
#
# TIMERS ARE NOT THROTTLED HERE
# -----------------------------
# docs/game-integrity-2026-09-21.md warns that an automation tab reports
# document.hidden, so timers throttle to ~1.5/sec and a poll-based driver
# stalls, and recommends draining the game's own setTimeout callbacks by hand.
# That is true of the Chrome-extension automation tab. It is NOT true of
# headless Playwright: measured here, document.hidden is false and three
# chained 200ms timeouts complete in ~620ms, which is full speed. So this
# driver waits on the game's real timers rather than reaching into them, which
# keeps it honest about the delays a student actually sits through.

TIER3_INIT = r"""
(() => {
  // Record every element that takes a click listener, before any page script runs.
  // The onclick-property bindings do not come through here; they are read directly
  // off the element at probe time.
  window.__mfgClicky = new WeakSet();
  const origAdd = EventTarget.prototype.addEventListener;
  EventTarget.prototype.addEventListener = function (type, fn, opts) {
    if (type === 'click' && this && this.nodeType === 1) {
      try { window.__mfgClicky.add(this); } catch (e) { /* cross-realm node */ }
    }
    return origAdd.call(this, type, fn, opts);
  };

  // Every game already narrates itself. 94 of the 95 game folders call
  // mfg('question_answered', {question_index: n}), 94 call mfg('game_completed'),
  // and .claude/rules/analytics.md is the contract for both. That is a far better
  // progress signal than watching the DOM for a change, because "the options are
  // different now" is simply false for a binary game: prime-or-composite renders
  // the same two buttons, PRIME and COMPOSITE, for every question it ever asks,
  // so an option-diff driver reads a game working perfectly as a game stuck on
  // question 1.
  //
  // mfg is captured through an accessor rather than by wrapping a function,
  // because analytics.js (and serve-stubbed.py's no-op version of it) ASSIGNS
  // window.mfg long after this init script has run. The setter keeps whatever
  // the page assigns and still delegates to it, so the page's own behaviour is
  // unchanged and nothing here suppresses a real call -- the network guard, not
  // this, is what stops an event reaching the sheet.
  window.__mfgEvents = [];
  let _mfgReal = null;
  try {
    Object.defineProperty(window, 'mfg', {
      configurable: true,
      get: function () {
        return function () {
          try {
            window.__mfgEvents.push({
              e: arguments[0],
              i: (arguments[1] && arguments[1].question_index)
            });
          } catch (err) { /* never let bookkeeping break the game */ }
          if (typeof _mfgReal === 'function') {
            try { return _mfgReal.apply(this, arguments); } catch (err) {}
          }
        };
      },
      set: function (v) { _mfgReal = v; }
    });
  } catch (err) { /* a page that defines mfg non-configurably keeps its own */ }

  window.__mfgStats = function () {
    let started = 0, answered = 0, completed = 0;
    (window.__mfgEvents || []).forEach(function (r) {
      if (r.e === 'game_started') started++;
      else if (r.e === 'question_answered') answered++;
      else if (r.e === 'game_completed') completed++;
    });
    return { started: started, answered: answered, completed: completed };
  };

  const CHROME_ID = ['a11yToggle'];
  const CHROME_TEXT = [
    'back to games', 'all games', 'leaderboard', 'leaderboards', 'about', 'privacy',
    'feedback', 'contact', 'buy me a coffee', 'home', 'skip', 'aa', 'share',
    'submit score', 'submit', 'close', 'how to play', 'instructions', 'help'
  ];
  // Controls that mean the run is over rather than that a question is waiting.
  const END_TEXT = ['play again', 'play again?', 'restart', 'try again', 'again',
                    'new game', 'start again', 'back to start'];

  function visible(el) {
    const r = el.getBoundingClientRect();
    if (r.width < 4 || r.height < 4) return false;
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0';
  }

  function textOf(el) {
    return (el.textContent || '').trim().replace(/\s+/g, ' ');
  }

  function isChrome(el) {
    if (CHROME_ID.indexOf(el.id) !== -1) return true;
    if (el.closest('header, footer, nav')) return true;
    const t = textOf(el).toLowerCase();
    if (CHROME_TEXT.indexOf(t) !== -1) return true;
    // A link that leaves the page is chrome, never an answer.
    if (el.tagName === 'A') {
      const h = el.getAttribute('href') || '';
      if (h && h !== '#' && !h.startsWith('#')) return true;
    }
    return false;
  }

  // Option identity, in the site's own order of preference. See canon:
  // never mark by re-parsing a displayed value.
  window.__mfgOptKey = function (el) {
    if (el.dataset && el.dataset.val !== undefined && el.dataset.val !== '') {
      return 'v:' + el.dataset.val;
    }
    const ann = el.querySelector('annotation[encoding="application/x-tex"]');
    if (ann) return 'x:' + (ann.textContent || '').trim();
    const c = el.cloneNode(true);
    c.querySelectorAll('.katex-mathml').forEach(function (n) { n.remove(); });
    return 't:' + (c.textContent || '').trim().replace(/\s+/g, ' ');
  };

  function candidates() {
    const out = [];
    document.querySelectorAll('*').forEach(function (el) {
      const clicky = (typeof el.onclick === 'function') || window.__mfgClicky.has(el);
      if (!clicky) return;
      if (!visible(el)) return;
      if (isChrome(el)) return;
      if (el.disabled) return;
      out.push(el);
    });
    return out;
  }

  // The option group is the largest set of same-tag candidates sharing a parent.
  // Parent alone -- adding the class name splits prime-or-composite's
  // ans-prime / ans-composite pair into two groups of one.
  window.__mfgProbe = function () {
    const cands = candidates();
    const byParent = new Map();
    cands.forEach(function (el) {
      const p = el.parentElement;
      if (!p) return;
      const key = p;
      if (!byParent.has(key)) byParent.set(key, []);
      byParent.get(key).push(el);
    });

    let best = null;
    byParent.forEach(function (els) {
      const tag = els[0].tagName;
      const same = els.filter(function (e) { return e.tagName === tag; });
      if (same.length < 2) return;
      if (!best || same.length > best.length) best = same;
    });

    window.__mfgGroup = best || [];

    const endBtn = cands.filter(function (e) {
      return END_TEXT.indexOf(textOf(e).toLowerCase()) !== -1;
    });

    return {
      n: window.__mfgGroup.length,
      keys: window.__mfgGroup.map(window.__mfgOptKey),
      texts: window.__mfgGroup.map(function (e) { return textOf(e).slice(0, 40); }),
      parent: best && best[0].parentElement
        ? (best[0].parentElement.id || String(best[0].parentElement.className).slice(0, 40) || best[0].parentElement.tagName)
        : '',
      hasNext: !!document.querySelector('.maffs-next'),
      atEnd: endBtn.length > 0 && (!best || best.length === 0),
      candidates: cands.length
    };
  };

  // seven-bridges builds its options as SVG nodes, and an SVGElement has no
  // .click() in Chromium -- the driver died with "g[i].click is not a function"
  // on four runs before this fallback existed. A dispatched MouseEvent reaches
  // the same listeners.
  function fire(el) {
    if (typeof el.click === 'function') { el.click(); return; }
    el.dispatchEvent(new MouseEvent('click', {
      bubbles: true, cancelable: true, view: window
    }));
  }

  window.__mfgClickOpt = function (i) {
    const g = window.__mfgGroup || [];
    if (!g[i]) return false;
    fire(g[i]);
    return true;
  };

  // The control that submits an answer the student has BUILT rather than
  // picked. prime-factorisation puts 2, 3, 5, 7, 11, 13 on screen and expects
  // several presses and then a submit; expectation-station fills a table from a
  // tile bank and then presses "Check Table". One click into either of those is
  // not a wrong answer, it is an unfinished one, and nothing is marked.
  const SUBMIT_RE = /^(check|submit|answer|enter|go|calculate|confirm|done|finish)\b/;

  window.__mfgClickSubmit = function () {
    const grp = window.__mfgGroup || [];
    let hit = null;
    candidates().forEach(function (c) {
      if (hit || grp.indexOf(c) !== -1) return;
      const t = textOf(c).toLowerCase();
      if (END_TEXT.indexOf(t) !== -1) return;
      if (SUBMIT_RE.test(t)) hit = c;
    });
    if (!hit) return '';
    const label = textOf(hit).slice(0, 24);
    fire(hit);
    return label;
  };

  // Not every question is a row of buttons. suvat is two-phase -- pick the
  // equation from a choice group, then TYPE the value -- so a driver that only
  // clicks gets one phase in and then reports a game Jon plays regularly as
  // dead. Its question_answered does not fire until the typed phase is marked.
  function typeableInputs() {
    const out = [];
    document.querySelectorAll('input, [contenteditable="true"]').forEach(function (el) {
      if (el.disabled || el.readOnly || !visible(el)) return;
      const t = (el.getAttribute('type') || 'text').toLowerCase();
      if (el.tagName === 'INPUT' && ['text', 'number', 'tel', ''].indexOf(t) === -1) return;
      out.push(el);
    });
    return out;
  }

  window.__mfgHasInput = function () { return typeableInputs().length > 0; };

  // What else is on the page that a click-and-type driver cannot work. Used to
  // tell "this game is broken" apart from "this game is not the shape tier 3
  // drives" -- the second must never be reported as a failure.
  window.__mfgModalities = function () {
    const vis = function (sel) {
      return [...document.querySelectorAll(sel)].filter(visible).length;
    };
    return {
      canvas: vis('canvas'),
      range: vis('input[type="range"]'),
      draggable: vis('[draggable="true"]'),
      svg: vis('svg'),
      inputs: typeableInputs().length
    };
  };

  window.__mfgTypeAnswer = function (value) {
    const els = typeableInputs();
    if (!els.length) return '';
    const el = els[0];
    if (el.tagName === 'INPUT') {
      el.focus();
      el.value = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    } else {
      el.focus();
      el.textContent = String(value);
      el.dispatchEvent(new Event('input', { bubbles: true }));
    }
    // Submit the way the game expects: its own button if it has one, otherwise
    // Enter, which several of these games bind instead.
    const submitted = window.__mfgClickSubmit();
    if (submitted) return 'button:' + submitted;
    ['keydown', 'keypress', 'keyup'].forEach(function (type) {
      el.dispatchEvent(new KeyboardEvent(type, {
        key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
      }));
    });
    const form = el.closest('form');
    if (form) { try { form.requestSubmit ? form.requestSubmit() : form.submit(); } catch (e) {} }
    return 'enter';
  };

  // The control that carries on after an answer has been marked.
  //
  // canon 7.6's `.maffs-next` is the one to press where it exists, but only a
  // handful of games are on it. The rest hand-rolled the same idea years
  // earlier and their button says whatever the author felt like: angle-ace
  // renders `<button class="next-btn" onclick="closeSol()">Got it -- next
  // question</button>` and does not auto-advance from a wrong answer at all,
  // so a driver that waits for the question to change on its own sits there
  // until it times out and calls a perfectly good game broken.
  //
  // Members of the current option group are excluded, so an answer that happens
  // to read "next" is never mistaken for the continue control, and END_TEXT is
  // excluded so "play again" does not restart a finished run.
  const CONTINUE_RE = /^(got it|next|continue|carry on|onward|ok|okay)\b/;

  window.__mfgClickContinue = function () {
    const mn = document.querySelector('.maffs-next');
    if (mn) { mn.click(); return 'maffs-next'; }
    const grp = window.__mfgGroup || [];
    let hit = null;
    candidates().forEach(function (el) {
      if (hit || grp.indexOf(el) !== -1) return;
      const t = textOf(el).toLowerCase();
      if (END_TEXT.indexOf(t) !== -1) return;
      if (CONTINUE_RE.test(t) || t.indexOf('next question') !== -1) hit = el;
    });
    if (!hit) return '';
    const label = textOf(hit).slice(0, 30);
    hit.click();
    return label;
  };

  // A start control, for games that open on a title screen rather than a question.
  //
  // A visible start control has to be pressed BEFORE anything is read as an
  // option group, not only when no group was found. angle-ace opens on a title
  // screen holding both a #levelSelect pair (Year 6 / GCSE, whose handlers only
  // set a variable) and a separate "Start" button. Take the largest clickable
  // group on that screen and you answer the level picker, wait the full advance
  // window for a question that was never coming, and report a working game as
  // broken -- which is exactly what the first run of this tier did.
  //
  // END_TEXT is excluded deliberately: "Play again" matches /^play\b/, so
  // without that guard the driver would restart a finished game instead of
  // stopping, and every short game would report the full question count.
  // Matched on id and class as well as text, because the text is often the
  // game's own joke: spot-the-muppet's start button reads "Spot the Muppets"
  // and no word list will ever catch that, while its id is plainly `startBtn`
  // and its class `start-btn`. The markup says what the button IS; the label
  // says what the author thought was funny.
  function startEls() {
    const words = ['start', 'start game', 'play', 'begin', "let's go", 'go'];
    const els = [];
    document.querySelectorAll('button, a, [role="button"]').forEach(function (el) {
      if (!visible(el)) return;
      // A link to another page is never this game's start: the Core Maths papers' "Play Fermi Lab" signpost
      // reads "Play ..." and took the driver away from the game (F1 batch 7, 8 Oct 2026).
      if (el.tagName === 'A' && el.getAttribute('href') && !/^(#|javascript:)/i.test(el.getAttribute('href')) &&
          new URL(el.href, location.href).pathname !== location.pathname) return;
      const t = (el.textContent || '').trim().toLowerCase().replace(/\s+/g, ' ');
      if (END_TEXT.indexOf(t) !== -1) return;
      const marker = (el.id + ' ' + String(el.className || '')).toLowerCase();
      if (/\bstart|start-?btn|btn-?start/.test(marker)) { els.push(el); return; }
      if (words.indexOf(t) !== -1 || /^start\b/.test(t) || /^play\b/.test(t)) els.push(el);
    });
    return els;
  }

  window.__mfgHasStart = function () { return startEls().length > 0; };

  window.__mfgClickStart = function () {
    const els = startEls();
    if (!els.length) return false;
    els[0].click();
    return true;
  };
})();
"""


def ascii_safe(text):
    """Printable on a Windows console, which is cp1252 and raises on an arrow.

    Tier 3 is the first tier that prints text taken off the page, and maths
    options are full of characters cp1252 has no room for: angle-ace's level
    names carry U+2192, degree signs and superscripts are everywhere, and the
    first debug run of this driver died on `print` rather than on anything to do
    with the site. A checker that crashes while reporting a real failure is
    worse than one that never found it.
    """
    return str(text).encode("ascii", "replace").decode("ascii")


def tier3_exceptions():
    """slug -> reason, from scripts/checker-allowlist.json."""
    data = load_config()
    out = {}
    for e in data.get("tier3_exceptions", []):
        out[e.get("slug", "")] = e.get("reason", "")
    return out


async def play_one(context, base, label, rel, query, live, timeout_ms, n_questions,
                   advance_ms):
    """Drive one game through n_questions and report what happened."""
    slug = label.split(":", 1)[-1]
    blocked, escaped, console_errs, page_errs = [], [], [], []

    page = await context.new_page()
    page.on("console", lambda m: console_errs.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errs.append(str(e)))
    page.on("requestfinished",
            lambda r: escaped.append(r.url) if is_write_host(r.url) else None)

    async def route_handler(route):
        url = route.request.url
        if block_reason(url):
            blocked.append(url)
            try:
                await route.abort()
            except Exception:
                pass
        else:
            try:
                await route.continue_()
            except Exception:
                pass

    await page.route("**/*", route_handler)

    # TIER3_INIT is added once per context, in tier3() -- not here. Contexts are
    # pooled and reused across jobs, and add_init_script appends, so adding it
    # per page stacks another copy on every run through the pool.

    sep = "&" if "?" in query else "?"
    cb = "%scb=%d%d" % (sep, int(time.time() * 1000), random.randint(1000, 9999))
    url = base + "/" + rel + query + cb

    res = {"label": label, "url": rel + query, "status": "PASS", "detail": "",
           "played": 0, "warns": [], "blocked": blocked, "escaped": escaped}

    async def alive():
        """False if the main thread has stopped answering."""
        try:
            await asyncio.wait_for(page.evaluate("1 + 1"), timeout=timeout_ms / 1000.0)
            return True
        except Exception:
            return False

    def fail(detail):
        res["status"], res["detail"] = "FAIL", detail

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        await page.wait_for_timeout(800)
        if not await alive():
            fail("main thread unresponsive on load (probable infinite loop)")
            raise _Done()

        # Getting to question 1. A game may open straight on a question, on a
        # title screen with a Start button, or on a screen that wants a choice
        # made first -- angle-ace has a Year 6 / GCSE level pair AND a separate
        # Start, and chart-interrogator opens on a grid of chart types. Rather
        # than special-case each, press the most student-like thing available
        # and let the game say when it has begun: `game_started` is the signal,
        # not a guess about the markup.
        for _ in range(4):
            if (await page.evaluate("window.__mfgStats()"))["started"]:
                break
            if await page.evaluate("window.__mfgHasStart()"):
                await page.evaluate("window.__mfgClickStart()")
            elif (await page.evaluate("window.__mfgProbe()"))["n"] >= 2:
                # A setup screen's group is a menu, not a question. Take the
                # first entry and look for the Start control again next pass.
                await page.evaluate("window.__mfgClickOpt(0)")
            else:
                break
            await page.wait_for_timeout(700)

        # Last resort for a game with no visible control we recognise.
        if not (await page.evaluate("window.__mfgStats()"))["started"]:
            try:
                await page.evaluate(
                    "typeof window.startGame === 'function' && window.startGame()")
                await page.wait_for_timeout(700)
            except Exception:
                pass

        probe = await page.evaluate("window.__mfgProbe()")
        if probe["n"] < 2:
            try:
                await page.evaluate(
                    "typeof window.startGame === 'function' && window.startGame()")
                await page.wait_for_timeout(700)
                probe = await page.evaluate("window.__mfgProbe()")
            except Exception:
                pass

        async def undrivable(where):
            """Say why this game is not tier 3's shape, rather than calling it broken.

            The difference between UNSUPPORTED and FAIL is the whole credibility
            of this tier. A drag game, a canvas, a slider or a free-text box is
            not a defect, and the first full run of this driver reported 118 of
            them as failures -- which is precisely the kind of noise that gets a
            checker ignored, and then the one real failure in it goes with them.
            """
            m = await page.evaluate("window.__mfgModalities()")
            bits = [k for k in ("canvas", "range", "draggable", "inputs") if m.get(k)]
            res["status"] = "UNSUPPORTED"
            res["detail"] = ("%s; page has %s"
                             % (where, ", ".join(bits) if bits else "no input it knows"))
            raise _Done()

        if probe["n"] < 2 and not await page.evaluate("window.__mfgHasInput()"):
            await undrivable("no option group found after starting (%d clickable "
                             "candidates)" % probe["candidates"])

        seen_console = 0
        for q in range(n_questions):
            stats = await page.evaluate("window.__mfgStats()")
            marked_before = stats["answered"]
            before = list(probe["keys"])

            # Answer by whatever this question offers. A game can change shape
            # between phases -- suvat picks an equation from a group and then
            # wants the value typed -- so the choice is made per question, not
            # once per game.
            if probe["n"] >= 2:
                keys = probe["keys"]
                dupes = [k for k in set(keys)
                         if keys.count(k) > 1 and k not in ("t:", "v:", "x:")]
                if dupes and not res["warns"]:
                    # A WARN, not a FAIL, and the reason is expectation-station.
                    # Its stage 1 is a TILE BANK feeding several blanks, not four
                    # options with one right answer, so a repeat is authored on
                    # purpose: es_gcse_001 ships ['0.25','0.25','0.50','0.10']
                    # because two cells of its table are both 0.25, and
                    # es_gcse_003 ships '1/3' twice for the same reason.
                    # A repeat in a pick-one group IS a real defect -- Trig Worms
                    # shipped -5.1 twice -- but nothing here can reliably tell
                    # the two apart, so it is reported for a person to judge
                    # rather than used to fail a build.
                    shown = ", ".join(sorted(probe["texts"]))
                    res["warns"].append(ascii_safe(
                        "question %d showed the same option twice (%s) -- options: "
                        "%s. Real defect in a pick-one group; expected in a tile "
                        "bank." % (q + 1, dupes[0][:40], shown[:110])))
                if not await page.evaluate("(i) => window.__mfgClickOpt(i)", 0):
                    fail("question %d: the option could not be clicked" % (q + 1))
                    break
            elif await page.evaluate("window.__mfgHasInput()"):
                await page.evaluate("(v) => window.__mfgTypeAnswer(v)", "1")
            else:
                await undrivable("question %d offered neither options nor a "
                                 "typed answer (after %d played)"
                                 % (q + 1, res["played"]))

            # Two separate things have to happen, and they fail in different
            # ways, so they are waited for and reported separately.
            #
            # Stage 1 -- was the answer MARKED? The game says so itself, by
            # firing question_answered. If that never comes, the click reached
            # nothing: this is the es_gcse_005 shape, where a student picks the
            # right tile and the game refuses it.
            #
            # Stage 2 -- did the NEXT question render? A correct answer keeps
            # whatever brisk delay the game already had and advances on its own.
            # A wrong one waits for the student: canon 7.6 games show the `Next`
            # control, and the older hand-rolled ones do the same with a button
            # of their own. Press it, rather than sitting out a 20s fallback
            # that is a safety net and not the mechanism.
            async def settle(stage, test):
                waited, step = 0, 250
                while waited < advance_ms:
                    await page.wait_for_timeout(step)
                    waited += step
                    if not await alive():
                        fail("question %d froze the main thread after a click "
                             "(probable infinite loop)" % (q + 1))
                        raise _Done()
                    if await test():
                        return True
                    if stage == 2:
                        await page.evaluate("window.__mfgClickContinue()")
                return False

            async def was_marked():
                s = await page.evaluate("window.__mfgStats()")
                if s["completed"]:
                    return True
                if s["answered"] > marked_before:
                    return True
                # The one game that narrates nothing still has a DOM to watch.
                p = await page.evaluate("window.__mfgProbe()")
                return p["atEnd"] or (p["n"] >= 2 and p["keys"] != before)

            if not await settle(1, was_marked):
                # Picking from the group may only have been half the question.
                # suvat's phase 1 chooses the equation and phase 2 wants the
                # value typed, and it does not fire question_answered until the
                # typed phase is marked -- so try that before concluding
                # anything, and only then decide between "not our shape" and
                # "genuinely unresponsive".
                got = False

                # An answer may be BUILT rather than picked -- several presses
                # and then a submit. One click into prime-factorisation's
                # 2/3/5/7/11/13 row is an unfinished answer, not a wrong one,
                # and nothing is marked until "Check" is pressed.
                if await page.evaluate("window.__mfgClickSubmit()"):
                    got = await settle(1, was_marked)
                if not got:
                    for extra in (1, 2):
                        await page.evaluate("(i) => window.__mfgClickOpt(i)", extra)
                    if await page.evaluate("window.__mfgClickSubmit()"):
                        got = await settle(1, was_marked)
                if not got and await page.evaluate("window.__mfgHasInput()"):
                    await page.evaluate("(v) => window.__mfgTypeAnswer(v)", "1")
                    got = await settle(1, was_marked)

                if not got:
                    # An unanswerable question is a COVERAGE limit, not a
                    # verdict -- even when earlier questions in the same run
                    # went through.
                    #
                    # The tempting rule is "it took two answers and then stopped,
                    # so it is broken". It is wrong, and better-value and
                    # spot-the-muppet are why: both answer question 1, advance
                    # cleanly, and then present a second phase of the same
                    # question that this driver has no way to complete. Calling
                    # either of them broken would be a false accusation against a
                    # working game, which is the one thing this tier must not do.
                    #
                    # So the run is recorded for what it was: N questions driven,
                    # then a shape we could not drive. The UNSUPPORTED list is
                    # the coverage ledger, it is meant to be read and recorded in
                    # checker-allowlist.json, and once a game is recorded there a
                    # game NEWLY arriving on the list is itself the signal -- the
                    # run prints which entries are unrecorded.
                    await undrivable(
                        "drove %d question(s), then question %d was never marked "
                        "by a click, a submit or a typed answer"
                        % (res["played"], q + 1))

            ended = False

            async def next_ready():
                nonlocal probe, ended
                s = await page.evaluate("window.__mfgStats()")
                probe = await page.evaluate("window.__mfgProbe()")
                if s["completed"] or probe["atEnd"]:
                    ended = True
                    return True
                return probe["n"] >= 2 and probe["keys"] != before

            if not await settle(2, next_ready):
                # A binary game reuses the same two buttons for every question,
                # so identical keys here are not evidence of a stall -- the
                # answer was marked, and that is the question turning over.
                probe = await page.evaluate("window.__mfgProbe()")
                if probe["n"] < 2 and not await page.evaluate("window.__mfgHasInput()"):
                    # Also coverage, not a verdict: the answer WAS marked, so
                    # the game is working; what came next is a screen this
                    # driver has no move for.
                    await undrivable(
                        "question %d was marked, then nothing this driver can "
                        "answer appeared within %dms" % (q + 1, advance_ms))

            real = [t for t in console_errs if not is_guard_noise(t, blocked)]
            real += [t for t in page_errs if not is_guard_noise(t, blocked)]
            if len(real) > seen_console:
                fail(ascii_safe("question %d threw: %s" % (q + 1, real[seen_console][:150])))
                break
            seen_console = len(real)

            res["played"] = q + 1
            if ended:
                res["detail"] = "game ended after %d question(s)" % res["played"]
                break

    except _Done:
        pass
    except Exception as exc:
        msg = str(exc).split("\n")[0]
        if res["status"] == "PASS":
            # A crashed renderer is the game's verdict, not the driver's.
            # Restoring 1a407fe's `while (choices.size < 4)` to modular-battle
            # does not hang politely enough for the watchdog to notice: the loop
            # allocates until Chromium kills the tab, and Playwright surfaces
            # that as "Target crashed". Reporting it as a driver error would put
            # the blame on the checker for the one bug this tier exists to find.
            low = msg.lower()
            if "target crashed" in low or "target closed" in low:
                fail("the page crashed the browser tab while being played "
                     "(runaway loop or allocation) -- %d question(s) in"
                     % res["played"])
            else:
                fail(ascii_safe("driver error: " + msg[:150]))

    if res["status"] == "PASS" and res["warns"]:
        res["status"] = "WARN"
        res["detail"] = res["warns"][0]
    if res["status"] == "PASS" and not res["detail"]:
        res["detail"] = "played %d question(s)" % res["played"]

    try:
        await page.close()
    except Exception:
        pass
    return res


class _Done(Exception):
    """Internal: stop driving this game, keep the status already set."""


async def tier3(pages, live, workers, timeout_ms, n_questions, advance_ms):
    from playwright.async_api import async_playwright

    exceptions = tier3_exceptions()
    games = [(lbl, rel, qs) for lbl, rel, qs in pages if lbl.startswith("game:")]
    jobs = [(lbl, rel, q) for lbl, rel, qs in games for q in qs]

    base = LIVE_ORIGIN if live else None
    server = None
    if not live:
        # A free port chosen per run; raises bc.StubServerError if the server cannot start.
        server, base = bc.start_stub_server()

    print("\n" + "=" * 78)
    print("TIER 3 - play-through (%s) - %d run(s) across %d games, %d question(s) each"
          % ("LIVE " + LIVE_ORIGIN if live else "local stub server",
             len(jobs), len(games), n_questions))
    print("=" * 78)

    results, all_blocked, all_escaped = [], [], []
    done = 0
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)
            contexts = [await browser.new_context() for _ in range(workers)]
            for ctx in contexts:
                # Once per context, before any page exists. Playwright replays a
                # context's init scripts on every navigation, so this covers
                # every job the context later serves.
                await ctx.add_init_script(TIER3_INIT)

                async def ws_handler(ws):
                    all_blocked.append(ws.url)
                    await ws.close()
                await ctx.route_web_socket(
                    lambda url: block_reason(url) is not None, ws_handler)
            pool = asyncio.Queue()
            for ctx in contexts:
                pool.put_nowait(ctx)

            async def run(label, rel, q):
                nonlocal done
                async with sem:
                    ctx = await pool.get()
                    try:
                        r = await play_one(ctx, base, label, rel, q, live,
                                           timeout_ms, n_questions, advance_ms)
                    finally:
                        pool.put_nowait(ctx)
                slug = label.split(":", 1)[-1]
                if r["status"] == "UNSUPPORTED" and slug in exceptions:
                    r["detail"] = "declared: " + exceptions[slug]
                results.append(r)
                all_blocked.extend(r["blocked"])
                all_escaped.extend(r["escaped"])
                done += 1
                if r["status"] in ("FAIL", "WARN"):
                    print("  %-5s %-34s %s"
                          % (r["status"], label, ascii_safe(r["detail"])))
                if done % 40 == 0:
                    print("  ... %d/%d" % (done, len(jobs)))

            await asyncio.gather(*(run(*j) for j in jobs))
            await browser.close()
    finally:
        if server:
            server.terminate()

    unsupported = sorted({r["label"].split(":", 1)[-1]: r for r in results
                          if r["status"] == "UNSUPPORTED"}.items())
    if unsupported:
        undeclared = [s for s, _ in unsupported if s not in exceptions]
        print("\n  UNSUPPORTED - no option group, so not driven (never a failure):")
        for slug, r in unsupported:
            mark = "   " if slug in exceptions else " * "
            print("  %s%-30s %s" % (mark, slug, ascii_safe(r["detail"])[:90]))
        if undeclared:
            print("\n  %d of those are not recorded in scripts/checker-allowlist.json"
                  % len(undeclared))
            print("  under \"tier3_exceptions\". Read each one, then either make it")
            print("  drivable or record why it cannot be. Marked * above.")

    return results, all_blocked, all_escaped


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Check that every page on the site runs.")
    ap.add_argument("--tier", choices=["1", "2", "3", "all"], default="all",
                    help="'all' is tiers 1+2, which is what CI runs. Tier 3 plays the "
                         "games and is opt-in: it is slower, and it is new.")
    ap.add_argument("--live", action="store_true",
                    help="run tier 1 against %s instead of a local server" % LIVE_ORIGIN)
    ap.add_argument("--only", help="substring filter on page label or path")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=20000, help="per-page ms")
    ap.add_argument("--questions", type=int, default=10,
                    help="tier 3: questions to play per run (default 10). "
                         "modular-battle froze on ~25%% of questions, which 10 "
                         "plays catches better than 94%% of the time.")
    ap.add_argument("--phone-widths", metavar="FILE",
                    help="tier 1: also write every phone-width measurement (label, url, "
                         "width) to FILE as JSON, to compare runs (todo §4 item 16)")
    ap.add_argument("--advance-ms", type=int, default=6000,
                    help="tier 3: how long to wait for a question to change after "
                         "answering (default 6000)")
    ap.add_argument("--phone-fonts", choices=("real", "fallback"), default="real",
                    help="tier 1 phone pass: real (default) draws pages in KaTeX and the Google faces "
                         "they ask for, from scripts/fonts/; fallback blocks Google Fonts, the old "
                         "measure in the runner's fallback font (for comparison only)")
    ap.add_argument("--shard", metavar="I/N",
                    help="tiers 1+2: load only shard I of N (each page in exactly one shard; tier 2 "
                         "and the other site-wide parts in shard 1 only). CI runs 1/4 .. 4/4")
    ap.add_argument("--shard-selftest", type=int, metavar="N",
                    help="prove that N shards load every page exactly once and that the workflow "
                         "runs all N; loads nothing")
    args = ap.parse_args()
    global PHONE_FONTS
    PHONE_FONTS = args.phone_fonts
    if args.shard_selftest:
        return shard_selftest(args.shard_selftest)
    try:
        shard = parse_shard(args.shard) if args.shard else None
    except ValueError as exc:
        ap.error(str(exc))
    site_wide = site_wide_here(shard)

    t0 = time.time()
    fails = 0
    t1_results, blocked, escaped = [], [], []

    if args.tier in ("1", "all"):
        pages = shard_pages(build_page_list(args.only), shard)
        if shard:
            print("shard %d/%d: %d pages, %d loads%s" % (shard[0], shard[1], len(pages),
                  sum(len(q) for _, _, q in pages), "; the site-wide parts run here" if site_wide else ""))
        t1_results, blocked, escaped = asyncio.run(
            tier1(pages, args.live, args.workers, args.timeout, site_wide))
        if args.phone_widths:
            with open(args.phone_widths, "w", encoding="utf-8") as fh:
                json.dump(sorted(({"label": r["label"], "url": r["url"], "width": r["width"]}
                                  for r in t1_results if "width" in r),
                                 key=lambda r: (r["url"], r["label"])), fh, indent=1)
        f = [r for r in t1_results if r["status"] == "FAIL"]
        w = [r for r in t1_results if r["status"] == "WARN"]
        fails += len(f)
        print("\n  tier 1: %d PASS, %d FAIL, %d WARN (of %d loads)"
              % (len(t1_results) - len(f) - len(w), len(f), len(w), len(t1_results)))

    if args.tier in ("2", "all") and not args.live and site_wide:
        flagged, _ = tier2(tier2_targets())
        fails += len(flagged)

    if args.tier == "3":
        pages = build_page_list(args.only)
        t3_results, t3_blocked, t3_escaped = asyncio.run(
            tier3(pages, args.live, args.workers, args.timeout,
                  args.questions, args.advance_ms))
        blocked += t3_blocked
        escaped += t3_escaped
        f = [r for r in t3_results if r["status"] == "FAIL"]
        u = [r for r in t3_results if r["status"] == "UNSUPPORTED"]
        w = [r for r in t3_results if r["status"] == "WARN"]
        played = sum(r["played"] for r in t3_results)
        fails += len(f)
        print("\n  tier 3: %d PASS, %d FAIL, %d WARN, %d UNSUPPORTED (of %d runs); "
              "%d questions played"
              % (len(t3_results) - len(f) - len(u) - len(w), len(f), len(w), len(u),
                 len(t3_results), played))

    print("\n" + "=" * 78)
    print("NETWORK GUARD")
    print("=" * 78)
    hosts = {}
    for u in blocked:
        hosts[host_of(u)] = hosts.get(host_of(u), 0) + 1
    if hosts:
        for h, c in sorted(hosts.items(), key=lambda kv: -kv[1]):
            print("  blocked %5d  %s" % (c, h))
    else:
        print("  blocked     0  (no page attempted a write)")
    if escaped:
        print("  ESCAPED %d write request(s) -- the guard leaked:" % len(escaped))
        for u in sorted(set(escaped))[:20]:
            print("    %s" % u)
        fails += len(escaped)
    else:
        print("  escaped     0  - no write request reached the network.")

    print("\n%s  (%.1fs)" % ("FAILED - %d problem(s)" % fails if fails else "OK", time.time() - t0))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
