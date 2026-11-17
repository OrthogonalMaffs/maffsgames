LANE: cloud (Claude Code on the web). SEND: now, BEFORE ANSWER-BOX-TEXT (Jon, 17 Nov 2026, 12:49: "pop the image in there before we move onto the next contract"). ANSWER-BOX-TEXT follows when this has merged.
RECOMMENDED: Opus 5.5, high effort. One game page plus one asset, but the Level 3 bank is replaced and the worked examples need correct KaTeX and a link from the feedback.

TASK: ITS-A-SINE-POLISH. On It's a SINE!! (games/its-a-sine/), on main b93078b:
- add Jon's start picture;
- add four worked examples (one per version), shown on the start screen and linked from the Stage 2 and Stage 3 feedback;
- change the All three stage marker from "∗" to "All";
- correct level4_034's units from m to mm;
- REPLACE the whole Level 3 bank (40 items) with the 40 below, matched to Jon's Level 3 assessment.

ROOT CAUSE: #810 shipped without the start picture (it wasn't made until 17 Nov) and without worked examples (Jon asked for them on 17 Nov). Its All three button shows "∗" (index.html:201, <span class="n">∗</span>), which reads as a footnote. level4_034's prompt gives a frame's members as "380 m and 520 m ... 450 m": these are millimetre sizes (Project Claude's slip in the bank). The angle is unchanged.

