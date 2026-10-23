#!/usr/bin/env python3
# ci-line: Answer counts file (the validator that guards data/answer-counts.json: schema, roster slugs, whole numbers, total = sum, as_of today) | --selftest
"""Fetch the answer counts from the counts Apps Script, validate them, and write data/answer-counts.json.

Contract ANSWER-COUNTS (23 Oct 2026). The daily workflow (.github/workflows/answer-counts.yml) runs this, then commits
the file with "[skip ci]". A failure writes nothing, so the file on main stays as it was and only that job fails; the
site hides every figure whose source is more than 7 days old (schools/assets/answer-count.js).

    python scripts/fetch-answer-counts.py                 # fetch, validate, write data/answer-counts.json
    python scripts/fetch-answer-counts.py --check         # validate the file already in the repo (as_of not required to be today)
    python scripts/fetch-answer-counts.py --selftest      # each planted fault must fail; the clean payload passes

The payload is exactly {as_of, since, total, games}. It is valid when:
  - as_of is an ISO time with an offset, and its date, in Europe/London, is today's;
  - since is 1 September of the school year that today falls in;
  - every game count is a whole number >= 0 (not a boolean, float or string), keyed by a slug that is a game directory
    under games/ or an escape room (escape-<directory> under escape-rooms/);
  - total is a whole number equal to the sum of the game counts.
"""
import argparse, datetime as dt, json, pathlib, re, sys, time, urllib.request

BASE = pathlib.Path(__file__).resolve().parent.parent
OUT = BASE / "data" / "answer-counts.json"
ENDPOINT = "https://script.google.com/macros/s/AKfycbxvtM7Y5jtL7flZozfFUEoZZalNHieP44vK6rB4juUG5yPgQf5hfb8tOlgetoEtogZl8w/exec"
KEYS = {"as_of", "since", "total", "games"}
AS_OF = re.compile(r"^(\d{4})-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)([+-])(\d\d):(\d\d)$")


def slugs(root=BASE):
    s = {p.name for p in (root / "games").iterdir() if p.is_dir()}
    s |= {"escape-" + p.name for p in (root / "escape-rooms").iterdir() if p.is_dir() and (p / "room.js").exists()}
    return s


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


def validate(obj, allowed, now_utc=None, require_today=True):
    """The faults in a payload (empty list = valid)."""
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
        got = dt.date(int(m[1]), int(m[2]), int(m[3]))
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
    bad = sorted(k for k in games if not isinstance(k, str) or k not in allowed)
    if bad:
        f.append("slugs not on the roster: %s" % ", ".join(map(str, bad)))
    nonwhole = sorted(k for k, v in games.items() if not is_whole(v))
    if nonwhole:
        f.append("counts that are not whole numbers >= 0: %s" % ", ".join("%s=%r" % (k, games[k]) for k in nonwhole))
    total = obj.get("total")
    if not is_whole(total):
        f.append("total %r is not a whole number >= 0" % (total,))
    elif not nonwhole and total != sum(games.values()):
        f.append("total %d is not the sum of the games (%d)" % (total, sum(games.values())))
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
    allowed = {"a", "b", "escape-x"}
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
        ("slug off the roster", with_(games={"a": 2, "zzz": 3}), "not on the roster"),
        ("total not the sum", with_(total=6), "not the sum"),
        ("total a string", with_(total="5"), "total"),
    ]
    bad = []
    for name, obj, want in cases:
        got = validate(obj, allowed, now)
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
    print("selftest: %s (%d cases)" % ("FAILED: " + ", ".join(bad) if bad else "PASS", len(cases) + len(edge) + 1))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--check", action="store_true", help="validate data/answer-counts.json as committed (as_of may be older)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    allowed = slugs()
    if a.check:
        obj = json.loads(OUT.read_text(encoding="utf-8"))
        faults = validate(obj, allowed, require_today=False)
        for f in faults:
            print("FAIL", f)
        print("answer counts file: %s (total %s over %d games, as_of %s)" % (
            "FAIL" if faults else "PASS", obj.get("total"), len(obj.get("games", {})), obj.get("as_of")))
        return 1 if faults else 0
    obj = fetch()
    faults = validate(obj, allowed)
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
