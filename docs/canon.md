# MaffsGames — Canonical Data Document

*Source of truth for platform facts. Update here first — except the per-game roster, which lives in `.claude/rules/game-roster.md`. See below.*

Last updated: 3 October 2026

> **Repository history.** This repository started fresh on 2 Oct 2026. Any commit hash or PR number
> from before then, here or in `CLAUDE.md` and `docs/todo.md`, refers to
> `OrthogonalMaffs/maffsgames-archive` (archived, read-only). The 25 Sep warning that stood here, about
> the unmerged branch `claude/wizardly-gauss-uxv4v4`, is resolved: it was merged on 24-25 Sep with both
> sides kept (todo, "Done") and `MIN_QUESTIONS_FOR_LEADERBOARD` no longer exists anywhere in the code.

**What is authoritative where.** This document is the source of truth for platform facts — IDs, policies, structure, curriculum coverage, the escape rooms and the backlog. It deliberately does **not** hold the per-game table: that is `.claude/rules/game-roster.md`, which is maintained and has all 93 rows with descriptions. Canon carried its own 60-row copy until 8 September 2026, by which point it was 33 games behind. Do not reintroduce a second roster here — see §4.

| **Property** | **Value** |
| --- | --- |
| Live site | maffsgames.co.uk |
| Repository | github.com/OrthogonalMaffs/maffsgames |
| GA4 Measurement ID | G-992JLHLP2D |
| Sheets Endpoint | Google Apps Script (see docs/apps-script-endpoint.js) |
| Contact | contact@maffsgames.co.uk |
| Total games | **96 live on the portal** (9 Oct 2026, contract DOCS-9OCT: `factor-theorem` relisted under SR-21, A-Level only; contract RELIST-SR: `screening-room` relisted under SR-21; 8 Oct, contract RELIST-3: `just-pythag-it-bruv` listed on Jon's approval, `expectation-station` and `truth-buster` relisted under SR-21), plus **1 roster game live but unlisted** pending its audit fixes (`glorious-gantt`; canon SR-20 and SR-21, the roster's "Unlisted" section). `regression-rumble` is **withdrawn** behind a `noindex` holding page pending its data rebuild (todo §1.26). Per-game detail in `.claude/rules/game-roster.md` (97 numbered rows, plus a Withdrawn section). `games/` holds **99 directories** — the extras are `regression-rumble` (withdrawn, a holding page) and `the-perfect-prank`, the unlisted escape-room prototype, deliberately not on the portal and not in the roster. Because the roster is where `scripts/check-site.py` reads each game's levels, that game is only ever loaded bare; it is recorded under `roster_exceptions` in `scripts/checker-allowlist.json` so the gap is declared rather than silent |
| Escape rooms | **8 live at `/escape-rooms/`**, indexed, in the sitemap and led from the front page. Not counted in the 96. **Two more are built but withdrawn** (`it-vengeance`, `car-trap`) behind `noindex` holding pages at their own URLs until each one's voice rewrite is done. Teacher pages stay `noindex` deliberately — they hold every answer. Full detail in **§11**; the live work is `docs/escape-room-voice-rewrite.md` |
| Parent guides | **20 at `/parents/`**, plus the hub: 21 indexed URLs, in the sitemap and linked from the portal footer. Ported from MathsWins on 28 Sep 2026 and corrected again on 29 Sep against Jon's approved wording; the findings are in `docs/audit-parent-guides.md` and the fix-by-fix record is in `docs/migrate-parent-guides.md`. `averages` links Distinctly Average at `?level=ks3`. The section has one template: `parents/guide.css` and `parents/guide.js`, portal theme, adult register (the game theme, §7.5, does not apply -- the reader is the parent). **GCSE tier badge:** one component in `parents/guide.js` (its `TIERS` table, built from bold parts of `data/dfe-gcse-parts.json`) on exactly four guides and their hub cards; partly-Higher guides mark each Higher section in the body. `scripts/verify-parent-guides.py` reads every checked value back from the pages. **`scripts/check-site.py` does not discover these pages**: `build_page_list()` globs `games/` and `escape-rooms/` and otherwise walks a hard-coded list of root pages |

---

# 0. Mission and priorities

## 0.1 The mission
MaffsGames exists to get students through maths.

The priority audience is students working at grades 1–3, and post-16 resitters above all, for whom a grade 4 opens doors that are otherwise shut. The format is fun and low-stakes because these students have usually learned to dread maths, not because they cannot do it. Sites such as Hannah Kettle Maths and Dr Frost serve able students well; MaffsGames is for the students who struggle.

The existing library, KS3 to Level 4, stays live and maintained. New effort goes to the struggling student first.

The gatekeeper is still a teacher, now typically a resit lecturer in an FE college. The test: within seconds of landing, would they trust this and share it?

## 0.2 Priority order

**BUILD FREEZE (Jon, 6 Oct 2026).** No new builds (games, modes, stages) until the exit bar is met:
1. every live game has a verifier in CI;
2. every CRITICAL and HIGH in the findings register fixed;
3. shared checks green site-wide (answer lock, level resolver, served bank size, SR-14 fields, B11 parser);
4. every level serves 40+;
5. every unlisted game relisted or archived;
6. one sweep of the already-verified games for true wrong options and unstated conventions.

