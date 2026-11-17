LANE: cloud (Claude Code on the web). SEND: now (HEATWAVE-APPROVE merged as #809). This jumps the queue ahead of ANSWER-BOX-TEXT (Jon, 17 Nov 2026).
RECOMMENDED: Opus 5.5, high effort. A new staged game with three tiers, drawn diagrams, a 120-item bank and a verifier.

TASK: SINE-NOT-SINE. Build a new game, "It's a SINE!!" / "No it's not" (slug its-a-sine), on the sine and cosine rules, for GCSE Higher, Level 3 and Level 4.
- It has three stages: 1, choose the rule; 2, choose the version; 3, solve.
- It has an "All three" run.
- Merge it UNLISTED, so Jon can play it and use it with his class by URL.

ROOT CAUSE: There is no sine and cosine rule game. Trig Identity Duel has a handful of items. Jon is teaching it to his Level 3 class now, and asked for it on 17 Nov 2026.

CLASS CHECK: A new build, not a fix. It reuses the shared layers and duplicates none of them:
- MaffsLevel.resolve, options.js, the fold components, MaffsLock, MaffsAnswer.decimal, the calculator by stage, MaffsLeaderboard and the theme.
- It ships checked (canon SR-30): its verifier runs in CI in this PR, it is in every shared check's MIGRATED lists, and it has a findings file docs/audits/findings/its-a-sine.yml.
- Pattern to follow: games/cast-away/index.html. It is a staged L3 trig game whose stages are leaderboard boards, and it was merged unlisted for Jon to play.

JON'S DECISIONS, 17 Nov 2026 (record verbatim in the PR body):
- Name: "It's a SINE !!" "No it's not". The first quote in one colour, the second in another.
- "stage 1, a diagram and you just need to choose sine rule or cosine rule, then you need to choose which VERSION of the equation to use, then you have to actually solve, including resolving the missing angle to use the sine rule."
- "3 stages please"
- "should be level 3 and 4, and GCSE (higher)"
- Colours: the site's teal for "It's a SINE!!" and a warm coral for "No it's not" ("yes they're fine"). Pick a coral that passes 4.5:1 contrast on the dark background.

EXACT CHANGE:
0. First commit: the close-out of #809 HEATWAVE-APPROVE per AGENTS.md's close-out rule: merge commit 862f7a6; main check-site 44057701420 and phone-fit-full 44057701474, both success; the contract to docs/history/contracts/.

1. games/its-a-sine/index.html: one page on the shared assets.
   - Dark GCSE theme (canon §7.5.1: the lowest tier served is GCSE), Outfit + JetBrains Mono.
   - Title in two parts: "It's a SINE!!" in teal, then "No it's not" in coral.
   - Levels: MaffsLevel.resolve({slug: 'its-a-sine', levels: ['gcse', 'level3', 'level4'], fallback: 'gcse'}), with a level picker.
   - Each level's QUESTIONS[level] holds its 40 items from the bank below, verbatim.

2. Stages, keyed stage-1, stage-2, stage-3 and all-three. Each run is 10 items drawn from the level's 40, with no repeat within a run.
   - Stage 1 ("Which rule?"). Show the diagram and the item's prompt. Two buttons:
     - "It's a SINE!!" (teal): the sine rule.
     - "No it's not" (coral): the cosine rule.
     The key is the item's "rule". After the answer, show one line of reason, chosen by what is given:
     - two angles and a side: "Two angles and a side: pair each side with its opposite angle. Sine rule."
     - two sides and a non-included angle: "Two sides and an angle opposite one of them: sine rule."
     - two sides and the included angle: "Two sides and the angle between them: cosine rule."
     - three sides: "All three sides: cosine rule."
     For context items, derive the pattern from the triangle the context forms.
   - Stage 2 ("Which version?"). Show the same diagram. Four buttons, in KaTeX, matched by dataset.val: sine-side, sine-angle, cosine-side, cosine-angle.
     - sine-side: \frac{a}{\sin A} = \frac{b}{\sin B}
     - sine-angle: \frac{\sin A}{a} = \frac{\sin B}{b}
     - cosine-side: a^2 = b^2 + c^2 - 2bc\cos A
     - cosine-angle: \cos A = \frac{b^2 + c^2 - a^2}{2bc}
     The key is the item's "version". The reason line says that a side on top is used to find a side, and the rearranged form is used to find an angle.
   - Stage 3 ("Solve it"). A typed answer marked by MaffsAnswer.decimal(raw, answer, 1). The answer box is type="text", never type="number". Unit shown beside the box.
     After the answer, show the working, worked from "given":
     - "third_angle_first" items show the missing angle first (180° minus the other two; for exterior-angle items, 180° minus the exterior angle).
     - bearings items show the angle at the turn ("working").
     - force and phasor items show "the triangle's angle is 180° − the angle between them" ("working.triangle_angle"). This is the classic slip, and the working names it.
     - "ambiguous" items show both solutions of sin B, and which one is obtuse.
   - All three: each item goes through stages 1, 2 and 3 in turn. A wrong step shows its reason and the run moves on to the next step with the correct choice shown.
   - Calculator by stage (canon "by stage", CALC-BY-STAGE): {"stage-1": "not allowed", "stage-2": "not allowed", "stage-3": "scientific", "all-three": "scientific"}.
   - Leaderboard: each stage is a board under each level, as in Cast Away. Submit only at a run's end (completion rule).

3. Diagrams: inline SVG, drawn TO THE TRUE SHAPE from "given", by computing the triangle's coordinates (canon "If it cannot be drawn honestly, do not draw it").
   - Label only what the prompt gives. Mark the unknown x (a side) or θ (an angle).
   - Plain triangles: vertices A, B and C, with sides a, b and c opposite them.
   - Exterior-angle items: extend CB beyond B and mark the exterior angle.
   - Ambiguous items: draw the obtuse case.
   - Bearings: a north line at each point, the two legs, and the closing line dashed.
   - Lighthouse items: A, B and L with north lines.
   - Forces and phasors: two arrows from a point with the angle between them, and the resultant dashed and marked ?. Force-direction items: the triangle of forces with α marked.
   - Crank: the crank, the rod and the line of stroke, with φ marked.
   - Survey: the baseline AB and the mast P.
   - Frames: a triangle of members with the joint A.
   - Never mark a derived value, such as the triangle's angle or the third angle, before the student answers.
   - Every diagram fits phone-fit at 360 px wide.

4. scripts/verify-its-a-sine.py, in CI, with --selftest.
   - Every item's "answer" is recomputed by a second, independent route: coordinate geometry or vector addition, not the formula the game uses.
   - Every item's "rule" and "version" match its given pattern.
   - Every "ambiguous" item has two valid triangles, and every other sine-angle item has one.
   - No answer lies within 0.005 of a 1 d.p. rounding boundary.
   - 40 items per level, with ids unique.
   - In play: each stage marks its key and only its key, the calculator mounts in stage 3 and all-three only, and the header badge follows the stage.
   - Plants that must fail:
     - an answer 0.1 out;
     - a rule swapped;
     - a version swapped;
     - an ambiguous item with only one solution;
     - a stage-1 key read from the rendered HTML instead of dataset.val.

5. Integration, each as the repo already does it for a new game:
   - .claude/rules/game-roster.md row: levels GCSE, L3, L4; topic Geometry; calculator "by stage"; "3 stages, 120 questions (40 per level)".
   - data/games.json entry with listing off (unlisted), then apply-meta.py and check-meta.py.
   - The findings file.
   - The MIGRATED lists.
   - The leaderboard hub registry.
   - /updates/: no line while unlisted.
   - docs/todo.md row ITS-A-SINE-LIST: Jon plays all three stages at each level, then rules on listing.
   - docs/handover/cloud.md.

6. Merge with scripts/merge-pr.py when the Gate is green. That is the only merge route.

THE BANK (verbatim; one item per line; ids give the level: gcse_, level3_, level4_; answers are to 1 d.p., independently recomputed by Project Claude by coordinate geometry; "unit" "°" means an angle):
{"id":"gcse_001","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":40,"B":65,"a":8},"find":"b","answer":11.3,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_002","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":35,"B":80,"a":12},"find":"b","answer":20.6,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_003","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":52,"B":71,"a":9.5},"find":"b","answer":11.4,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_004","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":28,"B":63,"a":15},"find":"b","answer":28.5,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_005","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":47,"B":58,"a":6.4},"find":"b","answer":7.4,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_006","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":61,"B":44,"a":11},"find":"b","answer":8.7,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_007","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":33,"B":72,"a":7.8},"find":"b","answer":13.6,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_008","rule":"sine","version":"sine-side","third_angle_first":false,"given":{"A":55,"B":38,"a":14},"find":"b","answer":10.5,"unit":"cm","prompt":"Find side b, to 1 d.p."}
{"id":"gcse_009","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":48,"B":67,"a":10},"find":"c","answer":12.2,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_010","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":41,"B":82,"a":12},"find":"c","answer":15.3,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_011","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":66,"B":49,"a":9},"find":"c","answer":8.9,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_012","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":29,"B":57,"a":16},"find":"c","answer":32.9,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_013","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":53,"B":64,"a":7.5},"find":"c","answer":8.4,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_014","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":44,"B":46,"a":11.2},"find":"c","answer":16.1,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_015","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":39,"B":71,"a":12},"find":"c","answer":17.9,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_016","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":57,"B":48,"a":10.4},"find":"c","answer":12.0,"unit":"cm","prompt":"Find side c, to 1 d.p."}
{"id":"gcse_017","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":12,"b":9,"A":64},"find":"B","answer":42.4,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_018","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":15,"b":11,"A":72},"find":"B","answer":44.2,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_019","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":9,"b":7.2,"A":81},"find":"B","answer":52.2,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_020","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":14,"b":10,"A":47},"find":"B","answer":31.5,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_021","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":13,"b":12,"A":66},"find":"B","answer":57.5,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_022","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":8.4,"b":6,"A":75},"find":"B","answer":43.6,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_023","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":11,"b":7.5,"A":53},"find":"B","answer":33.0,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_024","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":16,"b":13,"A":68},"find":"B","answer":48.9,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"gcse_025","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":7,"c":9,"A":48},"find":"a","answer":6.8,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_026","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":12,"c":10,"A":65},"find":"a","answer":11.9,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_027","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":8.5,"c":11,"A":37},"find":"a","answer":6.6,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_028","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":15,"c":13,"A":82},"find":"a","answer":18.4,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_029","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":10,"c":14,"A":123},"find":"a","answer":21.2,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_030","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":13,"c":16,"A":71},"find":"a","answer":17.0,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_031","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":11,"c":8,"A":62},"find":"a","answer":10.1,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_032","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":14,"c":12,"A":105},"find":"a","answer":20.7,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"gcse_033","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":9,"b":7,"c":8},"find":"A","answer":73.4,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_034","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":15,"b":11,"c":13},"find":"A","answer":76.9,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_035","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":6,"b":8,"c":9},"find":"A","answer":40.8,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_036","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":14,"b":9,"c":10},"find":"A","answer":94.8,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_037","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":10,"b":13,"c":15},"find":"A","answer":41.1,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_038","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":7.5,"b":6,"c":8},"find":"A","answer":62.9,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_039","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":11,"b":12,"c":5},"find":"A","answer":66.4,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"gcse_040","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":13,"b":8,"c":11},"find":"A","answer":84.8,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_001","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":42,"B_exterior":118,"a":9},"find":"b","answer":11.9,"unit":"cm","prompt":"The angle on the straight line at B is 118°. Find side b, to 1 d.p."}
{"id":"level3_002","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":37,"B_exterior":103,"a":12},"find":"b","answer":19.4,"unit":"cm","prompt":"The angle on the straight line at B is 103°. Find side b, to 1 d.p."}
{"id":"level3_003","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":55,"B_exterior":131,"a":8.5},"find":"b","answer":7.8,"unit":"cm","prompt":"The angle on the straight line at B is 131°. Find side b, to 1 d.p."}
{"id":"level3_004","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":48,"B_exterior":96,"a":14},"find":"b","answer":18.7,"unit":"cm","prompt":"The angle on the straight line at B is 96°. Find side b, to 1 d.p."}
{"id":"level3_005","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":33,"B_exterior":124,"a":10.6},"find":"b","answer":16.1,"unit":"cm","prompt":"The angle on the straight line at B is 124°. Find side b, to 1 d.p."}
{"id":"level3_006","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"A":61,"B_exterior":112,"a":7.4},"find":"b","answer":7.8,"unit":"cm","prompt":"The angle on the straight line at B is 112°. Find side b, to 1 d.p."}
{"id":"level3_007","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":16,"b":12,"A":71},"find":"B","answer":45.2,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"level3_008","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":9.8,"b":7,"A":62},"find":"B","answer":39.1,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"level3_009","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":13,"b":9.5,"A":54},"find":"B","answer":36.2,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"level3_010","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":20,"b":17,"A":77},"find":"B","answer":55.9,"unit":"°","prompt":"Find angle B, to 1 d.p."}
{"id":"level3_011","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":8,"b":11,"A":38},"find":"B","answer":122.2,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_012","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":10,"b":13,"A":42},"find":"B","answer":119.6,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_013","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":7,"b":9.5,"A":35},"find":"B","answer":128.9,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_014","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":9,"b":12.4,"A":40},"find":"B","answer":117.7,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_015","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":6.5,"b":8,"A":46},"find":"B","answer":117.7,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_016","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":13,"b":16,"A":52},"find":"B","answer":104.1,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_017","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":9.5,"b":12,"A":44},"find":"B","answer":118.7,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_018","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":14,"b":18,"A":41},"find":"B","answer":122.5,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
{"id":"level3_019","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":11,"c":14,"A":58},"find":"a","answer":12.4,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"level3_020","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":9.5,"c":12,"A":104},"find":"a","answer":17.0,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"level3_021","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":16,"c":13,"A":77},"find":"a","answer":18.2,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"level3_022","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":7.8,"c":10,"A":131},"find":"a","answer":16.2,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"level3_023","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":18,"c":21,"A":43},"find":"a","answer":14.6,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"level3_024","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":15,"c":10,"A":84},"find":"a","answer":17.1,"unit":"cm","prompt":"Find side a, to 1 d.p."}
{"id":"level3_025","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":17,"b":12,"c":14},"find":"A","answer":81.3,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_026","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":21,"b":15,"c":18},"find":"A","answer":78.5,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_027","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":19,"b":11,"c":13},"find":"A","answer":104.4,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_028","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":14,"b":17,"c":6},"find":"A","answer":50.8,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_029","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":16,"b":10,"c":9},"find":"A","answer":114.6,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_030","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":22,"b":18,"c":13},"find":"A","answer":88.9,"unit":"°","prompt":"Find angle A, to 1 d.p."}
{"id":"level3_031","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"leg1_km":12,"bearing1":50,"leg2_km":9,"bearing2":130},"find":"distance","answer":16.2,"unit":"km","prompt":"A boat sails 12 km on a bearing of 050°, then 9 km on a bearing of 130°. How far is it from its start, to 1 d.p.?","working":{"angle_at_turn":100}}
{"id":"level3_032","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"leg1_km":15,"bearing1":30,"leg2_km":11,"bearing2":145},"find":"distance","answer":14.4,"unit":"km","prompt":"A boat sails 15 km on a bearing of 030°, then 11 km on a bearing of 145°. How far is it from its start, to 1 d.p.?","working":{"angle_at_turn":65}}
{"id":"level3_033","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"leg1_km":8,"bearing1":70,"leg2_km":14,"bearing2":160},"find":"distance","answer":16.1,"unit":"km","prompt":"A boat sails 8 km on a bearing of 070°, then 14 km on a bearing of 160°. How far is it from its start, to 1 d.p.?","working":{"angle_at_turn":90}}
{"id":"level3_034","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"leg1_km":20,"bearing1":40,"leg2_km":13,"bearing2":110},"find":"distance","answer":27.3,"unit":"km","prompt":"A boat sails 20 km on a bearing of 040°, then 13 km on a bearing of 110°. How far is it from its start, to 1 d.p.?","working":{"angle_at_turn":110}}
{"id":"level3_035","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"leg1_km":10,"bearing1":15,"leg2_km":16,"bearing2":95},"find":"distance","answer":20.3,"unit":"km","prompt":"A boat sails 10 km on a bearing of 015°, then 16 km on a bearing of 095°. How far is it from its start, to 1 d.p.?","working":{"angle_at_turn":100}}
{"id":"level3_036","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"leg1_km":18,"bearing1":60,"leg2_km":7,"bearing2":170},"find":"distance","answer":16.9,"unit":"km","prompt":"A boat sails 18 km on a bearing of 060°, then 7 km on a bearing of 170°. How far is it from its start, to 1 d.p.?","working":{"angle_at_turn":70}}
{"id":"level3_037","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_km":12,"bearing_A_to_L":30,"bearing_A_to_B":100,"bearing_B_to_L":350},"find":"BL","answer":17.5,"unit":"km","prompt":"From A, a lighthouse L is on a bearing of 030°. A boat sails 12 km from A to B on a bearing of 100°. From B, L is on a bearing of 350°. Find the distance BL, to 1 d.p.","working":{"angle_A":70,"angle_B":70,"angle_L":40}}
{"id":"level3_038","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_km":8,"bearing_A_to_L":60,"bearing_A_to_B":120,"bearing_B_to_L":10},"find":"BL","answer":9.0,"unit":"km","prompt":"From A, a lighthouse L is on a bearing of 060°. A boat sails 8 km from A to B on a bearing of 120°. From B, L is on a bearing of 010°. Find the distance BL, to 1 d.p.","working":{"angle_A":60,"angle_B":70,"angle_L":50}}
{"id":"level3_039","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_km":14,"bearing_A_to_L":20,"bearing_A_to_B":80,"bearing_B_to_L":320},"find":"BL","answer":14.0,"unit":"km","prompt":"From A, a lighthouse L is on a bearing of 020°. A boat sails 14 km from A to B on a bearing of 080°. From B, L is on a bearing of 320°. Find the distance BL, to 1 d.p.","working":{"angle_A":60,"angle_B":60,"angle_L":60}}
{"id":"level3_040","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_km":15,"bearing_A_to_L":25,"bearing_A_to_B":85,"bearing_B_to_L":315},"find":"BL","answer":13.8,"unit":"km","prompt":"From A, a lighthouse L is on a bearing of 025°. A boat sails 15 km from A to B on a bearing of 085°. From B, L is on a bearing of 315°. Find the distance BL, to 1 d.p.","working":{"angle_A":60,"angle_B":50,"angle_L":70}}
{"id":"level4_001","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"F1":40,"F2":25,"angle_between":60},"find":"R","answer":56.8,"unit":"N","prompt":"Forces of 40 N and 25 N act at a point with 60° between them. Find the magnitude of the resultant, to 1 d.p.","working":{"triangle_angle":120}}
{"id":"level4_002","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"F1":120,"F2":85,"angle_between":45},"find":"R","answer":189.9,"unit":"N","prompt":"Forces of 120 N and 85 N act at a point with 45° between them. Find the magnitude of the resultant, to 1 d.p.","working":{"triangle_angle":135}}
{"id":"level4_003","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"F1":18,"F2":30,"angle_between":75},"find":"R","answer":38.8,"unit":"N","prompt":"Forces of 18 N and 30 N act at a point with 75° between them. Find the magnitude of the resultant, to 1 d.p.","working":{"triangle_angle":105}}
{"id":"level4_004","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"F1":250,"F2":180,"angle_between":110},"find":"R","answer":253.2,"unit":"N","prompt":"Forces of 250 N and 180 N act at a point with 110° between them. Find the magnitude of the resultant, to 1 d.p.","working":{"triangle_angle":70}}
{"id":"level4_005","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"V1":230,"V2":110,"phase":30},"find":"V","answer":329.9,"unit":"V","prompt":"Two sinusoidal voltages of peak 230 V and 110 V have a phase difference of 30°. Find the peak of their sum, to 1 d.p.","working":{"triangle_angle":150}}
{"id":"level4_006","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"V1":12,"V2":8,"phase":60},"find":"V","answer":17.4,"unit":"V","prompt":"Two sinusoidal voltages of peak 12 V and 8 V have a phase difference of 60°. Find the peak of their sum, to 1 d.p.","working":{"triangle_angle":120}}
{"id":"level4_007","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"V1":48,"V2":36,"phase":90},"find":"V","answer":60.0,"unit":"V","prompt":"Two sinusoidal voltages of peak 48 V and 36 V have a phase difference of 90°. Find the peak of their sum, to 1 d.p.","working":{"triangle_angle":90}}
{"id":"level4_008","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"V1":5.5,"V2":3.2,"phase":120},"find":"V","answer":4.8,"unit":"V","prompt":"Two sinusoidal voltages of peak 5.5 V and 3.2 V have a phase difference of 120°. Find the peak of their sum, to 1 d.p.","working":{"triangle_angle":60}}
{"id":"level4_009","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"F1":120,"F2":85,"R":190},"find":"alpha","answer":18.4,"unit":"°","prompt":"Two forces of 120 N and 85 N have a resultant of 190 N. Find the angle between the resultant and the 120 N force, to 1 d.p."}
{"id":"level4_010","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"F1":300,"F2":220,"R":480},"find":"alpha","answer":19.2,"unit":"°","prompt":"Two forces of 300 N and 220 N have a resultant of 480 N. Find the angle between the resultant and the 300 N force, to 1 d.p."}
{"id":"level4_011","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"F1":65,"F2":65,"R":110},"find":"alpha","answer":32.2,"unit":"°","prompt":"Two forces of 65 N and 65 N have a resultant of 110 N. Find the angle between the resultant and the 65 N force, to 1 d.p."}
{"id":"level4_012","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"F1":250,"F2":180,"R":300},"find":"alpha","answer":36.8,"unit":"°","prompt":"Two forces of 250 N and 180 N have a resultant of 300 N. Find the angle between the resultant and the 250 N force, to 1 d.p."}
{"id":"level4_013","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"F1":90,"F2":40,"R":105},"find":"alpha","answer":22.0,"unit":"°","prompt":"Two forces of 90 N and 40 N have a resultant of 105 N. Find the angle between the resultant and the 90 N force, to 1 d.p."}
{"id":"level4_014","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"F1":75,"F2":50,"R":110},"find":"alpha","answer":22.7,"unit":"°","prompt":"Two forces of 75 N and 50 N have a resultant of 110 N. Find the angle between the resultant and the 75 N force, to 1 d.p."}
{"id":"level4_015","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":75,"rod_mm":300,"crank_angle":65},"find":"phi","answer":13.1,"unit":"°","prompt":"A crank of 75 mm drives a connecting rod of 300 mm. The crank is 65° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_016","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":50,"rod_mm":180,"crank_angle":120},"find":"phi","answer":13.9,"unit":"°","prompt":"A crank of 50 mm drives a connecting rod of 180 mm. The crank is 120° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_017","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":90,"rod_mm":350,"crank_angle":30},"find":"phi","answer":7.4,"unit":"°","prompt":"A crank of 90 mm drives a connecting rod of 350 mm. The crank is 30° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_018","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":80,"rod_mm":280,"crank_angle":55},"find":"phi","answer":13.5,"unit":"°","prompt":"A crank of 80 mm drives a connecting rod of 280 mm. The crank is 55° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_019","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":100,"rod_mm":420,"crank_angle":75},"find":"phi","answer":13.3,"unit":"°","prompt":"A crank of 100 mm drives a connecting rod of 420 mm. The crank is 75° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_020","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":45,"rod_mm":200,"crank_angle":140},"find":"phi","answer":8.3,"unit":"°","prompt":"A crank of 45 mm drives a connecting rod of 200 mm. The crank is 140° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_021","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":70,"rod_mm":260,"crank_angle":85},"find":"phi","answer":15.6,"unit":"°","prompt":"A crank of 70 mm drives a connecting rod of 260 mm. The crank is 85° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_022","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":55,"rod_mm":220,"crank_angle":110},"find":"phi","answer":13.6,"unit":"°","prompt":"A crank of 55 mm drives a connecting rod of 220 mm. The crank is 110° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_023","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"crank_mm":85,"rod_mm":330,"crank_angle":50},"find":"phi","answer":11.4,"unit":"°","prompt":"A crank of 85 mm drives a connecting rod of 330 mm. The crank is 50° from the line of stroke. Find the angle the rod makes with the line of stroke, to 1 d.p."}
{"id":"level4_024","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":120,"angle_A":52,"angle_B":63},"find":"AP","answer":118.0,"unit":"m","prompt":"A surveyor's baseline AB is 120 m. At A, the angle between the baseline and a mast P is 52°; at B it is 63°. Find AP, to 1 d.p."}
{"id":"level4_025","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":85,"angle_A":48,"angle_B":71},"find":"AP","answer":91.9,"unit":"m","prompt":"A surveyor's baseline AB is 85 m. At A, the angle between the baseline and a mast P is 48°; at B it is 71°. Find AP, to 1 d.p."}
{"id":"level4_026","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":200,"angle_A":35,"angle_B":80},"find":"AP","answer":217.3,"unit":"m","prompt":"A surveyor's baseline AB is 200 m. At A, the angle between the baseline and a mast P is 35°; at B it is 80°. Find AP, to 1 d.p."}
{"id":"level4_027","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":150,"angle_A":66,"angle_B":58},"find":"AP","answer":153.4,"unit":"m","prompt":"A surveyor's baseline AB is 150 m. At A, the angle between the baseline and a mast P is 66°; at B it is 58°. Find AP, to 1 d.p."}
{"id":"level4_028","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":64,"angle_A":41,"angle_B":77},"find":"AP","answer":70.6,"unit":"m","prompt":"A surveyor's baseline AB is 64 m. At A, the angle between the baseline and a mast P is 41°; at B it is 77°. Find AP, to 1 d.p."}
{"id":"level4_029","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":95,"angle_A":73,"angle_B":49},"find":"AP","answer":84.5,"unit":"m","prompt":"A surveyor's baseline AB is 95 m. At A, the angle between the baseline and a mast P is 73°; at B it is 49°. Find AP, to 1 d.p."}
{"id":"level4_030","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":175,"angle_A":44,"angle_B":68},"find":"AP","answer":175.0,"unit":"m","prompt":"A surveyor's baseline AB is 175 m. At A, the angle between the baseline and a mast P is 44°; at B it is 68°. Find AP, to 1 d.p."}
{"id":"level4_031","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":60,"angle_A":79,"angle_B":53},"find":"AP","answer":64.5,"unit":"m","prompt":"A surveyor's baseline AB is 60 m. At A, the angle between the baseline and a mast P is 79°; at B it is 53°. Find AP, to 1 d.p."}
{"id":"level4_032","rule":"sine","version":"sine-side","third_angle_first":true,"given":{"AB_m":230,"angle_A":61,"angle_B":47},"find":"AP","answer":176.9,"unit":"m","prompt":"A surveyor's baseline AB is 230 m. At A, the angle between the baseline and a mast P is 61°; at B it is 47°. Find AP, to 1 d.p."}
{"id":"level4_033","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":2.4,"b":3.1,"c":3.8},"find":"A","answer":39.1,"unit":"°","prompt":"A triangular frame has members of 3.1 m and 3.8 m meeting at joint A, and a member of 2.4 m opposite A. Find the angle at A, to 1 d.p."}
{"id":"level4_034","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":450,"b":380,"c":520},"find":"A","answer":57.5,"unit":"°","prompt":"A triangular frame has members of 380 m and 520 m meeting at joint A, and a member of 450 m opposite A. Find the angle at A, to 1 d.p."}
{"id":"level4_035","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":1.8,"b":2.5,"c":2.2},"find":"A","answer":44.5,"unit":"°","prompt":"A triangular frame has members of 2.5 m and 2.2 m meeting at joint A, and a member of 1.8 m opposite A. Find the angle at A, to 1 d.p."}
{"id":"level4_036","rule":"cosine","version":"cosine-angle","third_angle_first":false,"given":{"a":6,"b":7.5,"c":4.8},"find":"A","answer":53.0,"unit":"°","prompt":"A triangular frame has members of 7.5 m and 4.8 m meeting at joint A, and a member of 6 m opposite A. Find the angle at A, to 1 d.p."}
{"id":"level4_037","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":2.8,"c":3.5,"A":64},"find":"a","answer":3.4,"unit":"m","prompt":"Two members of 2.8 m and 3.5 m meet at joint A at 64°. Find the length of the member that closes the triangle, to 1 d.p."}
{"id":"level4_038","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":4.2,"c":3.1,"A":112},"find":"a","answer":6.1,"unit":"m","prompt":"Two members of 4.2 m and 3.1 m meet at joint A at 112°. Find the length of the member that closes the triangle, to 1 d.p."}
{"id":"level4_039","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":1.6,"c":2.4,"A":48},"find":"a","answer":1.8,"unit":"m","prompt":"Two members of 1.6 m and 2.4 m meet at joint A at 48°. Find the length of the member that closes the triangle, to 1 d.p."}
{"id":"level4_040","rule":"cosine","version":"cosine-side","third_angle_first":false,"given":{"b":5,"c":6.5,"A":97},"find":"a","answer":8.7,"unit":"m","prompt":"Two members of 5 m and 6.5 m meet at joint A at 97°. Find the length of the member that closes the triangle, to 1 d.p."}

