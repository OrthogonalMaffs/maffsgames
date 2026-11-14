#!/usr/bin/env python3
"""Fetch the answer counts from the counts Apps Script, validate them, and write schools/assets/answer-counts.json;
then fetch the "Ugh, stats" figures from the same script (?stats=1), validate them, and write schools/assets/ugh-stats.json.

Contract ANSWER-COUNTS (23 Oct 2026). The daily workflow (.github/workflows/answer-counts.yml) runs this, then commits
the file with "[skip ci]". A failure writes nothing, so the file on main stays as it was and only that job fails; the
site hides every figure whose source is more than 7 days old (schools/assets/answer-count.js).

Contract UGH-STATS-DATA (14 Nov 2026). The two files are fetched, validated and written each on its own: a fault in one
never stops the other being written, and either fault fails the run. While the Apps Script has not been redeployed,
?stats=1 answers the counts payload: that is reported ("stats endpoint not deployed yet"), writes nothing and fails nothing.

    python scripts/fetch-answer-counts.py                 # fetch, validate, write both files
    python scripts/fetch-answer-counts.py --check         # validate the files already in the repo (as_of not required to be today)
    python scripts/fetch-answer-counts.py --selftest      # each planted fault must fail; the clean payloads pass

The payload is exactly {as_of, since, total, games}. It is valid when:
  - as_of is an ISO time with an offset (Z, +00:00 or +hh:mm), and its date, in Europe/London, is today's;
  - since is 1 September of the school year that today falls in;
  - every game count is a whole number >= 0 (not a boolean, float or string), keyed by a slug that is a game directory
    under games/ or an escape room (escape-<directory> under escape-rooms/);
  - total is a whole number equal to the sum of the game counts.

The stats payload is exactly {as_of, daily, levels, hours, countries}. It is valid when:
  - as_of is as above;
  - daily is exactly 30 {date, starts}, consecutive dates, oldest first, ending today or yesterday (Europe/London);
  - levels is a list of {level, starts}, each level once, a short plain label;
  - hours is exactly {weekday, weekend}, each a list of 24 counts;
  - countries is a list of {country, sessions}, each country once, every one at 10 sessions or more except
    "Other countries" (the countries under 10, summed), which may be "<10";
  - every count is 0, a whole number >= 10, or the string "<10": a figure from 1 to 9 is never published;
  - nothing in it is named "test" or "terminal-test".
"""
import argparse, datetime as dt, json, os, pathlib, re, sys, time, urllib.request

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "schools" / "assets" / "answer-counts.json"
ENDPOINT = "https://script.google.com/macros/s/AKfycbxvtM7Y5jtL7flZozfFUEoZZalNHieP44vK6rB4juUG5yPgQf5hfb8tOlgetoEtogZl8w/exec"
KEYS = {"as_of", "since", "total", "games"}
STATS_OUT = BASE / "schools" / "assets" / "ugh-stats.json"
STATS_KEYS = {"as_of", "daily", "levels", "hours", "countries"}
STATS_DAYS = 30
HIDDEN = "<10"                     # how a count from 1 to 9 is published ("figures below 10 are hidden")
HIDE_BELOW = 10
OTHER_COUNTRIES = "Other countries"
TEST_NAMES = {"test", "terminal-test"}
LEVEL_LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.+-]{0,23}$")     # the Apps Script's STATS_LEVEL_LABEL
# The offset is Z (zero, written by the Apps Script's "XXX" pattern while London is on GMT: ISO 8601 and RFC 3339 both allow it)
# or +hh:mm / -hh:mm. Until 26 Oct 2026 only the second was accepted, and every run since the clocks went back failed on it.
AS_OF = re.compile(r"^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(Z|[+-]\d\d:\d\d)$")
RETRY_PAUSES_S = (60, 300, 900)   # the pauses before the 2nd, 3rd and 4th attempt (Jon, 28 Oct 2026); the workflow's timeout allows them
FRESH_HOURS = 24           # the daily file's as_of must be younger than this when the scheduled site check looks (canon 7.5.5)


def as_of_utc(s):
    """The instant an as_of names, as an aware UTC datetime; None when it is not an ISO time with an offset (Z or +hh:mm)."""
    m = AS_OF.match(s) if isinstance(s, str) else None
    if not m:
        return None
    try:
        t = dt.datetime(*(int(m[i]) for i in range(1, 7)), tzinfo=dt.timezone.utc)
    except ValueError:
        return None
    off = m[7]
    if off != "Z":
        mins = int(off[1:3]) * 60 + int(off[4:6])
        t -= dt.timedelta(minutes=mins if off[0] == "+" else -mins)
    return t


def stale_faults(obj, now_utc=None, hours=FRESH_HOURS):
    """[fault] when the file's as_of is not within `hours` of now (or not readable): the daily job has stopped committing."""
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    t = as_of_utc(obj.get("as_of") if isinstance(obj, dict) else None)
    if t is None:
        return ["as_of %r is not an ISO time with an offset, so its age is unknown" % (obj.get("as_of") if isinstance(obj, dict) else None,)]
    age = (now_utc - t).total_seconds() / 3600
    if age > hours:
        return ["as_of %s is %.1f hours old (limit %d): the daily answer-counts job has not committed a figure since" % (obj["as_of"], age, hours)]
    if age < -1:
        return ["as_of %s is %.1f hours in the future" % (obj["as_of"], -age)]
    return []


