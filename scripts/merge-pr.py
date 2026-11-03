#!/usr/bin/env python3
# ci-line: Merge guard (scripts/merge-pr.py: green Gate and green main or no merge; override only for main; recorded API fixtures) | --selftest
"""The one way either lane merges a PR (CLAUDE.md "Neither lane merges while main's last full run is red", canon §7.8.3).

    python scripts/merge-pr.py <number>                      # merge if the guard passes, else refuse (exit 1)
    python scripts/merge-pr.py <number> --wait 600           # while a check is still running, poll up to 600 s, then refuse
    python scripts/merge-pr.py <number> --override "<Jon's ruling and date>"
    python scripts/merge-pr.py <number> --watch --wait 3600  # merge, then watch main's run on the squash commit
    python scripts/merge-pr.py --watch-main [<sha>] [--wait <s>]   # watch main's run on <sha> (default: main's newest merge)
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

  (b') the run judged is main's newest MERGE's own (GATE-FIX, Jon 2 Nov 2026): the newest commit on main that is not a
      bot skip-marker commit (github-actions[bot]'s REGISTER, timings and answer-counts commits) must have its own
      check-site run (push or manual), completed and green as above. A merge with no run is NOT green: #631's squash
      message carried a skip marker, GitHub started no run on main, and the guard went on judging the run before it.
  (c) the squash message it builds has GitHub's skip markers disarmed (GATE-FIX): the PR's title and body become the
      commit's title and message, and a body that quotes "[skip ci]" (#631's did) would stop main's run. Each bracketed
      marker keeps its words in round brackets; "skip-checks: true" loses its colon.

--override "<ruling>" waives (b) and only (b): it writes the ruling, with the run and any unfinished or red jobs it
overrode, as a comment on the
PR first, then merges. An empty ruling is refused. (a) is never waived. The merge is a squash pinned to the head
commit that (a) judged, so a later push cannot ride in on an earlier green. GitHub deletes the head branch itself
(canon §7.8.2). On success it prints main's head and the run it judged. end-task.py runs after, unchanged.

The watch (CLOUD-LEAN, Jon, 3 Nov 2026) is additive and changes nothing above. --watch-main [<sha>] waits up to --wait
seconds for main's check-site run (push or manual) on that commit to finish, read and judged as (b) reads and judges a
run, and prints ONE line, exit 0 for GREEN and 1 for anything else. With no <sha> it watches main's newest merge as
(b') picks it (newest_merge(): the bot's skip-marker commits have no run and are passed over):

    main <sha7> run <id>: GREEN
    main <sha7> run <id>: RED: <failed job names>
    main <sha7>: NOT FINISHED after <n>s
    main <sha7>: NO RUN FOUND

A run or job still going, or one that cannot be read yet, is NOT FINISHED, never green; a red run is never waited out; a
commit with no run is waited for (a new merge's run takes seconds to register), then NO RUN FOUND. A merge given --watch
runs the same watch on its squash commit, prints its line last and exits with its status.
"""
import argparse
import json
import re
import subprocess
import sys
import time

GATE = "Gate (every job passed)"
WORKFLOW = "check-site.yml"
MAIN_EVENTS = ("push", "workflow_dispatch")
POLL_S = 30
JOB_OK = ("success", "skipped", "neutral")
BOT = "github-actions[bot]"
# GitHub's skip markers (docs: "Skipping workflow runs"), matched loosely: case and inner spacing ignored.
SKIP_BRACKETS = re.compile(r"\[\s*(skip\s+ci|ci\s+skip|no\s+ci|skip\s+actions|actions\s+skip)\s*\]", re.I)
SKIP_CHECKS = re.compile(r"(skip-checks)\s*:\s*(true)", re.I)


def has_skip_marker(text):
    return bool(SKIP_BRACKETS.search(text or "") or SKIP_CHECKS.search(text or ""))


def disarm(text):
    """The text with every GitHub skip marker made inert, its words kept: "[skip ci]" -> "(skip ci)",
    "skip-checks: true" -> "skip-checks true"."""
    text = SKIP_BRACKETS.sub(lambda m: "(%s)" % m.group(1), text or "")
    return SKIP_CHECKS.sub(lambda m: "%s %s" % (m.group(1), m.group(2)), text)


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


JOBS_PER_PAGE = 50   # GitHub answered 502 at 100 a page for a re-run main run of 71 jobs, every time (27 Oct 2026); 50 read it


