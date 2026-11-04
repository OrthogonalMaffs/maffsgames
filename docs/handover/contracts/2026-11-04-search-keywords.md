# SEARCH-KEYWORDS (received 4 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER). Started after ROOM-ESCAPED merged (#656, a7b476c).

## Contract (verbatim)

CONTRACT: SEARCH-KEYWORDS (cloud lane, Shared; Jon, 4 Nov 2026)
LANE EXCEPTION, THIS CONTRACT ONLY (Jon, 4 Nov): you may edit schools/assets/card-filter.js, add one new shared file
under schools/assets/, edit data/games.json, root index.html and essentials/index.html, scripts/check-meta.py and
scripts/apply-meta.py, scripts/verify-card-filter.py, and /updates/. Save this contract verbatim as
docs/handover/contracts/2026-11-04-search-keywords.md in the first commit, with one line in docs/handover/cloud.md's queue.

TASK: A teacher who types the topic (e.g. "circle", "nth term", "simultaneous equations") into any MaffsGames search
box finds the games that teach it, whatever the game is called.

ROOT CAUSE: Search matches only the text visible on a card (title, description, hook, tags). Game names are deliberately
playful ("Take a Walk", "Six Sevens, Bruv"), so a topic word finds a game only if it happens to be in the card's
description. The metadata that does name the topic (search_phrase in data/games.json) is used only for page titles,
never for search. Separately, the site has TWO search matchers with different rules: the portal (index.html
applyFilters, ~line 3366) needs the whole query as one substring of the card text, so "area circle" finds nothing;
schools/assets/card-filter.js (used by /essentials/) needs every word to appear somewhere, so "area circle" works.

CLASS CHECK: Yes, a bug class, on two counts. (1) The same defect, topic words not searchable, affects every card on
every page that searches cards: the portal and /essentials/ today, any page that adopts card-filter.js tomorrow. (2) The
same function (match a query against a card) is implemented twice with different behaviour. So the fix is at the
architectural layer: keywords live once, per game, in data/games.json (the single metadata source, Jon's ruling, Oct
2026); they reach every card through the existing games.json-to-pages pipeline (apply-meta.py, held by check-meta.py
in CI); and ONE shared matcher decides a match on every page. Not a per-card text tweak, and not a third matcher.

EXACT CHANGE:
1. data/games.json: add "keywords" to every game: an array of lowercase strings, at least 4 per game, in the words a
   UK maths teacher would type: the topic name(s), the spec wording (AQA/Edexcel/OCR/BTEC), common synonyms
   (e.g. "nth term", "sequences", "arithmetic sequence"; "pie chart", "pie charts"), and the level words where they
   help ("foundation", "higher", "resit", "core maths", "a level", "further maths", "btec"). Derive them from each
   game's own question bank and spec mapping, not its name. No keyword the game does not actually teach. No brand
   names, no student slang, no misspellings.
2. scripts/check-meta.py: rules for "keywords": present on every game, at least 4, lowercase, trimmed, no duplicates
   within a game, each 2-40 characters. Plus the card rule below. Self-test: add planted faults for each.
