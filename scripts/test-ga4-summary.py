#!/usr/bin/env python3
# ci-line: GA4 summary Apps Script (mocked Sheet: weekly sums match the raw tabs, partial weeks marked, top ten, three charts created once, values-only rebuilds, GA4 tabs/Sheet1/Dashboard untouched; planted faults caught) |
"""Tests for docs/apps-script-ga4-summary.js, the Apps Script that rebuilds the 'GA4 summary' tab (weekly figures
and three charts) from the two GA4 country tabs. No network: the scripts run in Node's vm module against mocks of
SpreadsheetApp, Charts, LockService, Utilities and Logger.

    python scripts/test-ga4-summary.py

What it proves:
  (a) the weekly rows equal an independent sum of the raw tabs (Monday weeks from 31 Aug 2026; questions answered
      for w/c 19 Oct 2026 is 4,351), UK engaged sessions are the United Kingdom's and rest of world is everyone
      else's, the first week and the unfinished current week are marked 'partial' and complete weeks are not;
  (b) the top ten is the ten countries with most engaged sessions over the last 28 complete days, with sessions and
      engaged share, and a day outside the window is not counted;
  (c) three charts exist after the first run (line, line, bar), and a second run, and a run after the raw figures
      change, leave the same three chart objects: values change, charts do not;
  (d) the GA4 tabs, Sheet1 and the Dashboard are not changed, only the three tabs by name are asked for, and the
      summary tab is added at the end;
  (e) a missing GA4 tab raises and creates nothing; the window rolls at 52 weeks;
  (f) ga4CountryDaily and ga4CountryBackfill call the rebuild once their refresh has finished, and work as before
      when the summary file is not in the project;
  (g) no top-level name collides with ga4-country or the endpoint.
Then planted faults, each a small change to the script that must make a check fail: UK counted with the rest, a
chart added on every run, weeks starting on Sunday, nothing marked partial.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUMMARY = os.path.join(ROOT, "docs", "apps-script-ga4-summary.js")
COUNTRY = os.path.join(ROOT, "docs", "apps-script-ga4-country.js")
ENDPOINT = os.path.join(ROOT, "docs", "apps-script-endpoint.js")

NOW = "2026-10-28T10:00:00Z"            # Wednesday; yesterday is Tue 27 Oct; the 28-day window is 30 Sep..27 Oct
COUNTRIES = ["United Kingdom", "United States", "Ireland", "India", "Singapore", "China", "(not set)",
             "France", "Spain", "Italy", "Poland", "Kenya"]
D0, D1 = date(2026, 9, 1), date(2026, 10, 27)


def h(s):
    x = 2166136261
    for c in s:
        x = ((x ^ ord(c)) * 16777619) & 0xFFFFFFFF
    return x


def fixture():
    daily, events = [], []
    d = D1
    while d >= D0:
        k = d.isoformat()
        for c in COUNTRIES:
            if h(k + c) % 4 == 0:
                continue
            sessions = 5 + h(k + c + "s") % 60
            daily.append([k, c, 1 + h(k + c + "u") % 30, sessions, h(k + c + "e") % (sessions + 1), 100 + h(k + c + "n") % 900])
            for ev in ("page_view", "game_started", "question_answered", "game_completed"):
                if ev != "page_view" and h(k + c + ev) % 3 == 0:
                    continue
                events.append([k, c, ev, 1 + h(k + c + ev + "u") % 20, 1 + h(k + c + ev + "n") % 400])
        d -= timedelta(days=1)
    # w/c 19 Oct 2026: questions answered is exactly 4,351 (UK per day 700,650,600,500,450,400,300 = 3,600; US 751 on Monday)
    events = [r for r in events if not (r[2] == "question_answered" and "2026-10-19" <= r[0] <= "2026-10-25")]
    for i, n in enumerate([700, 650, 600, 500, 450, 400, 300]):
        events.append([(date(2026, 10, 19) + timedelta(days=i)).isoformat(), "United Kingdom", "question_answered", 9, n])
    events.append(["2026-10-19", "United States", "question_answered", 4, 751])
    return daily, events


def monday(k):
    d = date.fromisoformat(k)
    return (d - timedelta(days=d.weekday())).isoformat()


def expected(daily, events):
    weeks = {}
    for r in events:
        w = weeks.setdefault(monday(r[0]), [0, 0, 0, 0, 0])
        if r[2] == "question_answered":
            w[0] += r[4]
        elif r[2] == "game_started":
            w[1] += r[4]
        elif r[2] == "game_completed":
            w[2] += r[4]
    for r in daily:
        w = weeks.setdefault(monday(r[0]), [0, 0, 0, 0, 0])
        w[3 if r[1] == "United Kingdom" else 4] += r[4]
    out = []
    m = date(2026, 8, 31)
    while m <= date(2026, 10, 26):
        k = m.isoformat()
        w = weeks.get(k, [0, 0, 0, 0, 0])
        partial = (m + timedelta(days=6)).isoformat() > "2026-10-27" or k == "2026-08-31"
        out.append([k] + w + ["partial" if partial else ""])
        m += timedelta(days=7)
    top = {}
    for r in daily:
        if "2026-09-30" <= r[0] <= "2026-10-27":
            t = top.setdefault(r[1], [0, 0])
            t[0] += r[4]
            t[1] += r[3]
    ranked = sorted(top.items(), key=lambda kv: (-kv[1][0], kv[0]))[:10]
    return out, [[c, e, s, e / s if s else 0] for c, (e, s) in ranked]


HARNESS = r"""
'use strict';
const vm = require('vm');
const fs = require('fs');
const [summaryPath, countryPath, fixturePath] = process.argv.slice(2);
const FIX = JSON.parse(fs.readFileSync(fixturePath, 'utf8'));
const UNEXPECTED = [], ASKED = [];

