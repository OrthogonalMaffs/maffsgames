---
name: sheets-falsy-backfill
description: Audit and fix for 1.25 — the Sheets analytics endpoint's `|| ''` coercion silently blanked legitimate false/0 values. Covers the inventory, the fix, what the Dashboard has actually been showing, whether past rows can be recovered, and Jon's redeploy steps.
---

# Sheets analytics — falsy-value coercion (1.25): audit, fix, backfill

Written 29 Sep 2026, in response to Jon's contract for item 1.25. Code fix only — the live
spreadsheet, the deployed Apps Script and the daily trigger are untouched. Nothing in this session
sent a real event to the live endpoint.

## 0. Root cause, in one line

`docs/apps-script-endpoint.js`'s `doPost` wrote every field as `data.field || ''`. In JavaScript,
`false || ''` and `0 || ''` both evaluate to `''`, so a genuinely wrong answer (`correct: false`)
and a genuinely zero value (`question_index: 0`, `score: 0`, `questions_correct: 0`, …) were written
to the sheet as an **empty cell** — indistinguishable from a field that was never sent at all. GA4
is unaffected; it receives `params` unmodified via `gtag('event', eventName, params)`.

## 1. Inventory — every falsy-coercing default in the pipeline

### `docs/apps-script-endpoint.js` — `doPost`, pre-fix lines 40–48

All sixteen fields used the same `data.field || ''` shape. Verdict per field, based on what every
real sender actually puts there (checked against every call site — §1 below the table):

