#!/usr/bin/env python3
# ci-line: End-of-task helper (end-task.py: a squash-merged branch is removed; an unmerged branch, an extra local commit and a dirty worktree each refuse; gh stubbed) | --selftest
# ci-deps: scripts/bg.py
"""Remove a finished task's worktree and local branch, only when that is safe (RULINGS-12OCT, 12 Oct 2026).

    python scripts/end-task.py <branch>        # after the PR is merged and main's run is reported
    python scripts/end-task.py --selftest

This repo squash-merges every PR, so a merged branch's tip is never an ancestor of main and `git branch -d`
refuses. This helper checks instead, then deletes. It deletes only when ALL hold:
  1. the branch's PR is MERGED (REST: gh api repos/{owner}/{repo}/pulls?head=<owner>:<branch>&state=all; no GraphQL);
  2. the local tip equals the PR's headRefOid (nothing local that was not in the PR);
  3. the branch's worktree, if it has one, is clean (git status --porcelain is empty).
Then, first, it stops what the session registered through scripts/bg.py (<worktree>/.claude/pids.json: each process
and its children, taskkill /T on Windows, the process group on POSIX) and reports any other process whose command line
holds the worktree path without killing it (contract BG-LAUNCHER). Then: git worktree remove (never --force),
git branch -D, git worktree prune. Otherwise it names the failed
condition and deletes nothing. It never touches a remote branch (GitHub deletes a merged head branch itself).
"""
import json, os, signal, subprocess, sys, tempfile, time


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def real(p):
    return os.path.normcase(os.path.realpath(p))


# --- background processes (contract BG-LAUNCHER) --------------------------------------------------------------------
# scripts/bg.py registers a session's background servers in <worktree>/.claude/pids.json. This file runs from a copy
# in /tmp (so it cannot import bg.py); the registry format is the contract between them, and bg.py's --selftest
# runs the two together.
WIN = os.name == "nt"


def registry(wt):
    try:
        with open(os.path.join(wt, ".claude", "pids.json"), encoding="utf-8", newline="") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def create_time(pid):
    """The OS's creation time for a live pid (None if gone), in bg.py's format: identifies the process, not the number."""
    if WIN:
        ps = "$p=Get-CimInstance Win32_Process -Filter 'ProcessId=%d'; if($p){$p.CreationDate.ToUniversalTime().ToString('o')}" % pid
        r = run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps])
    else:
        try:
            r = run(["ps", "-p", str(pid), "-o", "stat=,lstart="])
            out = r.stdout.strip()
            return None if not out or out.startswith("Z") else out.split(None, 1)[-1]   # a zombie is already dead
        except (FileNotFoundError, OSError):                       # a container without procps: /proc/<pid>/stat, state then start ticks
            try:
                with open("/proc/%d/stat" % pid) as fh:
                    f = fh.read().rsplit(")", 1)[1].split()
                return None if f[0] == "Z" else f[19]
            except (OSError, IndexError):
                return None
    return r.stdout.strip() or None


def alive(pid, create=None):
    """Whether pid is running (and, given its recorded creation time, is still the same process)."""
    now = create_time(pid)
    return bool(now) and (create is None or now == create)


def kill_tree(pid):
    """Stop pid and its children: taskkill /T /F on Windows (the process is one this session registered), the process
    group on POSIX (bg.py starts each in its own session): TERM, then KILL after a grace period."""
    if WIN:
        run(["taskkill", "/PID", str(pid), "/T", "/F"])
        return
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(os.getpgid(pid), sig)
        except (ProcessLookupError, PermissionError):
            return
        for _ in range(20):
            if not alive(pid):
                return
            time.sleep(0.1)


def stop_registered(wt):
    """Stop every process registered under wt, report each, clear the registry. Returns [(pid, cmd, what happened)]."""
    done = []
    for e in registry(wt):
        pid, create = e.get("pid"), e.get("create")
        if not isinstance(pid, int):
            continue
        if not alive(pid, create):
            done.append((pid, e.get("cmd"), "already gone (or the pid was reused: left alone)"))
            continue
        kill_tree(pid)
        for _ in range(30):
            if not alive(pid, create):
                break
            time.sleep(0.1)
        done.append((pid, e.get("cmd"), "stopped" if not alive(pid, create) else "STILL RUNNING"))
    reg = os.path.join(wt, ".claude", "pids.json")
    if not any(d[2] == "STILL RUNNING" for d in done):
        try:
            os.remove(reg)
            os.rmdir(os.path.dirname(reg))                  # only if nothing else is in .claude
        except OSError:
            pass
    return done


