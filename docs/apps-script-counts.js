// ============================================================
//  MaffsGames Answer Counts — a SEPARATE Google Apps Script project
// ============================================================
//
//  Counts question_answered rows in the analytics Sheet, per game_slug, for the current school
//  year (from 1 September, Europe/London), and serves the totals as JSON. It is its own project
//  so it can never compete with the analytics script's doPost for capacity: it only READS the
//  Sheet (through the Sheets advanced service, with the read-only scope), and the analytics script does not know it exists.
//
//  SETUP: docs/apps-script-counts.md (click by click). Paste this file into Code.gs, set SHEET_ID,
//         and copy docs/apps-script-counts.appsscript.json over the project's appsscript.json (it also
//         switches on the Sheets advanced service, which every read goes through).
//
//  HOW IT COUNTS: the counts per game, the last row read and the period start live in script
//  properties. Each run reads only the rows added since the last run (never the whole Sheet),
//  under a script lock, a chunk at a time, and saves its place after every chunk, so a run cut
//  off by the time limit loses nothing. The first run (or the first run after 1 September)
//  finds the start of the period by binary search on the timestamp column, then reads on from there.
//
//  EVENT TIME: the client_ts column (the browser's clock) when it is present and within a day of
//  the arrival timestamp; otherwise the arrival timestamp. Rows written before 26 Aug 2026 have no
//  client_ts, and a wrong device clock is ignored rather than trusted.
//
//  Jon's own play on the live site is counted; nothing is filtered (Jon, 22 Oct 2026).
//
//  STATS (contract UGH-STATS-DATA, 14 Nov 2026): the same pass also tallies game_started rows for the "Ugh, stats"
//  pages: starts per UK date, per date and level, per date and hour, kept for the last 35 UK dates, one script
//  property per date. <exec URL>?stats=1 answers {as_of, daily, levels, hours, countries}: complete UK days only (the
//  windows end on the day before as_of), countries from the "GA4 country daily" tab of the same spreadsheet, and every
//  count from 1 to 9 published as the string "<10". Without ?stats=1 the address answers exactly as it did before.
//  What the tallies leave out: rows whose game_slug or level is "test" or "terminal-test"; a level that is not a
//  short plain label is counted as "other" (the Sheet's endpoint accepts any text from anyone, and these labels are
//  published). The answer counts are not touched by any of this.
//
//  SAFE TALLIES (contract COUNTS-SAFE-TALLY, 14 Nov 2026): a game_slug or level is whatever was posted, by anyone, and
//  it becomes a key. In a plain object a key such as "constructor" or "__proto__" reads a built-in member, so a count
//  started from a function and became text, or was dropped. Every object keyed by event data is therefore a map with
//  no prototype (map_, mapFrom_ for state read back from the properties) and is read through hasOwn_ (count_).

const SHEET_ID = 'PASTE_THE_SHEET_ID_HERE';   // the long id in the Sheet's address: /spreadsheets/d/<ID>/edit
const SHEET_NAME = 'Sheet1';                  // the TAB's name (the file is called MaffsGames Events)
const TIMEZONE = 'Europe/London';
const COUNTED_EVENT = 'question_answered';
const CHUNK_ROWS = 5000;                      // rows read per call
const RUN_BUDGET_MS = 240000;                 // a trigger or backfill run stops reading after 4 minutes
const GET_BUDGET_MS = 20000;                  // a web request that has to update stops after 20 seconds
const CACHE_SECONDS = 60;
const MAX_SKEW_MS = 24 * 3600 * 1000;         // client_ts further than this from arrival is not trusted
const PROP_LIMIT = 8500;                      // script properties hold 9 KB a value

