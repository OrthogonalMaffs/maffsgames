SITE-BAR-PILOT (Project Claude, Wed 25 Nov 2026 17:50; checked against main c4fbeff)
Jon, 25 Nov 2026, 17:14-17:31: a logo top left on every game, in play and after, that goes home; "I'd rather have a standard nav bar across the site ... it stops the '7 games working like this, but 29 games work a different way'"; "yes a small pilot works for me" (17:31, agreeing the compact phone bar and pinning on big screens as proposed). This knowingly replaces canon §7.5.8's margin-only logo (SITE-NAV, 21 Nov) for the pilot pages; the rest of the site keeps today's behaviour until a sweep Jon approves after playing the pilot.
RECOMMENDED: Claude Code, Opus 5.5, effort high. Shared navigation code on every page; three pages switched; the other 114 must not change.
LANE: home. SEND: now (#913 merged; the home lane is free). Lane 2 is on LIKE-TERMS-PLUS (games/like-terms-collector/, its verifier, updates/index.html, docs/handover/cloud.md): you share updates/index.html only; merge main in before merging.
TIER: Shared. Stop at Gate green for Project Claude's review and Jon's "merge" (AGENTS.md:60).

TASK: Build one shared site bar (logo home, back link to the hub, game name on big screens) and switch three pilot games to it on every screen, with every other page unchanged.

ROOT CAUSE: Shown, main c4fbeff: there is no standard exit. Of 117 game pages, 97 have a.back-link and 20 none; 19 also load stage-exit.js with its own home link; 41 have a bare results link <a href="/">← Back to Games</a> that site-nav.js never sends to the hub (it rewrites only a.back-link: schools/assets/site-nav.js:126 relink), usually at the bottom of the results screen (spot-the-muppet/index.html:242); back-link occurrences per page range 0 to 6. The margin logo (site-nav.js:146-341) shows only where nothing paints in the left margin, so every full-width-header game (35, per the GAME-TITLE-IN-PLAY survey, docs/history/handover-cloud-archive.md:80) shows no logo and no name in play.

CLASS CHECK: A class (one fault shape across 117 pages, in shared infrastructure), so the fix is at the architectural layer: one bar owned by site-nav.js, a static slot written by scripts/apply-site-nav.py, held by scripts/check-site-nav.py. This pilot builds that layer and switches three pages; the sweep of the rest is a later contract.

PILOT PAGES:
- games/spot-the-muppet: light; full-width header; back links :178 and :191; bare results link :242; a transient top banner .muppet-banner (position: fixed, z-index 1002, :94).
- games/better-value: dark; full-width header (:38); phone header rule (:149-154, its .back-link at :152); back links :222 and :236; bare results link :294; a full-screen .method-overlay (position: fixed, z-index 100, :180).
- games/its-just-base-60-bruv: loads stage-exit.js; back link :175.

EXACT CHANGE:
0. First commit: save this contract verbatim as docs/handover/contracts/2026-11-25-site-bar-pilot.md (and any close-out AGENTS.md requires of this lane).
1. The slot (scripts/apply-site-nav.py, for the pilot pages only, from a list SITE_BAR_PAGES in scripts/check-site-nav.py): the first child of <body> is
   <nav class="site-bar" data-site-bar aria-label="Site"><a class="site-bar-fallback" href="/">← MaffsGames</a></nav>
   and <head> links one new stylesheet, schools/assets/site-bar.css, which reserves the bar's height before any script runs (no layout jump): 48 px on a fine pointer ((hover: hover) and (pointer: fine)), 36 px otherwise.
2. The bar (schools/assets/site-nav.js): on a page with [data-site-bar], replace its contents with, left to right:
   - the logo (the existing favicon.svg mark, as now), a link to "/", aria-label "MaffsGames home";
   - the back link (class site-bar-back, NOT back-link): MaffsNav.backHref and "← Back to <backLabel>" when there is a hub (the existing HUBS, sessionStorage and /class/ rules, unchanged), otherwise "/" and "← Back to Games"; on a coarse pointer the short form (MaffsNav.shortLabel, or "← Games");
   - on a fine pointer only, the game's name from the tag's data-game-name, plain text, aria-hidden, as the margin label is now.
   Fine pointer: position: sticky; top: 0, so it stays at every scroll position, with the body's computed background colour behind it and a z-index above the page's normal content but below the page's own transient overlays (the two named above stay on top while they show). Coarse pointer: in the flow, not sticky. Colours from the page (body's computed colour and background); logo, link and name at 4.5:1 or better on all three pages, light and dark. On a page with the slot, the margin logo and margin name are not created. On a page without the slot, site-nav.js behaves exactly as now.
   Fail-safe: if anything throws, the fallback link stays.
