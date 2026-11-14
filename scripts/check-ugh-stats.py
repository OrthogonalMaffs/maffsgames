#!/usr/bin/env python3
# ci-line: Ugh, stats pages (the six /ugh-stats/ pages in Chromium: live figures match the repo's two JSON files; a missing, stale or misshapen file shows "Figures unavailable right now" and no number; "<10" drawn as a bar of 5, labelled, never summed; Case 1's live box against a hand-worked file; its 12 November figures unchanged; every case's questions played: each answer worked from the numbers shown, only the exact typed answer accepted, a question with a missing or "<10" figure skipped, one stats_question_answered per answer and never question_answered; Cases 3 and 4 against their CSVs and r values; every game and room has a launch date; no sideways scroll at 375 px; nothing loaded from outside the site but Google Fonts; nine planted faults caught) | --selftest && --check
# ci-deps: ugh-stats/ schools/assets/ugh-stats.js schools/assets/answer-counts.json schools/assets/ugh-stats.json schools/assets/launch-dates.json games/ escape-rooms/
"""Do the "Ugh, stats" pages show the figures the site's own files hold, and nothing when they cannot? (contracts
UGH-STATS-PAGES and UGH-STATS-QUESTIONS, 14 Nov 2026)

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
  QUIZ     every case's questions, played in the page: each typed answer is worked here from the numbers its question
           shows, and those numbers from the files the page reads (Case 1's days per game from launch-dates.json);
           one too high is refused, the exact answer is accepted, the working matches; each multiple-choice question
           offers four options with the contract's right one; every answer sends exactly one stats_question_answered.
  SKIP     a question whose figures are missing or include "<10" is skipped, and only that question.
  LAUNCH   every games/<slug>/ and escape-rooms/<slug>/ page has a real date in launch-dates.json.
  NOQA     no ugh-stats page or the loader names question_answered (the event that counts game answers).
  CASE34   Cases 3 and 4 (frozen): the tables on the page are their data.csv, every figure the text states is worked
           from it, every r is the Pearson r of data.csv's columns to 2 places, and the charts draw the tables.
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
LAUNCH = "/schools/assets/launch-dates.json"
PAGES = {"landing": "ugh-stats/index.html", "case1": "ugh-stats/half-our-games/index.html",
         "charts": "ugh-stats/charts/index.html", "case2": "ugh-stats/whos-playing/index.html",
         "case3": "ugh-stats/one-class/index.html", "case4": "ugh-stats/flu-and-answers/index.html"}
READS = {"landing": ("counts",), "case1": ("counts",), "charts": ("stats",), "case2": ("stats",), "case3": (), "case4": ()}
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
        page.wait_for_function("[...document.querySelectorAll('#questions')].every(m => m.getAttribute('data-ugh-quiz') === 'ready')",
                               timeout=30000)
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
            if not READS[key]:
                pass
            elif "counts" in READS[key]:
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
                if not READS[key]:
                    continue
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
    if want("QUIZ"):
        for key in ("case1", "case2", "case3", "case4"):
            check_quiz(site, key, dict(base_plants), "the repo's files", faults)
        # Factor Theorem as game 2: a counts file where it has 10 or more answers
        c = planted_counts()
        c["games"].update({SIX: 900, FT: 40})
        p = dict(base_plants)
        p[COUNTS] = c
        check_quiz(site, "case1", p, "Factor Theorem with 40 answers", faults)
    if want("SKIP"):
        for label, extra in (("answer-counts.json missing", {COUNTS: None}), ("launch-dates.json missing", {LAUNCH: None})):
            p = dict(base_plants)
            p.update(extra)
            check_quiz(site, "case1", p, label, faults)
        st = planted_stats(small=False)
        first_weekend = next(r for r in st["daily"] if dt.date.fromisoformat(r["date"]).weekday() >= 5)
        first_weekend["starts"] = HIDDEN
        st2 = planted_stats(small=False)
        first_weekday = next(r for r in st2["daily"] if dt.date.fromisoformat(r["date"]).weekday() < 5)
        first_weekday["starts"] = HIDDEN
        for label, s in (('a weekend day "<10"', st), ('a weekday "<10"', st2), ("ugh-stats.json missing", None)):
            p = dict(base_plants)
            p[STATS] = s
            check_quiz(site, "case2", p, label, faults)
    if want("LAUNCH"):
        check_launch(base_plants, faults)
    if want("NOQA"):
        check_no_game_event(base_plants, faults)
    if want("CASE34"):
        check_frozen_cases(site, base_plants, faults)
    return faults


# ------------------------------------------------------------------------------------------------ the questions
# (contract UGH-STATS-QUESTIONS, 14 Nov 2026). Every typed answer is worked here from the numbers the question shows,
# and those numbers are worked here from the files the page reads; every multiple-choice question's right option is the
# contract's. Each page is played through in Chromium: typed answers are tried one too high first (it must be refused)
# on alternate questions, multiple choice is answered wrongly on alternate questions, and every answer must send
# exactly one stats_question_answered event and never question_answered.
FULL_MONTHS = "January February March April May June July August September October November December".split()
SINCE = "2026-09-01"
SIX, FT = "six-sevens-bruv", "factor-theorem"
CSV3, CSV4 = "/ugh-stats/one-class/data.csv", "/ugh-stats/flu-and-answers/data.csv"
QUIZ_LEVEL = {"case1": "case1", "case2": "case2", "case3": "case3", "case4": "case4"}
RIGHT = {
    ("case1", 4): "The mean",
    ("case2", 3): "Most play happens on school days, which fits classroom use, but doesn't prove it.",
    ("case2", 4): "Whether play drops during school holidays, like half-term.",
    ("case3", 3): "The median, 402.",
    ("case3", 4): "No. It's real, so keep it, but use the median for a typical day and report the class separately.",
    ("case4", 1): "Weeks with more flu tended to have more answers: a fairly strong positive correlation.",
    ("case4", 2): "Something else drives both: the school term.",
    ("case4", 3): "They all follow the time of year.",
    ("case4", 4): "A few extreme values can make a correlation look much stronger than it is.",
}
FT_RIGHT = ("They're aimed at very different numbers of students: times tables are for almost everyone, factor theorem is "
            "for A level students only.")


class Wrong(Exception):
    pass


def source(path, plants):
    """A served file's text: the plant when there is one, else the repo's (None when absent)."""
    if path in plants:
        body = plants[path]
        return None if body is None else (json.dumps(body) if isinstance(body, dict) else body)
    try:
        return repo_text(path)
    except OSError:
        return None


def source_json(path, plants):
    text = source(path, plants)
    try:
        return json.loads(text) if text is not None else None
    except ValueError:
        return None


def long_date(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, FULL_MONTHS[d.month - 1], d.year)


def divide(n, d):
    """n / d to the nearest whole number (a half up), and the working, by Decimal (not the page's whole-number method)."""
    from decimal import Decimal, ROUND_HALF_UP
    exact = Decimal(n) / Decimal(d)
    ans = int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    for k in range(1, 7):
        shown = exact.quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP)
        if int(shown.quantize(Decimal(1), rounding=ROUND_HALF_UP)) == ans:
            break
    whole_part, frac = str(shown).split(".")
    return ans, "%s ÷ %s = %s.%s ≈ %s." % (fmt(n), fmt(d), fmt(int(whole_part)), frac, fmt(ans))