// ---- stats (the "Ugh, stats" pages)
const STARTED_EVENT = 'game_started';
const STATS_KEEP_DAYS = 35;                   // UK dates of start tallies kept (today and the 34 before it)
const STATS_DAILY_DAYS = 30;                  // the windows of the stats payload, in complete UK dates
const STATS_LEVEL_DAYS = 7;
const STATS_HOUR_DAYS = 28;
const STATS_COUNTRY_DAYS = 28;
const STATS_MAX_LEVELS = 40;                  // distinct levels kept per date; any more are counted as "other"
const STATS_LEVEL_LABEL = /^[A-Za-z0-9][A-Za-z0-9 _.+-]{0,23}$/;   // a level worth publishing; anything else is "other"
const STATS_TEST = /^(test|terminal-test)$/i; // a game_slug or level that marks a test row: never tallied
const STATS_HIDE_BELOW = 10;                  // a count from 1 to 9 is published as "<10"
const STATS_GA4_TAB = 'GA4 country daily';
const STATS_GA4_COLUMNS = ['date', 'country', 'activeUsers', 'sessions', 'engagedSessions', 'eventCount'];
const STATS_GA4_LAG_DAYS = 3;                 // the tab's newest date may be this far behind the last complete day
const DAY_PREFIX = 'd:';                      // one property per UK date: d:2026-11-13 -> {n, l:{level: n}, h:[24]}

// Bump when this file is redeployed; <exec URL>?version=1 then says which code is live.
const SCRIPT_VERSION = '2026-11-14-b';

// ============================================================
//  GET — the figures, from a 60-second cache
// ============================================================
function doGet(e) {
  if (e && e.parameter && e.parameter.version) return json_(JSON.stringify({ version: SCRIPT_VERSION }));
  if (e && e.parameter && e.parameter.stats) return json_(statsBody_());
  var cache = CacheService.getScriptCache();
  var hit = cache.get('payload');
  if (hit) return json_(hit);
  // Cache miss: catch up on any new rows first. If another run holds the lock, serve what is stored.
  try { updateCounts_(GET_BUDGET_MS, 3000); } catch (err) { console.error('doGet update failed: ' + err); }
  var body = JSON.stringify(payload_(loadState_(), new Date()));
  cache.put('payload', body, CACHE_SECONDS);
  return json_(body);
}

// ?stats=1: the stats payload, from its own 60-second cache. A fault in the stats (the GA4 tab missing, renamed
// columns, figures days behind) answers {error}, which the daily job reports; it never touches the counts above.
function statsBody_() {
  var cache = CacheService.getScriptCache();
  var hit = cache.get('stats');
  if (hit) return hit;
  try { updateCounts_(GET_BUDGET_MS, 3000); } catch (err) { console.error('stats update failed: ' + err); }
  var body;
  try {
    body = JSON.stringify(statsPayload_(loadState_(), new Date(), countryRows_()));
  } catch (err) {
    console.error('stats payload failed: ' + err);
    body = JSON.stringify({ error: String(err && err.message ? err.message : err) });
  }
  cache.put('stats', body, CACHE_SECONDS);
  return body;
}

function json_(text) {
  return ContentService.createTextOutput(text).setMimeType(ContentService.MimeType.JSON);
}

// ============================================================
//  Triggers and manual runs (set the trigger in the editor's Triggers panel, not in code)
// ============================================================

// Time-driven trigger target: every 5 minutes.
function updateCounts() {
  updateCounts_(RUN_BUDGET_MS, 30000);
}

// Run by hand, repeatedly, until the log says "caught up: true". Logs rows and time (for the first full count).
function backfill() {
  updateCounts_(RUN_BUDGET_MS, 30000);
}

// Run by hand to throw the stored counts away and count the school year again from scratch.
function resetCounts() {
  PropertiesService.getScriptProperties().deleteAllProperties();
  CacheService.getScriptCache().remove('payload');
  CacheService.getScriptCache().remove('stats');
  console.log('counts cleared; run backfill()');
}

// Run by hand to see exactly what the web address will return, without the cache.
function preview() {
  console.log(JSON.stringify(payload_(loadState_(), new Date())));
}

// Run by hand to see exactly what <exec URL>?stats=1 will return, without the cache.
function previewStats() {
  console.log(JSON.stringify(statsPayload_(loadState_(), new Date(), countryRows_())));
}

