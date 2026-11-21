# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-21 (home): CLASS-PAGE (one hidden /class/ page for every child-look game; MaffsKids shared)

Claude Code (home lane), worktree `~/mg-class-page`, branch `claude/class-page`; contract `docs/handover/contracts/2026-11-21-class-page.md` (stored verbatim but for one teacher's first name, written "[a teacher's]"). The first commit carries SOME-THINGIES-TURN-LABELS' close-out (#870, 7d827fa).

- The two games' fragment rules were identical (no STOP). `schools/assets/kids-look.js` (MaffsKids: `read(hash)`, `read(hash, 'bare')`, `greeting()`, `gameLink()`, `classLink()`) is now the one copy. Each game passes its own `location.hash` once and keeps `LOOK`, `CLASS_NAME` and `greeting()`, so both verifiers pass unchanged with every plant caught.
- `/class/`: noindex, no menu, search or sitemap entry. Cards come from `"kids": true` in `data/games.json`, written in by `scripts/apply-class-page.py` (data/ is never published, so a fetch could not work). It loads analytics.js (the loader rule holds noindex pages to it); GA4's default page view leaves the fragment out.
- site-nav: `/class/` in HUBS ("the class page"); a game opened from `/class/#<Name>` goes back to `/class/#<Name>`, the name read from its own hash through MaffsKids; only the hub's path is in sessionStorage. Both games show stage-exit's short form, "← the class page" (STAGE-EXIT-LABEL).
- Checks: `scripts/test-kids-look.py` (Node vm, selective; 10 plants); check-site-nav's `class` unit and plant; check-site's site-wide class-name rule (Maple, plus `MAFFS_CLASS_NAMES`). For cloud: ci-deps' KNOWN_TOP lacks `class` (like printables, ugh-stats, core-maths), so a `class/` change counts as shared.

## 2026-11-21 (home): SOME-THINGIES-TURN-LABELS (Stage 3's turn: labels gone first, thingies eyes up)

