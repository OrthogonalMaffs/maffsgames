// Emulator tests for firebase/database.rules.json (30 Sep 2026).
//
// Run from this folder (needs Java for the emulator, and `npm install` here first):
//     npx firebase emulators:exec --only database --project demo-maffsgames "node rules.test.mjs"
//
// Every case is a real request against the Realtime Database emulator loaded with the
// rules file, made the way the site makes it: unauthenticated, through the same
// compat SDK the pages use. A case that behaves otherwise prints FAIL and the run exits 1.
import { readFileSync } from 'node:fs';
import { initializeTestEnvironment, assertSucceeds, assertFails } from '@firebase/rules-unit-testing';

const env = await initializeTestEnvironment({
  projectId: 'demo-maffsgames',
  database: { rules: readFileSync(new URL('./database.rules.json', import.meta.url), 'utf8'),
              host: '127.0.0.1', port: 9000 },
});

// Seed an existing score of each kind, with the rules off (as the live data already is).
await env.withSecurityRulesDisabled(async ctx => {
  const db = ctx.database();
  await db.ref('leaderboards/factor_race_gcse/existing').set({ score: 500, timestamp: Date.now(), initials: 'ABC' });
  await db.ref('recent_scores/existing').set({ game: 'Factor Race', slug: 'factor-race', level: 'GCSE',
    levelKey: 'gcse', score: 500, timestamp: Date.now(), initials: 'ABC' });
  for (let i = 0; i < 30; i++) {
    await db.ref('recent_scores').push({ game: 'Factor Race', slug: 'factor-race', level: 'GCSE',
      levelKey: 'gcse', score: i, timestamp: Date.now() - (30 - i) * 1000 });
  }
});

const db = env.unauthenticatedContext().database();
const now = () => Date.now();
const board = (b = 'factor_race_gcse') => db.ref('leaderboards/' + b);
const recent = () => db.ref('recent_scores');
const goodBoard = (extra = {}) => ({ score: 640, timestamp: now(), initials: 'JLF', ...extra });
const goodRecent = (extra = {}) => ({ game: 'Free Daily Pizza', slug: 'free-daily-pizza', level: 'Daily pizza 1 Oct',
  levelKey: 'daily-2026-10-01', score: 640, timestamp: now(), initials: 'JLF', ...extra });

const cases = [
  // ---- accepted: what submitScore() writes
  ['ACCEPT new board score (initials)', 'ok', () => board().push(goodBoard())],
  ['ACCEPT new board score (Skip: no initials)', 'ok', () => board().push({ score: 12.5, timestamp: now() })],
  ['ACCEPT new board score on a daily board', 'ok', () => board('free_daily_pizza_daily_2026_10_01').push(goodBoard())],
  ['ACCEPT new ticker entry', 'ok', () => recent().push(goodRecent())],
  ['ACCEPT new ticker entry, level "all" (empty label)', 'ok', () => recent().push(goodRecent({ level: '', levelKey: 'all' }))],
  // ---- refused: overwrite, update, delete
  ['REFUSE overwrite of an existing board score', 'fail', () => board().child('existing').set(goodBoard({ score: 99999 }))],
  ['REFUSE update of an existing board score', 'fail', () => board().child('existing').update({ score: 99999 })],
  ['REFUSE delete of a board score', 'fail', () => board().child('existing').remove()],
  ['REFUSE delete of a whole board', 'fail', () => board().remove()],
  ['REFUSE delete of all leaderboards', 'fail', () => db.ref('leaderboards').remove()],
  ['REFUSE overwrite of a ticker entry', 'fail', () => recent().child('existing').set(goodRecent())],
  ['REFUSE delete of a ticker entry', 'fail', () => recent().child('existing').remove()],
  ['REFUSE delete of the whole ticker', 'fail', () => recent().remove()],
  // ---- refused: bad shape
  ['REFUSE score as a string', 'fail', () => board().push(goodBoard({ score: '640' }))],
  ['REFUSE missing timestamp', 'fail', () => board().push({ score: 640 })],
  ['REFUSE missing score', 'fail', () => board().push({ timestamp: now() })],
  ['REFUSE unexpected child', 'fail', () => board().push(goodBoard({ admin: true }))],
  ['REFUSE lower-case initials', 'fail', () => board().push(goodBoard({ initials: 'jlf' }))],
  ['REFUSE four-letter initials', 'fail', () => board().push(goodBoard({ initials: 'ABCD' }))],
  ['REFUSE initials with a digit', 'fail', () => board().push(goodBoard({ initials: 'A1' }))],
  ['REFUSE ticker entry missing levelKey', 'fail', () => { const e = goodRecent(); delete e.levelKey; return recent().push(e); }],
  ['REFUSE ticker slug with capitals', 'fail', () => recent().push(goodRecent({ slug: 'Free-Daily-Pizza' }))],
  ['REFUSE ticker game name of 200 characters', 'fail', () => recent().push(goodRecent({ game: 'x'.repeat(200) }))],
  ['REFUSE ticker unexpected child', 'fail', () => recent().push(goodRecent({ highScore: true }))],
  ['REFUSE board key with capitals', 'fail', () => board('Factor_Race').push(goodBoard())],
  ['REFUSE write outside leaderboards/recent_scores', 'fail', () => db.ref('anything/else').set({ a: 1 })],
  // ---- refused: timestamps
  ['REFUSE far-future timestamp (+1 day)', 'fail', () => board().push(goodBoard({ timestamp: now() + 86400000 }))],
  ['REFUSE stale timestamp (-5 min)', 'fail', () => board().push(goodBoard({ timestamp: now() - 300000 }))],
  ['REFUSE far-future ticker timestamp', 'fail', () => recent().push(goodRecent({ timestamp: now() + 86400000 }))],
  // ---- reads, as the hub, standing() and the ticker make them
  ['READ one board (hub, standing())', 'ok', () => board().once('value')],
  ['READ ticker: orderByChild(timestamp).limitToLast(20)', 'ok',
    async () => { const s = await recent().orderByChild('timestamp').limitToLast(20).once('value');
                  if (s.numChildren() !== 20) throw new Error('got ' + s.numChildren() + ' entries'); }],
  ['REFUSE read of the database root', 'fail', () => db.ref('/').once('value')],
];

let bad = 0;
for (const [name, want, fn] of cases) {
  try {
    await (want === 'ok' ? assertSucceeds(fn()) : assertFails(fn()));
    console.log('PASS  ' + name);
  } catch (e) {
    bad++;
    console.log('FAIL  ' + name + '  (' + String(e.message || e).split('\n')[0] + ')');
  }
}
await env.cleanup();
console.log(`\n${bad ? 'FAILED' : 'ALL PASS'}: ${cases.length - bad} of ${cases.length} cases behaved as the rules intend`);
process.exit(bad ? 1 : 0);
