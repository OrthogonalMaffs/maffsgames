#!/usr/bin/env python3
# ci-line: B3 | GA4 country Apps Script (mocked API and Sheet: replace-by-date is idempotent, other dates untouched, events tab never referenced; planted faults caught) |
"""Tests for docs/apps-script-ga4-country.js, the Apps Script that copies GA4's daily country figures into two
tabs of the events Sheet (Jon's ruling, 8 Oct 2026). No network: the script runs in Node's vm module against
mocks of AnalyticsData, SpreadsheetApp, DriveApp, Utilities, LockService, ScriptApp and Logger.

    python scripts/test-ga4-country.py

What it proves:
  (a) a re-run for the same dates leaves one set of rows: the daily run twice on one day gives the same tabs,
      every (date, country[, event]) appears once, and a window's rows are exactly what GA4 now says (a
      country GA4 no longer reports for a date is gone, not left behind);
  (b) dates outside the window are untouched, byte for byte, including when GA4 returns a stray row dated
      outside the window;
  (c) the events tab is never referenced: the mock spreadsheet records every access, the events tab is never
      reached, it stays the first tab, and the source never calls getActiveSheet, getSheets, deleteSheet,
      setActiveSheet or getSheetByName with anything but its own two tab names.
Also: the backfill covers 1 Sep 2026 to yesterday; the daily window is the last three complete UK days; the
request names property 528531831, the contract's metrics and the four events; pages are followed; a fetch
that returns nothing for a whole window is refused (rows kept); a tab whose row 1 is not this script's is not
overwritten; a failed API call writes nothing; dates stay text; the property check passes on the right
stream and fails on another; the trigger setup replaces only its own trigger; and no top-level name collides
with docs/apps-script-endpoint.js (both may share one Apps Script project).

Then four planted faults, each a one-line change to the script, and each must make its check fail: keeping
the window's old rows (a), dropping every old row (b), adding a tab at the front (c), and writing dates
without the text format.

Node: the runner's, or the copy the Playwright package ships (as verify-test-the-claim.py's CI line uses).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "docs", "apps-script-ga4-country.js")
ENDPOINT = os.path.join(ROOT, "docs", "apps-script-endpoint.js")

PROPERTY = "properties/528531831"
EVENTS = ["page_view", "game_started", "question_answered", "game_completed"]
DAILY_HEAD = ["date", "country", "activeUsers", "sessions", "engagedSessions", "eventCount"]
EVENTS_HEAD = ["date", "country", "eventName", "activeUsers", "eventCount"]
TABS = ("GA4 country daily", "GA4 country events")

HARNESS = r"""
'use strict';
const vm = require('vm');
const fs = require('fs');
const SRC = fs.readFileSync(process.argv[2], 'utf8');

// ---------- GA4 data the mock API serves ----------
const COUNTRIES = ['United Kingdom', 'United States', 'Ireland', 'India', '(not set)'];
const ALL_EVENTS = ['page_view', 'game_started', 'question_answered', 'game_completed',
                    'user_engagement', 'scroll', 'session_start'];