def _last_sunday(year, month):
    d = dt.date(year, month, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def london_date(now_utc):
    """The date in Europe/London at `now_utc` (UTC, aware). BST runs from 01:00 UTC on the last Sunday of March to
    01:00 UTC on the last Sunday of October. Written out because zoneinfo has no tz database on Windows."""
    y = now_utc.year
    start = dt.datetime.combine(_last_sunday(y, 3), dt.time(1), dt.timezone.utc)
    end = dt.datetime.combine(_last_sunday(y, 10), dt.time(1), dt.timezone.utc)
    return (now_utc + dt.timedelta(hours=1 if start <= now_utc < end else 0)).date()


def school_year_start(today):
    return dt.date(today.year if today.month >= 9 else today.year - 1, 9, 1)


def is_whole(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def validate(obj, now_utc=None, require_today=True, prev=None):
    """The faults in a payload (empty list = valid). Every slug the Sheet returns is counted, known or not (Jon, 27 Oct 2026: a
    slug check rejected the whole file when The 6 P's started sending events); `prev` is the file already published, and the
    total may not fall below its total within the same school year (the counts only grow; a fall means rows were lost)."""
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    if not isinstance(obj, dict):
        return ["the payload is not an object"]
    f = []
    if set(obj) != KEYS:
        f.append("keys are %s, want exactly %s" % (sorted(obj), sorted(KEYS)))
    as_of = obj.get("as_of")
    m = AS_OF.match(as_of) if isinstance(as_of, str) else None
    if not m:
        f.append("as_of %r is not an ISO time with an offset" % (as_of,))
    elif require_today:
        got = london_date(as_of_utc(as_of)) if as_of_utc(as_of) else None      # the instant's date in London, whatever offset it is written in
        today = london_date(now_utc)
        if got != today:
            f.append("as_of %s is not today (%s in London): the counts are not current" % (as_of, today))
    since = obj.get("since")
    want = school_year_start(london_date(now_utc)).isoformat()
    if since != want:
        f.append("since is %r, want %s" % (since, want))
    games = obj.get("games")
    if not isinstance(games, dict):
        f.append("games is not an object")
        games = {}
    badkey = sorted(str(k) for k in games if not isinstance(k, str) or not k)
    if badkey:
        f.append("game keys that are not non-empty text: %s" % ", ".join(badkey))
    nonwhole = sorted(k for k, v in games.items() if not is_whole(v))
    if nonwhole:
        f.append("counts that are not whole numbers >= 0: %s" % ", ".join("%s=%r" % (k, games[k]) for k in nonwhole))
    total = obj.get("total")
    if not is_whole(total):
        f.append("total %r is not a whole number >= 0" % (total,))
    elif not nonwhole and total != sum(games.values()):
        f.append("total %d is not the sum of the games (%d)" % (total, sum(games.values())))
    if is_whole(total) and isinstance(prev, dict) and prev.get("since") == since and is_whole(prev.get("total")) and total < prev["total"]:
        f.append("total %d is below the published file's total %d (as_of %s): the counts only grow, so rows have been lost and the file is not replaced"
                 % (total, prev["total"], prev.get("as_of")))
    return f


def is_count(v):
    """A count as the stats file may publish it: 0, a whole number >= 10, or "<10". Never a figure from 1 to 9."""
    return v == HIDDEN if isinstance(v, str) else is_whole(v) and (v == 0 or v >= HIDE_BELOW)


def _iso_date(s):
    try:
        return dt.date.fromisoformat(s) if isinstance(s, str) and re.fullmatch(r"\d{4}-\d\d-\d\d", s) else None
    except ValueError:
        return None


def _strings(x):
    """Every text value in a payload, at any depth."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from _strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from _strings(v)


def _rows(obj, key, fields, f):
    """obj[key] as a list of objects with exactly `fields`; the faults go to f, and only the well-formed rows come back."""
    rows = obj.get(key)
    if not isinstance(rows, list):
        f.append("%s is not a list" % key)
        return []
    bad = [r for r in rows if not isinstance(r, dict) or set(r) != set(fields)]
    if bad:
        f.append("%s: %d entr%s not exactly {%s}, e.g. %r" % (key, len(bad), "y is" if len(bad) == 1 else "ies are", ", ".join(fields), bad[0]))
    return [r for r in rows if isinstance(r, dict) and set(r) == set(fields)]


def validate_stats(obj, now_utc=None, require_today=True):
    """The faults in a stats payload (empty list = valid). With require_today (a fetch), as_of must be today in London and
    the 30 dates end today or yesterday; without it (the committed file), the dates are held to as_of's own date."""
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    if not isinstance(obj, dict):
        return ["the payload is not an object"]
    f = []
    if set(obj) != STATS_KEYS:
        f.append("keys are %s, want exactly %s" % (sorted(obj), sorted(STATS_KEYS)))
    as_of = obj.get("as_of")
    at = as_of_utc(as_of)
    today = london_date(now_utc)
    if at is None:
        f.append("as_of %r is not an ISO time with an offset" % (as_of,))
    elif require_today and london_date(at) != today:
        f.append("as_of %s is not today (%s in London): the figures are not current" % (as_of, today))
    # daily: exactly 30 consecutive dates, oldest first, ending on the reference day or the day before it
    daily = _rows(obj, "daily", ("date", "starts"), f)
    dates = [_iso_date(r["date"]) for r in daily]
    if not isinstance(obj.get("daily"), list) or len(obj["daily"]) != STATS_DAYS:
        f.append("daily has %s dates, want exactly %d" % (len(obj["daily"]) if isinstance(obj.get("daily"), list) else "no", STATS_DAYS))
    if None in dates:
        f.append("daily: a date that is not yyyy-mm-dd: %r" % ([r["date"] for r, d in zip(daily, dates) if d is None][0],))
    elif dates:
        if any(b - a != dt.timedelta(days=1) for a, b in zip(dates, dates[1:])):
            f.append("daily: the dates are not consecutive, oldest first")
        ref = today if require_today else (london_date(at) if at else None)
        if ref and dates[-1] not in (ref, ref - dt.timedelta(days=1)):
            f.append("daily ends on %s, want %s or the day before" % (dates[-1], ref))
    counts = [("daily " + str(r["date"]), r["starts"]) for r in daily]
    # levels
    levels = _rows(obj, "levels", ("level", "starts"), f)
    names = [r["level"] for r in levels]
    badname = [n for n in names if not isinstance(n, str) or not LEVEL_LABEL.match(n)]
    if badname:
        f.append("levels: a level that is not a short plain label: %r" % (badname[0],))
    if len(set(map(str, names))) != len(names):
        f.append("levels: a level is listed twice")
    counts += [("level %s" % (r["level"],), r["starts"]) for r in levels]
    # hours
    hours = obj.get("hours")
    if not isinstance(hours, dict) or set(hours) != {"weekday", "weekend"}:
        f.append("hours is not exactly {weekday, weekend}")
        hours = {}
    for k in ("weekday", "weekend"):
        if k in hours and (not isinstance(hours[k], list) or len(hours[k]) != 24):
            f.append("hours.%s has %s values, want 24" % (k, len(hours[k]) if isinstance(hours[k], list) else "no"))
        elif k in hours:
            counts += [("hours.%s[%d]" % (k, i), v) for i, v in enumerate(hours[k])]
    # countries: none under 10 by name; the small ones are one "Other countries" entry
    countries = _rows(obj, "countries", ("country", "sessions"), f)
    cnames = [r["country"] for r in countries]
    badname = [n for n in cnames if not isinstance(n, str) or not n.strip() or len(n) > 60 or "<" in n or ">" in n]
    if badname:
        f.append("countries: a name that is empty, over 60 characters or holds markup: %r" % (badname[0],))
    if len(set(map(str, cnames))) != len(cnames):
        f.append("countries: a country is listed twice")
    for r in countries:
        v = r["sessions"]
        if r["country"] != OTHER_COUNTRIES and is_count(v) and (v == HIDDEN or v == 0):
            f.append("countries: %s has %r sessions; a country under %d is folded into \"%s\", never listed by name" % (r["country"], v, HIDE_BELOW, OTHER_COUNTRIES))
        elif r["country"] == OTHER_COUNTRIES and v == 0:
            f.append("countries: \"%s\" is listed with 0 sessions" % OTHER_COUNTRIES)
    counts += [("country %s" % (r["country"],), r["sessions"]) for r in countries]
    # every count: 0, a whole number >= 10, or "<10"
    badcount = ["%s=%r" % (k, v) for k, v in counts if not is_count(v)]
    if badcount:
        f.append("counts that are not 0, a whole number >= %d or \"%s\": %s%s" % (
            HIDE_BELOW, HIDDEN, ", ".join(badcount[:8]), " and %d more" % (len(badcount) - 8) if len(badcount) > 8 else ""))
    test = sorted({x for x in _strings(obj) if x.strip().lower() in TEST_NAMES})
    if test:
        f.append("a test name is published: %s" % ", ".join(test))
    return f


def stats_url(url):
    return url + ("&" if "?" in url else "?") + "stats=1"


def fetch(url=ENDPOINT, pauses=RETRY_PAUSES_S, used=None):
    """One attempt, then one more after each pause (1, 5 and 15 minutes). Only the FETCH is retried: a network error, an HTTP error
    or a reply that is not JSON (a Google server error page). A reply that parses but fails validate() is not retried: it is
    not a temporary fault, and it fails the run at once. `used`, a list, gains each pause as it is slept: the stats fetch is
    given the pauses the counts fetch did not use, so the two together never wait longer than the one sequence (the
    workflow's timeout allows one)."""
    last = None
    for i in range(len(pauses) + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:
            last = exc
            if i < len(pauses):
                print("fetch attempt %d of %d failed (%s); trying again in %d s" % (i + 1, len(pauses) + 1, exc, pauses[i]), flush=True)
                time.sleep(pauses[i])
                if used is not None:
                    used.append(pauses[i])
    raise RuntimeError("could not fetch the counts after %d attempts: %s" % (len(pauses) + 1, last))


def fetch_stats(url, pauses, out=STATS_OUT):
    """Fetch ?stats=1, validate it and write ugh-stats.json. Returns 0 (written, or the endpoint is not deployed yet) or 1
    (not written: the file on main is unchanged). Never raises: the answer counts are already written or refused by now."""
    try:
        obj = fetch(stats_url(url), pauses)
    except RuntimeError as exc:
        print("FAIL ugh stats:", str(exc).replace("the counts", "the stats"))
        print("ugh stats: NOT written (the file on main is unchanged)")
        return 1
    if isinstance(obj, dict) and set(obj) == KEYS:
        print("ugh stats: stats endpoint not deployed yet (?stats=1 answered the counts payload); no ugh-stats.json written")
        return 0
    if isinstance(obj, dict) and set(obj) == {"error"}:
        faults = ["the stats endpoint answered an error: %s" % (obj["error"],)]
    else:
        faults = validate_stats(obj)
    if faults:
        for x in faults:
            print("FAIL ugh stats:", x)
        print("ugh stats: NOT written (the file on main is unchanged)")
        return 1
    write(obj, out)
    print("ugh stats: written, %d days to %s, %d level(s), %d countr%s, as_of %s" % (
        len(obj["daily"]), obj["daily"][-1]["date"], len(obj["levels"]), len(obj["countries"]),
        "y" if len(obj["countries"]) == 1 else "ies", obj["as_of"]))
    return 0


def write(obj, path=OUT):
    body = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")


def retry_selftest():
    """The retry: attempts and pauses, success after failures, exhaustion, and the planted failing address."""
    import io, subprocess, tempfile, unittest.mock as mock

    class Reply:
        def __init__(self, body): self.body = body
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return self.body

    def run(seq):
        """seq: what each attempt does (an Exception to raise, or bytes to return). Returns (result or error text, sleeps, attempts)."""
        sleeps, calls = [], []

        def fake_open(url, timeout=0):
            calls.append(url)
            x = seq[len(calls) - 1]
            if isinstance(x, Exception):
                raise x
            return Reply(x)
        with mock.patch("urllib.request.urlopen", fake_open), mock.patch("time.sleep", sleeps.append), mock.patch("builtins.print"):
            try:
                return fetch("http://x/"), sleeps, len(calls)
            except RuntimeError as exc:
                return str(exc), sleeps, len(calls)
    err = OSError("HTTP Error 500: Internal Server Error")
    out = []
    r, sl, n = run([b'{"a": 1}'])
    out.append(("fetch: a good first reply is used with no pause", r == {"a": 1} and sl == [] and n == 1))
    r, sl, n = run([err, b"<html>Google server error</html>", b'{"a": 2}'])
    out.append(("fetch: an HTTP error and a non-JSON page are retried after 1 then 5 minutes", r == {"a": 2} and sl == [60, 300] and n == 3))
    r, sl, n = run([err, err, err, b'{"a": 3}'])
    out.append(("fetch: succeeds on the 4th attempt after pauses of 1, 5 and 15 minutes", r == {"a": 3} and sl == [60, 300, 900] and n == 4))
    r, sl, n = run([err, err, err, err])
    out.append(("fetch: four failures raise, with exactly 4 attempts and no pause after the last", isinstance(r, str) and "after 4 attempts" in r and sl == [60, 300, 900] and n == 4))
    # the planted failing address, through main(): retries, fails, the counts file is byte for byte unchanged
    before = OUT.read_bytes() if OUT.exists() else None
    p = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve()), "--url", "http://127.0.0.1:9/", "--pauses", "0,0,0"],
                       capture_output=True, text=True)
    after = OUT.read_bytes() if OUT.exists() else None
    out.append(("planted failing address: 3 retries, exit 1, counts file unchanged",
                p.returncode == 1 and p.stdout.count("fetch attempt") == 3 and "NOT written" in p.stdout and before == after))
    return out


