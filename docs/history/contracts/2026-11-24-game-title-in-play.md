# GAME-TITLE-IN-PLAY (Project Claude, 24 Nov 2026), verbatim

```text
GAME-TITLE-IN-PLAY (Project Claude, Tue 24 Nov 2026 16:40; checked against main 07b5c7d)
Jon's request 24 Nov 2026: the game's name disappears when play starts on a laptop; agreed order "calc column, then title in play, then Base 60" ("I agree"). BASE-60 ruling 24 Nov 16:28: "Starting closed it fine" (the "Why 60?" panel).
RECOMMENDED: Fable 5.2 (continuing Jon's test), effort high. One shared script on every game page, plus a new check.
LANE: cloud (lane 1, the only MaffsGames cloud session). SEND: now; lane 1 is free (#901 merged as 5552d9d). One PR. Branch from current origin/main. No draft PR.

TASK: On a computer, a game's name stays on screen during play: site-nav.js shows it beside the margin logo whenever the page's own title is not showing. Plus three small BASE-60 items in the first commit.

ROOT CAUSE: Shown: in most game pages the title (<h1>) sits inside the start screen, so it hides with that screen when Start is pressed (e.g. games/scale-factor-scaling/index.html:97, the <h1> inside the menu's .header). Inferred, from a regex survey of the HTML: 70 game pages put the <h1> inside a .screen, 15 outside, 32 have no <h1> the regex found; measure this at run time, do not trust these numbers. Canon has no rule on the title during play. On a phone the space is needed for the fold; on a computer there is room. Separately: 20 roster game pages do not load site-nav.js at all, because they have no a.back-link (shown: boolean-blitz, differentiation-duel, distinctly-average, equatle, estimation-golf, factor-race, fraction-equivalence, index-laws, integration-duel, log-laws, modular-battle, percentage-flip, prime-factorisation, quadratic-factoriser, regression-rumble, split-it, suvat, trig-wars, trig-worms, truth-will-set-you-free; regression-rumble and the-perfect-prank have no roster row).

CLASS CHECK: A bug class: the same shape in about 70 games, and the fix belongs in shared infrastructure already loaded by game pages (schools/assets/site-nav.js, canon §7.5.8). No game's markup changes, beyond apply-site-nav.py writing its tag. The name comes from the one copy of the roster (.claude/rules/game-roster.md, column "Game"), written into each page by the existing apply script and held equal by CI. It cannot be fetched at run time: data/ and .claude/ are not published (_config.yml exclude: data; dot-paths), and data/games.json has no display-name field (its keys: slug, search_phrase, description, keywords). The BASE-60 items are local to that game and to docs.

EXACT CHANGE:
0. First commit (after any claim commit), close-out per AGENTS.md line 62 for #901 BASE-60: in docs/handover/cloud.md, the merge commit 5552d9d, the route merge-pr.py, its last line "main 5552d9d run 45430335219: GREEN", and main's run IDs and conclusions on 5552d9d, read back from the API in this session: check-site 45430335219, pages 45430334260, phone-fit-full 45430335047 (it was still in progress when the BASE-60 session stopped; record its final conclusion; if it failed, STOP). Move docs/handover/contracts/2026-11-24-base-60.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-24-game-title-in-play.md. Keep cloud.md under its size limit by the repo's archive rule.
1. BASE-60 items, in the same first commit or the next:
   a. games/its-just-base-60-bruv/index.html: the "Why 60?" panel (details#why, line 154) starts closed at every size, as canon §7.6.2's house pattern has it (collapsed; opening it is the student's choice). Delete the line that opens it from 1024 px (line 578, "if (window.matchMedia && window.matchMedia('(min-width:1024px)').matches) $('why').open = true;") and correct the comment above it (lines 573-574) and the CSS comment at line 58 ("closed on phones, open from 1024 px"). Nothing else in the page changes.
   b. scripts/verify-its-just-base-60-bruv.py: assert details#why is closed on load at 1280 x 720 and 375 x 667. One plant that must fail: the panel opened on load.
   c. .claude/rules/timer-policy.md, "## No Timer": add **It's Just Base 60, Bruv** (added 24 Nov 2026, contract BASE-60: no clock shown, logged or scored), in the style of the CAST Away entry.
   d. docs/todo.md row BASE60-LIST: add "'Why 60?' starts closed (Jon, 24 Nov 2026, 16:28; GAME-TITLE-IN-PLAY)."
2. Every roster game page loads site-nav.js. scripts/check-site-nav.py static rule 1 becomes: every page with an a.back-link, and every games/<slug>/index.html whose slug has a roster row, loads site-nav.js exactly once. scripts/apply-site-nav.py writes the tag on those pages by its existing placement rule (before stage-exit.js, else before </head>). This adds the margin logo to the 20 pages above wherever it fits, under its existing rules; list them in the PR.
3. The name on the tag. On every games/<slug>/index.html with a roster row, the site-nav.js tag carries data-game-name="<the roster's Game column for that slug>", HTML-escaped (names contain apostrophes, e.g. "But It's Only Half the Size!"). apply-site-nav.py writes it and rewrites it when the roster changes (idempotent: a second run changes nothing). check-site-nav.py's static rule gains: the attribute's decoded value equals the roster name exactly; a roster game page without it fails; a page outside games/ never carries it. The scripts' TAG constant and LOADS pattern accept the attribute. The roster is read by one function in check-site-nav.py, which apply-site-nav.py imports (as it already imports TAG and LOADS).
4. schools/assets/site-nav.js: the name label. Only when the tag has data-game-name:
   - A text element (not a link; aria-hidden="true", since the page's <title> names the game), fixed, top aligned with the logo, starting LOGO.clear px right of the logo. It shows only while the logo shows (same fine-pointer and conflict rules), never without it.
   - It shows only while the page's own title is not showing: hidden when the page's first <h1> is rendered (non-zero box, no ancestor display:none or visibility:hidden), or when any rendered text on the page (excluding the label) equals the name (case-folded, whitespace collapsed).
   - Its width is the measured free margin: from its left edge to the nearest thing the page paints, by the same measure conflict() uses (a fixed box where it is; anything in the flow by its left edge at any height), less LOGO.clear. It wraps to at most 3 lines; if the name needs more, or the free width is under 120 px, it does not show. No width guess, no viewport breakpoint.
   - Look: the body's computed font-family and colour, 15 px, weight 600, line-height 1.25, no background, no new colours or hex values.
   - Re-measured exactly when the logo is (load, resize, after each click, key or touch). Any failure hides it and leaves the page as written.
   - window.MaffsNav gains gameName (the attribute's value, or null). nav.place() also reports why the label is hidden.
   - Update the file's header comment (point 3, the label).
5. scripts/check-site-nav.py --check, in Chromium as it already plays pages:
   - Half the Size (scale-factor-scaling) at 1280 x 720: no label on the start screen (its <h1> shows); after Start, the label shows and reads "But It's Only Half the Size!".
   - Free Daily Pizza (its title stays during play; check this on the page first): no label at any point.
   - The label is hidden at 390 x 844 and on a 768 x 1024 tablet, and on Chart Interrogator and 52-dle (where the logo is hidden or off).
   - The label's box never overlaps anything the page paints, by an independent hit test (elementsFromPoint), at any scroll position.
   - Text contrast of the label against the body background at least 4.5:1, on the light and the dark theme games tested.
   - Plants that must fail (--selftest): a label shown while the <h1> is rendered; a label overlapping the game column; a data-game-name that differs from the roster; a roster game page without site-nav.js.
   Do not add a new always-run line (ALWAYS_BUDGET is full): extend the existing check and its ci-deps.
6. --survey, results in the PR as a table, at 1280 x 720, 1366 x 768 and 1920 x 1080, every roster game page, start screen and first question after Start: logo shown or what blocks it; label shown, hidden because the title shows, or hidden because of no room (with the free width). Give the totals.
7. Canon §7.5.8: a third paragraph, "The game's name during play" (contract GAME-TITLE-IN-PLAY, Jon 24 Nov 2026): the rule in point 4, the roster as the name's source, and that every roster game page loads site-nav.js. Update the "Checked:" paragraph to match.
8. /updates/: one dated line in plain words, e.g. "On a computer, a game's name now stays at the top left while you play."
9. docs/handover/cloud.md entry. Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 when the Gate is green (site-nav.js is a shared path, so phone-fit runs on every game on the PR by itself: do not dispatch it or measure locally in its place). Report its last line.

DO NOT TOUCH:
- Any game's markup, title, header, back link, layout, bank or logic, other than apply-site-nav.py's tag on each page and point 1a.
- The logo's own rules (position, size, clear space, opt-outs on LOGO_OPT_OUT), the back-link relinking and HUBS.
- stage-exit.js, kids-look.js, analytics.js, calculator.js, fold.css and every other shared asset except site-nav.js.
- The roster's content (read it, never edit it). data/games.json.
- Escape rooms, hub pages and parents' guides (no label outside games/).
- Gate files (workflows, scripts/ci-*, ci_shards.py, merge-pr.py) beyond check-site-nav.py's own ci-line and ci-deps header.
- No new collection, no fetch of any file at run time, no listing of BASE-60.

SUCCESS CONDITION:
- On a laptop (1280 x 720), Half the Size shows its name top left after Start, and not on its start screen; on a phone nothing new appears.
- Every roster game page loads site-nav.js once with data-game-name equal to its roster name; check-site-nav.py --static, --check and --selftest pass, with every plant caught.
- The PR carries the survey table with totals, the list of 20 pages that gained the logo, and any page where the roster name and the page's own title differ (report only).
- Base 60's "Why 60?" is closed on load at every size; its verifier passes with the new plant caught; the timer-policy line and the todo note are in.
- #901's close-out is recorded; merged through merge-pr.py on green; the last line reported; cloud.md records this task.

STOP IF:
- Main's phone-fit-full on 5552d9d (run 45430335047) concluded anything but success: report it and stop before any other work.
- The survey shows the label can show during play on fewer than half of the games that lose their title at 1280 x 720 or at 1366 x 768: stop before merging, report the survey with free widths, and wait for Jon. The design would not meet his request.
- Adding site-nav.js to the 20 pages changes anything other than the logo's appearance (a console error, a failing check, a phone-fit or fold change): stop and report which page and why.
- A roster Game cell contains markup, or a roster game page has no roster slug match that can be resolved unambiguously.
- merge-pr.py cannot reach GitHub, or refuses: report its output, do not merge another way.
```