def run_jobs(api, run_id):
    """Every job of the run's latest attempt, all pages. Raises Refused if the call fails."""
    jobs, page, total = [], 1, None
    while page <= 40:
        d = api("GET", "%s/actions/runs/%s/jobs?per_page=%d&page=%d" % (R, run_id, JOBS_PER_PAGE, page))
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


def newest_merge(api, runs=None):
    """(sha, why): the newest commit on main that is not a bot skip-marker commit, or (None, why) if none can be read."""
    try:
        commits = api("GET", "%s/commits?sha=main&per_page=50" % R)
    except Refused as e:
        return None, "main's commits could not be read (%s)" % e
    for c in commits if isinstance(commits, list) else []:
        login = (c.get("author") or {}).get("login") or ""
        name = ((c.get("commit") or {}).get("author") or {}).get("name") or ""
        if BOT in (login, name) and has_skip_marker((c.get("commit") or {}).get("message")):
            continue
        return c["sha"], None
    return None, "no commit on main in the last 50 that is not a bot skip-marker commit"


def check_main(api, merge_of=newest_merge):
    """(b) -> (ok, why, run). Never guesses: an unfinished run or job, or no run at all, is not green; nor is a merge
    with no run of its own (b')."""
    runs = main_runs(api)
    if not runs:
        return False, "no check-site run on main (push or manual) in the last 50 runs", None
    going = [r for r in runs if r["status"] != "completed"]
    if going:
        r = going[0]
        return False, "main's run %s (%s, %s) is %s, not finished" % (r["id"], r["event"], r["head_sha"][:7], r["status"]), r
    sha, why = merge_of(api, runs)
    if sha is None:
        return False, why, None
    own = [r for r in runs if r["head_sha"] == sha]
    if not own:
        return False, ("main's newest merge %s has no check-site run of its own (push or manual): not green. A skip marker "
                       "in its message stops the push run; start one by hand (workflow_dispatch on main)" % sha[:7]), runs[0]
    r = own[0]
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


def guard(api, number, override=None, wait=0, main_check=check_main, sleep=time.sleep, log=print, clean=disarm):
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
              commit_title=clean("%s (#%d)" % (pr["title"], number)), commit_message=clean(pr.get("body") or ""))
    if not res.get("merged"):
        raise Refused("GitHub did not merge #%d: %s" % (number, res.get("message")))
    return res, run


# ---------------------------------------------------------------------------------------------------------------
# The watch (CLOUD-LEAN, Jon, 3 Nov 2026): main's run on one commit, after a merge, in one line. It reads through (b)'s
# own reader, main_runs() and run_jobs(), and judges by JOB_OK; the guard above is not changed by it.

def watch_state(api, sha):
    """-> (state, run, detail): "green", "red", "going" (unfinished, or not readable yet) or "none" (main has no check-site
    run, push or manual, on this commit). Green as (b) means it: the run completed success, and its latest attempt has at
    least one job, every one finished, each in JOB_OK. A failed job, or a run that completed anything but success, is red."""
    try:
        own = [r for r in main_runs(api) if r["head_sha"].startswith(sha)]
    except Refused as e:
        return "going", None, "main's runs could not be read (%s)" % e
    if not own:
        return "none", None, "no check-site run on main for this commit yet"
    r = own[0]
    if r["status"] != "completed":
        return "going", r, "run %s is %s" % (r["id"], r["status"])
    try:
        jobs = run_jobs(api, r["id"])
    except Refused as e:
        if r["conclusion"] != "success":
            return "red", r, "run %s (its jobs could not be read)" % r["conclusion"]
        return "going", r, "run %s's jobs could not be read (%s)" % (r["id"], e)
    failed = [j["name"] for j in jobs if j["status"] == "completed" and j["conclusion"] not in JOB_OK]
    if failed:
        return "red", r, ", ".join(failed[:8]) + (" and %d more" % (len(failed) - 8) if len(failed) > 8 else "")
    if r["conclusion"] != "success":
        return "red", r, "run %s" % r["conclusion"]
    open_ = [j for j in jobs if j["status"] != "completed"]
    if not jobs or open_:
        return "going", r, ("run %s lists no jobs yet" % r["id"]) if not jobs else (
            "run %s: %d of %d jobs not finished: %s" % (r["id"], len(open_), len(jobs), _named(open_)))
    return "green", r, "%d jobs, all finished, none failed" % len(jobs)