function makeSheet(name, rows) {
  const s = { name, cells: rows.map(r => r.slice()), fmt: {}, charts: [], frozen: 0 };
  s.lastRow = () => { for (let i = s.cells.length; i > 0; i--) if (s.cells[i - 1].some(v => v !== '' && v !== undefined)) return i; return 0; };
  const range = (r, c, nr, nc) => {
    nr = nr || 1; nc = nc || 1;
    const rng = {
      a1: null, r, c, nr, nc,
      getValues() { const out = []; for (let i = 0; i < nr; i++) { const row = s.cells[r - 1 + i] || []; const o = []; for (let j = 0; j < nc; j++) o.push(row[c - 1 + j] === undefined ? '' : row[c - 1 + j]); out.push(o); } return out; },
      setValues(v) {
        if (v.length !== nr || v.some(x => x.length !== nc)) throw new Error('setValues: shape ' + v.length + 'x' + (v[0] || []).length + ' into ' + nr + 'x' + nc);
        for (let i = 0; i < nr; i++) for (let j = 0; j < nc; j++) {
          let val = v[i][j];
          if (typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val) && s.fmt[(r + i) + ':' + (c + j)] !== '@') val = new Date(val + 'T00:00:00+01:00');
          (s.cells[r - 1 + i] = s.cells[r - 1 + i] || [])[c - 1 + j] = val;
        }
        return rng;
      },
      clearContent() { for (let i = 0; i < nr; i++) { const row = s.cells[r - 1 + i]; if (row) for (let j = 0; j < nc; j++) row[c - 1 + j] = ''; } return rng; },
      setNumberFormat(f) { for (let i = 0; i < nr; i++) for (let j = 0; j < nc; j++) s.fmt[(r + i) + ':' + (c + j)] = f; return rng; },
      setFontWeight() { return rng; }
    };
    return rng;
  };
  const colNum = L => L.split('').reduce((a, ch) => a * 26 + ch.charCodeAt(0) - 64, 0);
  s.api = {
    getLastRow: () => s.lastRow(),
    setFrozenRows: k => { s.frozen = k; },
    getName: () => s.name,
    getRange(a, b, c, d) {
      if (typeof a === 'string') {
        const m = /^([A-Z]+)(\d+):([A-Z]+)(\d+)$/.exec(a);
        const rng = range(Number(m[2]), colNum(m[1]), Number(m[4]) - Number(m[2]) + 1, colNum(m[3]) - colNum(m[1]) + 1);
        rng.a1 = a; return rng;
      }
      return range(a, b, c, d);
    },
    getCharts: () => s.charts,
    newChart() {
      const spec = { ranges: [], options: {}, type: null, headers: 0, pos: null };
      const b = {
        setChartType: t => { spec.type = t; return b; },
        addRange: r => { spec.ranges.push(r.a1); return b; },
        setNumHeaders: n => { spec.headers = n; return b; },
        setPosition: (r, c) => { spec.pos = [r, c]; return b; },
        setOption: (k, v) => { spec.options[k] = v; return b; },
        build: () => ({ spec, getOptions: () => ({ get: k => spec.options[k] }) })
      };
      return b;
    },
    insertChart: c => { s.charts.push(c); }
  };
  return s;
}
function proxy(target, label) {
  return new Proxy(target, { get(t, k) {
    if (typeof k === 'symbol') return t[k];
    if (!(k in t)) { UNEXPECTED.push(label + '.' + String(k)); throw new Error('unexpected access ' + label + '.' + String(k)); }
    return t[k];
  } });
}
function makeSS(withGa4) {
  const sheet1 = makeSheet('Sheet1', [['timestamp', 'event'], ['2026-10-07T09:00:00Z', 'game_started']]);
  const dash = makeSheet('Dashboard', [['MaffsGames Dashboard']]);
  const sheets = [sheet1, dash];
  if (withGa4) {
    sheets.push(makeSheet('GA4 country daily', [['date', 'country', 'activeUsers', 'sessions', 'engagedSessions', 'eventCount']].concat(FIX.daily)));
    sheets.push(makeSheet('GA4 country events', [['date', 'country', 'eventName', 'activeUsers', 'eventCount']].concat(FIX.events)));
  }
  const ss = {
    getSheetByName(name) { ASKED.push(name); const s = sheets.find(x => x.name === name); return s ? s.api : null; },
    insertSheet(name, idx) { const s = makeSheet(name, []); sheets.splice(idx === undefined ? 1 : idx, 0, s); return s.api; },
    getNumSheets: () => sheets.length,
    getSpreadsheetTimeZone: () => 'Europe/London'
  };
  return { sheets, proxy: proxy(ss, 'spreadsheet') };
}

