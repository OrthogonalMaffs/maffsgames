#!/usr/bin/env python3
# ci-line: End-of-task helper (end-task.py: a squash-merged branch is removed; an unmerged branch, an extra local commit and a dirty worktree each refuse; gh stubbed) | --selftest
"""Remove a finished task's worktree and local branch, only when that is safe (RULINGS-12OCT, 12 Oct 2026).

    python scripts/end-task.py <branch>        # after the PR is merged and main's run is reported
    python scripts/end-task.py --selftest

This repo squash-merges every PR, so a merged branch's tip is never an ancestor of main and `git branch -d`
refuses. This helper checks instead, then deletes. It deletes only when ALL hold:
  1. the branch's PR is MERGED (gh pr view <branch> --json state,headRefOid,mergeCommit);
  2. the local tip equals the PR's headRefOid (nothing local that was not in the PR);
  3. the branch's worktree, if it has one, is clean (git status --porcelain is empty).
Then: git worktree remove (never --force), git branch -D, git worktree prune. Otherwise it names the failed
condition and deletes nothing. It never touches a remote branch (GitHub deletes a merged head branch itself).
"""
import json, os, subprocess, sys, tempfile


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8")


def real(p):
    return os.path.normcase(os.path.realpath(p))


def gh_pr(branch, cwd=None):
    """The PR's {state, headRefOid, mergeCommit} from the gh CLI, or None if gh cannot say."""
    r = run(["gh", "pr", "view", branch, "--json", "state,headRefOid,mergeCommit"], cwd)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
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
