// ============================================================
//  MaffsGames Analytics — Google Apps Script Endpoint
// ============================================================
//
//  SETUP: Paste into Code.gs, save, Deploy → Manage deployments
//         → edit → set version to latest → Deploy
//  Then: Select setupTrigger from dropdown → Run (once only)
//

const SHEET_NAME = 'MaffsGames Events';
const DASH_NAME = 'Dashboard';
const MAX_ROWS = 9000000;
// The owner's address is not kept in the repo (canon §7.7). Before pasting this file into the
// Apps Script editor, replace the placeholder with Jon's address (docs/apps-script-redeploy.md).
const REPORT_EMAIL = 'OWNER_EMAIL_HERE';
const TIMEZONE = 'Europe/London';

const EXPECTED_HEADERS = [
  'timestamp', 'event', 'game_slug', 'level', 'mode',
  'question_index', 'correct', 'attempts', 'score',
  'questions_answered', 'questions_correct', 'previous_score',
  'difficulty', 'filter_type', 'filter_value',
  // Appended 2026-08-26 — MUST stay at the end so existing column positions
  // (and every getRange/col[] lookup below) keep working. Rows written before
  // this date have both blank.
  //   client_ts — event time from the browser. The 'timestamp' column above is
  //               arrival time, and events race, so client_ts + seq is the only
  //               reliable ordering. Prefer it for any per-question analysis.
  //   seq       — per-page-load monotonic counter, breaks same-millisecond ties.
  'client_ts', 'seq'
];

// ============================================================
//  POST — receive events from games
// ============================================================
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = getOrCreateSheet();
    if (!data.event) return jsonResponse({ok: false, error: 'no event'});

    sheet.appendRow([
      new Date().toISOString(),
      cellValue(data.event), cellValue(data.game_slug), cellValue(data.level),
      cellValue(data.mode), cellValue(data.question_index), cellValue(data.correct),
      cellValue(data.attempts), cellValue(data.score), cellValue(data.questions_answered),
      cellValue(data.questions_correct), cellValue(data.previous_score),
      cellValue(data.difficulty), cellValue(data.filter_type), cellValue(data.filter_value),
      cellValue(data.client_ts), cellValue(data.seq)
    ]);

    var rowCount = sheet.getLastRow();
    if (rowCount > MAX_ROWS) sheet.deleteRows(2, Math.floor(MAX_ROWS * 0.1));
    return jsonResponse({ok: true});
  } catch (err) {
    return jsonResponse({ok: false, error: err.message});
  }
}

// ============================================================
//  GET — health check
// ============================================================
// Bump SCRIPT_VERSION whenever this file is redeployed. Hitting the /exec URL
// in a browser then tells you which code is actually live — without it there is
// no way to confirm a deploy landed, or which of several projects serves the URL.
const SCRIPT_VERSION = '2026-09-29-c';

function doGet(e) {
  return jsonResponse({
    status: 'ok',
    service: 'MaffsGames Analytics',
    sheet: SHEET_NAME,
    version: SCRIPT_VERSION
  });
}

