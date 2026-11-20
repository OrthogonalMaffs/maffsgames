#!/usr/bin/env python3
"""Counting Players: the Core Maths practice pack's three PDFs, from text.md and two frozen CSVs (contract COUNTING-PLAYERS, 20 Nov 2026).

Reads core-maths/counting-players/maffsgames-site-data-sep-nov-2026.csv (GA4) and
maffsgames-game-records-sep-nov-2026.csv (the site's own game records), and tools/counting-players/text.md, the text
Project Claude wrote and Jon approved (20 Nov 2026), with {{key}} placeholders, a Values table and a Conditions list.

It FAILS (exit 1, "BUILD FAILED", every fault listed) when:
  - any key in text.md's Values table, computed here from its definition, differs from the table's value (the line
    names the key, the computed value and the table's value);
  - any of text.md's Conditions is false (named by number), or a table's stated order is not the data's;
  - a placeholder is left unfilled ({{ in the output), or names a key the Values table does not hold;
  - the paper's marks do not add to the cover's maximum, or the mark scheme's totals differ from the paper's.
Otherwise it fills PRELIMINARY MATERIAL, PRACTICE PAPER and MARK SCHEME word for word, draws CHART 1 (deliberately
imperfect, as text.md says), CHART 2 and the 3 (a) box-plot grid as SVG, and prints three A4 PDFs in Chromium,
black on white, in Outfit and JetBrains Mono served from the repo's pinned copies (scripts/fonts/), with text.md's
footer and the page number on every page (tools/maffscards/build_pdf.py's route). Nothing reaches the network.

    python -X utf8 tools/counting-players/build.py            # writes the three PDFs into core-maths/counting-players/
    python -X utf8 tools/counting-players/build.py --check    # every computation and condition; writes nothing

Exact arithmetic (fractions); rounding is half up. Lines of text.md that tell the builder what to draw ("(columns:
...)", "Line above the table:", "Note under the table:", "Cover page:", "(Provide a grid from 0 to 180.)", a chart's
description) are layout, not printed; the text they introduce is. scripts/check-counting-players.py runs --check in CI.
"""
import argparse
import collections
import csv
import datetime as dt
import fractions
import html
import math
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
TEXT = HERE / "text.md"
DATA = ROOT / "core-maths" / "counting-players"


class BuildError(Exception):
    pass


# ================================================================================================ the values
F = fractions.Fraction
MINUS = "−"

SITE_NAME = "maffsgames-site-data-sep-nov-2026.csv"
GAMES_NAME = "maffsgames-game-records-sep-nov-2026.csv"
SITE_COLS = ["date", "source", "medium", "device", "landing_page", "sessions", "engaged_sessions", "active_users"]
GAMES_COLS = ["date", "game", "games_started", "answers_marked", "answers_correct"]

START, END = dt.date(2026, 9, 20), dt.date(2026, 11, 19)
WEEK5 = (dt.date(2026, 11, 13), dt.date(2026, 11, 19))           # TABLE 5
CHART2 = (dt.date(2026, 10, 20), dt.date(2026, 11, 19))          # CHART 2
MEDIUMS = [("organic", "organic"), ("none", "(none)"), ("referral", "referral"), ("ai", "ai-assistant"),
           ("notset", "(not set)"), ("cpc", "cpc")]
DEVICES = ["desktop", "mobile", "tablet"]
PLATFORMS = [("classroom", ["classroom.google.com"]), ("a", ["school platform A"]),
             ("onenote", ["euc-onenote.officeapps.live.com"]),
             ("teams", ["teams.public.onecdn.static.microsoft", "statics.teams.cdn.office.net"]),
             ("c", ["school platform C"]), ("b", ["school platform B"])]
ANON = {"school platform A", "school platform B", "school platform C"}
# Condition 11 / the CSV check. Every source must be one of these: general sites and tools, none of them a single
# school, college or other institution. A new source (a second edition's data) fails until a person has looked at it
# and either added it here or anonymised it as school platform A, B or C.
KNOWN_SOURCES = {
    "google", "(direct)", "bing", "facebook.com", "chatgpt.com", "m.facebook.com", "classroom.google.com",
    "euc-onenote.officeapps.live.com", "lm.facebook.com", "ecosia.org", "teams.public.onecdn.static.microsoft",
    "(not set)", "l.facebook.com", "linkedin.com", "yahoo", "gemini.google.com", "duckduckgo", "openai",
    "uk.search.yahoo.com", "perplexity.ai", "mathswins.co.uk", "mail.google.com", "iframely.net",
    "statics.teams.cdn.office.net",
}
INSTITUTION = re.compile(r"school|college|academy|universit|\.sch\b|sch\.uk|\.ac\.uk|\.edu\b|\btrust\b|grammar|"
                         r"\.gov\b|council|\bfe\b|sixth.?form", re.I)
QUERY_KEYS = {"level", "game", "type", "mode", "topic"}


class DataError(Exception):
    pass


# ------------------------------------------------------------------------------------------------ formatting
def rnd(x, dp=0):
    """x (a Fraction) rounded half up (away from zero on a tie) to dp places, as a Fraction."""
    q = 10 ** dp
    m = abs(F(x)) * q
    n = math.floor(m + F(1, 2))
    return F(n if x >= 0 else -n, q)


def thou(n):
    s = "{:,}".format(abs(int(n)))
    return (MINUS if n < 0 else "") + s


def fixed(x, dp):
    """x to exactly dp decimal places, thousands with a comma, U+2212 for a minus."""
    r = rnd(x, dp)
    neg = r < 0
    r = abs(r)
    whole = int(r)
    frac = r - whole
    s = "{:,}".format(whole)
    if dp:
        s += "." + str(int(frac * 10 ** dp)).rjust(dp, "0")
    return (MINUS if neg else "") + s


def num(x, dp=1):
    """A count or a rate: no decimals when whole, else dp places (quartiles: as many as they need, at most 2)."""
    x = F(x)
    if x.denominator == 1:
        return thou(x)
    for d in range(1, 3):
        if (x * 10 ** d).denominator == 1:
            return fixed(x, d)
    return fixed(x, dp)


def pct(a, b, dp=1):
    return F(a) * 100 / F(b) if dp is None else rnd(F(a) * 100 / F(b), dp)


# ------------------------------------------------------------------------------------------------ reading
def read_csv(path, cols):
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
        fh.seek(0)
        header = next(csv.reader(fh))
    if header != cols:
        raise DataError("%s: columns %s, expected %s" % (path.name, header, cols))
    return rows


def load(folder):
    folder = pathlib.Path(folder)
    site = read_csv(folder / SITE_NAME, SITE_COLS)
    games = read_csv(folder / GAMES_NAME, GAMES_COLS)
    for r in site:
        r["d"] = dt.date.fromisoformat(r["date"])
        for k in ("sessions", "engaged_sessions", "active_users"):
            r[k] = int(r[k])
    for r in games:
        r["d"] = dt.date.fromisoformat(r["date"])
        for k in ("games_started", "answers_marked", "answers_correct"):
            r[k] = int(r[k])
    return site, games


