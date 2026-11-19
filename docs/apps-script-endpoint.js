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
const SCRIPT_VERSION = '2026-11-19-a';

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
  // The 7 days before weekAgo: the Dashboard's "previous 7 days" (DASHBOARD-GLANCE).
  var prevWeekAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 14);
  var prevWeekRows = allRows.filter(function(r) { var t = new Date(r[col['timestamp']]); return t >= prevWeekAgo && t < weekAgo; });

  // ── Email from yesterday's data ──
  // The dashboard is deliberately rebuilt AFTER the email is sent. It used to
  // run first, which meant a flaky chart operation killed the daily report
  // before MailApp was ever reached — the report is the point, the charts are
  // decoration. See safeRebuildDashboard.
  var kinds = rptLoadKinds();
  if (yesterdayRows.length === 0) { safeRebuildDashboard(weekRows, monthRows, col, kinds, prevWeekRows); return; }

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

  safeRebuildDashboard(weekRows, monthRows, col, kinds, prevWeekRows);
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
function safeRebuildDashboard(weekRows, monthRows, col, kinds, prevWeekRows) {
  try {
    rebuildDashboard(weekRows, monthRows, col, kinds, prevWeekRows);
  } catch (err) {
    console.error('rebuildDashboard failed (dashboard will rebuild on the next run): ' + err);
  }
}

// ============================================================
//  DASHBOARD AT A GLANCE (contract DASHBOARD-GLANCE, Jon, 18 Nov 2026)
// ============================================================
// The Dashboard answers the questions Jon asks most weeks, in this order: is it growing (A), is anything broken (B),
// are teachers using it (C), did my posts bring visitors (D), who uses it (E), is my newest game landing (F), then
// escape rooms (G), Misunderstood Maths (H), the older tables (I) and Daily Activity (J). Sheet rows are classed by
// rptKind exactly as rptBuild classes them. The GA4 tabs (docs/apps-script-ga4-country.js) are read by name and never
// written; a missing or empty one gives one line, RPT_GA4_MISSING, in each section that uses it. GA4 figures run to
// the last complete day: "7 days" there is the 7 dates before today, and the previous 7 the dates before those.
const RPT_CHECK_MIN = 10;          // B1: marked answers before a question can be flagged
const RPT_CHECK_PCT = 0.10;        // B1: flagged when under this share right
const RPT_QUIT_MIN = 10;           // B2: game_abandoned rows before a game is listed
const RPT_CLASS_STARTS = 10;       // C1: starts of one game in one run
const RPT_CLASS_GAP_MIN = 30;      // C1: minutes allowed between one start and the next
const RPT_NEW_GAME_DAYS = 14;      // F
const RPT_LAUNCH_URL = 'https://raw.githubusercontent.com/OrthogonalMaffs/maffsgames/main/schools/assets/launch-dates.json';
const RPT_GA4_DAILY = 'GA4 country daily';
const RPT_GA4_SOURCES = 'GA4 sources daily';
const RPT_GA4_MISSING = 'GA4 figures not available yet.';
// D1's channels, matched in RPT_CHANNELS order, case-insensitive: a source "contains" one of these words.
const RPT_CH_GOOGLE = ['google'];
const RPT_CH_LINKEDIN = ['linkedin', 'lnkd'];
const RPT_CH_FACEBOOK = ['facebook', 'fb'];
const RPT_CH_TES = ['tes.com'];
const RPT_CH_DIRECT = '(direct)';
const RPT_CH_ORGANIC = 'organic';
const RPT_CHANNELS = ['Google search', 'Other search', 'LinkedIn', 'Facebook', 'Tes', 'Direct', 'Other'];
const RPT_UP = '#15803d', RPT_DOWN = '#b91c1c', RPT_GREY = '#6b7280', RPT_FLAG_BG = '#fee2e2';
var rptLaunchCache = null;

function rptDay(d) { return Utilities.formatDate(d, TIMEZONE, 'yyyy-MM-dd'); }

// Day keys: today, 7 days ago (weekRows' start), 14 days ago (prevWeekRows' start), and F's launch cut-off.
function rptWindows() {
  var now = new Date();
  var at = function(n) { return rptDay(new Date(now.getFullYear(), now.getMonth(), now.getDate() - n)); };
  return {today: at(0), week: at(7), prev: at(14), launch: at(RPT_NEW_GAME_DAYS)};
}

// Cells, every one through cellValue.
function rptTitle(dash, r, text) { dash.getRange(r, 1).setValue(cellValue(text)).setFontWeight('bold').setFontSize(11); return r + 1; }
function rptHead(dash, r, cells) {
  dash.getRange(r, 1, 1, cells.length).setValues([cells.map(cellValue)]).setFontWeight('bold').setBackground('#f0f0f0');
  return r + 1;
}
function rptLine(dash, r, text) { dash.getRange(r, 1).setValue(cellValue(text)).setFontStyle('italic'); return r + 1; }
function rptRow(dash, r, cells) { return dash.getRange(r, 1, 1, cells.length).setValues([cells.map(cellValue)]); }

