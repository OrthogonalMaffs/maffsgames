#!/usr/bin/env python3
"""Every game page, live escape room, the escape-rooms hub and /essentials/ carries the search title and description data/games.json generates.

    python scripts/check-meta.py              # CI
    python scripts/check-meta.py --selftest   # plant faults in a copy of the tree; all must be caught
    python scripts/check-meta.py --table      # markdown table: current title vs generated (for a PR)
    python scripts/check-meta.py --root <copy of the repo>   # testing

Until October 2026 each page's <title> and meta description were written by hand and named the
game ("Like Terms Collector — MaffsGames"), while teachers search for the topic ("collecting like
terms game"). Nothing held the 97 heads to one rule, so they are now generated from one file and
held here. This script is the authority on the rules: scripts/apply-meta.py imports them.

The rules (Jon, 5 Oct 2026):
  - Levels come from the Levels column of .claude/rules/game-roster.md, in teacher words (LEVEL_WORDS).
    "Year 6" is never shown, in a title or a description (SR-11 and the resit audience): it is left
    out of a mixed game's levels, and a Year 6-only game has no levels at all.
  - Title: "<search_phrase> Game – <levels> Maths | MaffsGames", levels joined with "/" in ORDER,
    at most 60 characters. " Maths" is not added after "Core Maths" or "Further Maths". Over 60:
    keep only "GCSE" if the game serves GCSE, otherwise its lowest level (RANK); still over 60, or
    no levels: "<search_phrase> Maths Game | MaffsGames" (no " Maths" if the phrase already says
    maths or mathematical). The phrase is never shortened.
  - Description: "<description> For <levels>. Free, no sign-up.", at most 155 characters; with no
    levels, "<description> Free, no sign-up."
  - og:title and twitter:title carry the title; og:description and twitter:description carry the
    description. Twitter tags are held wherever a page has them; og: tags are required.
  - /essentials/'s title and description are stated in games.json's "pages" and held the same way.
  - Escape rooms (contract ROOM-SEARCH-TITLES, Jon, 6 Nov 2026): every live room (its index.html is not noindex) has one
    entry in games.json's "rooms", and the hub is in "pages". Title: "<search_phrase> Escape Room – <level> | MaffsGames",
    at most 60 characters; over 60, "<search_phrase> Escape Room | MaffsGames", reported. Description: "Maths escape room
    on <topics>. <clock> minutes, <level>. Free, no sign-up.", at most 155 characters. <topics> is the lockMeta topics in
    the room's teacher.html, joined "A, B and C", all lower case except acronyms and ROOM_PROPER; over 155, the entry's
    short_topics through the same rule. <clock> is `minutes:` in its room.js, the start screen's figure, never the sum
    of lockMeta minutes (those are puzzle time). The head is the only source of a room's title: neither the engine nor a
    room script assigns document.title (teacher.js may: its pages are noindex).
  - Search keywords (contract SEARCH-KEYWORDS, Jon, 4 Nov 2026): every game has "keywords", at least 4, each lower
    case, trimmed, 2-40 characters, none twice. Every card on the portal (a.game-card) and /essentials/ (a.card)
    carries data-keywords="kw1 | kw2 | ..." from the record its link resolves to: the game's, or for a page that is not
    a game (The 6 P's) its "pages" record's keywords. For on-site search only (schools/assets/search.js), never SEO.

It fails when:
  - games.json's slugs differ from the roster's numbered rows (a withdrawn game, numbered "—", is
    not one), or one is listed twice, or a phrase or description is empty or "PHRASE NEEDED";
  - a live room has no "rooms" entry, an entry is not a live room or is listed twice, its timer or lockMeta cannot be
    read, or its description is over 155 with no short_topics or with them; a room script assigns document.title;
  - a generated title is over 60 or a description over 155, two titles are the same, or any title
    or description says "Year 6" or "Starter";
  - a page's <title>, meta description, og:/twitter: copies differ from what games.json generates,
    a required tag is missing or doubled, or its canonical link is not its own URL exactly once;
  - a game's keywords break a rule above; a card's data-keywords are missing, doubled or differ from games.json; a
    card links to a slug with no games.json record (listed, never given invented keywords), or to a record with none;
  - a PENDING game's page already matches (stale: remove it from PENDING in the PR that applies it),
    or a PENDING slug is not a roster game.

To change a title, description or keywords: edit data/games.json, run scripts/apply-meta.py, then this.
Never hand-edit a game's title. Stdlib only; under a second, plus a self-test on every run.
"""
import argparse, html, json, pathlib, re, shutil, sys, tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
ROSTER = ".claude/rules/game-roster.md"
DATA = "data/games.json"
SITE = "https://maffsgames.co.uk/"
TITLE_MAX, DESC_MAX = 60, 155
PHRASE_NEEDED = "PHRASE NEEDED"