def quartiles_inc(xs):
    """QUARTILE.INC: linear interpolation at (n - 1) * p."""
    xs = sorted(xs)
    out = []
    for p in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
        h = (len(xs) - 1) * p
        lo = math.floor(h)
        hi = min(lo + 1, len(xs) - 1)
        out.append(xs[lo] + (h - lo) * (xs[hi] - xs[lo]))
    return out


def days(a, b):
    return [a + dt.timedelta(n) for n in range((b - a).days + 1)]


def monday(d):
    return d - dt.timedelta(d.weekday())


# ------------------------------------------------------------------------------------------------ computing
def compute(site, games):
    """Returns (values, facts): values maps each key to the string the text shows; facts holds what the tables,
    charts and conditions need."""
    v, f = {}, {}
    window = days(START, END)
    for r in site:
        if not START <= r["d"] <= END:
            raise DataError("site data row dated %s is outside the window" % r["date"])
    S = lambda rows: sum(r["sessions"] for r in rows)
    E = lambda rows: sum(r["engaged_sessions"] for r in rows)
    v["days"] = thou(len(window))
    v["rows"] = thou(len(site))
    sessions, engaged = S(site), E(site)
    v["sessions"], v["engaged"] = thou(sessions), thou(engaged)

    by_med = {}
    for key, med in MEDIUMS:
        rows = [r for r in site if r["medium"] == med]
        by_med[key] = (S(rows), E(rows))
        v["m_%s_s" % key], v["m_%s_e" % key] = thou(by_med[key][0]), thou(by_med[key][1])
    f["medium_other"] = sorted({r["medium"] for r in site} - {m for _, m in MEDIUMS})
    f["by_med"] = by_med

    by_dev = {}
    for dev in DEVICES:
        rows = [r for r in site if r["device"] == dev]
        by_dev[dev] = (S(rows), E(rows))
        v["d_%s_s" % dev], v["d_%s_e" % dev] = thou(by_dev[dev][0]), thou(by_dev[dev][1])
    f["device_other"] = sorted({r["device"] for r in site} - set(DEVICES))

    mon = {m: S([r for r in site if r["d"].month == m]) for m in (9, 10, 11)}
    v["mon_sep"], v["mon_oct"], v["mon_nov"] = thou(mon[9]), thou(mon[10]), thou(mon[11])

    plat = {}
    for key, srcs in PLATFORMS:
        rows = [r for r in site if r["source"] in srcs]
        seen = {r["d"] for r in rows if r["sessions"] > 0}
        plat[key] = (S(rows), E(rows), len(seen))
        v["p_%s_s" % key], v["p_%s_e" % key], v["p_%s_d" % key] = (thou(x) for x in plat[key])
    f["plat"] = plat

    weeks = sorted({monday(d) for d in window})
    v["weeks"] = thou(len(weeks))
    per_day = {d: 0 for d in window}
    for r in site:
        per_day[r["d"]] += r["sessions"]
    f["per_day"] = per_day
    wk = []
    for m in weeks:
        ds = [d for d in days(m, m + dt.timedelta(6)) if START <= d <= END]
        wk.append({"monday": m, "days": len(ds), "sessions": sum(per_day[d] for d in ds)})
    f["weeks"] = wk

    eng = pct(engaged, sessions)
    v["eng_pct"] = fixed(eng, 1)
    mob = pct(*by_dev["mobile"][::-1])
    desk = pct(*by_dev["desktop"][::-1])
    v["mob_pct"], v["mob_pct_whole"] = fixed(mob, 1), fixed(pct(*by_dev["mobile"][::-1], dp=0), 0)
    v["desk_pct"] = fixed(desk, 1)
    v["desk_mob_gap"] = fixed(desk - mob, 1)
    f["mob"], f["desk"] = mob, desk

    change = F(mon[11] - mon[10]) * 100 / mon[10]
    v["sam_change_signed"] = fixed(change, 1)
    v["sam_fall"] = fixed(abs(change), 0)
    oct_rate, nov_rate = F(mon[10], 31), F(mon[11], 19)
    v["oct_rate"], v["nov_rate"] = fixed(oct_rate, 1), fixed(nov_rate, 1)
    v["rate_change"] = fixed((nov_rate / oct_rate - 1) * 100, 1)
    v["rate_change_lo"] = fixed((rnd(nov_rate, 1) / rnd(oct_rate, 1) - 1) * 100, 1)
    v["rate_change_hi"] = v["rate_change"]
    f.update(mon=mon, oct_rate=oct_rate, nov_rate=nov_rate)

    wd = [per_day[d] for d in window if d.weekday() < 5]
    we = [per_day[d] for d in window if d.weekday() >= 5]
    stats = {}
    for pre, xs in (("wd", wd), ("we", we)):
        mn, lq, med, uq, mx = quartiles_inc(xs)
        stats[pre] = dict(n=len(xs), min=mn, lq=lq, med=med, uq=uq, max=mx, iqr=uq - lq)
        for k in ("n", "min", "lq", "med", "uq", "max", "iqr"):
            v["%s_%s" % (pre, k)] = num(stats[pre][k])
    f["stats"] = stats

    v["users_sum"] = thou(sum(r["active_users"] for r in site))

    by_src = collections.Counter()
    for r in site:
        by_src[r["source"]] += r["sessions"]
    f["by_src"] = by_src
    google_s = by_src["google"]
    gp = pct(google_s, sessions)
    v["google_s"], v["google_pct"] = thou(google_s), fixed(gp, 1)
    v["google_pct_lo"], v["google_pct_hi"] = fixed(gp - F(1, 10), 1), fixed(gp + F(1, 10), 1)
    f["google_pct"] = gp
    v["organic_pct"] = fixed(pct(by_med["organic"][0], sessions), 1)
    v["none_pct"] = fixed(pct(by_med["none"][0], sessions), 1)

    v["first_week_days"], v["last_week_days"] = thou(wk[0]["days"]), thou(wk[-1]["days"])
    last_rate = F(wk[-1]["sessions"], wk[-1]["days"])
    v["last_week_s"], v["last_week_rate"] = thou(wk[-1]["sessions"]), num(rnd(last_rate, 1))
    complete = [w for w in wk if w["days"] == 7]
    best = max(complete, key=lambda w: w["sessions"])
    best_rate = F(best["sessions"], 7)
    v["best_week_rate"], v["best_week_label"] = fixed(best_rate, 1), best["monday"].strftime("%d/%m")
    f.update(last_rate=last_rate, best_rate=best_rate)

    cpc = [r for r in site if r["medium"] == "cpc"]
    f["cpc"] = cpc
    v["cpc_s"] = thou(S(cpc))
    d1 = [r for r in cpc if r["d"] == dt.date(2026, 10, 7)]
    d2 = [r for r in cpc if r["d"] == dt.date(2026, 10, 16)]
    v["cpc_day1_s"], v["cpc_day1_u"] = thou(S(d1)), thou(sum(r["active_users"] for r in d1))
    v["cpc_day2_s"] = thou(S(d2))

    teams_pct = pct(plat["teams"][1], plat["teams"][0], dp=0)
    a_pct = pct(plat["a"][1], plat["a"][0], dp=0)
    v["teams_pct"], v["a_pct"] = fixed(teams_pct, 0), fixed(a_pct, 0)
    f.update(teams_pct=teams_pct, a_pct=a_pct)

    # ---------------------------------------------------------------- game records
    wkrows = [r for r in games if WEEK5[0] <= r["d"] <= WEEK5[1]]
    wk_ans = sum(r["answers_marked"] for r in wkrows)
    wk_cor = sum(r["answers_correct"] for r in wkrows)
    wk_overall = pct(wk_cor, wk_ans, dp=0)
    v["wk_answers"], v["wk_overall_pct"] = thou(wk_ans), fixed(wk_overall, 0)
    per_game = collections.defaultdict(lambda: [0, 0])
    for r in wkrows:
        per_game[r["game"]][0] += r["answers_marked"]
        per_game[r["game"]][1] += r["answers_correct"]
    t5 = [{"game": g, "answers": a, "correct": c, "acc": F(c * 100, a)} for g, (a, c) in per_game.items() if a >= 100]
    t5.sort(key=lambda t: (t["acc"], t["game"]))
    f["t5"] = t5
    v["t5_n"] = thou(len(t5))
    t5_sum = sum(rnd(t["acc"], 0) for t in t5)
    v["t5_sum"] = num(t5_sum)
    sam_mean = F(t5_sum, len(t5))
    v["sam_mean"], v["sam_mean_round"] = num(rnd(sam_mean, 1)), fixed(sam_mean, 0)
    t5a, t5c = sum(t["answers"] for t in t5), sum(t["correct"] for t in t5)
    pooled = pct(t5c, t5a, dp=None)
    v["t5_answers"], v["t5_correct"] = thou(t5a), thou(t5c)
    v["t5_pooled"], v["t5_pooled_lo"], v["t5_pooled_hi"] = fixed(pooled, 1), fixed(pooled, 1), fixed(pooled, 0)
    v["t5_left_n"] = thou(wk_ans - t5a)
    most = max(t5, key=lambda t: t["answers"])
    fewest = min(t5, key=lambda t: t["answers"])
    v["t5_max_game"], v["t5_max_n"] = most["game"], thou(most["answers"])
    v["t5_min_game"], v["t5_min_n"] = fewest["game"], thou(fewest["answers"])
    cc = per_game.get("escape-comic-caper", [0, 0])
    v["cc_pct"] = fixed(pct(cc[1], cc[0], dp=None), 1) if cc[0] else "none"
    v["cc_n"] = thou(cc[0])
    f.update(sam_mean_round=rnd(sam_mean, 0), wk_overall=wk_overall, pooled=pooled, wk_overall_exact=pct(wk_cor, wk_ans, None))

    daily = collections.defaultdict(lambda: [0, 0])
    for r in games:
        daily[r["d"]][0] += r["games_started"]
        daily[r["d"]][1] += r["answers_marked"]
    f["daily"] = daily
    g = lambda y, m, d: daily[dt.date(y, m, d)]
    v["nov2_g"] = thou(g(2026, 11, 2)[0])
    v["nov3_g"], v["nov3_q"] = thou(g(2026, 11, 3)[0]), thou(g(2026, 11, 3)[1])
    v["nov4_g"] = thou(g(2026, 11, 4)[0])
    v["oct23_g"], v["oct23_q"] = thou(g(2026, 10, 23)[0]), thou(g(2026, 10, 23)[1])
    v["nov3_ratio"] = fixed(F(g(2026, 11, 3)[1], g(2026, 11, 3)[0]), 1)
    v["oct23_ratio"] = fixed(F(g(2026, 10, 23)[1], g(2026, 10, 23)[0]), 1)
    c2 = days(*CHART2)
    f["chart2"] = [(d, daily[d][0], daily[d][1]) for d in c2]
    v["c2_mean"] = fixed(F(sum(daily[d][1] for d in c2), sum(daily[d][0] for d in c2)), 1)
    return v, f


