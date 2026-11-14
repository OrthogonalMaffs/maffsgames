#!/usr/bin/env python3
# ci-line: Ugh, stats pages (the four /ugh-stats/ pages in Chromium: live figures match the repo's two JSON files; a missing, stale or misshapen file shows "Figures unavailable right now" and no number; "<10" drawn as a bar of 5, labelled, never summed; Case 1's live box against a hand-worked file; its 12 November figures unchanged; no sideways scroll at 375 px; nothing loaded from outside the site but Google Fonts; three planted faults caught) | --selftest && --check
# ci-deps: ugh-stats/ schools/assets/ugh-stats.js schools/assets/answer-counts.json schools/assets/ugh-stats.json
"""Do the "Ugh, stats" pages show the figures the site's own files hold, and nothing when they cannot? (contract
UGH-STATS-PAGES, 14 Nov 2026)

    python scripts/check-ugh-stats.py --check                 # the four pages, in Chromium, on the repo's files and on plants
    python scripts/check-ugh-stats.py --selftest              # three planted faults must each be caught
    python scripts/check-ugh-stats.py --screens docs/screens/ugh-stats   # also save a phone screenshot of each page

A figure on a page is a claim. The four pages (/ugh-stats/, half-our-games/, charts/, whos-playing/) draw every live
figure from two committed files through one loader, schools/assets/ugh-stats.js. This holds them to it:

  REAL     with the repo's own answer-counts.json and ugh-stats.json, each live figure equals the one this script works
           out from the same file by its own code (a file that is absent or over 7 days old must show no figure).
  ABSENT   with each file missing (404), with its as_of 8 days old, and with its shape wrong, every mount that reads it
           shows exactly "Figures unavailable right now" (no digit), and its download button stays hidden.
  SMALL    a planted ugh-stats.json with "<10" entries: each is a bar the height of 5 with the label "<10", reads "<10"
           in the table and in the CSV, and is never added in: the UK's share is given as "at least", worked with the
           hidden entry at its most (9), never as an exact figure.
  CASE 1   a planted answer-counts.json of 13 games (HAND below) gives the hand-worked figures; the CSV lists every
           slug, most answers first.
  FROZEN   Case 1's 12 November figures and sentences are exactly the contract's (Jon's decision record).
  FIT      no page scrolls sideways at 375 px, in any of the states above.
  OUTSIDE  no page requests any URL off the site except Google Fonts (served here from the pinned copies).

HAND, the planted file: answers 500, 200, 100, 60, 40, 30, 20, 16, 12, 10, 6, 4, 2 (13 games, total 1,000) and two
games with 0, which are not counted. Ten groups by position, boundaries at floor(13 i / 10) = 0, 1, 2, 3, 5, 6, 7, 9,
10, 11, 13: shares 50.0, 20.0, 10.0, 10.0 (60 + 40), 3.0, 2.0, 2.8 (16 + 12), 1.0, 0.6, 0.6 (4 + 2) per cent. Top
tenth 50.0%. Bottom half (the last five groups: 20, 16, 12, 10, 6, 4, 2 = 70) 7.0%. Mean 1000 / 13 = 76.9, shown 77.
Median, the 7th of 13, 20. Quartiles at positions 14 / 4 = 3.5 and 10.5 from the smallest (2, 4, 6, 10, 12, 16, 20,
30, 40, 60, 100, 200, 500): halfway from 6 to 10 = 8, and halfway from 60 to 100 = 80. At or above the mean: 100,
200, 500 = 3 of 13.

Everything is served by serve-stubbed.py; nothing is sent anywhere.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import zoneinfo

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

ROOT = bc.ROOT
UNAVAILABLE = "Figures unavailable right now"
HIDDEN = "<10"
STALE = dt.timedelta(days=7)
COUNTS = "/schools/assets/answer-counts.json"
STATS = "/schools/assets/ugh-stats.json"
LOADER = "/schools/assets/ugh-stats.js"
PAGES = {"landing": "ugh-stats/index.html", "case1": "ugh-stats/half-our-games/index.html",
         "charts": "ugh-stats/charts/index.html", "case2": "ugh-stats/whos-playing/index.html"}
READS = {"landing": ("counts",), "case1": ("counts",), "charts": ("stats",), "case2": ("stats",)}
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
LEVELS = {"year6": "Year 6", "ks3": "KS3", "gcse": "GCSE", "higher": "GCSE Higher", "core": "Core Maths", "alevel": "A level",
          "further": "Further Maths", "level3": "Level 3", "level4": "Level 4", "all": "All levels", "none": "No level", "other": "Other"}

# Case 1's decision record, exactly as the contract gives it.
FROZEN_TOP = [("Six Sevens, Bruv", "4,181"), ("Like Terms Collector", "2,475"), ("Prime or Composite", "1,930"),
              ("Factor Race", "1,882"), ("The Kiln Disaster (room)", "775"), ("Negative Number Line", "729")]
FROZEN_DECILES = [("Top tenth", "59.9%"), ("2nd", "18.9%"), ("3rd", "9.2%"), ("4th", "5.1%"), ("5th", "3.1%"),
                  ("6th", "1.7%"), ("7th", "1.1%"), ("8th", "0.6%"), ("9th", "0.3%"), ("Bottom", "0.1%")]
FROZEN_STATS = [("Mean answers per game", "219"), ("Median", "52"), ("Interquartile range", "13 to 192")]
FROZEN_TEXT = [
    "When we decided (12 November 2026)",
    "We had time for one big job before Christmas: build new games, or help people find the 116 we've already got. "
    "Which one would get more students answering questions?",
    "Every game counts the answers given in it. From 1 September to 12 November: 25,438 answers across 116 games and rooms.",
    "… and 110 more. The bottom 58 have 987 answers between them.",
    "Line all 116 up from most played to least, cut the queue into ten equal groups, and see what share of the answers each group gets.",
    "The top tenth of games (11 of them) get 59.9% of all answers. The bottom half get 3.9%.",
    'Which average tells the truth about a "typical" game? A handful of huge games drag the mean up to 219, but only 28 of '
    "the 116 games actually reach it. The median, 52, is what most games really look like. When data is this lopsided, the "
    "mean tells you about the giants, not the typical game.",
]


# ------------------------------------------------------------------------------------------------ the figures, worked here
def fmt(n):
    return "{:,}".format(int(round(n)))


def show(v):
    return HIDDEN if v == HIDDEN else fmt(v)


def as_of_time(obj):
    try:
        t = dt.datetime.fromisoformat(str(obj["as_of"]).replace("Z", "+00:00"))
        return t if t.tzinfo else None
    except Exception:
        return None


def usable(obj, now=None):
    """The loader's rule: a dict with an as_of no more than 7 days old."""
    t = as_of_time(obj) if isinstance(obj, dict) else None
    return bool(t) and (now or dt.datetime.now(dt.timezone.utc)) - t <= STALE


