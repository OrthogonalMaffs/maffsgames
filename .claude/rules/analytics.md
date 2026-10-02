# Analytics — Dual Logging (GA4 + Google Sheets)

All 91 games send events to both GA4 and a Google Sheets backend via the `mfg()` wrapper function.

## Infrastructure
- GA4 cookieless mode (`G-992JLHLP2D`) — no cookies, GDPR/PECR compliant
- Google Sheets backend via Apps Script — raw event-level data, no sampling
- Shared wrapper: `schools/assets/analytics.js` — loaded on every game via `<script>` tag
- Apps Script code: `docs/apps-script-endpoint.js` — includes daily email report + Dashboard charts
- Daily report emails to Jon (owner) at 7am UK time

## Usage
Call `mfg()` instead of `gtag('event',...)`. The wrapper sends to both GA4 and Sheets.

## Events — Required on ALL Games

```js
mfg('game_started', { game_slug: 'slug', level: currentLevel, mode: selectedMode });
mfg('question_answered', { game_slug: 'slug', level: currentLevel, question_index: n, correct: bool });
mfg('game_completed', { game_slug: 'slug', level: currentLevel, score: n, questions_answered: n, questions_correct: n });
mfg('personal_best_set', { game_slug: 'slug', level: currentLevel, score: n, previous_best: n });
```

Abandon tracking handled automatically by `analytics.js` via `visibilitychange`.

## Portal events — root `index.html` only, not games

```js
mfg('filter_applied',     { level, topic, fresh, search_used, search_length, search_query,
                            result_count, trigger, filter_type, filter_value });
mfg('game_card_clicked',  { level, topic, fresh, search_used, search_length, search_query,
                            result_count, game_slug, section, filter_type, filter_value });
```

`trigger` is `level` | `topic` | `fresh` | `search` | `reset` (`reset` reserved — no such control
yet). Search is debounced 1000 ms and only sends when the trimmed query changed. `section` is the
section id, or its heading text when there is none (currently always). `result_count` is read back
from `#gameCount`, the de-duplicated total `applyFilters()` already computed — never recount, a
game appears in several sections.

**`filter_value` exists because the Sheets endpoint drops unknown keys.** `doPost` writes a fixed
column list, so of everything above only `event`, `game_slug` and `level` would reach the sheet.
`filter_type`/`filter_value` are reserved columns nothing else writes, so the state is packed in,
in exactly this key order:

```
v1|level=<level>;topic=<topic>;fresh=0|1;su=0|1;sl=<search_length>;q=<search_query>;n=<result_count>
```

`filter_type` = `trigger` on `filter_applied`, `section` on `game_card_clicked`. `;`, `=` and `|`
are stripped from `q` so a search term cannot break parsing. Keep the `v1|` prefix: it is what lets
the format change later without invalidating rows already in the sheet.

**Two rules that must survive the move to generated cards:** `getFilterState()` is the only reader
of filter state, and card clicks use ONE delegated listener — never per-card handlers on the ~130
duplicated `.game-card` elements.

## Rules
- `game_slug` always matches the directory name
- `level` from game state / URL param
- `question_index` is 1-based
- Games without levels use level `'all'`
- Multi-mode games MUST include `mode` on all events
- Do not add any additional data collection without explicit approval from Jon