// ============================================================
//  The incremental count
// ============================================================
// Every read goes through the Sheets advanced service (Sheets.Spreadsheets.Values.get), which the read-only scope
// covers. SpreadsheetApp is never called: openById needs the full read-write scope, and this project must not have it.
function updateCounts_(budgetMs, lockWaitMs) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(lockWaitMs)) { console.log('another run holds the lock; skipped'); return; }
  var t0 = Date.now();
  try {
    var now = new Date();
    var sinceStr = sinceString_(now);
    var sinceDate = londonMidnight_(sinceStr);
    var keepFrom = addDays_(londonDate_(now), -(STATS_KEEP_DAYS - 1));   // the oldest UK date whose start tallies are kept
    var keepFromDate = londonMidnight_(keepFrom);
    var meta = meta_();
    var cols = columns_();
    var st = loadState_();

    // A new school year, no stored state, or rows that are not where the last run left them (the row it stopped on
    // no longer holds the timestamp it recorded, so rows were deleted): start the period again. So does state whose
    // start tallies do not cover exactly the rows read (statsRow is written with lastRow on every save): state from
    // before the stats existed, or a row read by an older version of this script that tallied no starts.
    var moved = st.lastRow > 1 && st.lastTs && String(readCell_(st.lastRow, cols.arrival)) !== st.lastTs;
    var unTallied = st.statsRow !== st.lastRow;
    if (st.since !== sinceStr || moved || unTallied) {
      // Read from whichever is earlier, the school year or the oldest date kept for the stats (they differ only in
      // September and early October). The answer counts still take nothing from before 1 September: tally_ checks.
      var readFrom = keepFromDate < sinceDate ? keepFromDate : sinceDate;
      st = { since: sinceStr, lastRow: startRow_(cols, readFrom, meta) - 1, lastTs: '', counts: map_(), starts: map_(),
             stored: st.stored, asOf: null };
      console.log('period start ' + sinceStr + ': reading from row ' + (st.lastRow + 1));
    }
    st.keepFrom = keepFrom;

    var rowsRead = 0, caughtUp = false;
    while (Date.now() - t0 < budgetMs) {
      var from = st.lastRow + 1;
      if (from > meta.rowCount) { caughtUp = true; break; }
      var to = Math.min(from + CHUNK_ROWS - 1, meta.rowCount);
      var rows = readRows_(from, to, cols.width);
      tally_(rows, cols, sinceDate, meta.tz, st.counts);
      tallyStarts_(rows, cols, keepFromDate, meta.tz, st.starts);
      if (rows.length) {
        st.lastRow = from + rows.length - 1;
        st.lastTs = String(rows[rows.length - 1][cols.arrival]);
      }
      rowsRead += rows.length;
      saveState_(st);
      if (rows.length < to - from + 1) { caughtUp = true; break; }   // ran off the end of the data
    }
    if (caughtUp) st.asOf = Utilities.formatDate(new Date(), TIMEZONE, "yyyy-MM-dd'T'HH:mm:ssXXX");
    saveState_(st);
    CacheService.getScriptCache().remove('payload');
    CacheService.getScriptCache().remove('stats');
    console.log('read ' + rowsRead + ' rows in ' + (Date.now() - t0) + ' ms; last row ' + st.lastRow +
                '; caught up: ' + caughtUp);
  } finally {
    lock.releaseLock();
  }
}

// Adds the counted rows of one chunk into `counts` (pure: no Sheet, no clock). `counts` is a map_(): the slug is
// whatever was posted, so it is never read as a member of a plain object.
function tally_(vals, cols, sinceDate, tz, counts) {
  for (var i = 0; i < vals.length; i++) {
    var r = vals[i];
    if (r[cols.event] !== COUNTED_EVENT) continue;
    var slug = String(r[cols.slug] || '').trim();
    if (!slug) continue;
    var t = eventTime_(r[cols.arrival], r[cols.clientTs], tz);
    if (!t || t < sinceDate) continue;
    counts[slug] = count_(counts, slug) + 1;
  }
}