def unregistered(wt, exclude=()):
    """[(pid, command line)] of running processes whose command line holds the worktree path and that are not registered.
    Reported only, never killed. The process list is read whole and filtered here, so this scan's own command line
    does not hold the path."""
    if WIN:
        ps = "Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }"
        out = run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps]).stdout or ""
    else:
        try:
            out = run(["ps", "-eo", "pid=,args="]).stdout
        except OSError:                                   # a container without procps: read /proc directly
            rows = []
            for d in os.listdir("/proc"):
                if d.isdigit():
                    try:
                        with open("/proc/%s/cmdline" % d, "rb") as fh:
                            rows.append("%s %s" % (d, fh.read().replace(b"\x00", b" ").decode("utf-8", "replace")))
                    except OSError:
                        pass
            out = "\n".join(rows)
    needle = real(wt).replace("\\", "/").lower()
    mine = {os.getpid()} | set(exclude)
    registered = {e.get("pid") for e in registry(wt)}
    found = []
    for line in out.splitlines():
        pid_s, _, cmd = line.strip().replace("\t", " ").partition(" ")
        if not pid_s.isdigit() or not cmd:
            continue
        if int(pid_s) in mine or int(pid_s) in registered:
            continue
        if needle in cmd.replace("\\", "/").lower():
            found.append((int(pid_s), cmd.strip()[:200]))
    return found


def pr_from_rest(pulls):
    """{state, headRefOid, mergeCommit} of the newest PR in a REST pulls list (state MERGED, CLOSED or OPEN), or None.
    The REST list has no `merged` flag: a PR is merged when merged_at is set."""
    if not isinstance(pulls, list) or not pulls:
        return None
    pr = max((x for x in pulls if isinstance(x, dict) and isinstance(x.get("number"), int)),
             key=lambda x: x["number"], default=None)
    if pr is None or not isinstance(pr.get("head"), dict) or not pr["head"].get("sha"):
        return None
    state = "MERGED" if pr.get("merged_at") else ("OPEN" if pr.get("state") == "open" else "CLOSED")
    return {"state": state, "headRefOid": pr["head"]["sha"], "mergeCommit": {"oid": pr.get("merge_commit_sha")}}


def gh_pr(branch, cwd=None):
    """The PR's {state, headRefOid, mergeCommit} through the REST API (`gh api`; GraphQL is refused in Claude Code
    sessions), or None if gh cannot say."""
    r = run(["gh", "api", "repos/{owner}/{repo}/pulls?head={owner}:%s&state=all&per_page=30" % branch], cwd)
    if r.returncode != 0:
        return None
    try:
        return pr_from_rest(json.loads(r.stdout))
    except ValueError:
        return None


def worktrees(repo):
    """[(path, branch or None)] from git worktree list --porcelain; the first is the primary checkout."""
    out, cur = [], None
    for line in run(["git", "worktree", "list", "--porcelain"], repo).stdout.splitlines():
        if line.startswith("worktree "):
            cur = [line[9:], None]
            out.append(cur)
        elif line.startswith("branch ") and cur:
            cur[1] = line[7:].replace("refs/heads/", "", 1)
    return [tuple(w) for w in out]


