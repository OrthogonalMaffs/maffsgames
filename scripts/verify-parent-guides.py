#!/usr/bin/env python3
# ci-line: Parent guides (every stated figure recomputed from the page) |
"""Recompute the numeric claims in the /parents/ guides, reading every value FROM THE PAGES.

WHY IT READS THE PAGES
----------------------
The first version of this script (PR #9, 28 Sep 2026) recomputed each corrected
figure from numbers typed into the script itself, then separately checked that the
page carried a fixed phrase. That proves the arithmetic, not the page: change "25.2"
to "25.3" on a guide and every arithmetic check still passes, because none of them
looked at the guide.

So every check here is built the same way:

  1. find the claim on the published page (parents/<slug>/index.html), by a pattern
     over the page's text with its KaTeX source normalised to plain symbols;
  2. pull out the operands AND the stated answer from what the page says;
  3. recompute the answer from those operands and compare.

The script holds formulas, never answers. A claim the pattern cannot find is a FAIL
("reworded or removed?"), never a silent skip. Checks that are about the section
rather than one sentence -- the tier badges, the hub, the template -- read the pages,
parents/guide.js, data/dfe-gcse-parts.json, the roster and the linked game's source,
and nothing typed in here.

    python scripts/verify-parent-guides.py            # report and exit 0/1
    python scripts/verify-parent-guides.py --quiet    # failures only

The reasons each correction was needed (the counterexamples that made the old wording
false) are recorded in docs/migrate-parent-guides.md, not re-proved here: they are
about text that is no longer on any page, so no page edit could make them pass or fail.
"""
import argparse
import html
import json
import math
import os
import re
import sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENTS = os.path.join(ROOT, "parents")

results = []   # (finding, kind, ok, detail, source)


def check(finding, kind, ok, detail, src="page"):
    """src names where the checked values came from: "page" is a published guide or the
    hub; anything else names the other repo file(s) read. Nothing is ever the script."""
    results.append((finding, kind, bool(ok), detail, src))


# --------------------------------------------------------------------------- #
# Reading the pages
# --------------------------------------------------------------------------- #
def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def raw(slug):
    return read("parents/%s/index.html" % slug)


_BLOCK = re.compile(r"</?(?:p|li|div|br|h[1-6]|td|th|tr|ul|ol|section|table|thead|tbody)\b[^>]*>", re.I)


def latex_to_text(s):
    """KaTeX source -> the symbols a reader sees. Enough for this section's maths."""
    # Inline delimiters vanish (the prose around them already has its spaces);
    # display delimiters become a space, since they sit between blocks.
    s = s.replace("\\(", "").replace("\\)", "").replace("$$", " ")
    for _ in range(4):   # \text{..} and friends can nest inside \frac{..}{..}
        s = re.sub(r"\\(?:text|mathbf|mathrm|operatorname)\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"√(\1)", s)
        s = re.sub(r"\^\{([^{}]*)\}", r"^(\1)", s)
        s = re.sub(r"_\{([^{}]*)\}", r"_\1", s)
    s = s.replace("{,}", ",")
    for cmd, sym in (("\\div", "÷"), ("\\times", "×"), ("\\approx", "≈"), ("\\neq", "≠"),
                     ("\\rightarrow", "→"), ("\\implies", "⟹"), ("\\qquad", " "),
                     ("\\quad", " "), ("\\cdot", "·"), ("\\%", "%"), ("\\,", " "), ("\\;", " ")):
        s = s.replace(cmd, sym)
    s = s.replace("{", "").replace("}", "")
    return s


_TEXT_CACHE = {}


def text(slug):
    """The page as a reader sees it: no tags, entities decoded, KaTeX normalised."""
    if slug not in _TEXT_CACHE:
        h = raw(slug)
        h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S | re.I)
        h = re.sub(r"<head\b.*?</head>", " ", h, flags=re.S | re.I)
        h = _BLOCK.sub(" ", h)
        h = re.sub(r"<[^>]+>", "", h)
        h = html.unescape(h)
        h = latex_to_text(h)
        h = h.replace("\u2212", "-").replace("\u2019", "'").replace("\u00a0", " ")
        _TEXT_CACHE[slug] = re.sub(r"\s+", " ", h)
    return _TEXT_CACHE[slug]


def find(finding, slug, pattern, what):
    """Locate one claim on a page. Missing is a FAIL, never a skip."""
    m = re.search(pattern, text(slug))
    if not m:
        check(finding, "FOUND", False, "%s: claim not found on the page (reworded or removed?) -- %s"
              % (slug, what))
    return m


def n(s):
    """A number as the page prints it -> exact rational."""
    s = s.replace(",", "").replace("£", "").strip()
    return F(s)


def pct(p, a):
    return F(p) * F(a) / 100


def says(finding, slug, present=(), absent=()):
    t = text(slug)
    for s in present:
        check(finding, "TEXT", s in t, "%s says: %r" % (slug, s[:78]))
    for s in absent:
        check(finding, "TEXT", s not in t, "%s no longer says: %r" % (slug, s[:78]))


def poly(expr):
    """'(x+3)(x+4)' or 'x^2 + 7x + 12' -> callable. Digits, x, + - ( ) and ^ only."""
    e = expr.replace(" ", "").replace("^", "**")
    if not re.fullmatch(r"[0-9x+\-*()]+", e):
        raise ValueError("not a polynomial: %r" % expr)
    e = re.sub(r"(\d)(x|\()", r"\1*\2", e)
    e = re.sub(r"\)(\(|x|\d)", r")*\1", e)
    return lambda x: eval(e, {"__builtins__": {}}, {"x": x})


def same_poly(a, b):
    fa, fb = poly(a), poly(b)
    return all(fa(x) == fb(x) for x in range(-6, 7))