# Roster Levels label (lower case) -> the word a teacher searches with. None: never shown (SR-11).
# A label not listed here is an error, never dropped.
LEVEL_WORDS = {
    "year 6": None, "ks3": "KS3", "gcse": "GCSE", "a-level": "A-Level", "a-level year 2": "A-Level",
    "l3": "Level 3", "l4": "Level 4", "further": "Further Maths", "core": "Core Maths",
}
# The order levels are written in.
ORDER = ["KS3", "GCSE", "A-Level", "Level 3", "Level 4", "Further Maths", "Core Maths"]
# "Lowest level" when a title keeps one (and the game does not serve GCSE): Core Maths is a
# Level 3 qualification below A-Level; Further Maths and Level 4 (HNC) sit above A-Level.
RANK = ["KS3", "GCSE", "Core Maths", "A-Level", "Level 3", "Further Maths", "Level 4"]

# Games in games.json whose page is not yet written: slug -> reason. Reported, never fails; fails
# once the page matches (remove the entry in the PR that runs apply-meta.py on it).
PENDING = {}

BANNED = re.compile(r"\byear\s*6\b|\bstarter\b", re.I)

ROOMS_DIR = "escape-rooms"
# Keep their capitals in a room's topics, with any all-capitals word (LCM, HCF).
ROOM_PROPER = {"Venn", "Pythagoras", "Celsius"}
ASSIGNS_TITLE = re.compile(r"""document\s*(?:\.\s*title|\[\s*["']title["']\s*\])\s*=(?!=)""")


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------

def roster(root):
    """[(slug, Levels cell)] for every numbered row, in roster order."""
    out = []
    for line in (root / ROSTER).read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 4 and c[0].isdigit():
            m = re.match(r"^`([a-z0-9-]+)`$", c[2])
            if m:
                out.append((m.group(1), c[3]))
    return out


def level_words(cell):
    words = []
    for part in cell.split(","):
        label = part.strip().lower()
        if label not in LEVEL_WORDS:
            raise ValueError("roster level %r has no entry in check-meta.py's LEVEL_WORDS" % part.strip())
        w = LEVEL_WORDS[label]
        if w and w not in words:
            words.append(w)
    return sorted(words, key=ORDER.index)


def _with_levels(phrase, words):
    lv = "/".join(words)
    if not lv.endswith("Maths"):
        lv += " Maths"
    return "%s Game – %s | MaffsGames" % (phrase, lv)


def fallback_title(phrase):
    maths = "" if re.search(r"\bmath", phrase, re.I) else " Maths"
    return "%s%s Game | MaffsGames" % (phrase, maths)


def title_for(phrase, words):
    if words:
        t = _with_levels(phrase, words)
        if len(t) <= TITLE_MAX:
            return t
        if len(words) > 1:
            one = "GCSE" if "GCSE" in words else min(words, key=RANK.index)
            t = _with_levels(phrase, [one])
            if len(t) <= TITLE_MAX:
                return t
    return fallback_title(phrase)


def description_for(practises, words):
    if not words:
        return "%s Free, no sign-up." % practises
    s = words[0] if len(words) == 1 else ", ".join(words[:-1]) + " and " + words[-1]
    return "%s For %s. Free, no sign-up." % (practises, s)


def live_rooms(root):
    """Every live room's slug: a folder with room.js whose index.html is not noindex (as check-escape-rooms.py reads it)."""
    return sorted(d.name for d in (root / ROOMS_DIR).iterdir() if (d / "room.js").is_file() and (d / "index.html").is_file()
                  and "noindex" not in (d / "index.html").read_text(encoding="utf-8"))


def room_clock(js):
    """The room's own timer, `minutes:` in room.js, the figure its start screen shows; None unless there is exactly one."""
    found = re.findall(r"^\s*minutes:\s*(\d+)\s*,", js, re.M)
    return int(found[0]) if len(found) == 1 else None


def room_topics(page):
    """The lockMeta topics in a teacher page's window.TEACH; [] when they cannot be read."""
    m = re.search(r'"lockMeta"\s*:\s*(?=\[)', page)
    if not m:
        return []
    try:
        meta, _ = json.JSONDecoder().raw_decode(page[m.end():])
        return [html.unescape(x["topic"]).strip() for x in meta]
    except (ValueError, KeyError, TypeError):
        return []


def topics_lower(text):
    """All lower case except acronyms and ROOM_PROPER."""
    return re.sub(r"[^\W\d_]+", lambda m: m.group(0) if m.group(0) in ROOM_PROPER or (len(m.group(0)) > 1 and m.group(0).isupper())
                  else m.group(0).lower(), text)


