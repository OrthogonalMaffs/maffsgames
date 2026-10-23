# ci-deps: docs/apps-script-counts.js docs/apps-script-counts.appsscript.json
"""Does the counts Apps Script (docs/apps-script-counts.js) count what the contract says it counts, with only the
read-only Sheets scope?

The script cannot run in CI (it needs Google's services), and Node is not installed on the Windows machine, so
this loads the file's own source into Chromium behind small fakes of the Apps Script services it uses
(the Sheets advanced service, PropertiesService, CacheService, LockService, Utilities, ContentService) and drives it.
SpreadsheetApp is a trap: openById needs the full read-write scope (it failed at deploy, 23 Oct 2026, with only
spreadsheets.readonly granted), so any call to it, or to DriveApp, ScriptApp or UrlFetchApp, fails this test.

  - the manifest: oauthScopes is exactly spreadsheets.readonly, and the Sheets v4 advanced service is switched on;
  - the period: 1 September of the school year, Europe/London, restarting on 1 September;
  - only question_answered rows, per game_slug, with event time on or after the period start;
  - the browser's clock when it agrees with arrival within a day, else arrival; a date cell (a serial number on the
    spreadsheet's clock) is read as the right instant;
  - incremental: a second run reads only the rows added since (and finds the period start by binary search,
    reading none of the older rows); trailing blank grid rows are not data;
  - chunked and time-boxed: a run cut off loses nothing, resumes, and as_of stays null until every row is read;
  - a new school year, or rows deleted from under the stored place, starts the count again;
  - a held lock skips the run; doGet serves the 60-second cache and ?version=1;
  - the payload is {as_of, since, total, games} with total = the sum of games.

    python scripts/test-apps-script-counts.py
"""
import asyncio, json, pathlib, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
SRC = BASE / "docs" / "apps-script-counts.js"
MANIFEST = BASE / "docs" / "apps-script-counts.appsscript.json"

