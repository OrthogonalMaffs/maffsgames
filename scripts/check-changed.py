#!/usr/bin/env python3
"""Before pushing: run the checks this branch's changes need, then let CI run the rest (canon §7.8).

    python scripts/check-changed.py              # selected verifiers + the site-wide checks, two queues
    python scripts/check-changed.py --list       # say what would run and what is deferred, run nothing
    python scripts/check-changed.py --full       # every check in the workflow (the old full local suite)
    python scripts/check-changed.py --workers 1  # light checks one at a time too (the runner before PREPUSH-SCOPE)
    python scripts/check-changed.py --files a b  # plan for these changed paths instead of the branch's

The changes are everything on this branch since it left origin/main, plus uncommitted and untracked
files. scripts/ci-deps.py picks the content verifiers they can affect (exactly as CI's plan job does:
the same select(), imported, not copied). Added to those: every site-wide check CI runs on every PR,
except the ones deferred below.

Deferred to CI, and printed as such on every run (contract PREPUSH-SCOPE, 10 Oct 2026): tier 1-2
(check-site.py), the tier 4 bank extraction and lint, and the leaderboard coverage job. CI runs them on
every PR; locally they are slow or Windows-unreliable. The last line of the output is the PR line:
"checks deferred to CI: ...".

Speed (PREPUSH-SCOPE): the cost was never the selection (cause b): a shared-asset change rightly selects
every game, and the checks ran one after another, each starting its own browser. They now run in TWO
QUEUES at once (Jon's ruling, 10 Oct 2026):
  heavy  one at a time, longest first: a check CI timed at HEAVY_SECONDS or more
         (scripts/ci-timings.json), or one whose script drives a browser AND runs its own work
         concurrently (the answer-lock parts, the teacher feedback line, the escape-room tests). Six of
         the answer-lock parts side by side overloaded the machine and every one failed (games
         UNPLAYABLE after Start), so these never share it with each other.
  light  everything else, --workers at once (default: half the CPUs, at most 6), longest first.
Each check still starts its own browser: they are separate scripts with their own harnesses, and a
browser launch is about a second of a check that takes tens.

Why not the full suite every time: the repo is public, so CI minutes are free, and CI runs every
site-wide check on every PR and EVERYTHING on every merge to main and weekly. A full local run was a
second, slower copy of CI, with three known Windows-only false failures (todo §4).
"""
import argparse, concurrent.futures, importlib.util, json, os, re, subprocess, sys, threading, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("ci_deps", os.path.join(ROOT, "scripts", "ci-deps.py"))
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)

SLOW_SITE_WIDE = {"scripts/check-site.py", "scripts/extract-banks.py", "scripts/check-banks.py"}
# Not a line in ci.checks(): its own workflow job (node), always run in CI.
OTHER_CI_JOBS = ["Leaderboard coverage (every live game submits, or is declared)"]
DEFER_WHY = "slow or Windows-unreliable locally; CI runs it on every PR"
HEAVY_SECONDS = 60
_CONCURRENT = re.compile(r"Semaphore\(|ThreadPoolExecutor|asyncio\.gather|--workers")


def is_heavy(label, cmd, est):
    """One at a time: long in CI, or a browser check that runs its own work concurrently."""
    if est.get(label, 0) >= HEAVY_SECONDS:
        return True
    m = re.search(r"scripts/[\w.-]+\.py", cmd)
    if not m:
        return False
    try:
        with open(os.path.join(ROOT, m.group(0)), encoding="utf-8") as f:
            src = f.read()
    except OSError:
        return False
    return "playwright" in src and bool(_CONCURRENT.search(src))


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def changed_files():
    base = git("merge-base", "origin/main", "HEAD").strip()
    files = set(git("diff", "--name-only", base).splitlines())            # committed + uncommitted
    files |= set(git("ls-files", "--others", "--exclude-standard").splitlines())
    return sorted(f for f in files if f.strip())


