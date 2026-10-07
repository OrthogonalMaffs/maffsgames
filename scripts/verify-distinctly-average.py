#!/usr/bin/env python3
# ci-line: B2 | Distinctly Average (independent recomputation) |
"""Independent verification for distinctly-average (docs/todo.md, 29 Sep 2026 build; extended 29 Sep 2026).

WHY THIS READS THE LIVE PAGE, NOT A HAND-COPY OF THE GENERATOR
----------------------------------------------------------------------------
Same reasoning as verify-log-laws.py / verify-quadratic-factoriser.py: a Python
re-implementation of the JS generator (buildMeanItems, buildMedianItems, ...) could
drift from the real one and would then only be verifying itself. Instead this script
launches the stub server, loads the live page under Playwright, and reads back
window.DA_ITEMS -- the RAW parameters (data/values/freqs/n) behind every item, not
just its rendered display strings. It then recomputes each item's answer straight
from those raw numbers with fractions.Fraction, completely independently of however
the generator built them, and asserts the recomputed value matches the stored
`correct` field exactly. It also reads window.DA_PROMPTS (the prompt each item is
shown with) and window.DA_MC (the misconception explanations).

WHAT IT ASSERTS, PER ITEM
----------------------------------------------------------------------------
  - mean / freqMean: the exact mean (a Fraction) reduces to a whole number (KS3) or
    to an exact 1-decimal value (GCSE freqMean, denominator dividing 10) -- and
    matches the stored `correct` string exactly, char for char.
  - median / freqMedian: recomputed from the item's own sorted data (or cumulative
    frequency), matches `correct` exactly, including the ".5" formatting for an
    even-n split.
  - modeUnique / modeBimodal: the value(s) with strictly the highest frequency
    match `correct` (bimodal: exactly two tied values, "v1 and v2" ascending).
  - range: max(data) - min(data) matches `correct`.
  - missing: total = mean * n (asserted to be an exact integer) minus the sum of
    the known values matches `correct`.
  - compareMean / compareRange: recomputed from data.a / data.b. The answer is the
    higher-mean / smaller-range set, or "They are the same" when the statistic is
    equal. Between 10% and 25% of each compare family is an equal-statistic item, so
    the third option is a live answer and not one a student could eliminate on sight.
  - outlierId / outlierMean / outlierCompare (GCSE only): the outlier is DERIVED from
    the raw data and must satisfy the construction rule below; the answer is then
    recomputed. For outlierCompare, |change in mean| > |change in median| is asserted
    on every item, in exact arithmetic.
  - every item's display data is NOT already sorted ascending (n >= 3) -- the
    platform requirement that data is always presented unsorted.
  - no distractor equals `correct`, and no two distractors on the same item share a
    value -- both asserted as hard bank defects, not tolerated the way
    MaffsOptions.build() tolerates a collision at render time.

EVERY DISTRACTOR IS RECOMPUTED FROM ITS MISCONCEPTION TAG
----------------------------------------------------------------------------
Knowing a tag is a *known key* is not enough: a distractor mislabelled with the
wrong tag makes the wrong-answer screen tell a struggling student they made a
mistake they did not make. So TAGS below maps each tag to a function that computes,
from the item's raw parameters and with fractions.Fraction (never floats), the
value(s) a student making THAT mistake would give. The script recomputes every
distractor of every item in both tiers and requires the stored value to be one of
them. A tag with no function FAILS the script, so a new tag cannot be added to the
game without a check being written for it. Every tag used must also have a
non-empty explanation in the game's MC catalogue.

Most tags produce exactly one value. A few name a *choice* rather than a number
("picked a value that is not the mode"); those return every value the mistake could
produce, and the stored distractor must be one of them.

PROMPTS (answer-shape leaks)
----------------------------------------------------------------------------
  - every mode question -- unique or bimodal, both tiers -- carries the IDENTICAL
    prompt, including "(There may be more than one value.)". A prompt that varies
    with the answer tells the student the shape of the answer.
  - within every other family the prompt is a single string. The one declared
    exception is outlierCompare, where half the items ask which average is LESS
    affected and half which is MORE affected, so the correct answer is not the same
    word every time; that mapping is asserted.
  - every family offers at least 3 options.

FORMAT SIGNATURES (the correct option must not be identifiable by its shape)
----------------------------------------------------------------------------
Each option is reduced to a format signature: every run of digits becomes `#`, every
other character and word is kept ("3 and 7" -> "# and #", "6.3" -> "#.#", "12" -> "#").
An item FAILS when the correct option's signature is unique among its options AND
the distractors share a shape the correct answer lacks -- the correct option is then
the only pair, the only decimal, the only option with a unit. (Categorical items, whose
options are all different words -- "Set A" / "Set B" / "They are the same" -- have
all-different signatures; nothing is singled out, so they pass. Read literally,
"correct signature is unique" would fail every one of them.) A family may be exempted
only through SIGNATURE_ALLOWLIST with a written reason; a stale entry fails.

A second, cross-family check covers families that SHARE a prompt (the two mode
families): if their option-shape multisets differ, the shape of the options tells the
student which family they are in, and so whether the answer is one value or two.
Known cases live in SHARED_PROMPT_CUES with a reason; a new one, or a stale entry, fails.

OUTLIER CONSTRUCTION RULE ("clearly separated", judged by eye at Foundation level)
----------------------------------------------------------------------------
  Data is 5 to 9 whole values in 1..50. Removing exactly one extreme value leaves a
  cluster of the other n-1 values spanning S, with 3 <= S <= 6; the removed value
  lies g beyond the nearest cluster value with g >= max(3*S, 10). Exactly one of
  the two extremes may satisfy this (else the item is ambiguous). No 1.5 x IQR test.

FAULT-INJECTION SELF-TEST
----------------------------------------------------------------------------
After verifying, the script mutates one distractor in every question family (an
off-by-one value, a flipped letter or a flipped direction), re-runs the checks on
the mutated copy, and requires each mutation to be caught. It also breaks the mode
prompt, the outlier separation and the mean-versus-median inequality and requires
those to be caught. Any mutation that slips through fails the script. This runs on
every CI pass; `--no-selftest` skips it.

USAGE
----------------------------------------------------------------------------
    python scripts/verify-distinctly-average.py
    python scripts/verify-distinctly-average.py --no-selftest
"""
import asyncio
import copy
import json
import math
import os
import re
import sys
from urllib.parse import urlsplit
from collections import Counter
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "distinctly-average"
PORT = None  # set by main() to the free port the stub server got