Claude Code (home lane), worktree `~/mg-stl`, branch `claude/some-thingies-turn-labels`; contract `docs/handover/contracts/2026-11-21-some-thingies-turn-labels.md` (the 20:09 reissue with amendment 1, which arrived after I'd started; I carried on). The first commit carries SOME-THINGIES-PERSONALITY's close-out (#868, 8bf4b4e; its entry below).

- `turnArray()`: the labels fade (120 ms) and are cleared, then the array turns on `MaffsLock.timer`. The turned array is redrawn with empty labels. With reduced motion it is drawn at once.
- Amendment 1: `.arr.turning .th{transform:rotate(-90deg)}`, centred on each thingy, with the array's 0.6 s ease, so every thingy stays eyes up. Measured mid-turn in Chromium: net 0° within 3°.
- Next is there at once after marking; marking and the lock are untouched.
- The verifier's new `turn` unit (laptop and phone at full motion, phone with reduced motion) and two plants (labels left visible, no counter-rotation), both caught; 15 plants in all.
- MERGED 21 Nov as 7d827fa (#870) via merge-pr.py, exit 0, last line "main 7d827fa run 44946545379: GREEN". Main on the merge commit: check-site 44946545379 success, pages build 44946545012 success, phone-fit-full 44946545381 success with its matrix skipped (a game-only change selects no shared path), so some-thingies was measured locally on main 4ac9b3af: PASS in normal, aa and laptop modes. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-21-some-thingies-turn-labels.md` (closed out by CLASS-PAGE's first commit).

## 2026-11-21 (home): SOME-THINGIES-PERSONALITY (the thingies as characters; the game's own look)

Claude Code (home lane), worktree `~/mg-stp`, branch `claude/some-thingies-personality`; contract `docs/handover/contracts/2026-11-21-some-thingies-personality.md` (Jon approved the mock-ups, 21 Nov 18:40-18:43). The first commit carries SOME-THINGIES-TWEAKS' close-out (#866, e2ac03a; its entry below; contract moved to `docs/history/contracts/`).

- **The thingy:** `thingy(k)` is one inline SVG on a 24 × 24 grid: a body in colour k, eyes, three mouths (waiting, happy, puzzled; CSS shows one) and the accessory for k. **Mapping (my call, for Jon to swap):** #866's fixed colour order is red, orange, amber, green, teal, sky, indigo, purple, pink, brown, which isn't the order the contract's list assumed. To keep Jon's three examples, the oranges have spiky hair, the blues (sky) glasses and the purples the top hat; the other seven take the contract's order: red bow, amber cap, green flower, teal sprout, indigo headphones, pink beanie, brown moustache. A test sheet at 14, 19, 22 and 44 px (1× and 2×) showed all ten distinct at 19 px. Every thingy is from the set of 10, including Stage 1's plates (one colour a plate, thingies now 18 px).
- **Pro:** every thingy in play wears a gold medal, and the HUD's stage shows a "Pro" badge.
- **Reactions:** the pictured thingies bounce once on a right answer and tilt, puzzled, on a wrong one; a random one blinks every few seconds while a question waits. Transform only. With reduced motion nothing animates (document.getAnimations() is empty) and only the faces change. The blink timers carry `// lock-ok:` reasons (decoration only), as check-answer-lock asks.
- **Start screen:** 14 thingies in a 7 × 2 grid under a chunkier title (Outfit 800 with a yellow shadow). Start is above the fold at every phone-fit size in both looks (320×568: 401 of 528 px).
- **The conga line (Stage 2):** g groups of n, each one colour, holding hands, the sum above it, one group per line on a phone, swaying. It is drawn from the start on adding items, and only after marking on groups-to-sum items. **Fit:** on a short phone the line shrinks (to 14 px) so Next stays above the fold; if it still wouldn't fit (320×568, six groups), it steps aside once marked, as the contract allows for Sarge. The Stage 2 card's gaps are tighter and its one-column sum options are 44 px tall, which keeps the line at 360×640.
- **The parade ground (Stage 3):** the array is unchanged from #866. Sarge (dark grey, peaked cap) stands beside it on screens 600 px and wider, and sits in the card's top row on phones (no extra height). A right answer's one line is Sarge's.
- **The crowd:** from question 11, the cheer, then one thingy per right answer in colour order, 48 shown, "+n" beyond. The run-ending wrong makes them faint, with "*thud*". Decoration only: drawCrowd() never reads or writes the score.
- **Scheme:** every accent comes from the 10: grown indigo (col-7), kids purple (col-8), the stage circles red, pink, indigo and purple (all 4.6:1 or more with white text), and the kid look's card edges a band of the ten colours. The pink is gone. check-theme passes; it read "#866" in a comment as a hex literal, so that comment now names the contract.
- **LINES:** the stage names, Sarge, the cheer and the faint, in both looks (kid lines 6 words or fewer). The stage buttons and the HUD label use the names.
- **Verifier:** every thingy's accessory read from its SVG shapes against the colour map, and medals exactly in pro; nothing animating under reduced motion; a `scenes` unit (start screen at every phone-fit size in both looks, the conga line on every Stage 2 item at 320×568, 360×640 and 1280×720, Sarge and Next on every array); the crowd growing, capped and never scoring, then fainting. Three new plants (a wrong accessory, an animation under reduced motion, the crowd changing the score); all 13 are caught.
- Roster note updated. Local runs: the verifier, check-theme, check-answer-lock (some-thingies), measure-phone-fit `--only some-thingies` in normal, aa and laptop modes, check-site `--only some-thingies`, check-start-mount, check-teacher-invite, verify-stage-exit and check-meta all pass.
- MERGED 21 Nov as 8bf4b4e (#868) via merge-pr.py, exit 0, last line "main 8bf4b4e run 44943720706: GREEN". Main on the merge commit: check-site 44943720706 success, phone-fit-full 44943720773 success (some-thingies PASS in normal, aa and laptop modes), pages build 44943720464 success. Jon accepted the conga fallback at 320 px (21 Nov, 19:46). Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-21-some-thingies-personality.md` (closed out by SOME-THINGIES-TURN-LABELS' first commit).

## 2026-11-21 (home): SOME-THINGIES-TWEAKS (Stage 3 as coloured thingies, a fading scaffold, winner stays on)

Claude Code (home lane), worktree `~/mg-st-tweaks`, branch `claude/some-thingies-tweaks`; contract `docs/handover/contracts/2026-11-21-some-thingies-tweaks.md` (Jon's rulings after play-testing, 21 Nov 17:40-18:07). The first commit carries SOME-THINGIES' close-out (#865, a579740; its entry below; contract moved to `docs/history/contracts/`).

- **Stage 3 picture (option C):** each cell is the game's thingy. Every column has its own colour from one fixed set of 10 (tokens `--col-1`..`--col-10`), and once the array turns the colours follow their thingies. There is a gap of 0.7 of a thingy after the 5th column and the 5th row. The size is 22 px at most, smaller only where the width or the height (with the options under it) needs it: 22 px for 5 × 10 and 10 × 5 at 360×640, 19 px for 10 × 5 at 320×568. The dot tokens are gone.
- **Scaffold:** questions 1-4 ask "How many rows?", "How many in each row?", then the total; 5-7 show the rows label and ask each row, then the total; 8 and later ask the total only. The step options are the number and its two neighbours, made in the page and marked by dataset.val. Each step labels the array ("R rows" down the side, "C in each row" along the top) with the right number either way, and never scores.
- **Winner stays on:** items are dealt with no repeat until all are used, then reshuffled without repeating the item just answered. In questions 1-10 a wrong answer goes on as before. From 11, the first wrong ends the run (its feedback, then "See results →"), and End in the HUD ends it at once. The HUD shows "n/10", then "n". The results show the score and "n answered". game_completed and submitScore carry the real counts, once.
- **LINES:** placeholders for the steps, the labels, question 11 (`overtime`) and the end screen after a wrong past 10 (`overtime_end`), in both looks; every kid line is 6 words or fewer. The stage 3 question reads "How many thingies?".
- **Verifier:** adds checks on the array (thingies, the colours by column and by row, one fixed set of 10, the gaps), the largest arrays at 360×640 with labels on, and a `winner` unit (10 right then a wrong; a wrong at 3; End at 12; no End before 11; the supply; the scaffold 3/2/1 steps, labels, no scoring). Full runs now end at the wrong at question 11. New plants: the run ending at the first wrong, End at question 5, a step that scores, a dot instead of a thingy. All 10 are caught. The bank's hash is unchanged.
- Roster row and note, and todo SOME-THINGIES-LIST ("Jon checks the new stage 3 picture, the scaffold and winner stays on"). The old row is kept word for word in `docs/history/todo-done.md` ("Row rewritten by SOME-THINGIES-TWEAKS"), as check-todo-trim requires.
- **Two follow-ons, both in the page:** (a) the maffs-lock-hint answers wrong from question 11. A run of right answers now never ends, so check-answer-lock's tap-through, which answers right every time, would never see game_completed. (b) Once turned, the array is sized with the feedback and Next under it, so Next stays above the fold: worst 574 of 600 px at 360×640, 650 of 680 at 1280×720. The verifier caught this on a 9-row turned array at 623 px.
- MERGED 21 Nov as e2ac03a (#866) via merge-pr.py, exit 0, last line "main e2ac03a run 44937592606: GREEN". Main on the merge commit: check-site 44937592606 success, phone-fit-full 44937592595 success (some-thingies PASS in normal, aa and laptop modes), pages build 44937592602 success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-21-some-thingies-tweaks.md` (closed out by SOME-THINGIES-PERSONALITY's first commit).

