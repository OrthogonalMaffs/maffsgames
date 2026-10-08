// ============================================================
//  MaffsGames — GA4 country figures, copied daily into the events Sheet
// ============================================================
//
//  SETUP: docs/ga4-country-setup.md (Jon's steps). Paste this file into the Apps Script project as
//  its own script file, add the "Google Analytics Data API" advanced service, run ga4CountryCheckProperty,
//  then ga4CountryBackfill (once), then ga4CountrySetupTrigger (once).
//
//  What it does. Reads aggregate figures by country from GA4's Data API (Jon's ruling, 8 Oct 2026) and
//  writes them into two tabs of the 'MaffsGames Events' spreadsheet:
//    'GA4 country daily'   date, country, activeUsers, sessions, engagedSessions, eventCount
//    'GA4 country events'  date, country, eventName, activeUsers, eventCount
//                          (eventName in page_view, game_started, question_answered, game_completed)
//  Nothing new is collected from anyone: these are figures GA4 already holds. The site, analytics.js,
//  the events endpoint and the privacy page are unchanged.
//
//  Why three days. GA4 keeps revising a day's figures for about 48 hours. The daily run fetches the last
//  three complete days and REPLACES those dates' rows, so a re-run, or two runs on one day, never
//  duplicates a row, and rows for every other date are left exactly as they were.
//
//  What it never touches. The events tab (the spreadsheet's first tab, which the endpoint writes) and
//  every tab other than the two above: it reads and writes sheets only by those two names, never by
//  position, never deletes a tab, and adds a missing tab at the END so the events tab stays first.
//  It never creates a spreadsheet.
//
//  It may share an Apps Script project with docs/apps-script-endpoint.js: script files in one project
//  share one global scope, so every top-level name here starts GA4C_, ga4c or ga4Country
//  (scripts/test-ga4-country.py fails on any name the endpoint also uses).
//
//  Functions ending in _ are helpers: Apps Script hides them from the Run menu.

const GA4C_PROPERTY = 'properties/528531831';
const GA4C_STREAM_ID = '13898555479';           // canon §1.1: the maffsgames.co.uk web stream
const GA4C_SPREADSHEET_NAME = 'MaffsGames Events';
const GA4C_TIMEZONE = 'Europe/London';
const GA4C_SETTLE_DAYS = 3;                      // the last three complete days are fetched and replaced
const GA4C_BACKFILL_START = '2026-09-01';
const GA4C_TRIGGER_HOUR = 6;                     // 06:00 UK time, before the endpoint's 07:00 report
const GA4C_PAGE_LIMIT = 100000;                  // rows per API request (the API allows 250,000)
const GA4C_EVENTS = ['page_view', 'game_started', 'question_answered', 'game_completed'];
const GA4C_TABLES = [
  {
    tab: 'GA4 country daily',
    dimensions: ['date', 'country'],
    metrics: ['activeUsers', 'sessions', 'engagedSessions', 'eventCount'],
    eventFilter: false,
    // newest date first; within a date, most users first
    order: [['date', -1], ['activeUsers', -1], ['country', 1]]
  },
  {
    tab: 'GA4 country events',
    dimensions: ['date', 'country', 'eventName'],
    metrics: ['activeUsers', 'eventCount'],
    eventFilter: true,
    // newest date first; within a date, by country, then the events in GA4C_EVENTS order
    order: [['date', -1], ['country', 1], ['eventName', 1]]
  }
];

// ============================================================
//  RUN THESE (from the Run menu)
// ============================================================

// The daily job (the trigger runs this): the last three complete days, replaced.
function ga4CountryDaily() {
  var today = ga4cDateKey_(ga4cNow_());
  ga4cRefresh_(ga4cDateRange_(ga4cAddDays_(today, -GA4C_SETTLE_DAYS), ga4cAddDays_(today, -1)));
}

// Once, after installing: 1 Sep 2026 to yesterday, replaced. Safe to run again at any time.
function ga4CountryBackfill() {
  var today = ga4cDateKey_(ga4cNow_());
  ga4cRefresh_(ga4cDateRange_(GA4C_BACKFILL_START, ga4cAddDays_(today, -1)));
}

