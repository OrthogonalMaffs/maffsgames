# Runbook — Redeploying the Analytics Apps Script

`docs/apps-script-endpoint.js` in this repo is a **mirror of** the deployed Web App, not the
deployment. Editing it changes nothing live until you follow this procedure.

## Where the live script actually is

**It is bound to the "MaffsGames Events" spreadsheet.** Open it via the Sheet →
**Extensions → Apps Script**.

> Confirmed 2026-08-26. An earlier version of this runbook claimed it was standalone, inferring
> that from `DriveApp.getFilesByName` (the standalone idiom). That was wrong — the code uses that
> call despite being container-bound.

### ⚠️ Deleting the spreadsheet deletes the script

A container-bound script has no independent existence. Deleting or trashing the
**MaffsGames Events** sheet destroys the analytics endpoint along with it. Treat that
spreadsheet as production infrastructure, not just a data file.

---

## ⚠️ The one thing that breaks everything

When deploying, choose **new version of the EXISTING deployment**, never *New deployment*.

A new deployment gets a **different `/exec` URL**. The current URL is hardcoded in
`schools/assets/analytics.js`, so a changed URL means **all 94 games silently stop logging** —
no error, no warning, the data just stops.

The live URL must stay ending in:

```
AKfycbzKUxT4TpL2kgFNFBzVEw0ALv3A7qHndNjgIdBoSedtl8T17O2KV7TLrtuVCrYmAkVR
```

---

## Which project is the live one?

As of 2026-08-26 there were **four "Untitled project"s** in this account (three standalone, one
bound to a Sheet) and only one of them serves the live URL. If you open the wrong one it says
*"This project has not been deployed yet"*.

**Triggers and deployments are independent.** A project fires its triggers whether or not it is
deployed — which is why duplicate projects produced duplicate daily emails while only one project
served `/exec`.

**Never delete a project before confirming it is not the deployed one.** Deleting the deployed
project destroys the `/exec` URL permanently; it cannot be recreated, and all 94 games would need
editing.

To identify it, open each project → **Deploy → Manage deployments**:

- Wrong ones say *"not been deployed yet"*.
- The live one shows an active **Web app** deployment whose **Deployment ID** matches the string
  in the warning box above.

Then **rename them** — `MaffsGames Analytics (LIVE)` and `OLD — do not use`. Four identically
named projects is what caused the confusion in the first place.

To find what is emailing you: open the **Triggers** panel (alarm-clock icon) in *every* project
and delete `sendDailyReport` from all except the live one.

---

## Procedure

### 1. Open the project
Open the **MaffsGames Events** spreadsheet → **Extensions → Apps Script**. That is the live,
container-bound project. The other "Untitled project"s at script.google.com are not deployed.

### 2. Replace the code
Open `Code.gs` (or whichever file holds `doPost`). Select all, delete, and paste the full
contents of `docs/apps-script-endpoint.js` from this repo. **Ctrl+S** to save.

**Then set `REPORT_EMAIL`** (near the top) from `'OWNER_EMAIL_HERE'` to your own address before
saving. The repo copy holds a placeholder on purpose: the address is not kept in the repo (canon §7.7).

### 3. Fix the duplicate daily email — run `setupTrigger`
In the function dropdown at the top of the editor, select **`setupTrigger`**, then click **Run**.

This deletes *every* existing `sendDailyReport` trigger and creates exactly one at 07:00
Europe/London. It is safe to run repeatedly — that is the point of it.

