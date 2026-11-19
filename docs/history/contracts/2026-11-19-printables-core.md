PRINTABLES-CORE — home lane (Claude Code, terminal). Tier: Medium (merge on green). Send: now, 19 Nov 2026 before Jon leaves for work; it runs unattended.
Recommended: Sonnet, medium effort — a content addition to one page, with every value given below.

TASK: List the seven ★★ Core escape-room packs and the three Core bundles on /printables/, with Tes links and prices, and close backlog rows PRINTABLES-CORE and CORE-BUNDLES-2.

ROOT CAUSE: /printables/ (printables/index.html) lists only The Christmas Tree Fiasco, the three ★ Warm-up rooms and the Warm-up bundle. All seven ★★ Core rooms and three Core bundles are now live on Tes (Jon sent the links on 18 Nov 2026, 23:27 and 23:48; Project Claude checked each Tes page's title and price at 23:50), so a teacher on the site cannot find them. docs/todo.md:396 (PRINTABLES-CORE) has waited for exactly these links; docs/todo.md:262 (CORE-BUNDLES-2) is Jon's task to list the bundles on Tes, now done.

CLASS CHECK: Not a bug class. One page is missing content that it was always meant to gain once Tes published the listings. There is no shared code or repeated defect, so the change is local to printables/index.html, following the page's existing card pattern exactly.

EXACT CHANGE:
0. FIRST COMMIT, close-out of #829 DASHBOARD-FIXES (merge commit e4ac609): in docs/handover/home.md, replace the DASHBOARD-FIXES entry's "- MERGED: pending." (currently :29) with the MERGED line in the same form as the DASHBOARD-GLANCE entry's. It records merge-pr.py's last line from #829's report and main's runs on e4ac609 (check-site and phone-fit-full, plus the pages build if any). Confirm every run ID from the GitHub API; check-site is probably 44397107631, per commit d474105. If a run ID cannot be confirmed, record what you could confirm, say which could not be, and carry on. Move docs/handover/contracts/2026-11-18-dashboard-fixes.md to docs/history/contracts/. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-19-printables-core.md.
1. printables/index.html, inside the first <div class="packs"> (the "Escape room packs" section), after the Warm-up bundle's </article> (currently :167) and before that div's </div>, add ten <article class="pack"> cards. Build each exactly like the existing cards (for example The Kiln Disaster, :126–:136):
   - the ★★ Core chip, copied verbatim from The Christmas Tree Fiasco's card (:117): <span class="chip" data-stars="2">…★★ Core &middot; grades 4–5…</span>;
   - h3, topics (rooms only), price;
   - links: "View on Tes &rarr;" (target="_blank" rel="noopener", data-mfg-item="tes-<id>"), and for rooms only "Play it free online" (data-mfg-item="play-<slug>").
   Room names come from /escape-rooms/'s cards, and topics from each room's own meta description, joined with " &middot; ".
   Seven rooms, in the order /escape-rooms/ lists them:
   | slug | h3 | topics | price | Tes URL |
   | hamster-heist | The Great Hamster Heist | Circumference &middot; Bounds &middot; Gradient | £3 | https://www.tes.com/teaching-resource/great-hamster-heist-circles-bounds-and-rates-escape-room-gcse-maths-13669800 |
   | pe-shed-rebellion | The P.E. Store Rebellion | Sector area &middot; Inverse proportion &middot; Sequences | £3 | https://www.tes.com/teaching-resource/p-e-store-rebellion-sectors-proportion-and-sequences-escape-room-gcse-maths-13669807 |
   | heatwave-mutiny | The Heatwave Mutiny | LCM &middot; Surface area to volume &middot; Inequalities | £3 | https://www.tes.com/teaching-resource/heatwave-mutiny-lcm-cubes-and-inequalities-escape-room-gcse-maths-13669810 |
   | prom-budget | The Prom Budget Embezzlement | Reverse percentages &middot; Compound growth &middot; Venn diagrams | £3 | https://www.tes.com/teaching-resource/prom-budget-percentages-and-venn-escape-room-gcse-maths-13662093 |
   | canteen-hack | The Canteen Menu Hack | Averages &middot; Simultaneous equations &middot; Fractions of an amount | £3 | https://www.tes.com/teaching-resource/canteen-menu-hack-means-simultaneous-equations-and-fractions-escape-room-gcse-maths-13671886 |
   | car-trap | The Headteacher&rsquo;s Car Trap | Error intervals &middot; Arc length &middot; Quadratics | £3 | https://www.tes.com/teaching-resource/car-trap-bounds-and-arc-length-escape-room-gcse-maths-13662073 |
   | roll-for-initiative | Roll for Initiative | Probability &middot; Scale drawings &middot; Area of a circle | £3 | https://www.tes.com/teaching-resource/roll-for-initiative-probability-and-circles-escape-room-gcse-math-13662087 |
   The order above is /escape-rooms/'s order on main d20fad0 (19 Nov). If the hub's order has changed, use the hub's order. The topics above are Project Claude's reading of each room's meta description; re-read each and use the description's own words if any differ.
   Then three bundles (no topics line, no play link):
   | id | h3 | price | Tes URL |
   | tes-core-bundle | Core bundle: Car Trap, Roll for Initiative and Prom Budget | £5 | https://www.tes.com/teaching-resource/3-maths-escape-rooms-core-bundle-gcse-car-trap-roll-for-initiative-prom-budget-13662115 |
   | tes-core-bundle-2 | Core bundle 2: Hamster Heist, P.E. Store, Heatwave and Canteen | £6.50 | https://www.tes.com/teaching-resource/4-maths-escape-rooms-core-bundle-2-gcse-hamster-heist-p-e-store-heatwave-canteen-13672017 |
   | tes-core-collection | The complete Core collection: all seven Core rooms | £10 | https://www.tes.com/teaching-resource/7-maths-escape-rooms-the-complete-core-collection-gcse-13672025 |
   Room data-mfg-item ids: tes-<slug> and play-<slug>, using the slug column.
2. /updates/: add one dated line (19 Nov 2026), in plain words, in the page's existing style. For example: "Printable packs: all seven Core escape rooms and three Core bundles are now listed, with links to play each room free online." (AGENTS.md: a PR that changes what a teacher sees adds its line.)
3. docs/todo.md: PRINTABLES-CORE (:396) and CORE-BUNDLES-2 (:262) are done; move both word for word to docs/history/todo-done.md with a done note (AGENTS.md: rows owe nothing more). todo.md is about 28 bytes under its 150 KiB cap, so this change may only shrink it.
4. Record this task in docs/handover/home.md (a new entry, within its archiving limit). When it merges, the next home contract carries this one's close-out.

DO NOT TOUCH:
- The existing cards on /printables/ (Christmas, Warm-up rooms, Warm-up bundle, loop cards): their order, wording, prices and links.
- The page's intro, CSS, nav and footer; the "Printable games" section.
- Any escape room page, /escape-rooms/, the packs or tools/pack-generator/.
- docs/handover/cloud.md (the cloud lane owns it).
- The DASHBOARD-PERCENT-CELLS todo row and docs/apps-script-endpoint.js: the percent check waits for Jon.
- Prices or titles not given above: never guess a price. Use each card's price exactly as the table gives it.
- Personal or identifying details beyond "Jon".

SUCCESS CONDITION:
- /printables/ shows 10 new cards after the Warm-up bundle: seven rooms (chip, name, topics, price, both links) and three bundles (chip, name, price, Tes link), each Tes link exactly as above.
- Every play link resolves to a live room: the existing site checks pass, and each /escape-rooms/<slug>/ exists in the repo.
- check-footer.py, check-publish-scope.py, check-content-safety.py and the full Gate are green; the phone-fit measurement passes for /printables/ at 320px if the Gate measures it.
- The /updates/ line is present; PRINTABLES-CORE and CORE-BUNDLES-2 are in docs/history/todo-done.md and gone from todo.md; todo.md is smaller than before.
- The first commit holds #829's close-out, with its run IDs confirmed from the API.
- Merged with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, and its last line is reported. home.md is current, and this task's close-out is recorded as owed.

STOP IF:
- Any of the seven rooms is not on /escape-rooms/, or its page is not live in the repo.
- A room's h3 on /escape-rooms/ or its meta description differs from the table so much that the topics no longer describe the room. Small wording differences: use the room's own words and note them in the PR.
- A Gate check fails because of this page and the fix would touch anything in DO NOT TOUCH.
- todo.md would grow past its cap.
- Main is red before you start.
