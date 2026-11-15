# PRINTABLES-PAGE (contract, verbatim)

Saved word for word from Jon's paste of 15 Nov 2026.

```text
PRINTABLES-PAGE (Project Claude, Sun 15 Nov 2026 13:25, re-checked against main d59aecaf at 14:20; Jon 09:52 scope; Jon 13:21 "a higher priority is the printables page though. I'd like that to go live today please"; Jon 13:23 wording "approved")
Recommended: Sonnet, effort medium: one new static page, one footer link applied site-wide by the existing script, one line on /escape-rooms/.
LANE: home (the shared footer, scripts/check-footer.py and apply-footer.py). TIER: Medium (merge on green; Project Claude reviews after merge; Jon checks the live page). START: now; MONOTONIC-CLOCK merged as d59aecaf (#781); carry its close-out (main's check-site and phone-fit-full on d59aecaf, home.md merge line) in the first commit if not already on main; before UNLIST-GRAPH-SKETCHER. One PR. Branch from current origin/main.
MERGE: merge-pr.py on a green Gate.

JON'S RULINGS (verbatim in the PR body):
- 15 Nov 09:52, to "when should the page go live?": "Now, add Core later" (live with the five Tes listings that have public links; the Core rooms and Core bundle are added by a one-line follow-up once Tes publishes them). To "where should it be linked from?": "Escape rooms page, Site footer".
- 15 Nov 13:23: "approved" (to: the page wording in EXACT CHANGE 1, and the /escape-rooms/ and /updates/ lines in 3 and 5).
- Earlier rulings, 6 Nov and 12 Nov 2026: the page is named "Printable packs"; online games and rooms stay free; the free pack links to Tes rather than being hosted on the site; paid packs may be linked from maffsgames.co.uk; printable games and worksheets shown as coming soon; no AI-made posters.

TASK: Publish /printables/, a "Printable packs" page listing the escape-room packs on Tes, linked from the site footer and from /escape-rooms/.

ROOT CAUSE: The packs are on Tes (five public listings, checked 14 Nov 2026) but nothing on maffsgames.co.uk mentions them, so a teacher who finds the site never learns a paper version exists, and a teacher who finds a pack on Tes has no page on the site to come back to.

CLASS CHECK: Local: one new page and two links. The footer link is added the one way the repo allows, through _LINKS in scripts/check-footer.py (which builds CANONICAL) and apply-footer.py, so every page gets it identically; no page is edited by hand for the footer.

EXACT CHANGE:
1. printables/index.html: a static page in the portal's style (canon §7.5: Outfit, white surfaces, navy #1a2744, teal #0d9488, no decorative emoji), the site header/back link and footer as other portal pages have them, title "Printable packs | MaffsGames", a meta description, canonical URL, in the sitemap. Wording verbatim:
   H1: Printable packs
   Every game and escape room on MaffsGames is free to play online, and always will be.
   If you'd rather run a room on paper, as a team race with no screens, we sell printable class packs on Tes for a small charge. The Christmas pack is free, so you can try one before you buy.
   H2: Escape room packs
   Each pack: 6 different sets so teams can't copy, a 15-minute race, a score sheet, hint cards, and an answer key with worked solutions and the common wrong answers.
   One card per item, in this order, each with: the room's name, its star level and grades exactly as /escape-rooms/ shows them (read from that page's chips), its three topics (from the room's own page description), the price, and a link "View on Tes →" (opens in a new tab, rel="noopener"):
     The Christmas Tree Fiasco · free · https://www.tes.com/teaching-resource/christmas-maths-escape-room-ks3-and-gcs-13656567
     The Kiln Disaster · £3 · https://www.tes.com/teaching-resource/kiln-multiples-and-lcm-escape-room-gcse-maths-13656545
     The Comic Caper · £3 · https://www.tes.com/teaching-resource/comic-caper-factors-escape-room-gcse-maths-13658732
     The Library Jam · £3 · https://www.tes.com/teaching-resource/library-jam-decimals-escape-room-gcse-maths-13658744
     Warm-up bundle: Kiln, Comic Caper and Library Jam · £5 · https://www.tes.com/teaching-resource/3-maths-escape-rooms-warm-up-bundle-gcse-13659410
   Each room card also links "Play it free online" to the room's own page on the site.
   H2: Printable games
   Coming soon: loop cards for whole-class starters. The Six Sevens, Bruv deck will be free.
   Closing line: Buying a pack supports the site. The games stay free whether you buy one or not.
2. Footer: add ('/printables/', 'Printable packs') to _LINKS in scripts/check-footer.py, after ('/ugh-stats/', 'Ugh, stats'); run scripts/apply-footer.py so every page carries it; site-footer.css only if the row needs it to fit (it must still fit at 320 px as it does today).
3. /escape-rooms/: one line under the page's first lede (escape-rooms/index.html:27): "Want to run a room on paper? Printable class packs →" linking to /printables/, in the page's existing link style.
4. Analytics: the page's links carry the site's existing section/click attributes so analytics.js records them as section_clicked (as the homepage links do); no new event, nothing new collected.
5. /updates/: one line: "New: <a href="/printables/">Printable packs</a>, paper versions of our escape rooms for whole-class team races. The rooms stay free online." todo: a row PRINTABLES-CORE for adding the three ★★ Core rooms (Car Trap, Roll for Initiative, Prom Budget) and the Core bundle once Tes publishes them, prices as Tes shows them. home.md entry.
DO NOT TOUCH: the rooms and their pages beyond the one /escape-rooms/ line; the Tes listings; data/games.json and the game counts (this is a page, not a game; if a check requires a listing entry for a new page, follow the pattern The 6 P's uses for pages and say so); every other page except through apply-footer.py; Gate files; the approved wording.
SUCCESS CONDITION: maffsgames.co.uk/printables/ is live with the wording verbatim and five working Tes links; every page's footer has "Printable packs" and check-footer passes; /escape-rooms/ links to it; the page passes the site's checks (phone fit at 320/375/390, theme, links, SR-14 content safety) without loosening; in the sitemap; Gate green; merged; main's check-site and phone-fit-full green on the merge commit and reported; home.md and todo updated.
STOP IF: any check would need loosening or an exception list entry for the new page; the footer no longer fits at 320 px; a Tes link does not resolve (report it; do not substitute a search link); the wording would need changing to pass a check (report it; do not reword).
```