def page_h1(slug):
    try:
        text = repo_text("games/%s/index.html" % slug)
    except OSError:
        return None
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
    if not m:
        return None
    import html as _html
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip() or None


def quiz_context(key, plants):
    """What the page's questions should be, from the files it is served: {'expect': [indexes], ...}."""
    ctx = {"expect": []}
    if key == "case1":
        counts, ld = source_json(COUNTS, plants), source_json(LAUNCH, plants)
        ok = usable(counts) and isinstance(counts.get("games"), dict) and counts.get("since") == SINCE and isinstance(ld, dict)
        ctx.update(counts=counts if ok else None, ld=ld if ok else None, g2=None)
        if ok:
            g = counts["games"]
            if isinstance(g.get(FT), int) and g[FT] >= 10 and ld.get(FT):
                ctx["g2"] = (FT, "Factor Theorem", True)
            else:
                cands = sorted((v, k) for k, v in g.items() if k != SIX and isinstance(v, int) and v >= 10 and ld.get(k))[:5]
                for _, slug in cands:
                    if page_h1(slug):
                        ctx["g2"] = (slug, page_h1(slug), False)
                        break
        q1 = ok and isinstance(counts["games"].get(SIX), int) and bool(ld.get(SIX))
        q2 = ok and ctx["g2"] is not None
        ctx["expect"] = [i for i, on in ((1, q1), (2, q2), (3, q1 and q2), (4, True)) if on]
    elif key == "case2":
        stats = source_json(STATS, plants)
        ok = usable(stats) and isinstance(stats.get("daily"), list) and len(stats["daily"]) == 30
        ctx["stats"] = stats if ok else None
        part = lambda wkend: [r["starts"] for r in stats["daily"] if (dt.date.fromisoformat(r["date"]).weekday() >= 5) == wkend]
        wd = ok and HIDDEN not in part(False) and bool(part(False))
        we = ok and HIDDEN not in part(True) and bool(part(True))
        ctx["expect"] = [i for i, on in ((1, wd), (2, we), (3, wd and we), (4, True)) if on]
    elif key == "case3":
        html = source("/" + PAGES["case3"], plants) or ""
        m = re.search(r'<table class="week-table" id="week">.*?<tbody>(.*?)</tbody>', html, re.S)
        ctx["week"] = [int(x.replace(",", "")) for x in re.findall(r"<td>([\d,]+)</td>", m.group(1))] if m else []
        ctx["expect"] = [1, 2, 3, 4]
    else:
        ctx["expect"] = [1, 2, 3, 4]
    return ctx