def watch_main(api, sha, wait=0, state=watch_state, sleep=time.sleep, clock=time.time, log=None):
    """-> (exit code, the one line). Polls every POLL_S while the run is missing or unfinished, up to `wait` seconds."""
    start = clock()
    while True:
        st, r, detail = state(api, sha)
        if st == "green":
            return 0, "main %s run %s: GREEN" % (sha[:7], r["id"])
        if st == "red":
            return 1, "main %s run %s: RED: %s" % (sha[:7], r["id"], detail)
        elapsed = clock() - start
        if elapsed >= wait:
            if st == "none":
                return 1, "main %s: NO RUN FOUND" % sha[:7]
            return 1, "main %s: NOT FINISHED after %ds" % (sha[:7], int(round(elapsed)))
        if log:
            log("waiting: main %s: %s" % (sha[:7], detail))
        sleep(min(POLL_S, wait - elapsed))


def merge_and_report(api, number, override=None, wait=0, watch=False, out=print, note=None, sleep=time.sleep,
                     clock=time.time, state=watch_state):
    """The merge command: guard() unchanged, then its report; with `watch`, the watch on the squash commit last."""
    try:
        res, run = guard(api, number, override, wait)
    except Refused as e:
        out("REFUSED #%d: %s" % (number, e))
        return 1
    head = api("GET", "%s/git/ref/heads/main" % R)["object"]["sha"]
    judged = ("run %s (%s)" % (run["id"], run["html_url"] if "html_url" in run else run["conclusion"])) if run else "waived by --override"
    out("MERGED #%d (squash, %s). main head %s. Judged: %s." % (number, res.get("sha", "")[:7], head[:7], judged))
    if not watch:
        out("Now wait for main's run on that commit and report it (CLAUDE.md), then end-task.py.")
        return 0
    code, line = watch_main(api, res.get("sha") or head, wait, state=state, sleep=sleep, clock=clock, log=note)
    out(line)
    return code


def watch_cmd(api, sha="", wait=0, pick=newest_merge, **kw):
    """--watch-main -> (exit code, line, to_stderr). With no sha, the commit is main's newest merge as (b') picks it,
    newest_merge(): the bot's skip-marker commits (timings, register, answer counts) have no run and are passed over
    (Amendment 2, Jon 3 Nov 2026). If main's commits cannot be read, exit 2 and say why on stderr."""
    if not sha:
        sha, why = pick(api)
        if sha is None:
            return 2, "--watch-main: %s" % why, True
    code, line = watch_main(api, sha, wait, **kw)
    return code, line, False


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


def _commit(sha, msg, who="Vector52F"):
    return {"sha": sha, "author": {"login": who}, "commit": {"author": {"name": who}, "message": msg}}


# main's commits, newest first: the merge the GREEN runs were for ("a" * 40)
COMMITS = [_commit("a" * 40, "Handover: MATHTEXT-NOWRAP and CTS-SEVEN done (#473)")]
BOT_ON_TOP = [_commit("c" * 40, "Record CI timings and repack (run 41428467865) [skip ci]", BOT),
              _commit("d" * 40, "Record the answer counts [skip ci]", BOT)] + COMMITS
# 2 Nov 2026: #631's merge (34bac35) carried "[skip ci]" from its body; no run started; the newest run was the merge before
UNRUN_MERGE = [_commit("b" * 40, "GATE-WARN-THEN-ENFORCE step 5 ... (#631)\n\n... commits what moved ([skip ci]) ...")] + BOT_ON_TOP
PERSON_MARKED = [_commit("e" * 40, "Quick fix [skip ci]")] + COMMITS
MARKED_PR = dict(PR_OPEN, title="Gate [skip ci] notes",
                 body="It commits [skip ci]; also [CI Skip], [ no  ci ], [skip actions], [Actions Skip].\n\nskip-checks: true")

JOBS_OK = [_job("Plan"), _job("Tier 1 (page load) shard 1/4"), _job("Content verifiers 1"), _job(GATE)]
JOBS_SKIPPED = JOBS_OK + [_job("Answer locks 3", concl="skipped"), _job("Leaderboard", concl="neutral")]
JOBS_OPEN = JOBS_OK + [_job("Content verifiers 10", "in_progress", None), _job("Tier 4 layer A", "queued", None)]
JOBS_RED = JOBS_OK + [_job("Content verifiers 4", concl="failure")]


