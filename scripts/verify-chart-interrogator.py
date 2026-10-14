#!/usr/bin/env python3
# ci-line: Chart Interrogator (independent recomputation of every key and tolerance) |
"""Verify Chart Interrogator's marking: box plots, stem and leaf, and the histogram modal-class item.

Reads the scenario data off the live page under Playwright, recomputes every key independently
(exact arithmetic for the readings; frequency density for the histograms), checks the game's
own values against them, then marks answers through the game's own controls:

  stem and leaf  - marked exactly: the key is accepted, in equivalent forms (35.5 and 35.50);
                   the key rounded to the table's precision (35 and 36 for 35.5) is rejected.
  box plots      - 2.5% of the drawn axis for a median, 5% for an IQR, each capped below half
                   the gap to the nearest named wrong answer (the other group's median and the
                   box's own Q1 and Q3, for a median; the other group's IQR and either
                   group's range, for an IQR). Canon 7.1.2.
  cumulative     - each reading to 2.5% of the axis (IQR 5%, the benchmark count 2.5% of n),
  frequency        capped below half the gap to the nearest named wrong answer: the other two
                   quartiles and the quartile's own position (n/4, n/2, 3n/4); for the IQR the
                   position difference n/2 and the axis range; for the count its complement.
                   Keys are recomputed here from the Bezier curve the game draws, and every
                   pixel-measured reading of the drawn curve (Contract B's record) must pass.
  all three      - no named wrong answer is ever accepted; just inside the band is accepted,
                   just outside is rejected (submitPhase1(), and submitPhase2() for the count).
                   Every histogram class is a whole number of observations (todo 1.15).
  histograms     - "[class] contains N people. Is it the modal class?" (todo 1.8). The key is
                   Yes exactly when the named class has the highest frequency density. For EVERY
                   class of every histogram, not only the one each scenario names: exactly one
                   option is keyed, "...contains the most..." is offered only when true of that
                   class and is never keyed. Through submitPhase2(), exactly one option of each
                   scenario is accepted, and choosing the most-observations option where the key
                   is Yes says "Right answer, wrong reason." Reports the Yes/No split.

A fault-injection self-test runs on every invocation: eight faults are injected into the page
source, and each must make the check FAIL, or the run fails.

  python scripts/verify-chart-interrogator.py [--chromium PATH]

Exit 0 when every check passes and every injected fault is caught, 1 otherwise. Uses the stub
server, so nothing reaches the live analytics endpoint or leaderboard.
"""
import argparse
import os
import statistics
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common  # noqa: E402

from playwright.sync_api import sync_playwright  # noqa: E402

DATA = """() => ({stemleaf: STEM_LEAF, boxplot: BOX_PLOTS, cumfreq: CUM_FREQ, histogram: HISTOGRAMS})"""

# Builds one scenario's Phase 1 questions with the game's own function.
BUILD = """([type, id]) => {
  const s = ({stemleaf: STEM_LEAF, boxplot: BOX_PLOTS, cumfreq: CUM_FREQ, histogram: HISTOGRAMS})[type].find(x => x.id === id);
  selectedType = type; selectedLevel = s.level; currentScenario = s; sessionAnswers = {};
  buildPhase1Questions();
  return phase1Questions.map(q => ({key: q.key, expected: q.expected, tolerance: q.tolerance, alt: q.alt || null, text: q.text}));
}"""

# Marks each case through the game's input and submitPhase1(); a timer stub stops a correct
# answer advancing the question under the next case.
MARK = """(cases) => {
  window.setTimeout = function () { return 0; };
  return cases.map(c => {
    const s = ({stemleaf: STEM_LEAF, boxplot: BOX_PLOTS, cumfreq: CUM_FREQ, histogram: HISTOGRAMS})[c.type].find(x => x.id === c.id);
    selectedType = c.type; selectedLevel = s.level; currentScenario = s; sessionAnswers = {};
    buildPhase1Questions(); currentPhase = 1; currentQIndex = c.qi; showCurrentQuestion();
    document.getElementById('qInput').value = c.typed; submitPhase1();
    return document.getElementById('qFeedback').className.indexOf('correct') >= 0;
  });
}"""


def num(v):
    """A Fraction from a JS number, through its shortest decimal form (4.4, not 4.4000000000000004)."""
    return F(repr(float(v)))


def typed(v):
    """How a student would type an exact value: 2.4, not 2.3999999999999995."""
    s = ("%.10f" % float(v)).rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def stemleaf_truth(s):
    a, b = [num(x) for x in s["a"]], [num(x) for x in s["b"]]
    prec = F(1, 10) if s.get("decimal") else F(1)
    keys = {"medA": statistics.median(a), "medB": statistics.median(b),
            "rangeA": max(a) - min(a), "rangeB": max(b) - min(b)}
    wrong = {"medA": [keys["medB"]], "medB": [keys["medA"]],
             "rangeA": [keys["rangeB"]], "rangeB": [keys["rangeA"]]}
    return keys, {k: F(0) for k in keys}, wrong, prec


