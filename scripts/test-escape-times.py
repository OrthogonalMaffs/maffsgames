#!/usr/bin/env python3
# ci-line: Escape-room times (every live room played on a fake clock: game_completed's detail is exactly "escaped or timeout, wrongs, hints, used, played, locks", used - played is the wrong-setting penalties, capped when a wrong runs the clock out, locks in lock order with "-" unopened, a resumed save keeps played and openAt, an old save resumes from nought, every room's worst case at most 100 characters; planted fault caught) |
# ci-deps: escape-rooms/ scripts/check-teacher-invite.py scripts/plant_common.py
"""What a finished escape room reports about time (contract ROOM-TIMES, 7 Nov 2026; canon §1.3).

    python -X utf8 scripts/test-escape-times.py

game_completed's detail is, exactly,

    <escaped|timeout> wrongs:<n> hints:<n> used:<s> played:<s> locks:<t1>,<t2>,...

used is the room's clock (TOTAL - left, so wrong-setting penalties included, never more than TOTAL); played is the
seconds the clock actually ran; locks are each lock's played-second when it opened, in the room's lock order, "-" for
one never opened. Hints are free, so used - played is wrongs x the room's penalty, except when the last wrong setting
runs the clock out, where used stops at TOTAL.

Each live room (room.js, no noindex) is played in Chromium on Playwright's fake clock (page.clock: each run_for(1000)
is one tick of the room's setInterval), with window.mfg pinned to a recorder by an init script, served by
serve-stubbed.py so nothing is sent. The expected seconds are the test's own count of the time it advanced, never read
from the engine:

  win      5 s; a wrong setting on lock 2 (lock 1 in a one-lock room); a hint on lock 1; 10 s, open the last lock;
           20 s, open lock 1 (out of order). The save then holds played 35 and both lock times; reload and Resume:
           the resumed save holds the same. Then 7 s per remaining lock, in order, to the escape.
  clock    5 s, open lock 1; two wrong settings and two hints on lock 2 (lock 1 in a one-lock room: wrongs before it
           opens); then the clock runs out: played = TOTAL - 2 x penalty, used = TOTAL, unopened locks "-".
  penalty  TOTAL - k seconds (0 < k < penalty), then one wrong setting runs the clock out: used = TOTAL, played =
           TOTAL - k, so used - played = k, less than the penalty.
  old      a save with played and openAt deleted (made before ROOM-TIMES) resumes with played 0 and openAt {}, its
           opened lock still open; the room still finishes with a detail in the format.

Also, for every live room, the worst case from its own data (TOTAL and penalty from room.js, every hint taken, the most
wrongs the clock allows, every figure at TOTAL's digits) is at most 100 characters (GA4's limit for a parameter).

Planted fault (the engine served from a patched copy by routing, no file edited): game_completed's detail sent without
the times, as before ROOM-TIMES. It must be caught.
"""
import importlib.util
import json
import math
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import plant_common as pc  # noqa: E402

spec = importlib.util.spec_from_file_location("teacher_invite", ROOT / "scripts" / "check-teacher-invite.py")
ti = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ti)

ENGINE = "escape-rooms/assets/engine.js"
LIMIT = 100
FORMAT = re.compile(r"^(escaped|timeout) wrongs:(\d+) hints:(\d+) used:(\d+) played:(\d+) locks:((?:\d+|-)(?:,(?:\d+|-))*)$")

# window.mfg pinned to a recorder: analytics.js (stubbed or not) assigns window.mfg, and the setter ignores it.
INIT = """(() => {
  const log = [];
  const rec = function (n, p) { log.push([n, JSON.parse(JSON.stringify(p || {}))]); };
  Object.defineProperty(window, 'mfg', { configurable: true, get: () => rec, set: () => {} });
  window.__mfgLog = log;
})();"""

