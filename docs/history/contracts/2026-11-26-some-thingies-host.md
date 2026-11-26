SOME-THINGIES-HOST (Project Claude, Thu 26 Nov 2026 18:00; checked against main e367eb4)
Jon, 26 Nov 2026, 14:55 (Main Stage 4, question 105, screenshot): "yes lets make the thingy in glasses more prominent please". Standing: SR-35 (canon §0.3, merged today in #928): on a phone, playability beats personality; decoration grows only where the screen has room.
RECOMMENDED: Claude Code, Opus 5.5, effort medium. One game's characters; the fold is the risk.
LANE: cloud, the large-screen lane (its branch already holds commit 292e92a9 with LARGE-SCREEN-LAYER's close-out and Jon's DAILY-POLISH rulings). SEND: now. That commit is this task's first commit; add main e72faba's runs (check-site 45868985623, phone-fit-full 45868985530, pages 45868984559, all success) to it if not already there (AGENTS.md:62). Never force-push: if a push is refused, report it.
TIER: Medium (merge on green).

TASK: Make Some Thingies' character beside the question (the thingy in glasses in Stage 4, and Sarge in Stage 3) a prominent presence wherever the screen has room, sized to the room, never costing the fold.

ROOT CAUSE: games/some-thingies/index.html draws the Stage 4 thingy in glasses in the card's top row at 22 px (:173 .sarge-mini .th 22px; :179 .qcard.quiz .sarge-mini shown at every width; markup :304), so on a laptop it is a dot beside the stage label (Jon's screenshot, 26 Nov 14:55). Sarge in Stage 3 is the same character slot: 30 px beside the array on wide screens (:170-171 .sarge-wide), 22 px in the top row on phones (:172-174).

CLASS CHECK: Two components of one game share the shape (a reacting character fixed at 22-30 px whatever the room): Stage 4's thingy in glasses and Stage 3's Sarge. So one sizing rule serves both, not two patches. Local to this game: no shared asset.

EXACT CHANGE (games/some-thingies/index.html; scripts/verify-some-thingies.py):
1. One measured size for the character beside the question, shared by Stage 3 (Sarge) and Stage 4 (the thingy in glasses): where the screen has room, it is drawn at the largest size from 96 px down to 48 px that keeps every rule in step 3, placed beside the question so it costs as little height as possible (Stage 4: beside the sum line, the quiz-show host; Stage 3: where Sarge stands now, beside the array, scaled). Where even 48 px would cost the fold, it stays as today (the top row at 22 px). Measured, never a breakpoint (the room as the game's own congaFit() :1068 / fitCrowd() :1136 measure it: the viewport less the fixed footer), re-run on resize.
2. The size is chosen when the question is drawn and does not change at marking (no jump as it reacts), and it is chosen so the marked screen also fits, with Stage 4's fact picture (SOME-THINGIES-FACTS) and the crowd past question 10 as they are measured today. Order of give, when room is short: the character gives way first (SR-35), then the fact picture as today; the crowd's own rules unchanged.
3. The fold, strict where main holds it: the options above the fold on every asking screen and Next above the fold after every marking, at every size the game is measured at today (phone and laptop, normal and Aa), both looks. Any item where main already loses the fold stays exactly as main (the character in the top row), listed on a known list with CI's own figures (measure in CI, not in the container: fallback fonts differ), failing as stale when it comes to fit.
4. Reactions as now (react-right bounce and smile; react-wrong tilt, puzzled), scaled with the size; reduced motion shows the faces without movement; the medal in Pro.
5. Verifier: units for Stage 3 and Stage 4, Main and Pro, both looks, at 320x568, 375x667, 1366x768, 1920x955, normal and Aa: the character's drawn size and place (beside the question at 48-96 px where it fits; the top row at 22 px otherwise); options and Next above the fold on every item not on the known list; the size the same before and after marking; past question 10 the crowd's size the same as it would be without the change (sampled as SOME-THINGIES-FACTS samples it). Plants (each must FAIL): the character fixed at 96 px whatever the room; its size changing at marking; Sarge left at 30 px while the thingy in glasses grows (the shared rule bypassed). docs/handover/cloud.md entry. /updates/: one dated line, "Some Thingies: the quiz-show host and Sarge are bigger on screens with room."

DO NOT TOUCH:
- The bank, marking, scoring, events, boards, LINES, the cheer lines, the crowd's own sizing (CROWD-FILL), the fact picture's own rules (SOME-THINGIES-FACTS), the start screen.
- schools/assets/ (the large-screen layer included: Some Thingies is not migrated to it), every other game, canon, the roster, every workflow, scripts/merge-pr.py.
- No force-push.

SUCCESS CONDITION:
- At 1366x768 and 1920x955 the thingy in glasses (Stage 4) and Sarge (Stage 3) are drawn at 48-96 px beside the question; on phones they are where they fit; the fold rules hold everywhere main holds them, normal and Aa, both looks.
- Verifier units and three plants in CI; merged on green through merge-pr.py; main green after; last line and main's runs reported; cloud.md records each measured viewport's size.

STOP IF:
- At 1366x768 normal mode the character cannot reach 48 px beside the question on some item without costing the fold: report the stage, item, room and size that fits.
- Any fold measurement that passes on main fails after the change.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