// ▲, ▼ or ▬ and the % change against the earlier figure, "new" when that was 0. dir: 1 up, -1 down, 0 neither.
function rptChange(cur, prev) {
  if (prev === 0) return cur === 0 ? {text: '▬ 0%', dir: 0} : {text: '▲ new', dir: 1};
  var dir = cur > prev ? 1 : cur < prev ? -1 : 0;
  return {text: (dir > 0 ? '▲ ' : dir < 0 ? '▼ ' : '▬ ') + Math.abs(Math.round(100 * (cur - prev) / prev)) + '%', dir: dir};
}
// % correct moves in percentage points (a rate's own % change would read as a second rate).
function rptPointsChange(cur, prev) {
  if (cur === null) return {text: 'n/a', dir: 0};
  if (prev === null) return {text: '▲ new', dir: 1};
  var p = Math.round(100 * cur) - Math.round(100 * prev);
  return {text: (p > 0 ? '▲ ' : p < 0 ? '▼ ' : '▬ ') + Math.abs(p) + ' pts', dir: p > 0 ? 1 : p < 0 ? -1 : 0};
}
function rptDirColour(dir) { return dir > 0 ? RPT_UP : dir < 0 ? RPT_DOWN : RPT_GREY; }

// One GA4 tab as objects keyed by its row-1 headings, each date as 'yyyy-MM-dd'; null when the tab is missing or
// holds no rows. Read only.
function rptGa4Tab(ss, name) {
  var tab = ss.getSheetByName(name);
  if (!tab) return null;
  var v = tab.getDataRange().getValues();
  if (v.length < 2) return null;
  var head = v[0].map(String);
  var rows = v.slice(1).filter(function(row) { return row.join('') !== ''; }).map(function(row) {
    var o = rptMap();
    head.forEach(function(h, i) { o[h] = row[i]; });
    var d = o['date'];
    o['date'] = Object.prototype.toString.call(d) === '[object Date]' ? rptDay(d) :
      String(d).replace(/^(\d{4})(\d{2})(\d{2})$/, '$1-$2-$3');
    return o;
  });
  return rows.length ? rows : null;
}
function rptInWeek(o, win) { return o['date'] >= win.week && o['date'] < win.today; }
function rptInPrev(o, win) { return o['date'] >= win.prev && o['date'] < win.week; }

function rptContains(s, words) {
  s = String(s).toLowerCase();
  return words.some(function(w) { return s.indexOf(w) >= 0; });
}
function rptChannel(source, medium) {
  var organic = String(medium).toLowerCase() === RPT_CH_ORGANIC;
  if (organic && rptContains(source, RPT_CH_GOOGLE)) return 'Google search';
  if (organic) return 'Other search';
  if (rptContains(source, RPT_CH_LINKEDIN)) return 'LinkedIn';
  if (rptContains(source, RPT_CH_FACEBOOK)) return 'Facebook';
  if (rptContains(source, RPT_CH_TES)) return 'Tes';
  if (String(source).toLowerCase() === RPT_CH_DIRECT) return 'Direct';
  return 'Other';
}

// schools/assets/launch-dates.json ({slug: 'yyyy-MM-dd'}; a room's key has no "escape-"), fetched once per run as
// games.json is. ok is false when it could not be read; the Dashboard says so in one line and carries on.
function rptLoadLaunches() {
  if (rptLaunchCache) return rptLaunchCache;
  var dates = rptMap(), ok = false;
  try {
    var res = UrlFetchApp.fetch(RPT_LAUNCH_URL, {muteHttpExceptions: true});
    if (res.getResponseCode() === 200) {
      var j = JSON.parse(res.getContentText());
      Object.keys(j).forEach(function(k) { if (/^\d{4}-\d\d-\d\d$/.test(String(j[k]))) dates[k] = String(j[k]); });
      ok = true;
    }
  } catch (err) {
    console.error('launch-dates.json could not be read: ' + err);
  }
  rptLaunchCache = {ok: ok, dates: dates};
  return rptLaunchCache;
}

// A: one week's headline figures. Questions answered and % correct are question games only (rptKind).
function rptWeekFigures(rows, col, kinds) {
  var f = {starts: 0, answers: 0, marked: 0, right: 0}, games = rptMap();
  rows.forEach(function(x) {
    var ev = x[col['event']], slug = String(x[col['game_slug']]);
    if (ev === 'game_started') { f.starts++; games[slug] = true; return; }
    if (ev !== 'question_answered' || rptKind(slug, kinds) !== 'question') return;
    f.answers++;
    var m = rptMarked(x, col);
    if (m !== null) { f.marked++; if (m) f.right++; }
  });
  f.games = Object.keys(games).length;
  return f;
}

