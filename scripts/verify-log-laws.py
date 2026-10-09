#!/usr/bin/env python3
# ci-line: Log Laws Solve (layers C + D, SymPy) | --require-katex
"""Layers C + D verification for log-laws Solve mode
(docs/next-contract-log-laws-solve.md, step 6; design in docs/log-laws-solve-build-notes.md).

WHY THIS READS THE LIVE PAGE, NOT A HAND-COPY OF THE POOLS
----------------------------------------------------------
A Python re-implementation of the six families could drift from the game and would
then be verifying itself. The game builds every line of working once, as an
expression tree, and exports the result on window.LL_SOLVE: for each line the TeX the
student sees and the SymPy text of the same tree. This script launches the stub
server (CLAUDE.md: "ALWAYS use the stub server"), reads window.LL_SOLVE back from
the loaded page, and checks THAT data with SymPy.

WHAT IT ASSERTS
---------------
For every item in every family:
  - every non-final state names all nine moves, each exactly once: a move is either
    an edge (`go`) or a named reason (`why`), and every reason exists;
  - every line has the same solution set as the first line, on the item's domain
    (every log argument of the first line positive);
  - every edge obeys the law it is named after: take logs, power, product,
    quotient, log 10 = 1 / ln e = 1, undo the log, or rearrange (which may not
    change the set of logs present);
  - every final line is `x = <no x>`, and its value matches SymPy's own solution
    of the first line, and the game's answer key, to 1e-9;
  - no answer lies within 1e-6 of a 3 s.f. rounding boundary;
  - every misconception value differs from the answer at 3 s.f.;
  - F5: the rejected root really makes a log argument <= 0 and the kept one does
    not, and the offered roots are exactly the roots of the quadratic;
  - every family pool has >= 40 items and no repeated question;
  - no `\\log_` other than `\\log_{10}` appears in any Solve string;
  - every TeX string and every \\( \\) segment parses in KaTeX (when KaTeX loads:
    always in CI, where --require-katex makes a missing KaTeX a failure).

USAGE
-----
    python scripts/verify-log-laws.py                  # CI runs --require-katex
    python scripts/verify-log-laws.py --katex-dir DIR  # serve KaTeX from a local
                                                       # copy of its dist/ folder
                                                       # (sandboxes without the CDN)
"""
import argparse
import asyncio
import math
import os
import re
import sys
import time

import mpmath
import sympy as sp
from urllib.parse import urlsplit
from sympy import S

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc  # noqa: E402  (start_stub_server: checked start, free port)
SLUG = "log-laws"
PORT = None  # set by main() to the free port the stub server got
KATEX_PREFIX = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"
MIN_POOL = 40
TOL = 1e-9

lg = sp.Function("lg")
ln = sp.Function("ln")
X, T = sp.symbols("x t")
NS = {"x": X, "t": T, "lg": lg, "ln": ln, "E": sp.E}

_FAILURES = []
_MAX_PRINT = [60]


def fail(msg):
    _FAILURES.append(msg)
    if len(_FAILURES) <= _MAX_PRINT[0]:
        print("FAIL: " + msg)


# Every TeX string in the export, and every \( \) segment of every mixed string,
# rendered with throwOnError so a parse error is reported rather than drawn red.
KATEX_JS = r"""
() => {
  if (typeof katex === 'undefined') return null;
  const D = window.LL_SOLVE, bad = [];
  const segs = s => { const out = []; const re = /\\\(([\s\S]*?)\\\)/g; let m; while ((m = re.exec(s))) out.push(m[1]); return out; };
  const tryTex = (where, tx) => { try { katex.renderToString(tx, { throwOnError: true }); } catch (e) { bad.push(where + ': ' + String(e.message || e).slice(0, 160)); } };
  const tryMixed = (where, s) => segs(s).forEach(tx => tryTex(where, tx));
  D.moves.forEach(m => tryMixed('move ' + m.id, m.label));
  Object.keys(D.reasons).forEach(k => tryMixed('reason ' + k, D.reasons[k].t.replace(/\{v\}/g, 'x')));
  D.laws.forEach((l, i) => tryTex('law ' + i, l));
  D.families.forEach(f => {
    tryTex(f.id + ' eg', f.eg);
    f.items.forEach(it => {
      tryMixed(it.id + ' prompt', it.prompt);
      it.states.forEach((s, i) => {
        tryTex(it.id + ' state ' + i, s.tex);
        if (s.note) tryMixed(it.id + ' note ' + i, s.note);
        if (s.choose) { s.choose.options.forEach(o => tryTex(it.id + ' option', o.tex)); tryMixed(it.id + ' okMsg', s.choose.okMsg); }
      });
      it.mis.forEach(m => tryMixed(it.id + ' ' + m.id, m.msg));
    });
  });
  return bad;
}
"""