def per_day(ctx, slug, name, stem):
    counts, ld = ctx["counts"], ctx["ld"]
    n, launch = counts["games"][slug], ld[slug]
    to = as_of_time(counts).astimezone(zoneinfo.ZoneInfo("Europe/London")).date()
    days = (to - dt.date.fromisoformat(max(launch, SINCE))).days + 1
    want = ("%s went on the site on %s. Since 1 September it has been available for %d days and has %s answers. What is "
            "its mean number of answers per day, to the nearest whole number?" % (name, long_date(launch), days, fmt(n)))
    if stem != want:
        raise Wrong("the stem reads %r, want %r" % (stem, want))
    return divide(n, days)


def expected(key, ctx, s):
    """A typed question -> (answer, working); a multiple-choice one -> its right option's text. Wrong if the stem is off."""
    i, stem = s["index"], s["stem"]
    if key == "case1":
        if i == 1:
            return per_day(ctx, SIX, "Six Sevens, Bruv", stem)
        if i in (2, 3):
            if not ctx["g2"]:
                raise Wrong("question %d shows, but there is no game 2 to ask about" % i)
            slug, name, is_ft = ctx["g2"]
        if i == 2:
            return per_day(ctx, slug, name, stem)
        if i == 3:
            a = per_day(ctx, SIX, "Six Sevens, Bruv", ctx["stem1"])[0]
            b = per_day(ctx, slug, name, ctx["stem2"])[0]
            want = ("Six Sevens gets about %s answers a day; %s about %s. Which is the best reason to be careful comparing "
                    "these two numbers?" % (fmt(a), name, fmt(b)))
            if stem != want:
                raise Wrong("the stem reads %r, want %r (its numbers are Q1's and Q2's answers)" % (stem, want))
            return FT_RIGHT if is_ft else "%s is for a much smaller group of students." % name
    if key == "case2" and i in (1, 2, 3):
        rows = ctx["stats"]["daily"]
        part = lambda wkend: [r["starts"] for r in rows if (dt.date.fromisoformat(r["date"]).weekday() >= 5) == wkend]
        wd, we = part(False), part(True)
        if i == 1:
            want = ("Over the last 30 days, %d weekdays had %s games started in total. What is the mean number of games "
                    "started per weekday, to the nearest whole number?" % (len(wd), fmt(sum(wd))))
            if stem != want:
                raise Wrong("the stem reads %r, want %r" % (stem, want))
            return divide(sum(wd), len(wd))
        if i == 2:
            want = ("The other %d days were weekends, with %s games started. What is the mean per weekend day, to the "
                    "nearest whole number?" % (len(we), fmt(sum(we))))
            if stem != want:
                raise Wrong("the stem reads %r, want %r" % (stem, want))
            return divide(sum(we), len(we))
        want = ("Weekdays average about %s games started; weekend days about %s. Which conclusion does this best support?"
                % (fmt(divide(sum(wd), len(wd))[0]), fmt(divide(sum(we), len(we))[0])))
        if stem != want:
            raise Wrong("the stem reads %r, want %r (its numbers are Q1's and Q2's answers)" % (stem, want))
    if key == "case3" and i in (1, 2):
        v = ctx["week"]
        if len(v) != 5:
            raise Wrong("the week table has %d figures, want 5" % len(v))
        if i == 1:
            ans = divide(sum(v), 5)[0]
            from decimal import Decimal
            return ans, "%s = %s. %s ÷ 5 = %s ≈ %s." % (" + ".join(fmt(x) for x in v), fmt(sum(v)), fmt(sum(v)),
                                                        Decimal(sum(v)) / 5, fmt(ans))
        srt = sorted(v)
        return srt[2], "In order: %s. The middle value is %s." % (", ".join(fmt(x) for x in srt), fmt(srt[2]))
    return RIGHT[(key, i)]