# ------------------------------------------------------------------------------------------------ conditions
def source_problems(site):
    """Condition 11, and the CSV check: sources that may name a single institution."""
    bad = []
    for s in sorted({r["source"] for r in site}):
        if s in ANON:
            continue
        if INSTITUTION.search(s):
            bad.append("%s (looks like an institution)" % s)
        elif s not in KNOWN_SOURCES:
            bad.append("%s (not a reviewed source: anonymise it or add it to KNOWN_SOURCES after checking)" % s)
    return bad


def conditions(v, f, site):
    """[(number, text, holds)] for text.md's Conditions 1 to 11, plus the order the text states for its tables."""
    st, wk = f["stats"], f["weeks"]
    t5 = f["t5"]
    daily = f["daily"]
    g = lambda m, d: daily[dt.date(2026, m, d)][0]
    cpc = f["cpc"]
    out = [
        (1, "mon_nov < mon_oct, and nov_rate > oct_rate",
         f["mon"][11] < f["mon"][10] and f["nov_rate"] > f["oct_rate"]),
        (2, "desk_pct > mob_pct", rnd(f["desk"], 1) > rnd(f["mob"], 1)),
        (3, "every weekday statistic above its weekend counterpart; wd_med > 2 x we_med; wd_max <= 180",
         all(st["wd"][k] > st["we"][k] for k in ("n", "min", "lq", "med", "uq", "max"))
         and st["wd"]["med"] > 2 * st["we"]["med"] and st["wd"]["max"] <= 180),
        (4, "google_pct < 50; google is the source with the most sessions",
         rnd(f["google_pct"], 1) < 50 and f["by_src"].most_common(1)[0][0] == "google"
         and list(f["by_src"].values()).count(f["by_src"]["google"]) == 1),
        (5, "the last week has fewer sessions than the week before; last_week_rate > best_week_rate",
         wk[-1]["sessions"] < wk[-2]["sessions"] and f["last_rate"] > f["best_rate"]),
        (6, "all cpc rows: source google, device desktop, landing page /, engaged 0, dates only 2026-10-07 and 2026-10-16",
         bool(cpc) and all(r["source"] == "google" and r["device"] == "desktop" and r["landing_page"] == "/"
                           and r["engaged_sessions"] == 0 for r in cpc)
         and {r["date"] for r in cpc} <= {"2026-10-07", "2026-10-16"}),
        (7, "teams_pct < a_pct", f["teams_pct"] < f["a_pct"]),
        (8, "sam_mean_round = wk_overall_pct, and t5_pooled != wk_overall_pct to 1 d.p.",
         f["sam_mean_round"] == f["wk_overall"] and rnd(f["pooled"], 1) != rnd(f["wk_overall_exact"], 1)),
        (9, "escape-comic-caper is in TABLE 5 and has its lowest accuracy",
         any(t["game"] == "escape-comic-caper" for t in t5)
         and min(t5, key=lambda t: t["acc"])["game"] == "escape-comic-caper"
         and sum(1 for t in t5 if t["acc"] == min(x["acc"] for x in t5)) == 1),
        (10, "nov3_g > 10 x nov2_g; nov4_g < nov3_g / 2", g(11, 3) > 10 * g(11, 2) and F(g(11, 4)) < F(g(11, 3), 2)),
        (11, "no source names a school, college or other single institution, other than school platform A, B or C",
         not source_problems(site)),
    ]
    med = [f["by_med"][k][0] for k, _ in MEDIUMS]
    pl = [f["plat"][k][0] for k, _ in PLATFORMS]
    out += [
        ("TABLE 1", "mediums largest first, and no medium outside the six rows",
         med == sorted(med, reverse=True) and len(set(med)) == len(med) and not f["medium_other"]),
        ("TABLE 2", "no device outside desktop, mobile, tablet", not f["device_other"]),
        ("TABLE 4", "rows largest first by sessions", pl == sorted(pl, reverse=True) and len(set(pl)) == len(pl)),
        ("CHART 1", "the first label is 14 Sep and the last 16 Nov",
         wk[0]["monday"] == dt.date(2026, 9, 14) and wk[-1]["monday"] == dt.date(2026, 11, 16)),
        ("CHART 2", "31 days", len(f["chart2"]) == 31),
        ("Q2", "October has 31 days and November's data 19", END == dt.date(2026, 11, 19)),
    ]
    return out