def room_title(phrase, level):
    """(title, used the fallback)."""
    t = "%s Escape Room – %s | MaffsGames" % (phrase, level)
    return (t, False) if len(t) <= TITLE_MAX else ("%s Escape Room | MaffsGames" % phrase, True)


def room_description(topics, clock, level):
    return "Maths escape room on %s. %d minutes, %s. Free, no sign-up." % (topics_lower(topics), clock, level)


def expected_rooms(root, data):
    """The live rooms' expected values, and [data errors]."""
    out, errors, seen = {}, [], {}
    rooms = data.get("rooms", [])
    for r in rooms:
        seen[r.get("slug")] = seen.get(r.get("slug"), 0) + 1
    live = live_rooms(root)
    for s, n in seen.items():
        if n > 1:
            errors.append("games.json: room %s listed %d times" % (s, n))
    for s in sorted(set(live) - set(seen)):
        errors.append("games.json: live room %s has no entry in \"rooms\"" % s)
    for s in sorted(set(seen) - set(live)):
        errors.append("games.json: room %s is not a live room" % s)
    for r in rooms:
        slug = r.get("slug")
        if slug not in live:
            continue
        phrase, level = (r.get("search_phrase") or "").strip(), (r.get("level") or "").strip()
        if not phrase or not level:
            errors.append("games.json: room %s has no search_phrase or level" % slug)
            continue
        clock = room_clock((root / ROOMS_DIR / slug / "room.js").read_text(encoding="utf-8"))
        if clock is None:
            errors.append("%s: the room's timer cannot be read from its room.js" % slug)
            continue
        topics = room_topics((root / ROOMS_DIR / slug / "teacher.html").read_text(encoding="utf-8"))
        if not topics:
            errors.append("%s: no lockMeta topics can be read from its teacher.html" % slug)
            continue
        joined = topics[0] if len(topics) == 1 else ", ".join(topics[:-1]) + " and " + topics[-1]
        description, short = room_description(joined, clock, level), False
        if len(description) > DESC_MAX:
            if not r.get("short_topics"):
                errors.append("%s: description is %d characters with no short_topics (a person writes them)" % (slug, len(description)))
                continue
            description, short = room_description(r["short_topics"], clock, level), True
            if len(description) > DESC_MAX:
                errors.append("%s: description is still over %d characters with its short_topics (%d)" % (slug, DESC_MAX, len(description)))
                continue
        title, fallback = room_title(phrase, level)
        out["%s/%s/index.html" % (ROOMS_DIR, slug)] = {
            "slug": "%s/%s" % (ROOMS_DIR, slug), "title": title, "description": description,
            "canonical": SITE + "%s/%s/" % (ROOMS_DIR, slug), "fallback": fallback, "short": short}
    return out, errors


def title_assignments(root):
    """Every room script that assigns document.title: the head is the only source of a room's title. teacher.js may."""
    rooms = root / ROOMS_DIR
    paths = [p for p in sorted((rooms / "assets").glob("*.js")) if p.name != "teacher.js"]
    paths += sorted(rooms.glob("*/room.js")) + [rooms / s / "index.html" for s in live_rooms(root)]
    return ["%s assigns document.title (the head is the only source of a room's title)" % p.relative_to(root).as_posix()
            for p in paths if ASSIGNS_TITLE.search(p.read_text(encoding="utf-8"))]


def load(root):
    return json.loads((root / DATA).read_text(encoding="utf-8"))


