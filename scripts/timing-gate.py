#!/usr/bin/env python3
# ci-line: Timing gate (the group budget step warns and does not fail; the persistence report finds Probability Paradox on its third slow run and ignores both flaky runs; contract TIMING-GATE) | --selftest
# ci-deps: .github/workflows/check-site.yml scripts/ci-groups.py scripts/ci-timings.json
"""The timing gate's non-blocking half: the persistence report, and the proof that the per-run budget only warns.

Contract TIMING-GATE (14 Oct 2026), from docs/handover/ci-timing-diagnosis.md (#400). What BLOCKS: the median-of-5 pack
and the 80% check (ci-groups.py --check, on every PR and in the main timings job), and each job's hard timeout against a
hang. What WARNS: a group past 75% of its timeout on that run's clock (the step in check-site.yml writes the group, the
slowest line against its recorded median and its time to the job summary and as an annotation, and the job passes), and
this report. Why: of 160 runs the per-run clock failed twice, both single-line stalls on unchanged code (Equation
Builder 260 s against 136 s; Spot the Muppet 290 s against 94 s), and it never saw the one real regression.

THE PERSISTENCE RULE. A verifier is reported when its last 3 main runs are EACH more than 20% and at least 15 s over the
median of the (up to) 5 runs before them (at least 3 of those). One slow run never reports, a lasting rise does. Probability
Paradox's 14 Oct rise (161 s to about 210 s) reports on the third slow run, the same run the pack check failed on.

  python scripts/timing-gate.py --report [--run-id ID --from-dir DIR]   the report for the main timings job (never fails)
  python scripts/timing-gate.py --selftest                              the backtest on recorded series, a planted
                                                                           rise, and the workflow step run with a planted slow line
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMINGS = "scripts/ci-timings.json"
WORKFLOW = ".github/workflows/check-site.yml"
PREV, LAST, PCT, SECS = 5, 3, 0.20, 15
GIT_VERSIONS = 5            # timing commits read back: with 5 runs in each, they cover the last 9 main runs


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def hits(series):
    """[(index of the third run, baseline, [the last 3])] for every window where the rule holds."""
    out = []
    for t in range(LAST - 1, len(series)):
        prev = series[max(0, t - LAST + 1 - PREV):t - LAST + 1]
        last = series[t - LAST + 1:t + 1]
        if len(prev) < 3:
            continue
        b = median(prev)
        if all(x > b * (1 + PCT) and x - b >= SECS for x in last):
            out.append((t, b, last))
    return out


def runs_from_git(root=ROOT):
    """Run records, oldest first: the union of the 'history' in the last GIT_VERSIONS committed ci-timings.json."""
    by = {}
    shas = subprocess.run(["git", "log", "--format=%H", "-n", str(GIT_VERSIONS), "--", TIMINGS], cwd=root,
                          capture_output=True, text=True, encoding="utf-8").stdout.split()
    texts = [subprocess.run(["git", "show", "%s:%s" % (s, TIMINGS)], cwd=root, capture_output=True, text=True,
                            encoding="utf-8").stdout for s in shas]
    try:
        with open(os.path.join(root, TIMINGS), encoding="utf-8", newline="") as fh:
            texts.append(fh.read())
    except OSError:
        pass
    for t in texts:
        try:
            for r in json.loads(t).get("history", []):
                by[r["run"]] = r
        except ValueError:
            pass
    return [by[k] for k in sorted(by)]


def new_run(run_id, from_dir):
    spec = importlib.util.spec_from_file_location("ci_groups", os.path.join(ROOT, "scripts", "ci-groups.py"))
    cg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cg)
    return cg.read_run(run_id, from_dir)


def report(runs):
    """(markdown, [warning lines]) for run records oldest first."""
    if len(runs) < LAST + 3:
        return ("### Persistence report\n\nOnly %d run(s) of history are readable; the rule needs at least %d. Nothing to report.\n"
                % (len(runs), LAST + 3)), []
    series = {}
    for r in runs:
        for label, sec in r["lines"].items():
            series.setdefault(label, []).append(sec)
    found = []
    for label, s in series.items():
        if s and runs[-1]["lines"].get(label) is not None:
            h = hits(s)
            if h and h[-1][0] == len(s) - 1:                      # the window ends at the newest run
                found.append((label, h[-1][1], h[-1][2]))
    found.sort(key=lambda f: -(f[2][-1] - f[1]))
    md = ["### Persistence report (warning only)", "",
          "Last %d of %d main runs each more than %d%% and at least %ds over the median of the runs before them."
          % (LAST, len(runs), int(PCT * 100), SECS), ""]
    warns = []
    if not found:
        md.append("No verifier has grown and stayed grown.")
    else:
        md += ["| Verifier | before (median s) | last %d runs (s) | rise |" % LAST, "|---|---|---|---|"]
        for label, b, last in found:
            short = label.split(" (")[0]
            md.append("| %s | %d | %s | +%d%% |" % (short, b, ", ".join(str(x) for x in last), round(100 * (median(last) / b - 1))))
            warns.append("::warning::persistent rise: %s was %ds, now %s (last %d runs)" % (short, b, "/".join(str(x) for x in last), LAST))
    return "\n".join(md) + "\n", warns


# --- the self-test -------------------------------------------------------------------------------------------------
# Real push-run series from the 160 runs behind the diagnosis (seconds per main run, oldest first).
PP = [162, 154, 155, 161, 161, 155, 160, 161, 161, 210, 211, 202, 51, 57, 57, 47, 51, 58, 51, 53, 51, 56, 48, 56, 58, 50,
      52, 47, 58, 49, 79, 59, 57, 79, 56]               # Probability Paradox: 161 -> ~210 after #371 -> 50 after #376
EB1 = [78, 145, 80, 145, 82, 146, 100, 144, 80, 145, 147, 77, 144, 154, 112, 148, 104, 145, 155, 82, 152, 153, 152, 155, 83,
       106, 108, 105, 153, 152, 85, 106, 152, 82, 154, 156, 155, 155, 80, 152, 152, 86, 150, 108, 141, 107, 114, 117, 84, 104,
       87, 108, 109, 153, 88, 157, 153, 98, 154, 78, 84, 138, 108, 136, 106, 153, 99, 154, 125, 105, 157, 136, 97, 260, 138,
       155, 127, 155, 156]                               # Equation Builder part 1, including the 260 s flake (run 38600298822)
STM = [78, 71, 78, 78, 77, 78, 72, 78, 78, 72, 75, 73, 79, 77, 78, 78, 74, 77, 79, 71, 71]   # Spot the Muppet's stable stretch
STM_FLAKE = STM[:10] + [290] + STM[10:]                  # with the 290 s flake of PR run 38556658031 injected


def workflow_step(text):
    """The group step's bash, dedented, from check-site.yml (without the leading `node --version`)."""
    a = text.index("          mmss() {")
    b = text.index("\n\n      # The group's timing lines", a)
    return "\n".join(l[10:] if l.startswith("          ") else l for l in text[a:b].split("\n"))


