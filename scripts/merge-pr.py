#!/usr/bin/env python3
# ci-line: Merge guard (scripts/merge-pr.py: green Gate and green main or no merge; override only for main; recorded API fixtures) | --selftest
"""The one way either lane merges a PR (CLAUDE.md "Neither lane merges while main's last full run is red", canon §7.8.3).

    python scripts/merge-pr.py <number>                      # merge if the guard passes, else refuse (exit 1)
    python scripts/merge-pr.py <number> --wait 600           # while a check is still running, poll up to 600 s, then refuse
    python scripts/merge-pr.py <number> --override "<Jon's ruling and date>"
    python scripts/merge-pr.py <number> --watch --wait 3600  # merge, then watch main's run on the squash commit
    python scripts/merge-pr.py <number> --head <sha> ...     # judge nothing until GitHub reports <sha> as the PR's head
    python scripts/merge-pr.py --watch-main [<sha>] [--wait <s>]   # watch main's run on <sha> (default: main's newest merge)
    python scripts/merge-pr.py --selftest                    # recorded API fixtures; no network

The guard, from the GitHub REST API through `gh api` (the credentials the lanes already use):

  (a) the PR is open, and its Gate ("Gate (every job passed)") is a completed success on the PR's head commit;
  (a') the PR head's phone-fit run (PHONE-FIT-CHANGED-GAMES, 22 Nov 2026): .github/workflows/phone-fit-full.yml runs on
      every pull request and measures the games the PR changes (all of them for a shared path, none when it changes
      neither). The newest pull_request run of it on the head commit must be a completed success, judged as the Gate
      is, by its own status and conclusion. Every push to a PR starts one, so no run on the head means not started yet:
      waited for within --wait, then refused (a head pushed before that workflow change has none: merge main in, which
      AGENTS.md asks for anyway once main has gained checks). A run that measured nothing is a success like any other.
      --override never waives it.
  (a'') the runs (a) and (a') judge tested main's newest merge (MERGE-GUARD, 27 Nov 2026). A pull_request run tests the PR
      merged onto main as main stood when the run was triggered; a PR merged to main after that is untested with this
      one. #930 merged so on 26 Nov: its Gate's run was created at 17:16:26Z, #927 (the large-screen layer) landed on
      main at 17:35:08Z, and #930 merged at 17:52:57Z on that Gate. M is main's newest merge as (b') picks it, the bot's
      skip-marker commits passed over. If M is the PR's head or an ancestor of it (compare M...head reads "ahead" or
      "identical"), main was merged in and this passes. Otherwise each judged run must have been created after M's
      committer date (GitHub's squash merge writes the merge time there): for the Gate, the check-site.yml pull_request
      run on the head whose check suite is the judged Gate check's (the run's created_at; the Gate check's own
      started_at is the END of the run, the Gate being its last job, and is never used); for phone-fit, the judged
      run's created_at. A run created at or before M's time is refused, naming M: merge main into the branch and let
      the checks re-run (AGENTS.md:58). It is red, never "not finished": --wait does not wait on it (a stale run never
      freshens), and it is judged while a run is still going. --override never waives it. A Gate check that cannot be
      tied to its run, or a compare or commit that cannot be read, is refused, never guessed. If M itself cannot be
      read, (b') refuses and this adds nothing (under --override, which waives (b'), it refuses itself). GitHub's
      "require branches to be up to date" setting is not used: the bots commit to main with a skip marker several times
      a day (daily.json, answer counts, CI timings, REGISTER, handover archives) and it would force a re-run after each.
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
PR first, then merges. An empty ruling is refused. (a), (a') and (a'') are never waived. The merge is a squash pinned to the head
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

GitHub's timing (MERGE-PR-ROBUST, 17 Nov 2026) changes none of the rules above; it stops a lane being refused by GitHub
rather than by a red Gate or red main:

  Retries. A read (GET) that fails with an HTTP 5xx, gh's "Server Error" or a connection reset is tried 4 times in all,
      5, 15 and 45 s apart (RETRY_BACKOFF_S), then raised as Transient, naming the status. A 4xx is never retried. A PUT
      or POST is never re-sent (a 502 on the merge PUT can come back after GitHub merged): it is refused, saying so. A
      jobs page that still fails is asked for at 25, then 13 a page (JOBS_SIZES), and paging goes on at that size.
      The guard counts a Transient as not finished: it waits within --wait ("waiting: GitHub <status> reading <what>"),
      and refuses, naming it, when --wait runs out. A Transient is never judged red or green.
  --head SHA. The commit expected at the PR's head. Until GitHub reports it nothing is judged (a stale head's Gate, red
      or green, never counts): the guard waits within --wait ("waiting: PR head <old7> has not caught up with <new7>"),
      then refuses. Without --head, when this checkout's branch is the PR's head branch, its `git rev-parse HEAD` is the
      expected head, said in the first log line; on any other branch nothing is expected, as before.
  Registration grace. After a merge with --watch, the watch waits at least REGISTER_GRACE_S (180 s) for main's run on
      the squash commit to register, whatever --wait is; NO RUN FOUND only after both. Once the run exists, --wait alone
      bounds the wait for it to finish. --watch-main has no grace.
"""
import argparse
import calendar
import json
import re
import subprocess
import sys
import time

GATE = "Gate (every job passed)"
WORKFLOW = "check-site.yml"
PHONE_FIT = "phone-fit-full.yml"     # (a'): its pull_request run on the PR's head
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


class Transient(Refused):
    """GitHub failed in a way that says nothing about the PR or main: an HTTP 5xx, gh's "Server Error", a connection
    reset. A Refused, so every caller that stops on Refused still stops; the guard alone treats it as "not finished"."""
    def __init__(self, msg, status="", what=""):
        Refused.__init__(self, msg)
        self.status, self.what = status, what


# MERGE-PR-ROBUST (17 Nov 2026): a read (GET) that fails transiently is tried 4 times in all, these seconds apart.
# PUT and POST are never re-sent: a 502 on the merge PUT can come back after GitHub has merged.
RETRY_BACKOFF_S = (5, 15, 45)
_HTTP4 = re.compile(r"HTTP 4\d\d")
_HTTP5 = re.compile(r"HTTP (5\d\d)")
_TRANSIENT = re.compile(r"server error|connection reset", re.I)


def classify(method, path, text):
    """-> the exception for a failed gh call: Transient for a 5xx/Server Error/connection reset, else Refused.
    A 4xx is never transient."""
    text = (text or "").strip()[:300]
    msg = "gh api %s %s failed: %s" % (method, path, text)
    if _HTTP4.search(text):
        return Refused(msg)
    m5, mt = _HTTP5.search(text), _TRANSIENT.search(text)
    if not (m5 or mt):
        return Refused(msg)
    return Transient(msg, ("HTTP " + m5.group(1)) if m5 else mt.group(0).lower(), "%s %s" % (method, path))