# ------------------------------------------------------------------------------------------------ the Values table
# Each Key cell of text.md's Values table, and the keys it stands for, in the order of its Value cell.
KEY_CELLS = {
    "days": ["days"], "rows": ["rows"], "sessions, engaged": ["sessions", "engaged"],
    "m_*_s, m_*_e": [k % m for m, _ in MEDIUMS for k in ("m_%s_s", "m_%s_e")],
    "d_*_s, d_*_e": [k % d for d in DEVICES for k in ("d_%s_s", "d_%s_e")],
    "mon_sep, mon_oct, mon_nov": ["mon_sep", "mon_oct", "mon_nov"],
    "p_classroom_*": ["p_classroom_s", "p_classroom_e", "p_classroom_d"],
    "p_a_*": ["p_a_s", "p_a_e", "p_a_d"], "p_onenote_*": ["p_onenote_s", "p_onenote_e", "p_onenote_d"],
    "p_teams_*": ["p_teams_s", "p_teams_e", "p_teams_d"],
    "p_c_*, p_b_*": ["p_c_s", "p_c_e", "p_c_d", "p_b_s", "p_b_e", "p_b_d"],
    "weeks": ["weeks"], "eng_pct": ["eng_pct"], "mob_pct, mob_pct_whole": ["mob_pct", "mob_pct_whole"],
    "desk_pct": ["desk_pct"], "desk_mob_gap": ["desk_mob_gap"],
    "sam_change_signed, sam_fall": ["sam_change_signed", "sam_fall"], "oct_rate, nov_rate": ["oct_rate", "nov_rate"],
    "rate_change (lo, hi)": ["rate_change", "rate_change_lo", "rate_change_hi"],
    "wd_*, we_*": ["%s_%s" % (p, k) for p in ("wd", "we") for k in ("n", "min", "lq", "med", "uq", "max")],
    "wd_iqr, we_iqr": ["wd_iqr", "we_iqr"], "users_sum": ["users_sum"],
    "google_s, google_pct (lo, hi)": ["google_s", "google_pct", "google_pct_lo", "google_pct_hi"],
    "organic_pct": ["organic_pct"], "none_pct": ["none_pct"],
    "first_week_days, last_week_days": ["first_week_days", "last_week_days"],
    "last_week_s, last_week_rate": ["last_week_s", "last_week_rate"],
    "best_week_rate, best_week_label": ["best_week_rate", "best_week_label"], "cpc_s": ["cpc_s"],
    "cpc_day1_s, cpc_day1_u, cpc_day2_s": ["cpc_day1_s", "cpc_day1_u", "cpc_day2_s"],
    "teams_pct, a_pct": ["teams_pct", "a_pct"], "wk_answers, wk_overall_pct": ["wk_answers", "wk_overall_pct"],
    "t5_n": ["t5_n"], "t5_sum": ["t5_sum"], "sam_mean, sam_mean_round": ["sam_mean", "sam_mean_round"],
    "t5_answers, t5_correct, t5_pooled (lo, hi)": ["t5_answers", "t5_correct", "t5_pooled", "t5_pooled_lo",
                                                   "t5_pooled_hi"],
    "t5_left_n": ["t5_left_n"],
    "t5_max_game, t5_max_n, t5_min_game, t5_min_n": ["t5_max_game", "t5_max_n", "t5_min_game", "t5_min_n"],
    "cc_pct, cc_n": ["cc_pct", "cc_n"], "nov2_g, nov3_g, nov3_q, nov4_g": ["nov2_g", "nov3_g", "nov3_q", "nov4_g"],
    "oct23_g, oct23_q": ["oct23_g", "oct23_q"], "nov3_ratio, oct23_ratio": ["nov3_ratio", "oct23_ratio"],
    "c2_mean": ["c2_mean"],
}
TOKEN = re.compile(r"[−-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?|[−-]?\d+(?:\.\d+)?|[a-z][a-z0-9-]*")
SEMI_ROWS = {"best_week_rate, best_week_label"}           # a dd/mm date: split on ";" only


def values_table(text):
    """{key: value string} from text.md's Values table."""
    sec = text.split("## Values", 1)
    if len(sec) != 2:
        raise DataError("text.md has no Values section")
    body = sec[1].split("\n## ", 1)[0]
    out, cells = {}, []
    for line in body.splitlines():
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Key "):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) != 3:
            raise DataError("Values row with %d cells: %s" % (len(parts), line))
        cell, _defn, value = parts
        if cell not in KEY_CELLS:
            raise DataError("Values row %r is not one build.py knows" % cell)
        keys = KEY_CELLS[cell]
        toks = [t.strip() for t in value.split(";")] if cell in SEMI_ROWS else TOKEN.findall(value)
        if len(toks) != len(keys):
            raise DataError("Values row %r: %d values for %d keys (%s)" % (cell, len(toks), len(keys), value))
        out.update({k: t.replace("-", MINUS) if re.match(r"-\d", t) else t for k, t in zip(keys, toks)})
        cells.append(cell)
    missing = sorted(set(KEY_CELLS) - set(cells))
    if missing:
        raise DataError("Values rows missing from text.md: %s" % ", ".join(missing))
    return out


def mismatches(v, table):
    return [(k, v.get(k, "(not computed)"), table[k]) for k in table if v.get(k) != table[k]]


# ================================================================================================ the documents
esc = html.escape
PLACEHOLDER = re.compile(r"\{\{([a-z0-9_]+)\}\}")
FONTS = ("https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800"
         "&family=JetBrains+Mono:wght@400;500;700&display=swap")      # the query tools/maffscards pins (scripts/fonts/google)
DOCS = [("PRELIMINARY MATERIAL", "counting-players-preliminary-material.pdf", "Counting Players: Preliminary Material"),
        ("PRACTICE PAPER", "counting-players-practice-paper.pdf", "Counting Players: Practice Paper"),
        ("MARK SCHEME", "counting-players-mark-scheme.pdf", "Counting Players: Mark Scheme")]