let VERSION = 1, ROGUE = false, EMPTY = false, FAIL_ON_CALL = 0;
function hash(s) { let h = 2166136261; for (const c of s) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619) >>> 0; } return h; }
function countriesOn(date) {
  // which countries visit on a date; version 2 drops India everywhere (a revised day can lose a row)
  return COUNTRIES.filter(c => (hash(date + c) % 5 !== 0) && !(VERSION === 2 && c === 'India'));
}
function n(seed, max) { return 1 + hash(seed + ':' + VERSION) % max; }
function dataRows(req) {
  const start = req.dateRanges[0].startDate, end = req.dateRanges[0].endDate;
  const dims = req.dimensions.map(d => d.name), mets = req.metrics.map(m => m.name);
  const filt = req.dimensionFilter ? req.dimensionFilter.filter.inListFilter.values : null;
  const rows = [];
  const dates = [];
  for (let d = new Date(start + 'T00:00:00Z'); d <= new Date(end + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + 1))
    dates.push(d.toISOString().slice(0, 10));
  if (ROGUE) dates.push('2026-09-15');       // GA4 answering for a date it was not asked for
  for (const date of dates) for (const c of countriesOn(date)) {
    const evs = dims.includes('eventName') ? ALL_EVENTS : [null];
    for (const ev of evs) {
      if (ev !== null && filt && !filt.includes(ev)) continue;
      const vals = { date: date.replace(/-/g, ''), country: c, eventName: ev };
      rows.push({
        dimensionValues: dims.map(x => ({ value: String(vals[x]) })),
        metricValues: mets.map(m => ({ value: String(n(date + c + ev + m, 900)) }))
      });
    }
  }
  return rows;
}
const REQUESTS = [];
let CALLS = 0;
const PAGE = 7;   // smaller than any real page, so every table needs several
const AnalyticsData = { Properties: { runReport(req, prop) {
  CALLS++;
  if (FAIL_ON_CALL && CALLS === FAIL_ON_CALL) throw new Error('Quota exceeded (mock)');
  REQUESTS.push({ req: JSON.parse(JSON.stringify(req)), prop });
  if (req.dimensions.some(d => d.name === 'streamId')) {
    return { rowCount: 2, rows: [
      { dimensionValues: [{ value: global.__STREAM }, { value: 'maffsgames.co.uk' }], metricValues: [{ value: '5000' }] },
      { dimensionValues: [{ value: global.__STREAM }, { value: 'www.maffsgames.co.uk' }], metricValues: [{ value: '3' }] }
    ] };
  }
  const all = EMPTY ? [] : dataRows(req);
  const take = Math.min(req.limit, PAGE);
  const page = all.slice(req.offset || 0, (req.offset || 0) + take);
  const resp = { rowCount: all.length, propertyQuota: { tokensPerDay: { remaining: 199000 } } };
  if (page.length) resp.rows = page;
  return resp;
} } };

// ---------- a spreadsheet that records every access ----------
const UNEXPECTED = [], ASKED = [], EVENTS_TOUCHED = [];
function isDate(v) { return Object.prototype.toString.call(v) === '[object Date]'; }
function makeSheet(name, rows) {
  const s = { name, cells: rows.map(r => r.slice()), fmt: {}, frozen: 0 };
  s.lastRow = () => { for (let i = s.cells.length; i > 0; i--) if (s.cells[i - 1].some(v => v !== '' && v !== undefined)) return i; return 0; };
  s.api = {
    getLastRow: () => s.lastRow(),
    setFrozenRows: k => { s.frozen = k; },
    getName: () => s.name,
    getRange(r, c, nr, nc) {
      nr = nr || 1; nc = nc || 1;
      const ensure = () => { while (s.cells.length < r + nr - 1) s.cells.push([]); };
      const rng = {
        getValues() { const out = []; for (let i = 0; i < nr; i++) { const row = s.cells[r - 1 + i] || []; const o = []; for (let j = 0; j < nc; j++) o.push(row[c - 1 + j] === undefined ? '' : row[c - 1 + j]); out.push(o); } return out; },
        setValues(v) {
          if (v.length !== nr || v.some(x => x.length !== nc)) throw new Error('setValues: shape ' + v.length + 'x' + (v[0] || []).length + ' into ' + nr + 'x' + nc);
          ensure();
          for (let i = 0; i < nr; i++) for (let j = 0; j < nc; j++) {
            let val = v[i][j];
            // real Sheets turns date-like text into a Date unless the cell is formatted as text
            if (typeof val === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(val) && s.fmt[(r + i) + ':' + (c + j)] !== '@')
              val = new Date(val + 'T00:00:00+01:00');
            (s.cells[r - 1 + i] = s.cells[r - 1 + i] || [])[c - 1 + j] = val;
          }
          return rng;
        },
        clearContent() { for (let i = 0; i < nr; i++) { const row = s.cells[r - 1 + i]; if (row) for (let j = 0; j < nc; j++) row[c - 1 + j] = ''; } return rng; },
        setNumberFormat(f) { for (let i = 0; i < nr; i++) for (let j = 0; j < nc; j++) s.fmt[(r + i) + ':' + (c + j)] = f; return rng; },
        setFontWeight() { return rng; }
      };
      return rng;
    }
  };
  return s;
}
function recordingProxy(target, label, log) {
  return new Proxy(target, { get(t, k) {
    if (typeof k === 'symbol') return t[k];
    if (!(k in t)) { log.push(label + '.' + String(k)); throw new Error('unexpected access ' + label + '.' + String(k)); }
    return t[k];
  } });
}
function makeSpreadsheet() {
  const events = makeSheet('Sheet1', [['timestamp', 'event', 'game_slug'], ['2026-10-07T09:00:00Z', 'game_started', 'split-it']]);
  const dash = makeSheet('Dashboard', [['MaffsGames Dashboard']]);
  const sheets = [events, dash];
  const eventsProxy = new Proxy({}, { get(t, k) { EVENTS_TOUCHED.push(String(k)); throw new Error('events tab touched: ' + String(k)); } });
  const ss = {
    getSheetByName(name) { ASKED.push(name); const s = sheets.find(x => x.name === name); if (!s) return null; return s === events ? eventsProxy : s.api; },
    insertSheet(name, idx) { const s = makeSheet(name, []); sheets.splice(idx === undefined ? 1 : idx, 0, s); return s.api; },
    getNumSheets: () => sheets.length,
    getSpreadsheetTimeZone: () => 'Europe/London'
  };
  return { sheets, events, proxy: recordingProxy(ss, 'spreadsheet', UNEXPECTED) };
}
let SS = makeSpreadsheet();

