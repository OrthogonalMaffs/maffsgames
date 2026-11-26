CROWD-FILL (Project Claude, Thu 26 Nov 2026 10:35; first drafted 25 Nov 10:30 and never sent; re-checked against main 5ee7387, every line reference still holds)
Jon, 25 Nov 2026, playing Some Thingies Pro Stage 4 to question 66: 10:18 "I like the growing crowd"; 10:20 "BOOO !!! We don't want a +5. we want more thingies."; 10:20 "makes me want to stop now."; 10:21 "we have LOADS of room on a big screen." 10:22 on the cheer at 500: "500 questions answered is a bit much." (Thresholds 1, 10, 20, 30, 50, 75, 100.) (Project Claude's proposal, 10:21, accepted: the crowd fills the room the screen has, full size until it reaches the bottom of the screen, then shrinks to fit more; the cheer escalates.) Jon, 26 Nov 2026, 10:28, at question 61: "we're on +2 again".
RECOMMENDED: Claude Code, Sonnet 5.5, effort medium. One game's decoration, measured, with its verifier.
LANE: cloud, lane 2. SEND: now, once lane 2 has reported MAFFSCARDS-START-ART (#921, merged 1e1f3db) finished. The home lane is idle (Jon at work). One PR, branch from current origin/main.
TIER: Small (merge on green).

TASK: In Some Thingies' winner-stays-on run, show every thingy the student has earned: the crowd grows at full size into the room the screen has, shrinks to fit more only once that room is full, and never collapses into "+n"; its cheer escalates with its size.

ROOT CAUSE: Shown: games/some-thingies/index.html:1053 caps the drawn crowd at CROWD_MAX = 48 and draws "+n" beyond (:1060), so after 48 right answers each new one adds a number, not a thingy, while a laptop screen has most of its height empty below the card (Jon's screenshot at question 66: one row of 47 and "+7"; 26 Nov at question 61: two rows and "+2"). The crowd is the run's reward; when it stops visibly growing the reason to answer one more goes (Jon: "makes me want to stop now"). The cheer is one fixed line (L.cheer, :350 and :373) at 1 thingy or 100.

CLASS CHECK: Local: one game's decoration (the comments at :175-176 and :1051-1052 call it decoration only; nothing reads or writes the score). No shared asset changes.

EXACT CHANGE:
0. First commit: close-outs per AGENTS.md:62 of MAFFSCARDS-START-ART (#921, 1e1f3db; its contract docs/handover/contracts/2026-11-25-maffscards-start-art.md to docs/history/contracts/) and of MARVIN-LOG (#911, 91b4e59; lane 1 is closed, so this lane records it; contract docs/handover/contracts/2026-11-25-marvin-log.md to docs/history/contracts/; main's runs on 91b4e59 as lane 1 reported them: check-site 45612786471, phone-fit-full 45612786218, pages 45612785652); then save this contract verbatim as docs/handover/contracts/2026-11-26-crowd-fill.md.
1. games/some-thingies/index.html, the crowd (CSS :175-183, the crowd code from :1051):
   a. Remove CROWD_MAX and the "+n" span: every thingy earned (crowdN) is drawn.
   b. Size: thingies are drawn at the current 16 px until the crowd's bottom would pass the bottom of the visible screen (the viewport, measured from the crowd's own top, after the card's other content); from then on every thingy shrinks together, to the largest size at which all fit in that room, down to a floor of 6 px. Below the floor (a phone at a very long run), rows simply continue at 6 px and the page may scroll; the crowd never covers or moves the question, the options, the feedback or Next, which are all above it. Re-measure on each new thingy and on resize. Measured, never a breakpoint or a width guess.
   c. The faint, the colours in order, the medal in Pro mode and reduced motion are unchanged at every size.
   d. The cheer escalates with crowdN, in both looks, from these lines (placeholders by Project Claude for Jon to rewrite; keep them in L beside cheer, one list per look):
      standard: 1 "A crowd is gathering." / 10 "Word is spreading." / 20 "Someone's selling hot dogs." / 30 "The thingies have formed a fan club." / 50 "Stadium capacity reached. They've opened another stadium." / 75 "Thingies are queuing round the block. The block is concerned." / 100 "Every thingy on Earth is here. Some came from Mars."
      kids: 1 "The crowd goes wild!" / 10 "More thingies are coming!" / 20 "The thingies are dancing!" / 30 "A thingy party!" / 50 "Fifty thingies! Wow!" / 75 "The whole town is here!" / 100 "Thingies from space!"
      The line shown is the one for the largest threshold crowdN has reached. The faint line is unchanged.
   e. Jon's tagline, 25 Nov 2026, 10:23: "how many thingies can you collect ?". Use it in three places:
      - the overtime line at question 11 (L.overtime, :344 and :368): standard "Ten done. How many thingies can you collect? One slip ends it."; kids "How many thingies can you collect? One slip ends it!";
      - the menu note (MENU_NOTE, :393): "At least 10 questions, then see how many thingies you can collect: keep going until a slip, or press End. A point for each one right.";
      - the results screen, when the crowd is not empty: one line under the existing end line (#endLine, set at :1242), "You collected <crowdN> thingies." (kids: "You collected <crowdN> thingies!"; "thingy" when it is 1).
   f. Update the comments at :175-176 and :1051-1052 to describe this.
2. scripts/verify-some-thingies.py: drive a run past 120 right answers (by its existing seeded play or test hook) at 1280 x 720, 1904 x 864 and 375 x 667, in both looks, and assert: the number of thingies drawn equals crowdN at every step (no "+n" anywhere); thingies are 16 px until the crowd reaches the viewport's bottom, then shrink, never below 6 px; nothing in the card above the crowd moves or is covered as it grows; the cheer is the right line at 1, 9, 10, 20, 30, 50, 75 and 100; the faint still happens on the run-ending slip; the overtime line and the results line carry the tagline and the right count (1 thingy, n thingies). Plants that must fail: CROWD_MAX put back at 48; a thingy drawn below 6 px; the cheer stuck on the first line. If the new checks push the verifier's CI line over the per-line limit, put it on SHARD units (scripts/ci_shards.py, as verify-maffscards.py).
3. Phone fit runs on the PR by itself for this game (do not dispatch it): every asking and wrong-answer screen must measure as on main.
4. /updates/: one dated line: "Some Thingies: every thingy you collect now joins the crowd, however long your run." docs/handover/cloud.md entry; docs/todo.md row SOME-THINGIES-LIST: add "crowd fills the screen, cheer escalates (CROWD-FILL, 26 Nov 2026); Jon to rewrite the cheer lines". Merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600 on green; report its last line.

DO NOT TOUCH:
- The bank, marking, scoring, the run rules (at least 10, then winner stays on), analytics, the boards, the Read aloud, Sarge, the start screen's crowd, Stage 4's question display (a separate decision is pending with Jon).
- schools/assets/, every other game, canon, the roster.

SUCCESS CONDITION:
- On a laptop, a run of 66 shows 55 thingies at full size in rows below the card (no "+7"); on a long run the crowd fills the screen and then shrinks to fit; on a phone it shrinks sooner and never moves the question or Next; the cheer changes at each threshold in both looks; the tagline shows at question 11, on the menu and, with the count, on the results screen.
- verify-some-thingies.py passes with the three plants caught; phone fit green; merged through merge-pr.py; last line reported; cloud.md records it; #921 and #911 closed out.

STOP IF:
- The crowd cannot grow without moving or covering anything above it at some contract size: report the size and what moves.
- A long run in the verifier becomes slow to draw (over 50 ms per new thingy at 120): report the timing; do not cap the crowd.
- Any existing check fails and the cause is not in this change.
- merge-pr.py cannot reach GitHub, or refuses: report its output, do not merge another way.