def sections(text):
    """{name: body} for every '## ' section of text.md (a body ends at the next '---' rule or '## ')."""
    out = {}
    for chunk in re.split(r"\n## ", "\n" + text)[1:]:
        name, _, body = chunk.partition("\n")
        out[name.strip()] = re.split(r"\n---\s*\n", body)[0]
    return out


def footer_text(text):
    m = re.search(r"Footer on every page of all three PDFs: `([^`]+ · Page) n`", text)
    if not m:
        raise BuildError("text.md states no footer in the form `... · Page n`")
    return m.group(1)


def fill(line, v, used):
    """One line of text.md as HTML: escaped, every {{key}} filled, **bold** and *italic*. A key with no value is left
    as it was, so the leftover check names it."""
    def sub(m):
        k = m.group(1)
        if k not in v:
            return m.group(0)
        used.add(k)
        return v[k]
    s = PLACEHOLDER.sub(sub, line)
    s = esc(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"\bmaffsgames-[a-z0-9-]+\.csv\b", r'<span class="mono">\g<0></span>', s)   # file names in JetBrains Mono
    return s


def numeric(cell):
    return bool(re.fullmatch(r"[−\d.,%\s]+", cell))


def table_html(heads, rows, cls="", total_last=False):
    th = "".join('<th class="%s">%s</th>' % ("n" if i else "", h) for i, h in enumerate(heads))
    trs = []
    for j, r in enumerate(rows):
        tds = "".join('<td class="%s">%s</td>' % ("n" if i and numeric(re.sub("<[^>]+>", "", c)) else "", c)
                      for i, c in enumerate(r))
        trs.append('<tr%s>%s</tr>' % (' class="total"' if total_last and j == len(rows) - 1 else "", tds))
    return '<table class="data %s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (cls, th, "".join(trs))


# ------------------------------------------------------------------------------------------------ charts (SVG)
def nice_top(x, step):
    return int(math.ceil(x / step) * step)


def svg_text(x, y, s, anchor="middle", size=11, weight=400, rotate=None, cls=""):
    rot = ' transform="rotate(%d %.1f %.1f)"' % (rotate, x, y) if rotate is not None else ""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" font-weight="%d"%s%s>%s</text>'
            % (x, y, anchor, size, weight, rot, (' class="%s"' % cls) if cls else "", esc(s)))


def chart1_svg(f):
    """CHART 1 as text.md describes it, faults included: one bar per Monday-start week, the Mondays as labels, the
    sessions on top of each bar; no vertical-axis label; nothing marks the part weeks; sessions per week."""
    wk = f["weeks"]
    W, H, L, R, T, B = 640, 330, 52, 16, 18, 52
    top = nice_top(max(w["sessions"] for w in wk), 100)
    pw, ph = W - L - R, H - T - B
    y = lambda val: T + ph - ph * val / top
    out = ['<svg class="chart" viewBox="0 0 %d %d" role="img" aria-label="CHART 1">' % (W, H)]
    for t in range(0, top + 1, 100):
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="grid"/>' % (L, y(t), W - R, y(t)))
        out.append(svg_text(L - 6, y(t) + 4, thou(t), "end", 10))
    slot = pw / len(wk)
    for i, w in enumerate(wk):
        x0 = L + slot * i + slot * 0.18
        bw = slot * 0.64
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bar"/>'
                   % (x0, y(w["sessions"]), bw, y(0) - y(w["sessions"])))
        out.append(svg_text(x0 + bw / 2, y(w["sessions"]) - 4, thou(w["sessions"]), size=10, weight=600))
        out.append(svg_text(x0 + bw / 2, y(0) + 15, w["monday"].strftime("%-d %b"), size=10))
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="axis"/>' % (L, y(0), W - R, y(0)))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%.1f" class="axis"/>' % (L, T, L, y(0)))
    out.append(svg_text(L + pw / 2, H - 10, "Week beginning", size=11, weight=600))
    out.append("</svg>")
    return "".join(out)


def chart2_svg(f):
    """CHART 2: questions answered as bars (left axis, labelled), games started as a line (right axis, labelled),
    dates along the bottom with every 7th labelled."""
    rows = f["chart2"]
    W, H, L, R, T, B = 640, 330, 64, 64, 40, 46
    qtop = nice_top(max(q for _, _, q in rows), 500)
    gtop = nice_top(max(g for _, g, _ in rows), 50)
    qstep = 500 if qtop <= 4000 else 1000
    gstep = 50 if gtop <= 400 else 100
    pw, ph = W - L - R, H - T - B
    yq = lambda val: T + ph - ph * val / qtop
    yg = lambda val: T + ph - ph * val / gtop
    out = ['<svg class="chart" viewBox="0 0 %d %d" role="img" aria-label="CHART 2">' % (W, H)]
    for t in range(0, qtop + 1, qstep):
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="grid"/>' % (L, yq(t), W - R, yq(t)))
        out.append(svg_text(L - 6, yq(t) + 4, thou(t), "end", 10))
    for t in range(0, gtop + 1, gstep):
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="tick"/>' % (W - R, yg(t), W - R + 4, yg(t)))
        out.append(svg_text(W - R + 7, yg(t) + 4, thou(t), "start", 10))
    slot = pw / len(rows)
    pts = []
    for i, (d, g, q) in enumerate(rows):
        x0 = L + slot * i + slot * 0.15
        bw = slot * 0.7
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="bar"/>' % (x0, yq(q), bw, yq(0) - yq(q)))
        pts.append((x0 + bw / 2, yg(g)))
        if i % 7 == 0:
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="tick"/>'
                       % (x0 + bw / 2, yq(0), x0 + bw / 2, yq(0) + 4))
            out.append(svg_text(x0 + bw / 2, yq(0) + 16, d.strftime("%-d %b"), size=10))
    out.append('<polyline points="%s" class="line"/>' % " ".join("%.1f,%.1f" % p for p in pts))
    out += ['<circle cx="%.1f" cy="%.1f" r="2.4" class="dot"/>' % p for p in pts]
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="axis"/>' % (L, yq(0), W - R, yq(0)))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%.1f" class="axis"/>' % (L, T, L, yq(0)))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%.1f" class="axis"/>' % (W - R, T, W - R, yq(0)))
    out.append(svg_text(16, T + ph / 2, "Questions answered", size=11, weight=600, rotate=-90))
    out.append(svg_text(W - 14, T + ph / 2, "Games started", size=11, weight=600, rotate=90))
    out.append(svg_text(L + pw / 2, H - 8, "Date", size=11, weight=600))
    # the key: which series is which
    out.append('<rect x="%d" y="10" width="14" height="10" class="bar"/>' % L)
    out.append(svg_text(L + 20, 19, "Bars: questions answered (left axis)", "start", 10))
    lx = L + 250
    out.append('<line x1="%d" y1="15" x2="%d" y2="15" class="line"/><circle cx="%d" cy="15" r="2.4" class="dot"/>'
               % (lx, lx + 18, lx + 9))
    out.append(svg_text(lx + 24, 19, "Line: games started (right axis)", "start", 10))
    out.append("</svg>")
    return "".join(out)