def gh_raw(method, path, **fields):
    """One `gh api` call, no retry. Raises Transient or Refused (classify())."""
    cmd = ["gh", "api", "-X", method, path]
    for k, v in fields.items():
        cmd += ["-f", "%s=%s" % (k, v)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        raise classify(method, path, p.stderr or p.stdout)
    return json.loads(p.stdout) if p.stdout.strip() else {}


def with_retry(call, sleep=time.sleep, log=None):
    """`call` with GETs retried on Transient (RETRY_BACKOFF_S between tries). After the last try, Transient again, its
    message naming the status and the attempts. A Transient on a PUT or POST is not retried and becomes a plain
    Refused, so nothing downstream waits on it or sends it again."""
    def api(method, path, **fields):
        attempt = 0
        while True:
            try:
                return call(method, path, **fields)
            except Transient as e:
                if method != "GET":
                    raise Refused("%s (not retried: a %s is never re-sent; check the PR on GitHub before running again)"
                                  % (e, method))
                if attempt >= len(RETRY_BACKOFF_S):
                    raise Transient("GitHub %s reading %s after %d attempts: %s" % (e.status, path, attempt + 1, e),
                                    e.status, path)
                if log:
                    log("retrying in %ds: GitHub %s reading %s" % (RETRY_BACKOFF_S[attempt], e.status, path))
                sleep(RETRY_BACKOFF_S[attempt])
                attempt += 1
    return api


gh_api = with_retry(gh_raw)


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


def check_phone_fit(api, pr):
    """(a') -> (ok, why). The newest pull_request run of phone-fit-full.yml on the head commit, judged as the Gate is: by
    its own status and conclusion. No run yet is "not finished" (every PR push starts one), never green."""
    sha = pr["head"]["sha"]
    d = api("GET", "%s/actions/workflows/%s/runs?event=pull_request&head_sha=%s&per_page=20" % (R, PHONE_FIT, sha))
    runs = sorted((r for r in d.get("workflow_runs", []) if r.get("head_sha") == sha and r.get("event") == "pull_request"),
                  key=lambda r: r["id"])
    if not runs:
        return False, ("no phone-fit run on head %s yet, not finished (every push to a PR starts one; a head pushed before "
                       "PHONE-FIT-CHANGED-GAMES has none: merge main into the branch)" % sha[:7])
    r = runs[-1]
    if r["status"] != "completed":
        return False, "phone-fit run %s on head %s is %s, not finished" % (r["id"], sha[:7], r["status"])
    if r["conclusion"] != "success":
        return False, "phone-fit run %s on head %s is %s" % (r["id"], sha[:7], r["conclusion"])
    return True, "phone-fit run %s green on head %s" % (r["id"], sha[:7])


def main_runs(api):
    d = api("GET", "%s/actions/workflows/%s/runs?per_page=50" % (R, WORKFLOW))
    runs = [r for r in d.get("workflow_runs", []) if r["event"] in MAIN_EVENTS and r["head_branch"] == "main"]
    return sorted(runs, key=lambda r: r["created_at"], reverse=True)


JOBS_PER_PAGE = 50   # GitHub answered 502 at 100 a page for a re-run main run of 71 jobs, every time (27 Oct 2026); 50 read it.
# 16-17 Nov 2026: 502 again at 50 a page on a re-run main run of 92 jobs (43961875130), three merge-pr.py runs on #805, while
# the same request by hand answered 8 of 8. So a page that still fails after gh_api's retries is asked for at half the size.
JOBS_SIZES = (JOBS_PER_PAGE, 25, 13)   # never lower than 13 (contract MERGE-PR-ROBUST)


def run_jobs(api, run_id, sizes=JOBS_SIZES):
    """Every job of the run's latest attempt, all pages. A page that fails with Transient is asked for again at the next
    smaller size in `sizes`, and paging goes on at that size; Transient at the smallest size, or any Refused, is raised."""
    jobs, page, total, i = [], 1, None, 0
    while page <= 200:
        per = sizes[i]
        try:
            d = api("GET", "%s/actions/runs/%s/jobs?per_page=%d&page=%d" % (R, run_id, per, page))
        except Transient:
            if i + 1 >= len(sizes):
                raise
            i += 1
            # go on from the same job at the smaller size; if that offset is not a whole page of it, start again
            if len(jobs) % sizes[i] == 0:
                page = len(jobs) // sizes[i] + 1
            else:
                jobs, page = [], 1
            continue
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
    except Transient:
        raise   # not "unreadable, so red": the guard waits on it (MERGE-PR-ROBUST)
    except Refused as e:
        return None, "main's commits could not be read (%s)" % e
    for c in commits if isinstance(commits, list) else []:
        login = (c.get("author") or {}).get("login") or ""
        name = ((c.get("commit") or {}).get("author") or {}).get("name") or ""
        if BOT in (login, name) and has_skip_marker((c.get("commit") or {}).get("message")):
            continue
        return c["sha"], None
    return None, "no commit on main in the last 50 that is not a bot skip-marker commit"


def check_main(api, merge_of=newest_merge, jobs_of=run_jobs):
    """(b) -> (ok, why, run). Never guesses: an unfinished run or job, or no run at all, is not green; nor is a merge
    with no run of its own (b'). A Transient read is raised, not judged: the guard counts it as not finished."""
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
        jobs = jobs_of(api, r["id"])
    except Transient:
        raise
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


def _when(stamp):
    """GitHub's UTC time ("2026-11-26T17:35:08Z") in seconds, or None if it is not one."""
    try:
        return calendar.timegm(time.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError):
        return None


def in_branch(api, base, head):
    """True if commit `base` is `head` or an ancestor of it: compare base...head reads "ahead" or "identical"."""
    if base == head:
        return True
    st = api("GET", "%s/compare/%s...%s?per_page=1" % (R, base, head)).get("status")
    if st not in ("ahead", "identical", "behind", "diverged"):
        raise Refused("compare %s...%s gave status %r" % (base[:7], head[:7], st))
    return st in ("ahead", "identical")


def gate_run_created(api, sha, gate):
    """(run id, created_at) of the check-site.yml pull_request run on `sha` that the Gate check `gate` belongs to: the run
    whose check_suite_id is the check's check suite. created_at is when the run was triggered, and so what main held in
    the merge it tested. The Gate check's own started_at is the end of that run and is never used."""
    suite = (gate.get("check_suite") or {}).get("id")
    if suite is None:
        raise Refused("the Gate check %s names no check suite" % gate.get("id"))
    d = api("GET", "%s/actions/workflows/%s/runs?event=pull_request&head_sha=%s&per_page=100" % (R, WORKFLOW, sha))
    own = [r for r in d.get("workflow_runs", [])
           if r.get("check_suite_id") == suite and r.get("head_sha") == sha and r.get("event") == "pull_request"]
    if not own:
        raise Refused("no check-site pull_request run on head %s is in the Gate check's check suite %s" % (sha[:7], suite))
    return own[0]["id"], own[0].get("created_at")


def check_fresh(api, pr, waived=False, merge_of=newest_merge, inside=in_branch, gate_when=gate_run_created):
    """(a'') -> (ok, why). The runs (a) and (a') judge tested main's newest merge M: M is in the PR's branch, or each run
    was created after M's committer date. Red when it fails, never "not finished". A run that does not exist yet is
    (a)'s or (a')'s to wait for; one that exists is judged whether or not it has finished. `waived`: (b) is waived by
    --override, so an unreadable M, which (b') would refuse, is refused here. A Transient read is raised, not judged."""
    sha = pr["head"]["sha"]
    m, why = merge_of(api)
    if m is None:
        if waived:
            return False, "the PR's runs cannot be judged against main's newest merge: %s (--override does not waive this)" % why
        return True, "main's newest merge could not be read; (b') refuses"
    try:
        if inside(api, m, sha):
            return True, "main's newest merge %s is in the branch" % m[:7]
        c = api("GET", "%s/commits/%s" % (R, m)).get("commit") or {}
        at = (c.get("committer") or {}).get("date")
        if _when(at) is None:
            raise Refused("its committer date reads %r" % (at,))
        title = ((c.get("message") or "").split("\n") or [""])[0][:60]
        judged = []   # (what, created_at) for each run that exists
        checks = api("GET", "%s/commits/%s/check-runs?per_page=100" % (R, sha)).get("check_runs", [])
        gates = sorted((x for x in checks if x["name"] == GATE), key=lambda x: x["id"])
        if gates:   # the Gate check (a) judges: the newest
            judged.append(("Gate", gate_when(api, sha, gates[-1])[1]))
        d = api("GET", "%s/actions/workflows/%s/runs?event=pull_request&head_sha=%s&per_page=20" % (R, PHONE_FIT, sha))
        runs = sorted((r for r in d.get("workflow_runs", []) if r.get("head_sha") == sha and r.get("event") == "pull_request"),
                      key=lambda r: r["id"])
        if runs:    # the run (a') judges: the newest
            judged.append(("phone-fit run", runs[-1].get("created_at")))
        for what, t in judged:
            if _when(t) is None:
                raise Refused("the %s on head %s has no readable start time (%r)" % (what, sha[:7], t))
    except Transient:
        raise
    except Refused as e:
        return False, ("cannot tell whether this PR's checks ran against main's newest merge %s: %s. Not guessed: merge main "
                       "into the branch and let the checks re-run (AGENTS.md:58)" % (m[:7], e))
    stale = [(what, t) for what, t in judged if _when(t) <= _when(at)]
    if stale:
        return False, ("main gained %s (%s) at %s after this PR's %s: merge main into the branch and let the checks re-run "
                       "(AGENTS.md:58)" % (m[:7], title, at, " and ".join("%s started at %s" % x for x in stale)))
    return True, "the PR's runs were created after main's newest merge %s" % m[:7]


def no_local(ref):
    """The default for guard()'s `local`: no checkout to compare with."""
    return None


def git_local(ref):
    """`git rev-parse HEAD` if the checkout's current branch is `ref` (the PR's head branch), else None."""
    try:
        br = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, encoding="utf-8")
        if br.returncode != 0 or br.stdout.strip() != ref:
            return None
        sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, encoding="utf-8")
        return sha.stdout.strip().lower() if sha.returncode == 0 and sha.stdout.strip() else None
    except OSError:
        return None