# --------------------------------------------------------------------------- #
# Mean, Median & Mode (the averages guide, new in this migration)
# --------------------------------------------------------------------------- #
def median_of(vals):
    s = sorted(vals)
    k = len(s)
    return s[k // 2] if k % 2 else F(s[k // 2 - 1] + s[k // 2], 2)


def averages():
    slug = "averages"
    # Worked example: the data, then each stated answer.
    m = find("AV", slug, r"five test scores: ([\d, ]+?)\. Find", "the worked example's data")
    if m:
        data = [int(v) for v in m.group(1).split(",")]
        check("AV", "COUNT", len(data) == 5, "worked example: %d values, the page calls them 'five'" % len(data))
        m2 = find("AV", slug, r"Mean = \(([\d + ]+)\)/\((\d+)\) = \((\d+)\)/\((\d+)\) = (\d+(?:\.\d+)?)",
                  "the worked mean")
        if m2:
            terms = [int(v) for v in m2.group(1).split("+")]
            check("AV", "ARITH", terms == data, "mean's numerator lists the data: %s" % terms)
            check("AV", "ARITH", int(m2.group(2)) == len(data) == int(m2.group(4)),
                  "divides by the count, %s" % m2.group(2))
            check("AV", "ARITH", int(m2.group(3)) == sum(data), "sum = %s" % m2.group(3))
            check("AV", "ARITH", n(m2.group(5)) == F(sum(data), len(data)),
                  "stated mean %s = %s / %s" % (m2.group(5), sum(data), len(data)))
        m3 = find("AV", slug, r"There are (\d+) values, so the middle one is the (\d+)(?:st|nd|rd|th) value\. "
                  r"Median = (\d+)", "the worked median")
        if m3:
            k, pos, med = int(m3.group(1)), int(m3.group(2)), n(m3.group(3))
            check("AV", "ARITH", k == len(data) and F(k + 1, 2) == pos,
                  "(n + 1) ÷ 2 = (%d + 1) ÷ 2 = %d, the position the page names" % (k, pos))
            check("AV", "ARITH", sorted(data)[pos - 1] == med == median_of(data),
                  "value in position %d of the sorted data is %s" % (pos, med))
        m4 = find("AV", slug, r"(\d+) appears twice; everything else appears once\. Mode = (\d+)", "the worked mode")
        if m4:
            v, mode = int(m4.group(1)), int(m4.group(2))
            counts = {x: data.count(x) for x in data}
            top = max(counts.values())
            check("AV", "ARITH", counts.get(v) == 2 and all(c == 1 for x, c in counts.items() if x != v),
                  "%d appears twice, every other value once: %s" % (v, counts))
            check("AV", "ARITH", [x for x, c in counts.items() if c == top] == [mode],
                  "the one value tied for most often is %d" % mode)
        m5 = find("AV", slug, r"Range = (\d+) - (\d+) = (\d+)", "the worked range")
        if m5:
            hi, lo, r = (int(g) for g in m5.groups())
            check("AV", "ARITH", (hi, lo) == (max(data), min(data)) and hi - lo == r,
                  "range = %d - %d = %d, highest minus lowest" % (hi, lo, r))
        m6 = find("AV", slug, r"the mean \((\d+(?:\.\d+)?)\) and the median \((\d+(?:\.\d+)?)\)",
                  "the tip's mean and median")
        if m6:
            check("AV", "ARITH", n(m6.group(1)) == F(sum(data), len(data)) and n(m6.group(2)) == median_of(data),
                  "tip repeats mean %s and median %s" % m6.groups())
        m7 = find("AV", slug, r"If we changed the (\d+) to (\d+),.*?The mean would jump to (\d+(?:\.\d+)?), "
                  r"but the median would stay at (\d+)", "the outlier follow-up")
        if m7:
            old, new, jmean, jmed = int(m7.group(1)), int(m7.group(2)), n(m7.group(3)), n(m7.group(4))
            changed = [new if x == old else x for x in data]
            check("AV", "ARITH", old in data and F(sum(changed), len(changed)) == jmean,
                  "%s -> mean %s" % (changed, jmean))
            check("AV", "ARITH", median_of(changed) == jmed == median_of(data),
                  "median stays %s" % jmed)
        m8 = find("AV", slug, r"If the data is ([\d, ]+?), there are (\d+) values", "the mistakes list's count")
        if m8:
            d2 = [int(v) for v in m8.group(1).split(",")]
            check("AV", "COUNT", len(d2) == int(m8.group(2)), "%s: %d values, including repeats" % (d2, len(d2)))

    # The median rule, in the approved wording, and its two examples.
    m = find("AV-M", slug, r"The median's position is \(n \+ 1\) ÷ 2, where n is how many values there are\. "
             r"For (\d+) values that's the (\d+)(?:st|nd|rd|th)\. For ([\d, ]+?) it's "
             r"\((\d+) \+ 1\) ÷ 2 = (\d+(?:\.\d+)?), so halfway between (\d+) and (\d+), which is (\d+(?:\.\d+)?)\.",
             "the approved (n + 1) ÷ 2 rule")
    if m:
        k1, p1 = int(m.group(1)), int(m.group(2))
        check("AV-M", "ARITH", F(k1 + 1, 2) == p1, "(%d + 1) ÷ 2 = %d" % (k1, p1))
        vals = [int(v) for v in m.group(3).split(",")]
        k2, p2 = int(m.group(4)), n(m.group(5))
        a, b, med = int(m.group(6)), int(m.group(7)), n(m.group(8))
        s = sorted(vals)
        check("AV-M", "ARITH", k2 == len(vals), "%s has %d values, the n used" % (vals, k2))
        check("AV-M", "ARITH", F(k2 + 1, 2) == p2, "(%d + 1) ÷ 2 = %s" % (k2, p2))
        lo = int(p2)   # a .5 position sits between the values in positions floor and ceil
        check("AV-M", "ARITH", p2.denominator == 2 and (s[lo - 1], s[lo]) == (a, b),
              "position %s lies between sorted positions %d and %d, which hold %d and %d"
              % (p2, lo, lo + 1, a, b))
        check("AV-M", "ARITH", F(a + b, 2) == med == median_of(vals), "halfway between %d and %d is %s" % (a, b, med))
        # the bonus example on the same page must agree
        mb = find("AV-M", slug, r"Data: ([\d, ]+?)\. Find the median\..*?Median = \((\d+) \+ (\d+)\)/\(2\) = "
                  r"\((\d+)\)/\(2\) = (\d+(?:\.\d+)?)", "the bonus even-count example")
        if mb:
            bvals = [int(v) for v in mb.group(1).split(",")]
            x, y, tot, bmed = int(mb.group(2)), int(mb.group(3)), int(mb.group(4)), n(mb.group(5))
            check("AV-M", "ARITH", bvals == vals and x + y == tot and F(tot, 2) == bmed == med,
                  "bonus: (%d + %d) ÷ 2 = %s, the same median the rule gives" % (x, y, bmed))

    # The median wording agrees with Distinctly Average's own scaffold card.
    game = read("games/distinctly-average/index.html")
    card = re.search(r"function renderScaffoldCard.*?\n\}", game, re.S)
    card_txt = re.sub(r"<[^>]+>", "", card.group(0)) if card else ""
    for phrase in ("(n + 1) ÷ 2", "halfway between"):
        check("AV-M", "MATCH", phrase in card_txt and phrase in text(slug),
              "guide and game scaffold card both say %r" % phrase, "page + game")

    m = find("AV-MODE", slug, r"The mode is the value that appears most often\. If two values tie for most often, "
             r"there are two modes\. If no value repeats, there is no mode\.", "the approved mode wording")
    check("AV-MODE", "TEXT", bool(m), "approved mode wording present")
    says("AV-MODE", slug, absent=["appear the same number of times"])
    says("AV-2", slug, present=["central reservation"], absent=["median strip"])
    says("AV-EXAM", slug, present=["often ask which average suits the data best, and why"],
         absent=["increasingly"])

    # The practice link: Distinctly Average at an explicit KS3 level, and it practises what the guide says.
    h = raw(slug)
    links = re.findall(r'href="\.\./\.\./games/([a-z0-9-]+)/(\?[^"]*)?"', h)
    check("AV-3", "LINK", links == [("distinctly-average", "?level=ks3")],
          "the only game link is distinctly-average/?level=ks3: %s" % links)
    check("AV-3", "LINK", "stat-attack" not in h, "no link to Stat Attack")
    roster = read(".claude/rules/game-roster.md")
    row = re.search(r"^\|[^|]*\|[^|]*\| `distinctly-average` \| ([^|]+) \|", roster, re.M)
    check("AV-3", "LINK", bool(row) and "KS3" in [s.strip() for s in row.group(1).split(",")],
          "roster declares distinctly-average levels: %s" % (row.group(1).strip() if row else None), "page + roster")
    impl = re.search(r"IMPLEMENTED_LEVELS\s*=\s*\[([^\]]*)\]", game)
    check("AV-3", "LINK", bool(impl) and "'ks3'" in impl.group(1),
          "the game implements ks3: %s" % (impl.group(1) if impl else None), "page + game")
    m = find("AV-3", slug, r"Our Distinctly Average game gives your child hands-on practice with ([a-z, ]+?)\. ",
             "the practice claim")
    if m:
        claimed = {w.strip() for w in re.split(r",\s*(?:and\s+)?|\s+and\s+", m.group(1)) if w.strip()}
        cats = set(re.findall(r"cat: '(\w+)', level: 'ks3'", game))
        practised = {"mode" if c.startswith("mode") else c for c in cats}
        check("AV-3", "MATCH", claimed == practised,
              "guide claims %s; the game's KS3 items practise %s" % (sorted(claimed), sorted(practised)), "page + game")


# --------------------------------------------------------------------------- #
# Fractions
# --------------------------------------------------------------------------- #
def fractions():
    slug = "fractions"
    m = find("FR-1", slug, r"Thinking (\d*\.\d+) is bigger than (\d*\.\d+) because (\d+) is bigger than (\d+)\. "
             r"Compare in hundredths: (\d*\.\d+) against (\d*\.\d+), and (\d+) beats (\d+)\.",
             "the 0.25 / 0.3 misconception")
    if m:
        x, y = n(m.group(1)), n(m.group(2))
        dx, dy = m.group(3), m.group(4)
        hy, hx = m.group(5), m.group(6)
        cy, cx = int(m.group(7)), int(m.group(8))
        check("FR-1", "ARITH", x < y, "%s < %s, so 'thinking %s is bigger' is the misconception" % (x, y, x))
        check("FR-1", "ARITH", int(dx) > int(dy) and m.group(1).split(".")[1] == dx and m.group(2).split(".")[1] == dy,
              "the faulty reason compares the digits after the point: %s > %s" % (dx, dy))
        check("FR-1", "ARITH", n(hy) == y and n(hx) == x and len(hy.split(".")[1]) == len(hx.split(".")[1]) == 2,
              "%s and %s are %s and %s written in hundredths" % (hy, hx, y, x))
        check("FR-1", "ARITH", cy == n(hy) * 100 and cx == n(hx) * 100 and cy > cx,
              "%d hundredths beats %d hundredths" % (cy, cx))
    says("FR-1", slug, absent=["0.125", "because 3 is bigger than 25"])

    m = find("FR-2", slug, r"Dividing by the percentage number \((\d+) ÷ (\d+) = (\d+)\) doesn't find (\d+)%\. "
             r"It only happens to work for (\d+)%\. To find (\d+)%, find (\d+)% \((\d+)\) and double it: (\d+)\.",
             "the divide-by-the-percentage bullet")
    if m:
        a, p, q, p2, k, p3, k2, t, ans = (int(g) for g in m.groups())
        check("FR-2", "ARITH", F(a, p) == q, "%d ÷ %d = %d" % (a, p, q))
        check("FR-2", "ARITH", p == p2 == p3 and pct(p, a) != q, "%d%% of %d is %s, not %d" % (p, a, pct(p, a), q))
        works = [r for r in range(1, 101) if F(a, r) == pct(r, a)]
        check("FR-2", "ARITH", works == [k],
              "percentages r in 1..100 where %d ÷ r = r%% of %d: %s (the page says only %d%%)" % (a, a, works, k))
        check("FR-2", "ARITH", k2 == k and pct(k, a) == t, "%d%% of %d = %d" % (k, a, t))
        check("FR-2", "ARITH", p == 2 * k and 2 * t == ans == pct(p, a), "double %d: %d = %d%% of %d" % (t, ans, p, a))
    says("FR-2", slug, absent=["only works for finding 1%", "only works for finding 10%"])

    # Worked example and "try another" (unchanged, still checked from the page)
    m = find("FR-EX", slug, r"What is (\d+)% of £(\d+)\?", "the worked percentage")
    if m:
        p, a = int(m.group(1)), int(m.group(2))
        m2 = find("FR-EX", slug, r"Answer: (\d+)% of £(\d+) is £(\d+)\.", "the worked answer")
        if m2:
            check("FR-EX", "ARITH", (int(m2.group(1)), int(m2.group(2))) == (p, a) and pct(p, a) == n(m2.group(3)),
                  "%d%% of £%d = £%s" % (p, a, m2.group(3)))
    m = find("FR-EX", slug, r"what is (\d+)% of £(\d+)\? \(Answer: 10% = £(\d+), 5% = £(\d+), so \1% = £(\d+)\.\)",
             "try another")
    if m:
        p, a, ten, five, tot = (int(g) for g in m.groups())
        check("FR-EX", "ARITH", pct(10, a) == ten and pct(5, a) == five and ten + five == tot == pct(p, a),
              "%d%% of £%d: £%d + £%d = £%d" % (p, a, ten, five, tot))


# --------------------------------------------------------------------------- #
# Probability trees
# --------------------------------------------------------------------------- #
def probability_trees():
    slug = "probability-trees"
    m = find("PT", slug, r"Given: the probability of rain on any day is (\d*\.\d+), assuming the two days are "
             r"independent \(the question will tell you to\)\.", "the independence assumption")
    if not m:
        return
    p = n(m.group(1))
    m = find("PT", slug, r"P\(rain both days\) = (\d*\.\d+) × (\d*\.\d+) = (\d*\.\d+)", "Q1")
    if m:
        a, b, both = (n(g) for g in m.groups())
        check("PT", "ARITH", a == b == p and a * b == both, "P(both) = %s × %s = %s" % (a, b, both))
    m = find("PT", slug, r"P\(no rain either day\) = (\d*\.\d+) × (\d*\.\d+) = (\d*\.\d+)", "Q2 complement")
    if m:
        a, b, none = (n(g) for g in m.groups())
        check("PT", "ARITH", a == b == 1 - p and a * b == none, "P(neither) = %s × %s = %s" % (a, b, none))
    m = find("PT", slug, r"P\(rain at least once\) = 1 - (\d*\.\d+) = (\d*\.\d+)", "Q2 answer")
    if m:
        none, once = n(m.group(1)), n(m.group(2))
        check("PT", "ARITH", none == (1 - p) ** 2 and 1 - none == once, "P(at least once) = 1 - %s = %s" % (none, once))
        c = find("PT-1", slug, r"Check: the chance of rain at least once must be more than (\d*\.\d+) \(one day alone "
                 r"gives that\) and less than (\d*\.\d+) \(adding double-counts the both-days case\)\. "
                 r"(\d*\.\d+) fits\.", "the approved sense-check")
        if c:
            lo, hi, fit = (n(g) for g in c.groups())
            check("PT-1", "ARITH", lo == p, "lower bound %s is one day's chance" % lo)
            check("PT-1", "ARITH", hi == p + p, "upper bound %s is the two days added" % hi)
            check("PT-1", "ARITH", fit == once and lo < fit < hi, "%s < %s < %s" % (lo, fit, hi))
            check("PT-1", "ARITH", hi - fit == p * p,
                  "adding over-counts by exactly the both-days case: %s - %s = %s = P(both)" % (hi, fit, p * p))
    m = find("PT", slug, r"the probability of rain on both days is (\d*\.\d+) × (\d*\.\d+) = (\d*\.\d+), not "
             r"(\d*\.\d+) \+ (\d*\.\d+) = (\d*\.\d+)", "the adding-not-multiplying mistake")
    if m:
        a, b, prod, c, d, s = (n(g) for g in m.groups())
        check("PT", "ARITH", a * b == prod and c + d == s and prod != s, "%s × %s = %s; %s + %s = %s" % (a, b, prod, c, d, s))
    m = find("PT", slug, r"if P\(rain\) = (\d*\.\d+), then P\(no rain\) must be (\d*\.\d+)", "branches sum to 1")
    if m:
        check("PT", "ARITH", n(m.group(1)) + n(m.group(2)) == 1, "%s + %s = 1" % m.groups())
    says("PT-2", slug, present=["With sweets taken out of a bag and not replaced, the second-branch probabilities change."],
         absent=["0.51 is just over a half", "30% chance each day, so over two days"])


# --------------------------------------------------------------------------- #
# Statistics & data
# --------------------------------------------------------------------------- #
def statistics():
    slug = "statistics-data"
    vals = {}
    for key, pat in (("min", r"Minimum = (\d+)"), ("q1", r"Lower quartile \(Q1\) = (\d+)"),
                     ("med", r"Median = (\d+)"), ("q3", r"Upper quartile \(Q3\) = (\d+)"),
                     ("max", r"Maximum = (\d+)")):
        m = find("ST", slug, pat, "box plot " + key)
        if m:
            vals[key] = int(m.group(1))
    if len(vals) == 5:
        check("ST", "ARITH", vals["min"] <= vals["q1"] <= vals["med"] <= vals["q3"] <= vals["max"],
              "five-number summary in order: %s" % vals)
        m = find("ST", slug, r"IQR = Q_3 - Q_1 = (\d+) - (\d+) = (\d+)", "the IQR")
        if m:
            a, b, c = (int(g) for g in m.groups())
            check("ST", "ARITH", (a, b) == (vals["q3"], vals["q1"]) and a - b == c, "IQR = %d - %d = %d" % (a, b, c))
        m = find("ST-1", slug, r"What fraction of the data lies between (\d+) and (\d+)\? Answer: about half "
                 r"\(roughly 50%\), by definition of quartiles\.", "the 'about half' answer")
        if m:
            check("ST-1", "ARITH", (int(m.group(1)), int(m.group(2))) == (vals["q1"], vals["q3"]),
                  "the question's interval is Q1 to Q3")
    says("ST-1", slug, absent=["exactly half (50%)", "will not be exactly a half"])
    says("ST-2", slug, present=['as hours revised increase, marks tend to increase'],
         absent=["there is a positive correlation between hours of revision and marks scored"])


# --------------------------------------------------------------------------- #
# The other corrected guides (PR #9's findings), now read from the pages
# --------------------------------------------------------------------------- #
def negative_numbers():
    slug = "negative-numbers"
    says("NN-1", slug, present=["Adding a positive number means moving right. Subtracting a positive number means moving left."],
         absent=["Adding always means moving right."])
    m = find("NN-1", slug, r"Adding a negative is the same as subtracting: (-?\d+) \+ \((-\d+)\) = (-?\d+) - (\d+) = (-?\d+)",
             "adding a negative")
    if m:
        a, b, c, d, r = (int(g) for g in m.groups())
        check("NN-1", "ARITH", a + b == c - d == r and a == c and -b == d and r < a,
              "%d + (%d) = %d: adding moved LEFT, which is why the rule names positive numbers" % (a, b, r))
    m = find("NN-1", slug, r"Subtracting a negative is the same as adding: (-?\d+) - \((-\d+)\) = (-?\d+) \+ (\d+) = (-?\d+)",
             "subtracting a negative")
    if m:
        a, b, c, d, r = (int(g) for g in m.groups())
        check("NN-1", "ARITH", a - b == c + d == r and r > a, "%d - (%d) = %d: subtracting moved RIGHT" % (a, b, r))
    m = find("NN-1", slug, r"work through (-?\d+) \+ (\d+):.*?Count the jumps: ((?:-?\d+ → )+-?\d+)\. You land on (-?\d+)\. "
             r"So (-?\d+) \+ (\d+) = (-?\d+)\.", "the number-line walk")
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        walk = [int(v) for v in m.group(3).split("→")]
        check("NN-1", "ARITH", walk[0] == a and len(walk) - 1 == b and all(y - x == 1 for x, y in zip(walk, walk[1:])),
              "walk %s: %d steps right from %d" % (walk, b, a))
        check("NN-1", "ARITH", walk[-1] == int(m.group(4)) == int(m.group(7)) == a + b, "%d + %d = %d" % (a, b, a + b))
    for m in re.finditer(r"\((-\d+)\) × \((-\d+)\) = (\d+)", text(slug)):
        a, b, r = (int(g) for g in m.groups())
        check("NN-2", "ARITH", a * b == r > 0, "(%d) × (%d) = %d" % (a, b, r))
    if not re.search(r"\((-\d+)\) × \((-\d+)\) = (\d+)", text(slug)):
        check("NN-2", "FOUND", False, "negative-numbers: no negative-times-negative example found")
    says("NN-2", slug, present=["when two negative numbers are multiplied or divided", "when multiplying or dividing two negatives"],
         absent=["This rule only applies when the signs are directly next to each other"])
    m = find("NN-2", slug, r"like (\d+) - \((-\d+)\) = (\d+)", "5 - (-2)")
    if m:
        a, b, r = (int(g) for g in m.groups())
        check("NN-2", "ARITH", a - b == r, "%d - (%d) = %d" % (a, b, r))
    m = find("NN-2", slug, r"It does not mean (-\d+) \+ \((-\d+)\) = (\d+)\. That's (-\d+) - (\d+) = (-\d+)\.", "not 7")
    if m:
        a, b, wrong, c, d, r = (int(g) for g in m.groups())
        check("NN-2", "ARITH", a + b != wrong and a + b == c - d == r, "%d + (%d) = %d, not %d" % (a, b, r, wrong))


def area_perimeter():
    slug = "area-perimeter"
    says("AP-1", slug, present=["a triangle is exactly half of the rectangle with the same base and the same perpendicular height"],
         absent=["if you imagine doubling the triangle to make a rectangle"])
    m = find("AP-1", slug, r"a triangle with a base of (\d+) cm and a perpendicular height of (\d+) cm", "the bonus triangle")
    if m:
        b, h = int(m.group(1)), int(m.group(2))
        m2 = find("AP-1", slug, r"Area = \(1\)/\(2\) × (\d+) × (\d+) = \(1\)/\(2\) × (\d+) = (\d+) cm\^2", "the bonus area")
        if m2:
            b2, h2, prod, area = (int(g) for g in m2.groups())
            check("AP-1", "ARITH", (b2, h2) == (b, h) and b * h == prod and F(prod, 2) == area,
                  "½ × %d × %d = %d cm²" % (b, h, area))
        # For every apex position over the base, the triangle is half the b x h rectangle, and
        # doubling it gives a rectangle only when the apex sits over an end of the base.
        halves, rects = [], []
        for ax in range(0, b + 1):
            v1, v2 = (b, 0), (ax, h)
            halves.append(F(abs(v1[0] * v2[1] - v1[1] * v2[0]), 2) == F(b * h, 2))
            right = any(u[0] * w[0] + u[1] * w[1] == 0 for u, w in
                        (((b, 0), (ax, h)), ((-b, 0), (ax - b, h)), ((-ax, -h), (b - ax, -h))))
            rects.append(right)
        check("AP-1", "ARITH", all(halves), "base %d, height %d: every apex position gives area ½ × %d × %d" % (b, h, b, h))
        check("AP-1", "ARITH", rects.count(True) == 2 and rects[0] and rects[-1],
              "only the two right-angled cases double to a rectangle; the rest make a parallelogram")
    m = find("AP-2", slug, r"A rectangle is (\d+) cm long and (\d+) cm wide", "the worked rectangle")
    if m:
        l, w = int(m.group(1)), int(m.group(2))
        m2 = find("AP-2", slug, r"Perimeter = 2 × \((\d+) \+ (\d+)\) = 2 × (\d+) = (\d+) cm", "the worked perimeter")
        if m2:
            a, b, s, per = (int(g) for g in m2.groups())
            check("AP-2", "ARITH", (a, b) == (l, w) and a + b == s and 2 * s == per == l + w + l + w,
                  "2 × (%d + %d) = %d = the four sides added up" % (l, w, per))
        m3 = find("AP-2", slug, r"Area = length × width = (\d+) × (\d+) = (\d+) cm\^2", "the worked area")
        if m3:
            a, b, ar = (int(g) for g in m3.groups())
            check("AP-2", "ARITH", (a, b) == (l, w) and a * b == ar, "%d × %d = %d cm²" % (a, b, ar))
            m4 = find("AP-2", slug, r"(\d+) cm by (\d+) cm instead.*?the area stays at (\d+) cm², but the perimeter "
                      r"changes to (\d+) cm", "the same-area follow-up")
            if m4:
                l2, w2, ar2, per2 = (int(g) for g in m4.groups())
                check("AP-2", "ARITH", l2 * w2 == ar2 == ar and 2 * (l2 + w2) == per2 != 2 * (l + w),
                      "%d × %d = %d, perimeter %d" % (l2, w2, ar2, per2))
    says("AP-2", slug, present=["they're adding up the side lengths"])


def probability():
    slug = "probability"
    says("PR-1", slug, present=["as long as every outcome is equally likely",
                                "provided each of those outcomes is equally likely."])
    m = find("PR-1", slug, r"≈ 1 in (\d+) million", "the lottery odds")
    if m:
        # UK Lotto: 6 numbers from 59. The page's rounded figure against the real count.
        check("PR-1", "ARITH", round(math.comb(59, 6) / 1e6) == int(m.group(1)),
              "C(59, 6) = %s, 'about 1 in %s million'" % (f"{math.comb(59, 6):,}", m.group(1)),
              "page + UK Lotto's 6-from-59 rule, which the page does not print")
    m = find("PR-EX", slug, r"A bag contains (\d+) red balls and (\d+) blue balls", "the bag")
    if m:
        r, b = int(m.group(1)), int(m.group(2))
        m2 = find("PR-EX", slug, r"P\(red\) = \((\d+)\)/\((\d+)\) = (\d*\.\d+) = (\d+)%", "P(red)")
        if m2:
            a, t, d, pc = m2.groups()
            check("PR-EX", "ARITH", F(int(a), int(t)) == F(r, r + b) == n(d) == F(int(pc), 100),
                  "P(red) = %d/%d = %s = %s%%" % (r, r + b, d, pc))
        m3 = find("PR-EX", slug, r"blue ball\?\" \(Answer: \((\d+)\)/\((\d+)\) = (\d*\.\d+) = (\d+)%\.\)", "P(blue)")
        if m3:
            a, t, d, pc = m3.groups()
            check("PR-EX", "ARITH", F(int(a), int(t)) == F(b, r + b) == n(d) == F(int(pc), 100),
                  "P(blue) = %d/%d" % (b, r + b))
    m = find("PR-EX", slug, r"A spinner has (\d+) equal sections numbered 1 to (\d+)\..*?Prime numbers between 1 and (\d+): "
             r"([\d, ]+) — that's (\d+) primes\.", "the spinner")
    if m:
        k = int(m.group(1))
        listed = [int(v) for v in m.group(4).split(",")]
        primes = [v for v in range(2, k + 1) if all(v % d for d in range(2, int(v ** 0.5) + 1))]
        check("PR-EX", "ARITH", listed == primes and len(primes) == int(m.group(5)), "primes 1..%d: %s" % (k, primes))
        m2 = find("PR-EX", slug, r"P\(prime\) = \((\d+)\)/\((\d+)\) = \((\d+)\)/\((\d+)\) = (\d*\.\d+) = (\d+)%", "P(prime)")
        if m2:
            a, t, c, d, dec, pc = m2.groups()
            check("PR-EX", "ARITH", F(int(a), int(t)) == F(len(primes), k) == F(int(c), int(d)) == n(dec) == F(int(pc), 100),
                  "P(prime) = %d/%d" % (len(primes), k))


def coordinates():
    slug = "coordinates"
    m = find("CO-2", slug, r"Plot \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), \((-?\d+), (-?\d+)\), and \((-?\d+), (-?\d+)\)\. "
             r"What shape have you made\?\" \(A square, with sides of (\d+) units", "the plotted square")
    if m:
        g = [int(v) for v in m.groups()]
        pts = [(g[0], g[1]), (g[2], g[3]), (g[4], g[5]), (g[6], g[7])]
        side = g[8]
        sides = [math.dist(pts[i], pts[(i + 1) % 4]) for i in range(4)]
        vec = [(pts[(i + 1) % 4][0] - pts[i][0], pts[(i + 1) % 4][1] - pts[i][1]) for i in range(4)]
        right = all(vec[i][0] * vec[(i + 1) % 4][0] + vec[i][1] * vec[(i + 1) % 4][1] == 0 for i in range(4))
        check("CO-2", "ARITH", all(s == side for s in sides) and right,
              "%s: four sides of %d and four right angles -- a square, and so a rectangle" % (pts, side))
    says("CO-2", slug, absent=["(A rectangle.)"])


def expanding():
    slug = "expanding-factorising"
    says("EF-1", slug, present=["genuinely the entire method whenever there is nothing in front of the x^2"],
         absent=["That is genuinely the entire method. "])
    m = find("EF-EX", slug, r"Factorise (x\^2 \+ \d+x \+ \d+)\. .*?multiply to give (\d+) and add to give (\d+)\..*?"
             r"(\d+) \+ (\d+) = \3\. That is the pair we need\. Write the answer: (\(x\+\d+\)\(x\+\d+\))\.", "the worked factorising")
    if m:
        quad, prod, s, a, b, fact = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), m.group(6)
        check("EF-EX", "ARITH", a * b == prod and a + b == s, "%d × %d = %d and %d + %d = %d" % (a, b, prod, a, b, s))
        check("EF-EX", "ARITH", same_poly(quad, fact), "%s = %s, checked at x = -6..6" % (quad, fact))
    for m in re.finditer(r"(x\^2 [+-] \d*x [+-] \d+) factorises to (\([^)]*\)\([^)]*\)), not (\([^)]*\)\([^)]*\))", text(slug)):
        check("EF-EX", "ARITH", same_poly(m.group(1), m.group(2)) and not same_poly(m.group(1), m.group(3)),
              "%s = %s, not %s" % m.groups())
    m = find("EF-EX", slug, r"\(x\+(\d+)\)\^2 = (x\^2 \+ \d+x \+ \d+)", "the squared bracket")
    if m:
        check("EF-EX", "ARITH", same_poly("(x+%s)(x+%s)" % (m.group(1), m.group(1)), m.group(2)),
              "(x+%s)^2 = %s" % m.groups())


