#!/usr/bin/env python3
"""The "Content verifiers" groups, built from each script's own header (contract V, 7 Oct 2026; canon §7.8.2).

    python scripts/ci-groups.py                       # every content group and its lines
    python scripts/ci-groups.py --json                # the matrix, as the workflow's content job reads it
    python scripts/ci-groups.py --github-output FILE  # plan job: writes groups=<that JSON>
    python scripts/ci-groups.py --compare FILE        # equal, line for line, to FILE's static content groups?
    python scripts/ci-groups.py --selftest            # header parsing proofs
    python scripts/ci-groups.py --record-timings ID   # scripts/ci-timings.json from a main full run (gh CLI)

Why. Until 7 Oct 2026 each content group listed its lines inside .github/workflows/check-site.yml, so every
new verifier edited that shared file: the cloud lane's #96, #97 and #100-#102 each did, and two of them
conflicted with home-lane PRs. Now a script declares the CI lines it contributes, in its own file:

    # ci-line: <group> | <label> | <args>
    # ci-deps: <path> [<path> ...]          (optional: extra dependencies for scripts/ci-deps.py)
    # ci-held: <reason>                     (instead of a ci-line: deliberately not run in CI, and why)

one "# ci-line:" comment per line it contributes, each at the start of a line. <args> are the arguments to
"python scripts/<this file>"; "&&" joins several runs of the same script in one line, so
"--part-selftest && --part 1" is "python scripts/X.py --part-selftest && python scripts/X.py --part 1", and
" && --selftest" (nothing before the &&) is "python scripts/X.py && python scripts/X.py --selftest".

The groups themselves (name, timeout) are GROUPS below. A ci-line naming any other group fails
(scripts/check-verifier-coverage.py). Lines run in the order: scripts by file name, then each script's
headers in file order. The site-wide jobs (tiers 1-2, site-wide checks, tier 4, shared assets) stay listed in
the workflow.

Stdlib only.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "check-site.yml")
PREFIX = "Content verifiers"
TIMINGS = "scripts/ci-timings.json"     # each content line's seconds on a main full run (--record-timings)

# (id, job name, timeout in minutes). The job name is what GitHub shows; keep it stable. Canon §7.8.1: no
# content job may run past 4 minutes; each fails at 75% of its timeout.
#   A   Free Daily Pizza: about 3 minutes, the longest single verifier.
#   C1-C4  Just Pythag It, Bruv in four parts (--part, dealt by measured cost; each runs --part-selftest).
#   D1-D2  Equation Builder in two parts (--part i/2, by candidate arrangement; D1 has the whole-question
#          checks and the planted-fault self-test).
#   E   Estimation Engine and the 6 Oct 2026 joiners.
#   E2  split from E (Jon, 9 Oct 2026; E reached 9m04s of its 9m budget on main): its three slowest verifiers.
#   B1-B4  every other content verifier, cut by the slowest time each line has taken on main.
#   L1-L5  check-answer-lock.py --part i/n (canon 7.6.0): the games migrated to MaffsLock, played in Chromium.
#          A group with no line is not in the matrix: add a part as the roll-out grows.
GROUPS = [
    ("A", "Content verifiers A (Free Daily Pizza)", 12),
    ("C1", "Content verifiers C1 (Just Pythag It, Bruv, part 1)", 6),
    ("C2", "Content verifiers C2 (Just Pythag It, Bruv, part 2)", 6),
    ("C3", "Content verifiers C3 (Just Pythag It, Bruv, part 3)", 6),
    ("C4", "Content verifiers C4 (Just Pythag It, Bruv, part 4)", 6),
    ("D1", "Content verifiers D1 (Equation Builder, part 1)", 6),
    ("D2", "Content verifiers D2 (Equation Builder, part 2)", 6),
    ("E", "Content verifiers E (Estimation Engine, Angle Ace, Simultaneous Solver, Like Terms Collector, Fermi Lab, Screening Room)", 12),
    ("E2", "Content verifiers E2 (Screening Room, Simultaneous Solver, Terrible Advice)", 12),
    ("B1", "Content verifiers B1 (Log Laws Solve, Maths Court, Six Sevens and two more)", 8),
    ("B2", "Content verifiers B2 (Growth and Decay and nine quick ones)", 8),
    ("B3", "Content verifiers B3 (Decimal Detective, Quadratic Factoriser and three more)", 8),
    ("B4", "Content verifiers B4 (Negative Number Line, Trig Worms and the rest)", 8),
    ("L1", "Answer lock L1 (migrated games, part 1)", 8),
    ("L2", "Answer lock L2 (migrated games, part 2)", 8),
    ("L3", "Answer lock L3 (migrated games, part 3)", 8),
    ("L4", "Answer lock L4 (migrated games, part 4)", 8),
    ("L5", "Answer lock L5 (migrated games, part 5)", 8),
]
GROUP_IDS = [g for g, _, _ in GROUPS]

LINE = re.compile(r"^# ci-line:(.*)$", re.M)
DEPS = re.compile(r"^# ci-deps:(.*)$", re.M)
HELD = re.compile(r"^# ci-held:(.*)$", re.M)


def command(script, args):
    """The shell command for a header's <args>: each '&&' part is one run of the script."""
    runs = []
    for part in args.split("&&"):
        part = part.strip()
        runs.append(("python scripts/%s %s" % (script, part)).rstrip())
    return " && ".join(runs)