class Fake:
    def __init__(self, pr=PR_OPEN, gate=GATE_OK, runs=GREEN, script=None, jobs=None, jobs_script=None, jobs_error=False,
                 max_per_page=None, commits=None, commits_error=False):
        self.pr, self.gate, self.runs, self.calls = pr, gate, runs, []
        self.commits = COMMITS if commits is None else commits   # main's commits, newest first (GATE-FIX b')
        self.commits_error = commits_error
        self.max_per_page = max_per_page   # GitHub's 502 for a page too large (27 Oct 2026)
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
            per = int(path.split("per_page=", 1)[1].split("&", 1)[0])
            if self.max_per_page and per > self.max_per_page:
                raise Refused("gh api GET %s failed: gh: Server Error (HTTP 502)" % path)
            page = int(path.rsplit("page=", 1)[1])
            if self.jobs_script and page == 1:
                self.jobs = self.jobs_script.pop(0) if len(self.jobs_script) > 1 else self.jobs_script[0]
            pages = self.jobs
            return {"total_count": sum(len(x) for x in pages), "jobs": pages[page - 1] if page <= len(pages) else []}
        if method == "GET" and "/commits?sha=main" in path:
            if self.commits_error:
                raise Refused("gh api GET %s failed: HTTP 502" % path)
            return self.commits
        if method == "GET" and "/actions/workflows/" in path:
            runs = self.script.pop(0) if len(self.script) > 1 else (self.script[0] if self.script else self.runs)
            return {"workflow_runs": runs}
        if method == "GET" and "/pulls/" in path:
            return self.pr
        if method == "POST" and path.endswith("/comments"):
            return {"id": 1}
        if method == "PUT" and path.endswith("/merge"):
            return {"merged": True, "sha": "m" * 40}
        if method == "GET" and path.endswith("/git/ref/heads/main"):
            return {"object": {"sha": "m" * 40}}
        raise AssertionError("unexpected call %s %s" % (method, path))

    def merged(self):
        return [c for c in self.calls if c[0] == "PUT"]

    def comments(self):
        return [c for c in self.calls if c[0] == "POST"]


def _try_one(fake, **kw):
    try:
        guard(fake, 473, sleep=lambda s: None, log=lambda *a: None, **kw)
        return None
    except Refused as e:
        return str(e)


def cases(main_check=check_main, clean=disarm):
    """-> list of (name, ok, detail). Every case states what must and must not happen."""
    out = []

    def _try(fake, **kw):
        return _try_one(fake, clean=clean, **kw)

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

    f = Fake(jobs=[JOBS_OK], max_per_page=50)
    err = _try(f, main_check=main_check)
    case("(v) jobs read 50 a page: a main run GitHub cannot list 100 a page (502, 27 Oct 2026) is read and merges",
         err is None and len(f.merged()) == 1, err or "")

    f = Fake(jobs=[JOBS_OPEN])
    err = _try(f, main_check=main_check, override="Jon, 22 Oct 2026: job record stuck")
    c = f.comments()
    case("--override on open jobs waives (b) only: the comment names the jobs, then it merges",
         err is None and len(c) == 1 and "Content verifiers 10 (in_progress)" in c[0][2]["body"] and len(f.merged()) == 1, err or "")

    f = Fake(jobs=[JOBS_OPEN], gate=GATE_RED)
    err = _try(f, main_check=main_check, override="Jon, 22 Oct 2026: x")
    case("--override never waives a red Gate (open jobs)", err and "Gate" in err and not f.merged() and not f.comments(), err or "MERGED")
    # ---- GATE-FIX (Jon, 2 Nov 2026) ----
    f = Fake(commits=UNRUN_MERGE)
    err = _try(f, main_check=main_check)
    case("(b') a merge with no run of its own refuses, though the run before it is green (#631, 34bac35)",
         err and "no check-site run of its own" in err and "bbbbbbb" in err and not f.merged(), err or "MERGED")

    f = Fake(commits=BOT_ON_TOP)
    err = _try(f, main_check=main_check)
    case("(b') bot skip-marker commits on top of a green merge: the merge's run is judged, and it merges",
         err is None and len(f.merged()) == 1, err or "")

    f = Fake(commits=PERSON_MARKED)
    err = _try(f, main_check=main_check)
    case("(b') a person's commit with a skip marker is not passed over as a bot commit: no run, refused",
         err and "eeeeeee" in err and not f.merged(), err or "MERGED")

    f = Fake(commits_error=True)
    err = _try(f, main_check=main_check)
    case("(b') main's commits unreadable refuses (never assumed green)", err and "could not be read" in err and not f.merged(),
         err or "MERGED")

    f = Fake(pr=MARKED_PR)
    err = _try(f, main_check=main_check)
    m = f.merged()
    put = m[0][2] if m else {}
    case("(a) every skip marker in the PR's title and body is disarmed in the squash title and message, its words kept",
         err is None and len(m) == 1 and not has_skip_marker(put.get("commit_title")) and not has_skip_marker(put.get("commit_message"))
         and "(skip ci)" in put.get("commit_message", "") and "(CI Skip)" in put.get("commit_message", "")
         and "skip-checks true" in put.get("commit_message", "") and put.get("commit_title", "").endswith("(#473)"),
         err or repr(put.get("commit_message")))
    return out


