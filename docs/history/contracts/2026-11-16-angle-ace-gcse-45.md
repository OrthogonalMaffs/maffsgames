ANGLE-ACE-GCSE-45, AMENDMENT 2 (whole contract reissued; Project Claude, Mon 16 Nov 2026 13:40; Amendment 1 12:10; original 11:40; Jon 11:15 "yes please, lets keep cloud lane working")
AMENDMENT 2: allows one generated file under schools/assets/: schools/assets/six-ps/angles.json, regenerated from the game (EXACT CHANGE 7, ROOT CAUSE, DO NOT TOUCH, SUCCESS, STOP IF), and widens the /updates/ line. CONTINUE on branch ccr-bd20fca4-euxido (PR #795, head 4cf84c4): its commits stand as done (close-out; bank, headers, COUNTS, ledger, /updates/; the :914 verifier fix; the stop recorded in cloud.md). Add one commit: the regenerated angles.json, the /updates/ line as amended, docs/handover/contracts/2026-11-16-angle-ace-gcse-45.md replaced with this text verbatim, and cloud.md's entry updated from STOPPED to this amendment. Push, wait for a green Gate, then merge with merge-pr.py. (Amendment 1 added the :914 self-test fix. The ccr- branch name is the cloud environment's own and is accepted.)
Recommended: Sonnet, effort medium: ten checked items pasted into one bank, one count changed in the verifier; the verifier does the geometry.
LANE: cloud. SEND: now, to the session that stopped on this contract (it holds the branch and PR #795). TIER: Small (merge on green; Project Claude reviews after the merge; Jon plays GCSE after it). One PR, branched from current origin/main.
CLOSE-OUT (first commit, AGENTS.md:61): MERGE-ROUTE-RETIRE merged #794 by merge-pr.py (the only route; its last line "main 4e7a25d run 43847525596: GREEN", exit 0) as 4e7a25d; main check-site 43847525596 success (10:31:06 UTC), phone-fit-full 43847525561 success (10:17:52 UTC), both push-triggered. Move docs/handover/contracts/2026-11-16-merge-route-retire.md to docs/history/contracts/ with those figures. Save this contract verbatim as docs/handover/contracts/2026-11-16-angle-ace-gcse-45.md in the same commit.
MERGE: python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, unpiped; report its last line. No other route: if merge-pr.py cannot reach GitHub, STOP and report; the PR waits.

TASK: Bring Angle Ace's GCSE bank from 35 to 45 questions with the ten items below, verbatim, so the level meets the site's 40-50 minimum.

ROOT CAUSE (main 4c13e95): QUESTIONS_BY_LEVEL.gcse in games/angle-ace/index.html (:501-645) has 35 items, below the 40 minimum (todo 1.52, "STILL LIVE: GCSE has 35 questions"). The headers at :301 and :499 say "GCSE 35"; scripts/verify-angle-ace.py holds COUNTS = {'year6': 40, 'gcse': 35} (:57).
- Latent verifier bug (found by the cloud lane, 16 Nov 11:59): the self-test's filter at scripts/verify-angle-ace.py:914 looks every recording key (level, index, width) up in banks['year6'] by index alone, ignoring the level. With 35 GCSE items every GCSE index was below year6's 40, so it never crashed but let GCSE recordings with a matching index into the planted set; with 45, indices 40-44 raise IndexError and the self-test dies before planting a fault.
- Derived bank (found by the Gate on #795, run 43863264772, step "The 6 P's banks"): schools/assets/six-ps/angles.json is generated from this game's GCSE bank (scripts/gen-six-ps.py topic_angles, :772, loads angle-ace?level=gcse). Adding items without regenerating it fails "angles.json is not what the game's questions generate". schools/assets/exam-topics-ocr-foundation.json depends only on the bank holding 30 or more, so it is unchanged (Project Claude: gen-exam-topics.py --check PASS with the 45-item bank).

CLASS CHECK: Local. One game's bank is short; the content was the missing piece (todo 1.52: "Adding questions is content (Jon's call); every new item needs only a fig and passes scripts/verify-angle-ace.py or fails it"). The diagram correctness class (audit class 6) is already fixed architecturally: every figure is drawn by drawFig() from its fig and measured by the verifier, which these items go through unchanged. No shared code changes. The verifier fix is local too: one verifier's filter fails to match on level; no shared module is involved. The 6 P's file is the repo's generated-bank pattern (the game is the source, the 6 P's file derived from it): the fix is to regenerate it, never to edit it by hand or change the check.

EXACT CHANGE:
1. In games/angle-ace/index.html, append these ten items to QUESTIONS_BY_LEVEL.gcse, verbatim, after the last item (the "Three angles on a straight line. Find x." item, whose steps end 'x = 90°']},) and before the closing ]; of the array:

// === MORE PRACTICE (10 added 16 Nov 2026) ===
{fig:{t:'par',m:[['T','lr',47],['B','ul','x']]},
prompt:'Find angle x',answer:47,reason:REASONS.ALT,angleOpts:[47,133,57,43],steps:['47° and x are alternate angles','Alternate angles are equal','x = 47°']},

{fig:{t:'par',m:[['T','ul',112],['B','ul','x']]},
prompt:'Find angle x',answer:112,reason:REASONS.CORR,angleOpts:[112,68,122,102],steps:['112° and x are in the same position at each intersection','Corresponding angles are equal','x = 112°']},

{fig:{t:'par',m:[['T','lr',84],['B','ur','x']]},
prompt:'Find angle x',answer:96,reason:REASONS.COINT,angleOpts:[96,84,106,86],steps:['84° and x are co-interior angles','Co-interior angles sum to 180°','x = 180° − 84° = 96°']},