def plan(branch, repo, gh=gh_pr, cwd=None):
    """(None, worktree path or None) if safe to remove, else (the failed condition, None)."""
    tip = run(["git", "rev-parse", "--verify", "-q", "refs/heads/" + branch], repo)
    if tip.returncode != 0:
        return "no local branch %s" % branch, None
    tip = tip.stdout.strip()
    pr = gh(branch)
    if not pr or "state" not in pr or "headRefOid" not in pr:
        return "gh cannot report a PR for %s (state and headRefOid)" % branch, None
    if pr["state"] != "MERGED":
        return "the PR for %s is %s, not MERGED" % (branch, pr["state"]), None
    if pr["headRefOid"] != tip:
        return ("the local tip %s is not the PR's head %s: there is a local commit the PR does not have"
                % (tip[:9], pr["headRefOid"][:9])), None
    wts = worktrees(repo)
    wt = next((p for p, b in wts if b == branch), None)
    if wt:
        if real(wt) == real(wts[0][0]):
            return "%s is checked out in the primary checkout; switch it to another branch first" % branch, None
        here = real(cwd or os.getcwd())
        if here == real(wt) or here.startswith(real(wt) + os.sep):
            return "you are inside the worktree %s; run this from the primary checkout" % wt, None
        dirty = run(["git", "status", "--porcelain"], wt).stdout.strip()
        if dirty:
            return "the worktree %s is not clean:\n%s" % (wt, dirty), None
    return None, wt


def end_task(branch, repo, gh=gh_pr, cwd=None):
    fail, wt = plan(branch, repo, gh, cwd)
    if fail:
        print("REFUSED: %s\nNothing was deleted." % fail)
        return 1
    if wt:                                     # the checks passed: stop what the session registered before removing its folder
        for pid, cmd, what in stop_registered(wt):
            print("process %s %s  %s" % (pid, what, " ".join(cmd) if isinstance(cmd, list) else cmd))
        for pid, cmd in unregistered(wt):
            print("NOT REGISTERED, NOT STOPPED: process %s holds this worktree's path: %s" % (pid, cmd))
    steps = ([["git", "worktree", "remove", wt]] if wt else []) + [["git", "branch", "-D", branch], ["git", "worktree", "prune"]]
    for s in steps:
        r = run(s, repo)
        if r.returncode != 0:
            print("FAILED: %s\n%s%s" % (" ".join(s), r.stdout, r.stderr))
            return 1
        print("ok  " + " ".join(s))
    print("Removed %s%s. The remote branch is GitHub's to delete; this script never touches it." % (branch, " and its worktree" if wt else ""))
    return 0


