MAFFSCARDS-START-ART (Project Claude, Wed 25 Nov 2026 22:25; checked against main 10aabbc)
Jon, 25 Nov 2026, 21:28-21:32: start art for MaffsCards, three cards "popping up over the name of the game", no hand, the tops showing; three very strong cards: 96, 1 and 89, in that order left to right ("I agree with your 3, 96,1 and 89 please"). Measured by Project Claude against cards.json (main deck): each of the three beats all 31 other main-deck cards in one category with no ties: 96 on sum of factors (252), 1 on superpowers (5), 89 on largest prime factor (89).
RECOMMENDED: Claude Code, Opus 5.5, effort medium. One page's start screen and one verifier unit; the numbers must be right.
LANE: cloud, lane 2. SEND: now (ANNOUNCE-STRIP merged; lane 2 is free). First commit closes out ANNOUNCE-STRIP (#915, #920) per AGENTS.md:62. The home lane is on DAILY-DEAL (#919, branch claude/daily-deal), which also edits games/maffscards/index.html (the menu's "Today's deal" panel and the daily results) and scripts/verify-maffscards.py: build now from main, but do NOT merge until #919 is on main; then merge main in (keep every line of #919), re-run the Gate, and merge.
TIER: Medium (merge on green, after #919).

TASK: Put three MaffsCards (96, 1, 89) fanned behind the game's title on its start screen, drawn by the page from the real card data, so the title has a picture.

ROOT CAUSE: A feature (and the start picture in the personality rule Jon is still to rule on). Shown: the start screen's title block is games/maffscards/index.html:261 (<div class="header"><h1>MaffsCards</h1><div class="sub">...</div></div>); the game draws its cards from cards.json in its own style (cardHtml: .mc-top with .mc-num and .mc-nick). No start art exists.

CLASS CHECK: Local: one game's start screen. It uses the game's own card style and data, never a generated image (a generator garbles digits; every number on the site must be right).

EXACT CHANGE:
0. First commit: ANNOUNCE-STRIP's close-out (#915 b3d9471, #920 4b89692; contract to docs/history/contracts/), then save this contract verbatim as docs/handover/contracts/2026-11-25-maffscards-start-art.md.
1. The art (games/maffscards/index.html, start screen only): three card tops fanned behind and above the title block at :261, rising out from behind it: 96 left (tilted about 14 degrees anticlockwise), 1 centre (upright), 89 right (tilted about 14 degrees clockwise). Each shows its number large and its nickname, in the game's own card style (white card, the deck's number and nickname styling): 96 "The Factor Factory", 1 "Technically Everything", 89 "Fibonacci's Lanky Prime", taken from cards.json's values (verbatim). Only the tops show; the title block sits in front, solid, with the title and subtitle at 4.5:1 or better. HTML/CSS or inline SVG; decorative, aria-hidden. No hand. Static, or one gentle rise into place on load that is off under prefers-reduced-motion; nothing loops.
2. Fit: the start screen still fits at 320x568 and 375x667, normal and Aa, and 1280x720: everything above the fold that is above it today stays above it (in particular, after #919, the "Today's deal" panel's button, and the Deal the cards button where it is above the fold now). On a phone the art may be shorter (e.g. a smaller fan); it is never hidden. Measure before and after.
3. Verifier (scripts/verify-maffscards.py, one new SHARD unit "art"; existing units and plants unchanged): the three cards' numbers, order and nicknames on the page equal cards.json's; recomputed from cards.json, each of 96, 1 and 89 beats all 31 other main-deck cards in its category (sum of factors, superpowers, largest prime factor) with no ties; the art is on the start screen only (not in play or results); aria-hidden; the fit above. Plant (must FAIL): one card's number changed on the page (e.g. 89 to 98).
4. /updates/: one dated line: "MaffsCards: three unbeatable cards on the start screen. Can you work out which category makes each one unbeatable?" docs/handover/cloud.md entry. After #919 is on main: merge main in, Gate green, python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line.

DO NOT TOUCH:
- MaffsCards' rules, cards.json, tools/maffscards/, Marvin, lines, challenge and daily logic, analytics, boards, the menu panels (including #919's "Today's deal" panel), play and results screens.
- schools/assets/, every other game, canon, the roster, .github/workflows/.

SUCCESS CONDITION:
- The start screen shows 96, 1 and 89 fanned behind the title, numbers and nicknames from cards.json, title readable; nothing that was above the fold falls below it at 320x568, 375x667 (normal and Aa) or 1280x720.
- The art unit passes and its plant is caught; every existing check passes; merged after #919, through merge-pr.py, last line reported; cloud.md records it.

STOP IF:
- The art cannot fit a phone start screen without pushing a control below the fold, even made smaller: report the measurements; do not hide the art or move the controls.
- Merging main (with #919) in conflicts in a way that needs changing #919's code: report the conflict; do not change #919's lines.
- Any existing check fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output; do not merge another way.
