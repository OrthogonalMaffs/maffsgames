#!/usr/bin/env python3
"""It's Just Base 60, Bruv: question bank generator (Project Claude, 24 Nov 2026). Deterministic: no randomness.

Four stages, 48 items each (two types of 24). Every value is computed here from whole numbers of minutes;
nothing is typed by hand except the contexts. Every distractor comes from a named error (canon SR-4), and
carries that error's key, so the page can show the line for it.

Formats (UK):
  24-hour clock  HH:MM, two-digit hour        e.g. 03:45, 15:45, 00:15
  12-hour clock  h:MM am/pm, h from 1 to 12   e.g. 3:45 pm, 12:15 am (00:15), 12:30 pm (12:30)
  duration       "2 h 15 min", "45 min", "3 h"
  decimal hours  shortest exact decimal       e.g. 1.5, 1.25, 2.1
Options are display strings; dataset.val is the string itself.
"""
import hashlib
import json
import sys
from fractions import Fraction

STAGES = {1: "Sixty, Not a Hundred", 2: "Twelve or Twenty-Four", 3: "How Long, Bruv?", 4: "The Calculator Lies"}


def dur(h, m):
    if h == 0:
        return f"{m} min"
    if m == 0:
        return f"{h} h"
    return f"{h} h {m} min"


def t24(h, m):
    return f"{h:02d}:{m:02d}"


def t12(h, m, half):
    return f"{h}:{m:02d} {half}"


def dec(x):
    """Shortest exact decimal of a Fraction with a terminating expansion."""
    x = Fraction(x)
    for dp in range(0, 7):
        if (x * 10 ** dp).denominator == 1:
            s = f"{float(x):.{dp}f}"
            assert Fraction(s) == x
            return s
    raise ValueError(x)


def pick(answer, pool):
    """First three distinct named errors, none equal to the answer. Pool is [(value, err)]."""
    out, seen = [], {minutes_of(answer)}
    for v, e in pool:
        if v is None or minutes_of(v) in seen:
            continue
        seen.add(minutes_of(v))
        out.append({"val": v, "err": e})
        if len(out) == 3:
            break
    assert len(out) == 3, (answer, pool)
    return out


def ctx(lst, i):
    return lst[i % len(lst)]


# ---------------------------------------------------------------------------------------------- stage 1
S1A_CTX = {  # minutes -> h min, chosen by the number of hours so every context is believable
    "short": ["A film lasts {T} minutes. How long is that in hours and minutes?",
              "A gaming session lasted {T} minutes. How long is that in hours and minutes?",
              "The coach journey takes {T} minutes. How long is that in hours and minutes?"],
    "long": ["A shift at the warehouse is {T} minutes. How long is that in hours and minutes?",
             "A charity walk took {T} minutes. How long is that in hours and minutes?",
             "A coach trip to the coast takes {T} minutes. How long is that in hours and minutes?",
             "A flight to New York takes {T} minutes. How long is that in hours and minutes?"],
}
S1B_CTX = {  # h min -> minutes, chosen by the number of hours
    1: ["A driving lesson is {d}. How many minutes is that?", "A football match, with half time, takes {d}. How many minutes is that?",
        "A cake bakes for {d}. How many minutes is that?", "A phone takes {d} to charge. How many minutes is that?"],
    2: ["A coach journey takes {d}. How many minutes is that?", "A film lasts {d}. How many minutes is that?",
        "A revision session lasts {d}. How many minutes is that?", "A gaming session lasted {d}. How many minutes is that?"],
    3: ["A gig lasts {d}, support act included. How many minutes is that?", "A train journey takes {d}. How many minutes is that?",
        "A theme park trip lasted {d}. How many minutes is that?", "A football tournament ran for {d}. How many minutes is that?"],
    4: ["A shift at the cafe is {d}. How many minutes is that?", "A hike took {d}. How many minutes is that?",
        "A coach trip to the coast takes {d}. How many minutes is that?", "A flight takes {d}. How many minutes is that?"],
}


