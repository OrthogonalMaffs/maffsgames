=== PART 1 OF 3 ===
CIRCLE-WORKING, part 1 of 3. Do not start until parts 2 and 3 have arrived; part 3 ends with "END OF CONTRACT".
LANE: cloud. Send now. TIER: Small. MODEL: Claude Code, Sonnet 5.5, medium effort.

TASK: Circle Theorem Spotter (games/circle-theorem-spotter/index.html) shows the reason and the working on every wrong answer, not just the answer.

ROOT CAUSE: On main d41f900 (re-checked) a wrong answer shows only "The answer: X." (handle(), :471-475). It never says which theorem applies or how the angle follows, so a student who chose wrongly learns nothing. Canon 7.6: "Any pause must have something on screen worth reading". 604 answers since September.

CLASS CHECK: The class (wrong pauses with no reason) was surveyed in #838; each game's reasons are its own content, so this fixes this game only. The rest of the class is a todo row added here (item 5).

EXACT CHANGE:
1. First commit: close out PACK-WORDING-VERSIONS (#847, merge 504bae6, run 44701989506: read main's runs on its merge commit from the API, record them in its cloud.md entry, move its contract to docs/history/contracts/). Save this contract verbatim (all three parts) as docs/handover/contracts/2026-11-19-circle-working.md.
2. Add a WORKING object keyed by the item's position in QUESTIONS.gcse (1-55, as written on main), verbatim from parts 2 and 3. Each entry is a list of KaTeX lines (\text{} for words, ^\circ for degrees).
3. On a wrong answer, keep "The answer: X." and show that item's lines, one each, rendered with rk(), in a reference card titled "Why", above Next, built as Surd Simplifier's (WORKING-CARD; canon 7.6.2): a .maffs-ref-row with open and collapsed copies, swapped by the page's media query on height, thresholds measured over all 55 items in normal and Aa mode at the canon phone sizes and 1280x720; keep: the shown card passed to MaffsNext.wrong(). A right answer advances as now. The card clears on the next question.
4. scripts/verify-circle-theorem-spotter.py: every item has an entry; in each line, every "=" chain is true (degrees stripped; for items whose answer is an unknown, the unknown replaced by the item's key: x for items 25, 28, 31, 32, 48, 49; y for 50; OP 13 for 42; AB 8 for 54; d 3 for 55); in Chromium a wrong answer shows the item's lines before Next, with the card open, Next's bottom in page coordinates is within the fold for every item at every size where it opens; with it collapsed, Next ends where it would with no card (Surd's no-height rule). Project Claude ran that check on these 55: 0 failures. Plants that must FAIL: a false line (item 12's '180^\circ - 72^\circ = 108^\circ' made '= 118^\circ'); the card not shown on a wrong answer; the card moved below Next. Every existing check passes.
5. docs/todo.md §3: one row, WRONG-PAUSE-REASONS, from #838's CORRECTED survey (cloud.md, head 3f46a4c): answer shown with no reason (curling-friction, force-resolver, moments-master, given-that, equation-builder, percentage-flip, estimation-golf, wrong-on-the-internet, expected-damage); marks and Next only (proportion-blaster, standard-form-blitz A-Level, complex-converter Roulette); not traced (expectation-station, maths-court, tax-theft); 41 not driven. The four with no pause at all are a separate row, owned elsewhere. todo.md must not grow by more than this row.
6. One /updates/ line: "Circle Theorem Spotter: get one wrong and it now tells you which theorem, and why." cloud.md entry.
7. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: every item's figure, context, question, options and key; the figure renderer FIG; marking and scoring; schools/assets/; canon; docs/handover/home.md; any other game.

SUCCESS CONDITION: all 55 items have the working, shown on a wrong answer under "The answer"; the verifier's new check passes and both plants fail; phone fit no worse; todo row and /updates/ in; PACK-WORDING-VERSIONS closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: QUESTIONS.gcse doesn't have 55 items in the order quoted (report the first that differs from its working); a line fails item 4's check (report it; don't edit it); with the card collapsed, Next is below the fold at a size where the game fits now (report sizes and items); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
=== PART 2 OF 3 ===
CIRCLE-WORKING, part 2 of 3. WORKING entries 1 onwards (one object with part 3):
1:['\\text{The angle at the centre (2x) is twice the angle at the circumference (x), both standing on arc AB}'],
2:['\\text{C is on the circle and AB is a diameter, so angle ACB = }90^\\circ'],
3:['\\text{C and D are on the same arc and both stand on chord AB, so the two angles are equal}'],
4:['\\text{All four corners are on the circle, so opposite angles add up to }180^\\circ'],
5:['\\text{A tangent meets the radius at the point of contact at }90^\\circ'],
6:['\\text{The angle between tangent and chord equals the angle in the opposite (alternate) segment}'],
7:['\\text{From one outside point, the two tangents to a circle are the same length}'],
8:['\\text{The line from the centre perpendicular to a chord cuts it into two equal halves}'],
9:['\\text{Same arc AB: the angle at the centre is twice the angle at the circumference}'],
10:['\\text{AB is a diameter, so the angle in the semicircle is }90^\\circ'],
11:['\\text{Tangent and chord at A: the angle in the alternate segment equals it}'],
12:['\\text{Opposite angles of a cyclic quadrilateral add to }180^\\circ','180^\\circ - 72^\\circ = 108^\\circ'],
13:['\\text{Tangent meets radius at }90^\\circ\\text{, so angle OAT = }90^\\circ'],
14:['\\text{Two tangents from P are equal, so PB = PA = 8 cm}'],
15:['\\text{Angle at circumference is half the angle at the centre}','120^\\circ \\div 2 = 60^\\circ'],
16:['\\text{Angle at centre is twice the angle at the circumference}','2\\times 35^\\circ = 70^\\circ'],
17:['\\text{Angle at circumference is half the angle at the centre}','98^\\circ \\div 2 = 49^\\circ'],
18:['\\text{Angle at centre is twice the angle at the circumference}','2\\times 64^\\circ = 128^\\circ'],
19:['\\text{A point on the major arc stands on the minor arc, which makes 140}^\\circ\\text{ at the centre}','140^\\circ \\div 2 = 70^\\circ'],
20:['\\text{The major arc makes the reflex 260}^\\circ\\text{ at the centre; half of it is at the circumference}','260^\\circ \\div 2 = 130^\\circ'],
21:['\\text{Angle at centre is twice the angle at the circumference}','2\\times 90^\\circ = 180^\\circ'],
22:['\\text{A 180}^\\circ\\text{ angle at the centre means A, O and B are in a straight line, so AB passes through the centre: a diameter}'],
23:['\\text{C and D are in the same segment, standing on the same chord AB, so the angles are equal: }42^\\circ'],
24:['\\text{R and S are in the same segment, standing on chord PQ, so the angles are equal: }58^\\circ'],
25:['\\text{Angles in the same segment are equal}','x = 3x - 80','80 = 2x','x = 40^\\circ'],
26:['\\text{Angles in opposite segments of the same chord add up to }180^\\circ','180^\\circ - 75^\\circ = 105^\\circ'],
27:['\\text{Y and W are in the same segment, standing on chord XZ, so the angles are equal: }50^\\circ'],
28:['\\text{Angles in the same segment are equal}','2x + 10 = 3x - 20','x = 30'],
29:['\\text{C is opposite A in the cyclic quadrilateral}','180^\\circ - 85^\\circ = 95^\\circ'],
30:['\\text{D is opposite B in the cyclic quadrilateral}','180^\\circ - 100^\\circ = 80^\\circ'],
31:['\\text{A and C are opposite, so they add to }180^\\circ','x + 2x - 30 = 180','3x = 210','x = 70'],
32:['\\text{B and D are opposite, so they add to }180^\\circ','3x + 10 + 2x + 20 = 180','5x = 150','x = 30'],
=== PART 3 OF 3 ===
CIRCLE-WORKING, part 3 of 3. WORKING entries, the rest:
33:['\\text{R is opposite P in the cyclic quadrilateral}','180^\\circ - 110^\\circ = 70^\\circ'],
34:['\\text{C is opposite A and D is opposite B}','C = 180^\\circ - 94^\\circ = 86^\\circ\\text{ and }D = 180^\\circ - 87^\\circ = 93^\\circ','86^\\circ + 93^\\circ = 179^\\circ'],
35:['\\text{The tangent meets the radius at }90^\\circ\\text{, so angle OAT = }90^\\circ','90^\\circ - 25^\\circ = 65^\\circ'],
36:['\\text{Alternate segment theorem: the angle in the alternate segment equals the tangent-chord angle: }40^\\circ'],
37:['\\text{Alternate segment theorem: angle ACB equals the tangent-chord angle: }55^\\circ'],
38:['\\text{Alternate segment theorem works both ways: the tangent-chord angle equals the angle in the alternate segment: }62^\\circ'],
39:['\\text{Alternate segment theorem: the angle at the circumference standing on PQ is }48^\\circ','\\text{The angle at the centre is twice that}','2\\times 48^\\circ = 96^\\circ'],
40:['\\text{OAPB has two right angles where the tangents meet the radii}','360^\\circ - 90^\\circ - 90^\\circ - 50^\\circ = 130^\\circ'],
41:['\\text{OP cuts the 60}^\\circ\\text{ angle at P into two equal halves}','60^\\circ \\div 2 = 30^\\circ'],
42:['\\text{Tangent meets radius at }90^\\circ\\text{, so triangle OAP is right-angled at A}','OP^2 = 5^2 + 12^2 = 25 + 144 = 169','OP = \\sqrt{169} = 13\\text{ cm}'],
43:['\\text{Alternate segment theorem: the angle at the circumference standing on AB is }70^\\circ','\\text{The angle at the centre is twice that}','2\\times 70^\\circ = 140^\\circ'],
44:['\\text{Alternate segment theorem: angle CED equals the tangent-chord angle TCD: }35^\\circ'],
45:['\\text{AB is a diameter, so angle ACB = }90^\\circ','\\text{Angles in triangle ABC add to }180^\\circ','180^\\circ - 90^\\circ - 32^\\circ = 58^\\circ'],
46:['\\text{AB is a diameter and D is on the circle, so angle ADB is the angle in a semicircle: }90^\\circ'],
47:['\\text{Angle ADB = }90^\\circ\\text{ (semicircle), and the angles in triangle ABD add to }180^\\circ','180^\\circ - 90^\\circ - 28^\\circ = 62^\\circ'],
48:['\\text{Angle at centre = 2 × angle at circumference}','4x = 2(x + 30)','4x = 2x + 60','x = 30'],
49:['\\text{A and C are opposite, so they add to }180^\\circ','x + 20 + 2x + 10 = 180','3x = 150','x = 50'],
50:['\\text{B and D are opposite, so they add to }180^\\circ','3y + 2y + 30 = 180','5y = 150','y = 30'],
51:['\\text{C on the major arc stands on the minor arc: half the angle at the centre}','130^\\circ \\div 2 = 65^\\circ'],
52:['\\text{A point on the major arc would see }65^\\circ\\text{; D on the minor arc is opposite it in a cyclic quadrilateral}','180^\\circ - 65^\\circ = 115^\\circ'],
53:['\\text{Alternate segment theorem: angle BCA equals the tangent-chord angle BAT: }40^\\circ'],
54:['\\text{A 90}^\\circ\\text{ angle at the circumference stands on a diameter, so AC is the hypotenuse}','AB^2 = 10^2 - 6^2 = 100 - 36 = 64','AB = \\sqrt{64} = 8'],
55:['\\text{The perpendicular from the centre cuts the chord in half: 4 cm each side}','\\text{Pythagoras with the radius 5 cm as the hypotenuse}','d^2 = 5^2 - 4^2 = 25 - 16 = 9','d = \\sqrt{9} = 3\\text{ cm}'],
END OF CONTRACT
