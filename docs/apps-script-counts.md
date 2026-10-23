# Answer counts: creating and deploying the counts script (Jon)

For the "N questions answered since September" lines (contract ANSWER-COUNTS, 23 Oct 2026).

**This is a new, separate Apps Script project.** Do not paste it into the analytics project (`docs/apps-script-endpoint.js`):
the point is that counting can never slow the script that records events. It only reads the Sheet, through the
**Google Sheets advanced service** (not `SpreadsheetApp`, which needs the read-and-write permission). It asks for one
permission, read-only access to your spreadsheets (Google words it "See and download your spreadsheets").
**If Google asks for anything else, stop and tell Claude which permission it named.**

Files in this repo that you paste from: `docs/apps-script-counts.js` (the code) and
`docs/apps-script-counts.appsscript.json` (the settings). Nothing in either is secret.

## 1. Get the Sheet's id

1. Open the Sheet called **MaffsGames Events** in Google Drive.
2. Look at the address bar: `https://docs.google.com/spreadsheets/d/`**`LONG_ID_HERE`**`/edit`.
3. Copy the long id between `/d/` and `/edit`.

## 2. Create the project

1. Go to <https://script.google.com> and click **New project**.
2. Click the title ("Untitled project") and rename it **MaffsGames Answer Counts**.
3. In the editor, select everything in `Code.gs` and delete it.
4. Open `docs/apps-script-counts.js` from the repo, copy all of it, and paste it into `Code.gs`.
5. Find the line `const SHEET_ID = 'PASTE_THE_SHEET_ID_HERE';` and replace the text inside the quotes with the id from step 1.
   Also check the next line, `const SHEET_NAME = 'Sheet1';`: it is the name of the **tab** at the bottom of the Sheet (the file is called
   MaffsGames Events, but its tab is `Sheet1`). If the tab has another name, put that name in the quotes.
6. Click **Save** (the disk icon).

## 3. Set the permissions and time zone (the settings file)

1. Click the **gear icon** (Project Settings) in the left column.
2. Tick **Show "appsscript.json" manifest file in editor**.
3. Click **Editor** (the `<>` icon), then click `appsscript.json` in the file list.
4. Select everything in it, delete it, and paste the whole of `docs/apps-script-counts.appsscript.json`.
   (It lists the read-only permission and switches on the Sheets service.)
5. Click **Save**.
6. **Check the Sheets service is on:** click `Code.gs`, then the **+** next to **Services** in the left column. If
   **Google Sheets API** is already listed there, do nothing. If it is not, choose **Google Sheets API**, set the
   version to **v4**, leave the identifier as `Sheets`, and click **Add**. (The settings file normally does this for you;
   the symptom of it being off is `ReferenceError: Sheets is not defined`.)

## 4. Count the school year so far (the first run)

1. In the editor, click `Code.gs`. In the function drop-down at the top choose **backfill** and click **Run**.
2. Google asks you to review permissions: **Review permissions**, choose your account, then **Advanced** →
   **Go to MaffsGames Answer Counts (unsafe)** → **Allow**. (It says "unsafe" only because you wrote the script yourself.)
   The only permission listed should be the read-only one ("See and download your spreadsheets").
   If you already granted it earlier, Google may not ask again. If the run then fails with a permissions message, click
   the **clock icon → Executions** and tell Claude the exact text.
   (Some accounts also ask to switch on the Google Sheets API in the project's Google Cloud project: **Enable** it.)
3. When it finishes, look at the **Execution log** at the bottom. The last line reads like
   `read 48210 rows in 31204 ms; last row 53901 of 53901; caught up: true`.
4. If it says `caught up: false`, click **Run** again (it carries on from where it stopped) until it says `true`.
5. **Write down for Claude:** the total number of rows and how long the first run took. (If the whole first count needed
   more than one run, say so: that is a stop condition in the contract and Claude will re-plan.)
6. Choose **preview** in the function drop-down and **Run**. The log shows the figures the site would get:
   `{"as_of":"…","since":"2026-09-01","total":…,"games":{…}}`.

## 5. Keep it up to date (a trigger, made in the editor, not in code)

1. Click the **clock icon** (Triggers) in the left column, then **Add Trigger** (bottom right).
2. Choose function **updateCounts**; deployment **Head**; event source **Time-driven**; type **Minutes timer**;
   interval **Every 5 minutes**. Click **Save**.
3. Later, open **Executions** (left column) and look at the **Duration** of an `updateCounts` run: it should be a few
   seconds at most. **Write down one duration for Claude.**

## 6. Deploy it as a web address

1. Click **Deploy** (top right) → **New deployment**.
2. Click the gear next to "Select type" → **Web app**.
3. Description: `answer counts`. **Execute as: Me.** **Who has access: Anyone.** (Anyone, because visitors' browsers
   fetch it; it returns only totals per game, nothing else.)
4. Click **Deploy**, authorise if asked, and **copy the Web app URL**. It ends in `/exec`.

## 7. Check it

1. Open the `/exec` URL in a private window. You should see JSON beginning `{"as_of":"…","since":"2026-09-01","total":…`.
2. Add `?version=1` to the address: it should show `{"version":"2026-10-23-a"}`. That is how you tell which code is live.

## 8. Tell Claude

Send: **the `/exec` URL**, the **row count and time of the first full count** (step 4), and **one `updateCounts` duration**
(step 5). Claude fills the URL into the loader and the daily job, and carries on.

## Changing the code later

Edit `Code.gs`, **Save**, then **Deploy** → **Manage deployments** → the pencil → **Version: New version** → **Deploy**.
The address stays the same. Bump `SCRIPT_VERSION` when you do, so `?version=1` shows the change landed.

## What it counts (so the page's claim is true)

- Rows whose `event` is `question_answered`, grouped by `game_slug`, for the school year: from 1 September (Europe/London)
  to the next 1 September, when the counts restart on their own.
- The event's time is the browser's `client_ts` when it is within a day of the row's arrival time, otherwise the arrival time.
- Your own play on the live site is counted. Nothing is filtered.
- `total` is the sum of every game's count, including the escape rooms (their slugs begin `escape-`).
- If a run is cut off by Google's time limit it saves its place and the next run carries on. While the first count is
  unfinished the address returns `"as_of": null`, and the site shows nothing rather than part of a count.
- The Sheet is read through the Sheets API, so a timestamp cell Sheets has turned into a date is read on the spreadsheet's
  own time zone, and a cell left as text is read as the ISO time it holds. Both give the same instant.
- Reset (only if the numbers ever look wrong): run **resetCounts**, then **backfill** until it says `caught up: true`.