**One named exception (Jon, 9 Oct 2026, 00:25): Simultaneous Solver Stage 5 only** (word problems, the two
equations built from tiles; merged #203). No other build is excepted: a further exception needs Jon's own named
ruling, never a contract's inference. The register's exit-bar dashboard
(`docs/audits/REGISTER.md`) shows how far the site is from each point.

When deciding what comes next:

1. **Correctness on live games.** Wrong maths or a broken game, first. A struggling student is the least able to spot a wrong answer.
2. **Work for the priority audience.** Grade 1–3 and resit content, and making it findable by the people who teach it.
3. **Gatekeeper trust.** Anything that makes the portal look less credible to a resit lecturer.
4. **Depth of the existing library.** Question-bank quality and quantity for live games.
5. **Level 4 / Further Maths.** Jon's specialism; maintained, not expanded ahead of the above.
6. **New builds for other audiences.**

This is the only copy in the repo. The claude.ai Project instructions mirror it; if the two disagree, this one wins.

## 0.3 Standing rulings

Jon's settled precedent, in one citable list (3 Oct 2026). **Before stopping a contract for a
decision, check this list.** If a ruling covers it, apply it and say so in the PR description
("SR-n applied: …"). Stop only for what no ruling covers, or for anything on the "Still stops for
Jon" list below. Where a ruling and a canon section say more, the section has the detail.

| # | Ruling | Date | Source |
|---|---|---|---|
| SR-1 | **Unstated precision.** If a typed answer isn't exact, the question states its precision; the default for a non-money answer is "Give your answer to 1 decimal place." Keys are computed exactly (no floating-point drift) and rounded half up. *Except* a value read from a drawn graph, which keeps §7.1.2's capped band. | 3 Oct 2026 | §7.1.2, §7.1.3; todo §1.36; PR #12 (split-it recipes and speed) |
| SR-2 | **Money** follows §7.1.3 through `MaffsAnswer.money()`: pence answers to exactly 2 d.p.; a whole-pound key needs no .00; a leading £ or € is optional. A typed answer that needs no rounding is marked with `MaffsAnswer.exact()`. | 3 Oct 2026 | §7.1.3; PR #4, PR #12 |
| SR-3 | **A right value in the wrong form** (1250.7; 333.33 when 1 d.p. is asked) gets the format message and is never marked right or wrong: no score, no penalty, no event. `MaffsAnswer.exact()` has no wrong form (nothing was asked to be rounded). | 3 Oct 2026 | §7.1.3; PR #12 |
| SR-4 | **Distractors.** Each comes from a nameable student error. Four distinct options wherever the student chooses from a list; a two-way comparison (Pack A / Pack B) keeps its two. None is equal in value to the key, unless the ask names the form that tells them apart (§7.1). Don't reuse one error type across a paper where an alternative exists. | 3 Oct 2026 | §7.1 (B11); §7.1.2; PR #7 (paper1 NI distractors), PR #11 |
| SR-5 | **Comparison questions never tie.** The options differ by at least the smallest unit shown (1p, 0.1, …). Draw from the values that qualify, never a redraw loop (no rejection sampling: §12, "No rejection sampling"; tier 2). | 3 Oct 2026 | PR #12 (split-it Best Value) |
| SR-6 | **Wording, picture and key agree.** Where one disagrees, change it to match the other two. | 3 Oct 2026 | PR #11 (Circle Theorem Spotter Q19) |
| SR-7 | **Tax, NI and student loan figures** in a game are the teaching year's, as in `scripts/uk_rates.py`, and the game is registered in `scripts/check-tax-year.py`. Scripts never restate a rate. | 3 Oct 2026 | §7.1.4; PR #7, PR #8 |
| SR-8 | **When a key changes,** recompute every dependent answer, distractor and worked line. | 3 Oct 2026 | PR #4 (tax-theft), PR #11 |
| SR-9 | **Bugs found outside the task are logged, not fixed,** except a live wrong answer in the same game that one of these rulings fixes: fix it and list it in the PR. | 3 Oct 2026 | todo START ("a live bug is never a decision item") |
| SR-10 | **Whole items scale by whole numbers.** A recipe with an ingredient that comes in whole items (eggs) is scaled only by a whole-number factor (×2, ×3). Draw its scale factors from whole numbers only (no redraw loop, SR-5); the game's verifier checks every whole-item amount it scales is a whole number. | 3 Oct 2026 | todo §1.47; split-it's GCSE Pancakes (3.3 eggs) |
| SR-11 | **Age-neutral level labels.** A student-facing level label never names a year group or key stage: "Year 6" becomes "Starter", "KS3" becomes "Foundation"; "GCSE" and every level above it keep their names. Start screens and other student-facing copy carry no year-group or key-stage wording (no "Year 7", "primary", "secondary school", "when your teacher introduces this"). **Level keys never change** (`year6`, `ks3` …): analytics values, leaderboard keys, personal-best keys and the label `firebase-leaderboard.js` stores with a ticker entry stay as they are. A question's own context ("90 Year 9 students") is content, not a label: it is listed for Jon, never changed under this ruling. | 3 Oct 2026 | Jon, 3 Oct 2026 (resit section contract); §7.5; Jon's ruling of 2 Oct 2026 on age wording |
| SR-12 | **Estimation questions are marked by the stated method.** "An estimation question accepts the answer produced by the stated estimation method (e.g. round each value to 1 significant figure, then calculate). Where a value could reasonably round two ways, accept each resulting answer. The exact calculator answer is not the target." Each question states its method. **Marking is an exact match** to the method's answer(s), not a band around it (Jon, 4 Oct 2026). A question whose method is undefined or gives no mental calculation (√2000, ln 1000, 3¹⁰, an undefined φ) is reworded with its own method or removed: content, so Jon's call. First conforming game: `estimation-engine`, rebuilt 6 Oct 2026 (PR #74): 45 GCSE N14 items, each rounding and each estimate marked by exact match through `MaffsAnswer`, the method answers computed by `scripts/verify-estimation-engine.py`; back on `/resit/`. The other estimation games are listed in todo, not yet brought under it. | 4 Oct 2026 | Jon, 4 Oct 2026 (resit safety contract; resit correctness audit, `estimation-engine` F4) |
| SR-13 | **Move-based equation games.** "In move-based equation games, any operation applied to both sides is valid and accepted, except × 0 and ÷ 0, which are blocked with an explanation (× 0 gives 0 = 0, true for every x, so the solution is lost; ÷ 0 is undefined). A valid move that makes the problem harder (introducing fractions or decimals, adding steps, or undoing the previous move) scores full marks and is followed by a nudge towards a neater move; the student chooses whether to continue their way or try the neater one. Equivalent final forms are accepted unless the question specifies the form. Multiplying or dividing by an expression containing the variable can gain or lose solutions; any game offering such moves must handle this explicitly." Where the question does specify the form, SR-3 applies (format message, no score). First games: `linear-equation-solver` (audit decision 3) and `equation-builder` (decision 5: equivalent rearrangements and swapped sides accepted), withdrawn from `/resit/` pending its rebuild. | 4 Oct 2026 | Jon, 4 Oct 2026 (resit correctness audit, decisions 3 and 5) |
| SR-14 | **Sensitive content, three tiers** (Jon, 4 Oct 2026). (a) **Banned everywhere:** death, fatal outcomes, suicide, self-harm, abuse, drowning, violence, family breakdown. (b) **Banned in jokes, silly theories and humour:** everything in (a), plus illness and injury. (c) **Allowed in neutral exam-style contexts:** illness, medical tests, screening, patients, hospitals, phrased as the exam boards phrase them. Established technical terms are not hits: "Prisoner's Dilemma", "base rate neglect". Titles and humour Jon has approved are allowlisted: "Tax Theft". Idioms are not SR-14 content (Jon, 4 Oct 2026 20:06): "half dead" (pot plants), "kills the claim", "neglected". Crime words are not in SR-14: neutral crime contexts are allowed, and violent crime is already tier (a). **SR-14 judges context, not keywords:** the scan is a tripwire, and a hit is a prompt to look, not an automatic fail of the content. The scan reads displayed text only; code identifiers (a CSS class named `dead`) are excluded, and so are lookup strings (`g['x']`, `'x' in g`, `hasOwnProperty('x')`). **Object keys are the exception** (Jon, 5 Oct 2026): a tier-(a) word is banned as an object key anywhere, quoted or bare, in a literal or written by assignment (`{dead: 1}`, `g.dead = …`, `g['dead'] = …`), because `Object.keys`/`entries`/`for…in` can put a key on screen. Checked by `scripts/check-content-safety.py` (CI, every game and escape room): tier (a) words fail anywhere, tier (b) words fail in humour fields (`joke:`, `theory:`, `conspiracies:` …); a new hit fails; the hits present when it was set are its `KNOWN` list, the SR-14 fix batch in todo START. A word list is a net, not a judge. First game: `correlation-or-coincidence`, rebuilt to it. | 4 Oct 2026 (amended the same evening, before merge) | Jon, 4 Oct 2026 (Correlation or Coincidence rebuild contract; rulings on PR #43) |
| SR-15 | **Every valid reason is accepted.** Where a game marks the reason for an answer, every reason that gives the answer in one step from what is drawn is accepted. A two-step item accepts the union of the reasons of every route its drawing allows; where the figure labels the intermediate angle (y), only the routes through it count (Jon: otherwise Angle Ace's L625 would accept 5 of 9 reasons and the question would stop discriminating). The game lists the accepted set (`multiReason`); the verifier derives it from the drawing and holds each two-step item's routes in a reviewed table with a one-line reason. First game: `angle-ace` (PR #79 one-step, PR #80 two-step; `scripts/verify-angle-ace.py`, `TWO_STEP`). | 6 Oct 2026 | Jon, 6 Oct 2026 (Angle Ace contract, audit F13; ruling on L638 and L625) |
| SR-16 | **A true statement is never a wrong option.** An option with the right value by a wrong method names the fault in its own text, or goes. A distractor may carry a stored reason, shown as feedback (e.g. "missing + c"). | 6 Oct 2026 | Jon, 6 Oct 2026 (20:30), rulings on audit tranches 3-6 |
| SR-17 | **Conventions and precision are stated in the question:** quartile method; wheel type; Monty Hall's host knowing; "simplify" names the form (Boolean, algebraic, trig); mechanics items state g; approximations state the number of terms and the precision; "speed" keys the magnitude; complex items state r > 0 and the argument range; a scalar multiple of an eigenvector is never a wrong option; rounded natural frequencies say so or use whole-count populations; multiple-choice answers state their precision (SR-1 applies to MC); square roots in rearranging state "positive". Notation puzzles (6÷2(1+2)) are removed. | 6 Oct 2026 | Jon, 6 Oct 2026 (20:30), rulings on audit tranches 3-6 |
| SR-18 | **Game-specific rulings.** Probability Paradox states assumptions; Sleeping Beauty accepts 1/2 and 1/3; the envelope item is "can't tell". Word Problem Decoder: one category scheme, both accepted where both fit. Spot the Error: a strategy choice is not an error. Truth Buster's statements are worded so the key holds as written. | 6 Oct 2026 | Jon, 6 Oct 2026 (20:30), rulings on audit tranches 3-6 |
| SR-19 | **Bank size alone never unlists a game.** | 6 Oct 2026 | Jon, 6 Oct 2026 (20:30), rulings on audit tranches 3-6 |
| SR-20 | **When a game is unlisted.** A game is unlisted until its verifier merges when a level reaches CRITICAL (10%+ of its items mark a correct answer wrong or a wrong one right) or 3+ items mark a correct answer wrong. Jon may unlist beyond this (tranche 5: all eleven). | 6 Oct 2026 | Jon, 6 Oct 2026 (20:30), rulings on audit tranches 3-6 |
| SR-21 | **Relisting an unlisted game.** A game unlisted for audit faults is ready to relist when its verifier runs in CI and the findings register has no open CRITICAL or HIGH entry for it. The home lane relists every ready game in one batched docs PR. That PR puts back everything the unlisting removed: the roster row in its old section, the portal cards and weekly-fact links, the sitemap, the spec map, the leaderboard hub row (out of `NOT_ON_HUB`), and `/resit/` and parent-guide links. Open MEDIUM and LOW entries do not hold a game back; they stay in the register. A game still on the cloud lane's `cloud-remaining:` list waits until it comes off it, and Jon may hold a named game (expectation-station, 7 Oct). | 7 Oct 2026 | Jon, 7 Oct 2026, contract F1 |
| SR-22 | **One leaderboard per mode or session length.** Where a game's modes or session lengths have different maxima or measure different things, each has its own board (its own level key in the leaderboard name); runs never share a board with a mode they cannot be compared to. Prime Sprint's board key (its session length) is shown on the hub, so a student sees which board a score is on. Prisoner's Dilemma ranks the tournament total only: single matches against one opponent are not submitted. New level keys are added; existing keys never change (SR-11). Open entries it decides: proof-builder-t5-023 and prisoners-dilemma-t4-001 (code still to change). | 7 Oct 2026 | Jon, 7 Oct 2026, his ruling R15 |
| SR-23 | **Timers follow `.claude/rules/timer-policy.md`.** A game listed under Hidden Count-Up runs a silent clock with no score multiplier, its time shown on the results screen only. Trig Identity Duel and Glorious Gantt Game follow it, as listed (their timers are visible now and Trig Identity Duel's feeds the score); scores before the change will not compare with scores after it, and that is accepted. Open entries it decides: trig-identity-duel-t2-010 and the timer part of glorious-gantt's entry at :783/:968 (code still to change). | 7 Oct 2026 | Jon, 7 Oct 2026, timer ruling |
| SR-24 | **A counterexample must refute the statement as written, not a softer one.** For Spot the Error-type games; read with SR-16 and SR-18. | 8 Oct 2026 | Jon, 8 Oct 2026 (contract CTX's "For Jon" list; first written in a CLAUDE.md handover, 5 Oct 2026, SR-14 fix batch) |
| SR-25 | **Words, figure and key must agree.** A question's text, its drawn figure and its key describe the same thing (Circle Theorem Spotter Q19: the figure drew the point on the minor arc while the text said major; a centreCirc `inside` flag puts C inside the marked angle). SR-8 covers what follows a changed key; this covers text against figure. | 8 Oct 2026 | Jon, 8 Oct 2026 (contract CTX's "For Jon" list; first written in a CLAUDE.md handover, 3 Oct 2026, PR #11) |

**Also recorded with SR-16 to SR-20** (Jon, 6 Oct 2026, 20:30):
- Start screens and cards state what the code does (timers, scoring claims).
- A level that serves another level's items is not listed as that level.
- Verifiers recompute explanation and hint figures, not just keys.

**Still stops for Jon**, whatever the rulings say:
- New content choices: contexts, numbers, a question's level.
- Spec mappings (todo §1.42).
- Anything in Jon's voice: `/updates/` entries, the bio.
- Privacy, data collection or public claims (§1, §3.3).
- Design or theme changes (§7.5).
- Anything irreversible.

**Adding a ruling.** When Jon rules on something that generalises, it becomes the next SR number,
dated, with its source, in the same PR as the work that prompted it. A ruling is changed only by Jon,
and the change is dated in its row.


## 0.4 Findings register

Every audit finding lives in `docs/audits/findings/<slug>.yml`, one file per game (so parallel fix PRs never edit the
same file), in the audits' own schema (`scripts/audit-register.py` holds it). `docs/audits/REGISTER.md` is generated
from them: counts by severity, status, class and game; open CRITICAL and HIGH by game, Year 6/KS3/GCSE/Core first; the
exit-bar dashboard for §0.2's freeze; and the live games no audit has covered. CI (the site-wide checks) fails if a
file breaks the schema, a `fixed` entry names no PR, or a roster-Unlisted game has no file.

**No PR edits REGISTER.md** (7 Oct 2026). Every fix PR used to regenerate it, so any two PRs open at once conflicted
on it. The workflow's `register` job regenerates it on every push to main, after the Gate, and commits it as the
workflow (`Regenerate REGISTER.md [skip ci]`) if it changed; on a PR, `audit-register.py --check` validates the
per-game files only and never reads REGISTER.md. So the file on main can lag a merge by a minute, never more.

**A fix PR closes its entries in the same PR, in its own game's file only:** set `status: fixed` and `pr: <n>` on
each entry it fixes in `docs/audits/findings/<slug>.yml`, and edit no other register file. An entry closed by a ruling, not a code
change, is `status: ruled` with `ruling:` naming the SR. A new audit adds its findings to the game's file (a second
`audited` entry when the game was audited before); ids are `<slug>-t<n>-NNN` (tranche n) or `<slug>-r-NNN` (resit audit).
Exit-bar points 3 and 6 are stated in the script (`SHARED_CHECKS_GREEN`, `SWEEP_DONE`): the PR that meets one sets it.

**The per-game files are edited by hand** (Jon, 8 Oct 2026; since 7 Oct, when the one-off builders were retired to
`~/.maffsgames-local/register-build/`), one game's file per PR; REGISTER.md never (above).

---

# 1. Analytics — Dual Logging (GA4 + Google Sheets)

Every game sends events to both GA4 and a Google Sheets backend via the `mfg()` wrapper function in `schools/assets/analytics.js`.

## 1.1 GA4 Configuration

Every HTML page must include the following snippet in the `<head>`. Cookieless mode — no cookies dropped, GDPR/PECR compliant.

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-992JLHLP2D"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-992JLHLP2D', {
    send_page_view: true,
    storage: 'none',
    anonymize_ip: true
  });
</script>
<script src="../../schools/assets/analytics.js"></script>
```

| **Property** | **Value** |
| --- | --- |
| Measurement ID | G-992JLHLP2D |
| Stream URL | https://maffsgames.co.uk |
| Stream ID | 13898555479 |
| Mode | Cookieless (storage: 'none'). No personal data collected. |

## 1.2 Google Sheets Backend

| **Property** | **Value** |
| --- | --- |
| Spreadsheet name | MaffsGames Events |
| Location | Jon's Google Drive (Jon, owner) |
| Apps Script code | docs/apps-script-endpoint.js |
| Dashboard tab | Auto-rebuilds daily with 5 charts |
| Daily email report | 7am UK time to Jon (owner) |
| Row limit protection | Auto-deletes oldest 10% at 9M rows |

### 1.2.1 GA4 country tabs (8 Oct 2026, Jon's ruling)

Two tabs in the **MaffsGames Events** spreadsheet hold GA4's daily figures by country, read from the Google Analytics Data API (advanced service `AnalyticsData`, property `properties/528531831`, the property of stream 13898555479). They are aggregates GA4 already holds. Nothing new is collected, and the site, `analytics.js`, the events endpoint and the privacy page are unchanged. **Live only once Jon has installed it** (`docs/ga4-country-setup.md`).

| Tab | Columns |
| --- | --- |
| GA4 country daily | date, country, activeUsers, sessions, engagedSessions, eventCount |
| GA4 country events | date, country, eventName, activeUsers, eventCount, for page_view, game_started, question_answered, game_completed |

- **Code:** `docs/apps-script-ga4-country.js`, a script file in the Sheet's bound Apps Script project beside the endpoint's `Code.gs`. Its names are prefixed `GA4C_`/`ga4c`/`ga4Country` so the two cannot clash. It is not part of the web app deployment. Setup is in `docs/ga4-country-setup.md`; the test is `scripts/test-ga4-country.py` (CI, B3).
- **Schedule:** `ga4CountryDaily`, between 06:00 and 07:00 UK time, before the 07:00 report.
- **The 48-hour settle window:** GA4 revises a day's figures for about 48 hours. So each run fetches the last **three** complete days and **replaces** those dates' rows. Re-runs never duplicate, and no other date changes. `ga4CountryBackfill` replaces 1 Sep 2026 to yesterday and is safe to re-run.
- **The events tab is never read or written.** Sheets are reached only by the two tab names, and new tabs are added at the end.
- **Reading: "users" are not people here.** GA4 runs cookieless, so activeUsers and sessions count visits, not people. Real use is the game events and engagedSessions. A crawler shows page_view with no question_answered. GA4 sees less than the Sheet (blockers), so the country split is a share, not a full count.

## 1.3 Events — Required on ALL Games

Use `mfg()` not `gtag('event',...)`. The wrapper sends to both GA4 and Sheets.

| **Event** | **When** | **Parameters** |
| --- | --- | --- |
| `game_started` | First question presented | game_slug, level, mode (if applicable) |
| `mode_selected` | Mode chosen (multi-mode games only) | game_slug, mode |
| `question_answered` | Every answer submission | game_slug, level, question_index (1-based), correct |
| `game_completed` | Results screen reached | game_slug, level, score, questions_answered, questions_correct |
| `personal_best_set` | New PB recorded in localStorage | game_slug, level, score, previous_best |
| `game_abandoned` | Page hidden before completion (automatic via analytics.js) | game_slug, level, question_index |

**Rules:**
- `game_slug` hardcoded to match directory name
- `level` from game state / URL param
- `question_index` is 1-based — use existing counter variable
- Games without levels use level `'all'`
- Multi-mode games MUST include `mode` on all events
- Abandon tracking handled automatically by `analytics.js` via `visibilitychange`
- Do not add additional data collection without explicit approval from Jon

### Portal events (root `index.html` only — not games)

| **Event** | **When** | **Parameters** |
| --- | --- | --- |
| `filter_applied` | A level pill, topic pill or the New & updated toggle is clicked; or 1000 ms after the last search keystroke, and only if the trimmed query changed | level, topic, fresh, search_used, search_length, search_query, result_count, trigger |
| `game_card_clicked` | A `.game-card` link is clicked, via one delegated listener | the same seven state parameters, plus game_slug and section |
| `section_clicked` | A labelled element in a portal feature section is clicked (a link), or a labelled toggle is opened. Any page that loads `analytics.js`, via one delegated listener there | section, item, position, action, plus game_slug, filter_type, filter_value |

`trigger` is `level` \| `topic` \| `fresh` \| `search` \| `reset`. (`reset` is reserved — the
portal has no reset control today.) `section` is the containing section's id, or its heading text
when it has none, which is currently always the case: `KS3`, `GCSE`, `New for 2026/27` and so on.
`search_query` is trimmed, lowercased and truncated to 40 characters. `result_count` is
**re-read from `#gameCount`**, which is where `applyFilters()` writes its de-duplicated total — a
game appears in several sections and must not be counted twice.

**Why these two events carry `filter_type` and `filter_value` as well.** The Apps Script endpoint
writes a fixed column list and silently drops any key it does not already name, so every parameter
above reaches GA4 but only `event`, `game_slug` and `level` would reach the sheet. `filter_type` and
`filter_value` are reserved columns nothing else writes, so the whole state is packed into
`filter_value` in this exact key order:

```
v1|level=<level>;topic=<topic>;fresh=0|1;su=0|1;sl=<search_length>;q=<search_query>;n=<result_count>
```

`filter_type` carries the `trigger` on `filter_applied` and the `section` on `game_card_clicked`.
The `v1|` prefix allows the format to change later without breaking rows already written. `;`, `=`
and `|` are stripped from `q` before encoding so a search term cannot break the parsing.

Two architectural rules, because the cards are due to be generated from a single metadata source:
`getFilterState()` is the only reader of filter state, and card clicks use **one** delegated
listener rather than handlers on the ~130 duplicated `.game-card` elements.

Nothing fires on page load: `filter('all')` runs during setup, and `mfgPortalReady` is only set
true afterwards.

**Feature sections are tracked by label, never by code (1 Oct 2026).** Before this, only the
Misunderstood Maths card (its own `fact_*` handlers) and game cards were tracked; the escape-rooms
band, the parent guides strip and every show/hide toggle recorded nothing, because each section's
tracking had to be written by hand. Now one capture-phase listener in `schools/assets/analytics.js`
handles any element carrying `data-mfg-item` inside an element carrying `data-mfg-section`:

```html
<div data-mfg-section="escape-rooms">
  <a data-mfg-item="hamster-heist" href="escape-rooms/hamster-heist/">…</a>
  <button data-mfg-item="show-all" aria-expanded="false">Show all rooms</button>
</div>
```

**Adding the two attributes is the only step to track a new section.** A link fires
`action: "open-link"`; an element with `aria-expanded` fires `action: "toggle-open"` only when it is
opening (read in the capture phase, before the page flips it), as `fact_expanded` does. `position` is
1-based among the section's labelled items in page order. The listener never calls
`preventDefault` or delays a link; `mfg()` posts with `keepalive`. Never label anything inside a
`.game-card`: one click would then fire both events. Sheet columns (the endpoint keeps a fixed list):
`item` → `game_slug`, `section` → `filter_type`, and `v1|pos=<position>;action=<action>` →
`filter_value`. Labels on the portal: `escape-rooms` (12 items), `parent-guides` (1), `new-2026-27`
(its "Show them" toggle), `essentials-link` (the homepage badge, item `open-essentials`).
`scripts/test-section-clicks.py` (CI) clicks every labelled element and checks the payload, and that game
cards and `fact_expanded` are unchanged.

**Renamed values, 8 Oct 2026 (contract ESSENTIALS: /resit/ became /essentials/).** The event (`section_clicked`)
and its parameters are unchanged; only these values changed, so the Sheet and GA4 read across the date by
mapping old to new: section `resit-link` -> `essentials-link` (homepage badge), item `open-resit` ->
`open-essentials`, section `resit` -> `essentials` (the page itself; its items, the game slugs, `contact`
and `spec-map`, are unchanged). Page views: `/resit/` before 8 Oct 2026 is `/essentials/` after; `/resit/`
after that date is the redirect stub (a hop, not a visit).

## 1.4 Dashboard Charts (auto-updating)

1. **Top Games** — bar chart, 7-day, sorted by starts
2. **Level Split** — pie chart, KS3/GCSE/A-Level/Core/L4/Further
3. **Accuracy by Game** — bar chart, sorted lowest first (hardest games)
4. **Hardest Questions** — table, top 15 lowest accuracy (min 5 attempts)
5. **Daily Activity** — line chart, 30-day trend

---

# 2. SEO Requirements — Mandatory on Every Page

## 2.1 Required Tags

**Every game page's and /essentials/'s title and description are generated, never hand-written (Jon, 5 Oct 2026,
PR #72; /resit/ until 8 Oct 2026).** `data/games.json` holds one search phrase and one description per roster game (plus /essentials/'s
stated pair); the levels come from the roster's Levels column. `scripts/apply-meta.py` writes `<title>`, the
meta description and their og:/twitter: copies; `scripts/check-meta.py` (CI) holds every page to it and is
the authority on the rules:
- Title: `<phrase> Game – <levels> Maths | MaffsGames`, at most 60 characters (over 60: GCSE only, else the
  game's lowest level; still over, `<phrase> Maths Game | MaffsGames`).
- Description: `<what the student practises> For <levels>. Free, no sign-up.`, at most 155 characters.
- "Year 6" and "Starter" never appear (SR-11): a Year 6-only game has no levels sentence.

To change one, edit `data/games.json`, run `apply-meta.py`, then `check-meta.py`. A new game gets its
games.json entry in the PR that adds it, or `check-meta.py` fails.

### Meta description
```html
<meta name="description" content="[generated from data/games.json, at most 155 characters]">
```

### Canonical link
```html
<link rel="canonical" href="https://maffsgames.co.uk/games/{slug}/">
```

### OG and Twitter tags (every game page)
```html
<meta property="og:title" content="{the generated title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://maffsgames.co.uk/schools/assets/og-image.png">
<meta property="og:type" content="website">
<meta property="og:url" content="https://maffsgames.co.uk/games/{slug}/">
<meta name="twitter:card" content="summary_large_image">
```

### JSON-LD structured data (portal only)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "MaffsGames",
  "url": "https://maffsgames.co.uk",
  "description": "Free curriculum-aligned maths games for UK schools"
}
</script>
```

---

# 3. Portal Structure

## 3.1 Level Filter System

| **Filter** | **Colour** | **CSS Variable** | **Audience** |
| --- | --- | --- | --- |
| KS3 | #22c55e green | --ks3: #22c55e | Year 7–9, ages 11–14 |
| GCSE | #3b82f6 blue | --gcse: #3b82f6 | Year 10–11, ages 14–16 |
| A-Level | #f97316 orange | --alevel: #f97316 | Year 12–13, standard maths |
| Further Maths | #8b5cf6 purple | --further: #8b5cf6 | Year 12–13, further maths |
| Level 4 | #ef4444 red | --l4: #ef4444 | HNC/HND/BTEC Level 4 |
| Core Maths | #0ea5e9 sky blue | --core: #0ea5e9 | AQA Core Maths (1350) |

## 3.2 Topic Filter System

Cards carry a `data-topics` attribute; the portal filters on these six tokens, and a card may carry several.

| **Token** | **Label** |
| --- | --- |
| `number` | Number |
| `algebra` | Algebra |
| `geometry` | Geometry |
| `statistics` | Statistics |
| `applied` | Applied |
| `reasoning` | Reasoning |

**Which games carry which topics is in `.claude/rules/game-roster.md`, not here.** Canon used to list games
per topic and the lists went stale silently as the roster grew from 60 to 93.

**A game appears on more than one card.** Games are duplicated across level sections and the "New for
2026/27" section, so the portal holds 135 `.game-card` elements for 96 games (135 counted 30 Sep 2026, plus Free Daily Pizza's two, less Regression Rumble's two when it was withdrawn). `applyFilters()` de-dupes the
visible count via `seen[href]` with `?...` stripped, so the count still reads 96. Copy cards **verbatim**
(same `href`, `data-levels`, `data-topics`) when duplicating one.

## 3.3 Privacy Page

Located at `/privacy/index.html` (canonical; `/schools/privacy/` redirects to it). Fully rewritten 20 March 2026. Discloses:
- Google Analytics (cookieless)
- Gameplay analytics backend (Google Sheets via Apps Script)
- Formspree feedback form
- Buy Me a Coffee

**Newsletter removed 2026-09-21.** It was never set up: the About page embedded a MailerLite form
whose id was still the literal placeholder `your-mailerlite-form-id`, so the signup 404'd for every
visitor who tried it, and no newsletter was ever sent. The privacy page meanwhile disclosed
MailerLite as a processor holding email addresses the site had never collected. Form, script, CSS
and disclosure are all gone, and the last-updated date moved to 21 September 2026.

There is now **no retention channel** — nothing tells a returning teacher what has changed since
they last looked. That is a real gap, and it should be reopened as a deliberate decision rather
than by quietly restoring this form: whatever replaces it needs a sender, a schedule someone will
actually keep, and a processor disclosed only once it is genuinely in use.

## 3.4 New & updated badges (Jon, 8 Oct 2026)

**NEW** = a genuinely new game, first added to the portal in the window (27 Sep 2026, unchanged).

**UPDATED** (Jon's ruling, 8 Oct 2026, verbatim): The Updated badge marks a change a returning student would notice in
what they learn or how they're marked: new questions or levels, a new mode, new help or worked explanations, or
marking that changes what earns credit (for example, Linear Equation Solver's optimal-move scoring, or Gradient
Hunter's typed gradient). It is not earned by correctness fixes, the answer lock, Next-button behaviour, phone fit
or visual restyling, however visible those are.

This replaces the 27 Sep 2026 definition (in `docs/history/claude-md-archive.md`, "Previous state — 2026-09-21").
The mechanism, as built 27 Sep 2026 (copied verbatim from there; the archive keeps the history):

- Each qualifying card carries `data-badge="new"` or `data-badge="updated"` plus
  `data-badge-date="YYYY-MM-DD"` (the day the qualifying work went live), on **every** occurrence
  of that game's card — a game can repeat across several level-filtered sections, and the
  attribute has to be on all of them for the toggle to work regardless of which section is
  showing. There is no hand-placed ribbon in the HTML any more.
- One function, `applyBadges()` (top of the portal's `<script>`, run once via `applyBadges();`
  right before the first `filter('all')` — i.e. before `applyFilters()` ever runs), computes
  whether each badge is still live: `BADGE_DAYS = 56` (half a term) since `data-badge-date`. If
  live, it sets `card.dataset.fresh = '1'` (the flag `applyFilters()` already reads — that
  function itself was never touched) and renders the `.fresh-badge` / `.fresh-badge.updated`
  ribbon on that game's *first* card only. If nothing is live, it also hides `#freshBtn` entirely,
  so the toggle can never be clicked into an empty result — there is never a state where "New &
  updated" is selectable and shows nothing.
- "Today" is read through a single function, `mfgToday()`, purely so a test can temporarily
  replace its body to simulate a later date without touching the badge data — never committed.
- When a game next qualifies, add or refresh `data-badge`/`data-badge-date` on every occurrence of
  its card; nothing else to update, no list to keep in sync, nothing to remember to remove later.


## 3.5 The /updates/ page

Entries are in Jon's voice (§0.3, "Still stops for Jon").

- **Writing an entry about a false claim:** describe it, don't quote it (Jon, 8 Oct 2026: quoting a wrong figure
  repeats it). `check-public-claims.py` blocks the literal "No data collected" on /updates/ like any other live page.
  (First written 3 Oct 2026 in a CLAUDE.md handover; contract CTX.)

---

# 4. Complete Game Roster

**The roster lives in `.claude/rules/game-roster.md`** — 96 numbered rows (plus a Withdrawn section), with slug, levels, topics and a
one-line description each. It is maintained; this document is not the place for a second copy.

Canon held its own 60-row table until 8 September 2026. By then it was **33 games behind**, still
listed four curriculum gaps that had already been filled, and nobody had noticed because both
tables looked plausible on their own. That is the reason for the split at the top of this file.

## 4.1 Shape of the roster

| **Section** | **Games** |
| --- | --- |
| KS3 | 34 |
| GCSE | 27 |
| Core Maths | 10 |
| A-Level | 17 |
| Further Maths | 5 |
| **Total** | **93** |

Section is the game's home level, not its only one — most games declare several tiers in `data-levels`.

## 4.2 Games not on the portal

| **Slug** | **Why** |
| --- | --- |
| `the-perfect-prank` | The original escape-room prototype, built to the old 40-minute spec. Unlisted on purpose and kept as the long-form example. It has a directory under `games/` but no portal card, which is why `games/` counts 95 and the site says 93 |

`just-pythag-it-bruv` was here from 4 Oct 2026 (merged unlisted, `noindex`, for Jon to play first). Jon approved it after
playing it (recorded 8 Oct 2026, contract RELIST-3); it is now listed: portal, `/essentials/` (Geometry and measures), spec
map G20, sitemap and the leaderboard hub.

## 4.3 Games excluded from leaderboards

`constructions-lab` and `given-that` — non-scored, exploratory formats. They are the only two of the
97 that do not call `submitScore()`. (`distinctly-average` was briefly a third, 29 Sep 2026; Jon ruled it
should have a leaderboard, so it is wired and **held** rather than excluded — see §9.)

## 4.4 The calculator tag

**Every game carries a Calculator field (Jon's contract, 4 Oct 2026),** the last column of
`.claude/rules/game-roster.md`. It matters for paper-specific revision: every GCSE maths
exam has a non-calculator paper and calculator papers.

| **Value** | **Means** | **Start screen** |
| --- | --- | --- |
| `required` | The questions need a calculator (Pythagoras to 1 d.p.) | "Calculator required" |
| `scientific` | The questions need a scientific calculator (powers beyond ², ln/log, eˣ, trig, π); the on-screen calculator shows its scientific keys (contract SCI-CALC, 9 Oct 2026) | "Scientific calculator required" |
| `not allowed` | Practice for a non-calculator paper; the numbers are chosen to be done by hand | "Non-calculator" (Jon, 6 Oct 2026) |
| `optional` | Either works | worded when the first game is tagged |
| `untagged` | Not yet decided. Every game starts here and is tagged in its own PR | nothing |

**One badge, one style.** The start screen shows `<span class="calc-badge" data-calc="…">…</span>`,
styled once in `schools/assets/theme.css` (`.calc-badge`; `data-calc="required"` takes `--hint`,
`"not-allowed"` takes `--wrong`, anything else `--muted`, all AA on `--surface-alt`). A game never styles
its own. A `required` game also says **"Use a calculator."** on every question (Jon, 4 Oct 2026). First
users: `just-pythag-it-bruv` (`required`) and `estimation-engine` (`not allowed`, PR #74); every other game
is `untagged` and its display is unchanged.
When `games.json` is built (§3.12) the field moves there with the rest of the roster.

**The on-screen calculator, `MaffsCalc` (4 Oct 2026).** Many resit students do not own a scientific
calculator, so every `required` game carries one: `schools/assets/calculator.js` (global `MaffsCalc`),
styled in `theme.css` (`.maffs-calc*`, tokens only; a game's `--accent` colours the toggle and =).

- **Keys:** 0–9, decimal point, + − × ÷, brackets, x², √ (which opens a bracket, as on a Casio), C, DEL,
  =. Order of operations as on a scientific calculator: −3² = −9; a number, bracket or √ straight after a
  value multiplies (2(3) = 6); missing closing brackets are closed on =, extra ones are an error. After =,
  an operator carries the answer on as "Ans"; a digit starts afresh.
- **Display:** 10 significant figures, trailing zeros dropped, so 0.1 + 0.2 shows 0.3, never
  0.30000000000000004; 10^10 and over, or under 10^−6, as a×10^n. Divide by 0, √ of a negative,
  unbalanced brackets and 1.2.3 show "Error", never NaN. The engine is a parser, never `eval()`.
- **On the page:** `MaffsCalc.mount(el, {dock: card})` puts a "Calculator" toggle and a panel in the page
  flow, under the answer box. It never covers the question or the answer box; the page may scroll to it.
  Closed at first; it stays open between questions once opened. Five columns of keys at least 44px fit a
  320px phone. Below the dock breakpoint the game hides it while the answer box is hidden (Pythag's tap
  step, and the feedback, §7.6.1), and puts the feedback above it, never below.
- **Wide screens: docked beside the card (Jon, 4 Oct 2026).** When the room right of the `dock` element
  (the question card) holds the panel, it docks there: level with the card's top, sticky while the page
  scrolls, out of the page flow, so opening or closing it never moves the game column. The breakpoint is
  measured, not a fixed media query: room = window width − card's right edge − 12px gap − 8px edge, and it
  docks when that is at least 262px (the narrowest panel whose keys stay 44px), up to 340px wide. For a
  720px column (a 688px card) that is a 1252px-wide page: 1252px windows with overlay scrollbars,
  about 1269px with a 17px desktop scrollbar; 1280px docks either way. Docked, it stays in view through the
  tap step and the feedback; only its toggle goes with the answer box. The constants are
  `MaffsCalc.DOCK`; the dock is in `theme.css` (`.maffs-calc.docked`, `.maffs-calc-host`).
- **Feedback in view.** A game that carries it shows its feedback without scrolling at 1280×720,
  1366×768 and 1920×1080 with the calculator docked (layout, never a scroll), and on phones; below the
  breakpoint, if the feedback is ever not fully in view after Check, the page glides to it (smoothly,
  instantly under reduced motion).
- **Keyboard:** typed keys drive it only while focus is inside the panel, so typing in the answer box is
  never taken over. Enter on a focused key presses that key; Escape closes the panel.
- **Phones: one keypad for the calculator and the answer (Jon, 4 Oct 2026).** On a touch screen
  (`(pointer: coarse)`) below the dock breakpoint the panel is **compact**: 48px keys, a slim display, and once
  open the Calculator toggle gives way to a close key inside the display. `mount(el, {answer: input,
  keepInView, foldInset, onToggle})` makes the same keypad type the answer, so the system keyboard never
  opens (it would cover the question and the diagram). The answer box is read-only with `inputmode="none"`
  and is never focused; tapping it opens the keypad on it. The student taps a display (the calculator's or
  the answer box) to choose where the keys go; the chosen one has a heavier border and a "typing here" tag.
  While the keypad types the answer, only 0-9, the point, DEL and C work (12 characters at most); the
  operators, brackets, x², √ and = are disabled. On open the page scrolls just enough to show the answer
  row, Check and the keypad together. Desktop, a mouse, and the docked calculator are unchanged: the answer
  box takes the physical keyboard as before. The switches are `MaffsCalc.ANSWER`, read live so a test can
  turn each off. Pythag's layout under it (Jon's option B): rounds 1-2 fit 390×844 with the keypad open;
  round 3 may scroll there; everything fits 412×915.
  - **WebKit (found in testing):** to keep focus, and so the keyboard, away, the answer box cancels
    `pointerdown`; WebKit then sends **no `click`**, so a click-only handler would never open the keypad
    on an iPhone. It opens on **`pointerup`** (`click` stays, debounced, for anything without pointer
    events).
  - **Ghost click (found in testing):** opening the keypad moves the page (the game shrinks its figure),
    so the tap's own synthetic click landed on whatever was now under the finger, a key. The answer box
    cancels `touchend`, which stops that click.
  - **Not yet tried on a real iPhone** (Playwright WebKit with touch passes; Jon tests on Android).
- **Nothing is sent:** no analytics event, no storage, no request.
- **Scientific keys (contract SCI-CALC, 9 Oct 2026):** `mount(el, {keys: 'scientific'})` adds a block above the
  basic keys: xʸ (right-associative, binding tighter than a minus on its left: 2^3^2 = 512, −2^2 = −4), ln,
  log (base 10), eˣ, sin, cos, tan and their inverses (each opens a bracket, like √), π and e (2π multiplies),
  and a DEG/RAD key whose mode the display shows (DEG by default). Errors: ln or log of 0 or less, sin⁻¹ or
  cos⁻¹ outside [−1, 1], tan at an odd multiple of 90° (exact for whole degrees) or of π/2, anything not
  finite. `mount()` without it is the basic panel, key for key. A `scientific` game loads the same scripts,
  shows "Scientific calculator required" and mounts with `{keys: 'scientific'}`.
- **Where it loads:** only on games whose roster field is `required` or `scientific`. The roster is not served, so each
  such game includes the script itself; `scripts/check-calculator.py` (CI) fails if a game's include, its
  badge and its roster field disagree, either way, or if any other page loads it.
- **Checked by** `scripts/test-calculator-js.py` (CI): 65 expressions (arithmetic, precedence, x², √,
  brackets, errors, the display), 16 key sequences, the keyboard, the toggle, nothing sent, key sizes
  at 320, 375 and 390px, and the dock beside a 720px column (docked at 1280/1366/1920, sticky, never over
  the column, not docked at 1240 or 390) with five planted dock faults, and the answer target in Chromium and WebKit (touch at 390 and
  320px, mouse at 1280 and 390px) with eight planted answer faults. A game that uses it measures its own
  phone fit with the panel open and closed, typing on the keypad (`verify-just-pythag-it-bruv.py`).

**The phone keypad, `MaffsKeypad` (5 Oct 2026, PR #70; todo §3.21, Jon's ruling (b)).** MaffsKeypad is
the phone keypad for every typed answer on the site, calculator or not: `schools/assets/keypad.js`
(global `MaffsKeypad`), styled in `theme.css` (`.maffs-keypad*`: the calculator's phone keypad, same
panel, five columns, 48px keys). **MaffsCalc composes it**: the answer mode above is MaffsKeypad driving
the answer box (attributes, focus handling, the WebKit `pointerup` and ghost-click handling, the mark,
typing, the fold scroll), with the calculator's own toggle, display and keys; `MaffsCalc.ANSWER` is passed
in as its live switches and its class names are kept. So there is one copy of the answer-box behaviour.

- **Mount:** `MaffsKeypad.mount(el, {targets, keys, maxLength, keepInView, foldInset})`. `targets` is one or
  more inputs; the first is active to begin with, and a tap makes another the active one. Keys: 0-9, the
  point, DEL, C, and a minus where the game asks for one (`keys: {minus: true}`; it types "-" into an empty
  box only). The keys type into the active box only, at most `maxLength` characters (12), firing an
  `input` event each.
- **Touch screens only** (`(pointer: coarse)`, `MaffsKeypad.CONFIG.query`): every box is read-only with
  `inputmode="none"` and never focused, so the system keyboard never opens. With a mouse nothing is drawn
  and the boxes are ordinary inputs (`inputmode="decimal"` unless the page set its own).
- **The active box** has a heavier border and outline plus the "typing here" tag, never colour alone. A box
  narrower than the tag (four in a row on a 320px phone) gets the tag centred on it, its text shrunk so it
  is at most 6px wider than the box each side, so it never lies over the next box, in any font.
- **Where it loads:** any page, whatever its roster Calculator field: it has no calculator in it. A page
  that loads `calculator.js` loads `keypad.js` too (before it); `scripts/check-calculator.py` checks both.
- **Checked by** `scripts/check-keypad.py` (CI): 1, 2 and 4 boxes on touch phones at 320, 375 and 390px
  (keys reach the active box only, DEL and C act on it alone, nothing editable is focused, the length limit
  holds, one box marked and its tag over no other box, 48px keys, no sideways scroll, a box below the fold
  brought into view with the keys, the minus key), ordinary inputs with a mouse, six planted faults.
- **Rollout:** the other typed-answer games (todo §3.21's list) move onto it one game per contract.

---

# 5. Timer Policy

**The per-game lists are in `.claude/rules/timer-policy.md`**, which is the maintained copy. The policy
itself:

| **Timer type** | **When it applies** |
| --- | --- |
| Countdown | Recall and recognition games only. **30-second minimum per question.** |
| Count-up | The default. Time feeds the scoring multiplier rather than ending the run |
| Count-up, display only | Shown but not scored |
| None | Games where time pressure would distort the thinking — exploratory, reasoning and puzzle formats |

Escape rooms are not covered by this policy: they run a single 15-minute room clock with a 45-second
penalty per wrong setting. See §11.

---

# 6. Curriculum Coverage

## 6.1 AQA Core Maths Coverage (1350)

**No open gaps as of 8 September 2026.** The three that stood here for months — §3.9, §3.10 and §3.11 —
were all closed by games that were built and shipped without this table being updated.

**6 Oct 2026: §3.8 (critical path) has no listed game while Glorious Gantt is rebuilt** (unlisted under SR-20,
tranche 4 audit). The spec map shows it as "Glorious Gantt Game (being fixed)".

| **Section** | **Topic** | **Coverage** | **Status** |
| --- | --- | --- | --- |
| §3.1 | Analysis of data | Stat Attack, Chart Interrogator, Core Maths Paper 1 | Covered |
| §3.2 | Maths for personal finance | Tax Theft, Core Maths Paper 1 | Covered |
| §3.3 | Estimation | Fermi Lab, Estimation Golf, Estimation Engine | Covered |
| §3.4 | Critical analysis of given data and models | Core Maths Papers 2A, 2B, 2C | Covered |
| §3.5 | The normal distribution | Normal Navigator, Core Maths Paper 2A | Covered |
| §3.6 | Probabilities and estimation (sampling, point estimates, confidence intervals) | Core Maths Paper 2A | Covered (by the practice paper only) |
| §3.7 | Correlation and regression | Correlation or Coincidence, Regression Rumble, Core Maths Paper 2A | Covered |
| §3.8 | Critical path analysis | Glorious Gantt Game (unlisted 6 Oct 2026 while it is rebuilt) | **No listed game** until Glorious Gantt is relisted (todo, its relist checklist) |
| §3.9 | Expectation (incl. Venn and tree diagrams, combined events) | **Expectation Station**, Expected Damage, Given That, Screening Room, Probability Paradox, Core Maths Paper 2B | **Covered** — was listed as a gap until 08/09/2026 |
| §3.10 | Cost-benefit analysis | **Better Value**, Core Maths Paper 2B | **Covered** — was listed as a gap until 08/09/2026 |
| §3.11 | Graphical methods | Graph Sketcher, Core Maths Paper 2C | Covered |
| §3.12 | Rates of change | **Gradient Hunter**, Core Maths Paper 2C | **Covered** — was listed as a gap (as §3.11) until 08/09/2026 |
| §3.13 | Exponential modelling | Growth and Decay, Core Maths Paper 2C | Covered |

**Titles are AQA 1350's own (resolved 3 Oct 2026, Jon's ruling, checked on aqa.org.uk).** This table carried "graph sketching" at §3.4, "hypothesis testing" at §3.6 and rates of change at
§3.11 from March; AQA's are §3.4 Critical analysis, §3.6 Probabilities and estimation, §3.11 Graphical
methods, §3.12 Rates of change. The games moved with them (spec map, todo §1.42): Graph Sketcher to
§3.11, Gradient Hunter to §3.12, the probability games to §3.9. 1350 has no hypothesis testing, so Test
the Claim is not a Core Maths game (it stays mapped at A-Level L1–L3 and HNC LO4).

## 6.2 Spec-Map Gaps

**None open as of 8 September 2026.** This section listed four for months after the games that
closed them had shipped. The four, and what closed them, are in §8.1.

## 6.3 Unit 4002 Scheme of Work (14 weeks)

| **Week** | **Topic** | **Games** |
| --- | --- | --- |
| 1 | Algebraic Foundations | Index Laws, Quadratic Factoriser |
| 2 | Trigonometry | Trig Worms, Trig Wars |
| 3 | Complex Numbers | Complex Converter |
| 4 | Functions & Graphs | Sequence Solver, Graph Sketcher |
| 5 | Statistical Methods | Chart Interrogator, Normal Navigator, Stat Attack |
| 6 | Matrices | Matrix Crunch |
| 7 | Consolidation I | All |
| 8 | Differentiation I | Differentiation Duel |
| 9 | Differentiation II | Differentiation Duel (Level 4 tier) |
| 10 | Integration I | Integration Duel |
| 11 | Integration II | Integration Duel, Partial Fractions Duel |
| 12 | Consolidation II | All |
| 13 | Vectors & Mechanics | Component Crusher, SUVAT Selector |
| 14 | Numerical Methods | Estimation Golf, Fermi Lab |

---

# 7. Technical Reference

## 7.1 Platform Principles

- Free forever — no subscription, no freemium, no ads
- No sign-up required — zero friction for students
- Gameplay event data may be logged to analytics backend — no PII collected. All collection disclosed in privacy page. No additional collection without Jon's approval.
- Curriculum aligned — every game maps to AQA/Edexcel/BTEC spec
- Single-file HTML games — no build step, no external runtime dependencies
- Minimum 40–50 questions per game
- Mathematical notation via KaTeX only — no ASCII approximations (scope: see 7.1.1)
- Answer matching via `dataset.val` always — never compare rendered HTML strings
- Session-length controls use `MaffsSession` (`schools/assets/session-length.js`) — never
  hand-roll one, the same pattern as `MaffsOptions` for answer options
- **Marking by structure, not value (audit class 4): the ACCEPTED-list pattern** (Equation Builder, PR #49,
  5 Oct 2026). When a game assembles an answer from tiles or steps, correctness is decided once, offline, by a
  verifier: it enumerates every well-formed answer the student can build, classifies each with SymPy (SR-13:
  equal value, or the same solution set and not an identity; per-question exceptions recorded in the verifier
  with a one-line reason), and writes the accepted list into the page as data. The game only looks answers up;
  it never compares slot by slot or evaluates anything. The verifier fails CI if the page's lists differ from
  what it computes, if a key is not in its own list (an unbuildable key), or if an accepted answer uses a tile
  tagged as a distractor (SR-4 applied to tiles). `scripts/verify-equation-builder.py` is the reference;
  linear-equation-solver and angle-ace reuse the pattern in their own contracts.
- **Teaching a method step by step: the staged-method pattern** (Simultaneous Solver, PR #83, 6 Oct 2026).
  When marks are lost in the method, not the answer, the game asks for each step in turn and marks each one:
  every step needs an answer before the next appears; a right step moves straight on; a wrong step shows its
  reason (the misconception made visible, such as the letter doubling instead of vanishing, or the working term
  by term) and waits for `MaffsNext`, then play continues from the correct values, so one slip costs one mark.
  Marking follows SR-13: any valid step scores, a valid but clumsier one scores with the neatest shown, x0 is
  blocked. Stages that add one step at a time are modes (`mode` on every event), each with its own board.
  The bank is generated offline by a seeded script to rules (`scripts/gen-simultaneous.py`), and a verifier
  recomputes every answer, holds every rule, marks every possible answer to the marked step in Chromium, and
  plays a whole problem on MaffsKeypad at phone sizes. A step that builds an answer from tiles (Stage 5, to
  come) uses the ACCEPTED-list pattern above. `scripts/verify-simultaneous-solver.py` is the reference.
- The teacher feedback line uses `MaffsInvite` (`schools/assets/teacher-invite.js`, Jon, 4 Oct 2026):
  one small line, "Using this with a class? I'd love to hear how it went. — Jon", linking to
  `/feedback/?type=classroom&game=<slug>` in a new tab. **It sits on the results screen (Jon, 5 Oct 2026,
  PR #73)**, where a teacher has just seen the class play; the start-screen placement of 4 Oct is retired.
  Every roster game has one empty mount point (`<p id="teacherInvite">`) and ONE
  `MaffsInvite.mount(el, '<directory name>')` call. A game's slug is in exactly one of four lists in
  `scripts/check-teacher-invite.py`:
  - **RESULTS:** the mount point sits inside the named results container, after its last control row.
  - **FUNCTION_ROUTE:** a game that rebuilds its end screen (`innerHTML`). It moves the line in with
    `MaffsInvite.place(parent[, before])` at each end state. Today: chart-interrogator, factor-theorem,
    prisoners-dilemma, log-laws.
  - **START_SCREEN, with a reason:** constructions-lab and trig-wars have no results screen.
  - **PENDING, with a content hash:** a game mid-rebuild.

  The escape-room engine mounts it on the end card `finish()` rebuilds, for a win and a loss; /leaderboards/
  mounts it with no game (`null`). **Rule:** the line is never inside a flex row or grid, never between an
  answer input and its keypad, and reads at 4.5:1 or better. It inherits the page's text colour (no
  opacity, no new tokens); a page whose colour does not read on its card sets an existing colour on the
  mount point (Estimation Golf: `var(--ink)` on its cream card). A new game adds the mount point, the
  call and its list entry. `scripts/check-teacher-invite.py` (CI) fails a missing or misplaced mount, a
  wrong slug or altered wording. It plays every function-route end state and every live room to a win
  and a loss in Chromium at 390 and 1280px. /feedback/ reads `?type=` and `?game=` (a bare escape-room name maps to
  `escape-room:<name>`; an unknown value is ignored).
- Mixed prose and maths renders through `MaffsText` (`schools/assets/mathtext.js`) — never
  pass prose to K()/`katex.renderToString()` whole. Math mode drops inter-word spacing, so a
  string that mixes English words with a symbol or two ("Find the angle between \(\mathbf{a}\)
  and \(\mathbf{b}\).") must wrap only the maths in `\( \)`; a string that is maths throughout,
  with no prose at all, keeps going straight to K() unchanged. Checker tier 4 layer A's B7 rule
  enforces this (component-crusher, factor-theorem, test-the-claim, 27 Sep 2026).
  **The rule the fix batches apply (2 Oct 2026, to-do §1.31):** text rendered through KaTeX, by
  any wrapper (`K`, `rk`, `rkStr`, `tex` …), is either pure maths, or marks its maths with `\( \)`
  and goes through `MaffsText`. B7 now checks every render site, not just K().
- Two options are never equal in value unless the question's ask names the form that tells
  them apart. `MaffsOptions.build()` and `dataset.val` compare strings, so √50 and 5√2 both
  reach the student and only one is marked right (coordinate-geometry-dash:233). Checker tier 4
  layer A's B11 rule enforces this with one shared SymPy parser, `bank_common.parse_value()`. It
  reads "20–40" as a class interval, j in a phasor's e^{jθ} as the imaginary unit, and an integer
  written straight before \frac{p}{q} as a mixed number. `\text{}` parts are compared as words:
  two options are equal only if their `\text{}` parts match exactly and the rest is equal in
  value, so "1 Nm clockwise" ≠ "1 Nm anticlockwise" while √50 cm = 5√2 cm. A deliberate form
  question is listed in `scripts/checker-allowlist.json` (`b11_form_questions`) with its ask
  quoted (2 Oct 2026).
  **What B11 compares since contract F0 (7 Oct 2026).** Before it, `parse_value` returned None for
  several shapes and B11 skipped the pair, so tranches 5 and 6 found key-equal options it had passed.
  All of these are exact (Fractions and SymPy; no floating tolerance in any of them), and each is a
  fixture in `scripts/test-bank-common.py` (CI, Tier 4 layer A) taken from the audit item that showed it:
  - **juxtaposition** is multiplication in a mathematical option (2xe^{-y}, x^2 e^x, gT); never in
    prose: a word standing on its own ("22.5 m vs 22.5 m"), a common word, or a function the parser
    does not model leaves the option unparsed;
  - **`\binom{n}{r}`**; **trig, log and exp of constants**, in degrees where the text says ° (12 cos 0° = 12);
    a value shown with its rounding ("10 cos 30° = 5√3 ≈ 8.66 N") is its exact part; an equation of
    constants without one ("1! = 1") is a statement, not a value;
  - **SI prefixes** on a unit in `\text{}` (5 kW = 5000 W; 5 kW ≠ 5 kN);
  - **vectors** (`pmatrix`) are compared up to a non-zero scalar when the item asks for an eigenvector or
    a direction (its text says so, or the game asks it of every item: `VECTOR_DIRECTION_GAMES` in
    `bank_common.py`), otherwise entry by entry;
  - **angles** (r∠θ) are compared as complex numbers, so θ mod 360° and −r at θ + 180°, unless the item
    states a range ("positive", "principal", "−180° < θ ≤ 180°"): then r and θ exactly;
  - **Boolean expressions**, in a game listed in `BOOLEAN_GAMES`, by their full truth tables
    (juxtaposition AND, + OR, overline/′/¬ NOT), so AB + BC = B(A + C).
  Its first run flagged 42 new pairs in 9 games: 28 already in the findings register (each ledger entry
  carries its `register` id), 14 filed as `<slug>-f0-NNN`. All are ledgered as known; a new one fails CI.

### 7.1.1 Scope of the KaTeX rule — expressions, not unit symbols

Confirmed 22 Sep 2026.

"KaTeX for all mathematical notation" is scoped to **expressions**: equations, fractions,
surds, and multi-term formulas. These must render through KaTeX.

A **bare unit superscript or subscript** — `cm²`, `m³`, `m/s²` — may remain plain Unicode.
It is not the ASCII-fallback case the rule was written against, and typesetting unit
symbols through KaTeX buys a student nothing. This exempts `unit-converter`'s 303
instances from rewrite.

The line is what the character is *doing*, not which character it is. `v² = u² + 2as` is an
expression and must be KaTeX. The `²` in `45 m²` is a unit and may stay as it is.

**Still to re-check against this narrower scope:** `estimation-golf` and `estimation-engine`
were queued as category B offenders on the wider reading. Some of their instances may turn
out to be units rather than expressions, so re-check each before queueing either for work.

**The audit that produced this rule** (22 Sep 2026) found raw Unicode notation in 17 games,
in three sub-classes:

| Sub-class | Games | Shape |
| --- | --- | --- |
| A — loads KaTeX, never calls it | `unit-converter`, `coordinate-geometry-dash`, `normal-navigator`, `probability-paradox` | CDN tags present, zero `katex.render` calls; `coordinate-geometry-dash` even styles `.katex` selectors that can never match |
| B — no KaTeX at all | `suvat` ✅fixed, `scale-factor-scaling`, `estimation-golf`*, `estimation-engine`*, `52dle`, `prime-or-composite`, `fraction-equivalence`, `trig-worms`, `trig-wars` | notation authored as Unicode throughout |
| C — KaTeX for options, raw for explanations | `differentiation-duel`, `integration-duel`, `index-laws`, `proof-builder` | options are correct LaTeX; the `exp`/working string is assigned via `.textContent`, so it can never render |

\* pending the 7.1.1 re-check above.

`games/suvat/` is the **reference implementation** of the fix. Categories A, B and C are
worked **one game at a time, each played through before the next** — never as a sweep.
Sweeps `96381d74`, `76514c70` and `4b3d7d3` are precisely why.

### 7.1.2 Marking tolerances — never wide enough to accept a named wrong answer

Ruled by Jon, 1 Oct 2026.

**A tolerance must never be wide enough to accept a named wrong answer. A scale-based band is
capped below half the gap to the nearest one.**

- **What counts as a named wrong answer:** a specific value a student reaches by a specific
  mistake. A "wrong" value equal to the key is not wrong, and does not cap anything. The two
  worked examples, both ruled by Jon on 1 Oct 2026, are below.
- **Why the cap is below half the gap:** no single typed value can then be marked correct against
  the key and also equal the wrong answer, or sit nearer to it. A student who read the wrong line
  is never told they were right.
- **A value read from a table of exact values is marked exactly,** with a floating-point guard
  only. Equivalent forms such as 35.5 and 35.50 are the same number. A value estimated from a
  drawn graph takes a scale band (2.5% of the axis span, twice that for a difference of two
  readings), capped as above.
- **Every number-line placement snaps to a grid containing every target, is marked by exact match
  through `MaffsNumberLine`, and offers step buttons on phones** (Jon, 5 Oct 2026: Negative Number
  Line's ruling (a), then his ruling on the resit audit's Decimal Detective F4).
  `MaffsNumberLine.placementCorrect({placed, target, mode: 'snapped'})` (`schools/assets/number-line.js`,
  1e-9 guard only): a band of a grid step or more would accept a neighbour, a named wrong answer.
  There is no other mode: 'continuous' (a freely dragged marker marked by a band) was removed, and any
  mode but 'snapped' throws, so no game can bring a tolerance band back through the helper. ◀ ▶ step
  buttons (at least 44px) and the arrow keys move a placed marker one grid step, so a phone reaches every
  position. Decimal Detective's marker shows no value until Check (F4: a live readout gave the answer
  away); Negative Number Line's marker label is a separate question for Jon. Held in CI by
  `scripts/verify-negative-number-line.py` and `scripts/verify-decimal-detective.py`.

**Worked example 1, box plots** (Chart Interrogator).
- **For a median:** the other group's median, and the box's own Q1 and Q3 (an edge read for the
  median line).
- **For an IQR:** the other group's IQR, and either group's range (the range given for the IQR).
- **Effect:** no median is capped. The IQR is capped in 8 of 10 plots.

**Worked example 2, cumulative frequency** (Chart Interrogator).
- **For a quartile:** the other two quartiles, and the quartile's own position on the cumulative-
  frequency axis: n/4, n/2 or 3n/4. This is the position given for the value, the classic
  cumulative-frequency misconception.
- **For the IQR:** the position difference n/2, and the axis range.
- **For the benchmark count:** its complement, n − count (the count read off the curve without
  subtracting it from n).
- **Effect:** only CF5's median is capped, from ±1.5 to ±1.047. Its true median of 37.9 sits 2.1
  from n/2 = 40. Every pixel-measured reading of the drawn curve still passes.

**Where it came from.** Chart Interrogator's box plots took the 2.5% / 5% band on 1 Oct 2026
(todo §1.16). In 7 of 10 plots, the 5% IQR band then held the other group's IQR, so measuring the
wrong box was marked correct.
- `capTol()` in `games/chart-interrogator/index.html` is the implementation for both examples.
- `scripts/verify-chart-interrogator.py` (in CI) recomputes every band. Its self-test puts a band
  back uncapped and must fail.

### 7.1.3 Money answers — the format standard

Ruled by Jon, 2–3 Oct 2026.

**A typed money answer is compared with the key as a number first. Its written form is then checked
separately, and a wrong form is never a mark.**

- **Pence answers are written to exactly 2 d.p.:** £114.40, never 114.4. **1 d.p. is never accepted**,
  and neither are 3 or more.
- **A whole number of pounds needs no .00:** 3050 and 3050.00 are both right. 3050.0 is the wrong form.
- **Right amount, wrong form → the format check, not a mark.** The step is not marked right or wrong,
  no penalty or analytics event is recorded, and the student is told: "Right amount, but money always
  has two decimal places. In the exam, £1250.7 loses the mark. Fix it and resubmit." (with their own
  figure). The corrected resubmission is marked correct.
- **Wrong amount → marked wrong as normal.** No tolerance band: a penny out is wrong.
- **Keys are exact to the penny**, worked from the figures the student can see (never unrounded
  internals); where the maths rounds, the question says "Give your answer to the nearest penny" and the
  key rounds half up. Worked answers are shown in full money form (£30,432.00, £1,133.33).
- **Where it came from.** Jon's 2 Oct ruling that "whole pounds" are fine was misread as "round money
  answers to whole pounds" (todo §1.36's tax-theft line, corrected 3 Oct 2026). It means only that a
  whole-pound amount needs no .00.
- **A leading £ or € is optional** (Jon, 3 Oct 2026): £12.34 and 12.34 are the same answer. A money input
  is `type="text" inputmode="decimal"`, because a `type="number"` input silently empties on a typed £.
- **Implementation, REQUIRED for every typed numeric answer:** `MaffsAnswer` in
  `schools/assets/answer.js` (3 Oct 2026). No game marks a typed number with its own code or a
  tolerance band. It reads the raw typed string, never a number the game parsed (114.4 and 114.40 are
  the same number, not the same answer), and returns `'correct'`, `'wrong'`, `'format'` or
  `'unreadable'`. `'format'` and `'unreadable'` are never marked: no score change, no penalty, no
  analytics event; the game shows `MaffsAnswer.message(...)` and the student resubmits.
  - `money(raw, key)`: this section's rule. Key in pounds (or euros) at the penny.
  - `decimal(raw, key, dp)`: **the question states its precision** ("Give your answer to 1 decimal
    place") and the key is the exact answer rounded half up to it. Any form equal in value is correct
    (2.5 and 2.50). A value that rounds to the key but isn't equal to it is `'format'`, with the words
    "Right value, but the question asks for 1 decimal place. In the exam, 333.33 loses the mark. Fix it
    and resubmit." (with the student's own figure). Anything else is wrong.
  - `exact(raw, key)`: an answer that needs no rounding (whole-number ratios, integer scale factors).
    Equal in value or wrong; nothing is `'format'`, since no precision was asked for.
  - `fractionOrDecimal(raw, num, den, dp)` (7 Oct 2026): the key is the exact fraction num/den, and the
    question accepts it as a fraction or as a decimal to its stated precision. A typed fraction (a/b, a
    sign on either part, any equivalent form: 3/7, 15/35) is read exactly by `fraction(raw)` and is
    correct or wrong, never `'format'`. Anything else goes to `decimal()` against num/den rounded half up,
    in integers, to dp places. `decimal()` and `exact()` still read no fractions.
  - `message(..., {sf: n})` names significant figures where the question states them (the marking is
    still at its dp places); `{fraction: true}` asks for "a fraction or a decimal" when unreadable.
  - **A question whose exact answer doesn't terminate must state its precision.** An unstated
    rounding is a key bug, not a marking choice.
  - Users: `tax-theft` (keys in pence; `moneyResult()` is now a one-line adapter, kept so its
    verifier's self-test can still patch it), `split-it`. The other money games move onto it under
    todo START item 5. `scripts/test-answer-js.py` (CI) tests every outcome, and shows `money()`
    equal to tax-theft's old rule on every string a `type="number"` input can pass.

### 7.1.4 UK tax, NI and student loan rates in use

Ruled by Jon, 3 Oct 2026.

**Teaching year: 2025/26.** Every game that states or uses UK income tax, National Insurance or a
student loan uses the 2025/26 figures below, for England, Wales and Northern Ireland (never Scottish
rates).
**Why 2025/26, not the current tax year:** exam papers are set well before the tax year they are sat
in, so the June 2027 series most likely uses 2025/26 figures.

**The April rule: each April, advance the teaching year by one** (2025/26 → 2026/27 in April 2027;
Jon, 3 Oct 2026). Jon has a yearly 1 April calendar reminder, and CI enforces it: `scripts/uk_rates.py`
holds `REVIEW_BY` (now 30 April 2027), and `scripts/check-tax-year.py` warns from 1 April and fails
after `REVIEW_BY` until the year is advanced. Advancing is one PR: `TEACHING_YEAR`, `REVIEW_BY` and
the figures in `scripts/uk_rates.py`, this table, and every game `check-tax-year.py` registers.

| Figure | 2025/26 | Source |
|---|---|---|
| Personal allowance | £12,570 | [Rates and thresholds for employers 2025 to 2026](https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2025-to-2026) |
| Allowance taper | −£1 for every £2 of adjusted net income over £100,000; zero at £125,140 and above | [Income over £100,000](https://www.gov.uk/income-tax-rates/income-over-100000) |
| Basic rate, 20% | the first £37,700 of **taxable** income | employers 2025 to 2026 (above) |
| Higher rate, 40% | taxable income £37,701 to £125,140 | employers 2025 to 2026 (above) |
| Additional rate, 45% | taxable income above £125,140 | employers 2025 to 2026 (above) |
| Employee Class 1 NI, primary threshold | £12,570 a year (£242 a week, £1,048 a month) | employers 2025 to 2026 (above) |
| Employee Class 1 NI, upper earnings limit | £50,270 a year (£967 a week, £4,189 a month) | employers 2025 to 2026 (above) |
| Employee Class 1 NI, main rate | 8% between the primary threshold and the upper earnings limit | employers 2025 to 2026 (above) |
| Employee Class 1 NI, above the UEL | 2% | employers 2025 to 2026 (above) |
| Student loan, Plan 1 | 9% above £26,065 a year | employers 2025 to 2026 (above), "Student loan and postgraduate loan recovery" |
| Student loan, Plan 2 | 9% above £28,470 a year | employers 2025 to 2026 (above) |
| Student loan, Plan 4 | 9% above £32,745 a year | employers 2025 to 2026 (above) |
| Student loan, Plan 5 | no 2025/26 threshold: repayments began April 2026 | [What you pay](https://www.gov.uk/repaying-your-student-loan/what-you-pay) (rate 9%) |
| Postgraduate Loan | 6% above £21,000 a year | employers 2025 to 2026 (above) |

- The bands apply to **taxable** income (salary minus the allowance), so the basic band does not widen
  when the allowance tapers (canon §7.1.3's tax-theft, todo §1.36).
- **One copy in code:** `scripts/uk_rates.py`. Verifiers import it, as statistics verifiers import
  `stats_common.py`; none restates a rate. `verify-tax-theft.py`, `verify-core-maths-paper1-tax.py`
  and `verify-better-value-tax.py` use it.
- **gov.uk's "What you pay" page always shows the current year's thresholds** (2026/27 when checked),
  so take a teaching year's figures from that year's "Rates and thresholds for employers" page.
- **Checked in CI:** `scripts/check-tax-year.py` registers every game that states or uses UK tax, NI
  or student loans. A game that does so without being registered fails, so does a registered game
  that states a tax year other than the teaching year, and so does the April rule above.

## 7.2 KaTeX Reference — Common Patterns

| **Pattern** | **LaTeX** | **Output** |
| --- | --- | --- |
| Log base a | `'\\log_a(b)'` | log_a(b) |
| Natural log | `'\\ln x'` | ln x |
| Inline fraction | `'\\tfrac{1}{2}'` | 1/2 |
| Display fraction | `'\\dfrac{a}{b}'` | a/b |
| Square root | `'\\sqrt{x}'` | sqrt(x) |
| Cartesian (Further Maths) | `'a + bi'` | a + bi |
| Cartesian (Level 4) | `'a + bj'` | a + bj |
| Exponential form | `'r e^{i\\theta}'` | re^(itheta) |
| Polar (Level 4) | `'r\\angle\\theta'` | r angle theta |
| 2x2 matrix | `'\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}'` | matrix |
| Column vector | `'\\begin{pmatrix} x \\\\ y \\end{pmatrix}'` | column vector |

### Answer Matching — Critical Rule

```js
// ALWAYS use dataset.val — NEVER compare innerHTML or rendered KaTeX
btn.dataset.val = latexString;
if (b.dataset.val === q.correct) { /* correct */ }
```

## 7.3 Standard Scoring Formula

```
score = max(1, round((BASE - penalty) * multiplier))
penalty = guesses * G_COST + hints * H_COST
multiplier = 1 / (1 + T_K * ln(1 + seconds))
```

Logarithmic time decay — fast solves rewarded, slow solves not catastrophically punished.

## 7.4 Branding Assets

| **Asset** | **Path** | **Notes** |
| --- | --- | --- |
| Full logo | schools/assets/m_plus_logo.svg | Navy M with white plus, two teal bars |
| Favicon | schools/assets/favicon.svg | Icon-only mark on navy rounded rect |
| OG image | schools/assets/og-image.png | 1200x630 PNG (converted from SVG) |

## 7.6 Advancing to the next question

Added 22 Sep 2026. **This supersedes the earlier "a wrong answer holds ~4.5s" rule**, which was an
interim fix and is retired — do not reintroduce a fixed wrong-answer timer.

- **A correct answer advances briskly** on whatever short delay the game already uses. A student who
  got it right should not be held up.
- **A wrong answer shows a `Next →` control and waits for the student.** They decide when they
  have read it. A generous auto-advance fallback (`MaffsNext.FALLBACK_MS`, 20s) exists only so a
  walked-away tab still finishes; it is a safety net, never the mechanism.
- **Any pause must have something on screen worth reading.** A pause with only "WRONG!" behind it is
  worse than no pause — it wastes the student's time and teaches nothing. Show the working, the
  step, or the misconception before handing over to the control.

Use the shared helper, do not hand-roll it:

```js
// after showing the working on the wrong path
MaffsNext.wrong({ mount: someElement, onAdvance: loadQuestion });
// and at the top of the load-next-question function
if (window.MaffsNext) MaffsNext.clear(someElement);
```

`schools/assets/next-control.js`, loaded alongside the other shared assets.

**What the helper guarantees** (1 Oct 2026; `scripts/test-next-control.py`, in CI):

- **A 3-second floor.** For `MaffsNext.FLOOR_MS` (3000ms) after `wrong()` mounts, Next is visibly
  disabled (dimmed, and a faint fill crosses it once; dimmed only under `prefers-reduced-motion`), and
  no click, Enter, Space or call to the returned `advance()` moves on. Jon's ruling of 29 Sep 2026: the
  explanation is on screen for at least that long, platform-wide (probability-pioneer's own 5s floor
  predates it and is its own). The floor is separate from the 20s fallback and from any game's
  `fallbackMs`, which run on their own clock.
- **Advance once.** `onAdvance` runs at most once per `wrong()` call, however it is triggered: a click,
  Enter or Space on the focused control, a game's own key handler calling the returned `advance()`, or
  the fallback. A game that handles Enter itself routes it through `advance()`.
- **`clear()` cancels.** Removing a control cancels its fallback and floor timers and its listener, so
  nothing it scheduled can fire after the game has moved on. A new `wrong()` on the same mount clears
  the old one first. (Found in phone-fit batch 1: the old `clear()` left the fallback running, so a game
  that advanced on Enter could skip a question 20 seconds later.)
- **A 44px target.** The control is at least 44px tall and wide.

**Why.** Advance delays had been tuned per game by guesswork: 800ms to 2400ms across 25 games, and
not one distinguished a right answer from a wrong one. No single number fits every reading speed —
too short and a slower reader never learns why they were wrong, too long and a quicker one is held
against their will. The fix is to stop picking a number.

**Rulings on feedback and replay (Jon, 8-9 Oct 2026; contract RULINGS-9OCT):**

- **Feedback on a wrong answer is shown, not skipped** (Jon, 8 Oct). A pause that holds the feedback on
  screen before the student can move on is allowed, and is the game's own: wrong-on-the-internet keeps its
  3 s pause before Try again (9 Oct). Do not shorten or remove it to speed play up.
- **Play Again may replay the mode just played, in the page** (complex-converter, 9 Oct), provided the
  game's mode menu is still one tap away from the end screen (complex-converter's end screen has Menu
  beside Play Again). A game whose end screen offers only Play Again adds a "Choose mode" control there.

**Rulings on skipping, logging and displayed numbers (Jon, 8-9 Oct 2026; recorded by contract DOCS-9OCT):**

- **Skip shows the answer and waits on Next** (Jon, 9 Oct, graph-transformer: "the learning needs to be shown not
  skipped"). A question's Skip, Give up or Reveal control shows the answer (and the working, where the game has
  it), then waits on Next; it never jumps straight to the next question. It holds for every such control, not one
  game's fix. (The initials overlay's Skip, which skips a leaderboard entry, is not a question control.)
- **A multi-part item logs one `question_answered` row per answer, not per question** (Jon, 8 Oct, Screening Room
  t4-017). Its gut check and its worked figure are two answers, and logging both shows where a student goes wrong. An
  analysis that counts questions groups by `question_index`; do not merge the rows in the game.
- **Number formatting is display-only; marking reads the stored value** (Unit Converter, UC-FIX, 8 Oct). Thousands
  separators (a comma for every number of 1,000 or more) go in prompts, options, keys and worked solutions as text;
  `dataset.val` and every value marking compares stay as the game stores them. A change that would alter what is
  marked right is a STOP, not a formatting fix.
- **"≈" for a rounded conversion factor, "=" only for an exact definition** (Jon, 9 Oct, Unit Converter t4-007:
  "1 mile ≈ 1609 m"; "1 inch = 2.54 cm" is exact). A verifier fails "=" before a stated conversion that is not
  the exact definition.

### 7.6.0 Answer once — MaffsLock (7 Oct 2026, contract F1)

**Every game marks through MaffsLock; no local answered flags.** `schools/assets/answer-lock.js`
(`MaffsLock`, loaded with `next-control.js`) is the one guard on input. The audits found the same faults
in 30+ games (register class 1): an option "locked" by a CSS class only, so Enter or Space still fired it;
a double-click on Next whose second click answered the next question; Check live during the pause;
stale timers that fired after the student moved on (two games finished and submitted twice).

- **`if (!MaffsLock.lock(container)) return;` first in every answer handler.** The first call for a
  question disables every answer control in the container (`disabled` and `aria-disabled`) and drops any
  later click, key or touch on them before the game's listeners see it; a second call returns false.
- **`MaffsLock.fresh(container)` when a question or screen renders:** all input on it is ignored for
  `FRESH_MS` (300ms), so the second click of a double-click, a second Enter or a double-tap lands on
  nothing. `MaffsLock.screen(container)` is a screen change: timers cleared, then fresh.
- **Every screen change goes through `MaffsLock.screen()`** (contract PLAY-AGAIN-SCREEN, 9 Oct 2026): a
  game's `show(id)` ends with `MaffsLock.screen(<the screen shown>)`, so Play Again, back to menu, mode select
  and results all open the fresh window on the new screen. A bare screen change put the menu under the
  pointer at once, and a double-click's second click took the student to `/leaderboards/`.
  `check-answer-lock.py` double-clicks Play Again in every migrated game: the second click must leave the
  page where it is and land on nothing the new screen has not covered.
- **Every per-question and per-screen timer is `MaffsLock.timer(fn, ms)`.** `MaffsNext`'s advance and
  `screen()` clear them all, so a stale timer can never fire.
- **The end-of-game handler is `MaffsLock.finishOnce(fn)`**: `game_completed` and `submitScore` run at
  most once per session; `MaffsLock.newSession()` starts the next run.
- A control MaffsNext mounts, or anything inside `data-maffs-lock-skip`, is never locked.
- Checked by `scripts/test-answer-lock.py` (the asset, with planted faults) and
  `scripts/check-answer-lock.py` (every migrated game played in Chromium; `NOT_YET` may only shrink).
- **Adopting MaffsLock includes the game's lock-hint declaration; the game passes `check-answer-lock.py`**
  (contract LH, 7 Oct 2026). The declaration says how the check produces a wrong answer. It is the game's
  own fact, so it lives in the game's page, never in the shared script: one HTML comment,
  `<!-- maffs-lock-hint ...` then a JSON object, then `-->`. Its keys are `answer` (JS that submits an
  answer, given `i`; it may return a promise), `ready`, `start`, `start_sel`, `level`, `surface`, `keys`,
  `each`, `mark_any` and `repeat` (check-answer-lock.py's `HINT_KEYS` documents each). A JS value may be a
  list of strings, joined with nothing between them. `{}` declares a game the generic driver plays unaided.
- **The check is deterministic: a verdict never depends on a draw or on timing** (contract DET, 8 Oct 2026).
  Every page's `Math.random` is seeded (`--seed`, default 1, printed in the check's first line), so a seed
  plays the same questions and gives the same event log every run. The driver never waits a fixed time on
  the path to a wrong answer: it taps only when no fresh window is open (`MaffsLock.isFresh()`, read-only),
  takes the next question as up only once it has rendered (a new `fresh()` call, or an enabled option
  group) and its window is over, and a tap the page sees land in a window is made again once it closes.
  A failure is fixed in the driver or the declaration, never with a retry. **A two-option game declares an
  `answer` that picks the option differing from its own key** for attempts `i >= 1` (the wrong answer then
  comes first time on every draw); for `i = 0` (the tap-through) it presses the first option, as the
  generic driver does. prime-or-composite, fraction-equivalence and factor-race are the pattern.
- **Script order is free.** answer-lock.js and next-control.js do not read each other at load (MaffsNext
  asks for `window.MaffsLock` only when it advances), so either may load first.
- **The home lane adds a game to `MIGRATED`.** A game the cloud lane migrates is judged in full as soon
  as its page loads the lock. Its failures are reported, not failed, only while it is on the
  `cloud-remaining:` line in `docs/handover/cloud.md`. Once the cloud lane takes it off that line, a failure
  fails CI.

### 7.6.1 The phone rule — the reason and the control both above the fold

Added 30 Sep 2026 (Jon's contract; first built in `six-sevens-bruv`).

**On a narrow screen, hide the controls that cannot be used during the feedback, and collapse the
secondary panels, so the reason to read and the `Next →` control both sit above the fold.** A
student who has to scroll to find Next either never reads the reason (they hunt for the button) or
never finds the button. Measure against the viewport minus the site footer, which is fixed and
40px tall.

- **Hide what cannot be used.** An answer keypad is locked while the feedback shows, so it is
  hidden, and the feedback takes its space. On a **wrong** answer only: a right answer shows one
  line for a moment, and hiding the keypad then makes it vanish and return under the student's
  thumb on every right answer.
- **Collapse secondary panels** on screens 600px wide or narrower. A progress picture (Six
  Sevens' 12 × 12 grid) becomes a one-line bar ("13 / 78 gold") that opens on tap, with
  `aria-expanded`, and at least 44px tall. The end-of-session screen still shows it in full.
- **Order: the fact → the hint → the picture → Next.** The reason to read always comes before the
  control.
- **Shrink a picture without changing what it says.** Smaller dots on a narrow screen, but every
  dot drawn (see "Scaffolds fade" in §12: a count is never scaled).
- **When the picture still cannot fit on a short screen (600px tall or less), it moves below Next.**
  This is a fixed CSS rule, not a per-question measurement, so the same phone always gets the same
  layout. It changes the visual order only; the reading order stays fact, hint, picture, Next.
  **The hint never moves below Next.**
- **Keep the title and the Aa toggle on one line during play** on narrow screens, rather than
  wrapping the toggle under the title.
- **Never shrink a tap target below 44px** to make room.

**When the asking screen may scroll (Jon, 1 Oct 2026).** Only when the content needed to answer cannot
fit: when the question itself (Better Value's scenario, two deals and four conclusions; Expected Damage's
two track cards on its longest questions) is taller than the screen at a legible size. The feedback screen
must always fit: the reason and Next above the fold, by folding away what cannot be used and, on a short
screen, moving a picture below Next. Record each game that takes this exception in todo §3.9.

**How it is checked.** Measure the wrong-answer screen at 320 × 568, 375 × 667 and 390 × 844, for
every question shape the game can produce, not a sample: Six Sevens was measured on all 144
orientations of its facts. Record where Next lands, confirm there is no horizontal scroll at 320px,
and confirm the on-screen order. Free Daily Pizza, whose pictures also sit behind `MaffsNext`, is
built to this rule and measured on all 518 items at all three sizes by `scripts/verify-free-daily-pizza.py`
(30 Sep 2026). There the stage label hides during the feedback and pictures shrink, but a fraction is
never shrunk: Jon's ruling, every fraction on screen stacked and big enough to read, never 1/3.

**Known gap (30 Sep 2026): the Aa (OpenDyslexic) mode.** Its wider spacing and double line height
make the hint much taller, so in Six Sevens Next still lands below the fold at 320 × 568 and
375 × 667 with Aa on. That is much better than before (1,077–1,268px down the page before,
595–850px after) but not fixed. **Ruled 1 Oct 2026 (Jon): fixed once, in its own contract, across `six-sevens-bruv`, `free-daily-pizza`
and `new-shapes`** (New Shapes' parallelogram asking screen is 11px over at 320 × 568 in Aa; Free Daily
Pizza is not yet measured in Aa). Extending the picture-below-Next fallback to Aa mode on every phone is
the obvious candidate; all three load the shared `schools/assets/opendyslexic.css`. See todo §3.9.

## 7.5 Theme

**Every game takes one register (Jon's ruling, 2 Oct 2026).** It replaces the three-row table
(portal; light/playful Nunito + Press Start 2P for KS3; dark for GCSE+) and the lowest-tier rule
that chose between them.

**Why.** The priority audience (§0) is students working at grades 1–3, and post-16 resitters above
all. The old table assumed the youngest person in the room is the one the content is pitched at.
For these students that is false by design: the maths is basic because they missed it, not
because they are young, and a 17-year-old handed a pastel, pixel-font times-tables game has been
told what the site thinks of them before the first question. A Year 7 loses nothing by being
spoken to as an adult; a resitter loses a great deal by being spoken to as a child. **The fun
comes from the mechanic, not the font.** The reference is Oak National Academy: calm, credible,
the same look whatever the age. This reasoning was first ruled for the resit strand alone (30 Sep
2026, `six-sevens-bruv` the first game under it); this ruling makes it the rule for every game.

**The register.**

- **Fonts: Outfit for text, JetBrains Mono for numbers and code.** No other font family, except
  OpenDyslexic in Aa mode, which wins over both.
- **No emoji in the game header** (`<h1>`).
- **Student-facing copy is age-neutral**: no year group, no key stage, no "primary" or "secondary
  school", no "when your teacher introduces this". A level's *name* on a button may still be a
  qualification (GCSE, A-Level, Core Maths); a key stage or a year group is replaced by what the
  level does (Split It's KS3 button reads "Foundation", Jon's ruling of 2 Oct 2026; a third level, if a game has one, is "Advanced"; a Year 6 level is "Starter", SR-11). **Level keys never change**: the Firebase leaderboard keys (`ks3`, `gcse` …) stay as they are, and the label a student sees is declared once per game and read by the leaderboard hub too (§3.12; it folds into `games.json` when that is built).
- **Each game keeps its own `--accent`** (and `--accent-dim`). The level colours of §3.1 are portal
  chrome and are not a game's accent.
- **A light or a dark palette, set by the rule below**, never chosen per game.

**The palette rule.** A game whose roster levels include **Year 6, KS3 or GCSE** takes
`data-theme="light"`. A game serving **only** A-Level, A-Level Year 2, Further, Core, L3 or L4
takes `data-theme="dark"`. Core Maths is dark (Jon's ruling, 2 Oct 2026); a game serving GCSE and
Core is light, because it includes GCSE. The palette is **derived from the Levels column of
`.claude/rules/game-roster.md`**, never chosen and never set by editing the roster: the only copy of
the rule is `palette()` in `scripts/check-theme.py`, and a level label it does not know fails CI
rather than taking a default. On 2 Oct 2026 the roster gives 67 games light and 30 dark. Three live
games move from light to dark (`differentiation-duel`, `integration-duel`, `log-laws`, the
light-slate sub-family §7.5 used to leave alone) and 53 move from dark to light (listed in to-do
§3.12). Withdrawn `regression-rumble` is dark by the rule if it returns.

**One stylesheet: `schools/assets/theme.css`.** It holds the base tokens, the two palettes (chosen
by `data-theme` on `<html>`) and the font stacks, and loads both fonts itself. Base tokens, which a
game never redefines: `--bg`, `--surface`, `--surface-alt`, `--text`, `--muted`, `--border`,
`--correct`, `--wrong`, `--hint`, `--font-text`, `--font-num`. A game sets `--accent`,
`--accent-dim` and any non-base tokens of its own (Split It's three ratio-bar part colours), all in
its `:root`; a colour hard-coded anywhere else becomes a token. Write every font as
`var(--font-text)` or `var(--font-num)`: in Aa mode `theme.css` switches both tokens to
OpenDyslexic, so every element follows (before, any element with its own `font-family`, such as
Split It's pixel-font score, stayed out of Aa mode). Aa mode keeps the per-game snippet's
reduced-glare backgrounds, now as tokens: cream `#fdf6e3` on light, deep navy `#12141f` on dark. The
light palette sits beside the portal: white surfaces, navy `#1a2744` text. `theme.css` coexists with
`opendyslexic.css` (font faces only) and `site-footer.css` (its own colours, no font) and edits
neither. The portal (root `index.html`) is not a game and keeps its own stylesheet.

**Contrast, measured 2 Oct 2026** (WCAG AA is 4.5:1 for text; every pair passes). Tint is the
token on a 10% mix of itself into `--surface`, the feedback-panel pattern.

| Light | on `--bg` `#f8fafc` | on `--surface` `#ffffff` | on `--surface-alt` `#f1f5f9` | on Aa `--bg` `#fdf6e3` | on its tint |
|---|---|---|---|---|---|
| `--text` `#1a2744` | 14.16 | 14.81 | 13.52 | 13.73 | – |
| `--muted` `#526077` | 6.09 | 6.37 | 5.81 | 5.90 | – |
| `--correct` `#166534` | 6.81 | 7.13 | 6.51 | 6.61 | 6.14 |
| `--wrong` `#b91c1c` | 6.18 | 6.47 | 5.91 | 6.00 | 5.45 |
| `--hint` `#a14a05` | 5.74 | 6.00 | 5.48 | 5.57 | 5.20 |

| Dark | on `--bg` `#0f1420` | on `--surface` `#182033` | on `--surface-alt` `#212b42` | on Aa `--bg` `#12141f` | on its tint |
|---|---|---|---|---|---|
| `--text` `#e8ecf4` | 15.54 | 13.71 | 11.91 | 15.48 | – |
| `--muted` `#a3adc2` | 8.16 | 7.20 | 6.26 | 8.13 | – |
| `--correct` `#4ade80` | 10.56 | 9.32 | 8.09 | 10.52 | 7.58 |
| `--wrong` `#fb7185` | 6.84 | 6.03 | 5.24 | 6.81 | 5.25 |
| `--hint` `#fbbf24` | 11.02 | 9.73 | 8.45 | 10.98 | 7.91 |

A game's accent is its own to measure: Split It's `#15803d` is 5.02 on `--surface`, 4.79 on `--bg`,
4.65 on the Aa cream. Change a token only with the table re-measured.

### 7.5.1 How it is checked, and how a game moves onto it

`scripts/check-theme.py` runs in CI (Tiers 1 + 2 job). Every roster game is in one of two lists in
the script. **MIGRATED**: every rule is enforced and a breach fails CI — links `theme.css` once in
`<head>`; `<html>` carries the `data-theme` the rule gives; no `font-family` outside the stacks and no
Google Fonts link of its own; no base token redefined in the game's CSS or script; no hex colour
literal outside `:root`; no emoji in `<h1>`. **NOT_YET**: the same findings and the game's expected
palette are reported and never fail. It also reports, for Jon to rule on, the age-specific wording in
each NOT_YET game's static page text (its start screen; text a script builds is not read).

**Migration is per game, never by sweep.** Two site-wide sweeps once left `chart-interrogator` and
`modular-battle` dead for six months. A game moves from NOT_YET to MIGRATED in the PR that migrates
it, with its phone fit re-measured (§7.6.1) in normal and Aa mode (`measure-phone-fit.py --aa`) and
its wording changes quoted for Jon. The order is in to-do §3.12: the resit suite (the audit's candidate list, `docs/resit-coverage-audit.md` §10.5; not the two-game resit strand, to-do §3.13) first, each
game's migration and its phone-fit fix done together, three at a time. **A new game is built to the
theme and goes straight into MIGRATED.** If a game can only look right by redefining a base token,
the token set is wrong: report it, never add an exception.

**Why this section was rewritten.** The old rows needed a tie-break (the lowest-tier rule, added 22
Sep 2026 after `suvat`, `trig-worms` and `modular-battle` were found in KS3 styling while serving no
KS3 tier), then an exception (the resit strand, 30 Sep 2026), and still drifted: the 30 Sep resit
audit (`docs/resit-coverage-audit.md` §5) found 12 games rendering a different row from the one canon
gave them, six still rendered pixel or rounded fonts, and colour names differed from game to game
(`--accent` and `--primary`, `--correct` and `--green`). Every game styled itself from scratch and
nothing was checked, the footer's failure before §7.5.2. One register, one stylesheet, one derived
palette and one check replace the rows, the tie-break and the exception.

### 7.5.2 The site footer — one markup, one stylesheet, checked in CI

Added 2 Oct 2026 (to-do §1.28). Every page carries the same footer: a fixed navy (`#1a2744`) bar,
exactly 40px, one line. Its look lives only in `schools/assets/site-footer.css`; its markup, nine
root-absolute links (About · Leaderboards · Spec Map · Parent guides · What's changed · Contact ·
Privacy · Feedback · ☕ Support MaffsGames), lives only in `scripts/check-footer.py` as `CANONICAL`.
`scripts/apply-footer.py` writes both into every page (idempotent); `check-footer.py` fails CI on a
page without the footer, a footer that differs by a byte, a missing stylesheet link, or any
`.site-footer` rule outside the shared stylesheet. Exempt pages, each with its reason, are listed
in `check-footer.py` (escape rooms and their teacher pages, redirect stubs).

**On a narrow screen the links scroll sideways inside the bar** (Jon's ruling, 2 Oct 2026, option
a): `justify-content: safe center` centres them when they fit and start-aligns them when they do
not, so none is lost off the left edge; a CSS-only shading cue sits on whichever edge has more;
every link is a 40px-high tap target; below 480px the Support link reads "☕ Support". **The bar
stays exactly 40px**: every game's phone fit (§7.6.1) measures its fold as the viewport minus it.

**Never hand-copy the footer or its CSS into a page.** It was copied by hand into 125 pages until
October 2026; the copies drifted into four link sets, and all of them shared one defect (on a phone
the links ran off both edges and could not be reached). To change it, edit `CANONICAL` or the
stylesheet, run `apply-footer.py`, then `check-footer.py`. A new page needs only
`<footer class="site-footer"></footer>` before `</body>`; a page gaining the bar for the first
time needs `padding-bottom: 40px` (or equivalent) so the bar covers nothing.

### 7.5.3 Name the maths, never the student (Jon, 7 Oct 2026; contracts ESSENTIALS and ESSENTIALS-WORDING, 8 Oct)

**Student surfaces describe the topic and level only; only teacher surfaces may say resit or post-16.** A link
posted in Google Classroom or Teams shows its page's description and og/twitter tags to the whole class. Until
8 Oct 2026 the two rooms built for a resit class opened "A GCSE resit escape room on...", and the portal's
cards said "for a GCSE resit class". Until the same evening /essentials/ was a teacher surface and /updates/ was
never scanned, so both still said "resit" ("resit page", "resit students", a link to /resit/).
**Jon, 8 Oct 2026: the section is "Essentials" everywhere public; no public page labels a student as a resitter.**

- **Student surfaces:** every game and escape-room page, including its description, og and twitter tags; the
  portal and /escape-rooms/ cards; /essentials/ and its metadata; /updates/. They say, e.g., "A GCSE escape
  room on factors, primes and HCF".
- **Teacher surfaces:** each room's teacher.html, and the teacher and parent guides, only. They may say resit
  or post-16.
- **Checked by `scripts/check-student-labels.py`** (CI, site-wide checks): "resit", "retake" or "post-16" in a
  student surface's visible text, script strings or description/og/twitter tags fails. Code comments and docs
  are exempt. A page whose label is maths content rather than a label on the player is in its `KNOWN`, with
  the reason: reported, never failed, and stale once the label is gone (given-that's tree-diagram question
  about students re-sitting, 8 Oct 2026, awaiting Jon's view).
- **/essentials/** (until 8 Oct 2026 /resit/, which now redirects there, as /schools/spec-map/ does) is headed
  "Essentials", with the teacher line "GCSE Foundation maths for students working at grades 1–3, in school or
  college."
- **A site fact is never hand-typed beside its data.** The homepage title and description carry no game or
  room count (each was stale within a week: "96 games" while the portal listed 91); the range reads "KS3 to
  Further Maths" everywhere on the homepage.

## 7.7 What the site publishes — SITE and INTERNAL

GitHub Pages builds `main` with Jekyll and publishes every tracked file except dot-paths
(`.claude/`, `.github/`), `_`-prefixed paths and the `exclude:` list in `_config.yml`. Until
October 2026 there was no `_config.yml`, so `CLAUDE.md`, `docs/`, `scripts/` and `data/` were all
public web pages on maffsgames.co.uk.

- **Every tracked path is SITE or INTERNAL.** SITE is what a live page needs at runtime or by link:
  the pages, `schools/`, `escape-rooms/`, `games/`, the root files, and `docs/art/` (the escape
  rooms' pictures). Everything else is INTERNAL and is excluded in `_config.yml`.
- **A live page must never fetch, load or link an INTERNAL file.** It would 404 on the live site.
  Anything a page needs belongs under a SITE path.
- **Classify every new top-level path, and every new kind of file in `docs/`, in both places**:
  SITE in `scripts/check-publish-scope.py`, or INTERNAL in `_config.yml`. Jekyll has no allow-list,
  so the check fails CI for any published file outside SITE, any excluded SITE path and any SITE
  reference to an unpublished file. Do not add a `.nojekyll`: it would publish every INTERNAL path again.
- **No personal contact details in the repo.** The repo copy of the Apps Script holds a placeholder
  for the report address (`docs/apps-script-redeploy.md` says where it is set).

## 7.8 CI: what runs when (Jon, 4 Oct 2026)

**Why it changed.** The repository is public, so GitHub Actions minutes are free; the cost of a check is
the wall-clock time a PR waits. Every PR used to run every content verifier (Just Pythag It, Bruv alone is
about 9 minutes) whatever it touched, and the full suite was run again locally on Windows first. The cost
grew with the number of games, not with the size of the change.

| **Run** | **What runs** |
| --- | --- |
| Pull request | Every site-wide check (tiers 1-2 in four shards, links, footer, theme, publish scope, verifier coverage, spec map, public claims, tax year, /essentials/, student labels, calculator; tier 4 bank extraction and lint; the shared-asset tests; leaderboard coverage), plus the content verifiers `scripts/ci-deps.py` selects for the files the PR changes |
| Push to main (every merge) | **Everything**, every verifier: the safety net |
| Weekly (Mondays 05:17 UTC) and manual (`workflow_dispatch`) | **Everything** |

- **The selection is derived, never kept by hand.** `scripts/ci-deps.py` reads the checks (the site-wide
  jobs from `check-site.yml`, the "Content verifiers" groups from each script's `# ci-line:` header, §7.8.2;
  a content group is per-game, every other group site-wide) and works out each verifier's dependencies: the script and the local modules it imports;
  the repo files its literals name; each game it names (its whole folder, and every local file the
  game's page loads, followed through the shared JS and CSS); and any path its own `# ci-deps:` header
  names. A changed file selects every verifier
  that depends on it. A change to CI itself (`.github/`, `scripts/ci-*`, `requirements*.txt`) or a path
  in no known area runs everything. A verifier whose dependencies cannot be derived (it names no page and
  is not a library's self-test, or its pages load a file through a computed path) always runs; none does
  today. `python scripts/ci-deps.py --explain` prints the map.
- **Proven on every run:** the plan job runs `ci-deps.py --selftest` first. A change to one game's page
  selects exactly the verifiers that name that game; a shared asset selects every verifier whose game
  loads it; CI files and unknown paths select everything; a docs-only change selects none; every verifier
  is reachable from its own script.
- **The gate.** The `gate` job passes only if every job in the run passed (none failed, cancelled or
  skipped). It is the one check branch protection should require when Jon adds it.
- **Triggers.** `push` runs on main only (a branch's commits are checked through its PR), so a PR no
  longer runs every job twice; a new push to a PR cancels its running checks; runs on main are never
  cancelled. A red run on main or on the schedule is the signal: GitHub marks the commit and emails the
  workflow's owner.
- **Before pushing:** `python scripts/check-changed.py` runs the verifiers `ci-deps.py` selects for the
  branch, the fast site-wide checks, and the shared-asset tests when `schools/` changed; CI runs the rest.
  `--full` still runs everything locally, but is not required. Known Windows-only differences from CI:
  todo §4 item 18.

### 7.8.1 The CI layout: shards and parts (7 Oct 2026)

**Why.** Measured on 7 Oct 2026, runs started within seconds (no queue): the time went on run length. A PR
took about 8 minutes, because tier 1 and 14 more checks ran one after another in one job ("Tiers 1 + 2",
6.5 minutes). Main's full run took about 10.5 minutes, because Just Pythag It, Bruv's verifier ran alone
for 9m41s, and group B for 8 minutes. Nothing a check checks changed; only where it runs.

| Job | What it runs |
| --- | --- |
| Tiers 1 + 2 (shard 1/4 .. 4/4) | `check-site.py --shard i/4`: page k of its stable page order goes to shard (k mod 4) + 1, with all its level loads, level controls and phone-width checks. Tier 2, the roster-gap notes and the phone-overflow entries that name no page run once, in shard 1. Each shard first runs `--shard-selftest 4`: the four shards together are the unsharded page list, no page in two, and the workflow runs all four. |
| Site-wide checks | links, footer, theme, publish scope, verifier coverage, spec map, public claims, tax year, /essentials/, student labels, calculator, content safety, teacher line, search titles, findings register, quoted figures |
| Tier 4 layer A | bank extraction and its lint (together: the lint reads what the extraction wrote) |
| Shared asset tests | Next control, section clicks, answer.js, calculator, keypad |
| Content verifiers 1..n and Answer lock L1..Ln (the `content` job) | the per-game verifiers and the answer-lock parts, selected on a PR (above); since contract V the matrix is built in the plan job from each script's `# ci-line:` header (§7.8.2), not listed in the workflow, and since CI-BALANCE (9 Oct 2026) packed from measured times (below), not named by hand: the A, B1-B4, C1-C4, D1-D2, E and E2 groups this row described are gone, though their scripts' parts are as described here. C1-C4 are Just Pythag It, Bruv's `--part 1` .. `4`, dealt by measured cost; each first runs `--part-selftest` (the parts are exactly the unsplit task list, nothing twice, and CI runs every part). D1-D2 are Equation Builder's `--part 1/2` and `2/2`: each classifies every second candidate arrangement of every question (one question is 60% of the time, so it is split by candidate, not by question); the whole-question checks and the planted-fault self-test run in D1, and the self-test proves the two parts together fail exactly where the whole run does. B1-B4 were group B cut by the slowest time each line had taken (runners vary up to 1.8x). |
| Regenerate REGISTER.md | push to main only, after the Gate (§0.4) |

**Timings** (GitHub-hosted `ubuntu-24.04`, 4 CPUs):

| Run | Before (7 Oct 2026) | After |
| --- | --- | --- |
| One-game PR, longest job | Tiers 1 + 2, 6m34s (run 8m13s) | 3m03s, Tier 4 layer A (every site-wide job 1m40s-3m03s; a selected verifier adds its own job: most under 4m, Equation Builder 4m48s, B1 4m51s); run about 4-5m |
| Main's full run | 10m42s (C 9m41s, B 8m03s, Tiers 1 + 2 6m15s) | 5m45s (PR #95, which ran everything: B1 4m51s, D 4m48s, B2 4m30s; shards 1m40s-2m18s) |

The same evening (queue item 2) every content job was brought under 4 minutes: B in four, C in four, D in two.
Measured on the full run of the PR that did it (#103): every job 3m38s or less (A 3m38s, B2 3m29s, C4 3m10s, D1/D2 1m56s/2m03s); the whole run 4m47s (main after #99: 6m19s, with D 5m23s and B2 4m33s).

**Groups are packed from measured times (contract CI-BALANCE, Jon, 9 Oct 2026).** Until then each verifier
named its group by hand, and groups filled and drifted as verifiers were added and pages grew: on 9 Oct group E
reached 9m04s of its 9m budget and turned main red after #211 though no verifier in it had changed, and B4 stood
at 5m17s of 6m; each fix was another hand-made group (B5, E2), which only bought time. Now:

- **A ci-line names only its tier** (content, or `lock` for the answer-lock parts). `scripts/ci-groups.py` packs
  each tier's lines into as many groups as it takes, from each line's seconds on main's last full run
  (`scripts/ci-timings.json`) plus the job's setup, so that **every group is estimated at most 70% of its
  budget** (the budget is 75% of the timeout: where the workflow fails a group). Content groups have a 6-minute
  timeout: packed to 3m09s, failed past 3m36s, so every content job stays inside 4 minutes. Answer-lock parts
  are one `check-answer-lock.py --part i/n` line each, too long to share a job, on a 10-minute timeout; add a part
  when one passes 70%.
- **A line with no recorded time counts as its tier's default** (content 120 s, lock 300 s) and is flagged
  (`ci-groups.py --check` lists it) until a main run times it.
- **The pack is stable.** `scripts/ci-pack.json` holds each line's group; a line moves only when its group would
  pass 70% (the fewest, smallest moves) or it is new (it joins the group with the most room), so job names do
  not churn.
- **CI fails, on every PR, when any group is estimated past 80% of its budget** (`ci-groups.py --check` in the
  plan job), naming the group and its largest lines. Packing keeps every group under 70%, so only a single line
  too long for any group can fail it: split its script (`--part`, `--shard`).
- **After every full run on main the "CI timings and pack" job** records that run's times and repacks, and
  commits both files if they changed (`[skip ci]`, as the register job does).
- "70%" and "80%" are of the budget, not the timeout (Jon's own wording, 9 Oct: "kept to 70% of the budget,
  CI fails at 80%"). Of the timeout they would sit either side of the 75% at which the workflow already fails a
  job, and the 80% check could never fire before the job had failed.

**Rules that keep it fast.** Every job still fails at 75% of its timeout ("time budget: … split it"). **No
"Content verifiers" job may run past 4 minutes** (Jon, 7 Oct 2026): the packer keeps every content group under it (below; each job's summary lists every check's duration;
`check-verifier-coverage.py` reports any content group estimated past 4 minutes from the main run recorded in
`scripts/ci-timings.json`). Since CI-BALANCE the packer cuts the lists of lines; a single line too long for any
group is split by an option on its script (`--shard`, `--part`) with a self-test proving the parts are the
whole.

### 7.8.2 Two lanes: home and cloud (7 Oct 2026)

Two sessions may work at once, one per lane. Each lane keeps its own handover: `docs/handover/home.md` and
`docs/handover/cloud.md`; a session edits only its own. CLAUDE.md's opening block is a fixed pointer to both
and is not edited by fix PRs.

- **Home lane:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and
  every docs PR: `docs/todo.md`, relisting fixed games (batched), the roster's listed section.
- **Cloud lane:** per-game fixes in games that are currently unlisted (and listed games it has claimed: below), one game per PR, each with its
  verifier, closing its register entries in its own `docs/audits/findings/<slug>.yml`. It never edits
  `schools/assets/`, the shared modules in `scripts/`, the workflow, canon, the roster's listed section or
  `docs/todo.md`.
- **The cloud lane may fix listed games it has claimed on the `cloud-remaining:` line in
  `docs/handover/cloud.md`** (Jon, 8 Oct 2026, contract CLAIM). It claims one game at a time, before starting
  it, in a handover commit of its own, and removes the game in the PR that fixes it. The home lane never claims
  or edits a game on that line: before building each batch it reads the line on main and drops any claimed
  game. **For a listed game the claim is a process lock only** (Jon's ruling, 8 Oct): `check-answer-lock.py`
  judges it exactly as if unclaimed (a migrated game must pass; a NOT_YET game is reported). The
  reported-not-failed exemption holds only for games in the roster's Unlisted section, so no time bound is needed.
- **A new verifier never edits the workflow** (contract V, Jon, 7 Oct 2026). It declares its CI lines in its
  own file, `# ci-line: <label> | <args>` (one per line it contributes; `&&` in `<args>` runs the
  script again, as `--part-selftest && --part 1`; an answer-lock part is `# ci-line: lock | <label> | <args>`),
  plus `# ci-deps: <paths>` if it depends on something the derivation cannot see, or `# ci-held: <reason>` if it
  is deliberately not run. A line names no group: `scripts/ci-groups.py` packs the groups (§7.8.1). Either lane
  adds a verifier this way; neither edits `.github/workflows/check-site.yml` for it, nor `scripts/ci-pack.json`
  or `scripts/ci-timings.json` (main's "CI timings" job writes both). A tier, a tier's timeout or the packing
  rule, and every site-wide job, stay home-lane CI work. (A hand-made group id from before CI-BALANCE, such as
  `B4 |`, is still read as its tier, so an older branch passes.) (Until then canon reserved the workflow for the
  home lane while the cloud contract had the cloud lane add its verifier's line there: #96, #97 and #100-#102 did,
  and two conflicted with home-lane PRs. Both lanes now follow this rule.)
- **A per-game fix PR edits neither `docs/todo.md` nor `docs/audits/REGISTER.md`:** the register file records
  the fix, and the `register` job regenerates REGISTER.md on main.
- **Neither lane merges while main's last full run is red.**
- **A finished cloud session is closed, not left idle** (Jon, 9 Oct 2026). An idle session from 6 Oct woke on a
  GitHub event on 9 Oct and re-sent its old report as if new. When its last PR merges and its handover is written,
  the session ends; new work starts a new session from the handover.
- **One-off exception, 9 Oct 2026: the cloud lane edited `scripts/ci-groups.py`** to add group E2 (Jon's approval,
  after #211 turned main red with group E at 9m04s of 9m). It set no precedent: CI-BALANCE (#220) replaced hand-made
  groups with packing from measured times (§7.8.1), and `scripts/ci-groups.py` is home-lane CI work again.
- **Before the first push of every PR:** `python scripts/check-changed.py` (one PR on 7 Oct 2026 cost three
  runs without it).
- **Relisting a fixed game** is a home-lane docs PR, batched with others.
- **Contracts are kept verbatim, outside the start-up load** (Jon, 8 Oct 2026, contract CONTRACTS-FOLDER; after a
  `/clear` wiped the cloud lane's only copy of three contracts, and the repo held summaries only). On receipt, each
  contract is saved verbatim as `docs/handover/contracts/<yyyy-mm-dd>-<name>.md`, in its claim commit or its PR's
  first commit; the lane's handover queue holds a one-line pointer to it, never the text; when the work merges the
  file moves to `docs/history/contracts/`. The folder is read only when starting the item it names, never at
  session start: CLAUDE.md names the two handover files, and `scripts/check-context-size.py` measures only those
  and CLAUDE.md.

## 7.9 Verifier conventions (Jon, 8 Oct 2026)

- **Read a mark from what the page shows, never from a wrapped `mfg`.** analytics.js can replace `window.mfg` after a
  hook is installed, so a verifier that reads the analytics event can see no mark at all (#88's flake, fixed in #89,
  7 Oct 2026, by reading the feedback icon's class, which `showFeedback()` sets synchronously). First written in a
  CLAUDE.md handover; contract CTX.
- Verifiers recompute explanation and hint figures, not just keys (§0.3, "Also recorded with SR-16 to SR-20").

---

# 8. Outstanding Backlog

## 8.1 Games — Gaps

**None open.** All four items that sat here are built and live — found on 8 September 2026 while
reconciling this document against the repo, having been shipped without the backlog being cleared:

- [x] **Gradient Hunter** — rates of change, Core Maths §3.11. `games/gradient-hunter/`
- [x] **Expectation Station** — expectation, Core Maths §3.9. `games/expectation-station/`
- [x] **Better Value** — cost-benefit analysis, Core Maths §3.10. `games/better-value/`
- [x] **Factor Theorem** — factor theorem and algebraic division, A-Level B6. `games/factor-theorem/`,
  built from `docs/factor-theorem-learn-practice-spec.md` as the first Learn + Practice template

**The lesson, not the list.** Four games shipped and four backlog lines stayed open, in two documents,
for months. When a game closes a gap, clear it in `.claude/rules/game-roster.md` **and** §6.1 **and**
here in the same commit.

## 8.2 Games — Content

- [ ] Matrix Crunch question bank expansion (35+18 → 50+50 to meet platform minimum)

## 8.2b Leaderboard / Data Integrity — found 21 July 2026, not fixed

- [ ] **higher-power mixed-scoring-mode leaderboard key.** Its two modes
  (Higher/Lower streak, higher-is-better; Pairs, attempts,
  lower-is-better) both write to the same
  `leaderboards/higher-power_{level}` key with no field distinguishing
  them, so a ranked "top scores" list is meaningless as-is (a bad Pairs
  run can outrank a good one). Currently excluded from the leaderboard
  hub's ranking display rather than fixed. A real fix means a
  mode-qualified key or field, which touches `firebase-leaderboard.js`'s
  write path and possibly the RTDB schema — needs your call before
  anyone touches it.
- [ ] **game-roster.md level lists vs. code reality.** Several games the
  roster lists as multi-tier only ever submit under one hardcoded level
  in their actual `submitScore()` call, regardless of what tiers the UI
  offers: `log-laws`, `test-the-claim`, `characteristic-quest`,
  `eigenvalue-extractor`, `eigenvector-engine`, `dimension-checker`,
  `normal-navigator`, `partial-fractions-duel`, `index-laws`,
  `quadratic-factoriser`, `trig-wars`, `trig-worms`, `modular-battle`,
  `circle-theorem-spotter`, `probability-paradox`,
  `correlation-or-coincidence`, `bearing-blitz`, `truth-buster`,
  `estimation-engine`, `equatle`, `52dle`, `prime-or-composite`. Either
  the leaderboard call needs to pass the real per-tier level, or the
  roster's tier claim is aspirational and should be corrected —
  needs a decision, not just a doc fix.
- [x] ~~**truth-will-set-you-free has no site footer at all**~~ **Fixed 2 Oct
  2026 (to-do §1.28):** it carries the standard footer (§7.5.2).
- [ ] **estimation-golf can never appear on any leaderboard.** Its
  `submitScore()` call hardcodes `questionsAnswered = 9` (it's a 9-hole
  game — structurally always 9), but the shared
  `MIN_QUESTIONS_FOR_LEADERBOARD = 10` gate in
  `firebase-leaderboard.js` rejects it before the write ever fires.
  Confirmed via direct RTDB read: zero entries across all 6 of its
  levels. Not a hub bug, not a sort-direction bug — the data has never
  existed. Needs a decision: add a 10th question, add a per-game
  exception to the gate, or accept it stays off leaderboards. Deferred
  by Jon (21 July 2026) — not fixed.

## 8.2c Duplicate-option / distractor-collision defects — found 23 September 2026

**Two different defect shapes, found while scoping the leaderboard gate work above.**

**Shape 1 — no dedupe at all (option collision).** `matrix-crunch:171` and
`formula-unlocked:295` build their options array (`matrix-crunch:306`,
`formula-unlocked:447`) as `shuffle([correct, ...currentQ.d])` with no check that a
distractor doesn't equal the correct answer. This is a different root cause from the
Trig Worms fix (§12, "No rejection sampling") — Trig Worms had a dedupe step
that was too narrow (distractor↔distractor only); these two have no dedupe step of any
kind (correct↔distractor collision). The Trig Worms fix pattern would have caught both,
but there is nowhere to apply it: **no shared option-assembly helper exists on this
platform** — 32 games hand-roll `shuffle([correct, ...distractors])` independently.
- [x] **`proof-builder:232` — fixed 23 September 2026.** The self-correction text was
  inside the *correct* field itself, rendering as a selectable option reading
  `1 + 2 + 3 = 6... actually try 2+3+4=9` against distractors
  `['1+2+3=6','4+5+6=15','10+11+12=33']` — the only option containing prose, giving the
  question away, with the real intended answer (`2+3+4=9`) existing nowhere as a clean
  option. Corrected: `2+3+4=9` is now the clean correct option. A second, independent
  defect surfaced once the prose was removed — two of the three distractors
  (`4+5+6=15`, `10+11+12=33`) were themselves valid counterexamples to the claim, so a
  student reasoning correctly could be marked wrong. Fixed by swapping both for genuine
  non-counterexamples: `4+5+6=15 → 3+4+5=12`, `10+11+12=33 → 5+6+7=18`.
- [x] **The 4th "collision" reference resolved — it was never a 4th file.** `proof-builder`
  came from a separate prose grep, not the collision scan. The collision scan's actual
  four hits are `matrix-crunch:171`, `formula-unlocked:295`, `scale-factor-scaling:162`,
  `unit-converter:163` — the latter two are Shape 2 below, not option collisions; see
  that entry for why they were correctly excluded from the `MaffsOptions` wiring.
- [x] **`formula-unlocked`'s compounding bug — fixed 23 September 2026.**
  `correctVal = correct_override || correct` had silently duplicated `d[2]`. Wired to
  `MaffsOptions.build()`, confirmed correct answer present exactly once post-fix.
- [x] **Two more `correct_override` drift bugs found while checking the other 3 games
  using that mechanism — both were worse than `proof-builder` was. Both fixed
  24 September 2026.**
  - `normal-navigator:222` — the question's two given conditions (P(X<20)=0.1587,
    P(X>30)=0.0228) solved to μ≈23.33, σ≈3.33; no option was correct, and the accepted
    override answer (μ=25, σ=5) satisfied only the first condition. **Fixed
    24 September 2026:** the second threshold changed from 30 to 35, which makes
    μ=25, σ=5 exactly correct — no redesign needed. Graph draw values updated from
    `mu:22, sigma:4` to `mu:25, sigma:5`, and `shade:[20,30]` to `shade:[20,35]`, to
    match. Verified per option: only μ=25, σ=5 satisfies both conditions
    (P(X<20)=0.1587, P(X>35)=0.0228, both exact); μ=22,σ=2 and μ=24,σ=4 satisfy the
    first alone, which is what makes them good distractors. The 11-step `steps` array
    — which was the author's visible flailing and referenced the old threshold
    throughout — was replaced by the clean 4-step derivation the new numbers allow.
    **That fix was inert for a day, and finding out why turned up a third defect
    shape.** This question is `QUESTIONS[29]`, and `normal-navigator:254` reassigned
    `QUESTIONS[29] = {…}` after the array literal closed, so the question served at
    that index was a different one entirely and the repair reached no student.
    Resolved 25 September 2026 by deleting the three trailing reassignments — see the
    `QUESTIONS[n]` overwrite entry below. Confirmed on the running page that the
    repaired question is now the one actually served.
  - `normal-navigator:241` — correct value rounds to 17; it was not among the options
    (`14,15,12,16`); the accepted override answer (16) was the floor, not the nearest
    integer, and the graph drew a third, unrelated value (`mu:14`). **Fixed
    24 September 2026:** option `"12"` replaced with `"17"`, `17` made the accepted
    answer, graph draw set to `mu:17`. Drawing at 17 against a true μ of 16.55 is an
    offset of 0.09σ — not visibly wrong. The trailing step `"Rounding... closest is 16
    actually"` was corrected to `"To the nearest integer, μ = 17"`, since leaving it
    would have contradicted the accepted answer.
  - [x] **The dead `correct` fields on both questions — removed 25 September 2026.**
    They held `"μ = 22, σ = 4"` and `"14"`, disagreeing with the accepted
    `correct_override`. `handleAnswer` is the only consumer
    (`correctVal = q.correct_override || q.correct`, `normal-navigator:316`), so the
    override short-circuits and deleting them is safe; verified afterwards that the
    other 45 questions still carry `correct:` and none is left with no answer field.
  - `coordinate-geometry-dash:298` — checked, clean. The override correctly fixed a
    genuinely wrong original; only the cosmetic prose-in-steps issue remains (see
    Shape 2 below).
  - `probability-paradox` — checked, clean. No question sets `correct_override`, so
    there is nothing to drift.
- [x] **`MaffsOptions.build(correct, distractors)` built 23 September 2026** —
  `schools/assets/options.js`. Guarantees the correct answer appears exactly once, no
  two options share a key, bounded Fisher-Yates, no rejection sampling (per
  §12, "No rejection sampling"). Wired into `matrix-crunch:306`, `formula-unlocked:447` and
  `proof-builder` (3 call sites: the two identical branches at :396/:398 and the
  induction stage at :563) — **scope deliberately held to the confirmed-broken sites
  plus the one repaired alongside them, not a platform sweep.** Emits `console.warn`
  when it drops a duplicate distractor; left on deliberately as a visible canary until
  the affected banks' missing 4th distractor is filled in (see next item), to be
  silenced once that's done.
- [ ] **`matrix-crunch:171` and `formula-unlocked:295` now render 3 options, not 4.**
  `MaffsOptions.build()` correctly drops the duplicate but can't invent a replacement
  distractor. Both are one option short of a clean 4-choice question until a genuine 4th
  distractor is authored for each — a content task, not a code task.
- [x] **`normal-navigator` overwrote three of its own questions after the array
  literal closes — found and fixed 25 September 2026.** `const QUESTIONS=[…]` runs
  179–251, and then lines **254, 257 and 260** reassign `QUESTIONS[29]`, `[28]` and
  `[27]` to different question objects. The three literal questions at those indices
  are dead code that no student ever sees — including the one repaired in this entry.
  Worse, the three replacements duplicate questions that already exist further down the
  literal, so the live 47-question bank contains **two exact duplicate pairs**:
  indices 28 & 31 (`X ~ N(μ, 6²). P(X > 70) = 0.0228.`) and indices 29 & 30
  (`X ~ N(50, σ²). P(X < 44) = 0.0668.`). Since `normal-navigator:274` draws with
  `pool=shuffle([...QUESTIONS]).slice(0,MAX_Q)` (MAX_Q = 20), **a student could be asked
  the same question twice in one run.**

  **Fixed 25 September 2026 by deleting all three reassignments**, which restores the
  literal entries at 27–29 and removes both duplicate pairs as a consequence — the
  reassignments were what created them, so nothing separate had to be done about them.
  Verified on the running page: bank length still 47, no empty slots, **no duplicate
  ctx anywhere**, no question matching the old `0.1587` / `P(X > 30)` pair, and the
  repaired question is now the one actually served.

  **The comments on those three lines are why this happened, and they are worth
  reading before writing another patch like it.** They said *"Fix questions with bad
  steps"*, *"Fix combined question"* and *"Remove the messy simultaneous equations
  question and replace"*. The intent was sound — the messy simultaneous-equations
  question is exactly the one repaired above — but **it is index 29 and the patch was
  written to `QUESTIONS[27]`.** So the patch missed its target, destroyed two perfectly
  good questions instead (`Exam marks: X ~ N(65, 12²)…` at 27 and `Battery life:
  X ~ N(48, 4²)…` at 28), left the messy one untouched, and duplicated two others.
  **Patch the entry, not an index** — an index written by hand is a guess that no
  checker was watching.

**Shape 2 — duplicate object keys (not an option collision).** `scale-factor-scaling:162`
and `unit-converter:163` each had `c:`/`d:` keys written twice in the same question
object; JavaScript kept the last, so the rendered options and the correct answer were
both fine. **The original diagnosis of where the leak lived was wrong and is corrected
here.** The self-correction prose (e.g. `'V = 1.5 × 0.6 × 0.4 = 0.36 m³... wait,
1.5 × 0.6 = 0.9, × 0.4 = 0.36'`) is not carried by the duplicate `c:`/`d:` pair at all —
`showExplain` renders only `q.s`, and the prose lives in the `s:` (worked-steps) array,
which was never duplicated. Deleting the dead `c:`/`d:` pair (done, 26 Sep 2026) removed
genuinely dead code but left the leaking text rendering exactly as before. **Fixed
26 September 2026** by rewriting both `s:` arrays: `scale-factor-scaling:162` also had a
mathematically wrong intermediate step (`4 cm² × 50000² = 4 × 2.5×10⁹ cm² = 10⁹ cm²` —
the correct product is `1×10¹⁰`, not `10⁹`), corrected as part of the same edit, and now
shows the cm²→m² conversion as an explicit step rather than folding it into the final
line. Independently confirmed by a brace-aware duplicate-key scan (2 files, matching
manual triage exactly, no false positives or negatives against 32 manually-discarded
nested-object lines) — that scan is still correct about the duplicate keys, only its
conclusion about where the prose rendered from was not. **Not wired to
`MaffsOptions.build()`** — correctly excluded, since these have no runtime option
collision to dedupe.
- [x] Both instances, and the original `proof-builder` case above, read as the same
  underlying process gap: **unreviewed LLM-generated bank content shipped without a
  read-through** — the same complaint a teacher made about the escape-room prose (see
  §11.5). Worth a deliberate decision on whether bank generation needs a read-through
  pass or an automated self-correction-language lint, separately from the code fixes
  above.

**Decided 23 September 2026 (Option B): build a shared `MaffsOptions.build(correct,
distractors)` helper that dedupes on the same representation `dataset.val` comparison
already uses (§7.1), wire it into new games and the confirmed-broken sites above now,
and retrofit the other ~30 games hand-rolling this logic gradually, during down-time —
not as a platform-wide sweep.** Explicitly rejected: fixing all of them in one pass. Per
§7.1.1 and the sweep history (`96381d74`, `76514c70`, `4b3d7d3`), a shared-code change
touching many live games at once is exactly the pattern that has broken games silently
before. **Too many tasks in flight to schedule the full retrofit now — parked here as
the thing to return to in the next down-time window, not forgotten.**

**Coverage caveat, stated by Code Claude and worth keeping in view:** the collision scan
only reaches banks whose distractors live under known key names. A game storing
distractors under some other name would be invisible to it, and a game with a combined
correct+distractor options array (`probability-paradox`-style) is structurally immune to
this specific defect. The "4 collisions" count is a floor, not a guaranteed total.

## 8.3 Analytics — Final Spec Pass

- [ ] Migrate abandon tracking from `beforeunload` to `visibilitychange` (already done in analytics.js, remove legacy listeners from game files)
- [ ] Add `attempts` parameter to `question_answered` across all games
- [ ] Add `game_replayed` event (fires when PB exists on game_started)
- [ ] Add `level_selected` event to all games with level pickers
- [ ] Add `difficulty_selected` event (Tax Theft, SUVAT, Matrix Crunch)
- [x] ~~Add `filter_applied` event to portal (level pills, topic pills, search with debounce)~~ **Done 2026-09-21**, with `game_card_clicked` alongside it — see §1.3 *Portal events*. The two are useless apart: GA4 is cookieless, so a filter click and a later `game_started` cannot be joined after the fact.
- [ ] Register all 13 custom dimensions in GA4 admin

## 8.4 Completed 20 March 2026 — historical

*Kept as a record of that session. Not a current to-do list.*

- [x] Test the Claim — built and deployed (48 questions, 4 modes)
- [x] Stat Attack — built and deployed (36 scenarios, 3 levels)
- [x] Growth and Decay — built and deployed (45 scenarios, 3 levels)
- [x] Graph Sketcher — built and deployed (45 scenarios, curve drawing)
- [x] Glorious Gantt Game — built and deployed (15 scenarios, CPA + Gantt)
- [x] Split It — built and deployed (600 procedural questions, 6 modes)
- [x] Component Crusher — built and deployed (45 scenarios, vectors, closes gap)
- [x] GA4 custom events on all 60 games via mfg() dual logger
- [x] Google Sheets analytics backend deployed
- [x] Daily email report + Dashboard charts
- [x] Privacy page fully rewritten
- [x] Spec-map comprehensive overhaul — all 60 games mapped, 4 gaps identified
- [x] CLAUDE.md updated to current state
- [x] question_index added to all question_answered events

---

# 9. Leaderboard & Score Ticker

**Status: live.** Anonymous, no accounts, no PII. Disclosed in full at
/privacy/index.html (lines 177–179).

## Architecture
- Firebase Realtime Database, project `maffsgames`, europe-west1
- Shared module: `schools/assets/firebase-leaderboard.js`
  → `MaffsLeaderboard.submitScore()`, `MaffsLeaderboard.standing()`
- Writes to:
  - `leaderboards/{slug}_{level}` — score, timestamp, optional 3-letter
    initials (voluntary, non-unique, no identity guarantee)
  - `recent_scores` — feeds the ticker (which reads the latest 20); no longer
    auto-pruned by the client (30 Sep 2026: the database rules in
    `firebase/database.rules.json` refuse deletes; prune by hand, see
    `docs/firebase-rules-deploy.md`); each new
    entry also carries `levelKey` (the raw level, since 28 Sep 2026)
    alongside the human-readable `level` label
- **A status that depends on other records is computed at display time,
  never stored** (28 Sep 2026). `recent_scores` entries used to carry
  `highScore`/`weeklyBest`/`best`, computed once by `submitScore()` and
  frozen at that moment — a later higher score, or the 7-day window
  simply moving on, made an old entry's badge and "best" wrong
  indefinitely (seen live: a 7-day-old "WEEKLY BEST 10" still showing
  beside a newer, higher "HIGH SCORE 30"). `submitScore()` no longer
  writes those three fields. `MaffsLeaderboard.standing(slug, levelKey)`
  reads `leaderboards/{slug}_{level}` live and returns `{allTimeBest,
  weekBest, direction, rankable}`, cached per game+level for the page's
  lifetime; the ticker and the hub both derive their badges from it, and
  `LOWER_IS_BETTER`/`MIXED_UNRELIABLE` now live only in this module too
  (previously duplicated in `leaderboards/index.html`). Existing
  `recent_scores` entries still carry the stale fields — no migration —
  and both readers ignore them. Contract:
  `docs/next-contract-ticker-live-standing.md`.
- Gating: **completion, not a count** (since 23 Sep 2026). Every game
  calls `submitScore()` at its own natural end (pool exhausted, out of
  lives, timer up, puzzle won or lost), so reaching the call is the
  qualification. The old `MIN_QUESTIONS_FOR_LEADERBOARD = 10` gate
  rejected silently and kept thirteen games off every board — any whose
  unit is not ten-plus questions: ten never ranked at any setting, three
  not at their default or shortest one. **`submitScore()` must only be
  called at a real end**; a call mid-run would now rank a partial run.
  The one designed early end is `like-terms-collector`'s Stage 3
  "Finish here" checkpoint, which the game tells the player still counts.
- Every score not written is logged: `console.warn('MaffsLeaderboard:
  score not submitted — <reason> [game, slug, level]')`. Reasons: SDK not
  loaded, not the production host, write failed.
- Certificate thresholds: `GOLD_THRESHOLD` / `SILVER_THRESHOLD`
  (top 5% / top 10% percentile cutoffs) — unrelated to submission volume,
  no submission-count gate exists anywhere in this feature

## The ticker
- Location: portal homepage, `index.html:664`
  (`<div class="score-ticker" id="scoreTicker">`)
- Logic: inline `<script>`, `index.html:3557–3684`, after loading
  `firebase-leaderboard.js` for `standing()`
- Live subscription via `db.ref('recent_scores').on('value')` — not a
  one-off fetch — renders last 20 entries: initials (if given), game,
  level, score, previous best, high-score/weekly-best badges, relative
  time ("3m ago"). Auto-scrolling. Badges and "best" are recomputed live
  via `standing()` on every snapshot, never read off the stored entry
  (28 Sep 2026 — see Architecture above).
- This is one of two player-facing surfaces for score data — see
  "Leaderboard Hub Page" below for the other. See §8 backlog for
  outstanding gaps.

## Coverage (96 live games)
- **The hub registry is checked too (30 Sep 2026).** `scripts/check-leaderboard-coverage.js` reads
  the `GAMES` array in `leaderboards/index.html` and fails if a game that calls `submitScore()` is
  missing from it, or if a row's levels differ from the keys the game really submits under (call-site
  literals, else the roster; games whose level variable takes other keys are declared in its
  `LEVEL_OVERRIDES` with where each key comes from). Its first run found six problems: two games absent (`linear-equation-solver`, `distinctly-average`),
  `six-sevens-bruv`, and three games submitting under keys the hub never showed — `quadratic-factoriser`
  (`higher`, `formula`), `chart-interrogator` (`l4`) and `binomial-blaster` (`alevel2`; it never submits
  `level4`). All six rows corrected the same day. (`regression-rumble` was first listed as splitting
  Level 4 across `l4` and `level4`; checked in a browser, its Level 4 *button* crashes on Start, so it
  never submits `l4` at all — todo, leaderboard tidy.) **Fixed 30 Sep 2026**: both Level 4 routes
  now play and submit `level4`.
- **A level is named in one place (30 Sep 2026): `MaffsLeaderboard.levelLabel(key)`** in
  `firebase-leaderboard.js`. It names every level key any game submits, old and new, from
  `LEVEL_NAMES`, plus `LEVEL_NAME_PATTERNS` for keys that are not a fixed list (`daily-YYYY-MM-DD` →
  "Daily pizza 1 Oct", no leading zero). It returns `null` for a key nothing names. `submitScore()` stores its label
  in the ticker entry. The coverage check loads the file in a bare `vm` and **fails on any submitted
  level `levelLabel()` cannot name**, and on any submitting game whose levels it cannot read. The old
  label → key lookup (`LEVEL_LABELS` / `LABEL_TO_LEVEL` / `levelKeyFromLabel()`) is **frozen
  legacy**. It is used only for ticker entries written before `levelKey` existed (28 Sep), and is
  never extended. Adding `l4:'Level 4'` to it would re-key every old "Level 4" entry to `l4`, and a
  pattern cannot be inverted. **The hub page uses `levelLabel()` too** (`levelName()` in
  `leaderboards/index.html`, falling back to the raw key for an unnamed one); its own copy is gone,
  and `levelLabel('all')` is `''` there as on the ticker. Individual games still keep their own
  in-game level-name maps (14 of them at 30 Sep 2026; todo).
- **A roster label becomes a level key in one place (30 Sep 2026): `scripts/roster-levels.json`.**
  `.claude/rules/game-roster.md` names levels with display labels ("L4", "A-Level Year 2") and the
  keys cannot be derived from them. `bank_common.roster_levels()` reads the table for `check-site.py`
  and `extract-banks.py`; `check-leaderboard-coverage.js` reads the same file, which is JSON because
  it cannot import Python. **A roster label the table does not list is an error in both readers**,
  never silently dropped: that is how `A-Level Year 2` went unchecked, and how `extract-banks.py`
  never extracted log-laws' Level 3 bank. Add a new label there, and nowhere else.
- **94 of the 96 live games call `submitScore()`** (recounted 3 Oct 2026; the two that do not are
  `constructions-lab` and `given-that`, above). The 29 Sep count of 95 included `regression-rumble`,
  withdrawn on 30 Sep (its `_withdrawn.html` still calls it). On 29 Sep, 91 of the 95 submitted
  unconditionally; that split has not been recounted.
- **Pattern keys off the hub (30 Sep 2026).** `free-daily-pizza` submits **mixed-stage** practice to
  `practice-q20` / `practice-q40` (on the hub, "Practice · 20" / "Practice · 40"). Single-stage practice
  submits to no board; it goes to score history only, under `stage-s1-q20` etc., and says so on its end
  screen, because a one-stage round and a mixed round are not the same test (Jon) and each day's pizza to
  `daily-YYYY-MM-DD` ("Daily pizza 1 Oct"), one board per UK day, deliberately not on the hub. The
  coverage check declares that pattern in `OFF_HUB_LEVEL_PATTERNS`, with a sample key it still asks
  `levelLabel()` to name, so a daily key can never reach the ticker unnamed. The game shows today's
  best as a target through `standing()`, unmodified: with Firebase blocked there is simply no target.
- 2 intentionally excluded (non-scored, exploratory format):
  `constructions-lab`, `given-that`.
- 2 **held** (24 Sep 2026) for scoring direction, which is not the same as excluded: they have a
  score and they call `submitScore()`, but the call is gated off at the call
  site behind `LEADERBOARD_MODE_READY`. `estimation-golf` (stroke total) and
  `equatle` (guesses used) are **lower-is-better**, and the boards rank high
  score first — publishing would put the worst round on top and rank a
  6-guess scrape above a 2-guess win. Both reached the boards for the first
  time when the ten-question gate was removed. The gate lifts when scoring
  modes land: `docs/next-contract-leaderboard-modes.md`. Device-local score
  history is unaffected and still records.
- 1 more **held in part** (28 Sep 2026): `log-laws`. Its Laws drill submits
  as before, under the real `?level=`; its **Solve** mode is gated behind
  `LEADERBOARD_MODE_READY`, and also kept out of device-local score history,
  because today there is one board per level and Solve's scores would mix
  into the Laws drill's. Its gated call already passes mode `'solve'`, ready
  for the modes contract.
- 1 more **held** (29 Sep 2026): `distinctly-average`. It is wired exactly like
  the other session-based games (`quadratic-factoriser`, `better-value`: one board
  per level, 10 points per correct answer, `submitScore()` at the end of a run) but
  the call is gated off behind `LEADERBOARD_MODE_READY` and declared in `HELD`.
  Reason: the student picks 10, 20 or 30 questions and the board key is
  `slug_level` only, so a 30-question run (up to 300) would outrank every
  10-question run (up to 100) on one board. This is a class, not a one-game bug:
  `quadratic-factoriser`, `better-value`, `spot-the-muppet`, `expected-damage`
  and `expectation-station` all rank different session lengths together today.
  The gated call already passes the session length as a mode (`'q10'` …), ready
  for `docs/next-contract-leaderboard-modes.md`, which is the architectural fix.
  It also needs an entry in `GAME_NAMES` (`schools/assets/firebase-leaderboard.js`)
  and in the hub's `GAMES` list (`leaderboards/index.html`) when the gate lifts.
  Device-local score history is unaffected and still records.
- Coverage is enforced going forward by
  `scripts/check-leaderboard-coverage.js` — run it before shipping a
  new game; it fails if any non-excluded game lacks a `submitScore()`
  call, if a held game has lost its gate, or if a gate exists that `HELD`
  does not declare. A game that silently submits nothing is the failure
  mode it exists to prevent.

## Device-Local Score History
- Shared module: `schools/assets/score-history.js` →
  `MaffsScoreHistory.record()` / `.get()`
- Purely local — no server call, no accounts. Stores the last 10 runs
  per game+level under `localStorage` key
  `mfg_hist_v1::{slug}::{level}`, additive alongside each game's
  existing single-value "personal best" key (untouched, different
  naming per game — see §8 backlog).
- Wired into every game that calls `submitScore()` (all 94 live ones, recounted 3 Oct 2026), called
  immediately after the `submitScore()` call.

## Leaderboard Hub Page
- Live at `/leaderboards/index.html` (added 21 July 2026)
- Public side: one card per game (91), each with a level switcher.
  Per level: top 5 scores from a trailing 7-day rolling window
  (filtered by timestamp client-side, not a calendar reset) plus a
  one-line all-time-high with the date it was set. Both computed
  client-side from a single `leaderboards/{slug}_{level}` read —
  no RTDB index or rules change needed (confirmed via REST that the
  `leaderboards` root itself denies listing, so per-key reads via a
  hardcoded game→levels registry in the page are the only viable
  approach regardless). Its `LOWER_IS_BETTER`/`MIXED_UNRELIABLE` are the
  shared copy from `firebase-leaderboard.js` (28 Sep 2026); the entries
  list and all-time-high date are still computed here directly from that
  same read, deliberately not routed through `standing()` — `standing()`
  returns bare numbers only, this page also needs each entry's date and
  initials, and output here was already live, never the frozen half of
  the bug the ticker had.
- Cards lazy-load via `IntersectionObserver` so opening the page
  doesn't fire 90+ simultaneous Firebase reads at once.
- On load, a card probes all of its own levels in parallel and defaults
  to whichever one actually has data, rather than trusting the
  registry's declared level order — several games' first-listed tier
  turned out to have zero traffic while a later tier had plenty (e.g.
  `factor-race`: `year6` empty, `ks3` populated). Falls back to the
  first level if none have data yet (genuinely new game).
- "Your Scores" section: device-local only, reads
  `MaffsScoreHistory`/`localStorage` directly (no server call), only
  lists games actually played on that device.
- `higher-power` is excluded from ranking (shows a note instead) — see
  §8 backlog, "higher-power mixed-scoring-mode leaderboard key".
- Linked from a portal header badge and the site footer, which every
  page carries (§7.5.2; fixed-position, so present on the results
  screen too).
- Certificates (gold/silver percentile tiers) are explicitly out of
  scope for this page — parked, not built.

---

# 10. Contact & Links

| **Item** | **Detail** |
| --- | --- |
| Email | contact@maffsgames.co.uk |
| Feedback form | maffsgames.co.uk/feedback/ (`/schools/feedback/` redirects to it) |
| Buy Me a Coffee | buymeacoffee.com/maffsgames |
| Repository | github.com/OrthogonalMaffs/maffsgames |
| Live site | maffsgames.co.uk |

---

# 11. Escape Rooms

Narrative maths escape rooms at `/escape-rooms/`. Started 2026-08-26; reference point
**Unlock!**. **Under 15 minutes each** — built to end a lesson, not fill one, and to be played by three or
four students round one screen. Not counted in the 96 live games.

## 11.1 Current state — 17 September 2026

**Eight rooms live, two withdrawn.** The site ships a room as its voice rewrite finishes (§11.5).

| Room | Slug | Level | Antagonist | State |
| --- | --- | --- | --- | --- |
| The Great Hamster Heist | `hamster-heist` | KS3 / GCSE | Mr Beaker (asleep) | **Live** |
| The P.E. Store Rebellion | `pe-shed-rebellion` | KS3 / GCSE | Mr Barry Lunge, "Lungey" | **Live** |
| The Prom Budget Embezzlement | `prom-budget` | GCSE / Core | Mr D Tension | **Live** |
| The Canteen Menu Hack | `canteen-hack` | KS3 / GCSE | Ms Cinnamon | **Live** (12/09) |
| The Heatwave Mutiny | `heatwave-mutiny` | KS3 / GCSE | Mr Robin Banks, the trust's energy contractor | **Live** (13/09) |
| The Rugby Mud Bath | `rugby-mud` | GCSE | Mr Mower | **Live** (15/09) |
| The Comic Caper | `comic-caper` | GCSE | Ms Fromage | **Live** (17/09) |
| The Kiln Disaster | `kiln-disaster` | GCSE | — (Mr Stephen Mudge, "Smudgey", Art, is an ally; the kiln is the clock) | **Live** (17/09) |
| The Headteacher's Car Trap | `car-trap` | GCSE / Core | — | Withdrawn |
| The IT Teacher's Vengeance | `it-vengeance` | GCSE Higher | — | Withdrawn |

Two further rooms, **A (Coach Trip Hijack) and B (Tuck Shop Heist)**, are narratives only. Their locks were
rejected in the batch-one audit and have never been repaired; they need a maths pass before any art.

**The school is St Martha's Secondary throughout, and no room carries a year or a brand mark** — the
material is meant to be reused next September.

## 11.2 Structure

| Path | What it is |
| --- | --- |
| `escape-rooms/index.html` | The hub. One card per **live** room |
| `escape-rooms/<slug>/index.html` | The room page — scaffold only; all content is in `room.js` |
| `escape-rooms/<slug>/room.js` | **The room.** Narrative slots, objects, locks, variant libraries, alt text |
| `escape-rooms/<slug>/teacher.html` | Answers, hint ladder, misconceptions, timings. **Stays `noindex`** |
| `escape-rooms/assets/engine.js` | The shared game engine. Read this before changing any room |
| `escape-rooms/assets/teacher.js` | The shared teacher-page renderer |
| `escape-rooms/assets/engine.css` | Shared styling for both |
| `docs/art/<slug>-{scene,fail,win}.webp` | Three pictures a room, 1600x873 WebP q80 |

Each room: **15 minutes, three locks, 45-second penalty** per wrong setting. Eight searchable objects —
usually six clues and two blanks (`comic-caper` has four and four); at least two blanks is enforced.

## 11.3 Rules that are load-bearing

- **`name` and `where` are escaped; everything else is not.** Object and lock `name`/`where` go through `esc()` in `engine.js`, so an HTML entity there renders literally on screen. Clues, flavour text and the narrative slots go through `fill()` and do render entities. Use real characters in `name` and `where`, entities everywhere else.
- **Object `id`s must never change.** `teacher.html` maps clues to locks by the `id` field in `room.js`.
  Rename one and the teacher page silently stops mapping that clue. Change `name`, `where` and `clue` freely.
- **No figure is written into the prose.** Every number is a `{{key.token}}` filled at run time from the
  variant drawn for that play, so clue, hints, misconception response and worked solution all move together.
  **Never hand-edit a `variants:` block** — edit `scripts/gen-escape-variants.py` and re-run it.
- **A hardcoded number in prose contradicts a drawn variant** and reads fine until it doesn't. Grep a room's
  prose for bare amounts before rewriting it.
- **Replay is a designed property.** Across the eight live rooms: **199 verified number sets, of which
  2,384 combinations are VALID and can actually be served** (per room: hamster 314, P.E. 248, heatwave 220,
  prom 342, canteen 600, rugby 156, comic 184, kiln 320). A lock never draws the set it gave last time.
  `check-escape-rooms.py` prints the VALID counts. **The hub quotes no totals or per-room ranges** (Jon,
  17/09): the sentence went stale twice, and 3,600 overstated what is served by 75%. Do not put a figure
  back. Nor may it claim no two groups get the same room — devices draw independently, and at rugby's 156
  VALID draws ten groups have about a 1 in 4 chance that two match.
- **Rooms are drawn jointly; no two locks may collide.** A draw is VALID when no clue figure appears in two
  locks' clues, no answer appears in another lock's clues, no answer equals another lock's misconception,
  and no two locks share an answer. Clue figures include numerals typed into clue text. The first two rules
  ignore figures of 2 or less. `engine.js` serves only VALID draws and `check-escape-rooms.py` fails a room
  with fewer than 20; the two implement the same rules and change together.
- **Keypads: fixed length, or up to N digits (KEYPAD-VARIABLE, 10 Oct 2026).** `digits: N` takes exactly N
  digits, empty slots shown (60 is entered as 060), and Set with too few says "Not enough digits." at no
  cost. `maxDigits: N` instead is **"up to N digits, Set to submit"**: the display shows only what has
  been typed (no empty slots), Set submits 1 to N digits and does nothing with none, and a leading zero is
  never kept. The typed fallback follows the same rule (`upTo()` in `engine.js`). Use it where a lock's
  answers vary in length: N fixed slots steer students to N digits, and too few slots cut a wrong answer
  down to a right one (5400 on two digits reads as 54). The misconception must fit too, so a four-digit
  misconception needs `maxDigits: 4`; `check-escape-rooms.py` fails a maxDigits lock whose answer or
  misconception cannot be set. The live rooms all use `digits`. Waiting on it: the cloud lane's drafts of
  **The Rightful King** (passcode, answers 24 to 504) and **The Library Jam** (fines lock, answer up to
  £99, misconception up to 9900). Tested by `scripts/test-escape-keypad.py`.
- **`wrongLines`** — a room's escalating wrong-entry lines, `{head, body}` objects, indexed by
  `st.wrongs - 1` and clamped so the last repeats. A room without the array gets the original fixed string.
  A misconception hit consumes an index without printing a line, which is intended.
- **Instrument art is dropped set-wide.** Three pictures a room, not six; the engine draws the live control
  and emits no `<img>` at all where a lock has no `art`.
- **The failure picture is not optional** — it is the timeout screen, and on any lock with `missArt: true`
  it also fires on that lock's named misconception. A room has exactly one failure picture; per-lock
  misconception pictures were considered for `heatwave-mutiny` and **cancelled**, not deferred.
- **The teacher page only mentions the mid-game failure picture when a lock sets `missArt`** — `teacher.js`
  derives it from room data.
- **The teacher page follows the live game.** The room mirrors its draw into `localStorage` under
  `mfg_escape_vars_<slug>`; the teacher page reads it and re-renders on the `storage` event.
- **Premise copy lives in three places**: the room's own `index.html` (meta, og:, Twitter), its card on
  `escape-rooms/index.html`, and its card in the front-page band in `index.html`. All three go stale silently.

## 11.4 Scripts

| Script | What it does |
| --- | --- |
| `scripts/check-escape-rooms.py` | The gate. Every room against the audited bank (every `lock-bank-batch*.txt`) and `variants.json`, all tokens resolve, VALID draw count per room (fails under 20; an invalid variant 0 only warns), art present. Run before shipping |
| `scripts/gen-escape-variants.py` | Generates and verifies the variant libraries |
| `scripts/test-escape-keypad.py` | The keypad's maxDigits mode on a fixture lock (5,4,Set opens; 5,4,0,0,Set is the misconception; no empty slots), a fixed keypad unchanged, the old rule planted |
| `scripts/check-lock-bank.py` | Rejects a lock with more than one settable answer |
| `scripts/strip-gen-watermark.py` | Removes the generator's sparkle and reframes to 1600x873. **Run on every image** — it is a no-op on a clean one |
| `scripts/serve-stubbed.py` | Serve the site locally with analytics stubbed. **Escape rooms load analytics too** — never render-test against the live endpoint |

## 11.5 The voice rewrite — the live work

A teacher found `/escape-rooms/` through the feedback form on 2026-09-08 and said the prose is visibly
AI-written and the rooms are unusable in class. **They were right, and the diagnosis is precise: the maths
and the puzzles are sound, the prose had no author behind it.** All eight rooms are being rewritten one at a
time, each around a named antagonist **drawn out of Jon in an interview rather than invented for him**.

- **Binding contract:** `docs/escape-room-voice-contract.md`
- **Running state, per-room status and the gotchas:** `docs/escape-room-voice-rewrite.md` — **read this
  first**
- **Reference implementation:** `escape-rooms/hamster-heist/room.js`
- **Art prompts and what went wrong:** `docs/escape-room-image-prompts.md`

**One room per session. Jon reviews every draft before a file is touched.** Expect the premise to move, not
just the wording — it has in every rewritten room so far. Two rules came out of that: **one enforceable failure
per room, able to reach the students during play**, and **a character who is not present can be the
standard, never the threat**. Characters may recur offstage but each speaks only in their own room.

**Releasing a room is part of finishing it**: write its real `index.html` and `teacher.html`, add its card
to the hub and the front-page band, add its `<url>` to `sitemap.xml`, and bump the room counts. The hub has no
sets/combinations figure to recompute. §5c of the working doc lists the files.

**The two withdrawn rooms were not deleted.** They have been indexed since 2026-09-01, and an indexed path
is not traded for tidiness while the domain is still earning trust, so each keeps its URL and serves a
`noindex` holding page. `room.js`, the teacher data and all art are untouched.

## 11.6 Art

Hand-drawn cartoon, visible ink linework of uneven weight, flat colour with limited cel shading, muted
desaturated palette, one dominant light source. **Empty rooms, no people, no lettering** — figures are
where generation fails and an empty room carries no text to garble. House frame **1600x873 WebP q80**.

**Every PNG downloaded from the generator since September 2026 carries a four-pointed sparkle in the
bottom-right, and the detector has a false-negative mode** — a soft, low-contrast stamp loses its points
under thresholding and is rejected for not being star-shaped. **Look at the corner yourself.** Do not loosen
the thresholds; an earlier version flagged 30 of 53 clean images. Marks on plain ground take `--at X,Y`;
marks on an edge or a line must be cropped out, because the fill smears. **JPG downloads carry no mark at
all — ask for JPGs.**

---

# 12. Engineering reference (moved from CLAUDE.md, 8 Oct 2026, contract CTX)

These sections were in `CLAUDE.md`, which loads into every session, and existed nowhere else. They moved here
verbatim (contract CTX: a rule that exists nowhere else moves into canon, listed in its PR). Their own words
still say "this file", "above" or "below" where they meant CLAUDE.md.

## Does it actually run? — `scripts/check-site.py`

```
python scripts/check-site.py            # tiers 1 + 2, local stub server
python scripts/check-site.py --tier 2   # static scan only, no browser
python scripts/check-site.py --tier 3   # PLAY every game (opt-in, ~16 min)
python scripts/check-site.py --live     # tier 1 against maffsgames.co.uk
python scripts/check-site.py --only modular-battle
```
One-time setup: `pip install playwright && python -m playwright install chromium`.
**In a Claude Code cloud sandbox** the CDNs are unreachable and the installed Chromium is not the one pip's
Playwright expects, so tiers 1 and 3 fail there identically on `main`: follow `docs/sandbox-checks.md`.

`check-leaderboard-coverage.js` verifies that code **exists**. It cannot tell you whether that
code **runs** — `chart-interrogator` and `modular-battle` were dead for six months after the
2026-03-22 sweeps (`96381d74`, `76514c70`) and passed the coverage check every time. `check-site.py`
is the missing layer:

- **Tier 1** loads every game, room, teacher page and portal page in headless Chromium — bare and
  once per `?level=` the game declares in `.claude/rules/game-roster.md` (a roster label becomes a
  level key in `scripts/roster-levels.json`, the one table; an unlisted label is an error). FAIL on an uncaught
  exception, a `console.error`, a 404 on a local asset, or a main thread that stops answering
  (an infinite loop). External-CDN trouble is WARN, not FAIL. **Tier 1 also presses every level
  button** (30 Sep 2026): each game's every level control, in a fresh page, must reach
  `game_started` with no uncaught exception. Loading `?level=` URLs never presses a button, which is
  how `regression-rumble`'s Level 4 button sat dead: it set `l4`, a key its bank did not have.
  125 controls across 47 games; the method is commented in `check-site.py` at "Tier 1, level controls"
  (122 across 46 since `regression-rumble` was withdrawn).
- **Tier 1 loads every page the site serves** (2 Oct 2026, to-do §4 item 12), not only files named
  `index.html`. "Served" is GitHub Pages' Jekyll rule, encoded once in `jekyll_serves()`: there is no
  `.nojekyll`, so a file or folder whose name starts with `_`, `.`, `#` or `~` is not published, nor is
  anything in Jekyll's default exclude list; everything else is, `docs/` and `scripts/` included. So
  `games/sequence-solver/index-original.html` (a redirect stub) is loaded and
  `games/regression-rumble/_withdrawn.html` is not.
- **Tier 1 fails any page that scrolls sideways on a 320px phone** (2 Oct 2026, to-do §1.34). Every
  page is loaded again at 320×568, and every game is started through its first level control or Start
  button and measured again; `scrollWidth` 1px past the viewport is a FAIL naming the outermost
  elements past the edge. Measured with **Google's web fonts blocked**, so in the fallback font CI pins
  to DejaVu, the same every run (Jon's ruling: in Outfit 12 of the 44 overflows fit, and a gate must
  not depend on a third-party fetch; to-do §4 item 14 is self-hosting Outfit). No fixed pause: load
  event, KaTeX, `document.fonts.ready`, two animation frames. **Known overflows live in
  `scripts/checker-allowlist.json` under `tier1_phone_overflow`**, one entry per path and `at`
  (`load` or `start`) with its width and owning to-do item; CI fails on a new overflow and on a stale
  entry (one that now fits), so **the PR that fixes an overflow removes its entry**. Redirect stubs
  are not measured themselves; the check asserts each stub's target is. A game that starts at desktop
  size but not at 320×568 FAILs as "phone start unreachable". Four games start at neither by this
  method and are noted, not measured (`factor-theorem`, `six-sevens-bruv`, `trig-worms`,
  `test-the-claim`; reasons in the to-do's §1.34). Commented in `check-site.py` at "Tier 1, phone
  width". **The phone pass is seeded** (3 Oct 2026, to-do §4 item 16): `PHONE_SEED` replaces
  `Math.random` before any page script runs with mulberry32 seeded by the FNV-1a hash of the page's own
  `location.pathname` (e.g. `/games/moments-master/`), so every run draws the same first question and
  option order and the verdict cannot flip between runs of one commit. Only the phone pass is seeded.
  A seed measures one draw, not a game's worst question: a game whose width depends on the draw is
  recorded in the to-do with its question ids (`moments-master`, §1.40), because a
  `tier1_phone_overflow` entry for a draw that fits fails as stale. **Never add retry or re-run
  logic to CI**; make the check deterministic instead. `--phone-widths FILE` writes every phone
  measurement to JSON so two runs can be compared.
- **Tier 2** scans every inline `<script>` and every `room.js` for the loop shape that froze
  modular-battle. Unlisted hits FAIL. Reviewed-safe loops live in `scripts/checker-allowlist.json`,
  keyed on **file + enclosing function name** (not line number), each with a written reason.
- **Tier 3 plays the games** — finds the options, clicks one, waits for the question to turn over,
  repeats. It is what tier 1 cannot be: modular-battle's freeze was on the *second* question, and a
  page load never gets there. Baseline 2026-09-23: **190 PASS, 0 FAIL, 6 WARN, 115 UNSUPPORTED**
  across 311 runs, 1544 questions played, ~16 min. Opt-in (`--tier 3`); `--tier all` is still 1+2.

**Three things about tier 3 that are load-bearing:**

- **UNSUPPORTED is not a failure, and the distinction is the whole point.** Tier 3 drives pick-one
  options and typed answers. A drag game, a canvas, a build-the-answer keypad or a second phase it
  cannot complete comes back UNSUPPORTED and never fails the run. The first draft called 118 of
  those FAIL — noise on that scale is how a checker gets ignored, and the one real failure inside it
  goes too. FAIL now means a crashed tab, a frozen main thread, a mid-play throw, or an option that
  cannot be clicked. The UNSUPPORTED list is the coverage ledger: record a game in
  `checker-allowlist.json` under `tier3_exceptions` **only once you have read it**, because what
  makes the ledger useful is that a game *newly* arriving on it is a change worth chasing.
- **Progress is read from the game, not the DOM.** 95 of 96 games fire `question_answered` with a
  `question_index` and 95 fire `game_completed`, so tier 3 hooks `window.mfg` through an accessor
  and counts events. Watching the options for a change instead is simply wrong for a binary game:
  `prime-or-composite` renders the same two buttons, PRIME and COMPOSITE, for every question it ever
  asks.
- **Options are found by behaviour, never by markup.** 27 games use `id="options"`, 8 use a class
  containing `option`, and **60 use neither**. Tier 3 takes every visible element carrying a click
  handler — as an `onclick` property (index-laws, suvat) or via `addEventListener` (angle-ace,
  matrix-crunch) — and groups by **parent alone**. Adding the class to that key splits
  prime-or-composite's `ans-prime`/`ans-composite` pair into two groups of one.

**Duplicate options are a WARN, deliberately.** A repeat in a pick-one group is a real defect —
Trig Worms shipped `-5.1` twice — but `expectation-station`'s stage 1 is a *tile bank* filling
several blanks, so `es_gcse_001`'s `['0.25','0.25','0.50','0.10']` is authored on purpose. Nothing
in the DOM tells the two apart, so the run reports it and a person judges.

**Timers are NOT throttled in headless Playwright.** `docs/game-integrity-2026-09-21.md` §5 says an
automation tab reports `document.hidden`, throttling timers to ~1.5/sec, and recommends draining
`setTimeout` callbacks by hand. That is true of the **Chrome-extension** tab and false here:
measured 2026-09-23, `document.hidden` is `false` and three chained 200ms timeouts finish in ~620ms.
Tier 3 waits on the game's real timers, so it sits through the delays a student sits through.

**When to run it:**

- **Before every commit touching `games/` or `escape-rooms/`.** No exceptions.
- **Any site-wide sweep runs it before committing** — a sweep is exactly what killed those two
  games, and the damage is invisible until someone opens the page.
- **Live verification uses `--live`, never a plain reload.** It cache-busts every page load.
  Chrome will happily replay the previous build and hand you a clean pass that means nothing.
- A **network guard is mandatory in every mode**, `--live` included: requests to the Apps Script
  endpoint, GA/gtag collect and Firebase are aborted over both HTTP and WebSocket, and the run
  fails if one completes. Checking a page must never write a row into the production Events
  sheet or a score into the live leaderboard.

`.github/workflows/check-site.yml` runs **tiers 1 and 2** on every push and PR. No secrets, free
runner. **Tier 3 is not in CI** — it takes ~16 minutes against ~85s for the other two, and it is new.
Putting it in CI is Jon's call once he has seen a few runs.

**Tier 3 is regression-proven, the same way tiers 1 and 2 were.** Restoring `1a407fe`'s
`while (choices.size < 4)` to modular-battle's `generateChoices` fails all three runs of
`--tier 3 --only modular-battle`; restoring the fixed version passes 24 questions. Note what that
proves and how: the loop does **not** hang politely enough for the watchdog — it allocates until
Chromium kills the tab, and Playwright reports "Target crashed". That is reported as *the page
crashed the browser tab*, not as a driver error, because blaming the checker for the one bug this
tier exists to find is how the tier stops being believed.

### Tier 4, layer A — bank extraction + lint (`scripts/extract-banks.py`, `scripts/check-banks.py`)

Tiers 1–3 prove a page runs and can be played. None of them inspects the *question
data* — matrix-crunch's duplicated determinant option, formula-unlocked's
`correct_override` collision, and normal-navigator's index patches all survived every
green checker run this repo has had, and were each found only by Jon playing the games.

Layer A closes that gap for **static data defects**: `extract-banks.py` reads every
game's question bank back from the live page under Playwright (post any runtime
patch), and `check-banks.py` lints it against eleven rules (B1–B11 — missing/duplicate
answers, duplicate questions, bank size, session-length overpromise, draft-prose
leaks, text that loses its spaces on render, duplicate object keys, hand-written index patches,
`correct_override` usage, options equal in value). **`data/check-ledger.json`** tracks every known violation
per game; CI (`.github/workflows/check-site.yml`) fails only on a violation not yet in
the ledger, or a ledger entry that no longer reproduces — a tracked, unfixed defect is
not a failure.

**B7, text that loses its spaces on render (rebuilt 2 Oct 2026, to-do §1.31).** Its KaTeX half used
to match two call shapes, `K(x.field)` and `katex.renderToString(x.field)`, and so never saw the 50
games that render through `rk`, `rkStr`, `tex`, `kx` and the rest (`docs/audit-katex-wrappers.md`).
Now, with no per-game list: **render sites are found by behaviour** (a function whose parameter, or
a local derived from it, reaches `katex.render`/`renderToString`/`MaffsText.html`, to a fixed point);
**what reaches each site is rebuilt per question** (locals, ternaries both ways, `||`, callbacks,
`shuffle`-like selectors), with **its guards evaluated per string**, so an option the game shows by
`textContent` is never counted; a game function on bank data is **computed in the page**, after
putting the page in the state that question sets where the function reads game state; and every
string is **rendered in the page through the site's own callee** (`extract-banks.py`), read as the
student sees it (`.katex-html`, a positive-width `.mspace` as a space). **The test**
(`bank_common.katex_lost_word_spaces`): a space the source has between two tokens is gone and one
of them is a word, 3+ letters or a 2-letter function word from a fixed list (`to of is as or an in
on at by if so no be do up it we he me my us am`), so maths products (`mg`, `bx`) never count and
units (`13 cm`) are out of scope. A site that cannot be rebuilt is listed by `--ci` as
`unresolved`, one fed only by a generator as `runtime-only` (log-laws Solve, free-daily-pizza,
graph-transformer, quadratic-factoriser; to-do §4 has the runtime-hook candidate), never a failure.
First run: 277 strings in 12 games, all of them in the audit's second count, 30 of 30 hand-read
hits genuine; the audit's other 246 strings were guarded (217), two-letter products (13) or other
(16). B7 alone has `RULE_MAX` 800. Fixtures: `check-banks.py --selftest`, and `--selftest-live`
renders them in a real page. Extraction takes about 40s longer for it.

**B11, options equal in value (2 Oct 2026, PR 51).** Two options that are different strings but
the same value (√50 beside 5√2) are invisible to B2 and to `MaffsOptions.build()`, which compare
strings. B11 parses every option with `bank_common.parse_value()`/`equal()` (SymPy; the one copy,
shared with `scripts/scan-value-equivalent-options.py`) and compares the distinct options within
each answer unit. An option it cannot read is never guessed at. A question whose ask names the form
("Write in standard form", "Simplify") is listed in `scripts/checker-allowlist.json` under
`b11_form_questions`, with a reason quoting the ask. **B11 findings are identified by content, not
position:** `bank_common.content_id()` is the SHA-1 of the whole question's canonical JSON, plus an
ordinal over exact copies, so inserting or reordering questions never turns a known pair into one
new + one stale entry. The whole question is hashed because a narrower hash (stem + ask + options)
gave one id to 74 groups of different questions in 21 games: simultaneous-solver's "Find x"
questions differ only in `sys`. The cost: editing any field of a question gives it a new id. `--ci` also fails in two cases beyond the
ledger diff: a bank the ledger knows as readable extracts as a generator (with the KaTeX CDN
unreachable, three games come back empty and every rule would pass them quietly), and a
`b11_form_questions` entry that matches nothing (the question changed; re-read it).

**Every finding is identified by content, not by bank index or line (to-do item 7, PR 52, 2 Oct
2026).** On 28 Sep the OpenDyslexic change moved `test-the-claim`'s known B8 entry from line 527 to
526, and CI failed on a defect it already tracked until the entry was moved by hand: a position-based
id turns any edit above a known defect into one new + one stale entry. B1, B2, B6, B7 and B10 now use
the question's `content_id()`. B3 is named after every copy in its group, sorted, so it survives
swaps too. B7's KaTeX and MaffsText halves, which carry no question, use the SHA-1 of the string plus
an ordinal. B8 uses the enclosing function (else top-level variable, else `(top level)`), the
duplicate keys and the SHA-1 of the object's text. B9 uses the target as written and the SHA-1 of
the right-hand side. B4, B5 and B11 are unchanged. The location goes in the detail and the line in
`line`. **Three things now change an id, all expected:** editing the content itself (a question's
fields, or a comment inside a B8 object), renaming a B8 object's enclosing function or variable, and
changing either syntax rewrite in `bank_common._shim_for_parser`, which B8 and B9 hash through and
which changes every B8/B9 id at once.

**`--write-ledger` merges; it never rebuilds (to-do §4 item 10, PR 53, 2 Oct 2026).** Only games this
run actually linted, or true generators the ledger already records as such, are replaced. Every other
game keeps its record byte for byte and is reported as carried, with its reason (withdrawn/off-roster,
not selected by `--only`, bank missing, bank not read) and entry count. So regression-rumble's three
B4 entries survive every write, and `--only=x --write-ledger` touches only `x`. **It refuses (exit 1,
nothing written)** when a bank the ledger knows as read (`generator: false`) came back missing or as a
generator, the KaTeX-CDN-unreachable case: a partial extraction is never the basis of a full ledger
write. A game new to the ledger that did not read is reported, not written; that includes a new
true generator, which has to be added deliberately.

Layer A is one of five designed layers, A–E; only A is built. **Full design, what each
layer catches, what none of them can (wording and pedagogy stay Jon's call), and the
proposed new-game gate: `docs/checker-tier4-design.md`.**

### No rejection sampling

**Build the candidate pool, dedupe on the same representation the answer check uses, shuffle,
slice.** Never draw at random and retry until the set happens to be big enough.

`while (choices.size < 4) { choices.add(randInt(0, mod - 1)) }` froze the tab on ~25% of
modular-battle's questions, because a modulus below 4 can never yield 4 distinct remainders.
Expectation Station had the same shape latent in its distractors. A loop that terminates only
when the dice cooperate is a hang waiting for the right question.

The test that separates a safe loop from a hanging one: **does a counter advance on every pass,
whatever the draw returns?** A Fisher-Yates shuffle reads `arr.length` and calls `Math.random`
just like the loop above, but its `i--` runs every time, so it is bounded. Rejection sampling
advances only when the draw happens to be new.

Constraints on distractors — sign, form, denominator — are **per-scenario properties, not global
rules**. Model them on the scenario that needs them rather than filtering a global pool until
what survives fits.

**Dedupe the distractors against each other, not just against the correct answer.** Trig Worms
filtered out candidates equal to the correct answer and nothing else, so when `asin` and `atan` of
the same near-zero ratio both returned -5.1 it shipped a question with **the same option twice**.
Where the candidate list can collide, top it up from a deterministic ladder (correct ±5, ±10, ±20,
clamped to the valid range) rather than redrawing. Finite list, no retry, always terminates.

### Assembling a question's options — `MaffsOptions.build()`

**Any new game assembles its options with `schools/assets/options.js`. Do not hand-roll it.**

```html
<script src="../../schools/assets/options.js"></script>
```
```js
const opts = MaffsOptions.build(q.correct, q.d);   // replaces shuffle([q.correct, ...q.d])
```

It guarantees the correct answer appears exactly once, that no two options share a key, and that
the order is shuffled by a bounded Fisher-Yates — never by retrying a draw. Options are compared on
`String(value)`, which is exactly what `dataset.val = v` stores and what the marking code compares
(canon §7.1). Deduping on any other representation would let through a pair the answer check cannot
tell apart, which is the whole failure being prevented.

**Why this exists rather than the rule above alone.** The Trig Worms lesson was written down as a
rule for authors and could not be applied platform-wide, because there was nowhere to apply it —
**32 games each hand-roll `shuffle([correct, ...d])` and not one checks for a collision.** Two more
shipped one, in shapes the Trig Worms rule does not describe:

- `matrix-crunch:171` **authored** it — `det([[6,2],[3,1]])` is 0 and `'0'` was listed in its own
  distractor array, so the question rendered **0, 0, 12, 6** with two buttons both marking correct.
- `formula-unlocked:295` **drifted** into it — a late `correct_override` was set to a string
  identical to the question's third distractor, so the override and that distractor became twins
  and the bank's real `correct` form never reached the screen at all.

**It cannot invent a replacement for what it drops.** A bank that authored a collision has one
fewer real option than its author intended, so those two questions now render **three** options,
honestly short — the same call modular-battle makes when a modulus of 2 has only 2 residues. It
warns to the console when it drops one (`console.warn`, never `console.error`, which would fail
tier 1). **Fixing the bank is still a teaching call**; this only guarantees the collision never
reaches a student.

**It cannot see two options that are equal in value.** To `String(value)`, √50 and 5√2 are different.
`coordinate-geometry-dash:233` shipped both, with only 5√2 marked right: a student who picked √50 was
marked wrong for a correct answer (fixed 28 Sep, to-do §1.24). A scan of every bank found the same
shape in 10 more games (`docs/scan-value-equivalent-options.md`). The guard belongs in the checker,
not here, because marking compares strings. Checker rule B11 (tier 4, layer A, 2 Oct 2026) now
fails CI on any new value-equal pair. **Never offer the answer in a second form unless the
question's ask names the form**; when it does, list the question in `checker-allowlist.json`'s
`b11_form_questions` with the ask quoted.

**Wired into `matrix-crunch`, `formula-unlocked` and `proof-builder` only.** The other ~28 games
hand-rolling this were deliberately left alone — that retrofit is a separate pass, and sweeps are
what killed `chart-interrogator` and `modular-battle` for six months.

### Check the generator's own range

Trig Worms picked its angle from `5*Math.floor(Math.random()*17)+15`, which is 15..**95**, with a
comment claiming it avoided 90. Neither 90 nor 95 can be the non-right angle of a right-angled
triangle; at 95 the adjacent goes negative and the game asked for a side of **-0.8**. It had been
doing that to 11.8% of questions, at every difficulty, since the game shipped.

**A comment saying a range is safe is not evidence that it is.** When a generator picks from a
range, enumerate the endpoints and ask what the game does at each one.

## Level Colours
| Level | Colour | CSS Var |
|-------|--------|---------|
| Year 6 | Indigo | #6366f1 |
| KS3 | Green | #22c55e |
| GCSE | Blue | #3b82f6 |
| A-Level | Orange | #f97316 |
| Further | Purple | #8b5cf6 |
| Level 4 | Red | #ef4444 |
| Core Maths | Sky | #0ea5e9 |

## Scaffolds fade, and never pre-announce the answer

Jon's rule, 22 Sep 2026. A visual aid earns its place by building the model, and then by getting
out of the way.

- **A scaffold is withdrawn once the student can work without it.** Modular Battle's dot grid now
  hides after 2 correct and returns after 2 wrong in a row. Showing it on every question turns
  "46 mod 7" into "count the red circles" — the student never divides. The picture teaches the
  model; **removing it is what embeds it.**
- **A visual aid must never give the answer away before the student has thought.** If it can only
  be made useful by pre-marking the answer, prefer showing it *after* they answer, as the reason.
- **If it cannot be drawn honestly, do not draw it.** Modular Battle scaled its dots to fit a
  40-dot cap, and scaling a count cannot preserve a remainder — it displayed 3 for an answer of 4.
  Draw it in full or omit it; never a lossy version of something that has to be exact.

## Accessibility
- **Aa toggle** on every game — OpenDyslexic font, increased spacing
- State persists in localStorage (`mfg_accessible`)
- Colour feedback: tick/cross symbols alongside colour
- `prefers-reduced-motion` respected

## Tiered Question Banks
Games load level-keyed banks via URL param: `/games/{slug}/?level=level4`
```js
const QUESTIONS = { ks3: [...], gcse: [...], alevel: [...], further: [...], level4: [...], year6: [...] }
```

## Firebase Leaderboard (LIVE)
- A status that depends on other records is computed at display time, never stored — see `docs/canon.md` §9 "Architecture".
- Firebase Realtime Database (europe-west1, project `maffsgames-c1c9f`)
- Anonymous score submission — `MaffsLeaderboard.submitScore(slug, level, score, questionsAnswered)`
- 3-letter arcade initials (profanity filter, ~50 blocked combos, localStorage persistence)
- High score detection: gold trophy (all-time), blue star (weekly best)
- All-time best shown as target on each ticker entry
- `recent_scores` feed powers the portal ticker (reads the latest 20). The client no longer prunes it: the database rules in `firebase/database.rules.json` (source of truth, create-only; emulator tests in `firebase/rules.test.mjs`) refuse every delete and overwrite; **deployed and verified live 30 Sep 2026**, so a score can now only be deleted in the Firebase console. Deploy, verify, roll back and the manual prune: `docs/firebase-rules-deploy.md`
- **Eligibility is completion, not a question count** (23 Sep 2026). A run that reaches the game's own end ranks; `submitScore()` must only ever be called there. Every unsubmitted score is logged with its reason. The old 10-question gate silently kept 13 games (Prime Sprint, Estimation Golf, Equatle, Gantt, Chart Interrogator …) off the leaderboards since launch
- Wired into 94 of the 96 live games (`constructions-lab`, `given-that` excluded — non-scored; `regression-rumble` withdrawn 30 Sep 2026, declared `WITHDRAWN` in the coverage check, its boards kept); recounted from the repo 29 Sep 2026, plus `six-sevens-bruv` and `free-daily-pizza` on 30 Sep. Four of the 94 carry a call-site gate declared in `HELD`: `estimation-golf`, `equatle` and `distinctly-average` submit nothing today, `log-laws` submits its Laws drill only — so 90 submit unconditionally. `six-sevens-bruv` submits its 20- and 40-question sessions to levels `q20`/`q40` and its clear-the-grid sessions to no board. `free-daily-pizza` submits mixed-stage practice to `practice-q20`/`practice-q40` (single-stage practice ranks nowhere: history only, under `stage-s1-q20` etc.) and each UK day's pizza to `daily-YYYY-MM-DD`, a pattern declared off the hub in the coverage check's `OFF_HUB_LEVEL_PATTERNS`. Coverage enforced by `scripts/check-leaderboard-coverage.js`, which since 30 Sep 2026 also fails if a submitting game is missing from the hub registry (`leaderboards/index.html` `GAMES`) or listed with levels other than the ones it submits under (canon §9)
- Device-local score history alongside it: `schools/assets/score-history.js` (`MaffsScoreHistory`) — last 10 runs per game+level, `localStorage` only, no server call
- Public hub page: `/leaderboards/index.html` — rolling 7-day top scores + all-time-high per game, plus a "Your Scores" device-local section. See `docs/canon.md` §9 for full detail
- Certificates planned for Phase 1b (still not built)
- **Lesson from the retrofit:** the July rollout shipped the feature to every game but left the
  old *"Global leaderboard coming soon"* copy in place — 78 games told students the leaderboard
  did not exist while submitting their scores to it. Fixed 2026-08-26. When rolling a feature out
  site-wide, grep for the placeholder copy it is meant to replace.