// Adds the game_started rows of one chunk into `starts` (pure: no Sheet, no clock), keyed by the UK date of the
// event: {date: {n: starts, l: {level: starts}, h: [starts in each hour 0-23]}}. Rows before `fromDate` are left out
// (their dates are no longer kept), and so are test rows.
function tallyStarts_(vals, cols, fromDate, tz, starts) {
  for (var i = 0; i < vals.length; i++) {
    var r = vals[i];
    if (r[cols.event] !== STARTED_EVENT) continue;
    var slug = String(r[cols.slug] || '').trim();
    if (!slug || STATS_TEST.test(slug)) continue;
    var level = levelKey_(r[cols.level]);
    if (STATS_TEST.test(level)) continue;
    var t = eventTime_(r[cols.arrival], r[cols.clientTs], tz);
    if (!t || t < fromDate) continue;
    var stamp = Utilities.formatDate(t, TIMEZONE, 'yyyy-MM-dd HH:mm:ss');   // the event on the UK clock
    var date = stamp.slice(0, 10), hour = Number(stamp.slice(11, 13));
    if (!hasOwn_(starts, date)) starts[date] = { n: 0, l: map_(), h: zeros_(24) };
    var d = starts[date];
    d.n += 1;
    d.h[hour] += 1;
    if (!hasOwn_(d.l, level) && Object.keys(d.l).length >= STATS_MAX_LEVELS) level = 'other';
    d.l[level] = (hasOwn_(d.l, level) ? d.l[level] : 0) + 1;
  }
}

// A level cell as the label it is tallied under: blank is "none"; anything that is not a short plain label is "other".
function levelKey_(v) {
  var s = String(v === null || v === undefined ? '' : v).trim();
  if (!s) return 'none';
  return STATS_LEVEL_LABEL.test(s) ? s : 'other';
}

// ---- safe maps: every object keyed by event data (a game_slug, a level, an event's date) is one of these
// A map with no prototype: "constructor", "__proto__", "toString" and "hasOwnProperty" are ordinary keys in it.
function map_() { return Object.create(null); }

// The own keys of `o` (parsed JSON, or nothing) copied into a map_(), in the same order.
function mapFrom_(o) {
  var m = map_();
  if (o) Object.keys(o).forEach(function (k) { m[k] = o[k]; });
  return m;
}

function hasOwn_(o, k) { return Object.prototype.hasOwnProperty.call(o, k); }

// The count stored under `k`, or 0 when the map has no such key of its own.
function count_(m, k) { return hasOwn_(m, k) ? m[k] : 0; }

function zeros_(n) { var a = []; while (a.length < n) a.push(0); return a; }

// The browser's clock when it agrees with the arrival time to within a day, else the arrival time.
function eventTime_(arrival, clientTs, tz) {
  var a = toDate_(arrival, tz);
  var c = toDate_(clientTs, tz);
  if (c && a && Math.abs(c - a) <= MAX_SKEW_MS) return c;
  return a;
}

// A cell as the API returns it with UNFORMATTED_VALUE: text stays text (an ISO timestamp parses as it is), and a
// cell Sheets turned into a date arrives as a serial number, days since 30 Dec 1899 on the SPREADSHEET's clock.
function toDate_(v, tz) {
  if (v === '' || v === null || v === undefined) return null;
  var d;
  if (typeof v === 'number') {
    var w = new Date(Date.UTC(1899, 11, 30) + Math.round(v * 86400000));   // the wall-clock reading, held as UTC
    d = Utilities.parseDate(Utilities.formatDate(w, 'UTC', 'yyyy-MM-dd HH:mm:ss'), tz, 'yyyy-MM-dd HH:mm:ss');
  } else {
    d = new Date(v);
  }
  return isNaN(d.getTime()) ? null : d;
}

// ---- reads (the only place the Sheet is touched)
function a1_(row1, row2, width) {
  return "'" + SHEET_NAME + "'!A" + row1 + ':' + colLetter_(width) + row2;
}

function colLetter_(n) {
  var s = '';
  while (n > 0) { var m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); }
  return s;
}

function values_(range) {
  var res = Sheets.Spreadsheets.Values.get(SHEET_ID, range, { valueRenderOption: 'UNFORMATTED_VALUE' });
  return res.values || [];
}

// Rows from..to, each padded to `width` (the API leaves off trailing empty cells and trailing empty rows).
function readRows_(from, to, width) {
  return values_(a1_(from, to, width)).map(function (r) {
    var out = r.slice(0, width);
    while (out.length < width) out.push('');
    return out;
  });
}

// One cell, or '' when it is empty or past the end of the data.
function readCell_(row, colIndex) {
  var v = values_("'" + SHEET_NAME + "'!" + colLetter_(colIndex + 1) + row);
  return v.length && v[0].length ? v[0][0] : '';
}