def boxplot_truth(s):
    A = {k: num(v) for k, v in s["a"].items()}
    B = {k: num(v) for k, v in s["b"].items()}
    lo, hi = min(A["min"], B["min"]), max(A["max"], B["max"])
    band = (hi - lo) * F(12, 10) * F(1, 40)
    iqrA, iqrB = A["q3"] - A["q1"], B["q3"] - B["q1"]
    spreads = [iqrA, iqrB, A["max"] - A["min"], B["max"] - B["min"]]
    keys = {"medA": A["med"], "medB": B["med"], "iqrA": iqrA, "iqrB": iqrB}
    wrong, tol = {}, {}
    for k, base, pool in (("medA", band, [B["med"], A["q1"], A["q3"]]),
                          ("medB", band, [A["med"], B["q1"], B["q3"]]),
                          ("iqrA", 2 * band, spreads), ("iqrB", 2 * band, spreads)):
        wrong[k] = sorted({w for w in pool if w != keys[k]})
        gap = min(abs(w - keys[k]) for w in wrong[k])
        tol[k] = min(base, gap / 2)  # the game sits a billionth below gap/2: strictly below half
    return keys, tol, wrong, None



# Every class of every histogram, through the game's own histQuestion(), and the class each
# scenario actually names (histNamed()).
HIST_ALL = """() => HISTOGRAMS.map(s => ({
  id: s.id,
  named: histNamed(s).interval,
  perClass: histClasses(s).map(c => {
    const q = histQuestion(s, c);
    return {interval: c.interval, options: q.options, correct: q.correct, near: q.near, lead: q.lead};
  })
}))"""

# Phase 2 of each histogram, marked option by option through submitPhase2().
HIST_MARK = """() => {
  window.setTimeout = function () { return 0; };
  return HISTOGRAMS.map(s => {
    const res = [];
    const setup = () => {
      selectedType = 'histogram'; selectedLevel = s.level; currentScenario = s; sessionAnswers = {};
      document.getElementById('gameContainer').style.display = 'block';
      drawDiagram(); buildPhase1Questions();
      phase1Questions.forEach(q => { sessionAnswers[q.key] = q.expected; });
      currentPhase = 2; showPhase2();
      return document.querySelector('.scaffold-text select');
    };
    const opts = [...setup().options].slice(1).map(o => o.value);
    for (const o of opts) {
      const sel = setup(); sel.value = o; submitPhase2();
      const fb = document.getElementById('p2Feedback');
      res.push({option: o, accepted: fb.className.indexOf('correct') >= 0, feedback: fb.textContent});
    }
    return {id: s.id, results: res};
  });
}"""

YES = "Yes, because it has the highest frequency density"
NO = "No, because another class has a higher frequency density"
NEAR_TEXT = "Right answer, wrong reason."


def hist_truth(s):
    """Independent of the game: each class's frequency and frequency density, the modal class
    (highest density) and the most populous class, both required to be unique, and the class
    the scenario's `ask` names."""
    cls = []
    for d in s["data"]:
        lo, hi, fd = num(d["lo"]), num(d["hi"]), num(d["fd"])
        cls.append({"interval": "%s\u2013%s" % (typed(lo), typed(hi)), "freq": fd * (hi - lo),
                    "fd": fd, "width": hi - lo})
    fds = sorted((c["fd"] for c in cls), reverse=True)
    freqs = sorted((c["freq"] for c in cls), reverse=True)
    modal = max(cls, key=lambda c: c["fd"])
    most = max(cls, key=lambda c: c["freq"])
    ask = s.get("ask", "most")
    if ask == "modal":
        named = modal
    elif ask == "wide":
        wide = [c for c in cls if c is not modal and c["width"] > modal["width"]]
        named = max(wide, key=lambda c: c["freq"]) if wide else most
    else:
        named = most
    return cls, modal, most, named, fds[0] == fds[1], freqs[0] == freqs[1]


# SWEEP-1 (chart-interrogator-s1-002, s1-003): each histogram's drawn labels name every class boundary, and its
# "highest frequency" question offers four different classes, the tallest bar among them where it is not the key.
HIST_SWEEP = """() => {
  const out = [];
  const C = CanvasRenderingContext2D.prototype, f = C.fillText;
  for (const s of HISTOGRAMS) {
    const texts = []; C.fillText = function (t, ...a) { texts.push(String(t)); return f.call(this, t, ...a); };
    currentScenario = s; selectedType = 'histogram'; selectedLevel = s.level; sessionAnswers = {};
    const d = document.createElement('div'); drawHistogram(d); C.fillText = f;
    buildPhase1Questions();
    const q1 = phase1Questions.find(q => q.key === 'maxInterval');
    out.push({id: s.id, texts, bounds: s.data.map(x => x.lo).concat([s.data[s.data.length - 1].hi]), options: q1.options,
              key: q1.expected, tallest: s.data.reduce((a, b) => a.fd > b.fd ? a : b)});
  }
  return out;
}"""