3. The pilot pages: remove every a.back-link and every bare "← Back to Games" link (spot-the-muppet :178, :191, :242; better-value :222, :236, :294, and its now-unused .back-link rules at :39-40 and :152); the bar is their only back link. Each page's own header and HUD (score, stage, level, Aa) stay, below the bar. No game hides the bar on any screen (start, play, results); only the two transient overlays named above may cover it while they show.
4. stage-exit.js (its-just-base-60-bruv): on a page with [data-site-bar], create no home link (neither the HUD copy nor the header-row link) and do not require a.back-link; the "← Stages" button appears exactly where it does now and works as now. On the other 18 stage-exit pages, nothing changes.
5. Checks (scripts/check-site-nav.py; check-site.py's static part where the existing rules live):
   - Static: each SITE_BAR_PAGES page has exactly one [data-site-bar], first in <body>, the site-bar.css link once, and no a.back-link and no other link whose text starts "← Back to"; every other page as now.
   - Chromium, each pilot page at 1920x1080, 1280x720, 390x844 and 320x568, on start, play and results: the bar is at the top of the viewport; the logo goes to "/"; the back link goes to the right place directly, from a hub (/essentials/), and reloaded; on a fine pointer, after scrolling to the bottom, the bar is still at the top; at scroll 0, with no transient overlay showing, nothing the page paints is under the bar (independent hit test); contrast 4.5:1; base-60's "← Stages" works in play.
   - Plants (each must FAIL): a pilot page with a second back link; a pilot page hiding the bar on its results screen; site-nav.js drawing the margin logo on a pilot page; the bar not sticky on a fine pointer.
   - All existing site-nav, stage-exit and per-game checks still pass for the other 114 pages, unchanged.
6. Phone fit: the three pages pass the Gate's phone fit (it runs on the PR by itself; do not dispatch it) at 320x568 and 375x667, normal and Aa. If a page fails because of the bar's 36 px, fix that page's own layout (spacing, its own header) and report the before and after; never hide or shrink the bar below 36 px to pass.
7. Canon §7.5.8: one added paragraph: "Site bar pilot (SITE-BAR-PILOT, Jon 25 Nov 2026): on the pages in check-site-nav.py's SITE_BAR_PAGES the margin logo and name are replaced by one site bar (logo home, back link to the hub, name on a fine pointer), pinned on a fine pointer, compact and in the flow on a coarse one, on every screen. The rest of the site keeps the rule above until the sweep." Nothing else in canon.
8. /updates/: one dated line, plain words: "Spot the Muppet, Better Value and It's Just Base 60, Bruv: a new bar at the top with the MaffsGames logo and a way back, on every screen. If you like it, it comes to every game." docs/handover/home.md entry with PR, run IDs, screenshots referenced in the PR (each pilot page at 1920x1080 and 390x844 on start, play and results) and the phone-fit numbers.
9. At Gate green: stop; report the head SHA, the Gate run ID and the phone-fit run ID; wait for Jon's "merge". Then python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line.

DO NOT TOUCH:
- Every page outside SITE_BAR_PAGES: no slot, no stylesheet, no markup change; site-nav.js and stage-exit.js behave on them exactly as on main (proved by the existing checks).
- site-nav.js's hub rules (HUBS, sessionStorage, /class/ via MaffsKids), data-game-name and apply-site-nav.py's existing tag; the logo file (favicon.svg; check-logo.py's registered copies).
- The pilot games' questions, marking, scoring, boards, analytics, themes, art, overlays, and their own headers beyond removing back links (and any layout fix step 6 requires).
- schools/assets/ beyond site-nav.js, stage-exit.js and the new site-bar.css; .github/workflows/; the roster; every other game; canon beyond step 7.

SUCCESS CONDITION:
- On the three pilot pages, on every screen and at all four sizes: one bar at the top, logo home, back link to the right hub, name on big screens; pinned on a fine pointer, compact and in the flow on a phone; no other back link; base-60's "← Stages" works.
- Every other page unchanged; all existing checks pass; the new checks pass and every plant is caught; phone fit green at 320x568 and 375x667, normal and Aa.
- Gate green, Project Claude's review, then merged through merge-pr.py after Jon's "merge"; last line reported; home.md records it.

STOP IF:
- A pilot page cannot pass phone fit with the bar without a change beyond that page's own layout: report the measurement.
- stage-exit.js cannot drop its home link on a bar page without changing the other 18 stage-exit pages: report why.
- Any existing check fails on a page outside SITE_BAR_PAGES.
- Making the bar sticky on a fine pointer overlaps a pilot page's own fixed or sticky element other than the two named overlays (found by the hit test): report it; do not remove the page's element.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
