#!/usr/bin/env python3
"""The "Content verifiers" groups, built from each script's own header (contract V, 7 Oct 2026; canon §7.8.2).

    python scripts/ci-groups.py                       # every content group and its lines
    python scripts/ci-groups.py --json                # the matrix, as the workflow's content job reads it
    python scripts/ci-groups.py --github-output FILE  # plan job: writes groups=<that JSON>
    python scripts/ci-groups.py --compare FILE        # equal, line for line, to FILE's static content groups?
    python scripts/ci-groups.py --check               # the budget check: fails past 80% (contract CI-BALANCE)
    python scripts/ci-groups.py --selftest            # header parsing and packing proofs, with planted faults
    python scripts/ci-groups.py --record-timings ID   # scripts/ci-timings.json from a main full run (gh CLI)
    python scripts/ci-groups.py --record-and-pack ID --from-dir D  # the timings job: record, repack, check, write only if it passes
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
(the budget is 75% of the timeout, where the workflow warns about a group: TIMING-GATE). A line with no recorded time counts as
the tier's DEFAULT and is flagged until a main run times it. The pack is stable: scripts/ci-pack.json holds
each line's group, and a line moves only when its group would pass 70% (the fewest, smallest moves) or it is
new; so the job names do not churn. --check fails CI, on every PR, when any group's estimate passes 80% of
its budget (only a single line too big for any group can: split it with --part), naming the group and its
largest lines. After every full run on main, the "CI timings" job records the run's times and rewrites the
pack (commit "[skip ci]").

TIMINGS ARE A MEDIAN, AND A PACK IS COMMITTED ONLY IF IT PASSES --check (contract CI-TIMINGS-MEDIAN, 12 Oct 2026;
canon §7.8.1). Until then ci-timings.json held ONE run's figures. Main run 785 (38224711265) had one slow group,
so its recorded setup (the longest group's total less its lines) was 125 s against 18-28 s in the eleven records
before it; the repack against that setup left twelve groups past 80% and turned --check, and so every PR, red.
Now ci-timings.json keeps the last HISTORY (5) main runs under "history" (each: run, date, branch, event, setup,
lines), and the top-level "run", "date", "setup" and "lines" that every reader uses are the MEDIANS over them:
per line over the runs that timed it (a line timed in fewer runs takes the median of what it has), and the
setup as the median of each run's own setup (a run's setup stays its longest group's, which is cautious within
a run). A median of 5 takes no notice of one slow run and moves when three of five are slow. The timings job
runs --record-and-pack, which works the new timings and pack out in memory, applies --check's test to them, and
writes neither file if it fails (the job then fails, so a genuine overrun shows on main instead of in every PR).
Even-sized histories round the middle pair up.

A LINE IS JUDGED ALONE, AND A SLOWER SETUP IS A WARNING (contract PER-LINE-LIMIT, 20 Oct 2026; canon §7.8.1). The packer
moves lines between groups but cannot split one, so a group holding one long line is only as safe as that line.
Content verifiers 1 and 2 each held one (Just Pythag It, Bruv part 4, 164 s; Free Daily Pizza, 171 s) at 68% and 71% of
a 270 s budget, and when setup ran 53, 59 and 87 s (main runs 39390699573, 39398807202, 39401811389, against about 20 s
before and since) the median-setup estimate crossed 80%, the timings job refused the pack, and main went red with no
code change to blame and nothing a repack could fix. So --check also failed (until LINE-LIMIT-SCOPE, below), on every PR, any
single timed line whose median plus the median setup passes TARGET (70%) of its group's budget, naming the line and
its figures; split its script (--part). And when the timings job's pack is refused, record-and-pack asks why: if the
same pack passes at the PREVIOUS median setup (the committed ci-timings.json's), only setup moved it, and the job warns,
writes nothing and does not fail (exit status SETUP_ONLY, 2, which the workflow reads as "stop, commit nothing"). Any
other refusal still fails the job, as before.

A LINE OVER THE LIMIT FAILS ONLY THE PR THAT SELECTS IT (contract LINE-LIMIT-SCOPE, Jon's ruling 21 Oct 2026; canon §7.8.1).
PER-LINE-LIMIT set the line limit equal to the pack target, with no margin, and counted the moving median setup, so a line
at 69% tipped over on noise: main run 39559284220 (setup median 57 s) put four unchanged lines over it (Shape Shifter,
Equation Builder part 1, Just Pythag It, Bruv part 2, Answer lock part 1), the timings job refused the pack and main went
red. Now a line over the limit is a SPLIT CANDIDATE. On main (--record-and-pack) it never refuses the pack: it is printed
as a warning and written to ci-pack.json under "split-candidates" (label, median, setup, percent), and the pack commits.
--check fails on it only when the change being checked selects the line's script, as CI's plan job selects it
(scripts/ci-deps.py select(), on the files changed since the pull request's base: read from the run's own event, so the
plan job's interface is unchanged; locally, since the merge base with origin/main); any other line over the limit is a
warning naming it. A change that selects every verifier (CI itself) selects every line. The group rule (past 80%) still
refuses the pack and fails --check everywhere, and the setup-only warning (exit 2) is unchanged.

Old headers ("# ci-line: B4 | ..."): a hand-made group id is still accepted and read as its tier only (L* is
the lock tier, any other is content), so a branch made before CI-BALANCE still passes; the repo's own headers
use the new form. Lines run in the order: scripts by file name, then each script's headers in file order. The
site-wide jobs (tiers 1-2, site-wide checks, tier 4, shared assets) stay listed in the workflow.

Stdlib only.
"""
import argparse, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "check-site.yml")
PREFIX = "Content verifiers"
TIMINGS = "scripts/ci-timings.json"     # each content line's seconds on a main full run (--record-timings)