// ---------- the rest of Apps Script ----------
const LOG = [];
const TRIGGERS = [];
function trig(fn, hour, tz) { return { fn, hour, tz, getHandlerFunction: () => fn }; }
const ctx = {
  AnalyticsData,
  SpreadsheetApp: recordingProxy({ getActiveSpreadsheet: () => global.__BOUND ? SS.proxy : null, open: f => f.ss }, 'SpreadsheetApp', UNEXPECTED),
  DriveApp: recordingProxy({ getFilesByName(nm) { let left = nm === 'MaffsGames Events' ? 1 : 0; return { hasNext: () => left > 0, next: () => { left--; return { ss: SS.proxy }; } }; } }, 'DriveApp', UNEXPECTED),
  Utilities: { formatDate(d, tz, fmt) {
    if (fmt !== 'yyyy-MM-dd') throw new Error('format ' + fmt);
    return new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
  } },
  LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
  Logger: { log: m => LOG.push(String(m)) },
  ScriptApp: {
    getProjectTriggers: () => TRIGGERS.slice(),
    deleteTrigger: t => { TRIGGERS.splice(TRIGGERS.indexOf(t), 1); },
    newTrigger(fn) { const b = { hour: null, tz: null,
      timeBased: () => b, atHour: h => { b.hour = h; return b; }, everyDays: () => b,
      inTimezone: z => { b.tz = z; return b; }, create: () => { TRIGGERS.push(trig(fn, b.hour, b.tz)); } }; return b; }
  }
};
vm.createContext(ctx);
vm.runInContext(SRC, ctx, { filename: 'apps-script-ga4-country.js' });
global.__BOUND = false;
global.__STREAM = '13911036386';

function setNow(iso) { vm.runInContext('ga4cNow_ = function () { return new Date(' + JSON.stringify(iso) + '); };', ctx); }
function run(fn) { try { vm.runInContext(fn + '()', ctx); return null; } catch (e) { return String(e && e.message || e); } }
function snap() {
  const out = { order: SS.sheets.map(s => s.name), tabs: {} };
  for (const s of SS.sheets) if (s !== SS.events) out.tabs[s.name] = s.cells.filter(r => r.some(v => v !== '' && v !== undefined)).map(r => r.map(v => isDate(v) ? { date: v.toISOString() } : v));
  out.eventsCells = JSON.parse(JSON.stringify(SS.events.cells));
  return out;
}
function expected(start, end) {   // what GA4 (this version) says for start..end, through the real request shape
  const tables = vm.runInContext('GA4C_TABLES', ctx);
  return tables.map(t => {
    const req = { dateRanges: [{ startDate: start, endDate: end }], dimensions: t.dimensions.map(n => ({ name: n })),
      metrics: t.metrics.map(n => ({ name: n })) };
    if (t.eventFilter) req.dimensionFilter = { filter: { inListFilter: { values: vm.runInContext('GA4C_EVENTS', ctx) } } };
    return dataRows(req).map(r => { const d = r.dimensionValues.map(x => x.value); d[0] = d[0].slice(0, 4) + '-' + d[0].slice(4, 6) + '-' + d[0].slice(6); return d.concat(r.metricValues.map(m => Number(m.value))); });
  });
}

