/**
 * MaffsGames Creator: sends Jon's result for MaffsCards' "Today's deal" to GitHub (contract DAILY-DEAL, 25 Nov 2026).
 *
 * Bound to the Google Sheet "MaffsGames Creator". Row 1 holds the headers: Date | Result | Rounds | Line.
 * When a row below it is edited and has its Date, Result and Rounds filled in, this starts the repository's
 * maffscards-daily workflow with those values. The workflow validates them and writes games/maffscards/daily.json;
 * the game shows the result a few minutes later. Column E of the row gets "sent HH:MM", or the error.
 *
 * Setting it up, step by step: docs/apps-script-creator.md.
 *
 * NOTHING IN THIS FILE IS SECRET. The GitHub token is never written here: it is read from the script's own
 * Script Properties (Project Settings), under the name GITHUB_TOKEN.
 *
 * It needs two permissions: this spreadsheet only (the @OnlyCurrentDoc line below), and connecting to an external
 * service (GitHub). If Google asks for anything else, stop and tell Claude which permission it named.
 *
 * @OnlyCurrentDoc
 */

const VERSION = '2026-11-25-a';
const DISPATCH_URL = 'https://api.github.com/repos/OrthogonalMaffs/maffsgames/actions/workflows/maffscards-daily.yml/dispatches';
const TIME_ZONE = 'Europe/London';
const COL = { DATE: 1, RESULT: 2, ROUNDS: 3, LINE: 4, STATUS: 5 };

/**
 * The installable trigger's function (Triggers: From spreadsheet, On edit). Not named onEdit on purpose: a simple
 * onEdit trigger is not allowed to connect to GitHub.
 */
function creatorEdit(e) {
  if (!e || !e.range) return;
  const sheet = e.range.getSheet();
  const first = e.range.getRow();
  const last = e.range.getLastRow();
  // Only edits to columns A to D count: the status this script writes in column E never sends anything.
  if (e.range.getColumn() > COL.LINE) return;
  for (let row = Math.max(first, 2); row <= last; row++) sendRow_(sheet, row);
}

/** Send one row, if its Date, Result and Rounds are all filled in, and write what happened in column E. */
function sendRow_(sheet, row) {
  const v = sheet.getRange(row, COL.DATE, 1, COL.LINE).getValues()[0];
  if (v[0] === '' || v[1] === '' || v[2] === '') return;   // not finished yet: say nothing
  const status = sheet.getRange(row, COL.STATUS);
  try {
    const inputs = {
      date: dateText_(v[0]),
      result: String(v[1]).trim().toLowerCase(),
      rounds: roundsText_(v[2]),
      line: String(v[3] === null || v[3] === undefined ? '' : v[3]).trim(),
    };
    const problem = problemWith_(inputs);
    if (problem) { status.setValue('not sent: ' + problem); return; }
    const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
    if (!token) { status.setValue('not sent: no GITHUB_TOKEN in Script Properties (runbook step 4)'); return; }
    const reply = UrlFetchApp.fetch(DISPATCH_URL, {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: 'Bearer ' + token,
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
      },
      payload: JSON.stringify({ ref: 'main', inputs: inputs }),
      muteHttpExceptions: true,
    });
    const code = reply.getResponseCode();
    if (code === 204) {
      status.setValue('sent ' + Utilities.formatDate(new Date(), TIME_ZONE, 'HH:mm'));
    } else {
      status.setValue('error ' + code + ': ' + githubMessage_(reply));
    }
  } catch (err) {
    status.setValue('error: ' + String(err && err.message ? err.message : err).slice(0, 200));
  }
}

/** A date cell (or typed text) as YYYY-MM-DD. */
function dateText_(value) {
  if (Object.prototype.toString.call(value) === '[object Date]') {
    return Utilities.formatDate(value, SpreadsheetApp.getActive().getSpreadsheetTimeZone(), 'yyyy-MM-dd');
  }
  const text = String(value).trim();
  const uk = text.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);       // 26/11/2026 typed as text
  if (uk) return uk[3] + '-' + ('0' + uk[2]).slice(-2) + '-' + ('0' + uk[1]).slice(-2);
  return text;
}

/** A whole number as text ("14", never "14.0"); anything else as typed, for the workflow to refuse. */
function roundsText_(value) {
  if (typeof value === 'number' && Math.floor(value) === value) return String(value);
  return String(value).trim();
}

/** A plain-words reason not to send, or '' if the row looks right. The workflow checks everything again. */
function problemWith_(inputs) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(inputs.date)) return 'the date is not a date (use the date picker, or type 2026-11-26)';
  if (inputs.result !== 'won' && inputs.result !== 'lost') return 'Result must be won or lost';
  if (!/^\d+$/.test(inputs.rounds)) return 'Rounds must be a whole number';
  const n = Number(inputs.rounds);
  if (n < 10 || n > (inputs.result === 'won' ? 100 : 200)) return 'Rounds must be 10 to 100 for a win, 10 to 200 for a loss';
  return '';
}

/** GitHub's own words for a failure, without anything of ours in it. */
function githubMessage_(reply) {
  let text = reply.getContentText() || '';
  try { text = JSON.parse(text).message || text; } catch (err) { /* not JSON: keep the text */ }
  return String(text).slice(0, 200);
}

/** Run by hand from the editor (runbook step 6): checks the token reaches the repository, and sends nothing. */
function checkToken() {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) { Logger.log('No GITHUB_TOKEN in Script Properties.'); return; }
  const reply = UrlFetchApp.fetch(DISPATCH_URL.replace(/\/dispatches$/, ''), {
    headers: { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' },
    muteHttpExceptions: true,
  });
  const code = reply.getResponseCode();
  Logger.log(code === 200 ? 'OK: the token can see the maffscards-daily workflow. Script version ' + VERSION
    : 'Not OK (' + code + '): ' + githubMessage_(reply));
}
