#!/usr/bin/env python3
"""The "Content verifiers" groups, built from each script's own header (contract V, 7 Oct 2026; canon §7.8.2).

    python scripts/ci-groups.py                       # every content group and its lines
    python scripts/ci-groups.py --json                # the matrix, as the workflow's content job reads it
    python scripts/ci-groups.py --github-output FILE  # plan job: writes groups=<that JSON>
    python scripts/ci-groups.py --compare FILE        # equal, line for line, to FILE's static content groups?
    python scripts/ci-groups.py --check               # the budget check: fails past 80% (contract CI-BALANCE)
    python scripts/ci-groups.py --selftest            # header parsing and packing proofs, with planted faults
    python scripts/ci-groups.py --record-timings ID   # scripts/ci-timings.json from a main full run (gh CLI)
    python scripts/ci-groups.py --write-pack          # scripts/ci-pack.json: the pack, from the timings

Why. Until 7 Oct 2026 each content group listed its lines inside .github/workflows/check-site.yml, so every
new verifier edited that shared file: the cloud lane's #96, #97 and #100-#102 each did, and two of them
conflicted with home-lane PRs. Now a script declares the CI lines it contributes, in its own file:

    # ci-line: <label> | <args>               (a content verifier line)
    # ci-line: lock | <label> | <args>        (a line of the answer-lock tier; "content |" is the default)
    # ci-deps: <path> [<path> ...]          (optional: extra dependencies for scripts/ci-deps.py)
    # ci-held: <reason>                     (instead of a ci-line: deliberately not run in CI, and why)

one "# ci-line:" comment per line it contributes, each at the start of a line. <args> are the arguments to
"python scripts/<this file>"; "&&" joins several runs of the same script in one line, so
"--part-selftest && --part 1" is "python scripts/X.py --part-selftest && python scripts/X.py --part 1", and
" && --selftest" (nothing before the &&) is "python scripts/X.py && python scripts/X.py --selftest".

GROUPS ARE PACKED, NOT CHOSEN (contract CI-BALANCE, 9 Oct 2026; canon §7.8.1). Until then each ci-line named its
group, and groups filled and drifted as verifiers were added and pages grew: on 9 Oct group E reached 9m04s of
its 9m budget and turned main red though no verifier in it had changed, and the fix each time was another
hand-made group (B5, E2). Now a line names only its tier (TIERS below: content, or the answer-lock parts), and
pack() deals each tier's lines into as many groups as it takes, from each line's seconds on main's last full run
(scripts/ci-timings.json) plus the job's setup, so that every group is estimated at most 70% of its time budget
(the budget is 75% of the timeout, where the workflow fails a group). A line with no recorded time counts as
the tier's DEFAULT and is flagged until a main run times it. The pack is stable: scripts/ci-pack.json holds
each line's group, and a line moves only when its group would pass 70% (the fewest, smallest moves) or it is
new; so the job names do not churn. --check fails CI, on every PR, when any group's estimate passes 80% of
its budget (only a single line too big for any group can: split it with --part), naming the group and its
largest lines. After every full run on main, the "CI timings" job records the run's times and rewrites the
pack (commit "[skip ci]").

Old headers ("# ci-line: B4 | ..."): a hand-made group id is still accepted and read as its tier only (L* is
the lock tier, any other is content), so a branch made before CI-BALANCE still passes; the repo's own headers
use the new form. Lines run in the order: scripts by file name, then each script's headers in file order. The
site-wide jobs (tiers 1-2, site-wide checks, tier 4, shared assets) stay listed in the workflow.

Stdlib only.
"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "check-site.yml")
PREFIX = "Content verifiers"
TIMINGS = "scripts/ci-timings.json"     # each content line's seconds on a main full run (--record-timings)

PACK = "scripts/ci-pack.json"           # each line's group (--write-pack, after each main full run)
LOCK_PREFIX = "Answer lock"

# The tiers. Each tier's groups share one timeout; the workflow fails a group past 75% of it (its budget).
# Canon §7.8.1: no "Content verifiers" job past 4 minutes. A content group is packed to 70% of a 6-minute
# timeout's budget (3m09s with setup) and --check fails past 80% (3m36s), so even a fail is inside 4 minutes.
# The answer-lock parts are one line each (check-answer-lock.py --part i/n, 2.5-5 minutes, too long to share a
# job and not split by the packer: add a part as the roll-out grows); their jobs are "Answer lock", not content
# jobs, and keep the timeout that holds the longest part under 70%.
#   tier: (job name prefix, id prefix, timeout in minutes, default seconds for a line with no timing)
TIERS = {
    "content": ("Content verifiers", "", 6, 120),
    "lock": ("Answer lock", "L", 10, 300),
}
TIER_ORDER = ["content", "lock"]
TARGET, FAIL = 0.70, 0.80          # of a group's budget: pack to TARGET; --check fails past FAIL
SETUP = 25                         # seconds before a group's first line, when the timings do not record it
# The hand-made group ids before CI-BALANCE: still accepted in a header, as their tier only.
OLD_IDS = {"A", "B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4", "D1", "D2", "E", "E2",
           "L1", "L2", "L3", "L4", "L5"}


def budget(tier):
    return TIERS[tier][2] * 60 * 0.75


def tier_of(field):
    """The tier a header's first field names ('' is content), or None if it names nothing known."""
    if field in ("", "content"):
        return "content"
    if field in TIERS:
        return field
    if field in OLD_IDS:
        return "lock" if field.startswith("L") else "content"
    return None


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
    """{'lines': [(tier field, label, cmd)], 'deps': [paths], 'held': reason or None, 'errors': [str]}.
    The tier field is '' for a two-field line (content), else what the header wrote (a tier, or an old id)."""
    out = {"lines": [], "deps": [], "held": None, "errors": []}
    for m in LINE.finditer(text):
        parts = [p.strip() for p in m.group(1).split("|")]
        if len(parts) == 2:
            parts = [""] + parts
        if len(parts) != 3:
            out["errors"].append("%s: a ci-line is '<label> | <args>' or '<tier> | <label> | <args>': %r"
                                 % (name, m.group(0)))
            continue
        group, label, args = parts
        if not label:
            out["errors"].append("%s: a ci-line with no label: %r" % (name, m.group(0)))
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