CLASS CHECK: Local. The start picture follows the existing site pattern (ESSENTIALS-ART: assets/start.webp, the .start-art rule, the img in the start screen; see games/just-pythag-it-bruv/index.html:172-174 and :214), so no new mechanism. The worked examples and the marker are this game's own content. The units fix is one prompt string. The Level 3 bank is content: it was written without checking Jon's Level 3 course (Project Claude's error). Jon's Level 3 assessment has exactly two question types (17 Nov 2026, 12:52, "these are the ONLY 2 questions in their assessment"): the cosine rule for a side (two sides and the included angle, mm, formula given) and the sine rule for an angle (two sides and an angle opposite one of them, a steel bracket, mm). The new bank is those two types only: no bearings, no lighthouses, no ambiguous case, no third-angle-first.

JON'S DECISIONS, 17 Nov 2026 (verbatim in the PR body):
- 10:48: "how about an image for the front screen? and a worked example for each rule ... something that is obviously NOT a right angle".
- 11:16: "4 works examples is fine".
- 12:49: the image goes in before the next contract.
- 12:51: "what the hell is this ? I think someone has very little idea of what the students at level 3 on my course are required to know." (a Level 3 bearings item).
- 12:55: "yes please, and bundle in the image to that same contract please." (to: Level 3 rebuilt as 20 cosine-rule-side and 20 sine-rule-angle items on components in mm, the given angle always opposite the longer side so there is one answer).

EXACT CHANGE:
0. First commit: the close-outs of #810 SINE-NOT-SINE (f5df4b9; check-site 44078857846 green, phone-fit-full 44078857810 red, fixed by #811) and #811 ITS-A-SINE-PHONE-FIT (313376d; check-site 44084244178, phone-fit-full 44084244189, both green), per AGENTS.md's close-out rule.

1. Start picture.
   - Branch art/its-a-sine (commit 8530e03, "Add files via upload") holds start.webp at the REPO ROOT: 1600 x 873 WebP, 163,702 bytes, already converted by Project Claude.
   - Copy it as-is (no re-encode) to games/its-a-sine/assets/start.webp. Confirm its size is 1600 x 873. Do not merge or rebase the art branch; take only the file.
   - Insert <img class="start-art" src="assets/start.webp" width="1600" height="873" alt="A building site with roof trusses being built and a mobile crane lifting timber, every triangle slanted"> immediately after the .header div in #menu (index.html:187).
   - Add the .start-art rule and its max-height:600px rule exactly as Just Pythag It Bruv's (:172-174), with the same comments.

2. Worked examples.
   - Add a "Worked examples" section on the start screen, below the stage list: four collapsed <details> items, one per version, KaTeX for every expression (canon §7.1.1), in this order, verbatim:
     A. Sine rule, finding a side. A = 50°, B = 70°, a = 10 cm. Find b.
        Two angles and a side: it's a SINE.
        \frac{b}{\sin 70^\circ} = \frac{10}{\sin 50^\circ}, so b = \frac{10 \sin 70^\circ}{\sin 50^\circ} = 12.266\ldots = 12.3 cm.
     B. Sine rule, finding an angle. a = 12 cm, b = 8 cm, A = 70°. Find B.
        Two sides and an angle opposite one of them: it's a SINE.
        \frac{\sin B}{8} = \frac{\sin 70^\circ}{12}, so \sin B = \frac{8 \sin 70^\circ}{12} = 0.62646\ldots, B = 38.8°.
     C. Cosine rule, finding a side. b = 9 cm, c = 11 cm, A = 50°. Find a.
        Two sides and the angle between them: no, it's not.
        a^2 = 9^2 + 11^2 - 2 \times 9 \times 11 \times \cos 50^\circ = 202 - 127.271\ldots = 74.728\ldots, so a = 8.6 cm.
     D. Cosine rule, finding an angle. a = 8 cm, b = 9 cm, c = 12 cm. Find A.
        All three sides: no, it's not.
        \cos A = \frac{9^2 + 12^2 - 8^2}{2 \times 9 \times 12} = \frac{161}{216} = 0.74537\ldots, so A = 41.8°.
   - Each example gets a small triangle diagram drawn to its true shape, the same way the game draws its questions, labelled with only the given values and the unknown.
   - In Stage 2 and Stage 3 feedback (and the matching steps of All three), after a wrong answer, add a link "See the worked example", which opens that item's version: sine-side → A, sine-angle → B, cosine-side → C, cosine-angle → D. It opens in place, as an expandable panel, without leaving the run.
   - None of these four triangles is in the bank. Do not add them to QUESTIONS.

3. All three marker: <span class="n">∗</span> → <span class="n">All</span>, sized so it fits the same circle; if it does not fit at 320 px, use "A".

4. level4_034 prompt only: "A triangular frame has members of 380 mm and 520 mm meeting at joint A, and a member of 450 mm opposite A. Find the angle at A, to 1 d.p." given, find, answer (57.5), unit "°" and id unchanged.

4b. Replace QUESTIONS.level3 entirely with these 40 items, verbatim (one per line; answers to 1 d.p., recomputed by Project Claude by coordinate geometry; every sine-angle item has exactly one triangle because a > b):
{"id":"level3_001","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":84,"c":52,"A":112},"find":"a","answer":114.2,"unit":"mm","prompt":"A steel bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_002","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":80,"c":95,"A":35},"find":"a","answer":54.5,"unit":"mm","prompt":"A shelf bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_003","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":50,"c":120,"A":62},"find":"a","answer":106.1,"unit":"mm","prompt":"A triangular brace (not to scale). Find side a, to 1 d.p."}
{"id":"level3_004","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":75,"c":60,"A":48},"find":"a","answer":56.6,"unit":"mm","prompt":"A mounting plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_005","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":110,"c":90,"A":70},"find":"a","answer":115.9,"unit":"mm","prompt":"A jig plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_006","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":36,"c":58,"A":75},"find":"a","answer":59.8,"unit":"mm","prompt":"A frame corner plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_007","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":95,"c":140,"A":28},"find":"a","answer":71.7,"unit":"mm","prompt":"A sheet-metal blank (not to scale). Find side a, to 1 d.p."}
{"id":"level3_008","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":64,"c":72,"A":105},"find":"a","answer":108.0,"unit":"mm","prompt":"A support bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_009","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":40,"c":55,"A":118},"find":"a","answer":81.8,"unit":"mm","prompt":"A linkage plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_010","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":130,"c":85,"A":44},"find":"a","answer":90.7,"unit":"mm","prompt":"A steel bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_011","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":72,"c":48,"A":66},"find":"a","answer":68.4,"unit":"mm","prompt":"A gusset plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_012","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":88,"c":105,"A":52},"find":"a","answer":86.0,"unit":"mm","prompt":"A shelf bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_013","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":66,"c":44,"A":97},"find":"a","answer":83.7,"unit":"mm","prompt":"A jig plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_014","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":150,"c":110,"A":58},"find":"a","answer":130.8,"unit":"mm","prompt":"A frame corner plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_015","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":48,"c":64,"A":82},"find":"a","answer":74.5,"unit":"mm","prompt":"A sheet-metal blank (not to scale). Find side a, to 1 d.p."}
{"id":"level3_016","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":90,"c":75,"A":124},"find":"a","answer":145.9,"unit":"mm","prompt":"A support bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_017","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":100,"c":125,"A":46},"find":"a","answer":90.9,"unit":"mm","prompt":"A linkage plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_018","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":58,"c":82,"A":71},"find":"a","answer":83.6,"unit":"mm","prompt":"A steel bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_019","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":140,"c":96,"A":36},"find":"a","answer":84.1,"unit":"mm","prompt":"A gusset plate (not to scale). Find side a, to 1 d.p."}
{"id":"level3_020","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":70,"c":115,"A":88},"find":"a","answer":132.5,"unit":"mm","prompt":"A shelf bracket (not to scale). Find side a, to 1 d.p."}
{"id":"level3_021","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":120,"b":90,"A":55},"find":"B","answer":37.9,"unit":"°","prompt":"A mounting plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_022","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":95,"b":70,"A":65},"find":"B","answer":41.9,"unit":"°","prompt":"A jig plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_023","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":150,"b":110,"A":48},"find":"B","answer":33.0,"unit":"°","prompt":"A frame corner plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_024","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":75,"b":55,"A":82},"find":"B","answer":46.6,"unit":"°","prompt":"A sheet-metal blank (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_025","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":140,"b":100,"A":60},"find":"B","answer":38.2,"unit":"°","prompt":"A support bracket (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_026","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":68,"b":50,"A":77},"find":"B","answer":45.8,"unit":"°","prompt":"A linkage plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_027","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":110,"b":95,"A":58},"find":"B","answer":47.1,"unit":"°","prompt":"A steel bracket (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_028","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":90,"b":64,"A":46},"find":"B","answer":30.8,"unit":"°","prompt":"A gusset plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_029","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":100,"b":75,"A":52},"find":"B","answer":36.2,"unit":"°","prompt":"A triangular brace (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_030","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":58,"b":42,"A":88},"find":"B","answer":46.4,"unit":"°","prompt":"A mounting plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_031","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":125,"b":96,"A":63},"find":"B","answer":43.2,"unit":"°","prompt":"A jig plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_032","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":80,"b":72,"A":95},"find":"B","answer":63.7,"unit":"°","prompt":"A frame corner plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_033","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":72,"b":50,"A":104},"find":"B","answer":42.4,"unit":"°","prompt":"A support bracket (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_034","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":105,"b":78,"A":57},"find":"B","answer":38.5,"unit":"°","prompt":"A linkage plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_035","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":62,"b":45,"A":67},"find":"B","answer":41.9,"unit":"°","prompt":"A steel bracket (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_036","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":145,"b":120,"A":74},"find":"B","answer":52.7,"unit":"°","prompt":"A gusset plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_037","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":88,"b":66,"A":49},"find":"B","answer":34.5,"unit":"°","prompt":"A shelf bracket (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_038","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":98,"b":70,"A":85},"find":"B","answer":45.4,"unit":"°","prompt":"A triangular brace (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_039","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":135,"b":100,"A":43},"find":"B","answer":30.3,"unit":"°","prompt":"A mounting plate (not to scale). Find angle B, to 1 d.p."}
{"id":"level3_040","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":76,"b":60,"A":110},"find":"B","answer":47.9,"unit":"°","prompt":"A jig plate (not to scale). Find angle B, to 1 d.p."}
   - Diagrams: the plain-triangle drawing the game already uses for GCSE items with the same "given" keys ({b, c, A} and {a, b, A}), labelled with only the given values and the unknown. No context drawing.
   - Stage 1's reason lines already cover both patterns (two sides and the included angle; two sides and an angle opposite one of them).
   - The Level 3 leaderboard boards stay as they are.

