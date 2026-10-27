#!/usr/bin/env python3
"""The "Content verifiers" groups, built from each script's own header (contract V, 7 Oct 2026; canon §7.8.2).

    python scripts/ci-groups.py                       # every content group and its lines
    python scripts/ci-groups.py --json                # the matrix, as the workflow's content job reads it
    python scripts/ci-groups.py --github-output FILE  # plan job: writes groups=<that JSON>
    python scripts/ci-groups.py --compare FILE        # equal, line for line, to FILE's static content groups?
    python scripts/ci-groups.py --check               # the budget check: fails past 80% (contract CI-BALANCE)
    python scripts/ci-groups.py --check-measured --run-id ID --from-dir D  # the same check on this PR run's own times
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
warning naming it. A change whose selection is everything (CI itself, or an unknown path) selects no line for a reason
of its own, so it warns too (Jon's ruling, 21 Oct 2026). The group rule (past 80%) still
refuses the pack and fails --check everywhere, and the setup-only warning (exit 2) is unchanged.

A PR IS ALSO JUDGED ON ITS OWN MEASURED TIMES (contract PR-MEASURED, Jon's ruling 25 Oct 2026; canon §7.8.1). --check runs
in the plan job, before any verifier has run, so it knows only main's medians: a line with none (new, or renamed) counts as
its tier's default, 120 s, and a line a PR grew is judged on main's old figure. Three times a verifier passed its PR and
turned main red after merge: Squared Squirrel (#515), Burst mode (BURST-STAGE #525 grew check-burst.py; the median caught
up on #527, a record-only PR) and Shape Shifter (#526's renamed line, estimated at 120 s, took 205 s). The PR run measures
every line it runs and saves the ci-timing-* artifacts the main timings job reads; the "PR budget (measured times)" job
reads them on every run, after the content groups, and runs --check-measured, and the Gate needs it. The check lays this
run's times over the committed timings (measured_timings()): a line the change selects (pr_selection(), as --check) takes
the larger of main's median and this run's time; a line with no median takes this run's time; every other line keeps its
median, so runner noise on an unchanged line moves nothing, and a time below the median never lowers it. The setup stays
the committed median, never this run's. It then repacks from ci-pack.json and applies budget_faults() and line_faults()
with the same selection: the same 70% and 80% rules, no second copy. A fault names the line, its main median (or
"none"), this run's time and its group. A run that is not a pull request, or one with no content or lock timing file
(no verifier ran), prints why and passes.

ON MAIN A GROUP OVER BUDGET IS A RECORDED WARNING (contract MAIN-WARN, Jon's ruling 25 Oct 2026; canon §7.8.1), reversing
CI-TIMINGS-MEDIAN's fail-on-main for groups between FAIL (80%) and HARD (100%). The estimate moves with runner speed, which
differs by about 25% between regions: #526's Shape Shifter, unchanged code, took 163 s on its PR run and 205 s on main
(Content verifiers 34 at 82%), the timings job refused the pack, main went red and merge-pr.py refused every merge, while
the job's real limit, its 6-minute timeout, was far off. Now the timings job (--record-and-pack, main_pack()) writes the
timings and the pack whatever group passes 80%, lists each such group in ci-pack.json under "over-budget" (group,
estimate, percent, its largest lines and their scripts), prints a ::warning:: naming them, and exits 0. A group past
HARD (100% of its budget, 75% of its timeout, close to the hang guard) still refuses the pack and fails, as before. On a
PR (--check, --check-measured) a group past 80% is a fault only where the change selects a script with a line in it
(group_faults(), as line_faults() scopes a single line; the base unreadable selects everything); otherwise, and on a
run-all change, a warning naming it. Past 100% is a fault everywhere. SETUP_ONLY (exit 2) is unchanged.

A LONG VERIFIER'S PARTS ARE CHOSEN HERE, FROM ITS UNITS' TIMES (contract SHARD, Jon 27 Oct 2026; canon §7.8.1). The packer
moves lines and never splits one, and until SHARD each long verifier split its own work by hand, so a part that outgrew the
per-line limit turned the first PR that ran it red: Shape Shifter on 26 Oct (a part grew), Just Pythag It, Bruv on 27 Oct
(the setup median went from about 20 s to 46 s; the per-job font fetch, since removed). Now such a verifier declares

    # ci-shards: [<tier> |] <label> | <args> | <parts until timed>

lists its work as named units through scripts/ci_shards.py (bank_common re-exports it), and runs the slice --shard i/k
gives it. expand() turns the header into k lines, "<label>, part i of k", each "python scripts/<it>.py <args> --shard i/k".
k is chosen by choose_parts() from the verifier's unit medians (ci-timings.json "units", recorded from the "unit ..."
lines ci_shards writes to the group's timing file) and its per-part overhead (the part's time less its units'; "overhead"):
the fewest parts whose every estimate (overhead plus its units, dealt by ci_shards.deal) plus the median setup is at most
SHARD_TARGET (75%) of the per-line limit. Until a main run has timed its units, k is the header's number. The pack keeps k
(ci-pack.json "shards"), and a repack keeps the previous k while it still meets the target and is at most one more than
needed, so the job names do not churn; a part that grows past the target is re-divided on the next repack, not warned
about. A part line is estimated from its units (its own label's median is not used once units are timed), so a unit too
long to share a part shows as a split candidate naming that unit. The deal is a partition by construction (ci_shards'
self-test), so no verifier checks its own parts any more.

Old headers ("# ci-line: B4 | ..."): a hand-made group id is still accepted and read as its tier only (L* is
the lock tier, any other is content), so a branch made before CI-BALANCE still passes; the repo's own headers
use the new form. Lines run in the order: scripts by file name, then each script's headers in file order. The
site-wide jobs (tiers 1-2, site-wide checks, tier 4, shared assets) stay listed in the workflow.

Stdlib only.
"""
import argparse, json, os, re, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)
import ci_shards  # noqa: E402  (stdlib only: how a verifier's units are dealt into parts, shared with the verifiers)
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "check-site.yml")
PREFIX = "Content verifiers"
TIMINGS = "scripts/ci-timings.json"     # each content line's seconds on a main full run (--record-timings)

REGIONS = "scripts/ci-timings-regions.json"   # per line, per runner region, the last REGION_KEEP times (--record-regions)

PACK = "scripts/ci-pack.json"           # each line's group (--write-pack, after each main full run)
WARN_LIST = "scripts/ci-warn-list.json"   # the per-line limit's shrink-only warn list (GATE-WARN-THEN-ENFORCE)
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
HARD = 1.00                        # of a group's budget: past it a group fails everywhere, main included (MAIN-WARN)
SETUP = 25                         # seconds before a group's first line, when the timings do not record it
HISTORY = 5                        # main runs kept in ci-timings.json; the estimates are their medians
REGION_KEEP = 10                   # times kept per line per region in ci-timings-regions.json (REGION-HISTORY, 15 Oct 2026)
REGION_RUNS = 20                   # run ids remembered there, so the same run recorded twice is counted once
SHARD_TARGET = 0.75                # of the per-line limit (TARGET of the budget): a sharded verifier's parts fit it (SHARD)
OVERHEAD = 10                      # seconds a part spends outside its units (start-up), until a run has recorded it
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
SHARDS = re.compile(r"^# ci-shards:(.*)$", re.M)
PART_LABEL = "%s, part %d of %d"
HAND_PART = re.compile(r"(?:^|\s)--part(?:[\s=]|$)")       # a hand split's flag (before SHARD); --part-selftest is not one


def command(script, args):
    """The shell command for a header's <args>: each '&&' part is one run of the script."""
    runs = []
    for part in args.split("&&"):
        part = part.strip()
        runs.append(("python scripts/%s %s" % (script, part)).rstrip())
    return " && ".join(runs)


def parse(name, text):
    """{'lines': [(tier field, label, cmd)], 'shards': [(tier field, label, args, parts until timed)], 'deps': [paths],
    'held': reason or None, 'errors': [str]}. The tier field is '' for a line with no tier (content), else what the header
    wrote (a tier, or an old id)."""
    out = {"lines": [], "shards": [], "deps": [], "held": None, "errors": []}
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
        if HAND_PART.search(args):
            # Two verifiers added on 27 Oct 2026, after SHARD's migration began, still split by hand: refused here so the
            # bug class (a hand-made part outgrowing the per-line limit) cannot come back through a new verifier.
            out["errors"].append("%s: a ci-line splits its script by hand (--part): declare its work units instead "
                                 "(# ci-shards, scripts/ci_shards.py), and ci-groups.py chooses the parts: %r"
                                 % (name, m.group(0)))
            continue
        out["lines"].append((group, label, command(name, args)))
    for m in SHARDS.finditer(text):
        parts = [p.strip() for p in m.group(1).split("|")]
        if len(parts) == 3:
            parts = [""] + parts
        if len(parts) != 4 or not parts[1] or not re.match(r"^[1-9]\d*$", parts[3]):
            out["errors"].append("%s: a ci-shards header is '[<tier> |] <label> | <args> | <parts until timed>': %r"
                                 % (name, m.group(0)))
            continue
        if "&&" in parts[2] or "--shard" in parts[2]:
            out["errors"].append("%s: a ci-shards header's <args> are one run of the script, without '&&' or --shard "
                                 "(each part adds --shard i/k): %r" % (name, m.group(0)))
            continue
        out["shards"].append((parts[0], parts[1], parts[2], int(parts[3])))
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
        if info["lines"] or info["shards"] or info["deps"] or info["held"] or info["errors"]:
            out[name] = info
    return out