def run_step(script, checks, timeout_min, age, td):
    scripts = os.path.join(td, "scripts")
    os.makedirs(scripts, exist_ok=True)
    with open(os.path.join(scripts, "ci-timings.json"), "w", encoding="utf-8", newline="") as fh:
        json.dump({"lines": {"Slow verifier": 1, "Fast verifier": 1}}, fh)
    summary = os.path.join(td, "summary.md")
    open(summary, "w", encoding="utf-8", newline="").close()
    env = dict(os.environ, CHECKS=checks, GROUP="Content verifiers 99", TIMEOUT_MIN=str(timeout_min),
               JOB_T0=str(int(time.time()) - age), RUNNER_TEMP=td, GITHUB_STEP_SUMMARY=summary)
    py = '"%s"' % sys.executable.replace("\\", "/")
    r = subprocess.run(["bash", "-c", script.replace("python3 -c", py + " -c")], cwd=td, env=env, capture_output=True,
                       text=True, encoding="utf-8")
    with open(summary, encoding="utf-8") as fh:
        return r.returncode, r.stdout + r.stderr, fh.read()


def selftest():
    fails = []

    def check(name, ok):
        print("  %s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails.append(name)

    h = hits(PP)
    third_slow = PP.index(202)
    check("backtest: Probability Paradox is reported on the third slow run (the one the pack check failed on)",
          h and h[0][0] == third_slow and h[0][1] == 161 and h[0][2] == [210, 211, 202])
    check("backtest: the Equation Builder 260 s flake is never reported",
          not [x for x in hits(EB1) if 260 in EB1[x[0] - 2:x[0] + 1]])
    check("backtest: the Spot the Muppet 290 s flake is never reported", hits(STM_FLAKE) == [])
    check("a single slow run is never reported, however slow", hits(STM[:10] + [900] + STM[10:]) == [])
    check("a planted lasting rise (3 runs, +50%) is reported", hits([100, 101, 99, 100, 102, 150, 152, 149])[-1][0] == 7)
    check("two slow runs are not enough", hits([100, 101, 99, 100, 102, 150, 152, 101]) == [])
    check("a rise under 15 s is not reported", hits([20, 21, 19, 20, 20, 26, 26, 26]) == [])
    md, warns = report([{"run": i, "lines": {"Probability Paradox": v}} for i, v in enumerate(PP[:12], 1)])
    check("the report names Probability Paradox on its third slow run, as a warning",
          "Probability Paradox" in md and len(warns) == 1 and warns[0].startswith("::warning::"))
    md, warns = report([{"run": i, "lines": {"Probability Paradox": v}} for i, v in enumerate(PP[:11], 1)])
    check("the report is silent on the second slow run", warns == [] and "No verifier" in md)

    with open(os.path.join(ROOT, WORKFLOW), encoding="utf-8", newline="") as fh:
        text = fh.read()
    check("the workflow no longer raises the budget as an error", "::error::time budget" not in text)
    script = workflow_step(text)
    check("the step's pass/fail is the checks alone (the budget is not in its exit test)", re.search(r"^\[ \$\{#failed\[@\]\} -eq 0 \]\s*$", script, re.M) is not None)
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Slow verifier|sleep 2\nFast verifier|true", 1, 100, td)
        check("a planted slow line past the 75% budget leaves the job green (exit 0)", code == 0)
        check("... with a warning annotation in the log", "::warning::time budget (a warning, the job is not failed)" in out)
        check("... and the summary names the group, the slow line, its time and its recorded median",
              "Content verifiers 99" in summ and "Slow verifier took 2s (recorded median 1s)" in summ and "Over the time budget" in summ)
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Slow verifier|true", 1, 5, td)
        check("inside the budget: green and no warning", code == 0 and "::warning::" not in out and "Over the time budget" not in summ)
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Bad verifier|false\nSlow verifier|true", 1, 100, td)
        check("a failing check still fails the job, and the checks after it still run",
              code == 1 and "::error::FAILED: Bad verifier" in out and "Slow verifier" in summ)
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--run-id")
    ap.add_argument("--from-dir")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.report:
        runs = runs_from_git()
        if a.run_id and a.from_dir:
            rec = new_run(a.run_id, a.from_dir)
            if rec:
                runs = [r for r in runs if r["run"] != rec["run"]] + [rec]
        md, warns = report(runs)
        print(md)
        for w in warns:
            print(w, file=sys.stderr)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
