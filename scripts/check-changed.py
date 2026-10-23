#!/usr/bin/env python3
"""Before pushing: run the checks this branch's changes need, then let CI run the rest (canon §7.8).

    python scripts/check-changed.py              # selected verifiers + the site-wide checks, two queues
    python scripts/check-changed.py --list       # say what would run and what is deferred, run nothing
    python scripts/check-changed.py --full       # every check in the workflow (the old full local suite)
    python scripts/check-changed.py --workers 1  # light checks one at a time too (the runner before PREPUSH-SCOPE)
    python scripts/check-changed.py --files a b  # plan for these changed paths instead of the branch's
    python scripts/check-changed.py --all-heavy  # run the heavy checks reached only through a shared file here too
    python scripts/check-changed.py --selftest   # the planning rules, each with a planted fault (not run by CI)

The changes are everything on this branch since it left origin/main, plus uncommitted and untracked
files. scripts/ci-deps.py picks the content verifiers they can affect (exactly as CI's plan job does:
the same select(), imported, not copied). Added to those: every site-wide check CI runs on every PR,
except the ones deferred below.

Deferred to CI, and printed as such on every run (contract PREPUSH-SCOPE, 10 Oct 2026): tier 1-2
(check-site.py), the tier 4 bank extraction and lint, and the leaderboard coverage job. CI runs them on
every PR; locally they are slow or Windows-unreliable. The last line of the output is the PR line:
"checks deferred to CI: ...".

Heavy checks reached only through a shared file (contract CHECK-CHANGED-DEFER, 23 Oct 2026): a shared-asset
change rightly selects every verifier whose pages load it (scripts/ci-deps.py, unchanged), but a heavy browser
verifier reached ONLY that way (an answer-lock part, a level resolver, another game's play-through) is a slower
duplicate of what CI runs on the PR, in parallel, before the Gate allows a merge. plan() classifies every selected
check from the paths select() says picked it: DIRECT when one of them is the check's own script, a page or file under a
games/<slug>/ or escape-rooms/<slug>/ (a game's own), a page it names, or data it declares; otherwise INDIRECT (schools/*,
escape-rooms/assets/*, a script library). INDIRECT and heavy: deferred to CI, listed with the shared file(s) that reached
it, and in the PR line. Nothing is skipped: CI still runs every selected check and the Gate still requires it. INDIRECT
light checks, DIRECT checks, always-run checks and a CI-file change (everything runs) are unchanged, and --all-heavy
runs the deferred heavy ones here too.

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


_MAP = {}


def dep_map():
    """The dependency map, built once per process (ci.select() would rebuild it on every call)."""
    if "map" not in _MAP:
        _MAP["map"] = ci.dependency_map()
        _MAP["declared"] = ci.declared_deps()
    return _MAP["map"], _MAP["declared"]


def is_direct(path, script, declared):
    """True when `path` reaches the check `script` as its own file, not through a shared one: the script itself, a
    game's or escape room's own page and files (not the engine, escape-rooms/assets/), a page the check names, data
    it reads, or a path its own "# ci-deps:" header declares. Anything else (schools/*, escape-rooms/assets/*, a
    script library) is a shared file."""
    path = path.replace("\\", "/")
    if path == script:
        return True
    if path.startswith(("games/", "escape-rooms/")) and not path.startswith("escape-rooms/assets/"):
        return True
    own = declared.get(script, ())
    if path in own or any(d.endswith("/") and path.startswith(d) for d in own):
        return True
    if path.endswith(".html") and not path.startswith("schools/"):
        return True
    return path.startswith(("data/", "docs/"))


def should_defer(indirect, heavy, run_all, all_heavy):
    """A heavy check reached only through shared files is left to CI (never on a CI-file change, never with --all-heavy)."""
    return indirect and heavy and not run_all and not all_heavy


def plan(full, files=None, all_heavy=False):
    """(to run [(label, cmd)], deferred [label], reasons, changed, via {label: [shared files]}). `via` names, for each
    heavy check deferred because only shared files reached it, those files."""
    checks = ci.checks()
    if full:
        return [(label, cmd) for _, _, label, cmd, _ in checks], [], ["--full: every check"], [], {}
    changed = sorted(files) if files is not None else changed_files()
    dmap, declared = dep_map()
    run_all, reasons, picked = ci.select(changed, dmap)
    est = expected_seconds()
    out, deferred, via = [], [], {}
    for group, selective, label, cmd, script in checks:
        if selective:
            if not (run_all or script in picked):
                continue
            why = picked.get(script, [])
            indirect = bool(why) and not any(w.startswith("always runs") or is_direct(w, script, declared) for w in why)
            if should_defer(indirect, is_heavy(label, cmd, est), run_all, all_heavy):
                deferred.append(label)
                via[label] = sorted(set(why))
            else:
                out.append((label, cmd))
        elif script in SLOW_SITE_WIDE:
            if label not in deferred:
                deferred.append(label)
        else:
            out.append((label, cmd))
    return out, deferred + OTHER_CI_JOBS, reasons, changed, via


def expected_seconds():
    """CI's last recorded time per check label, to start the longest first (unknown: 60 s)."""
    try:
        with open(os.path.join(ROOT, "scripts", "ci-timings.json"), encoding="utf-8") as f:
            return json.load(f).get("lines", {})
    except (OSError, ValueError):
        return {}


def selftest():
    """The planning rules on the real dependency map. Plants: a direct hit classified as indirect, a light check
    deferred, and a deferral on a CI-file change; each must be caught. Not run by CI (nothing in CI changes)."""
    global is_direct, should_defer
    est = expected_seconds()
    checks = ci.checks()
    dmap, declared = dep_map()
    oracle_direct = is_direct                                          # the real rule, kept apart from the planted ones
    cmds = {label: (cmd, script) for _, selective, label, cmd, script in checks if selective}

    def heavy(label):
        return is_heavy(label, cmds[label][0], est)
    # a game whose own verifier is heavy: its page change must still run that verifier here
    game = heavy_label = None
    for _, selective, label, cmd, script in checks:
        if selective and heavy(label) and len(dmap[script]["games"]) == 1 and not dmap[script]["always"]:
            game, heavy_label = next(iter(dmap[script]["games"])), label
            break
    other = "schools/assets/answer-count.js"
    fails = []

    def check(name, ok, detail=""):
        print("  %s  %-70s %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            fails.append(name)

    def labels(res):
        return {l for l, _ in res[0]}

    def run(files, **kw):
        return plan(False, files, **kw)

    def rules():
        out = {}
        res_a = run(["games/%s/index.html" % game])
        out["a"] = heavy_label in labels(res_a) and not res_a[4]
        res_b = run([other])
        # the oracle: light checks that only the shared asset reaches must still run here; heavy ones must not
        sel_b = ci.select([other], dmap)[2]
        ind = {l for l, (c, s) in cmds.items() if s in sel_b and not any(
            w.startswith("always runs") or oracle_direct(w, s, declared) for w in sel_b[s])}
        ind_light, ind_heavy = {l for l in ind if not heavy(l)}, {l for l in ind if heavy(l)}
        out["b"] = (bool(res_b[4]) and bool(ind_light) and ind_light <= labels(res_b) and bool(ind_heavy)
                    and not (ind_heavy & labels(res_b)) and ind_heavy == set(res_b[4]) & ind_heavy)
        res_c = run(["games/%s/index.html" % game, other])
        out["c"] = heavy_label in labels(res_c) and any(l != heavy_label for l in res_c[4])
        res_d = run([".github/workflows/check-site.yml"])
        out["d"] = not res_d[4] and set(cmds) <= labels(res_d)
        res_e = run([other], all_heavy=True)
        out["e"] = not res_e[4] and set(res_e[4]) == set() and len(res_e[0]) > len(res_b[0])
        return out

    def picked_why(label, files):
        return ci.select(files, dmap)[2].get(cmds[label][1], [])

    check("a game with a heavy verifier was found for the cases", bool(game), "%s: %s" % (game, heavy_label))
    ok = rules()
    check("(a) a game's own page still runs its heavy verifier here", ok["a"])
    check("(b) a shared asset alone defers heavy checks, with the files named, and runs the light ones", ok["b"])
    check("(c) a game's page plus a shared asset: that game's heavy verifier runs, other games' are deferred", ok["c"])
    check("(d) a CI-file change runs every selected check and defers none for being indirect", ok["d"])
    check("(e) --all-heavy defers nothing for being indirect", ok["e"])
    # the plants
    real_direct, real_defer = is_direct, should_defer
    try:
        is_direct = lambda *a: False                                   # a direct hit classified as indirect
        check("plant: a direct hit classified as indirect is caught", not rules()["a"])
        is_direct = real_direct
        should_defer = lambda indirect, heavy_, run_all, all_heavy: indirect and not run_all and not all_heavy   # a light check deferred
        r = rules()
        check("plant: a light check deferred is caught", not r["b"])
        should_defer = lambda indirect, heavy_, run_all, all_heavy: indirect and heavy_                          # deferred when run_all
        r = rules()
        check("plant: a deferral when everything must run is caught", not r["d"] or not r["e"])
    finally:
        is_direct, should_defer = real_direct, real_defer
    print("selftest: %s" % ("FAILED: " + "; ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main():
    # A failing check's tail is printed here; on Windows a redirected stdout is cp1252, and a £, → or ✓ in it
    # raised UnicodeEncodeError and lost the summary (contract CHANGED-UTF8, 8 Oct 2026).
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--all-heavy", action="store_true", help="run the heavy checks reached only through a shared file here too")
    ap.add_argument("--selftest", action="store_true", help="the planning rules, each with a planted fault")
    ap.add_argument("--files", nargs="+", metavar="PATH", help="plan for these changed paths")
    ap.add_argument("--workers", type=int, default=max(1, min(6, (os.cpu_count() or 2) // 2)))
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    todo, deferred, reasons, changed, via = plan(a.full, a.files, a.all_heavy)
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
    if via:
        print("%d heavy check(s) reached only through a shared file, deferred to CI (it runs them on every PR and the Gate "
              "requires them; --all-heavy runs them here):" % len(via))
        for label in via:
            print("  %s  <- %s" % (label, ", ".join(via[label])))
    fixed = [d for d in deferred if d not in via]
    if fixed:
        print("%d deferred to CI (%s):" % (len(fixed), DEFER_WHY))
        for label in fixed:
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