SAME = "They are the same"
BOTH = "Both are affected equally"
MODE_HINT = "(There may be more than one value.)"
OUTLIER_CATS = ("outlierId", "outlierMean", "outlierCompare")
OUT_MIN_ITEMS, OUT_MIN_PER_TYPE = 40, 8
OUT_S_MIN, OUT_S_MAX, OUT_GAP_FACTOR, OUT_GAP_FLOOR = 3, 6, 3, 10
OUT_N_MIN, OUT_N_MAX, OUT_VAL_MIN, OUT_VAL_MAX = 5, 9, 1, 50
EQUAL_SHARE_MIN, EQUAL_SHARE_MAX = Fraction(10, 100), Fraction(25, 100)
# The one family allowed to show more than one prompt, and how many.
PROMPT_EXCEPTIONS = {"outlierCompare": 2}
# Families whose format-signature leaks are TRACKED rather than failed, as
# {family: (exact number of leaking items, reason)}. Like data/check-ledger.json: a leak
# beyond the pinned number is new and fails; fewer than the pinned number is stale and
# fails (lower the number or delete the entry). Expected to stay empty -- a family whose
# correct answer can only be told apart by format should be fixed in its generator. The
# one entry below exists only because the contract said to stop and report, not fix,
# a family with more than 25% of its items failing.
SIGNATURE_ALLOWLIST = {
    "freqMean": (6, "the correct answer is the only decimal on 6 of 20 items (30%): every distractor happens "
                    "to be a whole number when the sum divides by the row count. Over the 25% stop threshold, "
                    "so reported to Jon, not redesigned. A tested proposal is in docs/todo.md."),
}
# Pairs of families that share a prompt and whose option shapes differ, each with the
# reason it is tolerated for now. Keys are sorted tuples of family names.
SHARED_PROMPT_CUES = {
    ("modeBimodal", "modeUnique"):
        "bimodal items carry pair options ('# and #') and unique-mode items do not, so the options "
        "reveal which family an item is from. Closing it means adding named pair distractors to the "
        "unique family too (a second family redesign): reported to Jon, whose call it is.",
}


# ---------------------------------------------------------------------------
# exact arithmetic helpers
# ---------------------------------------------------------------------------
def parse_decimal_to_fraction(s):
    """Parse a JS-formatted decimal string ("12", "-3", "4.5") into an exact
    Fraction -- never via float(), so no binary-fraction rounding can sneak in."""
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".")
        value = Fraction(int(whole or "0") * (10 ** len(frac)) + int(frac), 10 ** len(frac))
    else:
        value = Fraction(int(s), 1)
    return -value if neg else value


def tenths_str(tenths):
    neg = tenths < 0
    whole, frac = divmod(abs(tenths), 10)
    s = str(whole) if frac == 0 else "%d.%d" % (whole, frac)
    return ("-" + s) if neg else s


def format_exact(fr):
    """Format a Fraction that is an exact multiple of 1/10 the way the game does
    (whole number, or one decimal place). Returns None if it is not."""
    tenths = fr * 10
    if tenths.denominator != 1:
        return None
    return tenths_str(tenths.numerator)


def round1(fr):
    """Exact half-up rounding to 1 d.p., formatted like the game's roundStr()
    (Math.round is half-up, and integers print without a decimal point)."""
    return tenths_str(math.floor(fr * 10 + Fraction(1, 2)))


def mean_of(values):
    return Fraction(sum(values), len(values))


