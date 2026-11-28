TODO-SEARCH-DEMAND — home lane — Small tier (docs only): merges on green
Recommended: Claude Code, Sonnet, effort medium. Exact text is given; the only judgement is which finished todo parts to move out.
Send when: the home lane is free.

TASK: Put the 27 Nov 2026 search-log findings, the 3-gon Line-up build and Jon's Level 3 full-release plan into docs/todo.md; close two §6 manual tasks the Events sheet has answered; correct canon's stale ticker line; trim docs/todo.md to make room.

ROOT CAUSE: Jon ruled on 27 Nov 2026 (Project Claude chat) that the search items go on the backlog, that 3-gon Line-up is built next with Venn Diagrams AGAIN? after it, and that the Level 3 games are scaled up for full release after that. None of it is in the repo. docs/todo.md is 107,496 bytes against TODO_LIMIT 107,520 (scripts/check-context-size.py:59), so nothing fits until finished parts move out. Canon §1 line 3335 says the ticker "reads the latest 20"; since TICKER-LISTED (#940, 95d82bf) index.html:3927 reads TICKER_READ = 50 and shows TICKER_SHOW = 20 from games with a portal card (shown, index.html:3927-3930).

CLASS CHECK: Not a bug class. Backlog and canon text only. Where the new rows describe a shared-code fix (SEARCH-DEMAND part 1), the row itself names the shared layer, so the later contract starts architectural.

EXACT CHANGE:
1. First commit: save this contract verbatim to docs/handover/contracts/2026-11-27-todo-search-demand.md. TICKER-LISTED's close-out is not this lane's: it rides on the cloud lane's next task (AGENTS.md "Cloud close-outs").

2. docs/todo.md §6 "Manual tasks": move these two lines, word for word, to docs/history/todo-done.md under a new heading "## Part closed by TODO-SEARCH-DEMAND (27 Nov 2026)", each followed by its answer line:
   - "- Events sheet: confirm no `game_abandoned` against the homepage, 1–15 Sep."
     Answer: "Answered 27 Nov 2026 by Project Claude from Jon's Events sheet download: 53 `game_abandoned` events on 1–15 Sep carry no game_slug, i.e. fired from pages with no game (the homepage among them). The fault is fixed: the last blank-slug abandon is 3 Nov 2026 18:44 UTC and there are none since 4 Nov."
   - "- Events sheet (optional): `binomial-blaster` `game_completed`, score 400, about 17:16 UTC 16 Sep; if present, the deleted Firebase score was real and can be restored."
     Answer: "Answered 27 Nov 2026 by Project Claude from Jon's Events sheet download: not present. binomial-blaster has no event of any kind on 16 Sep (the Sheet holds 2 events between 16:30 and 18:00 UTC that day, both misunderstood-maths). The score is not restored."

3. docs/todo.md §6 "Decisions": move the line "- None open (11 Nov 2026: matrix-crunch's fourth distractor, §1.4, ruled by Jon on 10 Nov and closed by CLOUD-QUEUE-1111 PR 1)." word for word to the same todo-done heading, and put in its place:
   "- Functional Skills Maths: no game maps to its spec, and teachers and students look for it: 6 site searches 22 Sep–27 Nov 2026 (\"functional skills\", Level 1 and Level 2), and Level 2 phrasings at 10K–100K a month in Keyword Planner (7 Oct). Map existing games to the spec, build for it, or leave it (Jon)."

4. docs/todo.md §3 table: insert these three rows immediately after the PLOT-MIGRATE row (currently line 114), exactly as written:
| 3-GON-LINE-UP | **3-gon Line-up (`3-gon-line-up`), a congruence game for GCSE (G5.1, G6.1, G7.1; Jon, 27-28 Nov 2026): a police line-up of triangles in four stages (squared paper; not drawn accurately; which rule proves it, AAS answered as ASA; is the witness right?), built by contract 3-GON-LINE-UP-BUILD (cloud lane, 28 Nov 2026) and merged unlisted.** **Jon:** plays all four stages and gets some wrong; writes the LINES lines (placeholders now), the tagline and the look; rules on listing. Listed under GCSE, not Essentials (G5.1 stays OUT in the grade 1-3 banding). | Jon's play |
| SEARCH-DEMAND | **Site search: three fixes from the search log (Jon, 27 Nov 2026; Events sheet: since the 4 Nov keyword fix, 29 of 189 searches found nothing, 11 of them with a filter on).** (1) **Empty state:** "No games match this filter yet. More coming soon." (`index.html` `#noResults`) shows even when the search alone matches games; with any filter on (level, topic, New & updated), offer one click that clears the filters and shows them. The portal's `applyFilters()` and `MaffsCardFilter` (`schools/assets/card-filter.js`) each have an empty state, so the fix goes in one shared place both use. (2) **Escape rooms in search:** homepage search covers `.game-card` only, so "kiln disaster", "arc", "hcf" and "multiples" found nothing; `data/games.json` "rooms" holds their topics. (3) **Keywords** (`data/games.json`, applied by `scripts/apply-meta.py`), each only where the game's bank covers it: "67" (`six-sevens-bruv`), "open brackets" (`hc-factor`), "factorizing", "radicals", "slope", "common ratio", "ks2". | — |
| L3-FULL-RELEASE | **Scale the Level 3 games up for full release (Jon, 27 Nov 2026), after "a couple of gap games" (3-gon Line-up, then Venn Diagrams AGAIN?):** add GCSE or A-Level questions, whichever each game fits. Games with L3 in the roster: `i-dropped-my-ice-cream`, `cast-away`, `log-laws`, `its-a-sine`, `d-by-dx-why`. I Dropped My Ice Cream's other shapes (Jon: "not just circles and cones") are ICE-CREAM-GCSE. Scope per game is specced with Jon first. | 3-GON-LINE-UP, Venn Diagrams AGAIN? |

5. docs/todo.md "Game ideas, not yet built", exact replacements:
   - "- **Venn Diagrams AGAIN?**: HCF and LCM via prime-factor Venn diagrams."
     becomes
     "- **Venn Diagrams AGAIN?** (the next build after 3-gon Line-up, Jon, 27 Nov 2026): HCF and LCM via prime-factor Venn diagrams. Searched on the site: \"hcf\", \"multiples\"."
   - "- **Not in Pen**: constructing charts (drag bars, set pie angles, plot scatter points) (S2, S6)."
     becomes
     "- **Not in Pen**: constructing charts (drag bars, set pie angles, plot scatter points) (S2, S6). Searched on the site: \"constructing a pie chart\"."
   - Under "**Other games:**", after the "- **Is That a Fake Bag?**" line, add:
     "- **Plans and elevations** [PROPOSED]: G13.2, a GAP in the resit audit; searched on the site (\"elevation\")."
     "- **Whack-a-mole** [PROPOSED]: a fast-recall format, searched for three times (\"wack a mole\", \"wacka\"); topic open (Jon)."

6. Trim: move further finished parts of docs/todo.md to docs/history/todo-done.md, word for word, under the same heading, by the AGENTS.md rule (a row records only what is still owed; a finished part moves; a finished row moves whole). Verify each part as finished on main (a merged PR, a file or line that exists) before moving it, and list each move with its evidence in the PR body. Stop moving once docs/todo.md, with steps 2-5 applied, is at least 1,024 bytes under TODO_LIMIT. Never shorten or reword a part that is still owed.

7. docs/canon.md line 3335: replace "(reads the latest 20)" with "(reads the latest 50 and shows the newest 20 from games with a portal card; TICKER-LISTED, #940, 27 Nov 2026)". Nothing else in that line or in canon changes.

8. docs/handover/home.md: a new entry by the house format. No /updates/ line (internal work).

DO NOT TOUCH: any game, index.html, data/games.json, schools/assets/, scripts/ (check-context-size.py and TODO_LIMIT included: gate files are the cloud lane's), canon outside line 3335, AGENTS.md, CLAUDE.md, the roster. Do not add 3-gon Line-up's roster row: its build contract does that. Do not edit or move any part of a row that is still owed, including the ICE-CREAM-GCSE, D-BY-DX and GRAPH-SKETCHER-REDESIGN rows.

SUCCESS CONDITION: The three new §3 rows, the ideas edits, the §6 changes and the canon line are on main exactly as written. The four moved lines sit in docs/history/todo-done.md under "## Part closed by TODO-SEARCH-DEMAND (27 Nov 2026)", each §6 manual task with its answer line. docs/todo.md is at least 1,024 bytes under TODO_LIMIT. check-context-size.py passes with no new row-length warning from the three new rows (each is under 1,200 characters). Gate green; merged with merge-pr.py --watch; main's runs green; the PR body lists every trim move with its evidence.

STOP IF: (1) Finished parts verified on main come to less than the bytes needed for 1,024 bytes of headroom: apply steps 1-5 and 7 only if they fit under TODO_LIMIT, then report the shortfall and the candidates you were unsure of; do not merge an over-limit todo.md and do not shorten owed text. (2) Any of the exact "before" lines in steps 2, 3, 5 or 7 is not on main as quoted: stop and report what is there. (3) A part's finished state is unclear: leave it in place and list it in the report.