def expected(root):
    """({page path: {"title", "description", "canonical", "slug"}}, [data errors])."""
    errors, out = [], {}
    rows = roster(root)
    data = load(root)
    games = data.get("games", [])
    seen = {}
    for g in games:
        seen[g.get("slug")] = seen.get(g.get("slug"), 0) + 1
    for slug, n in seen.items():
        if n > 1:
            errors.append("games.json: %s listed %d times" % (slug, n))
    rslugs = [s for s, _ in rows]
    for s in sorted(set(rslugs) - set(seen)):
        errors.append("games.json: roster game %s is missing" % s)
    for s in sorted(set(seen) - set(rslugs)):
        errors.append("games.json: %s is not a numbered roster row" % s)
    for s in sorted(set(PENDING) - set(rslugs)):
        errors.append("PENDING: %s is not a roster game" % s)
    by = {g.get("slug"): g for g in games}
    for slug, cell in rows:
        g = by.get(slug)
        if g is None:
            continue
        phrase, practises = (g.get("search_phrase") or "").strip(), (g.get("description") or "").strip()
        if not phrase or not practises or PHRASE_NEEDED in (phrase, practises):
            errors.append("games.json: %s has no search_phrase or description" % slug)
            continue
        words = level_words(cell)
        out["games/%s/index.html" % slug] = {
            "slug": slug, "title": title_for(phrase, words),
            "description": description_for(practises, words),
            "canonical": SITE + "games/%s/" % slug}
    for g in games:
        errors += keyword_errors("games.json: %s" % g.get("slug"), g.get("keywords"))
    for path, page in sorted(data.get("pages", {}).items()):
        if "keywords" in page:
            errors += keyword_errors("games.json: pages %s" % path, page["keywords"])
    for path, page in sorted(data.get("pages", {}).items()):
        out[path] = {"slug": None, "title": page["title"], "description": page["description"],
                     "canonical": SITE + path[:-len("index.html")]}
    room_out, room_errors = expected_rooms(root, data)
    out.update(room_out)
    errors += room_errors
    titles = {}
    for path, v in out.items():
        if len(v["title"]) > TITLE_MAX:
            errors.append("%s: title is %d characters (max %d): %s" % (path, len(v["title"]), TITLE_MAX, v["title"]))
        if len(v["description"]) > DESC_MAX:
            errors.append("%s: description is %d characters (max %d)" % (path, len(v["description"]), DESC_MAX))
        for f in ("title", "description"):
            if BANNED.search(v[f]):
                errors.append("%s: %s says Year 6 or Starter (SR-11)" % (path, f))
        titles.setdefault(v["title"], []).append(path)
    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append("duplicate title %r: %s" % (t, ", ".join(ps)))
    return out, errors


# ---------------------------------------------------------------------------
# Reading and writing a page's head (apply-meta.py uses render())
# ---------------------------------------------------------------------------

def _meta(attr, name):
    return re.compile(r'(<meta\s+%s="%s"\s+content=")([^"]*)("\s*/?>)' % (attr, re.escape(name)), re.I)


