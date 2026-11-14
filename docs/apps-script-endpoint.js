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
  'client_ts', 'seq',
  // Appended 2026-11-03 (contract QUESTION-ID) — also at the end, for the same reason. Rows written before
  // the redeploy have it blank.
  //   question_id — which question a question_answered event was about: the game's own id, or "h" + the
  //                 8-hex FNV-1a hash of the prompt's text (analytics.js; the text itself is never sent).
  //                 scripts/decode-question-ids.py <slug> maps an id back to its question.
  'question_id',
  // Appended 2026-11-07 (contract ROOM-TIMES) — also at the end. Rows written before the redeploy have it blank.
  //   detail — sent by two callers. The escape-room engine: the lock id on question_answered, lock:step on
  //            hint_used, fresh/resumed on game_started, and on game_completed the outcome, wrongs, hints and the
  //            times ("escaped wrongs:1 hints:2 used:612 played:567 locks:182,431,567"; canon §1.3). The portal's
  //            score ticker: high, weekly or plain on ticker_clicked (contract TICKER-LINKS, 7 Nov 2026).
  'detail'
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
      cellValue(data.client_ts), cellValue(data.seq),
      cellValue(data.question_id), cellValue(data.detail)
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
const SCRIPT_VERSION = '2026-11-14-b';

function doGet(e) {
  return jsonResponse({
    status: 'ok',
    service: 'MaffsGames Analytics',
    sheet: SHEET_NAME,
    version: SCRIPT_VERSION
  });
}

// ============================================================
//  WHAT A ROW MEANS — the report's model (contract DASHBOARD-METRICS, Jon, 3 Nov 2026)
// ============================================================
// Each kind of game is measured by what its question_answered means:
//   question — correct says whether an answer was right: accuracy, and hardest questions by question_id;
//   shot     — correct says whether an attempt hit (Trig Wars): left out of accuracy, named on one line;
//   room     — an escape room logs correct once per lock opened and every wrong try: escapes, and attempts per lock.
// A game's kind lives in its one metadata record, data/games.json ("answer_kind", "question" when absent), read from
// GitHub at report time (Jon, Amendment 2: data/ is not published on the site). A room is any slug starting
// "escape-". Never a list of slugs in this file.
const GAMES_JSON_URL = 'https://raw.githubusercontent.com/OrthogonalMaffs/maffsgames/main/data/games.json';
const RPT_MIN_GAME_ANSWERS = 30;      // accuracy by game: one student's session cannot fill the table
const RPT_MIN_QUESTION_ATTEMPTS = 10; // hardest questions
// Before this instant a wrong answer was stored blank (cellValue's falsy bug, fixed 29 Sep 2026 about 20:00 UTC), so
// a blank `correct` from then counts as wrong. After it, a blank means the item has no right answer (Prisoner's
// Dilemma sends correct: null) and the row is not marked.
const RPT_BLANK_WAS_WRONG_UNTIL = new Date('2026-09-29T20:00:00Z');
var rptKindsCache = null;

// SAFE TALLIES (contract COUNTS-SAFE-TALLY, 14 Nov 2026). A game_slug, level or question_id is whatever was posted,
// by anyone, and the report uses it as a key. In a plain object a key such as "constructor" or "__proto__" reads a
// built-in member, so a tally started from a function and became text, or wrote into the built-in itself. Every
// report-side object keyed by event data is therefore a map with no prototype (rptMap), read through
// hasOwnProperty (rptHas, rptGet) and counted with rptAdd. doPost uses none of this: it writes cells, not keys.
function rptMap() { return Object.create(null); }
function rptHas(m, k) { return Object.prototype.hasOwnProperty.call(m, k); }
function rptGet(m, k, otherwise) { return rptHas(m, k) ? m[k] : otherwise; }
function rptAdd(m, k) { m[k] = rptGet(m, k, 0) + 1; }