// Every row of the "GA4 country daily" tab, header first (docs/apps-script-ga4-country.js keeps it; canon 1.2.1).
// Read only, like every other read here; a missing tab is an error the stats payload reports.
function countryRows_() {
  return values_("'" + STATS_GA4_TAB + "'!A:F");
}

// The Sheet's time zone and its grid height (the last row that can hold data; the data ends where reads come back empty).
function meta_() {
  var m = Sheets.Spreadsheets.get(SHEET_ID, { fields: 'properties.timeZone,sheets.properties(title,gridProperties.rowCount)' });
  var tab = (m.sheets || []).filter(function (s) { return s.properties.title === SHEET_NAME; })[0];
  if (!tab) throw new Error('no sheet named ' + SHEET_NAME);
  return { tz: m.properties.timeZone, rowCount: tab.properties.gridProperties.rowCount };
}

// The column positions, found by header name so a reordered Sheet cannot silently miscount.
function columns_() {
  var head = values_("'" + SHEET_NAME + "'!1:1")[0] || [];
  var at = function (name) {
    var i = head.indexOf(name);
    if (i < 0) throw new Error('Sheet has no column ' + name);
    return i;
  };
  var c = { arrival: at('timestamp'), event: at('event'), slug: at('game_slug'), level: at('level'), clientTs: at('client_ts') };
  c.width = Math.max(c.arrival, c.event, c.slug, c.level, c.clientTs) + 1;
  return c;
}

// First row to read for a period: the first row that arrived a day before the period began (rows arrive in
// order; the day's slack covers an event stamped before midnight that arrived after). Binary search, one cell
// per probe. An empty cell is past the end of the data, so it counts as "after"; an unreadable timestamp is
// treated as "before", so the search moves right past it.
function startRow_(cols, sinceDate, meta) {
  var cutoff = new Date(sinceDate.getTime() - MAX_SKEW_MS);
  var lo = 2, hi = meta.rowCount + 1;         // answer is in [lo, hi]; hi means "none"
  while (lo < hi) {
    var mid = Math.floor((lo + hi) / 2);
    var cell = readCell_(mid, cols.arrival);
    var t = toDate_(cell, meta.tz);
    if (cell === '' || (t && t >= cutoff)) hi = mid; else lo = mid + 1;
  }
  return lo;
}

// ============================================================
//  Period, state, payload
// ============================================================

// '2026-09-01' from 1 Sept of the school year `now` falls in (Europe/London).
function sinceString_(now) {
  var y = Number(Utilities.formatDate(now, TIMEZONE, 'yyyy'));
  var m = Number(Utilities.formatDate(now, TIMEZONE, 'M'));
  return (m >= 9 ? y : y - 1) + '-09-01';
}

function londonMidnight_(dateStr) {
  return Utilities.parseDate(dateStr + ' 00:00:00', TIMEZONE, 'yyyy-MM-dd HH:mm:ss');
}

function loadState_() {
  var p = PropertiesService.getScriptProperties().getProperties();
  var starts = map_();
  Object.keys(p).forEach(function (k) {
    if (k.indexOf(DAY_PREFIX) !== 0) return;
    var day = JSON.parse(p[k]);
    day.l = mapFrom_(day.l);                                      // keyed by level: a map again, as tallyStarts_ made it
    starts[k.slice(DAY_PREFIX.length)] = day;
  });
  return {
    since: p.since || '',
    lastRow: p.lastRow ? Number(p.lastRow) : 0,
    lastTs: p.lastTs || '',
    counts: p.counts ? mapFrom_(JSON.parse(p.counts)) : map_(),
    starts: starts,
    stored: Object.keys(starts),                                  // the dates that have a property now
    statsRow: p.statsRow === undefined ? -1 : Number(p.statsRow), // the last row the start tallies cover
    asOf: p.asOf || null
  };
}