def indices():
    slug = "indices-surds"
    says("IS-1", slug, present=["that cover most of what they will meet"], absent=["that cover every situation"])
    says("IS-2", slug, present=["anything except zero, to the power 0, is 1 — x^0 = 1 for x ≠ 0"])
    m = find("IS-EX", slug, r"√\((\d+)\) = √\((\d+) × (\d+)\) = √\((\d+)\) × √\((\d+)\) = (\d+)√\((\d+)\)", "√50")
    if m:
        a, sq, r, sq2, r2, k, r3 = (int(g) for g in m.groups())
        biggest = max(s * s for s in range(1, a + 1) if a % (s * s) == 0)
        check("IS-EX", "ARITH", sq * r == a and sq == sq2 == biggest and r == r2 == r3 and k * k == sq,
              "√%d = √(%d × %d) = %d√%d; %d is the largest square factor" % (a, sq, r, k, r, biggest))
    m = find("IS-EX", slug, r"but (\d+) = (\d+) × (\d+), so √\((\d+)\) = (\d+)√\((\d+)\)", "√8")
    if m:
        a, sq, r, a2, k, r2 = (int(g) for g in m.groups())
        check("IS-EX", "ARITH", sq * r == a == a2 and k * k == sq and r == r2, "√%d = %d√%d" % (a, k, r))
    m = find("IS-EX", slug, r"what is (\d+)\^(\d+) × \1\^(\d+)\? Add the powers: \1\^\(\2\+\3\) = \1\^(\d+) = (\d+)", "3^2 × 3^4")
    if m:
        b, p, q, s, v = (int(g) for g in m.groups())
        check("IS-EX", "ARITH", p + q == s and b ** p * b ** q == b ** s == v, "%d^%d × %d^%d = %d^%d = %d" % (b, p, b, q, b, s, v))
    m = find("IS-EX", slug, r"(\d+)\^\(-(\d+)\) does not equal (-\d+)\. It equals \(1\)/\(\1\^\2\) = \(1\)/\((\d+)\)", "2^-3")
    if m:
        b, e, wrong, den = (int(g) for g in m.groups())
        check("IS-EX", "ARITH", F(b) ** -e == F(1, den) != wrong, "%d^-%d = 1/%d, not %d" % (b, e, den, wrong))
    m = find("IS-EX", slug, r"x\^(\d+) × x\^(\d+) = x\^\((\d+)\) is wrong\. The correct answer is x\^\(\1\+\2\) = x\^(\d+)", "x^3 × x^4")
    if m:
        p, q, wrong, right = (int(g) for g in m.groups())
        check("IS-EX", "ARITH", p + q == right and p * q == wrong != right, "x^%d × x^%d = x^%d, not x^%d" % (p, q, right, wrong))