HARNESS = r"""
(src) => {
  const out = [];
  const ok = (name, cond, detail) => out.push([name, !!cond, cond ? '' : String(detail === undefined ? '' : detail)]);

  // ---- London time from Intl, enough of Utilities for the formats the script uses
  const parts = (d, tz) => Object.fromEntries(new Intl.DateTimeFormat('en-GB', { timeZone: tz, hourCycle: 'h23',
    year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' })
    .formatToParts(d).map(p => [p.type, p.value]));
  const pad = (n, w = 2) => String(n).padStart(w, '0');
  const offsetMin = (d, tz) => { const p = parts(d, tz);
    return Math.round((Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second) - Math.floor(d.getTime() / 1000) * 1000) / 60000); };
  const Utilities = {
    formatDate(d, tz, fmt) {
      const p = parts(d, tz), o = offsetMin(d, tz);
      const sign = o < 0 ? '-' : '+', a = Math.abs(o);
      if (fmt === 'yyyy-MM-dd HH:mm:ss') return `${p.year}-${pad(p.month)}-${pad(p.day)} ${pad(p.hour)}:${pad(p.minute)}:${pad(p.second)}`;
      return fmt.replace("yyyy-MM-dd'T'HH:mm:ssXXX", `${p.year}-${pad(p.month)}-${pad(p.day)}T${pad(p.hour)}:${pad(p.minute)}:${pad(p.second)}${sign}${pad(Math.floor(a / 60))}:${pad(a % 60)}`)
                .replace('yyyy', p.year).replace(/^M$/, p.month);
    },
    parseDate(s, tz) {   // 'yyyy-MM-dd HH:mm:ss' read as wall-clock time in tz
      const m = s.match(/(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)/).slice(1).map(Number);
      const guess = new Date(Date.UTC(m[0], m[1] - 1, m[2], m[3], m[4], m[5]));
      let d = new Date(guess.getTime() - offsetMin(guess, tz) * 60000);
      d = new Date(guess.getTime() - offsetMin(d, tz) * 60000);
      return d;
    },
  };

  const NAME = 'MaffsGames Events';
  const HEAD = ['timestamp', 'event', 'game_slug', 'level', 'mode', 'question_index', 'correct', 'attempts', 'score',
    'questions_answered', 'questions_correct', 'previous_score', 'difficulty', 'filter_type', 'filter_value', 'client_ts', 'seq'];
  const colNum = s => s.split('').reduce((n, ch) => n * 26 + ch.charCodeAt(0) - 64, 0);
  const trap = what => new Proxy({}, { get(_, k) { throw new Error(what + '.' + String(k) + ' called: it needs a wider scope than read-only'); } });

  function makeEnv(rows, extraBlankRows = 50) {
    const env = { rows: [HEAD].concat(rows), reads: [], props: {}, cache: {}, locked: false, clock: 0, extra: extraBlankRows, calls: [] };
    const grid = () => env.rows.length + env.extra;                   // the grid is taller than the data
    const get = (id, range, opts) => {
      env.calls.push('values.get ' + range);
      if (!opts || opts.valueRenderOption !== 'UNFORMATTED_VALUE') throw new Error('valueRenderOption must be UNFORMATTED_VALUE');
      const m = range.match(/^'(.+)'!(?:([A-Z]+)(\d+)(?::([A-Z]+)(\d+))?|(\d+):(\d+))$/);
      if (!m || m[1] !== NAME) throw new Error('bad range ' + range);
      let r1, r2, c1, c2;
      if (m[6]) { r1 = +m[6]; r2 = +m[7]; c1 = 1; c2 = HEAD.length; }
      else { c1 = colNum(m[2]); r1 = +m[3]; c2 = m[4] ? colNum(m[4]) : c1; r2 = m[5] ? +m[5] : r1; }
      if (r2 > grid()) throw new Error('range ' + range + ' exceeds grid limits');
      let vals = [];
      for (let r = r1; r <= r2; r++) vals.push((env.rows[r - 1] || []).slice(c1 - 1, c2));
      // the API leaves off trailing empty cells in a row, and trailing empty rows
      vals = vals.map(row => { const x = row.slice(); while (x.length && x[x.length - 1] === '') x.pop(); return x; });
      while (vals.length && vals[vals.length - 1].length === 0) vals.pop();
      env.reads.push([r1, vals.length]);
      return vals.length ? { range, majorDimension: 'ROWS', values: vals } : { range, majorDimension: 'ROWS' };
    };
    env.services = {
      Sheets: { Spreadsheets: {
        get: (id, opts) => { env.calls.push('spreadsheets.get'); return { properties: { timeZone: 'Europe/London' },
          sheets: [{ properties: { title: 'Dashboard', gridProperties: { rowCount: 10 } } },
                   { properties: { title: NAME, gridProperties: { rowCount: grid() } } }] }; },
        Values: { get } } },
      SpreadsheetApp: trap('SpreadsheetApp'), DriveApp: trap('DriveApp'), ScriptApp: trap('ScriptApp'), UrlFetchApp: trap('UrlFetchApp'),
      PropertiesService: { getScriptProperties: () => ({
        getProperties: () => Object.assign({}, env.props),
        setProperties: (p, del) => { if (del) env.props = {}; Object.assign(env.props, p); },
        deleteProperty: k => { delete env.props[k]; },
        deleteAllProperties: () => { env.props = {}; } }) },
      CacheService: { getScriptCache: () => ({ get: k => env.cache[k] || null, put: (k, v) => { env.cache[k] = v; }, remove: k => { delete env.cache[k]; } }) },
      LockService: { getScriptLock: () => ({ tryLock: () => !env.locked, releaseLock: () => {} }) },
      ContentService: { MimeType: { JSON: 'json' }, createTextOutput: t => ({ text: t, setMimeType() { return this; } }) },
      Utilities,
    };
    return env;
  }
  function load(env, patch) {
    let s = src;
    if (patch) s = patch(s);
    s = s.replace(/Date\.now\(\)/g, '__clock()');
    const names = Object.keys(env.services);
    const f = new Function(...names, 'console', '__clock',
      s + '\nreturn {updateCounts_, tally_, eventTime_, sinceString_, startRow_, columns_, doGet, payload_, loadState_, resetCounts, updateCounts, backfill};');
    return f(...names.map(n => env.services[n]), { log() {}, error() {} }, () => (env.clock += 100));
  }
  const row = (arrival, event, slug, clientTs) => {
    const r = new Array(HEAD.length).fill('');
    r[0] = arrival; r[1] = event; r[2] = slug; if (clientTs) r[15] = clientTs; return r;
  };
  const QA = 'question_answered';
  const NOW_OCT = new Date('2026-10-23T12:00:00Z');
  const serial = (y, mo, d, h, mi) => (Date.UTC(y, mo - 1, d, h, mi) - Date.UTC(1899, 11, 30)) / 86400000;   // wall-clock reading
  const bulk = env => env.reads.filter(r => r[1] > 1).reduce((s, r) => s + r[1], 0);

  // ---- the period
  {
    const g = load(makeEnv([]));
    ok('period: 23 Oct 2026 -> 2026-09-01', g.sinceString_(NOW_OCT) === '2026-09-01', g.sinceString_(NOW_OCT));
    ok('period: 31 Aug 2027 23:30 London -> still 2026-09-01', g.sinceString_(new Date('2027-08-31T22:30:00Z')) === '2026-09-01');
    ok('period: 1 Sep 2027 00:30 London -> 2027-09-01', g.sinceString_(new Date('2027-08-31T23:30:00Z')) === '2027-09-01');
    ok('period: January 2027 -> 2026-09-01', g.sinceString_(new Date('2027-01-15T12:00:00Z')) === '2026-09-01');
  }

  // ---- what counts
  {
    const env = makeEnv([
      row('2026-08-20T10:00:00Z', QA, 'old-game'),                                       // before the period
      row('2026-09-01T09:00:00Z', QA, 'a'),
      row('2026-09-01T09:00:01Z', 'game_started', 'a'),                                  // not a question
      row('2026-09-02T09:00:00Z', QA, 'a'),
      row('2026-09-02T09:00:01Z', QA, 'b'),
      row('2026-09-02T09:00:02Z', QA, ''),                                               // no slug
      row('2026-09-03T09:00:00Z', QA, 'b', '2020-01-01T00:00:00.000Z'),                  // wrong device clock: arrival wins
      row('2026-09-01T00:30:00Z', QA, 'c', '2026-08-31T22:30:00.000Z'),                  // stamped before 1 Sept 00:00 BST
      row('2026-09-01T00:30:00Z', QA, 'c', '2026-08-31T23:30:00.000Z'),                  // stamped after it
      row(serial(2026, 9, 4, 9, 0), QA, 'a'),                                            // a date cell: a serial number
      row(serial(2026, 9, 1, 0, 30), QA, 'd'),                                           // 00:30 London 1 Sept: counted
      row(serial(2026, 8, 31, 23, 30), QA, 'd'),                                         // 23:30 London 31 Aug: not counted
    ]);
    const g = load(env);
    g.updateCounts_(1e9, 0);
    const st = g.loadState_();
    ok('counts: per game, only question_answered, only from 1 Sept (text and date cells)',
       JSON.stringify(st.counts) === JSON.stringify({ a: 3, b: 2, c: 1, d: 1 }), JSON.stringify(st.counts));
    const p = g.payload_(st, NOW_OCT);
    ok('payload: total is the sum of games', p.total === 7 && Object.values(p.games).reduce((x, y) => x + y, 0) === 7, JSON.stringify(p));
    ok('payload: exactly as_of, since, total, games', JSON.stringify(Object.keys(p).sort()) === '["as_of","games","since","total"]', Object.keys(p));
    ok('payload: caught up gives a dated as_of', /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d$/.test(p.as_of), p.as_of);
    ok('reads: only the Sheets advanced service was used (no SpreadsheetApp, DriveApp, ScriptApp, UrlFetchApp)',
       env.calls.length > 0 && env.calls.every(c => /^(values\.get|spreadsheets\.get)/.test(c)), env.calls.slice(0, 3));
  }

  // ---- incremental
  {
    const pre = []; for (let i = 0; i < 400; i++) pre.push(row(new Date(Date.UTC(2026, 7, 1) + i * 3600000).toISOString(), QA, 'old'));
    const inP = []; for (let i = 0; i < 50; i++) inP.push(row(new Date(Date.UTC(2026, 8, 5) + i * 60000).toISOString(), QA, 'x'));
    const env = makeEnv(pre.concat(inP));
    const g = load(env);
    g.updateCounts_(1e9, 0);
    ok('incremental: first run reads only the period (the 400 older rows are found by binary search, not read)',
       bulk(env) <= 60 && g.loadState_().counts.x === 50, 'read ' + bulk(env) + ' ' + JSON.stringify(g.loadState_().counts));
    env.reads.length = 0;
    for (let i = 0; i < 7; i++) env.rows.push(row(new Date(Date.UTC(2026, 8, 6) + i * 60000).toISOString(), QA, 'x'));
    g.updateCounts_(1e9, 0);
    ok('incremental: the next run reads only the 7 new rows and adds them', bulk(env) === 7 && g.loadState_().counts.x === 57,
       'read ' + bulk(env) + ' ' + JSON.stringify(g.loadState_().counts));
    env.reads.length = 0;
    g.updateCounts_(1e9, 0);
    ok('incremental: a run with nothing new reads no rows', bulk(env) === 0 && g.loadState_().counts.x === 57, bulk(env));
    ok('incremental: the empty grid below the data is never counted or tripped over', g.loadState_().lastRow === 458, g.loadState_().lastRow);
  }

  // ---- chunked and time-boxed
  {
    const rows = []; for (let i = 0; i < 25; i++) rows.push(row(new Date(Date.UTC(2026, 8, 5) + i * 60000).toISOString(), QA, 'x'));
    const env = makeEnv(rows);
    const g = load(env, s => s.replace('const CHUNK_ROWS = 5000;', 'const CHUNK_ROWS = 10;'));
    g.updateCounts_(150, 0);        // the fake clock moves 100 ms a call: one chunk, then out of budget
    let st = g.loadState_();
    ok('budget: a cut-off run keeps what it read', st.counts.x === 10 && st.lastRow === 11 && st.asOf === null, JSON.stringify(st));
    ok('budget: the payload has as_of null while the count is incomplete', g.payload_(st, NOW_OCT).as_of === null);
    g.updateCounts_(1e9, 0);
    st = g.loadState_();
    ok('budget: the next run resumes and finishes without double-counting', st.counts.x === 25 && st.asOf !== null, JSON.stringify(st));
  }

  // ---- new school year; rows deleted
  {
    const env = makeEnv([row('2026-10-01T10:00:00Z', QA, 'x'), row('2027-09-02T10:00:00Z', QA, 'y')]);
    const g = load(env);
    g.updateCounts_(1e9, 0);
    ok('year: the count for 2026-09-01', g.loadState_().since === '2026-09-01' && g.loadState_().counts.x === 1, JSON.stringify(g.loadState_()));
    const g2 = load(env, s => s.replace('new Date();\n    var sinceStr', 'new Date("2027-09-10T12:00:00Z");\n    var sinceStr'));
    g2.updateCounts_(1e9, 0);
    const st = g2.loadState_();
    ok('year: on 1 September the counts restart', st.since === '2027-09-01' && JSON.stringify(st.counts) === '{"y":1}', JSON.stringify(st));
  }
  {
    const env = makeEnv([row('2026-10-01T10:00:00Z', QA, 'x'), row('2026-10-01T10:00:01Z', QA, 'x'), row('2026-10-01T10:00:02Z', QA, 'x')]);
    const g = load(env);
    g.updateCounts_(1e9, 0);
    env.rows.splice(1, 1);          // a row deleted from the top: every stored row number now points one row late
    g.updateCounts_(1e9, 0);
    ok('rows deleted: counted again from the start, not left stale', g.loadState_().counts.x === 2, JSON.stringify(g.loadState_().counts));
  }

  // ---- lock, doGet, cache
  {
    const env = makeEnv([row('2026-10-01T10:00:00Z', QA, 'x')]);
    const g = load(env);
    env.locked = true;
    g.updateCounts_(1e9, 0);
    ok('lock: a held lock skips the run and changes nothing', JSON.stringify(g.loadState_().counts) === '{}');
    env.locked = false;
    const first = JSON.parse(g.doGet({ parameter: {} }).text);
    ok('doGet: counts on a cache miss', first.total === 1 && first.games.x === 1, JSON.stringify(first));
    env.rows.push(row('2026-10-01T10:00:05Z', QA, 'x'));
    const second = JSON.parse(g.doGet({ parameter: {} }).text);
    ok('doGet: serves the cached payload for 60 s', second.total === 1, JSON.stringify(second));
    ok('doGet: ?version=1 says which code is live', /^\d{4}-\d\d-\d\d-[a-z]$/.test(JSON.parse(g.doGet({ parameter: { version: '1' } }).text).version));
  }
  return out;
}
"""