def selftest():
    fails = []

    def check(name, ok):
        print("  %s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory() as td:
        repo = os.path.join(td, "repo")
        os.makedirs(repo)
        g = lambda *a, cwd=repo: run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"] + list(a), cwd)
        g("init", "-q", "-b", "main")
        open(os.path.join(repo, "a.txt"), "w", newline='').write("a\n")
        open(os.path.join(repo, ".gitignore"), "w", newline='').write(".claude/pids.json\n.claude/bg-*.log\n")
        g("add", "."), g("commit", "-qm", "base")
        exists = lambda b: g("rev-parse", "--verify", "-q", "refs/heads/" + b).returncode == 0

        def make(branch):
            """A task branch in its own worktree with one commit; returns (worktree path, tip)."""
            wt = os.path.join(td, "wt-" + branch)
            g("worktree", "add", "-q", "-b", branch, wt, "main")
            open(os.path.join(wt, branch + ".txt"), "w", newline='').write(branch + "\n")
            g("add", ".", cwd=wt), g("commit", "-qm", branch, cwd=wt)
            return wt, g("rev-parse", branch).stdout.strip()

        stub = lambda state, oid: (lambda b: {"state": state, "headRefOid": oid, "mergeCommit": {"oid": "x"}})

        # A squash-merged branch: main gets the change as a NEW commit, so the branch is not an ancestor.
        wt, tip = make("squashed")
        g("merge", "--squash", "squashed"), g("commit", "-qm", "squash of squashed")
        check("premise: git branch -d refuses a squash-merged branch", g("branch", "-d", "squashed").returncode != 0)
        check("squash-merged, clean, tip = PR head: removed",
              end_task("squashed", repo, stub("MERGED", tip), cwd=td) == 0 and not exists("squashed") and not os.path.exists(wt))

        # A session's registered background process is stopped before its worktree is removed (contract BG-LAUNCHER).
        import importlib.util
        spec = importlib.util.spec_from_file_location("bg", os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg.py"))
        bg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bg)
        wt, tip = make("served")
        entry = bg.start([sys.executable, "-c", "import time; time.sleep(300)"], wt)
        check("premise: the registered server is running", alive(entry["pid"], entry["create"]))
        ok = end_task("served", repo, stub("MERGED", tip), cwd=td) == 0
        check("a registered server is stopped, then the worktree and branch are removed",
              ok and not alive(entry["pid"], entry["create"]) and not exists("served") and not os.path.exists(wt))
        wt, tip = make("served-open")
        entry = bg.start([sys.executable, "-c", "import time; time.sleep(300)"], wt)
        check("a refused removal (PR not merged) leaves the server running",
              end_task("served-open", repo, stub("OPEN", tip), cwd=td) == 1 and alive(entry["pid"], entry["create"]))
        kill_tree(entry["pid"])

        wt, tip = make("open-pr")
        check("PR not merged: refuses, nothing deleted",
              end_task("open-pr", repo, stub("OPEN", tip), cwd=td) == 1 and exists("open-pr") and os.path.isdir(wt))

        wt, tip = make("extra")
        open(os.path.join(wt, "more.txt"), "w", newline='').write("m\n")
        g("add", ".", cwd=wt), g("commit", "-qm", "local only", cwd=wt)
        check("an extra local commit: refuses, nothing deleted",
              end_task("extra", repo, stub("MERGED", tip), cwd=td) == 1 and exists("extra") and os.path.isdir(wt))

        wt, tip = make("dirty")
        open(os.path.join(wt, "scratch.txt"), "w", newline='').write("s\n")
        check("a dirty worktree: refuses, nothing deleted",
              end_task("dirty", repo, stub("MERGED", tip), cwd=td) == 1 and exists("dirty") and os.path.isdir(wt))

        wt, tip = make("inside")
        check("run from inside the worktree: refuses",
              end_task("inside", repo, stub("MERGED", tip), cwd=wt) == 1 and exists("inside") and os.path.isdir(wt))

        check("gh cannot report: refuses", end_task("dirty", repo, lambda b: None, cwd=td) == 1 and exists("dirty"))
        sha = "a" * 40
        pr = lambda n, state, merged, s=sha: {"number": n, "state": state, "merged_at": merged, "head": {"sha": s}, "merge_commit_sha": "m" * 40}
        check("REST: a merged PR reads MERGED with its head", pr_from_rest([pr(5, "closed", "2026-10-25T00:00:00Z")]) == {"state": "MERGED", "headRefOid": sha, "mergeCommit": {"oid": "m" * 40}})
        check("REST: closed unmerged reads CLOSED", pr_from_rest([pr(5, "closed", None)])["state"] == "CLOSED")
        check("REST: open reads OPEN", pr_from_rest([pr(5, "open", None)])["state"] == "OPEN")
        check("REST: the newest PR for a branch wins", pr_from_rest([pr(5, "closed", "x"), pr(9, "open", None)])["state"] == "OPEN")
        check("REST: no PR, a malformed list or a missing head reads None",
              pr_from_rest([]) is None and pr_from_rest({"message": "Not Found"}) is None and pr_from_rest([{"number": 1, "state": "open", "head": {}}]) is None)
        check("no such branch: refuses", end_task("nope", repo, stub("MERGED", "0" * 40), cwd=td) == 1)

        g("worktree", "add", "-q", "--detach", os.path.join(td, "det"), "main")
        g("branch", "bare", "main")
        check("a merged branch with no worktree: its branch is removed",
              end_task("bare", repo, stub("MERGED", g("rev-parse", "bare").stdout.strip()), cwd=td) == 0 and not exists("bare"))
        check("the primary checkout's branch is never removed", end_task("main", repo, stub("MERGED", g("rev-parse", "main").stdout.strip()), cwd=td) == 1
              and exists("main"))
        g("worktree", "prune")
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) != 1 or argv[0].startswith("-"):
        print(__doc__)
        return 2
    wts = worktrees(os.getcwd())          # the first entry is the primary checkout, from any worktree
    if not wts:
        print("not in a git repository")
        return 2
    repo = wts[0][0]
    return end_task(argv[0], repo)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