function saveState_(st) {
  var counts = JSON.stringify(st.counts);
  if (counts.length > PROP_LIMIT) throw new Error('counts are ' + counts.length + ' characters; split them across properties');
  var p = { since: st.since, lastRow: String(st.lastRow), lastTs: String(st.lastTs || ''), counts: counts,
            statsRow: String(st.lastRow) };
  if (st.asOf) p.asOf = st.asOf;
  // The start tallies: one property per UK date, so no value nears the limit however long the script runs. Dates
  // older than the 35 kept are pruned here, and their properties deleted below.
  if (st.keepFrom) pruneStarts_(st.starts, st.keepFrom);
  Object.keys(st.starts).forEach(function (date) {
    var v = JSON.stringify(st.starts[date]);
    if (v.length > PROP_LIMIT) throw new Error('the start tallies for ' + date + ' are ' + v.length + ' characters');
    p[DAY_PREFIX + date] = v;
  });
  var props = PropertiesService.getScriptProperties();
  props.setProperties(p, false);
  if (!st.asOf) props.deleteProperty('asOf');
  (st.stored || []).forEach(function (date) {
    if (!hasOwn_(st.starts, date)) props.deleteProperty(DAY_PREFIX + date);
  });
  st.stored = Object.keys(st.starts);
}

// Drops every date before `keepFrom` ('yyyy-MM-dd') from the start tallies (pure).
function pruneStarts_(starts, keepFrom) {
  Object.keys(starts).forEach(function (date) { if (date < keepFrom) delete starts[date]; });
}

// {as_of, since, total, games}. as_of is null until a run has read every row (the first full count in progress),
// which the site treats as "not available": it shows nothing rather than a part-count.
function payload_(st, now) {
  var games = map_();
  var total = 0;
  Object.keys(st.counts).sort().forEach(function (k) { games[k] = st.counts[k]; total += st.counts[k]; });
  return { as_of: st.asOf, since: st.since || sinceString_(now), total: total, games: games };
}

// ============================================================
//  The stats payload (pure: state, a clock reading and the GA4 tab's rows in; no Sheet)
// ============================================================

// {as_of, daily, levels, hours, countries}. Every window is of COMPLETE UK dates: it ends on the day before as_of
// (the day as_of falls in is still being played, and a part-day at the end of a chart reads as a fall).
//   daily      [{date, starts}]       the last 30 dates, oldest first, every date present (0 where there were none)
//   levels     [{level, starts}]      the last 7 dates; largest first, then the hidden ones by name
//   hours      {weekday:[24], weekend:[24]}   the last 28 dates (four whole weeks), Saturday and Sunday as weekend
//   countries  [{country, sessions}]  28 dates of the "GA4 country daily" tab; largest first, "Other countries" last
// A count from 1 to 9 is published as "<10"; 0 stays 0.
function statsPayload_(st, now, countryRows) {
  var end = addDays_(st.asOf ? st.asOf.slice(0, 10) : londonDate_(now), -1);
  var day = function (back) {
    var date = addDays_(end, -back);
    return { date: date, tally: hasOwn_(st.starts, date) ? st.starts[date] : null };
  };
  var i, d;

  var daily = [];
  for (i = STATS_DAILY_DAYS - 1; i >= 0; i--) {
    d = day(i);
    daily.push({ date: d.date, starts: hide_(d.tally ? d.tally.n : 0) });
  }

  var byLevel = Object.create(null);
  for (i = 0; i < STATS_LEVEL_DAYS; i++) {
    d = day(i);
    if (d.tally) Object.keys(d.tally.l).forEach(function (k) { byLevel[k] = (byLevel[k] || 0) + d.tally.l[k]; });
  }
  var levels = ranked_(byLevel).map(function (x) { return { level: x.name, starts: hide_(x.n) }; });

  var weekday = zeros_(24), weekend = zeros_(24);
  for (i = 0; i < STATS_HOUR_DAYS; i++) {
    d = day(i);
    if (!d.tally) continue;
    var into = isWeekend_(d.date) ? weekend : weekday;
    for (var h = 0; h < 24; h++) into[h] += d.tally.h[h] || 0;
  }

  return { as_of: st.asOf, daily: daily, levels: levels,
           hours: { weekday: weekday.map(hide_), weekend: weekend.map(hide_) },
           countries: countryTotals_(countryRows, end) };
}

