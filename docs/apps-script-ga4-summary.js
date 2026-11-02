// ============================================================
//  MaffsGames — "GA4 summary" tab: weekly figures and three charts, rebuilt after the GA4 country pull
// ============================================================
//
//  SETUP: docs/ga4-country-setup.md, section "The GA4 summary tab" (Jon's steps). Paste this file into the
//  Apps Script project as its own script file, next to ga4-country. No new service, no new trigger.
//
//  What it does. Reads the two tabs docs/apps-script-ga4-country.js keeps ('GA4 country daily' and
//  'GA4 country events') and rebuilds ONE tab, 'GA4 summary', from them:
//    A1:G      one row per week (Monday start), oldest first, from w/c 31 Aug 2026:
//                Week starting | Questions answered | game_started | game_completed |
//                Engaged sessions UK | Engaged sessions rest of world | Status
//              The week that is not yet complete (and the first week, which starts mid-week because the
//              GA4 pull starts on 1 Sep) is marked 'partial'. At most 52 weeks are kept: the window rolls
//              forward when the year is full, so nothing here needs editing next September.
//    I1:L11    the ten countries with most engaged sessions over the last 28 complete days:
//                Country | Engaged sessions | Sessions | Engaged share
//  and three charts pointed at those fixed ranges: questions answered per week (line), engaged sessions UK
//  vs rest of world (line, two series), top ten countries by engaged sessions (bar).
//
//  Why engaged sessions. Raw 'active users' counts crawlers as visitors: some countries are mostly bot
//  traffic (engaged share Singapore 2%, China 13%, US 24%, UK 62% on 28 Oct 2026). A crawler's session is
//  not engaged and it never answers a question.
//
//  Rebuilds change VALUES only. The three charts are created once (found again by title on every later
//  run) and never recreated or moved, so a second run leaves exactly three. Rows beyond the data are
//  left empty, which Sheets charts leave out.
//
//  What it never touches. The GA4 tabs (read only), Sheet1, the Dashboard, the endpoint and every trigger.
//  It reads and writes sheets only by name, never by position, never deletes a tab, and adds a missing
//  'GA4 summary' at the END so the events tab stays first.
//
//  It is called from the end of ga4CountryDaily and ga4CountryBackfill in ga4-country.js (when this file is
//  present), so the one existing daily trigger runs both. It shares ga4-country.js's helper names
//  (ga4cSpreadsheet_, ga4cCellDate_, ga4cDateKey_, ga4cAddDays_, ga4cNow_, GA4C_TABLES): script files in one
//  project share one global scope. Every top-level name here starts GA4S_, ga4s or ga4Summary
//  (scripts/test-ga4-summary.py fails on any name the other two files also use).
//
//  Functions ending in _ are helpers: Apps Script hides them from the Run menu.

const GA4S_TAB = 'GA4 summary';
const GA4S_DAILY_TAB = 'GA4 country daily';
const GA4S_EVENTS_TAB = 'GA4 country events';
const GA4S_FIRST_WEEK = '2026-08-31';            // the Monday of the week the GA4 pull begins
const GA4S_MAX_WEEKS = 52;
const GA4S_TOP_N = 10;
const GA4S_TOP_DAYS = 28;
const GA4S_UK = 'United Kingdom';
const GA4S_WEEK_HEAD = ['Week starting', 'Questions answered', 'game_started', 'game_completed',
                        'Engaged sessions UK', 'Engaged sessions rest of world', 'Status'];
const GA4S_TOP_HEAD = ['Country', 'Engaged sessions', 'Sessions', 'Engaged share'];
const GA4S_TOP_COL = 9;                           // column I
const GA4S_CHART_COL = 9;                         // charts sit under the top-ten table, from column I
const GA4S_CHARTS = [
  { title: 'Questions answered per week', row: 14 },
  { title: 'Engaged sessions: UK vs rest of world', row: 32 },
  { title: 'Top 10 countries by engaged sessions, last 28 days', row: 50 }
];

// ============================================================
//  RUN THIS (from the Run menu; the daily job also calls it)
// ============================================================