// games.json, fetched once per run. If the fetch fails, every game is treated as a question game and the report
// says so in one line (Jon's contract): the report still goes out.
function rptLoadKinds() {
  if (rptKindsCache) return rptKindsCache;
  var kinds = rptMap(), ok = false;
  try {
    var res = UrlFetchApp.fetch(GAMES_JSON_URL, {muteHttpExceptions: true});
    if (res.getResponseCode() === 200) {
      JSON.parse(res.getContentText()).games.forEach(function(g) {
        kinds[g.slug] = g.answer_kind === 'shot' ? 'shot' : 'question';
      });
      ok = true;
    }
  } catch (err) {
    console.error('games.json could not be read: ' + err);
  }
  rptKindsCache = {ok: ok, kinds: ok ? kinds : rptMap()};
  return rptKindsCache;
}

function rptKind(slug, kinds) {
  if (String(slug).indexOf('escape-') === 0) return 'room';
  return rptGet(kinds.kinds, slug, '') === 'shot' ? 'shot' : 'question';
}

// true, false, or null when the row cannot be marked (see RPT_BLANK_WAS_WRONG_UNTIL).
function rptMarked(x, col) {
  var c = String(x[col['correct']]);
  if (c === 'true') return true;
  if (c === 'false') return false;
  if (c === '' && new Date(x[col['timestamp']]) < RPT_BLANK_WAS_WRONG_UNTIL) return false;
  return null;
}

// A room's game_completed is sent when the room ends, escaped or out of time (engine.js finish(win)); it is an
// escape only when every lock opened: questions_correct (locks opened) equals questions_answered (locks), both
// numbers above 0 (contract ROOM-ESCAPED, Jon, 4 Nov 2026). Any other completion is a timeout.
function rptEscaped(x, col) {
  var a = x[col['questions_answered']], c = x[col['questions_correct']];
  return typeof a === 'number' && typeof c === 'number' && a > 0 && c === a;
}

// Everything the email and the Dashboard say about answers, from one set of rows.
function rptBuild(rows, col, kinds) {
  var games = rptMap(), qs = rptMap(), rooms = rptMap(), shots = rptMap(), idGames = rptMap(), overall = {total: 0, correct: 0};
  rows.forEach(function(x) {
    var ev = x[col['event']], slug = String(x[col['game_slug']]), kind = rptKind(slug, kinds);
    if (kind === 'room') {
      if (!rptHas(rooms, slug)) rooms[slug] = {slug: slug, starts: 0, escaped: 0, timedOut: 0, marked: 0, correct: 0};
      var rm = rooms[slug];
      if (ev === 'game_started') rm.starts++;
      else if (ev === 'game_completed') { if (rptEscaped(x, col)) rm.escaped++; else rm.timedOut++; }
      else if (ev === 'question_answered') {
        var rk = rptMarked(x, col);
        if (rk !== null) { rm.marked++; if (rk) rm.correct++; }
      }
      return;
    }
    if (ev !== 'question_answered') return;
    if (kind === 'shot') { shots[slug] = true; return; }
    var m = rptMarked(x, col);
    if (m === null) return;
    if (!rptHas(games, slug)) games[slug] = {slug: slug, total: 0, correct: 0};
    var g = games[slug];
    g.total++; overall.total++;
    if (m) { g.correct++; overall.correct++; }
    var qid = col['question_id'] === undefined ? '' : String(x[col['question_id']]);
    if (!qid) return;
    idGames[slug] = true;
    var level = String(x[col['level']]), key = slug + '|' + level + '|' + qid;
    if (!rptHas(qs, key)) qs[key] = {slug: slug, level: level, qid: qid, total: 0, correct: 0};
    var q = qs[key];
    q.total++;
    if (m) q.correct++;
  });
  var lowest = function(a, b) { return a.correct / a.total - b.correct / b.total; };
  var roomList = Object.keys(rooms).map(function(k) { return rooms[k]; });
  roomList.forEach(function(r) {
    r.rate = r.starts > 0 ? r.escaped / r.starts : null;
    r.perLock = r.correct > 0 ? r.marked / r.correct : null;
  });
  roomList.sort(function(a, b) {
    return (a.rate === null ? 2 : a.rate) - (b.rate === null ? 2 : b.rate) || (a.slug < b.slug ? -1 : 1);
  });
  return {
    kindsOk: kinds.ok,
    overall: overall,
    games: Object.keys(games).map(function(k) { return games[k]; })
      .filter(function(g) { return g.total >= RPT_MIN_GAME_ANSWERS; }).sort(lowest).slice(0, 15),
    hardest: Object.keys(qs).map(function(k) { return qs[k]; })
      .filter(function(q) { return q.total >= RPT_MIN_QUESTION_ATTEMPTS; }).sort(lowest).slice(0, 15),
    idGames: Object.keys(idGames).length,
    rooms: roomList,
    shots: Object.keys(shots).sort()
  };
}