// Sessions per country over 28 dates of the "GA4 country daily" tab, ending on its newest date that is not after
// `end` (GA4's figures arrive a day or so late, so the window follows the figures the tab holds). A country under 10
// sessions is summed into "Other countries", last in the list, itself "<10" when that sum is under 10; blank and
// "(not set)" are "Unknown". Throws when the columns are not the six expected or the tab is days behind: both are
// faults to be seen, not published.
function countryTotals_(rows, end) {
  var head = ((rows && rows[0]) || []).slice(0, STATS_GA4_COLUMNS.length).map(String);
  if (head.join('|') !== STATS_GA4_COLUMNS.join('|')) {
    throw new Error('the "' + STATS_GA4_TAB + '" tab\'s columns are [' + head.join(', ') + '], want [' + STATS_GA4_COLUMNS.join(', ') + ']');
  }
  var seen = [], newest = '';
  for (var i = 1; i < rows.length; i++) {
    var date = ga4Date_(rows[i][0]);
    var sessions = Number(rows[i][3]);
    if (!date || date > end || !(sessions > 0)) continue;
    var country = String(rows[i][1] === null || rows[i][1] === undefined ? '' : rows[i][1]).trim();
    seen.push({ date: date, country: country === '' || country === '(not set)' ? 'Unknown' : country, sessions: sessions });
    if (date > newest) newest = date;
  }
  if (!newest || newest < addDays_(end, -STATS_GA4_LAG_DAYS)) {
    throw new Error('the "' + STATS_GA4_TAB + '" tab has no sessions after ' + (newest || 'the start') + ' (the last complete day is ' + end + ')');
  }
  var from = addDays_(newest, -(STATS_COUNTRY_DAYS - 1));
  var by = Object.create(null);
  seen.forEach(function (x) { if (x.date >= from) by[x.country] = (by[x.country] || 0) + x.sessions; });
  var out = [], other = 0, folded = 0;
  ranked_(by).forEach(function (x) {
    if (x.n >= STATS_HIDE_BELOW) out.push({ country: x.name, sessions: x.n });
    else { other += x.n; folded += 1; }
  });
  if (folded) out.push({ country: 'Other countries', sessions: hide_(other) });
  return out;
}

// {name: n} as [{name, n}]: the counts that are published (10 or more) largest first, ties by name; then the hidden
// ones (1 to 9) by name alone, so their order says nothing about their size. Zero counts are left out.
function ranked_(by) {
  var all = Object.keys(by).filter(function (k) { return by[k] > 0; }).map(function (k) { return { name: k, n: by[k] }; });
  var byName = function (a, b) { return a.name < b.name ? -1 : a.name > b.name ? 1 : 0; };
  var shown = all.filter(function (x) { return x.n >= STATS_HIDE_BELOW; }).sort(function (a, b) { return b.n - a.n || byName(a, b); });
  var hidden = all.filter(function (x) { return x.n < STATS_HIDE_BELOW; }).sort(byName);
  return shown.concat(hidden);
}

// "Figures below 10 are hidden": 1 to 9 is "<10"; 0 and 10 or more are published as they are.
function hide_(n) {
  return n > 0 && n < STATS_HIDE_BELOW ? '<10' : n;
}

// A date cell of the GA4 tab as 'yyyy-MM-dd': text as the GA4 script wrote it, GA4's own yyyyMMdd, or the serial
// number Sheets holds once it has read the text as a date (whole days since 30 Dec 1899). Anything else is null.
function ga4Date_(v) {
  if (typeof v === 'number' && isFinite(v) && v > 0) {
    return new Date(Date.UTC(1899, 11, 30) + Math.floor(v) * 86400000).toISOString().slice(0, 10);
  }
  var s = String(v === null || v === undefined ? '' : v).trim();
  if (/^\d{8}$/.test(s)) return s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8);
  return /^\d{4}-\d\d-\d\d/.test(s) ? s.slice(0, 10) : null;
}

// ---- dates as 'yyyy-MM-dd' text
function londonDate_(d) {
  return Utilities.formatDate(d, TIMEZONE, 'yyyy-MM-dd HH:mm:ss').slice(0, 10);
}

function addDays_(dateStr, n) {
  var p = dateStr.split('-');
  return new Date(Date.UTC(Number(p[0]), Number(p[1]) - 1, Number(p[2]) + n)).toISOString().slice(0, 10);
}

function isWeekend_(dateStr) {
  var p = dateStr.split('-');
  var dow = new Date(Date.UTC(Number(p[0]), Number(p[1]) - 1, Number(p[2]))).getUTCDay();
  return dow === 0 || dow === 6;
}
