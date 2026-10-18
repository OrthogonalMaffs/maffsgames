CONTRACT: BSB-RELEASE (Project Claude for Jon, 18 Oct 2026, 10:45). HOME LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Release Big School Begins: the room becomes its own live, indexed
page with its Starter hub and front-page cards, sitemap entry, room
counts, and site copy that stays true now that one room has four locks
and twenty minutes; and replace one narration sentence in its win.

ROOT CAUSE: The room is built (#425), labelled (#430, Starter), in the
register (#427), shows coordinates as (x, y) (#432) and has its art
(#433). Jon play-tested it (17 and 18 Oct). It still sits behind a
noindex holding page. The hub and front page state "three locks a room"
and "fifteen minutes", which become false when it ships. One sentence
in the win slot is drafted narration Jon wants replaced (18 Oct).

CLASS CHECK: Local: the release pattern from DND-ROOM-RELEASE (16 Oct),
applied to one room, plus a copy change Jon ruled on 16 Oct ("three or
four locks, 15 to 20 minutes") and a one-sentence text change in one
room. No shared code changes: the labelled card format and its check
already exist (#430).

EXACT CHANGE:
1. big-school-begins/room.js, win slot only: the sentence
   "...and you all sit down at it: William too, between two people he
   hadn't met this morning, eating and, for the first time today,
   talking."
   becomes
   "...and you all sit down at it: William too, between two people he
   hadn't met this morning, and he hasn't stopped talking."
   Entities as for every slot (canon §11.3). Nothing else in the room
   changes.
2. escape-rooms/big-school-begins/index.html becomes the room:
   play.html's body with an existing live room's head (analytics on,
   indexable, canonical, og:image the room's scene). Meta description
   and og:description, word for word from the draft
   (docs/escape-room-drafts/big-school-begins-draft.md, "Hub card line
   and meta description"): "A 20-minute maths escape room. It's
   transition day at St Martha's: read the map, follow the librarian,
   collect William. Coordinates, turns, time and money." Delete
   play.html. teacher.html stays noindex, linked from inside the room.
3. Remove big-school-begins/play.html from check-analytics-loader.py's
   WITHDRAWN registry (data only).
4. Hub card: the draft's hub line ("It's transition day, the school is
   enormous, and your group has four stops to find before lunch,
   without losing anyone on the way.") and topics line ("Coordinates ·
   Turns · Time · Money"), with the Starter label chip in the format
   check-escape-rooms.py expects for a labelled room (#430), not stars.
   It sits in the hub's easiest-first order by its derived rating
   (★ Warm-up).
5. A card in the front page's escape-room band, same chip, same order
   rule.
6. A <url> entry in sitemap.xml.
7. Room counts "twelve" -> "thirteen" wherever the site states one: hub
   (description, og:description, lede), front page (band lede),
   CLAUDE.md, canon §11.1 (Big School Begins, Live 18/10/2026, Starter,
   no antagonist; Daisy Reddington, William Trembles, Mrs Barb Phile).
   Find every count by search; do not rely on this list.
8. Copy (Jon's ruling, 16 Oct): every site-wide statement that rooms
   have three locks or take fifteen minutes becomes "three or four
   locks" and "15 to 20 minutes" (or "fifteen to twenty minutes" where
   the page spells numbers), keeping each sentence's sense. Known
   places: hub lines 6, 9, 26, 27 and the FAQ "Is fifteen minutes
   right?" (40); front page lines 7, 11, 17 ("15-minute escape rooms"),
   777 ("under 15 minutes each"), 784-785. Find every one by search.
   A single room's own card or text stating its own time stays as it
   is. List every change, before and after, in the PR.
9. /updates/: one line under October's New, naming the room the way
   the other rooms are named there.
10. python scripts/check-changed.py before opening the PR. Merge on
    green with main green; watch main's run; then check the live URL
    loads, the hub card shows Starter, and the sitemap lists it.
    Remove the worktree with scripts/end-task.py.
11. Handover in docs/handover/home.md; this contract and BSB-ART move
    to docs/history/contracts/.

DO NOT TOUCH: the room's text except step 1's sentence; its locks,
variants, label and art; any other room's room.js, art or card wording
(except a count or the copy in step 8); engine.js, teacher.js,
rating.js, engine.css; the stars key line; the cloud lane's handover.

SUCCESS CONDITION: The win reads with step 1's sentence and nothing else
in the room has changed. /escape-rooms/big-school-begins/ loads with
its pictures, playable to a win and a time-out at 390 and 1280 px. Its
hub and front-page cards show the Starter chip in easiest-first order,
and check-escape-rooms.py now checks a real labelled card (not only the
planted fault). The sitemap lists it. No page says twelve rooms, and no
site-wide line says every room has three locks or takes fifteen
minutes. check-escape-rooms, test-escape-rating, test-escape-art and
check-analytics-loader pass. CI green; merged; live URL checked;
worktree removed; handover recorded.

STOP IF: Step 1's original sentence is not found word for word (quote
what is there; do not reword). The meta description or hub line is
missing from the draft or over 160 characters. A room count is found
that is not simply "twelve" (say so; do not guess). A copy line can't
take "three or four locks" or "15 to 20 minutes" without changing what
it means (quote it; do not reword freely). Any student-facing text
would name a year group (SR-11). Any check needs a change to shared
code to pass.

END OF CONTRACT