STATE = r"""() => {
  const box = document.querySelector('#questions .ugh-quiz');
  if (!box) return null;
  const t = s => (s || '').replace(/\s+/g, ' ').trim();
  const next = box.querySelector('.ugh-q-next'), input = box.querySelector('.ugh-q-input');
  return { index: Number(box.getAttribute('data-q-index')), type: box.getAttribute('data-q-type'),
    stem: t((box.querySelector('.ugh-q-stem') || {}).textContent),
    options: [...box.querySelectorAll('.ugh-q-option')].map(b => t(b.textContent)),
    feedback: [...box.querySelectorAll('.ugh-q-feedback p')].map(p => t(p.textContent)),
    answered: box.getAttribute('data-q-state') === 'answered', next: !!next && getComputedStyle(next).display !== 'none',
    inputDisabled: !!(input && input.disabled), events: window.__ev ? window.__ev.length : -1 };
}"""
RECORD = "window.__ev = []; window.mfg = (n, p) => { window.__ev.push([n, JSON.parse(JSON.stringify(p || {}))]); };"
CLICK_OPTION = """t => { const b = [...document.querySelectorAll('#questions .ugh-q-option')]
  .find(b => b.textContent.replace(/\\s+/g, ' ').trim() === t); if (b) b.click(); return !!b; }"""