REGIONS = "scripts/ci-timings-regions.json"   # per line, per runner region, the last REGION_KEEP times (--record-regions)

PACK = "scripts/ci-pack.json"           # each line's group (--write-pack, after each main full run)
LOCK_PREFIX = "Answer lock"

# The tiers. Each tier's groups share one timeout; the workflow warns about a group past 75% of it (its budget).
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
# A container job's hang guard is its group's timeout plus this many minutes (matrix.job_timeout in check-site.yml).
# GitHub counts the image pull ("Initialize containers") inside timeout-minutes; the group's budget (75% of
# `timeout`) runs from the first step, after the pull. Main run 802 (12 Oct 2026): Content verifiers 33 spent 379 s
# initialising against its 360 s timeout and was cancelled before it ran a check.
PULL_ALLOWANCE = 10
TARGET, FAIL = 0.70, 0.80          # of a group's budget: pack to TARGET; --check fails past FAIL
SETUP = 25                         # seconds before a group's first line, when the timings do not record it
HISTORY = 5                        # main runs kept in ci-timings.json; the estimates are their medians
REGION_KEEP = 10                   # times kept per line per region in ci-timings-regions.json (REGION-HISTORY, 15 Oct 2026)
REGION_RUNS = 20                   # run ids remembered there, so the same run recorded twice is counted once
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
                        "job_timeout": timeout + PULL_ALLOWANCE,
                        "lines": [(l, cmd[l]) for l in sorted(labels, key=order.get)]})
    return out


def estimate(g, timings=None):
    """(estimated seconds, [labels with no timing]) for a group: setup plus its lines (no timing: the default)."""
    timings = read_json(TIMINGS) if timings is None else timings
    secs = timings.get("lines", {})
    default = TIERS[g["tier"]][3]
    return (timings.get("setup", SETUP) + sum(secs.get(l, default) for l, _ in g["lines"]),
            [l for l, _ in g["lines"] if l not in secs])


def script_of(cmd):
    """The verifier a line runs ('scripts/<name>.py', as ci-deps.py names it), or None."""
    m = re.search(r"scripts/[\w.-]+\.py", cmd)
    return m.group(0) if m else None