def stats_sample(last="2026-10-22", as_of="2026-10-23T06:30:12+01:00"):
    """A clean stats payload: 30 dates ending `last`, with hidden counts, zeros and a folded "Other countries"."""
    end = dt.date.fromisoformat(last)
    starts = [0, HIDDEN, 10, 57, 123]
    return {
        "as_of": as_of,
        "daily": [{"date": (end - dt.timedelta(days=29 - i)).isoformat(), "starts": starts[i % 5]} for i in range(30)],
        "levels": [{"level": "gcse", "starts": 412}, {"level": "ks3", "starts": 96}, {"level": "none", "starts": 10},
                   {"level": "alevel", "starts": HIDDEN}, {"level": "other", "starts": HIDDEN}],
        "hours": {"weekday": [0, 0, 0, 0, 0, 0, HIDDEN, 12, 40, 88, 120, 131, 77, 95, 102, 64, 30, 18, 11, 10, HIDDEN, HIDDEN, 0, 0],
                  "weekend": [0] * 8 + [HIDDEN, 10, 14, 19, 12, HIDDEN, HIDDEN, 10, HIDDEN, 0, 0, HIDDEN, 0, 0, 0, 0]},
        "countries": [{"country": "United Kingdom", "sessions": 1840}, {"country": "United States", "sessions": 61},
                      {"country": "Unknown", "sessions": 12}, {"country": OTHER_COUNTRIES, "sessions": HIDDEN}],
    }