def median_of(values):
    s = sorted(values)
    n = len(s)
    return Fraction(s[(n - 1) // 2]) if n % 2 == 1 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def counts_of(values):
    c = {}
    for v in values:
        c[v] = c.get(v, 0) + 1
    return c


def modes_of(values):
    c = counts_of(values)
    best = max(c.values())
    return sorted(v for v, k in c.items() if k == best), best


# ---------------------------------------------------------------------------
# outlier analysis -- derived from the raw data, never trusted from the item
# ---------------------------------------------------------------------------
def analyse_outlier(data):
    """Return (info, problems). info = dict(o, side, cluster, S, g) for the single
    extreme value that satisfies the construction rule; problems is a list of
    strings (empty when the data is a valid outlier set)."""
    problems = []
    n = len(data)
    if not (OUT_N_MIN <= n <= OUT_N_MAX):
        problems.append("n=%d is outside %d..%d" % (n, OUT_N_MIN, OUT_N_MAX))
    if any((v < OUT_VAL_MIN or v > OUT_VAL_MAX) for v in data):
        problems.append("a value is outside %d..%d" % (OUT_VAL_MIN, OUT_VAL_MAX))
    s = sorted(data)
    found = []
    for side in ("high", "low"):
        cluster = s[:-1] if side == "high" else s[1:]
        o = s[-1] if side == "high" else s[0]
        span = cluster[-1] - cluster[0]
        gap = (o - cluster[-1]) if side == "high" else (cluster[0] - o)
        if OUT_S_MIN <= span <= OUT_S_MAX and gap >= max(OUT_GAP_FACTOR * span, OUT_GAP_FLOOR):
            found.append(dict(o=o, side=side, cluster=cluster, S=span, g=gap))
    if len(found) != 1:
        problems.append("%d extremes satisfy the separation rule (need exactly 1): sorted=%r" % (len(found), s))
        return None, problems
    return found[0], problems


def mean_shift_vs_median_shift(data, info):
    """(|change in mean|, |change in median|) when the outlier is removed, exact."""
    rest = list(data)
    rest.remove(info["o"])
    return abs(mean_of(data) - mean_of(rest)), abs(median_of(data) - median_of(rest))


# ---------------------------------------------------------------------------
# TAGS: misconception tag -> function(item) -> set of value strings that a student
# making THAT mistake would give. An empty set means "this tag cannot arise on this
# item", which is itself a failure when the tag is present on it.
# ---------------------------------------------------------------------------
TAGS = {}


def tag(name):
    def deco(fn):
        TAGS[name] = fn
        return fn
    return deco


def _stats_ab(item):
    a, b = item["data"]["a"], item["data"]["b"]
    return (mean_of(a), mean_of(b), max(a) - min(a), max(b) - min(b))


def _letter_by(item, which):
    """Letter of the set with the larger/smaller range or higher/lower mean.
    Empty set when the two are equal (no such set exists)."""
    ma, mb, ra, rb = _stats_ab(item)
    pick = {"larger_range": (ra, rb, True), "smaller_range": (ra, rb, False),
            "higher_mean": (ma, mb, True), "lower_mean": (ma, mb, False)}[which]
    x, y, larger = pick
    if x == y:
        return set()
    return {"A"} if ((x > y) == larger) else {"B"}


@tag("sum_not_divided")
def _(item):
    if item["cat"] == "mean":
        return {str(sum(item["data"]))}
    if item["cat"] == "freqMean":
        return {str(sum(v * f for v, f in zip(item["data"]["values"], item["data"]["freqs"])))}
    return set()


@tag("value_not_mean")
def _(item):
    return {str(v) for v in set(item["data"])} if item["cat"] == "mean" else set()


@tag("wrong_n")
def _(item):
    cat = item["cat"]
    if cat == "mean":
        return {round1(Fraction(sum(item["data"]), len(item["data"]) - 1))}
    if cat == "freqMean":
        s = sum(v * f for v, f in zip(item["data"]["values"], item["data"]["freqs"]))
        return {round1(Fraction(s, len(item["data"]["values"])))}   # divided by the number of ROWS
    if cat == "missing":
        n = item["n"]
        return {round1(parse_decimal_to_fraction(item["meanStr"]) * (n - 1) - sum(item["data"]))}
    return set()


@tag("unsorted_median")
def _(item):
    d, n = item["data"], len(item["data"])
    if item["cat"] != "median":
        return set()
    return {format_exact(Fraction(d[(n - 1) // 2]) if n % 2 else Fraction(d[n // 2 - 1] + d[n // 2], 2))}


@tag("position_not_value")
def _(item):
    if item["cat"] == "median":
        return {format_exact(Fraction(len(item["data"]) + 1, 2))}
    if item["cat"] == "freqMedian":
        return {format_exact(Fraction(sum(item["data"]["freqs"]) + 1, 2))}
    return set()


@tag("mean_not_median")
def _(item):
    if item["cat"] == "median":
        return {round1(mean_of(item["data"]))}
    if item["cat"] == "freqMedian":
        v, f = item["data"]["values"], item["data"]["freqs"]
        return {round1(Fraction(sum(a * b for a, b in zip(v, f)), sum(f)))}
    return set()


@tag("wrong_middle")
def _(item):
    d = sorted(item["data"])
    n = len(d)
    return {str(d[n // 2 - 1])} if (item["cat"] == "median" and n % 2 == 0) else set()


@tag("range_as_max")
def _(item):
    return {str(max(item["data"]))} if item["cat"] == "range" else set()


@tag("range_as_min")
def _(item):
    return {str(min(item["data"]))} if item["cat"] == "range" else set()


@tag("mean_not_range")
def _(item):
    return {round1(mean_of(item["data"]))} if item["cat"] == "range" else set()


@tag("mode_as_frequency")
def _(item):
    return {str(modes_of(item["data"])[1])} if item["cat"] in ("modeUnique", "modeBimodal") else set()


@tag("wrong_value_picked")
def _(item):
    if item["cat"] != "modeUnique":
        return set()
    c = counts_of(item["data"])
    best = max(c.values())
    return {str(v) for v, k in c.items() if k < best}


@tag("only_one_mode")
def _(item):
    return {str(v) for v in modes_of(item["data"])[0]} if item["cat"] == "modeBimodal" else set()


def _pair(a, b):
    lo, hi = sorted((a, b))
    return "%d and %d" % (lo, hi)


@tag("mode_and_wrong_value")          # exactly one of the two values is a mode
def _(item):
    if item["cat"] != "modeBimodal":
        return set()
    modes, _n = modes_of(item["data"])
    return {_pair(m, w) for m in modes for w in set(item["data"]) - set(modes)}


@tag("picked_extreme_values")         # the two largest, or the two smallest, distinct values
def _(item):
    if item["cat"] != "modeBimodal":
        return set()
    ds = sorted(set(item["data"]))
    return {_pair(ds[-2], ds[-1]), _pair(ds[0], ds[1])} if len(ds) >= 3 else set()


@tag("ignored_frequency")
def _(item):
    if item["cat"] != "freqMean":
        return set()
    v = item["data"]["values"]
    return {round1(Fraction(sum(v), len(v)))}


@tag("wrong_cumulative_row")
def _(item):
    if item["cat"] != "freqMedian":
        return set()
    v, f = item["data"]["values"], item["data"]["freqs"]
    pos = Fraction(sum(f) + 1, 2)
    cum, row = 0, len(v) - 1
    for i, fr in enumerate(f):
        cum += fr
        if pos <= cum:
            row = i
            break
    return {str(v[i]) for i in (row - 1, row + 1) if 0 <= i < len(v)}   # "one row away"


@tag("missing_equals_mean")
def _(item):
    return {item["meanStr"]} if item["cat"] == "missing" else set()


@tag("gave_sum_of_knowns")
def _(item):
    return {str(sum(item["data"]))} if item["cat"] == "missing" else set()


@tag("compared_wrong_stat")           # the mean question, answered from the ranges: picks the wider set
def _(item):
    return _letter_by(item, "larger_range") if item["cat"] == "compareMean" else set()


@tag("range_bigger_is_better")
def _(item):
    return _letter_by(item, "larger_range") if item["cat"] == "compareRange" else set()


@tag("consistent_means_higher")       # equal means: picks the tighter set as if consistency raised the mean
def _(item):
    return _letter_by(item, "smaller_range") if item["cat"] == "compareMean" else set()


@tag("compared_means_not_ranges")     # equal ranges: answers from the means instead
def _(item):
    return _letter_by(item, "higher_mean") if item["cat"] == "compareRange" else set()


@tag("lower_mean_more_consistent")
def _(item):
    return _letter_by(item, "lower_mean") if item["cat"] == "compareRange" else set()


@tag("assumed_means_equal")           # "They are the same" -- a wrong answer only when the means differ
def _(item):
    if item["cat"] != "compareMean":
        return set()
    ma, mb, _, _ = _stats_ab(item)
    return {SAME} if ma != mb else set()


@tag("assumed_ranges_equal")
def _(item):
    if item["cat"] != "compareRange":
        return set()
    _, _, ra, rb = _stats_ab(item)
    return {SAME} if ra != rb else set()


def _outlier_info(item):
    if item["cat"] not in OUTLIER_CATS:
        return None
    info, problems = analyse_outlier(item["data"])
    return info if not problems else None


@tag("picked_largest")
def _(item):
    info = _outlier_info(item)
    return {str(max(item["data"]))} if (info and item["cat"] == "outlierId" and info["side"] == "low") else set()


@tag("picked_smallest")
def _(item):
    info = _outlier_info(item)
    return {str(min(item["data"]))} if (info and item["cat"] == "outlierId" and info["side"] == "high") else set()


@tag("picked_neighbour")              # the cluster value nearest the outlier
def _(item):
    info = _outlier_info(item)
    if not (info and item["cat"] == "outlierId"):
        return set()
    return {str(info["cluster"][-1] if info["side"] == "high" else info["cluster"][0])}


@tag("picked_typical_value")          # the middle value of the sorted data
def _(item):
    info = _outlier_info(item)
    if not (info and item["cat"] == "outlierId" and len(item["data"]) % 2 == 1):
        return set()
    return {format_exact(median_of(item["data"]))}


def _direction_after_removal(item):
    info = _outlier_info(item)
    if not info:
        return None
    rest = list(item["data"])
    rest.remove(info["o"])
    m_all, m_rest = mean_of(item["data"]), mean_of(rest)
    if m_rest == m_all:
        return None
    return "Goes up" if m_rest > m_all else "Goes down"


@tag("mean_direction_reversed")
def _(item):
    if item["cat"] != "outlierMean":
        return set()
    d = _direction_after_removal(item)
    return {"Goes down" if d == "Goes up" else "Goes up"} if d else set()


@tag("mean_unaffected")
def _(item):
    if item["cat"] != "outlierMean":
        return set()
    return {"Stays the same"} if _direction_after_removal(item) else set()   # the mean DOES move


@tag("mean_thought_robust")           # asked which is LESS affected; picked the mean
def _(item):
    return {"The mean"} if (item["cat"] == "outlierCompare" and item.get("ask") == "less") else set()


@tag("median_thought_sensitive")      # asked which is MORE affected; picked the median
def _(item):
    return {"The median"} if (item["cat"] == "outlierCompare" and item.get("ask") == "more") else set()


@tag("all_averages_equal")
def _(item):
    return {BOTH} if item["cat"] == "outlierCompare" else set()


# ---------------------------------------------------------------------------
# per-family answer recomputation (the stored `correct`)
# ---------------------------------------------------------------------------
def v_mean(item):
    data, n, out = item["data"], item["n"], []
    if len(data) != n:
        out.append("n=%d but data has %d values" % (n, len(data)))
    m = mean_of(data)
    if m.denominator != 1:
        return out + ["mean %r is not a whole number as the KS3 spec requires" % (m,)]
    if str(m.numerator) != item["correct"]:
        out.append("recomputed mean %r != stored correct %r" % (m.numerator, item["correct"]))
    return out


def v_median(item):
    data, n, out = item["data"], item["n"], []
    expected_parity = "odd" if n % 2 == 1 else "even"
    if item.get("parity") != expected_parity:
        out.append("n=%d but parity tagged %r" % (n, item.get("parity")))
    got = format_exact(median_of(data))
    if got != item["correct"]:
        out.append("recomputed median %r != stored correct %r" % (got, item["correct"]))
    return out


def v_mode_unique(item):
    winners, _ = modes_of(item["data"])
    if len(winners) != 1:
        return ["expected a unique mode, found %d tied values %r" % (len(winners), winners)]
    return [] if str(winners[0]) == item["correct"] else ["recomputed mode %r != stored correct %r" % (winners[0], item["correct"])]


def v_mode_bimodal(item):
    winners, _ = modes_of(item["data"])
    if len(winners) != 2:
        return ["expected exactly two tied modes, found %d %r" % (len(winners), winners)]
    expected = "%d and %d" % (winners[0], winners[1])
    return [] if expected == item["correct"] else ["recomputed bimodal mode %r != stored correct %r" % (expected, item["correct"])]


def v_range(item):
    expected = max(item["data"]) - min(item["data"])
    return [] if str(expected) == item["correct"] else ["recomputed range %r != stored correct %r" % (expected, item["correct"])]


def v_freq_mean(item):
    values, freqs, out = item["data"]["values"], item["data"]["freqs"], []
    if len(values) != len(freqs):
        return ["values/freqs length mismatch"]
    total = sum(freqs)
    if total != item["n"]:
        out.append("sum(freqs)=%d != stored n=%d" % (total, item["n"]))
    mean = Fraction(sum(v * f for v, f in zip(values, freqs)), total)
    got = format_exact(mean)
    if got is None:
        return out + ["mean %r is not exactly representable to 1 d.p." % (mean,)]
    if got != item["correct"]:
        out.append("recomputed frequency-table mean %r != stored correct %r" % (got, item["correct"]))
    return out


def v_freq_median(item):
    values, freqs, out = item["data"]["values"], item["data"]["freqs"], []
    total = sum(freqs)
    if total != item["n"]:
        out.append("sum(freqs)=%d != stored n=%d" % (total, item["n"]))
    if total % 2 != 1:
        return out + ["total frequency %d is not odd -- freqMedian requires an exact single-row position" % total]
    pos, cum, correct_val = (total + 1) // 2, 0, values[-1]
    for v, f in zip(values, freqs):
        cum += f
        if pos <= cum:
            correct_val = v
            break
    if str(correct_val) != item["correct"]:
        out.append("recomputed frequency-table median %r != stored correct %r" % (correct_val, item["correct"]))
    return out


def v_missing(item):
    data, n, out = item["data"], item["n"], []
    if len(data) != n - 1:
        out.append("n=%d but only %d known values given" % (n, len(data)))
    total = parse_decimal_to_fraction(item["meanStr"]) * n
    if total.denominator != 1:
        return out + ["mean x n=%d is not an exact whole total" % n]
    missing = total.numerator - sum(data)
    if str(missing) != item["correct"]:
        out.append("recomputed missing value %r != stored correct %r" % (missing, item["correct"]))
    return out


def v_compare(item, use_mean):
    a, b = item["data"]["a"], item["data"]["b"]
    ma, mb, ra, rb = _stats_ab(item)
    if use_mean:
        expected = SAME if ma == mb else ("A" if ma > mb else "B")
    else:
        expected = SAME if ra == rb else ("A" if ra < rb else "B")
    out = []
    if expected != item["correct"]:
        out.append("recomputed comparison %r != stored correct %r" % (expected, item["correct"]))
    if ma != mb and ra != rb:
        # the deliberate inverse construction: higher mean <=> smaller range
        if ("A" if ma > mb else "B") != ("A" if ra < rb else "B"):
            out.append("higher-mean set does not have the smaller range -- the deliberate "
                       "inverse construction the unequal items rely on is broken")
    if len(a) != len(b):
        out.append("sets differ in size (%d vs %d)" % (len(a), len(b)))
    return out


def v_outlier(item):
    data, out = item["data"], []
    if len(data) != item["n"]:
        out.append("n=%d but data has %d values" % (item["n"], len(data)))
    info, problems = analyse_outlier(data)
    out.extend(problems)
    if not info:
        return out
    if item.get("side") != info["side"]:
        out.append("stored side %r != derived side %r" % (item.get("side"), info["side"]))
    cat = item["cat"]
    if cat == "outlierId":
        if len(data) % 2 != 1:
            out.append("outlierId needs odd n (the 'typical value' distractor is the median): n=%d" % len(data))
        if item["correct"] != str(info["o"]):
            out.append("recomputed outlier %r != stored correct %r" % (info["o"], item["correct"]))
    elif cat == "outlierMean":
        d = _direction_after_removal(item)
        if d is None:
            out.append("removing the outlier does not change the mean -- the question would be ambiguous")
        elif d != item["correct"]:
            out.append("recomputed direction %r != stored correct %r" % (d, item["correct"]))
    elif cat == "outlierCompare":
        out.extend(v_mean_vs_median(item, info))
    return out


def v_mean_vs_median(item, info):
    out = []
    dm, dmed = mean_shift_vs_median_shift(item["data"], info)
    if not dm > dmed:
        out.append("|change in mean| %s is not strictly greater than |change in median| %s" % (dm, dmed))
    ask = item.get("ask")
    if ask not in ("less", "more"):
        return out + ["ask %r is not 'less' or 'more'" % (ask,)]
    expected = "The median" if ask == "less" else "The mean"    # holds because |dmean| > |dmedian|
    if item["correct"] != expected:
        out.append("ask=%r so the answer should be %r, stored %r" % (ask, expected, item["correct"]))
    return out


VERIFIERS = {
    "mean": v_mean, "median": v_median, "modeUnique": v_mode_unique, "modeBimodal": v_mode_bimodal,
    "range": v_range, "freqMean": v_freq_mean, "freqMedian": v_freq_median, "missing": v_missing,
    "compareMean": lambda item: v_compare(item, True), "compareRange": lambda item: v_compare(item, False),
    "outlierId": v_outlier, "outlierMean": v_outlier, "outlierCompare": v_outlier,
}


# ---------------------------------------------------------------------------
# item-level checks (return lists of failure strings so the self-test can reuse them)
# ---------------------------------------------------------------------------
def check_distractors(item, mc):
    out, seen, correct = [], set(), item["correct"]
    for d in item["distractors"]:
        val, t = d["val"], d["misconception"]
        if val == correct:
            out.append("distractor %r equals the correct answer %r" % (val, correct))
        if val in seen:
            out.append("two distractors share the value %r" % (val,))
        seen.add(val)
        fn = TAGS.get(t)
        if fn is None:
            out.append("tag %r has NO recompute function in verify-distinctly-average.py -- add one before using it" % t)
            continue
        allowed = fn(item)
        if val not in allowed:
            out.append("distractor %r is tagged %r but that mistake gives %s" % (val, t, sorted(allowed) if allowed else "nothing on this item"))
        if not (mc.get(t) or "").strip():
            out.append("tag %r has no explanation in the game's MC catalogue" % t)
    if len(item["distractors"]) + 1 < 3:
        out.append("only %d options -- every family needs at least 3" % (len(item["distractors"]) + 1))
    return out


def not_sorted_problem(data, where=""):
    if len(data) >= 3 and len(set(data)) > 1 and list(data) == sorted(data):
        return ["%sdata is presented already sorted ascending (%r)" % (where, data)]
    return []


def signature(option_text):
    """Format signature of one option: each run of digits becomes '#', all else kept."""
    return re.sub(r"\d+", "#", option_text)


def displayed(item, v):
    """The text the student sees on the button (mirrors optionLabel() in the game)."""
    if item["cat"] in ("compareMean", "compareRange") and v != SAME:
        return "Set " + v
    return v


def signature_leak(item):
    """None if fine, else a message: the correct option's shape is unique while the
    distractors share a shape it lacks."""
    opts = [displayed(item, v) for v in [item["correct"]] + [d["val"] for d in item["distractors"]]]
    sigs = [signature(o) for o in opts]
    counts = Counter(sigs)
    correct_sig = sigs[0]
    shared = sorted(k for k, n in counts.items() if n > 1 and k != correct_sig)
    if counts[correct_sig] == 1 and shared:
        return "format singles out the correct answer %r (signature %r, no other option has it); the distractors share %s" % (
            opts[0], correct_sig, ", ".join(repr(k) for k in shared))
    return None


def check_item(item, mc):
    out = []
    verifier = VERIFIERS.get(item["cat"])
    if verifier is None:
        return ["unknown category %r" % item["cat"]]
    out.extend(verifier(item))
    out.extend(check_distractors(item, mc))
    if item["cat"] not in SIGNATURE_ALLOWLIST:      # tracked families are counted in main() instead
        leak = signature_leak(item)
        if leak:
            out.append(leak)
    data = item["data"]
    if isinstance(data, list):
        out.extend(not_sorted_problem(data))
    elif "a" in data:
        out.extend(not_sorted_problem(data["a"], "set A: "))
        out.extend(not_sorted_problem(data["b"], "set B: "))
    return out


def canonical_data(item):
    """A hashable canonical form of an item's raw data, used only to count distinct
    parameter sets -- not for correctness."""
    d = item["data"]
    key = {"ask": item.get("ask")}
    if isinstance(d, list):
        key["d"] = sorted(d)
    elif "values" in d:
        key.update(v=d["values"], f=d["freqs"])
    else:
        key.update(a=sorted(d["a"]), b=sorted(d["b"]))
    return json.dumps(key, sort_keys=True)


# ---------------------------------------------------------------------------
# tier-level checks
# ---------------------------------------------------------------------------
def check_prompts(tier, items, prompts):
    """Answer-shape leaks in the prompt text. Returns (failures, family table rows)."""
    out, fam = [], {}
    if len(prompts) != len(items):
        return ["DA_PROMPTS[%s] has %d entries for %d items" % (tier, len(prompts), len(items))], []
    for it, pr in zip(items, prompts):
        fam.setdefault(it["cat"], []).append((it, pr))
    rows = []
    for cat, lst in fam.items():
        pset = sorted({p for _, p in lst})
        opts = sorted({len(i["distractors"]) + 1 for i, _ in lst})
        allowed = PROMPT_EXCEPTIONS.get(cat, 1)
        if len(pset) != allowed:
            out.append("family %s shows %d distinct prompts, expected %d: %r" % (cat, len(pset), allowed, pset))
        if min(opts) < 3:
            out.append("family %s offers %d options, minimum is 3" % (cat, min(opts)))
        if cat == "outlierCompare":
            by_ask = {}
            for i, p in lst:
                by_ask.setdefault(i.get("ask"), set()).add((p, i["correct"]))
            for ask, pairs in by_ask.items():
                if len(pairs) != 1:
                    out.append("outlierCompare ask=%r has several prompt/answer pairs: %r" % (ask, pairs))
        rows.append((cat, len(lst), opts, len(pset)))
    return out, rows


def check_mode_prompts(all_tiers):
    """One identical prompt on every mode question, both tiers, carrying the hint."""
    seen = set()
    for tier, (items, prompts) in all_tiers.items():
        for it, pr in zip(items, prompts):
            if it["cat"] in ("modeUnique", "modeBimodal"):
                seen.add(pr)
    out = []
    if len(seen) != 1:
        out.append("mode questions show %d different prompts (must be exactly 1): %r" % (len(seen), sorted(seen)))
    for p in seen:
        if MODE_HINT not in p:
            out.append("mode prompt lacks %r: %r" % (MODE_HINT, p))
    return out


def option_shape(item):
    return tuple(sorted(signature(displayed(item, v)) for v in [item["correct"]] + [d["val"] for d in item["distractors"]]))


def check_shared_prompt_cues(all_tiers, known=None):
    """Families with the SAME prompt must not be told apart by the shape of their options."""
    known = SHARED_PROMPT_CUES if known is None else known
    groups = {}
    for tier, (items, prompts) in all_tiers.items():
        for it, pr in zip(items, prompts):
            groups.setdefault(pr, {}).setdefault(it["cat"], set()).add(option_shape(it))
    seen, out = set(), []
    for pr, fams in groups.items():
        names = sorted(fams)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if fams[names[i]] != fams[names[j]]:
                    pair = (names[i], names[j])
                    seen.add(pair)
                    if pair not in known:
                        out.append("families %s and %s share a prompt but their option shapes differ (%s vs %s): "
                                   "the options tell the student which family they are in" % (
                                       pair[0], pair[1], sorted(fams[names[i]])[:3], sorted(fams[names[j]])[:3]))
    for pair, reason in known.items():
        if pair not in seen:
            out.append("SHARED_PROMPT_CUES lists %s but it no longer occurs -- remove the stale entry (%s)" % (pair, reason[:60]))
    return out


def check_tier_shape(tier, items):
    out = []
    if len(items) < 50:
        out.append("tier %r has %d items, needs >= 50" % (tier, len(items)))
    distinct = {(it["cat"], it["n"], canonical_data(it)) for it in items}
    if len(distinct) < 200:
        out.append("tier %r has only %d distinct parameter sets, needs >= 200" % (tier, len(distinct)))
    ids = [it["id"] for it in items]
    if len(set(ids)) != len(ids):
        out.append("duplicate item ids")
    if tier == "ks3":
        stray = sorted({it["cat"] for it in items if it["cat"] in OUTLIER_CATS})
        if stray:
            out.append("outlier families %r must be GCSE only" % stray)
        return out
    per_type = {c: [it for it in items if it["cat"] == c] for c in OUTLIER_CATS}
    total = sum(len(v) for v in per_type.values())
    if total < OUT_MIN_ITEMS:
        out.append("only %d outlier items, needs >= %d" % (total, OUT_MIN_ITEMS))
    for c, lst in per_type.items():
        if len(lst) < OUT_MIN_PER_TYPE:
            out.append("%s has %d items, needs >= %d" % (c, len(lst), OUT_MIN_PER_TYPE))
        d = {(it["n"], canonical_data(it)) for it in lst}
        if len(d) != len(lst):
            out.append("%s has %d items but only %d distinct parameter sets" % (c, len(lst), len(d)))
        sides = {s: sum(1 for it in lst if it.get("side") == s) for s in ("high", "low")}
        if min(sides.values()) < OUT_MIN_PER_TYPE // 2:
            out.append("%s sides are unbalanced: %r" % (c, sides))
    ids_ = per_type["outlierId"]
    positions = set()
    for it in ids_:
        info, _ = analyse_outlier(it["data"])
        if info:
            positions.add(it["data"].index(info["o"]))
    if len(positions) < 3:
        out.append("the outlier sits in only %d distinct positions across outlierId items -- position gives the answer away" % len(positions))
    for c in ("compareMean", "compareRange"):
        lst = [it for it in items if it["cat"] == c]
        eq = sum(1 for it in lst if it["correct"] == SAME)
        share = Fraction(eq, len(lst)) if lst else Fraction(0)
        if not (EQUAL_SHARE_MIN <= share <= EQUAL_SHARE_MAX):
            out.append("%s: %d of %d items are equal-statistic (%.0f%%), expected 10-25%%" % (c, eq, len(lst), float(share) * 100))
    return out


# ---------------------------------------------------------------------------
# fault-injection self-test
# ---------------------------------------------------------------------------
def mutation_candidates(item, d):
    """Plausible wrong replacements for a distractor value: numeric off-by-one, a
    flipped letter, a flipped direction or average. Tried in order until one is NOT
    an admissible value for the tag and does not collide with the correct answer."""
    v = d["val"]
    cands = []
    if v in ("A", "B"):
        cands.append("B" if v == "A" else "A")
    if v == "Goes up":
        cands.append("Goes down")
    if v == "Goes down":
        cands.append("Goes up")
    if v == "The mean":
        cands.append("The median")
    if v == "The median":
        cands.append("The mean")
    try:
        f = parse_decimal_to_fraction(v)
        cands += [round1(f + 1), round1(f - 1), round1(f + Fraction(1, 10)), round1(f + 7)]
    except (ValueError, IndexError):
        pass
    cands += [v + "x", "zzz"]
    return cands


def run_selftest(tiers, mc):
    """Mutate one distractor in each question family and require the checks to fail.
    Returns (all_caught, report lines)."""
    lines, ok = [], True
    pool = {}
    for tier in ("gcse", "ks3"):
        for it in tiers[tier][0]:
            pool.setdefault(it["cat"], (tier, it))     # first item of each family, GCSE pool first
    for cat, (tier, it) in sorted(pool.items()):
        if check_item(it, mc):
            lines.append("  %-15s baseline item already fails -- cannot inject" % cat)
            ok = False
            continue
        d0 = it["distractors"][0]
        allowed = TAGS[d0["misconception"]](it)
        new = next((c for c in mutation_candidates(it, d0)
                    if c not in allowed and c != it["correct"] and c not in {x["val"] for x in it["distractors"]}), None)
        if new is None:
            lines.append("  %-15s no usable mutation found" % cat)
            ok = False
            continue
        bad = copy.deepcopy(it)
        bad["distractors"][0]["val"] = new
        msgs = check_item(bad, mc)
        caught = any(("tagged %r" % d0["misconception"]) in m for m in msgs)
        ok = ok and caught
        lines.append("  %-15s %-26s %-8s -> %-8s %s" % (cat, d0["misconception"], repr(d0["val"]), repr(new),
                                                       "CAUGHT" if caught else "*** MISSED ***"))
        # The failure this whole check exists for: the VALUE is right for some mistake, but
        # the item carries the wrong TAG, so the explanation blames the student for the
        # wrong error. Swap two distractors' tags (values untouched) and require a catch.
        pair = next(((i, j) for i in range(len(it["distractors"])) for j in range(i + 1, len(it["distractors"]))
                     if it["distractors"][i]["misconception"] != it["distractors"][j]["misconception"]), None)
        if pair is None:
            lines.append("  %-15s %-26s (all distractors share one tag -- no swap possible)" % (cat, "tag swap"))
            continue
        swapped = copy.deepcopy(it)
        i, j = pair
        ti, tj = swapped["distractors"][i]["misconception"], swapped["distractors"][j]["misconception"]
        swapped["distractors"][i]["misconception"], swapped["distractors"][j]["misconception"] = tj, ti
        caught2 = any("is tagged" in m for m in check_item(swapped, mc))
        ok = ok and caught2
        lines.append("  %-15s %-26s %-8s <-> %-7s %s" % (cat, "tag swap", ti, tj, "CAUGHT" if caught2 else "*** MISSED ***"))
    # guards that are not a single distractor
    all_prompts = {t: (tiers[t][0], tiers[t][1]) for t in tiers}
    broken = {t: (i, list(p)) for t, (i, p) in all_prompts.items()}
    for idx, it in enumerate(broken["gcse"][0]):
        if it["cat"] == "modeBimodal":
            broken["gcse"][1][idx] = broken["gcse"][1][idx].replace(" " + MODE_HINT, "")
            break
    c1 = bool(check_mode_prompts(broken))
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("mode prompt", "hint dropped on 1 item", "", "", "CAUGHT" if c1 else "*** MISSED ***"))
    src = next(it for it in tiers["gcse"][0] if it["cat"] == "outlierId")
    near = copy.deepcopy(src)
    info, _ = analyse_outlier(near["data"])
    j = near["data"].index(info["o"])
    near["data"][j] = near["data"][j] - 6 if info["side"] == "high" else near["data"][j] + 6   # pull the outlier closer
    c2 = any("separation rule" in m for m in v_outlier(near))
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("outlier rule", "outlier pulled 6 closer", "", "", "CAUGHT" if c2 else "*** MISSED ***"))
    fake = {"cat": "outlierCompare", "ask": "less", "correct": "The median", "data": [1, 10, 20, 21, 23], "n": 5, "side": "high"}
    fake_info = {"o": 23, "side": "high", "cluster": [1, 10, 20, 21], "S": 20, "g": 2}
    c3 = any("not strictly greater" in m for m in v_mean_vs_median(fake, fake_info))
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("mean vs median", "median moves more", "", "", "CAUGHT" if c3 else "*** MISSED ***"))
    orphan = copy.deepcopy(pool["mean"][1])
    orphan["distractors"][0]["misconception"] = "a_tag_with_no_function"
    c4 = any("NO recompute function" in m for m in check_distractors(orphan, mc))
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("unmapped tag", "new tag, no function", "", "", "CAUGHT" if c4 else "*** MISSED ***"))
    # format-signature guards: a deliberately LEAKY item must FAIL, a categorical item must not
    leaky_pair = copy.deepcopy(next(it for it in tiers["gcse"][0] if it["cat"] == "modeBimodal"))
    leaky_pair["distractors"] = [dict(val=v, misconception="mode_as_frequency") for v in ("2", "5", "7")]   # all single values
    c5 = signature_leak(leaky_pair) is not None
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("format leak", "only pair among singles", repr(leaky_pair["correct"]), "singled out", "CAUGHT" if c5 else "*** MISSED ***"))
    leaky_dec = copy.deepcopy(next(it for it in tiers["gcse"][0] if it["cat"] == "freqMean"))
    leaky_dec["correct"] = "6.3"
    leaky_dec["distractors"] = [dict(val=v, misconception="wrong_n") for v in ("21", "6", "63")]              # all whole numbers
    c6 = signature_leak(leaky_dec) is not None
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("format leak", "only decimal among wholes", repr(leaky_dec["correct"]), "singled out", "CAUGHT" if c6 else "*** MISSED ***"))
    cat_item = next(it for it in tiers["gcse"][0] if it["cat"] == "compareMean")
    c7 = signature_leak(cat_item) is None
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("no false alarm", "categorical Set A/B/SAME", "", "", "OK" if c7 else "*** FALSE ALARM ***"))
    c8 = bool(check_shared_prompt_cues(all_prompts, known={}))
    lines.append("  %-15s %-26s %-8s -> %-8s %s" % ("shared-prompt cue", "modes told apart by shape", "", "", "CAUGHT" if c8 else "*** MISSED ***"))
    return ok and c1 and c2 and c3 and c4 and c5 and c6 and c7 and c8, lines


# ---------------------------------------------------------------------------
# page access
# ---------------------------------------------------------------------------
async def fetch_page_data():
    from playwright.async_api import async_playwright

    base = "http://127.0.0.1:%d" % PORT
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        await page.goto(base + "/games/" + SLUG + "/?cb=verify", wait_until="load", timeout=20000)
        await page.wait_for_timeout(300)
        data = await page.evaluate("() => ({items: window.DA_ITEMS || null, prompts: window.DA_PROMPTS || null, mc: window.DA_MC || null})")
        await browser.close()
        return data


def main():
    global PORT
    selftest = "--no-selftest" not in sys.argv
    # A free port chosen per run; raises bc.StubServerError, naming the cause, if the
    # stub server cannot start.
    server, base = bc.start_stub_server()
    PORT = urlsplit(base).port
    try:
        data = asyncio.run(fetch_page_data())
    finally:
        server.terminate()

    if not data["items"] or not data["prompts"] or not data["mc"]:
        print("FAIL: could not read window.DA_ITEMS / DA_PROMPTS / DA_MC from the live page")
        return 1
    mc = data["mc"]
    failures = []

    def fail(msg):
        failures.append(msg)
        print("FAIL: " + msg)

    tiers = {}
    for tier in ("ks3", "gcse"):
        if tier not in data["items"]:
            fail("window.DA_ITEMS.%s is missing" % tier)
            continue
        tiers[tier] = (data["items"][tier], data["prompts"][tier])

    used_tags = set()
    for tier, (items, prompts) in tiers.items():
        print("Verifying tier %r: %d items" % (tier, len(items)))
        for it in items:
            for m in check_item(it, mc):
                fail("%s/%s: %s" % (tier, it["id"], m))
            used_tags.update(d["misconception"] for d in it["distractors"])
        for m in check_tier_shape(tier, items):
            fail("tier %s: %s" % (tier, m))
        pfail, rows = check_prompts(tier, items, prompts)
        for m in pfail:
            fail("tier %s: %s" % (tier, m))
        distinct = {(it["cat"], it["n"], canonical_data(it)) for it in items}
        print("  %d distinct parameter sets" % len(distinct))
        print("  %-15s %5s  %-8s %s" % ("family", "items", "options", "distinct prompts"))
        for cat, n, opts, np in rows:
            print("  %-15s %5d  %-8s %d" % (cat, n, "/".join(map(str, opts)), np))
    for m in check_mode_prompts(tiers):
        fail(m)
    for m in check_shared_prompt_cues(tiers):
        fail(m)

    # Format-signature report: how many items per family have a correct option singled out by shape.
    print()
    print("Format-signature check (digit runs -> '#'; correct option must not be the only one of its shape):")
    leaks_by = {}
    for tier, (items, _) in tiers.items():
        fam_total, fam_leak = Counter(), Counter()
        for it in items:
            fam_total[it["cat"]] += 1
            if signature_leak(it):
                fam_leak[it["cat"]] += 1
        leaks_by[tier] = (fam_total, fam_leak)
        bad = {c: "%d/%d" % (fam_leak[c], fam_total[c]) for c in fam_total if fam_leak[c]}
        print("  %-5s items leaking: %d of %d   %s" % (tier, sum(fam_leak.values()), len(items), bad if bad else "none"))
    for fam, (pinned, reason) in SIGNATURE_ALLOWLIST.items():
        actual = max(lk[fam] for _, lk in leaks_by.values())
        print("  tracked, not failed: %s leaks on %d items (pinned at %d)" % (fam, actual, pinned))
        if actual > pinned:
            fail("%s now leaks on %d items, more than the %d pinned in SIGNATURE_ALLOWLIST -- a NEW leak" % (fam, actual, pinned))
        elif actual < pinned:
            fail("%s leaks on only %d items, fewer than the %d pinned in SIGNATURE_ALLOWLIST -- lower the number or remove the entry" % (fam, actual, pinned))

    unmapped = sorted(t for t in used_tags if t not in TAGS)
    print()
    print("Misconception tags used: %d, all with a recompute function: %s" % (len(used_tags), "yes" if not unmapped else "NO " + repr(unmapped)))
    orphans = sorted(t for t in mc if t not in used_tags)
    if orphans:
        print("Note: MC explanations no item uses (harmless): %s" % ", ".join(orphans))
    if "gcse" in tiers:
        g = tiers["gcse"][0]
        out_counts = {c: sum(1 for it in g if it["cat"] == c) for c in OUTLIER_CATS}
        print("Outlier items (gcse): %d total  %s" % (sum(out_counts.values()), out_counts))

    if selftest and not failures:
        print()
        print("Fault-injection self-test (one distractor mutated per family; each must be caught):")
        ok, lines = run_selftest(tiers, mc)
        for ln in lines:
            print(ln)
        if not ok:
            fail("fault-injection self-test: at least one mutation was not caught (or could not be built)")

    print()
    if failures:
        print("%d FAILURE(S)" % len(failures))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