const R = { steps: {} };
function step(name, fn) { REQUESTS.length = 0; const err = run(fn); R.steps[name] = { error: err, snap: snap(), requests: JSON.parse(JSON.stringify(REQUESTS)) }; }

// 1. backfill on 8 Oct 2026, 06:00 UK
setNow('2026-10-08T05:00:00Z'); VERSION = 1;
step('backfill', 'ga4CountryBackfill');
R.expectBackfill = expected('2026-09-01', '2026-10-07');
// 2. GA4 revises: the daily run on the same morning, then again
VERSION = 2;
step('daily1', 'ga4CountryDaily');
R.expectDailyWindow = expected('2026-10-05', '2026-10-07');
step('daily2', 'ga4CountryDaily');
// 3. next morning, and GA4 slips in a row dated 15 Sep
setNow('2026-10-09T05:00:00Z'); ROGUE = true;
step('daily3', 'ga4CountryDaily');
ROGUE = false;
// 4. GA4 returns nothing for the whole window
EMPTY = true;
step('emptyRefused', 'ga4CountryDaily');
EMPTY = false;
// 5. the second report fails (quota): nothing written
CALLS = 0; FAIL_ON_CALL = 2;
step('apiFails', 'ga4CountryDaily');
FAIL_ON_CALL = 0;
// 6. the script bound to the Sheet (getActiveSpreadsheet) behaves the same
global.__BOUND = true;
step('bound', 'ga4CountryDaily');
global.__BOUND = false;
// 7. a tab of that name that is not this script's
SS = makeSpreadsheet();
SS.sheets.push(makeSheet('GA4 country daily', [['Jon notes', 'x'], ['keep', 'me']]));
step('foreignTab', 'ga4CountryDaily');
// 8. the property check
step('checkOk', 'ga4CountryCheckProperty');
global.__STREAM = '99999999999';
step('checkWrong', 'ga4CountryCheckProperty');
// 9. the trigger
TRIGGERS.push(trig('sendDailyReport', 7, 'Europe/London'), trig('ga4CountryDaily', 3, 'UTC'), trig('ga4CountryDaily', 4, 'UTC'));
R.triggerError = run('ga4CountrySetupTrigger');
R.triggers = TRIGGERS.map(t => ({ fn: t.fn, hour: t.hour, tz: t.tz }));

