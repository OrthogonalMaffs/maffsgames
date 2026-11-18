LANE: cloud (Claude Code on the web). SEND: now (CORE-PAPER-EXIT #816 and ITS-A-SINE-LIST #818 have merged). Jon teaches it Tue 24 Nov. Re-checked on main bb46787 (18 Nov 03:45): art branch art/i-dropped-my-ice-cream at 983c8f1, MaffsAnswer.decimal (schools/assets/answer.js:149), scripts/check-answer-inputs.py and games/its-a-sine/ all present; re-check any other file:line before editing.
TIER: Medium (a new game, plus entries in shared checks' lists; no shared asset changed). Merge on green, Project Claude reviews after.
RECOMMENDED: Opus 5.5, high effort. A new staged game with two levels, two-box answers, drawn diagrams, a 96-item bank, trap feedback and a verifier.
MERGE TIMING: one merge heading for main at a time. CANTEEN-APPROVE (home lane) may merge first; if any PR is in its Gate or merge when yours is green, wait, bring the branch up to date (merge main in; never force-push), then merge.

TASK: I-DROPPED-MY-ICE-CREAM. Build a new game, "I Dropped My Ice Cream" (slug i-dropped-my-ice-cream), at two levels (GCSE and Level 3). It covers:
- circumference → radius → area of a circle;
- cone volume;
- cone slant height and total surface area.
Merge it UNLISTED, so Jon can play it and use it with his class by URL.

ROOT CAUSE: No game on the site covers these:
- working back from a circumference to a radius;
- cone volume or cone surface area.
Take a Walk's stage 4 goes forwards only (radius → C or A). New Shapes stops at prisms. Jon needs it for his class on Tue 24 Nov, and his assessment asks exactly this (Q6: C = 220 mm → r, A; Q7: cone d 120 mm, h 180 mm → V, l, total surface area).

CLASS CHECK: A new build, not a fix. It reuses the shared layers and duplicates none of them:
- MaffsLevel.resolve, MaffsAnswer.decimal, MaffsLock, the calculator, MaffsLeaderboard, stage-exit.js, the theme and the start-art pattern.
It ships checked (canon SR-30): its verifier is in CI in this PR, it is in every shared check's MIGRATED lists, and it has a findings file docs/audits/findings/i-dropped-my-ice-cream.yml.
Pattern to follow: games/its-a-sine/index.html. It is light-themed (GCSE included, canon §7.5.1), has a level picker and stages, start art under the title, stage-exit, and was merged unlisted.

JON'S DECISIONS, 17 Nov 2026 (record verbatim in the PR body):
- 13:22: "the next game I will need for next week is about moving from circumference to radius and then onto area of a circle, and similar for a cone. This can also be a GCSE level question bank. "I dropped my ice cream" can be the name, for the cone shape".
- His answers to Project Claude (13:25–13:30):
  - one game, circle and cone;
  - two banks, GCSE and Level 3;
  - answers to 1 d.p. from full accuracy, with early rounding caught by its own feedback;
  - cone work matches his Q7 (forwards only).
- Feedback lines, verbatim (13:32, 13:34):
  - diameter used as the radius: "calm down bro, it's half that."
  - rounded too early: "save your rounding energy bruv, too soon, too soon."
  - the ⅓ left out: "just because we don't like fractions, that doesn't mean we can ignore them dude"
  - slant height from the diameter: "well it's definitely a number you calculated, it's just not what the question asked my friend"
  - curved surface only: "just cos you can't see the bottom, doesn't mean it aint there my man."
- Tagline (13:35), verbatim on the start screen: "Am I painting it or am I filling it? Surface area, volume, length. 3 different dimensions, 3 different calculations. You can move from one to the other if you're careful."
- Picture (13:37–13:41): accepted. It is on branch art/i-dropped-my-ice-cream (commit 983c8f1) as the original PNG "Sad Cone in a Sunlit School Hallway.png" (1672 × 941).

EXACT CHANGE:
0. First commit: close-outs per AGENTS.md for every merged PR not yet closed out on main, at least ITS-A-SINE-LIST: #818 merged as 71698a8 at 20:40:41 UTC via merge-pr.py, exit 0, last line "main 71698a8 run 44171822913: GREEN"; main on 71698a8: check-site 44171822913 success, phone-fit-full 44171822894 success, pages build 44171822226 success; PR's final checks on head 879b58e: Gate 44167827408, phone-fit-full 44167814376. Record: wall about 0:47 (contract 19:53, merged 20:40), review cycles 0, amendments 0, usage n/a. Move its contract to docs/history/contracts/.

1. games/i-dropped-my-ice-cream/index.html: one page on the shared assets.
   - Light theme (canon §7.5.1).
   - Title "I Dropped My Ice Cream", with the tagline under it.
   - Levels: MaffsLevel.resolve({slug: 'i-dropped-my-ice-cream', levels: ['gcse', 'level3'], fallback: 'gcse'}), with a level picker.
   - QUESTIONS[level] holds that level's 48 items from the bank below, verbatim.
   - Start picture: from art/i-dropped-my-ice-cream, take ONLY the PNG (do not merge or change the branch).
     - Convert it: crop box (0, 10, 1672, 922), Lanczos resize to 1600 × 873, WebP quality 80.
     - Save it to games/i-dropped-my-ice-cream/assets/start.webp and confirm it is 1600 × 873.
     - Insert it under the title, exactly as its-a-sine's start-art img and CSS, with alt "A sad ice cream cone upside down on a school corridor floor, its point to the sky, in a round puddle of melted strawberry ice cream".

2. Stages, keyed stage-1 … stage-4. Each run is 8 items drawn from that stage's 12, with no repeat within a run.
   - Stage 1 "Circumference to radius": one box, r.
   - Stage 2 "Circumference to area": two boxes, (a) r then (b) A, as in Jon's Q6.
   - Stage 3 "Cone volume": one box, V.
   - Stage 4 "Slant height and surface area": two boxes, (a) l then (b) A, as in Jon's Q7.
   - Formulas, in KaTeX (canon §7.1.1):
     - GCSE stages 1–2: NONE shown (GCSE students must recall C = 2πr and A = πr²).
     - GCSE stages 3–4: shown under the prompt, as on GCSE papers: V = \tfrac{1}{3}\pi r^2 h; l = \sqrt{r^2 + h^2}; A = \pi r^2 + \pi r l.
     - Level 3: every stage shows its formulas, as on Jon's paper: C = 2\pi r, A = \pi r^2, and the cone formulas above.
   - Marking: every box is marked by MaffsAnswer.decimal(raw, answer, 1). Every box is type="text" with inputmode="decimal" (no answer is negative). Units are shown beside the box: the length unit, unit², unit³.
   - Box (b) is marked against the bank's answer, which is worked from the UNROUNDED r or l. It is never marked against the student's own (a).
   - Trap feedback: when a wrong answer equals one of the box's trap values to 1 d.p., show Jon's line for that trap. Then, for every wrong answer, show the correct answer and the working. The trap keys map to his lines like this:
     - r.diameter, V.diameter → "calm down bro, it's half that."
     - A.early_rounding → "save your rounding energy bruv, too soon, too soon."
     - V.no_third → "just because we don't like fractions, that doesn't mean we can ignore them dude"
     - l.diameter → "well it's definitely a number you calculated, it's just not what the question asked my friend"
     - A.curved_only → "just cos you can't see the bottom, doesn't mean it aint there my man."
   - Working, after each answer:
     - stage 1: r = C ÷ 2π = r to 4 d.p.… → 1 d.p.;
     - stage 2: as stage 1, then A = πr² using the unrounded r;
     - stage 3: r = d ÷ 2, then V = ⅓πr²h;
     - stage 4: r = d ÷ 2, l = √(r² + h²) (unrounded), then A = πr² + πrl.
     Each "…" value is truncated, never rounded.
   - Calculator: scientific on every stage (canon "by stage", all four "scientific").
   - Leaderboard: each stage is a board under each level, as in its-a-sine. Submit only at a run's end.
   - stage-exit.js as in its-a-sine.

3. Diagrams: inline SVG, drawn from the item's given values.
   - Circle: the outline, with "C = <value> <unit>" written along the edge outside it, and a radius from the centre marked "r = ?" (stage 2 adds "A = ?" inside).
   - Cone: drawn to the true proportion of h to d:
     - the base as an ellipse, its back half dashed;
     - the height dashed from the apex to the base centre, labelled "h = <value> <unit>". The label must sit clear of the slant edge: Jon's own paper's label crosses it, and students read it as the slant height;
     - a diameter arrow under the base, "diameter = <value> <unit>";
     - stage 4 marks the slant edge "l = ?".
   - Label only the given values and the unknowns. Never mark r, l or A before they are answered.
   - Every diagram fits phone-fit at 360 px wide.

4. scripts/verify-i-dropped-my-ice-cream.py, in CI, with --selftest.
   - Recompute every answer and every trap value independently from "given", with exact decimals (40-digit π, half-up to 1 d.p.).
   - No answer within 0.005 of a 1 d.p. rounding boundary.
   - On stages 2 and 4, early_rounding ≠ the answer.
   - Every trap value ≠ its answer and ≠ the box's other traps.
   - 48 items per level (12 per stage); ids unique; no duplicate given within a level.
   - No item uses Jon's assessment numbers: C = 220; (d, h) = (120, 180); d = 120.
   - Every stage-4 prompt contains "solid".
   - In play:
     - each box marks its answer and only its answer;
     - each trap shows its line;
     - box (b) accepts the full-accuracy answer and rejects the early-rounded one;
     - the formula panel follows the level/stage rule above;
     - the calculator mounts on every stage.
   - Plants that must fail:
     - an answer 0.1 out;
     - box (b) marked against the rounded r;
     - a trap line swapped;
     - a GCSE stage 1 showing C = 2πr;
     - the height label crossing the slant edge;
     - a stage-4 prompt without "solid".

5. Integration, each as the repo already does it for a new game (follow its-a-sine's SINE-NOT-SINE PR):
   - a .claude/rules/game-roster.md row under Unlisted: levels GCSE, L3; topic Geometry; calculator scientific; "4 stages, 96 questions (48 per level)";
   - a data/games.json entry (unlisted), then apply-meta.py and check-meta.py;
   - the findings file;
   - the MIGRATED lists;
   - check-leaderboard-coverage.js NOT_ON_HUB with "new, unlisted until Jon has played and approved it; hub row added at listing";
   - /updates/: no line while unlisted;
   - docs/todo.md row ICE-CREAM-LIST: Jon plays all four stages at each level, then rules on listing (docs/todo.md is near its 153,600-byte cap: if the row does not fit, archive closed rows to docs/history/todo-done.md as the repo does);
   - docs/handover/cloud.md.

6. Merge with scripts/merge-pr.py <n> --watch --wait 3600 when the Gate is green (per MERGE TIMING). Report the live URLs:
   - https://maffsgames.co.uk/games/i-dropped-my-ice-cream/?level=gcse
   - https://maffsgames.co.uk/games/i-dropped-my-ice-cream/?level=level3

Run only the checks this contract names and the Gate; dispatch phone-fit-full on the branch. No optional all-game local runs.

THE BANK (verbatim; one item per line; 48 per level; ids give the level; answers to 1 d.p., computed by Project Claude and re-verified with exact decimals; trap values are the 1 d.p. results of each named mistake):
{"id":"gcse_001","stage":1,"given":{"C":93},"unit":"cm","prompt":"The circumference of a pizza is 93 cm. Find its radius, to 1 d.p.","answers":{"r":14.8},"traps":{"r":{"diameter":29.6}}}
{"id":"gcse_002","stage":1,"given":{"C":216},"unit":"cm","prompt":"The circumference of a bicycle wheel is 216 cm. Find its radius, to 1 d.p.","answers":{"r":34.4},"traps":{"r":{"diameter":68.8}}}
{"id":"gcse_003","stage":1,"given":{"C":363},"unit":"cm","prompt":"The circumference of a round table top is 363 cm. Find its radius, to 1 d.p.","answers":{"r":57.8},"traps":{"r":{"diameter":115.5}}}
{"id":"gcse_004","stage":1,"given":{"C":108},"unit":"cm","prompt":"The circumference of a clock face is 108 cm. Find its radius, to 1 d.p.","answers":{"r":17.2},"traps":{"r":{"diameter":34.4}}}
{"id":"gcse_005","stage":1,"given":{"C":61},"unit":"cm","prompt":"The circumference of a round cake tin is 61 cm. Find its radius, to 1 d.p.","answers":{"r":9.7},"traps":{"r":{"diameter":19.4}}}
{"id":"gcse_006","stage":1,"given":{"C":267},"unit":"cm","prompt":"The circumference of a hula hoop is 267 cm. Find its radius, to 1 d.p.","answers":{"r":42.5},"traps":{"r":{"diameter":85.0}}}
{"id":"gcse_007","stage":1,"given":{"C":20},"unit":"m","prompt":"The circumference of a garden pond is 20 m. Find its radius, to 1 d.p.","answers":{"r":3.2},"traps":{"r":{"diameter":6.4}}}
{"id":"gcse_008","stage":1,"given":{"C":15},"unit":"m","prompt":"The circumference of a trampoline is 15 m. Find its radius, to 1 d.p.","answers":{"r":2.4},"traps":{"r":{"diameter":4.8}}}
{"id":"gcse_009","stage":1,"given":{"C":80},"unit":"cm","prompt":"The circumference of a dinner plate is 80 cm. Find its radius, to 1 d.p.","answers":{"r":12.7},"traps":{"r":{"diameter":25.5}}}
{"id":"gcse_010","stage":1,"given":{"C":417},"unit":"cm","prompt":"The circumference of a round rug is 417 cm. Find its radius, to 1 d.p.","answers":{"r":66.4},"traps":{"r":{"diameter":132.7}}}
{"id":"gcse_011","stage":1,"given":{"C":46},"unit":"m","prompt":"The circumference of a roundabout is 46 m. Find its radius, to 1 d.p.","answers":{"r":7.3},"traps":{"r":{"diameter":14.6}}}
{"id":"gcse_012","stage":1,"given":{"C":181},"unit":"cm","prompt":"The circumference of a drum skin is 181 cm. Find its radius, to 1 d.p.","answers":{"r":28.8},"traps":{"r":{"diameter":57.6}}}
{"id":"gcse_013","stage":2,"given":{"C":24},"unit":"m","area_unit":"m²","prompt":"The circumference of a round flower bed is 24 m. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":3.8,"A":45.8},"traps":{"r":{"diameter":7.6},"A":{"early_rounding":45.4}}}
{"id":"gcse_014","stage":2,"given":{"C":73},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a frisbee is 73 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":11.6,"A":424.1},"traps":{"r":{"diameter":23.2},"A":{"early_rounding":422.7}}}
{"id":"gcse_015","stage":2,"given":{"C":228},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a round mirror is 228 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":36.3,"A":4136.8},"traps":{"r":{"diameter":72.6},"A":{"early_rounding":4139.6}}}
{"id":"gcse_016","stage":2,"given":{"C":833},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a paddling pool is 833 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":132.6,"A":55217.9},"traps":{"r":{"diameter":265.2},"A":{"early_rounding":55237.9}}}
{"id":"gcse_017","stage":2,"given":{"C":84},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a pie is 84 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":13.4,"A":561.5},"traps":{"r":{"diameter":26.7},"A":{"early_rounding":564.1}}}
{"id":"gcse_018","stage":2,"given":{"C":72},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a paint tin lid is 72 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":11.5,"A":412.5},"traps":{"r":{"diameter":22.9},"A":{"early_rounding":415.5}}}
{"id":"gcse_019","stage":2,"given":{"C":74},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a biscuit tin lid is 74 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":11.8,"A":435.8},"traps":{"r":{"diameter":23.6},"A":{"early_rounding":437.4}}}
{"id":"gcse_020","stage":2,"given":{"C":61},"unit":"m","area_unit":"m²","prompt":"The circumference of a helipad is 61 m. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":9.7,"A":296.1},"traps":{"r":{"diameter":19.4},"A":{"early_rounding":295.6}}}
{"id":"gcse_021","stage":2,"given":{"C":171},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a cymbal is 171 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":27.2,"A":2326.9},"traps":{"r":{"diameter":54.4},"A":{"early_rounding":2324.3}}}
{"id":"gcse_022","stage":2,"given":{"C":43},"unit":"m","area_unit":"m²","prompt":"The circumference of a circus ring is 43 m. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":6.8,"A":147.1},"traps":{"r":{"diameter":13.7},"A":{"early_rounding":145.3}}}
{"id":"gcse_023","stage":2,"given":{"C":304},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a round window is 304 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":48.4,"A":7354.2},"traps":{"r":{"diameter":96.8},"A":{"early_rounding":7359.4}}}
{"id":"gcse_024","stage":2,"given":{"C":141},"unit":"cm","area_unit":"cm²","prompt":"The circumference of a bin lid is 141 cm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":22.4,"A":1582.1},"traps":{"r":{"diameter":44.9},"A":{"early_rounding":1576.3}}}
{"id":"level3_001","stage":1,"given":{"C":309},"unit":"mm","prompt":"The circumference of a circular steel plate is 309 mm. Find its radius, to 1 d.p.","answers":{"r":49.2},"traps":{"r":{"diameter":98.4}}}
{"id":"level3_002","stage":1,"given":{"C":825},"unit":"mm","prompt":"The circumference of a flange is 825 mm. Find its radius, to 1 d.p.","answers":{"r":131.3},"traps":{"r":{"diameter":262.6}}}
{"id":"level3_003","stage":1,"given":{"C":888},"unit":"mm","prompt":"The circumference of a gasket is 888 mm. Find its radius, to 1 d.p.","answers":{"r":141.3},"traps":{"r":{"diameter":282.7}}}
{"id":"level3_004","stage":1,"given":{"C":199},"unit":"mm","prompt":"The circumference of a pulley wheel is 199 mm. Find its radius, to 1 d.p.","answers":{"r":31.7},"traps":{"r":{"diameter":63.3}}}
{"id":"level3_005","stage":1,"given":{"C":292},"unit":"mm","prompt":"The circumference of a grinding disc is 292 mm. Find its radius, to 1 d.p.","answers":{"r":46.5},"traps":{"r":{"diameter":92.9}}}
{"id":"level3_006","stage":1,"given":{"C":639},"unit":"mm","prompt":"The circumference of a flywheel is 639 mm. Find its radius, to 1 d.p.","answers":{"r":101.7},"traps":{"r":{"diameter":203.4}}}
{"id":"level3_007","stage":1,"given":{"C":625},"unit":"mm","prompt":"The circumference of a circular saw blade is 625 mm. Find its radius, to 1 d.p.","answers":{"r":99.5},"traps":{"r":{"diameter":198.9}}}
{"id":"level3_008","stage":1,"given":{"C":940},"unit":"mm","prompt":"The circumference of a brake disc is 940 mm. Find its radius, to 1 d.p.","answers":{"r":149.6},"traps":{"r":{"diameter":299.2}}}
{"id":"level3_009","stage":1,"given":{"C":280},"unit":"mm","prompt":"The circumference of a valve seat is 280 mm. Find its radius, to 1 d.p.","answers":{"r":44.6},"traps":{"r":{"diameter":89.1}}}
{"id":"level3_010","stage":1,"given":{"C":511},"unit":"mm","prompt":"The circumference of a bearing housing is 511 mm. Find its radius, to 1 d.p.","answers":{"r":81.3},"traps":{"r":{"diameter":162.7}}}
{"id":"level3_011","stage":1,"given":{"C":896},"unit":"mm","prompt":"The circumference of a manhole cover is 896 mm. Find its radius, to 1 d.p.","answers":{"r":142.6},"traps":{"r":{"diameter":285.2}}}
{"id":"level3_012","stage":1,"given":{"C":191},"unit":"mm","prompt":"The circumference of a shim disc is 191 mm. Find its radius, to 1 d.p.","answers":{"r":30.4},"traps":{"r":{"diameter":60.8}}}
{"id":"level3_013","stage":2,"given":{"C":382},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a clutch plate is 382 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":60.8,"A":11612.3},"traps":{"r":{"diameter":121.6},"A":{"early_rounding":11613.3}}}
{"id":"level3_014","stage":2,"given":{"C":203},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a cam disc is 203 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":32.3,"A":3279.3},"traps":{"r":{"diameter":64.6},"A":{"early_rounding":3277.6}}}
{"id":"level3_015","stage":2,"given":{"C":620},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a sprocket blank is 620 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":98.7,"A":30589.6},"traps":{"r":{"diameter":197.4},"A":{"early_rounding":30604.4}}}
{"id":"level3_016","stage":2,"given":{"C":517},"unit":"mm","area_unit":"mm²","prompt":"The circumference of an impeller disc is 517 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":82.3,"A":21270.2},"traps":{"r":{"diameter":164.6},"A":{"early_rounding":21278.9}}}
{"id":"level3_017","stage":2,"given":{"C":746},"unit":"mm","area_unit":"mm²","prompt":"The circumference of an end cap is 746 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":118.7,"A":44286.1},"traps":{"r":{"diameter":237.5},"A":{"early_rounding":44264.1}}}
{"id":"level3_018","stage":2,"given":{"C":661},"unit":"mm","area_unit":"mm²","prompt":"The circumference of an inspection cover is 661 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":105.2,"A":34769.1},"traps":{"r":{"diameter":210.4},"A":{"early_rounding":34768.1}}}
{"id":"level3_019","stage":2,"given":{"C":468},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a rotor blank is 468 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":74.5,"A":17429.4},"traps":{"r":{"diameter":149.0},"A":{"early_rounding":17436.6}}}
{"id":"level3_020","stage":2,"given":{"C":375},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a seal is 375 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":59.7,"A":11190.6},"traps":{"r":{"diameter":119.4},"A":{"early_rounding":11196.9}}}
{"id":"level3_021","stage":2,"given":{"C":253},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a spacer disc is 253 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":40.3,"A":5093.7},"traps":{"r":{"diameter":80.5},"A":{"early_rounding":5102.2}}}
{"id":"level3_022","stage":2,"given":{"C":548},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a sight glass is 548 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":87.2,"A":23897.4},"traps":{"r":{"diameter":174.4},"A":{"early_rounding":23888.2}}}
{"id":"level3_023","stage":2,"given":{"C":285},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a boss is 285 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":45.4,"A":6463.7},"traps":{"r":{"diameter":90.7},"A":{"early_rounding":6475.3}}}
{"id":"level3_024","stage":2,"given":{"C":832},"unit":"mm","area_unit":"mm²","prompt":"The circumference of a faceplate is 832 mm. Find (a) its radius and (b) its area, each to 1 d.p.","answers":{"r":132.4,"A":55085.4},"traps":{"r":{"diameter":264.8},"A":{"early_rounding":55071.4}}}
{"id":"gcse_025","stage":3,"given":{"d":7,"h":14},"unit":"cm","volume_unit":"cm³","prompt":"An ice cream cone is a cone with base diameter 7 cm and height 14 cm. Find its volume, to 1 d.p.","answers":{"V":179.6},"traps":{"V":{"diameter":718.4,"no_third":538.8}}}
{"id":"gcse_026","stage":3,"given":{"d":13,"h":24},"unit":"cm","volume_unit":"cm³","prompt":"A party hat is a cone with base diameter 13 cm and height 24 cm. Find its volume, to 1 d.p.","answers":{"V":1061.9},"traps":{"V":{"diameter":4247.4,"no_third":3185.6}}}
{"id":"gcse_027","stage":3,"given":{"d":29,"h":54},"unit":"cm","volume_unit":"cm³","prompt":"A traffic cone is a cone with base diameter 29 cm and height 54 cm. Find its volume, to 1 d.p.","answers":{"V":11889.4},"traps":{"V":{"diameter":47557.4,"no_third":35668.1}}}
{"id":"gcse_028","stage":3,"given":{"d":26,"h":49},"unit":"cm","volume_unit":"cm³","prompt":"A wizard's hat is a cone with base diameter 26 cm and height 49 cm. Find its volume, to 1 d.p.","answers":{"V":8671.8},"traps":{"V":{"diameter":34687.4,"no_third":26015.5}}}
{"id":"gcse_029","stage":3,"given":{"d":13,"h":9},"unit":"cm","volume_unit":"cm³","prompt":"A funnel is a cone with base diameter 13 cm and height 9 cm. Find its volume, to 1 d.p.","answers":{"V":398.2},"traps":{"V":{"diameter":1592.8,"no_third":1194.6}}}
{"id":"gcse_030","stage":3,"given":{"d":12,"h":30},"unit":"cm","volume_unit":"cm³","prompt":"A piping bag is a cone with base diameter 12 cm and height 30 cm. Find its volume, to 1 d.p.","answers":{"V":1131.0},"traps":{"V":{"diameter":4523.9,"no_third":3392.9}}}
{"id":"gcse_031","stage":3,"given":{"d":28,"h":17},"unit":"cm","volume_unit":"cm³","prompt":"A model volcano is a cone with base diameter 28 cm and height 17 cm. Find its volume, to 1 d.p.","answers":{"V":3489.3},"traps":{"V":{"diameter":13957.0,"no_third":10467.8}}}
{"id":"gcse_032","stage":3,"given":{"d":6,"h":3},"unit":"m","volume_unit":"m³","prompt":"A tepee is a cone with base diameter 6 m and height 3 m. Find its volume, to 1 d.p.","answers":{"V":28.3},"traps":{"V":{"diameter":113.1,"no_third":84.8}}}
{"id":"gcse_033","stage":3,"given":{"d":8,"h":9},"unit":"cm","volume_unit":"cm³","prompt":"A paper cup is a cone with base diameter 8 cm and height 9 cm. Find its volume, to 1 d.p.","answers":{"V":150.8},"traps":{"V":{"diameter":603.2,"no_third":452.4}}}
{"id":"gcse_034","stage":3,"given":{"d":35,"h":23},"unit":"cm","volume_unit":"cm³","prompt":"A lampshade is a cone with base diameter 35 cm and height 23 cm. Find its volume, to 1 d.p.","answers":{"V":7376.2},"traps":{"V":{"diameter":29504.8,"no_third":22128.6}}}
{"id":"gcse_035","stage":3,"given":{"d":2,"h":19},"unit":"cm","volume_unit":"cm³","prompt":"A carrot is a cone with base diameter 2 cm and height 19 cm. Find its volume, to 1 d.p.","answers":{"V":19.9},"traps":{"V":{"diameter":79.6,"no_third":59.7}}}
{"id":"gcse_036","stage":3,"given":{"d":5,"h":1},"unit":"m","volume_unit":"m³","prompt":"A pile of sand is a cone with base diameter 5 m and height 1 m. Find its volume, to 1 d.p.","answers":{"V":6.5},"traps":{"V":{"diameter":26.2,"no_third":19.6}}}
{"id":"gcse_037","stage":4,"given":{"d":12,"h":12},"unit":"cm","area_unit":"cm²","prompt":"A solid wooden cone is a solid cone with base diameter 12 cm and height 12 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":13.4,"A":366.0},"traps":{"l":{"diameter":17.0},"A":{"early_rounding":365.7,"curved_only":252.9}}}
{"id":"gcse_038","stage":4,"given":{"d":6,"h":19},"unit":"cm","area_unit":"cm²","prompt":"A cone-shaped candle is a solid cone with base diameter 6 cm and height 19 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":19.2,"A":209.6},"traps":{"l":{"diameter":19.9},"A":{"early_rounding":209.2,"curved_only":181.3}}}
{"id":"gcse_039","stage":4,"given":{"d":4,"h":16},"unit":"cm","area_unit":"cm²","prompt":"A unicorn horn is a solid cone with base diameter 4 cm and height 16 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":16.1,"A":113.9},"traps":{"l":{"diameter":16.5},"A":{"early_rounding":113.7,"curved_only":101.3}}}
{"id":"gcse_040","stage":4,"given":{"d":11,"h":20},"unit":"cm","area_unit":"cm²","prompt":"A model rocket nose cone is a solid cone with base diameter 11 cm and height 20 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":20.7,"A":453.4},"traps":{"l":{"diameter":22.8},"A":{"early_rounding":452.7,"curved_only":358.4}}}
{"id":"gcse_041","stage":4,"given":{"d":4,"h":12},"unit":"cm","area_unit":"cm²","prompt":"A solid chocolate cone is a solid cone with base diameter 4 cm and height 12 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":12.2,"A":89.0},"traps":{"l":{"diameter":12.6},"A":{"early_rounding":89.2,"curved_only":76.4}}}
{"id":"gcse_042","stage":4,"given":{"d":7,"h":7},"unit":"cm","area_unit":"cm²","prompt":"A spinning top is a solid cone with base diameter 7 cm and height 7 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":7.8,"A":124.5},"traps":{"l":{"diameter":9.9},"A":{"early_rounding":124.2,"curved_only":86.1}}}
{"id":"gcse_043","stage":4,"given":{"d":5,"h":8},"unit":"cm","area_unit":"cm²","prompt":"A pine cone is a solid cone with base diameter 5 cm and height 8 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":8.4,"A":85.5},"traps":{"l":{"diameter":9.4},"A":{"early_rounding":85.6,"curved_only":65.8}}}
{"id":"gcse_044","stage":4,"given":{"d":12,"h":15},"unit":"cm","area_unit":"cm²","prompt":"A cone-shaped crayon is a solid cone with base diameter 12 cm and height 15 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":16.2,"A":417.6},"traps":{"l":{"diameter":19.2},"A":{"early_rounding":418.5,"curved_only":304.5}}}
{"id":"gcse_045","stage":4,"given":{"d":7,"h":8},"unit":"cm","area_unit":"cm²","prompt":"A cone-shaped bath bomb is a solid cone with base diameter 7 cm and height 8 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":8.7,"A":134.5},"traps":{"l":{"diameter":10.6},"A":{"early_rounding":134.1,"curved_only":96.0}}}
{"id":"gcse_046","stage":4,"given":{"d":8,"h":14},"unit":"cm","area_unit":"cm²","prompt":"A wooden Christmas tree ornament is a solid cone with base diameter 8 cm and height 14 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":14.6,"A":233.2},"traps":{"l":{"diameter":16.1},"A":{"early_rounding":233.7,"curved_only":183.0}}}
{"id":"gcse_047","stage":4,"given":{"d":10,"h":8},"unit":"cm","area_unit":"cm²","prompt":"A cone-shaped paperweight is a solid cone with base diameter 10 cm and height 8 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":9.4,"A":226.7},"traps":{"l":{"diameter":12.8},"A":{"early_rounding":226.2,"curved_only":148.2}}}
{"id":"gcse_048","stage":4,"given":{"d":9,"h":7},"unit":"cm","area_unit":"cm²","prompt":"A cone of cheese is a solid cone with base diameter 9 cm and height 7 cm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":8.3,"A":181.3},"traps":{"l":{"diameter":11.4},"A":{"early_rounding":181.0,"curved_only":117.6}}}
{"id":"level3_025","stage":3,"given":{"d":62,"h":157},"unit":"mm","volume_unit":"mm³","prompt":"A solid metal cone (spike) is a cone with base diameter 62 mm and height 157 mm. Find its volume, to 1 d.p.","answers":{"V":157998.0},"traps":{"V":{"diameter":631992.1,"no_third":473994.1}}}
{"id":"level3_026","stage":3,"given":{"d":13,"h":18},"unit":"mm","volume_unit":"mm³","prompt":"A centre punch tip is a cone with base diameter 13 mm and height 18 mm. Find its volume, to 1 d.p.","answers":{"V":796.4},"traps":{"V":{"diameter":3185.6,"no_third":2389.2}}}
{"id":"level3_027","stage":3,"given":{"d":27,"h":11},"unit":"mm","volume_unit":"mm³","prompt":"A countersink bit tip is a cone with base diameter 27 mm and height 11 mm. Find its volume, to 1 d.p.","answers":{"V":2099.4},"traps":{"V":{"diameter":8397.5,"no_third":6298.1}}}
{"id":"level3_028","stage":3,"given":{"d":38,"h":76},"unit":"mm","volume_unit":"mm³","prompt":"A plumb bob is a cone with base diameter 38 mm and height 76 mm. Find its volume, to 1 d.p.","answers":{"V":28730.9},"traps":{"V":{"diameter":114923.6,"no_third":86192.7}}}
{"id":"level3_029","stage":3,"given":{"d":25,"h":52},"unit":"mm","volume_unit":"mm³","prompt":"A conical nozzle is a cone with base diameter 25 mm and height 52 mm. Find its volume, to 1 d.p.","answers":{"V":8508.5},"traps":{"V":{"diameter":34033.9,"no_third":25525.4}}}
{"id":"level3_030","stage":3,"given":{"d":75,"h":101},"unit":"mm","volume_unit":"mm³","prompt":"A conical hopper plug is a cone with base diameter 75 mm and height 101 mm. Find its volume, to 1 d.p.","answers":{"V":148734.8},"traps":{"V":{"diameter":594939.1,"no_third":446204.3}}}
{"id":"level3_031","stage":3,"given":{"d":47,"h":27},"unit":"mm","volume_unit":"mm³","prompt":"A valve cone is a cone with base diameter 47 mm and height 27 mm. Find its volume, to 1 d.p.","answers":{"V":15614.5},"traps":{"V":{"diameter":62458.0,"no_third":46843.5}}}
{"id":"level3_032","stage":3,"given":{"d":21,"h":9},"unit":"mm","volume_unit":"mm³","prompt":"A conical rivet head is a cone with base diameter 21 mm and height 9 mm. Find its volume, to 1 d.p.","answers":{"V":1039.1},"traps":{"V":{"diameter":4156.3,"no_third":3117.2}}}
{"id":"level3_033","stage":3,"given":{"d":116,"h":64},"unit":"mm","volume_unit":"mm³","prompt":"A cone pulley blank is a cone with base diameter 116 mm and height 64 mm. Find its volume, to 1 d.p.","answers":{"V":225457.4},"traps":{"V":{"diameter":901829.8,"no_third":676372.3}}}
{"id":"level3_034","stage":3,"given":{"d":10,"h":5},"unit":"mm","volume_unit":"mm³","prompt":"A drill point is a cone with base diameter 10 mm and height 5 mm. Find its volume, to 1 d.p.","answers":{"V":130.9},"traps":{"V":{"diameter":523.6,"no_third":392.7}}}
{"id":"level3_035","stage":3,"given":{"d":74,"h":28},"unit":"mm","volume_unit":"mm³","prompt":"A conical spacer is a cone with base diameter 74 mm and height 28 mm. Find its volume, to 1 d.p.","answers":{"V":40141.2},"traps":{"V":{"diameter":160564.7,"no_third":120423.5}}}
{"id":"level3_036","stage":3,"given":{"d":16,"h":11},"unit":"mm","volume_unit":"mm³","prompt":"A conical locating pin is a cone with base diameter 16 mm and height 11 mm. Find its volume, to 1 d.p.","answers":{"V":737.2},"traps":{"V":{"diameter":2948.9,"no_third":2211.7}}}
{"id":"level3_037","stage":4,"given":{"d":55,"h":45},"unit":"mm","area_unit":"mm²","prompt":"A conical bearing plug is a solid cone with base diameter 55 mm and height 45 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":52.7,"A":6932.0},"traps":{"l":{"diameter":71.1},"A":{"early_rounding":6928.8,"curved_only":4556.2}}}
{"id":"level3_038","stage":4,"given":{"d":18,"h":33},"unit":"mm","area_unit":"mm²","prompt":"A spray nozzle insert is a solid cone with base diameter 18 mm and height 33 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":34.2,"A":1221.6},"traps":{"l":{"diameter":37.6},"A":{"early_rounding":1221.5,"curved_only":967.1}}}
{"id":"level3_039","stage":4,"given":{"d":16,"h":33},"unit":"mm","area_unit":"mm²","prompt":"A lathe centre is a solid cone with base diameter 16 mm and height 33 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":34.0,"A":1054.5},"traps":{"l":{"diameter":36.7},"A":{"early_rounding":1055.6,"curved_only":853.4}}}
{"id":"level3_040","stage":4,"given":{"d":57,"h":54},"unit":"mm","area_unit":"mm²","prompt":"A conical buffer is a solid cone with base diameter 57 mm and height 54 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":61.1,"A":8018.7},"traps":{"l":{"diameter":78.5},"A":{"early_rounding":8022.4,"curved_only":5467.0}}}
{"id":"level3_041","stage":4,"given":{"d":129,"h":136},"unit":"mm","area_unit":"mm²","prompt":"A cast cone is a solid cone with base diameter 129 mm and height 136 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":150.5,"A":43570.1},"traps":{"l":{"diameter":187.4},"A":{"early_rounding":43566.0,"curved_only":30500.3}}}
{"id":"level3_042","stage":4,"given":{"d":22,"h":18},"unit":"mm","area_unit":"mm²","prompt":"A conical shaft end is a solid cone with base diameter 22 mm and height 18 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":21.1,"A":1109.1},"traps":{"l":{"diameter":28.4},"A":{"early_rounding":1109.3,"curved_only":729.0}}}
{"id":"level3_043","stage":4,"given":{"d":89,"h":81},"unit":"mm","area_unit":"mm²","prompt":"A solid conical plug is a solid cone with base diameter 89 mm and height 81 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":92.4,"A":19141.4},"traps":{"l":{"diameter":120.3},"A":{"early_rounding":19138.7,"curved_only":12920.2}}}
{"id":"level3_044","stage":4,"given":{"d":42,"h":48},"unit":"mm","area_unit":"mm²","prompt":"A taper plug is a solid cone with base diameter 42 mm and height 48 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":52.4,"A":4842.0},"traps":{"l":{"diameter":63.8},"A":{"early_rounding":4842.5,"curved_only":3456.5}}}
{"id":"level3_045","stage":4,"given":{"d":46,"h":18},"unit":"mm","area_unit":"mm²","prompt":"A conical stop is a solid cone with base diameter 46 mm and height 18 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":29.2,"A":3772.2},"traps":{"l":{"diameter":49.4},"A":{"early_rounding":3771.8,"curved_only":2110.3}}}
{"id":"level3_046","stage":4,"given":{"d":71,"h":69},"unit":"mm","area_unit":"mm²","prompt":"A conical float is a solid cone with base diameter 71 mm and height 69 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":77.6,"A":12613.3},"traps":{"l":{"diameter":99.0},"A":{"early_rounding":12613.7,"curved_only":8654.1}}}
{"id":"level3_047","stage":4,"given":{"d":45,"h":156},"unit":"mm","area_unit":"mm²","prompt":"A conical spike is a solid cone with base diameter 45 mm and height 156 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":157.6,"A":12731.5},"traps":{"l":{"diameter":162.4},"A":{"early_rounding":12730.5,"curved_only":11141.1}}}
{"id":"level3_048","stage":4,"given":{"d":64,"h":27},"unit":"mm","area_unit":"mm²","prompt":"A conical die is a solid cone with base diameter 64 mm and height 27 mm. Find (a) its slant height l and (b) its total surface area, each to 1 d.p.","answers":{"l":41.9,"A":7426.1},"traps":{"l":{"diameter":69.5},"A":{"early_rounding":7429.2,"curved_only":4209.1}}}
DO NOT TOUCH:
- Any other game, and schools/assets/ (use the shared assets; do not edit them).
- canon (home lane), escape-rooms/, tools/pack-generator/ (CANTEEN-APPROVE is working there).
- The branch art/i-dropped-my-ice-cream (do not delete, merge or change it).
- The bank's numbers, prompts, answers, traps and ids. If you think an item is wrong, STOP; do not "fix" it.
- Jon's feedback lines and tagline: verbatim, including his spelling and punctuation.
- No listing, sitemap entry or portal card while unlisted.
- No draft PR.