{fig:{t:'cross',r:[124,null,'x',null]},
prompt:'Find angle x',answer:124,reason:REASONS.VERTOP,angleOpts:[124,56,134,114],steps:['x and 124° are vertically opposite','Vertically opposite angles are equal','x = 124°']},

{fig:{t:'cross',r:[36,null,'x',null]},
prompt:'Find angle x',answer:36,reason:REASONS.VERTOP,angleOpts:[36,144,46,26],steps:['Vertically opposite angles are equal','x = 36°']},

{fig:{t:'point',r:[95,140,'x']},
prompt:'Find angle x',answer:125,reason:REASONS.POINT,angleOpts:[125,235,135,115],steps:['Angles at a point sum to 360°','95° + 140° + x = 360°','x = 360° − 235° = 125°']},

{fig:{t:'point',r:[80,75,90,'x']},
prompt:'Find angle x',answer:115,reason:REASONS.POINT,angleOpts:[115,245,105,125],steps:['Angles at a point sum to 360°','80° + 75° + 90° + x = 360°','x = 360° − 245° = 115°']},

{fig:{t:'tri',A:52,B:'x',iso:true},
prompt:'The triangle is isosceles (marked sides equal). Find x.',answer:52,reason:REASONS.ISOSC,angleOpts:[52,76,128,38],steps:['Base angles of an isosceles triangle are equal','x and 52° are the two base angles','x = 52°']},

{fig:{t:'ext',A:35,C:72,x:'x'},
prompt:'Find exterior angle x',answer:107,reason:REASONS.EXTERIOR,angleOpts:[107,73,117,97],steps:['The exterior angle equals the sum of the two interior opposite angles','x = 35° + 72° = 107°']},

{fig:{t:'tri',A:44,B:102,C:'x'},
prompt:'Find angle x',answer:34,reason:REASONS.TRIANGLE,angleOpts:[34,146,44,24],steps:['Angles in a triangle sum to 180°','44° + 102° + x = 180°','x = 180° − 146° = 34°']},

   (Project Claude ran scripts/verify-angle-ace.py --no-selftest locally with exactly these ten items appended and COUNTS gcse 45: "PASS: 0 FAIL(s); 85 items (year6, gcse) measured at 320/390/1280 px; every option and reason marked in Chromium".)
2. The comment headers: :301 "Starter 40, GCSE 45"; :499 "45 questions".
3. scripts/verify-angle-ace.py: COUNTS gcse 35 -> 45 (:57, done); and at :914 the filter becomes
       if k[0] == 'year6' and banks['year6'][k[1]].get('isRecognition') and banks['year6'][k[1]]['answer'].startswith('Alternate')}
   (k[0] == 'year6' added at the front; nothing else in the line changes). Nothing else in the verifier changes (no TWO_STEP entry: all ten are one-step items). Project Claude ran the full verifier, self-test included, with the ten items, COUNTS 45 and this fix: all 8 planted faults caught; "PASS: 0 FAIL(s); 85 items (year6, gcse) measured at 320/390/1280 px".
4. data/check-ledger.json: if it holds a B4 entry for angle-ace's GCSE level, remove it the way the repo removes a fixed entry; check-banks must pass B4 for angle-ace at both levels. Leave the year6 B3 duplicate entries (the recognition items) untouched.
5. /updates/: one line in the site's plain wording: "Angle Ace: ten more GCSE questions, including angles at a point, vertically opposite and exterior angles. The 6 P's angles practice gets them too." (replace the line already added).
6. docs/handover/cloud.md: an entry for this PR, ending with the row for the home lane: close todo 1.52 (GCSE now 45; KS3 part already fixed by #333).
7. schools/assets/six-ps/angles.json: regenerate with python -X utf8 scripts/gen-six-ps.py --write --only angles, and nothing else; commit the file as written. Then python -X utf8 scripts/gen-six-ps.py --check --only angles must PASS, and python scripts/gen-exam-topics.py --check must PASS. Project Claude ran exactly this with the 45-item bank: "angles 45 questions bands [1, 2, 3, 4]"; "0 still faulty after the labels are moved"; "PASS 1 banks match their games"; gen-exam-topics "PASS"; only angles.json changed (228 lines added).

DO NOT TOUCH: the 35 existing GCSE items and the 40 Starter items; the ten new items' text, numbers, options and steps (if any fails a check, STOP; do not edit it); drawFig, FIG and every other function; the verifier beyond COUNTS and the :914 filter; the ledger's year6 entries; schools/assets/ except schools/assets/six-ps/angles.json as regenerated (never hand-edited); scripts/gen-six-ps.py and its checks; docs/todo.md; canon; the roster; Gate files; every other game.

SUCCESS CONDITION: Angle Ace GCSE has 45 items, the ten above verbatim; verify-angle-ace.py passes with its self-test (every planted fault still fails); check-banks passes B4 for angle-ace at both levels; the headers say 45; schools/assets/six-ps/angles.json regenerated (45 questions) and the 6 P's checks pass; /updates/ has the line; merged by merge-pr.py; main's check-site and phone-fit-full green on the merge commit and reported with their IDs; cloud.md updated and the work committed.

STOP IF: gen-six-ps.py --write --only angles changes any file other than angles.json, or its --check, its diagram-label check or gen-exam-topics --check fails; the Gate fails for any other reason; any of the ten items fails verify-angle-ace.py or check-banks (report the item and the failure; change nothing in it); the verifier's self-test, with the :914 fix, fails to catch any planted fault or still crashes; merge-pr.py cannot reach GitHub; main's run on the merge commit does not start.