def read_json(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def all_lines(hdrs=None):
    """[(tier, label, cmd)] in run order: scripts by file name, then header order. Unknown tiers are left out
    (errors() reports them)."""
    hdrs = headers() if hdrs is None else hdrs
    out = []
    for name in sorted(hdrs):
        for field, label, cmd in hdrs[name]["lines"]:
            t = tier_of(field)
            if t:
                out.append((t, label, cmd))
    return out


def gid_key(gid):
    m = re.match(r"^([A-Z]*)(\d+)$", gid)
    return (m.group(1), int(m.group(2))) if m else (gid, 0)


def pack(lines=None, timings=None, prev=None):
    """{tier: {group id: [labels]}}: each tier's lines dealt into groups estimated at most TARGET of the budget.

    Starts from prev (ci-pack.json: {tier: {label: id}}). A group over the target gives up lines until it is
    not: the smallest line that is enough on its own, else its largest, and again. Then every new or evicted
    line, largest first, joins the group with the most room that it fits, or opens the lowest free id. A line
    alone in its group stays there however long it is (--check judges it). Deterministic: the same inputs give
    the same pack."""
    lines = all_lines() if lines is None else lines
    timings = read_json(TIMINGS) if timings is None else timings
    prev = read_json(PACK) if prev is None else prev
    secs, setup = timings.get("lines", {}), timings.get("setup", SETUP)
    out = {}
    for tier in TIER_ORDER:
        _, pre, _, default = TIERS[tier]
        mine = [l for t, l, _ in lines if t == tier]
        if not mine:
            continue
        est = {l: secs.get(l, default) for l in mine}
        target = TARGET * budget(tier)
        old = prev.get(tier, {})
        groups, loose = {}, []
        for l in mine:
            g = old.get(l)
            if g and re.match(r"^%s\d+$" % pre, g):
                groups.setdefault(g, []).append(l)
            else:
                loose.append(l)
        total = lambda g: setup + sum(est[x] for x in groups[g])
        for g in sorted(groups, key=gid_key):
            while len(groups[g]) > 1 and total(g) > target:
                over = total(g) - target
                enough = [x for x in groups[g] if est[x] >= over]
                x = (min(enough, key=lambda x: (est[x], x)) if enough
                     else max(groups[g], key=lambda x: (est[x], x)))
                groups[g].remove(x)
                loose.append(x)
        for x in sorted(loose, key=lambda x: (-est[x], x)):
            fit = [g for g in groups if total(g) + est[x] <= target]
            if fit:
                g = max(fit, key=lambda g: (target - total(g), [-n for n in gid_key(g)[1:]]))
            else:
                n = 1
                while "%s%d" % (pre, n) in groups:
                    n += 1
                g = "%s%d" % (pre, n)
                groups[g] = []
            groups[g].append(x)
        out[tier] = {g: groups[g] for g in sorted(groups, key=gid_key) if groups[g]}
    return out


def groups(hdrs=None, timings=None, prev=None):
    """[{'id', 'tier', 'name', 'timeout', 'lines': [(label, cmd)]}] by tier, then id; lines in run order."""
    lines = all_lines(hdrs)
    order = {l: i for i, (_, l, _) in enumerate(lines)}
    cmd = {l: c for _, l, c in lines}
    out = []
    for tier, gs in pack(lines, timings, prev).items():
        prefix, _, timeout, _ = TIERS[tier]
        for g, labels in gs.items():
            out.append({"id": g, "tier": tier, "name": "%s %s" % (prefix, g), "timeout": timeout,
                        "lines": [(l, cmd[l]) for l in sorted(labels, key=order.get)]})
    return out


def estimate(g, timings=None):
    """(estimated seconds, [labels with no timing]) for a group: setup plus its lines (no timing: the default)."""
    timings = read_json(TIMINGS) if timings is None else timings
    secs = timings.get("lines", {})
    default = TIERS[g["tier"]][3]
    return (timings.get("setup", SETUP) + sum(secs.get(l, default) for l, _ in g["lines"]),
            [l for l, _ in g["lines"] if l not in secs])


def budget_faults(gs=None, timings=None):
    """[fault]: every group whose estimate passes FAIL of its budget, naming its largest lines."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    secs = timings.get("lines", {})
    faults = []
    for g in gs:
        est, _ = estimate(g, timings)
        b = budget(g["tier"])
        if est > FAIL * b:
            big = sorted(g["lines"], key=lambda lc: -secs.get(lc[0], TIERS[g["tier"]][3]))[:3]
            faults.append("%s: estimated %ds, past %d%% of its %ds budget (%d%%). Largest: %s. A line this long "
                          "cannot share a job: split its script (--part, --shard)."
                          % (g["name"], est, FAIL * 100, b, 100 * est / b,
                             "; ".join("%s %ss" % (l, secs.get(l, "no timing, counted as %d" % TIERS[g["tier"]][3]))
                                       for l, _ in big)))
    return faults


def write_pack(gs=None):
    gs = groups() if gs is None else gs
    rec = {}
    for g in gs:
        rec.setdefault(g["tier"], {}).update({l: g["id"] for l, _ in g["lines"]})
    with open(os.path.join(ROOT, PACK), "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print("%s: %d group(s), %d line(s)" % (PACK, len(gs), sum(len(g["lines"]) for g in gs)))
    return 0


def matrix(hdrs=None, timings=None, prev=None):
    """The content job's matrix include list: one entry per packed group."""
    return [{"name": g["name"], "timeout": g["timeout"],
             "checks": "".join("%s|%s\n" % l for l in g["lines"])}
            for g in groups(hdrs, timings, prev) if g["lines"]]


def errors(hdrs=None):
    """Header faults: malformed lines, unknown group names."""
    hdrs = headers() if hdrs is None else hdrs
    errs = []
    for name, info in sorted(hdrs.items()):
        errs += info["errors"]
        for group, label, _ in info["lines"]:
            if tier_of(group) is None:
                errs.append("%s: ci-line names %r, which is not a tier (%s; or leave it out for content)"
                            % (name, group, ", ".join(TIER_ORDER)))
            if "|" in label:
                errs.append("%s: a label may not contain '|'" % name)
        if info["held"] and info["lines"]:
            errs.append("%s: declares both ci-held and ci-line" % name)
    seen = {}
    for name, info in sorted(hdrs.items()):
        for _, label, _ in info["lines"]:
            if label in seen:
                errs.append("%s: label %r is also %s's: labels key the timings and the pack" % (name, label, seen[label]))
            seen.setdefault(label, name)
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
    out = [(n, False, l, c) for n, l, c in static_checks()
           if not n.startswith(PREFIX) and not n.startswith(LOCK_PREFIX)]
    for g in groups():
        out += [(g["name"], True, l, c) for l, c in g["lines"]]
    return out


def ci_text():
    """Every command CI runs, one per line: for checks that ask 'does CI run this?' by searching for it."""
    return "\n".join(c for _, _, _, c in all_checks()) + "\n"


def compare(path):
    """Contract V's proof: the headers give exactly the static content lines of the workflow at `path`."""
    old = sorted((n, l, c) for n, l, c in static_checks(path) if n.startswith(PREFIX) or n.startswith(LOCK_PREFIX))
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
    job log's 'ok  <label>  (Ns; group at ...)' lines, and the longest setup (a group's total less its lines).
    Run by the "CI timings" job after every full run on main; --write-pack then repacks from it."""
    import subprocess
    gh = lambda *a: subprocess.run(["gh", "api", *a], cwd=ROOT, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", check=True).stdout
    run = json.loads(gh("repos/{owner}/{repo}/actions/runs/%s" % run_id))
    jobs = json.loads(gh("repos/{owner}/{repo}/actions/runs/%s/jobs?per_page=100" % run_id))["jobs"]
    secs, setups = {}, []
    for job in jobs:
        if not (job["name"].startswith(PREFIX) or job["name"].startswith(LOCK_PREFIX)):
            continue
        log = gh("repos/{owner}/{repo}/actions/jobs/%s/logs" % job["id"])
        mine = [(m.group(1), int(m.group(2))) for m in re.finditer(r"(?:ok|FAILED)  (.+?)  \((\d+)s; group at", log)]
        secs.update(mine)
        tot = re.findall(r"group total: (\d+)m(\d+)s of", log)
        if tot and mine:
            setups.append(int(tot[-1][0]) * 60 + int(tot[-1][1]) - sum(t for _, t in mine))
    rec = {"run": int(run_id), "date": run["created_at"][:10], "branch": run["head_branch"],
           "event": run["event"], "setup": max(setups) if setups else SETUP, "lines": dict(sorted(secs.items()))}
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
    p = parse("verify-x.py", "# ci-line: X (all) | --a\n")
    check("two fields: a content line", p["lines"] == [("", "X (all)", "python scripts/verify-x.py --a")]
          and tier_of("") == "content")
    check("lock tier, and old ids read as their tier",
          tier_of("lock") == "lock" and tier_of("L3") == "lock" and tier_of("B4") == "content" and tier_of("E2") == "content")
    p = parse("verify-x.py", "# ci-line: a | b | c | d\n")
    check("four fields is an error", bool(p["errors"]) and not p["lines"])
    p = parse("verify-x.py", "# ci-line: Z9 | X | \n")
    check("unknown tier is an error", bool(errors({"verify-x.py": p})))
    two = {"verify-x.py": parse("verify-x.py", "# ci-line: X | \n"), "verify-y.py": parse("verify-y.py", "# ci-line: X | \n")}
    check("a label twice is an error", bool(errors(two)))
    p = parse("verify-x.py", "# ci-held: withdrawn, held for a ruling\n")
    check("held reason", p["held"] == "withdrawn, held for a ruling" and not p["errors"])
    p = parse("verify-x.py", "# ci-held:\n")
    check("held with no reason is an error", bool(p["errors"]))
    p = parse("verify-x.py", "# ci-deps: data/a.json games/b/\n# ci-deps: c.txt\n")
    check("deps", p["deps"] == ["data/a.json", "games/b/", "c.txt"])
    m = matrix({"verify-x.py": parse("verify-x.py", "# ci-line: X | --a\n")}, {"lines": {}}, {})
    check("matrix entry", m == [{"name": "Content verifiers 1", "timeout": TIERS["content"][2],
                                  "checks": "X|python scripts/verify-x.py --a\n"}])

    # Packing (contract CI-BALANCE). target = 70% of 270s = 189s; fail = 80% = 216s; setup 20s.
    T = lambda d: {"setup": 20, "lines": d}
    L = lambda *names: [("content", n, "c " + n) for n in names]
    est = lambda gs, t: [estimate(g, t)[0] for g in gs]
    t = T({"a": 100, "b": 60, "c": 50, "d": 40, "e": 30})
    pk = pack(L("a", "b", "c", "d", "e"), t, {})["content"]
    check("every group at most 70%%: %s" % pk,
          all(20 + sum(t["lines"][x] for x in v) <= 0.7 * 270 for v in pk.values()) and
          sorted(x for v in pk.values() for x in v) == ["a", "b", "c", "d", "e"])
    prev = {"content": {x: g for g, v in pk.items() for x in v}}
    check("stable: the same inputs give the same pack", pack(L("a", "b", "c", "d", "e"), t, prev)["content"] == pk)
    t2 = T(dict(t["lines"], f=10))
    pk2 = pack(L("a", "b", "c", "d", "e", "f"), t2, prev)["content"]
    moved = [x for g, v in pk.items() for x in v if x not in pk2.get(g, [])]
    check("a new line moves no other line", not moved and any("f" in v for v in pk2.values()))
    t3 = T(dict(t["lines"], c=120))        # c drifts: its group passes 70%
    pk3 = pack(L("a", "b", "c", "d", "e"), t3, prev)["content"]
    moved3 = [x for g, v in pk.items() for x in v if x not in pk3.get(g, [])]
    check("drift: only what must move moves (%s), and every group is back under 70%%" % moved3,
          len(moved3) == 1 and all(20 + sum(t3["lines"][x] for x in v) <= 0.7 * 270 for v in pk3.values()))
    check("no timing: the tier's default (%ds)" % TIERS["content"][3],
          estimate({"tier": "content", "lines": [("new", "")]}, T({}))[0] == 20 + TIERS["content"][3])
    hd = {"verify-x.py": parse("verify-x.py", "".join("# ci-line: %s | \n" % x for x in "abcde"))}
    check("--check passes a packed tier", not budget_faults(groups(hd, t, prev), t))
    plant = T(dict(t["lines"], a=400))  # PLANT: one inflated timing, a line too long for any group
    f = budget_faults(groups(hd, plant, prev), plant)
    check("--check fails on one inflated timing, naming the group and its largest line: %s" % (f[:1],),
          len(f) == 1 and "Content verifiers" in f[0] and "a 400s" in f[0])
    lk = pack([("lock", "p%d" % i, "c") for i in (1, 2)], T({"p1": 280, "p2": 200}), {})["lock"]
    check("lock tier: its own L ids, one long part per group", sorted(lk) == ["L1", "L2"])
    check("the repo's own headers parse", not errors())
    check("the repo's pack passes --check", not budget_faults())
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--github-output")
    ap.add_argument("--compare")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--record-timings", metavar="RUN_ID")
    ap.add_argument("--write-pack", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.record_timings:
        return record_timings(a.record_timings)
    if a.write_pack:
        return write_pack()
    if a.check:
        timings = read_json(TIMINGS)
        gs = groups(timings=timings)
        for g in gs:
            est, missing = estimate(g, timings)
            b = budget(g["tier"])
            print("%-22s %2d line(s)  estimated %4ds of %4ds budget (%3d%%)%s" % (
                g["name"], len(g["lines"]), est, b, 100 * est / b,
                "" if not missing else "  NO TIMING (counted as %ds each): %s" % (TIERS[g["tier"]][3], "; ".join(missing))))
        faults = budget_faults(gs, timings)
        for x in faults:
            print("FAIL  " + x)
        print("check: %s (pack to %d%% of each budget; fail past %d%%; timings from main run %s)"
              % ("FAILED" if faults else "PASS", TARGET * 100, FAIL * 100, timings.get("run")))
        return 1 if faults else 0
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
            print("%s  (%s min, estimated %ds)" % (g["name"], g["timeout"], estimate(g)[0]))
            for l, c in g["lines"]:
                print("    %s|%s" % (l, c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
