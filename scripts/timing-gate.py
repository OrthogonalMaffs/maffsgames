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
import http.server
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
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
    series, regs = {}, {}
    for r in runs:
        for label, sec in r["lines"].items():
            series.setdefault(label, []).append(sec)
            regs.setdefault(label, []).append((r.get("regions") or {}).get(label, "unknown"))   # a record from before regions: unknown
    found = []
    for label, s in series.items():
        if s and runs[-1]["lines"].get(label) is not None:
            h = hits(s)
            if h and h[-1][0] == len(s) - 1:                      # the window ends at the newest run
                found.append((label, h[-1][1], h[-1][2], regs[label][-LAST:]))
    found.sort(key=lambda f: -(f[2][-1] - f[1]))
    # Region is shown, never used: the flagging above is region-blind until there are about 10 runs per region group.
    md = ["### Persistence report (warning only)", "",
          "Last %d of %d main runs each more than %d%% and at least %ds over the median of the runs before them."
          % (LAST, len(runs), int(PCT * 100), SECS), ""]
    warns = []
    if not found:
        md.append("No verifier has grown and stayed grown.")
    else:
        md += ["| Verifier | before (median s) | last %d runs (s) | region of each of those runs | rise |" % LAST, "|---|---|---|---|---|"]
        for label, b, last, where in found:
            short = label.split(" (")[0]
            md.append("| %s | %d | %s | %s | +%d%% |" % (short, b, ", ".join(str(x) for x in last), ", ".join(where),
                                                        round(100 * (median(last) / b - 1))))
            warns.append("::warning::persistent rise: %s was %ds, now %s (last %d runs, in %s)"
                         % (short, b, "/".join(str(x) for x in last), LAST, "/".join(where)))
        md += ["", "Verifier times differ by runner region (docs/handover/ci-slowdown-401.md); the rule does not yet allow for it."]
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


# The step reads time twice: bash's $SECONDS for each line and `date +%s` for the group. A self-test on the real clock
# is racy ($SECONDS counts whole seconds, so `sleep 2` reads as 3 whenever start-up overhead crosses a second; it failed
# once on main, run 38736408794). So the self-test runs a copy of the step whose clock reads come from a file, and each
# planted check advances that file by the seconds it is meant to take. The step's logic is the workflow's, unchanged.
CLOCK_SEAMS = [("start=$SECONDS", 'start=$(cat "$FAKE_CLOCK")', 1),
               ("took=$((SECONDS - start))", 'took=$(( $(cat "$FAKE_CLOCK") - start ))', 1),
               ("$(date +%s)", '$(cat "$FAKE_CLOCK")', 2)]


def on_fake_clock(script):
    """The step with its clock reads taken from $FAKE_CLOCK; refuses if the step reads time some other way."""
    for old, new, n in CLOCK_SEAMS:
        if script.count(old) != n:
            raise SystemExit("timing-gate selftest: the step reads time differently (%r appears %d times, expected %d): "
                             "update CLOCK_SEAMS" % (old, script.count(old), n))
        script = script.replace(old, new)
    if re.search(r"\bSECONDS\b|date \+%s", script):
        raise SystemExit("timing-gate selftest: a clock read is left on the real clock: update CLOCK_SEAMS")
    return script


def takes(seconds):
    """A planted check that takes `seconds` on the fake clock, instantly on the real one."""
    return 'echo $(( $(cat "$FAKE_CLOCK") + %d )) > "$FAKE_CLOCK"' % seconds


