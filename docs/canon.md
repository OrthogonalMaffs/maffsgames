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
| Total games | 96 live, all on portal (`six-sevens-bruv` and `free-daily-pizza` added 30 Sep 2026; `regression-rumble` **withdrawn** the same night behind a `noindex` holding page pending its data rebuild, todo §1.26). Per-game detail in `.claude/rules/game-roster.md` (96 numbered rows, plus a Withdrawn section). `games/` holds **98 directories** — the extras are `regression-rumble` (withdrawn, a holding page) and `the-perfect-prank`, the unlisted escape-room prototype, deliberately not on the portal and not in the roster. Because the roster is where `scripts/check-site.py` reads each game's levels, that game is only ever loaded bare; it is recorded under `roster_exceptions` in `scripts/checker-allowlist.json` so the gap is declared rather than silent |
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
| SR-5 | **Comparison questions never tie.** The options differ by at least the smallest unit shown (1p, 0.1, …). Draw from the values that qualify, never a redraw loop (no rejection sampling: CLAUDE.md, tier 2). | 3 Oct 2026 | PR #12 (split-it Best Value) |
| SR-6 | **Wording, picture and key agree.** Where one disagrees, change it to match the other two. | 3 Oct 2026 | PR #11 (Circle Theorem Spotter Q19) |
| SR-7 | **Tax, NI and student loan figures** in a game are the teaching year's, as in `scripts/uk_rates.py`, and the game is registered in `scripts/check-tax-year.py`. Scripts never restate a rate. | 3 Oct 2026 | §7.1.4; PR #7, PR #8 |
| SR-8 | **When a key changes,** recompute every dependent answer, distractor and worked line. | 3 Oct 2026 | PR #4 (tax-theft), PR #11 |
| SR-9 | **Bugs found outside the task are logged, not fixed,** except a live wrong answer in the same game that one of these rulings fixes: fix it and list it in the PR. | 3 Oct 2026 | todo START ("a live bug is never a decision item") |
| SR-10 | **Whole items scale by whole numbers.** A recipe with an ingredient that comes in whole items (eggs) is scaled only by a whole-number factor (×2, ×3). Draw its scale factors from whole numbers only (no redraw loop, SR-5); the game's verifier checks every whole-item amount it scales is a whole number. | 3 Oct 2026 | todo §1.47; split-it's GCSE Pancakes (3.3 eggs) |

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
(its "Show them" toggle). `scripts/test-section-clicks.py` (CI) clicks every labelled element and
checks the payload, and that game cards and `fact_expanded` are unchanged.

## 1.4 Dashboard Charts (auto-updating)

1. **Top Games** — bar chart, 7-day, sorted by starts
2. **Level Split** — pie chart, KS3/GCSE/A-Level/Core/L4/Further
3. **Accuracy by Game** — bar chart, sorted lowest first (hardest games)
4. **Hardest Questions** — table, top 15 lowest accuracy (min 5 attempts)
5. **Daily Activity** — line chart, 30-day trend

---

# 2. SEO Requirements — Mandatory on Every Page

## 2.1 Required Tags

### Meta description
```html
<meta name="description" content="[150-160 char description]">
```

### Canonical link
```html
<link rel="canonical" href="https://maffsgames.co.uk/games/{slug}/">
```

### OG and Twitter tags (every game page)
```html
<meta property="og:title" content="{Game Name} — MaffsGames">
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

## 4.3 Games excluded from leaderboards

`constructions-lab` and `given-that` — non-scored, exploratory formats. They are the only two of the
97 that do not call `submitScore()`. (`distinctly-average` was briefly a third, 29 Sep 2026; Jon ruled it
should have a leaderboard, so it is wired and **held** rather than excluded — see §9.)

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

| **Section** | **Topic** | **Coverage** | **Status** |
| --- | --- | --- | --- |
| §3.1 | Analysis of data | Stat Attack, Chart Interrogator, Core Maths Paper 1 | Covered |
| §3.2 | Maths for personal finance | Tax Theft, Core Maths Paper 1 | Covered |
| §3.3 | Estimation | Fermi Lab, Estimation Golf, Estimation Engine | Covered |
| §3.4 | Critical analysis of given data and models | Core Maths Papers 2A, 2B, 2C | Covered |
| §3.5 | The normal distribution | Normal Navigator, Core Maths Paper 2A | Covered |
| §3.6 | Probabilities and estimation (sampling, point estimates, confidence intervals) | Core Maths Paper 2A | Covered (by the practice paper only) |
| §3.7 | Correlation and regression | Correlation or Coincidence, Regression Rumble, Core Maths Paper 2A | Covered |
| §3.8 | Critical path analysis | Glorious Gantt Game | Covered |
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
  dot drawn (see "Scaffolds fade" in CLAUDE.md: a count is never scaled).
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
  level does (Split It's KS3 button reads "Foundation", Jon's ruling of 2 Oct 2026; a third level, if a game has one, is "Advanced"). **Level keys never change**: the Firebase leaderboard keys (`ks3`, `gcse` …) stay as they are, and the label a student sees is declared once per game and read by the leaderboard hub too (§3.12; it folds into `games.json` when that is built).
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
Trig Worms fix (CLAUDE.md:577, "No rejection sampling") — Trig Worms had a dedupe step
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
  CLAUDE.md:577). Wired into `matrix-crunch:306`, `formula-unlocked:447` and
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
