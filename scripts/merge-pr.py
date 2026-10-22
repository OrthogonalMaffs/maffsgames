#!/usr/bin/env python3
# ci-line: Merge guard (scripts/merge-pr.py: green Gate and green main or no merge; override only for main; recorded API fixtures) | --selftest
"""The one way either lane merges a PR (CLAUDE.md "Neither lane merges while main's last full run is red", canon §7.8.3).

    python scripts/merge-pr.py <number>                      # merge if the guard passes, else refuse (exit 1)
    python scripts/merge-pr.py <number> --wait 600           # while a check is still running, poll up to 600 s, then refuse
    python scripts/merge-pr.py <number> --override "<Jon's ruling and date>"
    python scripts/merge-pr.py --selftest                    # recorded API fixtures; no network

The guard, from the GitHub REST API through `gh api` (the credentials the lanes already use):

  (a) the PR is open, and its Gate ("Gate (every job passed)") is a completed success on the PR's head commit;
  (b) main's check-site runs, counting only a push to main or a manual run on main (a pull request run or the
      Monday schedule is not "main's full run"): none is queued or in progress, and the newest completed one is
      a success, AND every job of that run has finished and none failed (a run can read "completed success" in the
      list while GitHub's job records are still open, so the run's own status is not trusted alone): jobs are read
      from actions/runs/<id>/jobs, all pages, latest attempt; success, skipped and neutral pass; a job queued or in
      progress means "not finished" (--wait polls for it, and --wait is the ceiling: a job record GitHub never closes
      ends in a refusal naming the job, not a hang); failure, cancelled, timed_out, action_required or anything else is
      red; no jobs at all, or a jobs call that fails, is a refusal. A run still going counts as NOT green; nothing
      assumes it.

--override "<ruling>" waives (b) and only (b): it writes the ruling, with the run and any unfinished or red jobs it
overrode, as a comment on the
PR first, then merges. An empty ruling is refused. (a) is never waived. The merge is a squash pinned to the head
commit that (a) judged, so a later push cannot ride in on an earlier green. GitHub deletes the head branch itself
(canon §7.8.2). On success it prints main's head and the run it judged. end-task.py runs after, unchanged.
"""
import argparse
import json
import subprocess
import sys
import time

GATE = "Gate (every job passed)"
WORKFLOW = "check-site.yml"
MAIN_EVENTS = ("push", "workflow_dispatch")
POLL_S = 30
JOB_OK = ("success", "skipped", "neutral")


class Refused(Exception):
    pass