def run_step(script, checks, timeout_min, age, td, region_url="http://127.0.0.1:9/", fake=True):
    scripts = os.path.join(td, "scripts")
    os.makedirs(scripts, exist_ok=True)
    with open(os.path.join(scripts, "ci-timings.json"), "w", encoding="utf-8", newline="") as fh:
        json.dump({"lines": {"Slow verifier": 1, "Fast verifier": 1}}, fh)
    summary = os.path.join(td, "summary.md")
    open(summary, "w", encoding="utf-8", newline="").close()
    clock = os.path.join(td, "clock")
    with open(clock, "w", encoding="utf-8", newline="") as fh:
        fh.write("0\n")
    if fake:
        script = on_fake_clock(script)
        t0 = -age                     # the group started `age` seconds before the fake clock's 0
    else:
        t0 = int(time.time()) - age
    env = dict(os.environ, CHECKS=checks, GROUP="Content verifiers 99", TIMEOUT_MIN=str(timeout_min),
               JOB_T0=str(t0), RUNNER_TEMP=td, GITHUB_STEP_SUMMARY=summary, FAKE_CLOCK=clock,
               REGION_URL=region_url)
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
    rr = [{"run": i, "lines": {"Probability Paradox": v}} for i, v in enumerate(PP[:12], 1)]
    for r, g in zip(rr[-3:], ("eastus", "westus", "centralus")):
        r["regions"] = {"Probability Paradox": g}
    md, warns = report(rr)
    check("the report lists the region of each of the 3 flagged runs, in the table and in the annotation",
          "| eastus, westus, centralus |" in md and warns and "in eastus/westus/centralus" in warns[0])
    rr[-1].pop("regions")
    md, warns = report(rr)
    check("... and 'unknown' for a flagged run recorded before regions", "| eastus, westus, unknown |" in md)
    md2, warns2 = report([{"run": r["run"], "lines": r["lines"]} for r in rr])
    check("the regions change only what is shown: the same runs without regions flag the same line at the same figures",
          len(warns2) == len(warns) == 1 and "unknown, unknown, unknown" in md2)

    with open(os.path.join(ROOT, WORKFLOW), encoding="utf-8", newline="") as fh:
        text = fh.read()
    check("the workflow no longer raises the budget as an error", "::error::time budget" not in text)
    script = workflow_step(text)
    check("the step's pass/fail is the checks alone (the budget is not in its exit test)", re.search(r"^\[ \$\{#failed\[@\]\} -eq 0 \]\s*$", script, re.M) is not None)
    class Metadata(http.server.BaseHTTPRequestHandler):          # answers like the instance metadata service: a mixed-case name
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"WestUS3\n")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), Metadata)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "http://127.0.0.1:%d/" % srv.server_address[1]
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Slow verifier|%s\nFast verifier|%s" % (takes(2), takes(0)), 1, 100, td, url)
        check("a planted slow line past the 75% budget leaves the job green (exit 0)", code == 0)
        check("... with a warning annotation in the log, naming the runner region",
              "::warning::time budget (a warning, the job is not failed)" in out and "Slow verifier took 2s in westus3" in out)
        check("... and the summary names the group, the slow line, its time, its region and its recorded median",
              "Content verifiers 99" in summ and "Slow verifier took 2s in westus3 (recorded median 1s" in summ
              and "Runner region: westus3." in summ and "Over the time budget" in summ)
        with open(os.path.join(td, "ci-timing", "timing.txt"), encoding="utf-8") as fh:
            saved = fh.read()
        check("the saved timing file carries the region under the group name, and its lines are unchanged in form",
              saved.split("\n")[:2] == ["Content verifiers 99", "region: westus3"]
              and re.search(r"^ok  Slow verifier  [(]\d+s; group at ", saved, re.M) is not None)
        d = os.path.join(td, "artifacts", "ci-timing-content-1")
        os.makedirs(d)
        with open(os.path.join(d, "timing.txt"), "w", encoding="utf-8", newline="") as fh:
            fh.write(saved)
        old_d = os.path.join(td, "artifacts", "ci-timing-content-2")      # an artifact from before regions: no region line
        os.makedirs(old_d)
        with open(os.path.join(old_d, "timing.txt"), "w", encoding="utf-8", newline="") as fh:
            fh.write("Content verifiers 98\nok  Old line  (7s; group at 0m07s of 6m)\ngroup total: 0m09s of 6m (budget 4m30s)\n")
        rec = new_run(1, os.path.join(td, "artifacts"))
        check("a recorded run stores a region for every timed line (the old-format artifact reads as unknown)",
              rec["regions"] == {"Fast verifier": "westus3", "Old line": "unknown", "Slow verifier": "westus3"}
              and sorted(rec["lines"]) == sorted(rec["regions"]))
        spec = importlib.util.spec_from_file_location("ci_groups2", os.path.join(ROOT, "scripts", "ci-groups.py"))
        cg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cg)
        tm = cg.add_run({}, rec)
        check("the timing file's lines and medians are untouched by the regions (the packer and median-of-5 read what they did)",
              tm["lines"] == rec["lines"] and set(tm) == {"run", "date", "branch", "event", "setup", "lines", "history"})
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Slow verifier|%s\nFast verifier|%s" % (takes(2), takes(0)), 1, 100, td)  # the service does not answer
        check("with no answer from the metadata service the region is 'unknown' and the job is unaffected",
              code == 0 and "Slow verifier took 2s in unknown" in out and "Runner region: unknown." in summ)
    srv.shutdown()
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Slow verifier|%s" % takes(1), 1, 5, td)
        check("inside the budget: green and no warning", code == 0 and "::warning::" not in out and "Over the time budget" not in summ)
    with tempfile.TemporaryDirectory() as td:
        code, out, summ = run_step(script, "Bad verifier|%s; false\nSlow verifier|%s" % (takes(1), takes(1)), 1, 100, td)
        check("a failing check still fails the job, and the checks after it still run",
              code == 1 and "::error::FAILED: Bad verifier" in out and "Slow verifier" in summ)
    with tempfile.TemporaryDirectory() as td:
        # The one run of the step on the real clock: it runs and passes. Nothing here depends on how long it takes.
        code, out, summ = run_step(script, "Fast verifier|true", 1, 0, td, fake=False)
        check("the real step (real clock) runs a check and exits green, with its summary table",
              code == 0 and "| Fast verifier | ok |" in summ)
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
