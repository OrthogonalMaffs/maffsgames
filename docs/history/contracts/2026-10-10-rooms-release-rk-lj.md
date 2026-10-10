# ROOMS-RELEASE-RK-LJ (Jon, 10 Oct 2026, 22:45)

Start condition: ROOM-ART-RK-LJ (claude/contract-room-art-rk-lj-2026-10-10.md) merged and main green. Under the standing rule (7 Oct), start it then without asking.

```
MODEL: sonnet · effort: medium · LANE: home

TASK: Release The Rightful King and The Library Jam: each room becomes its own live page, with cards, stars, sitemap entries and counts, as Car Trap was released.

ROOT CAUSE: Both rooms are built (#257, #262), carry their art (ROOM-ART-RK-LJ), and Jon has play-tested both (10 Oct, 22:44: "both have been play tested, so lets just release"). Each still sits behind its noindex holding page with no hub card.

CLASS CHECK: Local, twice over. This is the release pattern CAR-TRAP-RELEASE set (docs/handover/contracts/2026-10-10-car-trap-release.md), applied to two rooms. No shared code changes; the hub, front-page band and counts are content edits on pages that already hold the other nine rooms.

EXACT CHANGE, for each room (rightful-king, library-jam):
1. escape-rooms/<slug>/index.html becomes the room: play.html's body with prom-budget's head (analytics on, indexable, canonical, the draft's meta description for description and og:description, og:image the room's scene). Delete play.html. teacher.html stays noindex, linked from inside the room as every room's is.
2. A hub card: the draft's hub card line, its topic chips, and the `data-stars` chip derived by rating.js (Rightful King ★★★, Library Jam ★). The hub's own ordering by stars places them.
3. A card in the front page's escape-room band.
4. A <url> entry in sitemap.xml for each room.
5. Counts "nine" -> "eleven" wherever the site states a room count: the hub (description, og:description, lede), the front page (band lede, "Open all nine rooms"), CLAUDE.md, canon §11.1 (both rooms Live 10/10 with their stars and characters: Mr Brian Narry; Mrs Barb Phile, "Bibby"). Find every count by search; do not rely on this list.
6. The it-vengeance URL keeps redirecting to rightful-king; check it still resolves after play.html is gone.
7. /updates/: one line each under October's New, naming each room the way the Essentials section and the stars key name things.
8. Handover entry in docs/handover/home.md; finished contracts move to docs/history/contracts/.

DO NOT TOUCH: Any other room's room.js, art or card wording; engine.js, teacher.js, rating.js, engine.css; the stars key line; the variant libraries and lock banks; the cloud lane's handover.

SUCCESS CONDITION: Both rooms load at /escape-rooms/rightful-king/ and /escape-rooms/library-jam/, with their pictures, playable to a win and a loss. Each has a hub card with the right stars, sits in the right star order, and appears on the front-page band. The sitemap lists both. No page anywhere still says nine rooms. check-escape-rooms, test-escape-rating and the escape-room art test pass, with no 320 px overflow beyond the allowlisted teacher pages (§1.37). CI green. Merged. Then check on the live site that both URLs load, and record it in the handover.

STOP IF: Either room's derived stars differ from ★★★ (Rightful King) or ★ (Library Jam). The draft's meta description or hub line is missing or over 160 characters. A count of rooms is found that is not simply "nine" (say so; do not guess). The it-vengeance redirect breaks. Any check needs a change to shared code to pass.
```
