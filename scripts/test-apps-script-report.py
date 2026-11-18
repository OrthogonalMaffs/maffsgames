#!/usr/bin/env python3
# ci-line: Analytics report (docs/apps-script-endpoint.js: each kind of game by its own measure, hardest questions by question_id, rooms by escapes, shot games left out, games.json fallback, pre-29-Sep blanks, doPost's column order with detail last; planted faults caught) |
# ci-deps: docs/apps-script-endpoint.js data/games.json
"""Does the daily email and Dashboard (docs/apps-script-endpoint.js) report each kind of game by a measure that means
something for it? Contract DASHBOARD-METRICS (Jon, 3 Nov 2026; Amendment 2: games.json is read from GitHub).

The script cannot run in CI (it needs Google's services), so, as scripts/test-apps-script-counts.py does, this loads the
file's own source into Chromium behind small fakes of what it calls (UrlFetchApp, SpreadsheetApp, DriveApp, MailApp,
Utilities, Charts) with a fixed clock, and drives the real functions on fixture rows:

  - a question game well over the minimum, one at exactly 30 and one at 29, one with no question_id (an older game),
    an escape room escaped and one never escaped, a shot game (Trig Wars), Prisoner's Dilemma's unmarked blanks, and a
    game whose rows are from before 29 Sep 2026 20:00 UTC with blank wrong answers;
  - a. accuracy by game: question games only, at least 30 marked answers, lowest first; overall accuracy from
    question games only;
  - b. hardest questions: question games only, keyed game + level + question_id, at least 10 attempts, no row without
    a question_id, and the heading counts the games that send one;
  - c. rooms: started, escaped, escape rate, attempts per lock opened (marked / correct), lowest escape rate first;
    a room's game_completed is an escape only when every lock opened (questions_correct = questions_answered > 0):
    a win (3/3), a timeout (1/3) and a timeout with no lock open (0/3) are 1 escaped, 2 timed out (ROOM-ESCAPED);
  - d. shot games: one line naming them, never in accuracy;
  - e. a blank `correct` before 2026-09-29T20:00Z counts as wrong; after it, it is not marked;
  - games.json is fetched once per run; a failed fetch counts every game as a question game and says so in one line
    of the email and of the Dashboard; the real data/games.json uses only "question" and "shot";
  - end to end: sendDailyReport sends one email and builds the Dashboard from the same model (--sample prints both).
Then planted faults, each a small change to the script that must make a check fail: a room counted in accuracy, a row
with no question_id in hardest questions, a minimum below 30, a pre-29-Sep blank ignored instead of counted wrong, every
room game_completed counted as escaped, doPost leaving detail out of the row, doPost writing detail before question_id.
  - f. doPost (ROOM-TIMES): EXPECTED_HEADERS is the 18 earlier columns in order then detail; each posted field lands
    under its own header, detail last; an old 18-header row 1 gains "detail" in S1; no detail leaves it blank.
  - g. safe tallies (COUNTS-SAFE-TALLY, 14 Nov 2026): four games whose game_slug and level are "constructor",
    "__proto__", "toString" and "hasOwnProperty" are reported like any other game, in the model, the email and the
    Dashboard (figures written by hand), every other line is unchanged, and no tally lands on a built-in object.
    Its planted fault: the tally maps given a prototype again.
  - h. posted values are data, never formulas (SHEET-FORMULA-CELLS, 14 Nov 2026): doPost hands the Sheet a leading
    apostrophe before any string beginning =, +, @, a tab, a carriage return, or "-" that is not a plain number
    (detail "=1+1", game_slug =IMAGE("x"), level "+1", question_id "@a", detail "-x"); -3, "-3", "2026-11-14",
    "true", false, 0 and a whole ordinary event are written exactly as sent; the Dashboard, which writes slugs,
    levels and question ids read back from the Sheet, does the same and writes no cell that could be a formula.
    What Sheets does with the apostrophe is modelled here (it is not part of the value read back), not run.
    Two planted faults: cellValue passing the string through, and a Dashboard row written without it.
  - i. daily activity (DAILY-ANSWERS, Jon 17 Nov 2026): the Dashboard's last table is Date | Games Started | Questions
    Answered, one row for every day with either count (a missing count is 0). Questions answered counts question games
    only (rptKind 'question'), marked or not; rooms and shot games are left out. Its chart is one LINE chart over the 3
    columns, starts on the left axis and answers on the right, with a legend. Figures written by hand. Three planted
    faults: room answers counted, shot answers counted, a day with no starts dropped.
  - j. the Dashboard at a glance (DASHBOARD-GLANCE, Jon 18 Nov 2026), sections A to H on hand-written Sheet rows and
    hand-written GA4 tab rows, through sendDailyReport (so its weekRows, monthRows and prevWeekRows): A the week
    against the previous 7 ("new" from 0, % correct in points and always grey); B1 questions under 10% right on 10+
    marked answers (9% of 11 in, 10% of 10 and 0 of 9 out, a room's lock never); B2 where students quit (9 quits
    out); C1 a probable class (10 starts 29 minutes apart in, a 31-minute gap splits, 9 out); C2 when it is used
    (15:29 Tuesday school day, 15:30 not, Saturday 10:00 Sat-Sun); C3 portal filters; D GA4 channels (lnkd.in,
    m.facebook.com, google / organic, bing / organic, (direct)) and landing pages; E the UK share, top countries and
    devices; a missing GA4 tab giving one line in A, D and E, never an error; F new games (13 and 14 days in, 15
    out, a failed launch-dates fetch giving its line); G hints and time by lock; H Misunderstood Maths; the order of
    every section, Daily Activity last; the chart's series named from its header row, with straight lines.
    Plants: the 10% threshold made <=, the class gap made 60 minutes, % correct coloured green or red, lnkd.in falling
    into Other, a missing GA4 tab throwing, a room counted in check-these, curveType back.

    python scripts/test-apps-script-report.py [--sample]
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import plant_common as pc  # noqa: E402

BASE = HERE.parent
SRC = BASE / "docs" / "apps-script-endpoint.js"
GAMES = BASE / "data" / "games.json"

HARNESS = r"""
([src, fixtureGames]) => {
  const out = [];
  const ok = (name, cond, detail) => out.push([name, !!cond, cond ? '' : String(detail === undefined ? '' : detail)]);
  const NOW = Date.parse('2026-11-04T07:00:00Z');
  const RealDate = Date;
  class FakeDate extends RealDate { constructor(...a) { if (a.length === 0) super(NOW); else super(...a); } static now() { return NOW; } }

  const HEAD = ['timestamp', 'event', 'game_slug', 'level', 'mode', 'question_index', 'correct', 'attempts', 'score',
    'questions_answered', 'questions_correct', 'previous_score', 'difficulty', 'filter_type', 'filter_value',
    'client_ts', 'seq', 'question_id', 'detail'];
  const col = {}; HEAD.forEach((h, i) => col[h] = i);
  const row = (ts, event, slug, level, correct, qid) => {
    const r = HEAD.map(() => ''); r[0] = ts; r[1] = event; r[2] = slug; r[3] = level;
    r[6] = correct === undefined ? '' : correct; r[17] = qid || ''; return r;
  };
  const completed = (slug, answered, correct) => { const r = row(Y, 'game_completed', slug, 'all'); r[9] = answered; r[10] = correct; return r; };
  const Y = '2026-11-03T10:00:00.000Z', OLD = '2026-09-28T10:00:00.000Z';
  const rows = [];
  const answers = (slug, n, right, qid, ts, level) => { for (let i = 0; i < n; i++) rows.push(row(ts || Y, 'question_answered', slug, level || 'gcse', i < right, typeof qid === 'function' ? qid(i) : qid)); };
  // question games
  answers('alpha-q', 12, 3, 'h00000001');                 // the hardest question: 25% over 12 attempts
  answers('alpha-q', 20, 18, 'h00000002');                // 90% over 20
  answers('alpha-q', 9, 0, 'h00000003');                  // 0% but only 9 attempts: below the minimum
  answers('beta-q', 35, 14);                              // no question_id (not migrated yet): 40%
  answers('thirty-q', 30, 21);                            // exactly 30: in
  answers('twentynine-q', 29, 1);                         // 29: out, however low
  rows.push(row(Y, 'question_answered', 'prisoners-dilemma', 'all', '', ''));   // no right answer: not marked
  rows.push(row(Y, 'question_answered', 'prisoners-dilemma', 'all', '', ''));
  // a shot game: hits, not answers
  answers('trig-wars', 40, 4);
  // escape rooms
  ['game_started', 'game_started', 'game_started', 'game_started'].forEach(e => rows.push(row(Y, e, 'escape-alpha', 'all')));
  rows.push(completed('escape-alpha', 3, 3));             // escaped: every lock open
  rows.push(completed('escape-alpha', 3, 1));             // the clock ran out with one lock open
  rows.push(completed('escape-alpha', 3, 0));             // the clock ran out with none open
  answers('escape-alpha', 36, 9, 'h0000000a', Y, 'all');  // 36 tries, 9 locks opened: 4.0 a lock
  ['game_started', 'game_started'].forEach(e => rows.push(row(Y, e, 'escape-beta', 'all')));
  answers('escape-beta', 5, 1, '', Y, 'all');
  // before the falsy fix: 30 blank (wrong) and 10 right, all before 29 Sep 20:00 UTC
  answers('delta-q', 10, 10, '', OLD);
  for (let i = 0; i < 30; i++) rows.push(row(OLD, 'question_answered', 'delta-q', 'gcse', '', ''));
  rows.push(row('2026-09-29T19:59:00.000Z', 'question_answered', 'delta-q', 'gcse', '', ''));    // a minute before: wrong
  rows.push(row('2026-09-29T20:01:00.000Z', 'question_answered', 'delta-q', 'gcse', '', ''));    // after: not marked

  function load(fetchMode, eventsHead, dataRows, opts) {
    opts = opts || {};
    const env = { fetches: 0, mails: [], cells: {}, sheets: {}, charts: [] };
    const UrlFetchApp = { fetch(url) {
      env.fetches++; env.url = url;
      if (fetchMode === 'throw') throw new Error('DNS error');
      if (fetchMode === '404') return { getResponseCode: () => 404, getContentText: () => 'Not Found' };
      if (/launch-dates\.json$/.test(url)) return opts.launch === 'fail' ? { getResponseCode: () => 404, getContentText: () => 'Not Found' }
        : { getResponseCode: () => 200, getContentText: () => JSON.stringify(opts.launch || {}) };
      return { getResponseCode: () => 200, getContentText: () => JSON.stringify(fixtureGames) };
    } };
    const chain = new Proxy({}, { get: (t, k) => k === 'build' ? () => ({}) : (...a) => { env.charts[env.charts.length - 1].push([k, a]); return chain; } });
    function sheetFake(name, data) {
      const sh = { name, cells: {}, fmt: {},
        clear() { sh.cells = {}; sh.fmt = {}; }, getCharts: () => [], removeChart() {}, insertChart() {}, setColumnWidth() {},
        setTabColor() {}, setFrozenRows() {}, newChart: () => { env.charts.push([]); return chain; },
        getDataRange: () => ({ getValues: () => data }),
        getLastRow: () => data.length,
        appendRow(r) { data.push(r); },
        getRange(r, c, nr, nc) {
          const rg = { dims: [r, c, nr || 1, nc || 1], setValue(v) { sh.cells[r + ',' + c] = v; return rg; },
            setValues(vs) { vs.forEach((line, i) => line.forEach((v, j) => sh.cells[(r + i) + ',' + (c + j)] = v)); return rg; },
            getValues: () => [data[r - 1].slice(c - 1, c - 1 + (nc || 1))] };
          ['setFontSize', 'setFontWeight', 'setFontStyle', 'setNumberFormat'].forEach(m => rg[m] = () => rg);
          ['setBackground', 'setFontColor'].forEach(m => rg[m] = v => {
            for (let i = 0; i < (nr || 1); i++) for (let j = 0; j < (nc || 1); j++) {
              const k = (r + i) + ',' + (c + j); sh.fmt[k] = Object.assign(sh.fmt[k] || {}, { [m]: v }); }
            return rg; });
          return rg;
        } };
      return sh;
    }
    const events = sheetFake('events', [eventsHead || HEAD].concat(eventsHead ? [] : (dataRows || rows)));
    Object.keys(opts.ga4 || {}).forEach(n => { env.sheets[n] = sheetFake(n, opts.ga4[n]); });
    env.events = events;
    const ss = { getActiveSheet: () => events, getSheetByName: n => env.sheets[n] || null,
      insertSheet: n => (env.sheets[n] = sheetFake(n, [])) };
    const DriveApp = { getFilesByName: () => ({ hasNext: () => true, next: () => ({}) }) };
    const SpreadsheetApp = { open: () => ss, create: () => ss };
    const MailApp = { sendEmail: (to, subject, body) => env.mails.push({ to, subject, body }) };
    // formatDate in the zone it is given, as Apps Script's does (a day key at midnight in BST is that day, not the
    // UTC day before). 'u' is the day of the week, Monday 1.
    const zoned = (d, tz, o) => new Intl.DateTimeFormat('en-GB', Object.assign({ timeZone: tz }, o)).formatToParts(d)
      .reduce((a, p) => (a[p.type] = p.value, a), {});
    const Utilities = { formatDate: (d, tz, f) => {
      if (f === 'yyyy-MM-dd') { const z = zoned(d, tz, { year: 'numeric', month: '2-digit', day: '2-digit' }); return z.year + '-' + z.month + '-' + z.day; }
      if (f === 'HH:mm') { const z = zoned(d, tz, { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }); return z.hour + ':' + z.minute; }
      if (f === 'u') return String(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(zoned(d, tz, { weekday: 'short' }).weekday) + 1);
      return d.toISOString().slice(0, 16);
    } };
    const Charts = { ChartType: { BAR: 'BAR', PIE: 'PIE', LINE: 'LINE' } };
    const ContentService = { MimeType: { JSON: 'JSON' }, createTextOutput: t => ({ setMimeType: () => JSON.parse(t) }) };
    const api = new Function('UrlFetchApp', 'DriveApp', 'SpreadsheetApp', 'MailApp', 'Utilities', 'Charts', 'Date', 'ContentService', 'ScriptApp',
      src + '\n;return {rptBuild, rptLoadKinds, rptMarked, rptKind, rptEmailText, sendDailyReport, rebuildDashboard,' +
      ' RPT_MIN_GAME_ANSWERS, RPT_MIN_QUESTION_ATTEMPTS, GAMES_JSON_URL, doPost, EXPECTED_HEADERS};')(
      UrlFetchApp, DriveApp, SpreadsheetApp, MailApp, Utilities, Charts, FakeDate, ContentService, {});
    return { api, env };
  }
  const dashText = sh => {
    const keys = Object.keys(sh.cells).map(k => k.split(',').map(Number));
    const maxR = Math.max(0, ...keys.map(k => k[0]));
    const lines = [];
    for (let r = 1; r <= maxR; r++) {
      const cells = keys.filter(k => k[0] === r).sort((a, b) => a[1] - b[1]).map(k => {
        const v = sh.cells[k[0] + ',' + k[1]]; return typeof v === 'number' && v > 0 && v < 1 ? Math.round(v * 100) + '%' : String(v); });
      lines.push(cells.join(' | '));
    }
    return lines.join('\n');
  };

  try {
    // ---- the model, games.json read
    let { api, env } = load('ok');
    const kinds = api.rptLoadKinds(); api.rptLoadKinds();
    ok('games.json is fetched once per run, from GitHub (Amendment 2)', env.fetches === 1 && env.url === 'https://raw.githubusercontent.com/OrthogonalMaffs/maffsgames/main/data/games.json', env.fetches + ' fetches of ' + env.url);
    ok('minimums are 30 answers and 10 attempts', api.RPT_MIN_GAME_ANSWERS === 30 && api.RPT_MIN_QUESTION_ATTEMPTS === 10, api.RPT_MIN_GAME_ANSWERS + ', ' + api.RPT_MIN_QUESTION_ATTEMPTS);
    ok('kinds: escape- is a room, answer_kind shot is a shot, anything else a question',
      api.rptKind('escape-alpha', kinds) === 'room' && api.rptKind('trig-wars', kinds) === 'shot' && api.rptKind('alpha-q', kinds) === 'question' && api.rptKind('unknown-game', kinds) === 'question');
    const rep = api.rptBuild(rows, col, kinds);
    const slugs = rep.games.map(g => g.slug);
    ok('a. accuracy: question games at 30 or more marked answers, lowest first',
      JSON.stringify(slugs) === JSON.stringify(['delta-q', 'beta-q', 'alpha-q', 'thirty-q']), JSON.stringify(rep.games));
    ok('a. a room is never in accuracy', !slugs.some(s => s.indexOf('escape-') === 0), slugs);
    ok('a. a shot game is never in accuracy', slugs.indexOf('trig-wars') < 0, slugs);
    ok('a. 29 answers are below the minimum, however low the score', slugs.indexOf('twentynine-q') < 0, slugs);
    // overall: alpha 41 (21 right), beta 35 (14), thirty 30 (21), twentynine 29 (1), delta 41 marked (10 right)
    ok('a. overall accuracy counts question games only', rep.overall.total === 176 && rep.overall.correct === 67, JSON.stringify(rep.overall));
    const hk = rep.hardest.map(q => q.slug + '|' + q.level + '|' + q.qid);
    ok('b. hardest: game + level + question_id, 10 or more attempts, lowest first',
      JSON.stringify(hk) === JSON.stringify(['alpha-q|gcse|h00000001', 'alpha-q|gcse|h00000002']), JSON.stringify(rep.hardest));
    ok('b. no hardest row without a question_id', rep.hardest.every(q => q.qid), JSON.stringify(rep.hardest));
    ok('b. a room\'s question_id never reaches hardest questions', !rep.hardest.some(q => q.slug.indexOf('escape-') === 0));
    ok('b. the count of games sending question_id', rep.idGames === 1, rep.idGames);
    const ra = rep.rooms.map(r => [r.slug, r.starts, r.escaped, r.timedOut, r.rate, r.perLock]);
    ok('c. rooms: started, escaped, timed out, rate, attempts per lock, lowest escape rate first',
      JSON.stringify(ra) === JSON.stringify([['escape-beta', 2, 0, 0, 0, 5], ['escape-alpha', 4, 1, 2, 0.25, 4]]), JSON.stringify(ra));
    const ea = rep.rooms.find(r => r.slug === 'escape-alpha') || {};
    ok('c. a win (3/3) is escaped; a timeout (1/3) and a timeout with no lock open (0/3) are timed out',
      ea.escaped === 1 && ea.timedOut === 2, JSON.stringify(ea));
    ok('d. shot games named', JSON.stringify(rep.shots) === '["trig-wars"]', rep.shots);
    const d = rep.games.find(g => g.slug === 'delta-q') || {};
    ok('e. a blank before 29 Sep 20:00 UTC is a wrong answer; after it, not marked', d.total === 41 && d.correct === 10, JSON.stringify(d));
    ok('e. Prisoner\'s Dilemma\'s blanks are not marked', !rep.games.some(g => g.slug === 'prisoners-dilemma') && rep.overall.total === 176);

    // ---- end to end, email and Dashboard
    api.sendDailyReport();
    const mail = env.mails[0] || { body: '' }, dash = env.sheets['Dashboard'];
    ok('one email sent', env.mails.length === 1, env.mails.length);
    ok('the email: overall accuracy from question games', /Overall accuracy: +42% \(question games, 135 marked answers\)/.test(mail.body), mail.body.match(/Overall accuracy.*/));
    ok('the email: accuracy, hardest, rooms and the shot line', ['ACCURACY BY GAME', 'HARDEST QUESTIONS', 'ESCAPE ROOMS', 'alpha-q · gcse · h00000001 — 25% correct (12 attempts)',
      'escape-alpha — 4 started, 1 escaped (25%), 2 timed out, 4.0 attempts per lock opened', 'Left out of accuracy (a correct answer there is a hit, not a right answer): trig-wars.'].every(t => mail.body.indexOf(t) >= 0), mail.body);
    ok('the email has no fetch-failure line when games.json is read', mail.body.indexOf('could not be read') < 0);
    const dt = dash ? dashText(dash) : '';
    ok('the Dashboard: question-game accuracy, hardest by question_id, rooms, the shot line',
      dt.indexOf('Accuracy by Game — Last 7 Days (question games, min 30') >= 0 && dt.indexOf('alpha-q | gcse | h00000001 | 12 | 3') >= 0 &&
      dt.indexOf('Room | Started | Escaped | Escape % | Timed out | Attempts per lock') >= 0 && dt.indexOf('escape-alpha | 4 | 1 | 25% | 2 | 4') >= 0 && dt.indexOf('Left out of accuracy') >= 0 && dt.indexOf('1 game sends question_id so far') >= 0, dt);
    out.push(['__sample_email', true, mail.body]); out.push(['__sample_dash', true, dt]);

    // ---- doPost: the column-order rule (ROOM-TIMES). The 18 columns before 7 Nov 2026 keep their order and
    // detail is appended last; each posted field lands under its own header; a Sheet whose row 1 has only the old
    // 18 headers gets "detail" written into S1 by the first post, as question_id's R1 was.
    {
      const OLD = HEAD.slice(0, 18);
      ({ api, env } = load('ok', OLD.slice()));
      ok('doPost: EXPECTED_HEADERS is the 18 earlier columns in order, then detail',
         JSON.stringify(api.EXPECTED_HEADERS) === JSON.stringify(OLD.concat(['detail'])), JSON.stringify(api.EXPECTED_HEADERS));
      const sent = {};
      api.EXPECTED_HEADERS.forEach(h => { if (h !== 'timestamp') sent[h] = 'v_' + h; });
      sent.detail = 'escaped wrongs:1 hints:2 used:612 played:567 locks:182,431,567';
      const res = api.doPost({ postData: { contents: JSON.stringify(sent) } });
      const got = env.events.getDataRange().getValues().slice(-1)[0];
      const misplaced = api.EXPECTED_HEADERS.filter((h, i) => h !== 'timestamp' && got[i] !== sent[h]);
      ok('doPost: every field is written under its own header, detail in the last column',
         res && res.ok && got.length === api.EXPECTED_HEADERS.length && !misplaced.length && got[got.length - 1] === sent.detail,
         JSON.stringify({ res, misplaced, got }));
      ok('doPost: an old row 1 gains "detail" in S1 on the first post',
         env.events.cells['1,19'] === 'detail' && env.events.cells['1,18'] === 'question_id', JSON.stringify(env.events.cells));
      const bare = Object.assign({}, sent); delete bare.detail;
      api.doPost({ postData: { contents: JSON.stringify(bare) } });
      const g2 = env.events.getDataRange().getValues().slice(-1)[0];
      ok('doPost: an event with no detail leaves the last column blank', g2.length === api.EXPECTED_HEADERS.length && g2[g2.length - 1] === '',
         JSON.stringify(g2));
    }

    // ---- games.json unreadable: every game a question game, one line saying so
    for (const mode of ['throw', '404']) {
      ({ api, env } = load(mode));
      const k2 = api.rptLoadKinds(), r2 = api.rptBuild(rows, col, k2);
      ok('fetch ' + mode + ': trig-wars is counted as a question game', !k2.ok && r2.games.some(g => g.slug === 'trig-wars') && r2.shots.length === 0, JSON.stringify(r2.games.map(g => g.slug)));
      ok('fetch ' + mode + ': rooms still by slug', r2.rooms.length === 2);
      api.sendDailyReport();
      const m2 = (env.mails[0] || { body: '' }).body, d2 = env.sheets['Dashboard'] ? dashText(env.sheets['Dashboard']) : '';
      const line = 'games.json could not be read, so every game is counted as a question game today.';
      ok('fetch ' + mode + ': one line in the email and one on the Dashboard', m2.split(line).length === 2 && d2.split(line).length === 2, m2.slice(0, 300));
    }

    // ---- h. a posted value is data, never a formula (SHEET-FORMULA-CELLS, 14 Nov 2026). appendRow and setValues
    // read a string as if it were typed, so "=..." became a formula. What these checks read is the value the script
    // HANDS to the Sheet (the fake stores it as given): a leading apostrophe there is what makes Sheets keep text.
    {
      ({ api, env } = load('ok', HEAD.slice()));          // an events tab holding only its header row
      const at = h => HEAD.indexOf(h);
      const post = fields => {
        api.doPost({ postData: { contents: JSON.stringify(Object.assign({ event: 'question_answered' }, fields)) } });
        return env.events.getDataRange().getValues().slice(-1)[0];
      };
      const wrote = (name, fields, header, want) => {
        const row = post(fields), got = row[at(header)];
        ok('h. doPost: ' + name, got === want && row.length === HEAD.length, typeof got + ' ' + JSON.stringify(got));
      };
      wrote('detail "=1+1" is written behind an apostrophe', { detail: '=1+1' }, 'detail', "'=1+1");
      wrote('game_slug =IMAGE("x") is written behind an apostrophe', { game_slug: '=IMAGE("x")' }, 'game_slug', '\'=IMAGE("x")');
      wrote('level "+1" is written behind an apostrophe', { level: '+1' }, 'level', "'+1");
      wrote('question_id "@a" is written behind an apostrophe', { question_id: '@a' }, 'question_id', "'@a");
      wrote('detail "-x" is written behind an apostrophe', { detail: '-x' }, 'detail', "'-x");
      wrote('a leading tab or carriage return is written behind an apostrophe',
            { detail: '\t=1+1', mode: '\r=1+1' }, 'detail', "'\t=1+1");
      ok('h. doPost: the carriage return too', env.events.getDataRange().getValues().slice(-1)[0][at('mode')] === "'\r=1+1");
      wrote('"-" alone and "-3x" are not plain numbers: behind an apostrophe', { detail: '-3x', mode: '-' }, 'detail', "'-3x");
      wrote('an array is written as its JSON text, not left to the Sheet', { detail: ['=1+1'] }, 'detail', '["=1+1"]');
      // controls: none of these may change
      wrote('question_index -3 (a number) is unchanged', { question_index: -3 }, 'question_index', -3);
      wrote('"-3" (a string) is unchanged', { question_index: '-3' }, 'question_index', '-3');
      wrote('"-3.5" (a string) is unchanged', { score: '-3.5' }, 'score', '-3.5');
      wrote('"2026-11-14" is unchanged', { detail: '2026-11-14' }, 'detail', '2026-11-14');
      wrote('"true" (a string) is unchanged', { correct: 'true' }, 'correct', 'true');
      wrote('false and 0 are still written, not blanked', { correct: false, score: 0 }, 'correct', false);
      const real = { event: 'game_completed', game_slug: 'six-sevens-bruv', level: 'ks3', mode: 'practice-q20', question_index: 7,
        correct: true, attempts: 2, score: 1480, questions_answered: 20, questions_correct: 17, previous_score: 1210,
        difficulty: 'mixed', filter_type: 'search', filter_value: 'v1|level=gcse;topic=all;fresh=0;su=1;sl=5;q=ratio;n=12',
        client_ts: '2026-11-14T11:00:00.000Z', seq: 41, question_id: 'h1a2b3c4d',
        detail: 'escaped wrongs:1 hints:2 used:612 played:567 locks:182,431,567' };
      const realRow = post(real);
      ok('h. doPost: an ordinary event is written exactly as it was sent, field for field',
         HEAD.every((h, i) => h === 'timestamp' || realRow[i] === real[h]), JSON.stringify(realRow));

      // the Dashboard writes slugs, levels and question ids read back from the Sheet: the same rule there.
      // asRead models what Sheets hands back (the apostrophe is not part of a cell's value); it is a model, not Google.
      const asRead = v => typeof v === 'string' && v.charAt(0) === "'" ? v.slice(1) : v;
      const evil = { game_slug: '=IMAGE("x")', level: '+1', question_id: '@a' }, back = [];
      const keep = row => { const r = row.map(asRead); r[0] = Y; back.push(r); };
      for (let k = 0; k < 30; k++) keep(post(Object.assign({ correct: k < 12 }, evil)));
      keep(post(Object.assign({}, evil, { event: 'game_started' }))); keep(post(Object.assign({}, evil, { event: 'game_started' })));
      keep(post(Object.assign({}, evil, { event: 'game_completed' })));
      ok('h. read back (model): the cell is the posted text, without the apostrophe',
         back[0][at('game_slug')] === '=IMAGE("x")' && back[0][at('level')] === '+1' && back[0][at('question_id')] === '@a', JSON.stringify(back[0]));
      ({ api, env } = load('ok', null, rows.concat(back)));
      const rh = api.rptBuild(rows.concat(back), col, api.rptLoadKinds());
      const gh = rh.games.find(g => g.slug === '=IMAGE("x")') || {}, qh = rh.hardest.find(q => q.qid === '@a') || {};
      ok('h. the report reads it as an ordinary game: 12 of 30, keyed by its own level and question_id',
         gh.total === 30 && gh.correct === 12 && qh.slug === '=IMAGE("x")' && qh.level === '+1' && qh.total === 30, JSON.stringify([gh, qh]));
      api.sendDailyReport();
      const dh = env.sheets['Dashboard'], th = dh ? dashText(dh) : '';
      ok('h. the Dashboard writes the slug, level and question id behind an apostrophe',
         th.indexOf('\'=IMAGE("x") | 2 | 1 | 50%') >= 0 && th.indexOf("\n'+1 | 2\n") >= 0 && th.indexOf('\'=IMAGE("x") | 30 | 12 | 40%') >= 0 &&
         th.indexOf('\'=IMAGE("x") | \'+1 | \'@a | 30 | 12 | 40%') >= 0, th);
      const formulas = dh ? Object.keys(dh.cells).filter(k => { const v = dh.cells[k];
        return typeof v === 'string' && (/^[=+@\t\r]/.test(v) || (v.charAt(0) === '-' && !/^-\d+(\.\d+)?$/.test(v))); }) : ['no Dashboard'];
      ok('h. no cell the Dashboard writes could be read as a formula', formulas.length === 0, formulas.map(k => k + ' ' + dh.cells[k]).join('; '));
      ok('h. the email names the game by its text (plain text: nothing to run)',
         (env.mails[0] || { body: '' }).body.indexOf('=IMAGE("x") — 2 starts, 1 completed (50%)') >= 0, (env.mails[0] || { body: '' }).body);
    }

    // ---- g. safe tallies (COUNTS-SAFE-TALLY, 14 Nov 2026). A game_slug, level or question_id is whatever anyone
    // posted. Four games whose slug and level are each the name of a built-in object member, added to the rows
    // above: each must be reported like any other game, and nothing already reported may move. Kept last, and on
    // its own rows, so every check above reads the same fixture as before.
    {
      const NAMES = ['constructor', '__proto__', 'toString', 'hasOwnProperty'];
      const extra = [];
      NAMES.forEach((n, i) => {
        for (let k = 0; k < 30; k++) extra.push(row(Y, 'question_answered', n, n, k < 6 + i, 'h0000000b'));   // 6, 7, 8, 9 right of 30
        extra.push(row(Y, 'game_started', n, n), row(Y, 'game_started', n, n), row(Y, 'game_completed', n, n));
      });
      const named = rows.concat(extra);
      ({ api, env } = load('ok', null, named));
      const kn = api.rptLoadKinds();
      ok('g. kinds: a slug named like a built-in member is a question game',
         NAMES.every(n => api.rptKind(n, kn) === 'question') && api.rptKind('trig-wars', kn) === 'shot', NAMES.map(n => api.rptKind(n, kn)));
      const base = api.rptBuild(rows, col, kn), rn = api.rptBuild(named, col, kn);
      const line = g => g.slug + ' ' + g.correct + '/' + g.total;
      ok('g. accuracy: each is listed with its own figures, lowest first',
         JSON.stringify(rn.games.map(line)) === JSON.stringify(['constructor 6/30', '__proto__ 7/30', 'delta-q 10/41', 'toString 8/30',
           'hasOwnProperty 9/30', 'beta-q 14/35', 'alpha-q 21/41', 'thirty-q 21/30']), JSON.stringify(rn.games.map(line)));
      ok('g. overall: 120 more marked answers, 30 more right, both numbers',
         rn.overall.total === 296 && rn.overall.correct === 97, JSON.stringify(rn.overall));
      ok('g. hardest: keyed game + level + question_id as for any game',
         JSON.stringify(rn.hardest.map(q => q.slug + '|' + q.level + '|' + q.qid + ' ' + q.correct + '/' + q.total)) === JSON.stringify([
           'constructor|constructor|h0000000b 6/30', '__proto__|__proto__|h0000000b 7/30', 'alpha-q|gcse|h00000001 3/12',
           'toString|toString|h0000000b 8/30', 'hasOwnProperty|hasOwnProperty|h0000000b 9/30', 'alpha-q|gcse|h00000002 18/20']), JSON.stringify(rn.hardest));
      ok('g. the count of games sending question_id is 5', rn.idGames === 5, rn.idGames);
      const others = r => JSON.stringify([r.games.filter(g => NAMES.indexOf(g.slug) < 0), r.hardest.filter(q => NAMES.indexOf(q.slug) < 0), r.rooms, r.shots]);
      ok('g. every other game, question, room and shot line is unchanged by them', others(rn) === others(base), others(rn));
      api.sendDailyReport();
      const mn = (env.mails[0] || { body: '' }).body, dn = env.sheets['Dashboard'] ? dashText(env.sheets['Dashboard']) : '';
      const clean = t => !/function|native code|\[object|NaN|undefined/.test(t);
      ok('g. the email: each is in top games and the level breakdown, with numbers',
         env.mails.length === 1 && NAMES.every(n => mn.indexOf('. ' + n + ' — 2 starts, 1 completed (50%)') >= 0 && mn.indexOf('\n  ' + n + ': 2 starts\n') >= 0) &&
         /Games started: +14\n/.test(mn) && /Overall accuracy: +34% \(question games, 255 marked answers\)/.test(mn) && clean(mn), mn);
      ok('g. the Dashboard: each is in top games, the level breakdown and accuracy, with numbers',
         NAMES.every((n, i) => dn.indexOf(n + ' | 2 | 1 | 50%') >= 0 && dn.indexOf('\n' + n + ' | 2\n') >= 0 && dn.indexOf(n + ' | 30 | ' + (6 + i) + ' | ') >= 0) &&
         dn.indexOf('2026-11-03 | 14') >= 0 && clean(dn), dn);
      // before the fix a tally for "__proto__", "constructor" or "toString" was kept ON the built-in it named
      const builtins = { 'Object.prototype': Object.prototype, 'Object': Object, 'toString': Object.prototype.toString, 'hasOwnProperty': Object.prototype.hasOwnProperty };
      const stray = Object.keys(builtins).filter(b => ['total', 'correct', 'starts'].some(k => Object.prototype.hasOwnProperty.call(builtins[b], k)));
      ok('g. no tally was written onto a built-in object', stray.length === 0, stray.join(', '));
    }

    // ---- i. daily activity: games started and questions answered (DAILY-ANSWERS, Jon 17 Nov 2026). Rows of their
    // own over five days; the expected table is written by hand below.
    {
      const day = (d, h) => d + 'T' + (h || '10') + ':00:00.000Z';
      const dr = [];
      const n = (k, f) => { for (let i = 0; i < k; i++) dr.push(f(i)); };
      // 30 Oct: 3 starts (two question, one room); 4 question answers, one of them correct: null (not marked, still
      // an answer); 5 room answers and 3 shot answers, left out
      n(2, () => row(day('2026-10-30'), 'game_started', 'alpha-q', 'gcse'));
      dr.push(row(day('2026-10-30'), 'game_started', 'escape-alpha', 'all'));
      n(3, i => row(day('2026-10-30', '11'), 'question_answered', 'alpha-q', 'gcse', i < 2, 'h00000001'));
      { const r = row(day('2026-10-30', '11'), 'question_answered', 'alpha-q', 'gcse', '', 'h00000001'); r[6] = null; dr.push(r); }
      n(5, i => row(day('2026-10-30', '12'), 'question_answered', 'escape-alpha', 'all', i < 1, 'h0000000a'));
      n(3, i => row(day('2026-10-30', '12'), 'question_answered', 'trig-wars', 'gcse', i < 1));
      // 31 Oct: answers but no starts (a game begun before midnight): 0 starts, 6 answers
      n(6, i => row(day('2026-10-31', '00'), 'question_answered', 'beta-q', 'gcse', i < 3));
      // 1 Nov: 2 starts (a question game and a shot game), only shot answers: 2 starts, 0 answers
      dr.push(row(day('2026-11-01'), 'game_started', 'beta-q', 'gcse'), row(day('2026-11-01'), 'game_started', 'trig-wars', 'gcse'));
      n(2, () => row(day('2026-11-01', '11'), 'question_answered', 'trig-wars', 'gcse', true));
      // 2 Nov: room answers only: neither count, so no row
      n(4, i => row(day('2026-11-02'), 'question_answered', 'escape-beta', 'all', i < 2));
      // 3 Nov: 1 start, 3 question answers and 2 room answers
      dr.push(row(day('2026-11-03'), 'game_started', 'alpha-q', 'gcse'));
      n(3, i => row(day('2026-11-03', '11'), 'question_answered', 'alpha-q', 'gcse', i < 1, 'h00000002'));
      n(2, () => row(day('2026-11-03', '11'), 'question_answered', 'escape-beta', 'all', false));
      ({ api, env } = load('ok', null, dr));
      api.rebuildDashboard(dr, dr, col, api.rptLoadKinds());
      const di = env.sheets['Dashboard'] ? dashText(env.sheets['Dashboard']).split('\n') : [];
      const at5 = di.indexOf('Daily Activity — Last 30 Days');
      const t5 = at5 < 0 ? [] : di.slice(at5 + 1);
      while (t5.length && t5[t5.length - 1] === '') t5.pop();
      ok('i. the table: Date, Games Started, Questions Answered; a row for every day with either count, 0 where missing',
         JSON.stringify(t5) === JSON.stringify(['Date | Games Started | Questions Answered', '2026-10-30 | 3 | 4', '2026-10-31 | 0 | 6',
           '2026-11-01 | 2 | 0', '2026-11-03 | 1 | 3']), JSON.stringify(t5));
      const c5 = env.charts.find(c => c.some(([k, a]) => k === 'setOption' && a[0] === 'title' && /^Daily/.test(a[1]))) || [];
      const opt = {}; c5.forEach(([k, a]) => { if (k === 'setOption') opt[a[0]] = a[1]; });
      const call = name => (c5.find(([k]) => k === name) || [null, []])[1];
      const rng = (call('addRange')[0] || {}).dims || [];
      ok('i. the chart: a LINE over Date and two series, one row per day plus the header, where it was',
         call('setChartType')[0] === 'LINE' && rng[1] === 1 && rng[2] === 5 && rng[3] === 3 && rng[0] === at5 + 2 &&
         JSON.stringify(call('setPosition')) === JSON.stringify([at5 + 1, 6, 0, 0]), JSON.stringify(c5.filter(([k]) => k !== 'setOption')));
      ok('i. the chart: starts on axis 0, answers on axis 1, both axes titled, a legend at the bottom, size and colours',
         opt.title === 'Daily Games Started and Questions Answered — Last 30 Days' && JSON.stringify(opt.legend) === '{"position":"bottom"}' &&
         opt.series && opt.series[1] && opt.series[1].targetAxisIndex === 1 && (!opt.series[0] || (opt.series[0].targetAxisIndex || 0) === 0) &&
         opt.vAxes && opt.vAxes[0].title === 'Games started' && opt.vAxes[1].title === 'Questions answered' &&
         opt.width === 500 && opt.height === 280 && JSON.stringify(opt.colors) === '["#0ea5e9","#0d9488"]',
         JSON.stringify(opt));
      ok('i. the chart: series named from the header row (setNumHeaders 1) and straight lines (no curveType)',
         JSON.stringify(call('setNumHeaders')) === '[1]' && !('curveType' in opt), JSON.stringify([call('setNumHeaders'), opt]));
      const cells = env.sheets['Dashboard'] ? env.sheets['Dashboard'].cells : {};
      ok('i. no cell in the table is undefined, NaN or text where a count belongs',
         t5.slice(1).every(l => /^\d{4}-\d\d-\d\d \| \d+ \| \d+$/.test(l)) && Object.keys(cells).every(k => cells[k] !== undefined), t5.join(' / '));
    }

    // ---- j. DASHBOARD-GLANCE (Jon, 18 Nov 2026): sections A to H on rows of their own, every figure worked out by
    // hand. NOW is Wed 4 Nov 2026 07:00 UTC (London is on UTC in November, as the fake formatDate assumes): this week
    // is from Wed 28 Oct, the previous week from Wed 21 Oct, GA4's last complete day is 3 Nov, and the launch cut-off
    // (14 days) is 21 Oct. Each run goes through sendDailyReport, so its real weekRows, monthRows and prevWeekRows.
    {
      const at = (d, hm) => d + 'T' + hm + ':00.000Z';
      const QI = 5, COR = 6, QA = 9, QC = 10, FT = 13, FV = 14, QID = 17, DET = 18;
      const ev = (ts, event, slug, f) => Object.assign(row(ts, event, slug, 'gcse'), f || {});
      const lines = sh => sh ? dashText(sh).split('\n') : [];
      const block = (ls, title) => {
        const i = ls.findIndex(l => l.indexOf(title) === 0);
        if (i < 0) return null;
        const out = [];
        for (let k = i + 1; k < ls.length && ls[k] !== ''; k++) out.push(ls[k]);
        return out;
      };
      const same = (got, want) => JSON.stringify(got) === JSON.stringify(want);
      const fmtOf = (sh, ls, line, c) => { const r = ls.indexOf(line) + 1; return r > 0 ? (sh.fmt[r + ',' + c] || {}) : {}; };
      const runDash = (rowsIn, opts) => {
        ({ api, env } = load('ok', null, rowsIn, opts));
        api.sendDailyReport();
        const sh = env.sheets['Dashboard'];
        return { sh, ls: lines(sh) };
      };
      const GA4D_HEAD = ['date', 'country', 'activeUsers', 'sessions', 'engagedSessions', 'eventCount'];
      const GA4S_HEAD = ['date', 'sessionSource', 'sessionMedium', 'deviceCategory', 'landingPage', 'sessions', 'engagedSessions', 'activeUsers'];
      const MISSING = 'GA4 figures not available yet.';

      // ---- A. Is it growing? This week (2 Nov): 5 starts of 3 games; quiz-a answers right, right, wrong and one
      // unmarked (4 answers, 2 of 3 marked right = 67%); shot and room answers left out. Previous week (22 Oct): 4
      // starts of 1 game, 2 answers both right (100%). GA4: 10 + 5 engaged sessions this week; today's row and a row
      // before the previous week are outside both, so the previous week is 0: "new".
      const W = '2026-11-02', P = '2026-10-22';
      const ra = [];
      ['quiz-a', 'quiz-a', 'quiz-a', 'quiz-b', 'escape-gamma'].forEach(s => ra.push(ev(at(W, '10:00'), 'game_started', s)));
      [true, true, false].forEach(c => ra.push(ev(at(W, '10:05'), 'question_answered', 'quiz-a', { [COR]: c })));
      ra.push(ev(at(W, '10:06'), 'question_answered', 'quiz-a', { [COR]: '' }));
      ra.push(ev(at(W, '10:07'), 'question_answered', 'trig-wars', { [COR]: true }), ev(at(W, '10:07'), 'question_answered', 'trig-wars', { [COR]: false }));
      for (let i = 0; i < 3; i++) ra.push(ev(at(W, '10:08'), 'question_answered', 'escape-gamma', { [COR]: i === 0 }));
      for (let i = 0; i < 4; i++) ra.push(ev(at(P, '10:00'), 'game_started', 'quiz-a'));
      ra.push(ev(at(P, '10:05'), 'question_answered', 'quiz-a', { [COR]: true }), ev(at(P, '10:05'), 'question_answered', 'quiz-a', { [COR]: true }));
      const ga4dA = [GA4D_HEAD, ['2026-10-30', 'United Kingdom', 5, 10, 10, 99], ['2026-11-03', 'United States', 1, 5, 5, 9],
        ['2026-11-04', 'United Kingdom', 1, 100, 100, 1], ['2026-10-20', 'United Kingdom', 1, 50, 50, 1]];
      let d = runDash(ra, { ga4: { 'GA4 country daily': ga4dA } });
      const headA = 'Games started | Questions answered | % correct | Different games played | Engaged sessions';
      const chA = '▲ 25% | ▲ 100% | ▼ 33 pts | ▲ 200% | ▲ new';
      ok('j. A: this week against the previous 7, % correct in points, "new" when the earlier week is 0',
         same(block(d.ls, 'Is it growing?'), [headA, '5 | 4 | 67% | 3 | 15', chA]), JSON.stringify(block(d.ls, 'Is it growing?')));
      ok('j. A: up is green; % correct is grey though it fell',
         fmtOf(d.sh, d.ls, chA, 1).setFontColor === '#15803d' && fmtOf(d.sh, d.ls, chA, 5).setFontColor === '#15803d' &&
         fmtOf(d.sh, d.ls, chA, 3).setFontColor === '#6b7280', JSON.stringify([1, 2, 3, 4, 5].map(c => fmtOf(d.sh, d.ls, chA, c))));
      // ---- no GA4 tabs at all: one line in A, D and E, and the rest of the Dashboard is still built
      d = runDash(ra, {});
      ok('j. a missing GA4 tab gives the line in A, D and E, never an error',
         same(block(d.ls, 'Is it growing?'), [headA, '5 | 4 | 67% | 3 | –', '▲ 25% | ▲ 100% | ▼ 33 pts | ▲ 200% | –', MISSING]) &&
         same(block(d.ls, 'Did my posts bring visitors?'), [MISSING]) && same(block(d.ls, 'Who uses it?'), [MISSING]) &&
         d.ls.filter(l => l === MISSING).length === 3 && d.ls.indexOf('Daily Activity — Last 30 Days') > 0, d.ls.join(' / '));

      // ---- B and C1
      const rb = [];
      const D2 = '2026-11-02', D3 = '2026-11-03';
      const answersOf = (slug, n, right, qid) => { for (let i = 0; i < n; i++) rb.push(ev(at(D2, '10:00'), 'question_answered', slug, { [COR]: i < right, [QID]: qid })); };
      answersOf('quiz-c', 11, 1, 'q1');          // 1 of 11 = 9%: listed
      answersOf('quiz-c', 10, 1, 'q2');          // 1 of 10 = 10%: not under 10%
      answersOf('quiz-c', 9, 0, 'q3');           // 0 of 9: too few answers
      answersOf('quiz-c', 12, 0, 'q4');          // 0 of 12: listed first
      for (let i = 0; i < 3; i++) rb.push(ev(at(D2, '10:00'), 'question_answered', 'quiz-c', { [COR]: '', [QID]: 'q4' }));   // unmarked
      answersOf('escape-gamma', 12, 0, 'lock-1');   // a room's lock, 0 of 12: never listed
      // B2: starts an hour apart (never a class); quits by question_index
      const hourly = (slug, n, day) => { for (let i = 0; i < n; i++) rb.push(ev(at(day, String(8 + i).padStart(2, '0') + ':00'), 'game_started', slug)); };
      const quits = (slug, day, positions) => positions.forEach(q => rb.push(ev(at(day, '20:00'), 'game_abandoned', slug, { [QI]: q })));
      hourly('quiz-d', 12, '2026-10-29'); quits('quiz-d', '2026-10-29', [3, 3, 3, 3, 3, 3, 5, 5, 5, 5]);   // 10 of 12, most at 3 (6)
      hourly('quiz-f', 10, '2026-10-30'); quits('quiz-f', '2026-10-30', [2, 2, 2, 2, 2, 4, 4, 4, 4, 4]);   // 10 of 10, a tie: 2 (5)
      hourly('quiz-e', 9, '2026-10-31'); quits('quiz-e', '2026-10-31', [1, 1, 1, 1, 1, 1, 1, 1, 1]);       // 9 quits: left out
      // C1: class-a, 10 starts 29 minutes apart from 09:00 (last 13:21); answers at 09:05 x5 and 13:50 x2 are in, 13:52
      // (31 minutes after the last) and 08:59 (before the first) are out: 7. class-b, 6 + 6 starts with a 31-minute gap
      // between: two runs of 6, none counted. class-c, 9 starts 10 minutes apart: not counted.
      const stepped = (slug, day, first, n, step) => { const t0 = Date.parse(at(day, first)); for (let i = 0; i < n; i++) rb.push(ev(new Date(t0 + i * step * 60000).toISOString(), 'game_started', slug)); };
      stepped('class-a', D2, '09:00', 10, 29);
      [['09:05', 5], ['13:50', 2], ['13:52', 1], ['08:59', 1]].forEach(([hm, n]) => { for (let i = 0; i < n; i++) rb.push(ev(at(D2, hm), 'question_answered', 'class-a', { [COR]: true })); });
      stepped('class-b', D3, '09:00', 6, 29); stepped('class-b', D3, '11:56', 6, 29);
      stepped('class-c', D3, '14:00', 9, 10);
      d = runDash(rb, {});
      const b1 = block(d.ls, 'Check these questions');
      ok('j. B1: under 10% right on 10+ marked answers, lowest first; 10% of 10, 0 of 9 and a room\'s lock not listed',
         same(b1, ['Game | Level | Question id | Marked answers | % right', 'quiz-c | gcse | q4 | 12 | 0', 'quiz-c | gcse | q1 | 11 | 9%',
           'Decode an id: python scripts/decode-question-ids.py <game> --id <id>']), JSON.stringify(b1));
      ok('j. B1: each flagged row on a red background',
         fmtOf(d.sh, d.ls, 'quiz-c | gcse | q4 | 12 | 0', 1).setBackground === '#fee2e2' && fmtOf(d.sh, d.ls, 'quiz-c | gcse | q1 | 11 | 9%', 5).setBackground === '#fee2e2');
      const b2 = block(d.ls, 'Where students quit');
      ok('j. B2: 10+ quits, highest % first, the position most quit at; 9 quits left out',
         same(b2, ['Game | Starts | Abandoned | % abandoned | Most quit at position | Quit there', 'quiz-f | 10 | 10 | 1 | 2 | 5',
           'quiz-d | 12 | 10 | 83% | 3 | 6', 'Position in the run, not which question: game_abandoned carries question_index only.']), JSON.stringify(b2));
      const c1 = block(d.ls, 'Probably a class');
      ok('j. C1: 10 starts 29 minutes apart counted; a 31-minute gap splits a run; 9 starts not counted',
         same(c1, ['Game | Date | First start | Last start | Starts | Questions answered', 'class-a | 2026-11-02 | 09:00 | 13:21 | 10 | 7']), JSON.stringify(c1));

      // ---- C2, C3 and H
      const rm = [];
      [at('2026-11-03', '15:29'), at('2026-11-03', '15:30'), at('2026-10-31', '10:00'), at('2026-11-02', '08:59'), at('2026-11-01', '22:00'),
        at('2026-10-28', '18:00')].forEach(t => rm.push(ev(t, 'game_started', 'quiz-w')));
      for (let i = 0; i < 3; i++) rm.push(ev(at(W, '11:00'), 'filter_applied', '', { [FT]: 'search', [FV]: 'v1|page=games;q=ratio' }));
      rm.push(ev(at(W, '11:00'), 'filter_applied', '', { [FT]: 'chip', [FV]: 'v1|page=games;level=gcse' }));
      rm.push(ev(at(P, '11:00'), 'filter_applied', '', { [FT]: 'search', [FV]: 'v1|page=games;q=ratio' }));   // the week before: out
      [['fact_viewed', 8], ['fact_expanded', 3], ['fact_game_clicked', 2], ['fact_shared', 1]].forEach(([e, n]) => {
        for (let i = 0; i < n; i++) rm.push(ev(at(W, '12:00'), e, 'misunderstood-maths')); });
      rm.push(ev(at(P, '12:00'), 'fact_viewed', 'misunderstood-maths'));   // the week before: out
      d = runDash(rm, {});
      const c2 = block(d.ls, 'When it is used');
      ok('j. C2: Tue 15:29 is the school day, 15:30 is not; Saturday 10:00 is Sat-Sun',
         same(c2, ['Days | Before 09:00 | 09:00-15:30 | 15:30-18:00 | 18:00-22:00 | After 22:00', 'Mon-Fri | 1 | 1 | 1 | 1 | 0',
           'Sat-Sun | 0 | 1 | 0 | 0 | 1', 'School day = 09:00-15:30, Mon-Fri. Term dates not applied.']), JSON.stringify(c2));
      const c3 = block(d.ls, 'What people look for on the portal');
      ok('j. C3: filters by type and value, most first, this week only',
         same(c3, ['Filter | Value | Times', 'search | v1|page=games;q=ratio | 3', 'chip | v1|page=games;level=gcse | 1']), JSON.stringify(c3));
      const h = block(d.ls, 'Misunderstood Maths');
      ok('j. H: facts viewed, expanded, game links, shared, clicks as % of views',
         same(h, ['Facts viewed | Expanded | Game links clicked | Shared | Game clicks % of views', '8 | 3 | 2 | 1 | 25%']), JSON.stringify(h));

      // ---- D and E (GA4). Sources this week: lnkd.in (LinkedIn), m.facebook.com (Facebook), google / organic (Google
      // search), bing / organic (Other search), (direct) (Direct), www.tes.com (Tes), duckduckgo / referral (Other);
      // today's row is out. The week before: LinkedIn 2 and Google 20 engaged. Countries this week: UK 30 + 20 of 72.
      const ga4s = [GA4S_HEAD,
        ['2026-10-30', 'lnkd.in', 'referral', 'mobile', '/games/a/', 10, 6, 9],
        ['2026-11-02', 'm.facebook.com', 'referral', 'mobile', '/', 4, 1, 4],
        ['2026-11-02', 'google', 'organic', 'desktop', '/', 20, 15, 18],
        ['2026-11-02', 'bing', 'organic', 'desktop', '/games/b/', 5, 4, 5],
        ['2026-11-02', '(direct)', '(none)', 'tablet', '/', 8, 2, 8],
        ['2026-11-03', 'www.tes.com', 'referral', 'desktop', '/games/a/', 3, 3, 3],
        ['2026-11-03', 'duckduckgo', 'referral', 'mobile', '/games/c/', 2, 1, 2],
        ['2026-11-04', 'google', 'organic', 'desktop', '/', 99, 99, 99],
        ['2026-10-22', 'lnkd.in', 'referral', 'mobile', '/', 4, 2, 4],
        ['2026-10-22', 'google', 'organic', 'desktop', '/', 30, 20, 25]];
      const ga4d = [GA4D_HEAD, ['2026-10-30', 'United Kingdom', 5, 10, 30, 99], ['2026-11-02', 'United Kingdom', 5, 10, 20, 99],
        ['2026-11-02', 'United States', 1, 5, 10, 9], ['2026-11-03', 'India', 1, 9, 6, 9], ['2026-11-03', 'Ireland', 1, 2, 3, 9],
        ['2026-11-03', 'Germany', 1, 2, 2, 9], ['2026-11-03', 'France', 1, 1, 1, 9], ['2026-10-22', 'United Kingdom', 1, 1, 40, 1],
        ['2026-11-04', 'France', 1, 500, 500, 1]];
      d = runDash([], { ga4: { 'GA4 country daily': ga4d, 'GA4 sources daily': ga4s } });
      const d1 = block(d.ls, 'Visitors by channel');
      ok('j. D1: lnkd.in is LinkedIn, m.facebook.com Facebook, google/organic Google search, bing/organic Other search, (direct) Direct',
         same(d1, ['Channel | Sessions | Engaged sessions | % engaged | Change in engaged sessions', 'Google search | 20 | 15 | 75% | ▼ 25%',
           'Other search | 5 | 4 | 80% | ▲ new', 'LinkedIn | 10 | 6 | 60% | ▲ 200%', 'Facebook | 4 | 1 | 25% | ▲ new', 'Tes | 3 | 3 | 1 | ▲ new',
           'Direct | 8 | 2 | 25% | ▲ new', 'Other | 2 | 1 | 50% | ▲ new']), JSON.stringify(d1));
      ok('j. D1: a fall is red, a rise green', fmtOf(d.sh, d.ls, 'Google search | 20 | 15 | 75% | ▼ 25%', 5).setFontColor === '#b91c1c' &&
         fmtOf(d.sh, d.ls, 'LinkedIn | 10 | 6 | 60% | ▲ 200%', 5).setFontColor === '#15803d');
      const d2 = block(d.ls, 'Top landing pages');
      ok('j. D2: landing pages by engaged sessions, this week only',
         same(d2, ['Landing page | Engaged sessions | Sessions', '/ | 18 | 32', '/games/a/ | 9 | 13', '/games/b/ | 4 | 5', '/games/c/ | 1 | 2']), JSON.stringify(d2));
      ok('j. E: the UK share of engaged sessions', same(block(d.ls, 'Who uses it?'), ['UK share of engaged sessions | 69% | 50 of 72']),
         JSON.stringify(block(d.ls, 'Who uses it?')));
      const e5 = block(d.ls, 'Top 5 countries'), dv = block(d.ls, 'Devices');
      ok('j. E: top 5 countries and the device split, by engaged sessions',
         same(e5, ['Country | Engaged sessions | Share', 'United Kingdom | 50 | 69%', 'United States | 10 | 14%', 'India | 6 | 8%',
           'Ireland | 3 | 4%', 'Germany | 2 | 3%']) &&
         same(dv, ['Device | Engaged sessions | Share', 'mobile | 8 | 25%', 'desktop | 22 | 69%', 'tablet | 2 | 6%']), JSON.stringify([e5, dv]));
      ok('j. A: engaged sessions summed from GA4 country daily, 72 against 40',
         same((block(d.ls, 'Is it growing?') || []).slice(1), ['0 | 0 | n/a | 0 | 72', '▬ 0% | ▬ 0% | n/a | ▬ 0% | ▲ 80%']), JSON.stringify(block(d.ls, 'Is it growing?')));

      // ---- F and G. Launches: 13 days ago in, 15 days ago out, exactly 14 in, a future date out.
      const launch = { 'quiz-new': '2026-10-22', 'old-game': '2026-10-20', 'gamma': '2026-10-25', 'trig-wars': '2026-11-01',
        'edge-game': '2026-10-21', 'future-game': '2026-11-20' };
      const rf = [];
      ['2026-10-21', '2026-10-23', '2026-10-30', W].forEach(day => rf.push(ev(at(day, '10:00'), 'game_started', 'quiz-new')));   // 21 Oct is before its launch
      [true, true, true, false, ''].forEach(c => rf.push(ev(at(W, '10:05'), 'question_answered', 'quiz-new', { [COR]: c })));
      rf.push(ev(at(W, '10:30'), 'game_completed', 'quiz-new'), ev(at(W, '10:31'), 'game_completed', 'quiz-new'));
      rf.push(ev(at(W, '10:00'), 'game_started', 'old-game'));
      for (let i = 0; i < 4; i++) rf.push(ev(at(W, String(10 + i) + ':00'), 'game_started', 'escape-gamma'));
      rf.push(ev(at(W, '11:00'), 'game_completed', 'escape-gamma', { [QA]: 3, [QC]: 3, [DET]: 'escaped wrongs:0 hints:1 used:600 played:580 locks:100,250,400' }));
      rf.push(ev(at(W, '12:00'), 'game_completed', 'escape-gamma', { [QA]: 3, [QC]: 2, [DET]: 'timeout wrongs:2 hints:0 used:900 played:900 locks:300,-,120' }));
      for (let i = 0; i < 6; i++) rf.push(ev(at(W, '11:30'), 'question_answered', 'escape-gamma', { [COR]: i < 2 }));
      for (let i = 0; i < 2; i++) rf.push(ev(at(W, String(14 + i) + ':00'), 'game_started', 'trig-wars'));
      for (let i = 0; i < 3; i++) rf.push(ev(at(W, '14:05'), 'question_answered', 'trig-wars', { [COR]: true }));
      rf.push(ev(at(W, '14:30'), 'game_completed', 'trig-wars'));
      ['lock-a:1', 'lock-a:2', 'lock-b:1'].forEach(x => rf.push(ev(at(W, '11:10'), 'hint_used', 'escape-gamma', { [DET]: x })));
      rf.push(ev(at(W, '11:10'), 'hint_used', 'escape-delta', { [DET]: 'lock-z:1' }));
      d = runDash(rf, { launch });
      const f = block(d.ls, 'New games');
      ok('j. F: launched 13 and 14 days ago in, 15 days ago out; rooms by escapes, shot games "–", newest first',
         same(f, ['Game | Launched | Starts | Questions answered | % correct | Completed', 'trig-wars | 2026-11-01 | 2 | – | – | 1',
           'gamma | 2026-10-25 | 4 | – | 1 escaped (25%) | 2', 'quiz-new | 2026-10-22 | 3 | 5 | 75% | 2', 'edge-game | 2026-10-21 | 0 | 0 | n/a | 0']),
         JSON.stringify(f));
      const gh = block(d.ls, 'Hints by lock');
      ok('j. G: hints by room and lock (the lock id before ":"), most first',
         same(gh, ['Room | Lock | Hints', 'escape-gamma | lock-a | 2', 'escape-delta | lock-z | 1', 'escape-gamma | lock-b | 1']), JSON.stringify(gh));
      const gt = block(d.ls, 'Time per lock');
      ok('j. G: time per lock from "locks:" (seconds since the previous lock opened), averaged over the runs that opened it',
         same(gt, ['Room | Lock | Runs that opened it | Average time', 'escape-gamma | lock 1 | 2 | 2 min 20 s', 'escape-gamma | lock 2 | 1 | 2 min 30 s',
           'escape-gamma | lock 3 | 2 | 2 min 15 s']), JSON.stringify(gt));
      ok('j. G: Table 4b first, then hints and time per lock; the older tables follow and Daily Activity is last',
         ['Escape Rooms — Last 7 Days', 'Hints by lock', 'Time per lock', 'Misunderstood Maths', 'Top Games — Last 7 Days', 'Accuracy by Game',
           'Hardest Questions', 'Level Breakdown', 'Daily Activity — Last 30 Days'].map(t => d.ls.findIndex(l => l.indexOf(t) === 0))
           .every((v, i, a) => v > 0 && (i === 0 || v > a[i - 1])), d.ls.join(' / '));
      d = runDash(rf, { launch: 'fail' });
      ok('j. F: a failed launch-dates fetch gives the line and the Dashboard carries on',
         same(block(d.ls, 'New games'), ['Launch dates could not be read today.']) && d.ls.indexOf('Daily Activity — Last 30 Days') > 0,
         JSON.stringify(block(d.ls, 'New games')));
    }
  } catch (e) {
    ok('the harness ran', false, e.stack || e);
  }
  return out;
}
"""

FIXTURE_GAMES = {"games": [{"slug": "alpha-q"}, {"slug": "beta-q", "answer_kind": "question"}, {"slug": "thirty-q"},
                           {"slug": "twentynine-q"}, {"slug": "delta-q"}, {"slug": "prisoners-dilemma"},
                           {"slug": "trig-wars", "answer_kind": "shot"}]}

PLANTS = [
    ("a room counted in accuracy", "  if (String(slug).indexOf('escape-') === 0) return 'room';\n", ""),
    ("a row with no question_id in hardest questions", "    if (!qid) return;\n", ""),
    ("a minimum below 30", "const RPT_MIN_GAME_ANSWERS = 30;", "const RPT_MIN_GAME_ANSWERS = 20;"),
    ("a pre-29-Sep blank ignored, not counted wrong",
     "  if (c === '' && new Date(x[col['timestamp']]) < RPT_BLANK_WAS_WRONG_UNTIL) return false;\n", ""),
    ("every room game_completed counted as escaped",
     "{ if (rptEscaped(x, col)) rm.escaped++; else rm.timedOut++; }", "rm.escaped++;"),
    ("doPost leaves detail out of the row", "      cellValue(data.question_id), cellValue(data.detail)\n",
     "      cellValue(data.question_id)\n"),
    ("doPost writes detail before question_id", "      cellValue(data.question_id), cellValue(data.detail)\n",
     "      cellValue(data.detail), cellValue(data.question_id)\n"),
    ("cellValue writes a posted formula as it came", "))) return \"'\" + v;\n", "))) return v;\n"),
    ("the Dashboard writes a posted slug without cellValue", "setValues([[slug, gc[slug], comp, frac].map(cellValue)]);",
     "setValues([[slug, gc[slug], comp, frac]]);"),
    ("Daily Activity counts room answers", "dayKinds) === 'question') rptAdd(dailyAnswers, day);",
     "dayKinds) !== 'shot') rptAdd(dailyAnswers, day);"),
    ("Daily Activity counts shot answers", "dayKinds) === 'question') rptAdd(dailyAnswers, day);",
     "dayKinds) !== 'room') rptAdd(dailyAnswers, day);"),
    ("Daily Activity drops a day with no starts", "  var days = Object.keys(dailyStarts).concat(",
     "  var days = Object.keys(dailyStarts).sort(); var unused = [].concat("),
    ("check-these: the 10% threshold made <=", "q.correct / q.total < RPT_CHECK_PCT;", "q.correct / q.total <= RPT_CHECK_PCT;"),
    ("a class: the gap made 60 minutes", "const RPT_CLASS_GAP_MIN = 30;", "const RPT_CLASS_GAP_MIN = 60;"),
    ("the headline's % correct coloured green or red", "RPT_GREY /* % correct: neutral whichever way it moves */",
     "rptDirColour(ch[2].dir)"),
    ("lnkd.in falling into Other", "const RPT_CH_LINKEDIN = ['linkedin', 'lnkd'];", "const RPT_CH_LINKEDIN = ['linkedin'];"),
    ("a missing GA4 tab throwing", "  if (!tab) return null;\n  var v = tab.getDataRange", "  if (!tab) throw new Error('no GA4 tab ' + name);\n  var v = tab.getDataRange"),
    ("a room counted in check-these", "    if (rptKind(slug, kinds) !== 'question') return;   // B1: question games only, never a room's lock\n",
     "    if (rptKind(slug, kinds) === 'shot') return;   // B1\n"),
    ("Daily Activity's curveType back", "      .setNumHeaders(1)\n", "      .setNumHeaders(1)\n      .setOption('curveType', 'function')\n"),
    # Kept last. The tally maps given a prototype again: a "__proto__" slug is then lost from every tally (section g).
    ("the report's tally maps have a prototype", "function rptMap() { return Object.create(null); }",
     "function rptMap() { return {}; }"),
]


def run(page, src):
    return page.evaluate(HARNESS, [src, FIXTURE_GAMES])


def real_games_json():
    """The real data/games.json: every answer_kind is "question" or "shot"."""
    games = json.loads(GAMES.read_text(encoding="utf-8"))["games"]
    bad = [(g["slug"], g["answer_kind"]) for g in games if "answer_kind" in g and g["answer_kind"] not in ("question", "shot")]
    shots = [g["slug"] for g in games if g.get("answer_kind") == "shot"]
    return bad, shots


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    src = SRC.read_text(encoding="utf-8")
    failed = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_context(timezone_id="Europe/London").new_page()
        results = run(page, src)
        samples = {name: detail for name, _, detail in results if name.startswith("__sample")}
        for name, good, detail in results:
            if name.startswith("__sample"):
                continue
            failed += not good
            print("  %s  %s%s" % ("PASS" if good else "FAIL", name, "" if good else "  <- " + detail[:600]))
        bad, shots = real_games_json()
        failed += bool(bad)
        print("  %s  data/games.json: answer_kind is only \"question\" or \"shot\"%s (shot: %s)"
              % ("FAIL" if bad else "PASS", "  <- %s" % bad if bad else "", ", ".join(shots) or "none"))
        for what, old, new in PLANTS:
            try:
                planted = pc.apply_plant(src, old, new, what)
            except pc.StalePlant as e:
                failed += 1
                print("  FAIL  plant: %s" % e)
                continue
            fails = [n for n, good, _ in run(page, planted) if not good and not n.startswith("__")]
            caught = pc.is_caught(fails)
            failed += not caught
            print("  %s  plant: %s%s" % ("CAUGHT" if caught else "MISSED", what, " (" + "; ".join(fails) + ")" if fails else ""))
        browser.close()
    if "--sample" in sys.argv:
        print("\n----- sample email (answer sections) -----\n" + samples.get("__sample_email", ""))
        print("----- sample Dashboard (cells by row) -----\n" + samples.get("__sample_dash", ""))
    print("analytics report: %s" % ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