let SS = makeSS(true);
const LOG = [];
const ctx = {
  SpreadsheetApp: proxy({ getActiveSpreadsheet: () => SS.proxy }, 'SpreadsheetApp'),
  Charts: { ChartType: { LINE: 'LINE', BAR: 'BAR' } },
  Utilities: { formatDate(d, tz, fmt) {
    if (fmt !== 'yyyy-MM-dd') throw new Error('format ' + fmt);
    return new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
  } },
  LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
  Logger: { log: m => LOG.push(String(m)) }
};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(countryPath, 'utf8'), ctx, { filename: 'country' });
vm.runInContext(fs.readFileSync(summaryPath, 'utf8'), ctx, { filename: 'summary' });
function setNow(iso) { vm.runInContext('ga4cNow_ = function () { return new Date(' + JSON.stringify(iso) + '); };', ctx); }
function run(fn) { try { vm.runInContext(fn + '()', ctx); return null; } catch (e) { return String(e && e.message || e); } }
const find = n => SS.sheets.find(s => s.name === n);
const clone = x => JSON.parse(JSON.stringify(x));
const body = s => s.cells.filter(r => r.some(v => v !== '' && v !== undefined));
function summary() {
  const t = find('GA4 summary');
  if (!t) return null;
  const weeks = body({ cells: t.cells.map(r => r.slice(0, 7)) });
  const top = body({ cells: t.cells.map(r => r.slice(8, 12)) });
  return { weeks, top, charts: t.charts.map(c => clone(c.spec)), chartObjs: t.charts.slice(), order: SS.sheets.map(s => s.name) };
}
const R = {};
const raw = () => clone({ s1: find('Sheet1').cells, dash: find('Dashboard').cells, d: find('GA4 country daily').cells, e: find('GA4 country events').cells });