TAGS = [  # (field, key in the expected values, pattern, required)
    ("title", "title", re.compile(r"(<title\b[^>]*>)(.*?)(</title>)", re.S | re.I), True),
    ("meta description", "description", _meta("name", "description"), True),
    ("og:title", "title", _meta("property", "og:title"), True),
    ("og:description", "description", _meta("property", "og:description"), True),
    ("twitter:title", "title", _meta("name", "twitter:title"), False),
    ("twitter:description", "description", _meta("name", "twitter:description"), False),
]
LOOSE = {  # any tag of this kind, whatever its shape: a tag the strict pattern misses is an error
    "meta description": re.compile(r'<meta\b[^>]*\bname=["\']description["\']', re.I),
    "og:title": re.compile(r'<meta\b[^>]*\bproperty=["\']og:title["\']', re.I),
    "og:description": re.compile(r'<meta\b[^>]*\bproperty=["\']og:description["\']', re.I),
    "twitter:title": re.compile(r'<meta\b[^>]*\bname=["\']twitter:title["\']', re.I),
    "twitter:description": re.compile(r'<meta\b[^>]*\bname=["\']twitter:description["\']', re.I),
}
CANONICAL = re.compile(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>', re.I)
HREF = re.compile(r'\bhref=["\']([^"\']*)["\']', re.I)


def split_head(text):
    i = text.lower().find("</head>")
    if i < 0:
        raise ValueError("no </head>")
    return text[:i], text[i:]


def _esc(value, attr):
    s = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s.replace('"', "&quot;") if attr else s


def read_head(text):
    """[(field, key, [values])] and [shape errors] for one page's head."""
    head, _ = split_head(text)
    found, errors = [], []
    for field, key, rx, required in TAGS:
        vals = [html.unescape(m.group(2)).strip() for m in rx.finditer(head)]
        loose = LOOSE.get(field)
        if loose and len(loose.findall(head)) != len(vals):
            errors.append("%s tag in a shape this check cannot read" % field)
        if required and len(vals) != 1:
            errors.append("%d %s tags (need exactly 1)" % (len(vals), field))
        elif len(vals) > 1:
            errors.append("%d %s tags (at most 1)" % (len(vals), field))
        found.append((field, key, vals))
    return found, errors


def render(text, values):
    """The page with every head tag set from values; nothing else changes. Raises on a shape it cannot read."""
    _, errors = read_head(text)
    if errors:
        raise ValueError("; ".join(errors))
    head, rest = split_head(text)
    for field, key, rx, _ in TAGS:
        attr = field != "title"
        head = rx.sub(lambda m: m.group(1) + _esc(values[key], attr) + m.group(3), head, count=1)
    return head + rest


def page_errors(text, values):
    found, errors = read_head(text)
    for field, key, vals in found:
        for v in vals:
            if v != values[key]:
                errors.append("%s is %r, games.json gives %r" % (field, v, values[key]))
    head, _ = split_head(text)
    cans = [HREF.search(t).group(1) if HREF.search(t) else None for t in CANONICAL.findall(head)]
    if cans != [values["canonical"]]:
        errors.append("canonical is %s, expected exactly %s" % (cans, values["canonical"]))
    return errors


# ---------------------------------------------------------------------------
# Search keywords on the cards (contract SEARCH-KEYWORDS, Jon, 4 Nov 2026)
# ---------------------------------------------------------------------------
# Each page's cards, by the class every card carries. A game appears in several portal sections: every copy is held.
CARD_PAGES = {"index.html": "game-card", "essentials/index.html": "card"}
KW_MIN, KW_CHARS, KW_SEP = 4, (2, 40), " | "
OPEN_A = re.compile(r"<a\b[^>]*>", re.I)
CLASS = re.compile(r'\bclass="([^"]*)"')
DATA_KW = re.compile(r'\s+data-keywords="([^"]*)"')


def keyword_errors(where, kws):
    if kws is None:
        return ["%s has no keywords" % where]
    if not isinstance(kws, list) or not all(isinstance(k, str) for k in kws):
        return ["%s: keywords must be a list of strings" % where]
    errs, seen = [], set()
    if len(kws) < KW_MIN:
        errs.append("%s has %d keywords (fewer than %d)" % (where, len(kws), KW_MIN))
    for k in kws:
        if k != k.strip():
            errs.append("%s: keyword %r is not trimmed" % (where, k))
        if k != k.lower():
            errs.append("%s: keyword %r is not lower case" % (where, k))
        if not KW_CHARS[0] <= len(k.strip()) <= KW_CHARS[1]:
            errs.append("%s: keyword %r is not %d-%d characters" % (where, k, KW_CHARS[0], KW_CHARS[1]))
        if "|" in k:
            errs.append("%s: keyword %r contains the separator |" % (where, k))
        if k in seen:
            errs.append("%s: duplicate keyword %r" % (where, k))
        seen.add(k)
    return errs


def card_records(data):
    """({link target: data-keywords value}, {every link target games.json has a record for}).
    A game is "games/<slug>/"; a "pages" record is its folder ("the-6-ps/")."""
    kw, known = {}, set()
    for g in data.get("games", []):
        t = "games/%s/" % g.get("slug")
        known.add(t)
        if isinstance(g.get("keywords"), list):
            kw[t] = KW_SEP.join(g["keywords"])
    for path, page in data.get("pages", {}).items():
        t = path[:-len("index.html")]
        known.add(t)
        if isinstance(page.get("keywords"), list):
            kw[t] = KW_SEP.join(page["keywords"])
    return kw, known


def card_target(href):
    """The site path a card links to: no origin, query, fragment or leading slash ("games/split-it/", "the-6-ps/")."""
    h = re.sub(r"^https?://maffsgames\.co\.uk", "", html.unescape(href))
    h = re.sub(r"^(?:\./|/)+", "", re.split(r"[?#]", h)[0])
    if h.endswith("index.html"):
        h = h[:-len("index.html")]
    return h if not h or h.endswith("/") else h + "/"


def cards(text, cls):
    """[(match of the opening tag, href)] for every <a> whose class list holds cls."""
    out = []
    for m in OPEN_A.finditer(text):
        c = CLASS.search(m.group(0))
        if c and cls in c.group(1).split():
            h = HREF.search(m.group(0))
            out.append((m, h.group(1) if h else ""))
    return out


def card_errors(path, text, cls, kw, known):
    found = cards(text, cls)
    errs = []
    n = sum(1 for c in CLASS.findall(text) if cls in c.split())
    if n != len(found):
        errs.append("%s: %d elements have class %s, but %d are <a> cards this check can read" % (path, n, cls, len(found)))
    if not found:
        errs.append("%s: no %s cards found; the page changed shape and this check is blind" % (path, cls))
    for m, href in found:
        t = card_target(href)
        vals = DATA_KW.findall(m.group(0))
        if t not in known:
            errs.append("%s: a card links to %s, which has no games.json record" % (path, href))
        elif t not in kw:
            errs.append("%s: a card links to %s, whose games.json record has no keywords" % (path, href))
        elif not vals:
            errs.append("%s: the card for %s has no data-keywords" % (path, t))
        elif len(vals) > 1:
            errs.append("%s: the card for %s has %d data-keywords" % (path, t, len(vals)))
        elif html.unescape(vals[0]) != kw[t]:
            errs.append("%s: the card for %s: data-keywords differ from games.json" % (path, t))
    return errs


def render_cards(text, cls, kw):
    """The page with data-keywords set on every card from games.json; nothing else changes. Raises when a card links
    to a target with no keywords (a person decides; keywords are never invented)."""
    missing = sorted({href for _, href in cards(text, cls) if card_target(href) not in kw})
    if missing:
        raise ValueError("cards link to %s, with no games.json keywords" % ", ".join(missing))

    def one(m):
        tag = m.group(0)
        c = CLASS.search(tag)
        if not (c and cls in c.group(1).split()):
            return tag
        h = HREF.search(tag)
        tag = DATA_KW.sub("", tag)
        return tag[:-1] + ' data-keywords="%s">' % _esc(kw[card_target(h.group(1) if h else "")], True)
    return OPEN_A.sub(one, text)


def write_cards(root):
    """Set data-keywords on every card page from games.json (apply-meta.py and the self-test). {path: new text}."""
    kw, _ = card_records(load(root))
    out = {}
    for path, cls in CARD_PAGES.items():
        p = root / path
        old = p.read_text(encoding="utf-8")
        new = render_cards(old, cls, kw)
        if new != old:
            out[path] = new
    return out


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------

def check(root):
    """(errors, reports)."""
    exp, errors = expected(root)
    reports = []
    for path, values in sorted(exp.items()):
        p = root / path
        if not p.exists():
            errors.append("%s: no such page" % path)
            continue
        errs = page_errors(p.read_text(encoding="utf-8"), values)
        if values["slug"] in PENDING:
            if errs:
                reports.append("PENDING %s: %s (%d differences)" % (values["slug"], PENDING[values["slug"]], len(errs)))
            else:
                errors.append("%s: PENDING but already matches games.json (stale: remove it from PENDING)" % path)
            continue
        errors += ["%s: %s" % (path, e) for e in errs]
    kw, known = card_records(load(root))
    for path, cls in CARD_PAGES.items():
        p = root / path
        if not p.exists():
            errors.append("%s: no such page" % path)
            continue
        errors += card_errors(path, p.read_text(encoding="utf-8"), cls, kw, known)
    errors += title_assignments(root)
    reports += ["FALLBACK title for %s: %s" % (v["slug"], v["title"]) for v in exp.values() if v.get("fallback")]
    return errors, reports


def apply_all(root):
    """Write every non-PENDING page, and every card page's data-keywords, from games.json (the self-test's copy of apply-meta.py)."""
    exp, errors = expected(root)
    if errors:
        raise ValueError("; ".join(errors))
    for path, values in exp.items():
        if values["slug"] in PENDING:
            continue
        p = root / path
        p.write_text(render(p.read_text(encoding="utf-8"), values), encoding="utf-8", newline='')
    for path, text in write_cards(root).items():
        (root / path).write_text(text, encoding="utf-8", newline='')


def selftest():
    """Copy what the check reads, write every page from games.json, then plant faults."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="check-meta-"))
    try:
        for rel in [ROSTER, DATA] + list(CARD_PAGES):
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(BASE / rel, tmp / rel)
        exp, _ = expected(BASE)
        for path in exp:
            (tmp / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(BASE / path, tmp / path)
        # The room scripts the check reads, the withdrawn room's too (it must stay out).
        rooms_read = [p.relative_to(BASE).as_posix() for p in sorted((BASE / ROOMS_DIR).glob("assets/*.js"))]
        for d in (BASE / ROOMS_DIR).iterdir():
            if (d / "room.js").is_file():
                rooms_read += ["%s/%s/%s" % (ROOMS_DIR, d.name, f) for f in ("room.js", "index.html", "teacher.html")]
        for rel in rooms_read:
            (tmp / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(BASE / rel, tmp / rel)
        pristine = {p: (tmp / p).read_text(encoding="utf-8") for p in list(exp) + [DATA]}
        apply_all(tmp)
        applied = {p: (tmp / p).read_text(encoding="utf-8") for p in set(exp) | set(CARD_PAGES) | set(rooms_read)}
        apply_all(tmp)
        if any((tmp / p).read_text(encoding="utf-8") != t for p, t in applied.items()):
            return ["apply is not idempotent: a second run changed a page"]
        errs, _ = check(tmp)
        if errs:
            return ["baseline after apply is not clean: %s" % errs[:3]]
        # a PENDING page that matches is stale
        pend = next(iter(PENDING), None)

        def edit(path, fn):
            (tmp / path).write_text(fn((tmp / path).read_text(encoding="utf-8")), encoding="utf-8", newline='')

        def data(fn):
            d = json.loads(pristine[DATA])
            fn(d)
            (tmp / DATA).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8", newline='')

        game = "games/split-it/index.html"
        kiln, kiln_js = "escape-rooms/kiln-disaster/index.html", "escape-rooms/kiln-disaster/room.js"
        engine = "escape-rooms/assets/engine.js"

        def room_entry(slug):
            return lambda d: next(r for r in d["rooms"] if r["slug"] == slug)
        kw0_slug = json.loads(pristine[DATA])["games"][0]["slug"]
        faults = [
            ("hand-edited title", lambda: edit(game, lambda t: re.sub(r"<title>.*?</title>", "<title>Split It — MaffsGames</title>", t, 1)),
             "games/split-it/index.html: title is"),
            ("hand-edited og:description", lambda: edit(game, lambda t: t.replace('property="og:description" content="', 'property="og:description" content="X', 1)),
             "og:description is"),
            ("over-length description", lambda: data(lambda d: d["games"][0].update(description="x" * 150)),
             "description is"),
            ("missing slug", lambda: data(lambda d: d["games"].pop()),
             "is missing"),
            ("duplicate title", lambda: data(lambda d: d["games"][1].update(search_phrase=d["games"][0]["search_phrase"])),
             "duplicate title"),
            ("Year 6 in a description", lambda: data(lambda d: d["games"][0].update(description="For Year 6 pupils.")),
             "Year 6 or Starter"),
            ("doubled og:title", lambda: edit(game, lambda t: t.replace("</head>", '<meta property="og:title" content="x">\n</head>', 1)),
             "2 og:title tags"),
            ("canonical changed", lambda: edit(game, lambda t: t.replace("https://maffsgames.co.uk/games/split-it/", "https://maffsgames.co.uk/games/split/", 1)),
             "canonical is"),
            ("PHRASE NEEDED left in", lambda: data(lambda d: d["games"][0].update(search_phrase=PHRASE_NEEDED)),
             "no search_phrase"),
            # search keywords (SEARCH-KEYWORDS): the rules on games.json, then the cards
            ("a game with no keywords", lambda: data(lambda d: d["games"][0].pop("keywords")),
             "%s has no keywords" % kw0_slug),
            ("three keywords", lambda: data(lambda d: d["games"][0].update(keywords=d["games"][0]["keywords"][:3])),
             "fewer than 4"),
            ("an upper-case keyword", lambda: data(lambda d: d["games"][0].update(keywords=["Ratio"] + d["games"][0]["keywords"])),
             "is not lower case"),
            ("an untrimmed keyword", lambda: data(lambda d: d["games"][0].update(keywords=["ratio "] + d["games"][0]["keywords"])),
             "is not trimmed"),
            ("a keyword twice", lambda: data(lambda d: d["games"][0]["keywords"].append(d["games"][0]["keywords"][0])),
             "duplicate keyword"),
            ("a one-character keyword", lambda: data(lambda d: d["games"][0]["keywords"].append("x")),
             "is not 2-40 characters"),
            ("a 41-character keyword", lambda: data(lambda d: d["games"][0]["keywords"].append("x" * 41)),
             "is not 2-40 characters"),
            ("a card's data-keywords edited", lambda: edit("index.html", lambda t: t.replace('data-keywords="', 'data-keywords="x ', 1)),
             "data-keywords differ from games.json"),
            ("a card with no data-keywords", lambda: edit("essentials/index.html", lambda t: DATA_KW.sub("", t, count=1)),
             "has no data-keywords"),
            ("a card linking to a slug with no record", lambda: edit("index.html", lambda t: t.replace('href="games/split-it/', 'href="games/no-such-game/', 1)),
             "games/no-such-game/?level=ks3, which has no games.json record"),
            ("a page record a card links to, without keywords", lambda: data(lambda d: d["pages"]["the-6-ps/index.html"].pop("keywords")),
             "the-6-ps/, whose games.json record has no keywords"),
            # escape rooms (ROOM-SEARCH-TITLES)
            ("a hand-edited room title", lambda: edit(kiln, lambda t: re.sub(r"<title>.*?</title>", "<title>The Kiln Disaster — MaffsGames</title>", t, 1)),
             "escape-rooms/kiln-disaster/index.html: title is"),
            ("a hand-edited room twitter:description", lambda: edit(kiln, lambda t: t.replace('name="twitter:description" content="', 'name="twitter:description" content="X', 1)),
             "twitter:description is"),
            ("a hand-edited hub title", lambda: edit("escape-rooms/index.html", lambda t: re.sub(r"<title>.*?</title>", "<title>Maths Escape Rooms — MaffsGames</title>", t, 1)),
             "escape-rooms/index.html: title is"),
            ("a live room missing from games.json", lambda: data(lambda d: d["rooms"].remove(room_entry("kiln-disaster")(d))),
             "live room kiln-disaster has no entry"),
            ("the withdrawn room given an entry", lambda: data(lambda d: d["rooms"].append({"slug": "it-vengeance", "search_phrase": "x", "level": "GCSE"})),
             "room it-vengeance is not a live room"),
            ("a room listed twice", lambda: data(lambda d: d["rooms"].append(dict(room_entry("kiln-disaster")(d)))),
             "room kiln-disaster listed 2 times"),
            ("a description over 155 with no short_topics", lambda: data(lambda d: room_entry("rightful-king")(d).pop("short_topics")),
             "rightful-king: description is"),
            ("short_topics still over 155", lambda: data(lambda d: room_entry("rightful-king")(d).update(short_topics="x" * 150)),
             "still over 155"),
            ("a clock differing from room.js", lambda: edit(kiln_js, lambda t: re.sub(r"(?m)^(\s*minutes:\s*)\d+", r"\g<1>16", t, 1)),
             "escape-rooms/kiln-disaster/index.html: meta description is"),
            ("a timer that cannot be read", lambda: edit(kiln_js, lambda t: re.sub(r"(?m)^\s*minutes:\s*\d+,?\n", "", t, 1)),
             "kiln-disaster: the room's timer cannot be read"),
            ("no lockMeta topics", lambda: edit("escape-rooms/kiln-disaster/teacher.html", lambda t: t.replace('"lockMeta"', '"lockmeta"', 1)),
             "kiln-disaster: no lockMeta topics"),
            ("the engine assigns document.title", lambda: edit(engine, lambda t: t + "\ndocument.title = R.title;\n"),
             "escape-rooms/assets/engine.js assigns document.title"),
            ("a room script assigns document.title", lambda: edit(kiln_js, lambda t: t + "\ndocument['title'] = 'x';\n"),
             "escape-rooms/kiln-disaster/room.js assigns document.title"),
        ]
        if pend:
            faults.append(("stale PENDING entry", lambda: (tmp / ("games/%s/index.html" % pend)).write_text(
                render(applied["games/%s/index.html" % pend], exp["games/%s/index.html" % pend]), encoding="utf-8", newline=''),
                "PENDING but already matches"))
        failures = []
        for name, plant, needle in faults:
            for p, t in applied.items():
                (tmp / p).write_text(t, encoding="utf-8", newline='')
            (tmp / DATA).write_text(pristine[DATA], encoding="utf-8", newline='')
            plant()
            errs, _ = check(tmp)
            if not any(needle in e for e in errs):
                failures.append("planted fault not caught: %s (got %s)" % (name, errs[:2]))
        # The over-60 fallback is reported, never silent.
        for p, t in applied.items():
            (tmp / p).write_text(t, encoding="utf-8", newline='')
        data(lambda d: next(r for r in d["rooms"] if r["slug"] == "kiln-disaster").update(search_phrase="Multiples and Common Factors"))
        apply_all(tmp)
        if not any(r.startswith("FALLBACK title for escape-rooms/kiln-disaster") for r in check(tmp)[1]):
            failures.append("a title over 60 did not report its fallback")
        if topics_lower("Sets and Venn diagrams, LCM (Lower bound)") != "sets and Venn diagrams, LCM (lower bound)":
            failures.append("topics_lower: %r" % topics_lower("Sets and Venn diagrams, LCM (Lower bound)"))
        print("self-test: %d of %d planted faults caught" % (len(faults) - len(failures), len(faults)))
        return failures
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def table(root):
    exp, errors = expected(root)
    cell = lambda s: s.replace("|", "\\|")
    lines = ["| Page | Current title | New title | Chars | New description | Chars |", "|---|---|---|---|---|---|"]
    for path, v in sorted(exp.items(), key=lambda kv: (kv[1]["slug"] is not None, list(exp).index(kv[0]))):
        cur = re.search(r"<title\b[^>]*>(.*?)</title>", (root / path).read_text(encoding="utf-8"), re.S | re.I)
        cur = html.unescape(cur.group(1)).strip() if cur else "—"
        name = "`%s`" % (v["slug"] or "/" + path[:-len("index.html")])
        if v["slug"] in PENDING:
            name += " (PENDING)"
        if v.get("fallback"):
            name += " (fallback title)"
        if v.get("short"):
            name += " (short_topics)"
        lines.append("| %s | %s | %s | %d | %s | %d |" % (name, cell(cur), cell(v["title"]), len(v["title"]),
                                                       cell(v["description"]), len(v["description"])))
    return "\n".join(lines), errors


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--table", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    if a.table:
        t, errors = table(root)
        print(t)
        return 1 if errors else 0
    if a.selftest:
        failures = selftest()
        for f in failures:
            print("SELF-TEST FAIL: " + f)
        return 1 if failures else 0
    errors, reports = check(root)
    for r in reports:
        print(r)
    for e in errors:
        print("FAIL: " + e)
    n, nr, np = len(expected(root)[0]), len(load(root).get("rooms", [])), len(load(root).get("pages", {}))
    print("%s: %d pages (%d games + %d rooms + %d other), %d PENDING" % (
        "FAILED" if errors else "OK", n, n - nr - np, nr, np, len(PENDING)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
