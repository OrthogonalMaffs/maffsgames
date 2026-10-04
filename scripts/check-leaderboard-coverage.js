#!/usr/bin/env node
/**
 * Coverage check: every live game must call MaffsLeaderboard.submitScore(),
 * except games explicitly excluded below (non-scored / exploratory format).
 *
 * It also reports games whose call is present but deliberately gated off, and
 * fails if a gate exists that nothing here declares. A leaderboard that quietly
 * drops scores is the bug this project has already fixed once: the old
 * ten-question gate rejected thirteen games in silence for months.
 *
 * It also checks the leaderboard hub's registry (the GAMES array in
 * leaderboards/index.html): every game that calls submitScore() must be listed
 * there, with exactly the levels it submits under. A game missing from the
 * registry ranks on boards nobody can open from the hub; a level the registry
 * does not list is a board the hub never shows. Both happened: on 30 Sep 2026
 * the audit that added this check found linear-equation-solver and
 * distinctly-average absent, and three games (quadratic-factoriser,
 * chart-interrogator, binomial-blaster) submitting under level keys the
 * registry did not list.
 *
 * It also checks that every level a game submits has a name. It loads
 * schools/assets/firebase-leaderboard.js (it runs without Firebase) and asks
 * MaffsLeaderboard.levelLabel(), the single source for naming a level, to name
 * each one. A level with no name is shown on the portal ticker as its raw key;
 * on 30 Sep 2026 six submitted keys had none (q20, q40, higher, formula,
 * alevel2, l4).
 *
 * It also checks every key a game writes to score history
 * (MaffsScoreHistory.record()), which the leaderboard hub's "Your Scores" panel
 * names with the same levelLabel(). A game that records under the level it
 * submits is already covered above; any other history key must be declared in
 * HISTORY_ONLY_KEYS and be nameable. On 30 Sep 2026 Free Daily Pizza's
 * single-stage keys (stage-s1-q20 ...) were recorded, never submitted, and so
 * never checked: "Your Scores" showed them raw.
 *
 * Run: node scripts/check-leaderboard-coverage.js
 * Exit code 1 if any live game is missing the call, if a gate is undeclared,
 * if the hub registry and the games disagree, or if a submitted or history
 * level has no name.
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
const GAMES_DIR = path.join(ROOT, 'games');
const HUB_PATH = path.join(ROOT, 'leaderboards', 'index.html');
const LEADERBOARD_JS = path.join(ROOT, 'schools', 'assets', 'firebase-leaderboard.js');
const ROSTER_PATH = path.join(ROOT, '.claude', 'rules', 'game-roster.md');

// Games deliberately excluded — no numeric score to submit.
// Keep this list in sync with docs/canon.md §9 "Coverage".
const EXCLUDED = ['constructions-lab', 'given-that'];

// Games that DO have a score and DO call submitScore(), but whose call is gated
// off at the call site. Two are lower-is-better and the boards rank high score
// first, so publishing would rank them backwards; log-laws holds only its Solve
// mode, whose scores would otherwise mix into the Laws drill's board;
// distinctly-average offers 10/20/30-question sessions that would otherwise
// share one board (session length becomes a mode). Each gate
// lifts when scoring modes land — docs/next-contract-leaderboard-modes.md,
// to-do item 0. Not the same thing as EXCLUDED. Keep in sync with docs/canon.md §9.
const HELD = {
  'estimation-golf': 'lower-is-better (stroke total)',
  'equatle': 'lower-is-better (guesses used)',
  'log-laws': 'Solve mode only; the Laws drill still submits (modes would mix on one board)',
  'distinctly-average': '10, 20 and 30-question sessions would rank together on one board per level (session length is not part of the board key)'
};
const HELD_FLAG = 'LEADERBOARD_MODE_READY';

// Games withdrawn behind a noindex holding page while they are rebuilt (canon §11.5): the URL
// stays, the full game is kept as _withdrawn.html, and its boards and hub row are kept (the
// row's name says "being rebuilt"). The declaration is checked, not trusted: index.html must be
// a noindex page that submits nothing, _withdrawn.html must exist and still call submitScore(),
// and a declared game that submits from index.html again is a stale declaration.
const WITHDRAWN = {
  'regression-rumble': 'data rebuild, 30 Sep 2026: 37 of 40 scenarios failed their verifier (todo §1.26)'
};
const withdrawnProblems = [];
for (const slug of Object.keys(WITHDRAWN)) {
  const idx = path.join(GAMES_DIR, slug, 'index.html');
  const kept = path.join(GAMES_DIR, slug, '_withdrawn.html');
  const html = fs.existsSync(idx) ? fs.readFileSync(idx, 'utf8') : '';
  if (!/<meta name="robots" content="noindex/.test(html)) withdrawnProblems.push(`${slug}: declared WITHDRAWN but index.html is not a noindex holding page`);
  if (html.includes('MaffsLeaderboard.submitScore(')) withdrawnProblems.push(`${slug}: declared WITHDRAWN but index.html submits scores (stale: drop it from WITHDRAWN)`);
  if (!fs.existsSync(kept) || !fs.readFileSync(kept, 'utf8').includes('MaffsLeaderboard.submitScore(')) {
    withdrawnProblems.push(`${slug}: declared WITHDRAWN but the full game is not kept as _withdrawn.html`);
  }
}

const gameDirs = fs.readdirSync(GAMES_DIR, { withFileTypes: true })
  .filter(d => d.isDirectory())
  .map(d => d.name)
  .sort();

const missing = [];
const heldWithoutGate = [];
const gatedButUndeclared = [];

for (const slug of gameDirs) {
  if (EXCLUDED.includes(slug) || WITHDRAWN[slug]) continue;

  const indexPath = path.join(GAMES_DIR, slug, 'index.html');
  if (!fs.existsSync(indexPath)) continue;

  const html = fs.readFileSync(indexPath, 'utf8');
  if (!html.includes('MaffsLeaderboard.submitScore(')) {
    missing.push(slug);
    continue;
  }

  const hasGate = html.includes(HELD_FLAG);
  if (HELD[slug] && !hasGate) heldWithoutGate.push(slug);
  if (hasGate && !HELD[slug]) gatedButUndeclared.push(slug);
}

const heldCount = Object.keys(HELD).length;
console.log(`Checked ${gameDirs.length} game directories (${EXCLUDED.length} excluded, ${heldCount} held, ${Object.keys(WITHDRAWN).length} withdrawn).`);

let failed = false;

if (withdrawnProblems.length) {
  console.log(`\nWithdrawn games (WITHDRAWN) not withdrawn as declared, in ${withdrawnProblems.length} place(s):`);
  withdrawnProblems.forEach(p => console.log('  - ' + p));
  failed = true;
}

if (missing.length) {
  console.log(`\nMissing MaffsLeaderboard.submitScore() call in ${missing.length} game(s):`);
  missing.forEach(slug => console.log(`  - ${slug}`));
  console.log('\nEither add the submitScore() call (see games/factor-race/index.html for the reference pattern),');
  console.log('or add the slug to EXCLUDED in this script if it is a deliberate non-scored format.');
  failed = true;
}

if (heldWithoutGate.length) {
  console.log(`\nDeclared HELD but no ${HELD_FLAG} gate found in ${heldWithoutGate.length} game(s):`);
  heldWithoutGate.forEach(slug => console.log(`  - ${slug}`));
  console.log('\nEither the gate was removed (drop the slug from HELD — the game now ranks),');
  console.log('or it was never added and the game is publishing backwards right now.');
  failed = true;
}

if (gatedButUndeclared.length) {
  console.log(`\nFound a ${HELD_FLAG} gate that HELD does not declare, in ${gatedButUndeclared.length} game(s):`);
  gatedButUndeclared.forEach(slug => console.log(`  - ${slug}`));
  console.log('\nA game that silently submits nothing is the failure mode this check exists to prevent.');
  console.log('Add it to HELD with a reason, or remove the gate.');
  failed = true;
}

// ---------------------------------------------------------------------------
// Hub registry: every submitting game listed, with exactly the levels it submits.
// ---------------------------------------------------------------------------

// Games that submit but are deliberately not on the hub.
const NOT_ON_HUB = {
  'the-perfect-prank': 'unlisted escape-room prototype, never on the portal (canon §4)',
  // Jon's contract, 4 Oct 2026: unlisted (noindex, off the portal, /resit/, sitemap, spec map,
  // /updates/) until he has played it. It submits to 'ks3' as built; the hub row is added with the
  // listing, and this entry removed in the same PR.
  'just-pythag-it-bruv': 'unlisted until Jon approves it (todo START); hub row added at listing'
};

// The levels a game submits under are read from its source: the level argument of
// every submitScore() call if they are all string literals, otherwise the roster's
// levels for the game (the hub registry's own documented rule). Where the level is
// a variable whose values are NOT the roster's tier keys, the true set was read from
// the game by hand and is declared here, with where it comes from. An override that
// the default rule would already produce is stale and fails the check.
const LEVEL_OVERRIDES = {
  'six-sevens-bruv':      [['q20', 'q40'], "board = 'q' + session length; clear-the-grid submits nothing (Jon, 30 Sep 2026)"],
  'free-daily-pizza':     [['practice-q20', 'practice-q40'], "FDP.boardFor(): mixed practice is 'practice-q' + session length (single-stage practice submits nothing); the daily pizza's keys are in OFF_HUB_LEVEL_PATTERNS"],
  'quadratic-factoriser': [['gcse', 'higher', 'formula'], 'IMPLEMENTED_LEVELS'],
  'chart-interrogator':   [['gcse', 'alevel', 'core', 'l4'], "selectedLevel = the level button's data-level; the L4 button says 'l4'"],
  'the-perfect-prank':    [['ks3'], "const LEVEL='ks3'; no roster row (unlisted prototype), so the default rule finds nothing"]
};

// Level keys a game submits that follow a pattern rather than a fixed list, and that the hub
// deliberately does not list (one board per UK day would be a new hub row every day). They are
// not compared with the registry; a sample key is still checked against levelLabel(), so the
// ticker can always name them. [pattern, sample key, why]
const OFF_HUB_LEVEL_PATTERNS = {
  'free-daily-pizza': [/^daily-\d{4}-\d{2}-\d{2}$/, 'daily-2026-10-01',
    "the daily pizza: one board per UK day, submitted as 'daily-YYYY-MM-DD'; not on the hub (Jon, 30 Sep 2026)"]
};

// Keys a game writes to score history (MaffsScoreHistory.record) that it never submits to a
// board, so the submitted-level checks never see them. "Your Scores" on the leaderboard hub names
// them with levelLabel(). [sample keys, pattern every key follows, why]; each sample must match
// the pattern and be named.
const HISTORY_ONLY_KEYS = {
  'free-daily-pizza': [['stage-s1-q20', 'stage-s1-q40', 'stage-s4-q20', 'stage-s4-q40', 'stage-s2-q3'],
    /^stage-s\d+-q\d+$/,
    "histKey = board || FDP.modeFor(): single-stage practice ranks nowhere, so history and personal best " +
    "go under 'stage-s' + stage + '-q' + questions played (a missed-questions replay can be any length)"]
};

// The roster's level labels -> level keys. One table, shared with check-site.py and
// extract-banks.py (through scripts/bank_common.py): scripts/roster-levels.json. It is
// JSON because this script cannot import Python. Do not keep a copy here.
const ROSTER_LEVEL_KEYS = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'roster-levels.json'), 'utf8')).labels;

function readRoster() {
  const out = {};
  for (const line of fs.readFileSync(ROSTER_PATH, 'utf8').split('\n')) {
    const cells = line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
    if (cells.length < 4 || !/^\d+$/.test(cells[0])) continue;
    const m = /^`([a-z0-9-]+)`$/.exec(cells[2]);
    if (!m) continue;
    // An unlisted label is an error, as in bank_common.roster_levels(); it is never dropped.
    out[m[1]] = cells[3].split(',').map(p => {
      const key = ROSTER_LEVEL_KEYS[p.trim().toLowerCase()];
      if (!key) throw new Error(`${m[1]}: roster level '${p.trim()}' is not in scripts/roster-levels.json`);
      return key;
    });
  }
  return out;
}

// One registry row per line: ['slug','Name',['lvl',...]],  (the name may be "double-quoted").
function readRegistry() {
  const html = fs.readFileSync(HUB_PATH, 'utf8');
  const start = html.indexOf('var GAMES = [');
  if (start < 0) return null;
  const end = html.indexOf('\n]', start);   // the array closes with "].map(...)"
  const out = {}, names = {};
  const row = /^\s*\[\s*'([a-z0-9-]+)'\s*,\s*('(?:[^'\\]|\\.)*'|"[^"]*")\s*,\s*\[([^\]]*)\]\s*\],?\s*$/;
  const bad = [];
  for (const line of html.slice(start, end).split('\n').slice(1)) {
    if (!line.trim() || /^\s*\/\//.test(line)) continue;
    const m = row.exec(line);
    if (!m) { bad.push(line.trim()); continue; }
    if (out[m[1]]) bad.push('duplicate row for ' + m[1]);
    names[m[1]] = m[2].slice(1, -1);
    out[m[1]] = m[3].split(',').map(x => x.trim().replace(/^'|'$/g, '')).filter(Boolean);
  }
  return { levels: out, names: names, bad: bad };
}

function submittedLevels(slug, html, roster) {
  const calls = [];
  const re = /MaffsLeaderboard\.submitScore\(\s*[^,]+,\s*([^,]+),/g;
  let m;
  while ((m = re.exec(html))) calls.push(m[1].trim());
  const literals = calls.filter(a => /^'[^']*'$|^"[^"]*"$/.test(a)).map(a => a.slice(1, -1));
  if (literals.length === calls.length) return [...new Set(literals)].sort();
  return [...new Set((roster[slug] || []).concat(literals))].sort();
}

const registry = readRegistry();
const roster = readRoster();
const hubProblems = [];
const submittedBySlug = {};   // slug -> the levels it submits under, for the naming check
if (!registry) {
  hubProblems.push('could not find "var GAMES = [" in leaderboards/index.html');
} else {
  registry.bad.forEach(l => hubProblems.push('unreadable registry row: ' + l));
  const submitting = new Set();
  for (const slug of gameDirs) {
    const indexPath = path.join(GAMES_DIR, slug, 'index.html');
    if (!fs.existsSync(indexPath)) continue;
    const html = fs.readFileSync(indexPath, 'utf8');
    if (!html.includes('MaffsLeaderboard.submitScore(')) continue;
    submitting.add(slug);
    const derived = submittedLevels(slug, html, roster);
    let want = derived;
    if (LEVEL_OVERRIDES[slug]) {
      want = [...LEVEL_OVERRIDES[slug][0]].sort();
      if (want.join() === derived.join()) hubProblems.push(`${slug}: LEVEL_OVERRIDES entry is stale (the default rule already gives ${derived.join(', ')})`);
    }
    submittedBySlug[slug] = want;
    if (NOT_ON_HUB[slug]) continue;
    const have = registry.levels[slug];
    if (!have) { hubProblems.push(`${slug}: calls submitScore() but is not in the hub registry (submits under: ${want.join(', ')})`); continue; }
    const got = [...new Set(have)].sort();
    if (got.join() !== want.join()) hubProblems.push(`${slug}: hub registry lists [${got.join(', ')}], but the game submits under [${want.join(', ')}]`);
  }
  for (const slug of Object.keys(registry.levels)) {
    if (WITHDRAWN[slug]) {
      if (!/being rebuilt/.test(registry.names[slug] || '')) hubProblems.push(`${slug}: WITHDRAWN, but its hub row does not say it is being rebuilt`);
      continue;
    }
    if (!submitting.has(slug)) hubProblems.push(`${slug}: in the hub registry but no game of that name calls submitScore()`);
  }
  for (const slug of Object.keys(LEVEL_OVERRIDES)) {
    if (!submitting.has(slug)) hubProblems.push(`${slug}: LEVEL_OVERRIDES names a game that does not submit`);
  }
  for (const slug of Object.keys(OFF_HUB_LEVEL_PATTERNS)) {
    if (!submitting.has(slug)) hubProblems.push(`${slug}: OFF_HUB_LEVEL_PATTERNS names a game that does not submit`);
  }
  for (const slug of Object.keys(NOT_ON_HUB)) {
    if (registry.levels[slug]) hubProblems.push(`${slug}: declared NOT_ON_HUB but listed in the registry`);
  }
}

// ---------------------------------------------------------------------------
// Score-history keys: every key a game records under, for the naming check below.
// ---------------------------------------------------------------------------
// A record() whose level argument is a string literal records under that key. One whose argument
// is the same expression a submitScore() call in the game uses records under the game's submitted
// levels, already named above. Anything else records under keys this script cannot read, so they
// must be declared in HISTORY_ONLY_KEYS.
function levelArgs(html, re) {
  const out = [];
  let m;
  while ((m = re.exec(html))) out.push(m[1].trim());
  return out;
}
const isLiteral = a => /^'[^']*'$|^"[^"]*"$/.test(a);
const historyBySlug = {};     // slug -> literal and declared history keys (the rest are submitted levels)
const historyProblems = [];
for (const slug of gameDirs) {
  const indexPath = path.join(GAMES_DIR, slug, 'index.html');
  if (!fs.existsSync(indexPath)) continue;
  const html = fs.readFileSync(indexPath, 'utf8');
  const rec = levelArgs(html, /MaffsScoreHistory\.record\(\s*[^,]+,\s*([^,]+),/g);
  if (!rec.length) continue;
  const sub = new Set(levelArgs(html, /MaffsLeaderboard\.submitScore\(\s*[^,]+,\s*([^,]+),/g));
  const keys = new Set(rec.filter(isLiteral).map(a => a.slice(1, -1)));
  const unseen = [...new Set(rec.filter(a => !isLiteral(a) && !sub.has(a)))];
  const decl = HISTORY_ONLY_KEYS[slug];
  if (unseen.length && !decl) {
    historyProblems.push(`${slug}: records score history under ${unseen.join(', ')}, which is not a level it ` +
      'submits; declare the keys it can take in HISTORY_ONLY_KEYS');
  }
  if (decl && !unseen.length) historyProblems.push(`${slug}: HISTORY_ONLY_KEYS entry is stale (every history key is a submitted level or a literal)`);
  if (decl) {
    for (const k of decl[0]) {
      if (!decl[1].test(k)) historyProblems.push(`${slug}: HISTORY_ONLY_KEYS sample '${k}' does not match its own pattern`);
      keys.add(k);
    }
  }
  historyBySlug[slug] = [...keys].sort();
}
for (const slug of Object.keys(HISTORY_ONLY_KEYS)) {
  if (!historyBySlug[slug]) historyProblems.push(`${slug}: HISTORY_ONLY_KEYS names a game that records no score history`);
}

if (hubProblems.length) {
  console.log(`\nLeaderboard hub registry (leaderboards/index.html GAMES) disagrees with the games in ${hubProblems.length} place(s):`);
  hubProblems.forEach(p => console.log('  - ' + p));
  console.log('\nA board the registry does not list is one nobody can open from the hub. Fix the registry row,');
  console.log('or, if a game submits under keys that are not its roster tiers, declare them in LEVEL_OVERRIDES.');
  failed = true;
} else {
  console.log(`\nHub registry: ${Object.keys(registry.levels).length} games listed, each with exactly the levels it submits.`);
}

// ---------------------------------------------------------------------------
// Level names: levelLabel() must name every level a game submits.
// ---------------------------------------------------------------------------

const unnamed = [];
let levelLabel = null;
try {
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(LEADERBOARD_JS, 'utf8'), sandbox, { filename: LEADERBOARD_JS });
  levelLabel = sandbox.window.MaffsLeaderboard && sandbox.window.MaffsLeaderboard.levelLabel;
} catch (e) {
  unnamed.push('could not load firebase-leaderboard.js: ' + e.message);
}
if (!unnamed.length && typeof levelLabel !== 'function') {
  unnamed.push('firebase-leaderboard.js does not export MaffsLeaderboard.levelLabel()');
}
if (!unnamed.length) {
  for (const slug of Object.keys(submittedBySlug).sort()) {
    if (!submittedBySlug[slug].length) unnamed.push(`${slug}: calls submitScore() but its levels cannot be read; declare them in LEVEL_OVERRIDES`);
    const off = OFF_HUB_LEVEL_PATTERNS[slug];
    if (off && !off[0].test(off[1])) unnamed.push(`${slug}: OFF_HUB_LEVEL_PATTERNS sample '${off[1]}' does not match its own pattern`);
    if (off && levelLabel(off[1]) === null) unnamed.push(`${slug}: submits pattern keys like '${off[1]}', which levelLabel() cannot name`);
    for (const lv of submittedBySlug[slug]) {
      if (levelLabel(lv) === null) unnamed.push(`${slug}: submits level '${lv}', which levelLabel() cannot name`);
    }
  }
  historyProblems.forEach(p => unnamed.push(p));
  for (const slug of Object.keys(historyBySlug).sort()) {
    for (const lv of historyBySlug[slug]) {
      if (levelLabel(lv) === null) unnamed.push(`${slug}: records score history under '${lv}', which levelLabel() cannot name ("Your Scores" shows it raw)`);
    }
  }
}

if (unnamed.length) {
  console.log(`\nLevel names (schools/assets/firebase-leaderboard.js levelLabel()) missing in ${unnamed.length} place(s):`);
  unnamed.forEach(p => console.log('  - ' + p));
  console.log('\nThe ticker would show the raw key. Add the key to LEVEL_NAMES, or a pattern to');
  console.log('LEVEL_NAME_PATTERNS. Never extend the frozen legacy LEVEL_LABELS / LABEL_TO_LEVEL.');
  failed = true;
} else {
  const n = new Set([].concat(...Object.values(submittedBySlug))).size;
  const h = new Set([].concat(...Object.values(historyBySlug))).size;
  console.log(`\nLevel names: all ${n} submitted level keys, and ${h} literal or declared score-history keys, are named by levelLabel().`);
}

if (failed) process.exit(1);

if (heldCount) {
  console.log(`\nHeld back deliberately (call present, gate closed) — see docs/next-contract-leaderboard-modes.md:`);
  Object.keys(HELD).sort().forEach(slug => console.log(`  - ${slug}: ${HELD[slug]}`));
}

console.log('\nAll live games call MaffsLeaderboard.submitScore(). Coverage OK.');