# ---- the watch (CLOUD-LEAN): main's run on one commit. W is the watched commit; GREEN's runs are on another (a * 40). ----
W = "f" * 40
SQUASH = "m" * 40   # Fake's merge answers with this squash commit


def _wrun(status, concl, sha=W, event="push", branch="main"):
    return _run(41615387944, event, status, concl, "2026-11-03T09:40:00Z", branch, sha)


W_GREEN = [_wrun("completed", "success")] + GREEN
W_GOING = [_wrun("in_progress", None)] + GREEN
W_RED = [_wrun("completed", "failure")] + GREEN
W_CANCELLED = [_wrun("completed", "cancelled")] + GREEN
W_NONE = GREEN                                                                   # main has runs, none on W
W_PR_ONLY = [_wrun("completed", "success", event="pull_request", branch="claude/x")] + GREEN   # not main's run
M_GREEN = [_wrun("completed", "success", sha=SQUASH)] + GREEN
M_RED = [_wrun("completed", "failure", sha=SQUASH)] + GREEN


class Clock:
    """A clock that moves only when the code under test sleeps, so a 3600 s wait takes no time."""
    def __init__(self):
        self.t, self.slept = 0.0, 0

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.t += s
        self.slept += 1


def head_literally(api):
    """The planted default (the spec before Amendment 2): main's head as it is, a bot skip-marker commit included.
    Errors are handled as newest_merge() handles them, so only the choice of commit differs."""
    try:
        commits = api("GET", "%s/commits?sha=main&per_page=50" % R)
    except Refused as e:
        return None, "main's commits could not be read (%s)" % e
    return commits[0]["sha"], None