function ga4SummaryRebuild() {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var ss = ga4cSpreadsheet_();
    var tz = ss.getSpreadsheetTimeZone();
    var daily = ga4sRead_(ss, GA4S_DAILY_TAB, ['date', 'country', 'activeUsers', 'sessions', 'engagedSessions', 'eventCount'], tz);
    var events = ga4sRead_(ss, GA4S_EVENTS_TAB, ['date', 'country', 'eventName', 'activeUsers', 'eventCount'], tz);
    var today = ga4cDateKey_(ga4cNow_());
    var model = ga4sBuild_(daily, events, today);

    var tab = ss.getSheetByName(GA4S_TAB);
    if (!tab) tab = ss.insertSheet(GA4S_TAB, ss.getNumSheets());   // at the end: the events tab stays first
    ga4sWrite_(tab, model);
    ga4sEnsureCharts_(tab);
    Logger.log('GA4 summary: ' + model.weeks.length + ' weeks (' + model.weeks[0][0] + ' to ' +
      model.weeks[model.weeks.length - 1][0] + '), ' + model.top.length + ' countries in the top ten.');
  } finally {
    lock.releaseLock();
  }
}

// ============================================================
//  READ, AGGREGATE (pure), WRITE, CHARTS
// ============================================================

// A GA4 tab's body rows, each as [date key, ...rest]. A tab that is missing, empty or has other headings
// is an error: there is nothing honest to summarise.
function ga4sRead_(ss, name, headers, tz) {
  var tab = ss.getSheetByName(name);
  if (!tab || tab.getLastRow() < 1) throw new Error('"' + name + '" is missing or empty: run ga4CountryBackfill first.');
  var head = tab.getRange(1, 1, 1, headers.length).getValues()[0];
  if (head.join('|') !== headers.join('|')) {
    throw new Error('Tab "' + name + '" has row 1 "' + head.join(', ') + '", not the GA4 country script\'s headers.');
  }
  if (tab.getLastRow() < 2) return [];
  return tab.getRange(2, 1, tab.getLastRow() - 1, headers.length).getValues()
    .filter(function (r) { return r.join('') !== ''; })
    .map(function (r) { return [ga4cCellDate_(r[0], tz)].concat(r.slice(1)); });
}

// The Monday on or before a date key.
function ga4sMonday_(key) {
  var p = key.split('-');
  var dow = new Date(Date.UTC(Number(p[0]), Number(p[1]) - 1, Number(p[2]))).getUTCDay();   // 0 = Sunday
  return ga4cAddDays_(key, -((dow + 6) % 7));
}

// The pure core. daily rows: [date, country, activeUsers, sessions, engagedSessions, eventCount];
// events rows: [date, country, eventName, activeUsers, eventCount]; today is a date key (UK).
// Returns { weeks: [[7 cells]...], top: [[4 cells]...] }.
function ga4sBuild_(daily, events, today) {
  var yesterday = ga4cAddDays_(today, -1);
  var thisMonday = ga4sMonday_(today);
  var start = ga4sMonday_(GA4S_FIRST_WEEK);
  var rolling = ga4cAddDays_(thisMonday, -7 * (GA4S_MAX_WEEKS - 1));
  if (rolling > start) start = rolling;

  var byWeek = {};
  var firstDay = null;
  function week_(date) {
    var m = ga4sMonday_(date);
    return byWeek[m] || (byWeek[m] = { q: 0, started: 0, completed: 0, uk: 0, row: 0 });
  }
  events.forEach(function (r) {
    var w = week_(r[0]);
    var count = Number(r[4]) || 0;
    if (r[2] === 'question_answered') w.q += count;
    else if (r[2] === 'game_started') w.started += count;
    else if (r[2] === 'game_completed') w.completed += count;
  });
  daily.forEach(function (r) {
    var w = week_(r[0]);
    var engaged = Number(r[4]) || 0;
    if (r[1] === GA4S_UK) w.uk += engaged; else w.row += engaged;
    if (firstDay === null || r[0] < firstDay) firstDay = r[0];
  });

  var weeks = [];
  for (var m = start; m <= thisMonday; m = ga4cAddDays_(m, 7)) {
    var w = byWeek[m] || { q: 0, started: 0, completed: 0, uk: 0, row: 0 };
    var partial = ga4cAddDays_(m, 6) > yesterday || (firstDay !== null && firstDay > m);
    weeks.push([m, w.q, w.started, w.completed, w.uk, w.row, partial ? 'partial' : '']);
  }

  var from = ga4cAddDays_(yesterday, -(GA4S_TOP_DAYS - 1));
  var by = {};
  daily.forEach(function (r) {
    if (r[0] < from || r[0] > yesterday) return;
    var c = by[r[1]] || (by[r[1]] = { country: r[1], engaged: 0, sessions: 0 });
    c.engaged += Number(r[4]) || 0;
    c.sessions += Number(r[3]) || 0;
  });
  var top = Object.keys(by).map(function (k) { return by[k]; })
    .sort(function (a, b) { return b.engaged - a.engaged || (a.country < b.country ? -1 : a.country > b.country ? 1 : 0); })
    .slice(0, GA4S_TOP_N)
    .map(function (c) { return [c.country, c.engaged, c.sessions, c.sessions ? c.engaged / c.sessions : 0]; });
  return { weeks: weeks, top: top };
}