// ============================================================
//  DAILY REPORT + DASHBOARD — runs at 7am UK time
// ============================================================
function sendDailyReport() {
  var sheet = getOrCreateSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  var col = {};
  headers.forEach(function(h, i) { col[h] = i; });

  var now = new Date();
  var yesterday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1);
  var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var weekAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7);
  var monthAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 30);

  var allRows = data.slice(1);
  var yesterdayRows = allRows.filter(function(r) { var t = new Date(r[col['timestamp']]); return t >= yesterday && t < today; });
  var weekRows = allRows.filter(function(r) { return new Date(r[col['timestamp']]) >= weekAgo; });
  var monthRows = allRows.filter(function(r) { return new Date(r[col['timestamp']]) >= monthAgo; });

  // ── Email from yesterday's data ──
  // The dashboard is deliberately rebuilt AFTER the email is sent. It used to
  // run first, which meant a flaky chart operation killed the daily report
  // before MailApp was ever reached — the report is the point, the charts are
  // decoration. See safeRebuildDashboard.
  if (yesterdayRows.length === 0) { safeRebuildDashboard(weekRows, monthRows, col); return; }

  var starts = yesterdayRows.filter(function(r) { return r[col['event']] === 'game_started'; });
  var completions = yesterdayRows.filter(function(r) { return r[col['event']] === 'game_completed'; });
  var abandons = yesterdayRows.filter(function(r) { return r[col['event']] === 'game_abandoned'; });
  var answers = yesterdayRows.filter(function(r) { return r[col['event']] === 'question_answered'; });
  var pbs = yesterdayRows.filter(function(r) { return r[col['event']] === 'personal_best_set'; });
  var correctAnswers = answers.filter(function(r) { return String(r[col['correct']]) === 'true'; });
  var overallAccuracy = answers.length > 0 ? Math.round(100 * correctAnswers.length / answers.length) : 0;

  var gameCounts = {}; var compCounts = {};
  starts.forEach(function(r) { var s = r[col['game_slug']]; gameCounts[s] = (gameCounts[s]||0)+1; });
  completions.forEach(function(r) { var s = r[col['game_slug']]; compCounts[s] = (compCounts[s]||0)+1; });
  var topGames = Object.keys(gameCounts).sort(function(a,b){return gameCounts[b]-gameCounts[a];}).slice(0,10);

  var qStats = {};
  answers.forEach(function(r) {
    var key = r[col['game_slug']] + ' | Q' + r[col['question_index']];
    if (!qStats[key]) qStats[key] = {total:0, correct:0};
    qStats[key].total++;
    if (String(r[col['correct']]) === 'true') qStats[key].correct++;
  });
  var hardest = Object.keys(qStats).filter(function(k){return qStats[k].total>=5;})
    .map(function(k){return{key:k,acc:Math.round(100*qStats[k].correct/qStats[k].total),n:qStats[k].total};})
    .sort(function(a,b){return a.acc-b.acc;}).slice(0,10);

  var levelCounts = {};
  starts.forEach(function(r) { var lv = r[col['level']]||'unknown'; levelCounts[lv]=(levelCounts[lv]||0)+1; });

  var dateStr = Utilities.formatDate(yesterday, TIMEZONE, 'dd MMM yyyy');
  var subject = 'MaffsGames Daily Report — ' + dateStr;
  var body = '';
  body += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  body += '  MAFFSGAMES DAILY REPORT\n';
  body += '  ' + dateStr + '\n';
  body += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n';
  body += 'OVERVIEW\n';
  body += '  Events logged:      ' + yesterdayRows.length + '\n';
  body += '  Games started:      ' + starts.length + '\n';
  body += '  Games completed:    ' + completions.length + '\n';
  body += '  Games abandoned:    ' + abandons.length + '\n';
  body += '  Completion rate:    ' + (starts.length>0?Math.round(100*completions.length/starts.length):0) + '%\n';
  body += '  Questions answered: ' + answers.length + '\n';
  body += '  Overall accuracy:   ' + overallAccuracy + '%\n';
  body += '  Personal bests:     ' + pbs.length + '\n\n';
  body += 'TOP GAMES (by starts)\n';
  topGames.forEach(function(slug, i) {
    var comp = compCounts[slug]||0;
    body += '  '+(i+1)+'. '+slug+' — '+gameCounts[slug]+' starts, '+comp+' completed ('+
      (gameCounts[slug]>0?Math.round(100*comp/gameCounts[slug]):0)+'%)\n';
  });
  body += '\nLEVEL BREAKDOWN\n';
  Object.keys(levelCounts).sort().forEach(function(lv) { body += '  '+lv+': '+levelCounts[lv]+' starts\n'; });
  if (hardest.length > 0) {
    body += '\nHARDEST QUESTIONS (lowest accuracy, min 5 attempts)\n';
    hardest.forEach(function(q,i) { body += '  '+(i+1)+'. '+q.key+' — '+q.acc+'% correct ('+q.n+' attempts)\n'; });
  }
  body += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  body += 'Dashboard: open "MaffsGames Events" in Drive → Dashboard tab\n';

  MailApp.sendEmail(REPORT_EMAIL, subject, body);

  safeRebuildDashboard(weekRows, monthRows, col);
}