function rptPct(n, d) { return d > 0 ? Math.round(100 * n / d) + '%' : 'n/a'; }

// The report's lines, shared by the email and the Dashboard so the two always say the same thing.
function rptKindsLine(rep) {
  return rep.kindsOk ? '' : 'games.json could not be read, so every game is counted as a question game today.';
}
function rptShotsLine(rep) {
  return rep.shots.length ? 'Left out of accuracy (a correct answer there is a hit, not a right answer): ' + rep.shots.join(', ') + '.' : '';
}
function rptHardestHeading(rep, window) {
  return 'Hardest Questions — ' + window + ' (question games, by question_id, min ' + RPT_MIN_QUESTION_ATTEMPTS +
    ' attempts; ' + rep.idGames + (rep.idGames === 1 ? ' game sends' : ' games send') + ' question_id so far)';
}

// The email's answer sections.
function rptEmailText(rep) {
  var t = '';
  if (rptKindsLine(rep)) t += rptKindsLine(rep) + '\n\n';
  t += 'ACCURACY BY GAME (question games, min ' + RPT_MIN_GAME_ANSWERS + ' marked answers, lowest first)\n';
  if (!rep.games.length) t += '  None reached ' + RPT_MIN_GAME_ANSWERS + ' answers.\n';
  rep.games.forEach(function(g, i) {
    t += '  ' + (i + 1) + '. ' + g.slug + ' — ' + rptPct(g.correct, g.total) + ' correct (' + g.total + ' answers)\n';
  });
  t += '\n' + rptHardestHeading(rep, 'yesterday').toUpperCase() + '\n';
  if (!rep.hardest.length) t += '  None reached ' + RPT_MIN_QUESTION_ATTEMPTS + ' attempts.\n';
  rep.hardest.forEach(function(q, i) {
    t += '  ' + (i + 1) + '. ' + q.slug + ' · ' + q.level + ' · ' + q.qid + ' — ' + rptPct(q.correct, q.total) +
      ' correct (' + q.total + ' attempts)\n';
  });
  if (rep.hardest.length) t += '  Decode an id: python scripts/decode-question-ids.py <game> --id <id>\n';
  t += '\nESCAPE ROOMS (lowest escape rate first)\n';
  if (!rep.rooms.length) t += '  None played.\n';
  rep.rooms.forEach(function(r, i) {
    t += '  ' + (i + 1) + '. ' + r.slug + ' — ' + r.starts + ' started, ' + r.escaped + ' escaped (' + rptPct(r.escaped, r.starts) +
      '), ' + r.timedOut + ' timed out, ' + (r.perLock === null ? 'no lock opened' : r.perLock.toFixed(1) + ' attempts per lock opened') + '\n';
  });
  if (rptShotsLine(rep)) t += '\n' + rptShotsLine(rep) + '\n';
  return t;
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
  var kinds = rptLoadKinds();
  if (yesterdayRows.length === 0) { safeRebuildDashboard(weekRows, monthRows, col, kinds); return; }

  var starts = yesterdayRows.filter(function(r) { return r[col['event']] === 'game_started'; });
  var completions = yesterdayRows.filter(function(r) { return r[col['event']] === 'game_completed'; });
  var abandons = yesterdayRows.filter(function(r) { return r[col['event']] === 'game_abandoned'; });
  var answers = yesterdayRows.filter(function(r) { return r[col['event']] === 'question_answered'; });
  var pbs = yesterdayRows.filter(function(r) { return r[col['event']] === 'personal_best_set'; });
  var rep = rptBuild(yesterdayRows, col, kinds);

  var gameCounts = rptMap(); var compCounts = rptMap();
  starts.forEach(function(r) { rptAdd(gameCounts, r[col['game_slug']]); });
  completions.forEach(function(r) { rptAdd(compCounts, r[col['game_slug']]); });
  var topGames = Object.keys(gameCounts).sort(function(a,b){return gameCounts[b]-gameCounts[a];}).slice(0,10);

  var levelCounts = rptMap();
  starts.forEach(function(r) { rptAdd(levelCounts, r[col['level']]||'unknown'); });

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
  body += '  Overall accuracy:   ' + rptPct(rep.overall.correct, rep.overall.total) + ' (question games, ' + rep.overall.total + ' marked answers)\n';
  body += '  Personal bests:     ' + pbs.length + '\n\n';
  body += 'TOP GAMES (by starts)\n';
  topGames.forEach(function(slug, i) {
    var comp = rptGet(compCounts, slug, 0);
    body += '  '+(i+1)+'. '+slug+' — '+gameCounts[slug]+' starts, '+comp+' completed ('+
      (gameCounts[slug]>0?Math.round(100*comp/gameCounts[slug]):0)+'%)\n';
  });
  body += '\nLEVEL BREAKDOWN\n';
  Object.keys(levelCounts).sort().forEach(function(lv) { body += '  '+lv+': '+levelCounts[lv]+' starts\n'; });
  body += '\n' + rptEmailText(rep);
  body += '\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n';
  body += 'Dashboard: open "MaffsGames Events" in Drive → Dashboard tab\n';

  MailApp.sendEmail(REPORT_EMAIL, subject, body);

  safeRebuildDashboard(weekRows, monthRows, col, kinds);
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
function safeRebuildDashboard(weekRows, monthRows, col, kinds) {
  try {
    rebuildDashboard(weekRows, monthRows, col, kinds);
  } catch (err) {
    console.error('rebuildDashboard failed (dashboard will rebuild on the next run): ' + err);
  }
}

// ============================================================
//  DASHBOARD — auto-rebuilds with charts
// ============================================================
function rebuildDashboard(weekRows, monthRows, col, kinds) {
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
  var rep = rptBuild(weekRows, col, kinds || rptLoadKinds());
  [rptKindsLine(rep), rptShotsLine(rep)].forEach(function(line) {
    if (line) { dash.getRange(r, 1).setValue(line).setFontStyle('italic'); r++; }
  });
  if (rptKindsLine(rep) || rptShotsLine(rep)) r++;

  // ══════════════════════════════════════
  //  TABLE 1: Top Games (7 days)
  // ══════════════════════════════════════
  var weekStarts = weekRows.filter(function(x){return x[col['event']]==='game_started';});
  var weekComp = weekRows.filter(function(x){return x[col['event']]==='game_completed';});
  var gc = rptMap(), cc = rptMap();
  weekStarts.forEach(function(x){ rptAdd(gc, x[col['game_slug']]); });
  weekComp.forEach(function(x){ rptAdd(cc, x[col['game_slug']]); });
  var topSlugs = Object.keys(gc).sort(function(a,b){return gc[b]-gc[a];}).slice(0,15);

  var t1Start = r;
  dash.getRange(r, 1).setValue('Top Games — Last 7 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 4).setValues([['Game', 'Starts', 'Completed', 'Completion %']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  topSlugs.forEach(function(slug) {
    var comp = rptGet(cc, slug, 0);
    var frac = gc[slug]>0 ? comp/gc[slug] : 0;
    dash.getRange(r, 1, 1, 4).setValues([[slug, gc[slug], comp, frac].map(cellValue)]);
    r++;
  });
  formatPercentColumn(dash, t1Start+2, topSlugs.length);
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
    r = rowBelowChart(r, t1Start, 300);
  }

  // ══════════════════════════════════════
  //  TABLE 2: Level Breakdown (7 days)
  // ══════════════════════════════════════
  var t2Start = r;
  var lc = rptMap();
  weekStarts.forEach(function(x){ rptAdd(lc, x[col['level']]||'unknown'); });
  dash.getRange(r, 1).setValue('Level Breakdown — Last 7 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 2).setValues([['Level', 'Starts']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  var levels = Object.keys(lc).sort();
  levels.forEach(function(lv) {
    dash.getRange(r, 1, 1, 2).setValues([[lv, lc[lv]].map(cellValue)]);
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
    r = rowBelowChart(r, t2Start, 280);
  }

  // ══════════════════════════════════════
  //  TABLE 3: Accuracy by Game (7 days) — question games only
  // ══════════════════════════════════════
  var t3Start = r;
  dash.getRange(r, 1).setValue('Accuracy by Game — Last 7 Days (question games, min ' + RPT_MIN_GAME_ANSWERS + ' marked answers; overall ' +
    rptPct(rep.overall.correct, rep.overall.total) + ' of ' + rep.overall.total + ')').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 4).setValues([['Game', 'Answers', 'Correct', 'Accuracy %']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  rep.games.forEach(function(g) {
    dash.getRange(r, 1, 1, 4).setValues([[g.slug, g.total, g.correct, g.correct/g.total].map(cellValue)]);
    r++;
  });
  formatPercentColumn(dash, t3Start+2, rep.games.length);
  r++;

  // Chart 3: Accuracy bar chart
  if (rep.games.length > 0) {
    // Built from the table data (cols 1 and 4); col 4 holds fractions, so the axis runs 0 to 1

    var chart3 = dash.newChart()
      .setChartType(Charts.ChartType.BAR)
      .addRange(dash.getRange(t3Start+1, 1, rep.games.length+1, 1))
      .addRange(dash.getRange(t3Start+1, 4, rep.games.length+1, 1))
      .setPosition(t3Start, 6, 0, 0)
      .setOption('title', 'Accuracy by Game (sorted lowest first)')
      .setOption('legend', {position: 'none'})
      .setOption('width', 500).setOption('height', 300)
      .setOption('colors', ['#f97316'])
      .setOption('hAxis', {minValue: 0, maxValue: 1, format: 'percent'})
      .build();
    dash.insertChart(chart3);
    r = rowBelowChart(r, t3Start, 300);
  }

  // ══════════════════════════════════════
  //  TABLE 4: Hardest Questions (7 days) — named by question_id, not round position
  // ══════════════════════════════════════
  var t4Start = r;
  dash.getRange(r, 1).setValue(rptHardestHeading(rep, 'Last 7 Days')).setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 6).setValues([['Game', 'Level', 'Question id', 'Attempts', 'Correct', 'Accuracy %']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  rep.hardest.forEach(function(q) {
    dash.getRange(r, 1, 1, 6).setValues([[q.slug, q.level, q.qid, q.total, q.correct, q.correct/q.total].map(cellValue)]);
    r++;
  });
  if (rep.hardest.length > 0) dash.getRange(t4Start+2, 6, rep.hardest.length, 1).setNumberFormat('0%');
  dash.getRange(r, 1).setValue('Decode an id: python scripts/decode-question-ids.py <game> --id <id>').setFontStyle('italic');
  r += 2;

  // ══════════════════════════════════════
  //  TABLE 4b: Escape Rooms (7 days) — escapes, not accuracy
  // ══════════════════════════════════════
  var t4bStart = r;
  dash.getRange(r, 1).setValue('Escape Rooms — Last 7 Days (lowest escape rate first)').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 6).setValues([['Room', 'Started', 'Escaped', 'Escape %', 'Timed out', 'Attempts per lock']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  rep.rooms.forEach(function(rm) {
    dash.getRange(r, 1, 1, 6).setValues([[rm.slug, rm.starts, rm.escaped, rm.rate === null ? '' : rm.rate, rm.timedOut,
      rm.perLock === null ? '' : Math.round(rm.perLock * 10) / 10].map(cellValue)]);
    r++;
  });
  formatPercentColumn(dash, t4bStart+2, rep.rooms.length);
  r += 2;

  // ══════════════════════════════════════
  //  TABLE 5: Daily Activity (30 days)
  // ══════════════════════════════════════
  var monthStarts = monthRows.filter(function(x){return x[col['event']]==='game_started';});
  var dailyCounts = rptMap();
  monthStarts.forEach(function(x) {
    rptAdd(dailyCounts, Utilities.formatDate(new Date(x[col['timestamp']]), TIMEZONE, 'yyyy-MM-dd'));
  });
  var days = Object.keys(dailyCounts).sort();

  var t5Start = r;
  dash.getRange(r, 1).setValue('Daily Activity — Last 30 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 2).setValues([['Date', 'Games Started']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  days.forEach(function(d) {
    dash.getRange(r, 1, 1, 2).setValues([[d, dailyCounts[d]].map(cellValue)]);
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
    r = rowBelowChart(r, t5Start, 280);
  }

  // ── Formatting ──
  dash.setColumnWidth(1, 220);
  dash.setColumnWidth(2, 80);
  dash.setColumnWidth(3, 80);
  dash.setColumnWidth(4, 100);
  dash.setTabColor('#0ea5e9');
}

// Percentages are written as fractions (0.17) and shown as 17% by the cell
// format, so a chart reading the column gets numbers from 0 to 1.
function formatPercentColumn(dash, firstRow, n) {
  if (n > 0) dash.getRange(firstRow, 4, n, 1).setNumberFormat('0%');
}

// Charts are anchored at their table's first row but have a fixed pixel height,
// while a table's height varies by day. Return the first free row below both
// the table (r) and its chart, plus one blank row, so the next section never
// starts underneath the chart.
const DEFAULT_ROW_PX = 21; // a Sheets row at the default height
function rowBelowChart(r, tStart, chartPx) {
  return Math.max(r, tStart + Math.ceil(chartPx / DEFAULT_ROW_PX) + 1);
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
  rebuildDashboard(weekRows, monthRows, col, rptLoadKinds());
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
//
// A posted value is data, never a formula (contract SHEET-FORMULA-CELLS, 14 Nov 2026). appendRow and setValues read
// a string as if a person had typed it, so one beginning "=" became a live formula, placed by anyone who posted an
// event; IMAGE or IMPORTDATA in one can send the Sheet's contents to an outside address. A string whose first
// character is =, +, @, a tab or a carriage return, or "-" not followed by a plain number, is written behind a
// leading apostrophe: Sheets keeps it as text, and the apostrophe is not part of the value read back. Numbers,
// booleans and every other string are written as they were. An array or object (no page sends one) is written as
// its JSON text, which begins "[" or "{", rather than left to whatever Sheets makes of it.
// Every cell of posted text goes through here: doPost's row, and the Dashboard's rows, which write slugs, levels
// and question ids read back from the Sheet.
function cellValue(v) {
  if (v === undefined || v === null) return '';
  if (typeof v === 'object') v = JSON.stringify(v);
  if (typeof v === 'string' && (/^[=+@\t\r]/.test(v) || (v.charAt(0) === '-' && !/^-\d+(\.\d+)?$/.test(v)))) return "'" + v;
  return v;
}