// A. IS IT GROWING?
function rptGrowing(dash, r, weekRows, prevWeekRows, col, kinds, ga4Daily, win) {
  r = rptTitle(dash, r, 'Is it growing? Last 7 days against the previous 7');
  var cur = rptWeekFigures(weekRows, col, kinds), prev = rptWeekFigures(prevWeekRows, col, kinds);
  var rate = cur.marked ? cur.right / cur.marked : null;
  var ch = [rptChange(cur.starts, prev.starts), rptChange(cur.answers, prev.answers),
    rptPointsChange(rate, prev.marked ? prev.right / prev.marked : null), rptChange(cur.games, prev.games)];
  var values = [cur.starts, cur.answers, rate === null ? 'n/a' : rate, cur.games];
  if (ga4Daily) {
    var e = 0, pe = 0;
    ga4Daily.forEach(function(o) {
      if (rptInWeek(o, win)) e += Number(o['engagedSessions']) || 0;
      else if (rptInPrev(o, win)) pe += Number(o['engagedSessions']) || 0;
    });
    values.push(e);
    ch.push(rptChange(e, pe));
  } else {
    values.push('–');
    ch.push({text: '–', dir: 0});
  }
  r = rptHead(dash, r, ['Games started', 'Questions answered', '% correct', 'Different games played', 'Engaged sessions']);
  rptRow(dash, r, values);
  if (rate !== null) dash.getRange(r, 3).setNumberFormat('0%');
  r++;
  rptRow(dash, r, ch.map(function(c) { return c.text; }));
  var colours = [rptDirColour(ch[0].dir), rptDirColour(ch[1].dir), RPT_GREY /* % correct: neutral whichever way it moves */,
    rptDirColour(ch[3].dir), rptDirColour(ch[4].dir)];
  colours.forEach(function(c, i) { dash.getRange(r, i + 1).setFontColor(c); });
  r++;
  if (!ga4Daily) r = rptLine(dash, r, RPT_GA4_MISSING);
  return r + 1;
}

// B. IS ANYTHING BROKEN?
function rptBroken(dash, r, weekRows, monthRows, col, kinds) {
  r = rptTitle(dash, r, 'Is anything broken?');
  // B1: a question almost nobody gets right may have a wrong answer key.
  r = rptTitle(dash, r, 'Check these questions — possible wrong answer key (last 30 days)');
  var chk = rptMap();
  monthRows.forEach(function(x) {
    if (x[col['event']] !== 'question_answered') return;
    var slug = String(x[col['game_slug']]);
    if (rptKind(slug, kinds) !== 'question') return;   // B1: question games only, never a room's lock
    var m = rptMarked(x, col), qid = col['question_id'] === undefined ? '' : String(x[col['question_id']]);
    if (m === null || !qid) return;
    var level = String(x[col['level']]), key = slug + '|' + level + '|' + qid;
    if (!rptHas(chk, key)) chk[key] = {slug: slug, level: level, qid: qid, total: 0, correct: 0};
    chk[key].total++;
    if (m) chk[key].correct++;
  });
  var flagged = Object.keys(chk).map(function(k) { return chk[k]; }).filter(function(q) {
    return q.total >= RPT_CHECK_MIN && q.correct / q.total < RPT_CHECK_PCT;
  }).sort(function(a, b) {
    return a.correct / a.total - b.correct / b.total || b.total - a.total ||
      (a.slug + '|' + a.level + '|' + a.qid < b.slug + '|' + b.level + '|' + b.qid ? -1 : 1);
  });
  if (!flagged.length) {
    r = rptLine(dash, r, 'None: every question answered ' + RPT_CHECK_MIN + '+ times has at least ' +
      Math.round(100 * RPT_CHECK_PCT) + '% right.');
  } else {
    r = rptHead(dash, r, ['Game', 'Level', 'Question id', 'Marked answers', '% right']);
    flagged.forEach(function(q) {
      rptRow(dash, r, [q.slug, q.level, q.qid, q.total, q.correct / q.total]).setBackground(RPT_FLAG_BG);
      dash.getRange(r, 5).setNumberFormat('0%');
      r++;
    });
    r = rptLine(dash, r, 'Decode an id: python scripts/decode-question-ids.py <game> --id <id>');
  }
  r++;

  // B2: where students quit.
  r = rptTitle(dash, r, 'Where students quit (last 7 days, games with ' + RPT_QUIT_MIN + '+ quits)');
  var quit = rptMap(), qStarts = rptMap();
  weekRows.forEach(function(x) {
    var ev = x[col['event']], slug = String(x[col['game_slug']]);
    if (ev === 'game_started') rptAdd(qStarts, slug);
    else if (ev === 'game_abandoned') {
      if (!rptHas(quit, slug)) quit[slug] = {slug: slug, n: 0, at: rptMap()};
      quit[slug].n++;
      rptAdd(quit[slug].at, String(x[col['question_index']]));
    }
  });
  var lower = function(a, b) { var x = Number(a), y = Number(b); return isNaN(x) || isNaN(y) ? a < b : x < y; };
  var quits = Object.keys(quit).map(function(k) { return quit[k]; }).filter(function(q) { return q.n >= RPT_QUIT_MIN; })
    .map(function(q) {
      q.starts = rptGet(qStarts, q.slug, 0);
      q.rate = q.starts > 0 ? q.n / q.starts : null;
      var best = null;
      Object.keys(q.at).forEach(function(k) {
        if (best === null || q.at[k] > q.at[best] || (q.at[k] === q.at[best] && lower(k, best))) best = k;
      });
      q.pos = /^\d+$/.test(best) ? Number(best) : best;
      q.posN = q.at[best];
      return q;
    }).sort(function(a, b) {
      return (b.rate === null ? -1 : b.rate) - (a.rate === null ? -1 : a.rate) || b.n - a.n || (a.slug < b.slug ? -1 : 1);
    }).slice(0, 10);
  if (!quits.length) {
    r = rptLine(dash, r, 'None: no game was quit ' + RPT_QUIT_MIN + ' or more times this week.');
  } else {
    r = rptHead(dash, r, ['Game', 'Starts', 'Abandoned', '% abandoned', 'Most quit at position', 'Quit there']);
    quits.forEach(function(q) {
      rptRow(dash, r, [q.slug, q.starts, q.n, q.rate === null ? '' : q.rate, q.pos, q.posN]);
      dash.getRange(r, 4).setNumberFormat('0%');
      r++;
    });
    r = rptLine(dash, r, 'Position in the run, not which question: game_abandoned carries question_index only.');
  }
  return r + 1;
}

