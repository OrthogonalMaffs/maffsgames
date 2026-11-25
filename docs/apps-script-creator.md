# Today's deal: the Creator sheet and its script (Jon)

For MaffsCards' "Today's deal" (contract DAILY-DEAL, 25 Nov 2026). You play today's deal, type your result into one
row of a Google Sheet, and the game shows it a few minutes later. No page edit and no visit to GitHub.

**This is a new Sheet with its own small script.** It has nothing to do with the analytics script
(`docs/apps-script-endpoint.js`) or the counts script (`docs/apps-script-counts.js`): do not paste it into either.

How it works: the script starts the repository's `maffscards-daily` workflow with your four values. The workflow
checks them (`scripts/set-maffscards-daily.py`) and writes `games/maffscards/daily.json`, which the game reads.

The file in this repo that you paste from: `docs/apps-script-creator.js`. Nothing in it is secret.
**The GitHub token in step 3 is a secret. It goes in one place only: the script's Script Properties (step 4).
Never paste it into the Sheet, the code, a chat or an e-mail.**

Do these steps after the DAILY-DEAL pull request is merged: the token test in step 6 needs the workflow to exist.

## 1. Make the Sheet

1. Go to <https://sheets.new> (signed in to the Google account you use for MaffsGames).
2. Click the title ("Untitled spreadsheet") and rename it **MaffsGames Creator**.
3. In row 1 type these four headers, one per cell: A1 `Date`, B1 `Result`, C1 `Rounds`, D1 `Line`.
4. Optional: type `Sent` in E1. The script writes what happened in column E.
5. Click **File → Settings**. Check **Time zone** is **(GMT+00:00) London**. If it is not, choose it and click **Save settings**.

## 2. Paste the script

1. In the Sheet, click **Extensions → Apps Script**. A new tab opens.
2. Click the title ("Untitled project") and rename it **MaffsGames Creator**.
3. Select everything in `Code.gs` and delete it.
4. Open `docs/apps-script-creator.js` from the repo, copy all of it, and paste it into `Code.gs`.
5. Click **Save** (the disk icon).

## 3. Create the GitHub token

1. Go to <https://github.com/settings/personal-access-tokens/new> (signed in to your own GitHub account).
2. **Token name:** `MaffsGames Creator sheet`.
3. **Resource owner:** choose `OrthogonalMaffs` (the organisation that holds the repository), not your own name.
   If `OrthogonalMaffs` is not in the list, or GitHub later says the token is "pending approval", stop and tell Claude.
4. **Expiration:** choose **Custom** and pick the date one year from today.
5. **Repository access:** choose **Only select repositories**, then pick **OrthogonalMaffs/maffsgames** and nothing else.
6. **Permissions → Repository permissions:** find **Actions** and set it to **Read and write**. Leave every other permission as it is.
   (GitHub adds **Metadata: Read-only** by itself. That is expected.)
7. Click **Generate token**.
8. Click the copy icon beside the token (it starts `github_pat_`). GitHub shows it once only: go straight to step 4.

## 4. Store the token

1. Back in the Apps Script tab, click the **gear icon** (Project Settings) in the left column.
2. Scroll down to **Script Properties** and click **Add script property**.
3. **Property:** `GITHUB_TOKEN` (exactly that, in capitals).
4. **Value:** paste the token.
5. Click **Save script properties**.
6. Write the token's expiry date in your calendar. When it expires, column E will say `error 401: Bad credentials`:
   repeat steps 3 and 4.

## 5. Install the trigger

1. Click the **clock icon** (Triggers) in the left column, then **Add Trigger** (bottom right).
2. **Choose which function to run:** `creatorEdit`.
3. **Choose which deployment should run:** `Head`.
4. **Select event source:** `From spreadsheet`.
5. **Select event type:** `On edit`.
6. Click **Save**.
7. Google asks you to review permissions: choose your account, then **Advanced** →
   **Go to MaffsGames Creator (unsafe)** → **Allow**. (It says "unsafe" only because you wrote the script yourself.)
8. It should list exactly two permissions:
   "**View and manage spreadsheets that this application has been installed in**" (this spreadsheet only) and
   "**Connect to an external service**" (GitHub).
   **If Google asks for anything else, stop: do not click Allow, and tell Claude which permission it named.**

## 6. Check the token (sends nothing)

1. Click **Editor** (the `<>` icon). In the function drop-down at the top choose **checkToken** and click **Run**.
2. Look at the **Execution log** at the bottom. It should read
   `OK: the token can see the maffscards-daily workflow. Script version 2026-11-25-a`.
3. If it reads `Not OK (404)`, the token cannot see the repository or the pull request is not merged yet. If it reads
   `Not OK (401)`, the token was pasted wrongly: repeat step 4. Anything else: tell Claude the exact text.

## 7. A first test row

1. Open <https://maffsgames.co.uk/games/maffscards/> and play **Play today's deal**. Note whether you won and the rounds.
2. In the Sheet, in row 2: click A2 and press **Ctrl+;** (today's date). Type `won` or `lost` in B2. Type the rounds in C2.
3. Leave D2 empty this first time. (The game then picks a line from its own list.)
4. Within a few seconds E2 should read `sent 08:15` (the time). If it reads `not sent: …` or `error …`, it says why.
5. Wait about three minutes, then refresh the game. Under **Today's deal** it should show a line about your result.
   (If it still says you have not played after ten minutes, open GitHub → **Actions** → **maffscards-daily** and
   tell Claude what the newest run says.)

## 8. Every day after that

1. Play today's deal.
2. Add a row: the date, `won` or `lost`, the rounds. Rows can go anywhere below row 1; a new row each day keeps a record.
3. If you want your own line, type it in column D. At most 240 characters, plain text. Write `{N}` where the number of
   rounds should appear. A line that is too long, or has `<` or `>` in it, is skipped and the game uses one of its own.
   When you won and your line has no `{N}`, the game adds "Jon took 14 rounds." after it.
4. Each edit to a finished row sends it again, so to correct a mistake just change the cell. To add a line later, type it in D.
5. The date must be today or yesterday (UK). The game shows a result only on that result's own date, so yesterday's
   needs no clearing: at midnight the panel goes back to "Jon hasn't played today's deal yet."

## 9. The fallback, from a phone (no Sheet needed)

1. Open <https://github.com/OrthogonalMaffs/maffsgames/actions/workflows/maffscards-daily.yml> (signed in).
2. Tap **Run workflow**.
3. Fill in the same four fields: the date as `2026-11-26`, `won` or `lost`, the rounds, and the line (or leave it empty).
4. Tap the green **Run workflow** button. A green tick a minute later means the result is on its way to the game;
   a red cross means it was refused, and the run's summary says why.

## What the messages in column E mean

- `sent 08:15`: GitHub accepted it at that time. The workflow then checks it and writes the file.
- `not sent: …`: the script saw a problem in the row (the date, the result or the rounds) and sent nothing. Fix the cell.
- `not sent: no GITHUB_TOKEN in Script Properties`: step 4 has not been done, or the name is misspelt.
- `error 401: Bad credentials`: the token has expired or was pasted wrongly. Steps 3 and 4.
- `error 403` or `error 404`: the token cannot use Actions on the repository. Check step 3, lines 5 and 6.
- `error 422`: GitHub did not accept the fields. Tell Claude the exact text.
