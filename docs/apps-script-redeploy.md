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