def stats_selftest():
    """The stats validator's plants (each must fail), the clean payloads (each must pass), and the two files' independence."""
    import contextlib, io, tempfile, unittest.mock as mock
    now = dt.datetime(2026, 10, 23, 5, 30, tzinfo=dt.timezone.utc)          # 06:30 on 23 Oct in London

    def edit(fn, **kw):
        d = stats_sample(**kw)
        fn(d)
        return d

    def setv(path, value):
        def fn(d):
            for k in path[:-1]:
                d = d[k]
            d[path[-1]] = value
        return fn
    cases = [
        ("stats: clean payload (30 dates to yesterday)", stats_sample(), None),
        ("stats: clean payload, 30 dates to today", stats_sample(last="2026-10-23"), None),
        ("stats: \"Other countries\" as a number of 10 or more", edit(setv(("countries", 3, "sessions"), 14)), None),
        ("stats: no \"Other countries\" entry at all", edit(lambda d: d["countries"].pop()), None),
        ("stats PLANT: a count of 3 published as a number", edit(setv(("daily", 4, "starts"), 3)), "counts that are not"),
        ("stats PLANT: a country with 4 sessions not folded", edit(lambda d: d["countries"].insert(3, {"country": "Ireland", "sessions": 4})), "counts that are not"),
        ("stats PLANT: 29 daily dates", edit(lambda d: d["daily"].pop(0)), "want exactly 30"),
        ("stats PLANT: a 23-length hours array", edit(lambda d: d["hours"]["weekend"].pop()), "want 24"),
        ("stats PLANT: a missing key", edit(lambda d: d.pop("countries")), "keys are"),
        ("stats: an extra key", edit(setv(("since",), "2026-09-01")), "keys are"),
        ("stats: a named country published as \"<10\"", edit(setv(("countries", 2, "sessions"), HIDDEN)), "folded into"),
        ("stats: a named country with 0 sessions", edit(setv(("countries", 2, "sessions"), 0)), "folded into"),
        ("stats: a count of 9 in an hours array", edit(setv(("hours", "weekday", 9), 9)), "counts that are not"),
        ("stats: a count of 1 for a level", edit(setv(("levels", 3, "starts"), 1)), "counts that are not"),
        ("stats: a float count", edit(setv(("daily", 4, "starts"), 12.0)), "counts that are not"),
        ("stats: a boolean count", edit(setv(("daily", 4, "starts"), True)), "counts that are not"),
        ("stats: a negative count", edit(setv(("hours", "weekend", 0), -1)), "counts that are not"),
        ("stats: a hidden count spelt another way", edit(setv(("daily", 4, "starts"), "< 10")), "counts that are not"),
        ("stats: a level named test", edit(setv(("levels", 4, "level"), "test")), "test name"),
        ("stats: a level named Terminal-Test", edit(setv(("levels", 4, "level"), "Terminal-Test")), "test name"),
        ("stats: a level that holds markup", edit(setv(("levels", 4, "level"), "<img src=x>")), "plain label"),
        ("stats: a level listed twice", edit(setv(("levels", 4, "level"), "gcse")), "listed twice"),
        ("stats: a country that holds markup", edit(setv(("countries", 1, "country"), "<b>US</b>")), "markup"),
        ("stats: 31 daily dates", edit(lambda d: d["daily"].append({"date": "2026-10-23", "starts": 0})), "want exactly 30"),
        ("stats: a gap in the dates", edit(setv(("daily", 10, "date"), "2026-10-01")), "not consecutive"),
        ("stats: dates newest first", edit(lambda d: d["daily"].reverse()), "not consecutive"),
        ("stats: 30 dates ending two days ago", stats_sample(last="2026-10-21"), "or the day before"),
        ("stats: 30 dates ending tomorrow", stats_sample(last="2026-10-24"), "or the day before"),
        ("stats: a daily entry with an extra field", edit(lambda d: d["daily"][0].update(slug="x")), "not exactly"),
        ("stats: hours without weekend", edit(lambda d: d["hours"].pop("weekend")), "weekday, weekend"),
        ("stats: as_of yesterday", stats_sample(as_of="2026-10-22T06:30:12+01:00"), "not today"),
        ("stats: as_of null (the first count unfinished)", stats_sample(as_of=None), "ISO time"),
        ("stats: not an object", [1], "not an object"),
        ("stats: the counts payload is not a stats payload", {"as_of": "2026-10-23T06:30:12+01:00", "since": "2026-09-01", "total": 0, "games": {}}, "keys are"),
    ]
    out = []
    for name, obj, want in cases:
        got = validate_stats(obj, now)
        out.append((name, (not got) if want is None else any(want in g for g in got), got[0][:110] if got else "(valid)"))
    # the committed file (--check): held to its own as_of, whatever today is
    later = dt.datetime(2026, 11, 2, 12, 0, tzinfo=dt.timezone.utc)
    got = validate_stats(stats_sample(), later, require_today=False)
    out.append(("stats --check: a ten-day-old file is valid against its own as_of", not got, got[0][:110] if got else "(valid)"))
    got = validate_stats(stats_sample(last="2026-10-20"), later, require_today=False)
    out.append(("stats --check: dates ending three days before as_of fail", any("or the day before" in g for g in got), got[0][:110] if got else "(valid)"))
    got = validate_stats(edit(setv(("daily", 4, "starts"), 3)), later, require_today=False)
    out.append(("stats --check: a count of 3 fails in a committed file too", any("counts that are not" in g for g in got), got[0][:110] if got else "(valid)"))

    # run(): each file on its own. urlopen is faked by address: the counts address and the ?stats=1 address answer separately.
    class Reply:
        def __init__(self, body): self.body = body
        def __enter__(self): return self
        def __exit__(self, *a): return False
        def read(self): return self.body

    today = london_date(dt.datetime.now(dt.timezone.utc))
    fresh = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    good_counts = {"as_of": fresh, "since": school_year_start(today).isoformat(), "total": 5, "games": {"a": 2, "b": 3}}
    good_stats = stats_sample(last=(today - dt.timedelta(days=1)).isoformat(), as_of=fresh)
    err = OSError("HTTP Error 500: Internal Server Error")

    def go(counts_seq, stats_seq, pauses=(60, 300, 900)):
        """Each seq: what each attempt at that address does (an Exception, or an object sent as JSON). Returns
        (exit status, counts file or None, stats file or None, sleeps, output)."""
        seqs = {False: list(counts_seq), True: list(stats_seq)}
        sleeps, buf = [], io.StringIO()

        def fake_open(url, timeout=0):
            x = seqs["stats=1" in url].pop(0)
            if isinstance(x, Exception):
                raise x
            return Reply(json.dumps(x).encode("utf-8"))
        with tempfile.TemporaryDirectory() as d:
            c, s_ = pathlib.Path(d) / "answer-counts.json", pathlib.Path(d) / "ugh-stats.json"
            with mock.patch("urllib.request.urlopen", fake_open), mock.patch("time.sleep", sleeps.append), contextlib.redirect_stdout(buf):
                rc = run("http://x/exec", pauses, c, s_)
            return (rc, json.loads(c.read_text(encoding="utf-8")) if c.exists() else None,
                    json.loads(s_.read_text(encoding="utf-8")) if s_.exists() else None, sleeps, buf.getvalue())
    bad_stats = edit(setv(("daily", 4, "starts"), 3), last=(today - dt.timedelta(days=1)).isoformat(), as_of=fresh)
    rc, c, s_, sl, text = go([good_counts], [good_stats])
    out.append(("run: both good: both written, exit 0", rc == 0 and c == good_counts and s_ == good_stats and sl == [], text))
    rc, c, s_, sl, text = go([good_counts], [good_counts])
    out.append(("run: not redeployed (?stats=1 answers the counts payload): counts written, no stats file, exit 0, said so",
                rc == 0 and c == good_counts and s_ is None and "stats endpoint not deployed yet" in text, text))
    rc, c, s_, sl, text = go([good_counts], [bad_stats])
    out.append(("run: a stats payload with a count of 3: counts still written, no stats file, exit 1",
                rc == 1 and c == good_counts and s_ is None and "FAIL ugh stats" in text, text))
    rc, c, s_, sl, text = go([good_counts], [{"error": "the \"GA4 country daily\" tab's columns are [...]"}])
    out.append(("run: the stats endpoint answers {error}: counts still written, no stats file, exit 1, the error shown",
                rc == 1 and c == good_counts and s_ is None and "answered an error" in text and "GA4 country daily" in text, text))
    rc, c, s_, sl, text = go([dict(good_counts, total=6)], [good_stats])
    out.append(("run: a counts payload whose total is not the sum: no counts file, stats still written, exit 1",
                rc == 1 and c is None and s_ == good_stats and "not the sum" in text, text))
    rc, c, s_, sl, text = go([err, err, err, err], [good_stats])
    out.append(("run: the counts fetch fails four times (1, 5, 15 minutes): the stats get one attempt, are written, exit 1",
                rc == 1 and c is None and s_ == good_stats and sl == [60, 300, 900], text))
    rc, c, s_, sl, text = go([err, err, good_counts], [err, good_stats])
    out.append(("run: the two fetches share the one retry sequence (counts use 1 and 5 minutes, the stats the 15)",
                rc == 0 and c == good_counts and s_ == good_stats and sl == [60, 300, 900], "%s %s" % (sl, text)))
    rc, c, s_, sl, text = go([err, err, good_counts], [err, err])
    out.append(("run: the stats fetch out of retries: counts written, no stats file, exit 1, never more than 21 minutes of pauses",
                rc == 1 and c == good_counts and s_ is None and sl == [60, 300, 900] and "could not fetch the stats" in text, "%s %s" % (sl, text)))
    rc, c, s_, sl, text = go([good_counts], [err, err, err, good_stats])
    out.append(("run: the stats fetch alone retries after 1, 5 and 15 minutes", rc == 0 and s_ == good_stats and sl == [60, 300, 900], "%s %s" % (sl, text)))
    out.append(("address: ?stats=1 on the endpoint, &stats=1 where it already has a query",
                stats_url(ENDPOINT) == ENDPOINT + "?stats=1" and stats_url("http://x/exec?a=1") == "http://x/exec?a=1&stats=1", stats_url(ENDPOINT)))
    return out