// C. ARE TEACHERS USING IT?
function rptTeachers(dash, r, weekRows, monthRows, col, kinds) {
  r = rptTitle(dash, r, 'Are teachers using it?');
  // C1: a run of starts of one game, each close to the one before, is probably a class.
  r = rptTitle(dash, r, 'Probably a class (estimate: ' + RPT_CLASS_STARTS + ' or more starts of one game, each within ' +
    RPT_CLASS_GAP_MIN + ' minutes of the one before; last 7 days)');
  var gap = RPT_CLASS_GAP_MIN * 60000, starts = rptMap(), ans = rptMap();
  weekRows.forEach(function(x) {
    var ev = x[col['event']], slug = String(x[col['game_slug']]), t = new Date(x[col['timestamp']]).getTime();
    if (ev === 'game_started') {
      if (!rptHas(starts, slug)) starts[slug] = [];
      starts[slug].push(t);
    } else if (ev === 'question_answered' && rptKind(slug, kinds) === 'question') {
      if (!rptHas(ans, slug)) ans[slug] = [];
      ans[slug].push(t);
    }
  });
  var classes = [];
  Object.keys(starts).forEach(function(slug) {
    var ts = starts[slug].sort(function(a, b) { return a - b; }), run = [];
    var close = function() {
      if (run.length < RPT_CLASS_STARTS) return;
      var first = run[0], last = run[run.length - 1];
      var n = rptKind(slug, kinds) !== 'question' ? '–' :
        rptGet(ans, slug, []).filter(function(t) { return t >= first && t <= last + gap; }).length;
      classes.push({slug: slug, first: first, last: last, starts: run.length, answers: n});
    };
    ts.forEach(function(t, i) {
      if (i > 0 && t - ts[i - 1] > gap) { close(); run = []; }
      run.push(t);
    });
    close();
  });
  classes.sort(function(a, b) { return b.first - a.first || (a.slug < b.slug ? -1 : 1); });
  if (!classes.length) {
    r = rptLine(dash, r, 'None this week.');
  } else {
    r = rptHead(dash, r, ['Game', 'Date', 'First start', 'Last start', 'Starts', 'Questions answered']);
    classes.forEach(function(c) {
      rptRow(dash, r, [c.slug, rptDay(new Date(c.first)), Utilities.formatDate(new Date(c.first), TIMEZONE, 'HH:mm'),
        Utilities.formatDate(new Date(c.last), TIMEZONE, 'HH:mm'), c.starts, c.answers]);
      r++;
    });
  }
  r++;

  // C2: when in the week and the day games are started.
  r = rptTitle(dash, r, 'When it is used (game starts, last 30 days)');
  var slots = {wd: [0, 0, 0, 0, 0], we: [0, 0, 0, 0, 0]};
  monthRows.forEach(function(x) {
    if (x[col['event']] !== 'game_started') return;
    var d = new Date(x[col['timestamp']]), hm = Utilities.formatDate(d, TIMEZONE, 'HH:mm');
    var s = hm < '09:00' ? 0 : hm < '15:30' ? 1 : hm < '18:00' ? 2 : hm < '22:00' ? 3 : 4;
    slots[Number(Utilities.formatDate(d, TIMEZONE, 'u')) >= 6 ? 'we' : 'wd'][s]++;
  });
  r = rptHead(dash, r, ['Days', 'Before 09:00', '09:00-15:30', '15:30-18:00', '18:00-22:00', 'After 22:00']);
  rptRow(dash, r, ['Mon-Fri'].concat(slots.wd)); r++;
  rptRow(dash, r, ['Sat-Sun'].concat(slots.we)); r++;
  r = rptLine(dash, r, 'School day = 09:00-15:30, Mon-Fri. Term dates not applied.');
  r++;

  // C3: what people filter the portal by.
  r = rptTitle(dash, r, 'What people look for on the portal (filters, last 7 days)');
  var looks = rptMap();
  weekRows.forEach(function(x) {
    if (x[col['event']] !== 'filter_applied') return;
    var type = String(x[col['filter_type']]), value = String(x[col['filter_value']]), key = type + '\u0001' + value;
    if (!rptHas(looks, key)) looks[key] = {type: type, value: value, n: 0};
    looks[key].n++;
  });
  var lookList = Object.keys(looks).map(function(k) { return looks[k]; }).sort(function(a, b) {
    return b.n - a.n || (a.type + '\u0001' + a.value < b.type + '\u0001' + b.value ? -1 : 1);
  }).slice(0, 10);
  if (!lookList.length) {
    r = rptLine(dash, r, 'None this week.');
  } else {
    r = rptHead(dash, r, ['Filter', 'Value', 'Times']);
    lookList.forEach(function(l) { rptRow(dash, r, [l.type, l.value, l.n]); r++; });
  }
  return r + 1;
}