# Open (win) or miss (not win) lock i: the shared room driver's setting logic (check-teacher-invite.py ROOM_STEP),
# aimed at one lock. Returns false if the lock is already open.
SET_LOCK = r"""([i, win]) => {
  const R = window.ROOM, l = R.locks[i];
  let vars = {};
  try { vars = (JSON.parse(localStorage.getItem('mfg_escape_vars_' + R.slug)) || {}).vars || {}; } catch (e) {}
  document.querySelector('[data-lock="' + i + '"]').click();
  const set = document.getElementById('setBtn');
  if (!set) return false;
  const v = l.variants ? (l.variants[vars[l.id] || 0] || l.variants[0]) : {};
  const ans = v.answer !== undefined ? v.answer : l.answer, ins = l.instrument;
  const put = (id, val) => { const n = document.getElementById(id); n.value = String(val); n.dispatchEvent(new Event('input', {bubbles: true})); };
  if (ins.kind === 'keypad') {
    const d = ins.digits || ins.maxDigits, good = String(ans).padStart(d, '0');
    put('numK', win ? good : (good === '0'.repeat(d) ? '1'.repeat(d) : '0'.repeat(d)));
  } else if (ins.kind === 'pair') {
    put('numA', win ? ans[0] : (Number(ans[0]) === ins.a.min ? ins.a.max : ins.a.min));
    put('numB', ans[1]);
  } else {
    put('num', win ? ans : (Number(ans) === ins.min ? ins.max : ins.min));
  }
  set.click();
  return true;
}"""

HINT = r"""(i) => {
  document.querySelector('[data-lock="' + i + '"]').click();
  const b = document.getElementById('hintBtn');
  if (!b) return false;
  b.click();
  return true;
}"""


def live_rooms():
    for room in sorted((ROOT / "escape-rooms").iterdir()):
        if (room / "room.js").exists() and "noindex" not in (room / "index.html").read_text(encoding="utf-8"):
            yield room.name


def plant_no_times(engine):
    return pc.apply_plant(
        engine,
        "      detail: (win ? 'escaped' : 'timeout') + ' wrongs:' + st.wrongs + ' hints:' + hintCount +\n"
        "              ' used:' + used + ' played:' + st.played + ' locks:' +\n"
        "              R.locks.map(function (l) { return st.openAt[l.id] === undefined ? '-' : st.openAt[l.id]; }).join(',')\n",
        "      detail: (win ? 'escaped' : 'timeout') + ' wrongs:' + st.wrongs + ' hints:' + hintCount\n",
        name="game_completed's detail without the times")


class Room:
    """One room's page on a fake clock, the engine optionally served from `engine_src`."""

    def __init__(self, browser, base, slug, engine_src=None):
        self.ctx = browser.new_context()
        self.ctx.add_init_script(INIT)
        if engine_src is not None:
            self.ctx.route("**/" + ENGINE, lambda r: r.fulfill(status=200, body=engine_src.encode("utf-8"),
                                                              content_type="application/javascript; charset=utf-8"))
        self.page = self.ctx.new_page()
        self.page.clock.install()
        self.url = "%s/escape-rooms/%s/?cb=times" % (base, slug)
        self.page.goto(self.url, wait_until="load")
        self.page.evaluate("localStorage.clear()")
        self.page.reload(wait_until="load")
        self.R = self.page.evaluate("() => ({ slug: ROOM.slug, minutes: ROOM.minutes, penalty: ROOM.penalty,"
                                    " locks: ROOM.locks.map(l => l.id) })")
        self.total = (self.R["minutes"] or 15) * 60
        self.pen = self.R["penalty"] or 45
        self.n = len(self.R["locks"])

    def start(self):
        self.page.click("#startBtn")

    def run(self, s):
        self.page.clock.run_for(int(s * 1000))

    def set(self, i, win):
        return self.page.evaluate(SET_LOCK, [i, win])

    def hint(self, i):
        return self.page.evaluate(HINT, i)

    def save(self):
        raw = self.page.evaluate("() => localStorage.getItem('mfg_escape_' + ROOM.slug)")
        return json.loads(raw) if raw else None

    def resume(self):
        self.page.reload(wait_until="load")
        self.page.click("#resumeBtn")

    def ended(self):
        return self.page.evaluate("document.getElementById('scrEnd').classList.contains('active')")

    def completed(self):
        return [p for n, p in self.page.evaluate("window.__mfgLog") if n == "game_completed"]

    def close(self):
        self.ctx.close()


def expect_detail(outcome, wrongs, hints, used, played, locks):
    return "%s wrongs:%d hints:%d used:%d played:%d locks:%s" % (
        outcome, wrongs, hints, used, played, ",".join("-" if t is None else str(t) for t in locks))