| Field | Can it legitimately be falsy? | Verdict |
|---|---|---|
| `event` | No — guarded by `if (!data.event) return …` immediately above, and event names are never empty | Harmless |
| `game_slug` | No — always a non-empty slug | Harmless |
| `level` | No — games without levels send `'all'` per canon, never `''` | Harmless |
| `mode` | Legitimately *absent* for single-mode games — `\|\| ''` is the intended default for a genuinely optional field | Harmless |
| `question_index` | **Yes** — 1-based for every real question, but the escape-room "search" event sends `0` deliberately (`escape-rooms/assets/engine.js:347`) | **Destructive** |
| `correct` | **Yes** — `false` on every wrong answer, which is roughly half of all `question_answered` rows | **Destructive** |
| `attempts` | Plausibly not — every sender increments before reporting (checked `equation-builder`, `maths-court`, `expectation-station`); no confirmed 0-send found, but not exhaustively traced through every game's internal state machine | Likely harmless, **not fully verified** |
| `score` | **Yes** — 0 is an ordinary score (e.g. every question wrong) | **Destructive** |
| `questions_answered` | Not confirmed — no call site found that could report 0 (an abandon at 0 answered doesn't fire `game_completed`), but not exhaustively traced | Likely harmless, **not fully verified** |
| `questions_correct` | **Yes** — 0 is ordinary (a completion with nothing right); 40 games send this field | **Destructive** |
| `previous_score` | **Dead column — see §1.1 below.** No sender ever populates it, under any value, so this was never affected by the coercion; it has always been blank for a different reason | N/A — separate finding |
| `difficulty` | String field, same shape as `mode` | Harmless |
| `filter_type` | Portal-only string, always non-empty when sent | Harmless |
| `filter_value` | Portal-only string, always non-empty when sent (`v1\|...`) | Harmless |
| `client_ts` | ISO timestamp string, always non-empty | Harmless |
| `seq` | `analytics.js` pre-increments from 0 (`++_seq`), so the first value sent is always `1`, never `0` | Harmless in practice |

**§1.1 — a second, unrelated finding surfaced while checking this table: `previous_score` is a dead
column.** The endpoint reads `data.previous_score`, but every sender (checked 69 games sending
`personal_best_set`) sends the field as **`previous_best`**, not `previous_score`. This is a
field-name mismatch, not a falsy-coercion bug — the column has been blank on *every* row since the
event was added, for every value including genuinely non-zero ones, and would have stayed blank
even with today's fix. It falls outside 1.25 and outside this contract's DO NOT TOUCH (no schema
changes without Jon's approval), so it is reported here, not fixed. Worth its own decision: rename
the column to `previous_best` to match reality, or start sending `previous_score`.

### `schools/assets/analytics.js`

The values actually **sent** to both GA4 and the Sheets endpoint are untouched by `||` anywhere:
`mfg()` builds the payload as `Object.assign({event, client_ts, seq}, params)` (`:84`), which copies
every key of `params` — including `false` and `0` — through unmodified. The escape-room `track()`
wrapper (`escape-rooms/assets/engine.js:205`) does the same with a plain `for (var k in extra)
p[k] = extra[k]` copy.

Three `||` uses exist in `analytics.js`, all found harmless:
- `:54`–`:56` (`game_abandoned` context backfill) — `if (!params.question_index) params.question_index
  = window._mfgQuestionIndex || 0;` only fires when the caller's own value is already falsy, and in
  the one real call site (`:143`) that value is already `window._mfgQuestionIndex || 0` — so the
  reassignment produces the identical value. Fragile pattern (relies on the two computations
  matching), currently a no-op.
- `:65`–`:67` (`game_started`-vs-`game_restarted` detection) — `!window._mfgQuestionIndex` uses `0`
  as its own "no question answered yet" sentinel, which is exactly what it means; self-consistent.
- `:108`–`:109` (`game_slug`/`level` capture on `game_started`) — same shape as the endpoint's
  harmless string fields; slugs and levels are never legitimately empty.

**Conclusion: no fix needed in `analytics.js`.** The bug is isolated to the endpoint's write path.

### Coverage check behind the inventory

To know whether a blank `correct`/`question_index`/`score` cell can be trusted as "was really
`false`/`0`" rather than "the field was never sent," every static call site was checked for
structural omission:

- 160 `mfg('question_answered', …)` calls across every game — **0 omit `correct`**, **0 omit
  `question_index`**.
- 171 `mfg('game_completed'/'personal_best_set', …)` calls — **0 omit `score`**.
- The escape-room engine's 3 direct `track('question_answered', …)` call sites (shared by every
  room) — all 3 carry both fields explicitly, including the `question_index: 0` search sentinel.

This is a structural check (the object literal always names the key) — it does not trace whether a
referenced variable could itself evaluate to `undefined` at runtime in some path not covered by
static reading. Given every occurrence found is either a literal boolean/number or a variable that
is also used for on-screen feedback in the same function (so an `undefined` there would already be a
visible game bug, not just an analytics gap), this is treated as high-confidence, not certainty.

## 2. The fix

One helper, `cellValue()`, used by the whole write path (`docs/apps-script-endpoint.js:461`):

```js
function cellValue(v) {
  return (v === undefined || v === null) ? '' : v;
}
```

`doPost` (`:40`–`:48`) now calls `cellValue(data.field)` for all sixteen fields instead of
`data.field || ''`. `SCRIPT_VERSION` bumped to `'2026-09-29-c'` so the redeploy is confirmable (§6).

**Local proof (node is not installed on this machine, same gap already noted elsewhere in
`docs/todo.md` for `check-leaderboard-coverage.js`).** The helper has no JS-specific coercion
quirks — it is a single equality check against two singleton values — so a Python-equivalent trace
of the exact same logic is a faithful proxy, run locally:

```
input        -> output     type
true         -> True       bool
false        -> False      bool
0            -> 0          int
1            -> 1          int
''           -> ''         str
null         -> ''         str
undefined    -> ''         str
'x'          -> 'x'        str
```

`false` and `0` now pass through unchanged; only `null`/`undefined` map to `''`. Jon's own
verification in the Apps Script editor (§6) is the authoritative confirmation, not this proxy.

## 3. Dashboard audit — what each chart has actually been showing

The Dashboard and the 7am email are rebuilt from the same sheet by the same script
(`sendDailyReport` → `rebuildDashboard`). Only two things read the affected fields:

**"Accuracy by Game" and "Hardest Questions" (and the email's identical logic, `:108`–`:125`).**
Both compute correctness with `String(r[col['correct']]) === 'true'`. A blank cell and a real `FALSE`
cell produce the **same result** under this check — `String('') !== 'true'` and `String(false) !==
'true'` are both true, so neither is counted as correct. Critically, the *denominator* (`total`) is
never gated on `correct` at all — it only requires `event === 'question_answered'` — so blanked rows
were still counted as attempts, just correctly never counted as correct. **Verdict: these figures
have been right all along, "right by accident"** — the check happens to treat "blank" and "false"
identically, not because the code accounted for the coercion, but because neither value equals the
string `'true'`. **Confirmed the fix doesn't break this**: after the fix, a real `FALSE` cell read
back via `getValues()` is the JS boolean `false`, and `String(false) === 'true'` is still `false` —
identical outcome to before. No chart logic needs to change.

**"Hardest Questions"' grouping key** (`key = slug + ' Q' + question_index`) is the one place the bug
was *visible*, not just latent: a blanked `question_index: 0` produced a key like `"room-slug Q"`
(no number) instead of `"room-slug Q0"`. This only ever affects the escape-room search sentinel — no
other event legitimately reaches this code with a falsy index — so it's a cosmetic label defect on
one row-shape, never a miscount. It self-corrects once the fix is live; no historical row needs
touching for this to display correctly going forward.

**Every other table** (Top Games, Level Breakdown, Daily Activity) reads only `event`, `game_slug`,
`level` and `timestamp` — none of which were ever coerced. Unaffected, not audited further.

**`score`, `questions_correct`, `questions_answered`, `attempts`, `previous_score`: not read by any
Dashboard table or the email.** They were silently losing data (except `previous_score`, dead for a
different reason, §1.1) but nothing in this script has been drawing a wrong conclusion from them —
because nothing in this script reads them yet. Anyone building a new report from the raw sheet,
though, would have been trusting blanks that were really zeros.

## 4. Backfill — can past rows be recovered?

**(a) `correct` on `question_answered` rows.** Yes, with high confidence. Every sender structurally
includes `correct` (§1's coverage check, 160/160). A blank cell in this column, on a
`question_answered` row written before the redeploy, can only be the coercion bug turning `false`
into `''` — there is no code path found that omits the field.

**(b) `question_index` (same rows) and `score` (`game_completed`/`personal_best_set` rows).** Same
conclusion, same evidence (171/171 for `score`; 160/160, including the escape-room engine's 3 direct
sites, for `question_index`).

**Not backfilled in the function below, deliberately:** `questions_correct` (40 senders confirmed,
plausibly destructive, but not named in the contract's exact change — add it once Jon's satisfied
with the pattern on the three fields above) and `attempts`/`questions_answered` (not confirmed to
ever legitimately be 0 — see §1's "not fully verified" rows). `previous_score` **cannot** be
backfilled at all — no sender has ever populated it under any name the endpoint reads, so there is no
correct value to recover; every historical blank there reflects the schema mismatch in §1.1, not a
lost `0`/`false`.

**(c) The one-off Apps Script function — write only, do NOT run.** Paste this into the same Apps
Script project (it can live in `Code.gs` alongside the rest, or a scratch file) and run it manually,
once, from the Apps Script editor — never from this repo, never against a test event:

```js
// One-off, paste into the Apps Script editor and run manually. Rewrites blank
// cells that the pre-2026-09-29-c `|| ''` coercion produced back to their real
// value, on rows written before Jon's redeploy only (see BACKFILL_CUTOFF).
// Safe to run twice: a cell already holding FALSE/0 is left alone, so a
// second run finds nothing left to change.
//
// Jon redeployed at approximately 19:18Z on 29 Sep 2026; live rows since
// then show correct/score writing through correctly. Confirm the exact
// moment against the Apps Script editor's "Manage deployments" dialog (or
// the Executions log) before running this, and tighten the value below if
// it disagrees with the approximate time here. Any row with a timestamp at
// or after this moment is left untouched — after the redeploy, a blank in
// these columns no longer means "was falsy", it means something genuinely
// omitted the field, which this function must not paper over.
var BACKFILL_CUTOFF = '2026-09-29T19:18:00Z'; // confirm exact time before running

function backfillFalsyBlanks() {
  var sheet = getOrCreateSheet();
  var data = sheet.getDataRange().getValues();
  var headers = data[0];
  var col = {};
  headers.forEach(function(h, i) { col[h] = i; });

  var cutoff = new Date(BACKFILL_CUTOFF);
  var changed = { correct: 0, question_index: 0, score: 0 };

  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var ts = new Date(row[col['timestamp']]);
    if (ts >= cutoff) continue; // never touch a post-redeploy row

    var event = row[col['event']];

    if (event === 'question_answered') {
      if (row[col['correct']] === '') {
        sheet.getRange(i + 1, col['correct'] + 1).setValue(false);
        changed.correct++;
      }
      if (row[col['question_index']] === '') {
        sheet.getRange(i + 1, col['question_index'] + 1).setValue(0);
        changed.question_index++;
      }
    }

    if (event === 'game_completed' || event === 'personal_best_set') {
      if (row[col['score']] === '') {
        sheet.getRange(i + 1, col['score'] + 1).setValue(0);
        changed.score++;
      }
    }
  }

  Logger.log('Backfill complete. correct: %s, question_index: %s, score: %s rows changed.',
    changed.correct, changed.question_index, changed.score);
}
```

Per-cell `setValue` rather than a batched `setValues` — simpler to reason about correctness on a
one-off run against a sheet whose size is a few thousand rows, not a hot path. If the sheet has grown
large enough that this is slow, batch by column range instead of rewriting the loop's logic.

**(d) Cutover rule.** Enforced by `BACKFILL_CUTOFF` above: any row timestamped at or after the moment
Jon redeploys is never touched. Run the backfill only after confirming the new version is live (§6),
and set the cutoff to that confirmed moment, not to "now" guessed in advance.

## 5. Escape-room `question_index: 0` — why, report only, not fixed here

`escape-rooms/assets/engine.js:347`:

```js
if (first) track('question_answered', { correct: true, question_index: 0, detail: 'searched:' + o.id });
```

This fires from the room's object-search interaction (looking at/examining a scene object), the
first time a player does it in a room — a "discovery" action the room credits as a correct answer,
distinct from the numbered lock puzzles. Locks use `R.locks.indexOf(l) + 1` (`:618`, `:628`) and
hints use `activeLock + 1` (`:719`) — both correctly 1-based, matching canon §1.3/`.claude/rules/
analytics.md:61`'s "question_index is 1-based" rule. The search action is the **only** place in the
whole codebase that sends `question_index: 0` on a `question_answered` event — it's a deliberate
sentinel for "not a numbered lock," not an accident, but it does contradict the documented 1-based
convention. Also worth noting: the endpoint has no `detail` column in `EXPECTED_HEADERS`, so this
event's `detail: 'searched:...'` field (which is what actually distinguishes it from a real lock) is
silently dropped by the Sheets write path — GA4 keeps it, the sheet doesn't. Both are reported for
Jon's own call, per DO NOT TOUCH; neither is touched in this session.

## 6. Jon's redeploy steps

**Steps 1–4 done — redeployed ~19:18Z 29 Sep 2026, live rows since confirm `correct`/`score` writing
through.** Steps 1–4 kept below for the record and for any future redeploy of this endpoint.

1. Open the Apps Script project (the one bound to the "MaffsGames Events" sheet — Extensions → Apps
   Script from the sheet, or apps.script.google.com).
2. Open `Code.gs` and replace its contents with the updated `docs/apps-script-endpoint.js` from this
   repo (the `doPost` fix, the new `cellValue()` helper, and `SCRIPT_VERSION = '2026-09-29-c'`).
3. Save, then **Deploy → Manage deployments → edit (pencil) → Version: New version → Deploy** — the
   same redeploy path already documented in the file's own header comment. Publishing a *new version*
   of the *existing* deployment keeps the same `/exec` URL live; do not create a fresh deployment.
4. **Confirm the new version is live without sending a live event** — DO NOT TOUCH forbids testing
   through a real game or the stub-free path. Two safe checks, either is sufficient:
   - Visit the deployment's `/exec` URL directly in a browser (a `GET`, which `doGet` answers) and
     confirm the JSON response's `"version"` reads `"2026-09-29-c"`.
   - In the Apps Script editor, open **Executions** (left sidebar) after the deploy and confirm the
     latest `doGet`/`doPost` execution ran against the version you just published, or run `doGet`
     manually from the editor (Run ▶ on the `doGet` function) and read its return value in the log.

**Outstanding — parked, Jon's own tasks, not blocking anything:**

5. **Back up the sheet** as it stands now (pre-backfill) before running step 6 — the backfill writes
   directly to real rows with `setValue()`, and a backup is the only undo.
6. Confirm the exact redeploy moment (§4 above) and tighten `BACKFILL_CUTOFF` in §4(c)'s function if
   it differs from the approximate `2026-09-29T19:18:00Z` already set there, paste the function into
   the same Apps Script project, and run it manually once from the editor (Run ▶ on
   `backfillFalsyBlanks`). Read the `Logger.log` output (View → Logs, or Executions) for the row
   counts changed. Running it again should log 0 for all three counts — that's the "safe to run
   twice" check.