// Chart operations (removeChart / newChart / insertChart) sporadically fail with
// "the JavaScript engine reported an unexpected error. Error code INTERNAL" —
// a Google-side V8 fault, not something this code can prevent. Observed roughly
// once a week (26 Aug 2026 07:50:50 among others).
//
// It is swallowed rather than thrown because the whole Dashboard sheet is cleared
// and rebuilt from scratch on every run, so a failed or half-built dashboard
// repairs itself within 24 hours. The daily email does not — it happens once and
// is gone. Never let the decoration take down the report.
function safeRebuildDashboard(weekRows, monthRows, col) {
  try {
    rebuildDashboard(weekRows, monthRows, col);
  } catch (err) {
    console.error('rebuildDashboard failed (dashboard will rebuild on the next run): ' + err);
  }
}

// ============================================================
//  DASHBOARD — auto-rebuilds with charts
// ============================================================
function rebuildDashboard(weekRows, monthRows, col) {
  var ss = SpreadsheetApp.open(DriveApp.getFilesByName(SHEET_NAME).next());
  var dash = ss.getSheetByName(DASH_NAME);
  if (dash) {
    dash.clear();
    // Remove existing charts
    dash.getCharts().forEach(function(c) { dash.removeChart(c); });
  } else {
    dash = ss.insertSheet(DASH_NAME);
  }

  var r = 1; // current row pointer

  // ── TITLE ──
  dash.getRange(r, 1).setValue('MaffsGames Dashboard').setFontSize(16).setFontWeight('bold');
  dash.getRange(r, 3).setValue('Last updated: ' + Utilities.formatDate(new Date(), TIMEZONE, 'dd MMM yyyy HH:mm'));
  r += 2;

  // ══════════════════════════════════════
  //  TABLE 1: Top Games (7 days)
  // ══════════════════════════════════════
  var weekStarts = weekRows.filter(function(x){return x[col['event']]==='game_started';});
  var weekComp = weekRows.filter(function(x){return x[col['event']]==='game_completed';});
  var gc = {}, cc = {};
  weekStarts.forEach(function(x){ var s=x[col['game_slug']]; gc[s]=(gc[s]||0)+1; });
  weekComp.forEach(function(x){ var s=x[col['game_slug']]; cc[s]=(cc[s]||0)+1; });
  var topSlugs = Object.keys(gc).sort(function(a,b){return gc[b]-gc[a];}).slice(0,15);

  var t1Start = r;
  dash.getRange(r, 1).setValue('Top Games — Last 7 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 4).setValues([['Game', 'Starts', 'Completed', 'Completion %']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  topSlugs.forEach(function(slug) {
    var comp = cc[slug]||0;
    var pct = gc[slug]>0 ? Math.round(100*comp/gc[slug]) : 0;
    dash.getRange(r, 1, 1, 4).setValues([[slug, gc[slug], comp, pct+'%']]);
    r++;
  });
  r++;

  // Chart 1: Top Games bar chart
  if (topSlugs.length > 0) {
    var chartRange = dash.getRange(t1Start+1, 1, topSlugs.length+1, 2);
    var chart1 = dash.newChart()
      .setChartType(Charts.ChartType.BAR)
      .addRange(chartRange)
      .setPosition(t1Start, 6, 0, 0)
      .setOption('title', 'Top Games — Last 7 Days')
      .setOption('legend', {position: 'none'})
      .setOption('width', 500).setOption('height', 300)
      .setOption('colors', ['#0ea5e9'])
      .build();
    dash.insertChart(chart1);
  }

  // ══════════════════════════════════════
  //  TABLE 2: Level Breakdown (7 days)
  // ══════════════════════════════════════
  var t2Start = r;
  var lc = {};
  weekStarts.forEach(function(x){ var lv=x[col['level']]||'unknown'; lc[lv]=(lc[lv]||0)+1; });
  dash.getRange(r, 1).setValue('Level Breakdown — Last 7 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 2).setValues([['Level', 'Starts']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  var levels = Object.keys(lc).sort();
  levels.forEach(function(lv) {
    dash.getRange(r, 1, 1, 2).setValues([[lv, lc[lv]]]);
    r++;
  });
  r++;

  // Chart 2: Level pie chart
  if (levels.length > 0) {
    var pieRange = dash.getRange(t2Start+1, 1, levels.length+1, 2);
    var chart2 = dash.newChart()
      .setChartType(Charts.ChartType.PIE)
      .addRange(pieRange)
      .setPosition(t2Start, 6, 0, 0)
      .setOption('title', 'Level Split — Last 7 Days')
      .setOption('width', 400).setOption('height', 280)
      .setOption('colors', ['#22c55e','#3b82f6','#f97316','#8b5cf6','#ef4444','#0ea5e9'])
      .build();
    dash.insertChart(chart2);
  }

  // ══════════════════════════════════════
  //  TABLE 3: Accuracy by Game (7 days)
  // ══════════════════════════════════════
  var weekAnswers = weekRows.filter(function(x){return x[col['event']]==='question_answered';});
  var accByGame = {};
  weekAnswers.forEach(function(x) {
    var s = x[col['game_slug']];
    if (!accByGame[s]) accByGame[s] = {total:0, correct:0};
    accByGame[s].total++;
    if (String(x[col['correct']]) === 'true') accByGame[s].correct++;
  });
  var accSlugs = Object.keys(accByGame).filter(function(k){return accByGame[k].total>=5;})
    .sort(function(a,b){
      return (accByGame[a].correct/accByGame[a].total) - (accByGame[b].correct/accByGame[b].total);
    }).slice(0, 15);

  var t3Start = r;
  dash.getRange(r, 1).setValue('Accuracy by Game — Last 7 Days (min 5 answers)').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 4).setValues([['Game', 'Answers', 'Correct', 'Accuracy %']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  accSlugs.forEach(function(slug) {
    var d = accByGame[slug];
    var pct = Math.round(100*d.correct/d.total);
    dash.getRange(r, 1, 1, 4).setValues([[slug, d.total, d.correct, pct+'%']]);
    r++;
  });
  r++;

  // Chart 3: Accuracy bar chart
  if (accSlugs.length > 0) {
    var accData = [[' Game', 'Accuracy %']];
    accSlugs.forEach(function(slug) {
      accData.push([slug, Math.round(100*accByGame[slug].correct/accByGame[slug].total)]);
    });
    var accRange = dash.getRange(t3Start+1, 1, accSlugs.length+1, 1);
    // Build from the table data (cols 1 and 4)
    var chart3 = dash.newChart()
      .setChartType(Charts.ChartType.BAR)
      .addRange(dash.getRange(t3Start+1, 1, accSlugs.length+1, 1))
      .addRange(dash.getRange(t3Start+1, 4, accSlugs.length+1, 1))
      .setPosition(t3Start, 6, 0, 0)
      .setOption('title', 'Accuracy by Game (sorted lowest first)')
      .setOption('legend', {position: 'none'})
      .setOption('width', 500).setOption('height', 300)
      .setOption('colors', ['#f97316'])
      .setOption('hAxis', {minValue: 0, maxValue: 100})
      .build();
    dash.insertChart(chart3);
  }

  // ══════════════════════════════════════
  //  TABLE 4: Hardest Questions (7 days)
  // ══════════════════════════════════════
  var qStats = {};
  weekAnswers.forEach(function(x) {
    var key = x[col['game_slug']] + ' Q' + x[col['question_index']];
    if (!qStats[key]) qStats[key] = {total:0, correct:0, game:x[col['game_slug']], qi:x[col['question_index']]};
    qStats[key].total++;
    if (String(x[col['correct']]) === 'true') qStats[key].correct++;
  });
  var hardest = Object.keys(qStats).filter(function(k){return qStats[k].total>=5;})
    .sort(function(a,b){return (qStats[a].correct/qStats[a].total)-(qStats[b].correct/qStats[b].total);})
    .slice(0, 15);

  dash.getRange(r, 1).setValue('Hardest Questions — Last 7 Days (min 5 attempts)').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 4).setValues([['Game + Question', 'Attempts', 'Correct', 'Accuracy %']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  hardest.forEach(function(key) {
    var d = qStats[key];
    dash.getRange(r, 1, 1, 4).setValues([[key, d.total, d.correct, Math.round(100*d.correct/d.total)+'%']]);
    r++;
  });
  r += 2;

  // ══════════════════════════════════════
  //  TABLE 5: Daily Activity (30 days)
  // ══════════════════════════════════════
  var monthStarts = monthRows.filter(function(x){return x[col['event']]==='game_started';});
  var dailyCounts = {};
  monthStarts.forEach(function(x) {
    var d = Utilities.formatDate(new Date(x[col['timestamp']]), TIMEZONE, 'yyyy-MM-dd');
    dailyCounts[d] = (dailyCounts[d]||0)+1;
  });
  var days = Object.keys(dailyCounts).sort();

  var t5Start = r;
  dash.getRange(r, 1).setValue('Daily Activity — Last 30 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 2).setValues([['Date', 'Games Started']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  days.forEach(function(d) {
    dash.getRange(r, 1, 1, 2).setValues([[d, dailyCounts[d]]]);
    r++;
  });

  // Chart 5: Daily activity line chart
  if (days.length > 1) {
    var lineRange = dash.getRange(t5Start+1, 1, days.length+1, 2);
    var chart5 = dash.newChart()
      .setChartType(Charts.ChartType.LINE)
      .addRange(lineRange)
      .setPosition(t5Start, 6, 0, 0)
      .setOption('title', 'Daily Games Started — Last 30 Days')
      .setOption('legend', {position: 'none'})
      .setOption('width', 500).setOption('height', 280)
      .setOption('colors', ['#0ea5e9'])
      .setOption('curveType', 'function')
      .build();
    dash.insertChart(chart5);
  }

  // ── Formatting ──
  dash.setColumnWidth(1, 220);
  dash.setColumnWidth(2, 80);
  dash.setColumnWidth(3, 80);
  dash.setColumnWidth(4, 100);
  dash.setTabColor('#0ea5e9');
}

// ============================================================
//  AUTO-SETUP — creates daily trigger on first run
// ============================================================
function setupTrigger() {
  var triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(function(trigger) {
    if (trigger.getHandlerFunction() === 'sendDailyReport') ScriptApp.deleteTrigger(trigger);
  });
  ScriptApp.newTrigger('sendDailyReport')
    .timeBased().atHour(7).everyDays(1).inTimezone(TIMEZONE).create();
}

// ============================================================
//  MANUAL TEST — run this to test dashboard without waiting
// ============================================================
function testDashboard() {
  var sheet = getOrCreateSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  var col = {};
  headers.forEach(function(h, i) { col[h] = i; });
  var now = new Date();
  var weekAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7);
  var monthAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 30);
  var allRows = data.slice(1);
  var weekRows = allRows.filter(function(r) { return new Date(r[col['timestamp']]) >= weekAgo; });
  var monthRows = allRows.filter(function(r) { return new Date(r[col['timestamp']]) >= monthAgo; });
  rebuildDashboard(weekRows, monthRows, col);
}