def guard(api, number, override=None, wait=0, main_check=check_main, sleep=time.sleep, log=print, clean=disarm,
          head=None, local=no_local, clock=time.time, phone_check=check_phone_fit, fresh_check=check_fresh):
    """Merge or raise Refused. Returns (merge_response, judged_run).

    MERGE-PR-ROBUST: `head` is the commit expected at the PR's head (--head, or `local(<the PR's head ref>)`, the
    checkout's HEAD when it is on that branch). Until GitHub reports it, nothing is judged: a stale head's Gate, red or
    green, never counts; the guard waits within `wait`, then refuses. A Transient read is waited on the same way."""
    if override is not None and not override.strip():
        raise Refused("--override needs Jon's ruling and its date as text")
    deadline = clock() + wait
    head = head.strip().lower() if head else None
    asked = head is not None
    while True:
        try:
            pr = api("GET", "%s/pulls/%d" % (R, number))
            if pr["state"] != "open" or pr.get("merged"):
                raise Refused("PR #%d is not open (%s)" % (number, "merged" if pr.get("merged") else pr["state"]))
            if pr["base"]["ref"] != "main":
                raise Refused("PR #%d targets %s, not main" % (number, pr["base"]["ref"]))
            if not asked:
                asked, head = True, local(pr["head"].get("ref"))
                if head:
                    log("expected head %s: this checkout's HEAD on %s (--head names another)" % (head[:7], pr["head"]["ref"]))
            got = pr["head"]["sha"]
            if head and not got.lower().startswith(head):
                stale = "PR head %s has not caught up with %s" % (got[:7], head[:7])
                if clock() >= deadline:
                    raise Refused(stale + (" after %ds" % wait if wait else "") + "; nothing judged")
                log("waiting: " + stale)
                sleep(POLL_S)
                continue
            ok_a, why_a = check_gate(api, pr)
            ok_p, why_p = phone_check(api, pr)          # (a'), never waived
            ok_b, why_b, run = main_check(api) if override is None else (True, "waived by --override", None)
            ok_f, why_f = fresh_check(api, pr, waived=override is not None)   # (a''), never waived, never waited on
        except Transient as e:
            what = "GitHub %s reading %s" % (e.status, e.what)
            if clock() >= deadline:
                raise   # its message names the status, the read and the attempts
            log("waiting: " + what)
            sleep(POLL_S)
            continue
        if ok_a and ok_p and ok_b and ok_f:
            break
        # a thing that is merely unfinished may be waited for; a red one never is
        unfinished = ("not finished" in why_a or "no %r" % GATE in why_a or "not finished" in why_b)
        red = ((not ok_a and not unfinished) or (not ok_b and "not finished" not in why_b)
               or (not ok_p and "not finished" not in why_p) or not ok_f)
        said = "; ".join(w for ok, w in ((ok_a, why_a), (ok_p, why_p), (ok_f, why_f), (ok_b, why_b)) if not ok)
        if red or clock() >= deadline:
            raise Refused(said)
        log("waiting: " + said)
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


REGISTER_GRACE_S = 180   # a fresh merge's push runs register within seconds to a minute (#803: NO RUN FOUND at --wait 0)


def watch_main(api, sha, wait=0, state=watch_state, sleep=time.sleep, clock=time.time, log=None, grace=0):
    """-> (exit code, the one line). Polls every POLL_S while the run is missing or unfinished, up to `wait` seconds;
    while no run has registered, up to max(wait, grace) (the post-merge watch passes REGISTER_GRACE_S)."""
    start = clock()
    while True:
        st, r, detail = state(api, sha)
        if st == "green":
            return 0, "main %s run %s: GREEN" % (sha[:7], r["id"])
        if st == "red":
            return 1, "main %s run %s: RED: %s" % (sha[:7], r["id"], detail)
        elapsed = clock() - start
        limit = max(wait, grace) if st == "none" else wait
        if elapsed >= limit:
            if st == "none":
                return 1, "main %s: NO RUN FOUND" % sha[:7]
            return 1, "main %s: NOT FINISHED after %ds" % (sha[:7], int(round(elapsed)))
        if log:
            log("waiting: main %s: %s" % (sha[:7], detail))
        sleep(min(POLL_S, limit - elapsed))


def merge_and_report(api, number, override=None, wait=0, watch=False, out=print, note=None, sleep=time.sleep,
                     clock=time.time, state=watch_state, head=None, local=no_local, log=print, grace=REGISTER_GRACE_S):
    """The merge command: guard(), then its report; with `watch`, the watch on the squash commit last, which waits at
    least `grace` seconds for that commit's run to register, whatever `wait` is."""
    try:
        res, run = guard(api, number, override, wait, sleep=sleep, clock=clock, head=head, local=local, log=log)
    except Refused as e:
        out("REFUSED #%d: %s" % (number, e))
        return 1
    try:   # the merge has happened: a failed read here must not hide it (no traceback in place of the report)
        main_head = api("GET", "%s/git/ref/heads/main" % R)["object"]["sha"]
        shown = main_head[:7]
    except Refused as e:
        main_head, shown = "", "unread (%s)" % e
    judged = ("run %s (%s)" % (run["id"], run["html_url"] if "html_url" in run else run["conclusion"])) if run else "waived by --override"
    out("MERGED #%d (squash, %s). main head %s. Judged: %s." % (number, res.get("sha", "")[:7], shown, judged))
    if not watch:
        out("Now wait for main's run on that commit and report it (CLAUDE.md), then end-task.py.")
        return 0
    sha = res.get("sha") or main_head
    if not sha:
        out("main: NOT FINISHED after 0s (neither the squash commit nor main's head could be read; use --watch-main)")
        return 1
    code, line = watch_main(api, sha, wait, state=state, sleep=sleep, clock=clock, log=note, grace=grace)
    out(line)
    return code


