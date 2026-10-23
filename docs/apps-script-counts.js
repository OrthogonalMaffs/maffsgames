// ============================================================
//  MaffsGames Answer Counts — a SEPARATE Google Apps Script project
// ============================================================
//
//  Counts question_answered rows in the analytics Sheet, per game_slug, for the current school
//  year (from 1 September, Europe/London), and serves the totals as JSON. It is its own project
//  so it can never compete with the analytics script's doPost for capacity: it only READS the
//  Sheet, and the analytics script does not know it exists.
//
//  SETUP: docs/apps-script-counts.md (click by click). Paste this file into Code.gs, set SHEET_ID,
//         and copy docs/apps-script-counts.appsscript.json over the project's appsscript.json.
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

const SHEET_ID = 'PASTE_THE_SHEET_ID_HERE';   // the long id in the Sheet's address: /spreadsheets/d/<ID>/edit
const SHEET_NAME = 'MaffsGames Events';
const TIMEZONE = 'Europe/London';
const COUNTED_EVENT = 'question_answered';
const CHUNK_ROWS = 5000;                      // rows read per call
const RUN_BUDGET_MS = 240000;                 // a trigger or backfill run stops reading after 4 minutes
const GET_BUDGET_MS = 20000;                  // a web request that has to update stops after 20 seconds
const CACHE_SECONDS = 60;
const MAX_SKEW_MS = 24 * 3600 * 1000;         // client_ts further than this from arrival is not trusted
const PROP_LIMIT = 8500;                      // script properties hold 9 KB a value

// Bump when this file is redeployed; <exec URL>?version=1 then says which code is live.
const SCRIPT_VERSION = '2026-10-23-a';

// ============================================================
//  GET — the figures, from a 60-second cache
// ============================================================
function doGet(e) {
  if (e && e.parameter && e.parameter.version) return json_(JSON.stringify({ version: SCRIPT_VERSION }));
  var cache = CacheService.getScriptCache();
  var hit = cache.get('payload');
  if (hit) return json_(hit);
  // Cache miss: catch up on any new rows first. If another run holds the lock, serve what is stored.
  try { updateCounts_(GET_BUDGET_MS, 3000); } catch (err) { console.error('doGet update failed: ' + err); }
  var body = JSON.stringify(payload_(loadState_(), new Date()));
  cache.put('payload', body, CACHE_SECONDS);
  return json_(body);
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
  console.log('counts cleared; run backfill()');
}

// Run by hand to see exactly what the web address will return, without the cache.
function preview() {
  console.log(JSON.stringify(payload_(loadState_(), new Date())));
}

// ============================================================
//  The incremental count
// ============================================================
function updateCounts_(budgetMs, lockWaitMs) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(lockWaitMs)) { console.log('another run holds the lock; skipped'); return; }
  var t0 = Date.now();
  try {
    var now = new Date();
    var sinceStr = sinceString_(now);
    var sinceDate = londonMidnight_(sinceStr);
    var sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    if (!sheet) throw new Error('no sheet named ' + SHEET_NAME);
    var cols = columns_(sheet);
    var lastRow = sheet.getLastRow();
    var st = loadState_();

    // A new school year, no stored state, or a Sheet that has shrunk (rows were deleted, so a stored row
    // number no longer points at the same rows): start the period again.
    if (st.since !== sinceStr || st.lastRow > lastRow) {
      st = { since: sinceStr, lastRow: startRow_(sheet, cols, sinceDate, lastRow) - 1, counts: {}, asOf: null };
      console.log('period start ' + sinceStr + ': reading from row ' + (st.lastRow + 1));
    }

    var rows = 0;
    while (st.lastRow < lastRow && Date.now() - t0 < budgetMs) {
      var from = st.lastRow + 1;
      var n = Math.min(CHUNK_ROWS, lastRow - from + 1);
      var vals = sheet.getRange(from, 1, n, cols.width).getValues();
      tally_(vals, cols, sinceDate, st.counts);
      st.lastRow = from + n - 1;
      rows += n;
      saveState_(st);
    }
    var caughtUp = st.lastRow >= lastRow;
    if (caughtUp) st.asOf = Utilities.formatDate(new Date(), TIMEZONE, "yyyy-MM-dd'T'HH:mm:ssXXX");
    saveState_(st);
    CacheService.getScriptCache().remove('payload');
    console.log('read ' + rows + ' rows in ' + (Date.now() - t0) + ' ms; last row ' + st.lastRow + ' of ' + lastRow +
                '; caught up: ' + caughtUp);
  } finally {
    lock.releaseLock();
  }
}

