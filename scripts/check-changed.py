#!/usr/bin/env python3
"""Before pushing: run the checks this branch's changes need, then let CI run the rest (canon §7.8).

    python scripts/check-changed.py            # selected verifiers + the fast site-wide checks
    python scripts/check-changed.py --list     # say what would run, run nothing
    python scripts/check-changed.py --full     # every check in the workflow (the old full local suite)

The changes are everything on this branch since it left origin/main, plus uncommitted and untracked
files. scripts/ci-deps.py picks the content verifiers they can affect (exactly as CI's plan job does).
Added to those: the fast site-wide checks (the stdlib ones, about a second each), and the shared-asset
tests (scripts/test-*.py) when anything under schools/ or the test itself changed. Not run here, because
CI always runs them and they are slow or Windows-unreliable: tier 1-2 (check-site.py), the tier 4 bank
extraction and lint, and the leaderboard coverage job.

Why not the full suite every time: the repo is public, so CI minutes are free, and CI runs every
site-wide check on every PR and EVERYTHING on every merge to main and weekly. A full local run was a
second, slower copy of CI, with three known Windows-only false failures (todo §4).
"""
import argparse, importlib.util, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("ci_deps", os.path.join(ROOT, "scripts", "ci-deps.py"))
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)

SLOW_SITE_WIDE = {"scripts/check-site.py", "scripts/extract-banks.py", "scripts/check-banks.py"}


def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def changed_files():
    base = git("merge-base", "origin/main", "HEAD").strip()
    files = set(git("diff", "--name-only", base).splitlines())            # committed + uncommitted
    files |= set(git("ls-files", "--others", "--exclude-standard").splitlines())
    return sorted(f for f in files if f.strip())


def plan(full):
    checks = ci.checks()
    if full:
        return [(label, cmd) for _, _, label, cmd, _ in checks], ["--full: every check"], []
    changed = changed_files()
    run_all, reasons, picked = ci.select(changed)
    assets = any(f.startswith("schools/") for f in changed)
    out = []
    for group, selective, label, cmd, script in checks:
        if selective:
            if run_all or script in picked:
                out.append((label, cmd))
        elif script in SLOW_SITE_WIDE:
            continue
        elif os.path.basename(script or "").startswith("test-"):
            if run_all or assets or script in changed:
                out.append((label, cmd))
        else:
            out.append((label, cmd))
    return out, reasons, changed


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    todo, reasons, changed = plan(a.full)
    if changed:
        print("changed since origin/main (%d): %s" % (len(changed), ", ".join(changed[:12]) + (" ..." if len(changed) > 12 else "")))
    for r in reasons:
        print(r)
    print("%d check(s) to run:" % len(todo))
    for label, _ in todo:
        print("  " + label)
    if a.list:
        return 0
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:                                         # node for Test the Claim: Playwright's own, as CI does
        import playwright
        env["PATH"] = os.path.join(os.path.dirname(playwright.__file__), "driver") + os.pathsep + env.get("PATH", "")
    except ImportError:
        pass
    failed = []
    for label, cmd in todo:
        t = time.time()
        r = subprocess.run(cmd, shell=True, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok = r.returncode == 0
        print("%s  %s  (%ds)" % ("ok    " if ok else "FAILED", label, time.time() - t))
        if not ok:
            failed.append(label)
            print("\n".join("      " + l for l in (r.stdout + r.stderr).strip().splitlines()[-15:]))
    print("FAILED: %s" % ", ".join(failed) if failed else "All selected checks passed. Push, and CI runs the rest.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