def hist_sweep_fails(page):
    out = []
    for h in page.evaluate(HIST_SWEEP):
        for b in h['bounds']:
            if ('%g' % b) not in h['texts']:
                out.append('%s: the class boundary %g is not labelled on the x-axis (chart-interrogator-s1-002)' % (h['id'], b))
        opts = h['options']
        tallest = '%g\u2013%g' % (h['tallest']['lo'], h['tallest']['hi'])
        if len(opts) != 4 or len(set(opts)) != 4:
            out.append('%s: "highest frequency" offers %d options %s, not four different classes (SR-4)' % (h['id'], len(opts), opts))
        if tallest != h['key'] and tallest not in opts:
            out.append('%s: the tallest bar %s, the named error, is not offered (SR-4)' % (h['id'], tallest))
    return out


def check_histograms(page, data, fails):
    fails.extend(hist_sweep_fails(page))
    checks, split, report = 0, {"Yes": 0, "No": 0}, []
    game = {g["id"]: g for g in page.evaluate(HIST_ALL)}
    marked = {m["id"]: m["results"] for m in page.evaluate(HIST_MARK)}
    for s in data["histogram"]:
        sid, g = s["id"], game[s["id"]]
        cls, modal, most, named, tie_fd, tie_freq = hist_truth(s)
        checks += 2
        for c in cls:
            checks += 1
            if c["freq"].denominator != 1:
                fails.append("%s: class %s holds %s observations, not a whole number" % (sid, c["interval"], c["freq"]))
        if tie_fd or tie_freq:
            fails.append("%s: tie for the %s, so the item is undecidable" % (sid, "modal class" if tie_fd else "most populous class"))
        if g["named"] != named["interval"]:
            fails.append("%s: game names %s, the scenario's ask=%s names %s" % (sid, g["named"], s.get("ask", "most"), named["interval"]))
        # Every class, not only the named one: no choice of class may key two options, key the
        # misconception, key anything but density, or offer a "most" claim that is false.
        for c, q in zip(cls, g["perClass"]):
            where = "%s, named class %s" % (sid, c["interval"])
            checks += 5
            want = YES if c is modal else NO
            if q["correct"] != want:
                fails.append("%s: keyed %r, frequency density says %r" % (where, q["correct"], want))
            if [o for o in q["options"] if o == q["correct"]] != [q["correct"]] or len(set(q["options"])) != len(q["options"]):
                fails.append("%s: the key is not exactly one of the options %r" % (where, q["options"]))
            most_opts = [o for o in q["options"] if "contains the most" in o]
            if (len(most_opts) == 1) != (c is most) or len(most_opts) > 1:
                fails.append("%s: 'contains the most' offered=%s, true of this class=%s" % (where, bool(most_opts), c is most))
            if any(o == q["correct"] for o in most_opts):
                fails.append("%s: the most-observations option is keyed correct" % where)
            if (q["near"] is not None) != (c is most and c is modal):
                fails.append("%s: right-answer-wrong-reason set=%s, should be %s" % (where, q["near"] is not None, c is most and c is modal))
        # The named class, marked through submitPhase2().
        if named["freq"].denominator != 1:
            fails.append("%s: named class %s holds %s, not a whole number" % (sid, named["interval"], named["freq"]))
        key = YES if named is modal else NO
        res = marked[sid]
        accepted = [r["option"] for r in res if r["accepted"]]
        checks += 2
        if accepted != [key]:
            fails.append("%s: submitPhase2 accepted %r, the key is %r" % (sid, accepted, key))
        for r in res:
            checks += 1
            is_near = "contains the most" in r["option"] and named is modal
            if is_near != r["feedback"].startswith(NEAR_TEXT):
                fails.append("%s: choosing %r gave feedback %r" % (sid, r["option"], r["feedback"][:60]))
        split["Yes" if named is modal else "No"] += 1
        report.append("%s %s (%s, %d %s, fd %s; modal %s) -> %s" % (
            sid, named["interval"], s.get("ask", "most"), named["freq"], s["contextPlural"], typed(named["fd"]),
            modal["interval"], "Yes" if named is modal else "No"))
    return checks, split, report


