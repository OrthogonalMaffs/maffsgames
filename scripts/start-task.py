#!/usr/bin/env python3
"""Create one new task worktree. Python stdlib only; no cleanup or rollback.

    python -X utf8 scripts/start-task.py <task> --agent codex|claude
    python -X utf8 scripts/start-task.py --selftest

Run a current copy (also works from a temporary file) with the primary or one of
its worktrees as cwd. Fetch refreshes origin refs; no existing worktree, local
branch or working file is changed. All checks precede worktree creation. A failed
creation/verification is reported and left for inspection, never removed/reset.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from unittest.mock import patch

PRIMARY = Path(r"E:\jon\maffsgames-new-clone")
REPO = "repos/OrthogonalMaffs/maffsgames"


class Refused(Exception):
    pass


def run(args, cwd):
    return subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def checked(args, cwd):
    result = run(args, cwd)
    if result.returncode:
        raise Refused("%s failed: %s" % (" ".join(map(str, args)),
                                        (result.stderr or result.stdout).strip()))
    return result.stdout.strip()


def api(path, cwd):
    try:
        return json.loads(checked(["gh", "api", "--method", "GET", path], cwd))
    except ValueError as exc:
        raise Refused("GitHub REST returned invalid JSON") from exc


def green_main(get):
    # Filter at the endpoint so busy PR traffic cannot hide the latest main run.
    runs = []
    for event in ("push", "workflow_dispatch"):
        data = get(REPO + "/actions/workflows/check-site.yml/runs?branch=main&event="
                   + event + "&per_page=1")
        runs.extend(data["workflow_runs"])
    if not runs:
        raise Refused("no full check-site run on main (push or manual)")
    latest = max(runs, key=lambda item: item["id"])
    if latest["status"] != "completed" or latest["conclusion"] != "success":
        raise Refused("main's latest full check-site run %s is %s/%s" %
                      (latest["id"], latest["status"], latest["conclusion"]))
    jobs, page = [], 1
    while True:
        data = get(REPO + "/actions/runs/%s/jobs?filter=latest&per_page=50&page=%d"
                   % (latest["id"], page))
        batch, total = data["jobs"], data["total_count"]
        jobs.extend(batch)
        if len(jobs) >= total:
            break
        if not batch:
            raise Refused("main run's jobs list is incomplete")
        page += 1
    if not jobs:
        raise Refused("main run lists no jobs")
    for job in jobs:
        if job["status"] != "completed" or job["conclusion"] not in (
                "success", "skipped", "neutral"):
            raise Refused("main run job %s is %s/%s" %
                          (job["name"], job["status"], job["conclusion"]))
    return "main full check-site run %s green (%d finished jobs)" % (latest["id"], len(jobs))


def has_ref(primary, ref):
    result = run(["git", "show-ref", "--verify", "--quiet", ref], primary)
    if result.returncode not in (0, 1):
        raise Refused("cannot check ref %s: %s" % (ref, result.stderr.strip()))
    return result.returncode == 0


def start(task, agent, cwd=None, primary=PRIMARY, get=None, log=print):
    """Internal dependency injection is for temporary-repo tests, not CLI overrides."""
    if not re.fullmatch(r"[a-z0-9-]+", task):
        raise Refused("task must match ^[a-z0-9-]+$")
    if agent not in ("codex", "claude"):
        raise Refused("agent must be codex or claude")
    cwd = Path(cwd or Path.cwd())
    common = Path(checked(["git", "rev-parse", "--git-common-dir"], cwd))
    common = (cwd / common).resolve()
    primary = Path(primary).resolve()
    if os.path.normcase(str(common)) != os.path.normcase(str(primary / ".git")):
        raise Refused("wrong primary: common git directory is %s; expected %s" %
                      (common, primary / ".git"))
    branch = agent + "/" + task
    target = primary.parent / ("mg-" + task)
    # Refuse existing paths (including broken symlinks) before any network call.
    if os.path.lexists(target):
        raise Refused("target folder already exists: %s" % target)
    if has_ref(primary, "refs/heads/" + branch):
        raise Refused("local branch already exists: " + branch)
    checked(["git", "fetch", "origin"], primary)
    if has_ref(primary, "refs/remotes/origin/" + branch):
        raise Refused("remote branch already exists: " + branch)
    remote = checked(["git", "ls-remote", "--heads", "origin", "refs/heads/" + branch], primary)
    if remote:
        raise Refused("remote branch already exists: " + branch)
    base = checked(["git", "rev-parse", "--verify", "refs/remotes/origin/main^{commit}"], primary)
    log(green_main(get or (lambda path: api(path, primary))))
    # Recheck local preconditions immediately before the only creation command.
    if os.path.lexists(target) or has_ref(primary, "refs/heads/" + branch):
        raise Refused("target or local branch appeared during checks; left alone")
    checked(["git", "-C", primary, "worktree", "add", "-b", branch, target, "origin/main"], primary)
    if checked(["git", "status", "--porcelain"], target):
        raise Refused("new worktree is dirty; left for inspection: %s" % target)
    head = checked(["git", "rev-parse", "HEAD"], target)
    origin = checked(["git", "rev-parse", "origin/main"], target)
    if head != base or head != origin:
        raise Refused("new HEAD differs from checked origin/main; left for inspection: %s" % target)
    log("Created %s at %s" % (branch, head))
    log("Path: %s" % target)
    log('Launch: codex -C "%s"' % target if agent == "codex" else
        "Launch (PowerShell): Set-Location -LiteralPath '%s'; claude" % target)
    return target


def selftest():
    """Real git repos; only GitHub REST and deliberately failed commands stubbed."""
    failures = []

    def check(name, condition):
        print(("PASS: " if condition else "FAIL: ") + name)
        if not condition:
            failures.append(name)

    good = {"id": 10, "status": "completed", "conclusion": "success"}
    job = {"name": "Gate", "status": "completed", "conclusion": "success"}

    def fixture(runs=None, jobs=None, error=False):
        def get(path):
            if error:
                raise Refused("REST unavailable")
            if "/jobs?" in path:
                entries = [job] if jobs is None else jobs
                page = int(path.rsplit("page=", 1)[1])
                return {"total_count": len(entries), "jobs": entries[(page-1)*50:page*50]}
            return {"workflow_runs": ([good] if runs is None else runs)
                    if "event=push" in path else []}
        return get

    with tempfile.TemporaryDirectory(prefix="start-task-") as td:
        root = Path(td)
        primary, remote = root / "primary", root / "origin.git"
        primary.mkdir()

        def git(*args):
            return checked(["git", *args], primary)

        checked(["git", "init", "--bare", remote], root)
        git("init", "-b", "main")
        git("config", "user.name", "Start task selftest")
        git("config", "user.email", "selftest@example.invalid")
        git("-c", "core.hooksPath=", "commit", "--allow-empty", "-m", "base")
        git("remote", "add", "origin", str(remote))
        git("push", "-u", "origin", "main")

        def snapshot():
            # Fetch may refresh FETCH_HEAD/remote refs, but refusal creates no
            # task branch/folder and changes no existing working file/worktree.
            return (git("for-each-ref", "--format=%(refname):%(objectname)", "refs/heads"),
                    git("worktree", "list", "--porcelain"), git("status", "--porcelain"),
                    sorted(p.name for p in root.iterdir()))

        def refuses(name, task="refuse", get=None, reason=None, cwd=None):
            before = snapshot()
            try:
                start(task, "codex", cwd or primary, primary, get or fixture(), log=lambda _: None)
                check(name, False)
            except Refused as exc:
                check(name + " (" + str(exc) + ")",
                      before == snapshot() and (reason is None or reason in str(exc)))

        for task in ("", "../escape", "UPPER", "two words", "a/b", "a\n"):
            refuses("invalid task %r refuses unchanged" % task, task, reason="task must match")
        wrong = root / "wrong"
        wrong.mkdir()
        checked(["git", "init", wrong], root)
        refuses("wrong primary refuses unchanged", cwd=wrong, reason="wrong primary")
        git("branch", "codex/local")
        refuses("local branch refuses unchanged", "local", reason="local branch")
        git("push", "origin", "main:refs/heads/codex/remote")
        refuses("remote branch refuses unchanged", "remote", reason="remote branch")
        (root / "mg-folder").mkdir()
        refuses("existing folder refuses unchanged", "folder", reason="target folder")
        original_run = run

        def fetch_failure(args, cwd):
            if list(args) == ["git", "fetch", "origin"]:
                return subprocess.CompletedProcess(args, 1, "", "planted fetch failure")
            return original_run(args, cwd)

        with patch.object(sys.modules[__name__], "run", fetch_failure):
            refuses("fetch failure refuses unchanged", reason="planted fetch failure")
        refuses("missing main run refuses unchanged", get=fixture(runs=[]), reason="no full")
        for conclusion in ("failure", "cancelled", "timed_out"):
            bad = dict(good, conclusion=conclusion)
            refuses("%s main refuses unchanged" % conclusion, get=fixture(runs=[bad]), reason="latest full")
        refuses("unfinished latest main refuses unchanged",
                get=fixture(runs=[good, dict(good, id=11, status="in_progress", conclusion=None)]),
                reason="in_progress")
        refuses("REST error refuses unchanged", get=fixture(error=True), reason="REST unavailable")
        refuses("empty jobs refuses unchanged", get=fixture(jobs=[]), reason="no jobs")
        refuses("unfinished job refuses unchanged", get=fixture(jobs=[dict(job, status="queued", conclusion=None)]), reason="queued")
        refuses("failed second page job refuses unchanged",
                get=fixture(jobs=[job] * 50 + [dict(job, conclusion="failure")]), reason="failure")
        # A newer manual run must beat a green push, even if it is red.
        def manual_red(path):
            if "event=workflow_dispatch" in path:
                return {"workflow_runs": [dict(good, id=12, conclusion="failure")]}
            return fixture()(path)
        refuses("newer red manual run refuses unchanged", get=manual_red, reason="failure")
        # Both agents use the same checked path and their own branch prefix.
        for agent in ("codex", "claude"):
            task = "success-" + agent
            target = start(task, agent, primary, primary, fixture(jobs=[job] * 51), log=print)
            check(agent + " success: clean, HEAD == origin/main, branch and path correct",
                  target == root / ("mg-" + task)
                  and not checked(["git", "status", "--porcelain"], target)
                  and checked(["git", "branch", "--show-current"], target) == agent + "/" + task
                  and checked(["git", "rev-parse", "HEAD"], target) == git("rev-parse", "origin/main"))
        # Calling from a linked worktree still resolves the one primary.
        linked = root / "mg-success-codex"
        third = start("linked", "codex", linked, primary, fixture(), log=lambda _: None)
        check("linked worktree resolves common primary", third.exists())
        # TemporaryDirectory owns these repos; the production helper never deletes.
    print("selftest: " + ("FAIL (%d)" % len(failures) if failures else "PASS"))
    return bool(failures)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="?")
    parser.add_argument("--agent", choices=("codex", "claude"))
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        if args.task is not None or args.agent is not None:
            parser.error("--selftest takes no task or agent")
        return selftest()
    if args.task is None or args.agent is None:
        parser.error("task and --agent are required")
    try:
        start(args.task, args.agent)
    except (Refused, OSError, ValueError, KeyError, TypeError) as exc:
        print("REFUSED: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