def split_candidates(gs=None, timings=None):
    """[{label, median, setup, percent, group, script, budget}]: every timed line whose median plus the median setup passes
    TARGET of its group's budget (PER-LINE-LIMIT, 20 Oct 2026; LINE-LIMIT-SCOPE, 21 Oct 2026). The packer can move a line
    between groups but cannot split it, so a line this size is one slow setup from failing a group that nothing can
    repack: split its script. A line with no timing counts as its tier's default and is not judged here (the group check
    and the NO TIMING flag cover it). By label, so the pack's list is stable."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    secs, setup = timings.get("lines", {}), timings.get("setup", SETUP)
    out = []
    for g in gs:
        b = budget(g["tier"])
        for l, c in g["lines"]:
            if l in secs and secs[l] + setup > TARGET * b:
                out.append({"label": l, "median": secs[l], "setup": setup, "percent": int(100 * (secs[l] + setup) / b),
                            "group": g["name"], "script": script_of(c), "budget": b})
    return sorted(out, key=lambda c: c["label"])


def line_message(c):
    return ("%s: line over the per-line limit: %s %ss (median) + %ss setup = %ds, %d%% of its %ds budget; "
            "the limit is %d%% (%ds). Split its script (--part, --shard)."
            % (c["group"], c["label"], c["median"], c["setup"], c["median"] + c["setup"], c["percent"], c["budget"],
               TARGET * 100, TARGET * c["budget"]))


def line_faults(gs=None, timings=None, selected=()):
    """(faults, warnings) for the split candidates (LINE-LIMIT-SCOPE). `selected` is the set of scripts the change being
    checked selects (ci-deps.py's names), True when it selects every verifier, or () for none (main, the timings job): a
    candidate whose script is selected is a fault, any other a warning, so runner noise on an unchanged line never fails
    main or a PR that does not touch it."""
    faults, warns = [], []
    for c in split_candidates(gs, timings):
        if selected is True or c["script"] in selected:
            faults.append(line_message(c) + " This change selects its verifier (%s)." % c["script"])
        else:
            warns.append("split candidate (a warning, not a failure: nothing checked here selects %s): %s"
                         % (c["script"], line_message(c)))
    return faults, warns


def budget_faults(gs=None, timings=None, selected=()):
    """[fault]: every split candidate the change selects (line_faults), and every group whose estimate passes FAIL of
    its budget, naming its largest lines. The group rule holds whatever is selected: it is what refuses a pack on main."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    secs = timings.get("lines", {})
    faults = line_faults(gs, timings, selected)[0]
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


def warn(msgs):
    """Print each warning; in a GitHub Actions run, also as a ::warning:: annotation, so a split candidate shows on the run."""
    for x in msgs:
        print("WARN  " + x)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print("::warning title=split candidate::" + x)


def pr_selection(env=None, deps=None):
    """(selected, how) for --check: the scripts the change being checked selects, as CI's plan job selects them
    (scripts/ci-deps.py select() on the files changed since the base), True for every verifier, or () for none.
    In a GitHub Actions run that is not a pull request (main, the schedule, a manual run): (). In a pull request run: the
    base is the event's pull_request.base.sha, the plan job's own BASE, read from GITHUB_EVENT_PATH, so the plan job's
    interface is unchanged. Locally: the merge base with origin/main. If the base cannot be read, every line counts as
    selected: a check that cannot tell fails strictly rather than passes. `deps` is ci-deps.py's module (loaded here when
    None; the self-test passes a stand-in, because its dependency map takes about a minute to build)."""
    env = os.environ if env is None else env
    import importlib.util, subprocess
    if env.get("GITHUB_ACTIONS") == "true":
        event = env.get("GITHUB_EVENT_NAME", "")
        if event != "pull_request":
            return (), "a %s run, not a pull request: no line is selected" % (event or "non-PR")
        try:
            with open(env["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
                base = json.load(f)["pull_request"]["base"]["sha"]
        except (KeyError, OSError, ValueError, TypeError):
            return True, "the pull request's base could not be read from the event: every line counts as selected"
    else:
        r = subprocess.run(["git", "merge-base", "origin/main", "HEAD"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            return True, "no merge base with origin/main: every line counts as selected"
        base = r.stdout.strip()
    if deps is None:
        spec = importlib.util.spec_from_file_location("ci_deps", os.path.join(SCRIPTS, "ci-deps.py"))
        deps = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(deps)
    try:
        changed = deps.changed_since(base)
    except Exception as e:  # git failed: the base is not in this checkout
        return True, "the files changed since %s could not be listed (%s): every line counts as selected" % (base[:10], e)
    run_all, reasons, picked = deps.select(changed)
    if run_all:
        return True, "this change selects every verifier (%s)" % (reasons[0] if reasons else "run all")
    return set(picked), "this change (%d file(s) since %s) selects %d verifier(s)" % (len(changed), base[:10], len(picked))


def pack_record(gs, timings=None):
    """ci-pack.json's content: {tier: {label: group id}}, and "split-candidates" (LINE-LIMIT-SCOPE): each line over the
    per-line limit, as {label, median, setup, percent}, for the lane that splits it. pack() reads only the tiers."""
    rec = {}
    for g in gs:
        rec.setdefault(g["tier"], {}).update({l: g["id"] for l, _ in g["lines"]})
    rec["split-candidates"] = [{k: c[k] for k in ("label", "median", "setup", "percent")}
                               for c in split_candidates(gs, timings)]
    return rec


def write_pack(gs=None, timings=None):
    gs = groups() if gs is None else gs
    rec = pack_record(gs, timings)
    with open(os.path.join(ROOT, PACK), "w", encoding="utf-8", newline="\n") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print("%s: %d group(s), %d line(s), %d split candidate(s)"
          % (PACK, len(gs), sum(len(g["lines"]) for g in gs), len(rec["split-candidates"])))
    return 0


def matrix(hdrs=None, timings=None, prev=None):
    """The content job's matrix include list: one entry per packed group."""
    return [{"name": g["name"], "timeout": g["timeout"], "job_timeout": g["job_timeout"],
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


def static_timeouts(path=WORKFLOW):
    """[(job name, timeout, job_timeout or None)] for the static matrix entries (a plain reader, no YAML library),
    plus the `timeout-minutes:` each container job uses, as [(line, expression)] under the key None."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    out, cur = [], None
    for raw in text.splitlines():
        m = re.match(r"^\s*- name: (.+)$", raw)
        if m:
            cur = [m.group(1).strip(), None, None]
            out.append(cur)
            continue
        m = re.match(r"^\s*(job_)?timeout: (\d+)\s*$", raw)
        if m and cur:
            cur[2 if m.group(1) else 1] = int(m.group(2))
    return [tuple(e) for e in out if e[1] is not None or e[2] is not None]


def container_job_guards(path=WORKFLOW):
    """The `timeout-minutes:` expressions of the jobs that take a matrix timeout (the container jobs)."""
    with open(path, encoding="utf-8") as f:
        return [m.group(1).strip() for m in re.finditer(r"^\s*timeout-minutes: (\$\{\{ matrix\.\w+ \}\})\s*$",
                                                        f.read(), re.M)]


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


def read_run(run_id, from_dir=None):
    """One finished run's record, from its content and lock jobs: each line's seconds, read from the
    'ok  <label>  (Ns; group at ...)' lines, and the longest setup (a group's total less its lines).
    {"run", "date", "branch", "event", "setup", "lines", "regions"}, or None when there is nothing to read. "regions" maps
    each line to the Azure region of the runner that timed it ('unknown' when the job did not say); nothing reads it
    but the warning and the persistence report, and a record from before it (no "regions") reads as 'unknown'.
    On main the "CI timings" job passes --from-dir: each group job saves those lines as an artifact
    (ci-timing-*), downloaded into one folder, because the job-log API failed for the workflow's own token
    on every fetch (9 Oct, runs 37964707421, 37965228268, 37966843652). From a workstation, without
    --from-dir, the logs are read through the gh CLI instead."""
    def parse(text):
        mine = [(m.group(1), int(m.group(2))) for m in re.finditer(r"(?:ok|FAILED)  (.+?)  \((\d+)s; group at", text)]
        tot = re.findall(r"group total: (\d+)m(\d+)s of", text)
        return mine, (int(tot[-1][0]) * 60 + int(tot[-1][1]) - sum(t for _, t in mine)) if tot and mine else None

    def region_of(text):
        """The runner's Azure region: the 'region: x' line the group step saves in its timing file, or the 'Region: x'
        line the runner prints at the head of a job log; 'unknown' when neither is there."""
        m = re.search(r"^region: ([a-z0-9]+)\s*$", text, re.M) or re.search(r"Region: ([A-Za-z0-9]+)\s*$", text, re.M)
        return m.group(1).lower() if m else "unknown"

    texts = []
    if from_dir:
        for dirpath, _, files in os.walk(from_dir):
            for fn in sorted(files):
                with open(os.path.join(dirpath, fn), encoding="utf-8", errors="replace") as f:
                    text = f.read()
                job = text.split("\n", 1)[0].strip()
                if job.startswith(PREFIX) or job.startswith(LOCK_PREFIX):
                    texts.append(text)
        run = {"created_at": os.environ.get("RUN_DATE", time.strftime("%Y-%m-%d")),
               "head_branch": os.environ.get("GITHUB_REF_NAME", ""), "event": os.environ.get("GITHUB_EVENT_NAME", "")}
        if not texts:
            print("record-timings: no content or lock timing files under %s" % from_dir)
            return None
    else:
        import subprocess

        def gh(path):
            r = subprocess.run(["gh", "api", path], cwd=ROOT, capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if r.returncode:
                raise RuntimeError("gh api %s: %s" % (path, (r.stderr or r.stdout).strip()[:300]))
            return r.stdout
        run = json.loads(gh("repos/{owner}/{repo}/actions/runs/%s" % run_id))
        jobs = json.loads(gh("repos/{owner}/{repo}/actions/runs/%s/jobs?per_page=100" % run_id))["jobs"]
        texts = [gh("repos/{owner}/{repo}/actions/jobs/%s/logs" % j["id"]) for j in jobs
                 if j["name"].startswith(PREFIX) or j["name"].startswith(LOCK_PREFIX)]
    secs, setups, regions = {}, [], {}
    for text in texts:
        mine, setup = parse(text)
        secs.update(mine)
        regions.update({label: region_of(text) for label, _ in mine})
        if setup is not None:
            setups.append(setup)
    rec = {"run": int(run_id), "date": run["created_at"][:10], "branch": run["head_branch"],
           "event": run["event"], "setup": max(setups) if setups else SETUP, "lines": dict(sorted(secs.items())),
           "regions": dict(sorted(regions.items()))}
    return rec


def median_int(xs):
    """The median of a non-empty list of numbers as a whole number; the middle pair of an even list rounds up."""
    xs = sorted(xs)
    n = len(xs)
    return int(xs[n // 2]) if n % 2 else int((xs[n // 2 - 1] + xs[n // 2] + 1) // 2)


def medians(history):
    """The timings every reader sees, from a list of run records (oldest first): the newest run's id, date,
    branch and event; the median setup; and each line's median over the runs that timed it."""
    last = history[-1]
    per = {}
    for r in history:
        for label, sec in r.get("lines", {}).items():
            per.setdefault(label, []).append(sec)
    return {"run": last["run"], "date": last["date"], "branch": last.get("branch", ""), "event": last.get("event", ""),
            "setup": median_int([r.get("setup", SETUP) for r in history]),
            "lines": {k: median_int(v) for k, v in sorted(per.items())}}


def add_run(existing, rec, keep=HISTORY):
    """The new ci-timings.json content: existing (the file's content) with the run record rec added to its history,
    the last `keep` runs kept, and the top-level fields the medians. A file from before the history (one run's
    figures at the top level) counts as one run of history; the same run twice is counted once."""
    hist = existing.get("history")
    if hist is None:
        hist = [{k: existing[k] for k in ("run", "date", "branch", "event", "setup", "lines") if k in existing}] \
            if existing.get("lines") else []
    hist = [r for r in hist if r.get("run") != rec["run"]] + [rec]
    hist = hist[-keep:]
    out = medians(hist)
    out["history"] = hist
    return out


def write_timings(timings):
    with open(os.path.join(ROOT, TIMINGS), "w", encoding="utf-8", newline="\n") as f:
        json.dump(timings, f, indent=1, ensure_ascii=False)
        f.write("\n")


def settle(existing, rec, hdrs=None, prev=None):
    """(timings, groups, faults): the timings with the run rec added, the groups packed from them (from prev, the
    current pack), and the faults that refuse that pack on main: the group rule only, since main selects no line and a
    line over the per-line limit is a split candidate, a warning (LINE-LIMIT-SCOPE). Nothing is written."""
    timings = add_run(existing, rec)
    gs = groups(hdrs, timings, read_json(PACK) if prev is None else prev)
    return timings, gs, budget_faults(gs, timings)


SETUP_ONLY = 2      # record_and_pack's exit status when only a slower setup refused the pack: a warning, not a failure


def commit(timings, gs, faults, writers=None, calm=None, prev_setup=0):
    """What the timings job does with settle()'s result. With no fault, write the timings and the pack (return 0); the
    pack carries the split candidates, which are warnings, never faults here (LINE-LIMIT-SCOPE).
    With a fault, write NOTHING, and say why: if `calm` (the faults the same pack has at the previous pack's median
    setup) is an empty list, setup alone moved it (a slow runner, not a slow line): warn and return SETUP_ONLY (the
    job warns and does not fail); any other fault returns 1 (the job fails). calm=None means the cause is unknown: 1.
    writers = (write_timings, write_pack), for the self-test."""
    wt, wp = writers or (write_timings, write_pack)
    if faults:
        for x in faults:
            print("FAIL  " + x)
        if calm is not None and not calm:
            print("record-and-pack: WARNING: setup alone moved these groups past the limit (they all pass at the previous "
                  "median setup, %ds); neither %s nor %s was written, and this is not a failure"
                  % (prev_setup, TIMINGS, PACK))
            return SETUP_ONLY
        print("record-and-pack: the pack for these timings fails --check%s; neither %s nor %s was written"
              % ("" if calm is None else " even at the previous median setup (%d fault(s): the lines grew)" % len(calm),
                 TIMINGS, PACK))
        return 1
    wt(timings)
    wp(gs, timings)
    return 0


def record_timings(run_id, from_dir=None):
    """Add a finished run to ci-timings.json (the file keeps the last HISTORY runs and their medians); no pack."""
    rec = read_run(run_id, from_dir)
    if rec is None:
        return 1
    write_timings(add_run(read_json(TIMINGS), rec))
    print("%s: %d line(s) from run %s (%s, %s); median of the last %d run(s)"
          % (TIMINGS, len(rec["lines"]), run_id, rec["event"], rec["date"], len(read_json(TIMINGS)["history"])))
    return 0


def calm_faults(existing, timings, gs, faults):
    """The cause test (PER-LINE-LIMIT): the faults the same pack gs has when the setup is the previous pack's median
    (existing's, the committed ci-timings.json) and every line keeps its new median. [] means the new setup alone
    moved the pack past the limit; a non-empty list means a line grew whatever the setup was. None when there is no
    fault to explain."""
    if not faults:
        return None
    return budget_faults(gs, dict(timings, setup=existing.get("setup", SETUP)))


def record_and_pack(run_id, from_dir=None):
    """The timings job: add the run, repack from the medians, apply the group rule, and write the timings and the
    pack only if it passes. A line over the per-line limit is printed as a warning and listed in the pack."""
    rec = read_run(run_id, from_dir)
    if rec is None:
        return 1
    existing = read_json(TIMINGS)
    timings, gs, faults = settle(existing, rec)
    print("run %s: setup %ds (median %ds of %d run(s)); %d line(s) timed" % (
        run_id, rec["setup"], timings["setup"], len(timings["history"]), len(rec["lines"])))
    warn(line_faults(gs, timings)[1])
    return commit(timings, gs, faults, calm=calm_faults(existing, timings, gs, faults),
                  prev_setup=existing.get("setup", SETUP))


def add_regions(existing, rec, keep=REGION_KEEP):
    """The new ci-timings-regions.json content (REGION-HISTORY): existing with the run record rec added. For each timed
    line it keeps, per region, the last `keep` seconds, oldest first; a line the run did not name a region for goes under
    "unknown". Pure, and independent of ci-timings.json and the packer: nothing in either reads this. The run ids
    recorded are remembered (the last REGION_RUNS) so the same run twice is counted once."""
    if rec["run"] in existing.get("runs", []):
        return existing
    lines = {k: {r: list(v) for r, v in d.items()} for k, d in existing.get("lines", {}).items()}
    for label, sec in rec["lines"].items():
        region = rec.get("regions", {}).get(label) or "unknown"
        lines.setdefault(label, {}).setdefault(region, []).append(sec)
        lines[label][region] = lines[label][region][-keep:]
    return {"keep": keep, "runs": (existing.get("runs", []) + [rec["run"]])[-REGION_RUNS:],
            "lines": {k: dict(sorted(d.items())) for k, d in sorted(lines.items())}}


def dump_regions(data):
    """The file's text: one line per timed line, its regions' times inline, so the file stays small and a diff reads."""
    out = ['{', ' "keep": %d,' % data["keep"], ' "runs": %s,' % json.dumps(data["runs"]), ' "lines": {']
    rows = ['  %s: %s' % (json.dumps(k, ensure_ascii=False), json.dumps(v, ensure_ascii=False))
            for k, v in data["lines"].items()]
    out.append(",\n".join(rows))
    out += [' }', '}', '']
    return "\n".join(out)


def write_regions(data):
    path = os.path.join(ROOT, REGIONS)
    with open(path + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        f.write(dump_regions(data))
    os.replace(path + ".tmp", path)          # never a half-written file


def record_regions(run_id, from_dir=None):
    """The timings job's second step: add the run to ci-timings-regions.json. It reads and writes only that file; the
    job treats a failure here as a warning (REGION-HISTORY), so nothing about ci-timings.json depends on it."""
    rec = read_run(run_id, from_dir)
    if rec is None:
        return 1
    existing = read_json(REGIONS)
    data = add_regions(existing, rec)
    write_regions(data)
    n = sum(len(d) for d in data["lines"].values())
    print("%s: run %s added; %d line(s), %d line/region record(s), %d bytes"
          % (REGIONS, run_id, len(data["lines"]), n, len(dump_regions(data).encode("utf-8"))))
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
                                  "job_timeout": TIERS["content"][2] + PULL_ALLOWANCE,
                                  "checks": "X|python scripts/verify-x.py --a\n"}])

    # Hang guard vs budget (contract CONTAINER-PULL-TIMEOUT): job_timeout = timeout + PULL_ALLOWANCE, everywhere.
    check("every emitted group: job_timeout = timeout + %d" % PULL_ALLOWANCE,
          all(g["job_timeout"] == g["timeout"] + PULL_ALLOWANCE for g in groups(hdrs=None)))
    st = static_timeouts()
    check("static matrix (%d entries): each has job_timeout = timeout + %d" % (len(st), PULL_ALLOWANCE),
          len(st) > 0 and all(t is not None and j == t + PULL_ALLOWANCE for _, t, j in st))
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        bad = os.path.join(td, "w.yml")      # PLANT: one entry's job_timeout one minute short, one missing
        with open(bad, "w", encoding="utf-8", newline='') as f:
            f.write("- name: A\n  timeout: 10\n  job_timeout: 19\n- name: B\n  timeout: 8\n")
        sb = static_timeouts(bad)
    check("PLANT: a static entry with job_timeout off by one, or missing, is caught: %s" % (sb,),
          sb == [("A", 10, 19), ("B", 8, None)]
          and [n for n, t, j in sb if j != t + PULL_ALLOWANCE] == ["A", "B"])
    check("both container jobs use matrix.job_timeout as timeout-minutes (and nothing else uses matrix.timeout there)",
          container_job_guards() == ["${{ matrix.job_timeout }}"] * 2)

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
    # Timings are the median of the last HISTORY main runs, and a pack that fails --check is not committed
    # (contract CI-TIMINGS-MEDIAN, after run 785's one slow group recorded a 125 s setup against 18-28 s).
    hd5 = {"verify-x.py": parse("verify-x.py", "".join("# ci-line: %s | \n" % x for x in "abcde"))}
    rn = lambda n, setup, lines: {"run": n, "date": "2026-10-%02d" % n, "branch": "main", "event": "push",
                                  "setup": setup, "lines": dict(lines)}
    flat = {x: 100 for x in "abcde"}
    check("median_int: odd, even rounds up, one", median_int([5, 1, 3]) == 3 and median_int([1, 2]) == 2
          and median_int([1, 2, 3, 4]) == 3 and median_int([7]) == 7)
    ex = {}
    for n, st in enumerate([22, 20, 24, 22], 1):
        ex = add_run(ex, rn(n, st, flat))
    tm, gs, fl = settle(ex, rn(5, 125, flat), hd5, {})
    alone = rn(5, 125, flat)                      # the old rule: the one run's own figures
    check("(a) one 125 s setup in five runs: the median setup is %ds and the pack passes --check: %s"
          % (tm["setup"], fl[:1]), tm["setup"] == 22 and len(tm["history"]) == 5 and not fl)
    check("(a) the same run alone (the old rule) fails --check, which is what turned every PR red",
          bool(budget_faults(groups(hd5, alone, {}), alone)))
    check("history keeps the last %d runs, oldest dropped, the same run twice counted once" % HISTORY,
          [h["run"] for h in add_run(tm, rn(6, 22, flat))["history"]] == [2, 3, 4, 5, 6]
          and len(add_run(tm, rn(5, 22, flat))["history"]) == 5 and add_run(tm, rn(6, 22, flat))["run"] == 6)
    leg = {k: v for k, v in rn(1, 30, flat).items()}      # a file from before the history: one run at the top level
    check("a file from before the history counts as one run", len(add_run(leg, rn(2, 20, flat))["history"]) == 2)
    check("a line timed in fewer runs takes the median of what it has",
          add_run(add_run({}, rn(1, 22, flat)), rn(2, 22, dict(flat, f=40)))["lines"]["f"] == 40)
    slow3 = {}
    for n, a in enumerate([60, 300, 60, 300], 1):
        slow3 = add_run(slow3, rn(n, 22, dict(flat, a=a)))
    tm3, gs3, fl3 = settle(slow3, rn(5, 22, dict(flat, a=300)), hd5, {})
    check("(b) a line slow in 3 of 5 runs moves its median to %s and is flagged: %s" % (tm3["lines"]["a"], fl3[:1]),
          tm3["lines"]["a"] == 300 and len(fl3) == 1 and "a 300s" in fl3[0])
    slow2 = {}
    for n, a in enumerate([60, 300, 60, 60], 1):
        slow2 = add_run(slow2, rn(n, 22, dict(flat, a=a)))
    tm2, gs2, fl2 = settle(slow2, rn(5, 22, dict(flat, a=300)), hd5, {})
    check("(b) a line slow in only 2 of 5 runs keeps its median (%s) and is not flagged" % tm2["lines"]["a"],
          tm2["lines"]["a"] == 60 and not fl2)
    wrote = []
    sink = (lambda t: wrote.append("timings"), lambda g, t: wrote.append("pack"))
    rc_bad = commit(tm3, gs3, fl3, sink)
    check("(c) a pack that fails --check is refused: exit 1, neither file written (%s)" % wrote, rc_bad == 1 and not wrote)
    rc_ok = commit(tm, gs, fl, sink)
    check("(c) a pack that passes is written (timings, then pack)", rc_ok == 0 and wrote == ["timings", "pack"])
    # LINE-LIMIT-SCOPE (Jon, 21 Oct 2026; PER-LINE-LIMIT, 20 Oct, before it): a line past 70% of its budget with the median
    # setup is a split candidate. It fails --check only where the change selects its script; on main (nothing selected)
    # and on a PR that selects only other verifiers it is a warning. Setup 20 s, budget 270 s: the limit is 189 s, so a
    # line of 169 s is at it (189) and 170 s is over (190). Line a is verify-x.py's; b to e are verify-y.py's.
    hs = {"verify-x.py": parse("verify-x.py", "# ci-line: a | \n"),
          "verify-y.py": parse("verify-y.py", "".join("# ci-line: %s | \n" % x for x in "bcde"))}
    one = lambda a: T(dict(t["lines"], a=a))
    X, Y = {"scripts/verify-x.py"}, {"scripts/verify-y.py"}
    for sec, want in ((168, False), (169, False), (170, True)):
        ft = one(sec)
        check("per-line limit, line selected: a line of %ds (+20s setup) %s" % (sec, "fails" if want else "passes"),
              bool(budget_faults(groups(hs, ft, {}), ft, X)) == want)
    ft = one(170)
    g170 = groups(hs, ft, {})
    fl, wn = line_faults(g170, ft, X)
    check("PLANT: a 170 s line the PR selects fails, naming the line, its figures and its script, once: %s" % (fl[:1],),
          len(fl) == 1 and "a 170s (median) + 20s setup = 190s" in fl[0] and "scripts/verify-x.py" in fl[0]
          and "Content verifiers" in fl[0] and "70%" in fl[0] and not wn and len(budget_faults(g170, ft, X)) == 1)
    fl, wn = line_faults(g170, ft, Y)
    check("the same line on a PR that does not select it: a warning naming it a split candidate, no fault: %s" % (wn[:1],),
          not fl and len(wn) == 1 and "split candidate" in wn[0] and "a 170s" in wn[0] and not budget_faults(g170, ft, Y))
    check("on main (nothing selected) the same line is a warning, not a fault",
          not budget_faults(g170, ft) and len(line_faults(g170, ft)[1]) == 1)
    check("a change that selects every verifier (CI itself) selects the line: it fails",
          len(budget_faults(g170, ft, True)) == 1)
    f400 = one(400)
    check("PLANT: past 80% the group rule fails whatever is selected (a 400 s line; main, unselected, selected, all)",
          all(any("past 80%" in x for x in budget_faults(groups(hs, f400, {}), f400, sel)) for sel in ((), Y, X, True)))
    check("a line with no timing is not judged by the per-line limit (the group check and the NO TIMING flag cover it)",
          line_faults([{"name": "g", "tier": "lock", "id": "L1", "lines": [("new", "")]}], T({}), True) == ([], []))
    # Main (the timings job): an unchanged line over the limit warns and the pack commits, listing it (LINE-LIMIT-SCOPE).
    packed = []
    sink4 = (lambda t: wrote.append("timings"), lambda g, t: (wrote.append("pack"), packed.append(pack_record(g, t))))
    f170 = dict(t["lines"], a=170)
    ex4 = {}
    for n in range(1, 5):
        ex4 = add_run(ex4, rn(n, 20, f170))
    tm4, gs4, fl4 = settle(ex4, rn(5, 20, f170), hs, {})
    wrote.clear()
    rc4 = commit(tm4, gs4, fl4, sink4, calm=calm_faults(ex4, tm4, gs4, fl4), prev_setup=ex4["setup"])
    check("main: an unchanged 170 s line refuses nothing; exit %d, the pack commits and lists it: %s"
          % (rc4, packed[-1]["split-candidates"] if packed else None),
          not fl4 and rc4 == 0 and wrote == ["timings", "pack"]
          and packed[-1]["split-candidates"] == [{"label": "a", "median": 170, "setup": 20, "percent": 70}])
    # Main run 39559284220's shape: the setup median rose (32 -> 57 s) and put an unchanged 158 s line at 215 s, over the
    # 189 s line limit but under the 216 s group limit. PER-LINE-LIMIT refused that pack; now it commits and warns.
    f158 = dict(t["lines"], a=158)
    ex5 = {}
    for n, st in enumerate([32, 32, 57, 57], 1):
        ex5 = add_run(ex5, rn(n, st, f158))
    tm5, gs5, fl5 = settle(ex5, rn(5, 57, f158), hs, {})
    wrote.clear()
    rc5 = commit(tm5, gs5, fl5, sink4, calm=calm_faults(ex5, tm5, gs5, fl5), prev_setup=ex5["setup"])
    check("run 39559284220's shape (setup median %d s, line 158 s): exit %d, the pack commits, the line listed"
          % (tm5["setup"], rc5), tm5["setup"] == 57 and rc5 == 0 and wrote == ["timings", "pack"]
          and [c["label"] for c in packed[-1]["split-candidates"]] == ["a"])
    check("pack() reads only the tiers: a pack with split-candidates repacks to the same groups",
          pack(L("a", "b", "c", "d", "e"), T(f170), packed[0])
          == pack(L("a", "b", "c", "d", "e"), T(f170), {k: v for k, v in packed[0].items() if k in TIERS}))
    # Which lines a --check selects (LINE-LIMIT-SCOPE): none outside a pull request; strictly all when the base is unreadable;
    # in a pull request, ci-deps.py's own selection on the files changed since the event's base.
    sel, how = pr_selection({"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push"})
    check("selection on main (a push run): none (%s)" % how, sel == ())
    sel, how = pr_selection({"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request",
                             "GITHUB_EVENT_PATH": os.path.join(ROOT, "no-such-event.json")})
    check("selection on a PR whose event cannot be read: every line (%s)" % how, sel is True)
    class Deps:                                   # a stand-in for ci-deps.py: records the base it is given
        def __init__(self, changed, result):
            self.changed, self.result, self.base = changed, result, None

        def changed_since(self, base):
            self.base = base
            return self.changed

        def select(self, changed):
            return self.result
    with tempfile.TemporaryDirectory() as td:
        ev = os.path.join(td, "event.json")
        with open(ev, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"pull_request": {"base": {"sha": "0123456789abcdef"}}}, f)
        env = {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request", "GITHUB_EVENT_PATH": ev}
        d1 = Deps(["games/x/index.html"], (False, [], {"scripts/verify-x.py": ["games/x/index.html"]}))
        sel1, how1 = pr_selection(env, d1)
        d2 = Deps([".github/workflows/check-site.yml"], (True, ["CI itself"], {}))
        sel2, how2 = pr_selection(env, d2)
    check("selection on a PR: ci-deps.py's select() on the files changed since the event's base (%s)" % how1,
          d1.base == "0123456789abcdef" and sel1 == X)
    check("selection on a PR that changes CI: every line (%s)" % how2, sel2 is True)
    # REGION-HISTORY: the per-region record keeps 10 per line per region and leaves ci-timings.json alone.
    regs = ["eastus", "centralus", "westus"]

    def rr(n):
        # run n: line "a" ran in region n % 3; line "b" ran in region (n // 2) % 3; line "c" has no region
        return dict(rn(n, 22, {"a": 10 + n, "b": 100 + n, "c": 50}), regions={"a": regs[n % 3], "b": regs[(n // 2) % 3]})
    plain, with_step, reg = {}, {}, {}
    for n in range(1, 13):
        plain = add_run(plain, rr(n))
        with_step = add_run(with_step, rr(n))
        reg = add_regions(reg, rr(n))
    check("12 runs across 3 regions: ci-timings.json is byte-identical with and without the region step",
          json.dumps(plain, indent=1) == json.dumps(with_step, indent=1) and len(plain["history"]) == HISTORY)
    check("a line keeps at most %d times per region, none lost below that" % REGION_KEEP,
          all(len(v) <= REGION_KEEP for d in reg["lines"].values() for v in d.values())
          and sum(len(v) for v in reg["lines"]["a"].values()) == 12)
    check("a region with more than %d runs rolls the oldest off (line a, eastus: runs 3,6,9,12 only)" % REGION_KEEP,
          reg["lines"]["a"]["eastus"] == [13, 16, 19, 22])
    big = {}
    for n in range(1, 31):
        big = add_regions(big, dict(rn(n, 22, {"a": n}), regions={"a": "eastus"}))
    check("30 runs in one region keep the newest %d, oldest first" % REGION_KEEP,
          big["lines"]["a"]["eastus"] == list(range(21, 31)))
    check("a line with no region is kept under 'unknown'", reg["lines"]["c"] == {"unknown": [50] * REGION_KEEP})
    check("the same run twice is counted once", add_regions(reg, rr(12)) == reg)
    check("the file text is small and parses back to the same data",
          json.loads(dump_regions(reg)) == reg and len(dump_regions(reg)) < 2000)
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
    ap.add_argument("--record-and-pack", metavar="RUN_ID", help="record, repack, check; write only if it passes")
    ap.add_argument("--record-regions", metavar="RUN_ID", help="add the run to ci-timings-regions.json (needs --from-dir)")
    ap.add_argument("--from-dir", metavar="DIR", help="with --record-timings or --record-and-pack: the run's ci-timing-* artifacts")
    ap.add_argument("--write-pack", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.record_regions:
        return record_regions(a.record_regions, a.from_dir)
    if a.record_and_pack:
        return record_and_pack(a.record_and_pack, a.from_dir)
    if a.record_timings:
        return record_timings(a.record_timings, a.from_dir)
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
        # The selection costs ci-deps.py's dependency map (about a minute in CI), and it matters only for a split
        # candidate: with none, nothing is computed.
        selected, how = pr_selection() if split_candidates(gs, timings) else ((), "no line is over the per-line limit")
        print("selection: " + how)
        faults = budget_faults(gs, timings, selected)
        warn(line_faults(gs, timings, selected)[1])
        for x in faults:
            print("FAIL  " + x)
        print("check: %s (pack to %d%% of each budget; a line past %d%% fails only where it is selected; a group fails "
              "past %d%%; timings from main run %s)"
              % ("FAILED" if faults else "PASS", TARGET * 100, TARGET * 100, FAIL * 100, timings.get("run")))
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
        with open(a.github_output, "a", encoding="utf-8", newline='') as f:
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
