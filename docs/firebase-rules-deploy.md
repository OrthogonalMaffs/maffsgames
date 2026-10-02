# Realtime Database rules: deploy, verify, roll back

Written 30 Sep 2026. **Jon deploys; no session touches the live rules.**

**Status: DEPLOYED by Jon on 30 Sep 2026 (night) and verified live**: every refusal below held, the ticker query
works, and a real score submitted. The steps stay here for the next change or a rollback.

## Why

On 30 Sep 2026 eleven `JLF` test scores were removed from the live database with a
plain REST `DELETE` and no login. The same request could empty every leaderboard and
the portal ticker, or overwrite any score. The new rules allow **new** scores only:
nothing can be deleted or overwritten from the site, and a new score must have the
shape `submitScore()` writes.

## What the rules do (`firebase/database.rules.json`)

| Path | Read | Write |
|---|---|---|
| `/` (root) | no | no |
| `leaderboards/<board>` | anyone (the hub, `standing()`) | — |
| `leaderboards/<board>/<entry>` | anyone | **create only**: `score` (number), `timestamp` (number, within 60 s of the server's clock), optional `initials` (0–3 capital letters), nothing else; board names `a-z 0-9 _`, up to 80 characters |
| `recent_scores` | anyone (the ticker) | — |
| `recent_scores/<entry>` | anyone | **create only**: `game` (1–80 chars), `slug` (`a-z 0-9 -`), `level` (the display label, up to 60 chars, may be empty for "all"), `levelKey` (`a-z 0-9 -`), `score` (number), `timestamp` (within 60 s), optional `initials`, nothing else |

`recent_scores` gains `.indexOn: ["timestamp"]`, so the ticker's
`orderByChild('timestamp').limitToLast(20)` is served by the database, not by downloading
the whole feed.

**The live rules today could not be read from here** (that needs the console). What is
known from their behaviour: single boards and `recent_scores` read anonymously, the root
does not, and anonymous writes and deletes succeed. Step 1 below saves them before they
are replaced.

## What changed in the site (same PR)

`schools/assets/firebase-leaderboard.js`:
- **The client-side prune of `recent_scores` is gone.** Each submit used to delete the
  oldest entries beyond 50, which needs the delete permission the new rules remove. The
  ticker only ever shows the latest 20, so the feed can grow; prune it now and then by
  hand (below).
- **The timestamp is taken when the score is written**, not when the initials overlay
  opens. The rules refuse a timestamp more than 60 s from the server's clock, and a player
  can sit on the overlay for longer than that.

**Deploy order: merge the site change first, then publish the rules.** Pages that loaded
the old script before the merge (browser cache, up to 10 minutes) will try the old prune
after a submit; the rules refuse it, the score itself is already saved, and nothing is
shown to the player.

## Tested (emulator, 30 Sep 2026)

`cd firebase && npm install && npm test` (needs Java) runs `rules.test.mjs` against the
Firebase emulator loaded with the rules. **32 of 32 cases pass**:

- **Accepted:**
  - a new board score, with initials and without (Skip);
  - a daily-pizza board;
  - a new ticker entry, including level "all" (empty label).
- **Refused, overwrites and deletes:**
  - overwriting or updating an existing score;
  - deleting a score, a whole board or all leaderboards;
  - overwriting a ticker entry, deleting a ticker entry, or deleting the whole ticker.
- **Refused, bad shape:**
  - a score as a string;
  - a missing timestamp or score;
  - an unexpected child;
  - lower-case, four-letter or digit initials;
  - a ticker entry missing `levelKey`;
  - a slug with capitals;
  - a 200-character game name;
  - a board key with capitals;
  - a write anywhere else.
- **Refused, timestamps:** one day in the future, 5 minutes stale, and a far-future
  ticker entry.
- **Reads:** one board works; the ticker query returns its 20; a read of the root is
  refused.

The same suite run against open rules (read and write for anyone, as live today) fails
26 of its 32 cases, so it tells the two apart.

## Deploy (Firebase console)

1. **Save the current rules.** Firebase console → project **maffsgames-c1c9f** → Build →
   Realtime Database → **Rules** tab. Select all, copy, and paste into a new file
   `firebase/database.rules.previous.json` (commit it, or keep it somewhere safe). This is
   the rollback.
2. **Paste the new rules.** Replace the editor's contents with the whole of
   `firebase/database.rules.json` from `main`.
3. Optional: the console's **Rules Playground** can simulate a write. Location
   `/leaderboards/factor_race_gcse/test1`, type **set**, unauthenticated, data
   `{"score": 1, "timestamp": <now in ms>}` should be allowed; type **remove** on an
   existing entry should be denied.
4. **Publish.**

## Verify (straight after publishing)

1. **A real score submits.** On maffsgames.co.uk (not localhost; the script writes from the
   live host only), finish a short game, e.g. Factor Race, enter initials, and check the
   score appears on its board in the hub and on the front-page ticker.
2. **A delete is refused.** From any terminal, against an entry of your own:

       curl -X DELETE "https://maffsgames-c1c9f-default-rtdb.europe-west1.firebasedatabase.app/leaderboards/<board>/<entry id>.json"

   Expected reply: `{ "error" : "Permission denied" }`. (Before the new rules this deleted
   the entry.) Then remove your test score by hand in the console's **Data** tab: the console
   is not bound by the rules.
3. **An overwrite is refused.** Same entry: `curl -X PUT -d '{"score":99999,"timestamp":1}' <same URL>`
   → `Permission denied`.

## Roll back

Rules tab → paste the saved `firebase/database.rules.previous.json` → Publish. The site
change needs no rollback: without the prune it still submits and reads normally under the
old rules (the feed simply grows, which the ticker ignores).

## Pruning the ticker feed (occasional, manual)

The feed now only grows. A few hundred entries is harmless; prune when it bothers you,
say once a term.

- **By hand:** console → Realtime Database → Data → `recent_scores` → delete entries
  (the console ignores the rules).
- **By script** (keeps the newest 50):
  1. Console → Project settings → **Service accounts** → *Generate new private key*.
     Save the JSON **outside the repo** and never commit it.
  2. `cd firebase && npm install`, then a dry run first:
     `node prune-recent-scores.mjs --key <path-to-key.json>`. This prints how many would go.
  3. `node prune-recent-scores.mjs --key <path-to-key.json> --apply`.
     `--keep 200` keeps more, and it will not keep fewer than 20.
  4. Delete the key file afterwards, or revoke it in the console.

  Tested against the emulator on 30 Sep 2026: 80 entries; the dry run deleted nothing;
  `--apply` left the newest 50.

## Known limits

- **A device whose clock is more than a minute out cannot submit.** Its score is refused
  (the player sees the usual end screen; the console logs why). School machines and phones
  normally sync their clocks. If it ever matters, the fix is for the client to write
  `firebase.database.ServerValue.TIMESTAMP` and the rule to require `newData.val() == now`.
  That is a change to what is stored, so it needs its own contract.
- **The rules do not stop someone writing a fake high score** of the right shape. They stop
  deletion and tampering with existing scores. Bounding scores per game would need per-game
  limits in the rules, which is a bigger piece of work.