# The benchmark count is typed in Phase 2: every dropdown is set to its key, the count to the
# case's value, and submitPhase2() must accept exactly when the count is within tolerance.
CF_BENCH = """(cases) => {
  window.setTimeout = function () { return 0; };
  return cases.map(c => {
    const s = CUM_FREQ.find(x => x.id === c.id);
    selectedType = 'cumfreq'; selectedLevel = s.level; currentScenario = s; sessionAnswers = {};
    document.getElementById('gameContainer').style.display = 'block';
    buildPhase1Questions(); phase1Questions.forEach(q => { sessionAnswers[q.key] = q.expected; });
    currentPhase = 2; showPhase2();
    document.querySelectorAll('.scaffold-text select').forEach(sel => { sel.value = sel.dataset.correct; });
    const inp = document.querySelector('.scaffold-text input');
    inp.value = c.typed; submitPhase2();
    return {accepted: document.getElementById('p2Feedback').className.indexOf('correct') >= 0,
            expected: +inp.dataset.expected, tolerance: +inp.dataset.tolerance};
  });
}"""

# Contract B's record (docs/audit-chart-interrogator-cumfreq.md): Q1, median and Q3 measured
# from the pixels of the drawn curve, independent of any key code. A correct reading must pass.
CF_PIXEL = {
    "CF1": (33.846, 44.779, 54.737), "CF2": (105.432, 115.897, 126.147), "CF3": (34.118, 43.935, 53.281),
    "CF4": (21.468, 26.907, 34.563), "CF5": (33.392, 37.904, 45.097), "CF6": (185.552, 231.326, 280.604),
    "CF7": (1120.876, 1330.478, 1546.757), "CF8": (33.267, 37.913, 42.639), "CF9": (1.525, 2.525, 3.565),
    "CF10": (48.696, 50.768, 52.724),
}


def cf_curve(s):
    """The game's curve, rebuilt here: per class one cubic Bezier between its two cumulative
    points, both control points at the class midpoint, level with each end."""
    segs, x, c = [], float(s["data"][0]["lo"]), 0.0
    for d in s["data"]:
        hi, f = float(d["hi"]), float(d["f"])
        mid = (x + hi) / 2
        segs.append(((x, c), (mid, c), (mid, c + f), (hi, c + f)))
        x, c = hi, c + f
    return segs


def _bez(g, a, t):
    u = 1 - t
    return u ** 3 * g[0][a] + 3 * u * u * t * g[1][a] + 3 * u * t * t * g[2][a] + t ** 3 * g[3][a]


def _solve(g, a, v):
    if v <= g[0][a]:
        return 0.0
    if v >= g[3][a]:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _bez(g, a, mid) < v else (lo, mid)
    return (lo + hi) / 2


def cf_x_at(s, cf):
    segs = cf_curve(s)
    g = next((q for q in segs if cf <= q[3][1]), segs[-1])
    return _bez(g, 0, _solve(g, 1, cf))


def cf_at_x(s, x):
    segs = cf_curve(s)
    g = next((q for q in segs if x <= q[3][0]), segs[-1])
    return _bez(g, 1, _solve(g, 0, x))


def cf_truth(s):
    n = s["n"]
    span = float(s["data"][-1]["hi"]) - float(s["data"][0]["lo"])
    q1, md, q3 = cf_x_at(s, n / 4), cf_x_at(s, n / 2), cf_x_at(s, 3 * n / 4)
    below = cf_at_x(s, float(s["benchVal"]))
    bench = n - below if s["benchSide"] == "above" else below
    keys = {"q1": q1, "median": md, "q3": q3, "iqr": q3 - q1, "bench": bench}
    wrong = {"q1": [md, q3, n / 4], "median": [q1, q3, n / 2], "q3": [q1, md, 3 * n / 4],
             "iqr": [n / 2, span], "bench": [n - bench]}
    band = {"q1": span / 40, "median": span / 40, "q3": span / 40, "iqr": span / 20, "bench": n / 40}
    tol = {}
    for k in keys:
        gaps = [abs(w - keys[k]) for w in wrong[k] if abs(w - keys[k]) > 1e-9]
        tol[k] = min(band[k], min(gaps) / 2) if gaps else band[k]
        wrong[k] = [w for w in wrong[k] if abs(w - keys[k]) > 1e-9]
    return keys, tol, wrong, band, span


def cf_poly(s):
    """The polygon: the same cumulative points joined by straight lines (chart-interrogator-s1-005)."""
    pts, x, c = [(float(s["data"][0]["lo"]), 0.0)], 0.0, 0.0
    for d in s["data"]:
        c += float(d["f"])
        pts.append((float(d["hi"]), c))
    return pts


def poly_x_at(s, cf):
    pts = cf_poly(s)
    for (x0, c0), (x1, c1) in zip(pts, pts[1:]):
        if cf <= c1:
            return x0 + (x1 - x0) * (cf - c0) / (c1 - c0)
    return pts[-1][0]