def watch_cmd(api, sha="", wait=0, pick=newest_merge, **kw):
    """--watch-main -> (exit code, line, to_stderr). With no sha, the commit is main's newest merge as (b') picks it,
    newest_merge(): the bot's skip-marker commits (timings, register, answer counts) have no run and are passed over
    (Amendment 2, Jon 3 Nov 2026). If main's commits cannot be read, exit 2 and say why on stderr."""
    if not sha:
        try:
            sha, why = pick(api)
        except Transient as e:   # newest_merge() raises it for the guard to wait on; here it is unreadable, as before
            sha, why = None, "main's commits could not be read (%s)" % e
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


def _pfrun(sha, status, concl, i=45000000001, event="pull_request"):
    """A phone-fit-full.yml run on a PR head (PHONE-FIT-CHANGED-GAMES)."""
    return _run(i, event, status, concl, "2026-11-22T10:00:00Z", "claude/x", sha)


def _job(name, status="completed", concl="success"):
    return {"name": name, "status": status, "conclusion": concl}


def _commit(sha, msg, who="Vector52F", when=None):
    return {"sha": sha, "author": {"login": who},
            "commit": {"author": {"name": who}, "message": msg, "committer": {"date": when}}}


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
                 max_per_page=None, commits=None, commits_error=False, faults=None, pr_script=None, gates=None,
                 pf=None, compare=None, gate_runs=None):
        self.pr, self.gate, self.runs, self.calls = pr, gate, runs, []
        # MERGE-GUARD (a''): compare is {base sha: status} for GET compare/<base>...<head>; a base not named reads
        # "ahead" (main's newest merge is in the branch), so every fixture older than (a'') passes it unread.
        # gate_runs: check-site.yml's pull_request runs on the head. A phone-fit script (pf) moves on once per poll
        # (per read of the PR), since (a') and (a'') each read the runs in one poll.
        self.compare, self.gate_runs, self._pf_now = compare or {}, gate_runs or [], None
        # pf (PHONE-FIT-CHANGED-GAMES): successive lists of phone-fit-full.yml runs, one per read (the last repeats);
        # None: one completed success pull_request run on whatever head is asked for.
        self.pf = list(pf) if pf is not None else None
        # MERGE-PR-ROBUST: faults are [method, path substring, times (None: every time), gh's text]; each call that
        # matches raises classify()'s exception, as gh_raw would. pr_script: successive PR reads (the last repeats);
        # gates: the Gate's check-runs by head sha.
        self.faults = [list(f) for f in (faults or [])]
        self.pr_script, self.gates = list(pr_script or []), gates
        self.commits = COMMITS if commits is None else commits   # main's commits, newest first (GATE-FIX b')
        self.commits_error = commits_error
        self.max_per_page = max_per_page   # GitHub's 502 for a page too large (27 Oct 2026)
        self.script = script or []   # successive run lists, for the wait case
        # jobs: a list of pages (each a list of jobs); jobs_script: successive such lists, one per poll
        self.jobs = jobs if jobs is not None else [JOBS_OK]
        self.jobs_script, self.jobs_error = jobs_script or [], jobs_error

    def __call__(self, method, path, **fields):
        self.calls.append((method, path, fields))
        for f in self.faults:
            if f[0] == method and f[1] in path and (f[2] is None or f[2] > 0):
                if f[2] is not None:
                    f[2] -= 1
                raise classify(method, path, f[3])
        if method == "GET" and "/check-runs" in path:
            if self.gates is not None:
                return self.gates[path.split("/commits/", 1)[1].split("/", 1)[0]]
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
        if method == "GET" and "/compare/" in path:
            return {"status": self.compare.get(path.split("/compare/", 1)[1].split("...", 1)[0], "ahead")}
        if method == "GET" and "/commits/" in path:   # one commit (a check-runs read was answered above)
            for c in self.commits:
                if c["sha"] == path.rsplit("/commits/", 1)[1]:
                    return c
            raise Refused("gh api GET %s failed: gh: Not Found (HTTP 404)" % path)
        if method == "GET" and "/commits?sha=main" in path:
            if self.commits_error:
                raise Refused("gh api GET %s failed: HTTP 502" % path)
            return self.commits
        if method == "GET" and "/actions/workflows/%s/" % PHONE_FIT in path:
            sha = path.split("head_sha=", 1)[1].split("&", 1)[0]
            if self.pf is None:
                return {"workflow_runs": [_pfrun(sha, "completed", "success")]}
            if self._pf_now is None:
                self._pf_now = self.pf.pop(0) if len(self.pf) > 1 else self.pf[0]
            return {"workflow_runs": [r for r in self._pf_now if r["head_sha"] == sha]}
        if method == "GET" and "/actions/workflows/%s/runs?event=pull_request" % WORKFLOW in path:
            return {"workflow_runs": self.gate_runs}
        if method == "GET" and "/actions/workflows/" in path:
            runs = self.script.pop(0) if len(self.script) > 1 else (self.script[0] if self.script else self.runs)
            return {"workflow_runs": runs}
        if method == "GET" and "/pulls/" in path:
            self._pf_now = None   # a new poll
            if self.pr_script:
                return self.pr_script.pop(0) if len(self.pr_script) > 1 else self.pr_script[0]
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
    out += phone_fit_cases(main_check)
    return out


