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
      a success. A run still going counts as NOT green; --wait polls for it, nothing assumes it.

--override "<ruling>" waives (b) and only (b): it writes the ruling, with the run it overrode, as a comment on the
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


def check_main(api):
    """(b) -> (ok, why, run). Never guesses: an unfinished run, or no run at all, is not green."""
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
    return True, "main's last full run %s is green (%s, finished %s)" % (r["id"], r["head_sha"][:7], r["updated_at"]), r


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


class Fake:
    def __init__(self, pr=PR_OPEN, gate=GATE_OK, runs=GREEN, script=None):
        self.pr, self.gate, self.runs, self.calls = pr, gate, runs, []
        self.script = script or []   # successive run lists, for the wait case

    def __call__(self, method, path, **fields):
        self.calls.append((method, path, fields))
        if method == "GET" and "/check-runs" in path:
            return self.gate
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
    return out


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
