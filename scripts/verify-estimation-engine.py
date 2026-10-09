#!/usr/bin/env python3
# ci-line: Estimation Engine (SR-12: every rounding and estimate recomputed; marked by exact match in Chromium; phone keypad fit) |
"""Estimation Engine (GCSE N14, canon SR-12): every method answer recomputed from the stored numbers.

The game asks: round each number to 1 significant figure, then estimate. It marks both steps by exact
match (MaffsAnswer), so the bank's roundings and estimates ARE the marking, and this script is what
computes them independently. It reads the bank literal from the page (between BANK-START and BANK-END)
and, for every item:

  - each stored number appears, in order, in what the student reads (the KaTeX string, or the word
    problem with thousands commas read as digits);
  - its 1 s.f. rounding, recomputed with Decimal (half up), equals the stored one; a number that is an
    exact half at 1 s.f. (25, 0.35) FAILS: SR-12 would need both roundings accepted, and this bank has
    none by design;
  - the estimate, recomputed exactly (SymPy, rationals) from the correct roundings through the item's
    expression shape, equals the stored estimate, and is a whole or terminating number a student can
    write;
  - the exact value, recomputed from the original numbers, rounds (half up, at the stored precision)
    to the stored one, which is shown as the calculator answer; money items are pence;
  - ids are unique and each item's group is its id's letter.

And for the bank: every group A-F has at least 5 items, 45 in all. Then, unless --static, it plays the
page in Chromium (stub server): on D01 the rounding step accepts 20, 4, 0.5 and the estimate accepts
160 and rejects 173; a wrong rounding still lets 160 earn the estimate mark; F02 accepts 10 for 9.8
and rejects 9; a full 10-question game draws every group, shows no timer and scores out of 20.

Self-test (--selftest, also run by default first): a wrong rounding, a wrong estimate and an exact-half
number are planted in a copy of the bank; each must fail.

    python scripts/verify-estimation-engine.py             # self-test, bank, then the page in Chromium
    python scripts/verify-estimation-engine.py --static    # self-test and bank only (no browser)
"""
import argparse
import json
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "games", "estimation-engine", "index.html")
SLUG = "estimation-engine"
GROUPS = "ABCDEF"
MIN_PER_GROUP, MIN_TOTAL = 5, 45


def read_bank(path=PAGE):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"/\* BANK-START \*/\s*(?:var|const|let)?\s*[\w.]*\s*=?\s*(\[.*?\])\s*;?\s*/\* BANK-END \*/", src, re.S)
    if not m:
        raise SystemExit("verify-estimation-engine: no bank between /* BANK-START */ and /* BANK-END */ in %s" % path)
    return json.loads(m.group(1))


def round_1sf(s):
    """(rounded Decimal, is_exact_half) for a number written as a string."""
    x = Decimal(s)
    if x == 0:
        return Decimal(0), False
    q = Decimal(1).scaleb(x.adjusted())
    lead = x / q                                   # 1 <= |lead| < 10
    r = lead.quantize(Decimal(1), rounding=ROUND_HALF_UP) * q
    half = (abs(lead) - int(abs(lead))) == Decimal("0.5")
    return r, half


def fmt(d):
    return format(Decimal(d).normalize(), "f")


def same(a, b):
    return Decimal(a) == Decimal(b)


def evaluate(shape, values):
    names = sp.symbols("a b c d")
    expr = sp.sympify(shape, locals={"sqrt": sp.sqrt, "a": names[0], "b": names[1], "c": names[2], "d": names[3]})
    used = sorted(str(s) for s in expr.free_symbols)
    want = ["a", "b", "c", "d"][:len(values)]
    if used != want:
        raise ValueError("shape %r uses %s, but the item has %d numbers" % (shape, used, len(values)))
    return sp.nsimplify(expr.subs({names[i]: sp.Rational(v) for i, v in enumerate(values)}))


