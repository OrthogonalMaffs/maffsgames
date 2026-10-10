#!/usr/bin/env python3
# ci-line: Escape-room lock bank (every lock-bank-batch*.txt: each VERIFY has exactly one answer, none is a restatement; a multi-line NOTE stays out of VERIFY; bad entries planted and caught) | --selftest
# ci-deps: docs/lock-bank-batch3.txt docs/lock-bank-batch4.txt docs/lock-bank-batch5.txt docs/lock-bank-batch6.txt docs/lock-bank-batch7.txt docs/lock-bank-batch8.txt docs/lock-bank-batch9.txt
"""Check a bank of escape-room locks for the only rule that really matters:
exactly one answer.

    python scripts/check-lock-bank.py docs/lock-bank-raw.txt   # one bank
    python scripts/check-lock-bank.py                          # every docs/lock-bank-batch*.txt
    python scripts/check-lock-bank.py --selftest               # planted entries, then every batch (CI)

Reads lock blocks in the format set out in docs/gemini-lock-brief.md, runs each
VERIFY expression, and reports anything that must not be built.

Three classes of problem, learned from two batches:

1. MULTIPLE OR NO SOLUTIONS. A lock with two answers is not a lock. Batch one
   had three of these.

2. A VERIFY THAT CANNOT FAIL. "[n for n in range(101) if n == <the answer>]"
   returns exactly one element no matter what the puzzle says, so it satisfies
   the letter of the request while testing nothing. Detected here by AST: a
   condition comparing the loop variable to an expression that does not mention
   the loop variable is a restatement, not a constraint.

3. EXACT FLOAT EQUALITY. 6e5 / 1.5e-4 is 4000000000.0000005, not 4e9, so a
   correct puzzle gets rejected. Flagged so it can be rewritten with a
   tolerance.

Locks whose answer is a minimum or maximum use VERIFY_MIN / VERIFY_MAX, which
return the whole candidate set; uniqueness is inherent in taking the extreme.

Exit code is non-zero if any lock fails, so it can gate a build step.
"""
import ast
import math  # noqa: F401 - available to VERIFY expressions
import re
import sys
from fractions import Fraction  # noqa: F401 - ditto

# NOTE is a field like the others (contract LOCK-BANK-CI, 10 Oct 2026): a note may span lines, and before it
# was listed here its indented continuation lines were glued onto the field above it -- in
# hamster-feeder-bounds, onto VERIFY, which then raised SyntaxError and rejected a sound lock.
FIELDS = ("ID", "LEVEL", "TOPIC", "INSTRUMENT", "CONTEXT", "CLUE", "ANSWER",
          "AHA", "MISCONCEPTION", "SOLVE", "TIME", "VERIFY", "VERIFY_MIN",
          "VERIFY_MAX", "NOTE")

# Only what a VERIFY line legitimately needs. The bank is text from a language
# model, not trusted code.
SAFE = {
    "range": range, "len": len, "set": set, "str": str, "int": int,
    "float": float, "abs": abs, "sum": sum, "min": min, "max": max,
    "sorted": sorted, "round": round, "map": map, "filter": filter,
    "list": list, "tuple": tuple, "any": any, "all": all, "zip": zip,
    "enumerate": enumerate, "divmod": divmod, "pow": pow,
    "math": math, "Fraction": Fraction, "__builtins__": {},
}


def parse(text):
    """Returns (locks, strays).

    Continuation lines are indented; anything starting in column 0 that is not
    a FIELD line is a heading, not part of the field above it. Gluing a section
    heading onto a VERIFY line is a silent way to break a sound lock, so those
    are collected and reported rather than appended.
    """
    locks, cur, strays = [], {}, []
    for raw in text.splitlines():
        line = raw.rstrip()
        m = re.match(r"^\s*([A-Z_]+):\s*(.*)$", line)
        if m and m.group(1) in FIELDS:
            key, val = m.group(1), m.group(2)
            if key == "ID" and cur:
                locks.append(cur)
                cur = {}
            cur[key] = val
        elif cur and line.strip() and not line.strip().startswith("```"):
            if raw[:1].strip():
                strays.append(line)
                continue
            last = list(cur)[-1]
            cur[last] = (cur[last] + " " + line.strip()).strip()
    if cur:
        locks.append(cur)
    return locks, strays


def is_tautological(expr):
    """True if the comprehension merely restates its own answer.

    Catches `[n for n in range(101) if n == <no mention of n>]` and the
    `[... ][0]` form, both of which return one element regardless of whether
    the puzzle is sound.
    """
    try:
        tree = ast.parse(expr, mode="eval").body
    except SyntaxError:
        return False
    if isinstance(tree, ast.Subscript):        # [...][0] always yields one
        return True
    if isinstance(tree, ast.List):             # a literal list has fixed length
        return True
    if not isinstance(tree, (ast.ListComp, ast.GeneratorExp)):
        return False
    targets = set()
    for gen in tree.generators:
        for node in ast.walk(gen.target):
            if isinstance(node, ast.Name):
                targets.add(node.id)
    if not targets:
        return False
    conds = [c for gen in tree.generators for c in gen.ifs]
    if not conds:
        return False

    def mentions(node):
        return any(isinstance(n, ast.Name) and n.id in targets
                   for n in ast.walk(node))

    # Every condition being "target == (something with no target in it)" means
    # the answer was computed and then matched.
    for cond in conds:
        if not (isinstance(cond, ast.Compare) and len(cond.ops) == 1
                and isinstance(cond.ops[0], ast.Eq)):
            return False
        left, right = cond.left, cond.comparators[0]
        lt, rt = mentions(left), mentions(right)
        if not ((lt and not rt) or (rt and not lt)):
            return False
        bare = left if lt else right
        if not isinstance(bare, ast.Name):
            return False
    return True


