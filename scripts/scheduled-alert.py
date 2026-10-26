#!/usr/bin/env python3
"""Make a failed or silent scheduled job visible: a GitHub issue, opened or updated by itself and closed on the next success.

Contract ANSWER-COUNTS-STALE (26 Oct 2026; canon 7.5.5). The answer-counts job failed on every scheduled run from 25 Oct and
nobody knew for two days, because a failed scheduled run only turns a badge red. Now .github/workflows/scheduled-watch.yml runs
this script when answer-counts or the weekly check-site finishes, and once a day:

    run        a finished scheduled run: failed -> open (or update) the issue "Scheduled workflow failing: <name>", labelled
               `scheduled-failure`, naming the failing step with an excerpt of its log; succeeded -> close that issue.
               Only answer-counts (any trigger) and check-site (the weekly schedule) are watched; a check-site push or pull
               request is merge-pr.py's business, not this.
    freshness  daily: the committed schools/assets/answer-counts.json older than 24 hours (the daily job has failed, or never
               fired) -> open (or update) "answer-counts.json is stale: no figure committed in 24 hours"; fresh -> close it.
               This is what catches a schedule that GitHub dropped, which no failed run reports.
    simulate   a test: <name> with a failure or a success, to watch an issue open and close (workflow_dispatch).

Nothing leaves GitHub: the issue is in this repository, written with the workflow's own token (permissions: issues write,
actions read). GitHub's own notification (and the @mention in the body) is how Jon sees it without looking.

    python scripts/scheduled-alert.py run --repo O/R --name answer-counts --conclusion failure --event schedule --run-id 1 --url U
    python scripts/scheduled-alert.py freshness --repo O/R
    python scripts/scheduled-alert.py simulate --repo O/R --name test-alert --conclusion failure
    python scripts/scheduled-alert.py --selftest
"""
import argparse, datetime as dt, importlib.util, json, os, pathlib, re, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "scheduled-failure"
OWNER_MENTION = "@OrthogonalMaffs"
WATCHED = {"answer-counts": None, "check-site": {"schedule"}}      # workflow -> the events that count (None: any)
STALE_TITLE = "answer-counts.json is stale: no figure committed in 24 hours"


def title_for(name):
    return "Scheduled workflow failing: %s" % name