async def main():
    from playwright.async_api import async_playwright
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    adv = (manifest.get("dependencies") or {}).get("enabledAdvancedServices")
    src = SRC.read_text(encoding="utf-8")
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("//"))
    results = [("manifest: the only OAuth scope is spreadsheets.readonly",
                manifest.get("oauthScopes") == ["https://www.googleapis.com/auth/spreadsheets.readonly"], str(manifest.get("oauthScopes"))),
               ("manifest: the Sheets v4 advanced service is switched on as `Sheets`",
                adv == [{"userSymbol": "Sheets", "serviceId": "sheets", "version": "v4"}], str(adv)),
               ("manifest: Europe/London, web app runs as the deployer, open to anyone",
                manifest.get("timeZone") == "Europe/London" and manifest.get("webapp") == {"executeAs": "USER_DEPLOYING", "access": "ANYONE_ANONYMOUS"},
                str(manifest.get("webapp"))),
               ("source: no SpreadsheetApp, DriveApp, ScriptApp or UrlFetchApp outside comments",
                not any(w in code for w in ("SpreadsheetApp", "DriveApp", "ScriptApp", "UrlFetchApp")), "")]
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page()
        try:
            got = await page.evaluate(HARNESS, src)
        except Exception as exc:     # a trapped service call, or a crash in the script, ends the run
            got = [["the script runs to the end under the fakes", False, str(exc).splitlines()[0][:200]]]
        await browser.close()
    results += [tuple(r) for r in got]
    bad = 0
    for name, ok, detail in results:
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  <- " + detail))
        bad += not ok
    print("counts script: %s (%d checks)" % ("FAIL" if bad else "PASS", len(results)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