// Values only: the two fixed regions are cleared and rewritten. Nothing else in the tab is touched.
function ga4sWrite_(tab, model) {
  var weekRows = GA4S_MAX_WEEKS;
  tab.getRange(1, 1, weekRows + 1, GA4S_WEEK_HEAD.length).clearContent();
  tab.getRange(1, 1, weekRows + 1, 1).setNumberFormat('@');                 // week starts stay text
  tab.getRange(1, 1, 1, GA4S_WEEK_HEAD.length).setValues([GA4S_WEEK_HEAD]).setFontWeight('bold');
  tab.getRange(2, 1, model.weeks.length, GA4S_WEEK_HEAD.length).setValues(model.weeks);

  tab.getRange(1, GA4S_TOP_COL, GA4S_TOP_N + 1, GA4S_TOP_HEAD.length).clearContent();
  tab.getRange(1, GA4S_TOP_COL, 1, GA4S_TOP_HEAD.length).setValues([GA4S_TOP_HEAD]).setFontWeight('bold');
  if (model.top.length) tab.getRange(2, GA4S_TOP_COL, model.top.length, GA4S_TOP_HEAD.length).setValues(model.top);
  tab.getRange(2, GA4S_TOP_COL + 3, GA4S_TOP_N, 1).setNumberFormat('0%');
  tab.setFrozenRows(1);
}

// Create each chart once. A chart is recognised by its title; one that exists is left exactly as it is.
function ga4sEnsureCharts_(tab) {
  var have = {};
  tab.getCharts().forEach(function (c) { have[c.getOptions().get('title')] = true; });
  var last = GA4S_MAX_WEEKS + 1;
  var topEnd = GA4S_TOP_N + 1;
  var specs = [
    { type: Charts.ChartType.LINE, ranges: ['A1:A' + last, 'B1:B' + last], extra: {} },
    { type: Charts.ChartType.LINE, ranges: ['A1:A' + last, 'E1:F' + last], extra: {} },
    { type: Charts.ChartType.BAR, ranges: ['I1:J' + topEnd], extra: { reverseCategories: true, legend: { position: 'none' } } }
  ];
  GA4S_CHARTS.forEach(function (c, i) {
    if (have[c.title]) return;
    var b = tab.newChart().setChartType(specs[i].type);
    specs[i].ranges.forEach(function (a) { b = b.addRange(tab.getRange(a)); });
    b = b.setNumHeaders(1).setPosition(c.row, GA4S_CHART_COL, 0, 0)
      .setOption('title', c.title).setOption('width', 640).setOption('height', 340);
    if (specs[i].type === Charts.ChartType.LINE) b = b.setOption('legend', { position: 'bottom' });
    Object.keys(specs[i].extra).forEach(function (k) { b = b.setOption(k, specs[i].extra[k]); });
    tab.insertChart(b.build());
  });
}