async def fetch(katex_dir):
    from playwright.async_api import async_playwright

    base = "http://127.0.0.1:%d" % PORT
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        async def route(r):
            u = r.request.url
            if katex_dir and u.startswith(KATEX_PREFIX):
                p = os.path.join(katex_dir, u[len(KATEX_PREFIX):].split("?")[0])
                if os.path.isfile(p):
                    return await r.fulfill(path=p)
            # Nothing a check needs leaves the machine except KaTeX itself.
            if u.startswith(base) or u.startswith(KATEX_PREFIX):
                return await r.continue_()
            return await r.abort()

        await page.route("**/*", route)
        await page.goto(base + "/games/" + SLUG + "/?cb=verify%d" % int(time.time()),
                        wait_until="load", timeout=30000)
        try:
            await page.wait_for_function("typeof katex !== 'undefined'", timeout=8000)
        except Exception:
            pass
        data = await page.evaluate(
            "() => window.LL_SOLVE ? JSON.parse(JSON.stringify(window.LL_SOLVE)) : null")
        katex_bad = await page.evaluate(KATEX_JS)
        await browser.close()
        return data, katex_bad, errors


# ── SymPy helpers ────────────────────────────────────────────────────────────

def parse(s):
    return sp.sympify(s, locals=NS)


def sem(e):
    """Give lg and ln their meaning: log base 10 and natural log."""
    return e.replace(lg, lambda a: sp.log(a, 10)).replace(ln, lambda a: sp.log(a))


def logs_in(e):
    return set(e.atoms(lg)) | set(e.atoms(ln))


def num(v):
    c = complex(sp.N(v, 30))
    return c.real if abs(c.imag) < 1e-12 else None


def in_domain(args, var, v):
    for a in args:
        try:
            val = num(sem(a).subs(var, v))
        except Exception:
            return False
        if val is None or val <= 0:
            return False
    return True


def solutions(lhs, rhs, var, dom_args):
    """Real solutions of lhs = rhs on the domain, as sorted floats."""
    f = sem(lhs) - sem(rhs)
    if var not in f.free_symbols:
        return None
    g = sp.expand_log(f, force=True)
    cands = []
    try:
        ss = sp.solveset(g, var, S.Reals)
        if isinstance(ss, sp.FiniteSet):
            cands = list(ss)
    except Exception:
        pass
    if not cands:
        try:
            cands = sp.solve(g, var)
        except Exception:
            cands = []
    out = []
    for c in cands:
        v = num(c)
        if v is None or not in_domain(dom_args, var, v):
            continue
        # Substitute the exact candidate, and judge the residual against the size
        # of the sides: 5^x = 6^(x-2) has its root near 19.6, where both sides are
        # about 1e13, so an absolute tolerance would reject a true root.
        try:
            res = complex(sp.N(f.subs(var, c), 40))
            scale = max(1.0, abs(complex(sp.N(sem(lhs).subs(var, c), 40))),
                        abs(complex(sp.N(sem(rhs).subs(var, c), 40))))
        except Exception:
            continue
        if abs(res) > 1e-12 * scale:
            continue
        if not any(abs(v - w) < 1e-9 * max(1.0, abs(v)) for w in out):
            out.append(v)
    return sorted(out)


def same_set(a, b):
    return a is not None and b is not None and len(a) == len(b) and all(
        abs(p - q) <= TOL * max(1.0, abs(p)) for p, q in zip(a, b))


def zero(e):
    d = sp.expand(e)
    return d == 0 or sp.simplify(d) == 0


