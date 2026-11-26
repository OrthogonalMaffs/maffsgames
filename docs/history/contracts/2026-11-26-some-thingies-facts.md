SOME-THINGIES-FACTS (Project Claude, Thu 26 Nov 2026 13:55; checked against main f060351)
Jon, 26 Nov 2026 (morning, on "WHERE ARE MY THINGIES?" at Pro Stage 4): "please go with both": (a) after marking, a picture of the fact in the Stage 1 plates style; (b) a thingy beside the question that reacts to each answer, as Sarge does in Stage 3. Jon, 13:34: a second cloud lane this afternoon.
RECOMMENDED: Claude Code, Opus 5.5, effort high. A live game for [name removed by the implementer, personal-details scan: a named person's] class; phone fit is the risk.
LANE: cloud, lane 3 (new this afternoon). SEND: now. Lane 2 is on DAILY-POLISH (MaffsCards and scripts/set-maffscards-daily.py): no shared files except docs/handover/cloud.md; merge main in before merging if cloud.md has moved. No close-out to carry (this lane's first task; DAILY-FIT's close-out rides on lane 2).
TIER: Medium (merge on green).

TASK: In Some Thingies' Stage 4 (Times table facts), give the question a thingy beside it that reacts to each answer, and after each answer is marked show the fact as plates of thingies, without ever pushing Next below the fold.

ROOT CAUSE: A design gap, shown by Jon at Pro Stage 4: Stages 1-3 each draw thingies (plates, the conga line, the array with Sarge); Stage 4 draws none. games/some-thingies/index.html nextQuestion() (:1004-1046): the fact and missing branches (:1043-1044) only set the sum and the options; #pic stays empty and #sargeMini is filled only for 'array' (:1023). settle() (:1205-) adds react-right / react-wrong to #pic and #sargeMini (:1217) but both are empty in Stage 4.

CLASS CHECK: Local. One game's Stage 4 decoration, built from its own plates() (:896), thingy() (:873) and the reaction classes it already has (CSS :119-131). No shared asset changes; nothing reads or writes the score.

EXACT CHANGE (games/some-thingies/index.html; scripts/verify-some-thingies.py):
1. The thingy beside the question: on every Stage 4 question (types 'fact' and 'missing'), #sargeMini holds one thingy, thingy(6) (the one in glasses), with the pro medal in Pro as every thingy in play has. It reacts exactly as Sarge does: react-right / react-wrong from settle(), cleared on the next question. No new line, no name, no new text. Stage 3 keeps Sarge; Stages 1 and 2 keep an empty #sargeMini.
2. The picture after marking: in settle(), for a Stage 4 item, after a right or a wrong answer, draw the fact into #pic with plates(): a 'fact' item a × b as a plates of b; a 'missing' item ? × b = product as answer plates of b. So it matches the game's "a groups of b" (working(), :824). Nothing is drawn before marking (a picture before would give the answer away). It gets the same react class as the rest of #pic, and clearPic() on the next question removes it.
3. The fit: Stage 4 has products up to 12 × 10 = 120 (Main) and 12 × 8 = 96 (Pro), more than plates() was sized for (50 thingies, 10 plates: CSS comment :97-98). The picture must never push Next (#nextBtn, or the shared Next after a wrong answer) below the fold, measured as congaFit() measures it (:1052-; the fold less the fixed footer). Shrink the picture's thingies and plate gaps first (the same idea as congaFit: a size variable, from 18 px down to a floor of 10 px); if Next would still be below the fold at the floor, the picture is not shown for that item at that size (the working line still shows the fact). Measured, never a breakpoint, re-run on resize.
4. The crowd: past question 10, the crowd's size is set when the question is drawn and must not change between marking and the next question because the picture appeared (fitCrowd() runs on changes above the crowd, :1103-1106). The picture fits into the room the crowd leaves. Reasonable ways: exclude #pic's after-marking change from the crowd's measurement, or measure the picture against the crowd as it stands. Your choice, named in the report.
5. Verifier (scripts/verify-some-thingies.py): new units, Main and Pro, both looks, at 320x568, 375x667, 1280x720, normal and Aa:
   - every Stage 4 item: #sargeMini holds one thingy with data-acc "glasses" (a medal in Pro); it carries react-right after a right answer and react-wrong after a wrong one, and neither on the next question;
   - after marking, every Stage 4 item where the picture shows: the number of plates and the thingies on each plate match the item (a plates of b; answer plates of b); none before marking;
   - Next above the fold on every item, right and wrong; report per size and look how many of the 192 items show the picture and how many drop it;
   - past question 10, the crowd's size is the same before and after marking.
   Plants (each must FAIL): the picture drawn before marking; b plates of a in place of a plates of b; the size floor removed so Next falls below the fold; the beside thingy left without its reaction.
6. docs/handover/cloud.md entry. Roster row 115: in "4 Facts (...)", add "a thingy in glasses beside each question; after marking, the fact as plates". /updates/: one dated line, "Some Thingies: Stage 4 now has thingies too: a quizzer in glasses, and each fact drawn as plates once you've answered."

DO NOT TOUCH:
- The bank (tools/some-thingies/bank.py and the items in the page), marking, scoring, options, events, boards, levels.
- LINES (Jon's), the cheer lines and the crowd's look (CROWD-FILL), Stages 1-3 and their pictures, Sarge.
- schools/assets/, every other game, canon, every workflow, scripts/merge-pr.py, MaffsCards and anything lane 2 is changing.

SUCCESS CONDITION:
- Every Stage 4 question in both modes and both looks has the reacting thingy in glasses beside it; after marking, the fact as a plates of b (or answer plates of b), shrunk as needed, dropped only where Next could not otherwise stay above the fold.
- Next above the fold on every Stage 4 item at the three sizes in normal and Aa; the crowd does not change size at marking.
- The verifier units and four plants run in CI; merged on green through merge-pr.py; main green after; last line and main's runs reported; cloud.md records it, with the per-size counts of items showing the picture.

STOP IF:
- At 375x667 in normal mode, more than a quarter of the 192 Stage 4 items would drop the picture even at the 10 px floor: report the counts per size before building further (Jon may prefer a different picture for the big facts).
- Showing the picture needs any change to Stages 1-3's own pictures or to plates()'s output for Stage 1.
- Any existing Some Thingies verifier unit fails and the cause is not in this change.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.