// D. DID MY POSTS BRING VISITORS? (GA4 sources daily)
function rptVisitors(dash, r, src, win) {
  r = rptTitle(dash, r, 'Did my posts bring visitors? (GA4, last 7 complete days against the previous 7)');
  if (!src) { r = rptLine(dash, r, RPT_GA4_MISSING); return r + 1; }
  r = rptTitle(dash, r, 'Visitors by channel');
  var ch = rptMap(), pages = rptMap();
  RPT_CHANNELS.forEach(function(n) { ch[n] = {s: 0, e: 0, pe: 0}; });
  src.forEach(function(o) {
    var c = ch[rptChannel(o['sessionSource'], o['sessionMedium'])];
    var s = Number(o['sessions']) || 0, e = Number(o['engagedSessions']) || 0;
    if (rptInWeek(o, win)) {
      c.s += s; c.e += e;
      var p = String(o['landingPage']);
      if (!rptHas(pages, p)) pages[p] = {page: p, s: 0, e: 0};
      pages[p].s += s; pages[p].e += e;
    } else if (rptInPrev(o, win)) {
      c.pe += e;
    }
  });
  r = rptHead(dash, r, ['Channel', 'Sessions', 'Engaged sessions', '% engaged', 'Change in engaged sessions']);
  RPT_CHANNELS.forEach(function(n) {
    var c = ch[n], chg = rptChange(c.e, c.pe);
    rptRow(dash, r, [n, c.s, c.e, c.s > 0 ? c.e / c.s : '', chg.text]);
    dash.getRange(r, 4).setNumberFormat('0%');
    dash.getRange(r, 5).setFontColor(rptDirColour(chg.dir));
    r++;
  });
  r++;
  r = rptTitle(dash, r, 'Top landing pages (by engaged sessions)');
  var top = Object.keys(pages).map(function(k) { return pages[k]; }).sort(function(a, b) {
    return b.e - a.e || b.s - a.s || (a.page < b.page ? -1 : 1);
  }).slice(0, 10);
  if (!top.length) {
    r = rptLine(dash, r, 'No visits in these 7 days.');
  } else {
    r = rptHead(dash, r, ['Landing page', 'Engaged sessions', 'Sessions']);
    top.forEach(function(p) { rptRow(dash, r, [p.page, p.e, p.s]); r++; });
  }
  return r + 1;
}

// E. WHO USES IT? (GA4 engaged sessions; no location finer than country)
function rptWho(dash, r, daily, src, win) {
  r = rptTitle(dash, r, 'Who uses it? (GA4 engaged sessions, last 7 complete days)');
  if (!daily || !src) r = rptLine(dash, r, RPT_GA4_MISSING);
  if (!daily && !src) return r + 1;
  if (daily) {
    var by = rptMap(), total = 0;
    daily.forEach(function(o) {
      if (!rptInWeek(o, win)) return;
      var e = Number(o['engagedSessions']) || 0, c = String(o['country']);
      total += e;
      by[c] = rptGet(by, c, 0) + e;
    });
    var uk = rptGet(by, 'United Kingdom', 0);
    rptRow(dash, r, ['UK share of engaged sessions', total > 0 ? uk / total : 'n/a', uk + ' of ' + total]);
    dash.getRange(r, 2).setNumberFormat('0%');
    r += 2;
    r = rptTitle(dash, r, 'Top 5 countries');
    var countries = Object.keys(by).sort(function(a, b) { return by[b] - by[a] || (a < b ? -1 : 1); }).slice(0, 5);
    r = rptHead(dash, r, ['Country', 'Engaged sessions', 'Share']);
    countries.forEach(function(c) {
      rptRow(dash, r, [c, by[c], total > 0 ? by[c] / total : '']);
      dash.getRange(r, 3).setNumberFormat('0%');
      r++;
    });
    r++;
  }
  if (src) {
    r = rptTitle(dash, r, 'Devices');
    var dev = {mobile: 0, desktop: 0, tablet: 0}, all = 0;
    src.forEach(function(o) {
      if (!rptInWeek(o, win)) return;
      var e = Number(o['engagedSessions']) || 0, d = String(o['deviceCategory']).toLowerCase();
      all += e;
      if (Object.prototype.hasOwnProperty.call(dev, d)) dev[d] += e;
    });
    r = rptHead(dash, r, ['Device', 'Engaged sessions', 'Share']);
    ['mobile', 'desktop', 'tablet'].forEach(function(d) {
      rptRow(dash, r, [d, dev[d], all > 0 ? dev[d] / all : '']);
      dash.getRange(r, 3).setNumberFormat('0%');
      r++;
    });
    r++;
  }
  return r;
}

