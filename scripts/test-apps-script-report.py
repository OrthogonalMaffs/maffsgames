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

  function load(fetchMode, eventsHead, dataRows) {
    const env = { fetches: 0, mails: [], cells: {}, sheets: {} };
    const UrlFetchApp = { fetch(url) {
      env.fetches++; env.url = url;
      if (fetchMode === 'throw') throw new Error('DNS error');
      if (fetchMode === '404') return { getResponseCode: () => 404, getContentText: () => 'Not Found' };
      return { getResponseCode: () => 200, getContentText: () => JSON.stringify(fixtureGames) };
    } };
    const chain = new Proxy({}, { get: (t, k) => k === 'build' ? () => ({}) : () => chain });
    function sheetFake(name, data) {
      const sh = { name, cells: {},
        clear() { sh.cells = {}; }, getCharts: () => [], removeChart() {}, insertChart() {}, setColumnWidth() {},
        setTabColor() {}, setFrozenRows() {}, newChart: () => chain,
        getDataRange: () => ({ getValues: () => data }),
        getLastRow: () => data.length,
        appendRow(r) { data.push(r); },
        getRange(r, c, nr, nc) {
          const rg = { setValue(v) { sh.cells[r + ',' + c] = v; return rg; },
            setValues(vs) { vs.forEach((line, i) => line.forEach((v, j) => sh.cells[(r + i) + ',' + (c + j)] = v)); return rg; },
            getValues: () => [data[r - 1].slice(c - 1, c - 1 + (nc || 1))] };
          ['setFontSize', 'setFontWeight', 'setFontStyle', 'setBackground', 'setNumberFormat'].forEach(m => rg[m] = () => rg);
          return rg;
        } };
      return sh;
    }
    const events = sheetFake('events', [eventsHead || HEAD].concat(eventsHead ? [] : (dataRows || rows)));
    env.events = events;
    const ss = { getActiveSheet: () => events, getSheetByName: n => env.sheets[n] || null,
      insertSheet: n => (env.sheets[n] = sheetFake(n, [])) };
    const DriveApp = { getFilesByName: () => ({ hasNext: () => true, next: () => ({}) }) };
    const SpreadsheetApp = { open: () => ss, create: () => ss };
    const MailApp = { sendEmail: (to, subject, body) => env.mails.push({ to, subject, body }) };
    const Utilities = { formatDate: (d, tz, f) => f === 'yyyy-MM-dd' ? d.toISOString().slice(0, 10) : d.toISOString().slice(0, 16) };
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