def standard_form():
    slug = "standard-form"
    says("SF-1", slug, absent=["how many zeros"])
    m = find("SF-1", slug, r"10\^(\d+) means a million, 10\^\(-(\d+)\) means a ten-thousandth", "the powers of ten")
    if m:
        check("SF-1", "ARITH", 10 ** int(m.group(1)) == 1_000_000 and F(1, 10 ** int(m.group(2))) == F(1, 10_000),
              "10^%s = 1,000,000; 10^-%s = 1/10,000" % m.groups())
    rows = re.findall(r"([\d,]*\.?\d+) (\d+(?:\.\d+)?) × 10\^\(?(-?\d+)\)? ([+-]\d+)", text(slug))
    check("SF", "FOUND", len(rows) >= 4, "the examples table: %d rows found" % len(rows))
    for ordinary, mant, exp, col in rows:
        check("SF", "ARITH", n(ordinary) == n(mant) * F(10) ** int(exp) and int(exp) == int(col) and 1 <= n(mant) < 10,
              "%s = %s × 10^%s" % (ordinary, mant, exp))
    for m in re.finditer(r"([\d,]{5,}|0\.\d+) = (\d+(?:\.\d+)?) × 10\^\(?(-?\d+)\)?", text(slug)):
        check("SF", "ARITH", n(m.group(1)) == n(m.group(2)) * F(10) ** int(m.group(3)), "%s = %s × 10^%s" % m.groups())
    m = find("SF", slug, r"Writing (\d+) × 10\^(\d+) instead of (\d+\.\d+) × 10\^(\d+) is NOT standard form, even though the "
             r"value is the same", "34 × 10^5")
    if m:
        a, e, b, f = int(m.group(1)), int(m.group(2)), n(m.group(3)), int(m.group(4))
        check("SF", "ARITH", a * F(10) ** e == b * F(10) ** f and not (1 <= a < 10) and 1 <= b < 10,
              "%d × 10^%d = %s × 10^%d; only the second is standard form" % (a, e, b, f))
    m = find("SF", slug, r"\((\d+) × 10\^(\d+)\) × \((\d+) × 10\^(\d+)\) = (\d+) × 10\^(\d+)", "the product")
    if m:
        a, e, b, f, c, g = (int(x) for x in m.groups())
        check("SF", "ARITH", a * b == c and e + f == g, "(%d × 10^%d)(%d × 10^%d) = %d × 10^%d" % (a, e, b, f, c, g))
    m = find("SF", slug, r"weighs about ([\d,]+) kg.*?Answer: (\d+\.\d+) × 10\^\(?(\d+)\)? kg", "the Earth's mass")
    if m:
        check("SF", "ARITH", n(m.group(1)) == n(m.group(2)) * F(10) ** int(m.group(3)), "%s = %s × 10^%s" % m.groups())
    says("SF-2", slug, present=["This usually loses marks."], absent=["This loses marks every time."])


