CONTRACT: DND-ROOM-RELEASE (Project Claude for Jon, 16 Oct 2026, 17:40). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Release Roll for Initiative: the room becomes its own live,
indexed page with its hub card, front-page card, sitemap entry and room
counts, as The Rightful King and The Library Jam were released.

ROOT CAUSE: The room is built and live but unlisted (#417), with its
art. Jon play-tested it on 16 Oct ("it worked nicely"). Mrs Rogers
previewed it with no changes requested (Jon, 16 Oct, 17:36: release).
It still sits behind a noindex holding page with analytics off and no
hub card.

CLASS CHECK: Local. This is the release pattern from
ROOMS-RELEASE-RK-LJ (docs/history/contracts/, 10 Oct), applied to one
room. No shared code changes: the hub, front-page band and counts are
content edits on pages that already hold the other eleven rooms.

EXACT CHANGE:
1. escape-rooms/roll-for-initiative/index.html becomes the room:
   play.html's body with an existing live room's head (analytics on,
   indexable, canonical, the draft's meta description for description
   and og:description, og:image the room's scene). Delete play.html.
   teacher.html stays noindex, linked from inside the room as every
   room's is.
2. Remove roll-for-initiative/play.html from check-analytics-loader.py's
   WITHDRAWN registry (the file no longer exists; data only).
3. A hub card: the draft's hub card line and topics line
   (docs/escape-room-drafts/dnd-club-draft.md, "Hub card line and meta
   description"), and the data-stars chip derived by rating.js
   (expected ★★ Core). The hub's ordering by stars places it.
4. A card in the front page's escape-room band.
5. A <url> entry in sitemap.xml.
6. Room counts "eleven" -> "twelve" wherever the site states one: hub
   (description, og:description, lede), front page (band lede, "Open
   all eleven rooms"), CLAUDE.md, canon §11.1 (Roll for Initiative,
   Live 16/10/2026, ★★, Commandant Strictmane; Mrs Rogers credited).
   Find every count by search; do not rely on this list.
7. The credit "Built from a teacher's idea. Thank you, Mrs Rogers."
   stays exactly as built.
8. /updates/: one line under October's New, naming the room the way
   the other rooms are named there.
9. python scripts/check-changed.py before the first push. Merge on
   green with main green. Then check the live URL loads, and record it.
10. Handover entry in docs/handover/home.md; the finished contract
    moves to docs/history/contracts/.

DO NOT TOUCH: any other room's room.js, art or card wording; engine.js,
teacher.js, rating.js, engine.css; the stars key line; variant
libraries and lock banks; the room's own text, locks or credit; the
"three locks, fifteen minutes" copy (true for this room; it changes
with Big School Begins' release); the cloud lane's handover.

SUCCESS CONDITION: /escape-rooms/roll-for-initiative/ loads with its
pictures, playable to a win and a loss at 390 and 1280 px. It has a hub
card showing ★★ in the right star order, and a front-page card. The
sitemap lists it. No page anywhere still says eleven rooms.
check-escape-rooms, test-escape-rating, the escape-room art test and
check-analytics-loader pass, with no 320 px overflow beyond the
allowlisted teacher pages. CI green; merged; live URL checked and
recorded.

STOP IF: The derived stars are not ★★. The draft's meta description or
hub line is missing or over 160 characters. A room count is found that
is not simply "eleven" (say so; do not guess). Any check needs a change
to shared code to pass.

END OF CONTRACT