def play(page, key, ctx, name, faults):
    """Answer every question on the page; return the question numbers seen, in order."""
    page.evaluate(RECORD)
    seen = []
    for _ in range(8):
        s = page.evaluate(STATE)
        if not s:
            faults.append("%s: QUIZ, no questions on the page" % name)
            break
        if s["index"] in seen:
            break
        seen.append(s["index"])
        pos, q = len(seen), "%s Q%d" % (name, s["index"])
        if s["next"]:
            faults.append("%s: QUIZ, Next is on screen before the question is answered" % q)
        if key == "case1" and s["index"] in (1, 2):
            ctx["stem%d" % s["index"]] = s["stem"]
        try:
            want = expected(key, ctx, s)
        except (Wrong, KeyError, TypeError) as e:
            faults.append("%s: QUIZ, %s" % (q, e))
            want = None
        before = len(page.evaluate("window.__ev"))
        if s["type"] == "typed":
            if want is None:
                break
            ans, working = want
            first_wrong = pos % 2 == 1
            if first_wrong:
                page.fill("#questions .ugh-q-input", str(ans + 1))
                page.click("#questions .ugh-q-check")
                s2 = page.evaluate(STATE)
                if s2["answered"] or "Right." in s2["feedback"]:
                    faults.append("%s: QUIZ, %d was accepted, want only the exact %d" % (q, ans + 1, ans))
            s2 = page.evaluate(STATE)
            if not s2["inputDisabled"]:
                page.fill("#questions .ugh-q-input", str(ans))
                page.click("#questions .ugh-q-check")
            s3 = page.evaluate(STATE)
            if not first_wrong or not s2["inputDisabled"]:
                if "Right." not in s3["feedback"]:
                    faults.append("%s: QUIZ, the exact answer %d was not accepted: %r" % (q, ans, s3["feedback"]))
                if "Working: " + working not in s3["feedback"]:
                    faults.append("%s: QUIZ, the working reads %r, want %r" % (q, s3["feedback"], "Working: " + working))
            want_ev = (not first_wrong, 2 if first_wrong else 1)
        else:
            if len(s["options"]) != 4 or (want and want not in s["options"]):
                faults.append("%s: QUIZ, the options are %r, want four with %r right" % (q, s["options"], want))
            right = want if want in s["options"] else s["options"][0]
            pick = right if pos % 2 == 0 else [o for o in s["options"] if o != right][0]
            page.evaluate(CLICK_OPTION, pick)
            s3 = page.evaluate(STATE)
            verdict = "Right." if pick == right else "Not quite."
            if not s3["feedback"] or s3["feedback"][0] != verdict:
                faults.append("%s: QUIZ, choosing %r shows %r, want %r first" % (q, pick[:40], s3["feedback"][:1], verdict))
            if pick != right and "The answer: " + right not in s3["feedback"]:
                faults.append("%s: QUIZ, a wrong choice does not show the right answer %r" % (q, right[:50]))
            want_ev = (pick == right, 1)
        ev = page.evaluate("window.__ev")[before:]
        want_params = {"game_slug": "ugh-stats", "level": QUIZ_LEVEL[key], "question_index": s["index"],
                       "correct": want_ev[0], "attempts": want_ev[1]}
        names = [e[0] for e in ev]
        if "question_answered" in names:
            faults.append("%s: QUIZ, the answer sent question_answered (the game-answer event)" % q)
        if ev != [["stats_question_answered", want_params]]:
            faults.append("%s: QUIZ, the answer sent %r, want exactly one stats_question_answered %r" % (q, ev, want_params))
        if s3["next"]:
            page.click("#questions .ugh-q-next")
        else:
            break
    return seen


def check_quiz(site, key, plants, label, faults):
    ctx = quiz_context(key, plants)
    name = "%s (%s)" % (key, label)
    page, rec = site.open(PAGES[key], plants)
    try:
        got = page.evaluate(PROBE)
        common(name, got, rec, faults)
        seen = play(page, key, ctx, name, faults)
    finally:
        page.close()
    if seen != ctx["expect"]:
        faults.append("%s: SKIP, the questions shown are %r, want %r (a question whose figures are missing or \"<10\" is skipped)"
                      % (name, seen, ctx["expect"]))


def check_launch(plants, faults):
    """Every game and room directory with a page has a launch date, and every date is a real one."""
    ld = source_json(LAUNCH, plants)
    if not isinstance(ld, dict):
        faults.append("LAUNCH: schools/assets/launch-dates.json is missing or not {slug: date}")
        return
    import glob
    for pattern in ("games/*/index.html", "escape-rooms/*/index.html"):
        for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
            slug = os.path.basename(os.path.dirname(path))
            if slug not in ld:
                faults.append("LAUNCH: %s has no line in launch-dates.json (a new game adds its own at launch)"
                              % os.path.relpath(path, ROOT).replace(os.sep, "/"))
    for slug, d in ld.items():
        try:
            ok = dt.date(2026, 1, 1) <= dt.date.fromisoformat(d) <= dt.date.today() and len(d) == 10
        except (TypeError, ValueError):
            ok = False
        if not ok:
            faults.append("LAUNCH: launch-dates.json gives %s the date %r, want a real YYYY-MM-DD" % (slug, d))


def check_no_game_event(plants, faults):
    for path in [LOADER] + ["/" + p for p in PAGES.values()]:
        text = source(path, plants) or ""
        if re.search(r"(?<!stats_)question_answered", text):
            faults.append("NOQA: %s names question_answered; the questions send stats_question_answered only" % path.lstrip("/"))


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** 0.5


def r2(v):
    s = "%.2f" % v
    return s.replace("-", "−")