// Adds the counted rows of one chunk into `counts` (pure: no Sheet, no clock).
function tally_(vals, cols, sinceDate, counts) {
  for (var i = 0; i < vals.length; i++) {
    var r = vals[i];
    if (r[cols.event] !== COUNTED_EVENT) continue;
    var slug = String(r[cols.slug] || '').trim();
    if (!slug) continue;
    var t = eventTime_(r[cols.arrival], r[cols.clientTs]);
    if (!t || t < sinceDate) continue;
    counts[slug] = (counts[slug] || 0) + 1;
  }
}

// The browser's clock when it agrees with the arrival time to within a day, else the arrival time.
function eventTime_(arrival, clientTs) {
  var a = toDate_(arrival);
  var c = toDate_(clientTs);
  if (c && a && Math.abs(c - a) <= MAX_SKEW_MS) return c;
  return a;
}

function toDate_(v) {
  if (v === '' || v === null || v === undefined) return null;
  var d = (v instanceof Date) ? v : new Date(v);
  return isNaN(d.getTime()) ? null : d;
}

// The column positions, found by header name so a reordered Sheet cannot silently miscount.
function columns_(sheet) {
  var head = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var at = function (name) {
    var i = head.indexOf(name);
    if (i < 0) throw new Error('Sheet has no column ' + name);
    return i;
  };
  var c = { arrival: at('timestamp'), event: at('event'), slug: at('game_slug'), clientTs: at('client_ts') };
  c.width = Math.max(c.arrival, c.event, c.slug, c.clientTs) + 1;
  return c;
}

// First row to read for a period: the first row that arrived a day before the period began (rows arrive in
// order; the day's slack covers an event stamped before midnight that arrived after). Binary search, one cell
// per probe. An unreadable timestamp is treated as "before", so the search moves right past it.
function startRow_(sheet, cols, sinceDate, lastRow) {
  var cutoff = new Date(sinceDate.getTime() - MAX_SKEW_MS);
  var lo = 2, hi = lastRow + 1;               // answer is in [lo, hi]; hi means "none"
  while (lo < hi) {
    var mid = Math.floor((lo + hi) / 2);
    var t = toDate_(sheet.getRange(mid, cols.arrival + 1).getValue());
    if (t && t >= cutoff) hi = mid; else lo = mid + 1;
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
  return {
    since: p.since || '',
    lastRow: p.lastRow ? Number(p.lastRow) : 0,
    counts: p.counts ? JSON.parse(p.counts) : {},
    asOf: p.asOf || null
  };
}

function saveState_(st) {
  var counts = JSON.stringify(st.counts);
  if (counts.length > PROP_LIMIT) throw new Error('counts are ' + counts.length + ' characters; split them across properties');
  var p = { since: st.since, lastRow: String(st.lastRow), counts: counts };
  if (st.asOf) p.asOf = st.asOf;
  PropertiesService.getScriptProperties().setProperties(p, false);
  if (!st.asOf) PropertiesService.getScriptProperties().deleteProperty('asOf');
}

// {as_of, since, total, games}. as_of is null until a run has read every row (the first full count in progress),
// which the site treats as "not available": it shows nothing rather than a part-count.
function payload_(st, now) {
  var games = {};
  var total = 0;
  Object.keys(st.counts).sort().forEach(function (k) { games[k] = st.counts[k]; total += st.counts[k]; });
  return { as_of: st.asOf, since: st.since || sinceString_(now), total: total, games: games };
}