// Before anything else: proves GA4C_PROPERTY is the property that holds the maffsgames.co.uk stream.
// Reads the last 7 days' events by stream and host name; writes nothing.
function ga4CountryCheckProperty() {
  var today = ga4cDateKey_(ga4cNow_());
  var resp = AnalyticsData.Properties.runReport({
    dateRanges: [{ startDate: ga4cAddDays_(today, -7), endDate: ga4cAddDays_(today, -1) }],
    dimensions: [{ name: 'streamId' }, { name: 'hostName' }],
    metrics: [{ name: 'eventCount' }],
    limit: 50
  }, GA4C_PROPERTY);
  var rows = (resp.rows || []).map(function (r) {
    return r.dimensionValues[0].value + '  ' + r.dimensionValues[1].value + '  ' + r.metricValues[0].value;
  });
  Logger.log('Streams and hosts in ' + GA4C_PROPERTY + ', last 7 days:\n' + (rows.join('\n') || '(none)'));
  var ours = (resp.rows || []).some(function (r) {
    return r.dimensionValues[0].value === GA4C_STREAM_ID &&
      /(^|\.)maffsgames\.co\.uk$/.test(r.dimensionValues[1].value);
  });
  if (!ours) {
    throw new Error(GA4C_PROPERTY + ' has no maffsgames.co.uk events from stream ' + GA4C_STREAM_ID +
      ' in the last 7 days. Check the property ID (GA4 Admin > Property details) before running anything else.');
  }
  Logger.log('OK: ' + GA4C_PROPERTY + ' holds stream ' + GA4C_STREAM_ID + ' (maffsgames.co.uk).');
}

// Once: the daily trigger at 06:00 UK time. Replaces only this script's own trigger.
function ga4CountrySetupTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'ga4CountryDaily') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('ga4CountryDaily')
    .timeBased().atHour(GA4C_TRIGGER_HOUR).everyDays(1).inTimezone(GA4C_TIMEZONE).create();
}

// ============================================================
//  FETCH AND WRITE
// ============================================================

// Fetch both tables for these dates, then write both. Every API call happens before any write, so a
// failed request (quota, authorisation) leaves both tabs exactly as they were.
function ga4cRefresh_(dates) {
  if (!dates.length) throw new Error('No complete days to fetch.');
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var fetched = GA4C_TABLES.map(function (t) {
      return ga4cFetch_(t, dates[0], dates[dates.length - 1]);
    });
    var ss = ga4cSpreadsheet_();
    GA4C_TABLES.forEach(function (t, i) { ga4cWriteTab_(ss, t, dates, fetched[i]); });
    Logger.log('Replaced ' + dates[0] + ' to ' + dates[dates.length - 1] + ': ' +
      GA4C_TABLES.map(function (t, i) { return t.tab + ' ' + fetched[i].length + ' rows'; }).join(', '));
  } finally {
    lock.releaseLock();
  }
}

// Every row of one table for startDate..endDate, as [date 'yyyy-MM-dd', dimension..., metric (number)...].
// Pages through the report: each pass moves the offset on by the rows it received, or stops.
function ga4cFetch_(table, startDate, endDate) {
  var request = {
    dateRanges: [{ startDate: startDate, endDate: endDate }],
    dimensions: table.dimensions.map(function (n) { return { name: n }; }),
    metrics: table.metrics.map(function (n) { return { name: n }; }),
    limit: GA4C_PAGE_LIMIT,
    offset: 0,
    returnPropertyQuota: true
  };
  if (table.eventFilter) {
    request.dimensionFilter = {
      filter: { fieldName: 'eventName', inListFilter: { values: GA4C_EVENTS, caseSensitive: true } }
    };
  }
  var out = [];
  var total = 0;
  var page;
  do {
    request.offset = out.length;
    var resp = AnalyticsData.Properties.runReport(request, GA4C_PROPERTY);
    page = resp.rows || [];
    total = Number(resp.rowCount || 0);
    page.forEach(function (r) { out.push(ga4cApiRow_(r)); });
    if (resp.metadata && resp.metadata.subjectToThresholding) {
      Logger.log(table.tab + ': GA4 withheld some small counts (thresholding); totals may be low.');
    }
    if (resp.propertyQuota && resp.propertyQuota.tokensPerDay) {
      Logger.log(table.tab + ': quota tokens left today ' + resp.propertyQuota.tokensPerDay.remaining);
    }
  } while (page.length > 0 && out.length < total);
  return out;
}

function ga4cApiRow_(r) {
  var dims = r.dimensionValues.map(function (d) { return d.value; });
  dims[0] = ga4cCellDate_(dims[0]);   // GA4 sends dates as yyyyMMdd
  return dims.concat(r.metricValues.map(function (m) { return Number(m.value); }));
}

// The events spreadsheet. A script bound to it uses it directly; otherwise it is found by name, as the
// endpoint finds it. Never created here.
function ga4cSpreadsheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (ss) return ss;
  var files = DriveApp.getFilesByName(GA4C_SPREADSHEET_NAME);
  if (!files.hasNext()) throw new Error('No spreadsheet named "' + GA4C_SPREADSHEET_NAME + '" in this Drive.');
  return SpreadsheetApp.open(files.next());
}

