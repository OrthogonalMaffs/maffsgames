# EQUATLE-PHONE-FIT (Jon, 6 Nov 2026), verbatim

Name given by the cloud lane (the contract has none).

LANE: cloud (one session) · TIER: Small · start from current main (1372859 or later)

COORDINATION: the home lane may be running ROOM-ORDER-HERRINGS (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. Record in docs/handover/cloud.md.

TASK: On a phone, Equatle's whole board and its full keypad, including Enter, fit on one screen with no scrolling, so a student can play a whole puzzle without touching the page.

ROOT CAUSE: games/equatle/index.html sizes everything from the screen's width only: the tiles are square (aspect-ratio 1) across 8 columns, the keypad has three rows with Enter alone on the third (line ~254), and the title block (eyebrow, "Equatle", subtitle) and the five-box stats bar sit above the board at full height on every screen. Nothing budgets for height. EQUATLE-320 (#669) measured Enter ending at 858px against a visible 528px at 320x568; the vertical fault was already on the phone-fit known-failures list.

CLASS CHECK: Local. The fault is this game's own layout (its keypad, title block and tile sizing); no shared CSS is involved. Other games' below-the-fold controls are already tracked one by one on the phone-fit list and are not in scope.

EXACT CHANGE (games/equatle/index.html only, CSS and the keypad markup):
1. Keypad: put Enter on the operator row with Del (row 2: + − × ÷ = Del Enter), removing the third row. Enter stays visually distinct (its existing colour) and at least 44px wide.
2. Tiles: size from height as well as width: the board's width is the smaller of the current width and what the remaining screen height allows for 6 rows, so tiles shrink on short screens and stay square. Use dvh/svh (with a vh fallback) so phone browser bars are counted.
3. Short screens (max-height around 740px): the eyebrow line and subtitle hide, the "Equatle" title shrinks, and the stats bar's height reduces. Nothing is removed on taller screens. The rules, help and stats stay reachable from the nav buttons.
4. Measure before and after (normal and Aa mode) at 320x568, 360x640, 375x667, 390x844, 412x915 and 1280x800: the bottom of the Enter key and the bottom of the sixth board row, against the visible height. Table in the PR.
5. Update the game's phone-fit entry: remove the vertical known-failure if it now passes; update scripts/phone-fit-state.json / checker entries only as the checks require (they fail on stale entries).
6. /updates/: one plain line (students see this change).

DO NOT TOUCH: game logic, puzzle generation, the daily seed, scoring, stats, the leaderboard, colours, the keypad's digit row (EQUATLE-320's fit), any other game, shared assets.

SUCCESS CONDITION: At 360x640, 375x667, 390x844 and 412x915, in normal and Aa mode, the whole board and the full keypad including Enter are visible with no scrolling and no sideways scroll; at 320x568, the same, or the best achievable with the shortfall measured and reported. Desktop unchanged in appearance. Equatle's verifier (if any), the phone-fit checks and check-changed.py (per the cloud-lean ruling) pass. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: tiles would fall below about 28px at 360x640 to make everything fit (report the size and wait); a change is needed outside games/equatle/index.html, the phone-fit/checker entries, /updates/ and cloud.md; the title block cannot shrink without breaking check-theme.py.