def boxplot_grid_svg(lo=0, hi=180):
    """The answer grid for 3 (a): a common horizontal scale from 0 to 180, small squares of 2, numbered every 20."""
    W, H, L, R, T = 640, 190, 20, 20, 8
    gh = 150
    pw = W - L - R
    x = lambda val: L + pw * (val - lo) / (hi - lo)
    out = ['<svg class="grid-svg" viewBox="0 0 %d %d" role="img" aria-label="Grid from %d to %d">' % (W, H, lo, hi)]
    rows = 30
    for k in range(rows + 1):
        yy = T + gh * k / rows
        out.append('<line x1="%d" y1="%.2f" x2="%d" y2="%.2f" class="%s"/>'
                   % (L, yy, W - R, yy, "gmaj" if k % 5 == 0 else "gmin"))
    for val in range(lo, hi + 1, 2):
        out.append('<line x1="%.2f" y1="%d" x2="%.2f" y2="%d" class="%s"/>'
                   % (x(val), T, x(val), T + gh, "gmaj" if val % 10 == 0 else "gmin"))
    for val in range(lo, hi + 1, 20):
        out.append('<line x1="%.2f" y1="%d" x2="%.2f" y2="%d" class="axis"/>' % (x(val), T + gh, x(val), T + gh + 4))
        out.append(svg_text(x(val), T + gh + 17, str(val), size=11))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="axis"/>' % (L, T + gh, W - R, T + gh))
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------------------------------------ the three documents
TABLE_HEAD = re.compile(r"^\*\*(TABLE (\d+): [^*]+)\*\*\s*(.*)$")
CHART_HEAD = re.compile(r"^\*\*(CHART (\d+): [^*]+)\*\*\s*(.*)$")


def head_columns(directions):
    m = re.match(r"\((?:columns: )?([^;)]+)", directions)
    return [c.strip() for c in m.group(1).split("·")] if m else None


def prelim_html(body, v, f, used):
    out, title, table, before = [], [], None, []

    def close():
        nonlocal table
        if table:
            if table["n"] == "5":
                rows = [[esc(t["game"]), thou(t["answers"]), thou(t["correct"]), fixed(t["acc"], 0) + "%"]
                        for t in f["t5"]]
            else:
                rows = table["rows"]
            if not table["heads"]:
                raise BuildError("%s has no column headings" % table["title"])
            if any(len(r) != len(table["heads"]) for r in rows):
                raise BuildError("%s: a row's cells differ from its %d columns" % (table["title"], len(table["heads"])))
            out.append('<section class="tbl"><h3>%s</h3>%s%s%s</section>' % (
                table["title"], "".join('<p class="above">%s</p>' % b for b in table["above"]),
                table_html(table["heads"], rows, total_last=rows[-1][0].startswith("Total")),
                "".join('<p class="note">%s</p>' % n for n in table["notes"])))
            table = None

    lines = [ln for ln in body.strip().splitlines() if ln.strip()]
    i = 0
    while i < len(lines) and not lines[i].startswith("### "):
        title.append(fill(lines[i], v, used))
        i += 1
    out.append('<header class="titleblock"><h1>%s</h1><p class="sub">%s</p>%s</header>'
               % (re.sub("</?b>", "", title[0]), title[1], "".join('<p class="instr">%s</p>' % t for t in title[2:])))
    for ln in lines[i:]:
        m_t, m_c = TABLE_HEAD.match(ln), CHART_HEAD.match(ln)
        if ln.startswith("### "):
            close()
            out.append("<h2>%s</h2>" % fill(ln[4:], v, used))
        elif m_t:
            close()
            table = {"title": fill(m_t.group(1), v, used), "n": m_t.group(2), "rows": [], "notes": [], "above": [],
                     "heads": head_columns(m_t.group(3))}
        elif table and ln.startswith("- "):
            table["rows"].append([fill(c.strip(), v, used) for c in ln[2:].split(" · ")])
        elif table and ln.startswith("Note under the table: "):
            table["notes"].append(fill(ln[len("Note under the table: "):], v, used))
        elif table and ln.startswith("Line above the table: "):
            table["above"].append(fill(ln[len("Line above the table: "):], v, used))
        elif table and ln.startswith("Columns: "):
            table["heads"] = [c.strip() for c in ln[len("Columns: "):].split(".")[0].split("·")]
            fill(ln, v, used)
        elif m_c:
            close()
            svg = chart1_svg(f) if m_c.group(2) == "1" else chart2_svg(f) if m_c.group(2) == "2" else None
            if svg is None:
                raise BuildError("no drawing for %s" % m_c.group(1))
            fill(ln, v, used)
            out.append('<section class="chartbox"><h3>%s</h3>%s</section>' % (fill(m_c.group(1), v, used), svg))
        elif ln.startswith("END OF "):
            close()
            out.append('<p class="end">%s</p>' % fill(ln, v, used))
        else:
            close()
            out.append("<p>%s</p>" % fill(ln, v, used))
    close()
    return "".join(out)


QLINE = re.compile(r"^\*\*(\d+(?: \([a-z]\))?)\*\*\s*(.*)$")
MARKS = re.compile(r"\s*\[(\d+) marks?\]\s*(\(Provide a grid from (\d+) to (\d+)\.\))?\s*$")


def answer_space(marks, grid):
    if grid:
        return '<div class="answer grid">%s</div>' % boxplot_grid_svg(*grid)
    n = max(3, 3 * marks)
    return '<div class="answer">%s</div>' % ('<div class="rule"></div>' * n)


def paper_html(body, v, used):
    lines = [ln for ln in body.strip().splitlines() if ln.strip()]
    if lines[0] != "Cover page:":
        raise BuildError("PRACTICE PAPER does not start with 'Cover page:'")
    i, cover = 1, []
    while i < len(lines) and not QLINE.match(lines[i]):
        cover.append(fill(lines[i], v, used))
        i += 1
    cov = ['<section class="cover"><h1>%s</h1><p class="sub">%s</p>' % (re.sub("</?b>", "", cover[0]), cover[1])]
    cov += ['<p class="%s">%s</p>' % ("time" if c.startswith("Time allowed") else "cov", c) for c in cover[2:]]
    cov.append("</section>")
    blocks, cur, marks_total = [], None, 0
    for ln in lines[i:]:
        q = QLINE.match(ln)
        if q or ln.startswith("END OF "):
            if cur:
                blocks.append(cur)
            cur = None
        if ln.startswith("END OF "):
            blocks.append({"end": fill(ln, v, used)})
            continue
        if q:
            cur = {"label": q.group(1), "parts": [], "marks": None, "grid": None}
            text = q.group(2)
            kind = "q"
        else:
            if cur is None:
                raise BuildError("PRACTICE PAPER line outside a question: %s" % ln)
            text = ln
            kind = "li" if ln.startswith("- ") else "p"
            if kind == "li":
                text = ln[2:]
        m = MARKS.search(text)
        if m:
            if cur["marks"] is not None:
                raise BuildError("question %s has two mark totals" % cur["label"])
            cur["marks"] = int(m.group(1))
            if m.group(2):
                cur["grid"] = (int(m.group(3)), int(m.group(4)))
            text = text[:m.start()]
        cur["parts"].append((kind, fill(text, v, used)))
    if cur:
        blocks.append(cur)
    out, per_q = [], {}
    for b in blocks:
        if "end" in b:
            out.append('<p class="end">%s</p>' % b["end"])
            continue
        inner, lis = [], []
        for kind, t in b["parts"]:
            if kind == "li":
                lis.append("<li>%s</li>" % t)
                continue
            if lis:
                inner.append("<ul>%s</ul>" % "".join(lis))
                lis = []
            inner.append('<p>%s</p>' % t if kind == "p" else t)
        if lis:
            inner.append("<ul>%s</ul>" % "".join(lis))
        mk = ""
        if b["marks"] is not None:
            marks_total += b["marks"]
            per_q[b["label"]] = b["marks"]
            mk = '<div class="marks">[%d mark%s]</div>' % (b["marks"], "" if b["marks"] == 1 else "s")
        first = inner[0] if inner else ""
        rest = "".join(inner[1:])
        out.append('<section class="q%s"><div class="qrow"><div class="qn">%s</div><div class="qt">%s%s</div></div>%s%s</section>'
                   % (" has-marks" if mk else " stem", esc(b["label"]), first, rest, mk,
                      answer_space(b["marks"], b["grid"]) if b["marks"] is not None else ""))
    return "".join(cov) + '<div class="questions">%s</div>' % "".join(out), marks_total, per_q