5. scripts/verify-its-a-sine.py:
   - Recompute each worked example's printed values independently: 12.266… → 12.3; 0.62646… → 38.8°; 127.271…, 74.728… → 8.6; 161/216 = 0.74537… → 41.8°. Each \ldots value must be a truncation, not a rounding, of the true value.
   - Assert each link opens the right example (version → letter).
   - Assert the start picture is present with width and height.
   - Assert level4_034's prompt says mm.
   - Level 3: recompute all 40 new items independently; assert exactly 20 cosine-side and 20 sine-angle, and no item with bearings, ambiguous or third_angle_first; every sine-angle item has exactly one triangle.
   - Plants: a wrong worked-example answer, and a feedback link opening the wrong example. Each must fail.

6. docs/handover/cloud.md entry. No /updates/ line (the game is unlisted).

7. Merge with scripts/merge-pr.py when the Gate is green.

DO NOT TOUCH:
- Every GCSE and Level 4 bank item, and level4_034's numbers, answer and id (only its prompt changes).
- Stage logic, scoring, the leaderboard boards and labels, colours, the calculator map.
- Any other game, schools/assets/, canon.
- The art/its-a-sine branch (do not delete, merge or change it).
- No draft PR.

SUCCESS CONDITION:
- On main, /games/its-a-sine/ shows the picture under the title.
- Four worked examples open on the start screen with correct KaTeX and diagrams.
- A wrong Stage 2 or 3 answer offers the matching example.
- All three's marker reads "All" (or "A"), fitting at 320 px.
- level4_034 says mm.
- Level 3 serves only the 40 new items (20 cosine-side, 20 sine-angle).
- The verifier passes with its new plants failing; phone-fit, answer-lock and check-theme pass.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover committed.

STOP IF:
- start.webp on the art branch is not 1600 x 873, or is missing.
- A worked example's or a Level 3 item's value disagrees with your independent recomputation (report the id and both values).
- The picture pushes the first stage button below the fold at 375 x 667 when it was above it before (report both measurements).
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

AMENDMENT 1 (Jon, 17 Nov 2026, after the STOP IF 3 report), verbatim:

1. PICTURE: keep it under the title, as the contract says. Waive STOP IF 3 for the first stage button; the level buttons must stay above the fold at 375 × 667 (record their measured top/bottom in the handover).

2. UNITS: yes, include the drawing fix. At games/its-a-sine/index.html:606 replace the hard-coded `frame ? 'm' : 'cm'` with: the question's own unit when it is a length unit; else the length unit in its prompt; else its level's unit. Do NOT change how kindOf (line 432) decides frame vs plain: frame detection must give the same result for every existing item. The verifier checks every drawn label's unit against the same rule. Success adds: every Level 3 drawing shows mm, level4_034 shows mm, and every other item's labels are unchanged (list any that change and why).

Then finish the rest of the contract as written, open the PR and merge on green.