def as_of_date(obj):
    d = as_of_time(obj).astimezone(zoneinfo.ZoneInfo("Europe/London"))
    return "%d %s %d" % (d.day, MONTHS[d.month - 1], d.year)


def d_mon(date):
    return "%d %s" % (int(date[8:10]), MONTHS[int(date[5:7]) - 1])


def case1(games):
    """Case 1's method, worked independently of the page (see HAND in the docstring)."""
    v = sorted((x for x in games.values() if x >= 1), reverse=True)
    n, total = len(v), sum(v)
    b = [n * i // 10 for i in range(11)]
    asc = v[::-1]

    def at(pos):
        lo = int(pos)
        frac = pos - lo
        a, c = asc[min(max(lo, 1), n) - 1], asc[min(max(lo + 1, 1), n) - 1]
        return a + (c - a) * frac
    mean = total / n
    median = asc[n // 2] if n % 2 else (asc[n // 2 - 1] + asc[n // 2]) / 2
    return {
        "Answers": fmt(total), "Games and rooms": fmt(n),
        "Top tenth's share of answers": "%.1f%%" % (100 * sum(v[:b[1]]) / total),
        "Bottom half's share of answers": "%.1f%%" % (100 * sum(v[b[5]:]) / total),
        "Mean answers per game": fmt(mean),
        "Median": ("%.1f" % median) if median % 1 else fmt(median),
        "Interquartile range": "%s to %s" % (fmt(at((n + 1) / 4)), fmt(at(3 * (n + 1) / 4))),
        "Games at or above the mean": "%s of %s" % (fmt(sum(1 for x in v if x >= mean)), fmt(n)),
    }


def uk_share(countries):
    """The sentence's figure: exact when every entry is a number; otherwise the least it can be (hidden entries at 9)."""
    uk = [c["sessions"] for c in countries if c["country"] == "United Kingdom"]
    if not uk or uk[0] == HIDDEN or not uk[0]:
        return None
    nums = [c["sessions"] for c in countries if c["sessions"] != HIDDEN]
    hid = len(countries) - len(nums)
    if not hid:
        return "%.1f%%" % (100 * uk[0] / sum(nums))
    return "at least %.1f%%" % ((1000 * uk[0] // (sum(nums) + 9 * hid)) / 10)


# ------------------------------------------------------------------------------------------------ plants
def now_iso(days_old=0):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_old)).strftime("%Y-%m-%dT%H:%M:%SZ")


HAND_GAMES = {"g%02d" % i: v for i, v in enumerate([500, 200, 100, 60, 40, 30, 20, 16, 12, 10, 6, 4, 2])}
HAND_GAMES.update({"quiet-one": 0, "quiet-two": 0})
HAND = {"Answers": "1,000", "Games and rooms": "13", "Top tenth's share of answers": "50.0%",
        "Bottom half's share of answers": "7.0%", "Mean answers per game": "77", "Median": "20",
        "Interquartile range": "8 to 80", "Games at or above the mean": "3 of 13"}


def planted_counts(days_old=0, since="2026-09-01"):
    return {"as_of": now_iso(days_old), "since": since, "total": 1000, "games": dict(HAND_GAMES)}


def planted_stats(days_old=0, small=True):
    """30 days ending yesterday. With small=True: one day, one level, three hours and "Other countries" are "<10"."""
    end = dt.date.today() - dt.timedelta(days=1)
    days = [end - dt.timedelta(days=29 - i) for i in range(30)]
    daily = [{"date": d.isoformat(), "starts": 20 if d.weekday() >= 5 else 100 + 10 * (i % 4)} for i, d in enumerate(days)]
    daily[3]["starts"] = HIDDEN if small else 12
    daily[4]["starts"] = 50
    daily[5]["starts"] = 0
    weekday = [0, 0, 0, 0, 0, 0, 10, 40, 90, 200, 260, 240, 150, 180, 220, 160, 90, 70, 60, 50, 40, 30, 12, 0]
    weekend = [0, 0, 0, 0, 0, 0, 0, 0, 10, 20, 30, 40, 40, 30, 30, 20, 20, 30, 40, 30, 20, 10, 0, 0]
    if small:
        weekday[5], weekday[23], weekend[7] = HIDDEN, HIDDEN, HIDDEN
    return {
        "as_of": now_iso(days_old), "daily": daily,
        "levels": [{"level": "gcse", "starts": 300}, {"level": "ks3", "starts": 120}, {"level": "none", "starts": 50},
                   {"level": "homebrew", "starts": 14}, {"level": "further", "starts": HIDDEN if small else 10}],
        "hours": {"weekday": weekday, "weekend": weekend},
        "countries": [{"country": "United Kingdom", "sessions": 900}, {"country": "France", "sessions": 60 if small else 100}]
                     + ([{"country": "Other countries", "sessions": HIDDEN}] if small else []),
    }


def misshapen_stats():
    s = planted_stats()
    s["hours"]["weekday"] = s["hours"]["weekday"][:23]
    return s


def misshapen_counts():
    c = planted_counts()
    c["games"]["g00"] = "500"
    return c


def repo_json(path):
    try:
        with open(os.path.join(ROOT, path.lstrip("/")), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def repo_text(path):
    with open(os.path.join(ROOT, path.lstrip("/")), encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------------------------------------------ the browser
PROBE = r"""() => {
  const norm = s => (s || '').replace(/\s+/g, ' ').trim();
  const rects = root => [...root.querySelectorAll('rect')].map(r => ({ v: r.getAttribute('data-value'),
    h: parseFloat(r.getAttribute('height')), w: parseFloat(r.getAttribute('width')) }));
  const tables = root => [...root.querySelectorAll('table')].map(t => [...t.querySelectorAll('tbody tr')].map(
    tr => [...tr.children].map(c => norm(c.textContent))));
  const pairs = root => { const o = {}; root.querySelectorAll('dt').forEach(dt => { o[norm(dt.textContent)] = norm(dt.nextElementSibling.textContent); }); return o; };
  const part = el => el ? { text: norm(el.innerText), rects: rects(el), tables: tables(el), pairs: pairs(el),
    labels: el.querySelectorAll('text[data-hidden-label]').length, charts: [...el.querySelectorAll('.ugh-chart')].map(rects) } : null;
  const mounts = {};
  document.querySelectorAll('[data-ugh-live]').forEach(m => {
    mounts[m.id] = Object.assign(part(m), { source: m.getAttribute('data-ugh-live'), state: m.getAttribute('data-ugh-state') });
  });
  const needs = {};
  document.querySelectorAll('[data-ugh-needs]').forEach(n => { needs[n.id] = n.hidden; });
  const de = document.documentElement;
  return { mounts, needs, text: norm(document.body.innerText), scrollW: Math.max(de.scrollWidth, document.body.scrollWidth),
    clientW: de.clientWidth, decided: part(document.getElementById('decided')),
    topSix: part(document.getElementById('topSixChart')), deciles: part(document.getElementById('decilesChart')) };
}"""


class Site:
    """The four pages behind a guard: plants replace a path's response; anything off the site but a pinned font is refused."""

    def __init__(self, width=375, height=667):
        from playwright.sync_api import sync_playwright
        self.proc, self.base = bc.start_stub_server()
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch()
        self.ctx = self.browser.new_context(viewport={"width": width, "height": height}, accept_downloads=True)

    def close(self):
        try:
            self.browser.close()
            self.pw.stop()
        finally:
            self.proc.terminate()

    def open(self, rel, plants):
        """plants: {path: None (404) | dict (JSON) | str (the body)} -> (page, rec)."""
        page = self.ctx.new_page()
        rec = {"outside": [], "errs": []}
        page.on("pageerror", lambda e: rec["errs"].append(str(e).splitlines()[0][:200]))

        def handle(route):
            url = route.request.url
            if url.startswith(("data:", "blob:")):
                return route.continue_()
            if not url.startswith(self.base + "/"):
                got = bc.real_font_response(url) if bc.is_font_cdn(url) and "fonts.g" in url else None
                if not got:
                    rec["outside"].append(url)
                    return route.abort()
                return route.fulfill(**got)
            path = urllib.parse.urlsplit(url).path
            if path in plants:
                body = plants[path]
                if body is None:
                    return route.fulfill(status=404, content_type="text/plain", body="not found")
                if isinstance(body, dict):
                    return route.fulfill(status=200, content_type="application/json", body=json.dumps(body))
                kind = "text/html; charset=utf-8" if path.endswith((".html", "/")) else "application/javascript; charset=utf-8"
                return route.fulfill(status=200, content_type=kind, body=body)
            return route.continue_()
        page.route("**/*", handle)
        page.goto("%s/%s" % (self.base, rel), wait_until="domcontentloaded", timeout=30000)
        page.wait_for_function("document.documentElement.getAttribute('data-ugh-ready') === '1'", timeout=30000)
        page.evaluate("document.fonts.ready.then(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))))")
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        page.wait_for_timeout(250)
        return page, rec

    def look(self, key, plants, also=None):
        """One page under `plants` -> (probe, rec, extra): extra is also(page) when given."""
        page, rec = self.open(PAGES[key], plants)
        try:
            got = page.evaluate(PROBE)
            extra = also(page) if also else None
        finally:
            page.close()
        return got, rec, extra


def csv_of(page):
    if page.evaluate("document.getElementById('csv').hidden"):
        return None
    with page.expect_download(timeout=15000) as dl:
        page.click("#csv")
    with open(dl.value.path(), encoding="utf-8") as f:
        return [line.split(",") for line in f.read().strip().splitlines()]


# ------------------------------------------------------------------------------------------------ the checks
def common(name, got, rec, faults):
    if rec["errs"]:
        faults.append("%s: a script error: %s" % (name, rec["errs"][0]))
    if rec["outside"]:
        faults.append("%s: OUTSIDE, the page asked for %s" % (name, rec["outside"][0][:120]))
    if got["scrollW"] > got["clientW"]:
        faults.append("%s: FIT, the page is %d px wide in a %d px window (sideways scroll)" % (name, got["scrollW"], got["clientW"]))


def expect_unavailable(name, got, source, faults):
    seen = 0
    for mid, m in got["mounts"].items():
        if m["source"] != source:
            continue
        seen += 1
        if m["text"] != UNAVAILABLE or m["state"] != "unavailable" or m["rects"]:
            faults.append('%s: ABSENT, #%s shows %r, want exactly "%s"' % (name, mid, m["text"][:80], UNAVAILABLE))
    if not seen:
        faults.append("%s: no mount reads %s" % (name, source))
    for nid, hid in got["needs"].items():
        if not hid:
            faults.append("%s: ABSENT, #%s is offered although its figures are unavailable" % (name, nid))


def expect_text(name, mount, wanted, faults, tag):
    for w in wanted:
        if w not in mount["text"]:
            faults.append("%s: %s, want %r in %r" % (name, tag, w, mount["text"][:160]))


def expect_counts(name, key, got, counts, faults, tag, extra=None):
    """A page that reads answer-counts.json, against `counts` (usable)."""
    if key == "landing":
        n = sum(1 for v in counts["games"].values() if v >= 1)
        m = got["mounts"]["answers"]
        want = "%s Across %s games and rooms. Updated daily; last %s." % (fmt(counts["total"]), fmt(n), as_of_date(counts))
        if m["text"] != want or m["state"] != "live":
            faults.append("%s: %s, the live box reads %r, want %r" % (name, tag, m["text"][:160], want))
    else:
        m = got["mounts"]["today"]
        want = case1(counts["games"])
        if m["pairs"] != want:
            diff = ["%s %r (want %r)" % (k, m["pairs"].get(k), v) for k, v in want.items() if m["pairs"].get(k) != v]
            faults.append("%s: %s, the Today box differs: %s" % (name, tag, "; ".join(diff) or "extra figures %r" % m["pairs"]))
        expect_text(name, m, ["Figures from " + as_of_date(counts)], faults, tag)
        if extra is not None:
            rows = sorted(counts["games"].items(), key=lambda kv: (-kv[1], kv[0]))
            want_csv = [["slug", "answers"]] + [[k, str(v)] for k, v in rows]
            if extra != want_csv:
                faults.append("%s: %s, the CSV is not slug, answers for every slug, most answers first (%d rows, first %r)"
                              % (name, tag, len(extra or []), (extra or [None, None])[1]))


def bar_check(name, what, rects, values, faults):
    """One chart's bars against the file's counts: one bar each, in order; a "<10" as tall (or long) as 5."""
    if [r["v"] for r in rects] != [str(v) for v in values]:
        faults.append("%s: %s has bars %r, want %r" % (name, what, [r["v"] for r in rects][:8], [str(v) for v in values][:8]))
        return
    size = "w" if what.startswith("Level") else "h"
    ref = [(r[size], v) for r, v in zip(rects, values) if v != HIDDEN and v >= 20]
    if not ref:
        return
    unit = ref[0][0] / ref[0][1]
    for r, v in zip(rects, values):
        want = unit * (5 if v == HIDDEN else v)
        if abs(r[size] - want) > max(1.2, 0.03 * want):
            faults.append("%s: %s, the bar for %r is %.1f px, want %.1f (a \"<10\" is drawn as 5)" % (name, what, v, r[size], want))
            return


def expect_stats(name, key, got, stats, faults, tag, extra=None):
    """A page that reads ugh-stats.json, against `stats` (usable)."""
    days = [r["starts"] for r in stats["daily"]]
    d = got["mounts"]["daily"]
    bar_check(name, "Daily Activity", d["rects"], days, faults)
    if d["labels"] != days.count(HIDDEN):
        faults.append('%s: SMALL, the daily chart has %d "<10" labels for %d hidden days' % (name, d["labels"], days.count(HIDDEN)))
    rows = [[d_mon(r["date"]) + (" (weekend)" if dt.date.fromisoformat(r["date"]).weekday() >= 5 else ""), show(r["starts"])]
            for r in stats["daily"]]
    if d["tables"] != [rows]:
        faults.append("%s: %s, the daily table is not the file's 30 days" % (name, tag))
    if key == "charts":
        lv = got["mounts"]["levels"]
        bar_check(name, "Level Split", lv["rects"], [r["starts"] for r in stats["levels"]], faults)
        rows = [[LEVELS.get(r["level"], r["level"]), show(r["starts"])] for r in stats["levels"]]
        if lv["tables"] != [rows]:
            faults.append("%s: %s, the level table reads %r, want %r" % (name, tag, lv["tables"], rows))
        up = got["mounts"]["updated"]
        if up["text"] != "Updated daily; last %s." % as_of_date(stats):
            faults.append("%s: %s, the updated line reads %r" % (name, tag, up["text"]))
    else:
        h = got["mounts"]["hours"]
        wd, we = stats["hours"]["weekday"], stats["hours"]["weekend"]
        if len(h["charts"]) != 2:
            faults.append("%s: the hours chart has %d panels, want 2" % (name, len(h["charts"])))
        else:
            bar_check(name, "Hours (weekday)", h["charts"][0], wd, faults)
            bar_check(name, "Hours (weekend)", h["charts"][1], we, faults)
            both = [(r["h"], v) for r, v in zip(h["charts"][0] + h["charts"][1], wd + we) if v != HIDDEN and v >= 20]
            if len(both) > 1 and any(abs(a / v - both[0][0] / both[0][1]) > 0.03 * both[0][0] / both[0][1] + 0.02 for a, v in both):
                faults.append("%s: the weekday and weekend panels are not on one scale" % name)
        if h["labels"] != (wd + we).count(HIDDEN):
            faults.append('%s: SMALL, the hours chart has %d "<10" labels for %d hidden hours' % (name, h["labels"], (wd + we).count(HIDDEN)))
        rows = [["%d:00" % i, show(wd[i]), show(we[i])] for i in range(24)]
        if h["tables"] != [rows]:
            faults.append("%s: %s, the hours table is not the file's 24 hours" % (name, tag))
        share = uk_share(stats["countries"])
        uk = got["mounts"]["uk"]
        want = "Share of sessions from the UK, last 4 weeks: %s" % share
        if share is None:
            faults.append("%s: the file has no UK figure to check against" % name)
        elif uk["text"] != want:
            faults.append("%s: %s, the UK line reads %r, want %r (a \"<10\" is never added in)" % (name, tag, uk["text"], want))
        if extra is not None:
            want_csv = [["hour", "weekday", "weekend"]] + [[str(i), str(wd[i]), str(we[i])] for i in range(24)]
            if extra != want_csv:
                faults.append("%s: %s, the CSV is not hour, weekday, weekend for 24 hours with \"<10\" kept" % (name, tag))


def expect_frozen(got, faults):
    d = got["decided"]
    if not d:
        faults.append("case1: FROZEN, no #decided block")
        return
    for s in FROZEN_TEXT:
        if s not in d["text"]:
            faults.append("case1: FROZEN, the 12 November record no longer reads: %r" % s[:90])
    want_tables = [[list(r) for r in FROZEN_TOP], [list(r) for r in FROZEN_DECILES]]
    if d["tables"] != want_tables:
        faults.append("case1: FROZEN, the two tables differ from the contract's figures: %r" % (d["tables"],))
    if d["pairs"] != dict(FROZEN_STATS):
        faults.append("case1: FROZEN, the three figures read %r, want %r" % (d["pairs"], dict(FROZEN_STATS)))
    for part, rows in (("topSix", FROZEN_TOP), ("deciles", FROZEN_DECILES)):
        want = [str(float(v.replace(",", "").rstrip("%"))) for _, v in rows]
        have = [str(float(r["v"])) for r in (got[part] or {"rects": []})["rects"]]
        if have != want:
            faults.append("case1: FROZEN, the %s chart draws %r, want %r" % (part, have, want))


def examine(site, base_plants=None, only=None):
    """Every check -> faults. base_plants (the selftest's faults) are applied under each case's own plants."""
    base_plants = base_plants or {}
    faults = []

    def look(key, plants, also=None):
        p = dict(base_plants)
        p.update(plants)
        return site.look(key, p, also)
    want = lambda group: only is None or group in only

    counts, stats = repo_json(COUNTS), repo_json(STATS)
    if want("REAL"):
        for key in PAGES:
            got, rec, extra = look(key, {}, csv_of if key in ("case1", "case2") else None)
            name = "%s (the repo's files)" % key
            common(name, got, rec, faults)
            if "counts" in READS[key]:
                if usable(counts):
                    expect_counts(name, key, got, counts, faults, "REAL", extra)
                else:
                    expect_unavailable(name, got, "counts", faults)
            else:
                if usable(stats):
                    expect_stats(name, key, got, stats, faults, "REAL", extra)
                else:
                    expect_unavailable(name, got, "stats", faults)
            if key == "case1":
                expect_frozen(got, faults)
    if want("ABSENT"):
        cases = [("the file missing", {COUNTS: None, STATS: None}),
                 ("as_of 8 days old", {COUNTS: planted_counts(8), STATS: planted_stats(8)}),
                 ("the wrong shape", {COUNTS: misshapen_counts(), STATS: misshapen_stats()})]
        for label, plants in cases:
            for key in PAGES:
                got, rec, _ = look(key, plants)
                name = "%s (%s)" % (key, label)
                common(name, got, rec, faults)
                expect_unavailable(name, got, READS[key][0], faults)
        got, rec, _ = look("landing", {COUNTS: planted_counts(since="2026-10-01")})
        expect_unavailable("landing (counted from another day)", got, "counts", faults)
    if want("CASE1"):
        plants = {COUNTS: planted_counts()}
        got, rec, extra = look("case1", plants, csv_of)
        common("case1 (the hand-worked file)", got, rec, faults)
        assert case1(HAND_GAMES) == HAND, "this script's own method disagrees with the hand working"
        if got["mounts"]["today"]["pairs"] != HAND:
            faults.append("case1: CASE 1, the Today box on the hand-worked file reads %r, want %r" % (got["mounts"]["today"]["pairs"], HAND))
        expect_counts("case1 (the hand-worked file)", "case1", got, planted_counts(), faults, "CASE 1", extra)
        got, rec, _ = look("landing", plants)
        common("landing (the hand-worked file)", got, rec, faults)
        expect_counts("landing (the hand-worked file)", "landing", got, planted_counts(), faults, "CASE 1")
    if want("SMALL"):
        for small in (True, False):
            st = planted_stats(small=small)
            for key in ("charts", "case2"):
                got, rec, extra = look(key, {STATS: st}, csv_of if key == "case2" else None)
                name = "%s (planted figures%s)" % (key, ', some "<10"' if small else "")
                common(name, got, rec, faults)
                expect_stats(name, key, got, st, faults, "SMALL", extra)
        assert uk_share(planted_stats()["countries"]) == "at least 92.8%"       # 900 / (900 + 60 + 9) = 92.87...
        assert uk_share(planted_stats(small=False)["countries"]) == "90.0%"      # 900 / 1000
    return faults


# ------------------------------------------------------------------------------------------------ self-test
def selftest():
    loader = repo_text(LOADER)
    case1_html = repo_text(PAGES["case1"])

    def swap(text, old, new):
        assert text.count(old) == 1, "the selftest's plant no longer finds %r" % old
        return text.replace(old, new)
    plants = [
        ("a stale file shown as a number", {LOADER: swap(loader, "var STALE_MS = 7 * 24 * 3600 * 1000;", "var STALE_MS = 70 * 24 * 3600 * 1000;")},
         ("ABSENT",), "ABSENT"),
        ('"<10" summed', {LOADER: swap(loader, "if (hidden(v)) hid += 1; else sum += v;", "sum += drawn(v);")}, ("SMALL",), "never added in"),
        ("a frozen figure changed", {"/" + PAGES["case1"]: swap(case1_html, "<td>4,181</td>", "<td>4,182</td>")}, ("REAL",), "FROZEN"),
    ]
    bad = []
    site = Site()
    try:
        for name, p, groups, word in plants:
            faults = examine(site, p, only=groups)
            hit = [f for f in faults if word in f]
            ok = bool(hit)
            print("  %s  plant: %-32s %s" % ("ok  " if ok else "FAIL", name, (hit or faults or ["passed, but must fail"])[0][:150]))
            if not ok:
                bad.append(name)
    finally:
        site.close()
    print("selftest: %s (%d plants)" % ("FAILED: " + "; ".join(bad) if bad else "PASS", len(plants)))
    return 1 if bad else 0


def screens(folder, stats_file=None):
    """A phone screenshot (375 px wide, full page) of each page on the repo's files."""
    os.makedirs(folder, exist_ok=True)
    plants = {STATS: json.load(open(stats_file, encoding="utf-8"))} if stats_file else {}
    site = Site()
    try:
        for key, rel in PAGES.items():
            page, _ = site.open(rel, plants)
            out = os.path.join(folder, "%s-375.png" % (rel.split("/")[-2] if rel.count("/") > 1 else "landing"))
            page.set_viewport_size({"width": 375, "height": page.evaluate("document.documentElement.scrollHeight")})
            page.wait_for_timeout(200)
            page.screenshot(path=out)
            page.close()
            print("saved", os.path.relpath(out, ROOT))
    finally:
        site.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="the four pages (the default)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--screens", metavar="DIR", help="save a 375 px screenshot of each page, on the repo's files")
    ap.add_argument("--preview-stats", metavar="FILE", help="with --screens only: draw FILE as ugh-stats.json (a preview, not a check)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.screens:
        screens(a.screens, a.preview_stats)
        return 0
    site = Site()
    try:
        faults = examine(site)
    finally:
        site.close()
    for f in faults:
        print("FAIL  " + f)
    counts, stats = repo_json(COUNTS), repo_json(STATS)
    state = lambda o: "absent" if o is None else ("as_of %s" % o.get("as_of") if usable(o) else "over 7 days old: no figure may show")
    print("answer-counts.json: %s; ugh-stats.json: %s" % (state(counts), state(stats)))
    if faults:
        print("ugh stats pages: FAIL, %d fault(s)" % len(faults))
        return 1
    print("ugh stats pages: PASS (4 pages: the repo's files, 3 unusable-file cases, the hand-worked Case 1 file, "
          "planted \"<10\" figures, the 12 November record, 375 px, nothing from outside the site)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