// F. IS MY NEWEST GAME LANDING? Everything since its launch date (all within monthRows: launches are 14 days back).
function rptNewGames(dash, r, monthRows, col, kinds, win) {
  r = rptTitle(dash, r, 'Is my newest game landing?');
  r = rptTitle(dash, r, 'New games (launched in the last ' + RPT_NEW_GAME_DAYS + ' days), since launch');
  var L = rptLoadLaunches();
  if (!L.ok) { r = rptLine(dash, r, 'Launch dates could not be read today.'); return r + 1; }
  var fresh = Object.keys(L.dates).filter(function(k) { return L.dates[k] >= win.launch && L.dates[k] <= win.today; })
    .sort(function(a, b) { return L.dates[a] < L.dates[b] ? 1 : L.dates[a] > L.dates[b] ? -1 : (a < b ? -1 : 1); });
  if (!fresh.length) { r = rptLine(dash, r, 'None launched in the last ' + RPT_NEW_GAME_DAYS + ' days.'); return r + 1; }
  var stats = rptMap();
  fresh.forEach(function(k) { stats[k] = {starts: 0, answers: 0, marked: 0, right: 0, done: 0, escaped: 0, room: false}; });
  monthRows.forEach(function(x) {
    var slug = String(x[col['game_slug']]), key = slug.indexOf('escape-') === 0 ? slug.slice(7) : slug;
    if (!rptHas(stats, key) || rptDay(new Date(x[col['timestamp']])) < L.dates[key]) return;
    var st = stats[key], kind = rptKind(slug, kinds), ev = x[col['event']];
    if (kind === 'room') st.room = true;
    if (ev === 'game_started') st.starts++;
    else if (ev === 'game_completed') { st.done++; if (kind === 'room' && rptEscaped(x, col)) st.escaped++; }
    else if (ev === 'question_answered' && kind === 'question') {
      st.answers++;
      var m = rptMarked(x, col);
      if (m !== null) { st.marked++; if (m) st.right++; }
    }
  });
  r = rptHead(dash, r, ['Game', 'Launched', 'Starts', 'Questions answered', '% correct', 'Completed']);
  fresh.forEach(function(k) {
    var st = stats[k], kind = st.room ? 'room' : rptKind(k, kinds);
    var pct = kind === 'room' ? st.escaped + ' escaped (' + rptPct(st.escaped, st.starts) + ')' :
      kind === 'shot' ? '–' : st.marked ? st.right / st.marked : 'n/a';
    rptRow(dash, r, [k, L.dates[k], st.starts, kind === 'question' ? st.answers : '–', pct, st.done]);
    if (typeof pct === 'number') dash.getRange(r, 5).setNumberFormat('0%');
    r++;
  });
  return r + 1;
}

// G (after Table 4b). Hints by lock, and time per lock from game_completed's "locks:" list. engine.js finish()
// writes st.openAt for each lock in room.js order: st.played (seconds the room's clock had run) when it opened, "-"
// if it never did. Opened locks sorted by that time give the seconds spent since the previous one opened.
function rptRoomExtras(dash, r, monthRows, col, kinds) {
  r = rptTitle(dash, r, 'Hints by lock (last 30 days, most first)');
  var hints = rptMap();
  monthRows.forEach(function(x) {
    var slug = String(x[col['game_slug']]);
    if (x[col['event']] !== 'hint_used' || rptKind(slug, kinds) !== 'room') return;
    var lock = String(x[col['detail']]).split(':')[0], key = slug + '\u0001' + lock;
    if (!rptHas(hints, key)) hints[key] = {room: slug, lock: lock, n: 0};
    hints[key].n++;
  });
  var hintList = Object.keys(hints).map(function(k) { return hints[k]; }).sort(function(a, b) {
    return b.n - a.n || (a.room + '\u0001' + a.lock < b.room + '\u0001' + b.lock ? -1 : 1);
  });
  if (!hintList.length) {
    r = rptLine(dash, r, 'No hints used.');
  } else {
    r = rptHead(dash, r, ['Room', 'Lock', 'Hints']);
    hintList.forEach(function(h) { rptRow(dash, r, [h.room, h.lock, h.n]); r++; });
  }
  r++;

  r = rptTitle(dash, r, 'Time per lock (last 30 days; lock N is the room\'s Nth lock in room.js; time since the previous lock opened, or the start)');
  var times = rptMap();
  monthRows.forEach(function(x) {
    var slug = String(x[col['game_slug']]);
    if (x[col['event']] !== 'game_completed' || rptKind(slug, kinds) !== 'room') return;
    var m = /(?:^|\s)locks:(\S+)/.exec(String(x[col['detail']]));
    if (!m) return;
    var opened = m[1].split(',').map(function(v, i) { return {pos: i + 1, t: /^\d+$/.test(v) ? Number(v) : null}; })
      .filter(function(o) { return o.t !== null; }).sort(function(a, b) { return a.t - b.t || a.pos - b.pos; });
    var prev = 0;
    opened.forEach(function(o) {
      var key = slug + '\u0001' + o.pos;
      if (!rptHas(times, key)) times[key] = {room: slug, pos: o.pos, runs: 0, sum: 0};
      times[key].runs++;
      times[key].sum += o.t - prev;
      prev = o.t;
    });
  });
  var timeList = Object.keys(times).map(function(k) { return times[k]; }).sort(function(a, b) {
    return a.room < b.room ? -1 : a.room > b.room ? 1 : a.pos - b.pos;
  });
  if (!timeList.length) {
    r = rptLine(dash, r, 'No room finished in these 30 days.');
  } else {
    r = rptHead(dash, r, ['Room', 'Lock', 'Runs that opened it', 'Average time']);
    timeList.forEach(function(t) {
      var s = Math.round(t.sum / t.runs);
      rptRow(dash, r, [t.room, 'lock ' + t.pos, t.runs, Math.floor(s / 60) + ' min ' + (s % 60) + ' s']);
      r++;
    });
  }
  return r + 1;
}