def check_completed(room, faults, label, want, opened):
    got = room.completed()
    if len(got) != 1:
        faults.append("%s %s: %d game_completed sent (want 1)" % (room.R["slug"], label, len(got)))
        return
    p = got[0]
    det = p.get("detail", "")
    if not FORMAT.match(det):
        faults.append("%s %s: detail %r is not in the format" % (room.R["slug"], label, det))
    if det != want:
        faults.append("%s %s: detail %r (want %r)" % (room.R["slug"], label, det, want))
    if len(det) > LIMIT:
        faults.append("%s %s: detail is %d characters (limit %d)" % (room.R["slug"], label, len(det), LIMIT))
    others = {k: v for k, v in p.items() if k != "detail"}
    want_others = {"game_slug": room.R["slug"], "level": others.get("level"), "score": opened,
                   "questions_answered": room.n, "questions_correct": opened}
    if others != want_others or others.get("level") in (None, ""):
        faults.append("%s %s: game_completed's other parameters changed: %r" % (room.R["slug"], label, others))


def scenario_win(browser, base, slug, faults, engine_src=None):
    r = Room(browser, base, slug, engine_src)
    try:
        r.start()
        n, t, locks = r.n, 0, [None] * r.n
        r.run(5); t += 5
        miss = 1 if n > 1 else 0
        r.set(miss, False)
        r.hint(0)
        r.run(10); t += 10
        if n > 1:
            r.set(n - 1, True); locks[n - 1] = t
        r.run(20); t += 20
        r.set(0, True); locks[0] = t
        s = r.save()
        want_at = {r.R["locks"][i]: locks[i] for i in range(n) if locks[i] is not None}
        if s is not None:
            if s.get("played") != t or s.get("openAt") != want_at:
                faults.append("%s win: save holds played %r, openAt %r (want %d, %r)" % (slug, s.get("played"), s.get("openAt"), t, want_at))
        if not r.ended() and s is not None:
            r.resume()
            s2 = r.save()
            if not s2 or s2.get("played") != t or s2.get("openAt") != want_at:
                faults.append("%s win: resumed save holds played %r, openAt %r (want %d, %r)"
                              % (slug, s2 and s2.get("played"), s2 and s2.get("openAt"), t, want_at))
            for i in range(n):
                if locks[i] is None:
                    r.run(7); t += 7
                    r.set(i, True); locks[i] = t
        r.run(0.95)                            # the engine's 900 ms before the end card; no tick falls in it
        if not r.ended():
            faults.append("%s win: the room never reached its end card" % slug)
            return
        wrongs = 1
        check_completed(r, faults, "win", expect_detail("escaped", wrongs, 1, t + wrongs * r.pen, t, locks), n)
    finally:
        r.close()


def scenario_clock(browser, base, slug, faults):
    r = Room(browser, base, slug)
    try:
        r.start()
        n, locks = r.n, [None] * r.n
        miss = 1 if n > 1 else 0
        if n == 1:
            for _ in range(2):
                r.set(miss, False)
            r.hint(miss); r.hint(miss)
            r.run(5)
        else:
            r.run(5)
            r.set(0, True); locks[0] = 5
            for _ in range(2):
                r.set(miss, False)
            r.hint(miss); r.hint(miss)
        r.run(r.total + 5)
        if not r.ended():
            faults.append("%s clock: the room never timed out" % slug)
            return
        played = r.total - 2 * r.pen
        check_completed(r, faults, "clock", expect_detail("timeout", 2, 2, r.total, played, locks),
                        sum(t is not None for t in locks))
    finally:
        r.close()


def scenario_penalty(browser, base, slug, faults):
    r = Room(browser, base, slug)
    try:
        r.start()
        k = (r.pen + 1) // 2                   # 0 < k < penalty: the wrong setting overshoots the clock by penalty - k
        r.run(r.total - k)
        r.set(0, False)
        if not r.ended():
            faults.append("%s penalty: the last wrong setting did not end the room" % slug)
            return
        played = r.total - k
        check_completed(r, faults, "penalty", expect_detail("timeout", 1, 0, r.total, played, [None] * r.n), 0)
        if r.total - played >= r.pen:
            faults.append("%s penalty: used - played is %d, not less than the penalty %d" % (slug, r.total - played, r.pen))
    finally:
        r.close()


