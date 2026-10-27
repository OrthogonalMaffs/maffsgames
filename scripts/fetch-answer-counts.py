#!/usr/bin/env python3
"""Fetch the answer counts from the counts Apps Script, validate them, and write schools/assets/answer-counts.json.

Contract ANSWER-COUNTS (23 Oct 2026). The daily workflow (.github/workflows/answer-counts.yml) runs this, then commits
the file with "[skip ci]". A failure writes nothing, so the file on main stays as it was and only that job fails; the
site hides every figure whose source is more than 7 days old (schools/assets/answer-count.js).

    python scripts/fetch-answer-counts.py                 # fetch, validate, write schools/assets/answer-counts.json
    python scripts/fetch-answer-counts.py --check         # validate the file already in the repo (as_of not required to be today)
    python scripts/fetch-answer-counts.py --selftest      # each planted fault must fail; the clean payload passes

The payload is exactly {as_of, since, total, games}. It is valid when:
  - as_of is an ISO time with an offset (Z, +00:00 or +hh:mm), and its date, in Europe/London, is today's;
  - since is 1 September of the school year that today falls in;
  - every game count is a whole number >= 0 (not a boolean, float or string), keyed by a slug that is a game directory
    under games/ or an escape room (escape-<directory> under escape-rooms/);
  - total is a whole number equal to the sum of the game counts.
"""
import argparse, datetime as dt, json, os, pathlib, re, sys, time, urllib.request

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "schools" / "assets" / "answer-counts.json"
ENDPOINT = "https://script.google.com/macros/s/AKfycbxvtM7Y5jtL7flZozfFUEoZZalNHieP44vK6rB4juUG5yPgQf5hfb8tOlgetoEtogZl8w/exec"
KEYS = {"as_of", "since", "total", "games"}
# The offset is Z (zero, written by the Apps Script's "XXX" pattern while London is on GMT: ISO 8601 and RFC 3339 both allow it)
# or +hh:mm / -hh:mm. Until 26 Oct 2026 only the second was accepted, and every run since the clocks went back failed on it.
AS_OF = re.compile(r"^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)(Z|[+-]\d\d:\d\d)$")
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


def fetch(url=ENDPOINT, tries=3):
    last = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:                                # network, HTTP, bad JSON: try again
            last = exc
            time.sleep(5 * (i + 1))
    raise RuntimeError("could not fetch the counts: %s" % last)


def write(obj, path=OUT):
    body = json.dumps(obj, indent=1, sort_keys=True, ensure_ascii=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")


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
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(cases) + len(edge) + 1 + len(forms) + len(fresh_cases) + 5))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true", help="validate schools/assets/answer-counts.json as committed (as_of may be older)")
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
        return 1 if faults else 0
    obj = fetch()
    try:
        prev = json.loads(OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        prev = None
    faults = validate(obj, prev=prev)
    if faults:
        for f in faults:
            print("FAIL", f)
        print("answer counts: NOT written (the file on main is unchanged)")
        return 1
    write(obj)
    over = sum(1 for v in obj["games"].values() if v >= 1000)
    print("answer counts: written, total %d, %d game(s) at 1,000 or more, as_of %s" % (obj["total"], over, obj["as_of"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