def power_law(e):
    """F(b**p) -> p*F(b); F(exp(u)) -> u*F(E), for F in lg, ln."""
    def is_pow_log(n):
        return isinstance(n, (lg, ln)) and (n.args[0].is_Pow or isinstance(n.args[0], sp.exp))

    def apply(n):
        a = n.args[0]
        if isinstance(a, sp.exp):
            return a.args[0] * n.func(sp.E)
        return a.exp * n.func(a.base)
    return e.replace(is_pow_log, apply)


def special_one(e):
    """log 10 = 1 and ln e = 1, including their one-step forms ln(e^u) = u, log(10^u) = u."""
    def hit(n):
        if isinstance(n, ln):
            a = n.args[0]
            return a == sp.E or isinstance(a, sp.exp)
        if isinstance(n, lg):
            a = n.args[0]
            return a == 10 or (a.is_Pow and a.base == 10)
        return False

    def apply(n):
        a = n.args[0]
        if a == sp.E or a == 10:
            return sp.Integer(1)
        return a.args[0] if isinstance(a, sp.exp) else a.exp
    return e.replace(hit, apply)


def check_combine(A, B, law):
    """Product or quotient law, combining two logs into one on exactly one side."""
    (Al, Ar), (Bl, Br) = A, B
    sides = [(Al, Bl), (Ar, Br)]
    changed = [(a, b) for a, b in sides if not zero(a - b)]
    if len(changed) != 1:
        return "the %s law should change exactly one side" % law
    a, b = changed[0]
    removed = logs_in(a) - logs_in(b)
    added = logs_in(b) - logs_in(a)
    if len(removed) != 2 or len(added) != 1:
        return "the %s law should turn two logs into one (removed %s, added %s)" % (law, removed, added)
    r1, r2 = sorted(removed, key=str)
    new = list(added)[0]
    if not (r1.func == r2.func == new.func):
        return "the %s law mixed bases" % law
    u, v, w = r1.args[0], r2.args[0], new.args[0]
    if law == "product":
        ok = zero(w - u * v)
    else:
        ok = zero(w - u / v) or zero(w - v / u)
    if not ok:
        return "the new log's argument %s is not the %s of %s and %s" % (w, law, u, v)
    if not zero(sp.expand_log(sem(a) - sem(b), force=True)):
        return "the %s law changed the value of a side" % law
    return None


def check_edge(move, A, B, var):
    (Al, Ar), (Bl, Br) = A, B
    if move in ("log", "ln"):
        F = lg if move == "log" else ln
        if not (zero(Bl - F(Al)) and zero(Br - F(Ar))):
            return "taking %s should give %s(lhs) = %s(rhs)" % (move, F, F)
        return None
    if move == "power":
        if not any(n.args[0].is_Pow or isinstance(n.args[0], sp.exp) for n in logs_in(Al) | logs_in(Ar)):
            return "the power law needs the log of a power"
        if not (zero(power_law(Al) - Bl) and zero(power_law(Ar) - Br)):
            return "the power law result does not match"
        return None
    if move in ("product", "quotient"):
        return check_combine(A, B, move)
    if move == "sp1":
        fwd = zero(special_one(Al) - Bl) and zero(special_one(Ar) - Br) and not (zero(Al - Bl) and zero(Ar - Br))
        rev = zero(special_one(Bl) - Al) and zero(special_one(Br) - Ar) and not (zero(Al - Bl) and zero(Ar - Br))
        return None if (fwd or rev) else "log 10 = 1 / ln e = 1 does not account for this line"
    if move == "undo":
        if not isinstance(Al, (lg, ln)):
            return "undo needs a single log on the left"
        F = Al.func
        if isinstance(Ar, F):
            ok = zero(Bl - Al.args[0]) and zero(Br - Ar.args[0])
        elif Ar.is_number:
            ok = zero(Bl - Al.args[0]) and zero(Br - (10 ** Ar if F is lg else sp.exp(Ar)))
        else:
            return "undo needs a single log, or a number, on the right"
        return None if ok else "undo should equate the insides of the logs"
    if move == "rearrange":
        if logs_in(Al) | logs_in(Ar) != logs_in(Bl) | logs_in(Br):
            return "rearranging changed which logs are present"
        return None
    return "unknown move " + move


