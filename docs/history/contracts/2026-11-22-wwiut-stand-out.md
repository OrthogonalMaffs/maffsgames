WWIUT-STAND-OUT. Home lane. Tier: Medium (a highlighted portal strip and a redesign of the section's hub and pages): stop at Gate green, report with screenshots, and wait for Project Claude's review and Jon's look and "merge". From Project Claude; Jon, 22 Nov 2026, 19:59 ("random link to itself at the bottom, and is not linked anywhere on the home screen?"), 20:01 ("if it has it's own strip it needs to stand out. We want a highlight as it's new"), 20:02 ("the page is SUPER boring, how do we make it stand out"), 20:04 ("just do what you can for now": route tiles first, and the key sum on every job card; his humour lines and job pictures come later).
Recommended: Claude Code, Opus, high effort. A portal strip with a generalised badge expiry, a generator redesign, 14 new checked headline sums.

TASK: (1) Give "When will I use this?" its own highlighted strip on the home page, with a New flag that expires like the others; (2) make the section stand out: lead the hub with big coloured route tiles ("Pick your course"), then a grid of all 14 jobs, each showing its key sum, then the topics; colour each route consistently across the section; (3) remove the hub's link to itself.

ROOT CAUSE: #883 (2710eed) linked the section from the portal as a second button inside the parent guides strip (index.html:931), headed "Help your child with maths", so a student or teacher scanning for themselves doesn't see it. scripts/build-uses.py:184 writes "When will I use this? · MaffsGames home" on every page, the hub included, where the first link points at itself. The pages (build-uses.py) are plain white cards in topic-first order. FE students think in their course (route) first, and a card shows no maths until it's opened, so nothing pulls a student in (Jon: "SUPER boring"). The parent strip's New flag expiry (index.html:3307-3313) is hard-wired to #parFlag, so a second strip can't reuse it without copying it.

CLASS CHECK: The expiry is shared portal behaviour keyed to one id: generalise it so every strip flag with data-badge-date expires on BADGE_DAYS (:3259), rather than copying it. The section's look is generated from one data file by one script: route colours and headline sums live in data/uses.json, written once, used on every page, checked by check-uses.py. Nothing is hand-edited per page.

EXACT CHANGE:
1. First commit: the standing close-out for WHEN-WILL-I-USE-THIS (#883, merged as 2710eed; record main's run IDs from its merge): MERGED line in home.md, contract to docs/history/contracts/. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-22-wwiut-stand-out.md.
2. Portal strip (index.html), directly ABOVE the parent guides strip (:918-932):
   - navy background (var(--navy), #1a2744) with white text, the same shape and spacing as .par-strip;
   - a teal "New" flag (the .par-flag look) with data-badge-date="2026-11-22";
   - h2 "When will I use this?" and the lede "Real jobs that use the maths you practise, with worked examples.";
   - chips styled for the dark background: "14 real jobs", "Worked examples", "Sources you can check";
   - a teal button "See the jobs" to when-will-i-use-this/;
   - data-mfg-section="when-will-i-use-this" and data-mfg-item="open-wwiut", for the portal's existing anonymous click count (already disclosed on the privacy page). No new data collection.
   It takes part in compact mode as the parents strip does (cmp class; data-cmp-hide on lede and chips). Remove the second button from the parents strip (:931). The New-flag expiry (:3307-3313) handles every strip flag with data-badge-date, not #parFlag alone; the parents flag (2026-09-29) behaves as now.
3. data/uses.json:
   - each route gets a colour: one distinct, saturated colour per route, all 15, white text on it at 4.5:1 or better, none the same as the portal's teal;
   - each scenario gets a "headline" sum, exactly as follows (recomputed by Project Claude, 22 Nov):
     - bricklayer "0.3 ÷ 6 = 0.05 m³ per part"
     - hairdresser "40 × 2 = 80 g of developer"
     - hospital-nurse "125 ÷ 250 × 5 = 2.5 ml"
     - plumber "£350 × 1.2 = £420"
     - electrician "5.4 ÷ 230 × 100 = 2.3%"
     - baker "0.7 × 500 = 350 g of water"
     - jeweller "4 × 0.375 = 1.5 g of gold"
     - painter-decorator "64 ÷ 16 = 4 litres"
     - groundsperson "2 × (100 + 64) = 328 m of line"
     - farmer "3 × 150 = 450 kg"
     - practice-nurse "816 ÷ 6 = 136"
     - health-visitor "100 − 91 = 9 in 100 weigh more"
     - ecologist "4 × 1500 = 6000 orchids"
     - meteorologist "9.1 − 8.3 = 0.8 °C warmer"
4. build-uses.py, the hub, in this order:
   (a) the header ("When will I use this?" and its line);
   (b) "Pick your course": big tiles, one per route that has scenarios, filled with the route's colour, with the route name in white and its jobs listed, the whole tile a link to the route page;
   (c) "The jobs": a grid of all 14 job cards, each with the job name, a band or dot in its route's colour, the headline sum in KaTeX (large: the sum is the point), and "How it works →" to the scenario on its topic page (an anchor per scenario);
   (d) "By maths topic": the 4 topic cards as now.
   Topic and route pages: each scenario card carries its route's colour (band or chip) and its headline sum above the text; route pages use their colour in the header. The hub's foot line drops its self-link (keep "MaffsGames home"); the other pages keep both. No emoji; Outfit and KaTeX; portal palette plus the route colours. Mobile first: tiles stack on phones, two or more across on laptops.
5. check-uses.py, extended: every headline's sum recomputes as the steps do (within half a unit of its last decimal place); every route has a colour that meets 4.5:1 with white, and the colours are distinct; every job card's anchor exists on its topic page; no page scrolls sideways at 320 or 390 px, in normal or Aa; text contrast on every coloured tile and card meets 4.5:1. Plants: a wrong headline (2.5 ml as 25 ml), a route colour failing 4.5:1, a broken anchor; and in the portal check, the expiry made to ignore the new flag. Each caught.
6. /updates/: one dated line, e.g. "When will I use this?" now has its own spot on the home page, with jobs grouped by course and the maths on every card.
7. Stop at Gate green. Proof in the PR body: screenshots at 375x667 and 1366x768 of the portal strip, the hub, and the Construction route page. Wait for Project Claude's review and Jon's look and "merge"; then merge via scripts/merge-pr.py; the close-out rides on the home lane's next contract.

DO NOT TOUCH: The 14 scenarios' text, steps and sources; the parents strip's text, look and flag date; other portal sections, the game grid, filters and search; shared assets (site-nav.js included, except a new HUBS line if check-site-nav.py requires one for a new page, labelled as the others); Gate files; games/expectation-station/ and docs/handover/cloud.md (the cloud lane's EXPECTATION-STATION-LINES is in flight).

SUCCESS CONDITION: The home page shows a navy "When will I use this?" strip with a New flag (expiring on the parents' rule) above the parent guides, which have their one button again. The hub opens with coloured course tiles, then 14 job cards each showing a checked sum, then the topics. Route colours carry through every page. The hub no longer links to itself. check-uses.py passes with every plant caught. CI is green; stopped for review and Jon's look.

STOP IF: A headline sum fails the check as written (report it; don't change it). No set of 15 distinct colours meets 4.5:1 with white without clashing with the portal's teal (report the closest set). The portal's phone-fit or compact-mode checks fail and the fix would change another section. The expiry can't be generalised without changing how a game card's New badge works. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).