setNow('2026-10-28T10:00:00Z');
const before = raw();
R.run1 = { error: run('ga4SummaryRebuild') }; const s1 = summary(); R.run1.weeks = s1.weeks; R.run1.top = s1.top; R.run1.charts = s1.charts; R.order = s1.order;
R.run2 = { error: run('ga4SummaryRebuild') }; const s2 = summary();
R.run2.same = JSON.stringify([s2.weeks, s2.top]) === JSON.stringify([s1.weeks, s1.top]);
R.run2.sameChartObjects = s2.chartObjs.length === s1.chartObjs.length && s2.chartObjs.every((c, i) => c === s1.chartObjs[i]);
R.run2.chartCount = s2.charts.length;
// the raw figures change: one Monday's questions answered
find('GA4 country events').cells.push(['2026-10-26', 'United Kingdom', 'question_answered', 3, 1000]);
R.run3 = { error: run('ga4SummaryRebuild') }; const s3 = summary();
R.run3.weeks = s3.weeks; R.run3.chartCount = s3.charts.length; R.run3.sameChartObjects = s3.chartObjs.every((c, i) => c === s1.chartObjs[i]);
find('GA4 country events').cells.pop();
const after = raw();
R.untouched = JSON.stringify(before) === JSON.stringify(after);
R.asked = Array.from(new Set(ASKED)); R.unexpected = UNEXPECTED.slice();

// a missing GA4 tab
SS = makeSS(true); SS.sheets.splice(SS.sheets.findIndex(s => s.name === 'GA4 country events'), 1);
R.missing = { error: run('ga4SummaryRebuild'), created: !!find('GA4 summary') };

// the window rolls at 52 weeks
SS = makeSS(true);
setNow('2027-12-01T10:00:00Z');
R.roll = { error: run('ga4SummaryRebuild') }; const sr = summary();
R.roll.n = sr.weeks.length - 1; R.roll.first = sr.weeks[1][0]; R.roll.last = sr.weeks[sr.weeks.length - 1][0];