3. scripts/apply-meta.py (via check-meta.py's expected values, as for titles): write data-keywords="kw1 | kw2 | ..."
   onto every game card on index.html and essentials/index.html whose link resolves to that slug (a game appears in
   several portal sections; every copy gets it). Idempotent. check-meta.py fails CI when a card's data-keywords differ
   from games.json, or a card links to a slug with no games.json record (list those; do not invent keywords for them).
4. New shared matcher, schools/assets/search.js, window.MaffsSearch.match(card, query) -> boolean:
   - haystack = the card's visible text plus its data-keywords, whitespace collapsed, lowercase;
   - the query is split into words; a card matches when EVERY word is found in the haystack (card-filter.js's rule);
   - a query word longer than 3 letters ending in "s" also matches without the "s" ("circles" finds a keyword "circle");
   - empty query matches everything. No ranking, no fuzzy matching.
5. index.html applyFilters() and card-filter.js matches() both call MaffsSearch.match; delete their own text matching.
   Filter analytics are unchanged: same events, same parameters, result_count still re-read from #gameCount.
6. scripts/verify-card-filter.py (or a new verify-search.py beside it, wired into CI the same way): render the portal
   and /essentials/ in Chromium and assert these queries return the named game (portal and, where the game is on it,
   /essentials/): "circle" and "circles" -> take-a-walk; "area circle" -> take-a-walk; "nth term" -> sequence-solver;
   "times tables" -> six-sevens-bruv; "ratio" -> split-it; "income tax" -> tax-theft; "prime" -> prime-or-composite;
   "circle theorems" -> circle-theorem-spotter. Add 10 more of your own from the keywords, one per topic area.
   Also assert a nonsense query ("zzqx") gives 0 and the "no results" message. Planted faults: break the matcher,
   drop a card's data-keywords; both must fail.
7. /updates/: one line in teacher language ("Search now finds games by topic, e.g. 'circle' or 'nth term'...").
8. Write docs/search-keywords-review.md: a table of every game, its name, and its keywords, for Project Claude's
   review of the content before merge.

DO NOT TOUCH: game pages under games/ (their titles and meta stay as they are); search_phrase values; the page
<title>/description rules; canon.md (put the canon §7 note for the home lane in docs/handover/cloud.md instead);
analytics.js, the Apps Script endpoint and every analytics event or parameter; card visible text, layout and CSS;
the escape-room band; leaderboards; the workflow file; docs/todo.md; anything in the home lane's queue
(escape-room packs). No sitemap or SEO changes: data-keywords is for on-site search only.

SUCCESS CONDITION: Every game in data/games.json has at least 4 keywords and every card on the portal and /essentials/
carries them, held by check-meta.py in CI; both pages search through the one MaffsSearch.match; all step-6 queries
pass on both pages with their planted faults caught; main green; the PR stops at a green Gate with
docs/search-keywords-review.md for Project Claude's review and Jon's "merge"; the work is committed and
docs/handover/cloud.md records the state, so the home session knows where it stands.

STOP IF: a portal card links to a game that has no games.json record and is listed (report the list, do not add
records); more than 5 games give you too little to derive 4 honest keywords from their own content; the portal's
filter code turns out to need restructuring beyond swapping its match line (e.g. the level/topic/fresh logic is
tangled with the text match); keeping card-filter.js's analytics identical proves impossible; any search page
other than the portal and /essentials/ turns up (list it, do not edit it); CI's time budget is exceeded by the new
browser checks.

## Found on receipt (4 Nov, Claude Code)

- STOP IF 1: one portal card links to a page with no "games" record: `the-6-ps/` (index.html:1717, GCSE section,
  listed since 27 Oct). It is not a game: canon §0 records that The 6 P's "is listed through data/games.json 'pages'"
  and has no roster row, so it cannot have a "games" record (check-meta.py holds games = roster rows). It does have a
  games.json record, `pages["the-6-ps/index.html"]`. Decided for you (standing STOP IF rules, 27 Oct): its keywords go
  on that existing pages record and its card is held to them like any game's; no record is added. Every other card on
  both pages (123 portal, 38 Essentials) resolves to a games.json game.
- STOP IF 5 clear: the only pages with a search box are index.html and essentials/index.html (every .html searched for
  type="search", card-filter.js and searchInput).
- STOP IF 3 clear: applyFilters' text match is two lines (`var text = ...`, `var searchMatch = ...`); level, topic and
  fresh are separate booleans.
- Baseline on the portal's visible card text: with the every-word rule alone, 7 of the 8 named queries already find
  their game; "nth term" is the one that needs keywords today. The dropped-keywords plant therefore drops
  sequence-solver's.