def risky_float_equality(expr):
    """Exact == between values produced by division or float literals."""
    try:
        tree = ast.parse(expr, mode="eval").body
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and any(isinstance(o, ast.Eq) for o in node.ops):
            for side in [node.left] + list(node.comparators):
                for n in ast.walk(side):
                    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div):
                        return True
                    if isinstance(n, ast.Constant) and isinstance(n.value, float):
                        return True
    return False


def check(lock):
    """Return (ok, note)."""
    kind = ("VERIFY_MIN" if "VERIFY_MIN" in lock else
            "VERIFY_MAX" if "VERIFY_MAX" in lock else "VERIFY")
    expr = lock.get(kind, "").strip()
    if not expr:
        return False, "no VERIFY line"

    notes = []
    if kind == "VERIFY" and is_tautological(expr):
        notes.append("VERIFY only restates the answer - it cannot fail, so this lock is UNCHECKED")
    if risky_float_equality(expr):
        notes.append("exact == on a float; use a tolerance")

    try:
        result = eval(expr, SAFE, {})  # noqa: S307 - sandboxed above
    except Exception as e:  # noqa: BLE001
        return False, "VERIFY raised %s: %s" % (type(e).__name__, e)
    try:
        result = list(result)
    except TypeError:
        return False, "VERIFY returned %r, not a list" % (result,)

    if kind == "VERIFY":
        if len(result) == 0:
            extra = " (" + "; ".join(notes) + ")" if notes else ""
            return False, "NO solutions - unsolvable as written" + extra
        if len(result) > 1:
            return False, "%d solutions: %s - not a lock" % (len(result), result[:5])
        got = result[0]
    else:
        if not result:
            return False, "NO candidates for a %s" % kind
        got = min(result) if kind == "VERIFY_MIN" else max(result)

    stated = lock.get("ANSWER", "").strip()
    want = re.findall(r"-?\d+\.?\d*", stated)
    have = re.findall(r"-?\d+\.?\d*", str(got))
    if want and have and not set(want) & set(have):
        notes.append("computed %s but ANSWER says %r" % (got, stated))

    mins = re.findall(r"\d+", lock.get("TIME", ""))
    if mins and int(mins[0]) > 6:
        notes.append("TIME %s min is long for a 15-minute room" % mins[0])

    ok = not any("UNCHECKED" in n or "ANSWER says" in n for n in notes)
    return ok, ("unique (%s)" % (got,)) + ("; " + "; ".join(notes) if notes else "")


# Planted entries for --selftest: (name, bank text, the IDs that must be rejected).
_GOOD = """ID:          plant-good
ANSWER:      5
VERIFY:      [x for x in range(16) if x**2 - 12*x + 35 == 0 and x < 6]
NOTE:        A note over two lines, as hamster-feeder-bounds has. Its continuation must stay
             in NOTE and never reach VERIFY.
"""
PLANTS = [
    ("a sound lock with a multi-line NOTE", _GOOD, set()),
    ("two answers", _GOOD.replace("plant-good", "plant-two").replace(" and x < 6", ""), {"plant-two"}),
    ("a VERIFY that only restates the answer", "ID:          plant-restate\nANSWER:      5\n"
     "VERIFY:      [n for n in range(10) if n == 5]\n", {"plant-restate"}),
    ("the wrong answer", _GOOD.replace("plant-good", "plant-wrong").replace("ANSWER:      5", "ANSWER:      7"),
     {"plant-wrong"}),
]


def run_bank(path):
    """Returns the IDs rejected in one bank file (or None if it has no lock blocks)."""
    with open(path, encoding="utf-8") as f:
        locks, strays = parse(f.read())
    print("== %s" % path)
    for line in strays:
        print("ignored (heading, not a continuation line): %s" % line.strip()[:70])
    if not locks:
        print("No lock blocks found. Check the file matches the brief's format.")
        return None

    bad = []
    print("%-30s %-7s %s" % ("ID", "STATUS", "NOTE"))
    print("-" * 96)
    for lock in locks:
        ok, note = check(lock)
        if not ok:
            bad.append(lock.get("ID", "?"))
        print("%-30s %-7s %s" % (lock.get("ID", "?")[:30], "ok" if ok else "REJECT", note))

    print("-" * 96)
    print("%d locks, %d usable, %d rejected." % (len(locks), len(locks) - len(bad), len(bad)))
    if bad:
        print("Rejected: " + ", ".join(bad))
    return bad


def selftest():
    ok = True
    for name, text, want in PLANTS:
        locks, _ = parse(text)
        got = {l.get("ID") for l in locks if not check(l)[0]}
        hit = got == want
        ok = ok and hit
        print("  %s  planted: %s" % ("caught" if hit else "MISSED", name))
    return ok


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    ok = True
    if args[:1] == ["--selftest"]:
        print("self-test (planted entries):")
        ok = selftest()
        args = args[1:]
    if not args:
        import glob, os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        args = sorted(glob.glob(os.path.join(root, "docs", "lock-bank-batch*.txt")),
                      key=lambda p: int(re.search(r"batch(\d+)", p).group(1)))
    for path in args:
        bad = run_bank(path)
        if bad is None or bad:
            ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