- First run will prompt for **authorisation**. Accept it (it's your own script).
- Google may warn the app is "unverified" — *Advanced → Go to (project name)*.

Then confirm: **left sidebar → Triggers (alarm-clock icon)**. You should see **exactly one** row,
`sendDailyReport`, Time-driven, Day timer, 7am–8am.

### 4. Deploy the new version
**Deploy → Manage deployments →** click the **pencil/edit icon** on the existing deployment →
**Version: New version** → optionally describe it → **Deploy**.

Do **not** use *Deploy → New deployment*. See the warning above.

### 5. Verify
Copy the Web App URL shown after deploying and check it still ends with the string in the
warning box above. If it changed, you created a new deployment — go back and edit the original
one instead.

Then open the `/exec` URL in a browser. It returns the health check, which now reports the
version baked into the code:

```json
{"status":"ok","service":"MaffsGames Analytics","sheet":"MaffsGames Events","version":"2026-08-26-a"}
```

If `version` is missing, the deploy did not land — you are still on old code, most likely because
you saved without deploying a new version. **Bump `SCRIPT_VERSION` in the source every time you
redeploy**, so this check stays meaningful.

Then play any game for a few questions and check the **MaffsGames Events** sheet:

- New rows appear
- Columns **P (`client_ts`)** and **Q (`seq`)** are populated
- Columns A–O are unchanged and still aligned
- From `2026-11-03-a` (QUESTION-ID): cell **R1** reads `question_id` (the first post after the deploy writes it:
  `ensureHeaders` rewrites row 1 whenever it differs from `EXPECTED_HEADERS`, so there is nothing to type), and a
  `question_answered` row from Sequence Solver has `h` + 8 hex digits in column **R**. Other games leave R blank
  until they are moved onto it.
- From `2026-11-03-b` (DASHBOARD-METRICS): the report reads `data/games.json` from GitHub with `UrlFetchApp`, so the
  first run after this deploy asks for one new permission, **"Connect to an external service"**: accept it (run
  `testDashboard` once from the editor to grant it straight away). The Dashboard then shows question-game accuracy
  (at least 30 answers), hardest questions by `question_id` (at least 10 attempts) and an Escape Rooms table, and names
  Trig Wars and Bearing Blitz as left out of accuracy. If either the email or the Dashboard says "games.json could
  not be read", the fetch failed: the report still went out, with every game counted as a question game.
- From `2026-11-04-a` (ROOM-ESCAPED): no new permission. A room counts as escaped only when every lock opened
  (`questions_correct` equals `questions_answered`, both above 0); any other room `game_completed` is a timeout, shown
  as "T timed out" in the email's rooms line and a **Timed out** column on the Dashboard's Escape Rooms table.
- From `2026-11-07-a` (ROOM-TIMES): no new permission. Cell **S1** reads `detail` (the first post after the deploy
  writes it, as R1 was), and an escape room's `game_completed` row has its times in column **S**, e.g.
  `escaped wrongs:1 hints:2 used:612 played:567 locks:182,431,567` (canon §1.3). Its other rows carry the lock id
  (`question_answered`), `lock:step` (`hint_used`) or `fresh`/`resumed` (`game_started`). Other games leave S blank.

---

## 14 Nov 2026: safe tallies

Version `2026-11-14-a` (contract COUNTS-SAFE-TALLY). **`doPost` is unchanged**: events are recorded exactly as before,
the columns and the `/exec` address stay as they are, and no new permission is asked for. Only the report changed.
Anyone can post an event, and its `game_slug`, `level` and `question_id` are used as keys when the daily email and the
Dashboard are added up. A slug such as `constructor` or `__proto__` used to turn that game's figures into text
("function Object() { [native code] }11 starts") or drop the game. Those names are now counted like any other.

The deploy is a **New version of the existing deployment**, never a new deployment.

1. Open https://script.google.com/home. Open **Maffsgames Analytics** (green icon, bound to MaffsGames Events). Check the title at the top says **Maffsgames Analytics** before doing anything else.
2. Open `Code.gs` and find the line that starts `const REPORT_EMAIL =`. Copy that whole line somewhere safe: it holds your address, which the repo's copy does not.
3. Select everything in `Code.gs` and delete it.
4. Paste the whole of `docs/apps-script-endpoint.js` from the repo.
5. Replace the pasted `const REPORT_EMAIL = 'OWNER_EMAIL_HERE';` line with the line you copied in step 2.
6. Click **Save** (the disk icon).
7. Click **Deploy** → **Manage deployments**.
8. Click the pencil on the existing deployment.
9. Set **Version** to **New version**.
10. Click **Deploy**. Do not use *New deployment*: it would change the address and every game would stop logging.
11. Check the Web app URL it shows still ends with the string in "The one thing that breaks everything" above.
12. Open the `/exec` URL in a private window. It must show `"version":"2026-11-14-a"`.
13. Back in the editor, choose **testDashboard** in the function drop-down and click **Run**. It rebuilds the Dashboard tab with the new code. If Google asks for a permission, stop and tell Claude which one it named.
14. Open the **MaffsGames Events** Sheet, play a few questions of any game, and check a new row appears as usual.

Do not run `setupTrigger`: the 7am trigger is not touched by this. Tomorrow's email is the first sent by the new code.

---

## If you still get two emails after this

`setupTrigger` can only see triggers **in this project, owned by you**
(`ScriptApp.getProjectTriggers()`). Two emails surviving step 3 means one of:

1. **A second copy of the project exists** — likely created during the April 2026 daily-email
   debugging. Check script.google.com for a duplicate project and delete its trigger (or the
   whole project, once you've confirmed it isn't the one serving the live `/exec` URL).
2. **A trigger owned by a different Google account** with edit access on the project. That
   account has to delete its own trigger; yours cannot.

Diagnose by comparing the two emails' arrival times. Identical content a few seconds apart
points at two triggers; genuinely different content points at two projects reading the sheet
differently.

**Resolution, 2026-08-26:** the live project is the sheet-bound one; the duplicate email came
from `sendDailyReport` triggers left behind on the unused standalone copies. Delete those
triggers, rename the projects `OLD — do not use`, confirm a single email arrives the next
morning, and only then delete the projects.

---

## Trigger failures

The Triggers panel shows a failure rate per trigger. On 2026-08-26 the live trigger read **17%**
(roughly one failed run in six) against pre-fix code.

Do not dismiss it. **Left sidebar → Executions → filter Status: Failed**, open a failed
`sendDailyReport` run, and read the error — it names the failing line. Re-check after any
redeploy, since a rate shown in the panel is history against whatever code was live at the time.

---

## Column-order rule

`EXPECTED_HEADERS` and the `appendRow` array in `doPost` **must stay in the same order**, and new
columns **must be appended at the end**. Everything downstream (`rebuildDashboard`,
`sendDailyReport`) looks columns up by name into a `col[]` map built from row 1 — inserting a
column in the middle silently misaligns every historical row.

`client_ts` and `seq` were appended on 2026-08-26 for exactly this reason. Rows written before
that date have both blank; treat blank `client_ts` as "fall back to the `timestamp` column".

`question_id` was appended on 2026-11-03 (contract QUESTION-ID) as column R, after `seq`, the same way. Rows
written before the redeploy have it blank. It names the question a `question_answered` row was about: a game's own
id, or `h` + the 8-hex FNV-1a hash of the question's text (`schools/assets/analytics.js`; the text itself is never
sent). `python -X utf8 scripts/decode-question-ids.py <slug>` prints each id beside its question.

`detail` was appended on 2026-11-07 (contract ROOM-TIMES) as column S, after `question_id`, the same way. Rows
written before the redeploy have it blank. Only the escape-room engine sends it (`escape-rooms/assets/engine.js`); on
`game_completed` it holds the outcome, wrong settings, hints, the clock's time used, the seconds played and each lock's
opening second, in the format canon §1.3 records.

---

## Why `client_ts` and `seq` exist

`doPost` stamps `new Date().toISOString()` into the `timestamp` column on **arrival**. Events are
sent fire-and-forget (`fetch` with `no-cors` / `sendBeacon`) and regularly arrive out of order —
so a `game_completed` can land *before* the `question_answered` that caused it. Observed in the
live data: 52dle logged completion 0.6s before its answer event, despite firing them in the
correct order in code.

`client_ts` is stamped in the browser at the moment the event happens, and `seq` is a
per-page-load counter that breaks same-millisecond ties. **Sort by `client_ts` then `seq` for any
per-question or sequence analysis.** The `timestamp` column remains useful only for "when did
this reach the sheet".