DO NOT TOUCH:
- Any other game, schools/assets/ (use the shared assets, do not edit them), canon (home lane), escape-rooms/ and tools/pack-generator/.
- The bank's numbers, prompts, keys and ids. If you think an item is wrong, STOP; do not "fix" it.
- No listing, sitemap entry or portal card while unlisted.
- No draft PR.

SUCCESS CONDITION:
- /games/its-a-sine/ plays all four modes at all three levels.
- Stage 1 keys the rule, stage 2 the version and stage 3 the 1 d.p. answer, all through dataset.val or MaffsAnswer.
- Diagrams are drawn to shape with only the given values labelled.
- The two quotes show in teal and coral.
- verify-its-a-sine.py passes with every plant failing.
- check-site, phone-fit, answer-lock, check-levels, check-calculator and leaderboard coverage all pass.
- Unlisted.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover and todo committed.

STOP IF:
- Any bank answer disagrees with your independent recomputation (report the id and both values).
- An item's given data admits both rules (report it).
- A diagram cannot be drawn to shape at 360 px without hiding a label.
- A shared check needs an exemption for this game.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

AMENDMENT 1 (Project Claude; Jon's ruling, 17 Nov 2026, "Change the bank (Jon, 17 Nov 2026)"), verbatim:
Replace level3_015's given and answer, everything else in the item unchanged:
{"id":"level3_015","rule":"sine","version":"sine-angle","third_angle_first":false,"given":{"a":7.5,"b":10,"A":37},"find":"B","answer":126.6,"unit":"°","prompt":"Angle B is obtuse. Find angle B, to 1 d.p.","ambiguous":true}
(was a 6.5, b 8, A 46°, answer 117.7). Recomputed by coordinate geometry: B = 126.638°, and two triangles exist. Your verifier must agree independently; STOP if it does not. No ledger entry.
Also add a todo row, BANK-LINT-GIVEN: check-banks.py's question_signature() ignores numbers held outside the prompt (diagram data such as its-a-sine's "given"), so different items can read as duplicates. Fix it in its own contract.
Then let merge-pr.py carry on as before.