def simultaneous():
    slug = "simultaneous-equations"
    says("SE-1", slug, present=["Checking catches slips"], absent=["almost always carries a mark for checking"])
    m = find("SE", slug, r"(\d+)x \+ y = (\d+) \.\.\.\(1\) x \+ y = (\d+) \.\.\.\(2\)", "the worked pair")
    if m:
        a, c1, c2 = (int(g) for g in m.groups())
        x = F(c1 - c2, a - 1)
        y = c2 - x
        m2 = find("SE", slug, r"(\d+)x = (\d+) x = (\d+)", "the elimination")
        if m2:
            k, r, xs = (int(g) for g in m2.groups())
            check("SE", "ARITH", k == a - 1 and r == c1 - c2 and xs == x, "(%dx + y) - (x + y): %dx = %d, x = %d" % (a, k, r, xs))
        m3 = find("SE", slug, r"(\d+) \+ y = (\d+), so y = (-?\d+)", "the substitution")
        if m3:
            check("SE", "ARITH", int(m3.group(1)) == x and int(m3.group(2)) == c2 and int(m3.group(3)) == y,
                  "x = %s, y = %s" % (x, y))
        m4 = find("SE", slug, r"Check in equation \(1\): (\d+)\((\d+)\) \+ (\d+) = (\d+) \+ (\d+) = (\d+)", "the check")
        if m4:
            p, q, r, s, t, u = (int(g) for g in m4.groups())
            check("SE", "ARITH", (p, q, r) == (a, x, y) and p * q == s and s + t == u == c1 and t == r,
                  "%d(%d) + %d = %d" % (p, q, r, u))
        m5 = find("SE", slug, r"There is exactly one pair of values \(x = (\d+), y = (\d+)\)", "the stated solution")
        if m5:
            check("SE", "ARITH", (int(m5.group(1)), int(m5.group(2))) == (x, y), "x = %s, y = %s" % m5.groups())
    m = find("SE", slug, r"two numbers add up to (\d+) and the difference between them is (\d+), what are they\?\" \((\d+) and (\d+)\.\)",
             "the conversation starter")
    if m:
        s, d, a, b = (int(g) for g in m.groups())
        check("SE", "ARITH", a + b == s and a - b == d, "%d + %d = %d, %d - %d = %d" % (a, b, s, a, b, d))