def scheme_html(body, v, used):
    lines = [ln for ln in body.strip().splitlines() if ln.strip()]
    title, paras, rows = [], [], []
    for ln in lines:
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if set(ln.replace("|", "").strip()) <= set("- "):
                continue
            rows.append([fill(c, v, used) for c in cells])
        elif not paras and not ln.startswith("**Notes") and len(title) < 3:
            title.append(fill(ln, v, used))
        else:
            paras.append(fill(ln, v, used))
    head, body_rows = rows[0], rows[1:]
    trs = []
    for r in body_rows:
        cls = ' class="total"' if r[1] == "Total" else ""
        trs.append("<tr%s><td class=\"qn\">%s</td><td>%s</td><td class=\"n\">%s</td></tr>" % (cls, r[0], r[1], r[2]))
    totals = {r[0]: int(r[2]) for r in body_rows if r[1] != "Total"}
    grand = [int(r[2]) for r in body_rows if r[1] == "Total"]
    html_ = ('<header class="titleblock"><h1>%s</h1><p class="sub">%s</p></header>%s'
             '<table class="scheme"><thead><tr><th>%s</th><th>%s</th><th class="n">%s</th></tr></thead><tbody>%s</tbody></table>'
             % (re.sub("</?b>", "", title[0]), title[1], "".join("<p>%s</p>" % p for p in paras),
                head[0], head[1], head[2], "".join(trs)))
    return html_, totals, grand


CSS = """
@page { size: A4; margin: 15mm 17mm 18mm 17mm;
  @bottom-center { content: "%(footer)s " counter(page); font-family: 'Outfit', sans-serif; font-size: 8pt; color: #000;
    vertical-align: top; padding-top: 4mm; } }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; color: #000; font-family: 'Outfit', sans-serif; font-size: 10.5pt; line-height: 1.4; }
b { font-weight: 700; }
h1 { font-size: 26pt; font-weight: 800; line-height: 1.1; }
h2 { font-size: 13pt; font-weight: 700; margin: 5mm 0 1.5mm; padding-bottom: 0.8mm; border-bottom: 0.4mm solid #000;
  break-after: avoid; }
h2 + p { break-before: avoid; }
h3 { font-size: 11pt; font-weight: 700; margin-bottom: 1.5mm; }
p { margin-bottom: 2mm; }
.titleblock { border-bottom: 0.8mm solid #000; padding-bottom: 3mm; margin-bottom: 4mm; }
.titleblock .sub { font-size: 13pt; font-weight: 600; margin: 1mm 0 2mm; }
.titleblock .instr { font-weight: 600; }
.tbl, .chartbox { break-inside: avoid; margin: 4mm 0 5mm; }
table.data { border-collapse: collapse; width: 100%%; }
table.data th { text-align: left; font-weight: 700; border-bottom: 0.4mm solid #000; padding: 1mm 2mm; vertical-align: bottom; }
table.data td { padding: 0.9mm 2mm; border-bottom: 0.15mm solid #000; }
table.data .n { text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 9.5pt; white-space: nowrap; }
table.data th.n { font-family: 'Outfit', sans-serif; font-size: 10.5pt; }
table.data tr.total td { font-weight: 700; border-top: 0.4mm solid #000; }
.note, .above { font-size: 9.5pt; margin: 1.5mm 0; }
svg.chart { width: 100%%; height: auto; display: block; font-family: 'Outfit', sans-serif; }
svg text { fill: #000; }
.grid { stroke: #999; stroke-width: 0.5; }
.axis { stroke: #000; stroke-width: 1.2; }
.tick { stroke: #000; stroke-width: 1; }
.bar { fill: #c8c8c8; stroke: #000; stroke-width: 0.8; }
.line { fill: none; stroke: #000; stroke-width: 1.6; }
.dot { fill: #000; }
.end { text-align: center; font-weight: 700; margin-top: 5mm; letter-spacing: 0.04em; }
.cover { break-after: page; padding-top: 30mm; }
.cover h1 { font-size: 34pt; }
.cover .sub { font-size: 15pt; font-weight: 600; margin: 2mm 0 10mm; padding-bottom: 6mm; border-bottom: 0.8mm solid #000; }
.cover .time { font-size: 13pt; font-weight: 700; margin-bottom: 8mm; }
.cover .cov { margin-bottom: 4mm; font-size: 11pt; }
.q { margin-bottom: 4mm; }
.q.has-marks { break-inside: avoid; }
.q.stem { break-after: avoid; margin-bottom: 2mm; }
.qrow { display: flex; gap: 3mm; align-items: flex-start; }
.qn { flex: none; width: 13mm; font-weight: 700; }
.qt { flex: 1 1 auto; }
.qt p { margin: 1.5mm 0 0; }
.qt ul { margin: 1mm 0 0 5mm; }
.marks { text-align: right; font-weight: 700; margin-top: 1mm; }
.answer { margin: 1.5mm 0 0 16mm; }
.rule { height: 8mm; border-bottom: 0.25mm solid #000; }
.grid-svg { width: 100%%; height: auto; display: block; font-family: 'Outfit', sans-serif; }
.gmin { stroke: #888; stroke-width: 0.35; }
.gmaj { stroke: #000; stroke-width: 0.8; }
table.scheme { border-collapse: collapse; width: 100%%; font-size: 9.5pt; margin-top: 3mm; }
table.scheme th { text-align: left; border-bottom: 0.5mm solid #000; padding: 1.2mm 1.5mm; }
table.scheme td { vertical-align: top; padding: 1.4mm 1.5mm; border-bottom: 0.2mm solid #000; line-height: 1.35; }
table.scheme tr { break-inside: avoid; }
table.scheme td.qn { width: 14mm; font-weight: 700; white-space: nowrap; }
table.scheme td.n { text-align: right; width: 12mm; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
table.scheme th.n { text-align: right; }
.mono { font-family: 'JetBrains Mono', monospace; font-size: 0.9em; }
table.scheme tr.total td { border-top: 0.5mm solid #000; font-weight: 700; }
"""

