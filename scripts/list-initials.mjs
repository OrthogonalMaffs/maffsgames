#!/usr/bin/env node
// One-off, READ ONLY (contract DOCS-BUNDLE, 9 Nov 2026): list every leaderboard entry whose initials are given on
// the command line (default JLF and SSF), from the public Firebase Realtime Database that
// schools/assets/firebase-leaderboard.js writes to.
//
//     node scripts/list-initials.mjs              # JLF and SSF
//     node scripts/list-initials.mjs ABC DEF      # any other initials
//
// Plain REST GETs of <databaseURL>/<path>.json: no key, no SDK, no dependencies, and nothing is ever written or
// deleted. The rules (firebase/database.rules.json) let anyone read recent_scores and each leaderboards/<board>, but
// not the root of leaderboards, so boards are read by name. Names are built as submitScore builds them,
// (slug + '_' + level) with hyphens to underscores, from every level and board a page declares to MaffsLevel.resolve
// (games/*/index.html, escape-rooms/*/index.html), plus every slug and levelKey seen in recent_scores. A board that
// matches only a boardPattern (one a day, for example) and never reached recent_scores cannot be named, so it is unseen.
// Prints a table (source, game, level, score, date, push id), the counts, and every read that failed.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = readFileSync(join(ROOT, 'schools', 'assets', 'firebase-leaderboard.js'), 'utf8');
const DB = (SRC.match(/databaseURL:\s*"([^"]+)"/) || [])[1];
if (!DB) { console.error('databaseURL not found in firebase-leaderboard.js'); process.exit(2); }
const WANT = new Set((process.argv.slice(2).length ? process.argv.slice(2) : ['JLF', 'SSF']).map(s => s.toUpperCase()));

const boardKey = (slug, level) => (slug + '_' + level).replace(/-/g, '_');
const strings = s => (s ? [...s.matchAll(/['"]([^'"]+)['"]/g)].map(m => m[1]) : []);

// slug -> Set of level/board keys, from each page's MaffsLevel.resolve({...}) declaration
const declared = new Map();
for (const dir of ['games', 'escape-rooms']) {
  for (const slug of readdirSync(join(ROOT, dir))) {
    const page = join(ROOT, dir, slug, 'index.html');
    if (!existsSync(page)) continue;
    for (const m of readFileSync(page, 'utf8').matchAll(/MaffsLevel\.resolve\(\s*\{([\s\S]*?)\}\s*\)/g)) {
      const body = m[1];
      const s = (body.match(/slug\s*:\s*['"]([^'"]+)['"]/) || [])[1] || slug;
      const keys = [...strings((body.match(/levels\s*:\s*\[([^\]]*)\]/) || [])[1]),
                    ...strings((body.match(/boards\s*:\s*\[([^\]]*)\]/) || [])[1])];
      if (!declared.has(s)) declared.set(s, new Set());
      keys.forEach(k => declared.get(s).add(k));
    }
  }
}

const failed = [];
async function get(path) {
  const url = DB + '/' + path + '.json';
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const r = await fetch(url, { method: 'GET' });
      if (r.ok) return await r.json();
      if (attempt === 2) failed.push(path + ' (HTTP ' + r.status + ')');
    } catch (e) {
      if (attempt === 2) failed.push(path + ' (' + e.message + ')');
    }
  }
  return undefined;
}

const rows = [];
const date = t => (typeof t === 'number' ? new Date(t).toISOString().replace('T', ' ').slice(0, 16) + 'Z' : '?');

const recent = (await get('recent_scores')) || {};
const recentCount = Object.keys(recent).length;
const fed = new Map();            // slug -> Set of levelKeys seen in recent_scores
for (const [id, e] of Object.entries(recent)) {
  if (e && e.slug && e.levelKey) {
    if (!fed.has(e.slug)) fed.set(e.slug, new Set());
    fed.get(e.slug).add(e.levelKey);
  }
  if (e && WANT.has(String(e.initials || '').toUpperCase()))
    rows.push({ source: 'recent_scores', initials: e.initials, game: e.slug || e.game, level: e.levelKey || e.level, score: e.score, ts: e.timestamp, id });
}

const boards = new Map();         // board key -> [slug, level]
for (const src of [declared, fed]) for (const [slug, keys] of src) for (const k of keys) boards.set(boardKey(slug, k), [slug, k]);
const extra = [...boards.keys()].filter(b => ![...declared].some(([s, ks]) => [...ks].some(k => boardKey(s, k) === b)));

let read = 0, nonEmpty = 0;
const list = [...boards.entries()];
for (let i = 0; i < list.length; i += 8) {
  await Promise.all(list.slice(i, i + 8).map(async ([key, [slug, level]]) => {
    const data = await get('leaderboards/' + key);
    if (data === undefined) return;
    read++;
    if (!data) return;
    nonEmpty++;
    for (const [id, e] of Object.entries(data))
      if (e && WANT.has(String(e.initials || '').toUpperCase()))
        rows.push({ source: 'leaderboards/' + key, initials: e.initials, game: slug, level, score: e.score, ts: e.timestamp, id });
  }));
}

rows.sort((a, b) => (a.source === b.source ? 0 : a.source === 'recent_scores' ? 1 : b.source === 'recent_scores' ? -1 : a.source < b.source ? -1 : 1) || (a.ts || 0) - (b.ts || 0));
console.log('Initials: ' + [...WANT].join(', ') + '  database: ' + DB);
console.log('recent_scores entries read: ' + recentCount);
console.log('boards named: ' + boards.size + ' (' + extra.length + ' only from recent_scores); read: ' + read + '; non-empty: ' + nonEmpty);
console.log('');
console.log('| Source | Initials | Game | Level | Score | Date (UTC) | Push id |');
console.log('|---|---|---|---|---|---|---|');
for (const r of rows) console.log('| ' + [r.source, r.initials, r.game, r.level, r.score, date(r.ts), r.id].join(' | ') + ' |');
console.log('');
const by = {};
for (const r of rows) {
  const k = (r.source === 'recent_scores' ? 'recent_scores' : 'leaderboards') + ' ' + r.initials;
  by[k] = (by[k] || 0) + 1;
}
console.log('Matches: ' + rows.length + ' (' + Object.entries(by).sort().map(([k, n]) => k + ' ' + n).join(', ') + ')');
console.log('Failed reads: ' + (failed.length ? failed.join('; ') : 'none'));
process.exit(failed.length ? 1 : 0);