def trigonometry():
    slug = "trigonometry"
    says("TR-1", slug, present=["Battle-style trig practice — instant feedback."], absent=["fast rounds"])
    m = find("TR", slug, r"an angle of (\d+) degrees and a hypotenuse of (\d+) cm", "the worked triangle")
    if m:
        ang, hyp = int(m.group(1)), int(m.group(2))
        m2 = find("TR", slug, r"Opp = (\d+) × (\d*\.\d+) = (\d+) cm", "the worked answer")
        if m2:
            h, s, opp = int(m2.group(1)), n(m2.group(2)), int(m2.group(3))
            check("TR", "ARITH", h == hyp and abs(math.sin(math.radians(ang)) - float(s)) < 1e-12 and h * s == opp,
                  "%d × sin %d° = %d × %s = %d cm" % (hyp, ang, hyp, s, opp))
    m = find("TR", slug, r"standing (\d+) metres from a building and you look up at (\d+) degrees.*?so the building is (\d+) metres tall",
             "the building")
    if m:
        d, ang, ht = (int(g) for g in m.groups())
        check("TR", "ARITH", abs(d * math.tan(math.radians(ang)) - ht) < 1e-9, "%d × tan %d° = %d m" % (d, ang, ht))


def graphs():
    slug = "graphs-transformations"
    t = text(slug)
    check("GT-1", "TEXT", not re.search(r"(?i)stretch|squash", t) and not re.search(r"(?i)stretch|squash", raw(slug)),
          "graphs-transformations: no 'stretch' or 'squash' anywhere on the page, head included")
    m = find("GT", slug, r"If y = x\^2, what does y = \(x - (\d+)\)\^2 look like\?.*?shifted (\d+) units to the right\. "
             r"The vertex moves from \(0, 0\) to \((\d+), 0\)", "the worked translation")
    if m:
        a, s, vx = (int(g) for g in m.groups())
        f = poly("(x-%d)^2" % a)
        check("GT", "ARITH", a == s == vx and f(vx) == 0 and all(f(x) > 0 for x in range(-10, 11) if x != vx),
              "(x - %d)^2 has its only zero, the vertex, at x = %d" % (a, vx))
    m = find("GT", slug, r"What about y = x\^2 \+ (\d+)\?.*?Vertex goes from \(0, 0\) to \(0, (\d+)\)", "the follow-up")
    if m:
        check("GT", "ARITH", m.group(1) == m.group(2), "x^2 + %s has its minimum %s at x = 0" % m.groups())