R.unexpected = UNEXPECTED; R.asked = Array.from(new Set(ASKED)); R.eventsTouched = EVENTS_TOUCHED;
process.stdout.write(JSON.stringify(R));
"""


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


def run_harness(node, source, workdir, tag):
    src_path = os.path.join(workdir, "script-%s.js" % tag)
    harness = os.path.join(workdir, "harness.js")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(source)
    if not os.path.exists(harness):
        with open(harness, "w", encoding="utf-8") as f:
            f.write(HARNESS)
    p = subprocess.run([node, harness, src_path], capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout), None


def tab(st, name):
    return st["snap"]["tabs"].get(name, [])


def body(rows):
    return rows[1:]


def day(v):
    """A date cell as a key; a cell Sheets turned into a Date (the mock's {"date": ...}) matches no window."""
    return v if isinstance(v, str) else json.dumps(v)


def outside(rows, window):
    return [r for r in body(rows) if day(r[0]) not in window]


def inside(rows, window):
    return [r for r in body(rows) if day(r[0]) in window]


def checks(R):
    """Every check, by name: a list of failure strings (empty = pass)."""
    out = {}
    s = R["steps"]
    bf, d1, d2, d3 = s["backfill"], s["daily1"], s["daily2"], s["daily3"]
    w1 = {"2026-10-05", "2026-10-06", "2026-10-07"}
    w3 = {"2026-10-06", "2026-10-07", "2026-10-08"}

    f = []
    for st_name in ("backfill", "daily1", "daily2", "daily3"):
        if s[st_name]["error"]:
            f.append("%s raised: %s" % (st_name, s[st_name]["error"]))
    out["runs without error"] = f

    # dates stay text (a Date in column A means the text format was not applied before writing)
    f = []
    for st_name in ("backfill", "daily1", "daily3"):
        for t in TABS:
            for r in body(tab(s[st_name], t)):
                if not isinstance(r[0], str):
                    f.append("%s %s: date cell %r is not text" % (st_name, t, r[0]))
                    break
    out["dates stay text"] = f

    # headers and the backfill's content
    f = []
    if tab(bf, TABS[0])[:1] != [DAILY_HEAD]:
        f.append("daily tab row 1 is %r" % (tab(bf, TABS[0])[:1],))
    if tab(bf, TABS[1])[:1] != [EVENTS_HEAD]:
        f.append("events tab row 1 is %r" % (tab(bf, TABS[1])[:1],))
    for i, t in enumerate(TABS):
        got = sorted(map(json.dumps, body(tab(bf, t))))
        want = sorted(map(json.dumps, R["expectBackfill"][i]))
        if got != want:
            f.append("backfill %s: %d rows, GA4 has %d (or they differ)" % (t, len(got), len(want)))
        dates = {day(r[0]) for r in body(tab(bf, t))}
        if min(dates, default="") != "2026-09-01" or max(dates, default="") != "2026-10-07":
            f.append("backfill %s covers %s..%s, not 2026-09-01..2026-10-07" % (t, min(dates, default=None), max(dates, default=None)))
    out["backfill: 1 Sep to yesterday, exactly GA4's rows"] = f

    # requests: property, window, metrics, events, paging
    f = []
    for st_name, window in (("backfill", ("2026-09-01", "2026-10-07")), ("daily1", ("2026-10-05", "2026-10-07")),
                            ("daily3", ("2026-10-06", "2026-10-08"))):
        reqs = s[st_name]["requests"]
        if not reqs:
            f.append("%s made no request" % st_name)
        for q in reqs:
            if q["prop"] != PROPERTY:
                f.append("%s asked %s" % (st_name, q["prop"]))
            dr = q["req"]["dateRanges"][0]
            if (dr["startDate"], dr["endDate"]) != window:
                f.append("%s asked %s..%s, not %s..%s" % ((st_name, dr["startDate"], dr["endDate"]) + window))
        dims = {tuple(d["name"] for d in q["req"]["dimensions"]) for q in reqs}
        if dims != {("date", "country"), ("date", "country", "eventName")}:
            f.append("%s dimensions %r" % (st_name, dims))
        for q in reqs:
            mets = [m["name"] for m in q["req"]["metrics"]]
            ev = [d["name"] for d in q["req"]["dimensions"]] == ["date", "country", "eventName"]
            if mets != (EVENTS_HEAD[3:] if ev else DAILY_HEAD[2:]):
                f.append("%s metrics %r" % (st_name, mets))
            if ev and q["req"].get("dimensionFilter", {}).get("filter", {}).get("inListFilter", {}).get("values") != EVENTS:
                f.append("%s event filter %r" % (st_name, q["req"].get("dimensionFilter")))
            if not ev and "dimensionFilter" in q["req"]:
                f.append("%s filtered the daily table" % st_name)
        offsets = sorted({q["req"]["offset"] for q in reqs})
        if len(reqs) <= 2 or offsets[:2] != [0, 7]:
            f.append("%s did not page through the report (offsets %r)" % (st_name, offsets[:4]))
    out["requests: property 528531831, window, metrics, the four events, paging"] = f

    # (a) idempotent replace-by-date
    f = []
    for t in TABS:
        if tab(d1, t) != tab(d2, t):
            f.append("%s: a second daily run on the same day changed the tab" % t)
        keyw = 3 if t == TABS[1] else 2
        keys = [json.dumps(r[:keyw]) for r in body(tab(d2, t))]
        if len(keys) != len(set(keys)):
            f.append("%s: %d rows duplicate a (date, country[, event])" % (t, len(keys) - len(set(keys))))
    for i, t in enumerate(TABS):
        got = sorted(map(json.dumps, inside(tab(d1, t), w1)))
        want = sorted(map(json.dumps, R["expectDailyWindow"][i]))
        if got != want:
            f.append("%s: window rows after the daily run are not GA4's revised rows (%d vs %d)" % (t, len(got), len(want)))
        if any(r[1] == "India" for r in inside(tab(d1, t), w1)):
            f.append("%s: a country GA4 no longer reports in the window was left behind" % t)
    out["(a) a re-run for the same dates leaves one set of rows"] = f

    # (b) dates outside the window untouched
    f = []
    for t in TABS:
        if outside(tab(bf, t), w1) != outside(tab(d1, t), w1):
            f.append("%s: rows outside 5-7 Oct changed in the daily run" % t)
        if outside(tab(d2, t), w3) != outside(tab(d3, t), w3):
            f.append("%s: rows outside 6-8 Oct changed when GA4 sent a stray 15 Sep row" % t)
        if not outside(tab(d1, t), w1):
            f.append("%s: no rows outside the window to compare" % t)
    out["(b) dates outside the window are untouched"] = f

    # (c) the events tab is never referenced
    f = []
    if R["eventsTouched"]:
        f.append("the events tab was accessed: %r" % R["eventsTouched"][:5])
    if R["unexpected"]:
        f.append("unexpected Apps Script calls: %r" % sorted(set(R["unexpected"])))
    stray = [a for a in R["asked"] if a not in TABS]
    if stray:
        f.append("getSheetByName asked for %r" % stray)
    for st_name in ("backfill", "daily3"):
        order = s[st_name]["snap"]["order"]
        if order[:2] != ["Sheet1", "Dashboard"]:
            f.append("%s: tab order is %r (the events tab must stay first, others unmoved)" % (st_name, order))
        if s[st_name]["snap"]["eventsCells"] != s["backfill"]["snap"]["eventsCells"]:
            f.append("%s: the events tab's cells changed" % st_name)
    if set(s["backfill"]["snap"]["order"]) != {"Sheet1", "Dashboard"} | set(TABS):
        f.append("tabs after the backfill: %r" % s["backfill"]["snap"]["order"])
    src = open(SCRIPT, encoding="utf-8").read()
    for call in ("getActiveSheet", "getSheets", "deleteSheet", "setActiveSheet", "getSheetId", "getSheetByName("):
        for m in re.finditer(re.escape(call), src):
            if call == "getSheetByName(" and src[m.end():m.end() + 10] == "table.tab)":
                continue
            f.append("source calls %s (line %d)" % (call, src.count("\n", 0, m.start()) + 1))
    out["(c) the events tab is never referenced"] = f

    # refusals and failures write nothing
    f = []
    if not s["emptyRefused"]["error"] or "no rows" not in s["emptyRefused"]["error"]:
        f.append("an empty GA4 window was not refused (%r)" % s["emptyRefused"]["error"])
    if s["emptyRefused"]["snap"]["tabs"] != d3["snap"]["tabs"]:
        f.append("an empty GA4 window changed the tabs")
    if not s["apiFails"]["error"] or "Quota" not in s["apiFails"]["error"]:
        f.append("the failed API call was not reported (%r)" % s["apiFails"]["error"])
    if s["apiFails"]["snap"]["tabs"] != d3["snap"]["tabs"]:
        f.append("a failed API call still wrote to the tabs")
    if s["bound"]["error"] or s["bound"]["snap"]["tabs"] != d3["snap"]["tabs"]:
        f.append("bound to the Sheet, a same-day re-run gave different tabs (%r)" % s["bound"]["error"])
    ft = s["foreignTab"]
    if not ft["error"] or "not overwriting" not in ft["error"]:
        f.append("a tab with someone else's row 1 was not refused (%r)" % ft["error"])
    if ft["snap"]["tabs"].get("GA4 country daily") != [["Jon notes", "x"], ["keep", "me"]]:
        f.append("a tab with someone else's row 1 was changed")
    out["refusals and failures write nothing"] = f

    # property check and trigger
    f = []
    if s["checkOk"]["error"]:
        f.append("the property check failed on the right stream: %s" % s["checkOk"]["error"])
    if not s["checkWrong"]["error"] or "13911036386" not in s["checkWrong"]["error"]:
        f.append("the property check passed on another stream")
    want = [{"fn": "sendDailyReport", "hour": 7, "tz": "Europe/London"},
            {"fn": "ga4CountryDaily", "hour": 6, "tz": "Europe/London"}]
    if R["triggerError"] or R["triggers"] != want:
        f.append("triggers after setup: %r (%r)" % (R["triggers"], R["triggerError"]))
    out["property check; trigger setup replaces only its own trigger"] = f
    return out


def top_level_names(path):
    names = set()
    for line in open(path, encoding="utf-8"):
        m = re.match(r"(?:function\s+([A-Za-z_$][\w$]*)|(?:const|let|var)\s+([A-Za-z_$][\w$]*))", line)
        if m:
            names.add(m.group(1) or m.group(2))
    return names


# (name, the line it changes, the change, the check that must fail)
FAULTS = [
    ("keep the window's old rows", "var kept = rows.filter(function (r) { return !inWindow[ga4cCellDate_(r[0], tz)]; });",
     "var kept = rows;", "(a) a re-run for the same dates leaves one set of rows"),
    ("drop every old row", "var kept = rows.filter(function (r) { return !inWindow[ga4cCellDate_(r[0], tz)]; });",
     "var kept = [];", "(b) dates outside the window are untouched"),
    ("add a tab at the front", "ss.insertSheet(table.tab, ss.getNumSheets())",
     "ss.insertSheet(table.tab, 0)", "(c) the events tab is never referenced"),
    ("write dates without the text format",
     "tab.getRange(1, 1, Math.max(last, merged.length + 1), 1).setNumberFormat('@');", "", "dates stay text"),
]


def main():
    node = find_node()
    source = open(SCRIPT, encoding="utf-8").read()
    failed = 0
    with tempfile.TemporaryDirectory() as work:
        R, err = run_harness(node, source, work, "real")
        if R is None:
            print("FAIL  the harness did not run: %s" % err)
            return 1
        for name, fails in checks(R).items():
            print(("PASS  " if not fails else "FAIL  ") + name)
            for x in fails:
                print("        " + x)
            failed += bool(fails)

        mine, theirs = top_level_names(SCRIPT), top_level_names(ENDPOINT)
        clash = sorted(mine & theirs)
        unprefixed = sorted(n for n in mine if not re.match(r"(GA4C_|ga4c|ga4Country)", n))
        ok = not clash and not unprefixed and len(mine) > 10
        print(("PASS  " if ok else "FAIL  ") + "no top-level name shared with apps-script-endpoint.js (%d names)" % len(mine))
        if clash:
            print("        shared: %s" % ", ".join(clash))
        if unprefixed:
            print("        not prefixed GA4C_/ga4c/ga4Country: %s" % ", ".join(unprefixed))
        failed += not ok

        for i, (name, old, new, must_fail) in enumerate(FAULTS):
            if source.count(old) != 1:
                print("FAIL  planted fault '%s': its line is not in the script exactly once; update FAULTS" % name)
                failed += 1
                continue
            Rf, err = run_harness(node, source.replace(old, new), work, "fault%d" % i)
            caught = Rf is not None and checks(Rf)[must_fail]
            print(("PASS  " if caught else "FAIL  ") + "planted fault '%s' is caught by '%s'" % (name, must_fail))
            failed += not caught

    print("\n%s" % ("all checks pass" if not failed else "%d check(s) failed" % failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
