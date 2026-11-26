#!/usr/bin/env python3
# ci-shards: Large-screen layer (schools/assets/large-screen.js: every MIGRATED page carries the layer's tag once, written from data/large-screen.json; each page's zoom at 1920x955, 2560x1310, 1366x650 and 390x844 equal to this script's own reading of rules a-f; a session played on each page at each size with the answer controls and Next above the fold, no sideways scroll and every media query answering as on the unzoomed page; planted faults caught) | | 4
# ci-deps: schools/assets/ data/large-screen.json scripts/apply-large-screen.py scripts/measure-large-screen.py scripts/measure-phone-fit.py scripts/check-site.py scripts/check-answer-lock.py scripts/plant_common.py games/maffscards/ games/factor-race/ games/surd-simplifier/ games/negative-number-line/ games/bearing-blitz/ games/core-maths-paper1/ games/its-just-base-60-bruv/
"""The large-screen layer: who loads it, what each page's zoom must be, and that a zoomed page still works
(SR-34's goal; contract LARGE-SCREEN-LAYER, 26 Nov 2026).

    python -X utf8 scripts/check-large-screen.py                 # everything: static, every page in the browser, the plants
    python -X utf8 scripts/check-large-screen.py --static        # the lists, the tags and data/large-screen.json only
    python -X utf8 scripts/check-large-screen.py --only base-60  # browser units whose name holds this text (no plants)
    python -X utf8 scripts/check-large-screen.py --selftest      # the planted faults only
    python -X utf8 scripts/check-large-screen.py --shots DIR     # also save a screenshot of each screen (1920x955, 1366x650)
    python -X utf8 scripts/check-large-screen.py --engines chromium,firefox,webkit   # the default in CI

schools/assets/large-screen.js scales a page up with CSS zoom on a large window, choosing the zoom for that page and
that window (its header has the rule, a to f). A page gets it from one tag before </head>, written by
scripts/apply-large-screen.py from the lists below and from data/large-screen.json, which
scripts/measure-large-screen.py writes (never a hand):

    <script src="/schools/assets/large-screen.js" data-need="742" data-pointer="none"></script>

STATIC (unit "static"). Fails when:
  1. a MIGRATED page does not carry the tag exactly once, inside <head>, after every stylesheet the head names (the
     layer reads the page's breakpoints as the tag runs); or any page not on MIGRATED carries it;
  2. a MIGRATED page has no entry in data/large-screen.json, or the entry is not current: its thresholds are not the
     ones this script reads from the page and its stylesheets today, its need is not a positive whole number, or the
     tag's data-need is not the entry's need;
  3. the tag's data-pointer is not what this script works out: "none" for a page whose scripts never read clientX,
     clientY, pageX or pageY; "verified" for one that does and is on POINTER_VERIFIED; "held" for one that does and
     is not. A POINTER_VERIFIED page that reads no pointer, or is not MIGRATED, fails too;
  4. a page carries <html data-large-screen="off"> without an OPT_OUT entry and reason, or an OPT_OUT entry's page
     does not carry it, is not MIGRATED or does not exist;
  5. a size condition in a page's media queries is one this script cannot read (the layer would refuse to zoom).

IN THE BROWSER (one unit per page and engine). At 1920x955 and 2560x1310 (real 1080p and 1440p browser windows) and
at 1366x650 and 390x844 (both must stay unzoomed), a whole session is played with the game's own lock-hint (canon
7.6.0; ROUTES below for a page with none), wrong answers on purpose, to the results screen:
  - the page's zoom, on every screen, is the one THIS script works out from rules a-f: its own parse of the page's
    media queries (never the layer's), the need from data/large-screen.json and the pointer scan;
  - no screen scrolls sideways that does not scroll sideways without the layer at the same size;
  - where the page is zoomed: the answer controls on every question, and Next after every answer, end above the
    fold; every media query in the page's readable sheets answers as it does on an unzoomed window of the effective
    size (the page loaded with the layer blocked at window / zoom, rounded down and rounded up: one of the two);
    100vh still ends at the bottom of the screen; the layer's own account of the engine is "vh zoomed" or
    "vh not zoomed";
  - a POINTER_VERIFIED page passes its measured pointer test under zoom (POINTER_TESTS).
The start and results screens are reported, not judged against the fold (start screens are report-only, canon 7.6.1).
An engine whose zoom the layer refuses (state().by starts "engine") leaves the page unzoomed and working: that is
reported loudly on every run, never failed, because rule 1 is then not broken, only unused.

PLANTS (unit "plants"; each must FAIL; plant_common, so a plant that did not apply fails the run):
  rule c removed from the layer (a page zooms across one of its own height breakpoints);
  rule d removed (a page's zoom ignores its height need);
  rule e removed (a page that reads clientX zooms without being on POINTER_VERIFIED);
  a MIGRATED page without the tag;
  and the static faults: the tag twice, an unlisted page with the tag, an unlisted opt-out, a tag whose need is not
  the data's, a tag marked "verified" for a page not on the list, a stale entry (a breakpoint added to the page).
"""
import argparse
import asyncio
import importlib.util
import json
import math
import os
import pathlib
import re
import shutil
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import plant_common as pc  # noqa: E402

LAYER = "schools/assets/large-screen.js"
LAYER_URL = "/" + LAYER
DATA = "data/large-screen.json"

# Pages that load the layer: the pilot's seven (contract LARGE-SCREEN-LAYER). The rest join in the rollout (todo
# LARGE-SCREEN-ROLLOUT), through this list and apply-large-screen.py, never by hand.
MIGRATED = [
    "games/maffscards/index.html",
    "games/factor-race/index.html",
    "games/surd-simplifier/index.html",
    "games/negative-number-line/index.html",
    "games/bearing-blitz/index.html",
    "games/core-maths-paper1/index.html",
    "games/its-just-base-60-bruv/index.html",
]

# Pages that carry <html data-large-screen="off">, each with its reason.
OPT_OUT = {}

# Pages that read the pointer's position and may be zoomed all the same: each has a measured test under zoom in
# POINTER_TESTS, run by this check. A page that reads the pointer and is not here is held at zoom 1 (rule e).
POINTER_VERIFIED = {}