def poly_at_x(s, x):
    pts = cf_poly(s)
    for (x0, c0), (x1, c1) in zip(pts, pts[1:]):
        if x <= x1:
            return c0 + (c1 - c0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def cf_alt(s, keys, wrong, band):
    """The polygon's readings and their bands, each capped below the nearest named wrong answer of either drawing."""
    n = s["n"]
    span = float(s["data"][-1]["hi"]) - float(s["data"][0]["lo"])
    pq1, pmd, pq3 = poly_x_at(s, n / 4), poly_x_at(s, n / 2), poly_x_at(s, 3 * n / 4)
    pbelow = poly_at_x(s, float(s["benchVal"]))
    pbench = n - pbelow if s["benchSide"] == "above" else pbelow
    alt = {"q1": pq1, "median": pmd, "q3": pq3, "iqr": pq3 - pq1, "bench": pbench}
    pool = {"q1": [pmd, pq3, n / 4, keys["median"], keys["q3"]], "median": [pq1, pq3, n / 2, keys["q1"], keys["q3"]],
            "q3": [pq1, pmd, 3 * n / 4, keys["q1"], keys["median"]], "iqr": [n / 2, span],
            "bench": [n - pbench, n - keys["bench"]]}
    tol = {}
    for k in alt:
        gaps = [abs(w - alt[k]) for w in pool[k] if abs(w - alt[k]) > 1e-9]
        tol[k] = min(band[k], min(gaps) / 2) if gaps else band[k]
    return alt, tol, pool


def check_cumfreq(page, data, fails):
    checks, cases, why, bench_cases, bench_why, report = 0, [], [], [], [], []
    for s in data["cumfreq"]:
        keys, tol, wrong, band, span = cf_truth(s)
        alt, atol, apool = cf_alt(s, keys, wrong, band)
        game = page.evaluate(BUILD, ["cumfreq", s["id"]])

        def ok_at(k, v, keys=keys, tol=tol, alt=alt, atol=atol):
            """Accepted by the curve's band or by the polygon's (chart-interrogator-s1-005)."""
            return abs(v - keys[k]) <= tol[k] or abs(v - alt[k]) <= atol[k]

        for qi, q in enumerate(game):
            k = q["key"]
            where = "%s %s" % (s["id"], k)
            checks += 4
            if abs(q["expected"] - keys[k]) > span * 1e-9:
                fails.append("%s: key %r, recomputed %r" % (where, q["expected"], keys[k]))
            if abs(q["tolerance"] - tol[k]) > span * 1e-7:
                fails.append("%s: tolerance %r, recomputed %r" % (where, q["tolerance"], tol[k]))
            ga = q.get("alt")
            if not ga or abs(ga["expected"] - alt[k]) > span * 1e-7 or abs(ga["tolerance"] - atol[k]) > span * 1e-7:
                fails.append("%s: polygon reading %r, recomputed %.6f +-%.6f (chart-interrogator-s1-005)" % (where, ga, alt[k], atol[k]))
            if any(ok_at(k, w) for w in wrong[k] + apool[k] if abs(w - keys[k]) > 1e-9 and abs(w - alt[k]) > 1e-9):
                fails.append("%s: a band reaches a named wrong answer" % where)

            def add(value, accept, label, qi=qi, where=where):
                cases.append({"type": "cumfreq", "id": s["id"], "qi": qi, "typed": "%.6f" % value})
                why.append((where, label, "%.6f" % value, accept))

            add(keys[k], True, "the key")
            add(alt[k], True, "the polygon's reading")
            for w in wrong[k]:
                add(w, False, "named wrong answer %g" % w)
            for sign in (1, -1):
                for f, lab in ((0.999, "just inside"), (1.001, "just outside")):
                    v = keys[k] + sign * tol[k] * f
                    add(v, ok_at(k, v), "%s the curve's band" % lab)
                    v = alt[k] + sign * atol[k] * f
                    add(v, ok_at(k, v), "%s the polygon's band" % lab)
            if k in ("q1", "median", "q3"):
                add(CF_PIXEL[s["id"]][("q1", "median", "q3").index(k)], True, "the pixel-measured reading of the drawn curve")
        cases_b = [(keys["bench"], True, "the key"), (alt["bench"], True, "the polygon's reading")]
        cases_b += [(w, False, "named wrong answer %g" % w) for w in wrong["bench"]]
        for sg in (1, -1):
            for f in (0.999, 1.001):
                for base_, t_ in ((keys["bench"], tol["bench"]), (alt["bench"], atol["bench"])):
                    v = base_ + sg * t_ * f
                    cases_b.append((v, ok_at("bench", v), "band edge"))
        for value, accept, label in cases_b:
            bench_cases.append({"id": s["id"], "typed": "%.6f" % value})
            bench_why.append(("%s bench" % s["id"], label, "%.6f" % value, accept))
        capped = [k for k in keys if tol[k] < band[k] - 1e-12]
        moved = [k for k in keys if abs(alt[k] - keys[k]) > tol[k]]
        report.append("%s %s%s" % (s["id"], ", ".join("%s +-%.4g -> +-%.4g" % (k, band[k], tol[k]) for k in capped)
                                   if capped else "no band capped",
                                   "; polygon outside the curve's band: " + ", ".join(moved) if moved else ""))
    got = page.evaluate(MARK, cases) + [r["accepted"] for r in page.evaluate(CF_BENCH, bench_cases)]
    for (where, label, text, accept), ok in zip(why + bench_why, got):
        checks += 1
        if ok != accept:
            fails.append("%s: typed %s (%s) was %s" % (where, text, label, "accepted" if ok else "rejected"))
    return checks, len(cases) + len(bench_cases), report


# SWEEP-1 (chart-interrogator-s1-001): a histogram frequency is a density read off the drawn axis times a width. Its band is
# 2.5% of the density axis's span (the tallest bar is 90% of the plot height) times the class width, the total's times the
# whole x width, each capped below half the gap to the nearest named wrong answer (canon 7.1.2).
def hist_phase1(s):
    cls = [{"lo": num(d["lo"]), "hi": num(d["hi"]), "fd": num(d["fd"])} for d in s["data"]]
    for c in cls:
        c["width"] = c["hi"] - c["lo"]
        c["freq"] = c["fd"] * c["width"]
    total = sum(c["freq"] for c in cls)
    most = cls[0]
    for c in cls[1:]:
        if c["freq"] > most["freq"]:
            most = c
    ask = cls[2] if cls[1] is most else cls[1]
    axis = max(c["fd"] for c in cls) / F(9, 10)
    d_band = axis / 40
    keys = {"askFreq": ask["freq"], "total": total}

    def cap(band, key, wrongs):
        gaps = [abs(w - key) for w in wrongs if abs(w - key) > 0]
        return min(band, min(gaps) / 2) if gaps else band

    wrong = {"askFreq": [ask["fd"], total], "total": [sum(c["fd"] for c in cls), ask["freq"]]}
    tol = {"askFreq": cap(d_band * ask["width"], ask["freq"], wrong["askFreq"]),
           "total": cap(d_band * (cls[-1]["hi"] - cls[0]["lo"]), total, wrong["total"])}
    return keys, tol, wrong


def check_hist_readings(page, data, fails):
    checks, cases, why, report = 0, [], [], []
    for s in data["histogram"]:
        keys, tol, wrong = hist_phase1(s)
        game = page.evaluate(BUILD, ["histogram", s["id"]])
        by_key = {q["key"]: (qi, q) for qi, q in enumerate(game)}
        for k in ("askFreq", "total"):
            qi, q = by_key[k]
            where = "%s %s" % (s["id"], k)
            checks += 2
            if abs(num(q["expected"]) - keys[k]) > F(1, 2):
                fails.append("%s: key %r, recomputed %s" % (where, q["expected"], keys[k]))
            if abs(num(q["tolerance"]) - tol[k]) > F(1, 10**6):
                fails.append("%s: tolerance %r, recomputed %s (the old fixed 1 is not a band read from the scale)" % (where, q["tolerance"], float(tol[k])))
            if any(abs(w - num(q["expected"])) <= num(q["tolerance"]) for w in wrong[k]):
                fails.append("%s: tolerance %r reaches a named wrong answer" % (where, q["tolerance"]))
            key = num(q["expected"])
            for w in wrong[k]:
                cases.append({"type": "histogram", "id": s["id"], "qi": qi, "typed": typed(w)})
                why.append((where, "named wrong answer %s" % typed(w), typed(w), False))
            cases.append({"type": "histogram", "id": s["id"], "qi": qi, "typed": typed(key)})
            why.append((where, "the key", typed(key), True))
            for sign in (1, -1):
                for f, ok in ((F(999, 1000), True), (F(1001, 1000), False)):
                    v = key + sign * tol[k] * f
                    cases.append({"type": "histogram", "id": s["id"], "qi": qi, "typed": "%.6f" % float(v)})
                    why.append((where, "%s the band" % ("just inside" if ok else "just outside"), "%.6f" % float(v), ok))
        report.append("%s frequency +-%.3g, total +-%.3g" % (s["id"], float(tol["askFreq"]), float(tol["total"])))
        # s1-006: the proportion is asked of a class, not a "range" (the word is also a statistic)
        prop = by_key["proportion"][1]["text"]
        checks += 1
        if " in the class " not in prop or "range" in prop:
            fails.append("%s: the proportion question reads %r; it must say 'in the class', not 'in the range' (chart-interrogator-s1-006)" % (s["id"], prop))
    got = page.evaluate(MARK, cases)
    for (where, label, text, accept), ok in zip(why, got):
        checks += 1
        if ok != accept:
            fails.append("%s: typed %s (%s) was %s" % (where, text, label, "accepted" if ok else "rejected"))
    return checks, len(cases), report


# SWEEP-1 (chart-interrogator-s1-004): a stem-and-leaf table writes each leaf with as many digits as the key does
# (a 0 under stems of 100 is "00") and each stem as the key does ("2|40", never "02").
SL_DRAW = """() => STEM_LEAF.map(s => {
  currentScenario = s; selectedType = 'stemleaf';
  const d = document.createElement('div'); drawStemLeaf(d);
  return {id: s.id, rows: Array.from(d.querySelectorAll('tr')).slice(1).map(r => Array.from(r.children).map(c => c.textContent))};
})"""


def check_stemleaf_layout(page, data, fails):
    checks = 0
    drawn = {d["id"]: d["rows"] for d in page.evaluate(SL_DRAW)}
    for s in data["stemleaf"]:
        div, dec = s["stemDiv"], s.get("decimal")
        width = len(str(div)) - 1
        def leaf(v, st):
            return str(int(round((num(v) - st * div) * 10))) if dec else str(int(num(v)) % div).zfill(width)
        stems = sorted({int(num(v) // div) for v in s["a"] + s["b"]})
        want = []
        for st in stems:
            la = [leaf(v, st) for v in sorted(s["a"], key=num) if int(num(v) // div) == st]
            lb = [leaf(v, st) for v in sorted(s["b"], key=num) if int(num(v) // div) == st]
            want.append(["  ".join(reversed(la)), str(st), "  ".join(lb)])
        checks += 1
        if drawn[s["id"]] != want:
            bad = next((a for a, b in zip(drawn[s["id"]], want) if a != b), None)
            fails.append("%s: the drawn table differs from the recomputed one (first row %r, expected %r) (chart-interrogator-s1-004)"
                         % (s["id"], bad, next(b for a, b in zip(drawn[s["id"]], want) if a != b) if bad else None))
    return checks


def check_readings(page, data, fails):
    checks, cases, why = 0, [], []
    for typ, truth in (("stemleaf", stemleaf_truth), ("boxplot", boxplot_truth)):
        for s in data[typ]:
            keys, tol, wrong, prec = truth(s)
            game = page.evaluate(BUILD, [typ, s["id"]])
            for qi, q in enumerate(game):
                k, key, t = q["key"], keys[q["key"]], tol[q["key"]]
                where = "%s %s" % (s["id"], k)
                checks += 2
                if abs(num(q["expected"]) - key) > F(1, 10**9):
                    fails.append("%s: key %r, recomputed %s" % (where, q["expected"], key))
                # The game's tolerance: equal to the recomputed one, and never so wide that it
                # reaches a named wrong answer.
                game_t = F(q["tolerance"])
                scale = prec if prec is not None else key or 1
                if not (t - abs(scale) * F(1, 10**6) <= game_t <= t + abs(scale) * F(1, 10**6)):
                    fails.append("%s: tolerance %r, recomputed %s" % (where, q["tolerance"], float(t)))
                if any(abs(w - key) <= game_t for w in wrong[k]):
                    fails.append("%s: tolerance %r reaches a named wrong answer" % (where, q["tolerance"]))

                def add(value, accept, label, text=None):
                    cases.append({"type": typ, "id": s["id"], "qi": qi,
                                  "typed": text if text is not None else typed(value)})
                    why.append((where, label, text or typed(value), accept))

                add(key, True, "the key")
                for w in wrong[k]:
                    add(w, False, "named wrong answer %s" % typed(w))
                if typ == "stemleaf":
                    add(key, True, "the key with a trailing zero", typed(key) + ("0" if "." in typed(key) else ".0"))
                    for r in {(key / prec).__floor__() * prec, (key / prec).__ceil__() * prec} - {key}:
                        add(r, False, "the key rounded to the table's precision")
                else:
                    for sign in (1, -1):
                        add(key + sign * t * F(999, 1000), True, "just inside the band")
                        add(key + sign * t * F(1001, 1000), False, "just outside the band")

    got = page.evaluate(MARK, cases)
    for (where, label, text, accept), ok in zip(why, got):
        checks += 1
        if ok != accept:
            fails.append("%s: typed %s (%s) was %s" % (where, text, label, "accepted" if ok else "rejected"))
    return checks, len(cases)


def run(browser, base, mutate=None):
    """One full check of the page; `mutate` rewrites the game's source first (self-test)."""
    fails, errors = [], []
    page = browser.new_page()
    game_url = base + "/games/chart-interrogator/"

    def route(r):
        url = r.request.url
        if not url.startswith(base):
            return r.fulfill(status=200, body="")
        if mutate and url.split("?")[0] in (game_url, game_url + "index.html"):
            resp = r.fetch()
            return r.fulfill(response=resp, body=mutate(resp.text()))
        return r.continue_()

    page.route("**/*", route)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(game_url + "?cb=verify")
    data = page.evaluate(DATA)
    checks, n_cases = check_readings(page, data, fails)
    c_checks, c_cases, cf_report = check_cumfreq(page, data, fails)
    h_checks, split, report = check_histograms(page, data, fails)
    hr_checks, hr_cases, hr_report = check_hist_readings(page, data, fails)
    h_checks += hr_checks + check_stemleaf_layout(page, data, fails)
    n_cases += hr_cases
    page.close()
    if errors:
        fails.append("page errors: %s" % errors)
    return fails, checks + c_checks + h_checks, n_cases + c_cases, split, (report, cf_report + ['histogram bands: ' + '; '.join(hr_report)])


# Each must make the check FAIL. (description, text in the game, replacement)
FAULTS = [
    ("box-plot band uncapped", "return Math.min(band,gap/2*(1-1e-9));", "return band;"),
    ("s1-002: the class boundaries not labelled", "if(Math.abs(b/xStep-Math.round(b/xStep))>1e-9)ctx.fillText(", "if(false)ctx.fillText("),
    ("s1-003: options by position (three on six histograms)",
     ".concat(freqs).map(function(f){return f.interval;}).filter(unique).slice(0,4))},", ".map(function(f){return f.interval;}).filter(unique))},"),
    ("s1-001: a histogram frequency back to a fixed +-1", "tolerance:freqTol,key:'askFreq'", "tolerance:1,key:'askFreq'"),
    ("s1-001: the total back to a fixed +-1", "tolerance:totalTol,key:'total'", "tolerance:1,key:'total'"),
    ("s1-005: the polygon's reading not accepted", "return Math.abs(val-expected)<=tolerance||(!!alt&&Math.abs(val-alt.expected)<=alt.tolerance);", "return Math.abs(val-expected)<=tolerance;"),
    ("s1-004: leaves not padded", ".padStart(String(div).length-1,'0')", ""),
    ("s1-004: stems padded to two digits", "var stemLabel=st.toString();", "var stemLabel=s.stemWidth===2&&st<10?'0'+st:st.toString();"),
    ("s1-006: 'in the range' back", "' in the class '+propInterval.interval", "' in the range '+propInterval.interval"),
    ("cumulative-frequency median uncapped", "median:capTol(xTol,median,[q1,q3,n/2])", "median:xTol"),
    ("stem and leaf to the nearest half unit", "var slTol=(s.decimal?0.1:1)*1e-9;", "var slTol=(s.decimal?0.1:1)*0.5;"),
    ("a histogram class of 22.5 observations (todo 1.15)", "{lo:35,hi:40,fd:4.6}", "{lo:35,hi:40,fd:4.5}"),
    ("histogram keyed on frequency, not density",
     "var isModal=named.interval===modal.interval,", "var isModal=named.interval===most.interval,"),
    ("'contains the most' offered for every class",
     "options:isMost?[mostOpt,HIST_YES,HIST_NO]:[HIST_YES,HIST_NO],", "options:[mostOpt,HIST_YES,HIST_NO],"),
    ("the misconception keyed correct as well",
     "correct:isModal?HIST_YES:HIST_NO,", "correct:isModal&&isMost?mostOpt:isModal?HIST_YES:HIST_NO,"),
    ("no 'right answer, wrong reason' feedback",
     "fb.textContent=near?'Right answer, wrong reason. '+near.dataset.why", "fb.textContent=false?''"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--chromium", help="Chromium executable (default: Playwright's own)")
    args = ap.parse_args()

    proc, base = bank_common.start_stub_server()
    missed = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(**({"executable_path": args.chromium} if args.chromium else {}))
            for name, old, new in FAULTS:
                def mutate(src, old=old, new=new, name=name):
                    if src.count(old) != 1:
                        raise SystemExit("self-test: the text for fault '%s' is not in the game once; update FAULTS" % name)
                    return src.replace(old, new)
                caught = run(browser, base, mutate)[0]
                print("self-test: %-45s %s" % (name, "caught (%d failures)" % len(caught) if caught else "NOT CAUGHT"))
                if not caught:
                    missed.append(name)
            fails, checks, n_cases, split, report = run(browser, base)
            browser.close()
    finally:
        proc.terminate()

    report, cf_report = report
    print("cumulative frequency (bands capped by canon 7.1.2):")
    for line in cf_report:
        print("  " + line)
    print("histogram items (named class, how chosen, count, density; modal class -> key):")
    for line in report:
        print("  " + line)
    print("histogram keys: %d Yes / %d No" % (split["Yes"], split["No"]))
    print("%d checks, %d marking cases through submitPhase1()/submitPhase2(), %d failures" % (checks, n_cases, len(fails)))
    for f in fails:
        print("  FAIL " + f)
    for m in missed:
        print("  FAIL self-test: injected fault not caught: " + m)
    return 1 if fails or missed else 0


if __name__ == "__main__":
    sys.exit(main())