SUCCESS CONDITION:
- /games/i-dropped-my-ice-cream/ plays all four stages at both levels.
- Box (b) is marked from full accuracy, and each trap shows Jon's line.
- Formulas are shown per the level/stage rule.
- The diagrams are drawn to proportion, with the height label clear of the slant edge.
- The picture is under the title (1600 × 873).
- verify-i-dropped-my-ice-cream.py passes with every plant failing.
- check-site, phone-fit (dispatched on the branch), answer-lock, check-levels, check-calculator, check-answer-inputs, check-theme and leaderboard coverage all pass.
- Unlisted.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover and todo committed.

STOP IF:
- Any bank answer or trap disagrees with your independent recomputation (report the id and both values).
- A diagram cannot be drawn to proportion at 360 px without a label crossing an edge.
- The PNG on art/i-dropped-my-ice-cream is missing or not 1672 × 941.
- A shared check needs an exemption for this game.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

AMENDMENT 1 (Jon, 18 Nov 2026, in session, answering two questions from Code Claude: the contract asked for per-level boards "as in its-a-sine" and "no shared asset changed", but two keys and one launch date have no home outside schools/assets/):
- Boards, answer "Add 2 labels (Recommended)": lane exception, add 'gcse-stage-4':'GCSE · Stage 4' and 'level3-stage-4':'Level 3 · Stage 4' to LEVEL_NAMES in schools/assets/firebase-leaderboard.js. Additive only, its-a-sine's Amendment 1 pattern. Per-level boards as the contract asks.
- Launch date, answer "Yes, add the line (Recommended)": one additive line in schools/assets/launch-dates.json ("i-dropped-my-ice-cream": "2026-11-18"), recorded as a lane exception in the PR. No check exemption needed.