// Replace this table's rows for `dates` with `fresh`; every other row is kept as it was.
function ga4cWriteTab_(ss, table, dates, fresh) {
  var headers = table.dimensions.concat(table.metrics);
  var width = headers.length;
  var tab = ss.getSheetByName(table.tab);
  if (!tab) tab = ss.insertSheet(table.tab, ss.getNumSheets());   // at the end: the events tab stays first
  var last = tab.getLastRow();
  var existing = [];
  if (last >= 1) {
    var head = tab.getRange(1, 1, 1, width).getValues()[0];
    if (head.join('|') !== headers.join('|')) {
      throw new Error('Tab "' + table.tab + '" has row 1 "' + head.join(', ') + '", not this script\'s headers: ' +
        'not overwriting it. Rename that tab, then run again.');
    }
    if (last >= 2) existing = tab.getRange(2, 1, last - 1, width).getValues();
  }
  var tz = ss.getSpreadsheetTimeZone();
  var merged = ga4cMerge_(existing, fresh, dates, table, tz);

  tab.getRange(1, 1, Math.max(last, merged.length + 1), 1).setNumberFormat('@');   // dates stay text
  tab.getRange(1, 1, 1, width).setValues([headers]).setFontWeight('bold');
  tab.setFrozenRows(1);
  if (merged.length) tab.getRange(2, 1, merged.length, width).setValues(merged);
  if (last > merged.length + 1) tab.getRange(merged.length + 2, 1, last - merged.length - 1, width).clearContent();
}

// The pure core: rows outside the window kept, rows inside it replaced by `fresh`, sorted.
// A fetch that returns nothing for the whole window while the tab holds rows there is refused: it is
// far likelier a GA4 or property fault than three days with no visitors anywhere, and replacing would
// blank those days. GA4 rows dated outside the window are dropped, so no other date can change.
function ga4cMerge_(existing, fresh, dates, table, tz) {
  var inWindow = {};
  dates.forEach(function (d) { inWindow[d] = true; });
  var rows = existing.filter(function (r) { return r.join('') !== ''; });
  var kept = rows.filter(function (r) { return !inWindow[ga4cCellDate_(r[0], tz)]; });
  var added = fresh.filter(function (r) { return inWindow[r[0]]; });
  if (!added.length && kept.length < rows.length) {
    throw new Error(table.tab + ': GA4 returned no rows for ' + dates[0] + ' to ' + dates[dates.length - 1] +
      ' but the tab has rows for those dates. Not replacing them; run again later.');
  }
  kept = kept.map(function (r) { return [ga4cCellDate_(r[0], tz)].concat(r.slice(1)); });
  return kept.concat(added).sort(ga4cComparator_(table));
}

function ga4cComparator_(table) {
  var headers = table.dimensions.concat(table.metrics);
  var keys = table.order.map(function (o) { return [headers.indexOf(o[0]), o[1], o[0]]; });
  return function (a, b) {
    for (var i = 0; i < keys.length; i++) {
      var c = keys[i][0], dir = keys[i][1], x = a[c], y = b[c];
      if (keys[i][2] === 'eventName') { x = GA4C_EVENTS.indexOf(x); y = GA4C_EVENTS.indexOf(y); }
      if (x < y) return -dir;
      if (x > y) return dir;
    }
    return 0;
  };
}

// ============================================================
//  DATES (keys are 'yyyy-MM-dd' strings)
// ============================================================

function ga4cNow_() { return new Date(); }

function ga4cDateKey_(d) { return Utilities.formatDate(d, GA4C_TIMEZONE, 'yyyy-MM-dd'); }

// A date cell as a key: GA4's yyyyMMdd, a key already, or a Date if Sheets ever converted the text.
function ga4cCellDate_(v, tz) {
  if (Object.prototype.toString.call(v) === '[object Date]') return Utilities.formatDate(v, tz, 'yyyy-MM-dd');
  var s = String(v);
  return /^\d{8}$/.test(s) ? s.slice(0, 4) + '-' + s.slice(4, 6) + '-' + s.slice(6, 8) : s;
}

function ga4cAddDays_(key, n) {
  var p = key.split('-');
  return new Date(Date.UTC(Number(p[0]), Number(p[1]) - 1, Number(p[2]) + n)).toISOString().slice(0, 10);
}

// Every date from start to end inclusive (empty if start is after end).
function ga4cDateRange_(start, end) {
  var out = [];
  for (var d = start; d <= end; d = ga4cAddDays_(d, 1)) out.push(d);
  return out;
}