def phone_fit_cases(main_check=check_main, phone_check=check_phone_fit):
    """(a') PHONE-FIT-CHANGED-GAMES, 22 Nov 2026: the PR head's phone-fit run, waited for and judged as the Gate is."""
    out = []

    def case(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    def go(fake, wait=0, **kw):
        c, logs = Clock(), []
        try:
            guard(fake, 473, wait=wait, main_check=main_check, sleep=c.sleep, clock=c, log=logs.append,
                  phone_check=phone_check, **kw)
            return None, c, logs
        except Refused as e:
            return str(e), c, logs

    ok, red, going, queued = (_pfrun(HEAD, "completed", "success"), _pfrun(HEAD, "completed", "failure"),
                              _pfrun(HEAD, "in_progress", None), _pfrun(HEAD, "queued", None))
    f = Fake(pf=[[red]])
    err, c, _ = go(f, wait=3600)
    case("(a') a red phone-fit run on the head refuses at once (never waited out), nothing merged",
         err and "phone-fit" in err and "failure" in err and not f.merged() and c.t == 0, err or "MERGED")
    f = Fake(pf=[[red]])
    err, c, _ = go(f, override="Jon, 22 Nov 2026: merge it")
    case("(a') a red phone-fit run refuses even with --override (no comment, no merge)",
         err and "phone-fit" in err and not f.merged() and not f.comments(), err or "MERGED")
    f = Fake(pf=[[]])
    err, c, _ = go(f)
    case("(a') no phone-fit run on the head yet (not started): refused with --wait 0, never green",
         err and "no phone-fit run" in err and "not finished" in err and not f.merged(), err or "MERGED")
    f = Fake(pf=[[], [queued], [going], [ok]])
    err, c, logs = go(f, wait=3600)
    case("(a') not started, then queued, then running, then green: waited for within --wait, then merges",
         err is None and len(f.merged()) == 1 and c.slept == 3 and any("no phone-fit run" in l for l in logs), err or repr(logs))
    f = Fake(pf=[[going]])
    err, c, _ = go(f, wait=120)
    case("(a') a phone-fit run that never finishes: refused when --wait runs out, naming it",
         err and "in_progress" in err and "not finished" in err and not f.merged() and c.t >= 120, err or "MERGED")
    f = Fake(pf=[[ok]])
    err, c, logs = go(f, wait=3600)
    case("(a') a run that measured nothing (no game or shared path changed) is a success: merges with no wait",
         err is None and len(f.merged()) == 1 and c.t == 0 and not logs, err or repr(logs))
    f = Fake(pf=[[_pfrun(HEAD, "completed", "success", i=45000000001), _pfrun(HEAD, "completed", "failure", i=45000000009)]])
    err, c, _ = go(f)
    case("(a') the newest run on the head wins: a red rerun after a green one refuses",
         err and "45000000009" in err and not f.merged(), err or "MERGED")
    f = Fake(pf=[[_pfrun(HEAD, "completed", "failure", i=45000000001), _pfrun(HEAD, "completed", "success", i=45000000009)]])
    err, c, _ = go(f)
    case("(a') ... and a green rerun after a red one merges", err is None and len(f.merged()) == 1, err or "")
    f = Fake(pf=[[_pfrun("9" * 40, "completed", "success"), _pfrun(HEAD, "completed", "failure", i=45000000009)]])
    err, c, _ = go(f)
    case("(a') a green run on another commit never counts for this head", err and "failure" in err and not f.merged(), err or "MERGED")
    f = Fake(pf=[[_pfrun(HEAD, "completed", "success", event="push")]])
    err, c, _ = go(f)
    case("(a') a push run on the head commit is not the PR's run: not green", err and "no phone-fit run" in err
         and not f.merged(), err or "MERGED")
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


# ---- MERGE-PR-ROBUST (17 Nov 2026): GitHub's 5xx, a PR head that has not caught up with a push, a run not registered yet ----
E502 = "gh: Server Error (HTTP 502)"
E404 = "gh: Not Found (HTTP 404)"
OLD = "c08a613" + "0" * 33   # #802: the head GitHub still reported, its Gate failed, after the fix was pushed
PR_OLD = dict(PR_OPEN, head={"sha": OLD, "ref": "claude/x"})
PR_NEW = dict(PR_OPEN, head={"sha": HEAD, "ref": "claude/x"})
M_GOING = [_wrun("in_progress", None, sha=SQUASH)] + GREEN


def old_api(call, sleep=None, log=None):
    """The planted fault: gh_api before MERGE-PR-ROBUST. One try, and every failure a plain Refused."""
    def api(method, path, **fields):
        try:
            return call(method, path, **fields)
        except Refused as e:
            raise Refused(str(e))
    return api


def naive_retry(call, sleep=time.sleep, log=None):
    """The planted fault: a retry that re-sends any call (PUT and POST too) on any failure (4xx too)."""
    def api(method, path, **fields):
        for attempt in range(len(RETRY_BACKOFF_S) + 1):
            try:
                return call(method, path, **fields)
            except Refused:
                if attempt == len(RETRY_BACKOFF_S):
                    raise
                sleep(RETRY_BACKOFF_S[attempt])
    return api


def robust_cases(retry=with_retry, sizes=JOBS_SIZES, use_head=True, grace=REGISTER_GRACE_S):
    """-> list of (name, ok, detail, plants): `plants` names the planted faults the case must catch (selftest())."""
    out = []

    def case(name, ok, detail, *plants):
        out.append((name, bool(ok), detail, set(plants)))

    def main_check(api):
        return check_main(api, jobs_of=lambda a, rid: run_jobs(a, rid, sizes=sizes))

    def try_guard(fake, wait=0, head=None, local=no_local):
        c, logs = Clock(), []
        if not use_head:
            head, local = None, no_local
        try:
            guard(retry(fake, sleep=c.sleep), 473, wait=wait, main_check=main_check, sleep=c.sleep, clock=c,
                  log=logs.append, head=head, local=local)
            return None, c, logs
        except Refused as e:
            return str(e), c, logs

    def jobs_calls(fake, per=None):
        return [x for x in fake.calls if "/jobs" in x[1] and (per is None or "per_page=%d&" % per in x[1])]

    f = Fake(faults=[["GET", "/jobs?per_page=50&page=1", 1, E502]])
    err, c, _ = try_guard(f)
    case("[robust] one 502 on the jobs' page 1, then success: retried after 5 s, merges", err is None and len(f.merged()) == 1
         and len(jobs_calls(f)) == 2 and c.t == 5, err or "jobs calls %d, t %s" % (len(jobs_calls(f)), c.t), "retry")

    f = Fake(faults=[["GET", "/jobs?per_page=50&", None, E502]])
    err, c, _ = try_guard(f)
    case("[robust] 502 on every try at 50 a page, success at 25: read at 25, merges", err is None and len(f.merged()) == 1
         and len(jobs_calls(f, 50)) == 4 and len(jobs_calls(f, 25)) == 1 and not jobs_calls(f, 13),
         err or "calls %s" % [x[1] for x in jobs_calls(f)], "retry", "sizes")

    f = Fake(faults=[["GET", "/jobs", None, E502]])
    err, c, _ = try_guard(f)
    case("[robust] 502 forever on the jobs: 4 tries at each of 50, 25 and 13, then refused naming the 502, nothing merged",
         err and "HTTP 502" in err and "after 4 attempts" in err and len(jobs_calls(f)) == 12
         and [int(x[1].split("per_page=")[1].split("&")[0]) for x in jobs_calls(f)] == [50] * 4 + [25] * 4 + [13] * 4
         and not f.merged(), err or "MERGED", "retry", "sizes")

    f = Fake(faults=[["GET", "/check-runs", 4, E502]])
    err, c, logs = try_guard(f, wait=600)
    case("[robust] a 502 that outlasts the retries on one poll is waited on within --wait (never red), then merges",
         err is None and len(f.merged()) == 1 and any(l.startswith("waiting: GitHub HTTP 502 reading ") for l in logs),
         err or repr(logs), "retry")

    f = Fake(faults=[["GET", "/check-runs", None, E502]])
    err, c, _ = try_guard(f, wait=0)
    case("[robust] --wait 0 and a 502 that outlasts the retries: refused, naming it", err and "HTTP 502" in err
         and not f.merged(), err or "MERGED")

    f = Fake(faults=[["GET", "/actions/workflows/", 1, E502]], runs=RED)
    err, c, _ = try_guard(f, wait=600)
    case("[robust] a 502, then a red main: still refused red, not waited out", err and "failure" in err and not f.merged()
         and c.t == 5, err or "MERGED")

    f = Fake(faults=[["PUT", "/merge", None, E502]])
    err, c, _ = try_guard(f)
    case("[robust] a 502 on the merge PUT: sent once, never retried, refused", err and "not retried" in err
         and len(f.merged()) == 1, err or "MERGED", "naive")

    f = Fake(runs=RED, faults=[["POST", "/comments", None, E502]])
    c = Clock()
    try:
        guard(retry(f, sleep=c.sleep), 473, override="Jon, 17 Nov 2026: x", main_check=main_check, sleep=c.sleep, clock=c,
              log=lambda *a: None)
        err = None
    except Refused as e:
        err = str(e)
    case("[robust] a 502 on the override's POST: sent once, never retried, refused, nothing merged",
         err and len(f.comments()) == 1 and not f.merged(), err or "MERGED", "naive")

    f = Fake(faults=[["GET", "/jobs", None, E404]])
    err, c, _ = try_guard(f, wait=600)
    case("[robust] a 404 on the jobs: never retried, refused at once", err and "HTTP 404" in err and len(jobs_calls(f)) == 1
         and c.t == 0 and not f.merged(), err or "MERGED", "naive")

    f = Fake(pr_script=[PR_OLD, PR_OLD, PR_NEW], gates={OLD: GATE_OK, HEAD: GATE_OK})
    err, c, logs = try_guard(f, wait=600, head=HEAD)
    m = f.merged()
    case("[robust] --head: PR head stale for two polls, then caught up: waits, merges on the new head's green Gate",
         err is None and len(m) == 1 and m[0][2]["sha"] == HEAD and c.slept == 2
         and "waiting: PR head c08a613 has not caught up with 0ba5dc1" in logs
         and not [x for x in f.calls if OLD in x[1]], err or repr(logs), "head")

    f = Fake(pr_script=[PR_OLD, PR_OLD, PR_NEW], gates={OLD: GATE_RED, HEAD: GATE_OK})
    err, c, logs = try_guard(f, wait=600, head=HEAD[:7])
    m = f.merged()
    case("[robust] --head: a red Gate on the stale head is never judged: waits, merges on the new head",
         err is None and len(m) == 1 and m[0][2]["sha"] == HEAD, err or repr(logs), "head")

    f = Fake(pr_script=[PR_OLD], gates={OLD: GATE_OK})
    err, c, _ = try_guard(f, wait=120, head=HEAD)
    case("[robust] --head: a head that never catches up is refused when --wait runs out, nothing judged or merged",
         err and "has not caught up with 0ba5dc1" in err and c.t >= 120 and not f.merged()
         and not [x for x in f.calls if "/check-runs" in x[1]], err or "MERGED", "head")

    f = Fake(pr_script=[PR_OLD, PR_NEW], gates={OLD: GATE_RED, HEAD: GATE_OK})
    err, c, logs = try_guard(f, wait=600, local=lambda ref: HEAD if ref == "claude/x" else None)
    m = f.merged()
    case("[robust] no --head, the checkout on the PR's branch: its HEAD is expected, said in the first log line",
         err is None and len(m) == 1 and m[0][2]["sha"] == HEAD and logs and logs[0].startswith("expected head 0ba5dc1"),
         err or repr(logs), "head")

    f = Fake(pr_script=[PR_NEW])
    err, c, logs = try_guard(f, local=lambda ref: None)
    case("[robust] no --head, the checkout on another branch: nothing expected, as before",
         err is None and len(f.merged()) == 1 and not [l for l in logs if l.startswith("expected head")], err or repr(logs))

    def watch_merge(script, wait=0):
        f, lines, c = Fake(script=script), [], Clock()
        code = merge_and_report(retry(f, sleep=c.sleep), 473, wait=wait, watch=True, out=lines.append, sleep=c.sleep,
                                clock=c, log=lambda *a: None, grace=grace)
        return code, lines, c, f

    code, lines, c, f = watch_merge([GREEN, GREEN, GREEN, M_GREEN])
    case("[robust] merge --watch, --wait 0: the squash commit's run registers after 60 s: GREEN, not NO RUN FOUND",
         code == 0 and len(f.merged()) == 1 and lines[-1] == "main mmmmmmm run 41615387944: GREEN" and c.t == 60,
         "%s %s t %s" % (code, lines, c.t), "grace")

    code, lines, c, f = watch_merge([GREEN])
    case("[robust] merge --watch, --wait 0: no run after the %d s grace: NO RUN FOUND" % REGISTER_GRACE_S,
         code == 1 and lines[-1] == "main mmmmmmm: NO RUN FOUND" and c.t == REGISTER_GRACE_S,
         "%s %s t %s" % (code, lines, c.t), "grace")

    code, lines, c, f = watch_merge([GREEN, GREEN, M_GOING])
    case("[robust] the grace waits for a run to register, never for it to finish (--wait governs that)",
         code == 1 and lines[-1] == "main mmmmmmm: NOT FINISHED after 30s", "%s %s t %s" % (code, lines, c.t))

    code, lines, c, f = watch_merge([GREEN, GREEN, M_GREEN], wait=3600)
    case("[robust] a --wait longer than the grace is unchanged", code == 0 and c.t == 30, "%s %s t %s" % (code, lines, c.t))

    f = Fake(faults=[["GET", "/git/ref/heads/main", None, E502]], runs=M_GREEN)
    lines, c = [], Clock()
    code = merge_and_report(retry(f, sleep=c.sleep), 473, wait=0, watch=True, out=lines.append, sleep=c.sleep, clock=c,
                            log=lambda *a: None, grace=grace)
    case("[robust] main's head unreadable after the merge: the merge is still reported, then the watch's line",
         code == 0 and lines[0].startswith("MERGED #473") and "unread" in lines[0]
         and lines[-1] == "main mmmmmmm run 41615387944: GREEN", "%s %s" % (code, lines))

    for text, want in ((E502, "HTTP 502"), ("gh: HTTP 503: Service Unavailable", "HTTP 503"),
                       ("Post https://api.github.com/x: read tcp: connection reset by peer", "connection reset"),
                       ("gh: Server Error", "server error")):
        e = classify("GET", "p", text)
        case("[robust] classify: %r is Transient (%s)" % (text, want), isinstance(e, Transient) and e.status == want, repr(e))
    for text in (E404, "gh: Forbidden (HTTP 403)", "gh: Validation Failed (HTTP 422)", "unknown flag"):
        e = classify("GET", "p", text)
        case("[robust] classify: %r is not Transient" % text, isinstance(e, Refused) and not isinstance(e, Transient), repr(e))
    return out


# ---- MERGE-GUARD (27 Nov 2026), (a''): the record of 26 Nov 2026. #930's head 8cd19935 had its check-site and phone-fit
# runs created at 17:16:26Z. #927 (the large-screen layer) squash-merged to main as e72faba at 17:35:08Z. The Gate check on
# 8cd19935 started at 17:37:25Z (the Gate is the run's last job) and #930 merged at 17:52:57Z, on a Gate that never held
# #927. Ids, shas and those times are GitHub's; the other times below are set for each case. ----
F_HEAD = "8cd19935f8aed622a802a80c9a86b99e7aee3ad5"
F_M = "e72faba7f2df78c9f168359d3106b1aa45304f62"        # #927's squash commit
F_M_AT = "2026-11-26T17:35:08Z"
F_BEFORE, F_AFTER = "2026-11-26T17:16:26Z", "2026-11-26T17:40:00Z"   # a run created before M, and one after
F_PREV = "a55da6b78947b7ab03623df1db102dd627c1d51f"     # #928's squash commit, the merge before
F_SUITE = 124092601822
F_PR = dict(PR_OPEN, head={"sha": F_HEAD, "ref": "claude/base-60-list"}, title="BASE-60-LIST", body="Listing.")
F_TITLE = ("LARGE-SCREEN-LAYER: the shared large-screen layer, piloted on seven games (Shared tier: review, then Jon's "
           "merge) (#927)")
F_COMMITS = [_commit(F_M, F_TITLE + "\n\nThe layer.", when=F_M_AT),
             _commit(F_PREV, "CANON-PRIORITY: Jon's own classes second in canon 0.2 (#928)", when="2026-11-26T16:41:53Z")]
# main as it stood at 17:00Z: #928 the newest merge, the bot's timings commit (42270b2, 16:58:12Z) on top of it
F_BOTS = [_commit("42270b2f" + "0" * 32, "Record CI timings and repack (run 45861149266) [skip ci]", BOT, "2026-11-26T16:58:12Z"),
          F_COMMITS[1]]
F_MAIN = [_run(45868985623, "push", "completed", "success", "2026-11-26T17:35:12Z", sha=F_M),
          _run(45861149266, "push", "completed", "success", "2026-11-26T16:41:57Z", sha=F_PREV)]
F_DIVERGED = {F_M: "diverged", F_PREV: "diverged", F_BOTS[0]["sha"]: "diverged"}   # main was not merged into the branch


def _fgate(started="2026-11-26T17:37:25Z", status="completed", concl="success", suite=F_SUITE):
    g = {"id": 140080085797, "name": GATE, "status": status, "conclusion": concl, "started_at": started,
         "completed_at": "2026-11-26T17:37:28Z"}
    if suite is not None:
        g["check_suite"] = {"id": suite}
    return {"check_runs": [g, {"id": 140080000001, "name": "Plan", "status": "completed", "conclusion": "success",
                               "started_at": "2026-11-26T17:16:30Z", "check_suite": {"id": suite or 1}}]}


def _ffake(gate_at, pf_at, commits=F_COMMITS, compare=F_DIVERGED, gate=None, runs=F_MAIN, tie=True, **kw):
    """#930's PR with its check-site run created at `gate_at` and its phone-fit run at `pf_at`."""
    gr = dict(_run(45866316754, "pull_request", "completed", "success", gate_at, "claude/base-60-list", F_HEAD),
              check_suite_id=F_SUITE)
    # another run on the same head, in another check suite and created late: never the judged Gate's run
    other = dict(_run(45866999999, "pull_request", "completed", "success", "2026-11-26T17:50:00Z", "claude/base-60-list", F_HEAD),
                 check_suite_id=124099999999)
    pf = dict(_run(45866316762, "pull_request", "completed", "success", pf_at, "claude/base-60-list", F_HEAD),
              check_suite_id=124092601837)
    return Fake(pr=F_PR, gate=gate or _fgate(), runs=runs, commits=commits, compare=compare,
                gate_runs=[other, gr] if tie else [other], pf=[[pf]], **kw)


def fresh_cases(fresh=check_fresh):
    """(a'') MERGE-GUARD -> list of (name, ok, detail, plants): `plants` names the planted faults the case must catch."""
    out = []

    def case(name, ok, detail, *plants):
        out.append((name, bool(ok), detail, set(plants)))

    def go(fake, wait=0, **kw):
        c, logs = Clock(), []
        try:
            guard(fake, 930, wait=wait, sleep=c.sleep, clock=c, log=logs.append, fresh_check=fresh, **kw)
            return None, c
        except Refused as e:
            return str(e), c

    def read(fake, part):
        return [x for x in fake.calls if part in x[1]]

    said = ("main gained e72faba (LARGE-SCREEN-LAYER: the shared large-screen layer, piloted o) at 2026-11-26T17:35:08Z "
            "after this PR's %s: merge main into the branch and let the checks re-run (AGENTS.md:58)")
    gate_said = said % "Gate started at 2026-11-26T17:16:26Z"
    pf_said = said % "phone-fit run started at 2026-11-26T17:16:26Z"

    f = _ffake(F_BEFORE, F_BEFORE, compare={F_M: "ahead"}, tie=False)
    err, c = go(f)
    case("(a'') main's newest merge is an ancestor of the head (main merged in): passes on the compare alone, merges",
         err is None and len(f.merged()) == 1 and len(read(f, "/compare/%s...%s" % (F_M, F_HEAD))) == 1,
         err or "compare not read", "inverted")

    f = _ffake(F_BEFORE, F_BEFORE, commits=[_commit(F_HEAD, "the head itself", when=F_AFTER)] + F_COMMITS, compare={},
               runs=[_run(45869000000, "push", "completed", "success", F_AFTER, sha=F_HEAD)] + F_MAIN, tie=False)
    err, c = go(f)
    case("(a'') main's newest merge is the head commit itself: passes", err is None and len(f.merged()) == 1, err or "")

    f = _ffake(F_AFTER, F_AFTER, gate=_fgate(started="2026-11-26T18:01:00Z"))
    err, c = go(f)
    case("(a'') not an ancestor, both runs created after the merge (the merge ref held it): merges",
         err is None and len(f.merged()) == 1, err or "")

    f = _ffake("2026-11-26T16:50:00Z", "2026-11-26T16:50:00Z", commits=F_BOTS, runs=F_MAIN[1:],
               gate=_fgate(started="2026-11-26T17:11:00Z"))
    err, c = go(f)
    case("(a'') only bot skip-marker commits on main since the runs started (42270b2, 16:58:12Z): merges",
         err is None and len(f.merged()) == 1, err or "", "bots")

    f = _ffake(F_BEFORE, F_AFTER)
    err, c = go(f)
    case("(a'') not an ancestor, the Gate's run created before the merge, phone-fit after: refused, naming the merge and the Gate",
         err == gate_said and not f.merged(), err or "MERGED", "removed", "started_at", "inverted")

    f = _ffake(F_AFTER, F_BEFORE, gate=_fgate(started="2026-11-26T18:01:00Z"))
    err, c = go(f)
    case("(a'') the same with phone-fit created before the merge and the Gate after: refused, naming the phone-fit run",
         err == pf_said and not f.merged(), err or "MERGED", "removed", "inverted")

    f = _ffake(F_BEFORE, F_BEFORE)
    err, c = go(f)
    case("(a'') #930 as it stood (both runs from 17:16:26Z, #927 on main at 17:35:08Z, the Gate check started 17:37:25Z): refused",
         err == said % "Gate started at 2026-11-26T17:16:26Z and phone-fit run started at 2026-11-26T17:16:26Z"
         and not f.merged(), err or "MERGED", "removed", "started_at", "inverted")

    f = _ffake(F_BEFORE, F_AFTER, runs=[_run(45869999999, "push", "completed", "failure", "2026-11-26T17:36:00Z", sha=F_M)])
    err, c = go(f, override="Jon, 26 Nov 2026: merge it")
    case("(a'') refused under --override, at once, with the same message: no comment, no merge",
         err == gate_said and not f.merged() and not f.comments() and c.t == 0, err or "MERGED", "removed", "started_at", "inverted")

    f = _ffake(F_BEFORE, F_AFTER)
    err, c = go(f, wait=3600)
    case("(a'') refused under --wait 3600 at once (red, never waited on: a stale run never freshens)",
         err == gate_said and not f.merged() and c.t == 0 and c.slept == 0, err or "MERGED", "removed", "started_at", "inverted")

    f = _ffake(F_BEFORE, F_AFTER, gate=_fgate(started=None, status="in_progress", concl=None))
    err, c = go(f, wait=3600)
    case("(a'') a Gate still running on a stale run is refused at once, not waited for and then refused",
         err and gate_said in err and "not finished" in err and not f.merged() and c.t == 0, err or "MERGED", "removed", "inverted")

    f = _ffake(F_M_AT, F_AFTER, gate=_fgate(started="2026-11-26T18:01:00Z"))
    err, c = go(f)
    case("(a'') a run created in the same second as the merge is not after it: refused",
         err and "Gate started at 2026-11-26T17:35:08Z" in err and not f.merged(), err or "MERGED", "removed", "inverted")

    f = _ffake(F_AFTER, F_AFTER, gate=_fgate(suite=None))
    err, c = go(f)
    case("(a'') not an ancestor and the Gate check names no check suite: refused, never guessed from the check's own times",
         err and "names no check suite" in err and "cannot tell" in err and not f.merged(), err or "MERGED", "removed", "inverted")

    f = _ffake(F_AFTER, F_AFTER, tie=False)
    err, c = go(f)
    case("(a'') not an ancestor and no check-site run in the Gate check's suite: refused (a later run in another suite is not it)",
         err and "check suite 124092601822" in err and not f.merged(), err or "MERGED", "removed", "inverted")

    f = _ffake(F_AFTER, F_AFTER, faults=[["GET", "/compare/", None, E404]])
    err, c = go(f, wait=600)
    case("(a'') a compare that cannot be read (404): refused at once, never assumed in the branch",
         err and "HTTP 404" in err and "cannot tell" in err and not f.merged() and c.t == 0, err or "MERGED", "removed")

    f = _ffake(F_BEFORE, F_BEFORE, commits_error=True)
    err, c = go(f, override="Jon, 26 Nov 2026: merge it")
    case("(a'') --override with main's commits unreadable: refused (the override waives (b'), never this)",
         err and "could not be read" in err and "--override does not waive" in err and not f.merged() and not f.comments(),
         err or "MERGED", "removed")

    f = _ffake(F_BEFORE, F_BEFORE, commits_error=True)
    err, c = go(f)
    case("(a'') main's commits unreadable, no override: (b') refuses and (a'') adds nothing",
         err and "could not be read" in err and "--override does not waive" not in err and not f.merged(), err or "MERGED")

    f = _ffake(F_AFTER, F_AFTER, faults=[["GET", "/compare/", 4, E502]])
    c, logs = Clock(), []
    try:
        guard(with_retry(f, sleep=c.sleep), 930, wait=600, sleep=c.sleep, clock=c, log=logs.append, fresh_check=fresh)
        err = None
    except Refused as e:
        err = str(e)
    case("(a'') a 502 on the compare that outlasts the retries is waited on within --wait (never red or green), then merges",
         err is None and len(f.merged()) == 1 and any(l.startswith("waiting: GitHub HTTP 502 reading ") for l in logs),
         err or repr(logs))
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
    # PHONE-FIT-CHANGED-GAMES: with the phone-fit check removed, the red and not-started cases must notice
    mutant = {n for n, ok, _ in phone_fit_cases(phone_check=lambda api, pr: (True, "mutant: always green")) if not ok}
    sens = {n for n, _, _ in phone_fit_cases() if n.startswith("(a') a red phone-fit") or n.startswith("(a') no phone-fit run")}
    print("  %s  removing the phone-fit check fails %d of %d red and not-started cases" % (
        "PASS" if sens and sens <= mutant else "FAIL", len(sens & mutant), len(sens)))
    bad += not (sens and sens <= mutant)
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
    # MERGE-PR-ROBUST: the new cases pass, and each planted fault (the behaviour before, or a naive fix) is caught
    for name, ok, detail, _ in robust_cases():
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "   -> " + detail))
        bad += not ok
    plants = (("retry", "gh_api before (one try, every failure plain Refused)", dict(retry=old_api)),
              ("sizes", "run_jobs before (50 a page only)", dict(sizes=(JOBS_PER_PAGE,))),
              ("naive", "a naive retry (re-sends PUT and POST, retries a 4xx)", dict(retry=naive_retry)),
              ("head", "the guard before (no expected head: GitHub's stale head judged)", dict(use_head=False)),
              ("grace", "the watch before (no registration grace)", dict(grace=0)))
    want = robust_cases()
    for key, label, kw in plants:
        must = [n for n, _, _, ps in want if key in ps]
        failed = {n for n, ok, _, _ in robust_cases(**kw) if not ok}
        missed = [n for n in must if n not in failed]
        print("  %s  planted fault (%s): %d of %d case(s) catch it%s" % (
            "PASS" if not missed else "FAIL", label, len(must) - len(missed), len(must),
            "" if not missed else "; NOT caught by " + str(missed)))
        bad += bool(missed) or not must
    # MERGE-GUARD (a''): the cases pass, and each planted fault is caught
    for name, ok, detail, _ in fresh_cases():
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "   -> " + detail))
        bad += not ok
    plants = (("removed", "(a'') removed (always fresh)", lambda api, pr, waived=False: (True, "mutant: always fresh")),
              ("started_at", "the Gate check's own started_at in place of its run's created_at",
               lambda api, pr, waived=False: check_fresh(api, pr, waived, gate_when=lambda a, s, g: (g["id"], g.get("started_at")))),
              ("bots", "bot skip-marker commits counted as main's newest merge",
               lambda api, pr, waived=False: check_fresh(api, pr, waived, merge_of=head_literally)),
              ("inverted", "the ancestor test inverted",
               lambda api, pr, waived=False: check_fresh(api, pr, waived, inside=lambda a, b, h: not in_branch(a, b, h))))
    want = fresh_cases()
    for key, label, planted in plants:
        must = [n for n, _, _, ps in want if key in ps]
        failed = {n for n, ok, _, _ in fresh_cases(fresh=planted) if not ok}
        missed = [n for n in must if n not in failed]
        print("  %s  planted fault (%s): %d of %d case(s) catch it%s" % (
            "PASS" if not missed else "FAIL", label, len(must) - len(missed), len(must),
            "" if not missed else "; NOT caught by " + str(missed)))
        bad += bool(missed) or not must
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
    ap.add_argument("--head", metavar="SHA",
                    help="the commit expected at the PR's head (default: this checkout's HEAD when it is on the PR's "
                         "branch); until GitHub reports it nothing is judged, and --wait is the ceiling")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    note = lambda m: print(m, file=sys.stderr)   # progress to stderr: stdout carries the one line
    api = with_retry(gh_raw, log=note)
    if a.watch_main is not None:
        if a.number or a.override is not None or a.watch:
            ap.error("--watch-main takes no PR number, --override or --watch")
        sha = a.watch_main.strip().lower()
        if sha and not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            ap.error("--watch-main takes a commit sha (7 to 40 hex digits)")
        if a.head:
            ap.error("--watch-main takes no --head")
        code, line, to_stderr = watch_cmd(api, sha, a.wait, log=note)
        print(line, file=sys.stderr if to_stderr else sys.stdout)
        return code
    if not a.number:
        ap.error("a PR number is required")
    head = (a.head or "").strip().lower()
    if a.head is not None and not re.fullmatch(r"[0-9a-f]{7,40}", head):
        ap.error("--head takes a commit sha (7 to 40 hex digits)")
    return merge_and_report(api, a.number, a.override, a.wait, a.watch, note=note, head=head or None, local=git_local)


if __name__ == "__main__":
    sys.exit(main())