def read_json(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def unit_medians(script, timings):
    """{unit id: median seconds} for a sharded verifier, from the timings' "units" (empty until a main run times them)."""
    return timings.get("units", {}).get(script, {})


def part_estimates(script, k, timings):
    """[seconds] for each of a sharded verifier's k parts: its per-part overhead plus the units ci_shards.deal() gives it.
    Only the units the timings know are counted (a new unit is counted once a main run times it; --check-measured counts
    it from the pull request's own run)."""
    times = unit_medians(script, timings)
    over = timings.get("overhead", {}).get(script, OVERHEAD)
    return [over + sum(times[u] for u in p) for p in ci_shards.deal(sorted(times), k, times)]


def shard_cap(tier, timings):
    """The most a part may take, setup excluded: SHARD_TARGET of the per-line limit (TARGET of the budget), less the
    median setup."""
    return SHARD_TARGET * TARGET * budget(tier) - timings.get("setup", SETUP)


def choose_parts(script, tier, start, timings, prev_k=None):
    """(k, how): how many parts a sharded verifier runs in. Until a main run has timed its units, the header's number.
    Then the fewest parts whose every estimate fits shard_cap(); if no number does (one unit is too long to share a
    part), one part per unit, and the line check names the unit. The previous k (the pack's) is kept while it fits and
    is at most one more than needed, so a time hovering at a boundary does not rename the lines on every repack."""
    times = unit_medians(script, timings)
    if not times:
        return start, "not yet timed: the header's %d" % start
    cap = shard_cap(tier, timings)
    fits = lambda k: max(part_estimates(script, k, timings)) <= cap
    need = next((k for k in range(1, len(times) + 1) if fits(k)), len(times))
    if prev_k and need <= prev_k <= min(need + 1, len(times)) and fits(prev_k):
        return prev_k, "kept from the pack (%d needed)" % need
    return need, "chosen from %d timed unit(s)" % len(times)


def expand(hdrs=None, timings=None, prev=None):
    """(lines, est, timed, shards) for every declared line, in run order (scripts by file name, then each script's
    ci-lines, then its parts); unknown tiers are left out (errors() reports them).
    lines: [(tier, label, cmd)]; a ci-shards header gives k lines PART_LABEL % (label, i, k), each adding --shard i/k.
    est: {label: seconds}: a ci-line's median (else its tier's default); a part's estimate from its units once they are
    timed, else its own label's median, else the default. timed: the labels whose figure is a timing, not a default.
    shards: {script: {"parts", "how", "tier", "label"}} for the pack."""
    hdrs = headers() if hdrs is None else hdrs
    timings = read_json(TIMINGS) if timings is None else timings
    prev = read_json(PACK) if prev is None else prev
    secs = timings.get("lines", {})
    lines, est, timed, shards = [], {}, set(), {}
    for name in sorted(hdrs):
        for field, label, cmd in hdrs[name]["lines"]:
            t = tier_of(field)
            if t:
                lines.append((t, label, cmd))
                est[label] = secs.get(label, TIERS[t][3])
                if label in secs:
                    timed.add(label)
        for field, label, args, start in hdrs[name].get("shards", []):
            t = tier_of(field)
            if not t:
                continue
            prev_k = (prev.get("shards", {}).get(name) or {}).get("parts")
            k, how = choose_parts(name, t, start, timings, prev_k)
            shards[name] = {"parts": k, "how": how, "tier": t, "label": label}
            pe = part_estimates(name, k, timings) if unit_medians(name, timings) else None
            for i in range(1, k + 1):
                l = PART_LABEL % (label, i, k)
                lines.append((t, l, command(name, ("%s --shard %d/%d" % (args, i, k)).strip())))
                if pe is not None:
                    est[l] = int(round(pe[i - 1]))
                    timed.add(l)
                else:
                    est[l] = secs.get(l, TIERS[t][3])
                    if l in secs:
                        timed.add(l)
    return lines, est, timed, shards


def all_lines(hdrs=None, timings=None, prev=None):
    """[(tier, label, cmd)] in run order (expand())."""
    return expand(hdrs, timings, prev)[0]


def gid_key(gid):
    m = re.match(r"^([A-Z]*)(\d+)$", gid)
    return (m.group(1), int(m.group(2))) if m else (gid, 0)


def pack(lines=None, timings=None, prev=None, est=None):
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
        est_t = {l: est[l] if est is not None and l in est else secs.get(l, default) for l in mine}
        target = TARGET * budget(tier)
        old = prev.get(tier, {})
        groups, loose = {}, []
        for l in mine:
            g = old.get(l)
            if g and re.match(r"^%s\d+$" % pre, g):
                groups.setdefault(g, []).append(l)
            else:
                loose.append(l)
        total = lambda g: setup + sum(est_t[x] for x in groups[g])
        for g in sorted(groups, key=gid_key):
            while len(groups[g]) > 1 and total(g) > target:
                over = total(g) - target
                enough = [x for x in groups[g] if est_t[x] >= over]
                x = (min(enough, key=lambda x: (est_t[x], x)) if enough
                     else max(groups[g], key=lambda x: (est_t[x], x)))
                groups[g].remove(x)
                loose.append(x)
        for x in sorted(loose, key=lambda x: (-est_t[x], x)):
            fit = [g for g in groups if total(g) + est_t[x] <= target]
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
    """[{'id', 'tier', 'name', 'timeout', 'lines': [(label, cmd)], 'secs', 'timed', 'shards'}] by tier, then id; lines in
    run order. 'secs' is each line's estimate and 'timed' the lines whose estimate is a timing (expand()); 'shards' is
    expand()'s choice of parts, the same on every group, for the pack."""
    timings = read_json(TIMINGS) if timings is None else timings
    prev = read_json(PACK) if prev is None else prev
    lines, est, timed, shards = expand(hdrs, timings, prev)
    order = {l: i for i, (_, l, _) in enumerate(lines)}
    cmd = {l: c for _, l, c in lines}
    out = []
    for tier, gs in pack(lines, timings, prev, est).items():
        prefix, _, timeout, _ = TIERS[tier]
        for g, labels in gs.items():
            mine = sorted(labels, key=order.get)
            out.append({"id": g, "tier": tier, "name": "%s %s" % (prefix, g), "timeout": timeout,
                        "job_timeout": timeout + PULL_ALLOWANCE,
                        "lines": [(l, cmd[l]) for l in mine], "secs": {l: est[l] for l in mine},
                        "timed": sorted(l for l in mine if l in timed), "shards": shards})
    return out


def line_secs(g, timings):
    """{label: (seconds, timed)} for a group's lines: groups()' estimates, or, for a group built without them (a
    self-test's hand-made group), each line's median, else its tier's default."""
    if "secs" in g:
        return {l: (g["secs"][l], l in g["timed"]) for l, _ in g["lines"]}
    secs, default = timings.get("lines", {}), TIERS[g["tier"]][3]
    return {l: (secs.get(l, default), l in secs) for l, _ in g["lines"]}


def estimate(g, timings=None):
    """(estimated seconds, [labels with no timing]) for a group: setup plus its lines (no timing: the default)."""
    timings = read_json(TIMINGS) if timings is None else timings
    ls = line_secs(g, timings)
    return (timings.get("setup", SETUP) + sum(t for t, _ in ls.values()), [l for l, _ in g["lines"] if not ls[l][1]])


def script_of(cmd):
    """The verifier a line runs ('scripts/<name>.py', as ci-deps.py names it), or None."""
    m = re.search(r"scripts/[\w.-]+\.py", cmd)
    return m.group(0) if m else None


def split_candidates(gs=None, timings=None):
    """[{label, median, setup, percent, group, script, budget}]: every timed line whose median plus the median setup passes
    TARGET of its group's budget (PER-LINE-LIMIT, 20 Oct 2026; LINE-LIMIT-SCOPE, 21 Oct 2026). The packer can move a line
    between groups but cannot split it, so a line this size is one slow setup from failing a group that nothing can
    repack: split its script. A line with no timing counts as its tier's default and is not judged here (the group check
    and the NO TIMING flag cover it). By label, so the pack's list is stable.
    A sharded verifier's part (SHARD) is judged on its estimate from its units: choose_parts() has already divided the
    verifier as far as its units allow, so a part still over the limit holds a unit too long to share a part, and the
    candidate names that unit ("unit": {"id", "seconds"}): divide the unit, in the verifier."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    setup = timings.get("setup", SETUP)
    out = []
    for g in gs:
        b = budget(g["tier"])
        ls = line_secs(g, timings)
        for l, c in g["lines"]:
            sec, timed = ls[l]
            if timed and sec + setup > TARGET * b:
                cand = {"label": l, "median": sec, "setup": setup, "percent": int(100 * (sec + setup) / b),
                        "group": g["name"], "script": script_of(c), "budget": b,
                        "measured": timings.get("measured", {}).get(l)}
                units = unit_medians(os.path.basename(cand["script"] or ""), timings) if "--shard " in c else {}
                if units:
                    big = max(sorted(units), key=lambda u: units[u])
                    cand["unit"] = {"id": big, "seconds": units[big]}
                out.append(cand)
    return sorted(out, key=lambda c: c["label"])


def source(m):
    """How a line's figure was reached, for a message: "(median)", or with --check-measured the figures behind it."""
    if not m:
        return "(median)"
    return "(main median %s, this run %ss)" % ("none" if m["median"] is None else "%ss" % m["median"], m["run"])


def line_message(c):
    if c.get("unit"):
        how = ("Its verifier is already divided as far as its units allow: its longest unit, %r, takes %ss; divide that "
               "unit in the verifier (scripts/ci_shards.py)." % (c["unit"]["id"], c["unit"]["seconds"]))
    else:
        how = "Divide its script into work units (# ci-shards, scripts/ci_shards.py)."
    return ("%s: line over the per-line limit: %s %ss %s + %ss setup = %ds, %d%% of its %ds budget; "
            "the limit is %d%% (%ds). %s"
            % (c["group"], c["label"], c["median"], source(c.get("measured")), c["setup"], c["median"] + c["setup"],
               c["percent"], c["budget"], TARGET * 100, TARGET * c["budget"], how))


def base_label(label):
    """A line's label as the warn list names it: a sharded verifier's part ("X, part 2 of 3") is its verifier's label."""
    m = re.match(r"^(.*), part \d+ of \d+$", label)
    return m.group(1) if m else label


def read_warn_list(path=None):
    """The warn list's labels (base_label()s), in file order; [] when there is no list."""
    try:
        with open(os.path.join(ROOT, path or WARN_LIST), encoding="utf-8") as f:
            return list(json.load(f).get("per-line", []))
    except (OSError, ValueError):
        return []


def unrecorded(gs):
    """{label}: the lines whose figure is an estimate, not a main run's time (a new or renamed line, or a sharded part
    whose units no main run has timed): groups()' 'timed' marks the rest."""
    return {l for g in gs for l, _ in g["lines"] if l not in set(g.get("timed", ()))} if gs and "timed" in gs[0] else set()


def line_faults(gs=None, timings=None, selected=(), listed=None, fresh=None):
    """(faults, warnings) for the split candidates (LINE-LIMIT-SCOPE). `selected` is the set of scripts the change being
    checked selects (ci-deps.py's names), True to judge every line strictly, or () for none (main, the timings job): a
    candidate whose script is selected is a fault, any other a warning, so runner noise on an unchanged line never fails
    main or a PR that does not touch it.
    WARN-THEN-ENFORCE (Jon, 27 Oct 2026): a candidate on the warn list (`listed`, base labels; default the committed
    scripts/ci-warn-list.json) is a warning wherever it is selected, and a line with no time recorded by a main run
    (`fresh`, labels; default every line whose figure is an estimate) is estimated and warned, never failed: the limit
    applies once a main run has recorded it."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    listed = set(read_warn_list() if listed is None else listed)
    fresh = unrecorded(gs) if fresh is None else set(fresh)
    faults, warns = [], []
    for c in split_candidates(gs, timings):
        if base_label(c["label"]) in listed:
            warns.append("on the warn list (%s, shrink-only: a warning, not a failure, until the line is divided): %s"
                         % (WARN_LIST, line_message(c)))
        elif c["label"] in fresh:
            warns.append("no time recorded by a main run (a warning, never a failure, until its first main run records "
                         "it): %s" % line_message(c))
        elif selected is True or c["script"] in selected:
            faults.append(line_message(c) + " This change selects its verifier (%s)." % c["script"])
        else:
            warns.append("split candidate (a warning, not a failure: nothing checked here selects %s): %s"
                         % (c["script"], line_message(c)))
    for g in gs:
        ls = line_secs(g, timings)
        for l, c in g["lines"]:
            if l in fresh and not ls[l][1]:
                warns.append("no time recorded by a main run: %s (%s) is estimated at %ds, the tier's default; the "
                             "per-line and group limits apply once its first main run records it"
                             % (l, script_of(c) or "?", ls[l][0]))
    return faults, warns


def over_budget(gs=None, timings=None):
    """[{group, estimate, percent, budget, message, scripts, lines}]: every group whose estimate passes FAIL of its budget,
    by group name. `lines` are its three largest ({label, seconds, script}); `scripts` every verifier with a line in it;
    `message` names the group, its estimate and its largest lines."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    meas = timings.get("measured", {})
    out = []
    for g in gs:
        est, _ = estimate(g, timings)
        b = budget(g["tier"])
        if est > FAIL * b:
            default = TIERS[g["tier"]][3]
            ls = line_secs(g, timings)
            big = sorted(g["lines"], key=lambda lc: -ls[lc[0]][0])[:3]
            msg = ("%s: estimated %ds, past %d%% of its %ds budget (%d%%). Largest: %s. A line this long "
                   "cannot share a job: divide its script into work units (# ci-shards, scripts/ci_shards.py)."
                   % (g["name"], est, FAIL * 100, b, 100 * est / b,
                      "; ".join("%s %ss%s" % (l, ls[l][0] if ls[l][1] else "no timing, counted as %d" % default,
                                              " " + source(meas[l]) if l in meas else "")
                                for l, _ in big)))
            out.append({"group": g["name"], "estimate": est, "percent": int(100 * est / b), "budget": b, "message": msg,
                        "scripts": sorted({script_of(c) for _, c in g["lines"]} - {None}),
                        "lines": [{"label": l, "seconds": ls[l][0], "script": script_of(c)} for l, c in big]})
    return sorted(out, key=lambda o: o["group"])


def group_faults(gs=None, timings=None, selected=(), listed=None, fresh=None):
    """(faults, warnings) for the groups past FAIL (MAIN-WARN, Jon's ruling 25 Oct 2026, scoping the group rule as
    LINE-LIMIT-SCOPE scoped the line rule). A group past HARD (100%) of its budget is a fault everywhere, main included.
    Between FAIL and HARD it is a fault only where the change selects a script with a line in it (`selected` True, the
    base unreadable, counts as every script); otherwise, on main and on a run-all change, a warning naming it.
    WARN-THEN-ENFORCE (Jon, 27 Oct 2026): an estimate never makes a group a fault. Past HARD, the group is a fault only if
    its timed lines alone pass HARD: a main run's median, or this pull request's own measured time (--check-measured),
    since a measured time past HARD would refuse main's pack and turn main red after the merge (#526's shape); a line
    with no time at all (the tier's default) is left out. Between FAIL and HARD, the lines no main run has timed
    (`fresh`) and the lines on the warn list (`listed`) are left out: the group is a fault only if its other lines pass
    FAIL."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    listed = set(read_warn_list() if listed is None else listed)
    fresh = unrecorded(gs) if fresh is None else set(fresh)
    by_name = {g["name"]: g for g in gs}
    setup = timings.get("setup", SETUP)
    faults, warns = [], []
    for o in over_budget(gs, timings):
        ls = line_secs(by_name[o["group"]], timings)
        recorded = setup + sum(t for l, (t, timed) in ls.items() if timed)
        firm = setup + sum(t for l, (t, timed) in ls.items() if timed and l not in fresh and base_label(l) not in listed)
        if o["estimate"] > HARD * o["budget"]:
            if recorded > HARD * o["budget"]:
                faults.append(o["message"] + " It is past %d%% of its budget: a fault everywhere, main included." % (HARD * 100))
            else:
                warns.append("over budget (a warning, never a failure: only lines with no time yet put it past %d%%; "
                             "its timed lines come to %ds): %s" % (HARD * 100, recorded, o["message"]))
        elif selected is True or set(o["scripts"]) & set(selected):
            hit = o["scripts"] if selected is True else sorted(set(o["scripts"]) & set(selected))
            if firm > FAIL * o["budget"]:
                faults.append(o["message"] + " This change selects its verifier%s (%s)." % ("s" if len(hit) > 1 else "", ", ".join(hit)))
            else:
                warns.append("over budget (a warning, not a failure: without its warn-listed lines and the lines no main "
                             "run has timed it comes to %ds, inside %d%%): %s" % (firm, FAIL * 100, o["message"]))
        else:
            warns.append("over budget (a warning, not a failure: nothing checked here selects %s): %s"
                         % (", ".join(o["scripts"]), o["message"]))
    return faults, warns


def budget_faults(gs=None, timings=None, selected=(), listed=None, fresh=None):
    """[fault]: every split candidate the change selects (line_faults), and every group past FAIL that it selects or
    that is past HARD (group_faults). With nothing selected (main) only a group past HARD is a fault: it is what refuses
    a pack on main. `listed` and `fresh` as line_faults()."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    return (line_faults(gs, timings, selected, listed, fresh)[0]
            + group_faults(gs, timings, selected, listed, fresh)[0])


