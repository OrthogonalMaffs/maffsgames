#!/usr/bin/env python3
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
  const s = ({stemleaf: STEM_LEAF, boxplot: BOX_PLOTS, cumfreq: CUM_FREQ})[type].find(x => x.id === id);
  selectedType = type; selectedLevel = s.level; currentScenario = s; sessionAnswers = {};
  buildPhase1Questions();
  return phase1Questions.map(q => ({key: q.key, expected: q.expected, tolerance: q.tolerance}));
}"""

# Marks each case through the game's input and submitPhase1(); a timer stub stops a correct
# answer advancing the question under the next case.
MARK = """(cases) => {
  window.setTimeout = function () { return 0; };
  return cases.map(c => {
    const s = ({stemleaf: STEM_LEAF, boxplot: BOX_PLOTS, cumfreq: CUM_FREQ})[c.type].find(x => x.id === c.id);
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


def check_histograms(page, data, fails):
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


def check_cumfreq(page, data, fails):
    checks, cases, why, bench_cases, bench_why, report = 0, [], [], [], [], []
    for s in data["cumfreq"]:
        keys, tol, wrong, band, span = cf_truth(s)
        game = page.evaluate(BUILD, ["cumfreq", s["id"]])
        for qi, q in enumerate(game):
            k = q["key"]
            where = "%s %s" % (s["id"], k)
            checks += 3
            if abs(q["expected"] - keys[k]) > span * 1e-9:
                fails.append("%s: key %r, recomputed %r" % (where, q["expected"], keys[k]))
            if abs(q["tolerance"] - tol[k]) > span * 1e-7:
                fails.append("%s: tolerance %r, recomputed %r" % (where, q["tolerance"], tol[k]))
            if any(abs(w - q["expected"]) <= q["tolerance"] for w in wrong[k]):
                fails.append("%s: tolerance %r reaches a named wrong answer" % (where, q["tolerance"]))

            def add(value, accept, label, qi=qi, where=where):
                cases.append({"type": "cumfreq", "id": s["id"], "qi": qi, "typed": "%.6f" % value})
                why.append((where, label, "%.6f" % value, accept))

            add(keys[k], True, "the key")
            for w in wrong[k]:
                add(w, False, "named wrong answer %g" % w)
            for sign in (1, -1):
                add(keys[k] + sign * tol[k] * 0.999, True, "just inside the band")
                add(keys[k] + sign * tol[k] * 1.001, False, "just outside the band")
            if k in ("q1", "median", "q3"):
                add(CF_PIXEL[s["id"]][("q1", "median", "q3").index(k)], True, "the pixel-measured reading of the drawn curve")
        for value, accept, label in ([(keys["bench"], True, "the key")] +
                                     [(w, False, "named wrong answer %g" % w) for w in wrong["bench"]] +
                                     [(keys["bench"] + sg * tol["bench"] * f, f < 1, "band edge")
                                      for sg in (1, -1) for f in (0.999, 1.001)]):
            bench_cases.append({"id": s["id"], "typed": "%.6f" % value})
            bench_why.append(("%s bench" % s["id"], label, "%.6f" % value, accept))
        capped = [k for k in keys if tol[k] < band[k] - 1e-12]
        report.append("%s %s" % (s["id"], ", ".join("%s +-%.4g -> +-%.4g" % (k, band[k], tol[k]) for k in capped)
                                 if capped else "no band capped"))
    got = page.evaluate(MARK, cases) + [r["accepted"] for r in page.evaluate(CF_BENCH, bench_cases)]
    for (where, label, text, accept), ok in zip(why + bench_why, got):
        checks += 1
        if ok != accept:
            fails.append("%s: typed %s (%s) was %s" % (where, text, label, "accepted" if ok else "rejected"))
    return checks, len(cases) + len(bench_cases), report


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
    page.close()
    if errors:
        fails.append("page errors: %s" % errors)
    return fails, checks + c_checks + h_checks, n_cases + c_cases, split, (report, cf_report)


# Each must make the check FAIL. (description, text in the game, replacement)
FAULTS = [
    ("box-plot band uncapped", "return Math.min(band,gap/2*(1-1e-9));", "return band;"),
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
