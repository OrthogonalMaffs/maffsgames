# ROOM-SEARCH-TITLES (Jon, 6 Nov 2026, consolidated 18:50), verbatim

LANE: home (Claude Code) · TIER: Shared · from current main · CONTRACT: ROOM-SEARCH-TITLES (consolidated 6 Nov 18:50; supersedes the first version, which built nothing)

COORDINATION: the cloud lane owns games/whose-side-are-you-on/ (WHOSE-SIDE-BIOS). Codex owns tools/pack-generator/ and may add <b> markup to escape-rooms/christmas-tree-fiasco/room.js (CHRISTMAS-PACK). Touch neither. Record in docs/handover/home.md.

TASK: Give every live escape-room page and the escape-rooms hub a generated, checked search title and description that lead with what a teacher searches, through the same system as game pages.

ROOT CAUSE: Game pages' titles and descriptions are generated from data/games.json and held by scripts/check-meta.py (canon §2.1); escape-room pages were never brought into that system, so their heads are hand-written story names ("The Kiln Disaster — MaffsGames Escape Rooms", "The Great Hamster Heist — MaffsGames"), with two different suffixes, and descriptions that lead with the plot. Nobody searches a room's story name; the hub, whose title is a search phrase, takes 83% of escape-room AI impressions (GSC, 6 Nov).

CLASS CHECK: Yes. Every room page has the same fault, and the fix belongs in the shared metadata system (games.json + check-meta.py + apply-meta.py), so a future room cannot ship without a checked title. Not 14 hand edits.

EXACT CHANGE:
1. data/games.json gains "rooms": one entry per LIVE room: slug, search_phrase, level, and an optional short_topics (used only as below). The hub's stated title and description join "pages". The withdrawn room (it-vengeance) is excluded and stays as it is.
2. scripts/check-meta.py (rules in its docstring; canon §2.1 updated to say rooms are included):
   Title: "<search_phrase> Escape Room – <level> | MaffsGames", at most 60 characters (if over: "<search_phrase> Escape Room | MaffsGames", reported).
   Description: "Maths escape room on <topics>. <clock> minutes, <level>. Free, no sign-up." at most 155 characters, where:
   - <topics> = the room's teacher.html window.TEACH lockMeta topics, joined "A, B and C", each lower-cased after its first letter except acronyms and proper names (LCM, HCF, Venn, Pythagoras, Celsius); if the description would exceed 155, short_topics is used instead; if there is none, or it still exceeds 155, CI fails (a person writes short_topics).
   - <clock> = the room's own timer from its room.js (the start screen's figure), read only; never the sum of lockMeta minutes (those are puzzle time).
   og:/twitter: copies held as for game pages. CI fails any live room page whose head differs, and any live room with no entry.
3. scripts/apply-meta.py writes them (same rewriter, idempotent). Run it; run check-meta.py.
4. Entries (search_phrase · level · short_topics where needed):
   christmas-tree-fiasco: Christmas Maths · KS3 & GCSE
   kiln-disaster: Multiples & LCM · GCSE Foundation
   big-school-begins: Year 7 Transition Maths · KS3 · short_topics "Coordinates, compass directions, time and money"
   canteen-hack: Simultaneous Equations · GCSE
   car-trap: Arc Length Maths · GCSE
   comic-caper: Factors, Primes & HCF · KS3 & GCSE
   hamster-heist: Circumference Maths · GCSE
   heatwave-mutiny: LCM and Inequalities · GCSE
   library-jam: Decimals and Angles · KS3
   pe-shed-rebellion: Inverse Proportion · GCSE
   prom-budget: Reverse Percentages · GCSE
   rightful-king: Venn Diagram · GCSE Higher · short_topics "Counting, exponential decay and conditional probability"
   roll-for-initiative: Probability Maths · GCSE
   rugby-mud: Index Laws Maths · GCSE Higher
   Hub: title "Free Maths Escape Rooms for KS3 & GCSE | MaffsGames"; description = the hub's existing live og:description, provided it is at most 155 characters and any room count in it equals the number of live rooms (else STOP).
   Report every generated title and description in a table in the PR body, with character counts and any fallback used.
5. Only <head> title/description/og/twitter tags change. The room's visible heading, story name, hub card text, room.js and teacher pages are unchanged.
6. No /updates/ line (invisible to users).

DO NOT TOUCH: room.js and teacher.html (read only), variants.json, any room's body text or art; game pages' existing titles; the portal and /essentials/ cards; sitemap.xml; it-vengeance; the files under COORDINATION.

SUCCESS CONDITION: Every live room page and the hub carry a generated title and description that check-meta.py holds in CI; planted faults fail check-meta.py: a hand-edited room title, a live room missing from games.json, a description over 155 with no short_topics, a clock figure differing from room.js; apply-meta.py is idempotent; no title uses the fallback. Committed, PR open, Gate green, home.md entry; stop for Project Claude's review AND Jon's approval of the title table before merge.

STOP IF: a room's timer cannot be read from its room.js (report which); the hub's og:description is over 155 or its room count is wrong; any title still needs the fallback; a room page's head has a shape the rewriter cannot read; a change outside <head> seems necessary.