def circle_theorems():
    slug = "circle-theorems"
    says("CT-1", slug, present=["At Higher tier, your child may be asked to prove theorems as well as apply them."],
         absent=["does not need to prove"])
    m = find("CT", slug, r"If the angle at the centre is (\d+) degrees, the angle at the circumference is (\d+) degrees "
             r"\(half\), not (\d+) degrees \(double\)", "the misconception")
    if m:
        c, h, d = (int(g) for g in m.groups())
        check("CT", "ARITH", F(c, 2) == h and 2 * c == d, "%d ÷ 2 = %d; %d × 2 = %d" % (c, h, c, d))
    m = find("CT", slug, r"So the angle at the circumference is (\d+) ÷ 2 = (\d+)°", "the worked answer")
    if m:
        check("CT", "ARITH", F(int(m.group(1)), 2) == int(m.group(2)), "%s ÷ 2 = %s" % m.groups())


# --------------------------------------------------------------------------- #
# Mark-scheme and examiner claims: softened in one pass (contract step 2)
# --------------------------------------------------------------------------- #
MARK_CLAIM = re.compile(r"(?i)\b(?:lose marks|loses marks|loses them|marks are(?: \w+)? lost|examiners(?: \w+)? want|"
                        r"cost marks|required for full marks|carries a mark|only half the marks|the exam will(?: \w+)? say)")
SOFTENER = re.compile(r"(?i)\b(?:usually|often)\b")


def examiner_claims():
    for slug in guide_slugs():
        body = text(slug)
        head = " ".join(re.findall(r'<meta (?:name|property)="(?:description|og:description)" content="([^"]*)"', raw(slug)))
        both = body + " " + html.unescape(head)
        # A claim counts as softened when "usually" or "often" governs it: inside the
        # match ("marks are often lost") or among the few words before it
        # ("is usually what examiners want").
        hits = [m.group(0) for m in MARK_CLAIM.finditer(both)
                if not SOFTENER.search(m.group(0)) and not SOFTENER.search(both[max(0, m.start() - 25):m.start()])]
        check("EXAM", "TEXT", not hits, "%s: no unqualified mark-scheme or examiner claim%s"
              % (slug, "" if not hits else " -- FOUND %s" % hits))