MIN_W, EFF_W, MAX_Z, MIN_Z, STEPS, EPS = 1500, 1200, 1.6, 1.1, 20, 1e-9
ZOOM_SIZES = [(1920, 955), (2560, 1310)]
FLAT_SIZES = [(1366, 650), (390, 844)]
SHOT_SIZES = [(1920, 955), (1366, 650)]
ENGINES = ["chromium", "firefox", "webkit"]
MAX_QUESTIONS = 60
CHECK_SEED = 7            # never one of measure-large-screen.py's seeds: the check plays a session the data did not see

# ---------------------------------------------------------------------------------------------------- reading a page
TAG_RE = re.compile(r'<script\b[^>]*\bsrc=["\']%s["\'][^>]*>\s*</script>' % re.escape(LAYER_URL), re.I)
ATTR_RE = lambda name: re.compile(r'\b%s=["\']([^"\']*)["\']' % re.escape(name))   # noqa: E731
OFF = re.compile(r"<html\b[^>]*\bdata-large-screen\s*=\s*[\"']off[\"']", re.I)
STYLE_RE = re.compile(r"<style\b([^>]*)>(.*?)</style>", re.S | re.I)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
MEDIA_AT = re.compile(r"@media\b([^{;]*)\{")
IMPORT_AT = re.compile(r"@import\s+(?:url\()?\s*[\"']?([^\"')\s;]+)[\"']?\s*\)?([^;]*);")
COMMENT = re.compile(r"/\*.*?\*/", re.S)
POINTER = re.compile(r"\b(?:client|page)[XY]\b")
UNIT = {"px": 1, "em": 16, "rem": 16}
CLASSIC = re.compile(r"(min|max)-(?:device-)?(width|height)\s*:\s*([\d.]+)(px|r?em)?(?![\w.%])")
RANGE_A = re.compile(r"\b(?:device-)?(width|height)\s*(<=|>=|<|>)\s*([\d.]+)(px|r?em)\b")
RANGE_B = re.compile(r"([\d.]+)(px|r?em)\s*(<=|>=|<|>)\s*(?:device-)?(width|height)\b")
FEATURE = re.compile(r"(?:^|[^a-z-])((?:min-|max-)?(?:device-)?(?:width|height))\b")
KIND = {">=": "ge", "<=": "le", ">": "gt", "<": "lt"}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}
SKIP_DIRS = {".git", "node_modules", "_site", "vendor"}


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def parse_media(text):
    """([(dim, kind, T)], problem or None) for one media query list. kind: ge (min-, >=), le (max-, <=), gt, lt."""
    t = text.lower()
    out, bad = [], None
    for m in CLASSIC.finditer(t):
        if not m.group(4) and float(m.group(3)) != 0:
            bad = "a length with no unit"
        out.append((m.group(2), "ge" if m.group(1) == "min" else "le", float(m.group(3)) * UNIT.get(m.group(4), 0)))
    for m in RANGE_A.finditer(t):
        out.append((m.group(1), KIND[m.group(2)], float(m.group(3)) * UNIT[m.group(4)]))
    for m in RANGE_B.finditer(t):
        out.append((m.group(4), KIND[FLIP[m.group(3)]], float(m.group(1)) * UNIT[m.group(2)]))
    if len(out) < len(FEATURE.findall(t)):
        bad = "a size condition this script cannot read"
    return out, bad


def local_path(root, rel, href):
    """The file a page's same-origin href names, or None for another origin."""
    href = href.split("#")[0].split("?")[0]
    if re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//", href, re.I) or re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):
        return None
    if href.startswith("/"):
        return root / href.lstrip("/")
    return (root / rel).parent / href


def css_media(css, root, rel, seen, problems):
    """Every media query list in a stylesheet's text, following local @imports."""
    css = COMMENT.sub("", css)
    out = [m.group(1).strip() for m in MEDIA_AT.finditer(css)]
    for m in IMPORT_AT.finditer(css):
        if m.group(2).strip():
            out.append(m.group(2).strip())
        p = local_path(root, rel, m.group(1))
        if p is not None and p not in seen:
            seen.add(p)
            if p.is_file():
                out.extend(css_media(read(p), root, p.relative_to(root).as_posix(), seen, problems))
            else:
                problems.append("an @import of %s, which does not exist" % m.group(1))
    return out


def page_facts(root, rel):
    """What the layer's rule needs to know about a page, read from its source and its same-origin stylesheets and
    scripts: {"thresholds": sorted [[dim, kind, T]], "pointer": bool, "problems": [...], "media": [texts]}."""
    src = read(root / rel)
    media, problems, seen = [], [], set()
    for attrs, body in STYLE_RE.findall(src):
        m = ATTR_RE("media").search(attrs)
        if m:
            media.append(m.group(1))
        media.extend(css_media(body, root, rel, seen, problems))
    for tag in LINK_RE.findall(src):
        rel_attr = ATTR_RE("rel").search(tag)
        href = ATTR_RE("href").search(tag)
        if not rel_attr or "stylesheet" not in rel_attr.group(1).lower() or not href:
            continue
        p = local_path(root, rel, href.group(1))
        if p is None:
            continue                                   # another origin: the layer cannot read it and skips it too
        m = ATTR_RE("media").search(tag)
        if m:
            media.append(m.group(1))
        if p not in seen:
            seen.add(p)
            if p.is_file():
                media.extend(css_media(read(p), root, p.relative_to(root).as_posix(), seen, problems))
            else:
                problems.append("a stylesheet %s that does not exist" % href.group(1))
    th = set()
    for text in media:
        got, bad = parse_media(text)
        if bad:
            problems.append('%s in "@media %s"' % (bad, text))
        th.update(x for x in got if x[2] > 0)
    pointer = False
    for attrs, body in SCRIPT_RE.findall(src):
        s = ATTR_RE("src").search(attrs)
        if s:
            p = local_path(root, rel, s.group(1))
            body = read(p) if p is not None and p.is_file() else ""
        if POINTER.search(body):
            pointer = True
    return {"thresholds": sorted([d, k, t] for d, k, t in th), "pointer": pointer, "problems": problems, "media": media}


