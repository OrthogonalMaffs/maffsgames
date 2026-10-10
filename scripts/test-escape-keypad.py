#!/usr/bin/env python3
# ci-line: Escape-room keypad, up to N digits (engine.js maxDigits on a fixture lock: 5,4,Set opens, 5,4,0,0,Set is the named misconception, no empty slots; a fixed keypad unchanged; the old fixed-length rule planted and caught) |
# ci-deps: escape-rooms/assets/engine.js escape-rooms/kiln-disaster/room.js scripts/check-teacher-invite.py
"""Browser test for the escape-room keypad's "up to N digits, Set to submit" mode (contract KEYPAD-VARIABLE,
10 Oct 2026).

    python scripts/test-escape-keypad.py               # the fixture, the fixed keypad, then the plant
    python scripts/test-escape-keypad.py --no-plants   # without the plant

A keypad with `maxDigits: N` (instead of `digits: N`) shows only the digits typed so far, Set submits 1 to N
of them (Set with nothing typed does nothing), and a leading zero is never kept; the typed fallback follows
the same rule. A keypad with `digits` behaves exactly as before.

  fixture  kiln-disaster's keypad lock rewritten in the page (no room file is edited) to maxDigits 4, answer 54,
           misconception 5400:
             5,4,Set opens the lock; the display reads "54" with no empty slot at every step
             5,4,0,0,Set raises the lock's named misconception response, display "5400"
             Set with nothing typed: no feedback, no time lost
             0,5,4 displays "54" (no leading zero); 5,4,0,0,9 stops at "5400"
             the typed fallback: "0054" becomes "54", "12345" becomes "1234", and Set then opens on "54"
  fixed    kiln-disaster's own two-digit keypad, unchanged: two empty slots to begin with; 5 then Set says
           "Not enough digits." and costs nothing
  plant    the fixture against the old fixed-length rule (maxDigits read as digits): it must FAIL
"""
import argparse
import asyncio
import importlib.util
import os
import pathlib
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = pathlib.Path(HERE).parent
_spec = importlib.util.spec_from_file_location("teacher_invite", os.path.join(HERE, "check-teacher-invite.py"))
ti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ti)

ENGINE = ROOT / "escape-rooms" / "assets" / "engine.js"
ROOM = "kiln-disaster"
LOCK = "kiln-sensor-limit"

# Rewrites the fixture lock as window.ROOM is assigned, before the engine reads it.
FIXTURE = """(() => {
  let r;
  Object.defineProperty(window, 'ROOM', { configurable: true, get: () => r, set: (v) => {
    const l = v.locks.find(x => x.id === '%s');
    l.instrument = { kind: 'keypad', label: 'FIXTURE: UP TO FOUR DIGITS', maxDigits: 4, verb: 'Enter code' };
    l.variants = l.variants.map(x => Object.assign({}, x, { answer: 54, miss: 5400 }));
    r = v;
  }});
})()""" % LOCK
STATE = """() => ({
  disp: document.getElementById('codeDisp') ? document.getElementById('codeDisp').textContent : null,
  blanks: document.querySelectorAll('#codeDisp .blank').length,
  fb: (document.querySelector('#fb.show') || {}).className || '',
  fbText: (document.querySelector('#fb.show') || {}).textContent || '',
  open: !document.getElementById('setBtn') && !!document.querySelector('.feedback.good.show'),
  clock: (document.getElementById('clock') || {}).textContent || ''
})"""


def plant(src):
    """The engine before KEYPAD-VARIABLE: a maxDigits keypad is read as a fixed-length one."""
    old = "var R = window.ROOM;"
    assert old in src, "plant: the ROOM line was not found"
    return src.replace(old, old + " R.locks.forEach(function (l) { var i = l.instrument;"
                       " if (i.maxDigits) { i.digits = i.maxDigits; delete i.maxDigits; } });", 1)


async def scenario(browser, base, engine_js, fixture, steps):
    """steps: list of ('key', k) | ('type', s) | ('set',) | ('look', name). Returns {name: state}."""
    ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
    try:
        await ctx.route(lambda u: not u.startswith(base), lambda r: r.abort())
        if engine_js is not None:
            await ctx.route(re.compile(r"/escape-rooms/assets/engine\.js(\?.*)?$"), lambda r: r.fulfill(
                status=200, content_type="application/javascript; charset=utf-8", body=engine_js))
        if fixture:
            await ctx.add_init_script(FIXTURE)
        page = await ctx.new_page()
        await page.goto(base + "/escape-rooms/%s/" % ROOM, wait_until="load", timeout=20000)
        await page.click("#startBtn")
        i = await page.evaluate("(id) => window.ROOM.locks.findIndex(l => l.id === id)", LOCK)
        await page.click('[data-lock="%d"]' % i)
        await page.wait_for_timeout(150)
        seen, blanks_ever = {}, 0
        for st in steps:
            if st[0] == "key":
                await page.click('.keypad [data-key="%s"]' % st[1])
            elif st[0] == "type":
                await page.fill("#numK", st[1])
            elif st[0] == "set":
                await page.click("#setBtn")
            await page.wait_for_timeout(60)
            now = await page.evaluate(STATE)
            blanks_ever = max(blanks_ever, now["blanks"])
            if st[0] == "look":
                seen[st[1]] = dict(now, blanks_ever=blanks_ever)
        return seen
    finally:
        await ctx.close()


