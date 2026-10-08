# GA4 country figures in the events Sheet: setup

`docs/apps-script-ga4-country.js` copies GA4's daily figures by country into two new tabs of the
**MaffsGames Events** spreadsheet, once a day. Jon's ruling (8 Oct 2026): aggregates from GA4's Data
API only. Nothing new is collected from students, and the site, `analytics.js`, the events endpoint and
the privacy page do not change. GA4 already works out each visit's country from its IP address; this
script only reads the totals GA4 already holds.

The repo file is a copy. Nothing runs until it is pasted into Apps Script, as below. Tested without
network by `scripts/test-ga4-country.py` (in CI).

## Before you start: two facts that matter

- **This goes into the live analytics project.** The Sheet's **Extensions → Apps Script** opens the
  project that serves the events endpoint (`docs/apps-script-redeploy.md`). That is fine: the new file
  is a separate script file, none of its names clash with `Code.gs` (the test checks this), and
  **nothing needs deploying**. A daily trigger runs the saved code, not the web app deployment.
  **Do not use Deploy at any point in these steps.**
- **No Google Cloud setup and no service account are needed.** An Apps Script project bound to a Sheet
  has a default Cloud project, and adding the advanced service switches the API on in it. Your own
  Google account reads the GA4 property, so it needs at least Viewer access there (as the owner, you
  have it).

## Steps

1. Open the **MaffsGames Events** spreadsheet. Choose **Extensions → Apps Script**. Check that this
   is the live project: `Code.gs` contains `function doPost`.
2. In the left bar, click **+** next to **Services**. Choose **Google Analytics Data API**. Leave
   the identifier as `AnalyticsData` and click **Add**.
3. Click **+** next to **Files**, choose **Script** and name it `ga4-country`. Delete the empty
   function it starts with. Paste in the whole of `docs/apps-script-ga4-country.js` from the repo.
   Click **Save** (the disk icon).
4. **Check the property ID.** In the function menu at the top, choose `ga4CountryCheckProperty` and
   click **Run**. The first run asks for authorisation: choose your account, click **Advanced**, then
   **Go to … (unsafe)** (this is your own script), then **Allow**. The new permission is "See and
   download your Google Analytics data". The log (View → Logs, or the panel at the bottom) should end with
   `OK: properties/528531831 holds stream 13911036386 (maffsgames.co.uk).` If it throws an error
   instead, stop: the property ID is wrong (see "If something fails").
5. **Backfill once.** Choose `ga4CountryBackfill` and click **Run**. It fills both tabs from
   1 Sep 2026 to yesterday and logs how many rows it wrote. The two tabs, **GA4 country daily** and
   **GA4 country events**, appear at the end of the tab bar. The events tab stays first and is not
   touched.
6. **Daily trigger.** Choose `ga4CountrySetupTrigger` and click **Run**. It adds one trigger:
   `ga4CountryDaily`, every day between 06:00 and 07:00 UK time. It replaces only its own trigger, so the
   07:00 report trigger is kept. You can check this under **Triggers** (the clock icon): there should be
   one `sendDailyReport` and one `ga4CountryDaily`. (Adding the trigger by hand there works too: function
   `ga4CountryDaily`, time-driven, day timer, 6am to 7am. Never have two.)
7. Check the next morning that the daily run worked. **Executions** (the list icon) should show
   `ga4CountryDaily` as Completed. Your 07:00 email should also still arrive: step 4's authorisation
   covers the existing trigger too.

That is all. To remove it later: delete the `ga4CountryDaily` trigger and the `ga4-country` file. The
two tabs can then be deleted by hand.

## What the two tabs hold

Every figure is GA4's, for one UK calendar day (the property's reporting time zone; see the last
section).

**GA4 country daily**: one row per date and country.

| Column | Meaning |
|---|---|
| date | the day, yyyy-mm-dd, newest first |
| country | as GA4 places the visitor's IP address; `(not set)` = it could not place it |
| activeUsers | GA4's "users" that day (see the warning below) |
| sessions | GA4's sessions |
| engagedSessions | sessions that lasted 10 seconds or more, or saw 2+ pages, or a key event |
| eventCount | every event, of every kind (page views, scrolls, game events …) |

**GA4 country events**: one row per date, country and event, for four events only: `page_view`,
`game_started`, `question_answered`, `game_completed`. Columns: date, country, eventName, activeUsers,
eventCount. A country with no `question_answered` row that day had no answered questions in GA4.