def gh_api(method, path, **fields):
    cmd = ["gh", "api", "-X", method, path]
    for k, v in fields.items():
        cmd += ["-f", "%s=%s" % (k, v)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        raise Refused("gh api %s %s failed: %s" % (method, path, (p.stderr or p.stdout).strip()[:300]))
    return json.loads(p.stdout) if p.stdout.strip() else {}


R = "repos/{owner}/{repo}"   # gh fills these from the current checkout


def check_gate(api, pr):
    """(a) -> (ok, why). The Gate on the head commit; the newest Gate check wins (a rerun replaces a failure)."""
    sha = pr["head"]["sha"]
    runs = api("GET", "%s/commits/%s/check-runs?per_page=100" % (R, sha)).get("check_runs", [])
    gates = sorted((c for c in runs if c["name"] == GATE), key=lambda c: c["id"])
    if not gates:
        return False, "no %r check on head %s yet" % (GATE, sha[:7])
    g = gates[-1]
    if g["status"] != "completed":
        return False, "the Gate on head %s is %s, not finished" % (sha[:7], g["status"])
    if g["conclusion"] != "success":
        return False, "the Gate on head %s is %s" % (sha[:7], g["conclusion"])
    return True, "Gate green on head %s" % sha[:7]


def main_runs(api):
    d = api("GET", "%s/actions/workflows/%s/runs?per_page=50" % (R, WORKFLOW))
    runs = [r for r in d.get("workflow_runs", []) if r["event"] in MAIN_EVENTS and r["head_branch"] == "main"]
    return sorted(runs, key=lambda r: r["created_at"], reverse=True)


def run_jobs(api, run_id):
    """Every job of the run's latest attempt, all pages. Raises Refused if the call fails."""
    jobs, page, total = [], 1, None
    while page <= 20:
        d = api("GET", "%s/actions/runs/%s/jobs?per_page=100&page=%d" % (R, run_id, page))
        got = d.get("jobs", [])
        jobs += got
        total = d.get("total_count", len(jobs)) if total is None else total
        if not got or len(jobs) >= total:
            break
        page += 1
    return jobs


def _named(jobs):
    names = ["%s (%s)" % (j["name"], j["status"] if j["status"] != "completed" else j["conclusion"]) for j in jobs]
    return ", ".join(names[:5]) + (" and %d more" % (len(names) - 5) if len(names) > 5 else "")


def check_main(api):
    """(b) -> (ok, why, run). Never guesses: an unfinished run or job, or no run at all, is not green."""
    runs = main_runs(api)
    if not runs:
        return False, "no check-site run on main (push or manual) in the last 50 runs", None
    going = [r for r in runs if r["status"] != "completed"]
    if going:
        r = going[0]
        return False, "main's run %s (%s, %s) is %s, not finished" % (r["id"], r["event"], r["head_sha"][:7], r["status"]), r
    r = runs[0]
    if r["conclusion"] != "success":
        return False, "main's last full run %s (%s, %s, finished %s) is %s" % (
            r["id"], r["event"], r["head_sha"][:7], r["updated_at"], r["conclusion"]), r
    try:
        jobs = run_jobs(api, r["id"])
    except Refused as e:
        return False, "main's run %s reads success but its jobs could not be read (%s)" % (r["id"], e), r
    if not jobs:
        return False, "main's run %s reads success but lists no jobs" % r["id"], r
    open_ = [j for j in jobs if j["status"] != "completed"]
    if open_:
        return False, ("main's run %s reads completed but %d of %d jobs are not finished: %s "
                       "(GitHub can leave a job record open; --wait ends the wait, then rerun or --override)"
                       % (r["id"], len(open_), len(jobs), _named(open_))), r
    bad = [j for j in jobs if j["conclusion"] not in JOB_OK]
    if bad:
        return False, "main's run %s reads success but %d of %d jobs did not pass: %s" % (r["id"], len(bad), len(jobs), _named(bad)), r
    return True, "main's last full run %s is green: %d jobs, all finished, none failed (%s, finished %s)" % (
        r["id"], len(jobs), r["head_sha"][:7], r["updated_at"]), r


def guard(api, number, override=None, wait=0, main_check=check_main, sleep=time.sleep, log=print):
    """Merge or raise Refused. Returns (merge_response, judged_run)."""
    if override is not None and not override.strip():
        raise Refused("--override needs Jon's ruling and its date as text")
    deadline = time.time() + wait
    while True:
        pr = api("GET", "%s/pulls/%d" % (R, number))
        if pr["state"] != "open" or pr.get("merged"):
            raise Refused("PR #%d is not open (%s)" % (number, "merged" if pr.get("merged") else pr["state"]))
        if pr["base"]["ref"] != "main":
            raise Refused("PR #%d targets %s, not main" % (number, pr["base"]["ref"]))
        ok_a, why_a = check_gate(api, pr)
        ok_b, why_b, run = main_check(api) if override is None else (True, "waived by --override", None)
        if ok_a and ok_b:
            break
        # a thing that is merely unfinished may be waited for; a red one never is
        unfinished = ("not finished" in why_a or "no %r" % GATE in why_a or "not finished" in why_b)
        red = (not ok_a and not unfinished) or (not ok_b and "not finished" not in why_b)
        if red or time.time() >= deadline:
            raise Refused("; ".join(w for ok, w in ((ok_a, why_a), (ok_b, why_b)) if not ok))
        log("waiting: " + "; ".join(w for ok, w in ((ok_a, why_a), (ok_b, why_b)) if not ok))
        sleep(POLL_S)
    if override is not None:
        _, why, run = main_check(api)
        api("POST", "%s/issues/%d/comments" % (R, number),
            body="Merge guard override (scripts/merge-pr.py), main's rule waived on this ruling:\n\n> %s\n\nWhat it overrode: %s.\n"
                 "The Gate was green on head %s." % (override.strip(), why, pr["head"]["sha"][:7]))
    res = api("PUT", "%s/pulls/%d/merge" % (R, number), merge_method="squash", sha=pr["head"]["sha"],
              commit_title="%s (#%d)" % (pr["title"], number), commit_message=pr.get("body") or "")
    if not res.get("merged"):
        raise Refused("GitHub did not merge #%d: %s" % (number, res.get("message")))
    return res, run


# ---------------------------------------------------------------------------------------------------------------
# Selftest: recorded API shapes (run ids, times and conclusions are 21 Oct 2026's: #473 merged at 07:28:30Z while
# main's newest finished run, 39559284220, was a failure).

def _run(i, event, status, concl, created, branch="main", sha="a" * 40):
    return {"id": i, "event": event, "head_branch": branch, "status": status, "conclusion": concl,
            "created_at": created, "updated_at": created, "head_sha": sha}


HEAD = "0ba5dc1be039d30de01f012835b5be7a09dd4a01"
PR_OPEN = {"state": "open", "merged": False, "base": {"ref": "main"}, "head": {"sha": HEAD},
           "title": "Handover: MATHTEXT-NOWRAP and CTS-SEVEN done", "body": "Docs only."}
GATE_OK = {"check_runs": [{"id": 9, "name": GATE, "status": "completed", "conclusion": "success"},
                          {"id": 3, "name": "Plan", "status": "completed", "conclusion": "success"}]}
GATE_RED = {"check_runs": [{"id": 9, "name": GATE, "status": "completed", "conclusion": "failure"}]}
GATE_RERUN = {"check_runs": [{"id": 7, "name": GATE, "status": "completed", "conclusion": "failure"},
                             {"id": 9, "name": GATE, "status": "completed", "conclusion": "success"}]}
GATE_GOING = {"check_runs": [{"id": 9, "name": GATE, "status": "in_progress", "conclusion": None}]}
GREEN = [_run(39559008796, "push", "completed", "success", "2026-10-21T07:00:23Z"),
         _run(39558280166, "pull_request", "completed", "success", "2026-10-21T06:53:38Z", "claude/x")]
RED = [_run(39559284220, "push", "completed", "failure", "2026-10-21T07:02:47Z")] + GREEN
GOING = [_run(39559284220, "push", "in_progress", None, "2026-10-21T07:02:47Z")] + GREEN
CANCELLED = [_run(39559284220, "push", "completed", "cancelled", "2026-10-21T07:02:47Z")] + GREEN
# a red pull-request run and a red Monday run are not main's full run
NOISE = [_run(39561331795, "pull_request", "completed", "failure", "2026-10-21T07:20:51Z", "handover-two-fixes"),
         _run(39600000000, "schedule", "completed", "failure", "2026-10-21T07:25:00Z")] + GREEN


def _job(name, status="completed", concl="success"):
    return {"name": name, "status": status, "conclusion": concl}


JOBS_OK = [_job("Plan"), _job("Tier 1 (page load) shard 1/4"), _job("Content verifiers 1"), _job(GATE)]
JOBS_SKIPPED = JOBS_OK + [_job("Answer locks 3", concl="skipped"), _job("Leaderboard", concl="neutral")]
JOBS_OPEN = JOBS_OK + [_job("Content verifiers 10", "in_progress", None), _job("Tier 4 layer A", "queued", None)]
JOBS_RED = JOBS_OK + [_job("Content verifiers 4", concl="failure")]


class Fake:
    def __init__(self, pr=PR_OPEN, gate=GATE_OK, runs=GREEN, script=None, jobs=None, jobs_script=None, jobs_error=False):
        self.pr, self.gate, self.runs, self.calls = pr, gate, runs, []
        self.script = script or []   # successive run lists, for the wait case
        # jobs: a list of pages (each a list of jobs); jobs_script: successive such lists, one per poll
        self.jobs = jobs if jobs is not None else [JOBS_OK]
        self.jobs_script, self.jobs_error = jobs_script or [], jobs_error

    def __call__(self, method, path, **fields):
        self.calls.append((method, path, fields))
        if method == "GET" and "/check-runs" in path:
            return self.gate
        if method == "GET" and "/actions/runs/" in path and "/jobs" in path:
            if self.jobs_error:
                raise Refused("gh api GET %s failed: HTTP 403" % path)
            page = int(path.rsplit("page=", 1)[1])
            if self.jobs_script and page == 1:
                self.jobs = self.jobs_script.pop(0) if len(self.jobs_script) > 1 else self.jobs_script[0]
            pages = self.jobs
            return {"total_count": sum(len(x) for x in pages), "jobs": pages[page - 1] if page <= len(pages) else []}
        if method == "GET" and "/actions/workflows/" in path:
            runs = self.script.pop(0) if len(self.script) > 1 else (self.script[0] if self.script else self.runs)
            return {"workflow_runs": runs}
        if method == "GET" and "/pulls/" in path:
            return self.pr
        if method == "POST" and path.endswith("/comments"):
            return {"id": 1}
        if method == "PUT" and path.endswith("/merge"):
            return {"merged": True, "sha": "m" * 40}
        raise AssertionError("unexpected call %s %s" % (method, path))

    def merged(self):
        return [c for c in self.calls if c[0] == "PUT"]

    def comments(self):
        return [c for c in self.calls if c[0] == "POST"]


def _try(fake, **kw):
    try:
        guard(fake, 473, sleep=lambda s: None, log=lambda *a: None, **kw)
        return None
    except Refused as e:
        return str(e)


def cases(main_check=check_main):
    """-> list of (name, ok, detail). Every case states what must and must not happen."""
    out = []

    def case(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    f = Fake()
    err = _try(f, main_check=main_check)
    m = f.merged()
    case("green Gate + green main merges (squash, pinned to the head)",
         err is None and len(m) == 1 and m[0][2]["merge_method"] == "squash" and m[0][2]["sha"] == HEAD
         and m[0][2]["commit_title"].endswith("(#473)") and not f.comments(), err or "")

    f = Fake(runs=RED)
    err = _try(f, main_check=main_check)
    case("red main refuses, and nothing is merged or commented", err and "failure" in err and "39559284220" in err
         and not f.merged() and not f.comments(), err or "MERGED")

    f = Fake(runs=GOING)
    err = _try(f, main_check=main_check)
    case("main in progress refuses (never assumed green)", err and "in_progress" in err and not f.merged(), err or "MERGED")

    f = Fake(runs=CANCELLED)
    err = _try(f, main_check=main_check)
    case("main cancelled refuses", err and "cancelled" in err and not f.merged(), err or "MERGED")

    f = Fake(runs=NOISE)
    err = _try(f, main_check=main_check)
    case("a red PR run and a red scheduled run are not main's full run", err is None and len(f.merged()) == 1, err or "")

    f = Fake(runs=[])
    err = _try(f, main_check=main_check)
    case("no main run at all refuses", err and not f.merged(), err or "MERGED")

    f = Fake(gate=GATE_RED)
    err = _try(f, main_check=main_check)
    case("red Gate refuses", err and "Gate" in err and not f.merged(), err or "MERGED")

    f = Fake(gate=GATE_RED, runs=RED)
    err = _try(f, main_check=main_check, override="Jon, 21 Oct 2026: merge it")
    case("red Gate refuses even with --override (no comment, no merge)", err and "Gate" in err and not f.merged() and not f.comments(), err or "MERGED")

    f = Fake(gate=GATE_GOING)
    err = _try(f, main_check=main_check)
    case("Gate still running refuses", err and not f.merged(), err or "MERGED")

    f = Fake(gate=GATE_RERUN)
    err = _try(f, main_check=main_check)
    case("a rerun Gate that passed counts (newest Gate check wins)", err is None and len(f.merged()) == 1, err or "")

    f = Fake(runs=RED)
    err = _try(f, main_check=main_check, override="Jon, 21 Oct 2026: timings job only")
    c = f.comments()
    case("--override on red main writes the ruling as a PR comment, then merges",
         err is None and len(c) == 1 and "Jon, 21 Oct 2026: timings job only" in c[0][2]["body"] and "39559284220" in c[0][2]["body"]
         and len(f.merged()) == 1 and f.calls.index(c[0]) < f.calls.index(f.merged()[0]), err or "")

    f = Fake(runs=RED)
    err = _try(f, main_check=main_check, override="   ")
    case("an empty --override ruling is refused", err and not f.merged() and not f.comments(), err or "MERGED")

    f = Fake(pr=dict(PR_OPEN, state="closed", merged=True))
    err = _try(f, main_check=main_check)
    case("an already-merged PR is refused", err and not f.merged(), err or "MERGED")

    f = Fake(pr=dict(PR_OPEN, base={"ref": "other"}))
    err = _try(f, main_check=main_check)
    case("a PR not aimed at main is refused", err and not f.merged(), err or "MERGED")

    f = Fake(script=[GOING, GREEN])
    err = _try(f, main_check=main_check, wait=120)
    case("--wait: main in progress, then green, merges", err is None and len(f.merged()) == 1, err or "")

    f = Fake(script=[GOING])
    err = _try(f, main_check=main_check, wait=0)
    case("--wait 0 on a run in progress refuses at once", err and not f.merged(), err or "MERGED")

    f = Fake(script=[RED])
    err = _try(f, main_check=main_check, wait=120)
    case("--wait never waits out a red main", err and "failure" in err and not f.merged(), err or "MERGED")
    # ---- the jobs of main's newest run (22 Oct 2026: a run's own status is not trusted alone) ----
    f = Fake(jobs=[JOBS_OPEN])
    err = _try(f, main_check=main_check)
    case("(i) run completed/success but jobs queued or in progress refuses as not finished, naming them",
         err and "not finished" in err and "Content verifiers 10 (in_progress)" in err and "Tier 4 layer A (queued)" in err
         and not f.merged(), err or "MERGED")

    f = Fake(jobs_script=[[JOBS_OPEN], [JOBS_OK]])
    err = _try(f, main_check=main_check, wait=120)
    case("(i) --wait: jobs still open, then done, merges", err is None and len(f.merged()) == 1, err or "")

    f = Fake(jobs=[JOBS_OPEN])
    err = _try(f, main_check=main_check, wait=0)
    case("(i) --wait 0 on open jobs refuses at once (a job record never closed ends the wait in a refusal, not a hang)",
         err and "not finished" in err and not f.merged(), err or "MERGED")

    f = Fake(jobs_script=[[JOBS_RED]])
    err = _try(f, main_check=main_check, wait=120)
    case("(ii) run completed/success with one job failed refuses red, and --wait does not wait it out",
         err and "Content verifiers 4 (failure)" in err and "not finished" not in err and not f.merged(), err or "MERGED")

    for concl in ("cancelled", "timed_out", "action_required"):
        f = Fake(jobs=[JOBS_OK + [_job("Z", concl=concl)]])
        err = _try(f, main_check=main_check)
        case("(ii) a %s job refuses" % concl, err and concl in err and not f.merged(), err or "MERGED")

    f = Fake(jobs=[JOBS_SKIPPED])
    err = _try(f, main_check=main_check)
    case("(iii) skipped and neutral jobs beside successes pass", err is None and len(f.merged()) == 1, err or "")

    f = Fake(jobs=[[]])
    err = _try(f, main_check=main_check)
    case("(iv) an empty jobs list refuses", err and "no jobs" in err and not f.merged(), err or "MERGED")

    f = Fake(jobs_error=True)
    err = _try(f, main_check=main_check)
    case("(iv) a jobs call that errors refuses (never assumed green)", err and "could not be read" in err and not f.merged(), err or "MERGED")

    f = Fake(jobs=[JOBS_OK[:2], JOBS_OK[2:] + [_job("Page two", concl="failure")]])
    err = _try(f, main_check=main_check)
    case("(v) jobs over two pages are both read (a failure on page 2 is seen)", err and "Page two (failure)" in err and not f.merged(), err or "MERGED")

    f = Fake(jobs=[JOBS_OK[:2], JOBS_OK[2:]])
    err = _try(f, main_check=main_check)
    jobs_calls = [c for c in f.calls if "/jobs" in c[1]]
    case("(v) two pages, all green, merges having read both pages", err is None and len(f.merged()) == 1 and len(jobs_calls) >= 2, err or "")

    f = Fake(jobs=[JOBS_OPEN])
    err = _try(f, main_check=main_check, override="Jon, 22 Oct 2026: job record stuck")
    c = f.comments()
    case("--override on open jobs waives (b) only: the comment names the jobs, then it merges",
         err is None and len(c) == 1 and "Content verifiers 10 (in_progress)" in c[0][2]["body"] and len(f.merged()) == 1, err or "")

    f = Fake(jobs=[JOBS_OPEN], gate=GATE_RED)
    err = _try(f, main_check=main_check, override="Jon, 22 Oct 2026: x")
    case("--override never waives a red Gate (open jobs)", err and "Gate" in err and not f.merged() and not f.comments(), err or "MERGED")
    return out


def check_main_run_only(api):
    """The check_main() before 22 Oct 2026, kept as the planted fault: the run's own status and conclusion, no jobs."""
    runs = main_runs(api)
    if not runs:
        return False, "no check-site run on main", None
    going = [r for r in runs if r["status"] != "completed"]
    if going:
        return False, "main's run %s is %s, not finished" % (going[0]["id"], going[0]["status"]), going[0]
    r = runs[0]
    if r["conclusion"] != "success":
        return False, "main's last full run %s is %s" % (r["id"], r["conclusion"]), r
    return True, "main's last full run %s is green" % r["id"], r


def selftest():
    bad = 0
    for name, ok, detail in cases():
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "   -> " + detail))
        bad += not ok
    # the cases must be sensitive: with the red-main check removed, they have to notice
    mutant = [n for n, ok, _ in cases(main_check=lambda api: (True, "mutant: always green", None)) if not ok]
    sens = {"red main refuses, and nothing is merged or commented", "main in progress refuses (never assumed green)",
            "main cancelled refuses", "no main run at all refuses"}
    missed = sorted(sens - set(mutant))
    print("  %s  removing the red-main check fails %d of %d main cases%s" % (
        "PASS" if not missed else "FAIL", len(sens) - len(missed), len(sens), "" if not missed else ": still passing " + str(missed)))
    bad += bool(missed)
    # ... and the jobs cases must catch the run-only judge (cases i, ii and iv)
    old = [n for n, ok, _ in cases(main_check=check_main_run_only) if not ok]
    allc = [n for n, _, _ in cases()]
    for tag in ("(i)", "(ii)", "(iv)"):
        caught = [n for n in old if n.startswith(tag)]
        total = [n for n in allc if n.startswith(tag)]
        print("  %s  planting the run-only check_main() fails %d of %d %s cases" % (
            "PASS" if caught else "FAIL", len(caught), len(total), tag))
        bad += not caught
    print("%s" % ("selftest FAILED" if bad else "selftest passed"))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("number", nargs="?", type=int)
    ap.add_argument("--override", help="Jon's ruling and its date; waives the main-is-green rule only")
    ap.add_argument("--wait", type=int, default=0, help="seconds to poll while a check is unfinished (default 0: refuse)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.number:
        ap.error("a PR number is required")
    try:
        res, run = guard(gh_api, a.number, a.override, a.wait)
    except Refused as e:
        print("REFUSED #%d: %s" % (a.number, e))
        return 1
    head = gh_api("GET", "%s/git/ref/heads/main" % R)["object"]["sha"]
    judged = ("run %s (%s)" % (run["id"], run["html_url"] if "html_url" in run else run["conclusion"])) if run else "waived by --override"
    print("MERGED #%d (squash, %s). main head %s. Judged: %s." % (a.number, res.get("sha", "")[:7], head[:7], judged))
    print("Now wait for main's run on that commit and report it (CLAUDE.md), then end-task.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