def check_frozen_cases(site, plants, faults):
    """Cases 3 and 4: the tables on the page are their data.csv, every stated figure and r is worked from it, and the
    charts draw it."""
    import csv as _csv
    import io
    rows3 = list(_csv.DictReader(io.StringIO(source(CSV3, plants) or "")))
    rows4 = list(_csv.DictReader(io.StringIO(source(CSV4, plants) or "")))
    html3, html4 = source("/" + PAGES["case3"], plants) or "", source("/" + PAGES["case4"], plants) or ""
    # Case 3
    table = re.findall(r'<tr data-date="([\d-]+)"><th scope="row">([^<]+)</th><td>([\d,]+)</td><td>(yes|no)</td></tr>', html3)
    want = [(r["date"], "%s %d %s" % (r["day"], int(r["date"][8:]), dt.date.fromisoformat(r["date"]).strftime("%b")),
             fmt(int(r["answers"])), r["whole_class_day"]) for r in rows3]
    if table != want or len(rows3) != 28:
        faults.append("case3: CSV, the 28-day table on the page is not data.csv (%d rows on the page, %d in the CSV)" % (len(table), len(rows3)))
    a = [int(r["answers"]) for r in rows3] or [0]
    rest = [int(r["answers"]) for r in rows3 if r["whole_class_day"] == "no"] or [0]
    week = [int(r["answers"]) for r in rows3 if "2026-11-02" <= r["date"] <= "2026-11-06"]
    wk_page = re.search(r'id="week">.*?<tbody>(.*?)</tbody>', html3, re.S)
    if not wk_page or [int(x.replace(",", "")) for x in re.findall(r"<td>([\d,]+)</td>", wk_page.group(1))] != week:
        faults.append("case3: CSV, the week of 2 November on the page is not data.csv's 2 to 6 November %r" % week)
    srt = sorted(week) if len(week) == 5 else [0] * 5
    no_tue = sorted(week[:1] + week[2:]) if len(week) == 5 else [0] * 4
    from decimal import Decimal, ROUND_HALF_UP
    rnd = lambda v: int(Decimal(v).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    stated = [
        "%s answers in %d days, a mean of %s a day" % (fmt(sum(a)), len(a), fmt(rnd(Decimal(sum(a)) / len(a)))),
        "the other %d days average %s" % (len(rest), fmt(rnd(Decimal(sum(rest)) / len(rest)))),
        "The median, %s." % fmt(srt[2]),
        "The mean, %s." % fmt(rnd(Decimal(sum(week)) / 5)),
        "The biggest value, %s." % fmt(max(week or [0])),
        "The range, %s." % fmt(max(week or [0]) - min(week or [0])),
        "Without Tuesday, the mean would be %s and the median %s" % (fmt(rnd(Decimal(sum(no_tue)) / 4)), fmt(rnd(Decimal(no_tue[1] + no_tue[2]) / 2))),
    ]
    for s in stated:
        if s not in html3:
            faults.append("case3: CSV, the page should say %r, worked from data.csv" % s)
    # Case 4
    table = re.findall(r'<tr( data-class-day="yes")?><th scope="row">([^<]+)</th><td>([\d,]+)</td><td>([\d.]+)</td></tr>', html4)
    want = [(' data-class-day="yes"' if r["answers"] != r["answers_without_class_days"] else "",
             "%d %s" % (int(r["week_beginning"][8:]), dt.date.fromisoformat(r["week_beginning"]).strftime("%b")),
             fmt(int(r["answers"])), r["flu_tests_positive_pct"]) for r in rows4]
    if table != want or len(rows4) != 9:
        faults.append("case4: CSV, the week table on the page is not data.csv (%d rows on the page, %d in the CSV)" % (len(table), len(rows4)))
    if len(rows4) >= 3:
        col = lambda k: [float(r[k]) for r in rows4]
        flu, ans, dl = col("flu_tests_positive_pct"), col("answers"), col("daylight_hours_plymouth")
        r_main, r_wo = pearson(flu, ans), pearson(flu, col("answers_without_class_days"))
        r_dl, r_dlf = pearson(dl, ans), pearson(dl, flu)
        for s in ("For these two, r = %s." % r2(r_main), "What does r = %s tell you?" % r2(r_main),
                  "correlates with our answers: r = %s." % r2(r_dl), "correlate with each other: r = %s." % r2(r_dlf),
                  "falls from %s to %s." % (r2(r_main), r2(r_wo))):
            if s not in html4:
                faults.append("case4: r = values must be worked from data.csv: the page should say %r" % s)
    # the charts draw the tables
    for key, sel in (("case3", "#dailyChart rect"), ("case4", "#scatterChart circle")):
        page, rec = site.open(PAGES[key], plants)
        try:
            got = page.evaluate(PROBE)
            common(key + " (frozen)", got, rec, faults)
            marks = page.evaluate("s => [...document.querySelectorAll(s)].map(e => [e.getAttribute('data-value') || e.getAttribute('data-x'), e.getAttribute('fill'), e.getAttribute('data-y'), e.getAttribute('data-hollow')])", sel)
        finally:
            page.close()
        if key == "case3":
            want = [[r["answers"], "#0d9488" if r["whole_class_day"] == "yes" else "#1a2744", None, None] for r in rows3]
        else:
            want = [[_num(r["flu_tests_positive_pct"]), "#ffffff" if r["answers"] != r["answers_without_class_days"] else "#1a2744", r["answers"],
                     "1" if r["answers"] != r["answers_without_class_days"] else "0"] for r in rows4]
        if marks != want:
            faults.append("%s: the chart draws %r, want %r (from data.csv)" % (key, marks[:4], want[:4]))


def _num(s):
    """A CSV figure as JavaScript's String(Number(s)) writes it."""
    v = float(s)
    return str(int(v)) if v == int(v) else repr(v)


# ------------------------------------------------------------------------------------------------ self-test
def selftest():
    loader = repo_text(LOADER)
    case1_html = repo_text(PAGES["case1"])
    case2_html = repo_text(PAGES["case2"])
    case4_html = repo_text(PAGES["case4"])
    launch = json.loads(repo_text(LAUNCH))
    launch.pop(SIX)
    csv3 = repo_text(CSV3)

    def swap(text, old, new):
        assert text.count(old) == 1, "the selftest's plant no longer finds %r" % old
        return text.replace(old, new)
    plants = [
        ("a stale file shown as a number", {LOADER: swap(loader, "var STALE_MS = 7 * 24 * 3600 * 1000;", "var STALE_MS = 70 * 24 * 3600 * 1000;")},
         ("ABSENT",), "ABSENT"),
        ('"<10" summed', {LOADER: swap(loader, "if (hidden(v)) hid += 1; else sum += v;", "sum += drawn(v);")}, ("SMALL",), "never added in"),
        ("a frozen figure changed", {"/" + PAGES["case1"]: swap(case1_html, "<td>4,181</td>", "<td>4,182</td>")}, ("REAL",), "FROZEN"),
        ("a typed answer not exact", {LOADER: swap(loader, "var right = Number(raw) === q.answer;",
                                                   "var right = Math.abs(Number(raw) - q.answer) <= 1;")}, ("QUIZ",), "was accepted"),
        ('a "<10" question not skipped', {"/" + PAGES["case2"]: swap(case2_html, "if (!v.length || v.some(U.hidden)) return null;",
                                                                    "if (!v.length) return null;")}, ("SKIP",), "SKIP"),
        ("a game with no launch date", {LAUNCH: launch}, ("LAUNCH",), "LAUNCH"),
        ("question_answered sent", {LOADER: swap(loader, "var EVENT = 'stats_question_answered';", "var EVENT = 'question_answered';")},
         ("QUIZ", "NOQA"), "question_answered"),
        ("a CSV figure changed", {CSV3: swap(csv3, "2026-10-15,Thu,513,", "2026-10-15,Thu,514,")}, ("CASE34",), "CSV"),
        ("an r changed", {"/" + PAGES["case4"]: swap(case4_html, "For these two, r = 0.70.", "For these two, r = 0.80.")}, ("CASE34",), "r = "),
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
    print("ugh stats pages: PASS (6 pages: the repo's files, 3 unusable-file cases, the hand-worked Case 1 file, "
          "planted \"<10\" figures, the 12 November record, every case's questions and skips, launch dates, Cases 3 "
          "and 4 against their CSVs, 375 px, nothing from outside the site)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