// H. MISUNDERSTOOD MATHS (the homepage's weekly fact)
function rptFacts(dash, r, weekRows, col) {
  r = rptTitle(dash, r, 'Misunderstood Maths (last 7 days)');
  var n = {fact_viewed: 0, fact_expanded: 0, fact_game_clicked: 0, fact_shared: 0};
  weekRows.forEach(function(x) {
    var ev = String(x[col['event']]);
    if (Object.prototype.hasOwnProperty.call(n, ev)) n[ev]++;
  });
  r = rptHead(dash, r, ['Facts viewed', 'Expanded', 'Game links clicked', 'Shared', 'Game clicks % of views']);
  rptRow(dash, r, [n.fact_viewed, n.fact_expanded, n.fact_game_clicked, n.fact_shared,
    n.fact_viewed > 0 ? n.fact_game_clicked / n.fact_viewed : 'n/a']);
  dash.getRange(r, 5).setNumberFormat('0%');
  return r + 2;
}

// ============================================================
//  DASHBOARD — auto-rebuilds with charts
// ============================================================
function rebuildDashboard(weekRows, monthRows, col, kinds, prevWeekRows) {
  var ss = SpreadsheetApp.open(DriveApp.getFilesByName(SHEET_NAME).next());
  var dash = ss.getSheetByName(DASH_NAME);
  if (dash) {
    dash.clear();
    // Sheet.clear() leaves number formats in place (proven in real Sheets, 19 Nov 2026), so a stale "0%" would show the next count written to that cell as a percentage.
    dash.getRange(1, 1, dash.getMaxRows(), dash.getMaxColumns()).setNumberFormat('General');
    // Remove existing charts
    dash.getCharts().forEach(function(c) { dash.removeChart(c); });
  } else {
    dash = ss.insertSheet(DASH_NAME);
  }

  var r = 1; // current row pointer
  kinds = kinds || rptLoadKinds();
  prevWeekRows = prevWeekRows || [];

  // ── TITLE ──
  dash.getRange(r, 1).setValue('MaffsGames Dashboard').setFontSize(16).setFontWeight('bold');
  dash.getRange(r, 3).setValue('Last updated: ' + Utilities.formatDate(new Date(), TIMEZONE, 'dd MMM yyyy HH:mm'));
  r += 2;
  var rep = rptBuild(weekRows, col, kinds || rptLoadKinds());
  [rptKindsLine(rep), rptShotsLine(rep)].forEach(function(line) {
    if (line) { dash.getRange(r, 1).setValue(line).setFontStyle('italic'); r++; }
  });
  if (rptKindsLine(rep) || rptShotsLine(rep)) r++;

  var win = rptWindows();
  var ga4Daily = rptGa4Tab(ss, RPT_GA4_DAILY), ga4Sources = rptGa4Tab(ss, RPT_GA4_SOURCES);
  r = rptGrowing(dash, r, weekRows, prevWeekRows, col, kinds, ga4Daily, win);   // A
  r = rptBroken(dash, r, weekRows, monthRows, col, kinds);                      // B
  r = rptTeachers(dash, r, weekRows, monthRows, col, kinds);                    // C
  r = rptVisitors(dash, r, ga4Sources, win);                                    // D
  r = rptWho(dash, r, ga4Daily, ga4Sources, win);                               // E
  r = rptNewGames(dash, r, monthRows, col, kinds, win);                         // F

  // G: escape rooms (Table 4b), then hints and time by lock
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

  r = rptRoomExtras(dash, r, monthRows, col, kinds);

  // H: Misunderstood Maths
  r = rptFacts(dash, r, weekRows, col);

  // I: the earlier tables, unchanged: Top games, Accuracy by game, Hardest questions, Levels
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
    dashChart(dash, {type: Charts.ChartType.BAR, ranges: [dash.getRange(t1Start+1, 1, topSlugs.length+1, 2)],
      row: t1Start, col: 6, options: {title: 'Top Games — Last 7 Days', legend: {position: 'none'}, width: 500, height: 300,
      colors: ['#0ea5e9']}});
    r = rowBelowChart(r, t1Start, 300);
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

    dashChart(dash, {type: Charts.ChartType.BAR,
      ranges: [dash.getRange(t3Start+1, 1, rep.games.length+1, 1), dash.getRange(t3Start+1, 4, rep.games.length+1, 1)],
      row: t3Start, col: 6, options: {title: 'Accuracy by Game (sorted lowest first)', legend: {position: 'none'},
      width: 500, height: 300, colors: ['#f97316'], hAxis: {minValue: 0, maxValue: 1, format: 'percent'}}});
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
    dashChart(dash, {type: Charts.ChartType.PIE, ranges: [dash.getRange(t2Start+1, 1, levels.length+1, 2)],
      row: t2Start, col: 6, options: {title: 'Level Split — Last 7 Days', width: 400, height: 280,
      colors: ['#22c55e','#3b82f6','#f97316','#8b5cf6','#ef4444','#0ea5e9']}});
    r = rowBelowChart(r, t2Start, 280);
  }

  // J: Daily Activity, last
  // ══════════════════════════════════════
  //  TABLE 5: Daily Activity (30 days)
  // ══════════════════════════════════════
  // Games started (every game) and questions answered (question games only, marked or not: a count of answers, not
  // accuracy; rooms and shot games left out by rptKind, as in rptBuild). Contract DAILY-ANSWERS, Jon 17 Nov 2026.
  var dayKinds = kinds || rptLoadKinds();
  var dailyStarts = rptMap(), dailyAnswers = rptMap();
  monthRows.forEach(function(x) {
    var ev = x[col['event']];
    if (ev !== 'game_started' && ev !== 'question_answered') return;
    var day = Utilities.formatDate(new Date(x[col['timestamp']]), TIMEZONE, 'yyyy-MM-dd');
    if (ev === 'game_started') rptAdd(dailyStarts, day);
    else if (rptKind(String(x[col['game_slug']]), dayKinds) === 'question') rptAdd(dailyAnswers, day);
  });
  var days = Object.keys(dailyStarts).concat(Object.keys(dailyAnswers).filter(function(d) {
    return !rptHas(dailyStarts, d);
  })).sort();

  var t5Start = r;
  dash.getRange(r, 1).setValue('Daily Activity — Last 30 Days').setFontWeight('bold').setFontSize(11);
  r++;
  dash.getRange(r, 1, 1, 3).setValues([['Date', 'Games Started', 'Questions Answered']]).setFontWeight('bold').setBackground('#f0f0f0');
  r++;
  days.forEach(function(d) {
    dash.getRange(r, 1, 1, 3).setValues([[d, rptGet(dailyStarts, d, 0), rptGet(dailyAnswers, d, 0)].map(cellValue)]);
    r++;
  });

  // Chart 5: Daily activity line chart, games started on the left axis, questions answered on the right. The
  // series are named from the header row (dashChart), and the lines are straight: a smoothed curve
  // overshot the real points and dipped below zero near a trough (DASHBOARD-GLANCE).
  if (days.length > 1) {
    dashChart(dash, {type: Charts.ChartType.LINE, ranges: [dash.getRange(t5Start+1, 1, days.length+1, 3)],
      row: t5Start, col: 6, options: {title: 'Daily Games Started and Questions Answered — Last 30 Days',
      legend: {position: 'bottom'}, width: 500, height: 280, colors: ['#0ea5e9', '#0d9488'],
      series: {0: {targetAxisIndex: 0}, 1: {targetAxisIndex: 1}},
      vAxes: {0: {title: 'Games started'}, 1: {title: 'Questions answered'}}}});
    r = rowBelowChart(r, t5Start, 280);
  }

  // ── Formatting ──
  dash.setColumnWidth(1, 220);
  dash.setColumnWidth(2, 80);
  dash.setColumnWidth(3, 80);
  dash.setColumnWidth(4, 100);
  dash.setTabColor('#0ea5e9');
}

// Every Dashboard chart is built here (DASHBOARD-FIXES, 18 Nov 2026), so every one takes its series and category
// names from its first row: each range starts at its table's header row, and without setNumHeaders(1) Sheets may
// draw that row as data (a "Game" bar). spec: type (Charts.ChartType), ranges (Ranges, header row first), row and
// col (the chart's top-left cell), options (setOption's names and values).
function dashChart(dash, spec) {
  var b = dash.newChart().setChartType(spec.type);
  spec.ranges.forEach(function(rg) { b = b.addRange(rg); });
  b = b.setNumHeaders(1);
  b = b.setPosition(spec.row, spec.col, 0, 0);
  Object.keys(spec.options).forEach(function(k) { b = b.setOption(k, spec.options[k]); });
  dash.insertChart(b.build());
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
  var prevWeekAgo = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 14);
  var prevWeekRows = allRows.filter(function(r) { var t = new Date(r[col['timestamp']]); return t >= prevWeekAgo && t < weekAgo; });
  rebuildDashboard(weekRows, monthRows, col, rptLoadKinds(), prevWeekRows);
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
