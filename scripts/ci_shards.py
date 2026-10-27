"""Work units and CI parts: how a long verifier's work is divided between CI lines (contract SHARD, Jon 27 Oct 2026;
canon §7.8.1).

Until SHARD each long verifier divided its own work into parts by hand (`--part 3`, `--part 2/6`, a PARTS tuple, plants
dealt modulo four), and ci-groups.py could only move whole lines between jobs. When a part outgrew the per-line limit
the first PR that ran it went red: Shape Shifter on 26 Oct (a part grew), Just Pythag It, Bruv on 27 Oct (the job
setup grew). Now a verifier lists its work as named units and runs the slice CI hands it; ci-groups.py chooses how many
parts each verifier has, from its units' median times, on every main repack.

A verifier declares, instead of its ci-lines,

    # ci-shards: <label> | <args> | <parts until timed>
    # ci-shards: lock | <label> | <args> | <parts until timed>

and ci-groups.py turns that into k lines, "<label>, part i of k", each running `python scripts/<it>.py <args> --shard i/k`.
<parts until timed> is k until a main run has timed the verifier's units; after that k is chosen from the timings.

In the verifier (bank_common re-exports these as bc.Shard and bc.shard_args):

    ap = argparse.ArgumentParser(); bc.shard_args(ap)
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    for uid in shard.pick(["sessions", "fit 320x568", ...]):     # every unit, in run order; this run's slice comes back
        with shard.unit(uid):
            ...                                                   # the unit's work, exactly as before

pick() deals the units into k parts with deal() and the committed medians (scripts/ci-timings.json "units"), so the
k runs of one CI run, which all read the same file, are a partition of the units: each unit runs in exactly one part,
whatever units the verifier has, and a unit the timings do not know yet counts at the mean of those they do. With no
--shard, pick() returns every unit (the full local run). --list-units prints the units and exits.

unit() times the unit and, in CI, appends "unit  <script> :: <unit id>  (<seconds>s)" to the group's timing file
($CI_UNIT_TIMING); ci-groups.py --record-and-pack records the medians, and the next repack re-divides. A verifier that
runs W units at once declares concurrency=W, and each unit is recorded at its wall time / W (its share of the line).

Stdlib only: ci-groups.py imports this in the plan job, which installs nothing.
"""
import contextlib
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMINGS = os.path.join(ROOT, "scripts", "ci-timings.json")
ENV = "CI_UNIT_TIMING"                      # the group step's timing file (check-site.yml)
UNIT_LINE = re.compile(r"^unit  (\S+) :: (.+)  \((\d+(?:\.\d+)?)s\)$")
SPEC = re.compile(r"^(\d+)/(\d+)$")
DEFAULT_UNIT = 1.0                          # seconds for a unit, when no unit of its verifier has been timed


def parse_spec(spec):
    """'i/k' -> (i, k), 1 <= i <= k; anything else raises ValueError."""
    m = SPEC.match(str(spec or ""))
    if not m or not 1 <= int(m.group(1)) <= int(m.group(2)):
        raise ValueError("--shard takes i/k with 1 <= i <= k, not %r" % (spec,))
    return int(m.group(1)), int(m.group(2))


def deal(units, k, times, default=None):
    """[[unit ids]] * k: the units dealt into k parts as evenly as their times allow, each part in the units' own order.
    Largest first, each to the part with the least time so far (ties: the lower part); a unit with no time counts at
    `default`, else at the mean of the units that have one (DEFAULT_UNIT if none has). Deterministic: the same units,
    k and times give the same parts. Every unit is in exactly one part."""
    if k < 1:
        raise ValueError("deal into %d parts" % k)
    known = [times[u] for u in units if u in times]
    d = default if default is not None else (sum(known) / len(known) if known else DEFAULT_UNIT)
    est = [times.get(u, d) for u in units]
    bins, load = [[] for _ in range(k)], [0.0] * k
    for n in sorted(range(len(units)), key=lambda n: (-est[n], n)):
        b = min(range(k), key=lambda j: (load[j], j))
        bins[b].append(n)
        load[b] += est[n]
    return [[units[n] for n in sorted(b)] for b in bins]


def unit_times(script, timings=None):
    """{unit id: median seconds} for a verifier (its file name), from ci-timings.json's "units"."""
    if timings is None:
        try:
            with open(TIMINGS, encoding="utf-8") as f:
                timings = json.load(f)
        except (OSError, ValueError):
            timings = {}
    return dict(timings.get("units", {}).get(os.path.basename(script), {}))


def check_ids(units):
    """The faults in a unit list: a repeated id, an empty one, or one the timing line cannot carry."""
    out, seen = [], set()
    for u in units:
        if not isinstance(u, str) or not u.strip() or u != u.strip():
            out.append("unit id %r: a non-empty string without outer spaces" % (u,))
        elif "\n" in u or " :: " in u or "  (" in u:
            out.append("unit id %r: no newline, ' :: ' or '  ('" % u)
        if u in seen:
            out.append("unit id %r twice" % (u,))
        seen.add(u)
    return out


def shard_args(ap):
    """Add --shard i/k and --list-units to an argparse parser."""
    ap.add_argument("--shard", metavar="I/K", default=None,
                    help="run part I of K of this verifier's work units (CI: scripts/ci-groups.py chooses K)")
    ap.add_argument("--list-units", action="store_true", help="print this verifier's work units and exit")
    return ap