// the hook: refresh stubbed out, so only the call order matters
for (const fn of ['ga4CountryDaily', 'ga4CountryBackfill']) {
  SS = makeSS(true); setNow(NOW_PLACEHOLDER);
  vm.runInContext('ga4cRefresh_ = function () { globalThis.__refreshed = true; };', ctx);
  vm.runInContext('globalThis.__refreshed = false;', ctx);
  const e = run(fn);
  R['hook_' + fn] = { error: e, built: !!find('GA4 summary'), refreshed: vm.runInContext('globalThis.__refreshed', ctx) };
}
// ... and without the summary file in the project
const ctx2 = Object.assign({}, ctx, {});
const ctxB = { SpreadsheetApp: ctx.SpreadsheetApp, Utilities: ctx.Utilities, LockService: ctx.LockService, Logger: ctx.Logger };
vm.createContext(ctxB);
vm.runInContext(fs.readFileSync(countryPath, 'utf8'), ctxB);
vm.runInContext('ga4cRefresh_ = function () { globalThis.__r = 1; };', ctxB);
try { vm.runInContext('ga4CountryDaily(); ga4CountryBackfill();', ctxB); R.noSummaryFile = { error: null, refreshed: vm.runInContext('globalThis.__r', ctxB) }; }
catch (e) { R.noSummaryFile = { error: String(e.message) }; }
process.stdout.write(JSON.stringify(R));
""".replace("NOW_PLACEHOLDER", json.dumps(NOW))


def find_node():
    node = shutil.which("node")
    if node:
        return node
    try:
        import playwright
        cand = os.path.join(os.path.dirname(playwright.__file__), "driver", "node")
        if os.path.exists(cand) or os.path.exists(cand + ".exe"):
            return cand
    except ImportError:
        pass
    sys.exit("FAIL  no node on PATH and no Playwright driver node")


def run_harness(node, summary_src, workdir, tag, fx_path):
    sp = os.path.join(workdir, "summary-%s.js" % tag)
    hp = os.path.join(workdir, "harness.js")
    with open(sp, "w", encoding="utf-8", newline="") as f:
        f.write(summary_src)
    if not os.path.exists(hp):
        with open(hp, "w", encoding="utf-8", newline="") as f:
            f.write(HARNESS)
    p = subprocess.run([node, hp, sp, COUNTRY, fx_path], capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout), None


def toplevel(src):
    names = set(re.findall(r"^(?:function\s+([A-Za-z0-9_$]+)|(?:const|let|var)\s+([A-Za-z0-9_$]+))", src, re.M))
    return {a or b for a, b in names}


def checks(R, daily, events):
    out = {}
    want_weeks, want_top = expected(daily, events)
    f = []
    for k in ("run1", "run2", "run3"):
        if R[k]["error"]:
            f.append("%s raised: %s" % (k, R[k]["error"]))
    out["rebuild runs without error"] = f

    got = R["run1"]["weeks"][1:]
    f = []
    if R["run1"]["weeks"][0][0] != "Week starting":
        f.append("weekly header row missing")
    if len(got) != len(want_weeks):
        f.append("%d weekly rows, expected %d" % (len(got), len(want_weeks)))
    for g, w in zip(got, want_weeks):
        if g[:6] != w[:6]:
            f.append("week %s: %s, expected %s" % (w[0], g[:6], w[:6]))
    if not any(g[0] == "2026-10-19" and g[1] == 4351 for g in got):
        f.append("w/c 19 Oct questions answered is not 4,351")
    out["weekly figures equal the raw tabs, from 31 Aug, 4,351 for w/c 19 Oct"] = f

    f = [("week %s status %r, expected %r" % (g[0], g[6], w[6])) for g, w in zip(got, want_weeks) if g[6] != w[6]]
    out["first and current weeks marked partial, complete weeks not"] = f

    top = R["run1"]["top"][1:]
    f = []
    if len(top) != 10:
        f.append("%d countries in the top table, expected 10" % len(top))
    for g, w in zip(top, want_top):
        if g[0] != w[0] or g[1] != w[1] or g[2] != w[2] or abs(g[3] - w[3]) > 1e-9:
            f.append("top ten: %s, expected %s" % (g, w))
    out["top ten by engaged sessions over the last 28 days"] = f

    ch = R["run1"]["charts"]
    f = []
    if [c["type"] for c in ch] != ["LINE", "LINE", "BAR"]:
        f.append("charts after run 1: %s" % [c["type"] for c in ch])
    else:
        rngs = [c["ranges"] for c in ch]
        if rngs[0] != ["A1:A53", "B1:B53"] or rngs[1] != ["A1:A53", "E1:F53"] or rngs[2] != ["I1:J11"]:
            f.append("chart ranges %s" % rngs)
    out["three charts: line, line (two series), bar, on fixed ranges"] = f

    f = []
    if not R["run2"]["same"]:
        f.append("a second run changed the values")
    if R["run2"]["chartCount"] != 3 or not R["run2"]["sameChartObjects"]:
        f.append("second run left %d charts (or replaced them)" % R["run2"]["chartCount"])
    if R["run3"]["chartCount"] != 3 or not R["run3"]["sameChartObjects"]:
        f.append("run after a data change left %d charts (or replaced them)" % R["run3"]["chartCount"])
    changed = [r for r, o in zip(R["run3"]["weeks"], R["run1"]["weeks"]) if r != o]
    prior = [o for o in R["run1"]["weeks"] if o[0] == "2026-10-26"]
    if len(changed) != 1 or changed[0][0] != "2026-10-26" or not prior or changed[0][1] != prior[0][1] + 1000:
        f.append("a changed Monday did not change exactly its own row: %s" % changed)
    out["rebuilds change values only; a second run leaves three charts"] = f

    f = []
    if not R["untouched"]:
        f.append("the GA4 tabs, Sheet1 or the Dashboard changed")
    if set(R["asked"]) - {"GA4 summary", "GA4 country daily", "GA4 country events"}:
        f.append("asked for other tabs: %s" % sorted(set(R["asked"])))
    if R["unexpected"]:
        f.append("unexpected API use: %s" % R["unexpected"])
    if R["order"][:2] != ["Sheet1", "Dashboard"] or R["order"][-1] != "GA4 summary":
        f.append("tab order %s" % R["order"])
    out["GA4 tabs, Sheet1 and Dashboard untouched; summary added at the end"] = f

    f = []
    if not R["missing"]["error"] or R["missing"]["created"]:
        f.append("a missing GA4 tab: %s" % R["missing"])
    out["a missing GA4 tab raises and creates nothing"] = f

    f = []
    r = R["roll"]
    if r["error"] or r["n"] != 52 or r["last"] != "2027-11-29" or r["first"] != "2026-12-07":
        f.append("rolling window: %s" % r)
    out["the window rolls at 52 weeks"] = f

    f = []
    for fn in ("ga4CountryDaily", "ga4CountryBackfill"):
        r = R["hook_" + fn]
        if r["error"] or not r["built"] or not r["refreshed"]:
            f.append("%s: %s" % (fn, r))
    if R["noSummaryFile"].get("error") or not R["noSummaryFile"].get("refreshed"):
        f.append("without the summary file: %s" % R["noSummaryFile"])
    out["the daily job and the backfill rebuild the summary; fine without the file"] = f
    return out


def main():
    node = find_node()
    summary_src = open(SUMMARY, encoding="utf-8", newline="").read()
    daily, events = fixture()
    work = tempfile.mkdtemp(prefix="ga4s-")
    try:
        fx = os.path.join(work, "fixture.json")
        with open(fx, "w", encoding="utf-8", newline="") as f:
            json.dump({"daily": daily, "events": events}, f)
        R, err = run_harness(node, summary_src, work, "real", fx)
        if err:
            print("FAIL  harness crashed:\n" + err)
            return 1
        res = checks(R, daily, events)
        fails = 0
        for name, f in res.items():
            if f:
                fails += 1
                print("FAIL  %s" % name)
                for x in f[:5]:
                    print("      " + x)
            else:
                print("PASS  %s" % name)

        # names shared with the other two files in the project
        mine = toplevel(summary_src)
        other = toplevel(open(COUNTRY, encoding="utf-8", newline="").read()) | toplevel(open(ENDPOINT, encoding="utf-8", newline="").read())
        clash = sorted(mine & other)
        if clash:
            fails += 1
            print("FAIL  top-level names also used by ga4-country or the endpoint: %s" % clash)
        else:
            print("PASS  no top-level name collides with ga4-country or the endpoint")

        plants = [
            ("UK counted with the rest of the world", "if (r[1] === GA4S_UK) w.uk += engaged; else w.row += engaged;",
             "w.uk += engaged; w.row += engaged;", "weekly figures equal the raw tabs, from 31 Aug, 4,351 for w/c 19 Oct"),
            ("a chart added on every run", "if (have[c.title]) return;", "", "rebuilds change values only; a second run leaves three charts"),
            ("weeks starting on Sunday", "-((dow + 6) % 7)", "-dow", "weekly figures equal the raw tabs, from 31 Aug, 4,351 for w/c 19 Oct"),
            ("nothing marked partial", "var partial = ga4cAddDays_(m, 6) > yesterday || (firstDay !== null && firstDay > m);", "var partial = false;",
             "first and current weeks marked partial, complete weeks not"),
        ]
        for label, old, new, check in plants:
            if summary_src.count(old) != 1:
                fails += 1
                print("FAIL  plant '%s': the line to change is not in the script exactly once" % label)
                continue
            R2, err = run_harness(node, summary_src.replace(old, new), work, "plant", fx)
            caught = bool(err) or bool(checks(R2, daily, events)[check])
            if caught:
                print("PASS  plant caught: %s" % label)
            else:
                fails += 1
                print("FAIL  plant NOT caught: %s" % label)
        print("%s" % ("FAILED (%d)" % fails if fails else "all green"))
        return 1 if fails else 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