def parse(name, text):
    """{'lines': [(group, label, cmd)], 'deps': [paths], 'held': reason or None, 'errors': [str]}."""
    out = {"lines": [], "deps": [], "held": None, "errors": []}
    for m in LINE.finditer(text):
        parts = m.group(1).split("|")
        if len(parts) != 3:
            out["errors"].append("%s: a ci-line needs exactly '<group> | <label> | <args>': %r" % (name, m.group(0)))
            continue
        group, label, args = (p.strip() for p in parts)
        if not group or not label:
            out["errors"].append("%s: a ci-line with no group or no label: %r" % (name, m.group(0)))
            continue
        out["lines"].append((group, label, command(name, args)))
    for m in DEPS.finditer(text):
        out["deps"] += m.group(1).split()
    held = [m.group(1).strip() for m in HELD.finditer(text)]
    if held:
        out["held"] = held[0] or None
        if not held[0]:
            out["errors"].append("%s: ci-held with no reason" % name)
    return out


def headers():
    """{script name: parse()} for every scripts/*.py that declares anything."""
    out = {}
    for name in sorted(os.listdir(SCRIPTS)):
        if not name.endswith(".py"):
            continue
        with open(os.path.join(SCRIPTS, name), encoding="utf-8") as f:
            info = parse(name, f.read())
        if info["lines"] or info["deps"] or info["held"] or info["errors"]:
            out[name] = info
    return out


def groups(hdrs=None):
    """[{'id', 'name', 'timeout', 'lines': [(label, cmd)]}] in GROUPS order (lines by script, then header order)."""
    hdrs = headers() if hdrs is None else hdrs
    by = {g: [] for g in GROUP_IDS}
    for name in sorted(hdrs):
        for group, label, cmd in hdrs[name]["lines"]:
            if group in by:
                by[group].append((label, cmd))
    return [{"id": g, "name": n, "timeout": t, "lines": by[g]} for g, n, t in GROUPS]


def matrix(hdrs=None):
    """The content job's matrix include list: one entry per group with lines, as the static entries were."""
    return [{"name": g["name"], "timeout": g["timeout"],
             "checks": "".join("%s|%s\n" % l for l in g["lines"])}
            for g in groups(hdrs) if g["lines"]]


def errors(hdrs=None):
    """Header faults: malformed lines, unknown group names."""
    hdrs = headers() if hdrs is None else hdrs
    errs = []
    for name, info in sorted(hdrs.items()):
        errs += info["errors"]
        for group, label, _ in info["lines"]:
            if group not in GROUP_IDS:
                errs.append("%s: ci-line names group %r, which is not in scripts/ci-groups.py GROUPS (%s)"
                            % (name, group, ", ".join(GROUP_IDS)))
            if "|" in label:
                errs.append("%s: a label may not contain '|'" % name)
        if info["held"] and info["lines"]:
            errs.append("%s: declares both ci-held and ci-line" % name)
    return errs


def static_checks(path=WORKFLOW):
    """[(job name, label, cmd)] still listed in the workflow file's matrices (site-wide jobs; before contract V,
    the content groups too). A plain reader of the 'checks: |' blocks: no YAML library needed."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out, name, inblock, indent = [], None, False, 0
    for raw in text.splitlines():
        m = re.match(r"^(\s*)- name: (.+)$", raw)
        if m:
            name, inblock = m.group(2).strip(), False
            continue
        m = re.match(r"^(\s*)checks: \|\s*$", raw)
        if m:
            inblock, indent = True, len(m.group(1))
            continue
        if inblock:
            if raw.strip() == "":
                continue
            if len(raw) - len(raw.lstrip()) <= indent:
                inblock = False
                continue
            label, cmd = raw.strip().split("|", 1)
            out.append((name, label.strip(), cmd.strip()))
    return out


def all_checks():
    """[(group name, selective, label, cmd)]: the workflow's static (site-wide) lines, then every content group's
    from the headers. A content group still listed in the workflow is not read: the headers are the source."""
    out = [(n, False, l, c) for n, l, c in static_checks() if not n.startswith(PREFIX)]
    for g in groups():
        out += [(g["name"], True, l, c) for l, c in g["lines"]]
    return out


def ci_text():
    """Every command CI runs, one per line: for checks that ask 'does CI run this?' by searching for it."""
    return "\n".join(c for _, _, _, c in all_checks()) + "\n"


def compare(path):
    """Contract V's proof: the headers give exactly the static content lines of the workflow at `path`."""
    old = sorted((n, l, c) for n, l, c in static_checks(path) if n.startswith(PREFIX))
    new = sorted((g["name"], l, c) for g in groups() for l, c in g["lines"])
    gone = [x for x in old if x not in new]
    extra = [x for x in new if x not in old]
    for x in gone:
        print("ONLY IN THE WORKFLOW  %s | %s | %s" % x)
    for x in extra:
        print("ONLY IN THE HEADERS   %s | %s | %s" % x)
    print("compare: %d static content line(s), %d from headers: %s"
          % (len(old), len(new), "EQUAL" if not gone and not extra else "DIFFERENT"))
    return 0 if not gone and not extra else 1


