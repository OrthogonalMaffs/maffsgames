// Occasional manual prune of recent_scores (the portal ticker's feed). NOT automated.
//
// The database rules refuse deletes from the site, so the feed only grows; the ticker
// reads the latest 20 and does not care how long it is. Run this now and then to keep
// the newest N and delete the rest. It uses the Admin SDK, which the rules do not
// apply to, so it needs a service-account key -- keep that file OUT of the repo.
//
//   node prune-recent-scores.mjs --key <service-account.json>              (dry run: counts only)
//   node prune-recent-scores.mjs --key <service-account.json> --apply      (deletes)
//   node prune-recent-scores.mjs --key <...> --keep 200 --apply            (keep a different number)
//
// Against the emulator (how it was tested): FIREBASE_DATABASE_EMULATOR_HOST=127.0.0.1:9000
// and no --key. Full procedure: docs/firebase-rules-deploy.md, "Pruning the ticker feed".
import { readFileSync } from 'node:fs';
import { initializeApp, cert } from 'firebase-admin/app';
import { getDatabase } from 'firebase-admin/database';

const DB_URL = 'https://maffsgames-c1c9f-default-rtdb.europe-west1.firebasedatabase.app';
const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : undefined; };
const keep = parseInt(arg('--keep') || '50', 10);
const apply = process.argv.includes('--apply');
const keyPath = arg('--key');
const emulator = process.env.FIREBASE_DATABASE_EMULATOR_HOST;

if (!emulator && !keyPath) {
  console.error('Pass --key <service-account.json> (Firebase console > Project settings > Service accounts).');
  process.exit(2);
}
if (!(keep >= 20)) {
  console.error('--keep must be at least 20: the ticker shows the latest 20.');
  process.exit(2);
}

const app = initializeApp(emulator
  ? { projectId: 'demo-maffsgames', databaseURL: 'http://' + emulator + '?ns=demo-maffsgames' }
  : { credential: cert(JSON.parse(readFileSync(keyPath, 'utf8'))), databaseURL: DB_URL });
const ref = getDatabase(app).ref('recent_scores');

const snap = await ref.orderByChild('timestamp').once('value');
const keys = [];
snap.forEach(child => { keys.push(child.key); });          // oldest first
const drop = keys.slice(0, Math.max(0, keys.length - keep));
console.log(`recent_scores holds ${keys.length}; keeping the newest ${Math.min(keep, keys.length)}, ` +
            `${apply ? 'deleting' : 'would delete'} ${drop.length}.`);
if (apply && drop.length) {
  const updates = {};
  for (const k of drop) updates[k] = null;
  await ref.update(updates);                                  // one multi-path delete
  console.log('Done.');
} else if (!apply) {
  console.log('Dry run: nothing deleted. Add --apply to delete.');
}
process.exit(0);