FIXTURE_RUNS = {
    "opens": [("look", "start"), ("key", "5"), ("key", "4"), ("look", "typed"), ("set",), ("look", "after")],
    "miss": [("key", "5"), ("key", "4"), ("key", "0"), ("key", "0"), ("look", "typed"), ("set",), ("look", "after")],
    "empty": [("look", "before"), ("set",), ("look", "after")],
    "zero": [("key", "0"), ("key", "5"), ("key", "4"), ("look", "lead"), ("key", "clr"),
             ("key", "5"), ("key", "4"), ("key", "0"), ("key", "0"), ("key", "9"), ("look", "cap")],
    "typed": [("type", "0054"), ("look", "lead"), ("type", "12345"), ("look", "cap"),
              ("type", "54"), ("set",), ("look", "after")],
}
FIXED_RUN = [("look", "start"), ("key", "5"), ("look", "one"), ("set",), ("look", "after")]


def judge_fixture(got):
    f = []

    def want(cond, msg):
        if not cond:
            f.append(msg)
    o = got["opens"]
    want(all(o[k]["blanks_ever"] == 0 for k in o), "fixture: the display showed an empty slot")
    want(o["typed"]["disp"] == "54", "fixture: 5,4 displays %r, want '54'" % o["typed"]["disp"])
    want(o["after"]["open"], "fixture: 5,4,Set did not open the lock (%s)" % (o["after"]["fbText"][:60] or "no feedback"))
    m = got["miss"]
    want(m["typed"]["disp"] == "5400", "fixture: 5,4,0,0 displays %r, want '5400'" % m["typed"]["disp"])
    want("near" in m["after"]["fb"], "fixture: 5,4,0,0,Set did not raise the named misconception (%s)" % (m["after"]["fbText"][:60] or "no feedback"))
    want(m["after"]["blanks_ever"] == 0, "fixture: the display showed an empty slot (misconception run)")
    e = got["empty"]
    want(not e["after"]["fb"] and e["after"]["clock"] == e["before"]["clock"] and not e["after"]["open"],
         "fixture: Set with nothing typed did something (%s, clock %s -> %s)" % (e["after"]["fbText"][:60], e["before"]["clock"], e["after"]["clock"]))
    z = got["zero"]
    want(z["lead"]["disp"] == "54", "fixture: 0,5,4 displays %r, want '54'" % z["lead"]["disp"])
    want(z["cap"]["disp"] == "5400", "fixture: 5,4,0,0,9 displays %r, want '5400'" % z["cap"]["disp"])
    t = got["typed"]
    want(t["lead"]["disp"] == "54", "fixture: typed 0054 displays %r, want '54'" % t["lead"]["disp"])
    want(t["cap"]["disp"] == "1234", "fixture: typed 12345 displays %r, want '1234'" % t["cap"]["disp"])
    want(t["after"]["open"], "fixture: typed 54 then Set did not open the lock")
    return f


def judge_fixed(got):
    f = []
    if got["start"]["blanks"] != 2:
        f.append("fixed: the two-digit keypad starts with %d empty slots, want 2" % got["start"]["blanks"])
    if got["one"]["blanks"] != 1:
        f.append("fixed: after 5 the display has %d empty slots, want 1" % got["one"]["blanks"])
    if "Not enough digits." not in got["after"]["fbText"] or got["after"]["clock"] != got["one"]["clock"]:
        f.append("fixed: 5,Set gave %r (clock %s -> %s), want 'Not enough digits.' at no cost"
                 % (got["after"]["fbText"][:60], got["one"]["clock"], got["after"]["clock"]))
    return f


async def run(engine_js, with_fixed):
    from playwright.async_api import async_playwright
    proc, base = ti._serve(ROOT)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            names = list(FIXTURE_RUNS)
            jobs = [scenario(browser, base, engine_js, True, FIXTURE_RUNS[n]) for n in names]
            if with_fixed:
                jobs.append(scenario(browser, base, engine_js, False, FIXED_RUN))
            res = await asyncio.gather(*jobs, return_exceptions=True)
            await browser.close()
    finally:
        proc.terminate()
    errs = [str(r).splitlines()[0][:120] for r in res if isinstance(r, Exception)]
    if errs:
        return ["could not drive the page: " + e for e in errs], []
    fixed = judge_fixed(res[-1]) if with_fixed else []
    return judge_fixture(dict(zip(names, res))), fixed


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-plants", action="store_true")
    a = ap.parse_args()
    fix, fixed = asyncio.run(run(None, True))
    print("Escape-room keypad (KEYPAD-VARIABLE): fixture %s/%s at maxDigits 4, answer 54, misconception 5400" % (ROOM, LOCK))
    print("  %s  fixture%s" % ("FAIL" if fix else "ok  ", (": " + "; ".join(fix)) if fix else ""))
    print("  %s  fixed two-digit keypad unchanged%s" % ("FAIL" if fixed else "ok  ", (": " + "; ".join(fixed)) if fixed else ""))
    ok = not fix and not fixed
    if not a.no_plants:
        pfix, _ = asyncio.run(run(plant(ENGINE.read_text(encoding="utf-8")), False))
        print("plant (the old fixed-length rule: maxDigits read as digits): %s"
              % (("CAUGHT: " + "; ".join(pfix[:3])) if pfix else "MISSED"))
        ok = ok and bool(pfix)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