def pointer_status(rel, facts):
    return "none" if not facts["pointer"] else ("verified" if rel in POINTER_VERIFIED else "held")


def steps(limit, strict):
    return math.ceil(limit * STEPS - EPS) - 1 if strict else math.floor(limit * STEPS + EPS)


def expected_zoom(W, H, facts, need, pointer, opted_out=False):
    """(zoom, the rule that limited it): this script's own reading of the layer's rules a-f."""
    if opted_out:
        return 1.0, "opt-out"
    if W < MIN_W:
        return 1.0, "a: window under %d px wide" % MIN_W
    if not need or need <= 0:
        return 1.0, "d: no measured height need"
    if pointer not in ("none", "verified"):
        return 1.0, "e: pointer use not verified"
    if facts["problems"]:
        return 1.0, "c: " + facts["problems"][0]
    best = (steps(MAX_Z, False), "f: upper limit %s" % MAX_Z)
    caps = [(steps(W / EFF_W, False), "b: effective width %d" % EFF_W),
            (steps(H / need, False), "d: height need %d" % need)]
    for dim, kind, t in facts["thresholds"]:
        v = W if dim == "width" else H
        name = {"ge": "min-%s:%gpx", "le": "max-%s:%gpx", "gt": "%s > %gpx", "lt": "%s < %gpx"}[kind] % (dim, t)
        if kind in ("ge", "lt") and v >= t:
            caps.append((steps(v / t, False), "c: breakpoint " + name))
        if kind in ("le", "gt") and v > t:
            caps.append((steps(v / t, True), "c: breakpoint " + name))
    for k, by in caps:
        if k < best[0]:
            best = (k, by)
    z = best[0] / STEPS
    if z < MIN_Z - EPS:
        return 1.0, best[1] + " (under %s: no zoom)" % MIN_Z
    return z, best[1]


def tag_for(need, pointer):
    return '<script src="%s" data-need="%d" data-pointer="%s"></script>' % (LAYER_URL, need, pointer)


def load_data(root):
    p = root / DATA
    if not p.is_file():
        return {}
    return json.loads(read(p)).get("pages", {})


def html_pages(root):
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        yield rel.as_posix(), p


# ---------------------------------------------------------------------------------------------------- the static check
def check_static(root, migrated=None):
    """Every failure as a line of text; empty when the tree passes."""
    migrated = MIGRATED if migrated is None else migrated
    fails = []
    if not (root / LAYER).is_file():
        return ["%s does not exist" % LAYER]
    data = load_data(root)
    pages = dict(html_pages(root))
    for rel in migrated:
        p = pages.get(rel)
        if p is None:
            fails.append("%s: on MIGRATED but does not exist" % rel)
            continue
        src = read(p)
        tags = TAG_RE.findall(src)
        if len(tags) != 1:
            fails.append("%s: carries the %s tag %d times (expected once)" % (rel, LAYER_URL, len(tags)))
            continue
        at, head_end = TAG_RE.search(src).start(), src.lower().find("</head>")
        if head_end < 0 or at > head_end:
            fails.append("%s: the %s tag is not inside <head>" % (rel, LAYER_URL))
        elif re.search(r"<style\b|<link\b[^>]*stylesheet", src[at:head_end], re.I):
            fails.append("%s: a stylesheet follows the %s tag inside <head> (the layer reads the page's breakpoints as "
                         "the tag runs)" % (rel, LAYER_URL))
        facts = page_facts(root, rel)
        for prob in facts["problems"]:
            fails.append("%s: %s (the layer would refuse to zoom)" % (rel, prob))
        entry = data.get(rel)
        need_attr, ptr_attr = ATTR_RE("data-need").search(tags[0]), ATTR_RE("data-pointer").search(tags[0])
        if entry is None:
            fails.append("%s: no entry in %s (run scripts/measure-large-screen.py)" % (rel, DATA))
        else:
            need = entry.get("need")
            if type(need) is not int or need <= 0:
                fails.append("%s: its need in %s is %r, not a positive whole number" % (rel, DATA, need))
            if entry.get("thresholds") != facts["thresholds"]:
                fails.append("%s: its entry in %s is not current: the page's breakpoints are now %s, measured with %s "
                             "(run scripts/measure-large-screen.py)" % (rel, DATA, facts["thresholds"], entry.get("thresholds")))
            if not need_attr or need_attr.group(1) != str(need):
                fails.append("%s: the tag's data-need is %s, the data's need is %r (run scripts/apply-large-screen.py)"
                             % (rel, need_attr.group(1) if need_attr else "missing", need))
        want = pointer_status(rel, facts)
        if not ptr_attr or ptr_attr.group(1) != want:
            fails.append('%s: the tag\'s data-pointer is %s, expected "%s" (%s)'
                         % (rel, '"%s"' % ptr_attr.group(1) if ptr_attr else "missing", want,
                            "its scripts read the pointer's position" if facts["pointer"] else "its scripts never read the pointer's position"))
    for rel, p in pages.items():
        src = read(p)
        if rel not in migrated and TAG_RE.search(src):
            fails.append("%s: carries the %s tag but is not on MIGRATED (the lists, then apply-large-screen.py)" % (rel, LAYER_URL))
        if OFF.search(src) and rel not in OPT_OUT:
            fails.append('%s: carries data-large-screen="off" with no OPT_OUT entry and reason' % rel)
    for rel, reason in OPT_OUT.items():
        if not str(reason).strip():
            fails.append("%s: OPT_OUT entry has no reason" % rel)
        if rel not in pages:
            fails.append("%s: on OPT_OUT but does not exist" % rel)
            continue
        if rel not in migrated:
            fails.append("%s: on OPT_OUT but not MIGRATED" % rel)
        if not OFF.search(read(pages[rel])):
            fails.append('%s: on OPT_OUT but its <html> does not carry data-large-screen="off"' % rel)
    for rel, reason in POINTER_VERIFIED.items():
        if rel not in migrated or rel not in pages:
            fails.append("%s: on POINTER_VERIFIED but not a MIGRATED page" % rel)
        elif not page_facts(root, rel)["pointer"]:
            fails.append("%s: on POINTER_VERIFIED but its scripts never read the pointer's position" % rel)
        if rel not in POINTER_TESTS:
            fails.append("%s: on POINTER_VERIFIED with no measured test in POINTER_TESTS" % rel)
    return fails