FIT_JS = """async () => {
  await document.fonts.ready;
  const loaded = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, ''));
  const over = [];
  const W = document.documentElement.clientWidth;
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.right > W + 0.5) over.push(el.tagName + '.' + el.className + ' ' + Math.round(r.right - W) + 'px');
  }
  return {loaded, over: over.slice(0, 10)};
}"""


def documents(text, v, f):
    """[(pdf name, html)] for the three PDFs, after every check on the text. Raises BuildError listing every fault."""
    secs = sections(text)
    for name, _, _ in DOCS:
        if name not in secs:
            raise BuildError("text.md has no %s section" % name)
    footer = footer_text(text)
    used, faults = set(), []
    pre = prelim_html(secs["PRELIMINARY MATERIAL"], v, f, used)
    paper, paper_total, per_q = paper_html(secs["PRACTICE PAPER"], v, used)
    scheme, scheme_rows, grand = scheme_html(secs["MARK SCHEME"], v, used)
    bodies = {"PRELIMINARY MATERIAL": pre, "PRACTICE PAPER": paper, "MARK SCHEME": scheme}
    for name, b in bodies.items():
        for m in sorted(set(re.findall(r"\{\{[^}]*\}\}?|\{\{", b))):
            faults.append("leftover placeholder %s in %s" % (m, name))
    m = re.search(r"maximum mark for this paper is (\d+)", paper)
    if not m or int(m.group(1)) != paper_total:
        faults.append("the paper's marks add to %d, but its cover says %s" % (paper_total, m.group(1) if m else "nothing"))
    if grand != [paper_total]:
        faults.append("the mark scheme's Total row says %s; the paper's marks add to %d" % (grand, paper_total))
    if scheme_rows != per_q:
        diff = sorted(set(scheme_rows.items()) ^ set(per_q.items()))
        faults.append("mark scheme totals differ from the paper's marks: %s" % diff)
    if sum(scheme_rows.values()) != paper_total:
        faults.append("the mark scheme's rows add to %d, not %d" % (sum(scheme_rows.values()), paper_total))
    if faults:
        raise BuildError("; ".join(faults))
    css = CSS % {"footer": footer.replace('"', '\\"')}
    out = []
    for name, pdf, title in DOCS:
        out.append((pdf, '<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><title>%s</title>'
                         '<link rel="stylesheet" href="%s"><style>%s</style></head><body>%s</body></html>'
                         % (esc(title), esc(FONTS), css, bodies[name])))
    return out, used


def placeholders_by_doc(text):
    """{pdf name: [keys its section's text names]}: what the committed PDF must contain."""
    secs = sections(text)
    return {pdf: sorted(set(PLACEHOLDER.findall(secs[name]))) for name, pdf, _ in DOCS}


def offline_context(browser, **opts):
    """Nothing reaches the network: Google Fonts from the repo's pinned copies (scripts/fonts/), all else aborted
    (tools/maffscards/build_pdf.py's route)."""
    import bank_common as bc
    ctx = browser.new_context(**opts)

    def route(r):
        url = r.request.url
        if bc.is_font_cdn(url):
            bc.serve_real_font(r)
        elif url.startswith(("http:", "https:")):
            r.abort()
        else:
            r.continue_()
    ctx.route("**/*", route)
    return ctx


def print_pdfs(docs, out_dir, proofs=None):
    from playwright.sync_api import sync_playwright
    out_dir = pathlib.Path(out_dir)
    report = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            ctx = offline_context(browser, viewport={"width": 680, "height": 1000})
            for pdf, doc in docs:
                page = ctx.new_page()
                page.set_content(doc, wait_until="load")
                page.emulate_media(media="print")
                fit = page.evaluate(FIT_JS)
                problems = ["font %s did not load (loaded: %s)" % (fam, sorted(set(fit["loaded"])))
                            for fam in ("Outfit", "JetBrains Mono") if fam not in fit["loaded"]]
                problems += ["%s: wider than the page: %s" % (pdf, o) for o in fit["over"]]
                if problems:
                    raise BuildError("; ".join(problems))
                out_dir.mkdir(parents=True, exist_ok=True)
                page.pdf(path=str(out_dir / pdf), prefer_css_page_size=True, print_background=True)
                if proofs:
                    pathlib.Path(proofs).mkdir(parents=True, exist_ok=True)
                    (pathlib.Path(proofs) / pdf.replace(".pdf", ".html")).write_text(doc, encoding="utf-8", newline="")
                report.append(pdf)
                page.close()
        finally:
            browser.close()
    return report


# ================================================================================================ main
def run(text_path=TEXT, data_dir=DATA, out_dir=DATA, check_only=False, proofs=None):
    """Every computation and condition; then (unless check_only) the PDFs. Returns (exit code, lines to print)."""
    msgs = []
    text = pathlib.Path(text_path).read_text(encoding="utf-8")
    site, games = load(data_dir)
    v, f = compute(site, games)
    table = values_table(text)
    for k, got, want in mismatches(v, table):
        msgs.append("VALUE %s: computed %s, Values table %s" % (k, got, want))
    secs = sections(text)
    named = {k for name, _, _ in DOCS for k in PLACEHOLDER.findall(secs.get(name, ""))}
    extra = sorted(named - set(table))
    for k in extra:
        msgs.append("PLACEHOLDER {{%s}} is not in the Values table" % k)
    for n, what, ok in conditions(v, f, site):
        if not ok:
            label = ("condition %d" % n) if isinstance(n, int) else n
            msgs.append("CONDITION %s is false: %s" % (label, what))
            if n == 11:
                msgs += ["  source: %s" % s for s in source_problems(site)]
    try:
        docs, _used = documents(text, v, f)
    except BuildError as e:
        msgs.append("TEXT %s" % e)
        docs = None
    if msgs:
        return 1, ["BUILD FAILED"] + msgs
    if check_only:
        return 0, ["check: %d values equal to the Values table, %d conditions true, every placeholder filled, marks "
                   "add to the cover's total" % (len(table), len(conditions(v, f, site)))]
    written = print_pdfs(docs, out_dir, proofs)
    return 0, ["wrote %s" % ", ".join(str(pathlib.Path(out_dir) / w) for w in written)]


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="every computation and condition; write nothing")
    ap.add_argument("--text", default=str(TEXT))
    ap.add_argument("--data", default=str(DATA), help="the folder holding the two CSVs")
    ap.add_argument("--out", default=str(DATA), help="where the three PDFs go")
    ap.add_argument("--proofs", help="also write the three HTML documents here (never committed)")
    a = ap.parse_args(argv)
    try:
        code, lines = run(a.text, a.data, a.out, a.check, a.proofs)
    except (DataError, BuildError) as e:
        code, lines = 1, ["BUILD FAILED", str(e)]
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