def scenario_old(browser, base, slug, faults):
    r = Room(browser, base, slug)
    try:
        r.start()
        r.run(3)
        r.set(0, True)
        if r.ended():                          # a one-lock room has nothing left to resume
            return
        r.page.evaluate("() => { const k = 'mfg_escape_' + ROOM.slug, s = JSON.parse(localStorage.getItem(k));"
                        " delete s.played; delete s.openAt; localStorage.setItem(k, JSON.stringify(s)); }")
        r.resume()
        s = r.save()
        if not s or s.get("played") != 0 or s.get("openAt") != {} or not s.get("open", {}).get(r.R["locks"][0]):
            faults.append("%s old save: resumed as %r (want played 0, openAt {}, lock 1 still open)"
                          % (slug, s and {k: s.get(k) for k in ("played", "openAt", "open")}))
        t = 0
        for i in range(1, r.n):
            r.run(2); t += 2
            r.set(i, True)
        r.run(0.95)
        got = r.completed()
        det = got[0].get("detail", "") if len(got) == 1 else ""
        # the clock's 3 s before the resume stay in used (left is saved); played and lock 1's time are not recoverable
        want = expect_detail("escaped", 0, 0, t + 3, t, [None] + [2 * i for i in range(1, r.n)])
        if det != want:
            faults.append("%s old save: detail %r (want %r: lock 1 opened before the times were kept)" % (slug, det, want))
    finally:
        r.close()


def worst_case(browser, base, slug):
    """The longest detail this room can send, from its own data."""
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto("%s/escape-rooms/%s/?cb=times" % (base, slug), wait_until="load")
    d = page.evaluate("() => ({ minutes: ROOM.minutes, penalty: ROOM.penalty,"
                      " hints: ROOM.locks.map(l => (l.hints || []).length) })")
    ctx.close()
    total = (d["minutes"] or 15) * 60
    pen = d["penalty"] or 45
    wrongs = math.ceil(total / pen)            # each wrong setting costs pen seconds; the room ends at 0
    s = "timeout wrongs:%d hints:%d used:%d played:%d locks:%s" % (
        wrongs, sum(d["hints"]), total, total, ",".join([str(total)] * len(d["hints"])))
    return s


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    rooms = list(live_rooms())
    faults, lengths = [], {}
    engine = (ROOT / ENGINE).read_text(encoding="utf-8")
    proc, base = ti._serve(ROOT)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for slug in rooms:
                w = worst_case(browser, base, slug)
                lengths[slug] = len(w)
                if len(w) > LIMIT:
                    faults.append("%s: worst-case detail is %d characters (limit %d): %s" % (slug, len(w), LIMIT, w))
                for sc in (scenario_win, scenario_clock, scenario_penalty, scenario_old):
                    try:
                        sc(browser, base, slug, faults)
                    except Exception as exc:
                        faults.append("%s %s: %s" % (slug, sc.__name__, str(exc).splitlines()[0][:200]))
            plant_faults, plant_err = [], None
            try:
                scenario_win(browser, base, rooms[0], plant_faults, plant_no_times(engine))
            except pc.StalePlant as exc:
                plant_err = str(exc)
            except Exception as exc:
                plant_err = "the planted run errored: %s" % str(exc).splitlines()[0][:200]
            browser.close()
    finally:
        proc.terminate()
        proc.wait(timeout=10)
    print("escape times: %d live rooms, 4 plays each; worst-case detail %d to %d characters (limit %d)"
          % (len(rooms), min(lengths.values()), max(lengths.values()), LIMIT))
    for slug in rooms:
        print("  %-24s worst case %d characters" % (slug, lengths[slug]))
    for f in faults:
        print("  FAIL " + f)
    caught = pc.is_caught([f for f in plant_faults if "detail" in f], plant_err)
    print("plant (game_completed's detail without the times, %s): %s"
          % (rooms[0], "CAUGHT" if caught else "MISSED: " + (plant_err or "; ".join(plant_faults) or "no fault")))
    ok = not faults and caught
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