def selftest():
    now = dt.datetime(2026, 10, 23, 5, 30, tzinfo=dt.timezone.utc)
    good = {"as_of": "2026-10-23T06:30:12+01:00", "since": "2026-09-01", "total": 5, "games": {"a": 2, "b": 3}}

    def with_(**kw):
        d = json.loads(json.dumps(good)); d.update(kw); return d

    def drop(k):
        d = json.loads(json.dumps(good)); del d[k]; return d
    cases = [
        ("clean payload", good, None),
        ("extra key", with_(version="x"), "keys are"),
        ("missing key", drop("games"), "keys are"),
        ("not an object", [1], "not an object"),
        ("as_of not ISO", with_(as_of="yesterday"), "ISO time"),
        ("as_of yesterday", with_(as_of="2026-10-22T06:30:12+01:00"), "not today"),
        ("as_of null (first count unfinished)", with_(as_of=None), "ISO time"),
        ("since wrong year", with_(since="2025-09-01"), "since is"),
        ("float count", with_(games={"a": 2.5, "b": 3}, total=5.5), "not whole"),
        ("string count", with_(games={"a": "2", "b": 3}), "not whole"),
        ("boolean count", with_(games={"a": True, "b": 3}, total=4), "not whole"),
        ("negative count", with_(games={"a": -1, "b": 6}), "not whole"),
        ("unknown slug is counted, not rejected", with_(games={"a": 2, "zzz": 3}), None),
        ("empty slug", with_(games={"a": 2, "": 3}), "not non-empty text"),
        ("unknown slug but total not the sum", with_(games={"a": 2, "zzz": 3}, total=4), "not the sum"),
        ("total not the sum", with_(total=6), "not the sum"),
        ("total a string", with_(total="5"), "total"),
    ]
    bad = []
    for name, obj, want in cases:
        got = validate(obj, now)
        ok = (not got) if want is None else any(want in g for g in got)
        print("  %s  %-38s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(valid)"))
        if not ok:
            bad.append(name)
    # London dates around the clock change and midnight
    edge = [(dt.datetime(2026, 10, 23, 23, 30, tzinfo=dt.timezone.utc), dt.date(2026, 10, 24)),     # BST: 00:30 next day
            (dt.datetime(2026, 12, 1, 23, 30, tzinfo=dt.timezone.utc), dt.date(2026, 12, 1)),       # GMT
            (dt.datetime(2026, 10, 25, 0, 30, tzinfo=dt.timezone.utc), dt.date(2026, 10, 25)),
            (dt.datetime(2026, 3, 29, 0, 30, tzinfo=dt.timezone.utc), dt.date(2026, 3, 29))]
    for n, want in edge:
        ok = london_date(n) == want
        print("  %s  london_date(%s) = %s" % ("PASS" if ok else "FAIL", n.isoformat(), london_date(n)))
        if not ok:
            bad.append("london_date " + n.isoformat())
    ok = school_year_start(dt.date(2027, 8, 31)) == dt.date(2026, 9, 1) and school_year_start(dt.date(2027, 9, 1)) == dt.date(2027, 9, 1)
    print("  %s  school_year_start on 31 Aug and 1 Sep" % ("PASS" if ok else "FAIL"))
    if not ok:
        bad.append("school_year_start")
    # The offset forms (26 Oct 2026: the Apps Script writes Z while London is on GMT, and the validator rejected it): Z, +00:00 and
    # +01:00 are all valid, and the exact payload that failed the 26 Oct 11:31 run is valid at the time it was fetched.
    exact = {"as_of": "2026-10-26T11:31:31Z", "since": "2026-09-01", "total": 5, "games": {"a": 2, "b": 3}}
    t26 = dt.datetime(2026, 10, 26, 11, 40, tzinfo=dt.timezone.utc)
    t23 = dt.datetime(2026, 10, 23, 5, 30, tzinfo=dt.timezone.utc)
    t24 = dt.datetime(2026, 10, 23, 23, 10, tzinfo=dt.timezone.utc)      # 00:10 on 24 Oct in London
    forms = [
        ("as_of Z: the exact 26 Oct payload", exact, t26, None),
        ("as_of +01:00 (summer)", with_(as_of="2026-10-23T06:30:12+01:00"), t23, None),
        ("as_of +00:00", with_(as_of="2026-10-23T05:30:12+00:00"), t23, None),
        ("as_of Z in summer, the same London day", with_(as_of="2026-10-23T05:30:12Z"), t23, None),
        ("as_of Z across London midnight (23:05Z is 00:05 on 24 Oct)", with_(as_of="2026-10-23T23:05:00Z"), t24, None),
        ("as_of Z yesterday", with_(as_of="2026-10-25T11:31:31Z"), t26, "not today"),
        ("as_of lower-case z", with_(as_of="2026-10-26T11:31:31z"), t26, "ISO time"),
        ("as_of +0100 (no colon)", with_(as_of="2026-10-26T11:31:31+0100"), t26, "ISO time"),
        ("as_of with no offset", with_(as_of="2026-10-26T11:31:31"), t26, "ISO time"),
    ]
    for name, obj, at, want in forms:
        got = validate(obj, at)
        ok = (not got) if want is None else any(want in g for g in got)
        print("  %s  %-58s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(valid)"))
        if not ok:
            bad.append(name)
    # the file's age, read from any offset: a stale file is caught (the planted file is 30 hours old)
    fresh_cases = [
        ("fresh: Z, 23 hours old", exact, dt.datetime(2026, 10, 27, 10, 31, tzinfo=dt.timezone.utc), None),
        ("fresh: +01:00, 5 hours old", with_(as_of="2026-10-23T06:30:12+01:00"), dt.datetime(2026, 10, 23, 10, 30, tzinfo=dt.timezone.utc), None),
        ("stale: the exact 26 Oct payload, 24.5 hours old", exact, dt.datetime(2026, 10, 27, 12, 1, tzinfo=dt.timezone.utc), "hours old"),
        ("stale: +01:00, 30 hours old", with_(as_of="2026-10-24T20:46:04+01:00"), dt.datetime(2026, 10, 26, 1, 46, tzinfo=dt.timezone.utc), "hours old"),
        ("stale: Z, the planted 30-hour-old file", with_(as_of="2026-10-25T10:00:00Z"), dt.datetime(2026, 10, 26, 16, 0, tzinfo=dt.timezone.utc), "hours old"),
        ("stale: unreadable as_of (age unknown)", with_(as_of="yesterday"), t26, "age is unknown"),
        ("stale: as_of null", with_(as_of=None), t26, "age is unknown"),
        ("stale: as_of in the future", with_(as_of="2026-10-26T20:00:00Z"), t26, "future"),
    ]
    for name, obj, at, want in fresh_cases:
        got = stale_faults(obj, at)
        ok = (not got) if want is None else any(want in g for g in got)
        print("  %s  %-58s %s" % ("PASS" if ok else "FAIL", name, got[0] if got else "(fresh)"))
        if not ok:
            bad.append(name)
    # The total never falls (same school year): a lower total than the published file fails; equal, higher, a new year and no file pass.
    prevf = with_(total=10, games={"a": 4, "b": 6}, as_of="2026-10-22T06:30:12+01:00")
    low = with_(total=9, games={"a": 4, "b": 5})
    for name, obj, pv, want in [
        ("total lower than the previous file's", low, prevf, "below the published file"),
        ("total equal to the previous file's", with_(total=10, games={"a": 4, "b": 6}), prevf, None),
        ("total higher than the previous file's", with_(total=11, games={"a": 4, "b": 7}), prevf, None),
        ("lower total in a new school year (since differs)", low, dict(prevf, since="2025-09-01"), None),
        ("no previous file", low, None, None),
    ]:
        got = validate(obj, now, prev=pv)
        ok = (not got) if want is None else any(want in g for g in got)
        print("  %s  %-58s %s" % ("PASS" if ok else "FAIL", name, got[0][:90] if got else "(valid)"))
        if not ok:
            bad.append(name)
    retry_cases = retry_selftest()
    for name, ok in retry_cases:
        print("  %s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            bad.append(name)
    stats_cases = stats_selftest()
    for name, ok, detail in stats_cases:
        # a validator case shows the fault it raised; a run() case shows its captured output only when it fails
        print("  %s  %-58s %s" % ("PASS" if ok else "FAIL", name, detail if not ok or name.startswith("stats") else ""))
        if not ok:
            bad.append(name)
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS",
                                       len(cases) + len(edge) + 1 + len(forms) + len(fresh_cases) + 5 + len(retry_cases) + len(stats_cases)))
    return 1 if bad else 0