def terminating(v):
    """A rational whose decimal ends (denominator 2^a 5^b)."""
    if not v.is_Rational:
        return False
    d = int(v.q)
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def dec(v, places=12):
    return Decimal(str(sp.N(v, 30))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def sig_figs(s):
    return len(s.replace(".", "").lstrip("0"))


def pct_off(estimate, calc):
    """Whole percents, half up: 100 |estimate - calc| / calc (Jon, 5 Oct 2026)."""
    e, c = Decimal(estimate), Decimal(calc)
    return int((abs(e - c) * 100 / c).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def calc_line(it):
    """The words the page must show under every answer (Jon, 5 Oct 2026, answers 1 and 2)."""
    if it.get("money"):
        line = "Calculator answer: \u00a3" + it["exact"] + (" (to the nearest penny)" if it.get("approx") else "")
    elif it.get("approx"):
        line = "Calculator answer: %s (to %d s.f.)" % (it["exact"], sig_figs(it["exact"]))
    else:
        line = "Calculator answer: " + fmt(it["exact"])
    n = pct_off(it["estimate"], it["exact"])
    return line, "The estimate is %s off the calculator answer. That\u2019s what estimates are for." % (
        "less than 1%" if n < 1 else "%d%%" % n)


def shown_numbers(item):
    """The numbers in what the student reads, in order."""
    text = item.get("tex") or item.get("text") or ""
    text = re.sub(r"(?<=\d),(?=\d{3}\b)", "", text)          # £4,180 -> 4180
    text = re.sub(r"\^2|²", " ", text)                       # the square is an operation, not a number
    return re.findall(r"\d+(?:\.\d+)?", text)


def check_bank(bank):
    fails = []
    ids = [it.get("id") for it in bank]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        fails.append("%s: id used twice" % d)
    for it in bank:
        iid = it.get("id", "?")
        try:
            if it.get("group") != iid[:1] or it["group"] not in GROUPS:
                fails.append("%s: group %r is not the id's letter (A-F)" % (iid, it.get("group")))
            nums, rounded = it["nums"], it["rounded"]
            if len(rounded) != len(nums):
                fails.append("%s: %d numbers but %d roundings" % (iid, len(nums), len(rounded)))
                continue
            if shown_numbers(it) != nums:
                fails.append("%s: the student reads the numbers %s, the bank stores %s" % (iid, shown_numbers(it), nums))
            for n, r in zip(nums, rounded):
                want, half = round_1sf(n)
                if half:
                    fails.append("%s: %s is an exact half at 1 s.f. (SR-12 would need two answers)" % (iid, n))
                if not same(r, want):
                    fails.append("%s: %s to 1 s.f. is %s, the bank says %s" % (iid, n, fmt(want), r))
            est = evaluate(it["shape"], [str(round_1sf(n)[0]) for n in nums])
            if not terminating(est):
                fails.append("%s: the method estimate %s is not a terminating decimal" % (iid, est))
            elif not same(it["estimate"], dec(est)):
                fails.append("%s: %s on the 1 s.f. numbers is %s, the bank says %s"
                             % (iid, it["shape"], fmt(dec(est)), it["estimate"]))
            exact = evaluate(it["shape"], nums)
            places = len(it["exact"].split(".")[1]) if "." in it["exact"] else 0
            got = dec(exact).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
            if not same(it["exact"], got):
                fails.append("%s: the exact value %s rounds to %s at %d d.p., the bank says %s"
                             % (iid, fmt(dec(exact)), got, places, it["exact"]))
            if it.get("money") and (places != 2 or "." in it["estimate"]):
                fails.append("%s: a money item needs pence in its exact value and whole pounds in its estimate" % iid)
            is_exact = sp.Rational(it["exact"]) == exact
            if bool(it.get("approx")) == is_exact:
                fails.append("%s: approx is %s, but the calculator answer %s is %s" % (
                    iid, bool(it.get("approx")), it["exact"], "exact" if is_exact else "rounded"))
            if it.get("approx") and not it.get("money") and sig_figs(it["exact"]) != 4:
                fails.append("%s: a rounded calculator answer is shown to 4 s.f. (Jon, 5 Oct 2026); %s is %d"
                             % (iid, it["exact"], sig_figs(it["exact"])))
            if pct_off(it["estimate"], it["exact"]) != pct_off(it["estimate"], dec(exact, 20)):
                fails.append("%s: the %% off differs between the shown calculator answer and the exact value "
                             "(a rounding boundary): reword or re-pick the item" % iid)
        except Exception as exc:                     # a malformed item is a failure, never a crash
            fails.append("%s: could not be checked: %s" % (iid, exc))
    for g in GROUPS:
        n = sum(1 for it in bank if it.get("group") == g)
        if n < MIN_PER_GROUP:
            fails.append("group %s has %d items (at least %d)" % (g, n, MIN_PER_GROUP))
    if len(bank) < MIN_TOTAL:
        fails.append("the bank has %d items (at least %d)" % (len(bank), MIN_TOTAL))
    return fails


def selftest(bank):
    """Each planted fault must fail; the clean bank must pass."""
    def plant(fn):
        b = json.loads(json.dumps(bank))
        fn({it["id"]: it for it in b})
        return b

    def wrong_rounding(by):
        by["A07"]["rounded"][0] = "10"               # 9.2 to 1 s.f. is 9

    def wrong_estimate(by):
        by["D01"]["estimate"] = "170"                 # 20 x 4 / 0.5 is 160

    def exact_half(by):
        it = by["A01"]                                # 48 x 21 -> 45 x 21: 45 is a half at 1 s.f.
        it["nums"][0], it["tex"], it["exact"] = "45", "45 \\times 21", "945"
    cases = [("a wrong rounding (A07: 9.2 -> 10)", wrong_rounding),
             ("a wrong estimate (D01: 170)", wrong_estimate),
             ("an exact-half number (A01: 45)", exact_half)]
    out = []
    if check_bank(bank):
        out.append("self-test: the clean bank does not pass")
    for name, fn in cases:
        caught = check_bank(plant(fn))
        print("  planted %-36s %s" % (name, ("CAUGHT (%s)" % caught[0]) if caught else "*** MISSED ***"))
        if not caught:
            out.append("self-test: planted %s was NOT caught" % name)
    return out


# ---------------------------------------------------------------- the page in Chromium
PHONES = [(320, 568), (375, 667), (390, 844)]
# The step's boxes (top) to the bottom of Check and the keypad, against the window less the fixed footer.
FIT_JS = """() => { const R = s => { const e = document.querySelector(s); return e && e.offsetParent !== null ? e.getBoundingClientRect() : null; };
  const head = R('#stepHead'), kp = R('.maffs-keypad-panel'), chk = R('#checkBtn'), ae = document.activeElement;
  return { top: head ? head.top : -1, bottom: Math.max(kp ? kp.bottom : 1e9, chk ? chk.bottom : 1e9), fold: innerHeight - 40,
    focused: !!ae && ae.tagName === 'INPUT', calc: !!document.querySelector('.maffs-calc, script[src*="calculator.js"]'),
    sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }; }"""


# Every item at 320px, both steps answered: the question, the step 2 line and the working never make the
# page scroll sideways, and where KaTeX loaded each of them is KaTeX (never the plain-text fallback).
ALL_JS = """() => { const has = s => { const e = document.querySelector(s); return !!e && !!e.querySelector('.katex'); };
  return { sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, katex: !!window.katex,
    question: has('#question'), head: has('#stepHead'), work: has('.fb-work'), words: !!EE.ui.item().text }; }"""


def play(fails, shots=None, katex_dir=None):
    import asyncio
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import bank_common as bc

    async def run(base):
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            ctx = await browser.new_context(viewport={"width": 390, "height": 844})
            await bc.no_next_floor(ctx)
            await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)  # MaffsLock's 300 ms window: the sweep answers at once (F1 batch 7)

            async def route(r):
                u = r.request.url
                if katex_dir and u.startswith("https://cdn.jsdelivr.net/npm/katex"):
                    f = os.path.join(katex_dir, u.split("/dist/", 1)[1].split("?")[0])
                    await (r.fulfill(path=f) if os.path.exists(f) else r.abort())
                elif u.startswith(base) or u.startswith("https://cdn.jsdelivr.net/npm/katex"):
                    await r.continue_()
                else:
                    await r.abort()
            await ctx.route("**/*", route)
            page = await ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            await page.goto(base + "/games/%s/" % SLUG, wait_until="load")
            await page.wait_for_function("!!window.EE && !!window.EE.ui")
            await page.evaluate("""() => { window.__events = []; window.__submits = [];
              window.mfg = function (n, p) { window.__events.push([n, p]); };
              if (window.MaffsLeaderboard) MaffsLeaderboard.submitScore = function (s, l, sc, n) {
                window.__submits.push([s, l, sc, n]); return Promise.resolve({}); }; }""")

            async def answer_rounding(vals):
                await page.evaluate("v => EE.ui.typeRounding(v)", vals)
                await page.click("#checkBtn")
                return await page.evaluate("EE.ui.state()")

            async def answer_estimate(v):
                await page.evaluate("v => EE.ui.typeEstimate(v)", v)
                await page.click("#checkBtn")
                return await page.evaluate("EE.ui.state()")

            # Every item's calculator line and percentage, as the page builds them.
            for it in bank:
                got = await page.evaluate("id => { const q = EE.BANK.filter(x => x.id === id)[0]; return [EE.calcLine(q), EE.percentLine(q)]; }", it["id"])
                if list(got) != list(calc_line(it)):
                    fails.append("page, %s: shows %r, expected %r" % (it["id"], got, calc_line(it)))
            # D01: 20, 4, 0.5 then 160 (both marks); then wrong rounding, 160 (one mark); 173 rejected.
            for label, rnd, est, want in [("D01 right, 160", ["20", "4", "0.5"], "160", [True, True]),
                                          ("D01 wrong rounding, 160", ["20", "4", "0.4"], "160", [False, True]),
                                          ("D01 right, 173", ["20", "4", "0.5"], "173", [True, False])]:
                await page.evaluate("EE.ui.startWith(['D01'])")
                await answer_rounding(rnd)
                shown = await page.evaluate("EE.ui.roundedShown()")
                if shown != ["20", "4", "0.5"]:
                    fails.append("page, %s: after the rounding step the correct roundings shown are %r" % (label, shown))
                await answer_estimate(est)
                got = await page.evaluate("EE.ui.marks()")
                if got != want:
                    fails.append("page, %s: marks %r, expected %r" % (label, got, want))
            # F02: 10 for 9.8 accepted, 9 rejected
            for vals, want in [(["300", "10"], True), (["300", "9"], False)]:
                await page.evaluate("EE.ui.startWith(['F02'])")
                await answer_rounding(vals)
                if (await page.evaluate("EE.ui.marks()"))[0] != want:
                    fails.append("page, F02: roundings %r marked %s, expected %s" % (vals, not want, want))
            # A full game: 10 questions, every group, no timer, Next after every question, out of 20.
            await page.evaluate("EE.ui.restart()")
            await page.click("#startBtn")
            seen, nexts = set(), 0
            for i in range(10):
                it = await page.evaluate("EE.ui.item()")
                seen.add(it["group"])
                await answer_rounding(it["rounded"])
                await answer_estimate(it["estimate"])
                if await page.locator(".maffs-next").count() == 0:
                    fails.append("page: no Next control after question %d" % (i + 1))
                else:
                    nexts += 1
                    await page.click(".maffs-next")
            if seen != set(GROUPS):
                fails.append("page: a full game drew groups %s, not all of A-F" % "".join(sorted(seen)))
            st = await page.evaluate("[EE.ui.state(), EE.ui.score(), !!document.querySelector('.timer, #timer')]")
            if st[0] != "done" or st[1] != 20 or st[2]:
                fails.append("page: after 10 right answers state %r, score %r (want 20), timer on page %s" % tuple(st))
            subs = await page.evaluate("window.__submits")
            if subs != [[SLUG, "gcse", 20, 10]]:
                fails.append("page: leaderboard submissions %r, expected one to gcse with 20" % subs)
            lv = {p.get("level") for n, p in await page.evaluate("window.__events")}
            if lv != {"gcse"}:
                fails.append("page: analytics levels %r, expected only 'gcse'" % lv)
            for e in errors:
                fails.append("page error: %s" % e)
            await ctx.close()
            # Phones: the keypad types into every box, no calculator anywhere, no sideways scroll, and each
            # step's boxes, Check and keypad are in the window together (D07 has four numbers, F01 is money).
            for (w, h), aa in [(p, False) for p in PHONES] + [(p, True) for p in PHONES]:
                ctx = await browser.new_context(viewport={"width": w, "height": h}, has_touch=True, is_mobile=True)
                await bc.no_next_floor(ctx)
                await ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)  # MaffsLock's 300 ms window: the sweep answers at once (F1 batch 7)
                if aa:      # the Aa (dyslexia-friendly) mode, which every phone fit is also measured in (canon §7.5.1)
                    await ctx.add_init_script("try { localStorage.setItem('mfg_accessible', 'true'); } catch (e) {}")
                await ctx.route("**/*", route)
                page = await ctx.new_page()
                await page.goto(base + "/games/%s/" % SLUG, wait_until="load")
                await page.wait_for_function("!!window.EE && !!window.EE.ui")
                for iid in ("D07", "F01", "E01"):
                    it = next(x for x in bank if x["id"] == iid)
                    await page.evaluate("id => EE.ui.startWith([id])", iid)
                    for step, vals in (("round", it["rounded"]), ("estimate", [it["estimate"]])):
                        boxes = page.locator("#stepBody input")
                        n = await boxes.count()
                        if n != len(vals):
                            fails.append("%dx%d%s %s %s: %d boxes, expected %d" % (w, h, " Aa" * aa, iid, step, n, len(vals)))
                            break
                        for i, v in enumerate(vals):
                            await boxes.nth(i).tap()
                            for ch in v:
                                await page.locator('.maffs-keypad-key[data-val="%s"]' % ch).tap()
                        m = await page.evaluate(FIT_JS)
                        got = await page.evaluate("[...document.querySelectorAll('#stepBody input')].map(i => i.value)")
                        if got != vals:
                            fails.append("%dx%d%s %s %s: the keypad typed %r, expected %r" % (w, h, " Aa" * aa, iid, step, got, vals))
                        if m["focused"]:
                            fails.append("%dx%d%s %s %s: a box took focus (the system keyboard would open)" % (w, h, " Aa" * aa, iid, step))
                        if m["calc"]:
                            fails.append("%dx%d%s %s: the calculator is on the page" % (w, h, " Aa" * aa, iid))
                        if m["sw"] > m["cw"]:
                            fails.append("%dx%d%s %s %s: the page is %dpx wide" % (w, h, " Aa" * aa, iid, step, m["sw"]))
                        if m["top"] < 0 or m["bottom"] > m["fold"]:
                            fails.append("%dx%d%s %s %s: the boxes, Check and keypad span y=%.0f..%.0f, the window ends at %.0f"
                                         % (w, h, " Aa" * aa, iid, step, m["top"], m["bottom"], m["fold"]))
                        await page.locator("#checkBtn").tap()
                    if await page.evaluate("[...document.querySelectorAll('.maffs-keypad-cue-answer')].some(c => !c.hidden)"):
                        fails.append("%dx%d%s %s: after the answer a box still says \"typing here\"" % (w, h, " Aa" * aa, iid))
                    if await page.evaluate("EE.ui.marks()") != [True, True]:
                        fails.append("%dx%d%s %s: typed on the keypad, the right answers were not both marked" % (w, h, " Aa" * aa, iid))
                    nb = await page.evaluate("(() => { const b = document.querySelector('.maffs-next'); if (!b) return null; "
                                             "const r = b.getBoundingClientRect(), f = document.getElementById('feedback').getBoundingClientRect(); "
                                             "return [r.bottom, innerHeight - 40, f.top]; })()")
                    if nb is None or nb[0] > nb[1] or nb[2] < 0:
                        fails.append("%dx%d%s %s: the feedback and Next are not all between the top of the window and the footer (Next bottom, fold, feedback top: %r)" % (w, h, " Aa" * aa, iid, nb))
                if w == 320 and not aa:
                    for it in bank:
                        await page.evaluate("id => EE.ui.startWith([id])", it["id"])
                        await page.evaluate("v => EE.ui.typeRounding(v)", it["rounded"])
                        await page.locator("#checkBtn").tap()
                        await page.evaluate("v => EE.ui.typeEstimate(v)", it["estimate"])
                        await page.locator("#checkBtn").tap()
                        a = await page.evaluate(ALL_JS)
                        if a["sw"] > a["cw"]:
                            fails.append("320x568 %s: the page is %dpx wide after both steps" % (it["id"], a["sw"]))
                        if a["katex"] and not (a["head"] and a["work"] and (a["words"] or a["question"])):
                            fails.append("320x568 %s: KaTeX loaded but the plain-text fallback shows (question %s, step 2 %s, "
                                         "working %s)" % (it["id"], a["question"], a["head"], a["work"]))
                    katex_seen.append(a["katex"])
                if shots:
                    await page.evaluate("EE.ui.startWith(['D07'])")
                    await page.locator("#stepBody input").nth(1).tap()
                    await page.screenshot(path=os.path.join(shots, "ee-%dx%d%s-step1.png" % (w, h, "-aa" * aa)))
                await ctx.close()
            await browser.close()
            return nexts

    bank = read_bank()
    katex_seen = []
    server, base = bc.start_stub_server()
    try:
        nexts = asyncio.run(run(base))
    finally:
        server.terminate()
    if katex_seen and not katex_seen[-1]:
        print("NOTE: KaTeX did not load (CDN unreachable): the plain-text fallback was measured; CI loads KaTeX")
    return nexts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--static", action="store_true", help="the bank only, no browser")
    ap.add_argument("--selftest", action="store_true", help="the self-test only")
    ap.add_argument("--shots", help="save phone screenshots of step 1 (D07) here")
    ap.add_argument("--katex-dir", help="serve KaTeX from this copy of its dist/ folder (a sandbox where the CDN is blocked)")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    bank = read_bank()
    fails = selftest(bank)
    if not args.selftest:
        fails += check_bank(bank)
        if not args.static and not fails:
            if args.shots:
                os.makedirs(args.shots, exist_ok=True)
            play(fails, args.shots, args.katex_dir)
    for f in fails:
        print("FAIL    " + f)
    if fails:
        print("\nFAILED: %d problem(s)" % len(fails))
        return 1
    counts = ", ".join("%s %d" % (g, sum(1 for it in bank if it["group"] == g)) for g in GROUPS)
    print("PASS: %d items (%s); every 1 s.f. rounding (Decimal, half up), estimate (SymPy, exact) and calculator "
          "answer recomputed from the stored numbers; no exact halves; 3 planted faults caught%s"
          % (len(bank), counts, "" if args.static or args.selftest else
             "; in Chromium D01 and F02 marked as the contract states, a full game draws A-F, no timer, 20 out of 20"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