# --------------------------------------------------------------------------- #
# Tier badges: one component, four guides, sections read from the DfE data
# --------------------------------------------------------------------------- #
def tiers():
    js = read("parents/guide.js")
    m = re.search(r"/\* TIERS-JSON-BEGIN \*/(.*?)/\* TIERS-JSON-END \*/", js, re.S)
    check("TIER", "FOUND", bool(m), "parents/guide.js carries the TIERS table between its markers", "guide.js")
    if not m:
        return
    table = json.loads(m.group(1))
    dfe = json.loads(read("data/dfe-gcse-parts.json"))
    parts = {p["ref"]: (s, p) for s in dfe["statements"] for p in s["parts"]}
    for slug, t in sorted(table.items()):
        for ref in t["dfe"]:
            ok = ref in parts and parts[ref][1]["tier"] == "bold"
            check("TIER", "DFE", ok, "%s: DfE %s is bold (Higher only): %r"
                  % (slug, ref, parts[ref][1]["text"].strip()[:60] if ref in parts else None), "guide.js + DfE data")
        if t["kind"] == "higher":
            stmts = {parts[r][0]["ref"] for r in t["dfe"] if r in parts}
            whole = all(p["tier"] == "bold" for s in dfe["statements"] if s["ref"] in stmts for p in s["parts"])
            check("TIER", "DFE", whole and not t.get("sections"),
                  "%s: every part of %s is bold, so the whole guide is Higher" % (slug, sorted(stmts)), "guide.js + DfE data")
        else:
            check("TIER", "DFE", bool(t.get("sections")), "%s: partly Higher, names its sections %s" % (slug, t.get("sections")),
                  "guide.js")

    badge = re.compile(r'data-tier-badge="([a-z-]+)"')
    hub = read("parents/index.html")
    for slug in guide_slugs():
        h = raw(slug)
        on_page = badge.findall(h)
        want = [slug] if slug in table else []
        check("TIER", "BADGE", on_page == want, "%s: guide carries badge %s" % (slug, on_page or "none"))
        if slug in table:
            check("TIER", "BADGE", re.search(r"</h1>\s*<p class=\"tier-badge\" data-tier-badge=\"%s\"></p>" % slug, h) is not None,
                  "%s: the badge sits directly under the title" % slug)
        card = re.search(r'<a href="%s/" class="topic-card">(.*?)</a>' % re.escape(slug), hub, re.S)
        check("TIER", "BADGE", bool(card) and badge.findall(card.group(1)) == want,
              "%s: hub card carries badge %s" % (slug, badge.findall(card.group(1)) if card else "(no card)"))
        marks = re.findall(r'<span class="higher-mark" data-higher-section="([^"]+)">Higher</span>', h)
        loose = len(re.findall(r'class="higher-mark"', h)) - len(marks)
        sections = table.get(slug, {}).get("sections") or []
        check("TIER", "MARK", loose == 0 and set(marks) == set(sections) and (bool(marks) == bool(sections)),
              "%s: body 'Higher' markers %s against the badge's sections %s"
              % (slug, sorted(set(marks)) or "none", sections or "none"), "page + guide.js")


# --------------------------------------------------------------------------- #
# The section as a whole: hub, sitemap, template
# --------------------------------------------------------------------------- #
def guide_slugs():
    return sorted(d for d in os.listdir(PARENTS)
                  if os.path.isfile(os.path.join(PARENTS, d, "index.html")))


def section():
    slugs = set(guide_slugs())
    hub = read("parents/index.html")
    cards = set(re.findall(r'<a href="([a-z-]+)/" class="topic-card">', hub))
    sitemap = read("sitemap.xml")
    mapped = set(re.findall(r"<loc>https://maffsgames\.co\.uk/parents/([a-z-]+)/</loc>", sitemap))
    audit = read("docs/audit-parent-guides.md")
    m = re.search(r"\| Guides \| \*\*(\d+)\*\*: KS3 (\d+), GCSE (\d+)", audit)
    total, ks3, gcse = (int(g) for g in m.groups()) if m else (None, None, None)
    levels = {s: re.search(r'<span class="badge">(KS3|GCSE)</span>', raw(s)) for s in slugs}
    count = {lv: sum(1 for s in slugs if levels[s] and levels[s].group(1) == lv) for lv in ("KS3", "GCSE")}
    check("HUB", "COUNT", len(slugs) == total and count == {"KS3": ks3, "GCSE": gcse},
          "%d guides published (KS3 %d, GCSE %d); the MathsWins set the audit counted is %s (KS3 %s, GCSE %s)"
          % (len(slugs), count["KS3"], count["GCSE"], total, ks3, gcse), "page + audit doc")
    check("HUB", "LINK", cards == slugs, "hub has a card for every guide and no other: %s"
          % (sorted(cards ^ slugs) or "match"))
    check("HUB", "LINK", mapped == slugs and "<loc>https://maffsgames.co.uk/parents/</loc>" in sitemap,
          "sitemap lists the hub and every guide: %s" % (sorted(mapped ^ slugs) or "match"), "page + sitemap")
    m = re.search(r'What do "Higher tier" and "Foundation tier" mean\?</div>\s*<div class="faq-a"><p>(.*?)</p>', hub, re.S)
    faq = html.unescape(m.group(1)) if m else ""
    check("HUB", "TEXT", bool(re.search(r"Foundation tier is graded 1 to 5", faq)) and
          bool(re.search(r"Higher tier is graded 4 to 9, and a grade 3 is allowed on the Higher tier", faq)) and
          len(re.findall(r"\.", faq)) == 3,
          "tier FAQ states Foundation 1-5, Higher 4-9 with an allowed grade 3, and nothing else: %r" % faq[:120])


def template():
    pages = ["parents/index.html"] + ["parents/%s/index.html" % s for s in guide_slugs()]
    for rel in pages:
        body = read(rel)
        check("TPL", "TEXT", "no data collected" not in body, "%s: no 'no data collected'" % rel)
        check("TPL", "TEXT", "G-992JLHLP2D" in body and "G-7GTLYCZMXN" not in body,
              "%s: MaffsGames GA4 property, not MathsWins'" % rel)
        check("TPL", "TEXT", 'rel="canonical" href="https://maffsgames.co.uk/parents/' in body,
              "%s: canonical points at maffsgames.co.uk/parents/" % rel)
        check("TPL", "TEXT", "mw-auth" not in body and "mw_cookies" not in body and "cookieConsent" not in body,
              "%s: no MathsWins auth script and no cookie banner" % rel)
        # The only legitimate /schools/ reference is the shared asset directory (audit T4).
        stray = [frag for frag in body.split("schools/")[1:] if not frag.startswith("assets/")]
        check("TPL", "TEXT", not stray, "%s: /schools/ appears only as the shared asset path" % rel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    for fn in (averages, fractions, probability_trees, statistics, negative_numbers, area_perimeter,
               probability, coordinates, expanding, indices, standard_form, simultaneous, trigonometry,
               graphs, circle_theorems, examiner_claims, tiers, section, template):
        fn()

    fails = [r for r in results if not r[2]]
    last = None
    for finding, kind, ok, detail, _src in results:
        if args.quiet and ok:
            continue
        if finding != last:
            print("\n%s" % finding)
            last = finding
        print("  %-4s %-6s %s" % ("PASS" if ok else "FAIL", kind, detail))
    arith = sum(1 for r in results if r[1] in ("ARITH", "COUNT", "MATCH"))
    on_page = sum(1 for r in results if r[4].startswith("page"))
    other = sorted({r[4] for r in results if not r[4].startswith("page")})
    print("\n%d checks, %d failed." % (len(results), len(fails)))
    print("  %d read their values from a published page (a guide or the hub); the other %d read %s."
          % (on_page, len(results) - on_page, ", ".join(other) or "nothing else"))
    print("  %d of them recompute a figure the page states from the page's own operands." % arith)
    print("  None compares against an answer typed into this script. One (PR-1) supplies operands the page")
    print("  does not print: UK Lotto's 6-from-59 rule, to test the page's rounded '1 in 45 million'.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