class Shard:
    """One run's slice of a verifier's units (see the module docstring)."""

    def __init__(self, script, args=None, spec=None, list_units=False, concurrency=1, timings=None, out=None):
        self.script = os.path.basename(script)
        self.spec = getattr(args, "shard", None) if args is not None else spec
        self.list_units = getattr(args, "list_units", False) if args is not None else list_units
        self.concurrency = max(1, int(concurrency))
        self.timings = timings
        self.out = out                                  # a file path for the unit lines; default $CI_UNIT_TIMING
        self.times = {}                                 # unit id -> seconds, this run
        if self.spec is not None:
            parse_spec(self.spec)

    def pick(self, units):
        """This run's units, in the order given: all of them with no --shard, else part i of k."""
        units = list(units)
        bad = check_ids(units)
        if bad:
            raise ValueError("%s: %s" % (self.script, "; ".join(bad)))
        if self.list_units:
            for u in units:
                print(u)
            sys.exit(0)
        if self.spec is None:
            return units
        i, k = parse_spec(self.spec)
        mine = deal(units, k, unit_times(self.script, self.timings))[i - 1]
        print("%s --shard %d/%d: %d of %d unit(s)" % (self.script, i, k, len(mine), len(units)))
        return mine

    @contextlib.contextmanager
    def unit(self, uid):
        """Time one unit; in CI, write its line to the group's timing file (also when the unit raises)."""
        t0 = time.monotonic()
        try:
            yield
        finally:
            self.record(uid, time.monotonic() - t0)

    def record(self, uid, wall):
        secs = round(wall / self.concurrency, 1)
        self.times[uid] = secs
        path = self.out or os.environ.get(ENV)
        if path:
            with open(path, "a", encoding="utf-8") as f:
                f.write("unit  %s :: %s  (%ss)\n" % (self.script, uid, secs))


def read_units(text):
    """[(script, unit id, seconds)] from a timing file's text, in order."""
    return [(m.group(1), m.group(2), float(m.group(3))) for m in (UNIT_LINE.match(l) for l in text.splitlines()) if m]


def selftest():
    """deal() is a partition and stable; the timing line round-trips; the spec and id checks refuse what they must."""
    import random
    import tempfile
    fails = []
    rng = random.Random(7)
    for trial in range(300):
        n = rng.randint(0, 40)
        units = ["u%d" % x for x in range(n)]
        times = {u: rng.choice([0.1, 1, 5, 30, 120]) for u in units if rng.random() < 0.7}
        for k in (1, 2, 3, 5, 9):
            parts = deal(units, k, times)
            flat = [u for p in parts for u in p]
            if sorted(flat) != sorted(units) or len(flat) != len(set(flat)) or len(parts) != k:
                fails.append("deal is not a partition: n=%d k=%d" % (n, k))
            if any(p != [u for u in units if u in p] for p in parts):
                fails.append("a part is not in the units' order: n=%d k=%d" % (n, k))
            if parts != deal(list(units), k, dict(times)):
                fails.append("deal is not deterministic: n=%d k=%d" % (n, k))
    # balance: the classic case
    if [sorted(p) for p in deal(list("abcdef"), 2, dict(zip("abcdef", [8, 7, 6, 5, 4, 3])))] != [["a", "d", "e"], ["b", "c", "f"]]:
        fails.append("deal does not balance 8 7 6 5 4 3 into 17 / 16")
    # planted: a deal that drops a unit, and one that doubles one, are caught by the partition test above
    def bad_drop(units, k, times):
        p = deal(units, k, times)
        return [x[1:] if x else x for x in p]
    p = bad_drop(["a", "b", "c"], 2, {})
    if sorted(u for x in p for u in x) == ["a", "b", "c"]:
        fails.append("plant: a dropped unit was not noticed")
    for bad in ("0/2", "3/2", "2", "a/b", "", None):
        try:
            parse_spec(bad)
            fails.append("parse_spec accepted %r" % (bad,))
        except ValueError:
            pass
    if not check_ids(["a", "a"]) or not check_ids(["x :: y"]) or not check_ids([" a"]) or check_ids(["fit 320x568", "plant: x"]):
        fails.append("check_ids is wrong")
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "t.txt")
        s = Shard("verify-x.py", spec="2/3", timings={"units": {"verify-x.py": {"a": 9, "b": 1, "c": 1}}}, out=path)
        got = s.pick(["a", "b", "c", "d"])
        if got != deal(["a", "b", "c", "d"], 3, {"a": 9, "b": 1, "c": 1})[1]:
            fails.append("pick is not deal's part i")
        for u in got:
            with s.unit(u):
                pass
        w = Shard("verify-y.py", spec=None, concurrency=4, out=path)
        if w.pick(["p", "q"]) != ["p", "q"]:
            fails.append("pick with no --shard is not every unit")
        w.record("p", 8.0)
        back = read_units(open(path, encoding="utf-8").read())
        if [b[:2] for b in back] != [("verify-x.py", u) for u in got] + [("verify-y.py", "p")] or back[-1][2] != 2.0:
            fails.append("the timing lines do not round-trip: %r" % back)
    for f in fails:
        print("FAIL  " + f)
    print("ci_shards self-test: %s" % ("FAILED" if fails else "PASS"))
    return not fails


if __name__ == "__main__":
    sys.exit(0 if selftest() else 1)