**How it stays right.** GA4 keeps revising a day's figures for about 48 hours. So each morning the
script fetches the **last three complete days** and replaces those days' rows outright: running it twice
never duplicates anything, and no older day is ever changed. (`ga4CountryBackfill` can be re-run at any
time on the same terms: it replaces 1 Sep to yesterday.)

## How to read it

**"Users" are GA4's estimate, not a head count.** The site runs GA4 cookieless (`storage: 'none'`,
canon §1.1), so you might expect every page load to count as a new user. The backfill of 8 Oct 2026 says
otherwise: from 1 Sep to 7 Oct the United Kingdom had 1,116 sessions from 763 users, and sessions
exceed users in 59 of 262 rows. So GA4 links some page loads within a day. How it does that without
cookies is not documented here. Also, `activeUsers` can be 0 on a row that has a session. Two safe
rules: never add daily `activeUsers` across days and call it people, and use `engagedSessions` as the
main measure.

**Separating real play from crawlers.** A crawler loads a page and leaves: it fires `page_view`, never
a game event, and its session is not engaged. So:

- **Real use** = `game_started`, `question_answered` and `game_completed` counts, and
  `engagedSessions`. `question_answered` is the strongest evidence: someone read a question and
  answered it.
- **Probably crawlers** = a country with many `page_view` users, few or no `question_answered`, and
  `engagedSessions` far below `sessions`. A sudden one-day spike from a single country with no game
  events is the classic shape.
- A useful ratio per country: **question_answered eventCount ÷ page_view eventCount**. Real classroom
  traffic is well above zero; crawler traffic is at or near zero.

**Three cautions before drawing conclusions.**

1. **GA4 sees less than the Sheet does.** Ad and tracker blockers stop GA4 more often than they stop
   the Sheet's own endpoint. So GA4's totals across all countries will be **below** the events tab's
   counts for the same day. Compare one day's `question_answered` total in both: the ratio tells you
   how much of real play GA4 is seeing. The country split is a **share**, not a full count.
2. **Country is the network's location, not the student's.** VPNs, mobile networks and some school
   and college networks route traffic through another country. Read a handful of visits from an
   unexpected country as noise, not a market.
3. **Small counts can be withheld.** If Google signals is switched on for the property, GA4 can hide
   very small rows (thresholding). The script logs a line when GA4 says it has done this.

To see one day at a glance: select the **GA4 country events** tab, then **Insert → Pivot table**. Use
rows = country, columns = eventName, values = SUM of eventCount, and filter = date.

## If something fails

Apps Script emails you when a trigger run fails (a daily digest, by default). The message names the
error. The usual ones:

| Error says | What it means | Do this |
|---|---|---|
| `AnalyticsData is not defined` | step 2 was missed | add the service (step 2), save, run again |
| "Authorization is required" or a permissions prompt | a new permission has not been granted | run `ga4CountryCheckProperty` from the editor and allow it (step 4) |
| "User does not have sufficient permissions for this property" | wrong property ID, or your account cannot read it | GA4 → Admin → Property details shows the property ID; it must be 528531831. If it is different, tell Code Claude: do not edit the file by hand |
| `… has no maffsgames.co.uk events from stream 13911036386` | `ga4CountryCheckProperty` found the property, but it is not the site's | the same: stop, report the ID GA4 Admin shows |
| "Google Analytics Data API has not been used in project … or it is disabled" | the project uses its own Cloud project, not the default one | open the link in the message, click **Enable**, wait five minutes, run again |
| "Exhausted property tokens" / quota | GA4's daily request allowance (200,000 tokens; one run uses a few dozen) is spent | wait: it resets daily (Pacific time). The next run re-fetches three days, so one missed day fills itself. If more than three days were missed, run `ga4CountryBackfill` once |
| `GA4 returned no rows … Not replacing them` | GA4 sent nothing at all for the three days, though the tab has rows for them | a GA4 delay or fault; the tab is unchanged. Run `ga4CountryDaily` later |
| `… not this script's headers: not overwriting it` | a tab already has that name but different column headings | rename that tab (it is someone's own), run again |
| "Lock timeout" | two runs at once (a manual run during the trigger's) | run again a minute later |

**Time zone.** The script asks GA4 for the last three complete UK days. GA4 reports dates in the
property's own reporting time zone: check it under GA4 → Admin → Property details. If it is not United
Kingdom, the dates in the tabs are that zone's days, and 06:00 UK may come before "yesterday" has ended
there. Tell Code Claude rather than change it in the file.