def boundary_distance(expr):
    """Distance from |value| to the nearest 3 s.f. rounding boundary, at 50 digits."""
    mpmath.mp.dps = 50
    v = abs(mpmath.mpf(str(sp.N(expr, 50))))
    e = int(mpmath.floor(mpmath.log10(v)))
    if mpmath.power(10, e + 1) <= v:
        e += 1
    if mpmath.power(10, e) > v:
        e -= 1
    q = mpmath.power(10, e - 2)
    f = v / q
    return float(abs(f - mpmath.floor(f) - mpmath.mpf("0.5")) * q)


def r3(v):
    return float("%.3g" % v)


# ── Per-item checks ──────────────────────────────────────────────────────────

def verify_item(it, move_ids, reasons):
    iid = it["id"]
    var = T if it["v"] == "t" else X
    states = it["states"]
    parsed = {}
    for i, s in enumerate(states):
        if s["kind"] == "choose":
            continue
        try:
            parsed[i] = (parse(s["lhs"]), parse(s["rhs"]))
        except Exception as e:
            fail("%s state %d does not parse: %s" % (iid, i, e))
            return
    dom_args = [n.args[0] for n in logs_in(parsed[0][0]) | logs_in(parsed[0][1]) if var in n.args[0].free_symbols]

    # Coverage: all nine moves, each exactly once, every reason real.
    for i, s in enumerate(states):
        if s["kind"] in ("final", "choose"):
            continue
        g = set((it["go"].get(str(i)) or {}).keys())
        w = it["why"].get(str(i)) or {}
        if g & set(w):
            fail("%s state %d: a move is both an edge and a reason: %s" % (iid, i, g & set(w)))
        if g | set(w) != set(move_ids):
            fail("%s state %d does not cover all nine moves (missing %s)" % (iid, i, set(move_ids) - (g | set(w))))
        for m, rid in w.items():
            if rid not in reasons:
                fail("%s state %d: move %s names unknown reason %s" % (iid, i, m, rid))

    # The root(s) of the first line, on the domain.
    expected = solutions(parsed[0][0], parsed[0][1], var, dom_args)
    if not expected:
        fail("%s: SymPy finds no solution to the first line" % iid)
        return
    if len(expected) != 1:
        fail("%s: the first line has %d solutions on its domain, expected 1" % (iid, len(expected)))
        return
    root = expected[0]

    # Every line: same solution set on the domain.
    for i, (l, r) in parsed.items():
        got = solutions(l, r, var, dom_args)
        if not same_set(got, expected):
            fail("%s state %d (%s = %s): solutions %s, expected %s" % (iid, i, l, r, got, expected))

    # Every edge obeys its law.
    for i_s, edges in it["go"].items():
        i = int(i_s)
        for move, j in edges.items():
            if states[j]["kind"] == "choose":
                continue
            err = check_edge(move, parsed[i], parsed[j], var)
            if err:
                fail("%s: %d -[%s]-> %d: %s" % (iid, i, move, j, err))

    # Final lines: x = <no x>, value = root = the game's key.
    finals = [i for i, s in enumerate(states) if s["kind"] == "final"]
    for i in finals:
        l, r = parsed[i]
        if l != var or var in r.free_symbols:
            fail("%s state %d is final but is not %s = <number>" % (iid, i, var))
            continue
        v = num(sem(r))
        if v is None or abs(v - root) > TOL * max(1.0, abs(root)):
            fail("%s state %d evaluates to %s, SymPy's root is %s" % (iid, i, v, root))
        if abs(it["answer"] - root) > TOL * max(1.0, abs(root)):
            fail("%s: the game's answer %s does not match SymPy's %s" % (iid, it["answer"], root))
        if boundary_distance(sem(r)) < 1e-6:
            fail("%s: the answer is within 1e-6 of a 3 s.f. rounding boundary" % iid)

    # F5: the choice of root.
    chooses = [i for i, s in enumerate(states) if s["kind"] == "choose"]
    for i in chooses:
        ch = states[i]["choose"]
        prev = [int(a) for a, e in it["go"].items() if i in e.values()]
        for p in prev:
            l, r = parsed[p]
            quad = sorted(num(c) for c in sp.solve(sem(l) - sem(r), var))
            if not same_set(quad, sorted(float(v) for v in ch["roots"])):
                fail("%s: offered roots %s are not the roots %s of the line before" % (iid, ch["roots"], quad))
        if abs(ch["keep"] - root) > TOL:
            fail("%s: kept root %s is not the solution %s" % (iid, ch["keep"], root))
        if not in_domain(dom_args, var, ch["keep"]):
            fail("%s: the kept root %s makes a log argument <= 0" % (iid, ch["keep"]))
        if in_domain(dom_args, var, ch["reject"]):
            fail("%s: the rejected root %s does not make any log argument <= 0" % (iid, ch["reject"]))
        if abs(it["answer"] - root) > TOL:
            fail("%s: the game's answer %s is not the kept root" % (iid, it["answer"]))
    if not finals and not chooses:
        fail("%s has no final state" % iid)

    # Misconceptions differ from the answer at 3 s.f.
    for m in it["mis"]:
        if r3(m["v"]) == r3(it["answer"]):
            fail("%s: misconception %s gives the answer itself (%s)" % (iid, m["id"], m["v"]))