def record_timings(run_id):
    """Write TIMINGS from a finished run's content jobs (needs the gh CLI): each line's seconds, read from the
    job log's 'ok  <label>  (Ns; group at ...)' lines. scripts/check-verifier-coverage.py reports any group
    whose lines add up past 4 minutes."""
    import subprocess
    gh = lambda *a: subprocess.run(["gh", "api", *a], cwd=ROOT, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", check=True).stdout
    run = json.loads(gh("repos/{owner}/{repo}/actions/runs/%s" % run_id))
    jobs = json.loads(gh("repos/{owner}/{repo}/actions/runs/%s/jobs?per_page=100" % run_id))["jobs"]
    secs = {}
    for job in jobs:
        if not job["name"].startswith(PREFIX):
            continue
        for m in re.finditer(r"(?:ok|FAILED)  (.+?)  \((\d+)s; group at", gh("repos/{owner}/{repo}/actions/jobs/%s/logs" % job["id"])):
            secs[m.group(1)] = int(m.group(2))
    rec = {"run": int(run_id), "date": run["created_at"][:10], "branch": run["head_branch"],
           "event": run["event"], "lines": dict(sorted(secs.items()))}
    with open(os.path.join(ROOT, TIMINGS), "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("%s: %d line(s) from run %s (%s, %s)" % (TIMINGS, len(secs), run_id, rec["event"], rec["date"]))
    return 0


def selftest():
    fails = []

    def check(name, ok):
        print("  %s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails.append(name)

    p = parse("verify-x.py", "#!/usr/bin/env python3\n# ci-line: B4 | X (all) | \n")
    check("plain line", p["lines"] == [("B4", "X (all)", "python scripts/verify-x.py")])
    p = parse("verify-x.py", "# ci-line: C1 | X, part 1 | --part-selftest && --part 1\n")
    check("&& runs the script twice",
          p["lines"] == [("C1", "X, part 1", "python scripts/verify-x.py --part-selftest && python scripts/verify-x.py --part 1")])
    p = parse("verify-x.py", "# ci-line: E | X | && --selftest\n")
    check("empty first part", p["lines"] == [("E", "X", "python scripts/verify-x.py && python scripts/verify-x.py --selftest")])
    p = parse("verify-x.py", "x = 1  # ci-line: B4 | X | \n    # ci-line: B4 | Y | \n")
    check("only at the start of a line", p["lines"] == [])
    p = parse("verify-x.py", "# ci-line: B4 | X\n")
    check("two fields is an error", bool(p["errors"]) and not p["lines"])
    p = parse("verify-x.py", "# ci-line: Z9 | X | \n")
    check("unknown group is an error", bool(errors({"verify-x.py": p})))
    p = parse("verify-x.py", "# ci-held: withdrawn, held for a ruling\n")
    check("held reason", p["held"] == "withdrawn, held for a ruling" and not p["errors"])
    p = parse("verify-x.py", "# ci-held:\n")
    check("held with no reason is an error", bool(p["errors"]))
    p = parse("verify-x.py", "# ci-deps: data/a.json games/b/\n# ci-deps: c.txt\n")
    check("deps", p["deps"] == ["data/a.json", "games/b/", "c.txt"])
    m = matrix({"verify-x.py": parse("verify-x.py", "# ci-line: B4 | X | --a\n")})
    check("matrix entry", m == [{"name": dict((g, n) for g, n, _ in GROUPS)["B4"], "timeout": 8,
                                  "checks": "X|python scripts/verify-x.py --a\n"}])
    check("the repo's own headers parse", not errors())
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--github-output")
    ap.add_argument("--compare")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--record-timings", metavar="RUN_ID")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.record_timings:
        return record_timings(a.record_timings)
    if a.compare:
        return compare(a.compare)
    errs = errors()
    for e in errs:
        print("ERROR  " + e, file=sys.stderr)
    if errs:
        return 1
    m = matrix()
    if a.json:
        print(json.dumps(m, indent=1))
    elif a.github_output:
        with open(a.github_output, "a", encoding="utf-8") as f:
            f.write("groups=%s\n" % json.dumps(m))
        print("%d content group(s), %d line(s)" % (len(m), sum(c["checks"].count("\n") for c in m)))
    else:
        for g in groups():
            print("%s  (%s, %d min)" % (g["id"], g["name"], g["timeout"]))
            for l, c in g["lines"]:
                print("    %s|%s" % (l, c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