def _fetch_module():
    spec = importlib.util.spec_from_file_location("fetch_counts", os.path.join(HERE, "fetch-answer-counts.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ the GitHub API (REST only)
def gh_api(method, path, data=None):
    """One REST call with the gh CLI (GH_TOKEN is the workflow's token); JSON back, or the raw text (job logs)."""
    cmd = ["gh", "api", "-X", method, path]
    if data is not None:
        cmd += ["--input", "-"]
    out = subprocess.run(cmd, input=json.dumps(data) if data is not None else None, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError("gh api %s %s: %s" % (method, path, (out.stderr or out.stdout).strip()[:300]))
    try:
        return json.loads(out.stdout) if out.stdout.strip() else None
    except ValueError:
        return out.stdout


class Alerts:
    """The issue logic, against any `api(method, path, data=None)`; `bug` plants a fault for the selftest."""

    def __init__(self, api, repo, bug=None):
        self.api, self.repo, self.bug = api, repo, bug

    def _label(self):
        try:
            self.api("POST", "/repos/%s/labels" % self.repo, {"name": LABEL, "color": "b60205",
                                                              "description": "A scheduled workflow failed or went quiet"})
        except RuntimeError:
            pass                                    # it exists already (422)

    def _open_issue(self, title):
        page = 1
        while True:
            items = self.api("GET", "/repos/%s/issues?labels=%s&state=open&per_page=100&page=%d" % (self.repo, LABEL, page)) or []
            for i in items:
                if "pull_request" not in i and i.get("title") == title:
                    return i
            if len(items) < 100:
                return None
            page += 1

    def failing(self, title, body):
        """Open the issue, or add a comment to the one already open. Returns ('opened'|'updated', number)."""
        if self.bug == "never_opens":
            return ("opened", 0)
        found = None if self.bug == "duplicates" else self._open_issue(title)
        if found:
            self.api("POST", "/repos/%s/issues/%d/comments" % (self.repo, found["number"]), {"body": body})
            return ("updated", found["number"])
        self._label()
        made = self.api("POST", "/repos/%s/issues" % self.repo, {"title": title, "body": OWNER_MENTION + "\n\n" + body, "labels": [LABEL]})
        return ("opened", made["number"])

    def recovered(self, title, note):
        """Close the open issue with this title, if any. Returns its number or None."""
        if self.bug == "never_closes":
            return None
        found = self._open_issue(title) if self.bug != "closes_all" else None
        if self.bug == "closes_all":
            items = self.api("GET", "/repos/%s/issues?labels=%s&state=open&per_page=100" % (self.repo, LABEL)) or []
            found = items[0] if items else None
        if not found:
            return None
        self.api("POST", "/repos/%s/issues/%d/comments" % (self.repo, found["number"]), {"body": note})
        self.api("PATCH", "/repos/%s/issues/%d" % (self.repo, found["number"]), {"state": "closed", "state_reason": "completed"})
        return found["number"]

    # ---- a finished run
    def run_finished(self, name, conclusion, event, run_id, url, details=None):
        events = WATCHED.get(name, "unwatched")
        if events == "unwatched" or (events is not None and event not in events):
            return ("ignored", None)
        if conclusion == "failure":
            step, excerpt = details if details else self.failure_details(run_id)
            body = ("The scheduled workflow **%s** failed (%s event).\n\nRun: %s\n\nFailing step: **%s**\n\n```\n%s\n```\n\n"
                    "This issue closes itself when the workflow next succeeds." % (name, event, url, step, excerpt))
            return self.failing(title_for(name), body)
        if conclusion == "success":
            n = self.recovered(title_for(name), "%s succeeded again: %s. Closing." % (name, url))
            return ("closed", n) if n else ("nothing open", None)
        return ("ignored", None)                    # cancelled, skipped, neutral: not a verdict

    def failure_details(self, run_id):
        """The failing step of a run and the log lines that say why."""
        jobs = self.api("GET", "/repos/%s/actions/runs/%s/jobs" % (self.repo, run_id)) or {}
        for j in jobs.get("jobs", []):
            for st in j.get("steps", []):
                if st.get("conclusion") == "failure":
                    text = ""
                    try:
                        text = self.api("GET", "/repos/%s/actions/jobs/%s/logs" % (self.repo, j["id"])) or ""
                    except RuntimeError:
                        pass
                    lines = [re.sub(r"^\S+Z\s", "", l).strip() for l in str(text).splitlines()
                             if re.search(r"FAIL|##\[error\]|Traceback|Error", l)]
                    return ("%s: %s" % (j.get("name"), st.get("name")), "\n".join(x[:300] for x in lines[:6]) or "(no log lines matched)")
        return ("(no failing step found)", "")

    # ---- the daily look at the committed file
    def freshness(self, obj, now_utc=None):
        f = _fetch_module()
        faults = f.stale_faults(obj, now_utc)
        if faults:
            runs = ""
            try:
                got = self.api("GET", "/repos/%s/actions/workflows/answer-counts.yml/runs?per_page=5" % self.repo) or {}
                runs = "\n".join("- %s %s %s %s" % (r.get("created_at"), r.get("event"), r.get("conclusion"), r.get("html_url"))
                                 for r in got.get("workflow_runs", []))
            except RuntimeError:
                pass
            body = ("%s\n\nThe daily answer-counts job commits a fresh figure three times a day; none has landed in 24 hours. "
                    "Either its runs are failing (see the `Scheduled workflow failing: answer-counts` issue) or GitHub did not start them.\n\n"
                    "Latest answer-counts runs:\n%s\n\nThis issue closes itself when a fresh figure is committed." % ("; ".join(faults), runs or "(none listed)"))
            return self.failing(STALE_TITLE, body)
        n = self.recovered(STALE_TITLE, "A fresh figure is committed (as_of %s). Closing." % obj.get("as_of"))
        return ("closed", n) if n else ("nothing open", None)


# ------------------------------------------------------------------------------------------------ self-test
class FakeGitHub:
    """Just enough of the issues API to see an issue opened, updated and closed."""

    def __init__(self):
        self.issues, self.labels, self.next = [], set(), 1
        self.log = []

    def __call__(self, method, path, data=None):
        self.log.append((method, path))
        m = re.match(r"/repos/[^/]+/[^/]+(/.*)", path)
        p = m.group(1)
        if p == "/labels" and method == "POST":
            if data["name"] in self.labels:
                raise RuntimeError("422 already exists")
            self.labels.add(data["name"])
            return {}
        if p.startswith("/issues?") and method == "GET":
            return [i for i in self.issues if i["state"] == "open" and LABEL in i["labels"]]
        if p == "/issues" and method == "POST":
            i = {"number": self.next, "title": data["title"], "body": data["body"], "labels": data["labels"], "state": "open", "comments": []}
            self.next += 1
            self.issues.append(i)
            return i
        mm = re.match(r"/issues/(\d+)/comments", p)
        if mm and method == "POST":
            [i for i in self.issues if i["number"] == int(mm.group(1))][0]["comments"].append(data["body"])
            return {}
        mm = re.match(r"/issues/(\d+)$", p)
        if mm and method == "PATCH":
            [i for i in self.issues if i["number"] == int(mm.group(1))][0]["state"] = data["state"]
            return {}
        if re.match(r"/actions/runs/\d+/jobs$", p):
            return {"jobs": [{"id": 9, "name": "Fetch and commit the answer counts",
                              "steps": [{"name": "Checkout", "conclusion": "success"}, {"name": "Fetch, validate, commit", "conclusion": "failure"}]}]}
        if re.match(r"/actions/jobs/\d+/logs$", p):
            return ("2026-10-26T11:31:29.0Z noise\n2026-10-26T11:31:32.0Z FAIL as_of '2026-10-26T11:31:31Z' is not an ISO time with an offset\n"
                    "2026-10-26T11:31:32.1Z ##[error]Process completed with exit code 1.\n")
        if re.match(r"/actions/workflows/.*/runs", p):
            return {"workflow_runs": [{"created_at": "2026-10-26T11:31:22Z", "event": "schedule", "conclusion": "failure", "html_url": "https://x/run/1"}]}
        raise AssertionError("unexpected call %s %s" % (method, path))


def _cases(bug=None):
    """[(name, passed, detail)] for the alert logic; `bug` plants a fault in it."""
    out = []

    def ok(name, cond, detail=""):
        out.append((name, bool(cond), "" if cond else str(detail)))
    gh = FakeGitHub()
    a = Alerts(gh, "O/R", bug)
    URL = "https://github.com/O/R/actions/runs/1"
    open_ = lambda: [i for i in gh.issues if i["state"] == "open"]
    r = a.run_finished("answer-counts", "failure", "schedule", 1, URL)
    ok("a failed scheduled run opens an issue", r[0] == "opened" and len(open_()) == 1, r)
    iss = open_()[0] if open_() else {"title": "", "body": "", "labels": []}
    ok("the issue is labelled and names the workflow", iss["title"] == "Scheduled workflow failing: answer-counts" and LABEL in iss["labels"], iss["title"])
    ok("the issue names the failing step and the log line that says why",
       "Fetch and commit the answer counts: Fetch, validate, commit" in iss["body"] and "is not an ISO time with an offset" in iss["body"], iss["body"])
    ok("the issue @mentions the owner and links the run", OWNER_MENTION in iss["body"] and URL in iss["body"], iss["body"])
    r = a.run_finished("answer-counts", "failure", "schedule", 2, URL)
    ok("a second failure updates the same issue, never a second one", r[0] == "updated" and len(open_()) == 1, "%s open=%d" % (r, len(open_())))
    r = a.run_finished("check-site", "failure", "push", 3, URL)
    ok("a check-site failure on a push is not this watch's business", r[0] == "ignored" and len(open_()) == 1, r)
    r = a.run_finished("check-site", "failure", "schedule", 4, URL)
    ok("a failed weekly check-site opens its own issue", len(open_()) == 2, [i["title"] for i in open_()])
    r = a.run_finished("answer-counts", "cancelled", "schedule", 5, URL)
    ok("a cancelled run is no verdict", r[0] == "ignored" and len(open_()) == 2, r)
    r = a.run_finished("check-site", "success", "push", 6, URL)
    ok("a check-site push success does not close the weekly issue", len(open_()) == 2, [i["title"] for i in open_()])
    r = a.run_finished("answer-counts", "success", "schedule", 7, URL)
    ok("the next success closes that workflow's issue", r[0] == "closed" and [i["title"] for i in open_()] == ["Scheduled workflow failing: check-site"], [i["title"] for i in open_()])
    ok("and leaves the other workflow's issue open", len(open_()) == 1, len(open_()))
    r = a.run_finished("answer-counts", "success", "schedule", 8, URL)
    ok("a success with nothing open does nothing", r[0] == "nothing open", r)
    # freshness: the committed file's age
    now = dt.datetime(2026, 10, 26, 17, 30, tzinfo=dt.timezone.utc)
    stale = {"as_of": "2026-10-24T20:46:04+01:00"}
    fresh = {"as_of": "2026-10-26T11:31:31Z"}
    r = a.freshness(stale, now)
    ok("a stale file opens the staleness issue, naming the latest runs", r[0] == "opened" and any(i["title"] == STALE_TITLE and "hours old" in i["body"] and "https://x/run/1" in i["body"] for i in open_()), r)
    r = a.freshness(stale, now)
    ok("a stale file on the next day updates it, no second issue", r[0] == "updated" and sum(1 for i in open_() if i["title"] == STALE_TITLE) == 1, r)
    r = a.freshness(fresh, now)
    ok("a fresh file (Z, 6 hours old) closes the staleness issue", r[0] == "closed" and not any(i["title"] == STALE_TITLE for i in open_()), r)
    r = a.freshness({"as_of": "yesterday"}, now)
    ok("an unreadable as_of counts as stale", r[0] == "opened", r)
    return out


def selftest():
    bad = []
    for name, good, detail in _cases():
        print("  %s  %s%s" % ("PASS" if good else "FAIL", name, "" if good else "  <- " + detail))
        if not good:
            bad.append(name)
    for bug, want in (("never_opens", "a failed scheduled run opens an issue"), ("duplicates", "never a second one"),
                      ("never_closes", "the next success closes"), ("closes_all", "leaves the other workflow's issue open")):
        try:
            got = [n for n, g, _ in _cases(bug) if not g]
        except Exception as exc:                    # a planted fault that breaks the run outright is caught too
            got = ["crashed: %s" % exc]
        hit = bool(got)                    # some case fails (`want` names the one meant to)
        print("  %s  planted: %-12s %s" % ("PASS" if hit else "FAIL", bug, got[0] if got else "(no case failed)"))
        if not hit:
            bad.append("planted " + bug)
    print("selftest: %s" % ("FAILED: " + ", ".join(bad) if bad else "PASS"))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run")
    for k in ("repo", "name", "conclusion", "event", "run-id", "url"):
        r.add_argument("--" + k, required=True)
    fr = sub.add_parser("freshness")
    fr.add_argument("--repo", required=True)
    sm = sub.add_parser("simulate")
    sm.add_argument("--repo", required=True)
    sm.add_argument("--name", default="test-alert")
    sm.add_argument("--conclusion", choices=["failure", "success"], required=True)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "run":
        res = Alerts(gh_api, a.repo).run_finished(a.name, a.conclusion, a.event, a.run_id, a.url)
    elif a.cmd == "freshness":
        res = Alerts(gh_api, a.repo).freshness(json.loads((BASE / "schools" / "assets" / "answer-counts.json").read_text(encoding="utf-8")))
    elif a.cmd == "simulate":
        al = Alerts(gh_api, a.repo)
        title = title_for(a.name)
        if a.conclusion == "failure":
            res = al.failing(title, "A simulated failure of **%s** (a test of the alert route: workflow_dispatch of scheduled-watch). "
                                    "Run the same workflow with a success to see this close." % a.name)
        else:
            n = al.recovered(title, "A simulated success of %s. Closing." % a.name)
            res = ("closed", n) if n else ("nothing open", None)
    else:
        ap.print_help()
        return 2
    print("scheduled-alert: %s %s" % res)
    return 0


if __name__ == "__main__":
    sys.exit(main())