// ============================================================
//  HELPERS
// ============================================================
function getOrCreateSheet() {
  var files = DriveApp.getFilesByName(SHEET_NAME);
  var ss;
  if (files.hasNext()) {
    ss = SpreadsheetApp.open(files.next());
  } else {
    ss = SpreadsheetApp.create(SHEET_NAME);
  }
  var sheet = ss.getActiveSheet();
  ensureHeaders(sheet);
  return sheet;
}

// Row 1 must match EXPECTED_HEADERS exactly, otherwise filters like
// col['timestamp'] return undefined and sendDailyReport silently exits.
function ensureHeaders(sheet) {
  var range = sheet.getRange(1, 1, 1, EXPECTED_HEADERS.length);
  var current = range.getValues()[0];
  var mismatch = EXPECTED_HEADERS.some(function(h, i) { return current[i] !== h; });
  if (!mismatch) return;
  range.setValues([EXPECTED_HEADERS]).setFontWeight('bold');
  sheet.setFrozenRows(1);
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// A field is genuinely missing only when it is undefined or null. Every other
// value — including false and 0, both falsy in JS — is a real, sent value and
// must be written as-is. `x || ''` treated false/0 the same as missing, which
// silently blanked every wrong answer's `correct: false` and any
// `question_index: 0` / `score: 0` row. See docs/todo.md 1.25 and
// docs/sheets-falsy-backfill.md.
function cellValue(v) {
  return (v === undefined || v === null) ? '' : v;
}