def stale_entries(gs=None, timings=None, listed=None):
    """[(label, why)]: warn-list entries that no longer hold a line over the per-line limit: no line has that label, or
    every line of it has a recorded time and none is a split candidate. An entry whose line has no recorded time yet is
    kept: it cannot be judged until a main run times it."""
    timings = read_json(TIMINGS) if timings is None else timings
    gs = groups(timings=timings) if gs is None else gs
    listed = read_warn_list() if listed is None else listed
    fresh = unrecorded(gs)
    over = {base_label(c["label"]) for c in split_candidates(gs, timings)}
    out = []
    for b in listed:
        mine = [l for g in gs for l, _ in g["lines"] if base_label(l) == b]
        if not mine:
            out.append((b, "no line has this label now"))
        elif b not in over and not any(l in fresh for l in mine):
            out.append((b, "every line of it is inside the per-line limit now"))
    return out


def write_warn_list(gs, timings, listed=None, path=None):
    """The timings job's pruning (shrink-only): rewrite the warn list without its stale entries. Returns the entries
    removed. Never adds one."""
    listed = read_warn_list(path) if listed is None else listed
    gone = {b for b, _ in stale_entries(gs, timings, listed)}
    if gone:
        full = os.path.join(ROOT, path or WARN_LIST)
        with open(full, encoding="utf-8") as f:
            data = json.load(f)
        data["per-line"] = [b for b in data.get("per-line", []) if b not in gone]
        with open(full, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return sorted(gone)


def warn_list_faults(base_list, listed, gs=None, timings=None):
    """[fault] for a pull request that edits the warn list (`base_list`: the list at the PR's base; `listed`: this
    branch's). Shrink-only: an entry the base did not have is a fault; and a PR that edits the list leaves no stale
    entry in it (the known-failures pattern). A PR that does not edit the list is never judged here: main's timings job
    removes stale entries itself (write_warn_list()), so a list that falls behind the timings blocks no lane."""
    if base_list is None or list(base_list) == list(listed):
        return []
    out = ["%s gains %r: the warn list is shrink-only (an entry is never added; divide the line instead)" % (WARN_LIST, b)
           for b in listed if b not in base_list]
    out += ["%s keeps %r, which passes now (%s): remove it" % (WARN_LIST, b, why)
            for b, why in stale_entries(gs, timings, listed)]
    return out


def warn(msgs, title="split candidate"):
    """Print each warning; in a GitHub Actions run, also as a ::warning:: annotation, so a split candidate or a group
    over budget shows on the run."""
    for x in msgs:
        print("WARN  " + x)
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print("::warning title=%s::%s" % (title, x))


def pr_base(env=None):
    """(base sha, None) for the change being checked, or (None, (selected, how)): pr_selection()'s answer when there is
    no base to compare with (not a pull request: (); the base unreadable: True)."""
    env = os.environ if env is None else env
    import subprocess
    if env.get("GITHUB_ACTIONS") == "true":
        event = env.get("GITHUB_EVENT_NAME", "")
        if event != "pull_request":
            return None, ((), "a %s run, not a pull request: no line is selected" % (event or "non-PR"))
        try:
            with open(env["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
                return json.load(f)["pull_request"]["base"]["sha"], None
        except (KeyError, OSError, ValueError, TypeError):
            return None, (True, "the pull request's base could not be read from the event: every line counts as selected")
    r = subprocess.run(["git", "merge-base", "origin/main", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        return None, (True, "no merge base with origin/main: every line counts as selected")
    return r.stdout.strip(), None


def base_warn_list(env=None):
    """The warn list at the change's base (pr_base()), or None when there is no base, or the base has no list (the PR
    that brings the list in)."""
    import subprocess
    base, _ = pr_base(env)
    if base is None:
        return None
    r = subprocess.run(["git", "show", "%s:%s" % (base, WARN_LIST)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        return None
    try:
        return list(json.loads(r.stdout).get("per-line", []))
    except ValueError:
        return None


# The gate's own files (GATE-WARN-THEN-ENFORCE step 2, Jon 27 Oct 2026): a pull request that touches one also passes the
# worst-case test. The limits live in ci-groups.py (70%, 80%, 100%), check-context-size.py (20 KB) and merge-pr.py (the main
# rule); ci-deps.py is the selection; ci_shards.py divides the verifiers; the workflow runs them all.
GATE_PREFIXES = (".github/", "scripts/ci-", "scripts/ci_shards.py", "scripts/merge-pr.py", "scripts/check-context-size.py",
                 "scripts/check-changed.py", "requirements")
WORST_CASE = "scripts/bank_common.py"      # the shared import nearly every verifier loads: the widest selective change


def gate_paths(changed):
    """The changed paths that are the gate's own files."""
    return sorted(p for p in (c.replace("\\", "/").strip() for c in changed) if p.startswith(GATE_PREFIXES))


def importers(hdrs=None):
    """{'scripts/<name>.py'}: every script with a CI line that imports bank_common itself."""
    hdrs = headers() if hdrs is None else hdrs
    out = set()
    for name, h in hdrs.items():
        if not (h.get("lines") or h.get("shards")):
            continue
        try:
            text = open(os.path.join(SCRIPTS, name), encoding="utf-8").read()
        except OSError:
            continue
        if re.search(r"^\s*(import bank_common\b|from bank_common import)", text, re.M):
            out.add("scripts/" + name)
    return out


def worst_case(changed, deps, gs=None, timings=None, listed=None, need=None):
    """(applies, faults, how): the worst-case test (GATE-WARN-THEN-ENFORCE step 2). When `changed` touches a gate file, the
    budget check runs again on the selection a change to scripts/bank_common.py makes, as Plan would judge that pull request:
    every verifier that imports it (`need`, default importers()) must be selected, and the result must pass. A gate change
    that would fail every shared-asset PR (the per-line limit of 27 Oct, which blocked #583) fails its own PR instead."""
    gates = gate_paths(changed)
    if not gates:
        return False, [], "no gate file changed: the worst-case test does not apply"
    run_all, reasons, picked = deps.select([WORST_CASE])
    if run_all:
        return True, ["a change to %s selects every verifier for a reason of its own (%s): the worst case cannot be judged "
                      "on a real selection" % (WORST_CASE, "; ".join(reasons) or "run all")], "gate files: %s" % ", ".join(gates)
    sel = set(picked)
    need = importers() if need is None else set(need)
    faults = ["%s imports bank_common but a change to %s does not select it" % (s, WORST_CASE) for s in sorted(need - sel)]
    faults += budget_faults(gs, timings, sel, listed)
    return True, faults, "gate files: %s; a change to %s selects %d verifier(s)" % (", ".join(gates), WORST_CASE, len(sel))


def pr_selection(env=None, deps=None):
    """(selected, how) for --check: the scripts the change being checked selects, as CI's plan job selects them
    (scripts/ci-deps.py select() on the files changed since the base), or () for none. A change that selects every verifier
    (CI itself, or an unknown path) selects none for a reason of its own, so it is () too (Jon, 21 Oct 2026). True (every
    line) is only the strict answer when the base cannot be read.
    In a GitHub Actions run that is not a pull request (main, the schedule, a manual run): (). In a pull request run: the
    base is the event's pull_request.base.sha, the plan job's own BASE, read from GITHUB_EVENT_PATH, so the plan job's
    interface is unchanged. Locally: the merge base with origin/main. If the base cannot be read, every line counts as
    selected: a check that cannot tell fails strictly rather than passes. `deps` is ci-deps.py's module (loaded here when
    None; the self-test passes a stand-in, because its dependency map takes about a minute to build)."""
    import importlib.util
    base, how = pr_base(env)
    if base is None:
        return how
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
        return (), "this change selects every verifier (%s), none for a reason of its own: a line over the limit warns" % (reasons[0] if reasons else "run all")
    return set(picked), "this change (%d file(s) since %s) selects %d verifier(s)" % (len(changed), base[:10], len(picked))


def pack_record(gs, timings=None):
    """ci-pack.json's content: {tier: {label: group id}}, "split-candidates" (LINE-LIMIT-SCOPE): each line over the
    per-line limit, as {label, median, setup, percent}, and "over-budget" (MAIN-WARN): each group past FAIL, as {group,
    estimate, percent, lines: its largest, each {label, seconds, script}}, for the lane that splits them; and "shards"
    (SHARD): each sharded verifier's parts, {script: {parts, how, tier, label}}, which the next repack keeps while they
    still fit (choose_parts()). pack() reads only the tiers."""
    rec = {}
    for g in gs:
        rec.setdefault(g["tier"], {}).update({l: g["id"] for l, _ in g["lines"]})
    rec["shards"] = dict(sorted((gs[0].get("shards") or {}).items())) if gs else {}
    rec["split-candidates"] = [{k: c[k] for k in ("label", "median", "setup", "percent")}
                               for c in split_candidates(gs, timings)]
    rec["over-budget"] = [{k: o[k] for k in ("group", "estimate", "percent", "lines")} for o in over_budget(gs, timings)]
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
        for group, label, _, _ in info.get("shards", []):
            if tier_of(group) is None:
                errs.append("%s: ci-shards names %r, which is not a tier (%s; or leave it out for content)"
                            % (name, group, ", ".join(TIER_ORDER)))
        if len(info.get("shards", [])) > 1:
            errs.append("%s: declares %d ci-shards headers: one verifier, one list of units"
                        % (name, len(info["shards"])))
        if info["held"] and (info["lines"] or info.get("shards")):
            errs.append("%s: declares both ci-held and ci-line or ci-shards" % name)
    seen = {}
    for name, info in sorted(hdrs.items()):
        for label in [l for _, l, _ in info["lines"]] + [l for _, l, _, _ in info.get("shards", [])]:
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

    def parse_units(text):
        """(units, overhead) from one timing file (SHARD): ci_shards' "unit" lines, each belonging to the next line's
        "ok"/"FAILED" entry (a line's units are written while it runs). units {script: {unit id: seconds}}; overhead
        {script: seconds}, a part's time less its units', the largest of the run's parts."""
        units, over, pending = {}, {}, []
        for row in text.splitlines():
            u = ci_shards.UNIT_LINE.match(row)
            if u:
                pending.append((u.group(1), u.group(2), float(u.group(3))))
                continue
            m = re.search(r"(?:ok|FAILED)  (.+?)  \((\d+)s; group at", row)
            if m:
                spent = {}
                for script, uid, t in pending:
                    units.setdefault(script, {})[uid] = t
                    spent[script] = spent.get(script, 0) + t
                for script, t in spent.items():
                    over[script] = max(over.get(script, 0), max(0, int(round(int(m.group(2)) - t))))
                pending = []
        return units, over

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
    secs, setups, regions, units, over = {}, [], {}, {}, {}
    for text in texts:
        mine, setup = parse(text)
        secs.update(mine)
        u, o = parse_units(text)
        for script, d in u.items():
            units.setdefault(script, {}).update(d)
        for script, t in o.items():
            over[script] = max(over.get(script, 0), t)
        regions.update({label: region_of(text) for label, _ in mine})
        if setup is not None:
            setups.append(setup)
    rec = {"run": int(run_id), "date": run["created_at"][:10], "branch": run["head_branch"],
           "event": run["event"], "setup": max(setups) if setups else SETUP, "lines": dict(sorted(secs.items())),
           "regions": dict(sorted(regions.items()))}
    if units:
        rec["units"] = {s: dict(sorted(d.items())) for s, d in sorted(units.items())}
        rec["overhead"] = dict(sorted(over.items()))
    return rec


def median_int(xs):
    """The median of a non-empty list of numbers as a whole number; the middle pair of an even list rounds up."""
    xs = sorted(xs)
    n = len(xs)
    return int(xs[n // 2]) if n % 2 else int((xs[n // 2 - 1] + xs[n // 2] + 1) // 2)


def median_tenths(xs):
    """The median of a non-empty list of seconds, to a tenth (a unit's time: many take under a second)."""
    xs = sorted(xs)
    n = len(xs)
    return round(xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2, 1)


def medians(history):
    """The timings every reader sees, from a list of run records (oldest first): the newest run's id, date,
    branch and event; the median setup; and each line's median over the runs that timed it. With sharded verifiers
    (SHARD), also "units" ({script: {unit id: median}}, over the runs that timed each unit) and "overhead" ({script:
    median}); a history with no unit times has neither key."""
    last = history[-1]
    per, units, over = {}, {}, {}
    for r in history:
        for label, sec in r.get("lines", {}).items():
            per.setdefault(label, []).append(sec)
        for script, d in r.get("units", {}).items():
            for uid, sec in d.items():
                units.setdefault(script, {}).setdefault(uid, []).append(sec)
        for script, sec in r.get("overhead", {}).items():
            over.setdefault(script, []).append(sec)
    out = {"run": last["run"], "date": last["date"], "branch": last.get("branch", ""), "event": last.get("event", ""),
           "setup": median_int([r.get("setup", SETUP) for r in history]),
           "lines": {k: median_int(v) for k, v in sorted(per.items())}}
    if units:
        out["units"] = {s: {u: median_tenths(v) for u, v in sorted(d.items())} for s, d in sorted(units.items())}
        out["overhead"] = {s: median_int(v) for s, v in sorted(over.items())}
    return out


def add_run(existing, rec, keep=HISTORY):
    """The new ci-timings.json content: existing (the file's content) with the run record rec added to its history,
    the last `keep` runs kept, and the top-level fields the medians. A file from before the history (one run's
    figures at the top level) counts as one run of history; the same run twice is counted once."""
    hist = existing.get("history")
    if hist is None:
        hist = [{k: existing[k] for k in ("run", "date", "branch", "event", "setup", "lines", "units", "overhead")
                 if k in existing}] \
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
    current pack), and the faults that refuse that pack on main: a group past HARD only, since main selects nothing, a
    line over the per-line limit is a warning (LINE-LIMIT-SCOPE) and so is a group past FAIL (MAIN-WARN). Nothing is
    written."""
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
    wl = writers[2] if writers and len(writers) > 2 else (None if writers else write_warn_list)
    if wl is not None:
        for b in wl(gs, timings) or []:
            print("record-and-pack: %s: removed %r, which passes the per-line limit now (shrink-only)" % (WARN_LIST, b))
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


def main_pack(existing, rec, hdrs=None, prev=None, writers=None):
    """The timings job's work on one run record: add it, repack from the medians, and write the timings and the pack
    unless a group is past HARD (MAIN-WARN). A line over the per-line limit and a group past FAIL are printed as warnings
    and listed in the pack ("split-candidates", "over-budget"). Returns commit()'s exit status."""
    timings, gs, faults = settle(existing, rec, hdrs, prev)
    print("run %s: setup %ds (median %ds of %d run(s)); %d line(s) timed" % (
        rec["run"], rec["setup"], timings["setup"], len(timings["history"]), len(rec["lines"])))
    warn(line_faults(gs, timings)[1])
    warn(group_faults(gs, timings)[1], "over budget")
    return commit(timings, gs, faults, writers, calm=calm_faults(existing, timings, gs, faults),
                  prev_setup=existing.get("setup", SETUP))


def record_and_pack(run_id, from_dir=None):
    """The timings job: add the run, repack from the medians, and write the timings and the pack unless a group is past
    HARD of its budget (MAIN-WARN; before it, past FAIL). Warnings for lines over the limit and groups over budget."""
    rec = read_run(run_id, from_dir)
    if rec is None:
        return 1
    return main_pack(read_json(TIMINGS), rec)


def measured_timings(timings, rec, selected, hdrs=None):
    """The timings --check-measured judges (PR-MEASURED): `timings` (the committed medians) with the run record rec's times
    laid over. A line the change selects (`selected`: scripts, True for every line, () for none) takes the larger of its
    median and this run's time; a line with no median takes this run's time; every other line keeps its median. The
    setup is the committed median, never the run's. "measured" records {label: {"median", "run"}} for each line whose
    figure this run set or confirmed, for the messages. A sharded verifier's units and overhead (SHARD) are laid over the
    same way, by its script, so a pull request that grows a unit is judged on the parts the next repack would choose. Pure."""
    script = {l: script_of(c) for _, l, c in all_lines(hdrs, timings)}
    secs, meas = dict(timings.get("lines", {})), {}
    for label, t in rec.get("lines", {}).items():
        med = timings.get("lines", {}).get(label)
        if med is None:
            secs[label] = t
        elif selected is True or script.get(label) in selected:
            secs[label] = max(med, t)
        else:
            continue
        meas[label] = {"median": med, "run": t}
    out = dict(timings, lines=secs, measured=meas)
    units = {s: dict(d) for s, d in timings.get("units", {}).items()}
    over = dict(timings.get("overhead", {}))
    for s, d in rec.get("units", {}).items():
        sel = selected is True or "scripts/" + s in selected
        for uid, t in d.items():
            med = units.get(s, {}).get(uid)
            if med is None:
                units.setdefault(s, {})[uid] = t
            elif sel:
                units[s][uid] = max(med, t)
        if s in rec.get("overhead", {}):
            o, med = rec["overhead"][s], over.get(s)
            over[s] = o if med is None else max(med, o) if sel else med
    if units:
        out["units"], out["overhead"] = units, over
    return out


def check_measured(run_id, from_dir, env=None, rec=None, timings=None, hdrs=None, prev=None, deps=None):
    """--check-measured (PR-MEASURED): judge this pull request run's own measured times with --check's rules. Returns
    the exit status: 1 on a fault, 0 otherwise, and 0 with the reason printed when there is nothing to judge (not a pull
    request; no content or lock timing file). rec, timings, hdrs, prev and deps are for the self-test."""
    env = os.environ if env is None else env
    if env.get("GITHUB_ACTIONS") == "true" and env.get("GITHUB_EVENT_NAME") != "pull_request":
        print("check-measured: a %s run, not a pull request: nothing to judge here (main's timings job records its times)"
              % (env.get("GITHUB_EVENT_NAME") or "non-PR"))
        return 0
    rec = read_run(run_id, from_dir) if rec is None else rec
    if not rec or not rec.get("lines"):
        print("check-measured: no content or lock timing file in this run (no verifier ran, or none was saved): "
              "nothing to judge")
        return 0
    timings = read_json(TIMINGS) if timings is None else timings
    prev = read_json(PACK) if prev is None else prev
    meds = timings.get("lines", {})
    # The selection costs ci-deps.py's dependency map; it matters only when this run raised a median, or a line is over
    # the per-line limit.
    base = measured_timings(timings, rec, (), hdrs)
    umeds = timings.get("units", {})
    grew = (any(t > meds[l] for l, t in rec["lines"].items() if l in meds)
            or any(t > umeds.get(s, {}).get(u, t) or u not in umeds.get(s, {})
                   for s, d in rec.get("units", {}).items() for u, t in d.items()))
    gb = groups(hdrs, base, prev)
    if grew or split_candidates(gb, base) or over_budget(gb, base):
        selected, how = pr_selection(env, deps)
    else:
        selected, how = (), "no line ran slower than its median and none is over the per-line limit"
    print("selection: " + how)
    mt = measured_timings(timings, rec, selected, hdrs)
    gs = groups(hdrs, mt, prev)
    fresh = unrecorded(groups(hdrs, timings, prev))      # no main run has timed these: warned, never failed
    for label, m in sorted(mt["measured"].items()):
        print("measured  %s: this run %ss, main median %s: judged at %ss" % (
            label, m["run"], "none" if m["median"] is None else "%ss" % m["median"], mt["lines"][label]))
    for g in gs:
        est, missing = estimate(g, mt)
        b = budget(g["tier"])
        print("%-22s %2d line(s)  estimated %4ds of %4ds budget (%3d%%)%s" % (
            g["name"], len(g["lines"]), est, b, 100 * est / b,
            "" if not missing else "  NO TIMING (counted as %ds each): %s" % (TIERS[g["tier"]][3], "; ".join(missing))))
    faults = budget_faults(gs, mt, selected, fresh=fresh)
    warn(line_faults(gs, mt, selected, fresh=fresh)[1])
    warn(group_faults(gs, mt, selected, fresh=fresh)[1], "over budget")
    for x in faults:
        print("FAIL  " + x)
    print("check-measured: %s (run %s: %d line(s) timed, %d judged on this run's time; setup %ds, main's median; timings "
          "from main run %s)" % ("FAILED" if faults else "PASS", run_id, len(rec["lines"]), len(mt["measured"]),
                                  mt.get("setup", SETUP), timings.get("run")))
    return 1 if faults else 0


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
    p = parse("verify-x.py", "# ci-line: C1 | X | --selftest && --level 1\n")
    check("&& runs the script twice",
          p["lines"] == [("C1", "X", "python scripts/verify-x.py --selftest && python scripts/verify-x.py --level 1")])
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
    ga = groups(hd5, alone, {})
    check("(a) the same run alone (the old rule) puts its groups past 80%%: on main now an over-budget warning, not the "
          "refusal that turned every PR red (MAIN-WARN reverses CI-TIMINGS-MEDIAN's fail-on-main below 100%%): %d warning(s)"
          % len(group_faults(ga, alone)[1]),
          not budget_faults(ga, alone) and group_faults(ga, alone)[1] and budget_faults(ga, alone, True))
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
    check("strict (the base unreadable): the line fails", len(budget_faults(g170, ft, True)) == 1)
    f400 = one(400)
    check("PLANT: past 100% the group rule fails whatever is selected (a 400 s line; main, unselected, selected, all)",
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
    check("selection on a PR that changes CI: none of its own (%s)" % how2, sel2 == ())
    fl, wn = line_faults(g170, ft, sel2)
    check("a CI PR and an unchanged line over the limit: a warning, never a fault (Jon, 21 Oct): %s" % (wn[:1],),
          not fl and len(wn) == 1 and "split candidate" in wn[0] and not budget_faults(g170, ft, sel2))
    check("a CI PR and a group past 100%: still a fault (past HARD the group rule holds whatever is selected)",
          any("past 80%" in x for x in budget_faults(groups(hs, f400, {}), f400, sel2)))
    # PR-MEASURED (Jon, 25 Oct 2026): a PR is also judged on its own run's measured times. Line a is verify-x.py's; setup
    # 20 s, budget 270 s: the per-line limit is 189 s, a group fails past 216 s.
    import contextlib, io
    run = lambda lines: {"run": 1, "lines": dict(lines)}
    hr = {"verify-x.py": parse("verify-x.py", "# ci-line: a2 | \n"),          # #526's shape: "a" renamed "a2"
          "verify-y.py": parse("verify-y.py", "".join("# ci-line: %s | \n" % x for x in "bcde"))}
    check("PLANT (1) before: a renamed line with no median passes --check on the 120 s default",
          not budget_faults(groups(hr, t, {}), t, X))
    mt = measured_timings(t, run({"a2": 205}), X, hr)
    fl = budget_faults(groups(hr, mt, {}), mt, X)
    check("PLANT (1) #526's shape: a renamed line, no median, measured 205 s: a fault naming the line, \"none\", 205 s and "
          "its group: %s" % (fl[:1],), bool(fl) and all("a2 205s" in x and "main median none, this run 205s" in x
                                                         and "Content verifiers" in x for x in fl))
    mt = measured_timings(t, run({"a": 200}), X, hs)
    fl = budget_faults(groups(hs, mt, {}), mt, X)
    check("PLANT (2) #525's shape: a selected line, median 100 s, measured 200 s: a fault naming both figures: %s" % (fl[:1],),
          mt["lines"]["a"] == 200 and bool(fl) and any("main median 100s, this run 200s" in x for x in fl))
    mt = measured_timings(t, run({"a": 200}), (), hs)
    check("PLANT (3) an unselected line measured slow on a run-all PR keeps its median (%ss): no fault" % mt["lines"]["a"],
          mt["lines"]["a"] == 100 and not budget_faults(groups(hs, mt, {}), mt, ()))
    mt = measured_timings(t, run({"a": 50}), X, hs)
    check("PLANT (4) a measured time below the median never lowers the estimate (100 s measured 50 s: %ss)" % mt["lines"]["a"],
          mt["lines"]["a"] == 100 and mt["setup"] == 20)
    check("the setup is the committed median, never the run's",
          measured_timings(t, dict(run({"a": 200}), setup=125), X, hs)["setup"] == 20)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc_none = check_measured("1", None, {}, rec={"lines": {}}, timings=t, hdrs=hs, prev={})
        rc_push = check_measured("1", None, {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push"}, rec=run({"a": 400}),
                                 timings=t, hdrs=hs, prev={})
    said = out.getvalue()
    check("PLANT (5) no artifacts: exit 0 with a reason (%r)" % said.splitlines()[0][:60],
          rc_none == 0 and "no content or lock timing file" in said)
    check("not a pull request (a push run with a 400 s line): exit 0 with a reason", rc_push == 0 and "not a pull request" in said)
    with tempfile.TemporaryDirectory() as td:
        ev = os.path.join(td, "event.json")
        with open(ev, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"pull_request": {"base": {"sha": "0123456789abcdef"}}}, f)
        env = {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request", "GITHUB_EVENT_PATH": ev}
        with contextlib.redirect_stdout(io.StringIO()) as o1:
            rc1 = check_measured("1", None, env, rec=run({"a2": 205}), timings=t, hdrs=hr, prev={},
                                 deps=Deps(["scripts/verify-x.py"], (False, [], {"scripts/verify-x.py": []})))
        with contextlib.redirect_stdout(io.StringIO()) as o2:
            rc2 = check_measured("1", None, env, rec=run({"a": 90, "b": 55}), timings=t, hdrs=hs, prev={},
                                 deps=Deps(["scripts/verify-x.py"], (False, [], {"scripts/verify-x.py": []})))
    check("end to end, #526's shape on a pull request run (WARN-THEN-ENFORCE, Jon 27 Oct: a line no main run has timed is "
          "warned, never failed): exit 0, the line named in a warning",
          rc1 == 0 and "a2 205s" in o1.getvalue() and "no time recorded by a main run" in o1.getvalue())
    check("end to end, a run at or under its medians: exit 0", rc2 == 0 and "check-measured: PASS" in o2.getvalue())
    # MAIN-WARN (Jon, 25 Oct 2026): a group between 80% and 100% of its budget is a warning on main, recorded in the pack, and a
    # fault only on a PR that selects one of its scripts; past 100% it fails everywhere. #526's shape: Shape Shifter, one line,
    # 202 s + 20 s setup = 222 s, 82% of 270 s; at 253 s it is 273 s, 101%.
    SS = "scripts/verify-shape-shifter.py"
    hss = {"verify-shape-shifter.py": parse("verify-shape-shifter.py", "# ci-line: Shape Shifter | \n"),
           "verify-y.py": parse("verify-y.py", "".join("# ci-line: %s | \n" % x for x in "bcde"))}
    ss = lambda sec: dict(t["lines"], **{"Shape Shifter": sec})
    for sec, want in ((202, "82%"), (253, "101%")):
        exm = {}
        for n in range(1, 5):
            exm = add_run(exm, rn(n, 20, ss(sec)))
        wrote.clear()
        packed.clear()
        with contextlib.redirect_stdout(io.StringIO()) as o:
            rcm = main_pack(exm, rn(5, 20, ss(sec)), hss, {}, sink4)
        said = o.getvalue()
        if sec == 202:
            ob = packed[-1].get("over-budget") if packed else None
            check("PLANT (1) #526's shape on main, a group at %s: timings and pack written, exit %d, the pack's over-budget "
                  "lists it (%s), a warning names the group and Shape Shifter" % (want, rcm, ob and ob[0]["group"]),
                  rcm == 0 and wrote == ["timings", "pack"] and ob and ob[0]["percent"] == 82
                  and ob[0]["lines"][0]["label"] == "Shape Shifter" and ob[0]["lines"][0]["script"] == SS
                  and re.search(r"WARN  over budget.*Content verifiers \d+: estimated 222s.*Shape Shifter 202s", said))
        else:
            check("PLANT (2) a group at %s on main: the pack is refused, exit %d, nothing written" % (want, rcm),
                  rcm == 1 and not wrote and "past 100% of its budget" in said)
    t82 = T(ss(202))
    g82 = groups(hss, t82, {})
    check("PLANT (3) a PR that selects a script in a group at 82%: a fault naming it",
          any("estimated 222s" in x and SS in x for x in budget_faults(g82, t82, {SS})))
    fl, wn = group_faults(g82, t82, Y)
    check("PLANT (4) a PR that selects none of its scripts: a warning only (%s)" % (wn[:1],),
          not fl and not budget_faults(g82, t82, Y) and len(wn) == 1 and "over budget" in wn[0] and "Shape Shifter" in wn[0])
    with tempfile.TemporaryDirectory() as td:
        ev = os.path.join(td, "event.json")
        with open(ev, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"pull_request": {"base": {"sha": "0123456789abcdef"}}}, f)
        sel5, how5 = pr_selection({"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request", "GITHUB_EVENT_PATH": ev},
                                  Deps([".github/workflows/check-site.yml"], (True, ["CI itself"], {})))
    check("PLANT (5) a run-all PR (CI itself): a warning only (%s)" % how5,
          sel5 == () and not budget_faults(g82, t82, sel5) and len(group_faults(g82, t82, sel5)[1]) == 1)
    check("PLANT (6) the base unreadable (every line selected): a fault", len(group_faults(g82, t82, True)[0]) == 1
          and bool(budget_faults(g82, t82, True)))
    check("a pack with no group past 80% carries an empty over-budget list",
          pack_record(groups(hs, t, {}), t)["over-budget"] == [])
    # WARN-THEN-ENFORCE (Jon, 27 Oct 2026). Setup 20 s, budget 270 s: per-line limit 189 s, a group fails past 216 s.
    # Line a is verify-x.py's; b to e are verify-y.py's.
    fl, wn = line_faults(g170, ft, X, listed=["a"])
    check("PLANT (w1) a listed 170 s line the PR selects: a warning naming the warn list, no fault",
          not fl and len(wn) == 1 and "on the warn list" in wn[0] and "a 170s" in wn[0])
    fl, wn = line_faults(g170, ft, X, listed=["b"])
    check("PLANT (w2) an unlisted 170 s line the PR selects still fails while another line is listed", len(fl) == 1)
    hsh = {"verify-x.py": parse("verify-x.py", "# ci-shards: A | | 2\n"),
           "verify-y.py": parse("verify-y.py", "".join("# ci-line: %s | \n" % x for x in "bcde"))}
    tsh = T(dict(t["lines"], **{"A, part 1 of 2": 170, "A, part 2 of 2": 30}))
    gsh = groups(hsh, tsh, {})
    fl, wn = line_faults(gsh, tsh, X, listed=["A"])
    check("PLANT (w3) a sharded verifier is listed by its own label: its part over the limit warns",
          not fl and any("on the warn list" in w and "A, part 1 of 2" in w for w in wn)
          and len(line_faults(gsh, tsh, X, listed=[])[0]) == 1)
    g82l = groups(hss, t82, {})
    check("PLANT (w4) a group at 82% that the PR selects, its long line listed: a warning, no fault",
          not group_faults(g82l, t82, {SS}, listed=["Shape Shifter"])[0]
          and any("warn-listed" in w for w in group_faults(g82l, t82, {SS}, listed=["Shape Shifter"])[1])
          and group_faults(g82l, t82, {SS}, listed=[])[0])
    hnew = {"verify-x.py": parse("verify-x.py", "# ci-line: brand new | \n"),
            "verify-y.py": parse("verify-y.py", "".join("# ci-line: %s | \n" % x for x in "bcde"))}
    tnew = T(dict(t["lines"]))
    gnew = groups(hnew, tnew, {})
    fl, wn = line_faults(gnew, tnew, X)
    check("PLANT (w5) a new line with no recorded time, selected: estimated and warned, never a fault (%s)" % (wn[:1],),
          not budget_faults(gnew, tnew, X) and any("no time recorded by a main run" in w and "brand new" in w for w in wn))
    t400 = T(dict(t["lines"], b=150))
    hn2 = {"verify-x.py": parse("verify-x.py", "# ci-line: n1 | \n# ci-line: n2 | \n"),
           "verify-y.py": parse("verify-y.py", "# ci-line: b | \n")}
    gn2 = [{"id": "1", "tier": "content", "name": "Content verifiers 1", "lines": [("n1", "python scripts/verify-x.py"),
            ("n2", "python scripts/verify-x.py"), ("b", "python scripts/verify-y.py")],
            "secs": {"n1": 120, "n2": 120, "b": 150}, "timed": ["b"]}]
    check("PLANT (w6) a group past 100% only on two unrecorded lines (120 + 120 + 150 + 20 s): a warning everywhere",
          not group_faults(gn2, t400, True)[0] and group_faults(gn2, t400, True)[1])
    gn3 = [dict(gn2[0], secs={"n1": 120, "n2": 120, "b": 280}, timed=["b"])]
    check("PLANT (w7) the same group with a recorded line alone past 100%: a fault everywhere",
          bool(group_faults(gn3, t400, ())[0]))
    mt9 = measured_timings(t, run({"a2": 205}), X, hr)
    g9 = groups(hr, mt9, {})
    f9 = unrecorded(groups(hr, t, {}))
    check("PLANT (w8) a new line measured at 205 s on its own PR run (#526's shape, 84%): a warning, never a failure",
          "a2" in f9 and not budget_faults(g9, mt9, X, fresh=f9))
    mt10 = measured_timings(t, run({"a2": 300}), X, hr)
    check("PLANT (w9) a new line measured at 300 s (past 100%: it would refuse main's pack after the merge): a fault",
          bool(budget_faults(groups(hr, mt10, {}), mt10, X, fresh=f9)))
    check("stale: a listed line inside the limit now, and a label no line has, are stale; a listed line over it is not",
          sorted(b for b, _ in stale_entries(g170, ft, ["a", "b", "gone"])) == ["b", "gone"])
    check("stale: a listed line no main run has timed is kept (it cannot be judged yet)",
          stale_entries(gnew, tnew, ["brand new"]) == [])
    check("shrink-only: a PR that adds an entry is a fault; one that removes an entry, or leaves the list alone, is not",
          warn_list_faults(["a"], ["a", "b"], g170, ft) and not warn_list_faults(["a", "b"], ["a"], g170, ft)
          and not warn_list_faults(["a", "b"], ["a", "b"], g170, ft) and not warn_list_faults(None, ["a"], g170, ft))
    check("a PR that edits the list and leaves a stale entry in it: a fault (the known-failures pattern)",
          any("passes now" in x for x in warn_list_faults(["a", "b", "c"], ["a", "b"], g170, ft)))
    with tempfile.TemporaryDirectory() as td:
        wpath = os.path.join(td, "w.json")
        with open(wpath, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"about": "x", "per-line": ["a", "b"]}, f)
        gone = write_warn_list(g170, ft, path=wpath)
        kept = json.load(open(wpath, encoding="utf-8"))
    check("the timings job prunes the list: 'b' (inside the limit) removed, 'a' (over it) kept, the rest of the file kept",
          gone == ["b"] and kept == {"about": "x", "per-line": ["a"]})
    # The worst-case test (GATE-WARN-THEN-ENFORCE step 2): a gate change is judged on bank_common.py's selection.
    wsel = Deps([], (False, [], {"scripts/verify-x.py": [WORST_CASE], "scripts/verify-y.py": [WORST_CASE]}))
    t150 = one(150)                                   # a 150 s line + 20 s setup = 170 s: inside the 189 s limit
    g150 = groups(hs, t150, {})
    ap_, fl, _ = worst_case(["games/x/index.html"], wsel, g150, t150, [])
    check("worst case: a change with no gate file is not judged", not ap_ and not fl)
    ap_, fl, how = worst_case([".github/workflows/check-site.yml"], wsel, g150, t150, [], need=X | Y)
    check("worst case: a workflow change on today's timings passes (%s)" % how, ap_ and not fl)
    old = globals()["TARGET"]
    globals()["TARGET"] = 0.60                        # PLANT: a gate change lowering the per-line limit to 60% (162 s)
    try:
        ap_, fl, _ = worst_case(["scripts/ci-groups.py"], wsel, g150, t150, [], need=X | Y)
    finally:
        globals()["TARGET"] = old
    check("PLANT a gate change that breaks on a full selection (the per-line limit at 60%%) fails its own PR: %s" % (fl[:1],),
          ap_ and any("verify-x.py" in x and "per-line limit" in x for x in fl))
    ap_, fl, _ = worst_case(["scripts/merge-pr.py"], wsel, g150, t150, [], need=X | Y | {"scripts/verify-z.py"})
    check("PLANT an importer the bank_common selection misses: a fault naming it",
          any("verify-z.py imports bank_common" in x for x in fl))
    ap_, fl, _ = worst_case(["scripts/ci_shards.py"], Deps([], (True, ["CI itself"], {})), g150, t150, [])
    check("PLANT bank_common.py selecting everything (no real selection): a fault", ap_ and len(fl) == 1)
    check("gate files: the workflow, ci-groups, ci_shards, merge-pr, the context-size limit; not a game or a verifier",
          gate_paths([".github/workflows/x.yml", "scripts/ci-groups.py", "scripts/ci_shards.py", "scripts/merge-pr.py",
                      "scripts/check-context-size.py", "games/a/index.html", "scripts/verify-x.py", "scripts/bank_common.py"])
          == [".github/workflows/x.yml", "scripts/check-context-size.py", "scripts/ci-groups.py", "scripts/ci_shards.py",
              "scripts/merge-pr.py"])
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
    # SHARD (27 Oct 2026): a verifier's parts are chosen here from its units' times.
    check("ci_shards' own self-test (deal is a partition, stable and balanced; the unit line round-trips)",
          ci_shards.selftest())
    p = parse("verify-x.py", "# ci-shards: X (all) | --a | 3\n")
    check("ci-shards: label, args, parts until timed", p["shards"] == [("", "X (all)", "--a", 3)] and not p["errors"])
    p = parse("verify-x.py", "# ci-shards: lock | X | | 2\n")
    check("ci-shards in the lock tier, no args", p["shards"] == [("lock", "X", "", 2)])
    for bad, why in (("# ci-shards: X | --a\n", "no part count"), ("# ci-shards: X | --a && --b | 2\n", "'&&'"),
                     ("# ci-shards: X | --shard 1/2 | 2\n", "its own --shard"), ("# ci-shards: X | --a | 0\n", "0 parts")):
        check("ci-shards with %s is an error" % why, bool(parse("verify-x.py", bad)["errors"]))
    for bad in ("# ci-line: X, part 1 | --part 1\n", "# ci-line: X | --part=2/3\n", "# ci-line: X | --a && --part 3\n"):
        check("PLANT a hand split (%s) is an error: caught" % bad.split("|")[1].strip(), bool(parse("verify-x.py", bad)["errors"]))
    check("a ci-line with --part-selftest is not a hand split",
          not parse("verify-x.py", "# ci-line: X | --part-selftest\n")["errors"])
    check("two ci-shards headers in one verifier are an error",
          bool(errors({"verify-x.py": parse("verify-x.py", "# ci-shards: X | | 2\n# ci-shards: Y | | 2\n")})))
    check("ci-held and ci-shards together are an error",
          bool(errors({"verify-x.py": parse("verify-x.py", "# ci-shards: X | | 2\n# ci-held: why\n")})))
    sh = {"verify-x.py": parse("verify-x.py", "# ci-shards: X (all) | --a | 3\n")}
    gs0 = groups(sh, {"lines": {}, "setup": 20}, {})
    lines0 = [l for g in gs0 for l in g["lines"]]
    check("untimed: the header's 3 parts, each '<label>, part i of 3' running --shard i/3",
          sorted(lines0) == [("X (all), part %d of 3" % i, "python scripts/verify-x.py --a --shard %d/3" % i)
                             for i in (1, 2, 3)])
    cap = shard_cap("content", {"setup": 20})

    def grown_case():
        """PLANT (7): units that grow past the target are re-divided on the next repack (not kept at the old count)."""
        before = {"lines": {}, "setup": 20, "units": {"verify-x.py": dict.fromkeys("abcd", 40.0)},
                  "overhead": {"verify-x.py": 10}}
        g1 = groups(sh, before, {})
        k1 = g1[0]["shards"]["verify-x.py"]["parts"]
        after = dict(before, units={"verify-x.py": dict.fromkeys("abcd", 70.0)})
        g2 = groups(sh, after, pack_record(g1, before))
        k2 = g2[0]["shards"]["verify-x.py"]["parts"]
        ests = [g["secs"][l] for g in g2 for l, _ in g["lines"]]
        return k1 == 2 and k2 == 4 and all(e <= cap for e in ests), (k1, k2, ests)
    ok, got = grown_case()
    check("units grown past the target: re-divided 2 -> 4 parts, every part within %ds (%r)" % (cap, got), ok)
    real_choose = globals()["choose_parts"]
    globals()["choose_parts"] = lambda script, tier, start, timings, prev_k=None: (prev_k or start, "planted")
    try:
        caught = not grown_case()[0]
    finally:
        globals()["choose_parts"] = real_choose
    check("PLANT (7) the parts never re-divided once set (the hand split): caught", caught)
    t4 = {"lines": {}, "setup": 20, "units": {"verify-x.py": dict.fromkeys("abcd", 40.0)}, "overhead": {"verify-x.py": 10}}
    check("a previous count that still fits and is one more than needed is kept (no churn)",
          choose_parts("verify-x.py", "content", 3, t4, 3)[0] == 3 and choose_parts("verify-x.py", "content", 3, t4, 4)[0] == 2
          and choose_parts("verify-x.py", "content", 3, t4, 1)[0] == 2)

    def big_unit_case():
        """PLANT (8): a part still over the per-line limit after the repack (one unit too long to share a part) fails
        --check where the change selects its verifier, naming the unit."""
        tb = {"lines": {}, "setup": 20, "units": {"verify-x.py": {"big": 190.0, "small": 5.0}}, "overhead": {"verify-x.py": 10}}
        gb = groups(sh, tb, {})
        fs = budget_faults(gb, tb, {"scripts/verify-x.py"})
        ws = line_faults(gb, tb, ())[1]
        return (any("'big'" in f and "part 1 of 2" in f for f in fs)
                and any("'big'" in w for w in ws) and not line_faults(gb, tb, ())[0]), fs
    ok, got = big_unit_case()
    check("a part over the limit after the repack: a fault where selected, naming the unit; a warning elsewhere (%r)" % got, ok)
    real_units = globals()["unit_medians"]
    globals()["unit_medians"] = lambda script, timings: {}
    try:
        caught = not big_unit_case()[0]
    finally:
        globals()["unit_medians"] = real_units
    check("PLANT (8) parts judged without their units' times (a part over the limit goes unjudged): caught", caught)
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "timing.txt"), "w", encoding="utf-8", newline="") as f:
            f.write("Content verifiers 1\nregion: eastus\nunit  verify-x.py :: a  (40.0s)\nunit  verify-x.py :: b  (30.5s)\n"
                    "ok  X (all), part 1 of 2  (80s; group at 1m40s of 6m)\nunit  verify-x.py :: c  (12.0s)\n"
                    "ok  X (all), part 2 of 2  (15s; group at 1m55s of 6m)\nok  Other  (5s; group at 2m00s of 6m)\n\n"
                    "group total: 2m00s of 6m (budget 4m30s)\n")
        rec = read_run(1, d)
    check("a run's unit lines are recorded per verifier, with the part's overhead (its time less its units', the largest)",
          rec["units"] == {"verify-x.py": {"a": 40.0, "b": 30.5, "c": 12.0}} and rec["overhead"] == {"verify-x.py": 10}
          and rec["lines"]["X (all), part 1 of 2"] == 80 and rec["setup"] == 20)
    h = add_run(add_run(add_run({}, dict(rec, run=1)), dict(rec, run=2, units={"verify-x.py": {"a": 50.0}})),
                dict(rec, run=3, units={"verify-x.py": {"a": 60.0, "d": 1.0}}))
    check("unit medians over the runs that timed each unit, to a tenth",
          h["units"] == {"verify-x.py": {"a": 50.0, "b": 30.5, "c": 12.0, "d": 1.0}} and h["overhead"] == {"verify-x.py": 10})
    check("a history with no unit times has no units key", "units" not in add_run({}, {"run": 1, "date": "d", "lines": {}}))
    grown = {"lines": {}, "units": {"verify-x.py": {"a": 90.0, "e": 3.0}}, "overhead": {"verify-x.py": 25}}
    mt = measured_timings(dict(t4, lines={}), grown, {"scripts/verify-x.py"}, sh)
    mt0 = measured_timings(dict(t4, lines={}), grown, (), sh)
    check("--check-measured: a selected verifier's grown unit and overhead are judged at this run's time; a new unit counts",
          mt["units"]["verify-x.py"]["a"] == 90.0 and mt["units"]["verify-x.py"]["e"] == 3.0 and mt["overhead"]["verify-x.py"] == 25
          and mt0["units"]["verify-x.py"]["a"] == 40.0 and mt0["units"]["verify-x.py"]["e"] == 3.0
          and mt0["overhead"]["verify-x.py"] == 10)
    check("the pack records each sharded verifier's parts",
          pack_record(gs0, {"lines": {}, "setup": 20})["shards"]["verify-x.py"]["parts"] == 3)
    with open(WORKFLOW, encoding="utf-8") as f:
        wf = f.read()
    check("the group step gives ci_shards its timing file (export %s=\"$timing\")" % ci_shards.ENV,
          'export %s="$timing"' % ci_shards.ENV in wf)
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
    ap.add_argument("--check-measured", action="store_true", help="the budget check on this PR run's measured times "
                    "(needs --run-id and --from-dir)")
    ap.add_argument("--run-id", metavar="ID", help="with --check-measured: this run's id")
    ap.add_argument("--worst-case", action="store_true", help="a pull request touching the gate: the budget check on the "
                    "selection a change to scripts/bank_common.py makes (GATE-WARN-THEN-ENFORCE step 2)")
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
    if a.check_measured:
        return check_measured(a.run_id or "0", a.from_dir)
    if a.worst_case:
        base, why = pr_base()
        if base is None:
            print("worst-case: %s: nothing to judge (the test is for a pull request)" % why[1])
            return 0
        import importlib.util
        spec = importlib.util.spec_from_file_location("ci_deps", os.path.join(SCRIPTS, "ci-deps.py"))
        deps = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(deps)
        applies, faults, how = worst_case(deps.changed_since(base), deps)
        print("worst-case: " + how)
        for x in faults:
            print("FAIL  " + x)
        if applies:
            print("worst-case: %s" % ("FAILED" if faults else "PASS"))
        return 1 if faults else 0
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
        selected, how = (pr_selection() if split_candidates(gs, timings) or over_budget(gs, timings)
                         else ((), "no line is over the per-line limit and no group past %d%%" % (FAIL * 100)))
        print("selection: " + how)
        listed = read_warn_list()
        faults = budget_faults(gs, timings, selected, listed) + warn_list_faults(base_warn_list(), listed, gs, timings)
        warn(line_faults(gs, timings, selected, listed)[1])
        warn(group_faults(gs, timings, selected, listed)[1], "over budget")
        warn(["%s: %r passes now (%s); main's timings job removes it" % (WARN_LIST, b, why)
              for b, why in stale_entries(gs, timings, listed)], "warn list")
        for x in faults:
            print("FAIL  " + x)
        print("check: %s (pack to %d%% of each budget; a line past %d%% or a group past %d%% fails only where it is selected; "
              "a group past %d%% fails everywhere; timings from main run %s)"
              % ("FAILED" if faults else "PASS", TARGET * 100, TARGET * 100, FAIL * 100, HARD * 100, timings.get("run")))
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