def stage1():
    items = []
    i = 0
    for h in (2, 3, 4, 5, 6, 7, 8, 9):
        for m in (15, 30, 45):
            T = 60 * h + m
            ans = dur(h, m)
            f = Fraction(T, 60) - h           # decimal part of T / 60
            hundred = f * 100
            pool = [
                (dur(T // 100, T % 100), "base100"),                                   # 135 -> 1 h 35 min
                (dur(h, int(hundred)) if hundred.denominator == 1 else None, "decimal_read"),  # 2.25 -> 2 h 25 min
                (dur(h + 1, m), "rounded_hour"),                                       # rounded the hours up
            ]
            items.append({"id": f"s1a-{T}", "stage": 1, "type": "min-to-hm", "T": T,
                          "prompt": ctx(S1A_CTX["short" if h <= 3 else "long"], i).format(T=T), "answer": ans, "decoys": pick(ans, pool),
                          "working": [f"\\({T} \\div 60 = {h}\\) remainder \\({m}\\)", f"\\({T}\\) min \\(= {h}\\) h \\({m}\\) min"]})
            i += 1
    i = 0
    for h in (1, 2, 3, 4):
        for m in (15, 30, 45, 10, 20, 40):
            T = 60 * h + m
            ans = str(T)
            pool = [
                (str(100 * h + m), "base100"),                                # 2 h 15 -> 215
                (dec(Fraction(60 * h) + Fraction(6 * m, 10)), "decimal_times60"),  # 2.15 h x 60 = 129
                (str(60 * h), "dropped_minutes"),                             # forgot the 15
            ]
            items.append({"id": f"s1b-{h}h{m:02d}", "stage": 1, "type": "hm-to-min", "h": h, "m": m,
                          "prompt": ctx(S1B_CTX[h], i).format(d=dur(h, m)), "answer": ans, "decoys": pick(ans, pool),
                          "working": [f"\\({h} \\times 60 + {m} = {T}\\)", f"{dur(h, m)} \\(= {T}\\) min"]})
            i += 1
    return items


# ---------------------------------------------------------------------------------------------- stage 2
S2A_CTX = {  # 12 -> 24, chosen by the time of day
    "day": ["Your train leaves at {t}. What is that on the 24-hour clock?",
            "The gym class starts at {t}. What is that on the 24-hour clock?",
            "Your shift starts at {t}. What is that on the 24-hour clock?",
            "Your parcel is due at {t}. What is that on the 24-hour clock?"],
    "evening": ["Your train leaves at {t}. What is that on the 24-hour clock?",
                "Doors open for the gig at {t}. What is that on the 24-hour clock?",
                "Your shift starts at {t}. What is that on the 24-hour clock?",
                "The film starts at {t}. What is that on the 24-hour clock?"],
}
S2B_CTX = [  # 24 -> 12
    "The bus timetable says {t}. What is that on the 12-hour clock?",
    "Your phone says {t}. What is that on the 12-hour clock?",
    "The parcel arrives at {t}. What is that on the 12-hour clock?",
    "The cinema ticket says {t}. What is that on the 12-hour clock?",
]
MINS = [15, 40, 5, 50, 25, 35, 10, 45, 20, 55, 30]


def stage2():
    items = []
    # Type A: 12-hour -> 24-hour. 20 afternoon/evening, 2 just after midday, 2 morning. No times just after midnight:
    # their only wrong forms (24:xx, 0:xx am) are equal in value to the answer or not a clock reading, so midnight is
    # taught through the noon_midnight line (12 pm read as midnight, or 12:xx pm read as 12:xx am).
    # Every err key names its error in one direction only (ERR_TYPES): pm adds 12; going back to the 12-hour clock
    # takes 12 off; just after midday and the morning change nothing.
    a_cases = [(h, MINS[k % 11], "pm") for k, h in enumerate(range(1, 12))]
    a_cases += [(h, MINS[(k + 5) % 11], "pm") for k, h in enumerate(range(1, 8))]
    a_cases += [(12, 30, "pm"), (12, 45, "pm"), (8, 20, "pm"), (11, 50, "pm"), (7, 30, "am"), (9, 25, "am")]
    for i, (h, m, half) in enumerate(a_cases):
        shown = t12(h, m, half)
        if half == "pm" and h < 12:
            ans = t24(h + 12, m)
            pool = [(t24(h, m), "forgot_pm"), (t24(h + 10, m), "added_10"), (t24(h + 11, m), "counted_short")]
        elif half == "pm":   # 12:mm pm is just after noon: nothing changes
            ans = t24(12, m)
            pool = [(t24(0, m), "noon_midnight"), (t24(22, m), "noon_changed"), (t24(2, m), "noon_changed")]
        else:                # morning: nothing changes
            ans = t24(h, m)
            pool = [(t24(h + 12, m), "added_to_morning"), (t24(h + 10, m), "added_to_morning"), (t24(h + 11, m), "added_to_morning")]
        work = {"pm": f"pm, so add 12: \\({h} + 12 = {h + 12}\\)", "noonpm": "12 pm is the hour after midday, so it stays 12",
                "am": "am, before midday: the hour stays the same"}
        key = "pm" if half == "pm" and h < 12 else ("noonpm" if half == "pm" else "am")
        evening = half == "pm" and 6 <= h <= 11
        items.append({"id": f"s2a-{h}{m:02d}{half}", "stage": 2, "type": "12-to-24", "h": h, "m": m, "half": half,
                      "prompt": ctx(S2A_CTX["evening" if evening else "day"], i).format(t=shown), "answer": ans, "decoys": pick(ans, pool),
                      "working": [work[key], f"{shown} \\(\\to\\) {ans}"]})
    # Type B: 24-hour -> 12-hour. 22 afternoon/evening (13:00 to 22:59), 2 noon hour.
    b_cases = [(H, MINS[k % 11]) for k, H in enumerate(range(13, 23))]
    b_cases += [(H, MINS[(k + 4) % 11]) for k, H in enumerate(range(13, 23))]
    b_cases += [(14, 52), (19, 8), (12, 20), (12, 55)]
    for i, (H, m) in enumerate(b_cases):
        shown = t24(H, m)
        if H > 12:
            ans = t12(H - 12, m, "pm")
            pool = [(t12(H - 12, m, "am"), "wrong_half"), (t12(H - 10, m, "pm"), "took_10"), (t12(H - 11, m, "pm"), "took_11")]
            w = f"After 12, so take off 12: \\({H} - 12 = {H - 12}\\), and it is pm"
        else:
            ans = t12(12, m, "pm")
            pool = [(t12(12, m, "am"), "noon_midnight"), (t12(2, m, "pm"), "noon_changed"), (t12(1, m, "pm"), "noon_changed")]
            w = "12:something is just after midday, so it is 12 pm"
        items.append({"id": f"s2b-{H:02d}{m:02d}", "stage": 2, "type": "24-to-12", "H": H, "m": m,
                      "prompt": ctx(S2B_CTX, i).format(t=shown), "answer": ans, "decoys": pick(ans, pool),
                      "working": [w, f"{shown} \\(\\to\\) {ans}"]})
    return items


# ---------------------------------------------------------------------------------------------- stage 3
S3A_CTX = {  # duration between, chosen by the length
    "short": ["A bus leaves at {s} and arrives at {e}. How long is the journey?",
              "Parking starts at {s} and you leave at {e}. How long did you park for?",
              "Your gym session starts at {s} and ends at {e}. How long is it?"],
    "mid": ["A train leaves at {s} and arrives at {e}. How long is the journey?",
            "The film starts at {s} and ends at {e}. How long is it?",
            "Parking starts at {s} and you leave at {e}. How long did you park for?",
            "The match kicks off at {s} and finishes at {e}. How long is that?"],
    "long": ["A train leaves at {s} and arrives at {e}. How long is the journey?",
             "You clock in at {s} and clock out at {e}. How long were you there?",
             "Parking starts at {s} and you leave at {e}. How long did you park for?"],
}
S3B_CTX = {  # end time, chosen by the length
    0: ["A bus leaves at {s}. The journey takes {d}. What time does it arrive?",
        "You put a lasagne in the oven at {s}. It needs {d}. What time is it ready?",
        "A delivery van sets off at {s}. The drop takes {d}. What time does it get there?"],
    1: ["A bus leaves at {s}. The journey takes {d}. What time does it arrive?",
        "A delivery van sets off at {s}. The drop takes {d}. What time does it get there?",
        "A film starts at {s} and lasts {d}. What time does it finish?"],
    2: ["Your shift starts at {s} and lasts {d}. What time does it end?",
        "A coach leaves at {s}. The trip takes {d}. What time does it arrive?",
        "A film starts at {s} and lasts {d}. What time does it finish?"],
}
S3A_CASES = [  # (start h, start m, end h, end m): end minutes smaller than start minutes, so the hour must be borrowed
    (9, 45, 11, 20), (8, 50, 10, 15), (13, 40, 15, 5), (10, 35, 12, 10), (14, 55, 16, 25), (7, 45, 9, 30),
    (11, 50, 13, 20), (15, 25, 16, 10), (6, 40, 8, 15), (12, 45, 14, 30), (16, 50, 18, 5), (9, 55, 10, 40),
    (18, 35, 20, 20), (8, 25, 9, 10), (13, 50, 16, 35), (10, 45, 13, 15), (17, 40, 19, 25), (7, 55, 10, 20),
    (19, 30, 21, 15), (11, 35, 12, 20), (14, 45, 17, 5), (6, 50, 9, 25), (20, 40, 22, 10), (15, 55, 17, 30),
]
S3B_CASES = [  # (start h, start m, dur h, dur m): the minutes carry past 60
    (10, 50, 0, 45), (9, 40, 1, 35), (14, 35, 2, 40), (7, 45, 0, 25), (16, 30, 1, 50), (11, 55, 0, 20),
    (8, 50, 2, 15), (13, 25, 1, 45), (18, 40, 0, 55), (6, 35, 3, 30), (12, 45, 1, 25), (15, 50, 2, 30),
    (9, 15, 0, 55), (17, 35, 1, 40), (10, 25, 2, 45), (19, 50, 0, 35), (8, 40, 1, 25), (13, 55, 3, 10),
    (11, 30, 0, 50), (14, 45, 1, 55), (7, 20, 2, 50), (16, 55, 0, 40), (12, 35, 2, 35), (20, 15, 1, 50),
]


def stage3():
    items = []
    for i, (sh, sm, eh, em) in enumerate(S3A_CASES):
        assert em < sm
        d = (60 * eh + em) - (60 * sh + sm)
        ans = dur(d // 60, d % 60)
        hhmm = (100 * eh + em) - (100 * sh + sm)            # 1120 - 945 = 175
        pool = [
            (dur(hhmm // 100, hhmm % 100), "hhmm_subtract"),  # 1 h 75 min
            (dur(eh - sh, sm - em), "no_borrow"),             # hours apart, then the smaller minutes from the larger
            (dur(hhmm // 60, hhmm % 60), "hhmm_as_minutes"),  # 175 read as minutes: 2 h 55 min
            (dur(0, 60 - sm), "stopped_at_hour"),             # counted on to the next o'clock and stopped
        ]
        s, e = t24(sh, sm), t24(eh, em)
        to_hour = 60 - sm
        items.append({"id": f"s3a-{sh:02d}{sm:02d}-{eh:02d}{em:02d}", "stage": 3, "type": "duration",
                      "start": s, "end": e, "prompt": ctx(S3A_CTX["short" if d < 60 else ("mid" if d <= 150 else "long")], i).format(s=s, e=e), "answer": ans,
                      "decoys": pick(ans, pool),
                      "working": [f"{s} to {t24(sh + 1, 0)} is \\({to_hour}\\) min",
                                  f"{t24(sh + 1, 0)} to {e} is {dur(eh - sh - 1, em)}",
                                  f"\\({to_hour}\\) min + {dur(eh - sh - 1, em)} = {ans}"]})
    for i, (sh, sm, dh, dm) in enumerate(S3B_CASES):
        assert sm + dm >= 60
        end = 60 * sh + sm + 60 * dh + dm
        assert end < 24 * 60
        ans = t24(end // 60, end % 60)
        pool = [
            (t24(sh + dh + 1, dm), "to_hour_then_all"),              # counted on to the hour, then added all the minutes again
            (t24(sh + dh, sm + dm - 60), "forgot_hour"),              # took off 60, never added the hour
            (f"{sh + dh + 1:02d}:{sm + dm:02d}" if sm + dm < 100 else None, "carry_no_subtract"),  # added the hour, kept 95
            (t24((60 * sh + sm - 60 * dh - dm) // 60, (60 * sh + sm - 60 * dh - dm) % 60), "subtracted"),  # took it away
        ]
        s, d = t24(sh, sm), dur(dh, dm)
        items.append({"id": f"s3b-{sh:02d}{sm:02d}+{dh}h{dm:02d}", "stage": 3, "type": "end-time",
                      "start": s, "dh": dh, "dm": dm, "prompt": ctx(S3B_CTX[min(dh, 2)], i).format(s=s, d=d), "answer": ans,
                      "decoys": pick(ans, pool),
                      "working": [f"\\({sm} + {dm} = {sm + dm}\\) min, which is 1 h \\({sm + dm - 60}\\) min",
                                  f"\\({sh} + {dh} + 1 = {sh + dh + 1}\\), so {ans}"]})
    return items


# ---------------------------------------------------------------------------------------------- stage 4
S4A_CTX = [  # decimal hours -> h min
    "A calculator says a job took {x} hours. How long is that in hours and minutes?",
    "A sat nav works out the drive as {x} hours. How long is that in hours and minutes?",
    "A spreadsheet logs your shift as {x} hours. How long is that in hours and minutes?",
    "Your fitness app says you walked for {x} hours. How long is that in hours and minutes?",
]
S4B_CTX = [  # h min -> decimal hours
    "You worked {d}. Your pay calculator wants the time in hours, as a decimal. What do you type in?",
    "A plumber was on the job for {d}. To work out the bill, write it in hours as a decimal.",
    "A cyclist rode for {d}. To work out the speed, write it in hours as a decimal.",
    "A cleaner worked {d}. The timesheet wants hours as a decimal. What goes in the box?",
]


def stage4():
    items = []
    fracs = [Fraction(1, 2), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 5),
             Fraction(4, 5), Fraction(1, 10), Fraction(3, 10), Fraction(7, 10), Fraction(9, 10), Fraction(1, 2)]
    a_cases = [(h, f) for h, f in zip([1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 4], fracs)]
    a_cases += [(h, f) for h, f in zip([2, 3, 1, 4, 5, 1, 4, 3, 1, 4, 5, 6], fracs)]
    seen = set()
    for i, (h, f) in enumerate(a_cases):
        assert (h, f) not in seen; seen.add((h, f))
        x = h + f
        mins = f * 60
        assert mins.denominator == 1
        mins = int(mins)
        ans = dur(h, mins)
        T = 60 * h + mins
        hundred = f * 100
        ten = f * 10
        pool = [
            (dur(h, int(hundred)), "decimal_read"),                                      # 2.5 -> 2 h 50 min
            (dur(T // 100, T % 100) if T >= 100 else None, "base100"),                    # 150 min -> 1 h 50 min
            (dur(int(x * 100) // 60, int(x * 100) % 60), "times100"),                     # 1.6 h -> 160 min -> 2 h 40 min
            (dur(h, int(ten)) if ten.denominator == 1 else None, "tenths_read"),          # 2.5 -> 2 h 5 min
            (dur(h + 1 if f >= Fraction(1, 2) else h, 0), "rounded_hour"),
        ]
        xs = dec(x)
        items.append({"id": f"s4a-{xs}", "stage": 4, "type": "dec-to-hm", "x": xs,
                      "prompt": ctx(S4A_CTX, i).format(x=xs), "answer": ans, "decoys": pick(ans, pool),
                      "working": [f"\\({dec(f)} \\times 60 = {mins}\\)", f"{xs} hours \\(=\\) {ans}"]})
    b_cases = [(1, 15), (2, 30), (1, 45), (3, 6), (2, 12), (1, 18), (2, 24), (1, 36), (3, 42), (2, 48), (1, 54), (4, 15),
               (3, 30), (2, 45), (1, 6), (3, 12), (4, 18), (3, 24), (2, 36), (1, 42), (4, 48), (3, 54), (5, 30), (2, 15)]
    seen = set()
    for i, (h, m) in enumerate(b_cases):
        assert (h, m) not in seen; seen.add((h, m))
        val = Fraction(60 * h + m, 60)
        ans = dec(val)
        T = 60 * h + m
        pool = [
            (dec(Fraction(100 * h + m, 100)), "minutes_as_decimal"),  # 1 h 15 -> 1.15
            (str(T), "total_minutes"),                                # 75 (minutes, not hours)
            (dec(Fraction(T, 100)), "minutes_over_100"),              # 75 / 100 = 0.75
        ]
        items.append({"id": f"s4b-{h}h{m:02d}", "stage": 4, "type": "hm-to-dec", "h": h, "m": m,
                      "prompt": ctx(S4B_CTX, i).format(d=dur(h, m)), "answer": ans, "decoys": pick(ans, pool),
                      "working": [f"\\({m} \\div 60 = {dec(Fraction(m, 60))}\\)", f"{dur(h, m)} \\(= {ans}\\) hours"]})
    return items


# Which item types each named error may appear in: a key's feedback line is written for these types only.
ERR_TYPES = {
    "base100": {"min-to-hm", "hm-to-min", "dec-to-hm"}, "decimal_read": {"min-to-hm", "dec-to-hm"},
    "rounded_hour": {"min-to-hm", "dec-to-hm"}, "decimal_times60": {"hm-to-min"}, "dropped_minutes": {"hm-to-min"},
    "forgot_pm": {"12-to-24"}, "added_10": {"12-to-24"}, "counted_short": {"12-to-24"},
    "added_to_morning": {"12-to-24"}, "noon_midnight": {"12-to-24", "24-to-12"}, "noon_changed": {"12-to-24", "24-to-12"},
    "wrong_half": {"24-to-12"}, "took_10": {"24-to-12"}, "took_11": {"24-to-12"},
    "hhmm_subtract": {"duration"}, "no_borrow": {"duration"}, "hhmm_as_minutes": {"duration"}, "stopped_at_hour": {"duration"},
    "to_hour_then_all": {"end-time"}, "forgot_hour": {"end-time"}, "carry_no_subtract": {"end-time"}, "subtracted": {"end-time"},
    "times100": {"dec-to-hm"}, "tenths_read": {"dec-to-hm"},
    "minutes_as_decimal": {"hm-to-dec"}, "total_minutes": {"hm-to-dec"}, "minutes_over_100": {"hm-to-dec"},
}


def bank():
    return stage1() + stage2() + stage3() + stage4()


# ---------------------------------------------------------------------------------------------- checks
def minutes_of(s):
    """Value of a display string, for the equal-value check: durations and clock times to minutes, decimals as Fractions."""
    import re
    if re.fullmatch(r"\d\d:\d\d", s):
        return ("clock", (int(s[:2]) * 60 + int(s[3:])) % 1440)
    m = re.fullmatch(r"(\d+):(\d\d) (am|pm)", s)
    if m:
        h, mm, half = int(m[1]), int(m[2]), m[3]
        return ("clock", (((h % 12) + (12 if half == "pm" else 0)) * 60 + mm) % 1440)
    m = re.fullmatch(r"(?:(\d+) h)?(?: ?(\d+) min)?", s)
    if m and (m[1] or m[2]):
        return ("dur", int(m[1] or 0) * 60 + int(m[2] or 0))
    return ("num", Fraction(s))


def check(items):
    ids = [i["id"] for i in items]
    assert len(ids) == len(set(ids)), "duplicate ids"
    prompts = [i["prompt"] for i in items]
    assert len(prompts) == len(set(prompts)), "duplicate prompts"
    for it in items:
        vals = [it["answer"]] + [d["val"] for d in it["decoys"]]
        assert len(set(vals)) == 4, it["id"]
        kinds = [minutes_of(v) for v in vals]
        # no decoy equal in value to the answer (SR-4); "24:xx" and "x:xx am/pm" forms count as clock values
        assert len(set(kinds)) == 4, (it["id"], vals)   # no two options equal in value either
        for d in it["decoys"]:
            assert it["type"] in ERR_TYPES[d["err"]], (it["id"], d)   # each error's line is written for these types only
    from collections import Counter
    c = Counter((i["stage"], i["type"]) for i in items)
    assert all(v == 24 for v in c.values()) and len(c) == 8, c
    return True


if __name__ == "__main__":
    items = bank()
    check(items)
    from collections import Counter
    for k, v in sorted(Counter((i["stage"], i["type"]) for i in items).items()):
        print(k, v)
    print("total", len(items))
    blob = "".join(json.dumps(i, separators=(",", ":"), ensure_ascii=False) + "\n" for i in items)
    print("sha256", hashlib.sha256(blob.encode("utf-8")).hexdigest())
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8", newline="\n").write(blob)
    if "--show" in sys.argv:
        for i in items:
            print(i["id"], "|", i["prompt"], "|", i["answer"], "|", [(d["val"], d["err"]) for d in i["decoys"]])