def watch_cases(state=watch_state, pick=newest_merge):
    """-> list of (name, ok, detail): the four outcomes, the waits, the default commit, and merge --watch."""
    out = []

    def case(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    def watch(fake, wait=0, sha=W):
        c = Clock()
        code, line = watch_main(fake, sha, wait, state=state, sleep=c.sleep, clock=c)
        return code, line, c

    code, line, _ = watch(Fake(runs=W_GREEN, jobs=[JOBS_SKIPPED]))
    case("[watch] GREEN: run completed success, every job finished in success/skipped/neutral, exit 0",
         code == 0 and line == "main fffffff run 41615387944: GREEN", "%s %s" % (code, line))

    code, line, c = watch(Fake(script=[W_NONE, W_GOING, W_GREEN]), wait=3600)
    case("[watch] GREEN after waiting: no run registered yet, then running, then green (a fresh squash commit)",
         code == 0 and line.endswith(": GREEN") and c.slept == 2, "%s %s slept %d" % (code, line, c.slept))

    code, line, c = watch(Fake(runs=W_RED, jobs=[JOBS_RED]), wait=3600)
    case("[watch] RED names the failed job, exit 1, and a red run is not waited out",
         code == 1 and line == "main fffffff run 41615387944: RED: Content verifiers 4" and c.slept == 0,
         "%s %s slept %d" % (code, line, c.slept))

    code, line, _ = watch(Fake(runs=W_GREEN, jobs=[JOBS_RED]))
    case("[watch] RED: a run reading success with a failed job is red, not green",
         code == 1 and line.endswith("RED: Content verifiers 4"), "%s %s" % (code, line))

    code, line, _ = watch(Fake(runs=W_CANCELLED, jobs=[JOBS_OK + [_job("Content verifiers 7", concl="cancelled")]]))
    case("[watch] RED: a cancelled run names its cancelled job", code == 1 and line.endswith("RED: Content verifiers 7"),
         "%s %s" % (code, line))

    code, line, _ = watch(Fake(runs=W_CANCELLED, jobs=[JOBS_OK]))
    case("[watch] RED: a run that ended cancelled with no failed job listed still reads red",
         code == 1 and line.endswith("RED: run cancelled"), "%s %s" % (code, line))

    code, line, _ = watch(Fake(runs=W_GOING))
    case("[watch] NOT FINISHED: run in progress, --wait 0, exit 1",
         code == 1 and line == "main fffffff: NOT FINISHED after 0s", "%s %s" % (code, line))

    code, line, c = watch(Fake(runs=W_GREEN, jobs=[JOBS_OPEN]), wait=120)
    case("[watch] NOT FINISHED: run reads success while jobs still run; waits the full --wait, never green",
         code == 1 and line == "main fffffff: NOT FINISHED after 120s" and c.slept == 4, "%s %s slept %d" % (code, line, c.slept))

    code, line, _ = watch(Fake(runs=W_GREEN, jobs_error=True))
    case("[watch] NOT FINISHED: jobs unreadable on a success run (never assumed green)",
         code == 1 and "NOT FINISHED" in line, "%s %s" % (code, line))

    code, line, _ = watch(Fake(runs=W_GREEN, jobs=[[]]))
    case("[watch] NOT FINISHED: a success run that lists no jobs", code == 1 and "NOT FINISHED" in line, "%s %s" % (code, line))

    code, line, _ = watch(Fake(runs=W_NONE))
    case("[watch] NO RUN FOUND: main has runs, none on this commit, exit 1",
         code == 1 and line == "main fffffff: NO RUN FOUND", "%s %s" % (code, line))

    code, line, c = watch(Fake(runs=W_PR_ONLY), wait=60)
    case("[watch] NO RUN FOUND: a pull-request run on the commit is not main's run (after waiting --wait)",
         code == 1 and line == "main fffffff: NO RUN FOUND" and c.slept == 2, "%s %s slept %d" % (code, line, c.slept))

    code, line, _ = watch(Fake(runs=W_GREEN, jobs=[JOBS_OK]), sha="fffffff")
    case("[watch] a short sha (7) is matched", code == 0 and line.endswith(": GREEN"), "%s %s" % (code, line))

    # ---- the default commit (Amendment 2, Jon 3 Nov 2026): main's newest merge, as (b') picks it ----
    def default(fake, wait=0):
        c = Clock()
        return watch_cmd(fake, "", wait, pick=pick, state=state, sleep=c.sleep, clock=c)

    code, line, err = default(Fake(commits=BOT_ON_TOP, runs=GREEN, jobs=[JOBS_OK]))
    case("[watch] default: a head that is a [skip ci] bot commit still reports the merge's run",
         code == 0 and not err and line == "main aaaaaaa run 39559008796: GREEN", "%s %s" % (code, line))

    code, line, err = default(Fake(commits=COMMITS, runs=GREEN, jobs=[JOBS_OK]))
    case("[watch] default: a head that is the merge itself reports its run",
         code == 0 and not err and line == "main aaaaaaa run 39559008796: GREEN", "%s %s" % (code, line))

    code, line, err = default(Fake(commits=UNRUN_MERGE, runs=GREEN, jobs=[JOBS_OK]))
    case("[watch] default: a merge with no run of its own is NO RUN FOUND, never the run before it (#631)",
         code == 1 and line == "main bbbbbbb: NO RUN FOUND", "%s %s" % (code, line))

    code, line, err = default(Fake(commits_error=True, runs=GREEN))
    case("[watch] default: main's commits unreadable exits 2, said on stderr (never a guess)",
         code == 2 and err and "could not be read" in line, "%s %s %s" % (code, err, line))

    for runs, want, label in ((M_GREEN, 0, "GREEN"), (M_RED, 1, "RED: Content verifiers 4")):
        # the guard reads main's green run's jobs first, then the watch reads the squash run's
        f, lines, c = Fake(runs=runs, jobs_script=[[JOBS_OK], [JOBS_RED] if want else [JOBS_OK]]), [], Clock()
        code = merge_and_report(f, 473, wait=600, watch=True, out=lines.append, sleep=c.sleep, clock=c, state=state)
        case("[watch] merge --watch: merged once, then the squash commit's run, %s, is the last line (exit %d)" % (label, want),
             code == want and len(f.merged()) == 1 and lines[0].startswith("MERGED #473")
             and lines[-1] == "main mmmmmmm run 41615387944: %s" % label, "%s %s" % (code, lines))

    f, lines = Fake(runs=M_GREEN), []
    code = merge_and_report(f, 473, out=lines.append)
    case("[watch] merge without --watch prints as before and watches nothing",
         code == 0 and len(lines) == 2 and lines[1].startswith("Now wait for main's run"), "%s %s" % (code, lines))
    return out


def watch_state_run_only(api, sha):
    """The planted fault: trusts the run's own status and conclusion and never reads its jobs, so a run that reads
    completed success while a job still runs is called green."""
    own = [r for r in main_runs(api) if r["head_sha"].startswith(sha)]
    if not own:
        return "none", None, "no run"
    r = own[0]
    if r["status"] != "completed":
        return "going", r, r["status"]
    return ("green", r, "run success") if r["conclusion"] == "success" else ("red", r, "run %s" % r["conclusion"])


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
    # GATE-FIX: the old judge (the newest run, whatever commit it ran on) must fail the unrun-merge case, and a builder
    # that copies the body as it is must fail the disarm case
    old_b = [n for n, ok, _ in cases(main_check=lambda api: check_main(api, merge_of=lambda a, runs: (runs[0]["head_sha"], None)))
             if not ok]
    caught = [n for n in old_b if n.startswith("(b') a merge with no run")]
    print("  %s  planting the newest-run judge (no merge check) fails the unrun-merge case" % ("PASS" if caught else "FAIL"))
    bad += not caught
    old_a = [n for n, ok, _ in cases(clean=lambda t: t) if not ok]
    caught = [n for n in old_a if n.startswith("(a)")]
    print("  %s  planting a squash message copied as it is fails the disarm case" % ("PASS" if caught else "FAIL"))
    bad += not caught
    # CLOUD-LEAN: the watch's four outcomes, and a watch that reports green while a job still runs must be CAUGHT
    for name, ok, detail in watch_cases():
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "   -> " + detail))
        bad += not ok
    planted = [n for n, ok, _ in watch_cases(state=watch_state_run_only) if not ok]
    caught = [n for n in planted if "while jobs still run" in n]
    print("  %s  planted fault (a watch that trusts the run's own status, green while a job still runs): %s (%d case(s) fail)" % (
        "PASS" if caught else "FAIL", "CAUGHT" if caught else "NOT CAUGHT", len(planted)))
    bad += not caught
    planted = [n for n, ok, _ in watch_cases(pick=head_literally) if not ok]
    caught = [n for n in planted if "[skip ci] bot commit" in n]
    print("  %s  planted fault (a default that takes main's head as it is, a bot skip-marker commit): %s" % (
        "PASS" if caught else "FAIL", "CAUGHT" if caught else "NOT CAUGHT"))
    bad += not caught
    print("%s" % ("selftest FAILED" if bad else "selftest passed"))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("number", nargs="?", type=int)
    ap.add_argument("--override", help="Jon's ruling and its date; waives the main-is-green rule only")
    ap.add_argument("--wait", type=int, default=0, help="seconds to poll while a check is unfinished (default 0: refuse)")
    ap.add_argument("--watch", action="store_true", help="after a merge, watch main's run on the squash commit (up to --wait)")
    ap.add_argument("--watch-main", nargs="?", const="", metavar="SHA",
                    help="watch main's run on SHA (default: main's newest merge, bot skip-marker commits passed over); "
                         "one line, exit 0 only if GREEN")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    note = lambda m: print(m, file=sys.stderr)   # progress to stderr: stdout carries the one line
    if a.watch_main is not None:
        if a.number or a.override is not None or a.watch:
            ap.error("--watch-main takes no PR number, --override or --watch")
        sha = a.watch_main.strip().lower()
        if sha and not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            ap.error("--watch-main takes a commit sha (7 to 40 hex digits)")
        code, line, to_stderr = watch_cmd(gh_api, sha, a.wait, log=note)
        print(line, file=sys.stderr if to_stderr else sys.stdout)
        return code
    if not a.number:
        ap.error("a PR number is required")
    return merge_and_report(gh_api, a.number, a.override, a.wait, a.watch, note=note)


if __name__ == "__main__":
    sys.exit(main())