def plan(full, files=None):
    """(to run [(label, cmd)], deferred [label], reasons, changed)."""
    checks = ci.checks()
    if full:
        return [(label, cmd) for _, _, label, cmd, _ in checks], [], ["--full: every check"], []
    changed = sorted(files) if files is not None else changed_files()
    run_all, reasons, picked = ci.select(changed)
    out, deferred = [], []
    for group, selective, label, cmd, script in checks:
        if selective:
            if run_all or script in picked:
                out.append((label, cmd))
        elif script in SLOW_SITE_WIDE:
            if label not in deferred:
                deferred.append(label)
        else:
            out.append((label, cmd))
    return out, deferred + OTHER_CI_JOBS, reasons, changed


def expected_seconds():
    """CI's last recorded time per check label, to start the longest first (unknown: 60 s)."""
    try:
        with open(os.path.join(ROOT, "scripts", "ci-timings.json"), encoding="utf-8") as f:
            return json.load(f).get("lines", {})
    except (OSError, ValueError):
        return {}


def main():
    # A failing check's tail is printed here; on Windows a redirected stdout is cp1252, and a £, → or ✓ in it
    # raised UnicodeEncodeError and lost the summary (contract CHANGED-UTF8, 8 Oct 2026).
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--files", nargs="+", metavar="PATH", help="plan for these changed paths")
    ap.add_argument("--workers", type=int, default=max(1, min(6, (os.cpu_count() or 2) // 2)))
    a = ap.parse_args()
    todo, deferred, reasons, changed = plan(a.full, a.files)
    if changed:
        print("changed since origin/main (%d): %s" % (len(changed), ", ".join(changed[:12]) + (" ..." if len(changed) > 12 else "")))
    for r in reasons:
        print(r)
    est = expected_seconds()
    heavy = [t for t in todo if is_heavy(t[0], t[1], est)]
    light = [t for t in todo if t not in heavy]
    print("%d check(s) to run: %d heavy, one at a time; %d light, %d at once:" % (len(todo), len(heavy), len(light), a.workers))
    for label, cmd in todo:
        print("  %s %s" % ("[heavy]" if (label, cmd) in heavy else "       ", label))
    if deferred:
        print("%d deferred to CI (%s):" % (len(deferred), DEFER_WHY))
        for label in deferred:
            print("  " + label)
    defer_line = "checks deferred to CI: " + ("; ".join(deferred) if deferred else "none")
    if a.list:
        print(defer_line)
        return 0
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    try:                                         # node for Test the Claim: Playwright's own, as CI does
        import playwright
        env["PATH"] = os.path.join(os.path.dirname(playwright.__file__), "driver") + os.pathsep + env.get("PATH", "")
    except ImportError:
        pass
    heavy.sort(key=lambda t: -est.get(t[0], 60))
    light.sort(key=lambda t: -est.get(t[0], 60))
    lock, failed, spent = threading.Lock(), [], []
    t0 = time.time()

    def one(label, cmd):
        t = time.time()
        r = subprocess.run(cmd, shell=True, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok, took = r.returncode == 0, time.time() - t
        with lock:
            spent.append(took)
            print("%s  %s  (%ds; %d/%d done at %ds)" % ("ok    " if ok else "FAILED", label, took, len(spent), len(todo), time.time() - t0))
            if not ok:
                failed.append(label)
                print("\n".join("      " + l for l in (r.stdout + r.stderr).strip().splitlines()[-15:]))
            sys.stdout.flush()

    def queue(items, workers):
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(lambda t: one(*t), items))

    both = [threading.Thread(target=queue, args=(heavy, 1)), threading.Thread(target=queue, args=(light, a.workers))]
    for t in both:
        t.start()
    for t in both:
        t.join()
    print("%d check(s) in %ds wall, %ds of check time (%d heavy one at a time, %d light %d at once)"
          % (len(todo), time.time() - t0, sum(spent), len(heavy), len(light), a.workers))
    print("FAILED: %s" % ", ".join(failed) if failed else "All selected checks passed. Push, and CI runs the rest.")
    print(defer_line)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