def strings(data):
    out = [m["label"] for m in data["moves"]]
    out += [r["t"] for r in data["reasons"].values()]
    out += data["laws"]
    for f in data["families"]:
        out.append(f["eg"])
        for it in f["items"]:
            out.append(it["prompt"])
            for s in it["states"]:
                out += [s["tex"], s.get("note") or ""]
                if s.get("choose"):
                    out += [o["tex"] for o in s["choose"]["options"]] + [s["choose"]["okMsg"]]
            out += [m["msg"] for m in it["mis"]]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-katex", action="store_true",
                    help="fail if KaTeX does not load (CI, where the CDN is reachable)")
    ap.add_argument("--katex-dir", help="serve KaTeX 0.16.9 from this local dist/ folder")
    ap.add_argument("--max-print", type=int, default=60, help="print at most this many failures")
    args = ap.parse_args()
    _MAX_PRINT[0] = args.max_print

    global PORT
    # A free port chosen per run; raises bc.StubServerError, naming the cause, if the
    # stub server cannot start.
    server, base = bc.start_stub_server()
    PORT = urlsplit(base).port
    try:
        data, katex_bad, page_errors = asyncio.run(fetch(args.katex_dir))
    finally:
        server.terminate()

    if not data:
        print("FAIL: could not read window.LL_SOLVE from the live page")
        return 1
    for e in page_errors:
        fail("page error: " + e)

    move_ids = [m["id"] for m in data["moves"]]
    if len(move_ids) != 9:
        fail("expected nine moves, found %d" % len(move_ids))
    reasons = data["reasons"]

    for f in data["families"]:
        items = f["items"]
        print("Verifying %s (stage %d, %d items, %d filtered at a rounding boundary)..."
              % (f["id"], f["stage"], len(items), f["filtered"]))
        if len(items) < MIN_POOL:
            fail("%s has %d items, below the floor of %d" % (f["id"], len(items), MIN_POOL))
        if max(data["lengths"]) > len(items):
            fail("%s cannot fill a %d-question session" % (f["id"], max(data["lengths"])))
        firsts = [it["states"][0]["tex"] for it in items]
        if len(set(firsts)) != len(firsts):
            fail("%s repeats a question" % f["id"])
        ids = [it["id"] for it in items]
        if len(set(ids)) != len(ids):
            fail("%s repeats an item id" % f["id"])
        for it in items:
            verify_item(it, move_ids, reasons)

    for s in strings(data):
        for m in re.finditer(r"\\log_(\{[^}]*\}|.)", s):
            if m.group(1) != "{10}":
                fail("a Solve string uses another log base: %r" % s[:80])

    if katex_bad is None:
        if args.require_katex:
            fail("KaTeX did not load, so no TeX string could be checked")
        else:
            print("SKIP: KaTeX did not load; TeX strings not parse-checked (CI runs --require-katex)")
    else:
        for b in katex_bad:
            fail("KaTeX: " + b)
        if not katex_bad:
            print("KaTeX: every Solve string parses.")

    print()
    if _FAILURES:
        print("%d FAILURE(S)" % len(_FAILURES))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