def fetch_counts(url, pauses, used, out=OUT):
    """Fetch the counts, validate them and write answer-counts.json. Returns 0 (written) or 1 (not written)."""
    try:
        obj = fetch(url, pauses, used)
    except RuntimeError as exc:
        print("FAIL", exc)
        print("answer counts: NOT written (the file on main is unchanged)")
        return 1
    try:
        prev = json.loads(out.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        prev = None
    faults = validate(obj, prev=prev)
    if faults:
        for f in faults:
            print("FAIL", f)
        print("answer counts: NOT written (the file on main is unchanged)")
        return 1
    write(obj, out)
    over = sum(1 for v in obj["games"].values() if v >= 1000)
    print("answer counts: written, total %d, %d game(s) at 1,000 or more, as_of %s" % (obj["total"], over, obj["as_of"]))
    return 0


def run(url=ENDPOINT, pauses=RETRY_PAUSES_S, out=OUT, stats_out=STATS_OUT):
    """The daily job: the counts, then the stats, each fetched, validated and written on its own. 1 if either was not written."""
    used = []
    counts = fetch_counts(url, pauses, used, out)
    stats = fetch_stats(url, pauses[len(used):], stats_out)
    return 1 if counts or stats else 0


def check_stats_file(path=STATS_OUT):
    """--check for ugh-stats.json: the faults in the committed file. No file yet is not a fault: only the workflow writes
    it, and it writes none until the counts script is redeployed with the stats."""
    if not path.exists():
        print("ugh stats file: not published yet (the workflow writes it once the counts script answers ?stats=1)")
        return []
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        obj, faults = {}, ["not JSON: %s" % exc]
    else:
        faults = validate_stats(obj, require_today=False)
    for f in faults:
        print("FAIL ugh stats:", f)
    print("ugh stats file: %s (%s days, as_of %s)" % ("FAIL" if faults else "PASS",
          len(obj.get("daily", [])) if isinstance(obj, dict) and isinstance(obj.get("daily"), list) else "?", obj.get("as_of") if isinstance(obj, dict) else None))
    return faults


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true", help="validate schools/assets/answer-counts.json and ugh-stats.json as committed (as_of may be older)")
    ap.add_argument("--url", default=ENDPOINT, help="fetch from this address instead (for the planted-failure test only)")
    ap.add_argument("--pauses", default=None, help="comma-separated seconds between attempts, instead of 60,300,900 (for the planted-failure test only)")
    ap.add_argument("--fresh", action="store_true", help="with --check: also fail when as_of is over 24 hours old (always on in a scheduled run)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.check:
        obj = json.loads(OUT.read_text(encoding="utf-8"))
        faults = validate(obj, require_today=False)
        # The weekly site check (a scheduled run) holds the file to 24 hours; a push or a PR must not go red because the daily
        # job is behind, so it does not (the daily watch in scheduled-watch.yml is what raises that).
        if a.fresh or os.environ.get("GITHUB_EVENT_NAME") == "schedule":
            faults += stale_faults(obj)
        for f in faults:
            print("FAIL", f)
        print("answer counts file: %s (total %s over %d games, as_of %s)" % (
            "FAIL" if faults else "PASS", obj.get("total"), len(obj.get("games", {})), obj.get("as_of")))
        return 1 if faults + check_stats_file() else 0
    return run(a.url, tuple(int(x) for x in a.pauses.split(",")) if a.pauses else RETRY_PAUSES_S)


if __name__ == "__main__":
    sys.exit(main())