# ---------------------------------------------------------------------------------------------------- playing a page
# How a page is played: the game's own maffs-lock-hint (canon 7.6.0: start, start_sel, ready, answer), with these
# additions for a page that has none or is not a question game. Keys: start (JS), ready (JS expression), answer (JS
# using i: 0 right, >= 1 wrong), controls (selector of the answer controls), marked (JS expression: an answer has
# been marked), next (selector of Next), cont (JS that carries on), done (JS expression: the results screen).
ROUTES = {
    # A card game: no question_answered, no option group (phone-fit's unmeasurable list says the same).
    "games/maffscards/index.html": {
        "start": "MC.ui.start()",
        "ready": "!!window.MC && (MC.ui.state() === 'choosing' || MC.ui.state() === 'marvin')",
        "answer": "if (MC.ui.state() === 'choosing') { var r = document.querySelector('#yourCard .mc-row'); MC.ui.tap(r.dataset.key); } MC.ui.play();",
        "controls": "#yourCard .mc-row, #playBtn",
        "marked": "MC.ui.state() === 'reveal'",
        "next": "#nextBtn",
        "cont": "MC.ui.next()",
        "done": "MC.ui.state() === 'over'",
    },
}

_mods = {}


def _load(name, file):
    if name not in _mods:
        spec = importlib.util.spec_from_file_location(name, BASE / "scripts" / file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _mods[name] = mod
    return _mods[name]


def mpf():
    return _load("measure_phone_fit", "measure-phone-fit.py")


def route_for(root, rel):
    """The page's lock-hint with ROUTES' additions over it."""
    al = _load("check_answer_lock", "check-answer-lock.py")
    hint, faults = al.read_hint(read(root / rel))
    route = {} if faults else dict(hint)
    route.update(ROUTES.get(rel, {}))
    return route


def seed_js(seed):
    """Math.random from a seed and the page's path (check-site's PHONE_SEED with a seed mixed in), so a session is the
    same on every run and a different seed plays different questions."""
    return ("(() => { let h = 0x811c9dc5; const p = location.pathname + '#%d';"
            " for (let i = 0; i < p.length; i++) { h ^= p.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }"
            " let s = h; Math.random = function () { s = (s + 0x6D2B79F5) >>> 0; let t = s;"
            " t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);"
            " return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })();" % seed)


# One reading of the screen. Positions are from the top of the page (rect + scrollY) against the fold (the window less
# a pinned site footer), all in the units getBoundingClientRect and innerHeight share, which the layer holds the
# engine to; so the same reading serves zoomed and unzoomed.
SCREEN_JS = r"""(sel) => {
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width >= 2 && r.height >= 2 && s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0'; };
  const bottom = el => el.getBoundingClientRect().bottom + window.scrollY;
  const f = document.querySelector('.site-footer');
  const pinned = f && getComputedStyle(f).position === 'fixed' && vis(f);
  const inset = pinned ? f.getBoundingClientRect().height : 0;
  const ls = window.MaffsLargeScreen ? window.MaffsLargeScreen.state() : null;
  const out = { fold: window.innerHeight - inset, inset: inset, ih: window.innerHeight, iw: window.innerWidth,
                sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
                zoom: ls ? ls.zoom : null, by: ls ? ls.by : null, units: ls ? ls.units : null,
                style: document.documentElement.style.zoom || '', bottom: null, n: 0 };
  if (sel) {
    const els = [...document.querySelectorAll(sel)].filter(vis);
    out.n = els.length;
    out.bottom = els.length ? Math.max.apply(null, els.map(bottom)) : null;
  }
  const btn = [...document.querySelectorAll('button, [role="button"], a.btn')].filter(el => vis(el) && !el.closest('.site-footer, header, nav'));
  out.lowest = btn.length ? Math.max.apply(null, btn.map(bottom)) : null;
  return out;
}"""

MEDIA_JS = r"""() => {
  const out = [];
  const rules = list => { for (const r of list || []) {
    if (r.media && r.media.mediaText) out.push(r.media.mediaText);
    if (r.styleSheet) sheet(r.styleSheet);
    if (r.cssRules) rules(r.cssRules); } };
  const sheet = s => { if (s.media && s.media.mediaText) out.push(s.media.mediaText);
    let list = null; try { list = s.cssRules; } catch (e) {} rules(list); };
  for (const s of document.styleSheets) sheet(s);
  const uniq = [...new Set(out)].sort();
  return uniq.map(t => [t, matchMedia(t).matches]);
}"""

# The layout has stopped moving: fonts in, every visible control's box (phone-fit's signature) unchanged for `quiet` ms
# and, when `timers` is set, no timed change still due (a banner, a reveal). In the page, so a session costs no round
# trips while it waits. Timers are waited for only where a screen is about to change by itself (before the first
# question, and when a question shows no answer controls yet): MaffsScroll alone keeps a 4 s timer after every answer.
QUIET_JS = r"""async ([quiet, ceiling, timers]) => {
  if (document.fonts) { try { await document.fonts.ready; } catch (e) {} }
  const t0 = performance.now(); let last = null, since = t0;
  for (;;) {
    await new Promise(r => setTimeout(r, 50));
    const sig = window.__pfSig ? window.__pfSig() : '', pend = timers && window.__pfPending ? window.__pfPending() : 0;
    const now = performance.now();
    if (sig !== last) { last = sig; since = now; }
    if (now - since >= quiet && !pend) return true;
    if (now - t0 >= ceiling) return false;
  }
}"""

VH_JS = r"""() => { const p = document.createElement('div');
  p.style.cssText = 'position:absolute;left:0;top:0;width:1px;visibility:hidden;pointer-events:none';
  document.body.appendChild(p);
  const b = getComputedStyle(document.body).minHeight;
  const r = { body: document.body.getBoundingClientRect().height, ih: window.innerHeight, min: b,
              sh: document.documentElement.scrollHeight };
  p.remove(); return r; }"""


async def open_page(browser, base, rel, size, seed, layer=True, layer_body=None, html=None):
    """A context and page for one play. layer False: the layer's script is not served (the unzoomed page).
    layer_body: the layer's script replaced by this text (a plant). html: the page's own source replaced."""
    m, cs, bc = mpf(), mpf().cs, mpf().bc
    ctx = await browser.new_context(viewport={"width": size[0], "height": size[1]}, reduced_motion="reduce")
    await ctx.add_init_script(seed_js(seed))
    await ctx.add_init_script(cs.TIER3_INIT)
    await ctx.add_init_script(m.CORRECT_INIT)
    await ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    page = await ctx.new_page()

    async def handle(r):
        url = r.request.url
        try:
            if url.split("?")[0].endswith(LAYER_URL):
                if not layer:
                    return await r.fulfill(status=200, content_type="application/javascript", body="/* layer off */")
                if layer_body is not None:
                    return await r.fulfill(status=200, content_type="application/javascript; charset=utf-8", body=layer_body)
                return await r.continue_()
            if html is not None and url.split("?")[0].endswith("/" + rel):
                return await r.fulfill(status=200, content_type="text/html; charset=utf-8", body=html)
            if bc.is_font_cdn(url):
                got = bc.real_font_response(url)
                return await (r.fulfill(**got) if got else r.abort())
            if not url.startswith(base) or cs.block_reason(url):
                return await r.abort()
            return await r.continue_()
        except Exception:
            pass
    await page.route("**/*", handle)
    await page.goto(base + "/" + rel + "?cb=large-screen", wait_until="domcontentloaded", timeout=30000)
    try:
        await asyncio.wait_for(page.evaluate("document.fonts.ready.then(() => 1)"), timeout=8)
    except Exception:
        pass
    return ctx, page


async def walk(page, root, rel, on_screen, max_questions=MAX_QUESTIONS):
    """Play one session to the results screen, calling on_screen(kind, reading, info) at each screen: 'start',
    'question', 'answered' (info["correct"]), 'results'. Returns a note on how far it got ('' for the whole way)."""
    m = mpf()
    route = route_for(root, rel)

    async def ev(js, arg=None):
        return await asyncio.wait_for(page.evaluate(js, arg), timeout=15)

    async def expr(js):
        try:
            return bool(await ev("() => { try { return !!(%s); } catch (e) { return false; } }" % js))
        except Exception:
            return False

    async def quiet(timers=False):
        try:
            await asyncio.wait_for(page.evaluate(QUIET_JS, [250, 5000, timers]), timeout=10)
        except Exception:
            pass

    async def reading(sel=None):
        await ev("window.scrollTo(0, 0)")
        return await ev(SCREEN_JS, sel)

    async def asking():
        """The answer controls: the route's selector, else phone-fit's reading of the page."""
        if route.get("controls"):
            return await reading(route["controls"])
        r = await reading()
        a = await ev("window.__pfAsking()")
        r["n"], r["bottom"] = a["n"], a["bottom"]
        return r

    async def started():
        if route.get("ready"):
            return await expr(route["ready"])
        return (await ev("window.__mfgStats()"))["started"] > 0

    async def done():
        if route.get("done"):
            return await expr(route["done"])
        st = await ev("window.__mfgStats()")
        return st["completed"] > 0 or (await ev("window.__mfgProbe()"))["atEnd"]

    await quiet()
    await on_screen("start", await reading(), {})

    # To the first question: the page's declared start, else the generic route (a level, then Start).
    if route.get("start"):
        try:
            await asyncio.wait_for(page.evaluate("async () => { %s }" % route["start"]), timeout=15)
        except Exception:
            pass
    elif route.get("start_sel"):
        try:
            await page.click(route["start_sel"], timeout=5000)
        except Exception:
            pass
    else:
        picked = False
        for _ in range(5):
            if (await ev("window.__mfgStats()"))["started"]:
                break
            if not picked and (await ev("window.__mfgProbe()"))["n"] >= 2:
                await ev("window.__mfgClickOpt(0)")
                picked = True
            elif await ev("window.__mfgHasStart()"):
                await ev("window.__mfgClickStart()")
            else:
                break
            await quiet()
    for _ in range(60):
        if await started():
            break
        await page.wait_for_timeout(100)
    else:
        return "the game did not start"

    for q in range(max_questions):
        for _ in range(100):                             # a banner or a deal between questions
            if await done() or not route.get("ready") or await expr(route["ready"]):
                break
            await page.wait_for_timeout(100)
        if await done():
            break
        await quiet(timers=(q == 0))
        if await done():
            break
        ask = await asking()
        if not ask["n"]:                                 # a banner over the question: wait it out, once
            await quiet(timers=True)
            ask = await asking()
        if not ask["n"]:
            return "question %d: no answer controls found" % (q + 1)
        await on_screen("question", ask, {"q": q + 1})

        # A wrong answer every time (Next after a wrong answer is what the fold rule is about): the page's declared
        # answer with i = 1, else the generic driver's press.
        before = (await ev("window.__pfLastAnswer()"))["n"]
        keys = (await ev("window.__mfgProbe()"))["keys"]
        if route.get("answer"):
            try:
                await ev("(i) => { %s }" % route["answer"], 1)
            except Exception as e:
                return "question %d: the declared answer failed: %s" % (q + 1, str(e).split("\n")[0][:80])
        else:
            p = await ev("window.__mfgProbe()")
            if p["n"] >= 2:
                await ev("(i) => window.__mfgClickOpt(i)", (q + 1) % p["n"])
            elif await ev("window.__mfgHasInput()"):
                await ev("(v) => window.__mfgTypeAnswer(v)", "1")
            else:
                return "question %d: nothing to answer with" % (q + 1)

        async def is_marked():
            if route.get("marked"):
                return await expr(route["marked"])
            return (await ev("window.__pfLastAnswer()"))["n"] > before
        marked = False
        for _ in range(60):
            await page.wait_for_timeout(100)
            marked = await is_marked()
            if marked or await done():
                break
        if not marked:
            if await done():
                break
            return "question %d: the answer was not marked" % (q + 1)
        correct = None if route.get("marked") else (await ev("window.__pfLastAnswer()"))["c"]
        await quiet()
        if await done():
            break

        # Next: the route's selector, else phone-fit's reading (.maffs-next, or a continue-like control). A game that
        # moves on by itself has none: two seconds after the layout went quiet, or a new question, settles that.
        async def find_next():
            if route.get("next"):
                return await reading(route["next"])
            r = await reading()
            got = await ev("window.__pfNext()")
            r["n"], r["bottom"] = (1 if got.get("found") else 0), got.get("bottom")
            return r
        nxt = await find_next()
        for _ in range(20):
            if nxt["n"] or await done():
                break
            p = await ev("window.__mfgProbe()")
            if (await ev("window.__pfLastAnswer()"))["n"] == before + 1 and p["n"] >= 2 and p["keys"] != keys:
                break                                    # the next question is already up
            await page.wait_for_timeout(100)
            nxt = await find_next()
        if nxt["n"]:
            await quiet()
            nxt = await find_next()
        await on_screen("answered", nxt, {"q": q + 1, "correct": correct})
        if nxt["n"]:
            if route.get("cont"):
                await ev("() => { %s }" % route["cont"])
            else:
                await ev("window.__mfgClickContinue()")
            for _ in range(60):                          # Next has gone: the next question, or the end
                await page.wait_for_timeout(50)
                if await done() or not (await find_next())["n"]:
                    break
    else:
        return "no results screen after %d questions" % max_questions
    await quiet()
    await on_screen("results", await reading(), {})
    return ""


# ---------------------------------------------------------------------------------------------------- pointer tests
# A measured test under zoom for each POINTER_VERIFIED page: an async function (page) -> [failures].
POINTER_TESTS = {}


# ---------------------------------------------------------------------------------------------------- the browser check
def near(a, b, tol=1.5):
    return a is not None and b is not None and abs(a - b) <= tol


async def check_page(browser, base, root, rel, engine, shots=None, layer_body=None, sizes=None, html=None):
    """(failures, report lines) for one page in one engine."""
    fails, report = [], []
    facts = page_facts(root, rel)
    entry = load_data(root).get(rel) or {}
    need = entry.get("need")
    pointer = pointer_status(rel, facts)
    opted = bool(OFF.search(read(root / rel) if html is None else html))
    slug = rel.split("/")[-2]
    for size in (sizes or ZOOM_SIZES + FLAT_SIZES):
        W, H = size
        tag = "%s %s %dx%d" % (slug, engine, W, H)
        want, by = expected_zoom(W, H, facts, need, pointer, opted)
        # The unzoomed page at the same size: which screens scroll sideways anyway.
        base_side = {}

        async def flat(kind, r, info):
            base_side[(kind, info.get("q"))] = r["sw"] > r["cw"] + 1
        ctx, page = await open_page(browser, base, rel, size, CHECK_SEED, layer=False, html=html)
        try:
            flat_note = await walk(page, root, rel, flat)
        finally:
            await ctx.close()

        seen = {"n": 0, "zoom": None, "engine": None, "kinds": set()}

        async def judge(kind, r, info):
            seen["n"] += 1
            seen["kinds"].add(kind)
            where = "%s, %s%s" % (tag, kind, " %d" % info["q"] if info.get("q") else "")
            if r["zoom"] is None:
                fails.append("%s: the layer is not running (no MaffsLargeScreen)" % where)
                return
            refused = str(r["by"]).startswith("engine")
            if refused:
                seen["engine"] = r["by"]
            if not near(r["zoom"], want, 0.001) and not (refused and r["zoom"] == 1):
                fails.append("%s: zoom %s (%s), this script's reading of the rule gives %s (%s)" % (where, r["zoom"], r["by"], want, by))
            if seen["zoom"] is None:
                seen["zoom"] = r["zoom"]
            if r["sw"] > r["cw"] + 1 and not base_side.get((kind, info.get("q"))):
                fails.append("%s: scrolls sideways (%d px wide in a %d px window) and does not without the layer" % (where, r["sw"], r["cw"]))
            if r["zoom"] and r["zoom"] > 1:
                if r["units"] not in ("vh zoomed", "vh not zoomed"):
                    fails.append("%s: zoomed, and the layer's account of the engine is %r" % (where, r["units"]))
                if kind in ("question", "answered") and r["n"] and r["bottom"] is not None and r["bottom"] > r["fold"] + 0.5:
                    fails.append("%s: %s at %d px, %d px under the fold (%d) at zoom %s"
                                 % (where, "the answer controls end" if kind == "question" else "Next ends", r["bottom"], r["bottom"] - r["fold"], r["fold"], r["zoom"]))
            if kind in ("start", "results") and r.get("lowest") is not None:
                report.append("%s: the lowest button ends %d px %s the fold (zoom %s; reported, not judged)"
                              % (where, abs(r["lowest"] - r["fold"]), "under" if r["lowest"] > r["fold"] else "above", r["zoom"]))
            if shots and size in SHOT_SIZES and engine == "chromium" and (kind in ("start", "results") or (info.get("q") == 1)):
                name = "%s-%dx%d-%s.jpg" % (slug, W, H, {"answered": "wrong-answer"}.get(kind, kind))
                await page.evaluate("window.scrollTo(0, 0)")
                await page.screenshot(path=os.path.join(shots, name), type="jpeg", quality=72)

        ctx, page = await open_page(browser, base, rel, size, CHECK_SEED, layer_body=layer_body, html=html)
        try:
            first = await page.evaluate(SCREEN_JS, None)
            if first["zoom"] and first["zoom"] > 1:
                # Every media query answers as on the unzoomed page at the effective size (rule c, seen from outside).
                got = await page.evaluate(MEDIA_JS)
                answers = []
                for rnd in (math.floor, math.ceil):
                    eff = (int(rnd(W / first["zoom"])), int(rnd(H / first["zoom"])))
                    c2, p2 = await open_page(browser, base, rel, eff, CHECK_SEED, layer=False, html=html)
                    try:
                        answers.append(dict(await p2.evaluate(MEDIA_JS)))
                    finally:
                        await c2.close()
                for text, matches in got:
                    if all(a.get(text) is not None and a.get(text) != matches for a in answers):
                        fails.append('%s: "@media %s" %s on the zoomed page and %s on an unzoomed %dx%d window (zoom %s)'
                                     % (tag, text, "matches" if matches else "does not match", "does not" if matches else "does",
                                        round(W / first["zoom"]), round(H / first["zoom"]), first["zoom"]))
                vh = await page.evaluate(VH_JS)
                if vh["min"].endswith("px") and float(vh["min"][:-2]) > 0 and vh["body"] > vh["ih"] + 2 and vh["sh"] > vh["ih"] + 2:
                    # the body's min-height reaches past the screen only if the page's content does too: compare unzoomed
                    c2, p2 = await open_page(browser, base, rel, (int(W / first["zoom"]), int(H / first["zoom"])), CHECK_SEED, layer=False, html=html)
                    try:
                        flat_vh = await p2.evaluate(VH_JS)
                    finally:
                        await c2.close()
                    if flat_vh["body"] <= flat_vh["ih"] + 2:
                        fails.append("%s: the start screen's body is %d px tall on a %d px window at zoom %s, and fits the window unzoomed "
                                     "at the effective size (100vh not divided back)" % (tag, vh["body"], vh["ih"], first["zoom"]))
            note = await walk(page, root, rel, judge)
            if note:
                fails.append("%s: the session stopped: %s" % (tag, note))
            elif not {"start", "question", "answered", "results"} <= seen["kinds"]:
                fails.append("%s: the session did not reach %s" % (tag, ", ".join(sorted({"start", "question", "answered", "results"} - seen["kinds"]))))
            if rel in POINTER_VERIFIED and seen["zoom"] and seen["zoom"] > 1 and rel in POINTER_TESTS:
                c3, p3 = await open_page(browser, base, rel, size, CHECK_SEED, layer_body=layer_body, html=html)
                try:
                    fails.extend("%s: pointer test: %s" % (tag, f) for f in await POINTER_TESTS[rel](p3))
                finally:
                    await c3.close()
        finally:
            await ctx.close()
        if seen["engine"]:
            report.append("%s: *** THE LAYER REFUSED THIS ENGINE'S ZOOM: %s. The page stays unzoomed here (rule would give %s). ***"
                          % (tag, seen["engine"], want))
        report.append("%s: zoom %s, limited by %s; %d screens played%s"
                      % (tag, seen["zoom"], by, seen["n"], "" if not flat_note else " (without the layer: %s)" % flat_note))
    return fails, report


def unit_names(engines):
    return ["%s %s" % (rel.split("/")[-2], e) for rel in MIGRATED for e in engines]


async def run_units(units, engines, shots=None):
    from playwright.async_api import async_playwright
    bc = mpf().bc
    fails, report, missing = [], [], []
    proc, base = bc.start_stub_server()
    try:
        async with async_playwright() as pw:
            browsers = {}
            for uid, shard_unit in units:
                slug, engine = uid.rsplit(" ", 1)
                rel = "games/%s/index.html" % slug
                with shard_unit:
                    if engine not in browsers:
                        try:
                            browsers[engine] = await getattr(pw, engine).launch()
                        except Exception as e:
                            browsers[engine] = None
                            missing.append("%s: %s" % (engine, str(e).split("\n")[0][:120]))
                    if browsers[engine] is None:
                        continue
                    try:
                        f, r = await check_page(browsers[engine], base, BASE, rel, engine, shots=shots)
                    except Exception as e:  # noqa: BLE001
                        f, r = ["%s %s: the check itself failed: %s" % (slug, engine, str(e).split("\n")[0][:200])], []
                    fails.extend(f)
                    report.extend(r)
            for b in browsers.values():
                if b is not None:
                    await b.close()
    finally:
        proc.terminate()
    return fails, report, missing


# ---------------------------------------------------------------------------------------------------- the plants
def static_plants():
    """[(name, edit(root))]: each makes check_static fail on a temporary copy of the tree's pages."""
    def edit(rel, old, new, name, regex=False):
        def go(root):
            f = root / rel
            src = read(f)
            out = pc.apply_re_plant(src, old, new, name=name) if regex else pc.apply_plant(src, old, new, name=name)
            with open(f, "w", encoding="utf-8", newline="") as fh:
                fh.write(out)
        return go

    def tag_of(rel):
        return TAG_RE.search(read(BASE / rel)).group(0)
    a, b, c = MIGRATED[0], MIGRATED[1], MIGRATED[6]
    held = next((r for r in MIGRATED if pointer_status(r, page_facts(BASE, r)) == "held"), None)
    plants = [
        ("a MIGRATED page without the tag", edit(a, tag_of(a), "", "the tag removed")),
        ("a MIGRATED page carrying the tag twice", edit(b, tag_of(b), tag_of(b) + "\n" + tag_of(b), "the tag doubled")),
        ("an unlisted page carrying the tag", edit("games/formula-forge/index.html", "</head>", tag_for(700, "none") + "\n</head>", "a hand-linked page")),
        ("an unlisted opt-out", edit(b, r"<html\b", '<html data-large-screen="off"', "an unlisted opt-out", regex=True)),
        ("a tag whose need is not the data's", edit(c, r'data-need="(\d+)"', lambda m: 'data-need="%d"' % (int(m.group(1)) - 100), "the tag's need lowered", regex=True)),
        ("a stale entry (a breakpoint added to the page)", edit(c, "</style>", "@media (min-height: 901px) { body { margin: 0; } }\n</style>", "a new breakpoint")),
    ]
    if held:
        plants.append(('a tag marked "verified" for a page not on POINTER_VERIFIED',
                       edit(held, 'data-pointer="held"', 'data-pointer="verified"', "the pointer status changed by hand")))
    return plants


def copy_tree(tmp):
    dst = tmp / "tree"
    if dst.exists():
        shutil.rmtree(dst)
    for rel in MIGRATED + ["games/formula-forge/index.html", LAYER, DATA]:
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(BASE / rel, dst / rel)
    shutil.copytree(BASE / "schools" / "assets", dst / "schools" / "assets", dirs_exist_ok=True)
    return dst


def layer_plants():
    """[(name, layer text, page, size, the failure expected)]: a rule removed from the layer; the browser check on that
    page must fail. Each page and size is one where that rule is the one that limits the zoom."""
    src = read(BASE / LAYER)
    out = []
    spec = [
        ("rule c removed (a page zooms across its own height breakpoint)",
         [("      if ((x.kind === 'ge' || x.kind === 'lt') && v >= x.t) cap(", "      if (false) cap("),
          ("      if ((x.kind === 'le' || x.kind === 'gt') && v > x.t) cap(", "      if (false) cap(")], "c: "),
        ("rule d removed (a page's zoom ignores its height need)",
         [("    cap(steps(H / need, false), 'd: height need ' + need);", "")], "d: "),
        ("rule e removed (a page that reads clientX is zoomed, unverified)",
         [("    if (pointer !== 'none' && pointer !== 'verified') return { zoom: 1, by: 'e: pointer use not verified' };", "")], "e: "),
    ]
    data = load_data(BASE)
    for name, edits, rule in spec:
        body = src
        for old, new in edits:
            body = pc.apply_plant(body, old, new, name=name)
        # the page and size where this rule limits the zoom, by this script's own reading
        where = None
        for rel in MIGRATED:
            facts = page_facts(BASE, rel)
            for size in ZOOM_SIZES:
                z, by = expected_zoom(size[0], size[1], facts, (data.get(rel) or {}).get("need"), pointer_status(rel, facts))
                if by.startswith(rule) and where is None:
                    where = (rel, size)
        out.append((name, body, where, rule))
    return out


async def run_plants(engine="chromium"):
    from playwright.async_api import async_playwright
    bc = mpf().bc
    bad = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="large-screen-selftest-"))
    try:
        clean = check_static(copy_tree(tmp))
        if clean:
            bad.append("the clean copy fails the static check: %s" % clean[:3])
        for name, plant in static_plants():
            root = copy_tree(tmp)
            try:
                plant(root)
            except pc.StalePlant as e:
                bad.append(str(e))
                print("  %-78s *** %s ***" % (name, e))
                continue
            found = check_static(root)
            print("  %-78s %s" % (name, "caught: " + found[0][:90] if found else "*** MISSED ***"))
            if not found:
                bad.append("plant not caught: " + name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    proc, base = bc.start_stub_server()
    try:
        async with async_playwright() as pw:
            browser = await getattr(pw, engine).launch()
            try:
                plants = layer_plants()
            except pc.StalePlant as e:
                bad.append(str(e))
                plants = []
            for name, body, where, rule in plants:
                if where is None:
                    bad.append("plant %r: no MIGRATED page is limited by rule %s at %s, so nothing proves the check for it" % (name, rule, ZOOM_SIZES))
                    print("  %-78s *** NO PAGE LIMITED BY THIS RULE ***" % name)
                    continue
                rel, size = where
                f, _ = await check_page(browser, base, BASE, rel, engine, layer_body=body, sizes=[size])
                hit = [x for x in f if "this script's reading of the rule gives" in x]
                print("  %-78s %s" % (name, "caught: " + hit[0][:110] if hit else "*** MISSED ***"))
                if not hit:
                    bad.append("plant not caught: " + name)
            # a MIGRATED page without the layer, in the browser: the tag removed from the served page
            rel = MIGRATED[1]
            html = pc.apply_plant(read(BASE / rel), TAG_RE.search(read(BASE / rel)).group(0), "", name="the tag removed from the served page")
            f, _ = await check_page(browser, base, BASE, rel, engine, sizes=[ZOOM_SIZES[0]], html=html)
            hit = [x for x in f if "the layer is not running" in x]
            name = "a MIGRATED page served without the tag (in the browser)"
            print("  %-78s %s" % (name, "caught: " + hit[0][:110] if hit else "*** MISSED ***"))
            if not hit:
                bad.append("plant not caught: " + name)
            await browser.close()
    finally:
        proc.terminate()
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true", help="the planted faults only")
    ap.add_argument("--static", action="store_true", help="the static check only")
    ap.add_argument("--only", help="browser units whose name holds this text (local use; no plants)")
    ap.add_argument("--engines", default=None, help="comma-separated; default: all three in CI, those installed otherwise")
    ap.add_argument("--shots", metavar="DIR", help="save a screenshot of each screen at 1920x955 and 1366x650 (Chromium)")
    bc = mpf().bc
    bc.shard_args(ap)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    in_ci = bool(os.environ.get("CI"))
    engines = args.engines.split(",") if args.engines else ENGINES
    shard = bc.Shard(__file__, args)
    all_units = ["static"] + unit_names(engines) + ["plants"]
    mine = shard.pick(all_units)
    if args.selftest:
        mine = ["plants"]
    elif args.static:
        mine = ["static"]
    elif args.only:
        mine = [u for u in all_units if args.only in u and u != "plants"]
    fails = []
    if "static" in mine:
        with shard.unit("static"):
            fails.extend(check_static(BASE))
            print("check-large-screen: static %s (%d MIGRATED, %d OPT_OUT, %d POINTER_VERIFIED)"
                  % ("FAIL" if fails else "PASS", len(MIGRATED), len(OPT_OUT), len(POINTER_VERIFIED)))
    browser_units = [(u, shard.unit(u)) for u in mine if u not in ("static", "plants")]
    if browser_units:
        if args.shots:
            os.makedirs(args.shots, exist_ok=True)
        f, report, missing = asyncio.run(run_units(browser_units, engines, shots=args.shots))
        fails.extend(f)
        for line in report:
            print("  " + line)
        for line in missing:
            if in_ci or args.engines:
                fails.append("engine not available: " + line)
            else:
                print("  NOT RUN (engine not installed here; CI runs it): " + line)
    if "plants" in mine:
        with shard.unit("plants"):
            bad = asyncio.run(run_plants())
            fails.extend("self-test: " + b for b in bad)
            print("check-large-screen self-test: %s" % ("FAIL" if bad else "PASS, every plant caught"))
    for f in fails[:120]:
        print("FAIL:", f)
    if len(fails) > 120:
        print("FAIL: ... and %d more" % (len(fails) - 120))
    print("check-large-screen: %s" % ("FAIL" if fails else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
